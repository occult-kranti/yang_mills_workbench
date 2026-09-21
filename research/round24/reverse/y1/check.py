#!/usr/bin/env python3
"""Exact canonical complete-factor spatial collars and all-tail bounds."""
import argparse
from fractions import Fraction as F
import itertools
from math import isqrt
import json
from pathlib import Path

UNITS=((1,0,0),(0,1,0),(0,0,1))


def require(ok,name):
    if not ok: raise RuntimeError(name)


def add(a,b): return tuple(x+y for x,y in zip(a,b))


def edges(face):
    p,a,b=face
    return {(p,a),(add(p,UNITS[a]),b),(add(p,UNITS[b]),a),(p,b)}


def omitted(face):
    (x,y,z),a,b=face
    return not ((a,b)==(0,1) and y%2==0 and x%4<3)


def owner(edge):
    (x,y,z),axis=edge
    if axis==2 or (axis==0 and x%4==3) or (axis==1 and y%2==1):
        return ('free',(x,y,z),axis)
    return ('strip',(x-x%4,y-y%2,z),-1)


def links(factor):
    kind,p,axis=factor
    if kind=='free':return {(p,axis)}
    x,y,z=p
    return {((x+i,y+j,z),0) for i in range(3) for j in range(2)}|{((x+i,y,z),1) for i in range(4)}


def all_links(factors): return set().union(*(links(f) for f in factors))


def touching(factors):
    result=set()
    for p,axis in all_links(factors):
        for other in range(3):
            if other==axis:continue
            aa,bb=sorted((axis,other))
            for base in [p,add(p,tuple(-x for x in UNITS[other]))]:
                if min(base)<0:continue
                face=(base,aa,bb)
                if omitted(face): result.add(face)
    return result


def tail_after(depth,x):
    m=depth+1
    return x**m*((m+1)*(m+2)-2*m*(m+2)*x+m*(m+1)*x*x)/(2*(1-x)**3)


def profile(q):
    return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))


