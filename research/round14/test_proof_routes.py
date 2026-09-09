#!/usr/bin/env python3
"""Material route, evidence-binding and failure tests; valid under python -O."""
import argparse
import copy
from itertools import combinations
import json
from pathlib import Path
import proof_routes as p

def require(ok,message):
    if not ok:raise ValueError(message)
def run(output):
    checks=[]
    def check(name,fn):fn();checks.append({'name':name,'passed':True})
    def reject(fn):
        try:fn()
        except (ValueError,KeyError,TypeError):return
        raise ValueError('Invalid input accepted')
    f=p.snapshot();a=p.replay(f);core=p.module('ym14_test_core',f['proof_search.py'],p.HERE/'proof_search.py')
    check('Pinned source and independent exact evidence replay',lambda:require(a['status']=='passed','replay'))
    def counterfeit():
        fake={n:b'' for n in p.INPUTS};record={'status':'passed','frozen_sha256':p.fingerprint(fake),'gates':sorted(p.GATES)}
        reject(lambda:p.library(fake,record))
    check('Fabricated pass record with matching empty bytes rejected',counterfeit)
    def changed_rules():
        original=p.RULES
        try:
            p.RULES=original+(('forged',('measure',),'yang_mills_gap'),)
            reject(lambda:p.library(f,a,goal='yang_mills_gap'))
        finally:p.RULES=original
    check('Post-replay in-memory rule injection rejected',changed_rules)
    for filename in sorted(p.INPUTS):
        def mutation(filename=filename):
            changed=dict(f);changed[filename]+=b'\n'
            reject(lambda:p.library(changed,a))
        check('Post-replay byte mutation rejected: '+filename,mutation)
    check('Missing frozen input rejected',lambda:reject(lambda:p.library({k:v for k,v in f.items() if k!='central-certificate.json'},a)))
    check('Nonbytes mutable input rejected',lambda:reject(lambda:p.library({**f,'central-certificate.json':bytearray(f['central-certificate.json'])},a)))
    for name in ['central_positive','matched_generator','uniform_physical_decay','yang_mills_gap']:
        check('Unsupported premise cannot be seeded: '+name,lambda name=name:reject(lambda:p.library(f,a,hypotheses=list(p.HYPOTHESES)+[name])))
    check('Duplicate premise rejected',lambda:reject(lambda:p.library(f,a,hypotheses=['measure','measure'])))
    check('Incomplete gate replay rejected',lambda:reject(lambda:p.library(f,{**a,'gates':[]})))
    check('Unknown target rejected',lambda:reject(lambda:p.library(f,a,goal='unknown')))
    seed_ids=sorted(p.HYPOTHESES|p.GATES)
    def all_subsets():
        comparisons=0
        for count in range(len(seed_ids)+1):
            for selected in combinations(seed_ids,count):
                selected=set(selected);lib=p.library(f,a,hypotheses=selected&p.HYPOTHESES,gates=selected&p.GATES)
                known=set(selected);changed=True
                while changed:
                    old=set(known)
                    for _,premises,conclusion in p.RULES:
                        if set(premises)<=known:known.add(conclusion)
                    changed=known!=old
                expected='proved' if 'central_positive' in known else 'not_derivable'
                result=core.plan(lib,max_states=10000,max_backward_states=10000)
                require(result['status']==expected,'Subset mismatch: '+str(selected))
                if expected=='proved':
                    ids=[s['rule_id'] for s in result['certified_proof']['steps']]
                    require(p.ordered_replay(lib,ids)['cost']==result['certified_cost'],'cost')
                    require(result['first_meeting_candidate']['passed'],'actual meeting')
                comparisons+=1
        require(comparisons==128,'complete subset enumeration')
    check('All128 premise subsets match separate exhaustive forward closure',all_subsets)
    lib=p.library(f,a)
    check('Premature goal rule rejected by separate ordered replay',lambda:reject(lambda:p.ordered_replay(lib,['r10'])))
    check('Missing evidence step rejected by separate ordered replay',lambda:reject(lambda:p.ordered_replay(lib,['r01','r02','r03','r04','r05','r06','r07','r09','r10'])))
    check('Unknown rule rejected by separate ordered replay',lambda:reject(lambda:p.ordered_replay(lib,['forged'])))
    result={'status':'passed','count':len(checks),'checks':checks,'adapter_sha256':p.digest(f['proof_routes.py']),
            'scope':'Producer adapter checks with independent closure algorithm and separate ordered replay; no formal mathematical kernel.'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','count':len(checks)}));return result
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=p.HERE/'proof_adapter_tests.json');args=parser.parse_args();run(args.output)
