# AW2 skeptical review (post-comparison, single direction)

**Verdict: accepted_within_scope, sub-label `static_not_dynamic`.** The forward producer and my frozen pre-comparison replay agree exactly on every value:

- `tau_AW2=10^-8`, which the frozen AW1 decade-grid rule returns from the gate-bound `K_2^+`. No literal coupling is used, and `10^-8` is the cap.
- The enclosure at `tau=+10^-8` has endpoints `42773581813770903096597852821080380528959/D` and `43188859201382168785822623711271900423873/D`, with `D=618929575309102117553427431032936422860390400000000`. Widened outward, this is `[6.91089641214e-11, 6.97799247674e-11]`.
- The enclosure at `tau=-10^-8` is its mirror.
- The exclusion margin is about 206.00005.
- The sign margin is about 207.00005.

Zero is strictly excluded at both signs. The contract target `m>=2` is met. The crude tier contains 0 at the cap and is kept as a recorded failure. There are **no blocking issues**.

**Admission basis.** AW2 has a single producer (`producers=["forward"]`, `direction: single+skeptic`). Admission therefore rests on two things: the forward producer, and my independent replay from the contract, which was written and frozen before I opened the producer. The `-tau` enclosure is a replay of the flip lemma. It is not a second confirmation.

**Standing.** I am a model-agent skeptic with correlated ancestry. I share a model family with the advisor and the producer, and the bound `K_2^+` is my own AW1 itemization. So the exact agreement below shows that one admitted formula was replayed correctly. It is not independent physical confirmation, human peer review or formal verification. Human project author: Hruday N M (BUNZEEY).

**My pre-comparison package is unchanged.** It consists of:
- `aw2-independent-derivation.md`;
- `aw2_check.py` (75 checks, all 23 controls);
- `aw2-contract-review.md`;
- `aw2-independent/results.json` (sha256 `ecff2cfc…4e6f`).

Its hashes still match `aw2-independent-freeze.json`. A fresh replay under normal and `-O` Python reproduces its `results.json` byte for byte. It was committed (`86edd4d`, 00:17:03Z) before the forward commit (`4ef9352`, 00:23:47Z).

**This review adds:**
- `aw2_postreview_check.py`: 73 exact checks, including 33 must-abort source edits, one silent edit that the static review catches, and two preview demonstrations;
- `aw2-postreview/results.json`: byte-identical under normal and `-O`, sha256 `27fa8ac6…c34f`;
- `aw2-replays.json`;
- `replay_declared.py`, a wrapper that imports `replay_loop.py` unchanged (see Replays).

## What is certified, with quantifiers

**Model.** The AM2/AQ1 zero-selected patterned family:
- SU(2) Kogut–Susskind form on Z^3 at fixed spacing, with coarse 24-link factors;
- selected triple exactly `(0,0,0)`, so the reference is the Haar product;
- whole stars `phi_b=-(tau/3) sum W_f` under I1.5 in `delta=alpha/8` units, with `V_b=phi_b/8` in alpha units;
- the original xz Wilson loop `W` with complete cover `R={0,e_z}`;
- fixed positive `alpha`, `hbar`, `E_star` and spacing.

**State.** The claim covers every state in the **whole set** `S(tau)` of AQ1 subsequential limits at `tau=+10^-8`. It also covers every centered whole-star box `N>=2` at every on-site cutoff. The bound is uniform in the box. It passes to the limits by local trace-norm convergence on `R`:

`|omega(W)-omega_{N_k}(W)|<=||W|| ||rho_R-rho_{N_k,R}||_1`, with `||W||<=1`, and the interval is closed.

**Statement.** The static equal-time Wilson mean satisfies

`omega_tau(W) in [tau/144-K_2^+tau^2, tau/144+K_2^+tau^2]`, with `K_2^+=81108864767825329926713064490531229475390625/24176936535511801466930759024724079017984` (≈3354.80322946).

