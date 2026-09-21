#!/usr/bin/env python3
"""Exact constants and outward rational spectral/heat fixtures; no physical cutoff."""
from fractions import Fraction as F
from math import isqrt, factorial
from pathlib import Path
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from t2_common import need, emit

DEN = 2**100


def rounded(lo, hi):
    need(lo <= hi, 'reversed interval')
    return (F((lo*DEN).__floor__(), DEN), F((hi*DEN).__ceil__(), DEN))


def add(a, b):
    return rounded(a[0]+b[0], a[1]+b[1])


def neg(a):
    return (-a[1], -a[0])


def mul(a, b):
    xs = [x*y for x in a for y in b]
    return rounded(min(xs), max(xs))


def inv(a):
    need(a[0] > 0, 'positive interval inverse required')
    return rounded(1/a[1], 1/a[0])


def point(x):
    return (F(x), F(x))


def sqrt_interval(x):
    need(x >= 0, 'negative square root')
    n = isqrt((x*DEN**2).__floor__())
    lo, hi = F(n,DEN), F(n+1,DEN)
    need(lo*lo <= x <= hi*hi, 'square root enclosure')
    return lo, hi


def exp_neg_point(x):
    need(x >= 0, 'nonnegative exponential argument')
    k = 0
    while x > 1:
        x /= 2
        k += 1
    # On [0,1], alternating Taylor terms decrease. Odd/even sums enclose exp(-x).
    lo = sum(((-x)**n/F(factorial(n)) for n in range(42)), F(0))
    hi = lo + x**42/F(factorial(42))
    a = rounded(lo, hi)
    for _ in range(k):
        a = mul(a,a)
    return a


def exp_neg(a):
    return exp_neg_point(a[1])[0], exp_neg_point(a[0])[1]


def spectral(lam, s):
    a, b, c = 20*lam, F(5,2)*lam, 3+20*s*lam
    r = sqrt_interval((c-a)**2+4*b*b)
    energy = mul(point(F(1,2)), add(point(a+c), neg(r)))
    weight = mul(point(F(1,2)), add(point(1), mul(point(c-a), inv(r))))
    return energy, weight, r


def heat(weight, gap, time):
    return add(weight, mul(add(point(1),neg(weight)), exp_neg(mul(gap,point(time)))))


def encode(a):
    return [str(x) for x in a]


def main():
    cap=F(1,100); d=3-40*cap; g=3-F(85,2)*cap
    coefficient=400/(d*g)+250*cap/(d*d*g)
    need((d,g)==(F(13,5),F(103,40)), 'endpoint gaps')
    need(coefficient==F(1042500,17407) and coefficient<60, 'uniform coefficient')
    need(250/d**2==F(6250,169), 'energy constant')
    need(100/(d*g)==F(20000,1339), 'projector constant')
    need(3-F(97,4)*cap>0, 'inherited positivity range')
    rows=[]
    for lam in (F(0),F(1,10000),F(1,1000),cap):
        if lam==0:
            # The two matrices are exactly identical; do not label interval rounding as error.
            need(spectral(lam,0)==spectral(lam,1),'zero-coupling identity')
            rows.append({'lambda':'0','exact_error':'0'})
            continue
        e0,w0,r0=spectral(lam,0); e1,w1,r1=spectral(lam,1)
        de=add(e1,neg(e0)); dw=add(w1,neg(w0))
        need(de[0]>0 and de[1]<F(6250,169)*lam**3,'different ground energies enclosed')
        need(dw[0]>0,'different selected ground weights enclosed')
        need(r0[0]>=g and r1[0]>=g,'fixture excitation separation')
        times=[]
        for time in (F(0),F(1,16),F(1),F(4),F(16)):
            difference=add(heat(w1,r1,time),neg(heat(w0,r0,time)))
            need(max(abs(x) for x in difference)<60*lam**2,'centered fixture bound')
            times.append({'sigma':str(time),'error_interval':encode(difference)})
        need(max(abs(x) for x in dw)<60*lam**2,'infinite-time fixture bound')
        rows.append({'lambda':str(lam),'energy_difference_interval':encode(de),
                     'ground_weight_difference_interval':encode(dw),'times':times})
    # Common shifts preserve the full centered matrix, partial shifts do not.
    a,b,c,z=F(1,5),F(1,40),F(3),F(7,11)
    need(((c+z)-(a+z))**2+4*b*b==(c-a)**2+4*b*b,'common shift gap identity')
    need((c-(a+z))**2+4*b*b!=(c-a)**2+4*b*b,'partial shift rejected')
    alpha,hbar,t=F(3,2),F(5,4),F(7,8)
    need(alpha*t/hbar==(3*alpha)*(t/3)/hbar,'clock unit invariance')
    need(alpha*t/hbar!=(3*alpha)*t/hbar,'uncompensated clock change')
    invalid=[]
    def validate(lam,alpha,hbar,estar):
        need(0<=lam<=cap and min(alpha,hbar,estar)>0,'out-of-contract scales')
    for label,args in [('negative_lambda',(-cap,1,1,1)),('large_lambda',(F(1,99),1,1,1)),
                       ('zero_alpha',(cap,0,1,1)),('zero_hbar',(cap,1,0,1)),('zero_reference',(cap,1,1,0))]:
        try: validate(*args)
        except ValueError: invalid.append(label)
        else: raise ValueError('invalid input admitted')
    emit('forward', {'uniform_centered_coefficient':'60','sharper_coefficient':str(coefficient),
        'excitation_gap_over_alpha':str(g),'energy_shift_coefficient':'6250/169',
        'projector_shift_coefficient':'20000/1339','coupling_cap':'1/100',
        'all_time_argument':'written spectral and Duhamel proof; fixtures are algebra only',
        'relative_error_proved':False,'continuum_proved':False,'fixtures':rows},
        {'different_grounds_enclosed':True,'different_ground_weights_enclosed':True,
         'lambda_zero_exact':True,'time_zero_identity':True,'infinity_projection_checked':True,
         'partial_shift_rejected':True,'common_shift_preserved':True,'clock_mismatch_rejected':True,
         'invalid_inputs_rejected':invalid,'physical_spin_truncation_claimed':False})


if __name__=='__main__': main()
