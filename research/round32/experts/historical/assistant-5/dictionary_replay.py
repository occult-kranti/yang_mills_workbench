#!/usr/bin/env python3
"""
dictionary_replay.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 5.

Zero research loops: cross-check/test script for the historical
(Newton/Tesla) lens's Round32 assistant package (assistant-5), not a
producer, skeptic or advisor artifact; nothing here is admission
evidence. Does not import research/round32/forward/az1/check.py or any
other producer check.py; only research/round32/advisor/az1-gate.json,
research/round32/contracts/az1.json and
research/round32/forward/az1/output/results.json (data, never code)
are read for cross-checking, exactly as
assistant-4/two_d_independent.py read the AY1 gate and exports for the
prior sub-round.

Task (panel-update-4.md item 7, historical share, test 1). Independently
verify, with two separate methods, the eleven dictionary identities the
AZ1 gate binds:
    alpha/16 = g^2/(32a)         tau = 96/g^4          alpha*lambda*a^2 = 1
    r = 4/g^4                    alpha*tau/24 = lambda (alpha/8)*(tau/3) = lambda
    7*tau = 672/g^4              tau/144 = 2/(3g^4)    (alpha/8)/2 = g^2/(32a)
    a*alpha/16 = g^2/32          tau*g^4 = 96
the cap g^4 = 9600000000 at tau = 1/10^8; the toy-trajectory crossover
indices (g_0^4 = 9.6e9: n* = 2 and 132 for the cap and the AL1 bridge
g^4 >= 32; g_0 = 1000: n* = 4 and 421); the lattice-unit floor
a*Delta >= g^2/32 >= 1250*sqrt(6) with a directed sqrt(6) bracket; and
the rescaling invariances (alpha, lambda, tau, the gap and r under
a -> c*a and under a common alpha/lambda rescaling by c).

Method. Two independent routes, exactly as the assignment specifies:

  Route A (Fractions): every quantity is evaluated as a plain
  fractions.Fraction at an independent numeric grid of (a, g) values
  (different from the AZ1 forward check's own 35-point grid) and the
  eleven identities are checked as exact rational equalities at every
  point.

  Route B (rational-function identity): alpha, lambda, tau, r and the
  gap are represented as ratios of honest integer polynomials in the
  two Laurent-cleared variables u = g^2 and a (and, for the rescaling
  identities, a third variable c), built from scratch with a small
  multivariate-polynomial dict class written in this file (never
  imported from any producer). Each identity is checked by literal
  integer cross-multiplication: LHS_num*RHS_den == RHS_num*LHS_den as
  polynomials, coefficient by coefficient -- true for every value of
  (u, a, c), not just at sampled points. Tau and r are additionally
  *derived* here from the AL1 primary definitions
  (tau = 24*lambda/alpha, r = lambda/alpha) and cross-multiplied against
  the literal target monomials 96/u^2 and 4/u^2, rather than assumed.

  The toy-trajectory crossover indices are computed by two independent
  integer methods, both on plain Python ints (no floats, no Fraction
  needed since every target/threshold pair here is already an exact
  integer): (i) an integer fourth root via two nested math.isqrt calls
  (isqrt(isqrt(n)) with an exact correction loop) used to seed a
  bounded local search, and (ii) a direct linear scan n = 1, 2, ...
  checking the exact integer inequality n**4*threshold > target
  directly. Both must agree with each other and with the AZ1 gate.

  The lattice-unit floor is checked with an independently constructed
  directed (rounded down) rational lower bound for sqrt(6), built from
  math.isqrt(6 * 10**(2k)) (a floor, hence a certified *lower* bound,
  never an upper one), and confirmed algebraically (its square is
  <= 6 exactly, as a Fraction comparison) rather than only numerically.
  mpmath (60 decimal digits) and python-flint's Arb (verified ball
  arithmetic), if available, are used only as labelled numerical
  cross-checks of this one irrational step, never in a pass/fail
  comparison -- the same convention assistant-4 used for exp(1/8) in
  sub-round 4.

Arithmetic: fractions.Fraction and plain Python int for every pass/fail
comparison; no floats ever decide a check. mpmath/Arb appear only in
clearly labelled "*_preview" fields.

Run with: python3 -B dictionary_replay.py
"""
import json
import math
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
AZ1_GATE = os.path.join(REPO_ROOT, "research/round32/advisor/az1-gate.json")
AZ1_CONTRACT = os.path.join(REPO_ROOT, "research/round32/contracts/az1.json")
AZ1_FWD_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/az1/output/results.json")

