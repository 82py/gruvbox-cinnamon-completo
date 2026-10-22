from pathlib import Path
import copy,json,os,shlex,subprocess
from .catalog import ROOT,COMPONENTS

def get(key,sandbox=False,home=None):
 if sandbox:
  p=Path(home)/'fake-dconf.json';return json.loads(p.read_text()).get(key) if p.is_file() else None
 return subprocess.check_output(['dconf','read',key],text=True).strip() or None

def existing_workspace(home):
 home=Path(home).resolve();candidates=[home/'.local/share/gruvbox-cinnamon/espacos/configuracao.json']
 auto=home/'.config/autostart/espacos-de-trabalho.desktop'
 if auto.is_file():
  for line in auto.read_text().splitlines():
   if line.startswith('Exec='):
    for arg in shlex.split(line[5:]):
     if arg.endswith('/espacos.py'):
      p=Path(arg)
      if p.is_absolute() and p.resolve().is_relative_to(home):candidates.append(p.parent/'configuracao.json')
 for path in candidates:
  if path.is_file():
   c=json.loads(path.read_text());funds=path.parent/'fundos.json'
   if len(c.get('folders',[]))==4 and funds.is_file():
    return c,json.loads(funds.read_text()),str(path)
 return None

def default_profile(home=None,sandbox=False):
 home=Path.home() if home is None else Path(home)
 values=json.loads((ROOT/'settings.json').read_text())
 # On the personal machine, live values are the default; a test account is isolated.
 if not sandbox:
  for key in list(values):
   current=get(key)
   if '/custom-keybindings/' in key:
    slot=key.split('/custom-keybindings/')[1].split('/')[0]
    name=get('/org/cinnamon/desktop/keybindings/custom-keybindings/'+slot+'/name')
    if name is not None and not any(token in name for token in ('Relax','Rain','rain')):continue
   if current is not None:values[key]=current
 existing=existing_workspace(home)
 if existing:
  c,f,origin=existing;spaces=[]
  for i,folder in enumerate(c['folders'],1):
   e=f['spaces'].get(str(i),{});spaces.append({'folder':folder,'mode':e.get('mode','static'),'image':e.get('image',''),'video':e.get('video',''),'fit':e.get('fit','zoom')})
  workspace={'folder_root':c['folder_root'],'pointer':c['pointer'],'spaces':spaces,'original':f.get('original',{}),'enabled':c.get('enabled',True),'imported_from':origin}
  tray=home/'.local/bin/video-wallpaper-tray'
  workspace['legacy_coupled_rain']=Path(origin)!=home/'.local/share/gruvbox-cinnamon/espacos/configuracao.json' and tray.is_file() and str(Path(origin).parent) in tray.read_text()
 else:
  desktop=home/'Desktop'
  if not sandbox:
   desktop=Path(subprocess.check_output(['xdg-user-dir','DESKTOP'],text=True).strip())
  root=home/'Espaços de trabalho Gruvbox'
  workspace={'folder_root':str(root),'pointer':str(root/'.atual'),'enabled':True,'spaces':[{'folder':str(desktop if i==1 else root/('Espaço '+str(i))),'mode':'static','image':'','video':'','fit':'scaled' if i in (1,3) else 'zoom'} for i in range(1,5)]}
 volume=35;muted=True
 if not sandbox:
  try:
   import socket
   with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as sock:
    sock.settimeout(.3);sock.connect(f'/run/user/{os.getuid()}/raincarroof-{os.getuid()}.sock')
    sock.sendall(b'{"command":["get_property","volume"],"request_id":71}\n{"command":["get_property","mute"],"request_id":72}\n')
    with sock.makefile('r') as f:
     found=set()
     while len(found)<2:
      reply=json.loads(f.readline());rid=reply.get('request_id')
      if reply.get('error')=='success' and rid in (71,72):
       if rid==71:volume=reply['data']
       else:muted=reply['data']
       found.add(rid)
  except (OSError,ValueError):pass
 def enabled(name):
  p=home/'.config/autostart'/name
  if p.is_file():
   for line in p.read_text().splitlines():
    if line.startswith('X-GNOME-Autostart-enabled='):return line.split('=',1)[1].strip().lower()=='true'
  return True
 return {'schema':1,'name':'Minha configuração atual','components':list(COMPONENTS),'settings':values,'workspaces':workspace,'autostart_workspaces':enabled('espacos-de-trabalho.desktop'),'autostart_rain':enabled('video-wallpaper.desktop'),'rain_volume':volume,'rain_muted':muted,'folder_color':'keep','keep_installer':True,'preserve_spice_settings':True,'language':'pt_BR'}

def validate(profile):
 from .catalog import closure
 if profile.get('schema')!=1:raise ValueError('Perfil incompatível')
 selected=closure(profile['components'])
 if profile.get('workspaces',{}).get('legacy_coupled_rain') and 'workspaces' in selected:selected=closure(selected|{'rain'})
 spaces=profile['workspaces']['spaces']
 if len(spaces)!=4:raise ValueError('Esta versão mantém quatro espaços; personalize as quatro pastas e fundos.')
 folders=[]
 for e in spaces:
  p=Path(e['folder']).expanduser()
  if not p.is_absolute():raise ValueError('Use caminhos absolutos nas pastas dos espaços')
  folders.append(p.resolve())
  if e['mode'] not in ('static','raincarroof'):raise ValueError('Tipo de fundo inválido')
  if e['mode']=='raincarroof' and 'rain' not in selected:raise ValueError('Selecione Rain para usar um fundo em vídeo')
  if e['fit'] not in ('scaled','zoom','centered','stretched','wallpaper','spanned','none'):raise ValueError('Ajuste de fundo inválido')
 if len(set(folders))!=4:raise ValueError('Cada espaço deve usar uma pasta diferente')
 if any(a in b.parents for a in folders for b in folders if a!=b):raise ValueError('As pastas dos espaços não podem ficar umas dentro das outras')
 if not 0<=float(profile['rain_volume'])<=100:raise ValueError('Volume inválido')
 if not isinstance(profile.get('settings'),dict):raise ValueError('Preferências inválidas')
 return selected

def load(path):
 p=json.loads(Path(path).read_text());validate(p);return p

def export(path,profile):
 validate(profile);path=Path(path);tmp=path.with_name(path.name+'.tmp');tmp.write_text(json.dumps(profile,ensure_ascii=False,indent=2)+'\n');tmp.chmod(0o600);os.replace(tmp,path)
