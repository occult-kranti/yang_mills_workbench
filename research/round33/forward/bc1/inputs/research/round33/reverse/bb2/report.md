# Hruday whole-sequence convergence of the named constructions, their common limit and its coarse translation invariance — BB2 reverse (union comparison)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted reverse production: the derivations, `check.py` and this report were written by a Claude model agent (an AI model) acting as the BB2 reverse producer under the frozen BB2 contract (`research/round33/contracts/bb2.json`, sha256 `ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35`) and with the frozen BB1 contract as the source of the hypotheses (`research/round33/contracts/bb1.json`, sha256 `30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018`). `check.py` verifies both hashes before any evaluation. This is correlated model-agent work, not independent human review and not formal verification. HNM labels are project aliases; the contribution alias of this packet is **HNM-BB2-R**.

**What this producer read.**
- **Scientific material: only `inputs/`** (38 files: `AGENTS.md`, the BB2 contract and its 36 shared premises), read in this order: the BB2 contract in full; the BB1 contract in full; `AGENTS.md`; `selection-bb2.md`; the BA2 gate in full (constants, statements (1)–(5), limitations, gate fields); the BA1 gate (`accepted`, `limitations`, `decision`, gate fields); the AQ1 and AQ2 gates and forward reports in full; the AV1 gate and the AV1 forward report section 7 (F20–F23); the AY1 and AY2 gates (`accepted`, `limitations`, gate fields); the AM2 and AW1 gates (`accepted`, `limitations`); the Nachtergaele–Sims excerpt in full; the I1 forward report in full; the BA2 forward report in full; the BA2 reverse report (header, items 3–4 and the constant lines, found by keyword search for `345744`, `1016064`, `E_up`); the BA1 reverse report (Theorem 4.1 and sections 4.2–4.5); the BA2 skeptic review (first 80 lines: headline table and binding choice); the AY1 forward report (keyword search for compactness, diagonal and padding, including the section 3.4 paragraph); the Round32 lessons reference in full; the paired-physics SKILL and its complete-residual reference; the Newton and Tesla SKILL files (first 40 and 30 lines). Not opened: the AM2 forward and reverse reports, `skeptic/am2.md`, the AV1 reverse report, the AY1 reverse report, the AY2 forward report, the AW1 forward report, the BA1 forward report, `skeptic/ba1.md`, the historical-panel SKILL (their gates or snapshots are bound by hash only).
- **Outside `inputs/`, for protocol and code style only:** `research/round33/tools/README.md`, `research/round33/tools/freeze.py`, `research/round33/tools/phrase_scan.py` (its round phrase list is copied into `check.py` as infrastructure), and `research/round33/reverse/ba2/check.py` (conventions only; BA2 is gated). None of these carries premise weight.
- **Not read:** anything under `research/round33/forward/bb2/`, `research/round33/forward/bb1/`, `research/round33/reverse/bb1/`, `research/round33/skeptic/` (other than the two snapshotted reviews in `inputs/`), `research/round33/experts/`, `research/round33/advisor/` (other than the snapshotted gates and `selection-bb2.md`); no BB1 producer, skeptic or gate file; no deliberation, plan, panel, triage or lens file.
- **Scratchpad disclosure.** My private scratch folder is `/tmp/claude-0/bb2-reverse-private/`: two float prototypes (`proto.py`, `proto2.py`, which located the item-5 threshold near N=14411), a value script (`bb2_values.py`, which imports this `check.py` to print exact values), and the development and production runs. **Nothing in it is evidence.** I created it with `mkdir -p` and did not list the shared scratchpad root `/tmp/claude-0/`; I opened no other agent's scratch folder. File-name exposure: after the first freeze, a `git status` run to confirm that nothing outside this directory changed listed two untracked file names of other agents (`research/round33/forward/bb1/check.py`, `research/round33/skeptic/bb1_check.py`); I opened neither, and every result here was fixed before that listing (this sentence is the only change made after it).

**Attribution.** The limit dynamics is Nachtergaele–Sims arXiv:1410.8174v1 Theorem 4.1 (quoted verbatim in section 1.4, admitted for both families in the BA2 gate); the GNS, stationarity and Fourier strategy inherited in item 3 is AQ1/AQ2's, credited there to Gauvin arXiv:2503.15539v3 Supplement A.10; completeness of the trace class and trace-norm contractivity of the partial trace are standard. The union comparison is named in the contract as the reverse assembly. Scientific priority is unverified.

## Verdict (reverse route)

Model: **`AQ_patterned_zero_selected`** (SU(2) Kogut–Susskind form on `Z^3` at fixed spacing, coarse 24-link factors, selected triple `(0,0,0)`, 21 omitted faces per anchor as `-(tau/3)W_f` in normalized units `delta=alpha/8`), both signs `|tau|<=10^-8`, the two named construction families **F1** (AQ1 centered whole-star boxes) and **F2** (I1 section 6 all-contained-face boxes with padding) on centered coarse cubes `Lambda_N=[-N,N]^3`, `N` at least 2. Assembly: **`union_comparison`**. Every statement below that uses BB1 is **`conditional_on_bb1_targets`**: it is derived from the BB1 frozen targets as explicit hypotheses, and it becomes unconditional only when the BB1 gate admits, for every comparison, form, cutoff regime and sign that it uses, constants at most those targets.

1. **Item 1 (section 4).** For `F` in {F1, F2}, `N>=2`, in each on-site cutoff space uniformly in `L` and, at fixed `N`, for the untruncated ground vectors:
   `sup_{M>N} ||rho^{F,M}_R-rho^{F,N}_R||_1 <= C' q^(N-1)` and `sup_{M>N} ||rho^{F,M}_Y-rho^{F,N}_Y||_1 <= c'_site |Y| e^{|Y|/10^8} q^{d_Y}` (`Y` inside `Lambda_N`, `d_Y=N-max_Y|y|_inf`), with
   **`C'(C_h,c_h) = C_h`** and **`c'_site(C_h,c_h) = c_h`** (assembly factor 1: the union of two nested centered cubes is the larger cube), evaluated at the hypothesis values: **`C' = 1/250000`** (target `1/100000`, margin `5/2`) and **`c'_site = 1/500000`** (target `1/200000`, margin `5/2`). Tier `exact_first_order`, assembly `union_comparison`, hypothesis source `bb1_frozen_targets`; the BB1 route is attached at the BB2 gate. The limit on every finite region exists by completeness of the trace class, **without compactness**.
2. **Item 2 (section 5).** The F1 and F2 limits coincide on every finite region: one limit of the named constructions, `omega_inf`.
3. **Item 3 (section 6).** `omega_inf` equals every AQ1 subsequential limit and every F2 subsequential limit; only then does it inherit, in its own GNS representation, exactly the AQ1/AQ2/BA2 admitted properties (stationarity under `T_theta`, GNS strong continuity, nonnegative generator, `H_phys>=(alpha/16)(I-P_Omega)` with a simple vacuum on the invariant-local cyclic completion, the full-GNS strengthening only as qualified in the AQ2 gate).
4. **Item 4 (section 7).** For every coarse translation `v` (fine `(4v_x,2v_y,v_z)`) the limit is invariant, and `||rho^{Lambda_N+v}_R-rho^{Lambda_N}_R||_1 <= C_h q^(N-|v|_inf-1)` for `N>=|v|_inf+2` (B5 direct); non-coarse fine translations are rejected (they break residues and face classes).
5. **Item 5 (section 8).** For `N>=5`, `r_N=floor((N-1)/2)`, `|theta|<=8`, `A` in `B(H_R)`: `|c^{F,N}_A(theta)-c^inf_A(theta)| <= ||A||^2 [C_dyn/(r_N-1) + c'_site |Lambda_{r_N}| e^{|Lambda_{r_N}|/10^8} q^(N-r_N) + 2C' q^(N-1)]`, complex-mean centering, three separate constants; **`C_dyn[F1] = 9261/77860400000000`** (about `1.18943647862e-10`, route `duhamel_inner_f1`, margin `4.2037`) and **`C_dyn[F2] = 1055961408185869563/15240701171875000000000000000`** (about `6.92856185734e-11`, route `duhamel_inner_f2`, margin `7.2165`), tier `polynomial_lieb_robinson`, each twice an exact BA2 gate value; target `1/2000000000`. The bracket is O(1/N) on the certified range `5<=N<=14000` and is vacuous from `N=14421` on (a property of the frozen forms, section 8.5); the whole sequence of correlation functions converges for every `N` (no rate beyond the certified range).
6. **Scaling and controls (sections 9–10, 16).** `C'` and `c'_site` ratios exactly 1; `C_dyn` ratios `1953058850/194651` (F1) and about `10019.588` (F2), inside `[9500,10500]`; secondary ratios exactly 1, `q_2` ratio exactly 100.

