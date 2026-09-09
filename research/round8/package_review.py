#!/usr/bin/env python3
"""Package new evidence with original textual dependencies; never modify originals."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile

HERE=Path(__file__).resolve().parent
SITE=HERE.parents[1]

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--evidence',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--source-dependencies-only',action='store_true',help='Omit duplicate historical numerical histories from the Site download; keep runnable source and proof contracts.')
    args=p.parse_args()
    if not (args.evidence/'qeg-research/round7/finite_scalar.py').is_file():raise RuntimeError('Missing original evidence tree')
    files={}
    def add(path,name):files[name]=path.read_bytes()
    for name in ['README.md','reproduce.py']:add(HERE/name,name)
    for f in sorted((HERE/'gap').iterdir()):
        if f.is_file():add(f,'gap-output/'+f.name)
    for f in sorted((HERE/'audit').rglob('*')):
        if f.is_file() and '__pycache__' not in f.parts:add(f,'skeptic-output/'+f.relative_to(HERE/'audit').as_posix())
    for f in sorted(args.evidence.rglob('*')):
        allowed={'.py','.md','.txt'} if args.source_dependencies_only else {'.py','.json','.md','.csv','.txt'}
        if f.is_file() and (f.suffix in allowed or f.name in {'proof_library.json','proof_manifest.json'}) and '__pycache__' not in f.parts:
            add(f,'evidence/'+f.relative_to(args.evidence).as_posix())
    for name in ['proof_search.py','proof_routes.py','proof_manifest.json','proof_results.json','spectral-proof.md','advisor-dossier.md','integration-review.md']:
        add(HERE/name,'proof/'+name)
    for name in ['research-millennium.js','research-millennium-data.js','research-millennium.css']:
        add(SITE/'dist'/name,'site-review/'+name)
    for name in ['site-validation.json','site_data.json']:
        if (HERE/name).exists():add(HERE/name,'site-review/'+name)
    manifest={name:hashlib.sha256(value).hexdigest() for name,value in files.items()}
    files['manifest.json']=(json.dumps({'algorithm':'SHA-256','files':manifest},indent=2)+'\n').encode()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(args.output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name,data in sorted(files.items()):
            info=zipfile.ZipInfo(name,(2026,9,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,data)
    print(json.dumps({'files':len(files),'bytes':args.output.stat().st_size,'sha256':hashlib.sha256(args.output.read_bytes()).hexdigest()}))

if __name__=='__main__':main()
