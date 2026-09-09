#!/usr/bin/env python3
"""Two-front conditional Horn search with exact arithmetic prerequisites."""
from pathlib import Path
from fractions import Fraction as F
import copy
import hashlib
import importlib.util
import json
import sys
from proof_search import plan,ContractError

HERE=Path(__file__).resolve().parent

def replay_arithmetic():
    path=HERE/'solver/certified_plaquette.py'
    spec=importlib.util.spec_from_file_location('round10_certificate',path)
    module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    certs=json.loads((HERE/'solver/output/stationary_certificates.json').read_text())
    cover=json.loads((HERE/'solver/output/continuous_range_certificate.json').read_text())
    if not isinstance(certs,list) or not certs:raise RuntimeError('empty stationary evidence')
    for c in certs:
        if module.verify_certificate(c) is not True:raise RuntimeError('certificate did not replay')
    # Independent, explicit coverage reconstruction for this exact six-center claim.
    expected=[F(i) for i in (0,2,4,6,8,10)]
    if cover.get('scope')!='alpha=1; single plaquette; coupling in closed [0,10]':raise RuntimeError('range scope changed')
    if [F(x) for x in cover['centers']]!=expected:raise RuntimeError('missing or changed centers')
    if F(cover['gap_lipschitz_constant'])!=2 or F(cover['nearest_center_radius'])!=1:raise RuntimeError('invalid continuity budget')
    cells=[(max(F(0),c-1),min(F(10),c+1)) for c in expected]
    if [[F(x) for x in cell] for cell in cover['cells']]!=[list(c) for c in cells]:raise RuntimeError('coverage cells changed')
    if cells[0][0]!=0 or cells[-1][1]!=10 or any(a[1]<b[0] for a,b in zip(cells,cells[1:])):raise RuntimeError('range has a hole')
    lows=[]
    for center in expected:
        index=cover['certificate_index_by_center'][str(center)]
        if isinstance(index,bool) or not isinstance(index,int) or not 0<=index<len(certs):raise RuntimeError('invalid certificate reference')
        c=certs[index]
        if F(c['alpha'])!=1 or F(c['coupling'])!=center:raise RuntimeError('certificate belongs to another parameter')
        lows.append(F(c['gap_interval']['lower']))
    lower=min(lows)-2
    conservative=F(cover['conservative_uniform_gap_lower'])
    if F(cover['uniform_gap_lower'])!=lower or not 0<conservative<=lower or conservative!=F(999999,1000000):raise RuntimeError('invalid range bound or changed target constant')
    if cover.get('status')!='certified-conditional-on-gap-Lipschitz-theorem':raise RuntimeError('invalid range status')
    return {'exact_point_certificates':len(certs),'uniform_lower':str(lower),'conservative_lower':str(conservative),'scope':cover['scope'],'status':'replayed exact arithmetic under analytic theorems'}

