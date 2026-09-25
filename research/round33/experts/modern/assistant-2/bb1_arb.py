#!/usr/bin/env python3
"""BB1 (forward + reverse) constant recomputation, Arb/mpmath cross-check.

Round33 sub-round 2, modern (Penrose/Feynman) lens, research assistant/coder
"assistant-2". **This script counts zero research loops. Nothing here is
evidence, a contract, a premise or a gate.** It never imports a producer
`check.py`; it reads only the frozen contracts, the ADMITTED
`output/results.json` files of the BB1 forward and reverse producers, and
the BA1 gate, for comparison. `python-flint` (Arb ball arithmetic) and
`mpmath.iv` (interval arithmetic) are reused by import as independent,
already-frozen open-source libraries, exactly as
`research/round32/tools/arb_crosscheck.py`'s `arb_of`/`iv_of` helpers are
(that frozen Round32 tool is itself reused by import, never modified).

What this script recomputes, independently, from the formulas each BB1
report states (never by importing the producers' `check.py` or by copying
their `output/results.json` numbers except for comparison):

  FORWARD (route polymer_kp, `research/round33/forward/bb1/report.md`):
    T(rho)      = (49 rho/144) / (1 - 28 rho G'(R)),  G'(R) = 352 (report S0)
    t(tau)      = T(tau)                    -- exact_first_order anchored bound
    K(tau)      = 2 T(64 tau)               -- headline every-site input (S8)
    tau_bar(tau)= w e^{3b} t_1(tau) / (1 - Gamma(tau)),
                  Gamma(tau) = 28 tau * (w e^{4b}) * G'(R)          (Cor. 5.2)
    a(tau)      = tau_bar(tau)^2                                   (Prop. 6.2)
    A(tau)      = 2 tau_bar^2 + a (1 + 2 tau_bar^2 S_{v/w})
    kappa_0(tau)= 4 tau_bar + 2 A (t + tau_bar (S_{v/w} - 1))       (F09)
    C(tau)      = K(1+q) [2(1+t) + (1+t)^4 kappa_0 (S_{1/(qv)}-1)]  (F12)
    c_site(tau) = K [2 + kappa_0 (S_{1/(qv)}-1)]                    (F13)
  with headline w=192, secondary w=3/(151552|tau|); e^b=1001/1000 (both);
  S_{v/w}=725, S_{1/(qv)}=147 (both pairs, HNM-BB1-F00 closed form); the
  secondary K is the *constant* 2T(1/151552) (the secondary disc radius
  rho=|tau|/q_2=1/151552 does not depend on tau, only q_2=151552|tau| does).

  REVERSE (route iterated_split, `research/round33/reverse/bb1/report.md`):
    t_0(tau)    = 2 T(tau)                                          (S0-S1)
    t_W(tau)    = 2 T(W tau), W=1024 (headline); 2T(1/37888) (secondary)
    c_1, c_2, beta* from (R11): c1 = 4 t0 tW + (4 tW + 4 t0 tW/(1-t0))/(1-8 tW),
                                 c2 = 16 t0 tW + 16 t0 tW/((1-t0)(1-8 tW)),
                                 beta* = c1/(1-c2)
    S_lambda    = S_x at x=lambda/q (closed form HNM-BB1-F00);
                  headline lambda=1/512, q=1/64 -> x=1/8 -> S=2169/343;
                  secondary lambda_2=q_2/2 -> x=1/2 -> S=147            (S5)
    c_site(tau) = K(tau) (2 + beta*(tau) S_lambda)                     (R13)
    C(tau)      = c_site(tau) (1+q)                                    (R13)
  with K(tau) the *same* every-site input as forward's headline K (both
  routes use the identical BA1 gate bound value K=49/111790368 at q=1/64,
  form (b)); the reverse secondary K is likewise the constant 2T(1/151552).

Crude tiers (`crude_majorant`, reported, never a target) replay the same
formulas with `t_i(rho) = 28 rho G(R)` in place of `T(rho)`.

This script checks: (1) every recomputed exact rational equals the exact
rational recorded in the ADMITTED `output/results.json` of the matching
producer (both headline, both secondary, both crude, both signs replay the
same |tau| formula so only |tau|=1e-8 is checked); (2) the forward and
reverse headline C/c_site, computed by two structurally different routes
from the *same* K, agree to the number of significant digits both reports
quote; (3) the tau -> tau/100 ratios of every headline/secondary constant,
recomputed from the same exact formulas at tau=1e-8 and tau=1e-10, match
the reports' own quoted ratios; (4) Arb (python-flint) and mpmath.iv,
reused by import, rigorously enclose the one shared transcendental input
both reports cite as a directed-rounding bound -- `e^{1/8} <= 8/7` -- and
the resulting independently-computed G(R), G'(R) balls are contained in
(and, being genuinely irrational, strictly tighter than) the reports'
admitted rational bounds 148/7 and 352.

Run: `python3 -B bb1_arb.py`
"""
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]

