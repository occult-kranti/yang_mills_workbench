#!/usr/bin/env python3
"""
haar_moments.py
Historical (Newton/Tesla) lens research assistant, Round33 applications
stage (assistant-4). Zero research loops: an independent, from-scratch
exact computation of E_Haar[W^k], k=1..4, for SU(2) and U(1) by direct
integration (the Weyl density for SU(2); the binomial constant term for
U(1)) and for Z2 by summation, plus the first-order coefficient
2*(1/3)*E[W^2]/(32*C_F) under the frozen BD1 convention, compared with
the BD1 gate.

This script never imports or executes research/round33/forward/bd1/
check.py, research/round33/reverse/bd1/check.py, or any other check.py.
It reads, as data only: research/round33/contracts/bd1.json (frozen)
and research/round33/advisor/bd1-gate.json.

Route, independent of both BD1 producers' own code:
  - SU(2): the class-function Weyl integration formula for SU(2),
    dmu(theta) = (2/pi) sin^2(theta) dtheta on theta in [0,pi] (the
    pushforward of Haar measure onto the eigenangle of a conjugacy
    class, i.e. the "Weyl density"), with W = cos(theta) (the real part
    of the trace of the fundamental over its dimension 2), integrated
    exactly via the classical Wallis recursion for
    J_n = int_0^{pi/2} cos^n(theta) dtheta (J_n is a rational multiple
    of pi for every even n, and the pi cancels exactly against the
    (2/pi) density prefactor, leaving an exact rational for every
    E[W^{2m}]). This is the "direct integration" route the task names,
    entirely independent of the two BD1 producers' character/Peter-Weyl
    or torus-constant-term routes.
  - U(1): W = cos(theta), Haar measure dtheta/(2 pi) uniform on the
    circle. cos^k(theta) = 2^-k sum_j C(k,j) e^{i(k-2j)theta}
    (binomial expansion); the Haar average keeps only the constant
    (frequency-0) term, i.e. j=k/2 when k is even (0 when k is odd).
    This is the "binomial constant term" the task names.
  - Z2: W in {+1,-1}, each with weight 1/2 (Haar measure on the two-
    element group); E[W^k] by direct summation, (1^k+(-1)^k)/2.

Arithmetic: `fractions.Fraction` throughout for every value that enters
a comparison; no floats decide anything (decimals below, where printed,
are labelled previews only, and none is printed here since every
quantity is already an exact small rational).

Run with: python3 -B haar_moments.py
Also checked identical under: python3 -B -O haar_moments.py
"""
import json
import os
import re
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

BD1_CONTRACT = os.path.join(REPO_ROOT, "research/round33/contracts/bd1.json")
BD1_GATE = os.path.join(REPO_ROOT, "research/round33/advisor/bd1-gate.json")

FORBIDDEN_SUBSTRINGS = ("check.py",)


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def load_text(path):
    with open(path) as fh:
        return fh.read()


for _p in (BD1_CONTRACT, BD1_GATE):
    assert not any(f in _p for f in FORBIDDEN_SUBSTRINGS), _p


