#!/usr/bin/python3
"""Verifica fundo sem mídia e escolha do primeiro vídeo, sem tocar na sessão."""
from pathlib import Path
import sys,json,tempfile,unittest
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
