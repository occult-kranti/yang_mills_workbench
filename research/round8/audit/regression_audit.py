"""Independent bounded regressions for three demonstrated round7 defects.

Original files are read only. Fixed files are explicitly a proposed new revision.
Run using Python with NumPy/SciPy; no SymPy dependency is needed for these tests.
"""
from pathlib import Path
from dataclasses import replace
import copy
import hashlib
import importlib.util
import json
import sys
import warnings
import numpy as np
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ORIGINAL = HERE.parent / 'evidence/qeg-research/round7'
FIXED = HERE / 'fixed'

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

oldf = load('original_finite_audit', ORIGINAL/'finite_scalar.py')
newf = load('revised_finite_audit', FIXED/'finite_scalar.py')
oldg = load('original_gravity_audit', ORIGINAL/'gravity_sim.py')
newg = load('revised_gravity_audit', FIXED/'gravity_sim.py')
# Resolve comparator references against archived evidence; no main() is called.
newf.HERE = ORIGINAL
rows=[]
def gate(name, condition, evidence):
    ok=bool(condition)
    rows.append(dict(name=name,passed=ok,evidence=evidence))
    if not ok: raise RuntimeError(name+': '+str(evidence))
def must_reject(name, call, exception):
    try: call()
    except exception as error: gate(name,True,str(error))
    else: gate(name,False,'Call returned without required exception')

pold=oldf.Params(nK=16,ncut=0,chi_b=.2)
pnew=newf.Params(nK=16,ncut=0,chi_b=.2)
mismatch=oldf.g0_baseline_compare(pold)
gate('Original arbitrary matching comparator changes physical coefficient',
     mismatch['status']=='compared' and not mismatch['passed'],mismatch)
blocked=newf.g0_baseline_compare(pnew)
gate('Revised arbitrary coefficient reports comparator unavailable',
     blocked['status']=='unavailable' and 'chi_b' in blocked['reason'],blocked)
for chi in (None,0.,-newf.chi_match(pnew.b)):
    match=newf.g0_baseline_compare(replace(pnew,chi_b=chi))
    gate('Supported matching prescription agrees '+str(chi),
         match['status']=='compared' and match['passed'],match)

extreme=dict(nK=16,ncut=0,g=0.,nu=0.,phi0=1e155,y0=1e155,target_E=0.)
with warnings.catch_warnings():
    warnings.simplefilter('ignore',RuntimeWarning)
    invalid=oldf._solve(oldf.Params(**extreme))
gate('Original finite states can return nonfinite energy diagnostic',
     np.isfinite(invalid['macro']['phi']).all() and
     not np.isfinite(invalid['diagnostics']['max_energy_mismatch']),
     {'state_is_finite':True,'energy_residual':'NaN','scalar_initial_amplitude':1e155})
must_reject('Revised finite solver rejects overflowed observables',
            lambda:newf._solve(newf.Params(**extreme)),newf.FiniteScalarFailure)
ordinary_old=oldf._solve(replace(pold,chi_b=None))
ordinary_new=newf._solve(replace(pnew,chi_b=None))
gate('Diagnostic correction preserves ordinary physical histories',
     all(np.array_equal(ordinary_old['macro'][k],ordinary_new['macro'][k])
         for k in ordinary_old['macro']),
     {'comparison':'exactly equal sampled floats across every macro field'})

empty=oldg.build_results([])
gate('Original empty gravity collection falsely reports pass',
     empty['status']=='passed' and all(empty['gates'].values()),
     {'status':empty['status'],'vacuously_true_trajectory_gates':len(empty['gates'])})
must_reject('Revised gravity results reject an empty collection',
            lambda:newg.build_results([]),newg.InputError)
run=newg.run_case(newg.default_cases()[0])
correct=newg.build_results([run])
gate('Revised gravity summary admits executed valid case',
     correct['status']=='passed' and all(correct['gates'].values()),correct['gates'])
corrupt=copy.copy(run);corrupt['diagnostics']=dict(run['diagnostics'])
corrupt['diagnostics']['max_constraint_scaled_full']=1.
old_result=oldg.build_results([corrupt]);new_result=newg.build_results([corrupt])
gate('Original builder exposes contradictory status with failed constraint gate',
     old_result['status']=='passed' and not old_result['gates']['true_constraint_small'],
     {'status':old_result['status'],'true_constraint_small':False,
      'input':'deliberately corrupted diagnostic record, not a physical trajectory'})
gate('Revised semantic status follows its failed diagnostic gate',
     new_result['status']=='failed' and not new_result['gates']['true_constraint_small'],
     {'status':new_result['status'],'true_constraint_small':False})

before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in
        [ORIGINAL/'finite_scalar.py',ORIGINAL/'gravity_sim.py',FIXED/'finite_scalar.py',FIXED/'gravity_sim.py']}
result={'status':'passed','scope':'Regression demonstration and proposed finite/gravity implementation corrections; no continuum or mathematical proof',
        'checks':rows,'passed_checks':len(rows),'source_sha256':before}
(HERE/'regression_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
print(json.dumps({'status':result['status'],'passed_checks':len(rows)}))
