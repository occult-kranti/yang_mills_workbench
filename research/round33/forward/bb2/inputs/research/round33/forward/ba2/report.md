# Hruday boundary comparison of the Heisenberg dynamics of the named constructions on compact windows — BA2 forward (Duhamel over the extra F2 faces, inner F1 evolution)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production: the derivations, `check.py` and this report were written by a Claude model agent acting as the BA2 forward producer under the frozen BA2 contract (`research/round33/contracts/ba2.json`, sha256 `275ba3b002529b7295d0f8b91dc1cc7a96451e3c7f936ee698a932fdca54fcff`, verified by `check.py` before any evaluation). It is correlated model-agent work, not independent human review and not formal verification. HNM labels are project aliases.

**What this producer read.**
- **The contract snapshot first**, then only files under `inputs/`:
  - *read in full:* `AGENTS.md`; `selection-ba2.md`; the committed Nachtergaele–Sims excerpt `research/round33/sources/nachtergaele-sims-1410.8174v1.md`; the AQ1 forward report and gate; `skeptic/aq1.md`; the AQ source dictionary and primary bindings; the I1 forward report; the AM2 forward report; the AY1 forward report; the Round32 lessons reference `round32-state-lemma-and-window.md`; the paired-physics SKILL and its complete-residual reference; the Newton, Tesla and historical-panel SKILL files;
  - *read in part:* the AY1 reverse report (verdict, sections 0–1.6, and keyword-search lines for `1323`, `28N`, `5N+1`); the AY2 forward report (header, verdict, sections 1–2 with the obligations table O1–O6); the AY1 and AY2 gates (`accepted`, `limitations`, `model`, `decision`, `sub_label`, `gate_fields`); the AM2 gate (`accepted`, `limitations`); the AV1 forward report (section 1 and headings); the AQ2 forward report (section 4 and headings);
  - *headings or hash only:* the AV1 reverse and AM2 reverse reports (headings); the AV1 gate (verdict, field names and sha256); `skeptic/am2.md` was not opened.
- **Outside `inputs/`, for protocol and code style only:** `research/round33/tools/README.md`, `research/round33/tools/freeze.py`, `research/round33/tools/phrase_scan.py` (its round phrase list is copied into `check.py` as infrastructure), and parts of `research/round32/forward/ay1/check.py` (header and helpers, the start of `compute`, the packet and tampering section, `main`). None of these carries premise weight.
- **Not read:** anything under `research/round33/reverse/`, `research/round33/skeptic/`, `research/round33/experts/`, `research/round33/advisor/` other than the snapshotted `selection-ba2.md`, and `research/round33/forward/ba1/`; no `deliberation-*` file; no other agent's scratch folder.
- **Scratchpad disclosure.** My scratch work is in `/tmp/claude-0/ba2-forward-private/`: two float/Fraction enumeration prototypes (`proto.py`, `proto2.py`), a report draft with three substitution markers (`report_draft.txt`), development runs `dev1` to `dev5` and later ones, and the production run `run1`. **None of it is evidence.** I created the folder directly with `mkdir -p` and did not list `/tmp/claude-0/`, so I saw no other agent's folder names, and I opened no file in any other agent's scratch folder. The Claude harness saved a copy of one of my own long reads (the AY1 forward report) to its tool-results cache; that is my own read, not another agent's file.

**Shared premises and attribution.** The route (Duhamel over the extra F2 faces with the AQ1 Nachtergaele–Sims constants) is named in the contract, the selection note and the AY2 obligations table (rows O5, O6); on this route those are shared premises. The Lieb–Robinson bound and the existence of the limit dynamics are Nachtergaele–Sims (arXiv:1410.8174v1, Theorems 3.1 and 4.1); Duhamel's formula, the tensor-product factorization of commuting unitary groups, Stone's theorem and Fourier inversion are standard. The compactness/dynamics/GNS/Fourier strategy of AQ1 sections 4–5 is credited to Gauvin arXiv:2503.15539v3 Supplement A.10 in AQ1. Independence from the reverse producer is limited to the inner family, the interaction indexing, the constants, the enumeration and the code. Scientific priority is unverified.

## Verdict (forward route)

Model: **`AQ_patterned_zero_selected`** (AM2/AQ1 zero-selected patterned family: SU(2) Kogut–Susskind form on `Z^3` at fixed spacing, coarse 24-link factors, selected triple `(0,0,0)`, 21 omitted faces per anchor entering as `-(tau/3)W_f` in normalized units `delta=alpha/8`), both signs, `|tau|<=10^-8`, cover `R={0,e_z}`, observables `A` in `B(H_R)`, window `|theta|<=8` in the common clock `theta=alpha t/hbar` (normalized `u=theta/8`, so `U=1`). Families on the same centered cube `Lambda_N=[-N,N]^3`, `N` at least 2: **F1** = AQ1 centered whole-star boxes, **F2** = I1 section 6 all-contained-face boxes with padding. Every constant below is tier `polynomial_lieb_robinson`, uses the **whole-star interaction Phi** (`C<=224`, `||Phi||_F<=2268|tau|`, `F(r)=(1+r)^-4`), and has the **F1 evolution inside the Duhamel integral**.

1. **Boundary source (item 2).** `H^{F2,pad}_N - H^{F1}_N` is the sum of the `28N(5N+1)` extra faces plus the onsite terms on the padding `B_+ minus Lambda_N`. The padding terms act on other tensor factors and **factor out of the evolution exactly**; they are never charged. The extra faces are enumerated on `Lambda_2`, `Lambda_3`, `Lambda_4` (616, 1344, 2352) and counted for every `N` by class type. Each has at most 3 owners; every owner lies on the outer layer (`y_i=N` for some `i`, so `max_i |y_i| = N`), at coarse `l1` distance at least `N-1` from `e_z` and at least `N` from `0` (both attained). Each face is charged exactly once.
2. **Comparison (item 3).** For `|theta|<=8`, `N` at least 2, both signs, every `A` in `B(H_R)`:

   `||T^{F2,N}_theta(A)-T^{F1,N}_theta(A)|| <= b(N)||A||`, with `b(N) <= K_cmp (5N+1) N^-3` and

   `K_cmp = 254016 tau^2/(1-338688|tau|) = 3969/155720800000000` (preview `2.54879245418e-11`) at the cap.

   The frozen target `6x10^-11` is met with margin `2.35405`. The bound is quadratic in `tau`: the first order vanishes exactly because the extra faces act on links owned outside `R`.
3. **Within-family Cauchy estimates (item 4), sup over all `M` greater than `N`.**
   - F1: `||T^{F1,M}_theta(A)-T^{F1,N}_theta(A)|| <= K_c1/(N-1) ||A||`, `K_c1 = 592704 tau^2/(1-338688|tau|) = 9261/155720800000000` (preview `5.94718239310e-11`), margin `4.20367` against `2.5x10^-10`. Hence `||T_theta(A)-T^{F1,N}_theta(A)|| <= K_c1/(N-1)||A||`.
   - F2: `||T^{F2,M}_theta(A)-T^{F2,N}_theta(A)|| <= K_c2/(N-1) ||A||`, `K_c2 = K_c1 + (11/8)K_cmp = 941976 tau^2/(1-338688|tau|) = 117747/1245766400000000` (preview `9.45177201761e-11`), margin `2.64500`. Also `||T_theta(A)-T^{F2,N}_theta(A)|| <= K_c1/(N-1)||A||`.
   - The rate `1/(N-1)` is the honest rate of the polynomial `F`; no exponential decay in `N` is claimed.
