# Node and sign certificates restated for the limit of the named constructions; a finite-box sign corollary for the padded family; updated obligations — BC1 forward (single producer)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production: this report, `check.py` and the exact computations were written by a Claude model agent acting as the BC1 forward producer under the frozen BC1 contract (`research/round33/contracts/bc1.json`, sha256 `3fb84ed3135c48670d26643f120ef2ef74f5888174cf11e7395919e408a279bd`). `check.py` verifies that digest before it parses any field. BC1 is a `statement+skeptic` loop: this is its only producer, and admission also needs the skeptic's replay of the restatement and the corollary from the contract and the gates alone. This is correlated model-agent work, not independent human review and not formal verification. HNM labels are project aliases.

**What this producer read.**
- **The contract snapshot first**, then only files under `inputs/` (40 files: `AGENTS.md`, the contract and its 38 `shared_premises`):
  - *read in full:* `AGENTS.md`; `selection-bc1.md`; the AV2, AW1, AW2, AV1, AY1 and AY2 gates (every field; the `bindings` were hashed and compared by script); the BA1, BA2, BB1 and BB2 gates (every field except `bindings`, which were hashed and compared by script); the AQ1 and AQ2 gates; the AQ1 forward report; the AW2 forward report; `skeptic/av2.md`; `skeptic/bb2.md`; the Round32 lessons reference `round32-state-lemma-and-window.md`; the paired-physics SKILL and its complete-residual reference; the Newton, Tesla and historical-panel SKILL files; the AY2 forward report (its repository copy, byte-identical to the snapshot, also served as a convention reference);
  - *read in part:* the AV2 forward report (header, verdict, sections 1, 2, 4–8, 11–12); the AV2 reverse report (headings, sections 1, 4, 6, 12); `skeptic/aw2.md` (first 120 lines); the AW1 forward and reverse reports (headings and the lines on the finite-box `C_N(s)`); the BB2 forward report (header through section 10); the BB2 reverse report (headings, sections 4–6 and 8); the BA1, BA2, BB1 and BB2 contracts (their control lists and `new_control_semantics`, printed by script); `skeptic/ba2.md` (the lines on items 3–6, the limitations, the advice and keyword lines); `skeptic/bb1.md` (keyword lines);
  - *not opened:* the AQ2 forward report (its gate carries what is used).
- **Outside `inputs/`, for protocol and code conventions only:** `research/round33/tools/README.md`, `research/round33/tools/freeze.py`, `research/round33/tools/phrase_scan.py` (its round phrase list and clause rule are copied into `check.py` as infrastructure) and `research/round32/forward/ay2/check.py` (read in part: helpers, contract parsing, report scanning, controls and packet assembly) with `research/round32/forward/ay2/report.md` (a Round32 statement loop; conventions only). None of these carries premise weight.
- **Not read:** anything under `research/round33/forward/bc2/`; `research/round33/skeptic/`, `research/round33/advisor/` and `research/round33/experts/` other than the snapshots in `inputs/`; no reverse directory; no other agent's scratch folder.
- **Scratchpad disclosure.** My private scratch folder is `/tmp/claude-0/bc1-forward-private/`: three Fraction/float preview scripts of the gate arithmetic (`prelim.py`, `values.py`, `replay.py`), the source-edit audit script `audit.py` with its mirrored copies under `audit/` (section 11), development runs of `check.py` and the production run `run1`. **None of it is evidence.** I created the folder with `mkdir -p`, did not list `/tmp/claude-0/`, and opened no file in any other agent's folder. The Claude harness cached several of my own long reads (gate prints, the AY2 checker, the BB2 skeptic review, the inherited control semantics) in its tool-results store; those are my own reads.
- **File writing.** The agent file-writing tool refused this report file, which `check.py` parses and `freeze.py` binds, so it was written with a shell heredoc; its content is as written by this producer.

**Shared premises and attribution.** Every constant restated here is admitted: the AV2 window lemma, datum and radius; the AW1 bound `K_2^+` and the AW2 enclosure; the BB2 whole-sequence bound, identification and correlation limits; the BA2 limit dynamics; the AQ1 construction and the AQ2 gap. BC1 contributes:
- the restatement for one state, with every constant read by hash and checked equal to its gate rational;
- the finite-box sign corollary for the padded family, a triangle-inequality argument with an exactly computed `N_sign`;
- the common GNS item with its scope;
- the updated obligations table and the controls.

The mathematics used is standard: trace duality, the triangle inequality, continuity of the trace norm, and the GNS construction, which determines the representation of a state up to unitary equivalence. The limit dynamics is Nachtergaele–Sims (arXiv:1410.8174v1, Theorem 4.1), as quoted in BA2 and BB2; the compactness/GNS/Fourier strategy of AQ1–AQ2 is credited there to Gauvin arXiv:2503.15539v3 Supplement A.10. Scientific priority is unverified.

## Verdict (forward, single producer)

1. **Item 1 — the AV2 node certificate for the limit of the named constructions.** At `s=1` and `tau=+10^-8`, the centered Euclidean Wilson correlation of `omega_inf` satisfies `|C(1)-d| <= R` with the AV2 datum `d=497870683678639429793424156500617766317/(4*10^40)` and radius bound `R=1831967503411879425147166810021607/10^40` unchanged, so `C(1)` lies in the unchanged AV2 interval. The `tau=-10^-8` value is a replay of the same `|tau|` formula. The free reference `e^{-3}/4` stays inside (`reference_unresolved`).
2. **Item 2 — the AW2 enclosure for the limit of the named constructions.** `omega_inf(W)` lies in `[tau/144-K_2^+ tau^2, tau/144+K_2^+ tau^2]` with the AW2 endpoints unchanged at `tau=+10^-8`, and in their mirror at `tau=-10^-8` (a replay). The full second-order remainder `K_2^+ tau^2` is kept.
3. **Item 3 — the finite-box sign corollary.** For every `N` at least 2, the static Wilson mean of the untruncated F2 ground state on `Lambda_N` lies in the AW2 enclosure widened by `C' q^(N-1)` on both sides, `C'=4/984375` (the BB2 gate bound value), `q=1/64`. **`N_sign = 4`**, computed exactly. The sign of `omega^{F2,N}(W)` equals the sign of `tau` at both signs of `tau` for every `N` at least 4. The F1 boxes are already certified by AW2 at every `N` at least 2. The rate in `N` of the widening is `q^(N-1)`, for every `N` at least 2.
4. **Item 4 — finite-box node.** No finite-box node is restated, for F1 or for F2 boxes; the admitted record does not prove one. Two open rows (N2, N3) record the missing premises and candidate routes.
5. **Item 5 — the common GNS item.** The F1 and F2 limits are one state, with one GNS triple up to unitary equivalence, whose GNS dynamics is the AQ1 limit dynamics `T_theta`. Its correlation functions on `theta` in `[-8,8]` are the limits of the finite-box correlation functions of either family, with the rate `K5/N` only on the certified range `5<=N<=14000`. This is not equality of GNS dynamics of different states.
6. **Item 6 — the obligations table** (Section 8): AY2 rows O1–O6 are closed within named scopes by the BB2 and BA2 gates; twelve new rows are open, each with its missing premise and a candidate route.
7. **Item 7 — checker.** `check.py` runs **50 exact checks**. All **25 contract controls** reject explicit damaging mutations (**104** rejections inside the control checks, **113** in the whole checker). The `-B` and `-B -O` outputs are byte-identical.

**Proposed forward verdict: `accepted_within_scope`** (forward half of a statement+skeptic loop), with sub-labels `certificate_restated_for_limit`, `reference_unresolved` (the node) and `static_not_dynamic` (the sign). Admission still requires the skeptic's replay.

## 1. Model, state, clock and topologies

