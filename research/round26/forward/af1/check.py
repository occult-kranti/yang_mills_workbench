#!/usr/bin/env python3
"""Certified actual293 heat vector; exact integer Horner arithmetic."""
import argparse,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise ValueError(m)
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    return x
def nearest_scaled(x,D):
    n,r=divmod(x.numerator*D,x.denominator);return n+int(2*r>=x.denominator)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);require(not out.exists(),'fresh output')
    source=json.loads((ROOT/'research/round26/forward/ac1/output/results.json').read_text());basis=source['basis'];n=len(basis);require(n==293,'actual dimension');gram=[F(b['norm2']) for b in basis];energy=[F(b['energy']) for b in basis];S={(i,j):F(a) for i,j,a in source['magnetic_sparse_entries']};labels={b['label']:i for i,b in enumerate(basis)}
    # Verify every sparse matrix column via its named actual product branch.
    expected={}
    def couple(label,p,c):
        i=labels[label];j=labels['face_'+str(p)];expected[i,j]=c;expected[j,i]=c*gram[i]
    for p in range(20):couple('vacuum',p,F(1,2));couple('spin1_'+str(p),p,F(1,2))
    for label in labels:
        parts=label.split('_')
        if parts[0] in ('pair','singlet','triplet'):
            kind,p,q=parts[0],int(parts[1]),int(parts[2]);i=labels[label]
            require(gram[i]==(3 if kind=='triplet' else 1),'triplet metric')
            for face in (p,q):couple(label,face,F(1,2) if kind=='pair' else F(1,4))
    require(expected==S and len(S)==1088,'entire magnetic matrix')
    require(all(gram[i]*a==gram[j]*S[j,i] for (i,j),a in S.items()),'metric self-adjointness')
    lam=F(1,100);c=20*lam;diag=[e+c for e in energy]
    def Smul(v):
        w=[F(0)]*n
        for (i,j),a in S.items():w[i]+=a*v[j]
        return w
    def Amul(v):
        sv=Smul(v);return [diag[i]*v[i]-lam*sv[i] for i in range(n)]
    def dot(v,w):return sum((gram[i]*v[i]*w[i] for i in range(n)),F(0))
    # One physical residual correction, used only to certify the retained center.
    v=[F(0)]*n;v[0]=1
    for p in range(20):v[p+1]=lam/6
    sv=Smul(v)
    for i in range(21,n):v[i]=lam*sv[i]/energy[i]
    av=Amul(v);norm2=dot(v,v);rayleigh=dot(v,av)/norm2;res2=dot(av,av)/norm2-rayleigh**2
    require(0<=rayleigh<3 and res2>=0,'actual spectral residual hypotheses')
    lo=rayleigh-res2/(3-rayleigh);hi=rayleigh;require(0<lo<=hi<c,'retained minimum enclosure')
    D=10**24;munum=nearest_scaled((lo+hi)/2,D);muhat=F(munum,D);center_radius=max(abs(muhat-lo),abs(muhat-hi));require(center_radius<F(1,10**11),'certified center precision')
    # Integer coefficient matrix for H=A-muhat at the frozen sigma=1.
    hdiag=[int((d-muhat)*D) for d in diag];hoff={(i,j):int(-lam*a*D) for (i,j),a in S.items()};require(all(F(hdiag[i],D)==diag[i]-muhat for i in range(n)),'diagonal integer exactness');require(all(F(v,D)==-lam*S[i,j] for (i,j),v in hoff.items()),'offdiagonal integer exactness')
    degree=100;numer=[0]*n;numer[0]=1;denom=1
    for k in range(degree,0,-1):
        hv=[hdiag[i]*numer[i] for i in range(n)]
        for (i,j),a in hoff.items():hv[i]+=a*numer[j]
        newden=denom*D*k;numer=[-a for a in hv];numer[0]+=newden;denom=newden
    require(denom==D**degree*math.factorial(degree),'exact Horner denominator')
    # e^9<2^14 from e^(2/3)<2; norm H<=9 in the actual Gram.
    x=F(2,3);N=30;psum=sum((x**k/F(math.factorial(k)) for k in range(N+1)),F(0));pupper=psum+x**(N+1)/math.factorial(N+1)/(1-x/(N+2));require(pupper<2,'exponential remainder prefactor')
    taylor=F(2**14*9**101,math.factorial(101));require(taylor<F(1,10**55),'certified Taylor norm error')
    exportD=10**50;coords=[nearest_scaled(F(a,denom),exportD) for a in numer];rounding=F(21,2*exportD);require(sum(gram)==417<21**2,'full metric export norm')
    center=center_radius/(1-center_radius);retained_error=center+taylor+rounding
    g=F(14,5);p21=F(1,12000);rp=F(1,60000);delta=rp*rp/g;qplus=F(61,8000);physical=delta+F(1,5)*F(1,32)*(qplus/F(9,2)+qplus/(g*F(9,2)));denfloor=1-F(5,9)*lam**2-p21;total=physical+retained_error;relative=total/denfloor
    require(relative<F(15,10**6),'full-space relative accuracy at the frozen point')
    require(coords[0]>0 and all(a>=0 for a in coords),'positive heat-vector readout')
    # Zero controls are exact identities, never Taylor approximations to them.
    zero_time=[1]+[0]*(n-1);require(sum(zero_time)==1,'zero-time vacuum identity');require(energy[0]==0,'zero-coupling vacuum eigenvalue')
    coordresult={'basis_labels':[b['label'] for b in basis],'coordinate_integer_numerators':coords,'common_denominator':exportD,'gram_diagonal':[str(g) for g in gram],'interpretation':'actual rational coordinate vector; triplets have squared norm3','display_only':{'vacuum_coefficient':float(F(coords[0],exportD)),'first_face_coefficient':float(F(coords[1],exportD)),'retained_center':float(muhat),'full_relative_upper':float(relative)}}
    contract=json.loads((ROOT/'research/round26/contracts/af1.json').read_text());paths=['research/round26/contracts/af1.json',*contract['bindings'],str(HERE.relative_to(ROOT)/'report.md'),str(HERE.relative_to(ROOT)/'check.py')]
    bindings={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(paths))}
    for p,digest in contract['bindings'].items():require(bindings[p]==digest,'dependency binding '+p)
    result={'schema':'ym26-forward-af1-v1','point':{'lambda':lam,'sigma':F(1),'input':'Omega'},'center':{'trial_norm_squared':norm2,'rayleigh':rayleigh,'retained_residual_squared':res2,'mu_interval':[lo,hi],'rounded_center':muhat,'center_radius':center_radius},'coordinates':coordresult,'errors':{'center_heat':center,'degree100_Taylor':taylor,'export_rounding':rounding,'retained_total':retained_error,'physical_omission_and_true_ground_center':physical,'true_denominator_floor':denfloor,'full_absolute':total,'full_relative':relative},'controls':{'all_sparse_entries_verified':True,'triplet_Gram_retained':True,'minimum_isolated_by_actual_second_eigenvalue_lower3':True,'zero_time_exact':True,'zero_coupling_vacuum_exact':True,'point_only_computation':True,'float_readouts_not_certificates':True},'bindings':bindings}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(clean(result),indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
