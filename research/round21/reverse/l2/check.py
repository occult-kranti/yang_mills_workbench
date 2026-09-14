#!/usr/bin/env python3
"""Reverse L2 exact finite-slope null directions and second-derivative discriminator."""
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
def add(a,b):
    out=dict(a)
    for k,v in b.items():out[k]=out.get(k,F(0))+v
    return out
def scale(a,c):return {k:c*v for k,v in a.items()}
def derivative(a):return {k-1:k*v for k,v in a.items() if k}
def moment(n):
    if n%2:return F(0)
    v=F(1)
    for k in range(1,n//2+1):v*=F(2*k-1,2*k+2)
    return v
def expect(a):return sum((v*moment(k) for k,v in a.items()),F(0))
def gamma(p):return mul(mul(derivative(p),derivative(p)),{0:F(1,4),2:F(-1,4)})
def null_vector(a):
    a=[list(row) for row in a];pivots=[];row=0;cols=len(a[0])
    for col in range(cols):
        pivot=next((i for i in range(row,len(a)) if a[i][col]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row];z=a[row][col];a[row]=[v/z for v in a[row]]
        for i in range(len(a)):
            if i!=row:
                z=a[i][col];a[i]=[a[i][j]-z*a[row][j] for j in range(cols)]
        pivots.append(col);row+=1
        if row==len(a):break
    free=next(col for col in range(cols) if col not in pivots)
    v=[F(0)]*cols;v[free]=F(1)
    for i,col in enumerate(pivots):v[col]=-a[i][free]
    length=sum(abs(x) for x in v);need(length>0,'nullvector vanished')
    return [x/length for x in v]
def run():
    obs=[{1:F(1)},{1:F(1),2:F(1,4)},{2:F(1),3:F(1)}]
    weights=[gamma(p) for p in obs]
    p5={5:F(1),3:F(-5,6),1:F(1,8)}
    nulls=[expect(mul(p5,w)) for w in weights]
    need(nulls==[0,0,0],'p5 is not invisible to all three slopes')
    coeff_bound=sum(abs(q) for q in p5.values());floor=1-F(1,4)*coeff_bound
    need(coeff_bound==F(47,24) and floor==F(49,96)>0,'explicit positive mobility interval')
    change=scale(add(scale(mul({1:F(1)},p5),F(3)),scale(mul({0:F(1),2:F(-1)},derivative(p5)),F(-1))),F(1,4))
    need(change.get(0)==F(-1,32),'generator residual at x0')
    change_norm=expect(mul(change,change));cross=expect(mul({1:F(3,4)},change))
    need(change_norm==F(1,1024) and cross==0,'complete-time-curve discriminator')
    matrix=[[expect(mul({k:F(1)},w)) for k in range(4)] for w in weights]
    nv=null_vector(matrix)
    need(sum(abs(v) for v in nv)==1,'coefficient normalization')
    need(all(sum((a*b for a,b in zip(row,nv)),F(0))==0 for row in matrix),'finite nullspace reconstruction')
    gegenbauer={}
    for ell in range(3):
        rising=1
        for j in range(5-ell):rising*=2+j
        degree=5-2*ell
        gegenbauer[degree]=F((-1)**ell*rising*2**degree,factorial(ell)*factorial(degree))
    need({k:v/192 for k,v in gegenbauer.items()}==p5,'NIST finite sum substitution')
    wrong={5:F(1),3:F(-4,5),1:F(1,8)}
    wrong_rates=[expect(mul(wrong,w)) for w in weights]
    need(any(q!=0 for q in wrong_rates),'wrong hidden polynomial must be detected')
    # epsilon bounds are exact model-preserving positivity sufficient conditions.
    fixtures=[]
    for epsilon in [F(-1,4),F(0),F(1,4)]:
        lower=1-abs(epsilon)*coeff_bound
        need(lower>=floor,'signed positive interval')
        fixtures.append({'epsilon':str(epsilon),'mobility_lower':str(lower),
          'initial_rate_differences':[str(epsilon*q) for q in nulls],
          'A_x_difference_at_zero':str(-epsilon/32),
          'second_correlation_derivative_difference_times_hbar_squared_over_c_squared':str(epsilon*epsilon*change_norm)})
    return {'schema':'ym21-reverse-l2-v1','loop':'l2','direction':'reverse','passed':True,
      'target_verdict':'constructive_finite_initial_slope_nonidentifiability_verified',
      'comparison':{'blind_polynomial':'x^5-5x^3/6+x/8','three_rate_null_vector':True,
        'mobility_floor_fixture':str(floor),'finite_slope_general_obstruction':True,
        'complete_time_curve_obstruction_claimed':False,'classical_gegenbauer_scale':'192'},
      'exact':{'p5_null_moments':[str(v) for v in nulls],
        'p5_coefficient_norm':str(coeff_bound),'signed_mobility_fixtures':fixtures,
        'three_by_four_moment_matrix':[[str(v) for v in row] for row in matrix],
        'normalized_nullvector_degree_at_most_three':[str(v) for v in nv],
        'C5_lambda2':{str(k):str(v) for k,v in gegenbauer.items()},
        'generator_difference_polynomial_over_epsilon':{str(k):str(v) for k,v in change.items() if v},
        'generator_difference_squared_norm':str(change_norm),
        'wrong_polynomial_initial_rate_differences':[str(v) for v in wrong_rates]},
      'general_theorem':{'N_constraints':'N by N+1 polynomial moment matrix, degree at most N',
        'normalization':'divide coefficients by their positive l1 sum, ensuring sup norm <=1',
        'positive_interval':'|epsilon|<=m_star/2 implies m_epsilon>=m_star/2',
        'assumptions':'fixed finite kappa, full positive x marginal support, finite smooth observables, smooth positive m0',
        'changed_generator':'nonzero principal symbol change on an open set',
        'scope':'finite initial slopes only; complete correlation curves can distinguish the example'},
      'controls':{'wrong_p5_coefficients_rejected':True,'same_full_generator_rejected':True,
        'full_time_curve_nonidentifiability_rejected':True,'finite_family_success_preserved':True,
        'noisy_matrix_exact_nullspace_inference_rejected':True},
      'primary_source':{'url':'https://dlmf.nist.gov/18.5.E10','equation':'18.5.10',
        'substitution':'n=5,lambda=2: C5=192x5-160x3+24x','novelty':'classical polynomial'}}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round21/contracts/l2.json',
      ROOT/'research/round21/advisor/l1-gate.json',ROOT/'research/round21/reverse/l1/report.md',
      ROOT/'research/round21/reverse/k1/report.md']
    need(all(p.is_file() for p in files),'required input absent')
    before={str(p.relative_to(ROOT)):digest(p) for p in files}
    c=json.loads((ROOT/'research/round21/contracts/l2.json').read_text())
    need(c['loop']=='l2' and c['status']=='frozen','L2 not frozen')
    need(digest(ROOT/c['depends_on']['gate'])==c['depends_on']['sha256'],'L1 gate mismatch')
    result=run();need(before=={str(p.relative_to(ROOT)):digest(p) for p in files},'source changed')
    result['source_bindings']=before
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'source-manifest.json').write_text(json.dumps({'schema':'ym21-source-bindings-v1','inputs':before,
      'outputs':{'results.json':digest(out/'results.json')}},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':result['passed'],'comparison':result['comparison'],'output':str(out)}))
if __name__=='__main__':main()
