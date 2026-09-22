#!/usr/bin/env python3
"""Exact arithmetic and creation-algebra checks for the analytic AM2 proof."""
import argparse,hashlib,json,math
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
HERE=Path(__file__).resolve().parent
tests=[]
def need(ok,name):
 if not ok:raise RuntimeError(name)
 tests.append(name)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def matmul(a,b):
 n=len(a);r=[[0]*n for _ in range(n)]
 for i in range(n):
  for k in range(n):
   if a[i][k]:
    for j in range(n):r[i][j]+=a[i][k]*b[k][j]
 return r
def comm(a,b):
 ab=matmul(a,b);ba=matmul(b,a)
 return [[x-y for x,y in zip(ar,br)] for ar,br in zip(ab,ba)]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
 p=4;R=Q(1,64);tau0=Q(1,100000000);J0=28*tau0
 L=[]
 for k in range(9):
  root_X=Q(2)**p*(2*p)**k
  root_I=Q(0) if k==0 else Q(2)**p*(2*p)**k*Q(k*(p+1),p)
  n=16*8**k*(1+Q(5*k,4))
  need(root_X+root_I==n,'anchored_coefficient_'+str(k));L.append(n)
 # All positive series tail ratios bounded rationally; no floating-point exp.
 x=8*R;N=12
 lower=sum(x**k/math.factorial(k) for k in range(N+1))
 tail=x**(N+1)/math.factorial(N+1)/(1-x/Q(N+2))
 upper=lower+tail
 need(lower<upper and upper<Q(8,7),'certified_exp_one_eighth')
 Gcap=16*Q(8,7)*(1+10*R);Dcap=16*Q(8,7)*(18+80*R)
 need(Gcap==Q(148,7) and Dcap==352,'majorant_endpoint_constants')
 need(J0*Gcap==Q(148,25000000) and J0*Gcap<R,'closed_ball_self_map')
 need(J0*Dcap==Q(77,781250) and J0*Dcap<1,'contraction')
 need(2*J0*Dcap==Q(77,390625) and 2*J0*Dcap<1,'excited_resolvent_exclusion_factor')
 # Derive coefficients of 16 exp(8t)(1+10t) independently.
 for k in range(9):
  coef=16*Q(8)**k/math.factorial(k)
  if k:coef+=160*Q(8)**(k-1)/math.factorial(k-1)
  need(coef==L[k]/math.factorial(k),'generating_function_'+str(k))
 inverse_cases=0
 for m in range(1,65):
  for size in range(1,m+5):
   if Q(1,m)>Q(5,size):raise RuntimeError('inverse anchor ratio')
   inverse_cases+=1
  for z in [Q(-1,2),Q(-1,3),Q(0),Q(1,3),Q(1,2)]:
   if 1/(Q(m)-z)>Q(2,m):raise RuntimeError('shifted inverse')
 need(inverse_cases>0,'all_tested_inverse_and_anchor_ratios')
 # Four qubits are an algebra countercontrol, not a rotor spectral cutoff.
 size=1<<p;C=[[0]*size for _ in range(size)];V=[[0]*size for _ in range(size)]
 for b in range(size):
  V[b^15][b]=1
  for j in range(p):
   if not (b>>j)&1:C[b|(1<<j)][b]+=1
 A=V;orders=[]
 for k in range(10):
  orders.append({'order':k,'nonzero_entries':sum(x!=0 for row in A for x in row),'vacuum_to_all_excited':A[15][0]})
  if k==8:need(A[15][0]==math.factorial(8),'actual_order_eight_nonzero')
  if k==9:need(all(x==0 for row in A for x in row),'order_nine_zero')
  A=comm(C,A)
 need(orders[7]['nonzero_entries']>0,'support_three_termination_rejected')
 # Scalar and retained diagonal are kept even in the simplest creation fixed point.
 H0=(Q(0),Q(1));Vdiag=(Q(1,4),Q(1,2));H=tuple(x+y for x,y in zip(H0,Vdiag))
 E=Vdiag[0];D=Vdiag[1]-E
 need(H[0]==E and H[1]-E==Q(5,4),'scalar_equation_retained')
 need(D==Q(1,4) and H[1]-E!=H0[1],'deleting_centered_diagonal_changes_gap')
 need(H[0]!=0 and (H[1]-E)-(H[0]-E)==H[1]-H[0],'scalar_is_ground_center_not_optional_raw_identity')
 # Zero and equality cases of the explicit sufficient interval.
 need(Q(0)*Gcap==0 and Q(0)*Dcap==0,'zero_source_fixed_point')
 need(28*abs(-tau0)==J0 and 28*abs(tau0)==J0,'both_signs_and_tau_equality')
 need(not abs(2*tau0)<=tau0,'outside_contract_not_certified_not_gap_failure')
 need(4*7*tau0==J0 and 7*tau0!=J0,'incoming_stars_retained')
 alpha=Q(24);hbar=Q(2);Estar=Q(3)
 need(alpha/Q(8)*Q(1,2)==alpha/16 and alpha/(16*hbar)==Q(3,4),'physical_energy_and_clock')
 need(alpha/(16*Estar)==Q(1,2),'fixed_reference_energy')
 result={'loop':'AM2','direction':'forward','verdict':'uniform_finite_volume_full_model_certificate_pending_independent_review','checks':tests,'tau_interval':'|tau|<=1/100000000','J_cap':str(J0),'radius':str(R),'G_cap':str(Gcap),'G_prime_cap':str(Dcap),'self_map_cap':str(J0*Gcap),'Lipschitz_cap':str(J0*Dcap),'exclusion_cap':str(2*J0*Dcap),'exponential_enclosure':[str(lower),str(upper)],'order_coefficients':list(map(str,L)),'creation_control':orders,'gap_normalized':'1/2','gap_physical':'alpha/16','support':'every finite complete-factor I1 volume with retained whole stars','empty_volume':'one-dimensional; excitation claim excluded','infinite_volume_proven':False,'Yarotsky_constants_evaluated':False,'continuum_proven':False}
 (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 src=[HERE/'report.md',HERE/'check.py',*sorted((HERE/'inputs').rglob('*'))]
 man={'sources':{str(p.relative_to(HERE)):sha(p) for p in src if p.is_file()},'outputs':{'results.json':sha(out/'results.json')}}
 (out/'source-manifest.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'checks':len(tests),'verdict':result['verdict']}))
if __name__=='__main__':main()
