#!/usr/bin/env python3
"""Replay exact inputs, then search reviewed two-loop implications in two directions."""
from pathlib import Path
from fractions import Fraction as F
import copy
import hashlib
import json
import re
import sys
import types

HERE=Path(__file__).resolve().parent
EXPECTED={'advisor/advisor.md','solver/two_plaquette.py','solver/output/stationary_certificates.json',
          'solver/output/continuous_rectangle_certificate.json','proof_routes.py','proof_search.py'}

def checked_inputs():
    manifest=json.loads((HERE/'proof_manifest.json').read_text())
    hashes=manifest.get('sha256') if isinstance(manifest,dict) else None
    if not isinstance(hashes,dict) or set(hashes)!=EXPECTED:
        raise ValueError('Missing or unexpected proof-manifest inputs')
    frozen={}
    for rel,digest in hashes.items():
        if not isinstance(digest,str) or re.fullmatch(r'[0-9a-f]{64}',digest) is None:
            raise ValueError('Invalid proof-input digest')
        path=HERE/rel
        if not path.resolve().is_relative_to(HERE) or any(p.is_symlink() for p in [path,*path.parents] if p!=HERE and p.is_relative_to(HERE)):
            raise ValueError('Symlink or escaped proof input')
        raw=path.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('Changed reviewed proof input: '+rel)
        frozen[rel]=raw
    return manifest,frozen

def load_frozen(name,rel,frozen):
    module=types.ModuleType(name);module.__file__=str(HERE/rel);sys.modules[name]=module
    exec(compile(frozen[rel],module.__file__,'exec'),module.__dict__)
    return module

def replay_arithmetic(frozen):
    module=load_frozen('ym11_frozen_certificate','solver/two_plaquette.py',frozen)
    module.source_digest=lambda:hashlib.sha256(frozen['solver/two_plaquette.py']).hexdigest()
    collection=json.loads(frozen['solver/output/stationary_certificates.json'])
    if not isinstance(collection,dict) or set(collection)!={'contract','scope','certificates'} or collection['contract']!=module.CONTRACT or collection['scope']!=module.SCOPE:
        raise ValueError('Invalid stationary collection contract')
    certificates=collection['certificates']
    cover=json.loads(frozen['solver/output/continuous_rectangle_certificate.json'])
    if not isinstance(certificates,list) or not certificates:raise ValueError('Empty point evidence')
    for certificate in certificates:
        if module.verify_certificate(certificate) is not True:raise ValueError('Point certificate did not replay')
    if module.verify_continuous_rectangle(cover) is not True:raise ValueError('Rectangle did not replay')
    # Reconstruct the declared domain and margin independently of dictionary equality.
    expected={(F(i),F(j)) for i in range(3) for j in range(3)}
    seen=set();margins=[]
    if cover['domain']!=[['0','2'],['0','2']] or F(cover['alpha'])!=1 or F(cover['rho'])!=1 or F(cover['gap_lipschitz_l1'])!=2:
        raise ValueError('Wrong continuous physical parameter contract')
    for cell in cover['cells']:
        center=tuple(map(F,cell['center']))
        if center in seen or center not in expected:raise ValueError('Duplicate or missing center')
        seen.add(center);point=cell['point_certificate']
        if (F(point['lambda1']),F(point['lambda2']))!=center or F(point['alpha'])!=1 or F(point['rho'])!=1:
            raise ValueError('Mismatched point parameter')
        for axis,value in zip(('x_interval','y_interval'),center):
            if list(map(F,cell[axis]))!=[max(F(0),value-F(1,2)),min(F(2),value+F(1,2))]:
                raise ValueError('Interval coverage changed')
        margin=F(point['gap'][0])-2
        if F(cell['radius_l1'])!=1 or F(cell['margin'])!=margin:raise ValueError('Wrong continuity budget')
        margins.append(margin)
    if seen!=expected or min(margins)!=F(cover['gap_lower']) or min(margins)<F(24,25):
        raise ValueError('Incomplete coverage or insufficient claimed lower bound')
    if cover['positive'] is not True or cover['status']!='certified-positive':raise ValueError('Invalid semantic status')
    return {'status':'exact arithmetic replayed under stated analytic theorems','point_certificates':len(certificates),'centers':9,
            'exact_rectangle_lower':str(min(margins)),'conservative_lower':'24/25','scope':cover['scope']}