4. **F2 limit dynamics (item 4, AY2 row O6).** The F2 finite-box evolutions converge **as a whole sequence** in norm, uniformly for `|theta|` at most 8, and their limit **equals the AQ1 limit dynamics `T_theta`**, identified through the comparison bound. AQ1 sections 4–5 are rerun for every subsequential F2 limit state with F2's own subsequences: stationarity under `T_theta`, strong continuity of the GNS evolution, nonnegative generator, and reduction by the physical cyclic space.
5. **Meaning (item 5).** Algebraic Heisenberg dynamics of the named constructions on a compact window at a rate in `N`; not equality of GNS dynamics or of correlation functions of different states; not a uniform-in-time statement; nothing in the lattice spacing `a`.
6. **Scaling and controls (item 6).** `C(tau)/C(tau/100) = 1953058850/194651` (preview `10033.64406`) for all three coefficients, inside `[9500,10500]` and inside the control bracket `[9900,10100]`.

**Checker.** `check.py` runs **44 exact checks**. All **35 contract controls** reject explicit damaging mutations, **116** rejections in total. The `-B` and `-B -O` outputs are byte-identical.

**Proposed forward verdict: `accepted_within_scope`** for the forward half, sub-label `dynamics_on_compact_windows`. The contract acceptance also requires the reverse route and skeptical review, which are outside this producer's work.

## 1. Model, families, clock, window and metric

**Model** (contract `model`, preregistration `model_id`). In normalized units `delta=alpha/8` (AV1 F01, AQ1 section 1):

\[
 h_b=8\sum_{e\in b}C_e,\qquad \phi_b=-\frac{\tau}{3}\sum_{f\in O_b}W_f,\qquad \|\phi_b\|=7|\tau|,\qquad \|W_f\|\le1 .
 \tag{HNM-BA2-F00}
\]

`h_b` is an unbounded self-adjoint Casimir sum with compact resolvent on the separable space `H_b=L^2(SU(2)^24)`; `O_b` is the set of the 21 omitted faces anchored at `b` (I1 table); a face `f` has owner set `M_f` (I1.4), `M_f` inside `b+S`, `S={0,e_x,e_y,e_z}`, `|M_f|` equal to 2 or 3.

**Families** (both on `Lambda_N=[-N,N]^3`, `N` at least 2):

\[
 \widehat H^{F1}_N=\sum_{b\in\Lambda_N}h_b+\sum_{b+S\subset\Lambda_N}\phi_b,\qquad
 \widehat H^{F2,{\rm pad}}_N=\sum_{x\in B_+}h_x+\sum_{f:\ M_f\subset\Lambda_N}\Big(-\frac{\tau}{3}\Big)W_f,\quad B_+=\Lambda_N+S .
\]

`T^{Fi,N}_theta(A)=e^{iu\widehat H}Ae^{-iu\widehat H}` with `u=theta/8`. F1 is contained in F2 face by face (1344 of 1960 faces at `N=2`, 4536 of 5880 at `N=3`).

**Clock and window.** The physical energy is `delta` times the normalized operator, so `e^{itK/hbar}=e^{i(delta t/hbar)\widehat H}=e^{i(theta/8)\widehat H}` with `theta=alpha t/hbar`. The window `|theta|<=8` is `|u|<=1`, i.e. `U=Theta/8=1`. AQ1's `T_t` (AQ1.4) is written `T_theta` here: `T_theta(A)=lim_N e^{i(theta/8)\widehat H^{F1}_N}Ae^{-i(theta/8)\widehat H^{F1}_N}`. `check.py` verifies the conversion with non-unit constants (`alpha=5`, `hbar=7`, `t=56/5` gives `theta=8`, `u=1`).

**Metric and weights** (contract `parameters`). Coarse `l1` metric on `Z^3`; `F(r)=(1+r)^-4` (shell count `4r^2+2`, enumerated for `r` up to 15); `||F||<=7`, convolution constant `C<=32||F||<=224` (AQ1 section 3, re-verified exactly in `lieb_robinson_F_declared`). No fine-site metric and no coarse-to-fine conversion enters any constant.

## 2. The Lieb–Robinson inequality and the limit dynamics, verbatim, and their placement

### 2.1 Verbatim quotations from the committed excerpt

Source: `research/round33/sources/nachtergaele-sims-1410.8174v1.md` (sha256 `6a28f4cd6aa2c55286fa839d83c00356ff0709f8b02027ee5b39050df1d6c921`, pinned in `check.py`), Part A (checked by the advisor against the rendered pages of the PDF with sha256 `501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba`). The lines below are copied byte for byte; `check.py` requires each one verbatim in this report and rejects paraphrased forms.

```text
For each x there is a self-adjoint operator H_x with dense domain D_x ⊂ H_x; the bounded interaction Φ maps finite X ⊂ Γ to Φ(X)* = Φ(X) ∈ A_X, and
(40) ‖F‖ = sup_{x∈Γ} Σ_{y∈Γ} F(d(x, y)) < ∞ (uniform integrability);
(41) C = sup_{x,y∈Γ} Σ_{z∈Γ} F(d(x, z)) F(d(z, y)) / F(d(x, y)) < ∞ (convolution condition).
(44) H_Λ = Σ_{x∈Λ} H_x + Σ_{X⊂Λ} Φ(X),
essentially self-adjoint on the dense domain (45) D_Λ = span{⊗_{x∈Λ} ψ_x | ψ_x ∈ D_x}; (46) τ_t^Λ(A) = e^{itH_Λ} A e^{−itH_Λ} for A ∈ A_Λ.
(48) ‖Φ‖ = sup_{x,y∈Γ} (1/F(d(x, y))) Σ_{X⊂Γ: x,y∈X} ‖Φ(X)‖ < ∞ defines the space B_F(Γ).
(49) S_Λ(X) = {Z ⊂ Λ : Z ∩ X ≠ ∅ and Z ∩ (Λ \ X) ≠ ∅}, the surface of X in Λ, and S(X) = S_Γ(X).
(50) ∂_Φ X = {x ∈ X : ∃Z ∈ S(X) with x ∈ Z and Φ(Z) ≠ 0}, the Φ-boundary of X.
Theorem 3.1. Let Γ and F be as indicated above. Fix a collection of local Hamiltonians {H_x}_{x∈Γ} and an interaction Φ ∈ B_F(Γ). Let X, Y ⊂ Γ be finite disjoint sets. For any finite Λ ⊂ Γ with X ∪ Y ⊂ Λ and any A ∈ A_X and B ∈ A_Y, the bound
(51) ‖[τ_t^Λ(A), B]‖ ≤ (2‖A‖‖B‖ / C) (e^{2‖Φ‖C|t|} − 1) D(X, Y)
holds for all t ∈ ℝ, where the quantity D(X, Y) is given by
(52) D(X, Y) = min{ Σ_{x∈X} Σ_{y∈∂_Φ Y} F(d(x, y)), Σ_{x∈∂_Φ X} Σ_{y∈Y} F(d(x, y)) }.
Theorem 4.1 (section title omitted). Let Γ and F be as described in Section 3. Fix a collection of on-site Hamiltonians {H_x}_{x∈Γ} and an interaction Φ ∈ B_F(Γ). For each t ∈ ℝ and A ∈ A_Γ^loc, the norm limit
(77) τ_t(A) = lim_{Λ→Γ} τ_t^Λ(A)
exists and the convergence is uniform for t in compact sets. The limit may be taken along any increasing sequence of finite sets Λ which tend to Γ, and the result is independent of the particular sequence. This limiting dynamics τ_t(·) can be uniquely extended to a one-parameter group of *-automorphisms on A_Γ.
The proof (steps 1–4) uses an interaction-picture dynamics (57) generated from H_0 = Σ_{x∈Λ} H_x + Σ_{Z⊂X} Φ(Z) (54), which is how the unbounded on-site terms are handled.
In its proof: (78) U_Λ(t, s) = e^{itH_Λ^loc} e^{−i(t−s)H_Λ} e^{−isH_Λ^loc}, with (79) H_Λ^loc = Σ_{x∈Λ} H_x.
```

