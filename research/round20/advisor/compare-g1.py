#!/usr/bin/env python3
import json,pathlib,copy
from fractions import Fraction as F
R=pathlib.Path(__file__).resolve().parents[1]
def tail(m):
 S=2*(1-F(1,2**(m+1)));Y=F(4,3)*(1-F(1,4**(m//2+1)));X=F(2,15)*(1-F(1,16**((m+1)//4)))
 return F(107,135)-(2*S**3+S*(S-Y)*S+X*Y*S)/24
def compare(a,b):
 fail=[]
 for x in a['time_tail_fixtures']:
  if F(x['epsilon_over_alpha'])!=tail(x['M'])/64 or F(x['unit_A_error'])!=4*abs(F(x['time_alpha_over_hbar']))*tail(x['M'])/64:fail.append('forward time error')
 for x in b['rows']:
  if F(x['operator_error_over_A_norm'])!=8*abs(F(x['t_in_hbar_over_E_star']))*abs(F(x['tau']))*tail(x['M']):fail.append('reverse time error')
 for x in a['character_shift_fixtures']:
  if F(x['time_over_pi_hbar_over_alpha'])*F(x['increment_over_alpha'])!=1 or x['norm_difference']!='2':fail.append('character phase')
 for x in b['character_shift']:
  if F(x['t_n_alpha_over_pi_hbar'])*F(x['spacing_over_alpha'])!=1 or x['operator_norm_difference']!='2':fail.append('reverse character phase')
 if not all(a['controls'].values()) or not all(x['passed'] for x in b['controls']):fail.append('controls')
 return fail
if __name__=='__main__':
 a=json.loads((R/'forward/g1/output/results.json').read_text());b=json.loads((R/'reverse/g1/output/results.json').read_text());fail=compare(a,b);m=copy.deepcopy(a);m['character_shift_fixtures'][0]['norm_difference']='0';bad=bool(compare(m,b))
 j={'loop':'g1','status':'accepted' if not fail and bad else 'rejected','forward_time_rows':len(a['time_tail_fixtures']),'reverse_time_rows':len(b['rows']),'failures':fail,'executed_mutations':{'false_norm_time_continuity_rejected':bad},'independence':'Domain-safe Duhamel reconstructed from each direction; exact different-unit time ledgers and actual SU2 spectral increments checked.'};(R/'advisor/g1-comparison.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j))
 if j['status']!='accepted':raise SystemExit(1)
