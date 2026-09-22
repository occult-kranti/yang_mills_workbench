#!/usr/bin/env python3
"""AT6 reverse: complete rational analytic AQ grid and inverse-form enclosure."""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import csv
import hashlib
import importlib.util
import json
import sys

sys.dont_write_bytecode=True
BASE=Path(__file__).resolve().parent
CONTRACT_SHA='7ce892e9fb5bf7a5da03777206129db31f9d757d0d4c227cc6077c51fbe55daf'
ARITH_SHA='665e367d496f3373ae162624bb55276364469cbf5f72e2b1e37cb3173abca490'
EVALUATOR_SHA='261a25623cd454b6ca6ef6ebd5d52c8a5c6512873903b81188c63d7aa8ac16d1'
TAU=Q(1,10**14)
L=Q(10**9)
T=Q(128)
H=Q(1,32)
N=4096
EPS=Q(1,10**6)
GAP=Q(1,16)
MASS=Q(63,250)
FIRST=Q(94,125)
FIELDS=['index','s','reference_lower','reference_upper','datum',
        'reference_arithmetic_error','analytic_comparison_error','actual_correlation_error',
        'actual_lower','actual_upper']


def require(condition,message):
    if condition is not True:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


ARITH=load(BASE/'inputs/research/round31/reverse/at5/check.py','frozen_reverse_at5_arithmetic')
AT3=load(BASE/'inputs/research/round30/forward/at3/evaluator.py','unchanged_at3_evaluator')


def serial(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def write_json(path,value):
    path.write_text(json.dumps(serial(value),sort_keys=True,indent=2)+'\n')


def exact(x):
    return ARITH.number(x)


def uniform_budget():
    endpoint=ARITH.certify({**ARITH.FROZEN,'s':str(T)})
    bound=endpoint['error_budget']['modeling_radius_upper']
    zero=endpoint['error_budget']['state_trace_norm_upper']+endpoint['error_budget']['centering_mean_square_upper']
    # Proof uses derivative positivity: log(1+y²)>2>2y²/(1+y²), y=L/s>=L/T>4.
    require(L/T > 4,'window monotonicity premise fails')
    log17low,_=ARITH.log_positive(Q(17))
    require(log17low > 2,'directed logarithm confirms derivative margin')
    return bound,zero,endpoint


def generate_rows(positive_budget,zero_budget):
    denominator=ARITH.DEN
    ratio_low,ratio_high=ARITH.exp_minus(3*H)
    low_i=high_i=denominator
    q_low=int(ratio_low*denominator)
    q_high=int(ratio_high*denominator)
    require(Q(q_low,denominator)==ratio_low and Q(q_high,denominator)==ratio_high,'recurrence grid lift')
    rows=[]
    for j in range(N+1):
        lo,hi=Q(low_i,4*denominator),Q(high_i,4*denominator)
        datum=(lo+hi)/2
        arithmetic=(hi-lo)/2
        analytic=zero_budget if j==0 else positive_budget
        error=analytic+arithmetic
        require(0 <= lo <= hi <= Q(1,4),'invalid reference bin')
        require(error <= EPS,'node error exceeds inherited contract')
        rows.append({'index':j,'s':j*H,'reference_lower':lo,'reference_upper':hi,
                     'datum':datum,'reference_arithmetic_error':arithmetic,
                     'analytic_comparison_error':analytic,'actual_correlation_error':error,
                     'actual_lower':max(Q(0),datum-error),'actual_upper':min(Q(1),datum+error)})
        if j < N:
            low_i=low_i*q_low//denominator
            high_i=(high_i*q_high+denominator-1)//denominator
    return rows


def save_rows(path,rows):
    with path.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=FIELDS,lineterminator='\n')
        writer.writeheader()
        writer.writerows([{k:str(v) for k,v in row.items()} for row in rows])


def read_rows(path):
    with path.open(newline='') as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError('grid columns do not match the source-bound schema')
        raw=list(reader)
    rows=[]
    for row in raw:
        if row.get('index') is None or not row['index'].isdigit():
            raise ValueError('noninteger grid index')
        converted={k:exact(v) for k,v in row.items() if k!='index'}
        converted['index']=int(row['index'])
        rows.append(converted)
    return rows


