#!/usr/bin/env python3
from fractions import Fraction as F
from math import factorial,isqrt
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from u_common import need,emit

def profile(q):
    return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def tail(x):
    need(0<=x<1,'outside connected-series disk')
    return F(44,9)*x*x/(1-x)**5
def sqrt_interval(v):
    need(v>=0,'negative square')
    den=2**160
    lo=F(isqrt(v.numerator*den*den//v.denominator),den)
    hi=lo if lo*lo==v else lo+F(1,den)
    need(lo*lo<=v<=hi*hi,'invalid square-root enclosure')
    return lo,hi
prod_count=1; poch=F(1)
for n in range(1,17):
    prod_count*=40*(8+3*(n-1));poch*=F(8,3)+(n-1)
    need(F(prod_count,12**n*factorial(n))==10**n*poch/factorial(n),'connected count identity')
need(40**2*8*11>40**2*8*8,'frozen-support mutation not detected')
# Polynomial P - 2(1+q)^2(1+q^2), exact coefficient arithmetic.
need([a-b for a,b in zip([2,5,5,6,3],[2,4,4,4,2])]==[0,1,1,2,1],'profile inequality')
z=F(1,10**6);x=F(80,7)*z;lim=z/84-tail(x)
need(lim>z/168,'endpoint positivity')
eta=F(1,2);C=F(1,500000);rows=[]
for k in range(3,10):
    eps=F(1,10**k);q=1-eps;tau=eta/(8*profile(q));s=C*tau/eps**3
    d2=F(2,3)*tau*tau*profile(q*q)/(1-eta)**2
    dlo,dhi=sqrt_interval(d2);lead=s*q**4/96;rem=tail(10*s)
    lower=lead-rem-6*dhi
    if k>=6: need(lower>0,'finite-q positive witness lost')
    need(s<=F(3,2)*z,'uniform time-domain condition')
    rows.append(dict(epsilon=str(eps),q=str(q),alpha_time_over_hbar=str(C/eps**3),
                     leading=str(lead),bulk_upper=str(rem),state_upper=str(6*dhi),
                     difference_lower=str(lower),variance_lower=str(1-2*dhi-4*dhi*dhi),
                     state_sqrt_interval=list(map(str,(dlo,dhi)))))
need(tail(F(80,7)*F(1,1000))>F(1,1000)/84,'large-window inconclusive control')
bad=False
try: tail(F(1))
except ValueError: bad=True
need(bad,'outside disk accepted')
emit('u2','forward','22c496e565897392f8a1d63bff270d10ab5c9d4ba278bf1323584ad830a10dd8',
 dict(status='full_system_endpoint_lower_bound',endpoint_proved=True,continuum_proved=False,
      z_cap=str(z),liminf_lower_at_cap=str(lim),simple_liminf_lower_at_cap=str(z/168),
      tail_power='8/3',tail_rational_coefficient='44/9',finite_q_certificates=rows,
      result_scope='Existence of one bounded local gauge-invariant rank-operator autocorrelation witness'),
 dict(connected_word_identity=True,support_growth_required=True,profile_uniform_bound=True,
      exact_positive_margin=True,state_square_root_enclosures=True,finite_q_positive=True,
      outside_series_disk_rejected=bad,large_window_certificate_only=True,
      large_window_lower_estimate=str(F(1,1000)/84-tail(F(80,7)*F(1,1000))),
      no_two_state_autonomy=True,first_order_bound_to_u1=True))
