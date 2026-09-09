#!/usr/bin/env python3
"""Independent skeptical checks; no production imports, no assert-based gates.

The identities are finite-model or classical scalar–Maxwell benchmarks, not a
construction of a renormalized Einstein–QED current/stress pair.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.special import digamma

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'round5' / 'deps'))
import sympy as sp

GATES = []

def gate(name, ok, evidence):
    ok = bool(ok)
    GATES.append({'name': name, 'passed': ok, 'evidence': evidence})
    if not ok:
        raise RuntimeError(f'Independent gate failed: {name}: {evidence}')

def ident(name, expr):
    value = sp.simplify(expr)
    gate(name, value == 0, str(value))


def symbolic():
    hp,hz,E,B,v,f,fp,Vp = sp.symbols('hp hz E B v f fp Vp', real=True)
    theta = 2*hp+hz
    fd = fp*v
    Ed = -(2*hp+fd/f)*E
    Bd = -2*hp*B
    vd = -theta*v - Vp - fp*(B**2-E**2)/2
    rem = f*(E**2+B**2)/2
    remd = fd*(E**2+B**2)/2 + f*(E*Ed+B*Bd)
    qem = sp.expand(remd+4*hp*rem)
    qphi = sp.expand(v*vd+Vp*v+theta*v**2)
    ident('EM energy exchange from independent differentiation', qem-fd*(B**2-E**2)/2)
    ident('Scalar energy exchange cancels Maxwell exchange', qem+qphi)
    ident('Omitted scalar force has a nonzero known Ward defect',
          qem+v*(-theta*v-Vp)+Vp*v+theta*v**2-fd*(B**2-E**2)/2)
    gate('Wrong-model Ward defect is discriminating', qem.subs({f:1,fp:2,v:3,E:1,B:2}) != 0,
         str(qem.subs({f:1,fp:2,v:3,E:1,B:2})))
    ident('Conserved electric displacement flux', fd*E+f*Ed+2*hp*f*E)
    ident('Conserved magnetic flux', Bd+2*hp*B)

    rho,pp,pl,Lambda,kappa,Q = sp.symbols('rho pp pl Lambda kappa Q', real=True)
    con = hp**2+2*hp*hz-kappa*rho-Lambda
    hpd = (Lambda-kappa*pl-3*hp**2)/2
    hzd = Lambda-kappa*pp-hpd-hp**2-hz**2-hp*hz
    rd = Q-2*hp*(rho+pp)-hz*(rho+pl)
    cd = 2*(hp+hz)*hpd+2*hp*hzd-kappa*rd
    ident('Bianchi constraint propagation with arbitrary Ward defect', cd+theta*con+kappa*Q)
    gate('Wrong factor two in constraint damping is rejected', sp.simplify(cd+2*theta*con+kappa*Q)!=0,
         str(sp.factor(cd+2*theta*con+kappa*Q)))

    x,F,e2,S,D,Z,chid = sp.symbols('x F e2 S D Z chid', real=True)
    zd = chid+2*e2*D*x
    naive_xd = (F-e2*(S+D*x*x))/Z
    naive_wd = zd*x*x/2+Z*x*naive_xd+e2*x*S
    ident('Naive time-varying chi produces plus half work defect', naive_wd-x*F-chid*x*x/2)
    action_xd = naive_xd-chid*x/Z
    action_wd = zd*x*x/2+Z*x*action_xd+e2*x*S
    ident('Action-consistent time-varying chi has support work', action_wd-x*F+chid*x*x/2)
    gate('Neither time-dependent chi prescription closes unsupported energy',
         sp.simplify(naive_wd-x*F)!=0 and sp.simplify(action_wd-x*F)!=0,
         {'naive':str(sp.simplify(naive_wd-x*F)), 'action':str(sp.simplify(action_wd-x*F))})


def finite_bridge_checks():
    x,F,e2,S,D,Z,fp,y,Vp,b = sp.symbols('x F e2 S D Z fp y Vp b', real=True)
    zd=fp*y+2*e2*D*x
    xd=(F-e2*(S+D*x*x)-fp*y*x)/Z
    yd=-Vp+fp*(x*x-b*b)/2
    wd=zd*x*x/2+Z*x*xd+e2*x*S+y*yd+Vp*y+fp*y*b*b/2
    ident('Finite QED–scalar combined exact work identity',wd-x*F)
    legacy=(F-e2*(S+D*x*x))/Z
    ident('Finite scalar bridge recovers legacy Maxwell at decoupling',xd.subs(fp,0)-legacy)
    gate('Omitting new Maxwell exchange creates a resolved work defect',
         sp.simplify((wd+fp*y*x*x)-x*F)==fp*y*x*x, str(fp*y*x*x))
    gate('Omitting scalar magnetic force creates a work defect',
         sp.simplify(wd+fp*y*b*b/2-x*F)==fp*y*b*b/2, str(fp*y*b*b/2))
    # Independent Euler–Lagrange collection: a_dot=−x, Z_a=−2e²D.
    za=-2*e2*D
    d_dt_L_adot=-Z*xd+za*x*x-fp*y*x
    L_a=za*x*x/2+e2*S-F
    ident('Reduced action Euler–Lagrange equation for potential',d_dt_L_adot-L_a)
    ident('Reduced action Euler–Lagrange equation for scalar',yd-(fp*x*x/2-Vp-fp*b*b/2))
    a,k,M,rx,ry,rz=sp.symbols('a k M rx ry rz', real=True)
    p=k-a; om=sp.sqrt(M*M+p*p)
    spin_part=-(M*rx+p*rz+om)
    ident('Spinor plus vacuum variation supplies S contact term',sp.diff(spin_part,a)-rz-p/om)
    spin=[rx,ry,rz]; spin_dot=[-2*p*ry,2*(p*rx-M*rz),2*M*ry]
    U=M*rx+p*rz+om
    ud=-x*sp.diff(U,a)+sum(sp.diff(U,q)*qd for q,qd in zip(spin,spin_dot))
    ident('Finite modal energy derivative retains full Bloch coherence',ud-x*(rz+p/om))
    g,phi=sp.symbols('g phi', real=True)
    f=1+g*g*phi*phi
    ident('Polynomial completion exactly returns f=1 at g=0',f.subs(g,0)-1)
    gate('Polynomial f has nonnegative excess on real fields',sp.ask(sp.Q.nonnegative(f-1)) is True,str(f-1))


def coefficient(b,N,K,a):
    # Quadrature reference rather than production endpoint formula.
    if not (b>0 and K>0 and isinstance(N,int) and N>=0 and all(map(math.isfinite,(b,K,a)))):
        raise ValueError('Invalid finite integral parameters')
    return b/(16*math.pi**2)*sum((1 if n==0 else 2)*quad(
        lambda p: (1+2*b*n)/(1+2*b*n+p*p)**2.5,
        -K-a,K-a,epsabs=2e-12,epsrel=2e-12,points=[0] if abs(a)<K else None)[0]
        for n in range(N+1))


def cutoff_checks():
    b,N,K,A = 1.3,17,8.0,2.0
    lower = coefficient(b,N,K-A,0)
    vals=[coefficient(b,N,K,a) for a in np.linspace(-A,A,11)]
    gate('Bounded-potential translated-window inclusion', min(vals)>=lower-1e-13,
         {'minimum_sampled_C':min(vals),'inclusion_lower_C':lower})
    b=10.0; e2=4*math.pi/137.035999084
    chi=e2/(12*math.pi**2)*(b-math.log(2*b)-digamma(1+1/(2*b)))
    cref=coefficient(b,4,20,0)
    zref=1+chi-e2*cref
    records=[]
    for n,k,a in [(0,2,0),(4,20,0),(20,50,3),(40,70,10)]:
        c0=coefficient(b,n,k,0); ca=coefficient(b,n,k,a)
        delta=e2*(c0-cref)
        direct=1+chi+delta-e2*ca
        formal=zref+e2*(c0-ca)
        records.append({'N':n,'K':k,'a':a,'gap':direct,'reference_gap':zref})
        gate(f'Reference coefficient subtraction identity N={n}',abs(direct-formal)<2e-15,
             {'direct':direct,'identity':formal})
        gate(f'Continuous integral reference gap N={n}',direct>=zref-2e-15,
             {'gap':direct,'reference_gap':zref})
    # Analytic harmonic identity at tractable N, including degeneracy n=0.
    for n in [0,1,4,40,400]:
        total=b/(12*math.pi**2)*sum((1 if j==0 else 2)/(1+2*b*j) for j in range(n+1))
        special=(b+digamma(n+1+1/(2*b))-digamma(1+1/(2*b)))/(12*math.pi**2)
        gate(f'Inclusive Landau full-momentum coefficient N={n}',abs(total-special)<2e-15,
             {'direct':total,'digamma':special})
    # A deliberately coarse discrete rule disproves transfer of the integral max.
    k=20.; nodes,weights=np.polynomial.legendre.leggauss(2); nodes*=k;weights*=k
    def discrete(a): return b/(16*math.pi**2)*np.sum(weights/(1+(nodes-a)**2)**2.5)
    peak=float(discrete(float(nodes[1])))
    origin=float(discrete(0.0))
    gate('Discrete reference-at-zero subtraction need not retain its gap',peak>origin+0.1,
         {'C_discrete_at_origin':origin,'C_discrete_at_node':peak,
          'z_at_node_minus_reference_gap':e2*(origin-peak)})
    return records


def scalar_run(*, wrong=False, rtol=1e-10):
    c=0.4; mass=0.5
    phi0=0.2; v0=0.03; e0=0.04; b0=0.07; hp0=0.04
    f0=math.exp(2*c*phi0)
    rho0=(v0*v0+mass*mass*phi0*phi0+f0*(e0*e0+b0*b0))/2
    hz0=(rho0-hp0*hp0)/(2*hp0)
    y0=np.array([0.,0.,hp0,hz0,phi0,v0,e0,b0,0.])
    # State uses logarithmic scale factors and a separately evolved constraint
    # response, avoiding algebraic constraint projection during integration.
    def rhs(t,y):
        la,lc,hp,hz,phi,v,E,B,ci=y
        f=math.exp(2*c*phi); fp=2*c*f; theta=2*hp+hz
        em=f*(E*E+B*B)/2; kinetic=v*v/2; potential=mass*mass*phi*phi/2
        pp=kinetic-potential+em; pl=kinetic-potential-em
        hpd=(-pl-3*hp*hp)/2
        hzd=-pp-hpd-hp*hp-hz*hz-hp*hz
        force=fp*(B*B-E*E)/2
        vd=-theta*v-mass*mass*phi-(0 if wrong else force)
        q=fp*v*(B*B-E*E)/2 if wrong else 0.
        return [hp,hz,hpd,hzd,v,vd,-(2*hp+2*c*v)*E,-2*hp*B,-theta*ci-q]
    times=np.linspace(0,10,251)
    sol=solve_ivp(rhs,(0,10),y0,method='Radau',rtol=rtol,atol=rtol/50,t_eval=times)
    if not sol.success or sol.y.shape!=(9,len(times)) or not np.isfinite(sol.y).all():
        raise RuntimeError('Independent scalar integration failed or incomplete')
    la,lc,hp,hz,phi,v,E,B,ci=sol.y
    f=np.exp(2*c*phi)
    rho=(v*v+mass*mass*phi*phi+f*(E*E+B*B))/2
    con=hp*hp+2*hp*hz-rho
    eflux=f*E*np.exp(2*la); bflux=B*np.exp(2*la)
    q=2*c*f*v*(B*B-E*E)/2 if wrong else np.zeros_like(E)
    diag={'wrong_model':wrong,'rtol':rtol,'max_constraint_absolute':float(np.max(np.abs(con))),
          'max_constraint_scaled_initial_density':float(np.max(np.abs(con))/rho0),
          'max_constraint_propagation_defect':float(np.max(np.abs(con-ci))),
          'max_electric_flux_relative_error':float(np.max(np.abs(eflux/(f0*e0)-1))),
          'max_magnetic_flux_relative_error':float(np.max(np.abs(bflux/b0-1))),
          'max_abs_Ward_defect':float(np.max(np.abs(q))),
          'max_phi_abs':float(np.max(np.abs(phi))),
          'final_state':sol.y[:8,-1].tolist(),'samples':len(times),'nfev':sol.nfev}
    return diag


def numerical_scalar():
    accurate=scalar_run(rtol=2e-11)
    loose=scalar_run(rtol=2e-8)
    wrong=scalar_run(wrong=True,rtol=2e-11)
    gate('Closed scalar benchmark preserves Einstein constraint',
         accurate['max_constraint_scaled_initial_density']<1e-8,accurate)
    gate('Independent Maxwell fluxes are preserved',
         max(accurate['max_electric_flux_relative_error'],accurate['max_magnetic_flux_relative_error'])<1e-8,accurate)
    error=float(np.max(np.abs(np.array(accurate['final_state'])-np.array(loose['final_state']))))
    gate('Independent scalar tolerance refinement',error<1e-7,{'max_final_state_error':error})
    gate('Omitted-force control creates resolved constraint error',
         wrong['max_constraint_scaled_initial_density']>1e-4,wrong)
    gate('Wrong-model constraint drift follows independently evolved Ward source',
         wrong['max_constraint_propagation_defect']<1e-9,wrong)
    gate('Wrong-model defect cannot be explained by correct-model numerical residue',
         wrong['max_constraint_absolute']>10000*accurate['max_constraint_absolute'],
         {'correct':accurate['max_constraint_absolute'],'wrong':wrong['max_constraint_absolute']})
    return {'correct':accurate,'loose':loose,'wrong_model':wrong}


def main():
    symbolic()
    finite_bridge_checks()
    cuts=cutoff_checks()
    scalar=numerical_scalar()
    result={'status':'passed','scope':'Independent finite-coefficient identities and classical scalar–Maxwell Bianchi I; no continuum quantum closure',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'passed_checks':len(GATES),'gates':GATES,'reference_subtraction_samples':cuts,
            'scalar_benchmark':scalar,
            'limitations':['Symbolic identities are conventional exact algebra, not proof-assistant certificates.',
                           'Floating-point tests have tolerance gates, not interval enclosures.',
                           'Cutoff no-go is proved in skeptic_review.md; finite samples do not prove an infinite limit.',
                           'Scalar benchmark is a different classical EFT hypothesis, not computed Einstein–QED.']}
    (HERE/'independent_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'passed_checks':len(GATES),'source_sha256':result['source_sha256'],
                      'scalar_correct_constraint':scalar['correct']['max_constraint_absolute'],
                      'scalar_wrong_constraint':scalar['wrong_model']['max_constraint_absolute']}))

if __name__=='__main__':
    main()
