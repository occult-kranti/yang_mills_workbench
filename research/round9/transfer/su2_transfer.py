"""Exact SU(2) central-convolution benchmark; this is not 4D Yang--Mills.

K(U,V)=exp(beta ReTr(U V†)/2)/Z, normalized Haar. n=2j+1.
Numerical domain: 0 <= beta <= 1e6, integer 1 <= n <= 4096.
Tiny positive eigenvalues are retained as logarithms; a missing float is None.
"""
from decimal import Decimal, localcontext
from math import isfinite, log, log1p, log10, factorial
from numbers import Integral, Real
import numpy as np
from scipy.special import ive


class NumericalDomainError(ValueError):
    """Input or numerical accuracy is outside the declared implementation scope."""


def _validate(beta, n):
    if isinstance(beta, (bool, np.bool_)) or not isinstance(beta, Real):
        raise NumericalDomainError("beta must be a real number, not a boolean")
    beta = float(beta)
    if not isfinite(beta) or beta < 0 or beta > 1e6:
        raise NumericalDomainError("require finite 0 <= beta <= 1e6")
    if isinstance(n, (bool, np.bool_)) or not isinstance(n, Integral) or not 1 <= n <= 4096:
        raise NumericalDomainError("n=2j+1 must be an integer in [1,4096]")
    return beta, int(n)


def _decimal_series(n, x, digits):
    """Positive power series for I_n(x), in caller's Decimal context.

The estimated omitted positive tail uses monotonically decreasing term ratios.
This controls truncation, not interval-enclosed Decimal rounding.
"""
    term = (x / 2) ** n / Decimal(factorial(n))
    total = term
    xx = x*x/4
    tol = Decimal(10) ** (-digits)
    for k in range(1, 20000):
        term *= xx / (Decimal(k) * (n+k))
        total += term
        q = xx / (Decimal(k+1) * (n+k+1))
        if q < 1 and term*q/(1-q) <= tol*total:
            return total
    raise NumericalDomainError("Decimal series did not satisfy its tail target")


def decimal_reference(beta, n, digits=80):
    """Independent positive series, <=1000 beta; decimal strings preserve range."""
    beta, n = _validate(beta, n)
    if beta == 0 or beta > 1000:
        raise NumericalDomainError("Decimal reference requires 0 < beta <= 1000")
    if isinstance(digits, bool) or not isinstance(digits, Integral) or not 30 <= digits <= 300:
        raise NumericalDomainError("reference precision must be 30..300 decimal digits")
    with localcontext() as ctx:
        # Z=1+O(beta²), so tiny beta needs extra working precision even though
        # I_n/I_1 itself has no near-unit cancellation for n>1.
        ctx.prec = int(digits)+20+max(0, int(-2*log10(beta)))
        # Required for high-order eigenvalues at tiny beta.
        ctx.Emin = -999999999
        ctx.Emax = 999999999
        x = Decimal(str(beta))
        den = _decimal_series(1, x, digits+5)
        num = _decimal_series(n, x, digits+5)
        ratio = num/den
        log_z = (2*den/x).ln()
        log_z_float = float(log_z)
        log_z_underflow = log_z > 0 and log_z_float == 0
        return {"ratio_decimal": str(ratio), "log_ratio": float(ratio.ln()),
                "log_Z": None if log_z_underflow else log_z_float,
                "log_Z_decimal": str(log_z),
                "log_Z_status": "positive_below_float_range" if log_z_underflow else "computed",
                "precision_digits": int(digits),
                "working_precision_digits": ctx.prec,
                "method": "positive Decimal power series; estimated relative tail target; not interval arithmetic"}


def eigenvalue_record(beta, n):
    beta, n = _validate(beta, n)
    common = {"beta": beta, "n": n, "j": (n-1)/2,
              "multiplicity_full": n*n, "multiplicity_class": 1}
    if n == 1:
        return dict(common, ratio=1.0, log_ratio=0.0, dimensionless_energy=0.0,
                    status="exact_constant_mode", method="Haar normalization")
    if beta == 0:
        return dict(common, ratio=0.0, log_ratio=None, dimensionless_energy=None,
                    status="exact_projection_zero_eigenvalue", method="analytic beta=0 limit")
    den, num = float(ive(1, beta)), float(ive(n, beta))
    # Scaled Bessel still underflows at large order or very small argument.
    if isfinite(den) and isfinite(num) and den >= np.finfo(float).tiny and num >= np.finfo(float).tiny:
        ratio = num/den
        if 0 < ratio < 1:
            log_ratio = log1p(ratio-1) if ratio > .5 else log(ratio)
            return dict(common, ratio=ratio, log_ratio=log_ratio,
                        dimensionless_energy=-log_ratio, status="computed",
                        method="SciPy exponentially scaled ive ratio")
    if beta > 1000:
        raise NumericalDomainError("scaled Bessel underflow or invalid ratio; Decimal fallback only supports beta <=1000")
    ref = decimal_reference(beta, n)
    ratio = float(Decimal(ref["ratio_decimal"]))
    if ratio == 0:
        ratio, status = None, "positive_below_float_range_log_retained"
    elif not 0 < ratio < 1:
        raise NumericalDomainError("fallback could not represent a strictly interior eigenvalue")
    else:
        status = "computed_with_decimal_fallback"
    return dict(common, ratio=ratio, log_ratio=ref["log_ratio"],
                dimensionless_energy=-ref["log_ratio"], status=status,
                method=ref["method"], ratio_decimal=ref["ratio_decimal"])


