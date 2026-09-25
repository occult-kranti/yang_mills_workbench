#!/usr/bin/env python3
"""
flip_sets.py
Historical (Newton/Tesla) lens research assistant, Round33 applications
stage (assistant-4). Zero research loops: an independent, from-scratch
exact enumeration of the BD1 flip sets E_3 (Z^3; the AW1 set) and
E_2 (Z^2), on the named boxes, on the 24-link coarse factors, and a
genuine GF(2) solvability check on five named periodic tori, compared
with the BD1 contract, the BD1 gate and the forward/reverse BD1 packets'
own recorded numbers.

This script never imports or executes research/round33/forward/bd1/
check.py, research/round33/reverse/bd1/check.py, or any other check.py.
It reads, as data only: research/round33/contracts/bd1.json (frozen),
research/round33/advisor/bd1-gate.json, research/round33/forward/bd1/
report.md and output/results.json, research/round33/reverse/bd1/
report.md and output/results.json, and research/round21/forward/i1/
report.md (prose only, for the coarse-factor link-ownership convention
and the 24-class anchored face table, sections 2-3). It never reads
research/round33/forward/bd2/, research/round33/skeptic/ (any file), or
any other assistant's scripts (only their README's layout convention is
followed, not their code).

Every construction below (the flip-set membership rule, the coarse
factor's 24 owned links, the whole-star box Lambda_N, the retained-face
count, and the periodic-torus GF(2) system) is re-derived from scratch
from the contract's own definition of E_3/E_2 and the I1 prose; it is
then cross-checked two independent ways against itself (a raw brute-force
enumeration of every plaquette owned by a box, versus a closed-form
per-anchor-type sum) before being compared against the forward and
reverse BD1 packets' own numbers.

Arithmetic: plain Python `int` and Python's builtin arbitrary-precision
integers used as GF(2) bit-vectors (XOR/AND/bit-length only) throughout.
No floats, no `Fraction` (every quantity here is an exact count or an
exact GF(2) linear-algebra fact).

Run with: python3 -B flip_sets.py
Also checked identical under: python3 -B -O flip_sets.py
"""
import itertools
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# HERE = .../research/round33/experts/historical/assistant-4
# up 5: assistant-4 -> historical -> experts -> round33 -> research -> <repo root>
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

BD1_CONTRACT = os.path.join(REPO_ROOT, "research/round33/contracts/bd1.json")
BD1_GATE = os.path.join(REPO_ROOT, "research/round33/advisor/bd1-gate.json")
BD1_FWD_REPORT = os.path.join(REPO_ROOT, "research/round33/forward/bd1/report.md")
BD1_FWD_RESULTS = os.path.join(REPO_ROOT, "research/round33/forward/bd1/output/results.json")
BD1_REV_REPORT = os.path.join(REPO_ROOT, "research/round33/reverse/bd1/report.md")
BD1_REV_RESULTS = os.path.join(REPO_ROOT, "research/round33/reverse/bd1/output/results.json")
I1_REPORT = os.path.join(REPO_ROOT, "research/round21/forward/i1/report.md")

FORBIDDEN_SUBSTRINGS = ("check.py", "forward/bd2", "skeptic/")


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def load_text(path):
    with open(path) as fh:
        return fh.read()


for _p in (BD1_CONTRACT, BD1_GATE, BD1_FWD_REPORT, BD1_FWD_RESULTS,
           BD1_REV_REPORT, BD1_REV_RESULTS, I1_REPORT):
    assert not any(f in _p for f in FORBIDDEN_SUBSTRINGS), _p


# =====================================================================
# Part 0: the flip sets, read from the contract text and re-derived
# independently as membership predicates (not copied combinatorics).
# =====================================================================

def e3_in(p, direction):
    """E_3 = {(p,x): p_y even} u {(p,y): p_z even} u {(p,z): p_x even}."""
    x, y, z = p
    if direction == "x":
        return y % 2 == 0
    if direction == "y":
        return z % 2 == 0
    if direction == "z":
        return x % 2 == 0
    raise AssertionError(direction)


def e2_in(p, direction):
    """E_2 = {(p,x): p_y even} on Z^2."""
    x, y = p
    if direction == "x":
        return y % 2 == 0
    if direction == "y":
        return False
    raise AssertionError(direction)


def vadd(p, offset):
    return tuple(a + b for a, b in zip(p, offset))


