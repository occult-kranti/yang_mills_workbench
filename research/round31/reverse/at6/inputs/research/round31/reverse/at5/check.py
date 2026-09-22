#!/usr/bin/env python3
"""Independent exact AT5 reverse calculator; no floating arithmetic in admission."""
from pathlib import Path
from fractions import Fraction as Q
from math import isqrt
import argparse
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
DEN = 10**36
CONTRACT_SHA = 'b936651d4520436e559e1e6bd071376c609bed868214751bf55a833a0ab6fba1'


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


FROZEN = {'tau': '1/100000000000000', 's': '1', 'L': '1000000000',
          'alpha': '1', 'hbar': '1', 'E_star': '1', 'a': '1',
          'selected': ['0', '0', '0']}
TARGET = Q(1, 1000000)


def number(value):
    """Only exact rational forms are admitted; bool and binary float are not."""
    if type(value) is Q:
        return value
    if type(value) is int:
        return Q(value)
    if type(value) is str and len(value) <= 4096:
        fraction = re.fullmatch(r'[+-]?[0-9]+/[0-9]+', value)
        decimal = re.fullmatch(r'[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?', value)
        if fraction or decimal:
            try:
                return Q(value)
            except (ValueError, ZeroDivisionError, OverflowError) as error:
                raise ValueError('invalid exact number') from error
    raise ValueError('number must be an integer, Fraction, or exact rational/decimal string')


def certify(parameters, *, fixed_design=False):
    """Return a containing interval for the stated actual AQ zero-selected scalar.

    Scales are caller declarations; units must match alpha/hbar/a/E_star meanings.
    The mathematical theorem applies at all positive rational s,L and stated scales.
    """
    if type(parameters) is not dict or set(parameters) != set(FROZEN):
        raise ValueError('calculator fields must exactly match the documented schema')
    if type(fixed_design) is not bool:
        raise ValueError('fixed_design must be a bool')
    selected = parameters['selected']
    if type(selected) not in (tuple, list) or len(selected) != 3:
        raise ValueError('selected must have exactly three coefficients')
    selected = tuple(number(v) for v in selected)
    if selected != (Q(0),Q(0),Q(0)):
        raise ValueError('only the zero selected triple has this reference comparison')
    p = {k:number(v) for k,v in parameters.items() if k != 'selected'}
    if any(p[k] <= 0 for k in ('s','L','alpha','hbar','E_star','a')):
        raise ValueError('positive time, cutoff and physical scales are required')
    if abs(p['tau']) > Q(1,100000000):
        raise ValueError('tau is outside the inherited numerical cap')
    if fixed_design and any(p[k] != number(FROZEN[k]) for k in ('tau','s','L')):
        raise ValueError('fixed-design mode cannot retune tau, s or L')
    tau, s, cutoff = abs(p['tau']), p['s'], p['L']
    a5l, a5u = atan_small(Q(1,5))
    a239l, a239u = atan_small(Q(1,239))
    pi_low = down(16*a5l-4*a239u)
    pi_high = up(16*a5u-4*a239l)
    leakage = Q(49,3)*tau
    _, root_upper = square_root(leakage)
    state = 2*root_upper if tau else Q(0)
    centering = 4*leakage
    slope = Q(49,4)*tau
    log_low, log_high = log_positive(1+(cutoff/s)**2)
    dynamic = up(slope*s*log_high/pi_low) if tau else Q(0)
    # atan(s/L)<=s/L; no restriction L>=s is necessary for this conservative bound.
    tail = up(4*s/(pi_low*cutoff)) if tau else Q(0)
    modeling_radius = state+centering+dynamic+tail
    free_low, free_high = exp_minus(3*s)
    free_low, free_high = free_low/4, free_high/4
    raw_interval = (free_low-modeling_radius,free_high+modeling_radius)
    # C(s)>=0 and C(s)<=||W||²<=1 are valid for the actual centered heat vector.
    lower, upper = max(Q(0),raw_interval[0]), min(Q(1),raw_interval[1])
    require(lower <= upper, 'empty correlation interval')
    datum = (lower+upper)/2
    radius = (upper-lower)/2
    arithmetic = (free_high-free_low)/2
    included = lower <= free_low <= free_high <= upper
    return {'model':'zero-selected full-Z3 patterned AQ subsequential state',
            'parameters':{**p,'selected':selected},
            'physical_euclidean_time':s*p['hbar']/p['alpha'],
            'normalized_AQ_time':s/8,
            'comparison_energy_ratio':p['alpha']/p['E_star'],
            'free_reference_interval':[free_low,free_high],
            'actual_centered_correlation_interval':[lower,upper],
            'exported_datum':datum, 'certified_absolute_error':radius,
            'absolute_target':TARGET, 'target_met':radius <= TARGET,
            'free_reference_included':included,
            'interaction_shift_resolved':False,
            'zero_coupling_exact_reference':tau == 0,
            'error_budget':{'state_trace_norm_upper':state,'centering_mean_square_upper':centering,
                            'duhamel_inside_upper':dynamic,'poisson_tail_upper':tail,
                            'modeling_radius_upper':modeling_radius,
                            'reference_arithmetic_half_width':arithmetic,
                            'unclipped_total_radius_upper':modeling_radius+arithmetic},
            'constants':{'reference_infidelity_upper':leakage,'duhamel_slope_alpha_time':slope,
                         'pi_interval':[pi_low,pi_high],
                         'log_one_plus_L_squared_over_s_squared_interval':[log_low,log_high]},
            'actual_aq_enclosure':True,'uniform_wilson_claim':False,'continuum_claim':False,
            'state_uniqueness_claim':False,'inverse_response_computed':False}


