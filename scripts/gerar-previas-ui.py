#!/usr/bin/python3
"""Captura widgets reais com dados temporários, sem aplicar fundos ou iniciar Rain."""
from pathlib import Path
import importlib.util,json,os,sys,tempfile
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/imagens'
with tempfile.TemporaryDirectory(prefix='gruvbox-ui-demo-') as td:
    home=Path(td)
    os.environ.update(HOME=str(home),XDG_CONFIG_HOME=str(home/'.config'),XDG_DATA_HOME=str(home/'.local/share'),XDG_CACHE_HOME=str(home/'.cache'),GSETTINGS_BACKEND='memory')
    import gi
    gi.require_version('Gtk','3.0');from gi.repository import Gtk,Gdk
    from PIL import Image,ImageDraw
    css=Gtk.CssProvider();css.load_from_data(b'window, box {background-color: #282828; color: #ebdbb2;} button {background-image:none; background-color:#3c3836; color:#ebdbb2; border-color:#665c54;} label {color:#ebdbb2;}')
    Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(),css,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    def load(name,path):
        spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
    def capture(window,title,name):
        child=window.get_child();window.remove(child)
        outer=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=16);outer.set_border_width(20)
        label=Gtk.Label(label=title);outer.pack_start(label,False,False,0);outer.pack_start(child,True,True,0)
        note=Gtk.Label(label='Interface real / Actual UI · Dados de exemplo / Sample data');outer.pack_start(note,False,False,0)
        off=Gtk.OffscreenWindow();off.set_default_size(720,-1);off.add(outer)
        # show_all was suppressed for the original application window only.
        show(off)
        while Gtk.events_pending():Gtk.main_iteration_do(False)
        pix=off.get_pixbuf();assert pix;pix.savev(str(OUT/name),'png',[],[])
        off.destroy()
        with patch.object(Gtk,'main_quit'):window.destroy()
    show=Gtk.Widget.show_all
    base=ROOT/'payload/.local/share/gruvbox-cinnamon/espacos';sys.path.insert(0,str(base))
    folders=[home/f'Workspace-{i}' for i in range(1,5)]
    spaces={}
    for i,(folder,color) in enumerate(zip(folders,['#455b57','#5b523e','#3e505c','#514b3d']),1):
        folder.mkdir();(folder/['Work-notes.txt','Study-plan.txt','Playlist.txt','Personal-list.txt'][i-1]).write_text('Example only')
        background=home/f'demo-{i}.png';im=Image.new('RGB',(608,380),color);d=ImageDraw.Draw(im);d.ellipse((290,-80,750,400),fill='#665c54');im.save(background)
        spaces[str(i)]={'mode':'static','image':background.as_uri(),'fit':'zoom','video':''}
    (home/'configuracao.json').write_text(json.dumps({'enabled':True,'folders':list(map(str,folders))}))
    (home/'fundos.json').write_text(json.dumps({'spaces':spaces}))
    app=load('copy_preview',base/'copiar_entre_areas.py');app.BASE=home
    def copy_main():
        w=next(w for w in Gtk.Window.list_toplevels() if w.get_title()=='Copiar entre áreas')
        capture(w,'Copiar entre áreas / Copy between workspaces','copy-workspaces-preview.png')
    with patch.object(Gtk.Widget,'show_all'),patch.object(Gtk,'main',copy_main),patch.object(sys,'argv',['copy-demo',str(folders[0]/'Work-notes.txt')]):app.main()
    import espacos,fundos
    fundos.CFG=home/'fundos.json'
    # A filename for interface demonstration only; no media is bundled or played.
    video=home/'my-local-video.mp4';video.write_text('Interface demonstration only')
    data=json.loads(fundos.CFG.read_text());data['spaces']['1']['video']=str(video);fundos.CFG.write_text(json.dumps(data))
    import shutil
    icon=home/'.local/share/icons/raincarroof-white-noise.png';icon.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'payload/.local/share/icons/raincarroof-white-noise.png',icon)
    rain=load('rain_preview',ROOT/'payload/.local/lib/rain/painel.py');rain.current_space=lambda:'1'
    with patch.object(Gtk.Widget,'show_all'),patch.object(Gtk,'main_quit'):
        window=rain.RainWindow();capture(window,'Rain — vídeo local por área / Local video per workspace','rain-ui-preview.png')
    print('Prévias das interfaces geradas em conta temporária, sem executar ações.')
