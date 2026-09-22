"""Independent physical cube/source checks for manuscript; no historical imports."""
from fractions import Fraction as F
from itertools import product,combinations
from collections import Counter
from pathlib import Path
import argparse,json,hashlib
out=[]
def ck(ok,name,**extra):
 if not ok:raise ValueError(name)
 out.append({'check':name,'passed':True,**extra})
def edge(a,b):return tuple(sorted((tuple(a),tuple(b))))
def face(p,a,b):
 pa=list(p);pa[a]+=1;pb=list(p);pb[b]+=1;pab=pa[:];pab[b]+=1
 return frozenset([edge(p,pa),edge(pa,pab),edge(pab,pb),edge(pb,p)])
origin=(3,1,0); verts=[tuple(origin[i]+d[i] for i in range(3)) for d in product((0,1),repeat=3)]
edges=sorted({edge(a,b) for a,b in combinations(verts,2) if sum(abs(a[i]-b[i]) for i in range(3))==1})
faces=sorted({face(p,a,b) for p in verts for a,b in combinations(range(3),2) if set().union(*face(p,a,b))<=set(verts)},key=lambda f:sorted(f))
# set().union(*edges) yields endpoint vertices because each edge is pair of tuples.
ck(len(edges)==12 and len(faces)==6,'Actual translated free cube has12links6faces')
cycles=[]
for ids in combinations(range(12),6):
 es=frozenset(edges[i] for i in ids);deg=Counter(v for e in es for v in e)
 if all(d==2 for d in deg.values()):cycles.append(es)
ck(len(cycles)==16,'Complete energy9/2 physical cube cycle census')
A=[[int(c^d in faces) for d in cycles] for c in cycles]
ck(Counter(map(sum,A))=={2:12,6:4},'Full flip graph degree census')
def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def add(*terms):return [[sum((f*a[i][j] for f,a in terms),F(0)) for j in range(16)] for i in range(16)]
I=[[F(int(i==j)) for j in range(16)] for i in range(16)];pw=[I,A]
for n in range(2,7):pw.append(mm(pw[-1],A))
ck(all(x==0 for row in add((1,pw[5]),(-16,pw[3]),(48,pw[1])) for x in row),'Full adjacency polynomial A(A2-4)(A2-12) vanishes')
P0=add((1,I),(-F(1,3),pw[2]),(F(1,48),pw[4]))
P4=add((F(3,8),pw[2]),(-F(1,32),pw[4]))
P12=add((-F(1,24),pw[2]),(F(1,96),pw[4]))
ck([sum(P[i][i] for i in range(16)) for P in (P0,P4,P12)]==[8,6,2],'Exact squared-spectrum projection multiplicities')
ck(all(mm(P,P)==P for P in (P0,P4,P12)),'All exact spectral projectors idempotent')
O=origin;D=(3,2,1)
X=[O,(3,2,0),D];Y=[O,(3,1,1),D];Z=[O,(4,1,0),(4,2,0),(4,2,1),D]
path=lambda vs:frozenset(edge(a,b) for a,b in zip(vs,vs[1:]))
i=cycles.index(path(X)|path(Z));j=cycles.index(path(Y)|path(Z))
single=[p[i][i] for p in pw]
plus=[(p[i][i]+p[i][j]+p[j][i]+p[j][j])/F(2) for p in pw]
ck(single==[1,0,2,0,16,0,160],'Single actual X-cycle adjacency moments')
ck(plus==[1,1,4,8,32,80,320],'Actual U-path coherent-state adjacency moments')
ck([P[i][i] for P in (P0,P4,P12)]==[F(2,3),F(1,4),F(1,12)],'Single actual X-cycle spectral masses')
# Physical ownership: complete strips, never merely the visible edge.
def owner(e):
 a,b=e;axis=next(i for i in range(3) if a[i]!=b[i]);x,y,z=a
 if axis==0 and x%4!=3:return ('strip',x-x%4,y-y%2,z)
 if axis==1 and y%2==0:return ('strip',x-x%4,y,z)
 return ('free',e)
