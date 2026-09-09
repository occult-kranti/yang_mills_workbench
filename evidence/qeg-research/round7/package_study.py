"""Package this research snapshot and its required historical references."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=HERE/'output'
skip={'deps','__pycache__','tmp','output','.venv','node_modules'}
exts={'.py','.json','.md','.csv','.txt'}
files=[]
for name in ('round3','round4','round5','round6','round7'):
    for p in sorted((ROOT/name).rglob('*')):
        rel=p.relative_to(ROOT)
        if not p.is_file() or p.suffix not in exts:continue
        if any(part in skip or part.startswith('tmp') for part in rel.parts):continue
        if p.name in {'site_data.json','response_results.csv'}:continue
        files.append(p)
files += [OUT/'einstein-qed-variable-study.pdf']+[OUT/(x+'.png') for x in ('finite','work','gravity')]
manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
archive=OUT/'einstein-qed-variable-study.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,'qeg-research/'+str(p.relative_to(ROOT)))
    z.writestr('research-manifest.json',json.dumps({'scope':'Project-authored research, figure exports and required historical snapshots; third-party dependencies and source publications are not bundled.','sha256':manifest},indent=2)+'\n')
    z.writestr('START-HERE.txt','Read qeg-research/round7/README.md or qeg-research/round7/output/einstein-qed-variable-study.pdf.\nInstall qeg-research/round7/requirements.txt to run the current solvers.\nRounds 3-6 and initial_implementations are historical evidence, not the current acceptance path.\n')
with zipfile.ZipFile(archive) as z:
    if z.testzip() is not None:raise RuntimeError('Archive CRC failure')
    for name,digest in manifest.items():
        if hashlib.sha256(z.read('qeg-research/'+name)).hexdigest()!=digest:
            raise RuntimeError('Archive hash mismatch: '+name)
shutil.copy2(archive,ROOT.parent/'physics-observatory/dist/research-review.zip')
print(json.dumps({'archive':str(archive),'files':len(files),'bytes':archive.stat().st_size,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'all_content_hashes_verified':True}))