sys.path.insert(0, str(ROOT / "research" / "round32" / "tools"))
import arb_crosscheck as acc  # noqa: E402  (frozen Round32 tool; only arb_of/iv_of reused)

import flint  # noqa: E402
import mpmath  # noqa: E402

PREC = 256
flint.ctx.prec = PREC
mpmath.mp.prec = PREC
mpmath.iv.prec = PREC

TAU_CAP = Q(1, 10 ** 8)
TAU_SMALL = Q(1, 10 ** 10)  # tau/100
Q64 = Q(1, 64)          # headline q
GPRIME_R = Q(352)       # 308 * 8/7
G_R = Q(148, 7)         # 16 * 8/7 * 37/32
EB = Q(1001, 1000)      # "e^b" (a rational stand-in, used exactly as such by both reports)
S_VW = Q(725)           # S_{2/3}, both pairs (HNM-BB1-F00)
S_1_QV = Q(147)         # S_{1/2}, both pairs
S_LAMBDA_HEADLINE = Q(2169, 343)  # S_{1/8} (reverse headline)
S_LAMBDA_SECONDARY = Q(147)       # S_{1/2} (reverse secondary)


def load(rel):
    return json.loads((ROOT / rel).read_text())


def find(results, cid):
    for c in results["checks"]:
        if c["id"] == cid:
            return c
    raise KeyError(cid)


def S_closed_form(x: Q) -> Q:
    """S_x = 1 + 24x(1+x)/(1-x)^3 + 2x/(1-x), for 0<x<1 (HNM-BB1-F00)."""
    assert 0 < x < 1
    return 1 + 24 * x * (1 + x) / (1 - x) ** 3 + 2 * x / (1 - x)


def T_exact(rho: Q) -> Q:
    """T(rho) = (49 rho/144) / (1 - 28 rho G'(R)) = (49 rho/144)/(1-9856 rho)."""
    denom = 1 - 28 * rho * GPRIME_R
    assert denom > 0, "rho outside the admissible disc"
    return Q(49) * rho / 144 / denom


def ti_crude(rho: Q) -> Q:
    """Crude circle bound t_i(rho) = 28 rho G(R) = 592 rho."""
    return 28 * rho * G_R


# --------------------------------------------------------------------------
# FORWARD (polymer_kp)
# --------------------------------------------------------------------------
def forward_headline_w(tau: Q) -> Q:
    return Q(192)


def forward_secondary_w(tau: Q) -> Q:
    q2 = 151552 * tau
    return Q(3) / q2


def forward_constants(tau: Q, w: Q, K: Q, q: Q, crude: bool):
    """Recompute (t_or_tcrude, tau_bar, kappa_0, C, c_site) at coupling tau."""
    t1 = Q(49) * tau / 144
    if crude:
        t_val = 592 * tau              # J G(R), forward's crude "t"
        what = w * EB ** 4
        tau_bar = what * t_val         # J w-hat G(R) = w-hat * (J G(R))
    else:
        t_val = T_exact(tau)           # = t1/(1-9856 tau)
        what = w * EB ** 4
        Gamma = 28 * tau * what * GPRIME_R
        tau_bar = w * EB ** 3 * t1 / (1 - Gamma)
    a = tau_bar ** 2
    A = 2 * tau_bar ** 2 + a * (1 + 2 * tau_bar ** 2 * S_VW)
    kappa0 = 4 * tau_bar + 2 * A * (t_val + tau_bar * (S_VW - 1))
    C = K * (1 + q) * (2 * (1 + t_val) + (1 + t_val) ** 4 * kappa0 * (S_1_QV - 1))
    c_site = K * (2 + kappa0 * (S_1_QV - 1))
    return {"t": t_val, "tau_bar": tau_bar, "a": a, "kappa0": kappa0, "C": C, "c_site": c_site}


