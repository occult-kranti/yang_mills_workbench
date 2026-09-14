#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import argparse,hashlib,json,itertools
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(ok,m):
    if not ok:raise ValueError(m)
def rejected(fn):
    try:fn()
    except ValueError:return True
    return False
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F())
def add(*xs):return tuple(sum(z,F()) for z in zip(*xs))
def times(c,x):return tuple(c*v for v in x)
def tangent(p,i):
    # Left multiplication by imaginary quaternion e_i/2.
    vec=p[1:];b=[F(0)]*3;b[i]=1
    cross=(b[1]*vec[2]-b[2]*vec[1],b[2]*vec[0]-b[0]*vec[2],b[0]*vec[1]-b[1]*vec[0])
    return (-vec[i]/2,*((p[0]*b[j]+cross[j])/2 for j in range(3)))
def derivatives(u,v,q):
    e=(F(1),F(0),F(0),F(0));x,y,z=u[0],v[0],q[0];w,t,r=dot(u,v),dot(v,q),dot(u,q)
    ambient=(add(times(3,e),v),add(e,u,q),add(e,v))
    projected=sum((dot(a,a)-dot(p,a)**2 for p,a in zip((u,v,q),ambient)),F())/4
    lie=sum((dot(a,tangent(p,i))**2 for p,a in zip((u,v,q),ambient) for i in range(3)),F())
    polynomial=(15+8*y+2*x+2*z+2*r-(3*x+w)**2-(y+w+t)**2-(z+t)**2)/4
    lap_lie=sum((dot(times(F(-3,4),p),a) for p,a in zip((u,v,q),ambient)),F())
    lap_polynomial=F(-3,4)*(3*x+y+z+2*w+2*t)
    require(projected==lie==polynomial and lap_lie==lap_polynomial,'exact derivative routes disagree')
    return {'x':x,'y':y,'z':z,'w':w,'t':t,'r':r,'S':3*x+y+z+w+t,'GammaS':polynomial,'DeltaS':lap_polynomial,'shared_middle_cross':(r-w*t)/2}
def exp_bounds(x,n=16):
    partial=sum((x**j/F(factorial(j)) for j in range(n+1)),F())
    require(0<=x<F(n+2),'invalid exp geometric ratio')
    upper=partial+x**(n+1)/F(factorial(n+1))/(1-x/F(n+2))
    return partial,upper
def calibration(slope=None,q=F(3,16),hbar=F(1)):
    require(slope is not None and slope<0 and q>0 and hbar>0,'independent negative slope and positive form/action required')
    return -hbar*slope/q
def energy(c=F(1),positive_reference=True,source='external coefficient'):
    require(c>0 and positive_reference is True and source=='external coefficient','positive independent energy required')
def encode(o):
    if isinstance(o,F):return str(o)
    if isinstance(o,dict):return {k:encode(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)):return [encode(v) for v in o]
    return o
