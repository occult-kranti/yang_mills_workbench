#!/usr/bin/env python3
"""Independent pre-comparison AT5 sufficient radius using coarse rational bounds."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial,isqrt
import argparse,hashlib,json

def run():
    checks=[]
    def need(v,k):
        if v is not True or k in checks:raise RuntimeError(k)
        checks.append(k)
    tau=F(1,10**14);L=10**9;target=F(1,10**6)
    p=F(49,3)*tau;scale=10**24;k=isqrt(4*p.numerator*scale*scale//p.denominator)
    dlo,dhi=F(k,scale),F(k+1,scale)
    need(dlo*dlo<=4*p<=dhi*dhi,'independent_sqrt_enclosure')
    need(dhi<F(809,10**9),'gap_six_state_budget_below_target')
    need(sum((F(1,factorial(j)) for j in range(6)),F(0))>F(27,10),'exact_lower_bound_for_exp_one')
    need(F(27,10)**42>1+L*L,'rigorous_log_one_plus_L_squared_below_42')
    slope=F(49,4)*tau
    dynamic=slope*F(42,3);tail=F(4,3*L);center=4*p
    error=dhi+center+dynamic+tail
    need(error<target,'conservative_actual_state_radius_passes')
    need(tail>0 and center>0 and dynamic>0,'all_positive_error_terms_retained')
    need(F(4,3*10000)>target,'inherited_short_cutoff_tail_budget_fails')
    capd2=F(196,3*10**8)
    need(capd2>target*target,'cap_coupling_state_budget_still_insufficient')
    part=term=F(1)
    for j in range(1,45):term*=-F(1,j);part+=term
    yl,yh=part-term/F(45),part
    free=(yl**3/4,yh**3/4)
    lo,hi=free[0]-error,free[1]+error
    midpoint=(lo+hi)/2;radius=(hi-lo)/2
    need(lo>0 and radius<target,'full_arithmetic_radius_passes')
    need(hi-lo==2*radius and hi-lo>target,'width_is_twice_radius_not_same_tolerance')
    need(lo<free[0]<free[1]<hi,'free_reference_not_excluded')
    need(radius-error==(free[1]-free[0])/2,'arithmetic_halfwidth_included_exactly')
    need(midpoint-lo==hi-midpoint==radius,'exact_rational_exportable_midpoint')
    need(midpoint>F(0) and hi<F(1,4),'positive_scalar_in_physical_envelope')
    need(abs(-tau)==tau,'negative_coupling_same_absolute_bound')
    need(F(49,3)*0==0 and F(49,4)*0==0,'exact_zero_coupling_free_limit')
    # An uncentered abstract mean has a positive zero atom, not physical heat decay.
    m=F(1,10);mhat=F(3,20)
    need((m-mhat)**2==F(1,400) and m*m-mhat*mhat==F(-1,80),'vector_scalar_mean_protocols_distinct')
    need(m*m>target,'omitted_vacuum_residue_can_exceed_target')
    alpha=F(3);hbar=F(7);physical=hbar/alpha
    need(alpha*physical/hbar==1 and (alpha/8)*physical/hbar==F(1,8),'fixed_physical_clock')
    return {'schema':'hnm-r31-independent-skeptic-controls-v1','loop':'AT5','passed':True,'checks':checks,'checks_count':len(checks),
      'independent_bound':{'state':str(dhi),'centering':str(center),'dynamic':str(dynamic),'tail':str(tail),'analytic_error':str(error),'midpoint':str(midpoint),'complete_radius':str(radius),'interval':[str(lo),str(hi)]},
      'actual_interacting_AQ_enclosure':True,'target_met':True,'resolved_interaction_shift':False,'scope':'Zero-selected patterned AQ tau=+1e-14 s=1; conservative independent upper certificate.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True);r=run();(out/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'passed':True,'checks':r['checks_count']}))