def endpoint_tail(actual_upper, *, gap=GAP, centered=False):
    if centered is not True or type(gap) is not Q or gap <= 0:
        raise ValueError('positive centered same-measure gap is required')
    actual_upper=exact(actual_upper)
    if actual_upper < 0:
        raise ValueError('endpoint upper bound cannot be negative')
    return actual_upper/gap


def apply_readout(rows,provenance,positive_budget,zero_budget):
    # A flag is not physical provenance: require the exact owned theorem binding and
    # reconstruct every arithmetic/analytic field before admitting the grid.
    expected_provenance={'contract_sha256':CONTRACT_SHA,'tau':str(TAU),'L':str(L),
                         'selected':[0,0,0],'state':'same actual chosen AQ state as AT5',
                         'meaning':'analytic reference proxies with actual-state error proof'}
    if provenance != expected_provenance:
        raise ValueError('missing or mismatched source-bound actual-state provenance')
    proved_positive,proved_zero,_=uniform_budget()
    if (positive_budget,zero_budget)!=(proved_positive,proved_zero):
        raise ValueError('analytic budgets must equal the fixed actual-state proof bounds')
    if rows != generate_rows(positive_budget,zero_budget):
        raise ValueError('rows fail reconstruction from the owned analytic proof')
    # Exact rational reported values mean arithmetic input-bin width is exactly zero.
    historical=AT3.evaluate([(r['datum'],r['datum']) for r in rows])
    require(historical['conditional_on_sample_contract'] is True and historical['computed_AQ_samples'] is False,
            'historical conditional flags must remain unchanged')
    trap=sum(((H/2 if j in (0,N) else H)*r['datum'] for j,r in enumerate(rows)),Q(0))
    require(trap==historical['trap_lower']==historical['trap_upper'],'all-node trapezoid mismatch')
    quadrature=H*H*FIRST/8
    noise=T*EPS
    require(quadrature==historical['quadrature_allowance'] and noise==historical['noise_allowance'],
            'unchanged readout budgets')
    mass_tail=historical['tail_upper']
    endpoint_upper=rows[-1]['actual_upper']
    end_tail=endpoint_tail(endpoint_upper,centered=True)
    primary=(max(Q(0),historical['lower']),historical['upper'])
    secondary=(max(Q(0),trap-quadrature-noise),trap+min(mass_tail,end_tail)+noise)
    return {'historical_evaluator_result':historical,'trapezoid':trap,
            'primary_I_interval':primary,'primary_width':primary[1]-primary[0],
            'primary_target_met':primary[1]-primary[0] <= Q(1,500),
            'secondary_I_interval':secondary,'secondary_width':secondary[1]-secondary[0],
            'secondary_target_met':secondary[1]-secondary[0] <= Q(1,2500),
            'quadrature_allowance':quadrature,'deterministic_noise_allowance':noise,
            'mass_only_tail_upper':mass_tail,'endpoint_upper':endpoint_upper,
            'endpoint_tail_upper':end_tail,'used_secondary_tail_upper':min(mass_tail,end_tail),
            'evaluator_arithmetic_trapezoid_width':Q(0),
            'free_inverse':Q(1,12),
            'free_inverse_in_primary':primary[0] <= Q(1,12) <= primary[1],
            'free_inverse_in_secondary':secondary[0] <= Q(1,12) <= secondary[1],
            'interaction_shift_resolved':False,
            'physical_R_intervals':{'primary':{'lower_numerator':primary[0],'upper_numerator':primary[1],
                                               'common_denominator':'alpha'},
                                    'secondary':{'lower_numerator':secondary[0],'upper_numerator':secondary[1],
                                                 'common_denominator':'alpha'},
                                    'alpha_must_be_positive':True,'units':'inverse physical energy'}}


