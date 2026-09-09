#!/usr/bin/env python3
"""Build explicitly labeled full and compact review archives from local evidence."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json
import hashlib

HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]

def selected(full):
    for path in sorted(HERE.rglob('*')):
        if not path.is_file() or '__pycache__' in path.parts or path.name in ('site_data.json','package-manifest.json') or path.suffix in ('.zip','.pyc'):
            continue
        rel=path.relative_to(HERE).as_posix()
        if not full:
            if path.suffix in ('.png','.svg','.npz'):continue
            if rel.startswith('lattice/results/') and path.suffix=='.csv':continue
        yield path,rel

def package(target,full):
    entries=[]
    with ZipFile(target,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for path,rel in selected(full):
            blob=path.read_bytes();z.writestr('yangmills-round9/'+rel,blob)
            entries.append({'path':rel,'sha256':hashlib.sha256(blob).hexdigest(),'bytes':len(blob)})
        z.writestr('yangmills-round9/ARCHIVE-CONTENTS.json',json.dumps({'full_raw_data':full,'files':entries,'scope':'Finite SU2 research; not continuum Yang-Mills proof.'},indent=2))
    with ZipFile(target) as z:
        if z.testzip() is not None:raise RuntimeError('archive integrity failed')
    return {'path':str(target),'bytes':target.stat().st_size,'files':len(entries),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'full_raw_data':full}

def main():
    result=[package(PROJECT/'dist/research-round9.zip',False),package(PROJECT.parent/'yangmills-research-round9.zip',True)]
    (HERE/'package-manifest.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
