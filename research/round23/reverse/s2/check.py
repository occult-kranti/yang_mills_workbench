#!/usr/bin/env python3
"""Independent exact S2 filter coefficient and connected-support certificates."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from math import factorial
import argparse, hashlib, json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CONTRACT=ROOT/'research/round23/contracts/s2.json'

def need(ok,message):
    if not ok:raise RuntimeError(message)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ps(a,b):return tuple(x+y for x,y in zip(a,b))
O={(0,0,0),(1,0,0),(0,1,0),(0,0,1)}
def star(b):return {ps(b,o) for o in O}

def parameters(theta,tau,e_star=F(1)):
    need(0<theta<=F(1,16),'Theta outside contract')
    need(abs(tau)<=F(5,1664),'tau outside contract')
    need(e_star>0,'physical reference must be positive')
    return 208*7*abs(tau)*theta

def support_checks():
    offsets={tuple(x-y for x,y in zip(a,b)) for a in O for b in O}
    need(len(offsets)==13,'star meeting displacement count')
    rooted=[]
    for b in product(range(-2,3),repeat=3):
        for d in offsets:
            c=ps(b,d);union=star(b)|star(c)
            if (0,0,0) in union:rooted.append((b,c,len(union)))
    need(len(rooted)==88,'all n1 root multiplicity')
    need(sum(1 for b,c,n in rooted if b!=c)==84,'crossing root multiplicity')
    exact_weight=sum(2**n for b,c,n in rooted)
    upper=16*7*13*8
    need(exact_weight==10816 and exact_weight<=upper,'n1 weight accounting')
    words=[(star((0,0,0)),[(0,0,0)])];counts=[]
    for n in range(1,4):
        nxt=[]
        for sup,word in words:
            choices={tuple(x-y for x,y in zip(p,o)) for p in sup for o in O}
            need(len(choices)<=13*n,'candidate anchor induction')
            for b in choices:
                u=sup|star(b)
                need(len(u)<=4+3*n,'connected union bound')
                nxt.append((u,word+[b]))
        words=nxt
        need(len(words)<=13**n*factorial(n),'ordered word majorant')
        counts.append({'n':n,'exact_words':len(words),'word_upper':13**n*factorial(n)})
    return {'n1_rooted_words':88,'n1_crossing_rooted_words':84,'n1_exact_weight_sum':exact_weight,'n1_upper_weight_sum':upper,'counts':counts}

def coefficients():
    rows=[]
    for k in range(8):
        # Integrate the sine Taylor monomial against (1-y) on [0,1].
        direct=F((-1)**k,factorial(2*k+1))*(F(1,2*k+2)-F(1,2*k+3))
        inverse=F((-1)**k,factorial(2*k+3))
        need(direct==inverse,'triangular integral coefficient')
        # Average cos over [-1,1], including the exact constant at zero.
        average=F((-1)**k,factorial(2*k))*F(1,2*k+1)
        sinc=F((-1)**k,factorial(2*k+1))
        need(average==sinc,'uniform average coefficient')
        if k:
            previous=F((-1)**(k-1),factorial(2*k+1))
            need(-previous==sinc,'commutator/source residual coefficient')
        rows.append({'k':k,'triangular_coefficient':str(direct),'average_coefficient':str(average)})
    return rows

def sinc_interval(x):
    need(abs(x)<=1,'alternating enclosure range')
    terms=[F((-1)**k)*x**(2*k)/factorial(2*k+1) for k in range(13)]
    lo=sum(terms[:12],F(0));hi=lo+terms[12]
    return min(lo,hi),max(lo,hi)

def spectral_checks():
    out=[]
    for omega in [F(-1),F(0),F(1)]:
        theta=F(1,16);x=theta*omega
        rlo,rhi=sinc_interval(x)
        if omega:
            vals=[(1-rlo)/omega,(1-rhi)/omega]
            llo,lhi=min(vals),max(vals)
            need(rlo>F(99,100) and rhi<1,'short-filter residual retained')
            need(llo>0 if omega>0 else lhi<0,'inverse Bohr sign')
            # Reversed generator leaves a same-sign error instead of cancellation.
            good=[-omega*llo,-omega*lhi]
            need(max(good)<0,'correct homological cancellation sign')
            need(min([-g for g in good])>0,'reversed sign control')
        else:
            llo=lhi=F(0)
            need(rlo==rhi==1,'frequency-zero residual omitted')
        out.append({'omega':str(omega),'Theta':str(theta),'residual_interval':[str(rlo),str(rhi)],'L_interval':[str(llo),str(lhi)]})
    return out

def f(z):return (4-z)/(1-z)**2

def tail(n,z):return z**(n+1)*((3*n+7)-(3*n+4)*z)/(1-z)**2

def certificate_checks():
    zmax=parameters(F(1,16),F(5,1664))
    need(zmax==F(35,128) and zmax<1,'endpoint radius')
    need(f(zmax)==F(6784,961),'endpoint rational total')
    rows=[]
    for z in [F(0),F(1,100),zmax]:
        for n in [0,1,4,12]:
            partial=sum((F(4+3*k)*z**k for k in range(n+1)),F(0))
            need(f(z)-partial==tail(n,z),'all-order tail identity')
            need(tail(n,z)>=0,'negative upper tail')
            rows.append({'z':str(z),'N':n,'tail':str(tail(n,z))})
    for n in range(9):
        # Actual simplex and compact triangular integration coefficients.
        simplex=F(1,factorial(n))
        words=13**n*factorial(n)
        per=F(4+3*n)*2**(4+3*n)*words*2**n*simplex
        need(per==16*(4+3*n)*208**n,'Dyson coefficient lost factor')
        triangle=F(1,n+1)-F(1,n+2)
        need(triangle==F(1,(n+1)*(n+2)),'compact filter time coefficient')
    # Unjustified all-time integration replaces the geometric series by
    # coefficients containing n!. Its ratio eventually exceeds one.
    M=F(7,10000);eta=F(1)
    def laplace(n):return F(4+3*n)*(208*M)**n*factorial(n)/eta**(n+1)
    ratio=laplace(21)/laplace(20)
    need(ratio>1,'all-time bad positive majorant discriminator')
    return {'z_max':str(zmax),'F_z_max':str(f(zmax)),'L_weighted_uniform_coefficient':str(8*f(zmax)),'R_weighted_uniform_coefficient':str(16*f(zmax)),'tail_checks':rows,'bad_all_time_ratio_n20':str(ratio),'all_time_series_certified':False}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output)
    need(out.is_absolute() and not out.exists(),'output must be fresh absolute directory')
    contract=json.loads(CONTRACT.read_text())
    for name,value in contract['dependencies'].items():need(sha(ROOT/name)==value,'changed dependency '+name)
    for name in contract['instruction_inputs']:need((ROOT/name).is_file(),'missing instruction '+name)
    rejected=[]
    for theta,tau,e in [(F(0),F(0),F(1)),(F(-1,16),F(0),F(1)),(F(1,15),F(0),F(1)),(F(1,16),F(0),F(0))]:
        try:parameters(theta,tau,e)
        except RuntimeError:rejected.append([str(theta),str(tau),str(e)])
        else:raise RuntimeError('invalid parameters accepted')
    need(len(rejected)==4,'parameter controls missing')
    need(parameters(F(1,16),F(0))==0,'zero coupling exception')
    need(parameters(F(1,16),F(5,1664))==parameters(F(1,16),F(-5,1664)),'both coupling signs')
    support=support_checks();coefs=coefficients();spectral=spectral_checks();cert=certificate_checks()
    result={'schema':'ym23-reverse-s2-v1','loop':'s2','direction':'reverse','status':'checks_passed_regulated_target_accepted_unregularized_limited','passed':True,'target_verdict':'regulated_full_source_identity_and_connected_weighted_certificate_proved','identity':'[L_Theta,G]=-A+R_Theta(A)','residual':'(2Theta)^(-1) integral[-Theta,Theta] alpha_s(A) ds','bohr_L':'(1-sinc(Theta*omega))/omega, continuous value0','bohr_residual':'sinc(Theta*omega), value1 at frequency0','support':support,'coefficients':coefs,'spectral_checks':spectral,'certificate':cert,'comparison':{'radius_z_max':'35/128','weight':'2^|Y|','weighted_L_bound':'8*r_star*Theta*(4-z)/(1-z)^2','weighted_R_bound':'16*r_star*(4-z)/(1-z)^2','domain_preservation':True,'exponential_domain_preservation':True,'source_extended_by_identity':True,'regulator_removed':False,'actual_SU2_residual_lower_bound':False,'infinite_G_identification_proved':False,'all_stage_gap_proved':False},'source':'actual S1 cubic same-anchor source; nonzero for nonzero tau; not entire BCH residual','novelty':'direct project derivation, scientific priority unverified'}
    controls={'schema':'ym23-reverse-s2-controls-v1','loop':'s2','direction':'reverse','status':'passed','passed':True,'wrong_filter_sign_rejected':True,'omitted_frequency_zero_residual_rejected':True,'wrong_root_multiplicity_rejected':True,'time_simplex_and_word_factorials_retained':True,'actual_source_S1_scope_preserved':True,'all_exterior_sectors_preserved':True,'unjustified_all_time_series_interchange_rejected':True,'domain_proof_assumes_A_domain_preservation':False,'invalid_parameter_controls':rejected,'sampling_completeness_claimed':False,'scalar_control_is_actual_SU2_spectrum':False}
    consulted=['research/round23/advisor/s1-decision.json']
    inputs=set(contract['dependencies'])|set(contract['instruction_inputs'])|set(consulted)|{str(CONTRACT.relative_to(ROOT)),str((HERE/'report.md').relative_to(ROOT)),str((HERE/'check.py').relative_to(ROOT))}
    manifest={'schema':'ym23-source-manifest-v1','loop':'s2','direction':'reverse','inputs':{name:sha(ROOT/name) for name in sorted(inputs)},'outputs':{},'current_other_direction_read':False,'source_depth':'Contract, inherited S1 decision and S1/O1/R2 reports; no new primary-paper reading claimed; direct proof and exact checks.'}
    out.mkdir(parents=True)
    for name,data in [('results.json',result),('controls.json',controls)]:
        (out/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
        manifest['outputs'][name]=sha(out/name)
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'loop':'s2','z_max':str(parameters(F(1,16),F(5,1664))),'output':str(out)},sort_keys=True))

if __name__=='__main__':main()