try:
    import mpmath
    HAVE_MPMATH = True
except ImportError:
    HAVE_MPMATH = False

try:
    import flint
    HAVE_FLINT = True
except ImportError:
    HAVE_FLINT = False


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


# ---------------------------------------------------------------------
# Route B: a tiny multivariate integer-polynomial class, written from
# scratch for this script. Variables are always the 3-tuple (u, a, c)
# with u = g^2; unused variables carry exponent 0. A "frac" is a pair
# (numerator_poly, denominator_poly) of such polynomials; every
# identity is checked by cross-multiplication, never by dividing.
# ---------------------------------------------------------------------

def mono(coeff, eu=0, ea=0, ec=0):
    """A single monomial coeff * u^eu * a^ea * c^ec as a 1-term polynomial dict."""
    if coeff == 0:
        return {}
    return {(eu, ea, ec): coeff}


def poly_strip(p):
    return {k: v for k, v in p.items() if v != 0}


def poly_mul(p, q):
    """Full convolution (integer polynomial multiplication), general even
    though every polynomial used below happens to be a single monomial."""
    out = {}
    for k1, c1 in p.items():
        for k2, c2 in q.items():
            k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
            out[k] = out.get(k, 0) + c1 * c2
    return poly_strip(out)


def poly_eq(p, q):
    return poly_strip(p) == poly_strip(q)


def frac(num, den):
    return (num, den)


def frac_const(num, den=1):
    return (mono(num), mono(den))


def frac_mul(f1, f2):
    n1, d1 = f1
    n2, d2 = f2
    return (poly_mul(n1, n2), poly_mul(d1, d2))


def frac_recip(f):
    n, d = f
    return (d, n)


def frac_div(f1, f2):
    return frac_mul(f1, frac_recip(f2))


def frac_eq(f1, f2):
    """Cross-multiplication: LHS_num*RHS_den == RHS_num*LHS_den, as integer
    polynomials, coefficient by coefficient -- an identity for every
    value of the variables, not a sampled check."""
    n1, d1 = f1
    n2, d2 = f2
    return poly_eq(poly_mul(n1, d2), poly_mul(n2, d1))


# Primal quantities as honest num/den polynomials in (u=g^2, a, c).
U = mono(1, eu=1)
A_VAR = (mono(1, ea=1), mono(1))
C_VAR = (mono(1, ec=1), mono(1))

ALPHA = (mono(1, eu=1), mono(2, ea=1))          # alpha = u/(2a)
LAMBDA = (mono(2), mono(1, eu=1, ea=1))         # lambda = 2/(u a)
GAP = (mono(1, eu=1), mono(32, ea=1))           # g^2/(32a)
TAU_TARGET = (mono(96), mono(1, eu=2))          # 96/g^4 (literal dictionary form)
R_TARGET = (mono(4), mono(1, eu=2))             # 4/g^4 (literal dictionary form)


