#!/usr/bin/env python3
"""BA1 weighted contraction inequalities -- Arb/mpmath enclosures (preview only).

Round33, sub-round 1, modern (Penrose/Feynman) lens, research assistant/coder
"assistant-1". **This script counts zero research loops.** It is a preview
and cross-check only, per `research/round33/experts/modern/loop2-response.md`
section 3 item 1. `python-flint` (Arb ball arithmetic) and `mpmath.iv`
(interval arithmetic) are independent, already-frozen open-source libraries,
reused here BY IMPORT (never reimplemented, never modified). This script
never imports a producer `check.py`; the only round-tool import is
`research/round32/tools/arb_crosscheck.py`'s `arb_of`/`iv_of` helpers, which
are reused for their exponential evaluation exactly as published there.
Nothing here changes any verdict; the admitted numbers below were already
decided by exact `fractions.Fraction` arithmetic in the frozen
`research/round33/forward/ba1/check.py` and `research/round33/reverse/ba1/check.py`,
which are never opened or imported here -- only the ADMITTED
`output/results.json` files and `research/round33/advisor/ba1-gate.json`
are read, for comparison.

What this checks (BA1 item 1 of the loop2-response task list):
  1. The AM2 majorant `G(t) = 16 e^{8t}(1+10t)` and its derivative
     `G'(t) = 16 e^{8t}(18+80t)` at `t = R = 1/64`, independently enclosed
     with a rigorous `e^{1/8}` ball (Arb) and interval (mpmath), confirming
     the admitted directed-rounding bound `e^{1/8} <= 8/7` (used throughout
     BA1's `check.py` files per their own `exact_arithmetic_admission` note)
     is a valid upper bound, and that the admitted `G(R)_upper = 148/7` and
     `G'(R)_upper = 352` safely contain the tighter Arb/mpmath value.
  2. The weighted ball self-map `J_0 w G(R) <= R` and the weighted Lipschitz
     constant `J_0 w G'(R)`, at the two weights BA1 actually uses:
     `w = 64` (headline) and `w = 390625/148` (floor, `= 1/(37888|tau|)` at
     the cap), confirming the admitted exact values
     (`selfmap = 148/390625`, `2464/390625`; `1/64`, `77/296`) contain the
     Arb/mpmath ball computed independently from the same `G`, `G'`.
  3. The two analytic-disc `K` values (`rho = 64|tau|` headline,
     `rho = 1/37888 = tau_star` floor) via the disc/Schwarz-lemma formula
     `T(rho) = t_1(rho)/(1 - 28 rho G'(R))`, `K = 2 T(rho)`
     (`research/round33/reverse/ba1/report.md` lines 55, 142), confirming
     containment of the admitted `K = 49/111790368` (headline) and
     `K = 49/2018304` (floor).
  4. Cross-reads `research/round33/advisor/ba1-gate.json` and both
     producers' `output/results.json` headline/floor entries, confirming the
     admitted numbers used above actually appear there (both routes:
     reverse `analytic_disc` and forward `weighted_norm`).

Run: `python3 -B weighted_contraction_arb.py`
"""
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]  # .../research/round33/experts/modern/assistant-1/<file> -> repo root

sys.path.insert(0, str(ROOT / "research" / "round32" / "tools"))
import arb_crosscheck as acc  # noqa: E402  (frozen Round32 tool; only arb_of/iv_of are reused)

import flint  # noqa: E402
import mpmath  # noqa: E402

PREC = 256
flint.ctx.prec = PREC
mpmath.mp.prec = PREC
mpmath.iv.prec = PREC


def _exp_expr(x: Q) -> str:
    assert x > 0, "this script only ever encloses exp of positive rationals"
    return f"exp({x.numerator})" if x.denominator == 1 else f"exp({x.numerator}/{x.denominator})"


def arb_exp_upper(x: Q) -> Q:
    """Exact rational UPPER bound of exp(x), from an Arb ball's own dyadic upper() (no decimal slack)."""
    ball = acc.arb_of(_exp_expr(x)).upper()
    man, exp = ball.man_exp()
    man, exp = int(man), int(exp)
    return Q(man) * Q(2) ** exp if exp >= 0 else Q(man, 2 ** (-exp))


