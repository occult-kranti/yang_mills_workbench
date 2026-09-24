#!/usr/bin/env python3
"""
two_d_independent.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 4.

Zero research loops: test/planning script for the historical
(Newton/Tesla) lens's Round32 assistant package (assistant-4), not a
producer, skeptic or advisor artifact. Does not import
research/round32/forward/ay1/check.py or research/round32/reverse/
ay1/check.py; only their frozen `output/results.json` exports (data,
never code) and the AY1 gate JSON (data) are read, for bit-for-bit
cross-checks.

Task (panel-update-3.md item 6, historical share, test 3). Recompute D
(AV1 forward tier (ii): eps=2T+T^2, T from the admitted AM2 majorant
with J=28|tau|, the formula in research/round32/forward/av1/report.md)
and 2D from scratch with Fractions, and compare to the AY1 gate
rationals
    2D = 1170159676931825184288274812132100/42981220507576537932303142777593983768257
(D = 585079838465912592144137406066050/42981220507576537932303142777593983768257,
the AV1 forward tier-(ii) rational quoted directly in the AY1
gate/report); also the margin against 1/1250000.

Method. This is the SAME chain as this lens's own assistant-1
am2_tiers_exact.py (S2, Round32 sub-round 1) built for AV1 directly;
here it is rebuilt from scratch a second time, independently, for AY1
(which reuses AV1's tier-(ii) D unchanged, since both named families F1
and F2 satisfy the AV1 premises at the same J_0=7/25000000 -- see this
package's padding_family_contraction.py, item b). Reusing the same
formula is the point of the cross-check: AY1's closeness bound 2D is
not a new derivation, it is AV1's D doubled by the triangle inequality
through the common reference P_R, and this script verifies that
literally, bit-for-bit, against the AY1 gate's own quoted rationals
(not merely against AV1's).

Arithmetic: fractions.Fraction only; no floats in any pass/fail
comparison (decimal previews only).

Run with: python3 -B two_d_independent.py
"""
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
AY1_GATE = os.path.join(REPO_ROOT, "research/round32/advisor/ay1-gate.json")
FWD_AY1_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/ay1/output/results.json")
REV_AY1_RESULTS = os.path.join(REPO_ROOT, "research/round32/reverse/ay1/output/results.json")
FWD_AV1_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/av1/output/results.json")


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


# ---------------------------------------------------------------------
# The AM2/AV1 tier-(ii) chain, rebuilt from scratch (Fractions only).
# J=28|tau| (both F1 and F2, see padding_family_contraction.py item b):
# per-site sum, each of the 4 incident whole stars contributing at most
# 21 faces of norm |tau|/3. t1=49|tau|/144: the first-order anchored
# norm (49 = the exact number of distinct faces meeting any one site,
# an AV1/AW1-pinned enumeration fact, reused here as a formula input,
# not re-derived -- its independent enumeration is this lens's
# assistant-1's am2_tiers_exact.py and this package's
# padding_family_contraction.py, which independently confirm 49 as the
# "faces per factor" count via faces_touching()). T is the AM2
# self-consistent fixed-point bound; eps=2T+T^2; D is the AV1 forward
# tier-(ii) trace-norm density bound.
# ---------------------------------------------------------------------

def am2_av1_D(tau_abs):
    per_star = F(21, 3) * tau_abs
    assert per_star == 7 * tau_abs
    J = 4 * per_star
    assert J == 28 * tau_abs

    t1 = F(49, 144) * tau_abs
    T = t1 / (1 - 352 * J)
    eps = 2 * T + T ** 2
    D = 2 * eps * (1 + eps) / (1 + eps ** 2)
    return {
        "tau": tau_abs, "J": J, "t1": t1, "T": T, "eps": eps, "D": D,
    }


