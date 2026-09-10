"""Exact total-degree Taylor enclosures for one closed cube Wilson graph."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib,math
ROOT=Path(__file__).resolve().parent
B1=ROOT.parent/'B1'
GRAPH_SHA='4e85817855a880ce5f48e6b3995adca6852557d55103623bb0d686295f334f65'
B1_SOURCE_SHA='d0df83cd06d062ae525f91bfc2c53eb4beacfdb8d467fe2000449e2e20a38107'
SOURCE_BYTES=Path(__file__).read_bytes();SOURCE_SHA=hashlib.sha256(SOURCE_BYTES).hexdigest()
SCHEMA='ym15-cube-taylor-certificate-v1'
def unchanged():
    if (Path(__file__).read_bytes()!=SOURCE_BYTES or hashlib.sha256((B1/'graph.json').read_bytes()).hexdigest()!=GRAPH_SHA or hashlib.sha256((B1/'cube.py').read_bytes()).hexdigest()!=B1_SOURCE_SHA):
        raise ValueError('frozen source or graph changed')
def rational(v):
    if type(v) is not str or len(v)>20000:raise ValueError('canonical rational string required')
    try:a=F(v)
    except (ValueError,ZeroDivisionError) as exc:raise ValueError('invalid rational') from exc
    if str(a)!=v:raise ValueError('noncanonical rational')
    return a
def degree(v):
    if type(v) is not int or not 0<=v<=48:raise ValueError('degree must be integer0..48')
    return v
def convolution(a,b,n):
    out=[F(0)]*(n+1)
    for i,x in enumerate(a):
        if not x:continue
        for j,y in enumerate(b[:n-i+1]):
            if y:out[i+j]+=x*y
    return out
def power6(a,n):
    out=[F(1)]+[F(0)]*n
    for _ in range(6):out=convolution(out,a,n)
    return out
def character_series(r,n,insert=False):
    degree(n)
    if type(r) is not int or not 0<=r<=9 or type(insert) is not bool:
        raise ValueError('invalid character index or insertion flag')
    # a_r(k)=sum_j (r+1)k^(r+2j)/(2^(r+2j)j!(r+1+j)!).
    out=[F(0)]*(n+1)
    for j in range((n+1)//2+2):
        p=r+2*j
        if insert:
            if p==0 or p-1>n:continue
            out[p-1]+=F((r+1)*p,2**p*math.factorial(j)*math.factorial(r+1+j))
        elif p<=n:out[p]+=F(r+1,2**p*math.factorial(j)*math.factorial(r+1+j))
    return out
def polynomials(n):
    return _polynomials(degree(n))
@lru_cache(maxsize=128)
def _polynomials(n):
    z=[F(0)]*(n+1);o=[F(0)]*(n+1)
    for r in range(n//6+2):
        zp=power6(character_series(r,n),n)
        op=power6(character_series(r,n,True),n)
        for j in range(n+1):
            z[j]+=zp[j]/(r+1)**4;o[j]+=op[j]/(r+1)**4
    # Product of six independent one-face partitions is precisely r=0 term.
    factorized=power6(character_series(0,n),n)
    return tuple(z),tuple(o),tuple(factorized)
def evaluate(coeff,k):return sum((c*k**i for i,c in enumerate(coeff)),F(0))
def tail(m,n):
    q=m/F(n+2)
    if q>=1:raise ValueError('tail requires N+2>M')
    return m**(n+1)/math.factorial(n+1)/(1-q),q
def divide_positive(a,b):
    if b[0]<=0 or b[0]>b[1]:raise ValueError('nonpositive normalization interval')
    c=[x/y for x in a for y in b]
    return min(c),max(c)
def typed_equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(typed_equal(a[k],b[k]) for k in b)
    if type(a) is list:return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b
def certify(k='1/4',n=24,precision='1/1000000000000'):
    unchanged();k=rational(k);n=degree(n);tol=rational(precision)
    if abs(k)>1 or tol<=0:raise ValueError('implementation requires |k|<=1 and positive precision')
    m=6*abs(k);err,ratio=tail(m,n)
    coeffs=polynomials(n);z,o,zind=[evaluate(c,k) for c in coeffs]
    zi=(max(F(1),z-err),z+err);oi=(o-err,o+err)
    independent=(max(F(1),zind-err),zind+err)
    if zi[1]<zi[0] or independent[1]<independent[0]:raise ValueError('Jensen/Taylor empty normalization')
    expected=divide_positive(oi,zi)
    excess=(zi[0]-independent[1],zi[1]-independent[0])
    width=expected[1]-expected[0]
    return {'schema':SCHEMA,'source_sha256':SOURCE_SHA,'graph_file_sha256':GRAPH_SHA,'b1_source_sha256':B1_SOURCE_SHA,
      'scope':{'graph':'closed oriented cube boundary','measure':'normalized product Haar on12 links',
               'action':'k*sum_f Tr(U_face_f)/2','observable':'product_f Tr(U_face_f)/2',
               'generator':'none; finite Euclidean measure'},
      'k':str(k),'degree':n,'precision':str(tol),'absolute_exponent_bound':str(m),
      'tail':{'remainder':str(err),'ratio':str(ratio),'first_omitted_degree':n+1},
      'polynomial_coefficients':{name:list(map(str,c)) for name,c in zip(('Z','Aproduct','Zindependent'),coeffs)},
      'polynomial_values':{'Z':str(z),'Aproduct':str(o),'Zindependent':str(zind)},
      'enclosures':{name:list(map(str,v)) for name,v in [('Z',zi),('Aproduct',oi),('Zindependent',independent),('expectation',expected),('partition_excess',excess)]},
      'expectation_width':str(width),'expectation_status':'target-certified' if width<tol else 'insufficient-width',
      'partition_excess_status':'certified-positive' if excess[0]>0 else 'inconclusive',
      'derivative_convention':'one derivative per distinct face coefficient, then all k_f=k'}
def verify(cert):
    unchanged()
    if type(cert) is not dict or cert.get('schema')!=SCHEMA:raise ValueError('wrong certificate schema')
    expected=certify(cert.get('k'),cert.get('degree'),cert.get('precision'))
    if not typed_equal(cert,expected):raise ValueError('cube arithmetic, convention, source or semantics mismatch')
    return True
