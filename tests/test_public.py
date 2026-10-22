#!/usr/bin/python3
"""Verifica código e contrato de segurança, sem uma sessão Cinnamon."""
from pathlib import Path
import ast,json,subprocess,unittest,importlib.util,tempfile
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('manager',R/'scripts/manage.py');manager=importlib.util.module_from_spec(spec);spec.loader.exec_module(manager)
class PublicTests(unittest.TestCase):
 def test_syntax(self):
  for p in R.rglob('*.py'):
   if p.name not in ['montar-local.py','escrever-documentacao.py']:ast.parse(p.read_text(),str(p))
  for p in list(R.glob('*.sh'))+list((R/'scripts').glob('*.sh')):
   subprocess.run(['bash','-n',str(p)],check=True)
  for p in [R/'payload/.local/bin'/n for n in ['video-wallpaper-tray']]:
   if p.exists():ast.parse(p.read_text())
 def test_manifest(self):
  manifest=json.loads((R/'manifest.json').read_text());targets=[u['target'] for u in manifest['units']]
  self.assertEqual(len(targets),len(set(targets)))
  for u in manifest['units']:
   self.assertFalse(Path(u['target']).is_absolute());self.assertNotIn('..',Path(u['target']).parts)
 def test_safe_paths(self):
  with tempfile.TemporaryDirectory() as d:
   h=Path(d);(h/'escape').symlink_to('/tmp')
   for rel in ['../escape','/tmp/file','escape/test']:
    with self.assertRaises(ValueError):manager.safe(h,rel)
 def test_dconf_keys(self):
  for key,v in json.loads((R/'settings.json').read_text()).items():
   self.assertTrue(key.startswith('/'));self.assertNotIn('//',key)
   self.assertNotIn('/home/',v);self.assertNotIn('looking-glass-history',key)
 def test_backup_restore_small(self):
  with tempfile.TemporaryDirectory() as d:
   h=Path(d);i=manager.Installer(h,True)
   (h/'original').write_text('anterior');(h/'fake-dconf.json').write_text('{"/test/key": "1"}')
   i.data={'sandbox':True,'files':[],'settings':{'/test/key':'1','/test/new':None},'status':'installing'};i.checkpoint()
   i.put('original',text='novo');i.put('link',symlink=str(h/'original'));i.set('/test/key','2');i.set('/test/new','true')
   (h/'original').write_text('alterado pelo usuário')
   i.restore()
   self.assertEqual((h/'original').read_text(),'anterior');self.assertFalse((h/'link').exists())
   self.assertEqual(json.loads((h/'fake-dconf.json').read_text()),{'/test/key':'1'})
   recovered=list(i.state.glob('alterados-*/original'));self.assertEqual(recovered[0].read_text(),'alterado pelo usuário')
if __name__=='__main__':unittest.main(verbosity=2)
