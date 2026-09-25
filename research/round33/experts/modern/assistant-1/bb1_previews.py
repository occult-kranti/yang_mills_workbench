#!/usr/bin/env python3
"""BB1 marginal-locality target previews from the gated BA1 constants (preview only).

Round33, sub-round 1, modern (Penrose/Feynman) lens, research assistant/coder
"assistant-1". **This script counts zero research loops. Nothing here is
evidence, a contract, a premise or a gate** -- it reproduces, and adds one
independent Arb/mpmath check to, the preview arithmetic already published
(as an advisory, not a producer input) in
`research/round33/experts/modern/bb-targets-proposal.md` section 7,
per `research/round33/experts/modern/loop2-response.md` section 3 item 3.
No BB1 contract, loop or check.py exists yet in this sub-round; BB1 has not
been produced, let alone admitted. This script never imports a producer
`check.py`; it reads only the ADMITTED BA1 `output/results.json` files
(forward and reverse) and `research/round33/advisor/ba1-gate.json`, and the
advisory `bb-targets-proposal.md` text, for comparison.

The two BB1 routes (`bb-targets-proposal.md` section 1, "polymer_kp" and
"iterated_split") both reach the headline rate `q = 1/64` using only
admitted BA1 constants plus the BA1 weighted-norm lemma at the floor
weight `w = 390625/148 = 1/(37888|tau|)`:

  t_bar   = T(rho=|tau|) at w=1 (BA1's own tier-rule T, unweighted)
  T_star  = T_w at the floor weight (BA1's own weighted_norm 'T_w' field)
  K_rev   = admitted BA1 headline K (reverse route, analytic_disc)
  K_fwd   = admitted BA1 headline K (forward route, weighted_norm, general/telescoped)

  iterated split:  C_split = 2(dbar_0+dbar_ez)(1+2 t_bar)(1+eta_str),
                   eta_str = 32 T_star/(1-32 T_star)
  polymer KP:      C_poly  = 2(dbar_0+dbar_ez)(1+t_bar)(1+eta_far),
                   eta_far = e^{2a} * 4 T_KP * S(q W_c)/(1-4 T_KP),
                   T_KP = 2 T_star, a = 1/1000, W_c = (1/2)(390625/148),
                   S(x) = sum_{d>=1} (24 d^2+8 d+2) x^{-d}  (closed form, exact)

with dbar_0 = dbar_ez = K_rev (reverse-input, the WORST-CASE pair named in
the proposal) or dbar_ez = K_fwd, dbar_0 = q K_fwd (forward-input pair).
`S(x)` is exact rational (Fraction); the only transcendental quantity is
`e^{2a} = e^{1/500}` in the polymer route's `eta_far`, rigorously enclosed
here with Arb (python-flint) and mpmath.iv, reused by import.

This script checks: (1) `t_bar` and `T_star` reproduce BA1's own admitted
values exactly; (2) `eta_str` reproduces the proposal's `49/126095`
exactly; (3) `S(qW_c)` reproduces the proposal's exact fraction; (4) both
routes' worst-case (reverse-input) `C` values reproduce the proposal's
`1.753963e-6` (split) and (via a rigorous Arb ball, since `eta_far` is
transcendental) contain `1.753614e-6` (polymer); (5) the proposal's
headline claim -- worst-case `C ~ 1.754e-6` against the proposed
`4x10^-6` target, margin `~2.28` -- and the rejected `2x10^-6` target
(margin `~1.14`, "do not freeze it") are both reproduced.

Run: `python3 -B bb1_previews.py`
"""
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]

sys.path.insert(0, str(ROOT / "research" / "round32" / "tools"))
import arb_crosscheck as acc  # noqa: E402  (frozen Round32 tool; only arb_of/iv_of are reused)

import flint  # noqa: E402
import mpmath  # noqa: E402

PREC = 256
flint.ctx.prec = PREC
mpmath.mp.prec = PREC
mpmath.iv.prec = PREC


def _exp_expr(x: Q) -> str:
    assert x > 0
    return f"exp({x.numerator})" if x.denominator == 1 else f"exp({x.numerator}/{x.denominator})"


def arb_exp_bounds(x: Q):
    ball = acc.arb_of(_exp_expr(x))
    lo, hi = ball.lower(), ball.upper()

    def to_q(v):
        man, exp = v.man_exp()
        man, exp = int(man), int(exp)
        return Q(man) * Q(2) ** exp if exp >= 0 else Q(man, 2 ** (-exp))

    return to_q(lo), to_q(hi)


