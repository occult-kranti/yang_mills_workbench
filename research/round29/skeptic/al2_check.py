#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
from replay_loop import replay
here=Path(__file__).resolve().parent
checks=[]
def need(q,n):
 if not q:raise RuntimeError(n)
 checks.append(n)
for g4,c1,c2 in product([F(1,9),F(1),F(16)],[F(1,10),F(100)],[F(1,1000),F(10)]):
 caps=[g4/32,c1*g4/672,g4/(1344*c2)]
 for s in [F(0),*caps,min(caps)/2,max(caps)*2]:
  r=4*s/g4;e=21*8*r
  direct=(r<=F(1,2) and r<=F(1,8) and e<c1 and 2*c2*e<1)
  reduced=(s<=caps[0] and s<caps[1] and s<caps[2])
  need(direct==reduced,'iff_'+str(len(checks)))
for q in [F(1,99),F(1),F(22)]:
 a,b=F(3,7),F(8,3)
 need(q*b/(q*a)==b/a,'ratio_'+str(q))
 need(q*a*(F(5)/q)==a*5,'clock_'+str(q))
need(F(0)<=F(1,32),'zero_is_formally_eligible')
need(not F(0)>0,'zero_is_not_nonzero_target')
result={'loop':'AL2','checks_count':len(checks),'checks':checks,'replays':replay('al2'),'verdict':'accepted_within_scope','c1_c2_are_synthetic':True}
(here/'al2-checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'passed':True,'checks':len(checks)}))
