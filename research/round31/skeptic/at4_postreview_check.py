#!/usr/bin/env python3
"""Independent validation of producer AT4 refinements after both freezes."""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import json,argparse
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def run():
    checks=[]
    def need(v,k):
        if v is not True or k in checks:raise RuntimeError(k)
        checks.append(k)
    def atan(x,n=40):
        p=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(n)),F(0))
        return p,p+x**(2*n+1)/F(2*n+1)
    def logseries(x,n):
        z=(x-1)/(x+1)
        p=2*sum((z**(2*k+1)/F(2*k+1) for k in range(n)),F(0))
        return p,p+2*z**(2*n+1)/(F(2*n+1)*(1-z*z))
    a,b=atan(F(1,5));c,d=atan(F(1,239));pi=(16*a-4*d,16*b-4*c)
    l10=logseries(F(10),300);lmini=logseries(1+F(1,10**8),5)
    logarithm=(8*l10[0]+lmini[0],8*l10[1]+lmini[1])
    p=F(49,3*10**8);scale=10**45;k=isqrt(p.numerator*scale*scale//p.denominator)
    d=(2*F(k,scale),2*F(k+1,scale));slope=F(49,4*10**8)
    dynamic=(slope*logarithm[0]/pi[1],slope*logarithm[1]/pi[0])
    tailF=((F(1,2)+d[0]/2)*2/(pi[1]*10000),(F(1,2)+d[1]/2)*2/(pi[0]*10000))
    atl,atu=atan(F(1,10000),8);tailR=(4*atl/pi[1],4*atu/pi[0])
    fr=json.loads((ROOT/'research/round31/forward/at4/output/results.json').read_text())
    rr=json.loads((ROOT/'research/round31/reverse/at4/output/results.json').read_text())
    for prefix, data, piin, login in [('forward',fr,fr['pi'],fr['log_one_plus_L_squared']),('reverse',rr,rr['constants']['pi_interval'],rr['constants']['log_one_plus_L_squared_interval'])]:
        if isinstance(piin,dict):piin=[piin['lower'],piin['upper']];login=[login['lower'],login['upper']]
        need(F(piin[0])<=pi[0]<pi[1]<=F(piin[1]),prefix+'_pi_contains_independent_enclosure')
        need(F(login[0])<=logarithm[0]<logarithm[1]<=F(login[1]),prefix+'_log_contains_independent_base10_enclosure')
    fc=fr['costs'];rc=rr['error_budget']
    for label,x,interval in [('forward_state',fc['state'],d),('reverse_state',rc['state_trace_norm_upper'],d),('forward_dynamics',fc['bulk_dynamic'],dynamic),('reverse_dynamics',rc['duhamel_inside_upper'],dynamic),('forward_tail',fc['whole_tail'],tailF),('reverse_tail',rc['poisson_tail_upper'],tailR)]:
        need(F(x)>=interval[1],label+'_outward_bound')
    need(F(fc['centering'])>=4*p and F(rc['centering_mean_square_upper'])==4*p,'centering_upper_semantics')
    need(F(fc['whole_tail'])<F(rc['poisson_tail_upper']),'forward_effect_tail_refinement_is_stricter')
    need(F(fr['absolute_error_upper'])==sum(map(F,fc.values())),'forward_budget_complete_sum')
    need(F(rc['radius_upper'])==sum(F(rc[k]) for k in ['state_trace_norm_upper','centering_mean_square_upper','duhamel_inside_upper','poisson_tail_upper']),'reverse_budget_complete_sum')
    # Independent exact free value and A/B gap from a single alternating e^-1.
    part=term=F(1)
    for k in range(1,45):term*=-F(1,k);part+=term
    yl=part-term/F(45);yh=part
    free=(yl**3/4,yh**3/4);half=(yl*(1-yh)**4/64,yh*(1-yl)**4/64)
    need(F(fr['free_C_at_s1']['lower'])<=free[0]<free[1]<=F(fr['free_C_at_s1']['upper']),'forward_free_value_independent_bracket')
    need(F(rr['free_reference_correlation_interval'][0])<=free[0]<free[1]<=F(rr['free_reference_correlation_interval'][1]),'reverse_free_value_independent_bracket')
    need(F(fr['abstract_information_limit']['minimax_point_error_lower'])<=half[0] and half[0]>F(9,10000),'forward_minimax_lower_rechecked')
    need(F(rr['moment_information']['deterministic_minimax_error_lower'])<=half[0],'reverse_minimax_lower_rechecked')
    for prefix,lo,hi,error,mid in [('forward',fr['actual_C_interval']['lower'],fr['actual_C_interval']['upper'],fr['interval_halfwidth'],fr['interval_midpoint']),('reverse',rr['actual_centered_correlation_interval'][0],rr['actual_centered_correlation_interval'][1],rr['absolute_point_error_upper'],rr['midpoint_estimator'])]:
        lo,hi,error,mid=map(F,(lo,hi,error,mid))
        need(error==(hi-lo)/2 and mid==(hi+lo)/2,prefix+'_actual_midpoint_radius')
        need(error>F(1,10**6),prefix+'_frozen_target_insufficient')
    need(fr['target_met'] is False and rr['target_met'] is False,'no_target_promotion')
    need(fr['abstract_controls_are_aq_realizations'] is False and rr['moment_information']['actual_AQ_realization_claim'] is False,'abstract_information_class_scope')
    return {'loop':'AT4','schema':'hnm-r31-postcomparison-independent-controls-v1','passed':True,'checks':checks,'checks_count':len(checks),'directional_refinement':'Forward effect trace bound v<=1/4+D/2 improves tail; reviewed after independent production.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    result=run();(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':True,'checks':result['checks_count']}))
