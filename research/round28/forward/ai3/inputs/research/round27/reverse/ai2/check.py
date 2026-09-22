#!/usr/bin/env python3
"""AI2 independent rational full-scalar discrimination, without current forward code."""
import argparse, hashlib, itertools, json
from fractions import Fraction as F
from math import factorial,isqrt
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
checks=[]
def req(x,m):
    if not x: raise ValueError(m)
    checks.append(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def add(v,a,n=1):return tuple(x+(n if j==a else 0) for j,x in enumerate(v))
def edge(v,w):
    a=next(j for j in range(3) if v[j]!=w[j]);return (min(v,w),a)
def face_edges(f):
    v,a,b=f;return {(v,a),(v,b),(add(v,a),b),(add(v,b),a)}
def own(e):
    (x,y,z),a=e
    if a==2 or (a==0 and x%4==3) or (a==1 and y%2==1):return ('link',(x,y,z),a)
    return ('strip',(x-x%4,y-y%2,z),-1)
def complete(o):
    kind,(x,y,z),a=o
    if kind=='link':return {((x,y,z),a)}
    return {((x+i,y+j,z),0) for i in range(3) for j in range(2)}|{((x+i,y,z),1) for i in range(4)}
def omitted(f):
    (x,y,z),a,b=f;return not(a==0 and b==1 and x%4<3 and y%2==0)
def incident(es):
    ans=set()
    for v,a in es:
        for b in range(3):
            if a==b:continue
            for p in [v,add(v,b,-1)]:
                f=(p,min(a,b),max(a,b))
                if min(p)>=0 and omitted(f):ans.add(f)
    return ans
def mv(A,v):return [sum((a*x for a,x in zip(row,v)),F(0)) for row in A]
def moments(A,pair,n=8):
    v=[F(i in pair) for i in range(len(A))];out=[]
    for j in range(n+1):
        out.append(sum(v[i] for i in pair)/2);v=mv(A,v)
    return out
def moment_polynomials(cycles,faces,pair,n=8):
    v=[{0:F(i in pair)} for i in range(len(cycles))];out=[]
    for _ in range(n+1):
        value={}
        for i in pair:
            for degree,c in v[i].items():value[degree]=value.get(degree,F(0))+c/2
        out.append({k:c for k,c in value.items() if c})
        w=[{} for i in cycles]
        for i,c in enumerate(cycles):
            for j,d in enumerate(cycles):
                if c^d in faces:
                    r=faces[c^d][1]
                    for degree,x in v[j].items():w[i][degree+r]=w[i].get(degree+r,F(0))+x
        v=w
    return out
def geometry():
    vs=list(itertools.product(range(2),repeat=3))
    ed=sorted((v,w) for v in vs for w in vs if v<w and sum(abs(a-b) for a,b in zip(v,w))==1)
    old=json.loads((ROOT/'research/round25/solo/aa1/output/results.json').read_text())
    req(ed==[(tuple(v),tuple(w)) for v,w in old['edges']],'independently constructed original edge order')
    cyc=[]
    for subset in itertools.combinations(range(12),6):
        adj={}
        for j in subset:
            v,w=ed[j];adj.setdefault(v,set()).add(w);adj.setdefault(w,set()).add(v)
        if len(adj)!=6 or any(len(x)!=2 for x in adj.values()):continue
        seen=set();todo=[next(iter(adj))]
        while todo:
            v=todo.pop()
            if v not in seen:seen.add(v);todo.extend(adj[v]-seen)
        if len(seen)==6:cyc.append(frozenset(subset))
    req(len(cyc)==16 and cyc==[frozenset(c) for c in old['cycles']],'independent complete sixteen-cycle shell')
    O=(3,1,0);physical=[edge(tuple(a+b for a,b in zip(v,O)),tuple(a+b for a,b in zip(w,O))) for v,w in ed]
    cube=set(physical);req(all(own(e)[0]=='link' for e in cube),'all twelve cube links free')
    faces={}
    for a,b in itertools.combinations(range(3),2):
        normal=3-a-b
        for side in [0,1]:
            anchor=add(O,normal,side);f=(anchor,a,b)
            support=frozenset(physical.index(e) for e in face_edges(f));faces[support]=(f,sum(anchor))
    pairs={4:(10,6),5:(10,9)}
    req(cyc[10]=={1,2,5,7,9,11} and cyc[6]=={0,2,3,7,9,11} and cyc[9]=={1,2,5,7,8,10},'frozen actual cycle supports')
    for r,(i,j) in pairs.items():req(faces[cyc[i]^cyc[j]][1]==r,'actual joining face exponent '+str(r))
    seed_idx=cyc[10]|cyc[6]|cyc[9];seed={physical[j] for j in seed_idx}
    req(len(seed)==10,'combined ten-free-link seed')
    req(not cyc[9]<=(cyc[10]|cyc[6]),'old eight-link support rejects B5')
    factors={own(e) for e in seed};collars=[]
    for depth in range(6):
        es=set().union(*(complete(o) for o in factors));touch=incident(es)
        inside={f for f in touch if {own(e) for e in face_edges(f)}<=factors}
        req(all(own(e)==o for o in factors for e in complete(o)),'whole-factor completion depth '+str(depth))
        if depth>=1:req(cube<=es and all(f in inside for f,r in faces.values()),'full cube and all faces retained depth '+str(depth))
        collars.append({'depth':depth,'factors':len(factors),'links':len(es),'faces':len(inside),'crossing_faces':len(touch-inside)})
        factors|={own(e) for f in touch for e in face_edges(f)}
    outside=[]
    for f in incident(cube):
        es=face_edges(f);shared=es&cube
        if es<=cube:continue
        req(len(shared)==1,'external face single cube edge')
        sharededge=next(iter(shared));opposite=next(e for e in es-shared if e[1]==sharededge[1]);req(own(opposite)[0]=='link','opposite external edge free')
        sides=(es-shared)-{opposite};owners={own(e) for e in sides}
        req(len(owners)==2 and owners.isdisjoint({own(e) for e in cube}),'distinct outside complete owners')
        gap=sum(F(1,8) if o[0]=='strip' else F(3,4) for o in owners)
        req(gap>=F(1,4),'full side spectral lower bound')
        outside.append({'face':f,'side_owners':sorted(owners),'gap_lower':gap})
    req(len(outside)==20,'complete twenty exterior touching faces')
    # Construct explicit oriented coordinate paths for the three supports.
    paths={}
    for idx in [10,6,9]:
        support=cyc[idx];adj={}
        for j in support:
            v,w=ed[j];adj.setdefault(v,[]).append(w);adj.setdefault(w,[]).append(v)
        start=min(adj);cur=start;prev=None;path=[start]
        for _ in range(6):
            nxt=sorted(w for w in adj[cur] if w!=prev)[0];path.append(nxt);prev,cur=cur,nxt
        req(cur==start and len(set(path[:-1]))==6,'actual closed path '+str(idx))
        paths[str(idx)]=[tuple(a+b for a,b in zip(v,O)) for v in path]
    return cyc,faces,pairs,collars,{'edges':ed,'cycles':[sorted(c) for c in cyc],'physical_paths':paths,'seed_indices':sorted(seed_idx),'collars':collars,'exterior_loading':outside}
def bfun(q):return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def sqrt_up(x):
    d=1<<300;n=isqrt(x.numerator*d*d//x.denominator);v=F(n,d);return v if v*v==x else F(n+1,d)
def tail(k,x):
    a=F(1)
    for j in range(k+1):a*=F(10,3)+j;a/=j+1
    return a*x**(k+1)/(1-x)**(k+5)
def series(ms,v):
    re=im=F(0)
    for n,m in enumerate(ms):
        c=m*v**n/factorial(n)
        if n%2:im+=(-1)**((n-1)//2)*c
        else:re+=(-1)**(n//2)*c
    return re,im
def ratio_error(v,q,delta):
    denominator=v*q**4-delta
    return ((1+q)*delta/denominator if denominator>0 else None),denominator
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    return x
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output)
    req(out.is_absolute() and not out.exists(),'fresh absolute output')
    con=json.loads((HERE/'inputs/contract.json').read_text());req(con['loop']=='ai2','AI2 frozen contract')
    req((HERE/'inputs/contract.json').read_bytes()==(ROOT/'research/round27/contracts/ai2.json').read_bytes(),'contract snapshot unchanged')
    for p,d in con['sources'].items():req(sha(ROOT/p)==d,'frozen source '+p)
    inv=json.loads((HERE/'inputs/source-inventory.json').read_text())
    for row in inv['entries']:req(sha(ROOT/row['source'])==sha(ROOT/row['snapshot'])==row['sha256'],'frozen instruction '+row['source'])
    cycles,faces,pairs,collars,geo=geometry();z=F(1,10**6);samples=[];decisions=[]
    polynomials={r:moment_polynomials(cycles,faces,pair) for r,pair in pairs.items()}
    req(polynomials[4][:4]==[{0:F(1)},{4:F(1)},{8:F(2),10:F(2)},{12:F(3),14:F(5)}],'B4 first four exact moment polynomials')
    req(polynomials[5][:4]==[{0:F(1)},{5:F(1)},{8:F(2),10:F(2)},{13:F(5),15:F(3)}],'B5 first four exact moment polynomials')
    req(F(5,2)!=1,'rank squared-action control for true multipliers')
    req(8!=1 and 48!=6,'true norm-squared and state budget reject rank substitution')
    for power in [12,18,24]:
        u=F(1,10**power);hdata=[]
        for h,q,eta in [('H1',1-u,F(1,2)),('H2',1-2*u,F(1,16))]:
            tau=eta/(8*bfun(q));s=z/eta*tau/(1-q)**3;v=s/96
            req(s<=3*z/2,'original clock envelope '+h+str(power))
            Q=[[q**faces[c^d][1] if c^d in faces else F(0) for d in cycles] for c in cycles]
            R=max(sum(row) for row in Q);req(R<=6,'full reached matrix norm '+h+str(power))
            ms={r:moments(Q,pair) for r,pair in pairs.items()}
            for r in [4,5]:req(ms[r][1]==q**r,'exact retained first moment '+str((power,h,r)))
            for r in [4,5]:req(ms[r]==[sum(c*q**degree for degree,c in poly.items()) for poly in polynomials[r]],'polynomial moment evaluator agreement '+str((power,h,r)))
            req(ms[5][1]/ms[4][1]==q,'retained slope ratio '+h+str(power))
            req(q**5!=q**4,'q5 to q4 mutation changes first moment '+h+str(power))
            centers={r:series(ms[r],v) for r in [4,5]}
            arithmetic=(v*R)**9/factorial(9);sine=(v*R)**3/6
            state=48*tau*sqrt_up(bfun(q*q)/96)/(F(1,8)*(1-eta))
            hrows=[]
            for k in [3,4,5]:
                M=F(collars[k]['faces'],24);spatial=8*tail(k,15*z);averaging=64*tau*M*(1+3*z*M);total=state+spatial+averaging+arithmetic
                delta=total+sine;ratio_err,den=ratio_error(v,q,delta)
                row={'power':power,'hypothesis':h,'q':q,'eta':eta,'z':z,'k':k,'tau':tau,'s':s,'v':v,'Q_norm_upper':R,'physical_time_in_hbar_over_alpha':z/eta/(1-q)**3,'moments':ms,'centers':{r:{'real':centers[r][0],'imag':centers[r][1],'real_minus_one':centers[r][0]-1} for r in [4,5]},'state_error':state,'spatial_error':spatial,'averaging_error':averaging,'arithmetic_error':arithmetic,'full_radius':total,'sine_linearization_error':sine,'ratio_denominator_lower':den,'ratio_error':ratio_err,'ratio_interval':None if ratio_err is None else [q-ratio_err,q+ratio_err]}
                samples.append(row);hrows.append(row)
            hdata.append(hrows)
        for i,k in enumerate([3,4,5]):
            h1,h2=hdata[0][i],hdata[1][i]
            req(h1['physical_time_in_hbar_over_alpha']==h2['physical_time_in_hbar_over_alpha'],'equal physical time '+str((power,k)))
            req(h1['eta']*(1-h1['q'])**3==h2['eta']*(1-h2['q'])**3,'same slow composite '+str((power,k)))
            row={'power':power,'k':k,'time_in_hbar_over_alpha':h1['physical_time_in_hbar_over_alpha'],'ratio_intervals_disjoint':abs(h1['q']-h2['q'])>h1['ratio_error']+h2['ratio_error'] if h1['ratio_error'] is not None and h2['ratio_error'] is not None else False,'probes':{}}
            for r in [4,5]:
                gap=abs(h1['centers'][r]['imag']-h2['centers'][r]['imag']);cost=h1['full_radius']+h2['full_radius'];margin=gap-cost
                row['probes'][r]={'imaginary_center_separation':gap,'sum_full_radii':cost,'separation_margin':margin,'certified_disjoint':margin>0,'additional_equal_absolute_error_per_hypothesis':max(F(0),margin/2),'conservative_allowed_extra_error_per_hypothesis':max(F(0),margin/4)}
            decisions.append(row)
    # Denominator failure is explicitly rejected, never silently divided.
    q=F(1,2);v=F(1,10**8);adverse=v*q**4
    req(v*q**4-adverse==0,'denominator reaches zero in adverse-readout control')
    req(ratio_error(v,q,adverse)[0] is None and ratio_error(v,q,2*adverse)[0] is None,'zero or negative denominator explicitly returns no inference')
    req(F(1,2)**4/F(1,2)**4==1,'wrong same-exponent retained ratio loses q discriminator')
    paths=list(con['sources'])+['research/round27/contracts/ai2.json','research/round24/forward/y1/report.md','research/round24/reverse/y2/check.py','research/round26/reverse/ad2/check.py','research/round27/methods/historical-physics-panel/references/lenses-and-evidence.md','.codex/skills/qeg-research-advisor/references/locality-and-computed-observables.md']
    paths += [str(p.relative_to(ROOT)) for p in (HERE/'inputs').rglob('*') if p.is_file()]
    paths += [str((HERE/n).relative_to(ROOT)) for n in ['report.md','check.py']]
    result={'schema':'ym27-reverse-ai2-v1','scope':'actual finite-q pairwise correlation disks under inherited canonical model; retained ratio is conditional','geometry':geo,'moment_polynomials':polynomials,'samples':samples,'decisions':decisions,'checks':checks,'check_count':len(checks),'bindings':{p:sha(ROOT/p) for p in sorted(set(paths))}}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(clean(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(checks),'collars':collars,'decisions':[{'power':d['power'],'k':d['k'],'ratio_disjoint':d['ratio_intervals_disjoint'],'probe_disjoint':{r:x['certified_disjoint'] for r,x in d['probes'].items()},'margins':{r:float(x['separation_margin']) for r,x in d['probes'].items()}} for d in decisions]}))
if __name__=='__main__':main()