**Checker.** `check.py` runs **59 exact checks**; all **34 contract controls** reject explicit damaging mutations, **162** rejections in total; the `-B` and `-B -O` outputs are byte-identical.

**Proposed reverse verdict: `accepted_within_scope`, conditional_on_bb1_targets** (for the reverse half only). If the BB1 gate discharges every hypothesis listed in section 2.3, the verdict stands as accepted within scope; if it does not admit the direct non-nested general-volume comparison (B5 for non-nested pairs), item 4's contract constant is dropped (limited; the union fallback `2C_h` then needs B5 for nested pairs); if it does not admit the region form, item 5 and the region parts of items 1–3 are dropped (limited); if BB1 is insufficient, the BB2 implications stay conditional statements (insufficient). The acceptance also requires the forward route and the skeptical review.

## 1. Model, families, notation, clock, window, metrics and topologies

**1.1 Model and families** (contract `model`). In normalized units `delta=alpha/8` (I1.3, I1.5): `h_b` is the unbounded self-adjoint on-site operator with compact resolvent and simple vacuum; `phi_b=-(tau/3) sum_{f in O_b} W_f`, `||phi_b||=7|tau|`; a face `f` has owner set `M_f` (I1.4), `|M_f|` 2 or 3, `M_f` inside `b+S`, `S={0,e_x,e_y,e_z}`. For a finite complete-factor volume `V` (a finite set of coarse sites):

\[
 \widehat H^{F1}_V=\sum_{b\in V}h_b+\sum_{b:\,b+S\subset V}\phi_b,\qquad
 \widehat H^{F2}_V=\sum_{x\in V+S}h_x+\sum_{f:\,M_f\subset V}\Big(-\frac{\tau}{3}\Big)W_f .
 \tag{HNM-BB2-R00}
\]

F1 on `Lambda_N` is the AQ1 centered whole-star box; F2 on `Lambda_N` is the I1 section 6 box with padding `Lambda_N+S`. Each has a simple ground vector `psi^{P,V}` (AM2 gate: every nonempty finite I1 complete-factor volume; F2 through the AY1 itemization). `rho^{P,V}_Y` is its reduced density on a finite region `Y` inside `V`; `rho^{F,N}_Y:=rho^{F,Lambda_N}_Y`. In the on-site cutoff space `Q_L` the cutoff ground vector is `psi^{P,V,L}`.

**1.2 Notation.** `q=1/64`; `m(Y)=max_{y in Y}|y|_inf`; `d_Y(n)=n-m(Y)`; `|Y|` is the number of coarse sites; `g(Y)=|Y| e^{|Y|/10^8}`. The cover `R={0,e_z}` (48 links, 36 endpoints) has `m(R)=1`, `d_R(n)=n-1`, `|R|=2`.

**1.3 Clock, window, metrics, topologies.** Common clock `theta=alpha t/hbar` for both families and every comparison; internally `u=theta/8` (`delta=alpha/8`), so the window `|theta|<=8` is `|u|<=1`, `U=1`. States: coarse l-infinity metric on factor sites (star diameter 1), **trace norm on `B(H_Y)`** for every finite region `Y`. Dynamics: `l1` on the coarse factor lattice with `F(r)=(1+r)^-4`, **operator norm uniformly for `|theta|<=8`**. Representations: **strong continuity of the GNS unitary group** only (the fixed-vector versus moving-vector fixture of section 10 shows that norm continuity in `theta` fails on moving vectors).

**1.4 The finite-box and limit dynamics, verbatim** (Part A of `research/round33/sources/nachtergaele-sims-1410.8174v1.md`, sha256 `6a28f4cd6aa2c55286fa839d83c00356ff0709f8b02027ee5b39050df1d6c921`, PDF sha256 `501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba`; copied byte for byte, the section title of Theorem 4.1 omitted):

```text
(44) H_Λ = Σ_{x∈Λ} H_x + Σ_{X⊂Λ} Φ(X),
essentially self-adjoint on the dense domain (45) D_Λ = span{⊗_{x∈Λ} ψ_x | ψ_x ∈ D_x}; (46) τ_t^Λ(A) = e^{itH_Λ} A e^{−itH_Λ} for A ∈ A_Λ.
Let Γ and F be as described in Section 3. Fix a collection of on-site Hamiltonians {H_x}_{x∈Γ} and an interaction Φ ∈ B_F(Γ). For each t ∈ ℝ and A ∈ A_Γ^loc, the norm limit
(77) τ_t(A) = lim_{Λ→Γ} τ_t^Λ(A)
exists and the convergence is uniform for t in compact sets. The limit may be taken along any increasing sequence of finite sets Λ which tend to Γ, and the result is independent of the particular sequence. This limiting dynamics τ_t(·) can be uniquely extended to a one-parameter group of *-automorphisms on A_Γ.
```

