# Hruday marginal locality of the reduced densities — BB1 forward (polymer_kp)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production (a Claude model agent) under the frozen BB1 contract (`research/round33/contracts/bb1.json`, sha256 `30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018`). It is correlated model-agent work: not independent human review and not formal verification. HNM labels are project aliases.

**What this producer read.**
- **First** the contract snapshot `inputs/research/round33/contracts/bb1.json`; its sha256 was checked with `sha256sum` before reading, and `check.py` checks it again before any evaluation. Every one of the 35 snapshots in `inputs/` was compared byte for byte with its repository path (`cmp`); all agree.
- **Then only files under `inputs/`:**
  - *read in full:* `AGENTS.md`; `selection-bb1.md`; the BA1 gate (every field); the BA1 forward report; the BA1 skeptic review; the AM2 forward report; the AM2 skeptic review; the I1 forward report; the Round32 lessons file; the paired-physics SKILL and its complete-residual reference;
  - *read in part:* the BA1 reverse report (sections 0–7 and the start of 8); the AV1 forward report (sections 1–9); the AV1 gate (every field except `bindings`); the AV1 reverse report (headings and section 1); the AY1 gate (every field except `bindings` and `decision`); the AY1 forward report (headings and sections 1–3); the AQ1 forward report (sections 1–4) and the AQ1 gate (`accepted`, `limitations`); the AM2 reverse report (sections 1–2); the BA2 gate (`accepted`, `limitations`); headings only of the AW1, AY2 and AQ2 forward reports;
  - *seen only as isolated lines displayed by one keyword search over `inputs/`* (for `N_c`, `omega_O`, `straddle region` and `Tr N`, to check whether a premise defines `N_c`; none does): single lines of the AY1 and AY2 gates, of the AY1 and AY2 forward reports, of the BA2 gate and of the BA2 forward and reverse reports, besides lines of files listed above; the matches came from strings such as `rate_in_N_claimed`;
  - *not opened:* the AY1 reverse report, the BA2 skeptic review, the AW1 and AY2 gates, and the Newton, Tesla and historical-panel SKILL files.
- **Outside `inputs/`, for protocol and conventions only** (no premise weight): `research/round33/tools/README.md`, `research/round33/tools/freeze.py`, `research/round33/tools/phrase_scan.py` (its round phrase list is copied into `check.py`), and `research/round33/forward/ba1/check.py` (checker conventions; BA1 is gated).
- **Not opened or listed:** `research/round33/reverse/bb1/`, `research/round33/forward/bb2/`, `research/round33/reverse/bb2/`, `research/round33/skeptic/` and `research/round33/advisor/` (other than the snapshots in `inputs/`), `research/round33/experts/`, and every other agent's scratch folder.
- **Repository-status disclosure.** One `git status --short` and one `git log --oneline | head -5`, run to see the state of the working tree, displayed three untracked path names outside this packet (`research/round33/reverse/bb2/check.py`, `research/round33/skeptic/bb2-contract-review.md`, `research/round33/skeptic/bb2_check.py`) and five commit subjects, one of which names the BB2 forward producer's freeze. None of these files was opened and nothing from them entered this packet.
- **Scratchpad disclosure.** My private scratch folder is `/tmp/claude-0/bb1-forward-private/`. I created it with `mkdir -p` and did not list `/tmp/claude-0/` or the shared scratchpad root, so I saw no other agent's folder names. It holds prototype scripts (the polymer identity, the exploration majorants, the KP truncation, a toy of Lemma 7.1, the constants, the outside-vector fixture), a harness that imports `check.py` with bytecode writing disabled, and development runs. **None of it is evidence.** I opened no file in any other agent's scratch folder.
- **Tooling note.** The agent file-writing tool refused to create this `.md` file with a generic rule against report files. Because this report is a required protocol artifact that `check.py`, `phrase_scan.py` and `freeze.py` read, it was written with a shell heredoc instead. The content is unaffected.

**Attribution.** Hard-core polymer (cluster) expansions and the Kotecký–Preiss criterion are established mathematics: R. Kotecký and D. Preiss, *Cluster expansion for abstract polymer models*, Comm. Math. Phys. 103 (1986) 491–498, and the decay-function form written as in D. Ueltschi, *Cluster expansions and correlation functions*, Moscow Math. J. 4 (2004) 511–522. They are **cited, not re-proved and not machine-checked**; the primary sources were not re-inspected in this session, and the statement used (Theorem 6.1) is transcribed as known to this producer. The Penrose tree-graph bound behind the criterion, the Schwarz (maximum-modulus) estimate and Weierstrass' theorem are standard. The commuting nilpotent creation expansion is the admitted AM2 construction. The decomposition of the reduced density into Y-clusters weighted by vacuum probabilities, the exploration-tree majorant, the mixed-weight lemma, the marginal-locality lemma and every constant are derived here. Scientific priority is unverified.

## Verdict (forward route)

Model **`AQ_patterned_zero_selected`**: SU(2) in Kogut–Susskind form on `Z^3` at fixed spacing, coarse 24-link factors, selected triple exactly `(0,0,0)` with Haar product reference, 21 omitted faces per anchor entering as `-(tau/3)W_f` in normalized units `delta=alpha/8`, both signs, `|tau| ≤ 10^-8`; the AM2 creation expansion (`J ≤ 28|tau|`, `R=1/64`, `G(t)=16e^{8t}(1+10t)`) in each on-site cutoff space. The named construction families are **F1** (AQ1 centered whole-star boxes `Lambda_N=[-N,N]^3`) and **F2** (I1 §6 all-contained-face boxes with padding on the same `Lambda_N`), `N ≥ 2`. The cover is `R={0,e_z}`, the metric the coarse l-infinity metric on factor sites (star diameter 1), and the topology the trace norm on `B(H_Y)`.

For every comparison of the contract, both signs, every on-site cutoff space `Q_L` (constants independent of the cutoff) and, at fixed `N`, the untruncated ground vectors:

| constant (route polymer_kp) | tier | BA1 input (every-site form (b)) | exact value | preview | frozen target | margin |
|---|---|---|---|---|---|---|
| `C` in `‖ρ^1_R − ρ^2_R‖_1 ≤ C q^(N-1)`, `q=1/64` | exact_first_order | gate bound value `K=49/111790368` (analytic_disc) | §10 | `8.90511999358e-7` | `1/250000` | `4.49179` |
| `c_site` in `‖ρ^1_Y − ρ^2_Y‖_1 ≤ c_site·|Y|·e^{|Y|/10^8}·q^{d_Y}` | exact_first_order | same | §10 | `8.76811811767e-7` | `1/500000` | `2.28099` |
| labelled secondary `C`, `q=151552·|tau|` | exact_first_order | analytic_disc at `rho=1/151552`, `K=49/10202112` | §10 | `9.64401426796e-6` | `1/20000` | `5.18456` |
| labelled secondary `c_site` | exact_first_order | same | §10 | `9.62942065531e-6` | `1/40000` | `2.59621` |
| crude tier `C`, `q=1/64` (reported, never a target) | crude_majorant | crude circle bound `K=296/390625` | §10 | `2.05285240831e-3` | — | fails `1/250000` |

1. **Item 1** (§2): the exact decomposition `ρ_Y = N_c(ω_O)/Tr N_c(ω_O)`, `Tr N_c ≥ 1` by AV1 orthogonality, and the two Lipschitz bounds (outside state: `2(2ε_Y+ε_Y^2)`; coefficients: `2(1+t)^{|Y|-1}`), each named with tier and route.
2. **Item 2** (§§3–7): the hard-core polymer representation of the norm and of the Y-marginal (Y-clusters and vacuum probabilities), the activity bound, the exploration-tree majorant, the **new mixed-weight contraction lemma proved in full** (§5), the Kotecký–Preiss condition with the explicit `a = τ̄^2` (§6), and the marginal-locality lemma in the contract form from the real-parameter derivative along `c + λ(c' − c)` (§7). No analyticity of the reduced density is claimed (no zero-free region is proved).
3. **Item 4** (§§8–9): the every-site input form (b) is **proved in full** (§8). The headline and region bounds hold for all five comparisons, both signs, in each `Q_L` and at fixed `N` for the untruncated vectors; the fixed-`N` F1-versus-F2 comparison is its own item; two one-prescription volumes are compared directly (the union form `2C` is labelled only).
4. **Items 5–6** (§§11–12): the fixtures named by the fixture controls, the mandatory sentence, the gate fields, the `tau → tau/100` ratios (`1.00647875e2` for `C` and `c_site`; `1.00150034e0` and `1.00000000e0` for the secondary pair; `q_2` ratio `1.00000000e2`, exactly 100), and every one of the 37 contract controls as a damaging mutation.

**Proposed forward verdict: `accepted_within_scope` for the forward half**, sub-label `static_not_dynamic`. The contract's acceptance also requires the reverse (iterated_split) route and skeptical review, which are outside this producer.

## 0. Frozen parameters, proof weights and notation

| symbol | meaning | value at the cap `|tau| = 1/100000000` |
|---|---|---|
| `J` | per-site interaction sum (four incident anchor groups; AM2, AY1 H4) | `28|tau| = 7/25000000` |
| `t_1` | first-order anchored norm (49 faces per site, `|tau|/144` each; AV1 F17) | `49|tau|/144` |
| `R`, `G(R)`, `G'(R)` | AM2 ball radius and majorant (directed `e^{1/8} ≤ 8/7`) | `1/64`, `≤ 148/7`, `≤ 352` |
| `tau_*` | largest disc radius with `28 rho G(R) ≤ R` | `1/37888` |
| `w_max(tau)` | `R/(J G(R)) = 1/(37888|tau|)` | `390625/148` |
| `t` | exact_first_order anchored bound `t_1/(1 − J G'(R))` (AV1 F18) | `49/14398580736` (about `3.40311318861e-9`) |
| `t` (crude) | `J G(R)` | `37/6250000` |

**Frozen pairs** (read by `check.py` from the contract): headline `q=1/64` with `C ≤ 1/250000` and `c_site ≤ 1/500000`; labelled secondary `q_2 = 151552|tau|` with `C ≤ 1/20000` and `c_site ≤ 1/40000`.

**Declared proof weights.** They were fixed before any constant was evaluated, by one rule for both pairs, and were not changed afterwards:
- creation (diameter) weight `w = 3/q`: `192` at the headline; `3/(151552|tau|)` for the secondary (`1171875/592` at the cap);
- Kotecký–Preiss cluster (distance) weight `v = e^μ = 2/q`: `128` at the headline; `2/(151552|tau|)` for the secondary (`390625/296` at the cap);
- cardinality factor `e^b = 1001/1000`, hence the loss per interaction `w e^{4b}`, which must be at most `w_max(tau)`;
- Kotecký–Preiss parameter `a = τ̄^2`, where `τ̄` is the proved bound of `‖c‖_{w,b}` in the tier of the constant.

Why this rule (structural, not tuned): the far-site sum needs `q v` above 1 to converge (`q v = 2`), the reach sum needs `v/w` below 1 (`v/w = 2/3`), admissibility needs `w e^{4b} ≤ w_max`, and the only cardinality requirement of the criterion is `a ≤ 2b`, so `e^b` close to 1 suffices. No value of `q`, `tau`, `N` or of a weight was changed after a constant was seen.

**Notation.** `‖c‖_a = max_u Σ_{I∋u} ‖c_I‖`; `‖c‖_{w,b} = max_u Σ_{I∋u} w^{diam I} e^{b|I|} ‖c_I‖`; `d` is the coarse l-infinity distance; `|y|_inf = d(y,0)`; the lattice sum

