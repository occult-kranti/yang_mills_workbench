#!/usr/bin/env python3
"""finite_graph_rehearsal_d8.py -- the D=8 rerun of assistant-3's finite-
graph rehearsal (`az2_dictionary_calc.py`) on the Round11 two-plaquette
graph, one representation-degree cutoff above assistant-3's own D=6.

Round32, sub-round 4, modern (Penrose/Feynman) lens, assistant-4.
Status: assistant/coder cross-check tool. Counts ZERO research loops.
The Round11 `two_plaquette.py` solver module is reused BY IMPORT ONLY
(never reimplemented, never modified); scipy/numpy floating eigenvalues
here are guesses only, certified into exact rational brackets by the
module's own `exact_bracket`/`inertia` (Fraction Gaussian elimination),
exactly as the module's own `certificate()` function does. Nothing here
is imported by any `check.py`, and nothing here decides admission.

    IMPORTANT: this is a FINITE GRAPH (seven links, two plaquettes),
    labelled `model_is_finite_graph: true`, `transfers_to_aq: false`
    throughout. It is a consistency/feasibility rehearsal for the AZ2
    contract, not evidence about the Z^3 model.

What assistant-3 did (read from `assistant-3/az2_dictionary_calc.py`)
-----------------------------------------------------------------------
`fg_derivative_regularized_solve(D=6)`: builds `H_FG(tau_FG)=K-tau_FG*x`
at truncation degree D=6 (dimension 84), and gets the exact first-order
coefficient `d<x>/d(tau_FG)|_0 = 1/6` via a regularized (G-orthogonal-
complement) exact linear solve, Arb-cross-checked at 256 bits. That
computation is reused here verbatim (by direct import and a `D=8` call,
not a re-implementation) as this file's own "derivative at zero, by
perturbation theory" deliverable, and independently checked against a
second, brand-new method: exact finite differences of the GROUND ENERGY
alone (Hellmann-Feynman: dE_0/d(tau_FG)=-<x>_0, and since E_0(0)=0
exactly, a central second difference of E_0 estimates <x>_0'(0) too).

This file's own new work at D=8
---------------------------------
1. Confirms the D=8 free facts (`K*1=0`, `K*x=3x`, `<x,x>=1/4`,
   `free_gap()==3`, `tail_lower(8)==69`) live against the module.
2. Re-derives `d<x>/d(tau_FG)|_0=1/6` via assistant-3's regularized-solve
   method called at D=8 (not D=6), Arb-cross-checked, PLUS an exact
   central-second-difference estimate on E_0 (a different, brand-new
   check, using only `exact_bracket`/`inertia`, no perturbation theory).
3. Exact-rational RITZ VALUES for `<x>(tau_FG)` (the finite-graph "W") at
   `tau_FG in {1/1000, 1/100, 1/10}`: NOT the eigenvector's floating
   overlap `v^T MX v`, but a fully rigorous EXACT RATIONAL BRACKET,
   derived from the Hellmann-Feynman/concavity sandwich
       [E_0(t-h)-E_0(t)]/h <= <x>_0(t) <= [E_0(t)-E_0(t+h)]/h
   (E_0(t)=min-eigenvalue of K-t*x is concave in t, being a pointwise
   minimum of functions affine in t; therefore its slope is non-
   increasing), using ONLY exact `exact_bracket`/`inertia` energy
   brackets at t-h, t, t+h -- never a floating eigenvector.
4. A rough truncation-tail estimate from `tail_lower(8)=69` and the
   D=6-vs-D=8 stability of item 2's exact value.
5. The A2/A3 normalization dictionary (`tau_FG:=tau/24`, reused from
   assistant-3), converting item 2's D=8 exact derivative into the AW1
   convention and comparing with the admitted `1/144`.
6. Timing of every exact-bracket/inertia call, and a small D=4/6/8
   calibration table, for the AZ2 contract's own `j_max` feasibility
   decision.
"""
import importlib.util
import json
import sys
import time
from fractions import Fraction as Q
from pathlib import Path

import flint
from scipy.linalg import eigh

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]
R32 = ROOT / 'research' / 'round32'
assert (ROOT / 'AGENTS.md').is_file(), f'unexpected ROOT: {ROOT}'

