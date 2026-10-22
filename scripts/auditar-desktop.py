#!/usr/bin/python3
"""Inventaria a personalização ativa e compara com a árvore extraída. Somente leitura."""
from pathlib import Path
import ast,json,os,re,subprocess,hashlib,sys
from gi.repository import GLib,Gio
R=Path(__file__).resolve().parents[1];H=Path.home();manifest=json.loads((R/'manifest.json').read_text());settings=json.loads((R/'settings.json').read_text())
def norm(s):return s.replace(str(H),'__HOME__').replace('@'+H.name,'@gruvbox-cinnamon')
def value(schema,key):return GLib.Variant.parse(None,subprocess.check_output(['gsettings','get',schema,key],text=True).strip(),None,None).unpack()
report={'date':'2026-10-21','version':manifest['version'],'source':'active Cinnamon profile','read_only':True,'settings_total':len(settings),'file_checks':[],'settings_missing':[],'intentional_adaptations':[],'excluded_private_settings':[],'unexpected_differences':[]}
allowed={
 '/org/cinnamon/desktop/background/picture-uri':'Imagem excluída a pedido; fundo sólido até escolha local.',
 '/org/cinnamon/desktop/background/primary-color':'Fundo sólido Gruvbox substitui a imagem não distribuída.',
 '/org/cinnamon/desktop/background/slideshow/image-source':'Imagens de fundo não distribuídas.',
 '/org/cinnamon/desktop/keybindings/custom-keybindings/custom0/command':'Escolha local de vídeo substitui o caminho de mídia pessoal.',
 '/org/cinnamon/desktop/applications/terminal/exec':'Mesmo perfil visual, com configuração isolada do terminal original.'}
for prefix in ['/org/cinnamon/','/org/nemo/','/org/blueman/','/org/gnome/desktop/interface/','/org/gnome/desktop/wm/preferences/']:
 section=''
 for line in subprocess.check_output(['dconf','dump',prefix],text=True).splitlines():
  if line.startswith('['):section=line[1:-1]
  elif '=' in line:
   key,v=line.split('=',1);key=re.sub('/+','/',prefix+(section+'/' if section else '')+key)
   if any(k in key for k in ['looking-glass-history','last-coordinates']):report['excluded_private_settings'].append(key);continue
   if key not in settings:report['settings_missing'].append(key)
   elif settings[key]!=norm(v):
    try:equivalent=GLib.Variant.parse(None,settings[key],None,None).equal(GLib.Variant.parse(None,norm(v),None,None))
    except GLib.Error:equivalent=False
    if not equivalent:
     if key in allowed:report['intentional_adaptations'].append({'key':key,'reason':allowed[key]})
     else:report['unexpected_differences'].append(key)
for u in manifest['units']:
 rel=u['target'];live=H/rel.replace('@gruvbox-cinnamon','@'+H.name);stored=R/u['source']
 if rel.startswith(('.local/share/icons/Gruvbox-', '.icons/Gruvbox_', '.themes/','.local/share/cinnamon/extensions/','.local/share/cinnamon/applets/')) and live.is_dir():
  missing=[];different=[];count=0;root=live.resolve()
  for p in root.rglob('*'):
   if not p.is_file() and not p.is_symlink():continue
   if '__pycache__' in p.parts or p.name=='icon-theme.cache' or '.antes-' in p.name:continue
   count+=1;q=stored/p.relative_to(root)
   if not q.exists() and not q.is_symlink():missing.append(str(p.relative_to(root)))
   elif p.is_symlink():
    if not q.is_symlink() or os.readlink(p)!=os.readlink(q):different.append(str(p.relative_to(root)))
   elif p.read_bytes()!=q.read_bytes():
    try:equivalent=norm(p.read_text())==q.read_text()
    except UnicodeError:equivalent=False
    if not equivalent:different.append(str(p.relative_to(root)))
  report['file_checks'].append({'component':rel,'checked':count,'missing':missing,'different':different})
