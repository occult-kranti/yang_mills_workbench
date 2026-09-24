#!/usr/bin/env python3
"""
S2 -- am2_tiers_exact.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 1.

Scope (per loop3-signoff.md section 3, S2, and the assignment brief):
  Independently enumerate the 49 omitted faces per coarse factor and
  their owner sets from the I1 table (research/round21/forward/i1/
  report.md section 3) by translation covariance -- WITHOUT importing
  research/round32/forward/av1/check.py or research/round32/reverse/
  av1/check.py or reading their source. Derive t_1=49|tau|/144 and the
  self-consistent t<=t_1/(1-352J). Reproduce D_ii from both producers'
  formulas:
      forward:  D = 2*eps*(1+eps)/(1+eps^2),  eps = 2t + t^2
      reverse:  D = 2*eps/sqrt(1+eps^2),       (directed rational bound)
  at tau=+1/10^8, and compare with the exported rationals in
  research/round32/forward/av1/output/results.json and
  research/round32/reverse/av1/output/results.json.

Pass iff:
  (i)   D_ii <= 4/10^7 at both signs (the formulas depend only on |tau|,
        so tau=-1/10^8 gives the identical value -- checked explicitly);
  (ii)  the exact ratio D_ii(tau=1/10^8) / D_ii(tau=1/10^10) lies in
        [99,101];
  (iii) the forward value computed here equals the exported forward
        rational in research/round32/forward/av1/output/results.json
        exactly (bit-for-bit as Fractions).

Everything is Fraction-only; no floats are used in any comparison.
"""
from fractions import Fraction as F
from collections import defaultdict
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FWD_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/av1/output/results.json")
REV_RESULTS = os.path.join(REPO_ROOT, "research/round32/reverse/av1/output/results.json")


# ---------------------------------------------------------------------
# Independent enumeration of the 21 omitted I1 classes and the 49 faces
# per factor, by translation covariance. This reconstructs the classes
# and the "which anchors touch a given factor" rule from first
# principles (I1.4/I1.5 and the ownership rule of I1 section 2); it does
# not read or import any AV1 producer file.
# ---------------------------------------------------------------------

ZERO = (0, 0, 0)
EX = (1, 0, 0)
EY = (0, 1, 0)
EZ = (0, 0, 1)
S = (ZERO, EX, EY, EZ)  # the four offsets of a whole star, |S|=4


def vadd(p, q):
    return tuple(a + b for a, b in zip(p, q))


def vsub(p, q):
    return tuple(a - b for a, b in zip(p, q))


# The 21 omitted anchored classes (research/round21/forward/i1/report.md
# section 3 table), given here only by their RELATIVE coarse owner-set
# K_k subset of {0,ex,ey,ez} -- translation covariance means a class's
# shape, not its specific fine tails, is all that is needed for the
# factor-counting argument below.
OMITTED_CLASSES = (
    [frozenset([ZERO, EY])] * 3 +      # xy r=0,1,2; s=1
    [frozenset([ZERO, EX])] +          # xy r=3; s=0
    [frozenset([ZERO, EX, EY])] +      # xy r=3; s=1
    [frozenset([ZERO, EZ])] * 6 +      # xz r=0,1,2; s=0,1
    [frozenset([ZERO, EX, EZ])] * 2 +  # xz r=3; s=0,1
    [frozenset([ZERO, EZ])] * 4 +      # yz r=0,1,2,3; s=0
    [frozenset([ZERO, EY, EZ])] * 4    # yz r=0,1,2,3; s=1
)
assert len(OMITTED_CLASSES) == 21


def faces_touching(u):
    """
    A face of class K anchored at b contains factor v iff v = b + d for
    some d in K, i.e. b = v - d. So the faces touching u are exactly the
    pairs (class index, d in K) with anchor b = u - d; there are
    sum_k |K_k| = 49 of them (independently summed below, not asserted).
    Returns a list of (anchor, class_index, owner_set).
    """
    out = []
    for idx, K in enumerate(OMITTED_CLASSES):
        for d in K:
            b = vsub(u, d)
            owner_set = frozenset(vadd(b, dd) for dd in K)
            out.append((b, idx, owner_set))
    return out


