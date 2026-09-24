# AV2 skeptical review (post-comparison)

**Verdict: accepted_within_scope, sub-label `reference_unresolved`.** Both routes prove the window lemma and the constants of the frozen C^2 window:
- forward, by half-line transforms;
- reverse, by residues.

With the AV1-admitted forward tier-(ii) state bound, both producers certify the centered original xz Wilson Euclidean correlation at `s=1` and `tau=+10^-8` to within about `1.8319675034e-7`. That meets the unchanged `10^-6` target with margin 5.4586. The `tau=-10^-8` value is a replay of the same `|tau|` formula.

The free value `e^{-3}/4` lies inside the interval, so no interaction shift is claimed. The retained insufficient Poisson controls stand at unchanged `tau` and `s`. There are no blocking issues. The datum is identical in both producers. The two exact radii differ by `2.520e-41`, a rounding choice (finding N2).

**Standing.** I am a model-agent skeptic with correlated ancestry: same model family as the advisor, the lenses and both producers, and my triage proposed this window. This is not human peer review or formal verification. Human project author: Hruday N M (BUNZEEY).

My pre-comparison package is unchanged; its hashes still match `av2-independent-freeze.json`. It was committed (`eebb0a1`, 22:30:01Z) before the forward (`0aa2f88`, 22:36:10Z) and reverse (`de1b771`) commits. It contains:
- `av2-independent-derivation.md`;
- `av2_check.py`, with 69 checks and all 24 controls;
- `av2-contract-review.md`.

This review adds:
- `av2_postreview_check.py`: 63 exact checks, including 24 source-edit mutations and 2 unmutated baselines;
- `av2-postreview/results.json`: byte-identical under normal and `-O` Python, sha256 `7ec72aa0…93c2`;
- `av2-replays.json`.

## What is proved, with quantifiers

**Model.** The AM2/AQ1 zero-selected patterned family:
- SU(2) Kogut–Susskind form on Z^3 at fixed spacing, with coarse 24-link factors;
- selected triple exactly `(0,0,0)`, so the reference is the Haar product;
- whole stars `phi_b=-(tau/3) sum W_f`;
- original xz Wilson loop `W` with complete cover `R={0,e_z}` (48 links, 36 endpoints) and seven incident stars;
- physical clock `s=alpha t_E/hbar` for Euclidean time and `theta=alpha t/hbar` for real time, with `G=H/alpha`.

**State.** Each AQ1 subsequential state of the centered whole-star construction at `tau=+10^-8` is covered, and so is each at `tau=-10^-8`. Every chosen state is treated separately. No uniqueness, whole-sequence convergence or rate in `N` is claimed.

**Window lemma.** The frozen conventions are `c(theta)=<chi,e^{i theta G}chi>` and `ghat(theta)=(2pi)^{-1} int g e^{-i theta x}dx`. The window is `g(x)=e^{-sx}` for `x>=0` and `e^{sx}(1-2sx+2s^2x^2)` for `x<0`. Its properties:
- `g` lies in `L^1 ∩ C_0` and is C^2, with `||g||_1=8/s`;
- `g'''` jumps by `-8s^3`;
- `ghat=4s^3/(pi(s-i theta)^3(s+i theta))` is in `L^1`.

L^1 inversion holds at every `x`, since both sides are continuous. Fubini applies because `M_0 eta(R)<inf`. AQ1 nonnegativity `G>=0` is used only to put `eta` on `[0,inf)`, where `g=e^{-sx}`; the AQ2 gap is not used. Hence:
- `C(s)=int ghat(theta)c(theta)dtheta`;
- `C_0(s)=g(3)/4=e^{-3s}/4`.

**Constants.** `M_0=||ghat||_1=2`, `M_1=4s/pi` and `M_2=2s^2`.

