#!/usr/bin/env python3
"""uniform_counts_from_scratch.py -- an independent (of the AV1/AX1
producers AND of the sub-round 1/2 "historical assistant"'s own
`flip_parity_k2.py`) re-derivation of the route-B uniform-model face
counts the AX1 gate admits:

    52 faces per factor (49 omitted + 3 selected)
    88 faces meeting R={0,e_z} (82 omitted + 6 selected)
    16 faces inside R (10 omitted + 6 selected)
     6 selected faces meeting/inside R (two single-factor groups' worth)

Round32, sub-round 3, modern (Penrose/Feynman) lens, assistant-3.
Status: assistant/coder preview/cross-check tool. Counts ZERO research
loops; nothing here is imported by any `check.py` and nothing here
changes a verdict -- it is an independent arithmetic check offered
alongside the admitted AX1 numbers.

Independence: this file encodes the I1 24-anchored-face-class table
(`research/round21/forward/i1/report.md` lines 59-66, a frozen shared
premise every AW1/AV1/AX1 producer and assistant-1's `flip_parity_k2.py`
also read) with its OWN structure and its OWN two methods, neither of
which is `flip_parity_k2.py`'s fine-lattice (x,y,z,orientation) box scan
with `block_and_residue`/`face_class`:

  Method 1 (closed-form inclusion-exclusion): works directly with the 24
  classes' (role, extra-offset-set) data, at the level of COARSE block
  coordinates only -- no fine (x,y,z) coordinates, no residues, ever
  appear. Touching-one-site and touching-both-R-sites counts are derived
  by set arithmetic on the offsets alone.

  Method 2 (independent brute force): iterates directly over (owner
  block, one of the 24 class rows) pairs in a finite coarse box -- again
  no fine coordinates or residues -- and counts membership by explicit
  set intersection, as a genuine second, structurally different
  computation of the same numbers (a cross-check of Method 1, not a
  restatement of `flip_parity_k2.py`'s own brute force, which instead
  scans fine (x,y,z) tuples through `block_and_residue`).

Route B (AX1, sub-round 3) is the only NEW ingredient over the earlier
(AW1/AV1) omitted-only counts: it puts the 3 "selected" xy classes on
equal footing with the 21 "omitted" classes (every one of the 24 classes
is charged once, per face, per block), which is why the per-factor count
rises from 49 to 52 and the R-cover count from 82 to 88 (of which 6 are
newly-counted selected faces, and 16=10+6 inside R). This file re-derives
the pre-existing 49/82/10 (omitted only) totals FROM SCRATCH as well
(not merely cited), because route B's arithmetic is only correct if
those inherited numbers are still right.
"""
import json
from itertools import product

# --- The I1 24-anchored-face-class table, encoded directly from
# research/round21/forward/i1/report.md lines 59-66. `extra` is the set of
# ADDITIONAL coarse-unit-vector offsets (beyond the class's own owner
# block, always included) that the class's support reaches. Each row here
# is ONE class (not consolidated by the report's "Count" column), so the
# list literally has 24 entries, matching "the 24 anchored face classes".
EX, EY, EZ = (1, 0, 0), (0, 1, 0), (0, 0, 1)

CLASSES = []
# xy, r=0,1,2, s=0: selected, support {0}
for r in (0, 1, 2):
    CLASSES.append({'orientation': 'xy', 'r': r, 's': 0, 'role': 'selected', 'extra': frozenset()})
# xy, r=0,1,2, s=1: omitted, support {0,e_y}
for r in (0, 1, 2):
    CLASSES.append({'orientation': 'xy', 'r': r, 's': 1, 'role': 'omitted', 'extra': frozenset({EY})})
# xy, r=3, s=0: omitted, support {0,e_x}
CLASSES.append({'orientation': 'xy', 'r': 3, 's': 0, 'role': 'omitted', 'extra': frozenset({EX})})
# xy, r=3, s=1: omitted, support {0,e_x,e_y}
CLASSES.append({'orientation': 'xy', 'r': 3, 's': 1, 'role': 'omitted', 'extra': frozenset({EX, EY})})
# xz, r=0,1,2, s=0,1: omitted, support {0,e_z} (6 classes)
for r in (0, 1, 2):
    for s in (0, 1):
        CLASSES.append({'orientation': 'xz', 'r': r, 's': s, 'role': 'omitted', 'extra': frozenset({EZ})})
# xz, r=3, s=0,1: omitted, support {0,e_x,e_z} (2 classes)
for s in (0, 1):
    CLASSES.append({'orientation': 'xz', 'r': 3, 's': s, 'role': 'omitted', 'extra': frozenset({EX, EZ})})
# yz, r=0,1,2,3, s=0: omitted, support {0,e_z} (4 classes)
for r in (0, 1, 2, 3):
    CLASSES.append({'orientation': 'yz', 'r': r, 's': 0, 'role': 'omitted', 'extra': frozenset({EZ})})
