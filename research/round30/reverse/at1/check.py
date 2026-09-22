#!/usr/bin/env python3
"""Exact AT1 reverse controls; the analytic proof is report.md, not fixtures."""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = []

def must(name, condition, **values):
    if any(c['id'] == name for c in CHECKS):
        raise ValueError('duplicate check ID: ' + name)
    if not condition:
        raise ValueError('failed check: ' + name + ' ' + repr(values))
    CHECKS.append({'id': name, 'passed': True, 'values': values})

def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    if isinstance(x, dict):
        return {str(k): encode(v) for k,v in x.items()}
    return x

def dump(p, x):
    p.write_text(json.dumps(encode(x), indent=2, sort_keys=True) + '\n')

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def add(a,b):
    return tuple(x+y for x,y in zip(a,b))

def sub(a,b):
    return tuple(x-y for x,y in zip(a,b))

def qm(a,b):
    w,x,y,z=a; v,p,q,r=b
    return (w*v-x*p-y*q-z*r,w*p+x*v+y*r-z*q,w*q-x*r+y*v+z*p,w*r+x*q-y*p+z*v)

def qc(a):
    return (a[0],-a[1],-a[2],-a[3])

def scale(q,c):
    return tuple(c*x for x in q)

def qproduct(qs):
    z=(F(1),F(0),F(0),F(0))
    for q in qs:
        z=qm(z,q)
    return z