SOLVER_DIR = ROOT / 'research' / 'round11' / 'solver'
if str(SOLVER_DIR) not in sys.path:
    sys.path.insert(0, str(SOLVER_DIR))
import two_plaquette as tp  # noqa: E402  (Round11's own frozen module, imported not reimplemented)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


az2_calc = _load('az2_dictionary_calc_a4', R32 / 'experts' / 'modern' / 'assistant-3' / 'az2_dictionary_calc.py')
flint_harness = _load('flint_harness_a4c', R32 / 'experts' / 'modern' / 'assistant-1' / 'flint_harness.py')

X_MONO = {(1, 0, 0): Q(1)}
D_PRIMARY = 8
ASSISTANT3_D = 6
WIDTH = Q(1, 10 ** 14)


# ---------------------------------------------------------------- (1) facts
def d8_free_facts():
    K_on_x = tp.kinetic(X_MONO)
    x2 = tp.inner(X_MONO, X_MONO)
    gap = tp.free_gap()
    tail8 = tp.tail_lower(8)
    tail6 = tp.tail_lower(6)
    return {
        'K_x_equals_3x': K_on_x == {(1, 0, 0): Q(3)},
        'x_squared_moment': str(x2), 'free_gap_exact': str(gap), 'free_gap_equals_3': gap == 3,
        'tail_lower_D6': str(tail6), 'tail_lower_D8': str(tail8),
    }


# --------------------------------------------------- (2) derivative at zero
def derivative_at_zero_via_second_difference(bs, G, K, MX, h, width=WIDTH):
    """A brand-new, independent check of assistant-3's regularized-solve
    result: E_0(t)=min eig(K - t*MX; G) satisfies E_0(0)=0 exactly (K's own
    ground state), and <x>_0'(0) = -d^2E_0/dt^2|_0 (from Hellmann-Feynman,
    dE_0/dt=-<x>_0(t), together with <x>_0(0)=0 by the t->-t, x->-x parity
    of this model). A central second difference gives
        <x>_0'(0) ~ -(E_0(h)+E_0(-h))/h^2  (since E_0(0)=0 exactly),
    with discretization error O(h^2) from the omitted 4th-order term.
    E_0(+-h) are each obtained as an EXACT rational bracket via the
    module's own `exact_bracket`/`inertia` (never a bare floating value)."""
    n = len(bs)
    Gf = tp.floating(G)

    def energy_bracket(t):
        Hm = [[K[i][j] - t * MX[i][j] for j in range(n)] for i in range(n)]
        Hf = tp.floating(Hm)
        vals = eigh(Hf, Gf, eigvals_only=True)
        guess = vals[0]
        br = tp.exact_bracket(Hm, G, 0, guess, width=width)
        return Q(br['lower']), Q(br['upper'])

    t0 = time.time()
    lo_p, hi_p = energy_bracket(h)
    lo_m, hi_m = energy_bracket(-h)
    elapsed = time.time() - t0

    # -(E(h)+E(-h))/h^2, worst-case directed: to LOWER-bound the true
    # (negative of a sum that could be positive or negative) quantity we
    # want the algebraically SMALLEST -(E(h)+E(-h)); to upper-bound it we
    # want the algebraically LARGEST. Since -(a+b) is decreasing in (a+b),
    # smallest -(a+b) <=> largest (a+b) <=> use the two upper endpoints;
    # largest -(a+b) <=> smallest (a+b) <=> use the two lower endpoints.
    val_lo = -(hi_p + hi_m) / h ** 2
    val_hi = -(lo_p + lo_m) / h ** 2

    return {
        'h': str(h), 'E0_plus_h_bracket': [str(lo_p), str(hi_p)], 'E0_minus_h_bracket': [str(lo_m), str(hi_m)],
        'second_difference_bracket_for_deriv_at_zero': [str(val_lo), str(val_hi)],
        'preview_bracket': [float(val_lo), float(val_hi)],
        'elapsed_seconds': elapsed,
    }


