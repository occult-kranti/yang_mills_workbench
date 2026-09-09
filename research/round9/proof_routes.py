#!/usr/bin/env python3
"""Scope-checked Horn planning and independent certificate replay; not a proof kernel."""
from pathlib import Path
import copy
import hashlib
import json
from proof_search import plan, ContractError

HERE=Path(__file__).resolve().parent

def library(scope,domain,statements,steps,goal,extra=None):
    seed=scope+'_domain'
    nodes=[dict(id=seed,statement=domain,scope=scope,kind='declared_hypothesis',assumption_ids=[],verification='explicit conditional model contract',source='advisor/advisor.md',version='9.1')]
    initials=[seed]
    for key,statement in (extra or {}).items():
        nodes.append(dict(id=key,statement=statement,scope=scope,kind='declared_hypothesis',assumption_ids=[],verification='explicit hypothesis; not supplied by sampled residuals',source='advisor/advisor.md',version='9.1'))
        initials.append(key)
    # Track the hypotheses actually inherited along each implication. Assigning
    # all initial facts to every conclusion fabricates hidden dependencies.
    inherited={key:{key} for key in initials}
    for premises,conclusion in steps:
        inherited[conclusion]=set().union(*(inherited[p] for p in premises))
    nodes.extend(dict(id=k,statement=v,scope=scope,kind='theorem',assumption_ids=sorted(inherited.get(k,{seed})),verification='reviewed conventional implication, not proof-kernel checked',source='advisor/advisor.md',version='9.1') for k,v in statements.items())
    rules=[dict(id=f'{scope}_{i+1}',premises=p,conclusion=c,cost=1,scope=scope,proof_ref='advisor/advisor.md',review_status='reviewed') for i,(p,c) in enumerate(steps)]
    return dict(nodes=nodes,rules=rules,initial_facts=initials,goals=[goal],conditional_assumptions=[],blocked_goals=[])

