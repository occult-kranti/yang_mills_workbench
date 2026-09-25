#!/usr/bin/env python3
"""Arb enclosures of the BD2 electric-band endpoints, the 1x2-loop bound
K_2' tau^2, and the 2+1D constants G_3, G_3' and the admissible-coupling
cap, each checked to contain (or match) the frozen admitted rational.

Round33 sub-round 4, modern (Penrose/Feynman) lens, research assistant/coder
"assistant-4". **This script counts zero research loops. Nothing here is
evidence, a contract, a premise or a gate.** It never imports a producer
`check.py` (`research/round33/forward/bd2/check.py` is never opened,
imported or executed). It reads only, as text/JSON, never executed:
  - `research/round33/contracts/bd2.json` (frozen `parameters.electric_band`,
    `parameters.z3_1x2`, `parameters.dimension_2p1`);
  - `research/round33/forward/bd2/report.md` (closed-form formulas and the
    exact constants `L`, `K_2'`, quoted here for arithmetic recomputation,
    never executed) and `output/results.json` (ADMITTED exact rationals,
    read only for comparison);
  - `research/round33/advisor/bd2-gate.json` (gate headline, comparison);
  - `research/round32/advisor/ay1-gate.json` and `ay2-gate.json` (the
    provenance of `K_2'` and `L`, read only to quote the admitted
    constants -- their derivations are NOT re-run here; like
    `research/round33/experts/modern/assistant-3/bc2_arb.py`'s reuse of
    already-admitted route constants such as `G(R)=148/7`, this script
    treats `K_2'` and `L` as ALREADY-REVIEWED inputs and independently
    checks the ARITHMETIC that combines them into the four BD2 quantities
    named below, in Arb ball arithmetic -- a wholly different arithmetic
    engine from the producer's `fractions.Fraction`).
`python-flint` (`fmpq` exact rationals, `arb` ball arithmetic) is reused BY
IMPORT.

**Four quantities, independently enclosed:**
  1. The electric-band endpoints: lower = (3/2) L^2 (L the AY2 lower
     distance), upper = 98|tau|, at tau = 1e-8.
  2. The 1x2-loop bound: K_2' tau^2, at tau = 1e-8.
  3. The 2+1D constants at R=1/64: G_3(R) = 8 e^{6R}(1+8R) = 9 e^{3/32},
     G_3'(R) = 8 e^{6R}(14+48R) = 118 e^{3/32}.
  4. The admissible-coupling cap: the directed-lower-bound rational
     `1580747155173/10^15` for the true cap 1/(576 e^{3/32}) = R/G_3(R).

`e^{3/32}` is computed by `flint.arb`'s own built-in `exp()` at 300 bits,
independent of any Machin/Taylor bracket hand-written by a producer. Every
containment/ordering check below is a PROVABLE ball comparison (Arb's own
rigorous interval comparison operators), not a floating-point approximation.

Run: `python3 -B bd2_numbers.py`
"""
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]

import flint  # noqa: E402

PREC = 300
flint.ctx.prec = PREC


def load_json(rel):
    return json.loads((ROOT / rel).read_text())


def load_text(rel):
    return (ROOT / rel).read_text()


CONTRACT = load_json("research/round33/contracts/bd2.json")
FWD = load_json("research/round33/forward/bd2/output/results.json")
_ = load_text("research/round33/forward/bd2/report.md")  # read for the closed-form
# formulas quoted in this script's own docstring; not executed, not re-parsed
GATE = load_json("research/round33/advisor/bd2-gate.json")
AY1_GATE = load_json("research/round32/advisor/ay1-gate.json")

assert CONTRACT["id"] == "BD2"
assert GATE["accepted"]

TAU = Q(1, 10**8)


def arb_exact(q: Q) -> flint.arb:
    fq = flint.fmpq(q.numerator, q.denominator)
    return flint.arb(fq)


def frac(s: str) -> Q:
    return Q(s)


# ---------------------------------------------------------------------------
# Inputs quoted from the frozen forward report (never executed; the
# provenance of L and K_2' is the AY2/AY1 gates, quoted, not re-derived)
# ---------------------------------------------------------------------------
L = frac(
    "315493271189404369878663368737136921794795815043212654249128159"
    "/720528856978172107545458049318912000000000000000000000000000000000000000"
)
# (the report line wraps across the 500-line window read for this script;
#  L is checked below against the ADMITTED electric_band rows directly)

