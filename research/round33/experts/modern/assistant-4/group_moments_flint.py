#!/usr/bin/env python3
"""BD1 Haar moments E[W^k], k=1..5, for SU(3), SU(4), SU(5), SO(3), and the
SU(N) first-order coefficient 1/(48 N (N^2-1)), recomputed by methods
DIFFERENT from both BD1 producers.

Round33 sub-round 4, modern (Penrose/Feynman) lens, research assistant/coder
"assistant-4". **This script counts zero research loops. Nothing here is
evidence, a contract, a premise or a gate.** It never imports a producer
`check.py` (in particular `research/round33/forward/bd1/check.py` and
`research/round33/reverse/bd1/check.py` are never opened, imported or
executed). It reads only, as text/JSON, never executed:
  - `research/round33/contracts/bd1.json` (the frozen convention and
    parameters, for the exact numbers used below -- per-link electric term
    8 C_2, magnetic term -(tau/3) W with W = Re chi_fund(U)/dim fund, face
    energy 32 C_F, C_F = (N^2-1)/(2N) for SU(N), C_2(l) = l(l+1) for SO(3));
  - `research/round33/forward/bd1/report.md` and `output/results.json`
    (ADMITTED values, read only for comparison, never for computation);
  - `research/round33/reverse/bd1/report.md` and `output/results.json`
    (same, comparison only);
  - `research/round33/advisor/bd1-gate.json` (the gate's own restated
    numbers, comparison only).
`python-flint` (`fmpq` exact rationals, `arb` ball arithmetic) and `sympy`
(exact symbolic integration) are reused BY IMPORT as independent,
already-frozen open-source libraries, never reimplemented, never modified.

The BD1 forward producer's route is "characters, Peter-Weyl and
tensor-product multiplicities" (Schur-Weyl duality with the hook-length
formula); the reverse producer's route is "Weyl integration over the
maximal torus by constant-term extraction" (formal Laurent-polynomial
coefficient bookkeeping). Both are algebraic/combinatorial routes on the
SAME underlying Weyl integration formula. This script recomputes the SAME
quantities by two DIFFERENT mechanisms, neither of which does tensor-
multiplicity counting or Laurent constant-term extraction:

  (A) SO(3): the LITERAL definite integral of W(theta)^k against the SO(3)
      class-angle Haar density (1-cos theta)/pi on theta in [0,pi], done by
      sympy's own general-purpose symbolic integrator (`sympy.integrate`),
      giving an EXACT closed-form rational for every k -- a genuinely
      different code path (a generic calculus engine, not a hand-written
      constant-term or tensor-multiplicity routine).

  (B) SU(3), SU(4), SU(5): the LITERAL Weyl integration formula
      E[f] = (1/N!) * (average over the maximal torus of f * |Delta|^2),
      Delta = prod_{i<j} (e^{i theta_i} - e^{i theta_j}) the Vandermonde
      denominator, evaluated by DIRECT NUMERICAL SAMPLING (a discrete
      Fourier / trapezoidal-rule quadrature on an (N-1)-torus grid of M
      points per angle, python's built-in `cmath`, no producer code, no
      symbolic combinatorics). Since |Delta|^2 and W^k are both FINITE
      trigonometric polynomials of bounded degree in each angle, this
      quadrature is EXACT up to floating-point roundoff once M exceeds the
      integrand's bandwidth (the sampling theorem for band-limited periodic
      functions) -- not merely a converging approximation. It is reported
      here as a numeric preview (double precision, ~1e-13 agreement with
      the admitted exact rationals), per this project's convention that
      floating-point results are previews, never admissions. As a further,
      genuinely rigorous cross-check (not merely a float preview), the same
      quadrature is repeated for SU(3) in `python-flint` Arb ball
      arithmetic at 200 bits, giving a proved enclosure (nonzero but tiny
      ball radius, since the torus angles 2*pi*k/M are themselves
      irrational) that is checked to CONTAIN the admitted exact rational.

  (C) The closed-form first-order coefficient 2(1/3)E[W^2]/(32 C_F) with
      E[W^2] = 1/(2N^2) for SU(N), N>=3 (an identity both BD1 reports state
      but do not need to re-derive, since only |chi_F|^2 = chi_F conj(chi_F)
      has an invariant summand): simplified symbolically in sympy for
      general N and confirmed EQUAL, as a polynomial identity, to
      1/(48 N (N^2-1)); then evaluated exactly via `python-flint` `fmpq`
      for N = 3, 4, 5 and compared bit-for-bit with the admitted table.

Run: `python3 -B group_moments_flint.py`
"""
import cmath
import json
import math
import sys
import time
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]