def make_library():
    assumptions={
      'C_graph':'Seven-link six-distinct-vertex open two-square SU(2) graph, specified paths and normalized product Haar.',
      'C_gauss':'Impose independent SU(2) Gauss invariance at each of the six vertices.',
      'C_coefficients':'Alpha>0, rho=1, nonnegative finite magnetic coefficients; kappa_i=lambda_i/alpha.',
      'C_exact_points':'All source-bound exact generalized matrix and tail certificates replayed successfully.',
      'C_exact_cover':'Nine exact source-bound certificates cover the complete closed rectangle [0,2]^2 with the declared margins.'}
    statements={
      'C_loop':'Tree reduction leaves two loop holonomies modulo simultaneous conjugation.',
      'C_coordinates':'The traces x,y,z classify the physical quotient and satisfy the exact Gram domain.',
      'C_measure':'The Haar pushforward is the normalized constant density 2/pi^2 on the quotient body.',
      'C_kinetic':'The seven-link electric operator includes the correctly signed shared-link derivative.',
      'C_domain':'The physical operator domain is inherited from the compact-group invariant sector.',
      'C_compact':'Positive electric coefficient and bounded potential yield a self-adjoint compact-resolvent Hamiltonian.',
      'C_polynomials':'Invariant coordinate polynomials are dense and their finite-degree spaces reduce the free kinetic operator.',
      'C_free':'The complete free spectrum and shell minima are given by the explicit degree eigenvalues.',
      'C_potential':'The compressed magnetic potential is nonnegative and bounded by twice the coefficient sum.',
      'C_tail':'The omitted-degree kinetic minimum supplies a proved infinite-dimensional compressed tail threshold.',
      'C_comparison':'Exact moment matrices and the Young/completion comparison give lower and upper spectral blocks.',
      'C_minmax':'The first two infinite-operator levels are enclosed with the required min-max ordering.',
      'C_points':'Opposite individual-energy endpoints give valid pointwise interacting gap intervals.',
      'C_lipschitz':'The dimensionless gap is 2-Lipschitz in the l1 distance of the two magnetic coefficients.',
      'C_cover':'The fixed 3-by-3 clipped cells cover every real point of the closed rectangle.',
      'C_rectangle':'The full two-loop Hilbert-space gap is at least24/25 on [0,2]^2, at alpha=rho=1.',
      'C_scaled':'Delta>=0.96alpha for rho=1,alpha>0,0<=lambda_i/alpha<=2.',
      'C_heat':'The commuting product heat evolution and shared-link averaging have explicit positive kernel envelopes.',
      'C_ground':'Feynman–Kac and kernel envelopes control the strictly positive ground-state ratio.',
      'C_poincare':'The free Poincare gap and ground-state transform give a quantitative weighted gap bound.',
      'C_all_finite':'Delta>=(243/625)alpha exp[-16(lambda1+lambda2)/(3alpha)] for the fixed graph and rho=1.'}
    rulespec=[
      (['C_graph','C_gauss'],'C_loop'),(['C_loop'],'C_coordinates'),(['C_coordinates'],'C_measure'),
      (['C_graph','C_loop','C_coordinates'],'C_kinetic'),(['C_loop','C_measure','C_kinetic'],'C_domain'),
      (['C_domain','C_coefficients'],'C_compact'),(['C_coordinates','C_measure','C_kinetic'],'C_polynomials'),
      (['C_polynomials'],'C_free'),(['C_coordinates','C_coefficients'],'C_potential'),
      (['C_free','C_potential','C_coefficients'],'C_tail'),(['C_tail','C_exact_points'],'C_comparison'),
      (['C_comparison','C_compact'],'C_minmax'),(['C_minmax','C_exact_points'],'C_points'),
      (['C_compact','C_coefficients','C_coordinates'],'C_lipschitz'),(['C_exact_cover'],'C_cover'),
      (['C_points','C_lipschitz','C_cover'],'C_rectangle'),(['C_rectangle','C_coefficients'],'C_scaled'),
      (['C_kinetic','C_measure','C_domain'],'C_heat'),(['C_heat','C_potential','C_compact'],'C_ground'),
      (['C_ground','C_free'],'C_poincare'),(['C_poincare','C_coefficients'],'C_all_finite')]
    inherited={x:{x} for x in assumptions}
    for premises,conclusion in rulespec:inherited[conclusion]=set().union(*(inherited[p] for p in premises))
    nodes=[]
    for key,statement in assumptions.items():
        exact=key in ('C_exact_points','C_exact_cover')
        nodes.append(dict(id=key,statement=statement,scope='C',kind='theorem' if exact else 'declared_hypothesis',assumption_ids=[],verification='exact arithmetic replay before admission' if exact else 'explicit physical contract',source='solver/output/continuous_rectangle_certificate.json' if exact else 'advisor/advisor.md',version='11.1'))
    for key,statement in statements.items():nodes.append(dict(id=key,statement=statement,scope='C',kind='theorem',assumption_ids=sorted(inherited[key]),verification='independently reviewed conventional derivation; no formal proof kernel',source='advisor/advisor.md',version='11.1'))
    nodes.append(dict(id='C_millennium',statement='Nontrivial 4D continuum quantum Yang–Mills and a positive physical mass gap.',scope='C',kind='target',assumption_ids=[],verification='open; no admitted proof',source='advisor/advisor.md',version='11.1'))
    rules=[dict(id=f'C_rule_{i+1}',premises=p,conclusion=c,cost=1,scope='C',proof_ref='advisor/advisor.md',review_status='reviewed') for i,(p,c) in enumerate(rulespec)]
    return dict(nodes=nodes,rules=rules,initial_facts=list(assumptions),goals=['C_scaled'],conditional_assumptions=[],blocked_goals=[])

