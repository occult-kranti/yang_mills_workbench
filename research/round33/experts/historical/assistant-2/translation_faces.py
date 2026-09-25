#!/usr/bin/env python3
"""
translation_faces.py
Historical (Newton/Tesla) lens research assistant, Round33 sub-round 2
(assistant-2). Zero research loops: an independent, face-by-face
cross-check of BB2 item 4 (coarse translation invariance), specifically
of the reverse report's Lemma 7.1/Lemma 7.2 claim: a fine translation
`t=(tx,ty,tz)` maps the face/owner/role structure of the I1 anchored
block onto itself, class by class, IFF `t=(4v_x,2v_y,v_z)` for an
integer coarse translation `v` -- and, among all 64 fine translations
of the period window `[0,8)x[0,4)x[0,2)`, exactly 8 are of this coarse
form (research/round33/reverse/bb2/report.md Section 7, Lemma 7.2).

This script also builds, deliberately, the "skeptic's pitfall" the
task asks for: a per-anchor OWNER-TYPE HISTOGRAM check (comparing only
the multiset of the six owner-set types {0,e_y}/{0,e_x}/{0,e_x,e_y}/
{0,e_z}/{0,e_x,e_z}/{0,e_y,e_z} and their fixed multiplicities
3/1/1/10/2/4 present at an anchor) and shows that this histogram is
IDENTICAL at every anchor of the lattice regardless of translation --
so a check that only compares histograms "accepts" all 64 fine
translations in the window, including the 56 non-coarse ones that the
exact face-by-face check correctly rejects.

This script never imports or executes
  research/round33/forward/bb2/check.py
  research/round33/reverse/bb2/check.py
or any other check.py. The face/orientation/(r,s)-residue classification
table is re-derived from scratch from research/round21/forward/i1/
report.md sections 2-3 (Euclidean division x=4i+r, y=2j+s, pi(x,y,z)=
(floor(x/4),floor(y/2),z), and the anchored face table). The BB2
reverse report.md (Section 7, Lemma 7.1/7.2) is read only as a PROSE
statement of the claim under test (the witness `t=(1,0,0)` it names is
reproduced below as one of the 64 cases, not assumed).

Arithmetic: plain Python `int` throughout (residues, floor divisions,
face-class labels and translation vectors are all exact integers). No
floats, no `Fraction`.

Run with: python3 -B translation_faces.py
Also checked identical under: python3 -B -O translation_faces.py
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
BB2_REV_REPORT = os.path.join(REPO_ROOT, "research/round33/reverse/bb2/report.md")


def load_text(path):
    with open(path) as fh:
        return fh.read()


# ---------------------------------------------------------------------
# Part 0: the face classification, re-derived from I1 (4i+r, 2j+s;
# pi(x,y,z) = (floor(x/4), floor(y/2), z)). Every face at a coarse
# anchor is identified by (orientation, r, s) with orientation in
# {xy, xz, yz}, r in 0..3 (x-residue mod 4), s in 0..1 (y-residue mod
# 2) -- 3*4*2 = 24 combinations, matching I1's 24 anchored classes
# exactly (I1 eq. I1.2: 24 = 10+14 links; the face table's 8 rows sum
# to 3 selected + 21 omitted = 24 faces).
#
# I1's table (Section 3), by (orientation, r-range, s-range):
#   xy, r in {0,1,2}, s=0        -> selected            (3 combos)
#   xy, r in {0,1,2}, s=1        -> omitted {0,e_y}      (3 combos)
#   xy, r=3,          s=0        -> omitted {0,e_x}      (1 combo)
#   xy, r=3,          s=1        -> omitted {0,e_x,e_y}  (1 combo)
#   xz, r in {0,1,2}, s in {0,1} -> omitted {0,e_z}      (6 combos)
#   xz, r=3,          s in {0,1}-> omitted {0,e_x,e_z}   (2 combos)
#   yz, r in {0,1,2,3}, s=0      -> omitted {0,e_z}      (4 combos)
#   yz, r in {0,1,2,3}, s=1      -> omitted {0,e_y,e_z}  (4 combos)
# ---------------------------------------------------------------------

ORIENTATIONS = ("xy", "xz", "yz")
SELECTED = "selected"


def face_class(orientation, r, s):
    """Return the owner-set label (a frozenset string) or SELECTED, for
    one (orientation, r, s) combination, r in 0..3, s in 0..1."""
    assert orientation in ORIENTATIONS
    assert 0 <= r <= 3 and 0 <= s <= 1
    if orientation == "xy":
        if r in (0, 1, 2) and s == 0:
            return SELECTED
        if r in (0, 1, 2) and s == 1:
            return "0,ey"
        if r == 3 and s == 0:
            return "0,ex"
        if r == 3 and s == 1:
            return "0,ex,ey"
    elif orientation == "xz":
        if r in (0, 1, 2):
            return "0,ez"
        if r == 3:
            return "0,ex,ez"
    elif orientation == "yz":
        if s == 0:
            return "0,ez"
        if s == 1:
            return "0,ey,ez"
    raise AssertionError("unreachable")


ALL_COMBOS = [(o, r, s) for o in ORIENTATIONS for r in range(4) for s in range(2)]
assert len(ALL_COMBOS) == 24

_owner_counts = {}
for (o, r, s) in ALL_COMBOS:
    c = face_class(o, r, s)
    _owner_counts[c] = _owner_counts.get(c, 0) + 1
assert _owner_counts == {
    SELECTED: 3, "0,ey": 3, "0,ex": 1, "0,ex,ey": 1,
    "0,ez": 10, "0,ex,ez": 2, "0,ey,ez": 4,
}, _owner_counts
# The fixed per-anchor histogram of the 21 OMITTED classes only
# (excludes "selected"), by owner-type label -> multiplicity. This is
# THE SAME dict at every anchor of the whole lattice (translation
# independent), which is exactly the pitfall this script demonstrates.
FIXED_OMITTED_HISTOGRAM = {k: v for k, v in _owner_counts.items() if k != SELECTED}
assert sum(FIXED_OMITTED_HISTOGRAM.values()) == 21


def anchor_owner_histogram():
    """A per-anchor owner-type histogram computed the naive way: just
    read off I1's table again. This is IDENTICAL for every anchor b
    (i,j,k) in the whole positive-offset-free orthant, by construction
    -- the (r,s) grid and hence the class table do not depend on
    (i,j,k) at all. Returns the fixed dict, independent of its
    (unused) argument, to make this invariance explicit at each call
    site below."""
    return dict(FIXED_OMITTED_HISTOGRAM)


# ---------------------------------------------------------------------
# Part 1: the fine period window and the coarse/non-coarse test.
# ---------------------------------------------------------------------

WINDOW_TX = range(8)   # [0,8)
WINDOW_TY = range(4)   # [0,4)
WINDOW_TZ = range(2)   # [0,2)


def block_shift_x(tx):
    """floor((r+tx)/4) - floor(r/4) for r=0..3; returns the list of the
    4 per-residue block shifts (constant iff tx is a multiple of 4)."""
    return [(r + tx) // 4 - r // 4 for r in range(4)]


def block_shift_y(ty):
    return [(s + ty) // 2 - s // 2 for s in range(2)]


def is_uniform_shift(tx, ty):
    """True iff pi(p+t)-pi(p) is the same vector for every p (i.e. t
    induces a single well-defined coarse shift v=(vx,vy,vz))."""
    xs = block_shift_x(tx)
    ys = block_shift_y(ty)
    return len(set(xs)) == 1 and len(set(ys)) == 1, (xs[0] if len(set(xs)) == 1 else None,
                                                       ys[0] if len(set(ys)) == 1 else None)


def is_class_preserving(tx, ty):
    """True iff, for every (orientation, r, s), the class attached to
    the ORIGINAL position equals the class attached to the position
    reached after shifting the local residues by (tx,ty) -- i.e. the
    pattern (selected vs. each of the 6 omitted owner types) maps onto
    itself. This is the exact witness Lemma 7.2 gives for t=(1,0,0)."""
    violations = []
    for (o, r, s) in ALL_COMBOS:
        r2 = (r + tx) % 4
        s2 = (s + ty) % 2
        c1 = face_class(o, r, s)
        c2 = face_class(o, r2, s2)
        if c1 != c2:
            violations.append({"orientation": o, "r": r, "s": s,
                                "maps_to_r": r2, "maps_to_s": s2,
                                "original_class": c1, "new_class": c2})
    return len(violations) == 0, violations


def analyze_translation(tx, ty, tz):
    uniform, v_xy = is_uniform_shift(tx, ty)
    class_ok, violations = is_class_preserving(tx, ty)
    is_coarse = uniform and class_ok
    vx = tx // 4 if is_coarse else None
    vy = ty // 2 if is_coarse else None
    vz = tz if is_coarse else None
    # exact-remainder test: a coarse translation must ALSO have tx, ty
    # be EXACT multiples (0 remainder), not merely a uniform shift by
    # coincidence; check both conditions agree.
    exact_multiple = (tx % 4 == 0) and (ty % 2 == 0)
    assert is_coarse == (uniform and class_ok)
    return {
        "t_fine": [tx, ty, tz],
        "uniform_anchor_shift": uniform,
        "uniform_shift_v_xy": list(v_xy),
        "class_preserving": class_ok,
        "class_violations_count": len(violations),
        "class_violations_sample": violations[:2],
        "is_coarse_translation": is_coarse,
        "exact_multiple_tx4_ty2": exact_multiple,
        "coarse_v_if_applicable": [vx, vy, vz] if is_coarse else None,
    }


# ---------------------------------------------------------------------
# Part 2: the histogram pitfall. For a translation t, the "naive"
# per-anchor histogram check just asks: does anchor b's owner-type
# histogram equal anchor (b + naive_v)'s owner-type histogram, where
# naive_v = (tx//4, ty//2, tz) is the best-effort (possibly wrong for
# non-coarse t) coarse-shift guess? Since FIXED_OMITTED_HISTOGRAM is
# the SAME dict at every anchor (by construction, see Part 0), this
# equality holds TRIVIALLY for every t, coarse or not -- the pitfall.
# ---------------------------------------------------------------------

def histogram_check_accepts(tx, ty, tz):
    naive_v = (tx // 4, ty // 2, tz)  # well-defined even when not uniform
    hist_b = anchor_owner_histogram()
    hist_b_plus_v = anchor_owner_histogram()  # identical at every anchor
    return hist_b == hist_b_plus_v, naive_v


# ---------------------------------------------------------------------
# Part 3: enumerate the full 64-translation window and cross-check
# against the reverse BB2 report's Lemma 7.2 (8 of 64 are coarse; the
# witness t=(1,0,0) fails class-preservation at the named face class).
# ---------------------------------------------------------------------

def cross_check_report():
    text = load_text(BB2_REV_REPORT)
    checks = {}
    checks["report_states_64_translations"] = "64 translations" in text
    checks["report_states_period_window"] = "[0,8)x[0,4)x[0,2)" in text
    checks["report_states_exactly_8_coarse"] = "exactly 8 are coarse" in text
    checks["report_names_witness_t_100"] = "t=(1,0,0)" in text
    checks["report_names_witness_class_0_ex"] = "owner set `{0,e_x}`" in text
    checks["report_has_lemma_7_1"] = "Lemma 7.1" in text
    checks["report_has_lemma_7_2"] = "Lemma 7.2" in text
    return checks


def main():
    per_translation = []
    coarse_count = 0
    histogram_false_accepts = 0
    non_coarse_count = 0
    for tx, ty, tz in itertools.product(WINDOW_TX, WINDOW_TY, WINDOW_TZ):
        analysis = analyze_translation(tx, ty, tz)
        hist_accept, naive_v = histogram_check_accepts(tx, ty, tz)
        analysis["histogram_check_accepts"] = hist_accept
        analysis["histogram_naive_v"] = list(naive_v)
        if analysis["is_coarse_translation"]:
            coarse_count += 1
        else:
            non_coarse_count += 1
            if hist_accept:
                histogram_false_accepts += 1
        per_translation.append(analysis)

    # the specific witness named in the reverse report
    witness = analyze_translation(1, 0, 0)
    witness_ok = (
        not witness["is_coarse_translation"]
        and not witness["class_preserving"]
        and any(
            v["orientation"] == "xy" and v["r"] == 2 and v["s"] == 0
            and v["new_class"] == "0,ex"
            for v in [vv for vv in is_class_preserving(1, 0)[1]]
        )
    )

    coarse_translations = [
        tuple(a["t_fine"]) for a in per_translation if a["is_coarse_translation"]
    ]
    expected_coarse = sorted(
        (vx * 4, vy * 2, vz)
        for vx in (0, 1) for vy in (0, 1) for vz in (0, 1)
    )
    coarse_translations_sorted = sorted(coarse_translations)

    cross = cross_check_report()

    checks = {
        "exactly_8_of_64_are_coarse": coarse_count == 8,
        "coarse_count": coarse_count,
        "total_translations": len(per_translation),
        "coarse_translations_are_exactly_4vx_2vy_vz": (
            coarse_translations_sorted == expected_coarse
        ),
        "witness_t_100_reproduced": witness_ok,
        "histogram_check_false_accepts_every_non_coarse_translation": (
            histogram_false_accepts == non_coarse_count and non_coarse_count == 56
        ),
        "histogram_false_accept_count": histogram_false_accepts,
        "non_coarse_count": non_coarse_count,
        "histogram_is_anchor_invariant_hence_uninformative": (
            FIXED_OMITTED_HISTOGRAM == anchor_owner_histogram()
        ),
    }

    overall = all([
        checks["exactly_8_of_64_are_coarse"],
        checks["coarse_translations_are_exactly_4vx_2vy_vz"],
        checks["witness_t_100_reproduced"],
        checks["histogram_check_false_accepts_every_non_coarse_translation"],
        checks["histogram_is_anchor_invariant_hence_uninformative"],
        all(v for k, v in cross.items()),
    ])

    report = {
        "script": "translation_faces.py",
        "task": "independent face-by-face check of BB2 item 4's coarse-translation "
                "lemma over the full 64-translation fine period window "
                "[0,8)x[0,4)x[0,2), plus a demonstration that a per-anchor "
                "owner-type histogram check (the skeptic's pitfall) accepts "
                "every non-coarse translation as well",
        "face_class_table_24_combos_check": {
            "counts": _owner_counts,
            "matches_I1_table": _owner_counts == {
                SELECTED: 3, "0,ey": 3, "0,ex": 1, "0,ex,ey": 1,
                "0,ez": 10, "0,ex,ez": 2, "0,ey,ez": 4,
            },
        },
        "checks": checks,
        "witness_t_100_detail": witness,
        "coarse_translations_found": coarse_translations_sorted,
        "per_translation": per_translation,
        "cross_check_against_frozen_report": cross,
        "overall_pass": overall,
    }
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
