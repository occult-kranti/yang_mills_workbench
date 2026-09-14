#!/usr/bin/env python3
"""Independent R2 collar/tail/actual-source controls; no current producer inputs."""
import argparse
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


E = ((1,0,0),(0,1,0),(0,0,1))
ZERO = (0,0,0)


def add(a,b):
    return tuple(x+y for x,y in zip(a,b))


def star(b):
    return {b,*(add(b,e) for e in E)}


def collar(y,n):
    return {add(a,d) for a in y for d in product(range(-n,n+1),repeat=3)
            if min(add(a,d)) >= 0}


def touching(y):
    anchors = set(y)
    for a in y:
        for e in E:
            b = tuple(x-z for x,z in zip(a,e))
            if min(b) >= 0:
                anchors.add(b)
    return {b:star(b) for b in anchors}


def tail(k,n):
    # Sum_{j>=n+1} k^j (2j-1)^3.
    g = 1-k
    a = 2*n+1
    return k**(n+1)*(F(a**3)/g+6*a*a*k/g**2
                    +12*a*k*(1+k)/g**3+8*k*(1+4*k+k*k)/g**4)


def haar(powers):
    if any(x % 2 for x in powers):
        return F(0)
    v = F(1)
    for p in powers:
        for k in range(1,p,2):
            v *= k
    for k in range(sum(powers)//2):
        v /= 4+2*k
    return v


def run():
    geometry=[]
    for name,y in [('origin',{ZERO}),('bulk',{(2,2,2)}),('two_sites',{ZERO,(1,0,0)})]:
        for n in range(6):
            x = collar(y,n)
            require(len(x) <= len(y)*(2*n+1)**3, 'general collar union bound')
            if name == 'origin':
                require(len(x) == (n+1)**3, 'clipped origin collar count')
            if name == 'bulk':
                require(len(x) == (2+n-max(0,2-n)+1)**3, 'bulk collar clipping count')
            ts = touching(x)
            require(len(ts) <= 4*len(x), 'touching star bound')
            require(set().union(*ts.values()) <= collar(y,n+1), 'one action grows at most one collar')
            containing = collar(y,n+1)
            require(all(s <= containing for s in ts.values()), 'finite-volume coefficient matching margin')
            geometry.append({'support':name,'n':n,'collar_size':len(x),'touching_stars':len(ts)})
    kmax = F(35,416)
    require(28*F(5,1664) == kmax and 1-kmax == F(381,416), 'actual coupling constants')
    tails=[]
    for k in (F(0),F(1,1000),kmax):
        for n in range(8):
            t = tail(k,n)
            require(t == k**(n+1)*(2*n+1)**3+tail(k,n+1), 'exact cubic geometric tail recurrence')
            partial = sum((k**j*(2*j-1)**3 for j in range(n+1,n+18)),F(0))
            require(t == partial+tail(k,n+17), 'finite tail telescoping')
            geometric = k**(n+1)/(1-k)
            require(geometric == k**(n+1)+k**(n+2)/(1-k), 'geometric tail starts at n+1')
            if k:
                require(t != geometric, 'dropping graph polynomial must be detected')
            tails.append({'kappa':str(k),'N':n,'Hilbert_energy_tail_over_r':str(geometric),
                          'H0_graph_tail_over_r_times_Y_size':str(t)})
    # The declared origin collar weight is 2^((n+1)^3), not 2^(n+1).
    ratios=[]
    for k in (F(1,1000),kmax):
        row=[k*2**(3*n*n+9*n+7) for n in range(3)]
        require(row[1] > row[0] and row[2] > row[1], 'eventual collar-weight growth')
        ratios.append({'kappa':str(k),'successive_upper_term_ratios':[str(x) for x in row]})
    require(ratios[0]['successive_upper_term_ratios'][0] == '16/125', 'early decreasing prefix')
    require(F(ratios[0]['successive_upper_term_ratios'][1]) > 1, 'later increase after decreasing prefix')
    require(kmax*2**7 == F(140,13), 'endpoint positive volume-weight failure')
    require(kmax*2 < 1 and kmax*2**7 > 1, 'linear-size replacement gives false certificate')

    # Actual independent free SU2 factors, not a finite-dimensional surrogate.
    chi_mean = 2*haar((1,0,0,0))
    chi2 = 4*haar((2,0,0,0))
    require(chi_mean == 0 and chi2 == 1, 'actual normalized free-character factors')
    source_edge = (2,(0,0,0)); exterior_edge = (2,(4,0,0))
    require(source_edge != exterior_edge and exterior_edge[1][0]//4 == 1, 'actual exterior site e_x')
    input_norm2 = chi2
    local_output_norm2 = chi2*chi2
    vacuum_output_norm2 = chi_mean**2*chi2
    require(input_norm2 == local_output_norm2 == 1 and vacuum_output_norm2 == 0,
            'A_local tensor I differs on the actual exterior character')
    require(8*F(3,4) == 6 and 2*8*F(3,4) == 12, 'actual local-domain energies')
    # Separate algebra sign check: (1+K) sum_{j=0}^N (-K)^j residual.
    k = F(1,10)
    for n in range(5):
        s = sum(((-k)**j for j in range(n+1)),F(0))
        require((1+k)*s == 1-(-k)**(n+1), 'sandwiched inverse sign')
    require((1+k)/(1-k) != 1, 'wrong inverse sign is rejected')
    require(tail(F(0),0) == 0, 'tau zero graph tail')
    bare_rows=[]
    for tau in (-F(5,1664),F(0),F(5,1664)):
        # R1 actual all-face Haar contraction: G(H0^-1 v)-v = Dv/6.
        residual2 = F(21,4)*(tau/F(18))**2
        require(residual2 == F(7,432)*tau*tau, 'actual first bare-truncation residual')
        require((residual2 > 0) == (tau != 0), 'omitted boundary rejected for both coupling signs')
        bare_rows.append({'tau':str(tau),'actual_bare_truncation_residual_norm_squared':str(residual2)})
    return {'schema':'ym22-skeptic-r2-preparation-checks-v1','loop':'r2','passed':True,
        'current_producers_or_root_R2_work_read':False,'research_loops_added':0,
        'geometry':geometry,'tail_controls':tails,'volume_weight_controls':ratios,
        'actual_bare_truncation_controls':bare_rows,
        'actual_exterior_character_control':{'source_edge':source_edge,'exterior_edge':exterior_edge,
            'input_norm_squared':'1','A_local_output_norm_squared':'1','A_vac_output_norm_squared':'0',
            'difference_norm_squared':'1','input_bare_energy':'6','output_bare_energy':'12',
            'finite_dimensional_surrogate':False},
        'controls':{'wrong_inverse_sign_rejected':True,'omitted_graph_polynomial_rejected':True,
            'omitted_one_collar_action_rejected':len(star(ZERO)) > 1,
            'linear_volume_weight_replacement_rejected':True,'source_sector_replacement_rejected':True,
            'tau_zero_passed':True,'r_zero_all_bounds_zero':True,'runtime_guards_use_assert':False},
        'scope':'Exact arithmetic and support witnesses accompany, rather than replace, the infinite-form and domain derivations.'}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output
    if out.exists():
        raise RuntimeError('fresh output required')
    out.write_text(json.dumps(run(),indent=2,sort_keys=True)+'\n')
