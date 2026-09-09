"""Minimal executable evidence of two self-audited pre-freeze defects.

The old acceptance condition below was a latent flaw; the benchmark's actual
quadrature rows did not have a large normalization error. The constructed row
proves that the omitted field could have escaped acceptance.
"""
from decimal import Decimal, localcontext
import json
from pathlib import Path
from su2_transfer import log_normalization, decimal_reference

with localcontext() as ctx:
    ctx.prec=100  # Original requested 80 digits plus 20 working digits.
    x=Decimal('1e-100')
    i1=x/2+x**3/16
    legacy_log_z=(2*i1/x).ln()
    exact_leading=x*x/8
relative_error=0.
refinement_error=0.
normalization_error=1.
legacy_accept=(relative_error < 1e-10 and refinement_error < 1e-10)
corrected_accept=(legacy_accept and normalization_error < 1e-10)
record={
    'tiny_beta_normalization':{
        'beta':'1e-100','old_working_digits':100,
        'legacy_log_Z_decimal':str(legacy_log_z),
        'analytic_leading_log_Z_decimal':str(exact_leading),
        'corrected_log_Z':log_normalization(1e-100),
        'failure':'Fixed working precision rounded Z to 1 before taking log.'},
    'omitted_normalization_acceptance':{
        'fixture':'constructed perturbation of normalization diagnostic, with exact ratio and refinement',
        'relative_ratio_error':relative_error,'refinement_error':refinement_error,
        'log_Z_error':normalization_error,'old_accepts':legacy_accept,
        'new_accepts':corrected_accept,
        'failure':'Diagnostic computed and recorded but not included in pass predicate.'},
    'reviewer_requested_underflow_case':decimal_reference(1e-300,1),
    'original_source_sha256':{
        'su2_transfer.py':'2870f48a246235514db3c1aab0e6b708105c1c1b81313790426dedc6f381225e',
        'run_benchmark.py':'0947db4586deb9001072b9ea0b2a7af4c1d6aafda545d21fd0b798c5e3bd7072'}
}
if legacy_log_z!=0 or not legacy_accept or corrected_accept:
    raise RuntimeError('retained failure fixture no longer reproduces')
out=Path(__file__).resolve().parent/'output'/'retained_failures.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
print(json.dumps({'retained_failure_fixture_status':'reproduced','output':str(out)}))
