#!/usr/bin/env python3
"""AI2 forward: exact physical geometry, full scalar disks, ratio obstruction."""
import argparse,hashlib,itertools,json,math,sys
from fractions import Fraction as F
from pathlib import Path
sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]; checks=[]
def require(ok,name):
    if not ok:raise ValueError(name)
    checks.append(name)
def clean(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [clean(x) for x in v]
    return v
def shift(v,a,d=1):return tuple(x+(d if j==a else 0) for j,x in enumerate(v))
def plaq(f):
    a,b,*v=f;v=tuple(v)
    return {(a,*v),(a,*shift(v,b)),(b,*v),(b,*shift(v,a))}
def omitted(f):
    a,b,x,y,z=f
    return not(a==0 and b==1 and y%2==0 and x%4<3)
def owner(e):
    a,x,y,z=e
    if (a==0 and x%4<3) or (a==1 and y%2==0):return ('s',4*(x//4),2*(y//2),z)
    return ('f',*e)
def owned(t):
    if t[0]=='f':return {t[1:]}
    _,x,y,z=t
    return {(0,x+i,y+j,z) for i in range(3) for j in range(2)}|{(1,x+i,y,z) for i in range(4)}
def touching(edges):
    fs=set()
    for a,*v in edges:
        for b in range(3):
            if b==a:continue
            for base in (tuple(v),shift(v,b,-1)):
                f=(*sorted((a,b)),*base)
                if min(base)>=0 and omitted(f):fs.add(f)
    return fs
def geometry():
    origin=(3,1,0);vertices=[tuple(origin[j]+v[j] for j in range(3)) for v in itertools.product(range(2),repeat=3)]
    edges=[]
    for v in vertices:
        for a in range(3):
            if v[a]==origin[a]:edges.append((a,*v))
    edges=sorted(edges);require(len(edges)==12 and all(owner(e)[0]=='f' for e in edges),'twelve actual free cube links')
    faces={}
    for a,b in itertools.combinations(range(3),2):
        other=3-a-b
        for side in (0,1):
            v=list(origin);v[other]+=side;f=(a,b,*v);faces[f]=plaq(f)
    cycles=[]
    for six in itertools.combinations(edges,6):
        adj={}
        for a,*v in six:
            v=tuple(v);w=shift(v,a);adj.setdefault(v,set()).add(w);adj.setdefault(w,set()).add(v)
        if len(adj)!=6 or any(len(x)!=2 for x in adj.values()):continue
        seen=set();todo=[next(iter(adj))]
        while todo:
            v=todo.pop()
            if v not in seen:seen.add(v);todo.extend(adj[v]-seen)
        if len(seen)==6:cycles.append(frozenset(six))
    require(len(cycles)==16,'complete sixteen six-cycle shell independently enumerated')
    def path(vs):
        result=set()
        for v,w in zip(vs,vs[1:]):
            a=next(i for i in range(3) if v[i]!=w[i]);base=min(v,w);result.add((a,*base))
        return result
    Xpath=[(3,1,0),(3,2,0),(3,2,1)]
    Zpath=[(3,1,0),(4,1,0),(4,2,0),(4,2,1),(3,2,1)]
    X=frozenset(path(Xpath)|path(Zpath));f4=(1,2,3,1,0);f5=(1,2,4,1,0)
    Y4=X^faces[f4];Y5=X^faces[f5]
    require(X in cycles and Y4 in cycles and Y5 in cycles,'both new coherent sources are actual six cycles')
    require(sum(f4[2:])==4 and sum(f5[2:])==5,'distinct anchor exponents four and five')
    require(len(X|Y4)==len(X|Y5)==8,'each actual multiplication support has eight free links')
    seed=set(X|Y4|Y5);require(len(seed)==10,'common seed has ten links')
    require(not Y5<=X|Y4,'old eight-link seed rejected for new source')
    # Each pair has a common length-four path; the other paths use independent Haar links.
    for label,Y in (('q4',Y4),('q5',Y5)):
        require(len(X&Y)==4 and len(X-Y)==len(Y-X)==2,'conditional Haar character independence '+label)
    cube=set(edges);exterior=touching(cube)-set(faces)
    require(len(exterior)==20,'all twenty exterior touching faces retained for inheritance check')
    exterior_rows=[]
    for f in sorted(exterior):
        es=plaq(f);shared=es&cube;require(len(shared)==1,'one shared cube link '+str(f))
        e=next(iter(shared));opp=next(t for t in es-shared if t[0]==e[0]);sides=es-shared-{opp};owners={owner(t) for t in sides}
        require(owner(opp)[0]=='f' and len(owners)==2,'complete external factor ownership '+str(f))
        require(not owners&{owner(t) for t in cube},'external sides outside cube '+str(f))
        cost=sum(F(1,8) if t[0]=='s' else F(3,4) for t in owners)
        require(cost>=F(1,4),'external spectral increment '+str(f))
        exterior_rows.append({'face':f,'side_owners':sorted(owners),'cost':cost})
    factors={owner(e) for e in seed};collars=[]
    for k in range(6):
        links=set().union(*(owned(t) for t in factors));inc=touching(links)
        inside={f for f in inc if {owner(e) for e in plaq(f)}<=factors}
        require(all(e in links for t in factors for e in owned(t)),'complete reference factors at depth '+str(k))
        if k>=1:require(cube<=links and set(faces)<=inside,'whole reached cube retained at depth '+str(k))
        collars.append({'k':k,'factors':len(factors),'links':len(links),'retained_faces':len(inside),'boundary_faces':len(inc-inside)})
        factors|={owner(e) for f in inc for e in plaq(f)}
    idx={c:i for i,c in enumerate(cycles)}
    flips={frozenset(es):sum(f[2:]) for f,es in faces.items()}
    return cycles,flips,[idx[X],idx[Y4],idx[Y5]],collars,{'edges':edges,'sources':{'X':sorted(X),'Y4':sorted(Y4),'Y5':sorted(Y5)},'seed':sorted(seed),'exterior':exterior_rows}
def budget(q):return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def sqrt_up(x):
    d=1<<320;n=math.isqrt(x.numerator*d*d//x.denominator);r=F(n,d)
    return r if r*r==x else F(n+1,d)
def tail(z,k):
    a=F(1)
    for j in range(k+1):a*=F(10,3)+j;a/=j+1
    x=15*z;return a*x**(k+1)/(1-x)**(k+5)
def centers(q,z,cycles,flips,indices):
    Q=[[q**flips[c^d] if c^d in flips else F(0) for d in cycles] for c in cycles]
    s=3*z*(1+q)**2*(1+q*q)/(2+5*q+5*q*q+6*q**3+3*q**4);v=s/96
    row=max(sum(r) for r in Q);require(row<=6 and s<=3*z/2,'retained operator and clock bounds '+str(q))
    result={}
    for exp,partner in ((4,indices[1]),(5,indices[2])):
        initial=[F(i in (indices[0],partner)) for i in range(len(cycles))];w=initial[:];mom=[];re=im=F(0)
        for n in range(9):
            m=sum(a*b for a,b in zip(initial,w))/2;mom.append(m);term=m*v**n/math.factorial(n)
            if n%2:im+=(-1)**((n-1)//2)*term
            else:re+=(-1)**(n//2)*term
            w=[sum(a*b for a,b in zip(r,w)) for r in Q]
        require(mom[0]==1 and mom[1]==q**exp,'actual coherent first moment q^'+str(exp))
        if q==1:require(mom[:7]==[1,1,4,8,32,80,320],'endpoint coherent moments '+str(exp))
        result[exp]={'real':re,'imag':im,'moments':mom,'sine_remainder':v**3*row**3/6}
    require(result[5]['moments'][1]/result[4]['moments'][1]==q,'exact retained slope ratio q')
    return result,v,(v*row)**9/math.factorial(9)
def ratio_interval(center4,center5,d4,d5):
    lower_den=center4-d4
    if lower_den<=0:return {'status':'denominator_failure','lower_denominator':lower_den}
    corners=[n/d for n in (center5-d5,center5+d5) for d in (lower_den,center4+d4)]
    return {'status':'bounded','lower_denominator':lower_den,'lower':min(corners),'upper':max(corners)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output)
    require(out.is_absolute() and not out.exists(),'fresh absolute output')
    inventory=json.loads((HERE/'inputs/source-inventory.json').read_text())
    for p,d in inventory.items():
        require(hashlib.sha256((HERE/'inputs'/p).read_bytes()).hexdigest()==d,'snapshot '+p)
        require(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==d,'source '+p)
    contract=json.loads((HERE/'inputs/research/round27/contracts/ai2.json').read_text())
    for p,d in contract['sources'].items():require(inventory.get(p)==d,'contract dependency '+p)
    cycles,flips,indices,collars,geo=geometry();z=F(1,10**6)
    centers(F(1),z,cycles,flips,indices)
    require(ratio_interval(F(1),F(1),F(2),F(2))['status']=='denominator_failure','nonpositive denominator returns no inference')
    signed=ratio_interval(F(2),F(-1),F(1),F(2))
    require(signed['lower']==-3 and signed['upper']==1,'signed numerator interval uses all corner quotients')
    require(F(1,2)**5/F(1,2)**4!=1,'q5 replaced by q4 loses q discriminator')
    fourth=(F(2)+6*F(1)*F(1)+F(2))/4
    require(fourth==F(5,2),'independent Haar fourth moment of coherent multiplication')
    require(fourth-1==F(3,2)>0,'rank loading identity B squared Omega equals Omega rejected')
    require(F(4)**2/2==8>1,'identity-holonomy norm square rejects norm-one multiplier budget')
    rows=[];displays=[]
    for power in (12,18,24):
        u=F(1,10**power);candidates=[(1-u,F(1,2)),(1-2*u,F(1,16))]
        data=[]
        for q,eta in candidates:
            cc,v,arithmetic=centers(q,z,cycles,flips,indices);tau=eta/(8*budget(q))
            dhat=tau*sqrt_up(budget(q*q)/96)/(F(1,8)*(1-eta))
            data.append({'q':q,'eta':eta,'v':v,'tau':tau,'dhat':dhat,'centers':cc,'arithmetic':arithmetic,'physical_time':z/eta/(1-q)**3})
        require(data[0]['physical_time']==data[1]['physical_time'],'equal original physical time hypotheses u=1e-'+str(power))
        for k in (3,4,5):
            N=collars[k]['retained_faces'];M=F(N,24);pair=[]
            for d in data:
                state=48*d['dhat'];spatial=8*tail(z,k);averaging=64*d['tau']*M*(1+3*z*M)
                radius=state+spatial+averaging+d['arithmetic']
                require(state>0 and spatial>0 and averaging>0,'nonzero complete state spatial and exterior-loading budgets')
                # Finite-time ratio inference from full measurements y4,y5: error contains physical disk and sine remainder.
                err4=radius+d['centers'][4]['sine_remainder'];err5=radius+d['centers'][5]['sine_remainder']
                require(d['v']*d['q']**5>err5,'positive numerator condition for displayed simple ratio formula')
                ratio=ratio_interval(d['v']*d['q']**4,d['v']*d['q']**5,err4,err5)
                if ratio['status']=='bounded':require(ratio['lower']<=d['q']<=ratio['upper'],'complete finite-time ratio covers true q')
                pair.append({'q':d['q'],'eta':d['eta'],'physical_time_in_hbar_over_alpha':d['physical_time'],'v':d['v'],'centers':d['centers'],'state_error':state,'spatial_error':spatial,'averaging_error':averaging,'arithmetic_error':d['arithmetic'],'radius':radius,'ratio':ratio})
            separation={}
            for exp in (4,5):
                distance=abs(pair[0]['centers'][exp]['imag']-pair[1]['centers'][exp]['imag']);margin=distance-pair[0]['radius']-pair[1]['radius']
                separation[exp]={'imaginary_center_distance':distance,'disk_sum':pair[0]['radius']+pair[1]['radius'],'signed_margin':margin,'disjoint':margin>0,'additional_equal_absolute_error_tolerance':max(F(0),margin/2)}
            rr=[p['ratio'] for p in pair]
            ratio_disjoint=all(x['status']=='bounded' for x in rr) and (rr[0]['upper']<rr[1]['lower'] or rr[1]['upper']<rr[0]['lower'])
            rows.append({'u':u,'power':power,'z':z,'k':k,'N_k':N,'hypotheses':pair,'scalar_discrimination':separation,'simple_ratio_intervals_disjoint':ratio_disjoint})
            displays.append({'power':power,'k':k,'N_k':N,'time':float(data[0]['physical_time']),'radius1':float(pair[0]['radius']),'radius2':float(pair[1]['radius']),'q4_distance':float(separation[4]['imaginary_center_distance']),'q4_margin':float(separation[4]['signed_margin']),'q5_distance':float(separation[5]['imaginary_center_distance']),'q5_margin':float(separation[5]['signed_margin']),'ratio_disjoint':ratio_disjoint})
    bindings=dict(inventory)
    for p in ('check.py','report.md','inputs/source-inventory.json'):bindings[str((HERE/p).relative_to(ROOT))]=hashlib.sha256((HERE/p).read_bytes()).hexdigest()
    result={'schema':'ym27-forward-ai2-v1','geometry':geo,'indices':indices,'collars':collars,'seed_factor_count':10,'tail_parameter':'10/3','tail_exponent':'k+5','coherent_fourth_moment':fourth,'rank_loading_identity_defect_squared':fourth-1,'rows':rows,'display_only':displays,'checks':checks,'checks_count':len(checks),'bindings':bindings,'scope':'Actual full connected scalar disks at specified common physical times; pairwise tests and failed simple-ratio certificates only'}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(clean(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','checks':len(checks),'collars':collars,'display':displays},indent=2))
if __name__=='__main__':main()
