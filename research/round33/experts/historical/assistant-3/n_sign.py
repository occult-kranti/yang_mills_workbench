#!/usr/bin/env python3
"""
n_sign.py
Historical (Newton/Tesla) lens research assistant, Round33 sub-round 3
(assistant-3). Zero research loops: an independent, exact-arithmetic
recomputation of N_sign (BC1 forward report Section 5, HNM-BC1-F04) from

    C' = 4/984375, q = 1/64,

and the AW2 enclosure endpoints L = tau/144 - K_2^+ tau^2 and
U = tau/144 + K_2^+ tau^2 at tau = 10^-8, with K_2^+ read from the
hash-verified AW2 gate (research/round32/advisor/aw2-gate.json). N_sign
is the least N at least 2 with C' q^(N-1) strictly below L (BC1
contract `new_control_semantics.finite_box_sign_from_whole_sequence`).

This script never imports or executes research/round33/forward/bc1/
check.py, research/round33/skeptic/bc1_check.py,
research/round33/skeptic/bc1_postreview_check.py, or any other
check.py, and never reads anything under
research/round33/forward/bd*/ or research/round33/reverse/bd1/ (in
production at the time this package was written). K_2^+ and C' are
parsed as exact rationals directly out of the plain text of the AW2 and
BB2 gates (regex over the quoted "K_2^+=<num>/<den>" and "C'=<num>/
<den>" spans in their `accepted`/`decision` fields), not read from any
producer's output/results.json and not read from the BC1 packet's own
already-restated values -- only afterwards is the result compared
against the BC1 forward report/results.json and the BC1 gate.

Arithmetic: `fractions.Fraction` throughout (tau, K_2^+, C', q, L, U and
every comparison decided by this script are exact rationals). No
floats participate in any pass/fail decision; decimals below are
labelled previews only.

Run with: python3 -B n_sign.py
Also checked identical under: python3 -B -O n_sign.py
"""
import json
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

AW2_GATE = os.path.join(REPO_ROOT, "research/round32/advisor/aw2-gate.json")
BB2_GATE = os.path.join(REPO_ROOT, "research/round33/advisor/bb2-gate.json")
BC1_GATE = os.path.join(REPO_ROOT, "research/round33/advisor/bc1-gate.json")
BC1_FWD_RESULTS = os.path.join(REPO_ROOT, "research/round33/forward/bc1/output/results.json")
BC1_FWD_REPORT = os.path.join(REPO_ROOT, "research/round33/forward/bc1/report.md")

FORBIDDEN_SUBSTRINGS = ("forward/bd", "reverse/bd1", "check.py")


def load_text(path):
    with open(path) as fh:
        return fh.read()


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


for _p in (AW2_GATE, BB2_GATE, BC1_GATE, BC1_FWD_RESULTS, BC1_FWD_REPORT):
    assert not any(f in _p for f in ("forward/bd", "reverse/bd1")), _p


TAU = Fraction(1, 10 ** 8)
Q = Fraction(1, 64)


# ---------------------------------------------------------------------
# Part 1: parse K_2^+ from the AW2 gate text and C' from the BB2 gate
# text, as exact rationals, independently of any producer's own parser.
# ---------------------------------------------------------------------

def parse_unique_fraction(text, pattern, label):
    """Find `pattern` (with two capture groups, numerator/denominator)
    in text and return it as an exact Fraction. Raises if not found or
    if more than one distinct value is quoted under the same pattern."""
    matches = re.findall(pattern, text)
    if not matches:
        raise AssertionError("pattern not found for %r" % label)
    values = {Fraction(int(n), int(d)) for n, d in matches}
    if len(values) != 1:
        raise AssertionError("inconsistent values for %r: %r" % (label, values))
    return values.pop()


def parse_constants():
    """K_2^+ from the AW2 gate (unambiguous: quoted once verbatim at
    every occurrence). C' and q from the BB2 gate, using patterns
    specific enough to pick out the `nested_telescoping` *bound* value
    the BC1 contract names (`C' the nested_telescoping bound value of
    the BB2 gate decision`), not the BB2 gate's own labelled
    `union_comparison` value C'=1/250000 or its labelled re-evaluated
    preview, which a bare `C'=<num>/<den>` regex would also match."""
    aw2_text = load_text(AW2_GATE)
    bb2_text = load_text(BB2_GATE)
    k2_plus = parse_unique_fraction(aw2_text, r"K_2\^\+=(\d+)/(\d+)", "K_2^+")
    c_prime_accepted = parse_unique_fraction(
        bb2_text,
        r"C'=(\d+)/(\d+) \(about [^;]*; exact_first_order, nested_telescoping",
        "C' (accepted field, nested_telescoping bound value)",
    )
    c_prime_decision = parse_unique_fraction(
        bb2_text, r"bound values C'=(\d+)/(\d+)", "C' (decision field, bound values)"
    )
    assert c_prime_accepted == c_prime_decision, (c_prime_accepted, c_prime_decision)
    c_prime = c_prime_accepted
    q_bb2 = parse_unique_fraction(bb2_text, r"(?<![_0-9])q=(\d+)/(\d+)", "q")
    return k2_plus, c_prime, q_bb2, aw2_text, bb2_text


