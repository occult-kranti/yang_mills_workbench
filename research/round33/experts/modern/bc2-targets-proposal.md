# BC2 frozen-target proposal (modern lens, Round33)

**Status.** This file is advisory. It admits nothing and counts zero research loops. It is not a contract, a premise or a gate.

**Author.** Human project author: Hruday N M (BUNZEEY). This lens is a model agent whose ancestry it shares with every other agent in the round, so this is not external review.

**Distribution.**
- Sections 0–9 are written so that the advisor can copy them into the BC2 contract. They carry frozen targets and admitted values, but no previews and no margins.
- Section 10, **previews (advisor only)**, holds every preview number, margin and scaling preview. It must stay out of producer inputs.
- BC2 is **single+skeptic**. Neither the BC2 producer nor the skeptic's pre-comparison replay "from the contract alone" may receive this file. The skeptic's post-comparison review may read it.

**Read for this proposal:**
- **Round32:**
  - the AX1 and AX2 gates, in full;
  - the AX1 forward report, in full;
  - the AX1 reverse report, §§1–2 and its scope paragraph;
  - the AX2 forward report, §§1–6;
  - the AY1 and AY2 gates (`accepted`, `limitations`, `decision`);
  - the AX1/AX2 contract preregistrations (model id, state provenance).
- **Round33:**
  - the BA1, BB1 and BB2 gates, all fields except `bindings`;
  - the BA1 forward and reverse reports, in full;
  - the BB1 forward report, §§0–10;
  - the BB1 reverse report, §§0–5;
  - the BB2 forward report, §§0–5, and the BB2 reverse report, §§6–7;
  - the BB1 contract (parameters, preregistration, controls);
  - `advisor/plan.json`;
  - the skeptic's triage §(c) and its sub-round BC plan;
  - the skeptic loop-2 review, P8–P9;
  - my own `bb-targets-proposal.md`, used as the format model.
- **Constant formulas,** read for reconstruction only:
  - the BB1 constant functions (`split_constants`, `beta_star` in `reverse/bb1/check.py`; `pair_constants` in `forward/bb1/check.py`).

**How the previews were checked.** The previews in §10 come from a private exact-Fraction script (scratch, not evidence).
- Re-evaluated at route A, the script reproduces **exactly** the admitted BB1 gate constants `C` and `c_site` of both routes and the BA1 forward `K_gen = 2734375/12204185915601`.
- The route-B previews are those same formulas with the per-site sum and face count changed from `(28|tau|, 49)` to `(29|tau|, 52)`.

---

## 0. The family question (answered first)

**Is there a second named family for route B in the admitted record? No.**
- The AX1 gate (limitation 1) says the whole-star-plus-single-group box "is not identified with AL1's all-contained-plaquette boundary".
- The AX1 reverse report (§1, grouping table) names the per-face grouping "all-contained prescription: a changed boundary and changed AM2 constants". It is disclosed there and not used.
- The AY1 and AY2 gates, which admit F2 (I1 §6 all-contained-face boxes with padding), are scoped to the zero-selected family: "nothing transfers to ... the uniform route-B model".
- BA1, BB1 and BB2 are zero-selected only. BA1's `changed_model_relabelled` control rejects "uniform `J=29`".

No route-B analogue of F2 has an item-by-item AM2 verification (the AY1 H1–H5 pattern at `J' <= 29|tau|`) anywhere in the record.

**Consequence.** BC2 is **whole-sequence convergence of one family** together with **its identification with every AX1/AX2 subsequential state**, followed by the AX2 node restated for the limit. The family is the AX1 construction: the centered whole-star-plus-single-group boxes of the uniform model, route B, model id `AQ_uniform_routeB`. Call it `FB`.
- **The common-limit item is dropped.** `common_limit_claimed:false` is recorded as not applicable: there is one family.
- **Two within-prescription items replace it.** Both are cheap, exact and new:
  - **(2′a) Exhaustion within the route-B prescription.** Along every sequence of finite complete-factor route-B volumes `V_k ⊇ Lambda_{N_k}` with `N_k → ∞`, the reduced densities converge on every finite region to the same limit. This follows from comparison c5B and item 1. It is a statement **within one prescription**, not a comparison of boundary conditions.
  - **(2′b) Pointwise sign mirror.** `omega^{-tau}_∞ = omega^{tau}_∞ ∘ alpha_E` on every finite region. AX1 had this only as an equality of sets, or pointwise along a common subsequence. Whole-sequence convergence at each sign makes it pointwise.
- **Recorded as an obligation, not a BC2 item: a boundary-prescription comparison for the uniform model.** An all-contained analogue for route B would keep every face whose owner set lies in the volume, grouped at its anchor into a clipped star plus the single group. It is the natural lattice boundary of the uniform Kogut–Susskind model. It needs, before any comparison:
  - an AY1-type itemization (`J' <= 29|tau|`, `|X| <= 4`, at most 52 first-order faces per site, termination order 8, padding decoupling, cutoff-vector removal, reset);
  - its own family of source terms.

---

## 1. Parametrization (frozen before production)

**Model and signs.**
- Model id `AQ_uniform_routeB`. Label: "uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling (g^4=9.6x10^9)".
- Every face coefficient is `nu = alpha tau/24` (AL1 dictionary `tau = 96/g^4`).
- Both signs are covered, with `|tau| <= 10^-8`. The value at `-tau` is the `U_E` mirror: it has no real `g` and is a replay of the same `|tau|` formula.

**Route-B inputs, all admitted in the AX1 gate:**
- the Haar reference `h_b = 8 sum_e C_e >= 6 Q_b`, with the Haar vacuum;
- whole stars `phi_b` (21 omitted faces, norm `7|tau|`) and single-factor groups `psi_b` (3 selected faces, support `{b}`, norm at most `|tau|`);
- `J' = 29|tau|` and the re-frozen `J_0' = 29/10^8`, with `1073/175000000 < 1/64` and `319/1562500 < 1`;
- a unique ground and full-space gap at least `1/2` (normalized) in every finite complete-factor route-B volume;
- cutoff-vector removal.

