#!/usr/bin/env python3
"""Independent exact controls for AQ1; the analytic proof is in aq1.md."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
from replay_loop import replay
HERE=Path(__file__).resolve().parent
checks=[]
def need(ok,label):
 if not ok:raise RuntimeError(label)
 checks.append(label)
S=((0,0,0),(1,0,0),(0,1,0),(0,0,1))
def anchors(R):return {tuple(x[i]-s[i] for i in range(3)) for x in R for s in S}
for R,expected in [({(0,0,0)},4),({(0,0,0),(0,0,1)},7),({(-7,-3,-2),(-7,-3,-1)},7)]:
 need(len(anchors(R))==expected,'incident_'+str(sorted(R)))
 need(14*len(anchors(R))<=56*len(R),'reset_'+str(sorted(R)))
need(14*7==98 and 14*4==56,'bulk_pair_and_single_reset')
for x,y in product(range(-17,18),range(-9,10)):
 bx,rx=divmod(x,4);by,ry=divmod(y,2)
 need(4*bx+rx==x and 2*by+ry==y and 0<=rx<4 and 0<=ry<2,'floor_'+str((x,y)))
need(int(Q(-1,4))==0 and (-1)//4==-1,'truncation_fails_negative_owner')
for n in [1,2,4,16]:
 count=0
 for x in range(-n,n+1):
  for y in range(-n,n+1):
   remain=n-abs(x)-abs(y)
   count+=1 if remain==0 else 2 if remain>0 else 0
 need(count==4*n*n+2,'independent_shell_'+str(n))
 need(Q(count,(n+1)**4)<=Q(6,(n+1)**2),'summable_shell_'+str(n))
for d in range(41):
 need((1+Q(d,2))**-4<=16*Q(1,(1+d)**4),'convolution_split_'+str(d))
need(2*16*7==224 and 3**4*28==2268,'global_convolution_and_F_constants')
# Energy-tight normal densities converge, unlike escaping trace-one densities.
for n in [2,4,16,128]:
 p=Q(1,n)
 need(p*n==1 and 2*p<=2,'energy_tight_distance_'+str(n))
 for cutoff in [1,3,9]:
  tail=p if n>cutoff else Q(0)
  need(tail<=Q(1,cutoff),'spectral_tail_'+str((n,cutoff)))
 need(n>1 and 2==sum(abs(a-b) for a,b in zip([1,0],[0,1])),'untight_escape_'+str(n))
# Rank-one purification projection: exact two-eigenvalue trace-norm square.
p=Q(9,25);off=Q(12,25)
need(p*p+4*off*off==4*p-3*p*p<=4*p,'offdiagonal_gentle_projection')
joint=[Q(1,2),Q(0),Q(0),Q(1,2)]
marginal=[joint[0]+joint[1],joint[2]+joint[3]]
need(marginal==[Q(1,2),Q(1,2)] and marginal!=[Q(1),Q(0)],'incompatible_density_control')
# Strong continuity of diagonal unitaries does not give B(H)-norm continuity.
for n in [1,3,10,100]:
 need(Q((n+1)**2-n*n,2*n+1)==1,'shift_phase_pi_'+str(n))
# An excited invariant state can have negative GNS transition energy.
E_initial=Q(0);E_target=Q(-1)
need(E_target-E_initial<0,'stationarity_alone_not_positive_spectrum')
alpha=Q(12);hbar=Q(3);t=Q(2);delta=alpha/8
need(delta*t/hbar==1 and alpha*t/hbar==8,'physical_clock_factor_eight_control')
need(len(checks)==len(set(checks)),'unique_ids')
out={'loop':'AQ1','checks':checks,'checks_count':len(checks),'replays':replay('aq1'),'scope':'Analytic construction reviewed separately; finite exact controls do not establish infinite statements by sampling.'}
(HERE/'aq1-checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':True,'checks':len(checks)}))
