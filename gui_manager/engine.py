"""Operações por componente com pontos de restauração; sem efeitos ao importar."""
from pathlib import Path
from contextlib import contextmanager
import copy,datetime,fcntl,hashlib,importlib.util,json,os,re,shlex,shutil,subprocess,tempfile,uuid
from .catalog import ROOT,COMPONENTS,EXTENSIONS,AGGREGATE,array,closure,setting_group,units
from .profiles import validate,get,existing_workspace
spec=importlib.util.spec_from_file_location('gruvbox_legacy_io',ROOT/'scripts/manage.py')
legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)

def stamp():return datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:10]
def raw(value):
 from gi.repository import GLib
 if isinstance(value,bool):return 'true' if value else 'false'
 if isinstance(value,int):return str(value)
 return GLib.Variant('as' if isinstance(value,list) else 's',value).print_(True)

class Manager:
 def __init__(self,home=None,sandbox=False,root=ROOT,progress=None):
  self.home=(Path.home() if home is None else Path(home)).resolve();self.sandbox=sandbox;self.root=Path(root)
  if sandbox and self.home==Path.home().resolve():raise ValueError('Testes exigem uma pasta pessoal temporária')
  if not sandbox and self.home!=Path.home().resolve():raise ValueError('Não é permitido operar em outra conta')
  self.state=self.home/'.local/state/gruvbox-manager';self.registry=self.state/'installed.json';self.progress=progress or (lambda message:None)
 def read_registry(self):
  data=json.loads(self.registry.read_text()) if self.registry.is_file() else {'schema':1,'groups':[],'files':{},'settings':{},'shortcuts':{}}
  data['settings']=legacy.managed_settings(data['settings'])
  return data
 def save(self,path,value):legacy.save(path,value)
 def target(self,rel):return legacy.safe(self.home,rel)
 def value(self,key):return get(key,self.sandbox,self.home)
 def set(self,key,value):
  if not legacy.manages_setting(key):return
  if self.sandbox:
   p=self.home/'fake-dconf.json';data=json.loads(p.read_text()) if p.is_file() else {}
   if value is None:data.pop(key,None)
   else:data[key]=value
   self.save(p,data)
  elif value is None:subprocess.run(['dconf','reset',key],check=True)
  else:subprocess.run(['dconf','write',key,value],check=True)
 def render(self,text):return text.replace('__HOME__',str(self.home)).replace('__USER__',self.home.name)
 @contextmanager
 def lock(self):
  if self.state.is_symlink() or not self.state.resolve().is_relative_to(self.home):raise ValueError('Pasta de estado insegura')
  self.state.mkdir(parents=True,exist_ok=True);self.state.chmod(0o700)
  with (self.state/'operation.lock').open('a') as f:
   try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
   except BlockingIOError:raise RuntimeError('Outra operação do gerenciador está em andamento')
   pending=list((self.state/'points').glob('*/point.json')) if (self.state/'points').exists() else []
   if any(json.loads(p.read_text()).get('status')=='applying' for p in pending):raise RuntimeError('Há uma operação interrompida. Use Recuperar operação antes de continuar.')
   yield
 def requirements(self,selected):
  commands={'dconf','gsettings','notify-send'}
  if selected & {'panel','system','themes','effects','photo','workspaces'}:commands|={'cinnamon','nemo'}
  if 'workspaces' in selected:commands|={'xdg-user-dir','systemd-run','nemo-desktop','zenity'}
  if 'rain' in selected:commands|={'mpv','ffmpeg','ffprobe','socat','wmctrl','xterm','make','cc'}
  if 'relax' in selected:commands|={'mpv','zenity'}
  if 'terminal' in selected:commands|={'cool-retro-term'}
  return sorted(commands)
 def preflight(self,selected):
  if self.sandbox:return
  if os.geteuid()==0:raise RuntimeError('Abra como usuário comum, sem sudo')
  old_journal=self.home/'.local/state/gruvbox-cinnamon/install.json'
  if old_journal.is_file():raise RuntimeError('Há uma instalação do pacote anterior registrada. Restaure-a pelo desinstalador anterior antes de instalar com esta GUI; os arquivos pessoais serão preservados.')
  if os.environ.get('XDG_SESSION_TYPE')!='x11' or 'cinnamon' not in os.environ.get('XDG_CURRENT_DESKTOP','').lower():raise RuntimeError('Ambiente testado: Cinnamon 6.6.x em X11')
  for command in ['cinnamon','nemo']:
   if not re.search(r'\b6\.6\.',subprocess.check_output([command,'--version'],text=True)):raise RuntimeError('Versões testadas: Cinnamon/Nemo 6.6.x')
  missing=[c for c in self.requirements(selected) if not shutil.which(c)]
  if missing:raise RuntimeError('Dependências ausentes: '+', '.join(missing))
  if 'rain' in selected:subprocess.run(['cc','-fsyntax-only',str(self.root/'vendor/xwinwrap/xwinwrap.c')],check=True,capture_output=True)
 def _entry(self,target,group,**content):
  self.target(target);return {'target':target,'group':group,**content}
 def plan(self,profile):
  selected=validate(profile)
  if self.read_registry().get('legacy_coupled_rain') and 'workspaces' in selected:selected=closure(selected|{'rain'})
  files=[];settings={};shortcut_ids={}
  for unit,group in units(self.root):
   if group not in selected:continue
   if unit.get('requires_command') and not self.sandbox and not shutil.which(unit['requires_command']):continue
   if unit.get('requires_flatpak') and not self.sandbox:
    if not shutil.which('flatpak') or subprocess.run(['flatpak','info','--show-ref',unit['requires_flatpak']],capture_output=True).returncode:continue
   source=self.root/unit['source']
   if not source.exists():
    if unit['target']=='.local/bin/xwinwrap':continue
    raise RuntimeError('Arquivo de origem ausente: '+unit['source'])
   if group=='folder_colors' and 'Gruvbox-Pastas-Coloridas-' in unit['target'] and profile.get('folder_color','keep')=='keep' and (self.target(unit['target'])/'.gruvbox-folder-colors-owned').is_file():continue
   if profile.get('preserve_spice_settings',True) and unit['target'].startswith('.config/cinnamon/spices/') and self.target(unit['target']).is_file():
    files.append(self._entry(unit['target'],group,text=self.target(unit['target']).read_text()))
   else:
    files.append(self._entry(unit['target'],group,source=str(source),merge_ini=unit.get('merge_ini',False),merge_menu=unit.get('merge_menu',False)))
  for key,value in legacy.managed_settings(profile['settings']).items():
   group=setting_group(key)
   if group in selected and key not in ('/org/cinnamon/desktop/keybindings/custom-list','/org/cinnamon/enabled-applets') and '/custom-keybindings/' not in key:
    settings[key]={'group':group,'value':self.render(value)}
  if 'panel' in selected:
   current=array(profile['settings'].get('/org/cinnamon/enabled-applets',"[]"))
   current=[x for x in current if ':Radio3.0@claudiux:' not in x]
   # Radio is outside this manager: preserve any currently enabled instance.
   current += [x for x in array(self.value('/org/cinnamon/enabled-applets')) if ':Radio3.0@claudiux:' in x]
   settings['/org/cinnamon/enabled-applets']={'group':'panel','value':raw(current)}
  current=array(self.value(AGGREGATE))
  for group,ids in EXTENSIONS.items():
   if group in selected:
    for name in ids:
     # Keep a pre-existing personal UUID of the same color extension.
     if name not in current and not any(x.split('@')[0]==name.split('@')[0] for x in current):current.append(name)
  if selected & set(EXTENSIONS):settings[AGGREGATE]={'group':'aggregate','value':raw(current)}
  # Allocate new shortcut IDs rather than replacing an unrelated user's shortcut.
  custom_key='/org/cinnamon/desktop/keybindings/custom-list';custom=array(self.value(custom_key));used=set(custom)
  for group,slot in [('relax','custom0'),('rain','custom1')]:
   if group not in selected:continue
   original='/org/cinnamon/desktop/keybindings/custom-keybindings/'+slot+'/'
   slotname=self.value(original+'name')
   recognized=slotname is None or any(n in slotname for n in ('Relax','Rain','rain'))
   destination=slot
   if not recognized:
    n=0
    while 'custom'+str(n) in used:n+=1
    destination='custom'+str(n)
   shortcut_ids[destination]=group
   used.add(destination)
   if destination not in custom:custom.append(destination)
   for key,value in json.loads((self.root/'settings.json').read_text()).items():
    if key.startswith(original):settings[key.replace('/'+slot+'/', '/'+destination+'/')]={'group':group,'value':self.render(profile['settings'].get(key,value))}
  if selected & {'relax','rain'}:settings[custom_key]={'group':'shortcuts','value':raw(custom)}
  workspace=copy.deepcopy(profile['workspaces']);directories=[]
  if 'folder_colors' in selected and profile.get('folder_color','keep')!='keep':
   color=profile['folder_color']
   colors_spec=importlib.util.spec_from_file_location('gruvbox_colors',self.root/'scripts/folder_colors.py');colors=importlib.util.module_from_spec(colors_spec);colors_spec.loader.exec_module(colors)
   if color not in colors.COLORS:raise ValueError('Cor de pasta inválida')
   for entry in files:
    if entry['target']=='.local/share/icons/Gruvbox-Pastas-Coloridas-A':entry['overlay_color']=color
   for schema in ['cinnamon','gnome']:settings['/org/'+schema+'/desktop/interface/icon-theme']={'group':'folder_colors','value':raw('Gruvbox-Pastas-Coloridas-A')}
  for entry in files:
   if entry['target']=='.local/share/gruvbox-cinnamon/folder_colors.py':
    text=Path(entry.pop('source')).read_text()
    original=" if not journal.is_file() or json.loads(journal.read_text()).get('status')!='installed':raise RuntimeError('Instale primeiro o pacote Gruvbox Cinnamon; nenhuma cor foi alterada.')"
    replacement=" gui=home/'.local/state/gruvbox-manager/installed.json'\n valid_gui=gui.is_file() and 'folder_colors' in json.loads(gui.read_text()).get('groups',[])\n if not valid_gui and (not journal.is_file() or json.loads(journal.read_text()).get('status')!='installed'):raise RuntimeError('Instale primeiro o pacote Gruvbox Cinnamon; nenhuma cor foi alterada.')"
    entry['text']=text.replace(original,replacement)
  if 'workspaces' in selected:
   folders=[str(Path(e['folder']).expanduser().resolve()) for e in workspace['spaces']]
   for folder in folders:
    p=Path(folder)
    if not p.exists() and not p.is_relative_to(self.home):raise ValueError('Crie primeiro a pasta externa: '+folder)
    if p.exists() and not p.is_dir():raise ValueError('O destino não é uma pasta: '+folder)
    if not p.exists():directories.append(folder)
   pointer=Path(workspace['pointer']).expanduser()
   if not pointer.is_absolute() or not pointer.is_relative_to(self.home):raise ValueError('O ponteiro deve estar na pasta pessoal')
   if legacy.exists(pointer) and not pointer.is_symlink():raise ValueError('O ponteiro foi substituído por um arquivo ou pasta; nenhum conteúdo será sobrescrito')
   config={'enabled':workspace.get('enabled',True),'folder_root':workspace['folder_root'],'folders':folders,'pointer':str(pointer),'validated_versions':'sandbox' if self.sandbox else subprocess.check_output(['dpkg-query','-W','-f=${Package}=${Version}\n',*legacy.PACKAGES],text=True).strip(),'original_desktop':folders[0]}
   base='.local/share/gruvbox-cinnamon/espacos/'
   files.append(self._entry(base+'configuracao.json','workspaces',text=json.dumps(config,ensure_ascii=False,indent=2)))
   original=workspace.get('original') or {'image':'','fit':'zoom','slideshow':False}
   if not workspace.get('original'):
    from gi.repository import GLib
    for name,key,default in [('image','picture-uri',"''"),('fit','picture-options',"'zoom'")]:original[name]=GLib.Variant.parse(None,self.value('/org/cinnamon/desktop/background/'+key) or default,None,None).unpack()
    original['slideshow']=self.value('/org/cinnamon/desktop/background/slideshow/slideshow-enabled')=='true'
   funds={'original':original,'spaces':{str(i):{k:e[k] for k in ['mode','image','video','fit']} for i,e in enumerate(workspace['spaces'],1)}}
   files.append(self._entry(base+'fundos.json','workspaces',text=json.dumps(funds,ensure_ascii=False,indent=2)))
   files.append(self._entry(base+'INSTRUCOES.txt','workspaces',text=(self.root/'docs/ESPACOS-E-RAIN.md').read_text()))
   files.append(self._entry(str(pointer.relative_to(self.home)),'workspaces',symlink=folders[0]))
   path=self.home/'.config/user-dirs.dirs';text=path.read_text() if path.is_file() else ''
   text=re.sub(r'^XDG_DESKTOP_DIR=.*\n?','',text,flags=re.M)
   escaped=str(pointer.relative_to(self.home)).replace('\\','\\\\').replace('"','\\"').replace('$','\\$').replace('`','\\`')
   files.append(self._entry('.config/user-dirs.dirs','workspaces',text=text.rstrip()+'\nXDG_DESKTOP_DIR="$HOME/'+escaped+'"\n'))
  # The settings snapshot supplies cosmetic defaults; per-workspace media stays local.
  if 'rain' in selected:
   for e in files:
    if e['target']=='.local/bin/raincarroof-mpv':
     text=Path(e.pop('source')).read_text().replace('--volume=35','--volume='+str(float(profile['rain_volume']))).replace('--mute=yes','--mute='+('yes' if profile['rain_muted'] else 'no'));e['text']=text;e['executable']=True
  for e in files:
   if e['target'] in ('.config/autostart/espacos-de-trabalho.desktop','.config/autostart/video-wallpaper.desktop'):
    enabled=profile['autostart_workspaces'] if e['group']=='workspaces' else profile['autostart_rain'];e['text']=Path(e.pop('source')).read_text().replace('X-GNOME-Autostart-enabled=true','X-GNOME-Autostart-enabled='+str(enabled).lower())
  if 'icons' in selected:
   for name,icon in json.loads((self.root/'app-icons.json').read_text()).items():
    rel='.local/share/applications/'+name
    if any(e['target']==rel for e in files):continue
    candidates=[self.home/rel,Path('/usr/share/applications')/name,self.home/'.local/share/flatpak/exports/share/applications'/name,Path('/var/lib/flatpak/exports/share/applications')/name]
    source=next((p for p in candidates if p.is_file()),None)
    if source is not None and not self.sandbox:
     text=re.sub(r'^Icon=.*$', 'Icon='+icon,source.read_text(),flags=re.M);files.append(self._entry(rel,'icons',text=text))
  launcher_root=self.state/'installer' if profile.get('keep_installer',True) else self.root
  launcher='#!/usr/bin/env bash\nexec /usr/bin/python3 '+shlex.quote(str(launcher_root/'gui.py'))+' "$@"\n'
  files.append(self._entry('.local/bin/gruvbox-manager','core',text=launcher,executable=True))
  desktop='[Desktop Entry]\nType=Application\nName=Gruvbox Manager\nName[pt_BR]=Gerenciador Gruvbox\nComment=Install, customize and restore Gruvbox components\nComment[pt_BR]=Instalar, personalizar e restaurar componentes Gruvbox\nExec='+json.dumps(str(self.home/'.local/bin/gruvbox-manager'))+'\nIcon=preferences-desktop-theme\nTerminal=false\nCategories=Settings;DesktopSettings;\n'
  files.append(self._entry('.local/share/applications/gruvbox-manager.desktop','core',text=desktop))
  targets=[e['target'] for e in files]
  if len(set(targets))!=len(targets):raise RuntimeError('Há destinos duplicados no plano')
  for key,entry in settings.items():
   if key not in profile['settings'] and key not in (AGGREGATE,custom_key) and not '/custom-keybindings/' in key:raise ValueError('Preferência não reconhecida')
   from gi.repository import GLib
   GLib.Variant.parse(None,entry['value'],None,None)
  return {'groups':sorted(selected),'files':files,'settings':settings,'directories':directories,'profile':copy.deepcopy(profile),'shortcut_ids':shortcut_ids}
 def estimated_space(self,plan):
  def size(path):
   if path.is_symlink() or not path.exists():return 0
   items=path.rglob('*') if path.is_dir() else [path]
   return sum(p.stat().st_size for p in items if not p.is_symlink() and p.is_file())
  needed=sum(size(self.target(e['target']))+size(Path(e['source'])) if 'source' in e else size(self.target(e['target']))+len(e.get('text','').encode()) for e in plan['files'])
  if plan['profile'].get('keep_installer',True) and not (self.state/'installer').is_dir():needed+=size(self.root/'payload')+size(self.root/'vendor')+size(self.root/'docs')
  return int(needed*1.3)+32*1024*1024
 def preview(self,plan):
  return {'components':plan['groups'],'files':len(plan['files']),'settings':len(plan['settings']),'new_directories':plan['directories'],'targets':[{'path':str(self.target(e['target'])),'component':e['group'],'exists':legacy.exists(self.target(e['target']))} for e in plan['files']],'dependencies_added':sorted(set(plan['groups'])-set(plan['profile']['components']))}
 def _snapshot(self,entries,settings,groups,action):
  settings=legacy.managed_settings(settings)
  point_id=stamp();path=self.state/'points'/point_id;path.mkdir(parents=True)
  runtime={'workspace_running':False,'rain_tray_running':False}
  if not self.sandbox:
   runtime['workspace_running']=subprocess.run(['systemctl','--user','is-active','--quiet','espacos-de-trabalho.service']).returncode==0
   runtime['rain_tray_running']=bool(self._rain_pids(tray_only=True))
  point={'runtime_before':runtime,'id':point_id,'created':datetime.datetime.now().isoformat(),'action':action,'groups':sorted(groups),'status':'prepared','registry_before':self.read_registry(),'files':[],'settings':{key:{'value':self.value(key),'group':entry['group']} for key,entry in settings.items()}}
  # These shared lists can change while disabling live components; always back them up first.
  for key,group in [(AGGREGATE,'aggregate'),('/org/cinnamon/enabled-applets','radio_aggregate')]:
   if key not in point['settings'] and (set(groups)&({'radio'}|set(EXTENSIONS))):point['settings'][key]={'value':self.value(key),'group':group}
  for i,e in enumerate(entries):
   dest=self.target(e['target']);backup=None
   if legacy.exists(dest):
    backup='files/'+str(i);legacy.copy(dest,path/backup)
   point['files'].append({'target':e['target'],'group':e['group'],'backup':backup})
  self.save(path/'point.json',point);return point
 def _blob(self,point_id,backup):
  if not re.fullmatch(r'[0-9]{8}-[0-9]{6}-[0-9a-f]{10}',point_id) or not re.fullmatch(r'files/[0-9]+',backup):raise ValueError('Referência de cópia de segurança inválida')
  p=self.state/'points'/point_id/backup
  if not p.parent.resolve().is_relative_to(self.state.resolve()):raise ValueError('Backup fora do gerenciador')
  if not legacy.exists(p):raise RuntimeError('Cópia de segurança ausente: '+str(p))
  return p
 def _write(self,e):
  dest=self.target(e['target']);dest.parent.mkdir(parents=True,exist_ok=True)
  temp=dest.with_name(dest.name+'.gruvbox-gui-'+uuid.uuid4().hex)
  try:
   if 'text' in e:temp.write_text(self.render(e['text']));temp.chmod(0o755 if e.get('executable') else 0o644)
   elif 'symlink' in e:temp.symlink_to(e['symlink'])
   elif e.get('restore_none'):pass
   else:
    legacy.copy(Path(e['source']),temp)
    for p in (temp.rglob('*') if temp.is_dir() and not temp.is_symlink() else [temp]):
     if p.is_file() and not p.is_symlink() and p.stat().st_size<1500000:
      try:text=p.read_text()
      except UnicodeError:continue
      if '__HOME__' in text or '__USER__' in text:p.write_text(self.render(text))
   if e.get('overlay_color'):
    places=self.root/'payload/.local/share/icons/Gruvbox-Plus-Dark/places/scalable';destdir=temp/'places/scalable';destdir.mkdir(parents=True,exist_ok=True);color=e['overlay_color']
    for original in places.glob('folder-'+color+'*.svg'):
     data=original.read_bytes();name=original.name.replace('-'+color,'',1);(destdir/name).write_bytes(data);(destdir/(name[:-4]+'-symbolic.svg')).write_bytes(data)
    bookmark=places/('bookmarks-'+color+'.svg')
    if bookmark.is_file():(destdir/'folder-bookmark.svg').write_bytes(bookmark.read_bytes())
   if e.get('merge_ini') or e.get('merge_menu'):
    merger=legacy.merge_ini if e.get('merge_ini') else legacy.merge_menu
    temp.write_text(merger(temp.read_text(),dest.read_text() if dest.is_file() else ''))
   legacy.remove(dest)
   if legacy.exists(temp):os.replace(temp,dest)
  finally:
   if legacy.exists(temp):legacy.remove(temp)
 def _restore_entries(self,point,groups):
  entries=[]
  for e in point['files']:
   if e['group'] in groups:
    entries.append(self._entry(e['target'],e['group'],source=str(self._blob(point['id'],e['backup']))) if e['backup'] else self._entry(e['target'],e['group'],restore_none=True))
  settings={k:copy.deepcopy(v) for k,v in point['settings'].items() if v['group'] in groups or v['group'] in ('aggregate','shortcuts','radio_aggregate')}
  return entries,legacy.managed_settings(settings)
 def _rollback(self,point):
  entries,settings=self._restore_entries(point,set(point['groups'])|{'core'})
  for e in reversed(entries):self._write(e)
  for key,e in sorted(settings.items(),key=lambda kv:kv[0].startswith('/org/gnome/desktop/interface/')):self.set(key,e['value'])
  self.save(self.registry,point['registry_before']);point['status']='rolled_back';self.save(self.state/'points'/point['id']/'point.json',point)
 def _rain_pids(self,tray_only=False):
  if self.sandbox:return []
  paths={str(self.home/'.local/bin/video-wallpaper-tray').encode()}
  if not tray_only:paths.add(str(self.home/'.local/lib/rain/painel.py').encode())
  found=[]
  for p in Path('/proc').glob('[0-9]*/cmdline'):
   try:
    if paths.intersection(p.read_bytes().split(b'\0')):found.append(int(p.parent.name))
   except OSError:continue
  return found
 def _stop(self,groups,desired=None):
  if self.sandbox:return
  ids={name for group in groups for name in EXTENSIONS.get(group,[])}
  applet_ids={'Radio3.0@claudiux'} if 'radio' in groups else set()
  for key,targets,is_applet in [(AGGREGATE,ids,False),('/org/cinnamon/enabled-applets',applet_ids,True)]:
   if not targets:continue
   if desired is not None and key in desired:
    wanted=desired[key]['value']
    if wanted is None:
     from gi.repository import Gio
     values=Gio.Settings.new('org.cinnamon').get_default_value(key.rsplit('/',1)[-1]).unpack()
    else:values=array(wanted)
   else:values=array(self.value(key))
   kept=[v for v in values if (v.split(':')[3] if is_applet else v) not in targets];self.set(key,raw(kept))
  if ids or applet_ids:
   from gi.repository import Gio,GLib
   Gio.Settings.sync()
   proxy=Gio.DBusProxy.new_for_bus_sync(Gio.BusType.SESSION,0,None,'org.Cinnamon','/org/Cinnamon','org.Cinnamon',None)
   import time
   deadline=time.monotonic()+15
   while time.monotonic()<deadline:
    code='JSON.stringify({extensions:imports.ui.extensionSystem.runningExtensions,applets:imports.ui.appletManager.definitions.filter(d=>!!d.applet).map(d=>d.real_uuid)})'
    ok,value=proxy.call_sync('Eval',GLib.Variant('(s)',(code,)),0,5000,None).unpack()
    if not ok:raise RuntimeError('Não foi possível verificar o desligamento dos componentes')
    while isinstance(value,str):value=json.loads(value)
    if not (set(value['extensions'])&ids or set(value['applets'])&applet_ids):
     # Settings writers finish just after the applet disappears from Cinnamon.
     time.sleep(.6);break
    time.sleep(.1)
   else:raise RuntimeError('Os componentes ainda estão sendo desligados; os arquivos foram preservados')
  if 'rain' in groups:
   import signal,time
   pids=self._rain_pids()
   for pid in pids:
    try:os.kill(pid,signal.SIGTERM)
    except ProcessLookupError:pass
   until=time.monotonic()+4
   while time.monotonic()<until and self._rain_pids():time.sleep(.1)
   if self._rain_pids():raise RuntimeError('A janela ou bandeja Rain ainda está fechando; os arquivos foram preservados')
  if groups & {'workspaces','rain'}:subprocess.run(['systemctl','--user','stop','espacos-de-trabalho.service'],capture_output=True,timeout=20)
  if 'rain' in groups:
   # The current player is kept during installation; removal explicitly stops it.
   pass
 def _resume(self,groups,runtime_override=None):
  if self.sandbox or not groups&{'workspaces','rain'}:return
  reg=self.read_registry()
  should_resume=runtime_override['workspace_running'] if runtime_override is not None else 'workspaces' in reg['groups'] or reg.get('baseline_runtime',{}).get('workspace_running',False)
  auto=self.home/'.config/autostart/espacos-de-trabalho.desktop'
  if auto.is_file() and should_resume:
   for line in auto.read_text().splitlines():
    if line.startswith('Exec='):
     args=shlex.split(line[5:]);scripts=[Path(a) for a in args if a.endswith('/espacos.py')]
     if scripts and scripts[0].resolve().is_relative_to(self.home):subprocess.run(['/usr/bin/python3',str(scripts[0]),'start'],check=True,timeout=20)
  tray=self.home/'.local/bin/video-wallpaper-tray'
  tray_wanted=('rain' in reg['groups'] and reg.get('profile',{}).get('autostart_rain',True)) or ('rain' not in reg['groups'] and reg.get('baseline_runtime',{}).get('rain_tray_running',False))
  if runtime_override is not None:tray_wanted=runtime_override['rain_tray_running']
  if 'rain' in groups and tray.is_file() and tray_wanted:
   args=['systemd-run','--user','--collect','--unit=gruvbox-rain-tray-'+uuid.uuid4().hex[:10]]
   for key in ('DISPLAY','XAUTHORITY','XDG_SESSION_TYPE','XDG_CURRENT_DESKTOP'):
    if key in os.environ:args+=['--setenv='+key+'='+os.environ[key]]
   subprocess.run(args+['/usr/bin/python3',str(tray)],check=True,capture_output=True,timeout=15)
 def apply(self,profile):
  plan=self.plan(profile);self.preflight(set(plan['groups']))
  if not self.sandbox and shutil.disk_usage(self.home).free<self.estimated_space(plan):raise RuntimeError('Espaço livre insuficiente para guardar as cópias de segurança e instalar os componentes')
  with self.lock():
   point=self._snapshot(plan['files'],plan['settings'],plan['groups'],'apply');reg=self.read_registry()
   point['status']='applying';self.save(self.state/'points'/point['id']/'point.json',point)
   try:
    if profile.get('keep_installer',True) and not self.sandbox and self.root.resolve()!=(self.state/'installer').resolve():
     destination=self.state/'installer';temp=self.state/('installer-'+uuid.uuid4().hex)
     shutil.copytree(self.root,temp,symlinks=True,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
     if destination.exists():legacy.remove(destination)
     os.replace(temp,destination)
    self._stop(set(plan['groups']))
    for directory in plan['directories']:Path(directory).mkdir(parents=True,exist_ok=True)
    for i,e in enumerate(plan['files']):
     self.progress(f"{i+1}/{len(plan['files'])} · {e['target']}")
     if e['target'] not in reg['files']:
      before=next(x for x in point['files'] if x['target']==e['target']);reg['files'][e['target']]={'group':e['group'],'point':point['id'],'backup':before['backup']}
     self._write(e)
    if 'rain' in plan['groups'] and not self.sandbox:
     with tempfile.TemporaryDirectory(prefix='gruvbox-build-') as td:
      build=Path(td)/'xwinwrap';shutil.copytree(self.root/'vendor/xwinwrap',build);subprocess.run(['make','-C',str(build)],check=True,capture_output=True)
      target='.local/bin/xwinwrap'
      # Ensure the compiled executable is also included in this operation's undo point.
      if not any(e['target']==target for e in point['files']):
       backup=None;p=self.target(target)
       if legacy.exists(p):backup='files/'+str(len(point['files']));legacy.copy(p,self.state/'points'/point['id']/backup)
       point['files'].append({'target':target,'group':'rain','backup':backup});self.save(self.state/'points'/point['id']/'point.json',point)
       if target not in reg['files']:reg['files'][target]={'group':'rain','point':point['id'],'backup':backup}
      self._write(self._entry(target,'rain',source=str(build/'xwinwrap')))
    for key,e in sorted(plan['settings'].items(),key=lambda kv:kv[0] in (AGGREGATE,'/org/cinnamon/enabled-applets')):
     self.progress('Preferência · '+key)
     if key not in reg['settings']:reg['settings'][key]={'group':e['group'],'value':point['settings'][key]['value']}
     self.set(key,e['value'])
    for key,entry in point['settings'].items():
     if entry['group'] in ('aggregate','radio_aggregate') and key not in plan['settings']:self.set(key,entry['value'])
    if 'icons' in plan['groups']:
     reg.setdefault('base_icon_themes',{})
     for schema in ['cinnamon','gnome']:
      key='/org/'+schema+'/desktop/interface/icon-theme';value=profile['settings'].get(key,raw('Gruvbox-Sistema-Colorido'))
      if 'Gruvbox-Pastas-Coloridas-' not in value:reg['base_icon_themes'][key]=value
      elif key not in reg['base_icon_themes']:reg['base_icon_themes'][key]=raw('Gruvbox-Sistema-Colorido' if 'system' in plan['groups'] else 'Gruvbox-Plus-Dark')
    baseline=reg.setdefault('baseline_runtime',{})
    if 'workspaces' in plan['groups'] and 'workspaces' not in reg['groups']:baseline['workspace_running']=point['runtime_before']['workspace_running']
    if 'rain' in plan['groups'] and 'rain' not in reg['groups']:baseline['rain_tray_running']=point['runtime_before']['rain_tray_running']
    reg['legacy_coupled_rain']=reg.get('legacy_coupled_rain',False) or profile['workspaces'].get('legacy_coupled_rain',False)
    reg.setdefault('shortcuts',{}).update(plan['shortcut_ids'])
    reg['groups']=sorted(set(reg['groups'])|set(plan['groups']));reg['profile']=copy.deepcopy(profile);self.save(self.registry,reg)
    self._resume(set(plan['groups']))
    point['status']='complete';self.save(self.state/'points'/point['id']/'point.json',point)
   except BaseException:
    self._rollback(point);self._resume(set(plan['groups']),point.get('runtime_before'));raise
  return point['id']
 def points(self):
  return sorted([json.loads(p.read_text()) for p in (self.state/'points').glob('*/point.json')],key=lambda p:p['created'],reverse=True) if (self.state/'points').is_dir() else []
 def _validate_remaining(self,groups):
  required=closure(groups)
  if self.read_registry().get('legacy_coupled_rain') and 'workspaces' in groups and 'rain' not in groups:required.add('rain')
  if required!=set(groups):raise ValueError('Outros componentes dependem dos que você escolheu remover: '+', '.join(sorted(required-set(groups))))
 def uninstall(self,groups):
  groups=set(groups);reg=self.read_registry()
  if not groups or not groups<=set(reg['groups']):raise ValueError('Selecione componentes instalados pelo gerenciador')
  self._validate_remaining(set(reg['groups'])-groups)
  entries=[]
  for target,e in reg['files'].items():
   if e['group'] in groups:entries.append(self._entry(target,e['group'],source=str(self._blob(e['point'],e['backup']))) if e['backup'] else self._entry(target,e['group'],restore_none=True))
  settings={key:copy.deepcopy(e) for key,e in reg['settings'].items() if e['group'] in groups}
  if groups & set(EXTENSIONS) and AGGREGATE in reg['settings']:
   original=array(reg['settings'][AGGREGATE]['value']);current=array(self.value(AGGREGATE));ids={x for g in groups for x in EXTENSIONS.get(g,[])}
   desired=[x for x in current if x not in ids]+[x for x in original if x in ids]
   settings[AGGREGATE]={'group':'aggregate','value':None if not desired and reg['settings'][AGGREGATE]['value'] is None else raw(desired)}
  if 'rain' in groups and 'workspaces' not in groups:
   target='.local/share/gruvbox-cinnamon/espacos/fundos.json';path=self.target(target)
   if path.is_file():
    data=json.loads(path.read_text())
    for entry in data['spaces'].values():
     if entry.get('mode')=='raincarroof':entry['mode']='static'
    entries.append(self._entry(target,'rain',text=json.dumps(data,ensure_ascii=False,indent=2)))
  custom_key='/org/cinnamon/desktop/keybindings/custom-list'
  if groups&{'relax','rain'} and custom_key in reg['settings']:
   ids={slot for slot,group in reg.get('shortcuts',{}).items() if group in groups}
   original=array(reg['settings'][custom_key]['value']);current=array(self.value(custom_key))
   desired=[x for x in current if x not in ids]+[x for x in original if x in ids]
   settings[custom_key]={'group':'shortcuts','value':None if not desired and reg['settings'][custom_key]['value'] is None else raw(desired)}
  applets='/org/cinnamon/enabled-applets'
  if 'radio' in groups and 'panel' not in groups:
   original=array(reg['settings'].get(applets,{}).get('value'));current=array(self.value(applets))
   settings[applets]={'group':'radio_aggregate','value':raw([x for x in current if ':Radio3.0@claudiux:' not in x]+[x for x in original if ':Radio3.0@claudiux:' in x])}
  if 'folder_colors' in groups and 'icons' not in groups and 'icons' in reg['groups']:
   for schema in ['cinnamon','gnome']:
    key='/org/'+schema+'/desktop/interface/icon-theme'
    if key in settings:settings[key]['value']=reg.get('base_icon_themes',{}).get(key,raw('Gruvbox-Sistema-Colorido'))
  # Keep the active icon theme resolvable when a dependent overlay is removed.
  if 'icons' in set(reg['groups'])-groups and any(e['target']=='.local/share/icons/Gruvbox-Sistema-Colorido' and e.get('restore_none') for e in entries):
   for schema in ['cinnamon','gnome']:
    key='/org/'+schema+'/desktop/interface/icon-theme';current=self.value(key)
    if current and any(name in current for name in ['Gruvbox-Sistema-Colorido','Gruvbox-Pastas-Coloridas-']):settings[key]={'group':'system','value':raw('Gruvbox-Plus-Dark')}
  return self._execute_restore(entries,settings,groups,reg,None)
 def restore_point(self,point_id,groups):
  point=next((p for p in self.points() if p['id']==point_id),None)
  if not point:raise ValueError('Ponto de restauração ausente')
  groups=set(groups)
  if not groups or not groups<=set(point['groups']):raise ValueError('Escolha componentes presentes no ponto')
  current=self.read_registry();previous=point['registry_before'];remaining=(set(current['groups'])-groups)|(set(previous['groups'])&groups);self._validate_remaining(remaining)
  entries,settings=self._restore_entries(point,groups)
  for key,entry in settings.items():
   if entry['group']=='aggregate':
    ids={x for g in groups for x in EXTENSIONS.get(g,[])}
    saved=array(entry['value']);active=array(self.value(key));entry=dict(entry);desired=[x for x in active if x not in ids]+[x for x in saved if x in ids];entry['value']=None if not desired and entry['value'] is None else raw(desired);settings[key]=entry
   elif entry['group']=='shortcuts':
    ids={slot for registry in [current,previous] for slot,group in registry.get('shortcuts',{}).items() if group in groups}
    saved=array(entry['value']);active=array(self.value(key));entry=dict(entry);desired=[x for x in active if x not in ids]+[x for x in saved if x in ids];entry['value']=None if not desired and entry['value'] is None else raw(desired);settings[key]=entry
   elif entry['group']=='radio_aggregate' and 'panel' not in groups:
    saved=array(entry['value']);active=array(self.value(key));entry=dict(entry);entry['value']=raw([x for x in active if ':Radio3.0@claudiux:' not in x]+[x for x in saved if ':Radio3.0@claudiux:' in x]);settings[key]=entry
  # Remove component files introduced after this older checkpoint.
  known={e['target'] for e in entries}
  for target,e in current['files'].items():
   if e['group'] in groups and target not in known and target not in previous['files']:entries.append(self._entry(target,e['group'],restore_none=True))
  return self._execute_restore(entries,settings,groups,current,previous)
 def _execute_restore(self,entries,settings,groups,reg,previous):
  settings=legacy.managed_settings(settings)
  with self.lock():
   undo=self._snapshot(entries,settings,groups,'restore' if previous is not None else 'uninstall');undo['status']='applying';self.save(self.state/'points'/undo['id']/'point.json',undo)
   try:
    self._stop(groups,settings)
    if 'rain' in groups and not self.sandbox:
     player=self.home/'.local/bin/video-wallpaper'
     if player.is_file():subprocess.run([str(player),'stop'],capture_output=True,timeout=20)
    for e in reversed(entries):self.progress(e['target']);self._write(e)
    for key,e in sorted(settings.items(),key=lambda kv:kv[0].startswith('/org/gnome/desktop/interface/')):self.set(key,e['value'])
    if not self.sandbox:
     import time
     time.sleep(.4)
     for key in ['/org/gnome/desktop/interface/gtk-theme','/org/gnome/desktop/interface/icon-theme','/org/gnome/desktop/interface/cursor-theme','/org/cinnamon/enabled-desklets']:
      if key in settings:self.set(key,settings[key]['value'])
    for key,entry in undo['settings'].items():
     if entry['group'] in ('aggregate','radio_aggregate') and key not in settings:self.set(key,entry['value'])
    transferred={}
    if previous is None and 'folder_colors' in groups and 'icons' not in groups and 'icons' in reg['groups']:
     for key,entry in reg['settings'].items():
      if entry['group']=='folder_colors':transferred[key]={**entry,'group':'icons'}
    for kind in ('files','settings'):
     reg[kind]={k:v for k,v in reg[kind].items() if v['group'] not in groups}
     if previous is not None:reg[kind].update({k:v for k,v in previous[kind].items() if v['group'] in groups})
    reg['settings'].update(transferred)
    if previous is not None and groups&{'icons','system','folder_colors'}:reg['base_icon_themes']=copy.deepcopy(previous.get('base_icon_themes',{}))
    reg['shortcuts']={slot:group for slot,group in reg.get('shortcuts',{}).items() if group not in groups}
    if previous is not None:reg['shortcuts'].update({slot:group for slot,group in previous.get('shortcuts',{}).items() if group in groups})
    reg['groups']=sorted((set(reg['groups'])-groups)|(set(previous['groups'])&groups if previous else set()))
    if previous is not None and groups&{'rain','workspaces'}:reg['legacy_coupled_rain']=previous.get('legacy_coupled_rain',False)
    if not set(reg['groups'])&{'rain','workspaces'}:reg['legacy_coupled_rain']=False
    if not set(reg['groups'])&set(EXTENSIONS):reg['settings'].pop(AGGREGATE,None)
    if not set(reg['groups'])&{'rain','relax'}:reg['settings'].pop('/org/cinnamon/desktop/keybindings/custom-list',None)
    self.save(self.registry,reg);self._resume(groups);undo['status']='complete';self.save(self.state/'points'/undo['id']/'point.json',undo)
   except BaseException:self._rollback(undo);self._resume(groups,undo.get('runtime_before'));raise
  return undo['id']
 def recover(self,point_id):
  point=next((p for p in self.points() if p['id']==point_id),None)
  if not point or point['status']!='applying':raise ValueError('Operação interrompida não encontrada')
  # Recovery needs the lock but intentionally bypasses the pending-operation gate.
  with (self.state/'operation.lock').open('a') as f:
   try:fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
   except BlockingIOError:raise RuntimeError('Uma operação ainda está em execução')
   self._rollback(point);self._resume(set(point['groups']),point.get('runtime_before'))
