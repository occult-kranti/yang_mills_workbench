#!/usr/bin/env python3
"""Reproduce the five actual research programs in a separate output tree."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent

def main(output,optimized=False):
    out=Path(output).expanduser().resolve()
    if out==HERE or HERE in out.parents or out.exists():raise ValueError('Use a new output folder outside the accepted round16 tree')
    sys.path.insert(0,str(HERE/'advisor'));from freeze_gate import verify
    for loop in ('loop1','loop2'):verify(HERE/'advisor'/(loop+'-gate.json'))
    out.mkdir(parents=True);source=out/'source'
    for role in ('forward','backward','advisor'):
        shutil.copytree(HERE/role,source/role,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    python=[sys.executable]+(['-O'] if optimized else []);runs=[]
    jobs=[('forward-loop1','forward/loop1/run_loop1.py',lambda t:[t],'forward/loop1/output/results.json','results.json'),
          ('scale','advisor/energy_scale.py',lambda t:['--output',t],'advisor/scale-output/review.json','review.json'),
          ('backward-loop1','backward/loop1/verify_loop1.py',lambda t:['--producer',source/'forward/loop1','--scale',source/'advisor','--output',t],'backward/loop1/final/review.json','review.json'),
          ('forward-loop2','forward/loop2/run_loop2.py',lambda t:[t],'forward/loop2/output/results.json','results.json'),
          ('backward-loop2','backward/loop2/verify_loop2.py',lambda t:['--producer',source/'forward/loop2','--output',t],'backward/loop2/output/review.json','review.json')]
    for name,script,args,expected,reportname in jobs:
        target=out/'runs'/name;target.parent.mkdir(exist_ok=True)
        command=python+[str(source/script)]+list(map(str,args(target)))
        p=subprocess.run(command,cwd=source,capture_output=True,text=True,timeout=180)
        target.mkdir(exist_ok=True);(target/'stdout.txt').write_text(p.stdout);(target/'stderr.txt').write_text(p.stderr)
        if p.returncode:raise RuntimeError(name+': '+p.stderr[-1000:])
        actual=target/reportname;record=json.loads(actual.read_bytes())
        if record.get('status')!='passed' or actual.read_bytes()!=(HERE/expected).read_bytes():raise ValueError('Semantic or byte replay failed '+name)
        comparisons={reportname:hashlib.sha256(actual.read_bytes()).hexdigest()}
        if name.startswith('forward-'):
            original=(HERE/expected).parent
            for f in sorted(original.iterdir()):
                if f.is_file():
                    if (target/f.name).read_bytes()!=f.read_bytes():raise ValueError('Output mismatch '+name+'/'+f.name)
                    comparisons[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
        runs.append({'name':name,'command':command,'status':'passed','matched_output_sha256':comparisons})
    report={'status':'passed','loops':2,'scientific_roles':3,'programs':len(runs),'optimized':optimized,'runs':runs,
            'scope':'Actual programs, exact outputs and semantic results; optimized mode repeats the same gates. Float diagnostic bytes may differ on another numerical platform.'}
    (out/'reproduction.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='runs'}));return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--optimized',action='store_true');a=p.parse_args();main(a.output,a.optimized)
