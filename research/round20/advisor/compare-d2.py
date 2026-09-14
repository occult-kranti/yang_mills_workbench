#!/usr/bin/env python3
import copy,json,pathlib
from fractions import Fraction as F
R=pathlib.Path(__file__).resolve().parents[1]
def compare(a,b):
 failures=[]
 if len(a['fixtures'])!=9 or len(b['rows'])!=9: failures.append('incomplete')
 for x,y in zip(a['fixtures'],b['rows']):
  for p,q in [('L','L'),('tail_weight','tail'),('projector_norm_error','projector_norm_bound'),('unit_observable_error','observable_error_over_operator_norm')]:
   if x[p]!=y[q]:failures.append(f"L{x['L']}:{p}")
  for p,q in [('beta_L_over_alpha','beta_L_over_E_star'),('g_L_over_alpha','g_L_over_E_star'),('energy_error_over_alpha','ground_energy_error_over_E_star')]:
   if 2*F(x[p])!=F(y[q]):failures.append(f"scale:L{x['L']}:{p}")
 if not all(a['controls'].values()) or not all(x['passed'] for x in b['controls']):failures.append('controls')
 return failures
if __name__=='__main__':
 a=json.loads((R/'forward/d2/output/results.json').read_text());b=json.loads((R/'reverse/d2/output/results.json').read_text());fail=compare(a,b)
 m=copy.deepcopy(a);m['fixtures'][0]['projector_norm_error']='0';bad=bool(compare(m,b))
 r={'loop':'d2','status':'accepted' if not fail and bad else 'rejected','compared_rows':9,'failures':fail,'executed_mutations':{'false_zero_projector_error_rejected':bad},'independence':'Residual reconstruction and independent Riesz-contour check; exact energy units translated.'}
 (R/'advisor/d2-comparison.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
 if r['status']!='accepted':raise SystemExit(1)
