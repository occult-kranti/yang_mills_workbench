# Historical lens (Newton/Tesla), deliberation loop 3 objection pass

2026-09-23. Read `deliberation-2.md`, `deliberation-3.md`, `plan.json`, `contracts/av1.json`, `contracts/av2.json`, own `loop2-response.md`. No endorsement, no invented quotation.

## 1. Sign-off / veto

- **Plan v2: sign-off.** Sub-round order and content match `loop2-response.md` section 4; AZ2 is labelled "a different finite model" and kept out of AY's path, resolving my loop-2 concern without needing a reorder.
- **AV1: sign-off.** 49-faces-per-factor tier, self-consistent `t<=t_1/(1-352J)`, forward/reverse route split (product-ordering vs. vacuum-overlap/AT4-F08), reverse premise isolation and `D_ii<=4/10^7` all match my recommendation; the `(R+)^2` over-count I flagged in loop 2 is correctly retired via `face_count_all_sites`/`tier_mixing_rejected`.
- **AV2: sign-off.** C^2 window frozen, `reference_unresolved` label, `k=49|tau|/4`, retained Poisson controls (L=10^4 and the 1.2651e-6 floor) and the `av1_tier_bound` control match the S3 budget below; no veto.

## 2. Method notes for freezing (deliberation-3 "Skill updates" 1-2)

1. **Newton (confirmed, edited):** Compute the first-order coefficient of the target observable exactly from the frozen Hamiltonian's representation content before charging a first-order error budget; if it vanishes, freeze a second-order contract rather than renegotiate the target. A local trace-norm bound alone identifies neither the state nor a remainder's sign; a failed certificate is retained data, not a lower bound.
2. **Tesla (confirmed, edited):** Name the source (stars), the load (cover), the clock and the transfer element (kernel) with their exact constants before evaluating; leakage is loss of summability, so weight the norm — only for multi-polymer or boundary-decay claims (AY), never as a per-site maximum summed over the AV cover. The `+tau/-tau` mirror is a control, not a magnitude estimate.

## 3. Assistant scripts after sub-round 1 (pass/fail)

- S1 `haar_parity_exact.py`: exact SU(2) character/Peter-Weyl values assembling `T_1(theta)=0` under I1.5's convention. Pass iff every value is the stated exact rational and `omega_0(W)=0, omega_0(W^2)=1/4` reproduce AV1's `reference_moments`; fail on any float or Monte Carlo step.
- S2 `am2_tiers_exact.py` (Fraction): enumerate 49 faces/factor and owner sets, derive `||c^(1)||_a=49|tau|/144` and the self-consistent `t`. Pass iff `D_ii<=4/10^7` at both signs at `tau=10^-8` and the `tau->tau/100` ratio of `D_ii` falls in `[99,101]` against `[9.9,10.1]` for the AT4 sqrt bound; fail if tier (i) is substituted for tier (ii).
- S3 `window_kernel_budget.py` (Fraction, directed `pi`): assemble `E=M_0(D+D^2)+k*M_1` from AV1's admitted `D`. Pass iff `E<1e-6` at tier (ii) (expect 1.7-2.0e-7), `E>1e-6` at tier (i) (expect 3.6-4.7e-5, reported "limited"), crossover `s*` in `[6.1,6.3]`, and the L=10^4 Poisson radius (~8.415e-4) and 1.2651e-6 floor reproduced as rejected controls.

## 4. Remaining disagreement

- None on plan v2 or AV1/AV2. Non-blocking preference retained from loop 2: I would still schedule AZ2 immediately after AW1 rather than after AY, but plan v2's ordering and finite-model label make this a scheduling preference, not an objection.
