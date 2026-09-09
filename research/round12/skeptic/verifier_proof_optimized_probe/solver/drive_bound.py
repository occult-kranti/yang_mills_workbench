"""Exact analytic Hilbert-space Galerkin error bounds for the round-11 graph.

The certificate bounds exact evolution versus exact Galerkin evolution. It does
not certify floating time stepping, coordinate conditioning or a sampled residual.
"""
from fractions import Fraction as F
from math import factorial,isfinite
from pathlib import Path
from functools import lru_cache
import hashlib,json

ROOT=Path(__file__).resolve().parent
CONTRACT='ym12-seven-link-driven-galerkin-v1'
SCOPE='two-adjacent-open-plaquettes-seven-links-gauge-invariant-infinite-representation-space'
DEPENDENCY_PATHS=('vendor/two_plaquette.py','vendor/round11_run_study.py')
ROUND11_DIGEST='ae9084850538ebf523f8c34564352b48ce0b30d07955991d4b4d1980ab36ce43'
ROUND11_PROTOCOL_DIGEST='65f4b186bb34c1659ae16c61c681cb5105264052fd638367b5172bc4da1f0cea'

def rat(value):
    if isinstance(value,bool):raise ValueError('Boolean is not a rational parameter')
    try:return F(str(value)) if isinstance(value,float) else F(value)
    except (ValueError,TypeError,ZeroDivisionError,OverflowError) as exc:raise ValueError('finite rational parameter required') from exc

def nonnegative_int(v,name):
    if type(v) is not int or v<0:raise ValueError(name+' must be a nonnegative integer')
    return v

def expected_dependencies():
    manifest=ROOT/'dependencies.json'
    if manifest.is_symlink() or manifest.resolve().parent!=ROOT:raise ValueError('substituted dependency manifest path')
    record=json.loads(manifest.read_text())
    if set(record)!={'expected_dependencies'} or not isinstance(record['expected_dependencies'],list):raise ValueError('dependency manifest schema')
    deps=record['expected_dependencies']
    if len(deps)!=len(DEPENDENCY_PATHS) or {d.get('path') for d in deps}!=set(DEPENDENCY_PATHS):raise ValueError('complete expected dependency set required')
    for d in deps:
        expected={'vendor/two_plaquette.py':{'path':'vendor/two_plaquette.py','sha256':ROUND11_DIGEST,'original_project_path':'research/round11/solver/two_plaquette.py','role':'exact-seven-link-kinetic-and-Haar-matrices'},'vendor/round11_run_study.py':{'path':'vendor/round11_run_study.py','sha256':ROUND11_PROTOCOL_DIGEST,'original_project_path':'research/round11/solver/run_study.py','role':'original-drive-protocol-provenance'}}
        if d!=expected[d['path']]:raise ValueError('fixed round11 dependency identity mismatch')
        p=ROOT/d['path']
        if p.is_symlink() or p.resolve().parent!=ROOT/'vendor':raise ValueError('substituted dependency path')
        digest=d['sha256']
        if not isinstance(digest,str) or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest):raise ValueError('dependency digest syntax')
        if hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise ValueError('round11 dependency hash mismatch')
    return deps

def source_hashes():
    deps=expected_dependencies()
    return {**{d['path']:d['sha256'] for d in deps},'dependencies.json':hashlib.sha256((ROOT/'dependencies.json').read_bytes()).hexdigest(),'drive_bound.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

def canonical_protocol(p):
    if not isinstance(p,dict) or 'kind' not in p:raise ValueError('protocol object required')
    kind=p['kind']
    if kind in ('cosine_ramp','constant'):
        if set(p)!={'kind','duration','lambda1_scale','lambda2_scale'}:raise ValueError('protocol fields mismatch')
        T,s1,s2=map(rat,(p['duration'],p['lambda1_scale'],p['lambda2_scale']))
        if T<0:raise ValueError('duration must be nonnegative')
        return {'kind':kind,'duration':str(T),'lambda1_scale':str(s1),'lambda2_scale':str(s2)}
    if kind=='piecewise_constant':
        if set(p)!={'kind','segments'} or not isinstance(p['segments'],list) or not p['segments']:raise ValueError('nonempty segment list required')
        segments=[]
        for seg in p['segments']:
            if not isinstance(seg,dict) or set(seg)!={'duration','lambda1','lambda2'}:raise ValueError('segment fields mismatch')
            T,s1,s2=map(rat,(seg['duration'],seg['lambda1'],seg['lambda2']))
            if T<=0:raise ValueError('each segment duration must be positive')
            segments.append({'duration':str(T),'lambda1':str(s1),'lambda2':str(s2)})
        return {'kind':kind,'segments':segments}
    raise ValueError('unsupported protocol kind')

def duration(protocol):
    p=canonical_protocol(protocol)
    return rat(p['duration']) if p['kind']!='piecewise_constant' else sum((rat(s['duration']) for s in p['segments']),F(0))

@lru_cache(None)
def pi_interval():
    """Machin formula, exact alternating-series enclosures; no machine pi premise."""
    def atan_bounds(q,n=20):
        x=F(1,q);s=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(n)),F(0))
        nxt=x**(2*n+1)/F(2*n+1)
        return (s,s+nxt) if n%2==0 else (s-nxt,s)
    a,b=atan_bounds(5);c,d=atan_bounds(239)
    return 16*a-4*d,16*b-4*c

