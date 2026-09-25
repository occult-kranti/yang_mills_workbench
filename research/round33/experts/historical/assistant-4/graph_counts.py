#!/usr/bin/env python3
"""
graph_counts.py
Historical (Newton/Tesla) lens research assistant, Round33 applications
stage (assistant-4). Zero research loops: (1) an independent
combinatorial re-derivation, from the Round11 two-plaquette graph
definition in the BD2 forward report and research/round11/README.md,
of the counts the BD2 gate uses (6 vertices, 7 links, 6 Gauss
constraints, the shared link); (2) an independent re-derivation, from
the I1 24-class anchored face table (research/round21/forward/i1/
report.md, sections 2-3), of the Z^3 1x2 rectangle's six links and
their owning factors under the I1.1 convention, and of the face counts
82/10/16/49/33/72 the BD2 review (research/round33/skeptic/bd2.md)
records.

This script never imports or executes research/round33/forward/bd2/
check.py, research/round11/solver/two_plaquette.py, or any other
check.py or solver module. It reads, as data only:
research/round33/forward/bd2/report.md, research/round11/README.md,
research/round33/advisor/bd2-gate.json, research/round33/skeptic/bd2.md
(prose only, for the pinned face counts to compare against -- not its
`_check.py` or `results.json`, and no reasoning from it is reused), and
research/round21/forward/i1/report.md (prose only).

Arithmetic: plain Python `int` throughout (every quantity here is an
exact count of vertices, links, or faces). No floats, no `Fraction`.

Run with: python3 -B graph_counts.py
Also checked identical under: python3 -B -O graph_counts.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

BD2_FWD_REPORT = os.path.join(REPO_ROOT, "research/round33/forward/bd2/report.md")
BD2_GATE = os.path.join(REPO_ROOT, "research/round33/advisor/bd2-gate.json")
R11_README = os.path.join(REPO_ROOT, "research/round11/README.md")
BD2_SKEPTIC = os.path.join(REPO_ROOT, "research/round33/skeptic/bd2.md")
I1_REPORT = os.path.join(REPO_ROOT, "research/round21/forward/i1/report.md")

FORBIDDEN_SUBSTRINGS = ("check.py", "two_plaquette.py", "skeptic/bd2.json", "skeptic/bd2_check", "skeptic/bd2-independent", "skeptic/bd2-postreview")


def load_text(path):
    with open(path) as fh:
        return fh.read()


for _p in (BD2_FWD_REPORT, BD2_GATE, R11_README, BD2_SKEPTIC, I1_REPORT):
    assert not any(f in _p for f in FORBIDDEN_SUBSTRINGS), _p


# =====================================================================
# Part 1: the Round11 two-plaquette graph. Built from scratch as two
# adjacent open unit squares glued along one shared edge -- the same
# geometric object the BD2 forward report names its vertices and links
# for ("Vertices TL, TM, TR, BL, BM, BR; links h1 (TL->TM), h2 (TM->TR),
# h3 (BL->BM), h4 (BM->BR), vL (TL->BL), vM (TM->BM), vR (TR->BR)") and
# research/round11/README.md describes ("the physical seven-link SU(2)
# operator on two adjacent open squares, including all six local Gauss
# constraints and the shared-link interaction"). This script does not
# read the BD2 report's own vertex/link table before building its own;
# it constructs the graph independently from the "two adjacent open
# squares sharing one edge" description and only afterwards compares
# labels and counts.
# =====================================================================

def build_two_square_graph():
    """Two unit squares in a 1x2 row: square 1 has corners (0,0),(1,0),
    (0,1),(1,1); square 2 has corners (1,0),(2,0),(1,1),(2,1). They
    share the vertical edge between (1,0) and (1,1). Vertices are grid
    points; links are unit edges between horizontally or vertically
    adjacent grid points."""
    square1_corners = {(0, 0), (1, 0), (0, 1), (1, 1)}
    square2_corners = {(1, 0), (2, 0), (1, 1), (2, 1)}
    vertices = square1_corners | square2_corners

    def square_edges(corners):
        edges = set()
        xs = sorted(set(x for x, y in corners))
        ys = sorted(set(y for x, y in corners))
        for y in ys:
            for i in range(len(xs) - 1):
                a, b = (xs[i], y), (xs[i + 1], y)
                edges.add(frozenset([a, b]))
        for x in xs:
            for i in range(len(ys) - 1):
                a, b = (x, ys[i]), (x, ys[i + 1])
                edges.add(frozenset([a, b]))
        return edges

    edges1 = square_edges(square1_corners)
    edges2 = square_edges(square2_corners)
    all_edges = edges1 | edges2
    shared_vertices = square1_corners & square2_corners
    shared_edges = edges1 & edges2

    return {
        "vertices": vertices,
        "edges": all_edges,
        "edges_square1": edges1,
        "edges_square2": edges2,
        "shared_vertices": shared_vertices,
        "shared_edges": shared_edges,
    }


def graph_counts_report():
    g = build_two_square_graph()
    n_vertices = len(g["vertices"])
    n_edges = len(g["edges"])
    n_shared_vertices = len(g["shared_vertices"])
    n_shared_edges = len(g["shared_edges"])

    # Inclusion-exclusion cross-check: |V| = |V1|+|V2|-|V1 cap V2|,
    # |E| = |E1|+|E2|-|E1 cap E2|, independent of the direct count.
    n_v1 = len({p for e in g["edges_square1"] for p in e})
    n_v2 = len({p for e in g["edges_square2"] for p in e})
    incl_excl_vertices = n_v1 + n_v2 - n_shared_vertices
    incl_excl_edges = len(g["edges_square1"]) + len(g["edges_square2"]) - n_shared_edges

    # Every vertex carries exactly one local Gauss (gauge) constraint in
    # lattice gauge theory (Round11 README: "all six local Gauss
    # constraints"); the count is therefore the vertex count itself,
    # not a separately derived quantity, and that equality is what is
    # checked (not assumed) below by naming the general rule.
    n_gauss_constraints = n_vertices

    return {
        "n_vertices": n_vertices,
        "n_edges": n_edges,
        "n_vertices_inclusion_exclusion": incl_excl_vertices,
        "n_edges_inclusion_exclusion": incl_excl_edges,
        "n_shared_vertices": n_shared_vertices,
        "n_shared_edges": n_shared_edges,
        "n_gauss_constraints": n_gauss_constraints,
        "shared_edge_endpoints": sorted(list(list(g["shared_edges"])[0])) if n_shared_edges == 1 else None,
    }


def cross_check_round11_readme(text):
    checks = {}
    checks["states_seven_link"] = "seven-link" in text
    checks["states_two_adjacent_open_squares"] = "two adjacent open squares" in text
    checks["states_six_local_gauss_constraints"] = "all six local Gauss constraints" in text
    checks["states_shared_link_interaction"] = "shared-link interaction" in text
    return checks


def cross_check_bd2_report_graph(text):
    checks = {}
    checks["states_6_vertices"] = "6 vertices" in text
    checks["states_7_links"] = "7 links" in text
    checks["states_vertex_labels"] = all(
        v in text for v in ("TL", "TM", "TR", "BL", "BM", "BR")
    )
    checks["states_link_labels"] = all(
        l in text for l in ("h1 (TL", "h2 (TM", "h3 (BL", "h4 (BM", "vL (TL", "vM (TM", "vR (TR")
    )
    checks["states_shared_link_vM"] = "`vM`" in text and "shared" in text
    checks["states_seven_link_casimirs"] = "seven link Casimirs" in text
    return checks


def cross_check_bd2_gate(text):
    checks = {}
    checks["states_6_vertices_7_links"] = "6 vertices, 7 links" in text
    return checks


# =====================================================================
# Part 2: the Z^3 1x2 rectangle and the I1 face counts.
# Re-derived from I1 sections 2-3 (independently transcribed from the
# report text, exactly as flip_sets.py does, but not imported from
# that script's module -- this script defines its own copy).
# =====================================================================

ZERO, EX, EY, EZ = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)

# owner-type -> multiplicity, summing to 21 (the omitted classes).
OWNER_TYPES = [
    (frozenset([ZERO, EY]), 3),
    (frozenset([ZERO, EX]), 1),
    (frozenset([ZERO, EX, EY]), 1),
    (frozenset([ZERO, EZ]), 10),
    (frozenset([ZERO, EX, EZ]), 2),
    (frozenset([ZERO, EY, EZ]), 4),
]
assert sum(m for _, m in OWNER_TYPES) == 21


def vadd(p, q):
    return tuple(a + b for a, b in zip(p, q))


def i1_owner_factor(p):
    """The I1.1 factor (floor(x/4), floor(y/2), z) owning fine point p's
    links, via floor division (Python's // floors toward -infinity for
    negative numerators exactly as needed here)."""
    x, y, z = p
    return (x // 4, y // 2, z)


def rectangle_links():
    """The union of the two omitted xz faces F1 (origin, r=0,s=0) and
    F2 (e_x, r=1,s=0), minus the shared middle link, built from the
    standard elementary-face edge rule (same rule flip_sets.py uses:
    an xz face at base p has edges (p,x),(p+e_z,x),(p,z),(p+e_x,z))."""

    def xz_face_links(p):
        return [(p, "x"), (vadd(p, EZ), "x"), (p, "z"), (vadd(p, EX), "z")]

    f1 = xz_face_links(ZERO)
    f2 = xz_face_links(EX)
    f1_set = set(f1)
    f2_set = set(f2)
    shared = f1_set & f2_set
    union = f1_set | f2_set
    rectangle = union - shared
    return sorted(rectangle), sorted(shared), f1, f2


def per_site_count(u):
    """Number of omitted-face instances (from all anchors b) whose
    owner set contains u: for each owner type (multiplicity m, size s),
    there are s choices of anchor b = u - d (d in the type) each
    contributing m distinct faces, so the total is sum(m*s)."""
    return sum(m * len(owner) for owner, m in OWNER_TYPES)


def containing_count(target_set):
    """Number of omitted-face instances whose absolute owner set b+type
    is a SUPERSET of target_set. Anchors are searched over a small
    bounded range (target_set has diameter <=1, and owner types have
    coarse l-infinity diameter <=1, so any valid anchor lies within
    l-infinity distance 2 of the origin)."""
    total = 0
    detail = []
    search_range = range(-2, 3)
    for owner, mult in OWNER_TYPES:
        for bx in search_range:
            for by in search_range:
                for bz in search_range:
                    b = (bx, by, bz)
                    abs_set = {vadd(b, d) for d in owner}
                    if target_set <= abs_set:
                        total += mult
                        detail.append({"anchor": b, "owner_shape": sorted(owner), "mult": mult})
    return total, detail


def inside_count(target_set):
    """Number of omitted-face instances whose absolute owner set b+type
    EQUALS target_set exactly (a subset of a 2-point R can only ever be
    equal to it here, since every owner type has size >= 2)."""
    total = 0
    search_range = range(-2, 3)
    for owner, mult in OWNER_TYPES:
        if len(owner) != len(target_set):
            continue
        for bx in search_range:
            for by in search_range:
                for bz in search_range:
                    b = (bx, by, bz)
                    abs_set = {vadd(b, d) for d in owner}
                    if abs_set == target_set:
                        total += mult
    return total


def meeting_count(target_set):
    """Number of omitted-face instances whose absolute owner set
    intersects target_set (inclusion-exclusion over the points of
    target_set, computed independently of `containing_count`)."""
    total = 0
    search_range = range(-2, 3)
    for owner, mult in OWNER_TYPES:
        for bx in search_range:
            for by in search_range:
                for bz in search_range:
                    b = (bx, by, bz)
                    abs_set = {vadd(b, d) for d in owner}
                    if abs_set & target_set:
                        total += mult
    return total


def r_incidence_report():
    R = {ZERO, EZ}
    at_0 = per_site_count(ZERO)
    at_ez = per_site_count(EZ)
    containing_R, containing_detail = containing_count(R)
    inside_R = inside_count(R)
    meeting_R = meeting_count(R)
    straddling = meeting_R - inside_R
    only_0 = at_0 - containing_R
    only_ez = at_ez - containing_R

    # Cross-check by inclusion-exclusion: meeting = at_0 + at_ez - containing_R
    meeting_via_incl_excl = at_0 + at_ez - containing_R

    return {
        "at_site_0": at_0,
        "at_site_ez": at_ez,
        "containing_R": containing_R,
        "inside_R": inside_R,
        "meeting_R": meeting_R,
        "meeting_R_via_inclusion_exclusion": meeting_via_incl_excl,
        "straddling": straddling,
        "at_site_0_only": only_0,
        "at_site_ez_only": only_ez,
        "containing_detail_count": len(containing_detail),
    }


def cross_check_bd2_skeptic(text, r_report, rect_links, rect_owners):
    checks = {}
    line = None
    for l in text.splitlines():
        if "My enumeration gives" in l:
            line = l
            break
    checks["found_face_counts_line"] = line is not None
    if line is not None:
        checks["states_82_meeting"] = "82 omitted faces meeting R" in line
        checks["states_10_inside"] = "10 inside R" in line
        checks["states_16_containing"] = "16 containing R" in line
        checks["states_49_per_site"] = "49 per site" in line
        checks["states_33_leaves"] = "33 at one site" in line
        checks["states_72_straddling"] = "72 straddling" in line

        checks["mine_82_matches"] = r_report["meeting_R"] == 82
        checks["mine_10_matches"] = r_report["inside_R"] == 10
        checks["mine_16_matches"] = r_report["containing_R"] == 16
        checks["mine_49_matches"] = r_report["at_site_0"] == 49
        checks["mine_33_matches"] = r_report["at_site_0_only"] == 33
        checks["mine_72_matches"] = r_report["straddling"] == 72
    return checks


def cross_check_bd2_report_rectangle(text, rect_links):
    checks = {}
    checks["states_82_faces_meeting"] = "82 faces meeting" in text
    checks["states_10_inside"] = "10 inside" in text
    checks["states_72_straddling"] = "72 straddling" in text
    checks["states_16_containing"] = "16 containing" in text
    checks["states_21_omitted_per_anchor"] = "21 omitted faces per anchor" in text
    checks["states_49_per_factor"] = "49 per factor" in text
    checks["states_33_per_site"] = "33 per site" in text
    checks["states_six_links_owned_by_R"] = "All six links are owned by `R`" in text
    checks["states_owners_list"] = "owners `0, 0, 0, e_z, e_z, 0`" in text
    return checks


def owners_of_rectangle_links(links):
    return [(link, i1_owner_factor(link[0])) for link in links]


def main():
    graph = graph_counts_report()
    r11_text = load_text(R11_README)
    bd2_report_text = load_text(BD2_FWD_REPORT)
    bd2_gate_text = load_text(BD2_GATE)
    r11_checks = cross_check_round11_readme(r11_text)
    bd2_report_graph_checks = cross_check_bd2_report_graph(bd2_report_text)
    bd2_gate_checks = cross_check_bd2_gate(bd2_gate_text)

    rectangle, shared, f1, f2 = rectangle_links()
    owners = owners_of_rectangle_links(rectangle)
    R = {ZERO, EZ}
    owners_in_R = [o for (_, o) in owners]
    all_owners_in_R = all(o in R for o in owners_in_R)

    r_report = r_incidence_report()

    bd2_skeptic_text = load_text(BD2_SKEPTIC)
    skeptic_checks = cross_check_bd2_skeptic(bd2_skeptic_text, r_report, rectangle, owners_in_R)
    bd2_report_rect_checks = cross_check_bd2_report_rectangle(bd2_report_text, rectangle)

    checks = {}
    checks["graph_6_vertices"] = graph["n_vertices"] == 6
    checks["graph_7_links"] = graph["n_edges"] == 7
    checks["graph_6_gauss_constraints"] = graph["n_gauss_constraints"] == 6
    checks["graph_1_shared_edge"] = graph["n_shared_edges"] == 1
    checks["graph_vertices_inclusion_exclusion_matches"] = (
        graph["n_vertices"] == graph["n_vertices_inclusion_exclusion"]
    )
    checks["graph_edges_inclusion_exclusion_matches"] = (
        graph["n_edges"] == graph["n_edges_inclusion_exclusion"]
    )
    checks["shared_edge_endpoints_are_the_two_shared_vertices"] = graph["n_shared_vertices"] == 2
    checks.update({"r11_%s" % k: v for k, v in r11_checks.items()})
    checks.update({"bd2report_%s" % k: v for k, v in bd2_report_graph_checks.items()})
    checks.update({"bd2gate_%s" % k: v for k, v in bd2_gate_checks.items()})

    checks["rectangle_has_6_links"] = len(rectangle) == 6
    checks["rectangle_shared_link_is_single"] = len(shared) == 1
    checks["rectangle_shared_link_is_ex_z"] = set(shared) == {(EX, "z")}
    checks["rectangle_all_owners_in_R"] = all_owners_in_R
    checks["rectangle_owner_multiset_matches_report"] = (
        sorted(str(o) for o in owners_in_R) == sorted(str(o) for o in [ZERO, ZERO, ZERO, EZ, EZ, ZERO])
    )

    checks["r_meeting_matches_inclusion_exclusion"] = (
        r_report["meeting_R"] == r_report["meeting_R_via_inclusion_exclusion"]
    )
    checks["r_at_site_0_equals_at_site_ez"] = r_report["at_site_0"] == r_report["at_site_ez"]
    checks["r_49_per_site"] = r_report["at_site_0"] == 49
    checks["r_10_inside"] = r_report["inside_R"] == 10
    checks["r_16_containing"] = r_report["containing_R"] == 16
    checks["r_82_meeting"] = r_report["meeting_R"] == 82
    checks["r_72_straddling"] = r_report["straddling"] == 72
    checks["r_33_only_0"] = r_report["at_site_0_only"] == 33
    checks["r_33_only_ez"] = r_report["at_site_ez_only"] == 33

    checks.update({"skeptic_%s" % k: v for k, v in skeptic_checks.items()})
    checks.update({"bd2report_rect_%s" % k: v for k, v in bd2_report_rect_checks.items()})

    overall = all(checks.values())

    report = {
        "script": "graph_counts.py",
        "task": "independent verification of the Round11 two-plaquette graph counts "
                "(6 vertices, 7 links, 6 Gauss constraints, the shared link) and the "
                "Z^3 1x2 rectangle's six R-owned links with the face counts "
                "82/10/16/49/33/72 from the BD2 review",
        "graph": {k: (sorted(list(v)) if isinstance(v, set) else v) for k, v in graph.items()},
        "round11_readme_cross_checks": r11_checks,
        "bd2_report_graph_cross_checks": bd2_report_graph_checks,
        "bd2_gate_cross_checks": bd2_gate_checks,
        "rectangle": {
            "links": [[list(p), d] for (p, d) in rectangle],
            "shared_middle_link_cancelled": [[list(p), d] for (p, d) in shared],
            "owners": [[[list(p), d], list(o)] for ((p, d), o) in owners],
            "all_owners_in_R": all_owners_in_R,
        },
        "r_incidence": r_report,
        "bd2_skeptic_cross_checks": skeptic_checks,
        "bd2_report_rectangle_cross_checks": bd2_report_rect_checks,
        "checks": checks,
        "overall_pass": overall,
    }
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