**Model** `AQ_patterned_zero_selected` (read from the contract):
- the AM2/AQ1 zero-selected patterned family: SU(2) Kogut–Susskind form on `Z^3` at fixed spacing, coarse 24-link factors, selected triple exactly `(0,0,0)` with the Haar product reference;
- 21 omitted faces per anchor entering as `-(tau/3)W_f` in normalized units `delta=alpha/8`;
- `tau=+10^-8`, with `tau=-10^-8` as a replay of the same `|tau|` formula at the mirrored coupling.

**Families.** On the centered coarse cubes `Lambda_N=[-N,N]^3`, `N` at least 2 (`N_min=2`, read from the contract): **F1** = AQ1 centered whole-star boxes; **F2** = I1 section 6 all-contained-face boxes with padding.

**States.**
- `omega_inf`, the limit of the named constructions: the common whole-sequence limit of F1 and F2 admitted in BB2 (Section 2).
- `omega^{F,N}`, the untruncated finite-box ground state of family `F` on `Lambda_N` at fixed `N`.

**Observable.** The original xz Wilson loop `W=(1/2)Tr[U U U^-1 U^-1]` with complete cover `R={0,e_z}` (48 links, 36 endpoints). `W` is real and at most 1 in absolute value pointwise, so its operator norm `||W||` is at most 1.

**Clock.** Euclidean `s=alpha t_E/hbar`, real time `theta=alpha t/hbar`, generator `G=H/alpha`. The only node is `s=1`. The BA2 window `theta` in `[-8,8]` is `u` in `[-1,1]` in the internal normalized time `u=theta/8` (conversion shown; `u` is used nowhere else). The free Wilson energy is 3 in `G` units, so `C_0(s)=e^{-3s}/4`; exponent 24 belongs to the normalized clock `u=s/8` only.

**Topologies.**
- States: the trace norm on `B(H_R)` (on `B(H_Y)` for a finite region `Y`); the inherited BB1/BB2 bounds use the coarse l-infinity metric with star diameter 1.
- Observables: the operator norm, with `||W||` at most 1.
- Dynamics: the norm on the compact window `theta` in `[-8,8]`.
- Representations: the GNS strong topology.

**Parameters** (contract fields, not prose): `metric`, `weights` (not applicable: no new decay estimate), `window` (the AV2 C^2 window at `s=1`, `M_0=2`, `M_1=4s/pi`), `clock`, `node` (`s=1` only), `N_min` (2).

## 2. The identification premise and what it licenses

**Admitted premises** (hash-pinned gates):
- **BB2 gate, item 1:** for `F` in `{F1,F2}`, both signs, every `N` at least 2 and every `M` greater than `N`, `||rho^{F,M}_R-rho^{F,N}_R||_1 <= C' q^(N-1)` with `C'=4/984375`, `q=1/64`, in each on-site cutoff space and at fixed `N` for the untruncated ground vectors; the limit exists on every finite region.
- **BB2 gate, items 2–3:** the F1 and F2 limits coincide on every finite region; "this limit coincides with every AQ1 subsequential limit and every F2 subsequential limit".
- **BA2 gate, item (4):** the F1 and F2 finite-box evolutions converge on `theta` in `[-8,8]` and "the F2 limit dynamics equals the AQ1 limit dynamics T_theta".

**Lemma (HNM-BC1-F01).** At each sign of `tau`, the set `S(tau)` of AQ1 subsequential limits is exactly `{omega_inf}`, and so is the set of F2 subsequential limits.

*Proof.* `S(tau)` is nonempty by the AQ1 gate. By BB2 item 3 every member equals `omega_inf` on every finite region; two states that agree on the local algebra agree on its norm closure. ∎

**Consequence.** Every statement that a Round32 gate admits *for every AQ1 subsequential state* holds for `omega_inf`, with the same constants. The GNS triple of `omega_inf` is the GNS triple of the (one) AQ1 subsequential state, up to the canonical unitary equivalence; its GNS evolution implements the same automorphism group `T_theta`; its generator `G` is nonnegative (AQ1 section 5, inherited by BB2 item 3). The window lemma of AV2 therefore applies to `omega_inf` word for word.

**Order.** The identification precedes every inheritance (`limit_identified_with_aq1_limits`). A restatement drawn from uniform local closeness (AV1/AY1: two limits within `2D` or `2K_2' tau^2`), from one BB1 comparison, or from a subsequence is rejected.

**What it does not license.** It changes no constant; it adds nothing about `C(s)` or `omega(W)` beyond the Round32 gates; it says nothing about states outside the named constructions or about other boundary conditions; it says nothing about finite boxes, except through the explicit BB2 item-1 bound of Section 5.

## 3. Item 1 — the AV2 node certificate restated for the limit of the named constructions

**Restated certificate (HNM-BC1-F02).** At the single preregistered node `s=1` and `tau=+10^-8`, let `(pi_inf, H_inf, Omega_inf)` be the GNS triple of `omega_inf`, `chi=(pi_inf(W)-omega_inf(W))Omega_inf` and `C(s)=(chi, e^{-sG} chi)`. Then `|C(1) - d| <= R`, hence `C(1)` lies in `[d-R, d+R]`, with the constants of the AV2 gate unchanged:

| symbol | exact rational (read from the AV2 gate) | truncated preview |
|---|---|---|
| datum `d` | `497870683678639429793424156500617766317/40000000000000000000000000000000000000000` | `1.24467670919e-2` |
| radius bound `R` | `1831967503411879425147166810021607/10000000000000000000000000000000000000000` | `1.83196750341e-7` |
| interval lower end `d-R` | `497863355808625782275723567833377679889/40000000000000000000000000000000000000000` | `1.24465838952e-2` |
| interval upper end `d+R` | `99575602309730615462224949033571570549/8000000000000000000000000000000000000000` | `1.24469502887e-2` |
| state bound `D` (AV1 gate, tier ii) | `585079838465912592144137406066050/42981220507576537932303142777593983768257` | `1.36124528702e-8` |
| window constants | `M_0=2`, `M_1=4s/pi` at `s=1` | — |

The gate writes `d` as `497870683678639429793424156500617766317/(4*10^40)`, `R` over `10^40` and the upper end as `99575602309730615462224949033571570549/(8*10^39)`; `check.py` parses these strings, requires `d-R` and `d+R` to equal the gate's interval ends exactly, and requires the gate's `accepted` and `decision` strings to carry the same `d` and `R`.

*Proof.* Lemma F01 makes `omega_inf` an AQ1 subsequential state; the AV2 gate admits the certificate for every such state, "each chosen state separately", with these constants. ∎ Nothing is re-derived.

**Consistency replays (exact, not sources).**
- *`R` is a valid directed bound of the gate's own formula.* With my own Machin enclosure of `pi` (width below `10^-60`), `2(D+D^2)+49|tau|/pi_lo+1/(4*10^40) <= R`, and `R` exceeds `2(D+D^2)+49|tau|/pi+1/(4*10^40)` by less than `10^-40`.
- *`R` is the common outward bound, not a producer radius.* The AV2 forward exact radius, rebuilt from the forward kernel term `1225000000000000000000000000000000/7853981633974483096156608458198757210489` quoted in the AV2 forward report, lies below `R` by less than `10^-40`. Restating it in place of `R` would be a smaller radius and is rejected.
- *`d` is the midpoint of an enclosure of `e^{-3}/4`.* My own series enclosure of `e^{-3}` (80 Taylor terms of `e^3` with a geometric tail) gives `|d-e^{-3}/4| <= 1.02e-43`, so `e^{-3}/4` lies inside `[d-R, d+R]`.

**Mirrored coupling.** At `tau=-10^-8` the same datum and radius hold for `omega_inf` at that coupling (BB2 at the minus sign identifies it with the AQ1 subsequential state there). Every term of `R` depends on `|tau|` only, so this is a replay of the same `|tau|` formula, **never a second confirmation**.