**Rate and disc.**
- The headline rate is **`q = 1/64`**, with the analytic disc radius **`rho = 64|tau|`**.
- No floor pair is frozen.
- No secondary pair is frozen. If the advisor wants one, it must be labelled and its weights re-declared (§10.6); the route-A secondary weights are inadmissible under `J'`.

**Tiers and routes** (closed vocabulary; plan R10):
- **Coefficient input:** tier `exact_first_order`, route `analytic_disc` (every-site form (b)), **required**. `weighted_norm` form (a) is allowed as a labelled value only.
- **Marginal locality:** one route, `iterated_split` or `polymer_kp`. `iterated_split` is recommended because it is self-contained. `polymer_kp` is allowed only if the committed Ueltschi excerpt (`research/round33/sources/ueltschi-math-ph-0304003v3.md`, with its PDF sha256) is a declared premise; this closes the BB1 defect D2 at freeze time.
- **Whole-sequence assembly:** `nested_telescoping` or `union_comparison`, recorded in the `assembly` field, never as a route.
- **Crude tier:** `crude_majorant` is reported, never a target.

**Proof weights** (declared before any constant; each is checked admissible under `J' = 29|tau|` as an exact rational):
- `iterated_split`: creation weight `W = 1024`, `lambda = 2/W`, cardinality charge `|I| <= 8·2^{diam I}`;
- `polymer_kp`: `w = 3/q`, `v = 2/q`, `e^b = 1001/1000`, loss `w e^{4b}`.

The route-A extremal quantities are **not admissible** under `J'` and must be rejected: the disc radius `tau_* = 1/37888` and the split weight `1/(37888|tau|)`.

**Metric.** Coarse l-infinity metric on factor sites. A star has diameter 1; a single-factor group has diameter 0.

**Comparisons** (`N` is the smaller box size, `N >= 2`):
- **c1B:** `FB` on `Lambda_N` versus `Lambda_{N+1}`.
- **c4B:** any two centered boxes `Lambda_M`, `Lambda_M'` with `M, M' >= N`, compared directly.
- **c5B:** any two finite complete-factor route-B volumes both containing `Lambda_N`, compared directly. Stars must lie inside the volume; every single group of the volume is kept.

A comparison through a union volume is labelled only. BB1's c2 and c3 (F2 nested; F1 versus F2) have no route-B counterpart.

**Cutoff order.**
1. Every estimate holds in each `Q_L`, uniformly in `L`.
2. Then `L → ∞` at fixed `N` (AV1 F20–F23 with the route-B gap `1/2`).
3. Then `N`. The limits are never exchanged.

**Clock and node.** `theta = alpha t/hbar`, `s = alpha t_E/hbar`. The single node is `s = 1`, at `tau = +10^-8`.

**State provenance.** The untruncated finite-box ground vectors of `FB`, taken as a **whole sequence**; AX1/AX2 used `AQ1_centered_whole_star_subsequence`.

---

## 2. Step 1 — the coefficient input for route B (BA1 analogue, every-site form)

### (a) What changes from route A

| item | route A (BA1/BB1 admitted) | route B (AX1 admitted, or re-derived in BC2) |
|---|---|---|
| per-site interaction sum | `J = 28|tau|`, `J_0 = 7/25000000` | `J' = 29|tau|`, `J_0' = 29/10^8` (AX1) |
| interaction groups per site | 4 stars | 4 stars and 1 single-factor group (5 groups) |
| supports of interaction terms | stars (4 sites, l-infinity diameter 1); F2 clipped groups | stars and single sites (diameter 0); nothing is clipped |
| first-order faces per factor | 49 (15 owner sets) | 52 (49+3; 16 owner sets, the new one `{u}` with `n=3`) (AX1) |
| site energy of a first-order face vector | at most 18 | a selected face has all four links on one factor: site energy 24 (kept for `L >= 24`, AX1 checklist) |
| largest disc radius | `tau_* = 1/37888` | re-derived from `29 rho G(R) <= R` |
| headline disc | `rho = 64|tau|` | `rho = 64|tau|`; admissible, checked exactly under `J'` |
| circle bound `T(rho)` | `(49 rho/144)/(1 - 28 rho G'(R))` | re-derived with the route-B count and per-site sum |
| every-site constant at `q = 1/64` | `K = 49/111790368` (BA1 gate value) | `K_B`: **new; no admitted value**. The BA1 value must not be used |
| nested source terms | new whole stars (F1); new faces (F2); 28N(5N+1) extra faces (F1 vs F2) | new whole stars and new single groups on the shell; no F2 regrouping |
| order versus distance | pieces of diameter at most 1 | unchanged; single-site pieces cost one order and zero distance |

**Is `q = 1/64` still admissible with `J_0' = 29/10^8`? Yes.**
- The disc `|z| <= 64|tau|` lies far inside the route-B admissible disc.
- The producer must check the disc self-map `29 rho G(R) <= R` and the contraction `29 rho G'(R) < 1` at `rho = 64|tau|` as exact rationals, never by citing the real-coupling AX1 constants.
- `J_0'` enters only through the AX1 gate. It supplies the unique real fixed point in the AM2 ball, which identifies the disc fixed point at real `tau`, together with the gap and the cutoff removal.

### (c) Frozen target BC2-T0 (coefficient input, every-site form (b))

For every comparison c1B, c4B and c5B, both signs, every on-site cutoff space `Q_L` (constants independent of `L`), and **every site `u` of the union volume**:

