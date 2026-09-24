# Hruday sign-certified enclosure of the Wilson mean at the AW1-frozen coupling — AW2 forward (single direction)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production under the frozen AW2 contract (`research/round32/contracts/aw2.json`, sha256 `aa559b18231961b5bb9dc5b7d0dd3097a1a2753916b54639eb1fd573e08368f9`). AW2 runs in one direction only (`producers=[forward]`, `direction=single+skeptic`). **Admission requires the skeptic's independent pre-comparison replay from the contract alone.** This packet is not that replay and is not an independent review of itself. It is correlated model-agent work, not human peer review.

**What this producer read.**
- The frozen contract snapshot, first.
- After that, only files under `inputs/`: AGENTS.md; the AW1 contract, gate, forward and reverse reports and the skeptic review; the AV1 gate, reports and review; the AM2, AQ1, AQ2, AT4 and I1 premises; `selection-aw2.md`; and the method skills.
- Undeclared reads, for protocol and code style only: `research/round32/tools/README.md`, `research/round32/tools/freeze.py`, `research/round32/forward/av2/check.py` (header and helpers), `research/round32/forward/av2/calculator.py`, and `research/round32/forward/aw1/check.py` (helpers, fixtures and packet assembly). None of these carries premise weight.
- I also computed the sha256 of the repository copies of `contracts/aw2.json` and `advisor/aw1-gate.json`, only to confirm that they equal the snapshots. I did not read their contents.
- Nothing under `research/round32/skeptic/aw2*` or `research/round32/reverse/`, and no other current AW2 work, was read.
- The forward AW1 `results.json` is not a declared premise and is absent from the input closure. The labelled-variant cross-check therefore uses the forward AW1 report snapshot's preview `unpinned t-bounds 3354.80322946` and the skeptic review's statement that `K_2^+` equals that variant exactly.

**Attribution.** The perturbative and centre-flip arguments are established kinds of mathematics. The contribution here is the exact instantiation of the admitted AW1 bound at the rule-fixed coupling, with its controls. Scientific priority is unverified.

## Verdict (forward, single direction)

**Proposed: `accepted_within_scope`, sub-label `static_not_dynamic`.** Admission needs the skeptic's independent replay.

1. **Coupling.** The frozen AW1 decade-grid rule, evaluated inside `check.py` from the `K_2^+` in the hash-verified AW1 gate, gives **`tau_AW2 = 10^-8`**, which is the cap. No literal coupling is used.
2. **Enclosure.** For every state in the whole set of AQ1 subsequential limits at the zero selected triple, and in every centered whole-star box `N>=2` at every on-site cutoff:
   - at `tau = +10^-8`: `omega_tau(W)` lies in **[6.91089641214e-11, 6.97799247674e-11]**;
   - at `tau = -10^-8`: in **[-6.97799247674e-11, -6.91089641214e-11]**.

   These decimals are widened outward. The exact rational endpoints are given in Section 4.
3. **Zero is excluded strictly at both signs.**
   - Exclusion margin: `m = 206.000052445...`, which meets the target `m >= 2`.
   - Sign margin: `1/(144 K_2^+ |tau|) = 207.000052445...`.
   - The `-10^-8` enclosure is the mirror image given by the AW1 flip lemma at the zero triple. It is a replay, not a second confirmation.
4. **Scope.** This is a static equal-time effect.
   - `sign_certified_below_cap` does not apply, because `tau_AW2` equals the cap.
   - No dynamical correction, mass shift or susceptibility is claimed.
   - The shift of the centered correlation remains unresolved (AV2 `reference_unresolved`).
5. **Checker.**
   - `check.py` runs **37 exact checks**. All 23 contract controls are damaging mutations raised through explicit exceptions, 116 rejected mutations in all.
   - Output is byte-identical under `python3 -B` and `python3 -B -O`.
   - `calculator.py` is a reusable exact calculator restricted to the proved domain.

## 1. Model and conventions

