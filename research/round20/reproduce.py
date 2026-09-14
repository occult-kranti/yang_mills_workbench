#!/usr/bin/env python3
"""Verify reviewed actual bytes, replay independent Round20 checks and compare results."""
import argparse, hashlib, json, pathlib, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
HERE=pathlib.Path(__file__).resolve().parent

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def local(name):
    q=pathlib.Path(name)
    if q.is_absolute() or '..' in q.parts: raise ValueError('nonlocal path')
    p=ROOT/q
    if not p.is_file() or p.is_symlink(): raise ValueError('missing/linked file: '+name)
    return p

def gate_check(loop):
    p=HERE/'advisor'/f'{loop}-gate.json'; g=json.loads(p.read_text())
    if g.get('status') not in ('accepted','limited') or g.get('loop')!=loop: raise ValueError('unadmitted loop '+loop)
    if not isinstance(g.get('files'),dict) or not g['files']: raise ValueError('empty inventory')
    for name,want in g['files'].items():
        if digest(local(name))!=want: raise ValueError('stale admitted bytes '+name)
    return g

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--output',type=pathlib.Path,required=True); ap.add_argument('--loops',nargs='+'); ap.add_argument('--optimized',action='store_true'); a=ap.parse_args()
    out=a.output.resolve()
    if out.exists() or HERE in out.parents: raise ValueError('new replay directory outside research/round20 required')
    loops=a.loops or json.loads((HERE/'execution.json').read_text())['completed_loops']
    gates={n:gate_check(n) for n in loops}; out.mkdir(parents=True); runs=[]
    for loop,g in gates.items():
        for direction in ('forward','reverse'):
            cmd=[sys.executable,'-B']+(['-O'] if a.optimized else [])+[str(local(f'research/round20/{direction}/{loop}/check.py')),'--output',str(out/loop/direction)]
            p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
            (out/loop).mkdir(exist_ok=True); (out/loop/f'{direction}.log').write_text(p.stdout+p.stderr)
            if p.returncode: raise RuntimeError('replay failed '+loop+'/'+direction)
            actual=out/loop/direction/'results.json'; expected=local(f'research/round20/{direction}/{loop}/output/results.json')
            if actual.read_bytes()!=expected.read_bytes(): raise ValueError('result drift '+loop+'/'+direction)
            runs.append({'loop':loop,'direction':direction,'status':'passed','source_sha256':digest(local(f'research/round20/{direction}/{loop}/check.py')),'results_sha256':digest(actual)})
        gate_check(loop)
    result={'status':'passed','loops':loops,'optimized':a.optimized,'executions':runs,'counting':'Each pair of independent directions is one loop. Optimized repeats are zero additional loops.'}
    (out/'reproduction.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps({'status':'passed','loops':len(loops),'executions':len(runs)}))
if __name__=='__main__': main()