**Reference unresolved.** The free value `e^{-3}/4` lies inside the restated interval. The sub-label is `reference_unresolved`: no interaction shift, sign or coefficient of `C(s)` is claimed, and `correlation_shift_resolved` is exported false.

**Only `s=1`.** The analytic crossover `s*` near `6.2368634460` (AV2 gate) is a property of the radius formula, not a node certificate; no grid and no other node is restated.

## 4. Item 2 — the AW2 enclosure restated for the limit of the named constructions

**Restated enclosure (HNM-BC1-F03).** With `K_2^+` and the endpoints read from the AW2 gate (and `K_2^+` equal to the AW1 gate bound value):

| quantity | exact rational | preview |
|---|---|---|
| `K_2^+` | `81108864767825329926713064490531229475390625/24176936535511801466930759024724079017984` | `3.35480322946e3` |
| `K_2^+ tau^2` at the cap | `207638693805632844612385445095759947457/618929575309102117553427431032936422860390400000000` | `3.35480322946e-13` |
| lower end `L = tau/144 - K_2^+ tau^2` | `42773581813770903096597852821080380528959/618929575309102117553427431032936422860390400000000` | gate outward `6.91089641214e-11` |
| upper end `U = tau/144 + K_2^+ tau^2` | `43188859201382168785822623711271900423873/618929575309102117553427431032936422860390400000000` | gate outward `6.97799247674e-11` |

- At `tau=+10^-8`: `omega_inf(W)` lies in `[L, U]`.
- At `tau=-10^-8`: `omega_inf(W)` lies in the mirror `[-U, -L]`. This follows from the AW1 remainder bound at both signs and the AW1 flip lemma at the zero triple; it is **a replay, not a second confirmation**.

*Proof.* The AW2 gate admits the enclosure "for every state in the whole set of AQ1 subsequential limits"; by Lemma F01 that set is `{omega_inf}` at each sign. ∎

`check.py` recomputes `tau/144 -+ K_2^+ tau^2` from the parsed `K_2^+` and requires equality with the gate endpoints, their mirror, and `(L+U)/2 = tau/144`. The full second-order remainder is kept at both endpoints (`second_order_remainder_kept`).

**Restated labelled margins** (AW2 gate): exclusion margin `(|tau|/144-K_2^+ tau^2)/(K_2^+ tau^2) = 42773581813770903096597852821080380528959/207638693805632844612385445095759947457` (about 206.00005) and sign margin `1/(144 K_2^+ |tau|)` (about 207.00005). Hence `sign(omega_inf(W)) = sign(tau)` at both signs, and the Haar reference 0 is strictly excluded.

**Scope.** A static equal-time mean (sub-label `static_not_dynamic`). The AW2 gate's `resolved_interaction_shift` refers to `omega(W)` only; nothing is said about `C(s)` (Section 3).

## 5. Item 3 — the finite-box sign corollary for the padded family

**Theorem (HNM-BC1-F04).** At `tau=+10^-8` and for every `N` at least 2, the untruncated F2 ground state on `Lambda_N` satisfies `omega^{F2,N}(W)` in `[L - C' q^(N-1), U + C' q^(N-1)]`, and at `tau=-10^-8` it lies in the mirror `[-U - C' q^(N-1), -L + C' q^(N-1)]`, with `C'=4/984375` (the `nested_telescoping` bound value of the BB2 gate decision, evaluated at the hypothesis values) and `q=1/64`. For every `N` at least `N_sign = 4` the lower end at `+tau` is positive and the upper end at `-tau` is negative, so `sign(omega^{F2,N}(W)) = sign(tau)` at both signs.

*Proof.*
1. **Whole-sequence bound (BB2 item 1, `F=F2`).** For every `M` greater than `N`: `||rho^{F2,M}_R - rho^{F2,N}_R||_1 <= C' q^(N-1)`, for the untruncated ground vectors at fixed `N` and `M`.
2. **Passage `M` to infinity.** By BB2 items 1–2 the whole sequence `rho^{F2,M}_R` converges in trace norm to `rho^inf_R`, the `R`-density of `omega_inf`. The trace norm is continuous, so `||rho^inf_R - rho^{F2,N}_R||_1 <= C' q^(N-1)` for every `N` at least 2.
3. **Duality.** `W` lies in `B(H_R)` with `||W||` at most 1, so `|omega^{F2,N}(W) - omega_inf(W)| = |Tr((rho^{F2,N}_R - rho^inf_R) W)| <= ||W|| ||rho^{F2,N}_R - rho^inf_R||_1 <= C' q^(N-1)`.
4. **Enclosure.** Section 4 places `omega_inf(W)` in `[L, U]` (mirror at `-tau`); adding step 3 on both sides gives the widened interval.
5. **`N_sign`.** `C' q^(N-1)` is strictly decreasing in `N`. `N_sign` is the least `N` at least 2 with `C' q^(N-1)` strictly below `L`, computed exactly below; for every larger `N` the inequality persists. ∎

**`N_sign`, exactly** (at `tau=10^-8`; `L` is about `6.91089641214e-11`):

| `N` | `C' q^(N-1)` (exact) | preview | widened lower end at `+tau` (preview) | sign certified |
|---|---|---|---|---|
| 2 | `1/15750000` | `6.34920634920e-8` | `-6.34229545279e-8` | no |
| 3 | `1/1008000000` | `9.92063492063e-10` | `-9.22954527941e-10` | no |
| 4 | `1/64512000000` | `1.55009920634e-11` | `5.36079720580e-11` | **yes** |
| 5 | `1/4128768000000` | `2.42203000992e-13` | `6.88667611205e-11` | yes |
| 6 | `1/264241152000000` | `3.78442189050e-15` | `6.91051796996e-11` | yes |

So **`N_sign = 4`**. The widened enclosure at `N_sign`:
- at `+tau`: `[232256915653307984268043972456662444208313/4332507027163714822873992017230554960022732800000000, 369480171452763518908899363269803522461511/4332507027163714822873992017230554960022732800000000]`, contained in `[5.36079720580e-11, 8.52809168309e-11]` (directed decimals);
- at `-tau`: the mirror, a replay.

The ratio `L/(C' q^3)` is about 4.4584, and the widened exclusion margin (lower end over half-width `K_2^+ tau^2 + C' q^3`) is about 3.3851 (labelled information).

**Rate in `N`, for every `N` at least 2.** The widening `C' q^(N-1)` is the BB2 density rate, `q=1/64` per coarse step at fixed spacing, for every `N` at least 2.

**F1 boxes (recorded as agreement, not re-derived).** The AW2 gate states the enclosure "in every centered whole-star box N>=2 at every on-site cutoff". The AV1 gate removes the on-site cutoff "for the ground vector itself in each fixed box", so the untruncated F1 value lies in the same closed interval: the sign of `omega^{F1,N}(W)` is certified by AW2 at every `N` at least 2.

**Not claimed.**
- F2 boxes with `N=2` or `N=3`: the widened interval contains 0 there. This is an open obligation (row N4), not a failure.
- Cutoff-`L` F2 states: BB2 identifies only the untruncated limit, so they are not claimed.
- Anything below the cap. For information only, at `tau/100` the half-width `K_2^+ (tau/100)^2 + C' q^3` is about `1.5501e-11`, larger than the first-order value `6.944e-13`. `C'` at the hypothesis values does not depend on `tau`, and AW2 admits the enclosure at the cap only, so no bracket applies and nothing is claimed below the cap.