**Real-time comparison.** For every real `theta`: `|c(theta)-c_0(theta)|<=k|theta|+D+m^2`. The terms rest on these facts:
- `k=49|tau|/4` comes from the seven-star relative-unitary Duhamel argument (AT4 F10–F12, restated with its domain argument by both producers). It is local and uniform in `N`.
- `D` is the AV1-admitted forward tier-(ii) value, with trace duality against the non-effect `W alpha^0_theta(W)`. There is no `D/2` refinement.
- `m^2<=D^2` is charged.

**Certificate at s=1.** Integrating the comparison against `|ghat|`:

`|C(1)-e^{-3}/4| <= E = M_0(D+D^2)+kM_1 = 2(D+D^2)+49|tau|/pi`.

The certificate is `|C(1)-d|<=r`, with `r=E^+ + 1/(4·10^40)`, and `r<=10^-6`. The free value `e^{-3}/4` lies inside `[d-r,d+r]`.

## Exact numbers re-derived (my own Fraction code at `10^-70`)

I used Hutton `pi` with a Machin overlap, and a positive-Taylor exponential with a geometric tail and outward squaring, all in `av2-postreview/results.json`.

**Inputs.**
- `D=585079838465912592144137406066050/42981220507576537932303142777593983768257` (~1.36124529e-8). It equals the AV1 formula, the gate decision, the contract, and both producers' exports.
- `k=49/400000000`.

**Itemized terms.** The state, mean-square and arithmetic terms are identical in both producers.
- `state = 2D = 1170159676931825184288274812132100/42981220507576537932303142777593983768257` (~2.72249057e-8).
- `mean_square = 2D^2` (~3.70598e-16).
- `kernel_dynamics` (~1.5597184423e-7) differs between the producers (N2):
  - forward: `49|tau|/pi_lo = 1225000000000000000000000000000000/7853981633974483096156608458198757210489`;
  - reverse: `1559718442300574290535060881050641/10^40`.
- `arithmetic = 1/(4·10^40)`, the half-width of the `e^{-3}/4` bracket.

**Datum** (identical in both producers): `d=497870683678639429793424156500617766317/(4·10^40)`. Here the numerator `m` is `e^{-3}·10^40` rounded to the nearest integer. Both producers' `e^{-3}` bracket is `[(m-1),(m+1)]/10^40`. My enclosure gives `|d-e^{-3}/4|<=1.02e-43`.

**Radius.**
- Forward: `r_F` (exact, 319 characters in `results.json`), ~`1.83196750341e-7`.
- Reverse: `r_R` (exact, 238 characters), ~`1.83196750341e-7`.
- Difference: `r_R-r_F=2.520e-41`, exactly `1979686519699651457242890990044705373449/(78539816339744830961566084581987572104890·10^40)`.
- Both are valid directed bounds: `r>=E^+ + |d-e^{-3}/4|`.
- Neither is inflated: `r-E<=5.02e-41`.
- Against my pre-comparison radius, they differ by `2.50e-41` (forward) and `5.02e-41` (reverse).

**Common outward bound.** `R=1831967503411879425147166810021607/10^40` (~1.8319675034118794e-7). It bounds both producers' radii, equals my pre-comparison outward radius digit for digit, and gives a margin `10^-6/R=5.45861`.

**Interval.** Producers' `[d-r,d+r]` is exact. With `R`:

`C(1) in [497863355808625782275723567833377679889/(4·10^40), 99575602309730615462224949033571570549/(8·10^39)] ~ [0.012446583895215644557, 0.012446950288716326933]`.

It contains `e^{-3}/4`.

**Scaling.** `E(tau)/E(tau/100)=100.00145`, which is linear. The AT4 square-root `D` would give 10.0081.

**Crossover.** `s*=pi(10^-6-2(D+D^2))/(49|tau|)=6.236863446033…`. The forward's `[6.236863446033, 6.236863446034]` and the reverse's `[6.236863446, 6.236863447]` both contain it, and it lies in the contract's 6.1–6.3.

