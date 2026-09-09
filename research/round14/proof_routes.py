#!/usr/bin/env python3
"""Source-frozen finite Horn planning; conventional rules, not a proof kernel."""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import json
import sys
import tempfile
import types
from types import MappingProxyType

HERE=Path(__file__).resolve().parent
CORE_HASH='07b5b397af86b6bf5a481b114844c6252046e8ca2b5604dac7d158091632be94'
ADAPTER_HASH=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
INPUTS={'proof_search.py','proof_routes.py','central-certificate.json',
        'forward/loop2_certificate.py','backward/verify_certificate.py','backward/oracle.py',
        'advisor/loop1_gate.json','advisor/loop2_gate.json'}
HYPOTHESES={'measure','parameters'}
GATES={'moment_gate','tail_gate','partition_gate','interval_gate','target_gate'}
OPEN={'matched_generator','uniform_physical_decay','continuum_construction','nontrivial_theory','yang_mills_gap'}
STATEMENTS={
 'measure':'Normalized SU(2)^2 Haar; finite declared Euclidean action/state and bounded trace observables.',
 'parameters':'Exactly k1=k2=1, eta=1/4 in the stated finite action.',
 'support':'Absolute values of x,y,z are at most one.',
 'defined_action':'S=k1*x+k2*y+eta*z with the declared coefficients.',
 'bounded_action':'Absolute exponent bound M=|k1|+|k2|+|eta|.',
 'moment_gate':'Independent character replay agrees with exact Haar polynomial moments.',
 'tail_gate':'Exact rational degree and geometric exponential remainder replay.',
 'partition_gate':'Jensen normalization lower bound and partition interval replay.',
 'interval_gate':'All signed numerator, product and positive-denominator interval corners replay.',
 'target_gate':'Recomputed covariance lower bound is positive and width<=1e-12.',
 'haar_functional':'Exact normalized polynomial Haar functional under declared measure.',
 'rigorous_tail':'Uniform remainder bounds all four bounded numerator integrands.',
 'polynomial_integrals':'Exact finite Taylor polynomial integral for Z,Ax,Ay,Axy.',
 'numerator_enclosures':'Rigorous enclosures of unnormalized integrals, including Z.',
 'positive_partition':'Same partition has strictly positive rigorous denominator enclosure.',
 'covariance_enclosure':'Normalized covariance is enclosed in the exact recorded interval.',
 'central_positive':'At (1,1,1/4), finite Euclidean covariance>0 with interval width<=1e-12.',
 'matched_generator':'A physical vacuum and time generator are matched to the constructed theory.',
 'uniform_physical_decay':'A common positive physical decay threshold holds on the required dense sector.',
 'continuum_construction':'Required continuum field-theory axioms and physical units established.',
 'nontrivial_theory':'Constructed theory is nontrivial pure four-dimensional Yang-Mills.',
 'yang_mills_gap':'A nontrivial four-dimensional Yang-Mills theory with positive physical mass gap.'}
RULES=[
 ('r01',['measure'],'support'),('r02',['measure','parameters'],'defined_action'),
 ('r03',['support','defined_action'],'bounded_action'),
 ('r04',['measure','moment_gate'],'haar_functional'),
 ('r05',['bounded_action','tail_gate'],'rigorous_tail'),
 ('r06',['haar_functional','defined_action'],'polynomial_integrals'),
 ('r07',['polynomial_integrals','rigorous_tail'],'numerator_enclosures'),
 ('r08',['measure','defined_action','partition_gate'],'positive_partition'),
 ('r09',['numerator_enclosures','positive_partition','interval_gate'],'covariance_enclosure'),
 ('r10',['covariance_enclosure','target_gate'],'central_positive'),
 ('r11',['matched_generator','uniform_physical_decay','continuum_construction','nontrivial_theory'],'yang_mills_gap')]
RULES=tuple((i,tuple(p),c) for i,p,c in RULES)
RULES_SERIALIZED=json.dumps(RULES,separators=(',',':'))
STATEMENTS=MappingProxyType(STATEMENTS)
INPUTS=frozenset(INPUTS);HYPOTHESES=frozenset(HYPOTHESES);GATES=frozenset(GATES);OPEN=frozenset(OPEN)