`sum_{I ∋ u} ||c^A_I - c^B_I|| <= K_B q^{(N - |u|_inf)_+}`, with `q = 1/64` and **`K_B <= 1/1000000`**.

This is tier `exact_first_order`, route `analytic_disc`, disc `rho = 64|tau|`. The input is a **BC2 lemma proved in full**, never an admitted BA1 statement. A `weighted_norm` form-(a) value may be reported as labelled.

### Required derivations

1. **The complexified route-B map.**
   - Take `V(z) = z V_1`, where `V_1` holds the unit-coupling stars and single groups.
   - Re-derive the AM2 multilinear estimate item by item at complex `z`, with `sum_{X ∋ u} ||V_X(z)|| <= 29|z|`.
   - The `|X| <= 4` majorant also covers `|X| = 1`, because AM2's counting constants are monotone in `p` (AX1 F05).
   - Termination stays at order 8.
2. **Disc lemma.** State the self-map and contraction at `rho = 64|tau|` as exact rationals. The fixed point is holomorphic on the open disc and continuous on the closed one. At real `tau` it is the AX1 route-B fixed point, by AX1's uniqueness in the AM2 ball.
3. **Circle bound.** The exact first-order coefficient is `-(1/72) sum_{M_f = M} W_f Omega_0` over all retained faces, **selected faces included**. There are at most 52 faces per factor, so the l1 face sum bounds the anchored norm. The remainder is `29|w|(G(t) - 16) <= 29|w| G'(R) t`.
4. **Order versus distance** with pieces that are faces, including the selected single-site faces. The bound `n >= 1 + d` must be checked by breadth-first search on the enumerated route-B piece graph.
5. **Every-site common core for route B.** Every face, omitted or selected, with a site within `N - |u|_inf - 1` of `u` is retained by every route-B volume containing `Lambda_N`. So every source term lies at distance at least `N - |u|_inf` from `u`. The new single groups of a nested comparison lie at distance at least `N + 1 - |u|_inf`, which is never the minimum.
6. **Schwarz/Cauchy estimate at every site.** The circle bound `2T_B(rho)` is uniform in `u`, because the anchored norm is a maximum over sites. At sites outside `Lambda_N`, use `2T_B(|tau|) <= 2T_B(rho)|tau|/rho`.
7. **No reduced-density analyticity** (no zero-free region is proved), and the global Lipschitz constant is never a decay factor.

---

## 3. Step 2 — marginal locality for `FB` (BB1 analogue)

### (a) What changes from route A

- **Near term.** At first order only supports **contained in `R`** move `rho_R` (BB1 reading D1). In route B these are `{0, e_z}` (the 10 omitted faces with owner set `R`) **and the two single sites `{0}` and `{e_z}`** (the 6 selected faces): 16 faces inside `R`, as the AX1 gate says. The single-site coefficients are common to both volumes of every comparison; their differences enter only through `K_B`.
- **Straddling.** The 72 first-order straddling faces (88 meeting `R`, minus 16 inside) still have zero first-order `R`-marginal (Haar). A single-factor interaction group, and a first-order single-site creation, can never straddle any region `Y`.
- **Region-form factor.** The polymer route's step `(1+t)^{|Y|-1} <= e^{|Y|/10^8}` needs `(1+t)^2 <= 1 + 10^-8` with the route-B exact-first-order anchored bound `t` (AX1 `T'`). It must be re-checked exactly; the route-A `t` is rejected. The crude tier has no region form.
- **Weights.** Every admissibility inequality (`W <= w_max'`, `w e^{4b} <= w_max'`, `a <= 2b`, `q v > 1`, `lambda < q`) is re-evaluated with `J' = 29|tau|`.
- **Counts.** The polymer exploration counts and the split's per-site charges use creation norms only; they are unchanged in form. Any constant that uses a per-site count of interaction groups must use 5, not 4.
- **Nothing else changes.** The AV1-type decomposition, `Tr N_c >= 1`, the two Lipschitz bounds, the covering recursion and the Kotecký–Preiss verification are model-independent algebra, re-run with the route-B inputs.

### (c) Frozen targets

Each target holds for every comparison c1B, c4B and c5B, both signs, each `Q_L`, and at fixed `N` for the untruncated ground vectors.
- **BC2-T1 (R form):** `||rho^{box1}_R - rho^{box2}_R||_1 <= C_B q^{N-1}`, with `q = 1/64` and **`C_B <= 1/250000`**.
- **BC2-T2 (region form):** for every finite complete-factor region `Y ⊂ Lambda_N`, `||rho^{box1}_Y - rho^{box2}_Y||_1 <= c_site,B |Y| e^{|Y|/10^8} q^{d_Y}`, with `d_Y = N - max_{y ∈ Y}|y|_inf` and **`c_site,B <= 1/500000`**.
- Tier `exact_first_order`; route as declared. The input is BC2-T0, form (b). Union-volume forms (factor 2) are labelled only.

---

## 4. Step 3 — whole-sequence convergence and its consequences (BB2 analogue)

### (a) What changes from route A

- There is one family, so there is no common limit (§0).
- Identification is with **every AQ1-type subsequential state of the AX1 construction**: the states AX1 and AX2 quantify over, with provenance `AQ1_centered_whole_star_subsequence`.
- The inherited list is the AX1 gate's route-B re-instantiation, not AQ1/AQ2 verbatim.
- **Coarse translations** work as in BB2: a coarse translation maps `FB` volumes to `FB` volumes (stars to stars, single groups to single groups, the factor partition to itself).
- **Non-coarse fine translations differ from route A.** In the uniform model every face has the same coefficient, so every fine translation is a symmetry of the bulk Hamiltonian. It does not preserve the factor partition or the route-B grouping, so nothing follows for the limit. The route-A rejection reason ("maps a selected face to an omitted face with another coefficient") is **false** here and must not be copied. BC2 claims neither invariance nor non-invariance under non-coarse translations.
- **Correlation functions** (BB2 item 5) are **excluded.** The record has no route-B BA2: the BA2 constants were computed with `||Phi||_F <= 2268|tau|`, while route B has `||Phi'||_F <= 2349|tau|`. This is recorded as an obligation. The node (§5) does not need it.

