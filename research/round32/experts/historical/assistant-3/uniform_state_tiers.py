#!/usr/bin/env python3
"""
T4 -- uniform_state_tiers.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 3.

Zero research loops: test/planning script, not a producer, skeptic or
advisor artifact. Does not read or import research/round32/forward/ax1/
check.py or research/round32/reverse/ax1/check.py -- only their frozen
JSON exports (data, not code).

Task (update-2.md section 5, test 4): reproduce the forward tier-(ii)
state bound

    t_1' = 52|tau|/144
    T'   = t_1'/(1-352J')
    eps  = 2T' + T'^2
    D'   = 2*eps*(1+eps)/(1+eps^2)

bit-for-bit against research/round32/forward/ax1/output/results.json's
D'_ii = 2425369125199104794263242601250/167893028420061547330293754713793182097;
reproduce the reverse's ~1.2224e-8 value as a labelled "88-face" variant
(same T', a1=88|tau|/144 in place of the forward's 2*t_1', rho'=352J'T',
eps_rev=a1+2*rho'+T'^2, D_rev=2*eps_rev -- the exact identity
eps_fwd-eps_rev=16|tau|/144=|tau|/9 the skeptic's independent review
records is checked directly); and check the tau-scaling ratios
D(tau=1e-8)/D(tau=1e-10) lie in [99,101] for both forms.

This reuses this lens's own am2_tiers_exact.py (S2) STRUCTURE (the same
J/t1/T self-consistency pattern, generalized from AV1/AW1's 49-face,
J=28|tau| model to route B's 52-face, J'=29|tau| model) rather than
importing it, since route B changes every constant (49->52, 28->29,
82->88) and the forward/reverse eps formulas here are the two genuinely
different "88-face vs 2x52-face" collections the skeptic's review
itemizes -- not a drop-in reuse of the AV1-era numbers.

Arithmetic: fractions.Fraction only; no floats in any comparison.
Run with: python3 -B uniform_state_tiers.py
"""
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FWD_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/ax1/output/results.json")
REV_RESULTS = os.path.join(REPO_ROOT, "research/round32/reverse/ax1/output/results.json")


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


J_PRIME_COEFF = F(29)      # J' = 29|tau|  (route B, script 1/3)
T1_COEFF = F(52, 144)      # t_1' = 52|tau|/144  (route B, 52 faces per factor)
A1_COEFF = F(88, 144)      # a1 = 88|tau|/144  (route B, 88 faces meeting R)
MAJORANT_352 = F(352)      # inherited AM2/AV1 G'(R)-derived majorant on J*t


def route_b_constants(tau_abs):
    J_prime = J_PRIME_COEFF * tau_abs
    t1_prime = T1_COEFF * tau_abs
    T_prime = t1_prime / (1 - MAJORANT_352 * J_prime)
    rho_prime = MAJORANT_352 * J_prime * T_prime
    return J_prime, t1_prime, T_prime, rho_prime


def forward_D(tau_abs):
    J_prime, t1_prime, T_prime, rho_prime = route_b_constants(tau_abs)
    eps = 2 * T_prime + T_prime ** 2
    D = 2 * eps * (1 + eps) / (1 + eps ** 2)
    return D, {"J_prime": J_prime, "t1_prime": t1_prime, "T_prime": T_prime, "eps": eps}


def reverse_D_88_face_variant(tau_abs):
    """Labelled variant: replaces the forward's 2*T'=2*t1'+2*rho' (which
    double-charges the 16 faces owning both 0 and e_z) with the exact
    88-faces-meeting-R triangle sum a1=88|tau|/144 counted once, plus
    2*rho' for the remainder beyond first order, plus the same T'^2
    pair term. D is the directed bound 2*eps (>= the fidelity form
    2*eps/sqrt(1+eps^2), since sqrt(1+eps^2)>=1)."""
    J_prime, t1_prime, T_prime, rho_prime = route_b_constants(tau_abs)
    a1 = A1_COEFF * tau_abs
    eps = a1 + 2 * rho_prime + T_prime ** 2
    D = 2 * eps
    return D, {"J_prime": J_prime, "T_prime": T_prime, "a1": a1, "rho_prime": rho_prime, "eps": eps}


