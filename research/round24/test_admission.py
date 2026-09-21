#!/usr/bin/env python3
"""Discriminating admission mutations against a temporary copy, never historical evidence."""
import argparse,copy,json,tempfile,shutil,sys
from pathlib import Path
sys.dont_write_bytecode=True
import admission as a

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    if args.output.exists(): raise ValueError('fresh output required')
    original=a.ROOT;loop='v1';g=a.gate(loop)
    names=set(g['files'])|{f'{a.ROUND}/advisor/{loop}-gate.json'}
    tests={}
    with tempfile.TemporaryDirectory(prefix='ym24-admission-') as tmp:
        root=Path(tmp)/'repo';root.mkdir()
        originals={n:(original/n).read_bytes() for n in names}
        def restore():
            for n,b in originals.items():
                t=root/n;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(b)
        def dump(n,d):(root/n).write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
        gate_path=f'{a.ROUND}/advisor/v1-gate.json'
        sub_path=f'{a.ROUND}/forward/v1/submission.json'
        def rebind():
            s=a.read(root/sub_path)
            for n in s['files']: s['files'][n]=a.digest(root/n)
            dump(sub_path,s)
            gg=a.read(root/gate_path);gg['submissions']['forward']=s
            for n in gg['files']:gg['files'][n]=a.digest(root/n)
            gg['payloads']['forward']={'results':a.read(root/f'{a.ROUND}/forward/v1/output/results.json'),'controls':a.read(root/f'{a.ROUND}/forward/v1/output/controls.json')}
            dump(gate_path,gg)
        def rejected(name,change,replay=False):
            restore();change()
            try:
                if replay:a.replay(loop,Path(tmp)/name)
                else:a.gate(loop)
            except (ValueError,KeyError):tests[name]=True
            else:raise RuntimeError('mutation admitted: '+name)
        a.ROOT=root;restore();a.gate(loop);tests['valid_pair_admitted']=True
        rejected('changed_producer_source',lambda:(root/f'{a.ROUND}/forward/v1/check.py').write_text('# invalid replacement\n'))
        def missing_snapshot():
            s=a.read(root/sub_path);n=next(iter(a.read(root/f'{a.ROUND}/contracts/v1.json')['instruction_inputs']));s['files'].pop(n);dump(sub_path,s);rebind()
        rejected('coherently_rebound_missing_snapshot',missing_snapshot)
        def bad_controls():
            n=f'{a.ROUND}/forward/v1/output/controls.json';d=a.read(root/n);d['controls']={};dump(n,d);rebind()
        rejected('coherently_rebound_missing_controls',bad_controls)
        def false_review():
            d=a.read(root/gate_path);d['review_mode']='external peer review';dump(gate_path,d)
        rejected('false_review_attribution',false_review)
        def false_results():
            n=f'{a.ROUND}/forward/v1/output/results.json';d=a.read(root/n);d['claims'].append('invented result');dump(n,d);rebind()
        rejected('coherently_rebound_output_requires_actual_replay',false_results,replay=True)
        directory=root/'regular';directory.mkdir();(directory/'value').write_text('source')
        (root/'linked').symlink_to(directory,target_is_directory=True)
        try:a.source('linked/value')
        except ValueError:tests['symlinked_source_parent_rejected']=True
        else:raise RuntimeError('symlinked source parent admitted')
        alias=Path(tmp)/'outside-alias';alias.symlink_to(root,target_is_directory=True)
        try:a.external_output(alias/'new-output')
        except ValueError:tests['output_alias_into_checkout_rejected']=True
        else:raise RuntimeError('output alias into checkout admitted')
        a.ROOT=original
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps({'status':'passed','controls':tests,'research_loops_added':0},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','admission_controls':len(tests)}))
if __name__=='__main__':main()
