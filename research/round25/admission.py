"""Check frozen sources and replay both same-author AA producers in fresh outputs."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];R=ROOT/'research/round25'
def require(ok,m):
    if not ok:raise ValueError(m)
def source(name):
    p=ROOT/name
    require(not Path(name).is_absolute() and '..' not in Path(name).parts,'unsafe path')
    require(p.is_file() and p.resolve().is_relative_to(ROOT) and not p.is_symlink(),'missing or linked source '+name)
    return p
def hashes(d):
    require(isinstance(d,dict) and bool(d),'empty bindings')
    for name,h in d.items():require(hashlib.sha256(source(name).read_bytes()).hexdigest()==h,'changed '+name)
def metadata(g,loop):
    prefix='research/round25/'
    required={prefix+f'contracts/{loop}.json',prefix+f'contracts/{loop}-freeze.json',
      *[prefix+f'solo/{loop}/'+x for x in ['check.py','report.md','output/results.json']]}
    require(required<=g.get('sha256',{}).keys(),'missing gate binding')
    require(g['loop']==loop and g['normal_optimized_equal'] is True,'gate identity')
    require(g['verdict']==('limited' if loop=='aa1' else 'accepted_within_scope'),'verdict changed')
    require('same-author' in g['review'] and 'not independent' in g['review'],'authorship')
def gate(loop):
    require(loop in ['aa1','aa2'],'unknown loop')
    g=json.loads((R/f'advisor/{loop}-gate.json').read_text());c=json.loads((R/f'contracts/{loop}.json').read_text())
    freeze=json.loads((R/f'contracts/{loop}-freeze.json').read_text())
    required={f'research/round25/contracts/{loop}.json',*c['inherited_sources'],*[str(p.relative_to(ROOT)) for p in (R/'inputs/aa1').iterdir()]}
    require(required<=freeze['sha256'].keys(),'missing frozen input')
    hashes(freeze['sha256']);hashes(g['sha256'])
    metadata(g,loop)
    expected=json.loads((R/f'solo/{loop}/output/results.json').read_text())
    require(len(expected['controls'])>=6 and all(type(x)is bool and x for x in expected['controls'].values()),'control semantics')
    return expected
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--optimized',action='store_true');a=p.parse_args()
    out=a.output.resolve();require(not out.exists() and not out.is_relative_to(ROOT),'fresh external output required');out.mkdir(parents=True)
    for loop in ['aa1','aa2']:
        expected=gate(loop);cmd=[sys.executable,'-B']+(['-O'] if a.optimized else [])+[str(R/f'solo/{loop}/check.py'),'--output',str(out/loop)]
        run=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);(out/f'{loop}.log').write_text(run.stdout+run.stderr);require(run.returncode==0,'producer failure '+loop)
        require(json.loads((out/loop/'results.json').read_text())==expected,'fresh semantic mismatch '+loop)
        require((out/loop/'results.json').read_bytes()==(R/f'solo/{loop}/output/results.json').read_bytes(),'byte mismatch '+loop)
    (out/'receipt.json').write_text(json.dumps({'status':'passed','optimized':a.optimized,'new_research_loops':0,'replayed':['aa1','aa2'],'authorship':'single agent, correlated checks'},indent=2)+'\n')
    print(json.dumps({'status':'passed','producer_executions':2,'optimized':a.optimized}))
if __name__=='__main__':main()
