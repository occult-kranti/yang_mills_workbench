# Hruday uniform local closeness of AQ-type subsequential states — AY1 reverse (vacuum-overlap / fidelity route)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted reverse production: the derivations, the checker and this report were written by Claude (an AI model) as the AY1 reverse producer, under premise isolation (`reverse_premise_isolation: true`). It is correlated model-agent work, not human review. HNM labels are project aliases.

I read the frozen contract snapshot `inputs/research/round32/contracts/ay1.json` first (sha256 `be9b354420e66e7edba03d59b3d194b69f26782b44cfb63cb10e176bf4879ae0`, verified by `check.py` before any evaluation), then `inputs/AGENTS.md` and `inputs/research/round32/advisor/selection-ay1.md`, then the other snapshots in `inputs/`. I did not open, list or read anything under `research/round32/forward/ay1/`, `research/round32/skeptic/` (outside the two snapshotted AV1/AW1 reviews in `inputs/`), `research/round32/experts/`, any `advisor/deliberation-*` or `panel*` file. Section 11 lists the non-scientific style files I read and discloses my private scratch folder.

**Attribution.** Uhlmann fidelity, the Bures angle as a metric, the Fuchs–van de Graaf inequality, the pure-state trace-distance formula, block positivity and partial-trace contractivity are standard. The commuting-creation expansion is the admitted AM2 construction (Bravyi–DiVincenzo–Loss lineage as credited there; Gauvin arXiv:2503.15539v3 A.6–A.8 as AM2's template). The padding prescription is I1 section 6. Scientific priority is unverified.

## Verdict (reverse half)

Model: the AM2/AQ1 zero-selected patterned family (label `AQ_patterned_zero_selected`), both signs of `|tau|<=10^-8`, cover `R={0,e_z}`. Two named construction families: **F1** = AQ1 centered whole-star boxes `Lambda_N`, and **F2** = I1 section-6 all-contained-face boxes with padding, `Lambda_N`, both with `N>=2`.

1. **Item 1 (both families satisfy the AV1 premises): proved.** F1 by the admitted chain I1 → AM2 → AQ1 → AV1 → AW1, cited step by step. F2 by an itemized re-application of the AM2 contraction at the same `J_0=7/25000000` to the padded interaction family: indexed supports `X_b=b+S` inside `B_+=B+S`, group norms at most `7|tau|`, per-site sum at most `28|tau|` (enumerated maximum exactly 28 on `Lambda_2`, `Lambda_3`), termination order `2|X|=8`, unchanged majorant constants, decoupled padding. The reset budget is at most `56|tau||F|` (98|tau| on R), which gives local trace-norm compactness. The two topologies are named separately: **trace norm on B(H_R)** for states, **operator norm on bounded local observables uniformly on compact time windows** for dynamics.
2. **Item 2: proved.** For any two subsequential limits (same family or different families) at the same `tau`: `||rho_R-rho'_R||_1 <= 2D`, with `D=D_ii` the AV1 admitted tier. The reverse route passes the vacuum-overlap (fidelity) identity to every limit and then uses either the trace-norm triangle through `P_R` or the Bures-angle triangle, which gives the slightly smaller `4eps/(1+eps^2)`.
   - `2D = 1170159676931825184288274812132100/42981220507576537932303142777593983768257 ≈ 2.72249057405e-8`, against the preregistered target `1/1250000` (margin ≈ 29.38).
3. **Item 3: proved.** The first-order reduced density comes from the derivative of the vacuum-overlap identity. The scalar fidelity identity kills the diagonal and excited blocks; its vector form gives the off-diagonal part:
   - `rho^(1)_R = (1/72) sum_{f in F_R} (|W_f Omega_R><Omega_R| + |Omega_R><W_f Omega_R|)`, where `F_R` is the set of 10 faces whose owner set is exactly `R`. Its trace norm is `sqrt(10)/72`, and `Tr(rho^(1)_R W)=1/144` as admitted in AW1.
   - It is the same operator for every subsequential limit of either family.
   - The R-local trace-norm remainder constant is `K_2' = 966771578474926086618624139557778885954947547760216752246561/72052885697817210754545804931891200000000000000000000000 ≈ 13417.5275439`. Two limits therefore differ by at most `2K_2' tau^2 ≈ 2.68350550879e-12` at the cap.
   - Comparison: `K_2'/K_2^+ ≈ 3.9995`, with `K_2^+ ≈ 3354.80322946` (AW1). `K_2'` bounds the full trace norm on `B(H_R)` while `K_2^+` bounds the single observable W (section 3.8).
4. **Item 4.** Both mandatory sentences are filled in section 4, and the gate fields are exported, all false.
5. **Items 5–6.** All 21 contract controls are damaging mutations in `check.py` (none unimplementable). The report and checker define "quantitative boundary comparison" (section 5.1).

**Proposed reverse verdict: `accepted_within_scope`**, sub-label `uniform_local_closeness_not_uniqueness`. Admission still needs the forward route, the exchange and the skeptical review. This is uniform local closeness, not uniqueness, not whole-sequence convergence, not translation invariance, not boundary independence of the dynamics and not a rate in N.

## 0. Model label, frozen parameters and notation

**Model (frozen, contract `model` and `preregistration`).**
- SU(2) Kogut–Susskind form on Z³ at fixed spacing `a_lat`, with coarse 24-link factors (I1.1).
- Selected triple exactly `(0,0,0)`, so the reference is the Haar product `P_R=|Omega_R><Omega_R|`.
- 21 omitted anchored faces per factor, grouped into whole stars `phi_b=-(tau/3) sum_{f in O_b} W_f` in normalized units `delta=alpha/8` (I1.5).
- Both signs of `tau` with `|tau|<=10^-8`, and fixed positive `alpha`, `hbar`, `E_star`.
- Common clock `s=alpha t_E/hbar`, `theta=alpha t/hbar`. The normalized clock `u=s/8` and the exponent 24 do not appear in any packet.
- Cover: `R={0,e_z}` is the complete factor cover of the original xz Wilson loop `W`, with 48 links, 36 endpoints and 7 incident anchors `R-S`.

**Notation** (all exact at the cap `|tau|=10^-8`):

| symbol | meaning | value at the cap |
|---|---|---|
| `a` | norm of one first-order face creation, `|tau|/144` | `1/14400000000` |
| `J` | per-site interaction sum, `4·7|tau|` | `7/25000000` (= `J_0`) |
| `t_1` | first-order anchored norm, `49a` | `49/14400000000` |
| `T` | `t_1/(1-352J)` | `49/14398580736` |
| `r_AM2` | AM2 remainder `352JT >= ||c-c^(1)||_a` | `3773/11248891200000000 ≈ 3.354e-13` |
| `eps` | AV1 admitted `2T+T^2` | `1411060914529/207319127211110301696 ≈ 6.806e-9` |
| `eps_R` | R-local `82a+2r_AM2+(33a+r_AM2)^2` | `180161487949673694520081/31634388307359360000000000000000 ≈ 5.695e-9` |
| `D` | AV1 admitted `D_ii=2eps(1+eps)/(1+eps^2)` | `585079838465912592144137406066050/42981220507576537932303142777593983768257 ≈ 1.36124528702e-8` |
| `K_2^+` | AW1 admitted Wilson-mean constant | `81108864767825329926713064490531229475390625/24176936535511801466930759024724079017984 ≈ 3354.80322946` |

The checker reads `D_ii` from the AV1 gate snapshot and `K_2^+` from the AW1 gate snapshot. It recomputes both exactly, and they agree to the last digit: `K_2^+ tau^2 = r_AM2 + T·T + T^2 + eps^2 + a·eps^2`, which is the AW1 skeptic itemization. Tier (i) is also recomputed: `D_i=36133347268157653748322/1525878906463907516326874161`.

The AM2 constants are re-derived, not copied:
- `exp(1/8)<8/7`, from a partial sum plus a geometric tail;
- `G(R)<148/7` and `G'(R)<352`;
- `J_0G(R)<1/64` and `2J_0G'(R)=77/390625<1`;
- `k![t^k]G = 16·8^k(1+5k/4)` for `k<=8`;
- a four-qubit exact fixture gives `ad_C^8(V)Omega=8!|1111>` and `ad_C^9(V)=0`, so the termination order for `|X|=4` is 8.

## 1. Item 1 — both named families satisfy the AV1 premises

### 1.1 The two families

- **F1 (AQ1).** `H^(1)_N = sum_{b in Lambda_N} h_b + sum_{b+S subset Lambda_N} phi_b`, with `Lambda_N=[-N,N]^3` and `N>=2`. This is the I1.6 empty-boundary rule: a whole star is retained only if it lies inside the box.
- **F2 (I1 section 6).** For a finite coarse set `B`, let `phi_b^(B) = -(tau/3) sum_{f in O_b, M_f subset B} W_f`, where `M_f` is the actual owner set (I1.4). Set `H^(2)_B = sum_{b in B} h_b + sum_{b in B} phi_b^(B)` and `B_+ = B+S`. The padded operator is
  `H^pad_B = H^(2)_B (x) 1 + 1 (x) sum_{x in B_+\B} h_x` on `H_{B_+}`.
  F2 is the family `B=Lambda_N`, `N>=2`. Every anchor of a retained face lies in `B`, since `0` belongs to every class support.

Enumerated on `Lambda_2` and `Lambda_3`:

| box | faces F1 | faces F2 | F2 minus F1 | partial groups in F2 | `B` sites | `B_+` sites |
|---|---:|---:|---:|---:|---:|---:|
| `Lambda_2` | 1344 | 1960 | 616 | 60 | 125 | 200 |
| `Lambda_3` | 4536 | 5880 | 1344 | 126 | 343 | 490 |

- The two families genuinely differ: F2 keeps boundary faces that F1 drops, as in I1.6's example where `B={0,e_z}` retains no face under F1 but ten under F2.
- On `Lambda_2`: faces(F1, `Lambda_2`) ⊆ faces(F2, `Lambda_2`) ⊆ faces(F1, `Lambda_3`).
- Both families at `N>=2` contain all 82 faces meeting R.
- Both have at most 49 faces through any site, with 49 attained in the bulk.

### 1.2 F1: the admitted chain, step by step

| step | admitted premise used by AV1 | source (snapshot) |
|---|---|---|
| 1 | Ownership, the 21 omitted classes, supports in `b+S`, and `||phi_b||<=7|tau|` | I1 §§2–4 (table parsed and re-derived from `pi` and the link tails) |
| 2 | `J<=28|tau|<=J_0`, the majorant `G`, a single fixed point in the anchored ball, `psi=e^{-C}Omega_0` simple with gap `>=1/2` in every cutoff space and untruncated (§6) | AM2 gate `accepted_within_scope`; AM2 forward and reverse reports |
| 3 | Reset `Tr(rho_{N,F}h_F)<=56|tau||F|`, trace-norm precompactness, diagonal extraction, Nachtergaele–Sims norm dynamics on compact windows | AQ1 §§2–3 |
| 4 | Product split `psi=psi_out+delta`, `(P_R(x)1)psi=psi_out`, `||delta||<=eps||psi_out||`; tier (ii) `D_ii`; cutoff-vector removal; passage to every subsequential limit of the centered construction | AV1 gate (value recomputed exactly) |
| 5 | First-order coefficient `+tau/144`, `c^(1)=-(tau/72)sum W_f Omega_0`, the lemma `||(Q_x(x)1)phi_out||<=t||phi_out||` (AW1 reverse R15), and `K_2^+` uniform in N and every limit | AW1 gate (value recomputed exactly) |

### 1.3 F2: the AM2 contraction at the same `J_0` for the padded interaction family

AM2's proof (forward §§2–4, reverse §§2–4) uses only the hypotheses listed below. The AM2 reverse report states its scope in exactly these terms: "Each V_X is an original omitted anchor group with its declared support of size at most four; repeats are separate indexed terms." A clipped group `phi_b^(B)` is a sub-sum of the original anchor group at `b` with the same declared support `b+S`. I verify each hypothesis for the indexed family `{V_{X_b}=phi_b^(B)}` with `X_b=b+S`, in the AM2 volume `Lambda=B_+`.

- **(a) Supports.** By I1.4 every retained face has `M_f=b+K_k subset b+S`, so `supp phi_b^(B) subset (b+S) cap B subset X_b subset B_+`, with `|X_b|=4`. The padding exists precisely so that each indexed support lies inside the AM2 volume. Without it, `X_b` leaves `B`; the checker rejects that as the mutation `no_padding_am2_volume_equals_B`.
- **(b) Norms.** `||phi_b^(B)|| <= (|tau|/3)·#{retained faces at b} <= 7|tau|`.
- **(c) Per-site sum.** `u in X_b` iff `b in u-S`, and `|S|=4`. Hence `J^(2) = max_{u in B_+} sum_{b: u in X_b} ||phi_b^(B)|| <= 28|tau| <= J_0 = 7/25000000`. The enumerated maximum is exactly 28 (per `|tau|`) on both boxes, attained where four full groups meet.
- **(d) Termination.** A nonzero nested word `ad_{C_1}...ad_{C_k}(V_X)Omega` needs every creation to meet `X`. Each side of `V_X` holds at most `|X|` pairwise-disjoint creations. So the word vanishes for `k>2|X|=8`, and the four-qubit fixture attains order 8 exactly. Importing a support-three order 6 is rejected.
- **(e) Constants.** `L_k^num = 16·8^k(1+5k/4)` comes from `2^{|X|}=16` output sets and `|I_j|<=|M|+4`. Hence `G`, `G(R)<148/7` and `G'(R)<352` are unchanged. `J_0G(R) < 148/25000000 < 1/64` gives the ball self-map. `2J_0G'(R) < 77/390625 < 1` gives the Lipschitz contraction and the excited-sector exclusion with the shifted inverse `2/|M|`.
- **(f) Onsite.** `h_x>=Q_x` at every `x in B_+`: the padded sites carry the same Haar-reference Casimir operator, `h_x>=6Q_x`.
- **(g) Conclusion.** In every cutoff space, AM2 gives a single fixed point in the anchored ball. `psi^pad=e^{-C}Omega_0` is a simple ground with gap at least 1/2, uniformly in the cutoff and in `B`, for both signs. The cutoff passage of AM2 §6 applies without change: each `h_x` has compact resolvent and `V` is bounded in a fixed volume.
- **(h) Decoupling.** No retained face touches `B_+\B`. The fixed-point map preserves the closed set of collections supported in `B`, since `V` acts only on `B`. So the fixed point is supported in `B` and `psi^pad = psi^(2)_B (x) Omega_{B_+\B}`. The spectrum of `H^pad` contains `spec(H^(2)_B)+0`, so `H^(2)_B` has a simple ground with gap `>=1/2`, and its reduced densities on `R` equal those of `psi^pad`.

The checker validates (a)–(h) on real F2 records for `Lambda_2` and `Lambda_3`. It rejects five damaging records:
- padding removed;
- a face with support outside `B` retained;
- a face counted in two groups;
- a padded site given an interaction;
- termination 6.

### 1.4 F2: tier-(ii) inputs, cutoff-vector removal and the AV1 split

- **First-order creations.** `c^(1)_M = H_M^{-1}P_M V Omega_0 = -(tau/72) sum_{retained f: M_f=M} W_f Omega_0`. The face energy is 24 in normalized units (3 in alpha units), and the amplitude is `-tau/72` in both unit systems.
- **Anchored norm.** At most 49 retained faces pass through any site of an F2 box, and 0 through a padded site. So `t_1<=49a`.
- **Remainder.** The AM2 multilinear bound with `J^(2)<=28|tau|` gives `||c-c^(1)||_a <= 352 J t`. Hence `t<=T`, `||c-c^(1)||_a<=r_AM2`, `eps=2T+T^2` and `D=D_ii`, with the same values as for F1.
- **Cutoff.** For `L>=24` every `W_f Omega_0` lies in the cutoff space, so `c^(1)_L=c^(1)`. The AV1 cutoff-vector argument (R20–R21: variational upper limit plus the uniform cutoff gap `1/2`) carries over verbatim to `H^pad`, and the reduced density on R of the untruncated simple ground is the trace-norm limit of the cutoff densities.
- **AV1 split.** It uses only commuting creations, excitedness `c_I in (x)Q_xH_x` and anchored sums at the two sites of R. All three hold. Hence `||rho^(2)_{N,R}-P_R||_1<=D` for every `N>=2` and every cutoff.

### 1.5 F2: reset budget and local trace-norm compactness

**Reset.** For a finite `F subset B`, reset the finite ground density on `F` to `P_F` and keep its exterior marginal.
- Groups that do not meet `F` keep their expectations.
- A group meeting `F` must have its anchor in `F-S`, and its expectation changes by at most `2||phi_b^(B)||<=14|tau|`.
- `h_F` drops to 0.
- Unbounded exterior energies cancel after bounded spectral truncation, exactly as in AQ1 §2.

The variational principle then gives

`Tr(rho^(2)_{B,F} h_F) <= 14|tau|·|F-S| <= 56|tau||F| =: C_F`, and on R, with the seven incident groups, `Tr(rho^(2)_{B,R} h_R) <= 98|tau|`.

The enumerated incident groups on `Lambda_2` and `Lambda_3` are 7 full groups, with charge exactly `98|tau|`. Charging only the two outgoing groups (`28|tau|`) is rejected.

**Compactness.** `h_F` has compact resolvent, so `Q_{F,L}=1_[0,L](h_F)` has finite rank. Then `Tr rho_F(1-Q_{F,L})<=C_F/L`, and `||rho_F-Q rho_F Q||_1<=2sqrt(C_F/L)` by purification and partial-trace contractivity. The family `{rho^(2)_{N,F}}_N` is therefore trace-norm precompact on every finite `F`. Diagonal extraction over nested cubes gives subsequences that converge in trace norm on every finite region. Their limits are compatible and define locally normal states. A subsequential limit of F2 means any such limit; a chosen subsequential limit is one member of that set.

### 1.6 Two topologies, named separately

- **States:** trace norm on `B(H_R)`, i.e. `||rho-rho'||_1 = sup_{A in B(H_R), ||A||<=1} |Tr((rho-rho')A)|`. Weak-* convergence on finite-rank observables is **not** enough: `rho_n=(1-D/2)|e_0><e_0|+(D/2)|e_n><e_n|` has a weak-* limit of mass `1-D/2` and pairwise trace distance D. The reset energy supplies the tightness that rules this out.
- **Dynamics:** operator norm on bounded local observables, uniformly on compact time windows (Nachtergaele–Sims, as placed in AQ1 §3). For F2 the finite Hamiltonians are the native restrictions `sum_{X subset Lambda} Phi_face(X)` of the owner-set interaction `Phi_face(M) = -(tau/3) sum_{M_f=M} W_f`, whose supports have l1 diameter at most 2 and whose per-site sum is at most `49|tau|/3`. So `||Phi_face||_F <= 81·49|tau|/3 = 1323|tau|`. This names the topology only. The AY1 statements are static, and I do **not** claim that the F1 and F2 dynamics coincide (`boundary_independence_of_dynamics_claimed: false`).

## 2. Item 2 — `||rho_R - rho'_R||_1 <= 2D` by the reverse route

### 2.1 Reverse analysis

Desired: one constant bounding the trace distance on `R` between any two states in the union of the two limit sets, at a fixed `tau`.

Working backwards:
- a trace distance between two states is controlled by their fidelity (Fuchs–van de Graaf);
- a fidelity between two states is controlled by their fidelities to one common pure state (Bures-angle triangle);
- fidelity to the pure reference `P_R` is the single number `F=<Omega_R,rho_R Omega_R>`, which passes to limits under trace norm.

So it suffices to bound `F` from below in every finite box of both families. The AV1 vacuum-overlap identity does exactly that.

### 2.2 The fidelity identity in every box, passed to every limit

In every box of either family, at every cutoff `L>=24` and for the untruncated ground, the AV1 split gives, exactly,

`F_N = Tr(rho_{N,R}P_R) = ||psi_out||^2/(||psi_out||^2+||delta||^2) = 1/(1+e_N^2)`, with `e_N <= eps`.

`|Tr((rho-sigma)P_R)| <= ||rho-sigma||_1` makes `F` trace-norm continuous. Hence every subsequential limit of F1 or F2 (along any subsequence, including a chosen subsequential one) satisfies

`F(rho_R) >= 1/(1+eps^2) = 42981220507576535941210238266176140476416/42981220507576537932303142777593983768257`.

### 2.3 Route A: fidelity, then trace distance, then the triangle through `P_R`

- The mixture inequality (AT4 F08, re-proved in AV1 reverse R05) gives `||rho_R-P_R||_1 <= 2sqrt(1-F) <= 2eps/sqrt(1+eps^2) <= 136124527776169485892526179064611/10^40` (directed).
- Since `sqrt(1+eps^2)<=1+eps^2<=(1+eps)^2`, this is at most `D_ii`.
- So `D_ii` is certified by the reverse inequality as well, which is the AV1 "both inequalities" binding.
- The triangle inequality gives `||rho_R-rho'_R||_1 <= 2D_ii`.

### 2.4 Route B: the Bures angle (pairwise, no triangle through a density)

Let `A(rho,sigma)=arccos sqrt(F(rho,sigma))` with the Uhlmann fidelity. It is a metric on states.
- For the pure `P_R`, `F(rho,P_R)=<Omega_R,rho Omega_R>`, so `cos A >= 1/sqrt(1+eps^2)`, i.e. `A(rho,P_R) <= arctan eps`.
- Then `A(rho,rho') <= 2arctan eps <= pi/2`, because `eps<=1`.
- Fuchs–van de Graaf gives `(1/2)||rho-rho'||_1 <= sqrt(1-F(rho,rho')) = sin A(rho,rho') <= sin(2arctan eps) = 2eps/(1+eps^2)`.

Hence

`||rho_R-rho'_R||_1 <= 4eps/(1+eps^2) = 1170159668967453566242603438964736/42981220507576537932303142777593983768257 ≈ 2.72249055552e-8 <= 2D_ii`.

This is an exact rational and a genuinely pairwise bound. The admitted headline constant stays `2D` (the contract names D, the AV1 admitted tier). Route B only shows that `2D` is not an artefact of the triangle through `P_R`.

### 2.5 Constants at the cap (both signs)

| quantity | exact | preview |
|---|---|---|
| `D=D_ii` | `585079838465912592144137406066050/42981220507576537932303142777593983768257` | `1.36124528702e-8` |
| **`2D`** | `1170159676931825184288274812132100/42981220507576537932303142777593983768257` | `2.72249057405e-8` |
| Bures `4eps/(1+eps^2)` | `1170159668967453566242603438964736/42981220507576537932303142777593983768257` | `2.72249055552e-8` |
| target (`preregistration.target`) | `1/1250000` | `8e-7` |

The target is met, with margin `target/2D ≈ 29.384858`. The target is read from the contract and must equal twice the AV1 admitted target `4/10^7`; a coherently rehashed `1/1000` is rejected. Tier (i), `2D_i = 72266694536315307496644/1525878906463907516326874161 ≈ 4.736e-5`, fails the target and is retained as a limited-tier value. The `-tau` evaluation replays the same `|tau|` formula.

### 2.6 What this statement is and is not

The bound is inherited from a finite-volume bound that holds for every volume: `||rho_{N,R}-rho'_{M,R}||_1<=2D` for all `N,M>=2` in either family. It is uniform local closeness on the fixed region `R` at a fixed coupling. It is **not** uniqueness, not whole-sequence convergence, not translation invariance, not a rate in N and not boundary independence of the dynamics. Two limits satisfying it may differ by up to `2D` on `R` (at second order, by up to `2K_2' tau^2`), and without bound elsewhere.

## 3. Item 3 — the first-order reduced density and the second-order difference

### 3.1 Reverse analysis: what can a first-order term be?

Desired: an operator `X` on `H_R` with `||rho_R-P_R-tau X||_1 = O(tau^2)`, uniformly over all limits of both families. Write the block decomposition of any density with respect to `P_R`:

`rho = F P + |rho_perp0><Omega| + |Omega><rho_perp0| + rho_perpperp`, where `rho_perp0 = (1-P)rho Omega` and `rho_perpperp=(1-P)rho(1-P) >= 0`.

- **The derivative of the fidelity identity** kills the diagonal. `F = 1/(1+e^2)` with `e<=eps(tau)=O(tau)`, so `0<=1-F<=eps^2`: the diagonal has no first-order part.
- **Positivity** kills the excited block. `Tr rho_perpperp = 1-F <= eps^2` and `rho_perpperp>=0`, so `||rho_perpperp||_1 <= eps^2`: that block has no first-order part either.
- Exactly, `||(F-1)P + rho_perpperp||_1 = 2(1-F) = 2e^2/(1+e^2)`.

So any first-order term is off-diagonal, `X = |eta><Omega| + |Omega><eta|` with `eta ⊥ Omega`, and it is determined by the single vector `rho_perp0`. The operator problem reduces to a vector problem. The scalar fidelity identity alone cannot supply `eta`, because its first derivative vanishes; its vector form can.

### 3.2 The vacuum-overlap vector identity

For every box of either family, every cutoff `L>=24` and the untruncated ground,

`rho_R Omega_R = (1_R (x) <phi_out|) psi / ||psi||^2`, with `phi_out = (<Omega_R|(x)1)psi = e^{-C_out}Omega_out`.

*Proof.* `<v, Tr_out(|psi><psi|) Omega_R> = sum_k <v(x)e_k,psi> conj<Omega_R(x)e_k,psi> = <v(x)chi, psi>` with `chi=(<Omega_R|(x)1)psi`. The AV1 split `(P_R(x)1)psi = psi_out = Omega_R(x)phi_out` gives `chi=phi_out`.

The `Omega_R` component of this identity is the fidelity identity: `<Omega_R,(1(x)<phi_out|)psi> = ||phi_out||^2`, and `||psi||^2 = ||phi_out||^2(1+e^2)`. Writing `n=||phi_out||` and `psi = Omega_R(x)phi_out + delta`,

`(1_R(x)<phi_out|)psi = n^2 (Omega_R + xi_hat)`, `xi_hat := (1_R(x)<phi_out|)delta / n^2 ⊥ Omega_R`, and so `rho_perp0 = xi_hat/(1+e^2)`.

### 3.3 The derivative: `rho^(1)_R` explicitly

Insert the AV1 expansion `delta = -sum_{I cap R != ∅} c_I-hat psi_out + sum_{I∋0, J∋e_z, I cap J=∅} c_I-hat c_J-hat psi_out` and sort the supports.

- **Inside R:** `I=R`, `{0}`, `{e_z}`. These contribute `-c_R - c_{0}(x)Omega_{e_z} - Omega_0(x)c_{e_z}` exactly: the normalization `n^2` cancels, with no approximation. No omitted face has a single-factor owner set, so `c^(1)_{0}=c^(1)_{e_z}=0`. The first-order part is `-c^(1)_R = +(tau/72) sum_{f in F_R} W_f Omega_R`.
- **Straddling:** `I cap R != ∅` and `I\R != ∅`. For `x in I\R`, the vector `c_I-hat psi_out` lies in the range of `Q_x`, so `(1(x)<phi_out|)c_I-hat psi_out = (1(x)<(Q_x(x)1)phi_out|)c_I-hat psi_out`. The AW1 lemma gives `||(Q_x(x)1)phi_out|| <= t||phi_out|| <= T n`. Each straddling contribution to `xi_hat` therefore has norm at most `T||c_I||`: it is second order. Pairing only with the vacuum part of `phi_out` gives exactly 0, because `c_I` is excited at x.
- **Pairs:** each has norm at most `||c_I|| ||c_J||`, which is second order.

Therefore the derivative of the overlap vector at `tau=0`, in the uniform-remainder sense of section 3.5, is `eta = (1/72) sum_{f in F_R} W_f Omega_R`, and

\[
\rho^{(1)}_R=\frac1{72}\sum_{f\in F_R}\bigl(|W_f\Omega_R\rangle\langle\Omega_R|+|\Omega_R\rangle\langle W_f\Omega_R|\bigr)
=\frac1{144}\sum_{f\in F_R}\bigl(|e_f\rangle\langle e_0|+|e_0\rangle\langle e_f|\bigr),\qquad e_0=\Omega_R,\ e_f=2W_f\Omega_R .
\tag{HNM-AY1-R01}
\]

`F_R` consists of the 10 faces with owner set exactly `{0,e_z}`: xz with `r=0,1,2`, `s=0,1` (6 faces) and yz with `r=0..3`, `s=0` (4 faces), all anchored at `0`. The original `W` (xz, `r=0,s=0`) is one of them. In the forward language, this is the R-marginal of `-(c^(1)Omega_0^* + h.c.)` restricted to creations meeting R. Straddling first-order creations have zero R-marginal against `Omega_out`, so only `c^(1)_R` survives.

### 3.4 Properties and AW1 consistency (exact, in `check.py`)

- The vectors `{e_0, e_f}` are orthonormal. `E[W_f]=0`, `E[W_f^2]=1/4`, and distinct faces share at most one link, which is checked on all 82 faces meeting R. So `E[W_fW_g]=(1/4)delta_{fg}`.
- `rho^(1)_R` is Hermitian and traceless, with zero diagonal and zero excited block.
- `||rho^(1)_R||_1 = 2||eta|| = sqrt(10)/72`. Its square is exactly `10/5184`; directed, `sqrt(10)/72 ∈ [0.043920523057, 0.043920523058]`.
- `Tr(rho^(1)_R W_g) = 1/144` for every `g in F_R`. In particular `tau Tr(rho^(1)_R W) = +tau/144`, the AW1-admitted first-order Wilson mean, giving `±1/14400000000` at `tau=±10^-8`.

The checker rejects the following as damaging:
- the AM2-sign literal (`-1/144`);
- a dropped adjoint (non-Hermitian);
- a scalar or diagonal first-order ansatz;
- a first-order excited block;
- an all-zero density;
- straddling faces treated as operators on `H_R`.

### 3.5 Exact second-order remainder identity

With `r_xi := xi_hat - tau eta`, which is orthogonal to `Omega_R`,

`rho_R - P_R - tau rho^(1)_R = [(F-1)P + rho_perpperp] + [|rho_perp0 - tau eta><Omega| + h.c.]`, with `rho_perp0 - tau eta = r_xi/(1+e^2) - tau eta e^2/(1+e^2)`.

So, exactly up to the triangle inequality,

`||rho_R - P_R - tau rho^(1)_R||_1 <= 2e^2/(1+e^2) + 2||r_xi|| + 2e^2 ||tau eta|| <= 2eps_R^2 + 2B_xi + 2eps_R^2·10a`,

where

- `B_xi := 2r_AM2 + T(72a+2r_AM2) + (33a+r_AM2)^2` bounds `||r_xi||`, item by item from section 3.3:
  - inside R, `||(c-c^(1))_R|| + ||c_{0}|| + ||c_{e_z}|| <= r_AM2 + r_AM2`, from the anchored sums at `0` (which contain `R` and `{0}`) and at `e_z`;
  - straddling, the 72 first-order faces meeting R outside R, plus the remainder `2r_AM2`, times `T`;
  - pairs, `s_0 s_z <= (33a+r_AM2)^2`, with 33 faces containing one site of R but not the other;
- `e <= eps_R`, since `sum_{I cap R != ∅}||c_I|| <= 82a+2r_AM2` and the pairs are at most `(33a+r_AM2)^2`;
- `||tau eta|| = ||c^(1)_R|| <= 10a`.

### 3.6 The R-local ledger `K_2'` (every item tier (ii), charged at its positive majorant)

| item (AW1 name) | exact value at the cap | `/tau^2` (preview) |
|---|---|---:|
| `am2_remainder` = `2·2r_AM2` | `3773/2812222800000000` | 13416.4334347 |
| `straddling` = `2T(72a+2r_AM2)` | `1378174049/40492017033419980800000000` | 0.340356976502 |
| `two_creation` = `2(33a+r_AM2)^2` | `166184094520081/15817194153679680000000000000000` | 0.105065470465 |
| `density` = `2eps_R^2` | `32458161740240419840923214704314125168912246561/500367261790397296906568089804800000000000000000000000000000000` | 0.648686759083 |
| `normalization` = `2eps_R^2·10a` (third order) | in `results.json` | 4.50476916030e-10 |
| `arithmetic` | exact rationals; no rounding in the headline | 0 |
| **`K_2'`** | `966771578474926086618624139557778885954947547760216752246561/72052885697817210754545804931891200000000000000000000000` | **13417.5275439** |

The items add linearly (triangle inequality). A root-sum-square assembly, tier mixing (for example a crude `t` in one item) or a zero item is rejected.

### 3.7 The same first-order density for every limit; the two-limit bound

`F_R` depends only on the 10 faces with owner set `R`. They belong to the star at anchor 0, retained in every F1 box with `N>=1`, and they are contained in every F2 box `B ⊇ R`. Their coefficient `-tau/72` is fixed by I1.5 and the face energy 24. So (HNM-AY1-R01) is the same operator for every box of either family at every cutoff `L>=24`.

The bound of section 3.5 holds in all of them, with the same `K_2'`: finite-box face counts are at most the bulk counts 72 and 33, and `T` and `r_AM2` are the same for both families. It passes to the untruncated ground and then to every subsequential limit, because the ball is closed in trace norm. Hence, for every subsequential limit of F1 or F2 at `tau`,

`||rho_R - P_R - tau rho^(1)_R||_1 <= K_2' tau^2`, and for any two such limits `||rho_R - rho'_R||_1 <= 2K_2' tau^2`.

At the cap, `2K_2' tau^2 = 966771578474926086618624139557778885954947547760216752246561/360264428489086053772729024659456000000000000000000000000000000000000000 ≈ 2.68350550879e-12`, which is `2D/10145` (ratio ≈ 1.0145276e4).

**In what sense `rho^(1)_R` is "the" first-order density.** A limit state at a fixed `tau` does not determine a derivative, and the limit sets may depend on `tau` through the subsequence. The statement is therefore the uniform-remainder expansion above, which holds for every selection `tau -> omega_tau` of subsequential limits of either family. If two operators `X`, `X'` both satisfied it along any sequence `tau_j -> 0`, then `||X-X'||_1 <= (K+K')|tau_j| -> 0`, so the first-order coefficient does not depend on the family, the subsequence or the selection. This concerns the first-order coefficient only. It does not identify the states: they may still differ at order `tau^2` on R, and without bound elsewhere.

### 3.8 Comparison of `K_2'` with `K_2^+`

`K_2'/K_2^+ = 3867086313899704346474496558231115543819790191040867008986244/966893014524284957965768152362480514948256313800811767578125 ≈ 3.99949762363`.

| item `/tau^2` | `K_2^+` (AW1, W only) | `K_2'` (trace norm on `B(H_R)`) | `K_2'` per unit trace multiplier |
|---|---:|---:|---:|
| am2_remainder | 3354.108358 (`r_AM2`, only `c_R`, multiplier `2||W Omega_R||=1`) | 13416.433435 (`4r_AM2`) | 6708.216717 |
| straddling | 0.115812 (`T·T`) | 0.340357 (`2T(72a+2r_AM2)`) | 0.170178 |
| two_creation | 0.115812 (`T^2`) | 0.105065 | 0.052533 |
| density | 0.463247 (`(2T+T^2)^2`) | 0.648687 (`2eps_R^2`) | 0.324343 |
| normalization | 3.2e-11 | 4.5e-10 | 2.3e-10 |

How to read the table:
- **Different quantities.** `K_2^+` bounds one observable: `W` pairs only with `c_R`, since `W Omega_R` is excited at both sites, and `||W Omega_R||=1/2`. `K_2'` bounds `sup_{||A||<=1}` over all of `B(H_R)`. That supremum costs the trace-norm multiplier 2 (for `||A Omega_R||` up to 1) and charges the single-site remainder supports `{0}`, `{e_z}` at both sites.
- **Where the R-local restriction helps.** Restricting to faces meeting R (82/72/33 instead of `2T≈98a`, `T·T`, `T^2`) lowers every count-dependent item per unit multiplier: `0.547` against `0.695` for straddling plus pairs plus density.
- **Where it cannot help.** The AM2 generic remainder `r_AM2 = 352JT` dominates both constants (≈99.98% of `K_2^+` and ≈99.99% of `K_2'`), and restricting face counts does not touch it. `K_2'<K_2^+` is not attainable by face restriction with the admitted remainder.
- **For W alone.** The AW1 `K_2^+` remains the sharper constant, and restricting `K_2'` to `A=W` reproduces AW1's structure.

### 3.9 Labelled variants (valid, not headline)

| variant | `K_2'` | ratio to `K_2^+` |
|---|---:|---:|
| orthogonal in-R sectors: `||(c-c^(1))_R + c_{0}(x)Omega + Omega(x)c_{e_z}|| <= sqrt(2) r_AM2` (the three pieces are mutually orthogonal and the anchored sums at `0` and `e_z` both contain `R`); directed `sqrt 2` | 9487.94517028 | 2.8281674 |
| directed AM2 remainder `r' = 288JT/(1-8T)` (`G(t)-16 <= 288t/(1-8t)`) | 10978.1762675 | 3.2723756 |
| both refinements | 7763.06332882 | 2.3140145 |
| admitted `eps=2T+T^2` in the density item | 13417.8053515 | 3.9995804 |

### 3.10 Scaling, monotonicity and sign

- **Scaling (`tau -> tau/100`).** The exact ratios are 100.0097592 for `2D` (linear, in `[99,101]`) and 10000.97595 for `2K_2'tau^2` (quadratic, in `[9900,10100]`).
- **Monotonicity.** `K_2'(tau)` is nondecreasing in `|tau|`: 13417.528, 13416.337, 13416.218 and 13416.206 at `tau`, `tau/10`, `tau/100` and `tau/1000`. So the cap value bounds every smaller `|tau|`.
- **Sign.** Only `|tau|` enters the constants. The first-order term `tau rho^(1)_R` changes sign with `tau`, consistently with the AW1 flip lemma, since `alpha_E` maps `W_f` to `-W_f`.

## 4. Item 4 — mandatory sentences and gate fields

**Contract template (preregistration `mandatory_sentence_template`), filled:**

> For every pair of subsequential limits of the named construction families F1 (centered whole-star boxes Lambda_N (AQ1), N>=2) and F2 (all-contained-face boxes with padding (I1 section 6), Lambda_N, N>=2) at the same coupling tau with |tau|<=10^-8 (either sign), on the fixed cover R and for the frozen observable class, the reduced densities satisfy ||rho_R - rho'_R||_1 <= 2D = 1170159676931825184288274812132100/42981220507576537932303142777593983768257 (~2.72249e-8 at the cap) and agree to first order in tau (common rho^(1)_R; ||rho_R - rho'_R||_1 <= 2 K2_prime tau^2 = 2.68350e-12 at the cap); this does not assert equality of the states, whole-sequence convergence, translation invariance, boundary independence of the dynamics, or a rate in N.

