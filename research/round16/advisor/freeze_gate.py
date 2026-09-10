"""Freeze a reviewed loop's complete file inventory after independent acceptance."""
from pathlib import Path
import argparse, hashlib, json
HERE=Path(__file__).resolve().parents[1]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inventory(loop):
    roots=[HERE/'forward'/loop,HERE/'backward'/loop]
    paths=[]
    for root in roots:
        if not root.is_dir():raise ValueError('Missing role directory')
        for p in sorted(root.rglob('*')):
            if '__pycache__' in p.parts:continue
            if p.is_symlink():raise ValueError('Symlink evidence not accepted')
            if p.is_file():paths.append(p)
    paths += [HERE/'advisor/contract.md']
    if loop=='loop1':paths += [HERE/'advisor'/n for n in ('energy_scale.py','energy_scale.md','scale-output/review.json','scale-output/energy_scale.csv')]
    else:paths += [HERE/'advisor/loop2-contract.md',HERE/'advisor/loop1-gate.json']
    return {str(p.relative_to(HERE)):digest(p) for p in paths}
def verify(path):
    r=json.loads(Path(path).read_bytes())
    if r.get('status')!='accepted' or r['files']!=inventory(r['loop']):raise ValueError('Stale/incomplete gate')
    return r
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('gate');a=p.parse_args();print(json.dumps({'status':'passed','loop':verify(a.gate)['loop']}))
