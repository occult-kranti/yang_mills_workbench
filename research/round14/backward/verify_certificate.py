#!/usr/bin/env python3
"""Independent exact replay of round14 compact two-loop certificates.

No producer code is imported. Taylor coefficients use the frozen Loop1
character/Schur oracle, while the producer uses an angular Beta formula.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import factorial
from pathlib import Path
import copy
import hashlib
import json
import re
import sys

HERE=Path(__file__).resolve().parent
SELF_BYTES=Path(__file__).read_bytes()
ORACLE_PIN='c6779c3151f1803e4baf78671d8e775eaa6baf240f3f943541fbcb2bb4ab5169'
ORACLE_BYTES=(HERE/'oracle.py').read_bytes()
if hashlib.sha256(ORACLE_BYTES).hexdigest()!=ORACLE_PIN:
    raise ValueError('Loop1 oracle differs from accepted frozen source')
_oracle_ns={'__name__':'frozen_independent_character_oracle','__file__':str(HERE/'oracle.py')}
exec(compile(ORACLE_BYTES,str(HERE/'oracle.py'),'exec'),_oracle_ns)
MOMENT=_oracle_ns['haar_moment']
SCHEMA='ym14-two-loop-taylor-certificate-v1'
SCOPE={
 'group':'SU(2)',
 'space':'two holonomies U,V with normalized product Haar measure',
 'exponent':'k1*x+k2*y+eta*z',
 'coordinates':'x=Tr(U)/2; y=Tr(V)/2; z=Tr(UV)/2',
 'observable':'Cov(x,y) in the normalized finite Euclidean measure',
 'limit':'fixed finite action; no Hamiltonian or continuum claim',
}
KEYS={'schema','scope','source_sha256','parameters','degree','absolute_exponent_bound',
      'tail','polynomial_integrals','enclosures','width','status'}
RAW={'Z':(0,0,0),'Ax':(1,0,0),'Ay':(0,1,0),'Axy':(1,1,0)}


def canonical(value):
    if type(value) is not str or len(value)>20000:
        raise ValueError('canonical rational string required')
    try:
        q=Q(value)
    except (ValueError,ZeroDivisionError,OverflowError) as error:
        raise ValueError('invalid rational') from error
    if str(q)!=value:
        raise ValueError('noncanonical rational')
    return q


def integer(value,maximum):
    if type(value) is not int or not 0<=value<=maximum:
        raise ValueError('integer domain/type violation')
    return value


def times(left,right):
    values=tuple(a*b for a in left for b in right)
    return min(values),max(values)


def quotient(numerator,denominator):
    if not 0<denominator[0]<=denominator[1]:
        raise ValueError('denominator is not a positive ordered interval')
    values=tuple(a/b for a in numerator for b in denominator)
    return min(values),max(values)


@lru_cache(maxsize=256)
def exact_data(k1,k2,eta,n):
    # Called only after public parameter/type checks. No external Boolean keys.
    m=abs(k1)+abs(k2)+abs(eta)
    ratio=m/Q(n+2)
    if ratio>=1:
        raise ValueError('tail ratio must be strictly smaller than1')
    remainder=m**(n+1)/factorial(n+1)/(1-ratio)
    parameters=(k1,k2,eta)
    weighted=[[p**j/Q(factorial(j)) for j in range(n+1)] for p in parameters]
    raw={name:Q(0) for name in RAW}
    for a in range(n+1):
        for b in range(n-a+1):
            for c in range(n-a-b+1):
                coefficient=weighted[0][a]*weighted[1][b]*weighted[2][c]
                if coefficient:
                    for name,(i,j,k) in RAW.items():
                        raw[name]+=coefficient*MOMENT(a+i,b+j,c+k)
    intervals={name:(value-remainder,value+remainder) for name,value in raw.items()}
    low,high=intervals['Z']
    intervals['Z']=(max(Q(1),low),high)
    if intervals['Z'][0]>high:
        raise ValueError('empty Jensen-normalizer intersection')
    p=times(intervals['Z'],intervals['Axy'])
    q=times(intervals['Ax'],intervals['Ay'])
    numerator=(p[0]-q[1],p[1]-q[0])
    denominator=tuple(z*z for z in intervals['Z'])
    covariance=quotient(numerator,denominator)
    intervals.update(numerator=numerator,denominator=denominator,covariance=covariance)
    lo,hi=covariance
    status=('certified-positive' if lo>0 else 'certified-negative' if hi<0 else
            'certified-zero' if lo==hi==0 else 'certified-enclosure-inconclusive')
    # Cache an immutable serialization, never an externally mutable expected map.
    return json.dumps({'absolute_exponent_bound':str(m),
            'tail':{'first_omitted_degree':n+1,'ratio_bound':str(ratio),'remainder':str(remainder)},
            'polynomial_integrals':{name:str(v) for name,v in raw.items()},
            'enclosures':{name:[str(v) for v in pair] for name,pair in intervals.items()},
            'width':str(hi-lo),'status':status},sort_keys=True,separators=(',',':'))


def verify(certificate,*,producer_source_sha256):
    """Return True after independent exact replay; every rejected input raises ValueError."""
    if Path(__file__).read_bytes()!=SELF_BYTES or (HERE/'oracle.py').read_bytes()!=ORACLE_BYTES:
        raise ValueError('independent evaluator source changed after loading')
    if type(producer_source_sha256) is not str or not re.fullmatch('[0-9a-f]{64}',producer_source_sha256):
        raise ValueError('expected producer SHA256 is required')
    if type(certificate) is not dict or set(certificate)!=KEYS:
        raise ValueError('certificate field set mismatch')
    if certificate['schema']!=SCHEMA or certificate['source_sha256']!=producer_source_sha256:
        raise ValueError('schema/source binding mismatch')
    if type(certificate['scope']) is not dict or certificate['scope']!=SCOPE:
        raise ValueError('physical scope mismatch')
    params=certificate['parameters']
    if type(params) is not dict or set(params)!={'k1','k2','eta'}:
        raise ValueError('parameter field set mismatch')
    p=tuple(canonical(params[name]) for name in ('k1','k2','eta'))
    if any(abs(v)>8 for v in p) or sum(map(abs,p))>12:
        raise ValueError('couplings outside implementation contract')
    n=integer(certificate['degree'],48)
    tail=certificate['tail']
    if type(tail) is not dict or set(tail)!={'first_omitted_degree','ratio_bound','remainder'}:
        raise ValueError('tail field set mismatch')
    integer(tail['first_omitted_degree'],49)
    # Exact serialization comparison also distinguishes1 from True and1.0.
    expected={'schema':SCHEMA,'scope':SCOPE,'source_sha256':producer_source_sha256,
              'parameters':dict(zip(('k1','k2','eta'),map(str,p))),'degree':n,
              **json.loads(exact_data(*p,n))}
    try:
        actual_json=json.dumps(certificate,sort_keys=True,allow_nan=False,separators=(',',':'))
    except (ValueError,TypeError) as error:
        raise ValueError('non-JSON or nonfinite certificate data') from error
    expected_json=json.dumps(expected,sort_keys=True,allow_nan=False,separators=(',',':'))
    if actual_json!=expected_json:
        raise ValueError('independent exact arithmetic or semantic replay mismatch')
    return True


def audit(collection_path,producer_source,output_dir):
    collection_path=Path(collection_path); producer_source=Path(producer_source)
    producer_bytes=producer_source.read_bytes(); source_sha=hashlib.sha256(producer_bytes).hexdigest()
    collection_bytes=collection_path.read_bytes(); collection=json.loads(collection_bytes)
    if (type(collection) is not dict or set(collection)!={'schema','producer_source_sha256','certificates','status'}
        or collection['schema']!='ym14-two-loop-certificate-collection-v1'
        or collection['producer_source_sha256']!=source_sha
        or collection['status']!='all-certificates-replayed'):
        raise ValueError('collection envelope schema/source/status mismatch')
    entries=collection['certificates']
    if type(entries) is not list or not entries:
        raise ValueError('nonempty certificate collection required')
    identifiers=set();certificates=[]
    for entry in entries:
        if type(entry) is not dict or set(entry)!={'id','certificate'} or type(entry['id']) is not str or not entry['id']:
            raise ValueError('invalid certificate entry')
        if entry['id'] in identifiers:
            raise ValueError('duplicate certificate identifier')
        identifiers.add(entry['id']);certificates.append(entry['certificate'])
    checks=[]
    def gate(name,condition,details=None):
        if not condition:
            raise ValueError(name)
        checks.append({'name':name,'passed':True,'details':details})
    selected=None; inadequate=None; zero=None
    for index,c in enumerate(certificates):
        gate('exact independent fixture '+str(index),verify(c,producer_source_sha256=source_sha),
             {'parameters':c['parameters'],'degree':c['degree'],'status':c['status']})
        if c['parameters']=={'k1':'1','k2':'1','eta':'1/4'}:
            if c['degree']==4:
                inadequate=c
            if Q(c['width'])<=Q(1,10**12) and c['status']=='certified-positive':
                selected=c
        if c['parameters']=={'k1':'0','k2':'0','eta':'0'} and c['degree']==0:
            zero=c
    gate('central rational target certified within requested width',selected is not None)
    gate('inadequate degree4 retained as inconclusive',inadequate is not None and
         inadequate['status']=='certified-enclosure-inconclusive')
    gate('zero-action degree0 fixture present',zero is not None and zero['status']=='certified-zero')
    def rejected(name,c):
        try:
            verify(c,producer_source_sha256=source_sha)
        except ValueError:
            gate(name,True)
            return
        raise ValueError('mutation accepted: '+name)
    mutations=[
      ('schema','bad'),('source_sha256','0'*64),('degree',True),('degree',-1),('degree',49),
      ('absolute_exponent_bound','0'),('width','0'),('status','certified-zero'),
      ('parameters.k1','1.0'),('parameters.k2',True),('parameters.eta',0.25),
      ('parameters.k1','9'),('parameters.k1','1/0'),
      ('tail.first_omitted_degree',True),('tail.ratio_bound','0'),('tail.remainder','0'),
      ('scope.group','U(1)'),('scope.limit','four-dimensional continuum mass gap'),
      ('polynomial_integrals.Axy','0'),('enclosures.covariance',['0','1']),
      ('enclosures.numerator',['1','0']),('enclosures.denominator',['0','1']),
      ('enclosures.Z',['0','1']),
    ]
    for path,value in mutations:
        c=copy.deepcopy(selected); fields=path.split('.'); target=c
        for field in fields[:-1]:
            target=target[field]
        target[fields[-1]]=value
        rejected('mutation '+path+'='+repr(value),c)
    c=copy.deepcopy(selected);c['extra']='unproved premise';rejected('unknown field',c)
    c=copy.deepcopy(selected);del c['tail'];rejected('missing tail field',c)
    c=copy.deepcopy(selected);c['parameters']['extra']='0';rejected('extra parameter',c)
    c=copy.deepcopy(zero);c['tail']['first_omitted_degree']=True
    rejected('nested bool alias at expected integer1',c)
    c=copy.deepcopy(zero);c['tail']['first_omitted_degree']=1.0
    rejected('nested float alias at expected integer1',c)
    c=copy.deepcopy(zero);c['parameters']['k1']='2';c['degree']=0
    rejected('tail ratio equality rejected',c)
    gate('negative numerator division uses all corners',
         quotient((Q(-3),Q(-1)),(Q(2),Q(4)))==(Q(-3,2),Q(-1,4)))
    gate('straddling numerator division uses all corners',
         quotient((Q(-3),Q(1)),(Q(2),Q(4)))==(Q(-3,2),Q(1,2)))
    gate('Schur denominator omission discriminated',MOMENT(1,1,1)==Q(1,16) and Q(1,8)!=MOMENT(1,1,1))
    gate('source unchanged during audit',producer_source.read_bytes()==producer_bytes and
         collection_path.read_bytes()==collection_bytes)
    result={'schema':'ym14-independent-certificate-review-v1','status':'passed','phase':'loop2',
      'check_count':len(checks),'checks':checks,'source_sha256':hashlib.sha256(SELF_BYTES).hexdigest(),
      'reviewed_source_hashes':{'forward/loop2_certificate.py':source_sha,'backward/oracle.py':ORACLE_PIN},
      'collection_sha256':hashlib.sha256(collection_bytes).hexdigest(),
      'certificates_replayed':len(certificates),'central_target':{
        'parameters':selected['parameters'],'degree':selected['degree'],
        'covariance_interval':selected['enclosures']['covariance'],'width':selected['width']},
      'acceptance':'Exact finite Euclidean covariance enclosures and strict semantic/source replay.',
      'limits':['No physical Hamiltonian, mass-gap or continuum inference is admitted.',
                'This conventional rational verifier is not a proof-assistant kernel.',
                'Collection envelope, unique IDs, actual producer bytes and all individual arithmetic are checked.']}
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    (out/'independent_certificate_review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','check_count':len(checks),'certificates':len(certificates)}))
    return result


if __name__=='__main__':
    if len(sys.argv)!=4:
        raise SystemExit('usage: verify_certificate.py COLLECTION PRODUCER_SOURCE OUTPUT_DIR')
    audit(*sys.argv[1:])