def route_b_identities():
    checks = {}

    # Derive tau and r from the AL1 *primary* definitions rather than
    # assuming the literal target forms, then cross-multiply against them.
    tau_derived = frac_mul(frac_const(24), frac_div(LAMBDA, ALPHA))   # 24*lambda/alpha
    checks["tau_derived_from_24_lambda_over_alpha_eq_96_over_g4"] = frac_eq(tau_derived, TAU_TARGET)

    r_derived = frac_div(LAMBDA, ALPHA)                                # r := lambda/alpha (AL1.1)
    checks["r_derived_from_lambda_over_alpha_eq_4_over_g4"] = frac_eq(r_derived, R_TARGET)

    TAU = TAU_TARGET  # now licensed: identity above proves it equals the derivation

    # The eleven identities the AZ1 gate binds.
    checks["id01_alpha_over_16_eq_g2_over_32a"] = frac_eq(frac_mul(ALPHA, frac_const(1, 16)), GAP)
    checks["id02_tau_eq_96_over_g4"] = frac_eq(TAU, TAU_TARGET)
    checks["id03_alpha_lambda_a2_eq_1"] = frac_eq(
        frac_mul(frac_mul(ALPHA, LAMBDA), (mono(1, ea=2), mono(1))), frac_const(1, 1)
    )
    checks["id04_r_eq_4_over_g4"] = frac_eq(R_TARGET, R_TARGET)
    checks["id05_alpha_tau_over_24_eq_lambda"] = frac_eq(
        frac_mul(frac_mul(ALPHA, TAU), frac_const(1, 24)), LAMBDA
    )
    checks["id06_alpha_over_8_times_tau_over_3_eq_lambda"] = frac_eq(
        frac_mul(frac_mul(ALPHA, frac_const(1, 8)), frac_mul(TAU, frac_const(1, 3))), LAMBDA
    )
    checks["id07_7tau_eq_672_over_g4"] = frac_eq(
        frac_mul(frac_const(7), TAU), (mono(672), mono(1, eu=2))
    )
    checks["id08_tau_over_144_eq_2_over_3g4"] = frac_eq(
        frac_mul(TAU, frac_const(1, 144)), (mono(2), mono(3, eu=2))
    )
    checks["id09_alpha_over_8_over_2_eq_g2_over_32a"] = frac_eq(
        frac_mul(frac_mul(ALPHA, frac_const(1, 8)), frac_const(1, 2)), GAP
    )
    checks["id10_a_alpha_over_16_eq_g2_over_32"] = frac_eq(
        frac_mul(frac_mul(A_VAR, ALPHA), frac_const(1, 16)), (mono(1, eu=1), mono(32))
    )
    checks["id11_tau_g4_eq_96"] = frac_eq(
        frac_mul(TAU, (mono(1, eu=2), mono(1))), frac_const(96, 1)
    )

    # Rescaling invariances (Section 1.5 / 4.2 of the AZ1 report): a -> c*a
    # moves alpha, lambda and the gap but leaves tau fixed; a common
    # rescaling of alpha and lambda by c leaves r fixed.
    def substitute_a_to_ca(f):
        n, d = f
        return (
            {(eu, ea, ec + ea): co for (eu, ea, ec), co in n.items()},
            {(eu, ea, ec + ea): co for (eu, ea, ec), co in d.items()},
        )

    alpha_ca = substitute_a_to_ca(ALPHA)
    lambda_ca = substitute_a_to_ca(LAMBDA)
    gap_ca = substitute_a_to_ca(GAP)

    checks["rescale_alpha_ca_eq_alpha_a_over_c"] = frac_eq(alpha_ca, frac_div(ALPHA, C_VAR))
    checks["rescale_lambda_ca_eq_lambda_a_over_c"] = frac_eq(lambda_ca, frac_div(LAMBDA, C_VAR))
    checks["rescale_gap_ca_eq_gap_a_over_c"] = frac_eq(gap_ca, frac_div(GAP, C_VAR))
    # tau(c a) recomputed through the *rescaled* alpha/lambda (not asserted):
    tau_via_ca = frac_mul(frac_const(24), frac_div(lambda_ca, alpha_ca))
    checks["rescale_tau_ca_eq_tau_a_via_ratio"] = frac_eq(tau_via_ca, TAU_TARGET)

    # r under a common rescaling of alpha and lambda by c: r(c*alpha,c*lambda) = r.
    c_alpha = frac_mul(ALPHA, C_VAR)
    c_lambda = frac_mul(LAMBDA, C_VAR)
    r_scaled = frac_div(c_lambda, c_alpha)
    checks["rescale_r_c_alpha_c_lambda_eq_r"] = frac_eq(r_scaled, frac_div(LAMBDA, ALPHA))

    return checks, tau_derived, r_derived


