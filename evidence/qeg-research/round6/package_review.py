"""Package project-authored research and necessary frozen references; no dependencies."""
from pathlib import Path
import hashlib,json,zipfile,shutil

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=HERE/'output'
OUT.mkdir(exist_ok=True)
skip={'deps','__pycache__','tmp','output','.venv','node_modules'}
exts={'.py','.json','.md','.csv','.txt'}
files=[]
for round_name in ['round3','round4','round5','round6']:
    for path in sorted((ROOT/round_name).rglob('*')):
        rel=path.relative_to(ROOT)
        if not path.is_file() or path.suffix not in exts:continue
        if any(part in skip or part.startswith('tmp') for part in rel.parts):continue
        if path.name in {'site_data.json','response_results.csv'}:continue
        files.append(path)
manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(OUT/'review-manifest.json').write_text(json.dumps({'scope':'Project-authored research files and frozen references; dependencies and duplicate Site payloads excluded.','sha256':manifest},indent=2)+'\n')
archive=OUT/'physics-observatory-skeptical-review.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for path in files:z.write(path,'qeg-research/'+str(path.relative_to(ROOT)))
    z.write(OUT/'review-manifest.json','review-manifest.json')
    z.writestr('START-HERE.txt','Read qeg-research/round6/README.md. Install qeg-research/round6/requirements.txt before running the scientific checks. Historical snapshots are retained.\n')
with zipfile.ZipFile(archive) as z:
    if z.testzip() is not None:raise RuntimeError('Archive CRC verification failed')
    for name,digest in manifest.items():
        if hashlib.sha256(z.read('qeg-research/'+name)).hexdigest()!=digest:raise RuntimeError('Packaged content mismatch: '+name)
shutil.copy2(archive,ROOT.parent/'physics-observatory/dist/research-review.zip')
print(json.dumps({'archive':str(archive),'files':len(files),'bytes':archive.stat().st_size,'content_hashes_verified':True}))
