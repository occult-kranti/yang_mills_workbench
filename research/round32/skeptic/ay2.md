# AY2 skeptical review (post-comparison, statement loop, single producer)

**Verdict: accepted_within_scope.** The primary sub-label is `uniform_local_closeness_not_uniqueness`, and `static_not_dynamic` is a secondary label because the certified tier is static. The single forward producer carries out contract items 1–6. Every one of its constants and certificates agrees with my frozen pre-comparison package to the rational, or within the stated `sqrt(10)` bracket difference. There are **no blocking issues**.

**Admission basis.** AY2 has one producer (`producers=["forward"]`, `direction: statement+skeptic`, `single_direction_independent_replay: true`). Admission rests on that producer plus my pre-comparison derivation and replay. I wrote that package from the contract and froze it without opening any file under `forward/ay2/`. The `-tau` values replay the same `|tau|` formula; they are not a second confirmation.

**Standing.** I am a model-agent skeptic with correlated ancestry: I share a model family with the advisor and the producer. My own earlier work is part of the AY2 premises:
- my AY1 review is a shared premise, and its "Advice for AY2" lists the obligations;
- my AY1 pre-comparison package first printed the two-sided tier;
- the AY1 gate records that tier as an observation.

The agreement below is therefore a replay of admitted constants and a re-derivation of standard mathematics. It is not independent discovery, human peer review or formal verification. Human project author: Hruday N M (BUNZEEY).

**My pre-comparison package is unchanged.** It consists of:
- `ay2-contract-review.md`;
- `ay2-independent-derivation.md`;
- `ay2_check.py` (82 checks, 29 controls, 88 rejected mutations);
- `ay2-independent/results.json` (sha256 `2d7d3886…5d83a`).

Its hashes match `ay2-independent-freeze.json` (sha256 `7a22def1…e1c7`). A fresh replay under normal and `-O` Python reproduces its `results.json` byte for byte.

**Commit order.** The package was committed as `f640111` at 03:40:16Z, **after** the forward commit `ce6bca8` at 03:39:41Z, which is the reverse of AX2. Both packages were developed at the same time after the contract froze (03:09:12Z):
- my checker, predictions and exact values were final at 03:34:06Z, in a private replay whose results sha256 is `fe7ed26c…`;
- the forward `check.py` was last written at 03:38:22Z and its report at 03:38:56Z;
- my later edits, at 03:39:05Z and 03:39:43Z, only extended the disclosure after `git status` showed the producer's file names. The frozen results differ from the 03:34:06Z results only in `checker_sha256` and `incidental_exposure`.

Isolation therefore rests on disclosure, exposure to names only, and content, not on commit order.

**This review adds:**
- `ay2_postreview_check.py`. It has 27 exact checks and runs 46 source-mutation runs:
  - 1 unmutated copy;
  - 42 must-abort edits, all aborting with the intended message, 21 of which weaken one contract control each;
  - 3 silent edits, all accounted for.

  Its own validator also rejects 14 damaged packets.
- `ay2-postreview/results.json`, byte-identical under normal and `-O` Python.
- `ay2-replays.json`.

## What is admitted, with quantifiers

**Model.** `AQ_patterned_zero_selected`:
- SU(2) Kogut–Susskind form on Z³ at fixed spacing, with 24-link factors;
- selected triple exactly `(0,0,0)`, with Haar reference `P_R`;
- 21 omitted faces per anchor, each entering as `−(tau/3)W_f`;
- both signs, `|tau|<=10^-8`;
- cover `R={0,e_z}`: 48 links, 36 endpoints, 7 incident anchors;
- observable class `B(H_R)`;
- the two named families on centered `Lambda_N=[-N,N]^3` with `N>=2`: F1 (AQ1 whole-star boxes) and F2 (I1 §6 all-contained-face boxes with padding);
- clock `s=alpha t_E/hbar`, `theta=alpha t/hbar`.