PLAQUETTE_ORIENTATIONS_3D = {
    "xy": ((1, 0, 0), "x", (0, 1, 0), "y"),
    "xz": ((1, 0, 0), "x", (0, 0, 1), "z"),
    "yz": ((0, 1, 0), "y", (0, 0, 1), "z"),
}


def plaquette_links_3d(p, orientation):
    """The four positively-oriented edges of the elementary face at base
    point p with the given orientation (a<c convention): two a-edges (at
    p and p+e_c) and two c-edges (at p and p+e_a)."""
    ea, da, ec, dc = PLAQUETTE_ORIENTATIONS_3D[orientation]
    return [
        (p, da),
        (vadd(p, ec), da),
        (p, dc),
        (vadd(p, ea), dc),
    ]


def plaquette_links_2d(p):
    """The single 2D plaquette type on Z^2 (orientation xy): two x-edges
    (at p and p+e_y) and two y-edges (at p and p+e_x)."""
    return [
        (p, "x"),
        (vadd(p, (0, 1)), "x"),
        (p, "y"),
        (vadd(p, (1, 0)), "y"),
    ]


def e3_count(p, orientation):
    return sum(1 for (q, d) in plaquette_links_3d(p, orientation) if e3_in(q, d))


def e2_count(p):
    return sum(1 for (q, d) in plaquette_links_2d(p) if e2_in(q, d))


# =====================================================================
# Part 1: E_3 meets every plaquette of Z^3 oddly; E_2 meets every
# plaquette of Z^2 exactly once. Checked over all 24 (orientation, p
# mod 2) residue classes for E_3 (with a second, independent covariance
# check under even translation) and all 4 (p mod 2) classes for E_2.
# =====================================================================

def check_e3_all_z3():
    residue_table = []
    all_odd = True
    for orientation in ("xy", "xz", "yz"):
        for px in (0, 1):
            for py in (0, 1):
                for pz in (0, 1):
                    base = (px, py, pz)
                    c = e3_count(base, orientation)
                    if c % 2 == 0:
                        all_odd = False
                    # covariance under even translation: sample eight
                    # even shifts and confirm the count is unchanged.
                    covariant = True
                    for sx, sy, sz in itertools.product((0, 2, -4, 6), repeat=3):
                        shifted = (px + sx, py + sy, pz + sz)
                        if e3_count(shifted, orientation) != c:
                            covariant = False
                            break
                    residue_table.append({
                        "orientation": orientation,
                        "base_parity": [px, py, pz],
                        "links_in_E3": c,
                        "odd": c % 2 == 1,
                        "covariant": covariant,
                    })
    n_classes = len(residue_table)
    all_covariant = all(r["covariant"] for r in residue_table)
    ones = sum(1 for r in residue_table if r["links_in_E3"] == 1)
    threes = sum(1 for r in residue_table if r["links_in_E3"] == 3)
    return {
        "n_classes": n_classes,
        "residue_table": residue_table,
        "all_odd": all_odd,
        "all_covariant": all_covariant,
        "count_value_1": ones,
        "count_value_3": threes,
    }


def check_e2_all_z2():
    residue_table = []
    all_exactly_one = True
    for px in (0, 1):
        for py in (0, 1):
            base = (px, py)
            c = e2_count(base)
            if c != 1:
                all_exactly_one = False
            residue_table.append({"base_parity": [px, py], "links_in_E2": c})
    return {
        "n_classes": len(residue_table),
        "residue_table": residue_table,
        "all_exactly_one": all_exactly_one,
    }


# =====================================================================
# Part 2: the coarse 24-link factor. Re-derived from I1 sections 2-3
# ("the block owns all three positively oriented links whose tail
# belongs to T_b"; the selected strip's six x tails and four y tails,
# plus the fourteen remaining links: two x separator links, four y
# links and eight z links -- 8 x-links + 8 y-links + 8 z-links = 24,
# one of each direction at each of the 8 fine points (4i+r,2j+s,k),
# r=0..3, s=0..1).
# =====================================================================

def factor_fine_points(b):
    i, j, k = b
    return [(4 * i + r, 2 * j + s, k) for r in range(4) for s in range(2)]


def factor_links(b):
    links = set()
    for p in factor_fine_points(b):
        for d in ("x", "y", "z"):
            links.add((p, d))
    return links