def main(output, parameters_file=None):
    require(output.is_absolute() and not output.exists(), 'output must be absolute and fresh')
    contract_path=BASE/'inputs/research/round31/contracts/at5.json'
    require(digest(contract_path) == CONTRACT_SHA, 'frozen AT5 contract changed')
    require((BASE/'inputs/AGENTS.md').is_file(), 'missing instructions')
    selected_parameters=FROZEN
    external_hash=None
    if parameters_file is not None:
        selected_parameters=json.loads(parameters_file.read_text())
        external_hash=digest(parameters_file)
    result=certify(selected_parameters, fixed_design=parameters_file is None)
    fixed=certify(FROZEN,fixed_design=True)
    checks=[]

    def check(name, condition, **detail):
        require(condition, 'AT5 check failed: '+name)
        checks.append({'id':name,'passed':True,**detail})

    check('fixed_design_actual_nonzero_sample', fixed['target_met'] is True
          and fixed['parameters']['tau'] == Q(1,10**14) and fixed['parameters']['s'] == 1)
    check('complete_exported_radius', fixed['certified_absolute_error'] ==
          fixed['error_budget']['unclipped_total_radius_upper'])
    check('free_reference_inclusion_no_shift', fixed['free_reference_included'] is True
          and fixed['interaction_shift_resolved'] is False)
    short=certify({**FROZEN,'L':'10000'})
    cap=certify({**FROZEN,'tau':'1/100000000'})
    check('old_cutoff_remains_insufficient', short['target_met'] is False
          and short['error_budget']['poisson_tail_upper'] > TARGET)
    check('coupling_cap_still_insufficient', cap['target_met'] is False
          and cap['error_budget']['state_trace_norm_upper'] > TARGET)
    negative=certify({**FROZEN,'tau':'-1/100000000000000'})
    check('negative_coupling_same_absolute_certificate', negative['actual_centered_correlation_interval'] ==
          fixed['actual_centered_correlation_interval'] and negative['parameters']['tau'] < 0)
    zero=certify({**FROZEN,'tau':0})
    check('zero_coupling_exact_free_limit', zero['zero_coupling_exact_reference'] is True
          and zero['error_budget']['modeling_radius_upper'] == 0
          and zero['actual_centered_correlation_interval'] == zero['free_reference_interval'])
    clocks=certify({**FROZEN,'alpha':'4','hbar':'3','E_star':'2','a':'1/2'})
    check('wrong_eightfold_clock', clocks['physical_euclidean_time'] == Q(3,4)
          and clocks['normalized_AQ_time'] == Q(1,8)
          and clocks['actual_centered_correlation_interval'] == fixed['actual_centered_correlation_interval'])
    check('uncentered_mean_square_cost_retained', fixed['error_budget']['centering_mean_square_upper'] == Q(49,75000000000000)
          and fixed['error_budget']['centering_mean_square_upper'] > 0)
    # An interval of width 1.5epsilon has a valid midpoint error, but exceeds epsilon as a width.
    artificial_width=Q(3,2)*TARGET
    check('radius_vs_width_tolerance', artificial_width > TARGET and artificial_width/2 <= TARGET)
    # Every valid s/L is mathematical domain; L<s produces a broad honest result.
    wide=certify({**FROZEN,'s':'2','L':'1/10'})
    check('positive_domain_broad_result_honest', wide['target_met'] is False
          and wide['actual_centered_correlation_interval'] == [Q(0),Q(1)])
    malformed=[
        ('nonzero_selected',{**FROZEN,'selected':['0','1/1000','0']}),
        ('selected_length',{**FROZEN,'selected':['0','0']}),
        ('negative_alpha',{**FROZEN,'alpha':'-1'}),
        ('zero_hbar',{**FROZEN,'hbar':0}),
        ('zero_E_star',{**FROZEN,'E_star':0}),
        ('negative_spacing',{**FROZEN,'a':'-1'}),
        ('zero_s',{**FROZEN,'s':0}),
        ('negative_L',{**FROZEN,'L':'-1'}),
        ('positive_cap_exceeded',{**FROZEN,'tau':'1/10000000'}),
        ('negative_cap_exceeded',{**FROZEN,'tau':'-1/10000000'}),
        ('float',{**FROZEN,'tau':1e-14}),
        ('boolean',{**FROZEN,'s':True}),
        ('nan',{**FROZEN,'s':'NaN'}),
        ('infinity',{**FROZEN,'s':'Infinity'}),
        ('bad_fraction',{**FROZEN,'tau':'1/0'}),
        ('whitespace',{**FROZEN,'s':' 1'}),
        ('underscore',{**FROZEN,'s':'1_000'}),
        ('extra_field',{**FROZEN,'gap':'1'}),
        ('missing_field',{k:v for k,v in FROZEN.items() if k!='alpha'}),
        ('not_mapping',[]),
    ]
    rejected=[]
    for name,parameters in malformed:
        try:
            certify(parameters)
        except (ValueError,TypeError,ZeroDivisionError):
            rejected.append(name)
        else:
            raise RuntimeError('malformed input accepted: '+name)
    check('malformed_out_of_domain_rejected', len(rejected) == len(malformed), cases=rejected)
    try:
        certify({**FROZEN,'tau':'1/100000000'},fixed_design=True)
    except ValueError:
        fixed_rejected=True
    else:
        fixed_rejected=False
    check('fixed_design_cannot_retune', fixed_rejected)
    check('exact_decimal_parser', number('1e-14') == Q(1,10**14)
          and number('0.00000000000001') == Q(1,10**14))
    result.update({'loop':'AT5','direction':'reverse','contract_sha256':CONTRACT_SHA,
                   'checks':checks,'fixed_design':parameters_file is None,'external_input_sha256':external_hash,
                   'scientific_priority_verified':False,
                   'scope':'One actual-state analytic enclosure; no grid or inverse response computed',
                   'controls':{'old_cutoff':short,'old_coupling_cap':cap,'zero_coupling':zero,
                               'negative_coupling':negative}})
    output.mkdir(parents=True)
    save(output/'results.json',result)
    save(output/'datum.json',{'observable':'actual centered original xz Wilson C_tau(s)',
                              'tau':result['parameters']['tau'],'s':result['parameters']['s'],
                              'value':result['exported_datum'],
                              'absolute_error':result['certified_absolute_error'],
                              'certified_to_1e_minus_6':result['target_met'],
                              'model':result['model'],
                              'selected':[0,0,0],
                              'method':'analytic direct-state comparison',
                              'free_reference_included':result['free_reference_included'],
                              'interaction_shift_resolved':False})
    sources={str(p.relative_to(BASE)):digest(p) for p in sorted((BASE/'inputs').rglob('*')) if p.is_file()}
    sources.update({name:digest(BASE/name) for name in ('check.py','report.md')})
    save(output/'source-manifest.json',{'schema':'at5-reverse-manifest-v1','sources':sources,
                                       'outputs':{name:digest(output/name) for name in ('results.json','datum.json')}})
    print('AT5 reverse: '+str(len(checks))+' checks passed; requested result target_met='+str(result['target_met']))


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--parameters',type=Path)
    args=parser.parse_args()
    main(args.output,args.parameters)
