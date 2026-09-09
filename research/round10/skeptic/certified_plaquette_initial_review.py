"""Exact rational enclosures for a single SU(2) plaquette Hamiltonian.

Physical space: class functions of one loop holonomy, normalized Haar measure.
Basis chi_{n/2}; N counts retained terms n=0,...,N-1. This is a finite
spatial graph with an infinite representation tower, not continuum 4D YM.
"""
from __future__ import annotations

from fractions import Fraction as F
import math


class ContractError(ValueError):
    pass


def rational(value, name="value"):
    if isinstance(value, bool):
        raise ContractError(f"{name} cannot be boolean")
    if isinstance(value, float) and not math.isfinite(value):
        raise ContractError(f"{name} must be finite")
    try:
        # Floats are interpreted as their displayed decimal value; artifacts
        # use rational strings, so their certified physical input is unambiguous.
        result = F(str(value)) if isinstance(value, float) else F(value)
    except (ValueError, TypeError, ZeroDivisionError, OverflowError) as exc:
        raise ContractError(f"{name} must be a finite rational") from exc
    return result


def contract(alpha, coupling, N):
    a, lam = rational(alpha, "alpha"), rational(coupling, "coupling")
    if a <= 0 or lam < 0:
        raise ContractError("require alpha>0 and coupling>=0")
    if isinstance(N, bool) or not isinstance(N, int) or N < 2:
        raise ContractError("N must be an integer >=2 to enclose a gap")
    return a, lam, N


def sturm_count(diagonal, offdiagonal, x):
    """Number of eigenvalues strictly below rational x.

    For the irreducible Jacobi case, use sign changes of leading principal
    determinants with zeros omitted. A terminal zero is an eigenvalue at x
    and is not counted. Zero coupling is handled as a diagonal operator.
    """
    d = tuple(rational(v) for v in diagonal)
    b, x = rational(offdiagonal), rational(x)
    if not d:
        raise ContractError("empty matrix")
    if b == 0:
        return sum(v < x for v in d)
    old, current = F(1), d[0] - x
    last_sign, variations = 1, 0
    if current:
        sign = 1 if current > 0 else -1
        variations += sign != last_sign
        last_sign = sign
    for v in d[1:]:
        nxt = (v - x) * current - b * b * old
        old, current = current, nxt
        if current:
            sign = 1 if current > 0 else -1
            variations += sign != last_sign
            last_sign = sign
    return int(variations)


def eigen_interval(diagonal, offdiagonal, k, bits=40):
    d = tuple(rational(v) for v in diagonal)
    b = rational(offdiagonal)
    if isinstance(k, bool) or not isinstance(k, int) or not 0 <= k < len(d):
        raise ContractError("eigenvalue index outside nonempty matrix")
    if isinstance(bits, bool) or not isinstance(bits, int) or not 1 <= bits <= 128:
        raise ContractError("bits must be an integer in [1,128]")
    radii = [abs(b) * ((i > 0) + (i + 1 < len(d))) for i in range(len(d))]
    lo = min(v-r for v,r in zip(d,radii))-1
    hi = max(v+r for v,r in zip(d,radii))+1
    tolerance = F(1, 1 << bits)
    while hi-lo > tolerance:
        mid = (lo+hi)/2
        if sturm_count(d,b,mid) <= k:
            lo = mid
        else:
            hi = mid
    if sturm_count(d,b,lo) > k or sturm_count(d,b,hi) <= k:
        raise ArithmeticError("Sturm enclosure failed its own endpoint gate")
    return lo, hi


def pair_json(interval):
    return {"lower": str(interval[0]), "upper": str(interval[1])}


def certify(alpha="1", coupling="1", N=16, bits=40):
    a, lam, N = contract(alpha,coupling,N)
    A = tuple(a*n*(n+2)+lam for n in range(N))
    off = -lam/2
    a_intervals = [eigen_interval(A,off,k,bits) for k in (0,1)]
    tau = a*N*(N+2)
    U = a_intervals[1][1] + a
    if U >= tau:
        raise ContractError("tail threshold insufficient; increase N")
    delta = (lam/2)**2/(tau-U)
    B = A[:-1] + (A[-1]-delta,)
    b_intervals = [eigen_interval(B,off,k,bits) for k in (0,1)]
    if b_intervals[1][1] >= U:
        raise ArithmeticError("B first excited eigenvalue not certified below U")
    energy = [(b_intervals[k][0],a_intervals[k][1]) for k in (0,1)]
    gap = (energy[1][0]-energy[0][1],energy[1][1]-energy[0][0])
    if any(lo>hi for lo,hi in energy) or gap[0]>gap[1]:
        raise ArithmeticError("inverted interval")
    return {
        "schema":"su2-single-plaquette-rational-v1",
        "scope":"single spatial plaquette; infinite SU(2) character tower",
        "alpha":str(a),"coupling":str(lam),"N":N,"bits":bits,
        "tail":{"tau":str(tau),"U":str(U),"delta":str(delta)},
        "A_eigen_intervals":[pair_json(z) for z in a_intervals],
        "B_eigen_intervals":[pair_json(z) for z in b_intervals],
        "energy_intervals":[pair_json(z) for z in energy],
        "gap_interval":pair_json(gap),
        "positive_gap_certified":gap[0]>0,
        "status":"certified-rational-enclosure",
    }


def verify_certificate(c):
    """Replay rational endpoints and every tail/minmax data dependency.

    This checks arithmetic certificates conditional on the proved operator
    reduction and tail theorem; it is not a general-purpose formal proof kernel.
    """
    if not isinstance(c,dict) or c.get("schema")!="su2-single-plaquette-rational-v1":
        raise ContractError("unknown certificate schema")
    a,lam,N=contract(c["alpha"],c["coupling"],c["N"])
    tau,U,delta=(rational(c["tail"][key]) for key in ("tau","U","delta"))
    if tau != a*N*(N+2) or not U<tau or delta != (lam/2)**2/(tau-U):
        raise ContractError("invalid tail certificate")
    A=tuple(a*n*(n+2)+lam for n in range(N)); B=A[:-1]+(A[-1]-delta,)
    parsed=[]
    for label,d in (("A",A),("B",B)):
        pairs=c[f"{label}_eigen_intervals"]
        if len(pairs)!=2:
            raise ContractError("both eigenvalue certificates are required")
        row=[]
        for k,pair in enumerate(pairs):
            lo,hi=rational(pair["lower"]),rational(pair["upper"])
            if not lo<hi or sturm_count(d,-lam/2,lo)>k or sturm_count(d,-lam/2,hi)<=k:
                raise ContractError("invalid Sturm endpoint certificate")
            row.append((lo,hi))
        parsed.append(row)
    AI,BI=parsed
    if not AI[1][1]<U or not BI[1][1]<U:
        raise ContractError("tail comparison levels not below U")
    energies=[(BI[k][0],AI[k][1]) for k in (0,1)]
    if c["energy_intervals"]!=[pair_json(z) for z in energies]:
        raise ContractError("energy endpoints were altered")
    gap=(energies[1][0]-energies[0][1],energies[1][1]-energies[0][0])
    if c["gap_interval"]!=pair_json(gap) or c["positive_gap_certified"]!=(gap[0]>0):
        raise ContractError("gap subtraction or status was altered")
    if c.get("status")!="certified-rational-enclosure":
        raise ContractError("invalid semantic status")
    return True


def float_matrix(alpha,coupling,N):
    import numpy as np
    a,lam,N=contract(alpha,coupling,N)
    diag=np.array([float(a*n*(n+2)+lam) for n in range(N)])
    off=np.full(N-1,-float(lam)/2)
    return diag,off