The model is the zero-selected patterned AQ subfamily of AV1/AW1, with no model change:
- SU(2) Kogut–Susskind form on `Z^3` at fixed spacing, with coarse 24-link factors;
- selected triple exactly `(0,0,0)`, so the reference is the Haar product;
- centered whole-star boxes `Lambda_N=[-N,N]^3`, `N>=2`;
- the original xz Wilson loop `W=(1/2)Tr[U_{0,x}U_{e_x,z}U_{e_z,x}^{-1}U_{0,z}^{-1}]`, with complete cover `R={0,e_z}` (link owners `0,0,e_z,0`);
- fixed positive `alpha`, `hbar`, `E_star` and spacing.

Under I1.5, which is frozen as the contract string `phi_b=-(tau/3) sum W_f, V_b=phi_b/8`:

\[
 H_N=\sum_b h_b+\sum_{b+S\subset\Lambda_N}\phi_b,\qquad \phi_b=-\tfrac{\tau}{3}\sum_{f\in O_b}W_f\ \ (\delta=\alpha/8\ \text{units}),\qquad V_b=\phi_b/8\ \ (\alpha\ \text{units}).
 \tag{HNM-AW2-F01}
\]

The observable is the **uncentered** mean `omega(W)`. Its free (Haar) reference value is `omega_0(W)=E[W]=0`, read from the contract.

## 2. The admitted premise (AW1 gate, hash-verified)

The AW1 gate snapshot has sha256 `647dc337…41ae`, which `check.py` and `calculator.py` hard-code and verify. The gate also binds 25 of the other 27 snapshots in `inputs/`, and every one of them matches its binding. The gate admits:

\[
 \omega_\tau(W)=+\frac{\tau}{144}+r(\tau),\qquad |r(\tau)|\le K_2^+\tau^2,\qquad |\tau|\le10^{-8},
 \tag{HNM-AW2-F02}
\]

uniformly in `N`, the cutoff and every AQ1 subsequential limit, at the exact tier (`T=(49|tau|/144)/(1-352J)`, `rho=352JT`, `J=28|tau|`). The constant is parsed from the gate's `decision` string:

\[
 K_2^+=\frac{81108864767825329926713064490531229475390625}{24176936535511801466930759024724079017984}\in[3354.80322946,\,3354.80322947].
 \tag{HNM-AW2-F03}
\]

It is cross-checked for exact equality against four sources:
- the gate's `accepted` string;
- the contract parameter;
- the skeptic review's exact rational;
- the forward AW1 report's `unpinned_t_bounds` preview, `3354.80322946`, which is its truncation.

The outward ceiling `3354803229461691/10^12` dominates it by less than `10^-12`.

As a consistency replay (not a source), the itemization named in the gate reproduces `K_2^+` exactly from the gate's own constants:

`K_2^+ tau^2 = rho + T*T (straddling) + T*T (two-creation) + eps^2 (density) + (|tau|/144) eps^2 (normalization, third order)`, with `eps=2T+T^2`.

The same `T` reproduces the AV1 gate's `D_ii` exactly. The AM2 remainder term is 99.979% of the constant.

## 3. The frozen coupling rule (item 1)

The rule is read from the AW1 contract snapshot, whose sha256 is the AW1 gate's binding:

\[
 \tau_{AW2}=\max\{10^{-k}:k\ge8,\ K_2^+10^{-k}\le\tfrac1{288}\}.
 \tag{HNM-AW2-F04}
\]

The checker ties the bound semantically to the coefficient: `1/288` must be half the first-order coefficient `1/144`. This is the lesson of AW1 review N7.

**Arithmetic, all exact:**

`K_2^+ 10^-8 = 207638693805632844612385445095759947457/6189295753091021175534274310329364228603904 <= 3.35480322947e-5 <= 1/288 = 3.47222...e-3`

- slack: `1/288 - K_2^+ tau = 21282971559982635125992733687992310290751/6189295753091021175534274310329364228603904`;
- ratio `(1/288)/(K_2^+ tau) = 103.500026222...`. This ratio is not the sign margin (AW1 review N4).

The grid starts at the cap `10^-8`, so no larger element exists and the rule returns **`tau_AW2=10^-8`**. This agrees with the contract's stated value and the gate's stated value. Both are cross-checks only.

Rejected couplings:
- a literal `1/10^8`;
- the contract text used as the coupling;
- `10^-9`, which is not the largest decade;
- the off-grid value `5·10^-9`;
- the forward AW1 headline constant `≈3354.638`, a recomputed value that is not the gate binding;
- the crude constant fed to the rule;
- a rule bound that is not half the coefficient.

