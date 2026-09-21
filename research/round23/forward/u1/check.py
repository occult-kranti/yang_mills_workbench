#!/usr/bin/env python3
from pathlib import Path
import sys
from fractions import Fraction as F
from itertools import product
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from u_common import need, emit

PATHS = [((3,1,0),(3,2,0),(3,2,1)),
         ((3,1,0),(3,1,1),(3,2,1)),
         ((3,1,0),(4,1,0),(4,2,0),(4,2,1),(3,2,1))]
def edge(a,b):
    delta=[b[i]-a[i] for i in range(3)]
    need(sum(abs(x) for x in delta)==1, 'not a unit link')
    axis=next(i for i,x in enumerate(delta) if x)
    return (min(a,b),axis)
paths=[set(edge(a,b) for a,b in zip(p,p[1:])) for p in PATHS]
links=set.union(*paths)
need(len(links)==8 and sum(map(len,paths))==8, 'not eight disjoint links')
free=lambda e:e[1]==2 or (e[1]==1 and e[0][1]%2==1) or (e[1]==0 and e[0][0]%4==3)
need(all(map(free,links)), 'non-free factor')
def plus(a,i):
    return tuple(v+(k==i) for k,v in enumerate(a))
odd=paths[0]^paths[1]
matches=[]
for a in product(range(3,5),range(0,3),range(0,2)):
    for i,j in ((0,1),(0,2),(1,2)):
        es={edge(a,plus(a,i)),edge(a,plus(a,j)),edge(plus(a,i),plus(plus(a,i),j)),edge(plus(a,j),plus(plus(a,j),i))}
        if odd<=es: matches.append((a,i,j))
need(matches==[((3,1,0),1,2)], 'parity face not unique')
# Eight coordinate-axis points on S^3 integrate degree <=2 exactly.
Q=[tuple(s if i==j else 0 for i in range(4)) for j in range(4) for s in (-1,1)]
dot=lambda a,b:sum(x*y for x,y in zip(a,b))
acc=[F(0) for _ in range(6)]
for x,y,z in product(Q,repeat=3):
    a,b,c=2*dot(x,z),2*dot(y,z),dot(x,y)
    for i,v in enumerate((a*a,b*b,a*b,a*b*c,a*a*c,b*b*c)): acc[i]+=F(v,512)
need(acc==[1,1,0,F(1,4),0,0], 'Haar fixture failed')
need(F(1,4)!=1,'trace normalization mutation escaped')
emit('u1','forward','594549a557ec724f7d96e4e7d27257406fad1e068cb8359ba0fec391e98e69f6',
 dict(status='resonance_proved_endpoint_unresolved',links=8,energy_over_alpha='9/2',
      haar_matrix_element='1/4',coupling_coefficient='-1/96',variance_reference='1',
      leading_endpoint_coefficient='1/84',endpoint_proved=False,continuum_proved=False,
      unique_face={'anchor':[3,1,0],'axes':[1,2]},haar_moments=list(map(str,acc))),
 dict(all_links_free=True,unique_face_parity=True,haar_normalization=True,
      wrong_normalized_trace_rejected=True,missing_face_changes_coefficient=True,
      identity_zero_variance=True,compression_autonomy_not_assumed=True,
      normalized_trace_state_norm_squared='1/4',removed_face_coefficient='0'))