**Labels.** The widened enclosure and `N_sign` form the one new constant family of BC1: tier `exact_first_order`; inputs, in place of a route, the AW2 gate endpoints (`static_not_dynamic`, `K_2^+` at the AW1 exact tier) and `C'` (BB2 assembly `nested_telescoping`, hypothesis source `bb1_frozen_targets`, BB1 route `polymer_kp`). Restated constants keep their Round32 labels unchanged.

**Traps, each an exact fixture in `check.py`.**
- *A comparison bound is not a distance to the limit.* The BB1 per-comparison constant (about `8.9051e-7`) bounds one comparison (for example `N` against `N+1`); without the whole-sequence passage it bounds nothing about `omega_inf`. A harmonic fixture `a_N = sum_{k=2}^N 1/k` has steps `1/N` tending to 0 yet first exceeds 4 at `N=83` (exact), and an alternating fixture `diag(1/2 +- 1/100, 1/2 -+ 1/100)` stays in a fixed ball with two subsequential limits.
- *Labelled constants are not the bound value.* The union value `1/250000` and the re-evaluated value (about `9.0465e-7`) are labelled in the BB2 gate; the rule reads `C'` as the nested_telescoping bound value, so both are rejected even though they would give the same `N_sign`.
- *Off by one.* At `N=3` the widened lower end is `-9.22954527941e-10`, so `N_sign=3` is rejected.
- *One-sided widening or a dropped remainder* changes an endpoint and is rejected.
- *The norm of `W`.* In a `2x2` fixture `Delta=diag(1/2,-1/2)`, `X=diag(1,-1)` gives `|Tr(Delta X)| = ||Delta||_1`, so duality is attained; with `2X` the difference doubles, so the factor `||W||` at most 1 is needed.

## 6. Item 4 — finite-box node: what the admitted record does and does not prove

The contract determines this item from the admitted record before freeze; `check.py` verifies each cited fact in the snapshots.
- The AV2 gate quantifies over "every AQ1 subsequential state of the centered whole-star construction (each chosen state separately".
- The window lemma and the real-time comparison are stated for the GNS vector of that state with AQ1 section 5 nonnegativity: AV2 forward `HNM-AV2-F01`, `F02`, `F07`, `F15`; AV2 reverse `HNM-AV2-R01`, `R02`, `R08`, `R13`.
- The only box-by-box step is the seven-star slope `k=49|tau|/4` (AV2 forward `F13`–`F14`, AV2 reverse `R12`), which the record passes to the AQ evolution.
- The AV2 reverse executes "finite-box provenance" as a damaging mutation of `changed_model_relabelled` (AV2 reverse section 12).
- The AW1 gate item (1) gives the finite-box `C_N(s)` only "with the tau^2 constant explicitly unbounded (not uniform in N".

**Conclusion.** The admitted record does not prove a finite-box node, and BC1 restates none, for F1 or for F2 boxes. `finite_box_node_claimed` is exported false. A finite-box node presented as a restatement, one obtained by applying the window lemma box by box, or one obtained by re-deriving or retuning an AV2 constant is rejected. The two open rows are N2 (finite F1 boxes) and N3 (F2 boxes) in Section 8, each with its missing premise and a candidate route. No constant is re-derived or retuned.

## 7. Item 5 — the common GNS item

**Statement (HNM-BC1-F05).** At each sign of `tau`:
1. The F1 limit and the F2 limit are one state, `omega_inf` (BB2 items 2–3). It has one GNS triple `(pi_inf, H_inf, Omega_inf)`, determined up to unitary equivalence by the GNS construction; the triple of every AQ1 subsequential state and of every F2 subsequential state is this one, up to the canonical unitary.
2. Its GNS dynamics is the AQ1 limit dynamics `T_theta` implemented in that representation: `U_theta pi_inf(A)Omega_inf = pi_inf(T_theta(A))Omega_inf`, strongly continuous, with a nonnegative self-adjoint generator. `T_theta` is the limit of the F1 evolutions (AQ1) and of the F2 evolutions (BA2 item (4)); stationarity and the generator come from AQ1 sections 4–5 and from BA2's rerun for F2 limits, inherited by BB2 item 3.
3. For `A` in `B(H_R)` and `theta` in `[-8,8]`, the correlation functions `c^inf_A(theta) = omega_inf(A* T_theta(A)) - |omega_inf(A)|^2` are the limits along the whole sequence of the finite-box correlation functions of either family (BB2 item 5). The BB2 inequality holds for every `N` at least 5; it gives the rate `K5/N` (`K5` about `6.10e-9`) only on the certified range `5<=N<=14000`, and it is vacuous from `N=14419` on, where only convergence without a rate is admitted.

**Scope.** This is one state with one representation and one dynamics, because BB2 admits that the two limits are one state and BA2 that the F2 limit dynamics is `T_theta`. It is **not** equality of GNS dynamics of different states: `gns_dynamics_equality_claimed` is exported false. The gate field `dynamics_limit_identified_claimed` restates BA2 item (4) and adds no dynamics claim. Nothing is uniform in time.

**Fixture (`same_state_not_different_states`).** On `M_2` with the Heisenberg dynamics of `H=diag(0,1)` at the rational phase `v=(3+4i)/5`, both basis vector states are invariant, yet the correlation of `A=sigma_x` is `v` in one and `conj(v)` in the other: one algebraic dynamics, two states, two GNS dynamics.

## 8. Item 6 — the updated obligations table

### 8.1 Table

Status is `closed_within_scope` (with the closing gate and its scope) or `open`. The O-row names are read from the AY2 gate item (5); the N-row names are read from the contract's `parameters.obligations`, with the item-4 entry split into two rows as item 4 requires.