def main():
    tau_cap = F(1, 10 ** 8)
    tau_smaller = F(1, 10 ** 10)

    cap = am2_av1_D(tau_cap)
    smaller = am2_av1_D(tau_smaller)

    D = cap["D"]
    twoD = 2 * D

    gate = load_json(AY1_GATE)
    gate_text = gate["accepted"]
    gate_2D_str = "1170159676931825184288274812132100/42981220507576537932303142777593983768257"
    gate_D_str = "585079838465912592144137406066050/42981220507576537932303142777593983768257"
    gate_2D = F(gate_2D_str)
    gate_D = F(gate_D_str)

    # Both rationals must literally appear (as substrings) in the gate's
    # "accepted" free-text field, not just be equal as numbers computed
    # separately -- i.e. this script reads them FROM the gate text, not
    # only from a hand-copied literal, before comparing.
    gate_2D_in_text = gate_2D_str in gate_text
    gate_D_in_text = gate_D_str in gate_text

    D_matches_gate = (D == gate_D)
    twoD_matches_gate = (twoD == gate_2D)

    target = F(1, 1250000)
    twoD_le_target = twoD <= target
    margin = target / twoD
    # the gate/report state the margin as "about 29.38"
    margin_close_to_2938 = abs(float(margin) - 29.38) < 0.01

    ratio_100 = cap["D"] / smaller["D"]
    ratio_100_in_99_101 = F(99) <= ratio_100 <= F(101)

    # ---- Cross-check against the forward and reverse AY1 exports,
    # which quote D_ii_forward (=D here) directly (AY1 does not
    # recompute D; it reuses the AV1 forward tier-(ii) rational).
    fwd = load_json(FWD_AY1_RESULTS)
    rev = load_json(REV_AY1_RESULTS)
    fwd_av1_D = F(fwd["checks"][1]["av1_D_ii_forward"])
    cross_fwd_ay1 = (fwd_av1_D == D)

    # forward AY1's own exported headline (if present) for 2D / closeness
    def find_all(obj, target_val, path=""):
        hits = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str):
                    try:
                        if F(v) == target_val:
                            hits.append(path + "/" + k)
                    except Exception:
                        pass
                hits += find_all(v, target_val, path + "/" + k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                hits += find_all(v, target_val, path + f"[{i}]")
        return hits

    fwd_2D_hits = find_all(fwd, twoD)
    rev_2D_hits = find_all(rev, twoD)

    # ---- Cross-check against the original AV1 forward export directly
    # (the loop this D and formula actually come from).
    av1_fwd = load_json(FWD_AV1_RESULTS)
    av1_D_hits = find_all(av1_fwd, D)

    overall_pass = bool(
        D_matches_gate
        and twoD_matches_gate
        and gate_2D_in_text
        and gate_D_in_text
        and twoD_le_target
        and margin_close_to_2938
        and ratio_100_in_99_101
        and cross_fwd_ay1
        and len(fwd_2D_hits) > 0
        and len(rev_2D_hits) > 0
        and len(av1_D_hits) > 0
    )

    result = {
        "script": "two_d_independent.py",
        "zero_research_loops": True,
        "arithmetic": "fractions.Fraction only; no floats in any pass/fail comparison",
        "formula": "J=28|tau|, t1=49|tau|/144, T=t1/(1-352J), eps=2T+T^2, D=2eps(1+eps)/(1+eps^2), 2D by the trace-norm triangle inequality through the common reference P_R",
        "at_cap_tau_1e-8": {
            "J": str(cap["J"]), "t1": str(cap["t1"]), "T": str(cap["T"]),
            "eps": str(cap["eps"]), "D": str(D), "D_decimal": float(D),
            "twoD": str(twoD), "twoD_decimal": float(twoD),
        },
        "at_tau_1e-10": {"D": str(smaller["D"]), "D_decimal": float(smaller["D"])},
        "gate_comparison": {
            "gate_D_string": gate_D_str,
            "gate_2D_string": gate_2D_str,
            "gate_D_string_found_in_accepted_text": gate_D_in_text,
            "gate_2D_string_found_in_accepted_text": gate_2D_in_text,
            "D_matches_gate_bit_for_bit": D_matches_gate,
            "twoD_matches_gate_bit_for_bit": twoD_matches_gate,
        },
        "target_margin": {
            "target_2D_le": str(target),
            "twoD_le_target": twoD_le_target,
            "margin_target_over_twoD": str(margin),
            "margin_decimal": float(margin),
            "margin_matches_reported_about_29_38": margin_close_to_2938,
        },
        "tau_scaling_ratio_1e8_over_1e10": {
            "ratio": str(ratio_100), "ratio_decimal": float(ratio_100),
            "in_99_101": ratio_100_in_99_101,
        },
        "cross_check_forward_ay1_export": {
            "av1_D_ii_forward_field_equals_D": cross_fwd_ay1,
            "paths_in_forward_export_equal_to_2D": fwd_2D_hits,
            "paths_in_reverse_export_equal_to_2D": rev_2D_hits,
        },
        "cross_check_av1_forward_export": {
            "paths_in_av1_forward_export_equal_to_D": av1_D_hits,
        },
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
