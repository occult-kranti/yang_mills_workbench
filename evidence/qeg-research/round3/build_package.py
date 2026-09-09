#!/usr/bin/env python3
"""Package authored research, source metadata and measured data; no paper copies."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent
OUT=ROOT/'output/qeg-research-reproducibility.zip'
ALLOW={'.py','.md','.json','.csv','.txt'}
EXCLUDE={'tmp','__pycache__','vendor-python','.venv','node_modules','.git'}

def include(p,base):
    rel=p.relative_to(base)
    if any(part in EXCLUDE for part in rel.parts):return False
    if p.name in {'package_integrity.json','MANIFEST.json'}:return False
    if p.suffix.lower() in ALLOW:return True
    return p==ROOT/'output/pdf/quantum_electromagnetism_gravity_research.pdf'

files=[]
for base in [ROOT,PROJECT/'retry']:
    for p in base.rglob('*'):
        if p.is_file() and include(p,base):files.append(p)
files=sorted(set(files))
members={str(Path('qeg-research')/p.relative_to(PROJECT)):p for p in files}
manifest={'scope':'Project-authored code, research, source metadata, measured results and final PDF. No full third-party papers/books or vendor copies.',
 'files':{n:{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for n,p in members.items()}}
OUT.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for n,p in members.items():z.write(p,n)
    z.writestr('MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT) as z:
    bad=z.testzip()
    if bad:raise RuntimeError('CRC failure '+bad)
    for n,item in manifest['files'].items():
        if hashlib.sha256(z.read(n)).hexdigest()!=item['sha256']:raise RuntimeError('SHA failure '+n)
status={'archive':OUT.name,'member_count':len(members)+1,'bytes':OUT.stat().st_size,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'crc_passed':True,'all_manifest_hashes_passed':True}
(ROOT/'output/package_integrity.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps(status))