`T^{F,N}_theta` is (46) for the native restriction (44) of the family's interaction (whole-star `Phi` for F1, owner-set `Phi'` for F2 with the padding factored out, BA2 gate statement (1)); `NS t` is `u=theta/8`. `T_theta` is the (77) limit for F1 (AQ1), and the BA2 gate admits that the F2 limit dynamics equals it. No new Lieb–Robinson estimate is made in this packet; every dynamics number is an exact BA2 gate value.

## 2. The hypotheses: BB1 frozen targets (conditional_on_bb1_targets)

**2.1 Statement.** The BB1 contract lists five comparisons (quoted in `results.json`):
- **B1** F1 on `Lambda_N` versus F1 on `Lambda_{N+1}`;
- **B2** F2 on `Lambda_N` versus F2 on `Lambda_{N+1}`;
- **B3** F1 versus F2 on the same `Lambda_N`;
- **B4** any two centered boxes `Lambda_M`, `Lambda_M'` with `M, M'` at least `N`, of F1 or F2, compared directly;
- **B5** two finite complete-factor volumes of one prescription both containing `Lambda_N`, compared directly (its coefficient input is the BA1 accepted comparison of any two such volumes).

**Hypothesis (H)**, read from the BB2 contract (twice: `rate_constant_pair.hypotheses` and `conditional_on_bb1_targets`) and cross-checked exactly against the BB1 contract targets: for every comparison, both signs, in each on-site cutoff space and at fixed `N` for the untruncated ground vectors, with `n` the smaller box size (the largest centered cube in both volumes),

\[
 \|\rho^{1}_R-\rho^{2}_R\|_1\le C_h\,q^{\,n-1},\qquad
 \|\rho^{1}_Y-\rho^{2}_Y\|_1\le c_h\,|Y|\,e^{|Y|/10^8}\,q^{\,d_Y(n)}\quad(Y\subset\Lambda_n),
 \tag{H}
\]

`q=1/64`, `C_h=1/250000`, `c_h=1/500000`; secondary (labelled): `q_2=151552|tau|` (`592/390625` at the cap), `C_2h=1/20000`, `c_2h=1/40000`. `check.py` rejects any other BB1 value, a dropped condition, a producer-recorded discharge and any "unconditional" label.

**2.2 What the reverse uses.** The reverse never sums nearest-neighbour steps: B1 and B2 are **not used** (they are the forward's nested telescoping). The union comparison needs only nested one-prescription comparisons; the contract constant of item 4 needs the direct non-nested B5.

**2.3 BB1 hypotheses used, item by item** (comparison, form, cutoff regime, sign):

| item | comparison | form | cutoff regime | sign |
|---|---|---|---|---|
| 1 | B4 restricted to same-family nested pairs `Lambda_N` inside `Lambda_M`, `M>N` (equivalently B5 for nested one-prescription pairs) | R (`C_h`) and region (`c_h`) | each `Q_L` uniformly in `L`; untruncated at fixed `N` | `+tau` and `-tau`, each separately |
| 2 | B3 (F1 versus F2 on the same `Lambda_N`), plus item 1 | R and region | untruncated at fixed `N` (each `Q_L` for the cutoff-space version) | both |
| 3 | through items 1–2 | R form for R-marginals; region form for every finite region | untruncated at fixed `N` | both |
| 4 | B5 for the non-nested pair `(Lambda_N+v, Lambda_N)`, both containing `Lambda_{N-|v|_inf}`; labelled fallback: B5 for nested pairs through the union (factor 2) | R for the quantitative bound; region for invariance on every finite region | untruncated at fixed `N` (and each `Q_L`) | both |
| 5 | through item 1 | R form (`C'`) and region form at `Y=Lambda_{r_N}` (`c'_site`) | untruncated at fixed `N` | both |
| secondary | as items 1–2 | R (`C_2h`), region (`c_2h`) | as items 1–2 | both; labelled only |

Item 5 also uses the **admitted** BA2 gate constants and the identification of the F2 limit dynamics; these are not hypotheses. No item uses a BB1 route label: the BB1 route of each discharging constant (`polymer_kp` or `iterated_split`) is attached at the BB2 gate.

## 3. The union comparison (assembly) and the BB2 state constants

**Lemma 3.1 (union comparison).** Let `V1`, `V2` be finite complete-factor volumes of one prescription `P` in {F1, F2}, both containing `Lambda_n`, `n>=2`, and `U=V1 ∪ V2`. Then `U` contains `Lambda_n`, and for `Y` inside `Lambda_n`

\[
 \|\rho^{P,V_1}_Y-\rho^{P,V_2}_Y\|_1\le\big([V_1\ne U]+[V_2\ne U]\big)\,\mathcal H_Y(n),
 \tag{HNM-BB2-R01}
\]

where `H_Y(n)` is the right side of (H) (`C_h q^{n-1}` for `Y=R`, `c_h g(Y) q^{d_Y(n)}` otherwise).

*Proof.* Triangle inequality through `rho^{P,U}_Y`. Each leg `(V_i,U)` is a nested pair of one prescription (`V_i` inside `U`) whose volumes both contain `Lambda_n`, so (H) applies to it (B5 for nested pairs; B4 when both are centered cubes). A leg with `V_i=U` vanishes. ∎

The **assembly factor** `a(V1,V2)=[V1≠U]+[V2≠U]` is 1 for a nested pair of distinct volumes (the union is the larger volume) and 2 for a non-nested pair. `check.py` enumerates it: `a=1` for `(Lambda_2,Lambda_3)`, `(Lambda_2,Lambda_5)`, `(Lambda_3,Lambda_4)`, `(Lambda_3,Lambda_6)`; `a=2` for `(Lambda_N, Lambda_N+v)` with `(N,v)` = `(3,(1,0,0))`, `(3,(0,1,1))`, `(4,(2,-1,0))`, `(4,(1,1,1))`, which are not nested, whose union is not a centered cube, and which both contain `Lambda_{N-|v|_inf}`. If B5 is admitted for arbitrary pairs, the direct comparison gives factor 1 for every pair; the union route needs only its nested sub-case.

**Definition 3.2 (BB2 state constants).** For the whole-sequence estimate the pairs are nested centered cubes, so `a=1`:

\[
 C'(C_h,c_h)=1\cdot C_h,\qquad c'_{\rm site}(C_h,c_h)=1\cdot c_h .
 \tag{HNM-BB2-R02}
\]

Both are nondecreasing in each hypothesis constant (linear with coefficients 1 and 0; `check.py` checks it exactly at three points and three increments per constant and rejects a decreasing function). At the hypothesis values: **`C' = 1/250000`** `<= 1/100000` (margin `5/2`) and **`c'_site = 1/500000`** `<= 1/200000` (margin `5/2`). Each carries tier `exact_first_order`, assembly `union_comparison`, hypothesis source `bb1_frozen_targets`, and no route label (the BB1 route is attached at the gate). Secondary (labelled): `C'_2 = 1/20000` `<= 1/8000` (margin `5/2`), `c'_2 = 1/40000`.

## 4. Item 1: whole-sequence Cauchy estimates, the limit without compactness, and the cutoff order

**Theorem 4.1 (conditional_on_bb1_targets).** For `F` in {F1, F2}, `N>=2`, both signs, in each on-site cutoff space `Q_L` with constants independent of `L`, and at fixed `N` for the untruncated ground vectors:

\[
 \sup_{M>N}\|\rho^{F,M}_R-\rho^{F,N}_R\|_1\le C'\,q^{\,N-1},\qquad
 \sup_{M>N}\|\rho^{F,M}_Y-\rho^{F,N}_Y\|_1\le c'_{\rm site}\,|Y|\,e^{|Y|/10^8}\,q^{\,d_Y(N)}\quad(Y\subset\Lambda_N).
 \tag{HNM-BB2-R03}
\]

*Proof.* Fix `M>N`. `V1=Lambda_N` and `V2=Lambda_M` carry the same prescription, `V1` is inside `V2`, and `Lambda_N` is the largest centered cube in both, so `n=N`. Lemma 3.1 with `U=Lambda_M` and `a=1` gives each bound. The right side does not depend on `M`, so it bounds the supremum. Every `M` is compared **directly** with `N`; no sum of step bounds is formed. ∎

The bound is a statement for all `M>N` at once. A bound for `N` to `N+1` alone is not a Cauchy estimate (the harmonic fixture of section 10 has steps `1/(n+1)` and no Cauchy property). Region bounds carry `|Y| e^{|Y|/10^8}` and the exponent `d_Y(N)=N-m(Y)`; the R constant is never reused on `Y`. Example rows (exact in `results.json`): `C' q^(N-1)` is `1/16000000` at `N=2` and `1/1024000000` at `N=3`; for `Y=Lambda_1` (27 sites, `m=1`) the region bound at `N=2` is about `8.4375e-7`.

**Corollary 4.2 (existence of the limit on every finite region, without compactness).** Fix `F` and a finite region `Y`; put `N_Y=max(2,m(Y))`. For `M>N>=N_Y`, (R03) gives `||rho^{F,M}_Y-rho^{F,N}_Y||_1 <= c'_site g(Y) q^{N-m(Y)}`, which tends to 0 as `N` grows. The trace class `T(H_Y)` with the trace norm is a Banach space, so

\[
 \rho^{F,\infty}_Y:=\lim_{N\to\infty}\rho^{F,N}_Y\quad\text{exists in trace norm (whole sequence).}
 \tag{HNM-BB2-R04}
\]

It is positive (the positive cone is trace-norm closed) with trace one (the trace is 1-Lipschitz). For `Y` inside `Y'`, `Tr_{Y' minus Y} rho^{F,N}_{Y'}=rho^{F,N}_Y` for every `N`, and the partial trace is trace-norm contractive (`||Tr_2 X||_1<=||X||_1`, audited exactly on diagonal two-qubit pairs), so the limits are compatible. Hence `omega^F_inf(A)=Tr(rho^{F,inf}_Y A)`, `A` in `B(H_Y)`, is a well-defined locally normal state on the local algebra; it is bounded by `||A||` and extends to the quasi-local algebra. The closed trace-norm balls give the rates

\[
 \|\rho^{F,\infty}_R-\rho^{F,N}_R\|_1\le C'q^{\,N-1},\qquad \|\rho^{F,\infty}_Y-\rho^{F,N}_Y\|_1\le c'_{\rm site}\,g(Y)\,q^{\,d_Y(N)},
 \tag{HNM-BB2-R05}
\]

and `omega^{F,N}` converges to `omega^F_inf` on every quasi-local observable (local convergence, uniform bound `||A||`, norm density). No compactness, subsequence or diagonal extraction is used; a compactness-plus-closeness argument is not a whole-sequence argument (section 10, fixture (a)). The rate is `q^(N-1)` per coarse step at fixed spacing (a coarse step is `(4a,2a,a)`), in N at fixed spacing, never a rate in the lattice spacing.

**Proposition 4.3 (cutoff: uniform in L, then removed at fixed N; limits never exchanged).**
1. In each `Q_L` the hypotheses hold with `L`-independent constants, so (R03) holds for the cutoff ground vectors uniformly in `L`.
2. At fixed `N` and `M`: AV1 (F21) gives `E_{0,L} -> E_0`, and (F22), with the **untruncated gap 1/2**, gives `1-|<psi,psi_L>|^2 <= 2(E_{0,L}-E_0) -> 0` (Eckart-type vector bound; F2 boxes through the AY1 itemization, which includes cutoff-vector removal; translated boxes through the covariance unitary of section 7). The pure-state trace distance `2 sqrt(1-|<psi,psi_L>|^2)` and partial-trace contractivity give `rho^{F,N,L}_Y -> rho^{F,N}_Y` in trace norm (F23), so (R03) passes to the untruncated vectors at every fixed pair `(N,M)` by closedness of the ball. (The hypothesis also states the untruncated bound at fixed `N` directly; this is a second derivation.)
3. Only then `N` tends to infinity, on the untruncated vectors.

