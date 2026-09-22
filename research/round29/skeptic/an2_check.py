#!/usr/bin/env python3
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
from replay_loop import replay
HERE=Path(__file__).resolve().parent;checks=[]
def need(q,m):
 if not q:raise RuntimeError(m)
 checks.append(m)
S=((0,0,0),(1,0,0),(0,1,0),(0,0,1))
for r in (0,1,2):
 n=r+2;F=set(product((-r,r),repeat=3));canon=set(product(range(-n+1,n),repeat=3));bulk=set(product(range(-n+2,n-1),repeat=3))
 for L,M in ((2*n,n),(3*n,n+2),(2*n+1,2*n)):
  def inside(p,lo,hi):return all(lo<=x<=hi for x in p)
  for lo,hi in ((-n,L-n),(-M,M)):
   for a in product(range(lo,hi),repeat=3):
    if a not in canon and any(tuple(a[i]+s[i] for i in range(3)) in bulk for s in S):raise RuntimeError('difference touched common bulk')
  need(min(n-1-abs(x) for p in F for x in p)==n-r-1,'distance_'+str((r,L,M)))
# Stronger logical control: diagonal zero but each fixed-n tail equals one.
for n in [1,2,3,8]:
 f=lambda L:int(L>=n*n+2*n)
 need(f(2*n)==0 and f(n*n+2*n)==1,'noninterchange_'+str(n))
# A single identical marginal does not identify two joint states.
a=[Q(1,2),0,0,Q(1,2)];b=[0,Q(1,2),Q(1,2),0]
reduce_first=lambda x:[x[0]+x[1],x[2]+x[3]]
need(reduce_first(a)==reduce_first(b) and a!=b,'one_marginal_not_entire_state')
# Fixed translations leave common interior after increasing outer radius.
z=(2,-3,1);n=4;M=n+max(map(abs,z))
need(all(-M-z[i]<=-n and M-z[i]>=n for i in range(3)),'shifted_box_contains_common_cube')
res={'loop':'AN2','checks':checks,'checks_count':len(checks),'replays':replay('an2'),'limit_order':'outer orthant at fixed translation; centered limit; translation limit','whole_state_compatibility_analytic':True}
(HERE/'an2-checks.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':True,'checks':len(checks)}))
