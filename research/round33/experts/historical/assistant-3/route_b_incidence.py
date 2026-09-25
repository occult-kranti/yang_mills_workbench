#!/usr/bin/env python3
"""
route_b_incidence.py
Historical (Newton/Tesla) lens research assistant, Round33 sub-round 3
(assistant-3). Zero research loops: an independent, from-scratch exact
enumeration of the route-B partition of the uniform Kogut-Susskind model
(BC2's model AQ_uniform_routeB), and a cross-check of every pinned number
against research/round33/contracts/bc2.json, the AX1 gate, the AX1
forward report and the BC2 forward report.md / output/results.json.

This script never imports or executes any producer `check.py` (BC2's,
BB2's, or any other round's), and never reads anything under
`research/round33/forward/bd*/` or `research/round33/reverse/bd1/`
(in production at the time this package was written). Every geometric
and combinatorial construction below is re-derived from scratch from:
  - research/round21/forward/i1/report.md sections 2-3 (the Euclidean
    division x=4i+r, y=2j+s, pi(x,y,z)=(floor(x/4),floor(y/2),z), and
    the 24-class anchored face table, six owner-set types among the 21
    omitted classes plus 3 selected classes);
  - research/round29/forward/am2/report.md (S={0,e_x,e_y,e_z});
  - research/round32/forward/ax1/report.md sections 1-5 (the route-B
    grouping: one whole star phi_b of the 21 omitted faces anchored at
    b, plus one single-factor group psi_b of the 3 selected faces
    anchored at b, support {b}; "every single-factor group of the box
    is retained, because its support {b} always lies inside the box";
    "a site u lies in exactly four stars ... and in exactly one
    single-factor group"; "seven stars and exactly two single-factor
    groups meet R").
Only research/round33/contracts/bc2.json (frozen), the AX1 gate
(research/round32/advisor/ax1-gate.json, read for its own text, not
executed), and the BC2 forward producer's report.md prose and exported
output/results.json (data, never code) are read for the final
comparison.

Arithmetic: plain Python `int` throughout (every quantity here is an
exact integer lattice coordinate, l-infinity distance, or face/anchor
count). No floats, no `Fraction` (nothing irrational or non-integer
rational appears in this script's task).

Run with: python3 -B route_b_incidence.py
Also checked identical under: python3 -B -O route_b_incidence.py
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# HERE = .../research/round33/experts/historical/assistant-3
# up 5: assistant-3 -> historical -> experts -> round33 -> research -> <repo root>
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

BC2_CONTRACT = os.path.join(REPO_ROOT, "research/round33/contracts/bc2.json")
AX1_GATE = os.path.join(REPO_ROOT, "research/round32/advisor/ax1-gate.json")
AX1_REPORT = os.path.join(REPO_ROOT, "research/round32/forward/ax1/report.md")
BC2_FWD_REPORT = os.path.join(REPO_ROOT, "research/round33/forward/bc2/report.md")
BC2_FWD_RESULTS = os.path.join(REPO_ROOT, "research/round33/forward/bc2/output/results.json")

FORBIDDEN_SUBSTRINGS = ("forward/bd", "reverse/bd1")


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def load_text(path):
    with open(path) as fh:
        return fh.read()


for _p in (BC2_CONTRACT, AX1_GATE, AX1_REPORT, BC2_FWD_REPORT, BC2_FWD_RESULTS):
    assert not any(f in _p for f in FORBIDDEN_SUBSTRINGS), _p


# ---------------------------------------------------------------------
# Part 0: the star, the 21 individual omitted-face owner-set classes,
# the single-factor group, and the 24-class (orientation,r,s) table,
# all re-derived from scratch from I1 sections 2-3 and 6, AM2's
# S={0,e_x,e_y,e_z}, and AX1's route-B grouping (Sections 1-5).
# ---------------------------------------------------------------------

ZERO, EX, EY, EZ = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)
S = [ZERO, EX, EY, EZ]
assert len(S) == 4


def vadd(p, q):
    return tuple(a + b for a, b in zip(p, q))


def linf(p, q=ZERO):
    return max(abs(a - b) for a, b in zip(p, q))


# I1's six omitted owner-set types (by owner-set label -> multiplicity),
# re-derived independently from the I1 anchored face table (as in the
# assistant-1/assistant-2 packages, but not imported from them):
OWNER_TYPES = [
    (frozenset([ZERO, EY]), 3),
    (frozenset([ZERO, EX]), 1),
    (frozenset([ZERO, EX, EY]), 1),
    (frozenset([ZERO, EZ]), 10),
    (frozenset([ZERO, EX, EZ]), 2),
    (frozenset([ZERO, EY, EZ]), 4),
]
assert sum(m for _, m in OWNER_TYPES) == 21
# The single-factor group's one owner type: support exactly {b} (the
# anchor alone), multiplicity 3 (the three selected xy faces, AX1
# Section 1: "each factor carries one whole star ... and one
# single-factor group psi_b").
SINGLE_TYPE = (frozenset([ZERO]), 3)

SELECTED = "selected"
ORIENTATIONS = ("xy", "xz", "yz")


def face_class(orientation, r, s):
    """The I1 (orientation, r, s) -> class table, r in 0..3, s in 0..1,
    re-derived from research/round21/forward/i1/report.md sections 2-3
    (independently of, but consistent with, the same table used by
    assistant-2's translation_faces.py -- not imported from it)."""
    assert orientation in ORIENTATIONS
    assert 0 <= r <= 3 and 0 <= s <= 1
    if orientation == "xy":
        if r in (0, 1, 2) and s == 0:
            return SELECTED
        if r in (0, 1, 2) and s == 1:
            return frozenset([ZERO, EY])
        if r == 3 and s == 0:
            return frozenset([ZERO, EX])
        if r == 3 and s == 1:
            return frozenset([ZERO, EX, EY])
    elif orientation == "xz":
        if r in (0, 1, 2):
            return frozenset([ZERO, EZ])
        if r == 3:
            return frozenset([ZERO, EX, EZ])
    elif orientation == "yz":
        if s == 0:
            return frozenset([ZERO, EZ])
        if s == 1:
            return frozenset([ZERO, EY, EZ])
    raise AssertionError("unreachable")


ALL_COMBOS = [(o, r, s) for o in ORIENTATIONS for r in range(4) for s in range(2)]
assert len(ALL_COMBOS) == 24
_counts = {}
for (o, r, s) in ALL_COMBOS:
    c = face_class(o, r, s)
    _counts[c] = _counts.get(c, 0) + 1
assert _counts[SELECTED] == 3
assert sum(v for k, v in _counts.items() if k != SELECTED) == 21
for owner, mult in OWNER_TYPES:
    assert _counts[owner] == mult


def pi(x, y, z):
    """Coarse anchor of fine point (x,y,z): (floor(x/4), floor(y/2), z)."""
    return (x // 4, y // 2, z)


def lambda_bounds(N):
    return ((-N, N), (-N, N), (-N, N))


def in_box(p, bounds):
    return all(lo <= c <= hi for c, (lo, hi) in zip(p, bounds))


def iter_points(bounds):
    return itertools.product(*(range(lo, hi + 1) for lo, hi in bounds))


# ---------------------------------------------------------------------
# Part 1: brute-force fine-lattice partition check. Every plaquette
# (fine base point, orientation) belongs to the star at its own coarse
# anchor if its class is an owner type, or to the single-factor group
# at its own coarse anchor if its class is `selected`. This is checked
# literally over the fine window underlying Lambda_2 (a coarse cube of
# 5^3=125 anchors, 8 fine (x mod 4, y mod 2) residues per anchor times
# 3 orientations = 3000 plaquette instances), matching the scale of
# the BC2 forward producer's own brute-force check (independently
# reproduced here, not read from its code).
# ---------------------------------------------------------------------

def brute_force_partition(N):
    bounds = lambda_bounds(N)
    groups = {}  # (kind, anchor) -> count of faces assigned
    total = 0
    for bx, by, bz in iter_points(bounds):
        for r in range(4):
            for s in range(2):
                for o in ORIENTATIONS:
                    x = 4 * bx + r
                    y = 2 * by + s
                    z = bz
                    anchor = pi(x, y, z)
                    assert anchor == (bx, by, bz)
                    cls = face_class(o, r, s)
                    total += 1
                    if cls == SELECTED:
                        key = ("single", anchor)
                    else:
                        key = ("star", anchor)
                    groups[key] = groups.get(key, 0) + 1
    # every plaquette in exactly one group, by construction of `groups`
    # (a dict keyed by (kind, anchor) is inherently a partition of the
    # `total` increments); verify the sizes independently:
    star_sizes = {v for (k, a), v in groups.items() if k == "star"}
    single_sizes = {v for (k, a), v in groups.items() if k == "single"}
    n_stars = sum(1 for (k, a) in groups if k == "star")
    n_singles = sum(1 for (k, a) in groups if k == "single")
    return {
        "total_plaquettes": total,
        "n_groups": len(groups),
        "n_star_groups": n_stars,
        "n_single_groups": n_singles,
        "star_sizes": sorted(star_sizes),
        "single_sizes": sorted(single_sizes),
        "sum_star_faces": sum(v for (k, a), v in groups.items() if k == "star"),
        "sum_single_faces": sum(v for (k, a), v in groups.items() if k == "single"),
    }


# ---------------------------------------------------------------------
# Part 2: per-site (per-factor) inputs, re-derived at coarse level.
# For a fixed factor u, find every face (owner type) whose absolute
# owner set contains u, by scanning the four incoming star anchors
# u-S and the single group at u.
# ---------------------------------------------------------------------

def per_site_inputs(u=ZERO):
    faces_from_stars = 0
    owner_sets = []  # (absolute frozenset, multiplicity)
    for b in [vadd(u, tuple(-c for c in d)) for d in S]:  # b in u - S
        rel = tuple(uc - bc for uc, bc in zip(u, b))  # u - b, a member of S
        for owner, mult in OWNER_TYPES:
            if rel in owner:
                abs_set = frozenset(vadd(b, d) for d in owner)
                owner_sets.append((abs_set, mult))
                faces_from_stars += mult
    # single group at b=u:
    single_owner, single_mult = SINGLE_TYPE
    abs_single = frozenset(vadd(u, d) for d in single_owner)
    owner_sets.append((abs_single, single_mult))
    faces_total = faces_from_stars + single_mult
    distinct_owner_sets = {s for s, m in owner_sets}
    assert len(distinct_owner_sets) == len(owner_sets), "owner sets must be pairwise distinct"
    mult_multiset = sorted(m for s, m in owner_sets)
    n_interaction_groups = 4 + 1  # 4 stars at u-S (incoming included) + 1 single at u
    return {
        "faces_omitted": faces_from_stars,
        "faces_selected": single_mult,
        "faces_total": faces_total,
        "n_owner_sets": len(owner_sets),
        "multiplicities_sorted": mult_multiset,
        "n_interaction_groups": n_interaction_groups,
    }


# ---------------------------------------------------------------------
# Part 3: incidence with R = {0, e_z}. A star at anchor b meets R iff
# (b+S) intersects R; a single group at anchor b meets R iff b in R
# (its support is {b} alone, so "meets" and "inside" coincide for
# singles). Face-level meeting/inside counts follow the same owner-set
# test as every_site_core.py's F2 rule, applied to route B's groups.
# ---------------------------------------------------------------------

R_COVER = [ZERO, EZ]


def star_anchors_meeting_R():
    out = set()
    for r_pt in R_COVER:
        for d in S:
            out.add(vadd(r_pt, tuple(-c for c in d)))  # b = r_pt - d
    return out


def route_b_incidence_on_R():
    star_anchors = sorted(star_anchors_meeting_R())
    table = []
    total_charged = total_meeting = total_inside = 0
    for b in star_anchors:
        meeting = inside = 0
        for owner, mult in OWNER_TYPES:
            abs_set = [vadd(b, d) for d in owner]
            if any(p in R_COVER for p in abs_set):
                meeting += mult
            if all(p in R_COVER for p in abs_set):
                inside += mult
        table.append({"group": "star", "anchor": b, "faces": 21, "meeting_R": meeting, "inside_R": inside})
        total_charged += 21
        total_meeting += meeting
        total_inside += inside
    single_anchors = sorted(p for p in R_COVER)  # single group at b meets/insides R iff b in R
    for b in single_anchors:
        table.append({"group": "single", "anchor": b, "faces": 3, "meeting_R": 3, "inside_R": 3})
        total_charged += 3
        total_meeting += 3
        total_inside += 3
    return {
        "n_stars_meeting_R": len(star_anchors),
        "n_singles_meeting_R": len(single_anchors),
        "faces_charged": total_charged,
        "meeting_R": total_meeting,
        "inside_R": total_inside,
        "straddling": total_meeting - total_inside,
        "table": table,
    }


# ---------------------------------------------------------------------
# Part 4: every-site common core for route B at N=2,3. Going from
# Lambda_N to Lambda_{N+1}, the new source terms are (a) the 21
# individual faces of every new whole star (anchor b with b+S subset
# Lambda_{N+1} but not subset Lambda_N) and (b) the 3 selected faces of
# every new single-factor group (anchor b in Lambda_{N+1} minus
# Lambda_N; every single group of the box is retained, AX1 Section 1).
# Every source face must lie at coarse l-infinity distance at least
# N-|u|_inf from every site u of Lambda_N (Lemma D5 of the BC2 forward
# report, re-derived here from scratch, not read from its proof).
# ---------------------------------------------------------------------

def whole_star_in(b, bounds):
    return all(in_box(vadd(b, d), bounds) for d in S)


def stars_retained(bounds):
    return {b for b in iter_points(bounds) if whole_star_in(b, bounds)}


def singles_retained(bounds):
    return set(iter_points(bounds))  # every single group of the box is kept


def check_common_core(N):
    bN = lambda_bounds(N)
    bN1 = lambda_bounds(N + 1)
    stars_N, stars_N1 = stars_retained(bN), stars_retained(bN1)
    singles_N, singles_N1 = singles_retained(bN), singles_retained(bN1)
    assert stars_N <= stars_N1 and singles_N <= singles_N1

    new_stars = stars_N1 - stars_N
    new_singles = singles_N1 - singles_N

    source_terms = []  # (kind, support)
    for b in new_stars:
        for owner, mult in OWNER_TYPES:
            support = [vadd(b, d) for d in owner]
            for _ in range(mult):
                source_terms.append(("omitted", support))
    for b in new_singles:
        owner, mult = SINGLE_TYPE
        support = [vadd(b, d) for d in owner]
        for _ in range(mult):
            source_terms.append(("selected", support))

    lam_n_points = list(iter_points(bN))
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

    n_selected = sum(1 for k, _ in source_terms if k == "selected")
    n_omitted = sum(1 for k, _ in source_terms if k == "omitted")
    return {
        "N": N,
        "comparison": "c1B Lambda_%d vs Lambda_%d" % (N, N + 1),
        "n_new_stars": len(new_stars),
        "n_new_singles": len(new_singles),
        "source_faces": len(source_terms),
        "selected_source_faces": n_selected,
        "omitted_source_faces": n_omitted,
        "num_sites_checked": len(lam_n_points),
        "min_slack": min_slack,
        "worst_case": worst,
        "ok": len(failures) == 0,
        "num_failures": len(failures),
    }


# Closed-form cross-check (route-B stars follow the same 8(3N^2+3N+1)
# route-A star count; new single anchors number (2N+3)^3-(2N+1)^3):
def closed_form_new_stars(N):
    return 8 * (3 * N * N + 3 * N + 1)


def closed_form_new_singles(N):
    return (2 * N + 3) ** 3 - (2 * N + 1) ** 3


# ---------------------------------------------------------------------
# Part 5: cross-check against the frozen BC2 contract, the AX1 gate,
# the AX1 forward report, and the BC2 forward report/results.json.
# ---------------------------------------------------------------------

def cross_check_sources():
    contract = load_json(BC2_CONTRACT)
    ax1_gate_text = load_text(AX1_GATE)
    ax1_report_text = load_text(AX1_REPORT)
    bc2_report_text = load_text(BC2_FWD_REPORT)
    bc2_results = load_json(BC2_FWD_RESULTS)

    checks = {}
    req1 = contract["required"][0]
    checks["contract_item1_has_7_stars_2_singles"] = "7 whole stars and 2 single-factor groups meet R" in req1
    checks["contract_item1_has_153_faces"] = "153 faces charged" in req1
    checks["contract_item1_has_88_meeting_R"] = "88 meeting R" in req1
    checks["contract_item1_has_16_inside_R"] = "16 inside R" in req1
    checks["contract_item1_has_72_straddling"] = "72 straddling" in req1
    checks["contract_item1_has_52_first_order"] = "52 first-order faces" in req1
    checks["contract_item1_has_5_interaction_groups"] = "5 interaction groups per site" in req1

    checks["ax1_gate_states_7_and_2"] = "7 whole stars (anchors R-S) and 2 single-factor groups meet R" in ax1_gate_text
    checks["ax1_report_states_52_faces_per_factor"] = "52 faces per factor" in ax1_report_text
    checks["ax1_report_states_4_stars_1_single"] = "in exactly four stars" in ax1_report_text and "exactly one single-factor group" in ax1_report_text

    checks["bc2_report_states_153_88_16_72"] = (
        "153 faces are charged" in bc2_report_text
        and "88 meet" in bc2_report_text
        and "16 lie inside" in bc2_report_text
        and "72 straddle" in bc2_report_text
    )
    checks["bc2_report_states_16_owner_sets"] = "owner sets containing `u`: **16**" in bc2_report_text
    checks["bc2_report_states_5_groups"] = "interaction groups containing `u`: **5**" in bc2_report_text
    checks["bc2_report_states_52_faces"] = "faces with `u` in their owner set" in bc2_report_text and "**52**" in bc2_report_text

    try:
        bc2_partition = bc2_results["checks"]
        found = None
        for c in bc2_partition:
            if c.get("id") == "route_b_partition_brute_force":
                found = c
                break
        checks["bc2_results_partition_found"] = found is not None
        if found is not None:
            checks["bc2_results_groups_250"] = found["partition"]["groups"] == 250
            checks["bc2_results_plaquettes_3000"] = found["partition"]["plaquettes"] == 3000
        found_incidence = None
        found_persite = None
        found_core = None
        for c in bc2_partition:
            if c.get("id") == "route_b_incidence_on_R":
                found_incidence = c
            if c.get("id") == "route_b_per_site_inputs_derived":
                found_persite = c
            if c.get("id") == "route_b_every_site_common_core":
                found_core = c
        checks["bc2_results_incidence_found"] = found_incidence is not None
        checks["bc2_results_persite_found"] = found_persite is not None
        checks["bc2_results_core_found"] = found_core is not None
    except Exception as exc:  # pragma: no cover
        checks["bc2_results_error"] = str(exc)

    return checks, bc2_results


def compare_with_bc2_results(bc2_results, incidence, persite, core_rows):
    comparisons = {}
    persite_c = None
    incidence_c = None
    core_c = []
    for c in bc2_results["checks"]:
        if c.get("id") == "route_b_per_site_inputs_derived":
            persite_c = c
        if c.get("id") == "route_b_incidence_on_R":
            incidence_c = c
        if c.get("id") == "route_b_every_site_common_core":
            core_c = c["rows"]

    if persite_c is not None:
        comparisons["faces_per_factor_matches"] = persite_c["faces_per_factor"] == persite["faces_total"]
        comparisons["owner_sets_per_factor_matches"] = persite_c["owner_sets_per_factor"] == persite["n_owner_sets"]
        comparisons["groups_per_site_matches"] = persite_c["groups_per_site"] == persite["n_interaction_groups"]
        comparisons["multiplicities_match"] = sorted(persite_c["multiplicities"]) == persite["multiplicities_sorted"]
        comparisons["omitted_matches"] = persite_c["omitted"] == persite["faces_omitted"]
        comparisons["selected_matches"] = persite_c["selected"] == persite["faces_selected"]

    if incidence_c is not None:
        n2 = incidence_c["N2"]
        comparisons["stars_meeting_R_matches"] = n2["stars"] == incidence["n_stars_meeting_R"]
        comparisons["singles_meeting_R_matches"] = n2["singles"] == incidence["n_singles_meeting_R"]
        comparisons["faces_charged_matches"] = n2["faces_charged"] == incidence["faces_charged"]
        comparisons["meeting_R_matches"] = n2["meeting_R"] == incidence["meeting_R"]
        comparisons["inside_R_matches"] = n2["inside_R"] == incidence["inside_R"]
        comparisons["straddling_matches"] = n2["straddling"] == incidence["straddling"]

    core_by_N = {}
    for row in core_c:
        if row.get("comparison", "").startswith("c1B"):
            core_by_N.setdefault(row["N"], row)
    for N in (2, 3):
        row = core_by_N.get(N)
        mine = next((r for r in core_rows if r["N"] == N), None)
        if row is not None and mine is not None:
            comparisons["N%d_source_faces_matches" % N] = row["source_faces"] == mine["source_faces"]
            comparisons["N%d_selected_source_faces_matches" % N] = (
                row["selected_source_faces"] == mine["selected_source_faces"]
            )
            comparisons["N%d_min_slack_matches" % N] = row["min_slack"] == mine["min_slack"]
            comparisons["N%d_ok_matches" % N] = row["ok"] == mine["ok"]

    return comparisons


def main():
    partition = brute_force_partition(2)
    persite = per_site_inputs(ZERO)
    incidence = route_b_incidence_on_R()
    core_rows = [check_common_core(2), check_common_core(3)]

    core_closed_form_ok = True
    for row in core_rows:
        N = row["N"]
        exp_stars = closed_form_new_stars(N)
        exp_singles = closed_form_new_singles(N)
        row["expected_new_stars_closed_form"] = exp_stars
        row["expected_new_singles_closed_form"] = exp_singles
        row["new_stars_matches_closed_form"] = row["n_new_stars"] == exp_stars
        row["new_singles_matches_closed_form"] = row["n_new_singles"] == exp_singles
        core_closed_form_ok = core_closed_form_ok and row["new_stars_matches_closed_form"] and row["new_singles_matches_closed_form"]

    cross, bc2_results = cross_check_sources()
    comparisons = compare_with_bc2_results(bc2_results, incidence, persite, core_rows)

    checks = {
        "partition_group_count_250": partition["n_groups"] == 250,
        "partition_plaquette_count_3000": partition["total_plaquettes"] == 3000,
        "partition_star_size_is_21": partition["star_sizes"] == [21],
        "partition_single_size_is_3": partition["single_sizes"] == [3],
        "partition_faces_sum_to_3000": (partition["sum_star_faces"] + partition["sum_single_faces"]) == 3000,
        "persite_faces_total_52": persite["faces_total"] == 52,
        "persite_owner_sets_16": persite["n_owner_sets"] == 16,
        "persite_groups_5": persite["n_interaction_groups"] == 5,
        "persite_multiplicities_expected": persite["multiplicities_sorted"] == [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 10, 10],
        "incidence_7_stars": incidence["n_stars_meeting_R"] == 7,
        "incidence_2_singles": incidence["n_singles_meeting_R"] == 2,
        "incidence_153_charged": incidence["faces_charged"] == 153,
        "incidence_88_meeting": incidence["meeting_R"] == 88,
        "incidence_16_inside": incidence["inside_R"] == 16,
        "incidence_72_straddling": incidence["straddling"] == 72,
        "core_N2_ok": core_rows[0]["ok"],
        "core_N3_ok": core_rows[1]["ok"],
        "core_closed_form_ok": core_closed_form_ok,
    }

    overall = all(checks.values()) and all(v for v in cross.values() if isinstance(v, bool)) and all(comparisons.values())

    report = {
        "script": "route_b_incidence.py",
        "task": "independent exact enumeration of the route-B partition, incidence and "
                "every-site common core of the BC2 uniform model, compared with the "
                "BC2 producer results and the AX1/AX2 gates",
        "partition_fine_grid_check": partition,
        "per_site_inputs": persite,
        "incidence_on_R": incidence,
        "every_site_common_core": core_rows,
        "checks": checks,
        "cross_check_against_frozen_sources": cross,
        "comparison_with_bc2_producer_results": comparisons,
        "overall_pass": overall,
    }
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
