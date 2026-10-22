#!/usr/bin/python3
"""Desktop folders for this Cinnamon X11 session. Never move/delete user content."""
from pathlib import Path
import ast, fcntl, json, os, select, signal, subprocess, sys, time, uuid

BASE = Path(__file__).resolve().parent
CFG = BASE/'configuracao.json'
STATUS = BASE/'estado.json'
PENDING = BASE/'exibicao-pendente.json'
PACKAGES = ['cinnamon', 'nemo', 'muffin', 'xdg-user-dirs', 'python3-xlib', 'mpv']

def run(*args):
    return subprocess.check_output(list(args),text=True,stderr=subprocess.PIPE,timeout=15).strip()

def read():
    return json.loads(CFG.read_text())

def save(path, value):
    # Only application-owned configuration/status files are replaced.
    tmp=path.with_name(path.name+'.'+uuid.uuid4().hex)
    with tmp.open('x') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)

def versions():
    return run('dpkg-query','-W','-f=${Package}=${Version}\n',*PACKAGES)

def notify(message):
    subprocess.run(['notify-send','--app-name=Espaços de trabalho','--expire-time=15000',
                    'Ícones por espaço de trabalho',message],capture_output=True,timeout=8)

def tag_wallpaper(d):
    # Identify only the existing Raincarroof wrapper; no files/processes changed.
    from Xlib import X, error
    p=d.screen().root.get_full_property(d.intern_atom('_NET_CLIENT_LIST'),X.AnyPropertyType)
    if not p:return
    for wid in p.value:
        try:
            w=d.create_resource_object('window',int(wid))
            cmd=w.get_full_property(d.intern_atom('WM_COMMAND'),X.AnyPropertyType)
            parts=cmd.value.decode().rstrip('\0').split('\0') if cmd else []
            if parts and parts[0]=='xwinwrap' and str(Path.home()/'.local/bin/raincarroof-mpv') in parts:
                if w.get_wm_class()!=('raincarroof','RaincarroofWallpaper'):
                    w.set_wm_class('raincarroof','RaincarroofWallpaper')
        except error.XError:
            continue  # A window may close during enumeration.
    d.sync()

def swap(c, target, force=False):
    pointer=Path(c['pointer']);target=Path(target)
    if not target.is_dir():raise RuntimeError('Pasta ausente: '+str(target))
    if not pointer.is_symlink():raise RuntimeError('O ponteiro foi substituído externamente; operação interrompida.')
    if os.readlink(pointer) not in c['folders']:
        raise RuntimeError('O ponteiro aponta para uma pasta não gerenciada; operação interrompida.')
    if os.readlink(pointer)==str(target) and not force:return
    layout=run('gsettings','get','org.nemo.desktop','desktop-layout')
    tmp=pointer.with_name('.ponteiro-'+uuid.uuid4().hex)
    tmp.symlink_to(target,target_is_directory=True)
    # This replaces only our own symlink, never its target or a user file.
    os.replace(tmp,pointer)
    save(PENDING,{'pending':True,'layout':layout})
    try:
        run('gsettings','set','org.nemo.desktop','desktop-layout','false::false')
        time.sleep(.18)
    finally:
        run('gsettings','set','org.nemo.desktop','desktop-layout',layout)
        save(PENDING,{'pending':False,'layout':layout})

def restart_icons():
    run('nemo-desktop','--quit');time.sleep(.5)
    run('systemd-run','--user','--collect','--unit=nemo-icones-'+str(time.time_ns()),'/usr/bin/nemo-desktop')
    time.sleep(1)
    run('pgrep','-x','nemo-desktop')

def start(fresh=False):
    if subprocess.run(['systemctl','--user','is-active','--quiet','espacos-de-trabalho.service']).returncode==0:
        if not fresh:return
        run('systemctl','--user','stop','espacos-de-trabalho.service')
    args=['systemd-run','--user','--collect','--unit=espacos-de-trabalho',
          '--property=Restart=on-failure','--property=RestartSec=5']
    for key in ('DISPLAY','XAUTHORITY','XDG_SESSION_TYPE','XDG_CURRENT_DESKTOP'):
        if key in os.environ:args+=['--setenv='+key+'='+os.environ[key]]
    run(*args,'/usr/bin/python3',str(Path(__file__).resolve()),'daemon')

