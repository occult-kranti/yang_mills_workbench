#!/usr/bin/env python3
"""Root audit: independent complex-spinor representation and held-out inputs.

The spinor reference shares the specified regulator and physical constants,
but imports no production RHS, term evaluator, energy, or initial-state code.
The gravitational flux comparison in gravity_sim shares its spatial RHS;
independent_checks.py supplies separately written symbolic and numeric checks.
"""
from pathlib import Path
import hashlib
import json
import math
from dataclasses import replace
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.special import digamma
import finite_scalar as fs
import gravity_sim as gs

HERE = Path(__file__).resolve().parent
CHECKS = []

def gate(name, value, evidence):
    row = dict(name=name, passed=bool(value), evidence=evidence)
    CHECKS.append(row)
    if not row['passed']:
        raise RuntimeError(f'{name}: {evidence}')

def rejects(name, call, exceptions):
    try:
        call()
    except exceptions:
        gate(name, True, 'Explicit exception')
    else:
        gate(name, False, 'Invalid input accepted')

def spinor_reference(p):
    nodes, w = np.polynomial.legendre.leggauss(p.nK)
    k = np.tile(p.a0 + p.Kmax*nodes, p.ncut+1)
    levels = np.arange(p.ncut+1)
    M = np.repeat(np.sqrt(1+2*p.b*levels), p.nK)
    weights = np.repeat(p.b*np.where(levels==0, 1, 2)/(4*np.pi**2), p.nK)*np.tile(p.Kmax*w, p.ncut+1)
    e2 = 4*np.pi/137.035999084
    chi = e2/(12*np.pi**2)*(p.b-np.log(2*p.b)-digamma(1+1/(2*p.b)))
    if p.chi_b is not None:
        chi = p.chi_b
    om = np.hypot(M, k-p.a0)
    # Negative eigenvector of h.sigma, normalized analytically at preparation.
    z0 = -np.sqrt((om-(k-p.a0))/(2*om))
    z1 = np.sqrt((om+(k-p.a0))/(2*om))
    n = len(k)
    initial = np.concatenate(([p.a0, 0, p.phi0, p.y0, 0], z0, z1)).astype(complex)
    normalizer = quad(lambda u: np.exp(-1/(u*(1-u))), 0, 1, epsabs=1e-14)[0]

    def source(t):
        u = t/p.Tpump
        return p.target_E*np.exp(-1/(u*(1-u)))/(p.Tpump*normalizer) if 0<u<1 else 0.

    def rhs(t, q):
        a, x, phi, v = q[:4].real
        zz0, zz1 = q[5:5+n], q[5+n:]
        pp = k-a
        omega = np.hypot(M, pp)
        rz = abs(zz0)**2-abs(zz1)**2
        C = np.dot(weights, M*M/(4*omega**5))
        D = np.dot(weights, 5*M*M*pp/(8*omega**7))
        S = np.dot(weights, rz+pp/omega)
        f = 1+(p.g*phi)**2
        fp = 2*p.g**2*phi
        Z = f+chi-e2*C
        if Z <= p.z_floor:
            raise RuntimeError('Spinor reference left positive kinetic domain')
        macro = [-x, (source(t)-e2*(S+D*x*x)-fp*v*x)/Z,
                 v, -p.nu**2*phi+fp*(x*x-p.b*p.b)/2, x*source(t)]
        return np.concatenate((macro, -1j*(pp*zz0+M*zz1), -1j*(M*zz0-pp*zz1)))

    times = np.linspace(0, p.tfinal, p.sample_count)
    sol = solve_ivp(rhs, (0,p.tfinal), initial, t_eval=times, method='RK45',
                    rtol=2e-11, atol=2e-13, max_step=.02)
    gate('Independent spinor integration completed', sol.success and sol.y.shape==(5+2*n,len(times)) and np.isfinite(sol.y).all(), sol.message)
    z0, z1 = sol.y[5:5+n], sol.y[5+n:]
    norm = np.max(abs(abs(z0)**2+abs(z1)**2-1))
    gate('Independent spinors remain normalized without projection', norm<2e-8, float(norm))
    energies = []
    for j in range(len(times)):
        a,x,phi,v = sol.y[:4,j].real
        pp=k-a; om=np.hypot(M,pp)
        rx=2*(z0[:,j].conj()*z1[:,j]).real
        rz=abs(z0[:,j])**2-abs(z1[:,j])**2
        C=np.dot(weights,M*M/(4*om**5))
        energies.append((1+(p.g*phi)**2+chi-e2*C)*x*x/2+
                        e2*np.dot(weights,M*rx+pp*rz+om)+v*v/2+
                        (p.nu**2+p.g**2*p.b**2)*phi**2/2)
    residual = np.max(abs(np.asarray(energies)-energies[0]-sol.y[4].real))
    gate('Independent spinor work residual', residual<2e-7, float(residual))
    return sol