## 4. The enclosure (item 2)

\[
 \omega_\tau(W)\in I(\tau):=\Big[\frac{\tau}{144}-K_2^+\tau^2,\ \frac{\tau}{144}+K_2^+\tau^2\Big].
 \tag{HNM-AW2-F05}
\]

At `tau=+10^-8`:
- the first-order value is `1/14400000000 ≈ 6.94444444444e-11`;
- the half-width is `K_2^+ tau^2 = 207638693805632844612385445095759947457/618929575309102117553427431032936422860390400000000 ∈ [3.35480322946e-13, 3.35480322947e-13]`.

| sign | exact lower endpoint | exact upper endpoint | outward decimals |
|---|---|---|---|
| `+` | `42773581813770903096597852821080380528959/618929575309102117553427431032936422860390400000000` | `43188859201382168785822623711271900423873/618929575309102117553427431032936422860390400000000` | `[6.91089641214e-11, 6.97799247674e-11]` |
| `-` | `-43188859201382168785822623711271900423873/618929575309102117553427431032936422860390400000000` | `-42773581813770903096597852821080380528959/618929575309102117553427431032936422860390400000000` | `[-6.97799247674e-11, -6.91089641214e-11]` |

Lower endpoints are rounded down and upper endpoints up, at 12 significant digits. The checker re-parses every decimal string exactly and verifies both its direction and that it lies within one unit of the last digit.

**Mirror.** `I(-tau)=-I(tau)`. This follows directly from (F02), which holds at both signs. It is also the image under the AW1 flip lemma at the zero triple: `U_E H_N(tau,0)U_E^*=H_N(-tau,0)`, `omega_{N,-tau}(W)=-omega_{N,tau}(W)` and `S(-tau)=S(tau) o alpha_E`. The minus-sign enclosure is therefore a **replay**, not a second confirmation.

## 5. Strict exclusion and margins

With `S` the sign margin and `m` the exclusion margin:

\[
 S=\frac{|\tau|/144}{K_2^+\tau^2}=\frac1{144K_2^+|\tau|},\qquad m=\frac{|\tau|/144-K_2^+\tau^2}{K_2^+\tau^2}=S-1,\qquad m\ge2\iff S\ge3 .
 \tag{HNM-AW2-F06}
\]

At `|tau|=10^-8`:
- `S = 42981220507576535941210238266176140476416/207638693805632844612385445095759947457 >= 2.07000052445e2`. This is at least the gate's directed floor `41400010489/200000000`, and it matches the contract's "about 207".
- `m = 42773581813770903096597852821080380528959/207638693805632844612385445095759947457 >= 2.06000052445e2 >= 2`. The target is read from the contract preregistration.

The lower endpoint at `+10^-8` is strictly positive, and the upper endpoint at `-10^-8` is strictly negative. The free reference `0` is therefore **strictly excluded at both signs**. The lower endpoint equals `(1-1/S)` times the first-order value, which is about 99.52% of it.

The crude tier is retained as a limited-tier control:
- `K_2^crude = 1937877026146766159414097129/244140625000000000000 ≈ 7.93754429909e6`, reproduced exactly from the gate's `t_c=592|tau|`;
- its cap enclosure is `[-7.2431e-10, 8.6320e-10]`, which **contains 0**; its sign margin is `0.0874886`;
- it is not admitted. The rule would give it `10^-10`, which is recorded as information only and never substituted.

## 6. Scope: what is and is not claimed (item 3)

**Claimed.** Take any state `omega` in the whole set `S(tau)` of AQ1 subsequential limits: local trace-norm limits, along subsequences of centered whole-star boxes `N>=2`, of the unique box ground states at the zero selected triple, at either sign with `|tau|=10^-8`. Then `omega(W)` lies in `I(tau)`, which excludes `0` strictly with sign `sign(tau)`. The passage to the limit is:

\[
 |\omega(W)-\omega_{N_k}(W)|\le\|W\|\,\|\rho_R-\rho_{N_k,R}\|_1\to0,\qquad \|W\|\le1,
 \tag{HNM-AW2-F07}
\]

