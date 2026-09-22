#!/usr/bin/env python3
"""Independent exact AT4 reverse certificate; no floating arithmetic in admission."""
from pathlib import Path
from fractions import Fraction as Q
from math import isqrt
import argparse
import hashlib
import json

BASE = Path(__file__).resolve().parent
DEN = 10**36
CONTRACT_SHA = 'ff7d1652f05e2c4201d85237f67780d9eb2456688c39d8398d72fe9a10d1940f'


def require(condition, message):
    if condition is not True:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def down(x):
    return Q(x.numerator * DEN // x.denominator, DEN)


def up(x):
    return Q(-((-x.numerator * DEN) // x.denominator), DEN)


def exp_minus(x):
    """Alternating polynomial brackets after halving, then outward squares."""
    require(type(x) is Q and x >= 0, 'exponential requires nonnegative Fraction')
    if x == 0:
        return Q(1), Q(1)
    y, steps = x, 0
    while y > Q(1, 2):
        y /= 2
        steps += 1
    term, even = Q(1), Q(1)
    for k in range(1, 41):
        term *= -y / k
        even += term
    odd = even + term * (-y) / 41
    lo, hi = down(odd), up(even)
    require(Q(0) <= lo <= hi <= Q(1), 'bad exponential bracket')
    for _ in range(steps):
        lo, hi = down(lo * lo), up(hi * hi)
    return lo, hi


def atan_small(x, n=64):
    require(type(x) is Q and 0 <= x < 1, 'arctangent argument invalid')
    # n is an even number of retained terms: partial sum is lower bound.
    require(type(n) is int and n > 0 and n % 2 == 0, 'arctangent term parity')
    total = sum(((-1)**k * x**(2*k+1) / (2*k+1) for k in range(n)), Q(0))
    return total, total + x**(2*n+1)/(2*n+1)


def log_unit(y, n=64):
    require(type(y) is Q and 1 <= y <= 2, 'log_unit range')
    z = (y-1)/(y+1)
    total = 2*sum((z**(2*k+1)/(2*k+1) for k in range(n)), Q(0))
    tail = 2*z**(2*n+1)/((2*n+1)*(1-z*z))
    return total, total + tail


def log_positive(x):
    require(type(x) is Q and x >= 1, 'log argument must be >=1')
    k, y = 0, x
    while y > 2:
        y /= 2
        k += 1
    ll, lu = log_unit(y)
    tl, tu = log_unit(Q(2))
    return down(ll+k*tl), up(lu+k*tu)


def square_root(x):
    require(type(x) is Q and x >= 0, 'sqrt argument')
    floor = isqrt(x.numerator * DEN * DEN // x.denominator)
    lo, hi = Q(floor, DEN), Q(floor+1, DEN)
    require(lo*lo <= x <= hi*hi, 'sqrt bracket failure')
    return lo, hi


def serial(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {k: serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def save(path, value):
    path.write_text(json.dumps(serial(value), sort_keys=True, indent=2)+'\n')


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def main(output):
    require(output.is_absolute() and not output.exists(), 'output must be absolute and fresh')
    contract_path = BASE/'inputs/research/round31/contracts/at4.json'
    require(digest(contract_path) == CONTRACT_SHA, 'frozen contract hash mismatch')
    contract = json.loads(contract_path.read_text())
    require(contract['id'] == 'AT4' and contract['status'] == 'frozen_before_production', 'contract identity')
    require((BASE/'inputs/AGENTS.md').is_file(), 'missing immutable instructions')
    tau, cap, target = Q(1, 100000000), Q(10000), Q(1, 1000000)
    checks = []

    def check(name, condition, **data):
        require(condition, 'failed control: '+name)
        checks.append({'id': name, 'passed': True, **data})

    zero = (0, 0, 0)
    axes = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]
    region = {zero, axes[2]}
    star = {zero, *axes}
    anchors = {sub(r, s) for r in region for s in star}
    positive_anchors = {b for b in anchors if all(x >= 0 for x in b)}
    links = {(add((4*b[0], 2*b[1], b[2]), (r, t, 0)), j)
             for b in region for r in range(4) for t in range(2) for j in range(3)}
    endpoints = {v for tail, j in links for v in (tail, add(tail, axes[j]))}
    wilson_links = [(zero, 0), (axes[0], 2), (axes[2], 0), (zero, 2)]
    owners = {(tail[0]//4, tail[1]//2, tail[2]) for tail, _ in wilson_links}
    check('complete_original_wilson_cover', len(links) == 48 and len(endpoints) == 36 and owners == region,
          link_count=len(links), endpoint_count=len(endpoints), incident_anchors=sorted(anchors))
    check('missing_incoming_stars', len(anchors) == 7 and len(positive_anchors) == 2,
          omitted_by_wrong_orthant=len(anchors-positive_anchors))
    check('zero_selected_corner_allowed', all(lo <= 0 <= hi for lo, hi in
          [(-Q(1,2), Q(1,2)), (-Q(1,8), Q(1,8)), (-Q(1,2), Q(1,2))]))
    # At the zero selected triple, h_b=8 sum C_e and its first nonzero energy is 6.
    reset_h = 2*len(anchors)*7*tau
    gap_h = 8*Q(3,4)
    leakage = reset_h/gap_h
    sqrt_low, sqrt_high = square_root(leakage)
    state_cost = 2*sqrt_high
    center_cost = 4*leakage
    v_norm = len(anchors)*Q(7,8)*tau
    slope = 2*v_norm
    check('zero_corner_energy_and_reset', gap_h == 6 and reset_h == 98*tau and leakage == Q(49,3)*tau)
    check('wrong_delta_alpha_hbar_normalization', slope == Q(49,4)*tau and 8*slope != slope,
          physical_interaction_per_star_in_alpha_units=Q(7,8)*tau)
    alpha, hbar, physical_time = Q(4), Q(3), Q(3,4)
    check('free_wilson_physical_clock', 4*Q(3,4) == 3 and alpha*physical_time/hbar == 1
          and (alpha/8)*physical_time/hbar == Q(1,8), correct_free_exponent=3, wrong_exponent=Q(3,8))
    # Nonzero selected plaquette: f=1+tW gives negative energy for t=lambda/(3 alpha).
    lam, alpha_test = Q(1,2), Q(1)
    t = lam/(3*alpha_test)
    energy_numerator = Q(3,4)*alpha_test*t*t-lam*t/2
    check('selected_reference_not_haar_outside_corner', energy_numerator < 0,
          trial_energy_numerator=energy_numerator)
    # Directed Machin formula and exact positive log-tail series.
    a5l, a5u = atan_small(Q(1,5))
    a239l, a239u = atan_small(Q(1,239))
    pi_low, pi_high = down(16*a5l-4*a239u), up(16*a5u-4*a239l)
    check('directed_pi_enclosure', 3 < pi_low < pi_high < Q(22,7))
    log_low, log_high = log_positive(1+cap*cap)
    atl, atu = atan_small(1/cap, n=8)
    dynamic_inside = up(slope*log_high/pi_low)
    dynamic_tail = up(4*atu/pi_low)
    radius = state_cost + center_cost + dynamic_inside + dynamic_tail
    e3lo, e3hi = exp_minus(Q(3))
    center_lo, center_hi = e3lo/4, e3hi/4
    interval = (max(Q(0), center_lo-radius), center_hi+radius)
    midpoint = sum(interval, Q(0))/2
    half_width = (interval[1]-interval[0])/2
    check('actual_aq_certificate_positive_interval', interval[0] > 0 and interval[0] < interval[1] < 1)
    check('frozen_target_insufficient', half_width > target,
          conclusion='certificate insufficient; not an actual error lower bound')
    check('state_bound_alone_exceeds_target', 2*sqrt_low > target)
    check('omitted_poisson_tail', dynamic_tail > target and atl > 0,
          kernel_tail_lower=2*atl/pi_high, charged_difference_tail_upper=dynamic_tail)
    # A bounded integrand which is one outside [-L,L] and zero inside has exactly
    # the positive kernel tail. Omitting it would assert zero for a positive integral.
    check('poisson_tail_counterexample', 2*atl/pi_high > 0,
          bounded_integrand='indicator(|v|>L)', incorrectly_omitted_value=0)
    # The local incidence is volume-independent, in contrast to all stars.
    totals = {str(n): (2*n)**3 for n in (2, 3, 4)}
    check('extensive_norm_not_local_budget', all(v > 7 for v in totals.values())
          and len(set(totals.values())) == 3, whole_box_star_counts=totals, local_star_count=7)
    # Centering controls with exactly representable scalar means.
    m, mhat = Q(1,10), Q(3,20)
    vector_residue = (m-mhat)**2
    scalar_residue = m*m-mhat*mhat
    check('vector_scalar_centering_distinction', vector_residue == Q(1,400)
          and scalar_residue == -Q(1,80) and vector_residue != scalar_residue)
    check('uncentered_vacuum_residue', m*m == Q(1,100) and m*m > target,
          zero_energy_atom=m*m)
    # Four terms of (1-r)^4 prove unequal nonzero-time Laplace data exactly.
    a = [(Q(2), Q(1,8)), (Q(4), Q(1,8))]
    b = [(Q(1), Q(1,32)), (Q(3), Q(3,16)), (Q(5), Q(1,32))]
    moments_a = [sum((w*x**k for x,w in a), Q(0)) for k in range(3)]
    moments_b = [sum((w*x**k for x,w in b), Q(0)) for k in range(3)]
    check('equal_first_three_moments', moments_a == moments_b == [Q(1,4), Q(3,4), Q(5,2)])
    coeff_diff = {i: Q(0) for i in range(6)}
    for x,w in b:
        coeff_diff[int(x)] += w
    for x,w in a:
        coeff_diff[int(x)] -= w
    check('laplace_separation_polynomial_identity', [32*coeff_diff[i] for i in range(6)] == [0,1,-4,6,-4,1])
    rlo, rhi = exp_minus(Q(1))
    separation_lo = rlo*(1-rhi)**4/32
    separation_hi = rhi*(1-rlo)**4/32
    minimax_lo = separation_lo/2
    check('moment_only_point_estimator_obstruction', minimax_lo > target,
          minimax_error_lower=minimax_lo, scope='abstract moment-information class, not AQ realizability')
    # Any finite prefix can agree while its later limit differs: no uniform rate follows.
    observed_n = 1000
    finite_prefix = [Q(0) for _ in range(observed_n)]
    check('finite_samples_no_thermodynamic_rate', all(x == 0 for x in finite_prefix),
          sequence_one_limit='0', sequence_two_limit='1',
          sequence_two='0 for N<=1000; 1 for N>1000',
          scope='abstract counterexample to inference from finite values')
    check('directed_exponential_free_limit', exp_minus(Q(0)) == (Q(1),Q(1))
          and Q(0) < e3lo < e3hi < 1 and e3hi-e3lo < Q(1,10**32))
    require(all(type(c['passed']) is bool and c['passed'] is True for c in checks), 'bad check semantics')
    results = {
        'loop': 'AT4', 'direction': 'reverse', 'human_author': 'Hruday N M (BUNZEEY)',
        'contract_sha256': CONTRACT_SHA, 'actual_aq_enclosure': True,
        'actual_aq_value_computed_to_target': False, 'target_met': False,
        'uniform_wilson_claim': False, 'continuum_claim': False,
        'aq_state_uniqueness_claim': False, 'scientific_priority_verified': False,
        'model': 'AQ zero selected triple, tau=10^-8, actual chosen centered-box subsequential state',
        'method': 'local reset; strong bounded-perturbation Duhamel; nonnegative GNS Poisson integral',
        's': 1, 'tau': tau, 'real_time_cutoff': cap, 'absolute_target': target,
        'constants': {'reset_h_energy': reset_h, 'free_onsite_gap_h_units': gap_h,
                      'local_reference_leakage_upper': leakage,
                      'duhamel_slope_alpha_time': slope,
                      'pi_interval': [pi_low,pi_high], 'log_one_plus_L_squared_interval': [log_low,log_high]},
        'error_budget': {'state_trace_norm_upper': state_cost, 'centering_mean_square_upper': center_cost,
                         'duhamel_inside_upper': dynamic_inside, 'poisson_tail_upper': dynamic_tail,
                         'radius_upper': radius},
        'free_reference_correlation_interval': [center_lo,center_hi],
        'actual_centered_correlation_interval': interval,
        'midpoint_estimator': midpoint, 'absolute_point_error_upper': half_width,
        'moment_information': {'moments': moments_a, 'C_B_minus_C_A_formula': 'r(1-r)^4/32, r=exp(-1)',
                               'separation_interval': [separation_lo,separation_hi],
                               'deterministic_minimax_error_lower': minimax_lo,
                               'actual_AQ_realization_claim': False},
        'checks': checks,
    }
    output.mkdir(parents=True)
    save(output/'results.json', results)
    sources = {str(p.relative_to(BASE)): digest(p) for p in sorted((BASE/'inputs').rglob('*')) if p.is_file()}
    sources.update({p: digest(BASE/p) for p in ('check.py','report.md')})
    save(output/'source-manifest.json', {'schema':'at4-reverse-manifest-v1','sources':sources,
                                       'outputs':{'results.json':digest(output/'results.json')}})
    print('AT4 reverse: actual interval certified; frozen absolute target insufficient; '+str(len(checks))+' checks passed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    main(args.output)
