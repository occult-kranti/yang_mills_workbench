#!/usr/bin/env python3
"""Aggregate executed evidence; unresolved limits are never converted to passes."""
import json
import hashlib
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def sha(n):return hashlib.sha256((ROOT/n).read_bytes()).hexdigest()

prod=read('results/production_baseline.json')
refine=read('results/fixed_window_refinement.json')
ind=read('independent_results.json')
cmp=read('implementation_comparison.json')
adv=read('advisor_checks.json')
grav=read('gravity_checks.json')
bos=read('results/bosonized_comparator.json')
emp=read('empirical_logic_results.json')
assert cmp['source_hash_before']==sha('code/backreaction.py')==cmp['source_hash_after']
assert prod['parameters']['nK']==4096 and prod['parameters']['Kmax']==40
assert ind['all_checks_passed'] and cmp['passed']
assert bos['all_gates_passed'] and emp['all_passed']
assert grav['symbolic']['n_passed']==19

summary={
 'date':'2026-09-09',
 'scope':'Matched finite-regulator homogeneous Maxwell-Dirac mean field; classical gravity fixture and separate quantum comparator.',
 'production_parameters':prod['parameters'],
 'production_diagnostics':prod['diagnostics'],
 'production_source_sha256':sha('code/backreaction.py'),
 'root_production_script_checks':{'executed':'2026-09-09','script':'test_backreaction.py','passed':4,'total':4},
 'independent_checks':ind['checks'],
 'implementation_comparison':cmp,
 'fixed_window_refinement':refine,
 'gravity_symbolic_checks':grav['symbolic']['n_passed'],
 'gravity_fixture':grav['numerical'],
 'bosonized_gates':bos['gates'],
 'empirical_check_groups':emp['number_of_check_groups'],
 'strict_advisor_1e_minus18_gate_passed':adv['strict_requested_abs_error_1e-18_passed'],
 'strict_advisor_gate_note':adv['strict_gate_note'],
 'unresolved':['Rigorous continuum/tail error bound','Full quantum fluctuation validity of the 3+1 mean field','Covariantly renormalized anisotropic quantum pressures','Metric backreaction','Charged de Sitter discharge endpoint','Cauchy-horizon quantum endpoint','Matched dispersive photon-graviton conversion in a multipolar geometry'],
 'source_record':read('assembly_manifest.json'),
 'warning':'Conservation and intersolver agreement do not certify the physical model or all regulator limits.'
}
(ROOT/'validation_summary.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
print(json.dumps({'production_field':prod['diagnostics']['final_x'],'source_hash_verified':True,'strict_advisor_gate_passed':summary['strict_advisor_1e_minus18_gate_passed']}))
