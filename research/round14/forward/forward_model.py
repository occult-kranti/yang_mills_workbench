"""Finite SU(2) two-loop exponential measure: floating diagnostic solvers.

Declared action exponent: k1*x + k2*y + eta*z, z = Tr(U V)/2.
No Hamiltonian, reflection-positivity, continuum or interval claim is made.
"""
from __future__ import annotations

import math
from numbers import Real, Integral

import numpy as np
from scipy.special import ive, roots_jacobi, roots_legendre

PARAMETER_LIMIT = 100.0
MOMENT_NAMES = ("x", "y", "z", "xx", "yy", "zz", "xy", "xz", "yz")


def _real(value, name, bound=PARAMETER_LIMIT):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a finite real number, not a Boolean")
    try:
        value = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{name} cannot be represented as a finite float") from exc
    if not math.isfinite(value) or abs(value) > bound:
        raise ValueError(f"{name} must be finite and have absolute value <= {bound}")
    return value


def _nodes(value, maximum):
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral):
        raise ValueError("nodes must be an integer, not a Boolean")
    value = int(value)
    if not 4 <= value <= maximum:
        raise ValueError(f"nodes must be between 4 and {maximum}")
    return value


def radial_coefficients(h):
    """Return log Z0(h), t=I2/(h I1), r=I3/(h² I1), including h=0.

    r=(1-4t)/h² mathematically; the I3 ratio avoids that cancellation.
    Small h uses positive Bessel series, and all larger Bessels are scaled.
    Inputs here are scalar and 0 <= h <= 200.
    """
    h = _real(h, "h", 2 * PARAMETER_LIMIT)
    if h < 0:
        raise ValueError("h must be nonnegative")
    if h < 0.5:
        a = h * h / 4.0
        # S_n(a) = sum a^j/(j! (j+n)!). Starting terms are exact.
        sums = []
        for nu in (1, 2, 3):
            term = 1.0 / math.factorial(nu)
            terms = [term]
            for j in range(1, 15):
                term *= a / (j * (j + nu))
                terms.append(term)
            sums.append(math.fsum(terms))
        term = 1.0
        tail = []
        for j in range(1, 15):
            term *= a / (j * (j + 1))
            tail.append(term)
        log_z = math.log1p(math.fsum(tail))
        t = 0.5 * sums[1] / sums[0]
        r = 0.25 * sums[2] / sums[0]
    else:
        i1, i2, i3 = (float(ive(j, h)) for j in (1, 2, 3))
        if min(i1, i2, i3) <= 0:
            raise ArithmeticError("scaled Bessel evaluation failed positivity")
        log_z = h + math.log(2.0 * i1 / h)
        t = i2 / (h * i1)
        r = i3 / (h * h * i1)
    result = (log_z, t, r)
    if not all(math.isfinite(v) for v in result):
        raise ArithmeticError("nonfinite radial coefficients")
    return result


def conditional(x, k2, eta):
    """Conditional y,z first/second moments at fixed x, including x=+-1.

    x identifies an SU(2) conjugacy class. No relative angle is divided by
    sqrt(1-x²). A and B are formed around the nearest central endpoint.
    """
    x = _real(x, "x", 1.0)
    k2, eta = _real(k2, "k2"), _real(eta, "eta")
    if x >= 0:
        delta = x - 1.0
        a = math.fsum((k2, eta, eta * delta))
        b = math.fsum((k2, eta, k2 * delta))
    else:
        delta = x + 1.0
        a = math.fsum((k2, -eta, eta * delta))
        b = math.fsum((-k2, eta, k2 * delta))
    sine = math.sqrt((1.0 - x) * (1.0 + x))
    h = math.hypot(a, eta * sine)
    # Roundoff in hypot can exceed the mathematically exact endpoint cap.
    if h > 2 * PARAMETER_LIMIT:
        raise ArithmeticError("conditional field exceeds the declared domain")
    log_z, t, r = radial_coefficients(h)
    out = {
        "h": h, "log_z": log_z, "y": t * a, "z": t * b,
        "yy": t + r * a * a, "zz": t + r * b * b,
        "yz": t * x + r * a * b,
    }
    if not all(math.isfinite(v) for v in out.values()):
        raise ArithmeticError("nonfinite conditional moment")
    return out