### (c) Items and frozen targets

**Item 1 — whole-sequence Cauchy estimate** (sup over **all** `M` greater than `N`; plan contract rule). For each sign, `N >= 2`, each `Q_L` and then for the untruncated vectors:
- **BC2-T3:** `sup_{M>N} ||rho^{FB,M}_R - rho^{FB,N}_R||_1 <= C'_B q^{N-1}`, with **`C'_B <= 1/250000`**.
- **BC2-T4:** for every finite complete-factor region `Y ⊂ Lambda_N`, `sup_{M>N} ||rho^{FB,M}_Y - rho^{FB,N}_Y||_1 <= c'_site,B |Y| e^{|Y|/10^8} q^{d_Y}`, with **`c'_site,B <= 1/400000`**.
- **Evaluation.** Both are evaluated **at the constants proved in this packet**. BC2 is one packet, so there is no hypothesis layer and no `conditional_on_targets` semantics. The limit `rho^∞_Y` exists on every finite region by trace-class completeness, without compactness.

**Item 2′a — exhaustion within the prescription.** For every sequence of finite complete-factor route-B volumes `V_k ⊇ Lambda_{N_k}` with `N_k → ∞`, and every finite `Y`:

`||rho^{V_k}_Y - rho^∞_Y||_1 <= (c_site,B + c'_site,B) |Y| e^{|Y|/10^8} q^{N_k - max_{y ∈ Y}|y|_inf}`.

This uses c5B and item 1. The wording is "the same limit along every exhausting sequence of finite complete-factor volumes of the route-B prescription". It never compares boundary conditions.

**Item 2′b — pointwise sign mirror.**
- In every box and every cutoff, `rho_{N,Y}(-tau) = U_{E,Y} rho_{N,Y}(tau) U_{E,Y}^*` (AX1 F19–F20, extended from `R` to every finite `Y`).
- Hence `omega^{-tau}_∞ = omega^{tau}_∞ ∘ alpha_E` on every finite region, and `omega^{-tau}_∞(W) = -omega^{tau}_∞(W)`.
- The mirror is not a second real-`g` coupling.

**Item 3 — identification, then inheritance, in that order.**
- Every AQ1-type subsequential state of `FB`, at each sign, equals `omega^B_∞` on every finite region, and hence on the quasi-local algebra.
- The limit then inherits exactly what the AX1 gate admits for those states:
  - compact local trace-norm construction, and stationarity under the route-B AQ1 dynamics (Nachtergaele–Sims, `||Phi'||_F <= 2349|tau|`);
  - strongly continuous GNS evolution and a nonnegative physical generator;
  - gauge averaging, and the physical gap `alpha/16` on the invariant-local cyclic completion (the full-GNS strengthening only as qualified in the AQ2 gate and re-applied in AX1);
  - the Wilson variance floor `61999/250000`, through the Haar gap six;
  - `||rho_R - P_R||_1 <= D'`, `|omega(W)| <= D'`, `|omega(W^2) - 1/4| <= D'/2` and `m^2 <= D'^2`, with the AX1 gate forward `D'`.
- **Not inherited:** a uniform `K_2`, a uniform `omega(W^2)` constant, a Wilson-mean sign, and anything about states outside the construction.

**Item 4 — coarse translation invariance.**
- For every coarse `v` and `N >= |v|_inf + 2`: `||rho^{Lambda_N+v}_R - rho^{Lambda_N}_R||_1 <= C_B q^{N-|v|_inf-1}` (c5B, direct, factor 1). No separate target is frozen.
- The region form gives invariance of the limit on every finite region.

**Item 5 — excluded.** Correlation functions on compact windows. Obligation: a route-B BA2 re-instantiation.

**Alternative, not recommended.** If the advisor prefers BB2's hypothesis layer, freeze `C'_B <= 1/100000` and `c'_site,B <= 1/200000`, evaluated at the T1/T2 targets. The `tau → tau/100` check then becomes non-discriminating (ratio exactly 1), as BB2 recorded.

---

## 5. Step 4 — the AX2 node certificate restated for the limit (item f)

**Statement to restate.** In the uniform model at `tau = +10^-8`, node `s = 1`, original xz Wilson loop `W`, cover `R`, clock `s = alpha t_E/hbar`, `G = H/alpha`, the limit `omega^B_∞` of the named construction satisfies

`|C_∞(1) - d| <= r <= R'`,

with the AX2 gate's exact datum `d = 497870683678639429793424156500617766317/(4·10^40)` and radius `R' = 1912298807996871790146581299723633/10^40`. So `C_∞(1)` lies in `[99572606896681488461252714035083774357/(8·10^39), 497878332873871417280584742825816660849/(4·10^40)]`, against the unchanged `10^-6` target. The free value `e^{-3}/4` lies inside the interval (`reference_unresolved`).

**Frozen target BC2-T5.**
- `d` and `R'` must **equal** the AX2 gate rationals, read by hash.
- The replay of the AX2 calculator uses the gate-bound `D'`, `k' = 51|tau|/4`, `M_0 = 2` and `M_1 = 4s/pi`, and must return them exactly.
- No re-derived radius, smaller or larger, is the headline.

**Why the restatement holds.** AX2 is proved for **every** AX1 subsequential state, each separately. BC2 item 3 identifies the limit with each of them, so the set of subsequential states is `{omega^B_∞}`, and the certificate holds for the limit with unchanged datum and radius.