def daemon():
    from Xlib import display, X, error
    import fundos
    lock=(BASE/'daemon.lock').open('a')
    try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    except BlockingIOError:return
    if os.environ.get('XDG_SESSION_TYPE')!='x11':
        notify('Esta configuração foi testada em X11. Use a sessão Cinnamon padrão e solicite revisão.');return
    try:d=display.Display()
    except error.DisplayConnectionError:return
    root=d.screen().root
    root.change_attributes(event_mask=X.PropertyChangeMask);d.flush()
    atom=d.intern_atom('_NET_CURRENT_DESKTOP')
    stop=False
    def stopping(*_):
        nonlocal stop
        stop=True
    signal.signal(signal.SIGTERM,stopping);signal.signal(signal.SIGINT,stopping)
    last=None;checked=0;actual='';warned=None;wallpaper_warning=None;disconnected=False
    backgrounds=fundos.Controller(d)
    try:
        if PENDING.exists():
            pending=json.loads(PENDING.read_text())
            if pending['pending']:
                if run('gsettings','get','org.nemo.desktop','desktop-layout')=="'false::false'":
                    run('gsettings','set','org.nemo.desktop','desktop-layout',pending['layout'])
                save(PENDING,{**pending,'pending':False})
        while not stop:
            while d.pending_events():d.next_event()
            c=read();tag_wallpaper(d)
            if time.monotonic()-checked>30:
                actual=versions();checked=time.monotonic()
                if actual==c['validated_versions'] and subprocess.run(['pgrep','-x','nemo-desktop'],capture_output=True).returncode:
                    # Raincarroof may start before Nemo during login. Its window
                    # has already been identified above, so icons can now start.
                    run('systemd-run','--user','--collect','--unit=nemo-icones-'+str(time.time_ns()),'/usr/bin/nemo-desktop')
                    time.sleep(.8);run('pgrep','-x','nemo-desktop')
            prop=root.get_full_property(atom,X.AnyPropertyType)
            if not prop:raise RuntimeError('Espaço ativo não disponível.')
            index=int(prop.value[0]);reason=''
            if actual!=c['validated_versions']:
                reason='Atualização detectada. Solicite revisão antes de reativar a separação.'
            elif index>=len(c['folders']):
                reason='Espaço novo sem pasta configurada. Solicite inclusão deste espaço.'
            elif not c['enabled']:
                reason='Pausado: a Área de Trabalho original aparece em todos os espaços.'
            if run('xdg-user-dir','DESKTOP')!=c['pointer']:
                raise RuntimeError('A configuração da Área de Trabalho foi alterada externamente. Não será sobrescrita.')
            target=c['folders'][0] if reason else c['folders'][index]
            identity=(target,reason)
            if identity!=last:
                swap(c,target,force=last is None)
                save(STATUS,{'estado':reason or 'Ativo','espaco':index+1,'pasta':target,
                             'pid':os.getpid(),'atualizado_em':time.strftime('%Y-%m-%d %H:%M:%S')})
                last=identity
            try:
                backgrounds.apply(index,disabled=bool(reason))
                wallpaper_warning=None
            except error.ConnectionClosedError:raise
            except Exception as e:
                detail=str(e)
                if detail!=wallpaper_warning:
                    notify('Wallpaper: '+detail)
                    save(BASE/'erro-wallpaper.json',{'erro':detail,'espaco':index+1})
                wallpaper_warning=detail
            if reason and reason!=warned and ('Atualização' in reason or 'Espaço novo' in reason):notify(reason)
            warned=reason
            select.select([d],[],[],.6)
    except error.ConnectionClosedError:
        # Logging out closes X11 normally. Keep the user's enabled preference.
        disconnected=True
    except Exception as e:
        c=read();c['enabled']=False;save(CFG,c)
        save(STATUS,{'estado':'Pausado por erro','detalhe':str(e)})
        notify('Separação pausada por segurança: '+str(e))
    finally:
        if not disconnected:
            try:backgrounds.restore()
            except Exception:pass
            try:swap(read(),read()['folders'][0])
            except Exception:pass
        try:d.close()
        except error.ConnectionClosedError:pass

def pause():
    c=read();c['enabled']=False;save(CFG,c)
    start()

def resume():
    c=read()
    if versions()!=c['validated_versions']:
        raise RuntimeError('Houve atualização. A compatibilidade precisa ser revista antes de reativar.')
    c['enabled']=True;save(CFG,c);start()

def wallpaper_menu():
    import fundos
    try:fundos.menu()
    except Exception as e:subprocess.run(['zenity','--error','--no-markup','--text='+str(e)])

def menu():
    choices=['Abrir pastas dos espaços','Pausar e mostrar Área de Trabalho original',
             'Reativar separação','Ver estado e versões','Ler instruções','Wallpapers por espaço']
    r=subprocess.run(['zenity','--list','--title=Ícones por espaço de trabalho',
                      '--text=Escolha uma ação. As pastas e os arquivos são preservados.',
                      '--column=Ação','--width=620','--height=360',*choices],text=True,capture_output=True)
    if r.returncode:return
    selected=r.stdout.strip()
    try:
        if selected==choices[0]:subprocess.Popen(['nemo',read()['folder_root']])
        elif selected==choices[1]:pause()
        elif selected==choices[2]:resume()
        elif selected==choices[3]:
            state=json.loads(STATUS.read_text()) if STATUS.exists() else {}
            message=state.get('estado','Ainda não iniciado')+'\n\nPasta exibida: '+state.get('pasta','')
            message+='\n\nVersões atuais:\n'+versions()
            message+='\n\nApós atualização, consulte a documentação de compatibilidade do pacote. Não há correção automática.'
            subprocess.run(['zenity','--info','--no-markup','--width=650','--text='+message])
        elif selected==choices[4]:subprocess.Popen(['xdg-open',str(BASE/'INSTRUCOES.txt')])
        elif selected==choices[5]:wallpaper_menu()
    except Exception as e:
        subprocess.run(['zenity','--error','--no-markup','--text='+str(e)])

if __name__=='__main__':
    command=sys.argv[1] if len(sys.argv)>1 else 'menu'
    {'start':start,'login':lambda:start(fresh=True),'daemon':daemon,'menu':menu,'pause':pause,'resume':resume,'fundos':wallpaper_menu}[command]()
