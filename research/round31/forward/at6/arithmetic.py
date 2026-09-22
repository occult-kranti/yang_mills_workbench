#!/usr/bin/env python3
"""Exact-rational zero-selected AQ local-reference calculator.

Only the admitted comparison domain is accepted. No floating input is treated
as certified data; every emitted endpoint and admission decision is rational.
"""
from fractions import Fraction as Q
from math import isqrt
import hashlib
import re
DEN=10**30

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def down(x):
    return Q((x.numerator*DEN)//x.denominator,DEN)

def up(x):
    return Q(-((-x.numerator*DEN)//x.denominator),DEN)

def textq(x):
    x=Q(x)
    return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'

def interval(lo,hi):
    require(lo<=hi,'inverted rigorous interval')
    return {'lower':textq(lo),'upper':textq(hi)}

def exp_negative(x):
    """P_41 <= exp(-z) <= P_40 on [0,1/2]; halve then square."""
    x=Q(x); require(x>=0,'negative decay argument')
    halvings=0
    while x>Q(1,2):
        x/=2; halvings+=1
    total=Q(1); term=Q(1); even=None
    for k in range(1,42):
        term*=(-x)/k; total+=term
        if k==40: even=total
    lo,hi=down(total),up(even)
    require(0<=lo<=hi<=1,'invalid alternating exponential bracket')
    for _ in range(halvings):
        lo,hi=down(lo*lo),up(hi*hi)
    return lo,hi

def log_small(y):
    """For 1<=y<=2, log y=2 sum z^(2k+1)/(2k+1)."""
    y=Q(y); require(1<=y<=2,'log_small domain')
    z=(y-1)/(y+1); terms=64
    partial=2*sum((z**(2*k+1)/Q(2*k+1) for k in range(terms)),Q(0))
    tail=2*z**(2*terms+1)/(Q(2*terms+1)*(1-z*z))
    return down(partial),up(partial+tail)

def log_positive(y):
    y=Q(y); require(y>=1,'log domain')
    shifts=0
    while y>2:
        y/=2; shifts+=1
    lo,hi=log_small(y); l2,u2=log_small(Q(2))
    return down(lo+shifts*l2),up(hi+shifts*u2)

def atan_interval(z):
    z=Q(z); require(0<=z<=Q(1,5),'atan domain')
    total=Q(0); lower=None; upper=None
    for k in range(80):
        total+=(-1 if k%2 else 1)*z**(2*k+1)/Q(2*k+1)
        if k==78: upper=total
        if k==79: lower=total
    return down(lower),up(upper)

def pi_interval():
    a,b=atan_interval(Q(1,5)); c,d=atan_interval(Q(1,239))
    return down(16*a-4*d),up(16*b-4*c)

def sqrt_interval(x):
    x=Q(x); require(x>=0,'sqrt domain')
    k=isqrt((x.numerator*DEN*DEN)//x.denominator)
    lo=Q(k,DEN); hi=lo if lo*lo==x else Q(k+1,DEN)
    require(lo*lo<=x<=hi*hi,'sqrt bracket failed')
    return lo,hi


def exact(value,name):
    if isinstance(value,bool) or isinstance(value,float):
        raise ValueError(name+': exact rational input required; bool/float rejected')
    if isinstance(value,Q):
        return value
    if isinstance(value,int):
        return Q(value)
    if not isinstance(value,str) or not re.fullmatch(r'[+-]?(?:[0-9]+/[0-9]+|[0-9]+(?:\.[0-9]*)?|\.[0-9]+)',value):
        raise ValueError(name+': expected integer, exact decimal or numerator/denominator text')
    try:
        return Q(value)
    except (ValueError,ZeroDivisionError) as error:
        raise ValueError(name+': invalid rational') from error

def certify(*,tau='1/100000000000000',s='1',L='1000000000',target='1/1000000',
            selected=('0','0','0'),alpha='1',hbar='1',E_star='1',lattice_spacing='1',fixed_design=False):
    """Enclose actual centered AQ C_tau(s), not an arbitrary supplied observation.

    Domain: zero selected triple, |tau|<=1e-8, s,L and physical scales positive.
    The target is a requested absolute point-error radius. A valid domain can
    correctly return target_met=False. `fixed_design=True` enforces AT5 values.
    """
    if type(fixed_design) is not bool:
        raise ValueError('fixed_design must be a Boolean')
    data={name:exact(value,name) for name,value in {
        'tau':tau,'s':s,'L':L,'target':target,'alpha':alpha,'hbar':hbar,
        'E_star':E_star,'lattice_spacing':lattice_spacing}.items()}
    if not isinstance(selected,(tuple,list)) or len(selected)!=3:
        raise ValueError('selected must contain exactly three coefficients')
    selected=tuple(exact(x,'selected') for x in selected)
    if any(selected):
        raise ValueError('proved calculator domain requires selected triple zero')
    if abs(data['tau'])>Q(1,100000000):
        raise ValueError('coupling exceeds admitted AQ cap')
    if any(data[name]<=0 for name in ('s','L','target','alpha','hbar','E_star','lattice_spacing')):
        raise ValueError('times, cutoff, target and physical scales must be positive')
    expected={'tau':Q(1,10**14),'s':Q(1),'L':Q(10**9),'target':Q(1,10**6)}
    if fixed_design and any(data[k]!=v for k,v in expected.items()):
        raise ValueError('changed AT5 fixed design; use reusable mode with explicit scope')
    coupling=abs(data['tau']); clock=data['s']; cutoff=data['L']
    # Admitted AT4 factor-six and positive-effect tail refinement.
    _,sqrt_upper=sqrt_interval(Q(49,3)*coupling)
    D=2*sqrt_upper; k=Q(49,4)*coupling
    pi_lower,pi_upper=pi_interval()
    _,log_upper=log_positive(1+(cutoff/clock)**2)
    costs={'state':D,'centering':D*D,
           'real_time_comparison':k*clock*log_upper/pi_lower,
           'Poisson_tail':(Q(1,2)+D/2)*2*clock/(pi_lower*cutoff)}
    # At exactly zero coupling, the model equals the free product reference.
    # Use that exact identity, rather than retain a fictitious finite-cutoff tail.
    if not coupling:
        costs={name:Q(0) for name in costs}
    free_lo,free_hi=exp_negative(3*clock); free_lo/=4; free_hi/=4
    datum=(free_lo+free_hi)/2
    arithmetic=(free_hi-free_lo)/2
    analytic=sum(costs.values(),Q(0)); radius=analytic+arithmetic
    lo,hi=datum-radius,datum+radius
    free_included=lo<=free_lo and free_hi<=hi
    require(free_included,'comparison interval must retain the exact free reference')
    require(hi-lo==2*radius,'width and radius mismatch')
    return {
        'model':'actual centered zero-selected patterned full-Z3 AQ Wilson; chosen subsequential state at specified tau',
        'parameters':{name:textq(value) for name,value in data.items()},'selected_coefficients_over_alpha':[textq(x) for x in selected],
        'fixed_design':fixed_design,'actual_aq_enclosure':True,'nonzero_interacting_coupling':bool(coupling),
        'exact_zero_reference_branch':not bool(coupling),
        'certified_datum':textq(datum),'certified_absolute_error':textq(radius),
        'actual_C_interval':interval(lo,hi),'interval_width':textq(hi-lo),
        'target_met':radius<=data['target'],'free_reference_included':free_included,
        'resolved_interaction_shift':False,'free_C_interval':interval(free_lo,free_hi),
        'costs':{**{name:textq(value) for name,value in costs.items()},'arithmetic':textq(arithmetic)},
        'state_distance_upper':textq(D),'local_reference_gap':'6','duhamel_slope':textq(k),
        'physical_Euclidean_time':textq(data['hbar']*clock/data['alpha']),
        'physical_real_time_cutoff':textq(data['hbar']*cutoff/data['alpha']),
        'alpha_over_E_star':textq(data['alpha']/data['E_star']),
        'energy_clock':'s=alpha*t_E/hbar; AQ normalized time u=s/8',
        'uniform_wilson_claim':False,'continuum_claim':False,'state_uniqueness_claim':False,
        'inverse_response_evaluated':False,'scientific_priority_verified':False,
        'scope':'analytic model enclosure, not a finite-box solver observation or detected interaction shift'
    }
