#!/usr/bin/env python3
"""Independent numeric check of the BB1 forward Kotecky-Preiss condition (PREVIEW ONLY).

Round33 sub-round 2, modern (Penrose/Feynman) lens, assistant-2. **Zero
research loops. This is a preview, not a proof, and never evidence for any
gate.** It never imports `research/round33/forward/bb1/check.py` (which
this script has not read); every combinatorial routine below is written
fresh from the definitions and lemma statements in
`research/round33/forward/bb1/report.md` Sections 3-6 (families, Y-clusters,
polymers, the exploration-tree Lemma 4.1/4.2, the Kotecky-Preiss
Proposition 6.2), on a small finite example of this script's own choosing
-- distinct rational creation norms on a 5-site chain, never the forward
producer's own fixture numbers.

**What the forward report actually needs proved, and what it cites.**
The forward report's own Attribution paragraph (report.md, top) states,
verbatim: "Hard-core polymer (cluster) expansions and the Kotecky-Preiss
criterion are established mathematics: R. Kotecky and D. Preiss, Cluster
expansion for abstract polymer models, Comm. Math. Phys. 103 (1986)
491-498, and the decay-function form written as in D. Ueltschi, Cluster
expansions and correlation functions, Moscow Math. J. 4 (2004) 511-522.
They are cited, not re-proved and not machine-checked; the primary sources
were not re-inspected in this session, and the statement used (Theorem 6.1)
is transcribed as known to this producer." No excerpt of either paper is
committed anywhere under `research/round33/sources/` (that directory holds
only the Nachtergaele-Sims excerpt used by BA2/BB2) or elsewhere in this
round. So:
  - **Theorem 6.1** (the Kotecky-Preiss cluster-expansion CONCLUSION: Z!=0,
    log Z an absolutely convergent cluster sum) is CITED, not proved and
    not machine-checked in the forward packet, and not committed as an
    excerpt anywhere in this round -- the forward report is *not*
    self-contained on it.
  - **Proposition 6.2** (the VERIFICATION that the forward's own choice of
    a(gamma)=a|supp gamma|, d(gamma)=mu*sum(diam K) satisfies Theorem 6.1's
    HYPOTHESIS at its declared weights) *is* proved in full inside the
    forward report, from its own Lemma 4.2 (the exploration-tree count),
    which is itself proved in the report and audited by brute-force
    enumeration on a five-site chain in the forward's own `check.py`
    (report.md S4: "233 polymers; 275 and 856 Y-clusters"). So the forward
    report *is* self-contained on the hypothesis-verification step, and
    relies on citation only for the abstract KP theorem's conclusion.

This script:
  (1) independently re-derives, on its OWN small finite chain (fresh code,
      own numbers), the combinatorial content of Lemma 4.1/4.2 (P1): that
      the sum over polymers through a marked site x of the product of
      per-support weights is bounded by sigma^2, sigma = the per-site
      mixed-weight sum -- a brute-force check of the *lemma the forward
      report needs*, not of the cited external theorem;
  (2) evaluates, at the forward's own DECLARED headline and secondary
      parameters (tau_bar, a=tau_bar^2, v, w, e^b=1001/1000), the two
      admissibility side-conditions Theorem 6.1's hypothesis needs
      (a<=2b, v<=w) with their numeric margins, and confirms the KP
      series bound itself, sigma^2<=a, holds with margin *exactly* 1 (by
      the forward's own construction a:=tau_bar^2, not by genuine slack);
  (3) states plainly, per the instructions above, that this is a preview
      of the hypothesis-verification arithmetic and a fresh finite-graph
      audit of the exploration-tree lemma, never a re-proof or independent
      verification of Kotecky-Preiss 1986 / Ueltschi 2004 themselves.

Run: `python3 -B kp_condition.py`
"""
import json
from fractions import Fraction as Q
from itertools import product


