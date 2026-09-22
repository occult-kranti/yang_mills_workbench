#!/usr/bin/env python3
"""Replay admitted Round29 evidence from its actual source tree."""
import argparse, hashlib, json, pathlib, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
R=ROOT/'research/round29'
sys.path.insert(0,str(ROOT))
from research.round29.release.admission import validate_loop
def require(ok, why):
    if not ok: raise ValueError(why)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(root=ROOT, complete=False):
    r=root/'research/round29'
    f=json.loads((r/'advisor/findings.json').read_text())
    require(f['completed']==len(f['loops']), 'Count mismatch')
    require(len(f['loops'])==10 if complete else 0<len(f['loops'])<=10,'Loop boundary')
    seen=set()
    for i,row in enumerate(f['loops'],1):
        loop=row['id'].lower(); require(loop not in seen,'Duplicate loop');seen.add(loop)
        g=json.loads((r/f'advisor/{loop}-gate.json').read_text())
        require(g['sequence']==i and row['sequence']==i,'Sequence mismatch')
        require(g['accepted']==row['accepted'] and g['limitations']==row['limitations'],'Presentation/gate mismatch')
        require(g['verdict'] in ('accepted_within_scope','limited','insufficient'),'Unrecognized verdict')
        require(g['accepted'] and g['limitations'],'Scope missing')
        required={f'research/round29/contracts/{loop}.json',f'research/round29/skeptic/{loop}.md',f'research/round29/skeptic/{loop}.json'}
        for side in ('forward','reverse'):
            required|={f'research/round29/{side}/{loop}/{p}' for p in ('check.py','report.md','freeze.json','output/results.json')}
        require(required<=g['bindings'].keys(),'Required evidence omitted')
        for rel,sha in g['bindings'].items():
            p=root/rel
            require(not p.is_symlink() and p.resolve().is_relative_to(root.resolve()),'Escaping evidence')
            require(p.is_file() and digest(p)==sha,f'Changed evidence: {rel}')
        review=json.loads((r/f'skeptic/{loop}.json').read_text())
        require(review.get('blocking_issues')==[],'Blocking or missing skeptical verdict')
        validate_loop(root,loop,gate=g,row=row,require_spec=True)
    return f
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=pathlib.Path);ap.add_argument('--complete',action='store_true');ap.add_argument('--validate-only',action='store_true');ap.add_argument('--optimized',action='store_true');a=ap.parse_args()
    f=verify(complete=a.complete)
    if a.validate_only: print(json.dumps({'validated':len(f['loops'])}));return
    require(a.output is not None and a.output.is_absolute() and not a.output.exists(),'Use fresh absolute output')
    require(not a.output.resolve().is_relative_to(ROOT.resolve()),'Replay output must be outside checkout')
    a.output.mkdir(parents=True);runs=[]
    for row in f['loops']:
        for side in ('forward','reverse'):
            p=R/side/row['id'].lower();out=a.output/side/row['id'].lower()
            cmd=[sys.executable,'-B']+(['-O'] if a.optimized else [])+[str(p/'check.py'),'--output',str(out)]
            result=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True)
            require(result.returncode==0,f'{side}/{row["id"]}: {result.stderr}')
            expected={str(x.relative_to(p/'output')):digest(x) for x in (p/'output').rglob('*') if x.is_file()}
            actual={str(x.relative_to(out)):digest(x) for x in out.rglob('*') if x.is_file()}
            require(actual==expected,f'Replay output inventory or bytes differ: {side}/{row["id"]}')
            runs.append({'id':row['id'],'direction':side,'results_sha256':digest(out/'results.json'),'output_sha256':actual})
    (a.output/'receipt.json').write_text(json.dumps({'loops':len(f['loops']),'runs':runs,'optimized':a.optimized},indent=2)+'\n')
    print(json.dumps({'loops':len(f['loops']),'producer_replays':len(runs),'status':'passed'}))
if __name__=='__main__':main()
