from pathlib import Path
import sys, json, hashlib, warnings
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'round4/code'))
import response as old
sys.path.insert(0,str(ROOT.parent/'round5'))
import proof_search as ps
from test_proof_search import library
p=old.Params(nK=12,ncut=0,Kmax=3,b=1,Tpump=.3,tfinal=1.2,probe_start=.5,probe_duration=.3,sample_count=61,max_step=.015,rtol=2e-9,atol=2e-11)
out={}
r=old.run_scenario(p,mode='delayed_probe',probe_amp=.5,epsilons=(.01,.003),include_legacy=False)
out['nonzero_probe']={'finite_difference_errors':[v['max_abs_error'] for v in r['finite_difference']], 'gauge':r['gauge'], 'gates':r['gates']}
with warnings.catch_warnings(record=True) as ws:
 warnings.simplefilter('always')
 r=old.run_scenario(p,epsilons=(0,),include_legacy=False)
 out['zero_epsilon']={'fd_error':str(r['finite_difference'][0]['max_abs_error']),'nan_in_fd':bool(np.any(~np.isfinite(r['finite_difference'][0]['a']))),'warnings':[str(v.message) for v in ws]}
r=old._solve(p,mode='misspelled')
out['unknown_mode_accepted']=r['mode']
for name in ['proposed','conjectural','unsafe','unresolved']:
 d=library(['A'],['T'],[('r',['A'],'T',1)])
 d['nodes'][0]['verification']=name
 try:out['verification_'+name]=ps.plan(d)['status']
 except Exception as exc:out['verification_'+name]=type(exc).__name__
d=library(['A'],['T'],[('r',['A'],'T',10**400)])
try:ps.load_library(d);out['huge_cost']='accepted'
except Exception as exc:out['huge_cost']=type(exc).__name__
(ROOT/'audit_repro_results.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print(json.dumps(out,indent=2))