def mm(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def msub(a,b):
    return [[a[i][j]-b[i][j] for j in range(2)] for i in range(2)]

def comm(a,b):
    return msub(mm(a,b),mm(b,a))

def moment(atoms,k):
    return sum((weight*energy**k for energy,weight in atoms),F(0))

def theta(energy,L):
    return max(F(0),min(F(1),2-energy/L))

def controls():
    zero=(0,0,0); axes=((1,0,0),(0,1,0),(0,0,1)); S=(zero,)+axes
    R={zero,axes[2]}
    links=[]
    for b in sorted(R):
        for r,s in itertools.product(range(4),range(2)):
            tail=(4*b[0]+r,2*b[1]+s,b[2])
            links.extend((tail,d) for d in range(3))
    endpoints={p for tail,d in links for p in (tail,add(tail,axes[d]))}
    anchors={sub(b,s) for b in R for s in S}
    orthant={b for b in anchors if min(b)>=0}
    must('complete-factor-links', len(links)==48 and len(set(links))==48, links=links)
    must('complete-original-endpoints',len(endpoints)==36,endpoints=sorted(endpoints))
    expected={zero,(-1,0,0),(0,-1,0),(0,0,-1),(0,0,1),(-1,0,1),(0,-1,1)}
    must('seven-bulk-stars',anchors==expected,anchors=sorted(anchors))
    must('two-star-boundary-substitution',len(orthant)==2 and 2*7*len(anchors)!=2*7*len(orthant),bulk_reset=2*7*len(anchors),wrong_orthant_reset=2*7*len(orthant))
    wilson_stored=[(zero,0),((1,0,0),2),((0,0,1),0),(zero,2)]
    owners=[(p[0]//4,p[1]//2,p[2]) for p,d in wilson_stored]
    must('stored-link-ownership',owners==[zero,zero,(0,0,1),zero] and set(wilson_stored)<=set(links),owners=owners)
    must('negative-coordinate-owner',(-1//4,-1//2,-1)==(-1,-1,-1),remainders=((-1)%4,(-1)%2))
    # Centered box restrictions retain all seven once radius >= 2.
    for n in (1,2,3):
        retained={b for b in anchors if all(all(-n<=x<=n for x in add(b,s)) for s in S)}
        must('centered-box-incidence-'+str(n),len(retained)<=7 and (n<2 or retained==anchors),retained=sorted(retained))
    cap=F(1,100000000); reset=F(2*7*len(anchors)); selected_budget=F(1,2)+F(1,8)+F(1,2)
    kinetic0=2*selected_budget; kinetic_slope=reset/8
    b0=18+8*kinetic0; bslope=8*kinetic_slope
    must('physical-kinetic-reconstruction',kinetic0==F(9,4) and kinetic_slope==F(49,4),constant=kinetic0,tau_coefficient=kinetic_slope)
    must('second-moment-seven-star-coefficient',b0==36 and bslope==98,constant=b0,tau_coefficient=bslope)
    for t in (-cap,F(0),cap):
        b2=b0+bslope*abs(t)
        must('both-sign-bound-'+str(t),b2<37,b2_over_alpha_squared=b2)
    # Actual allowed one-face variational trial, not arbitrary assigned booleans.
    lam=F(1,2); trial=lam/3; haar_second=F(1,4)
    numerator=3*trial**2/4-lam*trial/2; norm=1+trial**2*haar_second
    must('selected-reference-is-not-pure-electric',numerator/norm<0,numerator=numerator,norm_squared=norm,trial_energy=numerator/norm,haar_energy=0)
    # Rational noncommuting unit quaternions; exact original/inverse occurrences.
    qs=[(F(3,5),F(4,5),F(0),F(0)),(F(5,13),F(0),F(12,13),F(0)),(F(8,17),F(0),F(0),F(15,17)),(F(7,25),F(24,25),F(0),F(0))]
    for i,q in enumerate(qs):
        must('unit-quaternion-'+str(i),sum(x*x for x in q)==1,q=q)
    must('noncommuting-quaternions',qm(qs[0],qs[1])!=qm(qs[1],qs[0]))
    factors=[qs[0],qs[1],qc(qs[2]),qc(qs[3])]; w=qproduct(factors)[0]
    deriv=[]; second=[]
    for i,q in enumerate(qs):
        derivatives=[]; second_derivatives=[]
        for axis in range(3):
            gen=tuple(F(1,2) if j==axis+1 else F(0) for j in range(4))
            dq=qm(gen,q) if i<2 else scale(qm(qc(q),gen),-1)
            ddq=scale(factors[i],F(-1,4))
            fs=factors.copy();fs[i]=dq;derivatives.append(qproduct(fs)[0])
            fs=factors.copy();fs[i]=ddq;second_derivatives.append(qproduct(fs)[0])
        deriv.extend(derivatives);second.extend(second_derivatives)
        must('per-link-gradient-'+str(i),sum(x*x for x in derivatives)==(1-w*w)/4,derivatives=derivatives)
        must('per-link-casimir-'+str(i),-sum(second_derivatives)==F(3,4)*w,casimir=-sum(second_derivatives))
    gamma=sum(x*x for x in deriv); qw=-sum(second)
    must('four-link-gradient-identity',gamma==1-w*w,gamma=gamma,w=w)
    must('four-link-casimir-identity',qw==3*w,qw=qw)
    qw2=2*w*qw-2*gamma; actual_comm=qw2-w*qw; missing_cross=3*w*w
    must('missing-gradient-cross-term',qw2==8*w*w-2 and actual_comm==5*w*w-2 and actual_comm!=missing_cross,actual=actual_comm,missing_cross=missing_cross)
    u=qs[2]; g=(F(0),F(1,2),F(0),F(0)); du=qm(g,u); invder=scale(qm(qc(u),g),-1)
    dproduct=add(qm(du,qc(u)),qm(u,invder)); wrong=add(qm(du,qc(u)),qm(u,scale(invder,-1)))
    must('inverse-sign-square-blind-control',sum(x*x for x in invder)==sum(x*x for x in scale(invder,-1)),classification='nondiscriminating alone; next test discriminates')
    must('inverse-sign-identity-derivative',dproduct==(0,0,0,0) and wrong!=(0,0,0,0),correct=dproduct,wrong=wrong)
    # Finite energy and commutator fixtures. Algebraic controls, not AQ simulations.
    for alpha in (F(1,3),F(1),F(5)):
        v=F(1,4); mu1=3*alpha*v; mu2=9*alpha**2*v
        must('free-corner-energy-'+str(alpha),mu1==alpha*(1-v) and mu2==9*alpha**2/4,mu1=mu1,mu2=mu2)
    wrong_generator_mu2=F(1,4)*(12**2);correct_mu2=F(9,4)
    must('wrong-energy-or-generator-normalization',wrong_generator_mu2==16*correct_mu2 and wrong_generator_mu2!=correct_mu2,wrong=wrong_generator_mu2,correct=correct_mu2)
    K=[[F(0),F(0)],[F(0),F(3)]]; W=[[F(0),F(1,2)],[F(1,2),F(0)]]
    mu1=mm(mm(W,K),W)[0][0]; double=comm(W,comm(K,W))[0][0]
    raw=[[F(7),F(0)],[F(0),F(10)]]; raw_mu=mm(mm(W,raw),W)[0][0]
    must('double-commutator-half-factor',double/2==mu1 and double!=mu1,double=double,first_moment=mu1)
    must('actual-ground-energy-subtraction',raw_mu!=mu1 and comm(W,comm(raw,W))[0][0]==double,raw_moment=raw_mu,centered_moment=mu1)
    alpha=F(24);delta=alpha/8;hbar=F(2);normalized=F(2)
    must('physical-energy-frequency-clock',delta*normalized==6 and delta*normalized/hbar==3 and delta*normalized!=normalized,energy=delta*normalized,frequency=delta*normalized/hbar)
    Wc=[[F(1,2),F(1,2)],[F(1,2),F(1,2)]]; mean=Wc[0][0]; full_mass=mm(Wc,Wc)[0][0];v=full_mass-mean**2
    must('uncentered-vacuum-contamination',full_mass==F(1,2) and v==F(1,4) and full_mass-v==mean**2,uncentered_mass=full_mass,centered_mass=v,zero_energy_mass=mean**2)
    gap=F(1,16);family_a=[];family_b=[]
    for n in (2,4,16,256):
        a=[(gap,1-F(1,n)),(gap+F(n,2),F(1,n))]
        b=[(gap,1-F(1,n*n)),(gap+n,F(1,n*n))]
        a1=moment(a,1);a2=moment(a,2);b1=moment(b,1);b2=moment(b,2)
        must('bounded-first-moment-escaping-tail-'+str(n),a1==gap+F(1,2) and a2==gap*gap+gap+F(n,4),first=a1,second=a2,limit_first=gap)
        must('bounded-second-moment-with-unequal-limit-'+str(n),b1==gap+F(1,n) and b2==gap*gap+2*gap/n+1 and b2<=gap*gap+2*gap+1,first=b1,second=b2,limit_second=gap*gap)
        # Compact cutoff test at fixed L=1: high-energy contribution vanishes.
        L=F(1)
        for label,atoms,weight in [('first',a,F(1,n)),('second',b,F(1,n*n))]:
            compact=sum(wt*theta(e,L) for e,wt in atoms)
            must('compact-test-convergence-'+label+'-'+str(n),abs(compact-1)<=2*weight,value=compact,error=abs(compact-1))
            for L in (F(1,2),F(1),F(4)):
                tail=sum(wt*e for e,wt in atoms if e>L)
                upper=moment(atoms,2)/L
                f_int=sum(wt*e*theta(e,L) for e,wt in atoms)
                g_int=sum(wt*e*e*theta(e,L) for e,wt in atoms)
                must('uniform-tail-'+label+'-'+str(n)+'-'+str(L),0<=moment(atoms,1)-f_int<=tail<=upper and g_int<=moment(atoms,2),tail=tail,upper=upper,cutoff_first=f_int,cutoff_second=g_int)
        family_a.append({'n':n,'mu1':a1,'mu2':a2});family_b.append({'n':n,'mu1':b1,'mu2':b2})
    for e in (F(0),F(1,4),F(1),F(3),F(12)):
        vals=[e*theta(e,L) for L in (F(1,2),F(1),F(2),F(4),F(8),F(16))]
        must('monotone-energy-cutoffs-'+str(e),all(x<=y for x,y in zip(vals,vals[1:])) and vals[-1]==e,cutoffs=vals)
    # Two normalized pure state probability profiles, with K=g(I-Psi),
    # both have the same positive spectral gap and variance >1/5.
    p1=F(1,2);p2=F(3,5);mean1=p1-F(1,2);mean2=p2-F(1,2);var1=F(1,4)-mean1**2;var2=F(1,4)-mean2**2
    must('unproved-state-identification',mean1!=mean2 and min(var1,var2)>F(1,5) and gap*var1!=gap*var2,means=[mean1,mean2],variances=[var1,var2],gapped_first_moments=[gap*var1,gap*var2])
    return {'checks':CHECKS,'check_count':len(CHECKS),'coefficients':{'regional_reset':reset,'kinetic_constant':kinetic0,'kinetic_tau':kinetic_slope,'B2_constant':b0,'B2_tau':bslope,'B2_at_cap_over_alpha2':b0+bslope*cap},'escaping_first':family_a,'escaping_second':family_b,'claims':{'actual_aq_state':True,'second_moment_equality':False,'continuum_claim':False,'operator_domain_proved_in_report':True,'first_moment_equality_proved_in_report':True,'priority_verified':False},'scope':'Exact arithmetic/control fixtures support the report; finite sampling does not prove operator or thermodynamic theorems.'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    out=Path(args.output)
    if not out.is_absolute() or out.exists():
        raise ValueError('output must be a fresh absolute directory')
    for p in [out]+list(out.parents):
        if p.is_symlink():
            raise ValueError('symlink output path')
    inventory=json.loads((HERE/'inputs/source-inventory.json').read_text())
    expected=set(inventory)|{'source-inventory.json'}
    actual={str(p.relative_to(HERE/'inputs')) for p in (HERE/'inputs').rglob('*') if p.is_file()}
    if actual!=expected:
        raise ValueError('source inventory file set mismatch')
    for rel,h in inventory.items():
        p=HERE/'inputs'/rel
        if p.is_symlink() or any(q.is_symlink() for q in p.parents) or digest(p)!=h:
            raise ValueError('source binding mismatch: '+rel)
    contract=json.loads((HERE/'inputs/research/round30/contracts/at1.json').read_text())
    if contract['id']!='AT1' or contract['parameters']['tau']!='dimensionless omitted-interaction coupling, both signs |tau|<=1/100000000':
        raise ValueError('wrong contract or cap')
    result=controls();out.mkdir(parents=True)
    dump(out/'results.json',result)
    sources={str(p.relative_to(HERE)):digest(p) for p in sorted((HERE/'inputs').rglob('*')) if p.is_file()}
    sources.update({'check.py':digest(HERE/'check.py'),'report.md':digest(HERE/'report.md')})
    dump(out/'manifest.json',{'loop':'AT1','direction':'reverse','sources':sources,'outputs':{'results.json':digest(out/'results.json')}})
    print(json.dumps({'loop':'AT1','direction':'reverse','checks':len(CHECKS),'results_sha256':digest(out/'results.json')}))

if __name__=='__main__':
    main()
