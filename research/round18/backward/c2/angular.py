"""Independent conditional angular and semicircle-polynomial two-link oracle."""
from fractions import Fraction as F
from functools import lru_cache
from math import comb,factorial
from pathlib import Path

_SOURCE=Path(__file__).read_bytes()


def unchanged():
    if Path(__file__).read_bytes()!=_SOURCE:raise ValueError('angular source changed after loading')


def rational(value):
    if type(value) is not str:raise ValueError('canonical rational string required')
    try:q=F(value)
    except (ValueError,ZeroDivisionError) as exc:raise ValueError('invalid rational') from exc
    if str(q)!=value:raise ValueError('noncanonical rational')
    return q


def exponents(e):
    if type(e) not in (list,tuple) or len(e)!=3 or any(type(x) is not int or x<0 for x in e) or sum(e)>16:raise ValueError('three nonnegative exact integer exponents, total at most16 required')
    return tuple(e)


def semicircle(n):
    if type(n) is not int or n<0:raise ValueError('nonnegative exact integer power required')
    if n%2:return F(0)
    m=n//2;return F(comb(2*m,m),4**m*(m+1))


@lru_cache(maxsize=None)
def _block(p,j):
    return sum(((-1)**k*comb(j,k)*semicircle(p+2*k) for k in range(j+1)),F(0))


@lru_cache(maxsize=None)
def _moment(e):
    a,b,c=e
    return sum((F(comb(c,2*j),2*j+1)*_block(a+c-2*j,j)*_block(b+c-2*j,j) for j in range(c//2+1)),F(0))


def moment(e):
    unchanged();return _moment(exponents(e))


def multiply(p,q):
    out={}
    for e,v in p.items():
        for f,w in q.items():
            k=tuple(x+y for x,y in zip(e,f));out[k]=out.get(k,F(0))+v*w
    return {k:v for k,v in out.items() if v}


def observable():
    x={(2,0,0):F(4),(0,0,0):F(-1)};p={(0,0,0):F(1)}
    for _ in range(3):p=multiply(p,x)
    p=multiply(p,{(0,0,2):F(4),(0,0,0):F(-1)})
    return {e:v/81 for e,v in p.items()}


def coefficients(d,degree=8):
    unchanged()
    if type(d) is not int or d not in (0,1,2):raise ValueError('V-only multiplicity must be exact0,1,2')
    if type(degree) is not int or not 0<=degree<=8:raise ValueError('exact diagnostic degree from0through8 required')
    S={(1,0,0):F(3),(0,0,1):F(1)}
    if d:S[(0,1,0)]=F(d)
    p={(0,0,0):F(1)};O=observable();A=[];Z=[];used=set()
    for n in range(degree+1):
        op=multiply(O,p);used.update(p);used.update(op)
        A.append(sum((v*moment(e) for e,v in op.items()),F(0))/factorial(n))
        Z.append(sum((v*moment(e) for e,v in p.items()),F(0))/factorial(n))
        p=multiply(p,S)
    return {'d':d,'degree':degree,'numerator_coefficients':list(map(str,A)),'partition_coefficients':list(map(str,Z)),
      'used_exponents':[list(e) for e in sorted(used)],'primitive_moments':[{'exponents':list(e),'moment':str(moment(e))} for e in sorted(used)]}


def interval(lo,hi):return {'lower':str(lo),'upper':str(hi),'width':str(hi-lo)}


def certify(d,kappa,degree=8,precision='1/1000000000000'):
    unchanged();k=rational(kappa);eps=rational(precision)
    if eps<=0:raise ValueError('positive requested precision required')
    c=coefficients(d,degree);M=(4+d)*abs(k)
    if M>=degree+2:raise ValueError('selected geometric Taylor-tail ratio must be less than one')
    tail=M**(degree+1)/factorial(degree+1)/(1-M/F(degree+2))
    A=sum((F(a)*k**n for n,a in enumerate(c['numerator_coefficients'])),F(0));Z=sum((F(z)*k**n for n,z in enumerate(c['partition_coefficients'])),F(0))
    al,ah=A-tail,A+tail;zl,zh=max(F(1),Z-tail),Z+tail
    if not 0<zl<=zh:raise ValueError('invalid positive partition interval')
    corners=[a/z for a in (al,ah) for z in (zl,zh)];lo,hi=min(corners),max(corners)
    return {'d':d,'kappa':str(k),'degree':degree,'precision':str(eps),'M':str(M),'tail':str(tail),
      'numerator_coefficients':c['numerator_coefficients'],'partition_coefficients':c['partition_coefficients'],
      'numerator_polynomial':str(A),'partition_polynomial':str(Z),'numerator_interval':interval(al,ah),'partition_interval':interval(zl,zh),
      'expectation_interval':interval(lo,hi),'width_status':'target-met' if hi-lo<=eps else 'insufficient-width',
      'sign_status':'positive' if lo>0 else 'negative' if hi<0 else 'exact-zero' if lo==hi==0 else 'unresolved',
      'scope':'conditional integral over two Haar links with31otherlinks fixed; no bulk or spectral claim'}


def collection():
    unchanged()
    models=[coefficients(d) for d in (2,1,0)]
    used=[(a,b,n-a-b) for n in range(17) for a in range(n+1) for b in range(n-a+1)]
    return {'schema':'ym18-independent-c2-angular-v1','models':models,
      'primitive_moments':[{'exponents':list(e),'moment':str(moment(e))} for e in used],
      'refinements':[certify(2,'1/64',n) for n in (0,2,4,6,8)],
      'fixtures':[{'id':f'd{d}_{name}','certificate':certify(d,k)} for d in (2,1,0) for name,k in [('positive','1/64'),('zero','0'),('negative','-1/64')]]}


def strict(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict(a[k],b[k]) for k in a)
    if type(a) in (list,tuple):return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b