def mp_exp_bounds(x: Q):
    iv = acc.iv_of(_exp_expr(x))

    def to_q(m):
        sign, man, exp, _bc = mpmath.mpf(m)._mpf_
        val = Q(int(man)) * Q(2) ** int(exp)
        return -val if sign else val

    return to_q(iv.a), to_q(iv.b)


def find_check(results: dict, cid: str) -> dict:
    for c in results["checks"]:
        if c.get("id") == cid:
            return c
    raise KeyError(cid)


def T_of_rho(rho: Q, gprime_upper: Q) -> Q:
    """BA1's own tier-rule identity: T(rho) = 49 rho/144 / (1-28 rho G'(R)) (reverse report.md line 142)."""
    t1 = Q(49) * rho / 144
    denom = 1 - 28 * rho * gprime_upper
    assert denom > 0
    return t1 / denom


def S_closed_form(r: Q) -> Q:
    """sum_{d>=1} (24 d^2 + 8 d + 2) r^d, exact, for 0 < r < 1 (standard geometric-derivative sums)."""
    assert 0 < r < 1
    sum_d = r / (1 - r) ** 2
    sum_d2 = r * (1 + r) / (1 - r) ** 3
    sum_1 = r / (1 - r)
    return 24 * sum_d2 + 8 * sum_d + 2 * sum_1