**Jung loop-2 form (as relayed in my task), filled:**

> For every pair of subsequential limits omega', omega'' of the named families F1, F2 at the same coupling tau, and for every A in B(H_R) with ||A|| <= 1 on the fixed cover R: |omega'(A) - omega''(A)| <= 2D(tau) = 2.72249e-8 at |tau|=10^-8 [order tau^1], and <= 2 K2_prime tau^2 = 2.68350e-12 [order tau^2, after subtracting the common first-order density rho^(1)_R]. This is uniform local closeness on a fixed region at fixed coupling, inherited from a finite-volume bound that holds for every volume. It does not assert omega' = omega'', convergence of any whole sequence, translation invariance, boundary independence beyond R, or any rate in N; two states satisfying it may differ by the stated order on R and without bound elsewhere.

**Gate fields**, read from `preregistration.gate_fields_required` and exported unchanged: `uniqueness_claimed: false`, `whole_sequence_claimed: false`, `rate_claimed: false`, `translation_invariance_claimed: false` and `boundary_independence_of_dynamics_claimed: false`. Uniqueness, whole-sequence convergence, a rate and translation invariance are not claimed.

Also exported:
- `states_compared: "all subsequential limits of F1 and F2"`;
- `region: "R fixed before production"`;
- `topology: "trace norm on B(H_R)"`;
- `closeness_order: [1, 2]`;
- `label: "uniform_local_closeness_not_uniqueness"`.