**Mirror at `tau=-10^-8`.** The enclosure is the mirror image. This follows directly from gate item (4), which holds at both signs. It is also the image under the flip lemma at the zero triple, `S(-tau)=S(tau)∘alpha_E` as whole sets. It is a replay.

**Sign.** Hence `sign(omega_tau(W))=sign(tau)`, and the free reference 0 is strictly excluded.

**What does not follow.**
- No dynamical correction, mass shift, mass gap or susceptibility.
- No shift of the centered correlation `C(s)` or `c(theta)`: AV2's `reference_unresolved` stands.
- No uniqueness, whole-sequence convergence or rate in `N`.
- No third-order remainder.
- Nothing at nonzero triples, and no uniform Wilson, weak-coupling, continuum or priority statement.
- `sign_certified_below_cap` does not apply, because `tau_AW2` is the cap.

## Exact numbers re-derived (my own Fraction code)

**`K_2^+`.**
- My own regexes parse the AW1 gate `decision` and `accepted` texts. Both give the same rational, and it equals the contract `K_2_plus` string.
- The ceiling `3354803229461691/10^12` is exactly the `10^-12` ceiling of that value.
- **Itemization replay.** `J=28|tau|` (4 stars × 21 anchored faces × 1/3), `T=(49|tau|/144)/(1-352J)`, `rho=352JT`, `eps=2T+T^2`. Then `K_2^+tau^2 = rho + T·T + T^2 + eps^2 + (|tau|/144)eps^2` reproduces the gate value exactly. The counts 49 and 21 come from my frozen I1.4 enumeration.
- The AM2 term is 99.979% of the total.
- The same `T` reproduces the AV1 `D_ii` exactly.

**First-order sign chain.**
- `V=-(tau/24)W_f` per face (alpha units).
- `W_f Omega_0` has energy `4·3/4=3`.
- `c^(1)=-(tau/72)W_f Omega_0`.
- `omega=-2Re<W Omega_0,c^(1)>=(tau/36)E[W^2]=+tau/144`, with `E[W^2]=1/4` from the Clebsch–Gordan count. The Haar moments `E[W^n]`, n=1..8, are `0,1/4,0,1/8,0,5/64,0,7/128`.
- The AW1 contract's literal display `2<W Omega_0,c^(1)>` gives `-1/144`. It is not used.

**Rule.**
- Parsed from `contracts/aw1.json`: grid `{10^-8,10^-9,…}`, threshold `1/288`. The threshold equals half of my derived `1/144`, and the grid starts at the AW1 `tau_cap`.
- At `10^-8`: `K_2^+·10^-8 = 207638693805632844612385445095759947457/6189295753091021175534274310329364228603904`, which is at most `1/288`. The slack is `21282971559982635125992733687992310290751/6189295753091021175534274310329364228603904`, a ratio of about 103.50003.
- So `tau_AW2=10^-8`.
- The rule actually evaluates `K`: `1000 K_2^+` gives `10^-9`, and the crude `K_2` gives `10^-10`. The crude result is information only.

**Enclosure, margins and floors.** These are the stated rationals exactly, with `D` as above.

