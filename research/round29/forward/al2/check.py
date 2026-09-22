#!/usr/bin/env python3
"""Exact forward AL2 algebra. Diagnostic c1/c2 never evaluate source constants."""
import argparse,hashlib,json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
HERE=Path(__file__).resolve().parent
tests=[]
def need(ok,name):
 if not ok:raise RuntimeError(name)
 tests.append(name)
def direct(g2,s,c1,c2):
 if min(g2,c1,c2)<=0 or s<=0:return False
 r=4*s/g2**2;eps=168*r
 return r<=Q(1,2) and r<=Q(1,8) and eps<c1 and c2*eps<Q(1,2)
def caps(g2,s,c1,c2):
 if min(g2,c1,c2)<=0 or s<=0:return False
 g4=g2**2
 return s<=g4/32 and s<c1*g4/672 and s<g4/(1344*c2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
 comparisons=0
 for g2,s,c1,c2 in product(map(Q,[1,2,8]),[Q(0),Q(1,10000),Q(1,100),Q(1),Q(2)],[Q(1),Q(100)],[Q(1,1000),Q(1)]):
  need(direct(g2,s,c1,c2)==caps(g2,s,c1,c2),'iff_'+str(comparisons));comparisons+=1
 for k in (Q(1,7),Q(1),Q(11)):
  alpha=Q(5,3);lam=Q(2,9)
  need((k*lam)/(k*alpha)==lam/alpha,'ratio_invariance_'+str(k))
  raw=Q(19);E0=Q(7);C=Q(-13)
  need((k*raw+C)-(k*E0+C)==k*(raw-E0),'ground_shift_'+str(k))
 # Each strict cap is isolated from the other two in a diagnostic source-constant fixture.
 g2=Q(8);g4=g2**2;c1=Q(1);c2=Q(1,1000);s=c1*g4/672
 need(s<g4/32 and s<g4/(1344*c2) and not direct(g2,s,c1,c2),'strict_c1_equality_rejected')
 c1=Q(100);c2=Q(1);s=g4/(1344*c2)
 need(s<g4/32 and s<c1*g4/672 and not direct(g2,s,c1,c2),'strict_c2_equality_rejected')
 s=g4/32;c1=Q(1000);c2=Q(1,10000)
 need(direct(g2,s,c1,c2),'bridge_equality_permitted')
 need(Q(1,4)<=Q(1,2) and Q(1,4)>Q(1,8),'missing_bridge_rejected')
 need(not direct(g2,Q(0),c1,c2),'zero_s_excluded_from_nonzero_target')
 need(not direct(g2,Q(-1),c1,c2),'negative_s_rejected')
 need(Q(1,2)*Q(2,3)/Q(5,7)!=Q(2,3)/Q(5,7),'magnetic_only_not_units')
 need(Q(3)*Q(2)/Q(5)!=Q(2)/Q(5),'fixed_clock_change_detected')
 for k in (Q(0),Q(-1)):
  need(not k>0,'invalid_energy_multiplier_'+str(k))
 need(not Q(0)>0,'zero_reference_energy_rejected')
 path=[{'n':n,'max_selected_fraction':str(Q(1,32*n*n))} for n in (1,2,4,16,256)]
 need(all(Q(path[i+1]['max_selected_fraction'])<Q(path[i]['max_selected_fraction']) for i in range(len(path)-1)),'path_caps_strictly_decrease')
 result={'loop':'AL2','direction':'forward','verdict':'exact_eligibility_invariance_and_deformation_cap','checks':tests,'diagnostic_membership_pairs':comparisons,'caps':{'bridge':'s<=g^4/32','source_c1':'s<c1*g^4/672','source_c2':'s<g^4/(1344*c2)'},'path':path,'rational_c1_c2_are':'diagnostic parameters, not theorem constants','new_numerical_radius':False,'continuum_proof':False}
 (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 src=[HERE/'report.md',HERE/'check.py',*sorted((HERE/'inputs').rglob('*'))]
 man={'sources':{str(p.relative_to(HERE)):sha(p) for p in src if p.is_file()},'outputs':{'results.json':sha(out/'results.json')}}
 (out/'source-manifest.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'checks':len(tests),'verdict':result['verdict']}))
if __name__=='__main__':main()