and `I(tau)` is closed and independent of `N`. The constant is volume-uniform. The checker verifies that the formula inputs are identical in boxes `N=2` and `N=3`:
- 82 retained faces meet `R`;
- four incoming stars at each site of `R`;
- 49 faces per factor.

It also verifies that `N=1` would drop incoming stars and is out of scope.

This is a **static equal-time effect** in the stationary AQ state (sub-label `static_not_dynamic`). It is the first interaction-resolved statement for this model family: the free reference lies outside the enclosure. Accordingly `resolved_interaction_shift:true` is set, and only because the exclusion holds at the cap.

**Not claimed.**
- No dynamical correction, mass shift, susceptibility or mass-gap statement.
- The shift of the centered correlation `C(s)` remains unresolved (AV2 `reference_unresolved`). Its first-order term vanishes by parity (AW1), and its second-order constant is not uniform in `N`.
- `sign_certified_below_cap` is false, because `tau_AW2` is the cap.
- No uniqueness of the AQ state, whole-sequence convergence or rate in `N`. Pointwise `-tau` pairing holds only along a common subsequence.
- No third-order remainder, uniform Wilson theory, weak-coupling or continuum statement, and no statement at nonzero selected triples.
- No transfer from any finite graph.
- Scientific priority is not verified.

## 7. Controls (item 4)

Each control is an explicit `AdmissionError` raised through `require`. No `assert` is used, so every control stays active under `-O`. Every mutation below was run and rejected for the stated reason.

| control | damaging mutations rejected |
|---|---|
| `aw2_coupling_rule_prefrozen` | literal coupling; contract text used as coupling; `10^-9`; `5·10^-9`; forward headline constant; crude constant; rule bound not half the coefficient |
| `free_reference_exclusion` | crude enclosure (contains 0) claimed resolved; crude label on an exclusion claim; lower endpoint exactly 0; synthetic margin `3/2` claimed accepted |
| `sign_flip_tau` | sign-blind `abs(tau)` enclosure; mirror counted as a second confirmation |
| `haar_parity_exact` | odd tensor power given an invariant; nonzero reference value. Moments `1,0,1/4,0,1/8,0,5/64,0,7/128` by Clebsch–Gordan and by the free-link `S^3` route |
| `wilson_mean_first_order_coefficient` | `tau/72`; `tau/288`; the literal `+2<W Omega_0,L_0>` display (`-tau/144`). Face sum over all 82 faces meeting `R` gives `+tau/144` |
| `wrong_face_control` | another face with owner set `R` claimed to pair with `W`; all ten inside faces counted; `W` excluded. Every face other than `W` has `E[W W_f]=0` |
| `wilson_overlap_single_component` | factor 4 unlabelled; multiplier 1/2; single-site creations claimed to overlap. `W` has 3 links owned at 0 and 1 at `e_z`; `mult(1)=0`; `||W Omega_R||=1/2` |
| `full_original_wilson_cover` | cover `{0}`; cover `{0,e_x}`; fine drawn vertices as the cover |
| `missing_incoming_stars` | `J=7|tau|` (one star); `J=21|tau|` (three stars). The replayed `K_2^+` then differs from the gate |
| `wrong_delta_alpha_hbar_clock` | `tau/1152`; `tau/18`; `tau` rescaled by `alpha/E_star`; the `u=s/8` exponent-24 clock in the packet. Enclosure unchanged at `alpha=5`, `hbar=7`, `E_star=11/2`, spacing 3 |
| `first_order_mean_charged` | zero first-order mean; C(s) parity applied to the uncentered mean |
| `vector_versus_scalar_centering` | scalar subtraction as vector centring (3×3 exact fixture: residues `d^2` against `-(2md+d^2)`); `m_hat` inserted in the `omega(W)` path; calculator `m_hat` argument (TypeError) |
| `second_order_remainder_itemized` | second-order term dropped; density term dropped; smaller recomputed constant substituted; `K/2`; `not_applicable` entry without a reason; ledger item missing |
| `tier_mixing_rejected` | crude constant labelled exact; crude straddling term inside the exact sum; crude tier used to certify |
| `insufficient_verdict_retained` | crude tier reported as excluding 0 at the cap; crude retuned to `10^-10` under the cap label; margin in `[1,2)` upgraded to accepted |
| `tau_scaling_exponent` | the `K_2^+ tau^2` term relabelled first order; `tau/144` relabelled second order; AT4 square-root ratio 10 relabelled linear. Exact ratios under `tau -> tau/100`: 100 and 10000 |
| `root_n_misuse` | root sum of squares; division by `sqrt(82)`; division by 64 |
| `static_not_dynamic_effect` | dynamical, mass-shift, susceptibility and resolved-correlation-shift relabels; `sign_certified_below_cap` at the cap |
| `changed_model_relabelled` | coupling `10^-9`; nonzero triple; strip reference; finite-graph id; finite-volume provenance; cover `{0}` |
| `exact_arithmetic_admission` | float, bool, NaN and `1/0` inputs, in `check.py` and in the calculator. Imports of `check.py` and `calculator.py` are standard library only |
| `single_producer_declared` | fabricated reverse package; skeptic replay requirement dropped; reverse isolation claimed satisfied; mirror claimed independent. **`reverse_premise_isolation` is not applicable (single producer)** |
| `no_priority_or_continuum_claim` | continuum, priority, uniform Wilson or dynamical flag set true; shift claimed resolved with a crude enclosure containing 0 |
| `coherent_evidence_tampering` | each of the following, with the packet hash rebound: a control Boolean flipped; a snapshot removed; `K_2^+` halved; `K_2^+` replaced by the forward headline; `tau_AW2` changed; lower endpoint changed; below-cap flag set; reverse producer added. Also a contract target edited with the contract hash rebound, rejected because the hard-coded contract sha256 fails, and the gate `K` doubled with the hash rebound, rejected because the hard-coded gate sha256 fails |