**1. The statement (item 1).** For every pair of subsequential limits of F1 and F2 at the same coupling, on the fixed cover R and for the frozen observable class:
- `||rho_R−rho'_R||_1 <= 2D = 1170159676931825184288274812132100/42981220507576537932303142777593983768257` (about 2.72249057405e-8);
- after the common first-order density `rho^(1)_R=(tau/72)Σ_{f∈F_R}(|W_fΩ_R⟩⟨Ω_R|+h.c.)` is subtracted, `||rho_R−rho'_R||_1 <= 2K_2'tau^2` (about 2.68350550879e-12);
- `K_2' = 966771578474926086618624139557778885954947547760216752246561/72052885697817210754545804931891200000000000000000000000` (about 13417.5275440).

Each statement holds for a chosen subsequential limit of either family, every one separately. It does not assert equality of the states, whole-sequence convergence, translation invariance, boundary independence of the dynamics, or a rate in N.

**2. The certified tier (item 4), label `first_order_distance_from_product`.** For every subsequential limit of either family, at either sign and every `|tau|<=10^-8`:

`sqrt(10)|tau|/72 − K_2'tau^2 <= ||rho_R−P_R||_1 <= sqrt(10)|tau|/72 + K_2'tau^2`.

At the cap this is `[4.37863477824e-10, 4.40546983333e-10]`. It is a static property of the state on R:
- no interaction shift, Euclidean node or dynamical reading;
- the lower end is positive, so no limit has the Haar product as its R-marginal;
- it does not identify the limit.

**3. Obligations (item 2).** All six are **unproved**: uniqueness, whole-sequence convergence, translation invariance, a rate in N, boundary independence of dynamics on compact time windows, and dynamics of the padded family.

**4. Falsifying scenario (item 3).** Two limits may differ on R by up to `2K_2'tau^2`, and without bound off R. `2D` alone is not a boundary comparison.

**5. `K_2'` against `K_2^+` (item 5).** `K_2'` bounds the trace norm over all of `B(H_R)`. It is about 3.99950 times `K_2^+`, which bounds W alone and is uniform in N.

## Exact comparison (own code; nothing imported from the producer)

| quantity | producer | skeptic pre-comparison | own post-review re-derivation | status |
|---|---|---|---|---|
| `D`, `2D`, `K_2'`, `K_2'tau^2`, `2K_2'tau^2`, `K_2^+` | read from the gate and recomputed from its item formula | same rationals | tier-(ii) items recomputed (`pm.k2_prime`, `pm.d_forward`, `pm.k2_plus_formula`) | **equal** to the AY1 gate rationals in all three |
| `rho^(1)_R` | rank two, `c^2=10/144^2`, trace norm `sqrt(10)|tau|/72`, `Tr(rho^(1)W)=+tau/144` | Gram matrix of `{Ω_R, 2W_fΩ_R}` = identity by explicit Haar integration; characteristic polynomial `λ^9(λ^2−10/20736)` | Gram matrix re-integrated | **equal** |
| `sqrt(10)` bracket | `[197642353760523708249930846527/62500000000000000000000000000, 3162277660168379331998893544433/10^30]` (width `10^-30`) | width `10^-40`, nested inside the producer's | both directed (`lo^2<10<hi^2`) | nested |
| tier lower end | `315493271189404369878663368737136921794795815043212654249128159/720528856978172107545458049318912000000000000000000000000000000000000000` | `123239559058361081983852878412972198415914793719936897926499081872887/281456584757098479509944550515200000000000000000000000000000000000000000000000` | both equal `lo·|tau|/72−K_2'tau^2` exactly | producer ≤ skeptic, difference ≈9.98e-41 ≤ `10^-30|tau|/72` |
| tier upper end | `317426814346354222051900617016352553019063789598114401371582241/720528856978172107545458049318912000000000000000000000000000000000000000` | `619974246770223089945118392610008565852855028054286523715368951086693/1407282923785492397549722752576000000000000000000000000000000000000000000000000` | both equal `hi·|tau|/72+K_2'tau^2` exactly | skeptic ≤ producer, within `10^-30|tau|/72` |
| directedness | `(L+K_2'tau^2)^2 <= 10tau^2/5184 <= (U−K_2'tau^2)^2` | same | checked exactly for both | both valid; both inside the AY1 gate observation `[4.3786e-10, 4.4055e-10]`; producer ends within `10^-22` of the AY1-review exact ends |
| relative width | `(U−L)/(lo|tau|/72)` = `966771578474926086618624139607815612133987277450873561227041/158230021383939647982640996438347350340375381295486435500687360` ≈ 6.10991245541e-3 | `144K_2'|tau|/sqrt(10)`, directed, ≈ 6.1099124554e-3 | producer value ≥ ideal (checked by squares), exceeds mine by < `10^-28` | ≤ `1/100`, margin 1.6366846 |
| `±tau` separation | `2L` = `lo|tau|/36−2K_2'tau^2` ≈ 8.75726955649e-10 | `2L_s`, ≥ producer | `(sep+2K_2'tau^2)^2 <= 40tau^2/5184` | ≥ 8.7572e-10, a valid lower bound; each limit lies within D of `P_R` |
| falsifying witness | `psi_± = Ω_R + (tau/144)v ± nu w'`, `v=Σe_f`, `w'=e_{yz0}−e_{yz1}+e_{yz2}−e_{yz3}`, `nu = K_2'tau^2(1−10^-6)/4`; separation ≥ `(1−2·10^-6)2K_2'tau^2` | my own fixture (`χ_1` direction), 0.99999992 of `2K_2'tau^2` | producer witness rebuilt by explicit Haar integration: decomposition of `n^2(rho−P_R−rho^(1))` exact; ball bound 1.34175150939e-12 ≤ `K_2'tau^2`; within D; `omega(W)−tau/144` ≈ −3.349e-30; reset energy `24(n^2−1)/n^2` ≈ 1.16e-18 ≤ `98|tau|`; norm-one test operator `(|w'⟩⟨Ω|+h.c.)/2` gives `||rho_+−rho_−||_1 >= 8nu/n^2` ≈ 0.999999 `2K_2'tau^2` | **confirmed**; the exported `(1−2·10^-6)2K_2'tau^2` equals the claim exactly |