# yz, r=0,1,2,3, s=1: omitted, support {0,e_y,e_z} (4 classes)
for r in (0, 1, 2, 3):
    CLASSES.append({'orientation': 'yz', 'r': r, 's': 1, 'role': 'omitted', 'extra': frozenset({EY, EZ})})

assert len(CLASSES) == 24, len(CLASSES)
N_SELECTED = sum(1 for c in CLASSES if c['role'] == 'selected')
N_OMITTED = sum(1 for c in CLASSES if c['role'] == 'omitted')
assert (N_SELECTED, N_OMITTED) == (3, 21), (N_SELECTED, N_OMITTED)


def add3(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub3(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def support_of(owner, cls):
    """Every block this class's face touches when owned at `owner`."""
    return frozenset({owner}) | frozenset(add3(owner, v) for v in cls['extra'])


# --------------------------------------------------------- Method 1: I-E
def method1_touching_single_site():
    """Faces (of a given role) touching ONE fixed site s0=(0,0,0):
    owned-at-s0 (always touches, extra offset 0 always present) PLUS, for
    each nonzero offset v in {e_x,e_y,e_z}, classes with v in their
    `extra` set, owned at s0-v (so owner+v=s0)."""
    s0 = (0, 0, 0)
    owned_selected = sum(1 for c in CLASSES if c['role'] == 'selected')
    owned_omitted = sum(1 for c in CLASSES if c['role'] == 'omitted')
    neighbor = {'omitted': 0, 'selected': 0}
    per_direction = {}
    for v in (EX, EY, EZ):
        cnt = {'omitted': 0, 'selected': 0}
        for c in CLASSES:
            if v in c['extra']:
                cnt[c['role']] += 1
        per_direction[v] = cnt
        neighbor['omitted'] += cnt['omitted']
        neighbor['selected'] += cnt['selected']
    total_omitted = owned_omitted + neighbor['omitted']
    total_selected = owned_selected + neighbor['selected']
    return {
        'owned_at_site_selected': owned_selected, 'owned_at_site_omitted': owned_omitted,
        'neighbor_contribution_by_direction': {str(k): v for k, v in per_direction.items()},
        'neighbor_total_omitted': neighbor['omitted'], 'neighbor_total_selected': neighbor['selected'],
        'faces_per_site_omitted': total_omitted, 'faces_per_site_selected': total_selected,
        'faces_per_site_total': total_omitted + total_selected,
    }


def method1_R_cover():
    """R = {s_A=(0,0,0), s_B=(0,0,1)}. |touch(s_A) union touch(s_B)| via
    inclusion-exclusion; "inside R" via exhaustive case analysis on the
    (small, fixed) support shapes; selected faces (singleton support) are
    trivial special cases of the same reasoning."""
    s_A, s_B = (0, 0, 0), (0, 0, 1)

    def touches(support, site):
        return site in support

    # touch(s_A), touch(s_B) totals per role, by the single-site method.
    single = method1_touching_single_site()  # symmetric under z-translation
    touch_sA = {'omitted': single['faces_per_site_omitted'], 'selected': single['faces_per_site_selected']}
    touch_sB = dict(touch_sA)  # translation invariance in z (classes don't depend on z)

    # Faces whose support contains BOTH s_A and s_B: for omitted classes
    # this can only happen owned at s_A with e_z in `extra` (owned at s_B
    # would need a *negative* z offset to reach back to s_A, which never
    # occurs in the table); selected faces have singleton support and can
    # never contain two distinct sites.
    both_omitted = sum(1 for c in CLASSES if c['role'] == 'omitted' and EZ in c['extra'])
    both_selected = 0

    meeting_R_omitted = touch_sA['omitted'] + touch_sB['omitted'] - both_omitted
    meeting_R_selected = touch_sA['selected'] + touch_sB['selected'] - both_selected

    # Inside R: support subset of {s_A,s_B}. Selected: owner in {s_A,s_B}.
    inside_selected = sum(1 for owner in (s_A, s_B) for c in CLASSES if c['role'] == 'selected')
    # Omitted: owned at s_A or s_B with support (owner plus extras) a
    # subset of {s_A,s_B}; only a 2-element support {owner,owner+e_z} with
    # owner=s_A qualifies (owner=s_B+e_z leaves the box; any support
    # touching e_x or e_y leaves R immediately since R only varies in z).
    inside_omitted = 0
    for owner in (s_A, s_B):
        for c in CLASSES:
            if c['role'] != 'omitted':
                continue
            supp = support_of(owner, c)
            if supp <= {s_A, s_B}:
                inside_omitted += 1

    return {
        'touch_sA': touch_sA, 'touch_sB': touch_sB,
        'both_sA_and_sB_omitted': both_omitted, 'both_sA_and_sB_selected': both_selected,
        'meeting_R_omitted': meeting_R_omitted, 'meeting_R_selected': meeting_R_selected,
        'meeting_R_total': meeting_R_omitted + meeting_R_selected,
        'inside_R_omitted': inside_omitted, 'inside_R_selected': inside_selected,
        'inside_R_total': inside_omitted + inside_selected,
    }


# ------------------------------------------------- Method 2: brute force
def method2_brute_force(target_sites, box_radius=6):
    """Independent brute-force cross-check: enumerate every (owner block,
    class) pair with owner in a coarse box of the given radius, and count
    those whose support intersects / is contained in `target_sites`, by
    direct set operations -- no residue/fine-coordinate bookkeeping of any
    kind (contrast `flip_parity_k2.face_class`/`block_and_residue`, which
    works from fine (x,y,z) coordinates)."""
    target = frozenset(target_sites)
    rng = range(-box_radius, box_radius + 1)
    meeting = {'omitted': 0, 'selected': 0}
    inside = {'omitted': 0, 'selected': 0}
    for owner in product(rng, repeat=3):
        for c in CLASSES:
            supp = support_of(owner, c)
            if supp & target:
                meeting[c['role']] += 1
                if supp <= target:
                    inside[c['role']] += 1
    return {
        'box_radius': box_radius,
        'meeting_omitted': meeting['omitted'], 'meeting_selected': meeting['selected'],
        'meeting_total': meeting['omitted'] + meeting['selected'],
        'inside_omitted': inside['omitted'], 'inside_selected': inside['selected'],
        'inside_total': inside['omitted'] + inside['selected'],
    }


def method2_single_site(box_radius=6):
    return method2_brute_force({(0, 0, 0)}, box_radius=box_radius)


def method2_R(box_radius=6):
    return method2_brute_force({(0, 0, 0), (0, 0, 1)}, box_radius=box_radius)


EXPECTED = {
    'faces_per_site_omitted': 49, 'faces_per_site_selected': 3, 'faces_per_site_total': 52,
    'meeting_R_omitted': 82, 'meeting_R_selected': 6, 'meeting_R_total': 88,
    'inside_R_omitted': 10, 'inside_R_selected': 6, 'inside_R_total': 16,
}


def self_test():
    m1_site = method1_touching_single_site()
    m1_R = method1_R_cover()
    m2_site = method2_single_site(box_radius=6)
    m2_site_wide = method2_single_site(box_radius=9)  # a wider box: nothing further out matters
    m2_R = method2_R(box_radius=6)

    actual = {
        'faces_per_site_omitted': m1_site['faces_per_site_omitted'],
        'faces_per_site_selected': m1_site['faces_per_site_selected'],
        'faces_per_site_total': m1_site['faces_per_site_total'],
        'meeting_R_omitted': m1_R['meeting_R_omitted'],
        'meeting_R_selected': m1_R['meeting_R_selected'],
        'meeting_R_total': m1_R['meeting_R_total'],
        'inside_R_omitted': m1_R['inside_R_omitted'],
        'inside_R_selected': m1_R['inside_R_selected'],
        'inside_R_total': m1_R['inside_R_total'],
    }

    matches_expected = {k: (actual[k] == v) for k, v in EXPECTED.items()}
    method1_vs_method2_site = (
        m1_site['faces_per_site_omitted'] == m2_site['meeting_omitted']
        and m1_site['faces_per_site_selected'] == m2_site['meeting_selected']
        and m2_site['meeting_omitted'] == m2_site_wide['meeting_omitted']
        and m2_site['meeting_selected'] == m2_site_wide['meeting_selected']
    )
    method1_vs_method2_R = (
        m1_R['meeting_R_omitted'] == m2_R['meeting_omitted']
        and m1_R['meeting_R_selected'] == m2_R['meeting_selected']
        and m1_R['inside_R_omitted'] == m2_R['inside_omitted']
        and m1_R['inside_R_selected'] == m2_R['inside_selected']
    )

    passed = bool(all(matches_expected.values()) and method1_vs_method2_site and method1_vs_method2_R)

    return {
        'tool': 'A3-3 uniform_counts_from_scratch',
        'class_table_size': len(CLASSES),
        'class_table_role_split': {'selected': N_SELECTED, 'omitted': N_OMITTED},
        'method1_closed_form': {'single_site': m1_site, 'R_cover': m1_R},
        'method2_brute_force': {'single_site_r6': m2_site, 'single_site_r9_widened': m2_site_wide,
                                 'R_r6': m2_R},
        'actual': actual,
        'expected_from_ax1_gate': EXPECTED,
        'matches_expected': matches_expected,
        'method1_and_method2_agree_single_site': bool(method1_vs_method2_site),
        'method1_and_method2_agree_R': bool(method1_vs_method2_R),
        'widening_box_r6_to_r9_changes_nothing': bool(
            m2_site['meeting_omitted'] == m2_site_wide['meeting_omitted']
            and m2_site['meeting_selected'] == m2_site_wide['meeting_selected']),
        'passed': passed,
    }


def main():
    result = self_test()
    print(json.dumps(result, indent=2, default=str))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
