#!/usr/bin/env python3
"""Replay admitted Round21 scientific sources and independent pair comparisons.

This does not create gates or turn a limited target into a solved target.
Use a fresh output directory outside this study.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def unlinked(path):
    """Inspect lexical paths before resolve() can hide linked parents."""
    for component in (path,*path.parents):
        if component.is_symlink():raise ValueError('linked path component: '+str(component))
    return path
def local(name):
    if type(name) is not str or not name:raise ValueError('invalid scientific inventory name')
    q=Path(name)
    if q.is_absolute() or '..' in q.parts or '__pycache__' in q.parts or q.suffix=='.pyc':
        raise ValueError('nonportable scientific inventory path: '+name)
    p=unlinked(ROOT/q)
    if not p.is_file():raise ValueError('missing scientific file: '+name)
    return p
def gate(loop):
    if type(loop) is not str or re.fullmatch('[a-z][12]',loop) is None:raise ValueError('invalid loop identifier')
    p=local(f'research/round21/advisor/{loop}-gate.json');d=json.loads(p.read_text())
    if d.get('loop')!=loop or d.get('status') not in ('accepted','limited'):raise ValueError('unadmitted loop '+loop)
    required={f'research/round21/contracts/{loop}.json',f'research/round21/advisor/compare-{loop}.py',
              f'research/round21/advisor/{loop}-comparison.json'}
    required.update(f'research/round21/{direction}/{loop}/{file}' for direction in ('forward','reverse')
                    for file in ('check.py','report.md','output/results.json','output/source-manifest.json'))
    files=d.get('files')
    if not isinstance(files,dict) or not required<=files.keys():raise ValueError('incomplete scientific inventory '+loop)
    for name,want in files.items():
        if type(want) is not str or re.fullmatch('[0-9a-f]{64}',want) is None or digest(local(name))!=want:raise ValueError('changed admitted source '+name)
    for direction in ('forward','reverse'):
        prefix=f'research/round21/{direction}/{loop}/'
        manifest=json.loads(local(prefix+'output/source-manifest.json').read_text())
        inputs=manifest.get('inputs');outputs=manifest.get('outputs')
        if not isinstance(inputs,dict) or not inputs or not isinstance(outputs,dict) or not outputs:
            raise ValueError('missing source/output closure '+loop+'/'+direction)
        if not {prefix+'check.py',prefix+'report.md',f'research/round21/contracts/{loop}.json'}<=inputs.keys():
            raise ValueError('incomplete producer input closure '+loop+'/'+direction)
        for name,want in inputs.items():
            if name not in files or files[name]!=want:raise ValueError('unbound declared scientific input '+name)
        if 'results.json' not in outputs:raise ValueError('results absent from output closure')
        for name,want in outputs.items():
            if type(name) is not str or Path(name).is_absolute() or '..' in Path(name).parts:
                raise ValueError('invalid declared output path')
            full=prefix+'output/'+name
            if full not in files or files[full]!=want:raise ValueError('unbound declared scientific output '+full)
    contract=json.loads(local(f'research/round21/contracts/{loop}.json').read_text())
    dep=contract.get('depends_on')
    if dep and digest(local(dep['gate']))!=dep['sha256']:raise ValueError('changed feedback dependency '+loop)
    return d
def fresh_outputs(loop,direction,target,g):
    prefix=f'research/round21/{direction}/{loop}/output/'
    expected={name[len(prefix):]:want for name,want in g['files'].items() if name.startswith(prefix)}
    actual={str(p.relative_to(target)) for p in target.rglob('*') if p.is_file()}
    if not expected or set(expected)!=actual:raise ValueError('fresh scientific output inventory drift '+loop+'/'+direction)
    for name,want in expected.items():
        p=unlinked(target/name)
        if digest(p)!=want or p.read_bytes()!=local(prefix+name).read_bytes():
            raise ValueError('scientific output drift '+loop+'/'+direction+'/'+name)
    d=json.loads((target/'results.json').read_text())
    if d.get('loop')!=loop or d.get('direction')!=direction:raise ValueError('fresh result identity drift')
    if 'passed' in d and type(d['passed']) is not bool:raise ValueError('fresh passed status must be Boolean')
    if 'status' in d and type(d['status']) is not str:raise ValueError('fresh status must be text')
    return target/'results.json'
def fresh_comparison(loop,path,g):
    relative=f'research/round21/advisor/{loop}-comparison.json'
    if digest(unlinked(path))!=g['files'][relative] or path.read_bytes()!=local(relative).read_bytes():
        raise ValueError('fresh comparison content differs from reviewed comparison '+loop)
    d=json.loads(path.read_text())
    if d.get('loop')!=loop or d.get('status')!='accepted':raise ValueError('pair comparison rejected '+loop)
    controls=d.get('mutation_controls')
    if not isinstance(controls,list) or not controls or any(c.get('rejected') is not True for c in controls):
        raise ValueError('comparison lacks executed rejecting controls')
def run(cmd,out):
    p=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(p.stdout+p.stderr)
    if p.returncode:raise RuntimeError('execution failed; see '+str(out))
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--loops',nargs='+');p.add_argument('--optimized',action='store_true');a=p.parse_args()
    out=unlinked(a.output.absolute()).resolve()
    if out.exists() or HERE==out or HERE in out.parents:raise ValueError('choose a fresh external replay directory')
    loops=a.loops or json.loads((HERE/'execution.json').read_text())['completed_loops']
    if not loops or len(set(loops))!=len(loops):raise ValueError('empty or duplicate loop selection')
    gates={n:gate(n) for n in loops}
    gate_hashes={n:digest(local(f'research/round21/advisor/{n}-gate.json')) for n in loops}
    out.mkdir(parents=True);rows=[]
    flags=['-B']+(['-O'] if a.optimized else [])
    for loop,g in gates.items():
        for direction in ('forward','reverse'):
            source=local(f'research/round21/{direction}/{loop}/check.py')
            target=out/loop/direction
            run([sys.executable,*flags,str(source),'--output',str(target)],out/loop/f'{direction}.log')
            actual=fresh_outputs(loop,direction,target,g)
            rows.append({'loop':loop,'direction':direction,'source_sha256':digest(source),'result_sha256':digest(actual)})
        compare=local(f'research/round21/advisor/compare-{loop}.py')
        comparison=out/loop/'comparison.json'
        run([sys.executable,*flags,str(compare),'--forward',str(out/loop/'forward/results.json'),'--reverse',str(out/loop/'reverse/results.json'),'--output',str(comparison)],out/loop/'comparison.log')
        fresh_comparison(loop,comparison,g)
        gate(loop)
        if digest(local(f'research/round21/advisor/{loop}-gate.json'))!=gate_hashes[loop]:
            raise ValueError('reviewed gate changed during replay '+loop)
    result={'status':'passed','loops':loops,'executions':rows,'pair_comparisons':len(loops),'optimized':a.optimized,'counting':'Repeated executions add zero research loops. Target verdicts remain in the gates.'}
    (out/'reproduction.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','loops':len(loops),'executions':len(rows),'comparisons':len(loops)}))
if __name__=='__main__':main()
