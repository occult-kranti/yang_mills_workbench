#!/usr/bin/env python3
"""
T1 -- j0_contraction_replay.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 3.

Zero research loops: test/planning script, not a producer, skeptic or
advisor artifact. Does not read or import research/round32/forward/ax1/
check.py or research/round32/reverse/ax1/check.py -- only their frozen
JSON exports (data, not code) and the frozen contract/gate JSON.

Task (update-2.md section 5, test 1): recompute, as exact Fractions,

    J'      = 29|tau|
    J_0'    = 29/10^8
    G(R)    < 148/7
    G'(R)   < 352
    J_0'G(R)    < 1073/175000000 < 1/64
    2J_0'G'(R)  < 319/1562500    < 1

and show the OLD J_0 = 7/25000000 < 29/10^8 (the re-freeze is upward,
R1, not a loosening).

Method (self-contained; independent of both check.py files):
  1. Prove exp(1/8) < 8/7 from scratch with a rigorous truncated Taylor
     series plus an exact geometric tail bound (Fraction only) -- the
     same style of directed enclosure this lens's assistant-1 used for
     pi (window_kernel_budget.py's Machin bounds), applied here to exp.
  2. Feed that 8/7 bound through the SAME arithmetic chain the AX1
     report states (HNM-AX1-F06/F07) to reproduce 148/7 and 352
     literally (not merely "some valid bound" -- the exact named
     rationals, since 1073/175000000 and 319/1562500 are defined from
     these specific numbers).
  3. Re-derive J'=29|tau| from route B's own additive structure
     (4 stars x 7|tau| + 1 single-factor group x |tau|), independently
     of the face-geometry enumeration done in this lens's script 2/3.
  4. Assemble the two contraction rationals and compare them, and every
     intermediate, bit-for-bit against BOTH producers' exported
     j0_resolution blocks.

Arithmetic: fractions.Fraction only; no floats in any comparison.
Run with: python3 -B j0_contraction_replay.py
"""
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FWD_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/ax1/output/results.json")
REV_RESULTS = os.path.join(REPO_ROOT, "research/round32/reverse/ax1/output/results.json")
AX1_CONTRACT = os.path.join(REPO_ROOT, "research/round32/contracts/ax1.json")


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


# ---------------------------------------------------------------------
# Step 1: exp(1/8) < 8/7, proved from scratch with an exact rational
# truncated-series + geometric-tail bound (no reliance on the report's
# own truncation degree or huge intermediate fraction).
# ---------------------------------------------------------------------

def exp_upper_bound(x, n_terms):
    """
    Rigorous Fraction upper bound on exp(x) for 0 < x < 1, using the
    first n_terms of the Taylor series plus an exact geometric bound on
    the remainder:

        exp(x) = sum_{k=0}^{n_terms-1} x^k/k! + R,
        R = sum_{k=n_terms}^inf x^k/k!
          <= (x^n_terms/n_terms!) * sum_{j=0}^inf (x/(n_terms+1))^j
          =  (x^n_terms/n_terms!) * (n_terms+1)/(n_terms+1-x)   [since x/(n_terms+1)<1]

    This is valid because term_{k+1}/term_k = x/(k+1) is DECREASING in k,
    so from k=n_terms on, every ratio is <= x/(n_terms+1).
    """
    assert 0 < x < 1
    partial = F(0)
    term = F(1)
    for k in range(n_terms):
        partial += term
        term *= x
        term /= (k + 1)
    # term is now x^n_terms / n_terms!
    ratio_cap = x / (n_terms + 1)
    assert ratio_cap < 1
    tail_bound = term / (1 - ratio_cap)
    return partial + tail_bound


def prove_exp_eighth_lt_8_7():
    x = F(1, 8)
    upper = exp_upper_bound(x, 10)
    target = F(8, 7)
    ok = upper < target
    return upper, target, ok


