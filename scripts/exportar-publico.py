#!/usr/bin/python3
"""Cria somente uma árvore pública conservadora; não acessa nem publica no GitHub."""
from pathlib import Path
import shutil,tarfile,json,hashlib
R=Path(__file__).resolve().parents[1];out=R.parent/('Gruvbox-Cinnamon-GitHub-'+json.loads((R/'manifest.json').read_text())['version'])
if out.exists():raise SystemExit('Destino já existe; mantenha a cópia anterior ou escolha outra versão.')
exclude=['assets-locais','.git','__pycache__','SHA256SUMS','RELATORIO-VALIDACAO.json']
def ignored(directory,names):
 rel=Path(directory).relative_to(R)
 return [n for n in names if any((rel/n)==Path(e) for e in exclude) or n.endswith('.pyc')]
shutil.copytree(R,out,symlinks=True,ignore=ignored)
manifest=json.loads((out/'manifest.json').read_text());missing=[u for u in manifest['units'] if not (out/u['source']).exists()]
(out/'DISTRIBUICAO.json').write_text(json.dumps({'note':'Distribuição pública. O instalador compila xwinwrap do fonte incluído; o binário da máquina de origem não é distribuído.','components':missing},ensure_ascii=False,indent=2)+'\n')
archive=Path(str(out)+'.tar.gz')
def clean(info):
 info.uid=0;info.gid=0;info.uname='';info.gname='';return info
with tarfile.open(archive,'w:gz') as tf:tf.add(out,arcname=out.name,filter=clean)
archive.with_name(archive.name+'.sha256').write_text(hashlib.sha256(archive.read_bytes()).hexdigest()+'  '+archive.name+'\n')
print(out);print(archive)
