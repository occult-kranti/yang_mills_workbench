#!/usr/bin/env python3
"""Deterministic archive with a complete byte inventory and accepted-source checks."""
from pathlib import Path
import hashlib,json,zipfile
from build_site_data import verify_gates
HERE=Path(__file__).resolve().parent
DIST=HERE.parents[1]/'dist'
def main():
    verify_gates()
    files=[p for p in sorted(HERE.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.zip') and p.name!='archive-inventory.json']
    if any(p.is_symlink() for p in files):raise ValueError('Symlink artifact cannot enter archive')
    if any(any(x.startswith(('ym15-admission-','ym15-rerun-')) for x in p.parts) for p in files):raise ValueError('Temporary replay entered research tree')
    inventory={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    inv=HERE/'archive-inventory.json';inv.write_text(json.dumps({'schema':'ym15-archive-v1','sha256':inventory},indent=2)+'\n')
    target=DIST/'research-round15.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files+[inv]:
            info=zipfile.ZipInfo('round15/'+str(p.relative_to(HERE)),date_time=(2026,9,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,p.read_bytes())
    with zipfile.ZipFile(target) as z:
        if z.testzip() is not None:raise ValueError('Archive CRC failure')
        for name,h in inventory.items():
            if hashlib.sha256(z.read('round15/'+name)).hexdigest()!=h:raise ValueError('Archive byte mismatch '+name)
    print(json.dumps({'status':'packaged','files':len(files)+1,'bytes':target.stat().st_size}))
if __name__=='__main__':main()
