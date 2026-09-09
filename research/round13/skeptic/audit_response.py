"""Independent exact series launch and alternative linear-ODE verification."""
from pathlib import Path
from fractions import Fraction as Q
from math import factorial
import argparse, csv, hashlib, importlib.util, json, math
import numpy as np
from scipy.integrate import solve_ivp
from independent_oracle import bessel_mean_interval, haar_tilt_interval, haar

p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('--label',default='response_normal');args=p.parse_args()
source=Path(args.source).resolve();before=hashlib.sha256(source.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('response_producer',source);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
checks=[];failures=[]
def check(name,ok,detail=''):
    okay=bool(ok);row={'name':name,'status':'passed' if okay else 'failed','detail':detail};checks.append(row)
    if not okay:failures.append(row)
def reject(name,f):
    try:f()
    except (ValueError,TypeError,ArithmeticError,RuntimeError):check(name,True);return
    check(name,False,'Unexpected acceptance')

def ratio_series(degree):
    z=[haar(j)/factorial(j) for j in range(degree+1)]
    num=[haar(j+1)/factorial(j) for j in range(degree+1)]
    out=[]
    for j in range(degree+1):out.append(num[j]-sum((z[i]*out[j-i] for i in range(1,j+1)),Q(0)))
    return out

for order in [0,1,3,6,12]:
    series=ratio_series(2*order+1);expected=series[1::2]
    check('series_formal_division_order'+str(order),m.series_coefficients(order)==expected and all(series[i]==0 for i in range(0,len(series),2)))
    for eps in [Q(1,2),Q(1,8),Q(1,100)]:
        c=m.initial_bound(eps,order);p0=sum((a*eps**(2*i+1) for i,a in enumerate(expected)),Q(0))
        oracle=bessel_mean_interval(eps,180);bound=Q(c['analytic_initial_error_bound'])
        check('exact_launch_enclosure_'+str(order)+'_'+str(eps),p0-bound<=oracle[0]<=oracle[1]<=p0+bound)
        # Independently construct polynomial residual by coefficient convolution.
        dense=[Q(0)]*(2*order+2)
        for i,a in enumerate(expected):dense[2*i+1]=a
        residual={}
        for pwr,a in enumerate(dense):
            if a:residual[pwr]=residual.get(pwr,Q(0))+(pwr+3)*a
        residual[1]=residual.get(1,Q(0))-1
        for i,a in enumerate(dense):
            for j,b in enumerate(dense):
                if a and b:residual[i+j+1]=residual.get(i+j+1,Q(0))+a*b
        residual={p:a for p,a in residual.items() if a}
        analytic=sum((abs(a)*eps**p/(p+3) for p,a in residual.items()),Q(0))
        check('exact_launch_budget_'+str(order)+'_'+str(eps),analytic==bound and {str(p):str(a) for p,a in residual.items()}==c['residual_coefficients'])
        check('exact_polynomial_value_'+str(order)+'_'+str(eps),str(p0)==c['polynomial_value'])

# Distinct equation and implicit integrator: evolve Z,Z' linearly, then divide.
for stop in [5,20]:
    eps=Q(1,100);initial=[sum((eps**j*haar(j+nu)/factorial(j) for j in range(70)),Q(0)) for nu in [0,1]]
    grid=np.linspace(.05,stop,101)
    sol=solve_ivp(lambda k,y:[y[1],y[0]-3*y[1]/k],(.01,stop),list(map(float,initial)),t_eval=grid,method='Radau',rtol=2e-12,atol=2e-14)
    producer=m.integrate_response(stop=stop,grid=grid,rtol=2e-13)
    ratio=sol.y[1]/sol.y[0]
    reference=np.array([float(bessel_mean_interval(Q(str(k)),100)[0]) for k in grid])
    check('independent_linear_ode_complete_'+str(stop),sol.success and np.isfinite(ratio).all())
    check('independent_linear_ode_vs_riccati_'+str(stop),np.max(np.abs(ratio-producer['mean']))<2e-11,{'max_difference':float(np.max(np.abs(ratio-producer['mean'])))})
    check('independent_linear_ode_vs_exact_series_'+str(stop),np.max(np.abs(ratio-reference))<2e-11,{'max_difference':float(np.max(np.abs(ratio-reference)))})

for k in [-20,-5,-1,Q(-1,100),0,Q(1,100),1,5,20]:
    ref=haar_tilt_interval(k,1,200);vref=haar_tilt_interval(k,2,200);mu=float((ref[0]+ref[1])/2)
    variance=float((vref[0]+vref[1])/2)-mu*mu
    q=m.quadrature_moments(k)
    check('bessel_diagnostic_'+str(k),abs(m.bessel_mean(k)-mu)<3e-13)
    check('variance_diagnostic_'+str(k),abs(q['variance']-variance)<3e-13 and variance>0)

f=m.wrong_closure_fixture()
check('exact_false_closure',f['n0_residual']=='0' and Q(f['n1_residual'])==Q(8,9) and f['H1_determinant']=='0' and Q(f['L0'])==Q(8,9))
for bad in [True,False,np.bool_(True),float('nan'),float('inf'),None,[],{},'1']:
    reject('invalid_scalar_'+repr(bad),lambda bad=bad:m.bessel_mean(bad))
for bad in [True,0,-1,Q(3,4),.01]:reject('invalid_exact_launch_'+repr(bad),lambda bad=bad:m.initial_bound(bad))
for bad in [True,-1,13,3.0]:reject('invalid_series_order_'+repr(bad),lambda bad=bad:m.series_coefficients(bad))
for bad in [[],[1,1],[2,1],[0,1],[1,21],[float('nan')],[True],[True,2.0],np.array([np.bool_(True)]),['1'],[1+0j]]:
    reject('invalid_grid_'+repr(bad),lambda bad=bad:m.integrate_response(grid=bad))
reject('origin_division',lambda:m.rhs(0,0))
reject('negative_rhs_domain',lambda:m.rhs(-1,0))
reject('impossible_tolerance',lambda:m.integrate_response(rtol=1e-20))
reject('unbounded_helper_domain',lambda:m.series_value(2,m.series_coefficients(2)))

result_path=source.parent/'output'/'results.json'
if result_path.exists():
    data=json.loads(result_path.read_text());check('recorded_source_hash',data['source_sha256']==before)
    for name,digest in json.loads((result_path.parent/'SHA256SUMS.json').read_text()).items():
        check('output_hash_'+name,hashlib.sha256((result_path.parent/name).read_bytes()).hexdigest()==digest)
    init=json.loads((result_path.parent/'initialization_bounds.json').read_text())
    for j,c in enumerate(init):
        eps=Q(c['epsilon']);p0=Q(c['polynomial_value']);b=Q(c['analytic_initial_error_bound']);ref=bessel_mean_interval(eps,100)
        check('stored_launch_'+str(j),p0-b<=ref[0]<=ref[1]<=p0+b)
check('unchanged_source',before==hashlib.sha256(source.read_bytes()).hexdigest())
out={'status':'passed' if not failures else 'failed','source':str(source),'source_sha256':before,'count':len(checks),'checks':checks,'failures':failures,'scope':'Exact compact exponential-family response and rational launch enclosure; alternative linear partition-function ODE is a floating comparison, not a total error certificate.'}
Path(__file__).with_name(args.label+'_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'count':len(checks),'failures':failures},indent=2))
if failures:raise SystemExit(1)
