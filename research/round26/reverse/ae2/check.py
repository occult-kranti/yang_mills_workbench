#!/usr/bin/env python3
import argparse,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def require(x,m):
    if x is not True:raise RuntimeError(m)
def star(b):return {b}|{tuple(b[i]+int(i==j) for i in range(3)) for j in range(3)}
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve();require(not out.exists(),'fresh output required')
    con=json.loads((ROOT/'research/round26/contracts/ae2.json').read_text())
    for rel,h in con['bindings'].items():require(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,'binding '+rel)
    Y=star((0,0,0));anchors=list(itertools.product(range(-2,3),repeat=3));cross=[b for b in anchors if star(b)&Y and b!=(0,0,0)]
    require(len(cross)==12 and all(len(star(b)&Y)==1 and len(star(b)|Y)==7 for b in cross),'entire interior crossing set')
    origin=[b for b in cross if min(b)>=0];require(len(origin)==3,'origin exception distinct')
    T=F(3);M=F(1,1000);z=208*M*T;beta=(24*M+2/T)/(1-M);Fz=(4-z)/(1-z)**2
    require(beta==F(2072,2997) and beta<F(7,10),'whole family source contraction')
    require(z==F(78,125) and z<1,'original weighted radius')
    require(16*Fz==F(844000,2209) and 16*Fz<383,'weighted family bound')
    # Exact polynomial filter moments on the two half-intervals.
    moments=[]
    for n in range(12):
        pm=2*T**n*(F(1,n+1)-F(1,n+2));hm=T**(n+1)*(F(1,n+1)-2*F(1,n+2)+F(1,n+3))
        require(pm==2*T**n/((n+1)*(n+2)),'normalized triangular moment')
        require(hm==2*T**(n+1)/((n+1)*(n+2)*(n+3)),'odd inverse absolute moment')
        moments.append({'n':n,'p_absolute_moment':str(pm),'h_absolute_moment':str(hm)})
    require(F(moments[0]['p_absolute_moment'])==1 and F(moments[0]['h_absolute_moment'])==T/3,'kernel normalization/inverse norm')
    cap=F(35,1664);required_T=2/(1-25*cap);max_T=1/(208*cap);bestknown_T=1/(192*cap)
    require(required_T==F(3328,789) and max_T==F(8,35) and required_T>bestknown_T>max_T,'original cap certificate incompatibility')
    require(M<F(1,441)<cap,'continuous feasible range diagnostic')
    rows=[]
    for tau in [F(0),F(1,7000),F(-1,7000),F(1,14000),F(-1,14000)]:
        m=7*abs(tau);zz=208*m*T;bb=(24*m+2/T)/(1-m)
        require(zz<1 and bb<F(7,10),'continuous subrange endpoint checks')
        rows.append({'tau':str(tau),'M':str(m),'weighted_series_parameter':str(zz),'operator_bound_over_r':None if tau==0 else str(bb),'actual_source_zero':tau==0})
    # Positive majorant cannot prove weighted contraction: n=0 already 64r*.
    first_two=32*(F(4,2)+7*z/F(6));require(first_two>64,'weighted contraction not inferred')
    paths=list(con['bindings'])+['research/round26/contracts/ae2.json','research/round26/contracts/ae2-freeze.json','research/round26/reverse/ae2/report.md','research/round26/reverse/ae2/check.py','research/round23/reverse/s2/report.md','research/round23/forward/s2/report.md','.codex/skills/qeg-research-advisor/references/newton-tesla-project-method.md']
    data={'schema':'ym26-reverse-result-v1','loop':'ae2','status':'accepted-restricted-coupling-weighted-summability','checks_passed':True,'T':'3','M_upper':'1/1000','family_operator_contraction':str(beta),'rooted_weight':'2^support_cardinality','residual_weighted_upper_over_rstar':str(16*Fz),'inverse_weighted_upper_over_rstar':str(16*T*Fz/3),'weighted_contraction_proved':False,'interior_crossings':12,'origin_crossings':3,'original_cap_duration_constraints':{'contraction_strict_lower':str(required_T),'reverse_radius_strict_upper':str(max_T),'best_inherited_radius_strict_upper':str(bestknown_T)},'kernel_moments':moments,'rows':rows,'source_inventory':{r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in sorted(set(paths))}}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
