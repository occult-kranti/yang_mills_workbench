# BC1 independent derivation before producer comparison

**Standing.** I wrote this after the BC1 contract froze (`frozen_at` 2026-09-25T04:21:44Z, sha256 `3fb84ed3…79bd`) and before reading anything of the BC1 producer. It is a replay from the frozen contract and the admitted gates, with the declared premises for the record checks of item 4. I am a model-agent skeptic with correlated ancestry: same model family as the advisor, the lenses and the producers. This is not human review. Human project author: Hruday N M (BUNZEEY).

**Isolation, disclosed.**
- I did not open, list or read `research/round33/forward/bc1/` or `forward/bc2/`, except `find` on their `inputs/` (names only) and a sha256 comparison of each snapshot with the repository (BC1: 40 files; BC2: 42; all byte-identical, both equal to the contract-derived lists).
- Name-only exposures: a later `git status` printed the untracked paths `forward/bc1/check.py`, `forward/bc1/report.md`, `forward/bc2/check.py` and `forward/bc2/report.md`; I opened none of them. `git log` printed the subject of commit 1833023 (BD1/BD2 drafts, made during BC production); a hash glob over `contracts/*.json` printed the names and hashes of `bd1.json` and `bd2.json`, which I did not read.
- **Late exposure, after my values were final.** After `results.json` (sha256 `48414d13…5bdd`) and the first freeze of this package were written, a final `git log` printed the subject of the BC1 forward producer's commit 5816e0b, which states "N_sign=4". Every value here was computed and recorded before that; nothing was changed afterwards except this disclosure and the freeze hashes of the two markdown files.
- I did not read `experts/modern/bc2-targets-proposal.md`. In `bc-contract-review.md` I did not read §7 ("BC2 targets against my own previews") or the section "Advisor only: previews"; in `bc-contract-review.json` I did not read `previews_recomputed`. I read the rest of both files (the blocking and non-blocking edits, determinations and verification), and the markdown sections only after my values were computed.
- **Prior exposure of the role.** My pre-freeze review (an earlier session of this skeptic role) read that proposal's §10 and computed previews, including `N_sign`. This session saw neither. My code here is new; its independence is limited to derivation and code, and my ancestry is correlated.
- **Scratch.** Private folder `/tmp/claude-0/skeptic-bc-replay-private/` (inventory lists, a scratch script for the route-B constants, replay outputs, source-edit mutation copies). It is not evidence and not a premise. I read no other agent's scratch folder.

**Sources.** The frozen contract, `advisor/selection-bc1.md`, `advisor/plan.json` (vocabulary, recorded), the pre-freeze review as above, and the premises: the AV2, AW2, AW1, AV1, AY1, AY2, AQ1, AQ2 gates; the AV2 forward and reverse reports at the cited labels; the AY2 forward report (O1–O6); the BA1, BA2, BB1 and BB2 gates; the BA1/BA2/BB1/BB2 contracts (inherited control semantics). For format I read my own BB1/BB2 and Round32 AX2 packages; `bc1_check.py` reuses helper code of my own `bb1_check.py`/`bb2_check.py` and imports nothing.

**Exactness.** Every value comes from `bc1_check.py` (55 checks, 25 controls as 86 damaging mutations with 5 positives, byte-identical under `-B`, `-B -O` and plain `python3`). Decimals are previews.

## 1. Model and the admitted objects used

**Model.** `AQ_patterned_zero_selected` at `tau = +10^-8`, with `-10^-8` as a replay of the same `|tau|` formula. The state is `omega_inf`, the limit of the named constructions F1 (AQ1 centered whole-star boxes) and F2 (I1 §6 all-contained-face boxes with padding). The observable is the original xz Wilson loop `W` with cover `R = {0, e_z}`; the clock is `s = alpha t_E/hbar` at the node `s = 1`, with `G = H/alpha`.

