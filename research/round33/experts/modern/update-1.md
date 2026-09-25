# Modern lens (Penrose/Feynman), Round33 sub-round 1 update

2026-09-24. `round33_subround1_update`; not a contract, loop or gate. Human project author: Hruday N M (BUNZEEY). This lens is a model agent with ancestry shared with every other agent in the round, so this is not external review. Read this update: `advisor/ba1-gate.json`, `advisor/ba2-gate.json`, `skeptic/ba1.md`, `skeptic/ba2.md`, `advisor/plan.json`, `advisor/deliberation-2.md`, own `memo.md` §2, `loop2-response.md`, `bb-targets-proposal.md`. `experts/modern/assistant-1/README.md` is not yet present; the advisor records it in panel update 1. The arithmetic below is re-checked, not re-derived; it is a preview cross-check, not evidence for any gate.

## 1. Technical assessment of sub-round 1

**Feynman reading.** BA1 computed the constants this lens's own §2.4 predicted the shape of: headline `q=1/64` with `K=49/111790368` (~4.3832e-7, reverse `analytic_disc`, margin 1.1407 against `1/2000000`), also certified labelled by the forward `weighted_norm` route (`2734375/12204185915601`); floor `q=148/390625=37888|tau|` — this lens's own predicted per-tree-step decay ratio `S_*^{-1}` — with `K=49/2018304`, margin ~3432. Both are consistent with `S_*=R/(J_0 G(R))≈2639.36` at the cap. BA2's comparison coefficient, `K_cmp=3969/155720800000000` (~2.5488e-11), matches this lens's own closed form `254016 tau^2/(1-338688|tau|)` essentially exactly (this lens's loop-1 preview was 2.566e-11; the skeptic's independent reconciliation attributes the ~0.67% gap to two different directed bounds on the same remainder integral, not an error in either). The within-family Cauchy estimate is confirmed `O(1/N)`, not exponential, exactly as this lens's dissent 5 stated it must be with the polynomial `F(r)=(1+r)^-4`.

**Penrose reading.** The reverse `analytic_disc` route is a direct instantiation of this lens's own Route A (§2.4): complex coupling `s`, Cauchy's estimate on a disc, giving the geometric-in-`N` rate. The forward `weighted_norm` route instantiates Lemma W. Both converged on the same statement independently, which is the structural confirmation this lens's §2.7 ledger flagged as the main risk for the coefficient half ("nearly immediate from AM2") — resolved. My one required loop-2 edit (a `basis` field distinguishing `q=1/64` as a construction-specific remainder-to-leading-term bound from the tree-step ratio `q_min`) is present in BA1's decision text and limitations, with the control `ball_radius_not_used_as_tree_decay_ratio`.

**Not established.** State decay of the reduced density (`state_decay_claimed:false` — this is the "standard cluster expansion... main risk" ledger row in my own §2.7, not yet attempted). Uniqueness of any ground state (permanently false). Anything uniform in `a` (permanently false; every rate is in `N` at fixed spacing).

## 2. Goals for sub-round 2

**Keep BB1 (`polymer_kp` forward / `iterated_split` reverse) and BB2 (`nested_telescoping` / `union_comparison`), as proposed in `bb-targets-proposal.md`.** This is my own §3 feasibility ranking (BB1 rank 3, "a standard but new polymer expansion"; BB2 rank 4, "assembly") carried through unchanged; nothing in BA1/BA2 weakens either route.

**My own proposal's targets, restated with the reasons.** Headline `q=1/64`, not the floor `q_min`: neither route reaches the floor for reduced densities — the split route's admitted size control is the diameter, `|I|<=8*2^{diam I}`, cubic in the diameter, forcing weight `2/q<=1/(37888|tau|)` and hence `q>=2 q_min`; the polymer route's far-support sum over ℓ∞ shells converges only if the cluster weight satisfies `q W_c>1`, plus a cardinality factor `e^{4b}` on top, forcing `q>q_min e^{4b}`. At `q=q_min` the polymer sum diverges outright. `q2=4 q_min` is frozen only as a labelled secondary pair, never the headline, because the polymer route's far-support factor is already ~100x larger there. `C<=4e-6`: forced by the admitted BA1 reverse `K` (see next paragraph), with margin 2.28 against the worst preview (`1.753963e-6`, split route on reverse BA1 input). The correlation bound (BB2 item 5) keeps `C_dyn`, `c_site` and `C'` as three separate named constants rather than one sum, because the item-5 preview table shows the state term exceeding the dynamics term at `N=5` — a lumped constant would erase that fact.