**Phrasing rules.** `check.py` enforces them on this report and on both sentences:
- no definite-article phrase "thermodynamic limit" (a single limit is never presupposed);
- the definite phrase for a single AQ-type state appears only inside the verbatim negated contract exclusion (section 8);
- every line that mentions uniqueness also contains "not";
- the report says "a chosen subsequential" at least once.

## 5. Items 5–6 — controls, examples and definitions

### 5.1 Quantitative boundary comparison (definition)

In AY1, a *quantitative boundary comparison* means a closeness bound (here `2D` at order `tau`, and `2K_2' tau^2` at order `tau^2`) between the local states produced by two named boundary prescriptions, **plus** a matching first-order term (the common `rho^(1)_R`). It is explicitly **not** a variational statement about which boundary condition the infinite-volume theory selects, and not a statement that either family's limits are canonical.

### 5.2 Fixed-vector versus moving-vector example

Take `P=|Omega><Omega|` as the fixed vector and `w_N = Omega + lam e_{1+(N mod 2)}` with `lam=1/10000` and `e_1 ⊥ e_2 ⊥ Omega` as the moving vectors. Let `rho_N=|w_N><w_N|/(1+lam^2)`.
- Every `rho_N` is within `D_ex=2lam/sqrt(1+lam^2)` of `P`: exactly, `||rho_N-P||_1^2 = 4lam^2/(1+lam^2)`.
- `||rho_0-rho_1||_1^2 = 4(1-(1+lam^2)^{-2})`, which is at most `(2D_ex)^2` and at most the Bures bound `(4lam/(1+lam^2))^2`.
- The sequence has two distinct subsequential limits.

