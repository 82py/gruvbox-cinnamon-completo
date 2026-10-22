"""User controls change only the current workspace's saved wallpaper choice."""
import sys,time,subprocess
from Xlib import display,X
import espacos as app
import fundos

def current_space():
    d=display.Display()
    try:
        p=d.screen().root.get_full_property(d.intern_atom('_NET_CURRENT_DESKTOP'),X.AnyPropertyType)
        if not p:raise RuntimeError('Não foi possível identificar a área atual.')
        space=str(int(p.value[0])+1)
        if space not in ('1','2','3','4'):raise RuntimeError('Área ainda não configurada.')
        return space
    finally:d.close()

def control(action):
    if action not in ('start','stop','restart'):raise ValueError('Comando inválido.')
    c=app.read()
    if not c['enabled'] or app.versions()!=c['validated_versions']:
        raise RuntimeError('A separação das áreas está pausada. Verifique “Ícones por espaço de trabalho”.')
    space=current_space()
    if action!='stop':
        data=__import__('json').loads(fundos.CFG.read_text())
        if not __import__('pathlib').Path(data['spaces'][space].get('video','')).is_file():
            subprocess.Popen(['/usr/bin/python3',str(__import__('pathlib').Path.home()/'.local/lib/rain/painel.py'),'--choose'])
            return space
    fundos.set_choice(space,'static' if action=='stop' else 'raincarroof')
    app.start()
    if action=='restart':
        for attempt in range(30):
            try:fundos.ipc(['seek',0,'absolute']);break
            except (OSError,RuntimeError):
                if attempt==29:raise
                time.sleep(.2)
    return space

if __name__=='__main__':
    try:
        action=sys.argv[1];space=control(action)
        app.notify(('Imagem estática' if action=='stop' else 'Rain')+' selecionado somente na área '+space+'.')
    except Exception as e:
        subprocess.run(['notify-send','Rain',str(e)],capture_output=True)
        print(str(e),file=sys.stderr);sys.exit(1)
