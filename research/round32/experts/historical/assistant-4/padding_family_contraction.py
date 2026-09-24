#!/usr/bin/env python3
"""
padding_family_contraction.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 4.

Zero research loops: test/planning script for the historical (Newton/
Tesla) lens's Round32 assistant package (assistant-4), not a producer,
skeptic or advisor artifact. Does not import research/round32/forward/
ay1/check.py or research/round32/reverse/ay1/check.py; those files are
never opened. Only their frozen `output/results.json` exports (data,
never code) are read, for bit-for-bit cross-checks, plus the two AY1
report.md files (prose), the AY1 gate and the I1 forward report.

Task (panel-update-3.md item 6, historical share, test 1). For the I1
all-contained-face boxes with padding on Lambda_N=[-N,N]^3, N=2,3,4:

  (a) independently enumerate the anchor groups of retained faces (21
      omitted faces per anchor with support b+S, whole stars; the
      zero-selected patterned model, coefficient -(tau/3) per face,
      ||phi_b||<=7|tau|) for both named families F1 (AQ1 centered
      whole-star boxes) and F2 (I1 section 6 all-contained-face boxes
      with padding);
  (b) verify group supports |X|<=4 factors, the maximal per-site
      interaction sum 28|tau| (=J_0=7/25000000 at |tau|=10^-8), the
      AM2 contraction inequalities J_0 G(R)<1/64 with
      G(t)=16 e^{8t}(1+10t), R=1/64 (an exact rational majorant of
      e^{1/8}, independently re-derived, plus an mpmath and a
      python-flint/Arb cross-check), termination order 8, and the
      reset budget on R={0,e_z}: 98|tau| (7 incident anchors x 7|tau|
      x 2);
  (c) compare with F1: the count of extra boundary faces retained by
      F2, 28N(5N+1), and confirm both families retain the same 82
      faces meeting R for N>=2.

Method. The 21 I1 omitted face classes (research/round21/forward/i1/
report.md section 3) and the translation-covariant "faces touching a
site" method are reused from this lens's own assistant-1 script
(am2_tiers_exact.py -- an assistant script, not a producer check.py),
exactly as assistant-3's uniform_face_count.py and
route_b_incidence_table.py already reused it. On top of that, this
script adds its own from-scratch box enumeration (Lambda_N is a finite
set of coarse anchors; a class is F1-retained at anchor b iff the
WHOLE star b+S subset Lambda_N, and F2-retained iff its OWN owner set
(a subset of b+S) subset Lambda_N), which the earlier assistant scripts
did not need (they worked on the infinite translation-covariant
lattice only).

Read before writing: research/round32/forward/ay1/report.md,
research/round32/reverse/ay1/report.md (both frozen and gated),
research/round32/advisor/ay1-gate.json, research/round21/forward/i1/
report.md section 6, research/round32/forward/ay1/output/results.json,
research/round32/reverse/ay1/output/results.json (data only), and this
lens's assistant-1/am2_tiers_exact.py.

Arithmetic: fractions.Fraction for every pass/fail comparison. mpmath
(high-precision float) and python-flint's Arb (verified ball
arithmetic) are used only as independent, clearly labelled numerical
CROSS-CHECKS of the rational bound e^{1/8}<8/7, never as the bound
itself.

Run with: python3 -B padding_family_contraction.py
"""
import importlib.util
import itertools
import json
import math
import os
import sys
from fractions import Fraction as F

import mpmath

try:
    import flint
    HAVE_FLINT = True
