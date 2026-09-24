# AX2 skeptical review (post-comparison, single direction)

**Verdict: accepted_within_scope, sub-label `reference_unresolved`.** The single forward producer and my frozen pre-comparison replay agree exactly on every value:

- The exact datum is `d=497870683678639429793424156500617766317/(4·10^40)` (about 0.012446767091965986). It is the AV2 gate datum, unchanged because the reference is unchanged in route B.
- The certified radius is `r<=R'=1912298807996871790146581299723633/10^40`, about **1.91229880800e-7**. Its exact rational has the itemized form `2D'+2D'^2+51|tau|/pi^-` plus the arithmetic half-width `1/(4·10^40)`.
- `C_tau(1)` lies in `[0.012446575862085186, 0.012446958321846786]`. This is contained in `[d-R', d+R'] = [99572606896681488461252714035083774357/(8·10^39), 497878332873871417280584742825816660849/(4·10^40)]`.
- The Boolean `r<=10^-6` is true, with margin at least 5.22930.
- The free value `e^{-3}/4` lies inside the interval.
- `s*` lies in `[5.982012284161, 5.982012284163]` (about 5.98201228416). That is a crossover of the formula, not a certified node.

There are **no blocking issues**.

**Admission basis.** AX2 has a single producer (`producers=["forward"]`, `direction: single+skeptic`). Admission rests on the forward producer plus my independent replay from the contract, which I wrote and froze before opening anything under `forward/ax2/`. The `tau=-10^-8` value is the `U_E` mirror. It is a replay, not a second confirmation.

**Standing.** I am a model-agent skeptic with correlated ancestry: I share a model family with the advisor and the producer, and my own AX1 review (a shared premise) already printed the feasibility value 1.9123e-7. The exact agreement below therefore shows that one admitted formula was replayed correctly. It is not independent physical confirmation, human peer review or formal verification. Human project author: Hruday N M (BUNZEEY).

**My pre-comparison package is unchanged.** It consists of:
- `ax2-independent-derivation.md`;
- `ax2_check.py` (72 checks, all 25 controls);
- `ax2-contract-review.md`;
- `ax2-independent/results.json` (sha256 `db7e6b56…a5a1`).

Its hashes still match `ax2-independent-freeze.json` (sha256 `e06bbcf7…d602`). A fresh replay under normal and `-O` Python reproduces its `results.json` byte for byte. It was committed as `85df74d` at 01:48:07Z, before the forward commit `0ae59e6` at 01:50:59Z.

**This review adds:**
- `ax2_postreview_check.py`: 30 exact checks, 42 must-abort source edits (each aborting at the intended check), 2 silent edits that are accounted for, and 11 damaged packets that my own validator rejects;
- `ax2-postreview/results.json`: byte-identical under normal and `-O`, sha256 `4a0b33c2…04b9`;
- `ax2-replays.json`.

## What is certified, with quantifiers

**Model.** The uniform Kogut–Susskind SU(2) Hamiltonian on Z^3 at fixed spacing and strong bare coupling. Every elementary face, selected faces included, has `nu=alpha*tau/24`. The AL1 dictionary gives `tau=96/g^4`, so `g^4=9.6×10^9` at the cap.
- **Route B (AX1).** The Haar reference, the tau-independent on-site `h_b=8 sum C_e`, whole stars (21 omitted faces, norm `7|tau|`), and one single-factor group `psi_b=-(tau/3) sum W_g` per factor for its three selected xy faces.
- **Coupling and observable.** `tau=+10^-8`; `-10^-8` is the `U_E` mirror, with no real `g`. The node is `s=1`. The observable is the original xz Wilson loop `W` with cover `R={0,e_z}`.
- **State.** Every AQ1 subsequential state of the centered whole-star-plus-single-group construction (`N>=2`), each state separately.
- **Clock.** `s=alpha*t_E/hbar`, `G=H/alpha`.
- **Label**, as exported: `uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling (g^4=9.6x10^9)`.

**Statement.** `|C_tau(1)-d|<=r<=R'`, where
- `E'=M_0(D'+D'^2)+k'M_1`, with `M_0=2` and `M_1=4s/pi`;
- `k'=51|tau|/4`, from 7 stars and 2 single-factor groups meeting `R`;
- `D'` is the AX1 gate's forward tier-(ii) value `2425369125199104794263242601250/167893028420061547330293754713793182097` (about 1.44459192143e-8, outward).

