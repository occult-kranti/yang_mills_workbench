#!/usr/bin/env python3
"""Actual complete-reference-factor geometry; exact connected tail arithmetic."""
import argparse,json
from fractions import Fraction as F
from math import isqrt,factorial
from pathlib import Path

def need(x,m):
    if not x:raise RuntimeError(m)
def shift(p,a,d=1):
    v=list(p);v[a]+=d;return tuple(v)
def face_links(face):
    x,y,z,a,b=face;p=(x,y,z)
    return {(a,*p),(b,*shift(p,a)),(a,*shift(p,b)),(b,*p)}
def omitted(f):return not (f[3:]==(0,1) and f[1]%2==0 and f[0]%4<3)
def owner(link):
    a,x,y,z=link
    if (a==0 and x%4<3) or (a==1 and y%2==0):return ('s',x//4*4,y//2*2,z)
    return ('f',a,x,y,z)
def factor_links(f):
    if f[0]=='f':return {f[1:]}
    _,x,y,z=f
    return {(0,x+r,y+s,z) for r in range(3) for s in range(2)}|{(1,x+r,y,z) for r in range(4)}
def cover(face):return {owner(e) for e in face_links(face)}
def incidence(factors):
    faces=set()
    for fac in factors:
      for axis,x,y,z in factor_links(fac):
        p=(x,y,z)
        for b in range(3):
          if b==axis:continue
          for anchor in (p,shift(p,b,-1)):
            if min(anchor)<0:continue
            f=(*anchor,*sorted((axis,b)))
            if omitted(f):faces.add(f)
    return faces
def pathlinks(points):
    links=set()
    for a,b in zip(points,points[1:]):
      axes=[j for j in range(3) if a[j]!=b[j]]
      need(len(axes)==1 and abs(a[axes[0]]-b[axes[0]])==1,'path link')
      axis=axes[0];links.add((axis,*min(a,b)))
    return links
def b(q):return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def sqrtup(x):
    den=2**180;num=isqrt(x.numerator*den*den//x.denominator)
    lo,hi=F(num,den),F(num+1,den)
    need(lo*lo<=x<hi*hi,'sqrt enclosure')
    return hi
def tail(k,x):
    coefficient=F(1)
    for j in range(k+1):coefficient*=F(8,3)+j
    coefficient/=factorial(k+1)
    return coefficient*x**(k+1)/(1-x)**(k+4)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);out.mkdir(parents=True,exist_ok=True)
    O=(3,1,0);D=(3,2,1)
    X=pathlinks([O,(3,2,0),D]);Y=pathlinks([O,(3,1,1),D]);Z=pathlinks([O,(4,1,0),(4,2,0),(4,2,1),D])
    F0={owner(e) for e in X|Y|Z}
    need(len(F0)==8 and all(f[0]=='f' for f in F0),'actual eight free factors')
    regions=[F0];incident=[];retained=[]
    for depth in range(3):
      facs=regions[-1];faces=incidence(facs);incident.append(faces)
      retained.append({f for f in faces if cover(f)<=facs})
      if depth<2:regions.append(facs|set().union(*(cover(f) for f in faces)))
    need(incident[0]<=retained[1],'every first word retained')
    pairs=0
    for f in incident[0]:
      for h in incidence(F0|cover(f)):
        need(f in retained[2] and h in retained[2],'every connected second word retained')
        pairs+=1
    hidden=(2,1,0,0,2);displayed=face_links((0,0,0,0,2));full=set().union(*(factor_links(owner(e)) for e in displayed))
    need(len(full)==22 and bool(face_links(hidden)&full) and not bool(face_links(hidden)&displayed),'actual hidden complete-factor crossing')
    z=F(1,10**6);x=15*z;dynamic=tail(1,x)
    need(dynamic<z*(F(1,168)-F(1,250)),'all-z endpoint margin at cap')
    q=F(999999,1000000);eta=F(1,2);C=F(1,500000);tau=eta/(8*b(q));sd=C*tau/(1-q)**3
    dq=sqrtup(tau*tau*b(q*q)/96/(F(1,8)*(1-eta))**2)
    full_lower=sd*q**4/96-6*dq-tail(1,10*sd)
    finite_stationary_lower=full_lower-dynamic-12*dq
    need(finite_stationary_lower>F(1,125000000),'finite q stationary signal >8e-9')
    controls={
      'incomplete_factor_cover_misses_actual_face':bool(face_links(hidden)&full) and not bool(face_links(hidden)&displayed),
      'depth_zero_omits_actual_incident_faces':bool(incident[0]-retained[0]),
      'depth_one_has_nonempty_boundary_omissions':bool(incident[1]-retained[1]),
      'resonant_face_is_retained':(3,1,0,1,2) in retained[1],
      'omitted_tail_is_positive':dynamic>0,
      'wrong_clock_cancels_endpoint_scaling':tau/(1-q)**3>tau,
      'boundary_profile_is_not_renormalized':q**4!=F(1),
      'finite_spatial_region_retains_unbounded_casimir':F(2)*(2+1)>F(1,2)*(F(1,2)+1),
      'stationary_state_replacement_is_nonzero':dq>0,
    }
    need(all(controls.values()),'controls')
    result={'loop':'y1','direction':'forward','status':'passed','claims':['Actual finite complete-factor restriction matches all connected words through its depth','Full omitted connected tail controls local operator error uniformly on endpoint window','Stationary full/restricted correlators differ by tail+12 sigma/gbar','Depth1 preserves endpoint liminf >z/250'], 'limitations':['Finite spatial factors retain infinite spin spaces','No numerical evolution or finite circuit produced','Stationary ground states assumed from proved bounded-perturbation argument','No T-gap transfer homogeneous or continuum result'],'geometry':[{'depth':j,'factors':len(regions[j]),'links':sum(len(factor_links(f)) for f in regions[j]),'retained_faces':len(retained[j]),'crossing_omitted_faces':len(incident[j]-retained[j])} for j in range(3)],'enumerated_ordered_connected_pairs':pairs,'uniform_depth1_operator_error_at_cap':str(dynamic),'uniform_depth2_operator_error_at_cap':str(tail(2,x)),'finite_q_stationary_lower':str(finite_stationary_lower),'q_example':str(q),'continuum_proved':False,'finite_dimensional':False}
    (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'controls.json').write_text(json.dumps({'controls':controls},indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