| id | obligation | status | closing gate and scope | missing premise | candidate route |
|---|---|---|---|---|---|
| O1 | uniqueness of the limit | closed_within_scope | BB2 gate items 2-3: every AQ1 subsequential limit and every F2 subsequential limit equals omega_inf on every finite region; scope: the named constructions F1 and F2 only | Within the scope none. Beyond it (states outside the named constructions, other boundary conditions, uniqueness of every infinite-volume ground state) see row N1. | Executed in BB2: the whole-sequence Cauchy bound of item 1 plus the fixed-N comparison c3 of BB1; beyond the scope see row N1. |
| O2 | whole-sequence convergence | closed_within_scope | BB2 gate item 1: the reduced densities of F1 and F2 converge as whole sequences on every finite region (sup over all M greater than N, C'=4/984375, q=1/64); BA2 gate items (3)-(4): the finite-box Heisenberg evolutions on theta in [-8,8]; BA1 gate: the AM2 creation coefficients in each on-site cutoff space; scope: the named constructions | Within the scope none. Cutoff-L state limits are not used; non-centred F2 volumes see row N8. | Executed: BB1 nested comparisons telescoped with the full geometric tail (BB2), Lieb-Robinson Cauchy estimates for all M greater than N (BA2). |
| O3 | translation invariance under coarse translations | closed_within_scope | BB2 gate item 4: the limit of the named constructions is invariant under every coarse translation on every finite region, from the direct BB1 comparison c5 with constant C_h=1/250000 and exponent N minus the l-infinity norm of v minus 1; non-coarse translations are rejected; scope: coarse translations and the limit of the named constructions | Within the scope none. Non-centred F2 volumes in c5 rest on the AY1 local reading (row N8); states outside the named constructions see row N1. | Executed in BB2 through the general-volume comparison c5; non-coarse fine translations are not symmetries of the model. |
| O4 | a rate in N | closed_within_scope | BB2 gate item 1: the density rate q^(N-1) with C'=4/984375 for every N at least 2; BA2 gate: the dynamics comparison K_cmp(5N+1)N^-3 and the Cauchy rate K_F/(N-1) for every N at least 2 on theta in [-8,8]; BB2 gate item 5: the correlation rate K5/N only on 5<=N<=14000; scope: the named constructions at fixed spacing | Within the scope none. The correlation rate beyond N=14000 see row N5; nothing in the lattice spacing a (row N10). | Executed in BA1, BA2, BB1 and BB2; every rate is per coarse step in N at fixed spacing. |
| O5 | boundary independence of dynamics on compact time windows | closed_within_scope | BA2 gate items (1)-(4): the F1 and F2 finite-box Heisenberg evolutions of A in B(H_R) differ by at most K_cmp(5N+1)N^-3 in norm for theta in [-8,8] and every N at least 2, and the F2 limit dynamics equals the AQ1 limit dynamics T_theta; BB2 gate item 5: the correlation functions of the one limit state; scope: algebraic dynamics of the named constructions on the compact window | Within the scope none. Other boundary conditions (row N1), uniform in time (row N7), GNS dynamics of different states (row N6). | Executed in BA2: Duhamel with the Nachtergaele-Sims Lieb-Robinson bound and the AQ1 constants F(r)=(1+r)^-4, C at most 224. |
| O6 | dynamics of the padded family itself | closed_within_scope | BA2 gate items (4)-(5), decision "AY2 row O6 closed within scope": the F2 evolutions converge as a whole sequence to T_theta on theta in [-8,8] and AQ1 sections 4-5 are rerun for every F2 subsequential limit state; BB2 gate item 3 identifies those states with omega_inf; scope: the named constructions | Within the scope none. | Executed in BA2 (Nachtergaele-Sims Theorem 4.1 for the owner-set interaction and the AQ1 rerun). |
| N1 | states outside the named constructions and other boundary conditions | open | none (open) | A comparison of an arbitrary infinite-volume ground state, or of another boundary prescription (literal vertex boxes, periodic or orthant boxes), with omega_inf on R. Every admitted comparison is between F1 and F2 boxes or one-prescription volumes containing Lambda_N (BB1 c1-c5). | HTW-type local stability or a Dobrushin-type condition with evaluated constants at the cap (the AY2 O1 route; the Yarotsky constants of I1 are not evaluated), or a BB1-type comparison for a pre-frozen AM2-admissible class of boundary prescriptions; not executed. |
| N2 | the finite-box Euclidean node for finite F1 boxes (item 4) | open | none (open) | The window lemma for the untruncated finite-box ground vector with the generator G_N-E_N at the unchanged M_0=2 and M_1=4s/pi, with the AV1 per-box state bound D and the AV2 per-box seven-star slope. The admitted AV2 record states the window lemma and the comparison only for the GNS vector of an AQ1 subsequential state with AQ1 section 5 nonnegativity, and the AV2 reverse rejects a finite-box provenance as a changed model. | A new contract stating the window lemma for the finite-box vector state (the spectral measure of chi_N for G_N-E_N lies on the nonnegative half-line because E_N is the least eigenvalue, AM2), reusing F13-F14 box by box and the AV1 per-box D (the AV1 gate covers every centered whole-star box, untruncated), reviewed as a new statement; not executed, and no constant is re-derived here. |
| N3 | the finite-box Euclidean node for F2 boxes (item 4) | open | none (open) | Everything in N2, and in addition the F2 incidence of the groups meeting R and the F2 slope (the norm of the F2 interaction terms meeting R in G=H/alpha units), which are not in the AV2 record. The AY1 gate records that both families retain the same 82 faces meeting R for N at least 2, but no F2 relative-unitary slope is admitted. | The N2 route with the F2 grouping: enumerate the F2 groups meeting R from the I1 table as in the AY1 itemization, bound their norm to obtain the F2 slope, then apply the finite-box window lemma; not executed, and no constant is evaluated here. |
| N4 | the F2 finite-box sign for 2 <= N < N_sign | open | none (open) | N_sign=4, so N=2 and N=3 are open: there C' q^(N-1) is 1/15750000 and 1/1008000000, both above tau/144-K_2^+ tau^2, and the widened interval contains 0. A box-level bound on the Wilson mean of the untruncated F2 ground vector is missing. | Gate a box-level form of the AY1 remainder bound (AY1 forward F13-F14 as quoted in the AY2 forward report section 4.2: the R-local remainder is at most K_2' tau^2 in every box of either family at every cutoff) for the untruncated F2 vector through AV1 F22 via AY1; by duality it would place omega^{F2,N}(W) within K_2' tau^2 of tau/144 with sign margin 1/(144 K_2' tau) about 51.76 (labelled preview, not claimed); or an F2 itemization of the AW1 bound K_2^+. |
| N5 | the correlation-function rate in N beyond N=14000 with the frozen r_N | open | none (open) | With r_N=floor((N-1)/2) and the frozen region form, the BB2 item-5 bracket gives the rate K5/N only on 5<=N<=14000 and is vacuous from N=14419 on, because the factor e^(volume/10^8) of Lambda_{r_N} eventually outgrows q^(N-r_N); beyond N=14000 only convergence without a rate is admitted. | A region form with a polynomial volume factor (the BB1 iterated_split route proves c_site times a sum over y in Y of q^(N-y_inf), as the BB2 skeptic advises) admitted at a gate, then the BB2 item-5 argument unchanged; or a re-frozen r_N in a new contract; not executed. |
| N6 | GNS dynamics of different states | open | none (open) | Nothing compares the GNS dynamics of omega_inf with that of any other state; for a state outside the named constructions neither stationarity under T_theta nor a relation between its GNS representation and that of omega_inf is admitted. | Identify the other state with omega_inf (row N1), in which case it is the same state; or prove its stationarity under T_theta and its quasi-equivalence with omega_inf; not formulated. |
| N7 | uniform in time | open | none (open) | Every admitted dynamics constant holds on theta in [-8,8] (U=1 in u=theta/8) and grows like U^2/(1-vU/3) (BA2); no estimate holds for all theta. | A bound on the finite-box and limit correlation functions that holds for all theta, for example from spectral information (the AM2 finite-box gap 1/2 and the AQ2 gap alpha/16 on the invariant-local cyclic completion) with a real-time transfer; not formulated. |
| N8 | non-centred F2 volumes in the fifth BB1 comparison, which rest on the AY1 itemization as a reviewed local reading | open | none (open) | A gated statement of the AY1 itemization (on-site operator, per-anchor grouping inside the star, supports of at most 4 sites, per-site sum through b in u-S, cutoff compression) for every F2 volume containing Lambda_N, not only for the centred cubes; carried by BB2 item 4. | A statement loop reviewing the AY1 items H1-H5 for general F2 volumes item by item and recording them in a gate; not executed. |
| N9 | the route-B uniform model (BC2, produced in parallel; its row cites the BC2 gate only once recorded) | open | none (open) | No BC2 gate is recorded at the time of this production; BC1 restates nothing for the uniform model (route B, AX1/AX2). | BC2, in production in parallel; this row cites the BC2 gate only once it is recorded. |
| N10 | anything uniform in the lattice spacing a | open | none (open) | Every constant is at fixed spacing and strong bare coupling (a coarse step is (4a,2a,a)); by the AL1 dictionary of a different model, as quoted in AY1 and AY2, the cap corresponds to g^4 at least 9.6x10^9; no estimate in a. | None within this family at fixed coupling: a statement in a needs a coupling that moves with a and a scaling analysis; not formulated. |
| N11 | the continuum problem | open | none (open) | The four-dimensional Yang-Mills existence and mass-gap problem remains open; nothing here constructs a continuum theory. | None executed or claimed here. |
| N12 | an interaction shift, sign or coefficient of the Euclidean correlation C(s) (carried from Round32, not a Round33 gate row) | open | none (open) | The AV2 interval contains the free value e^{-3}/4 (reference_unresolved); by AW1 the first-order term of C(s) vanishes and its tau^2 constant is not uniform in N, so no second-order enclosure of C(1) for omega_inf exists. | A second-order refinement with the C^2 window's finite M_2=2s^2 (AV2 skeptic advice 7) and a tau^2 constant for C(s) uniform in N (AW1: the 40-star relative-unitary step), certified only if it excludes e^{-3}/4; not executed. |