except Exception:  # pragma: no cover - optional cross-check only
    HAVE_FLINT = False

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
ASSISTANT1_DIR = os.path.join(REPO_ROOT, "research/round32/experts/historical/assistant-1")
FWD_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/ay1/output/results.json")
REV_RESULTS = os.path.join(REPO_ROOT, "research/round32/reverse/ay1/output/results.json")


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def _load_assistant1_am2():
    spec = importlib.util.spec_from_file_location(
        "am2_tiers_exact", os.path.join(ASSISTANT1_DIR, "am2_tiers_exact.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


AM2 = _load_assistant1_am2()
ZERO, EX, EY, EZ, S = AM2.ZERO, AM2.EX, AM2.EY, AM2.EZ, AM2.S
OMITTED_CLASSES = AM2.OMITTED_CLASSES
vadd, vsub = AM2.vadd, AM2.vsub
assert len(OMITTED_CLASSES) == 21
assert len(S) == 4  # |X| <= 4 factors, by construction of the star


# ---------------------------------------------------------------------
# Part A: box enumeration of F1 (AQ1 centered whole-star) and F2 (I1
# section 6 all-contained-face padded) on Lambda_N=[-N,N]^3, N=2,3,4.
# Independent of, and not relying on, the closed forms derived below;
# the closed forms are cross-checked against this brute-force count.
# ---------------------------------------------------------------------

def lambda_n_sites(N):
    return list(itertools.product(range(-N, N + 1), repeat=3))


def in_box(p, N):
    return all(-N <= c <= N for c in p)


def anchor_report(N):
    """
    For every anchor b in Lambda_N, classify it and count F1/F2 retained
    faces at that anchor, by literally checking, for every one of the 21
    OMITTED_CLASSES entries K (a frozenset of offsets), whether every
    offset d in K has b+d inside Lambda_N (F2 rule) and whether the
    WHOLE star b+S is inside Lambda_N (F1 rule) -- the general method,
    not the 6-type shortcut table.
    """
    sites = lambda_n_sites(N)
    full_star_anchors = 0
    f2_total = 0
    f1_total = 0
    full_groups = 0
    partial_groups = 0
    zero_groups = 0
    per_anchor_f2 = {}
    for b in sites:
        whole_star_in = all(in_box(vadd(b, d), N) for d in S)
        if whole_star_in:
            full_star_anchors += 1
            f1_total += len(OMITTED_CLASSES)
        f2_here = 0
        for K in OMITTED_CLASSES:
            if all(in_box(vadd(b, d), N) for d in K):
                f2_here += 1
        f2_total += f2_here
        per_anchor_f2[b] = f2_here
        if f2_here == len(OMITTED_CLASSES):
            full_groups += 1
        elif f2_here == 0:
            zero_groups += 1
        else:
            partial_groups += 1
    assert full_groups == full_star_anchors
    return {
        "N": N,
        "B_sites": len(sites),
        "faces_F1": f1_total,
        "faces_F2": f2_total,
        "extra_F2_minus_F1": f2_total - f1_total,
        "full_star_anchors": full_star_anchors,
        "partial_groups": partial_groups,
        "zero_groups": zero_groups,
        "full_plus_partial_plus_zero": full_groups + partial_groups + zero_groups,
    }


def B_plus_size(N):
    """|B_+| = |union_{b in Lambda_N} (b+S)|, the padded on-site volume."""
    Bset = set(lambda_n_sites(N))
    Bplus = set()
    for b in Bset:
        for d in S:
            Bplus.add(vadd(b, d))
    return len(Bplus)


def closed_form_F1(N):
    return 21 * (2 * N) ** 3


def closed_form_F2(N):
    return 28 * N * (2 * N + 1) * (3 * N + 1)


def closed_form_extra(N):
    return 28 * N * (5 * N + 1)


# ---------------------------------------------------------------------
# Part B: the 82 faces meeting R={0,e_z}, and confirming both families
# retain exactly the same 82 (as (anchor,class_idx) pairs, not just as
# a count) for N=2,3,4.
# ---------------------------------------------------------------------

def faces_meeting_R():
    """Reuses assistant-1's faces_touching(u); union over u in R={0,e_z}."""
    faces_0 = AM2.faces_touching(ZERO)
    faces_ez = AM2.faces_touching(EZ)
    keyed = {}
    for b, idx, owner_set in faces_0 + faces_ez:
        keyed[(b, idx)] = owner_set
    return keyed  # dict (anchor,class_idx) -> owner_set


def face_family_membership(anchor, owner_set, N):
    f1_in = all(in_box(vadd(anchor, d), N) for d in S)
    f2_in = all(in_box(p, N) for p in owner_set)
    return f1_in, f2_in


# ---------------------------------------------------------------------
# Part C: per-site interaction sum J^(2) = max_u sum_{groups owning u}
# ||group||, in units of |tau|/3 per face (a full 21-face group has
# weight 7 in these units); verified <=28 and attained (=28) at bulk
# sites, for both families, at N=2,3,4.
# ---------------------------------------------------------------------

def max_per_site_sum(N):
    """
    AM2's per-site sum J = max_u sum_{b: u in X_b} ||phi_b||: each
    RETAINED GROUP (anchor b) contributes its own full norm
    (retained_face_count_b/3)|tau| to every site u in its actual
    support X_b = union of the owner sets of its retained classes
    (X_b=b+S exactly when the group is a whole/full star; a subset of
    b+S when F2 only partially retains it at the boundary) -- this is
    the AM2/AY1 definition (H4), NOT a per-face tally (that different,
    smaller quantity is the "49 faces per site" bound used for t_1).
    Returns the F1 and F2 maxima, in units of |tau|.
    """
    sites = lambda_n_sites(N)
    touched = set()
    for b in sites:
        for d in S:
            touched.add(vadd(b, d))

    f1_sum = {u: F(0) for u in touched}
    f2_sum = {u: F(0) for u in touched}
    for b in sites:
        whole_star_in = all(in_box(vadd(b, d), N) for d in S)
        retained_owner_union_f2 = set()
        f2_count = 0
        for K in OMITTED_CLASSES:
            owner_set = frozenset(vadd(b, dd) for dd in K)
            if all(in_box(p, N) for p in owner_set):
                f2_count += 1
                retained_owner_union_f2 |= owner_set
        if f2_count:
            weight_f2 = F(f2_count, 3)
            for u in retained_owner_union_f2:
                f2_sum[u] += weight_f2
        if whole_star_in:
            weight_f1 = F(len(OMITTED_CLASSES), 3)
            for u in S:
                f1_sum[vadd(b, u)] += weight_f1
    f1_max = max(f1_sum.values()) if f1_sum else F(0)
    f2_max = max(f2_sum.values()) if f2_sum else F(0)
    return f1_max, f2_max


# ---------------------------------------------------------------------
# Part D: exp(1/8) < 8/7, independently re-derived (Taylor truncation +
# exact geometric tail bound), then fed through the AM2/AY1 chain
# G(t)=16 e^{8t}(1+10t), G'(t)=16 e^{8t}(18+80t), at t=R=1/64, with
# J_0=28|tau|<=7/25000000 (NOT AX1's route-B J_0'=29|tau|). Cross-
# checked with mpmath and (if available) python-flint's Arb.
# ---------------------------------------------------------------------

def exp_upper_bound(x, n_terms):
    assert 0 < x < 1
    partial = F(0)
    term = F(1)
    for k in range(n_terms):
        partial += term
        term *= x
        term /= (k + 1)
    ratio_cap = x / (n_terms + 1)
    assert ratio_cap < 1
    tail_bound = term / (1 - ratio_cap)
    return partial + tail_bound


def am2_contraction(tau_abs_cap):
    # Independent re-derivation that exp(1/8)<8/7 (12-term Taylor
    # truncation + exact geometric tail bound -- a different truncation
    # degree from this lens's own assistant-3 j0_contraction_replay.py,
    # which used 10 terms for the AX1 loop, re-derived here from
    # scratch for AY1). This licenses plugging the literal clean
    # rational 8/7 (not our own possibly-tighter exp_bound) into the
    # AM2/AY1 chain below, exactly as HNM-AY1-F04 / the forward and
    # reverse reports do, to reproduce their named rationals 148/7 and
    # 352 literally (a tighter bound would give a smaller, still valid,
    # but non-matching number).
    exp_bound = exp_upper_bound(F(1, 8), 12)
    exp_ok = exp_bound < F(8, 7)

    R = F(1, 64)
    literal_8_7 = F(8, 7)
    G_R = 16 * literal_8_7 * (1 + 10 * R)
    Gp_R = 16 * literal_8_7 * (18 + 80 * R)
    G_R_expected = F(148, 7)
    Gp_R_expected = F(352)

    J0 = 28 * tau_abs_cap
    J0_expected = F(7, 25000000)

    self_map = J0_expected * G_R_expected
    self_map_expected = F(37, 6250000)
    exclusion = 2 * J0_expected * Gp_R_expected
    exclusion_expected = F(77, 390625)

    # mpmath cross-check (independent numerical route)
    mpmath.mp.dps = 60
    mp_exp_val = mpmath.e ** (mpmath.mpf(1) / 8)
    mp_bound_ok = mp_exp_val < mpmath.mpf(8) / 7
    mp_G_R = 16 * mp_exp_val * (1 + 10 * mpmath.mpf(1) / 64)
    mp_Gp_R = 16 * mp_exp_val * (18 + 80 * mpmath.mpf(1) / 64)
    mp_self_map = mpmath.mpf(J0_expected.numerator) / J0_expected.denominator * mp_G_R
    mp_exclusion = 2 * mpmath.mpf(J0_expected.numerator) / J0_expected.denominator * mp_Gp_R

    flint_result = None
    if HAVE_FLINT:
        arb_ctx = flint.ctx
        arb_ctx.prec = 200
        x = flint.arb(1) / 8
        arb_exp = x.exp()
        arb_lt_8_7 = bool(arb_exp < flint.arb(8) / 7)
        flint_result = {
            "arb_exp_1_8": str(arb_exp),
            "arb_exp_1_8_lt_8_7": arb_lt_8_7,
        }

    return {
        "exp_upper_bound_exact": str(exp_bound),
        "exp_upper_bound_decimal": float(exp_bound),
        "exp_1_8_lt_8_7": exp_ok,
        "R": str(R),
        "G_R": str(G_R),
        "G_R_expected_148_7": str(G_R_expected),
        "G_R_matches": G_R == G_R_expected,
        "Gp_R": str(Gp_R),
        "Gp_R_expected_352": str(Gp_R_expected),
        "Gp_R_matches": Gp_R == Gp_R_expected,
        "J0": str(J0),
        "J0_expected_7_25000000": str(J0_expected),
        "J0_matches": J0 == J0_expected,
        "self_map_J0_G_R": str(self_map),
        "self_map_expected_37_6250000": str(self_map_expected),
        "self_map_matches": self_map == self_map_expected,
        "self_map_lt_1_64": self_map < F(1, 64),
        "exclusion_2J0_Gp_R": str(exclusion),
        "exclusion_expected_77_390625": str(exclusion_expected),
        "exclusion_matches": exclusion == exclusion_expected,
        "exclusion_lt_1": exclusion < 1,
        "mpmath_cross_check": {
            "dps": 60,
            "exp_1_8": mpmath.nstr(mp_exp_val, 20),
            "exp_1_8_lt_8_7": bool(mp_bound_ok),
            "self_map_preview": mpmath.nstr(mp_self_map, 12),
            "exclusion_preview": mpmath.nstr(mp_exclusion, 12),
            "true_self_map_below_rational_bound": bool(mp_self_map < mpmath.mpf(self_map.numerator) / self_map.denominator),
        },
        "flint_arb_cross_check": flint_result,
        "flint_available": HAVE_FLINT,
    }


# ---------------------------------------------------------------------
# Part E: termination order 8. AM2's own combinatorial argument ("a
# nested word with more than 2p creations puts at least p+1 on one side
# of V_X, all meeting a p-site set, and two of them overlap") is
# verified as a GENERAL structural fact on a concrete, independently
# constructed finite-dimensional commuting-nilpotent creation algebra
# (generic rational matrix entries, p sites, each with two levels:
# vacuum/excited). This is our OWN fixture, not a reproduction of the
# forward/reverse check.py's internal numeric constants (their exported
# "four_site_order8: 40320=8!" and "two_site_order4: 24=4!" fixtures are
# read only for a qualitative, structural cross-check: same order 2p /
# 2p+1 pattern), since those check.py files are never opened.
# ---------------------------------------------------------------------

def creation_algebra_termination_fixture(p, seed_primes, v_seed=101):
    """
    C = sum_{i=0}^{p-1} a_i * (single-site raising operator at site i),
    on a p-qubit space (dimension 2^p): hat(c_i)|s> = a_i|s ∪ {i}> if
    bit i of s is 0, else 0 (nilpotent, hat(c_i)^2=0; disjoint c_i, c_j
    commute; here all generators are disjoint singletons by
    construction). V is a GENERIC dense operator on the same p-site
    space (support X = all p sites), with distinct rational entries, so
    that no cancellation in ad_C^k(V) is an artefact of a special
    choice of V. Returns the smallest k for which ad_C^k(V) is
    IDENTICALLY zero as an operator (not just applied to one vector).
    """
    D = 1 << p
    C = [[F(0)] * D for _ in range(D)]
    for i in range(p):
        mask = 1 << i
        a = F(seed_primes[i])
        for s in range(D):
            if s & mask == 0:
                C[s | mask][s] += a
    import random
    rnd = random.Random(v_seed)
    V = [[F(rnd.randint(1, 50), rnd.randint(1, 7)) for _ in range(D)] for _ in range(D)]

    def matmul(A, B):
        n = len(A)
        return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

    def matsub(A, B):
        n = len(A)
        return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

    def is_zero(A):
        return all(all(x == 0 for x in row) for row in A)

    def commutator(A, X):
        return matsub(matmul(A, X), matmul(X, A))

    # C^(p+1) must vanish identically: any p+1 singleton generators from
    # only p distinct labels must repeat a label (pigeonhole), and
    # hat(c_i)^2=0 kills the repeated factor after commuting it adjacent
    # (all generators here are mutually disjoint-or-equal, hence commute).
    Cpow = [[F(1) if i == j else F(0) for j in range(D)] for i in range(D)]
    for _ in range(p):
        Cpow = matmul(Cpow, C)
    C_p_zero = is_zero(Cpow)
    Cpow1 = matmul(Cpow, C)
    C_p1_zero = is_zero(Cpow1)

    ad = V
    first_zero_k = None
    last_nonzero_k = None
    history = {}
    for k in range(0, 2 * p + 3):
        z = is_zero(ad)
        history[k] = z
        if z and first_zero_k is None:
            first_zero_k = k
        if not z:
            last_nonzero_k = k
        ad = commutator(C, ad)

    return {
        "p": p,
        "dimension": D,
        "C_p_zero": C_p_zero,
        "C_p1_zero (pigeonhole: p+1 singleton generators from p labels must repeat)": C_p1_zero,
        "ad_C_k_zero_by_k": history,
        "first_k_with_ad_identically_zero": first_zero_k,
        "last_k_with_ad_nonzero": last_nonzero_k,
        "termination_order_2p": last_nonzero_k == 2 * p and first_zero_k == 2 * p + 1,
    }


# ---------------------------------------------------------------------
# Part F: reset budget on R={0,e_z}. Incident anchors = (0-S) union
# (e_z-S), independently derived (not asserted), then 2*7*7|tau|=98|tau|.
# ---------------------------------------------------------------------

def incident_anchors_R():
    from_0 = {vsub(ZERO, d) for d in S}
    from_ez = {vsub(EZ, d) for d in S}
    return from_0 | from_ez


def main():
    tau_cap = F(1, 10 ** 8)

    # --- Part A: box enumeration, N=2,3,4 ---
    box_reports = {}
    for N in (2, 3, 4):
        rep = anchor_report(N)
        rep["B_plus_sites"] = B_plus_size(N)
        rep["closed_form_F1_168N3"] = closed_form_F1(N)
        rep["closed_form_F2_28N_2N1_3N1"] = closed_form_F2(N)
        rep["closed_form_extra_28N_5N1"] = closed_form_extra(N)
        rep["F1_matches_closed_form"] = rep["faces_F1"] == rep["closed_form_F1_168N3"]
        rep["F2_matches_closed_form"] = rep["faces_F2"] == rep["closed_form_F2_28N_2N1_3N1"]
        rep["extra_matches_closed_form"] = rep["extra_F2_minus_F1"] == rep["closed_form_extra_28N_5N1"]
        box_reports[N] = rep

    # --- Part B: 82 faces meeting R, same for both families, N=2,3,4 ---
    faces_R = faces_meeting_R()
    n_faces_meeting_R = len(faces_R)
    R_membership = {}
    for N in (2, 3, 4):
        all_f1 = True
        all_f2 = True
        for (anchor, idx), owner_set in faces_R.items():
            f1_in, f2_in = face_family_membership(anchor, owner_set, N)
            all_f1 = all_f1 and f1_in
            all_f2 = all_f2 and f2_in
        R_membership[N] = {
            "all_82_in_F1": all_f1,
            "all_82_in_F2": all_f2,
            "both_families_retain_same_82": all_f1 and all_f2,
        }

    # --- Part C: max per-site sum, N=2,3,4 ---
    per_site = {}
    for N in (2, 3, 4):
        f1_max, f2_max = max_per_site_sum(N)
        per_site[N] = {
            "F1_max_per_site_over_abs_tau": str(f1_max),
            "F2_max_per_site_over_abs_tau": str(f2_max),
            "F1_le_28": f1_max <= 28,
            "F2_le_28": f2_max <= 28,
            "F1_attains_28": f1_max == 28,
            "F2_attains_28": f2_max == 28,
        }

    # --- Part D: AM2 contraction ---
    contraction = am2_contraction(tau_cap)

    # --- Part E: termination order ---
    primes = [2, 3, 5, 7, 11, 13, 17, 19]
    termination = {}
    for p in (1, 2, 3, 4):
        termination[p] = creation_algebra_termination_fixture(p, primes[:p])
    termination_order_8_confirmed = termination[4]["termination_order_2p"] and (2 * 4 == 8)

    # --- Part F: reset budget ---
    incident = incident_anchors_R()
    n_incident = len(incident)
    reset_budget = 2 * n_incident * 7  # units of |tau|
    reset_budget_expected = 98

    # --- Cross-checks against forward/reverse exported results.json ---
    fwd = load_json(FWD_RESULTS)
    rev = load_json(REV_RESULTS)

    fwd_audit2 = fwd["checks"][7]["audit"]["2"]
    fwd_audit3 = fwd["checks"][7]["audit"]["3"]

    cross_fwd = {
        "N2_faces_F1": fwd_audit2["faces_F1"] == box_reports[2]["faces_F1"],
        "N2_faces_F2": fwd_audit2["faces_F2"] == box_reports[2]["faces_F2"],
        "N2_extra": fwd_audit2["extra_F2_faces"] == box_reports[2]["extra_F2_minus_F1"],
        "N3_faces_F1": fwd_audit3["faces_F1"] == box_reports[3]["faces_F1"],
        "N3_faces_F2": fwd_audit3["faces_F2"] == box_reports[3]["faces_F2"],
        "N3_extra": fwd_audit3["extra_F2_faces"] == box_reports[3]["extra_F2_minus_F1"],
        "N2_faces_meeting_R_82": fwd_audit2["faces_meeting_R"] == n_faces_meeting_R,
        "reset_R_98": fwd["checks"][1]["aq2_reset_R"] == reset_budget,
        "incident_anchors_list": sorted(fwd["checks"][5]["incident_anchors"]) == sorted(list(map(list, incident))),
        "J0": F(fwd["checks"][8]["J_0"]) == F(7, 25000000),
        "G_R_upper": F(fwd["checks"][8]["G_R_upper"]) == F(148, 7),
        "self_map": F(fwd["checks"][8]["self_map"]) == F(contraction["self_map_J0_G_R"]),
        "exclusion": F(fwd["checks"][8]["exclusion"]) == F(contraction["exclusion_2J0_Gp_R"]),
        "termination_order_am2": fwd["checks"][1]["am2_termination_order"] == 8,
        "termination_fixture_qualitative_four_site_order8_matches_2p": (
            fwd["checks"][8]["termination_fixtures"]["four_site_order8"] == math.factorial(8)
            and fwd["checks"][8]["termination_fixtures"]["four_site_order9_zero"] is True
        ),
        "termination_fixture_qualitative_two_site_order4_matches_2p": (
            fwd["checks"][8]["termination_fixtures"]["two_site_order4"] == math.factorial(4)
            and fwd["checks"][8]["termination_fixtures"]["two_site_order5_zero"] is True
        ),
    }

    rev_boxes = rev["checks"][9]["boxes"]
    rev_box2 = rev_boxes["2"] if "2" in rev_boxes else rev_boxes[2]
    rev_box3 = rev_boxes["3"] if "3" in rev_boxes else rev_boxes[3]
    cross_rev = {
        "N2_B_sites": rev_box2["B_sites"] == box_reports[2]["B_sites"],
        "N2_am2_volume_sites_Bplus": rev_box2["am2_volume_sites"] == box_reports[2]["B_plus_sites"],
        "N2_partial_groups": rev_box2["F2_partial_groups"] == box_reports[2]["partial_groups"],
        "N2_reset_R_per_tau": int(rev_box2["padded_reset_R_per_tau"]) == reset_budget,
        "N2_padded_incident_groups_R": rev_box2["padded_incident_groups_R"] == n_incident,
        "N3_B_sites": rev_box3["B_sites"] == box_reports[3]["B_sites"],
        "N3_am2_volume_sites_Bplus": rev_box3["am2_volume_sites"] == box_reports[3]["B_plus_sites"],
        "N3_partial_groups": rev_box3["F2_partial_groups"] == box_reports[3]["partial_groups"],
    }

    overall_pass = bool(
        all(box_reports[N]["F1_matches_closed_form"] for N in (2, 3, 4))
        and all(box_reports[N]["F2_matches_closed_form"] for N in (2, 3, 4))
        and all(box_reports[N]["extra_matches_closed_form"] for N in (2, 3, 4))
        and n_faces_meeting_R == 82
        and all(R_membership[N]["both_families_retain_same_82"] for N in (2, 3, 4))
        and all(per_site[N]["F1_le_28"] and per_site[N]["F2_le_28"] for N in (2, 3, 4))
        and all(per_site[N]["F1_attains_28"] and per_site[N]["F2_attains_28"] for N in (2, 3, 4))
        and contraction["exp_1_8_lt_8_7"]
        and contraction["G_R_matches"] and contraction["Gp_R_matches"]
        and contraction["J0_matches"]
        and contraction["self_map_matches"] and contraction["self_map_lt_1_64"]
        and contraction["exclusion_matches"] and contraction["exclusion_lt_1"]
        and contraction["mpmath_cross_check"]["exp_1_8_lt_8_7"]
        and (contraction["flint_arb_cross_check"] is None or contraction["flint_arb_cross_check"]["arb_exp_1_8_lt_8_7"])
        and termination_order_8_confirmed
        and all(termination[p]["termination_order_2p"] for p in (1, 2, 3, 4))
        and n_incident == 7
        and reset_budget == reset_budget_expected
        and all(cross_fwd.values())
        and all(cross_rev.values())
    )

    result = {
        "script": "padding_family_contraction.py",
        "zero_research_loops": True,
        "arithmetic": "fractions.Fraction for all pass/fail comparisons; mpmath and (if available) python-flint Arb for labelled numerical cross-checks only",
        "box_enumeration": box_reports,
        "faces_meeting_R": {
            "n_faces_meeting_R": n_faces_meeting_R,
            "expected_82": n_faces_meeting_R == 82,
            "by_N": R_membership,
        },
        "max_per_site_sum": per_site,
        "am2_contraction": contraction,
        "termination_order": {str(p): v for p, v in termination.items()},
        "termination_order_8_confirmed_for_p4": termination_order_8_confirmed,
        "reset_budget": {
            "incident_anchors": sorted(list(map(list, incident))),
            "n_incident_anchors": n_incident,
            "n_incident_expected_7": n_incident == 7,
            "reset_budget_over_abs_tau": reset_budget,
            "reset_budget_expected_98": reset_budget_expected,
            "matches": reset_budget == reset_budget_expected,
        },
        "cross_check_forward": cross_fwd,
        "cross_check_reverse": cross_rev,
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
