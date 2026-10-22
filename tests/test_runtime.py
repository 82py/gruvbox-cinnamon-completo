#!/usr/bin/python3
"""Verifica fundo sem mídia e escolha do primeiro vídeo, sem tocar na sessão."""
from pathlib import Path
import sys,json,tempfile,unittest,signal,os
from types import SimpleNamespace
from unittest.mock import MagicMock
from unittest.mock import patch
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'payload/.local/share/gruvbox-cinnamon/espacos'))
import fundos,espacos,raincarroof_por_espaco as rain
class Background:
 def __init__(self):self.values={}
 def get_string(self,k):return self.values.get(k,'')
 def set_string(self,k,v):self.values[k]=v
 def set_boolean(self,k,v):self.values[k]=v
class Display:
 def sync(self):pass
class RuntimeTests(unittest.TestCase):
 def test_version_guard_checks_immediately_during_early_boot(self):
  for current in ['validated','updated']:
   with self.subTest(current=current),tempfile.TemporaryDirectory() as td:
    root=MagicMock();root.get_full_property.return_value=SimpleNamespace(value=[0])
    display=MagicMock();display.screen.return_value.root=root;display.pending_events.return_value=0
    cfg={'enabled':True,'validated_versions':'validated','pointer':td+'/.atual','folders':[td+'/Desktop']}
    handlers={};states=[];background=MagicMock()
    def hook(sig,callback):handlers[sig]=callback
    def tick(*args):handlers[signal.SIGTERM](signal.SIGTERM,None);return ([],[],[])
    def saved(path,data):
     if path==Path(td)/'estado.json':states.append(data)
    with patch.object(espacos,'BASE',Path(td)),patch.object(espacos,'PENDING',Path(td)/'pending.json'),patch.object(espacos,'STATUS',Path(td)/'estado.json'),patch.dict(os.environ,{'XDG_SESSION_TYPE':'x11'}),patch('Xlib.display.Display',return_value=display),patch.object(espacos,'tag_wallpaper'),patch.object(espacos,'read',return_value=cfg),patch.object(espacos,'versions',return_value=current) as versions,patch.object(espacos.time,'monotonic',return_value=5),patch.object(espacos.signal,'signal',side_effect=hook),patch.object(espacos.select,'select',side_effect=tick),patch.object(espacos,'run',return_value=cfg['pointer']),patch.object(espacos.subprocess,'run',return_value=SimpleNamespace(returncode=0)),patch.object(espacos,'swap'),patch.object(espacos,'save',side_effect=saved),patch.object(espacos,'notify'),patch.object(fundos,'Controller',return_value=background):
     espacos.daemon()
    versions.assert_called_once();self.assertEqual(states[0]['estado']=='Ativo',current=='validated')
    background.apply.assert_called_once_with(0,disabled=current!='validated')
 def test_blank_wallpaper_without_media(self):
  with tempfile.TemporaryDirectory() as d:
   cfg=Path(d)/'fundos.json';cfg.write_text(json.dumps({'spaces':{'1':{'mode':'static','image':'','fit':'scaled','video':''}}}))
   c=fundos.Controller.__new__(fundos.Controller)
   c.d=Display();c.last=None;c.attempted=None;c.observed=None;c.active_index=None;c.state={'hidden':False};c.bg=Background();c.slideshow=Background()
   with patch.object(fundos,'CFG',cfg),patch.object(fundos,'windows',return_value=[]):c.apply(0)
   self.assertEqual(c.bg.values['picture-uri'],'');self.assertEqual(c.slideshow.values['slideshow-enabled'],False)
 def test_first_rain_start_opens_chooser_without_changing_mode(self):
  with tempfile.TemporaryDirectory() as d:
   cfg=Path(d)/'fundos.json';cfg.write_text(json.dumps({'spaces':{'2':{'mode':'static','video':''}}}))
   with patch.object(rain.app,'read',return_value={'enabled':True,'validated_versions':'test'}),patch.object(rain.app,'versions',return_value='test'),patch.object(rain,'current_space',return_value='2'),patch.object(fundos,'CFG',cfg),patch.object(rain.subprocess,'Popen') as launch:
    self.assertEqual(rain.control('start'),'2');self.assertIn('--choose',launch.call_args[0][0])
   self.assertEqual(json.loads(cfg.read_text())['spaces']['2']['mode'],'static')
if __name__=='__main__':unittest.main(verbosity=2)
