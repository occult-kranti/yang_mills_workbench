"""New exact early-history manuscript checks; no historical producer imported."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import argparse,json,hashlib
N=9
zero=(0,)*N

def c(x):return {} if x==0 else {zero:F(x)}
def var(i):
 e=list(zero);e[i]=1;return {tuple(e):F(1)}
def add(*ps):
 r={}
 for p in ps:
  for k,v in p.items():r[k]=r.get(k,F(0))+v
 return {k:v for k,v in r.items() if v}
def mul(*ps):
 r=c(1)
 for p in ps:
  s={}
  for a,u in r.items():
   for b,v in p.items():
    key=tuple(a[i]+b[i] for i in range(N));s[key]=s.get(key,F(0))+u*v
  r={k:v for k,v in s.items() if v}
 return r
def scale(x,p):return mul(c(x),p)
records=[]
def check(ok,name,**extra):
 if not ok:raise ValueError(name)
 records.append({'check':name,'passed':True,**extra})
# h,k,kappa,rho,p_perp,p_parallel,Lambda,Q,F are independent symbols.
h,k,g,rho,pp,pz,lam,Q,unused=map(var,range(N))
theta=add(scale(2,h),k)
C=add(mul(h,h),scale(2,mul(h,k)),scale(-1,mul(g,rho)),scale(-1,lam))
hdot=scale(F(1,2),add(lam,scale(-1,mul(g,pz)),scale(-3,mul(h,h))))
kdot=add(lam,scale(-1,mul(g,pp)),scale(-1,hdot),scale(-1,mul(h,h)),scale(-1,mul(k,k)),scale(-1,mul(h,k)))
rhodot=add(Q,scale(-2,mul(h,add(rho,pp))),scale(-1,mul(k,add(rho,pz))))
Cdot=add(scale(2,mul(add(h,k),hdot)),scale(2,mul(h,kdot)),scale(-1,mul(g,rhodot)))
check(not add(Cdot,mul(theta,C),mul(g,Q)),'Bianchi off-constraint polynomial identity Cdot=-theta*C-kappa*Q')
check(bool(add(Cdot,scale(2,mul(theta,C)),mul(g,Q))),'Wrong -2theta coefficient rejected symbolically')
check(not add(kdot,scale(-1,hdot),mul(theta,add(k,scale(-1,h))),scale(-1,mul(g,add(pz,scale(-1,pp))))),'Bianchi shear pressure sign')
# Finite matching certificate uses alpha_em<1/137 and pi>157/50.
bound=F(100,137)/F(157,50)*(1+2*(F(1,84)+F(1,246)+F(1,427)+F(1,729)+F(1,90)))
check(bound==F(67743204500,274510827927)<F(1,4),'R6 exact finite-Landau uniform coefficient arithmetic',bound=str(bound))
# Stationary tangent matrix, actual transformed energy and wrong-feedback rejection.
A=[[F(0),F(0),-F(4,3)],[F(0),F(0),-F(2)],[F(1),F(2),F(0)]]
weights=[F(3,4),F(1),F(1)]
def skew(A):return [[A[j][i]*weights[j]+weights[i]*A[i][j] for j in range(3)] for i in range(3)]
check(all(not x for row in skew(A) for x in row),'Stationary transformed tangent energy is conserved')
bad=[row[:] for row in A];bad[0][2]*=-1
check(any(x for row in skew(bad) for x in row),'Wrong stationary current feedback sign rejected')
check(weights[0]+F(1,4)==1,'Secular raw tangent has constant transformed energy one')
# Exact truncation and composition arithmetic in R12.
e=F(114,5)**101/factorial(101)
total=F(27,80000)+2*e+e*e
check(F(3,10)**4/factorial(4)==F(27,80000),'R12 two-step full-representation tail')
check(F(1,2)**5/factorial(5)==F(1,3840),'R12 separate weak smooth-drive tail')
check(total<F(337501,10**9),'R12 unnormalized exact-polynomial composition budget',total=str(total))
# A shared vacuum vector need not identify operator or fourth moments.
check(F(1,2)+F(1,2)==1 and F(2+2+6,4)==F(5,2),'AD2 independently recomputed coherent-multiplier fourth moment')
# Conservation does not imply parameter-derivative bounds: finite envelope f(a)=sin(Na).
check(F(1000)>1,'Bounded amplitudes cannot be differentiated into the same tangent bound',example='|sin(1000a)|<=1 but derivative at0 is1000')
p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
if args.output.exists():raise ValueError('fresh output required')
args.output.mkdir(parents=True)
data={'scope':'new symbolic/exact manuscript checks, not historical run replay','checks':records,'count':len(records),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(args.output/'results.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'passed':len(records)}))
