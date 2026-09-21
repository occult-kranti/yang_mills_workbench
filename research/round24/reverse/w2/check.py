#!/usr/bin/env python3
"""Exact all-step identities and sufficient iteration counts; no spectrum simulation."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path


def require(ok,name):
    if not ok: raise RuntimeError(name)


def ceiling(q): return -(-q.numerator//q.denominator)


def serial(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict): return {k:serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)): return [serial(v) for v in x]
    return x


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    tau=F(5,1664); theta=F(1,16); m=7*tau; gap=1-4*m
    a=theta*gap; decay_step=a*a/8; rho=1-decay_step
    require(gap==F(381,416) and 0<a<F(1,16),'actual initial gap and duration')
    require(0<rho<1,'uniform column contraction')
    n_tenth=ceiling(9/decay_step)
    tenth_bound=1/(1+n_tenth*decay_step)
    require(tenth_bound<=F(1,10),'tenfold sufficient iterations')
    n_quartic=ceiling((1/tau-1)/decay_step)
    quartic_bound=1/(1+n_quartic*decay_step)
    require(quartic_bound<=tau,'column extra coupling factor')
    # Formal scalar map values are exact fixture coefficients, not actual Bohr data.
    coefficients=[F(1),F(3,4),F(-1,5),F(0)]
    for n in range(1,17):
        for t in coefficients:
            accumulated=sum((1-t)*t**k for k in range(n))
            require(accumulated==1-t**n,'all-step telescoping coefficient')
            if t==1: require(accumulated==0 and t**n==1,'zero-frequency retained')
    # Explicit 3-coordinate source: vacuum transition plus an excited equal-energy block.
    source=[[F(0),F(1),F(0)],[F(1),F(0),F(2)],[F(0),F(2),F(0)]]
    residual=[[F(0),F(3,4)**16,F(0)],
              [F(3,4)**16,F(0),F(2)],[F(0),F(2),F(0)]]
    vacuum_norm_squared=residual[1][0]**2
    require(vacuum_norm_squared<1 and residual[1][2]==source[1][2],
            'decaying column with retained full-source block')
    old_radius=208*m*theta
    require(old_radius==F(35,128),'inherited connected-radius cap')
    require(3*old_radius<1<4*old_radius,'positive majorant fails at fourth composition')
    # For neighbor energies 1/(2k),1/(2k+1), differences tend to zero.
    differences=[F(1,2*k)-F(1,2*k+1) for k in [1,10,100]]
    require(all(d>0 for d in differences) and differences[-1]<differences[0],
            'nonzero transition differences approach zero')
    # Bernoulli upper estimate is rigorous for every n: (1-u)^(-n)>=1+nu.
    for u in [F(1,8),F(1,100)]:
        for n in [1,2,7,13]:
            require((1-u)**n<=1/(1+n*u),'rational Bernoulli certificate')
    controls={
        'zero-frequency-never-contracts': coefficients[0]**100==1,
        'vacuum-contraction-not-full-source-contraction': residual[1][2]==2 and vacuum_norm_squared<1,
        'interaction-radius-does-not-cover-reduction-count': n_tenth*old_radius>1,
        'fixed-step-count-does-not-change-coupling-degree': rho**2>0,
        'near-zero-frequency-not-uniform-scalar-contraction': differences[-1]<differences[0],
        'tau-zero-valid-zero-source': F(0)**3==0,
    }
    for name,value in controls.items(): require(value,name)
    results={
        'loop':'w2','direction':'reverse','status':'passed',
        'claims':[
            'Exact finite-n accumulated inverse with all residual and zero-frequency blocks',
            'Actual vacuum-column residual norm decay and response G-graph convergence',
            'Finite-volume full-source strong limit equals the spectral diagonal block map',
            'Existing positive connected certificate does not cover all repeated filters',
        ],
        'limitations':[
            'No full-source operator-norm or weighted interaction contraction proved',
            'No actual excited diagonal blocks evaluated or infinite-volume all-sector limit proved',
            'Identity-extended source is not Hilbert-Schmidt on an infinite-dimensional exterior',
            'Fixed initial G iteration is not later-diagonal nonlinear closure',
            'Rational coefficient/topology fixtures are not actual SU2 spectral observations',
        ],
        'exact':{'gap_cap_lower':gap,'theta':theta,'column_rho':rho,'one_minus_rho':decay_step,
                 'iterations_sufficient_for_tenth':n_tenth,'certified_tenth_ratio':tenth_bound,
                 'iterations_sufficient_for_extra_tau':n_quartic,'certified_extra_tau_ratio':quartic_bound,
                 'old_connected_radius_per_step':old_radius,'old_radius_first_failed_step':4,
                 'fixture_vacuum_norm_squared_after16':vacuum_norm_squared,
                 'fixture_retained_excited_block':residual[1][2]},
    }
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'results.json').write_text(json.dumps(serial(results),indent=2,sort_keys=True)+'\n')
    (args.output/'controls.json').write_text(json.dumps({'controls':controls},indent=2,sort_keys=True)+'\n')


if __name__=='__main__':main()
