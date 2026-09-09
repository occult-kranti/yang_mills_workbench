#!/usr/bin/env python3
"""Source-bound two-front planning. Arithmetic replay precedes admission.

The search locates implications through independently reviewed conventional
lemmas. It does not prove the lemmas' mathematical text or the Clay problem.
"""
from pathlib import Path
import copy
import hashlib
import json
import re
import sys
import types
from fractions import Fraction as F

HERE=Path(__file__).resolve().parent
EXPECTED={
    'advisor/advisor.md','advisor/theorem_inventory.json','advisor/inference_rules.json',
    'solver/drive_bound.py','solver/dependencies.json','solver/vendor/two_plaquette.py',
    'solver/vendor/round11_run_study.py','solver/output/analytic_certificates.json',
    'solver/exact_stepper.py','solver/output/exact_step_certificate.json',
    'volume/volume-bridge.md','closure/closure-audit.md',
    'proof_routes.py','proof_search.py'
}


def checked_inputs():
    manifest=json.loads((HERE/'proof_manifest.json').read_text())
    if set(manifest)!={'sha256'} or not isinstance(manifest['sha256'],dict) or set(manifest['sha256'])!=EXPECTED:
        raise ValueError('Complete exact manifest set required')
    frozen={}
    for rel,digest in manifest['sha256'].items():
        if not isinstance(digest,str) or not re.fullmatch('[0-9a-f]{64}',digest):
            raise ValueError('Invalid digest')
        p=HERE
        for part in Path(rel).parts:
            p=p/part
            if p.is_symlink():raise ValueError('Symlink input rejected')
        if not p.resolve().is_relative_to(HERE):raise ValueError('Input escaped research root')
        raw=p.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('Stale source or artifact: '+rel)
        frozen[rel]=raw
    return manifest,frozen


def load_frozen(name,rel,frozen):
    module=types.ModuleType(name);module.__file__=str(HERE/rel)
    sys.modules[name]=module
    exec(compile(frozen[rel],module.__file__,'exec'),module.__dict__)
    return module


def replay_arithmetic(frozen):
    # Both the dependency declaration and the bytes it declares are frozen.
    deps=json.loads(frozen['solver/dependencies.json'])
    if set(deps)!={'expected_dependencies'}:raise ValueError('Dependency schema')
    records=deps['expected_dependencies']
    wanted={'vendor/two_plaquette.py','vendor/round11_run_study.py'}
    if not isinstance(records,list) or len(records)!=len(wanted) or {d.get('path') for d in records}!=wanted:
        raise ValueError('Dependency set mismatch')
    for d in records:
        if d['sha256']!=hashlib.sha256(frozen['solver/'+d['path']]).hexdigest():raise ValueError('Dependency bytes mismatch')
    db=load_frozen('drive_bound','solver/drive_bound.py',frozen)
    db.expected_dependencies=lambda:copy.deepcopy(records)
    db.source_hashes=lambda:{**{d['path']:d['sha256'] for d in records},
        'dependencies.json':hashlib.sha256(frozen['solver/dependencies.json']).hexdigest(),
        'drive_bound.py':hashlib.sha256(frozen['solver/drive_bound.py']).hexdigest()}
    collection=json.loads(frozen['solver/output/analytic_certificates.json'])
    if set(collection)!={'contract','scope','cases'} or collection['contract']!=db.CONTRACT or collection['scope']!=db.SCOPE:
        raise ValueError('Certificate collection scope/schema mismatch')
    cases=collection['cases']
    expected={(name,d) for name in ('original','reduced','short','slow') for d in (3,4)}
    protocols={name:{'kind':'cosine_ramp','duration':T,'lambda1_scale':a,'lambda2_scale':b}
               for name,T,a,b in [('original','2','1','3/2'),('reduced','2','1/10','3/20'),
                                  ('short','1/5','1','3/2'),('slow','4','1/20','3/40')]}
    if not isinstance(cases,list) or len(cases)!=8:raise ValueError('Eight declared cases required')
    pairs=[]
    for item in cases:
        if set(item)!={'case','certificate'}:raise ValueError('Case schema')
        c=item['certificate'];db.verify_certificate(c);pairs.append((item['case'],c['degree']))
        p=protocols.get(item['case'])
        if p is None or c['protocol']!=p or c['time']!=p['duration'] or c['alpha']!='1' or c['rho']!='1' or c['initial_degree']!=0:
            raise ValueError('Named study case does not match its declared physical fixture')
    if set(pairs)!=expected or len(set(pairs))!=8:raise ValueError('Missing or duplicate declared case')
    reduced=next(x['certificate'] for x in cases if x['case']=='reduced' and x['certificate']['degree']==4)
    if reduced['protocol']!={'kind':'cosine_ramp','duration':'2','lambda1_scale':'1/10','lambda2_scale':'3/20'} or reduced['state_error_upper']!='1/3840':
        raise ValueError('Selected reduced drive mismatch')
    # Freeze imports used by the separate exact-arithmetic evolution checker.
    vendor=types.ModuleType('vendor');vendor.__path__=[];sys.modules['vendor']=vendor
    tp=load_frozen('vendor.two_plaquette','solver/vendor/two_plaquette.py',frozen)
    vendor.two_plaquette=tp
    stepper=load_frozen('exact_stepper','solver/exact_stepper.py',frozen)
    exact=json.loads(frozen['solver/output/exact_step_certificate.json'])
    # The exact stepper's source-hash hook is sealed to the executable bytes.
    if hasattr(stepper,'hashes'):
        stepper.hashes=lambda:{**db.source_hashes(),'exact_stepper.py':hashlib.sha256(frozen['solver/exact_stepper.py']).hexdigest()}
    stepper.verify_certificate(exact)
    return {'status':'passed','analytic_case_count':8,'reduced_degree4_bound':'1/3840',
            'exact_evolution':exact,'scope':'Exact rational actions and stored-vector arithmetic; analytic lemmas are separately reviewed.'}


