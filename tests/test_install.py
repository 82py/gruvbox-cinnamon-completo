#!/usr/bin/python3
"""Instalação completa apenas em HOME falso, sem DBus/GSettings reais."""
from pathlib import Path
import importlib.util,tempfile,json,unittest,subprocess
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('manager',R/'scripts/manage.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class InstallTest(unittest.TestCase):
 def home(self,d):
  h=Path(d)/'usuario-teste';(h/'Desktop').mkdir(parents=True);(h/'Desktop/documento.txt').write_text('preservar')
  (h/'.config').mkdir();(h/'.config/user-dirs.dirs').write_text('XDG_DESKTOP_DIR="$HOME/Desktop"\nXDG_DOWNLOAD_DIR="$HOME/Downloads"\n')
  p=h/'.local/share/icons/Gruvbox-Plus-Dark';p.parent.mkdir(parents=True);p.symlink_to(h/'tema-anterior')
  (h/'tema-anterior').mkdir();(h/'tema-anterior/teste').write_text('ícone anterior')
  (h/'fake-dconf.json').write_text('{"/org/cinnamon/theme/name":"\'Original\'"}')
  return h
 def test_full_install_uninstall(self):
  with tempfile.TemporaryDirectory(prefix='gruvbox-test-') as d:
   h=self.home(d);old=(h/'.config/user-dirs.dirs').read_text();i=m.Installer(h,True);i.install()
   self.assertTrue((h/'Espaços de trabalho Gruvbox/.atual').is_symlink())
   self.assertEqual((h/'Espaços de trabalho Gruvbox/.atual').resolve(),h/'Desktop')
   self.assertEqual((h/'Desktop/documento.txt').read_text(),'preservar')
   cfg=json.loads((h/'.local/share/gruvbox-cinnamon/espacos/configuracao.json').read_text());self.assertEqual(cfg['folders'][0],str(h/'Desktop'))
   funds=json.loads((h/'.local/share/gruvbox-cinnamon/espacos/fundos.json').read_text());self.assertTrue(all(e['image']=='' and e['video']=='' for e in funds['spaces'].values()))
   keys=json.loads((h/'fake-dconf.json').read_text());self.assertEqual(keys['/org/cinnamon/theme/name'],"'Gruvbox-Dark-BL-MOD-Sistema-Colorido'")
   # All source links must remain relative and valid after installation.
   base=h/'.local/share/icons/Gruvbox-Plus-Dark'
   for p in base.rglob('*'):
    if p.is_symlink():self.assertTrue(p.exists(),str(p))
   (h/'Espaços de trabalho Gruvbox/Espaço 2/criado-depois.txt').write_text('não apagar')
   # Shell and Python templates must be usable under the installing user's home.
   for name in ['raincarroof-start','raincarroof-stop','video-wallpaper','gruvbox-desinstalar']:
    p=h/'.local/bin'/name;self.assertNotIn('__HOME__',p.read_text());subprocess.run(['bash','-n',str(p)],check=True)
   i.restore()
   self.assertEqual((h/'.config/user-dirs.dirs').read_text(),old)
   self.assertTrue((h/'.local/share/icons/Gruvbox-Plus-Dark').is_symlink())
   self.assertEqual((h/'tema-anterior/teste').read_text(),'ícone anterior')
   self.assertEqual((h/'Espaços de trabalho Gruvbox/Espaço 2/criado-depois.txt').read_text(),'não apagar')
   self.assertEqual(json.loads((h/'fake-dconf.json').read_text()),{'/org/cinnamon/theme/name':"'Original'"})
 def test_failure_rolls_back(self):
  with tempfile.TemporaryDirectory(prefix='gruvbox-rollback-') as d:
   h=self.home(d);i=m.Installer(h,True);put=i.put;count=0
   def fail(*a,**kw):
    nonlocal count
    count+=1
    if count==3:raise RuntimeError('falha simulada')
    return put(*a,**kw)
   i.put=fail
   with self.assertRaisesRegex(RuntimeError,'falha simulada'):i.install()
   self.assertTrue((h/'.local/share/icons/Gruvbox-Plus-Dark').is_symlink())
   self.assertFalse((h/'.local/share/icons/Gruvbox-Sistema-Colorido').exists())
   self.assertEqual((h/'Desktop/documento.txt').read_text(),'preservar')
if __name__=='__main__':unittest.main(verbosity=2)
