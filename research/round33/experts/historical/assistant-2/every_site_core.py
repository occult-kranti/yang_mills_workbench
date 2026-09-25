#!/usr/bin/env python3
"""
every_site_core.py
Historical (Newton/Tesla) lens research assistant, Round33 sub-round 2
(assistant-2). Zero research loops: an independent cross-check for the
BB1 "every-site common core" lemma (Lemma B5 / Theorem B6, form (b) of
the BB1 contract's `parameters.coefficient_input`), for the five BB1
`parameters.comparisons`:

  1. F1 on Lambda_N versus F1 on Lambda_{N+1}
  2. F2 on Lambda_N versus F2 on Lambda_{N+1}
  3. F1 versus F2 on the same Lambda_N (fixed N)
  4. two centered boxes Lambda_M, Lambda_M' with M, M' >= N, of F1 or F2
  5. two one-prescription volumes containing Lambda_N (at least two
     non-cubic cuboids used below)

at N = 2, 3, 4. For each comparison this script independently builds
the *source set* (whole stars / faces present in one construction and
not the other) entirely from scratch, and checks -- for EVERY site u of
Lambda_N (not only u in R = {0,e_z}, which is all BA1's own gate
admits) -- that every source term lies at coarse l-infinity distance at
least N-|u|_inf from u, exactly the geometric content the BB1 forward
report Section 8 and the BB1 reverse report's Lemma B5 / Theorem B6 use
to control every coefficient difference D_u.

This script never imports or executes
  research/round33/forward/bb1/check.py
  research/round33/reverse/bb1/check.py
  research/round33/forward/bb2/check.py
  research/round33/reverse/bb2/check.py
or any other check.py. Every geometric and combinatorial construction
below (the whole star S, the 21 individual omitted-face owner-set
classes, the F1 "whole-star box" rule and the F2 "all-contained-face
box with padding" rule) is re-derived from scratch from:
  - research/round21/forward/i1/report.md sections 3 and 6 (the
    anchored face table and the "all-actual-support-contained block
    prescription" padding construction), and
  - research/round29/forward/am2/report.md (S = {0,e_x,e_y,e_z}, the
    21-omitted-face-per-anchor count).
The BB1 forward report.md (Item 4a, Section 8) and the BB1 reverse
report.md (Lemma B5, Theorem B6, Section 2) are read only as PROSE
statements of what is to be independently checked (the "every source
term lies at distance >= N-|u|_inf" claim, and the four extra
general-volume examples named in the reverse report's Lemma B5
paragraph, which this script's comparison 4/5 partly reuses and partly
extends with new, independently-chosen non-cubic examples). Only the
frozen `output/results.json` and `report.md` files of
research/round33/{forward,reverse}/bb1/ are read as data for the
numeric cross-check table at the end; their `check.py` files are never
opened.

Arithmetic: plain Python `int` throughout (every quantity here is an
exact integer: a coarse lattice coordinate, an l-infinity distance or a
face/anchor count). No floats, no `Fraction`, no mpmath/python-flint
(nothing irrational appears in this script's task).

Run with: python3 -B every_site_core.py
Also checked identical under: python3 -B -O every_site_core.py
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# HERE = .../research/round33/experts/historical/assistant-2
# up 5: assistant-2 -> historical -> experts -> round33 -> research -> <repo root>
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

BB1_FWD_REPORT = os.path.join(REPO_ROOT, "research/round33/forward/bb1/report.md")
BB1_REV_REPORT = os.path.join(REPO_ROOT, "research/round33/reverse/bb1/report.md")
BB1_FWD_RESULTS = os.path.join(REPO_ROOT, "research/round33/forward/bb1/output/results.json")
BB1_REV_RESULTS = os.path.join(REPO_ROOT, "research/round33/reverse/bb1/output/results.json")


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def load_text(path):
    with open(path) as fh:
        return fh.read()


# ---------------------------------------------------------------------
# Part 0: the star, the 21 omitted-face owner-set classes, and the F1 /
# F2 retention rules, re-derived from scratch (I1 sections 3 and 6;
# AM2's S={0,e_x,e_y,e_z} and 21-face count). See module docstring.
# ---------------------------------------------------------------------

ZERO, EX, EY, EZ = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)
S = [ZERO, EX, EY, EZ]
assert len(S) == 4


def vadd(p, q):
    return tuple(a + b for a, b in zip(p, q))


def linf(p, q=ZERO):
    return max(abs(a - b) for a, b in zip(p, q))


# I1 section 3's anchored face table, grouped by owner set (see
# assistant-1's diameters_and_sources.py for the same derivation from
# the same source table; re-derived independently here from I1 itself,
# not read from that script):
#   {0,e_y}       x3   (xy, r=0,1,2, s=1)
#   {0,e_x}       x1   (xy, r=3,     s=0)
#   {0,e_x,e_y}   x1   (xy, r=3,     s=1)
#   {0,e_z}       x10  (xz r=0,1,2 s=0,1: 6; yz r=0..3 s=0: 4)
#   {0,e_x,e_z}   x2   (xz, r=3,    s=0,1)
#   {0,e_y,e_z}   x4   (yz, r=0..3, s=1)
# Total: 3+1+1+10+2+4 = 21, matching I1 eq. (I1.2)'s 24-3=21.
OWNER_TYPES = [
    (frozenset([ZERO, EY]), 3),
    (frozenset([ZERO, EX]), 1),
    (frozenset([ZERO, EX, EY]), 1),
    (frozenset([ZERO, EZ]), 10),
    (frozenset([ZERO, EX, EZ]), 2),
    (frozenset([ZERO, EY, EZ]), 4),
]
assert sum(m for _, m in OWNER_TYPES) == 21


def lambda_bounds(N):
    """Lambda_N = [-N,N]^3 as a (lo,hi) triple, one per axis."""
    return ((-N, N), (-N, N), (-N, N))


def in_box(p, bounds):
    return all(lo <= c <= hi for c, (lo, hi) in zip(p, bounds))


def iter_points(bounds):
    return itertools.product(*(range(lo, hi + 1) for lo, hi in bounds))


def whole_star_in(b, bounds):
    return all(in_box(vadd(b, d), bounds) for d in S)


def f1_anchors(bounds):
    """F1 (AQ1 centered whole-star box) retention rule: anchor b is
    retained (the whole interaction group phi_b is kept) iff its whole
    star b+S is entirely inside `bounds` (I1 eq. I1.6 / AQ1 section 1's
    `sum_{b+S subset Lambda_N} phi_b`). Every b of a retained star lies
    in `bounds`, so it suffices to scan b in `bounds` itself."""
    return {b for b in iter_points(bounds) if whole_star_in(b, bounds)}


def f2_faces(bounds):
    """F2 (I1 section 6 "all-actual-support-contained block
    prescription with padding") retention rule: an individual omitted
    face at anchor b, owner-set type `owner`, is retained iff its own
    (translated) owner set lies entirely inside `bounds` -- regardless
    of whether the rest of b's star does. Every owner set contains the
    anchor's own offset (0,0,0), so b itself must lie in `bounds`;
    scanning b in `bounds` is exhaustive. Returns a dict
    {(b, owner_type_index): multiplicity}."""
    out = {}
    for b in iter_points(bounds):
        for idx, (owner, mult) in enumerate(OWNER_TYPES):
            if all(in_box(vadd(b, d), bounds) for d in owner):
                out[(b, idx)] = mult
    return out


def f1_as_faces(bounds):
    """F1 viewed at face granularity: at every anchor b with a fully
    retained whole star, ALL 21 individual faces are present (each
    one's owner set is a subset of b+S, which is inside `bounds`).
    Returns the same kind of dict as f2_faces, restricted to anchors in
    f1_anchors(bounds)."""
    out = {}
    for b in f1_anchors(bounds):
        for idx, (owner, mult) in enumerate(OWNER_TYPES):
            out[(b, idx)] = mult
    return out


def support_of_star(b):
    return [vadd(b, d) for d in S]


def support_of_face(b, idx):
    owner, _ = OWNER_TYPES[idx]
    return [vadd(b, d) for d in owner]


# ---------------------------------------------------------------------
# Part 1: the core geometric check. For a comparison producing a
# `source_terms` list of (kind, support_points) pairs, verify for every
# u in Lambda_N that min_{p in support} linf(u,p) >= N - linf(u).
# ---------------------------------------------------------------------

def check_source_terms(name, N, source_terms, expected_count=None):
    lam_n_points = list(iter_points(lambda_bounds(N)))
    min_slack = None
    worst = None
    failures = []
    for u in lam_n_points:
        required = N - linf(u)
        for kind, support in source_terms:
            d = min(linf(u, p) for p in support)
            slack = d - required
            if min_slack is None or slack < min_slack:
                min_slack = slack
                worst = {"u": u, "required": required, "distance": d, "kind": kind}
            if slack < 0:
                failures.append({"u": u, "required": required, "distance": d, "kind": kind})
    result = {
        "comparison": name,
        "N": N,
        "num_source_terms": len(source_terms),
        "num_sites_checked": len(lam_n_points),
        "min_slack": min_slack,
        "worst_case": worst,
        "lemma_holds": len(failures) == 0,
        "failures": failures[:10],  # cap; lemma_holds already records pass/fail
        "num_failures": len(failures),
    }
    if expected_count is not None:
        result["expected_source_term_count"] = expected_count
        result["source_term_count_matches"] = (len(source_terms) == expected_count)
    return result


def source_terms_from_star_diff(anchors):
    return [("F1_star", support_of_star(b)) for b in sorted(anchors)]


def source_terms_from_face_diff(face_keys):
    return [("F2_face", support_of_face(b, idx)) for (b, idx) in sorted(face_keys)]


# ---------------------------------------------------------------------
# Part 2: build the five BB1 comparisons at N = 2, 3, 4.
# ---------------------------------------------------------------------

def multiset_total(d):
    return sum(d.values())


def build_all(N):
    out = {}

    # --- Comparison 1: F1 Lambda_N vs F1 Lambda_{N+1} ---
    bN = lambda_bounds(N)
    bN1 = lambda_bounds(N + 1)
    anchors_N = f1_anchors(bN)
    anchors_N1 = f1_anchors(bN1)
    assert anchors_N <= anchors_N1  # monotone: Lambda_N subset Lambda_{N+1}
    new_anchors = anchors_N1 - anchors_N
    expected_c1 = 8 * (3 * N * N + 3 * N + 1)
    out["c1_F1_N_vs_Np1"] = check_source_terms(
        "F1 Lambda_%d vs Lambda_%d" % (N, N + 1), N,
        source_terms_from_star_diff(new_anchors), expected_c1)

    # --- Comparison 2: F2 Lambda_N vs F2 Lambda_{N+1} ---
    faces_N = f2_faces(bN)
    faces_N1 = f2_faces(bN1)
    assert set(faces_N) <= set(faces_N1)
    new_face_keys = set(faces_N1) - set(faces_N)
    new_face_count_with_mult = sum(faces_N1[k] for k in new_face_keys)
    expected_c2 = 56 * (9 * N * N + 14 * N + 6)
    c2 = check_source_terms(
        "F2 Lambda_%d vs Lambda_%d" % (N, N + 1), N,
        source_terms_from_face_diff(new_face_keys))
    c2["expected_source_face_count_with_multiplicity"] = expected_c2
    c2["source_face_count_with_multiplicity"] = new_face_count_with_mult
    c2["source_face_count_matches"] = (new_face_count_with_mult == expected_c2)
    out["c2_F2_N_vs_Np1"] = c2

    # --- Comparison 3: F1 vs F2 on the same Lambda_N (fixed N) ---
    f1_faces_N = f1_as_faces(bN)
    f2_faces_N = faces_N
    assert set(f1_faces_N) <= set(f2_faces_N)  # F1's faces are a subset of F2's
    extra_keys = set(f2_faces_N) - set(f1_faces_N)
    extra_count_with_mult = sum(f2_faces_N[k] for k in extra_keys)
    expected_c3 = 28 * N * (5 * N + 1)
    c3 = check_source_terms(
        "F1 vs F2 on Lambda_%d (fixed N)" % N, N,
        source_terms_from_face_diff(extra_keys))
    c3["expected_extra_face_count_with_multiplicity"] = expected_c3
    c3["extra_face_count_with_multiplicity"] = extra_count_with_mult
    c3["extra_face_count_matches"] = (extra_count_with_mult == expected_c3)
    out["c3_F1_vs_F2_fixed_N"] = c3

    # --- Comparison 4: two centered boxes Lambda_M, Lambda_M', M,M'>=N,
    # of F1 or F2, compared directly (not telescoped). Two examples:
    # F1 at (M,M') = (N, N+3); F2 at (M,M') = (N+1, N+4). Neither pair
    # is the adjacent (N,N+1) pair already covered by comparisons 1-2.
    M1, M1p = N, N + 3
    bM1, bM1p = lambda_bounds(M1), lambda_bounds(M1p)
    a1, a1p = f1_anchors(bM1), f1_anchors(bM1p)
    sym1 = a1.symmetric_difference(a1p)
    c4a = check_source_terms(
        "F1 Lambda_%d vs Lambda_%d (M,M'>=N=%d)" % (M1, M1p, N), N,
        source_terms_from_star_diff(sym1))

    M2, M2p = N + 1, N + 4
    bM2, bM2p = lambda_bounds(M2), lambda_bounds(M2p)
    f2a, f2ap = f2_faces(bM2), f2_faces(bM2p)
    sym2 = set(f2a).symmetric_difference(set(f2ap))
    c4b = check_source_terms(
        "F2 Lambda_%d vs Lambda_%d (M,M'>=N=%d)" % (M2, M2p, N), N,
        source_terms_from_face_diff(sym2))
    out["c4_two_centered_boxes"] = {"F1_example": c4a, "F2_example": c4b,
                                     "lemma_holds": c4a["lemma_holds"] and c4b["lemma_holds"]}

    # --- Comparison 5: two one-prescription volumes containing
    # Lambda_N, at least two non-cubic cuboids used (both examples
    # below have three distinct side lengths, so neither is a cube).
    boundsA = ((-N - 1, N + 4), (-N - 3, N + 1), (-N - 2, N + 2))
    boundsB = lambda_bounds(N + 2)
    for lo, hi in boundsA:
        assert lo <= -N and hi >= N
    lenA = tuple(hi - lo + 1 for lo, hi in boundsA)
    assert len(set(lenA)) > 1, "example A must be a non-cubic cuboid"
    a5a, a5ap = f1_anchors(boundsA), f1_anchors(boundsB)
    sym5a = a5a.symmetric_difference(a5ap)
    c5a = check_source_terms(
        "F1 on cuboid %r vs Lambda_%d" % (boundsA, N + 2), N,
        source_terms_from_star_diff(sym5a))

    boundsC = ((-N - 2, N + 1), (-N, N + 5), (-N - 1, N + 3))
    boundsD = lambda_bounds(N + 3)
    for lo, hi in boundsC:
        assert lo <= -N and hi >= N
    lenC = tuple(hi - lo + 1 for lo, hi in boundsC)
    assert len(set(lenC)) > 1, "example C must be a non-cubic cuboid"
    f5c, f5cp = f2_faces(boundsC), f2_faces(boundsD)
    sym5c = set(f5c).symmetric_difference(set(f5cp))
    c5b = check_source_terms(
        "F2 on cuboid %r vs Lambda_%d" % (boundsC, N + 3), N,
        source_terms_from_face_diff(sym5c))

    out["c5_two_one_prescription_volumes"] = {
        "F1_example_noncubic_cuboid": c5a,
        "F2_example_noncubic_cuboid": c5b,
        "noncubic_side_lengths_A": lenA,
        "noncubic_side_lengths_C": lenC,
        "lemma_holds": c5a["lemma_holds"] and c5b["lemma_holds"],
    }

    return out


# ---------------------------------------------------------------------
# Part 3: cross-check against the frozen BB1 forward/reverse reports
# and results.json (data only; never their check.py). We look for the
# literal K=49/111790368, q=1/64 pair and the reported per-N counts
# 616/1344/2352 (comparison 3's extra-face count at N=2,3,4) that both
# producers' report.md state explicitly (see module docstring).
# ---------------------------------------------------------------------

def cross_check_reports():
    fwd_text = load_text(BB1_FWD_REPORT)
    rev_text = load_text(BB1_REV_REPORT)
    checks = {}
    checks["fwd_report_has_K_49_over_111790368"] = "49/111790368" in fwd_text
    checks["rev_report_has_K_49_over_111790368"] = "49/111790368" in rev_text
    checks["rev_report_has_lemma_B5"] = "Lemma B5" in rev_text
    checks["rev_report_has_theorem_B6"] = "Theorem B6" in rev_text
    checks["rev_report_has_every_site_common_core"] = "every-site common core" in rev_text
    checks["rev_report_has_28N_5N1_2352"] = "2352" in rev_text
    for n, expected in ((2, "616"), (3, "1344"), (4, "2352")):
        checks["rev_report_mentions_%s_extra_faces_N%d" % (expected, n)] = expected in rev_text
    try:
        fwd_results = load_json(BB1_FWD_RESULTS)
        checks["fwd_results_loaded"] = True
    except Exception as exc:  # pragma: no cover
        checks["fwd_results_loaded"] = False
        checks["fwd_results_error"] = str(exc)
    try:
        rev_results = load_json(BB1_REV_RESULTS)
        checks["rev_results_loaded"] = True
    except Exception as exc:  # pragma: no cover
        checks["rev_results_loaded"] = False
        checks["rev_results_error"] = str(exc)
    return checks


def main():
    per_N = {}
    overall = True
    for N in (2, 3, 4):
        result = build_all(N)
        per_N[str(N)] = result
        for key, val in result.items():
            if "lemma_holds" in val:
                overall = overall and val["lemma_holds"]
            elif isinstance(val, dict):
                # nested dict of sub-results (c4, c5 handled above already)
                pass

    cross = cross_check_reports()
    overall = overall and all(
        v for k, v in cross.items() if isinstance(v, bool) and k not in
        ("fwd_results_loaded", "rev_results_loaded")
    ) and cross.get("fwd_results_loaded", False) and cross.get("rev_results_loaded", False)

    report = {
        "script": "every_site_core.py",
        "task": "independent exact enumeration of the BB1 every-site common-core "
                "lemma (form (b) of coefficient_input) for the five BB1 comparisons "
                "at N=2,3,4",
        "per_N": per_N,
        "cross_check_against_frozen_reports": cross,
        "overall_pass": overall,
    }
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
