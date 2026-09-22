#!/usr/bin/env python3
"""Direct frozen calculator audit and independent tight constants for AT5."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import argparse,importlib.util,json,sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def run():
    checks=[]
    def need(v,k):
        if v is not True or k in checks:raise RuntimeError(k)
        checks.append(k)
    fw=load('fw_at5_audit',ROOT/'research/round31/forward/at5/calculator.py')
    rv=load('rv_at5_audit',ROOT/'research/round31/reverse/at5/check.py')
    f=fw.certify(fixed_design=True);r=rv.certify(rv.FROZEN,fixed_design=True)
    fs=json.loads((ROOT/'research/round31/forward/at5/output/results.json').read_text());rs=json.loads((ROOT/'research/round31/reverse/at5/output/results.json').read_text());datum=json.loads((ROOT/'research/round31/reverse/at5/output/datum.json').read_text())
    need(all(f[k]==fs[k] for k in f),'forward_api_matches_frozen_output')
    need(all(rv.serial(r[k])==rs[k] for k in r),'reverse_api_matches_frozen_output')
    need(F(datum['value'])==r['exported_datum'] and F(datum['absolute_error'])==r['certified_absolute_error'],'exported_datum_complete_radius_matches_API')
    own=json.loads((HERE/'at5-independent/results.json').read_text())
    ownradius=F(own['independent_bound']['complete_radius'])
    for name,datumv,rad,ends,free,cost in [('forward',F(f['certified_datum']),F(f['certified_absolute_error']),[F(f['actual_C_interval'][k]) for k in ['lower','upper']],[F(f['free_C_interval'][k]) for k in ['lower','upper']],sum(map(F,f['costs'].values()))),('reverse',r['exported_datum'],r['certified_absolute_error'],r['actual_centered_correlation_interval'],r['free_reference_interval'],r['error_budget']['unclipped_total_radius_upper'])]:
        need(rad==cost and rad==(ends[1]-ends[0])/2,name+'_complete_costs_radius')
        need(datumv==(ends[0]+ends[1])/2,name+'_rational_midpoint')
        need(F(0)<rad<ownradius<F(1,10**6),name+'_independent_coarse_success_crosscheck')
        need(ends[0]<=free[0]<=free[1]<=ends[1],name+'_free_reference_inclusion')
    def atan(x,n=40):
        p=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(n)),F(0));return p,p+x**(2*n+1)/F(2*n+1)
    def logseries(x,n):
        z=(x-1)/(x+1);p=2*sum((z**(2*k+1)/F(2*k+1) for k in range(n)),F(0));return p,p+2*z**(2*n+1)/(F(2*n+1)*(1-z*z))
    a,b=atan(F(1,5));c,d=atan(F(1,239));pi=(16*a-4*d,16*b-4*c)
    l10=logseries(F(10),300);lm=logseries(1+F(1,10**18),3);ln=(18*l10[0]+lm[0],18*l10[1]+lm[1])
    p=F(49,3*10**14);scale=10**45;k=isqrt(p.numerator*scale*scale//p.denominator);du=2*F(k+1,scale)
    dynamic_hi=F(49,4*10**14)*ln[1]/pi[0]
    need(F(f['costs']['state'])>=du and r['error_budget']['state_trace_norm_upper']>=du,'both_state_budgets_outward_independent_sqrt')
    need(F(f['costs']['centering'])>=4*p and r['error_budget']['centering_mean_square_upper']==4*p,'both_true_mean_square_budgets')
    need(F(f['costs']['real_time_comparison'])>=dynamic_hi and r['error_budget']['duhamel_inside_upper']>=dynamic_hi,'both_dynamic_budgets_outward_independent_log')
    need(F(f['costs']['Poisson_tail'])>=(F(1,2)+du/2)*2/(pi[0]*10**9),'forward_effect_tail_outward')
    need(r['error_budget']['poisson_tail_upper']>=4/(pi[0]*10**9),'reverse_conservative_tail_outward')
    # These are API domain controls and matched scientific cases, not new loops.
    cases=[('tau_float',{'tau':1e-14}),('tau_bool',{'tau':True}),('s_bool',{'s':True}),('s_zero',{'s':0}),('s_negative',{'s':-1}),('L_zero',{'L':0}),('L_negative',{'L':-1}),('alpha_zero',{'alpha':0}),('hbar_zero',{'hbar':0}),('E_star_zero',{'E_star':0}),('s_nan',{'s':'NaN'}),('s_inf',{'s':'Infinity'}),('bad_rational',{'tau':'1/0'}),('selected_nonzero',{'selected':[0,1,0]}),('selected_float',{'selected':[0,0.0,0]}),('selected_count',{'selected':[0,0]}),('tau_above_cap',{'tau':'1/10000000'}),('tau_below_cap',{'tau':'-1/10000000'})]
    for name,delta in cases:
        for direction,call in [('forward',lambda:fw.certify(**delta)),('reverse',lambda:rv.certify({**rv.FROZEN,**delta}))]:
            try:call()
            except (ValueError,TypeError,ZeroDivisionError):rejected=True
            else:rejected=False
            need(rejected,direction+'_reject_'+name)
    for name,delta in [('time',{'s':'2'}),('cutoff',{'L':'10000'}),('coupling',{'tau':'0'})]:
        for direction,call in [('forward',lambda:fw.certify(**delta,fixed_design=True)),('reverse',lambda:rv.certify({**rv.FROZEN,**delta},fixed_design=True))]:
            try:call()
            except ValueError:rejected=True
            else:rejected=False
            need(rejected,direction+'_fixed_design_reject_'+name)
    for direction,call in [('forward',lambda **kw:fw.certify(**kw)),('reverse',lambda **kw:rv.certify({**rv.FROZEN,**kw}))]:
        neg=call(tau='-1/100000000000000');zero=call(tau=0);short=call(L='10000');cap=call(tau='1/100000000')
        need(neg['target_met'] is True,direction+'_negative_coupling_control')
        need(zero['target_met'] is True,direction+'_exact_zero_branch')
        need(short['target_met'] is False and cap['target_met'] is False,direction+'_honest_insufficient_controls')
    # General positive input domain outside the fixed s=1 case: broad, correctly insufficient.
    need(fw.certify(s=2,L='1/10')['target_met'] is False,'forward_general_domain_honest_broad_result')
    need(rv.certify({**rv.FROZEN,'s':2,'L':'1/10'})['actual_centered_correlation_interval']==[F(0),F(1)],'reverse_general_domain_valid_clipping')
    need(f['resolved_interaction_shift'] is False and r['interaction_shift_resolved'] is False,'no_claim_of_detected_interaction_shift')
    return {'schema':'hnm-r31-skeptic-api-audit-v1','loop':'AT5','passed':True,'checks':checks,'checks_count':len(checks)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True);r=run();(out/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'passed':True,'checks':r['checks_count']}))