**What else is needed. Nothing beyond BC2 items 1–3, provided that:**
1. **The identification is of states on the quasi-local algebra, on every finite region, not only on `R`.** `C(1)` depends on the whole state through `alpha_theta(W)` and the GNS generator. A limit proved on `R` alone does not carry the node. The region form (T2/T4) is therefore load-bearing for §5.
2. **The finite-box states are the same objects AX1 used:** the untruncated ground vectors of the centered whole-star-plus-single-group boxes, with the cutoff removed at fixed `N` before `N → ∞`. A convergence proved only inside each `Q_L` does not identify.
3. **The four AV2-lemma hypotheses are inherited, not re-proved.** `G >= 0` and a finite `eta` hold for the identified state (AQ1 nonnegativity as re-applied in AX1). Inversion and Fubini depend on `g` alone.
4. **The state term `D'` holds for the limit** in either way: through "every subsequential limit" (AX1 item 6), or directly, because every finite box satisfies the AX1 state lemma and the closed trace-norm ball passes to the whole-sequence limit. The slope `k'` concerns the state-independent route-B limit dynamics (AX1 item 3), which is unchanged.

**What is not needed:**
- a route-B BA2 or any dynamics comparison between boxes;
- a rate in `N`;
- a common limit;
- uniqueness;
- a uniform `K_2`.

**Excluded strengthenings:**
- **Convergence of the finite-box nodes, `C_N(1) → C_∞(1)`.** This needs a route-B dynamics comparison and control of the window tail over all real `theta`; state convergence on finite regions does not give it.
- **Any node other than `s = 1`.**
- **An interaction shift, sign or coefficient of `C(s)`.**
- **A certified node at `-tau`.** The mirror gives `C^{-tau}_∞(1) = C^{tau}_∞(1)` exactly, but this is a replay, not a second observation.

---

## 6. Scaling brackets `tau → tau/100` (item d; declared before production)

| constant | tau order | bracket | note |
|---|---|---|---|
| `K_B` (T0) | linear | `[95,105]` | the positive nonlinear correction comes from `1/(1 - 29 rho G'(R))` |
| `C_B`, `c_site,B` (T1, T2) | linear | `[95,105]` | governed by `K_B` (the near term dominates) |
| `C'_B`, `c'_site,B` (T3, T4) | linear | `[95,105]` | only at the packet's own proved constants; the hypothesis-layer alternative gives exactly 1 (non-discriminating) |
| labelled `weighted_norm` `K_own,B` | linear | `[95,105]` | labelled only |
| `q = 1/64`, `rho/|tau| = 64` | fixed | exactly 1 | frozen |
| node datum `d` | independent | exactly 1 | the Haar reference and free z link are unchanged |
| node radius `R'` (replay only) | linear | `[95,105]` | gate-bound value; the ratio is recorded, not a target |
| crude tier | reported | none | never a target |

No single bracket is declared for a sum of constants of different `tau` order. The BA1 lesson applies: a quadratic refinement, for example first-order cancellation on the supports through `u`, must never be the headline under a linear bracket; it is labelled only.

---

## 7. Exact finite fixtures that must be required (item e)

Every fixture is exact (Fractions), labelled `model_is_finite_graph: true` and `transfers_to_aq: false`, and each carries a damaging mutation that `check.py` must reject.

1. **Route-B incidence and partition** (values from the AX1 gate).
   - A fine-lattice brute force puts every plaquette in exactly one group: a 21-face star or a 3-face single group.
   - `J' = 29|tau|` is attained in the bulk and lower at box boundaries.
   - 7 stars and 2 single groups meet `R`; 153 faces are charged; 88 meet `R`; 16 lie inside `R` (10 + 6); 72 straddle.
   - 52 faces per factor and 16 owner sets pass through a site; 5 interaction groups pass through a site.
   - *Rejected:* `28|tau|` (single groups dropped), 33 (double count), 32 (merged into stars), 49 faces, 96 or 168 used as exact counts, 4 groups per site.
2. **Support-one groups.**
   - A single-factor group is never clipped: it is retained in every route-B volume containing its site.
   - It never straddles any region `Y`.
   - Its first-order creation is nonzero, with norm `sqrt(3)|tau|/144` (AX1 F15).
   - In the order-versus-distance graph it costs one order and zero distance (BFS check `n >= 1 + d` on the route-B piece graph).
   - *Rejected:* a single group charged as straddling; a clipped single group; single groups omitted from the piece graph.
3. **Every-site common core and sources (route B).**
   - At every `u ∈ Lambda_N`, `N = 2, 3, 4`, every face (omitted or selected) within `N - |u|_inf - 1` of `u` is retained by every route-B volume containing `Lambda_N`, and the source distance `N - |u|_inf` is attained.
   - For the nested comparison, enumerate the new whole stars and the new single groups separately. The single groups lie on the shell and never attain the minimum distance.
   - Enumerate also general-volume examples for c4B and c5B.
   - *Rejected:* an exponent taken from the shell distance; single groups missing from the source list; old stars charged.
4. **Admissibility under `J'`** (the new core control).
   - The headline disc `64|tau|`, the split weight `W = 1024` and the polymer loss `w e^{4b}` are checked admissible as exact rationals under `J' = 29|tau|`.
   - *Rejected:*
     - the route-A disc `tau_* = 1/37888`, whose self-map exceeds `R` under `J'`;
     - the route-A secondary split weight `1/(37888|tau|)`;
     - the route-A circle bound (`49`, `28`) or the BA1 gate value `K = 49/111790368` used as the route-B input (silent route-A constants, including hard-coded `9856 = 28·352` or `37888`).
5. **First-order `R`-marginal of route B.**
   - It is derived from the 16 faces inside `R`. The route-A ten-face value `sqrt(10)|tau|/72` is rejected.
   - The 72 straddling faces have zero first-order `R`-marginal (Haar).
   - The two single-site creations move `rho_R` at first order but are common to all volumes containing `Lambda_N`.
