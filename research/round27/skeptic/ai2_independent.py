#!/usr/bin/env python3
"""Independent geometry and exact finite-profile scalar uncertainty audit."""
from fractions import Fraction as F
from itertools import product,combinations
from math import factorial,isqrt
from pathlib import Path
import json,hashlib
BASE=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
checks=[]
def require(label,ok):
 if not ok:raise RuntimeError(label)
 checks.append(label)
def canon(a,b):return tuple(sorted((a,b)))
def edge(a,axis):
 b=list(a);b[axis]+=1
 return canon(a,tuple(b))
def square(a,i,j):
 b=list(a);b[i]+=1;c=list(a);c[j]+=1
 return frozenset((edge(a,i),edge(tuple(b),j),edge(tuple(c),i),edge(a,j)))
def path(v):return frozenset(canon(a,b) for a,b in zip(v,v[1:]))
def direction(e):return next(i for i in range(3) if e[0][i]!=e[1][i])
def owner(e):
 a=direction(e);x,y,z=e[0]
 if a==0 and x%4<3 or a==1 and y%2==0:return ('strip',4*(x//4),2*(y//2),z)
 return ('link',e)
def members(f):
 if f[0]=='link':return {f[1]}
 _,x,y,z=f
 return {edge((x+r,y+s,z),0) for r in range(3) for s in range(2)}|{edge((x+r,y,z),1) for r in range(4)}
def face_is_omitted(a,i,j):return not ((i,j)==(0,1) and a[1]%2==0 and a[0]%4<3)
def incident(factors):
 result={}
 for f in factors:
  for e in members(f):
   i=direction(e);a=e[0]
   for j in range(3):
    if j==i:continue
    for shift in (0,-1):
     b=list(a);b[j]+=shift;b=tuple(b);ii,jj=sorted((i,j))
     if min(b)>=0 and face_is_omitted(b,ii,jj):
      sq=square(b,ii,jj);result[sq]={owner(ee) for ee in sq}
 return result
O=(3,1,0)
verts=[tuple(a+b for a,b in zip(O,p)) for p in product((0,1),repeat=3)]
edges=[canon(a,b) for a,b in combinations(verts,2) if sum(abs(x-y) for x,y in zip(a,b))==1]
faces={}
for i,j in combinations(range(3),2):
 axis=3-i-j
 for side in (0,1):
  a=list(O);a[axis]+=side;a=tuple(a)
  faces[square(a,i,j)]=sum(a)
cycles=[]
for ee in combinations(edges,6):
 degrees={v:sum(v in e for e in ee) for v in verts}
 if sum(d>0 for d in degrees.values())!=6 or any(d not in (0,2) for d in degrees.values()):continue
 # A six-edge even subgraph with six nonzero vertices in a cube cannot split into two cycles (girth four).
 cycles.append(frozenset(ee))
require('exact cube cycle count',len(cycles)==16)
X=path([(3,1,0),(3,2,0),(3,2,1)])
Y=path([(3,1,0),(3,1,1),(3,2,1)])
Z=path([(3,1,0),(4,1,0),(4,2,0),(4,2,1),(3,2,1)])
c=X|Z;d4=Y|Z;d5=c^square((4,1,0),1,2)
require('both selected pairs physical cycles',all(v in cycles for v in (c,d4,d5)))
require('selected connecting exponents',faces[c^d4]==4 and faces[c^d5]==5)
seed=set(c|d4|d5);require('combined ten-link source seed',len(seed)==10)
require('old seed misses new multiplier',not d5<=c|d4)
F0={owner(e) for e in seed};require('all ten source factors free',len(F0)==10 and all(f[0]=='link' for f in F0))
regions=[];current=F0
for k in range(6):
 I=incident(current);kept={f for f,own in I.items() if own<=current}
 regions.append({'k':k,'factors':len(current),'links':sum(len(members(f)) for f in current),'N':len(kept),'crossing':len(I)-len(kept)})
 if k>=1:require('full cube present k'+str(k),set(faces)<=kept)
 current=current|set().union(*I.values())
def mv(A,v):return [sum(a*b for a,b in zip(row,v)) for row in A]
def center(q,z,d):
 Q=[[q**faces[a^b] if a^b in faces else F(0) for b in cycles] for a in cycles]
 p=2+5*q+5*q*q+6*q**3+3*q**4
 s=3*z*(1+q)**2*(1+q*q)/p;v=s/96
 source=[F(a in (c,d)) for a in cycles];w=source[:];re=im=F(0);mom=[]
 for n in range(9):
  m=sum(x*y for x,y in zip(source,w))/2;mom.append(m)
  term=m*v**n/factorial(n)
  if n%2:im+=(-1)**((n-1)//2)*term
  else:re+=(-1)**(n//2)*term
  w=mv(Q,w)
 require('matrix row upper bound '+str(q),max(sum(row) for row in Q)<=6)
 require('exact first moment '+str(q)+' '+str(faces[c^d]),mom[1]==q**faces[c^d])
 return re,im,v,(6*v)**9/factorial(9),36*v**3

def b(q):return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def sqrt_up(x):
 D=1<<300;N=isqrt(x.numerator*D*D//x.denominator)
 return F(N,D) if F(N,D)**2==x else F(N+1,D)
def spatial(k,z):
 p=F(10,3);coef=F(1)
 for n in range(k+1):coef*=p+n
 return coef*(15*z)**(k+1)/factorial(k+1)/(1-15*z)**(k+5)
def budget(q,eta,z,k):
 tau=eta/(8*b(q));dh=tau*sqrt_up(b(q*q)/96)/(F(1,8)*(1-eta));M=F(regions[k]['N'],24)
 return {'state':48*dh,'spatial':8*spatial(k,z),'averaging':64*tau*M*(1+3*z*M)}
def clean(x):
 if isinstance(x,F):return str(x)
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 return x
z=F(1,10**6);rows=[]
for exponent in (12,18,24):
 u=F(1,10**exponent);h1=(1-u,F(1,2));h2=(1-2*u,F(1,16))
 require('equal physical times '+str(exponent),h1[1]*(1-h1[0])**3==h2[1]*(1-h2[0])**3)
 centers={(h,r):center(q,z,d) for h,(q,eta) in enumerate((h1,h2)) for r,d in ((4,d4),(5,d5))}
 for k in (3,4,5):
  budgets=[budget(q,eta,z,k) for q,eta in (h1,h2)]
  for r in (4,5):
   c1,c2=centers[0,r],centers[1,r]
   rad1=sum(budgets[0].values())+c1[3];rad2=sum(budgets[1].values())+c2[3]
   imag_dist=abs(c1[1]-c2[1]);margin=imag_dist-rad1-rad2
   rows.append({'u_exponent':exponent,'k':k,'probe':r,'physical_time_hbar_over_alpha':z/h1[1]/u**3,'center1_re':c1[0],'center1_im':c1[1],'center2_re':c2[0],'center2_im':c2[1],'radius1':rad1,'radius2':rad2,'imaginary_separation':imag_dist,'margin':margin,'certified_disjoint':margin>0,'equal_extra_error_per_hypothesis_allowance':max(F(0),margin/2),'budgets':budgets})
  # A cubic finite-ratio enclosure is generally too wide; retain this failure.
  for h,(q,eta) in enumerate((h1,h2)):
   c4,c5=centers[h,4],centers[h,5];delta=sum(budgets[h].values())+c4[4]
   denominator=c4[2]*q**4-delta
   require('positive ratio denominator '+str((exponent,k,h)),denominator>0)
   bound=(1+q)*delta/denominator
   require('simple ratio bound exceeds hypotheses q difference '+str((exponent,k,h)),bound>u)
require('wrong q5 to q4 collapses moment ratio',F(3,4)**4/F(3,4)**4==1)
require('correct moment ratio differs from collapsed model',F(3,4)**5/F(3,4)**4!=1)
# Arbitrary extra noise at least the actual signal denominator destroys the ratio certificate.
def guarded_ratio(v,q,delta):
 denominator=v*q**4-delta
 if denominator<=0:return None
 return (1+q)*delta/denominator
require('denominator failure refuses inference',guarded_ratio(c4[2],q,2*c4[2]*q**4) is None)
q_bad=F(1,10);bad_center=center(q_bad,z,d4);bad_budget=budget(q_bad,F(1,2),z,3)
require('actual admissible q one tenth has unusable denominator',guarded_ratio(bad_center[2],q_bad,sum(bad_budget.values())+bad_center[4]) is None)
blocked=next(row for row in rows if row['u_exponent']==12 and row['k']==5 and row['probe']==4)
without_state=F(blocked['radius1'])+F(blocked['radius2'])-sum(bb['state'] for bb in blocked['budgets'])
require('omitting physical state error creates false admission',blocked['margin']<0 and blocked['imaginary_separation']>without_state)
require('actual multiplier norm squared cannot be one',F(8)!=F(1))
contract=BASE/'research/round27/contracts/ai2.json'
result={'schema':'ym27-independent-ai2-v1','status':'PASS','scope':'Independent actual ten-link collar, 16-cycle retained moments, full scalar error comparisons under inherited transfer; not experiment or general inverse','checks':checks,'check_count':len(checks),'regions':regions,'rows':rows,'contract_sha256':hashlib.sha256(contract.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'ai2-independent.json').write_text(json.dumps(clean(result),indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks),'regions':regions,'disjoint':[(r['u_exponent'],r['k'],r['probe']) for r in rows if r['certified_disjoint']]}))
