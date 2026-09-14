#!/usr/bin/env python3
import copy,json,pathlib
from fractions import Fraction as F
R=pathlib.Path(__file__).resolve().parents[1]
def compare(a,b):
 fail=[];by={(x['kappa'],x['c_over_E_star']):x for x in a['fixtures']}
 for y in b['rows']:
  x=by[(y['kappa'],y['c/E_star'])]
  if x['correct_adjoint_residual_over_rho']!='0' or x['wrong_drift_adjoint_residual_over_rho']!=y['wrong_drift_stationarity_residual_over_rho']:fail.append('stationarity')
  if F(y['kappa'])==0 and F(x['exact_gap_at_kappa_zero'])!=F(3,4)*F(y['c/E_star']):fail.append('gap scaling')
  if y['static_depends_on_c'] is not False:fail.append('static underidentification')
 if a['free_gap']!='3/4' or b['action_checks']['DeltaS_identity']!='-27/4':fail.append('metric/action')
 if not all(a['controls'].values()) or not all(x['passed'] for x in b['controls']):fail.append('controls')
 return fail
if __name__=='__main__':
 a=json.loads((R/'forward/f1/output/results.json').read_text());b=json.loads((R/'reverse/f1/output/results.json').read_text());fail=compare(a,b);m=copy.deepcopy(b);m['rows'][0]['static_depends_on_c']=True;bad=bool(compare(a,m))
 j={'loop':'f1','status':'accepted' if not fail and bad else 'rejected','matched_signed_kappa_c_fixtures':6,'failures':fail,'executed_mutations':{'false_static_rate_dependence_rejected':bad},'independence':'Closed-form/weighted variational route and reverse stationary-adjoint reconstruction; same physical time convention.'};(R/'advisor/f1-comparison.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j))
 if j['status']!='accepted':raise SystemExit(1)