def make_library(frozen,exact=False):
    inventory=json.loads(frozen['advisor/theorem_inventory.json'])
    source=json.loads(frozen['advisor/inference_rules.json'])
    digest=hashlib.sha256(frozen['advisor/advisor.md']).hexdigest()
    if inventory['advisor_sha256']!=digest or source['advisor_sha256']!=digest:raise ValueError('Stale advisor inventory')
    claims={x['claim_id']:x for x in inventory['claims']}
    if len(claims)!=len(inventory['claims']):raise ValueError('Duplicate theory node')
    specs=source['rules']
    for r in specs:
        if any(k not in claims for k in [*r['premises'],r['conclusion']]):raise ValueError('Unlisted rule premise or conclusion')
        if r['source_sha256']!=digest:raise ValueError('Stale rule source')
    # Only this explicit contract set can enter as initial facts.
    seeds={'round11_physical_model','bounded_drive','initial_support','integrated_action',
           'volume_graph_contract','independent_tensor_copies_gate',
           'tilted_haar_contract','defined_point_closure_gate'}
    if exact:
        seeds.update({'exact_piecewise_fixture','exact_taylor_vector_gate',
                      'exact_segment_composition','matched_initial_error_gate'})
    if not seeds<=set(claims):raise ValueError('Missing named admission gate')
    inherited={k:{k} for k in seeds}
    # Compute transitive declared assumptions without inventing missing atoms.
    remaining=list(specs)
    while remaining:
        progressed=False
        for r in remaining[:]:
            if all(k in inherited for k in r['premises']):
                inherited[r['conclusion']]=set().union(*(inherited[k] for k in r['premises']))
                remaining.remove(r);progressed=True
        if not progressed:break
    nodes=[]
    for key,c in claims.items():
        is_open=c['status'] in ('unresolved','proposed')
        kind='declared_hypothesis' if key in seeds else ('target' if is_open and key not in inherited else 'theorem')
        # Unprovided input gates may be conditional hypotheses, never facts.
        if key not in seeds and key not in inherited and any(key in r['premises'] for r in specs):
            kind='declared_hypothesis' if c['status']=='proposed' else kind
        nodes.append(dict(id=key,statement=c['statement'],scope='R12',kind=kind,
            assumption_ids=sorted(inherited.get(key,set())-{key}),
            verification='Explicit source-bound contract or reviewed conditional derivation; unresolved gates cannot be seeded automatically.',
            source='advisor/advisor.md',version='12.1'))
    rules=[dict(id=r['rule_id'],premises=r['premises'],conclusion=r['conclusion'],cost=1,
                scope='R12',proof_ref='advisor/advisor.md; '+str(r.get('equation_or_section',[])),review_status='reviewed') for r in specs]
    return dict(nodes=nodes,rules=rules,initial_facts=sorted(seeds),goals=['factorial_representation_error'],conditional_assumptions=[],blocked_goals=[])


def execute():
    manifest,frozen=checked_inputs();arithmetic=replay_arithmetic(frozen)
    search=load_frozen('ym12_proof_search','proof_search.py',frozen)
    cosine=make_library(frozen);exact=make_library(frozen,exact=True)
    variants={}
    def add(name,base,goal,wanted='proved',without_fact=None,without_conclusion=None):
        m=copy.deepcopy(base);m['goals']=[goal]
        if without_fact:m['initial_facts'].remove(without_fact)
        if without_conclusion:m['rules']=[r for r in m['rules'] if r['conclusion']!=without_conclusion]
        variants[name]=(m,wanted)
    add('cosine_representation',cosine,'factorial_representation_error')
    add('exact_piecewise_computed_state',exact,'exact_piecewise_total_error')
    add('finite_volume_comparison',cosine,'volume_heat_comparison')
    add('vanishing_bound_is_not_gap_closure',cosine,'bound_decay_not_gap_closure')
    add('defined_point_closure_rejected',cosine,'point_closure_rejection')
    add('cosine_total_error_unavailable',cosine,'total_computed_state_error','not_derivable')
    add('without_degree_bandwidth',cosine,'factorial_representation_error','not_derivable',without_conclusion='degree_bandwidth_one')
    add('without_initial_support',cosine,'factorial_representation_error','not_derivable',without_fact='initial_support')
    add('without_absolute_action',cosine,'factorial_representation_error','not_derivable',without_fact='integrated_action')
    add('without_exact_vector_replay',exact,'exact_piecewise_total_error','not_derivable',without_fact='exact_taylor_vector_gate')
    add('four_dimensional_yang_mills',exact,'four_dimensional_yang_mills_gap','not_derivable')
    outputs={}
    for name,(library,wanted) in variants.items():
        result=search.plan(library)
        if result['status']!=wanted or wanted=='proved' and not result.get('certified_proof'):
            raise ValueError('Unexpected proof route outcome: '+name)
        outputs[name]={'library':library,'result':result}
    invalid=copy.deepcopy(cosine);invalid['initial_facts'].append('four_dimensional_yang_mills_gap')
    try:search.plan(invalid)
    except search.ContractError:pass
    else:raise ValueError('Unproved final target accepted as an axiom')
    result={'status':'passed','scope':'Finite ground-Horn bidirectional search plus separate certificate replay; no formal proof kernel or continuum result.',
            'manifest':manifest,'arithmetic':arithmetic,'routes':outputs}
    (HERE/'proof_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:{'status':v['result']['status'],'cost':v['result'].get('certified_cost')} for k,v in outputs.items()}))


if __name__=='__main__':execute()
