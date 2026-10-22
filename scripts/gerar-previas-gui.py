#!/usr/bin/python3
"""Previews with temporary sample data; never reads the personal desktop."""
import os,sys,tempfile
from pathlib import Path
os.environ['GSETTINGS_BACKEND']='memory'
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
from gui_manager.app import Window
from gui_manager.engine import Manager
from gui_manager.profiles import default_profile
with tempfile.TemporaryDirectory(prefix='gruvbox-preview-') as td:
 home=Path(td);(home/'Desktop').mkdir();p=default_profile(home,True)
 # Readable examples only, never exported as an installable profile.
 p['workspaces']['folder_root']='$HOME/Espaços de trabalho'
 for i,s in enumerate(p['workspaces']['spaces'],1):s['folder']='$HOME/Espaços de trabalho/Espaço '+str(i)
 w=Window(Manager(home,True),p);w.hide();child=w.get_child();w.remove(child)
 off=Gtk.OffscreenWindow();off.set_border_width(18);off.set_size_request(1140,850);off.add(child);off.show_all();w.points_combo.hide()
 for page,name in [(0,'componentes'),(1,'aparencia'),(2,'espacos')]:
  w.notebook.set_current_page(page)
  while Gtk.events_pending():Gtk.main_iteration_do(False)
  off.get_pixbuf().savev(str(ROOT/('PREVIA-GUI-'+name+'.png')),'png',[],[])
 off.destroy();w.destroy()