6. **Cutoff and site energies.**
   - A selected face vector has site energy exactly 24 on one factor, so it is kept for `L >= 24` and annihilated below.
   - *Rejected:* the route-A statement "first-order site energies at most 18".
   - The Eckart `3×3` gap-`1/2` fixture is re-run. *Rejected:* swapped `N` and `L` limits.
7. **Region-form factor.** `(1+t)^2 <= 1 + 10^-8` is checked exactly with the route-B anchored bound `t`. *Rejected:* the route-A `t`; a crude-tier region form.
8. **Carried over from BB1** (model-independent algebra, re-run):
   - coefficient decay is not marginal decay (the AV1-F13 fixture);
   - second-order propagation;
   - normalization coupling, including spectator independence and the global-fidelity fixture;
   - the split Lipschitz and trace checks (`Tr N_c >= 1` on mixed outside states);
   - the covering recursion identity;
   - if `polymer_kp` is used: the polymer identity, the cardinality factor and the zero-free-region control.
9. **Whole sequence against subsequence.** *Rejected:* a one-state ball with two distinct subsequential limits called convergence; an `N → N+1` bound alone called a Cauchy estimate; inheritance ordered before identification.
10. **Translations in the uniform model.**
    - Coarse covariance of `FB` volumes is enumerated (stars, single groups, factor partition).
    - For a non-coarse fine translation, the fixture shows that the uniform bulk coefficients are preserved while the factor partition and grouping are not.
    - *Rejected:* the route-A reason ("selected maps to omitted with another coefficient") offered as the reason; any claim of invariance or of non-invariance under a non-coarse translation.
11. **Sign mirror.**
    - `U_E` covariance holds in every box and cutoff, restricted to every finite region.
    - The `3×3` compression `D H(tau,kappa) D = H(-tau,-kappa)` holds with `kappa = tau`.
    - *Rejected:* `kappa` untied from `tau` (AX1 fixture); the mirror claimed as a second real-`g` coupling.
12. **Node replay.**
    - The AX2 calculator with gate-bound inputs returns exactly `d` and `R'`.
    - *Rejected:*
      - a smaller state term for the limit (the AX1 reverse R-refinement, or any re-derived `D`);
      - the seven-star slope `49|tau|/4`;
      - a node other than `s = 1`;
      - a finite-box node-convergence claim;
      - `reference_unresolved` dropped.
13. **Model crossing.** *Rejected:*
    - the route-B limit identified with the zero-selected BB2 limit;
    - BB1/BB2 constants applied to route B;
    - the route-B boxes identified with AL1's all-contained-plaquette boundary;
    - a common-limit claim.

---

## 8. Gate fields and mandatory sentence

**Sub-labels.** Primary `convergence_of_named_constructions`. Secondary `certificate_restated_for_limit`, `transfer_to_named_model` and `reference_unresolved` (node). Not `common_limit_of_named_constructions`.

**Gate fields.**
- **True, with scopes:**
  - `whole_sequence_claimed: true`, with `whole_sequence_scope` = "reduced densities of the centered whole-star-plus-single-group construction of the uniform route-B model on every finite region";
  - `state_convergence_claimed: true`;
  - `state_decay_claimed: true`, with scope "reduced densities of route-B finite-box ground vectors on R and on regions Y, per comparison (c1B, c4B, c5B)";
  - `rate_in_N_claimed: true`;
  - `translation_invariance_claimed: true`, with scope "coarse translations; the limit of the named construction (route B)".
- **False:**
  - `common_limit_claimed` (one family; recorded as not applicable);
  - `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `continuum_claim`, `weak_coupling_claim`;
  - `gns_dynamics_equality_claimed`, `uniform_in_time_claimed`;
  - `scientific_priority_verified`.
- **AX-style flags:**
  - `uniform_wilson_claim: true`, meaning only the label;
  - `resolved_interaction_shift`, `k2_uniform_claimed` and `wilson_mean_sign_certified`: false.
- **`dynamics_level`: absent**, because item 5 is excluded. If the schema requires a value, add `none` to the plan vocabulary before freeze (R10). If item 2′a is adopted with its own field (for example `exhaustion_scope`), that field also needs a vocabulary entry before freeze.

**Suggested mandatory sentence template.** It uses the plan's required phrases verbatim, "convergence of the named constructions" and "rate in N", and contains no phrase on the forbidden list:

> For the uniform Kogut-Susskind SU(2) model at fixed spacing and strong bare coupling handled by route B, at the same coupling |tau|<=10^-8, the reduced densities of the named construction (centered whole-star-plus-single-group boxes on centered coarse cubes) converge as a whole sequence, at a rate in N, on every finite region, and to the same limit along every exhausting sequence of finite complete-factor volumes of the same prescription; this limit coincides with every AQ1 subsequential state of that construction, is invariant under coarse translations, and at tau=+10^-8 has centered Euclidean Wilson correlation C(1) within the AX2 radius of the AX2 datum at the node s=1; this is convergence of the named constructions (one family for route B), not uniqueness of any ground state, not a statement about other boundary conditions or about states outside the named construction, not weak coupling or continuum, and not a statement uniform in the lattice spacing a.

---

## 9. Risks and retained-failure outcomes (item g)

**Risks:**
1. **Silent route-A constants.** This is the main risk. The admitted checkers hard-code `28`, `49`, `9856 = 28·352` and `37888`. A producer who copies helpers computes route-A numbers under a route-B label. Fixture 4 and a pinned route-B `T_B` are the defence.
2. **Doubling variants.** A union-volume density comparison, a telescoped coefficient input, or both would roughly double `c_site,B`. That can erase the region margin. The contract must require direct comparisons, as BB1 did, and label the variants.
3. **Single-site supports.** Each of these is small, but each must be written out:
   - the D1 reading (16 faces inside `R`, not 10);
   - the site-energy-24 cutoff fact;
   - 5 groups per site;
   - the tighter room in `(1+t)^2 <= 1 + 10^-8`;
   - single sites in the piece graph.
4. **The every-site input is new.** `K_B` has no admitted value. It is a BC2 lemma that must be proved in full (disc lemma, route-B order count, route-B common core), exactly as BB1 proved form (b).
5. **No second family.** There is a risk of wording drift toward comparing boundary conditions. Item 2′a is within one prescription only, and the all-contained analogue is an obligation.
6. **Node overreach:**
   - a finite-box node-convergence claim;
   - a "sharper" radius from the reverse R-refinement;
   - a node at `-tau` counted as a second observation;
   - an interaction shift inferred while the free value lies inside the interval.
7. **Region form is load-bearing for the node.** If only the R form is proved, the limit is not identified as a state and the node cannot be restated.
8. **Single direction.** Admission rests on one producer plus the skeptic's replay from the contract. The replay must use its own code for `T_B`, `K_B`, `C_B` and `c_site,B`, not the producer's.
9. **External theorem.** If `polymer_kp` is chosen, the Kotecký–Preiss statement must come from the committed excerpt as a declared premise at freeze, not repaired post hoc as in BB1.
10. **Label drift.** Every forbidden phrase stays excluded, and "rate" is always "rate in N". The limit is "the limit of the named construction(s)". `tau < 0` is always the `U_E` mirror.

**Retained outcomes:**
- **`accepted_within_scope`:**
  - T0–T4 are proved at or below their targets, for all of c1B, c4B and c5B, both signs, each `Q_L` and the untruncated vectors;
  - items 2′a, 2′b, 3 and 4 are proved;
  - the node is restated with `d` and `R'` equal to the AX2 gate rationals.
