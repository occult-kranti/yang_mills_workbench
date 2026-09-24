#!/usr/bin/env python3
"""BA2 directed-rounding reconciliation -- Arb enclosure of the 0.67% gap (preview only).

Round33, sub-round 1, modern (Penrose/Feynman) lens, research assistant/coder
"assistant-1". **This script counts zero research loops.** It is a preview
and cross-check only, per `research/round33/experts/modern/loop2-response.md`
section 3 item 2. It never imports a producer `check.py`; only
`research/round33/advisor/ba2-gate.json`, both producers' `report.md`/
`output/results.json`, and `research/round33/skeptic/ba2-independent-derivation.md`
are read as text/JSON, for comparison. `python-flint` (Arb) and `mpmath.iv`
are reused by import (never reimplemented) for the one transcendental
quantity here (`exp`); every other quantity is an exact `fractions.Fraction`.

Background (all at the frozen cap `|tau| = 10^-8`, window `|theta| <= 8`,
i.e. `U = theta/8 = 1`):
  - **Forward** (admitted `K_cmp`, route `duhamel_inner_f1`), from
    `research/round33/forward/ba2/report.md` line 195:
      `K_cmp^fwd(tau) = 254016 tau^2 / (1 - 338688|tau|)`
    using the bound `e^y-1-y <= y^2/2 * 1/(1-y/3)`-style remainder
    (`Lambda(U) <= 2||Phi||_F U^2/(1-vU/3)`).
  - **Reverse** (admitted `K'_cmp`, route `duhamel_inner_f2`), from
    `research/round33/reverse/ba2/report.md` lines 33, 170-172:
      `K_cmp^rev(tau) = 148176 tau^2 E_up(592704|tau|)`,
      `E_up(y) = 1 + y/3 + y^2/(12(1-y/5))` (a rational upper bound of
      `E(y) = 2(e^y-1-y)/y^2`).
  - **Modern loop-1 preview** (never admitted, from
    `research/round33/experts/modern/loop2-response.md` section 2):
      `M(tau,theta) = 3969 tau^2 theta^2 e^{127008|tau||theta|}`,
    which uses the cruder remainder bound `e^x-1-x <= (x^2/2) e^x`.

This script (1) reproduces the forward and reverse closed forms exactly in
`Fraction` arithmetic and checks them against the admitted
`research/round33/advisor/ba2-gate.json` numbers; (2) rigorously encloses
the modern form with Arb/mpmath (the only place `exp` is transcendental);
(3) derives and checks, in closed form, the exact identity
`M / K_cmp^fwd = e^x (1 - x/3)` at `x = 127008|tau||theta| = vU`, and
evaluates it with Arb to confirm the ~0.67% gap the BA2 skeptic recorded
in `research/round33/skeptic/ba2-independent-derivation.md` section 9;
(4) recomputes the exact `tau -> tau/100` ratios for both admitted routes
and checks they fall in the contract's `[9500, 10500]` bracket; (5) checks
the reverse producer's own claim that `E_up(y) >= E(y)` at its working
point, via a rigorous Arb/mpmath enclosure of `E(y)`.

Run: `python3 -B ba2_directed_reconciliation.py`
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


def E_up(y: Q) -> Q:
    """Reverse producer's rational upper bound of E(y)=2(e^y-1-y)/y^2 (report.md line 33/164)."""
    return 1 + y / 3 + y ** 2 / (12 * (1 - y / 5))


def K_cmp_forward(tau: Q) -> Q:
    return Q(254016) * tau ** 2 / (1 - 338688 * abs(tau))


def K_cmp_reverse(tau: Q, U: Q = Q(1)) -> Q:
    return Q(148176) * tau ** 2 * U ** 2 * E_up(592704 * abs(tau) * U)