**What does not follow.**
- No interaction shift, sign or coefficient of `C(s)`: the free reference is inside.
- No uniform Wilson-mean sign certificate and no uniform `K_2` (loop-2 veto).
- No node other than `s=1`, and no grid.
- No uniqueness, whole-sequence convergence or rate in `N`.
- No weak-coupling or continuum statement.
- No scientific priority.

## Exact comparison (own Fraction code, nothing imported from the producer)

| quantity | producer | my re-derivation | status |
|---|---|---|---|
| `D'` | gate decision rational | `J'=29|tau|`, `t_1'=52|tau|/144`, `T'=t_1'/(1-352J')=13/3599632512`, `eps=2T'+T'^2`, `D'=2eps(1+eps)/(1+eps^2)`, same value at both signs | equal; also equal to the contract string, both gate texts and my pre-comparison value |
| `k'` | `51/400000000` | own fine-lattice enumeration: 7 stars (anchors `R-S`), 2 groups (`{0}`, `{e_z}`), 153 faces charged, 88 meeting `R` (82+6), 16 inside, per star 21,21,16,8,8,4,4; `N=2,3,4` give (7,2) and `N=1` gives (4,2) | equal; local in the box |
| `M_0`, `M_1` | 2, `4s/pi` | half-line integrals `1/b+1/a+2s/a^2+4s^2/a^3=8s^3/(a^3b)` in Gaussian rationals, `|a^3b|^2=(s^2+theta^2)^4`, and antiderivative identities | equal |
| `pi` | Machin, `10^-40` | Gauss `48atan(1/18)+32atan(1/57)-20atan(1/239)`, `10^-60` | the producer's bracket contains mine |
| `e^{-3}/4` | alternating Taylor with halving, `10^-40` | power series of `e^3` with geometric remainder, inverted, `10^-60` | the producer's bracket contains mine |
| terms | state `2D'`, mean square `2D'^2`, kernel `51|tau|/pi^-`, arithmetic `1/(4·10^40)` | same formulas | equal as rationals |
| radius | exact `r`; ceiling `R'` | own analytic bound (Gauss `pi`) `<= r <= R'`; `r` exceeds my analytic upper bound by about 2.5e-41 | consistent; `R'` identical to my pre-comparison common bound |
| datum, interval | `d`, `[d-r,d+r]` | `d` = AV2 gate datum; `[d-r,d+r]` contains every value the lemma allows under my own enclosures | contained; my pre-comparison `d±R'` contains it, and it contains my `10^-60` interval |
| mirror | identical `d`, `r`; `mirrored_coupling_replay:true` | `|tau|`-only formula | replay only |
| `s*` | `[pi^-(10^-6-A)/(51|tau|), pi^+(…)/(51|tau|)]` with `E'^+(s*^-)=E'^-(s*^+)=10^-6` exactly | my Gauss-`pi` interval is nested inside it and inside my pre-comparison `[5.982012284161, 5.982012284163]`; below AV2's 6.236863446 | nested |

**Only difference: display precision.** The producer quotes `D'≈1.44459192142e-8` truncated in the report text, while its packet preview is 1.44459192143e-8 outward. No admission Boolean reads a decimal. Every decimal quoted in the report is within one unit of its last digit of my exact values, on the stated side. This covers the table at `s=1/2, 2, 5`, the bound at `s=128`, the four term decimals, the margin, the excess over AV2 (at least 8.03e-9), the floors, the first moment 46.907878, the AT4-type interval, tier (i), `s*`, and the contract preview (within 10^-9).

## Rejected alternatives and retained failures

**Rejected state values.** Each value below differs from the bound `D'`. The producer rejects each as a damaging mutation (`av1_tier_bound`, 10 rejections; `tier_mixing_rejected`, 4). The rejected values are:
- the AX1 reverse R-refinement (≈1.22237e-8);
- the AX1 target `4/10^7`;
- the AV1 zero-selected `D` (≈1.36125e-8);
- tier (i) (≈2.45261e-5);
- the mis-rounded contract note `4.19e-7`;
- `T'^2` dropped (≈1.4445919188e-8);
- the density form replaced by `2eps`;
- non-self-consistent `T'` (my own control).

My source edits show that `D'` cannot run silently:
- dropping the pair term or the density form in the calculator aborts at the gate pin;
- removing the pin as well aborts at `ax1_gate_state_bound_bound`, where `check.py` recomputes the gate formula;
- a gate digit edited with its hash rebound aborts;
- the contract `D_prime` set to the reverse refinement with its hash rebound aborts.

