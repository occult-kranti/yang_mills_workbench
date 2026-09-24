# AY2 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/ay2.json` (sha256 `8e55e8e9…6b38`, frozen 2026-09-24T03:09:12Z) before reading anything of the AY2 producer. From `research/round32/forward/ay2/` I saw only file names: the 23 files in `inputs/`, and, in `git status` runs after this package was written, the untracked producer paths `check.py`, `report.md`, `freeze.json` and `output/`. I opened none of them. I am a model-agent skeptic with correlated ancestry, and this is not human review. Three of my own files seeded the statement AY2 is asked to make:
- my triage goal-4 note;
- my AY1 review, which is a shared premise; its "Advice for AY2" lists the obligations and names a Yarotsky-type candidate;
- my AY1 pre-comparison package, which first printed the two-sided tier.

Human author: Hruday N M (BUNZEEY).

**Verdict: executable as written, with the readings below.** Nothing blocks production. `ay2_check.py` has 82 checks and 29 controls: the 21 contract ids plus 8 extra. Its 88 rejected mutations include 73 inside the 21 contract controls. The control mirror matches (`controls` = `preregistration.controls_required.ids`, 21 = 21), and both new ids, `lower_bound_is_static_not_dynamic` and `obligations_table_complete`, are present. The checker confirms:

| Item | Value (previews; exact rationals in `ay2-independent/results.json`) |
|---|---|
| AY1 gate `2D` / `K_2'` / `2K_2'tau^2` / `K_2^+` | 2.72249057405e-8 / 13417.5275440 / 2.68350550880e-12 / 3354.80322946, read from the hash-pinned gate and recomputed from the gate's own item formula |
| `||rho^(1)_R||_1` | `sqrt(10)|tau|/72` ≈ 4.392052305789e-10. The Gram matrix of `{Omega_R, 2W_f Omega_R}` is the identity (explicit Haar integration), and the characteristic polynomial is `lambda^9(lambda^2-10/20736)` per unit `tau` |
| Two-sided tier `first_order_distance_from_product` | `[4.378634778245e-10, 4.405469833333e-10]`, with `sqrt(10)` bracketed to `10^-40` and directed outward |
| Relative width `2K_2'tau^2/(sqrt(10)|tau|/72)` | 6.1099124554e-3 ≤ 1/100, margin 1.63668 |
| `±tau` separation | at least 8.757269556e-10; each limit lies within D of `P_R` (upper tier end ≈ 0.0324 D) |
| Falsifying-scenario fixture | two admissible densities on `H_R` 2.683505306e-12 apart, which is 0.99999992 of `2K_2'tau^2` |

**Readings and wording defects.** All are non-blocking.

1. **The target is well-posed and is met by construction.**
   - **Reading.** Take "tier width relative to its centre" as full width over centre, `2K_2'tau^2/(sqrt(10)|tau|/72) = 144K_2'|tau|/sqrt(10)`. That is the preregistration note's formula.
   - **Value.** 6.10991e-3, with directed bracket `[rw_lo, rw_hi]` in the results. The half-width reading gives 3.05496e-3. Both pass.
   - **Exact decision.** The Boolean needs no bracket, because it is equivalent to `(14400 K_2'|tau|)^2 <= 10`. The left side is ≈ 3.7331.
   - **Informativeness.** It passes with margin 1.6367. The first-order term exceeds the remainder by a factor of 327.34.
   - **Limits of the target.**
     - The note already prints "about 6e-3", so the target checks feasibility, not an unknown outcome.
     - It fails only if `K_2' >= 21960.26`.
     - It cannot separate `K_2'` from `K_2^+` (1.53e-3) or from the labelled √2 variant (≈ 9487.95). Those errors need their own controls (`tier_mixing_rejected`).
     - It does catch the pair constant used as the half-width (1.222e-2 > 1/100) and a double-counted τ, which makes the lower end vacuous.
   - A source edit that replaces 14400 by 20000 in the Boolean still passes. The value has to be read, not only the Boolean.
2. **Which AY1 item bounds the single-state remainder.**
   - The bound `||rho_R-P_R-rho^(1)_R||_1 <= K_2'tau^2`, for every subsequential limit of either family, is admitted in the AY1 gate **`accepted`** field, items (2)–(3).
   - It is proved in AY1 forward (HNM-AY1-F11 with F13–F14) and in AY1 reverse §3.5–3.7.
   - The gate's `decision` item (4) binds only the pair form, printed as `||rho_R-rho'_R-0||_1 <= 2K_2' tau^2` (the `-0` is typographical).
   - The tier must cite `accepted`. Using `2K_2'tau^2` as the half-width is valid but is not the contract tier. Using `K_2'tau^2/2` is invalid.
3. **The τ convention.** The gate and the contract include τ in `rho^(1)_R = (tau/72)Σ…`. AY1 reverse (HNM-AY1-R01) writes a τ-free operator and uses `tau·rho^(1)_R`. A packet that mixes the two conventions counts τ twice. Its first-order term is then ≈ 4.4e-18, and the lower tier end is negative, so the tier says nothing.
4. **`selected_after` is the unfilled placeholder `"<preceding gate>"`.** Every earlier frozen Round32 contract names its preceding gate here; this one should read `research/round32/advisor/ay1-gate.json`. The selection note and the premise list make the intent unambiguous. The AZ1 and AZ2 drafts carry the same placeholder and should be filled before they freeze.
5. **The mandatory sentence template is missing from the frozen AY2 preregistration.**
   - Item 1 mandates "the mandatory sentence template", but the AY2 preregistration, unlike AY1's, has no `mandatory_sentence_template` field.
   - The template appears verbatim in the AY1 gate `accepted` text, which is a snapshotted premise. The checker confirms it equals the hash-pinned AY1 contract string.
   - The producer should quote it from the gate.