**Sign-convention fixture.** The frozen I1.5 string is verified against the contract and against the I1.5 equation in the I1 snapshot. Two mutations are rejected:
- a flipped `phi_b` sign in the string;
- a coherent flip in both the derivation and the fixture, which gives `-tau/144` against the admitted `+tau/144`.

The one-plaquette character-basis fixture (`H_0=8k(k+2)`, `V=-(tau/3)W`) is labelled `FG(one_plaquette, …)`, `finite_graph:true`, `transfers_to_aq:false`. It gives:
- the exact Rayleigh–Schrödinger series `<W>=tau/144+0·tau^2-5tau^3/11943936+0·tau^4+289tau^5/6604518850560`, with `E_2=-tau^2/6912` in `alpha` units. This is identical at truncations 8 and 10 and equals the reviewed AW1 series.
- the exact `j<=1/2` ground: `det=-b^2<0` forces `E0<0`, so `sign(<W>)=sign(tau)`. The rational brackets are `[6.94444444439e-11, 6.94444444446e-11]` and its mirror.

**Other checks.** In addition to the 23 controls:
- contract, AW1-gate and AV1-gate bindings;
- both enclosures, and the exclusion and margins;
- the AQ1 whole-set scope (uniqueness, pointwise `-tau`, rate, nonzero-triple and finite-graph-transfer mutations rejected);
- the two-box volume uniformity;
- AV1 compatibility: `D_ii ≈ 1.3612e-8` contains both enclosures, with a ratio of about 195.08;
- the labelled Arb/mpmath preview;
- calculator domain rejections (13 cases) and the fixed-design match;
- the verdict classification.

**Arb/mpmath preview (labelled).** `arb_preview.py` recomputes the endpoints and margins with python-flint 0.9.0 (Arb) and mpmath 1.3.0 intervals at 256 bits. It stores exact dyadic ball bounds in `arb-preview.json`, marked `preview_only:true` and `used_for_admission:false`. `check.py` reads only that stored file. It verifies that every exact endpoint and margin lies inside both previews, and it rejects a promoted or shifted preview. Neither library is imported in the admission path.

## 8. Calculator (item 5)