Uniform closeness to a fixed vector therefore implies neither convergence of the moving sequence nor equality of its limits. The mutation "whole sequence converges" is rejected.

### 5.3 A common enclosing interval is not equality

`tau/144 ± K_2^+tau^2/2` both lie in the AW2-type enclosure `[tau/144-K_2^+tau^2, tau/144+K_2^+tau^2]` and differ. Equality inferred from a common interval, or from trace distance at most `2D`, is rejected.

### 5.4 "Uniform in N" is not "uniform in a"

Every constant here is uniform in the box size N, the on-site cutoff, the family and the subsequence, at **fixed** lattice spacing `a_lat`, fixed `alpha`, `hbar`, `E_star` and fixed `tau` with `|tau|<=10^-8`. Nothing is uniform in the spacing, and N → ∞ at fixed spacing is not a continuum limit. As an illustration from a different model (the AX1 uniform Kogut–Susskind dictionary `tau=96/g^4`), the cap sits at `g^4=9.6·10^9`, i.e. strong bare coupling. The certificate says nothing at weak coupling.

### 5.5 The 21 contract controls (each a damaging mutation in `check.py`)

| control | damaging mutations rejected |
|---|---|
| `missing_incoming_stars` | orthant anchors `{0,e_z}`; one-star `J=7|tau|`; two-anchor reset `28|tau|`; F2 reset charging only outgoing groups |
| `full_original_wilson_cover` | the four drawn links; cover `{0}`; cover with an extra factor (48 links, 36 endpoints required) |
| `wrong_delta_alpha_hbar_clock` | mixed units (`-tau/9`, `-tau/576`); exponent 24 on the alpha clock; `u=s/8` clock |
| `vector_versus_scalar_centering` | scalar subtraction as vector centering (`-51/10000` vs `+1/10000`); uncentered residue `1/16`; scalar first-order shift as the density; the W-only `K_2^+` as a trace-norm constant |
| `first_order_mean_charged` | zero first-order density; state budget `K_2'tau^2`; state budget `2K_2'tau^2` (both below the proved first-order size) |
| `tau_scaling_exponent` | second-order difference labelled order 1; `2D` labelled order 2; AT4 square root labelled linear |
| `changed_model_relabelled` | nonzero triple; coupling above the cap; uniform route-B `J=29|tau|`; finite-graph model id; an unnamed boundary family |
| `coherent_evidence_tampering` | 7 coherently rehashed contract tampers (target `1/1000`, cap `10^-7`, gate field true, family removed, template negation removed, control removed, isolation false); byte change without rehash; AV1 gate `D_ii` edited; AW1 gate `K_2^+` halved |
| `insufficient_verdict_retained` | one family relabelled accepted; no first-order density relabelled accepted; failing family relabelled limited; tier (i) relabelled accepted; tier-(i) closeness `2D_i` admitted |
| `exact_arithmetic_admission` | float `tau`; bool; NaN; zero denominator; float admission |
| `root_n_misuse` | `sqrt(72)a` for the straddling budget; `sqrt(82)a` for the R-sum; root-sum-square ledger; division by `sqrt(volume)` |
| `no_priority_or_continuum_claim` | continuum, priority, uniform-Wilson or uniqueness flags set true (the uniqueness flag must stay false, not true) |
| `topology_named` | weak-* for states; one topology for both; norm continuity on all of `B(H_F)`; the weak-* mass-escape limit accepted as a state |
| `two_families_named` | single family; "all boundary conditions"; F2 collapsed onto F1 (whole-star rule, 616 faces fewer on `Lambda_2`) |
| `subsequence_versus_whole_sequence` | whole-sequence convergence from uniform closeness (moving-vector example); an unquantified "the limit" |
| `local_closeness_not_uniqueness` | equality from closeness; equality from a common enclosing interval; mandatory sentence without its negation |
| `common_clock` | second-order closeness across `+tau`/`-tau`; alpha clock versus delta clock; `u=s/8` packet |
| `tier_mixing_rejected` | `D_ii+D_i`; the AV1 reverse 82-face refinement used as the admitted constant; a crude-`t` straddling item in the ledger; `4t_1` without self-consistency |
| `reverse_premise_isolation` | triage added; Jung loop-2 response added; forward AY1 report added; deliberation added; a premise removed |
| `padding_family_contraction_proved` | padding removed; a face with support outside `B`; a double-counted face; an interacting padded site; termination 6 |
| `not_uniform_in_a` | "uniform in lattice spacing"; "uniform in a"; "g → 0"; "N → ∞ called continuum" |

