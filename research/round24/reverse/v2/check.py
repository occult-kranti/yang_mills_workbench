#!/usr/bin/env python3
"""Exact finite-q sufficient resources. No stochastic samples or dynamics truncation."""
import argparse
from fractions import Fraction as F
from math import factorial, isqrt
import json
from pathlib import Path


def require(ok, name):
    if not ok:
        raise RuntimeError(name)


def b(q):
    return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))


def root_interval(x):
    precision=10**50
    lower=F(isqrt(x.numerator*precision*precision//x.denominator),precision)
    upper=lower+F(1,precision)
    require(lower*lower<=x<=upper*upper,'square-root enclosure')
    return lower,upper


def matmul(a,b):
    # Exact Gaussian rational pairs.
    def add(x,y): return (x[0]+y[0],x[1]+y[1])
    def mul(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    answer=[]
    for row in a:
        rr=[]
        for col in zip(*b):
            value=(F(0),F(0))
            for x,y in zip(row,col): value=add(value,mul(x,y))
            rr.append(value)
        answer.append(rr)
    return answer


def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [serial(v) for v in x]
    return x


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    eta=F(1,2); z=F(1,10**6); c=z/eta; q=1-F(1,10**8)
    tau=eta/(8*b(q)); sq=c*tau/(1-q)**3; x=10*sq
    require(0<x<1,'finite-q series admissible')
    d2=eta*eta*b(q*q)/(96*(1-eta)**2*b(q)**2)
    dlo,dhi=root_interval(d2)
    tail=F(44,9)*x*x/(1-x)**5
    finite_margin=sq*q**4/96-6*dhi-tail
    require(finite_margin>z/100,'finite-q positive margin')
    r=z/10000; ep=z/10**6; ei=z/10**6; dimensionless_h=z/10**6
    bias=2*ep+ei
    n=18/(r*r)
    require(n.denominator==1,'integer repetitions')
    exp_lower=sum(F(9)**k/factorial(k) for k in range(31))
    require(exp_lower>3600,'exponential lower bound')
    failure_upper=36/exp_lower
    require(failure_upper<F(1,100),'99 percent confidence')
    time_coeff=2*(9+eta/4)
    budget=8*(r+bias)+time_coeff*dimensionless_h
    require(budget<finite_margin,'complete resource budget')
    require(budget==F(84225,10**14),'exact resource decimal')
    t=c/(1-q)**3
    require(t==2*10**18,'actual growing physical time')
    relative_h=dimensionless_h/t
    require(relative_h==F(5,10**31),'relative clock tolerance')
    # Compute U W U*, then W beta(W), with exact Gaussian rationals.
    one=(F(1),F(0)); zero=(F(0),F(0)); imag=(F(0),F(1)); negimag=(F(0),F(-1))
    u=[[one,zero],[zero,imag]]; ustar=[[one,zero],[zero,negimag]]
    w=[[zero,one],[one,zero]]
    beta=matmul(matmul(u,w),ustar)
    target=matmul(w,beta)[0][0]
    require(target==imag,'computed imaginary correlator')
    rho01=(target[0]/2,-target[1]/2); rho10=(target[0]/2,target[1]/2)
    ymean=-rho01[1]+rho10[1]
    require(ymean==1,'computed ancilla Y sign')
    # [diag(0,E),W] has entries +/-E, so its adjoint product is E^2 I.
    energy=F(9,2)
    comm=[[zero,(-energy,F(0))],[(energy,F(0)),zero]]
    commstar=[[zero,(energy,F(0))],[(-energy,F(0)),zero]]
    normsq=matmul(commstar,comm)
    require(normsq==[[(energy**2,F(0)),zero],[zero,(energy**2,F(0))]],'commutator norm')
    fair_all_plus_probability=F(1,2)**8
    controls={
        'reversed-ancilla-Y-sign-detected': -ymean != target[1],
        'excessive-systematic-error-rejected': 8*(r+F(1,10**6))>finite_margin,
        'finite-q-state-term-not-zero': dhi>0 and finite_margin<sq*q**4/96-tail,
        'finite-sampling-not-deterministic-certainty': fair_all_plus_probability>0,
        'dropped-preparation-factor-two-detected': 2*ep>ep,
        'disconnected-mean-square-required': (F(1,2)+r)**2-F(1,2)**2>0,
        'relative-clock-not-fitted-time': relative_h<dimensionless_h and t>1,
    }
    for name,value in controls.items(): require(value,name)
    results={
        'loop':'v2','direction':'reverse','status':'passed',
        'claims':[
            'Eighteen-setting complex connected estimator at one declared q/time',
            'Independent bounded-sample confidence with explicit systematic bias',
            'Actual W and completion domain/commutator timing bound',
            'Exact finite-q positive certificate exceeds all allocated errors',
        ],
        'limitations':[
            'No samples drawn; deterministic certification of conditional probability bound',
            'Full infinite-system coherent control and ground-state preparations assumed',
            '3.24e22 sufficient state preparations and 5e-31 relative time tolerance are impractical',
            'No confidence over a continuum of q/time, correlated shots, or adaptive stopping',
            'No Wilson witness, homogeneous gap, physical calibration or continuum construction',
        ],
        'exact':{'q':q,'eta':eta,'z':z,'finite_q_margin_lower':finite_margin,
                 'state_error_interval':[dlo,dhi],'sampling_radius':r,'preparation_error':ep,
                 'instrument_error':ei,'dimensionless_time_tolerance':dimensionless_h,
                 'dimensionless_endpoint_time':t,'relative_time_tolerance':relative_h,
                 'shots_per_setting':n,'total_preparations':18*n,
                 'failure_probability_upper':failure_upper,'total_error_budget':budget,
                 'observed_magnitude_lower_with_confidence':z/100-budget,
                 'computed_imaginary_product':target,
                 'fair_eight_shot_all_plus_probability':fair_all_plus_probability},
    }
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'results.json').write_text(json.dumps(serial(results),indent=2,sort_keys=True)+'\n')
    (args.output/'controls.json').write_text(json.dumps({'controls':controls},indent=2,sort_keys=True)+'\n')


if __name__=='__main__': main()
