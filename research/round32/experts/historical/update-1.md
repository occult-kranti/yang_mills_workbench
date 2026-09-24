# Historical lens (Newton/Tesla) update — Round32 sub-round 1 to 2

2026-09-23. Read `advisor/plan.json`, `contracts/aw1.json`+`aw2.json` (drafts), own `loop3-signoff.md`, `experts/historical/assistant-1/README.md`+`results.json`, `advisor/av1-gate.json`, `skeptic/av1.md`, `forward/av2/report.md`, `reverse/av2/report.md`, `skeptic/av2-independent-derivation.md`. No historical endorsement, no invented quotation. AV2 is provisional: its post-comparison review is running and its gate is pending.

## 1. What sub-round 1 established, in lens terms

**Newton (analysis before synthesis).** AV1 computed the exact first-order face coefficient before charging any error budget (loop3-signoff rule 1), decomposed the density bound into the product-ordering split, straddling and two-creation terms, and synthesized two independently proved tier-(ii) inequalities; my S2 rebuilds the 49-face/15-owner-set enumeration from the I1 table alone and reproduces the forward `D_ii` bit-for-bit. AV2 did the same for C(1): the C^2 window's constants (`M_0=2, M_1=4s/pi, M_2=2s^2`) were derived, not assumed; my S3 independently reproduces `E~1.832e-7` at tier (ii) and rejects both tier-(i) values and both retained Poisson controls at the right magnitude.

**Tesla (source/load/clock/kernel).** Source = the 21 omitted face classes per star; load = cover `R={0,e_z}` (AV1) and its incident-star closure (AV2); clock = `s=alpha*t_E/hbar`; kernel = the tail-free C^2 window, fully budgeted (no leakage channel omitted, `M_0`/`M_1` exact). The `+tau/-tau` replay is used correctly as a control, not a magnitude estimate.

**Not established:** any first-order coefficient, sign or value of `omega(W)` (explicitly excluded, AW1's job); the parity theorem or flip lemma; any interaction-induced shift (AV2 carries `reference_unresolved`, 0 inside its enclosure); uniqueness or a rate in N; and AV2 itself is not yet admitted — three independent routes agree pre-comparison, which is not a gate.

## 2. Goals for sub-rounds 2-5

- **AW1/AW2 (shift): keep.** Already validated at the moment level: S1 proves every fact AW1 item 1 needs, by a route genuinely different from the sketched energy-24 multiplet split (one free link makes `W` itself Haar-distributed) — offer as a cross-check, not a replacement, since it doesn't cover "no omitted face returns the multiplet to itself."
- **AX1/AX2 (uniform): keep, unchanged order.** Depends on AW1's coefficient and the pre-frozen AW2 rule; nothing in sub-round 1 bears on route B or the `tau=96/g^4` dictionary.
- **AY1/AY2 (state): keep.** No new evidence changes the loop-3 disagreement; my non-blocking preference to schedule AZ2 right after AW1 stands but is not urgent now AZ2 is labelled a different finite model.
- **AZ1/AZ2 (continuum): keep**, plus one addition: check AZ2's finite-graph second-order coefficients against the 49/15/82-face enumeration S2 rebuilt — an external sanity target, not a premise import.

## 3. Improvements to the AW1 draft contract

- **Item 1**: name the "one free link => Haar-distributed" route as a required independent cross-check alongside multiplet-splitting, not a substitute.
- **Item 2 (flip lemma)**: require full enumeration over all 49 omitted faces per factor in each of the three orientations (147 checks), not a sample; S1's `face_links`/owner-set module is a template to reimplement independently.
- **Item 4 (K_2)**: pin the remainder/straddling terms to S2's concrete enumeration — 15 owner sets, multiplicities `[1,1,1,1,1,2,2,2,3,3,4,4,4,10,10]` (sum 49), and the 82 faces meeting `R` (16 touching both `0` and `e_z`) — as a shared target count. Add `||W Omega_R||=1/2` as a positive numeric control (S1 confirms `sqrt(1/4)=1/2` independently), not only a stated constant.
- **New control**: require separating `f=W` (the `E[W^3]` case, 4 shared links) from the 20 distinct omitted faces before "at most one shared link" — S1's first draft failed exactly this; a conflating mutation should be rejected explicitly.
- **`flip_breaks_at_nonzero_kappa`**: require a positive demonstration on one explicit nonzero kappa, not only rejection of the false claim.

## 4. Web check

WebSearch (2026-09-23), two queries on link-sign-flip / center-symmetry parity arguments for Wilson-loop expectations in Hamiltonian lattice gauge theory: no matching 2026 preprint found. Nearest hits — JHEP03(2026)181 (perimeter-law Wilson loops) and arXiv:2512.14833 (sign-problem sectors, U(1) quantum link model) — are adjacent topics, abstracts only, not read, not used as premises.

## 5. Assistant tests wanted after sub-round 2

- Full enumeration (3 orientations x 49 faces) of odd `|face_links(f) & E|`, extending S1, independent of AW1/AW2 `check.py`.
- Independent K_2^+ reassembly at both tiers from the 15-owner-set/82-face structure (extending S2), diffed bit-for-bit against AW1's admitted value.
- Independent recomputation of `tau_AW2` from the frozen decade-grid rule given AW1's reported K_2^+, checked against AW2's used value.
- Replay of the sign-exclusion margin (>=2) at both signs from AW2's exported enclosure, exact rationals only.
- A wrong-face control replay confirming the first-order coefficient uses `f=W` only, never a substituted omitted face.