The last two lines are the excerpt's own Part A description of the proof of Theorem 3.1 and its transcription of (78)–(79) from the proof of Theorem 4.1; they are quoted as the excerpt states them.

Equation (47) is available only in the excerpt's Part B machine text, whose norm bars and superscripts are lost; it is quoted as machine text and is used only for the statement that `t ↦ U_t^Λ` is a strongly continuous unitary group leaving the domain invariant:

```text
  By Stone’s theorem, see e.g. Section VIII.4 of [3] or Theorem 7.3.7 of [6], the unitaries t 7→ UtΛ =
e−itHΛ are strongly continuous, leave the domain of H   Λ invariant, and satisfy
                      d Λ
(47)                    U ψ = −iHΛ UtΛ ψ = −iUtΛ HΛ ψ for all ψ ∈ DΛ .
                     dt t
```

The AQ1 report is the placement record (its section 3), not the quotation source; `check.py` rejects a quotation taken from it.

### 2.2 Placement

| source object | this model |
|---|---|
| countable `Γ`, metric `d` | coarse `Z^3`, `l1` metric |
| `F`, (40), (41) | `F(r)=(1+r)^-4`, `‖F‖<=7`, `C<=224` |
| on-site `H_x` with dense domain `D_x` | `h_x=8 sum C_e`, unbounded, self-adjoint, compact resolvent |
| bounded interaction `Φ`, (48) | whole-star `Φ(b+S)=phi_b`, zero on other sets; `‖Φ‖<=81J=2268|tau|` with `J=28|tau|` (four incident stars) |
| (44) on `Λ` | F1 on `Lambda_N`: `sum_{x in Lambda_N} h_x + sum_{X subset Lambda_N} Φ(X)`, the native restriction |
| (46), time `t` | normalized `u=theta/8` |

For the Cauchy estimates the truncated interaction `Φ_N(X)=Φ(X)` for `X` inside `Lambda_N` and zero otherwise is also in `B_F(Γ)` with `‖Φ_N‖<=‖Φ‖`; its native restriction to any `Λ` containing `Lambda_N` is `sum_{x in Λ} h_x` plus the F1 interaction of `Lambda_N`. So the F1 box evolution **with the onsite terms of a larger box** is again an instance of (44).

**Monotone substitution.** The factor `(2/C)(e^{2‖Φ‖C|t|}-1)=sum_{k from 1} 2^{k+1}‖Φ‖^k C^{k-1}|t|^k/k!` in (51) is increasing in `C` and in `‖Φ‖`. The time integral used below, `(2/(Cv))(e^{vU}-1-vU)` with `v=2‖Φ‖C`, is also increasing in both (it equals `4‖Φ‖U^2 g(x)/x^2` with `x=vU`, `g(x)=e^x-1-x`, and `g(x)/x^2` increasing in `x`). The admitted upper bounds `C<=224` and `‖Φ‖<=2268|tau|` may therefore be substituted.

**Labelled observation (not used).** The exact supremum in (48) for the whole-star interaction is `567|tau|`: pairs at `l1` distance 2 inside one star give `81·7|tau|`, pairs at distance 1 give `16·7|tau|`, and `x=y` gives `28|tau|` (all four incident stars). The admitted `81J=2268|tau|` is four times larger and is used in every constant.

### 2.3 Duhamel with a bounded source (interaction picture)

**Lemma (HNM-BA2-F01).** Let `H_1=H_loc+V_1` and `H_2=H_loc+V_2` on one finite box, with `H_loc` the (closure of the) onsite sum and `V_1`, `V_2` bounded self-adjoint. Then `D(H_1)=D(H_2)=D(H_loc)` and, for bounded `B` and real `u`,

\[
 \tau^{(2)}_u(B)-\tau^{(1)}_u(B)=i\int_0^u\tau^{(2)}_s\big([V_2-V_1,\tau^{(1)}_{u-s}(B)]\big)\,ds\quad\text{(strong integral)},\qquad
 \|\tau^{(2)}_u(B)-\tau^{(1)}_u(B)\|\le\int_0^{|u|}\|[V_2-V_1,\tau^{(1)}_r(B)]\|\,dr .
 \tag{HNM-BA2-F01}
\]

*Proof.* `W(s)=e^{isH_2}e^{-isH_1}` satisfies `W(s)psi-psi=i int_0^s e^{irH_2}(V_2-V_1)e^{-irH_1}psi dr` for `psi` in the common domain (product rule for strongly differentiable unitary groups), hence for all `psi`; so `W` is norm-Lipschitz and strongly differentiable. `G(s)=W(s)τ^{(1)}_u(B)W(s)*=τ^{(2)}_s(τ^{(1)}_{u-s}(B))` then has strong derivative `iτ^{(2)}_s([V_2-V_1,τ^{(1)}_{u-s}(B)])`, and `G(u)-G(0)` is the stated integral. Pairing with unit vectors and using a continuous majorant of the integrand norm gives the inequality. ∎

The **unbounded onsite terms never enter the source**: in every pair used below they are identical in `H_1` and `H_2`; onsite terms of a larger box and the F2 padding are placed in the Hamiltonian whose evolution is inside the integral, where they factor out (this is the interaction-picture device of NS (78)–(79)). The Lieb–Robinson bound (51) for that inner evolution is applied as the theorem states it, with the onsite terms as its `H_x`; its own proof handles them through its interaction picture (54), (57).

## 3. The boundary source

### 3.1 The extra faces: characterization, count, owners and distances

**Lemma (HNM-BA2-F02).** A face `(b,K)` (anchor `b`, relative owner set `K` from the I1 table, `D_K` the set of directions `j` with `e_j` in `K`) is in F2 but not in F1 on `Lambda_N` if and only if `b` is in `Lambda_N`, `b_j<N` for every `j` in `D_K`, and `b_i=N` for some direction `i` not in `D_K`.

*Proof.* F2 keeps the face iff `b+K` lies in `Lambda_N`, i.e. `b` in `Lambda_N` and `b_j+1<=N` for `j` in `D_K`. F1 keeps it iff `b+S` lies in `Lambda_N`, i.e. `b_i<N` for all three `i`. ∎

**Count.** The table has 14 one-direction classes (owner sets `{0,e_y}` three times, `{0,e_x}` once, `{0,e_z}` ten times) and 7 two-direction classes (`{0,e_x,e_y}` once, `{0,e_x,e_z}` twice, `{0,e_y,e_z}` four times). Per one-direction class the count is `2N[(2N+1)^2-(2N)^2]=2N(4N+1)`; per two-direction class `(2N)^2[(2N+1)-2N]=4N^2`. Hence

\[
 \#\{\text{extra faces}\}=14\cdot2N(4N+1)+7\cdot4N^2=28N(5N+1),\qquad
 \#\{\text{(face, owner) incidences}\}=28N(11N+2).
 \tag{HNM-BA2-F02}
\]

The enumeration on the actual boxes confirms 616, 1344 and 2352 extra faces for `N=2,3,4` (equal to the F2 minus F1 counts), 1344, 2940 and 5152 incidences, and every per-class count; the class-sum identities are checked for `N` from 2 to 199.

