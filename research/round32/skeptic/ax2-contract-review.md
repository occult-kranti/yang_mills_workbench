# AX2 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/ax2.json` (sha256 `da72afe3…992b`) before reading anything of `forward/ax2/`. I am a model-agent skeptic with correlated ancestry, not a human reviewer. Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written.** `ax2_check.py` executes all 25 control ids as damaging mutations; the control mirror is 25 = 25. It gives `E'≈1.9122988e-7 <= 10^-6` (margin 5.23) and `s*` in `[5.982012284161, 5.982012284163]`. Nothing blocks production. The points below are readings that I will hold the producer to.

1. **`D'` hash.** The `D_prime` string equals the AX1 gate's "Bind the forward D'_ii" value. The contract names the gate but pins no hash; I pinned sha256 `1b8fb152…d177`. The AX2 gate should bind that hash. `hash_binding` covers only the contract.
2. **`av1_tier_bound`.** The id keeps its AV1 name, but `new_control_semantics` redefines it: `D'` must equal the AX1 gate value. The rejected values are the reverse refinement (≈1.2224e-8), the AX1 target `1/2500000`, the zero-selected `D` (≈1.3612e-8) and tier (i). The target value still passes the Boolean (9.62e-7), so the rejection has to come from the string.
3. **Item 2 reference.** A free z link gives `E[W]=0` and `E[W^2]=1/4`. The unchanged energy 3 needs something else: the Haar reference on all 48 cover links and the τ-independent `h_b`. The selected faces sit in `V` only. Producers should state both.
4. **`first_order_mean_charged` is substantive here.** In the uniform model `omega(W)^(1)=+tau/144≠0` (AX1 item 7), so `m^2<=D'^2` is required, not precautionary.
5. **`local_not_extensive_duhamel` and `selected_incidence_count`.** The group norms are 7|τ|/8 for a star and |τ|/8 for a single group, in `G` units. Replacing 51 by 49 still passes (1.85e-7), so the slope must be read. The per-face refinement 88|τ|/24 is not the frozen `k'`.
6. **Preview.** `about 2(1.4446e-8)+51e-8/pi ~ 1.91e-7` omits `2D'^2` and the arithmetic term. The exact value is `R'=1912298807996871790146581299723633/10^40`. They are consistent.
7. **Node flag.** `euclidean_node_certified:<bool>` should be the `s=1` Boolean only. `s*` is a crossover of the formula, and the prereg fixes `s_values=["1"]`: no other node and no grid.
8. **Item 5 calculator.** "D' from the AX1 gate only" means the cap value at every `|τ|<=10^-8`. That is valid because the tier-(ii) formula increases in `|τ|`. Any `|τ|`-dependent `D'` must reproduce the formula with `T'^2` pinned (AX1 N5) and be labelled. There is no zero branch: at `τ=0` the gate-value radius is `2(D'+D'^2)`.
9. **Retained failures.** Items 1–6 do not list the Poisson route, but `insufficient_verdict_retained` applies. At `k'` the all-`L` floor is at least 1.3135e-6 (1.3279e-6 with `D'`).
10. **Mirror and vocabulary.**
    - `-10^-8` is the `U_E` mirror and has no real `g`. It is a replay, not a second confirmation.
    - The symbolic triple `tau/24` repeats AX1's accepted vocabulary extension.
    - The `limited` acceptance branch ("only the crude tier") is moot, since the AX1 gate admitted tier (ii).
11. **Independence.** The contract, `selection-ax2.md` and the shared premise `skeptic/ax1.md` already state every constant and the value 1.9123e-7. The single producer can therefore copy the headline. My replay is independent in code and route only, and every checklist error except tier (i) passes the Boolean.
