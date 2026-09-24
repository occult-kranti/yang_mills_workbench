#!/usr/bin/env python3
"""
S1 -- haar_parity_exact.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 1.

Scope (per loop3-signoff.md section 3, S1):
  Exact SU(2) character / Peter-Weyl computations with `fractions.Fraction`
  only. No floats, no sympy, no numerical integration of any kind.

Part A. Single-link Haar moments of w = (1/2) Tr(U), U in SU(2) Haar,
        computed two INDEPENDENT ways:
          (A1) Clebsch-Gordan / Peter-Weyl route: E[w^n] = 2^-n * (number
               of copies of the trivial representation in the n-fold
               tensor power of the j=1/2 representation). That count is
               the Catalan number C_{n/2} for even n and 0 for odd n
               (a spin chain of n spin-1/2's can be coupled to total spin
               zero only for even n, and the number of ways is the
               classical ballot / Dyck-path count).
          (A2) Beta-function / Wallis-integral route: w = cos(phi) with
               Haar density (2/pi) sin^2(phi) dphi on phi in [0,pi]
               (this is I1's own W = (1/2)Tr U convention, SU(2) Weyl
               integration formula). The moment integral reduces, via
               the classical Wallis formula for even powers of cosine,
               to a finite rational expression in which the factor of
               pi introduced by the Wallis integral is cancelled
               EXACTLY and symbolically by the 2/pi Weyl-measure
               prefactor -- no numerical value of pi ever appears.
        Both routes are required to agree exactly, and to reproduce the
        AV1 contract's reference_moments (omega_0(W)=0, omega_0(W^2)=1/4)
        and the stated omega_0(W^4)=1/8.

Part B. The four-link plaquette
          W = (1/2) Tr( U_{0,x} U_{e_x,z} U_{e_z,x}^{-1} U_{0,z}^{-1} )
        (AT4-F04 / AV1's "original xz Wilson loop", cover R={0,e_z}).
        Its four link factors are four DISTINCT, independent fine
        SU(2) links. Fixing any three of them, right/left multiplying
        the remaining Haar link by a fixed group element preserves Haar
        measure, so W's own distribution is exactly that of the single
        link variable w. Hence E[W^n] = E[w^n] for every n without any
        further computation: E[W]=0, E[W^2]=1/4.

Part C. Link-wise odd-multiplicity vanishing.
        For every other omitted face f of the SAME anchor star as W
        (the 21 classes of research/round21/forward/i1/report.md
        section 3, at anchor b=(0,0,0)), and also for f=W itself,
        E[W^2 * W_f] is shown to vanish by an EXACT, purely
        combinatorial argument that needs no character computation:
          - the fine links making up each face are reconstructed
            explicitly from the I1.4 tail rule (face at p, directions
            a<c has tails (p,a),(p+e_a,c),(p+e_c,a),(p,c));
          - links are independent Haar variables, so the Haar integral
            of a product of face-loop characters factors link by link;
          - the SU(2) fundamental representation is self-dual
            (pseudoreal via the epsilon tensor), so a link entering as
            U or as U^{-1} contributes an equivalent copy of the j=1/2
            representation to the per-link tensor power at that link;
          - by Part A's own odd-vanishing (Catalan(count)=0 for odd
            count), if ANY link appears an odd total number of times
            across the whole monomial W*W*W_f, the Haar integral over
            that single link already vanishes, forcing the entire
            expectation to vanish, regardless of every other link.
        Because two distinct omitted faces share at most one link
        (checked explicitly below, matching AV1 first_order_face_
        enumeration's "max_links_shared_by_distinct_faces: 1"), every
        f != W has at least three links used only by f, each occurring
        an odd number of times (once) in W^2*W_f; and f=W gives every
        one of W's own four links occurring three times (odd) in W^3.
        So every one of the required expectations vanishes.

Nothing here reads or imports forward/av1, reverse/av1 or their
check.py. Everything is rebuilt from the frozen I1 table and from
elementary Haar/representation facts.

Run: python3 -B haar_parity_exact.py
"""
from fractions import Fraction as F
from math import comb
from collections import Counter, defaultdict
import json
import sys


# ---------------------------------------------------------------------
# Part A: single-link Haar moments, two independent exact routes
# ---------------------------------------------------------------------

def catalan(k):
    """Exact Catalan number C_k = C(2k,k)/(k+1) (integer division is exact)."""
    if k < 0:
        return 0
    num = comb(2 * k, k)
    assert num % (k + 1) == 0
    return num // (k + 1)


def moment_clebsch_gordan(n):
    """
    E[w^n] via the trivial-representation multiplicity in (1/2)^{tensor n}.
    Odd n: total spin of n spin-1/2's is always half-integer, so the
    trivial (spin-0) representation never occurs -> multiplicity 0.
    Even n=2m: multiplicity is the Catalan number C_m (reflection
    principle / ballot problem for the spin-projection random walk).
    """
    if n % 2 == 1:
        return F(0)
    m = n // 2
    return F(catalan(m), 2 ** n)


