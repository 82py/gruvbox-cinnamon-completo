#!/usr/bin/python3
"""Verifica idiomas e destinos locais da documentação própria, sem acessar a sessão."""
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
files=sorted(list(ROOT.glob('*.md'))+list((ROOT/'docs').glob('*.md')))
errors=[];links=0
for p in files:
    text=p.read_text()
    if not ('## English' in text and '## Português' in text and text.index('## English')<text.index('## Português')):
        errors.append(str(p.relative_to(ROOT))+': inglês deve vir antes do português')
    for target in re.findall(r'\]\(([^)\s]+)(?:\s+"[^"]*")?\)',text):
        url=urlsplit(target)
        if url.scheme or url.netloc:continue
        dest=(p.parent/unquote(url.path)).resolve() if url.path else p
        links+=1
        if not dest.exists():errors.append(str(p.relative_to(ROOT))+': link ausente '+target)
        elif url.fragment in ('english','português') and dest.suffix=='.md':
            heading='## English' if url.fragment=='english' else '## Português'
            if heading not in dest.read_text():errors.append('Âncora ausente: '+target)
if errors:raise SystemExit('\n'.join(errors))
print(f'OK: {len(files)} documentos bilíngues, inglês primeiro; {links} links locais conferidos.')
