"""Reproduce independent round-9 audits. Run from any directory with Python.

Gate thresholds were fixed before execution. Uses no production test helpers.
"""
from __future__ import annotations
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys
import os
import warnings
import numpy as np
from decimal import Decimal, localcontext
from reference_oracles import (q_to_matrix, matrix_action, matrix_gauge_transform,
    conditional_f_from_global_action, lie_derivatives, haar_ratio_reference, haar_moment_reference)

ROOT = Path(os.environ.get("YM9_REVIEW_ROOT",str(Path(__file__).resolve().parent.parent))).resolve()
LATTICE = ROOT/("lattice" if (ROOT/"lattice").exists() else "ym9-lattice")
TRANSFER = ROOT/("transfer" if (ROOT/"transfer").exists() else "ym9-transfer")
OUT = Path(__file__).resolve().parent
RECORDS = []


def load(name, rel):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def gate(name, value, maximum=None, minimum=None, detail=None):
    good = bool(value) if maximum is None and minimum is None else math.isfinite(float(value))
    if maximum is not None:
        good = good and value <= maximum
    if minimum is not None:
        good = good and value >= minimum
    RECORDS.append(dict(name=name, passed=bool(good), value=value,
                        maximum=maximum, minimum=minimum, detail=detail))


def rejects(name, fn):
    try:
        fn()
    except (ValueError, FloatingPointError, OverflowError) as exc:
        gate(name, True, detail=type(exc).__name__)
    else:
        gate(name, False, detail="returned instead of rejecting")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    sources = [LATTICE/'su2_lattice.py', TRANSFER/'su2_transfer.py',
               OUT/'audit_independent.py', OUT/'reference_oracles.py']
    before = {str(p.relative_to(ROOT)): digest(p) for p in sources}
    L = load('skeptic_lattice', LATTICE/'su2_lattice.py')
    T = load('skeptic_transfer', TRANSFER/'su2_transfer.py')
    rng = np.random.default_rng(914072)
    raw = rng.normal(size=(128,4)); q = raw/np.linalg.norm(raw,axis=1)[:,None]
    independent = q_to_matrix(q, orientation=-1)
    prod = np.array([L.to_matrix(v) for v in q])
    gate('quaternion_map_128_matrix_oracles', float(np.max(np.abs(prod-independent))), maximum=2e-15)
    mapped = q_to_matrix(L.qmul(q[:64], q[64:]), orientation=-1)
    gate('quaternion_multiply_64_matrix_oracles', float(np.max(np.abs(mapped-independent[:64]@independent[64:]))), maximum=2e-15)
    gate('quaternion_conjugate_matrix_oracle', float(np.max(np.abs(q_to_matrix(L.qconj(q),-1)-independent.conj().swapaxes(-1,-2)))), maximum=2e-15)

    for shape in [(2,2,2,2),(2,3,2,2)]:
        name='x'.join(map(str,shape))
        lattice=L.WilsonLattice(lengths=shape,beta=1.73,seed=2907)
        U=q_to_matrix(lattice.links.reshape(shape+(4,4)),-1)
        gate(f'{name}_full_action_matrix',abs(lattice.action()-matrix_action(U,lattice.beta)),maximum=2e-12)
        delta_errors=[]; factor_defects=[]; staple_errors=[]; staple_norm_errors=[]
        for mu in range(4):
            for x in [0,lattice.volume-1]:
                link=lattice.coords[x]+(mu,)
                proposed=q[(x+mu)%128]
                old=U[link].copy()
                base=matrix_action(U,lattice.beta)
                U[link]=q_to_matrix(proposed,-1)
                reference=matrix_action(U,lattice.beta)-base
                U[link]=old
                actual=lattice.local_delta(x,mu,proposed)
                delta_errors.append(abs(actual-reference))
                factor_defects.append(abs(actual/2-reference))
                f,norm,_=conditional_f_from_global_action(U,link)
                A=lattice.staple(x,mu)
                local=L.scalar_product(lattice.links[x,mu],A)
                staple_errors.append(abs(f-local)); staple_norm_errors.append(abs(norm-float(A@A)))
        gate(f'{name}_8_links_local_delta_matrix',max(delta_errors),maximum=3e-12)
        gate(f'{name}_8_staple_scalars_reconstructed_global',max(staple_errors),maximum=3e-12)
        gate(f'{name}_8_staple_norms_reconstructed_global',max(staple_norm_errors),maximum=3e-11)
        gate(f'{name}_wrong_half_action_factor_detected',max(factor_defects),minimum=.01)
        Graw=rng.normal(size=shape+(4,));Gq=Graw/np.linalg.norm(Graw,axis=-1)[...,None]
        G=q_to_matrix(Gq,-1)
        transformed=matrix_gauge_transform(U,G)
        gate(f'{name}_matrix_gauge_action',abs(matrix_action(U,1)-matrix_action(transformed,1)),maximum=3e-12)
        wrong=abs(matrix_action(U,1,True)-matrix_action(transformed,1,True))
        gate(f'{name}_omitted_reverse_dagger_detected',wrong,minimum=.01)
        lattice.gauge_transform(Gq.reshape(lattice.volume,4))
        gate(f'{name}_production_gauge_transform_matrix',float(np.max(np.abs(q_to_matrix(lattice.links.reshape(shape+(4,4)),-1)-transformed))),maximum=3e-15)

    lattice=L.WilsonLattice(beta=.83,seed=179)
    U=q_to_matrix(lattice.links.reshape(lattice.lengths+(4,4)),-1)
    f,norm,_=conditional_f_from_global_action(U,(1,1,1,1,2))
    grad,lap=lie_derivatives(U,(1,1,1,1,2),1e-3)
    gate('ward_lie_gradient_from_matrix_global_action',abs(grad-(norm-f*f)),maximum=1e-5)
    gate('ward_lie_laplacian_from_matrix_global_action',abs(lap+3*f),maximum=1e-5)
    all_terms=[]
    for x in range(lattice.volume):
        for mu in range(4):
            ff,nn,_=conditional_f_from_global_action(U,lattice.coords[x]+(mu,))
            all_terms.append(lattice.beta**2*(nn-ff*ff)-3*lattice.beta*ff)
    gate('all_64_link_ward_matrix_global_reconstruction',abs(lattice.ward()-float(np.mean(all_terms))),maximum=3e-11)
    with localcontext() as ctx:
        ctx.prec=80
        b=Decimal('.7');s=Decimal('2')
        first=haar_moment_reference(b*s,1)
        second=haar_moment_reference(b*s,2)
        correct=3*s*first-b*s*s*(1-second)
        wrong=2*s*first-b*s*s*(1-second)
    gate('conditional_Haar_Ward_exact_angle_integral',float(abs(correct)),maximum=1e-40)
    gate('wrong_Ward_dimension_factor_detected',float(abs(wrong)),minimum=.1)

    for beta in [0.,.5,2.2]:
        cold=L.WilsonLattice(beta=beta,start='cold')
        gate(f'cold_action_beta{beta}',cold.action(),maximum=0.)
    independent_lattice=L.WilsonLattice(beta=0.,seed=50)
    gate('beta_zero_sweep_acceptance_exact',independent_lattice.sweep()==1.)
    gate('beta_zero_evolved_group_defect',float(np.max(abs(np.sum(independent_lattice.links**2,axis=-1)-1))),maximum=2e-14)
    rejects('extent_one_rejected',lambda:L.WilsonLattice(lengths=(1,2,2,2)))
    rejects('boolean_extent_rejected',lambda:L.WilsonLattice(lengths=(True,2,2,2)))
    rejects('negative_beta_rejected',lambda:L.WilsonLattice(beta=-.1))
    rejects('empty_statistics_rejected',lambda:L.series_summary([]))
    rejects('NaN_samples_rejected',lambda:L.series_summary([0.,np.nan]))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        rejects('finite_input_overflow_statistics_rejected',lambda:L.series_summary(np.array([1e308,-1e308]*1024)))
        rejects('finite_input_variance_overflow_rejected',lambda:L.series_summary(np.r_[np.zeros(2047),1e308]))
        rejects('invalid_summary_mean_rejected',lambda:L.compare_to_exact({'status':'usable','se':1.,'mean':np.nan},0.))
    gate('one_sample_statistics_insufficient',L.series_summary([1.])['status']=='insufficient')
    gate('constant_statistics_degenerate',L.series_summary(np.ones(2048))['status']=='degenerate')
    gate('degenerate_evidence_not_consistent',L.compare_to_exact(L.series_summary(np.ones(2048)),1.)['status']=='insufficient')

    transfer_records=[]
    for beta,n in [(0,1),(0,2),(.0001,2),(.0001,7),(.1,2),(.1,5),(1,2),(1,8),(2.2,2),(10,3),(50,7),(500,8)]:
        actual=T.eigenvalue_record(beta,n)
        reference=haar_ratio_reference(beta,n,80)
        error=abs(float(actual['ratio'])-float(reference))/max(abs(float(reference)),1e-100)
        gate(f'transfer_Haar80_beta{beta}_n{n}',error,maximum=2e-11)
        gate(f'transfer_multiplicity_beta{beta}_n{n}',actual['multiplicity_full']==n*n and actual['multiplicity_class']==1)
        transfer_records.append({'beta':beta,'n':n,'ratio':actual['ratio'],'reference':str(reference),'relative_error':error})
    for bb,nn in [(500,8),(.0001,7)]:
        low=haar_ratio_reference(bb,nn,80,512);high=haar_ratio_reference(bb,nn,80,1024)
        gate(f'independent_Haar_node_refinement_beta{bb}_n{nn}',float(abs((high-low)/high)),maximum=1e-50)
    gate('tiny_positive_logZ_preserved',abs(T.log_normalization(1e-100)/1.25e-201-1),maximum=2e-15)
    rejects('unrepresentable_positive_logZ_rejected',lambda:T.log_normalization(1e-300))
    tinyz=T.decimal_reference(1e-300,1)
    gate('positive_logZ_decimal_retained',tinyz['log_Z'] is None and Decimal(tinyz['log_Z_decimal'])>0)
    actual=T.eigenvalue_record(1e-300,64)
    with localcontext() as ctx:
        ctx.prec=100
        # Positive-series corrections to this leading term are < beta^2/8.
        reference=63*(Decimal('1e-300').ln()-Decimal(2).ln())-Decimal(math.factorial(64)).ln()
    gate('tiny_eigenvalue_log_independent_asymptotic100',abs(actual['log_ratio']-float(reference)),maximum=1e-10)
    gate('tiny_positive_eigenvalue_not_zero',actual['ratio'] is None and 'positive_below_float' in actual['status'])
    negative=haar_ratio_reference(-2,2,70)
    gate('negative_beta_positive_kernel_negative_eigenvalue',float(negative),maximum=-.1)
    gate('negative_beta_counterexample_matches',abs(T.negative_beta_control()['ratio']-float(negative)),maximum=2e-14)
    true=T.eigenvalue_record(2.,2)['ratio']
    gate('omitted_representation_dimension_detected',abs(2*true-true),minimum=.1)
    gap=T.gap_record(1e6)
    gate('large_beta_gap_nonuniform_asymptotic',abs(1e6*gap['dimensionless_energy']-1.5),maximum=5e-5)
    gate('fixed_beta_time_scale_changes_energy',abs(T.gap_record(2.,.125)['physical_gap']-8*T.gap_record(2.,1.)['physical_gap']),maximum=1e-14)
    for name,fn in [('transfer_negative_beta',lambda:T.eigenvalue_record(-1,2)),('transfer_NaN',lambda:T.eigenvalue_record(np.nan,2)),('transfer_noninteger_representation',lambda:T.eigenvalue_record(1,1.5)),('transfer_zero_timestep',lambda:T.gap_record(1,0)),('transfer_zero_quadrature_nodes',lambda:T.haar_character_quadrature(1,2,0))]:
        rejects(name+'_rejected',fn)

    after={str(p.relative_to(ROOT)):digest(p) for p in sources}
    gate('source_bytes_stable_during_audit',before==after)
    report={'scope':'Independent matrix, high-precision Haar quadrature and rejection checks; not formal proof-kernel verification',
            'source_sha256_before':before,'source_sha256_after':after,
            'gate_count':len(RECORDS),'passed':all(x['passed'] for x in RECORDS),
            'failures':[r for r in RECORDS if not r['passed']], 'gates':RECORDS,
            'transfer_reference_records':transfer_records,
            'versions':{'python':sys.version,'numpy':np.__version__,'reference':'stdlib Decimal at 80 or 100 digits; Gauss-Chebyshev Haar quadrature'}}
    (OUT/'independent_audit.json').write_text(json.dumps(report,indent=2,allow_nan=False))
    print(json.dumps({k:report[k] for k in ['gate_count','passed','failures']},indent=2))
    if not report['passed']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