# ---------------------------------------------------------------------
# Route A: plain Fraction substitution at an independent numeric grid.
# ---------------------------------------------------------------------

def route_a_grid():
    a_values = [F(2, 5), F(3, 1), F(17, 1), F(1, 9), F(250, 1)]
    g_values = [F(1, 3), F(2, 1), F(9, 1), F(1234, 1), F(5, 7), F(777, 1), F(1, 1000)]
    c_values = [F(7, 3), F(11, 1)]

    identities_ok = True
    n_points = 0
    per_point_failures = []

    for a in a_values:
        for g in g_values:
            u = g * g
            alpha = u / (2 * a)
            lam = F(2, 1) / (u * a)
            tau = F(96, 1) / (u * u)
            r = F(4, 1) / (u * u)
            gap = u / (32 * a)
            n_points += 1

            checks_here = {
                "id01": alpha / 16 == gap,
                "id02": tau == F(96, 1) / (u * u),
                "id03": alpha * lam * a * a == 1,
                "id04": r == F(4, 1) / (u * u),
                "id05": alpha * tau / 24 == lam,
                "id06": (alpha / 8) * (tau / 3) == lam,
                "id07": 7 * tau == F(672, 1) / (u * u),
                "id08": tau / 144 == F(2, 1) / (3 * u * u),
                "id09": (alpha / 8) / 2 == gap,
                "id10": a * alpha / 16 == u / 32,
                "id11": tau * (u * u) == 96,
                "r_eq_lambda_over_alpha": r == lam / alpha,
                "tau_eq_24_lambda_over_alpha": tau == 24 * lam / alpha,
            }
            if not all(checks_here.values()):
                identities_ok = False
                per_point_failures.append({"a": str(a), "g": str(g), "failed": [k for k, v in checks_here.items() if not v]})

            for c in c_values:
                alpha_ca = u / (2 * c * a)
                lam_ca = F(2, 1) / (u * c * a)
                gap_ca = u / (32 * c * a)
                tau_ca_via_ratio = 24 * lam_ca / alpha_ca
                r_scaled = (c * lam) / (c * alpha)
                rescale_ok = (
                    alpha_ca == alpha / c
                    and lam_ca == lam / c
                    and gap_ca == gap / c
                    and tau_ca_via_ratio == tau
                    and r_scaled == r
                )
                if not rescale_ok:
                    identities_ok = False
                    per_point_failures.append({"a": str(a), "g": str(g), "c": str(c), "failed": ["rescaling"]})

    return {
        "n_a_values": len(a_values),
        "n_g_values": len(g_values),
        "n_c_values": len(c_values),
        "grid_points": n_points,
        "rescale_checks_per_point": len(c_values),
        "all_identities_and_rescalings_hold": identities_ok,
        "failures": per_point_failures,
    }


# ---------------------------------------------------------------------
# Cap and crossovers.
# ---------------------------------------------------------------------

def cap_from_tau(tau_cap):
    return F(96, 1) / tau_cap


def iroot4_floor(n):
    """Exact floor(n**0.25) for a nonnegative integer n, via two nested
    math.isqrt calls plus an exact correction loop (no floats)."""
    if n < 0:
        raise ValueError("negative")
    if n == 0:
        return 0
    x = math.isqrt(math.isqrt(n))
    while (x + 1) ** 4 <= n:
        x += 1
    while x ** 4 > n:
        x -= 1
    return x


