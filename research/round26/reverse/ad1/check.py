#!/usr/bin/env python3
import argparse,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def require(x,m):
    if x is not True:raise RuntimeError(m)
def shift(v,a,n=1):return tuple(v[i]+(n if i==a else 0) for i in range(3))
def links(f):
    a,b,*v=f;v=tuple(v);return {(a,*v),(b,*shift(v,a)),(a,*shift(v,b)),(b,*v)}
def omitted(f):
    a,b,x,y,z=f;return not(a==0 and b==1 and y%2==0 and x%4<3)
def owner(e):
    a,x,y,z=e
    return ('s',4*(x//4),2*(y//2),z) if (a==0 and x%4<3) or (a==1 and y%2==0) else ('f',*e)
def factor_edges(o):
    if o[0]=='f':return {o[1:]}
    _,x,y,z=o;return {(0,x+j,y+k,z) for j in range(3) for k in range(2)}|{(1,x+j,y,z) for j in range(4)}
def incident(edges):
    fs=set()
    for a,*v in edges:
        v=tuple(v)
        for b in range(3):
            if b!=a:
                for w in (v,shift(v,b,-1)):
                    f=(*sorted((a,b)),*w)
                    if min(w)>=0 and omitted(f):fs.add(f)
    return fs
def budget(q):return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def sqrt_upper(x):
    den=1<<240;n=math.isqrt(x.numerator*den*den//x.denominator);r=F(n,den);return r if r*r==x else F(n+1,den)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();out=Path(args.output).resolve();require(not out.exists(),'fresh output')
    con=json.loads((ROOT/'research/round26/contracts/ad1.json').read_text())
    for rel,h in con['bindings'].items():require(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,'binding '+rel)
    O=(3,1,0);cube=set()
    for v in itertools.product(range(2),repeat=3):
        for a in range(3):
            if v[a]==0:cube.add((a,*(O[i]+v[i] for i in range(3))))
    require(len(cube)==12 and all(owner(e)[0]=='f' for e in cube),'all cube factors free')
    fs=incident(cube);inside={f for f in fs if links(f)<=cube};outside=fs-inside
    require((len(inside),len(outside))==(6,20),'full face incidence')
    witness=(0,1,3,1,0);require(witness in inside,'fixed Wilson face')
    changes=[]
    for f in sorted(inside):
        r=len(links(f)&links(witness));d=[3-F(3,2)*r+2*m for m in range(r+1)]
        require(r in (0,1,4) and all(x!=0 for x in d),'no internal energy-three resonance')
        changes.append({'face':f,'overlap':r,'fusion_energy_changes':[str(x) for x in d]})
    external=[]
    for f in sorted(outside):
        el=links(f);common=el&cube;require(len(common)==1,'one shared edge')
        e=next(iter(common));op=next(t for t in el-common if t[0]==e[0]);require(owner(op)[0]=='f','free opposite')
        sides=el-common-{op};owners=[owner(t) for t in sorted(sides)];require(len(set(owners))==2,'distinct side factors')
        cost=sum(F(1,8) if t[0]=='s' else F(3,4) for t in owners);require(cost>=F(1,4),'positive loading')
        external.append({'face':f,'side_owners':owners,'minimum_external_energy_cost':str(cost)})
    factors={owner(e) for e in cube};collars=[]
    for k in range(4):
        es=set().union(*(factor_edges(o) for o in factors));cand=incident(es);retained={f for f in cand if {owner(e) for e in links(f)}<=factors}
        collars.append({'depth':k,'factors':len(factors),'links':len(es),'faces':len(retained)})
        factors|={owner(e) for f in cand for e in links(f)}
    samples=[];k=3;M=F(collars[k]['faces'],24);z=F(1,10**6);eta=F(1,2)
    coeff=F(1)
    for j in range(k+1):coeff*=F(4+j,j+1)
    x=15*z;tail=coeff*x**(k+1)/(1-x)**(k+5)
    for eps in [F(1,10**6),F(1,10**9),F(1,10**12)]:
        q=1-eps;tau=eta/(8*budget(q));s=z/eta*tau/eps**3;require(s<=3*z/2,'original slow clock')
        state=24*tau*sqrt_upper(budget(q*q)/96)/(F(1,8)*(1-eta));spatial=4*tail;avg=64*tau*M*(1+3*z*M)
        samples.append({name:str(val) for name,val in {'q':q,'tau':tau,'physical_time_in_hbar_over_alpha':z/eta/eps**3,'slow_time':s,'state_error':state,'spatial_error':spatial,'averaging_error':avg,'total_error':state+spatial+avg}.items()})
    require(F(samples[-1]['total_error'])<F(1,10**16),'explicit near-endpoint bound')
    # Independently enumerate the reserved six-cycle observable and its flip degree.
    edges=sorted(cube);vertices={tuple(e[1:]) for e in edges}|{shift(tuple(e[1:]),e[0]) for e in edges};cycles=[]
    for inds in itertools.combinations(range(12),6):
        deg={v:0 for v in vertices};adj={v:set() for v in vertices}
        for j in inds:
            a,*v=edges[j];v=tuple(v);w=shift(v,a);deg[v]+=1;deg[w]+=1;adj[v].add(w);adj[w].add(v)
        occupied={v for v in vertices if deg[v]}
        if all(deg[v] in (0,2) for v in vertices):
            seen={next(iter(occupied))}
            for _ in occupied:seen|=set().union(*(adj[v] for v in seen))
            if seen==occupied:cycles.append(frozenset(inds))
    require(len(cycles)==16,'complete six-cycle enumeration')
    masks={frozenset(edges.index(e) for e in links(f)) for f in inside};C=cycles[0];degree=sum(C^D in masks for D in cycles)
    require(degree in (2,6),'nonzero reserved curvature')
    paths=list(con['bindings'])+['research/round26/contracts/ad1.json','research/round26/reverse/ad1/report.md','research/round26/reverse/ad1/check.py','research/round24/forward/y1/report.md','research/round25/solo/aa2/check.py','.codex/skills/qeg-research-advisor/references/newton-tesla-project-method.md']
    result={'schema':'ym26-reverse-result-v1','loop':'ad1','status':'accepted-scoped-scalar','checks_passed':True,'observable':{'face':witness,'norm':'2','vacuum_mean':'0','vacuum_variance':'1','reference_energy_over_alpha':'3'},'internal_fusion_checks':changes,'external_loading':external,'collars':collars,'spatial_tail_initial_factor_parameter':'4','endpoint_scalar':'1','samples':samples,'reserved_wilson_discriminator':{'edges':[edges[j] for j in sorted(C)],'flip_degree':degree,'second_z_derivative':str(-F(degree,84**2)),'used_for_fitting':False},'source_inventory':{r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in sorted(set(paths))}}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
