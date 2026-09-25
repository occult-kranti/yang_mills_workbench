# Hruday whole-sequence convergence of the named constructions, their common limit and its coarse translation invariance — BB2 forward (assembly: nested telescoping)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production: the derivations, `check.py` and this report were written by a Claude model agent acting as the BB2 forward producer under the frozen BB2 contract (`research/round33/contracts/bb2.json`, sha256 `ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35`) and the frozen BB1 contract (`research/round33/contracts/bb1.json`, sha256 `30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018`); `check.py` verifies both digests before it parses any field. It is correlated model-agent work, not independent human review and not formal verification. HNM labels are project aliases.

**Status of every BB1-dependent statement: `conditional_on_bb1_targets`.** BB1 is in production. This packet uses only BB1's **frozen targets**, read from the two contracts, as explicit hypotheses (Section 0). It reads no BB1 producer, skeptic or gate file. No conclusion below that uses BB1 is unconditional; each becomes unconditional only when the BB1 gate admits, for every comparison, form, cutoff regime and sign that the item uses (Section 12), constants at most the hypothesis values.

**What this producer read.**
- **The contract snapshot first**, then the BB1 contract, then only files under `inputs/`:
  - *read in full:* `AGENTS.md`; `selection-bb2.md`; the committed Nachtergaele–Sims excerpt; the BA2 gate and the BA1 gate (every field except `bindings`); the AQ1 forward report and gate; the AQ2 forward report and gate; the I1 forward report; the Round32 lessons reference `round32-state-lemma-and-window.md`; the paired-physics SKILL, its complete-residual reference, and the Newton and Tesla SKILL files;
  - *read in part:* the BA2 forward report (header, verdict, sections 1, 2, 5, 6 and keyword lines); the BA1 forward report (keyword lines and its general-comparison paragraph); the BA1 reverse report (Theorem 4.1 and Section 4.2, keyword lines); the AV1 forward report (header, Section 1, Sections 7–8); the AY1 forward report (Sections 1 and 3); the AM2, AV1, AY1, AY2 and AW1 gates (`verdict`, `accepted`, `limitations`, `decision`, `gate_fields`); `skeptic/ba2.md` (keyword lines and its advice for BB2); `skeptic/ba1.md` (keyword lines); the historical-panel SKILL (first sixty lines);
  - *not opened:* the AM2 forward and reverse reports, `skeptic/am2.md`, the AW1 and AY2 forward reports, the AY1 and AV1 reverse reports, the BA2 reverse report (their gates or the named sections above carry what is used).
- **Outside `inputs/`, for protocol and code conventions only:** `research/round33/tools/README.md`, `research/round33/tools/freeze.py`, `research/round33/tools/phrase_scan.py` (its round phrase list is copied into `check.py` as infrastructure) and `research/round33/forward/ba2/check.py` (conventions only; BA2 is gated). None of these carries premise weight.
- **Not read:** anything under `research/round33/forward/bb1/`, `research/round33/reverse/bb1/`, `research/round33/reverse/bb2/`, `research/round33/skeptic/` other than the two snapshotted reviews, `research/round33/experts/`, `research/round33/advisor/` other than the snapshots in `inputs/`; no other agent's scratch folder.
- **Scratchpad disclosure.** My private scratch folder is `/tmp/claude-0/bb2-forward-private/`: one Fraction prototype of the headline constants (`proto1.py`), development runs and the production run `run1`. **None of it is evidence.** I created the folder with `mkdir -p` and did not list `/tmp/claude-0/`, so I saw no other agent's folder names and opened no file in any other agent's folder. The Claude harness cached one of my own long reads (part of the BA2 forward checker) in its tool-results store; that is my own read. **File-name exposure:** after the first freeze, a `git status` listing from the repository root (run to confirm that only this directory had changed) showed the names of two untracked files of other agents, `research/round33/reverse/bb2/check.py` and `research/round33/skeptic/bb2_check.py`. I opened neither; every derivation and constant here was fixed before that listing, and only this disclosure was added afterwards.

**Shared premises and attribution.** The route (nested telescoping of BB1's nested comparisons, AV1 cutoff removal at fixed `N`, identification with AQ1 limits, the general-volume comparison for translations, BA2's dynamics constants for correlations) is named in the contract, the selection note and the AY2 obligations table; on this route those are shared premises. Completeness of the trace class, partial-trace contractivity, the GNS construction and its uniqueness up to unitary equivalence are standard. The limit dynamics and the Lieb–Robinson bound are Nachtergaele–Sims (arXiv:1410.8174v1, Theorems 3.1 and 4.1). The compactness/GNS/Fourier strategy of AQ1–AQ2 is credited there to Gauvin arXiv:2503.15539v3 Supplement A.10. Independence from the reverse producer is limited to the assembly (telescoping here, unions there), the constants and the code. Scientific priority is unverified.

## Verdict (forward route)

Model: **`AQ_patterned_zero_selected`** (AM2/AQ1 zero-selected patterned family: SU(2) Kogut–Susskind form on `Z^3` at fixed spacing, coarse 24-link factors, selected triple `(0,0,0)`, 21 omitted faces per anchor entering as `-(tau/3)W_f` in normalized units `delta=alpha/8`), both signs, `|tau|` at most `10^-8`, each sign separately. Families on the centered coarse cubes `Lambda_N=[-N,N]^3`, `N` at least 2: **F1** = AQ1 centered whole-star boxes, **F2** = I1 section 6 all-contained-face boxes with padding. Reduced densities `rho^{F,N}_Y` of the normalized untruncated finite-box ground vectors on finite complete-factor regions `Y`, in the trace norm on `B(H_Y)`; cover `R={0,e_z}`. Assembly: **nested telescoping** (recorded in the `assembly` field, never as a route label).

All five items are proved **conditional on the BB1 frozen targets** (`q=1/64`, `C_h=1/250000`, `c_h=1/500000`):

1. **Whole-sequence Cauchy estimate** (sup over **all** `M` greater than `N`), for F1 and F2, on `R` and on every finite region `Y`, in each on-site cutoff space and then for the untruncated vectors: `C' = C_h/(1-q) = 4/984375` (preview `4.06349206349e-6`, target `1/100000`, margin `2.4609375`) and `c'_site = c_h/(1-q) = 2/984375` (preview `2.03174603174e-6`, target `1/200000`, margin `2.4609375`). The limit exists on every finite region **without compactness**.
2. **Common limit** of F1 and F2 on every finite region.
3. **Identification** with every AQ1 subsequential limit and every F2 subsequential limit; the inherited properties are listed exactly in Section 4.
4. **Coarse translation invariance**: `||rho^{Lambda_N+v}_R-rho^{Lambda_N}_R||_1 ≤ C_h q^(N-|v|_inf-1)` for `N ≥ |v|_inf+2`, from the general-volume comparison; non-coarse translations are rejected.
5. **Correlation functions** on `|theta| ≤ 8`: three separate constants, `C_dyn = 2K_F1 + K_cmp/4 = 78057/622883200000000` (preview `1.25315628997e-10`, tier `polynomial_lieb_robinson`, route `duhamel_inner_f1`, target `1/2000000000`, margin `3.98992`), `c'_site` and `C'`; `r_N=floor((N-1)/2)`; the rate is `O(1/N)`.