def make_library():
    scope='P';seed='P_contract'
    assumptions={seed:'One four-link SU(2) cycle with normalized product Haar and vertex gauge action; alpha>0, lambda>=0; h(kappa)=H/alpha.',
      'P_gauge':'The physical state space is the gauge-invariant sector on this declared cycle.',
      'P_tail_positive':'The compressed magnetic potential is nonnegative; tau=alpha*N*(N+2).',
      'P_exact_brackets':'All stored exact rational finite-matrix and strict tail-margin certificates replay successfully.',
      'P_exact_cover':'The stored exact six-center coverage of closed kappa interval [0,10] and its positive margin replay successfully.'}
    statements={
      'P_loop':'Tree reduction leaves the loop conjugacy class with normalized Haar class norm.',
      'P_characters':'SU(2) characters form the physical orthonormal basis.',
      'P_jacobi':'The exact operator has diagonal alpha*n*(n+2)+lambda and offdiagonal -lambda/2.',
      'P_radial':'The Haar unitary map gives the regular Dirichlet radial operator.',
      'P_operator':'Positive alpha and bounded potential give a self-adjoint compact-resolvent operator.',
      'P_simple':'The radial Dirichlet eigenspaces are simple; the first gap is positive at fixed parameters.',
      'P_tail':'Every omitted representation has the proved compressed lower threshold tau.',
      'P_lower_block':'Young completion gives H >= B_N direct_sum R with the verified strict margin.',
      'P_minmax':'First two B_N levels and A_N levels bound the full operator energies in the required directions.',
      'P_point_gaps':'Opposite energy endpoints provide exact lower and upper gap bounds at certified centers.',
      'P_lipschitz':'The scalar kappa shift cancels; norm(cos theta)=1 gives a 2-Lipschitz gap.',
      'P_cover':'Every kappa in [0,10] lies within radius one of a certified center.',
      'P_uniform':'For the full infinite character tower, delta(kappa)>=999999/1000000 on all [0,10].',
      'P_scaled':'Delta(alpha,lambda)>=alpha*999999/1000000 whenever alpha>0 and lambda/alpha is in [0,10].'}
    steps=[(['P_contract','P_gauge'],'P_loop'),(['P_loop'],'P_characters'),(['P_characters','P_contract'],'P_jacobi'),
      (['P_jacobi','P_characters'],'P_radial'),(['P_radial','P_contract'],'P_operator'),(['P_operator','P_radial'],'P_simple'),
      (['P_jacobi','P_tail_positive'],'P_tail'),(['P_tail','P_exact_brackets'],'P_lower_block'),
      (['P_lower_block','P_operator','P_exact_brackets'],'P_minmax'),(['P_minmax','P_exact_brackets'],'P_point_gaps'),
      (['P_jacobi','P_operator'],'P_lipschitz'),(['P_exact_cover'],'P_cover'),
      (['P_point_gaps','P_lipschitz','P_cover'],'P_uniform'),(['P_uniform','P_contract'],'P_scaled')]
    inherited={a:{a} for a in assumptions}
    for prem,con in steps:inherited[con]=set().union(*(inherited[p] for p in prem))
    nodes=[]
    for key,value in assumptions.items():
        arithmetic=key in ('P_exact_brackets','P_exact_cover')
        nodes.append(dict(id=key,statement=value,scope=scope,kind='theorem' if arithmetic else 'declared_hypothesis',assumption_ids=[],verification='exact arithmetic replay executed before admission' if arithmetic else 'explicit mathematical contract',source='solver/output/continuous_range_certificate.json' if arithmetic else 'advisor/advisor.md',version='10.1'))
    for key,value in statements.items():nodes.append(dict(id=key,statement=value,scope=scope,kind='theorem',assumption_ids=sorted(inherited[key]),verification='independently reviewed conventional proof; not a formal proof kernel',source='advisor/advisor.md',version='10.1'))
    nodes.append(dict(id='P_millennium',statement='Nontrivial four-dimensional quantum Yang-Mills with positive physical mass gap for every compact simple group.',scope=scope,kind='target',assumption_ids=[],verification='open obligation; no admitted certificate',source='advisor/advisor.md',version='10.1'))
    rules=[dict(id=f'P_rule_{i+1}',premises=p,conclusion=c,cost=1,scope=scope,proof_ref='advisor/advisor.md',review_status='reviewed') for i,(p,c) in enumerate(steps)]
    return dict(nodes=nodes,rules=rules,initial_facts=list(assumptions),goals=['P_scaled'],conditional_assumptions=[],blocked_goals=[])

def execute():
    manifest=json.loads((HERE/'proof_manifest.json').read_text())
    for rel,digest in manifest['sha256'].items():
        if hashlib.sha256((HERE/rel).read_bytes()).hexdigest()!=digest:raise RuntimeError('Changed reviewed proof input: '+rel)
    arithmetic=replay_arithmetic();base=make_library();libs={'certified_parameter_range':base}
    for label,premise in [('without_gauge_projection','P_gauge'),('without_tail_positivity','P_tail_positive'),('without_exact_brackets','P_exact_brackets'),('without_continuous_cover','P_exact_cover')]:
        lib=copy.deepcopy(base);lib['initial_facts'].remove(premise);libs[label]=lib
    prize=copy.deepcopy(base);prize['goals']=['P_millennium'];libs['yang_mills_prize']=prize
    outputs={}
    for name,lib in libs.items():
        result=plan(lib);expected='proved' if name=='certified_parameter_range' else 'not_derivable'
        if result['status']!=expected:raise RuntimeError((name,result['status']))
        if expected=='proved' and not result.get('certified_proof'):raise RuntimeError('missing proof replay')
        outputs[name]={'library':lib,'result':result}
    mutant=copy.deepcopy(prize);mutant['initial_facts'].append('P_millennium')
    try:plan(mutant)
    except ContractError:pass
    else:raise RuntimeError('unproved prize accepted as starting fact')
    out={'status':'passed','scope':'Exact arithmetic prerequisites plus conventional analytic implications in finite Horn search; no continuum proof or proof-assistant formalization.','arithmetic':arithmetic,'routes':outputs,'manifest':manifest}
    (HERE/'proof_results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:{'status':v['result']['status'],'cost':v['result'].get('certified_cost')} for k,v in outputs.items()}))

if __name__=='__main__':execute()