**Owners and distances.** An owner `y=b+k` (`k` in `K`) differs from `b` only in directions of `D_K`, so `y_i=b_i=N` for the direction `i` of the lemma; with `y` in `Lambda_N` this gives `max_i |y_i| = N`: **every owner lies on the outer layer**. Then `d(e_z,y)=|y_x|+|y_y|+|y_z-1|` is at least `N-1` (if `y_z=N`) or at least `N` (if `y_x=N` or `y_y=N`), and `d(0,y)=||y||_1` is at least `N`. Both are attained (at `y=(0,0,N)`, an owner of the xy faces anchored there). The enumeration gives the minima 1, 2, 3 from `e_z` and 2, 3, 4 from `0` for `N=2,3,4`. None of the extra faces meets `R`, so none of the 82 faces meeting `R` (nor the 10 inside `R`) is in the source; those pins are re-derived at both sites of `R` from the I1 table by translation covariance (49 faces per factor, 15 owner sets).

**Charged once.** The source is the set of extra faces indexed by (anchor, class); each face appears once, with norm `|tau|/3`.

### 3.2 The padding factorizes exactly

`\widehat H^{F2,pad}_N=\widehat H^{F2}_N\otimes1+1\otimes\sum_{x\in B_+\setminus\Lambda_N}h_x` on `H_{Lambda_N}⊗H_{B_+ minus Lambda_N}`, where `\widehat H^{F2}_N` is F2 without padding. The two summands are self-adjoint on separate tensor factors; the closure of their sum on the algebraic tensor product of domains generates `e^{iu\widehat H^{F2}_N}⊗e^{iu h_pad}` (Reed–Simon VIII.33 as cited by the source; cited, not machine-checked). Therefore

\[
 T^{F2,{\rm pad},N}_\theta(A\otimes1)=T^{F2,N}_\theta(A)\otimes1\qquad(A\in\mathcal B(\mathcal H_{\Lambda_N})),
 \tag{HNM-BA2-F03}
\]

and `H^{F2}_N - H^{F1}_N` on `Lambda_N` is exactly the bounded sum over the extra faces. `check.py` verifies the algebraic step exactly with Gaussian-rational unitaries (Cayley transforms) and rejects a source that keeps a padding onsite term (its norm grows with every onsite cutoff). The padding has `3(2N+1)^2` sites (75 at `N=2`, 147 at `N=3`). Without padding, F2 on `Lambda_N` is the native restriction of the owner-set interaction `Phi'(M)=-(tau/3) sum_{M_f=M} W_f` (`||Phi'||_F<=1323|tau|`, AY1 reverse); that interaction is **named only** and enters no forward constant.

### 3.3 Fine units (descriptive; no constant uses them)

A coarse step is `(4a,2a,a)`. The coarse `l1` distance `N-1` from `e_z` is realized along `z`, where one coarse step is one fine step: the link tails of the extra faces are at least `N-1` fine steps from the tails of `R`'s 48 links (enumerated: 1 at `N=2`, 2 at `N=3`). The plaquette corners of the extra faces come within `N-2` fine steps of `R`'s 36 endpoints (they touch at `N=2`), and no link is shared. Only link sets matter for commutation, and the constants use the coarse `l1` metric alone.

## 4. The comparison of the two families (forward route)

**Theorem (HNM-BA2-F04).** For `N` at least 2, both signs of `|tau|<=10^-8`, every `A` in `B(H_R)` and `|theta|<=8`,

\[
 \|T^{F2,N}_\theta(A)-T^{F1,N}_\theta(A)\|\le b(N)\|A\|,\qquad
 b(N)=\frac{|\tau|}{3}\,\Lambda(U)\,S_b(N),\quad U=1,
\]

\[
 \Lambda(U)=\int_0^U\frac2C\big(e^{vr}-1\big)dr=\frac{2}{Cv}\big(e^{vU}-1-vU\big)\le\frac{2\|\Phi\|_FU^2}{1-vU/3},\quad v=2\|\Phi\|_FC,\qquad
 S_b(N)=\sum_{f\ {\rm extra}}\ \sum_{x\in R}\sum_{y\in M_f}F(d(x,y)) .
 \tag{HNM-BA2-F04}
\]

*Proof.* Apply (F01) on `Lambda_N` with `H_1=\widehat H^{F1}_N` (inner) and `H_2=\widehat H^{F2}_N`; by (F03) the padded F2 evolution gives the same operator. The source is `V=sum_{f extra}(-tau/3)W_f`. For each extra face, `W_f` is in `A_{M_f}`, `M_f` is disjoint from `R` (its owners lie on the outer layer and `N` is at least 2), and (51) with `X=R`, `Y=M_f`, `Λ=Lambda_N`, the whole-star `Φ` and `D(R,M_f)<=sum_{x in R} sum_{y in M_f} F(d(x,y))` (the Φ-boundary is a subset) gives `||[W_f,T^{F1,N}_r(A)]||<=(2||A||/C)(e^{v|r|}-1)D(R,M_f)`. Add linearly over faces, multiply by `|tau|/3`, integrate over `r` in `[0,|u|]`, use monotonicity in `|u|<=U`, and bound `e^x-1-x<=x^2/(2(1-x/3))` for `0<=x<3` (because `k!` is at least `2·3^(k-2)` for `k` at least 2). ∎

**Why quadratic in `tau`; the first order.** With the onsite evolution alone, `T^0_r(A)=e^{irH_loc}Ae^{-irH_loc}` stays in `B(H_R)` (product of onsite unitaries), and every extra face acts on links owned outside `R`, so `[W_f,T^0_r(A)]=0`: the first-order Dyson term vanishes exactly. In the bound, one factor `|tau|` is the face coefficient and one is the Lieb–Robinson growth `e^{vr}-1=O(|tau|)`, which vanishes at `r=0` because the supports are disjoint.

**All-size bound.** Every extra face has at most 3 owners; each owner contributes `F(d(e_z,y))+F(d(0,y))<=N^-4+(N+1)^-4<=2N^-4`. So

\[
 S_b(N)\le 3\cdot28N(5N+1)\cdot2N^{-4}=168\,(5N+1)N^{-3},\qquad
 b(N)\le K_{\rm cmp}\,(5N+1)N^{-3},\quad K_{\rm cmp}=\frac{|\tau|}{3}\cdot\frac{4536|\tau|}{1-338688|\tau|}\cdot168=\frac{254016\,\tau^2}{1-338688|\tau|}.
 \tag{HNM-BA2-F05}
\]

**Evaluation at the cap** (`|tau|=10^-8`, both signs; the `-tau` value is a replay of the same `|tau|` formula, not a second confirmation). `v=0.01016064` exactly; `Lambda(1)<=567/12457664` (preview `4.55141509676e-5`).

| quantity | exact | preview |
|---|---|---|
| `K_cmp` | `3969/155720800000000` | `2.54879245418e-11` |
| frozen target | `3/50000000000` | `6e-11` |
| margin | | `2.35405` |
| `b(2)`, all-size | `K_cmp·11/8` | `3.50458962450e-11` (target `8.25e-11`) |
| `b(3)`, all-size | `K_cmp·16/27` | `1.51039552840e-11` |
| `b(10)`, all-size | `K_cmp·51/1000` | `1.29988415163e-12` |

The coefficient is increasing in `|tau|`, so the cap value bounds every smaller `|tau|`.

**Labelled refinement (same tier, same route; not the headline).** The exact enumerated sums are `S_b(2)=616396498531/82978560000` (about `7.42838`), `S_b(3)` about `3.93816`, `S_b(4)` about `2.47618`; they give `b(2)` about `1.12699e-12`, `b(3)` about `5.97473e-13`, `b(4)` about `3.75671e-13`, i.e. 3.2–4.5% of the all-size bound. The all-size bound spends its slack on charging every owner at the minimal distance.

