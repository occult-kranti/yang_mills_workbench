#!/usr/bin/env python3
"""BB2 constant recomputation, the new (5N+1)(r_N-1)<=N^3/4 lemma, and a
BB1-producer-value discharge preview (PREVIEW ONLY, zero research loops).

Round33 sub-round 2, modern (Penrose/Feynman) lens, assistant-2. Nothing
here is evidence, a contract, a premise or a gate. It never imports a
producer `check.py`; it reads only the frozen BB1/BB2 contracts, the
ADMITTED `output/results.json` of the BB1 and BB2 forward/reverse
producers, and the BA2 gate, for comparison. `python-flint` (Arb) and
`mpmath.iv` are reused by import as independent, already-frozen open-source
libraries, exactly as `research/round32/tools/arb_crosscheck.py`'s
`arb_of`/`iv_of` helpers are (itself reused by import, never modified).

**(1) State constants at the CONTRACT hypothesis values** (this is what the
BB2 producers themselves report, `conditional_on_bb1_targets`, i.e. not yet
an unconditional admission -- BB1's own gate has not yet discharged them):
  forward (assembly nested_telescoping):  C'  = C_h/(1-q)     = (64/63) C_h = 4/984375
                                            c'  = c_h/(1-q)    = (64/63) c_h = 2/984375
  reverse (assembly union_comparison):    C'  = C_h                        = 1/250000
                                            c'  = c_h                       = 1/500000
  with q=1/64, C_h=1/250000, c_h=1/500000 (the BB1 contract's frozen targets).

**(2) C_dyn, read from the BA2 gate (tier polynomial_lieb_robinson):**
  forward:  C_dyn = 2 K_F1 + K_cmp/4                     (route duhamel_inner_f1, both terms)
  reverse:  C_dyn[F1] = 2 K_F1                            (route duhamel_inner_f1)
            C_dyn[F2] = 2 K'_F2                           (route duhamel_inner_f2)
  K_F1 = 592704 tau^2/(1-338688|tau|) (rational, closed form);
  K_cmp = 254016 tau^2/(1-338688|tau|) (rational, closed form, forward route);
  K'_F2 = 345744 tau^2 E_up(592704|tau|), E_up(y)=1+y/3+y^2/(12(1-y/5)) a
  RATIONAL upper bound (reverse BA2 report S(notation)) of the transcendental
  E(y)=2(e^y-1-y)/y^2; Arb/mpmath, reused by import, rigorously confirm
  E_up(y)>=E(y) at the working point (independently of, not by importing,
  assistant-1's `ba2_directed_reconciliation.py`, which made the same check
  for BA2 itself in sub-round 1).

**(3) The new lemma** `(5N+1)(r_N-1) <= N^3/4` for `N>=5`, `r_N=floor((N-1)/2)`,
used by forward's item 5 (report.md "Lemma HNM-BB2-F08"). The forward
report proves it via `g(N)=N^3-10N^2+28N+6`, `g(5)=21`, `g'(N)>=3` for
`N>=5`. This script verifies, with sympy (if available; a from-scratch
polynomial-coefficient check otherwise), the SHARPER identity the task
requests: `N^3-10N^2+28N+6 = N(N-5)^2+3N+6`, which shows `g(N)>0` for
*every* `N>=0` directly (no calculus needed) since `N(N-5)^2>=0` and
`3N+6>0` there -- a strictly simpler proof of the same lemma.

**(4) BB2 discharge preview (PREVIEW, not a gate).** The BB2 producers'
own C', c'_site above are evaluated at the BB1 CONTRACT's frozen targets
(C_h, c_h), because BB2 is required to read no BB1 producer file
(`conditional_on_bb1_targets`, `reverse_premise_isolation`). This script,
being outside that isolation rule (a lens assistant, not a BB2 producer),
re-evaluates the SAME assembly functions at the BB1 PRODUCERS' own PROVED
values (`research/round33/{forward,reverse}/bb1/output/results.json`,
independently reproduced exactly in `bb1_arb.py` in this same folder) and
reports the resulting margins against the BB2 targets. **This is a labelled
preview of what the BB2 gate's eventual discharge is likely to look like,
not the discharge itself** -- the discharge is a documented step at the
BB2 gate, decided by the BB1 gate's admitted values, not by a lens preview.

Run: `python3 -B bb2_constants.py`
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

try:
    import sympy
    HAVE_SYMPY = True
except ImportError:  # pragma: no cover
    HAVE_SYMPY = False

PREC = 256
flint.ctx.prec = PREC
mpmath.mp.prec = PREC
mpmath.iv.prec = PREC

Q64 = Q(1, 64)
C_H = Q(1, 250000)
C_SITE_H = Q(1, 500000)


def load(rel):
    return json.loads((ROOT / rel).read_text())


def find(results, cid):
    for c in results["checks"]:
        if c["id"] == cid:
            return c
    raise KeyError(cid)


def arb_exp_bounds(y: Q):
    def expr(x: Q) -> str:
        return f"exp({x.numerator})" if x.denominator == 1 else f"exp({x.numerator}/{x.denominator})"
    ball = acc.arb_of(expr(y))
    lo, hi = ball.lower(), ball.upper()

    def to_q(v):
        man, exp = v.man_exp()
        man, exp = int(man), int(exp)
        return Q(man) * Q(2) ** exp if exp >= 0 else Q(man, 2 ** (-exp))
    return to_q(lo), to_q(hi)


def mp_exp_bounds(y: Q):
    def expr(x: Q) -> str:
        return f"exp({x.numerator})" if x.denominator == 1 else f"exp({x.numerator}/{x.denominator})"
    iv = acc.iv_of(expr(y))

    def to_q(m):
        sign, man, exp, _bc = mpmath.mpf(m)._mpf_
        val = Q(int(man)) * Q(2) ** int(exp)
        return -val if sign else val
    return to_q(iv.a), to_q(iv.b)


def E_up(y: Q) -> Q:
    """Reverse BA2 report's rational upper bound: 1+y/3+y^2/(12(1-y/5))."""
    return 1 + y / 3 + y ** 2 / (12 * (1 - y / 5))


