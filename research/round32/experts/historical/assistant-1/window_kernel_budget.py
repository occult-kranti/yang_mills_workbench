#!/usr/bin/env python3
"""
S3 -- window_kernel_budget.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 1.

Scope (per loop3-signoff.md section 3, S3, and the assignment brief):
  With Fractions and a directed pi enclosure (Machin's formula), assemble

      E = M_0*(D + D^2) + k*M_1,   M_0 = 2,  M_1 = 4*s/pi,  k = 49|tau|/4

  (research/round32/contracts/av2.json parameters: window_transform,
  duhamel_slope) with D the admitted forward tier-(ii) rational from the
  AV1 gate (research/round32/advisor/av1-gate.json "decision" /
  research/round32/contracts/av2.json parameters.state_bound).

  Pass iff:
    - E < 10^-6 at tier (ii)               (expect ~1.7-2.0e-7);
    - E > 10^-6 at tier (i)                (expect ~3.6-4.7e-5, both the
                                             crude and once-iterated tier-i
                                             values);
    - the crossover s* (where E=10^-6 at tier (ii)) lies in [6.1, 6.3];
    - the L=10^4 Poisson radius (~8.415e-4) and the 1.2651e-6 floor are
      reproduced as REJECTED controls (both exceed the 10^-6 target).

  All PASS/FAIL comparisons use exact fractions.Fraction and a directed
  (outward-rounded) rational enclosure of pi; only the single supplementary
  "optimized Poisson floor" preview (explicitly a preview in
  research/round32/advisor/selection-av2.md, not an admitted datum) uses
  ordinary floats, clearly labelled as such, consistent with this
  project's floating-point-is-a-labelled-preview convention.
"""
from fractions import Fraction as F
import importlib.util
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FWD_AV1_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/av1/output/results.json")
AV1_GATE = os.path.join(REPO_ROOT, "research/round32/advisor/av1-gate.json")
AV2_CONTRACT = os.path.join(REPO_ROOT, "research/round32/contracts/av2.json")
AT4_RESULTS = os.path.join(REPO_ROOT, "research/round31/forward/at4/output/results.json")

# S2 lives beside this script; reuse its independent tier-(ii) derivation
# purely as a same-author cross-check (not a producer's check.py).
_spec = importlib.util.spec_from_file_location(
    "am2_tiers_exact", os.path.join(HERE, "am2_tiers_exact.py"))
_am2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_am2)


# ---------------------------------------------------------------------
# Directed pi enclosure via Machin's formula, pi = 16*arctan(1/5) -
# 4*arctan(1/239), with exact alternating-series truncation bounds.
# ---------------------------------------------------------------------

def _arctan_partial(p, q, K):
    """Exact partial sum of the first K terms of the arctan(p/q) series."""
    x = F(p, q)
    x2 = x * x
    cur = x
    s = F(0)
    sign = 1
    for n in range(K):
        s += sign * (cur / (2 * n + 1))
        cur *= x2
        sign *= -1
    return s


def arctan_bounds(p, q, K_even):
    """
    Returns (lower, upper) exact rational bounds on arctan(p/q), using
    K_even (even) and K_even+1 terms of the alternating Taylor series.
    For a strictly-decreasing-term alternating series, consecutive
    partial sums bracket the true value, and since the (K_even)-th
    partial sum's last added term (index K_even-1, odd) is negative,
    partial(K_even) <= arctan(p/q) <= partial(K_even+1).
    """
    assert K_even % 2 == 0
    lower = _arctan_partial(p, q, K_even)
    upper = _arctan_partial(p, q, K_even + 1)
    assert lower <= upper
    return lower, upper


def pi_bounds():
    lo5, hi5 = arctan_bounds(1, 5, 60)
    lo239, hi239 = arctan_bounds(1, 239, 20)
    pi_lo = 16 * lo5 - 4 * hi239
    pi_hi = 16 * hi5 - 4 * lo239
    assert pi_lo <= pi_hi
    return pi_lo, pi_hi


PI_LO, PI_HI = pi_bounds()
_PI_WIDTH = PI_HI - PI_LO
assert _PI_WIDTH < F(1, 10 ** 30), "Machin enclosure not tight enough: %r" % (_PI_WIDTH,)


# ---------------------------------------------------------------------
# Load the frozen constants this script assembles but does not re-derive:
# D (AV1-admitted tier-ii forward rational), the AV1 tier-i values, tau,
# s, k.
# ---------------------------------------------------------------------