def check_factor_e3(b):
    links = factor_links(b)
    assert len(links) == 24
    in_e3 = [(p, d) for (p, d) in links if e3_in(p, d)]
    return {
        "z_parity": b[2] % 2,
        "links_in_E3": len(in_e3),
        "total_links": len(links),
    }


def coarse_factors_report():
    probed = [(0, 0, 0), (0, 0, 1), (1, 0, 0), (0, 1, 0), (1, 1, 1), (-1, -1, -1), (2, -3, 5)]
    per_factor = {}
    for b in probed:
        r = check_factor_e3(b)
        per_factor["%d,%d,%d" % b] = r
    # General rule, checked over a wide sample of anchors (independent
    # of the probed list): links_in_E3 = 16 if k even else 8.
    general_ok = True
    sample_range = range(-6, 7)
    for i in sample_range:
        for j in sample_range:
            for k in (-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6):
                r = check_factor_e3((i, j, k))
                expected = 16 if k % 2 == 0 else 8
                if r["links_in_E3"] != expected:
                    general_ok = False
    return {"per_factor": per_factor, "general_rule_16_or_8_by_z_parity_checked": general_ok}


# =====================================================================
# Part 3: the whole-star box Lambda_N = union of factor links for
# i,j,k in [-N,N] (this range, not [-N,N-1], is confirmed independently
# below by matching the total link count 24*(2N+1)^3 against the BD1
# packets' own reported "links" field). A face is "retained" only when
# the anchor's whole star (b, b+e_x, b+e_y, b+e_z in factor-index space)
# lies entirely in Lambda_N, i.e. i,j,k in [-N,N-1] -- giving (2N)^3
# retained anchors, matching the packets' own "anchors" field.
# =====================================================================

# The 24-class anchored face table (I1 sections 2-3), independently
# transcribed from the prose grep'd out of I1_REPORT above; the table
# itself is checked against the literal I1 text by
# `check_i1_table_in_report_text` below (a plain substring search, not
# a re-derivation from that text -- the geometric consequences of the
# table are what is exercised here).
ZERO3, EX3, EY3, EZ3 = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)

# Each entry: (orientation, r, s) -> "selected" or a frozenset owner
# (relative to the anchor, offsets in {0,ex,ey,ez}).
FACE_TABLE = {}
for r in range(3):
    FACE_TABLE[("xy", r, 0)] = "selected"
for r in range(3):
    FACE_TABLE[("xy", r, 1)] = frozenset([ZERO3, EY3])
FACE_TABLE[("xy", 3, 0)] = frozenset([ZERO3, EX3])
FACE_TABLE[("xy", 3, 1)] = frozenset([ZERO3, EX3, EY3])
for r in range(4):
    for s in range(2):
        FACE_TABLE[("xz", r, s)] = frozenset([ZERO3, EZ3]) if r in (0, 1, 2) else frozenset([ZERO3, EX3, EZ3])
for r in range(4):
    FACE_TABLE[("yz", r, 0)] = frozenset([ZERO3, EZ3])
    FACE_TABLE[("yz", r, 1)] = frozenset([ZERO3, EY3, EZ3])

assert len(FACE_TABLE) == 24
_n_selected = sum(1 for v in FACE_TABLE.values() if v == "selected")
_n_omitted = sum(1 for v in FACE_TABLE.values() if v != "selected")
assert _n_selected == 3 and _n_omitted == 21


def local_face_point(b, orientation, r, s):
    i, j, k = b
    return (4 * i + r, 2 * j + s, k)


def check_i1_table_in_report_text(i1_text):
    """A plain substring search confirming the literal I1 table rows
    this script's FACE_TABLE encodes are present in the frozen I1 text
    (data only; the table's geometric consequences, not this search,
    are what every other check below exercises)."""
    needles = [
        "xy: r=0,1,2; s=1", "{0,e_y}",
        "xy: r=3; s=0", "{0,e_x}",
        "xy: r=3; s=1", "{0,e_x,e_y}",
        "xz: r=0,1,2; s=0,1", "{0,e_z}",
        "xz: r=3; s=0,1", "{0,e_x,e_z}",
        "yz: r=0,1,2,3; s=0",
        "yz: r=0,1,2,3; s=1", "{0,e_y,e_z}",
    ]
    return {n: (n in i1_text) for n in needles}


def box_owned_links(N):
    owned = set()
    for i in range(-N, N + 1):
        for j in range(-N, N + 1):
            for k in range(-N, N + 1):
                owned |= factor_links((i, j, k))
    return owned