def moment_wallis_beta(n):
    """
    E[w^n] via w=cos(phi), Haar density (2/pi) sin^2(phi) on [0,pi]
    (Weyl integration formula for SU(2), I1's own W=(1/2)Tr U convention).

        E[w^n] = (2/pi) * Integral_0^pi cos^n(phi) sin^2(phi) dphi
               = (2/pi) * [ I(n) - I(n+2) ],  I(n):=Integral_0^pi cos^n(phi) dphi.

    I(n) = 0 for odd n; for n=2m, the classical Wallis formula gives
        I(2m) = pi * C(2m,m) / 4^m.
    The factor of pi in I(2m) is cancelled EXACTLY and symbolically by
    the 2/pi prefactor before any arithmetic is done -- pi itself never
    has to be represented, floating or otherwise.
    """
    if n % 2 == 1:
        return F(0)
    m = n // 2
    # (2/pi) * pi * [ C(2m,m)/4^m - C(2m+2,m+1)/4^{m+1} ]
    term1 = F(comb(2 * m, m), 4 ** m)
    term2 = F(comb(2 * m + 2, m + 1), 4 ** (m + 1))
    return 2 * (term1 - term2)


def check_part_a():
    expected = {0: F(1), 1: F(0), 2: F(1, 4), 3: F(0), 4: F(1, 8)}
    rows = []
    ok = True
    for n in range(0, 5):
        cg = moment_clebsch_gordan(n)
        wb = moment_wallis_beta(n)
        exp = expected[n]
        row_ok = (cg == wb == exp)
        ok = ok and row_ok
        rows.append({
            "n": n,
            "E_w_n_clebsch_gordan": str(cg),
            "E_w_n_wallis_beta": str(wb),
            "expected": str(exp),
            "routes_agree": (cg == wb),
            "matches_expected": row_ok,
        })
    return ok, rows


# ---------------------------------------------------------------------
# Part B: the plaquette W is Haar-distributed like a single link
# ---------------------------------------------------------------------

DIRS = ("x", "y", "z")


def unit(d):
    v = [0, 0, 0]
    v[DIRS.index(d)] = 1
    return tuple(v)


def padd(p, v):
    return (p[0] + v[0], p[1] + v[1], p[2] + v[2])


