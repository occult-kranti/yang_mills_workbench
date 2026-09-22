#!/usr/bin/env python3
"""Exact fixed-source spectral measures and actual multiplication error budgets."""
import argparse,hashlib,itertools,json,math
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise ValueError(m)
def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),F(0)) for j in range(len(B[0]))] for i in range(len(A))]
def mv(A,v):return [sum((a*b for a,b in zip(row,v)),F(0)) for row in A]
def expectation(v,A,norm2):return sum(a*b for a,b in zip(v,mv(A,v)))/norm2
def sqrt_up(x):
    d=1<<240;n=isqrt(x.numerator*d*d//x.denominator);r=F(n,d);return r if r*r==x else F(n+1,d)
def budget(q):return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [clean(v) for v in x]
    return x
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);require(not out.exists(),'fresh output')
    src=json.loads((ROOT/'research/round25/solo/aa1/output/results.json').read_text());edges=[tuple(map(tuple,e)) for e in src['edges']];edgeidx={frozenset(e):i for i,e in enumerate(edges)};cycles=[frozenset(c) for c in src['cycles']];faces={frozenset(f['edges']):f['anchor_sum'] for f in src['faces']};n=len(cycles)
    # Reconstruct all simple six-cycles from actual graph degrees/connectivity.
    actual=[]
    for choice in itertools.combinations(range(12),6):
        adj={}
        for e in choice:
            v,w=edges[e];adj.setdefault(v,set()).add(w);adj.setdefault(w,set()).add(v)
        if not all(len(v)==2 for v in adj.values()):continue
        seen=set();pending=[next(iter(adj))]
        while pending:
            v=pending.pop()
            if v in seen:continue
            seen.add(v);pending.extend(adj[v]-seen)
        if len(seen)==6:actual.append(frozenset(choice))
    require(set(actual)==set(cycles) and len(cycles)==16,'complete six-cycle shell')
    O=(3,1,0);X=[(3,1,0),(3,2,0),(3,2,1)];Y=[(3,1,0),(3,1,1),(3,2,1)];Z=[(3,1,0),(4,1,0),(4,2,0),(4,2,1),(3,2,1)]
    def path_edges(path):return {edgeidx[frozenset(tuple(v[j]-O[j] for j in range(3)) for v in (a,b))] for a,b in zip(path,path[1:])}
    cx=frozenset(path_edges(X)|path_edges(Z));cy=frozenset(path_edges(Y)|path_edges(Z));ix=cycles.index(cx);iy=cycles.index(cy);require([ix,iy]==src['u_indices']==[10,6],'named paths, no eigenvector selection')
    A=[[F(c^d in faces) for d in cycles] for c in cycles];require(A==src['matrix_adjacency'],'every physical face flip')
    I=[[F(i==j) for j in range(n)] for i in range(n)];A2=mm(A,A);A4=mm(A2,A2)
    P0=[[(A4[i][j]-16*A2[i][j]+48*I[i][j])/48 for j in range(n)] for i in range(n)];P4=[[(12*A2[i][j]-A4[i][j])/32 for j in range(n)] for i in range(n)];P12=[[(A4[i][j]-4*A2[i][j])/96 for j in range(n)] for i in range(n)]
    require(all(x==0 for row in mm(A,mm([[A2[i][j]-4*I[i][j] for j in range(n)] for i in range(n)],[[A2[i][j]-12*I[i][j] for j in range(n)] for i in range(n)])) for x in row),'full spectral polynomial')
    q=1-F(1,10**12);eta=F(1,2);z=F(1,10**6);theta=z/84;tau=eta/(8*budget(q));s=z/eta*tau/(1-q)**3;M=F(332,24);Q=[[q**faces[c^d] if c^d in faces else F(0) for d in cycles] for c in cycles]
    require(max(sum(row) for row in Q)<=6 and s<=3*z/2,'full matrix/time norm')
    dhat=tau*sqrt_up(budget(q*q)/96)/(F(1,8)*(1-eta));coeff=F(1)
    for j in range(4):coeff*=F(8,3)+j;coeff/=j+1
    tail=coeff*(15*z)**4/(1-15*z)**7;b=16*tau*M*(1+3*z*M);arithmetic=(s/16)**9/math.factorial(9);results=[]
    for name,inds,norm2,J2,avgfactor,expectedmom in [('X',[ix],F(1),F(4),F(3),[1,0,2,0,16,0,160]),('sum',[ix,iy],F(2),F(8),F(4),[1,1,4,8,32,80,320])]:
        v=[F(i in inds) for i in range(n)];w=v[:];mom=[]
        for degree in range(7):mom.append(sum(v[i]*w[i] for i in range(n))/norm2);w=mv(A,w)
        require(mom==expectedmom,'exact observable moments')
        weights=[expectation(v,P,norm2) for P in (P0,P4,P12)];odd=[expectation(v,mm(A,P),norm2) for P in (P0,P4,P12)]
        require(sum(weights)==1 and all(w>=0 for w in weights),'spectral squared weights')
        if name=='X':require(weights==[F(2,3),F(1,4),F(1,12)] and odd==[0,0,0],'X measure')
        else:require(weights==[F(1,3),F(1,2),F(1,6)] and odd==[0,F(1,2),F(1,2)],'coherent measure')
        re=im=F(0);w=v[:]
        for degree in range(9):
            moment=sum(v[i]*w[i] for i in range(n))/norm2;term=moment*(s/96)**degree/math.factorial(degree)
            if degree%2:im+=(-1)**((degree-1)//2)*term
            else:re+=(-1)**(degree//2)*term
            w=mv(Q,w)
        state=6*J2*dhat;spatial=J2*tail;averaging=avgfactor*b;total=state+spatial+averaging+arithmetic
        require(total<(F(5,10**18) if name=='X' else F(1,10**17)),'complete finiteq remainder')
        if name=='X':require(1-re>total,'finiteq scalar differs from one within complete disk')
        results.append({'name':name,'moments':mom,'squared_eigenvalue_weights':weights,'odd_projector_moments':odd,'norm_squared':J2,'vacuum_variance':F(1),'vacuum_fourth_moment':F(2) if name=='X' else F(5,2),'finiteq':{'center_real':re,'center_imag':im,'state_error':state,'spatial_error':spatial,'averaging_error':averaging,'arithmetic_error':arithmetic,'total_error':total}})
    require(theta*theta-F(2,3)*theta**4>0,'nonzero X endpoint')
    require(16!=2**2 and 4!=1**2,'higher-moment single-frequency rejection')
    contract=json.loads((ROOT/'research/round26/contracts/ad2.json').read_text());paths=['research/round26/contracts/ad2.json',*contract['bindings'],'research/round23/forward/u1/report.md',str(HERE.relative_to(ROOT)/'report.md'),str(HERE.relative_to(ROOT)/'check.py')]
    bindings={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(paths))}
    for p,digest in contract['bindings'].items():require(bindings[p]==digest,'dependency binding '+p)
    result={'schema':'ym26-forward-ad2-v1','sources':results,'u_indices':[ix,iy],'q':q,'eta':eta,'z':z,'physical_time_in_hbar_over_alpha':z/eta/(1-q)**3,'additional_limit_comparison':s*(1-q**5)/16+abs(s-8*z/7)/16,'controls':{'null_elementary_witness_retained':True,'rank_operator_identity_rejected_by_fourth_moment':True,'single_frequency_rejected_by_fourth_moment':True,'full_sixteen_component_used':True,'all_exterior_support_inherited_from_AA2':True},'bindings':bindings}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(clean(result),indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