K2PRIME = frac(
    "966771578474926086618624139557778885954947547760216752246561"
    "/72052885697817210754545804931891200000000000000000000000"
)
assert str(K2PRIME) in AY1_GATE["accepted"]


# ---------------------------------------------------------------------------
# 1. Electric band
# ---------------------------------------------------------------------------
def electric_band():
    lower_exact = Q(3, 2) * L * L
    upper_exact = 98 * TAU

    admitted_row = FWD["electric_band"]["rows"][0]
    admitted_lower = frac(admitted_row["lower"])
    admitted_upper = frac(admitted_row["upper"])

    exact_match_lower = lower_exact == admitted_lower
    exact_match_upper = upper_exact == admitted_upper

    # Arb ball recomputation (independent arithmetic engine)
    L_ball = arb_exact(L)
    lower_ball = flint.arb(3) / flint.arb(2) * L_ball * L_ball
    upper_ball = flint.arb(98) * arb_exact(TAU)

    lower_contains = arb_exact(admitted_lower) in lower_ball
    upper_contains = arb_exact(admitted_upper) in upper_ball
    band_nondegenerate = lower_ball < upper_ball

    return {
        "L": str(L),
        "lower_formula": "(3/2) L^2",
        "lower_exact": str(lower_exact),
        "admitted_lower": str(admitted_lower),
        "exact_match_lower": exact_match_lower,
        "arb_lower_ball": str(lower_ball),
        "arb_lower_contains_admitted": bool(lower_contains),
        "upper_formula": "98 |tau|",
        "upper_exact": str(upper_exact),
        "admitted_upper": str(admitted_upper),
        "exact_match_upper": exact_match_upper,
        "arb_upper_ball": str(upper_ball),
        "arb_upper_contains_admitted": bool(upper_contains),
        "band_nondegenerate_lower_lt_upper_provable": bool(band_nondegenerate),
        "passed": exact_match_lower
        and exact_match_upper
        and lower_contains
        and upper_contains
        and band_nondegenerate,
    }


# ---------------------------------------------------------------------------
# 2. 1x2-loop bound K_2' tau^2
# ---------------------------------------------------------------------------
def loop_1x2_bound():
    bound_exact = K2PRIME * TAU * TAU
    admitted = frac(FWD["z3_1x2"]["bound_rows"][0]["bound"])
    exact_match = bound_exact == admitted

    bound_ball = arb_exact(K2PRIME) * arb_exact(TAU) * arb_exact(TAU)
    contains = arb_exact(admitted) in bound_ball

    formal = frac(FWD["z3_1x2"]["formal"]["value"])  # 7/124416
    formal_tau2 = formal * TAU * TAU
    bound_dominates_formal = bound_exact > abs(formal_tau2)

    return {
        "K_2_prime": str(K2PRIME),
        "tau": str(TAU),
        "bound_exact": str(bound_exact),
        "admitted": str(admitted),
        "exact_match": exact_match,
        "arb_ball": str(bound_ball),
        "arb_contains_admitted": bool(contains),
        "formal_second_order_term_at_tau": str(formal_tau2),
        "certified_bound_dominates_formal_term": bool(bound_dominates_formal),
        "passed": exact_match and contains and bound_dominates_formal,
    }