**The thin BA1 margin (1.14) and what it implies for BB targets built on the reverse K.** My own loop-1 preview used `K≈2.2e-7`, giving an earlier `2e-6` candidate target a margin of only ~1.14 against the admitted reverse `K` (which is about twice the loop-1 preview). I withdrew that candidate in `bb-targets-proposal.md` §1 ("do not freeze it") precisely because it would compound one thin margin onto another. The `4e-6`/`2e-6` (`c_site`) figures I froze instead carry margin ≥2.24 against every worst-case preview I could construct from the admitted constants. This is the correct response to a thin upstream margin: widen the downstream target, never retune the upstream one.

## 3. Concrete requirements for the BB1/BB2 contracts

- **The six required derivations and ten fixtures already drafted in `bb-targets-proposal.md` §§2, 5** carry over verbatim: the exact AV1 decomposition with both Lipschitz bounds; the per-site diameter-weight charge for the split route (never the product of growing shell sizes); the hard-core polymer representation and KP condition with the mixed-weight cardinality lemma for the polymer route; both routes applied at every site, not only on `R`; the `Q_L -> infinity` pass at fixed `N`; the crude tier reported separately. The ten damaging-mutation fixtures (coefficient decay is not marginal decay; second-order propagation; normalization coupling; straddling supports; the split route's per-site charging; the polymer route's cardinality factor; cutoff order; whole sequence against subsequence; translations; correlation functions) are mandatory, fixture 1 and the zero-free-region control under P7 non-negotiably so.
- **P7 isolation, which this file itself is subject to.** "The BB1 reverse producer must not receive this file, just as it receives neither the modern memo nor the skeptic triage" is my own proposal's own rule (§0), and it must be enforced as an inventory check on the reverse producer's `inputs/`, not by disclosure alone.
- **`dynamics_level: correlation_functions_compact_window` is a new gate-field value** and must be added to `plan.json`'s vocabulary before BB2 freezes — flagged in my own proposal §3 and not yet done.
- **The `assembly` field** (`nested_telescoping`/`union_comparison`) needs its own vocabulary closure under Round32 rule R10 if the advisor wants it treated as a route label; my proposal notes this is not yet in `plan.json`.

## 4. Assistant tests wanted after sub-round 2

- Reconcile `bb-targets-proposal.md` §7's preview constants (`C`, `C'`, `c_site`, `C_dyn`) against the producers' admitted values with directed rounding, and identify, route by route, which one the gate should bind — the same reconciliation pattern the skeptic used for BA1/BA2.
- Independently verify the two "floor not reachable" claims computationally (the cubic diameter bound for the split route; the `q W_c>1` and `e^{4b}` conditions for the polymer route), rather than accepting the assertion.
- Confirm BB1's region form (T2) and BB2's translation-invariance item (item 4) are correctly dropped to `limited` if BA1's general-volume comparison does not itself extend as needed (the P6 dependency) — check this against BA1's admitted general-comparison values (both direct-K and telescoped-labelled forms) rather than assuming the dependency is automatically satisfied.
- Rehearse the item-5 three-constant bookkeeping (`C_dyn`, `c_site`, `C'`) on the `N in {5,...,10}` preview grid, confirming which term binds at each `N`, ahead of BB2 production.

## 5. Sources

None read this sub-round; no new WebSearch or WebFetch was run. `sources.json` is unchanged.

## 6. Closing

This lens admits nothing and counts zero research loops.