**Labelled weaker bound (retained, fails).** The triangle inequality through the common limit gives only `2K_c1/(N-1)` (preview `1.18943647862e-10/(N-1)`). Since `(5N+1)(N-1)N^-3<=11/8` and `2K_c1` exceeds `(11/8)·6x10^-11`, this misses the comparison target at every `N` at least 2 (checked exactly for `N` up to 59 and by that inequality for all `N`). Its dominating term is the `1/N` polynomial tail of all faces outside `Lambda_N`. It is reported as a weaker bound only.

## 5. Within-family Cauchy estimates (sup over all larger boxes) and distances to the limit

**Lemma (HNM-BA2-F06).** Let `E_N` be the set of faces whose anchor star `b+S` is not inside `Lambda_N`. Every point `y` of such a star has `||y||_inf` at least `N`. Hence every owner of a face of `E_N` has `||y||_inf` at least `N`, and every face with `M_f` not inside `Lambda_N` is in `E_N`. For every `M` greater than `N`: F1(M) minus F1(N), F2(M) minus F1(N) and F1(M) minus F2(N) are subsets of `E_N`, and F1(N) ⊂ F1(M) ⊂ F2(M), F2(N) ⊂ F1(M).

*Proof.* If `b` is outside `Lambda_N`, some `|b_i|` is at least `N+1` and `y_i` is `b_i` or `b_i+1`, so `|y_i|` is at least `N`. If `b` is inside, some `b_i=N` and `y_i` is at least `N`. An F2 face on `Lambda_N` has its anchor in `Lambda_N` and its star in `Lambda_{N+1}`. ∎ (`check.py` audits all inclusions for `(N,M)=(2,3),(2,4),(3,4)` and the owner layer of `E_N` on windows around `Lambda_2`, `Lambda_3`.)

**Tail lemma (HNM-BA2-F07).** At most 49 omitted faces contain a given site in their owner set (incoming faces included; 21 outgoing only is rejected). The shells satisfy `4r^2+2<=4(1+r)^2` and `sum_{k from m+1} k^-2<=1/m` (telescoping). Since `||y||_inf` at least `N` implies `d(0,y)` at least `N` and `d(e_z,y)` at least `N-1`,

\[
 S_c(N):=\sum_{f\in E_N}\sum_{x\in R}\sum_{y\in M_f}F(d(x,y))\le49\Big(\frac4N+\frac4{N-1}\Big)\le\frac{392}{N-1}.
 \tag{HNM-BA2-F07}
\]

**Theorem (HNM-BA2-F08), F1.** For `N` at least 2, every `M` greater than `N`, `A` in `B(H_R)`, `|theta|<=8`:

\[
 \|T^{F1,M}_\theta(A)-T^{F1,N}_\theta(A)\|\le\frac{|\tau|}{3}\Lambda(1)S_c(N)\|A\|\le\frac{K_{c1}}{N-1}\|A\|,\qquad
 K_{c1}=\frac{592704\,\tau^2}{1-338688|\tau|}=\frac{9261}{155720800000000}\ (\approx5.94718239310\times10^{-11}).
\]

*Proof.* On `Lambda_M`, take the inner Hamiltonian `sum_{x in Lambda_M} h_x + sum_{X subset Lambda_N} Φ(X)` (the (44) instance of `Φ_N`); by the tensor factorization its evolution of `A` is `T^{F1,N}(A)⊗1`. The outer Hamiltonian is `\widehat H^{F1}_M`. Their difference is the sum of the new whole stars, each meeting `Lambda_M minus Lambda_N`; split each star into its 21 faces (each charged once). Every such face is in `E_N`, disjoint from `R`. Apply (F01), (51) for `Φ_N` (with `‖Φ_N‖<=2268|tau|`, `C<=224`) and (F07). The bound does not depend on `M`. ∎

Letting `M` go to infinity (NS Theorem 4.1, or directly this Cauchy bound) gives `||T_theta(A)-T^{F1,N}_theta(A)|| <= K_c1/(N-1)||A||`.

**Theorem (HNM-BA2-F09), F2.** For `N` at least 2, `A` in `B(H_R)`, `|theta|<=8`:
- (a) `||T^{F2,N}_theta(A)-T_theta(A)|| <= K_c1/(N-1)||A||`. *Proof:* for `M` at least `N+1`, F2(N) ⊂ F1(M). On `Lambda_M` take the inner `\widehat H^{F1}_M` (whole-star `Φ` on `Lambda_M`) and the outer `sum_{x in Lambda_M} h_x` plus the F2(N) faces, whose evolution of `A` is `T^{F2,N}(A)⊗1` by (F03). The source is minus the faces of F1(M) minus F2(N), all in `E_N`. Apply (F01), (51), (F07), then let `M` go to infinity.
- (b) `sup over M greater than N of ||T^{F2,M}_theta(A)-T^{F2,N}_theta(A)|| <= [K_c1 + K_cmp(5N+1)(N-1)N^-3]/(N-1)·||A|| <= K_c2/(N-1)||A||` with `K_c2=K_c1+(11/8)K_cmp=941976 tau^2/(1-338688|tau|)=117747/1245766400000000` (about `9.45177201761e-11`). *Proof:* triangle through `T^{F1,N}`. The first term is one Duhamel pair on `B_+(M)`: inner F1(N) with all onsite terms of `B_+(M)`, outer padded F2(M), source F2(M) minus F1(N), all in `E_N`, so it is at most `K_c1/(N-1)||A||`. The second is (F04). Finally, `(5N+1)(N-1)N^-3` is at most `11/8` for `N` at least 2 (it decreases in `N`). ∎

A valid alternative, not used as the headline: (a) at `N` and at `M` gives `2K_c1/(N-1)`, also below the Cauchy target.

**Targets.** `K_c1` (about `5.94718e-11`) and `K_c2` (about `9.45177e-11`) are both at most the frozen `2.5x10^-10` (margins `4.20367` and `2.64500`), for every `N` at least 2.

**Honest rate.** With `F(r)=(1+r)^-4` the tail over `||y||_inf` at least `N` is of order `1/N`: `check.py` computes an exact lower bound over the slab `N<=y_z<=2N`, `|y_x|,|y_y|<=y_z`, with `N` times it at least `0.0255` for `N` up to 30, which contradicts any `C_0 q^N` tail with `C_0=1`, `q=1/2` from `N=9` on. The comparison decays like `N^-2` and the Cauchy bounds like `1/N`. These are the rates of the method; no lower bound on the actual dynamics difference is claimed, and no exponential decay in `N` is claimed. A bound for `N` to `N+1` alone is not a Cauchy estimate; summing step bounds of order `1/k` diverges (the harmonic partial sums are checked exactly). The estimates above are bounds for all `M` greater than `N` at once.

## 6. The F2 limit dynamics is `T_theta`; AQ1 sections 4–5 for F2 limit states (AY2 row O6)

**Whole-sequence convergence and identification (HNM-BA2-F10).** By (F09a), `T^{F2,N}_theta(A)` converges in norm to `T_theta(A)`, uniformly for `|theta|` at most 8, as a whole sequence (also from the Cauchy bound (F09b)). Through the comparison: `||T^{F2,N}_theta(A)-T_theta(A)|| <= b(N)+K_c1/(N-1)`, which tends to 0. For a general local `A` in `B(H_X)`, `X` inside `Lambda_n`, and any compact window `|u|<=U`, the same Duhamel argument with `N` at least `n+1` gives `||T^{F2,N}_u(A)-T_u(A)|| <= (|tau|/3)Lambda(U)·49|X|·4/(N-n)·||A||`, which tends to 0 (qualitatively on every compact window, with `Lambda(U)=(2/(Cv))(e^{vU}-1-vU)`; the frozen targets concern `|theta|` at most 8 only). Since `T` extends to a group of automorphisms of the quasi-local algebra (NS Theorem 4.1), the F2 limit dynamics equals the AQ1 limit dynamics on the whole quasi-local algebra.

