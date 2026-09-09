"""Package owned research records, executable code and historical evidence."""
from pathlib import Path
import hashlib,json,zipfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=HERE/'output/qeg-response-research.zip'
files=[]
for folder in [ROOT/'round3',HERE]:
    files.extend(p for p in folder.iterdir() if p.is_file() and p.suffix in {'.py','.md','.json','.csv','.txt'})
    for child in ['code','results','figures','verification_evidence']:
        d=folder/child
        if d.exists():files.extend(p for p in d.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix in {'.py','.md','.json','.csv','.txt','.png','.svg'})
files=sorted(set(files))
manifest={'description':'Reviewed cycle4 plus unchanged cycle3 historical evidence; website source is maintained separately.','files':[{'path':str(p.relative_to(ROOT.parent)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
OUT.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(OUT,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:z.write(p,str(p.relative_to(ROOT.parent)))
    z.writestr('qeg-research/MANIFEST.json',json.dumps(manifest,indent=2)+'\n')
with zipfile.ZipFile(OUT) as z:
    assert z.testzip() is None
    for item in manifest['files']:assert hashlib.sha256(z.read(item['path'])).hexdigest()==item['sha256']
summary={'file':str(OUT),'bytes':OUT.stat().st_size,'members':len(files)+1,'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'crc_and_member_hashes':'passed'}
(HERE/'output/package_validation.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
