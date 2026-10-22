#!/usr/bin/python3
"""Testes do gerenciador exclusivamente em contas temporárias."""
from pathlib import Path
import copy,fcntl,json,os,sys,tempfile,unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from gui_manager.catalog import COMPONENTS,EXTENSIONS,AGGREGATE,array,closure,units
from gui_manager.profiles import default_profile,existing_workspace,validate,export,load
from gui_manager.engine import Manager,raw

class ManagerTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='gruvbox-manager-test-');self.addCleanup(self.temp.cleanup);self.home=Path(self.temp.name);(self.home/'Desktop').mkdir();self.document=self.home/'Desktop/original.txt';self.document.write_text('preservar')
  self.fake=self.home/'fake-dconf.json';self.fake.write_text(json.dumps({'/org/cinnamon/theme/name':"'Anterior'"}))
  self.manager=Manager(self.home,True);self.profile=default_profile(self.home,True);self.profile['keep_installer']=False
 def choose(self,*groups):
  profile=copy.deepcopy(self.profile);profile['components']=list(groups);return profile
 def test_catalog_covers_every_unit(self):
  self.assertEqual(len(units()),78)
  self.assertEqual(closure(['rain']),{'rain','workspaces'})
 def test_radio_is_excluded_and_existing_instance_preserved(self):
  self.assertNotIn('radio',COMPONENTS)
  self.assertFalse(any('Radio3.0@' in u['target'] for u,g in units()))
  key='/org/cinnamon/enabled-applets';instance='panel1:right:8:Radio3.0@claudiux:999'
  self.manager.set(key,raw([instance]));p=self.choose('panel');plan=self.manager.plan(p)
  self.assertIn(instance,array(plan['settings'][key]['value']))
 def test_remove_rain_keeps_workspace_and_media_configuration(self):
  p=self.choose('rain');p['workspaces']['spaces'][2].update(mode='raincarroof',video='/media/user-loop.mp4')
  self.manager.apply(p);point=self.manager.uninstall(['rain'])
  f=self.home/'.local/share/gruvbox-cinnamon/espacos/fundos.json';data=json.loads(f.read_text())
  self.assertEqual(data['spaces']['3']['mode'],'static');self.assertEqual(data['spaces']['3']['video'],'/media/user-loop.mp4')
  self.assertEqual(self.manager.read_registry()['groups'],['workspaces'])
  self.manager.restore_point(point,['rain']);self.assertEqual(json.loads(f.read_text())['spaces']['3']['mode'],'raincarroof')
 def test_legacy_workspace_rain_coupling(self):
  p=self.choose('workspaces');p['workspaces']['legacy_coupled_rain']=True
  self.assertEqual(validate(p),{'workspaces','rain'});self.manager.apply(p)
  with self.assertRaises(ValueError):self.manager.uninstall(['rain'])
 def test_open_profile_and_preview_do_not_write(self):
  before=self.fake.read_bytes();plan=self.manager.plan(self.choose('cursor'));preview=self.manager.preview(plan)
  self.assertGreater(preview['files'],0);self.assertFalse(self.manager.state.exists());self.assertEqual(before,self.fake.read_bytes())
 def test_component_install_and_uninstall_preserve_documents_and_settings(self):
  old=self.fake.read_bytes();point=self.manager.apply(self.choose('cursor'))
  self.assertTrue((self.home/'.icons/Gruvbox_Cursors_Dark').is_dir());self.assertEqual(self.manager.read_registry()['groups'],['cursor'])
  self.manager.uninstall(['cursor'])
  self.assertFalse((self.home/'.icons/Gruvbox_Cursors_Dark').exists());self.assertEqual(json.loads(old),json.loads(self.fake.read_text()));self.assertEqual(self.document.read_text(),'preservar');self.assertTrue(self.manager.points())
 def test_keep_other_component_on_partial_uninstall(self):
  self.manager.apply(self.choose('cursor','photo'));self.manager.uninstall(['cursor'])
  self.assertEqual(self.manager.read_registry()['groups'],['photo']);self.assertTrue((self.home/'.local/share/cinnamon/extensions/gruvbox-profile-photo@gruvbox-cinnamon').exists());self.assertIn('gruvbox-profile-photo@gruvbox-cinnamon',array(self.manager.value(AGGREGATE)))
 def test_partial_restore_preserves_later_unrelated_extension(self):
  point=self.manager.apply(self.choose('photo'));key=AGGREGATE
  self.manager.set(key,raw(array(self.manager.value(key))+['external-animation@example.invalid']))
  self.manager.restore_point(point,['photo'])
  self.assertEqual(self.manager.read_registry()['groups'],[]);self.assertIn('external-animation@example.invalid',array(self.manager.value(key)));self.assertNotIn('gruvbox-profile-photo@gruvbox-cinnamon',array(self.manager.value(key)))
 def test_magic_lamp_is_not_distributed_or_enabled_by_preset(self):
  self.assertNotIn('effects',COMPONENTS)
  self.assertFalse(any('MagicLamp' in u['target'] for u,g in units()))
  self.assertFalse(any('MagicLamp' in x for x in array(self.profile['settings'][AGGREGATE])))
 def test_failure_rolls_back(self):
  original=self.fake.read_bytes();write=self.manager._write;calls=0
  def fail(entry):
   nonlocal calls
   calls+=1
   if calls==2:raise OSError('falha simulada')
   return write(entry)
  with patch.object(self.manager,'_write',side_effect=fail):
   with self.assertRaisesRegex(OSError,'falha simulada'):self.manager.apply(self.choose('cursor'))
  self.assertEqual(json.loads(original),json.loads(self.fake.read_text()));self.assertFalse((self.home/'.icons/Gruvbox_Cursors_Dark').exists());self.assertEqual(self.manager.read_registry()['groups'],[]);self.assertEqual(self.manager.points()[0]['status'],'rolled_back')
 def test_modified_files_kept_in_new_restore_point(self):
  self.manager.apply(self.choose('photo'));f=self.home/'.local/share/cinnamon/extensions/gruvbox-profile-photo@gruvbox-cinnamon/metadata.json';f.write_text('modificado pelo usuário')
  point=self.manager.uninstall(['photo']);history=next(p for p in self.manager.points() if p['id']==point);entry=next(e for e in history['files'] if e['target'].endswith('gruvbox-profile-photo@gruvbox-cinnamon'))
  self.assertEqual((self.manager._blob(point,entry['backup'])/'metadata.json').read_text(),'modificado pelo usuário')
 def test_snapshot_restores_previous_customization(self):
  p=self.choose('cursor');self.manager.apply(p);p['settings']['/org/cinnamon/desktop/interface/cursor-size']='48';point=self.manager.apply(p);self.assertEqual(self.manager.value('/org/cinnamon/desktop/interface/cursor-size'),'48')
  self.manager.restore_point(point,['cursor']);self.assertNotEqual(self.manager.value('/org/cinnamon/desktop/interface/cursor-size'),'48');self.assertEqual(self.manager.read_registry()['groups'],['cursor'])
 def test_workspace_documents_survive_install_remove(self):
  folders=[self.home/'Desktop']+[self.home/f'own{i}' for i in range(2,5)]
  for folder in folders[1:]:folder.mkdir();(folder/'dados.txt').write_text('manter')
  p=self.choose('workspaces')
  for e,folder in zip(p['workspaces']['spaces'],folders):e['folder']=str(folder)
  self.manager.apply(p);config=json.loads((self.home/'.local/share/gruvbox-cinnamon/espacos/configuracao.json').read_text());self.assertEqual(config['folders'],list(map(str,folders)))
  self.manager.uninstall(['workspaces'])
  for folder in folders[1:]:self.assertEqual((folder/'dados.txt').read_text(),'manter')
  self.assertEqual(self.document.read_text(),'preservar')
 def test_import_legacy_workspace_without_moving_it(self):
  base=self.home/'old/scripts';base.mkdir(parents=True);folders=[self.home/'Desktop']+[self.home/f'own{i}' for i in range(2,5)];config={'folders':list(map(str,folders)),'folder_root':str(self.home/'old'),'pointer':str(self.home/'old/.atual'),'enabled':True};(base/'configuracao.json').write_text(json.dumps(config));(base/'fundos.json').write_text(json.dumps({'original':{'image':'file:///sample.png','fit':'zoom','slideshow':False},'spaces':{str(i):{'mode':'static','image':'file:///sample.png','video':'/sample.mp4','fit':'scaled'} for i in range(1,5)}}));auto=self.home/'.config/autostart/espacos-de-trabalho.desktop';auto.parent.mkdir(parents=True);auto.write_text('Exec=/usr/bin/python3 "'+str(base/'espacos.py')+'" login\n')
  profile=default_profile(self.home,True);self.assertEqual(profile['workspaces']['spaces'][0]['image'],'file:///sample.png');self.assertEqual(profile['workspaces']['spaces'][1]['folder'],str(folders[1]))
 def test_refuse_replacing_real_workspace_pointer(self):
  p=self.choose('workspaces');pointer=Path(p['workspaces']['pointer']);pointer.mkdir(parents=True);(pointer/'keep').write_text('preservar')
  with self.assertRaises(ValueError):self.manager.plan(p)
  self.assertEqual((pointer/'keep').read_text(),'preservar')
 def test_symlink_escape_refused(self):
  (self.home/'.icons').symlink_to('/tmp')
  with self.assertRaises(ValueError):self.manager.plan(self.choose('cursor'))
 def test_unrelated_shortcuts_preserved(self):
  data=json.loads(self.fake.read_text());data.update({'/org/cinnamon/desktop/keybindings/custom-list':"['custom0']",'/org/cinnamon/desktop/keybindings/custom-keybindings/custom0/name':"'Meu atalho'",'/org/cinnamon/desktop/keybindings/custom-keybindings/custom0/command':"'my-command'"});self.fake.write_text(json.dumps(data))
  self.manager.apply(self.choose('relax'));self.assertEqual(self.manager.value('/org/cinnamon/desktop/keybindings/custom-keybindings/custom0/command'),"'my-command'");self.assertEqual(array(self.manager.value('/org/cinnamon/desktop/keybindings/custom-list')),['custom0','custom1'])
  self.manager.uninstall(['relax']);self.assertEqual(json.loads(self.fake.read_text()),data)
 def test_parallel_operation_refused(self):
  with self.manager.lock():
   with self.assertRaises(RuntimeError):self.manager.apply(self.choose('cursor'))
 def test_profile_roundtrip(self):
  p=self.home/'profile.json';export(p,self.profile);self.assertEqual(load(p),self.profile);self.assertEqual(p.stat().st_mode&0o777,0o600)
 def test_restore_dependency_guard(self):
  with self.assertRaises(ValueError):self.manager._validate_remaining({'rain'})
 def test_cancellation_rolls_back_partial_file_copy(self):
  calls=0
  def cancel(_):
   nonlocal calls
   calls+=1
   if calls==2:raise RuntimeError('cancelado')
  self.manager.progress=cancel
  with self.assertRaisesRegex(RuntimeError,'cancelado'):self.manager.apply(self.choose('cursor'))
  self.assertFalse((self.home/'.icons/Gruvbox_Cursors_Dark').exists());self.assertEqual(self.manager.read_registry()['groups'],[])
 def test_interrupted_operation_can_be_recovered(self):
  p=self.manager.plan(self.choose('cursor'));point=self.manager._snapshot(p['files'],p['settings'],p['groups'],'apply');point['status']='applying';self.manager.save(self.manager.state/'points'/point['id']/'point.json',point)
  self.manager._write(p['files'][0]);self.assertTrue((self.home/'.icons/Gruvbox_Cursors_Dark').exists())
  with self.assertRaises(RuntimeError):self.manager.apply(self.choose('photo'))
  self.manager.recover(point['id']);self.assertFalse((self.home/'.icons/Gruvbox_Cursors_Dark').exists());self.assertEqual(self.manager.points()[0]['status'],'rolled_back')
 def test_folder_color_overlay_and_dependency_removal(self):
  p=self.choose('folder_colors');p['folder_color']='blue';self.manager.apply(p)
  target=self.home/'.local/share/icons/Gruvbox-Pastas-Coloridas-A/places/scalable/folder.svg'
  from gui_manager.catalog import ROOT
  self.assertEqual(target.read_bytes(),(ROOT/'payload/.local/share/icons/Gruvbox-Plus-Dark/places/scalable/folder-blue.svg').read_bytes())
  cursor=self.choose('cursor');cursor['settings']['/org/cinnamon/desktop/interface/icon-theme']=raw('Gruvbox-Pastas-Coloridas-A');self.manager.apply(cursor)
  self.manager.uninstall(['folder_colors']);self.assertEqual(self.manager.value('/org/cinnamon/desktop/interface/icon-theme'),raw('Gruvbox-Sistema-Colorido'))
  self.manager.uninstall(['system']);self.assertEqual(self.manager.value('/org/cinnamon/desktop/interface/icon-theme'),raw('Gruvbox-Plus-Dark'))
  self.manager.uninstall(['icons','themes','cursor']);self.assertIsNone(self.manager.value('/org/cinnamon/desktop/interface/icon-theme'))
 def test_sandbox_refuses_real_home(self):
  with self.assertRaises(ValueError):Manager(Path.home(),True)
 def test_profile_rejects_shared_or_nested_workspaces(self):
  self.profile['workspaces']['spaces'][1]['folder']=str(self.home/'Desktop/subfolder')
  with self.assertRaises(ValueError):validate(self.profile)
if __name__=='__main__':unittest.main(verbosity=2)