def main(output):
    require(output.is_absolute() and not output.exists(),'absolute fresh output required')
    contract_path=BASE/'inputs/research/round31/contracts/at6.json'
    require(sha(contract_path)==CONTRACT_SHA,'contract hash changed')
    contract=json.loads(contract_path.read_text())
    for source in contract['shared_premises']+[contract['contract_review']]:
        require((BASE/'inputs'/source).is_file(),'missing declared source snapshot: '+source)
    require(sha(BASE/'inputs/research/round31/reverse/at5/check.py')==ARITH_SHA,'inherited arithmetic changed')
    require(sha(BASE/'inputs/research/round30/forward/at3/evaluator.py')==EVALUATOR_SHA,'historical evaluator changed')
    require((BASE/'inputs/AGENTS.md').is_file(),'missing instruction snapshot')
    positive,zero,endpoint=uniform_budget()
    rows=generate_rows(positive,zero)
    provenance={'contract_sha256':CONTRACT_SHA,'tau':str(TAU),'L':str(L),'selected':[0,0,0],
                'state':'same actual chosen AQ state as AT5',
                'meaning':'analytic reference proxies with actual-state error proof'}
    output.mkdir(parents=True)
    save_rows(output/'aq-analytic-grid.csv',rows)
    reread=read_rows(output/'aq-analytic-grid.csv')
    require(reread==rows,'CSV roundtrip changed exact values')
    readout=apply_readout(reread,provenance,positive,zero)
    checks=[]

    def check(name,condition,**detail):
        require(condition,'AT6 control failed: '+name)
        checks.append({'id':name,'passed':True,**detail})

    check('continuous_window_derivative_margin',L/T > 4 and ARITH.log_positive(Q(17))[0] > 2)
    check('zero_variance_ground_centering',rows[0]['datum']==Q(1,4)
          and rows[0]['reference_arithmetic_error']==0
          and rows[0]['actual_correlation_error']==zero
          and endpoint['error_budget']['centering_mean_square_upper'] > 0)
    check('all_4097_nodes_fixed_clock',len(rows)==4097 and all(r['s']==Q(j,32) for j,r in enumerate(rows))
          and rows[-1]['s']==128,physical_step='hbar/(32 alpha)',physical_end='128 hbar/alpha')
    check('all_node_actual_errors',max(r['actual_correlation_error'] for r in rows) <= EPS,
          largest_complete_error=max(r['actual_correlation_error'] for r in rows))
    check('analytic_vs_arithmetic_bins',readout['evaluator_arithmetic_trapezoid_width']==0
          and all(r['actual_correlation_error']==r['analytic_comparison_error']+r['reference_arithmetic_error']
                  for r in rows))
    check('endpoint_half_weights',sum((H/2 if j in (0,N) else H for j in range(N+1)),Q(0))==T
          and H*sum((r['datum'] for r in rows),Q(0))!=readout['trapezoid'])
    check('primary_target',readout['primary_target_met'] is True)
    check('secondary_endpoint_target',readout['secondary_target_met'] is True
          and readout['endpoint_tail_upper'] < readout['mass_only_tail_upper'])
    check('actual_endpoint_not_reference_alone',rows[-1]['actual_upper'] > rows[-1]['reference_upper']
          and readout['endpoint_tail_upper'] > 16*rows[-1]['reference_upper'],
          reference_upper=rows[-1]['reference_upper'],actual_upper=rows[-1]['actual_upper'])
    check('unchanged_historical_provenance_flags',readout['historical_evaluator_result']['computed_AQ_samples'] is False
          and readout['historical_evaluator_result']['conditional_on_sample_contract'] is True)
    try:
        apply_readout(rows,None,positive,zero)
    except ValueError:
        rejected=True
    else:
        rejected=False
    check('missing_actual_provenance_rejected',rejected)
    incomplete=rows[:-1]
    try:
        apply_readout(incomplete,provenance,positive,zero)
    except ValueError:
        rejected=True
    else:
        rejected=False
    check('missing_node_rejected',rejected)
    changed=[dict(r) for r in rows]
    changed[0]['actual_correlation_error']=Q(0)
    try:
        apply_readout(changed,provenance,positive,zero)
    except ValueError:
        rejected=True
    else:
        rejected=False
    check('coherent_zero_error_claim_rejected',rejected)
    try:
        apply_readout(generate_rows(Q(0),Q(0)),provenance,Q(0),Q(0))
    except ValueError:
        rejected=True
    else:
        rejected=False
    check('coherently_reconstructed_zero_budgets_rejected',rejected)
    noise=readout['deterministic_noise_allowance']
    constant_error=sum(((H/2 if j in (0,N) else H)*EPS for j in range(N+1)),Q(0))
    check('root_N_deterministic_error_invalid',constant_error==noise and constant_error > noise/64,
          constant_sign_error=constant_error,wrong_root_N_budget=noise/64)
    # Valid abstract slow positive spectrum: mass1/4 at x1/16. Tail beats any
    # trapezoid excess plus the inherited noise, so deleting the tail excludes I=4.
    slow_mass,slow_x=Q(1,4),GAP
    e8lo,e8hi=ARITH.exp_minus(Q(8))
    slow_tail_lower=slow_mass/slow_x*e8lo
    slow_quad=H*H*(slow_mass*slow_x)/8
    check('deleting_infinite_tail_fails',slow_tail_lower > slow_quad+noise
          and slow_mass<=MASS and slow_mass*slow_x<=FIRST,
          exact_inverse=slow_mass/slow_x,tail_lower=slow_tail_lower,
          maximal_no_tail_excess=slow_quad+noise)
    # Convex free heat yields trap>integral even allowing the tiny omitted free tail.
    e384lo,e384hi=ARITH.exp_minus(Q(384))
    free_finite_upper=(1-e384lo)/12
    check('wrong_quadrature_sign',readout['trapezoid'] > free_finite_upper)
    try:
        endpoint_tail(Q(1,100),gap=Q(0),centered=False)
    except ValueError:
        rejected=True
    else:
        rejected=False
    check('zero_energy_contamination_rejected',rejected,
          diagnosis='positive vacuum atom has constant correlation and divergent inverse integral')
    check('free_inverse_included_not_detected',readout['free_inverse_in_primary'] is True
          and readout['free_inverse_in_secondary'] is True and readout['interaction_shift_resolved'] is False)
    cap=ARITH.certify({**ARITH.FROZEN,'tau':'1/100000000'})
    oldcut=ARITH.certify({**ARITH.FROZEN,'L':'10000'})
    check('original_cap_and_old_cutoff_still_fail',cap['target_met'] is False and oldcut['target_met'] is False)
    # Exact endpoint gap tail on the slow atom is equality, with all arithmetic directed.
    check('endpoint_tail_same_measure_gap',slow_mass/slow_x==16*slow_mass
          and 16*slow_mass*e8lo <= slow_tail_lower <= 16*slow_mass*e8hi)
    require(all(c['passed'] is True for c in checks),'control semantics')
    result={'loop':'AT6','direction':'reverse','contract_sha256':CONTRACT_SHA,
            'tau':TAU,'selected':[0,0,0],'L':L,'T':T,'h':H,'N':N,'node_count':len(rows),
            'actual_aq_enclosure':True,'actual_aq_grid_provenance_established':True,
            'proxy_values_are_measurements':False,'proxy_values_are_interacting_simulation_outputs':False,
            'uniform_wilson_claim':False,'continuum_claim':False,'state_uniqueness_claim':False,
            'scientific_priority_verified':False,'interaction_shift_resolved':False,
            'primary_target_met':readout['primary_target_met'],'secondary_target_met':readout['secondary_target_met'],
            'uniform_positive_time_analytic_error':positive,'zero_time_analytic_error':zero,
            'largest_complete_node_error':max(r['actual_correlation_error'] for r in rows),
            'endpoint_error_budget':endpoint['error_budget'],
            'provenance':provenance,'readout':readout,'checks':checks,
            'stop':'Investigation3of3 completed; no further scientific execution authorized in this cycle'}
    write_json(output/'results.json',result)
    write_json(output/'inverse-enclosures.json',readout)
    write_json(output/'grid-provenance.json',{**provenance,'grid_sha256':sha(output/'aq-analytic-grid.csv'),
                                             'node_count':len(rows),'absolute_error_limit':EPS,
                                             'uniform_positive_time_error':positive,
                                             'zero_time_error':zero,
                                             'largest_complete_error':max(r['actual_correlation_error'] for r in rows)})
    sources={str(p.relative_to(BASE)):sha(p) for p in sorted((BASE/'inputs').rglob('*')) if p.is_file()}
    sources.update({name:sha(BASE/name) for name in ('check.py','report.md')})
    files=['results.json','aq-analytic-grid.csv','inverse-enclosures.json','grid-provenance.json']
    write_json(output/'source-manifest.json',{'schema':'at6-reverse-manifest-v1','sources':sources,
                                            'outputs':{name:sha(output/name) for name in files}})
    print('AT6 reverse: '+str(len(checks))+' checks passed; 4097 analytic AQ nodes; both inverse width targets met')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True,type=Path)
    main(parser.parse_args().output)