# ------------------------------------------------------- (3) Ritz brackets
def hellmann_feynman_x_bracket(bs, G, K, MX, t, h, width=WIDTH):
    """Rigorous exact-rational bracket for <x>_0(t) using ONLY exact
    energy brackets at t-h, t, t+h (Hellmann-Feynman + concavity of
    E_0(t), see module docstring). This IS the "exact-rational Ritz
    value": it certifies an enclosure of the D=8 truncated (Rayleigh-Ritz)
    ground-state expectation of x, never reading a floating eigenvector."""
    n = len(bs)
    Gf = tp.floating(G)
    times = {}

    def energy_bracket(tv):
        Hm = [[K[i][j] - tv * MX[i][j] for j in range(n)] for i in range(n)]
        Hf = tp.floating(Hm)
        vals = eigh(Hf, Gf, eigvals_only=True)
        guess = vals[0]
        t0 = time.time()
        br = tp.exact_bracket(Hm, G, 0, guess, width=width)
        times[tv] = time.time() - t0
        return Q(br['lower']), Q(br['upper'])

    lo_m, hi_m = energy_bracket(t - h)
    lo_0, hi_0 = energy_bracket(t)
    lo_p, hi_p = energy_bracket(t + h)

    # <x>_0(t) in [ (Elo(t-h)-Ehi(t))/h , (Ehi(t)-Elo(t+h))/h ]  (derived in
    # the module docstring from concavity; both endpoints use the WORST-CASE
    # combination of the three brackets, so this is a valid enclosure even
    # though it is not the tightest one that infinite precision would give).
    x_lo = (lo_m - hi_0) / h
    x_hi = (hi_0 - lo_p) / h

    return {
        't': str(t), 'h': str(h),
        'E0_at_t_minus_h': [str(lo_m), str(hi_m)], 'E0_at_t': [str(lo_0), str(hi_0)], 'E0_at_t_plus_h': [str(lo_p), str(hi_p)],
        'x_expectation_bracket': [str(x_lo), str(x_hi)],
        'x_expectation_preview_bracket': [float(x_lo), float(x_hi)],
        'first_order_estimate_t_over_6': float(t / 6),
        'timing_seconds': {str(k): v for k, v in times.items()},
        'total_seconds': sum(times.values()),
    }


# ---------------------------------------------------------------- (6) timing
def calibration_table():
    rows = []
    for D in (4, 6, 8):
        t0 = time.time()
        bs, G, K, MX, MY = tp.matrices(D, rho=Q(1))
        t1 = time.time()
        ni = tp.inertia(tp.shifted(K, G, Q(0)))
        t2 = time.time()
        rows.append({'D': D, 'dimension': len(bs), 'build_seconds': t1 - t0, 'one_inertia_call_seconds': t2 - t1})
    return rows


