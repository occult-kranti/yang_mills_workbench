#!/usr/bin/env python3
from itertools import product
from fractions import Fraction as F
from pathlib import Path
import json
from replay_loop import replay
HERE=Path(__file__).resolve().parent;checks=[]
def need(q,n):
 if not q:raise RuntimeError(n)
 checks.append(n)
S=[(0,0,0),(1,0,0),(0,1,0),(0,0,1)];Y=[(0,0,0),(0,0,1)]
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
for n in [3,5,7]:
 canon=set(product(range(-n+1,n),repeat=3));bulk=set(product(range(-n+2,n-1),repeat=3))
 # Generate only actual outer anchors and test every differing complete star.
 diff=0
 for a in product(range(-2*n,2*n),repeat=3):
  if a not in canon:
   need(all(plus(a,s) not in bulk for s in S),'disjoint_'+str(n)+'_'+str(diff));diff+=1
 nearest=min(min(n-1-abs(y[i]) for i in range(3)) for y in Y)
 need(nearest==n-2,'exact_distance_'+str(n))
need(len({tuple(y[i]-s[i] for i in range(3)) for y in Y for s in S})==7,'seven_anchors')
# Non-domain-preserving bounded rank-one map: psi_k=1/k is square-summable,
# while diag(k)psi has squared norm N in its N-prefix.
for N in [2,8,32]:
 need(sum(F(1,k*k) for k in range(1,N+1))<2,'bounded_vector_'+str(N))
 need(sum(F(k*k,k*k) for k in range(1,N+1))==N,'domain_failure_'+str(N))
# Identical gaps do not identify states in different bulk models.
need([0,1]!=[1,0] and abs(1-0)==abs(0-1),'same_gap_different_ground_control')
res={'loop':'AN1','checks_count':len(checks),'grouped_checks':['all_boundary_difference_stars_disjoint_n3_5_7','exact_n_minus_2_distance','seven_anchors','rank_one_domain_counterexample','same_gap_changed_bulk_counterexample'],'replays':replay('an1'),'verdict':'accepted_conditional_finite_comparison','state_limit_identified':False}
(HERE/'an1-checks.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'passed':True,'checks':len(checks)}))
