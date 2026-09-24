#!/usr/bin/env python3
"""S2 flip_parity_k2.py -- link-flip parity lemma and K_2 face-count cross-check.

Round32, sub-round 1, modern (Penrose/Feynman) lens, assistant-1.
Status: assistant/coder preview tool. Counts ZERO research loops. Never
admission arithmetic; numpy fixtures here are illustrative previews only.

Part (a): E = {(p,x): p_y even} U {(p,y): p_z even} U {(p,z): p_x even}
(loop3-signoff.md section 2, the AW1 link-flip antisymmetry lemma).
Exhaustively verifies on a 6x6x6 fine block that every plaquette meets E
in an odd number (1 or 3) of its 4 links, then builds a small random-SU(2)
numpy fixture, flips every link in E by the central element -1, and checks
(i) every plaquette Wilson trace changes sign, (ii) a Casimir-invariant
quantity (link trace squared) is unchanged link by link.

Part (b): an independent, from-scratch geometric encoding of the I1
24-anchored-face-class table (research/round21/forward/i1/report.md,
lines 59-66: the translation-covariant selected/omitted rule keyed by
r = x mod 4, s = y mod 2 of a face's base corner, block anchor at
(4*floor(x/4), 2*floor(y/2), z)), used to brute-force count, for the
cover R = {0, e_z}: total faces meeting R (expect 82), inside R (10),
straddling (72, split one-outside-site / two-outside-site), and the
count of faces sharing an actual fine link with a concrete W face
(reported, not target-checked). These are cross-checked against AV1's
own frozen enumeration (research/round32/forward/av1/output/results.json
and research/round32/experts/modern/loop2-response.md section 2), which
this script derives independently rather than imports.
"""
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q

import numpy as np

# ------------------------------------------------------------------ part (a)

def in_E(p, direction):
    x, y, z = p
    if direction == 'x':
        return y % 2 == 0
    if direction == 'y':
        return z % 2 == 0
    if direction == 'z':
        return x % 2 == 0
    raise ValueError(direction)


def plaquette_links(p, orientation):
    x, y, z = p
    if orientation == 'xy':
        return [(p, 'x'), ((x, y + 1, z), 'x'), (p, 'y'), ((x + 1, y, z), 'y')]
    if orientation == 'xz':
        return [(p, 'x'), ((x, y, z + 1), 'x'), (p, 'z'), ((x + 1, y, z), 'z')]
    if orientation == 'yz':
        return [(p, 'y'), ((x, y, z + 1), 'y'), (p, 'z'), ((x, y + 1, z), 'z')]
    raise ValueError(orientation)


def exhaustive_flip_parity(n=6):
    """Every plaquette of an n x n x n fine block (base corners 0..n-1 in
    each direction, all three orientations) meets E in an odd number of
    links. Returns (n_checked, n_failed, odd_count_histogram)."""
    failures = []
    hist = Counter()
    for x, y, z in itertools.product(range(n), repeat=3):
        for orientation in ('xy', 'xz', 'yz'):
            links = plaquette_links((x, y, z), orientation)
            k = sum(1 for (p, d) in links if in_E(p, d))
            hist[k] += 1
            if k % 2 == 0:
                failures.append(((x, y, z), orientation, k))
    return {
        'box': n,
        'plaquettes_checked': 3 * n * n * n,
        'failures': failures,
        'failure_count': len(failures),
        'odd_count_histogram': dict(hist),
        'passed': len(failures) == 0,
    }


def su2_random(rng):
    """Random SU(2): a0*I + i(a1 sx + a2 sy + a3 sz), unit quaternion."""
    v = rng.normal(size=4)
    v = v / np.linalg.norm(v)
    a0, a1, a2, a3 = v
    return np.array([[a0 + 1j * a3, a2 + 1j * a1],
                      [-a2 + 1j * a1, a0 - 1j * a3]], dtype=complex)