def main() -> int:
    checks = []
    all_ok = True

    def record(cid, ok, **fields):
        nonlocal all_ok
        all_ok = all_ok and ok
        checks.append({"id": cid, "passed": bool(ok), **fields})

    tau = Q(1, 10 ** 8)
    theta = Q(8)
    U = theta / 8
    assert U == 1

    ADMITTED_K_FWD = Q(3969, 155720800000000)
    ADMITTED_K_REV = Q(452554889222515527, 30481402343750000000000000000)

    # --- 1. Reproduce forward and reverse closed forms exactly -----------------------
    fwd_val = K_cmp_forward(tau)
    rev_val = K_cmp_reverse(tau, U)
    record(
        "forward_closed_form_reproduced",
        fwd_val == ADMITTED_K_FWD,
        formula="254016 tau^2/(1-338688|tau|)",
        computed=str(fwd_val), computed_preview=float(fwd_val),
        admitted=str(ADMITTED_K_FWD), admitted_preview=float(ADMITTED_K_FWD),
    )
    record(
        "reverse_closed_form_reproduced",
        rev_val == ADMITTED_K_REV,
        formula="148176 tau^2 U^2 E_up(592704|tau|U), E_up(y)=1+y/3+y^2/(12(1-y/5))",
        computed=str(rev_val), computed_preview=float(rev_val),
        admitted=str(ADMITTED_K_REV), admitted_preview=float(ADMITTED_K_REV),
    )

    # --- 2. Modern loop-1 preview: rigorous Arb/mpmath enclosure of exp -------------
    x = Q(127008) * abs(tau) * theta  # = vU at the cap; equals 3969/390625
    assert x == Q(3969, 390625)
    arb_lo, arb_hi = arb_exp_bounds(x)
    mp_lo, mp_hi = mp_exp_bounds(x)
    M_prefactor = Q(3969) * tau ** 2 * theta ** 2  # = 254016 tau^2
    assert M_prefactor == Q(254016) * tau ** 2
    M_lo_arb, M_hi_arb = M_prefactor * arb_lo, M_prefactor * arb_hi
    M_lo_mp, M_hi_mp = M_prefactor * mp_lo, M_prefactor * mp_hi
    record(
        "modern_loop1_form_enclosed",
        arb_lo <= arb_hi and mp_lo <= mp_hi
        and M_lo_arb <= M_hi_arb and M_lo_mp <= M_hi_mp
        and abs(float(M_hi_arb) - 2.5661e-11) < 2e-14,
        x="3969/390625", x_preview=float(x),
        formula="3969 tau^2 theta^2 e^{127008|tau||theta|} = 254016 tau^2 e^x",
        M_arb_ball=[str(M_lo_arb), str(M_hi_arb)], M_arb_preview=[float(M_lo_arb), float(M_hi_arb)],
        M_mpmath_ball=[str(M_lo_mp), str(M_hi_mp)], M_mpmath_preview=[float(M_lo_mp), float(M_hi_mp)],
        loop2_response_quoted_preview=2.5661e-11,
        note="rigorous enclosure agrees with the modern loop2-response.md hand-evaluation "
             "'3969*(10^-8)^2*64*exp(127008*10^-8*8) ~ 2.5661e-11' to its quoted digits",
    )

    # --- 3. Exact identity M/K_cmp^fwd = e^x (1-x/3), evaluated with Arb -------------
    # K_cmp^fwd = 254016 tau^2/(1-x/3) since x/3 = 338688|tau| at U=1; M = 254016 tau^2 e^x.
    assert 1 - 338688 * abs(tau) == 1 - x / 3
    ratio_lo_arb = arb_lo * (1 - x / 3)
    ratio_hi_arb = arb_hi * (1 - x / 3)
    ratio_lo_mp = mp_lo * (1 - x / 3)
    ratio_hi_mp = mp_hi * (1 - x / 3)
    # cross-check against the actual quotient of the two admitted/reproduced numbers directly
    ratio_direct_lo = M_lo_arb / ADMITTED_K_FWD
    ratio_direct_hi = M_hi_arb / ADMITTED_K_FWD
    SKEPTIC_RATIO = Q("10067939", ) * Q(1, 10 ** 7)  # skeptic quotes ratio ~1.0067939 (informal)
    gap_pct_lo = (ratio_lo_arb - 1) * 100
    gap_pct_hi = (ratio_hi_arb - 1) * 100
    record(
        "directed_gap_identity_e_x_times_1_minus_x_over_3",
        ratio_lo_arb <= ratio_hi_arb
        and abs(float(ratio_hi_arb) - float(SKEPTIC_RATIO)) < 2e-4
        and ratio_direct_lo <= ratio_direct_hi
        and Q(67, 10000) < gap_pct_lo / 100 < Q(70, 10000),
        identity="M/K_cmp^fwd = e^x (1-x/3) exactly, since both share the common prefactor 254016 tau^2 "
                 "and differ only in the remainder-bounding step (e^x vs 1/(1-x/3))",
        ratio_ball_arb=[str(ratio_lo_arb), str(ratio_hi_arb)],
        ratio_preview_arb=[float(ratio_lo_arb), float(ratio_hi_arb)],
        ratio_ball_mpmath_preview=[float(ratio_lo_mp), float(ratio_hi_mp)],
        ratio_via_direct_quotient_preview=[float(ratio_direct_lo), float(ratio_direct_hi)],
        gap_percent_preview=[float(gap_pct_lo), float(gap_pct_hi)],
        skeptic_quoted_ratio=1.0067939,
        skeptic_quoted_gap_percent=["+0.679% (relative to skeptic/forward)", "0.675% (relative to modern)"],
        note="independently derived, exact algebraic identity (not copied from the skeptic file); its "
             "Arb-evaluated numeric value reproduces the BA2 skeptic's recorded ~0.67% gap attribution "
             "(research/round33/skeptic/ba2-independent-derivation.md section 9) to 4 significant figures",
    )

    # --- 4. tau -> tau/100 ratios, exact Fraction (no Arb needed: both routes rational) -
    tau_100 = tau / 100
    fwd_ratio = K_cmp_forward(tau) / K_cmp_forward(tau_100)
    rev_ratio = K_cmp_reverse(tau, U) / K_cmp_reverse(tau_100, U)
    BRACKET = (Q(9500), Q(10500))
    ADMITTED_FWD_RATIO = Q(1953058850, 194651)  # skeptic table, "forward comparison, closed"
    ADMITTED_REV_RATIO = Q(38176688920663121234473000000, 3810205403940325763421973)  # reverse report.md line 187
    record(
        "tau_over_100_ratios",
        fwd_ratio == ADMITTED_FWD_RATIO and rev_ratio == ADMITTED_REV_RATIO
        and BRACKET[0] <= fwd_ratio <= BRACKET[1] and BRACKET[0] <= rev_ratio <= BRACKET[1],
        forward_ratio_exact=str(fwd_ratio), forward_ratio_preview=float(fwd_ratio),
        reverse_ratio_exact=str(rev_ratio), reverse_ratio_preview=float(rev_ratio),
        bracket=["9500", "10500"],
        note="both are quadratic-in-tau closed forms (E_up is rational), so the tau/100 ratio is exact "
             "Fraction arithmetic with no Arb enclosure needed; both fall inside the contract's [9500,10500]",
    )

    # --- 5. Reverse producer's own E_up >= E claim, at its working point ------------
    y = Q(9261, 1562500)  # = 592704*10^-8, reverse report.md line 164
    e_up_y = E_up(y)
    ADMITTED_E_UP_Y = Q(48866741088707, 48770243750000)
    assert e_up_y == ADMITTED_E_UP_Y
    # E(y) = 2(e^y-1-y)/y^2, evaluated rigorously via an Arb ball for e^y
    ey_lo, ey_hi = arb_exp_bounds(y)
    E_lo = 2 * (ey_lo - 1 - y) / y ** 2
    E_hi = 2 * (ey_hi - 1 - y) / y ** 2
    my_ey_lo, my_ey_hi = mp_exp_bounds(y)
    E_mp_lo = 2 * (my_ey_lo - 1 - y) / y ** 2
    E_mp_hi = 2 * (my_ey_hi - 1 - y) / y ** 2
    record(
        "reverse_E_up_dominates_E_at_working_point",
        E_hi <= e_up_y and E_mp_hi <= e_up_y and E_lo <= E_hi,
        y="9261/1562500", y_preview=float(y),
        E_up_exact=str(e_up_y), E_up_preview=float(e_up_y),
        E_arb_ball_preview=[float(E_lo), float(E_hi)],
        E_mpmath_ball_preview=[float(E_mp_lo), float(E_mp_hi)],
        gap_preview=float(e_up_y - E_hi),
        note="reverse report.md line 164 quotes 'the directed exact-exponential enclosure of E "
             "(1.00197861095729...) lies below E_up, by about 7e-13'; both independent libraries confirm "
             "E_up(y) is a valid (and very tight) upper bound of the true E(y) at this y",
    )

    # --- 6. Read the gate and both producers' report.md / results.json --------------
    ba2_gate = json.loads((ROOT / "research/round33/advisor/ba2-gate.json").read_text())
    fwd_results = json.loads((ROOT / "research/round33/forward/ba2/output/results.json").read_text())
    rev_results = json.loads((ROOT / "research/round33/reverse/ba2/output/results.json").read_text())
    gate_decision = ba2_gate["decision"]
    record(
        "gate_and_producer_results_cross_read",
        ba2_gate["verdict"] == "accepted_within_scope"
        and "3969/155720800000000" in gate_decision
        and "452554889222515527/30481402343750000000000000000" in gate_decision
        and isinstance(fwd_results.get("checks"), list) and isinstance(rev_results.get("checks"), list),
        ba2_gate_verdict=ba2_gate["verdict"],
        forward_checks_count=len(fwd_results["checks"]),
        reverse_checks_count=len(rev_results["checks"]),
        note="the admitted forward and reverse K_cmp values used above appear verbatim in the gate's "
             "decision text; both producers' results.json are read only for their check counts here",
    )

    report = {
        "tool": "ba2_directed_reconciliation",
        "status": "preview_only_zero_research_loops",
        "libraries": {"python-flint": flint.__version__, "mpmath": mpmath.__version__},
        "precision_bits": PREC,
        "all_passed": all_ok,
        "checks": checks,
        "interpretation": "Independent Arb/mpmath and exact-Fraction reconciliation of the BA2 forward, "
                           "reverse and modern-loop-1 dynamics-comparison coefficients; a comparison, "
                           "never an admission decision.",
    }
    print(json.dumps(report, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