# =====================================================================
# Part 1: SU(2) by direct integration of the Weyl density.
#
# The Weyl integration formula for a class function f on SU(2) is
#   integral_SU(2) f dHaar = (2/pi) integral_0^pi f(theta) sin^2(theta) dtheta,
# where e^{+-i theta} are the eigenvalues of the fundamental
# representation (this is the pushforward of Haar measure by the map
# to the eigenangle; the (2/pi) sin^2 density is the standard SU(2)
# Weyl density, |Delta(e^{i theta})|^2 normalized to a probability
# measure on [0,pi]). W = (1/2) Tr(fundamental) = cos(theta).
#
# E[W^k] = (2/pi) integral_0^pi cos^k(theta) sin^2(theta) dtheta.
#
# For odd k the integrand is antisymmetric under theta -> pi - theta
# (cos^k flips sign, sin^2 is invariant), so E[W^k] = 0 for odd k.
#
# For even k = 2m, substitute theta -> pi - theta on [pi/2, pi] to see
# the integral over [0,pi] is twice the integral over [0,pi/2], and use
# the classical Wallis recursion
#   J_n = integral_0^{pi/2} cos^n(theta) dtheta,   J_0 = pi/2, J_1 = 1,
#   J_n = (n-1)/n * J_{n-2}    (n >= 2).
# For even n, J_n = C_{n/2} * pi with C_0 = 1/2, C_{m+1} = C_m*(2m+1)/(2m+2)
# an exact rational (checked below against the closed double-factorial
# form 2*(2m-1)!!/(2m)!! as a second, independent route to the same
# C_m). Then
#   integral_0^{pi/2} cos^{2m}(theta) sin^2(theta) dtheta
#     = J_{2m} - J_{2m+2} = (C_m - C_{m+1}) * pi,
# so E[W^{2m}] = (2/pi) * 2 * (C_m - C_{m+1}) * pi = 4*(C_m - C_{m+1}),
# an exact rational with pi cancelled exactly (never approximated).
# =====================================================================

def wallis_C(m):
    """C_m = J_{2m}/pi, computed by the Wallis recursion, exactly."""
    c = Fraction(1, 2)  # C_0 = J_0/pi = (pi/2)/pi
    for i in range(m):
        c = c * Fraction(2 * i + 1, 2 * i + 2)
    return c


def double_factorial(n):
    if n <= 0:
        return 1
    result = 1
    k = n
    while k > 0:
        result *= k
        k -= 2
    return result


def wallis_C_double_factorial_route(m):
    """Second, independent route to the same C_m: the classical closed
    form J_{2m} = pi/2 * (2m-1)!!/(2m)!!, i.e. C_m = (2m-1)!!/(2m)!! / 2."""
    return Fraction(double_factorial(2 * m - 1), double_factorial(2 * m)) * Fraction(1, 2)


def su2_moment(k):
    if k % 2 == 1:
        return Fraction(0)
    m = k // 2
    Cm = wallis_C(m)
    Cm1 = wallis_C(m + 1)
    Cm_check = wallis_C_double_factorial_route(m)
    Cm1_check = wallis_C_double_factorial_route(m + 1)
    assert Cm == Cm_check, (k, "recursion vs double-factorial C_m disagree", Cm, Cm_check)
    assert Cm1 == Cm1_check, (k, "recursion vs double-factorial C_{m+1} disagree", Cm1, Cm1_check)
    return 4 * (Cm - Cm1)


def su2_moments_direct_integration():
    return {k: su2_moment(k) for k in range(1, 5)}


# A second, independent check of the whole SU(2) integral: the exact
# antiderivative of cos^k(theta) sin^2(theta) via the polynomial
# expansion in the variable u = sin(theta), integrated termwise as a
# definite Riemann sum limit is impractical without floats; instead we
# check the Wallis values against the well-known closed forms for
# small even n directly (J_2 = pi/4, J_4 = 3pi/16, J_6 = 5pi/32),
# i.e. C_1 = 1/4, C_2 = 3/16, C_3 = 5/32 -- literature constants, not
# re-derived from this script's own recursion.
KNOWN_C = {1: Fraction(1, 4), 2: Fraction(3, 16), 3: Fraction(5, 32)}


def check_known_wallis_constants():
    ok = True
    detail = {}
    for m, expected in KNOWN_C.items():
        got = wallis_C(m)
        detail[str(m)] = {"got": str(got), "expected": str(expected), "matches": got == expected}
        if got != expected:
            ok = False
    return ok, detail