**Admitted (read by hash; gate sha256 pinned in the program).**
- **BB2 items 1–3.** For `F ∈ {F1, F2}`, at both signs, at fixed `N` for the untruncated ground vectors: `sup_{M>N} ||rho^{F,M}_R − rho^{F,N}_R||_1 ≤ C' q^(N−1)` with `q = 1/64` and the bound value `C' = 4/984375` (nested telescoping at the hypothesis `C_h = 1/250000`; I checked `C' = C_h/(1−q)` from the BB2 contract's hypothesis text). The F1 and F2 limits coincide on every finite region and equal every AQ1 and every F2 subsequential limit.
- **AV2.** For every AQ1 subsequential state, `|C(1) − d| ≤ r ≤ R`.
- **AW2.** For every AQ1 subsequential state at `+10^-8`, `omega(W) ∈ [lo, hi] = [tau/144 − K_2^+ tau^2, tau/144 + K_2^+ tau^2]`; mirrored at `-10^-8`.
- **BA2 item 4** (the F2 limit dynamics is the AQ1 limit dynamics `T_theta`) and **BB2 item 5** (correlation functions on `|theta| ≤ 8`, with a rate in N only on `5 ≤ N ≤ 14000`).

## 2. Item 1: the AV2 node restated for `omega_inf`

Every value is read from the AV2 gate and checked equal to the gate decision:
- `d = 497870683678639429793424156500617766317/(4·10^40)` ≈ 0.012446767091966;
- `R = 1831967503411879425147166810021607/10^40` ≈ 1.83196750341e-7 (at most `10^-6`, margin above 5.4586);
- the interval `[497863355808625782275723567833377679889/(4·10^40), 99575602309730615462224949033571570549/(8·10^39)]`, which is exactly `[d − R, d + R]`.

**Free reference.** With a Taylor bracket of `e^3` of width below `10^-58`, `e^{-3}/4` lies strictly inside the interval, and `d` lies within the arithmetic half-width `1/(4·10^40)` of it. So the restatement keeps `reference_unresolved`: no interaction shift, sign or coefficient of `C(s)`.

**Why it applies to `omega_inf`.** BB2 item 3 makes `omega_inf` an AQ1 subsequential state (indeed equal to every one), and AV2 covers every such state. The identification comes first, then the restatement; nothing is re-derived. At `-10^-8` the `-tau` limit is an AQ1 subsequential state at `-tau` (BB2 holds at both signs), so AV2's replay of the same `|tau|` formula applies to it. It is a replay, not a second confirmation.

## 3. Item 2: the AW2 enclosure restated for `omega_inf`

`K_2^+ = 81108864767825329926713064490531229475390625/24176936535511801466930759024724079017984` (≈ 3354.80322946). At `tau = 10^-8`, with `D = 618929575309102117553427431032936422860390400000000`:
- `lo = 42773581813770903096597852821080380528959/D` = `tau/144 − K_2^+ tau^2` exactly (≈ 6.91089641e-11);
- `hi = 43188859201382168785822623711271900423873/D` = `tau/144 + K_2^+ tau^2` exactly (≈ 6.97799248e-11);
- the mirror at `-10^-8` is `[−hi, −lo]`, exactly as the gate prints it.

The gate's exclusion margin `lo/(K_2^+ tau^2)` (≈ 206.00005) and sign margin `1/(144 K_2^+ tau)` (≈ 207.00005) are reproduced exactly. The full second-order remainder `K_2^+ tau^2` stays at both endpoints.

## 4. Item 3: the finite-box sign corollary for the padded family

**Statement.** For every `N ≥ 2` and both signs, with `omega^{F2,N}` the untruncated F2 ground state on `Lambda_N`:

`|omega^{F2,N}(W) − omega_inf(W)| ≤ ||W|| · ||rho^{F2,N}_R − rho^inf_R||_1 ≤ C' q^(N−1)`.

**Proof.**
1. BB2 item 1 at fixed `N`: `||rho^{F2,M}_R − rho^{F2,N}_R||_1 ≤ C' q^(N−1)` for every `M > N`.
2. `rho^{F2,M}_R → rho^inf_R` in trace norm (BB2 item 1 and its limit), so the bound passes to `M = ∞` through the closed trace-norm ball.
3. `rho^inf` is the common F1/F2 limit (BB2 item 2) and equals every AQ1 subsequential limit (item 3), so AW2 applies: `omega_inf(W) ∈ [lo, hi]`.
4. `W ∈ B(H_R)` with `||W|| ≤ 1`, and trace duality gives the first inequality. The effect refinement `1/2` does not apply, because `W` is not an effect (fixture `fixture_trace_duality_no_half`).
5. Hence `omega^{F2,N}(W) ∈ [lo − C' q^(N−1), hi + C' q^(N−1)]`, and the mirror at `-10^-8`. The sign is certified whenever `C' q^(N−1) < lo`, strictly. ∎

**The rate in N** is `q^(N−1)` with `q = 1/64`, for every `N ≥ 2`. It is a density rate in N. The correlation-function rate in N (BB2 item 5) holds only on `5 ≤ N ≤ 14000`, and BC1 adds nothing to it.

**`N_sign` (exact).** The widening is `C' q^(N−1)`: `1/15750000` at `N = 2`, `1/1008000000` at `N = 3`, `1/64512000000` at `N = 4`.

| N | widening `C' q^(N−1)` | widened enclosure at `+10^-8` | at `-10^-8` | sign certified |
|---|---|---|---|---|
| 2 | 6.3492e-8 | [−6.3423e-8, 6.3562e-8] | [−6.3562e-8, 6.3423e-8] | no |
| 3 | 9.9206e-10 | [−9.2295e-10, 1.06184e-9] | [−1.06184e-9, 9.2295e-10] | no |
| **4** | **1.5501e-11** | **[5.36080e-11, 8.52809e-11]** | **[−8.52809e-11, −5.36080e-11]** | **yes** |
| 5 | 2.4220e-13 | [6.88668e-11, 7.00221e-11] | mirror | yes |
| 6 | 3.7844e-15 | [6.91052e-11, 6.97837e-11] | mirror | yes |

**`N_sign = 4`**, the least `N ≥ 2` with `C' q^(N−1) < tau/144 − K_2^+ tau^2`. The exact widened endpoints at `N_sign = 4` and `N_sign − 1 = 3` are in `results.json` (check `finite_box_sign_widened_enclosures`). At `N = 4`:
- the lower endpoint is `232256915653307984268043972456662444208313/4332507027163714822873992017230554960022732800000000`;
- the ratio `lo/(C' q^3)` ≈ 4.4584.

Nothing is claimed for `N = 2, 3`; that range is an open row (N4 below), not a failure.

**Robustness (the constant must still be read).** `N_sign = 4` for every `C'` in `[lo·64^2, lo·64^3) ≈ [2.8307e-7, 1.8117e-5)`. The labelled union value `1/250000` and the labelled re-evaluated value (about `9.0465e-7`) give the same integer; they are not used.

**`tau/100`, information only.** At `tau = 10^-10` the same `C'` (which does not depend on `tau` at the hypothesis values) would give `N_sign = 5`. The widened half-width at `N = 4` would be about `1.5501e-11` against a first-order term `6.944e-13`. AW2 admits the enclosure at the cap only, so nothing below the cap is claimed and no bracket applies.

**F1 boxes.** The AW2 gate certifies "every centered whole-star box N>=2 at every on-site cutoff (uniform in the box)". The untruncated F1 vector at fixed `N` follows by AV1 cutoff-vector removal and the closed interval. This is agreement, not a re-derivation.

**Tier and labels.** The new constant family (the widened enclosure and `N_sign`) carries `exact_first_order`. In place of a route it records its inputs: the AW2 gate endpoints, and `C'` with the BB2 assembly `nested_telescoping` and the BB1 route `polymer_kp`. The restated constants keep their Round32 labels.

## 5. Item 4: what the record proves about finite boxes

I checked each claim of the frozen item against the hash-pinned record:
- the AV2 gate quantifies over "every AQ1 subsequential state of the centered whole-star construction (each chosen state separately";
- AV2 forward F01–F02 define `c`, `C` and the spectral measure for the GNS vector of AQ1's chosen state with "AQ1 §5 (nonnegativity only)"; F07 is the window lemma, and F15 is the comparison in that state;
- the only box-by-box step is F13–F14 ("Fix a centered whole-star box"), passed to the AQ evolution ("So (F14) holds for the actual AQ evolution at every real theta");
- AV2 reverse R01, R02, R08, R12 and R13 are present, and its control table rejects "finite-box provenance" under `changed_model_relabelled`;
- the AW1 gate item (1) states the finite-box `C_N(s)` "with the tau^2 constant explicitly unbounded (not uniform in N".

So the record proves no finite-box node, and BC1 restates none. Two open rows follow (N2 and N3 below). The F1 route is short, but it is a new derivation: the spectral measure of `G_N − E_N` in `chi_N` is carried by `[0, ∞)` because `E_N` is the ground energy, and F13–F14 and AV1's per-box `D` exist. The F2 route additionally needs the F2 incidence and slope, which the AV2 record does not have.

## 6. Item 5: the common GNS item

- **One state.** The F1 and F2 limits are one state `omega_inf` (BB2 items 2–3). It has one GNS triple `(H, pi, Omega)`, unique up to unitary equivalence.
- **One dynamics.** `omega_inf` is `T_theta`-invariant (AQ1 stationarity, inherited by BB2 item 3), so `T_theta` has a unique unitary implementation fixing `Omega`. It is strongly continuous with a nonnegative generator (AQ1 gate: "strongly continuous GNS evolution with a nonnegative self-adjoint physical energy generator"). BA2 item 4 identifies the F2 limit dynamics with the same `T_theta`.
- **Correlation functions** on `|theta| ≤ 8` are the limits of the finite-box correlation functions of either family (BB2 item 5), with a rate in N only on `5 ≤ N ≤ 14000`.
- **Scope.** This is not equality of GNS dynamics of different states; `gns_dynamics_equality_claimed` stays false. `dynamics_limit_identified_claimed: true` restates BA2 item 4 and adds no dynamics claim.

## 7. Item 6: the updated obligations table (the skeptic's own)

| row | name | status after BA1–BB2 | closing gate and scope, or missing premise and candidate route |
|---|---|---|---|
| O1 | uniqueness of the limit | **open** | Missing: a statement covering every ground state (a two-state estimate or a classification). Route: HTW-type stability or a Dobrushin-type condition with evaluated constants; or the BB1 marginal-locality lemma extended to arbitrary outside states. The AY2 falsifying scenario is now excluded **for F1 and F2 only** (BB2 items 2–3), not for states outside them. |
| O2 | whole-sequence convergence | closed within scope | BB2 item 1: reduced densities of F1 and F2 on every finite region, `sup_{M>N}`, untruncated at fixed `N`; zero-selected family, fixed spacing, `|tau| ≤ 10^-8`. |
| O3 | translation invariance | closed within scope | BB2 item 4: coarse translations only, the limit of the named constructions; non-coarse translations rejected. |
| O4 | a rate in N | closed within scope | BB2 item 1 with BB1 (per comparison) and BA1 (coefficients): densities `q^(N−1)` for every `N ≥ 2` (regions: every `N` with `Y` inside `Lambda_N`); correlation functions only on `5 ≤ N ≤ 14000` (BB2 item 5). |
| O5 | boundary independence of dynamics on compact time windows | closed within scope | BA2 items 2–4 (F1 versus F2 Heisenberg dynamics of `A ∈ B(H_R)` on `|theta| ≤ 8` at a rate in N for every `N ≥ 2`) and BB2 item 5 (correlation functions). Not uniform in time; not GNS dynamics of different states. |
| O6 | dynamics of the padded family itself | closed within scope | BA2 items 4–5 ("AY2 row O6 closed within scope" in the BA2 decision). |
| N1 | states outside the named constructions; other boundary conditions | open | Missing: density comparisons for other prescriptions, each with its itemization. Route: the BB1 split with the prescription itemized (AY1-type), or O1 routes. |
| N2 | finite-box Euclidean node, finite F1 boxes | open | Missing: the window lemma for the untruncated finite-box ground vector with generator `G_N − E_N` at the unchanged `M_0 = 2`, `M_1 = 4s/pi`, with AV1's per-box `D` and AV2's per-box slope. Route: rerun AV2 F01–F15 per box. |
| N3 | finite-box Euclidean node, finite F2 boxes | open | Missing: the N2 premises plus the F2 incidence of the groups meeting `R` and the F2 slope (not in the AV2 record). Route: the AY1 itemization for the groups meeting `R` and an owner-set relative-unitary slope. |
| N4 | F2 finite-box sign for `2 ≤ N < N_sign` (`N = 2, 3`) | open | Missing: a finite-box enclosure sharper than AW2 widened by `C' q^(N−1)`. Route: the AW1 remainder re-derived per F2 box (AY1 itemization). The labelled BB2 values do not help (§4). |
| N5 | correlation-function rate in N beyond `N = 14000` with the frozen `r_N` | open | Missing: a region term that does not outgrow `q^(N−r_N)`. Route: a slower `r_N`, or a region form without the factor `e^{|Y|/10^8}`. Convergence without a rate in N already holds. |
| N6 | GNS dynamics of different states | open | Not needed for F1/F2 (one state); for other states it waits on N1 or O1. |
| N7 | uniform-in-time statements | open | Missing: bounds beyond `|theta| ≤ 8`. Route: the AQ2 gap `alpha/16` with a clustering-in-time argument (not formulated). |
| N8 | non-centred F2 volumes in the fifth BB1 comparison | open as a gated statement | Missing: a gated AY1 itemization H1–H5 for every F2 volume containing `Lambda_N` (reviewed local reading only). Route: a statement loop restating the AY1 items for general F2 volumes. |
| N9 | the route-B uniform model | **pending** | BC2 is produced in parallel; this row cites the BC2 gate only once it is recorded (after the BC1 gate). |
| N10 | analyticity of the reduced density in the coupling | open | Missing: a zero-free region of the complexified normalization (BA1, BB1 limitations). |
| N11 | untruncated creation coefficients | open | BA1 limitation; not needed by BB1/BB2. |
| N12 | anything uniform in the lattice spacing `a` | open | Every constant is at fixed spacing. |
| N13 | the continuum problem | open | Weak coupling and `a → 0`; none in this record. |

## 8. Round32 limitations: lifted or remaining (gates in `shared_premises` only)

| gate | limitation | after Round33 |
|---|---|---|
| AV2 | each AQ1 subsequential state separately; no uniqueness, whole-sequence convergence or rate in N | lifted in part for the named constructions (one limit, density rate in N `q^(N−1)` for every `N ≥ 2`); uniqueness of every ground state remains open; no finite-box node |
| AW2 | whole-set statement; no whole-sequence convergence or rate in N; `-tau` pairing only along a common subsequence | whole-sequence convergence and the F2 finite-box sign for `N ≥ 4` lifted within scope; the pairing limitation stays and is not needed (R2) |
| AW1 | finite-box `tau^2` constant for `C_N(s)` not uniform in N | remains |
| AY2 | uniform local closeness only; six obligations | O2–O6 closed within named scopes; O1 open; the falsifier excluded for F1 and F2 only |
| AQ1/AQ2 | subsequential states; full-GNS gap only as qualified in AQ2 | subsequence lifted for the named constructions; the AQ2 qualification remains |
| every gate | zero-selected family, fixed spacing, `|tau| ≤ 10^-8`; no continuum or weak coupling | remains |

## 9. Predictions (the post-comparison flags any difference)

| quantity | prediction |
|---|---|
| restated `d`, `R`, interval | exactly the AV2 gate rationals; the interval equals `[d−R, d+R]` |
| restated AW2 endpoints | exactly the gate rationals, `tau/144 ∓ K_2^+ tau^2`; mirror `[−hi, −lo]` |
| `C'` used | `4/984375` (nested_telescoping bound value) |
| `N_sign` | **4** |
| widened enclosure at `N = 4` | `[5.36080e-11, 8.52809e-11]`, mirror `[−8.52809e-11, −5.36080e-11]` |
| widened enclosure at `N = 3` | `[−9.22955e-10, 1.061843e-9]` (contains 0), mirror likewise |
| ratio `lo/(C' q^3)` at `N_sign` | ≈ 4.4584 |
| finite-box node | none restated; two open rows (F1, F2) |
| gate fields | the 15 frozen values exactly; no `resolved_interaction_shift` |

## 10. What I will require of the producer

1. Every restated rational read by hash from the gate and equal to it: no re-rounding and no re-derived radius. The Round32 gates are cited by hash and never edited.
2. The identification (BB2 items 2–3) before any restatement. The `-tau` statements labelled as replays (R2).
3. Item 3 written as a proof: BB2 item 1 at fixed `N` for the untruncated F2 vector, `M → ∞` through the closed ball, BB2 items 2–3, AW2, and trace duality with `||W|| ≤ 1` (no `1/2`). `C' = 4/984375` named as the bound value. `N_sign` computed exactly with the strict comparator, and the widened endpoints at `N_sign` and `N_sign − 1` given at both signs.
4. Nothing claimed for `N = 2, 3`, or for cutoff-L F2 states. F1 boxes recorded as agreement with AW2.
5. Item 4 as frozen: no finite-box node, two open rows with their missing premises and a candidate route, and `finite_box_node_claimed: false`.
6. The common GNS item with its scope; the correlation rate in N only on `5 ≤ N ≤ 14000`.
7. The obligations table with O1–O6 (status plus closing gate and scope, or missing premise and route), every new row the contract lists, the falsifier excluded for F1/F2 only, and the route-B row pending.
8. The template quoted once; the gate fields exactly as frozen; all 25 controls as damaging mutations; byte-identical replays.

## 11. Producer-error checklist

1. A restated radius or endpoint re-rounded, re-derived, or computed with a different `pi` or `e^{-3}` enclosure.
2. `C'` taken as `1/250000` (union, labelled), about `9.05e-7` (re-evaluated, labelled) or the BB1 `C` (per comparison, no whole-sequence passage). `N_sign` is unchanged, so only the string shows it.
3. `N_sign` computed with `≤`, or with the widening on one side only, or with `K_2^+ tau^2` dropped (that would still give 4, so the formula has to be read).
4. The `1/2` effect factor applied to `W`.
5. A finite-box node stated as a restatement, or the window lemma applied box by box.
6. The `-tau` value counted as a second confirmation, or derived by pairing states along a subsequence without a label.
7. The correlation rate in N stated without its range; the word rate without "in N".
8. O1 marked closed; the falsifier excluded for all states; the route-B row citing a BC2 outcome.
9. Phrases on the forbidden list ("confirms", "resolves the reference", "the thermodynamic limit").

## 12. Replay

`python3 -B research/round33/skeptic/bc1_check.py --output <absolute fresh dir>`. The normal, `-O` and no-`-B` runs are byte-identical, and no `.pyc` is written. Six source-edit mutations of scratch copies all abort (listed in the contract review §5).