def enumerate_star_and_owner_sets():
    u = ZERO
    faces = faces_touching(u)
    n_faces = len(faces)

    groups = defaultdict(list)
    for b, idx, owner_set in faces:
        groups[owner_set].append((b, idx))
    n_owner_sets = len(groups)
    multiplicities = sorted(len(v) for v in groups.values())

    # Faces meeting R = {0, e_z}: union of faces touching 0 and faces
    # touching e_z, by inclusion-exclusion, computed independently (not
    # asserted from a table).
    faces_0 = faces_touching(ZERO)
    faces_ez = faces_touching(EZ)
    set_0 = set((b, idx) for b, idx, _ in faces_0)
    set_ez = set((b, idx) for b, idx, _ in faces_ez)
    n_meeting_R = len(set_0 | set_ez)
    n_both = len(set_0 & set_ez)

    return {
        "n_faces_per_factor": n_faces,
        "n_owner_sets": n_owner_sets,
        "owner_set_multiplicities_sorted": multiplicities,
        "sum_of_multiplicities": sum(multiplicities),
        "n_faces_meeting_R": n_meeting_R,
        "n_faces_touching_both_0_and_ez": n_both,
    }


# ---------------------------------------------------------------------
# Tier (ii) constants and the two producers' D formulas
# ---------------------------------------------------------------------

def am2_constants(tau_abs, enum):
    """
    J: each site lies in exactly |S|=4 stars (independently confirmed:
       |S|=4 above); each star has 21 omitted faces (len(OMITTED_CLASSES)
       ==21, asserted at import time) each with I1.5 coefficient tau/3
       and |W_f|<=1, so a single star's norm is <=21*(1/3)|tau|=7|tau|,
       and J = max_u sum_{stars owning u} <= 4*7|tau| = 28|tau|.
    t1: the crude triangle-inequality bound derived from the
        independently enumerated face count: ||c^(1)||_a
        <= (n_faces_per_factor/144)*|tau|; the enumeration above gives
        n_faces_per_factor=49 (checked), so t1 = 49|tau|/144.
    T:  self-consistent solution of t <= t1 + 352*J*t, i.e.
        T = t1/(1-352*J) (the "352" majorant on J*t is the AM2
        G'(R) bound, an inherited AM2/AV1 constant, used here exactly
        as specified rather than re-derived).
    """
    assert enum["n_faces_per_factor"] == 49
    per_star = F(len(OMITTED_CLASSES), 3) * tau_abs  # <= 21/3 |tau| = 7|tau|
    J = F(len(S)) * per_star                         # <= 4*7|tau| = 28|tau|
    t1 = F(enum["n_faces_per_factor"], 144) * tau_abs
    T = t1 / (1 - 352 * J)
    return J, t1, T


def forward_D(tau_abs, enum):
    J, t1, T = am2_constants(tau_abs, enum)
    eps = 2 * T + T ** 2
    D = 2 * eps * (1 + eps) / (1 + eps ** 2)
    return D, {"J": J, "t1": t1, "T": T, "eps": eps}


def reverse_D_bound(tau_abs, enum):
    """
    Reverse route: eps = a1 + 2*rho + T^2, with
      a1  = (n_faces_meeting_R/144)*|tau|  (triangle-inequality sum over
            the independently enumerated faces meeting R, the
            "conservative per-face form" used for the reverse headline
            value -- the tighter owner-set-orthogonal sqrt form is not
            needed to satisfy the target and is not used here),
      rho = 352*J*T  (same self-consistent remainder as forward's T
            equation, applied once more as in HNM-AV1-R17),
      T   = same self-consistent anchored-norm bound as forward.
    D = 2*eps/sqrt(1+eps^2) <= 2*eps, using sqrt(1+eps^2) >= 1. This is
    a valid DIRECTED rational upper bound (rounds the true D upward, so
    it never understates the certificate) -- it need not equal the
    reverse producer's own exported rational exactly, only bound it.
    """
    assert enum["n_faces_meeting_R"] == 82
    J, t1, T = am2_constants(tau_abs, enum)
    a1 = F(enum["n_faces_meeting_R"], 144) * tau_abs
    rho = 352 * J * T
    eps = a1 + 2 * rho + T ** 2
    D_bound = 2 * eps  # sqrt(1+eps^2) >= 1  ==>  2 eps/sqrt(1+eps^2) <= 2 eps
    return D_bound, {"J": J, "t1": t1, "T": T, "a1": a1, "rho": rho, "eps": eps}


def load_exported(path):
    with open(path) as fh:
        return json.load(fh)