# ---------------------------------------------------------------------
# Step 2: G(R)<148/7, G'(R)<352, via the exact arithmetic chain
# HNM-AX1-F06 states (G(t)=16 e^{8t}(1+10t), G'(t)=16 e^{8t}(18+80t),
# t=R=1/64, so 8t=1/8 -- this is the SAME exponent bounded in step 1):
#     G(1/64)  < 16*(8/7)*(1+10/64) = 16*(8/7)*(74/64)  = 148/7
#     G'(1/64) < 16*(8/7)*(18+80/64)= 16*(8/7)*(77/4)   = 352
# Using literally 8/7 (proved valid in step 1, not a tighter self-bound)
# reproduces these two named rationals exactly.
# ---------------------------------------------------------------------

def G_and_Gprime_bounds(exp_bound_8_7):
    R = F(1, 64)
    G_R = 16 * exp_bound_8_7 * (1 + 10 * R)
    Gp_R = 16 * exp_bound_8_7 * (18 + 80 * R)
    return R, G_R, Gp_R


# ---------------------------------------------------------------------
# Step 3: J' = 29|tau| from route B's additive structure (HNM-AX1-F04):
# a site lies in exactly 4 stars (S={0,ex,ey,ez}) and exactly 1
# single-factor group; each star's 21 omitted faces give norm
# <=21*(1/3)|tau|=7|tau|, each single-factor group's 3 selected faces
# give norm <=3*(1/3)|tau|=|tau|.
# ---------------------------------------------------------------------

def route_b_J_prime(tau_abs):
    n_omitted_per_star = 21
    n_selected_per_group = 3
    per_star = F(n_omitted_per_star, 3) * tau_abs
    per_group = F(n_selected_per_group, 3) * tau_abs
    assert per_star == 7 * tau_abs
    assert per_group == tau_abs
    n_stars_per_site = 4
    n_groups_per_site = 1
    J_prime = n_stars_per_site * per_star + n_groups_per_site * per_group
    return J_prime, per_star, per_group