def outward(lo,hi,denominator=10**12):
    if type(denominator) is not int or denominator<=0:raise ValueError('positive integer denominator required')
    return F((lo.numerator*denominator)//lo.denominator,denominator),F(-((-hi.numerator*denominator)//hi.denominator),denominator)

def _series_interval(s,n):
    """Interval for Σ(k=1..n)(−1)^(k+1)π^(2k)s^(2k+1)/(2k+1)!."""
    pl,pu=pi_interval();lo=hi=F(0)
    for k in range(1,n+1):
        factor=s**(2*k+1)/factorial(2*k+1)
        left=pl**(2*k)*factor;right=pu**(2*k)*factor
        if k%2:lo+=left;hi+=right
        else:lo-=right;hi-=left
    return lo,hi

def action_interval(protocol,time=None):
    """Exact rational enclosure of ∫0^t (|λ1|+|λ2|)ds, including cosine ramp."""
    p=canonical_protocol(protocol);T=duration(p);t=T if time is None else rat(time)
    if t<0 or t>T:raise ValueError('time must lie in declared protocol interval')
    if t==0:return F(0),F(0)
    if p['kind']=='piecewise_constant':
        left=t;A=F(0)
        for seg in p['segments']:
            length=min(left,rat(seg['duration']));A+=length*(abs(rat(seg['lambda1']))+abs(rat(seg['lambda2'])));left-=length
            if left==0:break
        return A,A
    amp=abs(rat(p['lambda1_scale']))+abs(rat(p['lambda2_scale']))
    if p['kind']=='constant' or t==T:return amp*t,amp*t
    # For cosine: A/amp/T = s−sin(πs)/π. Alternating terms decrease because π²/20<1.
    # Fourteen terms give a lower partial sum; thirteen give an upper partial sum.
    s=t/T;lower,_=_series_interval(s,14);_,upper=_series_interval(s,13)
    lo,hi=outward(amp*T*lower,amp*T*upper)
    return max(F(0),lo),min(amp*T,hi)

def factorial_bound(action_upper,degree,initial_degree=0):
    A=rat(action_upper);D=nonnegative_int(degree,'degree');d0=nonnegative_int(initial_degree,'initial degree')
    if A<0 or d0>D:raise ValueError('nonnegative action and initial degree <= cutoff required')
    m=D-d0+1
    return min(F(2),A**m/factorial(m))

def certificate(protocol,degree,initial_degree=0,alpha=1,rho=1,time=None):
    p=canonical_protocol(protocol);a,r=rat(alpha),rat(rho)
    if a<=0 or r<=0:raise ValueError('fixed alpha and rho must be positive')
    D=nonnegative_int(degree,'degree');d0=nonnegative_int(initial_degree,'initial degree')
    if d0>D:raise ValueError('initial subspace must fit in Galerkin space')
    t=duration(p) if time is None else rat(time);lo,hi=action_interval(p,t);m=D-d0+1;raw=hi**m/factorial(m);bound=min(F(2),raw)
    return {'contract':CONTRACT,'scope':SCOPE,'kind':'analytic-Hilbert-space-Galerkin-error-bound','target':'exact-Schrodinger-state-versus-exact-embedded-Galerkin-state','norm':'normalized-product-Haar-L2','initial_state':'any-normalized-vector-in-P_initial_degree','protocol':p,'time':str(t),'alpha':str(a),'rho':str(r),'degree':D,'initial_degree':d0,'factorial_order':m,'action_interval':[str(lo),str(hi)],'uncapped_error_upper':str(raw),'state_error_upper':str(bound),'bound_is_below_trivial_two':bound<2,'time_step_error':'not-certified','coefficient_conditioning_error':'not-certified','status':'certified-analytic-truncation-bound','source_hashes':source_hashes()}

def verify_certificate(c):
    required={'contract','scope','kind','target','norm','initial_state','protocol','time','alpha','rho','degree','initial_degree','factorial_order','action_interval','uncapped_error_upper','state_error_upper','bound_is_below_trivial_two','time_step_error','coefficient_conditioning_error','status','source_hashes'}
    if not isinstance(c,dict) or set(c)!=required:raise ValueError('certificate fields mismatch')
    for key in ('degree','initial_degree','factorial_order'):
        if type(c[key]) is not int:raise ValueError('integer degree/order metadata required')
    if type(c['bound_is_below_trivial_two']) is not bool:raise ValueError('Boolean bound status required')
    expected=certificate(c['protocol'],c['degree'],c['initial_degree'],c['alpha'],c['rho'],c['time'])
    if c!=expected:raise ValueError('analytic certificate arithmetic/scope/dependency mismatch')
    return True

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--degree',type=int,default=4);p.add_argument('--duration',default='2');p.add_argument('--lambda1-scale',default='1/10');p.add_argument('--lambda2-scale',default='3/20');args=p.parse_args()
    c=certificate({'kind':'cosine_ramp','duration':args.duration,'lambda1_scale':args.lambda1_scale,'lambda2_scale':args.lambda2_scale},args.degree);verify_certificate(c);print(json.dumps(c,indent=2))
