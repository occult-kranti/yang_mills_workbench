# Historical lens (Newton/Tesla) update — Round32 sub-round 2 to 3

2026-09-24. Read `advisor/aw1-gate.json`, `skeptic/aw1.md`, `forward/aw2/report.md`, `skeptic/aw2-independent-derivation.md`, own `update-1.md`, `advisor/plan.json`, `contracts/ax1.json`+`ax2.json` (drafts), `advisor/selection-ax1.md`. AW2's post-comparison review is running; treated as provisional throughout. No historical endorsement, no invented quotation.

## 1. What sub-round 2 established, in lens terms

**Newton (analysis before synthesis).** AW1 itemized the exact first-order coefficient `tau/144` and the second-order bound `K_2^+` separately and proved each before AW2 was allowed to charge anything; AW2 then only *instantiated* that admitted formula at the frozen cap `tau=1e-8` — no new charging, no re-derivation, order preserved exactly as the method requires. The three independent exact-tier itemizations of `K_2^+` (forward, reverse, skeptic) that disagreed by refinement only, not by error, are themselves an analysis-before-synthesis result: the largest valid value was bound, not averaged.

**Tesla (the flip mirror as a control, not a doubled reading).** AW1's link-flip lemma gives `omega_{-tau}(W)=-omega_tau(W)` at the zero triple; AW2 uses this correctly to produce the `-1e-8` enclosure as an explicit **replay**, both in its own text and the skeptic's, never counted as a second confirmation. That is the right instrument discipline: one measurement, one mirror, no double-counting the margin.

**Tesla (source/load/clock accounting of a static effect).** Source = the 82 faces meeting cover `R`, of which only `f=W` pairs nonzero; load = `R={0,e_z}` with its four incident stars; clock = `s=alpha t_E/hbar`. Fully budgeted: `omega_{+-1e-8}(W)` is enclosed to `[6.911e-11, 6.978e-11]` (and its negative), zero excluded with margin ~206 — a complete, exact-rational static equal-time accounting, sub-labelled `static_not_dynamic`.

**Not established.** No dynamical correction, mass shift or susceptibility (explicitly excluded, and correctly so); the centered correlation `C(s)` shift stays unresolved (AV2's `reference_unresolved` still stands — AW1 only proved its first-order term vanishes and its `tau^2` constant is *not* uniform in `N`); nothing beyond the zero-selected-triple family, cover `R`, and `|tau|<=1e-8`; no uniqueness, rate in `N`, uniform Wilson theory, weak coupling, continuum or priority claim.

## 2. Goals for sub-rounds 3–5

- **AX1/AX2 (uniform): keep, unchanged order.** AX1 depends on AW1's coefficient and dictionary, not on AW2's still-provisional numeric enclosure; nothing in sub-round 2 touches route B or `tau=96/g^4`.
- **AY1/AY2 (state): keep.** AW2's exclusion is a fact about the zero-triple family only; it bears nothing on the loop-3 disagreement about limiting states that AY1 is to settle.
- **AZ1/AZ2 (continuum): keep, one addition (repeating update-1).** AZ1 should log `resolved_interaction_shift`-at-cap as a plotted waypoint on the `tau` trajectory, not a target; AZ2's finite-graph coefficients should be checked against the now-admitted `tau/144 + K_2^+ tau^2` formula as an external sanity target, not a premise.

## 3. Improvements to the AX1/AX2 drafts

- **Route-B grouping.** Item 2 cites the enlarged sum but does not require, as AW2's `wrong_face_control` did, an explicit rejection of double-counting a selected face in both the whole-star sum and its single-factor group. Add a `route_b_no_double_count` control.
- **J_0 re-freeze.** Pin `J_0'=29/10^8` and both contraction rationals (`1073/175000000<1/64`, `319/1562500<1`) verbatim in the contract text, as `K_2^+` was pinned for AW2 — AW1's review (N8) found silent undercounts caught only by cross-comparison; a producer-recomputed `J_0'` should not be trusted alone.
- **Incidence counts.** The "96 per four anchors" and "168 for R" figures are asserted, not itemized. Require a face-owner-set table analogous to AV1/AW1's 15-set/49/82 enumeration, plus one positive numeric control in the AW2 style (e.g. an exact `||W Omega_R||` recomputation under route B).
- **Uniform label.** `uniform_label_strong_coupling` exists; strengthen it to explicitly reject any wording that reads the large numeric value `g^4=9.6e9` as "weak coupling" — the dictionary `tau=96/g^4` makes large `g^4` *strong* coupling, and this is exactly the kind of unit confusion the flip-sign literal display caught in AW1 (N2, non-blocking but instructive).
- **First-order unchanged.** Item 6 says `omega(W)^{(1)}=+-tau/144` "unchanged (cite AW1)" — require an explicit proof step that the selected faces entering the interaction under route B still satisfy `E[W^2 W_g]=0`, not a bare citation.
- **AX2.** `D_prime` is a placeholder ("<AX1 admitted tier>"); require it hash-bound to the AX1 gate once frozen (as AW2 bound `K_2^+`), and add `tier_mixing_rejected` to AX2's own control list (AX1 has it; AX2 does not, though it inherits AX1's tier).

## 4. Web check

WebSearch (2026-09-24): "rigorous strong-coupling expansion uniform Kogut-Susskind SU(2) Hamiltonian lattice gauge theory 2025 2026" — no matching rigorous 2025–2026 result for this exact family (fixed-spacing, exact-rational strong-coupling perturbation theory of the uniform 3+1D SU(2) Kogut–Susskind Hamiltonian). Nearest hits are 2025 quantum-simulation papers on truncated/finite-dimensional link Hilbert spaces (dimer/spin-chain phases under strong-coupling expansion) — a different, digitization-oriented question. Abstracts only, not read, not used as premises.

## 5. Assistant tests wanted after sub-round 3

- Independent enumeration of the route-B face counts (24 per factor = 21 omitted + 3 selected; 96 per four anchors; 168 meeting `R`) from the I1 table, extending S2, diffed against AX1's claimed counts.
- Independent recomputation of `J_0'=29|tau|` and both exact contraction inequalities from the enlarged interaction, bit-for-bit against AX1's admitted values.
- Independent replay of the dictionary `tau=96/g^4` and the exact rational `g^4` at the cap.
- A route-B double-count control replay confirming no selected face appears in both the whole-star and single-factor sums.
- Independent recomputation of AX2's `E'=M_0(D'+D'^2)+k'M_1` from AX1's exact `D'` and `k'=51|tau|/4`, diffed against AX2's exported value.
