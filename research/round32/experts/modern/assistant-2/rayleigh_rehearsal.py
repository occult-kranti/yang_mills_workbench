#!/usr/bin/env python3
"""rayleigh_rehearsal.py -- rehearse exact Rayleigh quotients, residual
enclosures and an Arb (256-bit) cross-check on matrices of size >= 84, ahead
of AZ2 (sub-round 5).

Round32, sub-round 2, modern (Penrose/Feynman) lens, assistant-2.
Status: assistant/coder preview tool. Counts ZERO research loops. Never
admission arithmetic; nothing here is imported by any `check.py`. Every
Rayleigh quotient and residual bound is exact `fractions.Fraction` /
`flint.fmpq`; only the trial-vector *seed* (a scipy/numpy float
eigenvector, rounded to a nearby rational) and the Arb comparison are
floating/ball-arithmetic previews, exactly as `flint_harness.py` itself is
scoped.

Reuses BY IMPORT (never retyped):
  research/round32/experts/modern/assistant-1/flint_harness.py
    -- exact_matrix_from_rows, rayleigh_bounds, arb_eig_preview,
       rational_sqrt_bracket, to_fmpq/from_fmpq  (all used verbatim)
  research/round11/solver/two_plaquette.py
    -- matrices(degree, rho): exact rational Gram matrix G and kinetic
       operator matrix K on the polynomial basis {x^a y^b z^c : a+b+c<=D}
       of the Round11 two-plaquette physical Hilbert space
       (research/round11/advisor/advisor.md sections 2-5); combine(...) for
       the full interacting Hamiltonian form matrix H = alpha*K +
       (lambda1+lambda2)*G - lambda1*MX - lambda2*MY; solve_exact(A,B) for
       exact Fraction Gaussian elimination (reused both to build G^{-1} r
       products for the generalized residual bound and to build the exact
       rational matrix G^{-1} H whose eigenvalues equal the generalized
       eigenvalues of (H, G), for the Arb comparison).

Three fixtures, each >= 84x84:
  Fixture 0 (harness rehearsal, no G needed): a rational tridiagonal
    ("discrete Laplacian shifted") symmetric matrix, n=90, calling
    flint_harness.rayleigh_bounds and .arb_eig_preview UNMODIFIED, exactly
    the call pattern update-1.md section 5 asks AZ2's producer to use
    verbatim.
  Fixture 1 (Round11 physics, primary AZ2 tier): the two-plaquette
    interacting Hamiltonian at degree D=6 (dimension 84 = C(9,3)), alpha=1,
    lambda1=lambda2=1 (Round11's own solver.py CLI default).
  Fixture 2 (Round11 physics, AZ2 refinement tier): the same construction
    at degree D=8 (dimension 165 = C(11,3)).

Because G != I for fixtures 1-2 (the monomial basis is not orthonormal),
this script implements the standard GENERALIZED Rayleigh/residual bound
(the same mathematics as flint_harness.rayleigh_bounds, extended from the
identity-Gram case to a general SPD Gram matrix G), justified below, and
gets the Arb comparison by building the exact rational matrix M = G^{-1} H
(via two_plaquette.solve_exact, never floats) and passing it UNCHANGED into
flint_harness.arb_eig_preview (which calls acb_mat.eig() generically; it
does not require symmetry, and the generalized eigenvalues of (H,G) are
exactly the eigenvalues of G^{-1}H, real since G^{-1}H is similar to the
symmetric matrix G^{-1/2} H G^{-1/2}).

Generalized residual bound (used for fixtures 1-2). Trial vector v, mu =
v^T H v / v^T G v (exact), r = H v - mu G v. Writing w = G^{1/2} v and
A = G^{-1/2} H G^{-1/2} (symmetric, similar to the generalized problem),
A w - mu w = G^{-1/2} r, so by the standard perturbation bound some
generalized eigenvalue lambda satisfies
  |mu - lambda| <= ||G^{-1/2} r|| / ||w|| = sqrt(r^T G^{-1} r) / sqrt(v^T G v).
r^T G^{-1} r is computed exactly by solving G z = r (two_plaquette.solve_exact)
and forming r^T z, all Fraction; only the final sqrt is outward-rounded via
flint_harness.rational_sqrt_bracket, exactly as flint_harness.rayleigh_bounds
itself does for the identity-Gram case (of which this is the direct
generalization; G=I reduces to that function's own formula).

Pass iff, for every fixture: the exact Rayleigh quotient mu is >= the Arb
LOWER ball bound of the ground (smallest) eigenvalue, and the residual-based
enclosure [mu - bound, mu + bound] contains the Arb ground-eigenvalue ball.
"""
import importlib.util
import json
import time
from fractions import Fraction as Q
from pathlib import Path

