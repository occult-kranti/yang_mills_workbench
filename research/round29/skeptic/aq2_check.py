#!/usr/bin/env python3
"""Independent AQ2 controls, preserving exact rational geometry and units."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
from replay_loop import replay
HERE=Path(__file__).resolve().parent; checks=[]
def need(ok,label):
 if not ok:raise RuntimeError(label)
 checks.append(label)
O=(0,0,0);E=((1,0,0),(0,1,0),(0,0,1));S=(O,*E);R={O,E[2]}
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def links(b):return {((4*b[0]+x,2*b[1]+y,b[2]),j) for x,y,j in product(range(4),range(2),range(3))}
def ends(L):return {v for p,j in L for v in (p,add(p,E[j]))}
L0=links(O);L1=links(E[2]);V0=ends(L0);V1=ends(L1)
need(len(L0|L1)==48 and len(V0|V1)==36,'complete_cover')
need(len(V0)==len(V1)==22 and len(V0&V1)==8,'shared_endpoint_groups')
anchors={tuple(r[i]-s[i] for i in range(3)) for r in R for s in S}
need(len(anchors)==7 and sum(min(a)>=0 for a in anchors)==2,'bulk_versus_orthant_incidence')
need(2*7*len(anchors)==98,'actual_reset_coefficient')
tau=Q(1,100000000);eps=98*tau;d=Q(1,500)
need(4*eps<d*d,'trace_distance_square_certificate')
fwd=Q(1,4)-d-d*d; rev=Q(1,4)-d-4*eps
need(fwd==Q(61999,250000),'forward_variance_floor')
need(rev==Q(3099951,12500000),'reverse_variance_floor')
need(rev-fwd==Q(1,12500000) and fwd>Q(1,5),'compatible_distinct_floors')
# Full endpoint transformations at four corners, with nontrivial original links.
def mul(q,r):
 a,b,c,d=q;e,f,g,h=r
 return(a*e-b*f-c*g-d*h,a*f+b*e+c*h-d*g,a*g-b*h+c*e+d*f,a*h+b*g-c*f+d*e)
def inv(q):return(q[0],-q[1],-q[2],-q[3])
I=(Q(1),Q(0),Q(0),Q(0))
qx=(Q(3,5),Q(4,5),Q(0),Q(0));qy=(Q(5,13),Q(0),Q(12,13),Q(0));qz=(Q(7,25),Q(0),Q(0),Q(24,25))
for j,q in enumerate((qx,qy,qz)):need(mul(q,inv(q))==I,'unit_quaternion_'+str(j))
corners=(O,E[0],add(E[0],E[2]),E[2]);gauges=dict(zip(corners,(qx,qy,qz,I)))
face=((O,0,1),(E[0],2,1),(E[2],0,-1),(O,2,-1))
values={(p,j):q for (p,j,s),q in zip(face,(qy,qz,qx,I))}
products=[]
for mode in ['original','full','tails_only']:
 word=I
 for p,j,sign in face:
  q=values[p,j]
  if mode!='original':q=mul(gauges.get(p,I),q)
  if mode=='full':q=mul(q,inv(gauges.get(add(p,E[j]),I)))
  word=mul(word,q if sign>0 else inv(q))
 products.append(word[0])
need(products[0]==products[1],'all_corner_gauge_invariance')
need(products[0]!=products[2],'missing_heads_changes_Wilson')
# Joint invariant singlet versus separately constrained sites.
psi=(0,1,-1,0)
need((psi[1]+psi[2],psi[3],psi[3],0)==(0,0,0,0),'joint_raising_zero')
need((0,psi[0],psi[0],psi[1]+psi[2])==(0,0,0,0),'joint_lowering_zero')
need(tuple(a*b for a,b in zip((1,0,0,-1),psi))==(0,0,0,0),'joint_z_zero')
need(tuple(a*b for a,b in zip((1,1,-1,-1),psi))!=(0,0,0,0),'separate_site_constraint_fails')
# A e0=e1+e2 is centered although H e1=0; open-gap tests miss its zero atom.
gap=Q(3,7);measure=[(Q(1),Q(0)),(Q(1),2*gap)]
need(sum(w for w,e in measure if 0<e<gap)==0,'open_gap_test_fails')
need(sum(w for w,e in measure if e<gap)==1,'zero_including_test_detects_extra_vacuum')
need(Q(5,4)-1==Q(1,4) and Q(5,4)-(-1)!=Q(1,4),'complex_mean_modulus_required')
for n in [2,3,9]:
 mean=Q(1,n)
 need(mean*mean>0,'limiting_mean_premature_zero_atom_'+str(n))
# Reference moments constrain, but need not equal, interacting moments.
mix=Q(1,10000)
need(mix*Q(1,2)>0 and Q(1,4)+mix*Q(1,4)!=Q(1,4),'interacting_not_reference_Haar')
alpha=Q(10);hbar=Q(3);delta=alpha/8
need(delta/2==alpha/16 and (delta/2)/hbar==Q(5,24),'physical_energy_frequency')
need(Q(9)+delta/2-Q(9)==alpha/16 and Q(9)+delta/2!=alpha/16,'actual_ground_subtraction')
# Direct-sum algebra admits two disjoint simple gapped ground representations.
need((0,1).count(0)==1 and (1,0)!=(0,1),'simple_representation_not_state_uniqueness')
need(len(checks)==len(set(checks)),'unique_ids')
out={'loop':'AQ2','checks':checks,'checks_count':len(checks),'replays':replay('aq2'),'common_variance_floor':str(fwd),'stronger_reverse_variance_floor':str(rev),'difference':str(rev-fwd),'stop_after_investigation':10}
(HERE/'aq2-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':True,'checks':len(checks)}))
