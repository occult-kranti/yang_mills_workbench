"""Package authored research, checks and frozen historical model dependencies."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT=Path(__file__).resolve().parent


def main():
    qa=json.loads((ROOT/'visual_qa.json').read_text())
    pdf=ROOT/'output/pdf/bidirectional-proof-dossier.pdf'
    assert qa['accepted'] and qa['pdf_sha256']==hashlib.sha256(pdf.read_bytes()).hexdigest()
    files={p:Path('qeg-research/round5')/p.name for p in ROOT.iterdir()
           if p.is_file() and p.suffix in {'.py','.md','.json','.txt'}}
    old=['round3/code/backreaction.py','round4/code/response.py','round4/response_contract.md',
         'round4/physics_acceptance.json','round4/response_results.json',
         'round4/response_verification.json','round4/response_production_comparison.json']
    for name in old:
        p=ROOT.parent/name
        if p.exists(): files[p]=Path('qeg-research')/name
    for name in ['bidirectional-proof-dossier.diagnostics.json']:
        p=ROOT/'output/pdf'/name
        files[p]=Path('qeg-research/round5/output/pdf')/name
    hashes={str(archive):hashlib.sha256(p.read_bytes()).hexdigest() for p,archive in files.items()}
    out=ROOT/'output/bidirectional-proof-research.zip'
    out.parent.mkdir(exist_ok=True,parents=True)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p,archive in sorted(files.items(),key=lambda item:str(item[1])): z.write(p,str(archive))
        z.writestr('SHA256SUMS.json',json.dumps(hashes,indent=2)+'\n')
        z.writestr('README.md','# Bidirectional proof research\n\nRead `qeg-research/round5/README.md` for the theorem, sources and runnable checks. The PDF is supplied separately.\n\nFrom the extracted folder, enter `qeg-research/round5`, install its requirements in a virtual environment, and run `python run_checks.py`. No model API is required.\n\nThis is a conditional finite-model proof and research map. Continuum QED and gravitational closure remain unresolved.\n')
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for name,digest in hashes.items(): assert hashlib.sha256(z.read(name)).hexdigest()==digest
    (ROOT/'output/package_manifest.json').write_text(json.dumps({'file':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'authored_and_dependency_files':len(files),'all_member_hashes_verified':True,'excludes':['temporary dependencies','formula caches','third-party papers and books','Site repository']},indent=2)+'\n')
    print(json.dumps({'archive':str(out),'files':len(files),'bytes':out.stat().st_size,'member_hashes_verified':True}))


if __name__=='__main__':main()
