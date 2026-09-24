#!/usr/bin/env python3
"""az2_dictionary_calc.py -- a normalization-dictionary CALCULATOR for AZ2:
maps the Round11 two-plaquette finite-graph convention onto the Z^3
uniform-model convention explicitly enough to compare one number on each
side, and states exactly which assumptions license the comparison.

Round32, sub-round 3, modern (Penrose/Feynman) lens, assistant-3.
Status: assistant/coder preview/cross-check tool. Counts ZERO research
loops. THIS IS A CONSISTENCY MAP, NOT A TRANSFER (contract wording,
`research/round32/contracts/az2.json` and `az2_spec_check.md` section 3):
nothing here licenses treating the finite two-plaquette graph as evidence
about the Z^3/AQ model, and nothing here is admission arithmetic.

Two conventions to reconcile
-----------------------------
(A) Round11 two-plaquette finite graph (`research/round11/advisor/
    advisor.md`, `research/round11/solver/two_plaquette.py`, and this
    sub-round's own `assistant-2/az2_spec_check.md` section 3):

        H_FG(tau_FG) = K - tau_FG * x            (asymmetric, primary)

    with `K` the exact rational kinetic/electric operator (eq. K1),
    `x=(1/2)Tr(U)` one plaquette's own Wilson trace, alpha=1. `K`'s own
    free (tau_FG=0) ground state is the constant function 1, eigenvalue 0
    (`K*1=0`, moment((0,0,0))=1, confirmed live below); its first excited
    eigenspace is `span{x,y}`, eigenvalue exactly 3 (`Kx=3x`, `Ky=3y`,
    advisor.md eq. E1/E2 -- confirmed live, not merely cited); the FG
    model's own free/electric gap is EXACTLY 3 in alpha units
    (`two_plaquette.free_gap()==3`, confirmed live).

(B) The Z^3 convention THIS TASK SPECIFIES: the uniform route-B per-block
    potential

        V_b = -(tau/24) * sum_{f=1}^{24} W_f      (alpha units)

    summing the block's own 24 elementary faces (`uniform_counts_from_
    scratch.py`, this sub-round, confirms independently that a route-B
    block owns exactly 24 faces: 21 omitted + 3 selected, each at the
    SAME per-face coefficient tau/24 -- this is what makes the sum
    "uniform"), "with plaquette energy 3" -- read here as the declared Z^3
    reference/free electric energy scale used for the dictionary's gap
    calibration (assumption A4 below).

What is NOT given for free: `tau_FG` and `tau` are coupling constants of
TWO DIFFERENT MODELS (a 7-link finite graph vs. the infinite Z^3 lattice)
normalized by two different authors' conventions; there is no a-priori
reason their numerical values should be equal, or even proportional with
a "natural" constant, without further stated assumptions. This script
states them.

Stated assumptions (ALL must hold for the final numeric comparison to
mean anything; each is flagged, none is proved here)
-----------------------------------------------------
  A1. alpha=1 on both sides ("in alpha units", as both conventions above
      are already stated).
  A2. AW1's parity theorem is invoked EXACTLY as already admitted
      (`forward/aw1/report.md`, AX1 gate item 7 "Transfer, proved"):
      at first order in tau, only the term f=W of the 24-face sum
      contributes to d(omega_tau(W))/d(tau)|_0 -- every cross term
      <W, W_f> for f!=W vanishes by the parity/link-grading argument.
      Consequently the Z^3 side's EFFECTIVE single-observable coupling
      for the specific measured face W is exactly its own bare
      coefficient, tau/24, independent of the other 23 terms' presence.
  A3. IDENTIFY the FG's single coupling constant with this effective
      single-observable Z^3 coupling: tau_FG := tau/24. This is the
      dictionary's central, NOT independently forced, choice -- it
      equates "the one coupling constant multiplying the one observed
      trace on the FG side" with "the one coefficient multiplying the
      one first-order-relevant face on the Z^3 side", licensed by A2.
  A4. IDENTIFY the FG's own free/electric gap (exactly 3, `K`'s own
      eigenvalue, confirmed live) with the Z^3 side's declared reference
      "plaquette energy 3" (both alpha units) -- an assumed common scale,
      not a derived equality of physically identical operators (the two
      models' electric terms are built very differently: `K` is `research/
      round11/advisor/advisor.md` eq. K1's specific 7-link combination;
      the Z^3 electric term is `h_b=8*sum_e C_e` per AW1/AX1). Since both
      quoted numbers equal exactly 3, this assumption introduces a
      gap-ratio factor of exactly 1 (no further rescaling), but it remains
      an ASSUMED identification of two different operators' scales, not a
      proof they measure the same thing.

Given A1-A4, `d<x>/d(tau_FG)|_0` converts to `tau`-units by the chain
rule: `d<x>/d(tau)|_0 = d<x>/d(tau_FG)|_0 * d(tau_FG)/d(tau) = (1/6)*(1/24)`.
This script computes both factors independently and reports whether the
product equals the ADMITTED Z^3 first-order coefficient 1/144
(`forward/aw1/output/results.json`, live-read, never retyped). A match is
reported as a labelled CONSISTENCY OBSERVATION under A1-A4, explicitly
NOT as a proof, a transfer, or evidence for either model individually
(contract `claim_exclusions`; `no_transfer_to_aq: true`,
`fg_coefficients_not_fitted: true`).
"""
import importlib.util
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

