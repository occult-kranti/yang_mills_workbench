#!/usr/bin/env python3
"""Execute negative admission controls in isolated source copies."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import admission as a


def save(p,x): p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output
    a.require(out.is_absolute() and not out.exists(),'fresh absolute output required')
    original=a.ROOT; gate=a.gate('t2'); rows=[]
    gate_path='research/round23/advisor/t2-gate.json'
    def case(name,mutate):
        with tempfile.TemporaryDirectory(prefix='ym23-admission-') as tmp:
            root=Path(tmp)
            for path in {*gate['files'],gate_path}:
                target=root/path; target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(original/path,target)
            g=copy.deepcopy(gate)
            mutate(root,g)
            save(root/gate_path,g)
            a.ROOT=root
            try:
                a.gate('t2')
            except (ValueError,FileNotFoundError,KeyError) as exc:
                rows.append({'case':name,'rejected':True,'reason':str(exc).replace(str(root),'<fixture>')})
            else:
                raise ValueError('mutation incorrectly admitted: '+name)
            finally:
                a.ROOT=original
    def rewrite_control(root,g,direction,field,value,remove=False):
        base='research/round23/'+direction+'/t2/'
        cp=base+'output/controls.json'; mp=base+'output/source-manifest.json'
        c=a.read(root/cp)
        if remove: c.pop(field)
        else: c[field]=value
        save(root/cp,c); g['files'][cp]=a.digest(root/cp)
        m=a.read(root/mp);m['outputs']['controls.json']=a.digest(root/cp)
        save(root/mp,m);g['files'][mp]=a.digest(root/mp)
    for direction,field in [('forward','different_grounds_enclosed'),('reverse','ground_ground_cancellation_checked')]:
        case(direction+'_missing_control_coherent',lambda root,g,d=direction,f=field:rewrite_control(root,g,d,f,None,True))
        case(direction+'_integer_control_coherent',lambda root,g,d=direction,f=field:rewrite_control(root,g,d,f,1))
    case('gate_false_independence',lambda root,g:g['independence'].update(independent_agents=True))
    def result_independence(root,g):
        rp='research/round23/forward/t2/output/results.json';mp='research/round23/forward/t2/output/source-manifest.json'
        data=a.read(root/rp);data['independent_agent_review']=True
        save(root/rp,data);g['files'][rp]=a.digest(root/rp);g['expected_results']['forward']=data
        m=a.read(root/mp);m['outputs']['results.json']=a.digest(root/rp)
        save(root/mp,m);g['files'][mp]=a.digest(root/mp)
    case('result_false_independence_coherent',result_independence)
    def missing_amendment(root,g):
        mp='research/round23/forward/t2/output/source-manifest.json'
        m=a.read(root/mp);m['inputs'].pop('research/round23/methods/t2-solo-override.md')
        save(root/mp,m);g['files'][mp]=a.digest(root/mp)
    case('missing_solo_input_coherent',missing_amendment)
    def missing_instruction(root,g):
        mp='research/round23/reverse/t2/output/source-manifest.json'
        m=a.read(root/mp);m['inputs'].pop('research/round23/methods/v2/AGENTS.md')
        save(root/mp,m);g['files'][mp]=a.digest(root/mp)
    case('missing_frozen_instruction_coherent',missing_instruction)
    case('source_bytes_drift',lambda root,g:(root/'research/round23/forward/t2/check.py').write_text('changed\n'))
    case('verdict_not_reviewed',lambda root,g:g.update(status='planned'))
    case('wrong_result_expectation',lambda root,g:g['expected_results']['forward'].update(uniform_centered_coefficient='0'))
    case('cache_dependency',lambda root,g:g['files'].update({'__pycache__/x.pyc':'0'*64}))
    for loop in ('s1','s2','t1','t2'): a.gate(loop)
    a.require(len(rows)==12,'expected mutation count')
    out.parent.mkdir(parents=True,exist_ok=True)
    save(out,{'status':'passed','controls':rows,'historical_and_current_gates_pass':True,
              'research_loops_added':0,'review_mode':'single-agent'})
    print(json.dumps({'status':'passed','rejected_mutations':len(rows)}))


if __name__=='__main__': main()
