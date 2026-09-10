#!/usr/bin/env python3
"""Deterministic reproducibility archive with a byte inventory."""
from pathlib import Path
import hashlib,json,sys,zipfile
HERE=Path(__file__).resolve().parent;DIST=HERE.parents[1]/'dist'
sys.path.insert(0,str(HERE/'advisor'));from freeze_gate import verify

def main():
    for loop in ('a1','a2','b1','b2','c1','c2'):verify(HERE/'advisor'/(loop+'-gate.json'))
    files=[]
    for p in sorted(HERE.rglob('*')):
        if '__pycache__' in p.parts or p.name=='archive-inventory.json' or p.suffix in ('.pyc','.zip'):continue
        if p.is_symlink():raise ValueError('No symlinks in archive')
        if p.is_file():files.append(p)
    name=DIST/'research-round17.zip';inventory={}
    with zipfile.ZipFile(name,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:
            rel='round17/'+str(p.relative_to(HERE));data=p.read_bytes()
            entry=zipfile.ZipInfo(rel,date_time=(2026,9,10,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED;entry.external_attr=0o100644<<16
            z.writestr(entry,data);inventory[rel]=hashlib.sha256(data).hexdigest()
    with zipfile.ZipFile(name) as z:
        if z.testzip() is not None or set(z.namelist())!=set(inventory):raise ValueError('Incomplete archive')
        for rel,digest in inventory.items():
            if hashlib.sha256(z.read(rel)).hexdigest()!=digest:raise ValueError('Archive byte mismatch')
    result={'status':'passed','files':inventory,'archive_sha256':hashlib.sha256(name.read_bytes()).hexdigest(),'bytes':name.stat().st_size,'scope':'Round17 reproducible research package. Website launcher is in the full GitHub repository; see README.'}
    (HERE/'archive-inventory.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','files':len(files),'bytes':result['bytes']}))
if __name__=='__main__':main()
