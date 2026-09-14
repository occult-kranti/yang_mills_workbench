#!/usr/bin/env python3
import json,pathlib
from fractions import Fraction as F
R=pathlib.Path(__file__).resolve().parents[1]
def compare(a,b):
 failures=[]
 for x,y in zip(a['fixtures'],b['rows']):
  for ak,bk in [('L','L'),('completed_links','closed_links'),('factors','factor_count'),('omitted_faces','faces'),('raw_links','initial_links'),('retained_weight','retained_weight'),('tail_weight','tail')]:
   if x[ak]!=y[bk]: failures.append(f"L{x['L']}:{ak}")
  if F(y['epsilon_over_E_star'])!=2*F(x['epsilon_over_E_star']):failures.append('alpha scale translation')
  if F(y['resolvent_dimensionless_bound'])!=8*F(x['resolvent_bound_times_E_star']):failures.append('Im z scale translation')
 if len(a['fixtures'])!=9 or len(b['rows'])!=9:failures.append('incomplete fixtures')
 if not all(a['controls'].values()) or not all(c['passed'] for c in b['controls']): failures.append('control failure')
 return failures
if __name__=='__main__':
 a=json.loads((R/'forward/d1/output/results.json').read_text());b=json.loads((R/'reverse/d1/output/results.json').read_text());failures=compare(a,b)
 import copy
 m=copy.deepcopy(a);m['fixtures'][0]['tail_weight']='0';tail_rejected=bool(compare(m,b))
 m=copy.deepcopy(a);m['fixtures'][0]['completed_links']-=1;support_rejected=bool(compare(m,b))
 result={'loop':'d1','status':'accepted' if not failures and tail_rejected and support_rejected else 'rejected','compared_rows':9,'compared_fields_per_row':9,'failures':failures,'executed_mutations':{'wrong_tail_rejected':tail_rejected,'missing_completed_link_rejected':support_rejected},'independence':'Forward total-minus-selected versus reverse direct omitted classes; distinct scale fixtures translated explicitly.'}
 (R/'advisor/d1-comparison.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
 if result['status']!='accepted': raise SystemExit(1)