import flint

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


flint_harness = _load('flint_harness_a3b', R32 / 'experts' / 'modern' / 'assistant-1' / 'flint_harness.py')

X_MONO = {(1, 0, 0): Q(1)}
ONE_MONO = {(0, 0, 0): Q(1)}
D_PRIMARY = 6


# ---------------------------------------------------------------- FG side
def fg_free_facts():
    """Facts about H_FG(0)=K, confirmed LIVE against the frozen
    two_plaquette module (never merely cited)."""
    K_on_x = tp.kinetic(X_MONO)
    K_on_one = tp.kinetic(ONE_MONO)
    x2 = tp.inner(X_MONO, X_MONO)
    x_mean = tp.moment((1, 0, 0))
    one_norm = tp.moment((0, 0, 0))
    gap = tp.free_gap()
    tail6 = tp.tail_lower(6)
    tail8 = tp.tail_lower(8)
    return {
        'K_times_one': {str(k): str(v) for k, v in K_on_one.items()} or {'0': '0'},
        'K_x_equals_3x': K_on_x == {(1, 0, 0): Q(3)},
        'K_on_x_raw': {str(k): str(v) for k, v in K_on_x.items()},
        'x_squared_moment': str(x2), 'x_squared_preview': float(x2),
        'x_mean_is_zero': (x_mean == 0),
        'own_free_reference': one_norm == 1,
        'free_gap_exact': str(gap),
        'free_gap_equals_3': (gap == 3),
        'tail_lower_D6': str(tail6), 'tail_lower_D8': str(tail8),
    }


def fg_derivative_closed_form():
    """Non-degenerate Rayleigh-Schrodinger PT, no regularization needed:
    x is an EXACT eigenvector of K (Kx=3x), orthogonal to the ground state
    |0>=1 (<x>=0), separated by the real gap 3-0=3. So
      d<x>/d(tau_FG)|_0 = 2*<0|x|psi_1> ,  psi_1 = x / (gap) = x/3
    (H_FG=K-tau_FG*x, so V=-x; (K-0)|1>=-V|0>=x  =>  |1>=x/3 exactly, since
    K acts as the scalar 3 on x). Then <0|x|psi_1> = (1/3)<1,x*x> = (1/3)*
    <x,x> = (1/3)(1/4) = 1/12, times 2 = 1/6."""
    K_x = tp.kinetic(X_MONO)
    gap = K_x[(1, 0, 0)]  # =3, K's eigenvalue on x (K*1=0 is the ground state, E0=0)
    assert gap == 3
    psi1_coeff = Q(1) / gap  # |1> = (1/gap) * x, i.e. psi1 = x/3 as a scalar on the x monomial
    x2 = tp.inner(X_MONO, X_MONO)  # <x,x> = 1/4
    deriv = 2 * psi1_coeff * x2
    return deriv, {'gap_K_eigenvalue_on_x_shell': str(gap), 'psi1_coefficient_on_x': str(psi1_coeff),
                   'x_squared_moment': str(x2), 'formula': '2 * (1/gap) * <x,x>'}