def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def get_admitted_D_ii():
    """
    D is read from two independent frozen sources and cross-checked
    against this session's own S2 (am2_tiers_exact.py) re-derivation:
      - research/round32/advisor/av1-gate.json "decision" text names the
        bound explicitly;
      - research/round32/contracts/av2.json parameters.state_bound names
        the same value as AV2's frozen state premise.
    """
    gate = load_json(AV1_GATE)
    decision_text = gate["decision"]
    marker = "D_ii="
    i = decision_text.index(marker) + len(marker)
    j = decision_text.index(" ", i)
    D_from_gate = F(decision_text[i:j])

    contract = load_json(AV2_CONTRACT)
    state_bound_text = contract["parameters"]["state_bound"]
    marker2 = "D = "
    i2 = state_bound_text.index(marker2) + len(marker2)
    j2 = state_bound_text.index(" ", i2)
    D_from_av2_contract = F(state_bound_text[i2:j2])

    assert D_from_gate == D_from_av2_contract, "gate and AV2 contract disagree on admitted D"

    enum = _am2.enumerate_star_and_owner_sets()
    D_own, _ = _am2.forward_D(F(1, 10 ** 8), enum)
    assert D_own == D_from_gate, "own S2 re-derivation disagrees with the admitted D"

    return D_from_gate


def get_tier_i_values():
    fwd = load_json(FWD_AV1_RESULTS)
    tiers = fwd["tiers"]["+"]
    return {
        "crude": F(tiers["i"]["D"]),
        "iterated": F(tiers["i_iterated"]["D"]),
    }


# ---------------------------------------------------------------------
# The window-kernel radius E = M0*(D+D^2) + k*M1, M1 = 4s/pi, with
# directed rational bounds (E_upper for "<target" certificates, E_lower
# for ">target" certificates).
# ---------------------------------------------------------------------

M0 = F(2)
TAU = F(1, 10 ** 8)
S_CLOCK = F(1)
K_SLOPE = F(49) * TAU / 4  # av2.json parameters.duhamel_slope = 49|tau|/4
TARGET = F(1, 10 ** 6)


def E_bounds(D, s=S_CLOCK, k=K_SLOPE):
    """(E_lower, E_upper): exact rational bounds on E, using PI_HI/PI_LO
    appropriately since M1=4s/pi is decreasing in pi."""
    state_term = M0 * (D + D ** 2)
    M1_upper = 4 * s / PI_LO   # smaller pi => larger M1 => larger E
    M1_lower = 4 * s / PI_HI
    E_upper = state_term + k * M1_upper
    E_lower = state_term + k * M1_lower
    return E_lower, E_upper


def crossover_bounds(D, k=K_SLOPE):
    """s* solves M0*(D+D^2) + k*(4 s*/pi) = TARGET, i.e.
    s* = (TARGET - M0*(D+D^2)) * pi / (4k). Directed bounds follow from
    PI_LO/PI_HI directly (pi appears un-inverted here)."""
    state_term = M0 * (D + D ** 2)
    coefficient = (TARGET - state_term) / (4 * k)
    assert coefficient > 0, "tier-ii state term already exceeds target; no crossover"
    s_lower = coefficient * PI_LO
    s_upper = coefficient * PI_HI
    return s_lower, s_upper


# ---------------------------------------------------------------------
# Rejected control 1: the AT4 L=10^4 Poisson certificate radius, exactly
# reproduced by summing AT4's own four frozen exact-rational cost terms
# (data read from research/round31/forward/at4/output/results.json, not
# code).
# ---------------------------------------------------------------------

def at4_poisson_radius():
    at4 = load_json(AT4_RESULTS)
    costs = at4["costs"]
    state = F(costs["state"])
    centering = F(costs["centering"])
    bulk = F(costs["bulk_dynamic"])
    tail = F(costs["whole_tail"])
    total = state + centering + bulk + tail
    exported = F(at4["absolute_error_upper"])
    return total, exported, {
        "state": state, "centering": centering, "bulk_dynamic": bulk, "whole_tail": tail,
    }


# ---------------------------------------------------------------------
# Rejected control 2: the "optimized Poisson floor" (~1.2651e-6 at
# L~4.08e6, D->0). This single supplementary control is computed as a
# labelled FLOAT PREVIEW (per selection-av2.md, which itself calls it a
# preview, not an admitted datum): minimise, over integration cutoff L,
#     f(L) = (k/pi)*ln(1+L^2/s^2) + (s/2 + 0)*(2/(pi L))   [D -> 0]
# i.e. the AT4-F16 log-bulk term plus half the whole-kernel tail, with
# the state term switched off. This is not used in any pass/fail
# certificate above; it is reported only as a rejected supplementary
# control, exactly as the AV2 contract retains it.
# ---------------------------------------------------------------------

