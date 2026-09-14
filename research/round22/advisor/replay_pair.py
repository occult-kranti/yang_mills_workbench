#!/usr/bin/env python3
"""Advisor's fresh pre-admission replay; verdict and proof review remain separate."""
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from admission import ROOT,digest,read,require,source,unlinked


def main():
    p=argparse.ArgumentParser();p.add_argument('--loop',required=True)
    p.add_argument('--forward-hash',required=True);p.add_argument('--reverse-hash',required=True)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    require(not args.output.exists(),'summary must be new')
    contract_name=f'research/round22/contracts/{args.loop}.json';contract=read(source(contract_name))
    rows=[]
    for direction,wanted in [('forward',args.forward_hash),('reverse',args.reverse_hash)]:
        prefix=f'research/round22/{direction}/{args.loop}/'
        submission=source(prefix+'submission.json');require(digest(submission)==wanted,'submission drift')
        for name,h in read(submission)['files'].items():require(digest(source(name))==h,'submitted source drift')
        manifest=read(source(prefix+'output/source-manifest.json'))
        required={contract_name,prefix+'check.py',prefix+'report.md',*contract['instruction_inputs'],*contract['dependencies']}
        require(required<=manifest['inputs'].keys(),'incomplete source closure')
        for name,h in manifest['inputs'].items():require(digest(source(name))==h,'input drift')
        for name,h in contract['dependencies'].items():require(manifest['inputs'][name]==h,'dependency drift')
        expected={**manifest['outputs'],'source-manifest.json':digest(source(prefix+'output/source-manifest.json'))}
        for optimized in [False,True]:
            with tempfile.TemporaryDirectory(prefix='ym22-advisor-replay-') as folder:
                out=Path(folder)/'out';command=[sys.executable,'-B']+(['-O'] if optimized else [])
                command += [str(source(prefix+'check.py')),'--output',str(out)]
                run=subprocess.run(command,cwd=ROOT,text=True,capture_output=True)
                require(run.returncode==0,run.stdout+run.stderr)
                actual={str(p.relative_to(out)):digest(unlinked(p)) for p in out.rglob('*') if p.is_file()}
                require(actual==expected,'fresh inventory or hash drift')
                for name in expected:require((out/name).read_bytes()==source(prefix+'output/'+name).read_bytes(),'byte drift')
                for name in ['results.json','controls.json']:
                    result=read(out/name)
                    require(result.get('loop')==args.loop and result.get('direction')==direction and result.get('passed') is True,'invalid success identity')
                rows.append({'direction':direction,'mode':'optimized' if optimized else 'normal','outputs':actual,'byte_identical':True})
    result={'status':'passed','loop':args.loop,'research_loops_added':0,'executions':rows,
            'driver_sha256':digest(Path(__file__).resolve()),'scope':'Exact replay and source closure only; advisor proof review is recorded separately.'}
    import json
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','loop':args.loop,'executions':4}))


if __name__=='__main__':main()
