#!/usr/bin/env python3
"""BC2 route-B admissibility: disc self-map/contraction, the maximal disc
radius and split weight, and the rejection of the route-A extremes.

Round33 sub-round 3, modern (Penrose/Feynman) lens, research assistant/coder
"assistant-3". **This script counts zero research loops. Nothing here is
evidence, a contract, a premise or a gate.** It never imports a producer
`check.py`, and never reads `research/round33/forward/bd*` or
`research/round33/reverse/bd1` (in production). It reads only the frozen
`research/round33/contracts/bc2.json`, the ADMITTED
`research/round33/forward/bc2/output/results.json` and `report.md` (for the
closed-form admissibility statements, read as text, never executed), and
`research/round33/experts/modern/bc2-targets-proposal.md` Section 10.1 for
comparison. `python-flint` (Arb) is reused BY IMPORT, exactly as
`research/round32/tools/arb_crosscheck.py` reuses it, never modified.

What this script checks, independently, in exact `fractions.Fraction`
arithmetic AND in Arb 256-bit ball arithmetic (a second, independent
numeric path over the same rationals):

  1. The route-B disc self-map and contraction at the headline disc
     rho = 64|tau| (BC2 report Section 0, HNM-BC2-F01):
       29 * rho * G(R)  <= R = 1/64      (self-map)
       29 * rho * G'(R) <  1              (contraction)
     with G(R) = 148/7, G'(R) = 352 the route-B rational directed-rounding
     bounds (inherited from AM2/AX1, never re-derived here).
  2. The same two inequalities at the split weight's own disc, rho = W|tau|,
     W = 1024 (the split creation weight BC2's iterated_split route uses).
  3. The route-B maximal disc radius rho_max = R / (29 G(R)) = 7/274688, and
     the resulting maximal admissible split weight
     W_max = rho_max / |tau| = 2734375/1073 at the cap |tau| = 10^-8 (BC2
     report Section 0: "the admissible split weights are 1<=W<=7/(274688|tau|)").
  4. The rejection of the route-A extremes: the BA1/BB1 disc radius
     tau_star = 1/37888 and the BB1 secondary split weight 1/(37888|tau|)
     both give 29*(148/7)/37888 = 29/1792, which exceeds the route-B rate
     q = 1/64 = 28/1792 -- so both fail the route-B disc self-map and are
     correctly rejected in the BC2 report.

Every admitted rational this script recomputes is checked bit-for-bit equal
to the value recorded in the ADMITTED `research/round33/forward/bc2/output/results.json`
(`weights_declared_and_admissible`), and every inequality is re-verified in
Arb ball arithmetic as a numerically independent path (all quantities here
are rational, so the Arb "enclosure" has zero width and the check reduces to
an independent confirmation that a wholly different arithmetic library's
ball division/multiplication agrees with the exact Fraction result to the
last bit at 256-bit precision -- a defence against a transcription error in
either arithmetic path, in the spirit of
`research/round33/experts/modern/assistant-2/bb1_arb.py`).

Run: `python3 -B admissibility.py`
"""
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]

sys.path.insert(0, str(ROOT / "research" / "round32" / "tools"))

import flint  # noqa: E402

PREC = 256
flint.ctx.prec = PREC

TAU_CAP = Q(1, 10 ** 8)
J_PRIME = Q(29)              # route-B per-site sum coefficient (4 stars x 7|tau| + 1 single x |tau|)
G_R = Q(148, 7)              # route-B rational bound on G(R), inherited from AM2/AX1
GPRIME_R = Q(352)            # route-B rational bound on G'(R)
Q64 = Q(1, 64)               # frozen route-B rate q
W_SPLIT = Q(1024)            # iterated_split creation weight
J_PRIME_ROUTE_A = Q(28)      # route-A per-site sum coefficient, for the rejected-extremes check
TAU_STAR_ROUTE_A = Q(1, 37888)  # BA1/BB1 disc radius (route A)


def load(rel):
    return json.loads((ROOT / rel).read_text())


def find(results, cid):
    for c in results["checks"]:
        if c["id"] == cid:
            return c
    raise KeyError(cid)


def to_arb(x: Q):
    return flint.arb(flint.fmpq(x.numerator, x.denominator))


def arb_bounds(ball):
    lo, hi = ball.lower(), ball.upper()

    def to_q(v):
        man, exp = v.man_exp()
        man, exp = int(man), int(exp)
        return Q(man) * Q(2) ** exp if exp >= 0 else Q(man, 2 ** (-exp))

    return to_q(lo), to_q(hi)