**F2 limit states.** AY1 section 3.4 gives, for F2, local trace-norm compactness and a diagonal extraction of its own: along a subsequence `N_k` of F2 boxes the ground densities `rho^(2)_{N_k}` converge in trace norm on every finite region to a locally normal, gauge-invariant state `omega^(2)` (a chosen subsequential limit; nothing identifies different ones). For every such `omega^(2)`, with F2's own `N_k`:

1. **Stationarity.** Each F2 box ground state is invariant under its own evolution: `omega_N(T^{F2,N}_u(B))=omega_N(B)`. For local `A` and `n` fixed, `T^{F2,n}_u(A)` is local, so `omega^(2)(T^{F2,n}_u(A))=lim_k omega_{N_k}(T^{F2,n}_u(A))`, and `|omega_{N_k}(T^{F2,n}_u(A))-omega_{N_k}(A)| <= ||T^{F2,n}_u(A)-T^{F2,N_k}_u(A)||`. With `eps_n=sup_{|u|<=1}||T_u(A)-T^{F2,n}_u(A)||` this gives `|omega^(2)(T_u(A))-omega^(2)(A)| <= 2eps_n`, which tends to 0. Stationarity for quasi-local `A` follows by norm density and isometry, and for all `u` by the group property.
2. **GNS unitaries.** `U_u pi(A)Omega = pi(T_u(A))Omega` is well defined and extends to a unitary group, with `U_u Omega = Omega`.
3. **Strong continuity.** For fixed `n`, `u ↦ T^{F2,n}_u(A)` is strong-* continuous, and the normal density of `omega^(2)` on `Lambda_n` makes `u ↦ omega^(2)(A* T^{F2,n}_u(A))` continuous (finite-rank approximation of the trace-class density). The approximation error is at most `||A||·eps_n` for `|u|<=1`, so `u ↦ omega^(2)(A* T_u(A))` is continuous there. Then `||(U_u-1)pi(A)Omega||^2 = 2omega^(2)(A*A)-2Re omega^(2)(A*T_u(A))` tends to 0 as `u` tends to 0; local cyclic vectors are dense, and a unitary group that is strongly continuous at 0 is strongly continuous everywhere. Stone's theorem gives a self-adjoint generator `H^(2)_num` with `U_t=exp(itH^(2)_num/hbar)` in physical time.
4. **Nonnegative generator.** For local `A`, `c_{N,A}(u)=omega_N(A* T^{F2,N}_u(A))` is the Fourier transform of a positive measure on `[0,∞)`, because `\widehat H^{F2}_N` minus its ground energy is nonnegative (simple ground with gap at least `1/2`, AY1 via AM2). Along `N_k`, `c_{N_k,A}(u)` converges to the inner product of `pi(A)Omega` with `U_u pi(A)Omega` for every real `u`, by the compact-window convergence above, local trace-norm convergence and an approximation at fixed `n`; it is bounded by `||A||^2`. Nonnegative smooth tests supported in the negative half-line have integrable Fourier transforms, so dominated convergence passes their zero integrals to the limit spectral measure. The negative spectral projection therefore annihilates every local cyclic vector, and by density it is zero: `H^(2)_num` is nonnegative.
5. **Physical sector.** F2 box ground states are gauge invariant (every retained term is a Wilson loop; simple ground), so `omega^(2)` is gauge invariant; `T` preserves the norm-closed gauge-invariant algebra (norm limit of gauge-covariant finite evolutions). The physical cyclic space therefore reduces `U` and `H^(2)_num`, and the restriction is a nonnegative self-adjoint physical generator.

Stationarity alone would not give step 4: the checker's fixture `H=diag(0,1)` with the invariant excited vector has a correlation of frequency `E_0-E_1=-1`; the finite ground property is what is used. Only strong continuity of the GNS group is claimed; norm continuity in time on full `B(H)` fails (the AQ1 fixture `U(t)e_j=e^{ijt}e_j`, `Ae_j=e_{2j}`, gives 2 on the moving vector `e_n`).

These statements hold for each F2 subsequential limit state separately. **They do not identify F2 limit states with each other or with F1 limit states**, and no whole-sequence convergence of states is claimed.

## 7. Meaning, mandatory sentence and gate fields

**Meaning.** The comparison and the Cauchy estimates concern the algebraic Heisenberg dynamics of the named constructions on a compact time window, in the operator norm on `B(H_R)`, uniformly for `|theta|` at most 8, at a rate in `N` at fixed spacing. They do not assert equality of GNS dynamics or of correlation functions of different states; that needs a common state (BB2). A fixture in `check.py` shows one automorphism group with two invariant vector states whose `sigma_x` correlations differ (`(3+4i)/5` versus `(3-4i)/5`). The bounds grow like `U^2/(1-vU/3)` (exactly `(2/(Cv))(e^{vU}-1-vU)`) and say nothing outside the window.

**Mandatory sentence (the contract template, verbatim, once):**

For the zero-selected patterned family at the same coupling |tau|<=10^-8 and every A in B(H_R) with ||A||<=1 on the fixed cover R, the finite-box Heisenberg evolutions T^{F1,N}_theta and T^{F2,N}_theta of the named construction families F1 and F2 on the same centered coarse cube Lambda_N satisfy ||T^{F2,N}_theta(A)-T^{F1,N}_theta(A)|| <= b(N) for |theta|<=8 in the common clock theta=alpha t/hbar; this is an algebraic comparison of the dynamics of the named constructions on a compact time window at a rate in N, not equality of GNS dynamics or of correlation functions of different states, not a uniform-in-time statement, and not a statement uniform in the lattice spacing a.

The constant in it: `b(N) <= K_cmp (5N+1) N^-3` with `K_cmp=3969/155720800000000` (about `2.54879e-11`) at the cap; the families are F1 = AQ1 centered whole-star boxes and F2 = I1 section 6 all-contained-face boxes with padding, on `Lambda_N=[-N,N]^3`, `N` at least 2; `R={0,e_z}` (48 links, 36 endpoints).

**Gate fields exported in `results.json`** (exactly `gate_fields_required`; a true field is exported true only because its target is admitted here): `rate_in_N_claimed: true`, `whole_sequence_claimed: true`, `dynamics_limit_identified_claimed: true`; `uniqueness_of_ground_state_claimed`, `gns_dynamics_equality_claimed`, `uniform_in_time_claimed`, `rate_in_a_claimed`, `continuum_claim`, `scientific_priority_verified`, `common_limit_claimed`, `state_convergence_claimed`, `translation_invariance_claimed`, `weak_coupling_claim` all `false`; `whole_sequence_scope` and `dynamics_level: algebraic_heisenberg_compact_window` as in the contract. `common_limit_claimed: false` is read as "no common limit state"; the identification of the dynamics is `dynamics_limit_identified_claimed` (wording note W3).

## 8. Scaling `tau` to `tau/100`

All three headline coefficients have the form `c tau^2/(1-338688|tau|)`, so the exact ratio from the same formula without intermediate rounding is

`C(10^-8)/C(10^-10) = 1953058850/194651` (preview `10033.64406`),

inside the preregistered `[9500,10500]` (comparison and Cauchy, F1 and F2) and inside the control bracket `[9900,10100]`. A linear-order bound (ratio 100, e.g. the trivial commutator bound `2||A||` without the Lieb–Robinson factor) and a cubic one (`10^6`) are rejected, as is a bracket chosen after evaluation. Each coefficient is increasing in `|tau|` (checked at `tau/2`, `tau/10`, `tau/100`, `tau/1000`).

## 9. Exact finite fixtures for the traps