No control was left unimplemented: `controls_not_implementable_as_mutations` is empty.

Remarks attached to two controls (consequences, **not claimed**, not targets):
- **`first_order_mean_charged`.** `||tau rho^(1)_R||_1 - K_2'tau^2 ≈ 4.3786e-10` exceeds every second-order budget. This implies a state-level lower bound on `||rho_R-P_R||_1`. AY1 does not admit it, and `resolved_interaction_shift` stays false; the flag concerns `omega(W)`, which AW2 handles.
- **`common_clock`.** Limits at `+tau` and at `-tau` differ on `R` by at least `2sqrt(10)|tau|/72 - 2K_2'tau^2 ≈ 8.757e-10`. This is why "the same coupling" is part of every statement here.

### 5.6 Freeze and byte-identical replays

These are executed by `research/round32/tools/freeze.py`:
- replays under normal and `-O` Python into fresh external directories, required byte-identical to `output/`;
- the reverse premise-isolation check;
- `freeze.json`.

`check.py` uses no clock, randomness or floating decision, writes sorted JSON and truncates previews with integer arithmetic.

## 6. Error ledger (preregistered names)

| term | value | meaning |
|---|---|---|
| `state_boundary` | `2D ≈ 2.72249057405e-8` (exact above) | closeness of any two subsequential limits of F1/F2 at the same `tau`, from the finite-volume AV1 bound (order `tau`) |
| `second_order_difference` | `2K_2'tau^2 ≈ 2.68350550879e-12` (exact above) | after the common first-order density, itemized in section 3.6 (order `tau^2`) |
| `arithmetic` | `0` in the headline | all headline constants are exact rationals; directed `10^-40` roundings enter only the fidelity cross-check, the `sqrt 2` variant and brackets; decimals are truncated previews |

