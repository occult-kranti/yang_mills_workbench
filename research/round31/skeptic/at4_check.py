#!/usr/bin/env python3
"""Independent Round31 AT4 exact arithmetic and scientific countercontrols.

Written after the contract freeze and before reading either current producer.
No imports from producers; no sampled numerical approximation certifies a bound.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import argparse
import json

def execute():
    checks=[]
    def need(v,label):
        if v is not True or label in checks: raise RuntimeError(label)
        checks.append(label)
    def negexp_small(x,n=30):
        if not F(0)<=x<=1 or n%2: raise ValueError('small nonnegative x and even degree required')
        term=F(1);part=term
        for k in range(1,n+1):
            term*=-x/k;part+=term
        # Alternating terms decrease for x<=1: even upper, next odd lower.
        return part+term*(-x)/(n+1),part
    def sqrtbin(x,scale=10**15):
        if x<0: raise ValueError('negative square root')
        k=isqrt(x.numerator*scale*scale//x.denominator)
        return F(k,scale),F(k+1,scale)
    tau=F(1,10**8); eps=F(1,10**6);L=F(10000);s=F(1)
    R={(0,0,0),(0,0,1)};S={(0,0,0),(1,0,0),(0,1,0),(0,0,1)}
    incident={tuple(r[i]-t[i] for i in range(3)) for r in R for t in S}
    need(len(incident)==7,'complete_seven_incoming_and_outgoing_stars')
    need(len([b for b in incident if min(b)>=0])==2,'orthant_two_star_substitution_detected')
    links=set();endpoints=set()
    for bx,by,bz in R:
        for x in range(4*bx,4*bx+4):
            for y in range(2*by,2*by+2):
                for axis in range(3):
                    p=(x,y,bz);q=list(p);q[axis]+=1
                    links.add((p,axis));endpoints.update((p,tuple(q)))
    need(len(links)==48 and len(endpoints)==36,'complete_factor_links_and_original_endpoints')
    reset=14*len(incident)*tau
    d_lo,d_hi=sqrtbin(4*reset)
    need(d_lo*d_lo<=4*reset<=d_hi*d_hi,'exact_local_trace_distance_enclosure')
    need(d_lo>eps,'inherited_state_upper_budget_already_exceeds_target')
    # d is an upper certificate; its size does not lower-bound actual distance.
    need(d_hi<F(1,500),'rational_uniform_state_distance_cap')
    kappa=2*len(incident)*7*tau/8
    need(kappa==49*tau/4,'physical_clock_duhamel_constant')
    need(kappa!=2*len(incident)*7*tau,'normalized_clock_factor_eight_countercontrol')
    # Kernel mass <=1 on retained window; tail<=2s/(pi L), difference<=2.
    # pi>3 gives a fully rational outward time-tail budget.
    state=d_hi;centering=d_hi*d_hi;dynamics=kappa*L;tail=4*s/(3*L)
    error=state+centering+dynamics+tail
    need(error>eps,'frozen_cutoff_radius_insufficient')
    need(2*error>2*eps,'radius_and_full_interval_width_kept_distinct')
    need(tail>eps,'omitted_poisson_tail_is_material')
    need(kappa*F(2)<kappa*7,'missing_incoming_stars_undercharges_dynamic_budget')
    # A state-independent free-point bracket uses the pure-electric Wilson energy.
    ylo,yhi=negexp_small(F(1));free_lo=ylo**3/4;free_hi=yhi**3/4
    need(F(1,3)<ylo<yhi<F(3,8),'directed_exponential_bracket_at_one')
    need(free_lo<free_hi and free_hi-free_lo<F(1,10**25),'directed_free_C1_arithmetic_width')
    enclosing=(max(F(0),free_lo-error),free_hi+error)
    need(enclosing[1]-enclosing[0]>2*eps,'analytic_actual_state_enclosure_insufficient')
    # A/B exact common data and point-estimation lower bound at s=1.
    A=[(F(1,8),F(2)),(F(1,8),F(4))]
    B=[(F(1,32),F(1)),(F(3,16),F(3)),(F(1,32),F(5))]
    moment=lambda atoms,k:sum(p*x**k for p,x in atoms)
    common=[F(1,4),F(3,4),F(5,2)]
    need([moment(A,k) for k in range(3)]==common,'A_exact_first_three_moments')
    need([moment(B,k) for k in range(3)]==common,'B_exact_first_three_moments')
    need(common[2]<36+98*tau,'second_moment_only_ceiling_not_equality')
    # Polynomial in y: B-A = y(1-y)^4/32 for every y, not just a point.
    poly=[F(0),F(1,32),F(-1,8),F(3,16),F(-1,8),F(1,32)]
    binom=[F(0),F(1,32),F(-4,32),F(6,32),F(-4,32),F(1,32)]
    need(poly==binom,'continuous_AB_gap_factorization')
    minimax_lower=F(1,3)*F(5,8)**4/64
    need(minimax_lower==F(625,786432) and minimax_lower>eps,'same_moment_minimax_lower_bound_exceeds_target')
    need(2*minimax_lower>2*eps,'no_common_radius_epsilon_interval_for_AB')
    exact_gap_lo=ylo*(1-yhi)**4/32;exact_gap_hi=yhi*(1-ylo)**4/32
    need(exact_gap_lo/2>minimax_lower,'directed_AB_gap_stricter_than_simple_lower')
    # Full vector centering and scalar subtraction do not have the same residue.
    m=F(1,1000);mhat=-m
    vector=(m-mhat)**2;scalar=m*m-mhat*mhat
    need(vector==F(1,250000) and scalar==0,'vector_centering_residue_despite_scalar_cancellation')
    mhat=2*m
    need((m-mhat)**2==eps and m*m-mhat*mhat==-3*eps,'scalar_subtraction_can_be_negative')
    need((m-mhat)**2>=0,'vector_residue_is_nonnegative_zero_atom')
    alpha=F(2);hbar=F(3);t=F(3,2)
    need(alpha*t/hbar==1 and (alpha/8)*t/hbar==F(1,8),'physical_euclidean_clock_not_normalized_onsite_clock')
    # Exact fixture exposes selected potential not-Haar at nonzero coefficient.
    lam=F(1,8);trial_t=lam/3
    energy_numerator=3*trial_t*trial_t/4-lam*trial_t/2
    need(energy_numerator<0,'nonzero_selected_potential_invalidates_Haar_vacuum')
    need(F(0)<=F(1,2) and F(0)<=F(1,8),'zero_selected_triple_within_inherited_closed_bounds')
    # Extensive interaction norms cannot replace a volume-uniform local budget.
    need(7*tau*1000>7*tau*7,'extensive_norm_grows_beyond_local_incidence')
    # Eventual convergence supplies no computable index from finitely many values.
    first=[F(0)]*10;second=[F(0)]*10
    need(first==second and F(0)!=F(1),'finite_prefix_does_not_identify_limit_or_rate')
    # Min(linear,uniform) is needed before an unbounded time integral.
    need(kappa*F(10**10)>2,'uncut_linear_bound_exceeds_uniform_difference_cap')
    return {'schema':'hnm-r31-independent-skeptic-controls-v1','loop':'AT4','passed':True,
            'checks_count':len(checks),'checks':checks,
            'independent_certificate':{'trace_distance_upper':str(d_hi),'state':str(state),
                'centering':str(centering),'duhamel':str(dynamics),'poisson_tail':str(tail),
                'radius':str(error),'absolute_target':str(eps),'target_met':False,
                'C1_interval':[str(z) for z in enclosing]},
            'AB_gap_interval':[str(exact_gap_lo),str(exact_gap_hi)],
            'moment_point_estimator_error_lower':str(minimax_lower),
            'scope':'Independent sufficient analytic envelope and abstract information controls; no 1e-6 AQ sample or nonuniqueness theorem.',
            'AQ_sample_at_target_produced':False,'AQ_state_nonuniqueness_proved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    result=execute();(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':True,'checks':result['checks_count'],'target_met':False}))