def execute():
    manifest,frozen=checked_inputs();arithmetic=replay_arithmetic(frozen);base=make_library()
    search=load_frozen('ym11_frozen_proof_search','proof_search.py',frozen)
    variants={'certified_rectangle':base}
    heat=copy.deepcopy(base);heat['goals']=['C_all_finite'];variants['analytic_all_finite']=heat
    for label,atom in [('without_gauss','C_gauss'),('without_exact_points','C_exact_points'),('without_exact_cover','C_exact_cover')]:
        m=copy.deepcopy(base);m['initial_facts'].remove(atom);variants[label]=m
    for label,atom in [('without_shared_link_operator','C_kinetic'),('without_tail_theorem','C_tail')]:
        m=copy.deepcopy(base);m['rules']=[r for r in m['rules'] if r['conclusion']!=atom];variants[label]=m
    target=copy.deepcopy(base);target['goals']=['C_millennium'];variants['yang_mills_prize']=target
    outputs={}
    for name,library in variants.items():
        result=search.plan(library);wanted='proved' if name in ('certified_rectangle','analytic_all_finite') else 'not_derivable'
        if result['status']!=wanted or wanted=='proved' and not result.get('certified_proof'):
            raise ValueError('Unexpected proof outcome: '+name)
        outputs[name]={'library':library,'result':result}
    invalid=copy.deepcopy(target);invalid['initial_facts'].append('C_millennium')
    try:search.plan(invalid)
    except search.ContractError:pass
    else:raise ValueError('Unproved target accepted as a starting premise')
    result={'status':'passed','scope':'Exact arithmetic plus replay of reviewed analytic implications; no formal proof kernel or continuum result.',
      'arithmetic':arithmetic,'routes':outputs,'manifest':manifest}
    (HERE/'proof_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:{'status':v['result']['status'],'cost':v['result'].get('certified_cost')} for k,v in outputs.items()}))
if __name__=='__main__':execute()
