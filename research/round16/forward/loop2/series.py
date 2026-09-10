"""Exact total-action Taylor certificates for the eleven-face two-cube observable."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from types import MappingProxyType
import hashlib,json,math
ROOT=Path(__file__).resolve().parent
SOURCE_BYTES=Path(__file__).read_bytes();SOURCE_SHA=hashlib.sha256(SOURCE_BYTES).hexdigest()
INPUT_HASHES=MappingProxyType({'graph.json':'9e630191189fb3f69145e5cdbc91eceac138f95d44d7bed825b87b572b322e62',
 'two_cube.py':'13a82e2b804f07d7dbe8951f600ded429d4924b042162ec79d60c2889b767a80',
 'output/exact_evidence.json':'f0120c5508014a9f49e241eac666a56b7b1a86cac323f0eb364cec5974de333e'})
SCHEMA='ym16-two-cube-taylor-v1';MAX_DEGREE=24
FIXTURE_IDS=('zero','negative_shared','omitted_shared','half_shared','full_shared','outer_zero','unequal_signed')
def unchanged():
    if Path(__file__).read_bytes()!=SOURCE_BYTES:raise ValueError('source changed after load')
    for p,h in INPUT_HASHES.items():
        if hashlib.sha256((ROOT.parent/'loop1'/p).read_bytes()).hexdigest()!=h:raise ValueError('frozen Loop1 input changed '+p)
def graph():
    unchanged();return json.loads((ROOT.parent/'loop1/graph.json').read_text())
def rational(v):
    if type(v) is not str or len(v)>1000:raise ValueError('canonical rational string required')
    try:x=F(v)
    except (ValueError,ZeroDivisionError) as exc:raise ValueError('invalid rational') from exc
    if str(x)!=v:raise ValueError('noncanonical rational')
    return x
def degree(n):
    if type(n) is not int or not 0<=n<=MAX_DEGREE:raise ValueError('degree must be integer0..24, not Boolean')
    return n
def parameters(values):
    if type(values) is not list or len(values)!=11:raise ValueError('eleven exact face coefficients required')
    values=tuple(map(rational,values))
    if any(abs(x)>1 for x in values):raise ValueError('implementation coupling cap|k_f|<=1')
    return values
def multiply(a,b,n):
    result=[F(0)]*(n+1)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b[:n-i+1]):
                if y:result[i+j]+=x*y
    return tuple(result)
def character_series(label,coupling,n,insert=False):
    degree(n)
    if type(label) is not int or not 0<=label<=MAX_DEGREE+1 or type(insert) is not bool:raise ValueError('invalid character label or insertion flag')
    if type(coupling) is not F:raise ValueError('character helper coupling must be Fraction')
    return _character_series(label,coupling,n,insert)
@lru_cache(maxsize=16384)
def _character_series(label,coupling,n,insert):
    out=[F(0)]*(n+1)
    for j in range((n+2)//2+1):
        p=label+2*j
        coef=F(label+1,2**p*math.factorial(j)*math.factorial(label+1+j))
        if insert:
            if 1<=p<=n+1:out[p-1]+=p*coef*coupling**(p-1)
        elif p<=n:out[p]+=coef*coupling**p
    return tuple(out)
@lru_cache(maxsize=4096)
def _disk(couplings,label,n,insert):
    p=(F(1),)+(F(0),)*n
    for c in couplings:p=multiply(p,character_series(label,c,n,insert),n)
    return tuple(x/F((label+1)**4) for x in p)
def polynomials(couplings,n):
    values=parameters(couplings);n=degree(n);g=graph()
    regions=tuple(f['region'] for f in g['faces'])
    return _polynomials(values,n,regions)
@lru_cache(maxsize=128)
def _polynomials(couplings,n,regions):
    left=tuple(c for c,r in zip(couplings,regions) if r=='left');right=tuple(c for c,r in zip(couplings,regions) if r=='right');shared=next(c for c,r in zip(couplings,regions) if r=='shared')
    answers=[]
    for insert in (False,True):
        limit=n//5+(1 if insert else 0);result=[F(0)]*(n+1)
        for a in range(limit+1):
            l=_disk(left,a,n,insert)
            if not any(l):continue
            for b in range(limit+1):
                r=_disk(right,b,n,insert)
                if not any(r):continue
                lr=multiply(l,r,n)
                for c in range(abs(a-b),a+b+1,2):
                    s=character_series(c,shared,n,insert);term=multiply(lr,s,n)
                    for j,x in enumerate(term):result[j]+=x
        answers.append(tuple(result))
    return tuple(answers)
def tail(m,n):
    ratio=m/F(n+2)
    if ratio>=1:raise ValueError('tail requires N+2>M')
    return m**(n+1)/math.factorial(n+1)/(1-ratio),ratio
def quotient(a,b):
    if b[0]<=0 or b[0]>b[1]:raise ValueError('positive ordered normalization required')
    corners=[x/y for x in a for y in b];return min(corners),max(corners)
def strict_equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict_equal(a[k],b[k]) for k in b)
    if type(a) is list:return len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b))
    return a==b
def certify(couplings,n=24,precision='1/1000000000000'):
    unchanged();values=parameters(couplings);n=degree(n);tol=rational(precision)
    if tol<=0:raise ValueError('precision must be positive')
    m=sum(map(abs,values),F(0));err,ratio=tail(m,n)
    zpoly,apoly=polynomials(couplings,n);z=sum(zpoly,F(0));a=sum(apoly,F(0))
    zi=(max(F(1),z-err),z+err);ai=(a-err,a+err)
    if zi[1]<zi[0]:raise ValueError('Jensen/Taylor normalization intersection empty')
    expectation=quotient(ai,zi);width=expectation[1]-expectation[0]
    return {'schema':SCHEMA,'source_sha256':SOURCE_SHA,'loop1_input_hashes':dict(INPUT_HASHES),
      'face_order':[f['id'] for f in graph()['faces']],'couplings':list(map(str,values)),'degree':n,'precision':str(tol),
      'scope':{'graph':'adjacent two cubes with shared face included once','measure':'normalized product Haar on20links',
               'observable':'product of all11 normalized face traces; fixed for every fixture',
               'generator':'none; finite Euclidean action'},
      'bookkeeping':'epsilon scales original action; distinct face insertion before argument substitution; evaluate epsilon1',
      'absolute_exponent_bound':str(m),'tail':{'ratio':str(ratio),'remainder':str(err),'first_omitted_degree':n+1},
      'polynomial_coefficients':{'Z':list(map(str,zpoly)),'A':list(map(str,apoly))},
      'polynomial_values':{'Z':str(z),'A':str(a)},'enclosures':{'Z':list(map(str,zi)),'A':list(map(str,ai)),'expectation':list(map(str,expectation))},
      'width':str(width),'precision_status':'target-met' if width<=tol else 'insufficient-width',
      'sign_status':'positive' if expectation[0]>0 else 'negative' if expectation[1]<0 else 'zero' if expectation[0]==expectation[1]==0 else 'inconclusive'}
def verify(c):
    if type(c) is not dict or c.get('schema')!=SCHEMA:raise ValueError('wrong certificate schema')
    if not strict_equal(c,certify(c.get('couplings'),c.get('degree'),c.get('precision'))):raise ValueError('coefficient, normalization, scope or semantic replay failure')
    return True
def fixture_parameters():
    g=graph();shared=next(i for i,f in enumerate(g['faces']) if f['region']=='shared');left=next(i for i,f in enumerate(g['faces']) if f['region']=='left')
    def base(h):
        v=['1/8']*11;v[shared]=h;return v
    zero=['0']*11;outerzero=zero.copy();outerzero[shared]='1/8'
    unequal=base('1/16');unequal[left]='-1/16'
    return {'zero':zero,'negative_shared':base('-1/8'),'omitted_shared':base('0'),
      'half_shared':base('1/16'),'full_shared':base('1/8'),'outer_zero':outerzero,'unequal_signed':unequal}
def difference(full,omitted,precision='1/1000000000000'):
    verify(full);verify(omitted);tol=rational(precision)
    if tol<=0:raise ValueError('positive comparison precision required')
    fixtures=fixture_parameters()
    if full['couplings']!=fixtures['full_shared'] or omitted['couplings']!=fixtures['omitted_shared'] or full['degree']!=omitted['degree']:
        raise ValueError('primary difference parameters or degrees mismatch')
    f0,f1=map(F,full['enclosures']['expectation']);o0,o1=map(F,omitted['enclosures']['expectation'])
    interval=(f0-o1,f1-o0);width=interval[1]-interval[0]
    return {'degree':full['degree'],'full':full,'omitted':omitted,'difference_interval':list(map(str,interval)),
      'width':str(width),'precision':str(tol),'status':'target-met' if interval[0]>0 and width<=tol else 'insufficient',
      'sign_status':'positive' if interval[0]>0 else 'inconclusive'}
def make_collection():
    params=fixture_parameters();records=[]
    if FIXTURE_IDS!=tuple(params):raise ValueError('required fixture inventory changed in memory')
    for n in (0,6,12,18,24):records.append(difference(certify(params['full_shared'],n),certify(params['omitted_shared'],n)))
    fixtures=[{'id':i,'certificate':certify(params[i],24)} for i in FIXTURE_IDS]
    return {'schema':'ym16-two-cube-collection-v1','source_sha256':SOURCE_SHA,'loop1_input_hashes':dict(INPUT_HASHES),
      'primary_target':'E_all11(full shared1/8)-E_all11(omitted shared0), fixed outer1/8, same observable and graph',
      'required_fixture_ids':list(FIXTURE_IDS),'refinement':records,'fixtures':fixtures,
      'degree_cap':24,'primary_index':4,'primary_status':records[-1]['status']}
def verify_collection(c):
    if type(c) is not dict or c.get('schema')!='ym16-two-cube-collection-v1':raise ValueError('wrong collection schema')
    if not strict_equal(c,make_collection()):raise ValueError('collection fixture inventory or arithmetic replay failed')
    return True