**Notes.**
- Rows O1–O6 close only within the named scopes. Each closing cell names the gate whose admitted text `check.py` finds (for example "this limit coincides with every AQ1 subsequential limit and every F2 subsequential limit" for O1, and "AY2 row O6 closed within scope" for O6).
- Rows N1–N11 are the entries the contract lists; row N12 is an open Round32 item carried along for completeness.
- N9 cites no BC2 gate, because none is recorded; the row is to be updated when the BC2 gate exists.

### 8.2 The AY2 falsifying scenario

AY2 exhibited two admissible density matrices on `H_R` that differ by at least `(1-2x10^-6) 2K_2' tau^2` and asked whether two subsequential limits could differ on `R`. For the named constructions this is now **excluded**: every AQ1 subsequential limit and every F2 subsequential limit equals `omega_inf` (BB2 items 2–3). It is **not** excluded for states outside the named constructions or for other boundary conditions (row N1). The AY2 witness remains a valid pair of density matrices; it is simply not a pair of limits of F1 or F2.

### 8.3 Round32 limitations: lifted or remaining

Each anchor is a verbatim substring of the named gate's `limitations`; `check.py` verifies it.

| id | gate | limitation (anchor) | status | by |
|---|---|---|---|---|
| L1 | AV2 | Each AQ1 subsequential state separately; no uniqueness, whole-sequence convergence or rate in N | lifted_in_part | BB2 items 1-3: the AQ1 subsequential states are the one state omega_inf and the densities converge as a whole sequence at q^(N-1) for every N at least 2; uniqueness of every infinite-volume ground state stays excluded |
| L2 | AV2 | Upper certificate only: the free value e^{-3}/4 lies inside the interval (reference_unresolved) | remains | no Round33 gate; row N12 |
| L3 | AV2 | Sign-blind: the tau=-10^-8 value is a replay | remains | no Round33 gate; the minus sign is a replay here too |
| L4 | AV2 | The crossover s* is that of the analytic formula, not a node certificate | remains | no Round33 gate; only s=1 is restated |
| L5 | AW2 | the -tau pairing of individual states holds only along a common subsequence | lifted_in_part | BB2 at both signs: each sign has one limit, so the whole-set flip identity of AW1 pairs the two limits; this consequence is recorded and used for no value; the minus-sign enclosure stays a replay |
| L6 | AW2 | resolved_interaction_shift refers to omega(W) alone | remains | no Round33 gate; static_not_dynamic |
| L7 | AW1 | Parity theorem for C(s) and c(theta) is a finite-volume Taylor statement | remains | no Round33 gate; the tau^2 constant of C(s) stays unbounded (rows N2, N3, N12) |
| L8 | AV1 | Uniform local closeness of all AQ1 subsequential limits (pairwise within 2D on R), not uniqueness, whole-sequence convergence or a rate in N | lifted_in_part | BB2 items 1-3 within the named constructions; uniqueness of every infinite-volume ground state stays excluded |
| L9 | AY1 | two limits may differ by up to 2K_2' tau^2 on R and without bound elsewhere | lifted_in_part | BB2 items 2-3 for limits of F1 and F2; remains for states outside the named constructions (row N1) |
| L10 | AY2 | all six obligations unproved | updated | BA2, BB2: rows O1-O6 of Section 8.1 |
| L11 | AY2 | it shows what the bounds leave open and is not a constructed limit | lifted_in_part | BB2 items 2-3: the scenario is excluded for F1 and F2 limits (Section 8.2) |
| L12 | AY1 | nothing transfers to literal vertex boxes (I1 section 7), periodic or orthant boxes | remains | no Round33 gate; row N1 |
| L13 | AY2 | every constant is uniform in N at fixed spacing, never in a | remains | no Round33 gate; row N10 |

## 9. Item 7 — mandatory sentence, gate fields and checker

**Mandatory sentence (the contract template, verbatim, once):**

For the zero-selected patterned family at tau=10^-8, the limit of the named construction families F1 and F2 admitted in BB2 satisfies the Round32 node certificate at s=1 with the unchanged datum and radius and the Round32 enclosure of the static Wilson mean with the unchanged endpoints, and every padded box Lambda_N with N at least the exactly computed N_sign has a static Wilson mean of certified sign; these are restatements of admitted certificates for one limit of the named constructions and a finite-box corollary, not uniqueness of any ground state, not an interaction shift of the Euclidean correlation, and not a statement uniform in the lattice spacing a.

The values in it: datum `d` and radius bound `R` of Section 3; endpoints `L`, `U` of Section 4; `N_sign=4` (Section 5), for the untruncated F2 ground vectors at both signs of `tau` (the minus sign a replay).

**Gate fields** (exported exactly as `gate_fields_required`): `node_certificate_restated_for_limit`, `sign_certificate_restated_for_limit`, `finite_box_sign_claimed`, `dynamics_limit_identified_claimed` and `rate_in_N_claimed` true; `finite_box_sign_scope` as the contract writes it; `uniqueness_of_ground_state_claimed`, `gns_dynamics_equality_claimed`, `uniform_in_time_claimed`, `rate_in_a_claimed`, `continuum_claim`, `weak_coupling_claim`, `scientific_priority_verified`, `finite_box_node_claimed` and `correlation_shift_resolved` false. `rate_in_N_claimed` refers to the density rate `q^(N-1)` for every `N` at least 2 and to the correlation rate only on `5<=N<=14000`.

**Checker.** Standard library only; every admission Boolean in exact `Fraction` arithmetic; conditions raise `AdmissionError` through `require` (never `assert`), so every check stays active under `-O`. It records its own sha256 before any evaluation, verifies the contract sha256 before parsing, pins the sha256 of every admitted gate, reads the targets, the tau value, the node, `N_min`, `q`, the references and the obligations list from the contract, and reads every constant from the hash-verified gates.

## 10. Error ledger (preregistered terms)

| term | entry | note |
|---|---|---|
| `identification_premise_bb2` | `0` (exact identification) | an admitted premise, not a numerical term: BB2 items 2-3 make the set of AQ1 subsequential limits `{omega_inf}` |
| `restated_constants_exactness` | `0` | `d`, `R`, the interval, `K_2^+` and the four endpoints equal the gate rationals exactly |
| `finite_box_whole_sequence_term` | `C' q^(N-1)`, `C'=4/984375`, `q=1/64`; `1/64512000000` at `N_sign=4` | BB2 item 1 with `M` to infinity; added on both sides |
| `second_order_remainder_K2plus` | `K_2^+ tau^2 = 207638693805632844612385445095759947457/618929575309102117553427431032936422860390400000000` | kept at both endpoints (AW1, AW2) |
| `arithmetic` | `not_applicable` | stated reason: every value is an exact rational; the only transcendental quantities (`e^{-3}/4`, `pi`) enter through the AV2 gate datum and radius, whose arithmetic half-width `1/(4*10^40)` is already inside `R`; BC1 rounds nothing; decimals are labelled previews |

## 11. Controls (every one a damaging mutation in `check.py`; none deferred)