# --------------------------------------------------------------------------
# Part 1: fresh finite-graph brute-force audit of Lemma 4.1/4.2 (P1)
# --------------------------------------------------------------------------
# A small 5-site chain (0..4), with two candidate support types: singletons
# {i} and adjacent pairs {i,i+1}, both of coarse l-infinity diameter <=1
# (matching report.md's "owner sets have at most 3 sites and diameter 1").
# Norms are this script's OWN choice of concrete rationals -- not the
# forward producer's fixture numbers (report.md S11 uses a four-qutrit
# system and a separate five-site "taubar=539/1500" toy; both untouched
# here).
SITES = range(5)
NORMS = {
    (0,): Q(1, 90), (1,): Q(1, 80), (2,): Q(1, 70), (3,): Q(1, 85), (4,): Q(1, 95),
    (0, 1): Q(1, 200), (1, 2): Q(1, 150), (2, 3): Q(1, 160), (3, 4): Q(1, 190),
}
SUPPORTS = list(NORMS.keys())


def sigma_bound() -> Q:
    """sigma = max_u sum_{I ni u} ||c_I|| (the mixed-weight per-site sum)."""
    best = Q(0)
    for u in SITES:
        s = sum(NORMS[I] for I in SUPPORTS if u in I)
        best = max(best, s)
    return best


def tilings(remaining: frozenset):
    """All partitions of `remaining` into pairwise-disjoint supports from SUPPORTS."""
    if not remaining:
        yield ()
        return
    first = min(remaining)
    for I in SUPPORTS:
        if first in I and set(I) <= remaining:
            rest = remaining - set(I)
            for tail in tilings(rest):
                yield (I,) + tail


def connected(members) -> bool:
    """members: list of (side, support-tuple). Connected iff the overlap graph
    (edge when two supports on OPPOSITE sides, or the same support reused,
    intersect) is connected. Two members on the SAME side never overlap
    (they come from a tiling, hence pairwise disjoint by construction), so
    only cross-side intersections can create edges, exactly as in
    report.md S3 ("I in F and I' in F' are joined when they intersect")."""
    n = len(members)
    if n <= 1:
        return True
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for i in range(n):
        side_i, supp_i = members[i]
        for j in range(i + 1, n):
            side_j, supp_j = members[j]
            if side_i == side_j:
                continue  # same-side members never overlap (disjoint tiling)
            if set(supp_i) & set(supp_j):
                union(i, j)
    roots = {find(i) for i in range(n)}
    return len(roots) == 1


def polymer_sum_through_site(x: int) -> Q:
    """Sum over ALL polymers gamma=(F,F') with E(F)=E(F')=:E ni x and a
    connected bipartite overlap graph, of the product of member norms
    (with multiplicity, both sides), per report.md Proposition 3.3 /
    Section 3-4's own definitions -- coded fresh here, not imported."""
    total = Q(0)
    n_polymers = 0
    all_sites = frozenset(SITES)
    # enumerate every nonempty excitation set E containing x that admits at
    # least one tiling (E must be a union of chosen supports)
    for size in range(1, len(all_sites) + 1):
        for E_tuple in _subsets_containing(all_sites, x, size):
            E = frozenset(E_tuple)
            Fs = list(tilings(E))
            if not Fs:
                continue
            for F, Fp in product(Fs, repeat=2):
                members = [("L", I) for I in F] + [("R", I) for I in Fp]
                if not connected(members):
                    continue
                prod = Q(1)
                for _, I in members:
                    prod *= NORMS[I]
                total += prod
                n_polymers += 1
    return total, n_polymers


def _subsets_containing(universe: frozenset, x: int, size: int):
    rest = [s for s in universe if s != x]
    from itertools import combinations
    for combo in combinations(rest, size - 1):
        yield (x,) + combo


# --------------------------------------------------------------------------
# Part 2: the forward's declared REAL headline/secondary parameters
# --------------------------------------------------------------------------
GPRIME_R = Q(352)


