#!/usr/bin/python3
from pathlib import Path
import importlib.util,importlib.machinery,json,tempfile,unittest,sqlite3,os,subprocess,xml.etree.ElementTree as ET
from unittest.mock import patch
R=Path(__file__).resolve().parents[1]
def load(name,path):
 loader=importlib.machinery.SourceFileLoader(name,str(path));spec=importlib.util.spec_from_loader(name,loader);m=importlib.util.module_from_spec(spec);loader.exec_module(m);return m
manager=load('manager',R/'scripts/manage.py');terminal=load('terminal',R/'payload/.local/bin/gruvbox-terminal');fullscreen=load('fullscreen',R/'payload/.local/bin/gruvbox-video-tela-cheia')
class AuditTests(unittest.TestCase):
 def test_flatpak_merge_preserves_other_settings(self):
  old='[Environment]\nCUSTOM_KEEP=enabled\n[Context]\nfilesystems=xdg-download;\n'
  merged=manager.merge_ini('[Environment]\nFONTCONFIG_FILE=/new/fonts.conf\n',old)
  self.assertIn('CUSTOM_KEEP=enabled',merged);self.assertIn('filesystems=xdg-download;',merged);self.assertIn('FONTCONFIG_FILE=/new/fonts.conf',merged)
 def test_menu_merge_preserves_other_entries(self):
  old='<Menu><Name>Applications</Name><Menu><Name>chrome-apps</Name><Include><Filename>other.desktop</Filename></Include></Menu><Menu><Name>Other</Name></Menu></Menu>'
  src=(R/'payload/.config/menus/applications-merged/user-chrome-apps.menu').read_text()
  result=ET.fromstring(manager.merge_menu(src,old));names={n.text for n in result.findall('.//Filename')}
  self.assertIn('other.desktop',names);self.assertTrue(any(n.text=='Other' for n in result.findall('.//Name')))
  twice=ET.fromstring(manager.merge_menu(src,manager.merge_menu(src,old)));self.assertEqual(len(twice.findall('.//Filename')),len(result.findall('.//Filename')))
 def test_terminal_does_not_pass_scoped_paths_to_commands(self):
  with tempfile.TemporaryDirectory(prefix='terminal-test-') as td:
   h=Path(td)/'usuário com espaços';h.mkdir()
   with patch.object(terminal.shutil,'which',return_value='/usr/bin/cool-retro-term'),patch.object(terminal.os,'execvpe') as launch,patch.dict(os.environ,{'XDG_DATA_HOME':'/normal/data','XDG_CONFIG_HOME':'/normal/config','XDG_CACHE_HOME':'/normal/cache'}):terminal.launch(['--','/bin/sh','-c','echo ok'],h)
   program,args,env=launch.call_args[0];self.assertEqual(program,'/usr/bin/cool-retro-term');self.assertIn('XDG_DATA_HOME=/normal/data',args);self.assertIn('XDG_CONFIG_HOME=/normal/config',args);self.assertIn('XDG_CACHE_HOME=/normal/cache',args)
   self.assertTrue(env['XDG_DATA_HOME'].endswith('/gruvbox-cinnamon/terminal-data'));self.assertEqual(args[-3:],['/bin/sh','-c','echo ok'])
 def test_terminal_profile_is_visual_only(self):
  root=R/'payload/.local/share/gruvbox-cinnamon/terminal-data';p=next(root.rglob('*.sqlite'));db=sqlite3.connect('file:'+str(p)+'?mode=ro',uri=True);rows=dict(db.execute('select setting,value from settings'));db.close()
  self.assertEqual(set(rows),{'_CURRENT_SETTINGS','_CURRENT_PROFILE'});prefs=json.loads(rows['_CURRENT_SETTINGS']);self.assertFalse(prefs['useCustomCommand']);self.assertEqual(prefs['customCommand'],'');self.assertNotIn('width',prefs);self.assertNotIn('height',prefs)
  self.assertEqual(json.loads(rows['_CURRENT_PROFILE']),json.loads((R/'profiles/terminal-visual.json').read_text())['profile'])
 def test_relax_preserves_celluloid_and_local_choice(self):
  with tempfile.TemporaryDirectory() as td:
   h=Path(td);video=h/'vídeo.mp4';video.write_bytes(b'file');result=type('Result',(),{'returncode':0,'stdout':str(video)+'\n'})()
   with patch.object(fullscreen.subprocess,'run',return_value=result),patch.object(fullscreen.shutil,'which',return_value='/usr/bin/celluloid'),patch.object(fullscreen.subprocess,'Popen') as call:fullscreen.main(h,'celluloid')
   self.assertEqual(call.call_args[0][0],['celluloid','--mpv-fullscreen=yes',str(video)])
 def test_preferences_are_explicit_and_private_data_excluded(self):
  d=json.loads((R/'settings.json').read_text());self.assertGreater(len(d),800);self.assertIn('/org/cinnamon/desktop/interface/first-day-of-week',d)
  self.assertFalse(any('looking-glass-history' in k or 'last-coordinates' in k for k in d));self.assertEqual(d['/org/cinnamon/desktop/background/picture-uri'],"''")
 def test_install_and_restore_merged_settings(self):
  with tempfile.TemporaryDirectory() as td:
   h=Path(td);(h/'Desktop').mkdir();p=h/'.local/share/flatpak/overrides/org.kde.kclock';p.parent.mkdir(parents=True);old='[Environment]\nCUSTOM_KEEP=yes\n[Context]\nfilesystems=xdg-download;\n';p.write_text(old)
   inst=manager.Installer(h,True);inst.install();self.assertIn('CUSTOM_KEEP=yes',p.read_text());self.assertIn('FONTCONFIG_FILE='+str(h),p.read_text())
   self.assertTrue((h/'.local/share/applications/Relax.desktop').exists());self.assertTrue((h/'.local/bin/gruvbox-terminal').exists());self.assertNotIn('__HOME__',(h/'.local/share/applications/Relax.desktop').read_text())
   inst.restore();self.assertEqual(p.read_text(),old);self.assertFalse((h/'.local/bin/gruvbox-terminal').exists())
if __name__=='__main__':unittest.main(verbosity=2)
