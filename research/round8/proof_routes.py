#!/usr/bin/env python3
"""Replay finite reviewed Horn rules. These are conditional proof notes, not a proof kernel."""
from pathlib import Path
import copy
import hashlib
import json
from proof_search import plan, ContractError

HERE = Path(__file__).resolve().parent

def library(scope, domain, statements, steps, goal):
    seed = scope + '_domain'
    nodes = [dict(id=seed, statement=domain, scope=scope, kind='declared_hypothesis',
                  assumption_ids=[], verification='explicit conditional domain',
                  source='spectral-proof.md', version='8.1')]
    nodes += [dict(id=k, statement=v, scope=scope, kind='theorem', assumption_ids=[seed],
                   verification='independently reviewed conventional argument; not kernel checked',
                   source='spectral-proof.md', version='8.1') for k,v in statements.items()]
    rules = [dict(id=f'{scope}_{i+1}',premises=p,conclusion=c,cost=1,scope=scope,
                  proof_ref='spectral-proof.md',review_status='reviewed') for i,(p,c) in enumerate(steps)]
    return dict(nodes=nodes,rules=rules,initial_facts=[seed],goals=[goal],
                conditional_assumptions=[],blocked_goals=[])

def build():
    effective=library('E','Finite nonzero positive Borel spectral measure on [0,infinity), finite norm states, t>=0 and fixed delta>0; zero-temperature semigroup.',{
        'E_positive':'C(t) is finite and strictly positive.',
        'E_probability':'The measure exp(-Et)dmu/C(t) is a probability measure.',
        'E_support':'Its energies obey E>=inf support mu.',
        'E_ratio':'C(t+delta)/C(t)<=exp(-delta inf support mu).',
        'E_bound':'Effective mass >= inf support mu.',
        'E_convex':'Holder implies log C is convex.',
        'E_monotone':'Fixed-step negative secant slopes are nonincreasing.',
        'E_result':'Effective mass is a monotone upper estimate of its channel threshold.'},[
            (['E_domain'],'E_positive'),(['E_positive'],'E_probability'),
            (['E_domain'],'E_support'),(['E_probability','E_support'],'E_ratio'),
            (['E_ratio'],'E_bound'),(['E_domain'],'E_convex'),
            (['E_convex'],'E_monotone'),(['E_bound','E_monotone'],'E_result')],'E_result')
    uniform=library('U','Assume already constructed nonnegative self-adjoint H, normalized zero vacuum, positive diagonal semigroup correlators on states spanning densely in vacuum-orthogonal space, and a common m>0 with finite per-state prefactors and onset times for all sufficiently large physical t.',{
        'U_spectral':'The diagonal correlator is the Laplace transform of a finite positive spectral measure.',
        'U_upper':'C_psi(t)<=A_psi exp(-m t) at every t>=t_psi.',
        'U_lower':'exp(-(m-epsilon)t)||P([0,m-epsilon])psi||^2 <= C_psi(t).',
        'U_zero':'Comparison and t->infinity force every such low-energy projection to vanish.',
        'U_union':'A countable increasing union excludes [0,m) on each admitted state.',
        'U_density':'A bounded spectral projection vanishing on a dense span vanishes throughout vacuum-orthogonal space.',
        'U_gap':'H restricted to the vacuum-orthogonal space has spectrum in [m,infinity).'},[
            (['U_domain'],'U_spectral'),(['U_domain'],'U_upper'),(['U_spectral'],'U_lower'),
            (['U_lower','U_upper'],'U_zero'),(['U_zero'],'U_union'),
            (['U_domain'],'U_density'),(['U_union','U_density'],'U_gap')],'U_gap')
    missing=library('Y','Only the project finite-model results and the conditional spectral lemmas are established; Yang-Mills quantum existence and uniform spectral estimates are not assumed.',{
        'Y_context':'The finite-model work supplies methods and counterexamples only.',
        'Y_existence':'Construct nontrivial four-dimensional pure Yang-Mills for every compact simple group.',
        'Y_decay':'Establish common positive physical decay rates across regulator removal on a dense family.',
        'Y_reconstruction':'Establish full axiomatic reconstruction and physical-state coverage.',
        'Y_prize':'Yang-Mills existence and mass gap holds for the exact prize statement.'},[
            (['Y_domain'],'Y_context')],'Y_prize')
    for node in missing['nodes']:
        if node['id'] not in ('Y_domain','Y_context'):
            node.update(kind='target',verification='open obligation; no certificate admitted')
    broken=copy.deepcopy(effective)
    broken['rules']=[r for r in broken['rules'] if r['conclusion']!='E_probability']
    return {'effective_mass':effective,'uniform_decay_gap':uniform,
            'withheld_probability_certificate':broken,'yang_mills_prize':missing}

def execute():
    manifest=json.loads((HERE/'proof_manifest.json').read_text())
    for name,digest in manifest['sha256'].items():
        if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('Changed proof reference: '+name)
    libraries=build();results={}
    for name,lib in libraries.items():
        result=plan(lib)
        expected='not_derivable' if name in ('withheld_probability_certificate','yang_mills_prize') else 'proved'
        if result['status']!=expected: raise RuntimeError((name,result['status']))
        if expected=='proved' and not result.get('certified_proof'):raise RuntimeError('Missing replay certificate')
        results[name]={'library':lib,'result':result}
    mutant=copy.deepcopy(libraries['yang_mills_prize'])
    mutant['initial_facts'].append('Y_prize')
    try: plan(mutant)
    except ContractError: pass
    else: raise RuntimeError('Unproved target was accepted as a seed')
    out={'status':'passed','scope':'Conditional conventional lemmas and finite inference replay; no mathematical proof kernel or Yang-Mills completion.',
         'routes':results,'checks':['effective mass route replay','uniform decay route replay','withheld prerequisite blocks route','prize stays underivable','unproved target seed rejected'],
         'manifest':manifest}
    (HERE/'proof_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'passed','routes':{k:{'status':v['result']['status'],'cost':v['result'].get('certified_cost')} for k,v in results.items()}}))

if __name__=='__main__':execute()
