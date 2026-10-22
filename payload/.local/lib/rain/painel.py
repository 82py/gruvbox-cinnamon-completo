#!/usr/bin/python3
"""Rain: vídeos locais por área de trabalho, sem modificar os arquivos de mídia."""
from pathlib import Path
import json, subprocess, sys, time, threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
BASE=Path.home()/".local/share/gruvbox-cinnamon/espacos"
sys.path.insert(0,str(BASE))
import espacos, fundos
from raincarroof_por_espaco import current_space
DEFAULT=Path.home()/"Vídeos/escolha-um-video.mp4"
TARGET_SPACE=next((a.split("=",1)[1] for a in sys.argv if a.startswith("--space=")),None)
if TARGET_SPACE not in (None,"1","2","3","4"):raise ValueError("Espaço inválido")
EXT={".mp4",".webm",".mkv",".mov",".avi",".m4v"}
def validate_video(path):
    path=Path(path).expanduser().resolve(strict=True)
    if not path.is_file():raise ValueError("Escolha um arquivo de vídeo.")
    r=subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=codec_type","-of","json",str(path)],capture_output=True,text=True,timeout=15)
    if r.returncode or not json.loads(r.stdout).get("streams"):raise ValueError("O arquivo não contém um vídeo válido.")
    return path

def save_video(path,space):
    c=espacos.read()
    if not c["enabled"] or espacos.versions()!=c["validated_versions"]:
        raise RuntimeError("As áreas independentes estão pausadas. Confira o controle de áreas.")
    data=json.loads(fundos.CFG.read_text());entry=dict(data["spaces"][space])
    entry.update(mode="raincarroof",video=str(path),request_id=time.time_ns())
    data["spaces"][space]=entry;espacos.save(fundos.CFG,data);espacos.start()

class RainWindow(Gtk.Window):
    def __init__(self,choose=False):
        super().__init__(title="Rain")
        self.set_default_size(570,250);self.set_border_width(18)
        self.set_icon_from_file(str(Path.home()/".local/share/icons/raincarroof-white-noise.png"))
        self.connect("destroy",Gtk.main_quit)
        box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=12);self.add(box)
        self.info=Gtk.Label(label="Vídeo de fundo da área atual",xalign=0);box.pack_start(self.info,False,False,0)
        row=Gtk.Box(spacing=8);box.pack_start(row,False,False,0)
        self.combo=Gtk.ComboBoxText();row.pack_start(self.combo,True,True,0)
        pick=Gtk.Button(label="Escolher arquivo…");pick.connect("clicked",self.choose);row.pack_start(pick,False,False,0)
        self.note=Gtk.Label(xalign=0);self.note.set_line_wrap(True);self.note.set_selectable(True);box.pack_start(self.note,True,True,0)
        actions=Gtk.Box(spacing=8);box.pack_start(actions,False,False,0)
        self.apply_button=Gtk.Button(label="Usar vídeo nesta área");self.apply_button.connect("clicked",self.apply);actions.pack_start(self.apply_button,True,True,0)
        stop=Gtk.Button(label="Usar imagem estática");stop.connect("clicked",self.stop);actions.pack_start(stop,False,False,0)
        try:
            space=TARGET_SPACE or current_space();entry=json.loads(fundos.CFG.read_text())["spaces"][space]
            selected=Path(entry.get("video",str(DEFAULT)));self.info.set_text("Vídeo de fundo — área "+space)
        except Exception:selected=DEFAULT
        self.paths=set()
        for path in sorted((Path.home()/"Relaxamento").glob("*")):
            if path.is_file() and path.suffix.lower() in EXT:self.add_video(path)
        if selected.is_file():self.add_video(selected);self.combo.set_active_id(str(selected))
        self.note.set_text("Escolha um vídeo local. A alteração vale somente para a área em que você clicar em Usar vídeo.")
        self.show_all()
        if choose:GLib.idle_add(self.quick_choose)
    def add_video(self,path):
        path=str(path)
        if path not in self.paths:self.combo.append(path,Path(path).name);self.paths.add(path)
    def choose(self,*_):
        dialog=Gtk.FileChooserDialog(title="Rain — escolher vídeo de fundo",parent=self,action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons("Cancelar",Gtk.ResponseType.CANCEL,"Escolher",Gtk.ResponseType.OK)
        filt=Gtk.FileFilter();filt.set_name("Vídeos")
        for ext in EXT:filt.add_pattern("*"+ext);filt.add_pattern("*"+ext.upper())
        dialog.add_filter(filt);allfiles=Gtk.FileFilter();allfiles.set_name("Todos os arquivos");allfiles.add_pattern("*");dialog.add_filter(allfiles)
        dialog.set_current_folder(str(Path.home()))
        accepted=dialog.run()==Gtk.ResponseType.OK
        if accepted:self.add_video(dialog.get_filename());self.combo.set_active_id(dialog.get_filename())
        dialog.destroy();return accepted
    def quick_choose(self):
        if self.choose():self.apply()
        return False
    def apply(self,*_):
        path=self.combo.get_active_id()
        if not path:self.note.set_text("Escolha um vídeo primeiro.");return
        try:space=TARGET_SPACE or current_space()
        except Exception as e:self.note.set_text(str(e));return
        self.apply_button.set_sensitive(False);self.note.set_text("Conferindo o vídeo…")
        def work():
            try:video=validate_video(path);save_video(video,space);message="Vídeo salvo na área "+space+": "+video.name
            except Exception as e:message="Não foi possível aplicar: "+str(e)
            GLib.idle_add(self.done,message)
        threading.Thread(target=work,daemon=True).start()
    def done(self,message):self.note.set_text(message);self.apply_button.set_sensitive(True);return False
    def stop(self,*_):
        try:
            space=TARGET_SPACE or current_space();fundos.set_choice(space,"static");espacos.start();self.note.set_text("Imagem estática selecionada na área "+space+".")
        except Exception as e:self.note.set_text(str(e))
if __name__=="__main__":
    RainWindow("--choose" in sys.argv);Gtk.main()
