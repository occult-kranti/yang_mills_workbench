#!/usr/bin/env python3
import copy,json,pathlib
from fractions import Fraction as F
R=pathlib.Path(__file__).resolve().parents[1]
def B(q):return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def compare(a,b):
 fail=[]
 if a['exact_variance_formula']!='alpha^2*tau(q)^2*B(q^2)/96' or b['exact_sigma_identity']!='alpha^2*tau^2*B(q^2)/96':fail.append('exact variance equation')
 if a['canonical_variance_scaled_limit']!='eta^2/5376' or b['asymptotic_sigma2_over_alpha2_eta2_one_minus_q_cubed']!='1/5376':fail.append('variance asymptotic')
 if a['canonical_projector_squared_scaled_limit']!=b['asymptotic_projector_squared_coefficient'] or a['canonical_projector_squared_scaled_limit']!='eta^2/[84(1-eta)^2]':fail.append('projector asymptotic')
 if a['proved_universal_factor_overlap_degree']!=b['geometry']['universal_overlap_bound'] or a['proved_universal_factor_overlap_degree']!=160:fail.append('general overlap proof')
 if a['max_shared_links']!=1 or a['distinct_face_pairs_checked']!=a['faces_checked']*(a['faces_checked']-1)//2:fail.append('pair completeness')
 ar={(x['q'],x['eta']):x for x in a['ray_fixtures']};br={(x['q'],x['eta']):x for x in b['rows']};common=ar.keys()&br.keys()
 if len(common)!=12:fail.append('common ray coverage')
 for key in common:
  x,y=ar[key],br[key];q,eta=map(F,key);tau=eta/(8*B(q));g=(1-eta)/8;sigma2=tau*tau*B(q*q)/96
  expected={'tau':tau,'B':B(q),'g_bar_over_alpha':g,'variance_over_alpha_squared':sigma2,'operator_norm_over_alpha':eta/8,'projector_error_squared':min(F(1),sigma2/g**2),'energy_lower_over_alpha':-sigma2/g}
  if any(F(x[k])!=v for k,v in expected.items()):fail.append('forward exact ray '+str(key))
  for ak,bk,scale in [('variance_over_alpha_squared','exact_sigma_squared_over_E_star_squared',4),('g_bar_over_alpha','g_bar_over_E_star',2),('operator_norm_over_alpha','operator_norm_over_E_star',2),('projector_error_squared','projector_norm_squared_upper',1),('energy_lower_over_alpha','negative_ground_energy_bound_over_E_star',-2)]:
   if scale*F(x[ak])!=F(y[bk]):fail.append('physical rescaling '+str((key,ak)))
 if not all(a['controls'].values()) or not all(x['passed'] for x in b['controls']):fail.append('controls')
 return fail
if __name__=='__main__':
 a=json.loads((R/'forward/h2/output/results.json').read_text());b=json.loads((R/'reverse/h2/output/results.json').read_text());fail=compare(a,b);tests={}
 def coherent_variance(m):
  for x in m['ray_fixtures']:
   for k in ['variance_over_alpha_squared','projector_error_squared','energy_lower_over_alpha']:x[k]=str(2*F(x[k]))
 for label,mutator in [('coherent_false_variance',coherent_variance),('fixture_degree_as_universal',lambda m:m.update(proved_universal_factor_overlap_degree=m['observed_max_factor_overlap_degree'])),('false_pair_completeness',lambda m:m.update(distinct_face_pairs_checked=m['distinct_face_pairs_checked']-1))]:
  m=copy.deepcopy(a);mutator(m);tests[label]=bool(compare(m,b))
 j={'loop':'h2','status':'accepted' if not fail and all(tests.values()) else 'rejected','failures':fail,'matched_physical_ray_fixtures':12,'executed_mutations':tests,'independence':'Separate coordinate/factor construction and conditional Haar proofs agree on exact off-diagonal cancellation, diagonal1/4, varianceB(q²)/96, spectral consequences and physical rescaling. Variance target originated in the separately assigned audit; both directions reconstructed it independently.'}
 (R/'advisor/h2-comparison.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j))
 if j['status']!='accepted':raise SystemExit(1)