| control | damaging mutations rejected |
|---|---|
| `coherent_evidence_tampering` | with the packet hash rebound: a control Boolean flipped; `R` re-rounded; `N_sign` lowered to 3; `C'` replaced by the labelled union value; an obligation row removed; `finite_box_node_claimed` true; the BB2 gate hash replaced; the AV2 gate snapshot removed; the widened lower end raised; a minus-sign endpoint changed |
| `exact_arithmetic_admission` | float, bool, NaN and zero-denominator inputs; a decimal preview used as an admission value |
| `no_priority_or_continuum_claim` | continuum, priority, weak-coupling or rate-in-a flag set true |
| `changed_model_relabelled` | the route-B uniform model; a nonzero selected triple; `tau=10^-7`; literal vertex boxes as a family; a finite-box provenance for the node; a finite-graph result under the family label |
| `insufficient_verdict_retained` | a restated constant differing from its gate value relabelled accepted; an omitted corollary relabelled accepted; an overclaim relabelled limited; the open rows `N=2,3` counted as a failure; the sign claimed for `N=2,3` (the retained open rows retuned away) |
| `wrong_delta_alpha_hbar_clock` | exponent 24 with the `s` clock; the window `theta` in `[-1,1]` (a window in `u` labelled `theta`); first-order coefficients `tau/1152` and `tau/18` |
| `placeholder_span_rejected` | an angle-bracket placeholder span (the words preceding gate) in `selected_after`; a placeholder span appended to the report |
| `negation_aware_phrase_scan` | four appended affirmative sentences, each carrying one forbidden phrasing of the round list or the contract list (the phrasings are quoted only in `check.py`); the template occurring twice; a negated occurrence passes (fixture) |
| `parameters_declare_metric_weights_window` | `window`, `metric` or `clock` removed from `parameters`; `weights` emptied without a reason |
| `named_construction_not_uniqueness` | `uniqueness_of_ground_state_claimed` true; the limit called uniqueness of every infinite-volume ground state; an affirmative definite infinite-volume phrasing appended to the report (quoted only in `check.py`) |
| `common_clock` | the enclosure at `tau/10` beside the node at `tau`; a normalized clock for one statement; `C'` from the secondary pair at `q_2` |
| `topology_named` | weak-* for states; one topology for states and dynamics; a moving-vector norm claim (fixture difference 2 against 0 on the fixed vector) |
| `limit_identified_with_aq1_limits` | the restatement from uniform local closeness `2D`; from a subsequence; inheritance ordered before the identification |
| `certificate_values_unchanged` | `R` re-rounded up by `10^-40`; the smaller AV2 forward radius; `d` shifted by `10^-40`; the interval rounded to 12 digits; an AW2 endpoint shifted; `K_2^+` replaced by its outward ceiling |
| `post_hoc_node_rejected` | the node `s=2`; the crossover `s*` as a node; a grid on `[0,128]` |
| `finite_box_sign_from_whole_sequence` | the BB1 per-comparison constant; an `N` to `N+1` bound alone; a subsequence bound; the labelled union value; the labelled re-evaluated value; `q=1/32`; `N_sign=3`; `N_sign=5` |
| `mirror_sign_replay_not_confirmation` | the minus sign counted as a second confirmation; a sign-blind (unmirrored) minus-sign enclosure |
| `reference_unresolved_retained` | `correlation_shift_resolved` true; the node reported as deciding the reference; the free value claimed outside the interval |
| `obligations_table_complete` | row N3 removed; O1 without its closing gate; N1 marked closed; a candidate route emptied; N9 citing a BC2 gate; rows reordered |
| `rate_range_stated` | an appended unqualified `O(1/N)` sentence; an appended "the densities converge at a rate in N" without a range; the correlation range extended to 14418; the density rate restricted to `N` at least 5 |
| `round32_gates_untouched` | the restatement written into an AV2 gate copy (its hash then differs from the pinned and cross-bound value); a packet declaring a Round32 file edited |
| `route_b_not_restated` | the AV2 restatement applied to the route-B uniform limit; the AW2 restatement applied to it; a BC2 gate cited before it is recorded |
| `same_state_not_different_states` | `gns_dynamics_equality_claimed` true; the common GNS item stated without the BB2 identification; the item phrased as equality of GNS dynamics of different states |
| `second_order_remainder_kept` | `K_2^+ tau^2` dropped at an endpoint; `K_2^+/2`; the `C' q^(N-1)` widening applied on one side only |
| `finite_box_node_only_from_record` | a finite-box node presented as a restatement; one obtained by applying the window lemma box by box; one with the AV2 state term retuned to `D/2`; `finite_box_node_claimed` true |

**Source-edit audit (private scratch, not evidence).** I ran nineteen source edits, each on a mirrored copy of this directory in `/tmp/claude-0/bc1-forward-private/audit/`, plus one unmutated copy, which reproduces the development run byte for byte. Eighteen damaging edits abort:
- *report edits:* one `N_sign` claim site changed to 3; row N3 removed; a sentence stating the `O(1/N)` rate with no range appended; row O6 marked open; the exact `R` changed; the template altered; a preview changed in its last digit; the L13 anchor altered; an affirmative forbidden phrase appended;
- *checker edits:* the widening exponent `N` in place of `N-1`; the AV2 pin changed; `K_2^+` replaced by its outward ceiling; `C'` replaced by the union value; the least-`N` rule tightened to `L/100`; the rate scan disabled;
- *input edits:* the BB2 gate snapshot edited; the contract edited; an undeclared file added to `inputs/`.

One non-damaging edit runs silently: tightening the least-`N` rule to `L/4` returns the same `N_sign=4`. The checker certifies the answer (the least `N` whose widened lower end is positive, computed independently in the table), not the code path.

Disclosure: the first version of the report check let two damaging edits run silently (one of the two `N_sign = 4` claim sites changed to 3, and one occurrence of a repeated preview changed), because it required only that a correct string be present somewhere. It now rejects any stated `N_sign` other than the computed value (outside descriptions of rejected mutations) and any 12-digit preview that is not an exact truncation or a quoted gate decimal.

## 12. Exclusions and limitations

**Contract claim exclusions (verbatim):** uniqueness of every infinite-volume ground state; states outside the named constructions; an interaction shift, sign or coefficient of the Euclidean correlation C(s); the route-B uniform model (BC2); equality of GNS dynamics of different states; uniform-in-time statements; any estimate uniform in the lattice spacing a; continuum or weak coupling; scientific priority.

**Preregistration claim exclusions (verbatim):** uniqueness of every infinite-volume ground state; states outside the named constructions; an interaction shift of C(s); the route-B uniform model (BC2); equality of GNS dynamics of different states; uniform-in-time statements; any estimate uniform in the lattice spacing a; continuum or weak coupling; scientific priority.

**Additional exclusions:** no finite-box node for F1 or F2 boxes; no F2 finite-box sign for `N=2,3`; no cutoff-`L` F2 state; nothing below the cap; no node other than `s=1`; no correlation rate outside `5<=N<=14000`.

