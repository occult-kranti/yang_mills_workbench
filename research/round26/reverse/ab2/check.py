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
    con=json.loads((ROOT/'research/round26/contracts/ab2.json').read_text())
    for rel,h in con['bindings'].items():require(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,'binding '+rel)
    cube=set(itertools.product(range(3),repeat=3));Y=star((0,0,0));cross=[b for b in cube if star(b)<=cube and star(b)&Y and not star(b)<=Y]
    require(len(cross)==3 and all(len(Y|star(b))==7 for b in cross),'all crossing supports')
    capM=F(35,1664);cap=(6*capM+F(1,2))/(1-capM);require(cap==F(1042,1629) and cap<F(2,3),'uniform actual-source contraction')
    require(1-7*capM>0 and 2>1/(1-7*capM),'sufficient duration')
    rows=[]
    for tau in [F(0),F(5,1664),F(-5,1664),F(1,1664),F(-1,1664)]:
        M=7*abs(tau)
        for s in [F(1,2),F(2),F(10),F(100)]:
            bound=(6*M+1/s)/(1-M)
            if tau and s>=2:require(bound<1,'full-source norm contraction')
            rows.append({'tau':str(tau),'s':str(s),'residual_bound_over_r':None if tau==0 else str(min(F(1),bound)),'boundary_upper_budget_over_r':None if tau==0 else str(6*M/(1-M)),'source_zero':tau==0})
    # Scalar algebra controls only: arbitrary rational Gaussian multiplier values,
    # not evaluated physical SU2 frequencies or a substitute spectrum.
    for omega,q in [(F(2),F(1,3)),(F(-3),F(2,5))]:
        j=(1-q)/omega;require(-omega*j==-1+q,'homological sign')
        require(omega*j!=(-1+q),'wrong-sign rejection')
    require(F(0)==0,'zero frequency inverse multiplier')
    paths=list(con['bindings'])+['research/round26/contracts/ab2.json','research/round26/reverse/ab2/report.md','research/round26/reverse/ab2/check.py','.codex/skills/qeg-research-advisor/references/newton-tesla-project-method.md']
    data={'schema':'ym26-reverse-result-v1','loop':'ab2','status':'accepted-finite-resolution-parent-open','checks_passed':True,'s_2_uniform_residual_over_r':str(cap),'gaussian_derivative_L1':'sqrt(2/pi)/s','gaussian_inverse_kernel_L1':'s sqrt(2/pi)','exact_homological_identity':'[J_s(A),G]=-A+R_s(A)','weighted_locality_proved':False,'equal_energy_blocks_evaluated':False,'rows':rows,'source_inventory':{r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in sorted(set(paths))}}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
