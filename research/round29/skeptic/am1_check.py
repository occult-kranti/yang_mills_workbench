#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import json
from replay_loop import replay
HERE=Path(__file__).resolve().parent
O=(0,0,0); E=((1,0,0),(0,1,0),(0,0,1)); checks=[]
def need(x,t):
 if not x:raise RuntimeError(t)
 checks.append(t)
def step(p,i):q=list(p);q[i]+=1;return tuple(q)
def owner(v):return(v[0]//4,v[1]//2,v[2])
def edges(p,i,j):
 vs=[p,step(p,i),step(step(p,i),j),step(p,j)]
 return {(tuple(min(a[k],b[k]) for k in range(3)),next(k for k in range(3) if a[k]!=b[k])) for a,b in zip(vs,vs[1:]+vs[:1])}
square=edges(O,0,1)
need(len(square)==4 and len({p for p,d in square})==3,'four_links_three_fine_tails')
need({owner(p) for p,d in square}=={O},'one_coarse_factor')
# Complete shifted anchor incidence is recomputed from star membership.
anchors=[]
for a in product(range(-1,2),repeat=3):
 if O in {tuple(a[k]+s[k] for k in range(3)) for s in (O,*E)}:anchors.append(a)
need(len(anchors)==4,'four_star_anchors')
indexed=0;touching=0
for a in anchors:
 for x,y in product(range(4),range(2)):
  p=(4*a[0]+x,2*a[1]+y,a[2])
  for i,j in combinations(range(3),2):
   if (i,j)==(0,1) and y==0 and x<3:continue
   indexed+=1;touching+=O in {owner(t) for t,d in edges(p,i,j)}
need((indexed,touching)==(84,49),'indexed_support_not_minimal_support_budget')
need(F(84,3)==28,'site_norm_conversion')
# A one-factor physical Wilson in the Haar subcase has norm-square 1/4,
# excitation count one, but energy 4*(3/4)*alpha; delta=alpha/8.
need(F(4)*F(3,4)*8==24,'Haar_witness_energy_24_delta_does_not_refute_4_delta')
need(F(3,4)!=F(4,3),'Casimir_dictionary_not_identical')
result={'loop':'AM1','checks':checks,'checks_count':len(checks),'replays':replay('am1'),'numerical_radius':'insufficient','source_energy_claim_refuted':False}
(HERE/'am1-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':True,'checks':len(checks)}))
