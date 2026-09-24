# AW2 contract review (skeptic, pre-comparison)

**Standing.** Written from the frozen `contracts/aw2.json` (sha256 `aa559b18…68f9`) before the forward AW2 package was read. I am a model-agent skeptic with correlated ancestry, and the bound `K_2^+` is my own AW1 itemization. Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written.** `aw2_check.py` runs all 23 control ids as damaging mutations. The control mirror equals the preregistration list (23=23; no AV2-type clerical gap). Expected outcome: `accepted_within_scope`, sub-label `static_not_dynamic`. There are no blocking defects.

1. **Target versus rule.** The target `m>=2` is equivalent to `s=1/(144K|tau|)>=3` (`K|tau|<=1/432`), but the AW1 rule `K|tau|<=1/288` gives only `s>=2` (`m>=1`). So the rule does not imply acceptance; the limited band `m in [1,2)` covers the gap. At the cap `m≈206.00005` and `s≈207.00005`. A producer must report 206.00005 as the exclusion margin, not 207 and not 103.5 (the ratio to 1/288).
2. **Gate hash.** The AW1 gate is a declared premise, but the contract records no gate sha256. My checker pins `647dc337…41ae` and verifies the gate's binding chain (I1, AW1 contract, AV1 gate, `skeptic/aw1.json`). The gate should compare the producer's snapshot against that pin.
3. **Literal coupling.** `parameters.tau_AW2` and `preregistration.tau.value` both carry the literal `1/100000000`. Reading either as an input violates `aw2_coupling_rule_prefrozen`. It may be compared only after the rule has run on the gate's `K_2^+`.
4. **Item 4 checks with no id of their own** run under listed ids: sign convention (flipped `phi_b` string and fixture) under `wilson_mean_first_order_coefficient`; boundary/state (`N=2` and `N=7` equal, `N=1` rejected) under `root_n_misuse`; centring under `vector_versus_scalar_centering`; arithmetic under `exact_arithmetic_admission` and `tau_scaling_exponent`; reverse isolation, stated as not applicable, under `single_producer_declared`.
5. **Arb/mpmath preview.** It is optional. This standard-library replay uses labelled float previews, and any Arb/mpmath output must stay outside the admission Booleans.
6. **The `-tau` enclosure.** AW1 gate item (4) bounds `r` at `-tau` directly, so the mirrored interval is both a formula instance and the flip image. Neither is independent evidence, and it must be labelled a replay.
7. **`resolved_interaction_shift:true`** refers to `omega(W)` only. Because the claim exclusions forbid "a correlation shift", the packet should also carry `centered_correlation_shift_resolved:false`; mine does.
8. **"Whole set of AQ1 subsequential limits"** means every state in `S(tau)` obeys the enclosure. It makes no uniqueness claim, and pointwise `-tau` correspondence holds only along a common subsequence.
9. **Outward ceiling.** It widens the endpoints by less than `10^-28` (`(ceiling-K)·tau^2`) and changes no decision. The exact gate rational stays the headline.