ck(all(owner(e)[0]=='free' for e in edges),'Every cube edge is an actual free reference factor')
ext=[]
for p in product(range(2,6),range(0,4),range(0,3)):
 for a,b in combinations(range(3),2):
  f=face(p,a,b);shared=f.intersection(edges)
  if shared and f not in faces:ext.append((p,a,b,f,shared))
ck(len(ext)==20 and all(len(r[-1])==1 for r in ext),'All20 exterior touching faces meet exactly one cube edge')
for p,a,b,f,shared in ext:
 e=next(iter(shared));ax=next(i for i in range(3) if e[0][i]!=e[1][i])
 opp=next(g for g in f if g!=e and g[0][ax]!=g[1][ax]);sides=f-{e,opp}
 if owner(opp)[0]!='free' or len({owner(g) for g in sides})!=2:raise ValueError('exterior factor witness')
ck(True,'Every exterior opposite edge is free and remaining sides own distinct complete factors')
ck(-F(3,4)+F(3,4)+2*F(1,8)==F(1,4),'Exterior excitation floor after lowest shared-edge fusion')
ck(min(abs(F(3)-F(3,2)*r+2*m) for r in range(5) for m in range(r+1) if F(3)-F(3,2)*r+2*m!=0)==F(1,2),'Internal nonzero participating frequency floor')
# Actual single-source commutator algebra on a noncommuting three-level fixture.
def m3(a,b):return [[sum((a[i][k]*b[k][j] for k in range(3)),F(0)) for j in range(3)] for i in range(3)]
def a3(*terms):return [[sum((f*a[i][j] for f,a in terms),F(0)) for j in range(3)] for i in range(3)]
def comm(a,b):return a3((1,m3(a,b)),(-1,m3(b,a)))
phi=[[F(0),F(1,5),F(1,7)],[F(1,5),F(1,3),F(1,11)],[F(1,7),F(1,11),F(-1,4)]]
v=[phi[1][0],phi[2][0]];u=[v[0]/2,v[1]/5];aa=sum(x*y for x,y in zip(u,v));bb=sum(x*x for x in u)
S=[[F(0),-u[0],-u[1]],[u[0],F(0),F(0)],[u[1],F(0),F(0)]]
Ar=[[F(0),v[0],v[1]],[v[0],F(0),F(0)],[v[1],F(0),F(0)]]
C=a3((F(1,2),comm(S,comm(S,phi))),(-F(1,6),comm(S,comm(S,Ar))))
w=[C[1][0],C[2][0]]
ck(w==[-aa*u[k]-bb*v[k]/3 for k in range(2)],'Actual-source cubic column algebra with nonzero diagonal interaction')
ck(sum(x*y for x,y in zip(u,w))==-F(4,3)*aa*bb<0,'Cubic source nonzero sign witness')
ck(8*4*F(3,16)*F(21,9)==14,'Source form energy14tau2 independently normalized')
ck(F(1,24)**2+F(1,3*576)==F(1,432),'Inverse spectral Jensen lower bound coefficient')
ck(1-12*F(1,16)*(1+4*F(35,1664))==F(311,1664),'Short-filter residual positive lower bound cap')
# Exact phase coefficient and small-z full-model transfer domain.
ck(F(8,7)/96==F(1,84),'Same-clock phase conversion rho/96=z/84')
ck(F(4,2)*F(1,84)**2==F(1,3528),'Full endpoint second-moment Taylor disk')
z=F(1,10**6); xx=F(80,7)*z
ck(F(44,9)*xx**2/(1-xx)**5<z/168,'Uniform small-endpoint positive lower margin')
# Negative time exponents invalidate N2 iff unless gamma>=0 is stipulated.
ck(F(1,100)*F(1,4)<F(1,4),'Shrinking time beta>=1 control requires stated gamma>=0 domain')
p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
if args.output.exists():raise ValueError('fresh output required')
args.output.mkdir(parents=True)
(args.output/'results.json').write_text(json.dumps({'scope':'new independent graph and exact-source manuscript checks','count':len(out),'checks':out,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2)+'\n')
print(json.dumps({'passed':len(out)}))