def main():
    bound = [Path(fs.__file__), Path(gs.__file__), Path(__file__), HERE/'variable_contract.md',
             HERE/'independent_checks.py']
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in bound}
    p = fs.Params(ncut=0,nK=64)
    ref = spinor_reference(p)
    production = fs._solve(p)
    for i,field in enumerate(('a','x','phi','y')):
        err = float(np.max(abs(ref.y[i].real-np.asarray(production['macro'][field]))))
        gate('Spinor/Bloch agreement: '+field, err<2e-7, err)

    zero = fs.zero_drive_gate(replace(p,g=0.,nu=0.))
    gate('Zero-frequency scalar is affine, with no division by zero', zero['passed'],zero)
    invariant = fs._solve(replace(p,phi0=0.,y0=0.))
    err=max(max(abs(np.array(invariant['macro'][k]))) for k in ('phi','y'))
    gate('Zero scalar is a valid invariant subspace',err<1e-14,float(err))
    translated=fs._solve(replace(p,a0=3.25))
    for field in ('x','phi','y'):
        err=float(np.max(abs(np.array(translated['macro'][field])-np.array(production['macro'][field]))))
        gate('Canonical gauge translation: '+field,err<2e-9,err)
    for field,value in [('nu',-.1),('b',0),('b',True),('g','0.1'),('phi0',float('nan')),
                        ('ncut',True),('nK',1),('sample_count',True),('chi_b',float('inf'))]:
        rejects('Finite input '+field+'='+repr(value),lambda f=field,v=value:fs.validate_params(replace(p,**{f:v})),(fs.FiniteScalarFailure,))
    rejects('Unused probe cannot be silently ignored',lambda:fs._solve(p,probe_amp=.1),(fs.FiniteScalarFailure,))
    rejects('Wrong-model switch cannot be an arbitrary truthy value',lambda:fs._solve(p,wrong='false'),(fs.FiniteScalarFailure,))
    rejects('Unknown finite mode',lambda:fs._solve(p,mode='mystery'),(fs.FiniteScalarFailure,))
    rejects('Negative initial kinetic coefficient',lambda:fs._solve(replace(p,chi_b=-2)),(fs.FiniteScalarFailure,))

    c=gs.default_cases()[0]
    for field,value in [('mhat',True),('c','0.4'),('samples',True),('branch',True),('lam',float('nan'))]:
        rejects('Gravity input '+field+'='+repr(value),lambda f=field,v=value:gs.validate_case(replace(c,**{f:v})),(gs.InputError,))
    rejects('Negative Friedmann radicand is rejected rather than clipped',
            lambda:gs.make_initial_state(replace(c,mhat=0.,E0=0.,B0=0.,v0=0.,lam=-1e-15)),(gs.InputError,))
    for times in ([0,0,1],[1,0],[-1,1],[0,float('inf')],[[0,1]]):
        rejects('Invalid time grid '+repr(times),lambda t=times:gs.validate_times(t),(gs.InputError,))
    for exp in (701.,-746.):
        rejects('Exponential range '+str(exp),lambda e=exp:gs._safe_exp(e),(FloatingPointError,))
    # Equal initial fields null the initial source but are not generally an
    # invariant E=B solution when f evolves. A negative coupling is permitted.
    for case in (replace(c,name='equal_initial_fields',E0=.07,B0=.07),
                 replace(c,name='negative_coupling',c=-.45)):
        run=gs.run_case(case)
        d=run['diagnostics']
        gate(case.name+' preserves the correct constraint', d['max_constraint_abs_full']<2e-9,d['max_constraint_abs_full'])
        gate(case.name+' methods agree',d['max_full_vs_Radau_state_abs']<2e-7,d['max_full_vs_Radau_state_abs'])
    for result,source in [('finite_results.json',Path(fs.__file__)),('gravity_results.json',Path(gs.__file__))]:
        r=json.loads((HERE/result).read_text())
        sha=r.get('source_sha256',r.get('source_hashes',{}).get('finite_scalar'))
        gate(result+' matches delivered source',sha==hashlib.sha256(source.read_bytes()).hexdigest(),sha)
        gate(result+' semantic pass',r['status']=='passed',r['status'])
    after={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in bound}
    gate('No source or contract changed during root validation',before==after,before)
    result=dict(status='passed',checks=CHECKS,passed_checks=len(CHECKS),source_hashes=before,
                scope='Finite regulator and bounded classical gravity; no common quantum stress closure',
                review='Root completed code audit after child-agent usage limit; no claim of finished agent code review')
    (HERE/'root_validation.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'passed_checks':len(CHECKS)}))

if __name__=='__main__':
    main()