At fixed `L` the cutoff-space sequences are also Cauchy, but their limits are not used and nothing is said about letting `L` grow after `N`: the fixture `a(N,L)=1 if L<=N else 0` has iterated limits 1 and 0. `check.py` verifies an exact Eckart instance (`H=diag(0,1/2,1)`, `psi_L=(2/3,2/3,1/3)`: `1-|<psi,psi_L>|^2=5/9 <= (E_L-E_0)/gap=2/3`).

## 5. Item 2: the common limit of F1 and F2

**Theorem 5.1 (conditional_on_bb1_targets).** `omega^{F1}_inf = omega^{F2}_inf` on every finite region; write `omega_inf` for this state, **the limit of the named constructions**: `omega_inf(A)=lim_N omega^{F1,N}(A)=lim_N omega^{F2,N}(A)` for every quasi-local `A`.

*Proof.* For `N>=N_Y`,

\[
 \|\rho^{F1,\infty}_Y-\rho^{F2,\infty}_Y\|_1\le\|\rho^{F1,\infty}_Y-\rho^{F1,N}_Y\|_1+\|\rho^{F1,N}_Y-\rho^{F2,N}_Y\|_1+\|\rho^{F2,N}_Y-\rho^{F2,\infty}_Y\|_1\le(2c'_{\rm site}+c_h)\,g(Y)\,q^{\,d_Y(N)},
 \tag{HNM-BB2-R06}
\]

by (R05) twice and B3 (region form) for the middle term. The right side tends to 0 and the left side does not depend on `N`. On `R` the same argument gives `(2C'+C_h) q^{N-1}`. ∎

The identification constants are `2c'_site+c_h = 3/500000` (region) and `2C'+C_h = 3/250000` (R), both nondecreasing in `(C_h,c_h)`. This is a common limit of the two named constructions; it is not uniqueness of any ground state and says nothing about states outside the named constructions.

## 6. Item 3: identification with every AQ1 and F2 subsequential limit, then inheritance

**Theorem 6.1 (conditional_on_bb1_targets).** (a) **Identification.** Every AQ1 subsequential limit and every F2 subsequential limit equals `omega_inf` on every finite region.

*Proof.* An AQ1 subsequential limit is (AQ1 section 2) a state `omega'` for which, along some subsequence `N_k`, `rho^{F1,N_k}_Y -> rho'_Y` in trace norm for every finite `Y`. By Corollary 4.2 the whole sequence `rho^{F1,N}_Y` converges to `rho^{F1,inf}_Y`; a subsequence of a convergent sequence converges to the same limit, and trace-norm limits are single-valued, so `rho'_Y=rho^{F1,inf}_Y` for every finite `Y`. A state on the quasi-local algebra is determined by its local restrictions, so `omega'=omega^{F1}_inf=omega_inf`. For an F2 subsequential limit (AY1 section 3.4, BA2 gate statement (5)) the same argument uses `rho^{F2,inf}_Y=rho^{F1,inf}_Y` (Theorem 5.1). ∎

Consequently the set of AQ1 subsequential limits, nonempty by AQ1 compactness, is the single state `omega_inf`, and the AQ1 "chosen" state is `omega_inf` whichever subsequence was chosen.

(b) **Inheritance, only after (a).** In the GNS representation `(pi_inf, H_inf, Omega_inf)` of `omega_inf` (unitarily equivalent to AQ1's chosen representation, because the states are equal), `omega_inf` has exactly the following admitted properties, each quoted from its gate:
1. AQ1: a compatible locally normal gauge-invariant **stationary** state under `T_theta`; strongly continuous GNS evolution `U_theta pi(A)Omega=pi(T_theta(A))Omega` with a **nonnegative self-adjoint** physical energy generator (`U_t=exp(itH_num/hbar)`, `H_num Omega=0`); the physical cyclic restriction reduces it.
2. AQ2: the complete original-endpoint gauge-fixed space equals the invariant-local cyclic completion `H_phys` and reduces the generator; on it `H_phys >= (alpha/16)(I-P_Omega)` as a quadratic-form inequality, with a **simple vacuum on the invariant-local cyclic completion**.
3. AQ2, full-GNS strengthening **only as qualified in the AQ2 gate**: the same inequality on the full GNS space, which explicitly uses AM2's separately reviewed full-Hilbert finite gap (a premise of AQ2, not re-proved here).
4. AQ2: the original xz Wilson loop has variance at least `61999/250000` in the same state.
5. BA2: the F2 limit dynamics is `T_theta`, so BA2's rerun of AQ1 sections 4–5 for F2 subsequential limits concerns this same state and the same dynamics.

**Not inherited:** uniqueness of every infinite-volume ground state; any statement about states outside the named constructions; equality of GNS dynamics of different states; an unqualified full-GNS gap; translation invariance (AQ1 and AQ2 exclude it; it is item 4, proved separately). `check.py` rejects each of these as an inherited property, and rejects inheritance ordered before the identification or from a subsequence only.

## 7. Item 4: coarse translation invariance through the general-volume comparison

**Lemma 7.1 (covariance under coarse translations).** Let `v` be in `Z^3` and `t_v=(4v_x,2v_y,v_z)` the fine translation. By (I1.1), `x=4i+r` gives `x+4v_x=4(i+v_x)+r`, and likewise for `y` and `z`, so `pi(p+t_v)=pi(p)+v`: the links owned by `b` map to the links owned by `b+v` with the same residues and directions, and every face maps to a face of the same class (orientation, `r`, `s`): selected to selected, omitted to omitted, `M_f` to `M_f+v`. The on-site operators repeat at every coarse site (selected triple `(0,0,0)`, AQ1 section 1). Let `T_v` be the site relabelling `H_V -> H_{V+v}`. Then

\[
 T_v\,\widehat H^{P}_V\,T_v^{*}=\widehat H^{P}_{V+v}\qquad(P=F1,F2),
 \tag{HNM-BB2-R07}
\]

because `b+S` is inside `V` iff `b+v+S` is inside `V+v`, `M_f` is inside `V` iff `M_f+v` is inside `V+v`, and `(V+S)+v=(V+v)+S`; the same holds in each `Q_L` (the cutoff projections are functions of the `h_b`). Ground vectors are simple, so `psi^{P,V+v}=T_v psi^{P,V}` up to a phase and `rho^{P,V+v}_{Y+v}=T_v rho^{P,V}_Y T_v^*`. `check.py` verifies the face-set, padding and owner-set covariance for F1 and F2 at `(N,v)=(3,(1,0,0))`, `(3,(0,-1,1))`, `(4,(1,1,0))`. ∎

**Lemma 7.2 (non-coarse fine translations are rejected).** A fine translation `t` preserves the selected set, every face class and the owner map (`pi(p+t)-pi(p)` constant) **iff** `t=(4v_x,2v_y,v_z)`: checked exhaustively for all 64 translations of the fine period window `[0,8)x[0,4)x[0,2)`, of which exactly 8 are coarse. Witness: `t=(1,0,0)` maps the selected xy face at `r=2`, `s=0` to the class `r=3`, `s=0`, which is omitted (owner set `{0,e_x}`). Such a `t` is not a symmetry of the patterned model; nothing is claimed for it. ∎

**Theorem 7.3 (conditional_on_bb1_targets; pre-registered item 4).** For every coarse `v`, `P` in {F1, F2} and `N>=|v|_inf+2`:

\[
 \|\rho^{P,\Lambda_N+v}_R-\rho^{P,\Lambda_N}_R\|_1\le C_h\,q^{\,N-|v|_\infty-1},\qquad
 \|\rho^{P,\Lambda_N+v}_Y-\rho^{P,\Lambda_N}_Y\|_1\le c_h\,g(Y)\,q^{\,N-|v|_\infty-m(Y)}\ \ (Y\subset\Lambda_{N-|v|_\infty}),
 \tag{HNM-BB2-R08}
\]

and the limit is invariant: `omega_inf(alpha_v(A))=omega_inf(A)` for every quasi-local `A`, with `alpha_v(A)=T_v A T_v^*`.

*Proof.* Coordinatewise `[-N+v_i,N+v_i]` contains `[-(N-|v|_inf),N-|v|_inf]`, so both volumes contain `Lambda_{N-|v|_inf}`, with `n=N-|v|_inf>=2`. For `v` nonzero they are not nested and their union is not a centered cube, so the centered-cube comparisons do not apply; **B5, compared directly**, gives (R08). (Through the union with nested-only B5, Lemma 3.1 gives the labelled fallback `2C_h q^{N-|v|_inf-1}`.) For invariance, take `A` in `B(H_Y)`. By Lemma 7.1 with `V=Lambda_N-v`, `omega^{P,N}(alpha_v(A))=omega^{P,Lambda_N-v}(A)`, hence

\[
 |\omega^{P,N}(\alpha_v(A))-\omega^{P,N}(A)|\le\|\rho^{P,\Lambda_N-v}_Y-\rho^{P,\Lambda_N}_Y\|_1\|A\|\le c_h\,g(Y)\,q^{\,N-|v|_\infty-m(Y)}\|A\|\longrightarrow0 .
\]

By item 1 on `Y+v` and on `Y`, the left terms tend to `omega_inf(alpha_v(A))` and `omega_inf(A)`. Density and `||alpha_v||=1` extend the identity to the quasi-local algebra. With the R form alone, the limit on each translate `R+v` exists and equals the translate of the limit on `R`. ∎

Rows `C_h q^(N-|v|_inf-1)` (exact in `results.json`): `(N,v)=(2,0)`: `1/16000000`; `(3,(1,0,0))`: `1/16000000`; `(4,(1,-1,0))`: `1/1024000000`; `(6,(2,1,0))`: `1/65536000000`; `(8,(1,2,-3))`: `1/4194304000000`; `(10,(3,0,0))`: `1/17179869184000000`. Scope: coarse translations; the limit of the named constructions. Translation invariance is claimed only as this separate item, from the general-volume comparison; nested cubes alone cannot compare `Lambda_N+v` with `Lambda_N`.

## 8. Item 5: correlation functions on the compact window

**8.1 Inputs from the BA2 gate (admitted; exact).** For `|theta|<=8`, `A` in `B(H_R)`, `n>=2` and `F` in {F1, F2}:

\[
 \text{(D1)}\ \ \sup_{M>n}\|T^{F,M}_\theta(A)-T^{F,n}_\theta(A)\|\le\frac{K_F}{n-1}\|A\|,\qquad
 \text{(D2)}\ \ \|T_\theta(A)-T^{F,n}_\theta(A)\|\le\frac{K_F}{n-1}\|A\|,
\]

with `K_F1 = 9261/155720800000000` (BA2 forward, faces charged once, inner F1; route `duhamel_inner_f1`; `592704 tau^2/(1-338688|tau|)` at the cap; (D2) by `M -> infinity` in (D1)) and `K'_F2 = 1055961408185869563/30481402343750000000000000000` (BA2 reverse, owner-set `Phi'`, inner F2; route `duhamel_inner_f2`; `345744 tau^2 E_up(592704|tau|)` at the cap; (D2) is the gate's `min(K_F1, second-route K_F2)/(N-1)` bound). `check.py` parses these values from the pinned BA2 gate text, re-evaluates the BA2 formulas exactly and requires equality.

**Definition 8.2 (dynamics constants).** `C_dyn[F]=2K_F`, because item 5 replaces the finite-box evolution by `T^{F,r_N}` inside `omega^{F,N}` (D1 with `M=N`) and the limit evolution by `T^{F,r_N}` inside `omega_inf` (D2):
- **`C_dyn[F1] = 9261/77860400000000`** (preview `1.18943647862e-10`), tier `polynomial_lieb_robinson`, route `duhamel_inner_f1`, margin `4.2037` against `1/2000000000`;
- **`C_dyn[F2] = 1055961408185869563/15240701171875000000000000000`** (preview `6.92856185734e-11`), tier `polynomial_lieb_robinson`, route `duhamel_inner_f2`, margin `7.2165`.

Labelled alternatives, also admitted, not used: `2x` the BA2 reverse whole-star F1 value (about `2.0390e-10`, `duhamel_inner_f1`) and `2x` the BA2 forward F2 value (about `1.8904e-10`, `duhamel_inner_f1`).

**Lemma 8.3 (every r; conditional_on_bb1_targets through item 1).** For `N>r>=2`, `|theta|<=8`, `A` in `B(H_R)`, with `c^{F,N}_A(theta)=omega^{F,N}(A* T^{F,N}_theta(A))-|omega^{F,N}(A)|^2` and `c^inf_A(theta)=omega_inf(A* T_theta(A))-|omega_inf(A)|^2`:

\[
 |c^{F,N}_A(\theta)-c^{\infty}_A(\theta)|\le\|A\|^2\Big[\frac{C_{\rm dyn}[F]}{r-1}+c'_{\rm site}\,|\Lambda_r|\,e^{|\Lambda_r|/10^8}\,q^{\,N-r}+2C'\,q^{\,N-1}\Big].
 \tag{HNM-BB2-R09}
\]

*Proof.* Put `a_N=omega^{F,N}(A)`, `a=omega_inf(A)`, `B_r=T^{F,r}_theta(A)`, an element of `B(H_{Lambda_r})` (the F2 padding factors out) with `||B_r||=||A||`; `R` is inside `Lambda_r`. Then

\[
 c^{F,N}_A-c^{\infty}_A=\omega^{F,N}\big(A^*(T^{F,N}_\theta(A)-B_r)\big)+(\omega^{F,N}-\omega_\infty)(A^*B_r)+\omega_\infty\big(A^*(B_r-T_\theta(A))\big)-\big(|a_N|^2-|a|^2\big).
\]

The first and third terms are at most `||A|| K_F/(r-1) ||A||` by (D1) with `n=r`, `M=N`, and by (D2). The second is `|Tr((rho^{F,N}_{Lambda_r}-rho^inf_{Lambda_r}) A* B_r)| <= ||rho^{F,N}_{Lambda_r}-rho^inf_{Lambda_r}||_1 ||A||^2`, and (R05) with `Y=Lambda_r` inside `Lambda_N`, `m(Y)=r`, `d_Y=N-r` bounds it by `c'_site |Lambda_r| e^{|Lambda_r|/10^8} q^{N-r} ||A||^2`. The fourth is `| |a_N|-|a| |(|a_N|+|a|) <= 2||A|| |a_N-a| <= 2||A||^2 ||rho^{F,N}_R-rho^inf_R||_1 <= 2C' q^{N-1} ||A||^2`. The four deterministic terms add linearly. ∎

The centering uses the **complex mean** `|omega(A)|^2`; with `omega(A)^2` the `theta=0` value is not the variance (fixture (c), `omega(A)=12i/25`).

**Theorem 8.4 (item 5 with the frozen r_N; conditional_on_bb1_targets).** For `N>=5`, `r_N=floor((N-1)/2)` (so `2<=r_N<N`, `R` inside `Lambda_{r_N}` inside `Lambda_N`, `N-r_N>=(N+1)/2`), `|theta|<=8`, `A` in `B(H_R)` and `F` in {F1, F2}:

\[
 |c^{F,N}_A(\theta)-c^{\infty}_A(\theta)|\le\|A\|^2\Big[\frac{C_{\rm dyn}[F]}{r_N-1}+c'_{\rm site}\,|\Lambda_{r_N}|\,e^{|\Lambda_{r_N}|/10^8}\,q^{\,N-r_N}+2C'\,q^{\,N-1}\Big].
 \tag{HNM-BB2-R10}
\]

This is (R09) with `r=r_N` as frozen; no other `r` enters any quantitative statement. The three constants are separate (tiers: `C_dyn` polynomial_lieb_robinson with its BA2 route; `c'_site` and `C'` exact_first_order, union_comparison, bb1_frozen_targets); there is no single bracket for the sum.

**Values** (per term exact; the region term and the sum are directed rational upper bounds on the `10^-40` grid, `e^x` enclosed with `E_UP=27183/10000`, `E_LO=2718/1000` and a series tail bound):

| `F`, `N` | `r_N`, `|Lambda_{r_N}|` | `C_dyn/(r_N-1)` | region term | `2C'q^(N-1)` | sum (upper) |
|---|---|---|---|---|---|
| F1, 5 | 2, 125 | `1.18943647862e-10` | `9.53675508499e-10` | `4.76837158203e-13` | **`1.07309599352e-9`** |
| F2, 5 | 2, 125 | `6.92856185734e-11` | `9.53675508499e-10` | `4.76837158203e-13` | **`1.02343796423e-9`** |
| F1, 10 | 4, 729 | `3.96478826206e-11` | `2.12168470732e-14` | `4.44089209850e-22` | **`3.96690994682e-11`** |
| F2, 10 | 4, 729 | `2.30952061911e-11` | `2.12168470732e-14` | `4.44089209850e-22` | **`2.31164230386e-11`** |

At `N=5` the region term dominates (its `q^3` is only `1/262144`); from `N=6` on the dynamics term does for F1.

**8.5 Rate in N: certified range and where the frozen form stops being useful.**
- **Certified O(1/N) on `5<=N<=14000`.** The bracket of (R10) is at most `K5[F]/N` with `K5[F]=10 C_dyn[F] + K_reg + K_R`: `N/(r_N-1)<=10` (checked for every `N` in the range); `N` times the region term is at most `K_reg = 27183/2097152000000` (about `1.29619e-8`) — block A, `5<=N<=464`, where `|Lambda_{r_N}|<10^8`, `|Lambda_{r_N}|<=N^3`, `q^{N-r_N}<=8^{-(N+1)}` and `N^4 8^{-(N+1)}` decreases, and nine blocks B from 465 to 14000, each verified by one integer inequality `b^4 27183^k 10000*262144 <= 625*27183*10^(4k) 8^(a+1)` with `k=ceil(b^3/10^8)`; `N` times `2C'q^(N-1)` is at most `K_R = 1/419430400000`. Hence **`K5[F1] = 7222143131/510265917440000000`** (about `1.41537e-8`) and **`K5[F2] = 42627861255071838599399/3121295600000000000000000000000`** (about `1.36571e-8`). The rate is O(1/N) because the Lieb–Robinson function `F(r)=(1+r)^-4` is polynomial; no exponential rate in `N` is claimed for item 5.
- **The frozen form is not O(1/N) as N grows without bound.** At `N=14421` (`r_N=7210`, `|Lambda_{r_N}|=14421^3`) the region term alone is at least 2, certified exactly with `E_LO`; since each centred correlation has modulus at most `||A||^2`, the bracket then exceeds the trivial bound 2 and (R10) is vacuous. Labelled float previews: the region term first exceeds the dynamics term at `N=14411` and exceeds 1 at `N=14419`. The cause is the frozen region form: `e^{|Lambda_{r_N}|/10^8}` with `|Lambda_{r_N}|` of order `N^3` eventually beats `q^{N-r_N}`. This is recorded as a contract wording finding (W1); `r_N` is not re-chosen.

**Corollary 8.6 (whole-sequence convergence of the correlation functions, no rate).** For each fixed `r>=2`, (R09) gives `limsup_N |c^{F,N}_A(theta)-c^inf_A(theta)| <= ||A||^2 C_dyn[F]/(r-1)`, uniformly for `|theta|<=8`. Since `r` is arbitrary, `c^{F,N}_A(theta) -> c^inf_A(theta)` along the whole sequence, uniformly on the window: the correlation functions of `omega_inf` on `|theta|<=8` are the limits of the finite-box correlation functions. Here `r` is a free parameter of a family of inequalities that hold simultaneously; it is not a choice of `r_N` and gives no rate. `c^inf_A` is the Stone correlation of `(pi(A)-a)Omega` in the GNS representation of `omega_inf` (AQ2.6), now along the whole sequence.

**What item 5 does not say.** Nothing uniform in time (the BA2 constants hold for `|theta|<=8`, `U=1`, and grow like `U^2/(1-vU/3)`); no equality of GNS dynamics of different states (`omega^{F,N}` and `omega_inf` are different states; only the numbers `c` converge; fixture (e) shows two states with one algebraic dynamics and different correlations); nothing uniform in the lattice spacing.

## 9. Scaling tau to tau/100, each constant against its own bracket

| constant | ratio `X(tau)/X(tau/100)` | preregistered bracket | met |
|---|---|---|---|
| `C'` | exactly 1 (`C_h` is a tau-independent hypothesis value; factor 1) | exactly 1 | yes |
| `c'_site` | exactly 1 | exactly 1 | yes |
| `C_dyn[F1]` | `1953058850/194651` (about `10033.644`), from `2*592704 tau^2/(1-338688|tau|)` | `[9500,10500]` | yes |
| `C_dyn[F2]` | `38176688920663121234473000000/3810205403940325763421973` (about `10019.588`), from `2*345744 tau^2 E_up(592704|tau|)` | `[9500,10500]` | yes |
| `C'_2`, `c'_2` (secondary) | exactly 1 | `[99/100,101/100]` | yes |
| `q_2` | exactly 100 | exactly 100 | yes |
| item-5 sum | no single bracket; each constant separately | — | — |

The same exact formula is evaluated at `tau` and at `tau/100` without intermediate rounding. A linear-order dynamics bound (ratio 100), a tau-dependent `C'`, a cubic label, a misread secondary factor, a `q_2` ratio of 10 and a bracket chosen after evaluation are each rejected.

## 10. Exact finite fixtures (model_is_finite_graph true, transfers_to_aq false)

- **(a) One-state ball versus whole sequence** (`fixture_whole_sequence_vs_subsequence`, `cauchy_estimate_not_compactness`): `rho_N=diag(1/2+(-1)^N delta, 1/2-(-1)^N delta)`, `delta=1/1000`. Every term lies within `2 delta` of `P=diag(1/2,1/2)` (a one-state ball in every box), yet the even and odd subsequences have limits at distance `4 delta`; the tail supremum stays `4 delta`. Rejected as convergence.
- **(b) Steps alone are not a Cauchy estimate:** the zigzag walk on `[0,1]` with steps `1/(n+1)` satisfies every `N` to `N+1` bound and oscillates by at least `1/2` after `N=10`, `100`, `400`. Rejected as a Cauchy estimate; the BB2 bound is a supremum over all `M>N`.
- **(c) Complex-mean centering** (`fixture_correlation_centering`): `phi=(3/5,4/5)`, `A e_1 = i e_0`: `omega(A)=12i/25`, `|omega(A)|^2=144/625`, `omega(A)^2=-144/625`, `omega(A*A)=16/25`, and `||(A-a)phi||^2=256/625=omega(A*A)-|omega(A)|^2`. Centering with `omega(A)^2` or without centering is rejected; so are a post-hoc `r_N` and an exponential tail claimed with the polynomial `F`.
- **(d) Translation residues** (`fixture_translation_residues`): section 7; `t=(1,0,0)`, `(0,1,0)`, `(2,0,0)` rejected as symmetries; a translated box compared through nested cubes rejected.
- **(e) Topology and algebraic versus GNS dynamics:** `U(t)e_j=e^{ijt}e_j`, `A e_j=e_{2j}`: on the moving vector `e_n` at `t=pi/n` the difference `U A U*-A` has norm 2 for every `n` up to 40, while on the fixed vector `e_1` it is at most `pi/n<22/(7n)`; `H=diag(0,1)`, `A=sigma_x`, `u=pi/2`: two states under one algebraic dynamics give `omega_0(A tau(A))=i` and `omega_1(A tau(A))=-i`.
- **(f) Cutoff order:** `a(N,L)=1 if L<=N else 0` has `lim_L lim_N = 1` and `lim_N lim_L = 0`, checked exactly on a grid; reversing the order is rejected.

These are exact finite audits of the traps; they prove no infinite-volume statement.

## 11. Error ledger (preregistered terms)

| term | entry |
|---|---|
| `bb1_hypothesis_constants` | `C_h=1/250000` (R form), `c_h=1/500000` (region form) at `q=1/64`; secondary `C_2h=1/20000`, `c_2h=1/40000` at `q_2=151552|tau|` (labelled); conditional_on_bb1_targets |
| `cauchy_telescoping_or_union` | union comparison with factor 1 for nested centered cubes (the union is the larger cube): `C'=C_h`, `c'_site=c_h`; no telescoping sum (no `1/(1-q)`); non-nested pairs cost factor 2 (labelled) |
| `identification_with_subsequential_limits` | 0: exact (every subsequence of a trace-norm convergent sequence has the same limit); no constant enters |
| `translation_general_volume` | `C_h q^(N-|v|_inf-1)` on `R`, `c_h g(Y) q^(N-|v|_inf-m(Y))` on `Y` (B5 direct); labelled union fallback `2C_h q^(N-|v|_inf-1)` |
| `dynamics_constant_from_ba2` | `C_dyn[F1]=9261/77860400000000` (`duhamel_inner_f1`), `C_dyn[F2]=1055961408185869563/15240701171875000000000000000` (`duhamel_inner_f2`): twice the exact BA2 gate values |
| `region_form_on_Lambda_rN` | `c'_site |Lambda_{r_N}| e^{|Lambda_{r_N}|/10^8} q^(N-r_N)`: `9.53676e-10` at `N=5`, `2.12168e-14` at `N=10`; O(1/N) of the bracket certified on `5<=N<=14000`; vacuous at `N=14421` |
| `arithmetic` | 0: exact Fractions; `e^x` replaced by directed rational enclosures; block comparisons in integers; decimals are truncated previews that no admission reads |

## 12. Mandatory sentence and gate fields

**Mandatory sentence (the contract template, verbatim, once):**

For the zero-selected patterned family at the same coupling |tau|<=10^-8, under the BB1 locality bounds at their frozen targets as hypotheses (discharged only when the BB1 gate admits constants at most those targets), the reduced densities of the named construction families F1 and F2 on centered coarse cubes converge as whole sequences, at a rate in N, to one common limit on every finite region; this limit coincides with every AQ1 subsequential limit and every F2 subsequential limit, is invariant under coarse translations, and has as correlation functions on |theta|<=8 the limits of the finite-box correlation functions; this is convergence of the named constructions, not uniqueness of any ground state, not a statement about states outside the named constructions, and not a statement uniform in the lattice spacing a.

The constants in it: `C'=1/250000`, `c'_site=1/500000` at `q=1/64` (item 1), `C_h q^(N-|v|_inf-1)` (item 4), `C_dyn[F1]=9261/77860400000000`, `C_dyn[F2]=1055961408185869563/15240701171875000000000000000` (item 5); F1 = AQ1 centered whole-star boxes, F2 = I1 section 6 all-contained-face boxes with padding, `Lambda_N=[-N,N]^3`, `N>=2` (`N>=5` for item 5).

**Gate fields.** The contract's `gate_fields_rule` says an undischarged hypothesis keeps every field that depends on it false. This producer cannot see the BB1 gate, so `results.json` exports two blocks:
- **top level (before the discharge):** `whole_sequence_claimed`, `common_limit_claimed`, `state_convergence_claimed`, `translation_invariance_claimed`, `rate_in_N_claimed` all `false`; `dynamics_level: algebraic_heisenberg_compact_window` (the BA2 level, which does not depend on BB1); the scope texts as in the contract; `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `continuum_claim`, `gns_dynamics_equality_claimed`, `uniform_in_time_claimed`, `weak_coupling_claim`, `scientific_priority_verified` all `false`;
- **`gate_fields_after_discharge`:** exactly the contract values (the five BB1-dependent fields `true`, `dynamics_level: correlation_functions_compact_window`), which hold for accepted_within_scope once the BB1 gate admits every hypothesis of section 2.3.

Claim flags `continuum_claim`, `uniqueness_of_ground_state_claimed`, `gns_dynamics_equality_claimed`, `uniform_in_time_claimed`, `rate_in_a_claimed`, `scientific_priority_verified`, `weak_coupling_claim`, `uniform_wilson_claim`, `resolved_interaction_shift` are all `false`.

## 13. Exclusions and limitations

**Contract exclusions.** None of the following is claimed (verbatim, comma-separated): uniqueness of every infinite-volume ground state, states outside the named constructions, uniform-in-time statements, equality of GNS dynamics of different states, any estimate uniform in the lattice spacing a, continuum or weak coupling, scientific priority.

**Preregistration exclusions.** None of the following is claimed either (verbatim, comma-separated): uniqueness of every infinite-volume ground state, statements about boundary conditions outside the named constructions, any estimate uniform in the lattice spacing a, continuum or weak coupling, scientific priority.

The object is the limit of the named constructions. It is not called the thermodynamic limit, and it is not the infinite-volume ground state of the model in any uniqueness sense.

**Limitations.**
1. **Conditional.** Every BB2 conclusion here is conditional_on_bb1_targets. It becomes unconditional only after the BB1 gate admits constants at most `C_h`, `c_h` (and, for the labelled secondary pair, `C_2h`, `c_2h`) for B3, B4/B5 nested and B5 general, in the R and region forms, in each `Q_L`, for the untruncated vectors at fixed `N`, at both signs. This producer read no BB1 file other than the contract and cannot record that discharge.
2. **Item 5 rate range.** The frozen bracket is O(1/N) only on the certified range `5<=N<=14000`; at `N=14421` it is vacuous (section 8.5). Beyond the certified range only the qualitative whole-sequence convergence of Corollary 8.6 holds.
3. **Item 4 constant.** The contract constant `C_h q^(N-|v|_inf-1)` needs the direct non-nested B5; the union route alone gives the labelled `2C_h q^(N-|v|_inf-1)`.
4. **Scope.** Only the zero-selected patterned family, fixed spacing and strong bare coupling `|tau|<=10^-8`, the two named families on centered cubes and their coarse translates; nothing transfers to literal vertex boxes, periodic or orthant boxes, nonzero selected triples, the uniform route-B model, weak coupling or the continuum. Every constant is uniform in `N` at fixed spacing and in the on-site cutoff, never in the spacing.
5. **Inherited without re-proof:** the BA2 gate constants and identification (Nachtergaele–Sims Theorem 4.1 as transcribed, not machine-checked); AQ1 compactness, stationarity, GNS continuity and generator; AQ2's gap on `H_phys` and its qualified full-GNS strengthening (which uses AM2's full-Hilbert finite gap); AM2's simple ground and gap for every finite I1 volume; AV1 F20–F23; AY1's F2 itemization; the I1 dictionary; standard Banach-space facts.
6. **Upper bounds only.** `C'=C_h` and `c'_site=c_h` are the hypothesis constants themselves (the union adds nothing for nested cubes); the dynamics constants are twice BA2 upper bounds.
7. **Independence.** The contract names the assembly; the hypotheses and the BA2 constants are shared with the forward producer; all agents are correlated model agents. The `-tau` evaluations replay the same `|tau|` formulas. Scientific priority is unverified.

**Methodological lenses (modern use of the snapshotted skills).** *Newton, analysis before synthesis:* the reverse starts from the desired Cauchy form and asks which comparisons are sufficient; it finds that nested one-prescription comparisons suffice for items 1–3 and 5, and that item 4's constant needs the non-nested one. *Tesla, complete accounting:* each of the four terms of item 5 is placed and charged once, and the frozen region form is followed to the size where it stops being useful rather than being quoted beyond it. No historical figure endorses anything here, and no historical or occult material supplies a premise.

## 14. Contract wording findings (non-blocking)

- **W1 (item 5 rate).** `required` item 5 says the rate in `N` is O(1/N). With the frozen `r_N` and the frozen region form `c'_site |Y| e^{|Y|/10^8} q^{d_Y}`, the bracket is O(1/N) on the certified range `5<=N<=14000` and vacuous from `N=14421` on, because `|Lambda_{r_N}|` grows like `N^3` inside the exponential. The polynomial-F reading (the dynamics term is O(1/N), never exponential) is met; the literal asymptotic reading is not. Nothing was retuned.
- **W2 (gate fields before the discharge).** `gate_fields_rule` keeps BB1-dependent fields false while undischarged, and producers finish before the BB1 gate; both blocks are exported (section 12).
- **W3 (union versus direct).** The contract describes the reverse as the general-volume comparison "through unions", while item 4's constant is the direct factor-1 bound; BB1 labels the union route as costing a factor 2. For nested pairs the union is the larger volume and costs nothing; for translated boxes the direct B5 is needed for the contract constant.
- **W4 (C_dyn).** "`C_dyn` read exactly from the BA2 gate": the gate states Cauchy constants `K`; item 5 needs two replacements, so `C_dyn=2K`, consistent with the frozen `1/2000000000 = 2 x 2.5x10^-10`. Item 5 names one `C_dyn`; the gate has one per family and route, so one constant per family is exported.
- **W5.** The `exactly 1` brackets for `C'` and `c'_site` are satisfied by construction (hypothesis values are numbers); the tau scaling of BB1 is checked in BB1.
- **W6.** The contract and preregistration exclusion lists differ (seven versus five items); both are quoted and honoured.
- **W7.** 15 of the 34 controls carry frozen semantics in `new_control_semantics`; the other 19 are implemented from their BA1/BA2/BB1 meaning.
- **W8.** At `Y=R` the region form gives `2c_h e^{2/10^8} q^{N-1}`, marginally above the R form `C_h q^{N-1}`; the R form is used on `R`.
- **W9.** Item 3 lists BA2's rerun of AQ1 sections 4–5 for F2 limits; after items 1–2 every F2 subsequential limit is `omega_inf`, so the rerun is consistent and adds no new state.
- **W10.** `preregistration.observable` names "translation differences"; the quantity bounded is the difference of the reduced densities of `Lambda_N+v` and `Lambda_N`.

## 15. Discharge table for the BB2 skeptic

| item | holds unconditionally when the BB1 gate admits, at most the hypothesis values, | otherwise |
|---|---|---|
| 1 (R) | B4 or B5 for same-family nested pairs, R form, each `Q_L` and untruncated, both signs | insufficient (the Cauchy estimate is not closed) |
| 1 (Y) | the same with the region form | limited: items 1–2 on `R` only |
| 2 | B3, R and region forms | limited: no common limit (items 3–5 per family only) |
| 3 | items 1–2 | limited: identification for `R`-marginals only (without the region form) |
| 4 | B5 for non-nested pairs, R and region forms | limited: item 4 dropped (with nested-only B5: the labelled `2C_h` bound) |
| 5 | item 1 in both forms | limited: item 5 dropped |

## 16. Map of contract items and controls to sections and checks

| contract item | section | `check.py` check ids |
|---|---|---|
| 1 | §§2–4 | `hypotheses_equal_bb1_frozen_targets`, `item0_union_comparison_assembly`, `item1_whole_sequence_cauchy_R_and_regions`, `item1_cutoff_uniform_then_removed`, `cauchy_estimate_not_compactness`, `region_constant_scales_with_Y`, `cutoff_uniform_then_removed`, `conditional_on_bb1_targets`, `rate_constant_pair_prefrozen` |
| 2 | §5 | `item2_common_limit_F1_F2`, `two_families_named`, `named_construction_not_uniqueness` |
| 3 | §6 | `item3_identification_then_inheritance`, `limit_identified_with_aq1_limits`, `subsequence_versus_whole_sequence` |
| 4 | §7 | `item4_coarse_translation_invariance`, `translation_invariance_separate_item`, `fixture_translation_residues` |
| 5 | §8 | `ba2_gate_dynamics_constants_read_exactly`, `item5_correlation_bound_three_constants`, `item5_rate_in_N_certified_range`, `r_N_prefrozen`, `fixture_correlation_centering`, `lieb_robinson_polynomial_tail`, `time_window_named_common_clock`, `algebraic_not_gns_dynamics`, `topology_named`, `common_clock`, `ns_theorem_4_1_quoted_verbatim` |
| 6 | §§9–12 | `item6_tau_scaling_per_constant`, `tau_scaling_exponent`, `fixtures_exact`, `fixture_whole_sequence_vs_subsequence`, `mandatory_template_once`, `gate_fields_undischarged_and_after_discharge`, `error_ledger_itemized`, the 34 control ids |
| binding | header | `contract_snapshots_bound_before_evaluation`, `check_py_sha256_recorded_before_evaluation`, `pinned_gate_and_excerpt_hashes`, `reverse_inputs_inventory_isolated`, `premise_gates_read`, `no_interpreter_cache_in_closure` |

| control | damaging mutations rejected (summary) |
|---|---|
| `coherent_evidence_tampering` | with the contract hash rebound: isolation flag, a control removed, a gate field, a hash-binding flag, the `C'` target loosened, the hypothesis changed in both places, `r_N` changed; a snapshot removed with its line; unrehashed byte change; BB1 contract target edited; BA2 gate constant edited; NS excerpt edited |
| `exact_arithmetic_admission` | float, bool, NaN, zero denominator, float target, decimal preview |
| `no_priority_or_continuum_claim` | continuum, priority, weak coupling, ground-state uniqueness flags |
| `changed_model_relabelled` | `tau=10^-7`, nonzero triple, SU(3), 2D, finite graph, uniform model, `l1` state metric, exponential weights, window 64, literal vertex boxes |
| `insufficient_verdict_retained` | missed `C'` relabelled accepted; BB1 insufficient relabelled limited; partial discharge relabelled accepted; item 4 dropped relabelled accepted; open Cauchy estimate relabelled limited; condition dropped before the discharge; tau retuned |
| `tau_scaling_exponent` | linear `C_dyn`, tau-dependent `C'`, cubic label, secondary factor misread, `q_2` ratio 10, post-hoc bracket |
| `wrong_delta_alpha_hbar_clock` | `u` window labelled `theta`, `delta` clock, one-eighth window, Euclidean clock |
| `root_n_misuse` | item-5 terms in quadrature, division by `sqrt(N)`, union legs in quadrature |
| `tier_mixing_rejected` | state constant with the LR tier; dynamics constant with a state tier; BB1 route claimed; assembly as a route label; assembly missing; lumped item-5 bracket; dynamics value not twice a gate value; F1 constant with the inner-F2 route; dynamics constant with an assembly label |
| `reverse_premise_isolation` | forward BB2 report, BB1 gate, BB1 reverse producer, BB1 skeptic, a triage file, a BB contract review, a lens memo, a deliberation; a premise removed |
| `uniform_in_N_not_in_a` | uniformity in the spacing (two forms), unqualified uniformity, continuum reading |
| `placeholder_span_rejected` | whitespace, bar and `e.g.` angle spans; a rehashed contract placeholder |
| `negation_aware_phrase_scan` | five affirmative forbidden phrasings; a negated clause passes |
| `parameters_declare_metric_weights_window` | metric, weights, window, clock removed (rehashed) |
| `rate_constant_pair_prefrozen` | `q` per `N`, `q=1/32`, `C_h` or `c_h` retuned |
| `decay_rate_in_N_not_a` | fm, physical-length, lattice-spacing readings, rate without a coarse step |
| `topology_named` | norm continuity in `theta`, weak-* states, one topology |
| `two_families_named` | one family, all boundary conditions, F2 collapsed onto F1 |
| `subsequence_versus_whole_sequence` | whole sequence from compactness, unquantified limit, whole sequence from diagonal extraction |
| `common_clock` | `+tau` versus `-tau`, `tau` versus `tau/2`, F2 on the `u` clock |
| `named_construction_not_uniqueness` | three affirmative phrasings, uniqueness flag |
| `cauchy_estimate_not_compactness` | compactness plus closeness, `N` to `N+1` only, the one-state-ball sequence as Cauchy |
| `limit_identified_with_aq1_limits` | inheritance before identification, subsequence only, uniqueness, unqualified full-GNS gap, translation invariance from AQ1 |
| `translation_invariance_separate_item` | from nested cubes, not a separate item, `N` too small, hidden union factor |
| `region_constant_scales_with_Y` | R constant on `Y`, size factor dropped, exponent `N-1` for all `Y`, `e`-factor dropped |
| `cutoff_uniform_then_removed` | limits exchanged, `L`-dependent constant, eigenvalue-only removal |
| `algebraic_not_gns_dynamics` | GNS equality finite versus limit, equal correlations of F1 and F2 boxes, level relabelled |
| `lieb_robinson_polynomial_tail` | exponential rate, O(1/N) for all `N` (vacuity witness `N=14421`), exponential form, unstated range |
| `time_window_named_common_clock` | uniform in time, window unnamed, `U=Theta` |
| `fixture_whole_sequence_vs_subsequence` | alternating one-state-ball sequence as convergent, harmonic steps as Cauchy, harmonic tail as small |
| `fixture_translation_residues` | `(1,0,0)`, `(0,1,0)`, `(2,0,0)` as symmetries, a non-coarse record, a translated box through nested cubes |
| `fixture_correlation_centering` | `omega(A)^2` centering, no centering, post-hoc `r_N`, exponential tail |
| `conditional_on_bb1_targets` | another BB1 value, condition dropped, unconditional before the discharge, producer-recorded discharge, decreasing constant, gate fields true before the discharge |
| `r_N_prefrozen` | `N-2`, `floor(N/2)`, an optimized `r_N`, a record with another `r_N` |

**Not executable inside `check.py`:** what this producer actually read (checked by `freeze.py` and the skeptic); the freeze and the byte-identical replays (protocol steps of `research/round33/tools/freeze.py`); the BB1 discharge (recorded at the BB2 gate).

## 17. Reproduction

```bash
python3 -B research/round33/reverse/bb2/check.py --output /absolute/fresh/dir
python3 -B -O research/round33/reverse/bb2/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round33/tools/freeze.py verify research/round33/reverse/bb2
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/bb2.json research/round33/reverse/bb2/report.md
```
