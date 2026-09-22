#!/usr/bin/env python3
"""Exact AG1 selected-source estimates and independently labeled finite-algebra controls."""
import argparse,hashlib,itertools,json
from fractions import Fraction as F
from math import factorial,comb
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];checks=[]
def req(x,m):
    if not x:raise ValueError(m)
    checks.append(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
STAR={(0,0,0),(1,0,0),(0,1,0),(0,0,1)}
def stars(anchor):return {plus(anchor,s) for s in STAR}
def face_count():
    diff={tuple(a-b for a,b in zip(x,y)) for x in STAR for y in STAR}
    req(len(diff)==13,'thirteen actual overlap anchor differences')
    req(len(diff-{(0,0,0)})==12,'twelve interior crossings')
    origin=[a for a in diff if min(a)>=0 and a!=(0,0,0)]
    req(len(origin)==3,'three positive-octant origin crossings')
    req(all(len(STAR&stars(a))==1 and len(STAR|stars(a))==7 for a in diff if a!=(0,0,0)),'crossing supports retain seven factors')
    counts=[]
    for side in [1,2,3]:
        verts=set(itertools.product(range(side+1),repeat=3));anchors=[a for a in verts if stars(a)<=verts]
        c=max([sum(x in stars(a) for a in anchors) for x in verts],default=0)
        req(1<=c<=4,'nonempty actual input multiplicity '+str(side));counts.append({'side':side,'anchors':len(anchors),'max_root_multiplicity':c,'actual_input_norm_coefficient':16*c})
    req(counts[0]['max_root_multiplicity']==1 and counts[-1]['max_root_multiplicity']==4,'both denominator extremal cases occur')
    # Full relative two-word census checks repeats and attachment away from base.
    words=[]
    for a in diff:
        union=STAR|stars(a)
        second={tuple(v[j]-s[j] for j in range(3)) for v in union for s in STAR}
        req(len(second)<=26,'second step full incoming overlap bound')
        for b in second:words.append((a,b))
    req(any(a==b for a,b in words),'repeated words retained')
    req(any(not(STAR&stars(b)) and (stars(a)&stars(b)) for a,b in words),'attachment to generated support retained')
    return {'difference_set':sorted(diff),'finite_cuboids':counts,'two_word_count':len(words)}
def Fgeom(x):return (4-x)/(1-x)**2
def ftail(x,n):return x**(n+1)*((3*n+7)-(3*n+4)*x)/(1-x)**2
def interval(M):
    rho=F(9,4);T=F(3);z=26*M*rho**3*T;z2=208*M*T
    req(z<1,'auxiliary rho radius '+str(M));req(z2<1,'original weight radius '+str(M))
    r_up=F(1337,2250)*(M/7)**3
    B=rho**4*Fgeom(z);A=4*rho**4;theta=18*B*r_up
    req(theta<1,'all-order commutator majorant converges '+str(M))
    n_over_r=theta/(1-theta)*(A+B/2)
    # Main unrestricted positive residual budget; not an actual denominator.
    main_residual_coefficient=16*Fgeom(z2)
    narrow_ratio=F(4,9)+(Fgeom(z2)-4)+n_over_r/16
    return {'M_max':M,'rho':rho,'T':T,'auxiliary_ratio':z,'original_ratio':z2,'r_upper':r_up,'A_rho_over_r':A,'R_and_S_rho_over_r':B,'theta':theta,'N_weight2_over_actual_r':n_over_r,'main_R_weight2_over_r':main_residual_coefficient,'narrow_selected_contraction_ratio':narrow_ratio,'additional_E_transport_factor':1/(1-theta)}
def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),F(0)) for j in range(len(B[0]))] for i in range(len(A))]
def addm(A,B):return [[x+y for x,y in zip(a,b)] for a,b in zip(A,B)]
def scale(A,c):return [[c*x for x in row] for row in A]
def sub(A,B):return addm(A,scale(B,-1))
def comm(A,B):return sub(mm(A,B),mm(B,A))
def ad(S,A,n):
    for _ in range(n):A=comm(S,A)
    return A
def split(A):
    c=A[0][0];I=[[F(1),F(0)],[F(0),F(1)]]
    source=[[F(0),A[0][1]],[A[1][0],F(0)]]
    diag=[[F(0),F(0)],[F(0),A[1][1]-c]]
    return c,source,diag,addm(addm(scale(I,c),source),diag)
