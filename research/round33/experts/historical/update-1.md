# Historical lens (Newton/Tesla) update — Round33 sub-round 1 to 2

2026-09-24. Read `advisor/ba1-gate.json`, `advisor/ba2-gate.json`, `skeptic/ba1.md`, `skeptic/ba2.md`, `advisor/plan.json`, `advisor/deliberation-2.md`, `experts/modern/bb-targets-proposal.md`, own `loop2-response.md`. `experts/historical/assistant-1/README.md` is not yet present; the advisor records it in panel update 1. No historical endorsement, no invented quotation.

## 1. What sub-round 1 established, in lens terms

**Newton (exact limiting arguments).** BA1 proved, not posited, that the AM2 creation coefficients on supports meeting `R` are Cauchy in `N`: headline pair `q=1/64` with `K=49/111790368` (~4.3832e-7, reverse `analytic_disc` route, a Schwarz estimate on the disc `|z|<=64|tau|`; margin 1.1407 against `1/2000000`), also certified by the forward `weighted_norm` route (labelled, `2734375/12204185915601`); floor pair `q=148/390625=37888|tau|`, the per-step ball ratio, `K=49/2018304` (margin ~3432). BA2 proved the algebraic Heisenberg-dynamics comparison, forward `K_cmp=3969/155720800000000` (margin 2.354) with a reverse second route (margin 4.041), and the honest `O(1/N)` within-family Cauchy estimate for both families over every `M>N` — never the exponential rate the polynomial Lieb–Robinson function cannot give. The F2 limit dynamics is identified with AQ1's `T_theta` on the whole quasi-local algebra. Both my loop-2 edits landed: BA1's limitations enumerate the l-infinity/l1 diameter tables on `Lambda_2..Lambda_4` I asked for, and BA2's decision text derives that the F2 padding on-site terms "factor out of the evolution exactly and are never charged" rather than being silently dropped.

**Tesla (source/load/clock/kernel).** BA1's ledger: source = the coefficients on supports meeting `R`; kernel = the anchored norm, weighted or analytic; clock = the coarse step `N`. BA2's ledger: source = the `28N(5N+1)` extra faces plus the padding on-site terms (both charged, the second shown to vanish); load = `A in B(H_R)`, `||A||<=1`; clock = `theta=alpha t/hbar`, window `|theta|<=8`; kernel = the Duhamel integral with the F-norm Lieb–Robinson bound, quoted verbatim from the committed Nachtergaele–Sims excerpt. Neither certificate folds an omitted channel into another; the crude tiers are retained as failures, not discarded.

**Not established.** State decay: `state_decay_claimed` is false in both gates; nothing about the reduced density `rho_R`, only the coefficients (BA1) or the algebraic evolution of one observable (BA2). Uniqueness: `uniqueness_of_ground_state_claimed` is permanently false. Anything uniform in `a`: `rate_in_a_claimed` is permanently false; every rate is in `N` at fixed spacing.

## 2. Goals for sub-round 2

**Keep BB1 (paired: `polymer_kp` forward / `iterated_split` reverse) and BB2 (paired: `nested_telescoping` / `union_comparison`).** These are exactly the "coefficient decay done, state decay next" order this lens's own Round33 loop-1 memo set out, and BA1's thin margin does not change the feasibility reading: the state part remains a standard cluster expansion with room to spare at the cap (modern lens's own ledger, §2.7).

**View of the modern proposal's targets.** `q=1/64` headline: right, since the reduced-density routes cannot reach the floor for genuinely different reasons in each route — the split route's diameter weight is cubic in support size, forcing `q>=2 q_min`, and the polymer route's cluster-weight condition forces `q>q_min e^{4b}` — both documented derivations, not assertions, and this lens will require the assistant to check them (Section 4). `q2=4 q_min` as an optional, explicitly labelled secondary pair: acceptable, never as the headline. `C<=4e-6`: correct, and directly answers this section's next point. Keeping the correlation bound (BB2 item 5) as three separate named constants (`C_dyn`, `c_site`, `C'`) rather than one lumped sum: this is the Tesla discipline of a complete-device ledger applied again, and it is load-bearing here — the preview table shows the state term exceeding the dynamics term at `N=5`, so a single constant would hide which channel actually binds.

**The thin BA1 margin (1.14) and what it implies.** `contract_rules` already states the margin-of-2 rule is a freeze-time property against the recorded preview, not an acceptance condition, so BA1's 1.14 does not itself invalidate BA1. But BB1/BB2 use BA1's admitted reverse `K=49/111790368` (~4.38e-7) as an input, roughly double the loop-1 preview (~2.2e-7) the modern lens used to draft an earlier `2e-6` candidate target — which the proposal's own §7 computes at margin ~1.14 and explicitly says not to freeze. The `4e-6` target (margin ~2.28) is the correct response: since a thin input margin has already been spent once, the downstream target must not spend it again.

## 3. Concrete requirements for the BB1/BB2 contracts

- **Fixed-N boundary-condition comparison, named as its own item.** As flagged in this lens's `loop2-response.md` §1: a successful BB1/BB2 Cauchy chain (two different `N`) is not the same construction as comparing two different exterior conditions at the same `N` (needed for a genuine Dobrushin/HTW-type uniqueness reading). The BB1 and BB2 contracts must name this fixed-`N`, changed-exterior comparison as its own required item if attempted, never let it be assumed to follow automatically from volume growth.
- **Jung's gate-field templates.** `whole_sequence_claimed` paired with a non-empty `whole_sequence_scope` naming family and region; `common_limit_claimed` paired with `common_limit_families`; `translation_invariance_claimed` true only with a scope naming coarse translations and the construction; BB2's new `dynamics_level` value `correlation_functions_compact_window` registered in `plan.json`'s vocabulary before freeze, the same way `sub_labels_allowed` was extended twice already.
- **The P7 isolation rule.** BB1's reverse producer must receive neither the modern memo, the skeptic triage, nor the BB targets proposal itself — the same "reverse producer isolation" discipline BA1's `reverse_premise_isolation` control already enforced and both producers passed. The reverse route (`iterated_split`) must be a genuinely different construction from the forward (`polymer_kp`), not a relabelling, exactly as BA1's two routes independently converged on the same bound.

## 4. Tests for the assistants after sub-round 2

1. Replay the assembly formulas `C_split` and `C_poly` (bb-targets-proposal §7) with BA1's admitted reverse `K` substituted, and confirm the resulting margins match the proposal's `1.75e-6`/`4e-6` figures exactly in `Fraction` arithmetic.
2. Verify computationally, not by assertion, that the diameter weight forces `q>=2 q_min` for `iterated_split` and the cluster-weight condition forces `q>q_min e^{4b}` for `polymer_kp` — the "floor not reachable" claim in Section 2.
3. Extend the padding-audit script from BA2 to BB1's region form: enumerate `d_Y` for a finite complete-factor region `Y` on `Lambda_2`..`Lambda_4` and cross-check against the contract's `c_site |Y| e^{|Y|/10^8} q^{d_Y}` formula.
4. A ledger-completeness auditor over the BB1/BB2 forward/reverse reports against the proposal's six required derivations and ten fixtures, flagging any uncharged item.

## 5. Sources read this sub-round

None. No new WebFetch or WebSearch was run this sub-round; `sources.json` is unchanged.

## 6. Closing

This lens admits nothing and counts zero research loops.