- **`limited`:**
  - **R form only (no T2/T4):** whole-sequence convergence of `rho_R` is recorded. Items 2′a (regions), 3, 4 (regions) and §5 are dropped, and AX2 stays a statement about every subsequential state.
  - **A constant above its target while convergence still holds:** the proved constant is retained and labelled, and nothing is retuned.
  - **Convergence proved only inside each `Q_L`:** no identification, and no node restatement.
  - **Item 2′a or 2′b fails alone:** recorded, and the rest stands.
- **`insufficient`:**
  - the route-B every-site input fails;
  - or neither marginal-locality route controls the outside-state dependence for route B.

  Coefficient locality is then kept as a labelled observation. AX2 is unchanged, and the Round32 gates stay untouched.
- **Either way:** a failed route is never evidence that two states differ. Nothing is retuned: not `q`, not `rho`, not a weight, not `tau`, not the node.

---

## 10. Previews (advisor only; item b) — not for producer or skeptic-replay inputs

All values are at `|tau| = 10^-8`, as exact Fractions with truncated decimals. Both signs replay the same `|tau|` formula.

### 10.1 Route-B disc and admissibility (answers item (a) numerically)

| quantity | route A (admitted) | route B (preview) |
|---|---|---|
| largest disc radius `tau_* = R/(J/|tau| · 148/7)` | `1/37888` | `7/274688` (about `2.54835e-5`) |
| floor ratio `q_min = |tau|/tau_*` | `37888|tau|` = `148/390625` | `(274688/7)|tau|` = `1073/2734375` (about `3.92411e-4`; not frozen) |
| maximal weight `w_max = R/(J G(R))` | `390625/148` (about 2639.36) | `2734375/1073` (about 2548.35) |
| disc self-map at `rho = 64|tau|` | `148/390625` | `1073/2734375 < 1/64` |
| disc contraction at `rho = 64|tau|` | `2464/390625` | `2552/390625` (about `6.53312e-3`) |
| `T(|tau|)` (unweighted exact first order) | `49/14398580736` | `13/3599632512` (= AX1 `T'`) |
| `T(64|tau|)` | `49/223580736` | `13/55882512` (about `2.32631e-7`) |
| route-A extremal weights under `J'` | — | `29·(1/37888)·148/7 = 29/1792 > 1/64`: inadmissible |

So `q = 1/64` is admissible, with a factor of about 39.8 between `rho = 64|tau|` and the route-B `tau_*`.

### 10.2 Step 1 — the coefficient input

| constant | route A | route B preview | ratio B/A |
|---|---|---|---|
| `K` (form (b), analytic_disc, `2T(64|tau|)`) | `49/111790368` (`4.38320e-7`) | **`K_B = 13/27941256` (`4.652618e-7`)** | `20184372/19015577` (`1.061465`) |
| `K_own` (form (a), weighted_norm, `w=64`, labelled) | `19140625/86785322066496` (`2.20551e-7`) | `5078125/21686494079376` (`2.341607e-7`) | — |
| crude `2·J·64·G(R)` (reported) | `296/390625` | `2146/2734375` (`7.84823e-4`) | — |
| floor `2T(tau_*)` (not frozen) | `49/2018304` (`2.42778e-5`) | `91/3658176` (`2.48758e-5`) | — |

### 10.3 Step 2 — marginal locality (both routes at the declared weights)

| constant | route A admitted (bound / labelled) | route B `iterated_split` | route B `polymer_kp` |
|---|---|---|---|
| `C_B` | `8.90512e-7` / `8.90426e-7` | `2326328761843649826272217312701707175/2461302090348550272620124432958434944821248` (`9.451618e-7`) | `9.452589e-7` (exact fraction in the scratch output) |
| `c_site,B` | `8.76812e-7` / `8.76727e-7` | `35789673259133074250341804810795495/38457845161696098009689444264975546012832` (`9.306209e-7`) | `9.307164e-7` |