def brute_force_box(N):
    """Method A: raw brute force. Enumerate every plaquette (base point,
    orientation) in a padded window and keep those all four of whose
    links are owned; tally the E_3 histogram. Independent of the
    per-anchor face table."""
    owned = box_owned_links(N)
    x_lo, x_hi = -4 * N - 2, 4 * N + 4
    y_lo, y_hi = -2 * N - 2, 2 * N + 3
    z_lo, z_hi = -N - 2, N + 2
    n_owned = 0
    hist = {1: 0, 3: 0}
    for x in range(x_lo, x_hi):
        for y in range(y_lo, y_hi):
            for z in range(z_lo, z_hi):
                p = (x, y, z)
                for orientation in ("xy", "xz", "yz"):
                    links = plaquette_links_3d(p, orientation)
                    if all((q, d) in owned for (q, d) in links):
                        n_owned += 1
                        c = sum(1 for (q, d) in links if e3_in(q, d))
                        assert c in (1, 3)
                        hist[c] += 1
    return {
        "n_links_owned": len(owned),
        "n_plaquettes_owned": n_owned,
        "histogram": {"1": hist[1], "3": hist[3]},
    }


def anchor_based_box(N):
    """Method B: per-anchor closed-form sum using the 24-class face
    table and, for each factor b in [-N,N]^3, which of b's coarse
    neighbours (b+ex, b+ey, b+ez in factor-index space) are also inside
    the box -- an omitted face is owned exactly when every offset its
    own owner set needs is present; a selected face is always owned (it
    needs no neighbour); a face is *retained* only when b's whole star
    is present (all three neighbours), matching the Hamiltonian's own
    'retained when the whole star lies in Lambda_N' rule."""
    n_owned = 0
    hist_owned = {1: 0, 3: 0}
    n_retained = 0
    hist_retained = {1: 0, 3: 0}
    n_anchors_total = 0
    n_anchors_retained = 0
    for i in range(-N, N + 1):
        for j in range(-N, N + 1):
            for k in range(-N, N + 1):
                n_anchors_total += 1
                has_x = i < N
                has_y = j < N
                has_z = k < N
                whole_star = has_x and has_y and has_z
                if whole_star:
                    n_anchors_retained += 1
                for (orientation, r, s), owner in FACE_TABLE.items():
                    p = local_face_point((i, j, k), orientation, r, s)
                    c = e3_count(p, orientation)
                    if owner == "selected":
                        # always owned (single-factor support)
                        n_owned += 1
                        hist_owned[c] += 1
                        continue
                    needed = owner - {ZERO3}
                    needs_x = EX3 in needed
                    needs_y = EY3 in needed
                    needs_z = EZ3 in needed
                    owned_here = (not needs_x or has_x) and (not needs_y or has_y) and (not needs_z or has_z)
                    if owned_here:
                        n_owned += 1
                        hist_owned[c] += 1
                        if whole_star:
                            n_retained += 1
                            hist_retained[c] += 1
    return {
        "n_anchors_total": n_anchors_total,
        "n_anchors_retained": n_anchors_retained,
        "n_plaquettes_owned": n_owned,
        "histogram_owned": {"1": hist_owned[1], "3": hist_owned[3]},
        "n_retained_faces": n_retained,
        "histogram_retained": {"1": hist_retained[1], "3": hist_retained[3]},
    }


def closed_form_retained(N):
    return 21 * (2 * N) ** 3


def e2_box(N):
    """E_2 on the literal box [-N,N]^2: every plaquette with base point
    p in [-N,N-1]^2 (so p and p+e_x+e_y both lie in the box)."""
    n = 0
    hist_one = 0
    for x in range(-N, N):
        for y in range(-N, N):
            c = e2_count((x, y))
            n += 1
            if c == 1:
                hist_one += 1
    return {"plaquettes": n, "meeting_once": hist_one, "all_meet_once": hist_one == n}


# =====================================================================
# Part 4: periodic tori. A genuine GF(2) linear-algebra solvability
# check (Gaussian elimination over GF(2), bit-packed in Python ints) --
# not the closed-form rule -- for whether *some* link set meets every
# plaquette of the torus oddly, on the five named tori, plus the
# specific seam count when the *keyed* E_3/E_2 rule itself is applied
# with periodic wraparound.
# =====================================================================