The on-site cutoff enters at no cost: each box is handled by an exact limit (section 1.4).

## 7. Finite fixtures (audits of the algebra; `model_is_finite_graph: true`, `transfers_to_aq: false`)

**Creation-algebra fixture.** Four qubit sites `(0, e_z | o1, o2)`. The first-order creations `lam·(...)` sit on two or three sites (in R, straddling one site, strictly containing R, and outside); the second-order creations `lam^2·(...)` are single-site and in-R corrections. `lam=1/50`, `u=-1/2`. Two environments, A and B, share only the first-order in-R creation `lam u` (two "boundary families"). Checked exactly:
1. `(<Omega_R|(x)1)psi = prod_{I cap R=∅}(1-c_I)Omega_out`.
2. The vacuum-overlap vector identity, and `F=1/(1+e^2)`.
3. The expansion of `delta` into in-R, straddling and pair terms.
4. Each component of `xi_hat` lies within its ledger item. The straddling component is nonzero, so dropping that item is rejected.
5. `||rho-P-lam rho^(1)||_1 <= 2||.||_2 <=` the ledger bound, in both environments.
6. `rho_A != rho_B`, but `2||rho_A-rho_B||_2 <= bound_A+bound_B < ||lam rho^(1)||_1`.
7. `Tr(rho_A-rho_B)^2` scales by ≈ 9889 when `lam -> lam/10`, i.e. `lam^2` for the difference.

