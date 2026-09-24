#!/usr/bin/env python3
"""first_order_density_from_c1.py -- an independent recomputation of the
first-order reduced density `rho^(1)_R` from the ADMITTED AW1 first-order
coefficient `c^(1)`, plus an explicit small-basis SU(2) Peter-Weyl / exact
Clebsch-Gordan construction of the operator, cross-checked against the
AY1-admitted numbers.

Round32, sub-round 4, modern (Penrose/Feynman) lens, assistant-4.
Status: assistant/coder cross-check tool. Counts ZERO research loops
(update-3.md panel-update-3 section 6 item 6, modern share). sympy,
python-flint 0.9 (Arb) are cross-check libraries only; nothing here is
imported by any `check.py`, and nothing here decides admission. Every
number this repository actually admits was already decided by exact
`fractions.Fraction` arithmetic in `forward/aw1/check.py`,
`forward/ay1/check.py`, `reverse/ay1/check.py` and the skeptic's own
checkers; this file recomputes it a second, independent way and compares.

What is recomputed, and from where
-----------------------------------
`research/round32/forward/aw1/report.md` (accepted item 3) gives the
admitted first-order creation `c^(1) = L_0 = -(tau/72) sum_f W_f Omega_0`,
summed over the ten omitted faces anchored at 0 whose owner set is exactly
`R = {0, e_z}` (I1 table, AW1 F02). `research/round32/advisor/aw1-gate.json`
and `research/round32/advisor/ay1-gate.json` (loop AY1, already admitted in
this same round) both restate the resulting first-order REDUCED density

    rho^(1)_R = (tau/72) sum_{f: M_f=R} (|W_f Omega_R><Omega_R| + h.c.)

This file does NOT read AY1's own derivation and copy it: it re-derives
the same object from the AW1 report's stated `c^(1)` and the I1 combinatorics
(section 1 below, reusing assistant-3's already-cross-checked encoding of
the shared I1 24-anchored-face-class table plus a genuinely different,
anchor-union enumeration route), and re-derives the SU(2) Haar moments that
make the operator algebra work from first principles via the Peter-Weyl
character theory / exact SU(2) Clebsch-Gordan fusion rule (section 2),
rather than citing AW1's Haar-moment line. Section 3 builds the operator in
an explicit small orthonormal basis and checks the Gram matrix, rank,
eigenvalues, trace norm and the two named traces. Section 4 compares every
number to the admitted AY1 gate and to both AY1 producers' `results.json`.

Reused BY IMPORT (never reimplemented, never modified):
  - `research/round32/experts/modern/assistant-3/uniform_counts_from_scratch.py`
    (an assistant tool, not a producer `check.py`): its independently-typed
    encoding of the shared I1 24-anchored-face-class table, and its own two
    validated methods, as a cross-check of this file's own from-scratch
    anchor enumeration.
  - `research/round32/experts/modern/assistant-1/flint_harness.py` (an
    assistant tool): `to_fmpq`, `contains`, `rational_sqrt_bracket`, for the
    Arb/mpmath-style cross-check of `sqrt(10)`.
"""
import importlib.util
import json
import sys
import time
from fractions import Fraction as Q
from pathlib import Path

import flint
import sympy as sp

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]
R32 = ROOT / 'research' / 'round32'
assert (ROOT / 'AGENTS.md').is_file(), f'unexpected ROOT: {ROOT}'


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ucs = _load('uniform_counts_a4', R32 / 'experts' / 'modern' / 'assistant-3' / 'uniform_counts_from_scratch.py')
flint_harness = _load('flint_harness_a4', R32 / 'experts' / 'modern' / 'assistant-1' / 'flint_harness.py')

EX, EY, EZ = (1, 0, 0), (0, 1, 0), (0, 0, 1)
S_SET = (ZERO := (0, 0, 0), EX, EY, EZ)
R_SITES = (ZERO, EZ)


