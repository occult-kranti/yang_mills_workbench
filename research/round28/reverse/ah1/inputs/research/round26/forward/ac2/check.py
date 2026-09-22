#!/usr/bin/env python3
"""Independently reconstruct AC1 sparse metric and certify state-sensitive error."""
import argparse,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise ValueError(m)
def faces():
    vs=list(itertools.product(range(3),range(3),range(2)));lookup={}
    for v in vs:
        for a,n in enumerate((3,3,2)):
            if v[a]+1<n:
                w=tuple(v[j]+(j==a) for j in range(3));lookup[frozenset((v,w))]=len(lookup)
    masks=[]
    for v in vs:
        for a,b in itertools.combinations(range(3),2):
            if v[a]+1<(3,3,2)[a] and v[b]+1<(3,3,2)[b]:
                walk=[v,tuple(v[j]+(j==a) for j in range(3)),tuple(v[j]+(j in (a,b)) for j in range(3)),tuple(v[j]+(j==b) for j in range(3))]
                masks.append(sum(1<<lookup[frozenset((walk[j],walk[(j+1)%4]))] for j in range(4)))
    return masks
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);require(not out.exists(),'fresh output')
    source=json.loads((ROOT/'research/round26/forward/ac1/output/results.json').read_text());basis=source['basis'];require(len(basis)==293,'basis dimension')
    labels={b['label']:i for i,b in enumerate(basis)};norms=[F(b['norm2']) for b in basis];expected={};fs=faces()
    def entry(label,p,coef):
        i=labels[label];j=labels['face_'+str(p)];expected[i,j]=F(coef);expected[j,i]=F(coef)*norms[i]
    for p in range(20):entry('vacuum',p,F(1,2));entry('spin1_'+str(p),p,F(1,2))
    for p,q in itertools.combinations(range(20),2):
        shared=bool(fs[p]&fs[q]);kinds=('singlet','triplet') if shared else ('pair',)
        for kind in kinds:
            label=f'{kind}_{p}_{q}';idx=labels[label]
            require(norms[idx]==(3 if kind=='triplet' else 1),'branch metric')
            require(F(basis[idx]['energy'])==({'singlet':F(9,2),'triplet':F(13,2),'pair':F(6)}[kind]),'complete K eigenvalue')
            for face in (p,q):entry(label,face,F(1,4) if shared else F(1,2))
    actual={(i,j):F(v) for i,j,v in source['magnetic_sparse_entries']};require(expected==actual and len(actual)==1088,'independent complete sparse reconstruction')
    gram=[]
    for p in range(20):
        row=[]
        for q in range(20):
            val=sum((norms[i]*actual.get((i,p+1),F(0))*actual.get((i,q+1),F(0)) for i in range(21,293)),F(0))
            require(val==(5 if p==q else F(1,4)),'all-input old-to-new Gram');row.append(str(val))
        gram.append(row)
    require(all(actual.get((i,0),0)==0 for i in range(21,293)),'vacuum new-loading cancellation')
    require(all(not(i>=21 and j>=21) for i,j in actual),'complete new-to-new magnetic zero block')
    L=F(1,100);g=3-20*L;r21=F(7,3)*L*L;p21=r21/g;rplus=20*L*p21;pplus=rplus/g;delta=rplus*rplus/g;d=F(9,2);t=F(13,5);eta=F(1,100);qplus=F(3,4)*L+F(3,2)*p21;b=qplus+eta;den=1-F(5,9)*L*L-eta-p21;coupling=F(25,8)*L
    require(F(25,8)**2>F(39,4),'continuous radical upper bound')
    exp_lower=sum(((g*t)**n/F(math.factorial(n)) for n in range(48)),F(0));require(exp_lower>1400,'positive exponential enclosure')
    early=delta*t+20*L*coupling*(qplus*t/d+b/(g*d));late=pplus+(2*b+pplus)/1400;relative=max(early,late)/den
    require((den,early,late,relative)==(F(7127,7200),F(457097,12600000000),F(2441,78400000),F(457097,12472250000)),'reported exact certificate')
    require(relative<F(37,10**6),'improved all-time bound')
    require(relative<F(44,100000),'improvement over inherited class bound')
    contract=json.loads((ROOT/'research/round26/contracts/ac2.json').read_text());paths=['research/round26/contracts/ac2.json',*contract['bindings'],str(HERE.relative_to(ROOT)/'report.md'),str(HERE.relative_to(ROOT)/'check.py')]
    bindings={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(paths))}
    for p,digest in contract['bindings'].items():require(bindings[p]==digest,'dependency binding '+p)
    result={'schema':'ym26-forward-ac2-v1','matrix_reconstruction':'all 1088 entries and all zeros agree in full metric','old_to_new_gram':gram,'gram_eigenvalues':{'bright':'39/4','dark':'19/4'},'certificate':{k:str(v) for k,v in {'lambda_cap':L,'eta':eta,'join_time':t,'denominator':den,'early_absolute':early,'late_absolute':late,'relative':relative}.items()},'controls':{'new_channel_envelope_retained':True,'new_input_ball_not_admitted':True,'lambda_zero_exact':True,'time_zero_exact':True,'distinct_ground_centers_charged':True,'no_sampled_uniformity':True,'arithmetic_error_of_rational_bound':0,'matrix_exponential_not_evaluated':True},'bindings':bindings}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