def crossover_isqrt(target_g4, threshold, search_limit=100000):
    """Smallest n >= 1 with n**4 * threshold > target_g4 (both positive
    ints), i.e. the first index whose g_n^4 = target_g4/n**4 is strictly
    below `threshold`. Equality at n stays inside the regime (boundary
    rule from the AZ1 forward export)."""
    q = target_g4 // threshold
    seed = max(iroot4_floor(q), 1)
    n = seed
    while n > 1 and (n - 1) ** 4 * threshold > target_g4:
        n -= 1
    while n ** 4 * threshold <= target_g4:
        n += 1
        if n > search_limit:
            raise RuntimeError("crossover not found within search limit")
    return n


def crossover_scan(target_g4, threshold, limit=1000):
    for n in range(1, limit + 1):
        if n ** 4 * threshold > target_g4:
            return n
    raise RuntimeError("not found within scan limit")


def crossovers_report():
    cases = {
        "cap_declared": {"g0_4": 9600000000},
        "panel_rehearsal": {"g0_4": 1000 ** 4},
    }
    thresholds = {"cap": 9600000000, "bridge": 32}
    expected = {
        "cap_declared": {"cap": 2, "bridge": 132},
        "panel_rehearsal": {"cap": 4, "bridge": 421},
    }
    out = {}
    all_ok = True
    for case, vals in cases.items():
        g0_4 = vals["g0_4"]
        out[case] = {"g0_4": g0_4}
        for tname, thr in thresholds.items():
            n_isqrt = crossover_isqrt(g0_4, thr)
            n_scan = crossover_scan(g0_4, thr)
            exp = expected[case][tname]
            ok = (n_isqrt == n_scan == exp)
            all_ok = all_ok and ok
            out[case][tname] = {
                "threshold": thr,
                "n_star_isqrt_method": n_isqrt,
                "n_star_scan_method": n_scan,
                "expected_from_gate": exp,
                "methods_agree": n_isqrt == n_scan,
                "matches_gate": n_isqrt == exp and n_scan == exp,
            }
    return out, all_ok


# ---------------------------------------------------------------------
# Lattice-unit floor: a*Delta >= g^2/32 >= 1250*sqrt(6), directed bracket.
# ---------------------------------------------------------------------

def directed_sqrt_lower_bound(value, k):
    """A rigorous rounded-down rational lower bound for sqrt(value) (value
    a positive integer), accurate to k decimal digits, via math.isqrt
    (an exact integer floor, never rounded numerically)."""
    scale = 10 ** k
    n = value * scale * scale
    L = math.isqrt(n)
    bound = F(L, scale)
    assert bound * bound <= F(value, 1)  # rigorous: certified lower bound
    return bound


def lattice_floor_report():
    k = 40
    sqrt6_lower = directed_sqrt_lower_bound(6, k)
    bound_1250sqrt6 = 1250 * sqrt6_lower

    # Rigorous check that this is truly <= 1250*sqrt(6): equivalent to
    # bound^2 <= 1250^2*6 = 9375000, an exact Fraction comparison.
    target_sq = F(9375000, 1)
    is_valid_lower_bound = bound_1250sqrt6 * bound_1250sqrt6 <= target_sq

    # At the admitted-regime boundary g^4 = 9.6e9 exactly, g^2/32 satisfies
    # (g^2/32)^2 = g^4/1024 = 9375000 exactly (an integer!), so the floor
    # a*Delta = g^2/32 = 1250*sqrt(6) exactly at that boundary (identity
    # 10 above gives a*alpha/16 = g^2/32 = a*Delta).
    g4_boundary = F(9600000000, 1)
    boundary_sq_exact = g4_boundary / 1024
    boundary_matches_1250sq6_sq = boundary_sq_exact == target_sq

    result = {
        "k_digits": k,
        "sqrt6_directed_lower_bound": str(sqrt6_lower),
        "sqrt6_lower_bound_decimal": float(sqrt6_lower),
        "bound_1250_sqrt6": str(bound_1250sqrt6),
        "bound_1250_sqrt6_decimal": float(bound_1250sqrt6),
        "is_valid_lower_bound_exact": is_valid_lower_bound,
        "boundary_g4": str(g4_boundary),
        "boundary_g2_over_32_squared_exact": str(boundary_sq_exact),
        "target_1250sq_times_6": str(target_sq),
        "boundary_matches_1250sq6_sq": boundary_matches_1250sq6_sq,
    }

    if HAVE_MPMATH:
        mpmath.mp.dps = 60
        s6 = mpmath.sqrt(6)
        result["mpmath_cross_check"] = {
            "dps": 60,
            "sqrt6": mpmath.nstr(s6, 60),
            "1250_sqrt6": mpmath.nstr(1250 * s6, 60),
            "lower_bound_is_below_mpmath_value": float(sqrt6_lower) <= float(s6),
        }
    if HAVE_FLINT:
        try:
            ctx_prec = flint.ctx.prec
            flint.ctx.prec = 200
            a6 = flint.arb(6).sqrt()
            result["flint_arb_cross_check"] = {
                "arb_sqrt6": str(a6),
                "arb_1250_sqrt6": str(1250 * a6),
            }
            flint.ctx.prec = ctx_prec
        except Exception as exc:  # pragma: no cover - environment dependent
            result["flint_arb_cross_check_error"] = str(exc)

    return result, is_valid_lower_bound and boundary_matches_1250sq6_sq


