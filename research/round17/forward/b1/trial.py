"""Twelve-state variational upper bound plus independent full E1 lower bound."""
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache
import hashlib,json,math
import haar_graph
SOURCE_BYTES=Path(__file__).read_bytes();SOURCE_SHA=hashlib.sha256(SOURCE_BYTES).hexdigest()
HAAR_SHA='13a82e2b804f07d7dbe8951f600ded429d4924b042162ec79d60c2889b767a80'
GRAPH_SHA='9e630191189fb3f69145e5cdbc91eceac138f95d44d7bed825b87b572b322e62'
def unchanged():
    if Path(__file__).read_bytes()!=SOURCE_BYTES or haar_graph.SOURCE_SHA!=HAAR_SHA or hashlib.sha256((Path(__file__).parent/'haar_graph.py').read_bytes()).hexdigest()!=HAAR_SHA or hashlib.sha256((Path(__file__).parent/'graph.json').read_bytes()).hexdigest()!=GRAPH_SHA:
        raise ValueError('trial or accepted graph/Haar source changed')
def rational(v):
    if type(v) is not str or len(v)>1000:raise ValueError('canonical rational string required')
    try:x=F(v)
    except (ValueError,ZeroDivisionError) as exc:raise ValueError('invalid rational') from exc
    if str(x)!=v:raise ValueError('noncanonical rational')
    return x
def graph():
    unchanged();g=json.loads((Path(__file__).parent/'graph.json').read_text());haar_graph.validate_graph(g);return g
def _index(i,maxi):
    if type(i) is not int or not 0<=i<=maxi:raise ValueError('bounded integer index required, not Boolean')
    return i
def matrix_moment(i,j,face=None):
    i=_index(i,11);j=_index(j,11)
    if face is not None:face=_index(face,10)
    return _matrix_moment(i,j,face)
@lru_cache(maxsize=None)
def _matrix_moment(i,j,face):
    powers=[0]*11;factor=F(1)
    for b in (i,j):
        if b:powers[b-1]+=1;factor*=2
    if face is not None:powers[face]+=1
    return factor*haar_graph.moment(powers)
def matrices(alpha,coefficients):
    unchanged();a=rational(alpha)
    if a<=0:raise ValueError('positive alpha required')
    if type(coefficients) is not list or len(coefficients)!=11:raise ValueError('eleven physical coefficients required')
    ls=tuple(map(rational,coefficients));gram=[];electric=[];potential=[]
    for i in range(12):
        gr=[];er=[];vr=[]
        for j in range(12):
            moment=matrix_moment(i,j);gr.append(moment);er.append((0 if j==0 else 3*a)*moment)
            vr.append(-sum((l*matrix_moment(i,j,f) for f,l in enumerate(ls)),F(0)))
        gram.append(gr);electric.append(er);potential.append(vr)
    h=[[electric[i][j]+potential[i][j] for j in range(12)] for i in range(12)]
    return tuple(tuple(tuple(row) for row in m) for m in (gram,electric,potential,h))
def sqrt_bracket(q,bits):
    if type(q) is not F or q<0 or type(bits) is not int or not 0<=bits<=512:raise ValueError('nonnegative rational radicand and integer bits0..512 required')
    p=math.isqrt(q.numerator);r=math.isqrt(q.denominator)
    if p*p==q.numerator and r*r==q.denominator:return F(p,r),F(p,r)
    d=2**bits;m=math.isqrt(q.numerator*d*d//q.denominator);lo,hi=F(m,d),F(m+1,d)
    if lo*lo>q or hi*hi<q:raise ValueError('radical bracket failed exact squares')
    return lo,hi
def certify(alpha='1',coefficients=None,bits=48,precision='1/1000000000000'):
    a=rational(alpha);tol=rational(precision)
    if a<=0 or tol<=0:raise ValueError('positive alpha and precision required')
    gram,electric,potential,h=matrices(alpha,coefficients);ls=list(map(rational,coefficients));delta=3*a;L=sum(map(abs,ls),F(0));Q=sum((l*l for l in ls),F(0))
    lo,hi=sqrt_bracket(delta*delta+Q,bits);e0=((delta-hi)/2,(delta-lo)/2);bound=((delta+lo)/2-L,(delta+hi)/2-L)
    common=len(set(map(abs,ls)))==1;ratio=abs(ls[0])/a if common else None
    sign='positive' if bound[0]>0 else 'zero-insufficient' if bound[0]==bound[1]==0 else 'negative-insufficient' if bound[1]<0 else 'inconclusive'
    return {'schema':'ym17-two-cube-twelve-state-v1','source_sha256':SOURCE_SHA,'haar_source_sha256':HAAR_SHA,'graph_file_sha256':GRAPH_SHA,
      'alpha':str(a),'coefficients':list(map(str,ls)),'face_order':[f['id'] for f in graph()['faces']],'bits':bits,'precision':str(tol),
      'gram':[[str(x) for x in row] for row in gram],'electric_matrix':[[str(x) for x in row] for row in electric],
      'potential_matrix':[[str(x) for x in row] for row in potential],'trial_H':[[str(x) for x in row] for row in h],
      'delta':str(delta),'L':str(L),'Q':str(Q),'radicand':str(delta*delta+Q),'sqrt_bracket':list(map(str,(lo,hi))),
      'trial_minimum_bracket':list(map(str,e0)),'full_E0_upper':str(e0[1]),'full_E1_lower':str(delta-L),
      'gap_bound_bracket':list(map(str,bound)),'gap_lower':str(bound[0]),'width':str(bound[1]-bound[0]),
      'precision_status':'target-met' if bound[1]-bound[0]<=tol else 'insufficient-width','sign_status':sign,
      'common_magnitude_ratio':str(ratio) if common else None,
      'common_exact_classification':'positive' if common and ratio<F(12,43) else 'zero-insufficient' if common and ratio==F(12,43) else 'negative-insufficient' if common else 'not-common-magnitude',
      'scope':'Untruncated physical dense two-cube operator; separate E1 lower and trial E0 upper; bracket encloses sufficient lower-bound formula, not actual gap; sparse theorem inapplicable'}
def verify(c):
    if type(c) is not dict or c.get('schema')!='ym17-two-cube-twelve-state-v1':raise ValueError('wrong certificate schema')
    expected=certify(c.get('alpha'),c.get('coefficients'),c.get('bits'),c.get('precision'))
    if not haar_graph.strict_equal(c,expected):raise ValueError('trial, bound or physical contract failed replay')
    return True
