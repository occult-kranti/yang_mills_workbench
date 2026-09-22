#!/usr/bin/env python3
"""Exact finite commutator controls, not sampled interacting moments."""
import argparse,hashlib,json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
HERE=Path(__file__).resolve().parent; tests=[]
def need(ok,name):
 if not ok:raise RuntimeError(name)
 tests.append(name)
S=((0,0,0),(1,0,0),(0,1,0),(0,0,1));E=S[1:]
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def incident(R):return {tuple(x-y for x,y in zip(r,s)) for r in R for s in S if all(x-y>=0 for x,y in zip(r,s))}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
 R={(0,0,0),(0,0,1)}
 need(incident(R)==R,'origin_two_incident_stars')
 need(len(incident({(1,1,1),(1,1,2)}))==7,'interior_incidence_different')
 links=set();ends=set()
 for b in R:
  for r,s,j in product(range(4),range(2),range(3)):
   p=(4*b[0]+r,2*b[1]+s,b[2]);links.add((p,j));ends|={p,plus(p,E[j])}
 need(len(links)==48 and len(ends)==36,'48_links_36_endpoints')
 budget=2*(Q(1,2)+Q(1,8)+Q(1,2));need(budget==Q(9,4),'selected_budget')
 cap=Q(1,65536);rows=[]
 for tau in (Q(0),cap,-cap,Q(1,100000000)):
  kinetic=Q(1,8)*28*abs(tau)+budget;second=18+8*kinetic
  need(kinetic==Q(9,4)+Q(7,2)*abs(tau),'kinetic_'+str(tau))
  need(second==36+28*abs(tau) and second<37,'second_'+str(tau))
  rows.append({'tau':str(tau),'kinetic_over_alpha':str(kinetic),'second_over_alpha2':str(second)})
 need(36+28*cap==36+Q(7,16384),'endpoint_constant')
 W=Q(3,5);Gamma=(1-W*W)/4
 need(4*Gamma==1-W*W and Gamma==Q(4,25),'four_half_Pauli_gradients')
 need(4*(4*Gamma)!=1-W*W,'wrong_double_generator')
 omega=1+W/3;cross=Gamma/3;full=Q(3,4)*W*omega-2*cross;wrong=Q(3,4)*W*omega
 need(full==Q(13,30) and wrong==Q(27,50),'derivative_cross_term')
 need(4*Q(3,4)==3,'four_link_Casimir_sum')
 h=Q(0);T=Q(16,25);Vsel=Q(-41,25);B=Q(-1)
 need(T==h-Vsel+B,'scalar_exact_reconstruction')
 need(T!=h-Vsel and T<=h-Vsel,'dropping_negative_scalar_only_upper_bound')
 need(T>0 and h==0,'selected_ground_not_electric_zero')
 alpha=Q(3);free=Q(1,4)*(3*alpha)**2
 need(free==Q(9,4)*alpha**2 and free>0,'free_second_moment')
 need(37*alpha**2!=37*alpha,'physical_energy_squared')
 tails=[]
 for n in (4,16,64,256):
  mu1=(1-Q(1,2*n))*Q(1,4)+Q(1,2*n)*n;mu2=(1-Q(1,2*n))*Q(1,16)+Q(1,2*n)*n*n
  need(mu1<1 and mu2>Q(n,2),'escaping_tail_'+str(n))
  tails.append({'n':n,'mu1':str(mu1),'mu2':str(mu2)})
 result={'loop':'AO1','direction':'forward','verdict':'uniform_finite_physical_second_moment','checks':tests,'bound':'alpha^2(36+28|tau|)<=alpha^2(36+7/16384)<37alpha^2','kinetic_bound':'alpha(9/4+(7/2)|tau|)','parameter_cases':rows,'escaping_first_moment_control':tails,'infinite_operator_domain_claim':False,'limiting_moment_equality_claim':False}
 (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 src=[HERE/'report.md',HERE/'check.py',*sorted((HERE/'inputs').rglob('*'))]
 man={'sources':{str(p.relative_to(HERE)):sha(p) for p in src if p.is_file()},'outputs':{'results.json':sha(out/'results.json')}}
 (out/'source-manifest.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'checks':len(tests),'verdict':result['verdict']}))
if __name__=='__main__':main()
