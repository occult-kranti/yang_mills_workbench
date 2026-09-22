#!/usr/bin/env python3
import argparse,hashlib,itertools,math,json
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
    a,x,y,z=e;return ('s',4*(x//4),2*(y//2),z) if (a==0 and x%4<3) or (a==1 and y%2==0) else ('f',*e)
def factor_edges(o):
    if o[0]=='f':return {o[1:]}
    _,x,y,z=o;return {(0,x+j,y+k,z) for j in range(3) for k in range(2)}|{(1,x+j,y,z) for j in range(4)}
def incident(es):
    fs=set()
    for a,*v in es:
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
def matmul(A,B):return [[sum(A[i][k]*B[k][j] for k in range(len(A))) for j in range(len(B[0]))] for i in range(len(A))]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve();require(not out.exists(),'fresh output required')
    con=json.loads((ROOT/'research/round26/contracts/ad2.json').read_text())
    for rel,h in con['bindings'].items():require(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,'binding '+rel)
    old=json.loads((ROOT/'research/round25/solo/aa1/output/results.json').read_text());edges=[(tuple(v),tuple(w)) for v,w in old['edges']];cycles=[frozenset(x) for x in old['cycles']];u=old['u_indices'];require(u==[10,6],'frozen actual source indices')
    require(cycles[u[0]]=={1,2,5,7,9,11} and cycles[u[1]]=={0,2,3,7,9,11},'actual cycles')
    # Enumerate all six-edge degree-two connected cycle subsets, independently of stored list.
    allcycles=[];vertices=set(itertools.product(range(2),repeat=3))
    for c in itertools.combinations(range(12),6):
        deg={v:0 for v in vertices};adj={v:set() for v in vertices}
        for i in c:
            v,w=edges[i];deg[v]+=1;deg[w]+=1;adj[v].add(w);adj[w].add(v)
        occupied={v for v in vertices if deg[v]}
        if all(deg[v] in (0,2) for v in vertices):
            seen={next(iter(occupied))}
            for _ in occupied:seen|=set().union(*(adj[v] for v in seen))
            if seen==occupied:allcycles.append(frozenset(c))
    require(set(allcycles)==set(cycles) and len(cycles)==16,'complete cube shell')
    faces={frozenset(f['edges']):f['anchor_sum'] for f in old['faces']}
    A=[[int(c^d in faces) for d in cycles] for c in cycles];require(A==old['matrix_adjacency'],'actual adjacency rebuilt')
    I=[[int(i==j) for j in range(16)] for i in range(16)];A2=matmul(A,A);A4=matmul(A2,A2);poly=matmul(A,[[A4[i][j]-16*A2[i][j]+48*I[i][j] for j in range(16)] for i in range(16)])
    require(all(v==0 for row in poly for v in row),'full spectral polynomial')
    moments={}
    for name,inds in [('single',[u[0]]),('sum',u)]:
        v=[F(i in inds) for i in range(16)];ms=[]
        for j in range(7):
            ms.append(sum(v[i] for i in inds)/len(inds));v=[sum(A[i][k]*v[k] for k in range(16)) for i in range(16)]
        moments[name]=ms
    require(moments['single']==[1,0,2,0,16,0,160] and moments['sum']==[1,1,4,8,32,80,320],'full frozen-source moments')
    require(F(2,3)+F(1,4)+F(1,12)==1 and 4*F(1,4)+12*F(1,12)==2,'single squared spectrum')
    require(F(1,3)+F(1,2)+F(1,6)==1 and 4*F(1,2)+12*F(1,6)==4,'sum squared spectrum')
    # Full support cover, all eight U free factors.
    O=(3,1,0);initial=set()
    for j in cycles[u[0]]|cycles[u[1]]:
        v,w=edges[j];axis=next(i for i in range(3) if v[i]!=w[i]);initial.add((axis,*(v[i]+O[i] for i in range(3))))
    factors={owner(e) for e in initial};require(len(factors)==8 and all(o[0]=='f' for o in factors),'actual eight-factor cover')
    collars=[]
    for k in range(4):
        es=set().union(*(factor_edges(o) for o in factors));cand=incident(es);inside={f for f in cand if {owner(e) for e in links(f)}<=factors};collars.append({'depth':k,'faces':len(inside),'factors':len(factors),'links':len(es)});factors|={owner(e) for f in cand for e in links(f)}
    require([r['faces'] for r in collars]==[1,20,129,332],'complete original collars')
    k=3;z=F(1,10**6);eta=F(1,2);q=1-F(1,10**12);tau=eta/(8*budget(q));s=z/eta*tau/(1-q)**3;M=F(332,24);require(s<=3*z/2,'original clock envelope')
    coeff=F(1)
    for j in range(k+1):coeff*=F(8,3)+j;coeff/=j+1
    spatial_base=coeff*(15*z)**(k+1)/(1-15*z)**(k+4);dhat=tau*sqrt_upper(budget(q*q)/96)/(F(1,8)*(1-eta));baseavg=tau*M*(1+3*z*M)
    Q=[[q**faces[c^d] if c^d in faces else F(0) for d in cycles] for c in cycles];norm=max(sum(row) for row in Q)/96;require(norm<=F(1,16),'entire matrix norm bound')
    samples=[]
    for name,inds,norm2,avgcoef in [('single',[u[0]],4,48),('sum',u,8,64)]:
        v=[F(i in inds) for i in range(16)];re=F(0);im=F(0)
        for j in range(9):
            moment=sum(v[i] for i in inds)/len(inds);term=moment*(s/96)**j/math.factorial(j)
            if j%2:im+=(-1)**((j-1)//2)*term
            else:re+=(-1)**(j//2)*term
            v=[sum(Q[i][l]*v[l] for l in range(16)) for i in range(16)]
        arithmetic=(s*norm)**9/math.factorial(9);state=6*norm2*dhat;spatial=norm2*spatial_base;averaging=avgcoef*baseavg;total=state+spatial+averaging+arithmetic
        require(total<F(1,10**17),'full actual multiplication finite-q radius')
        displacement=1-re if name=='single' else im;require(displacement>total,'actual finite-q nonzero witness')
        samples.append({'observable':name,**{key:str(val) for key,val in {'real':re,'imag':im,'real_minus_one':re-1,'state_error':state,'spatial_error':spatial,'averaging_error':averaging,'arithmetic_error':arithmetic,'total_error':total,'witness_lower':displacement-total}.items()}})
    theta=z/84;require(theta-2*theta*theta>0 and theta*theta-F(2,3)*theta**4>0,'continuous endpoint nonzero at cap with monotone ratios')
    require(F(2+2+6,4)==F(5,2),'actual sum fourth moment');require(moments['sum'][2]!=moments['sum'][1]**2,'held-out rejects single phase')
    paths=list(con['bindings'])+['research/round26/contracts/ad2.json','research/round26/reverse/ad2/report.md','research/round26/reverse/ad2/check.py','research/round24/forward/y1/report.md','.codex/skills/qeg-research-advisor/references/newton-tesla-project-method.md']
    data={'schema':'ym26-reverse-result-v1','loop':'ad2','status':'accepted-two-wilson-scalars','checks_passed':True,'u_indices':u,'moments':{n:[str(v) for v in ms] for n,ms in moments.items()},'single_measure':{'0':'2/3','+2':'1/8','-2':'1/8','+2sqrt3':'1/24','-2sqrt3':'1/24'},'sum_measure':{'0':'1/3','+2':'3/8','-2':'1/8','+2sqrt3':'1/12+1/(8sqrt3)','-2sqrt3':'1/12-1/(8sqrt3)'},'observable_squared_norms':{'single':4,'sum':8},'collars':collars,'q':str(q),'physical_time_in_hbar_over_alpha':str(z/eta/(1-q)**3),'samples':samples,'rank_squared_action_control':{'rank':'1','single':'2','sum':'5/2'},'source_inventory':{r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in sorted(set(paths))}}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
