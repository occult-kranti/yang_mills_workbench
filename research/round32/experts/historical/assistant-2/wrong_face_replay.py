#!/usr/bin/env python3
"""
T5 -- wrong_face_replay.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 2.

Zero research loops: test/planning script, not a producer, skeptic or
advisor artifact. This does not read or import research/round32/forward/
aw1/check.py or research/round32/reverse/aw1/check.py; the geometry
below is a fresh re-implementation of the I1.4 face-link rule and the
21-omitted-class enumeration, the same convention independently used
(and disclosed) by research/round32/experts/historical/assistant-1's
S1 (haar_parity_exact.py) and S2 (am2_tiers_exact.py); reused here per
the task's instruction to reuse assistant-1 by import/copy rather than
read a producer's check.py.

Task (update-1.md section 5, test 5): an exact Haar computation showing
that every omitted face other than W gives zero first-order contribution
to omega(W), and that the W face itself gives +tau/144, under I1.5:

    phi_b = -(tau/3) sum_{f in O_b} W_f          (whole-star interaction)
    V_b   = phi_b / 8                             (alpha units)
    each W_f Omega_0 has H_0-energy 3 (alpha units)
    E[W^2] = 1/4                                  (Haar moment, Part A)

Derivation (AW1 report.md section 4.1/HNM-AW1-F12, re-derived here from
scratch): per omitted face f, the interaction contributes to the ground
vector's first-order correction

    c^(1)_f = H_0^{-1} V_f Omega_0 = (1/3) * (-tau/24) * W_f Omega_0
            = -(tau/72) W_f Omega_0                (energy-3 eigenvalue -> H_0^{-1} factor 1/3;
                                                      V_f coefficient = phi_b-coefficient/8 = -(tau/3)/8 = -tau/24)

and the first-order shift of omega(W) from face f alone is

    contribution_f = -2 * <W Omega_0, c^(1)_f> = (tau/36) * E[W * W_f].

E[W*W_f] is computed EXACTLY via the odd-link-multiplicity vanishing
argument (fractions.Fraction Haar moments, no floats): two distinct
plaquettes share at most one fine link (checked exhaustively below), so
for f != W at least one of W's or f's exclusive links occurs an ODD
number of times in the product W*W_f, forcing E[W*W_f]=0 by SU(2)
Peter-Weyl/Haar orthogonality (a link's Haar integral of an odd tensor
power of the fundamental representation is zero). For f=W the product is
W^2, whose exact Haar moment is 1/4 (independently re-derived by two
routes, Clebsch-Gordan/Catalan counting and the Weyl/Wallis integral).

The faces checked are the 10 omitted classes anchored at factor 0 whose
owner set is exactly R={0,e_z} (research/round32/forward/aw1/output/
results.json's face_enumeration_derived.faces_inside_R=10): the 6 xz
classes (r=0,1,2; s=0,1) and the 4 yz classes (r=0,1,2,3; s=0); W itself
is the xz, r=0, s=0 class.

Pass iff the only nonzero contribution among these 10 is f=W, with
value exactly tau/144 (equivalently coefficient (tau/36)*(1/4)=tau/144),
and every other face gives exactly 0.

Arithmetic: fractions.Fraction only; no floats in any comparison.
Run with: python3 -B wrong_face_replay.py
"""
import json
import sys
from collections import Counter
from math import comb
from fractions import Fraction as F

DIRS = ("x", "y", "z")


def unit(d):
    v = [0, 0, 0]
    v[DIRS.index(d)] = 1
    return tuple(v)


def padd(p, v):
    return (p[0] + v[0], p[1] + v[1], p[2] + v[2])


def face_links(p, a, c):
    assert DIRS.index(a) < DIRS.index(c)
    ea, ec = unit(a), unit(c)
    return frozenset([(p, a), (padd(p, ea), c), (padd(p, ec), a), (p, c)])