# ---------------------------------------------------------------------------
# 3-4. 2+1D constants: G_3(R), G_3'(R), and the admissible cap, at R=1/64
# ---------------------------------------------------------------------------
def dimension_2p1_constants():
    dim = FWD["dimension_2p1"]
    R = Q(1, 64)

    e_arg = arb_exact(Q(3, 32))
    e_val = e_arg.exp()  # flint's own exp(), independent of any hand bracket

    G3_ball = flint.arb(9) * e_val
    G3p_ball = flint.arb(118) * e_val
    cap_ball = 1 / (flint.arb(576) * e_val)

    G3_lo, G3_hi = frac(dim["G3_R"][0]), frac(dim["G3_R"][1])
    G3p_lo, G3p_hi = frac(dim["G3prime_R"][0]), frac(dim["G3prime_R"][1])
    cap_dir_lo = frac(dim["cap_directed_lower"])

    G3_ok_lo = arb_exact(G3_lo) < G3_ball
    G3_ok_hi = G3_ball < arb_exact(G3_hi)
    G3p_ok_lo = arb_exact(G3p_lo) < G3p_ball
    G3p_ok_hi = G3p_ball < arb_exact(G3p_hi)
    cap_ok = arb_exact(cap_dir_lo) < cap_ball  # a valid (safe) directed lower bound

    # self-map / exclusion conditions at the directed-lower cap, exact rational
    # arithmetic times an Arb ball for G3/G3' (rigorous, not merely numeric)
    selfmap_holds = arb_exact(cap_dir_lo) * G3_ball <= arb_exact(R)
    exclusion_holds = 2 * arb_exact(cap_dir_lo) * G3p_ball < flint.arb(1)

    # also recompute G_3, G_3' from their own closed forms in the contract,
    # 8 e^{6t}(1+8t) and 8 e^{6t}(14+48t) at t=1/64, as an internal identity
    # check independent of the "9 e^{3/32}" / "118 e^{3/32}" simplification
    t = arb_exact(R)
    e6t = (flint.arb(6) * t).exp()
    G3_alt = flint.arb(8) * e6t * (1 + flint.arb(8) * t)
    G3p_alt = flint.arb(8) * e6t * (14 + flint.arb(48) * t)
    alt_matches_G3 = (G3_alt - G3_ball).contains(flint.arb(0))
    alt_matches_G3p = (G3p_alt - G3p_ball).contains(flint.arb(0))

    return {
        "R": str(R),
        "e_3_32_ball": str(e_val),
        "G3_ball_9_e_3_32": str(G3_ball),
        "G3_admitted_bracket": [str(G3_lo), str(G3_hi)],
        "G3_bracket_contains_ball_lo": bool(G3_ok_lo),
        "G3_bracket_contains_ball_hi": bool(G3_ok_hi),
        "G3p_ball_118_e_3_32": str(G3p_ball),
        "G3p_admitted_bracket": [str(G3p_lo), str(G3p_hi)],
        "G3p_bracket_contains_ball_lo": bool(G3p_ok_lo),
        "G3p_bracket_contains_ball_hi": bool(G3p_ok_hi),
        "cap_ball_1_over_576_e_3_32": str(cap_ball),
        "cap_directed_lower_admitted": str(cap_dir_lo),
        "cap_directed_lower_is_valid_lower_bound": bool(cap_ok),
        "selfmap_condition_tau_G3_leq_R_at_cap_directed_lower": bool(selfmap_holds),
        "exclusion_condition_2_tau_G3p_lt_1_at_cap_directed_lower": bool(exclusion_holds),
        "closed_form_8e6t_1p8t_matches_9e_3_32": bool(alt_matches_G3),
        "closed_form_8e6t_14p48t_matches_118e_3_32": bool(alt_matches_G3p),
        "passed": G3_ok_lo
        and G3_ok_hi
        and G3p_ok_lo
        and G3p_ok_hi
        and cap_ok
        and selfmap_holds
        and exclusion_holds
        and alt_matches_G3
        and alt_matches_G3p,
    }


def main():
    report = {
        "schema": "hnm-round33-modern-lens-assistant4-bd2-numbers-v1",
        "status": "preview_and_crosscheck_only_zero_research_loops_not_a_contract_or_gate",
        "human_author": "Hruday N M (BUNZEEY)",
        "role": "modern (Penrose/Feynman) lens, research assistant/coder assistant-4",
        "round": 33,
        "subround": 4,
        "precision_bits": PREC,
    }

    eb = electric_band()
    lb = loop_1x2_bound()
    dc = dimension_2p1_constants()

    report["electric_band"] = eb
    report["loop_1x2_bound"] = lb
    report["dimension_2p1_constants"] = dc
    report["all_passed"] = eb["passed"] and lb["passed"] and dc["passed"]

    print(json.dumps(report, indent=1, default=str))
    sys.exit(0 if report["all_passed"] else 1)


if __name__ == "__main__":
    main()
