"""Independent P3 response verification, using complex two-component spinors.

This module never imports a production solver or its right-hand side. It uses
central pump differences, separately evolved spinor tangents, exact work
identities and deliberately broken controls at a stated finite regulator.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, replace
from pathlib import Path
import argparse
import hashlib
import json
import math
import sys

import numpy as np
import scipy
from scipy.integrate import quad, solve_ivp
from scipy.special import digamma

ROOT = Path(__file__).resolve().parent
E2 = 4 * math.pi / 137.035999084
BUMP_INTEGRAL = quad(lambda u: math.exp(-1 / (u * (1-u))), 0, 1,
                     epsabs=2e-15, epsrel=2e-13)[0]


@dataclass(frozen=True)
class Config:
    b: float = 10.
    nmax: int = 2
    Kmax: float = 6.
    nK: int = 32
    amplitude: float = 1.
    pump_duration: float = 4.
    final_time: float = 8.
    samples: int = 81
    a0: float = 0.
    translated_grid: bool = True
    rtol: float = 2e-11
    atol: float = 2e-13
    max_step: float = .02


def bump(t, duration, start=0.):
    u = (t-start)/duration
    if not 0 < u < 1:
        return 0.
    return math.exp(-1/(u*(1-u))) / (duration * BUMP_INTEGRAL)


def simulate(cfg=Config(), tangent=True, mutation=None, probe=None,
             gauge_tangent=False):
    """Independent complex spinors; optional source or pure-gauge tangent.

    mutation='omit_deltaZ' deletes the quotient derivative alone.
    mutation='freeze_mode_response' deletes the full dynamical eta_z term
    in delta current. It is a deliberately erroneous frozen-mode response,
    not a consistent alternate quantum approximation.
    """
    nodes, wk = np.polynomial.legendre.leggauss(cfg.nK)
    ns = np.arange(cfg.nmax + 1)
    k = np.tile(cfg.Kmax*nodes + (cfg.a0 if cfg.translated_grid else 0.), len(ns))
    mass = np.repeat(np.sqrt(1+2*cfg.b*ns), cfg.nK)
    weights = np.concatenate([cfg.Kmax*wk*cfg.b*(1 if n == 0 else 2)/(4*math.pi**2)
                              for n in ns])
    size = len(k)
    chi = E2/(12*math.pi**2)*(cfg.b-math.log(2*cfg.b)-digamma(1+1/(2*cfg.b)))
    p0 = k-cfg.a0
    angle = np.arctan2(mass, p0)
    psi0 = np.array([-np.sin(angle/2), np.cos(angle/2)], dtype=complex)
    # State: a,x,work, psi0[all modes],psi1[all modes], then v,u,dwork,dpsi.
    initial = np.concatenate(([cfg.a0, 0., 0.], psi0.ravel()))
    block = len(initial)
    if tangent:
        delta = np.zeros_like(initial)
        if gauge_tangent:
            delta[0] = 1.  # delta k=delta a=1 leaves p and vacuum unchanged.
        initial = np.concatenate((initial, delta))

    def read(y):
        a, x = y[0].real, y[1].real
        psi = y[3:block].reshape(2, size)
        p = k-a
        omega = np.sqrt(mass**2+p**2)
        rx = 2*(psi[0].conj()*psi[1]).real
        rz = (abs(psi[0])**2-abs(psi[1])**2)
        current = weights @ (rz + p/omega)
        C = weights @ (mass**2/(4*omega**5))
        D = weights @ (5*mass**2*p/(8*omega**7))
        Z = 1+chi-E2*C
        if Z <= .05:
            raise ArithmeticError('Regulator yields an ill-conditioned kinetic coefficient')
        return a, x, psi, p, omega, rx, rz, current, C, D, Z

    def h_apply(psi, p):
        return np.array([p*psi[0]+mass*psi[1], mass*psi[0]-p*psi[1]])

    def derivative(t, y):
        a,x,psi,p,omega,rx,rz,current,C,D,Z = read(y)
        force = cfg.amplitude*bump(t, cfg.pump_duration)
        dx = (force-E2*(current+D*x*x))/Z
        dpsi = -1j*h_apply(psi, p)
        out = np.concatenate(([-x,dx,x*force], dpsi.ravel()))
        if not tangent:
            return out
        v,u = y[block].real,y[block+1].real
        dpsi_state = y[block+3:].reshape(2,size)
        q = (1. if gauge_tangent else 0.)-v
        eta_z = 2*(psi[0].conj()*dpsi_state[0]-psi[1].conj()*dpsi_state[1]).real
        delta_current = weights @ (eta_z+mass**2*q/omega**3)
        if mutation == 'freeze_mode_response':
            delta_current = weights @ (mass**2*q/omega**3)
        delta_C = weights @ (-5*mass**2*p*q/(4*omega**7))
        delta_D = weights @ (5*mass**2*(mass**2-6*p*p)*q/(8*omega**9))
        delta_force = 0. if gauge_tangent else (bump(t, cfg.pump_duration) if probe is None
                       else bump(t, probe[1], probe[0]))
        delta_dx = (delta_force-E2*(delta_current+delta_D*x*x+2*D*x*u)
                    +(0. if mutation == 'omit_deltaZ' else E2*delta_C*dx))/Z
        ddpsi = -1j*(h_apply(dpsi_state,p)+q*np.array([psi[0],-psi[1]]))
        return np.concatenate((out,[-u,delta_dx,u*force+x*delta_force],ddpsi.ravel()))

    times = np.linspace(0,cfg.final_time,cfg.samples)
    sol = solve_ivp(derivative,(0,cfg.final_time),initial,method='DOP853',t_eval=times,
                    rtol=cfg.rtol,atol=cfg.atol,max_step=cfg.max_step)
    if not sol.success:
        raise RuntimeError(sol.message)
    energies, delta_energies, norms, tangent_norms, bloch_tangent_norms, z_values = [], [], [], [], [], []
    currents, delta_currents = [], []
    for time,state in zip(times,sol.y.T):
        a,x,psi,p,omega,rx,rz,current,C,D,Z = read(state)
        deriv = derivative(time,state)
        dx = deriv[1].real
        currents.append(float(current-C*dx+D*x*x+chi*dx/E2))
        energy = Z*x*x/2+E2*(weights @ (mass*rx+p*rz+omega))
        energies.append(float(energy)); z_values.append(float(Z))
        norms.append(float(np.max(abs(np.sum(abs(psi)**2,axis=0)-1))))
        if tangent:
            v,u = state[block].real,state[block+1].real
            dpsi = state[block+3:].reshape(2,size)
            q = (1. if gauge_tangent else 0.)-v
            eta_x = 2*(psi[0].conj()*dpsi[1]+psi[1].conj()*dpsi[0]).real
            eta_y = 2*(-1j*psi[0].conj()*dpsi[1]+1j*psi[1].conj()*dpsi[0]).real
            eta_z = 2*(psi[0].conj()*dpsi[0]-psi[1].conj()*dpsi[1]).real
            ry = 2*(psi[0].conj()*psi[1]).imag
            delta_C = weights @ (-5*mass**2*p*q/(4*omega**7))
            delta_D = weights @ (5*mass**2*(mass**2-6*p*p)*q/(8*omega**9))
            delta_current0 = weights @ (eta_z+mass**2*q/omega**3)
            delta_dx = deriv[block+1].real
            delta_currents.append(float(delta_current0-delta_C*dx-C*delta_dx+
                                        delta_D*x*x+2*D*x*u+chi*delta_dx/E2))
            delta_U = weights @ (mass*eta_x+p*eta_z+q*(rz+p/omega))
            delta_energies.append(float(Z*x*u-E2*delta_C*x*x/2+E2*delta_U))
            tangent_norms.append(float(np.max(abs(2*np.sum(psi.conj()*dpsi,axis=0).real))))
            bloch_tangent_norms.append(float(np.max(abs(rx*eta_x+ry*eta_y+rz*eta_z))))
    energy = np.array(energies)
    result = {'config':asdict(cfg),'t':times.tolist(),'x':sol.y[1].real.tolist(),
              'a_relative':(sol.y[0].real-cfg.a0).tolist(),'energy':energies,
              'current_renormalized':currents,
              'energy_work_max_abs_residual':float(np.max(abs(energy-energy[0]-sol.y[2].real))),
              'spinor_norm_max_residual':max(norms),'Z_min':min(z_values),
              'nfev':sol.nfev,'mutation':mutation,'probe':probe,'gauge_tangent':gauge_tangent}
    if tangent:
        de = np.array(delta_energies)
        u = sol.y[block+1].real
        scale = max(abs(sol.y[1].real))
        dwork = sol.y[block+2].real
        work_scale = max(float(np.max(abs(de))), float(np.max(abs(dwork))))
        residual = float(np.max(abs(de-de[0]-dwork)))
        result.update({'dx_damplitude':u.tolist(),'da_damplitude':sol.y[block].real.tolist(),
                       'dcurrent_damplitude':delta_currents,
                       'delta_energy':delta_energies,'delta_work':dwork.tolist(),
                       'tangent_energy_work_max_abs_residual':residual,
                       'tangent_energy_scale':work_scale,
                       'tangent_energy_work_relative_residual':residual/work_scale if work_scale else None,
                       'spinor_tangent_normalization_max_residual':max(tangent_norms),
                       'bloch_tangent_orthogonality_max_residual':max(bloch_tangent_norms),
                       'global_field_scale':float(scale),
                       'amplitude_weighted_gain':float(abs(cfg.amplitude)*max(abs(u))/scale) if scale and cfg.amplitude else None,
                       'response_max_abs':float(max(abs(u)))})
    return result


def finite_difference_suite(cfg, tangent_reference, steps=(.002,.001,.0005,.00025,.000125,.0000625)):
    out = []
    for step in steps:
        plus = simulate(replace(cfg,amplitude=cfg.amplitude+step),tangent=False)
        minus = simulate(replace(cfg,amplitude=cfg.amplitude-step),tangent=False)
        dx = (np.array(plus['x'])-np.array(minus['x']))/(2*step)
        da = (np.array(plus['a_relative'])-np.array(minus['a_relative']))/(2*step)
        dj = (np.array(plus['current_renormalized'])-np.array(minus['current_renormalized']))/(2*step)
        out.append({'step':step,'dx_damplitude':dx.tolist(),'da_damplitude':da.tolist(),
                    'dcurrent_damplitude':dj.tolist(),
                    'max_field_derivative_difference':float(max(abs(dx-np.array(tangent_reference['dx_damplitude'])))),
                    'max_current_derivative_difference':float(max(abs(dj-np.array(tangent_reference['dcurrent_damplitude'])))),
                    'max_potential_derivative_difference':float(max(abs(da-np.array(tangent_reference['da_damplitude']))))})
    for previous,current in zip(out,out[1:]):
        current['observed_field_difference_order']=math.log(previous['max_field_derivative_difference']/current['max_field_derivative_difference'],2)
    return out


def compare_production(path, reference):
    """Compare frozen numerical output only, without importing its code."""
    data=json.loads(Path(path).read_text())
    if 'time' in data: times=data['time']
    elif 't' in data: times=data['t']
    else: raise KeyError('Expected time or t in frozen production JSON')
    # Avoid interpolation hiding discrepancies: same stated sample grid required.
    if not np.allclose(times,reference['t'],rtol=0,atol=2e-13):
        raise ValueError('Production and verification sample times differ')
    response_key=next((key for key in ['dx_damplitude','u','delta_x','dx_dtarget'] if key in data),None)
    potential_key=next((key for key in ['da_damplitude','v','delta_a','da_dtarget'] if key in data),None)
    if response_key is None or potential_key is None:
        raise KeyError('Expected sampled field and potential tangents')
    return {'path':str(path),'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),
            'field_tangent_max_abs_difference':float(max(abs(np.array(data[response_key])-reference['dx_damplitude']))),
            'potential_tangent_max_abs_difference':float(max(abs(np.array(data[potential_key])-reference['da_damplitude'])))}


def run_all():
    cfg=Config()
    baseline=simulate(cfg)
    heldout_cfg=replace(cfg,b=3.,amplitude=.5,pump_duration=6.,final_time=18.,samples=181)
    heldout=simulate(heldout_cfg)
    finite_differences=finite_difference_suite(cfg,baseline)
    heldout_fd=finite_difference_suite(heldout_cfg,heldout)
    mutants={name:simulate(cfg,mutation=name) for name in ['omit_deltaZ','freeze_mode_response']}
    gauge=simulate(replace(cfg,a0=7.3))
    wrong_window=simulate(replace(cfg,a0=7.3,translated_grid=False))
    gauge_direction=simulate(cfg,gauge_tangent=True)
    delayed=simulate(heldout_cfg,probe=(9.,3.))
    zero=simulate(replace(cfg,amplitude=0.))
    gauge_difference=float(max(abs(np.array(gauge['dx_damplitude'])-baseline['dx_damplitude'])))
    wrong_window_difference=float(max(abs(np.array(wrong_window['dx_damplitude'])-baseline['dx_damplitude'])))
    mutant_summary={name:{'tangent_field_max_difference':float(max(abs(np.array(row['dx_damplitude'])-baseline['dx_damplitude']))),
                         'tangent_work_max_residual':row['tangent_energy_work_max_abs_residual']}
                    for name,row in mutants.items()}
    pre=np.array(delayed['t'])<=9.
    causality=float(max(abs(np.array(delayed['dx_damplitude'])[pre])))
    checks={
      'independent_fd_field_reference':finite_differences[-1]['max_field_derivative_difference']<2e-7,
      'heldout_fd_field_reference':heldout_fd[-1]['max_field_derivative_difference']<2e-7,
      'baseline_tangent_work_identity':baseline['tangent_energy_work_max_abs_residual']<2e-8,
      'heldout_tangent_work_identity':heldout['tangent_energy_work_max_abs_residual']<2e-8,
      'spinor_tangent_normalization':baseline['spinor_tangent_normalization_max_residual']<2e-8,
      'bloch_tangent_orthogonality':baseline['bloch_tangent_orthogonality_max_residual']<4e-8,
      'translated_gauge_tangent':gauge_difference<2e-10,
      'wrong_window_detected':wrong_window_difference>1e-4,
      'pure_gauge_direction_zero_field':gauge_direction['response_max_abs']<2e-12,
      'delayed_probe_causal':causality<2e-12,
      'missing_deltaZ_detected':mutant_summary['omit_deltaZ']['tangent_work_max_residual']>2e-7,
      'frozen_mode_response_detected':mutant_summary['freeze_mode_response']['tangent_field_max_difference']>1e-3,
      'zero_amplitude_linear_response_finite':math.isfinite(zero['response_max_abs']) and zero['response_max_abs']>.5,
    }
    return {'baseline':baseline,'heldout':heldout,'finite_differences':finite_differences,
       'heldout_finite_differences':heldout_fd,'mutants':mutant_summary,
       'gauge':{'translated_tangent_max_difference':gauge_difference,
                'wrong_window_tangent_max_difference':wrong_window_difference,
                'pure_gauge_field_tangent_max_abs':gauge_direction['response_max_abs']},
       'delayed_probe':{'start':9.,'duration':3.,'max_response_before_start':causality,
                        'max_response_after_start':delayed['response_max_abs']},
       'zero_amplitude':{'response_max_abs':zero['response_max_abs'],
                        'global_field_scale':zero['global_field_scale'],
                        'relative_gain_is_defined':False,
                        'explanation':'At identically zero prescribed amplitude the global baseline field is zero up to numerical noise. Report absolute response; never divide by its numerical residual.'},
       'checks':checks,'all_checks_passed':all(checks.values()),
       'provenance':{'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__,
                     'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     'production_solver_imported':False},
       'scope':'Finite-regulator derivative of a semiclassical initial-value model. This is not a quantum current-noise kernel, a renormalized retarded commutator calculation, a continuum error certificate, or proof of semiclassical validity.'}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--production')
    parser.add_argument('--heldout-production')
    parser.add_argument('--reuse',action='store_true')
    args=parser.parse_args()
    path=ROOT/'response_verification.json'
    data=json.loads(path.read_text()) if args.reuse else run_all()
    for key,file,reference in [('production_comparison',args.production,'baseline'),
                               ('heldout_production_comparison',args.heldout_production,'heldout')]:
        if file:
            data[key]=compare_production(file,data[reference])
            data['checks'][key]=data[key]['field_tangent_max_abs_difference']<2e-8 and data[key]['potential_tangent_max_abs_difference']<2e-8
    data['all_checks_passed']=all(data['checks'].values())
    path.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'checks':data['checks'],'mutants':data['mutants'],
                      'finite_difference_errors':[r['max_field_derivative_difference'] for r in data['finite_differences']],
                      'heldout_finite_difference_errors':[r['max_field_derivative_difference'] for r in data['heldout_finite_differences']]},indent=2))
    if not data['all_checks_passed']:
        raise AssertionError('One or more verification gates failed; inspect recorded evidence')


if __name__=='__main__':
    main()