def log_normalization(beta):
    beta, _ = _validate(beta, 1)
    if beta == 0:
        return 0.0
    if beta <= .01:
        reference=decimal_reference(beta, 1)
        if reference['log_Z'] is None:
            raise NumericalDomainError("positive log Z is below float range; decimal_reference retains its Decimal value")
        return reference["log_Z"]
    den = float(ive(1, beta))
    if not isfinite(den) or den <= 0:
        raise NumericalDomainError("invalid scaled normalization")
    return beta + log(2*den/beta)


def gap_record(beta, time_step=1.):
    beta, _ = _validate(beta, 2)
    if isinstance(time_step, (bool, np.bool_)) or not isinstance(time_step, Real):
        raise NumericalDomainError("time_step must be positive finite")
    time_step = float(time_step)
    if not isfinite(time_step) or time_step <= 0:
        raise NumericalDomainError("time_step must be positive finite")
    result = eigenvalue_record(beta, 2)
    result["time_step"] = time_step
    if beta == 0:
        result.update(markov_gap=1.0, physical_gap=None,
                      physical_gap_status="no_finite_excited_generator_energy_at_exact_projection",
                      log_doeblin_lower_bound=0.0)
        return result
    result["markov_gap"] = -np.expm1(result["log_ratio"]).item()
    physical = result["dimensionless_energy"]/time_step
    if not isfinite(physical):
        raise NumericalDomainError("physical gap overflows for this time_step")
    result.update(physical_gap=physical, physical_gap_status="computed",
                  log_doeblin_lower_bound=-beta-log_normalization(beta))
    return result


def haar_character_quadrature(beta, n, nodes=256):
    """Independent double-precision quadrature, includes negative-beta control.

Integrates radial Haar times the character directly without Bessel functions.
The implementation does not certify tiny eigenvalues whose sign is unresolved.
Use refinement and the Decimal series comparison separately.
"""
    if isinstance(beta, (bool, np.bool_)) or not isinstance(beta, Real) or not isfinite(float(beta)):
        raise NumericalDomainError("quadrature beta must be a finite real")
    beta = float(beta)
    if abs(beta)>1000:
        raise NumericalDomainError("Haar quadrature scope is |beta|<=1000")
    _, n = _validate(abs(beta), n)
    if isinstance(nodes, bool) or not isinstance(nodes, Integral) or not 16 <= nodes <= 2048:
        raise NumericalDomainError("quadrature nodes must be an integer in [16,2048]")
    z, w = np.polynomial.legendre.leggauss(int(nodes))
    theta = (z+1)*np.pi/2
    weights = w*np.pi/2
    # e^{-|beta|} removes overflow. sin²(theta)*chi is sin(theta)*sin(n theta),
    # avoiding 0/0 at group endpoints and the wrong flat-angle measure.
    kernel = np.exp(beta*np.cos(theta)-abs(beta))
    denominator = (2/np.pi)*np.dot(weights, kernel*np.sin(theta)**2)
    numerator = (2/np.pi)*np.dot(weights, kernel*np.sin(theta)*np.sin(n*theta))/n
    if not isfinite(denominator) or denominator <= 0 or not isfinite(numerator):
        raise NumericalDomainError("incomplete or nonfinite quadrature")
    return {"ratio": float(numerator/denominator),
            "log_Z": float(abs(beta)+log(denominator)), "nodes": int(nodes)}


def negative_beta_control(beta=-2., n=2):
    """Counterexample only, deliberately excluded from positive-transfer API."""
    if isinstance(beta, (bool, np.bool_)) or not isinstance(beta, Real) or not isfinite(float(beta)) or beta >= 0:
        raise NumericalDomainError("counterexample requires a finite negative beta")
    record = eigenvalue_record(-float(beta), n)
    if record["ratio"] is None:
        raise NumericalDomainError("counterexample eigenvalue outside floating range")
    return {"beta": float(beta), "n": n,
            "ratio": (-1 if n % 2 == 0 else 1)*record["ratio"],
            "kernel_strictly_pointwise_positive": True,
            "is_positive_operator": False,
            "scope": "negative-beta counterexample; outside main beta>0 domain"}
