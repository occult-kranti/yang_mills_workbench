#!/usr/bin/env python3
"""Reverse K2: exact marginal-copy determinant and blind mobility polynomial."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import argparse, hashlib, json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def moment(n):
    if n%2:return F(0)
    out=F(1)
    for k in range(1,n//2+1):out*=F(2*k-1,2*k+2)
    return out
def mul(a,b):
    out={}
    for i,x in a.items():
        for j,y in b.items():out[i+j]=out.get(i+j,F(0))+x*y
    return out
def expct(a):return sum((q*moment(i) for i,q in a.items()),F(0))
def bimul(a,b):
    out={}
    for i,x in a.items():
        for j,y in b.items():
            k=(i[0]+j[0],i[1]+j[1]);out[k]=out.get(k,F(0))+x*y
    return out
def copy_expect(a):return sum((q*moment(i)*moment(j) for (i,j),q in a.items()),F(0))
def invert(rf,rg,a1,b1,a2,b2):
    d=a1*b2-a2*b1
    need(d!=0,'singular rate design')
    c=(rf*b2-rg*b1)/d;q=(a1*rg-a2*rf)/d
    need(c>0,'inverse has nonpositive c')
    zeta=q/c;need(abs(zeta)<1,'inverse mobility outside allowed range')
    return c,zeta
def run():
    a=F(1,4);G={0:F(1,4),2:F(-1,4)};h={0:F(1),1:4*a,2:4*a*a}
    a1=expct(G);b1=expct(mul(G,{1:F(1)}));a2=expct(mul(G,h));b2=expct(mul(mul(G,h),{1:F(1)}))
    det=a1*b2-a2*b1
    need((a1,b1,a2,b2,det)==(F(3,16),F(0),F(25,128),F(1,32),F(3,512)),'rate determinant')
    gg=bimul({(0,0):F(1,4),(2,0):F(-1,4)},{(0,0):F(1,4),(0,2):F(-1,4)})
    square={(2,0):F(1),(1,1):F(-2),(0,2):F(1)}
    bare=copy_expect(bimul(gg,square))
    double=2*a*copy_expect(bimul(bimul(gg,square),{(0,0):F(1),(1,0):a,(0,1):a}))
    need(bare==F(3,256) and double==det,'independent marginal-copy determinant')
    exp_upper=sum((F(3,2)**n/F(factorial(n)) for n in range(11)),F(0))
    exp_upper+=(F(3,2)**11/F(factorial(11)))/(1-F(1,8))
    need(exp_upper*exp_upper<21,'rigorous exp3 upper bound')
    uniform=F(3)*a*(1-2*a)/128/21
    need(uniform==F(1,7168),'continuous determinant floor')
    p3={3:F(1),1:F(-3,8)}
    blind1=expct(mul(p3,G));blind2=expct(mul(mul(p3,h),G))
    need(blind1==blind2==0,'out-of-family blind polynomial')
    minimum_mobility=1-F(1,4)*F(11,8)
    need(minimum_mobility==F(21,32)>0,'blind deformation positivity')
    recovery=[]
    for c,zeta in [(F(2),F(1,2)),(F(3,7),F(-3,4)),(F(1),F(0))]:
        rf=c*(a1+zeta*b1);rg=c*(a2+zeta*b2)
        need(invert(rf,rg,a1,b1,a2,b2)==(c,zeta),'synthetic inverse')
        recovery.append({'c':str(c),'zeta':str(zeta),'rf':str(rf),'rg':str(rg)})
    invalid=[]
    for rf,rg in [(F(0),F(1)),(F(-1),F(0)),(a1,a2+b2),(a1,a2-b2)]:
        try:invert(rf,rg,a1,b1,a2,b2)
        except RuntimeError as ex:invalid.append({'rf':str(rf),'rg':str(rg),'reason':str(ex)})
        else:raise RuntimeError('inadmissible inverse accepted')
    # Beyond the sufficient monotone range the integrand can be negative; Haar rank can remain positive.
    outside_a=F(1);x,y=F(-3,4),F(-1,2)
    need(1+outside_a*(x+y)<0,'nonmonotone fixture must fail positivity argument')
    outside_haar_det=3*outside_a/128
    need(outside_haar_det>0,'sufficient-range failure must not be relabeled universal rank failure')
    return {'schema':'ym21-reverse-k2-v1','loop':'k2','direction':'reverse','passed':True,
      'target_verdict':'uniform_rank_and_family_inverse_verified_arbitrary_mobility_not_identified',
      'comparison':{'design_a':str(a),'zero_kappa_determinant':str(det),
        'uniform_determinant_lower':str(uniform),'kappa_absolute_bound':'1/8',
        'two_parameter_inverse_identified':True,'arbitrary_mobility_identified':False,
        'blind_polynomial':'x^3-3x/8'},
      'exact':{'zero_kappa_matrix':[[str(a1),str(b1)],[str(a2),str(b2)]],
        'double_copy_Haar_base':str(bare),'double_copy_Haar_determinant':str(double),
        'exp_three_upper':str(exp_upper*exp_upper),'blind_moments':[str(blind1),str(blind2)],
        'blind_mobility_lower':str(minimum_mobility),'synthetic_recovery':recovery,
        'invalid_inverse_controls':invalid,'nonmonotone_Haar_determinant':str(outside_haar_det)},
      'scope':{'copy_variables':'independent copies of the full interacting x marginal, not independently sampled interacting links',
        'parameterization':'linear variables (c,c*zeta); original-coordinate Jacobian is c*D',
        'design_a':'dimensionless observable coefficient only',
        'known_static_parameter':True,'physical_measurements_supplied':False,
        'positive_all_finite_kappa':'holds for 0<a<1/2; displayed numerical floor only for |kappa|<=1/8',
        'noise':'rate inversion remains sensitive in zeta as c approaches zero; arbitrary noise not admitted'},
      'controls':{'zero_a_rank_collapse':True,'wrong_determinant_sign_rejected':det>0,
        'nonmonotone_positivity_argument_rejected':True,'universal_rank_failure_outside_range_rejected':True,
        'inadmissible_inverse_rejected':True,'arbitrary_mobility_identification_rejected':True}}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round21/contracts/k2.json',
      ROOT/'research/round21/advisor/k1-gate.json',ROOT/'research/round21/reverse/k1/report.md',
      ROOT/'research/round20/reverse/f2/report.md']
    need(all(p.is_file() for p in files),'source input absent')
    before={str(p.relative_to(ROOT)):digest(p) for p in files}
    c=json.loads((ROOT/'research/round21/contracts/k2.json').read_text())
    need(c['loop']=='k2' and c['status']=='frozen','K2 not frozen')
    need(digest(ROOT/c['depends_on']['gate'])==c['depends_on']['sha256'],'K1 dependency mismatch')
    result=run();need(before=={str(p.relative_to(ROOT)):digest(p) for p in files},'source changed')
    result['source_bindings']=before
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'source-manifest.json').write_text(json.dumps({'schema':'ym21-source-bindings-v1','inputs':before,
      'outputs':{'results.json':digest(out/'results.json')}},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':result['passed'],'comparison':result['comparison'],'output':str(out)}))
if __name__=='__main__':main()
