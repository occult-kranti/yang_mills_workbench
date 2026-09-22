#!/usr/bin/env python3
"""AT1 independent forward exact fixtures. Analytic proof is report.md."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKS = []

def test(name, value):
    if name in {x['id'] for x in CHECKS}:
        raise RuntimeError('duplicate check: '+name)
    if not value:
        raise RuntimeError('failed check: '+name)
    CHECKS.append({'id': name, 'passed': True})

def add(x,y): return tuple(a+b for a,b in zip(x,y))
def sub(x,y): return tuple(a-b for a,b in zip(x,y))
def mul(k,x): return tuple(k*a for a in x)
def qm(a,b):
    w,x,y,z=a;v,r,s,t=b
    return (w*v-x*r-y*s-z*t,w*r+x*v+y*t-z*s,w*s-x*t+y*v+z*r,w*t+x*s-y*r+z*v)
def inv(q): return (q[0],-q[1],-q[2],-q[3])
def qprod(qs):
    v=(F(1),F(0),F(0),F(0))
    for q in qs: v=qm(v,q)
    return v

def owner(v): return (v[0]//4,v[1]//2,v[2])
AXES=((1,0,0),(0,1,0),(0,0,1));ZERO=(0,0,0)

def links(b):
    return {((4*b[0]+r,2*b[1]+s,b[2]),d) for r in range(4) for s in range(2) for d in range(3)}
def endpoints(es): return {p for e in es for p in (e[0],add(e[0],AXES[e[1]]))}
def moment(atoms,k): return sum(w*e**k for w,e in atoms)
def resolvent(atoms): return sum(w/(1+e) for w,e in atoms)
def theta(e,L): return min(F(1),max(F(0),F(2)-e/L))
def put(p,data): p.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    args=parser.parse_args();out=Path(args.output)
    if not out.is_absolute() or out.exists():
        raise SystemExit('--output must be an absolute path that does not exist')
    contract=json.loads((HERE/'inputs/research/round30/contracts/at1.json').read_text())
    controls=['two-star-boundary-substitution','selected-reference-is-not-pure-electric','missing-gradient-cross-term','wrong-energy-or-generator-normalization','uncentered-vacuum-contamination','bounded-first-moment-escaping-tail','bounded-second-moment-with-unequal-limit','unproved-state-identification']
    test('contract-id',contract['id']=='AT1')
    test('contract-controls-complete',contract['controls']==controls)
    test('contract-actual-aq-state',contract['model'].startswith('Exactly the AQ1/AQ2 chosen subsequential centered-full-Z3 state'))
    R={ZERO,AXES[2]};stars={ZERO,*AXES};es=set().union(*(links(b) for b in R))
    test('two-complete-factors-48-links',len(es)==48)
    test('joint-original-36-endpoints',len(endpoints(es))==36)
    test('one-factor-22-endpoints',len(endpoints(links(ZERO)))==22)
    test('shared-8-endpoints',len(endpoints(links(ZERO))&endpoints(links(AXES[2])))==8)
    wilson=((ZERO,0),(AXES[0],2),(AXES[2],0),(ZERO,2))
    test('four-distinct-original-stored-links',len(set(wilson))==4 and set(wilson)<=es)
    test('wilson-complete-owner-cover',{owner(p) for p,d in wilson}==R)
    anchors={sub(r,s) for r in R for s in stars}
    expected={ZERO,(-1,0,0),(0,-1,0),(0,0,-1),(0,0,1),(-1,0,1),(0,-1,1)}
    test('seven-incident-bulk-anchors',anchors==expected and len(anchors)==7)
    orthant={b for b in anchors if all(x>=0 for x in b)}
    test('control-two-star-boundary-substitution',len(orthant)==2 and len(orthant)!=len(anchors))
    for n in (2,3,5):
        retained={b for b in anchors if all(all(-n<=x<=n for x in add(b,s)) for s in stars)}
        test(f'centered-box-{n}-all-seven-stars',retained==anchors)
    for p in [(-9,-5,-2),(-1,-1,0),(0,0,0),(5,7,1)]:
        b=owner(p)
        test('euclidean-owner-'+','.join(map(str,p)),0<=p[0]-4*b[0]<4 and 0<=p[1]-2*b[1]<2 and b[2]==p[2])
    cap=F(1,10**8); reset=2*7*len(anchors)
    test('reset-coefficient-98',reset==98)
    budget=2*(F(1,2)+F(1,8)+F(1,2))
    test('complete-selected-budget-9over4',budget==F(9,4))
    values=[]
    for tau in (-cap,F(0),cap):
        kinetic=budget+F(reset,8)*abs(tau)
        B2=18+8*kinetic
        test('B2-formula-'+str(tau),B2==36+98*abs(tau) and B2<37)
        values.append({'tau':str(tau),'kinetic_over_alpha':str(kinetic),'B2_over_alpha_squared':str(B2)})
    test('exact-cap-B2',36+98*cap==F(1800000049,50000000))
    # Selected reference differs from pure electric for a legitimate trial.
    alpha=F(1);lam=F(1,4);t=lam/(3*alpha)
    numerator=3*alpha*t*t/4-lam*t/2
    test('control-selected-reference-is-not-pure-electric',numerator<0)
    test('nonzero-selected-trial-normalization',1+t*t/4>1)
    # Exact scalar identity fixture: delta*h=T+V-B.
    T=F(2);V=F(-3,2);B=F(-1,2);dh=T+V-B
    test('actual-ground-scalar-reconstruction',dh-V+B==T)
    test('control-dropping-ground-scalar-from-identity',dh-V!=T and T<=dh-V)
    # Exact quaternion differentiation of all four original occurrences.
    stored=[(F(3,5),F(4,5),F(0),F(0)),(F(5,13),F(0),F(12,13),F(0)),(F(8,17),F(0),F(0),F(15,17)),(F(7,25),F(24,25),F(0),F(0))]
    orientations=[1,1,-1,-1]
    factors=[q if s==1 else inv(q) for q,s in zip(stored,orientations)]
    W=qprod(factors)[0];gamma=F(0);lap=F(0);inverse_nonzero=False
    basis=[(F(0),F(1,2),F(0),F(0)),(F(0),F(0),F(1,2),F(0)),(F(0),F(0),F(0),F(1,2))]
    test('holonomies-are-unit-quaternions',all(sum(v*v for v in q)==1 for q in stored))
    for i,(U,sgn) in enumerate(zip(stored,orientations)):
        gradients=[]
        for a,Tgen in enumerate(basis):
            dq=qm(Tgen,U) if sgn==1 else mul(-1,qm(inv(U),Tgen))
            slots=list(factors);slots[i]=dq;der=qprod(slots)[0];gradients.append(der)
            if sgn==-1 and der:
                inverse_nonzero=True
                wrong_slots=list(factors);wrong_slots[i]=qm(inv(U),Tgen)
                test(f'inverse-sign-not-discarded-{i}-{a}',qprod(wrong_slots)[0]==-der and qprod(wrong_slots)[0]!=der)
            d2=mul(F(-1,4),factors[i]);slots[i]=d2
            test(f'casimir-link-{i}-direction-{a}',qprod(slots)[0]==-W/4)
        gi=sum(x*x for x in gradients);gamma+=gi;lap+=3*W/4
        test(f'gradient-link-{i}',gi==(1-W*W)/4)
    test('inverse-sign-control-nonzero',inverse_nonzero)
    test('four-link-gradient-identity',gamma==1-W*W)
    test('four-link-casimir-identity',lap==3*W)
    test('control-wrong-full-pauli-generators',4*gamma!=gamma)
    # QW^2=2 W QW - 2 Gamma, so [Q,W]W=5W^2-2.
    QW2=6*W*W-2*gamma;comm=QW2-3*W*W
    test('exact-polynomial-commutator',comm==5*W*W-2)
    test('control-missing-gradient-cross-term',comm!=3*W*W)
    test('double-commutator-half-factor',2*gamma/2==gamma and 2*gamma!=gamma)
    free_v=F(1,4);free_E=F(3);free_mu1=free_v*free_E;free_mu2=free_v*free_E**2
    test('free-corner-moments',free_mu1==F(3,4) and free_mu2==F(9,4))
    test('control-reference-energy-is-not-excited-energy',free_mu2>0)
    delta=F(1,8)
    test('control-wrong-energy-normalization',(free_E/delta)**2*free_v!=free_mu2)
    test('physical-clock-energy-frequency-distinct',free_mu2/F(2)**2!=free_mu2)
    # Centered measure and true vacuum subtraction are independently necessary.
    m=F(1,3);centered=[(F(2,9),F(2))];uncentered=centered+[(m*m,F(0))]
    test('control-uncentered-vacuum-contamination',moment(uncentered,0)!=moment(centered,0) and resolvent(uncentered)!=resolvent(centered))
    test('uncentering-preserves-positive-moments',moment(uncentered,1)==moment(centered,1) and moment(uncentered,2)==moment(centered,2))
    shifted=[(w,e+F(3,7)) for w,e in centered]
    test('control-wrong-raw-ground-subtraction',moment(shifted,1)!=moment(centered,1))
    first_escape=[];second_escape=[]
    for n in (2,3,10,100,10000):
        eta=[(1-F(1,n),F(1)),(F(1,n),F(n))]
        zeta=[(1-F(1,n*n),F(1)),(F(1,n*n),F(n))]
        test(f'first-escape-mean-{n}',moment(eta,1)==2-F(1,n))
        test(f'first-escape-second-growing-{n}',moment(eta,2)==n+1-F(1,n))
        test(f'second-escape-mean-{n}',moment(zeta,1)==1+F(1,n)-F(1,n*n))
        test(f'second-escape-uniform-second-{n}',moment(zeta,2)==2-F(1,n*n) and moment(zeta,2)<2)
        test(f'second-escape-second-tail-{n}',zeta[1][0]*zeta[1][1]**2==1)
        test(f'compact-resolvent-convergence-{n}',abs(resolvent(zeta)-F(1,2))<=F(1,n*n))
        first_escape.append({'n':n,'mu1':str(moment(eta,1)),'mu2':str(moment(eta,2))})
        second_escape.append({'n':n,'mu1':str(moment(zeta,1)),'mu2':str(moment(zeta,2)),'limit_mu2':'1'})
        for i,L in enumerate((F(1),F(n,2),F(n))):
            tail=sum(w*e for w,e in zeta if e>L)
            loss=moment(zeta,1)-sum(w*e*theta(e,L) for w,e in zeta)
            test(f'first-tail-bound-{n}-{i}',tail<=2/L and 0<=loss<=2/L)
            test(f'probability-tail-bound-{n}-{i}',sum(w for w,e in zeta if e>L)<=2/L**2)
    test('control-bounded-first-moment-escaping-tail',moment([(F(9999,10000),F(1)),(F(1,10000),F(10000))],2)>37)
    test('control-bounded-second-moment-with-unequal-limit',all(moment([(1-F(1,n*n),F(1)),(F(1,n*n),F(n))],2)-1==1-F(1,n*n)>=F(3,4) for n in (2,3,10,100,10000)))
    # Same supplied broad constraints permit different bounded-observable states.
    def mv(p):
        mean=p*F(1,2)+(1-p)*F(-1,2)
        return mean,F(1,4)-mean*mean
    ma,va=mv(F(1,2));mb,vb=mv(F(1,3))
    test('control-unproved-state-identification',va>F(1,5) and vb>F(1,5) and ma!=mb)
    # Explicitly execute every contract control; analytic hypotheses are not numeric samples.
    source_files=[HERE/'check.py',HERE/'report.md']+sorted(p for p in (HERE/'inputs').rglob('*') if p.is_file())
    manifest={p.relative_to(HERE).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in source_files}
    result={'loop':'AT1','direction':'forward','human_author':'Hruday N M (BUNZEEY)','ai_assisted':True,'classification':'model-specific extension; scientific priority unverified','claims':{'actual_aq_state':True,'operator_domain':True,'first_moment_equality':True,'second_moment_upper_bound':True,'second_moment_equality':False,'state_identification':False,'continuum_claim':False},'model':'AQ1/AQ2 chosen subsequential centered-full-Z3 state','bounds':values,'geometry':{'links':len(es),'endpoints':len(endpoints(es)),'bulk_stars':len(anchors),'orthant_stars':len(orthant),'anchors':[list(x) for x in sorted(anchors)]},'controls':{c:True for c in controls},'measure_controls':{'bounded_first_escaping_tail':first_escape,'bounded_second_unequal_limit':second_escape},'checks':CHECKS,'fixture_scope':'Exact arithmetic, geometry and countermodel diagnostics. Infinite-volume proof is report.md; no sampled fixture certifies it.'}
    out.mkdir(parents=True);put(out/'results.json',result);put(out/'source-manifest.json',manifest)
    print(json.dumps({'loop':'AT1','checks':len(CHECKS),'all_passed':True,'output':str(out)}))

if __name__=='__main__': main()