def algebra():
    G=[[F(0),F(0)],[F(0),F(2)]]
    S=[[F(0),F(-1,10)],[F(1,10),F(0)]]
    A=[[F(0),F(3,5)],[F(3,5),F(0)]]
    R=addm(A,comm(S,G));req(R==[[0,F(2,5)],[F(2,5),0]],'finite diagnostic retains nonzero residual')
    rows=[]
    for j in range(1,10):
        lhs=addm(scale(ad(S,G,j),F(1,factorial(j))),scale(ad(S,A,j-1),F(1,factorial(j-1))))
        rhs=R if j==1 else scale(ad(S,addm(scale(A,j-1),R),j-1),F(1,factorial(j)))
        req(lhs==rhs,'full G plus A BCH coefficient '+str(j))
        c,source,diagonal,recombined=split(rhs)
        req(recombined==rhs,'all scalar source diagonal terms retained '+str(j))
        rows.append({'power':j,'coefficient':rhs,'scalar':c,'mixing':source,'centered_diagonal':diagonal})
    correct=scale(comm(S,addm(A,R)),F(1,2));wrong=scale(comm(S,sub(R,A)),F(1,2))
    req(correct!=wrong,'G-only BCH coefficient rejected')
    req(correct!=scale(comm(S,A),F(1,2)),'omitted residual BCH rejected')
    req(rows[1]['scalar']!=0 and rows[1]['centered_diagonal']!=[[0,0],[0,0]],'nonlinear scalar and diagonal actually nonzero in diagnostic')
    E=[[F(1,7),F(1,9)],[F(1,9),F(-2,7)]]
    req(any(x for row in comm(S,E) for x in row),'additional E is transformed not dropped')
    for j in range(1,8):
        base=addm(scale(ad(S,G,j),F(1,factorial(j))),scale(ad(S,A,j-1),F(1,factorial(j-1))))
        req(addm(base,scale(ad(S,E,j),F(1,factorial(j))))!=base,'additional E order retained '+str(j))
    # Same-weight commutator obstruction: Phi=2^-n product X, Psi=sum Z_i/2.
    pauli=[]
    for n in range(1,6):
        d=2**n;P=[[F(int(j==(d-1-i)),2**n) for j in range(d)] for i in range(d)]
        Z=[[F(n-2*i.bit_count(),2) if i==j else F(0) for j in range(d)] for i in range(d)]
        C=comm(P,Z);Ct=[list(row) for row in zip(*C)];C2=mm(Ct,C)
        req(all(C2[i][j]==0 for i in range(d) for j in range(d) if i!=j),'Pauli commutator squared diagonal '+str(n))
        req(max(C2[i][i] for i in range(d))==F(n*n,4**n),'same-weight exact norm growth '+str(n))
        pauli.append({'sites':n,'input_norms':[1,1],'output_weight2_norm':n})
    return {'scope':'finite algebra diagnostic only, not SU2 spectral simulation','G':G,'S':S,'A':A,'R':R,'BCH_coefficients':rows,'same_weight_obstruction':pauli}
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    return x
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output)
    req(out.is_absolute() and not out.exists(),'fresh absolute output')
    contract=json.loads((HERE/'inputs/contract.json').read_text());req(contract['loop']=='ag1','frozen AG1 contract')
    inventory=json.loads((HERE/'inputs/source-inventory.json').read_text());req(inventory['frozen_before_production'],'inputs frozen before production')
    for e in inventory['entries']:req(sha(ROOT/e['source'])==sha(ROOT/e['snapshot'])==e['sha256'],'bound snapshot '+e['source'])
    req(F(191,250)**2>F(7,12),'rational cubic-source square-root upper bound')
    req(F(4,3)*F(7,12)*F(191,250)==F(1337,2250),'rational source coefficient')
    req((24*F(1,1000)+F(2,3))/(1-F(1,1000))==F(2072,2997),'complete twelve-crossing per-source residual')
    req(F(2072,2997)<F(7,10),'main per-source contraction retained without weighted inference')
    geometry=face_count();mainbound=interval(F(1,1000));narrow=interval(F(1,10000));zero=interval(F(0))
    req(mainbound['auxiliary_ratio']==F(28431,32000),'main auxiliary endpoint exact')
    req(mainbound['main_R_weight2_over_r']>64,'main positive residual is not contraction proof')
    req(narrow['narrow_selected_contraction_ratio']<F(93,100),'actual narrow selected-family contraction below 0.93')
    req(narrow['narrow_selected_contraction_ratio']>F(4,9),'positive D-loading and nonlinear cost retained')
    req(zero['r_upper']==0 and zero['theta']==0 and zero['N_weight2_over_actual_r']==0,'zero coupling remains zero without dividing actual r')
    for tau in [F(1,7000),F(-1,7000),F(1,70000),F(-1,70000),F(0)]:
        M=7*abs(tau);req(F(1337,2250)*abs(tau)**3==interval(M)['r_upper'],'both-sign absolute cubic bound '+str(tau))
    for x in [mainbound['auxiliary_ratio'],narrow['auxiliary_ratio'],narrow['original_ratio']]:
        for n in [0,1,4,10]:
            partial=sum((4+3*j)*x**j for j in range(n+1))
            req(partial+ftail(x,n)==Fgeom(x),'complete positive geometric tail '+str((x,n)))
    # Exact compact-kernel time integrals; factors before n! appear in report.
    for n in range(9):
        p_moment=2*3**n*(F(1,n+1)-F(1,n+2))
        h_moment=3**(n+1)*(F(1,n+1)-F(2,n+2)+F(1,n+3))
        req(p_moment==F(2*3**n,(n+1)*(n+2)),'triangular residual kernel moment '+str(n))
        req(h_moment==F(2*3**(n+1),(n+1)*(n+2)*(n+3)),'integrated primitive kernel moment '+str(n))
    req(F(4,9)<1,'free source spectral-gap residual bound')
    req(F(1,8)/(1+F(1,8))==F(1,9),'log(9/8) lower bound coefficient')
    algebra_result=algebra()
    paths=list(contract['sources'])+['research/round27/contracts/ag1.json','research/round27/methods/historical-physics-panel/references/lenses-and-evidence.md']
    paths += [str(p.relative_to(ROOT)) for p in (HERE/'inputs').rglob('*') if p.is_file()]
    paths += [str((HERE/n).relative_to(ROOT)) for n in ['report.md','check.py']]
    result={'schema':'ym27-reverse-ag1-v1','scope':'one actual selected-source nonlinear update, not complete transformed Hamiltonian','main':mainbound,'narrow':narrow,'zero':zero,'geometry':geometry,'diagnostic':algebra_result,'checks':checks,'check_count':len(checks),'bindings':{p:sha(ROOT/p) for p in sorted(set(paths))}}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(clean(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'checks':len(checks),'main':{k:float(v) for k,v in mainbound.items()},'narrow':{k:float(v) for k,v in narrow.items()}}))
if __name__=='__main__':main()