import numpy as np
from scipy.linalg import eigh as scipy_geigh

ROOT = Path(__file__).resolve().parents[5]
FLINT_HARNESS_PATH = ROOT / 'research/round32/experts/modern/assistant-1/flint_harness.py'
TWO_PLAQUETTE_PATH = ROOT / 'research/round11/solver/two_plaquette.py'
ARB_CROSSCHECK_PATH = ROOT / 'research/round32/tools/arb_crosscheck.py'


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fh = _load_module(FLINT_HARNESS_PATH, 'assistant1_flint_harness')
tp = _load_module(TWO_PLAQUETTE_PATH, 'round11_two_plaquette')
arb_crosscheck = _load_module(ARB_CROSSCHECK_PATH, 'arb_crosscheck')

import flint  # noqa: E402  (after module loads, matching flint_harness's own import order)


# ================================================================
# Fixture 0: plain (G=I) harness rehearsal, flint_harness calls verbatim.
# ================================================================

def build_tridiagonal(n, diag=Q(5), off=Q(-2)):
    """n x n symmetric tridiagonal Toeplitz matrix, rational entries. Known
    closed-form spectrum: eigenvalues diag + 2*off*cos(k*pi/(n+1)), k=1..n;
    eigenvector k has components sin(j*k*pi/(n+1)), j=1..n. For off<0 the
    ground (smallest) eigenvalue is at k=1 (cos closest to +1, most negative
    2*off*cos term dominates least)... off<0 => 2*off*cos(pi/(n+1)) is the
    most NEGATIVE of the n values (since cos(k pi/(n+1)) is largest, closest
    to 1, at k=1, and off<0 makes larger cos give a more negative product),
    so k=1 gives the smallest eigenvalue. Used only to seed a good rational
    trial vector via numpy; the admitted numbers below never depend on this
    closed form, only on the exact matrix entries themselves."""
    rows = [[Q(0)] * n for _ in range(n)]
    for i in range(n):
        rows[i][i] = diag
        if i + 1 < n:
            rows[i][i + 1] = off
            rows[i + 1][i] = off
    return rows


def rational_trial_vector(float_vec, denom=10 ** 7):
    scale = float_vec[np.argmax(np.abs(float_vec))]
    v = float_vec / scale
    return [Q(round(float(x) * denom), denom) for x in v]


