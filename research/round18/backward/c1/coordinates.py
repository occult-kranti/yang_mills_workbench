"""Independent four-coordinate S3 polynomial oracle and full Gram validation."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations,product
from math import factorial
from pathlib import Path
import hashlib

_SOURCE=Path(__file__).read_bytes()


def unchanged():
    if Path(__file__).read_bytes()!=_SOURCE:raise ValueError('coordinate source changed after load')


def rational(x,canonical=False):
    if canonical and type(x) is not str:raise ValueError('canonical rational string required')
    if type(x) not in (str,int,F):raise ValueError('exact rational required, not Boolean or floating point')
    q=F(x)
    if type(x) is str and str(q)!=x:raise ValueError('canonical rational encoding required')
    return q


def vector(v):
    if type(v) not in (tuple,list) or len(v)!=4:raise ValueError('four exact coordinates required')
    return tuple(rational(x) for x in v)


def exponents(e,dimension):
    if type(e) not in (tuple,list) or len(e)!=dimension or any(type(x) is not int or x<0 for x in e) or sum(e)>14:raise ValueError('correct-dimensional nonnegative integer exponents of total at most14 required')
    return tuple(e)


def sphere(e):
    unchanged();return _sphere(exponents(e,4))


@lru_cache(maxsize=None)
def _sphere(e):
    if any(x%2 for x in e):return F(0)
    m=[x//2 for x in e];M=sum(m)
    return F(product_factorials([2*x for x in m]),4**M*product_factorials(m)*factorial(M+1))


def product_factorials(values):
    n=1
    for x in values:n*=factorial(x)
    return n


def add(a,b):
    c=dict(a)
    for e,v in b.items():c[e]=c.get(e,F(0))+v
    return {e:v for e,v in c.items() if v}


def multiply(a,b):
    c={}
    for e,v in a.items():
        for f,w in b.items():
            key=tuple(x+y for x,y in zip(e,f));c[key]=c.get(key,F(0))+v*w
    return {e:v for e,v in c.items() if v}


def linear(v):
    return {tuple(int(i==j) for i in range(4)):q for j,q in enumerate(v) if q}


def power(p,n):
    result={(0,0,0,0):F(1)}
    for _ in range(n):result=multiply(result,p)
    return result


def integrate(p):
    return sum((v*_sphere(e) for e,v in p.items()),F(0))


def coordinate_moment(vectors,k):
    unchanged()
    if type(vectors) not in (list,tuple) or len(vectors)!=5:raise ValueError('five four-coordinate vectors required')
    vs=tuple(vector(v) for v in vectors);k=exponents(k,5)
    return _coordinate_moment(vs,k)


@lru_cache(maxsize=None)
def _coordinate_moment(vs,k):
    if sum(k)%2:return F(0)
    p={(0,0,0,0):F(1)}
    for v,n in zip(vs,k):
        if n:p=multiply(p,power(linear(v),n))
    return integrate(p)


def determinant(matrix):
    a=[list(row) for row in matrix];n=len(a);det=F(1)
    for j in range(n):
        pivot=next((i for i in range(j,n) if a[i][j]),None)
        if pivot is None:return F(0)
        if pivot!=j:a[pivot],a[j]=a[j],a[pivot];det=-det
        q=a[j][j];det*=q
        for i in range(j+1,n):
            ratio=a[i][j]/q
            for k in range(j+1,n):a[i][k]-=ratio*a[j][k]
            a[i][j]=F(0)
    return det


def rank(matrix):
    a=[list(row) for row in matrix];p=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(p,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[pivot],a[p]=a[p],a[pivot];q=a[p][j]
        for i in range(p+1,len(a)):
            ratio=a[i][j]/q
            for k in range(j,len(a[0])):a[i][k]-=ratio*a[p][k]
        p+=1
        if p==len(a):break
    return p


def validate_gram(G,kappa):
    unchanged()
    if type(G) not in (list,tuple) or len(G)!=5 or any(type(r) not in (list,tuple) or len(r)!=5 for r in G):raise ValueError('five-by-five canonical Gram matrix required')
    g=tuple(tuple(rational(x,True) for x in row) for row in G)
    if type(kappa) not in (list,tuple) or len(kappa)!=4:raise ValueError('four canonical action coefficients required')
    k=tuple(rational(x,True) for x in kappa)
    if any(g[i][j]!=g[j][i] for i in range(5) for j in range(5)):raise ValueError('Gram must be symmetric')
    minors=[]
    for size in range(1,6):
        for ids in combinations(range(5),size):
            d=determinant([[g[i][j] for j in ids] for i in ids]);minors.append({'indices':list(ids),'determinant':str(d)})
            if d<0:raise ValueError('Gram has a negative principal minor')
    r=rank(g)
    if r>4:raise ValueError('Gram rank exceeds four-coordinate realization')
    if any(g[i][i]!=1 for i in range(1,5)):raise ValueError('every observable direction must be unit')
    if any(g[0][i]!=sum((k[j]*g[j+1][i] for j in range(4)),F(0)) for i in range(1,5)):raise ValueError('action cross relation fails')
    if g[0][0]!=sum((k[i]*k[j]*g[i+1][j+1] for i in range(4) for j in range(4)),F(0)):raise ValueError('action norm relation fails')
    return {'rank':r,'principal_minors':minors,'positive_semidefinite':True,'b_relation':True}


def data(directions,kappa,degree=6):
    unchanged()
    if type(degree) is not int or not 0<=degree<=6:raise ValueError('auxiliary Taylor degree from zero through six required')
    if type(directions) not in (tuple,list) or len(directions)!=4:raise ValueError('four observable directions required')
    a=tuple(vector(v) for v in directions)
    if any(sum((q*q for q in v),F(0))!=1 for v in a):raise ValueError('unit directions required')
    if type(kappa) not in (tuple,list) or len(kappa)!=4:raise ValueError('four action coefficients required')
    k=tuple(rational(x) for x in kappa);b=tuple(sum((k[i]*a[i][j] for i in range(4)),F(0)) for j in range(4));vs=(b,*a)
    G=[[str(sum((x*y for x,y in zip(u,v)),F(0))) for v in vs] for u in vs];admitted=validate_gram(G,list(map(str,k)))
    O={(0,0,0,0):F(1)}
    for v in a:
        square=multiply(linear(v),linear(v));factor={e:4*q for e,q in square.items()};factor=add(factor,{(0,0,0,0):F(-1)});O=multiply(O,factor)
    O={e:q/81 for e,q in O.items()};action=linear(b);current={(0,0,0,0):F(1)};A=[];Z=[]
    for n in range(degree+1):
        A.append(integrate(multiply(O,current))/factorial(n));Z.append(integrate(current)/factorial(n));current=multiply(current,action)
    return {'directions':[[str(q) for q in v] for v in a],'kappa':list(map(str,k)),'b':list(map(str,b)),
      'vectors':[[str(q) for q in v] for v in vs],'joint_Gram':G,'admissibility':admitted,'degree':degree,
      'numerator_coefficients':list(map(str,A)),'partition_coefficients':list(map(str,Z)),
      'observable_coordinate_polynomial':[{'exponents':list(e),'coefficient':str(q)} for e,q in sorted(O.items())],
      'coefficient_semantics':'[t^n] of numerator or partition for exp(t q dot b), includes1/n!; t is formal and not physical time.',
      'scope':'Exact coefficient diagnostics through finite degree, not a full weighted-integral error certificate; all-order equality under complete Gram is an analytic theorem.'}


def fixtures():
    tetra=[tuple(F(x,2) for x in v) for v in ((1,1,1,1),(1,1,-1,-1),(1,-1,1,-1),(1,-1,-1,1))]
    commuting=[(F(1),F(0),F(0),F(0)),(F(1),F(0),F(0),F(0)),(F(0),F(1),F(0),F(0)),(F(0),F(-1),F(0),F(0))]
    H=[tuple(F(x,2) for x in v) for v in ((1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1))]
    def transform(a):return [tuple(sum((row[j]*v[j] for j in range(4)),F(0)) for row in H) for v in a]
    def reflect(a):return [(-v[0],*v[1:]) for v in a]
    common=['1/16']*4
    return [('tetra_common',tetra,common),('commuting_common',commuting,common),('tetra_hadamard',transform(tetra),common),('commuting_hadamard',transform(commuting),common),
      ('tetra_reflected',reflect(tetra),common),('commuting_reflected',reflect(commuting),common),('rank1_equal',[commuting[0]]*4,common),
      ('rank2',[(1,0,0,0),(0,1,0,0),(F(3,5),F(4,5),0,0),(-F(4,5),F(3,5),0,0)],common),
      ('tetra_zero_kappa',tetra,['0']*4),('tetra_signed_kappa',tetra,['1/16','-1/32','1/8','-3/64']),
      ('commuting_zero_b_nonzero_kappa',commuting,['1/16','-1/16','1/16','1/16'])]


def primitives(vectors,degree=6):
    if type(degree) is not int or not 0<=degree<=6:raise ValueError('diagnostic degree must be an exact integer from zero through six')
    rows=[]
    for n in range(degree+1):
        for mask in range(16):
            e=[n]+[2*((mask>>i)&1) for i in range(4)]
            rows.append({'degree':n,'subset_mask':mask,'exponents':e,'moment':str(coordinate_moment(vectors,e))})
    return rows


def collection():
    unchanged();values=[]
    for name,a,k in fixtures():
        value=data(a,k);value['primitive_moments']=primitives(value['vectors'])
        values.append({'id':name,'data':value})
    return {'schema':'ym18-independent-c1-coordinate-v1','dimension':4,'degree':6,'fixtures':values,
      'oracle':'Direct four-coordinate polynomial multiplication and exact even S3 monomial integration; Gram admissibility uses all principal minors and independent row rank.',
      'scope':'Complete declared central Gram sufficiency is an analytic isometry theorem. Finite Taylor coefficients have no remainder certificate; no surrounding-link measure transformation is inferred.'}


def strict(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict(a[k],b[k]) for k in a)
    if type(a) in (tuple,list):return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b


def verify(value):
    if not strict(value,collection()):raise ValueError('complete independent coordinate evidence differs')
    return True