**Claim flags, all false:** `continuum_claim`, `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `scientific_priority_verified`, `weak_coupling_claim`, `gns_dynamics_equality_claimed`, `uniform_in_time_claimed`, `finite_box_node_claimed`, `correlation_shift_resolved`.

**Limitations.**
1. **Scope.** Only the zero-selected patterned family, the cover `R`, fixed spacing and `tau=+-10^-8`, the named families on centered cubes and their limit. Nothing transfers to nonzero selected triples, the uniform route-B model, literal vertex boxes, other boundary conditions, weak coupling or the continuum.
2. **Restatement, not new evidence.** Items 1–2 restate admitted certificates for one state; they are exactly as strong as AV2 and AW2. The node is an upper certificate with the free value inside; the enclosure is a static equal-time mean.
3. **Inherited without re-proof.** AV2's window lemma, constants and radius; AW1's `K_2^+` and flip lemma; AW2's enclosure; BB2's items 1–5 and its BB1 discharge (including the Kotecky–Preiss citation checked post hoc and the AY1 local reading for non-centred F2 volumes); BA2's limit dynamics; AQ1/AQ2; AV1 cutoff removal. The GNS construction, trace duality and the continuity of the norm are standard.
4. **The corollary is only as sharp as `C'`.** `C'` is evaluated at the BB1 hypothesis values (about 4.5 times the admitted BB1 constant); the labelled re-evaluated value would give the same `N_sign=4`, but only the bound value is used.
5. **Single producer, correlated model agents.** The skeptic's replay from the contract and the gates is the second admission input.
6. **Scientific priority** is unverified.

**Methodological lenses** (modern uses of the snapshotted skills; no historical figure endorses anything and no historical or occult material supplies a premise):
- **Newton, analysis before synthesis:** the finite-box statement is analysed back to exactly which admitted bound reaches a finite box (the BB2 item-1 whole-sequence bound, not a comparison or a subsequence) before the corollary is synthesized.
- **Tesla, complete accounting:** both the second-order remainder and the finite-box widening are charged on both sides, at both signs.

## 13. Contract wording notes (non-blocking; each a verified fact about the frozen text, checked in `contract_wording_defects_recorded`)

| id | field | note |
|---|---|---|
| W1 | `selection_reason` | says AW2 was stated "for each AQ1 subsequential state separately"; the AW2 gate states the enclosure for the whole set of AQ1 subsequential limits and also "in every centered whole-star box N>=2 at every on-site cutoff", which `parameters.finite_box_sign` itself uses for the F1 boxes |
| W2 | `claim_exclusions` against `preregistration.claim_exclusions` | the two lists differ in one entry ("an interaction shift, sign or coefficient of the Euclidean correlation C(s)" against "an interaction shift of C(s)"); BC1 applies the wider entry |
| W3 | `parameters` | declares `metric`, `weights`, `window`, `clock`, `node` and `N_min` but no `d_X` field, which the inherited semantics of `parameters_declare_metric_weights_window` name; BC1 derives no decay estimate, the inherited BB1/BB2 bounds carry their metric (coarse l-infinity, star diameter 1), and `N_min` plays the role of `N_0` |
| W4 | `parameters.obligations` | lists "the finite-box Euclidean node for F2 boxes and for finite F1 boxes (item 4)" as one entry, while item 4 requires two rows; the table carries two rows (N2, N3) |
| W5 | `mandatory_sentence_template` | "every padded box Lambda_N ... has a static Wilson mean of certified sign" leaves the state implicit; the scope is the untruncated F2 ground vector at fixed `N`, at both signs of `tau` (the minus sign a replay), as `finite_box_sign_scope` states; cutoff-`L` F2 states are not claimed |

**Premise observation (non-blocking; checked in `trap_fixtures` and `contract_wording_defects_recorded`).**

| id | source | observation |
|---|---|---|
| P1 | BB2 forward report, section 9 | the harmonic fixture is described as exceeding 4 at `N=119`; the exact first exceedance of `sum_{k=2}^N 1/k` above 4 is `N=83`. This is fixture wording only: no BB2 constant, gate statement or conclusion depends on it. |

## 14. Proposed verdict

**`accepted_within_scope`** (forward half), sub-labels `certificate_restated_for_limit`, `reference_unresolved`, `static_not_dynamic`. The rule in `check.py` follows the contract acceptance:
- `insufficient` if the identification premise is not admitted as used, a restated constant differs from its gate value, or a claim flag overreaches;
- `limited` if the finite-box corollary or the common GNS item is omitted or the obligations table is incomplete;
- otherwise `accepted_within_scope`, which the skeptic's replay must still support.

## 15. Map of required items and controls to statements and checks

| item / control | where stated | `check.py` check id(s) |
|---|---|---|
| item 1 (AV2 node restated) | §§2–3 | `bb2_identification_premise`, `av2_certificate_parsed_exact`, `av2_consistency_replays`, `av2_node_restated_for_limit` |
| item 2 (AW2 enclosure restated) | §4 | `aw2_enclosure_parsed_exact`, `aw2_enclosure_restated_for_limit` |
| item 3 (finite-box sign corollary) | §5 | `bb2_whole_sequence_constant`, `f2_finite_box_sign_corollary`, `f1_boxes_recorded`, `tau_over_100_information_only`, `trap_fixtures` |
| item 4 (finite-box node from the record) | §6 | `finite_box_node_record_facts`, `finite_box_node_only_from_record` |
| item 5 (common GNS item) | §7 | `common_gns_item_scope`, `same_state_not_different_states` |
| item 6 (obligations, falsifying scenario, limitations) | §8 | `obligations_table_complete`, `falsifying_scenario_named_constructions_only`, `round32_limitations_lifted_or_remaining` |
| item 7 (sentence, gate fields, checker) | §§9–11 | `mandatory_sentence_once`, `gate_fields_exported`, `error_ledger_itemized`, `label_block_and_tier`, `report_item_and_control_map`, the 25 control ids |
| contract and premise binding | header, §9 | `contract_snapshot_sha256`, `premise_inventory_bound`, `gate_hashes_pinned_and_cross_bound`, `snapshot_bytes_equal_gate_bindings` |
| `coherent_evidence_tampering` | §11 | `coherent_evidence_tampering` |
| `exact_arithmetic_admission` | §§3–5, 10 | `exact_arithmetic_admission` |
| `no_priority_or_continuum_claim` | header, §12 | `no_priority_or_continuum_claim` |
| `changed_model_relabelled` | §1 | `changed_model_relabelled` |
| `insufficient_verdict_retained` | §14 | `insufficient_verdict_retained` |
| `wrong_delta_alpha_hbar_clock` | §1 | `wrong_delta_alpha_hbar_clock` |
| `placeholder_span_rejected` | §13 | `placeholder_span_rejected` |
| `negation_aware_phrase_scan` | §9 | `negation_aware_phrase_scan` |
| `parameters_declare_metric_weights_window` | §1 | `parameters_declare_metric_weights_window` |
| `named_construction_not_uniqueness` | §§2, 12 | `named_construction_not_uniqueness` |
| `common_clock` | §1 | `common_clock` |
| `topology_named` | §1 | `topology_named` |
| `limit_identified_with_aq1_limits` | §2 | `limit_identified_with_aq1_limits` |
| `certificate_values_unchanged` | §§3–4 | `certificate_values_unchanged` |
| `post_hoc_node_rejected` | §3 | `post_hoc_node_rejected` |
| `finite_box_sign_from_whole_sequence` | §5 | `finite_box_sign_from_whole_sequence` |
| `mirror_sign_replay_not_confirmation` | §§3–5 | `mirror_sign_replay_not_confirmation` |
| `reference_unresolved_retained` | §3 | `reference_unresolved_retained` |
| `obligations_table_complete` | §8.1 | `obligations_table_complete` |
| `rate_range_stated` | §§5, 7, 8 | `rate_range_stated` |
| `round32_gates_untouched` | §§2, 16 | `round32_gates_untouched` |
| `route_b_not_restated` | §§1, 8.1 | `route_b_not_restated` |
| `same_state_not_different_states` | §7 | `same_state_not_different_states` |
| `second_order_remainder_kept` | §§4–5 | `second_order_remainder_kept` |
| `finite_box_node_only_from_record` | §6 | `finite_box_node_only_from_record` |

## 16. Reproduction

```bash
python3 -B research/round33/forward/bc1/check.py --output /absolute/fresh/dir
python3 -B -O research/round33/forward/bc1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/bc1.json research/round33/forward/bc1/report.md
python3 -B research/round33/tools/freeze.py verify research/round33/forward/bc1
```

`check.py` writes `results.json` and `source-manifest.json`; the manifest records the sha256 of `check.py`, `report.md`, every `inputs/` file and `results.json`. No Round32 gate, report or snapshot is edited: this is a new Round33 record that cites them by hash, and `freeze.py` checks that every snapshot equals its repository file. BC1 is investigation 5 of 8 in Round33; this producer executed only the forward statement of BC1.
