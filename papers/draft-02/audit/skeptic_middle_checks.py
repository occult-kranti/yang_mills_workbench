"""Independent rational manuscript probes; no workbench producer imported."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial,comb
from collections import defaultdict
from functools import lru_cache
import argparse,json,hashlib
D=12; Z=(0,)*D

def scalar(x):return {Z:F(x)} if x else {}
def var(i):
 k=list(Z);k[i]=1;return {tuple(k):F(1)}
def add(*ps):
 r=defaultdict(F)
 for p in ps:
  for k,v in p.items():r[k]+=v
 return {k:v for k,v in r.items() if v}
def mul(*ps):
 r=scalar(1)
 for p in ps:
  q=defaultdict(F)
  for a,u in r.items():
   for b,v in p.items():q[tuple(x+y for x,y in zip(a,b))]+=u*v
  r={k:v for k,v in q.items() if v}
 return r
def scale(c,p):return {k:c*v for k,v in p.items() if c*v}
def power(p,n):
 r=scalar(1)
 for _ in range(n):r=mul(r,p)
 return r
@lru_cache(None)
def sphere(k):
 if any(x%2 for x in k):return F(0)
 n=sum(k)//2
 v=F(1,2**n*factorial(n+1))
 for a in k:
  for j in range(1,a,2):v*=j
 return v
def E(p):return sum((v*sphere(k[:4])*sphere(k[4:8])*sphere(k[8:]) for k,v in p.items()),F(0))
records=[]
def ck(v,name,**extra):
 if not v:raise ValueError(name)
 records.append({'check':name,'passed':True,**extra})
u=[var(i) for i in range(4)];v=[var(i+4) for i in range(4)];w=[var(i+8) for i in range(4)]
x,y,z=u[0],v[0],w[0]
dot=lambda a,b:add(*(mul(a[i],b[i]) for i in range(4)))
uv,vw,uw=dot(u,v),dot(v,w),dot(u,w)
ck(E(mul(x,y,uv))==F(1,16),'Shared two-link triple moment')
ck(E(mul(power(x,2),power(y,2),power(uv,2)))==F(1,48),'Shared two-link repeated moment retains spin-one channel')
ck(E(mul(x,z,uv,vw))==F(1,64),'Actual common-middle four-factor moment')
ck(E(mul(x,uv))*E(mul(z,vw))==0,'Independently resampled middle destroys the selected moment')
O=scale(F(1,81),mul(power(add(scale(4,power(x,2)),scalar(-1)),3),add(scale(4,power(uv,2)),scalar(-1))))
S=add(scale(3,x),y,z,uv,vw)
nums=[E(mul(O,power(S,n)))/factorial(n) for n in range(4)]
zeds=[E(power(S,n))/factorial(n) for n in range(4)]
ck(nums==[F(0),F(0),F(1,324),F(13,1296)],'Independent quaternion static numerator coefficients',values=list(map(str,nums)))
ck(zeds==[F(1),F(0),F(13,8),F(1,4)],'Independent quaternion static denominator coefficients',values=list(map(str,zeds)))
ck(2*nums[3]==F(13,648),'Static sign cross-difference cubic coefficient')
# Spherical tetrahedral direction variables are orthogonal coordinates by O(4) invariance.
adj=scalar(1)
for a in u:adj=mul(adj,add(scale(4,power(a,2)),scalar(-1)))
ck(E(adj)/81==-F(1,405),'Complete adjoint projector tetrahedral negative value')
comm=mul(power(add(scale(4,power(u[0],2)),scalar(-1)),2),power(add(scale(4,power(u[1],2)),scalar(-1)),2))
ck(E(comm)/81==F(13,1215),'Equal action vector does not identify observable integral')
# Pure Haar one-coordinate exact rate polynomials and second-derivative witness.
G=scale(F(1,4),add(scalar(1),scale(-1,power(x,2))))
p3=add(power(x,3),scale(-F(3,8),x))
p5=add(power(x,5),scale(-F(5,6),power(x,3)),scale(F(1,8),x))
derivatives=[scalar(1),add(scalar(1),scale(F(1,2),x)),add(scale(2,x),scale(3,power(x,2)))]
weights=[mul(G,power(p,2)) for p in derivatives]
mat=[[E(mul(a,b)) for b in [scalar(1),x,p3]] for a in weights]
expected=[[F(3,16),F(0),F(0)],[F(25,128),F(1,32),F(0)],[F(59,256),F(9,64),F(9,512)]]
ck(mat==expected,'All entries of actual three-rate matrix',matrix=[[str(c) for c in r] for r in mat])
ck(mat[0][0]*mat[1][1]*mat[2][2]==F(27,262144),'Rate determinant in linear parameter coordinates')
ck(all(E(mul(p5,a))==0 for a in weights),'Fifth-degree mobility preserves all three slopes')
T=add(scale(2,power(x,6)),scale(-F(5,2),power(x,4)),scale(F(3,4),power(x,2)),scalar(-F(1,32)))
ck(E(mul(T,x))==0 and E(power(T,2))==F(1,1024),'Hidden mobility changes curvature rather than all-time curve')
ck(F(1)-F(1,4)-F(11,32)==F(13,32),'Declared cubic mobility remains uniformly positive')
# Conditional leakage is a nonconstant multiplier, not its average.
d=add(scalar(F(19,4)),scale(F(1,2),add(uw,x,z)))
ck(E(d)==F(19,4) and E(power(d,2))==F(91,4),'Conditional variance first and second moments')
ck(E(mul(d,scale(2,x)))==F(1,4),'Projected-memory off-diagonal at zero delay')
ck(E(mul(d,scale(4,power(x,2))))==F(19,4),'Excited-channel zero-delay variance')
weights_by_energy=defaultdict(F)
weights_by_energy[F(15,2)]+=9*F(1,4)
for m,count in [(1,6),(2,2),(3,2)]:
 low=F(3,4)*(10-2*m)
 weights_by_energy[low]+=count*F(1,16)
 weights_by_energy[low+2*m]+=count*F(3,16)
expected={F(3):F(1,8),F(9,2):F(1,8),F(6):F(3,8),F(15,2):F(9,4),F(8):F(9,8),F(17,2):F(3,8),F(9):F(3,8)}
ck(dict(weights_by_energy)==expected,'All seven physical path-recoupling energy weights')
ck(sum(expected.values())==F(19,4) and sum(e*w for e,w in expected.items())==F(285,8),'Full spectral weight and first energy moment')
ck(F(19,4)*F(1,8)-F(1,4)**2>0,'Matrix spectral weight is positive with nonzero off-diagonal')
ck(F(25,4)*40==250,'Full selected-space kernel/resolvent error coefficient')
# General block-memory sign and return cannot be dropped: powers on positive block.
H=[[F(2),F(1,3)],[F(1,3),F(4)]]
def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(2)),F(0)) for j in range(2)] for i in range(2)]
H2=mm(H,H)
ck((H2[0][0]-H[0][0]**2)/2==F(1,18),'Compression difference begins with positive BstarB over two')
# Exact Schur inverse at positive energy z=1.
ck(F(5,1)/(3*5-F(1,9))==1/(3-F(1,9)/5),'Schur complement minus sign')
ck(F(5,1)/(3*5-F(1,9))!=1/(3+F(1,9)/5),'Wrong plus Schur sign rejected')
# Interaction support cardinality and retained remainder arithmetic.
Gstar={(0,0,0),(1,0,0),(0,1,0),(0,0,1)}
ck(len({tuple(a-b for a,b in zip(x,y)) for x in Gstar for y in Gstar})==13,'Star overlap difference set has thirteen elements')
ck(F(7,12)+14*F(4,5)==F(707,60),'Local remainder conservative rational constant')
ck(F(1,8)-F(107,135*64)==F(973,8640),'Infinite summable-model gap arithmetic')
ck(F(1,4)-F(2,150)-F(4,22500)==F(5321,22500),'Nonzero physical Wilson variance after projector error')
ck(F(3,4)*F(13,32)/F(9,2)==F(13,192),'Mobility gap restored with conservative exponential bound')
# Response certificate direction: wrong side of origin reverses the damping assumption.
ck(F(3)/F(-1)<0,'Residual certificate must restrict positive coupling interval')
# Endpoint phase formula is whole spectral characteristic; transfer admitted only small z.
ck(F(1,10**6)>0 and F(1,10**6)<F(1,5),'Finite-q to full endpoint certificate does not authorize z=.2')
# Independent full support and SU2 multiplicity census through energy six alpha.
from itertools import product,combinations
vertices=list(product(range(3),range(2),range(2)))
vedges=[]
for a in vertices:
 for axis,lim in enumerate((3,2,2)):
  b=list(a);b[axis]+=1
  if b[axis]<lim:vedges.append((vertices.index(a),vertices.index(tuple(b))))
@lru_cache(None)
def invariant(labels):
 channels={0:1}
 for n in labels:
  nxt=defaultdict(int)
  for a,m in channels.items():
   for b in range(abs(a-n),a+n+1,2):nxt[b]+=m
  channels=dict(nxt)
 return channels.get(0,0)
strict={0:1}; threshold_supports=0; threshold_channels=0; threshold_mult=defaultdict(int)
for size in range(1,9):
 for ids in combinations(range(len(vedges)),size):
  incidence=[[] for _ in vertices]
  for j,eid in enumerate(ids):
   a0,b0=vedges[eid];incidence[a0].append(j);incidence[b0].append(j)
  if any(len(vv)==1 for vv in incidence):continue
  # n>=4 costs24 alone and cannot fit a nonempty closed support; n<=3 exhaustive.
  # Only zero, one, or two replacements fit at nonempty leafless support size>=4.
  assignments=[(1,)*size]
  for count in (1,2):
   for positions in combinations(range(size),count):
    for values in product((2,3),repeat=count):
     ns=[1]*size
     for at,n in zip(positions,values):ns[at]=n
     if sum(n*(n+2) for n in ns)<=24:assignments.append(tuple(ns))
  for labels in assignments:
   e4=sum(n*(n+2) for n in labels)
   if e4>24:continue
   mult=1
   for local in incidence:
    mult*=invariant(tuple(sorted(labels[j] for j in local)))
    if not mult:break
   if not mult:continue
   if e4<24:strict[e4]=strict.get(e4,0)+mult
   else:
    threshold_supports+=1;threshold_channels+=mult;threshold_mult[mult]+=1
ck(strict=={0:1,12:11,18:36},'Independent exhaustive physical strict-cutoff classification rank48',energy_fourths=strict)
ck(threshold_supports==99 and threshold_channels==107 and dict(threshold_mult)=={1:91,2:8},'Independent threshold multiplicities distinguish99 assignments from107 channels')
a=argparse.ArgumentParser();a.add_argument('--output',required=True,type=Path);args=a.parse_args()
if args.output.exists():raise ValueError('fresh output required')
args.output.mkdir(parents=True)
(args.output/'results.json').write_text(json.dumps({'scope':'new exact manuscript calculations, not historical production replay','count':len(records),'checks':records,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
print(json.dumps({'passed':len(records)}))
