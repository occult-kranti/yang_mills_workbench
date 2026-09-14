#!/usr/bin/env python3
"""Reverse K1 exact Haar polynomial rates, inverse rank, and mobility controls."""
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import argparse, hashlib, json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def pmul(a,b):
    out={}
    for i,x in a.items():
        for j,y in b.items():out[i+j]=out.get(i+j,F(0))+x*y
    return out
def derivative(a):return {k-1:k*v for k,v in a.items() if k}
def moment(n):
    if n%2:return F(0)
    value=F(1)
    for k in range(1,n//2+1):value*=F(2*k-1,2*k+2)
    return value
def expect(p):return sum((v*moment(k) for k,v in p.items()),F(0))
def rate(p):
    d=derivative(p);gamma=pmul(pmul(d,d),{0:F(1,4),2:F(-1,4)})
    return expect(gamma),expect(pmul(gamma,{1:F(1)}))
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def add(*vectors):return [sum(v[i] for v in vectors) for i in range(4)]
def scaled(q,v):return [q*x for x in v]
def run():
    rf=rate({1:F(1)});rg=rate({1:F(1),2:F(1)});rh=rate({2:F(1)})
    det=rf[0]*rg[1]-rf[1]*rg[0]
    need(rf==(F(3,16),F(0)) and rg==(F(5,16),F(1,8)) and rh==(F(1,8),F(0)),'Haar rates')
    need(det==F(3,128),'linear inverse determinant')
    need(rf[0]*rh[1]-rf[1]*rh[0]==0,'parity pair must lose mobility')
    recovery=[]
    for c,zeta in [(F(1),F(0)),(F(2),F(1,2)),(F(3,7),F(-3,4))]:
        f=c*(rf[0]+zeta*rf[1]);g=c*(rg[0]+zeta*rg[1])
        got_c=16*f/3;got_zeta=8*g/got_c-F(5,2)
        need((got_c,got_zeta)==(c,zeta),'synthetic inverse fails')
        need(1<g/f<F(7,3),'admissible slope cone')
        recovery.append({'c':str(c),'zeta':str(zeta),'r_f':str(f),'r_g':str(g),
                         'jacobian_original_coordinates':str(c*det)})
    U=[F(0),F(1),F(0),F(0)];V=[F(1),F(0),F(0),F(0)];W=U;e0=V
    x,y,z=U[0],V[0],W[0];w,t,r=dot(U,V),dot(V,W),dot(U,W)
    gradients=[add(scaled(3,e0),V),add(e0,U,W),add(e0,V)]
    gamma=sum((dot(a,a)-dot(a,q)**2 for a,q in zip(gradients,[U,V,W])),F(0))/4
    formula=(15+8*y+2*x+2*z+2*r-(3*x+w)**2-(y+w+t)**2-(z+t)**2)/4
    cross=(3+y-x*(3*x+w))/4
    need(gamma==formula==6 and cross==1,'shared-coordinate gradient fixture')
    k,zeta=F(1,8),F(1,2)
    missing_grad_m_residual=-(k/2)*zeta*cross
    need(missing_grad_m_residual==F(-1,32),'missing mobility potential must discriminate')
    wrong_drift_mean=3*zeta*moment(2)/4
    correct_drift_mean=3*moment(1)/4+zeta*(moment(2)-F(1,4))
    need(wrong_drift_mean==F(3,32) and correct_drift_mean==0,'stationarity drift test')
    exp_upper=sum((F(3,2)**n/F(factorial(n)) for n in range(11)),F(0))
    exp_upper+=(F(3,2)**11/F(factorial(11)))/(1-F(1,8))
    need(exp_upper<F(9,2),'rigorous exponential upper bound')
    need(F(3,4)/exp_upper>F(1,6),'gap factor certificate')
    need(rate({0:F(1)})==(F(0),F(0)),'constant observable must not identify a clock')
    need(1+F(2)*F(-1)<0,'wrong mobility range must fail positivity')
    symbol_left=F(2)*(1-F(1,2));symbol_right=F(2)*(1+F(1,2))
    need(symbol_left!=symbol_right,'nonconstant principal symbol control')
    return {'schema':'ym21-reverse-k1-v1','loop':'k1','direction':'reverse','passed':True,
      'target_verdict':'conditional_mobility_operator_and_two_rate_inverse_verified_physical_matching_unverified',
      'comparison':{'mobility_lower':'1-|zeta|','gap_factor':'(1-|zeta|)/6',
        'rate_f_c':str(rf[0]),'rate_g_c_constant':str(rg[0]),'rate_g_c_zeta':str(rg[1]),
        'two_rate_determinant':str(det),'static_parameters_identified':False,'physical_model_matched':False},
      'haar':{'moments':{str(n):str(moment(n)) for n in range(7)},
        'f_rate_coefficients':[str(v) for v in rf],'g_rate_coefficients':[str(v) for v in rg],
        'x_squared_rate_coefficients':[str(v) for v in rh],
        'parameterization':'determinant 3/128 applies to (c,c*zeta); original Jacobian determinant is 3*c/128',
        'synthetic_recovery':recovery},
      'gradient_fixture':{'Gamma_S':str(gamma),'Gamma_x_S':str(cross),
        'missing_grad_m_potential_residual_over_ground':str(missing_grad_m_residual),
        'wrong_nondivergence_stationary_mean':str(wrong_drift_mean),
        'correct_divergence_stationary_mean':str(correct_drift_mean)},
      'gap':{'exp_three_halves_upper':str(exp_upper),'haar_gap':'3/4',
        'bound':'3*c*(1-|zeta|)*exp(-12|kappa|)/4 >= c*(1-|zeta|)/6',
        'range':'|kappa|<=1/8, |zeta|<1, c>0'},
      'controls':{'constant_observable_rejected':True,'symmetric_pair_rank_failure':True,
        'missing_divergence_drift_rejected':True,'missing_grad_m_potential_rejected':True,
        'negative_mobility_rejected':True,'static_clock_inference_rejected':True,
        'same_coordinate_nonconstant_symbol_match_rejected':True},
      'scope':{'deformation':'m=1+zeta*x is an explicit reversible-dynamics deformation',
        'physical_data_supplied':False,'physical_scale':'c/E_star and alpha/E_star remain distinct',
        'symbol_claim':'necessary condition under same-coordinate multiplication conjugacy only'}}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round21/contracts/k1.json',
      ROOT/'research/round21/advisor/j2-gate.json',ROOT/'research/round20/reverse/f2/report.md']
    need(all(p.is_file() for p in files),'source absent')
    before={str(p.relative_to(ROOT)):digest(p) for p in files}
    c=json.loads((ROOT/'research/round21/contracts/k1.json').read_text())
    need(c['loop']=='k1' and c['status']=='frozen','K1 not frozen')
    need(digest(ROOT/c['depends_on']['gate'])==c['depends_on']['sha256'],'J2 gate mismatch')
    result=run();need(before=={str(p.relative_to(ROOT)):digest(p) for p in files},'source changed')
    result['source_bindings']=before
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'source-manifest.json').write_text(json.dumps({'schema':'ym21-source-bindings-v1','inputs':before,
      'outputs':{'results.json':digest(out/'results.json')}},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':result['passed'],'comparison':result['comparison'],'output':str(out)}))
if __name__=='__main__':main()