def main():
    tau8 = F(1, 10 ** 8)
    tau8_minus = -tau8
    tau10 = F(1, 10 ** 10)

    D_fwd_plus, terms_fwd_plus = forward_D(tau8)
    D_fwd_minus, terms_fwd_minus = forward_D(abs(tau8_minus))  # formula uses |tau| only
    D_fwd_scale, _ = forward_D(tau10)

    D_rev_plus, terms_rev_plus = reverse_D_88_face_variant(tau8)
    D_rev_scale, _ = reverse_D_88_face_variant(tau10)

    # the skeptic's own exact identity: eps_fwd - eps_rev = |tau|/9
    eps_diff = terms_fwd_plus["eps"] - terms_rev_plus["eps"]
    eps_diff_expected = tau8 / 9
    eps_diff_matches = (eps_diff == eps_diff_expected)

    # tau-scaling ratios
    ratio_fwd = D_fwd_plus / D_fwd_scale
    ratio_rev = D_rev_plus / D_rev_scale
    ratio_fwd_ok = (F(99) <= ratio_fwd <= F(101))
    ratio_rev_ok = (F(99) <= ratio_rev <= F(101))

    target_4e7 = F(4, 10 ** 7)
    target_1e6 = F(1, 10 ** 6)
    fwd_meets_targets = bool(D_fwd_plus <= target_4e7 and D_fwd_plus <= target_1e6)
    rev_meets_targets = bool(D_rev_plus <= target_4e7 and D_rev_plus <= target_1e6)
    fwd_signs_equal = (D_fwd_plus == D_fwd_minus)

    # --- bit-for-bit cross-check against both producers' exports ---
    fwd = load_json(FWD_RESULTS)
    rev = load_json(REV_RESULTS)

    fwd_tier_ii_plus = fwd["tiers"]["+"]["ii"]
    fwd_tier_ii_minus = fwd["tiers"]["-"]["ii"]
    fwd_checks = {
        "D_plus_matches_exported": F(fwd_tier_ii_plus["D"]) == D_fwd_plus,
        "D_minus_matches_exported": F(fwd_tier_ii_minus["D"]) == D_fwd_minus,
        "t1_matches": F(fwd_tier_ii_plus["t1"]) == terms_fwd_plus["t1_prime"],
        "T_matches": F(fwd_tier_ii_plus["t"]) == terms_fwd_plus["T_prime"],
        "eps_matches": F(fwd_tier_ii_plus["eps"]) == terms_fwd_plus["eps"],
        "two_creation_term_matches": F(fwd_tier_ii_plus["two_creation_term_t2"]) == terms_fwd_plus["T_prime"] ** 2,
        "J_matches": F(fwd_tier_ii_plus["J"]) == terms_fwd_plus["J_prime"],
    }

    rev_tier_ii_plus = rev["tiers"]["tier_ii"]["+"]
    rev_checks = {
        "D_exact_2eps_matches_exported": F(rev_tier_ii_plus["D_exact_2eps"]) == D_rev_plus,
        "T_self_consistent_matches": F(rev_tier_ii_plus["T_self_consistent"]) == terms_rev_plus["T_prime"],
        "a1_matches": F(rev_tier_ii_plus["a1_first_order_meeting_R"]) == terms_rev_plus["a1"],
        "rho_matches": F(rev_tier_ii_plus["remainder_anchored_upper_rho"]) == terms_rev_plus["rho_prime"],
        "epsilon_matches": F(rev_tier_ii_plus["epsilon"]) == terms_rev_plus["eps"],
        "two_creation_term_matches": F(rev_tier_ii_plus["two_creation_term"]) == terms_rev_plus["T_prime"] ** 2,
    }

    # reverse's own exported scaling variant (tau/100), cross-checked too
    rev_scaling = rev["tiers"]["tier_ii"]["scaling_only_tau_over_100"]
    rev_scaling_matches = (F(rev_scaling["D_exact_2eps"]) == D_rev_scale)
    fwd_scaling = fwd["scaling_tau_over_100"]["ii"]
    fwd_scaling_matches = (F(fwd_scaling["D"]) == D_fwd_scale)

    all_fwd_ok = all(fwd_checks.values())
    all_rev_ok = all(rev_checks.values())

    overall_pass = bool(
        fwd_signs_equal
        and eps_diff_matches
        and ratio_fwd_ok
        and ratio_rev_ok
        and fwd_meets_targets
        and rev_meets_targets
        and all_fwd_ok
        and all_rev_ok
        and rev_scaling_matches
        and fwd_scaling_matches
    )

    def s(x):
        return str(x) if isinstance(x, F) else x

    result = {
        "script": "uniform_state_tiers.py",
        "zero_research_loops": True,
        "arithmetic": "fractions.Fraction only; no floats in any comparison",
        "forward_tier_ii": {
            "formula": "t1'=52|tau|/144, T'=t1'/(1-352J'), eps=2T'+T'^2, D=2eps(1+eps)/(1+eps^2)",
            "tau": str(tau8),
            "J_prime": s(terms_fwd_plus["J_prime"]),
            "t1_prime": s(terms_fwd_plus["t1_prime"]),
            "T_prime": s(terms_fwd_plus["T_prime"]),
            "eps": s(terms_fwd_plus["eps"]),
            "D": s(D_fwd_plus),
            "D_decimal_preview": float(D_fwd_plus),
            "signs_equal": fwd_signs_equal,
        },
        "reverse_88_face_variant": {
            "formula": "same T'; a1=88|tau|/144, rho'=352J'T', eps=a1+2rho'+T'^2, D=2eps (directed, >= fidelity form)",
            "tau": str(tau8),
            "a1": s(terms_rev_plus["a1"]),
            "rho_prime": s(terms_rev_plus["rho_prime"]),
            "eps": s(terms_rev_plus["eps"]),
            "D": s(D_rev_plus),
            "D_decimal_preview": float(D_rev_plus),
        },
        "eps_difference_identity": {
            "eps_fwd_minus_eps_rev": s(eps_diff),
            "expected_tau_over_9": s(eps_diff_expected),
            "matches": eps_diff_matches,
        },
        "tau_scaling_ratio_1e-8_over_1e-10": {
            "forward": s(ratio_fwd), "forward_decimal": float(ratio_fwd), "forward_in_99_101": ratio_fwd_ok,
            "reverse_variant": s(ratio_rev), "reverse_decimal": float(ratio_rev), "reverse_in_99_101": ratio_rev_ok,
        },
        "targets": {
            "forward_meets_4e-7_and_1e-6": fwd_meets_targets,
            "reverse_variant_meets_4e-7_and_1e-6": rev_meets_targets,
        },
        "cross_check_forward_exported": fwd_checks,
        "cross_check_reverse_exported": rev_checks,
        "cross_check_forward_scaling_variant": fwd_scaling_matches,
        "cross_check_reverse_scaling_variant": rev_scaling_matches,
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