def owner_factor(tail):
    """Coarse factor owning a fine link with the given tail (I1 section 2)."""
    x, y, z = tail
    return (x // 4, y // 2, z)


def face_links(p, a, c):
    """
    I1.4: face at p, directions a<c, has positive link tails
    p, p+e_a, p+e_c, p -- i.e. the four (tail,direction) edges
    (p,a), (p+e_a,c), (p+e_c,a), (p,c).
    """
    assert DIRS.index(a) < DIRS.index(c)
    ea, ec = unit(a), unit(c)
    return frozenset([(p, a), (padd(p, ea), c), (padd(p, ec), a), (p, c)])


# The original xz Wilson loop, AT4-F04 / AV1 section 1:
#   W = (1/2) Tr[U_{0,x} U_{e_x,z} U_{e_z,x}^{-1} U_{0,z}^{-1}]
# This is exactly the I1.4 face at p=(0,0,0), directions x<z.
W_LINKS = face_links((0, 0, 0), "x", "z")
_expected_W_links = frozenset([
    ((0, 0, 0), "x"), ((1, 0, 0), "z"), ((0, 0, 1), "x"), ((0, 0, 0), "z"),
])
assert W_LINKS == _expected_W_links, "W link reconstruction does not match AT4-F04"
W_OWNER_SET = frozenset(owner_factor(t) for (t, d) in W_LINKS)
assert W_OWNER_SET == {(0, 0, 0), (0, 0, 1)}, "W owner set must be {0,e_z}"


def check_part_b(moments):
    """
    W's four links are four distinct fine SU(2) links (checked: |W_LINKS|=4),
    hence independent Haar variables. Fixing three of them, the fourth link's
    Haar-ness plus Haar right-invariance makes W = (1/2)Tr(U1 U2 U3^-1 U4^-1)
    Haar-distributed exactly like the single link w. So E[W^n]=E[w^n] for
    every n, with no separate computation needed.
    """
    distinct_links = len(W_LINKS)
    ok = (distinct_links == 4)
    E_W = moments[1]
    E_W2 = moments[2]
    ok = ok and (E_W == F(0)) and (E_W2 == F(1, 4))
    return ok, {
        "W_links": sorted([(list(t), d) for (t, d) in W_LINKS]),
        "distinct_links_in_W": distinct_links,
        "W_owner_set": sorted(list(W_OWNER_SET)),
        "omega_0(W)": str(E_W),
        "omega_0(W^2)": str(E_W2),
    }


# ---------------------------------------------------------------------
# Part C: the 21 omitted I1 classes at anchor 0, and odd-multiplicity
#         vanishing of E[W^2 * W_f] for every omitted f (incl. f=W)
# ---------------------------------------------------------------------

def build_omitted_classes():
    """
    research/round21/forward/i1/report.md section 3 table (21 omitted
    anchored face classes out of 24; the other 3, xy r=0,1,2 s=0, are
    "selected" and excluded here).
    """
    classes = []
    for r in range(3):                      # xy r=0,1,2; s=1 -> {0,e_y}
        classes.append(("xy_s1_r%d" % r, face_links((r, 1, 0), "x", "y")))
    classes.append(("xy_r3_s0", face_links((3, 0, 0), "x", "y")))       # {0,e_x}
    classes.append(("xy_r3_s1", face_links((3, 1, 0), "x", "y")))       # {0,e_x,e_y}
    for r in range(3):                      # xz r=0,1,2; s=0,1 -> {0,e_z}
        for s in range(2):
            classes.append(("xz_r%d_s%d" % (r, s), face_links((r, s, 0), "x", "z")))
    for s in range(2):                      # xz r=3; s=0,1 -> {0,e_x,e_z}
        classes.append(("xz_r3_s%d" % s, face_links((3, s, 0), "x", "z")))
    for r in range(4):                      # yz r=0..3; s=0 -> {0,e_z}
        classes.append(("yz_r%d_s0" % r, face_links((r, 0, 0), "y", "z")))
    for r in range(4):                      # yz r=0..3; s=1 -> {0,e_y,e_z}
        classes.append(("yz_r%d_s1" % r, face_links((r, 1, 0), "y", "z")))
    assert len(classes) == 21
    return classes


def multiplicities(link_lists):
    c = Counter()
    for links in link_lists:
        for l in links:
            c[l] += 1
    return c


def check_part_c():
    classes = build_omitted_classes()
    per_face = []
    all_vanish = True
    max_shared_distinct = 0  # only over f != W
    w_is_among_classes = False
    for name, links in classes:
        is_W = (links == W_LINKS)
        shared = len(links & W_LINKS)
        mult = multiplicities([W_LINKS, W_LINKS, links])  # W^2 * W_f
        odd_links = [l for l, cnt in mult.items() if cnt % 2 == 1]
        vanishes = len(odd_links) > 0
        all_vanish = all_vanish and vanishes
        exclusive = [l for l in links if l not in W_LINKS]
        if is_W:
            w_is_among_classes = True
        else:
            max_shared_distinct = max(max_shared_distinct, shared)
        per_face.append({
            "face": name,
            "is_W_itself": is_W,
            "shared_links_with_W": shared,
            "exclusive_links_to_f": len(exclusive),
            "odd_multiplicity_links_in_W2_Wf": len(odd_links),
            "E[W^2 * W_f]_vanishes": vanishes,
        })

    # W is one of its own star's 21 omitted classes (r=0,s=0 xz face); the
    # f=W row above already computes W^2*W == W^3 and finds it vanishes.
    # Cross-check that identical computation directly from W_LINKS alone.
    mult_w3 = multiplicities([W_LINKS, W_LINKS, W_LINKS])
    odd_w3 = [l for l, c in mult_w3.items() if c % 2 == 1]
    w3_vanishes = len(odd_w3) == 4  # all four links occur 3 times each (odd)
    all_vanish = all_vanish and w3_vanishes

    # AV1's own fact, re-derived independently here: two DISTINCT omitted
    # faces (f != W) share at most one link.
    distinct_faces_ok = (max_shared_distinct <= 1)

    ok = all_vanish and distinct_faces_ok and w_is_among_classes
    return ok, {
        "num_omitted_classes_checked": len(classes),
        "W_is_one_of_the_21_omitted_classes": w_is_among_classes,
        "max_links_shared_by_two_DISTINCT_omitted_faces": max_shared_distinct,
        "per_face": per_face,
        "E[W^3]_odd_multiplicity_links": len(odd_w3),
        "E[W^3]_vanishes": w3_vanishes,
    }


# ---------------------------------------------------------------------
# Assemble and report
# ---------------------------------------------------------------------

def main():
    a_ok, a_rows = check_part_a()
    moments = {r["n"]: F(r["expected"]) for r in a_rows}  # exact, from Part A
    b_ok, b_info = check_part_b(moments)
    c_ok, c_info = check_part_c()

    # AV1 contract reference_moments reproduced (values only; the contract
    # file itself is read here purely as a target datum, not as code).
    reference_moments = {"omega_0(W)": "0", "omega_0(W^2)": "1/4"}
    ref_ok = (b_info["omega_0(W)"] == reference_moments["omega_0(W)"] and
              b_info["omega_0(W^2)"] == reference_moments["omega_0(W^2)"])

    overall_pass = bool(a_ok and b_ok and c_ok and ref_ok)

    result = {
        "script": "haar_parity_exact.py",
        "arithmetic": "fractions.Fraction only; no floats; no sympy",
        "part_a_single_link_moments": {"pass": a_ok, "rows": a_rows},
        "part_b_plaquette_is_haar_distributed": {"pass": b_ok, **b_info},
        "part_c_odd_multiplicity_vanishing": {"pass": c_ok, **c_info},
        "av1_reference_moments_reproduced": {"pass": ref_ok, **reference_moments},
        "overall_pass": overall_pass,
    }

    print(json.dumps(result, indent=2))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