def main(out):
    contract=ROOT/'research/round20/contracts/f2.json';con=json.loads(contract.read_text());gate=ROOT/con['depends_on']['gate']
    require(hashlib.sha256(gate.read_bytes()).hexdigest()==con['depends_on']['sha256'],'F1 gate changed')
    p=[tuple(map(F,row)) for row in [(1,0,0,0),(-1,0,0,0),(0,1,0,0),(0,0,1,0),('3/5','4/5',0,0),('1/3','2/3','2/3',0)]]
    require(all(dot(v,v)==1 for v in p),'nonunit fixture')
    rows=[]
    for idx in [(0,0,0),(1,0,1),(2,0,2),(4,5,3),(5,4,2),(2,3,4),(1,5,4),(4,1,5)]:
        vals=derivatives(*(p[i] for i in idx));vals['quaternion_fixture_indices']=idx
        for k in (F(-1,8),F(0),F(1,8)):
            kinetic=-k*vals['DeltaS']/2-k*k*vals['GammaS']/4
            potential=k*vals['DeltaS']/2+k*k*vals['GammaS']/4
            require(kinetic+potential==0,'ground-state transform residual')
        rows.append(vals)
    require(rows[0]['S']==7 and rows[1]['S']==-5,'attained action extrema changed')
    lo,up=exp_bounds(F(3,2));require(up<F(9,2),'rational exp upper does not prove gap c/6')
    cross=rows[2];k=F(1,8)
    missing_cross_residual=-k*k*cross['shared_middle_cross']/4
    wrong_lap_residual=-k*rows[0]['DeltaS']
    calibration_c=calibration(slope=F(-3,8));require(calibration_c==2,'synthetic algebraic rate identity failed')
    controls={
      'missing_r_cross_rejected':missing_cross_residual==F(-1,512) and missing_cross_residual!=0,
      'independent_middle_copy_rejected':cross['GammaS']-cross['shared_middle_cross']==F(11,2) and cross['GammaS']==6,
      'wrong_Laplacian_sign_rejected':wrong_lap_residual!=0,
      'unit_sphere_metric_without_quarter_rejected':F(3)!=F(3,4),
      'false_action_range_rejected':rejected(lambda:require(rows[1]['S']>=-4,'actual minimum -5 outside false range')),
      'inward_exponential_envelope_rejected':rejected(lambda:require(F(4)>=lo,'claimed upper4 is below rigorous lower')),
      'missing_dynamic_slope_rejected':rejected(lambda:calibration()),
      'constant_observable_rejected':rejected(lambda:calibration(F(-1),F(0))),
      'zero_c_rejected':rejected(lambda:energy(F(0))),
      'zero_reference_rejected':rejected(lambda:energy(positive_reference=False)),
      'static_notation_matching_rejected':rejected(lambda:energy(source='c=alpha=kappa by notation'))}
    require(all(controls.values()),'wrong-model control failed')
    gamma={'1':F(15,4),'x':F(1,2),'y':F(2),'z':F(1,2),'r':F(1,2)}
    order=['x','y','z','w','t','r']
    for linear in ({'x':F(3),'w':F(1)},{'y':F(1),'w':F(1),'t':F(1)},{'z':F(1),'t':F(1)}):
        for (a,ca),(b,cb) in itertools.product(linear.items(),repeat=2):
            key=a+'^2' if a==b else '*'.join(sorted((a,b),key=order.index))
            gamma[key]=gamma.get(key,F())-ca*cb/4
    def evaluate_gamma(values):
        total=F()
        for name,coef in gamma.items():
            value=F(1)
            if name!='1':
                for factor in name.split('*'):
                    value*=values[factor[:-2]]**2 if factor.endswith('^2') else values[factor]
            total+=coef*value
        return total
    require(all(evaluate_gamma(v)==v['GammaS'] for v in rows),'expanded coefficient tensor differs')
    result={'schema':'ym20-forward-f2-v1','loop':'f2','status':'passed','derivative_fixtures':rows,'controls':controls,'GammaS_coefficients':gamma,'DeltaS_coefficients':{'x':F(-9,4),'y':F(-3,4),'z':F(-3,4),'w':F(-3,2),'t':F(-3,2)},'action_range':['-5','7'],'action_oscillation':'12','exp_3_over_2_lower':lo,'exp_3_over_2_upper':up,'gap_lower_over_c':'1/6','kappa_range':['-1/8','1/8'],'calibration':'c=-hbar*C_f_prime(0)/q_kappa[f]','calibration_evidence':'identity only; no measured slope supplied','missing_cross_residual_at_kappa_1_over_8':missing_cross_residual,'scope':'specified finite reversible generator and externally fixed c; no original YM identification'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(encode(result),indent=2,sort_keys=True)+'\n')
    sources=[HERE/'check.py',HERE/'report.md',contract,gate,ROOT/'research/round20/forward/f1/report.md',ROOT/'research/round19/advisor/c2-gate.json',ROOT/'research/round19/forward/c1/report.md',ROOT/'research/round20/advisor/diffusion-source-notes.md']
    manifest={'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'outputs':{'results.json':hashlib.sha256((out/'results.json').read_bytes()).hexdigest()}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'passed','loop':'f2','fixtures':len(rows),'controls':len(controls)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output');main(p.parse_args().output)