**Retained failures.**
- **AT4 Poisson at `L=10^4`:** `8.415187043862665e-4`. It is inside the forward bracket and below the reverse upper value, and it matches the frozen AT4 decimal to `10^-17`.
- **Poisson floor, every `L`:** `(2k/pi)(1+log(1/(2k)))>=1.265088223301e-6`, and `>=1.2787006e-6` with the admitted `D`. The forward lower bound (`1.265088223301e-6`) and the reverse lower bound (`1.265088204195e-6`, looser) are both below it and valid. Each producer's upper value is at least `F(L)` at its evaluated integer `L`.
- **Tier (i):** the window radius is `4.751779428e-5`.
- **C^1 preview:** `1.733037577e-7`, which is below the C^2 value. The kernel-switch rejection therefore guards a real post-hoc gain.

## The two routes (and two more)

**Forward: half-line transforms.** The Laplace transforms of the two branches give `2pi ghat·a^3b=(2s-c_1)a^2+(2sc_1-2c_2)a+4sc_2`, with `a=s-i theta` and `b=s+i theta`.
- C^1 matching kills the `a^2` (`theta^-2`) term.
- C^2 matching kills the `a` (`theta^-3`) term.
- Only `8s^3` survives.

The moments come from exact antiderivatives (`R+B·arctan`). I rechecked the numerator algebra by hand.

**Reverse: residues.** The reverse starts from an analysis of the target.
- Exactness on `x>=0` forces one simple upper pole at `theta=is`, with `N_n=(2s)^n/(2pi)`.
- Finite `M_0`, `M_1` and `M_2` force the lower pole order to be `n=3`.
- The residue at the triple pole reproduces `e^{sx}(1-2sx+2s^2x^2)`.
- The moments follow from `Res_{is}`: `M_0=2` and `M_2=2s^2`. `M_1` comes from a keyhole contour: `-sum Res[z log z/(z^2+s^2)^2]=1/(2s^2)`, with the log terms cancelling pole by pole.

I rederived both keyhole residues (each `-1/(4s^2)`) and `Res_{is}` for `M_0` and `M_2` by hand.

**Skeptic, pre-comparison: annihilator and jump.** `P(D)=(D+s)(D-s)^3`, and `P(D)g=-8s^3 delta`. The moments follow from Wallis integrals.

**Skeptic, post-comparison: Leibniz.** A fourth route checks the residues. `-2pi i Res_{-is}` expanded by Leibniz gives:
- `1` for `n=1`;
- `1-2sx` for `n=2`;
- `1-2sx+2s^2x^2` for `n=3`,

at `s` in `{1/3,1,2,7}`. At `s=1` the triple-pole residue is `e^x(i/8-ix/4+ix^2/4)` and the upper residue is `-i/8`. Both equal the reverse's exported strings.

All four routes give `M_0=2`, `M_1=4s/pi` and `M_2=2s^2`. They agree on Poisson (`M_1` infinite) and on C^1 (`M_2` infinite).

## Review against the ten required items (both producers)

1. **Window lemma.**
   - Both state `g in L^1 ∩ C_0`, `ghat in L^1`, inversion at every `x` by continuity, Fubini with the finite measure `eta`, and AQ1 nonnegativity as the only spectral input.
   - Neither uses the AQ2 gap. The forward rejects a window matched only above the gap.
   - Both exhibit the negative-atom misread: `5/e` against the heat value `e`.
2. **Constants.** Correct by both routes, and derived before the contract strings are compared. Both checkers carry directed Machin `pi` at `10^-40`. Both reject the trap `∫ghat=g(0)=1` used as the L^1 norm.
3. **Real-time comparison.** Both use `k=49|tau|/4` and the seven stars, with the extensive `(2N)^3` norm rejected. `D` is read from the contract, equals the gate, and is reproduced by the AV1 formula. `m^2<=D^2` is charged. The `D/2` effect refinement is rejected with a non-effect fixture:
   - forward: `diag(1,-1)`;
   - reverse: `diag(1,(-7+24i)/25)`.