The entry point is `calculator.enclose(*, tau, selected=('0','0','0'), fixed_design=False, tier='exact', alpha, hbar, E_star, lattice_spacing)`.
- **Inputs.** Exact inputs only (int, Fraction, `p/q` or plain decimal text); floats and bools raise `ValueError`.
- **Constants.** `K_2^+`, the first-order coefficient `1/144`, the cap and the rule are read only from the hash-verified AW1 gate and the gate-bound AW1 contract snapshot. There is no `K` or centering parameter (TypeError).
- **Domain.** Zero triple and `0<|tau|<=10^-8`. The gate constant is admitted for every `|tau|<=10^-8`, and the replayed itemization is nondecreasing in `|tau|`.
- **Fixed design.** `fixed_design=True` enforces `|tau|=tau_AW2` from the rule.
- **Returns:**
  - the exact enclosure and its outward decimals, with `excludes_zero` and `sign_of_omega_W`;
  - both margins and the rule arithmetic;
  - sub-labels: `static_not_dynamic`, plus `sign_certified_below_cap` only in reusable mode below the cap;
  - `resolved_interaction_shift_at_cap` and the claim flags.

## 9. Claim flags (results.json)

- false: `continuum_claim`, `uniform_wilson_claim`, `sign_certified_below_cap`, `dynamical_correction_claim`, `scientific_priority_verified`, `mass_shift_claim`, `susceptibility_claim`, `correlation_shift_resolved`, `uniqueness_claim`, `whole_sequence_convergence_claim`, `rate_in_N_claim`, `third_order_remainder_claim`;
- true: `static_not_dynamic`, and `resolved_interaction_shift` (the exclusion holds at the cap at both signs);
- `producers:["forward"]`, `single_direction_independent_replay_required:true`.

Every number in `results.json` is a string, and keys are sorted.

## 10. Limitations and exclusions

The contract's claim exclusions, verbatim:
- a dynamical correction or mass gap statement
- a correlation shift
- uniform Wilson magnetic theory
- AQ uniqueness
- continuum
- scientific priority

The preregistration exclusions, verbatim:
- free reference inside enclosure => no interaction claim
- uniqueness of the AQ state
- whole-sequence convergence or rate in N
- continuum or weak coupling
- transfer from a finite graph
- relabelling a static shift as dynamical
- scientific priority

Further limitations, stated honestly:
1. **Single direction.** One producer instantiates an admitted formula. Admission requires the skeptic's independent replay from the contract alone. Nothing here is independent confirmation, and the `-tau` enclosure is a mirror replay.
2. **Inherited, not re-proved.** The AW1 gate's first-order coefficient, remainder bound and flip lemma. AV1's product split, anchored-norm tier, cutoff removal and AQ passage. AM2's fixed point, majorant, gaps and ground uniqueness. AQ1's construction. The I1 dictionary. The consistency replay only reproduces the gate constant from the gate's own named constants; it does not re-prove them.
3. **Absolute bound.** `K_2^+` is an absolute second-order upper bound with no sign of `r(tau)`. The enclosure is correspondingly conservative, since the AM2 majorant is 99.98% of the constant. No third-order remainder is used.
4. **Model restriction.** Only the zero selected triple, the cover `R`, fixed spacing and `|tau|<=10^-8` (the certificate is at `|tau|=10^-8`). Nothing transfers to nonzero triples, uniform Wilson theory, weak coupling or the continuum.
5. **Fixtures.** The one-plaquette, 3×3 centring and synthetic two-limit fixtures are exact finite audits, not proofs of infinite-volume statements.
6. **Preview.** The Arb/mpmath preview depends on the installed library versions. It is a stored, labelled comparison and never admission arithmetic.

**Methodological lenses.** These are modern uses of the snapshotted skills. No historical figure endorses anything, and no historical or occult material supplies a premise.
- **Newton, analysis before synthesis.** The coupling is fixed by analysis of the admitted constant before any enclosure is synthesized.
- **Tesla, complete accounting.** The full `K_2^+ tau^2` is charged linearly, and nothing is divided by root-N.

## 11. Reproduction

```bash
python3 -B research/round32/forward/aw2/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/forward/aw2/check.py --output /absolute/fresh/dir2      # byte-identical
python3 -B research/round32/forward/aw2/arb_preview.py --output /absolute/path/arb-preview.json   # optional labelled preview
python3 -B research/round32/tools/freeze.py verify research/round32/forward/aw2
```

`output/results.json` sha256 `ec09f259e0956eb347a792098b5a9af32e4563ca3cba25b38cfc189b1136abe0`. `freeze.json` binds every file in this producer closure, including this report.
