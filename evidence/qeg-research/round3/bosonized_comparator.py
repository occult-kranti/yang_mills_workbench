"""Independent numerical audit of a published first-mass-order QED comparator.

This solves the classical-looking first-order effective equation derived by
Gralla and Mizuno, not full QED at all orders and not the 3+1 Landau solver.
Two independent numerical methods: event periods and energy quadrature.
"""
from pathlib import Path
import json,hashlib,platform
import numpy as np
import scipy
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import j1, roots_legendre

ROOT=Path(__file__).resolve().parent

def period_ode(A,g):
    def rhs(t,y): return [y[1],-y[0]-g*np.sin(y[0]-A)]
    def minimum(t,y):return y[1]
    minimum.direction=1
    sol=solve_ivp(rhs,(0.,20.),[A,0.],method='DOP853',rtol=2e-12,atol=2e-14,events=minimum,dense_output=True,max_step=.08)
    if not sol.success:raise RuntimeError(sol.message)
    times=sol.t_events[0]
    if len(times)<3:raise RuntimeError('Insufficient complete periods')
    ts=np.linspace(0,20,1201);z,v=sol.sol(ts)
    energy=.5*v*v+.5*z*z-g*np.cos(z-A)
    return float(np.mean(np.diff(times))),float(np.max(np.abs(energy-energy[0]))),times.tolist()

def period_quadrature(A,g,N=256):
    def difference(z):return .5*(A-z)*(A+z)-2*g*np.sin((z-A)/2)**2
    low=brentq(difference,-A-1.,-A+.5,xtol=5e-15)
    center=(A+low)/2;radius=(A-low)/2
    nodes,weights=roots_legendre(N);theta=(nodes+1)*np.pi/2
    z=center+radius*np.cos(theta);gap=difference(z)
    if np.any(gap<=0):raise RuntimeError('Quadrature entered nonpositive energy gap')
    T=np.sqrt(2)*np.pi/2*np.sum(weights*radius*np.sin(theta)/np.sqrt(gap))
    return float(T),float(low)

def main():
    rows=[]
    for A in [.5,2.,5.]:
        for g in [0.,.02,.01,.005,.0025]:
            T,err,events=period_ode(A,g)
            q128,low=period_quadrature(A,g,128);q256,_=period_quadrature(A,g,256)
            omega=2*np.pi/T;slope=float(np.cos(A)*j1(A)/A)
            approx=1+g*slope
            rows.append({'A':A,'g':g,'m_over_q':g/(2*np.exp(np.euler_gamma)*np.sqrt(np.pi)),
                         'omega_over_q_sqrt_pi':omega,'first_order_frequency':approx,'first_order_error':omega-approx,
                         'linear_coefficient':slope,'ode_period':T,'energy_quadrature_period':q256,
                         'quadrature_128_256_difference':q256-q128,'ode_quadrature_period_difference':T-q256,
                         'energy_max_error':err,'lower_turning_point':low,'minimum_events':events})
    rates=[]
    for A in [.5,2.,5.]:
        rr=[r for r in rows if r['A']==A and r['g']>0]
        rates.append({'A':A,'g_coarse':rr[-2]['g'],'g_fine':rr[-1]['g'],
                      'measured_error_order':float(np.log(abs(rr[-2]['first_order_error']/rr[-1]['first_order_error']))/np.log(2))})
    gates={'massless_frequency_abs_error_below_1e-10':all(abs(r['omega_over_q_sqrt_pi']-1)<1e-10 for r in rows if r['g']==0),
           'all_period_method_differences_below_1e-7':all(abs(r['ode_quadrature_period_difference'])<1e-7 for r in rows),
           'energy_errors_below_1e-9':all(r['energy_max_error']<1e-9 for r in rows),
           'first_order_remainders_approach_second_order':all(1.8<r['measured_error_order']<2.2 for r in rates)}
    out={'source':'https://arxiv.org/html/2511.23464v2','scope':'Numerical verification of the first-order effective equation and frequency expansion; no all-orders quantum solution.',
         'equation':'z_ddot+z+g*sin(z-A)=0; z(0)=A, z_dot(0)=0; time=q*t/sqrt(pi)',
         'warning':'Higher powers produced by solving the truncated equation exactly are not derived full-QED higher-order predictions.',
         'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'rows':rows,'remainder_orders':rates,'gates':gates,'all_gates_passed':all(gates.values())}
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/bosonized_comparator.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'gates':gates,'orders':rates,'max_period_difference':max(abs(r['ode_quadrature_period_difference']) for r in rows)},indent=2))
    if not all(gates.values()):raise SystemExit(1)
if __name__=='__main__':main()