4. **Radius.** Itemized as `state`, `mean_square`, `kernel_dynamics` and `arithmetic`. The `pi` lower bound sits in the kernel term only. The arithmetic term is the half-width about the rational datum. The Boolean is exact.
5. **Retained failures.**
   - Both keep AT4 at `L=10^4` and prove an all-`L` Poisson floor. The forward uses `log(1+L^2)>=2log L`; the reverse uses the monotonicity of `u(L)=2kL^3-L^2-1` and bisection. One evaluation at `L*` is not used as a proof.
   - Both exhibit the divergent Poisson first moment against the window's finite `4s/pi`.
6. **Crossover.** Both enclose `s*` and certify no node but `s=1`. `grid_claim` is false, and there is no `[0,128]` claim.
7. **No resolved shift.** Both carry `reference_unresolved`, with `resolved_interaction_shift:false`.
8. **Calculators.** I probed both on temporary copies. Each rejects 20 bad calls: a float, a bool, `NaN`, `Infinity`, `1/0`, an empty string, a nonzero triple, `|tau|>10^-8` at either sign, `s<=0`, nonpositive scales or target, an unadmitted tier, the C^1 or Poisson kernel, a changed fixed design, and a supplied `D` (`TypeError`: `D` is not an input). Both accept exact inputs:
   - the forms `Fraction`, `p/q` and exact decimal give identical radii;
   - `tau=0` gives the arithmetic term alone;
   - below the cap, `D` equals the AV1 formula in both;
   - fixed design reproduces the frozen radius.
9. **Freeze, replays and flags.** Both `freeze.py verify` pass, and all four replays are byte-identical. The flags are the contract's: `continuum_claim`, `uniform_wilson_claim`, `resolved_interaction_shift`, `scientific_priority_verified` and `grid_claim` false, `euclidean_node_certified` true.
10. **Minus-tau and C^1.** Both report `-tau` as a replay; the radius and datum are exactly equal. Both label C^1 preview-only, and both reject a kernel switch after `D` is known.

**Contract binding.** Both checkers verify the contract snapshot's sha256 before parsing. They read the target, `D` and the reference from it:
- **Forward:**
  - target: `parameters.absolute_target`, cross-checked with `preregistration.target`;
  - reference: `e^{-3s}/4`, parsed from the model string and cross-checked with the observable block;
  - `D`: from `parameters.state_bound`, compared with the gate.
- **Reverse:**
  - target: `preregistration.target.value`, compared with the selection record's "unchanged 10^-6";
  - `D`: from `parameters.state_bound`, compared with the gate;
  - reference: its calculator constants `3` and `1/4`, validated against the contract model string.

Neither checker contains the target literal `1/1000000` or the `D` numerator. This is the re-run the Jung assistant asked for. The only `1e-6` occurrences are float-rejection probes. The reverse calculator holds the cap `D` only as an equality check on its formula.

**All 24 controls.** Both checkers implement every contract control as a damaging mutation that must raise:
- forward: 68 recorded rejections, and the run aborts if any control lacks one;
- reverse: 80 rejections, every entry `kind: damaging_mutation_control`.

## The pre-registration mirror discrepancy

`controls` has 24 ids, and `preregistration.controls_required.ids` has 23. The missing id is **`c1_window_preview_only`**: the 24th control, defined in required item 10 and in `new_control_semantics`.

**Both producers implemented it anyway, as damaging mutations:**
- forward: `kernel_switch_to_C1`, `calculator_C1_certificate` and `calculator_poisson_certificate`;
- reverse: `kernel_switch_after_D_known`, `calculator_c1_certificate` and `c1_residue_modulus`.

Neither checker relies on the 23-id mirror:
- the forward iterates `contract['controls']` and never reads `controls_required`;
- the reverse iterates `contract['controls']` and requires only that the mirror be a subset.

**Who found it.**
- I recorded the defect before production (`av2-contract-review.md` item 1).
- The Jung/Pauli assistant found it independently (`experts/jung/assistant-1/README.md`, audit item 4).
- The lens's own loop-3 sign-off had described the mirror as "`=controls`", which is inaccurate for AV2.