def main():
    exp_upper, exp_target, exp_ok = prove_exp_eighth_lt_8_7()

    R, G_R, Gp_R = G_and_Gprime_bounds(F(8, 7))
    G_R_expected = F(148, 7)
    Gp_R_expected = F(352)
    G_R_matches = (G_R == G_R_expected)
    Gp_R_matches = (Gp_R == Gp_R_expected)

    tau_cap = F(1, 10 ** 8)
    J_prime, per_star, per_group = route_b_J_prime(tau_cap)
    J_prime_over_tau = J_prime / tau_cap
    assert J_prime_over_tau == 29

    J0_prime = F(29, 10 ** 8)
    J_prime_equals_J0_prime_at_cap = (J_prime == J0_prime)

    self_map = J0_prime * G_R_expected
    self_map_expected = F(1073, 175000000)
    self_map_matches = (self_map == self_map_expected)
    self_map_lt_radius = (self_map < F(1, 64))

    exclusion = 2 * J0_prime * Gp_R_expected
    exclusion_expected = F(319, 1562500)
    exclusion_matches = (exclusion == exclusion_expected)
    exclusion_lt_one = (exclusion < 1)

    J0_old = F(7, 25000000)
    J0_old_as_29ths = J0_old  # = 28/10^8
    assert J0_old_as_29ths == F(28, 10 ** 8)
    old_lt_new = (J0_old < J0_prime)

    # ---- cross-check bit-for-bit against both producers' exports ----
    fwd = load_json(FWD_RESULTS)
    rev = load_json(REV_RESULTS)
    contract = load_json(AX1_CONTRACT)

    fwd_j0 = fwd["j0_resolution"]
    rev_j0 = rev["j0_resolution"]

    fwd_checks = {
        "J0_prime": F(fwd_j0["J0_prime"]) == J0_prime,
        "self_map": F(fwd_j0["self_map"]) == self_map,
        "exclusion": F(fwd_j0["exclusion"]) == exclusion,
        "tau_cap": F(fwd_j0["tau_cap"]) == tau_cap,
        "contract_sha256": fwd_j0["contract_sha256"],
    }
    rev_checks = {
        "J0_prime": F(rev_j0["J0_prime"]) == J0_prime,
        "J_prime_at_cap": F(rev_j0["J_prime_at_cap"]) == J_prime,
        "G_R_upper": F(rev_j0["G_R_upper"]) == G_R_expected,
        "G_prime_R_upper": F(rev_j0["G_prime_R_upper"]) == Gp_R_expected,
        "self_map_upper": F(rev_j0["self_map_upper"]) == self_map,
        "contraction_upper": F(rev_j0["contraction_upper"]) == exclusion,
        "frozen_AM2_J0": F(rev_j0["frozen_AM2_J0"]) == J0_old,
        "radius": F(rev_j0["radius"]) == F(1, 64),
    }
    # The contract itself carries no self-hash; both producers recorded
    # the SAME sha256 of the contract snapshot they read, which is the
    # meaningful cross-check (both froze against the identical contract).
    contract_hash_consistent = (fwd_j0["contract_sha256"] == rev_j0["contract_sha256"])
    assert contract.get("id") == "AX1"

    all_fwd_ok = all(v is True for k, v in fwd_checks.items() if k != "contract_sha256")
    all_rev_ok = all(v is True for k, v in rev_checks.items())

    overall_pass = bool(
        exp_ok
        and G_R_matches
        and Gp_R_matches
        and J_prime_equals_J0_prime_at_cap
        and self_map_matches
        and self_map_lt_radius
        and exclusion_matches
        and exclusion_lt_one
        and old_lt_new
        and all_fwd_ok
        and all_rev_ok
        and contract_hash_consistent
    )

    def s(x):
        return str(x) if isinstance(x, F) else x

    result = {
        "script": "j0_contraction_replay.py",
        "zero_research_loops": True,
        "arithmetic": "fractions.Fraction only; no floats in any comparison",
        "step1_exp_eighth_bound": {
            "method": "10-term Taylor truncation + exact geometric tail bound",
            "exp_1_8_upper_bound_exact": s(exp_upper),
            "exp_1_8_upper_bound_decimal_preview": float(exp_upper),
            "target_8_7_decimal_preview": float(exp_target),
            "exp_1_8_lt_8_7": exp_ok,
        },
        "step2_G_bounds": {
            "R": s(R),
            "G_R": s(G_R), "G_R_expected_148_7": s(G_R_expected), "G_R_matches": G_R_matches,
            "Gp_R": s(Gp_R), "Gp_R_expected_352": s(Gp_R_expected), "Gp_R_matches": Gp_R_matches,
        },
        "step3_J_prime": {
            "per_star_over_tau": s(per_star / tau_cap),
            "per_group_over_tau": s(per_group / tau_cap),
            "J_prime": s(J_prime),
            "J_prime_over_tau": s(J_prime_over_tau),
            "J0_prime": s(J0_prime),
            "J_prime_equals_J0_prime_at_cap": J_prime_equals_J0_prime_at_cap,
        },
        "step4_contraction": {
            "self_map": s(self_map), "self_map_expected": s(self_map_expected),
            "self_map_matches": self_map_matches,
            "self_map_lt_1_64": self_map_lt_radius,
            "exclusion": s(exclusion), "exclusion_expected": s(exclusion_expected),
            "exclusion_matches": exclusion_matches,
            "exclusion_lt_1": exclusion_lt_one,
        },
        "old_vs_new_J0": {
            "J0_old": s(J0_old), "J0_old_decimal_preview": float(J0_old),
            "J0_prime": s(J0_prime), "J0_prime_decimal_preview": float(J0_prime),
            "old_lt_new": old_lt_new,
        },
        "cross_check_forward_j0_resolution": {k: (v if isinstance(v, str) else bool(v)) for k, v in fwd_checks.items()},
        "cross_check_reverse_j0_resolution": {k: bool(v) for k, v in rev_checks.items()},
        "contract_hash_consistent_across_producers": contract_hash_consistent,
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
