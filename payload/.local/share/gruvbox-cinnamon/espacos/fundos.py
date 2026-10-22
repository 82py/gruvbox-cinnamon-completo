"""Per-workspace wallpaper preferences; original images/video remain read-only."""
from pathlib import Path
import json, os, socket, subprocess, time
from urllib.parse import unquote, urlparse
from Xlib import X, error
import gi
from gi.repository import Gio, GLib
import espacos as app

CFG=app.BASE/'fundos.json'
STATE=app.BASE/'estado-fundos.json'
BACKGROUND='org.cinnamon.desktop.background'
SLIDESHOW='org.cinnamon.desktop.background.slideshow'

def ipc(command):
    path=f'/run/user/{os.getuid()}/raincarroof-{os.getuid()}.sock'
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:
        s.settimeout(2);s.connect(path)
        s.sendall((json.dumps({'command':command,'request_id':917})+'\n').encode())
        with s.makefile('r') as f:
            for line in f:
                reply=json.loads(line)
                if reply.get('request_id')==917:
                    if reply.get('error')!='success':raise RuntimeError(str(reply))
                    return reply.get('data')
    raise RuntimeError('O Rain não respondeu.')

def windows(d):
    root=d.screen().root
    candidates={w.id:w for w in root.query_tree().children}
    managed=root.get_full_property(d.intern_atom('_NET_CLIENT_LIST'),X.AnyPropertyType)
    if managed:
        for wid in managed.value:
            candidates[int(wid)]=d.create_resource_object('window',int(wid))
    found=[]
    for w in candidates.values():
        try:
            p=w.get_full_property(d.intern_atom('WM_COMMAND'),X.AnyPropertyType)
            cmd=p.value.decode().rstrip('\0').split('\0') if p else []
            if cmd and cmd[0]=='xwinwrap' and str(Path.home()/'.local/bin/raincarroof-mpv') in cmd:
                w.set_wm_class('raincarroof','RaincarroofWallpaper');found.append(w)
        except error.XError:continue
    d.sync()
    return found

class Controller:
    def __init__(self,d):
        self.d=d;self.last=None;self.warned=None;self.attempted=None
        self.observed=None;self.active_index=None
        self.bg=Gio.Settings.new(BACKGROUND);self.slideshow=Gio.Settings.new(SLIDESHOW)
        self.state=json.loads(STATE.read_text()) if STATE.exists() else {'hidden':False}

    def show(self, ws):
        mapped=False
        for w in ws:
            if w.get_attributes().map_state!=X.IsViewable:w.map();mapped=True
            w.configure(stack_mode=X.Below)
        self.d.sync()
        if ws and (mapped or self.last is None):
            time.sleep(.15)
            c=app.read();app.swap(c,os.readlink(c['pointer']),force=True)
        if self.state.get('hidden'):
            ipc(['set_property','pause',self.state.get('previous_pause',False)])
            self.state={'hidden':False};app.save(STATE,self.state)

    def hide(self, ws):
        if ws and not self.state.get('hidden'):
            self.state={'hidden':True,'previous_pause':ipc(['get_property','pause'])}
            app.save(STATE,self.state)
        if ws:
            ipc(['set_property','pause',True])
        for w in ws:
            if w.get_attributes().map_state!=X.IsUnmapped:w.unmap()
        self.d.sync()

    def restore(self):
        if not CFG.exists():return
        c=json.loads(CFG.read_text())
        self.bg.set_string('picture-uri',c['original']['image'])
        self.bg.set_string('picture-options',c['original']['fit'])
        self.slideshow.set_boolean('slideshow-enabled',c['original']['slideshow'])
        Gio.Settings.sync()
        self.show(windows(self.d));self.last=None;self.observed=None;self.active_index=None

    def remember_external_choice(self,c,index):
        # Dispatch dconf notifications: this daemon otherwise waits only for X11.
        context=GLib.MainContext.default()
        while context.pending():context.iteration(False)
        actual=(self.bg.get_string('picture-uri'),self.bg.get_string('picture-options'))
        if self.observed is not None and actual!=self.observed:
            uri,fit=actual
            parsed=urlparse(uri)
            if parsed.scheme=='file' and Path(unquote(parsed.path)).is_file():
                # The wallpaper being replaced belongs to the area last rendered.
                owner=index if self.active_index is None else self.active_index
                entry=dict(c['spaces'][str(owner+1)])
                entry.update(mode='static',image=uri,fit=fit,request_id=time.time_ns())
                c['spaces'][str(owner+1)]=entry;app.save(CFG,c)
        return c

    def apply(self,index,disabled=False):
        if not CFG.exists():return
        c=json.loads(CFG.read_text())
        if disabled:
            if self.last!='disabled':self.restore();self.last='disabled'
            return
        c=self.remember_external_choice(c,index)
        entry=c['spaces'][str(index+1)]
        ws=windows(self.d)
        choice=(index,json.dumps(entry,sort_keys=True))
        signature=(*choice,tuple(w.id for w in ws))
        if signature==self.last:return
        may_start=self.attempted!=choice
        self.attempted=choice
        image=entry['image']
        if entry['mode']=='static' and image:
            p=Path(unquote(urlparse(image).path))
            if not p.is_file():
                raise RuntimeError('Imagem não encontrada: '+str(p))
        # Disable the global slideshow while per-workspace backgrounds are active.
        self.slideshow.set_boolean('slideshow-enabled',False)
        self.bg.set_string('picture-uri',image)
        self.bg.set_string('picture-options',entry['fit']);Gio.Settings.sync()
        self.observed=(image,entry['fit']);self.active_index=index
        if entry['mode']=='raincarroof':
            if not ws and may_start:
                # Keep the player alive after its short-lived launcher exits.
                # At most one attempt per workspace/explicit choice: never fight Stop.
                app.run('systemd-run','--user','--collect','--unit=raincarroof-espacos-'+str(time.time_ns()),
                        '--property=Type=exec','--property=ExitType=cgroup',
                        '--setenv=RAIN_VIDEO='+entry.get('video',''),
                        str(Path.home()/'.local/bin/video-wallpaper'),'start')
                for _ in range(30):
                    time.sleep(.1);ws=windows(self.d)
                    if ws:break
                if not ws:raise RuntimeError('Rain não iniciou. Sua imagem estática foi mantida.')
                signature=(index,json.dumps(entry,sort_keys=True),tuple(w.id for w in ws))
                self.state={'hidden':False};app.save(STATE,self.state)
            if ws:
                video=entry.get('video', '')
                if not Path(video).is_file():raise RuntimeError('Vídeo não encontrado: '+video)
                if ipc(['get_property','path']) != video:
                    ipc(['loadfile',video,'replace'])
                    ipc(['set_property','loop-file','inf'])
                self.show(ws)
        else:self.hide(ws)
        self.last=signature