6. **Item 2: "Lieb–Robinson locality argument with the AM2 constants".** AM2 supplies the finite-volume gap and the creation fixed point, not Lieb–Robinson constants. The Lieb–Robinson constants are AQ1's Nachtergaele–Sims constants (HNM-AQ1.3):
   - `F(r)=(1+r)^-4` on the l1 metric;
   - `||F||<=7`;
   - `C_F<=224`;
   - `||Phi||_F<=81J<=2268|tau|`.

   For F2 there is also `||Phi'||_F<=81·49|tau|/3=1323|tau|` (AY1 reverse, named only). With these constants the algebraic-dynamics comparison looks writable (my derivation §9, row 5). The producer should name the AQ1 constants. My validator has an extra, reading-level control (`dynamics_route_constants_named`) for this.
7. **Item 2, HTW and Dobrushin routes.**
   - **HTW** is Henheik–Teufel–Wessel, LMP 112 (2022), Thm 7, which restates Yarotsky 2005 Thm 2. Its constants `c_1`, `c_2` and the smallness `c_HTW(1,1)` are existential. The AM2 gate says AM2 does not evaluate them.
   - **Precedent.** Round29 AN1/AN2 applied this route with those constants unevaluated. The AN gates are not AY2 premises, and AQ1 deliberately used no HTW smallness. So "HTW-type local stability with evaluated constants" names a missing premise, not an available one.
   - **Dobrushin.** A Dobrushin-type condition is a classical Gibbs criterion. It needs a Euclidean path-space representation that no premise supplies.
8. **Item 3: "both lie within 2D of the product".**
   - Each subsequential limit lies within **D** of `P_R` (AV1 tier (ii)). Two limits are within 2D of each other.
   - The contract's "at least 8.7e-10" is a rounded-down preview of `sqrt(10)|tau|/36 - 2K_2'tau^2` ≈ 8.7573e-10.
   - The `±tau` limits are at different couplings. Comparing them is a `common_clock` control, not a boundary comparison.
9. **`error_terms_itemized`: "K_2' tau^2 … (single state versus product)".** `K_2'tau^2` bounds a single state against `P_R + rho^(1)_R`, not against the product. The √10 bracket slack, the arithmetic term, is folded into the first-order entry. It should be reported: at most `10^-40|tau|/72` with my bracket.
10. **Item 5 and `K2_prime`: "face restriction cannot make K_2' smaller than K_2^+".**
    - This holds for trace-norm constants assembled from the AW1 items with the admitted AM2 remainder: every such constant is at least `2rho/tau^2` ≈ 6708.2 > `K_2^+`.
    - It is not an impossibility theorem about every trace-norm constant.
    - `K_2^+` is itself an R-local constant for W, uniform in N ("whole-box" is a misnomer). The W-projected R-local analogue (3354.4994) lies below it, but it is a constant for W, not a density bound.
    - The labelled variants (√2 ≈ 9487.95, 288-majorant, combined, admitted-`eps`) may appear only as previews.
11. **Premises not snapshotted.** The AY1 contract and the AV1 and AW1 gates are not AY2 inputs. `D`, `K_2^+`, the item formula and the template are all in the AY1 gate text (checked string by string). Item 5's "correct the AY1 contract wording" can be done from the gate's and `skeptic/ay1.md`'s quotations.
12. **Recurring AY1 wording items.**
    - The preregistration's `claim_exclusions` still contain "uniqueness of the AQ state" (AY1 W2); quote it only negated.
    - `gate_fields_required` lists five fields while item 6 lists ten; export all of them (AY1 W3).
    - `state_provenance` now names both families, which fixes AY1 W4.
13. **Labels.** `first_order_distance_from_product` is a tier label, not one of `sub_labels_allowed`. The loop's sub-label stays `uniform_local_closeness_not_uniqueness`. The tier carries the meaning of `static_not_dynamic` and the flags `resolved_interaction_shift`, `euclidean_node_certified` and `dynamical_claim`, all false.
14. **Scope in τ.** Item 4 says "at |tau|=10^-8". `K_2'(|tau|)` is nondecreasing (checked at τ/10, τ/100 and τ/1000), so the cap tier formula holds at every `|tau|<=10^-8`, at both signs. The first-order to remainder ratio only improves as `|tau|` decreases. The same bound also holds in every finite box of either family with `N>=2` (AY1 F14), but the contract asks only for limits.
15. **Independence.** This is a single-producer statement loop.
    - The contract, `selection-ay2.md` and the AY1 gate state every headline value, including the tier preview [4.3786e-10, 4.4055e-10] and "about 6e-3".
    - My `ay1.md` (a premise) states the obligations list.
    - The producer can therefore copy the headline. My replay is independent in code and route only: explicit Haar integration instead of the parity rule, and an exact falsifying fixture.

**Control semantics for the two new ids (as executed):**
- `lower_bound_is_static_not_dynamic` rejects any of the following:
  - the tier label changed;
  - `static:false`;
  - `resolved_interaction_shift`, `euclidean_node_certified` or `dynamical_claim` set true;
  - the lower end described as a resolved interaction shift.
- `obligations_table_complete` rejects any of the following:
  - a dropped row (each of the six);
  - an empty missing premise or candidate route;
  - a row marked "proved";
  - a duplicate row.

**Deferred parts** (executed on synthetic or reference inputs, rechecked at post-comparison):
- the producer's actual freeze and 23-file inventory;
- its actual obligations table;
- the forbidden-phrase scan of its report.