def root_upper(x):
    scale=10**50
    lo=F(isqrt(x.numerator*scale*scale//x.denominator),scale)
    hi=lo+F(1,scale)
    require(lo*lo<=x<=hi*hi,'rational root enclosure')
    return hi


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serial(v) for v in x]
    return x


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    initial_links={((3,1,0),1),((3,2,0),2),((3,1,0),2),((3,1,1),1),
                   ((3,1,0),0),((4,1,0),1),((4,2,0),2),((3,2,1),0)}
    seed={owner(e) for e in initial_links}
    require(len(seed)==8 and all(f[0]=='free' for f in seed),'actual eight free U1 factors')
    regions=[seed];face_sets=[set()]
    for depth in [1,2,3]:
        fs=touching(regions[-1]);nxt=regions[-1]|{owner(e) for f in fs for e in edges(f)}
        require(regions[-1]<=nxt and face_sets[-1]<=fs,'nested finite region')
        require(all(owner(e) in nxt for f in fs for e in edges(f)),'complete face cover')
        for factor in nxt:
            require(all(owner(e)==factor for e in links(factor)),'exact partition closure')
        regions.append(nxt);face_sets.append(fs)
    resonant=((3,1,0),1,2)
    require(resonant in face_sets[1],'actual U1 resonant face retained')
    # An order-two eligible face may be reached through a new complete factor.
    candidate=sorted(face_sets[2]-face_sets[1])[0]
    new_owners={owner(e) for e in edges(candidate)}&regions[1]
    predecessor=next(f for f in sorted(face_sets[1]) if {owner(e) for e in edges(f)}&new_owners)
    require(candidate not in face_sets[1] and predecessor in face_sets[1],
            'omitted boundary face needs second connected layer')
    displayed=set().union(*(edges(f) for f in face_sets[1]))|initial_links
    hidden_links=all_links(regions[1])-displayed
    require(hidden_links,'reference strips enlarge displayed face links')
    z=F(1,10**6);xcap=15*z
    tails={depth:tail_after(depth,xcap) for depth in [0,1,2,3]}
    require(tails[2]<F(34,10**15),'uniform depth-two tail below 3.4e-14')
    require(tails[2]<z/1000000<z/168,'endpoint signal not consumed')
    # Validate rational all-tail expression against geometric derivatives.
    for depth in range(5):
        xx=F(1,7)
        finite=sum(F((n+1)*(n+2),2)*xx**n for n in range(depth+1))
        require(tail_after(depth,xx)==1/(1-xx)**3-finite,'exact complete tail')
    q=1-F(1,10**8);eta=F(1,2);c=z/eta;tau=eta/(8*profile(q))
    s=c*tau/(1-q)**3;x=10*s
    require(x<=xcap,'original q-dependent clock bound')
    dq=root_upper(eta**2*profile(q*q)/(96*(1-eta)**2*profile(q)**2))
    count=len(face_sets[2]);dregion=tau*count/(3*(1-eta))
    spatial=tail_after(2,xcap);comparison=spatial+6*(dq+dregion)
    u2_lower=s*q**4/96-6*dq-F(44,9)*x*x/(1-x)**5
    finite_region_lower=u2_lower-comparison
    require(u2_lower>z/100 and finite_region_lower>z/101,
            'finite-q regional stationary endpoint remains positive')
    controls={
        'original-eight-factors-not-full-region':len(regions[2])>8,
        'complete-factor-enlargement-required':len(hidden_links)>0,
        'boundary-word-beyond-retained-depth-exists':candidate not in face_sets[1],
        'resonant-face-not-lost':resonant in face_sets[2],
        'finite-region-not-finite-Hilbert-dimension':any(f[0]=='strip' for f in regions[2]),
        'finite-q-state-error-not-zero':dq>0 and dregion>0,
        'q-one-not-substituted-into-original-clock':q<1 and c/(1-q)**3>1,
        'tail-not-finite-order-polynomial':tails[2]>F(10)*xcap**3,
    }
    for name,value in controls.items():require(value,name)
    rows=[{'depth':j,'factors':len(regions[j]),'physical_links':len(all_links(regions[j])),
           'retained_omitted_faces':len(face_sets[j]),'strip_factors':sum(f[0]=='strip' for f in regions[j])}
          for j in range(4)]
    results={
        'loop':'y1','direction':'reverse','status':'passed',
        'claims':[
            'Actual finite complete-factor collar matches all connected words through its depth',
            'Uniform original-clock full operator tail with a closed rational majorant',
            'Finite-region stationary state replacement with retained vanishing error',
            'Depth-two finite spatial dynamics retains a certified endpoint witness',
        ],
        'limitations':[
            'Finite factors retain infinite-dimensional Haar/strip Hilbert spaces',
            'No finite-spin or finite-dimensional evolution, trajectory or laboratory simulation computed',
            'Regional ground and local dynamics are defined, not numerically solved',
            'No canonical generator limit, T-gap transfer, homogeneous gap or continuum result',
        ],
        'geometry':{'layers':rows,'boundary_face':candidate,'predecessor_face':predecessor,
                    'hidden_reference_links':len(hidden_links)},
        'exact':{'z':z,'uniform_x_cap':xcap,'uniform_tails':tails,'q':q,
                 'actual_x_at_q':x,'full_state_distance_upper':dq,'regional_state_distance_upper':dregion,
                 'stationary_comparison_upper':comparison,'full_U2_lower':u2_lower,
                 'finite_region_endpoint_lower':finite_region_lower},
    }
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'results.json').write_text(json.dumps(serial(results),indent=2,sort_keys=True)+'\n')
    (args.output/'controls.json').write_text(json.dumps({'controls':controls},indent=2,sort_keys=True)+'\n')


if __name__=='__main__':main()