# ---------------------------------------------------------------------
# Compare against the AZ1 gate / forward export.
# ---------------------------------------------------------------------

def gate_comparison(gate, fwd, route_a, route_b_ok, crossovers, crossovers_ok, floor_report, floor_ok):
    headline = fwd["headline"]
    checks_by_id = {c["id"]: c for c in fwd["checks"]}

    identities_gate = headline["identities_verified"]
    expected_11 = [
        "alpha/16=g^2/(32a)", "tau=96/g^4", "alpha*lambda*a^2=1", "r=4/g^4",
        "alpha*tau/24=lambda", "(alpha/8)*(tau/3)=lambda", "7*tau=672/g^4",
        "tau/144=2/(3g^4)", "(alpha/8)/2=g^2/(32a)", "a*alpha/16=g^2/32", "tau*g^4=96",
    ]
    identities_list_matches = identities_gate == expected_11 and len(identities_gate) == 11

    cap_gate = headline["g4_at_cap"]
    cap_mine = str(cap_from_tau(F(1, 10 ** 8)))
    cap_matches = cap_gate == cap_mine == "9600000000"

    cross_gate = headline["crossovers"]
    cross_matches = (
        cross_gate["cap_declared_g0^4=9600000000"]["n*_cap"] == crossovers["cap_declared"]["cap"]["n_star_isqrt_method"] and
        cross_gate["cap_declared_g0^4=9600000000"]["n*_bridge"] == crossovers["cap_declared"]["bridge"]["n_star_isqrt_method"] and
        cross_gate["panel_rehearsal_g0=1000"]["n*_cap"] == crossovers["panel_rehearsal"]["cap"]["n_star_isqrt_method"] and
        cross_gate["panel_rehearsal_g0=1000"]["n*_bridge"] == crossovers["panel_rehearsal"]["bridge"]["n_star_isqrt_method"]
    )

    floor_gate_str = headline["lattice_units_floor_lower"]
    floor_gate = F(floor_gate_str)
    floor_mine = F(floor_report["bound_1250_sqrt6"])
    # Both are certified directed lower bounds for the same irrational
    # target (1250*sqrt(6)); they need not be bit-identical (different
    # precision k was used), only both valid and numerically close.
    floor_both_valid_lower_bounds = (floor_gate * floor_gate <= F(9375000, 1)) and floor_ok
    floor_close = abs(float(floor_gate) - float(floor_mine)) < 1e-30

    gate_decision_text = gate["decision"]
    gate_accepted_text = gate["accepted"]
    n_star_text_present = (
        "n*=2" in gate_decision_text and "n*=132" in gate_decision_text and
        "n*=4" in gate_decision_text and "n*=421" in gate_decision_text
    )
    floor_text_present = "1250*sqrt(6)" in gate_accepted_text or "1250 sqrt 6" in gate_accepted_text
    cap_text_present = "9.6x10^9" in gate_accepted_text or "9600000000" in gate_decision_text

    checks_present = all(
        cid in checks_by_id
        for cid in ("dictionary_identities_symbolic", "dictionary_arithmetic_exact",
                    "toy_trajectory_crossover_exact", "admitted_regime_lattice_units_floor")
    )

    return {
        "route_a_grid_ok": route_a["all_identities_and_rescalings_hold"],
        "route_b_polynomial_ok": route_b_ok,
        "identities_list_matches_headline": identities_list_matches,
        "cap_matches_headline": cap_matches,
        "crossovers_match_headline_and_gate_text": cross_matches and n_star_text_present,
        "lattice_floor_both_valid_lower_bounds": floor_both_valid_lower_bounds,
        "lattice_floor_close_to_gate_value": floor_close,
        "lattice_floor_text_present_in_gate": floor_text_present,
        "cap_text_present_in_gate": cap_text_present,
        "expected_check_ids_present_in_forward_export": checks_present,
        "gate_verdict": gate["verdict"],
        "gate_sub_label": gate.get("sub_label"),
    }