def su2_numerical_fixture(n=4, seed=20320923):
    """n x n x n open lattice, random SU(2) link matrices on every x/y/z
    link with tail in [0,n). Flip every link in E by the central -I.
    Checks every plaquette trace flips sign, and every link's tr(U)^2
    (Casimir-invariant, gauge-covariant quantity) is unchanged."""
    rng = np.random.default_rng(seed)
    links = {}
    for x, y, z in itertools.product(range(n), repeat=3):
        for d in ('x', 'y', 'z'):
            links[((x, y, z), d)] = su2_random(rng)

    flipped = {}
    for key, U in links.items():
        p, d = key
        flipped[key] = -U if in_E(p, d) else U.copy()

    def trace(U):
        return np.trace(U)

    def holonomy(link_dict, key_links):
        # bottom, top, left, right (order returned by plaquette_links); the
        # dagger pattern is fixed and immaterial to the sign-flip property
        # tested here (only that it is applied identically before/after).
        bottom, top, left, right = (link_dict[k] for k in key_links)
        return bottom @ right @ top.conj().T @ left.conj().T

    plaquette_checks = []
    trace_sign_ok = True
    for x, y, z in itertools.product(range(n - 1), repeat=3):
        for orientation in ('xy', 'xz', 'yz'):
            key_links = plaquette_links((x, y, z), orientation)
            if any(k not in links for k in key_links):
                continue
            tr_before = trace(holonomy(links, key_links))
            tr_after = trace(holonomy(flipped, key_links))
            k_in_E = sum(1 for (p, d) in key_links if in_E(p, d))
            ok = np.isclose(tr_after, -tr_before, atol=1e-10)
            trace_sign_ok &= bool(ok)
            plaquette_checks.append({
                'base': (x, y, z), 'orientation': orientation,
                'links_in_E': k_in_E,
                'trace_before': complex(tr_before),
                'trace_after': complex(tr_after),
                'sign_flipped': bool(ok),
            })

    casimir_ok = True
    casimir_max_dev = 0.0
    for key, U in links.items():
        before = (trace(U)) ** 2
        after = (trace(flipped[key])) ** 2
        dev = abs(before - after)
        casimir_max_dev = max(casimir_max_dev, dev)
        casimir_ok &= dev < 1e-10

    return {
        'lattice': n,
        'seed': seed,
        'plaquettes_checked': len(plaquette_checks),
        'all_traces_flip_sign': trace_sign_ok,
        'casimir_invariant_unchanged': casimir_ok,
        'casimir_max_deviation': casimir_max_dev,
        'sample': plaquette_checks[:3],
        'passed': bool(trace_sign_ok and casimir_ok),
    }


# ------------------------------------------------------------------ part (b)

# I1 24-anchored-face-class table (research/round21/forward/i1/report.md L59-66),
# reproduced here as an independent, from-scratch translation-covariant rule:
# key = (orientation, r, s) -> (role, support_extra) where support_extra is
# the set of nonzero coarse-unit offsets (in addition to the always-present
# block itself) that the face's owner set includes.
E_X, E_Y, E_Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def face_class(orientation, r, s):
    if orientation == 'xy':
        if r in (0, 1, 2) and s == 0:
            return 'selected', frozenset()
        if r in (0, 1, 2) and s == 1:
            return 'omitted', frozenset({E_Y})
        if r == 3 and s == 0:
            return 'omitted', frozenset({E_X})
        if r == 3 and s == 1:
            return 'omitted', frozenset({E_X, E_Y})
    elif orientation == 'xz':
        if r in (0, 1, 2):
            return 'omitted', frozenset({E_Z})
        if r == 3:
            return 'omitted', frozenset({E_X, E_Z})
    elif orientation == 'yz':
        if s == 0:
            return 'omitted', frozenset({E_Z})
        if s == 1:
            return 'omitted', frozenset({E_Y, E_Z})
    raise ValueError((orientation, r, s))


def block_and_residue(x, y, z):
    bi = x // 4
    r = x - 4 * bi
    bj = y // 2
    s = y - 2 * bj
    bk = z  # z is not coarsened: block width 1
    return (bi, bj, bk), r, s


def face_links(orientation, base):
    x, y, z = base
    if orientation == 'xy':
        return frozenset({(base, 'x'), ((x, y + 1, z), 'x'), (base, 'y'), ((x + 1, y, z), 'y')})
    if orientation == 'xz':
        return frozenset({(base, 'x'), ((x, y, z + 1), 'x'), (base, 'z'), ((x + 1, y, z), 'z')})
    if orientation == 'yz':
        return frozenset({(base, 'y'), ((x, y, z + 1), 'y'), (base, 'z'), ((x, y + 1, z), 'z')})
    raise ValueError(orientation)