def main() -> int:
    checks = []
    all_ok = True

    def record(cid, ok, **fields):
        nonlocal all_ok
        all_ok = all_ok and ok
        checks.append({"id": cid, "passed": bool(ok), **fields})

    # --- 0. Load admitted BB1/BB2 outputs and the BA2 gate constants -------
    bb2_fwd = load("research/round33/forward/bb2/output/results.json")
    bb2_rev = load("research/round33/reverse/bb2/output/results.json")
    bb1_fwd = load("research/round33/forward/bb1/output/results.json")
    bb1_rev = load("research/round33/reverse/bb1/output/results.json")
    contract_bb2 = load("research/round33/contracts/bb2.json")

    assert contract_bb2["parameters"]["rate_constant_pair"]["hypotheses"].startswith(
        "the BB1 frozen targets"
    )

    # --- 1. Forward/reverse BB2 state constants at the CONTRACT hypotheses -
    C_prime_fwd = C_H / (1 - Q64)          # = (64/63) C_H
    c_site_prime_fwd = C_SITE_H / (1 - Q64)
    C_prime_rev = C_H                       # union comparison, factor 1
    c_site_prime_rev = C_SITE_H

    admitted_fwd_item1 = find(bb2_fwd, "item1_whole_sequence_cauchy_R")
    admitted_fwd_C_prime = Q(admitted_fwd_item1["C_prime"])
    admitted_rev_item1 = find(bb2_rev, "item1_whole_sequence_cauchy_R_and_regions")
    admitted_rev_C_prime = Q(admitted_rev_item1["C_prime"]["exact"])
    admitted_rev_c_site_prime = Q(admitted_rev_item1["c_site_prime"]["exact"])

    ADMITTED_FWD_C_PRIME = Q(4, 984375)
    ADMITTED_FWD_C_SITE_PRIME = Q(2, 984375)
    record(
        "forward_state_constants_at_hypothesis_values",
        C_prime_fwd == ADMITTED_FWD_C_PRIME == admitted_fwd_C_prime
        and c_site_prime_fwd == ADMITTED_FWD_C_SITE_PRIME,
        formula="C'=(64/63) C_h, c'_site=(64/63) c_h (nested_telescoping, factor 1/(1-q))",
        C_prime_exact=str(C_prime_fwd), C_prime_preview=float(C_prime_fwd),
        c_site_prime_exact=str(c_site_prime_fwd), c_site_prime_preview=float(c_site_prime_fwd),
        target_C_prime="1/100000", margin_preview=float(Q(1, 100000) / C_prime_fwd),
        target_c_site_prime="1/200000", margin_preview_c_site=float(Q(1, 200000) / c_site_prime_fwd),
    )
    record(
        "reverse_state_constants_at_hypothesis_values",
        C_prime_rev == admitted_rev_C_prime and c_site_prime_rev == admitted_rev_c_site_prime,
        formula="C'=C_h, c'_site=c_h (union_comparison, assembly factor 1 for nested centered cubes)",
        C_prime_exact=str(C_prime_rev), C_prime_preview=float(C_prime_rev),
        c_site_prime_exact=str(c_site_prime_rev), c_site_prime_preview=float(c_site_prime_rev),
        target_C_prime="1/100000", margin_preview=float(Q(1, 100000) / C_prime_rev),
        target_c_site_prime="1/200000", margin_preview_c_site=float(Q(1, 200000) / c_site_prime_rev),
    )

    # --- 2. C_dyn from the BA2 gate -----------------------------------------
    ba2_fwd_dyn = find(bb2_fwd, "ba2_dynamics_constants_read_from_gate")
    K_F1 = Q(ba2_fwd_dyn["K_F1"])
    K_cmp = Q(ba2_fwd_dyn["K_cmp"])
    ba2_rev_dyn = find(bb2_rev, "ba2_gate_dynamics_constants_read_exactly")
    K_prime_F2 = Q(ba2_rev_dyn["ba2_gate_values"]["K_F2_rev"]["exact"])

    C_dyn_fwd = 2 * K_F1 + K_cmp / 4
    C_dyn_rev_F1 = 2 * K_F1
    C_dyn_rev_F2 = 2 * K_prime_F2

    ADMITTED_C_DYN_FWD = Q(78057, 622883200000000)
    ADMITTED_C_DYN_REV_F1 = Q(9261, 77860400000000)
    ADMITTED_C_DYN_REV_F2 = Q(1055961408185869563, 15240701171875000000000000000)
    record(
        "C_dyn_from_ba2_gate",
        C_dyn_fwd == ADMITTED_C_DYN_FWD and C_dyn_rev_F1 == ADMITTED_C_DYN_REV_F1
        and C_dyn_rev_F2 == ADMITTED_C_DYN_REV_F2,
        forward_formula="C_dyn = 2 K_F1 + K_cmp/4 (both duhamel_inner_f1)",
        forward_C_dyn_preview=float(C_dyn_fwd), target="1/2000000000",
        forward_margin_preview=float(Q(1, 2000000000) / C_dyn_fwd),
        reverse_F1_formula="C_dyn[F1] = 2 K_F1 (duhamel_inner_f1)",
        reverse_F1_preview=float(C_dyn_rev_F1),
        reverse_F1_margin_preview=float(Q(1, 2000000000) / C_dyn_rev_F1),
        reverse_F2_formula="C_dyn[F2] = 2 K'_F2 (duhamel_inner_f2)",
        reverse_F2_preview=float(C_dyn_rev_F2),
        reverse_F2_margin_preview=float(Q(1, 2000000000) / C_dyn_rev_F2),
    )

    # --- 3. Arb/mpmath: E_up(y) >= E(y) at the reverse's working point ------
    tau_cap = Q(1, 10 ** 8)
    y_rev = 592704 * tau_cap  # = 9261/1562500, the point K'_F2 uses
    e_y_lo_arb, e_y_hi_arb = arb_exp_bounds(y_rev)
    e_y_lo_mp, e_y_hi_mp = mp_exp_bounds(y_rev)

    def E_true_bounds(e_lo: Q, e_hi: Q):
        # E(y) = 2(e^y - 1 - y)/y^2, monotone increasing in e^y on this range
        lo = 2 * (e_lo - 1 - y_rev) / y_rev ** 2
        hi = 2 * (e_hi - 1 - y_rev) / y_rev ** 2
        return lo, hi

    E_lo_arb, E_hi_arb = E_true_bounds(e_y_lo_arb, e_y_hi_arb)
    E_lo_mp, E_hi_mp = E_true_bounds(e_y_lo_mp, e_y_hi_mp)
    Eup_val = E_up(y_rev)
    ADMITTED_EUP = Q(48866741088707, 48770243750000)
    record(
        "E_up_ge_E_arb_mpmath_confirmed",
        Eup_val == ADMITTED_EUP and E_hi_arb <= Eup_val and E_hi_mp <= Eup_val
        and E_lo_arb <= E_hi_arb and E_lo_mp <= E_hi_mp,
        formula="E(y)=2(e^y-1-y)/y^2 <= E_up(y)=1+y/3+y^2/(12(1-y/5)), y=592704|tau|",
        y_exact=str(y_rev), y_preview=float(y_rev),
        E_up_exact=str(Eup_val), E_up_preview=float(Eup_val),
        E_arb_ball_preview=[float(E_lo_arb), float(E_hi_arb)],
        E_mpmath_iv_preview=[float(E_lo_mp), float(E_hi_mp)],
        gap_preview=float(Eup_val - E_hi_arb),
        note="independently confirms (own Arb/mpmath calls, not imported from "
             "assistant-1's ba2_directed_reconciliation.py, which made the analogous check "
             "for BA2's own K_cmp forward-route quantity) the reverse BA2 report's own claim "
             "that its rational E_up dominates the true E at the working point; the reported "
             "gap ~7e-13 there is reproduced here to the digit.",
    )

    # --- 4. The new lemma: (5N+1)(r_N-1) <= N^3/4 for N>=5 ------------------
    if HAVE_SYMPY:
        Nsym = sympy.symbols("N")
        lhs = Nsym ** 3 - 10 * Nsym ** 2 + 28 * Nsym + 6
        rhs = Nsym * (Nsym - 5) ** 2 + 3 * Nsym + 6
        identity_holds = sympy.simplify(lhs - rhs) == 0
        expanded_rhs = str(sympy.expand(rhs))
    else:  # pragma: no cover -- fallback if sympy is unavailable
        from fractions import Fraction as QQ

        def poly_eval(coeffs, n):
            return sum(c * n ** i for i, c in enumerate(coeffs))
        # coefficients (const, N, N^2, N^3) checked at 6 sample integers
        lhs_c = (6, 28, -10, 1)
        identity_holds = all(
            poly_eval(lhs_c, n) == n * (n - 5) ** 2 + 3 * n + 6 for n in range(-5, 20)
        )
        expanded_rhs = "N**3 - 10*N**2 + 28*N + 6 (checked pointwise, sympy unavailable)"

    def g(N: int) -> int:
        return N ** 3 - 10 * N ** 2 + 28 * N + 6

    def factored_g(N: int) -> int:
        return N * (N - 5) ** 2 + 3 * N + 6

    lemma_holds = True
    lemma_rows = []
    for N in list(range(5, 30)) + [100, 1000, 10 ** 6]:
        r_N = (N - 1) // 2
        lhs_val = (5 * N + 1) * (r_N - 1)
        rhs_val = Q(N ** 3, 4)
        ok = lhs_val <= rhs_val
        lemma_holds = lemma_holds and ok and g(N) == factored_g(N) and g(N) > 0
        if N <= 10 or N in (100, 1000, 10 ** 6):
            lemma_rows.append({"N": N, "r_N": r_N, "lhs": lhs_val,
                                "N_cubed_over_4": str(rhs_val), "g_N": g(N), "holds": ok})

    record(
        "lemma_F08_identity_and_bound",
        identity_holds and lemma_holds,
        identity="N^3-10N^2+28N+6 = N(N-5)^2+3N+6",
        identity_verified_with="sympy" if HAVE_SYMPY else "pointwise fallback (sympy unavailable)",
        expanded_rhs=expanded_rhs,
        note="the factored form shows g(N)=N(N-5)^2+3N+6 > 0 for EVERY N>=0 directly "
             "(N(N-5)^2>=0, 3N+6>0), a strictly simpler proof of forward report.md's Lemma "
             "HNM-BB2-F08 than its own g(5)=21-plus-derivative-growth argument (which is also "
             "reproduced and confirmed: g(5)=21, and g is increasing for N>=5 since "
             "g'(N)=3N^2-20N+28>=3 there).",
        sample_rows=lemma_rows,
    )

    # --- 5. BB2 discharge PREVIEW at the BB1 producers' own proved values --
    fwd_bb1_headline = find(bb1_fwd, "headline_R_form_every_comparison_both_signs")
    fwd_bb1_region = find(bb1_fwd, "region_form_every_comparison_both_signs")
    rev_bb1_headline = find(bb1_rev, "headline_C_meets_target")
    rev_bb1_region = find(bb1_rev, "region_c_site_meets_target")

    C_bb1_fwd = Q(fwd_bb1_headline["C"])
    c_site_bb1_fwd = Q(fwd_bb1_region["c_site"])
    C_bb1_rev = Q(rev_bb1_headline["C"]["exact"])
    c_site_bb1_rev = Q(rev_bb1_region["c_site"]["exact"])

    def discharge(C_h_val, c_h_val, assembly):
        if assembly == "nested_telescoping":
            return C_h_val / (1 - Q64), c_h_val / (1 - Q64)
        else:  # union_comparison
            return C_h_val, c_h_val

    previews = {}
    for bb1_label, (Ch, ch) in {
        "forward_bb1_producer": (C_bb1_fwd, c_site_bb1_fwd),
        "reverse_bb1_producer": (C_bb1_rev, c_site_bb1_rev),
        "worse_of_the_two": (max(C_bb1_fwd, C_bb1_rev), max(c_site_bb1_fwd, c_site_bb1_rev)),
    }.items():
        for assembly in ("nested_telescoping", "union_comparison"):
            Cp, cp = discharge(Ch, ch, assembly)
            key = f"{bb1_label}__{assembly}"
            previews[key] = {
                "C_prime_preview": float(Cp), "c_site_prime_preview": float(cp),
                "C_prime_margin_preview": float(Q(1, 100000) / Cp),
                "c_site_prime_margin_preview": float(Q(1, 200000) / cp),
                "meets_targets": Cp <= Q(1, 100000) and cp <= Q(1, 200000),
            }

    all_meet = all(v["meets_targets"] for v in previews.values())
    record(
        "bb2_discharge_preview_at_bb1_producer_values",
        all_meet,
        status="PREVIEW ONLY -- not a gate, not the BB2 discharge, not read by any BB2 "
               "producer or by the BB2 gate; the actual discharge happens at the BB2 gate "
               "using the BB1 gate's admitted values, per contract control "
               "'conditional_on_bb1_targets'.",
        bb1_producer_values={
            "forward_C": float(C_bb1_fwd), "forward_c_site": float(c_site_bb1_fwd),
            "reverse_C": float(C_bb1_rev), "reverse_c_site": float(c_site_bb1_rev),
            "contract_hypothesis_C_h": float(C_H), "contract_hypothesis_c_h": float(C_SITE_H),
        },
        previews=previews,
        note="both BB1 producers' own headline C, c_site (~8.90e-7) are about 4.49x smaller "
             "than the contract hypothesis values they are bound to beat (C_h=4e-6, matching "
             "BB1's own reported margin against its C<=4e-6 target); since both assembly "
             "functions are linear in the hypothesis constant with a fixed positive "
             "coefficient (64/63 or 1), the discharge-preview margins here (~11.05-11.23 for "
             "C', ~5.61-5.70 for c'_site) are correspondingly about 4.49x the "
             "contract-hypothesis-value margins computed in check 1 above (~2.46 and ~2.50).",
    )

    report = {
        "tool": "bb2_constants",
        "status": "preview_and_crosscheck_only_zero_research_loops_not_a_contract_or_gate",
        "libraries": {"python-flint": flint.__version__, "mpmath": mpmath.__version__,
                       "sympy": sympy.__version__ if HAVE_SYMPY else "unavailable"},
        "precision_bits": PREC,
        "all_passed": all_ok,
        "checks": checks,
        "interpretation": "Independent recomputation of the BB2 state constants at the BB1 "
                           "contract's frozen hypothesis values (exactly what the BB2 "
                           "producers themselves report, conditional_on_bb1_targets) and of "
                           "C_dyn from the admitted BA2 gate values; a from-scratch sympy "
                           "verification of the new lemma's polynomial identity; and a "
                           "clearly labelled, non-authoritative PREVIEW of what the discharge "
                           "would look like if evaluated at the BB1 producers' own (not yet "
                           "gated) proved values instead of the contract hypotheses. Never "
                           "evidence, never a gate, never read by any producer.",
    }
    print(json.dumps(report, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