class ContractError(ValueError): pass
def digest(b): return hashlib.sha256(b).hexdigest()
def read(root,name):
    if name not in INPUTS: raise ContractError('Unknown input')
    p=Path(root)
    for part in Path(name).parts:
        p=p/part
        if p.is_symlink(): raise ContractError('Symlink input rejected')
    if not p.is_file(): raise ContractError('Missing regular input: '+name)
    return p.read_bytes()
def fingerprint(frozen):
    if type(frozen) is not dict or set(frozen)!=INPUTS or any(type(v) is not bytes for v in frozen.values()):
        raise ContractError('Complete frozen byte snapshot required')
    return {n:digest(frozen[n]) for n in sorted(INPUTS)}
def snapshot(root=HERE):
    p=Path(root)/'proof_manifest.json'
    if p.is_symlink(): raise ContractError('Symlink manifest rejected')
    m=json.loads(p.read_bytes())
    f={n:read(root,n) for n in INPUTS}
    if type(m) is not dict or set(m)!={'sha256'} or m['sha256']!=fingerprint(f):
        raise ContractError('Manifest source bytes changed')
    if digest(f['proof_search.py'])!=CORE_HASH or digest(f['proof_routes.py'])!=ADAPTER_HASH:
        raise ContractError('Pinned core or executing adapter mismatch')
    return f
def module(name,raw,path):
    m=types.ModuleType(name);m.__file__=str(path);sys.modules[name]=m
    exec(compile(raw,str(path),'exec'),m.__dict__);return m
def replay(frozen):
    before=fingerprint(frozen)
    if digest(frozen['proof_search.py'])!=CORE_HASH or digest(frozen['proof_routes.py'])!=ADAPTER_HASH:
        raise ContractError('Pinned core or executing adapter mismatch')
    if json.dumps(RULES,separators=(',',':'))!=RULES_SERIALIZED:
        raise ContractError('In-memory rule semantics changed')
    gate=json.loads(frozen['advisor/loop2_gate.json'])
    if gate.get('status')!='accepted within declared finite-model scope':raise ContractError('Missing second-loop acceptance')
    if gate.get('reviewed_rule_ids')!=[r[0] for r in RULES]:raise ContractError('Rules lack explicit review')
    for name in ['forward/loop2_certificate.py','backward/verify_certificate.py','backward/oracle.py','central-certificate.json','proof_routes.py']:
        if gate.get('source_sha256',{}).get(name)!=digest(frozen[name]):raise ContractError('Stale reviewed input: '+name)
    c=json.loads(frozen['central-certificate.json'])
    if c.get('parameters')!={'k1':'1','k2':'1','eta':'1/4'}:raise ContractError('Wrong target parameters')
    # Materialize immutable sources for source-hashing tools. No producer mathematics is imported.
    with tempfile.TemporaryDirectory(prefix='ym14-replay-',dir=HERE) as tmp:
        tmp=Path(tmp)
        for name,raw in frozen.items():
            p=tmp/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        old_oracle=sys.modules.get('oracle')
        try:
            module('oracle',frozen['backward/oracle.py'],tmp/'backward/oracle.py')
            v=module('ym14_independent_frozen',frozen['backward/verify_certificate.py'],tmp/'backward/verify_certificate.py')
            if v.verify(c,producer_source_sha256=digest(frozen['forward/loop2_certificate.py'])) is not True:
                raise ContractError('Independent exact replay failed')
        finally:
            if old_oracle is None:sys.modules.pop('oracle',None)
            else:sys.modules['oracle']=old_oracle
    lo,hi=map(Fraction,c['enclosures']['covariance'])
    if not 0<lo<=hi or hi-lo>Fraction(1,10**12):raise ContractError('Central target failed')
    if fingerprint(frozen)!=before:raise ContractError('Evidence changed during replay')
    return {'status':'passed','frozen_sha256':before,'gates':sorted(GATES),'interval':list(map(str,(lo,hi)))}