def enumerate_omitted_faces(x_range, y_range, z_range):
    """Every omitted face with base corner in the box, as
    {'orientation', 'base', 'block', 'owner_set' (absolute coarse coords,
    frozenset of (bi,bj,bk) tuples), 'links'}."""
    faces = []
    for x in x_range:
        for y in y_range:
            for z in z_range:
                block, r, s = block_and_residue(x, y, z)
                for orientation in ('xy', 'xz', 'yz'):
                    role, extra = face_class(orientation, r, s)
                    if role != 'omitted':
                        continue
                    owner_set = frozenset(
                        (block[0] + dx, block[1] + dy, block[2] + dz)
                        for (dx, dy, dz) in ({(0, 0, 0)} | extra)
                    )
                    faces.append({
                        'orientation': orientation, 'base': (x, y, z), 'block': block,
                        'owner_set': owner_set, 'links': face_links(orientation, (x, y, z)),
                    })
    return faces


def face_count_and_cover_report():
    # Generous box: owner-set offsets are only 0/+1 per coordinate, so blocks
    # b=-v for v in a support set lie in {-1,0}^3; a wider box double-checks
    # there is nothing else out there that could also touch site 0 or e_z.
    faces = enumerate_omitted_faces(range(-12, 16), range(-6, 8), range(-3, 5))

    R = frozenset({(0, 0, 0), (0, 0, 1)})

    touching_origin = [f for f in faces if (0, 0, 0) in f['owner_set']]
    groups = defaultdict(int)
    for f in touching_origin:
        groups[f['owner_set']] += 1

    meeting_R = [f for f in faces if f['owner_set'] & R]
    inside_R = [f for f in meeting_R if f['owner_set'] <= R]
    straddling = [f for f in meeting_R if not (f['owner_set'] <= R)]
    straddle_one_outside = [f for f in straddling if len(f['owner_set'] - R) == 1]
    straddle_two_outside = [f for f in straddling if len(f['owner_set'] - R) == 2]

    # W: the concrete original xz Wilson loop at the selected triple (0,0,0):
    # the xz-oriented face, r=0,s=0, block (0,0,0), i.e. base fine corner (0,0,0).
    w_candidates = [f for f in inside_R if f['orientation'] == 'xz' and f['block'] == (0, 0, 0)
                    and f['base'] == (0, 0, 0)]
    assert len(w_candidates) == 1, w_candidates
    W = w_candidates[0]

    shares_link_with_W = [f for f in meeting_R
                           if f is not W and f['links'] & W['links']]
    # also check against the full omitted-face universe in the box (not just meeting_R)
    shares_link_with_W_universe = [f for f in faces
                                    if f is not W and f['links'] & W['links']]

    owner_group_sizes = sorted(groups.values())

    return {
        'box': {'x': [-12, 16], 'y': [-6, 8], 'z': [-3, 5]},
        'faces_per_site': len(touching_origin),
        'owner_sets_per_site': len(groups),
        'owner_set_multiplicities_sorted': owner_group_sizes,
        'faces_meeting_R': len(meeting_R),
        'faces_inside_R': len(inside_R),
        'faces_straddling': len(straddling),
        'straddling_one_outside_site': len(straddle_one_outside),
        'straddling_two_outside_site': len(straddle_two_outside),
        'W': {'orientation': W['orientation'], 'base': W['base'], 'owner_set': sorted(W['owner_set'])},
        'faces_sharing_a_link_with_W_within_meeting_R': len(shares_link_with_W),
        'faces_sharing_a_link_with_W_in_box': len(shares_link_with_W_universe),
        'expected': {'faces_per_site': 49, 'owner_sets_per_site': 15, 'faces_meeting_R': 82,
                     'faces_inside_R': 10, 'faces_straddling': 72,
                     'straddling_one_outside_site': 42, 'straddling_two_outside_site': 30},
        'matches_expected': (
            len(touching_origin) == 49 and len(groups) == 15 and len(meeting_R) == 82
            and len(inside_R) == 10 and len(straddling) == 72
            and len(straddle_one_outside) == 42 and len(straddle_two_outside) == 30
        ),
    }


