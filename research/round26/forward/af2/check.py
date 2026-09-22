#!/usr/bin/env python3
"""All-time piecewise evaluator for the actual fixed-coupling293 heat matrix."""
import argparse,hashlib,itertools,json,math
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise ValueError(m)
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    return x
def nearest(x,D):
    n,r=divmod(x.numerator*D,x.denominator);return n+int(2*r>=x.denominator)
def sqrt_upper(x,D=10**40):
    a=isqrt(x.numerator*D*D//x.denominator);r=F(a,D);return r if r*r==x else F(a+1,D)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);require(not out.exists(),'fresh output')
    src=json.loads((ROOT/'research/round26/forward/ac1/output/results.json').read_text());af1=json.loads((ROOT/'research/round26/forward/af1/output/results.json').read_text());basis=src['basis'];n=len(basis);require(n==293,'actual dimension');G=[F(b['norm2']) for b in basis];K=[F(b['energy']) for b in basis];S={(i,j):F(a) for i,j,a in src['magnetic_sparse_entries']};labels={b['label']:i for i,b in enumerate(basis)};expected={}
    def edge(label,p,a):
        i=labels[label];j=labels['face_'+str(p)];expected[i,j]=a;expected[j,i]=a*G[i]
    for p in range(20):edge('vacuum',p,F(1,2));edge('spin1_'+str(p),p,F(1,2))
    for label in labels:
        ps=label.split('_')
        if ps[0] in ('pair','singlet','triplet'):
            kind,p,q=ps[0],int(ps[1]),int(ps[2]);require(G[labels[label]]==(3 if kind=='triplet' else 1),'actual branch Gram')
            for face in (p,q):edge(label,face,F(1,2) if kind=='pair' else F(1,4))
    require(S==expected and len(S)==1088,'every actual sparse entry');require(all(G[i]*a==G[j]*S[j,i] for (i,j),a in S.items()),'metric self-adjointness')
    lam=F(1,100);c=F(1,5);diag=[e+c for e in K]
    def Smul(v):
        w=[F(0)]*n
        for (i,j),a in S.items():w[i]+=a*v[j]
        return w
    def Amul(v):
        w=Smul(v);return [diag[i]*v[i]-lam*w[i] for i in range(n)]
    def dot(v,w):return sum((G[i]*v[i]*w[i] for i in range(n)),F(0))
    # Certify an actual rational ground-projector vector, never assume iteration convergence.
    v=[F(0)]*n;v[0]=1
    for p in range(20):v[p+1]=lam/6
    sv=Smul(v)
    for i in range(21,n):v[i]=lam*sv[i]/K[i]
    iterations=[];trialD=10**30
    for unused in range(3):
        av=Amul(v);a=dot(v,av)/dot(v,v);sv=Smul(v)
        v=[F(1)]+[F(nearest(lam*sv[i]/(diag[i]-a),trialD),trialD) for i in range(1,n)]
        av=Amul(v);norm2=dot(v,v);a=dot(v,av)/norm2;res2=dot(av,av)/norm2-a*a
        require(0<a<F(1,5) and res2>=0,'actual trial spectral hypotheses');iterations.append({'rayleigh':a,'residual_squared':res2})
    projector_error=sqrt_upper(res2)/(3-a);require(projector_error<F(1,10**11),'actual ground-projector certificate')
    muhat=F(af1['center']['rounded_center']);urad=F(af1['center']['center_radius']);require(urad<F(1,10**11),'inherited own-ground enclosure')
    HD=10**24;hdiag=[int((d-muhat)*HD) for d in diag];hoff={(i,j):int(-lam*a*HD) for (i,j),a in S.items()};require(all(F(hdiag[i],HD)==diag[i]-muhat for i in range(n)),'rounded-center matrix exactness');require(all(F(a,HD)==-lam*S[i,j] for (i,j),a in hoff.items()),'offdiagonal matrix exactness')
    degree=256;exportD=10**40;rounding=F(15,exportD);require(2*sum(G)<30**2,'complex coordinate rounding metric')
    early_poly=F(2*72**257,math.factorial(257));early_center=8*urad/(1-8*urad);early_error=early_poly+early_center+rounding
    require(early_poly<F(1,10**25),'continuous early polynomial bound')
    exponent=F(112,5);partial=sum((exponent**j/F(math.factorial(j)) for j in range(128)),F(0));require(partial>5*10**9,'late complete spectral tail')
    late_tail=F(1,5*10**9);late_error=projector_error+late_tail+rounding;numerical=max(early_error,late_error);require(numerical<F(1,10**8),'uniform numerical allowance stricter than contract')
    def validate(inp):
        den=inp['denominator'];re=[F(a,den) for a in inp['real']];im=[F(a,den) for a in inp['imag']]
        require(all(re[i]==im[i]==0 for i in range(21,n)),'original P21 class');require(dot(re,re)+dot(im,im)==1,'exact normalized input');delta=re[:];delta[0]-=1;require(dot(delta,delta)+dot(im,im)<=F(1,10000),'radius .01');return re,im
    def polynomial(sigma,vecnum,inputden):
        if not any(vecnum):return [0]*n
        scale=HD*sigma.denominator;tdiag=[a*sigma.numerator for a in hdiag];toff={k:a*sigma.numerator for k,a in hoff.items()};numer=vecnum[:];den=inputden
        for k in range(degree,0,-1):
            hv=[tdiag[i]*numer[i] for i in range(n)]
            for (i,j),a in toff.items():hv[i]+=a*numer[j]
            newden=den*scale*k;mult=newden//inputden;numer=[mult*vecnum[i]-hv[i] for i in range(n)];den=newden
        return [nearest(F(a,den),exportD) for a in numer]
    def evaluate(sigma,inp):
        re,im=validate(inp)
        if sigma==0:return {'branch':'exact_zero','denominator':inp['denominator'],'real':inp['real'],'imag':inp['imag'],'numerical_error_upper':F(0)}
        if sigma<=8:
            rr=polynomial(sigma,inp['real'],inp['denominator']);ii=polynomial(sigma,inp['imag'],inp['denominator']);branch='early_polynomial';bound=early_error
        else:
            ar=dot(v,re)/norm2;ai=dot(v,im)/norm2;rr=[nearest(a*ar,exportD) for a in v];ii=[nearest(a*ai,exportD) for a in v];branch='late_projector';bound=late_error
        return {'branch':branch,'denominator':exportD,'real':rr,'imag':ii,'numerical_error_upper':bound}
    # Three exact rational normalized preparations, including a complex nonvacuum input.
    inp0={'name':'vacuum','denominator':1,'real':[1]+[0]*(n-1),'imag':[0]*n};inp1={'name':'real_face0','denominator':160001,'real':[159999,800]+[0]*(n-2),'imag':[0]*n};inp2={'name':'imaginary_face19','denominator':160001,'real':[159999]+[0]*(n-1),'imag':[0]*n};inp2['imag'][20]=800
    times=[F(0),F(1),F(13,5),F(8),F(9),F(1000)];exports=[]
    for inp in (inp0,inp1,inp2):
        validate(inp)
        for sigma in times:exports.append({'input':inp['name'],'sigma':sigma,**evaluate(sigma,inp)})
    require(all(e['branch']=='early_polynomial' for e in exports if e['sigma']==8),'frozen join inclusive');require(all(e['branch']=='late_projector' for e in exports if e['sigma']>8),'late branch')
    for name in ('vacuum','real_face0','imaginary_face19'):
        a=next(e for e in exports if e['input']==name and e['sigma']==9);b=next(e for e in exports if e['input']==name and e['sigma']==1000);require(a['real']==b['real'] and a['imag']==b['imag'],'late projection prevents secular center growth')
    denfloor=F(7127,7200);physical_relative=F(457097,12472250000);full_relative=physical_relative+numerical/denfloor;require(full_relative<F(37,10**6),'complete all-time full-space allowance')
    contract=json.loads((ROOT/'research/round26/contracts/af2.json').read_text());paths=['research/round26/contracts/af2.json',*contract['bindings'],str(HERE.relative_to(ROOT)/'report.md'),str(HERE.relative_to(ROOT)/'check.py')]
    bindings={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(paths))}
    for p,digest in contract['bindings'].items():require(bindings[p]==digest,'dependency binding '+p)
    result={'schema':'ym26-forward-af2-v1','lambda':lam,'basis_labels':[b['label'] for b in basis],'gram_diagonal':G,'late_projector':{'trial_coordinates':v,'trial_norm_squared':norm2,'iterations':iterations,'projector_error_upper':projector_error},'uniform_errors':{'early_polynomial':early_poly,'early_center':early_center,'export_rounding':rounding,'early_total':early_error,'late_projector':projector_error,'late_excited_tail':late_tail,'late_total':late_error,'numerical_maximum':numerical,'physical_relative_AC2':physical_relative,'true_denominator':denfloor,'full_relative_total':full_relative},'inputs':[inp0,inp1,inp2],'exports':exports,'controls':{'all_1088_entries_checked':True,'complex_normalized_nonvacuum_executed':True,'zero_time_exact':True,'sigma8_early_sigma9_late':True,'sigma1000_no_center_secular_drift':True,'proof_covers_continuous_sigma_not_only_exports':True,'coupling_fixed_not_evaluated_uniformly':True},'bindings':bindings}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(clean(result),indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