This closes AX1 N5 for AX2.

**Rejected slopes.**
- The seven-star slope `49|tau|/4` (AV2's zero-selected slope) is rejected as a changed model.
- The extensive norm is rejected because it depends on the box.
- A dropped conjugation factor 2 is rejected.
- `root-N` variants are rejected.

My edits (single groups set to 0, factor 2 dropped, contract `k_prime` set to 49 with rehash) all abort.

**Retained failures** at unchanged `tau` and `s`, recomputed with my own brackets:
- **AT4-type Poisson certificate at `L=10^4`,** with `D=2sqrt(17|tau|)` and `k'`: in `[8.5790595e-4, 8.5790596e-4]`. The same formula with AT4's own inputs reproduces the frozen AT4 decimal `0.000841518704386267` to `10^-15`.
- **Poisson floor with `D->0`:** in `[1.313477283e-6, 1.313477284e-6]` for every `L`, from `log(1+L^2)>=2log L` with the minimum at `L=1/(2k')`. With `D'` it is at least 1.3279232e-6. The truncated first moment at `L=10^32` is at least 46.907878.
- **Tier-(i) window:** at least 4.921572155e-5.

All are insufficient and retained. Retuning `tau` to the floor threshold is rejected.

## Review against the contract items

1. **Lemma transfer, verbatim.**
   - The window, conventions and constants are parsed from the hash-bound AV2 contract and gate and re-audited (`C^2` matching with jump `-8s^3`, the transform, the modulus, `M_0`, `M_1`, `M_2`, `int ghat=1`).
   - `G>=0` and the finite spectral measure are the AQ1 nonnegativity and GNS construction re-applied (AX1 gate item 3).
   - Only `k'` and `D'` change. `D'` is read from the AX1 gate decision, whose snapshot hash `1b8fb152…d177` is pinned in `check.py`, and it equals the contract, the accepted text, the calculator pin and the recomputed formula.
   - `+tau` is the certificate; `-tau` is the mirror replay.
2. **Itemized terms and datum.**
   - The four preregistered terms are exact and none is `not_applicable`.
   - The datum is the midpoint of the directed enclosure and equals the AV2 gate datum.
   - My contract-review item 3 is met: the report states the Haar reference on the cover and the tau-independent `h_b`, with the selected faces only in `B_N`.
   - The first-order mean `+tau/144` is charged through `m^2<=D'^2`. Replacing it by `(tau/144)^2` is rejected, as is a zero mean.
3. **Label.**
   - The exported label is exactly the contract's.
   - Every mention of weak coupling or the continuum in `results.json` (35 hits) and `report.md` (11 lines, bound to the report hash) is a negation, a flag set to `false`, an exclusion entry or a rejected mutation.
   - No sign rider or `K_2` value is attached.
   - `uniform_wilson_claim:true` carries the fixed-spacing scope string and the phrase "no uniform Wilson-mean sign certificate".
4. **Controls.**
   - All 25 contract ids have a passing check with at least one damaging mutation: 98 rejections among the 25 controls, plus 31 calculator-domain rejections, for 129 in total.
   - For each id I verified that the labels carrying its meaning are present. Examples: `av1_tier_bound` has the reverse refinement, the target, the zero-selected `D` and tier (i); `local_not_extensive_duhamel` has the extensive norm, the seven-star slope and factor 2; `single_producer_declared` has a reverse route claimed, the replay dropped, self-review called independent and the mirror as a confirmation.
   - Weakening the producer's own validators makes the run abort with "damaging mutation accepted". The weakened validators are the state bound, the label, the claim flags, the single-producer check, the group count and the slope. So the controls are live.
5. **Calculator and flags.**
   - The domain was exercised on a hash-verified copy:
     - only the uniform triple is accepted (a zero triple at `tau≠0`, a non-uniform triple, and a positive triple at negative `tau` are all refused);
     - `|tau|<=10^-8` at both signs, so `1/99999999` is refused;
     - `s>0` and positive scales;
     - exact input only (floats, Booleans, `None` and exponent text are refused);
     - `D'` and `k'` are not inputs (TypeError);
     - only the tier-(ii) state tier and the `C^2` window are accepted;
     - a `fixed_design` that is not a Boolean, or that changes the design, is refused.
   - `E'(s)` is exactly linear in `s`.
   - The flags match contract item 5:
     - false: `continuum_claim`, `weak_coupling_claim`, `resolved_interaction_shift`, `scientific_priority_verified` and `grid_claim`, and also `wilson_mean_sign_certified`, `k2_uniform_claimed`, `state_uniqueness_claim`, `independent_review_claimed` and `mirror_is_second_confirmation`;
     - true: `uniform_wilson_claim` (fixed spacing) and `euclidean_node_certified`.
6. **Independent replay.** My package was frozen and committed before the forward commit, and it agrees exactly.

## Source-edit receipts

Each edit is applied to a temporary copy of the closure outside the checkout. An unmutated copy reproduces `output/results.json` and `source-manifest.json` byte for byte.

**Must abort: 42 of 42 aborted, each at the intended check or validator.**
- **Calculator (22):**
  - single groups set to 0 (slope 49);
  - pair term dropped;
  - `2eps` density form;
  - pin removed with the pair term dropped;
  - state `D/2`;
  - `pi^+` in the kernel term;
  - mean square dropped;
  - exponent 24;
  - `M_0=1`;
  - weak-coupling label;
  - `continuum_claim` true;
  - cap widened;
  - zero triple accepted;
  - float accepted;
  - fixed design unchecked;
  - mirror flag dropped;
  - arithmetic term dropped;
  - factor 2 dropped;
  - `uniform_wilson_claim` false;
  - window sign flipped;
  - resolved shift claimed;
  - gate constant digit.
- **`check.py` (10):**
  - six validator weakenings: state bound, label, claim flags, single producer, groups, slope;
  - selected predicate changed;
  - incoming-star anchors dropped;
  - tier (i) used as `D'`;
  - a `decimal` import.
- **Inputs (10):**
  - contract byte edit without rehash;
  - contract target `10^-7` with rehash, which aborts at `target_boolean_1e-6` and shows that the target is read from the contract;
  - contract `D_prime` set to the reverse refinement, with rehash;
  - contract `k_prime` set to 49, with rehash;
  - contract `tau` halved with rehash, which aborts and shows that `tau` is read from the contract;
  - AX1 gate byte edit;
  - AX1 gate `D'` edit with rehash;
  - AV2 gate byte edit;
  - undeclared `skeptic/ax2*` input;
  - premise snapshot removed.

**Silent by design (2, accounted for).**
- A literal `D'` equal to the gate value in `check.py` runs to completion; only the `check.py` sha256 changes. My static data-flow validator rejects the mutated source. It requires `tau`, `s`, `target`, `D'` and `k'` to be assigned once, from the contract snapshot. It also finds no `assert` in either file.
- Removing only the box-dependence test from the Duhamel validator runs to completion, as the producer disclosed. The slope-value test is the redundant guard, and removing both aborts.

## Replays, closure and isolation

**Replays.** `replay_declared.py ax2` gives identical output under normal and `-O` Python (sha256 `9add8d25…64e0`). It does the following:
- verifies the `freeze.json` closure (35 listed files; `freeze.json` sha256 `b38f3a75…3950`);
- compares the 30 input snapshots with their repository sources byte for byte;
- replays `check.py` under normal and `-O` into fresh external directories. Both runs reproduce `output/` byte for byte: `results.json` `ba8d36d7…d3a7` and `source-manifest.json` `e17de51d…d7b0`, with 52 checks each;
- runs `tools/freeze.py verify research/round32/forward/ax2`, which reports `verified`.

The receipts are in `ax2-replays.json`.

**Inputs.** The inputs are exactly `AGENTS.md`, `contracts/ax2.json` and the 28 `shared_premises`. Every hash is pinned in `check.py` (contract, AX1 gate, `selection-ax2.md`) or bound by the pinned AX1 gate or the AX1-bound AV2 gate. There is no `skeptic/ax2*` or `reverse/ax2` input, and no `reverse/ax2` package exists.

## Blocking issues

None.

## Non-blocking findings

**N1. Read isolation is verifiable for repository inputs only.**
- **Concurrent development.** The forward `calculator.py` (01:38:07Z) and `check.py` (01:45:43Z) were written at the same time as my pre-comparison package: `ax2_check.py` at 01:41:35Z, results at 01:41:43Z, commit at 01:48:07Z. The forward report (01:50:06Z) and freeze (01:50:26Z) came after my commit.
- **What each side declares.**
  - The producer declares no `skeptic/ax2*` read, and its closure holds none. I declared no `forward/ax2` read; I saw only the untracked `calculator.py` name in `git status`.
  - The producer's disclosed scratch (`/tmp/claude-0/ax2-private`, `/tmp/claude-0/ax2-run`) matches the listings, which I checked by name and time only.
  - The shared scratchpad root holds an `ax2feas.py` (01:35:33Z), which I checked by name only. The same AX2 budget appears in the committed assistant tools (`5c80b0a`, `06ad78b`) and in my AX1 review.
- **Why the agreement is expected.** The codes differ in structure: Machin and alternating Taylor to `10^-40` against Hutton and Taylor to `10^-60`; 52 against 72 checks; different ids and anchor ranges. The identical `R'` is expected by construction, because both round the same admitted formula to the same `10^-40` grid. My pre-comparison `R'` used the admitted AV2 calculator's primitives, which the producer's calculator reuses.

**N2. The calculator's reusable mode goes beyond the cap.**
- **Below the cap.** `D'(|tau|)` is the tier-(ii) `|tau|`-form (AX1 F17, gate item 6). It is pinned to the gate rational at the cap, strictly smaller below it, and labelled `state_bound_equals_ax1_gate_value:false`.
- **At `tau=0`.** This value is accepted as the free Casimir limit: `D=0`, radius equal to the arithmetic half-width, label "…strong bare coupling limit tau=0 (g^4 infinite; free Casimir model)", and `nonzero_interacting_coupling:false`. There the uniform triple coincides with the zero triple, so the report's "zero triple rejected" holds only for `tau≠0`.
- **Validity.** Both are mathematically valid. My contract-review reading (item 8: the cap value at every `|tau|`, no zero branch) is more conservative. Below-cap and `tau=0` values are corollaries, not AX2 admissions, and any reuse needs its own contract. The gate should say so.

**N3. Silent-by-value edits.**
- A literal `D'` equal to the gate value passes at runtime. It is caught by static data-flow review and protected by the `check.py` hash in `freeze.json`. This is the AX2 analogue of AW2 N3.
- The Duhamel validator's box-dependence test alone is redundant; this was disclosed by the producer.

**N4. Display.** The report text quotes `D'≈1.44459192142e-8` truncated. The outward 12-digit preview is 1.44459192143e-8. No Boolean reads it.

**N5. Undeclared reads, all disclosed.** They are the tools README, `freeze.py` and the AV2 forward `check.py`, read for protocol and style only. Parts of the AX1 reverse report, the AQ1 report and the SKILL files were read in part, and the AM2, AQ2, I1 and AV2-reverse reports were not opened; all are hash-verified. None carries premise weight beyond the admitted gates.

## Limitations

1. **Single direction.** One forward producer instantiates the admitted AV2 lemma with the admitted AX1 constants. Admission rests on that producer plus my pre-comparison replay from the contract. Our ancestry is correlated, and the headline value was already in shared premises. The exact agreement is a replay of one admitted formula, not independent physical confirmation.
2. **Model scope.**
   - Only the uniform Kogut–Susskind SU(2) model at fixed spacing and strong bare coupling (`g^4=9.6×10^9` at `|tau|=10^-8`), route B, the Haar reference, centered whole-star-plus-single-group boxes `N>=2`, the cover `R={0,e_z}` and the node `s=1`.
   - `tau<0` is the `U_E` mirror and has no real `g`.
   - Calculator values below the cap or at `tau=0` are corollaries, not AX2 admissions.
3. **Inherited without re-proof:**
   - the AV2 window lemma and constants (Fourier inversion, Fubini);
   - the AT4 relative-unitary Duhamel estimate and trace duality;
   - AX1's route-B constants: `J_0'`, gap, reset, incidence, `D'` and its passage to every AQ1 limit, and the flip identity;
   - AQ1's construction, nonnegativity and norm dynamics;
   - the AL1/I1 dictionary.
4. **Upper certificate only.** `r` bounds `|C(1)-d|`, and the free value is inside (`reference_unresolved`). There is no interaction shift, sign or coefficient; no uniform `K_2`, `omega(W^2)` constant or Wilson-mean sign rider.
5. **State scope.** Each AQ1 subsequential state holds separately. There is no uniqueness, whole-sequence convergence or rate in `N`.
6. **Crossover.** `s*≈5.98201228416` is a crossover of the linear formula only. There is no grid and no other node.
7. **Retained failures remain failures** at this `tau` and `s`: the Poisson certificates and the tier-(i) window.
8. **Read isolation.** Verified for repository inputs only. Scratch and shared-filesystem reads cannot be determined.
9. **Wording.** No weak-coupling or continuum statement follows.
10. **Priority.** Scientific priority is unverified.