**Constants and labels** (one tier, the assembly and the hypothesis source per state constant; the tier and one route per dynamics constant):

| constant | exact value | preview | target | tier | assembly | source | route |
|---|---|---|---|---|---|---|---|
| `C'` | `4/984375` | `4.06349206349e-6` | `1/100000` | `exact_first_order` | `nested_telescoping` | `bb1_frozen_targets` | BB1 route attached at the BB2 gate |
| `c'_site` | `2/984375` | `2.03174603174e-6` | `1/200000` | `exact_first_order` | `nested_telescoping` | `bb1_frozen_targets` | BB1 route attached at the BB2 gate |
| item-4 constant (`C_h`, factor 1) | `1/250000` | `4e-6` | none frozen | `exact_first_order` | `nested_telescoping` (direct `H4` through `Lambda_{N-|v|_inf}`) | `bb1_frozen_targets` | BB1 route attached at the BB2 gate |
| `C_dyn` | `78057/622883200000000` | `1.25315628997e-10` | `1/2000000000` | `polynomial_lieb_robinson` | not applicable | BA2 gate `K_F1`, `K_cmp` | `duhamel_inner_f1` |

**Checker.** `check.py` runs **52 exact checks**; all **34 contract controls** reject explicit damaging mutations (**122** rejections in total); the `-B` and `-B -O` outputs are byte-identical.

**Proposed forward verdict: `accepted_within_scope`, conditional_on_bb1_targets** — for the forward half only, sub-labels `convergence_of_named_constructions` and `common_limit_of_named_constructions`. It becomes unconditional only after the BB1 gate discharges every hypothesis listed in Section 12; otherwise the contract's `limited` or `insufficient` outcome applies with the undischarged items retained as labelled conditional statements. The contract acceptance also requires the reverse route and the skeptical review, which are outside this producer's work.

## 0. The hypotheses (BB1 frozen targets) and the admitted inputs