**Consequence.** This is a non-blocking clerical defect, and the frozen contract is not amended. `tools/freeze_contract.py` now refuses a contract whose mirror differs from its controls (commit `2e1bfc8`, 22:23:19Z, after this contract froze). All eight Round32 draft contracts now have equal mirrors. `freeze.py`, which binds the producer closures, is unchanged since 21:05Z.

## Replays, closures and isolation

**Replays.** `replay_loop.py av2` (the same output under normal and `-O` Python) verifies both closures and replays each producer under normal and `-O` into fresh external directories. All four runs reproduce `output/` byte for byte:

| Output | sha256 |
|---|---|
| forward `results.json` | `ebfe372a…94fc` |
| reverse `results.json` | `f47b977f…7932` |

**Freeze.** `python3 -B research/round32/tools/freeze.py verify` returns `verified` for both directions. The closures have 35 (forward) and 32 (reverse) files, and every premise snapshot equals its repository source.

**Isolation.** The reverse `inputs/` inventory is exactly AGENTS.md, the contract and the 25 `shared_premises`, 27 files in all. It contains no forward-only premise, no `skeptic/av2*`, no expert or deliberation file, and no forward AV2 file. The forward inventory is those 27 files plus the three `forward_additional_premises`.

**Mutation harness.** An unmutated copy of each closure reproduces the frozen `results.json` exactly. Each of 24 source edits aborts at the intended check, and every abort reason is recorded:
- calculator edits: state term `D/2`, mean square dropped, `pi` direction flipped (forward), Duhamel factor 2 dropped, a C^2 coefficient changed, the AV1 coefficient doubled, `M_0=1` (reverse), C^1 admitted as a certificate kernel (reverse);
- checker edits: sign convention flipped, free atom read at `-3`, a residue-window coefficient, `grid_claim` true, Poisson floor halved, C^1 `M_0` in the radius;
- input edits: contract target relaxed, an undeclared input added.

## Blocking issues

None.

## Non-blocking findings (the gate should not repeat the quoted sentences)

**N1. Mirror discrepancy.** See the section above. It is clerical, and both producers executed the missing id.

**N2. Two exact radii.** The datum is identical, but the exact radii differ by `2.520e-41`, because the producers rounded the kernel term differently:
- the forward divides exactly by its Machin `pi_lo`, whose arctangents were rounded to `10^-40` before scaling, so `pi-pi_lo<2e-39`;
- the reverse rounds `49|tau|/floor_{10^-40}(pi)` up to the `10^-40` grid.

Both are valid and within `5.1e-41` of the exact `E`. The gate should quote one directed value, either the common `R` above or one producer's exact rational named as such, and should not assert exact-rational equality.

**N3. Forward sign control.** The forward's sign control reads the free atom through the inversion identity, as the multiplier `g(±3)`, rather than through its half-line transform. The transform's own convention is fixed by F09 (`∫_0^∞e^{-sx}e^{-i theta x}dx=1/(s+i theta)`), and the reverse evaluates the mirrored atom through its residue engine. Both meet my contract-review item 6.

**N4. Forward shift expectation.** The forward writes: "The centered shift is expected to be `O(tau^2)` (triage (c)3)". It is labelled not used, and it is not admitted: first-order vanishing is AW1's obligation.

**N5. Forward premise-isolation control.** The forward's `reverse_premise_isolation` control mutates the contract-declared lists. The forward cannot see the reverse inventory, so the actual enforcement is the reverse's `validate_inventory`, `freeze.py` and `replay_loop.py` (27 files, verified here).

**N6. Tier-(i) previews.** The forward exports only a lower value for the tier-(i) window radius, `2D_i+49|tau|/pi_hi` (~4.7517e-5, omitting `2D_i^2`), and labels it. The full value is `4.751779428e-5`, which the reverse reports. The contract's "3.6–4.7e-5" preview is slightly low (reverse finding 1). All of these fail `10^-6`, and the tier is retained as limited.