def choose(*args):
    r=subprocess.run(['zenity',*args],capture_output=True,text=True)
    return r.stdout.strip() if r.returncode==0 else None

def set_choice(space,mode,image=None):
    if space not in ('1','2','3','4') or mode not in ('static','raincarroof'):raise ValueError('Escolha inválida.')
    c=json.loads(CFG.read_text())
    entry=dict(c['spaces'][space]);entry['mode']=mode;entry['request_id']=time.time_ns()
    if image:
        p=Path(image).resolve(strict=True)
        # Validate that the selected file can actually be decoded as an image.
        gi.require_version('GdkPixbuf','2.0')
        from gi.repository import GdkPixbuf
        if not GdkPixbuf.Pixbuf.get_file_info(str(p))[0]:raise ValueError('Escolha um arquivo de imagem válido.')
        entry.update(image=p.as_uri(),fit='zoom')
    c['spaces'][space]=entry;app.save(CFG,c)

def menu():
    c=json.loads(CFG.read_text());rows=[]
    for n,e in c['spaces'].items():rows += [n,'Rain' if e['mode']=='raincarroof' else 'Imagem estática']
    space=choose('--list','--title=Wallpaper de cada espaço','--text=Escolha o espaço que deseja configurar.',
                 '--column=Espaço','--column=Fundo atual','--width=550','--height=340',*rows)
    if not space:return
    mode=choose('--list','--title=Wallpaper do espaço '+space,'--text=Esta escolha altera somente o espaço '+space+'.',
                '--column=Tipo','--width=520','--height=280','Rain','Escolher imagem estática','Usar última imagem estática')
    if not mode:return
    image=None
    if mode=='Escolher imagem estática':
        image=choose('--file-selection','--title=Escolha a imagem do espaço '+space,
                     '--file-filter=Imagens | *.png *.jpg *.jpeg *.webp *.bmp *.PNG *.JPG *.JPEG')
        if not image:return
    if mode=='Rain' and not Path(c['spaces'][space].get('video','')).is_file():
        subprocess.Popen(['/usr/bin/python3',str(Path.home()/'.local/lib/rain/painel.py'),'--choose','--space='+space])
        return
    set_choice(space,'raincarroof' if mode=='Rain' else 'static',image)
    app.start()
    choose('--info','--no-markup','--title=Wallpaper salvo',
           '--text=Escolha salva somente para o espaço '+space+'.\nOs outros espaços permanecem como estavam.')