# ---------------------------------------------------------------------
# Part 2: the AW2 endpoints L, U at tau = 10^-8, independently
# recomputed from the parsed K_2^+, and cross-checked against the
# literal endpoint rationals quoted in the same AW2 gate text.
# ---------------------------------------------------------------------

def endpoints(k2_plus, tau=TAU):
    L = tau * Fraction(1, 144) - k2_plus * tau * tau
    U = tau * Fraction(1, 144) + k2_plus * tau * tau
    return L, U


def cross_check_endpoints(L, U, aw2_text):
    """The AW2 gate spells its enclosure literally as
    "[num1/D, num2/D], D=<denominator>" (num1 the lower end, num2 the
    upper end); extract that triple and compare against our own
    recomputation from the parsed K_2^+."""
    matches = re.findall(r"\[(\d+)/D, (\d+)/D\], D=(\d+)", aw2_text)
    if not matches:
        return {"literal_endpoints_found": False}
    values = {(n1, n2, d) for n1, n2, d in matches}
    if len(values) != 1:
        raise AssertionError("inconsistent literal AW2 endpoints: %r" % values)
    n1, n2, d = values.pop()
    L_lit = Fraction(int(n1), int(d))
    U_lit = Fraction(int(n2), int(d))
    return {
        "literal_endpoints_found": True,
        "L_matches_gate_literal": L == L_lit,
        "U_matches_gate_literal": U == U_lit,
        "L_lit": str(L_lit),
        "U_lit": str(U_lit),
    }


# ---------------------------------------------------------------------
# Part 3: N_sign, exactly, and the widening table at N=2..6 (the range
# the task asks this script to record).
# ---------------------------------------------------------------------

def widening(c_prime, q, N):
    return c_prime * q ** (N - 1)


def compute_n_sign(c_prime, q, L, n_lo=2, n_hi=10000):
    """Least N >= n_lo with c_prime*q^(N-1) < L, strictly (the BC1
    contract's own rule); q^(N-1) decreases in N since 0<q<1, so this
    search may stop at the first N found, but we scan monotonically
    from n_lo for an auditable, from-scratch computation rather than a
    closed-form log inversion."""
    for N in range(n_lo, n_hi + 1):
        w = widening(c_prime, q, N)
        if w < L:
            return N
    raise AssertionError("N_sign not found in range")


def widening_table(c_prime, q, L, lo=2, hi=6):
    rows = []
    for N in range(lo, hi + 1):
        w = widening(c_prime, q, N)
        rows.append({
            "N": N,
            "widening_exact": str(w),
            "widening_preview": float(w),
            "below_L": bool(w < L),
        })
    return rows


# ---------------------------------------------------------------------
# Part 4: robustness range of C' giving the same N_sign = 4, at the
# same q and L. N_sign(C') = 4 holds exactly when
#     C' q^3 < L  and  C' q^2 >= L,
# i.e. C' in [L/q^2, L/q^3). Both endpoints are computed exactly.
# ---------------------------------------------------------------------

def robustness_range(q, L, n_sign):
    """N_sign(C') = n_sign holds exactly when C' q^(n_sign-1) < L (the
    N=n_sign condition) and C' q^(n_sign-2) >= L (the N=n_sign-1
    condition fails), i.e. C' in [L/q^(n_sign-2), L/q^(n_sign-1))."""
    lower = L / (q ** (n_sign - 2))  # L / q^2 at n_sign=4 (inclusive)
    upper = L / (q ** (n_sign - 1))  # L / q^3 at n_sign=4 (exclusive)
    return lower, upper