These fixtures audit the algebra. The infinite-dimensional statements rest on sections 1–3.

## 8. Exclusions and claim flags

**Contract `claim_exclusions` (verbatim), none claimed:**
- not claimed: uniqueness of the AQ state;
- not claimed: whole-sequence convergence or a rate in N;
- not claimed: translation invariance;
- not claimed: continuum;
- not claimed: scientific priority.

**Preregistered exclusions, all respected:**
- free reference inside enclosure ⇒ no interaction claim;
- no uniqueness claim (uniqueness is not asserted);
- whole-sequence convergence or rate in N;
- continuum or weak coupling;
- transfer from a finite graph;
- relabelling a static shift as dynamical;
- scientific priority.

**Claim flags,** all `false`:
- `continuum_claim`, `uniform_wilson_claim`, `resolved_interaction_shift`, `scientific_priority_verified`;
- the five gate fields (uniqueness is not claimed).

**Further scope limits:**
- only the zero-selected patterned family, the cover `R`, fixed spacing and `|tau|<=10^-8`;
- nothing transfers to nonzero selected triples, where `P_R` is not Haar;
- nothing transfers to uniform Wilson theory, weak coupling or the continuum;
- no statement about the dynamics of either family beyond naming its topology.

## 9. Proposed reverse verdict, honest gaps and contract wording notes

**Proposed reverse verdict: `accepted_within_scope`** (sub-label `uniform_local_closeness_not_uniqueness`). The rule in `check.py` gives `insufficient` if a family fails the premises, and `limited` for one family only, no first-order density, tier (i) only or inexact constants.