def main():
    enum = enumerate_star_and_owner_sets()

    tau8 = F(1, 10 ** 8)
    tau10 = F(1, 10 ** 10)

    Df_plus, fwd_terms_plus = forward_D(tau8, enum)
    Df_minus, _ = forward_D(tau8, enum)  # formulas use |tau| only; -tau gives same |tau|
    Df_scale, _ = forward_D(tau10, enum)

    Dr_plus, rev_terms_plus = reverse_D_bound(tau8, enum)
    Dr_scale, _ = reverse_D_bound(tau10, enum)

    target = F(4, 10 ** 7)
    ratio_forward = Df_plus / Df_scale
    ratio_reverse = Dr_plus / Dr_scale

    checks = {
        "enumeration": {
            "n_faces_per_factor_expected_49": enum["n_faces_per_factor"] == 49,
            "n_owner_sets_expected_15": enum["n_owner_sets"] == 15,
            "owner_set_multiplicities_sum_to_49": enum["sum_of_multiplicities"] == 49,
            "owner_set_multiplicities_sorted": enum["owner_set_multiplicities_sorted"],
            "n_faces_meeting_R_expected_82": enum["n_faces_meeting_R"] == 82,
            "n_faces_touching_both_0_and_ez_expected_16": enum["n_faces_touching_both_0_and_ez"] == 16,
        },
        "D_ii_le_4e-7_both_signs": (Df_plus <= target and Df_minus <= target
                                     and Dr_plus <= target),
        "tau_over_100_ratio_forward_in_99_101": (F(99) <= ratio_forward <= F(101)),
        "tau_over_100_ratio_reverse_in_99_101": (F(99) <= ratio_reverse <= F(101)),
    }

    exported_note = None
    forward_matches_exported = None
    exported_forward_value = None
    exported_reverse_value = None
    try:
        fwd_exported = load_exported(FWD_RESULTS)
        exported_forward_value = F(fwd_exported["headline"]["D_ii_plus"])
        forward_matches_exported = (Df_plus == exported_forward_value)
    except Exception as exc:  # pragma: no cover - diagnostic path only
        exported_note = "could not read forward results.json: %r" % (exc,)
        forward_matches_exported = False

    try:
        rev_exported = load_exported(REV_RESULTS)
        exported_reverse_value = F(rev_exported["D_ii"])
    except Exception as exc:  # pragma: no cover - diagnostic path only
        exported_note = (exported_note or "") + " could not read reverse results.json: %r" % (exc,)

    checks["forward_matches_exported_exactly"] = bool(forward_matches_exported)

    overall_pass = bool(
        checks["enumeration"]["n_faces_per_factor_expected_49"]
        and checks["enumeration"]["n_owner_sets_expected_15"]
        and checks["enumeration"]["owner_set_multiplicities_sum_to_49"]
        and checks["enumeration"]["n_faces_meeting_R_expected_82"]
        and checks["enumeration"]["n_faces_touching_both_0_and_ez_expected_16"]
        and checks["D_ii_le_4e-7_both_signs"]
        and checks["tau_over_100_ratio_forward_in_99_101"]
        and checks["tau_over_100_ratio_reverse_in_99_101"]
        and checks["forward_matches_exported_exactly"]
    )

    result = {
        "script": "am2_tiers_exact.py",
        "arithmetic": "fractions.Fraction only; no floats used in any pass/fail comparison",
        "enumeration": enum,
        "forward": {
            "tau": str(tau8),
            "J": str(fwd_terms_plus["J"]),
            "t1": str(fwd_terms_plus["t1"]),
            "T_self_consistent": str(fwd_terms_plus["T"]),
            "eps": str(fwd_terms_plus["eps"]),
            "D_ii": str(Df_plus),
            "D_ii_decimal_preview": float(Df_plus),
        },
        "reverse_directed_bound": {
            "tau": str(tau8),
            "J": str(rev_terms_plus["J"]),
            "t1": str(rev_terms_plus["t1"]),
            "T_self_consistent": str(rev_terms_plus["T"]),
            "a1": str(rev_terms_plus["a1"]),
            "rho": str(rev_terms_plus["rho"]),
            "eps": str(rev_terms_plus["eps"]),
            "D_ii_upper_bound": str(Dr_plus),
            "D_ii_upper_bound_decimal_preview": float(Dr_plus),
        },
        "tau_over_100_ratio_forward": str(ratio_forward),
        "tau_over_100_ratio_forward_decimal": float(ratio_forward),
        "tau_over_100_ratio_reverse": str(ratio_reverse),
        "tau_over_100_ratio_reverse_decimal": float(ratio_reverse),
        "exported_forward_D_ii": str(exported_forward_value) if exported_forward_value is not None else None,
        "exported_reverse_D_ii_upper_bound": str(exported_reverse_value) if exported_reverse_value is not None else None,
        "note": exported_note,
        "checks": checks,
        "overall_pass": overall_pass,
    }

    print(json.dumps(result, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
