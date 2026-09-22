#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json
from replay_loop import replay
HERE=Path(__file__).resolve().parent;checks=[]
def need(v,s):
 if not v:raise RuntimeError(s)
 checks.append(s)
def theta(E,R):return F(0) if E<0 else min(F(1),max(F(0),2-E/R))
def cutoff(E,R,k):return E**k*theta(E,R)
for E in [F(-3),F(0),F(1,3),F(2),F(13)]:
 for k in [1,2]:
  vals=[cutoff(E,R,k) for R in [F(1,4),F(1),F(4),F(16)]]
  need(all(a<=b for a,b in zip(vals,vals[1:])),'monotone_'+str((E,k)))
  if E<0:need(vals==[0]*4,'zero_extension_'+str(k))
for n in [2,4,16,128]:
 g=F(1,7);mu=[(1-F(1,n*n),g),(F(1,n*n),g+n)]
 m1=sum(w*e for w,e in mu);m2=sum(w*e*e for w,e in mu)
 need(m1==g+F(1,n) and m2==g*g+2*g/n+1,'escaping_second_'+str(n))
 for R in [F(1),F(3),F(9)]:
  rem=m1-sum(w*cutoff(e,R,1) for w,e in mu)
  need(0<=rem<=m2/R,'uniform_first_tail_'+str((n,R)))
 need(m2<2 and m2-g*g>1,'bounded_second_not_equality_'+str(n))
need(F(36)+F(7,16384)<37,'actual_second_cap_finite')
res={'loop':'AO2','checks':checks,'checks_count':len(checks),'replays':replay('ao2'),'cutoff_clarification':'Extend both compact half-line tests by zero on E<0.','second_moment_equality':False}
(HERE/'ao2-checks.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':True,'checks':len(checks)}))