def gf2_solvable(rows, n_vars):
    """rows: list of ints, bit i (i<n_vars) = coefficient of variable i,
    bit n_vars = right-hand side. Returns True iff the system is
    consistent (Gaussian elimination finds no row 0...0=1)."""
    rows = list(rows)
    pivot_col = 0
    n_rows = len(rows)
    row_idx = 0
    for col in range(n_vars):
        pivot = None
        for r in range(row_idx, n_rows):
            if (rows[r] >> col) & 1:
                pivot = r
                break
        if pivot is None:
            continue
        rows[row_idx], rows[pivot] = rows[pivot], rows[row_idx]
        for r in range(n_rows):
            if r != row_idx and (rows[r] >> col) & 1:
                rows[r] ^= rows[row_idx]
        row_idx += 1
    var_mask = (1 << n_vars) - 1
    for r in rows:
        if (r & var_mask) == 0 and ((r >> n_vars) & 1):
            # no variable bits set, RHS bit set -> the contradiction 0 = 1
            return False
    return True


def torus_e3_system(Lx, Ly, Lz):
    """Variables: links (p,d), p in the Lx*Ly*Lz torus, d in x,y,z.
    Equations: one per plaquette (3 orientations per site), RHS = 1."""
    var_index = {}
    idx = 0
    for x in range(Lx):
        for y in range(Ly):
            for z in range(Lz):
                for d in ("x", "y", "z"):
                    var_index[((x, y, z), d)] = idx
                    idx += 1
    n_vars = idx

    def wrap(p):
        x, y, z = p
        return (x % Lx, y % Ly, z % Lz)

    rows = []
    for x in range(Lx):
        for y in range(Ly):
            for z in range(Lz):
                p = (x, y, z)
                for orientation in ("xy", "xz", "yz"):
                    links = plaquette_links_3d(p, orientation)
                    row = 0
                    for (q, d) in links:
                        row |= 1 << var_index[(wrap(q), d)]
                    row |= 1 << n_vars  # RHS = 1
                    rows.append(row)
    return rows, n_vars


def torus_e2_system(Lx, Ly):
    var_index = {}
    idx = 0
    for x in range(Lx):
        for y in range(Ly):
            for d in ("x", "y"):
                var_index[((x, y), d)] = idx
                idx += 1
    n_vars = idx

    def wrap(p):
        x, y = p
        return (x % Lx, y % Ly)

    rows = []
    for x in range(Lx):
        for y in range(Ly):
            p = (x, y)
            links = plaquette_links_2d(p)
            row = 0
            for (q, d) in links:
                row |= 1 << var_index[(wrap(q), d)]
            row |= 1 << n_vars
            rows.append(row)
    return rows, n_vars


def keyed_e3_seam_count(Lx, Ly, Lz):
    """Apply the literal E_3 rule (not re-solved, just evaluated) with
    periodic wraparound coordinates and count plaquettes it meets an
    even number of times (the seam defect)."""
    even = 0
    total = 0
    for x in range(Lx):
        for y in range(Ly):
            for z in range(Lz):
                p = (x, y, z)
                for orientation in ("xy", "xz", "yz"):
                    total += 1
                    links = plaquette_links_3d(p, orientation)
                    c = 0
                    for (q, d) in links:
                        qx, qy, qz = q[0] % Lx, q[1] % Ly, q[2] % Lz
                        if e3_in((qx, qy, qz), d):
                            c += 1
                    if c % 2 == 0:
                        even += 1
    return {"plaquettes": total, "even_plaquettes_at_seam": even}


def keyed_e2_seam_count(Lx, Ly):
    even = 0
    total = 0
    for x in range(Lx):
        for y in range(Ly):
            p = (x, y)
            total += 1
            links = plaquette_links_2d(p)
            c = 0
            for (q, d) in links:
                qx, qy = q[0] % Lx, q[1] % Ly
                if e2_in((qx, qy), d):
                    c += 1
            if c % 2 == 0:
                even += 1
    return {"plaquettes": total, "even_plaquettes_at_seam": even}