def main() -> int:
    checks = []
    all_ok = True

    def record(cid, ok, **fields):
        nonlocal all_ok
        all_ok = all_ok and ok
        checks.append({"id": cid, "passed": bool(ok), **fields})

    tau_cap = Q(1, 10 ** 8)
    R = Q(1, 64)
    q = Q(1, 64)
    ADMITTED_E18_BOUND = Q(8, 7)
    Gprime_R = Q(308) * ADMITTED_E18_BOUND  # = 352, BA1's own admitted upper bound

    # --- 0. Load the admitted BA1 outputs (never a check.py) -------------------------
    fwd = json.loads((ROOT / "research/round33/forward/ba1/output/results.json").read_text())
    rev = json.loads((ROOT / "research/round33/reverse/ba1/output/results.json").read_text())
    ba1_gate = json.loads((ROOT / "research/round33/advisor/ba1-gate.json").read_text())
    fwd_headline = find_check(fwd, "coefficient_difference_headline_pair")
    fwd_floor = find_check(fwd, "coefficient_difference_floor_pair")
    rev_headline = find_check(rev, "headline_pair_met")

    K_rev = Q(rev_headline["K"]["exact"])  # admitted BA1 headline K, reverse route (analytic_disc)
    K_fwd = Q(fwd_headline["K_pair"])  # admitted BA1 headline K, forward route (weighted_norm)
    T_star_admitted = Q(fwd_floor["per_sign"]["+"]["T_w"])  # BA1 floor weighted-norm T_w
    assert ba1_gate["verdict"] == "accepted_within_scope"

    # t_bar = T(rho=|tau|) at w=1 (unweighted); T_star = T(rho) at the floor weight w=390625/148
    t_bar = T_of_rho(tau_cap, Gprime_R)
    T_star = T_of_rho(Q(390625, 148) * tau_cap, Gprime_R)
    ADMITTED_T_BAR = Q(49, 14398580736)
    ADMITTED_T_STAR = Q(49, 4036608)
    record(
        "ba1_inputs_reproduced",
        t_bar == ADMITTED_T_BAR and T_star == ADMITTED_T_STAR and T_star == T_star_admitted
        and K_rev == Q(49, 111790368) and K_fwd == Q(2734375, 12204185915601),
        t_bar=str(t_bar), t_bar_preview=float(t_bar),
        T_star=str(T_star), T_star_preview=float(T_star),
        K_rev=str(K_rev), K_rev_preview=float(K_rev),
        K_fwd=str(K_fwd), K_fwd_preview=float(K_fwd),
        note="t_bar and T_star are both BA1's own T(rho) tier-rule identity (weighted_contraction_arb.py "
             "in this same folder derives and cross-checks that identity against BA1's admitted T_w field); "
             "K_rev/K_fwd are the admitted BA1 headline pair, read from output/results.json, not a check.py",
    )

    # --- 1. Iterated-split route: normalization + straddling ------------------------
    eta_str = 32 * T_star / (1 - 32 * T_star)
    ADMITTED_ETA_STR = Q(49, 126095)
    record(
        "eta_str_reproduced",
        eta_str == ADMITTED_ETA_STR,
        formula="32 T_star/(1-32 T_star)",
        computed=str(eta_str), computed_preview=float(eta_str),
        admitted=str(ADMITTED_ETA_STR), admitted_preview=float(ADMITTED_ETA_STR),
    )

    def C_split(dbar_0: Q, dbar_ez: Q) -> Q:
        return 2 * (dbar_0 + dbar_ez) * (1 + 2 * t_bar) * (1 + eta_str)

    C_split_rev = C_split(K_rev, K_rev)  # worst-case / reverse-input pair
    C_split_fwd = C_split(q * K_fwd, K_fwd)  # forward-input pair
    ADMITTED_C_SPLIT_REV = Q(352765230433, 201124673670833280)
    ADMITTED_C_SPLIT_FWD = Q(255912276541796875, 562095032088559080946176)
    record(
        "C_split_reproduced_both_inputs",
        C_split_rev == ADMITTED_C_SPLIT_REV and C_split_fwd == ADMITTED_C_SPLIT_FWD,
        formula="C_split = 2(dbar_0+dbar_ez)(1+2 t_bar)(1+eta_str)",
        reverse_input_preview=float(C_split_rev), reverse_input_admitted_preview=float(ADMITTED_C_SPLIT_REV),
        forward_input_preview=float(C_split_fwd), forward_input_admitted_preview=float(ADMITTED_C_SPLIT_FWD),
    )

    # --- 2. Polymer/KP route: cardinality weight, far-support sum --------------------
    a = Q(1, 1000)
    T_KP = 2 * T_star
    four_T_KP = 4 * T_KP
    ADMITTED_4TKP = Q(49, 504576)
    W_c = Q(1, 2) * Q(390625, 148)
    x_far = q * W_c  # = 390625/18944
    r_far = 1 / x_far  # = 18944/390625, the geometric ratio S is summed at
    S_val = S_closed_form(r_far)
    ADMITTED_S = Q(99977074261152768, 51346528044814241)
    record(
        "polymer_inputs_reproduced",
        four_T_KP == ADMITTED_4TKP and four_T_KP < a and S_val == ADMITTED_S,
        four_T_KP=str(four_T_KP), four_T_KP_preview=float(four_T_KP), a_preview=float(a),
        x_far="390625/18944", x_far_preview=float(x_far),
        S_exact=str(S_val), S_preview=float(S_val),
        admitted_S=str(ADMITTED_S), admitted_S_preview=float(ADMITTED_S),
        note="S(x)=sum_{d>=1}(24d^2+8d+2)x^-d has a closed rational form (geometric-derivative sums), so "
             "it is reproduced exactly in Fraction arithmetic -- no Arb needed for this quantity",
    )

    # eta_far needs e^{2a} = e^{1/500}, the one transcendental input; enclose with Arb/mpmath.
    two_a = 2 * a
    e2a_lo_arb, e2a_hi_arb = arb_exp_bounds(two_a)
    e2a_lo_mp, e2a_hi_mp = mp_exp_bounds(two_a)

    def eta_far_bounds(e2a_lo: Q, e2a_hi: Q):
        num_lo = e2a_lo * four_T_KP * S_val
        num_hi = e2a_hi * four_T_KP * S_val
        denom = 1 - four_T_KP
        return num_lo / denom, num_hi / denom

    eta_far_lo_arb, eta_far_hi_arb = eta_far_bounds(e2a_lo_arb, e2a_hi_arb)
    eta_far_lo_mp, eta_far_hi_mp = eta_far_bounds(e2a_lo_mp, e2a_hi_mp)
    record(
        "eta_far_enclosed",
        eta_far_lo_arb <= eta_far_hi_arb and abs(float(eta_far_hi_arb) - 1.895e-4) < 2e-7
        and abs(float(eta_far_hi_mp) - 1.895e-4) < 2e-7,
        formula="eta_far = e^{2a} * 4 T_KP * S(q W_c) / (1-4 T_KP), a=1/1000",
        eta_far_arb_ball=[str(eta_far_lo_arb), str(eta_far_hi_arb)],
        eta_far_arb_preview=[float(eta_far_lo_arb), float(eta_far_hi_arb)],
        eta_far_mpmath_preview=[float(eta_far_lo_mp), float(eta_far_hi_mp)],
        proposal_quoted_preview=1.895e-4,
    )

    def C_poly_bounds(dbar_0: Q, dbar_ez: Q, eta_far_lo: Q, eta_far_hi: Q):
        base = 2 * (dbar_0 + dbar_ez) * (1 + t_bar)
        return base * (1 + eta_far_lo), base * (1 + eta_far_hi)

    C_poly_rev_lo, C_poly_rev_hi = C_poly_bounds(K_rev, K_rev, eta_far_lo_arb, eta_far_hi_arb)
    C_poly_fwd_lo, C_poly_fwd_hi = C_poly_bounds(q * K_fwd, K_fwd, eta_far_lo_arb, eta_far_hi_arb)
    record(
        "C_poly_enclosed_both_inputs",
        C_poly_rev_lo <= C_poly_rev_hi
        and abs(float(C_poly_rev_hi) - 1.753614e-6) < 5e-10
        and abs(float(C_poly_fwd_hi) - 4.55192e-7) < 5e-11,
        formula="C_poly = 2(dbar_0+dbar_ez)(1+t_bar)(1+eta_far)",
        reverse_input_ball_preview=[float(C_poly_rev_lo), float(C_poly_rev_hi)],
        forward_input_ball_preview=[float(C_poly_fwd_lo), float(C_poly_fwd_hi)],
        proposal_quoted_reverse_preview=1.753614e-6,
        proposal_quoted_forward_preview=4.55192e-7,
    )

    # --- 3. Worst-case C, target margin, and the rejected 2e-6 target ----------------
    worst_C = max(C_split_rev, C_poly_rev_hi)  # both routes' reverse-input (worst-case) value
    TARGET_PROPOSED = Q(4, 10 ** 6)
    TARGET_REJECTED = Q(2, 10 ** 6)
    margin_proposed = TARGET_PROPOSED / worst_C
    margin_rejected = TARGET_REJECTED / worst_C
    record(
        "worst_case_C_and_target_margins",
        abs(float(worst_C) - 1.754e-6) < 1e-9
        and abs(float(margin_proposed) - 2.2806) < 2e-3
        and worst_C < TARGET_PROPOSED
        and abs(float(margin_rejected) - 1.14) < 2e-2
        and worst_C < TARGET_REJECTED,  # 2e-6 target is NOT violated either, but its margin is thin
        worst_case_C_is=("C_split, reverse BA1 input" if C_split_rev >= C_poly_rev_hi
                          else "C_poly, reverse BA1 input"),
        worst_C_preview=float(worst_C),
        target_proposed="4e-6", margin_proposed_preview=float(margin_proposed),
        target_rejected="2e-6", margin_rejected_preview=float(margin_rejected),
        note="bb-targets-proposal.md section 7 recommends freezing 4e-6 (margin ~2.28) and explicitly "
             "declines to freeze 2e-6 ('margin of only about 1.14. Do not freeze it') though even that "
             "smaller target is not technically violated by this preview -- both figures are reproduced",
    )

    # --- 4. c_site and the nested-telescoping C' (BB2 item 1), for completeness -----
    C_prime = C_split_rev / (1 - q)
    c_site = C_prime / 2
    ADMITTED_C_PRIME = Q(50395032919, 28283157234960930)
    record(
        "c_site_and_nested_C_prime",
        C_prime == ADMITTED_C_PRIME,
        formula="C' = C_split/(1-q) [BB2 item 1, nested_telescoping]; c_site = C'/2",
        C_prime_preview=float(C_prime), admitted_C_prime_preview=float(ADMITTED_C_PRIME),
        c_site_preview=float(c_site),
        proposal_quoted_C_prime=1.781804e-6, proposal_quoted_c_site=8.909018e-7,
    )

    report = {
        "tool": "bb1_previews",
        "status": "preview_only_zero_research_loops_not_a_contract_or_gate",
        "libraries": {"python-flint": flint.__version__, "mpmath": mpmath.__version__},
        "precision_bits": PREC,
        "all_passed": all_ok,
        "checks": checks,
        "interpretation": "Reproduction, with one added Arb/mpmath rigorous enclosure (e^{2a} in the "
                           "polymer route), of the BB1 marginal-locality preview arithmetic in "
                           "research/round33/experts/modern/bb-targets-proposal.md section 7; a preview "
                           "of a proposed target, never evidence, never a BB1 admission (BB1 has not been "
                           "produced or gated in Round33 sub-round 1).",
    }
    print(json.dumps(report, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
