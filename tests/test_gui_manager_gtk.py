#!/usr/bin/python3
"""Interface real com dados e operações restritos a pastas temporárias."""
from pathlib import Path
import copy,json,os,sys,tempfile,unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
os.environ['GSETTINGS_BACKEND']='memory'
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from gui_manager.app import Window
from gui_manager.engine import Manager
from gui_manager.profiles import default_profile
class GuiTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='gruvbox-gui-test-');self.addCleanup(self.temp.cleanup);self.home=Path(self.temp.name);(self.home/'Desktop').mkdir();self.manager=Manager(self.home,True);self.profile=default_profile(self.home,True)
  self.show=patch.object(Gtk.Widget,'show_all');self.show.start();self.addCleanup(self.show.stop)
  self.window=Window(self.manager,self.profile);self.addCleanup(self.window.destroy)
 def test_open_and_cancel_review_do_not_write(self):
  with patch.object(self.window,'confirm',return_value=False) as confirm:self.window.review()
  confirm.assert_called_once();self.assertFalse(self.manager.state.exists());self.assertEqual(self.window.notebook.get_n_pages(),5)
 def test_dependencies_selected_and_removed_together(self):
  self.window.select_all(False);self.window.checks['rain'].set_active(True);self.assertEqual(set(self.window.selected()),{'rain','workspaces'})
  self.window.checks['workspaces'].set_active(False);self.assertEqual(self.window.selected(),[])
 def test_uninstall_does_not_adopt_unmanaged_components(self):
  self.window.operation.set_active_id('uninstall');self.assertEqual(self.window.selected(),[]);self.assertTrue(all(not c.get_sensitive() for c in self.window.checks.values()))
 def test_language_and_modes_preserve_profile(self):
  self.window.profile['rain_volume']=19;self.window.lang='en';self.window.profile['language']='en';self.window.build();self.assertEqual(self.window.profile['rain_volume'],19);self.assertEqual(self.window.review_button.get_label(),'Review changes…')
 def test_no_package_install_on_open_or_cancel(self):
  with patch('gui_manager.app.subprocess.run') as run,patch.object(self.window,'confirm',return_value=False):self.window.install_dependencies()
  run.assert_not_called()
if __name__=='__main__':unittest.main(verbosity=2)