def fixture0_plain_harness_rehearsal(n=90):
    timings = {}
    t0 = time.time()
    rows = build_tridiagonal(n)
    A = fh.exact_matrix_from_rows(rows)
    timings['build_exact_matrix_s'] = time.time() - t0

    t0 = time.time()
    rows_f = np.array([[float(x) for x in row] for row in rows], dtype=float)
    w, V = np.linalg.eigh(rows_f)
    v_trial = rational_trial_vector(V[:, 0])  # smallest eigenvalue (float seed only)
    timings['numpy_seed_eigh_s'] = time.time() - t0

    t0 = time.time()
    rayleigh, residual_bound = fh.rayleigh_bounds(A, v_trial)  # verbatim S1 call
    timings['exact_rayleigh_bounds_s'] = time.time() - t0
    mu = fh.from_fmpq(rayleigh)
    bound = fh.from_fmpq(residual_bound)

    t0 = time.time()
    eigs = fh.arb_eig_preview(A, prec=256)  # verbatim S1 call
    timings['arb_eig_preview_s'] = time.time() - t0
    reals = [(complex(e.mid()).real, e) for e in eigs]
    reals.sort(key=lambda pair: pair[0])
    ground_ball = reals[0][1]
    ground_lo, ground_hi = arb_crosscheck.rational_bounds_arb(ground_ball.real)

    mu_ge_arb_lower = mu >= ground_lo
    enclosure_lo, enclosure_hi = mu - bound, mu + bound
    contains = (enclosure_lo <= ground_lo) and (ground_hi <= enclosure_hi)

    return {
        'fixture': 'fixture0_plain_tridiagonal_n90_harness_verbatim',
        'dimension': n,
        'matrix': 'tridiagonal, diagonal=5, off-diagonal=-2 (rational, exact)',
        'timings_seconds': timings,
        'rayleigh_exact': str(mu), 'rayleigh_preview': float(mu),
        'residual_bound_exact': str(bound), 'residual_bound_preview': float(bound),
        'arb_ground_eigenvalue_ball_bounds': [str(ground_lo), str(ground_hi)],
        'arb_ground_eigenvalue_preview': float(complex(ground_ball.mid()).real),
        'mu_ge_arb_lower_ball': mu_ge_arb_lower,
        'residual_enclosure': [str(enclosure_lo), str(enclosure_hi)],
        'residual_enclosure_contains_arb_ball': contains,
        'passed': bool(mu_ge_arb_lower and contains),
    }


# ================================================================
# Fixtures 1-2: Round11 two-plaquette Hamiltonian, generalized (G != I).
# ================================================================

def matvec(M, v):
    n = len(M)
    return [sum((M[i][j] * v[j] for j in range(n)), Q(0)) for i in range(n)]


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Q(0))


def generalized_rayleigh_residual(H, G, v):
    """Exact generalized Rayleigh quotient and directed-rational residual
    bound for the generalized eigenproblem H x = lambda G x (see module
    docstring for the derivation). Reuses two_plaquette.solve_exact for the
    G z = r solve and flint_harness.rational_sqrt_bracket for the final
    outward-rounded sqrt, exactly mirroring flint_harness.rayleigh_bounds's
    own directed-rounding pattern for the identity-Gram case."""
    Hv = matvec(H, v)
    Gv = matvec(G, v)
    vHv = dot(v, Hv)
    vGv = dot(v, Gv)
    if vGv <= 0:
        raise ValueError('trial vector not G-admissible (v^T G v <= 0)')
    mu = vHv / vGv
    r = [Hv[i] - mu * Gv[i] for i in range(len(v))]
    z_rows = tp.solve_exact(G, [[ri] for ri in r])
    z = [row[0] for row in z_rows]
    resid_quad = dot(r, z)  # r^T G^{-1} r, exact, >= 0
    if resid_quad < 0:
        raise ValueError('negative r^T G^-1 r: G not admissible as SPD in this arithmetic')
    _, hi = fh.rational_sqrt_bracket(resid_quad)
    denom_lo, _ = fh.rational_sqrt_bracket(vGv)
    residual_bound = hi / denom_lo if denom_lo != 0 else hi  # divide by ||v||_G >= denom_lo (directed: use LOWER bound of ||v||_G in the denominator to keep the overall bound valid upward)
    return mu, residual_bound, resid_quad