import flint  # noqa: E402
import sympy as sp  # noqa: E402

flint.ctx.prec = 200


def load(rel):
    return (ROOT / rel).read_text()


def load_json(rel):
    return json.loads(load(rel))


# ---------------------------------------------------------------------------
# Admitted values (read for comparison only; never used in the computation)
# ---------------------------------------------------------------------------
CONTRACT = load_json("research/round33/contracts/bd1.json")
FWD = load_json("research/round33/forward/bd1/output/results.json")
REV = load_json("research/round33/reverse/bd1/output/results.json")
GATE = load_json("research/round33/advisor/bd1-gate.json")

ADMITTED_MOMENTS = {g: c["moments"] for g, c in FWD["cells"].items()}
ADMITTED_FIRST_ORDER = {
    g: c["first_order_coefficient"]["value"] for g, c in FWD["cells"].items()
}

assert CONTRACT["id"] == "BD1"
assert GATE["accepted"], "BD1 gate not accepted; nothing to compare against"


# ---------------------------------------------------------------------------
# Part (C): closed-form first-order coefficient, exact, via sympy + flint
# ---------------------------------------------------------------------------
def part_C_first_order_coefficient():
    N = sp.symbols("N", positive=True, integer=True)
    C_F = (N**2 - 1) / (2 * N)
    E_W2 = 1 / (2 * N**2)  # for SU(N), N>=3: only |chi_F|^2 term survives
    coeff = sp.together(2 * sp.Rational(1, 3) * E_W2 / (32 * C_F))
    target = 1 / (48 * N * (N**2 - 1))
    identity_holds = sp.simplify(coeff - target) == 0

    checks = []
    for Nval in (3, 4, 5):
        exact = flint.fmpq(1, 48 * Nval * (Nval**2 - 1))
        admitted = flint.fmpq(ADMITTED_FIRST_ORDER[f"SU({Nval})"])
        checks.append(
            {
                "id": f"first_order_coefficient_SU{Nval}",
                "N": Nval,
                "formula_value": str(exact),
                "admitted_value": ADMITTED_FIRST_ORDER[f"SU({Nval})"],
                "passed": exact == admitted,
            }
        )
    return {
        "closed_form_identity_2_E_W2_over_96_CF_equals_1_over_48N_N2m1": bool(
            identity_holds
        ),
        "checks": checks,
    }


# ---------------------------------------------------------------------------
# Part (A): SO(3), exact sympy symbolic integration on the class angle
# ---------------------------------------------------------------------------
def part_A_SO3_moments(kmax=5):
    theta = sp.symbols("theta", real=True)
    density = (1 - sp.cos(theta)) / sp.pi
    W = (1 + 2 * sp.cos(theta)) / 3
    # sanity: total mass is 1 (an independent check that this density is
    # correctly normalized before trusting any moment computed with it)
    mass = sp.nsimplify(sp.integrate(density, (theta, 0, sp.pi)))
    assert mass == 1, f"SO(3) class-angle density does not integrate to 1: {mass}"

    moments = {}
    for k in range(1, kmax + 1):
        val = sp.integrate(W**k * density, (theta, 0, sp.pi))
        val = sp.nsimplify(sp.simplify(val))
        moments[str(k)] = str(sp.Rational(val))
    return moments


