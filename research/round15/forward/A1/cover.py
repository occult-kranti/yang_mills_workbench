"""Exact complete parameter covers for the fixed round14 covariance family."""
from __future__ import annotations
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SCHEMA='ym15-covariance-cover-v1'
POINT_SHA='c1141b027f310159494e18a93a8a2afa96073009a9b16f4f7d1a822f96bf4682'
THEOREM_BYTES=(ROOT/'derivation.md').read_bytes()
THEOREM_SHA=hashlib.sha256(THEOREM_BYTES).hexdigest()
SOURCE_BYTES=Path(__file__).read_bytes()
SOURCE_SHA=hashlib.sha256(SOURCE_BYTES).hexdigest()
point_path=ROOT/'vendor/point_certificate.py'
if hashlib.sha256(point_path.read_bytes()).hexdigest()!=POINT_SHA:
    raise ValueError('point producer source hash mismatch')
spec=importlib.util.spec_from_file_location('ym15_pinned_point',point_path)
point=importlib.util.module_from_spec(spec)
spec.loader.exec_module(point)
TARGET=(F(1,8),F(1,4))

def _unchanged():
    if (Path(__file__).read_bytes()!=SOURCE_BYTES or
        (ROOT/'derivation.md').read_bytes()!=THEOREM_BYTES or
        hashlib.sha256(point_path.read_bytes()).hexdigest()!=POINT_SHA):
        raise ValueError('source changed after loading')

def rational(value):
    if type(value) is not str or len(value)>20000:
        raise ValueError('canonical rational string required')
    try:
        v=F(value)
    except (ValueError,ZeroDivisionError) as exc:
        raise ValueError('invalid rational') from exc
    if str(v)!=value:
        raise ValueError('noncanonical rational')
    return v

def count(value,name,maximum=4096):
    if type(value) is not int or not 1<=value<=maximum:
        raise ValueError(name+' must be a positive bounded integer, not Boolean')
    return value

def typed_equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict:
        return set(a)==set(b) and all(typed_equal(a[k],b[k]) for k in b)
    if type(a) is list:
        return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b

def build(edges,degree=24):
    _unchanged()
    if type(edges) is not list or not 2<=len(edges)<=4097:
        raise ValueError('nonempty bounded ordered cover edges required')
    endpoints=[rational(x) for x in edges]
    if endpoints[0]!=TARGET[0] or endpoints[-1]!=TARGET[1]:
        raise ValueError('target endpoints must remain 1/8 and 1/4')
    if any(a>=b for a,b in zip(endpoints,endpoints[1:])):
        raise ValueError('cover edges must be strictly ordered')
    if type(degree) is not int or not 0<=degree<=point.MAX_DEGREE:
        raise ValueError('degree must be a supported integer, not Boolean')
    cells=[]
    for left,right in zip(endpoints,endpoints[1:]):
        center=(left+right)/2; radius=(right-left)/2
        cert=point.certify(F(1),F(1),center,degree)
        lo,hi=map(F,cert['enclosures']['covariance'])
        lower=lo-2*radius; upper=hi+2*radius
        cells.append({'left':str(left),'right':str(right),'center':str(center),
                      'radius':str(radius),'certificate':cert,
                      'transported_lower':str(lower),'transported_upper':str(upper),
                      'status':'positive' if lower>0 else 'insufficient'})
    minimum=min(F(c['transported_lower']) for c in cells)
    return {'schema':SCHEMA,'source_sha256':SOURCE_SHA,
            'point_source_sha256':POINT_SHA,'derivative_source_sha256':THEOREM_SHA,
            'scope':dict(point.SCOPE),'fixed_parameters':{'k1':'1','k2':'1'},
            'target':list(map(str,TARGET)),'lipschitz':'2','degree':degree,
            'cell_count':len(cells),'cells':cells,'minimum_lower':str(minimum),
            'insufficient_indices':[i for i,c in enumerate(cells) if c['status']=='insufficient'],
            'status':'certified-positive-cover' if minimum>0 else 'insufficient-cover'}

def uniform(cells=8,degree=24):
    count(cells,'cell count')
    a,b=TARGET
    return build([str(a+(b-a)*i/cells) for i in range(cells+1)],degree)

def verify(cover):
    _unchanged()
    if type(cover) is not dict or cover.get('schema')!=SCHEMA:
        raise ValueError('wrong cover schema')
    if type(cover.get('cells')) is not list or not cover['cells']:
        raise ValueError('empty/malformed cells')
    count(cover.get('cell_count'),'cell count')
    if len(cover['cells'])!=cover['cell_count']:
        raise ValueError('cell count mismatch')
    edges=[]
    for i,cell in enumerate(cover['cells']):
        if type(cell) is not dict:
            raise ValueError('cell must be an object')
        left=rational(cell.get('left')); right=rational(cell.get('right'))
        if left>=right: raise ValueError('empty or reversed cell')
        if i and left!=rational(cover['cells'][i-1].get('right')):
            raise ValueError('gap or overlap between cells')
        if not i: edges.append(str(left))
        edges.append(str(right))
    expected=build(edges,cover.get('degree'))
    if not typed_equal(cover,expected):
        raise ValueError('cover arithmetic, source, scope or semantics failed replay')
    return True

def save(path,cover):
    verify(cover)
    Path(path).write_text(json.dumps(cover,indent=2)+'\n')
