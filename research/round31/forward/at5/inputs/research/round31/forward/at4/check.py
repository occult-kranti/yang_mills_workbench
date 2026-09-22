#!/usr/bin/env python3
"""Independent AT4 forward exact geometry and rational-enclosure certificate.

All admission decisions use Fraction/integer arithmetic; no binary floating
transcendental is an input. Analytic completeness is proved in report.md.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import isqrt
import argparse
import hashlib
import json

BASE = Path(__file__).resolve().parent
DEN = 10**30
CONTRACT_SHA = 'ff7d1652f05e2c4201d85237f67780d9eb2456688c39d8398d72fe9a10d1940f'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def down(x):
    return Q((x.numerator*DEN)//x.denominator,DEN)

def up(x):
    return Q(-((-x.numerator*DEN)//x.denominator),DEN)

def textq(x):
    x=Q(x)
    return str(x.numerator) if x.denominator==1 else f'{x.numerator}/{x.denominator}'

def interval(lo,hi):
    require(lo<=hi,'inverted rigorous interval')
    return {'lower':textq(lo),'upper':textq(hi)}

def exp_negative(x):
    """P_41 <= exp(-z) <= P_40 on [0,1/2]; halve then square."""
    x=Q(x); require(x>=0,'negative decay argument')
    halvings=0
    while x>Q(1,2):
        x/=2; halvings+=1
    total=Q(1); term=Q(1); even=None
    for k in range(1,42):
        term*=(-x)/k; total+=term
        if k==40: even=total
    lo,hi=down(total),up(even)
    require(0<=lo<=hi<=1,'invalid alternating exponential bracket')
    for _ in range(halvings):
        lo,hi=down(lo*lo),up(hi*hi)
    return lo,hi

def log_small(y):
    """For 1<=y<=2, log y=2 sum z^(2k+1)/(2k+1)."""
    y=Q(y); require(1<=y<=2,'log_small domain')
    z=(y-1)/(y+1); terms=64
    partial=2*sum((z**(2*k+1)/Q(2*k+1) for k in range(terms)),Q(0))
    tail=2*z**(2*terms+1)/(Q(2*terms+1)*(1-z*z))
    return down(partial),up(partial+tail)

def log_positive(y):
    y=Q(y); require(y>=1,'log domain')
    shifts=0
    while y>2:
        y/=2; shifts+=1
    lo,hi=log_small(y); l2,u2=log_small(Q(2))
    return down(lo+shifts*l2),up(hi+shifts*u2)

def atan_interval(z):
    z=Q(z); require(0<=z<=Q(1,5),'atan domain')
    total=Q(0); lower=None; upper=None
    for k in range(80):
        total+=(-1 if k%2 else 1)*z**(2*k+1)/Q(2*k+1)
        if k==78: upper=total
        if k==79: lower=total
    return down(lower),up(upper)

def pi_interval():
    a,b=atan_interval(Q(1,5)); c,d=atan_interval(Q(1,239))
    return down(16*a-4*d),up(16*b-4*c)

def sqrt_interval(x):
    x=Q(x); require(x>=0,'sqrt domain')
    k=isqrt((x.numerator*DEN*DEN)//x.denominator)
    lo=Q(k,DEN); hi=lo if lo*lo==x else Q(k+1,DEN)
    require(lo*lo<=x<=hi*hi,'sqrt bracket failed')
    return lo,hi

def add(a,b):
    return tuple(x+y for x,y in zip(a,b))

def sub(a,b):
    return tuple(x-y for x,y in zip(a,b))

def compute():
    contract=BASE/'inputs/research/round31/contracts/at4.json'
    require(digest(contract)==CONTRACT_SHA,'frozen contract has changed')
    c=json.loads(contract.read_text())
    require(c['id']=='AT4' and c['parameters']['tau'].startswith('1/100000000 '),'wrong contract identity or coupling')
    checks=[]
    def check(identity,condition,**details):
        require(condition,'failed control '+identity)
        checks.append({'id':identity,'passed':True,**details})
    zero=(0,0,0); ex=(1,0,0); ey=(0,1,0); ez=(0,0,1)
    axes=(ex,ey,ez); R={zero,ez}; S={zero,ex,ey,ez}
    links={(add((4*b[0]+r,2*b[1]+s,b[2]),zero),j) for b in R for r in range(4) for s in range(2) for j in range(3)}
    endpoints={p for p,j in links}|{add(p,axes[j]) for p,j in links}
    wilson=[(zero,0,1),(ex,2,1),(ez,0,-1),(zero,2,-1)]
    owners=[(p[0]//4,p[1]//2,p[2]) for p,j,sign in wilson]
    anchors={sub(r,s) for r in R for s in S}
    expected={zero,tuple(-x for x in ex),tuple(-x for x in ey),tuple(-x for x in ez),ez,sub(ez,ex),sub(ez,ey)}
    check('full_original_wilson_cover',set(owners)==R and len(links)==48 and len(endpoints)==36,links=len(links),endpoints=len(endpoints),owners=owners)
    check('missing_incoming_stars',anchors==expected and len(anchors)==7 and sum(all(a>=0 for a in b) for b in anchors)==2,bulk_count=7,wrong_orthant_count=2)
    tau=Q(1,100000000); s=Q(1); cutoff=Q(10000); target=Q(1,1000000)
    selected=(Q(0),Q(0),Q(0))
    check('zero_selected_is_allowed',abs(selected[0])<=Q(1,2) and abs(selected[1])<=Q(1,8) and abs(selected[2])<=Q(1,2))
    local_gap=Q(8)*Q(3,4)
    free_energy=4*Q(3,4)
    check('electric_and_physical_normalization',local_gap==6 and free_energy==3 and Q(1,8)*7*tau==Q(7,8)*tau,normalized_reference_gap=textq(local_gap),free_W_energy_over_alpha=textq(free_energy))
    reset=2*len(anchors)*7*tau
    excitation=reset/local_gap
    sqrtlo,sqrthi=sqrt_interval(excitation)
    distance_lo,distance_hi=2*sqrtlo,2*sqrthi
    check('reference_gap_six_refinement',reset==98*tau and excitation==Q(49,3)*tau and distance_hi*distance_hi>=4*excitation)
    # A selected one-plaquette trial 1+tW has negative energy for t=lambda/(3alpha).
    lam=Q(1,2); trial_t=lam/3
    trial_numerator=Q(3,4)*trial_t**2-lam*trial_t/2
    check('selected_reference_not_generally_haar',trial_numerator<0,negative_trial_energy_numerator=textq(trial_numerator))
    dynamic_slope=2*len(anchors)*Q(7,8)*tau
    check('local_not_extensive_duhamel',dynamic_slope==Q(49,4)*tau and 7<(2*2)**3,incident_count=7,total_stars_in_centered_N2_box=64)
    pil,piu=pi_interval(); logl,logu=log_positive(1+cutoff**2/s**2)
    check('directed_pi_and_log',Q(314159,100000)<pil<piu<Q(314160,100000) and 18<logl<logu<19)
    # Trace-zero state difference improves positive W^2 expectation error to D/2.
    state_cost=distance_hi
    centering_cost=distance_hi**2
    bulk_dynamic=dynamic_slope*s*logu/pil
    tail_mass=2*s/(pil*cutoff)
    tail_correlation=Q(1,2)+distance_hi/2
    tail_cost=tail_mass*tail_correlation
    error=state_cost+centering_cost+bulk_dynamic+tail_cost
    freelo,freehi=exp_negative(3*s); freelo/=4; freehi/=4
    enclosure_lo=max(Q(0),freelo-error)
    enclosure_hi=min(Q(1,4)+distance_hi/2,freehi+error)
    halfwidth=(enclosure_hi-enclosure_lo)/2
    check('frozen_target_insufficient',halfwidth>target,target_met=False)
    check('whole_poisson_tail_retained',tail_cost>0 and error>state_cost+centering_cost+bulk_dynamic,tail_correlation_upper=textq(tail_correlation))
    # An admissible kernel diagnostic: zero spectral energy gives c(t)=1, and
    # dropping the tail loses exactly its positive mass at every finite cutoff.
    a_lo,a_hi=atan_interval(s/cutoff)
    exact_tail_lo=2*a_lo/piu; exact_tail_hi=2*a_hi/pil
    check('omitted_poisson_tail_damaging_control',exact_tail_lo>0 and exact_tail_hi<=tail_mass,missing_mass=interval(exact_tail_lo,exact_tail_hi),scope='abstract nonnegative-spectrum kernel diagnostic, not AQ centered data')
    A=[(Q(2),Q(1,8)),(Q(4),Q(1,8))]
    B=[(Q(1),Q(1,32)),(Q(3),Q(3,16)),(Q(5),Q(1,32))]
    moment=lambda atoms,k:sum((w*x**k for x,w in atoms),Q(0))
    mA=[moment(A,k) for k in range(3)]; mB=[moment(B,k) for k in range(3)]
    check('same_moments',mA==mB==[Q(1,4),Q(3,4),Q(5,2)])
    def laplace(atoms):
        lo=Q(0); hi=Q(0)
        for x,w in atoms:
            a,b=exp_negative(s*x); lo+=w*a; hi+=w*b
        return lo,hi
    Alo,Ahi=laplace(A); Blo,Bhi=laplace(B)
    information_lo=(Blo-Ahi)/2; information_hi=(Bhi-Alo)/2
    # r(1-r)^4/32 factorization provides an independent exact sign identity.
    coeff_B_minus_A=[Q(0),Q(1,32),-Q(1,8),Q(3,16),-Q(1,8),Q(1,32)]
    factorized=[Q(0),Q(1,32),-Q(4,32),Q(6,32),-Q(4,32),Q(1,32)]
    check('same_moments_unequal_nonzero_time',coeff_B_minus_A==factorized and information_lo>Q(9,10000),deterministic_worst_case_error_lower=textq(information_lo))
    actual_mean=Q(1,4); mean_error=Q(1,100)
    vector_cost=mean_error**2
    scalar_signed=actual_mean**2-(actual_mean+mean_error)**2
    check('vector_versus_scalar_centering',vector_cost==Q(1,10000) and scalar_signed==-Q(51,10000) and abs(scalar_signed)>vector_cost,vector_additive_error=textq(vector_cost),scalar_signed_error=textq(scalar_signed))
    check('uncentered_vacuum_residue',actual_mean**2==Q(1,16),uncentered_constant=textq(actual_mean**2))
    alpha=Q(5); hbar=Q(7); physical_time=hbar/alpha
    normalized_time=(alpha/8)*physical_time/hbar
    check('wrong_delta_alpha_hbar_clock',alpha*physical_time/hbar==1 and normalized_time==Q(1,8) and 24*normalized_time==3 and 24!=3,physical_time=textq(physical_time),normalized_aq_time=textq(normalized_time))
    # Both traces have the same arbitrary finite observed prefix; limits differ.
    observed_N=100; prefix_A=[Q(0)]*observed_N; prefix_B=[Q(0)]*observed_N
    check('finite_samples_do_not_prove_thermodynamic_rate',prefix_A==prefix_B and Q(0)!=Q(1),description='a_N=0; b_N=0 for N<=100 and b_N=1 later: equal sampled prefix, distinct limits; abstract information control only')
    return {
        'loop':'AT4','direction':'forward','human_author':'Hruday N M (BUNZEEY)',
        'contribution_alias':'HNM-AT4-F local zero-selected AQ heat enclosure',
        'actual_aq_enclosure':True,'actual_aq_point_estimate_at_target':False,
        'target_met':False,'verdict':'valid analytic actual-AQ interval; frozen absolute 1e-6 midpoint target insufficient',
        'uniform_wilson_claim':False,'continuum_claim':False,'state_uniqueness_claim':False,
        'scientific_priority_verified':False,'abstract_controls_are_aq_realizations':False,
        'selected_coefficients_over_alpha':['0','0','0'],'tau':textq(tau),'s':textq(s),'L':textq(cutoff),
        'target_absolute_point_error':textq(target),'local_reset_energy':textq(reset),
        'normalized_free_reference_gap':textq(local_gap),'excitation_mass_upper':textq(excitation),
        'state_distance_upper':textq(distance_hi),'duhamel_slope':textq(dynamic_slope),
        'pi':interval(pil,piu),'log_one_plus_L_squared':interval(logl,logu),
        'costs':{'state':textq(state_cost),'centering':textq(centering_cost),'bulk_dynamic':textq(bulk_dynamic),'whole_tail':textq(tail_cost)},
        'absolute_error_upper':textq(error),'free_C_at_s1':interval(freelo,freehi),
        'actual_C_interval':interval(enclosure_lo,enclosure_hi),'interval_midpoint':textq((enclosure_lo+enclosure_hi)/2),'interval_halfwidth':textq(halfwidth),
        'abstract_information_limit':{'moments':[textq(x) for x in mA],'A_Laplace':interval(Alo,Ahi),'B_Laplace':interval(Blo,Bhi),'minimax_point_error_lower':textq(information_lo),'half_separation':interval(information_lo,information_hi),'factorization':'C_B(1)-C_A(1)=exp(-1)*(1-exp(-1))^4/32'},
        'checks':checks,
        'arithmetic':'exact Fraction; 10^30 outward rational bins; alternating Taylor, positive log series remainder, Machin pi and integer-square-root bounds',
        'limitations':['single zero-selected patterned AQ corner','analytic enclosure does not meet frozen tolerance','no finite volume rate or uniqueness proved','no actual finite-matrix or thermodynamic solver values used','moment ambiguity is about abstract admissible measures, not multiple AQ states']
    }

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True); args=parser.parse_args()
    out=Path(args.output)
    require(out.is_absolute(),'--output must be absolute')
    require(not out.exists(),'--output must be a fresh nonexistent directory')
    result=compute()
    out.mkdir(parents=True)
    results_path=out/'results.json'; results_path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    sources={str(p.relative_to(BASE)):digest(p) for p in sorted(BASE.rglob('*')) if p.is_file() and ('inputs'==p.relative_to(BASE).parts[0] or p.name in ('check.py','report.md'))}
    manifest={'loop':'AT4','direction':'forward','sources':sources,'outputs':{'results.json':digest(results_path)},'contract_sha256':CONTRACT_SHA}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'loop':'AT4','direction':'forward','checks_passed':len(result['checks']),'target_met':result['target_met'],'output_files':['results.json','source-manifest.json']},sort_keys=True))

if __name__=='__main__':
    main()
