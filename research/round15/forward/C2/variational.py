"""A finite-cube full-operator gap bound from a seven-state variational upper bound."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parent
SOURCE_BYTES=Path(__file__).read_bytes();SOURCE_SHA=hashlib.sha256(SOURCE_BYTES).hexdigest()
INPUTS={
 'B1/cube.py':'d0df83cd06d062ae525f91bfc2c53eb4beacfdb8d467fe2000449e2e20a38107',
 'B1/graph.json':'4e85817855a880ce5f48e6b3995adca6852557d55103623bb0d686295f334f65',
 'B1/output/moments.json':'863d88c35c36e9ffbdd7f28698aa64544e2abcef3af33efad990788dbe012739',
 'C1/spectral_bound.py':'0fcad91d2bc6c22ec65614f38b6367c1a8145f5d889fe187b966d32a8ce315f8'}
SCHEMA='ym15-cube-variational-gap-v1'
def unchanged():
    if Path(__file__).read_bytes()!=SOURCE_BYTES:raise ValueError('source changed')
    for name,sha in INPUTS.items():
        if hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest()!=sha:raise ValueError('frozen input changed '+name)
def rational(v):
    if type(v) is not str or len(v)>1000:raise ValueError('canonical rational string required')
    try:x=F(v)
    except (ValueError,ZeroDivisionError) as exc:raise ValueError('invalid rational') from exc
    if str(x)!=v:raise ValueError('noncanonical rational')
    return x
def sqrt_interval(q,bits):
    if type(q) is not F or q<0:raise ValueError('nonnegative Fraction radicand required')
    if type(bits) is not int or not 0<=bits<=4096:raise ValueError('bits must be integer0..4096')
    pn=math.isqrt(q.numerator);pd=math.isqrt(q.denominator)
    if pn*pn==q.numerator and pd*pd==q.denominator:return F(pn,pd),F(pn,pd)
    scale=2**bits
    p=math.isqrt(q.numerator*scale*scale//q.denominator)
    lo=F(p,scale);hi=F(p+1,scale)
    if not 0<=lo<=hi or lo*lo>q or hi*hi<q:raise ValueError('radical enclosure defect')
    return lo,hi
def fixture_check():
    data=json.loads((ROOT.parent/'B1/output/moments.json').read_text())
    if len(data['character_gram'])!=36 or len(data['character_triples'])!=216:raise ValueError('missing B1 trial fixture')
    expected_pairs=[[p,q,str(int(p==q))] for p in range(6) for q in range(6)]
    expected_triples=[[p,q,r,'0'] for p in range(6) for q in range(6) for r in range(6)]
    if not typed_equal(data['character_gram'],expected_pairs) or not typed_equal(data['character_triples'],expected_triples):raise ValueError('trial Gram or potential fixture mismatch')
def common_range(r):
    if type(r) is not F or r<0:raise ValueError('nonnegative Fraction ratio required')
    if r<F(12,23):return 'strictly-positive-exact-bound'
    if r==F(12,23):return 'zero-bound-insufficient'
    return 'negative-bound-insufficient'
def certify(alpha='1',couplings=None,bits=48,precision='1/1000000000000'):
    unchanged();fixture_check();a=rational(alpha);tol=rational(precision)
    if a<=0 or tol<=0:raise ValueError('positive alpha and precision required')
    if type(couplings) is not list or len(couplings)!=6:raise ValueError('six cube couplings required')
    ls=list(map(rational,couplings));delta=3*a;L=sum(map(abs,ls),F(0));Q=sum((x*x for x in ls),F(0));rad=delta*delta+Q
    lo,hi=sqrt_interval(rad,bits)
    e0=((delta-hi)/2,(delta-lo)/2)
    bound=((delta+lo)/2-L,(delta+hi)/2-L)
    status='certified-positive' if bound[0]>0 else 'zero-bound-insufficient' if bound[0]==bound[1]==0 else 'negative-bound-insufficient' if bound[1]<0 else 'inconclusive-enclosure'
    gram=[[str(int(i==j)) for j in range(7)] for i in range(7)]
    matrix=[[F(0) for _ in range(7)] for _ in range(7)]
    for p,l in enumerate(ls):matrix[0][p+1]=matrix[p+1][0]=-l/2;matrix[p+1][p+1]=delta
    common=len(set(map(abs,ls)))==1;ratio=abs(ls[0])/a if common else None
    return {'schema':SCHEMA,'source_sha256':SOURCE_SHA,'input_hashes':dict(INPUTS),
      'scope':{'graph':'one cube, six simple square loops','group':'SU(2)',
               'Hilbert':'untruncated gauge-invariant link L2 Haar; Gauss all8vertices, no charges',
               'operator':'H=alpha*sum_e J_e^2-sum_p lambda_p Tr(U_p)/2',
               'interpretation':'full-operator lower bound from independent E1 lower and trial E0 upper',
               'uniform_threshold':'open; this is a finite cube result'},
      'alpha':str(a),'couplings':list(map(str,ls)),'bits':bits,'precision':str(tol),
      'delta':str(delta),'L':str(L),'Q':str(Q),'radicand':str(rad),'sqrt_interval':list(map(str,(lo,hi))),
      'gram':gram,'trial_hamiltonian':[[str(x) for x in row] for row in matrix],
      'trial_minimum_interval':list(map(str,e0)),'full_E0_upper':str(e0[1]),
      'full_E1_lower':str(delta-L),'gap_bound_interval':list(map(str,bound)),
      'certified_gap_lower':str(bound[0]),'bound_interval_width':str(bound[1]-bound[0]),
      'precision_status':'target-met' if bound[1]-bound[0]<tol else 'insufficient-precision',
      'status':status,'common_magnitude_ratio':str(ratio) if ratio is not None else None,
      'common_range_status':common_range(ratio) if common else 'not-common-magnitude'}
def typed_equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(typed_equal(a[k],b[k]) for k in b)
    if type(a) is list:return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b
def verify(certificate):
    if type(certificate) is not dict or certificate.get('schema')!=SCHEMA:raise ValueError('wrong certificate schema')
    expected=certify(certificate.get('alpha'),certificate.get('couplings'),certificate.get('bits'),certificate.get('precision'))
    if not typed_equal(certificate,expected):raise ValueError('variational arithmetic, trial fixtures or semantics mismatch')
    return True