- **Polynomial versus exponential tail:** the exact slab lower bound of the tail (Section 5) contradicts an exponential tail from `N=9`; `F(r)=(1+r)^-3` violates (40) (partial shell sums exceed 7); an exponential instance carrying AQ1's `||Phi||_F` instead of its own `e^{2mu}81J` is rejected.
- **Unbounded onsite term placed wrongly:** placing `h_x` inside the bounded interaction makes `||Phi||_F`, and the velocity `2||Phi||_F C`, grow with every onsite cutoff (4032, 44352, 447552 at cutoffs 10, 100, 1000); a Cauchy source containing the onsite terms of the larger box is unbounded. Both are rejected; the onsite terms enter only as the `H_x` of (44).
- **Padding onsite terms left in the Duhamel difference:** rejected (cutoff-dependent source norm); the exact factorization fixture shows they drop out.
- **Inner-family constant swapped:** the F1-inner comparison evaluated with `Phi'`'s `1323|tau|` (preview `1.48469e-11`), with or without the label, is rejected; only the inner family's constants enter.
- **`N` to `N+1` bound summed as a Cauchy estimate:** rejected; the harmonic partial sums `H(2^m)-1` grow past 6.5 at `m=10`.
- Also: two-anchor and outgoing-only per-site counts (7, 14, 21), a face charged twice, an old face meeting `R` in the source, a regrouped F2 group charged whole, different couplings (the source would contain all 82 faces meeting `R`), the four drawn links or one factor as the cover, and the alternating sequence `(-1)^N/7` whose parity subsequences converge without any Cauchy bound.

## 10. Error ledger (preregistered terms)

| term | entry | note |
|---|---|---|
| `lieb_robinson_tail` | comparison `S_b(N)<=168(5N+1)N^-3`; Cauchy `S_c(N)<=392/(N-1)` | all-size bounds; the enumerated `S_b` for `N=2,3,4` is 3–5% of the bound |
| `duhamel_boundary_sum` | face norm `|tau|/3` times `Lambda(1)<=567/12457664` times the F-sum | faces added linearly, each charged once |
| `interaction_picture_onsite` | 0, `not_applicable` | onsite terms identical in every Duhamel pair (padding and larger-box onsite terms sit in the inner Hamiltonian and factor out); (51) handles them by its own interaction picture |
| `inner_family_constants` | F1 inner: `C<=224`, `||Phi||_F<=2268|tau|`, `v=1016064|tau|` | monotone substitution of upper bounds |
| `arithmetic` | 0, `not_applicable` | exact Fractions; `e^x-1-x` replaced by the directed rational bound `x^2/(2(1-x/3))` |

Deterministic terms add linearly; there is no division by `sqrt(N)` or by the square root of a face count.

## 11. Controls

Each of the 35 contract controls is a check in `check.py` that rejects at least one damaging mutation through an explicit `AdmissionError` (never `assert`).

| control | damaging mutations rejected |
|---|---|
| `coherent_evidence_tampering` | with the packet hash rebound: a control Boolean flipped, the NS excerpt snapshot removed, `K_cmp` halved, `K_c2` replaced by `K_c1`, the GNS-equality flag set, `common_limit_claimed` set, one family only, the extra-face count changed |
| `exact_arithmetic_admission` | float, bool, NaN, zero denominator, a preview decimal read as an admission value |
| `no_priority_or_continuum_claim` | continuum, priority, weak-coupling flags set true |
| `changed_model_relabelled` | `tau=10^-14`, nonzero triple, fine-site metric, exponential weights, a `u` window, the AX1 route-B model, SU(3), 2D, finite graph |
| `insufficient_verdict_retained` | a missed comparison relabelled accepted, a miscounted source relabelled limited, `tau` retuned; retained: the triangle bound fails the comparison target at every `N` |
| `tau_scaling_exponent` | linear order (ratio 100), cubic order, bracket chosen after evaluation |
| `wrong_delta_alpha_hbar_clock` | eightfold `u` labelled `theta`, `hbar` dropped, `delta=alpha` |
| `missing_incoming_stars` | outgoing-star `J=7|tau|`, two-anchor count, 21 outgoing faces per site |
| `root_n_misuse` | division by `sqrt(N)` at `N=4`, division by the integer square root of the 616 faces |
| `tier_mixing_rejected` | exponential label on polynomial constants, missing tier, mixed interaction constants |
| `reverse_premise_isolation` | declaration false; reverse inventory with a deliberation, the forward BA2 report, a lens memo |
| `face_count_all_sites` | site-0-only count (49 instead of 82), a typed literal 84 |
| `uniform_in_N_not_in_a` | a claim of uniformity in the lattice spacing and an unqualified uniformity word next to a rate (neither is accepted). |
| `placeholder_span_rejected` | whitespace, vertical-bar and `e.g.` angle-bracket spans |
| `negation_aware_phrase_scan` | affirmative forbidden phrasings (three kinds); a negated clause passes |
| `parameters_declare_metric_weights_window` | `window` or `metric` field absent |
| `lieb_robinson_polynomial_tail` | `N` to `N+1` bound as Cauchy, a divergent harmonic step sum, an exponential rate with AQ1 constants |
| `lieb_robinson_F_declared` | `F=(1+r)^-3`, an exponential instance with AQ1's `||Phi||_F`, a `C` not from the convolution split |
| `lieb_robinson_form_quoted` | velocity factor 2 dropped, prefactor `1/C` dropped, min replaced by max in (52), (77) paraphrased, quotation from the AQ1 report, excerpt bytes changed |
| `unbounded_onsite_interaction_picture` | onsite term inside the bounded interaction, larger-box onsite terms in the Duhamel source |
| `duhamel_inner_family_constants` | F1 inner with `1323|tau|` unstated, relabelled owner-set, inner family unnamed |
| `extra_face_count_and_distance` | padding sites counted, all F2 faces charged, distance `N-2`, owner layer `N-1`, padding onsite charged |
| `duhamel_tau_order_quadratic` | quadratic bound labelled linear, the linear trivial-commutator bound |
| `time_window_named_common_clock` | a claim that the bound holds for all times (not accepted), a `u` window labelled `theta`. |
| `algebraic_not_gns_dynamics` | GNS-equality claim, correlations of different states equal, GNS-level label |
| `f2_limit_dynamics_equals_f1` | identification from local terms near `R` only, F1 subsequence used for F2 states, stationarity assumed |
| `two_families_named` | one family, a third (literal vertex boxes), orthant boxes |
| `subsequence_versus_whole_sequence` | whole-sequence state convergence, parity subsequences as whole-sequence basis, an unlabelled limit |
| `decay_rate_in_N_not_a` | a rate per fm, a rate in `a` |
| `boundary_source_new_terms_only` | an old face meeting `R` charged, a new star dropped, the old star at 0 charged in the Cauchy source |
| `f2_regrouping_charged_once` | a regrouped clipped group charged whole (its old faces twice), faces charged twice |
| `full_original_wilson_cover` | the four drawn links, a single factor |
| `topology_named` | strong topology relabelled norm, norm time continuity claimed |
| `cross_coupling_comparison_rejected` | opposite signs compared, different couplings compared |
| `gate_fields_topic_specific` | a field missing, `rate_in_a_claimed` true, `common_limit_claimed` true, `state_convergence_claimed` true |

