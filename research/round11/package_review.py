#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib,json
HERE=Path(__file__).resolve().parent
path=HERE.parents[1]/'dist/research-round11.zip'
rows=[]
with ZipFile(path,'w',ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(HERE.rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts or p.suffix in ('.pyc','.zip'):continue
        rel=p.relative_to(HERE).as_posix();data=p.read_bytes()
        z.writestr('two-plaquette-study/'+rel,data)
        rows.append({'file':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    z.writestr('two-plaquette-study/ARCHIVE-CONTENTS.json',json.dumps(rows,indent=2))
with ZipFile(path) as z:
    if z.testzip() is not None:raise RuntimeError('Research archive is invalid')
print(json.dumps({'file':str(path),'files':len(rows),'bytes':path.stat().st_size}))
