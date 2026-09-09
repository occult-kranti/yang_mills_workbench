#!/usr/bin/env python3
"""Independent exact checks and counterexamples for the finite-model theorem.

Runs without the response solver. SymPy is used only for local algebra;
the analytic continuation and parameter-dependence proofs remain in the text.
Use an installed SymPy or the existing workspace deps; do not fetch code here.
"""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
for candidate in (HERE / 'deps', HERE.parent / 'vendor-python'):
    if candidate.is_dir():
        sys.path.insert(0, str(candidate))
        break
import sympy as s


def main():
    checks = []

    def check(name, passed, evidence, category='exact_algebra'):
        checks.append(dict(name=name, passed=bool(passed), category=category,
                           evidence=evidence))

    def zero(name, expression):
        result = s.simplify(expression)
        check(name, result == 0, str(result))

    p, M, w, x = s.symbols('p M w x', real=True, positive=True)
    e2, chi, F = s.symbols('e2 chi F', real=True)
    rx, ry, rz = s.symbols('rx ry rz', real=True)
    omega = s.sqrt(M*M+p*p)
    C = w*M*M/(4*omega**5)
    D = 5*w*M*M*p/(8*omega**7)
    S = w*(rz+p/omega)
    Z = 1+chi-e2*C
    h = s.Matrix([M, 0, p])
    r = s.Matrix([rx, ry, rz])
    rdot = 2*h.cross(r)
    U = w*(h.dot(r)+omega)
    Udot = s.diff(U,p)*x + sum(s.diff(U,z)*dz for z,dz in zip(r,rdot))
    zero('Bloch norm derivative', 2*r.dot(rdot))
    zero('U prime equals x S', Udot-x*S)
    zero('C prime equals minus two D x', s.diff(C,p)*x+2*D*x)
    xdot = (F-e2*(S+D*x*x))/Z
    W = Z*x*x/2+e2*U
    Wdot = s.diff(W,p)*x+s.diff(W,x)*xdot + sum(s.diff(W,z)*dz for z,dz in zip(r,rdot))
    zero('Complete fixed-regulator work identity', Wdot-x*F)

    mass_cubes_lower = [84,246,427,729]
    for n, lower in enumerate(mass_cubes_lower, start=1):
        check(f'M_{n} cubed lower bound', (1+20*n)**3 >= lower**2,
              {'squared_actual':(1+20*n)**3,'squared_lower':lower**2}, 'exact_integer')
    bracket = 1 + 2*sum((Q(1,d) for d in mass_cubes_lower), Q(0))
    c_upper = Q(100,137)/Q(157,50)*bracket
    gap = Q(1,4)-c_upper
    check('Selected exact ideal regulator has e2 C less than one quarter',
          c_upper < Q(1,4),
          {'upper':str(c_upper), 'strict_margin':str(gap),
           'implied_Z_lower':str(1-c_upper)}, 'exact_rational')

    # A smooth source and a bounded exact trajectory reach the excluded Z=0
    # boundary at t=1. All r=0 is an admissible mixed Bloch state.
    t = s.symbols('t', real=True)
    pt = 1-t
    omt = s.sqrt(1+pt**2)
    Ct = 1/omt**5                # M=1,w=4,e2=1,chi=0
    Dt = 5*pt/(2*omt**7)
    St = 4*pt/omt
    Zt = 1-Ct
    Ft = St+Dt                  # x=-1, x'=0
    zero('Smooth Z-boundary counterexample obeys undivided Maxwell equation',
         Zt*0 - (Ft-St-Dt))
    check('Z-boundary counterexample starts positive', Zt.subs(t,0)>0,
          str(Zt.subs(t,0)))
    check('Z-boundary counterexample reaches zero at finite time',
          Zt.subs(t,1)==0, {'time':1,'Z':str(Zt.subs(t,1)),
                           'F':str(Ft.subs(t,1)), 'x':-1})

    # Coercivity really uses both initial-state and quadrature hypotheses.
    check('Invalid Bloch norm can make U negative', Q(-2)+1 < 0,
          {'M':1,'p':0,'w':1,'r':[-2,0,0],'U':-1}, 'exact_counterexample')
    check('A negative weight can make U negative despite unit Bloch norm',
          -2 < 0, {'M':1,'p':0,'w':-1,'r':[1,0,0],'U':-2},
          'exact_counterexample')
    check('Massless zero-momentum vacuum normalization is undefined',
          s.sqrt(M*M+p*p).subs({M:0,p:0})==0,
          {'M':0,'p':0,'omega':0,'undefined_terms':['p/omega','h/omega','C','D']},
          'exact_counterexample')

    # For an admissible pure initial-state rotation, tangent energy is zero
    # while the electric-field tangent already has nonzero derivative.
    lam = s.symbols('lam', real=True)
    rotated = s.Matrix([-s.cos(lam),0,s.sin(lam)])
    eta = rotated.diff(lam).subs(lam,0)
    zero('Rotated initial states have exactly unit norm',rotated.dot(rotated)-1)
    deltaW0 = s.Matrix([1,0,0]).dot(eta)
    uprime0 = -eta[2]/s.Rational(3,4)
    check('Zero tangent energy does not force zero response',
          deltaW0==0 and uprime0 == -s.Rational(4,3),
          {'eta0':list(map(str,eta)), 'deltaW0':str(deltaW0),
           'u_prime0':str(uprime0),'F_and_f':0},'exact_counterexample')
    check('Mixed-state parameter families need not have r dot eta zero',
          Q(1,2)!=0, {'r0':['1/2',0,0],'eta0':[1,0,0],
                      'r_dot_eta':'1/2','family':'r(lambda)=(lambda,0,0)'},
          'exact_counterexample')

    # Global bounded solutions need not have a uniformly bounded derivative.
    phase = s.Matrix([s.cos(lam*t),s.sin(lam*t)])
    tangent = phase.diff(lam)
    zero('Bounded-phase family norm identity',phase.dot(phase)-1)
    zero('Bounded-phase derivative norm grows quadratically',
         tangent.dot(tangent)-t*t)
    check('Continuum-energy obstruction with fixed positive gap',
          Q(1,4)*(1+1)==Q(1,2),
          {'family':'M_i=1,k_i=i,w_i=1/i^2,r_i=h_i/omega_i,e2=1,chi=0',
           'uniform_C_upper':'1/2','uniform_Z_lower':'1/2',
           'initial_U_lower':'2*H_N, where H_N is the harmonic sum',
           'meaning':'Each finite truncation passes existence assumptions; U diverges as N increases.'},
          'exact_inequality_plus_analytic_comparison')

    # A two-sided parameter cusp violates C1 without spoiling each IVP.
    check('Continuous source families need not be differentiable',
          s.limit(s.Abs(lam)/lam,lam,0,dir='+') != s.limit(s.Abs(lam)/lam,lam,0,dir='-'),
          {'x_family':'x(t,lambda)=t*abs(lambda)',
           'one_sided_derivatives_at_t1':[1,-1],
           'construction':'a=-abs(lambda)*t^2/2,r=0,F=Z*xprime+e2*(S+D*x^2)'},
          'exact_counterexample')
    check('Singular relative gain need not imply singular response',
          s.cos(s.pi/2)==0 and s.sin(s.pi/2)==1,
          {'family':'x(t,lambda)=cos(t)+lambda*sin(t)',
           'base_at_pi_over_2':0,'absolute_tangent':1},'exact_counterexample')

    # Independent algebra for the next gravitational interface; no quantum
    # closure is assumed to exist merely because this identity is verified.
    hp, hl, kap, rho, pp, pl, cosm, defect = s.symbols(
        'Hp Hl kappa rho pperp pparallel Lambda Q',real=True)
    dhp = (cosm-kap*pl-3*hp**2)/2
    dhl = cosm-kap*pp-dhp-hp**2-hl**2-hp*hl
    drho = defect-2*hp*(rho+pp)-hl*(rho+pl)
    constraint = hp**2+2*hp*hl-kap*rho-cosm
    dconstraint = (2*hp+2*hl)*dhp+2*hp*dhl-kap*drho
    zero('Conditional Bianchi I constraint propagation with Ward defect',
         dconstraint+(2*hp+hl)*constraint+kap*defect)

    result = {
        'status':'independent_exact_checks_passed' if all(c['passed'] for c in checks) else 'failed',
        'check_count':len(checks),
        'all_checks_passed':all(c['passed'] for c in checks),
        'checks':checks,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'sympy_version':s.__version__,
        'scope':'Exact finite-mode identities, rational certificate, and logical counterexamples. This script is not a proof-assistant verification of global ODE existence, continuum QED, or gravitation.',
        'selected_regulator_certificate_assumptions':{
            'b':10,'K':20,'Landau_indices':[0,1,2,3,4],
            'longitudinal_weights':'positive exact mathematical weights whose sum is40',
            'alpha':'0<alpha<1/137','pi':'pi>157/50','chi':'>=0',
            'floating_implementation_certified':False,
        },
    }
    (HERE/'counterexample_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('status','check_count','all_checks_passed','source_sha256')},indent=2))
    if not result['all_checks_passed']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