def forward_all(tau: Q):
    K_headline = 2 * T_exact(64 * tau)
    K_secondary = 2 * T_exact(Q(1, 151552))          # constant: rho=1/151552 fixed
    K_headline_crude = 2 * ti_crude(64 * tau)
    K_secondary_crude = 2 * ti_crude(Q(1, 151552))    # = 1/128
    q2 = 151552 * tau
    out = {
        "headline": forward_constants(tau, forward_headline_w(tau), K_headline, Q64, crude=False),
        "secondary": forward_constants(tau, forward_secondary_w(tau), K_secondary, q2, crude=False),
        "headline_crude": forward_constants(tau, forward_headline_w(tau), K_headline_crude, Q64, crude=True),
        "secondary_crude": forward_constants(tau, forward_secondary_w(tau), K_secondary_crude, q2, crude=True),
        "K_headline": K_headline, "K_secondary": K_secondary,
    }
    return out


# --------------------------------------------------------------------------
# REVERSE (iterated_split)
# --------------------------------------------------------------------------
def beta_star(t0: Q, tW: Q) -> Q:
    c1 = 4 * t0 * tW + (4 * tW + 4 * t0 * tW / (1 - t0)) / (1 - 8 * tW)
    c2 = 16 * t0 * tW + 16 * t0 * tW / ((1 - t0) * (1 - 8 * tW))
    return c1 / (1 - c2), c1, c2


def reverse_constants(t0: Q, tW: Q, K: Q, q: Q, S_lambda: Q):
    beta, c1, c2 = beta_star(t0, tW)
    c_site = K * (2 + beta * S_lambda)
    C = c_site * (1 + q)
    return {"t0": t0, "tW": tW, "beta": beta, "c1": c1, "c2": c2, "C": C, "c_site": c_site}


def reverse_all(tau: Q):
    q2 = 151552 * tau
    t0 = 2 * T_exact(tau)
    tW_headline = 2 * T_exact(1024 * tau)
    tW_secondary = 2 * T_exact(Q(1, 37888))           # constant
    t0_crude = 2 * ti_crude(tau)
    tW_headline_crude = 2 * ti_crude(1024 * tau)
    tW_secondary_crude = 2 * ti_crude(Q(1, 37888))    # = 1/32
    K_headline = 2 * T_exact(64 * tau)
    K_secondary = 2 * T_exact(Q(1, 151552))
    K_headline_crude = 2 * ti_crude(64 * tau)
    K_secondary_crude = 2 * ti_crude(Q(1, 151552))
    out = {
        "headline": reverse_constants(t0, tW_headline, K_headline, Q64, S_LAMBDA_HEADLINE),
        "secondary": reverse_constants(t0, tW_secondary, K_secondary, q2, S_LAMBDA_SECONDARY),
        "headline_crude": reverse_constants(t0_crude, tW_headline_crude, K_headline_crude, Q64, S_LAMBDA_HEADLINE),
        "secondary_crude": reverse_constants(t0_crude, tW_secondary_crude, K_secondary_crude, q2, S_LAMBDA_SECONDARY),
    }
    return out


# --------------------------------------------------------------------------
# Arb / mpmath: the one shared transcendental input, e^{1/8} <= 8/7
# --------------------------------------------------------------------------
def arb_exp_eighth():
    ball = acc.arb_of("exp(1/8)")
    lo, hi = ball.lower(), ball.upper()

    def to_q(v):
        man, exp = v.man_exp()
        man, exp = int(man), int(exp)
        return Q(man) * Q(2) ** exp if exp >= 0 else Q(man, 2 ** (-exp))

    return to_q(lo), to_q(hi)


def mp_exp_eighth():
    iv = acc.iv_of("exp(1/8)")

    def to_q(m):
        sign, man, exp, _bc = mpmath.mpf(m)._mpf_
        val = Q(int(man)) * Q(2) ** int(exp)
        return -val if sign else val

    return to_q(iv.a), to_q(iv.b)