def check_robustness_range(c_prime, q, L, n_sign):
    lower, upper = robustness_range(q, L, n_sign)
    in_range = (c_prime >= lower) and (c_prime < upper)
    # Independent brute check: recompute N_sign at both endpoints and at
    # the true C' to confirm the boundary claims.
    n_sign_at_lower = compute_n_sign(lower, q, L)  # boundary itself: C'q^2=L, not < L, so N_sign should be n_sign (lower is inclusive)
    n_sign_at_just_below_upper = compute_n_sign(upper - Fraction(1, 10 ** 30), q, L)
    return {
        "lower_bound_exact": str(lower),
        "lower_bound_preview": float(lower),
        "upper_bound_exact": str(upper),
        "upper_bound_preview": float(upper),
        "c_prime_in_range": in_range,
        "n_sign_at_lower_bound": n_sign_at_lower,
        "n_sign_just_below_upper_bound": n_sign_at_just_below_upper,
    }


# ---------------------------------------------------------------------
# Part 5: cross-check against the BC1 forward report/results.json and
# the BC1 gate (data only; no check.py is read or executed).
# ---------------------------------------------------------------------

def cross_check_bc1(n_sign, table, robust):
    bc1_results = load_json(BC1_FWD_RESULTS)
    bc1_report = load_text(BC1_FWD_REPORT)
    bc1_gate = load_text(BC1_GATE)

    checks = {}
    checks["bc1_report_states_N_sign_4"] = "**`N_sign = 4`**" in bc1_report or "N_sign = 4" in bc1_report
    checks["bc1_gate_states_N_sign_exactly_4"] = "is exactly 4" in bc1_gate

    f2_sign = None
    for c in bc1_results["checks"]:
        if c.get("id") == "f2_finite_box_sign_corollary":
            f2_sign = c
            break
    checks["bc1_results_f2_sign_found"] = f2_sign is not None
    if f2_sign is not None:
        checks["bc1_N_sign_matches"] = f2_sign["N_sign"] == n_sign
        widenings_by_N = {row["N"]: row for row in f2_sign["table"]}
        for row in table:
            N = row["N"]
            if N in widenings_by_N:
                theirs = widenings_by_N[N]
                key = "N%d_widening_matches" % N
                checks[key] = theirs["widening"] == row["widening_exact"]
                key2 = "N%d_certified_matches" % N
                checks[key2] = theirs["certified"] == row["below_L"]

    return checks


def main():
    k2_plus, c_prime, q_bb2, aw2_text, bb2_text = parse_constants()
    assert c_prime == Fraction(4, 984375), c_prime
    assert q_bb2 == Q == Fraction(1, 64), q_bb2

    L, U = endpoints(k2_plus)
    endpoint_cross = cross_check_endpoints(L, U, aw2_text)

    n_sign = compute_n_sign(c_prime, Q, L)
    table = widening_table(c_prime, Q, L, lo=2, hi=6)
    robust = check_robustness_range(c_prime, Q, L, n_sign)

    cross_bc1 = cross_check_bc1(n_sign, table, robust)

    checks = {
        "n_sign_equals_4": n_sign == 4,
        "c_prime_in_robustness_range": robust["c_prime_in_range"],
        "table_N2_not_below_L": table[0]["below_L"] is False,
        "table_N3_not_below_L": table[1]["below_L"] is False,
        "table_N4_below_L": table[2]["below_L"] is True,
        "table_N5_below_L": table[3]["below_L"] is True,
        "table_N6_below_L": table[4]["below_L"] is True,
        "L_less_than_U": L < U,
        "L_positive": L > 0,
    }
    if endpoint_cross.get("literal_endpoints_found"):
        checks["L_matches_gate_literal"] = endpoint_cross["L_matches_gate_literal"]
        checks["U_matches_gate_literal"] = endpoint_cross["U_matches_gate_literal"]

    overall = (
        all(checks.values())
        and all(v for v in cross_bc1.values() if isinstance(v, bool))
    )

    report = {
        "script": "n_sign.py",
        "task": "independent exact recomputation of N_sign from C'=4/984375, q=1/64 and "
                "the AW2 endpoints (tau/144 -+ K_2^+ tau^2 at tau=10^-8), the widenings at "
                "N=2..6, and the robustness range of C' giving the same N_sign",
        "parsed_constants": {
            "K_2_plus": str(k2_plus),
            "K_2_plus_preview": float(k2_plus),
            "C_prime": str(c_prime),
            "C_prime_preview": float(c_prime),
            "q": str(Q),
            "tau": str(TAU),
        },
        "endpoints": {
            "L_exact": str(L),
            "L_preview": float(L),
            "U_exact": str(U),
            "U_preview": float(U),
            "cross_check_against_gate_literal": endpoint_cross,
        },
        "n_sign": n_sign,
        "widening_table_N2_to_6": table,
        "robustness_range_of_C_prime": robust,
        "checks": checks,
        "cross_check_against_bc1_forward_and_gate": cross_bc1,
        "overall_pass": overall,
    }
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