**Report decimals.** The eleven report previews I checked are all truncations of the exact values to their last digit: the tier ends, relative width, separation, falsifier, `K_2'`, `K_2'tau^2`, `2K_2'tau^2`, `D`, `2D` and `K_2^+`.

## The trace norm of rho^(1)_R, and a correction to my own wording

Both routes give exactly `sqrt(10)|tau|/72`. The producer uses the rank-two cube identity. I used the explicit Haar Gram matrix and the characteristic polynomial.

**What the pieces look like.** Each of the ten pieces `(tau/72)(|W_fΩ_R⟩⟨Ω_R|+h.c.)` is a rank-one operator plus its adjoint, so it is **rank two**, with eigenvalues `±|tau|/144`. Because all ten share `Ω_R`, their sum is again rank two, with eigenvalues `±sqrt(10)tau/144`.

**Corrections.**
- The producer's R1 corrects a relayed instruction that said "rank-one pieces … eigenvalues ±sqrt(10)tau/72".
- The same correction applies to my pre-comparison wording: the derivation §2 and a checker note say "ten rank-one pieces". The per-piece trace norm `|tau|/72`, the triangle value `5|tau|/36` and every value I derived are unaffected.
- My frozen files stay as they are; this review records the correction (S1).

## Which values the gate should bind

**Bind the producer's exact rationals.**
- tier `[L, U]` as above, with its `sqrt(10)` bracket at `10^-30`;
- relative width `966771578474926086618624139607815612133987277450873561227041/158230021383939647982640996438347350340375381295486435500687360`, target `1/100` met;
- `±tau` separation `315493271189404369878663368737136921794795815043212654249128159/360264428489086053772729024659456000000000000000000000000000000000000000`;
- falsifier separation `483384822465884568383225451154749885198587818932560615906528253439/180132214244543026886364512329728000000000000000000000000000000000000000000000`;
- the AY1 constants unchanged.

**Why the producer's values:**
- They are the frozen certificate under the AY2 contract.
- They are directed and valid.
- They agree with my previews to 12 digits.

**Record mine as the tighter independent enclosure** (`10^-40` bracket). It is nested inside the producer's, and the ends differ by at most `10^-30|tau|/72` ≈ 1.4e-40.

## Obligations: assessment

All six rows are present:
- the names follow contract item 2 in order;
- every row has status `unproved` and states its missing premise, a candidate route and the constants to evaluate;
- no row claims to be closed.

I agree with each row. They map onto my own table as follows:

