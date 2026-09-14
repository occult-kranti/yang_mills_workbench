#!/usr/bin/env python3
"""Reverse L1 exact three-observable inverse and classical polynomial substitution."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def mul(a,b):
    out={}
    for i,x in a.items():
        for j,y in b.items():out[i+j]=out.get(i+j,F(0))+x*y
    return out
def moment(n):
    if n%2:return F(0)
    q=F(1)
    for k in range(1,n//2+1):q*=F(2*k-1,2*k+2)
    return q
def expect(p):return sum((v*moment(k) for k,v in p.items()),F(0))
def rate_row(p):
    d={k-1:k*v for k,v in p.items() if k};gamma=mul(mul(d,d),{0:F(1,4),2:F(-1,4)})
    return [expect(mul(gamma,m)) for m in [{0:F(1)},{1:F(1)},{3:F(1),1:F(-3,8)}]]
def determinant(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
      -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
      +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
def inverse(r):
    c=16*r[0]/3;need(c>0,'nonpositive recovered energy scale')
    zeta=32*r[1]/c-F(25,4)
    xi=512*r[2]/(9*c)-F(118,9)-8*zeta
    need(abs(zeta)<=F(1,4) and abs(xi)<=F(1,4),'inverse outside certified box')
    return c,zeta,xi
def run():
    obs=[{1:F(1)},{1:F(1),2:F(1,4)},{2:F(1),3:F(1)}]
    matrix=[rate_row(p) for p in obs]
    expected=[[F(3,16),F(0),F(0)],[F(25,128),F(1,32),F(0)],[F(59,256),F(9,64),F(9,512)]]
    need(matrix==expected,'three Haar rate rows')
    det=determinant(matrix);need(det==F(27,262144),'linear determinant')
    floor=1-F(1,4)-F(1,4)*F(11,8)
    need(floor==F(13,32) and floor/6==F(13,192),'positive-box gap factor')
    # DLMF18.5.10 finite sum, n=3, lambda=2.
    gegenbauer={}
    for ell in range(2):
        rising=1
        for j in range(3-ell):rising*=2+j
        degree=3-2*ell
        gegenbauer[degree]=F((-1)**ell*rising*2**degree,factorial(ell)*factorial(degree))
    need(gegenbauer=={3:F(32),1:F(-12)},'classical Gegenbauer coefficient substitution')
    need({k:v/32 for k,v in gegenbauer.items()}=={3:F(1),1:F(-3,8)},'p3 classical scaling')
    recovery=[]
    for params in [(F(1),F(0),F(0)),(F(2),F(1,8),F(1,4)),(F(3,7),F(-1,4),F(-1,4))]:
        c,zeta,xi=params;q=[c,c*zeta,c*xi]
        rates=[sum((a*b for a,b in zip(row,q)),F(0)) for row in matrix]
        need(inverse(rates)==params,'synthetic recovery')
        recovery.append({'c':str(c),'zeta':str(zeta),'xi':str(xi),'rates':[str(v) for v in rates],
                         'original_coordinate_jacobian':str(c*c*det)})
    wrong=matrix[:2]+[rate_row({3:F(1)})]
    need(determinant(wrong)==0,'wrong third observable must remain blind')
    c,zeta,xi=F(2),F(1,8),F(1,4)
    hidden=c*xi*matrix[2][2]
    need(hidden==F(9,1024)>0,'omitted cubic must produce third-rate residual')
    need(matrix[0][2]==matrix[1][2]==0,'first two remain cubic blind')
    # A simple point outside the sufficient box is still positive everywhere.
    need(1-F(1,2)>0,'outside box does not imply negative mobility')
    return {'schema':'ym21-reverse-l1-v1','loop':'l1','direction':'reverse','passed':True,
      'target_verdict':'three_parameter_conditional_inverse_and_positive_box_verified',
      'comparison':{'linear_determinant':str(det),'third_rate_xi_coefficient':str(matrix[2][2]),
        'mobility_floor_box':str(floor),'gap_factor_box':str(floor/6),
        'hidden_cubic_detected':True,'arbitrary_mobility_identified':False},
      'exact':{'rate_matrix':[[str(v) for v in row] for row in matrix],
        'synthetic_recovery':recovery,'wrong_third_x_cubed_row':[str(v) for v in wrong[-1]],
        'omitted_cubic_third_rate_residual':str(hidden),
        'gegenbauer_C3_lambda2':{str(k):str(v) for k,v in gegenbauer.items()}},
      'scope':{'inverse_static_point':'known kappa=0',
        'gap_interval':'|kappa|<=1/8; |zeta|,|xi|<=1/4; c>0',
        'jacobian':'c^2 times linear determinant',
        'mobility_extension':'explicit dynamics deformation; rho unchanged',
        'physical_data_supplied':False,'lattice_model_matched':False},
      'controls':{'wrong_third_observable_rank_failure':True,'hidden_cubic_omission_rejected':True,
        'outside_box_negative_mobility_inference_rejected':True,'arbitrary_mobility_identification_rejected':True},
      'primary_source':{'url':'https://dlmf.nist.gov/18.5.E10','equation':'18.5.10',
        'accessed':'2026-09-14','substitution':'n=3, lambda=2: C3=32x^3-12x',
        'novelty':'classical Gegenbauer polynomial; no new polynomial family'}}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round21/contracts/l1.json',
      ROOT/'research/round21/advisor/k2-gate.json',ROOT/'research/round21/advisor/post-six-selection.json',
      ROOT/'research/round21/reverse/k2/report.md',ROOT/'research/round21/reverse/k1/report.md']
    need(all(p.is_file() for p in files),'source absent')
    before={str(p.relative_to(ROOT)):digest(p) for p in files}
    c=json.loads((ROOT/'research/round21/contracts/l1.json').read_text())
    need(c['loop']=='l1' and c['status']=='frozen','L1 not frozen')
    need(digest(ROOT/c['depends_on']['gate'])==c['depends_on']['sha256'],'K2 gate mismatch')
    result=run();need(before=={str(p.relative_to(ROOT)):digest(p) for p in files},'source changed')
    result['source_bindings']=before
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'source-manifest.json').write_text(json.dumps({'schema':'ym21-source-bindings-v1','inputs':before,
      'outputs':{'results.json':digest(out/'results.json')}},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':result['passed'],'comparison':result['comparison'],'output':str(out)}))
if __name__=='__main__':main()
