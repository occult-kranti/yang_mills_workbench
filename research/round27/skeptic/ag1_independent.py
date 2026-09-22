#!/usr/bin/env python3
"""Independent exact algebra and norm-budget tests for the frozen single AG1 update."""
from fractions import Fraction as F
from math import factorial
from itertools import product
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
checks=[]
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
 checks.append(msg)
def add(A,B):return [[a+b for a,b in zip(ra,rb)] for ra,rb in zip(A,B)]
def scale(c,A):return [[c*a for a in r] for r in A]
def mul(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def comm(A,B):return add(mul(A,B),scale(-1,mul(B,A)))
def trans(A):return list(map(list,zip(*A)))
def zero(n):return [[F(0) for j in range(n)] for i in range(n)]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def fgeom(z):return (4-z)/(1-z)**2
rho=F(9,4);delta=F(1,10);T=F(3)
need(1/(1-delta)<rho/2,'rational exp(delta) upper bound fits rho/2')
need(F(16,9)*F(7,12)**3<F(4,9),'actual cubic coefficient below rational two-thirds')
a_coef=4*rho**4
budgets=[]
for M in (F(1,1000),F(1,10000)):
 tau=M/7;r_cap=F(2,3)*tau**3;zeta=26*M*rho**3*T
 need(0<zeta<1,'strong connected-word tail converges '+str(M))
 s_coef=rho**4*fgeom(zeta);r_coef=s_coef
 s_cap=s_coef*r_cap;x=2*s_cap/delta
 need(x<1,'all nested commutator series converges '+str(M))
 nonlinear_coef=x/(1-x)*(a_coef+r_coef/2)
 transported_E_factor=1/(1-x)
 original_zeta=208*M*T
 positive_tail_coef=F(16,3)*(fgeom(original_zeta)-4)
 improved_residual_coef=F(256,9)+positive_tail_coef
 contraction_upper=F(4,9)+(positive_tail_coef+nonlinear_coef)/16
 # Actual input norm >=16 r*, since any four-site term contributes16||A_b|| at one of its roots.
 if M==F(1,10000):
  need(improved_residual_coef<31,'narrow residual upper budget below31 rstar')
  need(contraction_upper<F(61,100),'narrow selected off-diagonal norm contracts below0.61')
 else:
  need(positive_tail_coef>F(80,9),'main-range free-plus-positive tail fails this contraction certificate')
 budgets.append({'M':M,'tau_abs':tau,'rstar_rational_cap':r_cap,'rho_zeta':zeta,'strong_S_R_coefficient':s_coef,'strong_A_coefficient':a_coef,'commutator_parameter':x,'nonlinear_bound_per_rstar':nonlinear_coef,'conditional_E_transport_factor':transported_E_factor,'positive_D_tail_per_rstar':positive_tail_coef,'residual_upper_budget_per_rstar':improved_residual_coef,'selected_source_contraction_upper':contraction_upper})
# Exact formal matrix diagnostic for e^(tS)(G+tA)e^(-tS), never replacing physical Hilbert spaces.
G=[[F(0),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(3)]]
S=[[F(0),F(1,5),F(1,7)],[-F(1,5),F(0),F(1,11)],[-F(1,7),-F(1,11),F(0)]]
A=[[F(0),F(2,5),F(1,3)],[F(2,5),F(1,4),F(0)],[F(1,3),F(0),-F(1,4)]]
R=add(comm(S,G),A)
need(trans(S)==scale(-1,S),'diagnostic generator skew-adjoint')
need(trans(A)==A and trans(R)==R,'diagnostic input and residual self-adjoint')
N=9;powers=[eye(3)]
for n in range(N):powers.append(mul(powers[-1],S))
exact=[]
for n in range(N+1):
 C=zero(3)
 for i in range(n+1):
  j=n-i;C=add(C,scale(F((-1)**j,factorial(i)*factorial(j)),mul(mul(powers[i],G),powers[j])))
 if n>=1:
  for i in range(n):
   j=n-1-i;C=add(C,scale(F((-1)**j,factorial(i)*factorial(j)),mul(mul(powers[i],A),powers[j])))
 exact.append(C)
need(exact[0]==G and exact[1]==R,'exact selected-source first-order identity')
for n in range(2,N+1):
 k=n-1;C=add(scale(k,A),R)
 for _ in range(k):C=comm(S,C)
 need(exact[n]==scale(F(1,factorial(k+1)),C),'full BCH coefficient '+str(n))
wrong=scale(F(1,2),comm(S,add(R,scale(-1,A))))
need(exact[2]!=wrong,'G-only BCH omits A conjugation')
need(exact[1]!=zero(3),'dropping nonzero residual fails')
P=[[F(1),F(0),F(0)],[F(0),F(0),F(0)],[F(0),F(0),F(0)]];Q=add(eye(3),scale(-1,P))
for n in range(1,N+1):
 B=exact[n];c=B[0][0];off=add(mul(mul(P,B),Q),mul(mul(Q,B),P));diag=mul(mul(Q,add(B,scale(-c,eye(3)))),Q)
 need(add(add(scale(c,eye(3)),off),diag)==B,'all-term scalar/diagonal/source reconstruction '+str(n))
 need(mul(diag,P)==zero(3),'updated relative diagonal annihilates local vacuum '+str(n))
E=[[F(1),F(0),F(0)],[F(0),F(2),F(0)],[F(0),F(0),F(4)]]
need(comm(S,E)!=zero(3),'additional E transport cannot be deleted')
# Complete star incidence and finite volume denominator controls.
star={(0,0,0),(1,0,0),(0,1,0),(0,0,1)}
diffs={tuple(a-b for a,b in zip(x,y)) for x in star for y in star}
need(len(diffs)==13,'full star difference set13')
need(len(diffs-{(0,0,0)})==12,'twelve interior crossings')
need(sum(min(d)>=0 for d in diffs)-1==3,'positive origin has only three crossings')
for extent in (1,2,3):
 anchors=list(product(range(extent),repeat=3));counts={}
 for b in anchors:
  for s in star:
   x=tuple(a+c for a,c in zip(b,s));counts[x]=counts.get(x,0)+1
 inputnorm=16*max(counts.values())
 need(inputnorm>=16,'actual nonempty source-family norm lower16rstar '+str(extent))
 if extent==1:need(inputnorm==16 and inputnorm!=64,'small volume64rstar denominator rejected')
 if extent>=2:need(inputnorm==64,'interior four-star norm attained '+str(extent))
# Weight2 alone does not control first support moment: one n-site term of norm2^-n has rooted norm1 and momentn.
for n in (1,8,64):need(F(2)**n*F(1,2**n)==1 and n*F(2)**n*F(1,2**n)==n,'support-moment obstruction '+str(n))
for sign in (-1,0,1):
 tau=sign*F(1,7000);r_cap=F(2,3)*abs(tau)**3
 need(r_cap>=0,'both signs cubic norm bound '+str(sign))
 if sign==0:need(r_cap==0,'zero coupling no divided source norm')
# Explicit exact geometric derivative tail identity coefficient check, no sampled convergence claim.
for z in (F(0),F(39,625),F(78,125)):
 partial=sum((4+3*n)*z**n for n in range(21))
 rem=z**21*((4+3*21)/(1-z)+3*z/(1-z)**2)
 need(partial+rem==fgeom(z),'complete positive tail identity '+str(z))
def clean(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,list):return [clean(y) for y in x]
 if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
 return x
result={'schema':'ym27-independent-ag1-v1','status':'PASS','checks':checks,'check_count':len(checks),'scope':'All-order analytic norm argument checked with exact budget algebra; finite matrices only formal coefficient/bookkeeping diagnostics. Actual inherited unbounded domains remain proof premises.','budgets':budgets,'contraction_note':'For selected-source update only, with rstar actual supremum and local source projection norm at most1; not all-stage iteration or full original Hamiltonian.','contract_sha256':hashlib.sha256((ROOT/'research/round27/contracts/ag1.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'ag1-independent.json').write_text(json.dumps(clean(result),indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks),'budgets':[{'M':str(x['M']),'S_R_coeff':float(x['strong_S_R_coefficient']),'x':float(x['commutator_parameter']),'N_over_rstar':float(x['nonlinear_bound_per_rstar']),'residual_budget_over_rstar':float(x['residual_upper_budget_per_rstar']),'source_contraction_upper':float(x['selected_source_contraction_upper'])} for x in budgets]}))