**What leans on inherited results** (not re-proved here):
- AM2's multilinear estimate, fixed point, excited-sector exclusion and cutoff passage. They are re-applied to the padded family by checking that every hypothesis the proof uses holds (section 1.3), not by a new proof.
- AV1's split and cutoff-vector argument.
- AW1's lemma R15 and the admitted `K_2^+`.
- AQ1's reset argument, including exterior cancellation, and diagonal extraction.
- Nachtergaele–Sims, named only.
- Uhlmann/Bures/Fuchs–van de Graaf, which are standard.

**Independence.** The product split, the admitted constants and the contract text (which names the families, the constant `2D` and the forward form of `rho^(1)_R`) are shared. Independence is claimed only for:
- the reverse routes (fidelity passage, Bures angle, the vector overlap identity and its derivative, the block-positivity reduction);
- the padded-family itemization;
- the R-local ledger;
- the code.

**Contract wording notes** (non-blocking):
1. Item 3's "derivative of the vacuum-overlap/fidelity identity" needs the **vector** form of the identity. The scalar fidelity identity is `1-O(tau^2)` and determines only that the diagonal and excited blocks have no first-order part; the off-diagonal `rho^(1)_R` comes from `rho_R Omega_R=(1(x)<phi_out|)psi/||psi||^2`.
2. Item 3 calls `K_2^+` "whole-box". It is volume-uniform and uses anchored sums at the two sites of `R`. More importantly, it bounds the single observable W, whereas an R-local trace-norm `K_2'` necessarily carries the multiplier 2 and the single-site remainder supports. With the admitted AM2 remainder, `K_2'<K_2^+` is not attainable by restricting face counts (section 3.8).
3. The preregistered `mandatory_sentence_template` and the Jung loop-2 form relayed to me differ in wording (quantifier over `A in B(H_R)`, "without bound elsewhere"). Both are filled in section 4.
4. `preregistration.state_provenance` names only the AQ1 subsequence, while the contract compares two families. F2's provenance is the analogous F2 subsequence (section 1.5).
5. The contract exclusion quoted in section 8 uses a definite article for a single AQ-type state, which the relayed phrasing rule avoids. It appears only once in this report, verbatim and negated.

## 10. Map of contract items and controls

| contract item / control | where proved | where checked (`results.json` check id) |
|---|---|---|
| 1 F1 admitted chain | §1.2 | `item1_F1_admitted_chain`, `am2_constants_rederived`, `av1_gate_D_ii_recomputed`, `aw1_gate_K2_plus_recomputed` |
| 1 F2 contraction, reset, compactness | §§1.3–1.5 | `item1_F2_padded_am2_contraction`, `item1_F2_reset_and_compactness`, `padding_family_contraction_proved` |
| 1 two topologies | §1.6 | `topology_named` |
| 2 `2D` for any two limits | §2 | `item2_pairwise_closeness_2D` |
| 3 `rho^(1)_R` (reverse derivation) | §§3.1–3.4 | `item3_fidelity_derivative_block_structure`, `item3_first_order_density_explicit` |
| 3 same for every limit; `2K_2'tau^2` | §§3.5–3.7 | `item3_second_order_ledger_K2_prime` |
| 3 compare `K_2'` with `K_2^+` | §§3.8–3.10 | `item3_K2_prime_versus_K2_plus`, `item3_scaling_and_monotonicity` |
| 4 sentences, gate fields | §4 | `item4_mandatory_sentences_and_gate_fields`, `report_phrasing` |
| 5 fixed-vector vs moving-vector | §5.2 | `subsequence_versus_whole_sequence` |
| 5 common interval is not equality | §5.3 | `local_closeness_not_uniqueness` |
| 5 freeze; byte-identical replays | §5.6 | `freeze.py` (`freeze.json`); `no_interpreter_cache_in_closure` |
| 6 not uniform in a; definition | §§5.1, 5.4 | `not_uniform_in_a`; `quantitative_boundary_comparison_definition` |
| `missing_incoming_stars` | §§0, 1.5 | same id |
| `full_original_wilson_cover` | §0 | same id |
| `wrong_delta_alpha_hbar_clock` | §§0, 1.4 | same id |
| `vector_versus_scalar_centering` | §3.4 | same id |
| `first_order_mean_charged` | §§3.4, 5.5 | same id |
| `tau_scaling_exponent` | §3.10 | same id |
| `changed_model_relabelled` | §0 | same id |
| `coherent_evidence_tampering` | §§0, 2.5 | same id |
| `insufficient_verdict_retained` | §§2.5, 9 | same id |
| `exact_arithmetic_admission` | §6 | same id |
| `root_n_misuse` | §§3.4, 3.6 | same id |
| `no_priority_or_continuum_claim` | §8 | same id |
| `topology_named` | §1.6 | same id |
| `two_families_named` | §1.1 | same id |
| `subsequence_versus_whole_sequence` | §§2.6, 5.2 | same id |
| `local_closeness_not_uniqueness` | §§2.6, 5.3 (closeness, not identification) | same id |
| `common_clock` | §§0, 5.5 | same id |
| `tier_mixing_rejected` | §§2.3, 3.6 | same id |
| `reverse_premise_isolation` | §11 | same id (and `freeze.py`) |
| `padding_family_contraction_proved` | §1.3 | same id |
| `not_uniform_in_a` | §5.4 | same id |

## 11. Files read, scratch disclosure and reproduction

**Snapshots read in full:**
- the contract, AGENTS.md and `selection-ay1.md`;
- the AV1 gate, forward report, reverse report and skeptic review;
- the AW1 gate, forward report, reverse report and skeptic review;
- the AW2, AX1 and AX2 gates (without their bindings lists);
- the AM2 gate, forward report, reverse report and skeptic review;
- AQ1, AQ2, AT4 and I1;
- the paired-physics SKILL and its complete-residual reference.

**Snapshots not read in full:** the Newton, Tesla and historical-panel SKILL files and references. I used them as modern methodological lenses in the sense of AGENTS.md: analysis before synthesis in §§2.1 and 3.1, and complete channel accounting in §3.6. No historical figure endorses anything here, and no historical or occult material supplies a premise.

**Non-scientific style and protocol files outside `inputs/`:**
- `research/round32/tools/README.md` and `research/round32/tools/freeze.py`;
- portions of `research/round32/reverse/av1/check.py` and `research/round32/reverse/aw1/check.py`, for checker conventions;
- a directory listing of `research/round32/reverse/av1` and `research/round32/reverse/aw1`, and the first lines of `reverse/aw1/freeze.json`.

None of these carries premise weight.

**Incidental name exposure.** A final `git status` (run to confirm that nothing outside this directory changed) listed the names, not the contents, of two untracked files under `research/round32/forward/ay1/` (`check.py`, `report.md`). I did not open, read or list them further, and this report and checker were complete before that listing.

**Scratch disclosure.** My private scratch folder is `/tmp/claude-0/ay1-reverse-private/`. It holds exploratory Fraction/float previews (`prelim.py`, `fixture_try.py`), two sentence-comparison text files (`s1.txt`, `s2.txt`), development runs (`dev*`) and the production run `run1`. **Nothing in it is evidence.** I opened no other agent's folder and no file in the shared scratchpad root.

**Reproduce** (fresh absolute output directories outside the checkout):

```bash
python3 -B research/round32/reverse/ay1/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/reverse/ay1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round32/tools/freeze.py verify research/round32/reverse/ay1
```
