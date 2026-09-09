#!/usr/bin/env python3
"""Build or verify a finite, reviewed proof-obligation snapshot.

--freeze is an explicit authoring operation, not part of verification.
Normal execution refuses changed referenced bytes through the round6 guard.
The engine is h=0 bidirectional Horn planning, independently cost-checked by
forward uniform-cost search. It is not a mathematical proof kernel.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def library(scope, domain, facts, rules, goal, reference):
    seed=scope+'_domain'
    nodes=[dict(id=seed,statement=domain,scope=scope,kind='declared_hypothesis',
                assumption_ids=[],verification='declared model domain',source=reference,version='7.1')]
    nodes += [dict(id=i,statement=s,scope=scope,kind='theorem',assumption_ids=[seed],
                   verification='reviewed conventional argument; not proof-kernel checked',
                   source=reference,version='7.1') for i,s in facts.items()]
    rr=[dict(id=scope+'_'+str(j+1),premises=p,conclusion=c,cost=1,scope=scope,
             proof_ref=ref or reference,review_status='reviewed')
        for j,(p,c,ref) in enumerate(rules)]
    return dict(nodes=nodes,rules=rr,initial_facts=[seed],goals=[goal],
                conditional_assumptions=[],blocked_goals=[])

def build():
    F='round7/variable_contract.md F1-F5; round7/skeptic_review.md'
    facts={
      'F_def':'Finite positive modes, source, f=1+g^2 phi^2 and scalar potential are defined.',
      'F_action':'The complete finite hybrid action includes scalar kinetic and magnetic energy.',
      'F_coeff':'C_a=2D and Z_a=-2e^2D by differentiation at fixed canonical nodes.',
      'F_spin':'Spinor variation gives normalized Bloch precession.',
      'F_maxwell':'Potential variation gives Z xprime=F-e^2(S+Dx^2)-f_phi y x.',
      'F_scalar':'Scalar variation gives yprime=-nu^2 phi+f_phi(x^2-b^2)/2.',
      'F_norm':'Bloch norms remain <=1 at all times where the solution exists.',
      'F_modework':'Differentiation of mode energy gives Uprime=xS.',
      'F_fieldwork':'Field plus mode work is xF-f_phi y x^2/2.',
      'F_scalarwork':'Scalar plus shifted magnetic work is f_phi y x^2/2.',
      'F_work':'The full shifted energy satisfies Wtildeprime=xF.',
      'F_oldgap':'At b=10,K=20 the exact-coefficient positive quadrature family has original gap >=3/4.',
      'F_gap':'The scalar f>=1 retains the original global positive gap.',
      'F_positive':'Physical Bloch norms and the gap make all shifted energy terms nonnegative.',
      'F_bound':'The epsilon-regularized work estimate bounds sqrt(Wtilde) on every finite interval.',
      'F_states':'x,y,phi,a and all finite modes are bounded on each finite interval; Omega=0 handled separately.',
      'F_global':'Smoothness on the positive-gap domain and continuation give a unique global forward solution for each finite model.'}
    rules=[(['F_domain'],'F_def',None),(['F_def'],'F_action',None),(['F_action'],'F_coeff',None),
      (['F_action'],'F_spin',None),(['F_coeff','F_action'],'F_maxwell',None),(['F_action'],'F_scalar',None),
      (['F_spin'],'F_norm',None),(['F_norm','F_spin'],'F_modework',None),
      (['F_modework','F_coeff','F_maxwell'],'F_fieldwork',None),(['F_scalar'],'F_scalarwork',None),
      (['F_fieldwork','F_scalarwork'],'F_work',None),
      (['F_def'],'F_oldgap','round6/advisor_plan.md; round6/code/coefficient_certificate.py; round7/variable_contract.md F1 F4'),
      (['F_oldgap','F_def'],'F_gap',None),(['F_gap','F_norm'],'F_positive',None),
      (['F_positive','F_work'],'F_bound',None),(['F_bound','F_norm'],'F_states',None),
      (['F_states','F_gap','F_maxwell','F_scalar'],'F_global',None)]
    finite=library('F','Finite canonical positive modes, physical initial Bloch norms, continuous drive, b=10,K=20 and exact positive quadrature normalization; g>=0,nu>=0 fixed.',facts,rules,'F_global',F)
    G='round7/variable_contract.md G1-G4; round7/independent_checks.py'
    gfacts={
      'G_action':'Classical Einstein plus canonical scalar and -fF^2/4 action, no charged quantum sector.',
      'G_stress':'Metric variation yields rho, p_perp and p_parallel including scalar and anisotropic EM stress.',
      'G_flux':'Gauge variation and Bianchi identity give conserved displacement and magnetic flux.',
      'G_scalar':'Scalar variation gives the electromagnetic force with its fixed sign and coefficient.',
      'G_emwork':'The flux laws give Q_EM=fprime(B^2-E^2)/2.',
      'G_scalarwork':'The scalar equation gives Q_scalar=-fprime(B^2-E^2)/2.',
      'G_ward':'Total homogeneous matter exchange Q_total=0.',
      'G_spatial':'The two spatial Einstein equations fix hpprime and hlprime.',
      'G_identity':'Differentiating the constraint gives Cgprime=-theta Cg-Q_total.',
      'G_propagation':'The integrating factor gives Cg(t)=Cg(0) exp(-integral theta).',
      'G_result':'Constraint-satisfying data preserve Cg=0 on the regular interval.'}
    grules=[(['G_domain'],'G_action',None),(['G_action'],'G_stress',None),(['G_action'],'G_flux',None),
      (['G_action'],'G_scalar',None),(['G_flux','G_stress'],'G_emwork',None),
      (['G_scalar','G_stress'],'G_scalarwork',None),(['G_emwork','G_scalarwork'],'G_ward',None),
      (['G_action','G_stress'],'G_spatial',None),(['G_spatial','G_stress'],'G_identity',None),
      (['G_identity','G_ward'],'G_propagation',None),(['G_propagation','G_domain'],'G_result',None)]
    gravity=library('G','Classical axial Bianchi I, aligned homogeneous fields, f=exp(2c varphi), finite regular solution and initial Cg=0.',gfacts,grules,'G_result',G)
    C='round7/variable_contract.md 1.1; round7/skeptic_review.md S1-S8'
    cutoff=library('C','Continuous symmetric momentum integral, positive field and finite inclusive Landau cutoff; fixed reference potential a=0 and z_ref>0.',
      {'C_max':'The exact continuous coefficient is maximized at a=0.',
       'C_match':'Declare the constant-per-run coefficient chi_NK=z_ref-1+e^2 C_NK(0).',
       'C_identity':'Z_NK(a)=z_ref+e^2(C_NK(0)-C_NK(a)).',
       'C_gap':'The reference-subtracted continuous coefficient has gap Z>=z_ref.'},
      [(['C_domain'],'C_max',C),(['C_domain'],'C_match',C),(['C_match'],'C_identity',C),
       (['C_identity','C_max'],'C_gap',C)],'C_gap',C)
    no_go=library('B','Cofinal N,K grow together, |a_NK|<=A and h_NK<=H uniformly; coefficient is Z=h-e^2 C with fixed e^2>0.',
      {'B_include':'The translated window contains the centered K-A window.',
       'B_diverge':'C_N,K-A(0) diverges along every cofinal sequence.',
       'B_bound':'C_NK(a)>=C_N,K-A(0) and h_NK<=H.',
       'B_result':'Z tends to negative infinity, so bounded additions cannot retain a uniform positive gap.'},
      [(['B_domain'],'B_include',C),(['B_domain'],'B_diverge',C),(['B_include'],'B_bound',C),
       (['B_bound','B_diverge'],'B_result',C)],'B_result',C)
    missing=library('U','The two reduced actions and coefficient lemmas have been established in their separate scopes; no common quantum functional has been constructed.',
      {'U_observations':'Scoped reduced-model results are available as context only.',
       'U_ctp':'A common causal quantum functional and admissible evolving state are constructed.',
       'U_variation':'Current, both pressures, energy and scalar density are varied from that same functional.',
       'U_matching':'Allowed counterterms and finite physical matching conditions are fixed together.',
       'U_limits':'State/current/stress convergence and a controlled approximation error are established.',
       'U_evolution':'The resulting constrained semiclassical initial-value problem has controlled regular evolution.',
       'U_result':'A verifiable semiclassical Einstein-QED closure is constructed in a stated regime.'},
      [(['U_domain'],'U_observations','round7/variable_contract.md 4')],
      'U_result','round7/renormalization_map.md')
    # Missing nodes are targets, not admitted theorems, and there is no sufficient
    # rule to the final target. Backward obligation proposals remain non-executable.
    for node in missing['nodes']:
        if node['id'] not in ('U_domain','U_observations'):
            node.update(kind='target',verification='open obligation; not an admitted premise')
    missing['proposed_obligations']=['U_ctp','U_variation','U_matching','U_limits','U_evolution']
    missing['proposal_semantics']='Research decomposition, not a reviewed sufficient theorem or executable inference.'
    broken=copy.deepcopy(finite)
    broken['rules']=[r for r in broken['rules'] if r['conclusion']!='F_maxwell']
    # Withdrawal of a certificate tests the planner; it does not say the wrong
    # physical system has the same action. Its nonzero work defect is tested separately.
    finite['scenarios']={'gravity_constraint':gravity,'reference_coefficient':cutoff,
                        'bounded_addition_obstruction':no_go,'missing_Maxwell_certificate':broken,
                        'common_quantum_closure':missing}
    return finite

def freeze():
    path=HERE/'proof_library.json'
    path.write_text(json.dumps(build(),indent=2)+'\n')
    refs=['round7/proof_library.json','round7/proof_obligations.py',
          'round7/variable_contract.md','round7/skeptic_review.md','round7/independent_checks.py',
          'round7/renormalization_map.md','round6/advisor_plan.md','round6/code/coefficient_certificate.py',
          'round6/code/proof_search.py','round6/code/evidence_guard.py']
    (HERE/'proof_manifest.json').write_text(json.dumps({'version':'7.1',
       'files':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in refs}},indent=2)+'\n')

def run():
    spec=importlib.util.spec_from_file_location('round7_guard',ROOT/'round6/code/evidence_guard.py')
    mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    result=mod.bound_plan(HERE/'proof_library.json',HERE/'proof_manifest.json',ROOT)
    if result['status']!='proved':
        raise RuntimeError('Finite continuation route was not certified in the rule library')
    for name,r in result['scenario_results'].items():
        expected='not_derivable' if name in ('common_quantum_closure','missing_Maxwell_certificate') else 'proved'
        if r['status']!=expected:
            raise RuntimeError(f'{name}: expected {expected}, got {r["status"]}')
    (HERE/'proof_search_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'cost':result.get('certified_cost'),
                     'scenarios':{k:{'status':v['status'],'cost':v.get('certified_cost')} for k,v in result['scenario_results'].items()}}))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--freeze',action='store_true')
    args=parser.parse_args()
    if args.freeze:
        freeze()
    run()
