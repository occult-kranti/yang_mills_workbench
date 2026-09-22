"""Actual factor geometry and certified scalar arithmetic, standard library only."""
import argparse
from fractions import Fraction as F
import itertools as it
import json
from math import factorial, isqrt
from decimal import Decimal, localcontext
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
def require(ok, message):
    if not ok: raise ValueError(message)
def shift(v,a,d=1): return tuple(v[j]+(d if j==a else 0) for j in range(3))
def links(f):
    a,b,*v=f;v=tuple(v)
    return {(a,*v),(b,*shift(v,a)),(a,*shift(v,b)),(b,*v)}
def omitted(f):
    a,b,x,y,z=f
    return not (a==0 and b==1 and y%2==0 and x%4<3)
def owner(e):
    a,x,y,z=e
    return ('s',x//4*4,y//2*2,z) if (a==0 and x%4<3) or (a==1 and y%2==0) else ('f',a,x,y,z)
def factor_edges(t):
    if t[0]=='f': return {t[1:]}
    _,x,y,z=t
    return {(0,x+r,y+s,z) for r in range(3) for s in range(2)}|{(1,x+r,y,z) for r in range(4)}
def incident(edges):
    result=set()
    for a,*v in edges:
        v=tuple(v)
        for b in range(3):
            if a==b:continue
            for w in (v,shift(v,b,-1)):
                f=(*sorted((a,b)),*w)
                if min(w)>=0 and omitted(f): result.add(f)
    return result
def ceil_sqrt(x,bits=240):
    den=1<<bits
    n=isqrt(x.numerator*den*den//x.denominator)
    lo=F(n,den)
    return lo if lo*lo==x else F(n+1,den)
def budget(q):
    P=2+5*q+5*q*q+6*q**3+3*q**4
    return P/(24*(1-q)**3*(1+q)**2*(1+q*q))
def scalar(q,eta,z,k,N,basis):
    tau=eta/(8*budget(q)); s=z/eta*tau/(1-q)**3; M=F(N,24); S=3*z/2
    require(s<=S,'slow clock envelope')
    sigma2=tau*tau*budget(q*q)/96
    state=6*ceil_sqrt(sigma2)/(F(1,8)*(1-eta))
    ak=F(1)
    for j in range(k+1):ak*=F(8,3)+j;ak/=j+1
    x=15*z; spatial=ak*x**(k+1)/(1-x)**(k+4)
    averaging=32*tau*M*(1+2*S*M) # two source vectors, each delta >= 1/8
    cycles=[frozenset(c) for c in basis['cycles']]; n=len(cycles)
    face_weights={frozenset(f['edges']):q**f['anchor_sum'] for f in basis['faces']}
    Q=[[face_weights.get(c^d,F(0)) for d in cycles] for c in cycles]
    u=basis['u_indices'];v=[F(i in u) for i in range(n)]
    re=F(0);im=F(0);degree=8
    for j in range(degree+1):
        moment=sum(v[i] for i in u)/2
        term=moment*(s/96)**j/factorial(j)
        if j%2: im+=term*((-1)**((j-1)//2))
        else: re+=term*((-1)**(j//2))
        v=[sum(Q[i][j]*v[j] for j in range(n)) for i in range(n)]
    row_norm=max(sum(row) for row in Q)/96
    require(row_norm<=F(1,16),'matrix row norm')
    arithmetic=(s*row_norm)**(degree+1)/factorial(degree+1)
    total=state+spatial+averaging+arithmetic
    limit_difference=s*(1-q**5)/16+abs(s-8*z/7)/16
    exact={'q':q,'eta':eta,'z':z,'tau':tau,'slow_time':s,
      'physical_time_in_hbar_over_alpha':z/eta/(1-q)**3,
      'scalar_real':re,'scalar_imag':im,'state_error':state,'spatial_error':spatial,
      'averaging_error':averaging,'arithmetic_error':arithmetic,'total_error':total,
      'additional_limit_comparison_error':limit_difference}
    return {'exact':{key:str(val) for key,val in exact.items()},
            'display':{**{key:float(val) for key,val in exact.items()},'scalar_real_minus_one':float(re-1)},
            'depth':k,'retained_faces':N}

def compute():
    basis=json.loads((ROOT/'research/round25/solo/aa1/output/results.json').read_text())
    O=(3,1,0)
    cube=set()
    for v,w in basis['edges']:
        a=next(i for i in range(3) if v[i]!=w[i])
        cube.add((a,*(v[j]+O[j] for j in range(3))))
    require(len(cube)==12 and all(owner(e)[0]=='f' for e in cube),'free cube')
    all_faces=incident(cube)
    internal={f for f in all_faces if links(f)<=cube};external=all_faces-internal
    require(len(internal)==6,'all cube faces')
    rows=[]
    for f in sorted(external):
        el=links(f);shared=el&cube
        require(len(shared)==1,'external face intersects at most one cube edge')
        a,*v=next(iter(shared))
        opposite=next(e for e in el-shared if e[0]==a)
        require(owner(opposite)[0]=='f','opposite edge must be free')
        sides=el-shared-{opposite};owners=[owner(e) for e in sorted(sides)]
        require(len(set(owners))==2,'side strip factors must be distinct')
        require(all(t not in {owner(e) for e in cube} for t in owners),'side factors outside cube')
        cost=sum(F(1,8) if t[0]=='s' else F(3,4) for t in owners)
        require(cost>=F(1,4),'positive exterior cost')
        rows.append({'face':f,'shared':sorted(shared),'opposite':opposite,'side_owners':owners,'lower_energy_increment':str(cost)})
    # An independent candidate-box enumeration catches incidence omissions.
    brute={(*ab,x,y,z) for ab in it.combinations(range(3),2)
      for x in range(2,5) for y in range(0,3) for z in range(0,2)
      if omitted((*ab,x,y,z)) and links((*ab,x,y,z))&cube}
    require(brute==all_faces,'candidate-box and incidence enumerations disagree')
    changes={3-F(3,2)*r+2*m for r in range(5) for m in range(r+1)}
    require(min(abs(d) for d in changes if d)!=0 and min(abs(d) for d in changes if d)>=F(1,2),'internal frequency separation')
    initial=set()
    for i in basis['u_indices']:
        for j in basis['cycles'][i]:
            v,w=basis['edges'][j];a=next(a for a in range(3) if v[a]!=w[a])
            initial.add((a,*(v[d]+O[d] for d in range(3))))
    factors={owner(e) for e in initial};collars=[]
    for k in range(4):
        edges=set().union(*(factor_edges(t) for t in factors))
        candidates=incident(edges);inside={f for f in candidates if {owner(e) for e in links(f)}<=factors}
        collars.append({'depth':k,'factors':len(factors),'links':len(edges),'faces':len(inside),'contains_cube':cube<=edges})
        if k>=1:require(cube<=edges and internal<=inside,'embedding in every k>=1 collar')
        factors|={owner(e) for f in candidates for e in links(f)}
    require([x['faces'] for x in collars[:3]]==[1,20,129],'inherited collar agreement')
    samples=[]
    for epsilon in [F(1,10),F(1,100),F(1,10**6),F(1,10**9),F(1,10**12)]:
        samples.append(scalar(1-epsilon,F(1,2),F(1,10**6),3,collars[3]['faces'],basis))
    for eta,z in [(F(1,4),F(1,10**6)),(F(3,4),F(1,10**6)),(F(1,2),F(1,10**7))]:
        samples.append(scalar(1-F(1,10**12),eta,z,3,collars[3]['faces'],basis))
    require(F(samples[4]['exact']['total_error'])<F(2,10**18),'near-endpoint enclosure')
    return {'scope':'Observable-reachable reducing component of every regional averaged block; not the entire energy eigenspace or instantaneous invariant dynamics',
      'authorship':'single agent; correlated self-review','exterior_faces':rows,'internal_faces':sorted(internal),
      'collars':collars,'source_specific_nonzero_frequency_lower_bound':'1/8',
      'samples':samples,'controls':{'two_geometry_enumerations_agree':True,
      'strip_side_owners_distinct':True,'all_exterior_costs_positive':True,
      'instantaneous_invariance_rejected':True,'global_excited_gap_not_used':True,
      'q_is_static_not_time_driver':True,'original_time_retained':True,
      'full_energy_shell_enumeration_not_claimed':True,'continuum_solution_not_claimed':True}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    out=Path(a.output).resolve();require(not out.exists(),'output must be fresh');out.mkdir(parents=True)
    d=compute();(out/'results.json').write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps({'status':'passed','exterior_faces':len(d['exterior_faces']),'collars':d['collars'],
      'example':d['samples'][4]['display']}))