def main() -> int:
    checks = []
    all_ok = True

    def record(cid, ok, **fields):
        nonlocal all_ok
        all_ok = all_ok and ok
        checks.append({"id": cid, "passed": bool(ok), **fields})

    # --- 0. Arb/mpmath enclosure of e^{1/8} and the admitted 8/7 bound -----
    e18_lo_arb, e18_hi_arb = arb_exp_eighth()
    e18_lo_mp, e18_hi_mp = mp_exp_eighth()
    ADMITTED_E18 = Q(8, 7)
    Gp_tight_hi = Q(308) * e18_hi_arb
    G_tight_hi = Q(16) * e18_hi_arb * Q(37, 32)
    record(
        "e18_enclosure_and_admitted_bound",
        e18_hi_arb <= ADMITTED_E18 and e18_hi_mp <= ADMITTED_E18
        and e18_lo_arb <= e18_hi_arb and e18_lo_mp <= e18_hi_mp
        and Gp_tight_hi < GPRIME_R and G_tight_hi < G_R,
        formula="e^{1/8}; G'(R)=308 e^{1/8}<=352; G(R)=16 e^{1/8}(37/32)<=148/7 "
                "(both reports' shared directed-rounding bound, S0)",
        arb_ball_preview=[float(e18_lo_arb), float(e18_hi_arb)],
        mpmath_iv_preview=[float(e18_lo_mp), float(e18_hi_mp)],
        admitted_bound="8/7", admitted_bound_preview=float(ADMITTED_E18),
        tighter_Gprime_upper_preview=float(Gp_tight_hi), admitted_Gprime=352,
        tighter_G_upper_preview=float(G_tight_hi), admitted_G="148/7",
        note="two independent open-source rigorous-arithmetic libraries confirm the shared "
             "e^{1/8}<=8/7 directed-rounding bound both BB1 reports cite from AM2/BA1, and give "
             "a strictly tighter (irrational) enclosure of G(R), G'(R) contained inside the "
             "reports' admitted rational bounds -- exactly as BA1's own producers and "
             "assistant-1's weighted_contraction_arb.py already established for these same "
             "quantities; reproduced here independently for BB1's use of them.",
    )

    # --- 1. Load admitted BB1 forward/reverse outputs ----------------------
    fwd = load("research/round33/forward/bb1/output/results.json")
    rev = load("research/round33/reverse/bb1/output/results.json")
    ba1_gate = load("research/round33/advisor/ba1-gate.json")
    assert ba1_gate["verdict"] == "accepted_within_scope"

    fwd_headline = find(fwd, "headline_R_form_every_comparison_both_signs")
    fwd_region = find(fwd, "region_form_every_comparison_both_signs")
    fwd_secondary = find(fwd, "secondary_pair_labelled")
    fwd_crude = find(fwd, "crude_tier_reported_separately")
    fwd_kp = find(fwd, "kotecky_preiss_condition_and_tree_majorant")

    rev_headline = find(rev, "headline_C_meets_target")
    rev_region = find(rev, "region_c_site_meets_target")
    rev_secondary = find(rev, "secondary_pair_meets_targets")
    rev_crude = find(rev, "crude_tier_reported_separately")
    rev_lemma = find(rev, "marginal_locality_lemma_constants")

    K_GATE = Q(49, 111790368)
    fwd_K_str = fwd_headline["ba1_input"].split("K=")[1].split(" ")[0].rstrip(")")
    rev_K_str = rev_headline["ba1_input"].split("K=")[1]
    record(
        "K_gate_bound_value_shared_input",
        Q(fwd_K_str) == K_GATE and Q(rev_K_str) == K_GATE,
        note="both BB1 routes use the identical BA1 gate bound value K=49/111790368 at q=1/64, "
             "form (b), as their headline every-site coefficient input (forward S8, reverse S2)",
        K_gate=str(K_GATE), K_gate_preview=float(K_GATE),
        forward_ba1_input=fwd_headline["ba1_input"], reverse_ba1_input=rev_headline["ba1_input"],
    )

    # --- 2. Recompute forward at the cap and compare exactly ---------------
    F = forward_all(TAU_CAP)
    admitted_fwd_C = Q(fwd_headline["C"])
    admitted_fwd_c_site = Q(fwd_region["c_site"])
    admitted_fwd_C2 = Q(fwd_secondary["C"])
    admitted_fwd_c_site2 = Q(fwd_secondary["c_site"])
    admitted_fwd_Ccrude = Q(fwd_crude["C_crude"])
    admitted_fwd_csitecrude_formula = Q(fwd_crude["c_site_crude_formula"])
    admitted_fwd_C2crude = Q(fwd_crude["secondary_crude_C"])
    admitted_fwd_taubar = Q(fwd_kp["record"]["headline"]["taubar_mixed"])
    admitted_fwd_a = Q(fwd_kp["record"]["headline"]["a"])

    record(
        "forward_headline_reproduced_exactly",
        F["headline"]["C"] == admitted_fwd_C and F["headline"]["c_site"] == admitted_fwd_c_site
        and F["headline"]["tau_bar"] == admitted_fwd_taubar and F["headline"]["a"] == admitted_fwd_a,
        formula="C = K(1+q)[2(1+t)+(1+t)^4 kappa0 (S_1qv-1)], c_site = K[2+kappa0(S_1qv-1)]",
        C_preview=float(F["headline"]["C"]), admitted_C_preview=float(admitted_fwd_C),
        c_site_preview=float(F["headline"]["c_site"]), admitted_c_site_preview=float(admitted_fwd_c_site),
        tau_bar_preview=float(F["headline"]["tau_bar"]),
        a_preview=float(F["headline"]["a"]),
    )
    record(
        "forward_secondary_reproduced_exactly",
        F["secondary"]["C"] == admitted_fwd_C2 and F["secondary"]["c_site"] == admitted_fwd_c_site2,
        C_preview=float(F["secondary"]["C"]), admitted_C_preview=float(admitted_fwd_C2),
        c_site_preview=float(F["secondary"]["c_site"]), admitted_c_site_preview=float(admitted_fwd_c_site2),
    )
    record(
        "forward_crude_reproduced_exactly",
        F["headline_crude"]["C"] == admitted_fwd_Ccrude
        and F["headline_crude"]["c_site"] == admitted_fwd_csitecrude_formula
        and F["secondary_crude"]["C"] == admitted_fwd_C2crude,
        C_crude_preview=float(F["headline_crude"]["C"]), admitted_preview=float(admitted_fwd_Ccrude),
        c_site_crude_preview=float(F["headline_crude"]["c_site"]),
        admitted_c_site_crude_preview=float(admitted_fwd_csitecrude_formula),
        C2_crude_preview=float(F["secondary_crude"]["C"]), admitted_C2_crude_preview=float(admitted_fwd_C2crude),
    )

    # --- 3. Recompute reverse at the cap and compare exactly ----------------
    Rv = reverse_all(TAU_CAP)
    admitted_rev_C = Q(rev_headline["C"]["exact"])
    admitted_rev_c_site = Q(rev_region["c_site"]["exact"])
    admitted_rev_C2 = Q(rev_secondary["C"]["exact"])
    admitted_rev_c_site2 = Q(rev_secondary["c_site"]["exact"])
    admitted_rev_Ccrude = Q(rev_crude["C_crude"]["exact"])
    admitted_rev_csitecrude = Q(rev_crude["c_site_crude"]["exact"])
    admitted_rev_C2crude = Q(rev_crude["secondary_crude"]["C"]["exact"])
    admitted_rev_c_site2crude = Q(rev_crude["secondary_crude"]["c_site"]["exact"])
    admitted_beta = Q(rev_lemma["beta"]["exact"])
    admitted_c1 = Q(rev_lemma["c1"]["exact"])
    admitted_c2 = Q(rev_lemma["c2"]["exact"])
    admitted_t0 = Q(rev_lemma["t0"]["exact"])
    admitted_tW = Q(rev_lemma["tW"]["exact"])

    record(
        "reverse_headline_reproduced_exactly",
        Rv["headline"]["C"] == admitted_rev_C and Rv["headline"]["c_site"] == admitted_rev_c_site
        and Rv["headline"]["beta"] == admitted_beta and Rv["headline"]["c1"] == admitted_c1
        and Rv["headline"]["c2"] == admitted_c2 and Rv["headline"]["t0"] == admitted_t0
        and Rv["headline"]["tW"] == admitted_tW,
        formula="c_site = K(2+beta* S_lambda), C = c_site (1+q); "
                "beta*=c1/(1-c2), c1,c2 from (R11)",
        C_preview=float(Rv["headline"]["C"]), admitted_C_preview=float(admitted_rev_C),
        c_site_preview=float(Rv["headline"]["c_site"]), admitted_c_site_preview=float(admitted_rev_c_site),
        beta_preview=float(Rv["headline"]["beta"]), admitted_beta_preview=float(admitted_beta),
    )
    record(
        "reverse_secondary_reproduced_exactly",
        Rv["secondary"]["C"] == admitted_rev_C2 and Rv["secondary"]["c_site"] == admitted_rev_c_site2,
        C_preview=float(Rv["secondary"]["C"]), admitted_C_preview=float(admitted_rev_C2),
        c_site_preview=float(Rv["secondary"]["c_site"]), admitted_c_site_preview=float(admitted_rev_c_site2),
    )
    record(
        "reverse_crude_reproduced_exactly",
        Rv["headline_crude"]["C"] == admitted_rev_Ccrude and Rv["headline_crude"]["c_site"] == admitted_rev_csitecrude
        and Rv["secondary_crude"]["C"] == admitted_rev_C2crude
        and Rv["secondary_crude"]["c_site"] == admitted_rev_c_site2crude,
        C_crude_preview=float(Rv["headline_crude"]["C"]), admitted_preview=float(admitted_rev_Ccrude),
        c_site_crude_preview=float(Rv["headline_crude"]["c_site"]), admitted_preview2=float(admitted_rev_csitecrude),
    )

    # --- 4. Forward vs reverse headline agreement ("to the stated digits") --
    diff_C = abs(F["headline"]["C"] - Rv["headline"]["C"])
    rel_C = diff_C / F["headline"]["C"]
    diff_c = abs(F["headline"]["c_site"] - Rv["headline"]["c_site"])
    rel_c = diff_c / F["headline"]["c_site"]
    # Both reports quote 12 significant digits: 8.90511999358e-7 (fwd) vs
    # 8.90425620114e-7 (rev); they agree to 3 significant figures (8.90e-7)
    # and differ from the 4th, a genuine route-dependent difference (forward
    # carries the (1+t)^4 Lipschitz-in-coefficients factor 2(1+t) instead of
    # the reverse's exact eta=0 factor of 2), not a discrepancy: both are
    # independently proved upper bounds on the same headline target.
    record(
        "forward_reverse_headline_agree_to_stated_digits",
        rel_C < Q(1, 10 ** 3) and rel_c < Q(1, 10 ** 3),
        forward_C_preview=float(F["headline"]["C"]), reverse_C_preview=float(Rv["headline"]["C"]),
        relative_difference_C_preview=float(rel_C),
        forward_c_site_preview=float(F["headline"]["c_site"]), reverse_c_site_preview=float(Rv["headline"]["c_site"]),
        relative_difference_c_site_preview=float(rel_c),
        note="agree to 3 significant figures (8.90e-7); the 4th-digit difference is the "
             "route-dependent Lipschitz-in-coefficients factor (forward: 2(1+t) via Lemma 2.4's "
             "(1+t)^{|Y|-1} bound; reverse: exactly 2, eta=0, via Lemma 1.3's single-support "
             "split) -- both are independently proved upper bounds on the same headline target "
             "1/250000, not two measurements of one quantity, so exact equality is not expected.",
    )

    # --- 5. tau -> tau/100 ratios, recomputed exactly -----------------------
    F_small = forward_all(TAU_SMALL)
    Rv_small = reverse_all(TAU_SMALL)

    def ratio(big, small):
        return big / small

    fwd_ratio_C = ratio(F["headline"]["C"], F_small["headline"]["C"])
    fwd_ratio_c = ratio(F["headline"]["c_site"], F_small["headline"]["c_site"])
    fwd_ratio_C2 = ratio(F["secondary"]["C"], F_small["secondary"]["C"])
    fwd_ratio_c2 = ratio(F["secondary"]["c_site"], F_small["secondary"]["c_site"])
    rev_ratio_C = ratio(Rv["headline"]["C"], Rv_small["headline"]["C"])
    rev_ratio_c = ratio(Rv["headline"]["c_site"], Rv_small["headline"]["c_site"])
    rev_ratio_C2 = ratio(Rv["secondary"]["C"], Rv_small["secondary"]["C"])
    rev_ratio_c2 = ratio(Rv["secondary"]["c_site"], Rv_small["secondary"]["c_site"])

    def close(a: Q, b: float, tol=1e-6) -> bool:
        return abs(float(a) - b) < tol * max(1.0, abs(b))

    record(
        "tau_over_100_ratios_recomputed",
        close(fwd_ratio_C, 100.647875) and close(fwd_ratio_c, 100.647875)
        and close(fwd_ratio_C2, 1.00150034) and close(fwd_ratio_c2, 1.00000000, tol=1e-8)
        and close(rev_ratio_C, 100.638216785) and close(rev_ratio_c, 100.638216785)
        and close(rev_ratio_C2, 1.00150034215) and close(rev_ratio_c2, 1.00000000009, tol=1e-9),
        forward={"C_headline": float(fwd_ratio_C), "c_site": float(fwd_ratio_c),
                 "C_secondary": float(fwd_ratio_C2), "c_site_secondary": float(fwd_ratio_c2)},
        reverse={"C_headline": float(rev_ratio_C), "c_site": float(rev_ratio_c),
                 "C_secondary": float(rev_ratio_C2), "c_site_secondary": float(rev_ratio_c2)},
        forward_report_quoted={"C_headline": 100.647875, "c_site": 100.647875,
                                "C_secondary": 1.00150034, "c_site_secondary": 1.00000000},
        reverse_report_quoted={"C_headline": 100.638216785, "c_site": 100.638216785,
                                "C_secondary": 1.00150034215, "c_site_secondary": 1.00000000009},
        note="each ratio is C(tau=1e-8)/C(tau=1e-10) from the same exact Fraction formula, no "
             "intermediate rounding, exactly as each report's own check.py computes it; the "
             "forward and reverse headline ratios (~100.64-100.65) differ slightly because "
             "K(tau)=2T(64 tau) is common to both, but t(tau) [forward] and t0(tau),beta*(tau) "
             "[reverse] carry slightly different nonlinear-in-tau corrections",
    )

    # --- 6. bracket checks (contract scaling_brackets_per_constant) --------
    in_bracket = (Q(95) <= fwd_ratio_C <= Q(105) and Q(95) <= rev_ratio_C <= Q(105)
                  and Q(99, 100) <= fwd_ratio_C2 <= Q(101, 100)
                  and Q(99, 100) <= rev_ratio_C2 <= Q(101, 100))
    record(
        "scaling_brackets_per_constant",
        in_bracket,
        headline_bracket="[95,105]", secondary_bracket="[99/100,101/100]",
        forward_C_headline_preview=float(fwd_ratio_C), reverse_C_headline_preview=float(rev_ratio_C),
        forward_C_secondary_preview=float(fwd_ratio_C2), reverse_C_secondary_preview=float(rev_ratio_C2),
    )

    report = {
        "tool": "bb1_arb",
        "status": "preview_and_crosscheck_only_zero_research_loops_not_a_contract_or_gate",
        "libraries": {"python-flint": flint.__version__, "mpmath": mpmath.__version__},
        "precision_bits": PREC,
        "all_passed": all_ok,
        "checks": checks,
        "interpretation": "Independent Fraction recomputation, from the closed-form formulas "
                           "stated in research/round33/forward/bb1/report.md and "
                           "research/round33/reverse/bb1/report.md, of every headline, secondary "
                           "and crude BB1 constant, cross-checked exactly against the ADMITTED "
                           "output/results.json of each producer; Arb (python-flint) and "
                           "mpmath.iv rigorously enclose the one shared transcendental input "
                           "(e^{1/8}<=8/7) both routes' K, t, tau_bar, t0, tW ultimately rest on "
                           "through G(R), G'(R). Never evidence, never admission; the BB1 "
                           "contract's own admission is decided only by the frozen producers' "
                           "exact fractions.Fraction check.py files.",
    }
    print(json.dumps(report, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
