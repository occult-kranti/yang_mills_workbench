"""Independent advisor checks: shared subtraction and prior exact benchmark.

No numerical implementation from the research solvers is imported.
"""
from pathlib import Path
import json
import math
import sys
import numpy as np
import mpmath as mp
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.special import digamma

ROOT = Path(__file__).resolve().parent

def symbolic_checks():
    p, m, e, ed = sp.symbols('p M E Edot', real=True)
    w = sp.sqrt(m*m+p*p)
    u2 = m*m*e*e/(8*w**5)
    j2 = m*m*ed/(4*w**5)-5*m*m*p*e*e/(8*w**7)
    energy = sp.simplify(sp.diff(u2,p)*e+sp.diff(u2,e)*ed-e*j2)
    c = m*m/(4*w**5)
    ss = 5*m*m*p/(8*w**7)
    c_identity = sp.simplify(sp.diff(c,p)*e+2*ss*e)
    return {'u2_derivative_minus_E_j2': str(energy),
            'C_derivative_plus_2S_E': str(c_identity),
            'all_passed': energy == 0 and c_identity == 0}

def exact_expansion(eta=1., Tg=.5, b=10., n=1, K=0.):
    mp.mp.dps=70
    et, t, bb, kk = map(lambda x: mp.mpf(str(x)), [eta,Tg,b,K])
    mperp = mp.sqrt(2*bb*n+kk*kk)
    k_eff=1+et/2
    a_eff=et/(2*t)
    wi=mp.sqrt((k_eff-a_eff*t)**2+mperp*mperp)
    wo=mp.sqrt((k_eff+a_eff*t)**2+mperp*mperp)
    f=(mp.cosh(2*mp.pi*a_eff*t*t)-mp.cosh(mp.pi*t*(wo-wi)))/(2*mp.sinh(mp.pi*t*wi)*mp.sinh(mp.pi*t*wo))
    return 2*f

def independent_sector(L, tol, max_step):
    sigma1=np.array([[0,1],[1,0]],complex)
    sigma2=np.array([[0,-1j],[1j,0]],complex)
    def H(t):
        ag=1.5+.5*math.tanh(t/.5)
        return ag*sigma1-math.sqrt(20)*sigma2
    eig, v=np.linalg.eigh(H(-L))
    sol=solve_ivp(lambda t,y: -1j*H(t)@y,(-L,L),v[:,0],method='DOP853',
                  rtol=tol,atol=tol/100,max_step=max_step)
    if not sol.success: raise RuntimeError(sol.message)
    eig,v=np.linalg.eigh(H(L)); y=sol.y[:,-1]
    norm=float(np.vdot(y,y).real)
    raw=2*float(abs(np.vdot(v[:,1],y))**2)
    maxnorm=float(np.max(np.abs(np.sum(abs(sol.y)**2,axis=0)-1)))
    exact=float(exact_expansion())
    return {'L':L,'rtol':tol,'max_step':max_step,'N_raw':raw,
            'N_normalized':raw/norm,'N_exact':exact,
            'absolute_error':abs(raw-exact), 'relative_error':abs(raw-exact)/exact,
            'max_sampled_norm_error':maxnorm,'endpoint_norm_error':abs(norm-1),
            'nfev':sol.nfev}

def susceptibility_matching():
    rows=[]
    e2=4*math.pi/137.035999084
    for b in [1.,10.,100.]:
        aa=1/(2*b)
        chi=e2/(12*math.pi**2)*(b-math.log(2*b)-digamma(1+aa))
        for N in [16,64,256,1024,4096]:
            cb=(b+digamma(N+1+aa)-digamma(1+aa))/(12*math.pi**2)
            c0=math.log(1+2*b*N)/(12*math.pi**2)
            rows.append({'b':b,'N':N,'e2_CB_minus_C0':e2*(cb-c0),'chi':chi,
                         'absolute_error':abs(e2*(cb-c0)-chi)})
    return rows

def main():
    exact=exact_expansion()
    audit=[independent_sector(L,tol,step) for L,tol,step in
           [(2.,2e-12,.05),(3.,2e-12,.05),(4.,2e-12,.05),(6.,2e-12,.05),
            (12.,2e-12,.05),(16.,2e-12,.05),(12.,5e-14,.025),(16.,5e-14,.025)]]
    prior=json.loads((ROOT.parent/'retry/curved_sector_results.json').read_text())
    old=next(x for x in prior['cases'] if x['case']['name']=='expansion_only_zero_momentum')
    data={'scope':'Independent symbolic finite-system checks and exact external-background counterexample audit; no continuum backreaction claim',
          'symbolic':symbolic_checks(),
          'expansion_only_exact_total_70_digit_working_precision':mp.nstr(exact,65),
          'prior_full_4x4_value':old['full_4x4_occupation'],
          'prior_full_4x4_abs_error_vs_exact':abs(old['full_4x4_occupation']-float(exact)),
          'prior_full_4x4_relative_error_vs_exact':abs(old['full_4x4_occupation']-float(exact))/float(exact),
          'prior_full_4x4_norm_residual':old['full_4x4_norm_residual'],
          'finite_time_tolerance_audit':audit,
          'Landau_zero_B_charge_matching':susceptibility_matching(),
          'strict_requested_abs_error_1e-18_passed':audit[-1]['absolute_error'] < 1e-18,
          'strict_gate_note':'The initial 1e-18 numerical target failed; retain the measured error rather than claim a certified precision or silently loosen the gate.'}
    assert data['symbolic']['all_passed']
    (ROOT/'advisor_checks.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'symbolic_passed':True,'exact':str(exact),'best_abs_error':audit[-1]['absolute_error'],
                      'prior_abs_error':data['prior_full_4x4_abs_error_vs_exact']},allow_nan=False))

if __name__=='__main__': main()
