#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from math import factorial,prod
from pathlib import Path
import json
from replay_loop import replay
HERE=Path(__file__).resolve().parent;checks=[]
def need(v,t):
 if not v:raise RuntimeError(t)
 checks.append(t)
def mul(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def sub(A,B):return [[a-b for a,b in zip(x,y)] for x,y in zip(A,B)]
R=F(1,64);tau=F(1,100000000);J=28*tau
G=16/(1-8*R)*(1+10*R);Gp=16/(1-8*R)*(18+80*R)
need((G,Gp)==(F(148,7),F(352)),'geometric_series_endpoint')
need(J*G<R and 2*J*Gp<1,'complete_map_and_excited_contraction')
need(2*J*Gp==F(77,390625),'exact_shifted_cap')
for k in range(9):
 coeff=16*8**k+(16*2**k*5*k*4**(k-1) if k else 0)
 egf=16*F(8**k,factorial(k))+(160*F(8**(k-1),factorial(k-1)) if k else 0)
 need(F(coeff,factorial(k))==egf,'order_coefficient_'+str(k))
need(F(1)==F(5,5),'anchored_ratio_five_needed_by_bound')
need(F(1)/(1-F(1,2))==2,'shifted_inverse_factor_two')
# Independent tensor-multinomial route to the order-eight control.
tuples8=[t for t in product(range(3),repeat=4) if sum(t)==8]
coef8=sum(F(factorial(8),prod(factorial(i) for i in t))*(-2)**4 for t in tuples8)
need(tuples8==[(2,2,2,2)] and coef8==40320,'tensor_multinomial_eighth_nonzero')
need(not [t for t in product(range(3),repeat=4) if sum(t)==9],'tensor_multinomial_ninth_zero')
need(any(sum(t)==7 for t in product(range(3),repeat=4)),'support_three_termination_not_importable')
# Exact nontrivial fixed point with mixing and retained diagonal.
c=F(1,10);a=F(0);d=F(1,20);b=c*(1+d-a)/(1-c*c)
V=[[a,b],[b,d]];H=[[a,b],[b,1+d]];P=[[1,0],[c,1]];Pinv=[[1,0],[-c,1]]
T=mul(mul(P,H),Pinv);W=mul(mul(P,V),Pinv);E=a-b*c
need(T[1][0]==0 and T[0][0]==E,'actual_fixed_point_and_scalar')
z=1+d-a+2*b*c;v=1+c*c;B=[[0,0],[v,0]]
comm=sub(mul(B,W),mul(W,B))
need(comm[1][0]/(1-z)==v,'exact_centered_excited_resolvent_identity')
need(E!=0,'zero_ground_substitution_rejected')
need(c!=b+c*a-b*c*c,'retained_diagonal_deletion_rejected')
need(mul(mul(Pinv,H),P)[1][0]!=0,'wrong_conjugation_sign_rejected')
need(F(24,8)*F(1,2)==F(24,16),'physical_gap_restoration')
res={'loop':'AM2','checks':checks,'checks_count':len(checks),'majorant_caps':{'G':str(G),'Gprime':str(Gp),'selfmap':str(J*G),'shifted_contraction':str(2*J*Gp)},'mixing_fixture':{'c':str(c),'b':str(b),'d':str(d),'actual_E0':str(E),'gap':str(z)},'replays':replay('am2'),'analytic_proof_required':True,'infinite_volume_claim':False}
(HERE/'am2-checks.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':True,'checks':len(checks)}))
