#!/usr/bin/env python3
import argparse,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def require(x,m):
    if x is not True:raise RuntimeError(m)
def star(b):return {b}|{tuple(b[i]+int(i==j) for i in range(3)) for j in range(3)}
def exp_upper(x,n=120):
    require(x>=0 and x<F(n+2),'positive Taylor radius');term=total=F(1)
    for j in range(1,n+1):term*=x/j;total+=term
    return total+term*x/(n+1)/(1-x/(n+2))
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve();require(not out.exists(),'fresh output required')
    con=json.loads((ROOT/'research/round26/contracts/ae1.json').read_text())
    for rel,h in con['bindings'].items():require(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,'binding '+rel)
    geometry=[];Y=star((0,0,0))
    for R in range(1,6):
        cube=set(itertools.product(range(R+2),repeat=3));inside={b:star(b) for b in cube if star(b)<=cube};boundary={b:star(b) for b in cube if star(b)&cube and not star(b)<=cube}
        require(len(boundary)==3*R*R+9*R+7,'complete boundary count')
        reachable=set(Y)
        for n in range(R):
            require(not any(s&reachable for s in boundary.values()),'no shorter source-boundary star chain')
            reachable|=set().union(*(s for s in inside.values() if s&reachable))
        require(any(s&reachable for s in boundary.values()),'radius chain reachable')
        geometry.append({'radius':R,'factors':len(cube),'crossing_stars':len(boundary)})
    # Interior star-incidence count, including repeated anchor, is <=16.
    anchors=list(itertools.product(range(-2,3),repeat=3));overlap=sum(bool(star(b)&Y) for b in anchors);require(overlap==13 and overlap<=16,'bounded transition count')
    rows=[]
    for tau in [F(0),F(5,1664),F(-5,1664)]:
        M=7*abs(tau);v=64*M;s=F(2);ex=exp_upper(v*v*s*s/2)
        for R in [20,32,40,48]:
            b=3*R*R+9*R+7;er=4*M*b*s*(1+v*s)*ex/F(2**R);kr=4*M*b*s*s*ex/F(2**R)
            if tau and R==40:require(er<F(2,10**7) and kr<F(1,10**7),'explicit collar precision');require(F(1042,1629)+2*er<F(2,3),'localized contraction')
            if tau==0:require(er==0 and kr==0,'zero source/boundary exception')
            rows.append({'tau':str(tau),'radius':R,'factors':(R+2)**3,'residual_approximation_over_r':str(er),'inverse_approximation_over_r':str(kr),'commutator_error_over_r':str(2*er)})
    # Explicit wrong-weight diagnostic: fixed diameter rate 1 cannot offset mu*R^3.
    mu=F(1,100);exponents=[mu*(R+2)**3-R for R in [10,20,40,80]];require(exponents[-1]>exponents[-2]>exponents[-3],'cardinality upper budget grows eventually')
    paths=list(con['bindings'])+['research/round26/contracts/ae1.json','research/round26/contracts/ae1-freeze.json','research/round26/reverse/ae1/report.md','research/round26/reverse/ae1/check.py','.codex/skills/qeg-research-advisor/references/newton-tesla-project-method.md']
    data={'schema':'ym26-reverse-result-v1','loop':'ae1','status':'accepted-all-time-collar-cardinality-open','checks_passed':True,'all_time_velocity':'64M','geometry_checks':geometry,'collar_certificates':rows,'cardinality_norm_certified':False,'source_reading':{'url':'https://arxiv.org/pdf/1410.8174','version':'v1','scope':'Section 2 strong calculus; Section 3 especially (71)-(73), unbounded onsite permitted; constants derived here'},'source_inventory':{r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in sorted(set(paths))}}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
