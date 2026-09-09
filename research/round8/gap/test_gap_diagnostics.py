#!/usr/bin/env python3
"""Independent arithmetic references and adversarial input tests.

Test success verifies these finite computations, not a continuum gauge theory.
"""
from __future__ import annotations
import json
import math
from decimal import Decimal, localcontext
from pathlib import Path
import numpy as np
from gap_diagnostics import effective_mass, lattice_frequency, log_correlator, manifest


def decimal_effective(t, delta, masses, amplitudes):
    """Independent high-precision direct exponential/ratio evaluation."""
    with localcontext() as ctx:
        ctx.prec = 100
        t, delta = Decimal(str(t)), Decimal(str(delta))
        masses, amplitudes = list(map(lambda x: Decimal(str(x)), masses)), list(map(lambda x: Decimal(str(x)), amplitudes))
        c0 = sum(a * (-m*t).exp() for m, a in zip(masses, amplitudes))
        c1 = sum(a * (-m*(t+delta)).exp() for m, a in zip(masses, amplitudes))
        return float((c0/c1).ln()/delta)


def run():
    records = []
    def check(name, condition, **evidence):
        records.append(dict(name=name, status="pass" if bool(condition) else "fail", **evidence))
    def rejects(name, thunk, expected=(ValueError,)):
        try:
            thunk()
        except expected as exc:
            check(name, True, exception=type(exc).__name__)
        except Exception as exc:
            check(name, False, exception=type(exc).__name__)
        else:
            check(name, False, exception=None)

    # A separate matrix implementation checks the dispersion without using sin.
    n, a, mass = 16, .25, .7
    lap = (2*np.eye(n)-np.roll(np.eye(n), 1, axis=1)-np.roll(np.eye(n), -1, axis=1))/a**2
    frequencies = np.sqrt(np.linalg.eigvalsh(lap+mass**2*np.eye(n)))
    target = lattice_frequency(mass,a,n,1)
    check("dispersion_vs_independent_circulant_eigenvalues", abs(frequencies[1]-target)<1e-12,
          error=float(abs(frequencies[1]-target)), reference=float(frequencies[1]))
    check("massless_zero_mode_is_zero", lattice_frequency(0,.25,16,0)==0)
    check("massive_zero_mode_equals_mass", lattice_frequency(.7,.25,16,0)==.7)
    check("opposite_modes_equal", lattice_frequency(.7,.25,16,1)==lattice_frequency(.7,.25,16,15))
    check("nyquist_frequency", abs(lattice_frequency(0,.25,16,8)-8)<1e-14)
    expected=2*math.pi/10
    errors=[expected-lattice_frequency(0,10/n,n) for n in [32,64,128,256]]
    ratios=[errors[i]/errors[i+1] for i in range(3)]
    check("fixed_volume_second_order_refinement", all(3.99<r<4.01 for r in ratios), error_ratios=ratios)
    f1=lattice_frequency(0,.125,4096); f2=lattice_frequency(0,.125,8192)
    check("massless_volume_doubling_halves_mode_scale", abs(f1/f2-2)<1e-6, ratio=f1/f2)
    g=lattice_frequency(.7,.125,8192)
    check("massive_volume_limit_remains_above_mass", .7<g<.7001, omega=g)
    for name, args in [
        ("negative_mass",(-1,.2,8)),("zero_spacing",(0,0,8)),
        ("negative_spacing",(0,-.1,8)),("nan_spacing",(0,float('nan'),8)),
        ("infinite_mass",(float('inf'),.2,8)),("one_site",(0,.2,1)),
        ("noninteger_sites",(0,.2,8.5)),("boolean_sites",(0,.2,True)),
        ("negative_mode",(0,.2,8,-1)),("mode_out_of_range",(0,.2,8,8)),
        ("nan_mode",(0,.2,8,float('nan'))),("noninteger_mode",(0,.2,8,.5))]:
        rejects("reject_lattice_"+name,lambda args=args:lattice_frequency(*args))
    rejects("lattice_overflow_reports_error",lambda:lattice_frequency(0,5e-324,8),expected=(ArithmeticError,))

    references=[]
    for t,delta,masses,amps in [
        (0,.5,[.1,1],[1e-12,1]),(30,.5,[.1,1],[1e-12,1]),
        (80,.5,[.1,1],[1e-12,1]),(12,1e-12,[.1,1],[1e-12,1]),
        (10000,.5,[.1,1],[1e-12,1]),(0,1,[.1,2],[5e-324,1e308]),
        (2,.3,[0,.3,1.7],[.2,3,4]),(7,.5,[1,1],[2,3])]:
        actual=effective_mass(t,delta,masses,amps)
        reference=decimal_effective(t,delta,masses,amps)
        references.append(dict(time=t,interval=delta,actual=actual,reference=reference,error=abs(actual-reference)))
    check("matched_decimal_references_100_digits",all(r['error']<3e-13 for r in references),cases=references)
    for mass in [0,.1,1.0,1e100]:
        actual=effective_mass(1e100,.5,[mass],[1e-200])
        check("single_exponential_exact_"+str(mass),actual==mass,actual=actual)
    check("equal_masses_equal_single_support",effective_mass(5,.5,[.7,.7],[2,3])==.7)
    check("zero_amplitudes_are_excluded_from_support",effective_mass(5,.5,[0,.7],[0,1])==.7)
    ordinary=effective_mass(30,.5,[.1,1],[1e-12,1])
    rescaled=effective_mass(30,.5,[.1,1],[1e-112,1e-100])
    check("common_amplitude_scale_invariance",abs(ordinary-rescaled)<1e-14,error=abs(ordinary-rescaled))
    tiny=effective_mass(0,5e-324,[0,.1],[1,1])
    check("subnormal_delta_uses_stable_divided_difference",abs(tiny-.05)<1e-15,actual=tiny,expected_limit=.05)
    check("naive_correlator_underflow_occurs",math.exp(log_correlator(10000,[.1,1],[1e-12,1]))==0)
    check("effective_mass_survives_correlator_underflow",effective_mass(10000,.5,[.1,1],[1e-12,1])==.1)
    check("enormous_time_effective_mass_finite",effective_mass(1e308,1,[2,3],[1,1])==2)
    rejects("log_correlator_overflow_reported",lambda:log_correlator(1e308,[2,3],[1,1]),expected=(ArithmeticError,))

    ts=np.linspace(0,80,801)
    eff=[effective_mass(float(t),.5,[.1,1],[1e-12,1]) for t in ts]
    check("hidden_state_lower_spectral_bound",min(eff)>=.1-2e-15,minimum=min(eff))
    check("hidden_state_upper_spectral_bound",max(eff)<=1+2e-15,maximum=max(eff))
    check("hidden_state_effective_mass_monotone",max(np.diff(eff))<=2e-14,maximum_increase=float(max(np.diff(eff))))
    check("early_plateau_exceeds_true_supported_mass_nearly_tenfold",eff[0]>.99999999999 and eff[0]/.1>9.99,early=eff[0],true_supported_mass=.1)
    check("late_plateau_reaches_hidden_light_state",abs(eff[-1]-.1)<1e-14,late=eff[-1])
    # Independent direct finite-exponential log-convexity determinant, Decimal.
    with localcontext() as ctx:
        ctx.prec=100
        def c(t):
            t=Decimal(str(t))
            return Decimal('1e-12')*(-Decimal('.1')*t).exp()+(-t).exp()
        determinants=[c(t)*c(t+1)-c(t+.5)**2 for t in [0,10,30,60]]
    check("independent_decimal_log_convexity",all(v>0 for v in determinants),determinants=[str(v) for v in determinants])

    invalid=[
        ("nan_time",(float('nan'),.5,[1],[1])),("negative_time",(-1,.5,[1],[1])),
        ("zero_interval",(0,0,[1],[1])),("negative_interval",(0,-1,[1],[1])),
        ("infinite_interval",(0,float('inf'),[1],[1])),("nan_mass",(0,1,[float('nan')],[1])),
        ("negative_mass",(0,1,[-1],[1])),("negative_amplitude",(0,1,[1],[-1])),
        ("nan_amplitude",(0,1,[1],[float('nan')])),("infinite_amplitude",(0,1,[1],[float('inf')])),
        ("all_zero_amplitudes",(0,1,[1,2],[0,0])),("empty_spectrum",(0,1,[],[])),
        ("mismatched_lengths",(0,1,[1,2],[1])),("boolean_time",(True,1,[1],[1]))]
    for name,args in invalid:
        rejects("reject_correlator_"+name,lambda args=args:effective_mass(*args))

    # Deterministic randomized ensembles compare an independent direct formula,
    # with positive random energies; separate fixtures test zero-energy support.
    rng=np.random.default_rng(1729)
    largest_reference_error=0.; largest_monotonic_error=0.; bound_ok=True
    for _ in range(80):
        masses=sorted(rng.uniform(0,3,5).tolist()); amps=np.exp(rng.uniform(-12,2,5)).tolist()
        t=float(rng.uniform(0,10)); delta=float(rng.uniform(.02,1))
        actual=effective_mass(t,delta,masses,amps)
        direct=math.log(math.fsum(a*math.exp(-m*t) for m,a in zip(masses,amps))/math.fsum(a*math.exp(-m*(t+delta)) for m,a in zip(masses,amps)))/delta
        largest_reference_error=max(largest_reference_error,abs(actual-direct))
        largest_monotonic_error=max(largest_monotonic_error,effective_mass(t+.1,delta,masses,amps)-actual)
        bound_ok=bound_ok and masses[0]-1e-13<=actual<=masses[-1]+1e-13
    check("random_80_independent_direct_references",largest_reference_error<2e-13,maximum_error=largest_reference_error)
    check("random_80_spectral_interval",bound_ok)
    check("random_80_monotonicity",largest_monotonic_error<2e-13,maximum_increase=largest_monotonic_error)
    result={"status":"pass" if all(r['status']=='pass' for r in records) else "fail",
            "passed":sum(r['status']=='pass' for r in records),"failed":sum(r['status']=='fail' for r in records),
            "scope":"Finite toy-model arithmetic and explicit input guards; not a Yang--Mills theorem.",
            "records":records}
    output=Path(__file__).resolve().parent
    (output/'test_results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    manifest(output)
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
    for r in records:
        if r['status']=='fail': print(json.dumps(r))
    return result['status']=='pass'

if __name__=='__main__':
    raise SystemExit(0 if run() else 1)