def _finish(log_z, moments, method, nodes):
    values = np.asarray(moments, dtype=float)
    if values.shape != (len(MOMENT_NAMES),) or not np.all(np.isfinite(values)):
        raise ArithmeticError("missing or nonfinite moment output")
    if not math.isfinite(log_z):
        raise ArithmeticError("nonfinite normalization")
    out = dict(zip(MOMENT_NAMES, map(float, values)))
    mean = values[:3]
    second = np.array([[out["xx"], out["xy"], out["xz"]],
                       [out["xy"], out["yy"], out["yz"]],
                       [out["xz"], out["yz"], out["zz"]]])
    covariance = second - np.outer(mean, mean)
    if not np.all(np.isfinite(covariance)):
        raise ArithmeticError("nonfinite derived covariance")
    out.update(log_z=float(log_z), covariance=covariance.tolist(),
               cov_xy=float(covariance[0, 1]),
               method=method, nodes=nodes,
               status="floating numerical diagnostic; not an interval certificate")
    return out


def marginal_moments(k1, k2, eta, nodes=64):
    """One-dimensional Gauss-Jacobi quadrature after exact integration of V."""
    k1, k2, eta = (_real(v, n) for v, n in zip((k1, k2, eta), ("k1", "k2", "eta")))
    nodes = _nodes(nodes, 512)
    x, w = roots_jacobi(nodes, 0.5, 0.5)
    w = w * (2.0 / math.pi)
    cond = [conditional(float(t), k2, eta) for t in x]
    logs = np.array([k1 * float(t) + c["log_z"] for t, c in zip(x, cond)])
    shift = float(np.max(logs))
    weights = w * np.exp(logs - shift)
    norm = math.fsum(map(float, weights))
    if not math.isfinite(norm) or norm <= 0:
        raise ArithmeticError("quadrature normalization is not finite positive")
    weights /= norm
    rows = np.array([[t, c["y"], c["z"], t*t, c["yy"], c["zz"],
                      t*c["y"], t*c["z"], c["yz"]] for t, c in zip(x, cond)])
    moments = [math.fsum(float(v * wgt) for v, wgt in zip(rows[:, j], weights))
               for j in range(len(MOMENT_NAMES))]
    return _finish(shift + math.log(norm), moments, "integrated-V / 1D Gauss-Jacobi", nodes)


def direct_moments(k1, k2, eta, nodes=32):
    """Independent 3D angular cubature, with no Bessel or conditional formula.

    Haar coordinates: x=cos(theta), y=cos(phi), relative dot-product c in
    [-1,1]; z=cos(theta)cos(phi)-sin(theta)sin(phi)c. theta and phi use
    their explicit sine-squared weights. All three axes use Legendre nodes.
    """
    k1, k2, eta = (_real(v, n) for v, n in zip((k1, k2, eta), ("k1", "k2", "eta")))
    nodes = _nodes(nodes, 128)
    q, v = roots_legendre(nodes)
    theta = (q + 1.0) * (math.pi / 2.0)
    sine, cosine = np.sin(theta), np.cos(theta)
    angle_weights = v * sine * sine
    c, cweights = q[None, :], v[None, :] / 2.0
    y = cosine[:, None]
    sy = sine[:, None]
    weights_2d = angle_weights[:, None] * cweights
    shift = abs(k1) + abs(k2) + abs(eta)
    accum = [[] for _ in range(10)]
    for x, sx, wx in zip(cosine, sine, angle_weights):
        z = x * y - sx * sy * c
        weights = wx * weights_2d * np.exp(k1*x + k2*y + eta*z - shift)
        monomials = (1.0, x, y, z, x*x, y*y, z*z, x*y, x*z, y*z)
        for j, f in enumerate(monomials):
            accum[j].append(float(np.sum(weights * f)))
    totals = np.array([math.fsum(a) for a in accum])
    norm = float(totals[0])
    if not math.isfinite(norm) or norm <= 0:
        raise ArithmeticError("direct cubature normalization is not finite positive")
    return _finish(shift + math.log(norm), totals[1:] / norm,
                   "direct 3D angular Legendre cubature", nodes)


def single_loop(kappa):
    """One-loop helper for |kappa|<=200, including derived conditional fields."""
    kappa = _real(kappa, "kappa", 2 * PARAMETER_LIMIT)
    log_z, t, r = radial_coefficients(abs(kappa))
    mean = kappa * t
    second = t + r * kappa * kappa
    variance = second - mean * mean
    return {"log_z": log_z, "mean": mean, "second": second, "variance": variance}


def special_family(eta):
    """The exact k1=k2=0 identity, evaluated with floating Bessel ratios."""
    eta = _real(eta, "eta")
    one = single_loop(eta)
    return {"x": 0.0, "y": 0.0, "z": one["mean"],
            "xx": 0.25, "yy": 0.25, "zz": one["second"],
            "xy": one["mean"] / 4.0, "xz": 0.0, "yz": 0.0,
            "cov_xy": one["mean"] / 4.0, "log_z": one["log_z"]}