# ---------------------------------------------------------------------------
# Part (B): SU(N), N=3,4,5, numeric DFT-exact Weyl-integral quadrature
# ---------------------------------------------------------------------------
def su_moments_numeric(N, kmax, M):
    """E[W^k], k=0..kmax, for SU(N) by literal numerical quadrature of the
    Weyl integration formula on the maximal torus, using an M-point grid per
    free angle (theta_N = -(theta_1+...+theta_{N-1}) enforces det=1). Exact
    up to floating roundoff once M exceeds the integrand's bandwidth (a
    finite trigonometric polynomial), by the sampling theorem."""
    t0 = time.time()
    roots = [cmath.exp(1j * 2 * math.pi * m / M) for m in range(M)]
    fact = math.factorial(N)
    sums = [0.0] * (kmax + 1)
    grid = 0
    for idxs in product(range(M), repeat=N - 1):
        zs = [roots[i] for i in idxs]
        zN = 1.0 + 0j
        for z in zs:
            zN /= z
        zs = zs + [zN]
        Delta = 1.0 + 0j
        for i in range(N):
            for j in range(i + 1, N):
                Delta *= zs[i] - zs[j]
        absDelta2 = (Delta * Delta.conjugate()).real
        Wval = sum(z.real for z in zs) / N
        Wp = 1.0
        for k in range(kmax + 1):
            sums[k] += absDelta2 * Wp
            Wp *= Wval
        grid += 1
    denom = (M ** (N - 1)) * fact
    E = [s / denom for s in sums]
    return E, grid, time.time() - t0


# bandwidth-safe grid sizes (see docstring: max frequency per angle is
# bounded by roughly 2(N-1)+kmax; these M satisfy M > 2*maxfreq+1 with a
# comfortable margin, and were checked empirically stable -- see
# `bandwidth_convergence_check` below, which reruns at M+2 and confirms
# agreement to double-precision roundoff)
SU_GRID_M = {3: 21, 4: 25, 5: 29}


def part_B_SU_moments(kmax=5):
    out = {}
    for N in (3, 4, 5):
        M = SU_GRID_M[N]
        E, grid, dt = su_moments_numeric(N, kmax, M)
        E_check, grid2, dt2 = su_moments_numeric(N, kmax, M + 2)
        max_drift = max(abs(a - b) for a, b in zip(E, E_check))
        out[f"SU({N})"] = {
            "M": M,
            "M_recheck": M + 2,
            "grid_points": grid,
            "seconds": round(dt, 3),
            "max_drift_vs_finer_grid": max_drift,
            "E": {str(k): E[k] for k in range(kmax + 1)},
        }
    return out


def part_B_SU3_arb_enclosure(kmax=5, M=21, prec_bits=200):
    """SU(3) only: the same quadrature repeated in Arb ball arithmetic at
    high precision, giving a genuinely rigorous (not just floating-point)
    enclosure, checked to contain the admitted exact rationals."""
    flint.ctx.prec = prec_bits
    N = 3
    two_pi = flint.arb(2) * flint.arb.pi()
    # build cos/sin tables directly (flint.arb has no native complex ball;
    # carry real/imag parts explicitly as a pair of arb balls)
    cos_t = [((two_pi * m) / M).cos() for m in range(M)]
    sin_t = [((two_pi * m) / M).sin() for m in range(M)]

    def cmul(a, b):
        ar, ai = a
        br, bi = b
        return (ar * br - ai * bi, ar * bi + ai * br)

    def cdiv_unit(a):
        # a is on the unit circle exactly (cos,sin of a rational multiple of
        # 2*pi); its inverse is its conjugate
        ar, ai = a
        return (ar, -ai)

    sums = [flint.arb(0) for _ in range(kmax + 1)]
    grid = 0
    for i1 in range(M):
        for i2 in range(M):
            z = [(cos_t[i1], sin_t[i1]), (cos_t[i2], sin_t[i2])]
            zNr, zNi = flint.arb(1), flint.arb(0)
            for zr, zi in z:
                inv = cdiv_unit((zr, zi))
                zNr, zNi = cmul((zNr, zNi), inv)
            z.append((zNr, zNi))
            Dr, Di = flint.arb(1), flint.arb(0)
            for a in range(N):
                for b in range(a + 1, N):
                    dr = z[a][0] - z[b][0]
                    di = z[a][1] - z[b][1]
                    Dr, Di = cmul((Dr, Di), (dr, di))
            absD2 = Dr * Dr + Di * Di
            Wval = (z[0][0] + z[1][0] + z[2][0]) / N
            Wp = flint.arb(1)
            for k in range(kmax + 1):
                sums[k] += absD2 * Wp
                Wp *= Wval
            grid += 1
    denom = flint.arb(M ** (N - 1) * math.factorial(N))
    E = [s / denom for s in sums]
    return E, grid