**Proof constants (route B):**
- **Split:**
  - `t_0 = 2T_B(|tau|) = 13/1799816256`;
  - `t_W = 2T_B(1024|tau|) = 26/3148137` (`8.25885e-6`);
  - `beta* = 3.30376e-5` (route A `3.10066e-5`);
  - `S_lambda = 2169/343`.
- **Polymer:**
  - `t = 13/3599632512`;
  - `w e^{4b} = 3012018012003/15625000000` (`192.769`, well below `2548.35`);
  - `Gamma = 960833745828957/48828125000000000` (`1.96779e-2`);
  - `taubar = 1629879876625/2297629980200210064` (`7.09374e-7`);
  - `kappa_0 = 2.83750e-6`.
- **Region-form check:** `2t + t^2 = 7.22296e-9 <= 10^-8` (route A `6.806e-9`).
- **Near term:** `2K_B(1+q) = 845/894120192` (`9.45063e-7`). The far-site terms are about `2.1e-4` of `C_B` (polymer).

### 10.4 Step 3 — the whole-sequence constants

| constant | nested_telescoping (`×64/63`) | union_comparison (direct c4B) |
|---|---|---|
| `C'_B` | `9.602630e-7` (polymer input), `9.601644e-7` (split input) | `= C_B` (`9.4526e-7`) |
| `c'_site,B` | `9.454897e-7` (polymer), `9.453926e-7` (split) | `= c_site,B` (`9.3072e-7`) |

The labelled union-volume fallbacks are `2C_B = 1.8905e-6` and `2c_site,B = 1.8614e-6`.

### 10.5 Margins (target over the worse plausible preview)

| target | worse preview (route) | frozen target | margin |
|---|---|---|---|
| T0 `K_B` | `4.652618e-7` (analytic_disc) | `1/1000000` | `3492657/1625000` = `2.14933` |
| T1 `C_B` | `9.452589e-7` (polymer) | `1/250000` | `4.23165` |
| T2 `c_site,B` | `9.307164e-7` (polymer) | `1/500000` | `2.14888` (binding) |
| T3 `C'_B` | `9.602630e-7` (nested, polymer input) | `1/250000` | `4.16553` |
| T4 `c'_site,B` | `9.454897e-7` (nested, polymer input) | `1/400000` | `2.64413` |
| T5 node | `R' = 1.91229880800e-7` (gate) | `10^-6` (unchanged) | `>= 5.22930` (AX2 gate) |

**Notes on the targets:**
- `c'_site,B <= 1/500000`, for parity with T2, would still give `2.11531`. I chose `1/400000` for room above the `64/63` telescoping factor.
- The hypothesis-layer alternative gives `C' = 4/984375` and `c' = 2/984375`, against `1/100000` and `1/200000`, with margin `2.46094`.
- Route B is about 6.15% above route A throughout. The BB1 region margin falls from `2.28` to `2.149`; that is still above 2, and it is the binding margin. The doubling variants of risk 2 would fail T2, which is why direct comparisons are required.

### 10.6 Optional secondary pair (not recommended; labelled if frozen)

- `q_2 = 151552|tau|` is still admissible under `J'` (its disc `1/151552` lies inside `7/274688`).
  - Coefficient input: `K_2,B = 13/2544192` (`5.10968e-6`).
  - The split weight must be re-declared, for example `W_2 = 2734375/1073` (the route-B maximum). Then `lambda/q_2 = 0.517857` and `S = 171.46`.
- Previews:

  | route | `C_2` | `c_site,2` |
  |---|---|---|
  | split | `1.03222e-5` | `1.03066e-5` |
  | polymer (loss `1987.45 <= 2548.35`, `Gamma = 0.20288`) | `1.02617e-5` | `1.02462e-5` |

- Against BB1's secondary targets `1/20000` and `1/40000`, the margins are about `4.84` and `2.43`.

### 10.7 Scaling previews (`tau → tau/100`)

| constant | ratio | inside its bracket |
|---|---|---|
| `K_B` | `39059948/388073` (`100.6510`) | yes, `[95,105]` |
| `C_B`, `c_site,B` (split) | `100.6615` | yes |
| `C_B`, `c_site,B` (polymer) | `100.6717` | yes |
| `C'_B`, `c'_site,B` (own-constant evaluation) | same as `C_B`, `c_site,B` | yes |
| `K_own,B` (labelled) | `101.306` | yes |
| node radius replay | `100.0015` | yes; `d` exactly 1 |

### 10.8 Fixture expected values (advisor cross-check; not for the contract)

- **Nested sources at `N = 2, 3, 4`:** new whole stars `152, 296, 488`; new single groups on the shell `218, 386, 602` (`(2N+3)^3 - (2N+1)^3`).
- **Route-B first-order `R`-marginal:** 16 orthogonal face vectors of norm `1/2`, a rank-two operator. Trace norm `|tau|/18` (`5.556e-10` at the cap), against route A's `sqrt(10)|tau|/72` (`4.392e-10`).
- **`D'` recomputed** from `J' = 29|tau|` and `t_1' = 52|tau|/144` equals the AX1 gate rational exactly.

**Recommendation.**
- **Freeze BC2** as single+skeptic on the one family `FB`, with:
  - **T0** `K_B <= 1/1000000`;
  - **T1** `C_B <= 1/250000`;
  - **T2** `c_site,B <= 1/500000`;
  - **T3** `C'_B <= 1/250000`;
  - **T4** `c'_site,B <= 1/400000`,

  all at `q = 1/64`, `rho = 64|tau|`, tier `exact_first_order`, and evaluated at the packet's own constants.
- **Items:** identification, coarse translations, exhaustion within the prescription and the pointwise sign mirror.
- **Node:** the AX2 certificate restated for the limit with `d` and `R'` bound by equality to the AX2 gate.
- **Drop:** the common limit and correlation functions, both recorded as obligations.

This lens admits nothing and counts zero research loops.