| quantity | exact | directed decimal |
|---|---|---|
| lower, `+10^-8` | `42773581813770903096597852821080380528959/D` | `6.91089641214e-11` (down) |
| upper, `+10^-8` | `43188859201382168785822623711271900423873/D` | `6.97799247674e-11` (up) |
| lower, `-10^-8` | `-43188859201382168785822623711271900423873/D` | `-6.97799247674e-11` (down) |
| upper, `-10^-8` | `-42773581813770903096597852821080380528959/D` | `-6.91089641214e-11` (up) |
| exclusion margin `m=(|tau|/144-K tau^2)/(K tau^2)` | `42773581813770903096597852821080380528959/207638693805632844612385445095759947457` | `2.06000052445e2`; floor on the 10^-9 grid `41200010489/200000000` |
| sign margin `S=1/(144K|tau|)` | `42981220507576535941210238266176140476416/207638693805632844612385445095759947457` | `2.07000052445e2`; floor `41400010489/200000000` (= the gate's directed floor) |

**Margin relations.**
- `m=S-1` exactly. The lower endpoint equals `(1-1/S)` times the first-order value, about 99.52% of it.
- The rule `K|tau|<=1/288` guarantees only `S>=2`, i.e. `m>=1`. The target `m>=2` needs `S>=3`, i.e. `K|tau|<=1/432`, and both codes test it separately.
- At the rule boundary, `m` would equal exactly 1.

**Controls on the numbers.**
- **Outward ceiling.** With the ceiling in place of `K_2^+`, the enclosure widens by less than `10^-28` and still excludes 0 with `m>=2`.
- **AV1 containment.** `|endpoints| <= D_ii` (≈1.3612e-8), a ratio of about 195.08.
- **Scaling.** Under `tau -> tau/100`, the first-order term changes by exactly 100 and the remainder by exactly 10^4. The itemized constant at `10^-10` is below `K_2^+`.

**Crude tier (retained failure).**
- Replacing `T` by `t_c=592|tau|` gives `K_2=1937877026146766159414097129/244140625000000000000` (≈7.93754429909e6).
- At the cap, the enclosure is `[-15915014329070895434726874161, 18966772141570895434726874161]/21972656250000000000000000000000000000`, about `[-7.24309985466e-10, 8.63198874355e-10]`. It **contains 0**.
- Sign margin ≈0.0874886 (<1).
- The producer records the same exact rationals as a failed limited-tier control. It never substitutes the rule's `10^-10` for the crude tier.

## Comparison with the producer (every exported rational)

All of the following are equal, as exact rationals, to my re-derivation and to my pre-comparison `results.json`:
- `headline`: `K_2^+`, `tau_AW2`, both enclosures, both margins and target `2`;
- both `enclosures` records: `tau`, first-order value, radius, endpoints, `excludes_zero_strictly`, sign and margins;
- the rule arithmetic: `K_2^+tau`, slack, ratio 103.5 and the single step;
- the crude constant and its enclosure;
- the first-order values `±1/14400000000` and the one-plaquette series;
- the counts 49, 82, 10, 16 and 21 and the Haar moments. These agree with my pre-comparison I1.4 enumeration, which is an independent code.

**Decimals.**
- Every producer decimal (12 significant digits) parses exactly, lies on the outward side and is within one unit of its last digit. This covers the enclosures, the margins (rounded down) and `K_2^+` (rounded up).
- My 16-digit pre-comparison decimals nest inside the producer's decimals, and the exact endpoints lie inside mine.

**Only difference: display precision.** The producer uses 12 digits and I used 16. No admission Boolean reads a decimal.

## Review against the contract items

1. **Coupling from the hash-checked gate; literals rejected.**
   - `check.py` verifies the gate snapshot's hash (pin `647dc337…41ae`) and parses `K_2^+` from its decision text. It cross-checks that value against the accepted text, the contract, my AW1 review and the forward AW1 preview truncation. It then evaluates the rule, parsed from the gate-bound AW1 contract snapshot, inside `check.py`.
   - My static data-flow check confirms the whole chain:
     - `tau_aw2` is assigned exactly once, from `aw2_rule(K, R)`;
     - `K` comes from `G['K']`, and `G` from `parse_gate(read_input(AW1_GATE_REL))`, which hash-verifies the gate;
     - `aw2_rule` holds no literal beyond the grid mechanics;
     - the calculator likewise uses `coupling_rule(gate_constants())`.
   - The producer rejects seven non-rule couplings: a literal, the contract text, `10^-9`, an off-grid value, the forward headline constant, the crude constant, and a rule bound that is not half the coefficient.
   - A source edit to `10^-9` aborts.
2. **Enclosure and exclusion.** Exact, at both signs. `m≈206.00005>=2` and `S≈207.00005`. The mirror is labelled a replay. The producer's `minus_tau_status:"replay"` is enforced: an edit to "independent_confirmation" aborts.
3. **Scope.**
   - The producer's `scope` record states the whole set of AQ1 subsequential limits, `uniform_in_N`, local trace-norm passage and `static_not_dynamic`.
   - Uniqueness, rate in `N`, whole-sequence convergence and finite-graph transfer are all false.
   - The `-tau` pointwise pairing holds only along a common subsequence.
   - `sign_certified_below_cap:false`. The centered correlation is "unresolved (AV2 reference_unresolved)".
4. **Controls.** All 23 contract ids are present in the producer packet as damaging mutations, 92 rejections among them (116 over all 37 checks). This covers every sub-item of item 4:
   - **sign flip:** a sign-blind enclosure is rejected;
   - **wrong face:** another face with owner set `R`, all ten inside faces, and `W` excluded are all rejected;
   - **centring:** the 3×3 vector/scalar identities are checked, and the calculator has no `m_hat` argument;
   - **sign convention:** a flipped I1.5 string and a coherent flip in derivation and fixture are rejected, and the one-plaquette `j<=1/2` determinant sign is checked;
   - **boundary/state:** `N=2` and `N=3` give identical formula inputs, and `N=1` is rejected;
   - **arithmetic:** Fraction-only arithmetic, exponents 1 and 2, and a labelled preview;
   - **tier mixing:** the crude tier fails and is retained;
   - **coherent tampering:** ten rebound-hash mutations are rejected, including a removed snapshot and a rehashed contract or gate;
   - **reverse isolation:** stated as not applicable.

   I also ran source edits that weaken the producer's own validators: strict exclusion made non-strict, the incoming-star validator disabled, the below-cap label check disabled, and the claim-flag check disabled. Each makes a producer mutation get accepted, and the run aborts with "damaging mutation accepted". So the controls are live.
5. **Calculator and flags.**
   - **Domain.** The calculator is restricted to the zero triple and `0<|tau|<=10^-8`. `K_2^+` comes only from the gate: there is no `K` or `m_hat` argument (TypeError). Floats, Booleans, exponent text, `tau=0`, `|tau|>10^-8`, nonzero or float triples, the crude tier, non-positive scales and a non-Boolean or mismatched `fixed_design` all raise ValueError.
   - **Valid calls.** A tampered gate snapshot raises `CalculatorError`. Plain decimal text `0.00000001` gives the same exact enclosure, and physical scales `(5,7,11/2,3)` leave it unchanged.
   - **Claim flags.** `resolved_interaction_shift:true`, set only because the exclusion holds at the cap; `static_not_dynamic:true`. All of the following are false: `sign_certified_below_cap`, `dynamical_correction_claim`, `correlation_shift_resolved`, `continuum_claim`, `uniform_wilson_claim`, `scientific_priority_verified`, `mass_shift_claim`, `susceptibility_claim`, `uniqueness_claim`, `whole_sequence_convergence_claim`, `rate_in_N_claim` and `third_order_remainder_claim`.
   - **Replays.** Byte-identical under normal and `-O`, and frozen.
6. **Independent replay.** My package was frozen and committed before the forward commit, and it agrees exactly.

**Arb/mpmath preview.**
- `arb-preview.json` is labelled `PREVIEW ONLY`, `preview_only:true`, `used_for_admission:false` (python-flint 0.9.0 and mpmath 1.3.0, 256 bits).
- Regenerating it reproduces the stored file byte for byte, and every exact endpoint and margin lies inside both backends' bounds.
- Neither `check.py` nor `calculator.py` imports flint, mpmath or `arb_preview` (checked by AST import scan). Adding `import mpmath` to `check.py` aborts.
- I replaced every stored ball with the exact point value. The only field of `results.json` that changed was `preview_sha256`, so no admitted value, flag or verdict depends on the preview.

## Source-edit receipts

Each edit is applied to a temporary copy of the closure outside the checkout. An unmutated copy reproduces `output/results.json` and `source-manifest.json` byte for byte.

**Must abort (33 of 33 aborted).** The edits:
- first-order sign flipped;
- literal `10^-9` coupling;
- `K` halved after the gate read;
- radius halved;
- margin measured against the first-order term;
- sign-blind minus enclosure;
- crude tier reported as excluding 0;
- `sign_certified_below_cap`, `dynamical_correction_claim` or `correlation_shift_resolved` set true;
- `static_not_dynamic` set false;
- rule threshold set to the coefficient;
- grid start shifted;
- lower decimal rounded inward;
- mirror counted as independent;
- `mpmath` import added;
- four validator weakenings;
- three calculator domain widenings (float accepted, cap check removed, nonzero triple allowed);
- a gate `K` digit edited without rehash;
- gate `K` doubled with its hash rebound in both files;
- contract target raised to 300 with rehash;
- contract reference set to `1/144` with rehash;
- contract edited without rehash;
- the I1 `phi_b` sign flipped;
- an undeclared `skeptic/aw2` input added;
- a premise snapshot removed;
- the preview promoted to admission;
- a preview bound moved to exclude the exact endpoint.

**Reads-from-contract demonstration.** With the target raised to 300 and the pin rehashed, the producer fails exactly at `zero_exclusion_and_margins`. The target is therefore read from the contract snapshot. With the reference raised to `1/144`, it fails at the same check.

**Silent edit caught by review (1).** A literal coupling equal to the rule value (`tau_aw2 = Q(1, 10 ** 8)`) runs to completion. Only the recorded `check.py` sha256 changes. My data-flow validator rejects the mutated source.

## Replays, closures and isolation

**Replays.** `replay_declared.py aw2` produces the same output under normal and `-O` Python. For the forward closure it:
- verifies the closure (35 files);
- compares the 28 input snapshots with their repository sources byte for byte;
- replays `check.py` under normal and `-O` into fresh external directories. Both runs reproduce `output/` byte for byte: `results.json` `ec09f259…6abe0` and `source-manifest.json` `cd82ab33…a37a`;
- runs `tools/freeze.py verify research/round32/forward/aw2`, which reports `verified`.

**Why a wrapper.** `replay_loop.py` always replays forward and reverse, so it fails on AW2 (no `reverse/aw2/freeze.json`). It is not edited, because its sha256 `e627df04…ed66` is recorded in the AV1, AV2 and AW1 skeptic bindings. `replay_declared.py` imports it unchanged and replays only the directions the contract declares. It refuses an undeclared direction package, and it reproduces all four AW1 replays.

**Inputs.** The inputs equal `AGENTS.md`, `contracts/aw2.json` and the 26 `shared_premises` exactly. There is no `skeptic/aw2*`, `reverse/aw2` or forward AW1 `results.json` input. No `reverse/aw2` package exists.

## Blocking issues

None.

## Non-blocking findings

**N1. Read isolation is verifiable for repository inputs only.**
- The forward files were written from 00:10Z to 00:23Z, in a shared filesystem, after my pre-comparison package was committed (00:17:03Z).
- The producer declares that it read nothing under `skeptic/aw2*`, and its closure contains no such file.
- The code differs from mine in structure (12-digit against 16-digit decimals, boxes `N=2,3` against `N=2,7`, different check ids). No forward AW2 scratch file is in the shared scratchpad root.
- Reads cannot be determined. The exact agreement is expected in any case, since both apply the same admitted formula to the same gate constant.

**N2. The preview is a veto-only dependency.**
- `check.py` reads the stored `arb-preview.json` as a labelled comparison. A missing or inconsistent preview aborts the run (`FileNotFoundError` or `AdmissionError`).
- It never supplies an admitted value, as the point-ball replacement shows.
- The report's wording ("`check.py` reads only that stored file") is accurate. "Not read by the admission path" would not be, so the gate should say "labelled comparison, veto only".

**N3. A literal equal to the rule value passes at runtime.**
- The producer's runtime controls reject non-rule provenance labels and non-rule values. A literal coupling that happens to equal the rule value is caught only by source review, and it is protected by the `check.py` hash in `freeze.json`.
- This is the AW2 analogue of AW1 N7.

**N4. Flag naming.** The producer carries `correlation_shift_resolved:false` and `centered_correlation_shift:"unresolved (AV2 reference_unresolved)"`. The key `centered_correlation_shift_resolved` is absent. The meaning is the same, and my packet carries that key as false.

**N5. Report wording: "first interaction-resolved statement for this model family".** This should be read as "first in this workbench's admitted record". It is not a priority claim, and the gate should not repeat it.

**N6. Calculator reusable mode.**
- Below the cap, the calculator attaches `sign_certified_below_cap` to any `|tau|<10^-8` that excludes 0, with sign margin `S(|tau|)=207.00005·10^-8/|tau|`.
- These values are corollaries of the AW1 bound for `|tau|<=10^-8`, not AW2 admissions. The contract's sub-label refers to `tau_AW2` itself, and any reuse needs its own contract.

**N7. Rule slack.** `K_2^+tau` is about 103.5 times below `1/288` at the cap. Any constant up to about `3.47·10^5` would also return the cap. The rule guarantees only `m>=1`, and the target `m>=2` is checked on its own.

**N8. Undeclared reads, all disclosed.** The tools README, `freeze.py`, the AV2 forward checker and calculator, and the AW1 forward checker were read for code style. The producer also computed the sha256 of the repository contract and gate. None carries premise weight.

## Limitations

1. **Single direction.** One forward producer instantiates the admitted AW1 formula. Admission rests on that producer plus my pre-comparison replay from the contract. Our ancestry is correlated, and `K_2^+` is my own AW1 itemization. The exact agreement is a replay of one admitted formula, not independent physical confirmation.
2. **Model scope.** Only the AM2/AQ1 zero-selected patterned family, the cover `R={0,e_z}`, fixed spacing and `tau=±10^-8`. Nothing transfers to nonzero selected triples, uniform Wilson theory, weak coupling or the continuum. Calculator values below the cap are corollaries, not AW2 admissions.
3. **Inherited without re-proof:**
   - from AW1: the first-order coefficient `+tau/144`, the remainder bound `|r|<=K_2^+tau^2` (uniform in `N`, cutoff and every AQ1 limit), and the flip lemma;
   - from AV1: the product split, the anchored-norm tier, cutoff removal and AQ passage;
   - from AM2: the fixed point, majorant, gaps and ground uniqueness;
   - the AQ1 construction and the I1 dictionary.
4. **Absolute bound.** `K_2^+` is an absolute second-order bound. It gives no sign of `r(tau)` and no third-order remainder. The AM2 majorant is 99.98% of it, so the enclosure is conservative.
5. **Static only.** This is a static equal-time mean in the AQ states. `resolved_interaction_shift` refers to `omega(W)` alone. There is no dynamical, mass-gap, susceptibility or centered-correlation statement.
6. **Whole-set statement.** No uniqueness of the AQ state, and no whole-sequence convergence or rate in `N`. The `-tau` pairing of individual states holds only along a common subsequence.
7. **Fixtures and preview.** The one-plaquette, 3×3 centring and synthetic two-limit fixtures are finite exact audits (`transfers_to_aq:false`). The Arb/mpmath preview is a labelled, veto-only comparison.
8. **Literal-coupling protection.** For a literal equal to the rule value, it rests on source review and the `check.py` hash in `freeze.json`.
9. **Read isolation.** Verified for repository inputs only. Scratch and shared-filesystem reads cannot be determined.
10. **Priority.** Scientific priority is unverified.
