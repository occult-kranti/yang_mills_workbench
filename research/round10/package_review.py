#!/usr/bin/env python3
"""Create full evidence and compact Site packages without historical overwrite."""
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import json,hashlib
HERE=Path(__file__).resolve().parent
PROJECT=HERE.parents[1]
def package(path,full):
    entries=[]
    with ZipFile(path,'w',ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(HERE.rglob('*')):
            if not p.is_file() or '__pycache__' in p.parts or p.name in ('site_data.json','package-manifest.json') or p.suffix in ('.zip','.pyc'):continue
            rel=p.relative_to(HERE).as_posix()
            if not full and (p.suffix in ('.png','.svg') or '/initial_proof_manifest_probe/' in '/'+rel or '/omitted_midpoint_work_probe/' in '/'+rel or '/corrected_proof_probe/' in '/'+rel):continue
            data=p.read_bytes();z.writestr('yangmills-coupling-study/'+rel,data)
            entries.append({'path':rel,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        z.writestr('yangmills-coupling-study/ARCHIVE-CONTENTS.json',json.dumps({'full_figures_and_probes':full,'files':entries},indent=2))
    with ZipFile(path) as z:
        if z.testzip() is not None:raise RuntimeError('invalid archive')
    return {'path':str(path),'files':len(entries),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
def main():
    result=[package(PROJECT/'dist/research-round10.zip',False),package(PROJECT.parent/'yangmills-continuous-coupling-study.zip',True)]
    (HERE/'package-manifest.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