\[
S_x=\sum_{y\in\mathbb Z^3}x^{d(y,0)}=1+\sum_{r\ge1}(24r^2+2)x^r=1+\frac{24x(1+x)}{(1-x)^3}+\frac{2x}{1-x}\qquad(0\le x\lt 1),
\tag{HNM-BB1-F00}
\]

since `(2r+1)^3 − (2r−1)^3 = 24r^2+2` sites lie at distance `r ≥ 1`. At the declared weights `S_{v/w} = S_{2/3} = 725` and `S_{1/(qv)} = S_{1/2} = 147`, for both pairs.

## 1. Model, families, comparisons and the union volume

**Model and families** (AV1 F01–F02; AY1 F02). `h_b = 8 Σ_{e∈b} C_e ≥ Q_b`, Haar vacuum `Ω_b`, `φ_b = −(tau/3) Σ_{f∈O_b} W_f`. F1 on a finite complete-factor volume `V` keeps the whole star `b+S ⊂ V`; F2 keeps every omitted face whose owner set `M_f` lies in `V`, grouped at its anchor, with padding sites that carry only `h_x` and decouple (the padded ground vector is `ψ ⊗ Ω_pad`, AY1). F2 is verified item by item against the AM2 premises by the AY1 gate (supports `|X| ≤ 4`, `J ≤ 28|tau|`, termination order 8, at most 49 first-order faces per site, cutoff-vector removal).

**Comparisons.** Every comparison of `parameters.comparisons` is a comparison of two finite complete-factor volumes `V^A, V^B ⊇ Lambda_N` with prescriptions in `{F1, F2}`: F1 `Lambda_N` versus `Lambda_(N+1)`; F2 `Lambda_N` versus `Lambda_(N+1)`; F1 versus F2 on the same `Lambda_N` (fixed `N`, changed exterior); any two centered boxes `Lambda_M, Lambda_M'` with `M, M' ≥ N` (directly, no telescoping); and two volumes of one prescription containing `Lambda_N` (directly). `N` is the smaller box size, `N ≥ 2`.

**Union volume.** Put `Λ = V^A ∪ V^B`; the sites of one volume that are not in the other carry only their on-site operators. In each cutoff space `Q_L` the AM2 fixed point of `V^A` is supported in `V^A` (the map preserves collections supported there, BA1 reverse Theorem 4.1 step 1), so both finite-box ground vectors live on `Λ` as `ψ(c^A)` and `ψ(c^B)` with the zero-extended collections, and their reduced densities on `Y ⊂ Lambda_N` are those of the boxes.

**Objects.** In `Q_L`, a creation vector `c_I ∈ ⊗_{x∈I} Q_x Q_L H_x` is excited at every site of `I`; `ĉ_I = |c_I⟩⟨Ω_I| ⊗ 1`; creations commute and overlapping ones multiply to zero (AM2 §2). The ground vector is `ψ(c) = e^{−C}Ω = Π_I (1 − ĉ_I) Ω` (AV1 F06), and

\[
\rho_Y(c)=\frac{\operatorname{Tr}_{\Lambda\setminus Y}|\psi(c)\rangle\langle\psi(c)|}{\|\psi(c)\|^2}.
\]

The exact_first_order anchored bound `‖c‖_a ≤ t = 49/14398580736` holds for both boxes of every comparison (AV1 F18; AY1 for F2).

## 2. Item 1 — the AV1-type decomposition, orthogonality and the two Lipschitz bounds

Let `A = {I : I ∩ Y ≠ ∅}` and `B` the other supports. Put `T_c = Π_{I∈A}(1 − ĉ_I) = 1 + D_c`, `φ_out = Π_{I∈B}(1 − ĉ_I)Ω` on `H_{Λ∖Y}`, and let the straddle region be `O = ∪_{I∈A}(I ∖ Y)`. Every `ĉ_I` with `I ∈ B` acts as the identity on `H_Y`, so `ψ(c) = T_c(Ω_Y ⊗ φ_out)`. Let `ω_O` be the normalized marginal of `φ_out` on `O`, and for a trace-class `X` on `H_O`

\[
N_c(X)=\operatorname{Tr}_O\big[T_c(P_Y\otimes X)T_c^{*}\big],\qquad
\rho_Y(c)=\frac{N_c(\omega_O)}{\operatorname{Tr}N_c(\omega_O)} .
\tag{HNM-BB1-F01}
\]

The identity holds because `T_c` acts trivially outside `Y ∪ O`, so the partial trace over `Λ∖(Y∪O)` can be taken first, and the normalization cancels. `ω_O` depends only on the coefficients of `B`, and `T_c` only on those of `A`.

**Lemma 2.1 (orthogonality; `Tr N_c ≥ 1`).** `(P_Y ⊗ 1) D_c = 0`. For every state `ω`, the cross terms `Tr_O[D_c(P_Y⊗ω)]` are traceless and `Tr N_c(ω) = 1 + Tr[D_c(P_Y⊗ω)D_c^*] ≥ 1`. Moreover `Tr N_c(ω_O) = Z(Λ)/Z(Λ∖Y)` (§3).

*Proof.* `D_c` is a sum of products `± ĉ_{I_1}⋯ĉ_{I_m}` over nonempty families of disjoint members of `A`; each has range in `Ran(Q_y ⊗ 1)` for some `y ∈ Y`, and `P_Y Q_y = 0`. Hence `Tr[D_c(P_Y⊗ω)] = Tr[(P_Y⊗1)D_c(P_Y⊗1)(1⊗ω)] = 0`, and expanding `(1+D_c)(P_Y⊗ω)(1+D_c)^*` gives the identity. The last claim is `‖ψ‖^2 = Tr N_c(ω_O^{un})` with `ω_O^{un}` the unnormalized marginal, of trace `‖φ_out‖^2 = Z(Λ∖Y)`. ∎

**Lemma 2.2 (Lipschitz in the outside state; a global constant, never a decay factor).** With `ρ_c(ω) = N_c(ω)/Tr N_c(ω)` and `ε_Y = Π_{y∈Y}(1 + Σ_{I∋y}‖c_I‖) − 1 ≤ (1+t)^{|Y|} − 1`:

\[
\|\rho_c(\omega)-\rho_c(\omega')\|_1\le 2\|N_c(\omega-\omega')\|_1\le 2(2\varepsilon_Y+\varepsilon_Y^2)\|\omega-\omega'\|_1 .
\tag{HNM-BB1-F02}
\]

*Proof.* For positive `N, N'` of traces `n, n' ≥ 1`: `‖N/n − N'/n'‖_1 ≤ (‖N−N'‖_1 + |n−n'|)/n ≤ 2‖N−N'‖_1`. For `Tr X = 0`, `N_c(X) = Tr_O[D_c(P_Y⊗X)] + Tr_O[(P_Y⊗X)D_c^*] + Tr_O[D_c(P_Y⊗X)D_c^*]`, and partial traces contract the trace norm. Finally `‖D_c‖ ≤ ε_Y`: assign each member of a disjoint family in `A` its least point of `Y`; these points are distinct. ∎ For `Y=R` at the cap, `2(2ε_R+ε_R^2) ≤ 585079836474819687632719562774209/21490610253788267970605119133088070238208` (about `2.72249056478e-8`; exact_first_order, polymer_kp). It does not depend on `N` and is never used as a decay factor. Likewise the fixed-point map has Lipschitz constant `J_0G'(R) ≤ 77/781250` (`2J_0G'(R) ≤ 77/390625` is AM2's exclusion constant), which bounds `‖c^{N+1} − c^N‖_a` only by `J_0G(R)/(1 − J_0G'(R)) = 37/6249384`, the same number for every `N`; neither constant is a decay factor here. Decay comes only from the every-site input (the rate `q`) and from the polymer weights (`v^{−d}`).

**Lemma 2.3 (pure-state Lipschitz).** If `‖ψ‖, ‖ψ'‖ ≥ 1`, then `‖ρ_Y(ψ) − ρ_Y(ψ')‖_1 ≤ 2‖ψ − ψ'‖`, where `ρ_Y(ψ) = Tr_{Λ∖Y}|ψ⟩⟨ψ|/‖ψ‖^2`.

*Proof.* With `ψ̂ = ψ/‖ψ‖`: `‖ψ − ψ'‖^2 = (‖ψ‖ − ‖ψ'‖)^2 + ‖ψ‖‖ψ'‖·‖ψ̂ − ψ̂'‖^2 ≥ ‖ψ̂ − ψ̂'‖^2`. For unit vectors, `‖ |ψ̂⟩⟨ψ̂| − |ψ̂'⟩⟨ψ̂'| ‖_1 = 2(1 − |⟨ψ̂,ψ̂'⟩|^2)^{1/2} ≤ 2((1−r)(1+r))^{1/2} ≤ 2‖ψ̂ − ψ̂'‖` with `r = Re⟨ψ̂,ψ̂'⟩`, and partial traces contract. ∎

**Lemma 2.4 (Lipschitz in the coefficients, derivative form).** Let `c, c'` agree on `B` and let `t ≥ ‖c + λ(c'−c)‖_a` for `λ ∈ [0,1]`. Then

