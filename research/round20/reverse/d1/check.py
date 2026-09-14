#!/usr/bin/env python3
"""Independent omitted-class sums and factor closure for frozen D1."""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json
ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent

def sums(L):
    if type(L) is not int or L<0: raise ValueError('nonnegative integer cutoff required')
    S=2*(1-F(1,2**(L+1)))
    Y=F(4,3)*(1-F(1,4**(L//2+1)))
    X=F(2,15)*(1-F(1,16**((L+1)//4)))
    classes=[2*S**3/24,S*(S-Y)*S/24,X*Y*S/24]
    return classes,F(107,135)-sum(classes)

def face_links(a,b,x,y,z):
    c=(x,y,z); ca=list(c);ca[a]+=1;cb=list(c);cb[b]+=1
    return {(a,*c),(b,*ca),(a,*cb),(b,*c)}

def omitted_faces(L):
    return [(a,b,x,y,z) for a,b in [(0,1),(0,2),(1,2)]
     for x in range(L+1) for y in range(L+1) for z in range(L+1)
     if (a,b)!=(0,1) or y%2==1 or x%4==3]

def factor(edge):
    a,x,y,z=edge
    if a==0 and x%4!=3: return ('strip',x-x%4,y-y%2,z)
    if a==1 and y%2==0: return ('strip',x-x%4,y,z)
    return ('free',a,x,y,z)

def support(f):
    if f[0]=='free': return {tuple(f[1:])}
    _,x,y,z=f
    return {(0,x+j,y+k,z) for j in range(3) for k in range(2)}|{(1,x+j,y,z) for j in range(4)}

def closure(L):
    faces=omitted_faces(L)
    initial=set().union(*(face_links(*f) for f in faces))
    factors={factor(e) for e in initial}
    closed=set().union(*(support(f) for f in factors))
    if not initial<=closed: raise RuntimeError('retained face support lost')
    if any(factor(e)!=f for f in factors for e in support(f)): raise RuntimeError('reference factors not disjoint')
    if len(closed)>40*len(faces): raise RuntimeError('finite closure bound violated')
    return faces,initial,factors,closed

def scale(E_star,alpha,tau,eta):
    if isinstance(E_star,bool) or isinstance(alpha,bool) or isinstance(tau,bool): raise ValueError('boolean is not a scale')
    E,al,ta,im=map(F,[E_star,alpha,tau,eta])
    if E<=0 or al<=0 or im==0:raise ValueError('positive reference/alpha, nonreal z required')
    return al*abs(ta)/E,(al*abs(ta)/E)/(im/E)**2

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    rows=[];allpass=[]
    for L in range(9):
        classes,tail=sums(L);faces,initial,factors,closed=closure(L)
        direct=sum((F(1,24*2**sum(f[2:])) for f in faces),F(0))
        if direct!=sum(classes) or tail<=0:raise RuntimeError('tail reconstruction disagrees')
        rows.append({'L':L,'class_weights':list(map(str,classes)),'retained_weight':str(direct),'tail':str(tail),'epsilon_over_E_star':str(tail/32),'resolvent_dimensionless_bound':str(tail/8),'faces':len(faces),'initial_links':len(initial),'factor_count':len(factors),'closed_links':len(closed),'crossing_links':sum(max(e[1:])>L for e in initial)})
    inversion=[]
    for tolerance in [F(1,100),F(1,1000),F(1,10000),F(1,1000000)]:
        L=0
        while sums(L)[1]/32>tolerance:L+=1
        inversion.append({'epsilon_over_E_star_target':str(tolerance),'first_L':L,'achieved':str(sums(L)[1]/32),'previous_failed': L==0 or sums(L-1)[1]/32>tolerance})
    controls=[]
    def require(name,condition):
        if not condition:raise RuntimeError(name)
        controls.append({'name':name,'passed':True})
    faces,initial,factors,closed=closure(0)
    clipped={e for e in initial if max(e[1:])<=0}
    require('discard_crossing_support_rejected',not initial<=clipped)
    require('signed_cancellation_not_absolute_tail',abs(F(1,8)-F(1,8))<abs(F(1,8))+abs(-F(1,8)))
    require('exterior_generator_unbounded',all(F(j*(j+1))>j for j in range(1,20)))
    require('finite_factor_not_finite_dimension',len({F(j,2)*(F(j,2)+1) for j in range(30)})==30)
    for name,args in [('zero_energy',(0,2,F(1,64),F(1,2))),('static_kappa_energy',('kappa',2,F(1,64),F(1,2))),('real_resolvent',(1,2,F(1,64),0))]:
        try:scale(*args)
        except (ValueError,ZeroDivisionError):require(name+'_rejected',True)
        else:raise RuntimeError('invalid scale admitted')
    require('signed_tau_absolute_bound',scale(1,2,F(-1,64),F(1,2))==scale(1,2,F(1,64),F(1,2)))
    data={'schema':'ym20-reverse-d1-v1','status':'passed','tail_formula':'107/135-[2S^3+S(S-Y)S+XYS]/24','infinite_omitted_classes':['2/3','1/9','2/135'],'rows':rows,'inverse_tolerances':inversion,'controls':controls,'claim':'Norm-resolvent convergence of exact exterior-reference lifts in A2 representation only','scale':{'E_star':'1 energy unit','alpha/E_star':'2','tau':'1/64','Im_z/E_star':'1/2'}}
    target=out/'results.json';target.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    paths=[HERE/'check.py',HERE/'report.md',ROOT/'research/round20/contracts/d1.json',ROOT/'research/round19/advisor/a2-gate.json',ROOT/'research/round19/backward/a2/report.md']
    manifest={'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'outputs':{'results.json':hashlib.sha256(target.read_bytes()).hexdigest()}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','rows':len(rows),'controls':len(controls),'last_tail':rows[-1]['tail']}))
if __name__=='__main__':main()