**Source-edit audit (private scratch, not evidence).** Twelve edits were made to copies of this directory in `/tmp/claude-0/ba2-forward-private/audit/`. Eleven abort at the intended check: the comparison face-sum bound 168 replaced by 84 and the factor 2 dropped from the time integral (`comparison_bound_all_N`), the Cauchy face-sum bound 392 replaced by 196 (`within_family_cauchy_and_limits`), a two-direction class count `4N^2+1` (`extra_face_count_and_distance`), the F1-inner record given `Phi'`'s constant (`duhamel_inner_family_constants`), the contract target edited to `60x10^-11` (contract sha256, before any evaluation), the factor 2 removed from the quoted (51) (`lieb_robinson_form_quoted`), an affirmative forbidden phrasing (`negation_aware_phrase_scan`), a uniformity claim in the lattice spacing (`uniform_in_N_not_in_a`), a second copy of the template (`mandatory_sentence_verbatim_once`) and an angle-bracket placeholder (`placeholder_span_rejected`). The twelfth, removing the code-span backticks from a verbatim exclusion inside the negated exclusion sentence, is not damaging and passes, as intended.

**Not executable inside `check.py`:** what the reverse agent actually reads (checked by `freeze.py` and the skeptic); the freeze and the byte-identical replays (protocol steps of `research/round33/tools/freeze.py`).

## 12. Contract wording findings (non-blocking)

- **W1.** Required item 2 asks for the distance "converted to fine units", while `parameters.metric` says no coarse-to-fine conversion enters any constant. Section 3.3 gives the conversion descriptively only; the plaquette corners come within `N-2` fine steps of `R`'s endpoints (touching at `N=2`) while the link tails are `N-1` fine steps apart and no link is shared.
- **W2.** The control `parameters_declare_metric_weights_window` names `d_X` and `N_0` fields; this contract's `parameters` has `metric`, `weights`, `window`, `boundary_source` and `targets`, with `N` at least 2 stated inside the targets. The check requires the fields that exist.
- **W3.** `gate_fields_required` has `common_limit_claimed: false` and `dynamics_limit_identified_claimed: true`; the first is read as "no common limit state".
- **W4.** Required item 3 asks for a margin of at least 2, while `acceptance` calls the margin a freeze-time property; the margin here is `2.35405`, so both readings are met.
- **W5.** Two brackets for the same `tau` ratio: `[9500,10500]` (preregistration) and `[9900,10100]` (control semantics); the ratio `10033.64` is inside both.
- **W6.** `||Phi||_F<=81J=2268|tau|` is a valid upper bound; the exact (48) supremum for the whole-star interaction is `567|tau|` (Section 2.2), not used.
- **W7.** Item 3 writes both `b(N)` and `B(N)`; item 4 writes `tau^{F,M}` for `T^{F,M}`: the same objects.
- **W8.** Item 1 asks for (44)–(47) as placed; (47) exists only in the excerpt's Part B machine text (Section 2.1).
- **W9.** `boundary_source_new_terms_only` speaks of new terms "meeting the source set". For the Cauchy estimates the source set is `Lambda_M minus Lambda_N` and the new F1 terms are whole stars (each meets it; individual faces of a new star may lie inside `Lambda_N`); for the comparison on one box it is the outer layer. The check validates both.

## 13. Exclusions and limitations

**Contract exclusions.** None of the following is claimed (verbatim, comma-separated) — `equality of GNS dynamics or of correlation functions of different states`, `uniform-in-time statements`, `exponential decay in N with the polynomial Lieb-Robinson function`, `uniqueness of every infinite-volume ground state`, `any estimate uniform in the lattice spacing a`, `continuum or weak coupling`, `scientific priority`.

**Additional exclusions on this route:** no identification of limit states (F1 or F2) with each other; nothing claimed outside `|theta|` at most 8 at the frozen targets (outside it only the qualitative compact-window convergence of Section 6 is used); no exponential-tier constant (the optional instance is not executed); no fine-lattice or physical-length reading of `N`.

**Limitations.**
1. **Scope.** Only the zero-selected patterned family, the cover `R` (and, qualitatively, local observables in Section 6), fixed spacing, `|tau|<=10^-8` (extreme strong bare coupling), and the two named families on centered cubes. Nothing transfers to literal vertex boxes, periodic or orthant boxes, other couplings, weak coupling or the continuum.
2. **Inherited without re-proof:** Nachtergaele–Sims Theorems 3.1 and 4.1 (cited from the committed excerpt, not machine-checked); AQ1's `C<=224` and `||Phi||_F<=2268|tau|` (their arithmetic re-verified); AM2's simple ground and gap for F2 boxes via AY1; AY1's F2 compactness and extraction; the I1 dictionary; Stone's theorem, Fourier inversion, the tensor-product factorization (Reed–Simon VIII.33).
3. **Upper bounds.** All constants are upper bounds; the all-size face sum is about 22 to 31 times the enumerated sum at `N=2,3,4`; the admitted `||Phi||_F` is four times the exact (48) supremum.
4. **Correlation.** The route is named in the shared contract, selection note and AY2 table; independence from the reverse route is limited to the inner family, indexing, constants, enumeration and code; all agents are correlated model agents.
5. **Fixtures** are exact finite audits of algebraic steps and traps, not proofs of the infinite-volume statements.
6. **Scientific priority is unverified.**

**Methodological lenses (modern use of the snapshotted skills).** *Newton, analysis before synthesis:* the extra faces were characterized exactly (the lemma of Section 3.1) before any bound was written, and the first order was shown to vanish rather than assumed small. *Tesla, complete accounting:* every term of the two Hamiltonians is placed — faces in the source once each, onsite terms in the inner Hamiltonian, padding factored out. No historical figure endorses anything here, and no historical or occult material supplies a premise.

## 14. Map of contract items and controls to sections and checks

| contract item | report section | `check.py` check id(s) |
|---|---|---|
| 1 (verbatim NS, F, C, `‖Φ‖_F`, placement) | §2 | `lieb_robinson_form_quoted`, `lieb_robinson_F_declared`, `premise_constants_parsed`, `pinned_gates_and_source_excerpt`, `unbounded_onsite_interaction_picture`, `missing_incoming_stars` |
| 2 (extra faces, count, distance, charged once) | §3 | `extra_face_count_and_distance`, `padding_onsite_terms_factor_out`, `face_count_all_sites`, `boundary_source_new_terms_only` |
| 3 (comparison, quadratic, target) | §4 | `comparison_bound_all_N`, `duhamel_tau_order_quadratic`, `duhamel_inner_family_constants`, `root_n_misuse`, `cross_coupling_comparison_rejected` |
| 4 (Cauchy F1, F2; whole sequence; identification; O6) | §§5–6 | `within_family_cauchy_and_limits`, `lieb_robinson_polynomial_tail`, `f2_regrouping_charged_once`, `subsequence_versus_whole_sequence`, `f2_limit_dynamics_equals_f1`, `o6_limit_state_properties_rerun` |
| 5 (meaning, gate fields, template) | §7 | `algebraic_not_gns_dynamics`, `gate_fields_topic_specific`, `mandatory_sentence_verbatim_once`, `topology_named`, `time_window_named_common_clock` |
| 6 (scaling, traps, controls) | §§8–11 | `tau_scaling_exponent`, the 35 control ids, `error_ledger_itemized` |
| contract binding | header | `contract_snapshot_sha256` |

## 15. Reproduction

```bash
python3 -B research/round33/forward/ba2/check.py --output /absolute/fresh/dir
python3 -B -O research/round33/forward/ba2/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round33/tools/freeze.py verify research/round33/forward/ba2
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/ba2.json research/round33/forward/ba2/report.md
```

`check.py` verifies the contract sha256 before any evaluation, records its own sha256 before evaluation, compares the pinned sha256 of every admitted gate it reads and of the NS excerpt before reading values, and writes `results.json` (44 checks) and `source-manifest.json` (sha256 of `check.py`, `report.md`, every `inputs/` file and `results.json`). BA2 is investigation 2 of 8 in Round33; this producer executed only the forward half.