def self_test():
    t_start = time.time()

    facts = d8_free_facts()

    bs, G, K, MX, MY = tp.matrices(D_PRIMARY, rho=Q(1))
    dimension = len(bs)

    # --- derivative at zero, method A: assistant-3's regularized solve,
    # called at D=8 (imported, not reimplemented). ---
    d_solve_8, solve_detail_8, internals_8 = az2_calc.fg_derivative_regularized_solve(D_PRIMARY)
    bs8, G8, K8, MX8, K_reg8, v0_8, MXv0_8, v1_8 = internals_8
    arb_8 = az2_calc.arb_crosscheck_regularized_solve(bs8, G8, K_reg8, MXv0_8, v1_8, d_solve_8)
    # Same method at D=6, for a direct side-by-side with assistant-3's own
    # published value (should reproduce it exactly: the x-shell is an
    # EXACT eigenvector of K at every D>=1, so this is a D-stability check).
    d_solve_6, solve_detail_6, _ = az2_calc.fg_derivative_regularized_solve(ASSISTANT3_D)

    # --- derivative at zero, method B (brand new): exact central second
    # difference of E_0 alone, at two step sizes for a convergence check. ---
    sd_h1 = derivative_at_zero_via_second_difference(bs, G, K, MX, Q(1, 1000))
    sd_h2 = derivative_at_zero_via_second_difference(bs, G, K, MX, Q(1, 10000))

    # --- (3) Ritz brackets for <x>(tau_FG) at the three required points ---
    taus = [Q(1, 1000), Q(1, 100), Q(1, 10)]
    ritz_results = {}
    for tv in taus:
        h = tv / 1000
        ritz_results[str(tv)] = hellmann_feynman_x_bracket(bs, G, K, MX, tv, h)

    # --- (5) normalization dictionary, reusing assistant-3's own factor ---
    aw1 = json.loads((R32 / 'forward' / 'aw1' / 'output' / 'results.json').read_text())
    z3_coeff = Q(aw1['checks'][29]['first_order_mean_per_tau'])
    dictionary_factor = Q(24)
    converted_from_D8 = d_solve_8 / dictionary_factor
    matches_admitted = (converted_from_D8 == z3_coeff)

    # --- (6) timing / calibration ---
    calib = calibration_table()

    elapsed_total = time.time() - t_start

    passed = bool(
        facts['K_x_equals_3x'] and facts['free_gap_equals_3'] and facts['tail_lower_D8'] == '69'
        and d_solve_8 == Q(1, 6) and d_solve_6 == Q(1, 6) and d_solve_8 == d_solve_6
        and arb_8['arb_ball_contains_exact_fraction']
        and matches_admitted
        and all(Q(r['x_expectation_bracket'][0]) < Q(r['x_expectation_bracket'][1]) for r in ritz_results.values())
        and all(Q(r['x_expectation_bracket'][0]) > 0 for r in ritz_results.values())  # <x> should be positive for tau_FG>0
    )

    return {
        'tool': 'A4-3 finite_graph_rehearsal_d8',
        'labels': {'zero_research_loops': True, 'model_is_finite_graph': True, 'transfers_to_aq': False,
                   'toy_illustrative_matrix_elements': False, 'reused_by_import_only': ['two_plaquette.py (Round11)',
                   'az2_dictionary_calc.py (assistant-3)', 'flint_harness.py (assistant-1)']},
        'dimension_at_D8': dimension,
        'free_facts_confirmed_live_at_D8': facts,
        'derivative_at_zero': {
            'method_A_regularized_solve_D8': {'value': str(d_solve_8), 'detail': solve_detail_8, 'arb_crosscheck': arb_8},
            'method_A_regularized_solve_D6_assistant3_reproduction': {'value': str(d_solve_6), 'detail': solve_detail_6},
            'D6_and_D8_agree_exactly': d_solve_8 == d_solve_6,
            'method_B_exact_second_difference_h_1e-3': sd_h1,
            'method_B_exact_second_difference_h_1e-4': sd_h2,
            'method_B_converges_toward_1_6': [abs(sum(sd_h1['preview_bracket']) / 2 - 1 / 6),
                                               abs(sum(sd_h2['preview_bracket']) / 2 - 1 / 6)],
        },
        'ritz_values_x_expectation': ritz_results,
        'normalization_dictionary': {
            'tau_FG_equals_tau_over_24': True, 'derivative_at_zero_D8': str(d_solve_8),
            'converted': str(converted_from_D8), 'converted_preview': float(converted_from_D8),
            'z3_admitted_first_order_coefficient': str(z3_coeff), 'matches': matches_admitted,
        },
        'tail_residual_estimate': {
            'tail_lower_D8': facts['tail_lower_D8'],
            'note': "Heuristic only, not a certified bound: the exact closed-form derivative at "
                    "zero uses only the x-shell (K's eigenvalue-3 eigenspace), which is EXACT and "
                    "complete at every D>=1 -- so tail_lower(8)=69 has NO bearing on the derivative-"
                    "at-zero result (method A is D-independent by construction, confirmed above). "
                    "It DOES bound the truncation error of the finite-tau Ritz brackets in section "
                    "'ritz_values_x_expectation': the leading omitted correction to <x>_0(tau_FG) from "
                    "coupling into degree-9-and-above channels is second order in tau_FG and inversely "
                    "proportional to at least tail_lower(8)-3=66 in energy denominator, i.e. of order "
                    "tau_FG^2/66; at tau_FG=1/10 that is of order 1.5e-4, small compared with the "
                    "leading term ~1/60, and negligible at 1/100 and 1/1000.",
        },
        'timing_calibration_D4_D6_D8': calib,
        'elapsed_seconds_total': elapsed_total,
        'passed': passed,
    }


def main():
    result = self_test()
    print(json.dumps(result, indent=2, default=str))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
