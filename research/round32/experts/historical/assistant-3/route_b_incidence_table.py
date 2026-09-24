#!/usr/bin/env python3
"""
T3 -- route_b_incidence_table.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 3.

Zero research loops: test/planning script, not a producer, skeptic or
advisor artifact. Does not read or import research/round32/forward/ax1/
check.py or research/round32/reverse/ax1/check.py.

Task (update-2.md section 5, test 3): itemize the seven stars and the
two single-factor groups that meet R={0,e_z} FACE BY FACE (153 charges),
check no face is charged twice, and derive ||B_N||<=51|tau|/8.

Method: build the actual fine-link face objects (not just abstract
owner-set shapes) for every face in the 9 charged groups, using the
I1.4 tail rule this lens's assistant-1/assistant-2 already used
(face_links, owner_factor, from haar_parity_exact.py), generalized here
from "anchored at factor 0" to "anchored at any factor b" by the same
translation rule the AX1 report states (factor b owns tails
(4b_x+r,2b_y+s,b_z)). The 7 star anchors and 2 single-factor anchors
that meet R are themselves independently derived (not asserted) as
R-S and R respectively, S={0,ex,ey,ez}.

Reuse: imports research/round32/experts/historical/assistant-1/
haar_parity_exact.py (an assistant script, not a producer) for
face_links/unit/padd/owner_factor and its own anchor-0 build of the 21
omitted classes, used here only as a same-author cross-check that the
generalized (arbitrary-anchor) class builder below reduces to the
existing anchor-0 one when b=0.

Arithmetic: exact link-set (frozenset) identity for "no double charge";
fractions.Fraction for the norm bound ||B_N||. No floats anywhere.
Run with: python3 -B route_b_incidence_table.py
"""
import importlib.util
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
ASSISTANT1_DIR = os.path.join(REPO_ROOT, "research/round32/experts/historical/assistant-1")
FWD_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/ax1/output/results.json")
REV_RESULTS = os.path.join(REPO_ROOT, "research/round32/reverse/ax1/output/results.json")


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def _load_assistant1_haar():
    spec = importlib.util.spec_from_file_location(
        "haar_parity_exact", os.path.join(ASSISTANT1_DIR, "haar_parity_exact.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_haar = _load_assistant1_haar()
face_links = _haar.face_links
owner_factor = _haar.owner_factor
padd = _haar.padd
unit = _haar.unit

ZERO = (0, 0, 0)
EX, EY, EZ = (1, 0, 0), (0, 1, 0), (0, 0, 1)
S = (ZERO, EX, EY, EZ)
R_COVER = (ZERO, EZ)


def vsub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def base(b, r, s):
    """I1 tail rule generalized to anchor b: factor b owns fine tails
    (4b_x+r, 2b_y+s, b_z)."""
    bx, by, bz = b
    return (4 * bx + r, 2 * by + s, bz)


def omitted_classes_at(b):
    """The 21 omitted I1 classes anchored at factor b (star phi_b),
    same table as assistant-1's build_omitted_classes(), generalized
    from b=(0,0,0) to an arbitrary anchor via base(b,r,s)."""
    classes = []
    for r in range(3):                      # xy r=0,1,2; s=1 -> {0,e_y}
        classes.append(("xy_s1_r%d" % r, face_links(base(b, r, 1), "x", "y")))
    classes.append(("xy_r3_s0", face_links(base(b, 3, 0), "x", "y")))       # {0,e_x}
    classes.append(("xy_r3_s1", face_links(base(b, 3, 1), "x", "y")))       # {0,e_x,e_y}
    for r in range(3):                      # xz r=0,1,2; s=0,1 -> {0,e_z}
        for s in range(2):
            classes.append(("xz_r%d_s%d" % (r, s), face_links(base(b, r, s), "x", "z")))
    for s in range(2):                      # xz r=3; s=0,1 -> {0,e_x,e_z}
        classes.append(("xz_r3_s%d" % s, face_links(base(b, 3, s), "x", "z")))
    for r in range(4):                      # yz r=0..3; s=0 -> {0,e_z}
        classes.append(("yz_r%d_s0" % r, face_links(base(b, r, 0), "y", "z")))
    for r in range(4):                      # yz r=0..3; s=1 -> {0,e_y,e_z}
        classes.append(("yz_r%d_s1" % r, face_links(base(b, r, 1), "y", "z")))
    assert len(classes) == 21
    return classes


def selected_classes_at(b):
    """Route B's 3 selected xy classes anchored at factor b (single-
    factor group psi_b), (r,s)=(0,0),(1,0),(2,0)."""
    classes = [
        ("xy_sel_r%d_s0" % r, face_links(base(b, r, 0), "x", "y"))
        for r in range(3)
    ]
    assert len(classes) == 3
    return classes


def owner_set_of(links):
    return frozenset(owner_factor(t) for (t, _d) in links)


def main():
    # --- sanity gate: generalized builder at b=0 must reduce exactly
    # to assistant-1's own anchor-0 build (same names, same link sets) ---
    own_21_at_0 = dict(_haar.build_omitted_classes())
    my_21_at_0 = dict(omitted_classes_at(ZERO))
    sanity_omitted_matches = (own_21_at_0 == my_21_at_0)

    # --- independently derive the anchors that meet R={0,e_z} ---
    star_anchors = sorted({vsub(r_pt, s_pt) for r_pt in R_COVER for s_pt in S})
    single_anchors = sorted(R_COVER)
    n_star_anchors_ok = (len(star_anchors) == 7)
    n_single_anchors_ok = (len(single_anchors) == 2)

    # --- build every charged face, keyed by its exact fine link set ---
    charges = {}          # frozenset(links) -> label
    duplicates = []
    for b in star_anchors:
        for name, links in omitted_classes_at(b):
            key = links
            label = "star anchor=%s class=%s" % (b, name)
            if key in charges:
                duplicates.append((label, charges[key]))
            else:
                charges[key] = label
    for b in single_anchors:
        for name, links in selected_classes_at(b):
            key = links
            label = "single anchor=%s class=%s" % (b, name)
            if key in charges:
                duplicates.append((label, charges[key]))
            else:
                charges[key] = label

    n_charged_faces = len(charges)
    n_star_faces = 7 * 21
    n_single_faces = 2 * 3
    total_expected = n_star_faces + n_single_faces
    counts_ok = (n_charged_faces == total_expected == 153)
    no_double_charge = (len(duplicates) == 0)

    # --- cross-check: which of these 153 faces meet R / lie inside R ---
    R_set = frozenset(R_COVER)
    meeting_R = 0
    inside_R = 0
    for links in charges:
        owners = owner_set_of(links)
        if owners & R_set:
            meeting_R += 1
        if owners <= R_set:
            inside_R += 1
    meeting_R_ok = (meeting_R == 88)
    inside_R_ok = (inside_R == 16)

    # --- ||B_N|| <= 51|tau|/8 ---
    tau = F(1)  # symbolic: every entry below is "coefficient of |tau|"
    star_norm_bound = F(21, 3) * tau        # 7|tau| per star, I1.5 coefficient tau/3
    single_norm_bound = F(3, 3) * tau       # |tau| per single-factor group
    assert star_norm_bound == 7 * tau
    assert single_norm_bound == tau
    B_N_alpha_units = 7 * star_norm_bound + 2 * single_norm_bound
    assert B_N_alpha_units == 51 * tau
    # normalized units delta=alpha/8: divide by 8 to reach G=H/alpha units
    B_N_G_units = B_N_alpha_units / 8
    B_N_matches_51_8 = (B_N_G_units == F(51, 8) * tau)

    # --- cross-check against both producers' exports ---
    fwd = load_json(FWD_RESULTS)
    rev = load_json(REV_RESULTS)

    fwd_incidence = fwd["incidence_totals"]
    fwd_checks = {
        "stars": fwd_incidence["stars"] == len(star_anchors),
        "single_factor_groups": fwd_incidence["single_factor_groups"] == len(single_anchors),
        "selected_faces_inside_R": fwd_incidence["selected_faces_inside_R"] == 6,
        "B_N_over_abs_tau": F(fwd_incidence["B_N_over_abs_tau"]) == F(51, 8),
    }

    rev_incidence = rev["incidence"]["table"]
    rev_total_faces = sum(row["n_faces"] for row in rev_incidence)
    rev_n_stars = sum(1 for row in rev_incidence if row["kind"] == "whole_star")
    rev_n_single = sum(1 for row in rev_incidence if row["kind"] == "single_factor")
    rev_anchors_star = sorted(tuple(row["anchor"]) for row in rev_incidence if row["kind"] == "whole_star")
    rev_anchors_single = sorted(tuple(row["anchor"]) for row in rev_incidence if row["kind"] == "single_factor")
    rev_checks = {
        "total_faces_153": rev_total_faces == 153,
        "n_stars_7": rev_n_stars == 7,
        "n_single_2": rev_n_single == 2,
        "star_anchors_match": rev_anchors_star == star_anchors,
        "single_anchors_match": rev_anchors_single == single_anchors,
        "faces_meeting_R_88": load_json(REV_RESULTS)["face_enumeration"]["derived"]["faces_meeting_R"] == 88,
    }

    all_fwd_ok = all(fwd_checks.values())
    all_rev_ok = all(rev_checks.values())

    overall_pass = bool(
        sanity_omitted_matches
        and n_star_anchors_ok
        and n_single_anchors_ok
        and counts_ok
        and no_double_charge
        and meeting_R_ok
        and inside_R_ok
        and B_N_matches_51_8
        and all_fwd_ok
        and all_rev_ok
    )

    def s(x):
        return str(x) if isinstance(x, F) else x

    result = {
        "script": "route_b_incidence_table.py",
        "zero_research_loops": True,
        "arithmetic": "exact fine-link frozenset identity for double-charge check; fractions.Fraction for the norm bound; no floats",
        "sanity_gate_generalized_builder_matches_assistant1_at_anchor_0": sanity_omitted_matches,
        "anchors": {
            "star_anchors_meeting_R_R_minus_S": star_anchors,
            "n_star_anchors": len(star_anchors),
            "n_star_anchors_expected_7": n_star_anchors_ok,
            "single_factor_anchors_meeting_R": single_anchors,
            "n_single_anchors_expected_2": n_single_anchors_ok,
        },
        "charge_table": {
            "n_charged_faces": n_charged_faces,
            "n_star_faces_7x21": n_star_faces,
            "n_single_faces_2x3": n_single_faces,
            "total_expected_153": total_expected,
            "counts_match_153": counts_ok,
            "no_face_charged_twice": no_double_charge,
            "duplicates_found": duplicates,
        },
        "R_incidence_within_the_153": {
            "faces_meeting_R": meeting_R,
            "faces_meeting_R_expected_88": meeting_R_ok,
            "faces_inside_R": inside_R,
            "faces_inside_R_expected_16": inside_R_ok,
        },
        "norm_bound": {
            "star_norm_bound_over_tau": s(star_norm_bound),
            "single_group_norm_bound_over_tau": s(single_norm_bound),
            "B_N_alpha_units_over_tau": s(B_N_alpha_units),
            "B_N_G_units_over_tau": s(B_N_G_units),
            "matches_51_over_8": B_N_matches_51_8,
        },
        "cross_check_forward": fwd_checks,
        "cross_check_reverse": rev_checks,
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