| producer | my row | agreement |
|---|---|---|
| O1 uniqueness | uniqueness | Agreed. HTW constants are unevaluated (AM2 gate), the Yarotsky `c_1(S), c_2(S)` are existential, and a Dobrushin-type condition is not formulated for this model. My extra candidates are a complex-τ analyticity route (the AM2 inequalities hold for real `|tau|<1/37888`) and a quasi-adiabatic route using the AM2 gap 1/2. Both are candidates only |
| O2 whole-sequence convergence | same | Agreed. Its "boundary-influence refinement of the AM2 fixed point" and its note that `2J_0G'(R)` is a global Lipschitz bound with no decay in distance match my reading. Within-family uniqueness plus AQ1 compactness would also give whole-sequence convergence, without a rate |
| O3 translation invariance | same | Agreed. The model is only coarse-translation covariant, and translated boxes form a different sequence |
| O4 rate in N | same | Agreed |
| O5 boundary independence of dynamics | same | Agreed in substance. **The dynamics row is where my reading differs.** The route text repeats the contract's "with the AM2 constants", but the constants the producer lists are the **AQ1** Nachtergaele–Sims constants: `F(r)=(1+r)^-4`, `C<=224`, `||Phi||_F<=81J<=2268|tau|`, plus `||Phi'||_F<=1323|tau|` from the AY1 reverse. The per-site sum `J<=28|tau|` is common to AM2 and AQ1. The Lieb–Robinson constants are therefore AQ1's; AM2 supplies the gap and the fixed point, which an algebraic-dynamics comparison does not use. Every constant this row needs is available, and the Duhamel comparison over the `28N(5N+1)` boundary faces at distance `N−1` is unwritten. GNS-level dynamics would also need O1. The gate should name AQ1 |
| O6 padded-family dynamics | same | Agreed. The route is Nachtergaele–Sims with the owner-set interaction, followed by AQ1 §4–5. All constants are available and the proof is unwritten |

## Review against the contract items

1. **Complete.**
   - The constants are read from the gate text and recomputed; the pins 82/72/33/10 come from the I1 table.
   - The phrase "a chosen subsequential" is present, and the forbidden-phrase scan finds nothing (see the table after this list).
   - **Sentence form.** The mandatory sentence is the **Jung loop-2 form**: the AY1 forward §6 sentence, whose fixed text is identical in the AY1 reverse, filled with the exact `2D` and `2K_2'tau^2`. It does not quote the AY1-contract template that the AY1 gate carries verbatim.

   | Form | Wording on boundary independence |
   |---|---|
   | AY1-contract template | "boundary independence of the dynamics" |
   | Jung form (used) | "boundary independence beyond R" |

   The producer covers dynamics separately, in §1.5 and in the gate fields. This is finding N2 below.