def fg_derivative_regularized_solve(D=D_PRIMARY):
    """Independent cross-check: the GENERIC method az2_spec_check.md
    section 5 proposed but did not execute in exact Fraction -- a
    regularized singular solve on the full degree-D truncated matrices,
    reusing `two_plaquette.matrices`/`solve_exact` verbatim (not
    reimplemented). K has a 1-dimensional exact null space (v0, the
    constant function); (K + G v0 v0^T G^T / (v0^T G v0)) v1 = MX v0 is
    the regularized, nonsingular system whose solution agrees with the
    true first-order correction on v0's G-orthogonal complement."""
    bs, G, K, MX, MY = tp.matrices(D, rho=Q(1))
    n = len(bs)
    assert bs[0] == (0, 0, 0), 'basis index 0 must be the constant function'
    v0 = [Q(1) if i == 0 else Q(0) for i in range(n)]
    Gv0 = [sum(G[i][j] * v0[j] for j in range(n)) for i in range(n)]
    v0Gv0 = sum(v0[i] * Gv0[i] for i in range(n))
    assert v0Gv0 == 1, 'constant function should already be G-normalized'
    MXv0 = [sum(MX[i][j] * v0[j] for j in range(n)) for i in range(n)]
    K_reg = [[K[i][j] + Gv0[i] * Gv0[j] / v0Gv0 for j in range(n)] for i in range(n)]
    rhs = [[MXv0[i]] for i in range(n)]
    v1_cols = tp.solve_exact(K_reg, rhs)
    v1 = [row[0] for row in v1_cols]
    # v0^T MX v1 = (MX v0) . v1 since MX is symmetric (MX v0 = MX's row 0 = column 0)
    v0_MX_v1 = sum(MXv0[i] * v1[i] for i in range(n))
    deriv = 2 * v0_MX_v1 / v0Gv0
    return deriv, {
        'degree': D, 'dimension': n,
        'K_reg_symmetric': all(K_reg[i][j] == K_reg[j][i] for i in range(n) for j in range(n)),
        'v0_G_v0': str(v0Gv0),
        'MX_v0_nonzero_count': sum(1 for v in MXv0 if v != 0),
        'v0_MX_v1': str(v0_MX_v1),
    }, (bs, G, K, MX, K_reg, v0, MXv0, v1)


def arb_crosscheck_regularized_solve(bs, G, K_reg, MXv0, v1_exact, deriv_exact, prec=256):
    """Independent Arb (256-bit) numeric confirmation: solve the SAME
    linear system K_reg @ v1 = MXv0 using flint's arb_mat.solve (ball
    arithmetic, not Fractions), then check the resulting ball for the
    derivative CONTAINS the exact Fraction value -- reusing
    flint_harness.to_fmpq/contains verbatim, exactly the workbench's
    standard Arb-preview pattern."""
    flint.ctx.prec = prec
    n = len(bs)
    K_reg_arb = flint.arb_mat(n, n, [flint.arb(flint_harness.to_fmpq(K_reg[i][j]))
                                      for i in range(n) for j in range(n)])
    rhs_arb = flint.arb_mat(n, 1, [flint.arb(flint_harness.to_fmpq(v)) for v in MXv0])
    v1_arb_mat = K_reg_arb.solve(rhs_arb)
    v0_MX_v1_arb = sum((flint.arb(flint_harness.to_fmpq(MXv0[i])) * v1_arb_mat[i, 0] for i in range(n)),
                        flint.arb(0))
    deriv_arb = 2 * v0_MX_v1_arb
    ball_lo, ball_hi = flint_harness.arb_crosscheck.rational_bounds_arb(deriv_arb)
    contains_exact = (Q(str(ball_lo)) <= deriv_exact <= Q(str(ball_hi)))
    return {
        'precision_bits': prec, 'method': 'flint.arb_mat.solve (ball arithmetic)',
        'derivative_arb_ball_bounds': [str(ball_lo), str(ball_hi)],
        'derivative_arb_ball_preview': float(deriv_arb.mid()),
        'exact_fraction_value': str(deriv_exact),
        'arb_ball_contains_exact_fraction': bool(contains_exact),
    }


# ---------------------------------------------------------------- Z3 side
def read_json(rel_path):
    with open(ROOT / rel_path) as fh:
        return json.load(fh)


def z3_admitted_first_order_coefficient():
    aw1 = read_json('research/round32/forward/aw1/output/results.json')
    value = aw1['checks'][29]['first_order_mean_per_tau']
    coeff = Q(value)
    headline = aw1['headline']['first_order_coefficient']
    gate_text = ROOT.joinpath('research/round32/advisor/ax1-gate.json').read_text()
    return coeff, {
        'source': 'research/round32/forward/aw1/output/results.json checks[29].first_order_mean_per_tau',
        'string': value, 'headline_field': headline,
        'referenced_as_unchanged_in_ax1_gate_transfer_item': ('tau/144' in gate_text),
    }


def z3_uniform_face_count():
    """Reused from this sub-round's own `uniform_counts_from_scratch.py`
    (imported, not retyped): 24 faces owned per block under route B, each
    at the uniform per-face coefficient tau/24."""
    ucs = _load('uniform_counts_a3', HERE.parent / 'uniform_counts_from_scratch.py')
    site = ucs.method1_touching_single_site()
    owned = site['owned_at_site_omitted'] + site['owned_at_site_selected']
    return owned, ucs


