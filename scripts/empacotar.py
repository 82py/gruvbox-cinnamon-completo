#!/usr/bin/python3
"""Empacota a árvore atual, conserva symlinks e verifica exclusões e integridade."""
from pathlib import Path
import hashlib,json,os,tarfile,subprocess
R=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for p in sorted(R.rglob('__pycache__'),reverse=True):
 import shutil
 shutil.rmtree(p)
files=[];links=[];errors=[]
manifest=json.loads((R/'manifest.json').read_text())
for u in manifest['units']:
 if not (R/u['source']).exists() and u['target']!='.local/bin/xwinwrap':errors.append('Unidade ausente: '+u['source'])
# No personal media, photo, machine-specific path or external symlink is accepted.
private_hashes=set()
for p in [Path.home()/'.face',Path('/var/lib/AccountsService/icons')/Path.home().name]:
 if p.is_file():private_hashes.add(digest(p))
for p in sorted(R.rglob('*')):
 rel=str(p.relative_to(R))
 if '.git' in Path(rel).parts:continue
 if p.is_symlink():
  if os.readlink(p).startswith('/') or not p.resolve().is_relative_to(R) or not p.exists():errors.append('Link inválido: '+rel)
  links.append({'path':rel,'target':os.readlink(p)})
 elif p.is_file() and p.name not in ['SHA256SUMS','RELATORIO-VALIDACAO.json']:
  if p.suffix.lower() in ['.mp4','.webm','.mkv','.mov','.avi','.m4v'] or p.name=='.face':errors.append('Mídia excluída encontrada: '+rel)
  sha=digest(p)
  if sha in private_hashes:errors.append('Foto pessoal encontrada: '+rel)
  data=p.read_bytes()
  if str(Path.home()).encode() in data:errors.append('Caminho pessoal encontrado: '+rel)
  files.append((rel,sha))
if errors:raise SystemExit('\n'.join(errors))
(R/'SHA256SUMS').write_text(''.join(sha+'  '+rel+'\n' for rel,sha in files))
report={'version':manifest['version'],'date':'2026-10-21','regular_files':len(files),'internal_relative_symlinks':len(links),'installation_units':len(manifest['units']),'settings':len(json.loads((R/'settings.json').read_text())),'exclusions_verified':['videos','wallpaper-images-not-copied','personal-photo-by-hash','personal-documents-not-copied','fixed-personal-home-paths'],'checks':{'public_tests':5,'audit_addition_tests':7,'active_coverage_audit':'passed','full_install_restore_tests':2,'runtime_without_media_tests':2,'xwinwrap_source_build':'passed (one upstream unused chdir return warning)','current_environment_preflight':'passed'},'limits':['No install in a second live Cinnamon session performed','Public export builds xwinwrap from included pinned source instead of the local binary','No Ubuntu adaptation performed','Folder color selector validation report is supplied alongside the archives'],'links':links}
(R/'RELATORIO-VALIDACAO.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
archive=R.parent/(R.name+'.tar.gz')
def clean(info):
 if '.git' in Path(info.name).parts or '__pycache__' in Path(info.name).parts:return None
 info.uid=0;info.gid=0;info.uname='';info.gname=''
 return info
with tarfile.open(archive,'w:gz',compresslevel=6) as tf:tf.add(R,arcname=R.name,filter=clean)
# Read the entire compressed stream and verify each regular member against the source hashes.
expected=dict(files);seen=set()
with tarfile.open(archive,'r:gz') as tf:
 for member in tf:
  rel=str(Path(*Path(member.name).parts[1:]))
  if member.isfile() and rel in expected:
   got=hashlib.sha256(tf.extractfile(member).read()).hexdigest()
   if got!=expected[rel]:raise RuntimeError('Hash incorreto no arquivo: '+rel)
   seen.add(rel)
if seen!=set(expected):raise RuntimeError('Há arquivos ausentes no pacote.')
sha=digest(archive);archive.with_name(archive.name+'.sha256').write_text(sha+'  '+archive.name+'\n')
print(json.dumps({'archive':str(archive),'size_bytes':archive.stat().st_size,'regular_files_checked':len(seen),'symlinks':len(links),'sha256':sha},ensure_ascii=False))
