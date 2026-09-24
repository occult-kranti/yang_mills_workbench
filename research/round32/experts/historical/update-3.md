# Historical lens (Newton/Tesla) update — Round32 sub-round 3 to 4

2026-09-24. Read `advisor/ax1-gate.json`, `skeptic/ax1.md`, `forward/ax1/report.md`, `reverse/ax1/report.md`, own `update-2.md`, `advisor/plan.json`, drafts `contracts/ay1.json`, `ay2.json`, `az1.json`, `az2.json`, `advisor/selection-ay1.md`. AX2 (preview radius ~1.9e-7) treated throughout as provisional, single+skeptic, not yet closed. No historical endorsement, no invented quotation.

## 1. What sub-round 3 established, in lens terms

**Newton (analysis re-done, not rescaled).** Route B forced a genuine re-derivation, not a relabelling of AV1's constants: the source/load ledger is 21 omitted faces per star plus one single-factor group of 3 selected faces, giving `J'=29|tau|` per site — a new count that failed the old `J_0` and required AM2's contraction machinery to be re-run from a re-frozen `J_0'=29/10^8`, with its own exact inequalities `1073/175000000<1/64` and `319/1562500<1` proved fresh, not inherited. That re-freeze is properly called a new theorem, not a corollary.

**Tesla (source/load/clock ledger on the cover).** Nine interaction groups meet `R` — 7 whole stars plus 2 single-factor groups — charging 88 faces meeting `R` (82 omitted, 6 selected) and 16 inside, every face charged exactly once. That is a complete circuit accounting, the same discipline as AW2's mirror reading: nothing left off the ledger, nothing double-billed.

**Exact count over bound.** The theorem is 52 faces per factor (49+3); 96 (4×24) and 168 (7×24) are outer envelopes only, both producers reject them as exact, and the gate records this correctly.

**Mirror transferred, not repeated.** `U_E H_N(tau) U_E^*=H_N(-tau)` carries over to route B verbatim, because the tie `kappa=tau` and the odd meeting of `E` with every plaquette (selected faces included) survive the regrouping; `-tau` remains a replay of one instrument reading, not a second confirmation, exactly as in AW2.

**Not established.** No uniform `K_2` for route B (only the finite-box parity theorem transfers; `C_N`'s tau^2 constant is still not uniform in `N`); no uniform Wilson-mean sign certificate; no continuum, weak coupling, uniqueness, whole-sequence convergence or rate in `N`; AX2's ~1.9e-7 is a single-producer preview pending its own skeptic replay.

## 2. Goals for sub-rounds 4–5

- **AY1: change direction to single+skeptic, not paired as drafted.** Its two load-bearing constants — `2D` and the first-order density — are read from AV1's and AW1's already independently-paired-admitted values, not re-derived by a genuinely different route; running two full producers here duplicates arithmetic already checked twice upstream, the same reasoning that made AX2 single+skeptic on AX1's `D'`. Keep a second independent pass only for the one new claim: that the padding-box family actually satisfies AM2/AV1's premises.
- **AY2 (statement+skeptic): keep as drafted**, unchanged in scope and direction.
- **AZ1 (continuum statement, statement+skeptic): keep as drafted**, unchanged.
- **AZ2 (finite-graph loop): stays.** Its labels (`model_is_finite_graph`, `no_transfer_to_aq`, `own_free_reference`) already fence it as a labelled comparison, in the same spirit as the panel's own cautionary cases; no goal change needed.

## 3. Concrete improvements to the drafts

- **AY1, two families.** Require an itemized contraction proof for the padding-box family at the same `J_0` as AV1, in the AX1 face-owner-table style — "AV1 premises available for each finite volume" is currently asserted, not shown.
- **AY1, topology.** Name two topologies, not one: trace norm on `B(H_R)` for fixed finite `R` for the closeness bound, and a separately stated metric (operator or strong) for the dynamics comparison on compact time windows; forbid reading either as a statement about the GNS-completed infinite-volume topology.
- **AY1, first-order density.** Require `rho^(1)_R` to be written as the literal AW1 `c^(1)` coefficient, cited not re-derived, with "boundary-independent" defined precisely as unchanged across `N` and across family once the star is interior — not independent of where `R` sits.
- **What "quantitative boundary comparison" may honestly mean.** A closeness bound (`2D`) plus one matching exact first-order term between two named finite constructions; it is not a statement about which boundary condition the infinite-volume theory selects, and the report should say once, explicitly, that it is not a variational principle over boundary prescriptions.
- **AZ1.** Pin one control distinguishing the two senses of "uniform" already in play: the fixed-`a` gap `alpha/16` is uniform in volume `N` but not in `a` — the report must not let these drift within one sentence.
- **AZ2.** Require the coupling-to-`alpha` map for `tau_FG` to be stated explicitly wherever `1/144` is compared, and add a no-post-hoc-grid-point control (the panel's own 1952 cautionary case) so no grid value is read as chosen to match the Z^3 coefficient after the fact.

## 4. Web check

WebSearch (2026-09-24), two queries on rigorous 2025–2026 boundary-independence/uniqueness results for gapped lattice-gauge Hamiltonians: no matching theorem for this exact question found. Nearest items, abstracts only, not read as premises: "Generic Hilbert Space Fragmentation in Kogut–Susskind Lattice Gauge Theories" (arXiv:2502.03533, Feb 2025) — a caution, not a match: it reports Hilbert-space fragmentation in a different (non strong-coupling-perturbative) Kogut–Susskind regime, relevant only as a reminder that "unique ground state" claims outside a proved regime can fail structurally; and a Lieb–Schultz–Mattis-type gauge-constraint result (pith.science summary of arXiv 2506.13606) noting LSM obstructions to trivial gapped ground states under translation/reflection symmetry, again not this workbench's model or regime.

## 5. Assistant tests wanted after sub-round 4

- Independent recomputation of the closeness constant `2D` from the AV1-admitted `D` (not AX1's), diffed against AY1's exported value.
- Independent verification that the padding-box family's contraction inequality is proved at AV1's `J_0`, not merely asserted by analogy to the whole-star family.
- Independent recomputation of the second-order difference bound `2K_2' tau^2` from the AW1 remainder items, bit-for-bit against AY1.
- A textual diff confirming AY1's `rho^(1)_R` is the cited AW1 `c^(1)` term, not an independently re-derived coefficient.
- A control replay confirming the mandatory sentence-template fields (`uniqueness_claimed:false`, `whole_sequence_claimed:false`, `rate_claimed:false`) appear in both producer reports and the gate.