# =====================================================================
# Part 2: U(1) by the binomial constant term.
#
# cos^k(theta) = (1/2^k) * sum_{j=0}^k C(k,j) e^{i(k-2j)theta}
# (binomial expansion of ((e^{i theta}+e^{-i theta})/2)^k). Haar
# measure on U(1) is uniform, so the average of e^{i n theta} is 1 if
# n=0 and 0 otherwise: the average keeps exactly the terms with
# k - 2j = 0, i.e. j = k/2 (only possible for even k). Hence
#   E[W^k] = 0                       (k odd)
#   E[W^k] = C(k, k/2) / 2^k         (k even).
# =====================================================================

def binomial(n, r):
    if r < 0 or r > n:
        return 0
    num = 1
    den = 1
    for i in range(r):
        num *= (n - i)
        den *= (i + 1)
    return num // den


def u1_moment(k):
    if k % 2 == 1:
        return Fraction(0)
    return Fraction(binomial(k, k // 2), 2 ** k)


def u1_moments_binomial_constant_term():
    return {k: u1_moment(k) for k in range(1, 5)}


# =====================================================================
# Part 3: Z2 by direct summation.
# =====================================================================

def z2_moment(k):
    return Fraction(1 ** k + (-1) ** k, 2)


def z2_moments_summation():
    return {k: z2_moment(k) for k in range(1, 5)}


# =====================================================================
# Part 4: the first-order coefficient under the frozen BD1 convention,
# 2*(1/3)*E[W^2]/(32*C_F), for the three groups this script covers.
# C_F is read from the convention, not fitted: SU(2) fundamental
# C_2 = j(j+1) at j=1/2 -> 3/4; U(1) charge 1 -> C_2 = 1^2 = 1;
# Z2 odd state -> C_2 = 1 (frozen convention text: "C_F=1 for Z2 as
# for U(1)").
# =====================================================================

C_F = {"SU(2)": Fraction(3, 4), "U(1)": Fraction(1), "Z2": Fraction(1)}


def first_order_coefficient(e_w2, c_f):
    return Fraction(2, 1) * Fraction(1, 3) * e_w2 / (32 * c_f)


# =====================================================================
# Part 5: comparison with the BD1 gate (data only).
# =====================================================================

def parse_moment_from_gate(gate_text, group_prefix):
    """The gate's accepted text lists moments as
    'SU(2) 0,1/4,0,1/8; SU(3) 0,1/18,...' -- extract the four
    comma-separated fractions following the group name."""
    pattern = re.escape(group_prefix) + r" (-?\d+(?:/\d+)?),(-?\d+(?:/\d+)?),(-?\d+(?:/\d+)?),(-?\d+(?:/\d+)?)"
    m = re.search(pattern, gate_text)
    if not m:
        return None
    return [Fraction(g) for g in m.groups()]


def parse_first_order_from_gate(gate_text, group_prefix, stop_chars=","):
    """The gate's decision text lists first-order coefficients as
    'SU(2) 1/144 (the admitted value...), SU(3) 1/1152, SU(4) 1/2880,
    SU(5) 1/5760, U(1) 1/96, Z2 1/48, SO(3) 1/864'."""
    pattern = re.escape(group_prefix) + r" (\d+/\d+)"
    m = re.search(pattern, gate_text)
    if not m:
        return None
    return Fraction(m.group(1))


def main():
    su2 = su2_moments_direct_integration()
    u1 = u1_moments_binomial_constant_term()
    z2 = z2_moments_summation()

    wallis_ok, wallis_detail = check_known_wallis_constants()

    fo = {
        "SU(2)": first_order_coefficient(su2[2], C_F["SU(2)"]),
        "U(1)": first_order_coefficient(u1[2], C_F["U(1)"]),
        "Z2": first_order_coefficient(z2[2], C_F["Z2"]),
    }

    gate_text = load_text(BD1_GATE)
    gate_moments = {
        "SU(2)": parse_moment_from_gate(gate_text, "SU(2)"),
        "U(1)": parse_moment_from_gate(gate_text, "U(1)"),
        "Z2": parse_moment_from_gate(gate_text, "Z2"),
    }
    gate_fo = {
        "SU(2)": parse_first_order_from_gate(gate_text, "SU(2)"),
        "U(1)": parse_first_order_from_gate(gate_text, "U(1)"),
        "Z2": parse_first_order_from_gate(gate_text, "Z2"),
    }

    contract = load_json(BD1_CONTRACT)
    conv = contract["parameters"]["convention"]

    checks = {}
    checks["wallis_known_constants_match"] = wallis_ok

    checks["su2_moment_1_is_0"] = su2[1] == 0
    checks["su2_moment_2_is_1_4"] = su2[2] == Fraction(1, 4)
    checks["su2_moment_3_is_0"] = su2[3] == 0
    checks["su2_moment_4_is_1_8"] = su2[4] == Fraction(1, 8)

    checks["u1_moment_1_is_0"] = u1[1] == 0
    checks["u1_moment_2_is_1_2"] = u1[2] == Fraction(1, 2)
    checks["u1_moment_3_is_0"] = u1[3] == 0
    checks["u1_moment_4_is_3_8"] = u1[4] == Fraction(3, 8)

    checks["z2_moment_1_is_0"] = z2[1] == 0
    checks["z2_moment_2_is_1"] = z2[2] == 1
    checks["z2_moment_3_is_0"] = z2[3] == 0
    checks["z2_moment_4_is_1"] = z2[4] == 1

    checks["fo_su2_is_1_144"] = fo["SU(2)"] == Fraction(1, 144)
    checks["fo_u1_is_1_96"] = fo["U(1)"] == Fraction(1, 96)
    checks["fo_z2_is_1_48"] = fo["Z2"] == Fraction(1, 48)

    checks["contract_C2_n_squared_for_U1"] = "C_2(n) = n^2" in conv
    checks["contract_C_F_1_for_Z2"] = "C_F = 1 for Z2" in conv

    for g in ("SU(2)", "U(1)", "Z2"):
        gv = gate_moments[g]
        checks["gate_moments_found_%s" % g.replace("(", "").replace(")", "")] = gv is not None
        if gv is not None:
            mine = [su2, u1, z2][["SU(2)", "U(1)", "Z2"].index(g)]
            matches = [mine[k] == gv[k - 1] for k in range(1, 5)]
            checks["gate_moments_match_%s" % g.replace("(", "").replace(")", "")] = all(matches)
        gfo = gate_fo[g]
        checks["gate_fo_found_%s" % g.replace("(", "").replace(")", "")] = gfo is not None
        if gfo is not None:
            checks["gate_fo_matches_%s" % g.replace("(", "").replace(")", "")] = (fo[g] == gfo)

    overall = all(checks.values())

    report = {
        "script": "haar_moments.py",
        "task": "independent exact computation of E_Haar[W^k], k=1..4, for SU(2) (Weyl "
                "density direct integration), U(1) (binomial constant term) and Z2 "
                "(summation), and the first-order coefficient under the frozen BD1 "
                "convention, compared with the BD1 gate",
        "wallis_recursion_constants_C_m": {str(m): str(wallis_C(m)) for m in range(0, 5)},
        "wallis_known_constants_cross_check": wallis_detail,
        "moments": {
            "SU(2)": {str(k): str(v) for k, v in su2.items()},
            "U(1)": {str(k): str(v) for k, v in u1.items()},
            "Z2": {str(k): str(v) for k, v in z2.items()},
        },
        "C_F": {g: str(v) for g, v in C_F.items()},
        "first_order_coefficients": {g: str(v) for g, v in fo.items()},
        "gate_moments_parsed": {
            g: ([str(x) for x in v] if v is not None else None) for g, v in gate_moments.items()
        },
        "gate_first_order_parsed": {g: (str(v) if v is not None else None) for g, v in gate_fo.items()},
        "checks": checks,
        "overall_pass": overall,
    }
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
