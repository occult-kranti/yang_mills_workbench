"""Reproduce exact SU(2) convolution spectra, checks, CSVs and static figures."""
import csv
import hashlib
import json
import math
import platform
from pathlib import Path
import sys
import numpy as np
import scipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from su2_transfer import (eigenvalue_record, decimal_reference, gap_record,
                          haar_character_quadrature, negative_beta_control,
                          NumericalDomainError, log_normalization)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'output'


def hash_sources():
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [ROOT/'su2_transfer.py', ROOT/'run_benchmark.py']}


def run_checks():
    checks=[]
    def gate(name, ok, **evidence):
        record=dict(name=name, passed=bool(ok), **evidence)
        checks.append(record)
        if not ok:
            OUT.mkdir(exist_ok=True)
            (OUT/'failure.json').write_text(json.dumps(checks, indent=2, allow_nan=False))
            raise RuntimeError('FAILED GATE: '+name)
    def rejects(name, function):
        try:
            function()
        except NumericalDomainError:
            gate(name, True)
        else:
            gate(name, False)

    for beta in [0., 1e-12, .1, 1., 10., 1000., 1e6]:
        row=eigenvalue_record(beta,1)
        gate('constant mode beta='+str(beta), row['ratio']==1 and row['dimensionless_energy']==0)
    zero=eigenvalue_record(0.,2)
    gate('beta=0 is exact projection; no manufactured finite energy', zero['ratio']==0 and zero['dimensionless_energy'] is None)
    for beta in [1e-300, 1e-10, .01, .1, 1., 10., 100., 1000.]:
        for n in [2,5,12]:
            row=eigenvalue_record(beta,n)
            ref=decimal_reference(beta,n,80)
            difference=abs(row['log_ratio']-ref['log_ratio'])
            # A log error is a relative multiplicative eigenvalue error to first order.
            gate('Decimal log ratio beta=%g n=%d'%(beta,n), difference < 2e-11,
                 absolute_log_error=difference)
    # Direct Haar/character integration is independent of the Bessel series and AMOS.
    for beta,n in [(.1,2),(1.,2),(1.,5),(10.,2),(10.,7),(100.,2),(1000.,2),(1000.,9)]:
        low=haar_character_quadrature(beta,n,128)
        high=haar_character_quadrature(beta,n,256)
        exact=eigenvalue_record(beta,n)['ratio']
        relative=abs(high['ratio']/exact-1)
        refinement=abs(high['ratio']-low['ratio'])
        normalization_error=abs(high['log_Z']-log_normalization(beta))
        gate('Haar quadrature beta=%g n=%d'%(beta,n), relative < 1e-10 and refinement < 1e-10 and normalization_error < 1e-10,
             relative_eigenvalue_error=relative, absolute_refinement=refinement,
             log_Z_error=normalization_error)
    for beta in [.01, .1, 1., 10., 100., 1000., 1e6]:
        spectrum=[eigenvalue_record(beta,n) for n in range(1,33)]
        logs=[r['log_ratio'] for r in spectrum]
        gate('ordered positive spectrum beta='+str(beta),
             all(math.isfinite(x) for x in logs) and all(b<a for a,b in zip(logs,logs[1:])))
        row=gap_record(beta)
        gate('Doeblin lower bound beta='+str(beta), math.log(row['markov_gap']) >= row['log_doeblin_lower_bound']-1e-12)
    for n in [2,3,5,10]:
        row=eigenvalue_record(1e6,n)
        leading=(n*n-1)/2
        relative=abs(1e6*row['dimensionless_energy']/leading-1)
        gate('large beta Casimir limit n='+str(n), relative < 1e-6, relative_error=relative)
    for n in [2,3,5]:
        beta=1e-5
        leading=(n-1)*math.log(beta/2)-math.lgamma(n+1)
        error=abs(eigenvalue_record(beta,n)['log_ratio']-leading)
        gate('small beta power law n='+str(n), error < 1e-10, absolute_log_error=error)
    rare=eigenvalue_record(.1,4096)
    gate('positive eigenvalue underflow retains finite logarithm', rare['ratio'] is None and rare['log_ratio'] < -10000 and math.isfinite(rare['log_ratio']), status=rare['status'])
    overflow=gap_record(1e6)
    gate('large beta normalization uses log domain', math.isfinite(log_normalization(1e6)) and overflow['physical_gap']>0)
    small_norm=log_normalization(1e-100)
    gate('tiny beta normalization cancellation resolved', small_norm>0 and abs(small_norm/(1e-200/8)-1)<1e-13,
         log_Z=small_norm)
    counter=negative_beta_control(-2.,2)
    direct=haar_character_quadrature(-2.,2,256)
    gate('positive pointwise kernel has negative spectral eigenvalue', counter['ratio']<0 and abs(counter['ratio']-direct['ratio'])<1e-13,
         negative_eigenvalue=counter['ratio'])
    # Mutants model concrete normalization/sign mistakes and must be distinguishable.
    exact=eigenvalue_record(2.,2)['ratio']
    direct=haar_character_quadrature(2.,2,256)['ratio']
    gate('missing representation dimension mutant detected', abs(2*direct-exact)>.1)
    gate('wrong Bessel order mutant detected', abs(eigenvalue_record(2.,3)['ratio']-direct)>.1)
    gate('full and class multiplicity distinguished', eigenvalue_record(2.,3)['multiplicity_full']==9 and eigenvalue_record(2.,3)['multiplicity_class']==1)
    for value in [-1., float('nan'), float('inf'), 1e7, True, '1']:
        rejects('invalid beta '+repr(value), lambda value=value: eigenvalue_record(value,2))
    for value in [0, -1, 1.5, 4097, True]:
        rejects('invalid representation '+repr(value),lambda value=value:eigenvalue_record(2.,value))
    for value in [0., -1., float('inf'), float('nan'), True]:
        rejects('invalid time step '+repr(value),lambda value=value:gap_record(2.,value))
    rejects('physical-unit overflow rejected',lambda:gap_record(1.,1e-320))
    rejects('large-order scaled underflow outside fallback rejected', lambda:eigenvalue_record(1001.,4096))
    rejects('quadrature out of scope rejected',lambda:haar_character_quadrature(1001.,2))
    rejects('invalid reference precision rejected',lambda:decimal_reference(1.,2,2))
    rejects('negative control positive beta rejected',lambda:negative_beta_control(2.,2))
    rejects('unrepresentable positive log Z rejected',lambda:log_normalization(1e-300))
    tiny=decimal_reference(1e-300,1)
    gate('unrepresentable log Z explicitly retained in Decimal',tiny['log_Z'] is None and tiny['log_Z_status']=='positive_below_float_range' and tiny['log_Z_decimal']!='0')
    gate('nonempty evaluated check set',len(checks)>0)
    return checks