applets=value('org.cinnamon','enabled-applets');extensions=value('org.cinnamon','enabled-extensions')
report['applets']=[{'id':x.split(':')[-1],'uuid':x.split(':')[-2],'provided_by':'Linux Mint Cinnamon' if x.split(':')[-2].endswith('@cinnamon.org') else 'payload'} for x in applets]
report['extensions']=[{'uuid':norm(x),'present_in_package':(R/'payload/.local/share/cinnamon/extensions'/norm(x)).is_dir()} for x in extensions]
report['desklets']=value('org.cinnamon','enabled-desklets')
try:
 proxy=Gio.DBusProxy.new_for_bus_sync(Gio.BusType.SESSION,Gio.DBusProxyFlags.NONE,None,'org.Cinnamon','/org/Cinnamon','org.Cinnamon',None)
 code='JSON.stringify({running:imports.ui.extensionSystem.runningExtensions,states:imports.ui.extension.extensions.filter(x=>x.lowerType==="extension").map(x=>({uuid:x.uuid,state:x.meta.state,path:x.meta.path}))})'
 success,data=proxy.call_sync('Eval',GLib.Variant('(s)',(code,)),Gio.DBusCallFlags.NONE,5000,None).unpack()
 if not success:raise RuntimeError('Consulta indisponível')
 while isinstance(data,str):data=json.loads(data)
 report['runtime_extensions']=json.loads(norm(json.dumps(data)))
except Exception:
 report['runtime_extensions']={'note':'Consulta de execução indisponível; configurações e arquivos foram comparados.'}

report['personalization_tools']=[{'tool':n,'present':any(u['target']==t for u in manifest['units'])} for n,t in [('Rain','.local/lib/rain/painel.py'),('Relax','.local/share/applications/Relax.desktop'),('Pastas coloridas','escolher-cor-pastas.sh'),('Espaços independentes','.local/share/gruvbox-cinnamon/espacos/espacos.py'),('Fundos por espaço','.local/share/gruvbox-cinnamon/espacos/fundos.py'),('Copiar entre áreas','.local/share/gruvbox-cinnamon/espacos/copiar_entre_areas.py'),('Terminal visual isolado','.local/bin/gruvbox-terminal')]]
report['menu_application_count']=json.loads((R/'docs/MENU-INVENTARIADO.json').read_text())['application_count']
report['autostart']=[{'file':n,'treatment':t} for n,t in [('espacos-de-trabalho.desktop','included'),('video-wallpaper.desktop','included'),('insync.desktop','included only if insync is installed'),('com.bitwarden.desktop.desktop','included only if Bitwarden Flatpak is installed'),('nvidia-prime.desktop','disabled in source; not enabled by theme'),('remmina-applet.desktop','disabled in source; not enabled by theme')]]
report['external_application_policy']='Only theme/integration programs are bundled. Standard and third-party apps, credentials, personal servers, VPN, synchronization data and unrelated personal scripts are not copied. Their icons and visible menu inventory are included.'
report['portable_changes']=['No videos, wallpapers, photo or desktop documents.','Workspace folders are empty, except the existing recipient desktop is reused as area 1.','Media chooser replaces original fixed paths.','Fontconfig overrides merge with existing overrides.','Browser-menu entries merge without removing other entries.','Terminal profile runs in an isolated app-data folder and restores normal XDG paths for child commands.','Old dated workspace installers are replaced by the new install/uninstall tools; source-machine restoration backups are not distributed.','GTK/Qt application accounts and sessions are excluded; appearance-only files are included.']
report['coverage_ok']=not report['settings_missing'] and not report['unexpected_differences'] and all(not f['missing'] and not f['different'] for f in report['file_checks']) and all(x['present_in_package'] for x in report['extensions']) and all(x['present'] for x in report['personalization_tools'])
print(json.dumps(report,ensure_ascii=False,indent=2))
if not report['coverage_ok']:sys.exit(1)