2. **Complete.** See "Obligations: assessment" above.
3. **Complete.**
   - The witness satisfies every one-state constraint, and its separation is certified.
   - `2D` is shown to hold across opposite couplings, and "each within D" is stated (the producer's D4).
   - The producer's constraint list is more complete than my pre-comparison list: it adds the reset energy `omega(h_R)<=98|tau|`. My own fixture satisfies it retroactively (1.16e-18).
4. **Complete.**
   - The tier is certified with a directed `10^-30` bracket.
   - Its label and static reading are stated, and the lower end's consequence is stated without identifying the limit.
   - Monotonicity gives every `|tau|<=10^-8`, and `-tau` is a replay.
   - The single-state remainder is justified from the AY1 gate `accepted` statement with F11, F13, F14 and the AV1 cutoff removal F22 (my contract-review reading 2). The pair constant and a halved remainder are both rejected.
5. **Complete.**
   - The producer's duality formulation is sharper than mine and correct. Every valid trace-norm constant is also a valid W constant, so a trace-norm constant can never beat the best W constant.
   - Separately, every constant assembled from the AW1 items is at least `2rho/tau^2`, about 6708.2, which exceeds `K_2^+`.
   - The variants are given as previews only. The AY1 wording is corrected: `K_2^+` is uniform in N and specific to W.
6. **Complete.**
   - The six claim fields are false. `states_compared`, `region`, `topology` and `closeness_order` `[1,2]` are exported.
   - The flags `continuum_claim`, `uniform_wilson_claim`, `resolved_interaction_shift`, `scientific_priority_verified` and `weak_coupling_claim` are false.
   - All 21 controls are damaging mutations: 85 rejections inside the control checks and 114 in total, over 42 checks, with nothing deferred.
   - The `-B` and `-B -O` outputs are byte-identical.

**Forbidden-phrase scan of `report.md`.** With code spans removed:
- no line contains "the thermodynamic limit", "the limit state", "converges as N" or "uniform in a";
- "the AQ state" occurs only in the negated verbatim exclusion;
- every line with "uniq" contains "not".

## Contract defects and readings, reconciled

The producer's D1–D6 are all verified against the frozen text.

| producer | my contract-review reading | outcome |
|---|---|---|
| D1 `selected_after` placeholder | 4 | same finding |
| D2 "uniqueness of the AQ state" in the preregistration exclusions | 12 | same; quoted only in negated code spans |
| D3 `rate_in_N_claimed` missing from `gate_fields_required` | 12 | same; both rate fields exported false |
| D4 "within 2D of the product" | 8 | same: **each limit lies within D of `P_R`**, so any two lie within 2D of each other; 8.7e-10 is the preview of `sqrt(10)|tau|/36−2K_2'tau^2` ≈ 8.757e-10 |
| D5 "not the whole-box `K_2^+`" | 10 | same; `K_2^+` is uniform in N and specific to W, and `K_2'` is larger |
| D6 `selection_reason` "certified two-sided distance" anticipates AY2 | — | new and valid; the AY1 gate recorded the distance as an observation only |
| R1 relayed "rank-one … `±sqrt(10)tau/72`" | — | valid; it also corrects my own "rank-one pieces" wording (S1) |

**How my other readings came out:**
- **1, target:** met with margin 1.6367, by construction. Both relative-width definitions are upper bounds.
- **2, single-state item:** cited as I read it.
- **3, τ convention:** τ is inside `rho^(1)_R = tau·rho_hat`, with no double counting.
- **5, template:** not in the AY2 preregistration; the producer used the Jung form (N2).
- **6, Lieb–Robinson constants:** the AQ1 constants are named in O5's constants column (N3).
- **7, HTW and Dobrushin:** as in O1.
- **9, error-term wording:** the producer's ledger and constants table say "single state against `P_R+rho^(1)_R`".
- **11, premises not snapshotted:** everything was read from the gate text.
- **13, labels:** as recommended.
- **14, scope in τ:** by monotonicity.
- **15, independence:** disclosed.

## Replays, closure and isolation

**The existing replay tools do not apply unchanged.** `replay_loop.py ay2` replays the forward package under normal and `-O` Python without a mismatch, then stops on the absent `reverse/ay2/freeze.json`: it always replays two directions. `replay_declared.py ay2` refuses, because it accepts a single producer only with direction `single+skeptic`. Both tools are bound by earlier reviews and gates, so neither was edited.

**What I ran instead.** The same steps run in `ay2_postreview_check.py` with the unchanged `replay_loop.verify_freeze`:
- the closure is verified file by file: 27 listed files plus `freeze.json` (sha256 `f2fccf3a…8eac`);
- the inputs are exactly AGENTS.md, the contract and the 21 shared premises (23 files), each byte-identical to its repository source;
- the only skeptic inputs are the declared shared premises `round32/skeptic/ay1.md` and `round29/skeptic/am2.md`, and there is no `skeptic/ay2*` input;
- no `reverse/ay2` package exists;
- `check.py` replayed under normal and `-O` Python into fresh external directories reproduces `output/` byte for byte (`results.json` `a2d55af6…3ec5`, `source-manifest.json` `a5b12868…e80f`);
- `tools/freeze.py verify` reports `verified`;
- the `check.py` sha256 recorded before evaluation equals the frozen file.

**Disclosed reads.** The producer declares reads outside `inputs/` for protocol and style only:
- the tools README and `freeze.py`;
- parts of `forward/ay1/check.py`;
- the first 60 lines of `forward/ax2/report.md`;
- file names and line counts.

It declares no read under `skeptic/` except the snapshotted `ay1.md`. Its private scratch (`/tmp/claude-0/ay2-forward-private`, checked by name and time only) matches its disclosure. `scan.py` is not named individually but falls under its development scripts.

**Shared scratchpad root.** After the AY2 freeze it holds only manuscript files, checked by name only.

## Source-edit receipts

Each edit is applied to a temporary copy of the closure outside the checkout. The unmutated copy reproduces `results.json` and `source-manifest.json` byte for byte.

**Must abort: 42 of 42 aborted with the intended message.**
- **Control weakenings (21, one per contract control).** Each weakens the validator of one control, and each run aborts with "damaging mutation accepted: <label>". The controls, with the mutation that got through:

  | Control | Mutation accepted |
  |---|---|
  | `missing_incoming_stars` | outgoing stars only, 42 faces |
  | `full_original_wilson_cover` | `{0}` cover |
  | `wrong_delta_alpha_hbar_clock` | `tau/576` |
  | `vector_versus_scalar_centering` | vector centering |
  | `first_order_mean_charged` | density set to zero |
  | `tau_scaling_exponent` | first order labelled second order |
  | `changed_model_relabelled` | tau above the cap |
  | `coherent_evidence_tampering` | flipped Boolean with the hash rebound |
  | `insufficient_verdict_retained` | missing row relabelled accepted |
  | `exact_arithmetic_admission` | float `sqrt(10)` input |
  | `root_n_misuse` | `sqrt(10)` read as root-N |
  | `no_priority_or_continuum_claim` | `continuum_claim` true |
  | `topology_named` | weak-* for states |
  | `two_families_named` | one family |
  | `subsequence_versus_whole_sequence` | whole sequence inferred |
  | `local_closeness_not_uniqueness` | equality from closeness |
  | `common_clock` | opposite signs |
  | `tier_mixing_rejected` | `K_2^+` as the trace-norm remainder |
  | `not_uniform_in_a` | uniform in a |
  | `lower_bound_is_static_not_dynamic` | tier relabelled dynamical |
  | `obligations_table_complete` | padded-family row removed |

- **Value edits (9):**
  - half remainder at the lower end;
  - `sqrt(10)` upper bracket used at the lower end;
  - AM2 item halved;
  - witness `nu` doubled;
  - parity rule disabled;
  - coefficient `1/144`;
  - `continuum_claim` true;
  - `uniqueness_claimed` true;
  - separation computed with the `sqrt(10)` upper bracket.
- **Input edits (5):**
  - contract byte edit without rehash;
  - contract target `1/1000` with rehash, which aborts because `check.py` requires the preregistered `1/100`;
  - AY1 gate `K_2'` digit edited, which aborts at `ay1_gate_constants_parsed_exact`;
  - an undeclared `skeptic/ay2` input;
  - a premise snapshot removed.
- **Report edits (7):**
  - O1 marked proved;
  - O6 row removed;
  - sentence negation removed;
  - "The AQ state" appended;
  - "unique" without "not" appended;
  - a control row removed from the §6.7 map;
  - the exact tier lower end removed.

**Silent: 3, all accounted for.**
1. An edit to an unparsed field of the AY1 gate snapshot runs to completion. `check.py` records the gate hash but does not pin it, which the contract does not require. The snapshot-versus-source comparison in `replay_loop.verify_freeze` catches it, and so does this review's validator, which pins the gate sha256 (N4).
2. W moved to another face of `F_R` does not change the output. `Tr(rho^(1)_R W_g)=+tau/144` for every `g∈F_R`, so the Wilson readout cannot tell which face is W. My own pre-comparison harness found the same.
3. Removing the witness's reset-energy test does not change the output. The constraint holds with a margin of about `10^12`, and I rebuilt the witness and re-checked it.

A source edit always changes the recorded `check.py` sha256, which `freeze.json` and the source manifest bind.

**Own validator.** It accepts the frozen packet and rejects 14 damaged packets:
- a tier end moved;
- `K_2'` quartered;
- the bracket swapped;
- the relative width halved;
- the separation doubled;
- the falsifier set beyond `2K_2'tau^2`;
- an obligation row dropped;
- `uniqueness_claimed`, `rate_in_N_claimed` or `resolved_interaction_shift` set true;
- `closeness_order` `[1]`;
- the tier relabelled dynamical;
- the gate hash changed.

## Blocking issues

None.

## Non-blocking findings

- **N1. Isolation and independence.** The two packages were developed at the same time, and my commit follows the producer's (see the commit-order paragraph above). My exact values were fixed before the producer's final `check.py` and report were written. Neither side opened the other's files. Independence is limited to route and code:
  - the contract, the selection note, the AY1 gate and my `ay1.md` state every headline value;
  - the producer's single-state remainder and my own are the same AY1 item.
- **N2. Mandatory sentence form.** The AY2 preregistration has no template (my reading 5). The producer filled the Jung loop-2 form; the AY1-contract template, which the AY1 gate quotes, is not repeated in the report. Both forms are admitted in AY1. The gate should carry the AY1-gate template with the constants filled (as in the supported statement) and may add the Jung form.
- **N3. The dynamics row.** "With the AM2 constants" is the contract's wording. The constants the row lists are AQ1's Nachtergaele–Sims constants. The gate should name AQ1 (my reading 6).
- **N4. The AY1 gate hash is not pinned in `check.py`.** An unparsed-field edit runs to completion. Numeric gate edits abort through recomputation, and freeze and snapshot verification catch the rest.
- **N5. Readout-blind and margin-guarded edits run silently by design** (W within `F_R`; the energy test), as accounted above.
- **N6. Self-correction S1.** "Ten rank-one pieces" in my pre-comparison derivation §2 and checker note should read "rank-two pieces (a rank-one operator plus its adjoint)". No value changes.
- **N7. Self-correction on scope.** My pre-comparison list of admitted one-state constraints left out the reset energy `omega(h_R)<=98|tau|`. My fixture satisfies it (1.16e-18), and the producer's list includes it.
- **N8. Relative-width definitions differ but agree.**

  | Definition | Value |
  |---|---|
  | producer: `(U−L)/(lo|tau|/72)`, including the bracket slack | 6.10991245541e-3 |
  | mine: `144K_2'|tau|/sqrt(10)`, directed | 6.1099124554e-3 |

  Both are upper bounds and meet `1/100` with margin 1.6367. The target is met by construction.
- **N9. Replay tools.** `replay_loop.py` and `replay_declared.py` do not accept a `statement+skeptic` contract. For future statement loops, a new wrapper, not an edit of the bound tools, would remove the need for the in-checker replay used here.

## Limitations

1. **Model scope.**
   - Covered: only the zero-selected patterned family, the cover R, fixed spacing and `|tau|<=10^-8`, with the two named families on centered cubes `N>=2`.
   - Not covered: literal vertex boxes, periodic or orthant boxes, nonzero selected triples, the uniform route-B model, weak coupling or the continuum.
   - Every constant is uniform in N at fixed spacing, never in a.
2. **Local closeness only.**
   - The result is uniform local closeness on R at the same coupling and a static two-sided distance tier.
   - It says nothing about uniqueness, whole-sequence convergence, translation invariance, a rate in N, boundary independence of the dynamics, or dynamics of the padded family. All six are unproved.
   - Two limits may differ by up to `2K_2'tau^2` on R, and without bound elsewhere.
3. **The tier is static.** It is not an interaction shift, a Euclidean node or a dynamical statement. Its lower end excludes the Haar product on R but does not identify the limit. It is the AY1 observation, now certified under the AY2 contract; it is not a new mathematical result.
4. **The falsifying witness** is a pair of density matrices on `H_R`. It shows what the admitted bounds leave open; it is not a constructed limit (`transfers_to_aq: false`).
5. **Inherited without re-proof:**
   - AM2 majorant, fixed point, exclusion and cutoff passage;
   - AV1 split and cutoff-vector removal (F22);
   - AY1 F13/F14 and the passage to every limit;
   - AQ1 compactness and extraction;
   - the I1 dictionary.

   Nachtergaele–Sims, the Yarotsky theorem, HTW and Dobrushin-type conditions are named as candidate routes only.
6. **Constants are upper bounds**, except the certified lower end. `K_2'` is 99.99% the generic AM2 majorant.
7. **Single producer and correlated agents.** Isolation is shown by disclosure, exposure to names only, and content. Commit order does not show it: the skeptic commit follows the producer commit.
8. **Priority.** Scientific priority is unverified.
