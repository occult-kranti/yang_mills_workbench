"""Rational dual-witness bounds for the compact tilted SU(2) Haar hierarchy.

Finite necessary constraints, not a Hamiltonian ground state or mass gap.
The proposer may fail to find an interior point; accepted certificates use
only exact recurrences, quadratic forms and rational arithmetic.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext
from math import gcd,lcm,comb
from pathlib import Path
import hashlib

SCHEMA='su2-compact-moment-dual-v1'
SCOPE='one-plaquette Euclidean tilted Haar probability on [-1,1]; no Hamiltonian or continuum gap'

def rat(x):
    if type(x) not in (int,str,F):raise ValueError('Use an integer or exact rational string/Fraction')
    try:return F(x)
    except (ValueError,ZeroDivisionError) as e:raise ValueError('Finite rational required') from e

def integer(x,lo,hi,name):
    if type(x) is not int or not lo<=x<=hi:raise ValueError(name+' outside declared integer range')
    return x

def parameters(kappa,level,bits):
    k=rat(kappa);r=integer(level,1,6,'level');b=integer(bits,8,96,'bits')
    if abs(k)>100:raise ValueError('Implementation supports |kappa|<=100')
    return k,r,b

def affine(kappa,degree):
    k=rat(kappa);degree=integer(degree,2,12,'moment degree')
    if not k:raise ValueError('Zero coupling uses exact Haar moments, not division')
    out=[(F(1),F(0)),(F(0),F(1))]
    for n in range(degree-1):
        prev=out[n-1] if n else (F(0),F(0))
        out.append(tuple(out[n][j]+(n*prev[j]-(n+3)*out[n+1][j])/k for j in (0,1)))
    return out

def haar(n):
    integer(n,0,100,'Haar moment')
    return F(0) if n%2 else F(comb(n,n//2), (n//2+1)*2**n)

def matrix_pairs(kappa,level,family):
    k=rat(kappa);r=integer(level,1,6,'level');m=affine(k,2*r)
    if family=='H':return [[m[i+j] for j in range(r+1)] for i in range(r+1)]
    if family=='L':return [[tuple(m[i+j][q]-m[i+j+2][q] for q in (0,1)) for j in range(r)] for i in range(r)]
    raise ValueError('Unknown positivity family')

def evaluate(pairs,u):
    u=rat(u)
    return [[a+b*u for a,b in row] for row in pairs]

def quadratic(A,v):
    v=list(map(rat,v));A=[list(map(rat,row)) for row in A];n=len(A)
    if not n or len(v)!=n or any(len(row)!=n for row in A):raise ValueError('Matrix/vector shape mismatch')
    return sum((v[i]*A[i][j]*v[j] for i in range(n) for j in range(n)),F(0))

def primitive(v):
    den=lcm(*(x.denominator for x in v));ints=[int(x*den) for x in v];g=0
    for x in ints:g=gcd(g,abs(x))
    if not g:raise ValueError('Zero witness')
    sign=1 if next(x for x in ints if x)>0 else -1
    return [F(sign*x//g) for x in ints]

def negative_witness(matrix):
    """Exact PSD test; return rational v with v*A*v<0, or None.

    Positive-pivot congruences retain their original-coordinate vectors.
    A zero-diagonal nonzero off-diagonal block is explicitly indefinite.
    """
    A=[list(map(rat,row)) for row in matrix];n=len(A)
    if not n or any(len(row)!=n for row in A) or A!=[list(row) for row in zip(*A)]:raise ValueError('Nonempty symmetric matrix required')
    S=[row[:] for row in A];vectors=[[F(i==j) for i in range(n)] for j in range(n)]
    while S:
        neg=next((i for i in range(len(S)) if S[i][i]<0),None)
        if neg is not None:v=primitive(vectors[neg]);break
        pivot=next((i for i in range(len(S)) if S[i][i]>0),None)
        if pivot is None:
            pair=next(((i,j) for i in range(len(S)) for j in range(i+1,len(S)) if S[i][j]),None)
            if pair is None:return None
            i,j=pair;sgn=1 if S[i][j]>0 else -1
            v=primitive([x-sgn*y for x,y in zip(vectors[i],vectors[j])]);break
        order=[pivot]+[i for i in range(len(S)) if i!=pivot]
        S=[[S[i][j] for j in order] for i in order];vectors=[vectors[i] for i in order];p=S[0][0]
        vectors=[[vectors[i][j]-S[i][0]/p*vectors[0][j] for j in range(n)] for i in range(1,len(S))]
        S=[[S[i][j]-S[i][0]*S[0][j]/p for j in range(1,len(S))] for i in range(1,len(S))]
    if quadratic(A,v)>=0:raise ArithmeticError('Congruence witness failed direct replay')
    return v

def witness(k,r,u):
    u=rat(u)
    for family in ('H','L'):
        pairs=matrix_pairs(k,r,family);v=negative_witness(evaluate(pairs,u))
        if v is None:continue
        c=quadratic([[a for a,b in row] for row in pairs],v)
        d=quadratic([[b for a,b in row] for row in pairs],v)
        if c+d*u>=0:raise ArithmeticError('Expected a separating witness')
        if not d:raise ArithmeticError('Constant infeasibility contradicts the existing measure')
        return {'family':family,'vector':list(map(str,v)),'constant':str(c),'slope':str(d),'root':str(-c/d)}
    return None

def propose_mean(k,binary_digits=384):
    """Decimal Bessel-series proposal only. It is never a certificate premise."""
    with localcontext() as ctx:
        ctx.prec=int(binary_digits*.302)+30
        x=Decimal(k.numerator)/Decimal(k.denominator);y=x*x/4;term=Decimal(1);z=term;dz=Decimal(0)
        for j in range(1,2000):
            term*=y/(j*(j+1));z+=term;dz+=2*j*term/x
            if j>abs(x) and abs(term)<abs(z)*Decimal(10)**(-ctx.prec+5):break
        else:raise RuntimeError('Proposal resource limit; no certificate')
        return F(int((dz/z)*Decimal(2)**binary_digits),2**binary_digits)

def variance_interval(k,l,u):
    if not k:return F(1,4),F(1,4)
    f=lambda x:1-3*x/k-x*x
    candidates=[f(l),f(u)];peak=-F(3,2)/k
    upper=max(candidates+[f(peak)] if l<=peak<=u else candidates)
    return max(F(0),min(candidates)),min(F(1),upper)

def source_hash():return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

def certify(kappa,level,bits=48):
    k,r,b=parameters(kappa,level,bits)
    base={'schema':SCHEMA,'scope':SCOPE,'source_sha256':source_hash(),'kappa':str(k),'level':r,'bits':b,'status':'certified-outer-interval'}
    if not k:
        return {**base,'method':'exact-Haar-zero-coupling','mean_interval':['0','0'],'variance_interval':['1/4','1/4'],'moments':[str(haar(n)) for n in range(2*r+1)]}
    center=None
    for precision in (256,512,1024):
        candidate=propose_mean(k,precision)
        if -1<candidate<1 and witness(k,r,candidate) is None:center=candidate;break
    if center is None:raise RuntimeError('No exact feasible center found; no certificate')
    sides=[]
    for sign in (-1,1):
        outside=F(sign);inside=center;best=witness(k,r,outside)
        if best is None:raise ArithmeticError('Endpoint unexpectedly feasible')
        for _ in range(b):
            mid=(outside+inside)/2;w=witness(k,r,mid)
            if w is None:inside=mid
            else:outside=mid;best=w
        if (F(best['slope'])>0)!=(sign<0):raise ArithmeticError('Separating half-line points in the wrong direction')
        sides.append((best,inside))
    lower=max(F(-1),F(sides[0][0]['root']));upper=min(F(1),F(sides[1][0]['root']))
    v=variance_interval(k,lower,upper)
    result={**base,'method':'exact-affine-PSD-dual-witness','mean_interval':list(map(str,(lower,upper))),
        'variance_interval':list(map(str,v)),'witnesses':[s[0] for s in sides],
        'feasible_inner_points':[str(s[1]) for s in sides],
        'optimization_slack_per_side':str(F(2,2**b))}
    verify(result)
    return result

def verify(c):
    if not isinstance(c,dict):raise ValueError('Certificate object required')
    k,r,b=parameters(c.get('kappa'),c.get('level'),c.get('bits'))
    common={'schema','scope','source_sha256','kappa','level','bits','status','method','mean_interval','variance_interval'}
    extra={'moments'} if not k else {'witnesses','feasible_inner_points','optimization_slack_per_side'}
    if set(c)!=common|extra or c['schema']!=SCHEMA or c['scope']!=SCOPE or c['status']!='certified-outer-interval' or c['source_sha256']!=source_hash():raise ValueError('Certificate semantics/source mismatch')
    if not k:
        expected={**{x:c[x] for x in ('schema','scope','source_sha256','kappa','level','bits','status')},'method':'exact-Haar-zero-coupling','mean_interval':['0','0'],'variance_interval':['1/4','1/4'],'moments':[str(haar(n)) for n in range(2*r+1)]}
        if c!=expected:raise ValueError('Zero-coupling certificate mismatch')
        return True
    if c['method']!='exact-affine-PSD-dual-witness' or type(c['witnesses']) is not list or len(c['witnesses'])!=2:raise ValueError('Two signed dual witnesses required')
    roots=[]
    for index,w in enumerate(c['witnesses']):
        if not isinstance(w,dict) or set(w)!={'family','vector','constant','slope','root'}:raise ValueError('Witness schema mismatch')
        pairs=matrix_pairs(k,r,w['family'])
        if type(w['vector']) is not list or len(w['vector'])!=len(pairs):raise ValueError('Witness dimension mismatch')
        v=list(map(rat,w['vector']))
        if not any(v):raise ValueError('Zero dual witness')
        a=quadratic([[a for a,d in row] for row in pairs],v);d=quadratic([[d for a,d in row] for row in pairs],v)
        if not d or (d>0)!=(index==0):raise ValueError('Wrong half-line direction')
        if rat(w['constant'])!=a or rat(w['slope'])!=d or rat(w['root'])!=-a/d:raise ValueError('Dual arithmetic mismatch')
        roots.append(-a/d)
    l,u=max(F(-1),roots[0]),min(F(1),roots[1])
    if not -1<=l<=u<=1 or c['mean_interval']!=list(map(str,(l,u))):raise ValueError('Mean interval mismatch')
    if c['variance_interval']!=list(map(str,variance_interval(k,l,u))):raise ValueError('Variance propagation mismatch')
    if type(c['feasible_inner_points']) is not list or len(c['feasible_inner_points'])!=2:raise ValueError('Two interior checks required')
    il,iu=map(rat,c['feasible_inner_points']);eps=F(2,2**b)
    if not l<=il<=iu<=u or il-l>eps or u-iu>eps or rat(c['optimization_slack_per_side'])!=eps:raise ValueError('Optimization slack mismatch')
    if witness(k,r,il) is not None or witness(k,r,iu) is not None:raise ValueError('Claimed inner point violates a PSD constraint')
    return True
