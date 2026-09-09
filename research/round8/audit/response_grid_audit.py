"""New bounded delayed-response quadrature study for the fixed finite model.

A centered difference in probe amplitude is computed at the same finite
b=10, ncut=1, Kmax=20 and pump/probe history for all longitudinal node grids.
No continuum claim. This script performs no source editing and writes separate
results next to itself. Threshold is inherited as a working absolute diagnostic
scale from the old epsilon-refinement gate, not a rigorous error enclosure.
"""
from pathlib import Path
from dataclasses import replace
import csv,hashlib,importlib.util,json,sys
import numpy as np
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
source=HERE/'fixed/finite_scalar.py'
spec=importlib.util.spec_from_file_location('r8_scalar_response_grid',source)
f=importlib.util.module_from_spec(spec);sys.modules[spec.name]=f;spec.loader.exec_module(f)
FIELDS=('a','x','phi','y')
EPS=5e-5
BASE_AMPLITUDE=.15
THRESHOLD=2e-5
p=f.Params()
responses={};diagnostics={};records=[]
def run_grid(nk):
    q=replace(p,nK=nk)
    plus=f._solve(q,mode='delayed_probe',probe_amp=BASE_AMPLITUDE+EPS)
    minus=f._solve(q,mode='delayed_probe',probe_amp=BASE_AMPLITUDE-EPS)
    t=np.array(plus['macro']['t']);pre=t<q.probe_start
    d={k:(np.array(plus['macro'][k])-np.array(minus['macro'][k]))/(2*EPS) for k in FIELDS}
    if not all(np.isfinite(v).all() for v in d.values()):raise RuntimeError('Nonfinite derivative')
    responses[nk]=d
    diagnostics[nk]={'plus':plus['diagnostics'],'minus':minus['diagnostics'],
                     'pre_probe_samples':int(np.sum(pre)),
                     'max_pre_probe_response':{k:float(np.max(abs(v[pre]))) for k,v in d.items()}}
    for i,time in enumerate(t): records.append({'nK':nk,'t':float(time),**{k:float(d[k][i]) for k in FIELDS}})
    print(json.dumps({'completed_nodes':nk,'response_peaks':{k:float(np.max(abs(v))) for k,v in d.items()}}),flush=True)

def compare(lo,hi):
    return {'coarse_nK':lo,'fine_nK':hi,'max_abs_response_difference':
            {k:float(np.max(abs(responses[lo][k]-responses[hi][k]))) for k in FIELDS}}
for nk in (64,128,256):run_grid(nk)
comparisons=[compare(64,128),compare(128,256)]
# One conditional extension, declared before observing any computed result.
if max(comparisons[-1]['max_abs_response_difference'].values())>THRESHOLD:
    run_grid(512);comparisons.append(compare(256,512))
last=comparisons[-1]
resolved=max(last['max_abs_response_difference'].values())<THRESHOLD
result={'status':'resolved_working_threshold' if resolved else 'unresolved_working_threshold',
        'scope':'Finite-regulator centered delayed-source sensitivity; common source and physical cutoffs. No rigorous interval or continuum bound.',
        'base_parameters':p.__dict__,'probe_amplitude':BASE_AMPLITUDE,'epsilon':EPS,
        'working_absolute_threshold':THRESHOLD,'nodes':list(responses),
        'comparisons':comparisons,'integration_diagnostics':diagnostics,
        'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'limitations':['Response error still contains finite-difference truncation and ODE error.',
                       'Adjacent-grid agreement is evidence, not an upper bound on all discretization error.',
                       'Landau cutoff and momentum window remain fixed; current/stress continuum limits untested.']}
(HERE/'response_grid_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
with (HERE/'response_grid_histories.csv').open('w',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=['nK','t',*FIELDS]);writer.writeheader();writer.writerows(records)
print(json.dumps({'status':result['status'],'comparisons':comparisons}))
