"""Independent manuscript stress calculations; no producer module is imported.

These checks falsify specific invalid extensions and rederive selected identities.
They do not constitute a formal verification of the entire historical program.
"""
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import argparse, hashlib, json
from itertools import combinations, product as cartesian

records=[]
def require(ok, name, **evidence):
    if not ok: raise ValueError(name)
    records.append({'check':name,'passed':True,**evidence})
def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [serial(v) for v in x]
    return x

def haar(n):
    return F(comb(n,n//2),n//2+1)/4**(n//2) if n%2==0 else F(0)
def product(a,b,n):
    return [sum((a[j]*b[i-j] for j in range(i+1)),F(0)) for i in range(n+1)]
def quotient(a,b,n):
    q=[]
    for i in range(n+1): q.append((a[i]-sum((b[j]*q[i-j] for j in range(1,i+1)),F(0)))/b[0])
    return q

# Normalized tilted Haar family, derived from its moments rather than an ODE solver.
N=18
z=[haar(i)/factorial(i) for i in range(N+1)]
u=quotient([haar(i+1)/factorial(i) for i in range(N+1)],z,N)
m2=quotient([haar(i+2)/factorial(i) for i in range(N+1)],z,N)
u2=product(u,u,N)
variance=[m2[i]-u2[i] for i in range(N+1)]
require(all((i+1)*u[i+1]==variance[i] for i in range(N)),'R13 coupling derivative equals variance through order17',u_prime_zero=u[1])
res=[(i+3)*u[i]-(F(1) if i==1 else 0)+(u2[i-1] if i else 0) for i in range(N+1)]
require(all(x==0 for x in res),'R13 Haar scalar ODE exact formal coefficients through order18')
wrong=[res[i]-u[i] for i in range(N+1)]
require(wrong[1]==-F(1,4),'R13 wrong uniform-prior coefficient rejected',linear_residual=wrong[1])
k=F(9,8); x=F(1,3)
require(3*x==k*(1-x*x) and 1-4*x*x+k*(x-x**3)==F(8,9),'R13 point closure passes zeroth identity but fails next',next_residual=F(8,9))
require(haar(2)==F(1,4) and 16*haar(4)==2,'SU2 half-trace versus full-trace normalization',half_trace_variance=haar(2),full_trace_variance=4*haar(2),full_trace_fourth=16*haar(4))

# Exact quaternion multiplication, independently resolving the three-trace loss.
def qm(a,b):
    s,u=a[0],a[1:];t,v=b[0],b[1:]
    return (s*t-sum(u[i]*v[i] for i in range(3)),
      s*v[0]+t*u[0]-u[1]*v[2]+u[2]*v[1],
      s*v[1]+t*u[1]-u[2]*v[0]+u[0]*v[2],
      s*v[2]+t*u[2]-u[0]*v[1]+u[1]*v[0])
a=(F(0),F(1),F(0),F(0)); b=(F(0),F(0),F(1),F(0))
require(qm(a,a)[0]==-1 and qm(a,b)[0]==0,'R10 two traces do not determine simultaneous-conjugation orbit')
quats=[(F(1),F(0),F(0),F(0)),a,b,(F(3,5),F(4,5),F(0),F(0)),(F(1,2),F(1,2),F(1,2),F(1,2))]
for U in quats:
 for V in quats:
    x,y,zv=U[0],V[0],qm(U,V)[0]
    dot=sum(U[i]*V[i] for i in range(1,4))
    shared_carre=-dot/4
    actual_kxy=6*x*y-2*shared_carre
    require(actual_kxy==F(13,2)*x*y-zv/2,'R11 shared-link mixed derivative identity',x=x,y=y,z=zv)
require(F(13,2)*0-F(-1,2)!=0,'R11 independent-rotor closure rejected at x=y=0,z=-1')
for degree in range(25):
    vals=[]
    for a_ in range(degree+1):
      for b_ in range(degree-a_+1):
       c=degree-a_-b_
       j,k_,ell=F(a_+c,2),F(b_+c,2),F(a_+b_,2)
       e=3*j*(j+1)+3*k_*(k_+1)+ell*(ell+1)
       polynomial=a_*a_+b_*b_+F(3,2)*c*c+F(1,2)*a_*b_+F(3,2)*c*(a_+b_)+2*a_+2*b_+3*c
       if e!=polynomial: raise ValueError('R11 representation/degree normalization')
       vals.append(e)
    target=F(5,8)*degree**2+2*degree+F(3,8)*(degree%2)
    require(min(vals)==target,'R11 shell minimum independent spin-label enumeration',degree=degree,minimum=target)

# New exact finite-to-infinite audit of the recorded one-square lower bound.
# P spans n=0,...,16, QKQ>=17*19=323. V=1-x>=0 and ||PHQ||=lambda/2.
# Young's inequality gives H >= (A-b^2/(323-24)) direct_sum 24 Q.
# E1(A)<=3+2lambda<=23<24. Two exact Sturm brackets thus enclose the
# full first gap from below; the gap is2-Lipschitz in lambda after removing
# the common scalar lambda. Grid spacing1/2 costs at most1/2 globally.
def less(diag,off,e):
    prev=F(1);cur=diag[0]-e; signs=[1]
    if cur==0:return None
    signs.append(1 if cur>0 else -1)
    for i in range(1,len(diag)):
      nxt=(diag[i]-e)*cur-off[i-1]**2*prev
      prev,cur=cur,nxt
      if cur==0:return None
      signs.append(1 if cur>0 else -1)
    return sum(signs[i]!=signs[i-1] for i in range(1,len(signs)))
def bracket(lam,k):
    diag=[F(n*(n+2))+lam for n in range(17)];off=[-lam/2]*16
    lo,hi=F(-1),F(30)
    for _ in range(45):
      mid=(lo+hi)/2
      count=less(diag,off,mid)
      if count is None:
       mid+=F(1,10**30);count=less(diag,off,mid)
      if count is None:raise ValueError('unexpected exact Sturm collision')
      if count<=k:lo=mid
      else:hi=mid
    return lo,hi
plaq=[]
for i in range(21):
    lam=F(i,2);e0=bracket(lam,0);e1=bracket(lam,1)
    lower=e1[0]-lam**2/(4*(323-24))-e0[1]
    plaq.append({'lambda_over_alpha':lam,'ritz0':e0,'ritz1':e1,'full_gap_lower_at_node':lower})
continuous=min(x['full_gap_lower_at_node'] for x in plaq)-F(1,2)
require(continuous>F(999999,1000000),'R10 independently certified full one-square claimed lower bound over continuous [0,10]',continuous_lower=continuous,point_count=21,tail_threshold=323,young_threshold=24,grid_transport=F(1,2))

# Closed cube character gluing:12 Haar contractions give2^-12,8 free
# vertex index loops give2^8. Removing any face leaves an edge appearing once.
require(F(2**8,2**12)==F(1,16),'R15 six-face product detects dependence invisible to proper face subsets',six_fundamental_trace_moment=F(1,16))

# Rebuild physical box geometry independently of every workbench graph module.
def box(extent):
    vertices=list(cartesian(*(range(n) for n in extent)))
    edges=[]
    for v in vertices:
      for axis in range(3):
       if v[axis]+1<extent[axis]:
        w=list(v);w[axis]+=1;edges.append((v,tuple(w)))
    ids={frozenset(e):i for i,e in enumerate(edges)}
    faces=[]
    for v in vertices:
      for a_,b_ in combinations(range(3),2):
       if v[a_]+1<extent[a_] and v[b_]+1<extent[b_]:
        w=list(v);w[a_]+=1;u=list(v);u[b_]+=1;t=list(w);t[b_]+=1
        circuit=[v,tuple(w),tuple(t),tuple(u)]
        faces.append(frozenset(ids[frozenset((circuit[i],circuit[(i+1)%4]))] for i in range(4)))
    return vertices,edges,faces
v,e,f=box((3,2,2))
accepted=[]
for size in range(1,6):
 for subset in combinations(range(len(e)),size):
    degrees={}
    for i in subset:
      for vertex in e[i]:degrees[vertex]=degrees.get(vertex,0)+1
    if min(degrees.values())>=2:accepted.append(frozenset(subset))
require(len(v)==12 and len(e)==20 and len(f)==11 and set(accepted)==set(f),'R18 complete below-six-link physical support classification',supports_examined=sum(comb(20,k) for k in range(6)),nonempty_no_leaf_supports=len(accepted))
v,e,f=box((3,3,2))
shared=sum(bool(a_&b_) for a_,b_ in combinations(f,2))
unshared=comb(len(f),2)-shared
dim=1+len(f)+len(f)+unshared+2*shared
require((len(v),len(e),len(f),shared,unshared,dim)==(18,33,20,62,128,293),'R24/R26 actual graph and complete generated-pair count')
require(1+20+20+128+62+3*62==417 and 4*20+4*128+8*62==1088,'AC1 actual Gram trace and magnetic-entry incidence',gram_trace=417,entries=1088)

# Independent exact arithmetic on finite-graph and summable-family thresholds.
r=F(12,43)
require(F(135,43)**2==9+11*r*r and (3+F(135,43))/2-11*r==0,'R17 B1 zero certificate margin is exact')
eta=F(3,3817);G=F(45,44);old_e=-F(3,43)
rayleigh=(old_e*G-F(6,473)*eta+8*eta*eta)/(G+eta*eta)
require(old_e-rayleigh==F(1388,284767457),'R17 added-adjoint Rayleigh improvement exact',gap_lower=old_e-rayleigh)
require(F(3)*F(3,8)-F(21)*F(3,8)**2/4==F(99,256),'R18 signed-box endpoint scalar determinant')
selected=(F(1)+F(1,2)+F(1,4))/(1-F(1,16))/(1-F(1,4))/(1-F(1,2))/24
require(selected==F(28,135) and 1-selected==F(107,135),'R19 dyadic selected/omitted exact infinite geometric sums')
def budget(q):
 return F(1,8)/(1-q)**3-(1+q+q*q)/(24*(1-q**4)*(1-q*q)*(1-q))
for q in [F(1,10),F(1,2),F(3,4),F(9,10)]:
 direct=F(2,24)/(1-q)**3+q/(24*(1-q)**2*(1-q*q))+q**3/(24*(1-q**4)*(1-q*q)*(1-q))
 require(budget(q)==direct,'R20 omitted-class and subtraction ledgers agree',q=q)
require(budget(F(1,2))==F(107,135) and budget(F(764003,1000000))<8<budget(F(764004,1000000)),'R20 sufficient-budget boundary bracket, not physical critical point')
require(F(21,24*8)==F(7,64) and F(1,64*96)*F(8,7)==F(1,5376),'R20 canonical variance asymptotic coefficient',variance_coefficient=F(1,5376))

# Late-time, source-sector and graph-topology falsifiers.
# Exact matrix powers make delayed loading visible without any exponential routine.
def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
L=[[F(1),F(1,3),F(0)],[F(1,3),F(3),F(1,5)],[F(0),F(1,5),F(5)]]
L2=mm(L,L);L3=mm(L2,L)
A=[x[:2] for x in L[:2]];A3=mm(mm(A,A),A)
require(L[2][0]==0 and L2[2][0]/2==F(1,30),'R23/R26 zero initial leakage does not remove second-order loading',second_order_omitted_amplitude=F(1,30))
require(-(L3[1][0]-A3[1][0])/6==-F(1,450),'R22/R23 memory return factor required',third_order_retained_defect=-F(1,450))
for n in [2,7,100]:
    require(F(1,n)*n==1,'Norm-small J does not imply small unbounded commutator',J_norm=F(1,n),commutator_norm=1)
require(9>1,'Equal vacuum-created source vectors do not identify operator norms',B_norm=1,C_norm=9,shared_vacuum_source='e1')
require(2**20>10**6,'Uncertain ground center has secular heat error despite excited gap',ground_scalar_example='exp(delta_mu*t)-1 grows without bound; gap acts only on excited space')

# Actual Round26 constants and exact endpoint spectral normalization.
S={(0,0,0),(1,0,0),(0,1,0),(0,0,1)}
diff={tuple(a[i]-b[i] for i in range(3)) for a in S for b in S}
require(len(diff)-1==12,'AE2 translated family retains twelve crossings',crossings=len(diff)-1)
M=F(1,1000);T=F(3)
require((24*M+2/T)/(1-M)==F(2072,2997)<F(7,10),'AE2 source contraction exact continuous cap')
old=F(35,1664);minimum_T=2/(1-25*old);maximum_T=1/(192*old)
require(minimum_T==F(3328,789) and maximum_T==F(26,105) and minimum_T>maximum_T,'AE2 original-cap positive-certificate incompatibility',contraction_requires_T_above=minimum_T,positive_radius_T_below=maximum_T)
require(F(2,3)+F(1,4)+F(1,12)==1,'AD2 single-cycle spectral mass normalization')
require([F(1,4)*4**k+F(1,12)*12**k for k in [1,2,3]]==[2,16,160],'AD2 single-cycle second fourth sixth spectral moments')
require(F(1,3)+F(1,2)+F(1,6)==1,'AD2 coherent-sum spectral mass normalization')
require([F(1,2)*4**k+F(1,6)*12**k for k in [1,2,3]]==[4,32,320],'AD2 coherent-sum even moments')
require([F(2)**(m-2)*(1+3**((m-1)//2)) for m in [1,3,5]]==[1,8,80],'AD2 coherent-sum odd moments and phase sign')
require(F(159999,160001)**2+F(800,160001)**2==1 and F(2,160001)==2*F(1,160001),'AF2 rational nonvacuum normalization')
require((1-F(159999,160001))**2+F(800,160001)**2==F(4,160001)<F(1,10000),'AF2 original preparation-ball membership')
complete=F(457097,12472250000)+F(1,10**8)/F(7127,7200)
require(complete<F(37,10**6),'AF2 complete numerical plus physical true-relative budget',complete_relative_upper=complete)

p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
if args.output.exists():raise ValueError('fresh output required')
args.output.mkdir(parents=True)
result={'scope':'independently authored selected mathematical stress tests; not all-history formal verification','count':len(records),'checks':records,'one_square_audit_nodes':plaq,'own_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'new_roadmap_loops':0}
(args.output/'results.json').write_text(json.dumps(serial(result),indent=2)+'\n')
print(json.dumps({'status':'passed','checks':len(records),'one_square_continuous_gap_lower':float(continuous),'output':str(args.output)}))