def arb_exp_lower(x: Q) -> Q:
    ball = acc.arb_of(_exp_expr(x)).lower()
    man, exp = ball.man_exp()
    man, exp = int(man), int(exp)
    return Q(man) * Q(2) ** exp if exp >= 0 else Q(man, 2 ** (-exp))


def _mpf_to_fraction(m) -> Q:
    sign, man, exp, _bc = m._mpf_
    val = Q(int(man)) * Q(2) ** int(exp)
    return -val if sign else val


def mp_exp_upper(x: Q) -> Q:
    iv = acc.iv_of(_exp_expr(x))
    return _mpf_to_fraction(mpmath.mpf(iv.b))


def mp_exp_lower(x: Q) -> Q:
    iv = acc.iv_of(_exp_expr(x))
    return _mpf_to_fraction(mpmath.mpf(iv.a))


def find_check(results: dict, cid: str) -> dict:
    for c in results["checks"]:
        if c.get("id") == cid:
            return c
    raise KeyError(cid)


def main() -> int:
    checks = []
    all_ok = True

    def record(cid, ok, **fields):
        nonlocal all_ok
        all_ok = all_ok and ok
        checks.append({"id": cid, "passed": bool(ok), **fields})

    R = Q(1, 64)
    ADMITTED_E18_BOUND = Q(8, 7)  # BA1 check.py's own directed rounding, both forward and reverse
    ADMITTED_G_R = Q(148, 7)
    ADMITTED_GPRIME_R = Q(352)

    # --- 1. e^{1/8} enclosure, independent of the admitted rounding -----------------
    e18_arb_hi = arb_exp_upper(Q(1, 8))
    e18_arb_lo = arb_exp_lower(Q(1, 8))
    e18_mp_hi = mp_exp_upper(Q(1, 8))
    e18_mp_lo = mp_exp_lower(Q(1, 8))
    record(
        "e18_enclosure_below_admitted_bound",
        e18_arb_hi <= ADMITTED_E18_BOUND and e18_mp_hi <= ADMITTED_E18_BOUND and e18_arb_lo <= e18_arb_hi,
        arb_upper=str(e18_arb_hi), arb_upper_preview=float(e18_arb_hi),
        mpmath_iv_upper=str(e18_mp_hi), mpmath_iv_upper_preview=float(e18_mp_hi),
        admitted_bound="8/7", admitted_bound_preview=float(ADMITTED_E18_BOUND),
        slack_arb_preview=float(ADMITTED_E18_BOUND - e18_arb_hi),
        note="BA1 forward+reverse check.py record 'directed upward enclosure e^{1/8} at most 8/7'; "
             "both independent libraries confirm 8/7 is a valid (non-tight) upper bound",
    )

    # G(R) = 16 e^{1/8}(1+10/64) = (37/2) e^{1/8}; G'(R) = 16 e^{1/8}(18+80/64) = 308 e^{1/8}
    G_R_from_admitted_e18 = Q(37, 2) * ADMITTED_E18_BOUND
    Gprime_R_from_admitted_e18 = Q(308) * ADMITTED_E18_BOUND
    record(
        "G_and_Gprime_reproduce_admitted_exactly_from_8_over_7",
        G_R_from_admitted_e18 == ADMITTED_G_R and Gprime_R_from_admitted_e18 == ADMITTED_GPRIME_R,
        G_R="148/7", Gprime_R="352",
        formula="G(R)=(37/2)e^{1/8}<=(37/2)(8/7)=148/7; G'(R)=308e^{1/8}<=308(8/7)=352",
    )

    G_R_arb = Q(37, 2) * e18_arb_hi
    G_R_mp = Q(37, 2) * e18_mp_hi
    Gprime_R_arb = Q(308) * e18_arb_hi
    Gprime_R_mp = Q(308) * e18_mp_hi
    record(
        "G_and_Gprime_arb_ball_below_admitted",
        G_R_arb <= ADMITTED_G_R and G_R_mp <= ADMITTED_G_R
        and Gprime_R_arb <= ADMITTED_GPRIME_R and Gprime_R_mp <= ADMITTED_GPRIME_R,
        G_R_arb_preview=float(G_R_arb), G_R_mp_preview=float(G_R_mp),
        Gprime_R_arb_preview=float(Gprime_R_arb), Gprime_R_mp_preview=float(Gprime_R_mp),
        admitted_G_R_preview=float(ADMITTED_G_R), admitted_Gprime_R_preview=float(ADMITTED_GPRIME_R),
        note="independent Arb/mpmath e^{1/8} ball is tighter than 8/7, so G(R)/G'(R) computed from it "
             "are strictly below the admitted rational bounds -- containment confirmed with margin to spare",
    )

    # --- 2. Weighted self-map and Lipschitz constant, both admitted weights ----------
    J0 = Q(7, 25000000)  # BA1 premise J_0 = 28*tau_cap, tau_cap = 1e-8 (checked below)
    tau_cap = Q(1, 10 ** 8)
    assert J0 == 28 * tau_cap

    weight_targets = [
        ("headline", Q(64), Q(148, 390625), Q(2464, 390625)),
        ("floor", Q(390625, 148), Q(1, 64), Q(77, 296)),
    ]
    for label, w, admitted_selfmap, admitted_lipschitz in weight_targets:
        selfmap_from_admitted = J0 * w * G_R_from_admitted_e18
        lipschitz_from_admitted = J0 * w * Gprime_R_from_admitted_e18
        selfmap_arb = J0 * w * G_R_arb
        selfmap_mp = J0 * w * G_R_mp
        lipschitz_arb = J0 * w * Gprime_R_arb
        lipschitz_mp = J0 * w * Gprime_R_mp
        record(
            f"weighted_contraction_{label}_w_{w}",
            selfmap_from_admitted == admitted_selfmap
            and lipschitz_from_admitted == admitted_lipschitz
            and selfmap_arb <= admitted_selfmap and selfmap_mp <= admitted_selfmap
            and lipschitz_arb <= admitted_lipschitz and lipschitz_mp <= admitted_lipschitz,
            w=str(w), w_preview=float(w),
            selfmap_reproduced_exactly=str(selfmap_from_admitted),
            lipschitz_reproduced_exactly=str(lipschitz_from_admitted),
            selfmap_arb_preview=float(selfmap_arb), selfmap_mp_preview=float(selfmap_mp),
            lipschitz_arb_preview=float(lipschitz_arb), lipschitz_mp_preview=float(lipschitz_mp),
            admitted_selfmap=str(admitted_selfmap), admitted_lipschitz=str(admitted_lipschitz),
            statement="self-map J_0 w G(R) <= R and Lipschitz J_0 w G'(R) < 1",
            selfmap_at_most_R=(selfmap_arb <= R and selfmap_mp <= R),
        )

    # --- 3. Analytic-disc K values (Schwarz-lemma route) -----------------------------
    def T_of_rho(rho: Q, gprime_upper: Q) -> Q:
        t1 = Q(49) * rho / 144
        denom = 1 - 28 * rho * gprime_upper
        assert denom > 0, "disc radius crosses the contraction boundary"
        return t1 / denom

    rho_headline = 64 * tau_cap  # = 1/1562500, matches reverse ba1 output disc_contraction_rechecked
    rho_floor = Q(1, 37888)  # tau_star, independent of tau

    disc_targets = [
        ("headline", rho_headline, Q(49, 111790368)),
        ("floor", rho_floor, Q(49, 2018304)),
    ]
    for label, rho, admitted_K in disc_targets:
        K_from_admitted = 2 * T_of_rho(rho, Gprime_R_from_admitted_e18)
        K_arb = 2 * T_of_rho(rho, Gprime_R_arb)
        K_mp = 2 * T_of_rho(rho, Gprime_R_mp)
        record(
            f"analytic_disc_K_{label}",
            K_from_admitted == admitted_K and K_arb <= admitted_K and K_mp <= admitted_K,
            rho=str(rho), rho_preview=float(rho),
            K_reproduced_exactly=str(K_from_admitted),
            K_arb_preview=float(K_arb), K_mp_preview=float(K_mp),
            admitted_K=str(admitted_K), admitted_K_preview=float(admitted_K),
            formula="T(rho)=49 rho/144 / (1-28 rho G'(R)); K=2 T(rho)",
        )

    # --- 4. Cross-read the gate and both producers' results.json ---------------------
    ba1_gate = json.loads((ROOT / "research/round33/advisor/ba1-gate.json").read_text())
    fwd = json.loads((ROOT / "research/round33/forward/ba1/output/results.json").read_text())
    rev = json.loads((ROOT / "research/round33/reverse/ba1/output/results.json").read_text())

    rev_headline = find_check(rev, "headline_pair_met")
    rev_floor = find_check(rev, "floor_pair_met")
    fwd_headline = find_check(fwd, "coefficient_difference_headline_pair")
    fwd_floor = find_check(fwd, "coefficient_difference_floor_pair")

    rev_headline_K = Q(rev_headline["K"]["exact"])
    rev_floor_K = Q(rev_floor["K"]["exact"])
    fwd_headline_K = Q(fwd_headline["K_pair"])
    fwd_floor_K = Q(fwd_floor["K_pair"])

    gate_decision = ba1_gate["decision"]
    gate_verdict = ba1_gate["verdict"]

    record(
        "gate_and_producer_headlines_cross_read",
        gate_verdict == "accepted_within_scope"
        and rev_headline_K == Q(49, 111790368)
        and rev_floor_K == Q(49, 2018304)
        and fwd_headline_K == Q(2734375, 12204185915601)
        and fwd_floor_K == Q(708203125, 43148545682688)
        and "49/111790368" in gate_decision
        and "2734375/12204185915601" in gate_decision
        and "49/2018304" in gate_decision
        and "708203125/43148545682688" in gate_decision,
        ba1_gate_verdict=gate_verdict,
        reverse_headline_K=str(rev_headline_K), reverse_floor_K=str(rev_floor_K),
        forward_headline_K_weighted_norm=str(fwd_headline_K), forward_floor_K_weighted_norm=str(fwd_floor_K),
        note="the reverse analytic_disc K values (reproduced above via Arb/mpmath) are the headline/floor "
             "admitted numbers; the forward weighted_norm route gives smaller, separately-certified K values "
             "for the same pairs -- both routes and both numbers are named verbatim in the gate's decision text",
    )

    # Also confirm the forward weighted_norm route independently, at the SAME weights as section 2,
    # via the general fixed-point/self-consistency identity T(rho)=w t1 /(1 - J w G'(R)) with J=28|tau|,
    # w=rho/|tau| -- i.e. exactly the forward's own tier_label_rule, re-derived with the Arb G'(R) ball.
    for label, w, admitted_K in [("headline", Q(64), fwd_headline_K), ("floor", Q(390625, 148), fwd_floor_K)]:
        t1_w = Q(49) * w / 144 * tau_cap  # = w * t1(|tau|), t1(|tau|)=49|tau|/144
        denom_from_admitted = 1 - J0 * w * Gprime_R_from_admitted_e18
        denom_arb = 1 - J0 * w * Gprime_R_arb
        T_from_admitted = t1_w / denom_from_admitted
        T_arb = t1_w / denom_arb
        fwd_side = find_check(fwd, "coefficient_difference_headline_pair" if label == "headline"
                               else "coefficient_difference_floor_pair")
        fwd_T_w = Q(fwd_side["per_sign"]["+"]["T_w"])
        record(
            f"weighted_norm_route_{label}_self_consistency",
            T_from_admitted == fwd_T_w and T_from_admitted <= admitted_K and T_arb <= admitted_K,
            w=str(w), T_reproduced_exactly=str(T_from_admitted), T_arb_preview=float(T_arb),
            forward_T_w_field=str(fwd_T_w),
            admitted_forward_K=str(admitted_K), admitted_forward_K_preview=float(admitted_K),
            note="T(rho)=w t1/(1-J w G'(R)) reproduces the forward producer's own published T_w field exactly "
                 "(the forward report's 'tier rule' identity, reverse report.md line 142); T_w is one step short "
                 "of the forward's fully telescoped K_pair, so containment against admitted_forward_K has margin",
        )

    report = {
        "tool": "weighted_contraction_arb",
        "status": "preview_only_zero_research_loops",
        "libraries": {"python-flint": flint.__version__, "mpmath": mpmath.__version__},
        "precision_bits": PREC,
        "all_passed": all_ok,
        "checks": checks,
        "interpretation": "Containment of independent Arb/mpmath rigorous enclosures inside the exact "
                           "rational bounds admitted by the BA1 gate and both BA1 producers; a comparison, "
                           "never an admission decision.",
    }
    print(json.dumps(report, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
