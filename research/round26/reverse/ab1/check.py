#!/usr/bin/env python3
import argparse, hashlib, itertools, json
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
def require(value,message):
    if value is not True: raise RuntimeError(message)
def make_star(b):
    return {b}|{tuple(b[i]+int(i==j) for i in range(3)) for j in range(3)}
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    out=Path(args.output).resolve()
    require(not out.exists(),'output must be fresh')
    contract_path=ROOT/'research/round26/contracts/ab1.json';contract=json.loads(contract_path.read_text())
    for rel,digest in contract['bindings'].items(): require(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,'binding '+rel)
    cube=set(itertools.product(range(3),repeat=3));Y=make_star((0,0,0))
    retained={b:make_star(b) for b in cube if make_star(b)<=cube}
    crossings={b:s for b,s in retained.items() if s&Y and not s<=Y}
    require(len(retained)==8,'retained stars');require(set(crossings)=={(1,0,0),(0,1,0),(0,0,1)},'complete crossings')
    require(all(len(Y|s)==7 and len(Y&s)==1 for s in crossings.values()),'full supports')
    for s in crossings.values():
        union=Y|s;seen={next(iter(union))}
        for _ in union: seen|={q for q in union if any(sum(abs(q[i]-r[i]) for i in range(3))==1 for r in seen)}
        require(seen==union,'connected')
    rows=[]
    for tau in [F(0),F(5,1664),F(-5,1664),F(1,1664),F(-1,1664)]:
        M=7*abs(tau);coef=6*M/(1-M)
        require(1-M>0,'local gap')
        require(coef>=0,'nonnegative bound')
        require((coef==0)==(tau==0),'zero source coefficient')
        rows.append({'tau':str(tau),'M':str(M),'resonant_bound_over_r':str(coef)})
    cap=F(210,1629);require(cap<F(129,1000),'strict cap');require(F(rows[1]['resonant_bound_over_r'])==cap,'cap arithmetic')
    paths=list(contract['bindings'])+['research/round26/contracts/ab1.json','research/round26/reverse/ab1/report.md','research/round26/reverse/ab1/check.py','.codex/skills/qeg-research-advisor/references/newton-tesla-project-method.md','research/round25/inputs/aa1/newton-SKILL.md','research/round25/inputs/aa1/tesla-SKILL.md','research/round23/forward/s1/report.md']
    inventory={rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in sorted(set(paths))}
    result={'schema':'ym26-reverse-result-v1','loop':'ab1','status':'limited-parent-open','checks_passed':True,'actual_geometry':{'factors':27,'retained_stars':len(retained),'crossing_anchors':[list(x) for x in sorted(crossings)],'crossing_union_sizes':[7]*3},'actual_source_result':'all equal-energy blocks and full fixed-volume diagonal norm <=6Mr/(1-M); no exact block value claimed','rational_rows':rows,'models_not_identified':['canonical q','finite 18-vertex graph','continuum'],'source_inventory':inventory}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
if __name__=='__main__': main()