def add3(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub3(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


# =====================================================================
# 1. Combinatorics: the 82 faces meeting R from the 7 incident anchors
# =====================================================================
def incident_anchors():
    """R - S = {r - s : r in R, s in S}, deduplicated. AW1 report section 4
    ('the groups meeting R are exactly the seven anchors
    R-S={0,-e_x,-e_y,-e_z,e_z,e_z-e_x,e_z-e_y}') and AY1
    forward/output/results.json check 'missing_incoming_stars'
    ('incident_anchors') both state this set; this function derives it
    from R and S alone, not by citing either."""
    anchors = sorted({sub3(r, s) for r in R_SITES for s in S_SET})
    return anchors


def anchor_union_enumeration():
    """Independent enumeration route: iterate the 7 incident anchors
    directly (not assistant-3's per-site inclusion-exclusion, and not its
    brute-force box scan), and for each anchor's 21 omitted I1 classes
    (reusing assistant-3's already-cross-checked `CLASSES`/`support_of`
    data, never retyped here) keep those whose support meets R. Since
    every omitted face has support size >= 2 (I1 table: no one-site
    owner set), a support that is a SUBSET of the two-site R must equal R
    exactly, so 'support <= R' below literally means 'owner set exactly
    R'. Each (anchor, class) pair is a distinct physical face (a face is
    charged exactly once, at its anchor), so no anchor-level
    double-counting arises."""
    anchors = incident_anchors()
    meeting = []
    owner_set_R = []
    for anchor in anchors:
        for cls in ucs.CLASSES:
            if cls['role'] != 'omitted':
                continue
            supp = ucs.support_of(anchor, cls)
            if supp & frozenset(R_SITES):
                entry = {'anchor': anchor, 'orientation': cls['orientation'], 'r': cls['r'], 's': cls['s'],
                         'support': sorted(supp)}
                meeting.append(entry)
                if supp <= frozenset(R_SITES):
                    owner_set_R.append(entry)
    return anchors, meeting, owner_set_R


def combinatorics_report():
    anchors, meeting, owner_R = anchor_union_enumeration()
    straddling = len(meeting) - len(owner_R)

    # Cross-check 1: assistant-3's own two independently-agreeing methods
    # (imported, not retyped), restricted to the omitted role only (the
    # zero-selected patterned model gives the 3 selected classes per anchor
    # coefficient 0, so they never enter c^(1); AW1/AY1's 82/10/72 counts
    # are the OMITTED-only counts, identical to assistant-3's AX1-route-B
    # omitted subtotal).
    m1 = ucs.method1_R_cover()
    m2 = ucs.method2_R(box_radius=6)
    cross_check_assistant3 = {
        'meeting_R_omitted': m1['meeting_R_omitted'], 'inside_R_omitted': m1['inside_R_omitted'],
        'method1_matches_mine': (m1['meeting_R_omitted'], m1['inside_R_omitted']) == (len(meeting), len(owner_R)),
        'method2_matches_mine': (m2['meeting_omitted'], m2['inside_omitted']) == (len(meeting), len(owner_R)),
    }

    # Cross-check 2: the AY1 forward producer's own admitted pins and
    # incident-anchor list (live-read, never retyped as literals here).
    ay1_fwd = json.loads((R32 / 'forward' / 'ay1' / 'output' / 'results.json').read_text())
    pins_check = next(c for c in ay1_fwd['checks'] if c['id'] == 'face_enumeration_R_local')['pins']
    anchors_check = next(c for c in ay1_fwd['checks'] if c['id'] == 'missing_incoming_stars')['incident_anchors']
    admitted_anchors = sorted(tuple(a) for a in anchors_check)
    explicit_10 = next(c for c in ay1_fwd['checks'] if c['id'] == 'first_order_density_explicit')['faces_owner_set_R']

    my_10_labels = [f"anchor {tuple(e['anchor'])} {e['orientation']} r={e['r']} s={e['s']}" for e in owner_R]

    return {
        'incident_anchors_mine': [list(a) for a in anchors],
        'incident_anchors_admitted_ay1': [list(a) for a in admitted_anchors],
        'anchors_match': anchors == admitted_anchors,
        'faces_meeting_R': len(meeting),
        'faces_owner_set_R': len(owner_R),
        'faces_straddling_R': straddling,
        'expected': {'meeting': 82, 'owner_set_R': 10, 'straddling': 72},
        'counts_match_expected': (len(meeting), len(owner_R), straddling) == (82, 10, 72),
        'cross_check_assistant3': cross_check_assistant3,
        'counts_match_ay1_pins': (len(meeting), len(owner_R), straddling) == (pins_check['meet'], pins_check['inside'], pins_check['straddling']),
        'my_10_face_labels': my_10_labels,
        'ay1_admitted_10_face_labels': explicit_10,
        'my_10_labels_match_ay1_as_sets': sorted(my_10_labels) == sorted(explicit_10),
        'wilson_face_is_first_listed': my_10_labels[0] == 'anchor (0, 0, 0) xz r=0 s=0',
    }


# =====================================================================
# 2. SU(2) Haar integration: Peter-Weyl characters and exact CG fusion
# =====================================================================
def su2_character_theory_report():
    """Two independent exact derivations of the SU(2) Haar moments
    E[W^n] (W=(1/2)chi_{1/2}, the normalized fundamental Wilson trace),
    used below to build the orthonormal basis. Neither cites AW1's
    Haar-moment line; both work from the SU(2) class-angle measure
    dmu(theta)=(2/pi) sin^2(theta) dtheta and the character
    chi_j(theta)=sin((2j+1)theta)/sin(theta), i.e. genuine "SU(2) Haar
    integration on the relevant link"."""
    theta = sp.symbols('theta', positive=True)

    def chi(j):
        j = sp.Rational(j)
        return sp.sin((2 * j + 1) * theta) / sp.sin(theta)

    measure = sp.Rational(2, 1) / sp.pi * sp.sin(theta) ** 2

    # (a) Exact Clebsch-Gordan fusion identities, verified as symbolic trig
    # identities (sympy `simplify`, not floating evaluation): chi_a*chi_b =
    # sum_{c=|a-b|}^{a+b, step 1} chi_c, with unit SU(2) fusion coefficients.
    fusion_half_half = sp.simplify(chi(sp.Rational(1, 2)) * chi(sp.Rational(1, 2)) - (chi(0) + chi(1)))
    fusion_half_one = sp.simplify(chi(sp.Rational(1, 2)) * chi(1) - (chi(sp.Rational(1, 2)) + chi(sp.Rational(3, 2))))

    # (b) Direct symbolic Haar integration (orthogonality of characters,
    # a genuinely different computation from (c) below) for the low
    # moments, plus the orthogonality table on {0,1/2,1,3/2}.
    orth_table = {}
    spins = [0, sp.Rational(1, 2), 1, sp.Rational(3, 2)]
    for j in spins:
        for jp in spins:
            if j <= jp:
                orth_table[f'{j},{jp}'] = str(sp.nsimplify(sp.integrate(chi(j) * chi(jp) * measure, (theta, 0, sp.pi))))
    direct_moments_low = []
    for n in range(5):
        val = sp.nsimplify(sp.integrate((sp.Rational(1, 2) * chi(sp.Rational(1, 2))) ** n * measure, (theta, 0, sp.pi)))
        direct_moments_low.append(str(val))

    # (c) Exact Clebsch-Gordan fusion iteration (Fraction arithmetic, no
    # symbolic integration): repeatedly fuse chi_{1/2} into the running
    # state and read off the chi_0 coefficient, i.e. exact-Fraction
    # book-keeping of the same fusion rule verified symbolically in (a).
    def fuse2j(a2j, b2j):
        return list(range(abs(a2j - b2j), a2j + b2j + 1, 2))

    state = {0: Q(1)}
    moments_fusion = [Q(1)]
    for _ in range(1, 9):
        new = {}
        for j2, c in state.items():
            for c2 in fuse2j(j2, 1):
                new[c2] = new.get(c2, Q(0)) + c * Q(1, 2)
        state = new
        moments_fusion.append(state.get(0, Q(0)))

    admitted_moments = [Q(1), Q(0), Q(1, 4), Q(0), Q(1, 8), Q(0), Q(5, 64), Q(0), Q(7, 128)]

    return {
        'fusion_identity_half_times_half_minus_chi0_plus_chi1_simplifies_to_zero': fusion_half_half == 0,
        'fusion_identity_half_times_one_minus_half_plus_threehalves_simplifies_to_zero': fusion_half_one == 0,
        'character_orthogonality_table_j_le_jp': orth_table,
        'orthogonality_all_diagonal_one_offdiagonal_zero': all(
            (v == '1') == (a.split(',')[0] == a.split(',')[1]) for a, v in orth_table.items()),
        'direct_symbolic_integration_moments_n0_to_4': direct_moments_low,
        'fusion_iteration_moments_n0_to_8': [str(m) for m in moments_fusion],
        'admitted_haar_moments_n0_to_8': [str(m) for m in admitted_moments],
        'direct_matches_fusion_n0_to_4': direct_moments_low == [str(m) for m in moments_fusion[:5]],
        'fusion_matches_admitted': moments_fusion == admitted_moments,
    }


# =====================================================================
# 3. Explicit small basis: build rho^(1)_R and verify its algebra
# =====================================================================
FACE_LABELS = None  # filled in main() from the combinatorics section, in the AY1-matching order


def fuse2j(a2j, b2j):
    return list(range(abs(a2j - b2j), a2j + b2j + 1, 2))


def apply_W_at(state, idx, n_faces):
    """Multiply a state (dict: tuple-of-2j -> Fraction coefficient) by the
    fixed face's Wilson variable W_idx=(1/2)chi_{1/2} at tensor factor
    `idx`, using the exact CG fusion rule (section 2); other factors are
    untouched. The 10 faces are modelled as independent SU(2) class-
    function factors (Peter-Weyl basis truncated to the spins that occur),
    inheriting the AW1-admitted 'two distinct plaquettes share at most one
    link' fact (forward/aw1/report.md line 103) as the licence for this
    independence -- not re-derived from lattice link geometry here."""
    new = {}
    for spins, coeff in state.items():
        j2 = spins[idx]
        for c2 in fuse2j(j2, 1):
            key = spins[:idx] + (c2,) + spins[idx + 1:]
            new[key] = new.get(key, Q(0)) + coeff * Q(1, 2)
    return {k: v for k, v in new.items() if v != 0}


def inner(state1, state2):
    return sum(state1.get(k, Q(0)) * v for k, v in state2.items())


def scale(state, s):
    return {k: s * v for k, v in state.items()}


def add_states(*states):
    out = {}
    for st in states:
        for k, v in st.items():
            out[k] = out.get(k, Q(0)) + v
    return {k: v for k, v in out.items() if v != 0}


def build_operator_algebra(n_faces, idx_w):
    vac_key = tuple(0 for _ in range(n_faces))
    Omega = {vac_key: Q(1)}
    v = [apply_W_at(Omega, f, n_faces) for f in range(n_faces)]  # v[f] = W_f Omega_R

    # --- Gram matrix of {Omega_R, 2 W_f Omega_R}, 11x11 ---
    basis_vecs = [Omega] + [scale(v[f], 2) for f in range(n_faces)]
    n = len(basis_vecs)
    gram = [[inner(basis_vecs[i], basis_vecs[j]) for j in range(n)] for i in range(n)]
    identity = [[Q(1) if i == j else Q(0) for j in range(n)] for i in range(n)]
    gram_is_identity = (gram == identity)

    # --- The operator's shape matrix M (tau=1 placeholder; T = tau * M),
    # built purely from apply_W_at + inner, not hand-plugged as a "star
    # graph": M_ij = <basis_i, apply_T(basis_j, tau=1)> where
    # apply_T(state)=(1/72) sum_f (|v_f><Omega|+|Omega><v_f|) state. ---
    def apply_T_shape(state):
        c_omega = inner(Omega, state)
        out = {}
        for f in range(n_faces):
            out = add_states(out, scale(v[f], Q(1, 72) * c_omega))
        total_vf_overlap = Q(0)
        for f in range(n_faces):
            total_vf_overlap += inner(v[f], state)
        out = add_states(out, scale(Omega, Q(1, 72) * total_vf_overlap))
        return out

    M = [[inner(basis_vecs[i], apply_T_shape(basis_vecs[j])) for j in range(n)] for i in range(n)]
    M_sym = sp.Matrix([[sp.Rational(x.numerator, x.denominator) for x in row] for row in M])
    rank_M = M_sym.rank()
    eigen = M_sym.eigenvals()  # {eigenvalue: multiplicity}
    eig_list = sorted(((sp.nsimplify(k), v) for k, v in eigen.items()), key=lambda kv: sp.N(kv[0]))

    sqrt10 = sp.sqrt(10)
    expected_eigs = {sp.nsimplify(sqrt10 / 144): 1, sp.nsimplify(-sqrt10 / 144): 1, sp.Integer(0): n - 2}
    eig_dict_simplified = {sp.nsimplify(k): v for k, v in eigen.items()}
    eigenvalues_match_expected = (eig_dict_simplified == expected_eigs)

    # --- Traces of rho^(1) W and rho^(1) W^2, using tau=1 (coefficient
    # extraction; the overall tau-prefactor is manifest by construction). ---
    def W_op(state):
        return apply_W_at(state, idx_w, n_faces)

    def trace_rho1_times(op):
        total = Q(0)
        for f in range(n_faces):
            total += inner(Omega, op(v[f]))
            total += inner(v[f], op(Omega))
        return Q(1, 72) * total

    tr_rho1_W = trace_rho1_times(W_op)
    tr_rho1_W2 = trace_rho1_times(lambda st: W_op(W_op(st)))

    return {
        'n_basis': n,
        'gram_matrix_is_identity_11x11': gram_is_identity,
        'operator_rank': int(rank_M),
        'rank_equals_2': rank_M == 2,
        'eigenvalues_of_shape_matrix_M': {str(k): v for k, v in eig_dict_simplified.items()},
        'eigenvalues_match_plus_minus_sqrt10_over_144_and_zero': bool(eigenvalues_match_expected),
        'tr_rho1_W_coefficient_of_tau': str(tr_rho1_W),
        'tr_rho1_W_matches_1_over_144': tr_rho1_W == Q(1, 144),
        'tr_rho1_W2_coefficient_of_tau': str(tr_rho1_W2),
        'tr_rho1_W2_matches_zero': tr_rho1_W2 == 0,
    }


# =====================================================================
# 4. Numeric preview at the cap tau=1e-8, Arb cross-check, AY1 comparison
# =====================================================================
def numeric_and_arb_report():
    tau_cap = Q(1, 10 ** 8)
    lo, hi = flint_harness.rational_sqrt_bracket(Q(10), bits=200)  # sqrt(10) directed bracket, reused not reimplemented
    assert lo * lo <= 10 <= hi * hi
    trace_norm_lo = lo * tau_cap / 72
    trace_norm_hi = hi * tau_cap / 72

    flint.ctx.prec = 256
    sqrt10_arb = flint.arb(10).sqrt()
    tau_arb = flint.arb(flint_harness.to_fmpq(tau_cap))
    trace_norm_arb = sqrt10_arb * tau_arb / 72
    ball_lo, ball_hi = flint_harness.arb_crosscheck.rational_bounds_arb(trace_norm_arb)
    bracket_contains_ball = (trace_norm_lo <= ball_lo and ball_hi <= trace_norm_hi)

    ay1_fwd = json.loads((R32 / 'forward' / 'ay1' / 'output' / 'results.json').read_text())
    ay1_admitted_trace_norm_upper = Q(ay1_fwd['headline']['rho1_R_trace_norm_upper'])
    ay1_admitted_preview = ay1_fwd['headline']['rho1_R_trace_norm_preview']
    ay1_admitted_tr_W = ay1_fwd['headline']['rho1_R_coefficient_in_orthonormal_basis']

    my_preview = float(trace_norm_hi)

    # AY1's own "trace_norm_upper" is itself an outward-rounded UPPER bound
    # on the true value (not the value itself), so the correct consistency
    # check is that it lies at or above my tight two-sided enclosure
    # [trace_norm_lo, trace_norm_hi] (built from a 200-bit directed sqrt(10)
    # bracket) and is close to it -- not that it falls "inside" my bracket.
    admitted_is_valid_and_tight_upper_bound = (
        ay1_admitted_trace_norm_upper >= trace_norm_hi
        and (ay1_admitted_trace_norm_upper - trace_norm_hi) < Q(1, 10 ** 20)
    )

    return {
        'tau_cap': str(tau_cap),
        'sqrt10_directed_bracket': [str(lo), str(hi)],
        'my_trace_norm_bracket': [str(trace_norm_lo), str(trace_norm_hi)],
        'my_trace_norm_preview': my_preview,
        'arb_256bit_ball_bounds': [str(ball_lo), str(ball_hi)],
        'my_fraction_bracket_contains_arb_ball': bool(bracket_contains_ball),
        'ay1_admitted_trace_norm_upper': str(ay1_admitted_trace_norm_upper),
        'ay1_admitted_trace_norm_preview': ay1_admitted_preview,
        'ay1_admitted_upper_is_valid_and_tight_vs_my_bracket': bool(admitted_is_valid_and_tight_upper_bound),
        'ay1_admitted_rho1_R_coefficient': ay1_admitted_tr_W,
    }


def compare_with_ay1_gate():
    gate = json.loads((R32 / 'advisor' / 'ay1-gate.json').read_text())
    accepted_text = gate['accepted']
    checks = ['rho^(1)_R=(tau/72) sum_{f in F_R}' in accepted_text,
              '||rho^(1)_R||_1=sqrt(10)|tau|/72' in accepted_text,
              'Tr(rho^(1)_R W)=+tau/144' in accepted_text]
    return {
        'gate_loop': gate['loop'], 'gate_verdict': gate['verdict'],
        'formula_string_found_verbatim_in_gate': checks[0],
        'trace_norm_string_found_verbatim_in_gate': checks[1],
        'tr_W_string_found_verbatim_in_gate': checks[2],
        'all_found': all(checks),
    }


def self_test():
    t0 = time.time()
    combi = combinatorics_report()
    theory = su2_character_theory_report()
    algebra = build_operator_algebra(n_faces=10, idx_w=0)  # index 0 <-> first-listed face, xz r=0 s=0, matches AY1 wilson_face_index
    numeric = numeric_and_arb_report()
    gate_cmp = compare_with_ay1_gate()
    elapsed = time.time() - t0

    passed = bool(
        combi['counts_match_expected'] and combi['counts_match_ay1_pins'] and combi['anchors_match']
        and combi['cross_check_assistant3']['method1_matches_mine'] and combi['cross_check_assistant3']['method2_matches_mine']
        and combi['my_10_labels_match_ay1_as_sets'] and combi['wilson_face_is_first_listed']
        and theory['fusion_identity_half_times_half_minus_chi0_plus_chi1_simplifies_to_zero']
        and theory['fusion_identity_half_times_one_minus_half_plus_threehalves_simplifies_to_zero']
        and theory['orthogonality_all_diagonal_one_offdiagonal_zero']
        and theory['direct_matches_fusion_n0_to_4'] and theory['fusion_matches_admitted']
        and algebra['gram_matrix_is_identity_11x11'] and algebra['rank_equals_2']
        and algebra['eigenvalues_match_plus_minus_sqrt10_over_144_and_zero']
        and algebra['tr_rho1_W_matches_1_over_144'] and algebra['tr_rho1_W2_matches_zero']
        and numeric['my_fraction_bracket_contains_arb_ball'] and numeric['ay1_admitted_upper_is_valid_and_tight_vs_my_bracket']
        and gate_cmp['all_found']
    )

    return {
        'tool': 'A4-1 first_order_density_from_c1',
        'labels': {'zero_research_loops': True, 'model_is_finite_graph': False,
                   'transfers_to_aq': 'no (recomputation of an already-admitted AQ_patterned_zero_selected result)',
                   'consistency_and_crosscheck_not_admission': True},
        'combinatorics_7_incident_anchors': combi,
        'su2_character_theory': theory,
        'operator_algebra_11dim_basis': algebra,
        'numeric_preview_and_arb_crosscheck': numeric,
        'comparison_with_ay1_gate': gate_cmp,
        'elapsed_seconds': elapsed,
        'passed': passed,
    }


def main():
    result = self_test()
    print(json.dumps(result, indent=2, default=str))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