**N7. Reverse reference source.** The reverse takes the reference constants `3` and `1/4` from its calculator and validates them against the contract rather than parsing them from it. Its fixed design admits only `+tau`, and `-tau` is replayed in reusable mode. Neither affects any number.

**N8. Undeclared reads.** Both producers disclose reads outside `inputs/` for protocol and code style:
- `tools/README.md` and `tools/freeze.py`;
- AT5 `check.py`;
- their own direction's AV1 `check.py`.

None carries premise weight, and no current counterpart or `skeptic/av2*` file was read.

## Limitations

- **Scope.** Only this family, the cover `R`, fixed spacing and the single node `s=1` at `tau=±10^-8` are covered. Nothing transfers to nonzero selected triples, uniform Wilson theory, weak coupling or the continuum.
- **Upper certificate only.** The free value lies inside the interval (`reference_unresolved`). No interaction shift, sign or coefficient of `C(s)` is claimed. AV2 is not evidence for or against first-order vanishing.
- **Each AQ1 subsequential state separately.** There is no uniqueness, whole-sequence convergence or rate in `N`. The `-tau` value is a replay of the same `|tau|` formula.
- **Inherited without re-proof:**
  - AQ1's construction, `G>=0`, the GNS implementation and local norm dynamics on compact `theta` intervals;
  - AT4 F10–F12 (restated);
  - AV1's `D` and its passage to AQ limits;
  - the I1 dictionary.

  Fourier inversion and Fubini are cited, not machine-checked.
- **Independence.** The window, transform and constants are frozen shared premises. The forward read my triage and loop-2 response, which contain the moment integrals. The reverse read `skeptic/av1.md`, which states the radius formula. Independence covers only the derivation routes, the code and the controls.
- **Crossover.** `s*` is the crossover of the analytic formula, not a node certificate. At `s*` the free value (<1.9e-9) is about 500 times smaller than the radius.
- **Priority.** Scientific priority is unverified.

## Next-decision advice for AW1 (planning only; nothing here is executed)

1. **Do not cite AV2 for the parity theorem.** The AV2 interval contains `e^{-3}/4`, and its radius is about 2600 times `|tau|/144`. AW1 item 1 must come from the Peter–Weyl character count, not from AV2.
2. **The minus-tau replay is not evidence for the flip lemma.** It is equal by construction, since only `|tau|` enters. The evenness of `C` in `tau` and the oddness of `omega(W)` must come from the flip lemma, passed to AQ limits as a whole-set statement.
3. **Make sign controls read signed values.** In AV2, `theta->-theta` left `|ghat|`, `M_j` and `E` unchanged, and only the free-atom datum exposed it. AW1's `sign_convention_fixture` and `sign_flip_tau` must evaluate a signed quantity, such as the first-order coefficient on a small fixture, and require the sign to flip under `tau->-tau`, not only its magnitude.
4. **Keep the same state premise and tier discipline.** Bind `D_ii(fwd)` from the AV1 gate. `K_2^+` must be at the exact tier, with no tier mixing. `D` is not a calculator input. Target and `tau` rules are read from the hash-checked contract. The AW2 coupling rule is evaluated inside the checker from the AW1 gate.
5. **Pre-register the rounding grid.** Declare one outward grid (for example `10^-40`) for `K_2^+` and the sign margin, so that the gate quotes one directed value. AV2 shows two correct producers give exact rationals that differ at `10^-41`.
6. **Freeze with the enforcing tool.** Freeze AW1 with `freeze_contract.py`, which now enforces mirror equality; AW1's draft has 30=30. Both checkers should require equality, not the subset test.
7. **Later loop, not AW1.** The C^2 window's finite `M_2=2s^2` makes a second-order Dyson refinement well defined; the C^1 window's `M_2` is infinite. The dynamics term is 85% of the radius. Any such refinement needs its own contract, and it resolves nothing unless it excludes `e^{-3}/4`.
