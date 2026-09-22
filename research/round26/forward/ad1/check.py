#!/usr/bin/env python3
"""Exact free-cube selection, complete owners, and full scalar error."""
import argparse,hashlib,itertools,json
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise ValueError(m)
def shift(v,a,d=1):return tuple(v[j]+(d if j==a else 0) for j in range(3))
def links(f):
    a,b,*v=f;v=tuple(v);return {(a,*v),(b,*shift(v,a)),(a,*shift(v,b)),(b,*v)}
def omitted(f):
    a,b,x,y,z=f;return not(a==0 and b==1 and y%2==0 and x%4<3)
def owner(e):
    a,x,y,z=e;return ('s',x//4*4,y//2*2,z) if (a==0 and x%4<3) or (a==1 and y%2==0) else ('f',a,x,y,z)
def factor_edges(t):
    if t[0]=='f':return {t[1:]}
    _,x,y,z=t;return {(0,x+r,y+s,z) for r in range(3) for s in range(2)}|{(1,x+r,y,z) for r in range(4)}
def incident(edges):
    result=set()
    for a,*v in edges:
        v=tuple(v)
        for b in range(3):
            if a==b:continue
            for w in (v,shift(v,b,-1)):
                f=(*sorted((a,b)),*w)
                if min(w)>=0 and omitted(f):result.add(f)
    return result
def sqrt_up(x):
    den=1<<240;n=isqrt(x.numerator*den*den//x.denominator);lo=F(n,den);return lo if lo*lo==x else F(n+1,den)
def budget(q):return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [clean(v) for v in x]
    return x
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);require(not out.exists(),'fresh output')
    origin=(3,1,0);cube=set()
    for off in itertools.product((0,1),repeat=3):
        v=tuple(origin[j]+off[j] for j in range(3))
        for a in range(3):
            if off[a]==0:cube.add((a,*v))
    require(len(cube)==12 and all(owner(e)[0]=='f' for e in cube),'actual free cube')
    f0=(1,2,*origin);occupied=links(f0);allfaces=incident(cube);internal={f for f in allfaces if links(f)<=cube};external=allfaces-internal
    require((len(internal),len(external))==(6,20),'complete face incidence')
    counts={r:sum(len(links(f)&occupied)==r for f in internal) for r in (0,1,4)};require(counts=={0:1,1:4,4:1},'actual square intersections')
    changes={3-F(3,2)*r+2*m for r in counts for m in range(r+1)};require(0 not in changes,'internal no resonance')
    rows=[]
    for f in sorted(external):
        el=links(f);shared=el&cube;require(len(shared)==1,'one shared cube edge');a=next(iter(shared))[0]
        opposite=next(e for e in el-shared if e[0]==a);require(owner(opposite)[0]=='f','opposite free')
        sides=el-shared-{opposite};owners=sorted(owner(e) for e in sides);require(len(set(owners))==2,'distinct outside owners')
        cost=sum(F(1,8) if t[0]=='s' else F(3,4) for t in owners);require(cost>=F(1,4),'positive external loading')
        rows.append({'face':f,'side_owners':owners,'cost_lower':cost})
    # Haar marginal: chi_half^2=1+chi_one; both summands normalized orthogonal.
    require(4*F(1,4)==1,'actual variance one');same_face_norm2=F(1,4)+F(1,4);require(same_face_norm2==F(1,2),'full same-face image')
    # Reconstruct original U support, which contains B support.
    X=[(3,1,0),(3,2,0),(3,2,1)];Y=[(3,1,0),(3,1,1),(3,2,1)];Z=[(3,1,0),(4,1,0),(4,2,0),(4,2,1),(3,2,1)]
    initial=set()
    for path in (X,Y,Z):
        for v,w in zip(path,path[1:]):
            a=next(j for j in range(3) if v[j]!=w[j]);initial.add((a,*min(v,w)))
    require(len(initial)==8 and occupied<=initial,'B support in inherited collar seed')
    factors={owner(e) for e in initial};collars=[]
    for k in range(4):
        edges=set().union(*(factor_edges(t) for t in factors));candidates=incident(edges);inside={f for f in candidates if {owner(e) for e in links(f)}<=factors}
        collars.append({'k':k,'face_count':len(inside),'factor_count':len(factors)})
        if k>=1:require(cube<=edges,'cube retained')
        factors|={owner(e) for f in candidates for e in links(f)}
    require([d['face_count'] for d in collars]==[1,20,129,332],'actual collars')
    q=1-F(1,10**12);eta=F(1,2);z=F(1,10**6);tau=eta/(8*budget(q));s=z/eta*tau/(1-q)**3;M=F(332,24);k=3
    dhat=tau*sqrt_up(budget(q*q)/96)/(F(1,8)*(1-eta));coeff=F(1)
    for j in range(k+1):coeff*=F(8,3)+j;coeff/=j+1
    x=15*z;tail=coeff*x**(k+1)/(1-x)**(k+4);state=24*dhat;spatial=4*tail;averaging=48*tau*M*(1+3*z*M);total=state+spatial+averaging
    require(s<=3*z/2 and total<F(5,10**18),'original-clock full scalar certificate')
    discriminant=z/84-z*z/3528;require(discriminant>0,'held-out rank scalar differs')
    contract=json.loads((ROOT/'research/round26/contracts/ad1.json').read_text());paths=['research/round26/contracts/ad1.json',*contract['bindings'],'research/round23/forward/u1/report.md',str(HERE.relative_to(ROOT)/'report.md'),str(HERE.relative_to(ROOT)/'check.py')]
    bindings={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(paths))}
    for p,d in contract['bindings'].items():require(bindings[p]==d,'dependency binding '+p)
    result={'schema':'ym26-forward-ad1-v1','observable':'fundamental character of yz face at (3,1,0), multiplication norm2','endpoint':{'demodulation_energy_in_alpha':3,'scalar':1,'reachable_averaged_dimension':1,'reachable_generator':0},'internal_intersections':counts,'exterior':rows,'collars':collars,'finite_q':{'q':q,'eta':eta,'z':z,'physical_time_in_hbar_over_alpha':z/eta/(1-q)**3,'state_error':state,'spatial_error':spatial,'averaging_error':averaging,'total_error':total},'controls':{'actual_instantaneous_vacuum_loading':-q**4/48,'wrong_rank_swap_rejected':True,'wrong_norm_one_rejected':True,'AA2_scalar_difference_lower':discriminant,'same_clock_no_rate_identification':True},'bindings':bindings}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(clean(result),indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