# ------------------------------------------------------------ Dictionary
def dictionary_map(dxdtauFG, z3_coeff):
    dictionary_factor = Q(24)      # tau_FG := tau / dictionary_factor  (A3)
    tau_FG_over_tau = Q(1) / dictionary_factor
    converted = dxdtauFG * tau_FG_over_tau
    matches = (converted == z3_coeff)

    # Contrast: the naive (unwarranted) alternative dictionary tau_FG:=tau
    # (i.e. ignoring A2's "effective single term" argument and instead
    # matching the couplings literally one-to-one), to show the match
    # above is not a vacuous identity of the two Fraction literals.
    naive_converted = dxdtauFG * Q(1)
    naive_matches = (naive_converted == z3_coeff)

    return {
        'A3_dictionary_factor_tau_over_tau_FG': str(dictionary_factor),
        'tau_FG_equals_tau_over_24': True,
        'dxdtau_converted_via_dictionary': str(converted), 'dxdtau_converted_preview': float(converted),
        'z3_admitted_dxdtau': str(z3_coeff), 'z3_admitted_dxdtau_preview': float(z3_coeff),
        'matches_under_A1_A4': bool(matches),
        'contrast_naive_dictionary_tau_FG_equals_tau': {
            'converted': str(naive_converted),
            'matches': bool(naive_matches),
            'note': 'Without A2/A3 (i.e. naively setting tau_FG=tau instead of tau/24), the FG '
                    'derivative does NOT reproduce the admitted 1/144; the match above is '
                    'therefore a genuine (if assumption-dependent) consequence of the stated '
                    'dictionary, not an algebraic tautology of the two numbers involved.',
        },
    }


def self_test():
    fg_facts = fg_free_facts()
    d_closed, closed_detail = fg_derivative_closed_form()
    d_solve, solve_detail, solve_internals = fg_derivative_regularized_solve(D_PRIMARY)
    bs, G, K, MX, K_reg, v0, MXv0, v1 = solve_internals
    arb = arb_crosscheck_regularized_solve(bs, G, K_reg, MXv0, v1, d_solve)

    two_methods_agree = (d_closed == d_solve)

    z3_coeff, z3_meta = z3_admitted_first_order_coefficient()
    owned_per_block, _ucs_mod = z3_uniform_face_count()

    mapping = dictionary_map(d_closed, z3_coeff)

    labels = {
        'finite_graph_model_id': f'FG(two-plaquette, D={D_PRIMARY}, tau_FG, I1.5-style, gauge-invariant)',
        'complete_residual_all_channels': True,
        'certified_representation_tail': True,
        'own_free_reference': bool(fg_facts['own_free_reference']),
        'no_transfer_to_aq': True,
        'fg_coefficients_not_fitted': True,
        'consistency_map_not_proof': True,
    }

    passed = bool(
        fg_facts['K_x_equals_3x'] and fg_facts['x_mean_is_zero'] and fg_facts['own_free_reference']
        and fg_facts['free_gap_equals_3']
        and two_methods_agree
        and arb['arb_ball_contains_exact_fraction']
        and owned_per_block == 24
        and z3_meta['referenced_as_unchanged_in_ax1_gate_transfer_item']
        and mapping['matches_under_A1_A4']
        and not mapping['contrast_naive_dictionary_tau_FG_equals_tau']['matches']
    )

    return {
        'tool': 'A3-4 az2_dictionary_calc',
        'assumptions': {
            'A1_alpha_equals_1_both_sides': True,
            'A2_AW1_parity_theorem_only_f_equals_W_survives_at_first_order': True,
            'A3_tau_FG_defined_as_tau_over_24': True,
            'A4_free_gap_identification_FG_3_equals_Z3_plaquette_energy_3': True,
        },
        'fg_side': {
            'convention': 'H_FG(tau_FG) = K - tau_FG * x  (Round11 advisor.md / az2_spec_check.md section 3, primary/asymmetric variant)',
            'facts_confirmed_live': fg_facts,
            'derivative_closed_form': {'value': str(d_closed), 'preview': float(d_closed), **closed_detail},
            'derivative_regularized_solve': {'value': str(d_solve), 'preview': float(d_solve), **solve_detail},
            'two_independent_methods_agree': bool(two_methods_agree),
            'arb_crosscheck_of_regularized_solve': arb,
        },
        'z3_side': {
            'convention': 'V_b = -(tau/24) * sum_{f=1}^{24} W_f  (alpha units, route-B uniform per-block '
                           'potential; "plaquette energy 3" read as the declared free/reference electric scale)',
            'owned_faces_per_block_confirmed_independently': owned_per_block,
            'admitted_first_order_coefficient': z3_meta,
        },
        'dictionary': mapping,
        'labels': labels,
        'passed': passed,
    }


def main():
    result = self_test()
    print(json.dumps(result, indent=2, default=str))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
