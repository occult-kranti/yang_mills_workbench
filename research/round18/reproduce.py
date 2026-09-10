#!/usr/bin/env python3
"""Reproduce all six loops from frozen sources in a new output directory."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys
HERE=Path(__file__).resolve().parent
LOOPS=('a1','a2','b1','b2','c1','c2')

def main(output, optimized=False, independent_only=False):
    out=Path(output).expanduser().resolve()
    if out.exists() or out==HERE or HERE in out.parents:
        raise ValueError('Use a new output directory outside the accepted round18 tree')
    sys.path.insert(0,str(HERE/'advisor'))
    from freeze_gate import verify
    for loop in LOOPS:
        verify(HERE/'advisor'/(loop+'-gate.json'))
    out.mkdir(parents=True)
    source=out/'source'
    shutil.copytree(HERE,source,ignore=shutil.ignore_patterns('__pycache__','*.pyc','figures'))
    python=[sys.executable]+(['-O'] if optimized else [])
    roles=('backward',) if independent_only else ('forward','backward')
    runs=[]
    for loop in LOOPS:
        for role in roles:
            target=out/'runs'/role/loop
            target.parent.mkdir(parents=True,exist_ok=True)
            proc=subprocess.run(python+[str(source/role/loop/'check.py'),'--output',str(target)],cwd=source,capture_output=True,text=True,timeout=240)
            if proc.returncode:
                raise RuntimeError(role+'/'+loop+': '+proc.stderr[-1800:])
            actual=target/'results.json'
            record=json.loads(actual.read_bytes())
            expected=json.loads((HERE/role/loop/'output/results.json').read_bytes())
            if record.get('status')!='passed' or type(record.get('checks_count')) is not int or record['checks_count']<=0:
                raise ValueError('Missing executed acceptance '+role+'/'+loop)
            if record!=expected:
                raise ValueError('Semantic reproduction differs '+role+'/'+loop)
            runs.append({'loop':loop,'role':role,'status':'passed','checks_count':record['checks_count'],'results_sha256':hashlib.sha256(actual.read_bytes()).hexdigest()})
        compare=source/'backward'/loop/'compare.py'
        if not compare.is_file():raise ValueError('Missing independent comparison '+loop)
        target=out/'runs/comparison'/loop;target.parent.mkdir(parents=True,exist_ok=True)
        evidence=source/'forward'/loop/'output' if independent_only else out/'runs/forward'/loop
        proc=subprocess.run(python+[str(compare),'--producer',str(source/'forward'/loop),'--evidence',str(evidence),'--output',str(target)],cwd=source,capture_output=True,text=True,timeout=240)
        if proc.returncode:raise RuntimeError('comparison/'+loop+': '+proc.stderr[-1800:])
        actual=target/'results.json';record=json.loads(actual.read_bytes());expected=json.loads((HERE/'backward'/loop/'comparison/results.json').read_bytes())
        if record.get('status')!='passed' or type(record.get('checks_count')) is not int or record['checks_count']<=0 or record!=expected:raise ValueError('Independent comparison differs '+loop)
        runs.append({'loop':loop,'role':'comparison','status':'passed','checks_count':record['checks_count'],'results_sha256':hashlib.sha256(actual.read_bytes()).hexdigest()})
    report={'status':'passed','loops':6,'scientific_roles':3,'optimized':optimized,'independent_only':independent_only,'runs':runs,'scope':'Fresh execution and exact semantic comparison. Normal/optimized runs repeat the same checks, counted once; conventional proofs also require the written domain arguments.'}
    (out/'reproduction.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='runs'}))
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--optimized',action='store_true');p.add_argument('--independent-only',action='store_true');a=p.parse_args()
    main(a.output,a.optimized,a.independent_only)
