#!/usr/bin/python3
"""GTK real, janelas ocultas e dados temporários: não usa a conta pessoal."""
from pathlib import Path
import importlib.util,json,os,sys,tempfile,time,unittest
from unittest.mock import patch
os.environ['GSETTINGS_BACKEND']='memory'
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'payload/.local/share/gruvbox-cinnamon/espacos/copiar_entre_areas.py'
spec=importlib.util.spec_from_file_location('copy_dialog',SCRIPT)
app=importlib.util.module_from_spec(spec);spec.loader.exec_module(app)

def pump():
    while Gtk.events_pending():Gtk.main_iteration_do(False)

def wait(window):
    deadline=time.monotonic()+5
    while window.busy and time.monotonic()<deadline:
        pump();time.sleep(.005)
    pump()
    if window.busy:raise AssertionError('A cópia não terminou no prazo.')

class CopyDialogTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='gruvbox-copy-regression-')
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.folders=[self.root/str(i) for i in range(4)]
        for folder in self.folders:folder.mkdir()
        (self.root/'configuracao.json').write_text(json.dumps({'enabled':True,'folders':list(map(str,self.folders))}))
        self.source=self.folders[0]/'arquivo.txt';self.source.write_text('original de teste')
        self.base=patch.object(app,'BASE',self.root);self.base.start();self.addCleanup(self.base.stop)

    def exercise(self,args,action):
        def main():
            window=next(w for w in Gtk.Window.list_toplevels() if w.get_title()=='Copiar entre áreas')
            try:action(window)
            finally:window.destroy();pump()
        with patch.object(sys,'argv',[str(SCRIPT),*map(str,args)]),patch.object(Gtk,'main',main),patch.object(Gtk.Widget,'show_all'),patch.object(Gtk.MessageDialog,'run',return_value=Gtk.ResponseType.CLOSE):
            app.main()

    def test_repeated_clicks_copy_once_close_and_notify(self):
        def action(window):
            destroyed=[];window.connect('destroy',lambda *_:destroyed.append(True))
            with patch.object(app,'copy_batch',wraps=app.copy_batch) as batches,patch.object(app,'notify_completed') as notice:
                for _ in range(20):window.clicked(None,self.folders[1],2)
                wait(window)
                for _ in range(20):window.clicked(None,self.folders[1],2)
                self.assertFalse(window.start_copy([self.source],self.folders[1],2))
                self.assertEqual(batches.call_count,1)
                self.assertEqual(list(self.folders[1].iterdir()),[self.folders[1]/self.source.name])
                self.assertEqual((self.folders[1]/self.source.name).read_bytes(),self.source.read_bytes())
                self.assertTrue(window.completed);self.assertFalse(window.sources);self.assertTrue(destroyed)
                notice.assert_called_once_with(2,1)
        self.exercise(['--',self.source],action)

    def test_partial_failure_does_not_repeat_successful_items(self):
        special=self.folders[0]/'especial';os.mkfifo(special)
        def action(window):
            destroyed=[];window.connect('destroy',lambda *_:destroyed.append(True))
            with patch.object(app,'copy_batch',wraps=app.copy_batch) as batches,patch.object(app,'notify_completed') as notice,patch.object(Gtk.MessageDialog,'run',return_value=Gtk.ResponseType.CLOSE) as warning:
                window.clicked(None,self.folders[2],3);wait(window)
                for _ in range(20):window.clicked(None,self.folders[2],3)
                self.assertEqual(batches.call_count,1)
                self.assertEqual(len(list(self.folders[2].iterdir())),1)
                self.assertTrue(window.completed);self.assertTrue(destroyed);self.assertFalse(window.sources)
                warning.assert_called_once();notice.assert_not_called()
        self.exercise([self.source,special],action)
        self.assertEqual(self.source.read_text(),'original de teste');self.assertTrue(special.exists())

    def test_standalone_drag_mode_allows_new_operations(self):
        def action(window):
            self.assertFalse(window.one_shot)
            self.assertTrue(window.start_copy([self.source],self.folders[3],4));wait(window)
            self.assertFalse(window.completed)
            self.assertTrue(window.start_copy([self.source],self.folders[3],4));wait(window)
            self.assertEqual(len(list(self.folders[3].iterdir())),2)
        self.exercise([],action)

    def test_missing_notification_command_does_not_block_completion(self):
        with patch.object(app.subprocess,'Popen',side_effect=FileNotFoundError):
            app.notify_completed(2,1)

if __name__=='__main__':unittest.main(verbosity=2)