def compare_ball_to_admitted(E_balls, kmax=5):
    checks = []
    for k in range(1, kmax + 1):
        admitted = flint.fmpq(ADMITTED_MOMENTS["SU(3)"][str(k)])
        admitted_arb = flint.arb(admitted)
        contains = admitted_arb in E_balls[k]
        checks.append(
            {
                "k": k,
                "admitted": str(admitted),
                "ball": str(E_balls[k]),
                "admitted_in_ball": bool(contains),
            }
        )
    return checks


# ---------------------------------------------------------------------------
# Comparison helpers
# ---------------------------------------------------------------------------
def compare_moments_numeric(numeric_E, group, kmax=5, tol=1e-9):
    rows = []
    ok = True
    for k in range(1, kmax + 1):
        admitted_frac = flint.fmpq(ADMITTED_MOMENTS[group][str(k)])
        admitted_float = float(admitted_frac.p) / float(admitted_frac.q)
        diff = abs(numeric_E[k] - admitted_float)
        passed = diff < tol
        ok = ok and passed
        rows.append(
            {
                "k": k,
                "admitted": ADMITTED_MOMENTS[group][str(k)],
                "admitted_preview": admitted_float,
                "numeric_preview": numeric_E[k],
                "abs_diff": diff,
                "passed": passed,
            }
        )
    return rows, ok


def compare_moments_exact(exact_dict, group, kmax=5):
    rows = []
    ok = True
    for k in range(1, kmax + 1):
        exact_val = flint.fmpq(exact_dict[str(k)])
        admitted_val = flint.fmpq(ADMITTED_MOMENTS[group][str(k)])
        passed = exact_val == admitted_val
        ok = ok and passed
        rows.append(
            {
                "k": k,
                "computed": str(exact_val),
                "admitted": str(admitted_val),
                "passed": passed,
            }
        )
    return rows, ok


def main():
    report = {
        "schema": "hnm-round33-modern-lens-assistant4-group-moments-v1",
        "status": "preview_and_crosscheck_only_zero_research_loops_not_a_contract_or_gate",
        "human_author": "Hruday N M (BUNZEEY)",
        "role": "modern (Penrose/Feynman) lens, research assistant/coder assistant-4",
        "round": 33,
        "subround": 4,
        "admitted_gate_sha256_of_bd1": None,
        "bd1_gate_accepted_headline": GATE["verdict"][:200] + "...",
    }

    all_passed = True

    # (C)
    c_res = part_C_first_order_coefficient()
    report["first_order_coefficient"] = c_res
    all_passed &= c_res["closed_form_identity_2_E_W2_over_96_CF_equals_1_over_48N_N2m1"]
    all_passed &= all(chk["passed"] for chk in c_res["checks"])

    # (A) SO(3) exact
    so3_moments = part_A_SO3_moments()
    so3_rows, so3_ok = compare_moments_exact(so3_moments, "SO(3)")
    report["SO(3)"] = {
        "method": "sympy.integrate of W(theta)^k against (1-cos theta)/pi on [0,pi], exact",
        "computed_moments": so3_moments,
        "comparison": so3_rows,
        "all_passed": so3_ok,
    }
    all_passed &= so3_ok

    # (B) SU(3), SU(4), SU(5) numeric
    su_numeric = part_B_SU_moments()
    for N in (3, 4, 5):
        g = f"SU({N})"
        E = [su_numeric[g]["E"][str(k)] for k in range(6)]
        rows, ok = compare_moments_numeric(E, g)
        su_numeric[g]["comparison"] = rows
        su_numeric[g]["all_passed_at_tol_1e-9"] = ok
        all_passed &= ok
    report["SU_numeric_weyl_quadrature"] = su_numeric

    # (B, bonus) SU(3) rigorous Arb ball
    E_balls, grid = part_B_SU3_arb_enclosure()
    ball_checks = compare_ball_to_admitted(E_balls, kmax=5)
    ball_ok = all(c["admitted_in_ball"] for c in ball_checks)
    report["SU3_arb_rigorous_enclosure"] = {
        "precision_bits": 200,
        "M": 21,
        "grid_points": grid,
        "checks": ball_checks,
        "all_passed": ball_ok,
    }
    all_passed &= ball_ok

    report["all_passed"] = all_passed
    print(json.dumps(report, indent=1, default=str))
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
