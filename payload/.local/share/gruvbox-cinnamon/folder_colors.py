#!/usr/bin/python3
"""GPL-3.0-or-later. Pir (82py), com assistência do OpenAI Codex.
Compatibilidade com o seletor Gruvbox Plus de akarzim; escreve só variantes próprias.
"""
from pathlib import Path
import argparse,ast,fcntl,json,os,shutil,subprocess,sys,tempfile,uuid
COLORS='black blue caramel citron firebrick gold green grey highland jade lavender lime olive orange pistachio plasma pumpkin purple red rust sapphire tomato violet white yellow'.split()
SLOTS=('Gruvbox-Pastas-Coloridas-A','Gruvbox-Pastas-Coloridas-B')
BASE='Gruvbox-Plus-Dark';SYSTEM='Gruvbox-Sistema-Colorido'
SCHEMAS=('org.cinnamon.desktop.interface','org.gnome.desktop.interface')
MARKER='.gruvbox-folder-colors-owned'
def get(schema):return ast.literal_eval(subprocess.check_output(['gsettings','get',schema,'icon-theme'],text=True).strip())
def set_theme(schema,name):subprocess.run(['gsettings','set',schema,'icon-theme',name],check=True)
def atomic_json(p,data):
 t=p.with_name(p.name+'.'+uuid.uuid4().hex);t.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');os.replace(t,p)
def index(name):
 return '[Icon Theme]\nName='+name+'\nComment=Escolha de cor em variante separada; originais preservados.\nInherits='+SYSTEM+','+BASE+',hicolor\nDirectories=places/scalable\n\n[places/scalable]\nSize=64\nMinSize=8\nMaxSize=512\nType=Scalable\nContext=Places\n'
def apply(color=None,restore=False):
 home=Path.home().resolve();icons=home/'.local/share/icons';state=home/'.local/state/gruvbox-cinnamon';journal=state/'install.json';prefs=state/'folder-colors.json'
 if not icons.resolve().is_relative_to(home) or not state.resolve().is_relative_to(home):raise RuntimeError('Destino fora da pasta pessoal; operação recusada.')
 gui=home/'.local/state/gruvbox-manager/installed.json'
 valid_gui=gui.is_file() and 'folder_colors' in json.loads(gui.read_text()).get('groups',[])
 if not valid_gui and (not journal.is_file() or json.loads(journal.read_text()).get('status')!='installed'):raise RuntimeError('Instale primeiro o pacote Gruvbox Cinnamon; nenhuma cor foi alterada.')
 state.mkdir(parents=True,exist_ok=True);state.chmod(0o700)
 with (state/'folder-colors.lock').open('a') as lock:
  try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:raise RuntimeError('Outra troca de cor está em andamento; tente novamente.')
  current={s:get(s) for s in SCHEMAS}
  if any(v not in (*SLOTS,BASE,SYSTEM) for v in current.values()):raise RuntimeError('Outro tema de ícones está selecionado. Volte ao Gruvbox antes de usar este seletor.')
  saved=json.loads(prefs.read_text()) if prefs.exists() else {}
  if not restore and any(v in SLOTS for v in current.values()) and len(set(current.values()))!=1:raise RuntimeError('As duas configurações de ícones divergem; restaure primeiro com --restore.')
  if restore:
   if not saved or not any(v in SLOTS for v in current.values()):print('A aparência original do pacote já está selecionada.');return
   before=saved['before']
   if any(v not in (BASE,SYSTEM) for v in before.values()):raise RuntimeError('Registro de restauração inválido.')
   try:
    for schema,name in before.items():set_theme(schema,name)
   except BaseException:
    for schema,name in current.items():set_theme(schema,name)
    raise
   saved['color']=None;atomic_json(prefs,saved);print('Aparência anterior ao seletor restaurada.');return
  if color not in COLORS:raise ValueError('Cor inválida.')
  base=(icons/BASE).resolve();places=base/'places/scalable'
  if not places.is_dir() or not (icons/SYSTEM/'index.theme').is_file():raise RuntimeError('Os temas exigidos não estão instalados.')
  # Build completely before touching any active theme. Do not recolor unrelated icons.
  data={}
  for src in sorted(places.glob('folder-'+color+'*.svg')):
   if not src.resolve().is_relative_to(base):raise RuntimeError('Arquivo de origem fora do tema-base.')
   name=src.name.replace('-'+color,'',1);data[name]=src.read_bytes()
  bookmark=places/('bookmarks-'+color+'.svg')
  if bookmark.is_file():
   if not bookmark.resolve().is_relative_to(base):raise RuntimeError('Bookmark fora do tema-base.')
   data['folder-bookmark.svg']=bookmark.read_bytes()
  if 'folder.svg' not in data:raise RuntimeError('O tema não contém esta variante de pasta.')
  # Symbolic aliases use the same artwork; Cinnamon's existing extension requests full color.
  for name,blob in list(data.items()):data[name[:-4]+'-symbolic.svg']=blob
  slot=SLOTS[1] if SLOTS[0] in current.values() else SLOTS[0]
  dest=icons/slot
  for owned in SLOTS:
   p=icons/owned
   if p.is_symlink() or not p.is_dir() or not (p/MARKER).is_file():raise RuntimeError('Variante própria ausente ou substituída: '+owned)
  tmp=Path(tempfile.mkdtemp(prefix='.gruvbox-pastas-',dir=icons));old=icons/('.gruvbox-pastas-anterior-'+uuid.uuid4().hex)
  replaced=False;switched=False
  previous=saved.get('before') if any(v in SLOTS for v in current.values()) else current
  if not previous:raise RuntimeError('Registro da aparência anterior ausente; operação recusada.')
  try:
   (tmp/'places/scalable').mkdir(parents=True);(tmp/MARKER).write_text('Gruvbox Cinnamon folder selector v1\n');(tmp/'index.theme').write_text(index(slot))
   for name,blob in data.items():(tmp/'places/scalable'/name).write_bytes(blob)
   os.replace(dest,old);replaced=True;os.replace(tmp,dest)
   try:
    for schema in SCHEMAS:set_theme(schema,slot)
    atomic_json(prefs,{'before':previous,'color':color,'slot':slot})
    switched=True
   except BaseException:
    for schema,name in current.items():set_theme(schema,name)
    raise
   shutil.rmtree(old)
  except BaseException:
   if replaced and not switched:
    if dest.exists():shutil.rmtree(dest)
    os.replace(old,dest)
   raise
  finally:
   if tmp.exists():shutil.rmtree(tmp)
  print('Cor das pastas: '+color+'. Temas originais preservados.')
def main():
 p=argparse.ArgumentParser(description='Escolher cor de pastas Gruvbox em variantes separadas.')
 g=p.add_mutually_exclusive_group();g.add_argument('-c','--color',choices=COLORS);g.add_argument('-C','--reset-color',action='store_true');g.add_argument('--restore',action='store_true');g.add_argument('-l','--list',action='store_true')
 a=p.parse_args()
 if a.list:print('Cores disponíveis: '+', '.join(COLORS));return
 if not a.color and not a.reset_color and not a.restore:p.print_help();return
 try:apply(a.color or ('plasma' if a.reset_color else None),a.restore)
 except Exception as e:print('Erro: '+str(e),file=sys.stderr);sys.exit(1)
if __name__=='__main__':main()
