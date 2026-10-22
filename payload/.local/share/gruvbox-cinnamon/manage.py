#!/usr/bin/python3
"""GPL-3.0-or-later. Pir (82py), com assistência do OpenAI Codex."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,shutil,subprocess,sys,tempfile,time,configparser,io,copy as copy_module
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
PACKAGES=['cinnamon','nemo','muffin','xdg-user-dirs','python3-xlib','mpv']
COMMANDS=['dconf','gsettings','nemo','nemo-desktop','mpv','ffprobe','ffmpeg','socat','wmctrl','xterm','zenity','systemd-run','notify-send','xdg-user-dir','make','cc']
# This external extension list belongs to the user, including in older backups.
def manages_setting(key):return key!='/org/nemo/plugins/disabled-extensions'
def managed_settings(values):return {key:value for key,value in values.items() if manages_setting(key)}
def run(*args,**kw):return subprocess.check_output(args,text=True,stderr=subprocess.PIPE,**kw).strip()
def save(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_name(p.name+'.tmp');t.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');os.replace(t,p)
def exists(p):return p.exists() or p.is_symlink()
def remove(p):
 if p.is_dir() and not p.is_symlink():shutil.rmtree(p)
 elif exists(p):p.unlink()
def copy(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True)
 if src.is_symlink():dst.symlink_to(os.readlink(src),target_is_directory=src.is_dir())
 elif src.is_dir():shutil.copytree(src,dst,symlinks=True)
 else:shutil.copy2(src,dst)
def fingerprint(p):
 if not exists(p):return None
 h=hashlib.sha256()
 items=[p] if not p.is_dir() or p.is_symlink() else sorted(p.rglob('*'))
 for q in items:
  h.update(str(q.relative_to(p) if q!=p else '.').encode())
  if q.is_symlink():h.update(b'L'+os.readlink(q).encode())
  elif q.is_file():h.update(b'F'+hashlib.sha256(q.read_bytes()).digest())
  else:h.update(b'D')
 return h.hexdigest()
def safe(home,rel):
 p=home/rel
 if Path(rel).is_absolute() or '..' in Path(rel).parts:raise ValueError('Destino inválido: '+rel)
 if not p.parent.resolve().is_relative_to(home.resolve()):raise ValueError('Destino sai da pasta pessoal: '+rel)
 return p
def merge_ini(source,destination):
 def read(text):
  c=configparser.ConfigParser(interpolation=None);c.optionxform=str
  if text.strip():c.read_string(text)
  return c
 base=read(destination);added=read(source)
 for section in added.sections():
  if not base.has_section(section):base.add_section(section)
  for key,value in added.items(section):base[section][key]=value
 out=io.StringIO();base.write(out,space_around_delimiters=False);return out.getvalue()
def merge_menu(source,destination):
 incoming=ET.fromstring(source)
 if not destination.strip():return source
 base=ET.fromstring(destination)
 if base.tag!='Menu' or base.findtext('Name')!=incoming.findtext('Name'):raise ValueError('Menu existente incompatível; arquivo preservado.')
 for new in incoming.findall('Menu'):
  old=next((x for x in base.findall('Menu') if x.findtext('Name')==new.findtext('Name')),None)
  if old is None:base.append(copy_module.deepcopy(new));continue
  if old.find('Directory') is None and new.find('Directory') is not None:old.append(copy_module.deepcopy(new.find('Directory')))
  inc=old.find('Include')
  if inc is None:inc=ET.SubElement(old,'Include')
  existing={x.text for x in inc.findall('Filename')}
  for f in new.findall('Include/Filename'):
   if f.text not in existing:inc.append(copy_module.deepcopy(f));existing.add(f.text)
 return ET.tostring(base,encoding='unicode')+'\n'
class Installer:
 def __init__(self,home,sandbox=False):
  self.home=home.resolve();self.sandbox=sandbox
  self.state=self.home/'.local/state/gruvbox-cinnamon';self.journal=self.state/'install.json'
  self.data=None
 def render(self,s):return s.replace('__HOME__',str(self.home)).replace('__USER__',self.home.name)
 def get(self,key):
  if self.sandbox:return json.loads((self.home/'fake-dconf.json').read_text()).get(key) if (self.home/'fake-dconf.json').exists() else None
  return run('dconf','read',key) or None
 def set(self,key,value):
  if not manages_setting(key):return
  if self.sandbox:
   p=self.home/'fake-dconf.json';d=json.loads(p.read_text()) if p.exists() else {}
   if value is None:d.pop(key,None)
   else:d[key]=value
   save(p,d);return
  if value is None:subprocess.run(['dconf','reset',key],check=True)
  else:subprocess.run(['dconf','write',key,value],check=True)
 def checkpoint(self):
  self.state.mkdir(parents=True,exist_ok=True);self.state.chmod(0o700);save(self.journal,self.data)
 def preflight(self):
  if self.sandbox:return
  if os.geteuid()==0:raise RuntimeError('Execute como usuário comum, sem sudo.')
  if self.home!=Path.home().resolve():raise RuntimeError('--home alternativo somente com --sandbox.')
  if os.environ.get('XDG_SESSION_TYPE')!='x11' or 'cinnamon' not in os.environ.get('XDG_CURRENT_DESKTOP','').lower():raise RuntimeError('Ambiente testado: Cinnamon 6.6.x em X11; outros ambientes não foram validados.')
  version=run('cinnamon','--version')
  if not re.search(r'\b6\.6\.',version):raise RuntimeError('Versão validada: Cinnamon 6.6.x; encontrada '+version)
  missing=[c for c in COMMANDS if not shutil.which(c)]
  if missing:raise RuntimeError('Dependências ausentes: '+', '.join(missing)+'. Leia docs/INSTALAR.md.')
  subprocess.run(['cc','-fsyntax-only',str(ROOT/'vendor/xwinwrap/xwinwrap.c')],check=True)
  subprocess.run(['/usr/bin/python3','-c','import gi, Xlib, PIL; gi.require_version("Gtk","3.0"); from gi.repository import Gtk,Gio,GdkPixbuf'],check=True)
  # Validate all GVariants before any installation write.
  from gi.repository import GLib
  for key,value in managed_settings(json.loads((ROOT/'settings.json').read_text())).items():GLib.Variant.parse(None,self.render(value),None,None)
  if '6.6.' not in run('nemo','--version'):raise RuntimeError('Nemo 6.6.x necessário para a separação dos espaços.')
 def put(self,rel,src=None,text=None,symlink=None):
  dest=safe(self.home,rel);backup=self.state/'backup'/str(len(self.data['files']))
  if any(e['target']==rel for e in self.data['files']):raise RuntimeError('Destino duplicado: '+rel)
  had=exists(dest)
  if had:copy(dest,backup)
  entry={'target':rel,'backup':str(backup.relative_to(self.state)) if had else None,'installed':None}
  self.data['files'].append(entry);self.checkpoint()
  dest.parent.mkdir(parents=True,exist_ok=True)
  tmp=dest.with_name(dest.name+'.gruvbox-new')
  if exists(tmp):raise RuntimeError('Temporário pré-existente: '+str(tmp))
  if text is not None:tmp.write_text(text)
  elif symlink is not None:tmp.symlink_to(symlink,target_is_directory=True)
  else:
   copy(src,tmp)
   files=tmp.rglob('*') if tmp.is_dir() and not tmp.is_symlink() else [tmp]
   for p in files:
    if p.is_symlink() or not p.is_file() or p.stat().st_size>1500000:continue
    try:s=p.read_text()
    except UnicodeError:continue
    if '__HOME__' in s or '__USER__' in s:p.write_text(self.render(s))
  remove(dest);os.replace(tmp,dest)
  entry['installed']=fingerprint(dest);self.checkpoint()
 def install(self):
  self.preflight()
  if self.journal.exists():raise RuntimeError('Há uma instalação/cópia de segurança existente. Desinstale-a antes de reinstalar.')
  manifest=json.loads((ROOT/'manifest.json').read_text())
  missing=[u['source'] for u in manifest['units'] if not (ROOT/u['source']).exists() and u['target']!='.local/bin/xwinwrap']
  if missing:raise RuntimeError('Componentes locais ausentes: '+', '.join(missing)+'. Consulte docs/PUBLICAR.md; não instale uma distribuição incompleta.')
  values=managed_settings(json.loads((ROOT/'settings.json').read_text()))
  original_settings={key:self.get(key) for key in values}
  self.data={'version':manifest['version'],'sandbox':self.sandbox,'status':'installing','files':[],'settings':original_settings,'created':datetime.datetime.now().isoformat()};self.checkpoint()
  try:
   # Existing desktop data stays exactly in place. Only the managed pointer changes.
   current=Path(run('xdg-user-dir','DESKTOP')) if not self.sandbox else self.home/'Desktop'
   if not current.exists():raise RuntimeError('Pasta da Área de Trabalho ausente; crie-a antes de instalar.')
   first=current.resolve()
   if not first.is_relative_to(self.home):raise RuntimeError('Área de Trabalho externa à pasta pessoal: configuração manual necessária.')
   folder=self.home/'Espaços de trabalho Gruvbox';pointer=folder/'.atual'
   folders=[str(first)]+[str(folder/('Espaço '+str(n))) for n in range(2,5)]
   for d in folders:Path(d).mkdir(parents=True,exist_ok=True)
   for u in manifest['units']:
    if u.get('requires_command') and (self.sandbox or not shutil.which(u['requires_command'])):continue
    if u.get('requires_flatpak'):
     if self.sandbox or not shutil.which('flatpak'):continue
     if subprocess.run(['flatpak','info','--show-ref',u['requires_flatpak']],capture_output=True).returncode:continue
    source=ROOT/u['source'];dest=safe(self.home,u['target'])
    if not source.exists():continue
    if u.get('merge_ini') or u.get('merge_menu'):
     merger=merge_ini if u.get('merge_ini') else merge_menu
     text=merger(self.render(source.read_text()),dest.read_text() if dest.exists() else '')
     self.put(u['target'],text=text)
    else:self.put(u['target'],src=source)
   # Public installations can build the pinned original source instead of a local binary.
   if not self.sandbox:
    with tempfile.TemporaryDirectory(prefix='gruvbox-build-') as td:
     build=Path(td)/'xwinwrap';shutil.copytree(ROOT/'vendor/xwinwrap',build)
     subprocess.run(['make','-C',str(build)],check=True,stdout=subprocess.DEVNULL)
     target='.local/bin/xwinwrap'
     # Local payload included the running binary; replace the installed copy but keep its original backup.
     entry=next((e for e in self.data['files'] if e['target']==target),None)
     if entry:
      remove(self.home/target);shutil.copy2(build/'xwinwrap',self.home/target)
      entry['installed']=fingerprint(self.home/target);self.checkpoint()
     else:self.put(target,src=build/'xwinwrap')
   self.put(str(pointer.relative_to(self.home)),symlink=str(first))
   dirs=self.home/'.config/user-dirs.dirs';text=dirs.read_text() if dirs.exists() else ''
   text=re.sub(r'^XDG_DESKTOP_DIR=.*\n?', '',text,flags=re.M)
   self.put('.config/user-dirs.dirs',text=text.rstrip()+'\nXDG_DESKTOP_DIR="$HOME/Espaços de trabalho Gruvbox/.atual"\n')
   base='.local/share/gruvbox-cinnamon/espacos/'
   versions=run('dpkg-query','-W','-f=${Package}=${Version}\n',*PACKAGES) if not self.sandbox else 'sandbox'
   self.put(base+'configuracao.json',text=json.dumps({'enabled':True,'folder_root':str(folder),'folders':folders,'pointer':str(pointer),'validated_versions':versions,'original_desktop':str(first)},ensure_ascii=False,indent=2))
   original={'image':self.get('/org/cinnamon/desktop/background/picture-uri') or "''",'fit':self.get('/org/cinnamon/desktop/background/picture-options') or "'zoom'",'slideshow':self.get('/org/cinnamon/desktop/background/slideshow/slideshow-enabled')=='true'}
   # GVariant strings can contain escaped characters; parse instead of stripping quotes.
   if not self.sandbox:
    from gi.repository import GLib
    for k in ['image','fit']:original[k]=GLib.Variant.parse(None,original[k],None,None).unpack()
   else:original.update(image='',fit='zoom')
   self.put(base+'fundos.json',text=json.dumps({'original':original,'spaces':{str(i):{'mode':'static','image':'','fit':('scaled' if i in [1,3] else 'zoom'),'video':''} for i in range(1,5)}},ensure_ascii=False,indent=2))
   self.put(base+'INSTRUCOES.txt',text=(ROOT/'docs/ESPACOS-E-RAIN.md').read_text())
   # Only override icons for applications already installed. Do not copy other users' launch commands.
   for name,icon in json.loads((ROOT/'app-icons.json').read_text()).items():
    rel='.local/share/applications/'+name
    if any(e['target']==rel for e in self.data['files']):continue
    candidates=[self.home/rel,Path('/usr/share/applications')/name,self.home/'.local/share/flatpak/exports/share/applications'/name,Path('/var/lib/flatpak/exports/share/applications')/name]
    src=next((p for p in candidates if p.is_file()),None)
    if not src or self.sandbox:continue
    s=src.read_text();s=re.sub(r'^Icon(?:\[[^\]]+\])?=.*$',lambda m:'Icon='+icon if m[0].startswith('Icon=') else m[0],s,flags=re.M)
    self.put(rel,text=s)
   values=managed_settings(json.loads((ROOT/'settings.json').read_text()))
   for key in sorted(values,key=lambda k:k.endswith('enabled-extensions')):
    self.set(key,self.render(values[key]))
   self.data['status']='installed';self.checkpoint()
  except BaseException:
   self.restore(rollback=True);raise
  print('Instalação concluída. Encerre a sessão e entre novamente. Escolha suas imagens e vídeos no menu.')
 def suspend_managed_spices(self):
  if self.sandbox:return
  from gi.repository import Gio,GLib
  owned={kind:set() for kind in ['extensions','applets']}
  for unit in self.data['files']:
   parts=Path(unit['target']).parts
   for kind in owned:
    if kind in parts and '.local' in parts:
     index=parts.index(kind)
     if len(parts)>index+1:owned[kind].add(parts[index+1])
  settings=Gio.Settings.new('org.cinnamon')
  for key,kind in [('enabled-extensions','extensions'),('enabled-applets','applets')]:
   path='/org/cinnamon/'+key
   if path not in self.data['settings']:continue
   raw=self.data['settings'][path]
   previous=GLib.Variant.parse(None,raw,None,None).unpack() if raw is not None else settings.get_default_value(key).unpack()
   kept=[entry for entry in previous if (entry if kind=='extensions' else entry.split(':')[3]) not in owned[kind]]
   self.set(path,GLib.Variant('as',kept).print_(True))
  Gio.Settings.sync()
  proxy=Gio.DBusProxy.new_for_bus_sync(Gio.BusType.SESSION,Gio.DBusProxyFlags.NONE,None,'org.Cinnamon','/org/Cinnamon','org.Cinnamon',None)
  code='JSON.stringify({extensions:imports.ui.extensionSystem.runningExtensions,applets:imports.ui.appletManager.definitions.filter(d=>!!d.applet).map(d=>d.real_uuid)})'
  deadline=time.monotonic()+15
  while time.monotonic()<deadline:
   ok,data=proxy.call_sync('Eval',GLib.Variant('(s)',(code,)),Gio.DBusCallFlags.NONE,5000,None).unpack()
   if not ok:raise RuntimeError('Não foi possível conferir o desligamento dos componentes do Cinnamon.')
   while isinstance(data,str):data=json.loads(data)
   if all(not (set(data[kind]) & owned[kind]) for kind in owned):
    time.sleep(.4);return
   time.sleep(.1)
  raise RuntimeError('O Cinnamon ainda está desligando componentes. Tente novamente antes de remover os arquivos.')
 def restore(self,rollback=False):
  if not self.journal.exists():raise RuntimeError('Nenhuma instalação registrada neste usuário.')
  self.data=json.loads(self.journal.read_text())
  if bool(self.data['sandbox'])!=self.sandbox:raise RuntimeError('Modo de restauração não corresponde ao registro.')
  for entry in self.data['files']:
   if entry['backup'] and not exists(self.state/entry['backup']):raise RuntimeError('Cópia de segurança ausente: '+entry['target'])
  self.suspend_managed_spices()
  if not self.sandbox:
   subprocess.run(['systemctl','--user','stop','espacos-de-trabalho.service'],capture_output=True)
   player=self.home/'.local/bin/video-wallpaper'
   if player.exists():subprocess.run([str(player),'stop'],capture_output=True,timeout=15)
   # Match only owned Rain launchers, never unrelated Python applications.
   rain_launchers={str(self.home/'.local/bin/video-wallpaper-tray').encode(),str(self.home/'.local/lib/rain/painel.py').encode()}
   for proc in Path('/proc').glob('[0-9]*/cmdline'):
    try:
     args=proc.read_bytes().split(b'\0')
     if rain_launchers.intersection(args):os.kill(int(proc.parent.name),15)
    except (OSError,ValueError):pass
  recovery=self.state/('alterados-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
  for e in reversed(self.data['files']):
   dest=safe(self.home,e['target'])
   if exists(dest) and e['installed'] is not None and fingerprint(dest)!=e['installed']:
    copy(dest,recovery/e['target'])
   remove(dest)
   if e['backup']:copy(self.state/e['backup'],dest)
  for key in sorted(managed_settings(self.data['settings']),key=lambda k:(k.startswith('/org/gnome/desktop/interface/'),k)):
   self.set(key,self.data['settings'][key])
  if not self.sandbox:
   time.sleep(.4)
   for key in ['/org/gnome/desktop/interface/gtk-theme','/org/gnome/desktop/interface/icon-theme','/org/gnome/desktop/interface/cursor-theme','/org/cinnamon/enabled-desklets']:
    if key in self.data['settings']:self.set(key,self.data['settings'][key])
  self.data['status']='rolled-back' if rollback else 'uninstalled';self.checkpoint()
  # Retain backups, and all workspace documents. Archive the journal to allow a future install.
  stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
  os.replace(self.journal,self.state/('registro-'+stamp+'.json'))
  if (self.state/'backup').exists():os.replace(self.state/'backup',self.state/('backup-'+stamp))
  print('Configurações anteriores restauradas. Arquivos dos espaços preservados. Encerre a sessão e entre novamente.')
def main():
 p=argparse.ArgumentParser(description='Instalar/restaurar Gruvbox Cinnamon sem tocar em arquivos internos do sistema.')
 p.add_argument('action',choices=['check','install','uninstall']);p.add_argument('--sandbox',action='store_true');p.add_argument('--home',type=Path,default=Path.home());a=p.parse_args()
 if a.sandbox and a.home.resolve()==Path.home().resolve():p.error('--sandbox requer --home apontando para uma pasta isolada.')
 i=Installer(a.home,a.sandbox)
 try:
  if not a.sandbox and os.geteuid()==0:raise RuntimeError('Execute como usuário comum, sem sudo.')
  if a.action=='check':i.preflight();print('Pré-requisitos verificados. Nenhuma configuração alterada.')
  elif a.action=='install':i.install()
  else:i.restore()
 except Exception as e:print('Erro: '+str(e),file=sys.stderr);sys.exit(1)
if __name__=='__main__':main()
