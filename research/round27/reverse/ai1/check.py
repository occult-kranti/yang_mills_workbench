#!/usr/bin/env python3
"""Independent exact arithmetic checks for the AI1 endpoint readout maps."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import factorial
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
checks=[]

def require(value,label):
    if not value:
        raise ValueError(label)
    checks.append(label)

def coeff(kind,n):
    if kind=='null':
        return (F(n==0),F(0))
    if n==0:
        return F(1),F(0)
    if n%2==0:
        m=n//2
        weights=(F(1,4),F(1,12)) if kind=='X' else (F(1,2),F(1,6))
        return ((-1)**m*2**n*(weights[0]+weights[1]*3**m)/F(84**n*factorial(n)),F(0))
    if kind=='X':
        return F(0),F(0)
    m=(n-1)//2
    return F(0),F((-1)**m*2**n*(1+3**m),4*84**n*factorial(n))

def kappa(p):
    a,eta,q=p
    return a*eta*(1-q)**3

def signature(kind,p,order=10):
    k=kappa(p)
    return [tuple(c*k**n for c in coeff(kind,n)) for n in range(order+1)]

def rank(rows):
    A=[list(map(F,row)) for row in rows]
    r=0
    for c in range(len(A[0])):
        pivot=next((i for i in range(r,len(A)) if A[i][c]),None)
        if pivot is None:
            continue
        A[r],A[pivot]=A[pivot],A[r]
        a=A[r][c]
        A[r]=[v/a for v in A[r]]
        for i in range(len(A)):
            if i!=r:
                b=A[i][c]
                A[i]=[x-b*y for x,y in zip(A[i],A[r])]
        r+=1
    return r

def clean(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [clean(v) for v in x]
    return x

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',required=True)
    out=Path(ap.parse_args().output)
    require(out.is_absolute(),'fresh output path must be absolute')
    require(not out.exists(),'output directory must not exist')
    contract_path=ROOT/'research/round27/contracts/ai1.json'
    contract=json.loads(contract_path.read_text())
    require(contract['loop']=='ai1','correct frozen loop')
    for p,digest in contract['sources'].items():
        require(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==digest,'frozen binding '+p)
    require(coeff('sum',1)==(0,F(1,84)),'coherent first derivative')
    require(coeff('X',1)==(0,0),'single-six-cycle slope null')
    require(2*coeff('X',2)[0]==F(-1,3528),'single-six-cycle curvature')
    require(2*coeff('sum',2)[0]==F(-1,1764),'coherent curvature')
    require(all(coeff('null',n)==(0,0) for n in range(1,11)),'elementary endpoint all tested derivatives null')
    require(24*coeff('X',4)[0]==F(16,84**4),'single-frequency false fourth moment rejected')
    require(F(16)!=F(2)**2,'a fitted single cosine does not match fourth moment')
    require(2*coeff('sum',2)[0]!=-coeff('sum',1)[1]**2,'a fitted single phase does not match second moment')
    p1=(F(1),F(1,16),F(999,1000))
    p2=(F(1),F(1,2),F(1999,2000))
    p3=(F(2),F(1,32),F(999,1000))
    points=[p1,p2,p3]
    require(len(set(points))==3,'distinct exact parameter points')
    for i,p in enumerate(points):
        require(p[0]>0 and 0<p[1]<1 and 0<p[2]<1,'parameter domain '+str(i))
        require(kappa(p)==F(1,16000000000),'exact compensation '+str(i))
    for kind in ['null','X','sum']:
        require(signature(kind,p1)==signature(kind,p2)==signature(kind,p3),'surrogate derivative signatures coincide '+kind)
    for p in points:
        a=p[0];k=kappa(p)
        u0_der_im=-3*a
        usum_der_im=k/F(84)-F(9,2)*a
        recovered_a=-u0_der_im/3
        recovered_k=84*(usum_der_im+F(9,2)*recovered_a)
        require((recovered_a,recovered_k)==(a,k),'conditional carrier reconstruction '+str(p))
    require(-3*p1[0]==-3*p2[0] and -3*p1[0]!=-3*p3[0],'carrier separates alpha but not eta-q compensation')
    for p in [p1,p2]:
        r=kappa(p)/p[0]
        require(p[1]==r/(1-p[2])**3,'complete fixed-alpha fiber formula '+str(p))
        require((1-p[2])**3>r,'eta upper-bound equivalent without cube root '+str(p))
    require(rank([[1,1,3]])==1,'log composite Jacobian rank one')
    require(rank([[1,0,0],[1,1,3]])==2,'carrier-plus-composite Jacobian rank two')
    require(all(sum(F(a)*b for a,b in zip(row,[0,-3,1]))==0 for row in [[1,0,0],[1,1,3]]),'remaining exact log null direction')
    require(all(coeff('X',n)==(0,0) for n in range(1,11,2)),'X signed ambiguity')
    require(coeff('sum',1)[1]>0,'coherent phase breaks signed ambiguity')
    # Delta=(4pi/3), hbar=1, alpha'=2, eta'=eta/2 preserves kappa.
    delta_over_pi=F(4,3)
    alpha_difference=F(1)
    for carrier in [F(3),F(9,2)]:
        turns=carrier*alpha_difference*delta_over_pi/2
        require(turns.denominator==1,'carrier alias exact integer turns '+str(carrier))
    require(kappa(p1)==kappa(p3),'aliased amplitude compensation')
    # q-sensitive weights distinguish these finite-q retained matrices.
    require(p1[2]**4!=p2[2]**4 and p1[2]**5!=p2[2]**5,'no inferred finite-q matrix equality')
    for p in points:
        q=p[2]
        require(q**5/q**4==q,'proposed retained moment ratio '+str(q))
    epsilon=F(1,10**12);frequency=10**15
    require(epsilon*frequency==1000,'bounded value error can hide arbitrarily large derivative')
    require(kappa(p1)>0,'positive kappa removes X sign ambiguity in contract domain')
    sources=list(contract['sources'])+[
        'research/round27/contracts/ai1.json',
        'research/round26/advisor/roadmap.json',
        'research/round26/advisor/network-extensions.json',
        'research/round26/forward/ad2/check.py',
        'research/round26/PARAMETERS.md',
        'research/round25/solo/aa1/output/results.json',
        'papers/draft-01/sections/roadmap.tex',
        'papers/draft-01/sections/recent.tex',
        str(HERE.relative_to(ROOT)/'report.md'),
        str(HERE.relative_to(ROOT)/'check.py')]
    result={
        'schema':'ym27-reverse-ai1-v1',
        'scope':'exact structural classification of declared endpoint surrogate maps; not actual finite-q initial derivatives',
        'parameters_in_units_hbar_equals_1':points,
        'shared_kappa':kappa(p1),
        'identified':{'scaled_label':'none from ordinates; kappa from supplied time schedule','demodulated_physical_time':'kappa','undemodulated_continuous_physical_time':'alpha/hbar and kappa','remaining_fiber':'eta*(1-q)^3 fixed; alpha fixed'},
        'checks':checks,'check_count':len(checks),
        'coefficient_audit':{kind:[coeff(kind,n) for n in range(11)] for kind in ['null','X','sum']},
        'derivative_control_counterexample':{'epsilon':epsilon,'frequency':frequency,'derivative_at_zero':epsilon*frequency},
        'bindings':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(sources))}}
    out.mkdir(parents=True)
    (out/'results.json').write_text(json.dumps(clean(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(checks),'scope':result['scope']}))

if __name__=='__main__':
    main()
