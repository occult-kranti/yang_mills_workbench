#!/usr/bin/env python3
"""
T2 -- k2_reassembly.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 2.

Zero research loops: test/planning script, not a producer, skeptic or
advisor artifact. Reads only the FROZEN output JSON of the AW1 forward
and reverse producers and the skeptic's own exported JSON (data, not
code; nothing here imports or reads forward/aw1/check.py,
reverse/aw1/check.py or skeptic/aw1_check.py).

Task (update-1.md section 5, test 2): independently reassemble the
exact-tier K_2 terms named in research/round32/forward/aw1/report.md
section 5.2/5.3 and research/round32/skeptic/aw1.md's re-derivation
table, as exact Fractions, at tau=10^-8:

    J          = 28|tau|                      (four incoming stars, 7|tau| each)
    t_1        = 49|tau|/144                   (49 faces per factor, |tau|/144 each)
    T          = t_1 / (1 - 352 J)             (self-consistent AM2 anchored norm)
    am2_remainder (rho) = 352 J T
    straddling          = T (6a + rho)                 a := |tau|/144
    two_creation        = (33a + rho)^2
    eps_F (AV1/forward)     = 2T + T^2
    eps_R (reverse, 82-face refinement) = 82a + 2*rho + (33a+rho)^2
    eps_min             = min(eps_F, eps_R)            (skeptic's accepted density bound)
    density             = eps_min^2
    normalization_order = a * eps_min^2                (3rd order; overlap_multiplier = 1
                                                          already folded into am2_remainder/
                                                          straddling/two_creation above)

    K_2_min = am2_remainder + straddling + two_creation + density + normalization_order

Compared against:
  - forward's exported headline.K2_exact_plus  (research/round32/forward/aw1/output/results.json)
  - reverse's exported k2_exact_tier_itemized_uniform.exact_tier.K2_exact_rational
    (research/round32/reverse/aw1/output/results.json)
  - the skeptic's admitted (= gate-bound) K_2^+ and its own exported
    "minimal accepted" value (research/round32/skeptic/aw1.json)
  - the literal gate-bound K_2^+ named in the task itself
    (research/round32/advisor/aw1-gate.json), which equals the skeptic's
    admitted value and the forward's labelled "unpinned_t_bounds" variant.

Pass iff:
  (i)  the am2_remainder term computed here from 352*J*T equals the
       common value exported identically by the forward, reverse and
       skeptic producers (3773/11248891200000000 at tau=10^-8);
  (ii) every exported K_2 (forward, reverse, skeptic/gate) is >= the
       sum of this script's minimal terms (K_2_min), i.e. K_2_min is a
       valid, and the tightest disclosed, exact-tier upper bound.

Arithmetic: fractions.Fraction only; no floats in any comparison
(decimal previews are reported for readability only).
Run with: python3 -B k2_reassembly.py
"""
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FWD_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/aw1/output/results.json")
REV_RESULTS = os.path.join(REPO_ROOT, "research/round32/reverse/aw1/output/results.json")
SKEPTIC_JSON = os.path.join(REPO_ROOT, "research/round32/skeptic/aw1.json")
SKEPTIC_INDEP = os.path.join(REPO_ROOT, "research/round32/skeptic/aw1-independent/results.json")

# The gate-bound K_2^+, named verbatim in the assignment and in
# research/round32/advisor/aw1-gate.json's "accepted" field / "decision"
# field, and in research/round32/contracts/aw2.json's frozen parameter.
GATE_K2_PLUS = F(
    81108864767825329926713064490531229475390625,
    24176936535511801466930759024724079017984,
)

TAU = F(1, 10 ** 8)


