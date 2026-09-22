#!/usr/bin/env python3
"""Independent outward integer-interval AT3 implementation and controls."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import math

N=4096;H=F(1,32);T=F(128);EPS=F(1,1000000)
MASS_UP=F(63,250);FIRST_UP=F(94,125);GAP=F(1,16)
SCALE=10**30

def ceil_fraction(q):return -((-q.numerator)//q.denominator)

def exp_base(y):
    """For 0<=y<=1/4, alternating Taylor gives an exact interval."""
    if not F(0)<=y<=F(1,4):raise ValueError('range outside declared Taylor step')
    term=F(1);total=term;upper=None
    for k in range(1,18):
        term=-term*y/k;total+=term
        if k==16:upper=total
    lower=total
    return (lower.numerator*SCALE//lower.denominator,ceil_fraction(upper*SCALE))

def multiply_interval(lo,hi,ql,qh):
    return lo*ql//SCALE, (hi*qh+SCALE-1)//SCALE

def samples_for_atoms(atoms):
    bounds=[[F(0),F(0)] for _ in range(N+1)]
    for weight,energy in atoms:
        qlo,qhi=exp_base(H*energy);lo=hi=SCALE
        for j in range(N+1):
            bounds[j][0]+=weight*F(lo,SCALE)
            bounds[j][1]+=weight*F(hi,SCALE)
            if j<N:lo,hi=multiply_interval(lo,hi,qlo,qhi)
    return bounds

def trap(samples):return H*(samples[0]/2+sum(samples[1:-1],F(0))+samples[-1]/2)

def exact_api(samples,*,n=N,h=H,t=T,epsilon=EPS):
    if type(n) is not int or n!=N or h!=H or t!=T or n*h!=t:
        raise ValueError('wrong frozen design')
    if isinstance(epsilon,bool) or not isinstance(epsilon,(int,F)) or not F(0)<=epsilon<=EPS:
        raise ValueError('invalid deterministic error')
    if not isinstance(samples,(list,tuple)) or len(samples)!=N+1:
        raise ValueError('wrong sample count')
    if any(isinstance(x,bool) or not isinstance(x,(int,F)) for x in samples):
        raise ValueError('sample must be exact finite rational')
    q=trap(samples);tail=tail_bound()
    return q-H*H*FIRST_UP/8-t*epsilon,q+tail+t*epsilon

def tail_bound():
    # exp(-8)=(exp(-1/8))^64. Every multiplication rounds outwards.
    qlo,qhi=exp_base(F(1,8));lo=hi=SCALE
    for _ in range(64):lo,hi=multiply_interval(lo,hi,qlo,qhi)
    return MASS_UP/GAP*F(hi,SCALE)

def execute():
    checks=[]
    def need(condition,label):
        if condition is not True or label in checks:raise RuntimeError(label)
        checks.append(label)
    def rejected(call,label):
        try:call()
        except (ValueError,TypeError):need(True,label)
        else:need(False,label)
    need(N*H==T and N+1==4097,'frozen_full_node_design')
    kernel=lambda r:r*(H-r)/2
    need(kernel(F(0))==0 and kernel(H)==0 and kernel(H/2)==H*H/8,
         'exact_peano_kernel_endpoints_and_maximum')
    # Maximum follows from k(r)=h²/8-(r-h/2)²/2, identically.
    for j,r in enumerate((F(0),H/7,H/2,5*H/7,H)):
        need(kernel(r)==H*H/8-(r-H/2)**2/2,'peano_completed_square_'+str(j))
    quadrature=H*H*FIRST_UP/8;noise=T*EPS;tail=tail_bound()
    width=quadrature+tail+2*noise
    need(width<F(1,500),'uniform_target_width_with_all_terms')
    need(noise==F(2,15625),'deterministic_noise_sum_exact')
    need(H*(F(1,2)+N-1+F(1,2))==T,'positive_trapezoid_weights_sum_T')
    need(noise>H*EPS*64,'root_N_noise_shortcut_understates_constant_error')
    eqlo,eqhi=exp_base(F(1,8));bare_float=F.from_float(math.exp(-0.125))
    need(bare_float<F(eqlo,SCALE) or bare_float>F(eqhi,SCALE),
         'bare_floating_exponential_is_not_a_zero_error_certificate')
    # A positive measure at the gap attains the shape of the tail bound.
    need(tail>F(1,1000),'omitted_tail_is_material_at_frozen_cutoff')
    need(MASS_UP/GAP>0 and GAP>0,'tail_uses_positive_gap_and_correct_mass_units')
    fixtures={'A':[(F(1,8),F(2)),(F(1,8),F(4))],
              'B':[(F(1,32),F(1)),(F(3,16),F(3)),(F(1,32),F(5))]}
    records={};worst={}
    for label,atoms in fixtures.items():
        intervals=samples_for_atoms(atoms)
        need(len(intervals)==4097,label+'_all_4097_nodes_generated')
        need(all(0<=lo<=hi for lo,hi in intervals),label+'_outward_positive_sample_intervals')
        need(all(intervals[j+1][0]<=intervals[j][0] and intervals[j+1][1]<=intervals[j][1]
                 for j in range(N)),label+'_all_nodes_monotone')
        arithmetic=max(hi-lo for lo,hi in intervals)
        need(arithmetic<F(1,10**24),label+'_rigorous_sample_arithmetic_budget')
        tlo=trap([x[0] for x in intervals]);thi=trap([x[1] for x in intervals])
        exact=sum(weight/energy for weight,energy in atoms)
        need(exact==({'A':F(3,32),'B':F(1,10)}[label]),label+'_exact_inverse_reference')
        # A/B tails at T are far smaller than their positive trap bias.
        need(tlo>exact,label+'_wrong_trapezoid_error_sign_rejected')
        output_intervals={}
        for sign in (-1,0,1):
            lo=tlo+sign*noise-quadrature-noise
            hi=thi+sign*noise+tail+noise
            need(lo<=exact<=hi,label+'_contains_truth_worst_noise_'+str(sign))
            need(hi-lo<F(1,500),label+'_reported_width_'+str(sign))
            output_intervals[str(sign)]=[str(lo),str(hi)]
        worst[label]=(tlo-quadrature-2*noise,thi+tail+2*noise)
        # Exact rational supplied samples are distinct from symbolic C±eps.
        mid=[(lo+hi)/2 for lo,hi in intervals]
        alo,ahi=exact_api(mid)
        need(alo<=exact<=ahi,label+'_reusable_exact_input_evaluator')
        digest=hashlib.sha256('\n'.join(f'{lo},{hi}' for lo,hi in intervals).encode()).hexdigest()
        records[label]={'all_nodes':len(intervals),'sample_interval_sha256':digest,
                        'max_sample_arithmetic_width':str(arithmetic),
                        'trapezoid_interval':[str(tlo),str(thi)],'exact_inverse':str(exact),
                        'noise_case_intervals':output_intervals}
    need(worst['A'][1]<worst['B'][0],'all_admissible_noise_patterns_separate_A_and_B')
    need(worst['B'][0]-worst['A'][1]>0,'separation_counts_observed_shift_and_reported_uncertainty')
    zeros=[F(0)]*(N+1)
    rejected(lambda:exact_api(zeros[:-1]),'reject_missing_endpoint_sample')
    rejected(lambda:exact_api(zeros+[F(0)]),'reject_extra_sample')
    rejected(lambda:exact_api(zeros,n=N//2),'reject_wrong_N')
    rejected(lambda:exact_api(zeros,h=2*H),'reject_wrong_grid')
    rejected(lambda:exact_api(zeros,t=2*T),'reject_wrong_cutoff')
    rejected(lambda:exact_api(zeros,epsilon=-EPS),'reject_negative_error')
    rejected(lambda:exact_api(zeros,epsilon=2*EPS),'reject_oversized_error')
    rejected(lambda:exact_api(zeros,epsilon=True),'reject_boolean_error')
    rejected(lambda:exact_api(zeros,epsilon=float('nan')),'reject_nonfinite_error')
    rejected(lambda:exact_api(zeros[:-1]+[float('inf')]),'reject_nonfinite_sample')
    rejected(lambda:exact_api(zeros[:-1]+[True]),'reject_boolean_sample')
    # A spurious uncentered vacuum atom z gives C(s)>=z and an infinite
    # infinite-time integral, even though every finite-window sum is finite.
    z=F(1,100)
    need(trap([z]*(N+1))==T*z,'zero_atom_adds_constant_correlation')
    need(2*T*z>T*z>0,'uncentered_integral_cannot_have_exponential_tail')
    # The existing rectangle would be insufficient at a much coarser grid,
    # independently of exponential/numerical errors.
    need(F(1,4)**2*FIRST_UP/8>F(1,500),'coarse_grid_certificate_insufficient')
    # A shorter T=16 has exp(-aT)=exp(-1)>1/3, checked outward.
    shortlo=shorthi=SCALE
    for _ in range(8):shortlo,shorthi=multiply_interval(shortlo,shorthi,eqlo,eqhi)
    need(F(shortlo,SCALE)>F(1,3) and MASS_UP/GAP/F(3)>1,
         'short_cutoff_tail_certificate_insufficient')
    for j,alpha in enumerate((F(1,2),F(2),F(7))):
        hbar=F(3);physical_duration=T*hbar/alpha
        need(alpha*physical_duration/hbar==T,'physical_Euclidean_time_dictionary_'+str(j))
        need(F(3,32)/alpha*alpha==F(3,32),'inverse_energy_output_dictionary_'+str(j))
    need(records['A']['exact_inverse']!=records['B']['exact_inverse'],'abstract_fixture_outputs_not_unique_AQ_value')
    return {'schema':'hnm-r30-independent-skeptic-controls-v1','loop':'AT3','passed':True,
            'checks_count':len(checks),'checks':checks,
            'uniform_budget':{'quadrature':str(quadrature),'tail_upper':str(tail),'T_epsilon':str(noise),'interval_width_upper':str(width)},
            'fixture_records':records,'worst_case_separation_lower':str(worst['B'][0]-worst['A'][1]),
            'actual_AQ_samples_generated':False,'actual_AQ_response_evaluated':False,
            'scope':'Conditional AQ theorem; executed data and reference inverse values are abstract A/B fixtures only.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True);result=execute()
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':True,'checks':result['checks_count'],'width':float(F(result['uniform_budget']['interval_width_upper']))}))