def build():
    H=library('H','Finite connected compact Lie product G^E, smooth real action S and Borel probability nu; all link Lie algebra generators.',{
        'H_bounded':'S bounded; exp(S)nu is a finite nonzero measure eta.',
        'H_insert':'The complete smooth hierarchy permits f=exp(S)phi for every smooth phi.',
        'H_cancel':'Derivative terms cancel, giving integral Li phi deta=0.',
        'H_flow':'All one-parameter generator flows preserve eta.',
        'H_translation':'Connectedness and all link generators imply full left-translation invariance.',
        'H_haar':'Haar uniqueness identifies eta=cHaar.',
        'H_density':'nu=c exp(-S)Haar.',
        'H_result':'Normalization gives exactly nu=Z^-1 exp(-S)Haar.'},[
          (['H_domain'],'H_bounded'),(['H_all'],'H_insert'),(['H_bounded','H_insert'],'H_cancel'),
          (['H_cancel'],'H_flow'),(['H_flow','H_domain'],'H_translation'),(['H_translation'],'H_haar'),
          (['H_haar','H_bounded'],'H_density'),(['H_density','H_domain'],'H_result')],'H_result',
          {'H_all':'For every smooth test f and every link generator Li, integral(Li f-f LiS)dnu=0.'})
    K=library('K','Normalized central SU(2) convolution exp(beta ReTr(UVdagger)/2), beta>0, full L2(SU2,Haar), at>0.',{
        'K_haar':'Class integration has weight (2/pi)sin^2(theta).',
        'K_char':'Spin j character sin(n theta)/sin(theta), n=2j+1.',
        'K_integral':'Character integral=2n I_n(beta)/beta; Z=2I1(beta)/beta.',
        'K_divide':'Central convolution divides character coefficient by dimension n.',
        'K_spectrum':'Peter-Weyl gives all eigenvalues I_n/I1 with multiplicity n^2.',
        'K_order':'Positive Bessel integral and recurrence give 0<I_(n+1)/I_n<1.',
        'K_result':'Largest nonconstant eigenvalue I2/I1; rotor generator gap -log(I2/I1)/at.'},[
          (['K_domain'],'K_haar'),(['K_domain'],'K_char'),(['K_haar','K_char'],'K_integral'),
          (['K_domain'],'K_divide'),(['K_integral','K_divide'],'K_spectrum'),(['K_domain'],'K_order'),
          (['K_spectrum','K_order'],'K_result')],'K_result')
    T=library('T','Positive self-adjoint contractions T,S on one common Hilbert space, a,m>0; logarithmic generators on support.',{
        'T_invariant':'The common vacuum complement is invariant under both operators.',
        'T_triangle':'On that complement norm S<=exp(-ma)+epsilon.',
        'T_margin':'The upper bound lies strictly below one.',
        'T_spectrum':'Spectral calculus turns contraction norm into a logarithmic energy lower bound.',
        'T_result':'Gap of S on its nonvacuum support is at least -log(exp(-ma)+epsilon)/a>0.'},[
          (['T_domain','T_vacuum'],'T_invariant'),(['T_invariant','T_reference','T_error'],'T_triangle'),
          (['T_budget'],'T_margin'),(['T_domain','T_triangle'],'T_spectrum'),
          (['T_margin','T_spectrum'],'T_result')],'T_result',{
            'T_vacuum':'T Omega=S Omega=Omega for the same normalized vacuum.',
            'T_reference':'Reference norm on Omega complement <=exp(-ma).',
            'T_error':'Actual operator norm ||T-S||<=epsilon>=0, not merely average kernel L1.',
            'T_budget':'exp(-ma)+epsilon<1.'})
    Y=library('Y','Project finite SU2 Wilson and auxiliary operator results only; no continuum construction assumed.',{
        'Y_context':'Finite models supply exact identities and falsification tools.',
        'Y_prize':'Nontrivial four-dimensional pure Yang-Mills exists with positive physical mass gap for every compact simple group.'},[
          (['Y_domain'],'Y_context')],'Y_prize')
    for n in Y['nodes']:
        if n['id']=='Y_prize':n.update(kind='target',verification='open; no admitted proof')
    missing_h=copy.deepcopy(H);missing_h['initial_facts'].remove('H_all')
    missing_t=copy.deepcopy(T);missing_t['initial_facts'].remove('T_vacuum')
    wrongnorm=copy.deepcopy(T);wrongnorm['initial_facts'].remove('T_error')
    return {'complete_hierarchy':H,'group_convolution':K,'conditional_stability':T,
      'withheld_all_tests':missing_h,'withheld_common_vacuum':missing_t,'only_product_l1':wrongnorm,'yang_mills_prize':Y}

def execute():
    manifest=json.loads((HERE/'proof_manifest.json').read_text())
    for name,digest in manifest['sha256'].items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest:raise RuntimeError('Changed reviewed file: '+name)
    results={}
    for name,lib in build().items():
        out=plan(lib);expected='proved' if name in ('complete_hierarchy','group_convolution','conditional_stability') else 'not_derivable'
        if out['status']!=expected:raise RuntimeError((name,out['status']))
        if expected=='proved' and not out.get('certified_proof'):raise RuntimeError('missing replay')
        results[name]={'library':lib,'result':out}
    mutant=copy.deepcopy(build()['yang_mills_prize']);mutant['initial_facts'].append('Y_prize')
    try:plan(mutant)
    except ContractError:pass
    else:raise RuntimeError('unproved target accepted as a starting fact')
    out={'status':'passed','scope':'Reviewed conditional implications and two-front Horn search with h=0; not a formal mathematical proof kernel. No continuum route.', 'routes':results,'manifest':manifest}
    (HERE/'proof_results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:{'status':v['result']['status'],'cost':v['result'].get('certified_cost')} for k,v in results.items()}))

if __name__=='__main__':execute()