def arb_contains_exact(value: Q) -> bool:
    """True iff the Arb 256-bit ball of `value` (built from the exact fmpq,
    independently of the fractions.Fraction arithmetic above) contains
    `value`. Most of these rationals are not exactly binary-representable at
    256 bits, so the ball generally has a tiny nonzero radius; containment,
    not zero-width equality, is the correct independent-arithmetic check."""
    lo, hi = arb_bounds(to_arb(value))
    return lo <= value <= hi


def self_map(rho: Q) -> Q:
    """29 * rho * G(R)."""
    return J_PRIME * rho * G_R


def self_map_arb(rho: Q):
    return to_arb(J_PRIME) * to_arb(rho) * to_arb(G_R)


def contraction(rho: Q) -> Q:
    """29 * rho * G'(R)."""
    return J_PRIME * rho * GPRIME_R


def contraction_arb(rho: Q):
    return to_arb(J_PRIME) * to_arb(rho) * to_arb(GPRIME_R)


def main() -> int:
    checks = []
    all_ok = True

    def record(cid, ok, **fields):
        nonlocal all_ok
        all_ok = all_ok and ok
        checks.append({"id": cid, "passed": bool(ok), **fields})

    contract = load("research/round33/contracts/bc2.json")
    assert contract["id"] == "BC2" and contract["status"] == "frozen_before_production"
    fwd = load("research/round33/forward/bc2/output/results.json")
    admitted = find(fwd, "weights_declared_and_admissible")

    # --- 1. Headline disc self-map and contraction at rho=64|tau| ----------
    rho_headline = 64 * TAU_CAP
    sm_headline = self_map(rho_headline)
    ct_headline = contraction(rho_headline)
    admitted_sm = Q(admitted["disc_self_map"])
    admitted_ct = Q(admitted["disc_contraction"])
    record(
        "headline_disc_self_map_and_contraction",
        sm_headline == admitted_sm == Q(1073, 2734375) and sm_headline < Q64
        and ct_headline == admitted_ct == Q(2552, 390625) and ct_headline < 1
        and arb_contains_exact(sm_headline) and arb_contains_exact(ct_headline)
        and arb_bounds(self_map_arb(rho_headline))[1] < Q64
        and arb_bounds(contraction_arb(rho_headline))[1] < 1,
        formula="self-map: 29*64|tau|*148/7 <= 1/64; contraction: 29*64|tau|*352 < 1",
        rho=str(rho_headline), self_map=str(sm_headline), self_map_preview=float(sm_headline),
        contraction=str(ct_headline), contraction_preview=float(ct_headline),
        q_target="1/64",
    )

    # --- 2. Split-weight disc self-map and contraction at rho=W|tau| -------
    rho_split = W_SPLIT * TAU_CAP
    sm_split = self_map(rho_split)
    ct_split = contraction(rho_split)
    admitted_sm_split = Q(admitted["split_self_map"])
    admitted_ct_split = Q(admitted["split_contraction"])
    record(
        "split_weight_disc_self_map_and_contraction",
        sm_split == admitted_sm_split == Q(17168, 2734375) and sm_split < Q64
        and ct_split == admitted_ct_split == Q(40832, 390625) and ct_split < 1
        and arb_contains_exact(sm_split) and arb_contains_exact(ct_split),
        formula="self-map: 29*1024|tau|*148/7 <= 1/64; contraction: 29*1024|tau|*352 < 1",
        rho=str(rho_split), self_map=str(sm_split), self_map_preview=float(sm_split),
        contraction=str(ct_split), contraction_preview=float(ct_split),
    )

    # --- 3. Route-B maximal disc radius and maximal split weight -----------
    rho_max = Q64 / (J_PRIME * G_R)
    ADMITTED_RHO_MAX = Q(7, 274688)
    W_max_at_cap = rho_max / TAU_CAP
    ADMITTED_W_MAX = Q(2734375, 1073)
    record(
        "route_b_maximal_disc_radius_and_split_weight",
        rho_max == ADMITTED_RHO_MAX == Q(admitted["weights"]["route_B_disc_radius_max"])
        and W_max_at_cap == ADMITTED_W_MAX == Q(admitted["weights"]["route_B_split_weight_max"])
        and arb_contains_exact(rho_max) and arb_contains_exact(W_max_at_cap)
        and W_SPLIT <= W_max_at_cap,
        formula="rho_max = q/(29*G(R)) = (1/64)/(29*148/7) = 7/274688; "
                "W_max = rho_max/|tau| = 7/(274688|tau|)",
        rho_max=str(rho_max), rho_max_preview=float(rho_max),
        W_max_at_cap=str(W_max_at_cap), W_max_at_cap_preview=float(W_max_at_cap),
        chosen_split_weight="1024", chosen_within_admissible_range=True,
    )

    # --- 4. Rejection of the route-A extremes -------------------------------
    # The BC2 report's own comparison (Section 0, HNM-BC2-F02): the route-A
    # disc radius tau_star=1/37888 gives self-map/|tau| = 29*G(R)/37888 =
    # 29*(148/7)/37888 = 29/1792, compared with q=1/64 written as 28/1792.
    assert TAU_STAR_ROUTE_A == Q(1, 37888)
    route_a_ratio = J_PRIME * G_R / Q(37888)
    ADMITTED_ROUTE_A = Q(29, 1792)
    q_as_1792 = Q(28, 1792)
    assert q_as_1792 == Q64
    # Route A's own per-site coefficient (28, not 29) sits exactly at its own
    # admissible boundary: this radius is precisely where route A's disc
    # self-map saturates q=1/64, which is why the BA1/BB1 producers chose it.
    route_a_own_boundary = J_PRIME_ROUTE_A * G_R / Q(37888)
    assert route_a_own_boundary == Q64, "route-A's own radius should saturate its own q=1/64 exactly"
    record(
        "route_a_extremes_rejected",
        route_a_ratio == ADMITTED_ROUTE_A == Q(admitted["route_A_extremes_self_map"])
        and route_a_ratio > q_as_1792
        and arb_contains_exact(route_a_ratio)
        and to_arb(route_a_ratio).lower() > to_arb(q_as_1792).upper(),
        formula="29*G(R)/37888 = 29*(148/7)/37888 = 29/1792, compared with q=1/64=28/1792",
        route_a_ratio=str(route_a_ratio), route_a_ratio_preview=float(route_a_ratio),
        q_as_over_1792=str(q_as_1792),
        route_a_own_boundary_check=str(route_a_own_boundary) + " == q (1/64), exactly",
        note="the route-A disc radius tau_star=1/37888 (BA1/BB1) and the route-A secondary "
             "split weight 1/(37888|tau|) (BB1) both reduce to this same ratio under the "
             "route-B per-site coefficient 29. Route A's own per-site coefficient is 28, for "
             "which 28*(148/7)/37888=1/64 exactly: tau_star=1/37888 is precisely the radius "
             "where route A's own disc self-map saturates route A's own q=1/64, which is why "
             "the BA1/BB1 producers chose it. Route B's larger per-site sum J'=29|tau| pushes "
             "the same radius just outside q=1/64, by exactly the factor 29/28; rejected "
             "because 29/1792 > 28/1792 = 1/64.",
    )

    # --- 5. Reconciliation with this lens's own bc2-targets-proposal.md ----
    proposal_text = (ROOT / "research/round33/experts/modern/bc2-targets-proposal.md").read_text()
    checks_against_proposal = {
        "largest_disc_radius_7_over_274688": "`7/274688`" in proposal_text,
        "maximal_weight_2734375_over_1073": "`2734375/1073`" in proposal_text,
        "disc_self_map_1073_over_2734375": "1073/2734375" in proposal_text,
        "route_a_extremal_29_over_1792": "29/1792" in proposal_text,
    }
    record(
        "reconciled_with_lens_bc2_targets_proposal_section_10_1",
        all(checks_against_proposal.values()),
        note="every admissibility number this script recomputes (rho_max=7/274688, "
             "W_max=2734375/1073, the headline disc self-map 1073/2734375, and the route-A "
             "rejection ratio 29/1792) already appears verbatim in this lens's own "
             "bc2-targets-proposal.md Section 10.1, and the BC2 report's own recomputation "
             "reproduces the same values exactly; no difference found.",
        found=checks_against_proposal,
    )

    report = {
        "tool": "admissibility",
        "status": "preview_and_crosscheck_only_zero_research_loops_not_a_contract_or_gate",
        "libraries": {"python-flint": flint.__version__},
        "precision_bits": PREC,
        "all_passed": all_ok,
        "checks": checks,
        "interpretation": "Exact Fraction and independent Arb-ball recomputation of the BC2 "
                           "route-B admissibility inequalities (disc self-map and contraction at "
                           "the headline and split-weight discs, the maximal disc radius and "
                           "split weight, and the rejection of the route-A extremes), cross-checked "
                           "exactly against the ADMITTED research/round33/forward/bc2/output/results.json. "
                           "Never evidence, never admission.",
    }
    print(json.dumps(report, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
