#!/usr/bin/env python3
"""Independent omitted-class rational profile and finite-tail H1 ledger."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent

def validq(q):
 if isinstance(q,bool):raise ValueError('q must be a profile, not boolean')
 q=F(q)
 if not 0<q<1:raise ValueError('summable profile requires 0<q<1')
 return q

def budget(q):
 q=validq(q)
 classes=[2/(1-q)**3,q/((1-q)**2*(1-q*q)),q**3/((1-q)*(1-q*q)*(1-q**4))]
 return sum(classes,F(0))/24

def total_minus_selected(q):
 q=validq(q)
 return (3/(1-q)**3-(1+q+q*q)/((1-q**4)*(1-q*q)*(1-q)))/24

def retained(q,L):
 q=validq(q)
 if type(L) is not int or L<0:raise ValueError('independent nonnegative integer L required')
 S=(1-q**(L+1))/(1-q);Y=(1-q**(2*(L//2+1)))/(1-q*q);X=q**3*(1-q**(4*((L+1)//4)))/(1-q**4)
 return (2*S**3+S*(S-Y)*S+X*Y*S)/24

def direct(q,L):
 return sum((q**(x+y+z)/24 for a,b in [(0,1),(0,2),(1,2)] for x in range(L+1) for y in range(L+1) for z in range(L+1) if (a,b)!=(0,1) or y%2==1 or x%4==3),F(0))
def gap(q,tau,alpha=F(2),E=F(1)):
 if E<=0 or alpha<=0:raise ValueError('positive physical scale required')
 return alpha/E*(F(1,8)-abs(tau)*budget(q))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 rows=[]
 for q in [F(1,4),F(1,2),F(3,4),F(7,8)]:
  B=budget(q)
  if B!=total_minus_selected(q):raise RuntimeError('independent rational routes disagree')
  for L in [0,1,2,4,8]:
   W=retained(q,L);T=B-W
   if W!=direct(q,L) or T<=0:raise RuntimeError('finite exact sum mismatch')
   rows.append({'q':str(q),'L':L,'B':str(B),'retained':str(W),'tail':str(T),'default_gap_floor_over_E_star':str(gap(q,F(1,64))),'default_certificate_positive':gap(q,F(1,64))>0})
 # Exact 10^-4 bracket. Monotonicity is proved analytically in the report.
 lo,hi=1,9999
 while hi-lo>1:
  mid=(lo+hi)//2
  if budget(F(mid,10000))<8:lo=mid
  else:hi=mid
 bracket={'lower':str(F(lo,10000)),'upper':str(F(hi,10000)),'B_lower':str(budget(F(lo,10000))),'B_upper':str(budget(F(hi,10000))),'classification':'unique boundary of sufficient default-tau certificate only'}
 if not budget(F(lo,10000))<8<budget(F(hi,10000)):raise RuntimeError('bracket not strict')
 controls=[]
 def ck(name,value):
  if not value:raise RuntimeError(name)
  controls.append({'name':name,'passed':True})
 # Cleared common-denominator polynomial: two routes equal coefficientwise.
 D=[1,2,2,2,1]
 cls=[2*d for d in D]
 for i,v in enumerate([0,1,1,2,1]):cls[i]+=v
 tot=[3*d for d in D]
 for i in range(3):tot[i]-=1
 ck('rational_function_identity_coefficientwise',cls==tot==[2,5,5,6,3])
 ck('dyadic_regression',budget(F(1,2))==F(107,135))
 ck('changed_q_rejects_fixed_dyadic_budget',budget(F(3,4))!=F(107,135))
 ck('asymptotic_coefficient_exact',F(sum(cls),24*sum(D))==F(7,64))
 ck('signed_amplitude_absolute',gap(F(1,2),F(-1,64))==gap(F(1,2),F(1,64)))
 ck('finite_q1_sum_not_infinite_budget',direct(F(1),4)>direct(F(1),2))
 for name,fn in [('q1',lambda:budget(F(1))),('q0',lambda:budget(F(0))),('zero_E',lambda:gap(F(1,2),F(1,64),E=F(0)))]:
  try:fn()
  except ValueError:ck(name+'_rejected',True)
  else:raise RuntimeError(name+' admitted')
 bad=gap(F(7,8),F(1,64));ck('insufficient_certificate_retained',bad<0)
 data={'schema':'ym20-reverse-h1-v1','status':'passed','rows':rows,'controls':controls,'critical_default_tau_bracket':bracket,'asymptotic_normalized_budget':'7/64','proof_route_status':'negative lower certificate is insufficient, not physical gap closed','parameter_q':'continuous action-profile deformation independent of L and E_star','scope':'fixed selected-strip reference, summable q<1 only'}
 p=out/'results.json';p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round20/contracts/h1.json',ROOT/'research/round20/advisor/g2-gate.json']
 (out/'source-manifest.json').write_text(json.dumps({'sources':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'outputs':{'results.json':hashlib.sha256(p.read_bytes()).hexdigest()}},indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'passed','rows':len(rows),'controls':len(controls),'critical_bracket':[bracket['lower'],bracket['upper']]}))
if __name__=='__main__':main()