def periodic_tori_report():
    """The five named tori: 4x3x4, 3x3x4 (E_3, 3D) and 4x3, 3x3, 3x4
    (E_2, 2D)."""
    result = {}
    for (Lx, Ly, Lz) in [(4, 3, 4), (3, 3, 4)]:
        rows, n_vars = torus_e3_system(Lx, Ly, Lz)
        solvable = gf2_solvable(rows, n_vars)
        seam = keyed_e3_seam_count(Lx, Ly, Lz)
        result["E3 on %dx%dx%d" % (Lx, Ly, Lz)] = {
            "gf2_some_flip_set_exists": solvable,
            "n_vars": n_vars,
            "n_equations": len(rows),
            "keyed_E3_rule": seam,
        }
    for (Lx, Ly) in [(4, 3), (3, 3), (3, 4)]:
        rows, n_vars = torus_e2_system(Lx, Ly)
        solvable = gf2_solvable(rows, n_vars)
        seam = keyed_e2_seam_count(Lx, Ly)
        result["E2 on %dx%d" % (Lx, Ly)] = {
            "gf2_some_flip_set_exists": solvable,
            "n_vars": n_vars,
            "n_equations": len(rows),
            "keyed_E2_rule": seam,
        }
    return result


# =====================================================================
# Part 5: comparison against the BD1 contract, gate, and the forward
# and reverse packets' own recorded numbers (data only).
# =====================================================================