def owner_factor(tail):
    """Coarse factor owning a fine link with the given tail (I1 section 2:
    the coarse factor spans 4 fine x-sites, 2 fine y-sites, 1 fine z-site)."""
    x, y, z = tail
    return (x // 4, y // 2, z)


# --- Part A: single-link Haar moments, two independent exact routes ---

def catalan(k):
    if k < 0:
        return 0
    num = comb(2 * k, k)
    assert num % (k + 1) == 0
    return num // (k + 1)


def moment_clebsch_gordan(n):
    if n % 2 == 1:
        return F(0)
    m = n // 2
    return F(catalan(m), 2 ** n)


def moment_wallis_beta(n):
    if n % 2 == 1:
        return F(0)
    m = n // 2
    term1 = F(comb(2 * m, m), 4 ** m)
    term2 = F(comb(2 * m + 2, m + 1), 4 ** (m + 1))
    return 2 * (term1 - term2)


def haar_moment(n):
    a, b = moment_clebsch_gordan(n), moment_wallis_beta(n)
    assert a == b
    return a


# The original xz Wilson loop, AT4-F04 / AW1 model:
#   W = (1/2) Tr[U_{0,x} U_{e_x,z} U_{e_z,x}^{-1} U_{0,z}^{-1}]
W_LINKS = face_links((0, 0, 0), "x", "z")
assert owner_factor((0, 0, 0)) == (0, 0, 0)
W_OWNER_SET = frozenset(owner_factor(t) for (t, d) in W_LINKS)
R = frozenset({(0, 0, 0), (0, 0, 1)})
assert W_OWNER_SET == R, "W's owner set must be R={0,e_z}"


def build_faces_with_owner_set_R():
    """
    The 21 omitted I1 classes anchored at factor 0 (research/round21/
    forward/i1/report.md section 3), built directly at their fine
    coordinates (same convention as assistant-1's S1
    build_omitted_classes()); filtered here to the 10 whose owner set is
    exactly R = {0,e_z} (6 xz + 4 yz classes).
    """
    faces = []
    # xz: r=0,1,2; s=0,1 -> owner set {0,e_z} (6 classes; r=0,s=0 is W itself)
    for r in range(3):
        for s in range(2):
            name = "xz_r%d_s%d" % (r, s)
            links = face_links((r, s, 0), "x", "z")
            faces.append((name, links))
    # yz: r=0,1,2,3; s=0 -> owner set {0,e_z} (4 classes)
    for r in range(4):
        name = "yz_r%d_s0" % r
        links = face_links((r, 0, 0), "y", "z")
        faces.append((name, links))
    # sanity: every one of these really has owner set R
    for name, links in faces:
        owners = frozenset(owner_factor(t) for (t, d) in links)
        assert owners == R, (name, sorted(owners))
    return faces


def haar_product_moment(face_list):
    """
    Exact Haar expectation of a product of Wilson-face variables, using
    ONLY the odd-link-multiplicity vanishing argument plus haar_moment()
    for the fully-coincident case: if every link in the multiset union
    occurs the SAME number of times as in a single repeated face (i.e.
    all face_list entries are literally the same face f, repeated k
    times), the product collapses to W_f^k and its moment is haar_moment(k).
    Otherwise, if any link occurs an ODD number of times across the
    whole product, Haar orthogonality on that single link forces the
    expectation to 0 (each link is an independent Haar variable, and the
    Haar integral of an odd tensor power of the SU(2) fundamental
    representation contains no invariant, by Part A above).
    """
    if len(set(face_list)) == 1:
        return haar_moment(len(face_list))
    mult = Counter()
    for links in face_list:
        for l in links:
            mult[l] += 1
    if any(c % 2 == 1 for c in mult.values()):
        return F(0)
    # No odd link anywhere but the faces are not all identical: this
    # combination does not occur among the pairs checked below (distinct
    # plaquettes share at most one link), so we do not need a further
    # route here; flag it rather than silently return a wrong value.
    raise AssertionError("even-everywhere product of distinct faces: needs a separate route (not encountered here)")


def main():
    E_W = haar_moment(1)
    E_W2 = haar_moment(2)
    E_W3 = haar_moment(3)
    moments_ok = (E_W == 0 and E_W2 == F(1, 4) and E_W3 == 0)

    faces = build_faces_with_owner_set_R()
    assert len(faces) == 10

    # Independently confirm: two DISTINCT faces among these 10 (and W
    # itself vs. each of the other 9) share at most one link.
    max_shared = 0
    for i in range(len(faces)):
        for j in range(len(faces)):
            if i == j:
                continue
            shared = len(faces[i][1] & faces[j][1])
            max_shared = max(max_shared, shared)
    distinctness_ok = (max_shared <= 1)

    # Per-face first-order contribution to omega(W):
    #   c^(1)_f = -(tau/72) W_f Omega_0   (H_0^{-1}=1/3 on energy-3 eigenstate,
    #                                       V_f coefficient = -(tau/3)/8 = -tau/24)
    #   contribution_f(tau) = -2<W Omega_0, c^(1)_f> = (tau/36) * E[W W_f]
    # computed here with tau symbolic via a unit Fraction coefficient
    # (tau factored out; every entry below is contribution_f / tau).
    energy = F(3)                       # H_0 eigenvalue of W_f Omega_0, alpha units
    H0_inv = 1 / energy                 # = 1/3
    phi_b_coeff_per_face = F(-1, 3)     # phi_b = -(tau/3) sum_f W_f -> coefficient -1/3 per face (tau factored out)
    V_coeff_per_face = phi_b_coeff_per_face / 8   # V_b = phi_b/8 -> -1/24
    c1_coeff_per_face = H0_inv * V_coeff_per_face  # = -1/72
    assert c1_coeff_per_face == F(-1, 72)

    rows = []
    nonzero_faces = []
    for name, links in faces:
        is_W = (links == W_LINKS)
        e_w_wf = haar_product_moment([W_LINKS, links])
        contribution_over_tau = -2 * c1_coeff_per_face * e_w_wf  # = (1/36)*E[W W_f]
        nonzero = (contribution_over_tau != 0)
        if nonzero:
            nonzero_faces.append(name)
        rows.append({
            "face": name,
            "is_W_itself": is_W,
            "E_W_Wf": str(e_w_wf),
            "contribution_over_tau": str(contribution_over_tau),
            "nonzero": nonzero,
        })

    w_row = next(r for r in rows if r["is_W_itself"])
    w_value_correct = (w_row["contribution_over_tau"] == str(F(1, 144)))
    only_W_nonzero = (nonzero_faces == [w_row["face"]])

    # Damaging-mutation control: claiming a DIFFERENT face (say the first
    # non-W face) as the sole contributor must be rejected.
    wrong_claim_face = next(r for r in rows if not r["is_W_itself"])
    wrong_claim_rejected = (wrong_claim_face["contribution_over_tau"] == "0")

    # Damaging-mutation control: summing ALL 10 contributions (as if
    # every inside-R face contributed) must NOT reproduce tau/144 unless
    # only W is nonzero -- confirm the naive "count all 10" sum equals
    # tau/144 only because 9 of them are exactly zero, not by coincidence.
    total_over_tau = sum(F(r["contribution_over_tau"]) for r in rows)
    sum_equals_single_W_contribution = (total_over_tau == F(1, 144))

    overall_pass = bool(
        moments_ok
        and distinctness_ok
        and w_value_correct
        and only_W_nonzero
        and wrong_claim_rejected
        and sum_equals_single_W_contribution
    )

    result = {
        "script": "wrong_face_replay.py",
        "zero_research_loops": True,
        "arithmetic": "fractions.Fraction only; no floats in any comparison",
        "model": "I1.5: phi_b=-(tau/3) sum W_f, V_b=phi_b/8, energy(W_f Omega_0)=3 (alpha units)",
        "haar_moments": {"E_W": str(E_W), "E_W2": str(E_W2), "E_W3": str(E_W3), "moments_ok": moments_ok},
        "per_face_coefficient_c1_over_tau": str(c1_coeff_per_face),
        "faces_checked": len(faces),
        "faces_owner_set": "R={0,e_z} (6 xz classes r=0,1,2 s=0,1 + 4 yz classes r=0,1,2,3 s=0)",
        "max_links_shared_by_two_distinct_faces": max_shared,
        "distinctness_ok": distinctness_ok,
        "per_face_rows": rows,
        "nonzero_faces": nonzero_faces,
        "only_W_nonzero": only_W_nonzero,
        "W_first_order_contribution_over_tau": w_row["contribution_over_tau"],
        "W_value_is_1_over_144": w_value_correct,
        "sum_of_all_10_over_tau": str(total_over_tau),
        "sum_equals_1_over_144": sum_equals_single_W_contribution,
        "damaging_mutation_wrong_face_claim_rejected": wrong_claim_rejected,
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
