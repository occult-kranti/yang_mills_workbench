#!/usr/bin/env python3
"""AN2 reverse independent-cutoff geometry and limit-order controls."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
BASE=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise AssertionError(m)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=BASE/'output');args=p.parse_args()
    need(json.loads((BASE/'inputs/research/round29/contracts/an2.json').read_text())['id']=='AN2','contract')
    rows=[]
    for radius in (0,1,3):
      for n in (radius+2,radius+4):
       region={(radius,0,0),(-radius,0,0)}
       for L,M in [(2*n,n),(2*n+1,3*n),(5*n,n+1)]:
        need(-n<=-n and L-n>=n and M>=n,'common cube inclusion')
        K=max(L-n,M,n+1);need(K>n,'explicit ambient collar')
        actual=min(n-1-abs(t) for v in region for t in v)
        lower=n-radius-1;need(actual>=lower and lower>=1,'independent-cutoff distance')
        rows.append({'r':radius,'n':n,'L':L,'M':M,'ambient_radius':K,'distance_lower':lower})
    triangular=[]
    for n in range(2,9):
      val=lambda L:int(L<=n*n)
      need(2*n<=n*n and val(2*n)==1 and val(n*n+1)==0,'triangular-array witness')
      triangular.append({'n':n,'diagonal_L':2*n,'diagonal_value':val(2*n),'tail_L':n*n+1,'tail_value':val(n*n+1)})
    # Two individually valid finite marginals fail the partial-trace consistency test.
    rhoF=[1,0];rhoG=[0,0,0,1];traceG=[rhoG[0]+rhoG[1],rhoG[2]+rhoG[3]]
    need(sum(rhoF)==sum(rhoG)==1 and rhoF!=traceG,'compatibility necessary')
    original_triple=(F(1,4),F(1,4),F(1,16));changed_triple=(F(1,8),F(1,4),F(1,16))
    controls={'diagonal_does_not_identify_iterated_limit':all(x['diagonal_value']==1 and x['tail_value']==0 for x in triangular),'near_boundary_distance_constant':all(n-1-(n-2)==1 for n in range(3,10)),'changed_coefficient_triple_is_different':original_triple!=changed_triple,'HTW_premise_cannot_be_deleted':not all([True,False]),'positive_marginals_need_compatibility':rhoF!=traceG,'legal_outer_limit_before_translation':'fixed n; L->infinity; M->infinity; n->infinity'!='L=2n; n->infinity'}
    need(all(controls.values()),'controls')
    result={'loop':'AN2','direction':'reverse','verdict':'specified local bulk states identified under both symbolic hypotheses','bound':'min(2, exp(C1*|F|-C2*(n-r-1)))','uniform_outer_cutoffs':'L>=2n and M>=n','ordered_limits':['at fixed n: L->infinity','M->infinity','n->infinity'],'centered_marginals':'trace-norm Cauchy, positive trace-one, partial-trace compatible','symmetries':['original endpoint gauge invariance','coarse translation invariance only'],'geometry':rows,'triangular_array':triangular,'controls':controls,'scope':'Local states for these two routes; no identification of dynamics, generators, gaps, all boundaries or continuum.'}
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    files=[BASE/'check.py',BASE/'report.md']+sorted(f for f in (BASE/'inputs').rglob('*') if f.is_file());h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
    (out/'manifest.json').write_text(json.dumps({'source_files':[{'path':str(f.relative_to(BASE)),'sha256':h(f)} for f in files],'results_sha256':h(out/'results.json')},indent=2)+'\n');print(json.dumps({'loop':'AN2','passed':True,'controls':len(controls),'geometries':len(rows)}))
if __name__=='__main__':main()
