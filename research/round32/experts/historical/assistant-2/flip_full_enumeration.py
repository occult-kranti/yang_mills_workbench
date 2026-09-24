#!/usr/bin/env python3
"""
T1 -- flip_full_enumeration.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 2.

Zero research loops: this is a test/planning script for the lens, not a
producer, skeptic or advisor artifact. It does not read or import
research/round32/forward/aw1/check.py or research/round32/reverse/aw1/check.py
or their source; the geometry helpers below are a fresh re-implementation
of the same I1.4 face-link rule used (independently, and disclosed) by
research/round32/experts/historical/assistant-1/haar_parity_exact.py
(S1), reused here per update-1.md's own suggestion (section 3, item 2)
and per the task's instruction to reuse assistant-1's work by import or
copy rather than read a producer's check.py.

Task (update-1.md section 5, test 1):
  Full enumeration (3 orientations x 49 faces [extended here to every
  plaquette of an 8x8x8 fine block]) of odd |face_links(f) & E| for the
  AW1 flip set

      E = {(p,x): p_y even} u {(p,y): p_z even} u {(p,z): p_x even}

  independent of AW1/AW2 check.py.

Pass iff:
  (i)  every plaquette of the 8x8x8 fine block (all three orientations,
       all base points p in {0,...,7}^3) meets E in an ODD number of
       links -- i.e. the count of plaquettes meeting E in an EVEN
       number of links (0, 2 or 4) is exactly zero;
  (ii) the count split between "meets E in 1 link" and "meets E in 3
       links" is reported (both AW1's forward and reverse producers,
       and the historical lens's own advisor/deliberation-2.md note,
       report only ODD counts in {1,3}; this script confirms that
       split exactly on an independent block).

Arithmetic: this check is purely combinatorial (link membership in a
fixed integer point-set); every quantity is an exact Python int, never
a float. Run with: python3 -B flip_full_enumeration.py
"""
import itertools
import json
import sys
from collections import Counter

DIRS = ("x", "y", "z")


def unit(d):
    v = [0, 0, 0]
    v[DIRS.index(d)] = 1
    return tuple(v)


def padd(p, v):
    return (p[0] + v[0], p[1] + v[1], p[2] + v[2])


def face_links(p, a, c):
    """
    I1.4 face-link rule (same convention as assistant-1's S1 and as the
    AW1 contract/producers): the face at fine base point p, orientation
    a<c, has the four positive (tail, direction) links
        (p,a), (p+e_a,c), (p+e_c,a), (p,c).
    """
    assert DIRS.index(a) < DIRS.index(c)
    ea, ec = unit(a), unit(c)
    return [(p, a), (padd(p, ea), c), (padd(p, ec), a), (p, c)]


def in_E(tail, direction):
    """
    The AW1 contract's flip set, read from research/round32/contracts/aw1.json
    and reproduced verbatim in research/round32/advisor/aw1-gate.json:

        E = {(p,x): p_y even} u {(p,y): p_z even} u {(p,z): p_x even}.
    """
    x, y, z = tail
    if direction == "x":
        return y % 2 == 0
    if direction == "y":
        return z % 2 == 0
    if direction == "z":
        return x % 2 == 0
    raise ValueError(direction)


ORIENTATIONS = (("x", "y"), ("x", "z"), ("y", "z"))
BLOCK = 8  # the 8x8x8 fine block named by the task


def enumerate_block(n=BLOCK):
    """
    Every plaquette of the n x n x n fine block: n^3 base points, 3
    orientations each. Returns a list of (p, a, c, links, count_in_E).
    """
    rows = []
    for px, py, pz in itertools.product(range(n), repeat=3):
        p = (px, py, pz)
        for a, c in ORIENTATIONS:
            links = face_links(p, a, c)
            count = sum(1 for (tail, d) in links if in_E(tail, d))
            rows.append((p, a, c, links, count))
    return rows


def parity_class_check(rows):
    """
    Cross-check: |face_links(f) & E| depends only on orientation and on
    p mod 2 (translation covariance by any even vector), so there are
    exactly 3 orientations x 8 parity classes = 24 classes. Confirm
    every base point with the same (orientation, p mod 2) gives the same
    count, independent of the brute-force per-plaquette computation
    above.
    """
    class_counts = {}
    consistent = True
    for p, a, c, links, count in rows:
        key = (a, c, tuple(v % 2 for v in p))
        if key not in class_counts:
            class_counts[key] = count
        elif class_counts[key] != count:
            consistent = False
    return consistent, len(class_counts), class_counts


def main():
    n = BLOCK
    rows = enumerate_block(n)
    total = len(rows)
    assert total == 3 * n ** 3

    hist = Counter(count for (_, _, _, _, count) in rows)
    even_hits = sum(v for k, v in hist.items() if k % 2 == 0)
    odd_hits = sum(v for k, v in hist.items() if k % 2 == 1)
    count_1 = hist.get(1, 0)
    count_3 = hist.get(3, 0)

    consistent, n_classes, class_counts = parity_class_check(rows)
    # every class value must itself be odd
    classes_all_odd = all(v % 2 == 1 for v in class_counts.values())

    # An explicit damaging-mutation control: dropping one link from E
    # (E_minus = E \ {a single fixed link, here every (p,x) link with
    # p==(0,0,0)}) must produce an EVEN intersection for at least one
    # plaquette that used to meet E oddly through that very link.
    def in_E_minus_one_link(tail, direction):
        if (tail, direction) == ((0, 0, 0), "x"):
            return False
        return in_E(tail, direction)

    mutation_face = ((0, 0, 0), "x", "z")  # this is exactly W's own face
    mutation_links = face_links((0, 0, 0), "x", "z")
    mutation_count_before = sum(1 for (t, d) in mutation_links if in_E(t, d))
    mutation_count_after = sum(1 for (t, d) in mutation_links if in_E_minus_one_link(t, d))
    mutation_rejected = (mutation_count_before % 2 == 1) and (mutation_count_after % 2 == 0)

    overall_pass = bool(
        even_hits == 0
        and odd_hits == total
        and count_1 + count_3 == total
        and consistent
        and classes_all_odd
        and n_classes == 24
        and mutation_rejected
    )

    result = {
        "script": "flip_full_enumeration.py",
        "zero_research_loops": True,
        "arithmetic": "exact integers only (link-membership combinatorics); no floats",
        "flip_set": "E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even}",
        "block": "%dx%dx%d fine lattice, base points p in {0,...,%d}^3, all 3 orientations" % (n, n, n, n - 1),
        "total_plaquettes_checked": total,
        "even_intersection_count": even_hits,
        "odd_intersection_count": odd_hits,
        "count_split": {"links_in_E_1": count_1, "links_in_E_3": count_3},
        "histogram": {str(k): v for k, v in sorted(hist.items())},
        "translation_covariance": {
            "pass": consistent,
            "num_orientation_parity_classes_found": n_classes,
            "expected_classes": 24,
            "all_classes_odd": classes_all_odd,
        },
        "damaging_mutation_control": {
            "name": "E_minus_one_link (drop (0,0,0,x) from E)",
            "target_face": "W itself: p=(0,0,0), orientation xz",
            "count_before": mutation_count_before,
            "count_after": mutation_count_after,
            "rejected": mutation_rejected,
            "reason": "removing one link from E must turn some odd intersection even; a flip set that survives this mutation unmodified would be a bug",
        },
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