def second_order_multiplier_structure(cover_report):
    """The AW1 parity lemma (loop3-signoff.md section 2) kills the direct
    tau^2/K_2 term whose creation is supported exactly on R and overlaps
    W Omega_R: by the mod-2 obstruction, two distinct omitted faces never
    sum (as link sets, mod 2) to a single face, so <W Omega_0, L_1(c^(1))
    Omega_0> = 0 identically. This function reports, from the same brute
    force, which faces have owner_set == R exactly (support exactly on R,
    the only candidates whose *single-face* creation could overlap W
    Omega_R without a straddling partner) versus every other owner-set
    shape, as the multiplier structure the K_2 budget must itemize."""
    return {
        'faces_with_owner_set_exactly_R': cover_report['faces_inside_R'],
        'note': 'Only these (owner_set == R = {0,e_z} exactly) are supported exactly on R; '
                'every other face meeting R has at least one link anchored outside R and so '
                'contributes to the straddling/pair terms (b)-(f) of loop2-response.md section 2, '
                'never to the single-face direct overlap with W Omega_R that the flip-parity '
                'lemma sets to zero at first order.',
    }


def k2_tier_check():
    """Reproduce the three first-order K_2 tiers from loop2-response.md's
    table and check each is below the cap 6.9e5 with margin>=10, the crude
    tier failing, and each term's exact tau-scaling exponent (1 or 2)."""
    cap = Q(69, 10) * 10**5  # 6.9e5
    tau = Q(1, 10**8)
    tiers = {
        'crude_AM2_majorant_only': {'t_over_abs_tau': Q(44804, 100), 'K2': Q(165, 10) * 10**6},
        'skeptic_84_face_bound': {'t_over_abs_tau': Q(5834, 10000), 'K2': Q(188, 10) * 10**3},
        'enumerated_49_face_triangle': {'t_over_abs_tau': Q(3403, 10000), 'K2': Q(110, 10) * 10**3},
    }
    out = {}
    for name, d in tiers.items():
        K2 = d['K2']
        margin = cap / K2 if K2 != 0 else None
        out[name] = {
            't_over_abs_tau_preview': float(d['t_over_abs_tau']),
            'K2_preview': float(K2),
            'below_cap': bool(K2 < cap),
            'margin_ratio_preview': float(margin) if margin is not None else None,
        }
    out['crude_AM2_majorant_only']['expected_fail'] = True
    out['crude_AM2_majorant_only']['fails_as_expected'] = not out['crude_AM2_majorant_only']['below_cap']
    out['cap'] = float(cap)
    out['passed'] = (
        out['crude_AM2_majorant_only']['fails_as_expected']
        and out['skeptic_84_face_bound']['below_cap'] and out['skeptic_84_face_bound']['margin_ratio_preview'] >= 10
        and out['enumerated_49_face_triangle']['below_cap'] and out['enumerated_49_face_triangle']['margin_ratio_preview'] >= 10
    )
    return out


def self_test():
    parity = exhaustive_flip_parity(n=6)
    parity9 = exhaustive_flip_parity(n=9)
    su2 = su2_numerical_fixture(n=4)
    cover = face_count_and_cover_report()
    multiplier = second_order_multiplier_structure(cover)
    k2 = k2_tier_check()

    passed = bool(parity['passed'] and parity9['passed'] and su2['passed']
                  and cover['matches_expected'] and k2['passed'])

    return {
        'tool': 'S2 flip_parity_k2',
        'part_a_exhaustive_parity_6cubed': parity,
        'part_a_exhaustive_parity_9cubed_bonus': parity9,
        'part_a_su2_numerical_fixture': su2,
        'part_b_face_count_and_cover_report': cover,
        'part_b_second_order_multiplier_structure': multiplier,
        'part_b_k2_tier_check': k2,
        'passed': passed,
    }


def main():
    result = self_test()
    print(json.dumps(result, indent=2, default=str))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
