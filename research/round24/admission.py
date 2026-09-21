#!/usr/bin/env python3
"""Admit reviewed paired evidence and reproduce executed checks, never infer a proof from hashes."""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys
sys.dont_write_bytecode = True
ROOT=Path(__file__).resolve().parents[2]
ROUND='research/round24'
LOOPS=('v1','v2','w1','w2','x1','x2','y1','y2','z1','z2')
def require(ok,message):
    if not ok: raise ValueError(message)
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path): return json.loads(path.read_text())
def external_output(path):
    out=path.absolute()
    require(not out.exists() and not out.resolve().is_relative_to(ROOT.resolve()),'choose fresh output outside checkout')
    return out
def source(name):
    p=ROOT/name
    require(not Path(name).is_absolute() and '..' not in Path(name).parts,'unsafe source path')
    require(p.is_file() and not any(x.is_symlink() for x in [p,*p.parents] if x!=ROOT and ROOT in x.parents) and p.resolve().is_relative_to(ROOT.resolve()),'missing or linked source: '+name)
    return p
def payload(loop,direction,folder,expected=None):
    result=read(folder/'results.json'); controls=read(folder/'controls.json')
    require(result.get('loop')==loop and result.get('direction')==direction and result.get('status')=='passed','invalid result identity/status')
    require(isinstance(result.get('claims'),list) and result['claims'],'missing claims')
    require(isinstance(result.get('limitations'),list) and result['limitations'],'missing limitations')
    c=controls.get('controls',{})
    require(isinstance(c,dict) and len(c)>=3 and all(type(v) is bool and v for v in c.values()),'invalid required controls')
    if expected is not None: require({'results':result,'controls':controls}==expected,'reviewed payload changed')
    return {'results':result,'controls':controls}
def submission(loop,direction):
    prefix=f'{ROUND}/{direction}/{loop}'
    s=read(source(prefix+'/submission.json'))
    require(s.get('loop')==loop and s.get('direction')==direction,'submission identity')
    files=s.get('files',{})
    contract_path=f'{ROUND}/contracts/{loop}.json'; contract=read(source(contract_path))
    required={contract_path,prefix+'/report.md',prefix+'/check.py',prefix+'/output/results.json',prefix+'/output/controls.json'}|set(contract['instruction_inputs'])|set(contract['dependencies'])
    require(required<=set(files),'submission missing required binding')
    for name,h in files.items(): require(digest(source(name))==h,'source mismatch: '+name)
    for name,h in {**contract['instruction_inputs'],**contract['dependencies']}.items(): require(digest(source(name))==h,'frozen dependency changed')
    return s,payload(loop,direction,source(prefix+'/output/results.json').parent)
def gate(loop):
    require(loop in LOOPS,'unknown loop')
    g=read(source(f'{ROUND}/advisor/{loop}-gate.json'))
    require(g.get('loop')==loop and g.get('reviewed') is True,'unreviewed gate')
    require(g.get('verdict') in ('accepted_within_scope','limited','insufficient'),'invalid verdict')
    for name,h in g['files'].items(): require(digest(source(name))==h,'gate binding changed: '+name)
    for d in ('forward','reverse'):
        s,p=submission(loop,d)
        require(s==g['submissions'][d] and p==g['payloads'][d],'reviewed evidence changed')
    require(g.get('review_mode')=='independent model-agent review; not external peer review','false attribution')
    require(f'{ROUND}/skeptic/{loop}-review.md' in g['files'],'missing skeptical report')
    return g
def replay(loop,out,optimized=False):
    g=gate(loop)
    for d in ('forward','reverse'):
        target=out/loop/d; target.parent.mkdir(parents=True,exist_ok=True)
        cmd=[sys.executable,'-B']+(['-O'] if optimized else [])+[str(source(f'{ROUND}/{d}/{loop}/check.py')),'--output',str(target)]
        run=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
        (target.parent/(d+'.log')).write_text(run.stdout+run.stderr)
        require(run.returncode==0,'producer failed: '+loop+'/'+d)
        require({p.name for p in target.iterdir()}=={'results.json','controls.json'},'unexpected outputs')
        payload(loop,d,target,g['payloads'][d])
        for name in ('results.json','controls.json'):
            require((target/name).read_bytes()==source(f'{ROUND}/{d}/{loop}/output/{name}').read_bytes(),'non-deterministic output')
    return {'loop':loop,'verdict':g['verdict'],'gate_sha256':digest(source(f'{ROUND}/advisor/{loop}-gate.json'))}
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--loops',nargs='+');p.add_argument('--optimized',action='store_true');a=p.parse_args()
    out=external_output(a.output)
    loops=a.loops or [l for l in LOOPS if (ROOT/f'{ROUND}/advisor/{l}-gate.json').exists()]
    require(loops and len(loops)==len(set(loops)),'invalid loop selection');out.mkdir(parents=True)
    rows=[replay(l,out,a.optimized) for l in loops]
    (out/'reproduction.json').write_text(json.dumps({'status':'passed','optimized':a.optimized,'loops':rows,'research_loops_added':0},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','loops':len(rows),'producer_executions':2*len(rows)}))
if __name__=='__main__': main()
