#!/usr/bin/env python3
"""finite_graph_two_face_replay.py -- an independent D=10 replay of the AZ2
finite-graph two-face model on the Round11 two-plaquette graph.

Round32, sub-round 5, modern (Penrose/Feynman) lens, assistant-5.
Status: assistant/coder cross-check tool, per the sub-round-5 instruction
(panel-update-4 item 7, modern share). Counts ZERO research loops.
sympy, numpy/scipy, mpmath and python-flint (Arb) are labelled cross-check
libraries only; the Round11 `two_plaquette.py` solver module is reused BY
IMPORT (never reimplemented, never modified); `flint_harness.py`
(assistant-1, a shared tool, not a producer `check.py`) is reused for its
`to_fmpq`/`arb_crosscheck` helpers. Nothing here is imported by any
`check.py`, and nothing here decides admission. Every number this
workbench actually admits for AZ2 was already decided by exact
`fractions.Fraction` arithmetic in the frozen `research/round32/forward/
az2/check.py`; that file is NEVER imported here (per instruction), only
the ADMITTED `output/results.json` it produced is read, for comparison.

What the AZ2 gate admits (`research/round32/advisor/az2-gate.json`;
producer `research/round32/forward/az2/report.md` and
`output/results.json`; skeptic `research/round32/skeptic/az2.md` and
`az2-independent-derivation.md`)
-----------------------------------------------------------------------
The TWO-FACE model `H_FG = K - tau_FG (W_1 + W_2)` on the Round11
two-plaquette graph (`= Round11 H(alpha=1, lambda1=lambda2=tau_FG, rho=1)
- 2 tau_FG`, both faces coupled equally), certified at cutoffs D in
{6, 8} (dimensions 84 and 165):
  - `d<W_1>/dtau_FG` at `tau_FG=0` is exactly `1/6`, D-stable;
  - the second-order coefficient of `<W_1>` is exactly `0` and of `E_0`
    is exactly `-1/6`, D-stable;
  - `a_3` (third-order coefficient of `<W_1>`) is exactly `-187/33696`
    (two-face); the skeptic's independent derivation also gives the
    ONE-FACE variant `H(lambda1=tau, lambda2=0)` (second face
    uncoupled -- a DIFFERENT finite model, admitted only as the
    skeptic's side reading) `a_3 = -5/864`;
  - exact enclosures of `<W_1>` at `tau_FG` in `{+-1/1000,+-1/100,+-1/10}`
    at D=6 and D=8, e.g. D=8, tau_FG=+1/100: preview
    `~1.666661117076960224e-3`.

This file's own new work
-------------------------
1. **RS chain at D=10** (dimension 286, the "other" cutoff named by the
   task; NOT the contract's declared cutoff, `contracts/az2.json`
   `runtime_note` says "D=10 is not declared" -- this is an independent
   extra-cutoff replay, exactly as assistant-4's own planning notes for
   sub-round 5 recommended testing). Rayleigh-Schroedinger perturbation
   theory is carried out FROM SCRATCH in exact `Fraction` arithmetic,
   order by order, via the SAME regularized-solve deflation trick
   assistant-3's `az2_dictionary_calc.py` used at order 1 (not imported;
   re-derived and extended here to orders 2 and 3): `K` has a
   one-dimensional exact null space at the constant function `psi_0`;
   `K_reg = K + G psi_0 psi_0^T G^T` (since `psi_0^T G psi_0=1`) is then
   invertible, and solving `K_reg psi_n = RHS_n` for a source RHS_n whose
   zeroth (unweighted) component is zero automatically returns a `psi_n`
   satisfying the standard RS gauge `psi_0^T G psi_n = 0` for `n>=1` --
   proved directly below from `K`'s own zero row at index 0 (`K*1=0`
   exactly), not merely asserted.

   This is done SIMULTANEOUSLY for TWO independent models sharing the
   same `K_reg` (so `tp.solve_exact`'s multi-column back-substitution is
   used once per order, not once per model):
     - **two-face**: `M = MX + MY` (the admitted AZ2 model);
     - **one-face**: `M = MX` only (`H(lambda1=tau,lambda2=0)`, the
       skeptic's alternative model).
   The observable is always `<W_1> = <x>` (matrix `MX`), for both models.

   Reports, at D=10: `a_1` (derivative at zero) for both models, `E_2`
   and `a_2` (second-order coefficients of `E_0` and `<W_1>`) for both
   models, and `a_3` (third-order coefficient of `<W_1>`) for both
   models -- compared bit-for-bit against the admitted two-face values
   and the skeptic's one-face values, read LIVE from
   `forward/az2/output/results.json` (never retyped) and the skeptic's
   `az2-independent-derivation.md` text (quoted, not parsed).

2. **Floating/Arb PREVIEWS (not certified brackets) of `<W_1>` at
   `tau_FG = +-1/100`, D=10.** A `scipy.linalg.eigh` generalized
   floating eigensolve gives a Ritz vector; a python-flint (Arb,
   256-bit) one-step inverse-iteration refinement
   `(H_arb - s G_arb) y = G_arb v_float` (the same style of Arb
   refinement `az2_dictionary_calc.arb_crosscheck_regularized_solve`
   and this sub-round's own `finite_graph_rehearsal_d8.py` already use)
   gives an independent high-precision Arb ball for `<W_1>_D=10(tau_FG)`.
   **Neither is `exact_bracket`/`inertia`-based, and neither uses
   `tail_lower`.** This is deliberate: the skeptic's retained correction
   of the modern update-4/assistant-4 claims
   (`research/round32/skeptic/az2.md` line 219,
   `az2-independent-derivation.md` line 179+217) is that
   `two_plaquette.exact_bracket` certifies only the TRUNCATED matrix's
   Ritz value, not the full-graph value, and does so WITHOUT using
   `tail_lower` at all -- so calling such a bracket "certified" for the
   full graph is false. Both previews here are labelled accordingly:
   `preview_only:true`, `exact_bracket_used:false`, `tail_lower_used:
   false`, `certifies_full_graph:false`, `certifies_truncated_D10_matrix
   _only: true` (and even that last claim is only approximate, since the
   Arb step is a single inverse-iteration refinement of a floating
   guess, not an isolation certificate). They are compared only as
   numbers against the gate's own exact enclosure and preview.

3. **One measured `inertia` call at D=10** (dimension 286), for the
   AZ2/AZ-series runtime-budgeting question assistant-4's own planning
   notes for sub-round 5 raised: `two_plaquette.inertia(shifted(K,G,0))`,
   timed once, reported honestly (no `exact_bracket` loop is run here;
   seeing that a single `inertia` call alone already costs several tens
   of seconds at D=10 is exactly the data point needed to answer the
   "is D=10 practical for `exact_bracket`-style certification" question
   without spending the further several-times-that cost of actually
   running one).

D=7 fallback note
------------------
Not needed: every D=10 computation below (matrix build, all three
RS-order regularized solves for both models together, the two
floating/Arb Wilson previews and the one measured `inertia` call)
completed well within a few minutes total on this container (see
`elapsed_seconds` in the self-test output). D=7 was not attempted.
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


flint_harness = _load('flint_harness_a5', R32 / 'experts' / 'modern' / 'assistant-1' / 'flint_harness.py')

D_PRIMARY = 10
MODEL_NAMES = ('two_face', 'one_face')


# ---------------------------------------------------------- linear algebra
def matvec(A, v, n):
    return [sum(A[i][j] * v[j] for j in range(n)) for i in range(n)]


def dot(u, v, n):
    return sum(u[i] * v[i] for i in range(n))


def build(D):
    bs, G, K, MX, MY = tp.matrices(D, rho=Q(1))
    n = len(bs)
    assert bs[0] == (0, 0, 0), 'basis index 0 must be the constant function'
    # --- K's own zero row at index 0, confirmed LIVE (not merely cited):
    # this is what makes the regularized-solve gauge trick below correct
    # at every order, not just order 1. K*1=0 exactly (kinetic(1)=0), and
    # K is self-adjoint w.r.t. the moment inner product, so
    # K[0][j] = <1, K p_j> = <K*1, p_j> = 0 for every j.
    row0_all_zero = all(K[0][j] == 0 for j in range(n))
    models = {
        'two_face': [[MX[i][j] + MY[i][j] for j in range(n)] for i in range(n)],
        'one_face': MX,
    }
    return bs, G, K, MX, MY, n, models, row0_all_zero


def regularized_kernel(G, K, n):
    v0 = [Q(1) if i == 0 else Q(0) for i in range(n)]
    Gv0 = matvec(G, v0, n)
    v0Gv0 = dot(v0, Gv0, n)
    assert v0Gv0 == 1, 'constant function should already be G-normalized'
    K_reg = [[K[i][j] + Gv0[i] * Gv0[j] / v0Gv0 for j in range(n)] for i in range(n)]
    return v0, Gv0, v0Gv0, K_reg


# --------------------------------------------------------------- RS chain
def rs_chain(D):
    """Exact Rayleigh-Schroedinger perturbation theory, orders 0-3, for
    BOTH models (two_face: M=MX+MY; one_face: M=MX) simultaneously,
    sharing one `K_reg` and one `tp.solve_exact` call per order (packing
    both models' right-hand sides as columns). H(tau)=K-tau*M, so V=-M;
    E_0=0, psi_0=e_0 (the constant basis vector). Standard intermediate
    normalization gauge: psi_0^T G psi_n = 0 for n>=1, proved to hold
    automatically here (not merely assumed) because K's row 0 is
    identically zero (see `build()`): for any RHS with RHS[0]=0,
    K_reg psi = RHS forces (K psi)[0] + (G psi_0)[0]*(psi_0^T G psi) = 0,
    i.e. 0 + 1*(psi_0^T G psi) = 0, i.e. psi_0^T G psi = 0, unconditionally.
    """
    bs, G, K, MX, MY, n, models, row0_all_zero = build(D)
    v0, Gv0, v0Gv0, K_reg = regularized_kernel(G, K, n)

    psi = {name: {0: v0} for name in MODEL_NAMES}
    E = {name: {0: Q(0)} for name in MODEL_NAMES}
    timings = {}

    # ---- order 1: K psi_1 = M psi_0  (E_1=0 automatically: (M psi_0)[0]
    # = M[0][0] = moment(x[+y]) = 0 by Haar odd-moment vanishing, checked
    # live below)
    t0 = time.time()
    rhs_cols = [matvec(models[name], v0, n) for name in MODEL_NAMES]
    e1_source_zero = {name: (rhs_cols[i][0] == 0) for i, name in enumerate(MODEL_NAMES)}
    rhs_mat = [[rhs_cols[k][i] for k in range(len(MODEL_NAMES))] for i in range(n)]
    sol = tp.solve_exact(K_reg, rhs_mat)
    for k, name in enumerate(MODEL_NAMES):
        psi[name][1] = [sol[i][k] for i in range(n)]
        E[name][1] = Q(0)
    timings['order1_solve_seconds'] = time.time() - t0

    a1 = {name: 2 * dot(matvec(MX, psi[name][1], n), v0, n) for name in MODEL_NAMES}

    # ---- order 2: K psi_2 = M psi_1 + E_2 G psi_0, E_2 = -(M psi_1)[0]
    t0 = time.time()
    rhs_cols = []
    for name in MODEL_NAMES:
        Mpsi1 = matvec(models[name], psi[name][1], n)
        E2 = -Mpsi1[0]
        E[name][2] = E2
        rhs_cols.append([Mpsi1[i] + E2 * Gv0[i] for i in range(n)])
    rhs_mat = [[rhs_cols[k][i] for k in range(len(MODEL_NAMES))] for i in range(n)]
    sol = tp.solve_exact(K_reg, rhs_mat)
    for k, name in enumerate(MODEL_NAMES):
        psi[name][2] = [sol[i][k] for i in range(n)]
    timings['order2_solve_seconds'] = time.time() - t0

    a2 = {name: 2 * dot(matvec(MX, psi[name][2], n), v0, n) + dot(matvec(MX, psi[name][1], n), psi[name][1], n)
          for name in MODEL_NAMES}

    # ---- order 3: K psi_3 = M psi_2 + E_2 G psi_1 + E_3 G psi_0,
    # E_3 = -(M psi_2 + E_2 G psi_1)[0]
    t0 = time.time()
    rhs_cols = []
    for name in MODEL_NAMES:
        Mpsi2 = matvec(models[name], psi[name][2], n)
        Gpsi1 = matvec(G, psi[name][1], n)
        E2 = E[name][2]
        term = [Mpsi2[i] + E2 * Gpsi1[i] for i in range(n)]
        E3 = -term[0]
        E[name][3] = E3
        rhs_cols.append([term[i] + E3 * Gv0[i] for i in range(n)])
    rhs_mat = [[rhs_cols[k][i] for k in range(len(MODEL_NAMES))] for i in range(n)]
    sol = tp.solve_exact(K_reg, rhs_mat)
    for k, name in enumerate(MODEL_NAMES):
        psi[name][3] = [sol[i][k] for i in range(n)]
    timings['order3_solve_seconds'] = time.time() - t0

    a3 = {}
    for name in MODEL_NAMES:
        c2 = dot(matvec(G, psi[name][1], n), psi[name][1], n)  # D(tau)'s tau^2 coefficient
        a3[name] = (2 * dot(matvec(MX, psi[name][3], n), v0, n)
                    + 2 * dot(matvec(MX, psi[name][2], n), psi[name][1], n)
                    - c2 * a1[name])

    # ---- gauge check, live (not assumed): psi_0^T G psi_n == 0 for n=1,2,3
    gauge_ok = {name: all(dot(v0, matvec(G, psi[name][k], n), n) == 0 for k in (1, 2, 3)) for name in MODEL_NAMES}

    return {
        'D': D, 'dimension': n,
        'row0_of_K_all_zero_live': row0_all_zero,
        'e1_source_zero_by_haar_odd_moment': e1_source_zero,
        'a1_derivative_at_zero': {name: str(a1[name]) for name in MODEL_NAMES},
        'E2_second_order_energy': {name: str(E[name][2]) for name in MODEL_NAMES},
        'a2_second_order_W1': {name: str(a2[name]) for name in MODEL_NAMES},
        'E3_third_order_energy': {name: str(E[name][3]) for name in MODEL_NAMES},
        'a3_third_order_W1': {name: str(a3[name]) for name in MODEL_NAMES},
        'gauge_orthogonality_holds_live': gauge_ok,
        'timings': timings,
        '_raw': {'a1': a1, 'a2': a2, 'a3': a3, 'E2': {n_: E[n_][2] for n_ in MODEL_NAMES},
                 'E3': {n_: E[n_][3] for n_ in MODEL_NAMES}, 'G': G, 'MX': MX, 'MY': MY, 'K': K, 'n': n,
                 'models': models},
    }


# --------------------------------------------------- floating/Arb previews
def wilson_preview(D, tau_val, prec=256):
    """PREVIEW ONLY (no exact_bracket, no inertia, no tail_lower): scipy
    generalized floating eigh for the D-truncated ground Ritz vector,
    then ONE step of Arb (python-flint) 256-bit inverse iteration
    (H_arb - s G_arb) y = G_arb v_float, giving a high-precision but
    UNCERTIFIED ball for <W_1>_D(tau_val) = (y^T MX y)/(y^T G y).
    Labelled explicitly per the skeptic's retained correction of the
    modern update-4/assistant-4 claims: this brackets (previews) the
    TRUNCATED D-dimensional matrix's Ritz value only, not the full-graph
    value the AZ2 gate certifies, and it does not use tail_lower at all."""
    bs, G, K, MX, MY, n, models, _ = build(D)
    M = models['two_face']
    H = [[K[i][j] - tau_val * M[i][j] for j in range(n)] for i in range(n)]
    Hf, Gf, MXf = tp.floating(H), tp.floating(G), tp.floating(MX)

    t0 = time.time()
    vals, vecs = eigh(Hf, Gf)
    t_eigh = time.time() - t0
    v_float = vecs[:, 0]
    E_float = float(vals[0])
    w1_float = float((v_float @ MXf @ v_float) / (v_float @ Gf @ v_float))

    flint.ctx.prec = prec
    H_arb = flint.arb_mat(n, n, [flint.arb(flint_harness.to_fmpq(H[i][j])) for i in range(n) for j in range(n)])
    G_arb = flint.arb_mat(n, n, [flint.arb(flint_harness.to_fmpq(G[i][j])) for i in range(n) for j in range(n)])
    MX_arb = flint.arb_mat(n, n, [flint.arb(flint_harness.to_fmpq(MX[i][j])) for i in range(n) for j in range(n)])
    v_arb = flint.arb_mat(n, 1, [flint.arb(float(x)) for x in v_float])
    s_arb = flint.arb(E_float)
    t0 = time.time()
    A = H_arb - s_arb * G_arb
    y = A.solve(G_arb * v_arb)
    t_arb = time.time() - t0
    num = (y.transpose() * MX_arb * y)[0, 0]
    den = (y.transpose() * G_arb * y)[0, 0]
    w1_arb = num / den
    lo, hi = flint_harness.arb_crosscheck.rational_bounds_arb(w1_arb)

    return {
        'D': D, 'dimension': n, 'tau_FG': str(tau_val), 'tau_FG_preview': float(tau_val),
        'preview_only': True, 'exact_bracket_used': False, 'inertia_used': False, 'tail_lower_used': False,
        'certifies_full_graph': False,
        'caveat': "PREVIEW ONLY (scipy floating eigh + one Arb inverse-iteration refinement step at "
                  f"{prec} bits). Not an exact_bracket/inertia-based enclosure, and tail_lower is not used. "
                  "Per the skeptic's retained correction of the modern update-4/assistant-4 claims "
                  "(research/round32/skeptic/az2.md and az2-independent-derivation.md): an exact_bracket-style "
                  "bracket, if one were built here instead, would enclose only the D-truncated matrix's own "
                  "Ritz value, not the AZ2 gate's certified full-graph value, and it would not use tail_lower "
                  "either -- this preview makes no stronger claim than that in the first place.",
        'scipy_eigh_seconds': t_eigh, 'floating_E0': E_float, 'floating_W1_preview': w1_float,
        'arb_refine_seconds': t_arb, 'arb_W1_ball_mid': float(w1_arb.mid()), 'arb_W1_ball_rad': float(w1_arb.rad()),
        'arb_W1_bracket': [str(lo), str(hi)],
    }


def one_inertia_timing_probe(D):
    """A single measured tp.inertia() call at D, for the AZ2/AZ-series
    runtime-budgeting question (not an exact_bracket loop: exact_bracket
    calls inertia repeatedly per point -- assistant-4's own D=8 data
    showed roughly 3-4 inertia calls per exact_bracket -- so this single
    call alone already answers "is exact_bracket practical at D=10"
    without paying that multiple)."""
    bs, G, K, MX, MY, n, models, _ = build(D)
    t0 = time.time()
    ni = tp.inertia(tp.shifted(K, G, Q(0)))
    elapsed = time.time() - t0
    return {'D': D, 'dimension': n, 'inertia_result_neg_zero_pos': list(ni), 'elapsed_seconds': elapsed,
            'note': 'A single inertia() call, not a full exact_bracket refinement loop (which calls inertia '
                    'repeatedly). Reported to budget runtime for any future exact_bracket-based work at D=10, '
                    'not used itself as a bracket.'}


# ------------------------------------------------------------- comparison
def read_admitted_az2():
    result_path = R32 / 'forward' / 'az2' / 'output' / 'results.json'
    az2 = json.loads(result_path.read_text())
    return az2


def self_test():
    t_start = time.time()

    chain = rs_chain(D_PRIMARY)

    previews = {}
    for sign, tau in (('plus', Q(1, 100)), ('minus', Q(-1, 100))):
        previews[sign] = wilson_preview(D_PRIMARY, tau)

    inertia_probe = one_inertia_timing_probe(D_PRIMARY)

    az2 = read_admitted_az2()
    admitted_a1 = Q(az2['rs_coefficients']['W_1'][1])
    admitted_a2_two = Q(az2['rs_coefficients']['W_1'][2])
    admitted_a3_two = Q(az2['rs_coefficients']['W_1'][3])
    admitted_E2_two = Q(az2['rs_coefficients']['E_0'][2])
    admitted_E3_two = Q(az2['rs_coefficients']['E_0'][3])
    # Skeptic's independently-derived one-face side values (quoted verbatim
    # from research/round32/skeptic/az2.md and az2-independent-derivation.md,
    # never parsed out of a file this script imports):
    admitted_a1_one = Q(1, 6)
    admitted_a3_one = Q(-5, 864)
    admitted_E2_one = Q(-1, 12)
    wilson_enclosures = az2['headline']['wilson_enclosures']
    admitted_wilson_D8_plus = [Q(wilson_enclosures['D8_tau+1/100'][0]), Q(wilson_enclosures['D8_tau+1/100'][1])]
    admitted_wilson_D8_minus = [Q(wilson_enclosures['D8_tau-1/100'][0]), Q(wilson_enclosures['D8_tau-1/100'][1])]

    my_a1 = {name: Q(chain['a1_derivative_at_zero'][name]) for name in MODEL_NAMES}
    my_a2 = {name: Q(chain['a2_second_order_W1'][name]) for name in MODEL_NAMES}
    my_a3 = {name: Q(chain['a3_third_order_W1'][name]) for name in MODEL_NAMES}
    my_E2 = {name: Q(chain['E2_second_order_energy'][name]) for name in MODEL_NAMES}
    my_E3 = {name: Q(chain['E3_third_order_energy'][name]) for name in MODEL_NAMES}

    comparison = {
        'a1_two_face_matches_1_6': my_a1['two_face'] == admitted_a1 == Q(1, 6),
        'a1_one_face_matches_1_6': my_a1['one_face'] == admitted_a1_one == Q(1, 6),
        'a2_two_face_matches_0': my_a2['two_face'] == admitted_a2_two == 0,
        'a2_one_face_matches_0': my_a2['one_face'] == 0,
        'a3_two_face_matches_admitted': my_a3['two_face'] == admitted_a3_two == Q(-187, 33696),
        'a3_one_face_matches_skeptic': my_a3['one_face'] == admitted_a3_one == Q(-5, 864),
        'E2_two_face_matches_admitted': my_E2['two_face'] == admitted_E2_two == Q(-1, 6),
        'E2_one_face_matches_skeptic': my_E2['one_face'] == admitted_E2_one == Q(-1, 12),
        'E3_two_face_matches_admitted_zero': my_E3['two_face'] == admitted_E3_two == 0,
        'E3_one_face_zero': my_E3['one_face'] == 0,
    }
    all_exact_match = all(comparison.values())

    wilson_preview_plus_inside_gate_enclosure = (
        admitted_wilson_D8_plus[0] <= Q(previews['plus']['arb_W1_bracket'][0]) and
        Q(previews['plus']['arb_W1_bracket'][1]) <= admitted_wilson_D8_plus[1]
    )
    wilson_preview_minus_inside_gate_enclosure = (
        admitted_wilson_D8_minus[0] <= Q(previews['minus']['arb_W1_bracket'][0]) and
        Q(previews['minus']['arb_W1_bracket'][1]) <= admitted_wilson_D8_minus[1]
    )

    elapsed_total = time.time() - t_start

    passed = bool(
        chain['row0_of_K_all_zero_live']
        and all(chain['e1_source_zero_by_haar_odd_moment'].values())
        and all(chain['gauge_orthogonality_holds_live'].values())
        and all_exact_match
        and wilson_preview_plus_inside_gate_enclosure
        and wilson_preview_minus_inside_gate_enclosure
        and previews['plus']['floating_W1_preview'] > 0
        and previews['minus']['floating_W1_preview'] < 0
    )

    return {
        'tool': 'A5-1 finite_graph_two_face_replay',
        'labels': {
            'zero_research_loops': True, 'model_is_finite_graph': True, 'transfers_to_aq': False,
            'fg_coefficients_fitted': False, 'toy_illustrative_matrix_elements': False,
            'D7_fallback_needed': False, 'D7_fallback_reason': 'D=10 completed well within budget; see timings below',
            'reused_by_import_only': ['two_plaquette.py (Round11)', 'flint_harness.py (assistant-1, shared tool)'],
        },
        'rs_chain_D10': {k: v for k, v in chain.items() if k != '_raw'},
        'wilson_previews_tau_pm_1_100_D10': previews,
        'inertia_timing_probe_D10': inertia_probe,
        'comparison_with_admitted_az2_and_skeptic_one_face': {
            'admitted_a1_two_face': str(admitted_a1), 'admitted_a1_one_face_skeptic': str(admitted_a1_one),
            'admitted_a3_two_face': str(admitted_a3_two), 'admitted_a3_one_face_skeptic': str(admitted_a3_one),
            'admitted_E2_two_face': str(admitted_E2_two), 'admitted_E2_one_face_skeptic': str(admitted_E2_one),
            'my_a1': {k: str(v) for k, v in my_a1.items()}, 'my_a3': {k: str(v) for k, v in my_a3.items()},
            'my_E2': {k: str(v) for k, v in my_E2.items()},
            'checks': comparison, 'all_exact_match': all_exact_match,
        },
        'wilson_preview_inside_gate_D8_enclosure': {
            'tau_FG=+1/100': wilson_preview_plus_inside_gate_enclosure,
            'tau_FG=-1/100': wilson_preview_minus_inside_gate_enclosure,
            'gate_D8_enclosure_plus_1_100': [str(admitted_wilson_D8_plus[0]), str(admitted_wilson_D8_plus[1])],
            'gate_D8_enclosure_minus_1_100': [str(admitted_wilson_D8_minus[0]), str(admitted_wilson_D8_minus[1])],
            'note': 'Containment is checked against the gate\'s D=8 FULL-GRAPH certified enclosure as a sanity '
                    'comparison only; this preview is itself a D=10 TRUNCATED-matrix preview, not a certificate, '
                    'so containment here is informative, not a proof that it must hold.',
        },
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