def compare_with_sources(box_results, factor_results, e2_box_results, torus_results):
    contract = load_json(BD1_CONTRACT)
    gate_text = load_text(BD1_GATE)
    fwd_report = load_text(BD1_FWD_REPORT)
    fwd_results = load_json(BD1_FWD_RESULTS)
    rev_report = load_text(BD1_REV_REPORT)
    rev_results = load_json(BD1_REV_RESULTS)

    checks = {}
    fs = contract["parameters"]["flip_sets"]
    checks["contract_states_E3_formula"] = (
        "(p,x): p_y even" in fs and "(p,y): p_z even" in fs and "(p,z): p_x even" in fs
    )
    checks["contract_states_E2_formula"] = "E_2 = {(p,x): p_y even}" in fs
    checks["contract_names_N_2_3_4"] = "N=2,3,4" in fs

    fwd_check = None
    for c in fwd_results["checks"]:
        if c.get("id") == "flip_sets_verified":
            fwd_check = c
            break
    rev_checks_by_id = {c.get("id"): c for c in rev_results["checks"]}

    checks["fwd_flip_sets_verified_present"] = fwd_check is not None
    checks["fwd_flip_sets_verified_passed"] = bool(fwd_check and fwd_check.get("passed"))

    for N in (2, 3, 4):
        mine = box_results[N]
        checks["N%d_plaquettes_owned_methods_agree" % N] = (
            mine["brute_force"]["n_plaquettes_owned"] == mine["anchor_based"]["n_plaquettes_owned"]
        )
        checks["N%d_links_owned_methods_agree" % N] = (
            mine["brute_force"]["n_links_owned"] == 24 * (2 * N + 1) ** 3
        )
        checks["N%d_histogram_methods_agree" % N] = (
            mine["brute_force"]["histogram"] == mine["anchor_based"]["histogram_owned"]
        )
        checks["N%d_retained_matches_closed_form" % N] = (
            mine["anchor_based"]["n_retained_faces"] == closed_form_retained(N)
        )
        if fwd_check is not None:
            fwd_box = fwd_check["boxes"][str(N)]
            checks["N%d_fwd_plaquettes_owned_matches" % N] = (
                fwd_box["plaquettes_owned"] == mine["brute_force"]["n_plaquettes_owned"]
            )
            checks["N%d_fwd_links_matches" % N] = fwd_box["links"] == mine["brute_force"]["n_links_owned"]
            checks["N%d_fwd_retained_faces_matches" % N] = (
                fwd_box["retained_faces"] == mine["anchor_based"]["n_retained_faces"]
            )
            checks["N%d_fwd_histogram_matches" % N] = (
                fwd_box["plaquette_histogram"] == mine["brute_force"]["histogram"]
            )
            checks["N%d_fwd_retained_histogram_matches" % N] = (
                fwd_box["retained_histogram"] == mine["anchor_based"]["histogram_retained"]
            )
        rev_faces = rev_checks_by_id.get("flip_set_e3_boxes_and_retained_faces")
        if rev_faces is not None:
            rev_box = rev_faces["boxes"]["N=%d" % N]
            checks["N%d_rev_owned_matches" % N] = (
                rev_box["owned_plaquettes"] == mine["brute_force"]["n_plaquettes_owned"]
            )
            checks["N%d_rev_retained_faces_matches" % N] = (
                rev_box["retained_faces"] == mine["anchor_based"]["n_retained_faces"]
            )
            checks["N%d_rev_meet_once_matches" % N] = (
                rev_box["meet_once"] == mine["brute_force"]["histogram"]["1"]
            )
            checks["N%d_rev_meet_three_matches" % N] = (
                rev_box["meet_three_times"] == mine["brute_force"]["histogram"]["3"]
            )

    # coarse factors
    probed = [(0, 0, 0), (0, 0, 1), (1, 0, 0), (0, 1, 0), (1, 1, 1), (-1, -1, -1), (2, -3, 5)]
    checks["general_16_or_8_rule_checked"] = factor_results["general_rule_16_or_8_by_z_parity_checked"]
    if fwd_check is not None:
        fwd_factors = fwd_check["factors"]
        for b in probed:
            key = "%d,%d,%d" % b
            mine_v = factor_results["per_factor"][key]["links_in_E3"]
            fwd_v = fwd_factors[key]["links_in_E3"]
            checks["factor_%s_fwd_matches" % key.replace(",", "_").replace("-", "m")] = (mine_v == fwd_v)
    rev_factors = rev_checks_by_id.get("flip_set_e3_coarse_factors")
    if rev_factors is not None:
        checks["rev_even_z_links_16_matches"] = rev_factors["even_z_links"] == 16
        checks["rev_odd_z_links_8_matches"] = rev_factors["odd_z_links"] == 8

    # E2 boxes
    for N in (2, 3, 4):
        mine_e2 = e2_box_results[N]
        checks["E2_N%d_all_meet_once" % N] = mine_e2["all_meet_once"]
        if fwd_check is not None:
            fwd_e2 = fwd_check["E2_boxes"][str(N)]
            checks["E2_N%d_fwd_plaquettes_matches" % N] = fwd_e2["plaquettes"] == mine_e2["plaquettes"]
        rev_e2 = rev_checks_by_id.get("flip_set_e2_boxes")
        if rev_e2 is not None:
            checks["E2_N%d_rev_plaquettes_matches" % N] = rev_e2["plaquettes"]["N=%d" % N] == mine_e2["plaquettes"]

    # periodic tori: compare GF(2) existence and seam counts against
    # both producers' own remarks, for exactly the five requested tori.
    fwd_remark = fwd_check.get("remark_gf2_not_claimed", {}).get("any_flip_set_exists", {}) if fwd_check else {}
    fwd_e3_seams = fwd_check.get("periodic_tori_E3", {}) if fwd_check else {}
    fwd_e2_seams = fwd_check.get("periodic_tori_E2", {}) if fwd_check else {}
    rev_gf2 = rev_checks_by_id.get("finding_torus_flip_set_existence_gf2", {}).get("existence", {})
    rev_seam = rev_checks_by_id.get("periodic_tori_odd_side_recorded", {}).get("tori", {})

    torus_cross = {}
    mapping = {
        "E3 on 4x3x4": ("4x3x4", "E_3 on 4x3x4"),
        "E3 on 3x3x4": ("3x3x4", "E_3 on 3x3x4"),
        "E2 on 4x3": ("4x3", "E_2 on 4x3"),
        "E2 on 3x3": ("3x3", "E_2 on 3x3"),
        "E2 on 3x4": ("3x4", "E_2 on 3x4"),
    }
    for mine_key, (fwd_seam_key, rev_key) in mapping.items():
        mine_v = torus_results[mine_key]["gf2_some_flip_set_exists"]
        entry = {"mine_gf2_exists": mine_v}
        if rev_key in rev_gf2:
            entry["reverse_gf2_exists"] = rev_gf2[rev_key]
            entry["matches_reverse_gf2"] = (rev_gf2[rev_key] == mine_v)
        if fwd_seam_key in fwd_e3_seams:
            entry["forward_even_plaquettes_at_seam"] = fwd_e3_seams[fwd_seam_key]["even_plaquettes_at_seam"]
            entry["matches_forward_seam"] = (
                fwd_e3_seams[fwd_seam_key]["even_plaquettes_at_seam"]
                == torus_results[mine_key]["keyed_E3_rule"]["even_plaquettes_at_seam"]
            )
        if fwd_seam_key in fwd_e2_seams:
            entry["forward_even_plaquettes_at_seam"] = fwd_e2_seams[fwd_seam_key]["even_plaquettes_at_seam"]
            entry["matches_forward_seam"] = (
                fwd_e2_seams[fwd_seam_key]["even_plaquettes_at_seam"]
                == torus_results[mine_key]["keyed_E2_rule"]["even_plaquettes_at_seam"]
            )
        if fwd_remark and mine_key.split(" on ")[1] in fwd_remark:
            fwd_v = fwd_remark[mine_key.split(" on ")[1]]
            entry["forward_gf2_remark"] = fwd_v
            entry["matches_forward_gf2_remark"] = (fwd_v == mine_v)
        if rev_seam:
            rk = rev_key
            if rk in rev_seam:
                entry["reverse_seam_gf2_exists"] = rev_seam[rk]["any_flip_set_exists_gf2"]
                entry["matches_reverse_seam_gf2"] = (rev_seam[rk]["any_flip_set_exists_gf2"] == mine_v)
        torus_cross[mine_key] = entry

    for k, v in torus_cross.items():
        for kk, vv in v.items():
            if kk.startswith("matches_") and isinstance(vv, bool):
                checks["torus_%s_%s" % (k.replace(" ", "_"), kk)] = vv

    checks["bd1_gate_states_at_most_one_odd_side"] = "at most one odd side" in gate_text
    checks["bd1_gate_limitations_mentions_16_on_4x3x4"] = "16 on 3x4x4, 4x3x4" in gate_text
    checks["bd1_gate_limitations_mentions_24_on_3x3x4"] = "24 on 3x3x4" in gate_text
    checks["bd1_gate_limitations_mentions_4_on_4x3"] = "4 on the 4x3 torus" in gate_text

    return checks, torus_cross


