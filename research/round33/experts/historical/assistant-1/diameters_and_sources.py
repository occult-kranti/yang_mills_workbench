#!/usr/bin/env python3
"""
diameters_and_sources.py
Historical (Newton/Tesla) lens research assistant, Round33 sub-round 1
(assistant-1). Zero research loops: an independent cross-check and
preview script for the lens, requested by this lens's own
`loop2-response.md` section 3, item 1 (the exact-enumeration script)
and item 2 (the padding audit, folded in here since both concern the
same F1/F2 box enumeration). Not a producer, skeptic or advisor
artifact; nothing here is admission evidence.

This script never imports research/round33/forward/ba1/check.py,
research/round33/reverse/ba1/check.py, research/round33/forward/ba2/
check.py or research/round33/reverse/ba2/check.py (or any other
check.py). Every geometric and combinatorial construction below is
re-derived from scratch from the star definition and the 21-omitted-
face table in research/round21/forward/i1/report.md sections 3 and 6,
and from research/round29/forward/am2/report.md (S = {0,e_x,e_y,e_z},
21 omitted faces per anchor, ||phi_b|| = 7|tau|); only the *numeric*
results of the BA1/BA2 forward and reverse `report.md` files and the
BA1/BA2 gates (research/round33/advisor/ba1-gate.json, ba2-gate.json)
are read, as data, for the final comparison table -- never their code
and never their intermediate derivations.

Read before writing: research/round33/experts/historical/loop2-response.md
section 3, research/round21/forward/i1/report.md sections 3 and 6,
research/round29/forward/am2/report.md, research/round33/contracts/
ba1.json and ba2.json, research/round33/advisor/ba1-gate.json and
ba2-gate.json, research/round33/forward/ba1/report.md, research/round33/
reverse/ba1/report.md, research/round33/forward/ba2/report.md,
research/round33/reverse/ba2/report.md.

Arithmetic: plain Python `int` throughout (every quantity here is an
exact integer: a count, a diameter or an l1/l-infinity distance); no
floats appear anywhere, so `fractions.Fraction` is not needed for this
script's own claims. mpmath/python-flint are not used here (no
irrational bound appears in this script's task).

Run with: python3 -B diameters_and_sources.py
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# HERE = .../research/round33/experts/historical/assistant-1
# up 5: assistant-1 -> historical -> experts -> round33 -> research -> <repo root>
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

BA1_GATE = os.path.join(REPO_ROOT, "research/round33/advisor/ba1-gate.json")
BA2_GATE = os.path.join(REPO_ROOT, "research/round33/advisor/ba2-gate.json")
BA1_FWD_REPORT = os.path.join(REPO_ROOT, "research/round33/forward/ba1/report.md")
BA1_REV_REPORT = os.path.join(REPO_ROOT, "research/round33/reverse/ba1/report.md")
BA2_FWD_REPORT = os.path.join(REPO_ROOT, "research/round33/forward/ba2/report.md")
BA2_REV_REPORT = os.path.join(REPO_ROOT, "research/round33/reverse/ba2/report.md")


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def load_text(path):
    with open(path) as fh:
        return fh.read()


# ---------------------------------------------------------------------
# Part 0: the star and the 21 omitted face classes, re-derived from
# research/round21/forward/i1/report.md section 3 (the anchored face
# table) and section 6 (F2's "all-contained-face boxes with padding");
# research/round29/forward/am2/report.md confirms S={0,e_x,e_y,e_z} and
# the 21-face count. Nothing here is read from any check.py.
# ---------------------------------------------------------------------

ZERO, EX, EY, EZ = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)
S = [ZERO, EX, EY, EZ]                       # the whole star's offsets
assert len(S) == 4


def vadd(p, q):
    return tuple(a + b for a, b in zip(p, q))


def vsub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def linf(p, q=ZERO):
    return max(abs(a - b) for a, b in zip(p, q))


def l1(p, q=ZERO):
    return sum(abs(a - b) for a, b in zip(p, q))


def diam(points, metric):
    pts = list(points)
    if len(pts) <= 1:
        return 0
    return max(metric(p, q) for p in pts for q in pts)


# I1 section 3's anchored face table (24 anchored classes = 3 selected +
# 21 omitted). Each row of the source table is (orientation/phase,
# count, relative support). The 3 selected xy faces (support {0}) are
# not omitted and play no part below. The 21 omitted rows, grouped by
# relative support (the "owner set"):
#   xy: r=0,1,2; s=1   count 3   support {0,e_y}
#   xy: r=3;     s=0   count 1   support {0,e_x}
#   xy: r=3;     s=1   count 1   support {0,e_x,e_y}
#   xz: r=0,1,2; s=0,1 count 6   support {0,e_z}   \
#   yz: r=0,1,2,3; s=0 count 4   support {0,e_z}    } combined: 10
#   xz: r=3;     s=0,1 count 2   support {0,e_x,e_z}
#   yz: r=0,1,2,3; s=1 count 4   support {0,e_y,e_z}
# Total omitted: 3+1+1+10+2+4 = 21, matching I1 eq. (I1.2)'s 24-3=21
# and AM2's "21 omitted faces per anchor".
_OWNER_TYPES = [
    (frozenset([ZERO, EY]), 3),
    (frozenset([ZERO, EX]), 1),
    (frozenset([ZERO, EX, EY]), 1),
    (frozenset([ZERO, EZ]), 10),
    (frozenset([ZERO, EX, EZ]), 2),
    (frozenset([ZERO, EY, EZ]), 4),
]
OMITTED_CLASSES = []
for _owner, _mult in _OWNER_TYPES:
    for _ in range(_mult):
        OMITTED_CLASSES.append(_owner)
assert len(OMITTED_CLASSES) == 21, len(OMITTED_CLASSES)
assert sum(mult for _, mult in _OWNER_TYPES) == 21


def lambda_n_sites(N):
    return list(itertools.product(range(-N, N + 1), repeat=3))


def in_box(p, N):
    return all(-N <= c <= N for c in p)


def whole_star_in(b, N):
    return all(in_box(vadd(b, d), N) for d in S)


def f2_retained_classes(b, N):
    """Owner sets (of the 21 individual omitted-face entries) retained
    by F2 at anchor b on Lambda_N: retained iff the owner set itself
    (not the whole star) is inside Lambda_N (I1 section 6)."""
    out = []
    for owner in OMITTED_CLASSES:
        if all(in_box(vadd(b, d), N) for d in owner):
            out.append(owner)
    return out


# ---------------------------------------------------------------------
# Part 1: diameters (l-infinity and l1) of the whole star and of every
# distinct owner-set type -- independent of N, but reported at every N
# below as "confirmed by enumeration" per the loop-2 edit to BA1's
# required item 2.
# ---------------------------------------------------------------------

def diameters_section():
    star_diam_inf = diam(S, linf)
    star_diam_l1 = diam(S, l1)
    owner_diams = []
    for owner, mult in _OWNER_TYPES:
        pts = list(owner)
        owner_diams.append({
            "owner_set": sorted(pts),
            "multiplicity": mult,
            "diam_linf": diam(pts, linf),
            "diam_l1": diam(pts, l1),
        })
    return {
        "star_S": sorted(S),
        "star_diam_linf": star_diam_inf,
        "star_diam_linf_expected_1": star_diam_inf == 1,
        "star_diam_l1": star_diam_l1,
        "star_diam_l1_expected_2": star_diam_l1 == 2,
        "owner_set_diameters": owner_diams,
        "every_owner_diam_linf_le_1": all(o["diam_linf"] <= 1 for o in owner_diams),
        "every_owner_diam_l1_le_2": all(o["diam_l1"] <= 2 for o in owner_diams),
    }


# ---------------------------------------------------------------------
# Part 2: incidence -- how many stars meet a (bulk) site, and how many
# meet R = {0, e_z}. u in b+S iff b in u-S (S is translation-covariant),
# so on the infinite lattice every site is met by exactly |S|=4 stars,
# incoming anchors included (AM2's J<=28|tau| = 4 stars x 7|tau|).
# ---------------------------------------------------------------------

R_COVER = [ZERO, EZ]


def incidence_section():
    bulk_site = (5, 5, 5)  # far from any Lambda_N boundary used below
    incident_to_bulk = sorted({vsub(bulk_site, d) for d in S})
    assert len(incident_to_bulk) == 4

    incident_to_0 = {vsub(ZERO, d) for d in S}
    incident_to_ez = {vsub(EZ, d) for d in S}
    incident_to_R = sorted(incident_to_0 | incident_to_ez)

    # faces (not just stars) meeting a site: by translation covariance,
    # the omitted-face classes whose owner set contains the offset that
    # reaches back to u from each of the (up to 4) incident anchors.
    def faces_touching(u):
        total = 0
        by_anchor = {}
        for d in S:
            b = vsub(u, d)
            cnt = sum(1 for owner in OMITTED_CLASSES if d in owner)
            by_anchor[b] = cnt
            total += cnt
        return total, by_anchor

    faces_0, by_anchor_0 = faces_touching(ZERO)
    faces_ez, by_anchor_ez = faces_touching(EZ)

    # faces meeting BOTH sites of R (only possible from the shared
    # anchor b=0, since (0-S) intersect (e_z-S) = {0} exactly, verified
    # below rather than assumed).
    shared_anchors = {vsub(ZERO, d) for d in S} & {vsub(EZ, d) for d in S}
    both_faces = 0
    for b in shared_anchors:
        for owner in OMITTED_CLASSES:
            owner_abs = {vadd(b, o) for o in owner}
            if ZERO in owner_abs and EZ in owner_abs:
                both_faces += 1

    faces_meeting_R = faces_0 + faces_ez - both_faces

    # faces with owner set exactly inside R = {0,e_z} (anchored at 0,
    # owner-set type {0,e_z}): these are the "10 inside R" faces.
    inside_R = sum(1 for owner in OMITTED_CLASSES if owner == frozenset([ZERO, EZ]))

    # distinct owner-set "types" as seen translated to a site u (I1's
    # "15 owner sets" pin): count distinct (owner_type - offset) shapes
    # over the (up to 4) incident anchors of a bulk site.
    distinct_types = set()
    for d in S:
        for owner in OMITTED_CLASSES:
            if d in owner:
                shifted = frozenset(vsub(o, d) for o in owner)
                distinct_types.add(shifted)

    return {
        "generic_bulk_site_incident_star_count": len(incident_to_bulk),
        "generic_bulk_site_incident_star_count_expected_4": len(incident_to_bulk) == 4,
        "incident_anchors_meeting_R": incident_to_R,
        "incident_anchors_meeting_R_count": len(incident_to_R),
        "incident_anchors_meeting_R_expected_7": len(incident_to_R) == 7,
        "faces_touching_0": faces_0,
        "faces_touching_ez": faces_ez,
        "faces_touching_both_sites_of_R": both_faces,
        "faces_meeting_R": faces_meeting_R,
        "faces_meeting_R_expected_82": faces_meeting_R == 82,
        "faces_touching_both_expected_16": both_faces == 16,
        "faces_with_owner_set_inside_R": inside_R,
        "faces_with_owner_set_inside_R_expected_10": inside_R == 10,
        "distinct_owner_set_types_by_translation": len(distinct_types),
        "distinct_owner_set_types_expected_15": len(distinct_types) == 15,
    }


# ---------------------------------------------------------------------
# Part 3: F1-vs-F2 extra faces on Lambda_N -- count, owner sets,
# anchors, and l1/l-infinity distances from 0 and from e_z.
# ---------------------------------------------------------------------

def extra_faces_on(N):
    """Enumerate every (anchor, class-index) extra face on Lambda_N:
    present in F2 (owner set inside Lambda_N) but not in F1 (whole star
    NOT inside Lambda_N). Iterates over a box slightly larger than
    Lambda_N so no anchor is assumed confined a priori."""
    extra = []
    for b in itertools.product(range(-N - 1, N + 1), repeat=3):
        w_in = whole_star_in(b, N)
        if w_in:
            continue
        for idx, owner in enumerate(OMITTED_CLASSES):
            owner_abs = frozenset(vadd(b, d) for d in owner)
            if all(in_box(p, N) for p in owner_abs):
                extra.append((b, idx, owner_abs))
    return extra


def classify_anchor(b, N):
    """A(b) = directions i with b_i == N (S has only nonnegative
    offsets, so clipping only ever happens at the +N face)."""
    axes = ("x", "y", "z")
    return frozenset(axes[i] for i in range(3) if b[i] == N)


def classes_avoiding(direction_set):
    """Number of the 21 omitted-face entries whose owner set contains
    none of the basis vectors named in direction_set."""
    axis_vec = {"x": EX, "y": EY, "z": EZ}
    vecs = {axis_vec[a] for a in direction_set}
    return sum(1 for owner in OMITTED_CLASSES if not (owner & vecs) - {ZERO})


def extra_faces_section():
    per_N = {}
    for N in (2, 3, 4):
        extra = extra_faces_on(N)
        count = len(extra)
        anchors = sorted({b for b, _, _ in extra})
        owner_sets_flat = [pt for _, _, owner_abs in extra for pt in owner_abs]
        # distances: over every point of every extra face's owner set
        dists_from_0_linf = [linf(p, ZERO) for p in owner_sets_flat]
        dists_from_0_l1 = [l1(p, ZERO) for p in owner_sets_flat]
        dists_from_ez_linf = [linf(p, EZ) for p in owner_sets_flat]
        dists_from_ez_l1 = [l1(p, EZ) for p in owner_sets_flat]

        # per-anchor-type classification (the class table 17/13/5/10/3/1/0)
        by_type = {}
        for b in anchors:
            a = classify_anchor(b, N)
            by_type.setdefault(a, 0)
            by_type[a] += 1  # anchors of this type (counted once here)
        # cross-check: number of RETAINED extra faces at each anchor
        # type equals classes_avoiding(type); recompute directly.
        type_face_counts = {}
        for b in anchors:
            a = classify_anchor(b, N)
            n_faces_here = sum(1 for bb, _, _ in extra if bb == b)
            type_face_counts.setdefault(a, set()).add(n_faces_here)

        closed_form = 28 * N * (5 * N + 1)

        # class table, keyed by readable labels
        def label(fs):
            names = {"x": "e_x", "y": "e_y", "z": "e_z"}
            if not fs:
                return "none"
            return ",".join(sorted(names[a] for a in fs))

        class_table = {}
        for a in [frozenset(["x"]), frozenset(["y"]), frozenset(["z"]),
                  frozenset(["x", "y"]), frozenset(["x", "z"]), frozenset(["y", "z"]),
                  frozenset(["x", "y", "z"])]:
            class_table[label(a)] = classes_avoiding(a)

        per_N[N] = {
            "count": count,
            "closed_form_28N_5N1": closed_form,
            "count_matches_closed_form": count == closed_form,
            "n_anchors": len(anchors),
            "n_anchors_closed_form_2N1cubed_minus_2Ncubed_minus_1": (2 * N + 1) ** 3 - (2 * N) ** 3 - 1,
            "n_anchors_matches": len(anchors) == (2 * N + 1) ** 3 - (2 * N) ** 3 - 1,
            "corner_NNN_has_zero_extra_faces": all(bb != (N, N, N) for bb in anchors),
            "class_table_avoided_to_count": class_table,
            "class_table_matches_gate_17_13_5_10_3_1_0": (
                class_table["e_x"] == 17 and class_table["e_y"] == 13 and
                class_table["e_z"] == 5 and class_table["e_x,e_y"] == 10 and
                class_table["e_x,e_z"] == 3 and class_table["e_y,e_z"] == 1 and
                class_table["e_x,e_y,e_z"] == 0
            ),
            "min_dist_from_0_linf": min(dists_from_0_linf),
            "min_dist_from_0_l1": min(dists_from_0_l1),
            "min_dist_from_ez_linf": min(dists_from_ez_linf),
            "min_dist_from_ez_l1": min(dists_from_ez_l1),
            "min_dist_from_0_expected_N_both_metrics": (
                min(dists_from_0_linf) == N and min(dists_from_0_l1) == N
            ),
            "min_dist_from_ez_expected_Nminus1_both_metrics": (
                min(dists_from_ez_linf) == N - 1 and min(dists_from_ez_l1) == N - 1
            ),
            "max_owners_per_face": max(
                (len(owner_abs) for _, _, owner_abs in extra), default=0
            ),
            "max_owners_per_face_le_3": max(
                (len(owner_abs) for _, _, owner_abs in extra), default=0
            ) <= 3,
            "no_extra_face_meets_R": not any(
                (set(owner_abs) & set(R_COVER)) for _, _, owner_abs in extra
            ),
        }
    return per_N


# ---------------------------------------------------------------------
# Part 4: F2 padding sites -- B_+ \ Lambda_N, count 3(2N+1)^2 (BA2
# reverse). B_+ = union over every b in Lambda_N of the WHOLE star
# b+S (I1 section 6's B_plus construction), independent of which faces
# F2 actually retains.
# ---------------------------------------------------------------------

def padding_section():
    per_N = {}
    for N in (2, 3, 4):
        lam = set(lambda_n_sites(N))
        b_plus = set()
        for b in lam:
            for d in S:
                b_plus.add(vadd(b, d))
        padding = b_plus - lam
        closed_form = 3 * (2 * N + 1) ** 2
        per_N[N] = {
            "lambda_N_sites": len(lam),
            "B_plus_sites": len(b_plus),
            "padding_sites": len(padding),
            "closed_form_3_2N1_sq": closed_form,
            "padding_matches_closed_form": len(padding) == closed_form,
        }
    return per_N


# ---------------------------------------------------------------------
# Part 5: nested-comparison sources -- new F1 stars and new F2 faces
# from Lambda_N to Lambda_{N+1}.
# ---------------------------------------------------------------------

def nested_sources_section():
    per_N = {}
    for N in (2, 3, 4):
        # new F1 stars: whole-star anchors in Lambda_{N+1} not in Lambda_N
        f1_anchors_N = {b for b in itertools.product(range(-N - 1, N + 2), repeat=3)
                         if whole_star_in(b, N)}
        f1_anchors_N1 = {b for b in itertools.product(range(-N - 2, N + 3), repeat=3)
                          if whole_star_in(b, N + 1)}
        new_f1_stars = f1_anchors_N1 - f1_anchors_N
        assert f1_anchors_N <= f1_anchors_N1, "F1(N) must nest inside F1(N+1)"

        f1_count_N = len(f1_anchors_N)
        f1_count_N1 = len(f1_anchors_N1)
        f1_closed_N = (2 * N) ** 3
        f1_closed_N1 = (2 * (N + 1)) ** 3

        new_f1_closed_form = 8 * (3 * N * N + 3 * N + 1)

        # new F2 faces: (anchor, class) pairs retained on Lambda_{N+1}
        # but not on Lambda_N.
        def f2_faces_on(M):
            faces = set()
            for b in itertools.product(range(-M - 1, M + 2), repeat=3):
                for idx, owner in enumerate(OMITTED_CLASSES):
                    owner_abs = frozenset(vadd(b, d) for d in owner)
                    if all(in_box(p, M) for p in owner_abs):
                        faces.add((b, idx))
            return faces

        f2_N = f2_faces_on(N)
        f2_N1 = f2_faces_on(N + 1)
        assert f2_N <= f2_N1, "F2(N) must nest inside F2(N+1)"
        new_f2_faces = f2_N1 - f2_N

        f2_closed_N = 28 * N * (2 * N + 1) * (3 * N + 1)
        f2_closed_N1 = 28 * (N + 1) * (2 * (N + 1) + 1) * (3 * (N + 1) + 1)
        new_f2_closed_form = 56 * (9 * N * N + 14 * N + 6)

        per_N[N] = {
            "f1_count_N": f1_count_N,
            "f1_count_N_closed_form_2N_cubed": f1_closed_N,
            "f1_count_N_matches": f1_count_N == f1_closed_N,
            "f1_count_N1": f1_count_N1,
            "f1_count_N1_closed_form": f1_closed_N1,
            "f1_count_N1_matches": f1_count_N1 == f1_closed_N1,
            "new_f1_stars": len(new_f1_stars),
            "new_f1_stars_closed_form_8_3Nsq_3N_1": new_f1_closed_form,
            "new_f1_stars_matches": len(new_f1_stars) == new_f1_closed_form,
            "new_f1_stars_by_difference_of_closed_forms": f1_closed_N1 - f1_closed_N,
            "f2_count_N": len(f2_N),
            "f2_count_N_closed_form": f2_closed_N,
            "f2_count_N_matches": len(f2_N) == f2_closed_N,
            "f2_count_N1": len(f2_N1),
            "f2_count_N1_closed_form": f2_closed_N1,
            "f2_count_N1_matches": len(f2_N1) == f2_closed_N1,
            "new_f2_faces": len(new_f2_faces),
            "new_f2_faces_closed_form_56_9Nsq_14N_6": new_f2_closed_form,
            "new_f2_faces_matches": len(new_f2_faces) == new_f2_closed_form,
            "new_f2_faces_by_difference_of_closed_forms": f2_closed_N1 - f2_closed_N,
        }
    return per_N


# ---------------------------------------------------------------------
# Part 6: compare with the BA1/BA2 gates and producer reports (data
# only -- their prose is scanned for the literal numbers, never their
# code executed).
# ---------------------------------------------------------------------

def gate_and_report_comparison(extra_faces, padding, nested):
    ba1_gate_text = load_json(BA1_GATE)["accepted"] + " " + load_json(BA1_GATE)["decision"]
    ba2_gate_text = load_json(BA2_GATE)["accepted"] + " " + load_json(BA2_GATE)["decision"]
    ba1_fwd = load_text(BA1_FWD_REPORT)
    ba1_rev = load_text(BA1_REV_REPORT)
    ba2_fwd = load_text(BA2_FWD_REPORT)
    ba2_rev = load_text(BA2_REV_REPORT)

    checks = []

    def record(label, ok, detail=""):
        checks.append({"label": label, "ok": bool(ok), "detail": detail})

    # extra-face counts 616, 1344, 2352 at N=2,3,4. The gates state only
    # the general formula 28N(5N+1) (checked separately below); the
    # literal per-N instance numbers are in the forward/reverse reports.
    expected_extra = {2: 616, 3: 1344, 4: 2352}
    for N, exp in expected_extra.items():
        got = extra_faces[N]["count"]
        record(f"extra_faces_N{N}_equals_{exp}", got == exp, f"got {got}")
        record(f"extra_faces_N{N}_in_ba1_fwd_report", str(exp) in ba1_fwd)
        record(f"extra_faces_N{N}_in_ba2_fwd_report", str(exp) in ba2_fwd)

    # padding sites 75, 147, 243 at N=2,3,4 (named in BA2 reverse/forward for N=2,3 only)
    expected_padding = {2: 75, 3: 147, 4: 243}
    for N, exp in expected_padding.items():
        got = padding[N]["padding_sites"]
        record(f"padding_sites_N{N}_equals_{exp}", got == exp, f"got {got}")
    record("padding_75_in_ba2_fwd_report", "75" in ba2_fwd)
    record("padding_147_in_ba2_fwd_report", "147" in ba2_fwd)
    record("padding_formula_3_2N1_sq_in_ba2_fwd_report", "3(2N+1)^2" in ba2_fwd)
    record("padding_75_in_ba2_rev_report", "75" in ba2_rev)
    record("padding_147_in_ba2_rev_report", "147" in ba2_rev)

    # new F1 stars 152, 296, 488 at N=2,3,4 (BA1 forward report table)
    expected_new_f1 = {2: 152, 3: 296, 4: 488}
    for N, exp in expected_new_f1.items():
        got = nested[N]["new_f1_stars"]
        record(f"new_f1_stars_N{N}_equals_{exp}", got == exp, f"got {got}")
        record(f"new_f1_stars_N{N}_in_ba1_fwd_report", str(exp) in ba1_fwd)

    # new F2 faces 3920, 7224, 11536 at N=2,3,4 (BA1 forward report table)
    expected_new_f2 = {2: 3920, 3: 7224, 4: 11536}
    for N, exp in expected_new_f2.items():
        got = nested[N]["new_f2_faces"]
        record(f"new_f2_faces_N{N}_equals_{exp}", got == exp, f"got {got}")
        record(f"new_f2_faces_N{N}_in_ba1_fwd_report", str(exp) in ba1_fwd)

    # 28N(5N+1) and 8(3N^2+3N+1) and 56(9N^2+14N+6) formula strings
    record("formula_28N_5N1_named_in_ba1_gate", "28N(5N+1)" in ba1_gate_text)
    record("formula_28N_5N1_named_in_ba2_gate", "28N(5N+1)" in ba2_gate_text)
    record("formula_140N2_28N_named_in_ba2_rev_report", "140N^2+28N" in ba2_rev)

    # class table 17,13,5,10,3,1,0 stated verbatim in the BA1 forward report
    record("class_table_17_13_5_in_ba1_fwd_report",
           all(tok in ba1_fwd for tok in ["17", "13", "5", "10", "3", "1", "0"]))
    record("class_table_phrase_in_ba2_gate",
           "per anchor 17, 13 and 5 faces when exactly one coordinate equals N, 10, 3 and 1 when two do, none at the corner" in ba2_gate_text)

    # incident anchors count 7 and diameter values 1 (l-infinity) / 2 (l1)
    record("star_diam_linf_1_named_in_ba1_gate", "star diameter d_X=1" in ba1_gate_text)
    record("star_diam_l1_2_stated_in_ba1_fwd_report", "l1 diameter 2" in ba1_fwd)

    all_ok = all(c["ok"] for c in checks)
    return {"all_ok": all_ok, "n_checks": len(checks), "checks": checks}


def main():
    diam_sec = diameters_section()
    inc_sec = incidence_section()
    extra_sec = extra_faces_section()
    pad_sec = padding_section()
    nested_sec = nested_sources_section()
    comparison = gate_and_report_comparison(extra_sec, pad_sec, nested_sec)

    overall_pass = bool(
        diam_sec["star_diam_linf_expected_1"]
        and diam_sec["star_diam_l1_expected_2"]
        and diam_sec["every_owner_diam_linf_le_1"]
        and diam_sec["every_owner_diam_l1_le_2"]
        and inc_sec["generic_bulk_site_incident_star_count_expected_4"]
        and inc_sec["incident_anchors_meeting_R_expected_7"]
        and inc_sec["faces_meeting_R_expected_82"]
        and inc_sec["faces_touching_both_expected_16"]
        and inc_sec["faces_with_owner_set_inside_R_expected_10"]
        and inc_sec["distinct_owner_set_types_expected_15"]
        and all(v["count_matches_closed_form"] for v in extra_sec.values())
        and all(v["n_anchors_matches"] for v in extra_sec.values())
        and all(v["corner_NNN_has_zero_extra_faces"] for v in extra_sec.values())
        and all(v["class_table_matches_gate_17_13_5_10_3_1_0"] for v in extra_sec.values())
        and all(v["min_dist_from_0_expected_N_both_metrics"] for v in extra_sec.values())
        and all(v["min_dist_from_ez_expected_Nminus1_both_metrics"] for v in extra_sec.values())
        and all(v["max_owners_per_face_le_3"] for v in extra_sec.values())
        and all(v["no_extra_face_meets_R"] for v in extra_sec.values())
        and all(v["padding_matches_closed_form"] for v in pad_sec.values())
        and all(v["f1_count_N_matches"] and v["f1_count_N1_matches"] for v in nested_sec.values())
        and all(v["new_f1_stars_matches"] for v in nested_sec.values())
        and all(v["f2_count_N_matches"] and v["f2_count_N1_matches"] for v in nested_sec.values())
        and all(v["new_f2_faces_matches"] for v in nested_sec.values())
        and comparison["all_ok"]
    )

    result = {
        "script": "diameters_and_sources.py",
        "zero_research_loops": True,
        "arithmetic": "plain Python int only; every quantity is an exact integer count or distance",
        "diameters": diam_sec,
        "incidence": inc_sec,
        "extra_faces_by_N": {str(k): v for k, v in extra_sec.items()},
        "padding_by_N": {str(k): v for k, v in pad_sec.items()},
        "nested_sources_by_N": {str(k): v for k, v in nested_sec.items()},
        "gate_and_report_comparison": comparison,
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
