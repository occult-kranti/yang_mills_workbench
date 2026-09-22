#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json
from replay_loop import replay
HERE=Path(__file__).resolve().parent;checks=[]
def need(v,m):
 if not v:raise RuntimeError(m)
 checks.append(m)
tau=F(1,65536);kin=F(9,4)+F(7,2)*tau;moment=18+8*kin
need(moment==F(589831,16384) and moment<37,'physical_second_moment_cap')
need(2*F(9,8)==F(9,4),'two_selected_strip_budgets')
# Four-link action on a holonomy class function f(w): Qf=-(1-w²)f''+3wf'.
def qpoly(p):
 out={}
 for k,c in p.items():
  out[k]=out.get(k,0)+(k*(k-1)+3*k)*c
  if k>=2:out[k-2]=out.get(k-2,0)-k*(k-1)*c
 return {k:v for k,v in out.items() if v}
need(qpoly({1:F(1)})=={1:F(3)},'Casimir_on_W')
need(qpoly({2:F(1)})=={2:F(8),0:F(-2)},'full_derivative_cross_term')
need(F(-2)!=0,'dropping_cross_at_Wzero_rejected')
lam=F(1,8);trial_t=lam/3
trial=(3*trial_t**2/4-lam*trial_t/2)/(1+trial_t**2/4)
need(trial==F(-3,2305),'nonzero_selected_reference_ground_shift')
for alpha in [F(1,7),F(1),F(13)]:
 free=F(1,4)*(3*alpha)**2
 need(free==F(9,4)*alpha**2 and 0<free<moment*alpha**2,'free_moment_'+str(alpha))
# Exact kinetic identity and the one-sided scalar deletion distinction.
h,V,B=F(0),F(-5,2),F(-1);T=h-V+B
need(T==F(3,2) and T!=h-V and T<=h-V,'negative_scalar_identity_versus_upper_bound')
# Bounded first moment with lost moment under weak convergence.
for n in [2,8,32]:
 m1=(1-F(1,n))*1+F(1,n)*n;m2=(1-F(1,n))+F(1,n)*n*n
 need(m1<2 and m2==n+1-F(1,n),'first_moment_not_UI_'+str(n))
res={'loop':'AO1','checks':checks,'checks_count':len(checks),'cap':str(moment),'replays':replay('ao1'),'infinite_domain_asserted':False}
(HERE/'ao1-checks.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':True,'checks':len(checks)}))