def main():
    e3_all = check_e3_all_z3()
    e2_all = check_e2_all_z2()

    box_results = {}
    for N in (2, 3, 4):
        box_results[N] = {
            "brute_force": brute_force_box(N),
            "anchor_based": anchor_based_box(N),
        }

    factor_results = coarse_factors_report()
    i1_text = load_text(I1_REPORT)
    table_cross_check = check_i1_table_in_report_text(i1_text)

    e2_box_results = {N: e2_box(N) for N in (2, 3, 4)}

    torus_results = periodic_tori_report()

    checks, torus_cross = compare_with_sources(box_results, factor_results, e2_box_results, torus_results)

    structural_checks = {
        "e3_all_24_classes_odd": e3_all["all_odd"],
        "e3_all_24_classes_covariant_under_even_translation": e3_all["all_covariant"],
        "e3_n_classes_24": e3_all["n_classes"] == 24,
        "e3_ones_equal_threes": e3_all["count_value_1"] == e3_all["count_value_3"] == 12,
        "e2_all_4_classes_equal_one": e2_all["all_exactly_one"],
        "i1_table_needles_all_present": all(table_cross_check.values()),
    }
    for N in (2, 3, 4):
        structural_checks["N%d_methods_cross_consistent" % N] = (
            box_results[N]["brute_force"]["n_plaquettes_owned"]
            == box_results[N]["anchor_based"]["n_plaquettes_owned"]
        )

    all_checks = dict(structural_checks)
    all_checks.update(checks)
    overall = all(all_checks.values())

    report = {
        "script": "flip_sets.py",
        "task": "independent exact enumeration of the flip sets E_3 (Z^3, the AW1 set) and "
                "E_2 (Z^2) on the named boxes, the 24-link coarse factors, and a GF(2) "
                "solvability check on five named periodic tori, compared with the BD1 "
                "contract, gate and the forward/reverse BD1 packets",
        "e3_all_z3": e3_all,
        "e2_all_z2": e2_all,
        "boxes": {
            str(N): {
                "brute_force": box_results[N]["brute_force"],
                "anchor_based": box_results[N]["anchor_based"],
                "closed_form_retained_21_times_2N_cubed": closed_form_retained(N),
            }
            for N in (2, 3, 4)
        },
        "coarse_factors": factor_results,
        "i1_table_needles_found_in_text": table_cross_check,
        "e2_boxes": e2_box_results,
        "periodic_tori": torus_results,
        "periodic_tori_cross_comparison": torus_cross,
        "structural_checks": structural_checks,
        "cross_checks": checks,
        "checks": all_checks,
        "overall_pass": overall,
    }
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
