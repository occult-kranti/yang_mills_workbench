#!/usr/bin/env python3
"""Write an advisor-authored contract only after its explicit selection record exists."""
from pathlib import Path
import datetime,hashlib,json
ROOT=Path(__file__).resolve().parents[3]
R=ROOT/'research/round24'
def freeze(loop,*,target,model,scales,parameters,acceptance,dependencies,selection_record):
    p=R/f'contracts/{loop}.json'
    if p.exists(): raise ValueError('Contract already frozen')
    if not (ROOT/selection_record).is_file(): raise ValueError('Missing prior advisor decision')
    dependencies=list(dict.fromkeys([selection_record]+dependencies))
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    data={'schema':'ym24-contract-v1','loop':loop,'status':'frozen','selected_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'target':target,'model':model,'scales':scales,'parameters':parameters,'acceptance':acceptance,'selection_record':selection_record,'dependencies':{n:sha(ROOT/n) for n in dependencies},'instruction_inputs':{str(p.relative_to(ROOT)):sha(p) for p in sorted((R/'methods').glob('*.md'))},'review':'Independent forward/reverse frozen before skeptic review; completion may be limited or insufficient; no continuum/priority inference.'}
    p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    return p