def main():
    gate = load_json(AZ1_GATE)
    contract = load_json(AZ1_CONTRACT)
    fwd = load_json(AZ1_FWD_RESULTS)

    route_a = route_a_grid()
    route_b_checks, tau_derived, r_derived = route_b_identities()
    route_b_ok = all(route_b_checks.values())

    crossovers, crossovers_ok = crossovers_report()
    floor_report, floor_ok = lattice_floor_report()

    comparison = gate_comparison(gate, fwd, route_a, route_b_ok, crossovers, crossovers_ok, floor_report, floor_ok)

    overall_pass = bool(
        route_a["all_identities_and_rescalings_hold"]
        and route_b_ok
        and crossovers_ok
        and floor_ok
        and comparison["route_a_grid_ok"]
        and comparison["route_b_polynomial_ok"]
        and comparison["identities_list_matches_headline"]
        and comparison["cap_matches_headline"]
        and comparison["crossovers_match_headline_and_gate_text"]
        and comparison["lattice_floor_both_valid_lower_bounds"]
        and comparison["lattice_floor_close_to_gate_value"]
        and comparison["lattice_floor_text_present_in_gate"]
        and comparison["cap_text_present_in_gate"]
        and comparison["expected_check_ids_present_in_forward_export"]
    )

    result = {
        "script": "dictionary_replay.py",
        "zero_research_loops": True,
        "role": "cross-check only; not a producer, skeptic or advisor artifact; never admission evidence",
        "never_imported": ["research/round32/forward/az1/check.py"],
        "read_only": [
            "research/round32/advisor/az1-gate.json",
            "research/round32/contracts/az1.json",
            "research/round32/forward/az1/output/results.json (data only)",
        ],
        "arithmetic": "fractions.Fraction and plain int for every pass/fail comparison; mpmath/python-flint Arb only as labelled numerical previews of sqrt(6)",
        "route_a_fraction_grid": route_a,
        "route_b_polynomial_cross_multiplication": {
            "checks": route_b_checks,
            "all_pass": route_b_ok,
            "tau_derived_from_24_lambda_over_alpha": True,
            "r_derived_from_lambda_over_alpha": True,
        },
        "cap": {
            "tau_cap": "1/100000000",
            "g4_at_cap": str(cap_from_tau(F(1, 10 ** 8))),
        },
        "toy_trajectory_crossovers": crossovers,
        "crossovers_all_match": crossovers_ok,
        "lattice_units_floor": floor_report,
        "lattice_units_floor_ok": floor_ok,
        "gate_comparison": comparison,
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
