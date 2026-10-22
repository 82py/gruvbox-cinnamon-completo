#!/usr/bin/python3
"""Teste de integração de ambos os TAR.GZ em HOME e GSettings keyfile isolados."""
from pathlib import Path
import ast,configparser,fcntl,hashlib,importlib.util,json,os,shutil,subprocess,sys,tarfile,tempfile
from unittest.mock import patch
D=Path(__file__).resolve().parents[2]
VERSION=json.loads((Path(__file__).resolve().parents[1]/'manifest.json').read_text())['version']
NAMES=['Gruvbox-Cinnamon-Completo-'+VERSION,'Gruvbox-Cinnamon-GitHub-'+VERSION]
REPORT=[]
def digest_tree(root):
 h=hashlib.sha256()
 for p in sorted(root.rglob('*')):
  h.update(str(p.relative_to(root)).encode())
  if p.is_symlink():h.update(b'L'+os.readlink(p).encode())
  elif p.is_file():h.update(b'F'+hashlib.sha256(p.read_bytes()).digest())
 return h.hexdigest()
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
for name in NAMES:
 archive=D/(name+'.tar.gz');archive_sha=hashlib.sha256(archive.read_bytes()).hexdigest()
 with tempfile.TemporaryDirectory(prefix='gruvbox-cores-extraido-') as td:
  td=Path(td);extract=td/'extraido';extract.mkdir()
  with tarfile.open(archive,'r:gz') as tf:tf.extractall(extract,filter='data')
  root=extract/name
  subprocess.run([sys.executable,str(root/'tests/test_audit_additions.py')],check=True)
  home=td/'conta de teste';(home/'Desktop').mkdir(parents=True)
  (home/'Desktop/documento.txt').write_text('preservar')
  (home/'escolher-cor-pastas.sh').write_text('menu anterior')
  (home/'folders-color-chooser.sh').write_text('auxiliar anterior')
  manager=load('manager',root/'scripts/manage.py');installer=manager.Installer(home,True);installer.install()
  env=dict(os.environ,HOME=str(home),XDG_CONFIG_HOME=str(home/'.config'),XDG_CACHE_HOME=str(home/'.cache'),XDG_DATA_HOME=str(home/'.local/share'),GSETTINGS_BACKEND='keyfile',TERM='xterm')
  def cmd(args,check=True,input=None):
   r=subprocess.run(args,env=env,input=input,capture_output=True,text=True)
   if check and r.returncode:raise AssertionError(str(args)+'\n'+r.stdout+'\n'+r.stderr)
   return r
  for schema in ['org.cinnamon.desktop.interface','org.gnome.desktop.interface']:cmd(['gsettings','set',schema,'icon-theme','Gruvbox-Sistema-Colorido'])
  icons=home/'.local/share/icons';protected=[icons/'Gruvbox-Plus-Dark',icons/'Gruvbox-Sistema-Colorido',home/'.local/share/cinnamon',home/'.themes',home/'.local/bin',home/'.config/user-dirs.dirs']
  def whole_hash():return {str(p.relative_to(home)):digest_tree(p) if p.is_dir() else hashlib.sha256(p.read_bytes()).hexdigest() for p in protected}
  before=whole_hash()
  colors=load('folder_colors',root/'scripts/folder_colors.py')
  chooser=home/'folders-color-chooser.sh';ui=home/'escolher-cor-pastas.sh'
  for p in [chooser,ui]:cmd(['bash','-n',str(p)])
  assert (root/'scripts/folder_colors.py').read_bytes()==(home/'.local/share/gruvbox-cinnamon/folder_colors.py').read_bytes()
  listed=cmd([str(chooser),'-l']).stdout
  assert all(c in listed for c in colors.COLORS)
  assert 'variantes separadas' in cmd([str(chooser),'-h']).stdout
  # GTK objects use an explicit theme/search path. No system/default theme is changed.
  os.environ.update({k:env[k] for k in ['HOME','XDG_CONFIG_HOME','XDG_CACHE_HOME','XDG_DATA_HOME','GSETTINGS_BACKEND']})
  import gi
  gi.require_version('Gtk','3.0');from gi.repository import Gtk
  resolved_checks=0;rendered_checks=0
  for color in colors.COLORS:
   cmd([str(chooser),'-c',color])
   selected=[ast.literal_eval(cmd(['gsettings','get',s,'icon-theme']).stdout.strip()) for s in colors.SCHEMAS]
   assert selected[0]==selected[1] and selected[0] in colors.SLOTS
   theme=Gtk.IconTheme.new();theme.set_search_path([str(icons)]);theme.set_custom_theme(selected[0])
   for icon in ['folder','folder-documents','folder-download','folder-remote','folder-music','folder-pictures']:
    expected=(icons/'Gruvbox-Plus-Dark/places/scalable'/(icon.replace('folder','folder-'+color,1)+'.svg')).read_bytes()
    for size in [16,24,32,48,64,128,256]:
     info=theme.lookup_icon(icon,size,Gtk.IconLookupFlags.FORCE_REGULAR);assert info is not None
     file=Path(info.get_filename());assert file.is_relative_to(icons/selected[0]);assert file.read_bytes()==expected
     resolved_checks+=1
    pix=theme.load_icon(icon,48,Gtk.IconLookupFlags.FORCE_REGULAR);assert pix.get_width()==48 and pix.get_height()==48;rendered_checks+=1
   # All system and application icons continue to resolve to the original inherited paths.
   original=Gtk.IconTheme.new();original.set_search_path([str(icons)]);original.set_custom_theme('Gruvbox-Sistema-Colorido')
   for icon in ['xsi-printer','xsi-folder-download','xsi-applications-office','audio-volume-high','network-wireless','bluetooth','rain-gruvbox','masterpdfeditor','yubioath']:
    a=theme.lookup_icon(icon,24,Gtk.IconLookupFlags.FORCE_REGULAR);b=original.lookup_icon(icon,24,Gtk.IconLookupFlags.FORCE_REGULAR)
    assert (a.get_filename() if a else None)==(b.get_filename() if b else None),icon
  assert before==whole_hash(),'Alteração em tema original, applets, executáveis ou configurações não relacionadas'
  # The existing menu itself works with the installed helper, also with spaces in HOME.
  cmd(['bash',str(ui)],input='2\n\nq\n')
  state=home/'.local/state/gruvbox-cinnamon/folder-colors.json';assert json.loads(state.read_text())['color']=='blue'
  cmd([str(chooser),'-C']);assert json.loads(state.read_text())['color']=='plasma'
  # Invalid color, unrelated selected theme and concurrent invocation must do no work.
  old=state.read_bytes();assert cmd([str(chooser),'-c','inexistente'],False).returncode!=0;assert state.read_bytes()==old
  for schema in colors.SCHEMAS:cmd(['gsettings','set',schema,'icon-theme','Adwaita'])
  snapshot=whole_hash();assert cmd([str(chooser),'-c','red'],False).returncode!=0;assert snapshot==whole_hash();assert state.read_bytes()==old
  for schema in colors.SCHEMAS:cmd(['gsettings','set',schema,'icon-theme',json.loads(old)['slot']])
  with (state.parent/'folder-colors.lock').open('a') as lock:
   fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);assert cmd([str(chooser),'-c','red'],False).returncode!=0
  # A missing package record or a replaced owned variant must block changes.
  journal=state.parent/'install.json';saved_journal=journal.read_bytes();journal.unlink()
  assert cmd([str(chooser),'-c','red'],False).returncode!=0;assert state.read_bytes()==old
  journal.write_bytes(saved_journal)
  marker=icons/colors.SLOTS[0]/colors.MARKER;owned_marker=marker.read_bytes();marker.unlink()
  assert cmd([str(chooser),'-c','red'],False).returncode!=0;assert state.read_bytes()==old
  marker.write_bytes(owned_marker)
  # Simulate the second settings write failing. Both settings and the inactive slot must roll back.
  current={s:colors.get(s) for s in colors.SCHEMAS};slot_hashes={s:digest_tree(icons/s) for s in colors.SLOTS};setter=colors.set_theme;failed=False
  def fail_once(schema,theme):
   global failed
   if schema==colors.SCHEMAS[1] and not failed:failed=True;raise RuntimeError('falha simulada')
   return setter(schema,theme)
  with patch.object(colors,'set_theme',side_effect=fail_once):
   try:colors.apply('red')
   except RuntimeError as e:assert str(e)=='falha simulada'
   else:raise AssertionError('Falha não simulada')
  assert current=={s:colors.get(s) for s in colors.SCHEMAS};assert slot_hashes=={s:digest_tree(icons/s) for s in colors.SLOTS};assert state.read_bytes()==old
  cmd([str(chooser),'--restore'])
  for schema in colors.SCHEMAS:assert ast.literal_eval(cmd(['gsettings','get',schema,'icon-theme']).stdout.strip())=='Gruvbox-Sistema-Colorido'
  assert before==whole_hash()
  # The actual keyfile backend received only icon-theme settings, no unrelated preferences.
  keyfile=home/'.config/glib-2.0/settings/keyfile'
  config=configparser.ConfigParser();config.read(keyfile)
  assert all(section in ['org/cinnamon/desktop/interface','org/gnome/desktop/interface'] and set(config[section])=={'icon-theme'} for section in config.sections())
  installer.restore()
  assert (home/'escolher-cor-pastas.sh').read_text()=='menu anterior';assert (home/'folders-color-chooser.sh').read_text()=='auxiliar anterior'
  assert (home/'Desktop/documento.txt').read_text()=='preservar'
  assert all(not (icons/s).exists() for s in colors.SLOTS)
  report={'archive':archive.name,'sha256':archive_sha,'colors_checked':len(colors.COLORS),'gtk_path_checks':resolved_checks,'gtk_icons_rendered':rendered_checks,'terminal_menu':'passed','reset_plasma':'passed','restore_previous_theme':'passed','invalid_color':'refused without changes','unrelated_theme':'refused without changes','concurrent_selection':'refused','failure_rollback':'passed','original_themes_and_other_components':'unchanged','uninstall_restores_original_scripts':'passed','personal_documents':'preserved'}
  REPORT.append(report);print(json.dumps(report,ensure_ascii=False),flush=True)
output=D/('Gruvbox-Cinnamon-Validacao-Cores-'+VERSION+'.json');output.write_text(json.dumps({'date':'2026-10-21','method':'Extract exact final archives, install in fake HOME, real GSettings keyfile backend, explicit GTK icon-theme objects. Active desktop settings never used for writes.','results':REPORT},ensure_ascii=False,indent=2)+'\n');print(output)