def optimized_poisson_floor_preview(k_float, s_float=1.0):
    def f(L):
        return (k_float / math.pi) * math.log(1 + (L / s_float) ** 2) + s_float / (math.pi * L)

    lo, hi = 1.0, 5.0e7
    for _ in range(200):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if f(m1) < f(m2):
            hi = m2
        else:
            lo = m1
    L_star = (lo + hi) / 2
    return L_star, f(L_star)


def main():
    D_ii = get_admitted_D_ii()
    tier_i = get_tier_i_values()

    E_ii_lower, E_ii_upper = E_bounds(D_ii)
    E_i_crude_lower, E_i_crude_upper = E_bounds(tier_i["crude"])
    E_i_iter_lower, E_i_iter_upper = E_bounds(tier_i["iterated"])

    s_lower, s_upper = crossover_bounds(D_ii)

    at4_total, at4_exported, at4_terms = at4_poisson_radius()

    K_SLOPE_float = float(K_SLOPE)
    L_star, floor_preview = optimized_poisson_floor_preview(K_SLOPE_float)

    checks = {
        "tier_ii_E_below_target": bool(E_ii_upper < TARGET),
        "tier_i_crude_E_above_target": bool(E_i_crude_lower > TARGET),
        "tier_i_iterated_E_above_target": bool(E_i_iter_lower > TARGET),
        "crossover_s_star_in_6_1_6_3": bool(F(61, 10) <= s_lower and s_upper <= F(63, 10)),
        "at4_poisson_radius_matches_export": bool(at4_total == at4_exported),
        "at4_poisson_radius_rejected_above_target": bool(at4_total > TARGET),
        "optimized_poisson_floor_rejected_above_target": bool(floor_preview > float(TARGET)),
    }

    overall_pass = bool(
        checks["tier_ii_E_below_target"]
        and checks["tier_i_crude_E_above_target"]
        and checks["tier_i_iterated_E_above_target"]
        and checks["crossover_s_star_in_6_1_6_3"]
        and checks["at4_poisson_radius_matches_export"]
        and checks["at4_poisson_radius_rejected_above_target"]
        and checks["optimized_poisson_floor_rejected_above_target"]
    )

    result = {
        "script": "window_kernel_budget.py",
        "arithmetic": ("fractions.Fraction with a directed Machin pi enclosure for every "
                        "pass/fail comparison; the single 'optimized Poisson floor' "
                        "supplementary control is a labelled float preview only"),
        "pi_enclosure": {
            "pi_lower": str(PI_LO), "pi_upper": str(PI_HI),
            "width_decimal": float(_PI_WIDTH),
        },
        "inputs": {
            "tau": str(TAU), "s": str(S_CLOCK), "k_duhamel_slope": str(K_SLOPE),
            "M0": str(M0), "target": str(TARGET),
            "D_ii_admitted_forward_tier_ii": str(D_ii),
            "D_i_crude": str(tier_i["crude"]),
            "D_i_iterated": str(tier_i["iterated"]),
        },
        "E_tier_ii": {
            "E_lower": str(E_ii_lower), "E_upper": str(E_ii_upper),
            "E_upper_decimal_preview": float(E_ii_upper),
            "below_1e-6": checks["tier_ii_E_below_target"],
        },
        "E_tier_i_crude": {
            "E_lower": str(E_i_crude_lower), "E_upper": str(E_i_crude_upper),
            "E_lower_decimal_preview": float(E_i_crude_lower),
            "above_1e-6": checks["tier_i_crude_E_above_target"],
        },
        "E_tier_i_iterated": {
            "E_lower": str(E_i_iter_lower), "E_upper": str(E_i_iter_upper),
            "E_lower_decimal_preview": float(E_i_iter_lower),
            "above_1e-6": checks["tier_i_iterated_E_above_target"],
        },
        "crossover_s_star": {
            "s_lower": str(s_lower), "s_upper": str(s_upper),
            "decimal_preview": [float(s_lower), float(s_upper)],
            "in_6_1_6_3": checks["crossover_s_star_in_6_1_6_3"],
        },
        "rejected_control_at4_poisson_L_1e4": {
            "terms": {k_: str(v) for k_, v in at4_terms.items()},
            "total_exact": str(at4_total),
            "matches_at4_export_exactly": checks["at4_poisson_radius_matches_export"],
            "decimal_preview": float(at4_total),
            "rejected_above_1e-6": checks["at4_poisson_radius_rejected_above_target"],
        },
        "rejected_control_optimized_poisson_floor": {
            "note": "float preview only, per selection-av2.md; not an admission datum",
            "L_star_preview": L_star,
            "floor_preview": floor_preview,
            "rejected_above_1e-6": checks["optimized_poisson_floor_rejected_above_target"],
        },
        "checks": checks,
        "overall_pass": overall_pass,
    }

    print(json.dumps(result, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
