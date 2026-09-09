#!/usr/bin/env python3
"""Package portable round12 research with exact file-byte inventory."""
from pathlib import Path
import hashlib
import json
import zipfile
from trace_archive import verify_archives

HERE=Path(__file__).resolve().parent
DEST=HERE.parents[1]/'dist/research-round12.zip'

def main():
    traces=verify_archives()
    files=[]
    for p in sorted(HERE.rglob('*')):
        if p.is_symlink():raise ValueError('Symlink research input rejected: '+str(p))
        if str(p.relative_to(HERE)) in traces:continue
        if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.zip'):
            files.append(p)
    manifest={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    with zipfile.ZipFile(DEST,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in files:z.write(p,'yangmills-round12/'+str(p.relative_to(HERE)))
        z.writestr('yangmills-round12/ARCHIVE-CONTENTS.json',json.dumps({'sha256':manifest},indent=2)+'\n')
    with zipfile.ZipFile(DEST) as z:
        for rel,digest in manifest.items():
            if hashlib.sha256(z.read('yangmills-round12/'+rel)).hexdigest()!=digest:raise ValueError('Archive verification failed')
    print(json.dumps({'files':len(files),'bytes':DEST.stat().st_size,'path':str(DEST)}))

if __name__=='__main__':main()
