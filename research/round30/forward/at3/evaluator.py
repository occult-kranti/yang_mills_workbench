#!/usr/bin/env python3
"""Exact, conditional AT3 finite-readout API. No AQ data are provided here.

evaluate(samples, T='128', h='1/32', N=4096, epsilon='1/1000000')
accepts 4097 exact rational values or [lower,upper] arithmetic enclosures.
Caller must independently guarantee a real observed sample in every enclosure
and deterministic |observed_j-C(jh)|<=epsilon. Returned interval is conditional
on that guarantee and the AT1/AT2 AQ moment hypotheses. Floats are rejected.
"""
from fractions import Fraction as F

SCALE=10**30
A=F(1,16); MASS=F(63,250); FIRST=F(94,125)
DESIGN_T=F(128); DESIGN_H=F(1,32); DESIGN_N=4096; DESIGN_EPS=F(1,1000000)

def rational(x):
    if isinstance(x,bool) or isinstance(x,float) or not isinstance(x,(int,str,F)):
        raise ValueError('exact finite rational input required; floating values rejected')
    try:return F(x)
    except (ValueError,ZeroDivisionError) as exc:raise ValueError('invalid rational input') from exc

def ceil_fraction(x): return -((-x.numerator)//x.denominator)

def exp_negative_interval(y):
    """Enclose exp(-y) by alternating rational Taylor and directed grid rounding."""
    y=rational(y)
    if y<0:raise ValueError('nonnegative argument required')
    if y==0:return (F(1),F(1))
    r=y;k=0
    while r>F(1,2):r/=2;k+=1
    total=F(1);term=F(1);lower=None
    for n in range(1,41):
        term*=(-r)/n;total+=term
        if n==39:lower=total
    upper=total
    lo=(lower*SCALE).__floor__();hi=ceil_fraction(upper*SCALE)
    for _ in range(k):
        lo=lo*lo//SCALE;hi=(hi*hi+SCALE-1)//SCALE
    return F(lo,SCALE),F(hi,SCALE)

def evaluate(samples,*,T='128',h='1/32',N=4096,epsilon='1/1000000'):
    T=rational(T);h=rational(h);epsilon=rational(epsilon)
    if type(N) is not int or N!=DESIGN_N or (T,h,epsilon)!=(DESIGN_T,DESIGN_H,DESIGN_EPS) or T!=N*h:
        raise ValueError('design/error contract mismatch')
    if not isinstance(samples,(list,tuple)) or len(samples)!=N+1:
        raise ValueError('exactly 4097 samples required')
    traplo=F(0);traphi=F(0)
    for j,item in enumerate(samples):
        if isinstance(item,(tuple,list)):
            if len(item)!=2:raise ValueError('sample enclosure must have two endpoints')
            lo,hi=(rational(t) for t in item)
        else:lo=hi=rational(item)
        if lo>hi:raise ValueError('reversed sample enclosure')
        weight=h/2 if j in (0,N) else h
        traplo+=weight*lo;traphi+=weight*hi
    tail_lo,tail_hi=exp_negative_interval(A*T)
    tail_hi*=MASS/A
    quadrature=h*h*FIRST/8;noise=T*epsilon
    lower=traplo-quadrature-noise;upper=traphi+tail_hi+noise
    return {'lower':lower,'upper':upper,'width':upper-lower,'trap_lower':traplo,'trap_upper':traphi,'arithmetic_trap_width':traphi-traplo,'quadrature_allowance':quadrature,'noise_allowance':noise,'tail_upper':tail_hi,'conditional_on_sample_contract':True,'computed_AQ_samples':False,'target_width_passed':upper-lower<=F(1,500)}

def fixture_nodes(atoms):
    """All 4097 nodes, only for declared abstract atoms (weight, energy)."""
    lo=[F(0)]*(DESIGN_N+1);hi=[F(0)]*(DESIGN_N+1)
    for weight,x in atoms:
        weight=rational(weight);x=rational(x)
        if weight<=0 or x<A:raise ValueError('positive spectral fixture required')
        qlo,qhi=exp_negative_interval(x*DESIGN_H)
        # qlo/qhi have fixed SCALE denominators after reduction; integer lift exact.
        ql=int(qlo*SCALE);qh=int(qhi*SCALE);pl=ph=SCALE
        for j in range(DESIGN_N+1):
            lo[j]+=weight*F(pl,SCALE);hi[j]+=weight*F(ph,SCALE)
            if j<DESIGN_N:
                pl=pl*ql//SCALE;ph=(ph*qh+SCALE-1)//SCALE
    return list(zip(lo,hi))