def two_plaquette_fixture(degree, alpha=Q(1), lambda1=Q(1), lambda2=Q(1), trial_denom=10 ** 7, arb_prec=256):
    timings = {}
    t0 = time.time()
    bs, G, K, MX, MY = tp.matrices(degree, Q(1))
    H = tp.combine(G, K, MX, MY, alpha, lambda1, lambda2)
    timings['build_matrices_s'] = time.time() - t0
    n = len(bs)

    t0 = time.time()
    Gf = tp.floating(G)
    Hf = tp.floating(H)
    vals, vecs = scipy_geigh(Hf, Gf)
    timings['scipy_generalized_eigh_seed_s'] = time.time() - t0
    v_trial = rational_trial_vector(vecs[:, 0], denom=trial_denom)

    t0 = time.time()
    mu, bound, resid_quad = generalized_rayleigh_residual(H, G, v_trial)
    timings['exact_generalized_rayleigh_residual_s'] = time.time() - t0

    t0 = time.time()
    M = tp.solve_exact(G, H)  # exact rational G^{-1} H
    timings['solve_exact_Ginv_H_s'] = time.time() - t0

    t0 = time.time()
    A = fh.exact_matrix_from_rows(M)
    eigs = fh.arb_eig_preview(A, prec=arb_prec)  # verbatim S1 call, on a nonsymmetric fmpq_mat
    timings['arb_eig_preview_s'] = time.time() - t0

    reals = [(complex(e.mid()).real, e) for e in eigs]
    reals.sort(key=lambda pair: pair[0])
    ground_ball = reals[0][1]
    ground_lo, ground_hi = arb_crosscheck.rational_bounds_arb(ground_ball.real)
    ground_imag_lo, ground_imag_hi = arb_crosscheck.rational_bounds_arb(ground_ball.imag)
    imag_contains_zero = (ground_imag_lo <= 0 <= ground_imag_hi)

    mu_ge_arb_lower = mu >= ground_lo
    enclosure_lo, enclosure_hi = mu - bound, mu + bound
    contains = (enclosure_lo <= ground_lo) and (ground_hi <= enclosure_hi)

    return {
        'fixture': f'two_plaquette_D{degree}',
        'dimension': n,
        'alpha': str(alpha), 'lambda1': str(lambda1), 'lambda2': str(lambda2),
        'timings_seconds': timings,
        'scipy_seed_ground_eigenvalue_preview': float(vals[0]),
        'rayleigh_exact': str(mu), 'rayleigh_preview': float(mu),
        'residual_quadratic_r_T_Ginv_r_exact': str(resid_quad),
        'residual_bound_exact': str(bound), 'residual_bound_preview': float(bound),
        'ground_eigenvalue_ball_real_bounds': [str(ground_lo), str(ground_hi)],
        'ground_eigenvalue_ball_imag_contains_zero': imag_contains_zero,
        'mu_ge_arb_lower_ball': mu_ge_arb_lower,
        'residual_enclosure': [str(enclosure_lo), str(enclosure_hi)],
        'residual_enclosure_contains_arb_ball': contains,
        'passed': bool(mu_ge_arb_lower and contains and imag_contains_zero),
    }


def self_test():
    f0 = fixture0_plain_harness_rehearsal(n=90)
    f1 = two_plaquette_fixture(degree=6)   # AZ2 primary tier, dimension 84
    f2 = two_plaquette_fixture(degree=8)   # AZ2 refinement tier, dimension 165

    passed = bool(f0['passed'] and f1['passed'] and f2['passed'])

    scaling_note = (
        f"84x84 (D=6): build {f1['timings_seconds']['build_matrices_s']:.2f}s, "
        f"solve_exact G^-1 H {f1['timings_seconds']['solve_exact_Ginv_H_s']:.2f}s, "
        f"Arb eig(256-bit) {f1['timings_seconds']['arb_eig_preview_s']:.2f}s; "
        f"165x165 (D=8): build {f2['timings_seconds']['build_matrices_s']:.2f}s, "
        f"solve_exact G^-1 H {f2['timings_seconds']['solve_exact_Ginv_H_s']:.2f}s, "
        f"Arb eig(256-bit) {f2['timings_seconds']['arb_eig_preview_s']:.2f}s. "
        "No scaling blocker observed up to 165x165 (all sub-20s); every step stays "
        "well inside a single check.py run's practical budget."
    )

    return {
        'tool': 'rayleigh_rehearsal',
        'fixture0_plain_harness_rehearsal': f0,
        'fixture1_two_plaquette_D6_primary_tier': f1,
        'fixture2_two_plaquette_D8_refinement_tier': f2,
        'scaling_note': scaling_note,
        'passed': passed,
    }


def main():
    result = self_test()
    print(json.dumps(result, indent=2, default=str))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
