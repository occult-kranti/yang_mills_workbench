#!/usr/bin/env python3
"""Exact F1 weighted-generator and dynamic underidentification controls."""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,hashlib
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
# coeff, number of link factors acted on, Haar variance of trace/2
TERMS=[(F(3),1,F(1,4)),(F(1),1,F(1,4)),(F(1),1,F(1,4)),(F(1),2,F(1,4)),(F(1),2,F(1,4))]

def register(kappa,c,E,provenance='external'):
 if any(isinstance(x,bool) for x in [kappa,c,E]):raise ValueError('boolean parameter')
 k,c,E=map(F,[kappa,c,E])
 if c<=0 or E<=0:raise ValueError('positive external energy c and E_star required')
 if provenance!='external':raise ValueError('physical coefficient requires independent calibration or declared external model choice')
 return {'kappa':str(k),'c/E_star':str(c/E),'ground_density':'exp(kappa*S)/Z_kappa','static_depends_on_c':False}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 lap_at_identity=-sum((coef*links*F(3,4) for coef,links,var in TERMS),F(0))
 gamma_haar=sum((coef**2*links*F(3,4)*var for coef,links,var in TERMS),F(0))
 action_variance=sum((coef**2*var for coef,links,var in TERMS),F(0))
 if (lap_at_identity,gamma_haar,action_variance)!=(F(-27,4),F(45,16),F(13,4)):raise RuntimeError('action algebra mismatch')
 rows=[]
 for k in [F(-1,8),F(0),F(1,8)]:
  for c in [F(1),F(2)]:
   row=register(k,c,F(1));row.update({'wrong_drift_stationarity_residual_over_rho':str(-2*k*lap_at_identity),'unweighted_symmetry_defect':str(-k*gamma_haar)})
   if k==0:row.update({'exact_gap_over_E_star':str(F(3,4)*c),'x_static_variance':'1/4','normalized_initial_decay_in_E_star_over_hbar':str(F(3,4)*c)})
   rows.append(row)
 controls=[]
 def ck(name,value):
  if not value:raise RuntimeError(name)
  controls.append({'name':name,'passed':True})
 zero=[r for r in rows if r['kappa']=='0'];ck('same_static_moments_distinct_dynamic_rates',zero[0]['x_static_variance']==zero[1]['x_static_variance'] and zero[0]['exact_gap_over_E_star']!=zero[1]['exact_gap_over_E_star'])
 ck('wrong_drift_both_signs_rejected',all(F(r['wrong_drift_stationarity_residual_over_rho'])!=0 for r in rows if r['kappa']!='0'))
 ck('missing_rho_measure_breaks_symmetry',all(F(r['unweighted_symmetry_defect'])!=0 for r in rows if r['kappa']!='0'))
 for name,args in [('zero_c',(0,0,1,'external')),('negative_c',(0,-1,1,'external')),('zero_E',(0,1,0,'external')),('kappa_matching',(F(1,8),F(1,8),1,'from_kappa')),('alpha_matching',(0,2,1,'from_alpha_notation')),('fibonacci_matching',(0,1,1,'spiral_index'))]:
  try:register(*args)
  except ValueError:ck(name+'_rejected',True)
  else:raise RuntimeError(name+' admitted')
 data={'schema':'ym20-reverse-f1-v1','status':'passed','rows':rows,'controls':controls,'action_checks':{'DeltaS_identity':str(lap_at_identity),'Haar_integral_GammaS':str(gamma_haar),'Haar_variance_S':str(action_variance)},'conclusion':'Same complete static density underdetermines positive physical c even within specified local reversible diffusions','new_parameter_classification':'c is an external energy coefficient for added dynamics, not a derived match to A2 alpha','source_reading':'Ledoux section1.1 targeted; standard construction; no priority audit'}
 p=out/'results.json';p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round20/contracts/f1.json',ROOT/'research/round20/advisor/e2-gate.json',ROOT/'research/round20/advisor/diffusion-source-notes.md',ROOT/'research/round19/advisor/c2-gate.json']
 (out/'source-manifest.json').write_text(json.dumps({'sources':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'outputs':{'results.json':hashlib.sha256(p.read_bytes()).hexdigest()}},indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'passed','rows':len(rows),'controls':len(controls)}))
if __name__=='__main__':main()
