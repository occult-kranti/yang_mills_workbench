#!/usr/bin/env python3
"""
T4 -- sign_margin_replay.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 2.

Zero research loops: test/planning script, not a producer, skeptic or
advisor artifact. Reads only frozen JSON data (research/round32/forward/
aw2/output/results.json, research/round32/contracts/aw2.json) -- never
any producer's check.py.

Task (update-1.md section 5, test 4): independently recompute, as exact
rationals, the AW2 enclosure endpoints

    [ tau/144 - K_2^+ tau^2 ,  tau/144 + K_2^+ tau^2 ]     at tau = +-10^-8,

the exclusion margin

    m = (|tau|/144 - K_2^+ tau^2) / (K_2^+ tau^2),

and the sign margin

    s = 1 / (144 K_2^+ |tau|),

using the gate-bound K_2^+ = 81108864767825329926713064490531229475390625
/24176936535511801466930759024724079017984 (research/round32/advisor/
aw1-gate.json, research/round32/contracts/aw2.json).

Pass iff every one of these equals the AW2 forward producer's exported
rational bit-for-bit, and both margins exceed 2 (the contract's
"accepted_within_scope" threshold, research/round32/contracts/aw2.json
acceptance.accepted_within_scope: "0 strictly excluded with margin >=2").

Arithmetic: fractions.Fraction only; no floats in any comparison.
Run with: python3 -B sign_margin_replay.py
"""
import json
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FWD_AW2_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/aw2/output/results.json")
AW2_CONTRACT = os.path.join(REPO_ROOT, "research/round32/contracts/aw2.json")

THRESHOLD = F(2)


def extract_fraction(text):
    m = re.search(r"(\d{5,}\s*/\s*\d{5,})", text)
    if not m:
        return None
    num, den = m.group(1).split("/")
    return F(int(num.strip()), int(den.strip()))


def load_K2_plus():
    with open(AW2_CONTRACT) as fh:
        contract = json.load(fh)
    field = contract["parameters"]["K_2_plus"]
    return extract_fraction(field.split(" (")[0])


def enclosure(tau, K2_plus):
    first_order = tau / 144
    radius = K2_plus * tau ** 2
    lower = first_order - radius
    upper = first_order + radius
    a = abs(tau)
    exclusion_margin = (a / 144 - K2_plus * tau ** 2) / (K2_plus * tau ** 2)
    sign_margin = 1 / (144 * K2_plus * a)
    return {
        "tau": tau, "first_order": first_order, "radius": radius,
        "lower": lower, "upper": upper,
        "exclusion_margin": exclusion_margin, "sign_margin": sign_margin,
        "excludes_zero_strictly": (lower > 0) if tau > 0 else (upper < 0),
    }


def main():
    K2_plus = load_K2_plus()
    tau_plus = F(1, 10 ** 8)
    tau_minus = -tau_plus

    plus = enclosure(tau_plus, K2_plus)
    minus = enclosure(tau_minus, K2_plus)

    # cross-check margins are sign-independent (same magnitude both signs)
    margins_sign_independent = (
        plus["exclusion_margin"] == minus["exclusion_margin"]
        and plus["sign_margin"] == minus["sign_margin"]
    )

    exceed_threshold = bool(
        plus["exclusion_margin"] > THRESHOLD
        and plus["sign_margin"] > THRESHOLD
        and minus["exclusion_margin"] > THRESHOLD
        and minus["sign_margin"] > THRESHOLD
    )

    excludes_zero = bool(plus["excludes_zero_strictly"] and minus["excludes_zero_strictly"])

    read_ok = True
    match = {}
    try:
        with open(FWD_AW2_RESULTS) as fh:
            fwd = json.load(fh)
        h = fwd["headline"]
        exp_plus_lower = F(h["enclosure_plus"]["lower"])
        exp_plus_upper = F(h["enclosure_plus"]["upper"])
        exp_minus_lower = F(h["enclosure_minus"]["lower"])
        exp_minus_upper = F(h["enclosure_minus"]["upper"])
        exp_excl = F(h["exclusion_margin"])
        exp_sign = F(h["sign_margin"])

        match = {
            "enclosure_plus_lower": (plus["lower"] == exp_plus_lower),
            "enclosure_plus_upper": (plus["upper"] == exp_plus_upper),
            "enclosure_minus_lower": (minus["lower"] == exp_minus_lower),
            "enclosure_minus_upper": (minus["upper"] == exp_minus_upper),
            "exclusion_margin": (plus["exclusion_margin"] == exp_excl),
            "sign_margin": (plus["sign_margin"] == exp_sign),
        }
    except Exception as exc:
        read_ok = False
        match = {"read_error": str(exc)}

    exported_match_ok = read_ok and all(v is True for v in match.values())

    overall_pass = bool(
        exported_match_ok
        and margins_sign_independent
        and exceed_threshold
        and excludes_zero
    )

    def s(x):
        return str(x) if isinstance(x, F) else x

    result = {
        "script": "sign_margin_replay.py",
        "zero_research_loops": True,
        "arithmetic": "fractions.Fraction only; no floats in any comparison",
        "K2_plus": s(K2_plus),
        "tau_plus": s(tau_plus),
        "tau_minus": s(tau_minus),
        "enclosure_plus": {
            "lower": s(plus["lower"]), "upper": s(plus["upper"]),
            "lower_preview": float(plus["lower"]), "upper_preview": float(plus["upper"]),
        },
        "enclosure_minus": {
            "lower": s(minus["lower"]), "upper": s(minus["upper"]),
            "lower_preview": float(minus["lower"]), "upper_preview": float(minus["upper"]),
        },
        "exclusion_margin": s(plus["exclusion_margin"]),
        "exclusion_margin_preview": float(plus["exclusion_margin"]),
        "sign_margin": s(plus["sign_margin"]),
        "sign_margin_preview": float(plus["sign_margin"]),
        "margins_sign_independent": margins_sign_independent,
        "both_margins_exceed_2": exceed_threshold,
        "excludes_zero_at_both_signs": excludes_zero,
        "matches_exported_aw2_producer_bit_for_bit": match,
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
