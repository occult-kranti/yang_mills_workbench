#!/usr/bin/env python3
import copy,json,pathlib,importlib.util
from fractions import Fraction as F
R=pathlib.Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('f2_reverse',R/'reverse/f2/check.py');rev=importlib.util.module_from_spec(sp);sp.loader.exec_module(rev)
def expected_coeffs():
 d={'1':F(15,4),'x':F(1,2),'y':F(2),'z':F(1,2),'r':F(1,2)}
 for l in [{'x':3,'w':1},{'y':1,'w':1,'t':1},{'z':1,'t':1}]:
  for p,a in l.items():
   for q,b in l.items():
    key=p+'^2' if p==q else '*'.join(sorted([p,q],key=lambda v:'xyzwt'.index(v)))
    d[key]=d.get(key,F(0))-F(a*b,4)
 return {k:str(v) for k,v in d.items() if v}
def compare(a,b):
 fail=[]
 if a['GammaS_coefficients']!=expected_coeffs():fail.append('full symbolic Gamma coefficient tensor')
 if a['action_range']!=['-5','7'] or b['exact_range']!=['-5','7'] or a['action_oscillation']!='12' or b['oscillation']!='12':fail.append('exact range')
 for x in [a['exp_3_over_2_upper'],b['exponential_upper_3over2']]:
  if not rev.exp_upper(F(3,2),80)<=F(x)<F(9,2):fail.append('outward exponential envelope')
 if a['gap_lower_over_c']!='1/6':fail.append('gap')
 if any(x['ground_residual_over_c_psi']!='0' for x in b['rows']):fail.append('ground residual')
 if not all(a['controls'].values()) or not all(x['passed'] for x in b['controls']):fail.append('controls')
 return fail
if __name__=='__main__':
 a=json.loads((R/'forward/f2/output/results.json').read_text());b=json.loads((R/'reverse/f2/output/results.json').read_text());fail=compare(a,b);m=copy.deepcopy(a);m['GammaS_coefficients'].pop('r');bad=bool(compare(m,b))
 j={'loop':'f2','status':'accepted' if not fail and bad else 'rejected','full_symbolic_coefficients_compared':len(expected_coeffs()),'failures':fail,'executed_mutations':{'deleted_shared_middle_r_rejected':bad},'independence':'Projected gradients and explicit left-invariant derivatives; extremum derivative proof versus exact squared tangent bounds; independent outward exponential certificates.'};(R/'advisor/f2-comparison.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps(j))
 if j['status']!='accepted':raise SystemExit(1)