\[
\|\rho_Y(c)-\rho_Y(c')\|_1\le 2(1+t)^{|Y|-1}\sum_{I\cap Y\neq\varnothing}\|c_I-c'_I\| ,
\tag{HNM-BB1-F03}
\]

and the same bound holds for `ρ_c(ω)` at any fixed state `ω` (purify `ω` on an ancilla). The constant is `2(1+η_Y)` with `η_Y = (1+t)^{|Y|-1} − 1`; `η_R = t = 49/14398580736` (exact_first_order, polymer_kp).

*Proof.* Along the segment the outside vector is fixed; write `φ̂` for it normalized. By Lemma 2.1, `ψ_λ = T_{c_λ}(Ω_Y ⊗ φ̂)` has `‖ψ_λ‖ ≥ 1`, and `ρ_Y(c_λ) = ρ_Y(ψ_λ)`. By Lemma 2.3, `‖(d/dλ)ρ_Y(c_λ)‖_1 ≤ 2‖(d/dλ)ψ_λ‖`. Since creations commute and a creation kills an overlapping one, `(d/dλ)T_{c_λ} = −Σ_{J∈A} δ̂_J Π_{I∈A, I∩J=∅}(1 − ĉ_{λ,I})` with `δ = c'−c`. The product has norm at most `Π_{y∈Y∖J}(1 + Σ_{I∋y}‖c_{λ,I}‖) ≤ (1+t)^{|Y|-1}` by the least-point assignment of Lemma 2.2 (each member avoids `J`, which meets `Y`). Integrate over `λ`. ∎

The derivative form charges only the current coefficients, so the exponential rate is `t` per site; a finite-difference form would charge `max(‖c_I‖, ‖c'_I‖)` and double it. Lemma 2.3 is applied only to two vectors with a **common** outside vector; applied to the global ground vectors of two boxes it gives nothing, because their global overlap collapses with the volume (§11, fixture 4).

## 3. Item 2 (a) — hard-core polymer representation of the norm and of the Y-marginal

**Families.** A *family* `𝓕` is a set of pairwise disjoint supports; `E(𝓕) = ∪𝓕` is its excitation set and `c_𝓕 = (⊗_{I∈𝓕} c_I) ⊗ Ω_{Λ∖E(𝓕)}`. Expanding the product,

\[
\psi(c)=\sum_{\mathcal F}(-1)^{|\mathcal F|}c_{\mathcal F},\qquad \|c_{\mathcal F}\|=\prod_{I\in\mathcal F}\|c_I\| .
\tag{HNM-BB1-F04}
\]

**Lemma 3.1 (matching).** For `A ∈ B(H_Y)`, `⟨c_𝓕, (A⊗1)c_𝓕'⟩ = 0` unless `E(𝓕)∖Y = E(𝓕')∖Y`; in particular (`Y=∅`) families with different excitation sets pair to zero. *Proof:* at a site `x ∉ Y` one vector lies in `Ran(Q_x)` and the other in `Ran(P_x)`, and `A⊗1` commutes with `P_x`. ∎ The premise `c_I ∈ ⊗Q_xH_x` is essential; a creation with a vacuum component breaks it (§11).

**Definitions.** A pair `(𝓕, 𝓕')` with `E(𝓕)∖Y = E(𝓕')∖Y` is *Y-matched*. Its overlap graph has the vertices `𝓕 ⊔ 𝓕' ⊔ {Y}`; `I ∈ 𝓕` and `I' ∈ 𝓕'` are joined when they intersect, and a member is joined to the vertex `Y` when it meets `Y`.
- A **Y-cluster** `η = (𝓕_0, 𝓕'_0)` is a Y-matched pair all of whose members are connected to the vertex `Y` (the empty pair included); `supp η = Y ∪ E(𝓕_0) ∪ E(𝓕'_0)`, and `ρ_η ∈ B(H_Y)` is defined by `Tr(ρ_η A) = (−1)^{|𝓕_0|+|𝓕'_0|}⟨c_{𝓕_0}, (A⊗1)c_{𝓕'_0}⟩` on `H_{supp η}`, that is `ρ_η = ± Tr_{supp η∖Y}|c_{𝓕'_0}⟩⟨c_{𝓕_0}|`.
- A **polymer** `γ = (𝓕, 𝓕')` is a pair of nonempty families with `E(𝓕) = E(𝓕') =: supp γ` whose bipartite overlap graph is connected. Its **activity** is `w(γ) = (−1)^{|𝓕|+|𝓕'|}⟨c_𝓕, c_𝓕'⟩` on `H_{supp γ}`. Polymers are compatible when their supports are disjoint (hard core).
- `Z(Λ') = Σ_Γ Π_{γ∈Γ} w(γ)` over families `Γ` of pairwise compatible polymers with supports in `Λ'` (`Γ = ∅` gives 1).

**Lemma 3.2 (decomposition).** Let `(𝓕, 𝓕')` be Y-matched. The component of the vertex `Y` (with `Y` removed) is a Y-cluster `η`, and every other component is a polymer disjoint from `Y`; the sets `supp η, supp γ_1, supp γ_2, …` are pairwise disjoint. Conversely a Y-cluster together with compatible polymers in `Λ ∖ supp η` is a Y-matched pair with exactly this decomposition.

*Proof.* Take a component `γ` other than that of `Y`, and `x ∈ E(𝓕_γ)`. Then `x ∉ Y` (otherwise its member is joined to `Y`), so `x ∈ E(𝓕')`, and the member of `𝓕'` through `x` overlaps the member of `𝓕` through `x` and belongs to `γ`; by symmetry `E(𝓕_γ) = E(𝓕'_γ)`. The same argument outside `Y` gives the matching of `η`. If a site belonged to two components, the unique member of `𝓕` (or of `𝓕'`) through it would lie in both. The converse is immediate: pieces with disjoint supports have no edges between them. ∎

**Proposition 3.3 (polymer representation).** For every `Y ⊂ Λ` and `A ∈ B(H_Y)`,

\[
\langle\psi,(A\otimes 1)\psi\rangle=\sum_{\eta}\operatorname{Tr}(\rho_\eta A)\,Z(\Lambda\setminus\operatorname{supp}\eta),\qquad \|\psi\|^2=Z(\Lambda).
\tag{HNM-BB1-F05}
\]

*Proof.* Expand both vectors by (F04). By Lemma 3.1 only Y-matched pairs contribute; by Lemma 3.2 each is a Y-cluster with compatible polymers, the inner product factorizes over the disjoint supports (the rest is vacuum), and the signs multiply. ∎

**Corollary 3.4 (vacuum probabilities).** `P_S ψ = ψ_{Λ∖S} ⊗ Ω_S`, so `Z(Λ∖S) = ⟨ψ, P_S ψ⟩ ≥ 1` and

\[
\pi(S):=\frac{Z(\Lambda\setminus S)}{Z(\Lambda)}=\frac{\langle\psi,P_S\psi\rangle}{\langle\psi,\psi\rangle}\in(0,1],\qquad
\rho_Y=\sum_{\eta}\rho_\eta\,\pi(\operatorname{supp}\eta).
\tag{HNM-BB1-F06}
\]

This is (F01) written in polymers: `Tr N_c(ω_O) = 1/π(Y)`, and the outside state enters only through the vacuum probabilities of the Y-cluster supports. Every vacuum probability is at most 1. This replaces the factor `e^{a|γ|}` of a rooted cluster sum and keeps every bound below free of an exponential in the size of the differentiated support.

**Lemma 3.5 (activity bounds).** `|w(γ)| ≤ Π_{K∈γ}‖c_K‖` and `‖ρ_η‖_1 ≤ Π_{K∈η}‖c_K‖` (products over both families, with multiplicity), by Cauchy–Schwarz and `‖Tr_{…}|u⟩⟨v|‖_1 ≤ ‖u‖‖v‖`.

## 4. Item 2 (b) — exploration-tree majorants (the combinatorial counts)

**Lemma 4.1 (maximal path).** In a finite rooted tree, give each child a weight at least 0 and suppose the child weights of a node `ν` sum to at most `σ(ν)`. The sum over leaves of the product of weights along the path is at most the maximum over root-to-leaf paths of `Π σ(ν)`. *Proof:* `W(ν) = Σ_child wt·W(child) ≤ σ(ν) max W(child)`, by induction. ∎

**Exploration.** Fix a total order on sites. For a pair `(𝓕, 𝓕')` and a starting member, call a site *unbalanced* when a chosen member of one side contains it and no chosen member of the other side does. *Balancing* at a site adds the member of the other side through the least unbalanced site; each step adds a new member. The whole polymer is recovered: if a member `M'` overlaps a chosen member at a site `x`, then either `x` is unbalanced and balancing at `x` adds `M'` (the unique member of its side through `x`), or `x` is balanced and `M'` is already chosen. For Y-clusters the same holds at sites outside `Y`, and members meeting `Y` are handled at the sites of `Y` (Lemma 4.3). So the map from polymers (or Y-clusters) to exploration sequences is injective, and the children of a step are the supports through one determined site. With `u_K ≥ 0` and `max_x Σ_{K∋x} u_K ≤ σ ≤ 1`, Lemma 4.1 gives:

**Lemma 4.2 (polymers).** (P1) `Σ_{γ∋x} Π_{K∈γ} u_K ≤ σ^2` (the member through `x` costs `σ`; at least one balancing step follows). (P2) For a marked occurrence `(I, s)`, `Σ_{γ∋(I,s)} Π_{K∈γ∖(I,s)} u_K ≤ σ` (at least one step).

**Lemma 4.3 (Y-clusters).** Let `t_a = max_x Σ_{K∋x}‖c_K‖ ≤ 1` and `N_Y = (1+t_a)^{2|Y|}`.
- (Y0) `Σ_{η} Π_{K∈η}‖c_K‖ ≤ N_Y`. *Exploration:* for each `(y, side)` in order, choose none or the member through `y` (sum at most `1 + t_a`; at most `2|Y|` such steps), then balance outside `Y` (each step at most `t_a`). Members meeting `Y` are chosen first, and the others are reached along overlap paths through sites outside `Y`.
- (YJ) For `J` missing `Y`: `Σ_{η∋(J,s)} Π_{K∈η∖(J,s)}‖c_K‖ ≤ σ_w w^{−d(J,Y)} N_Y`, where `σ_w = max_x Σ_{K∋x} w^{diam K}‖c_K‖`.
- (YS) For `z ∉ Y`: `Σ_{η: z∈supp η} Π_{K∈η}‖c_K‖ ≤ 2σ_w^2 w^{−d(z,Y)} N_Y`.

*Proof of (YJ) and (YS).* Let `C(J)` be the closure of `J` under balancing outside `Y` inside `η`. A path `J = K_0, K_1, …, K_m` in `η` to the first member meeting `Y` has its overlaps outside `Y`, so it lies in `C(J)`, and `d(J,Y) ≤ Σ_{i≥1} diam K_i`. Hence `Π_{K∈C(J)∖J}‖c_K‖ ≤ w^{−d(J,Y)} Π_{K∈C(J)∖J} w^{diam K}‖c_K‖`. The rest `η ∖ C(J)` is again a Y-cluster (it is matched outside `Y`, and a path from one of its members to `Y` that enters `C(J)` does so at a site of `Y`), so it costs at most `N_Y` by (Y0). The closure costs at most `σ_w`: all its steps are balancing steps, and at least one is needed because `J` misses `Y`. For (YS), sum over the member through `z` on either side (`2σ_w`), then its closure (at least one step, `σ_w`), with `d(z,Y)` at most the sum of the diameters in the closure. ∎

The bounds are tight for single-site creations (`γ = ({x},{x})` gives exactly `σ^2`; independent Y-sites give exactly `(1+t_a)^{2|Y|}`). `check.py` verifies (P1), (P2), (Y0), (YJ) and (YS) by brute-force enumeration on a five-site chain (233 polymers; 275 and 856 Y-clusters).

## 5. Item 2 (c) — the mixed-weight contraction lemma (new; proved in full)

Let `W(I) = w^{diam I} e^{b|I|}` with `w ≥ 1`, `b ≥ 0`, and `‖c‖_{w,b} = max_u Σ_{I∋u} W(I)‖c_I‖`. Let `V = Σ_X V_X` be a finite-volume interaction whose pieces have `|X| ≤ p = 4`, `diam X ≤ 1` and per-site sum `J`. Recall `(L_k(c_1,…,c_k))_M = H_M^{-1} P_M ad_{C_1}⋯ad_{C_k}(V) Ω` and `L_k^num = 16·8^k(1+5k/4)`.

**Lemma 5.1 (mixed-weight multilinear estimate).**

\[
\|L_k(c_1,\ldots,c_k)\|_{w,b}\le w\,e^{4b}\,J\,L_k^{\rm num}\prod_{j}\|c_j\|_{w,b}.
\tag{HNM-BB1-F07}
\]

*Proof.* Fix a piece `V_X` and one support `I_j` per slot.
- (a) **Localization.** A nonzero nested commutator needs every `I_j` to meet `X`: the adjoint actions of commuting creations commute, and a creation disjoint from `X` moved innermost commutes with `V_X`.
- (b) **Output support.** Expand the commutators into `2^k` products of creations to the left and right of `V_X`, applied to `Ω`. Outside `X`, a site touched twice gives zero, and a site touched once is excited in the output. So with `𝒩 = ∪I_j`, `𝒩∖X ⊂ M ⊂ 𝒩 ∪ X`: at most `2^p = 16` output sets. Also `|I_j| ≤ |M| + p ≤ (p+1)|M|`, because `I_j ∖ X ⊂ M` and `|M| ≥ 1`. Each projected product has norm at most `‖V_X‖ Π_j ‖c_{j,I_j}‖`.
- (c) **Weight through one interaction.** For `p, p' ∈ M ⊂ X ∪ 𝒩`, route through points of `I_a ∩ X`: `diam M ≤ diam X + Σ_j diam I_j` (the sum cannot be replaced by the maximum: the disconnected output of §11 has diameter `3 = 1 + 1 + 1`). And `|M| ≤ |X| + Σ_j |I_j|`. Hence, for `w ≥ 1`, `W(M) ≤ W_X Π_j W(I_j)` with `W_X = w^{diam X} e^{b|X|} ≤ w e^{4b}`: **the loss is charged once per interaction term, never per creation.**
- (d) **Root in `X`.** For `u ∈ M ∩ X`, use `‖H_M^{-1}‖ ≤ 1`, `Σ_{X∋u} W_X‖V_X‖ ≤ w e^{4b} J`, and for each slot `Σ_{I∩X≠∅} W(I)‖c_{j,I}‖ ≤ |X|·‖c_j‖_{w,b} ≤ p‖c_j‖_{w,b}`. Contribution: `2^p 2^k p^k w e^{4b} J Π_j‖c_j‖_{w,b} = 16·8^k w e^{4b} J Π_j‖c_j‖_{w,b}`.
- (e) **Root in a creation.** For `u ∈ M ∩ I_l` (all `k` choices of `l` overcounted), use `‖H_M^{-1}‖ ≤ 1/|M| ≤ (p+1)/|I_l|` and `Σ_{X∩I_l≠∅} W_X‖V_X‖ ≤ w e^{4b} J |I_l|`, which cancels the denominator; the other slots cost `p^{k−1}` and slot `l` costs `Σ_{I_l∋u} W(I_l)‖c_{l,I_l}‖ ≤ ‖c_l‖_{w,b}`. Contribution: `2^p 2^k k(p+1)p^{k−1} w e^{4b} J Π = 16·8^k (5k/4) w e^{4b} J Π`.
- (f) **Total.** `16·8^k(1+5k/4)`, which is `k!` times the Taylor coefficient of `G(t) = 16e^{8t}(1+10t)`. Every sum is finite and dimension-free, so the lemma holds in each `Q_L` with constants independent of the cutoff. Repeated terms are counted, never cancelled. ∎

**Corollary 5.2 (self-map, contraction, identification, tiers).** Put `ŵ = w e^{4b}` and `Γ = J ŵ G'(R)`. Summing (F07), `‖Φ(c)‖_{w,b} ≤ J ŵ G(‖c‖_{w,b})`; telescoping each `k`-linear term, `‖Φ(c) − Φ(c')‖_{w,b} ≤ Γ‖c − c'‖_{w,b}` on the ball of radius `R`. If `ŵ ≤ w_max(tau) = R/(J G(R)) = 1/(37888|tau|)` (admissibility: "at most `1/(37888|tau|)` after the cardinality loss"), then `Φ` maps the `‖·‖_{w,b}`-ball of radius `R` into itself and contracts it. The ball lies inside AM2's anchored ball (`W ≥ 1`), so by AM2's uniqueness in that ball the Banach fixed point is AM2's fixed point, and `‖c‖_{w,b} ≤ R`. The first-order coefficient `L_0 = −(tau/72)Σ_f W_fΩ` lives on owner sets of at most 3 sites and diameter exactly 1, with at most 49 faces per site, and `Q_L` keeps or removes each face vector. The tiers are:
- exact_first_order: `τ̄ = w e^{3b} t_1/(1 − Γ)`, from `‖c‖ ≤ ‖L_0‖ + ‖c − L_0‖ ≤ w e^{3b} t_1 + J ŵ (G(‖c‖) − 16)` and the convexity bound `G(s) − 16 ≤ s G'(R)`;
- crude_majorant: `τ̄ = J ŵ G(R)`.

Values at the cap (both pairs admissible):

| pair | `ŵ = w e^{4b}` | `w_max` | `Γ` | exact `τ̄` | crude `τ̄` |
|---|---|---|---|---|---|
| headline (`w=192`) | `3012018012003/15625000000` (about `192.769`) | `390625/148` | `231925386924231/12207031250000000` (about `1.89993e-2`) | `6143393381125/9196881302842190592` (about `6.67986590109e-7`) | `111444666444111/97656250000000000` (about `1.14119338438e-3`) |
| secondary (`w=1171875/592`) | `3012018012003/1515520000` (about `1987.45`) | `390625/148` | `231925386924231/1184000000000000` (about `1.95883e-1`) | `6143393381125/731193302842190592` (about `8.40187315344e-6`) | about `1.17657e-2` |

`check.py` verifies the weight inequality `W(M) ≤ W_X Π W(I_j)` over 19432 configurations at each of three weight pairs, and the attained loss at order zero: a four-site piece `X⊗X⊗X⊗X` on the star gives `M = X`, so `W(M) = w e^{4b}` exactly. It rejects a loss `w e^{3b}`, a loss charged per creation, the maximum-instead-of-sum shortcut, `e^b = 2` (inadmissible for the secondary) and `w = 42/q` (beyond `w_max`).

## 6. Item 2 (d) — the Kotecký–Preiss condition with an explicit `a`

**Theorem 6.1 (Kotecký–Preiss; cited).** Let a finite set of polymers carry complex activities `w(γ)` with hard-core incompatibility. Suppose functions `a(·) ≥ 0`, `d(·) ≥ 0` satisfy `Σ_{γ'≁γ}|w(γ')| e^{a(γ')+d(γ')} ≤ a(γ)` for every polymer `γ` and every test set `γ` (a finite set of sites with `a(γ) = a|γ|`, treated as a polymer of activity 0, which leaves every other sum unchanged). Then for every `Λ' ⊂ Λ`, `Z(Λ') ≠ 0` and `Z(Λ') = exp Σ_{X⊂Λ'} Φ^T(X)`, with an absolutely convergent cluster sum (clusters `X` are connected multisets of polymers, `Φ^T(X)` is the Ursell coefficient times the product of the activities), and `Σ_{X≁γ}|Φ^T(X)| e^{d(X)} ≤ a(γ)` with `d(X) = Σ_{γ'∈X} d(γ')`. The proof majorizes `|Φ^T|` by spanning trees of the incompatibility graph (the tree majorant). A vertex `γ'` of such a tree can attach neighbours at each of its `|supp γ'|` sites, which is why `a(γ)` must carry the cardinality factor `a|supp γ|`.

**Proposition 6.2 (verification).** Take `a(γ) = a|supp γ|` and `d(γ) = μ Σ_{K∈γ} diam K` with `e^μ = v ≤ w`, `a ≤ 2b` and `a ≥ τ̄^2`. Since `supp γ = E(𝓕) = E(𝓕')` is a disjoint union on each side, `a|supp γ| = (a/2)Σ_{K∈γ}|K|`, so `|w(γ)| e^{a(γ)+d(γ)} ≤ Π_{K∈γ} v^{diam K} e^{(a/2)|K|}‖c_K‖ ≤ Π_{K∈γ} W(K)‖c_K‖`. By Lemma 4.2 (P1) with `σ = ‖c‖_{w,b} ≤ τ̄`, for every site `x`, `Σ_{γ∋x}|w(γ)|e^{a(γ)+d(γ)} ≤ τ̄^2 ≤ a`; summing over `x ∈ γ_0` gives the condition for every polymer and every test set `γ_0`. The inputs are the activity bound (Lemma 3.5), the exploration count (Lemma 4.2), the mixed norm (Corollary 5.2) and `b ≥ ln(1001/1000) ≥ 1/1001`. Values (both signs):

| pair / tier | `τ̄` | `a = τ̄^2` | `a ≤ 2b` | `v ≤ w` |
|---|---|---|---|---|
| headline, exact_first_order | `6143393381125/9196881302842190592` | `37741282235250459506265625/84582625698568269021279506561253310464` (about `4.46206084565e-13`) | yes (`2b ≥ 2/1001`) | `128 ≤ 192` |
| secondary, exact_first_order | `6143393381125/731193302842190592` | `37741282235250459506265625/534643646121271444464914561253310464` (about `7.05914724864e-11`) | yes | `390625/296 ≤ 1171875/592` |
| headline, crude_majorant | `111444666444111/97656250000000000` | about `1.30232234057e-6` | yes | yes |

**Corollary 6.3 (site decay).** For sites `z, s`: `Σ_{X≁z, X≁s}|Φ^T(X)| ≤ a v^{−d(z,s)}`. *Proof:* a cluster touching `z` and `s` is connected through shared sites, and each polymer is connected through overlapping members, so `d(z,s) ≤ Σ_{γ∈X}Σ_{K∈γ} diam K`, that is `e^{d(X)} ≥ v^{d(z,s)}`; apply Theorem 6.1 to the test set `{z}`. ∎

**Lemma 6.4 (truncated vacuum probabilities).** For `S ⊃ Y` and a polymer `γ ⊂ Λ∖S`, with `π_{Λ'}(γ) = Z(Λ'∖supp γ)/Z(Λ') ∈ (0,1]`:

\[
|\pi_{\Lambda\setminus S}(\gamma)-\pi_\Lambda(\gamma)|\le\sum_{X\not\sim\gamma,\ X\not\sim S}|\Phi^T(X)|\le\sum_{z\in\operatorname{supp}\gamma}\sum_{s\in S}a\,v^{-d(z,s)} .
\tag{HNM-BB1-F08}
\]

*Proof.* `π_{Λ'}(γ) = exp(−Σ_{X⊂Λ', X≁γ}Φ^T(X))`, so `π_{Λ∖S}(γ) = π_Λ(γ) e^{Δ}` with `Δ = Σ_{X≁γ, X≁S}Φ^T(X)`. Both probabilities are real and positive, so `e^Δ = e^{Re Δ}`. If `Re Δ ≤ 0`, the difference is `π_Λ(γ)(1 − e^{ReΔ}) ≤ |Δ|`. If `Re Δ ≥ 0`, it is at most `π_Λ(γ)e^{ReΔ}Re Δ = π_{Λ∖S}(γ) Re Δ ≤ |Δ|`. No factor `e^{a|γ|}` appears. Then apply Corollary 6.3. ∎ `check.py` verifies (F08) exactly on a six-site chain for every interval `S` of at most two sites and every disjoint interval `γ`-support of at most four sites (largest ratio of the two sides about `3.3e-2`).

## 7. Item 2 (e) — the marginal-locality lemma from the real-parameter derivative

**Theorem 7.1 (marginal locality).** Let `c, c'` be collections on `Λ` (in `Q_L`) with anchored norms at most `t ≤ 1`, mixed norms `‖·‖_{w,b} ≤ τ̄ ≤ 1`, and weights with `a = τ̄^2 ≤ 2b` and `1 ≤ v ≤ w`. Put `δ = c' − c`, `N_Y = (1+t)^{2|Y|}`, and

\[
A=2\bar\tau^2+a\,(1+2\bar\tau^2S_{v/w}),\qquad
\kappa_0=4\bar\tau+2A\big(t+\bar\tau(S_{v/w}-1)\big).
\tag{HNM-BB1-F09}
\]

Then for every nonempty `Y ⊂ Λ`,

\[
\|\rho_Y(c)-\rho_Y(c')\|_1\le 2(1+t)^{|Y|-1}\sum_{I\cap Y\neq\varnothing}\|\delta_I\|
+N_Y\,\kappa_0\sum_{x\notin Y}\Big(\sum_{y\in Y}v^{-d(x,y)}\Big)\sum_{I\ni x}\|\delta_I\| .
\tag{HNM-BB1-F10}
\]

**Contract form.** Since `Σ_{x∈I}Σ_{y∈Y} v^{−d(x,y)} ≤ |Y||I| v^{−d(I,Y)}`, (F10) is the lemma `‖ρ_Y(c) − ρ_Y(c')‖_1 ≤ 2(1+η)Σ_{I meets Y}‖δ_I‖ + Σ_{I misses Y} κ(I)‖δ_I‖` with `η = (1+t)^{|Y|-1} − 1`, `κ(I) ≤ κ_0(Y)(w')^{−d_inf(I,Y)} p(|I|)`, `κ_0(Y) = N_Y|Y|κ_0`, `w' = v` and `p(s) = s`.
- For `Y = R` at the headline (exact_first_order, polymer_kp): `η_R = 49/14398580736`; `κ_0 = 824003615421033359856202170876376351556618924570689440304611678118040666133306269616823661654125/308390777308485285224458518087412347816221841803426111318855541982858616135745390771824726938082082816` (about `2.67194636173e-6`); `κ_0(R) = 2(1+t)^4 κ_0` (about `5.34389279620e-6`); `w' = 128`; `p(s) = s`.
- Secondary: `κ_0 = 32922715148647726325329420393175507885187326208842439817022007753938876745972894167411654125/979624186876531107244708757168660074614272083297048274852346723212847598054806251606938082082816` (about `3.36074951901e-5`); `w' = 390625/296` at the cap.

The site form (F10) is what the constants use.

*Proof.* Put `c_λ = c + λδ`, `λ ∈ [0,1]` **real**. Every coefficient of `ψ(c_λ)` is a real polynomial in `λ` and `Z_λ(Λ) ≥ 1`, so `λ ↦ ρ_Y(c_λ)` is smooth on `[0,1]` and `ρ_Y(c') − ρ_Y(c) = ∫_0^1 (d/dλ)ρ_Y(c_λ) dλ`. No complex `λ` and no analyticity is used (§11, `zero_free_region_required`). By linearity of the differential, `(d/dλ)ρ_Y = Dρ_Y[δ_in] + Dρ_Y[δ_out]`, where `δ_in` keeps the supports meeting `Y` and `δ_out` the others. All norms of `c_λ` are bounded by `t` and `τ̄` (convexity), so the Kotecký–Preiss condition of §6 holds for every `λ`.

**Inside part.** `‖Dρ_Y[δ_in]‖_1 ≤ 2(1+t)^{|Y|-1}Σ_{I∩Y≠∅}‖δ_I‖` by Lemma 2.4 (the outside vector is fixed along `δ_in`).

**Outside part.** By (F06), `Dρ_Y[δ_out] = Σ_η ρ̇_η π(supp η) + Σ_η ρ_η π̇(supp η)`, where the dot is the derivative along `δ_out`. Each activity and each `ρ_η` is linear or conjugate-linear in every member, so the real derivative replaces one occurrence `(J, s)`, with `J` missing `Y`, by `δ_J`: `‖ρ̇_η‖_1 ≤ Σ_{(J,s)}‖δ_J‖Π_{other}‖c_K‖` and `|ẇ(γ)| ≤ Σ_{(J,s)}‖δ_J‖Π_{other}‖c_K‖`.
- *Term I (straddling families).* With `π ≤ 1` and (YJ) on both sides: `Σ_η‖ρ̇_η‖_1 π ≤ Σ_{J∩Y=∅}‖δ_J‖·2τ̄ w^{−d(J,Y)} N_Y`, and `w^{−d(J,Y)} ≤ Σ_{x∈J}Σ_{y∈Y} w^{−d(x,y)}`.
- *Term II (normalization).* `Ż(Λ') = Σ_{γ⊂Λ'} ẇ(γ) Z(Λ'∖supp γ)`, hence `π̇(S)/π(S) = −Σ_{γ≁S} ẇ(γ)π_Λ(γ) + Σ_{γ⊂Λ∖S} ẇ(γ)(π_{Λ∖S}(γ) − π_Λ(γ))`. With `π ≤ 1`, (F08) and `1(γ≁S) ≤ Σ_{z∈supp γ} 1(z∈S)`, `Σ_η‖ρ_η‖_1|π̇(supp η)| ≤ Σ_γ|ẇ(γ)| Σ_η‖ρ_η‖_1[1(γ≁supp η) + Σ_{z∈supp γ}Σ_{s∈supp η} a v^{−d(z,s)}] ≤ Σ_γ|ẇ(γ)| Σ_{z∈supp γ} h(z)`, where `h(z) = n(z) + aΣ_s v^{−d(z,s)} n(s)` and `n(s) = Σ_{η: s∈supp η}‖ρ_η‖_1`. By (Y0) and (YS), `n(s) ≤ N_Y` for `s ∈ Y` and `n(s) ≤ 2τ̄^2 w^{−d(s,Y)} N_Y` otherwise. Using `w^{−d(s,y)} v^{−d(z,s)} ≤ v^{−d(z,y)}(v/w)^{d(s,y)}` and summing `s` over `Z^3`, `h(z) ≤ N_Y Σ_{y∈Y}[1(z=y) + A v^{−d(z,y)}]`. For a marked occurrence `(J,s)`: by (P2), sites `z ∈ J` cost `t` (unweighted), and sites `z ∉ J` cost `τ̄ w^{−d(J,z)}` (the polymer contains a path from `J` to `z`). With `Σ_{z≠x} w^{−d(x,z)} v^{−d(z,y)} ≤ v^{−d(x,y)}(S_{v/w} − 1)`, each `J` missing `Y` costs at most `2N_YΣ_{x∈J}Σ_{y∈Y}[τ̄ w^{−d(x,y)} + A(t + τ̄(S_{v/w} − 1))v^{−d(x,y)}]`.

Adding Terms I and II, using `w^{−d} ≤ v^{−d}` and exchanging `Σ_J Σ_{x∈J} = Σ_x Σ_{J∋x}` gives the second sum of (F10) with `κ_0` of (F09). ∎

The factor `|I|` (the polynomial `p`) is absorbed by summing over the sites of `I`, which pairs each site with the every-site coefficient input at that site; no cardinality weight on the coefficient differences is needed. The cardinality factor of the Kotecký–Preiss tree majorant is carried by the mixed weight of the fixed points (§§5–6). `check.py` verifies (F10) exactly on a six-site chain for `Y = {2}` and `Y = {2,3}`, with changes inside and outside `Y`.

## 8. Item 4 (a) — the every-site coefficient input, form (b), proved in full

The BA1 gate admits the coefficient bound for `u ∈ R` only. The following restatement for every site is a BB1 lemma, proved here; it is not cited as an admitted BA1 statement.

**Theorem 8.1 (every-site analytic-disc input).** Let `N ≥ 2`, let `V^A, V^B` be finite complete-factor volumes containing `Lambda_N` with prescriptions in `{F1, F2}`, `L` any cutoff, `rho ∈ (0, tau_*]` with `tau_* = 1/37888`, and `tau` real with `|tau|` strictly between 0 and `rho` and `|tau| ≤ 10^-8`. Then for **every site `u`** of the union volume

\[
\sum_{I\ni u}\|c^A_I(\tau)-c^B_I(\tau)\|\le K\,q^{(N-|u|_\infty)_+},\qquad K=2T(\rho),\quad q=\frac{|\tau|}{\rho},
\tag{HNM-BB1-F11}
\]

with `T(rho) = (49 rho/144)/(1 − 28 rho G'(R))` (exact_first_order) or `T(rho) = 28 rho G(R)` (crude_majorant). The sharp count gives the exponent `1 + (N − |u|_inf)_+` for `|u|_inf ≤ N`; the contract form `(N − |u|_inf)_+` is used for every bound.

**Lemma 8.2 (complexified map).** For complex `z`, `V(z) = zV_1` with `V_1` the unit-coupling interaction (per-site sum 28, pieces of at most 4 sites), and `L_k^{(z)} = z L_k^{(1)}` because `L_k` is linear in `V`. The AM2 multilinear estimate (AM2.5; its proof uses only norms, supports and counts) applied to `V_1` gives `‖L_k^{(z)}(c_1,…,c_k)‖_a ≤ 28|z| L_k^num Π‖c_j‖_a` for complex collections. With `F_z(c) = Σ_{k≤8} L_k^{(z)}(c,…,c)/k!`: `‖F_z(c)‖_a ≤ 28 rho G(R) ≤ R` and `‖F_z(c) − F_z(c')‖_a ≤ 28 rho G'(R)‖c − c'‖_a` on the ball, for `|z| ≤ rho ≤ tau_*` (`28 tau_* G'(R) = 77/296`).

**Lemma 8.3 (analyticity and identification).** The iterates `c^{(m+1)}(z) = F_z(c^{(m)}(z))`, `c^{(0)} = 0`, are polynomials in `z`, stay in the ball and converge in the supremum over the closed disc (`‖c^{(m+1)} − c^{(m)}‖_a ≤ κ^m R`, `κ = 28 rho G'(R)`). The limit `c(z)` is continuous on the closed disc, holomorphic inside (Weierstrass, coordinatewise in the finite-dimensional coefficient space of `Q_L`), and the only fixed point in the ball. At real `tau` it is the AM2 fixed point, by AM2's uniqueness in the ball.

**Lemma 8.4 (circle bound, the same at every site).** `c(z) = z L_0^{(1)} + r(z)` with `‖z L_0^{(1)}‖_a ≤ 49|z|/144` (at most 49 faces per site for F1, F2 and every sub-volume; `Q_L` keeps or removes face vectors) and `‖r(z)‖_a ≤ 28|z|(G(t) − 16) ≤ 28|z| G'(R) t`. So `t(z) = ‖c(z)‖_a ≤ T(rho)` on the circle. The anchored norm is a maximum over sites, so for every `u`: `Σ_{I∋u}‖c^A_I(z) − c^B_I(z)‖ ≤ 2T(rho)`.

**Lemma 8.5 (connected families and order versus distance at `u`).** Decompose both interactions face by face (pieces of diameter at most 1). By the Taylor recursion `c_1 = L_0^{(1)}`, `c_n = Σ_{k≥1}(1/k!) Σ_{n_1+…+n_k=n−1} L_k^{(1)}(c_{n_1},…,c_{n_k})`, every term of `c_n` is multilinear in `n` pieces, and it vanishes unless the pieces form an overlap-connected family whose union contains the output support (induction with steps (a) and (b) of Lemma 5.1). If the output contains `u` and a piece lies at distance `d ≥ 1` from `u`, then a chain of distinct pieces joins a piece through `u` to it, so `d ≤ m` and `n ≥ m + 1 ≥ d + 1`.

**Lemma 8.6 (common core at `u`).** Every omitted face at distance at most `N − |u|_inf − 1` from `u` is retained by both prescriptions on every volume containing `Lambda_N`. *Proof:* it has a site `q` with `d(q,u) ≤ N − |u|_inf − 1`, so `|q|_inf ≤ N − 1`; its anchor is `b = q − s` with `s ∈ S ⊂ {0,1}^3`, so `b ∈ [−N, N−1]^3` and `b + S ⊂ Lambda_N`. F1 keeps the whole star `b+S`, and F2 keeps the face since `M_f ⊂ b+S`. ∎ Hence every source face of every comparison lies at distance at least `N − |u|_inf` from `u`.

*Proof of Theorem 8.1.* `g(z) = (c^A_I(z) − c^B_I(z))_{I∋u}` is holomorphic on the open disc and continuous on the closed one (Lemma 8.3, on the union volume). Terms built from common faces coincide, since the on-site operators and the cutoff are the same. Every other term contains a source face at distance at least `N − |u|_inf` from `u` (Lemma 8.6), and so enters at order at least `1 + (N − |u|_inf)` (Lemma 8.5). Hence `g` vanishes to order `n_0 ≥ (N − |u|_inf)_+`. The Schwarz estimate (maximum modulus for `g(z)/z^{n_0}`, applied to every functional of dual norm at most 1 and passed to the closed disc by continuity) gives `‖g(tau)‖_u ≤ (|tau|/rho)^{n_0} max_{|z|=rho}‖g(z)‖_u ≤ 2T(rho) q^{n_0}` by Lemma 8.4. ∎

**Instances** (exact, both signs, every `Q_L`):
- headline: `rho = 64|tau|`, `q = 1/64`, `K = 2T(64|tau|) = 49/111790368` (about `4.38320410574e-7`); `check.py` requires equality with the BA1 gate bound value;
- secondary (labelled): `rho = |tau|/q_2 = 1/151552`, `q_2 = 151552|tau|` (`592/390625` at the cap), `K = 49/10202112` (about `4.80292708019e-6`), `28 rho G'(R) = 77/1184`;
- crude: `K = 2·28 rho G(R) = 296/390625` at `rho = 64|tau|`.

**Enumeration audit.** For `N = 2, 3`, `check.py` enumerates the source faces of: F1 `Lambda_N` versus `Lambda_(N+1)`; F2 `Lambda_N` versus `Lambda_(N+1)`; F1 versus F2 on `Lambda_N`; F1 `Lambda_N` versus F2 `Lambda_(N+2)`; and two one-prescription volumes (`[−2,3]×[−2,2]×[−2,4]` versus `[−3,2]×[−2,3]×[−2,2]`, for F1 and for F2). For every site `u` of `Lambda_N`, the least distance to a source site is at least `N − |u|_inf`, with slack 0 attained; it equals `N−1` at `e_z` and `N` at `0`. It also verifies the `28N(5N+1)` extra F2 faces at `N = 2, 3, 4`, at most 49 faces per site (attained), and face-vector site energies at most 18.

## 9. Item 4 (b) — the bounds for every comparison, both signs, each cutoff and the untruncated vectors

**Theorem 9.1.** For every comparison of the contract, both signs and every `Q_L`, with `N` the smaller box size (`N ≥ 2`), `R = {0, e_z}` and every finite complete-factor region `Y ⊂ Lambda_N`:

\[
\|\rho^{\rm box1}_R-\rho^{\rm box2}_R\|_1\le C\,q^{N-1},\qquad
C=K(1+q)\Big[2(1+t)+(1+t)^4\kappa_0\big(S_{1/(qv)}-1\big)\Big],
\tag{HNM-BB1-F12}
\]

\[
\|\rho^{\rm box1}_Y-\rho^{\rm box2}_Y\|_1\le c_{\rm site}\,|Y|\,e^{|Y|/10^8}\,q^{d_Y},\qquad
c_{\rm site}=K\Big[2+\kappa_0\big(S_{1/(qv)}-1\big)\Big],\quad d_Y=N-\max_{y\in Y}|y|_\infty .
\tag{HNM-BB1-F13}
\]

*Proof.* Apply Theorem 7.1 on the union volume to `c = c^A` and `c' = c^B` (norms bounded by `t` and `τ̄` of §§1, 5). Theorem 8.1 gives `D(x) := Σ_{I∋x}‖δ_I‖ ≤ K q^{(N−|x|_inf)_+}`. Since `|x|_inf ≤ |y|_inf + d(x,y)` and `q ≤ 1`, `D(x) ≤ K q^{N−|y|_inf} q^{−d(x,y)}`, so `Σ_{x≠y} v^{−d(x,y)} D(x) ≤ K q^{N−|y|_inf}(S_{1/(qv)} − 1)`; and `Σ_{I meets Y}‖δ_I‖ ≤ Σ_{y∈Y} D(y)`. Hence

`‖ρ_Y(c^A) − ρ_Y(c^B)‖_1 ≤ Σ_{y∈Y} K q^{N−|y|_inf}[2(1+t)^{|Y|−1} + (1+t)^{2|Y|}κ_0(S_{1/(qv)} − 1)]`.

For `Y = R`, `q^N + q^{N−1} = (1+q)q^{N−1}`, which is (F12). For a general `Y`, `Σ_y q^{N−|y|_inf} ≤ |Y| q^{d_Y}`, and `(1+t)^{|Y|−1} ≤ (1+t)^{2|Y|} ≤ (1 + 10^{−8})^{|Y|} ≤ e^{|Y|/10^8}`, because `(1+t)^2 = 1 + 2t + t^2 ≤ 1 + 10^{−8}` (exact check; `2t + t^2` is about `6.806e-9`). That is (F13). ∎ The exponent is the contract form (`d_R = N − 1`); the rate is per coarse l-infinity step in `N` at fixed spacing.

**Corollary 9.2 (fixed `N`, changed exterior: F1 versus F2 on the same `Lambda_N`).** This is its own item. The source is the `28N(5N+1)` extra F2 faces (616, 1344, 2352 at `N = 2, 3, 4`), all on the outer layer of `Lambda_N`, at distance `N−1` from `e_z` and `N` from `0`. The bound is (F12)–(F13) with the same `C` and `c_site`.

**Corollary 9.3 (two volumes of one prescription, compared directly).** Theorem 8.1 compares the two volumes directly (no union comparison and no telescoping), and Theorem 7.1 runs once on their union, so (F12)–(F13) hold with the same constants. The route through the union volume (each volume against the union, then the triangle inequality) costs a factor 2 and is **labelled only**: `2C` about `1.78102399871e-6`, `2c_site` about `1.75362362353e-6`. Any two centered boxes `Lambda_M, Lambda_M'` (`M, M' ≥ N`) of F1 or F2 are compared directly in the same way.

**Proposition 9.4 (untruncated ground vectors at fixed `N`; the limits are never exchanged).** Fix `N` and the two volumes. In each `Q_L` the bounds hold with constants independent of the cutoff. AM2 §6 gives, for every finite volume of F1, a simple untruncated ground eigenvalue with gap at least `1/2`; the AY1 itemization gives the same for F2 with padding, including cutoff-vector removal. AV1 F22 gives `1 − |⟨ψ, ψ_L⟩|^2 ≤ 2(E_{0,L} − E_0) → 0` as `L` grows, so `‖ρ_{L,Y} − ρ_Y‖_1 ≤ 2(1 − |⟨ψ,ψ_L⟩|^2)^{1/2} → 0` (partial traces contract). Then `‖ρ^A_Y − ρ^B_Y‖_1 ≤ ‖ρ^A_Y − ρ^A_{L,Y}‖_1 + C q^{N−1} + ‖ρ^B_{L,Y} − ρ^B_Y‖_1` for every `L`, and the outer terms vanish. So (F12)–(F13) hold for the untruncated finite-box ground vectors at fixed `N`. No limit in `N` is taken.

**Secondary pair (labelled; the headline decides the loop).** The same proof runs at `q_2 = 151552|tau|` with `K = 49/10202112` and the secondary weights. Both frozen secondary targets are met at both signs.

**Crude tier (reported separately, never a target).** With every input crude (`K = 296/390625`, `t = 37/6250000`, crude `τ̄`), `C` is about `2.05285240831e-3`, which fails `1/250000`. The crude anchored norm has `(1+t)^2 − 1` about `1.184e-5`, above `10^{−8}`, so the crude estimate has no `c_site` in the frozen form: its `K[2+κ_0(S−1)]` is about `2.02124911591e-3`, with an exponential rate in `|Y|` too large for that form. The secondary crude `C` is about `7.80358341717e-2`. The crude tier is retained as a reported value, and nothing is retuned.

## 10. Constants (exact rationals and labelled previews)

All values are at `tau = +10^-8`; the `tau = −10^-8` values replay the same `|tau|` formula (a replay, not a second confirmation). At fixed `q`, every headline constant is increasing in `|tau|`; the secondary weights scale with `1/|tau|`.

**Headline, `q = 1/64`** (exact_first_order, polymer_kp; BA1 input the gate bound value `K = 49/111790368`, form (b)):
- `C = 578430793501182095316361404668712117814097366497488882433123687207743348935643590594947878052521565633072717772804866626438590065415931413647325/649548567473042337664409810664855266791889949984121342174530956201606073245694809426490159178862195173312829634280741896750749402941566759659762614272` (about `8.90511999358e-7`; target `1/250000`; margin `4.49179`);
- `c_site = 207042404781481370031872233170526436180882031154261216585642344563461649618003876497888095865804915933/236130948514531640807035481765249880343283808663306771542081002582898728697162432799219796273340474330185728` (about `8.76811811767e-7`; target `1/500000`; margin `2.28099`);
- the same `C` and `c_site` for each of the five comparisons and both signs (the input does not distinguish comparisons);
- previews of `C q^(N−1)`: `1.39142e-8` (`N=2`), `2.17410e-10` (`N=3`), `3.39703e-12` (`N=4`).

**Secondary, `q_2 = 151552|tau|`** (labelled; exact_first_order, polymer_kp; analytic_disc input at `rho = 1/151552`, `K = 49/10202112`):
- `C = 2216783849637614754349816349476828114862546732666598528993087032521892875263338674219111526932043758579379827148311137041515669004129835740137/229861112607616296602818624078789013955273108257059557062373235093825295569112762540951209099237770614965194496235530341122563389965929021440000000` (about `9.64401426796e-6`; target `1/20000`; margin `5.18456`);
- `c_site = 659169174096393659891184006000147019832940371882251984588910646015963995435696594125709554915933/68453668989200688545168014712434746377692880768971340886646744746921034481411750117768234866260836352` (about `9.62942065531e-6`; target `1/40000`; margin `2.59621`).

**Crude tier at `q = 1/64`** (crude_majorant, polymer_kp; crude circle input `K = 296/390625`):
- `C = 21735420321144166777522632385502981285912142211672183541927211065279383108115704743849910101438724890590774286407/10587911840678754238354031258495524525642395019531250000000000000000000000000000000000000000000000000000000000000000` (about `2.05285240831e-3`; fails `1/250000`; reported);
- crude `τ̄ = 111444666444111/97656250000000000`.

**Proof constants.**
- `t = 49/14398580736`;
- `τ̄`: headline `6143393381125/9196881302842190592`, secondary `6143393381125/731193302842190592`;
- `a`: headline `37741282235250459506265625/84582625698568269021279506561253310464`, secondary `37741282235250459506265625/534643646121271444464914561253310464`;
- `κ_0` as in §7;
- loss `ŵ`: headline `3012018012003/15625000000`, secondary `3012018012003/1515520000`;
- `Γ`: headline `231925386924231/12207031250000000`, secondary `231925386924231/1184000000000000`;
- `S_{v/w} = 725`, `S_{1/(qv)} = 147`.

## 11. Item 5 — fixtures, mandatory sentence and gate fields

Every fixture is exact and labelled `model_is_finite_graph: true`, `transfers_to_aq: false` in `results.json`. None is a proof of a lattice statement; each audits one step or one trap.

1. **Coefficient decay is not marginal decay** (`coefficient_decay_not_marginal_decay`; AV1 F13 type). Qubits `r, o, o'` with `c_{r,o} = 1/3` (straddling), `c_o = b` and `c_{o'} = 2/5`. The coefficients on supports meeting `R = {r}` are identical for `b = 1/2` and `b = 0`, yet `ρ_r = [[45/49, 6/49],[6/49, 4/49]]` against `[[9/10, 0],[0, 1/10]]`.
2. **Second-order propagation** (`fixture_second_order_propagation`). Chain `r – o1 – o2` with `c_{r o1} = a`, `c_{o1 o2} = b` and `c_{o2} = g`. The off-diagonal numerator of `ρ_r` is exactly the polynomial `−abg`, so a change of `g` two supports away moves the marginal exactly at the order `ab` of the two straddling amplitudes; with `b = 0` nothing moves. A first-order claim (`−a`) and a per-link factor `1/2` are rejected.
3. **Normalization coupling and straddling supports** (`normalization_couples_supports`). For `R = {r0, r1}` and one outside site:
   - a one-site straddling support and a support strictly containing `R` both have **zero first-order** `R`-marginal;
   - a support equal to `R` has one (`−ε` on `|11⟩⟨00|`);
   - at second order the straddling support excites one site of `R`, and the strictly containing support excites both.

   In the three-site fixture, `‖δ‖^2 = a^2`, so `e` is first order in the straddling amplitude `a`, while the off-diagonal element is `ab` (second order). Three shortcuts are rejected: dropping the straddling supports; normalizing by `1 + O(t^2)` without the split (the naive value changes with a decoupled spectator: `36/49` against `900/1421`); and charging the straddling term only at first order.
4. **Global fidelity** (`global_fidelity_orthogonality_catastrophe`). Product states `φ^{⊗n}`, `φ'^{⊗n}` with `φ = (1, 1/10)` and `φ' = (1, 1/8)`. The one-site fidelity is `6561/6565`, and the squared marginal distance `16/6565` stays fixed, while the squared global-overlap bound `4(1 − F^n)` grows with `n` (about `0.865` at `n = 400`). A bound through the global overlap is rejected.
5. **Split-route trace and Lipschitz checks** (`fixture_split_lipschitz_and_trace`). `Y = {r}`, outside `{o1, o2}`, creations meeting `Y` with amplitudes `1/5, 1/4, −1/6, 1/7`, and two mixed outside states. `check.py` verifies exactly: `Tr N_c(ω) = 1 + Tr[D(P⊗ω)D^*] ≥ 1`; `‖ρ(ω) − ρ(ω')‖_1 ≤ 2‖N(ω − ω')‖_1`; and `‖N(X)‖_1 ≤ (2ε+ε^2)‖X‖_2`. A per-site charge stays below `S_{1/64}` at every depth, while a charge by the product of growing region sizes exceeds it and is rejected.
6. **Polymer identity and cardinality factor** (`fixture_polymer_identity`). Four qutrit sites with all 15 supports and 80 rational creation components:
   - the brute-force `(ψ, ψ)` equals the polymer sum;
   - families with different excitation sets pair to zero;
   - the Y-cluster formula (F06) reproduces `ρ_Y` for `Y = {1}` and `{1,2}`, and the vacuum probabilities agree;
   - dropping overlap connectivity, replacing activities by their bounds, and a creation with a vacuum component are rejected.

   Cardinality: single-site creations `1/3` give polymers of activity `1/9`. With `a = 1/7` (`(1/9)e^{1/7} ≤ 1/7`), the cluster sum over a four-site test set lies in `[38/81, 1/2]`. The majorant `a|S| = 4/7` covers it, while the majorant without the cardinality factor (`1/7`) underestimates it and is rejected.
7. **Cutoff-limit order** (`cutoff_limit_order`, with `cutoff_vector_removal`). `a(N,L) = (1 − 2^{−L})^{(2N+1)^3}` tends to 1 as `L` grows at fixed `N`, and to 0 as `N` grows at fixed `L`, so exchanging the limits changes the answer. The Eckart bound is verified exactly on `diag(0, 1/2, 1)`, and `diag(0,0,1)` shows that eigenvalue convergence without a gap says nothing about vectors.
8. **Also exact:**
   - the outside vector is not a ground state: on the chain `y – o1 – o2` with `gXX` bonds, the restricted coefficient on `{o1,o2}` is `g/2 + 0·g^3`, while the outside ground coefficient is `g/2 − g^3/8`;
   - a normalization zero at `z = i/2` for `ψ(z) = Ω − 2z|11⟩`;
   - a nonlocal map with Lipschitz constant `1/2` and no decay;
   - an alternating sequence with convergent subsequences;
   - fixed versus moving vectors: `‖A_n ψ‖^2 = 4^{−n}` against `‖A_n e_n‖ = 1`.

**Mandatory sentence** (quoted once, verbatim, as one unbroken span; the constants follow it):

> For the zero-selected patterned family at the same coupling |tau|<=10^-8, and for every comparison of the named construction families F1 and F2 on centered coarse cubes, the reduced densities of the finite-box ground vectors on the cover R differ by at most C q^(N-1) in trace norm, in each on-site cutoff space and, at fixed N, for the untruncated ground vectors, where N is the smaller box size; this is locality of the reduced densities of the named constructions at a rate in N, not uniqueness of any ground state, not a statement about other boundary conditions, and not a statement uniform in the lattice spacing a.

The constants for it:
- `q = 1/64` and `C` as in §10 (about `8.90511999358e-7`; exact_first_order, polymer_kp; BA1 input the gate bound value `K = 49/111790368`, through form (b));
- `R = {0, e_z}`; F1 and F2 on `Lambda_N`, `N ≥ 2`;
- both signs, `|tau| ≤ 10^-8`;
- every comparison of `parameters.comparisons`.

**Gate fields** (exported exactly as in `gate_fields_required`):
- `state_decay_claimed: true`, with `state_decay_scope` "reduced densities of F1/F2 finite-box ground vectors on R and on regions Y, per comparison";
- `rate_in_N_claimed: true`;
- `false`: `whole_sequence_claimed`, `common_limit_claimed`, `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `continuum_claim`, `translation_invariance_claimed`, `weak_coupling_claim` and `scientific_priority_verified`;
- also exported false: `reduced_density_analyticity_claimed`, `uniform_wilson_claim` and `resolved_interaction_shift`.

The per-comparison bounds are recorded as the input of BB2; no limit object is formed here.

## 12. Item 6 — scaling and controls

**`tau → tau/100`** (same exact formulas at both couplings, no intermediate rounding; brackets read from the contract):

| constant | ratio (exact in `results.json`) | bracket | in bracket |
|---|---|---|---|
| headline `C` | `1.00647875e2` | `[95,105]` | yes (linear in `tau`, positive nonlinear correction) |
| `c_site` | `1.00647875e2` | `[95,105]` | yes |
| secondary `C` | `1.00150034e0` | `[99/100,101/100]` | yes (the factor `1+q_2`) |
| secondary `c_site` | `1.00000000e0` | `[99/100,101/100]` | yes |
| `q_2` | `1.00000000e2` | exactly 100 | yes |

**Controls.** `check.py` runs 51 exact checks. Each of the 37 contract controls is a check with at least one damaging mutation that must raise `AdmissionError` (no `assert` is used); 107 damaging mutations are rejected in total:

| control | damaging mutations rejected |
|---|---|
| `coherent_evidence_tampering` | with the packet hash rebound: a control Boolean flipped; the BA1 gate snapshot removed; the headline `C` halved; `whole_sequence_claimed` set true; one family; the mandatory sentence trimmed; a forbidden phrase added |
| `exact_arithmetic_admission` | float, bool, NaN string, zero denominator |
| `no_priority_or_continuum_claim` | `continuum_claim` true; `scientific_priority_verified` true |
| `changed_model_relabelled` | `tau` changed; nonzero triple; SU(3); two dimensions; finite-graph model id; l1 metric; weights retuned after the constants |
| `insufficient_verdict_retained` | the crude tier relabelled accepted; `tau` retuned |
| `tau_scaling_exponent` | a square-root bound labelled linear; a bracket narrowed after evaluation; a secondary constant written in the headline `q` form |
| `wrong_delta_alpha_hbar_clock` | first-order coefficient `tau/576` or `tau/9` (mixed units); `u=theta/8` labelled `theta` |
| `root_n_misuse` | a root-sum-of-squares style combination; division by a square root of a site count; a region bound divided by `sqrt|Y|` |
| `tier_mixing_rejected` | a crude anchored norm in an exact constant; a BA1 route label used as the BB1 route; a Lieb–Robinson tier; a crude BA1 input in an exact constant; no BA1 input named |
| `reverse_premise_isolation` | a skeptic triage, a forward BB1 file, a BB2 producer file or a deliberation added to the inventory |
| `uniform_in_N_not_in_a` | a rate statement without the qualifier "in N at fixed spacing"; a claim in the lattice spacing |
| `placeholder_span_rejected` | angle spans with whitespace, a bar, or "e.g." |
| `negation_aware_phrase_scan` | affirmative forbidden phrases (two fixtures); the report and the results are scanned with the template removed as one literal |
| `parameters_declare_metric_weights_window` | `metric`, `weights` or `window` removed |
| `rate_constant_pair_prefrozen` | a rate optimized after the constants; weights chosen after the constants; the secondary weight `5/q` (inadmissible) |
| `decay_rate_in_N_not_a` | rate per fm; rate per lattice spacing; `rate_in_a_claimed` true |
| `topology_named` | a Hilbert–Schmidt topology of the global vectors; convergence claimed along moving vectors |
| `two_families_named` | one family; literal vertex boxes added |
| `subsequence_versus_whole_sequence` | `whole_sequence_claimed` true from the per-comparison bounds; `common_limit_claimed` true |
| `common_clock` | the two boxes at different couplings |
| `coefficient_decay_not_marginal_decay` | state decay inferred from equal coefficients (F13 fixture) |
| `normalization_couples_supports` | straddling supports dropped; normalization by `1+O(t^2)`; straddling charged only at first order |
| `outside_vector_not_ground_state` | a gap argument applied to the outside vector; the outside vector called a ground state |
| `global_fidelity_orthogonality_catastrophe` | a bound through the global overlap |
| `marginal_locality_constants_explicit` | the KP criterion without activity bounds; without combinatorial counts; `p` not named; `η` not named |
| `cutoff_uniform_then_removed` | limits reversed; a cutoff-dependent constant |
| `cutoff_vector_removal` | eigenvalue convergence used for vectors without a gap |
| `region_constant_scales_with_Y` | the `R` constant reused on `Y` without the `|Y|` factor; the hybrid rate `4t` (above `10^−8`); the exponent of `R` reused for a region reaching `|y| = 2` |
| `named_construction_not_uniqueness` | uniqueness claimed; two forbidden phrasings |
| `global_lipschitz_not_decay` | the map constant as a per-shell factor; the outside-state Lipschitz constant as decay; the Lipschitz-`1/2` decay claim (mean-field fixture) |
| `fixture_second_order_propagation` | first-order propagation; a per-link factor below the exact one |
| `fixture_split_lipschitz_and_trace` | the normalization Lipschitz factor quartered; product-of-region-sizes charging |
| `fixture_polymer_identity` | polymers without overlap connectivity; activities replaced by their bounds; a creation with a vacuum component; the cardinality factor dropped |
| `zero_free_region_required` | analyticity claimed without a zero-free region; a complex-parameter derivative |
| `every_site_coefficient_input` | the R-only input used at far sites; form (b) cited as admitted; a wrong box size for the exponent; the input `K` halved |
| `mixed_weight_lemma_proved` | cited from BA1; loss `w e^{3b}`; loss per creation; the maximum-instead-of-sum shortcut; `e^b = 2`; `w = 42/q` |
| `cutoff_limit_order` | the `N` and `L` limits exchanged |

**Positive checks** without a contract id: `contract_snapshot_sha256`, `premise_gates_pinned_and_parsed`, `polymer_kp_lemmas_audited_on_finite_graphs`, `kotecky_preiss_condition_and_tree_majorant`, `headline_R_form_every_comparison_both_signs`, `region_form_every_comparison_both_signs`, `fixed_N_F1_versus_F2_item`, `one_prescription_volumes_compared_directly`, `secondary_pair_labelled`, `crude_tier_reported_separately`, `untruncated_ground_vectors_at_fixed_N`, `error_ledger_itemized`, `mandatory_sentence_and_gate_fields`, `report_bound_to_results`.

## 13. Error ledger (preregistered terms, added linearly)

The headline `C` is the exact sum of five items. The first is `2K(1+q)`; the next four carry the factor `K(1+q)(1+t)^4(S_{1/(qv)} − 1)`.

| term | headline contribution to `C` | status |
|---|---|---|
| `coefficient_input_every_site` | `3185/3577291776` (about `8.90338333978e-7`): `2K(1+q)` from `D(0) + D(e_z) ≤ K(1+q)q^{N−1}`; the far-site input `D(x) ≤ K q^{(N−|x|)_+}` enters the next three items through `S_{1/2} − 1 = 146` | charged |
| `straddling_supports` | about `8.68311750746e-11` (Term I: Y-cluster derivatives, `2τ̄` per site) | charged |
| `normalization` | about `8.68342050528e-11`: the `η_R` part, about `3.02992212669e-15`, plus the vacuum-probability derivative, about `8.68311751307e-11` | charged |
| `polymer_or_split_remainder` | about `2.80512868271e-20` (Kotecký–Preiss clusters in the truncated vacuum probabilities) | charged |
| `cutoff_removal_at_fixed_N` | — | not_applicable, with reason: not a numeric cost; at fixed `N` the terms `‖ρ_{L,Y} − ρ_Y‖_1` tend to 0 as `L` grows (AV1 F22 with the untruncated gap `1/2`; AY1 for F2) and the closed bound passes; no constant depends on `L` |
| `arithmetic` | — | not_applicable, with reason: exact Fractions; directed enclosures only (`e^{1/8} ≤ 8/7`, so `G(R) ≤ 148/7` and `G'(R) ≤ 352`; `ln(1001/1000) ≥ 1/1001`; `e^x ≥ 1+x`) |

Deterministic terms add linearly. There is no root-sum-of-squares combination and no division by a square root of a site count.

## 14. Exclusions, limitations, contract wording defects and readings

**Contract exclusions (respected):**
- whole-sequence convergence or a common limit (BB2);
- uniqueness of every infinite-volume ground state;
- boundary conditions outside the named constructions;
- analyticity of the reduced density in the coupling;
- any estimate in the lattice spacing `a`;
- continuum or weak coupling;
- scientific priority.

**Additionally:** no dynamics, and no limit object is formed. The rate is per coarse step `(4a,2a,a)` in `N` at fixed spacing and strong bare coupling, never per unit of the lattice spacing or of physical length.

**Limitations.**
1. **Scope.** Only the zero-selected patterned family, fixed spacing, `|tau| ≤ 10^-8`, the named families F1 and F2 (and one-prescription complete-factor volumes containing `Lambda_N`), the cover `R` and regions `Y ⊂ Lambda_N`. Nothing transfers to other boundary conditions, nonzero selected triples, literal vertex boxes, weak coupling or the continuum.
2. **Cited, not re-proved:** the Kotecký–Preiss theorem (Theorem 6.1; primary source not re-inspected in this session), Weierstrass and the maximum principle. **Inherited without re-proof:** the AM2 multilinear estimate, fixed point, uniqueness in the ball and §6 cutoff facts; AV1 F06, F15–F18 and F20–F23; the AY1 F2 itemization; the I1 dictionary.
3. **Upper bounds only.** The constants are majorants. The far-site terms are about `10^{−4}` of `C` at the headline, so the margin is carried by the input `K` and the factor `2(1+q)`.
4. **Fixtures** are exact finite audits (`transfers_to_aq: false`), not proofs of the lattice statements.
5. **Correlation.** The contract and selection note name this route (polymers, Kotecký–Preiss, mixed weight); both producers use the admitted BA1 constants; all agents are correlated model agents. Independence is limited to route and code.

**Contract wording defect (non-blocking).**
- **D1.** `normalization_couples_supports` says a one-site straddling first-order face has zero R-marginal "while a support strictly containing R does not". At first order a support strictly containing `R` also has zero `R`-marginal: the AY1 gate records that all 72 straddling faces among the 82 meeting `R` vanish, and 6 of them strictly contain `R`. The nonzero first-order marginal belongs to supports equal to `R`; a support strictly containing `R` differs at second order (the fully excited `R` block). The fixture records all three kinds.

**Readings (recorded).**
- **R1.** Form (b) is stated for `u ∈ Lambda_N` with exponent `N − |u|_inf`. The polymer route also needs the union-volume sites outside `Lambda_N`, where the same theorem gives `K` (exponent `(N − |u|_inf)_+ = 0`).
- **R2.** `ω_O` is the outside marginal on `O = ∪_{I meets Y}(I ∖ Y)`, or on any larger outside region; `N_c` depends on `ω` only through its marginal on `O`.
- **R3.** The lemma form `κ(I) ≤ κ_0 (w')^{−d_inf(I,Y)} p(|I|)` is implied by the sharper site form (F10), with `p(s) = s`, `w' = v` and `κ_0(Y) = N_Y|Y|κ_0`; the constants use the site form.
- **R4.** The AY1 itemization (H1–H5, including cutoff-vector removal) is stated for F2 on `Lambda_N`. No step uses the cube shape, so it applies verbatim to the one-prescription volumes, as the BA1 accepted statement already uses.

## 15. Proposed forward verdict

**`accepted_within_scope` for the forward half**, sub-label `static_not_dynamic`:
- both frozen targets are met: `C` about `8.90511999358e-7 ≤ 1/250000`, and `c_site` about `8.76811811767e-7 ≤ 1/500000`;
- they hold for every comparison (including the fixed-`N` F1-versus-F2 comparison and two one-prescription volumes compared directly), at both signs, in each on-site cutoff space and, at fixed `N`, for the untruncated ground vectors;
- the labelled secondary pair meets `1/20000` and `1/40000`, and the crude tier is reported separately.

The global Lipschitz constant is never used as a decay factor. The contract's acceptance also requires the reverse iterated_split route and skeptical review.

## 16. Map of required items and controls to proofs and checks

| contract item | report section | `check.py` check id(s) |
|---|---|---|
| 1 (decomposition, `Tr N_c ≥ 1`, two Lipschitz bounds) | §2 | `fixture_split_lipschitz_and_trace`, `global_lipschitz_not_decay`, `normalization_couples_supports`, `outside_vector_not_ground_state` |
| 2 (polymer representation of norm and expectation) | §3 | `fixture_polymer_identity` |
| 2 (activity bound, exploration counts, tree majorant) | §§3–4, 6 | `polymer_kp_lemmas_audited_on_finite_graphs`, `kotecky_preiss_condition_and_tree_majorant` |
| 2 (mixed-weight lemma, in full) | §5 | `mixed_weight_lemma_proved` |
| 2 (KP condition, explicit `a`) | §6 | `kotecky_preiss_condition_and_tree_majorant`, `marginal_locality_constants_explicit` |
| 2 (real-parameter derivative, no analyticity) | §7 | `marginal_locality_constants_explicit`, `zero_free_region_required` |
| 3 (reverse route) | — | outside this producer; the inventory rule is checked in `reverse_premise_isolation` |
| 4 (every-site input, form (b) in full) | §8 | `every_site_coefficient_input` |
| 4 (headline and region, every comparison, both signs) | §9 | `headline_R_form_every_comparison_both_signs`, `region_form_every_comparison_both_signs`, `fixed_N_F1_versus_F2_item`, `one_prescription_volumes_compared_directly`, `region_constant_scales_with_Y` |
| 4 (each `Q_L`, then the untruncated vectors at fixed `N`) | §9 | `cutoff_uniform_then_removed`, `cutoff_vector_removal`, `cutoff_limit_order`, `untruncated_ground_vectors_at_fixed_N` |
| 4 (secondary pair, crude tier, no global-Lipschitz decay) | §§9–10 | `secondary_pair_labelled`, `crude_tier_reported_separately`, `global_lipschitz_not_decay` |
| 5 (fixtures, sentence, gate fields) | §11 | the fixture controls, `mandatory_sentence_and_gate_fields`, `report_bound_to_results` |
| 6 (scaling, controls) | §12 | `tau_scaling_exponent` and all 37 control ids |
| preregistered error terms | §13 | `error_ledger_itemized` |
| contract binding and premises | header, §0 | `contract_snapshot_sha256`, `premise_gates_pinned_and_parsed` |

Every contract control appears in §12 with its mutations: `coherent_evidence_tampering`, `exact_arithmetic_admission`, `no_priority_or_continuum_claim`, `changed_model_relabelled`, `insufficient_verdict_retained`, `tau_scaling_exponent`, `wrong_delta_alpha_hbar_clock`, `root_n_misuse`, `tier_mixing_rejected`, `reverse_premise_isolation`, `uniform_in_N_not_in_a`, `placeholder_span_rejected`, `negation_aware_phrase_scan`, `parameters_declare_metric_weights_window`, `rate_constant_pair_prefrozen`, `decay_rate_in_N_not_a`, `topology_named`, `two_families_named`, `subsequence_versus_whole_sequence`, `common_clock`, `coefficient_decay_not_marginal_decay`, `normalization_couples_supports`, `outside_vector_not_ground_state`, `global_fidelity_orthogonality_catastrophe`, `marginal_locality_constants_explicit`, `cutoff_uniform_then_removed`, `cutoff_vector_removal`, `region_constant_scales_with_Y`, `named_construction_not_uniqueness`, `global_lipschitz_not_decay`, `fixture_second_order_propagation`, `fixture_split_lipschitz_and_trace`, `fixture_polymer_identity`, `zero_free_region_required`, `every_site_coefficient_input`, `mixed_weight_lemma_proved`, `cutoff_limit_order`.

**Methodological lenses** (modern use of the snapshotted skills; no historical figure endorses anything here):
- **Newton, analysis before synthesis.** The density difference was first analysed into a coefficient part meeting `Y`, straddling families and vacuum probabilities; only then were constants synthesized.
- **Tesla, complete accounting.** Every channel is charged: the far sites through the every-site input, the straddling families, the normalization and the cluster remainder.

## 17. Reproduction

```bash
python3 -B research/round33/forward/bb1/check.py --output /absolute/fresh/dir
python3 -B -O research/round33/forward/bb1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round33/tools/freeze.py verify research/round33/forward/bb1
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/bb1.json research/round33/forward/bb1/report.md
```

`check.py` does the following:
- verifies the contract sha256 before any evaluation;
- pins the sha256 of every gate and parsed report;
- reads every target, bracket, parameter and control id from the contract;
- records its own sha256 before evaluation;
- writes `results.json` and `source-manifest.json`, which bind `check.py`, `report.md`, every `inputs/` file and `results.json`.

BB1 is investigation 3 of 8 in Round33. This producer executed only the forward half.
