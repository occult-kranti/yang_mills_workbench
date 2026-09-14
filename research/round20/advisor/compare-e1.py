#!/usr/bin/env python3
import copy,json,pathlib
from fractions import Fraction as F
R=pathlib.Path(__file__).resolve().parents[1]
def compare(a,b):
 fail=[]
 if len(a['fixtures'])!=4 or len(b['rows'])!=4:fail.append('incomplete')
 for x,y in zip(a['fixtures'],b['rows']):
  for p,q in [('N','N'),('faces','faces'),('free_links','free_factors'),('links','links'),('omitted_faces','omitted_faces'),('strips','strips'),('retained_weight','retained_weight'),('tail_weight','tail'),('projector_error','projector_bound'),('unit_observable_error','observable_over_norm_bound')]:
   if x[p]!=y[q]:fail.append(f"N{x['N']}:{p}")
  if 2*F(x['epsilon_over_alpha'])!=F(y['epsilon_over_E_star']):fail.append('energy scales')
 if not all(a['controls'].values()) or not all(x['passed'] for x in b['controls']):fail.append('controls')
 return fail
if __name__=='__main__':
 a=json.loads((R/'forward/e1/output/results.json').read_text());b=json.loads((R/'reverse/e1/output/results.json').read_text());fail=compare(a,b);m=copy.deepcopy(a);m['fixtures'][0]['strips']+=1;bad=bool(compare(m,b))
 result={'loop':'e1','status':'accepted' if not fail and bad else 'rejected','compared_rows':4,'failures':fail,'executed_mutations':{'wrong_strip_count_rejected':bad},'independence':'Literal geometry and orientation-specific weighted sums derived by independent selected/complement classes.'}
 (R/'advisor/e1-comparison.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
 if result['status']!='accepted':raise SystemExit(1)
