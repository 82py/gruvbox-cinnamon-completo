#!/usr/bin/python3
"""Preserve external Nemo extension choices using temporary homes only."""
from pathlib import Path
import contextlib, copy, importlib.util, io, json, sys, tempfile, unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from gui_manager.engine import Manager
from gui_manager.profiles import default_profile, load

KEY = '/org/nemo/plugins/disabled-extensions'
CURRENT = "['ColumnExtension+NemoPython', 'OutroPlugin']"

class NemoExtensionPreferencesTests(unittest.TestCase):
 def setUp(self):
  self.temp = tempfile.TemporaryDirectory(prefix='gruvbox-nemo-policy-')
  self.addCleanup(self.temp.cleanup)
  self.home = Path(self.temp.name) / 'home'; self.home.mkdir(); (self.home/'Desktop').mkdir()
  self.fake = self.home/'fake-dconf.json'
  self.fake.write_text(json.dumps({KEY: CURRENT}))
  self.manager = Manager(self.home, True)
  self.profile = default_profile(self.home, True)
  self.profile.update(components=['nemo'], keep_installer=False)
 def legacy_modules(self):
  for index, rel in enumerate(('scripts/manage.py', 'payload/.local/share/gruvbox-cinnamon/manage.py')):
   spec = importlib.util.spec_from_file_location('nemo_policy_legacy_'+str(index), ROOT/rel)
   module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
   yield rel, module
 def seed_current(self, value=CURRENT):
  data = json.loads(self.fake.read_text()); data[KEY] = value; self.fake.write_text(json.dumps(data))
 def test_preset_and_default_profile_exclude_only_external_extension_list(self):
  values = json.loads((ROOT/'settings.json').read_text())
  self.assertNotIn(KEY, values); self.assertNotIn(KEY, self.profile['settings'])
  expected = {'/org/nemo/plugins/disabled-actions': '@as []',
              '/org/nemo/plugins/disabled-scripts': '@as []',
              '/org/nemo/extensions/nemo-media-columns/use-timeout': 'true',
              '/org/nemo/extensions/nemo-media-columns/timeout': '0.20000000000000001'}
  for key, value in expected.items(): self.assertEqual(values[key], value)
 def test_import_old_profile_discards_stale_empty_list(self):
  old = copy.deepcopy(self.profile); old['settings'][KEY] = '@as []'
  path = self.home/'old-profile.json'; path.write_text(json.dumps(old))
  self.assertNotIn(KEY, load(path)['settings'])
  self.assertEqual(self.manager.value(KEY), CURRENT)
 def test_gui_install_uninstall_preserves_current_list_despite_stale_profile(self):
  self.profile['settings'][KEY] = '@as []'
  self.assertNotIn(KEY, self.manager.plan(self.profile)['settings'])
  point = self.manager.apply(self.profile)
  self.assertEqual(self.manager.value(KEY), CURRENT)
  self.assertNotIn(KEY, self.manager.read_registry()['settings'])
  self.assertNotIn(KEY, next(p for p in self.manager.points() if p['id']==point)['settings'])
  self.manager.uninstall(['nemo'])
  self.assertEqual(self.manager.value(KEY), CURRENT)
 def test_restore_old_point_and_undo_preserve_current_disabled_plugins(self):
  point_id = self.manager.apply(self.profile)
  path = self.manager.state/'points'/point_id/'point.json'; point = json.loads(path.read_text())
  point['settings'][KEY] = {'group': 'nemo', 'value': '@as []'}
  point['registry_before']['settings'][KEY] = {'group': 'nemo', 'value': '@as []'}
  path.write_text(json.dumps(point))
  self.seed_current()
  undo_id = self.manager.restore_point(point_id, ['nemo'])
  self.assertEqual(self.manager.value(KEY), CURRENT)
  self.assertNotIn(KEY, self.manager.read_registry()['settings'])
  undo = next(p for p in self.manager.points() if p['id']==undo_id)
  self.assertNotIn(KEY, undo['settings'])
  self.manager.restore_point(undo_id, ['nemo'])
  self.assertEqual(self.manager.value(KEY), CURRENT)
 def test_rollback_old_snapshot_does_not_reset_current_list(self):
  plan = self.manager.plan(self.profile)
  point = self.manager._snapshot(plan['files'], plan['settings'], plan['groups'], 'apply')
  point['settings'][KEY] = {'group': 'nemo', 'value': '@as []'}
  self.manager._rollback(point)
  self.assertEqual(self.manager.value(KEY), CURRENT)
 def test_low_level_setters_ignore_stale_values_and_reset_requests(self):
  for value in ('@as []', None, "['UnrelatedOnly']"):
   self.manager.set(KEY, value); self.assertEqual(self.manager.value(KEY), CURRENT)
   for rel, module in self.legacy_modules():
    with self.subTest(legacy=rel, value=value):
     installer = module.Installer(self.home, True); installer.set(KEY, value)
     self.assertEqual(installer.get(KEY), CURRENT)
 def test_legacy_install_and_old_restore_journal_preserve_current_list(self):
  # A minimal package exercises the real installation/settings/restoration paths
  # without copying the full icon collection or touching the logged-in desktop.
  for index, (rel, module) in enumerate(self.legacy_modules()):
   with self.subTest(legacy=rel):
    package = Path(self.temp.name)/('package'+str(index)); package.mkdir(); (package/'docs').mkdir()
    (package/'manifest.json').write_text(json.dumps({'version':'test','units':[]}))
    (package/'app-icons.json').write_text('{}')
    (package/'settings.json').write_text(json.dumps({KEY:'@as []','/org/cinnamon/theme/name':"'Gruvbox-Test'"}))
    (package/'docs/ESPACOS-E-RAIN.md').write_text('Temporary test reference.\n')
    home = Path(self.temp.name)/('legacy-home'+str(index)); home.mkdir(); (home/'Desktop').mkdir()
    fake = home/'fake-dconf.json'; fake.write_text(json.dumps({KEY:CURRENT}))
    installer = module.Installer(home, True)
    with patch.object(module,'ROOT',package), contextlib.redirect_stdout(io.StringIO()):
     installer.install()
     self.assertEqual(installer.get(KEY), CURRENT)
     self.assertNotIn(KEY, installer.data['settings'])
     old = json.loads(installer.journal.read_text()); old['settings'][KEY] = '@as []'
     installer.journal.write_text(json.dumps(old)); installer.restore()
    self.assertEqual(json.loads(fake.read_text()), {KEY:CURRENT})
 def test_preferences_added_after_profile_creation_survive_apply_and_remove(self):
  later = "['ColumnExtension+NemoPython', 'OutroPlugin', 'DisabledAfterOpeningGUI']"
  self.seed_current(later); self.manager.apply(self.profile)
  self.assertEqual(self.manager.value(KEY), later)
  self.manager.uninstall(['nemo']); self.assertEqual(self.manager.value(KEY), later)

if __name__ == '__main__': unittest.main(verbosity=2)