def T_exact(rho: Q) -> Q:
    denom = 1 - 28 * rho * GPRIME_R
    assert denom > 0
    return Q(49) * rho / 144 / denom


def forward_taubar(tau: Q, w: Q) -> Q:
    eb = Q(1001, 1000)
    t1 = Q(49) * tau / 144
    what = w * eb ** 4
    Gamma = 28 * tau * what * GPRIME_R
    return w * eb ** 3 * t1 / (1 - Gamma)


def main() -> int:
    checks = []
    all_ok = True

    def record(cid, ok, **fields):
        nonlocal all_ok
        all_ok = all_ok and ok
        checks.append({"id": cid, "passed": bool(ok), **fields})

    # --- Part 1: fresh finite-graph audit of the exploration-tree lemma ----
    sigma = sigma_bound()
    x = 2  # marked site (interior, to exercise both directions of the chain)
    S, n_polymers = polymer_sum_through_site(x)
    margin = sigma ** 2 / S if S > 0 else None
    record(
        "fresh_finite_graph_exploration_tree_audit",
        S <= sigma ** 2,
        model_is_finite_graph=True,
        transfers_to_aq=False,
        note="Own 5-site chain, own rational norms (not the forward producer's fixture "
             "numbers), own fresh enumeration code (report.md's check.py, which uses a "
             "different 5-site fixture and 233 polymers/275+856 Y-clusters, was neither "
             "read nor imported). Verifies Lemma 4.1/4.2's structural claim "
             "'sum over polymers through x of the product of member norms <= sigma^2', "
             "sigma = the per-site mixed-weight sum -- the combinatorial fact Proposition "
             "6.2 needs, independently re-derived on a different concrete instance.",
        sites=list(SITES), marked_site=x,
        n_polymers_through_x=n_polymers,
        sigma_exact=str(sigma), sigma_preview=float(sigma),
        sigma_squared_exact=str(sigma ** 2), sigma_squared_preview=float(sigma ** 2),
        sum_over_polymers_exact=str(S), sum_over_polymers_preview=float(S),
        margin_sigma_sq_over_sum_preview=float(margin) if margin is not None else None,
    )

    # --- Part 2: admissibility side-conditions at the real declared params -
    tau_cap = Q(1, 10 ** 8)
    b_lower = Q(1, 1001)  # e^b = 1001/1000 = 1 + 1/1000 >= e^{1/1001} (b >= ln(1001/1000) >= 1/1001)
    v_headline, w_headline = Q(128), Q(192)
    v_secondary, w_secondary = Q(390625, 296), Q(1171875, 592)

    taubar_headline = forward_taubar(tau_cap, w_headline)
    taubar_secondary = forward_taubar(tau_cap, w_secondary)
    a_headline = taubar_headline ** 2
    a_secondary = taubar_secondary ** 2

    ADMITTED_TAUBAR_HEADLINE = Q(6143393381125, 9196881302842190592)
    ADMITTED_A_HEADLINE = Q(37741282235250459506265625, 84582625698568269021279506561253310464)
    record(
        "declared_parameters_reproduced",
        taubar_headline == ADMITTED_TAUBAR_HEADLINE and a_headline == ADMITTED_A_HEADLINE,
        taubar_headline_preview=float(taubar_headline),
        a_headline_preview=float(a_headline),
        taubar_secondary_preview=float(taubar_secondary),
        a_secondary_preview=float(a_secondary),
        note="tau_bar, a=tau_bar^2 recomputed exactly as in bb1_arb.py (same formulas as "
             "report.md Corollary 5.2 / Proposition 6.2), reproduced here without importing "
             "that file, for a self-contained script.",
    )

    margin_a_le_2b_headline = (2 * b_lower) / a_headline
    margin_a_le_2b_secondary = (2 * b_lower) / a_secondary
    margin_v_le_w_headline = w_headline / v_headline
    margin_v_le_w_secondary = w_secondary / v_secondary
    record(
        "kp_admissibility_side_conditions_margins",
        a_headline <= 2 * b_lower and a_secondary <= 2 * b_lower
        and v_headline <= w_headline and v_secondary <= w_secondary,
        headline={
            "a_le_2b_margin_preview": float(margin_a_le_2b_headline),
            "v_le_w_margin_preview": float(margin_v_le_w_headline),
        },
        secondary={
            "a_le_2b_margin_preview": float(margin_a_le_2b_secondary),
            "v_le_w_margin_preview": float(margin_v_le_w_secondary),
        },
        note="Theorem 6.1's hypothesis (Prop. 6.2) needs a<=2b and v<=w at the declared "
             "weights; both hold with large margin at both pairs. This is a genuine, "
             "non-tautological numeric check (unlike the KP series bound itself, next).",
    )

    record(
        "kp_series_bound_is_definitional_not_slack",
        a_headline == taubar_headline ** 2 and a_secondary == taubar_secondary ** 2,
        note="Proposition 6.2's headline inequality 'sum_{gamma ni x}|w(gamma)|e^{a|supp "
             "gamma|+d(gamma)} <= taubar^2 <= a' has ZERO slack margin on its SECOND "
             "inequality by the forward's own construction: a is DEFINED to equal taubar^2 "
             "exactly (Corollary 5.2/Prop 6.2), not derived as a separate quantity found to "
             "exceed it. The forward report itself states this literally ('a=tau_bar^2'); "
             "reporting a numeric 'margin' greater than 1 for that specific inequality would "
             "misrepresent it as having slack it does not have. The genuine numeric slack in "
             "the forward's KP verification sits entirely in the two side-conditions above "
             "(a<=2b, v<=w) and in the smallness of tau_bar itself (~6.68e-7 at the cap).",
    )

    self_contained = {
        "theorem_6_1_kp_cluster_expansion_conclusion": {
            "self_contained": False,
            "reason": "cited from Kotecky-Preiss 1986 and Ueltschi 2004 'as known to this "
                      "producer'; report.md's own Attribution paragraph states it is "
                      "'cited, not re-proved and not machine-checked'; the primary sources "
                      "were not re-inspected; no excerpt of either paper is committed under "
                      "research/round33/sources/ (which holds only the Nachtergaele-Sims "
                      "excerpt, used by BA2/BB2) or anywhere else in this round.",
        },
        "proposition_6_2_hypothesis_verification": {
            "self_contained": True,
            "reason": "proved in full inside report.md Section 6 from the report's own "
                      "Lemma 4.2 (exploration-tree count, Section 4), itself proved and "
                      "audited by brute-force enumeration on a five-site chain in the "
                      "forward producer's own check.py (report.md S4: 233 polymers, 275 "
                      "and 856 Y-clusters). This script's Part 1 above independently "
                      "re-derives the same combinatorial fact on a different finite example.",
        },
    }
    record(
        "forward_report_self_containment_on_kp",
        True,  # a factual finding, not a pass/fail numeric check
        self_containment=self_contained,
    )

    report = {
        "tool": "kp_condition",
        "status": "preview_only_zero_research_loops_not_a_proof_of_kotecky_preiss",
        "all_passed": all_ok,
        "checks": checks,
        "interpretation": "A finite-graph, freshly-coded (not imported) audit of the "
                           "exploration-tree combinatorial lemma the forward BB1 producer's "
                           "Kotecky-Preiss verification (Proposition 6.2) depends on, plus a "
                           "numeric evaluation of that verification's two genuine "
                           "side-condition margins (a<=2b, v<=w) at the forward's own declared "
                           "headline and secondary parameters. This is a preview, not a proof: "
                           "it re-derives none of Kotecky-Preiss 1986 or Ueltschi 2004's own "
                           "results, and the forward report itself cites, rather than proves "
                           "or machine-checks, the abstract Kotecky-Preiss theorem (Theorem "
                           "6.1) it applies. Nothing here is evidence for, or against, the "
                           "BB1 gate.",
    }
    print(json.dumps(report, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