def save_csv(name, rows):
    if not rows:
        raise RuntimeError('empty CSV '+name)
    with (OUT/name).open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)


def main():
    OUT.mkdir(exist_ok=True)
    source_hashes=hash_sources()
    checks=run_checks()
    # First plot has no arbitrary temporal scale: exact dimensionless generator energies.
    betas=np.geomspace(.01,1e5,121)
    spectra=[]
    for beta in betas:
        for n in [2,3,4,5]:
            r=eigenvalue_record(float(beta),n)
            spectra.append({k:r[k] for k in ['beta','j','n','multiplicity_full','multiplicity_class','ratio','dimensionless_energy']})
    save_csv('su2_spectra.csv',spectra)
    plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False})
    fig,ax=plt.subplots(figsize=(8,5),layout='constrained')
    for n in [2,3,4,5]:
        points=[r for r in spectra if r['n']==n]
        ax.loglog([r['beta'] for r in points],[r['dimensionless_energy'] for r in points],label='j=%g'%((n-1)/2))
    ax.loglog(betas,1.5/betas,'k--',alpha=.55,label=r'$3/(2\beta)$ asymptote, j=1/2')
    ax.set(xlabel=r'$\beta$',ylabel=r'$-\log(I_{2j+1}/I_1)$',title='Exact SU(2) rotor spectrum: finite parameter, decreasing gap')
    ax.legend();ax.grid(True,which='major',alpha=.15)
    fig.savefig(OUT/'su2-spectrum.png',dpi=180);plt.close(fig)
    # a_t=beta^{-p} in chosen time units; all paths have a_t -> 0.
    path_rows=[]
    for beta in np.geomspace(10,1e6,101):
        for p in [.5,1.,1.5]:
            a_t=float(beta**(-p))
            row=gap_record(float(beta),a_t)
            path_rows.append({'beta':float(beta),'time_exponent_p':p,'time_step':a_t,
                              'dimensionless_gap':row['dimensionless_energy'],
                              'physical_gap_in_chosen_units':row['physical_gap'],
                              'large_beta_asymptote':1.5*float(beta**(p-1))})
    save_csv('su2_joint_limits.csv',path_rows)
    fig,ax=plt.subplots(figsize=(8,5),layout='constrained')
    names={.5:'p=1/2: gap tends to 0',1.:'p=1: gap tends to 3/2',1.5:'p=3/2: gap diverges'}
    for p in [.5,1.,1.5]:
        points=[r for r in path_rows if r['time_exponent_p']==p]
        ax.loglog([r['beta'] for r in points],[r['physical_gap_in_chosen_units'] for r in points],label=names[p])
    ax.set(xlabel=r'$\beta\to\infty$, with $a_t=\beta^{-p}\to0$',ylabel='Generator gap in chosen time units',
           title='Three continuum-time paths; positivity does not choose a scale')
    ax.legend();ax.grid(True,which='major',alpha=.15)
    fig.savefig(OUT/'su2-joint-limits.png',dpi=180);plt.close(fig)
    examples=[gap_record(b) for b in [.01,.1,1.,2.,10.,100.,1000.,1e6]]
    after=hash_sources()
    if source_hashes != after:
        raise RuntimeError('source changed during run')
    summary={'status':'passed','scope':'exact single SU(2) central-convolution operator, not full 4D Yang--Mills',
             'check_count':len(checks),'checks':checks,'source_sha256':source_hashes,
             'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform()},
             'examples':examples,'negative_beta_control':negative_beta_control(),
             'limitations':['High precision uses Python Decimal positive series, not interval arithmetic.',
              'Quadrature checks are numerical comparisons, not substitutes for the analytic spectrum proof.',
              'Asymptotics hold for fixed representation; the benchmark is not a uniform large-spin theorem.',
              'No spatial plaquette coupling, local gauge projection, continuum 4D construction or Yang--Mills mass gap established.']}
    (OUT/'validation.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':'passed','checks':len(checks),'output':str(OUT),'source_sha256':source_hashes}))


if __name__=='__main__':
    main()
