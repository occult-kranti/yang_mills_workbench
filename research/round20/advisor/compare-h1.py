#!/usr/bin/env python3
import copy,json,pathlib
from fractions import Fraction as F
R=pathlib.Path(__file__).resolve().parents[1]
def budget(q):return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def compare(a,b):
 fail=[]
 if a['numerator_coefficients_ascending']!=['2','5','5','6','3']:fail.append('symbolic numerator')
 if a['asymptotic_scaled_budget']!=b['asymptotic_normalized_budget'] or a['asymptotic_scaled_budget']!='7/64':fail.append('endpoint residue')
 ar={(x['q'],x['L']):x for x in a['tail_fixtures']};br={(x['q'],x['L']):x for x in b['rows']}
 common=ar.keys()&br.keys()
 if len(common)!=16:fail.append('common tail coverage')
 for k in common:
  if ar[k]['retained_weight']!=br[k]['retained'] or ar[k]['tail_weight']!=br[k]['tail']:fail.append('tail '+str(k))
 for x in a['q_fixtures']:
  y=next(y for y in b['rows'] if y['q']==x['q'])
  if x['B']!=y['B'] or F(x['B'])!=budget(F(x['q'])) or 2*F(x['default_gap_margin_over_alpha'])!=F(y['default_gap_floor_over_E_star']):fail.append('scale/budget '+x['q'])
 pairs=[(a['critical_q_lower'],a['critical_q_upper'],a['B_critical_lower'],a['B_critical_upper']),tuple(b['critical_default_tau_bracket'][k] for k in ['lower','upper','B_lower','B_upper'])]
 for lo,hi,blo,bhi in pairs:
  if not 0<F(lo)<F(hi)<1 or not budget(F(lo))==F(blo)<8<F(bhi)==budget(F(hi)):fail.append('critical bracket')
 if not all(a['controls'].values()) or not all(x['passed'] for x in b['controls']):fail.append('controls')
 return fail
if __name__=='__main__':
 a=json.loads((R/'forward/h1/output/results.json').read_text());b=json.loads((R/'reverse/h1/output/results.json').read_text());fail=compare(a,b)
 tests={}
 for label,mutator in [('false_endpoint',lambda m:m.update(asymptotic_scaled_budget='1/8')),('coherent_false_bracket',lambda m:m.update(critical_q_lower='1/2',critical_q_upper='3/4',B_critical_lower='7',B_critical_upper='9')),('lost_tail',lambda m:m['tail_fixtures'].pop())]:
  m=copy.deepcopy(a);mutator(m);tests[label]=bool(compare(m,b))
 j={'loop':'h1','status':'accepted' if not fail and all(tests.values()) else 'rejected','failures':fail,'matched_tail_fixtures':16,'executed_mutations':tests,'independence':'Disjoint omitted-class reconstruction agrees with total-minus-selected rational ledger; exact common coordinate tails and physical rescaling agree. Different critical brackets independently contain the same unique monotone budget root.'}
 (R/'advisor/h1-comparison.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j))
 if j['status']!='accepted':raise SystemExit(1)
