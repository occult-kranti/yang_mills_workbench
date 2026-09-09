#!/usr/bin/env python3
"""Independent compact SU(2) identity and scalar-closure stress tests.

Exact Fraction fixtures test printed coefficients; quadrature only diagnoses
finite one-plaquette moments. No continuum existence or mass-gap certificate.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math
import numbers

import numpy as np
from scipy.integrate import quad

HERE = Path(__file__).resolve().parent
SOURCE = "https://arxiv.org/html/2608.05415v1"


def real_parameter(value):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, numbers.Real):
        raise ValueError("kappa must be a finite real number")
    value = float(value)
    if not math.isfinite(value) or abs(value) > 40:
        raise ValueError("diagnostic implementation supports |kappa|<=40")
    return value


def haar_moment(n):
    """E_Haar[x^n], x=Tr(U)/2: exact Catalan moments on [-1,1]."""
    if isinstance(n, bool) or not isinstance(n, int) or n < 0:
        raise ValueError("moment order must be a nonnegative integer")
    if n % 2:
        return F(0)
    k = n // 2
    return F(math.comb(2*k, k), (k+1) * 4**k)


def moment_diagnostics(kappa, max_order=8):
    """Tilted Haar moments with scaled positive weight; errors are estimates."""
    kappa = real_parameter(kappa)
    if isinstance(max_order, bool) or not isinstance(max_order, int) or max_order < 2:
        raise ValueError("max_order must be an integer at least 2")
    # theta coordinates avoid the sqrt endpoint singularity of x quadrature.
    # A common exp(-|kappa|) factor cancels from every normalized moment.
    def integrate(n):
        return quad(lambda theta: math.cos(theta)**n * math.sin(theta)**2
                    * math.exp(kappa*math.cos(theta)-abs(kappa)),
                    0, math.pi, epsabs=2e-13, epsrel=2e-13, limit=180)
    norm, norm_err = integrate(0)
    if not math.isfinite(norm) or norm <= 0:
        raise ArithmeticError("positive normalization lost")
    raw = [integrate(n) for n in range(max_order+1)]
    moments = [value/norm for value, _ in raw]
    if not all(math.isfinite(x) for x in moments):
        raise ArithmeticError("nonfinite moment")
    residuals = []
    for n in range(max_order-1):
        lower = n*moments[n-1] if n else 0.0
        residuals.append(lower-(n+3)*moments[n+1]
                         + kappa*(moments[n]-moments[n+2]))
    variance = moments[2]-moments[1]**2
    # Replacing m2 by m1^2 violates n=0 by exactly kappa*variance.
    collapsed_residual = -3*moments[1]+kappa*(1-moments[1]**2)
    return dict(kappa=kappa, moments=moments, variance=variance,
                hierarchy_residuals=residuals,
                collapsed_residual=collapsed_residual,
                predicted_collapsed_residual=kappa*variance,
                analytic_variance_lower=math.exp(-2*abs(kappa))/4,
                quadrature_error_estimates=[err/norm+abs(v)*norm_err/norm**2
                                             for v, err in raw],
                scope="Floating quadrature diagnostics, not interval certificates")


def printed_coefficient_fixtures():
    """Exact comparisons in the displayed v1 conventions, not author intent.

    One open square, U=diag(exp(i theta),exp(-i theta)), other links I,
    T3=diag(1/2,-1/2), beta=1. A left epsilon shifts theta by epsilon/2.
    Coefficients below multiply cos(theta), or are evaluated at theta=pi/2.
    """
    # Gaussian rational diagonal matrices suffice for these exact fixtures.
    def add(a,b): return (a[0]+b[0],a[1]+b[1])
    def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    def scale(c,a): return (c*a[0],c*a[1])
    def trace(diagonal):
        value=(F(0),F(0))
        for entry in diagonal: value=add(value,entry)
        return value
    def serial(a): return {"real":str(a[0]),"imag":str(a[1])}
    identity=[(F(1),F(0)),(F(1),F(0))]
    generator=[F(1,2),F(-1,2)]
    imag=(F(0),F(1)); minus_imag=(F(0),F(-1))
    quarter_turn=[imag,minus_imag]
    # One unoriented square contributes two ordered orientations in Eq.8.
    tr_identity=trace(identity)[0]
    first_action=-F(1,2)*sum([tr_identity,tr_identity])
    later_action=-F(1,4)*(tr_identity+tr_identity)
    left_link_derivative=[mul(imag,scale(t,u)) for t,u in zip(generator,quarter_turn)]
    direct_derivative=-F(1,2)*trace(left_link_derivative)[0]
    trace_difference=trace([scale(t,add(u,scale(-1,(u[0],-u[1]))))
                            for t,u in zip(generator,quarter_turn)])
    printed_derivative=scale(F(1,16),mul(minus_imag,trace_difference))[0]
    source_derivative=trace([mul(imag,scale(t*t,u)) for t,u in zip(generator,identity)])
    printed_source=(F(1,4)*tr_identity,F(0))
    return dict(
        source=SOURCE,
        equation8=dict(first_action_cos_coefficient=str(first_action),
                       later_action_cos_coefficient=str(later_action),
                       ratio=str(first_action/later_action),
                       verdict="The first directed sum is twice the later unordered real-trace action as printed; the difference depends on the link."),
        equation14=dict(direct_left_derivative_at_half_pi=str(direct_derivative),
                        printed_staple_derivative_at_half_pi=str(printed_derivative),
                        ratio=str(printed_derivative/direct_derivative),
                        verdict="The printed staple prefactor is one quarter of the derivative of the later Eq.8 action for the one-square fixture."),
        equation18=dict(direct_source_derivative_at_identity=serial(source_derivative),
                        printed_source_coefficient_at_identity=serial(printed_source),
                        verdict="The displayed source-side coefficient omits the i from the Lie derivative in Eqs.5 and19."),
        equation29=dict(spacetime_dimension=4, SU3_color_dimension=3**2-1,
                        maximum_gram_rank=4, required_identity_rank=8,
                        verdict="A 4-by-8 color-Lorentz matrix cannot have eta^T g eta=I8: rank is at most4 for any metric and real or complex entries."),
        periodic_check=dict(graph="Two-dimensional periodic box with side at least3; one varied link, all others identity.",
                            staple_multiplicity=2,
                            direct_left_derivative_at_half_pi=str(2*direct_derivative),
                            printed_left_derivative_at_half_pi=str(2*printed_derivative),
                            ratio=str(printed_derivative/direct_derivative)),
        interpretation="These local v1 formula discrepancies do not refute Haar integration by parts, establish intent, or adjudicate an apparatus or the entire research programme.")


def run(output):
    output.mkdir(parents=True, exist_ok=True)
    checks = []
    def check(name, condition):
        if not bool(condition):
            raise AssertionError(name)
        checks.append({"name":name,"passed":True})
    check("Haar normalization", haar_moment(0)==1)
    check("Haar variance", haar_moment(2)==F(1,4))
    check("Haar fourth moment", haar_moment(4)==F(1,8))
    for n in range(24):
        check(f"exact Haar hierarchy n={n}",
              (n*haar_moment(n-1) if n else 0)==(n+3)*haar_moment(n+1))
    for invalid in [True, False, float("nan"), float("inf"), "1", 41, -41]:
        try:
            moment_diagnostics(invalid)
        except ValueError:
            check(f"reject invalid parameter {invalid!r}", True)
        else:
            check(f"reject invalid parameter {invalid!r}", False)
    rows = []
    cases = {}
    for kappa in [-5, -2, -1, 0, 1, 2, 5]:
        result = moment_diagnostics(kappa)
        cases[str(kappa)] = result
        check(f"compact hierarchy kappa={kappa}", max(map(abs,result["hierarchy_residuals"]))<2e-11)
        check(f"nonzero variance kappa={kappa}", result["variance"]>0)
        check(f"variance comparison kappa={kappa}", result["variance"]+2e-12>=result["analytic_variance_lower"])
        check(f"closure residual identity kappa={kappa}", abs(result["collapsed_residual"]-result["predicted_collapsed_residual"])<2e-11)
        if kappa:
            check(f"false closure rejected kappa={kappa}", abs(result["collapsed_residual"])>0.01)
        else:
            check("zero-coupling first identity is nondiscriminating", abs(result["collapsed_residual"])<2e-12)
            check("zero-coupling next identity rejects point closure", F(1)-4*F(0)==1)
        rows.append(dict(kappa=kappa,mean=result["moments"][1],second=result["moments"][2],
                         variance=result["variance"],true_residual=max(map(abs,result["hierarchy_residuals"])),
                         collapsed_residual=result["collapsed_residual"],variance_lower=result["analytic_variance_lower"]))
    for kappa in [1,2,5]:
        p, m=cases[str(kappa)],cases[str(-kappa)]
        check(f"reflection moment parity kappa={kappa}", all(abs(a-(-1)**n*b)<2e-12 for n,(a,b) in enumerate(zip(p["moments"],m["moments"]))))
    fixtures = printed_coefficient_fixtures()
    check("Eq8 action coefficients disagree", F(fixtures["equation8"]["ratio"])==2)
    check("Eq14 staple prefactor disagrees", F(fixtures["equation14"]["ratio"])==F(1,4))
    check("Eq18 source derivative has different phase", fixtures["equation18"]["direct_source_derivative_at_identity"]!=fixtures["equation18"]["printed_source_coefficient_at_identity"])
    check("Eq29 rank obstruction for SU3",fixtures["equation29"]["maximum_gram_rank"]<fixtures["equation29"]["required_identity_rank"])
    with (output/"closure_moments.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    result={"status":"passed","count":len(checks),"checks":checks,"cases":cases,
            "printed_fixtures":fixtures,"source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "scope":"Finite one-plaquette Euclidean measure; neither a Hamiltonian ground state nor a continuum certificate."}
    (output/"results.json").write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"status":"passed","count":len(checks),"output":str(output)}))


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path,default=HERE/"output")
    run(parser.parse_args().output)