def library(frozen,accepted,goal='central_positive',hypotheses=HYPOTHESES,gates=GATES):
    if accepted.get('status')!='passed' or accepted.get('frozen_sha256')!=fingerprint(frozen) or accepted.get('gates')!=sorted(GATES):
        raise ContractError('Fresh complete evidence replay required')
    # Records supplied by a caller are not authority. Recompute before admitting any gate.
    if accepted!=replay(frozen):raise ContractError('Evidence record differs from independent fresh replay')
    for items,allowed in [(hypotheses,HYPOTHESES),(gates,GATES)]:
        if not isinstance(items,(list,tuple,set,frozenset)) or len(items)!=len(set(items)) or not set(items)<=allowed:
            raise ContractError('Unsupported or duplicate seed')
    if goal not in STATEMENTS:raise ContractError('Unknown goal')
    atoms={goal};selected=[]
    changed=True
    while changed:
        changed=False
        for r in RULES:
            if r[2] in atoms and r not in selected:selected.append(r);atoms.update(r[1]);changed=True
    selected.sort(key=lambda r:r[0]);deps={n:({n} if n in HYPOTHESES|GATES|OPEN else set()) for n in atoms}
    for _ in range(len(atoms)):
        for _,p,c in selected:deps[c]=set().union(*(deps[x] for x in p))
    return {'nodes':[{'id':n,'statement':STATEMENTS[n],'scope':'R14-physical-continuum' if n in OPEN else 'R14-finite-Euclidean','kind':'declared_hypothesis' if n in HYPOTHESES else 'target' if n in OPEN else 'theorem',
             'assumption_ids':sorted(deps[n]-{n}),'verification':'Explicit reviewed finite-model hypotheses; exact replayed gates; no formal proof-kernel claim.',
             'source':'round14 conventional derivations and source-frozen independent arithmetic','version':'14.1'} for n in sorted(atoms)],
      'rules':[{'id':i,'premises':list(p),'conclusion':c,'cost':1,'scope':'R14-physical-continuum' if c in OPEN else 'R14-finite-Euclidean','proof_ref':'backward derivation; source-bound rule '+i,'review_status':'reviewed'} for i,p,c in selected],
      'initial_facts':sorted((set(hypotheses)|set(gates))&atoms),'goals':[goal],'conditional_assumptions':[],'blocked_goals':[]}
def ordered_replay(lib,ids):
    # Deliberately separate simple verifier from the search core.
    known=set(lib['initial_facts']);rules={r['id']:r for r in lib['rules']};cost=0
    for i in ids:
        if i not in rules or not set(rules[i]['premises'])<=known:raise ContractError('Invalid ordered proof')
        known.add(rules[i]['conclusion']);cost+=rules[i]['cost']
    if not set(lib['goals'])<=known:raise ContractError('Proof misses goal')
    return {'passed':True,'cost':cost,'steps':len(ids)}
def execute(output=None):
    f=snapshot();a=replay(f);core=module('ym14_core_frozen',f['proof_search.py'],HERE/'proof_search.py')
    cases=[('certified_positive_covariance','central_positive',HYPOTHESES,GATES,'proved'),
           ('certified_covariance_interval','covariance_enclosure',HYPOTHESES,GATES,'proved')]
    cases += [('without_'+g,'central_positive',HYPOTHESES,GATES-{g},'not_derivable') for g in sorted(GATES)]
    cases += [('without_'+h,'central_positive',HYPOTHESES-{h},GATES,'not_derivable') for h in sorted(HYPOTHESES)]
    cases += [('static_moments_do_not_supply_generator','matched_generator',HYPOTHESES,GATES,'not_derivable'),
              ('four_dimensional_yang_mills','yang_mills_gap',HYPOTHESES,GATES,'not_derivable')]
    results={}
    for name,goal,h,g,expected in cases:
        lib=library(f,a,goal,h,g);r=core.plan(lib,max_states=10000,max_backward_states=10000)
        if r['status']!=expected:raise ContractError('Unexpected route: '+name)
        if expected=='proved':
            ids=[s['rule_id'] for s in r['certified_proof']['steps']];check=ordered_replay(lib,ids)
            if check['cost']!=r['certified_cost'] or not r.get('first_meeting_candidate',{}).get('passed'):raise ContractError('Meeting/cost failed')
            r['independent_ordered_replay']=check
        results[name]={'library':lib,'result':r}
    out={'status':'passed','arithmetic':a,'routes':results,'scope':'Actual two-front finite ground-Horn search. Reviewed analysis is conventional mathematics; no formal-kernel or continuum proof.'}
    Path(output or HERE/'proof_results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':'passed','routes':len(results),'positive':sum(r['result']['status']=='proved' for r in results.values())}))
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);args=p.parse_args();execute(args.output)
