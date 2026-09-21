#!/usr/bin/env python3
"""Coherent mutation controls for U scope, instructions and solo disclosure."""
import argparse,copy,json,shutil,tempfile
from pathlib import Path
import admission as a

def save(p,x): p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);out=p.parse_args().output
    a.require(out.is_absolute() and not out.exists(),'fresh output required')
    original=a.ROOT;rows=[]
    for loop in ('u1','u2'):
        gate=a.gate(loop);gp=f'research/round23/advisor/{loop}-gate.json'
        def case(name, mutate):
            with tempfile.TemporaryDirectory(prefix='ym23-u-mutation-') as tmp:
                r=Path(tmp)
                for n in {*gate['files'],gp}:
                    dest=r/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original/n,dest)
                g=copy.deepcopy(gate);mutate(r,g);save(r/gp,g);a.ROOT=r
                try: a.gate(loop)
                except (ValueError,KeyError,FileNotFoundError) as exc:
                    rows.append(dict(loop=loop,case=name,rejected=True,reason=str(exc).replace(str(r),'<fixture>')))
                else: raise ValueError('coherent mutation escaped: '+name)
                finally: a.ROOT=original
        def rewrite(r,g,d,file,fn):
            b=f'research/round23/{d}/{loop}/';n=b+'output/'+file;mp=b+'output/source-manifest.json'
            v=a.read(r/n);fn(v);save(r/n,v);g['files'][n]=a.digest(r/n)
            if file=='results.json':g['expected_results'][d]=v
            m=a.read(r/mp);m['outputs'][file]=a.digest(r/n);save(r/mp,m);g['files'][mp]=a.digest(r/mp)
        for d in ('forward','reverse'):
            field='missing_face_changes_coefficient' if loop=='u1' else 'exact_positive_margin'
            case(d+'_missing_control',lambda r,g,d=d,f=field:rewrite(r,g,d,'controls.json',lambda v:v.pop(f)))
            case(d+'_integer_control',lambda r,g,d=d,f=field:rewrite(r,g,d,'controls.json',lambda v:v.update({f:1})))
            case(d+'_false_independence',lambda r,g,d=d:rewrite(r,g,d,'results.json',lambda v:v.update(independent_agent_review=True)))
            case(d+'_endpoint_scope_flip',lambda r,g,d=d:rewrite(r,g,d,'results.json',lambda v:v.update(endpoint_proved=loop!='u2')))
        case('gate_false_independence',lambda r,g:g['independence'].update(independent_agents=True))
        def instruction(r,g):
            n=f'research/round23/forward/{loop}/output/source-manifest.json';v=a.read(r/n)
            v['inputs'].pop('research/round23/methods/u-v1/newton-analysis-synthesis.md');save(r/n,v);g['files'][n]=a.digest(r/n)
        case('missing_skill_snapshot',instruction)
    a.require(len(rows)==20,'mutation coverage drift')
    out.parent.mkdir(parents=True,exist_ok=True);save(out,dict(status='passed',controls=rows,research_loops_added=0,review_mode='single-agent'))
    print(json.dumps(dict(status='passed',rejected_mutations=len(rows))))
if __name__=='__main__':main()