**Hypotheses (read from `parameters.rate_constant_pair.hypotheses` and from the BB1 contract's frozen targets; `check.py` requires equality).** For every BB1 comparison, both signs, in each on-site cutoff space and at fixed `N` for the untruncated ground vectors, with `N` the smaller box size (for the general-volume comparison: the size of a centered cube contained in both volumes):

- **R form:** `||rho^{box1}_R-rho^{box2}_R||_1 ≤ C_h q^(N-1)`, `C_h = 1/250000`, `q = 1/64`;
- **region form:** for every finite complete-factor region `Y` inside `Lambda_N`, `||rho^{box1}_Y-rho^{box2}_Y||_1 ≤ c_h |Y| e^{|Y|/10^8} q^{d_Y}`, `d_Y = N - max_{y in Y}|y|_inf` (so `d_R = N-1`), `c_h = 1/500000`;
- **secondary pair (labelled):** `q_2 = 151552|tau|`, `C_2h = 1/20000`, `c_2h = 1/40000`.

The comparisons used are named `H1`–`H4` (Section 12): `H1` F1 on `Lambda_N` versus `Lambda_{N+1}`; `H2` F2 on `Lambda_N` versus `Lambda_{N+1}`; `H3` F1 versus F2 on the same `Lambda_N`; `H4` two finite complete-factor volumes of one prescription both containing `Lambda_N` (its coefficient input is BA1's accepted comparison of any two such volumes). The BB1 comparison "any two centered boxes `Lambda_M`, `Lambda_M'`, compared directly" is **not used** by this assembly.

**Admitted inputs (unconditional).**
- *BA2 gate* (sha256 `e6b163fc…`, pinned): for every `A` in `B(H_R)`, `|theta| ≤ 8`, `N ≥ 2`: `||T^{F2,N}_theta(A)-T^{F1,N}_theta(A)|| ≤ b(N)||A||`, `b(N) = K_cmp (5N+1) N^-3`, `K_cmp = 3969/155720800000000`; `sup_{M greater than N} ||T^{F1,M}_theta(A)-T^{F1,N}_theta(A)|| ≤ K_F1/(N-1)||A||`, `K_F1 = 9261/155720800000000`; the F2 analogue with `K_F2 = 117747/1245766400000000`; the F2 evolutions converge as a whole sequence to the AQ1 limit dynamics `T_theta`. The closed forms `K_cmp = 254016 tau^2/(1-338688|tau|)` and `K_F1 = 592704 tau^2/(1-338688|tau|)` are read from the BA2 forward report, reconstructed from `C ≤ 224` and `||Phi||_F ≤ 2268|tau|`, and checked equal to the gate values. All are tier `polynomial_lieb_robinson`, route `duhamel_inner_f1`. The second-route (`duhamel_inner_f2`) values are read and not used.
- *BA1 gate*: the coefficient comparison covers any two complete-factor volumes of one prescription containing `Lambda_N` (input of `H4`, used here only as the named input of that hypothesis).
- *AQ1 and AQ2 gates*: the subsequential state and its properties (Section 4). *AV1 gate/report* (F20–F23): ground-vector cutoff removal in each fixed box; *AY1 gate*: the same for F2, and F2 compactness with its own diagonal extraction. *AM2 gate*: simple ground and cutoff removal in every nonempty finite complete-factor volume.

## 1. Model, regions, topology, clock and cutoff order

**Boxes.** F1 on a finite complete-factor volume `V`: `H^{F1}_V = sum_{b in V} h_b + sum_{b+S ⊂ V} phi_b`, `S={0,e_x,e_y,e_z}`. F2 on `V`: every omitted face whose owner set lies in `V`, grouped at its anchor, padded to `V+S` with onsite terms only (the padded ground is a product with the onsite vacua on the padding, AY1). On `Lambda_N` these are the named families. A **coarse translation** `v` is the fine translation `(4v_x,2v_y,v_z)`; it preserves the residues `x mod 4`, `y mod 2`, the face classes and link ownership (I1.1, AV1 Section 1), and maps each prescription on `V` to the same prescription on `V+v` (Section 5).

**Regions and topology.** A finite complete-factor region `Y` is a finite set of coarse sites; `|Y|` is its number of sites; `d_Y = N - max_{y in Y}|y|_inf` for `Y` inside `Lambda_N`. States: the **trace norm on `B(H_Y)`**. Dynamics: the **operator norm on `B(H_R)`**, uniformly for `|theta|` at most 8 (BA2). Representations: the **GNS strong topology** (a strongly continuous unitary group). A fixed-vector versus moving-vector fixture and a mass-escape fixture are in `check.py` (`topology_named`).

**Clock and window.** `theta = alpha t/hbar`; the finite-box evolutions `T^{F,N}_theta(A) = e^{i(theta/8)H}Ae^{-i(theta/8)H}` with `delta=alpha/8`, and the AQ1 limit dynamics `T_theta`, all in the same clock, at the same coupling and sign. Window `|theta| ≤ 8` (normalized `u = theta/8`, `|u| ≤ 1`). The conversion is checked with non-unit constants (`alpha=5`, `hbar=7`, `t=56/5`).

**Cutoff order (Lemma C).** Fix a finite box `B` of F1 or F2 (centered or translated) and let `psi^B_L` be the normalized ground vector in the on-site cutoff space `Q_L`, `psi^B` the untruncated one. AV1 F21–F22 give `1-|⟨psi^B,psi^B_L⟩|^2 ≤ 2(E_{0,L}-E_0) → 0` (untruncated gap `1/2`); AY1 applies F20–F23 verbatim to F2; translated boxes follow by covariance. The pure-state trace distance and partial-trace contractivity give, for every `Y` inside `B`,

\[
\|\rho^{B,L}_Y-\rho^{B}_Y\|_1\ \le\ 2\sqrt{1-|\langle\psi^B,\psi^B_L\rangle|^2}\ \longrightarrow\ 0\qquad(L\to\infty,\ B\ \text{fixed}).
\tag{HNM-BB2-F00}
\]

Hence a bound `||rho^{B1,L}_Y-rho^{B2,L}_Y||_1 ≤ beta` that holds for every `L` with the same `beta` passes to the untruncated vectors. **Order:** (i) the bound in each `Q_L`, uniformly in the on-site cutoff `L`; (ii) `L → infinity` at fixed `N` and `M`; (iii) the supremum over `M`; (iv) `N → infinity` for the untruncated sequence only. The `N` and `L` limits are never exchanged; the double sequence `a_{N,L} = 1` if `L ≥ N`, else `0`, shows why (`lim_N lim_L = 1`, `lim_L lim_N = 0`). The degenerate fixture `diag(0,0,1)` shows that eigenvalue convergence without a gap gives no vector convergence.

## 2. Item 1 — the whole-sequence Cauchy estimate and the limit without compactness

**Theorem (HNM-BB2-F01), conditional_on_bb1_targets.** For `F` in `{F1,F2}`, each sign, `N ≥ 2` and every `M` greater than `N`,

\[
\|\rho^{F,M}_R-\rho^{F,N}_R\|_1\le\sum_{k=N}^{M-1}C_h q^{k-1}=\frac{C_h q^{N-1}(1-q^{M-N})}{1-q}\ \lneq\ C'\,q^{N-1},\qquad C'(C_h,c_h)=\frac{C_h}{1-q}=\frac{64}{63}C_h ,
\]

and for every finite complete-factor region `Y` inside `Lambda_N`,

\[
\|\rho^{F,M}_Y-\rho^{F,N}_Y\|_1\le\sum_{k=N}^{M-1}c_h|Y|e^{|Y|/10^8}q^{\,k-\max_{y\in Y}|y|_\infty}\ \lneq\ c'_{\rm site}\,|Y|\,e^{|Y|/10^8}q^{d_Y},\qquad c'_{\rm site}(C_h,c_h)=\frac{c_h}{1-q}=\frac{64}{63}c_h .
\]

*Proof.* Write `rho^{F,M}_Y - rho^{F,N}_Y` as the telescoping sum of `rho^{F,k+1}_Y - rho^{F,k}_Y` over `k = N, …, M-1`. Each step is the BB1 comparison `H1` (F1) or `H2` (F2) with smaller box `Lambda_k`, `k ≥ N ≥ 2`; `Y` lies in `Lambda_N ⊂ Lambda_k`, so its exponent is `k - max|y|_inf = d_Y + (k-N)`. The triangle inequality adds the steps linearly, and the geometric series gives the bounds. The argument is run in each `Q_L` with the `Q_L` hypotheses; the bound does not depend on `L`; Lemma C passes it to the untruncated vectors at fixed `N` and `M`; then the supremum over `M` is taken. The supremum `C' q^(N-1)` is the limit of the partial sums and is not attained. ∎

**Values at the hypotheses.** `C' = 4/984375` (preview `4.06349206349e-6`) at most `1/100000` (margin `984375/400000 = 2.4609375`); `c'_site = 2/984375` (preview `2.03174603174e-6`) at most `1/200000` (margin `2.4609375`). Both functions are linear with the positive coefficient `64/63` in one hypothesis constant and independent of the other, hence nondecreasing in each (checked exactly on an 8×8 rational grid). Tier `exact_first_order`, assembly `nested_telescoping`, hypothesis source `bb1_frozen_targets`; the BB1 route of the discharging constant is attached at the BB2 gate.

**Region dependence.** The region bound carries `|Y| e^{|Y|/10^8}` and the exponent `d_Y`. A constant proved for `R` is not reused on `Y`: at `N=5` on `Y=Lambda_2` the region form gives `c'_site·125·q^3` (preview `9.69e-10`) while the `R` form would give `C' q^4` (preview `2.42e-13`). The transcendental factor is enclosed by the directed bound `e^x ≤ 1/(1-x)` for `0 ≤ x` below 1.

**Existence without compactness (HNM-BB2-F02).** For fixed `Y`, `(rho^{F,N}_Y)_N` is Cauchy in the Banach space of trace-class operators on `H_Y`, so it converges in trace norm to some `rho^{F,inf}_Y` — **no compactness is used**. Positivity and unit trace are closed conditions; partial trace is a trace-norm contraction, so the limits are consistent (`Tr_{Y'\Y} rho^{F,inf}_{Y'} = rho^{F,inf}_Y`). Hence `omega^F_inf(B) = Tr(rho^{F,inf}_Y B)` for `B` in `B(H_Y)` is a well-defined state on the local algebra, bounded by `||B||`, and it extends by norm continuity to the quasi-local algebra, which Nachtergaele–Sims define as the norm completion (Part B, verbatim):

```text
where the union taken over all finite subsets of Γ. The completion of AlocΓ with respect to the
operator norm, which we denote by AΓ , is a C ∗ -algebra, and it will be called the algebra of all
quasi-local observables.
```

Letting `M → infinity` in F01: `||rho^{F,N}_R - rho^{F,inf}_R||_1 ≤ C' q^(N-1)` and `||rho^{F,N}_Y - rho^{F,inf}_Y||_1 ≤ c'_site |Y| e^{|Y|/10^8} q^{d_Y}`. A bound for `N` to `N+1` alone is not a Cauchy estimate (the harmonic fixture), and a one-state ball in every box does not give convergence (the alternating fixture); both are in Section 9.

## 3. Item 2 — the common limit of F1 and F2

**Theorem (HNM-BB2-F03), conditional_on_bb1_targets.** For every finite region `Y`, each sign: `rho^{F1,inf}_Y = rho^{F2,inf}_Y =: rho^inf_Y`.

*Proof.* For `N ≥ max(2, max_{y in Y}|y|_inf)`, the triangle inequality with F01 and the fixed-`N` comparison `H3` (region form) gives

\[
\|\rho^{F1,\infty}_Y-\rho^{F2,\infty}_Y\|_1\le(2c'_{\rm site}+c_h)\,|Y|e^{|Y|/10^8}q^{d_Y}\qquad\text{for every such }N ,
\]

and the right side tends to 0. On `R`, the R form gives `(2C'+C_h) q^(N-1)`. ∎ The common limit is written as the limit of the named constructions: `rho^inf_Y = lim_N rho^{F1,N}_Y = lim_N rho^{F2,N}_Y`, and `||rho^{F,N}_Y - rho^inf_Y||_1 ≤ c'_site |Y| e^{|Y|/10^8} q^{d_Y}` for both families. The state `omega_inf` is this common limit. It is the limit of the named constructions and nothing else: no statement is made about other boundary conditions or other states.

## 4. Item 3 — identification with every AQ1 and every F2 subsequential limit, and what is inherited

**Theorem (HNM-BB2-F04), conditional_on_bb1_targets.** Every AQ1 subsequential limit and every F2 subsequential limit equals `omega_inf` on the quasi-local algebra.

*Proof.* AQ1's construction is a subsequence `N_k` along which the F1 densities converge in trace norm on every finite region (AQ1 Section 2: "Diagonal extraction over the countable nested coarse cubes produces a subsequence N_k whose densities converge in trace norm on every finite F."). Since the whole sequence converges (F02), every subsequence has the same local limits: `rho^{AQ1}_Y = rho^inf_Y` for every finite `Y`. Two states that agree on the local algebra agree on its norm closure. For F2, AY1's own diagonal extraction gives trace-norm limits along F2 subsequences; by F03 they equal `rho^inf_Y`. ∎ **Identification precedes inheritance**; nothing is inherited before this step.

**Representation.** Let `(pi_inf, H_inf, Omega_inf)` be the GNS triple of `omega_inf`. For each identified subsequential state `omega` (equal to `omega_inf` as a state), `pi_inf(B)Omega_inf ↦ pi_omega(B)Omega_omega` is a well-defined unitary that intertwines the representations and, by stationarity, the time evolutions. Every inherited statement below holds in the GNS representation of `omega_inf`, up to this canonical unitary equivalence.

**Inherited — exactly the admitted properties, no more.**
- From the **AQ1 gate** (F1 subsequential limits): `omega_inf` is a compatible locally normal gauge-invariant state on the norm closure of the full bounded local algebras; it is stationary under `T_theta`; its GNS evolution `U_theta pi(A)Omega = pi(T_theta(A))Omega` is strongly continuous (GNS strong topology, not norm continuity in time on full `B(H)`); its self-adjoint physical energy generator is nonnegative; the physical cyclic space reduces it.
- From the **BA2 gate**, item (5) (AQ1 sections 4–5 rerun for every F2 subsequential limit with F2's own extraction): the same list; after F04 these are statements about the same state.
- From the **AQ2 gate**, because every AQ1 centered subsequential state is `omega_inf`: the complete original-endpoint gauge-fixed space equals the invariant-local cyclic completion and reduces the physical generator; on it `H_phys ≥ (alpha/16)(I - P_Omega)` as a quadratic-form inequality, with a simple vacuum in this representation. The **full-GNS strengthening** (the same inequality on the whole GNS space of `omega_inf`) is inherited **only as the AQ2 gate qualifies it**: it explicitly uses AM2's separately reviewed full-Hilbert finite gap.

**Not inherited, not claimed.** Vacuum simplicity in this representation is not uniqueness of every infinite-volume state (the AQ2 gate's own limitation); nothing is said about states outside the named constructions, about GNS dynamics of different states, or uniformly in the lattice spacing `a`. The AQ2 Wilson-variance witness is a property of the same state as the AQ2 gate records it; it is not a BB2 item and is not re-derived here.

## 5. Item 4 — coarse translation invariance through the general-volume comparison

**Covariance (HNM-BB2-F05).** For a coarse `v` let `U_v` identify each factor space `H_b` with `H_{b+v}` through the fine translation `(4v_x,2v_y,v_z)`. Because the translation preserves residues and face classes, `U_v h_b U_v* = h_{b+v}` and `U_v W_f U_v* = W_{f+v}` with the same class; so `U_v H^{F}_V U_v* = H^{F}_{V+v}` for both prescriptions (checked on `Lambda_2` for two shifts: F1 stars and F2 owner-set-contained faces are translated exactly). The ground vector is simple (AM2 gate, every nonempty finite complete-factor volume), so `rho^{V+v}_{Y+v} = U_v rho^V_Y U_v*`, in each `Q_L` and untruncated.

**Theorem (HNM-BB2-F06), conditional_on_bb1_targets.** For every coarse `v`, each sign, `F` in `{F1,F2}` and `N ≥ |v|_inf + 2`:

\[
\|\rho^{\Lambda_N+v}_R-\rho^{\Lambda_N}_R\|_1\ \le\ C_h\,q^{\,N-|v|_\infty-1}.
\]

*Proof.* `Lambda_N` and `Lambda_N+v` are complete-factor volumes of one prescription that both contain `Lambda_{N-|v|_inf}` (and not `Lambda_{N-|v|_inf+1}`; enumerated for `N=2..5` and five shifts). Apply `H4`, R form, with `Lambda_{N-|v|_inf}`, whose size `N-|v|_inf ≥ 2 = N_min`. The constant is the hypothesis constant itself (factor 1). ∎

**Invariance.** (a) *From the R form:* with `u=-v`, `rho^{Lambda_N}_{R+u} = U_u rho^{Lambda_N-u}_R U_u*`, and F06 with F01 gives `||rho^{Lambda_N}_{R+u} - U_u rho^inf_R U_u*||_1 ≤ C_h q^(N-|u|_inf-1) + C' q^(N-1)`: the limit on every translate `R+u` exists and is the translate of `rho^inf_R`. (b) *From the region form of `H4`:* for every finite `Y` and `B` in `B(H_Y)`, `|omega^{Lambda_N}(tau_v B) - omega^{Lambda_N}(B)| = |omega^{Lambda_N}(tau_v B) - omega^{Lambda_N+v}(tau_v B)| ≤ c_h|Y|e^{|Y|/10^8} q^{N-|v|_inf-max_{y in Y+v}|y|_inf}||B||`, which tends to 0; with F02, `omega_inf(tau_v(B)) = omega_inf(B)`, where `tau_v(B) = U_v B U_v*`. So the limit of the named constructions is invariant under every coarse translation, on every finite region, hence on the quasi-local algebra.

**Separate item; non-coarse translations rejected.** Invariance is claimed only from the general-volume comparison: `Lambda_N+v` is not in the nested centered family, and nested cubes alone cannot give invariance (a covariant 1D domain-wall fixture has constant nested marginals and a translated marginal at trace distance 2 for every `N`). A fine translation that is not of the form `(4v_x,2v_y,v_z)` is not a symmetry: `(1,0,0)` maps the selected xy face at `r=2` to the omitted class `r=3` and splits one factor's links between two factors; `(0,1,0)` maps the selected `s=0` row to the omitted `s=1` row; `(2,0,0)` maps `r=1` to the omitted `r=3`. `check.py` enumerates roles, classes and owners on a fine window for five coarse and six non-coarse shifts (`fixture_translation_residues`).

## 6. Item 5 — correlation functions on the window `|theta| ≤ 8`

For `A` in `B(H_R)` set `c^{F,N}_A(theta) = omega^{F,N}(A* T^{F,N}_theta(A)) - |omega^{F,N}(A)|^2` and `c^inf_A(theta) = omega_inf(A* T_theta(A)) - |omega_inf(A)|^2` (complex means: the absolute square). `T_theta(A)` lies in the quasi-local algebra by Nachtergaele–Sims Theorem 4.1 (Part A, verbatim):

```text
(77) τ_t(A) = lim_{Λ→Γ} τ_t^Λ(A)
```

```text
exists and the convergence is uniform for t in compact sets. The limit may be taken along any increasing sequence of finite sets Λ which tend to Γ, and the result is independent of the particular sequence. This limiting dynamics τ_t(·) can be uniquely extended to a one-parameter group of *-automorphisms on A_Γ.
```

so `omega_inf(A* T_theta(A))` is defined through the extension of Section 2.

**Theorem (HNM-BB2-F07), conditional_on_bb1_targets.** For `F` in `{F1,F2}`, each sign, `N ≥ 5`, `r = r_N = floor((N-1)/2)` (frozen as written), `|theta| ≤ 8` and `A` in `B(H_R)`:

\[
|c^{F,N}_A(\theta)-c^{\infty}_A(\theta)|\ \le\ \|A\|^2\Big[\frac{C_{\rm dyn}}{r_N-1}+c'_{\rm site}\,|\Lambda_{r_N}|\,e^{|\Lambda_{r_N}|/10^8}q^{\,N-r_N}+2C'q^{\,N-1}\Big],
\]

with `C_dyn = 2K_F1 + K_cmp/4 = 78057/622883200000000` (preview `1.25315628997e-10`; for F1 alone `2K_F1 = 9261/77860400000000`, preview `1.18943647862e-10`), tier `polynomial_lieb_robinson`, route `duhamel_inner_f1`, both BA2 values read exactly from the gate; `C'` and `c'_site` are the item-1 constants.

*Proof.* `N ≥ 5` gives `r ≥ 2`, so `r-1 ≥ 1`, `R ⊂ Lambda_r ⊂ Lambda_N` and `d_{Lambda_r} = N-r ≥ 3`. The **local approximant** is `X_r = T^{F1,r}_theta(A)`, an element of `B(H_{Lambda_r})` (the F1 box Hamiltonian of `Lambda_r` acts on `H_{Lambda_r}`), with `||X_r|| = ||A||`. Then

\[
c^{F,N}_A-c^\infty_A=\underbrace{\omega^{F,N}\!\big(A^*[T^{F,N}_\theta(A)-X_r]\big)}_{(1)}+\underbrace{[\omega^{F,N}-\omega_\infty](A^*X_r)}_{(2)}+\underbrace{\omega_\infty\!\big(A^*[X_r-T_\theta(A)]\big)}_{(3)}-\underbrace{\big(|\omega^{F,N}(A)|^2-|\omega_\infty(A)|^2\big)}_{(4)} .
\]

- (1), F1: the BA2 Cauchy bound with smaller box `r ≥ 2` and `M = N` gives `||T^{F1,N}_theta(A) - T^{F1,r}_theta(A)|| ≤ K_F1/(r-1)||A||`. F2: add the BA2 comparison, `||T^{F2,N}_theta(A)-T^{F1,N}_theta(A)|| ≤ b(N)||A||`, and **Lemma (HNM-BB2-F08)**: for `N ≥ 5`, `(5N+1)(r_N-1) ≤ N^3/4`, so `b(N) ≤ (K_cmp/4)/(r_N-1)`. *Proof of F08:* `2(r_N-1) ≤ N-3`, and `N^3 - 2(5N+1)(N-3) = g(N) = N^3-10N^2+28N+6` has `g(5)=21` and `g'(N) = 3N^2-20N+28 ≥ 3` for `N ≥ 5`; also checked exactly for `N=5..3000`. ∎ So (1) is at most `K_F1/(r-1)` (F1) or `(K_F1 + K_cmp/4)/(r-1)` (F2), times `||A||^2`.
- (2): `A* X_r` lies in `B(H_{Lambda_r})`, so `|(2)| ≤ ||rho^{F,N}_{Lambda_r} - rho^inf_{Lambda_r}||_1 ||A||^2 ≤ c'_site |Lambda_r| e^{|Lambda_r|/10^8} q^(N-r) ||A||^2` (item 1, region form, `Y = Lambda_r`, with item 2 for the F2 limit). The state difference is taken on the region the approximant reaches, not only on `R`.
- (3): letting `M → infinity` in the BA2 Cauchy bound, `||T^{F1,r}_theta(A) - T_theta(A)|| ≤ K_F1/(r-1)||A||`.
- (4): `||a|^2-|b|^2| ≤ (|a|+|b|)|a-b| ≤ 2||A|| |a-b|` and `|a-b| ≤ ||rho^{F,N}_R - rho^inf_R||_1 ||A|| ≤ C' q^(N-1)||A||`. ∎

The three constants are kept separate and each is checked against its own target: `C_dyn ≤ 1/2000000000` (margin `3.98992`), `c'_site ≤ 1/200000`, `C' ≤ 1/100000`. There is no single bracket for the sum.

**Values of the bracket** (headline `C_dyn`, `||A|| = 1`, exact rationals in `results.json`):

| `N` | `r_N` | `|Lambda_r|` | dynamics `C_dyn/(r_N-1)` | region term | mean term `2C'q^(N-1)` | sum |
|---|---|---|---|---|---|---|
| 5 | 2 | 125 | `1.25315628997e-10` | `9.68813214984e-10` | `4.84406001984e-13` | `1.09461324998e-9` |
| 10 | 4 | 729 | `4.17718763325e-11` | `2.15536224241e-14` | `4.51138244927e-22` | `4.17934299553e-11` |

For F1 alone (`2K_F1`): `1.08824126884e-9` at `N=5` and `3.96694362435e-11` at `N=10`.

**Rate.** The rate in `N` is `O(1/N)`: `r_N - 1 ≥ (N-4)/2`, so the dynamics term is at most `2C_dyn/(N-4)`, while the state terms decay geometrically in `N` (the cube volume grows only like `N^3`); `N` times the bracket is at most `6x10^-9` for `N = 5..59`. The dynamics term is polynomial because the Lieb–Robinson function `F(r) = (1+r)^-4` is polynomial: Nachtergaele–Sims give an exponential form only under the condition quoted verbatim below, which the admitted constants do not use.

```text
If Φ ∈ B(Γ, F_a) with F_a(r) = e^{−ar}F(r) for some a > 0, then (53)
```

The BA2 constants rest on the bound

```text
(51) ‖[τ_t^Λ(A), B]‖ ≤ (2‖A‖‖B‖ / C) (e^{2‖Φ‖C|t|} − 1) D(X, Y)
```

with the AQ1 constants; they are named here, not re-derived.

**Meaning.** Item 5 is convergence of the correlation functions of the finite-box ground states to those of the one common limit state on the compact window, at a rate in `N`. It is not a statement outside `|theta| ≤ 8`: nothing is claimed uniformly in time. It is not equality of GNS dynamics of different states (a fixture with one automorphism group and two invariant states with correlations `(3+4i)/5` and `(3-4i)/5` is in `check.py`). The post-hoc optimum of `r` differs from `r_N` at every `N` from 10 to 15; the frozen `r_N` is used anyway.

## 7. Scaling `tau → tau/100`, each constant separately

| constant | ratio `C(10^-8)/C(10^-10)` | bracket (contract) | status |
|---|---|---|---|
| `C'` | exactly `1` | exactly 1 | in bracket |
| `c'_site` | exactly `1` | exactly 1 | in bracket |
| `C_dyn` | `1953058850/194651` (preview `10033.64406`) | `[9500,10500]` | in bracket |
| secondary `C'_2` | `(1-q_2/100)/(1-q_2)` `= 1085053/1083425` (preview `1.001502642`) | `[99/100,101/100]` | in bracket |
| secondary `c'_2` | same | `[99/100,101/100]` | in bracket |
| `q_2` | exactly `100` | exactly 100 | in bracket |

`C'` and `c'_site` are exactly `tau`-independent at the hypothesis values (the hypothesis constants and `1/(1-q)` at fixed `q`); the linear `tau`-scaling of the underlying BB1 constants is checked in BB1 and recorded at the BB2 gate with the discharge. `C_dyn(tau) = (2·592704 + 254016/4) tau^2/(1-338688|tau|) = 1248912 tau^2/(1-338688|tau|)` has the same structure as the BA2 constants, hence the BA2 gate's exact ratio. A linear-order ratio for `C_dyn`, a single lumped bracket for the item-5 sum, a `C'` scaled like a BB1 constant and a bracket chosen after evaluation are each rejected.

**Secondary pair (labelled, decides nothing).** `q_2 = 151552|tau| = 592/390625` at the cap; `C'_2 = C_2h/(1-q_2) = 625/12481056` (preview `5.00758910143e-5`) at most `1/8000` (margin `2.4962112`); `c'_2 = c_2h/(1-q_2) = 625/24962112` (preview `2.50379455071e-5`, no target).

## 8. Error ledger (preregistered terms)

| term | entry | note |
|---|---|---|
| `bb1_hypothesis_constants` | `C_h=1/250000`, `c_h=1/500000` at `q=1/64` | hypotheses, `conditional_on_bb1_targets`; not proved here |
| `cauchy_telescoping_or_union` | factor `1/(1-q) = 64/63` | full geometric tail; the slack `C' q^(M-1)` is kept, nothing is dropped |
| `identification_with_subsequential_limits` | `0` (not_applicable) | exact equality: the whole-sequence limit is the limit of every subsequence |
| `translation_general_volume` | `C_h q^(N-|v|_inf-1)`; region form `c_h|Y|e^{|Y|/10^8}q^(N-|v|_inf-max|y|_inf)` | `H4` with `Lambda_{N-|v|_inf}`, factor 1 |
| `dynamics_constant_from_ba2` | `C_dyn = 2K_F1 + K_cmp/4 = 78057/622883200000000` | BA2 gate values; Lemma F08 |
| `region_form_on_Lambda_rN` | `c'_site |Lambda_{r_N}| e^{|Lambda_{r_N}|/10^8} q^(N-r_N)`, `|Lambda_r| = (2r+1)^3` | directed `e^x ≤ 1/(1-x)` |
| `arithmetic` | `0` (not_applicable) | exact Fractions; the only transcendental factor is enclosed by `1/(1-x)` |

## 9. Fixtures (finite, `model_is_finite_graph: true`, `transfers_to_aq: false`)

- **Whole sequence versus subsequence.** `rho_N = diag(1/2+(-1)^N/100, 1/2-(-1)^N/100)`: every `rho_N` lies within `1/50` of `diag(1/2,1/2)` (a one-state ball in every box), yet there are two subsequential limits and `||rho_{N+1}-rho_N||_1 = 1/25` for every `N` — rejected as convergence. `a_N = sum_{k=2}^N 1/k` has steps `1/(N+1) → 0` and exceeds 4 at `N=119` — an `N` to `N+1` bound alone is rejected as a Cauchy estimate.
- **Translation residues.** Section 5: five coarse shifts pass role, class and owner checks on a fine window; six non-coarse shifts fail.
- **Correlation centering.** `rho = diag(1/2,1/2)`, `A = diag((3+4i)/5, 0)`: `omega(A) = (3+4i)/10`, `omega(A*A) = 1/2`; `omega(A*A) - |omega(A)|^2 = 1/4`, the variance; `omega(A*A) - omega(A)^2 = (57-24i)/100` is not real and is rejected. A post-hoc `r_N` and an exponential tail with the polynomial `F` are rejected (`r_N_prefrozen`, `lieb_robinson_polynomial_tail`).
- **Topology.** `U(t)e_j = e^{ijt}e_j`, `Ae_j = e_{2j}`: the difference `U(pi/n)AU(pi/n)* - A` has norm 2 on the moving vector `e_n` and at most `|t|` on the fixed `e_1`; `|e_n⟩⟨e_n|` tends to 0 against every finite-rank observable but keeps trace norm 1.
- **Named construction, not uniqueness.** `H = diag(0,0,1)`: the construction with boundary field `-|e_0⟩⟨e_0|/N` converges to `e_0` as a whole sequence while `e_1` is another ground vector of the limit operator.
- **Algebraic, not GNS dynamics.** One automorphism group, two invariant vector states, different correlations.
- **Cutoff order and Eckart.** The double sequence of Section 1; Eckart pairs `(16/25, 16/25)`, `(5/9, 2/3)`, `(0, 0)` on `diag(0,1/2,1)`.

## 10. Mandatory sentence and gate fields

**Mandatory sentence (the contract template, verbatim, once):**

For the zero-selected patterned family at the same coupling |tau|<=10^-8, under the BB1 locality bounds at their frozen targets as hypotheses (discharged only when the BB1 gate admits constants at most those targets), the reduced densities of the named construction families F1 and F2 on centered coarse cubes converge as whole sequences, at a rate in N, to one common limit on every finite region; this limit coincides with every AQ1 subsequential limit and every F2 subsequential limit, is invariant under coarse translations, and has as correlation functions on |theta|<=8 the limits of the finite-box correlation functions; this is convergence of the named constructions, not uniqueness of any ground state, not a statement about states outside the named constructions, and not a statement uniform in the lattice spacing a.

The constants in it: `q = 1/64`, `C' = 4/984375`, `c'_site = 2/984375` (at the hypothesis values), `C_dyn = 78057/622883200000000`; F1 = AQ1 centered whole-star boxes, F2 = I1 section 6 all-contained-face boxes with padding, on `Lambda_N=[-N,N]^3`, `N ≥ 2` (`N ≥ 5` for correlations); `R={0,e_z}`.

**Gate fields.** `results.json` exports exactly `gate_fields_required` as the **proposed** values (`whole_sequence_claimed`, `common_limit_claimed`, `state_convergence_claimed`, `translation_invariance_claimed`, `rate_in_N_claimed` true; `dynamics_level: correlation_functions_compact_window`; both scope strings; `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `continuum_claim`, `gns_dynamics_equality_claimed`, `uniform_in_time_claimed`, `weak_coupling_claim`, `scientific_priority_verified` false), together with `gate_fields_status` (conditional on the BB1 discharge, per `gate_fields_rule`) and `gate_fields_if_undischarged`, in which every field that depends on a BB1 hypothesis is false and `dynamics_level` is not set. A limited outcome exports `translation_invariance_claimed` false if `H4` is not admitted, and does not set `dynamics_level` if the region form is not admitted.

## 11. Controls

Every one of the 34 contract controls is a check in `check.py` with at least one damaging mutation that must raise `AdmissionError`.

| control | damaging mutations rejected |
|---|---|
| `coherent_evidence_tampering` | control Boolean flipped, BB1 contract snapshot removed, `C'` replaced by `C_h`, `C_dyn` replaced, condition dropped, uniqueness field, hypothesis `H4` dropped, assembly relabelled — each with the packet hash rebound |
| `exact_arithmetic_admission` | float, bool, `nan`, zero denominator, preview decimal read as a value, exp enclosure outside its radius |
| `no_priority_or_continuum_claim` | continuum, priority, weak coupling, rate in `a` set true |
| `changed_model_relabelled` | `tau`, triple, state metric, route-B model, SU(3), finite graph |
| `insufficient_verdict_retained` | missed item relabelled accepted, open Cauchy estimate relabelled limited, producer-declared discharge, retuned hypothesis |
| `tau_scaling_exponent` | linear `C_dyn`, lumped item-5 bracket, `C'` scaled like a BB1 constant, bracket chosen after evaluation |
| `wrong_delta_alpha_hbar_clock` | `u` labelled `theta`, `hbar` dropped, `delta = alpha` |
| `root_n_misuse` | division by an integer square root of the step count, largest step only |
| `tier_mixing_rejected` | state constant with a Lieb–Robinson tier, dynamics constant with a state tier, BB1 route claimed by this producer, lumped item-5 bracket, missing route |
| `reverse_premise_isolation` | BB1 producer, BB1 gate, BB1 skeptic, forward BB2, lens memo, other skeptic file in the reverse inventory |
| `uniform_in_N_not_in_a` | "uniform in the lattice spacing a", an unqualified "uniform" |
| `placeholder_span_rejected` | whitespace, vertical-bar and `e.g.` placeholders |
| `negation_aware_phrase_scan` | affirmative forbidden phrasings (three) |
| `parameters_declare_metric_weights_window` | window or metric field absent |
| `rate_constant_pair_prefrozen` | `q` retuned, target moved, smaller hypothesis value |
| `decay_rate_in_N_not_a` | conversion to fm, rate in `a` |
| `topology_named` | weak-* relabelled trace norm, norm continuity in time claimed |
| `two_families_named` | one family, literal vertex boxes, orthant boxes |
| `subsequence_versus_whole_sequence` | whole sequence from compactness, unlabelled limit |
| `common_clock` | F2 at the opposite sign, limit in another clock |
| `named_construction_not_uniqueness` | uniqueness claimed, object widened |
| `cauchy_estimate_not_compactness` | compactness plus closeness, compactness plus first-order agreement |
| `limit_identified_with_aq1_limits` | inheritance first, no extension to the quasi-local algebra |
| `translation_invariance_separate_item` | invariance from nested cubes, domain wall passing the general-volume comparison |
| `region_constant_scales_with_Y` | `R` constant reused on `Lambda_2`, size factor dropped |
| `cutoff_uniform_then_removed` | `N` limit taken in `Q_L` first, constant depending on `L` |
| `algebraic_not_gns_dynamics` | GNS equality, GNS-level label, uniform in time |
| `lieb_robinson_polynomial_tail` | exponential tail with the polynomial `F`, exponential decay in `r_N` |
| `time_window_named_common_clock` | uniform in time, `u` window labelled `theta` |
| `fixture_whole_sequence_vs_subsequence` | one-state ball read as convergence, `N` to `N+1` bound as Cauchy |
| `fixture_translation_residues` | fine shifts `(1,0,0)`, `(0,1,0)`, `(2,0,0)` accepted as symmetries |
| `fixture_correlation_centering` | centering with `omega(A)^2`, uncentred correlation |
| `conditional_on_bb1_targets` | a BB1 value other than the frozen target, condition dropped, unconditional before the discharge, a constant decreasing in `C_h` |
| `r_N_prefrozen` | post-hoc optimized `r_N`, `r_N = floor(N/2)` |

Further checks (not contract controls): both contract digests; pinned gates and the source excerpt; the BA2 constants read from the gate; the premise statements; the BB1 hypotheses; the verbatim quotations (a paraphrase is rejected); items 1–5; the secondary pair; the error ledger; the gate fields; the mandatory sentence.

## 12. The BB1 hypotheses each item uses (for the discharge at the BB2 gate)

Every hypothesis is used at **both signs**, in **each on-site cutoff space `Q_L` with the same constant for every `L`**, and at **fixed `N` for the untruncated ground vectors** (reached from the `Q_L` form by Lemma C; the untruncated form is the same statement after `L → infinity`). Constants: `C_h = 1/250000` (R form), `c_h = 1/500000` (region form), `q = 1/64`. The machine-readable list is `hypotheses_used` in `results.json`.

| item | comparisons | forms | if the BB1 gate does not admit it |
|---|---|---|---|
| 1 on `R` | `H1` (F1 `Lambda_N` vs `Lambda_{N+1}`), `H2` (F2) | R | item 1 on `R` stays conditional |
| 1 on `Y` | `H1`, `H2` | region | region parts of items 1–3 and item 5 dropped (limited) |
| 2 | `H1`, `H2`, `H3` (F1 vs F2, same `Lambda_N`) | region (R for the `R` part) | common limit on `R` only with the R form |
| 3 | `H1`, `H2`, `H3` | region (R for `R`-marginals) | identification of `R`-marginals only |
| 4 | `H4` (two volumes of one prescription containing `Lambda_N`) with `H1`/`H2` for the limit | R (quantitative bound, translates of `R`); region (every finite region) | item 4 dropped and recorded |
| 5 | `H1`, `H2` (F2), `H3` (F2 limit) | region on `Lambda_{r_N}`, R on `R` | item 5 dropped |

Not used: BB1's direct comparison of any two centered boxes (used directly it would give the labelled value `C' = C_h`). The secondary pair enters only the labelled secondary constants.

## 13. Contract wording findings (non-blocking)

- **W1 (`C_dyn`).** The BA2 gate has no single constant named `C_dyn`; a correlation bound needs two dynamics approximations to one local approximant (the finite-box evolution and the limit dynamics). `C_dyn` is therefore the explicit combination `2K_F1 + K_cmp/4` of gate values (F1 needs only `2K_F1`), with the lemma F08; both BA2 values are read exactly.
- **W2 (the BA2 limit bound).** The gate writes the F2-to-limit bound with `min(K_F1, second-route K_F2)`, mixing routes; this producer uses only `K_F1` (route `duhamel_inner_f1`).
- **W3 (item 4 and the region form).** With the R form alone, `omega_inf` is defined on `B(H_R)` only and invariance holds for translates of `R`; invariance on every finite region needs the region form of `H4`. The contract's limited clause names only the general-volume comparison.
- **W4 (BA1 gate).** The BA1 `accepted` text lists the one-prescription general volumes; its `decision` text lists only centered boxes. `H4` names the `accepted` statement as its coefficient input.
- **W5 (gate fields at producer time).** `gate_fields_required` lists the values after the discharge; the producer exports them as proposed values with `gate_fields_if_undischarged`, per `gate_fields_rule`.
- **W6 (scaling brackets).** "Exactly 1" for `C'` and `c'_site` holds by construction and has no discriminating power in this loop; the `tau` content sits in BB1.
- **W7 (naive placeholder regex).** The contract text itself contains a less-than-or-equal sign and an arrow in one string, which a naive span regex would flag; `check.py` scans the report and the exported statements with the template removed.

## 14. Exclusions and limitations

- Only the zero-selected patterned family, fixed spacing, `|tau|` at most `10^-8`, each sign separately, the two named families on centered cubes and, for item 4, their coarse translates; nothing transfers to literal vertex boxes, periodic or orthant boxes, nonzero selected triples, the uniform route-B model, weak coupling or the continuum.
- **Conditional throughout:** every BB2 state statement rests on the BB1 frozen targets as hypotheses (`conditional_on_bb1_targets`); no BB1 value other than those targets is used.
- Not uniqueness of every infinite-volume ground state; nothing about states outside the named constructions; not equality of GNS dynamics of different states; nothing uniformly in time; no estimate uniform in the lattice spacing `a`; no continuum or weak-coupling statement; scientific priority is unverified.
- Rates are per coarse step at fixed spacing: geometric `q = 1/64` per coarse l-infinity step for states, `O(1/N)` for correlations with the polynomial `F`.
- Inherited without re-proof: the BA2 constants and Nachtergaele–Sims Theorems 3.1 and 4.1; AQ1's construction and properties; AQ2's gap statement with its qualification; AV1 F20–F23 and AY1's F2 itemization; AM2's simple ground in finite complete-factor volumes; the I1 dictionary.
- Upper bounds only; the `-tau` evaluation of `C_dyn` replays the same `|tau|` formula and the state constants are `tau`-independent.
- **Methodological lenses (modern use of the snapshotted skills).** *Newton, analysis before synthesis:* the limit is identified with the AQ1 limits before any property is carried over, and every limit order is stated. *Tesla, complete accounting:* every term of the item-5 difference is placed, the state difference is charged on the region the dynamics reaches, and each constant is checked alone. No historical figure endorses anything here, and no historical or occult material supplies a premise.

## 15. Map of contract items to sections and checks

| contract item | section | checks |
|---|---|---|
| 1 whole-sequence Cauchy, limit without compactness | 2 | `item1_whole_sequence_cauchy_R`, `item1_whole_sequence_cauchy_regions`, `item1_limit_exists_without_compactness`, `cutoff_uniform_then_removed` |
| 2 common limit | 3 | `item2_common_limit` |
| 3 identification and inheritance | 4 | `item3_identification_and_inheritance`, `limit_identified_with_aq1_limits` |
| 4 coarse translations | 5 | `item4_coarse_translation_invariance`, `translation_invariance_separate_item`, `fixture_translation_residues` |
| 5 correlations | 6 | `item5_correlation_bound`, `item5_rate_and_sums`, `r_N_prefrozen`, `fixture_correlation_centering`, `lieb_robinson_polynomial_tail` |
| 6 fixtures, template, gate fields, scaling, controls | 7, 9–11 | `tau_scaling_exponent`, `mandatory_sentence_verbatim_once`, `gate_fields_exported`, every control |

## 16. Reproduction

```bash
python3 -B research/round33/forward/bb2/check.py --output /absolute/fresh/directory
python3 -B -O research/round33/forward/bb2/check.py --output /another/absolute/fresh/directory
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/bb2.json research/round33/forward/bb2/report.md
```

The two outputs are byte-identical and equal to `output/`.