def reassemble(tau):
    a = tau / 144
    J = 28 * tau
    t1 = F(49, 144) * tau
    T = t1 / (1 - 352 * J)
    rho = 352 * J * T  # am2_remainder, self-consistent AM2 anchored-norm remainder

    straddling = T * (6 * a + rho)
    two_creation = (33 * a + rho) ** 2

    eps_F = 2 * T + T ** 2
    eps_R = 82 * a + 2 * rho + (33 * a + rho) ** 2
    eps_min = eps_F if eps_F <= eps_R else eps_R

    density = eps_min ** 2
    normalization_order = a * eps_min ** 2

    k2_raw = rho + straddling + two_creation + density + normalization_order
    return {
        "a": a, "J": J, "t1": t1, "T": T, "rho": rho,
        "straddling": straddling, "two_creation": two_creation,
        "eps_F": eps_F, "eps_R": eps_R, "eps_min": eps_min,
        "density": density, "normalization_order": normalization_order,
        "k2_raw_at_tau": k2_raw, "k2_coefficient": k2_raw / tau ** 2,
    }


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def main():
    terms = reassemble(TAU)
    rho = terms["rho"]
    k2_min_coeff = terms["k2_coefficient"]

    read_ok = True
    exported = {}
    try:
        fwd = load_json(FWD_RESULTS)
        exported["forward_am2_remainder"] = F(
            next(c for c in fwd["checks"] if c.get("id") == "k2_exact_tier")["record"]["terms"]["am2_remainder"]["value"]
        )
        exported["forward_K2_exact_plus"] = F(fwd["headline"]["K2_exact_plus"])
    except Exception as exc:
        read_ok = False
        exported["forward_error"] = str(exc)

    try:
        rev = load_json(REV_RESULTS)
        rev_k2 = next(c for c in rev["checks"] if c.get("id") == "k2_exact_tier_itemized_uniform")
        exported["reverse_am2_remainder"] = F(rev_k2["exact_tier"]["terms"]["am2_remainder"]["value"])
        exported["reverse_K2_exact_rational"] = F(rev_k2["exact_tier"]["K2_exact_rational"])
    except Exception as exc:
        read_ok = False
        exported["reverse_error"] = str(exc)

    try:
        skep = load_json(SKEPTIC_JSON)
        av = skep["admitted_values"]
        exported["skeptic_K2_exact_tier_bound"] = F(av["K2_exact_tier_bound"])
        exported["skeptic_K2_exact_tier_forward_echo"] = F(av["K2_exact_tier_forward"])
        exported["skeptic_K2_exact_tier_reverse_echo"] = F(av["K2_exact_tier_reverse"])
        exported["skeptic_K2_exact_tier_minimal_accepted"] = F(av["K2_exact_tier_minimal_accepted"])
    except Exception as exc:
        read_ok = False
        exported["skeptic_error"] = str(exc)

    try:
        skep_indep = load_json(SKEPTIC_INDEP)
        exported["skeptic_independent_am2_remainder"] = F(
            skep_indep["K2"]["exact"]["terms"]["am2_remainder"]["value"]
        )
    except Exception as exc:
        read_ok = False
        exported["skeptic_indep_error"] = str(exc)

    # (i) the common am2_remainder = 352 J T value
    common_am2_candidates = [
        v for k, v in exported.items()
        if k.endswith("am2_remainder") and isinstance(v, F)
    ]
    am2_common_ok = bool(common_am2_candidates) and all(v == rho for v in common_am2_candidates)

    # (ii) every exported K_2 (forward, reverse, skeptic/gate) is >= our minimal sum
    exported_k2_values = {
        "forward_K2_exact_plus": exported.get("forward_K2_exact_plus"),
        "reverse_K2_exact_rational": exported.get("reverse_K2_exact_rational"),
        "skeptic_K2_exact_tier_bound": exported.get("skeptic_K2_exact_tier_bound"),
        "gate_bound_literal": GATE_K2_PLUS,
    }
    domination = {}
    domination_ok = True
    for name, val in exported_k2_values.items():
        if val is None:
            domination_ok = False
            domination[name] = "MISSING (read failure)"
            continue
        ok = (val >= k2_min_coeff)
        domination_ok = domination_ok and ok
        domination[name] = {"value_preview": float(val), "dominates_minimal": ok}

    # Extra cross-check: the skeptic's own exported "minimal accepted"
    # value should equal our K_2_min coefficient bit-for-bit.
    skeptic_minimal_echo = exported.get("skeptic_K2_exact_tier_minimal_accepted")
    minimal_matches_skeptic = (skeptic_minimal_echo == k2_min_coeff) if skeptic_minimal_echo is not None else False

    # Gate value equals skeptic's admitted bound bit-for-bit (sanity: the
    # task's literal number and the live gate file must agree).
    gate_equals_skeptic_admitted = (
        exported.get("skeptic_K2_exact_tier_bound") == GATE_K2_PLUS
        if "skeptic_K2_exact_tier_bound" in exported else False
    )

    overall_pass = bool(read_ok and am2_common_ok and domination_ok)

    def sstr(x):
        return str(x) if isinstance(x, F) else x

    result = {
        "script": "k2_reassembly.py",
        "zero_research_loops": True,
        "arithmetic": "fractions.Fraction only; decimal previews for readability only",
        "tau": str(TAU),
        "reassembled_terms": {
            "J": sstr(terms["J"]), "t1": sstr(terms["t1"]), "T": sstr(terms["T"]),
            "am2_remainder_352JT": sstr(rho),
            "straddling_T_6a_plus_rho": sstr(terms["straddling"]),
            "two_creation_33a_plus_rho_sq": sstr(terms["two_creation"]),
            "eps_F_2T_plus_Tsq": sstr(terms["eps_F"]),
            "eps_R_82a_plus_2rho_plus_two_creation": sstr(terms["eps_R"]),
            "eps_min": sstr(terms["eps_min"]),
            "density_eps_min_sq": sstr(terms["density"]),
            "normalization_order_a_eps_min_sq": sstr(terms["normalization_order"]),
            "overlap_multiplier": "1 (already folded into am2_remainder/straddling/two_creation, per AV1 F12: 2||W Omega_R||=1)",
            "K2_min_raw_at_tau": sstr(terms["k2_raw_at_tau"]),
            "K2_min_coefficient": sstr(k2_min_coeff),
            "K2_min_coefficient_preview": float(k2_min_coeff),
        },
        "reads_ok": read_ok,
        "exported_am2_remainder_terms": {k: sstr(v) for k, v in exported.items() if k.endswith("am2_remainder") and isinstance(v, F)},
        "am2_remainder_common_value_confirmed": am2_common_ok,
        "exported_K2_dominates_minimal": domination,
        "domination_ok": domination_ok,
        "skeptic_minimal_accepted_echo_matches_bit_for_bit": minimal_matches_skeptic,
        "gate_literal_equals_skeptic_admitted_bit_for_bit": gate_equals_skeptic_admitted,
        "ordering_note": "skeptic/gate >= forward >= reverse >= K2_min, matching skeptic/aw1.md's own stated ordering",
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
