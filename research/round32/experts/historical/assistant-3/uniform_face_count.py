#!/usr/bin/env python3
"""
T2 -- uniform_face_count.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 3.

Zero research loops: test/planning script, not a producer, skeptic or
advisor artifact. Does not read or import research/round32/forward/ax1/
check.py or research/round32/reverse/ax1/check.py.

Task (update-2.md section 5, test 2): from the 24 anchored face classes
per factor (21 omitted, exactly the I1 table this lens's assistant-1
already encoded in am2_tiers_exact.py, plus the 3 selected xy faces at
(r,s)=(0,0),(1,0),(2,0), route B's new single-factor group), enumerate
BY TRANSLATION COVARIANCE (the same abstract-owner-set method as
assistant-1's S2, extended here to the 24-class route-B model, never
reading a producer's check.py):

    owner-set faces per factor      (expect 52)
    faces meeting R={0,e_z}          (expect 88)
    faces inside R (owning both 0 and e_z)  (expect 16)
    selected faces inside R (touching 0 or e_z)  (expect 6)

and show the contract's candidates 96 (=4x24) and 168 (=7x24) are only
labelled upper bounds (naive per-anchor multiplication), strictly above
the derived exact counts.

Reuse: imports research/round32/experts/historical/assistant-1/
am2_tiers_exact.py (an assistant script, not a producer) for its
OMITTED_CLASSES table and coarse-lattice vector helpers, exactly as
that lens's own S3 (window_kernel_budget.py) already reused S2. The
route-B SELECTED_CLASSES (support {0} each, single-factor group) are
new here. As a sanity gate, the 21-class (omitted-only, AW1/AV1) case
is first reproduced to match assistant-1's own 49/15/82/16 numbers
before the 24-class (route-B) case is run.

Arithmetic: exact integer/combinatorial enumeration; no floats anywhere.
Run with: python3 -B uniform_face_count.py
"""
import importlib.util
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
ASSISTANT1_DIR = os.path.join(REPO_ROOT, "research/round32/experts/historical/assistant-1")
FWD_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/ax1/output/results.json")
REV_RESULTS = os.path.join(REPO_ROOT, "research/round32/reverse/ax1/output/results.json")


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def _load_assistant1_am2():
    spec = importlib.util.spec_from_file_location(
        "am2_tiers_exact", os.path.join(ASSISTANT1_DIR, "am2_tiers_exact.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_am2 = _load_assistant1_am2()
ZERO, EX, EY, EZ = _am2.ZERO, _am2.EX, _am2.EY, _am2.EZ
vadd, vsub = _am2.vadd, _am2.vsub
OMITTED_CLASSES = _am2.OMITTED_CLASSES  # 21 classes, frozensets of offsets in {0,ex,ey,ez}

# Route B's 3 new selected classes (xy, r=0,1,2, s=0): single-factor
# group support {0} each -- I1.4/AX1-F03's psi_b.
SELECTED_CLASSES = [frozenset([ZERO])] * 3

ALL_CLASSES = list(OMITTED_CLASSES) + list(SELECTED_CLASSES)  # 24 classes
N_OMITTED = len(OMITTED_CLASSES)
assert N_OMITTED == 21
assert len(ALL_CLASSES) == 24


def faces_touching(u, classes):
    """
    A face of class K (K subset {0,ex,ey,ez}) anchored at b touches
    factor v iff v=b+d for some d in K, i.e. b=v-d. Returns a list of
    (anchor, class_index, owner_set) for every (class, d in K) pair
    touching u. class_index >= N_OMITTED marks a SELECTED class.
    """
    out = []
    for idx, K in enumerate(classes):
        for d in K:
            b = vsub(u, d)
            owner_set = frozenset(vadd(b, dd) for dd in K)
            out.append((b, idx, owner_set))
    return out


def enumerate_route_b(classes, n_omitted):
    u = ZERO
    faces = faces_touching(u, classes)
    n_faces = len(faces)

    groups = defaultdict(list)
    for b, idx, owner_set in faces:
        groups[owner_set].append((b, idx))
    n_owner_sets = len(groups)
    multiplicities = sorted(len(v) for v in groups.values())

    faces_0 = faces_touching(ZERO, classes)
    faces_ez = faces_touching(EZ, classes)
    set_0 = set((b, idx) for b, idx, _ in faces_0)
    set_ez = set((b, idx) for b, idx, _ in faces_ez)
    union = set_0 | set_ez
    both = set_0 & set_ez

    n_meeting_R = len(union)
    n_inside_R = len(both)
    n_selected_meeting_R = len({(b, idx) for (b, idx) in union if idx >= n_omitted})

    return {
        "n_faces_per_factor": n_faces,
        "n_owner_sets": n_owner_sets,
        "owner_set_multiplicities_sorted": multiplicities,
        "sum_of_multiplicities": sum(multiplicities),
        "n_faces_meeting_R": n_meeting_R,
        "n_faces_inside_R": n_inside_R,
        "n_selected_faces_meeting_R": n_selected_meeting_R,
    }


def main():
    # --- sanity gate: 21-class (omitted-only) case must match
    # assistant-1's own numbers before trusting the 24-class extension ---
    sanity = enumerate_route_b(OMITTED_CLASSES, n_omitted=21)
    sanity_ok = (
        sanity["n_faces_per_factor"] == 49
        and sanity["n_owner_sets"] == 15
        and sanity["n_faces_meeting_R"] == 82
        and sanity["n_faces_inside_R"] == 16
        and sanity["n_selected_faces_meeting_R"] == 0
    )
    # cross-check directly against assistant-1's own function
    own_am2 = _am2.enumerate_star_and_owner_sets()
    sanity_matches_assistant1 = (
        sanity["n_faces_per_factor"] == own_am2["n_faces_per_factor"]
        and sanity["n_owner_sets"] == own_am2["n_owner_sets"]
        and sanity["n_faces_meeting_R"] == own_am2["n_faces_meeting_R"]
        and sanity["n_faces_inside_R"] == own_am2["n_faces_touching_both_0_and_ez"]
    )

    # --- route-B case: all 24 classes ---
    route_b = enumerate_route_b(ALL_CLASSES, n_omitted=N_OMITTED)

    expected = {
        "n_faces_per_factor": 52,
        "n_faces_meeting_R": 88,
        "n_faces_inside_R": 16,
        "n_selected_faces_meeting_R": 6,
    }
    route_b_ok = all(route_b[k] == v for k, v in expected.items())
    multiplicities_sum_ok = (route_b["sum_of_multiplicities"] == route_b["n_faces_per_factor"] == 52)

    # --- 96 and 168 are naive per-anchor bounds only, not exact counts ---
    n_anchors_per_star_support = 4    # |S|={0,ex,ey,ez}
    n_anchors_meeting_R = 7           # independently confirmed in script 3
    bound_per_factor = n_anchors_per_star_support * 24
    bound_R = n_anchors_meeting_R * 24
    bounds_are_strict_overcounts = bool(
        bound_per_factor == 96 and bound_per_factor > route_b["n_faces_per_factor"]
        and bound_R == 168 and bound_R > route_b["n_faces_meeting_R"]
    )

    # --- cross-check against both producers' exported face_enumeration ---
    fwd = load_json(FWD_RESULTS)["face_enumeration"]
    rev = load_json(REV_RESULTS)["face_enumeration"]["derived"]
    rev_bounds = load_json(REV_RESULTS)["face_enumeration"]["labelled_bounds"]

    fwd_checks = {
        "faces_per_factor": fwd["faces_per_factor"] == route_b["n_faces_per_factor"],
        "faces_meeting_R": fwd["faces_meeting_R"] == route_b["n_faces_meeting_R"],
        "faces_inside_R": fwd["faces_inside_R"] == route_b["n_faces_inside_R"],
        "owner_sets_per_factor": fwd["owner_sets_per_factor"] == route_b["n_owner_sets"],
        "multiplicities": sorted(fwd["multiplicities"]) == route_b["owner_set_multiplicities_sorted"],
        "labelled_bound_per_factor_96": fwd["labelled_bounds"]["per_factor"] == 96 == bound_per_factor,
        "labelled_bound_R_168": fwd["labelled_bounds"]["R"] == 168 == bound_R,
    }
    rev_checks = {
        "faces_per_factor": rev["faces_per_factor"] == route_b["n_faces_per_factor"],
        "faces_meeting_R": rev["faces_meeting_R"] == route_b["n_faces_meeting_R"],
        "faces_inside_R": rev["faces_inside_R"] == route_b["n_faces_inside_R"],
        "selected_faces_per_factor": rev["selected_faces_per_factor"] == 3,
        "omitted_faces_per_factor": rev["omitted_faces_per_factor"] == 49,
        "owner_sets_per_factor": rev["owner_sets_per_factor"] == route_b["n_owner_sets"],
        "labelled_bound_per_factor_96": rev_bounds["per_factor"] == 96 == bound_per_factor,
        "labelled_bound_R_168": rev_bounds["R"] == 168 == bound_R,
    }
    all_fwd_ok = all(fwd_checks.values())
    all_rev_ok = all(rev_checks.values())

    overall_pass = bool(
        sanity_ok
        and sanity_matches_assistant1
        and route_b_ok
        and multiplicities_sum_ok
        and bounds_are_strict_overcounts
        and all_fwd_ok
        and all_rev_ok
    )

    result = {
        "script": "uniform_face_count.py",
        "zero_research_loops": True,
        "method": "translation-covariant owner-set enumeration (assistant-1 S2 method extended to 24 route-B classes); no floats",
        "sanity_gate_21_classes_omitted_only": {
            **sanity,
            "matches_AW1_49_15_82_16": sanity_ok,
            "matches_assistant1_own_function": sanity_matches_assistant1,
        },
        "route_b_24_classes": route_b,
        "route_b_matches_expected_52_88_16_6": route_b_ok,
        "labelled_bounds": {
            "per_factor_4x24": bound_per_factor,
            "R_7x24": bound_R,
            "strictly_exceed_exact_counts": bounds_are_strict_overcounts,
        },
        "cross_check_forward_face_enumeration": fwd_checks,
        "cross_check_reverse_face_enumeration": rev_checks,
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
