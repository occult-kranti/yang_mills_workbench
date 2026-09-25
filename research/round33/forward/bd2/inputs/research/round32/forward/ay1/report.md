# Hruday uniform local closeness of AQ-type subsequential states and the family-independent first-order density — AY1 forward

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production (a Claude model agent) under the frozen AY1 contract (`research/round32/contracts/ay1.json`, sha256 `be9b354420e66e7edba03d59b3d194b69f26782b44cfb63cb10e176bf4879ae0`). It is correlated model-agent work, not independent human review and not formal verification.

**What this producer read.**
- The contract snapshot first (its sha256 was checked before anything else). After that, only files under `inputs/`:
  - **read in full:** `AGENTS.md`; `selection-ay1.md`; the AV1, AW1, AW2, AX1 and AX2 gates (every field except the `bindings` blocks, which were not printed) and the AM2 gate (all of it); the forward AV1 and AW1 reports; `skeptic/av1.md`; `skeptic/aw1.md`; the AM2, AQ1, AQ2, AT4 and I1 forward reports; `skeptic/am2.md`; the two forward-additional premises (`skeptic/triage.md` and `experts/jung/loop2-response.md`); the paired-physics SKILL and its complete-residual reference; the Newton, Tesla and historical-panel SKILL files;
  - **read in part:** the AW1 reverse report (its headings, and sections 5–7 on the coefficient, the remainder ledger and the outside-excitation lemma); the AV1 reverse report (headings and a keyword search of its passage section); the AM2 reverse report (headings only);
  - **not opened:** the Newton and Tesla `references/research.md` notes and the historical-panel `lenses-and-evidence.md` reference.
- **Outside `inputs/`, for protocol and code style only:** `research/round32/tools/README.md`, `research/round32/tools/freeze.py`, parts of `research/round32/forward/ax1/check.py`, the header and scratch-disclosure lines of `research/round32/forward/ax1/report.md`, and the top-level field names of `research/round32/forward/ax1/output/results.json` and `source-manifest.json` (output conventions). I did not open the AV1 or AW1 forward `check.py`. None of these carries premise weight.
- **Nothing under `research/round32/reverse/ay1/`**, no skeptic file other than the snapshotted `triage.md`, no expert file other than the snapshotted Jung loop-2 response, no `advisor/deliberation-*.md` or `panel*.md`, and no other current AY1 work was read.
- **Scratchpad disclosure (sub-round 2 rule).** My scratch work is in `/tmp/claude-0/ay1-forward-private/`. It holds a Fraction/float preview, a prototype of the creation-algebra fixture, development runs and a source-edit harness; **none of it is evidence**. I created the folder directly with `mkdir -p` and did not list `/tmp/claude-0/`, so I saw no other agent's folder names. **I opened no file in any other agent's scratchpad folder**, and no file in the shared session scratchpad root. The Claude harness saved copies of two of my own long tool outputs (the triage/Jung/selection read and the gate read) to its tool-results cache; those are my own reads, not other agents' files.

**Shared premises and attribution.** The triage (goal-4 note: "any two subsequential AQ-type limits satisfy `||rho_R-rho'_R||_1<=2D_AM2`") and the Jung loop-2 note (the first-order density coinciding for the two families; the mandatory sentence) already state the mechanism of items 2 and 3. On the forward route they are **shared panel premises**. Independence is claimed only for the F2 verification, the explicit first-order density, the exact R-marginal decomposition, the R-local constant `K_2'` and the code. The underlying facts are standard: a uniform finite-volume bound passes to every trace-norm limit (closed balls), creation-operator expansions, first-order perturbation theory and SU(2) Haar orthogonality. Scientific priority is unverified. HNM labels are project aliases.

## Verdict (forward route)

Model: **`AQ_patterned_zero_selected`**, the AM2/AQ1 zero-selected patterned family. This is SU(2) in Kogut–Susskind form on `Z^3` at fixed spacing, with coarse 24-link factors. The selected triple is exactly `(0,0,0)`, so the reference is the Haar product. The omitted faces are grouped into whole stars `phi_b=-(tau/3) sum W_f` (normalized units `delta=alpha/8`). Both signs of `tau` are covered, with `|tau|<=10^-8`. The cover is `R={0,e_z}`: 48 links, 36 endpoints and 7 incident anchors. The observable class is `B(H_R)`, and the clock is the common one, `s=alpha t_E/hbar`, `theta=alpha t/hbar`.

1. **Both families satisfy the AV1 premises (item 1).**
   - **F1**, the AQ1 centered whole-star boxes `Lambda_N` (`N>=2`), is covered by the admitted chain I1 → AV1 §1 → AM2 → AV1 → AQ1/AQ2 → AW1 (Section 2).
   - **F2**, the I1 §6 all-contained-face boxes with padding on the same `Lambda_N`, is verified item by item (Section 3):
     - supports `|X_b|<=4` and termination order 8;
     - per-site sum `J^(2)<=28|tau|=J_0` at the cap, so the AM2 contraction holds at the same `J_0` (`J_0G(R)<37/6250000<1/64`, `2J_0G'(R)<77/390625<1`);
     - reset `omega(h_R)<=98|tau|` (and `56|tau||F|` on any `F`);
     - local trace-norm compactness and diagonal extraction.

   The two topologies are named separately: states in the **trace norm on `B(H_R)`**, and dynamics in the **norm on compact time windows**. The latter is named only; no dynamical statement is made for F2.
2. **Closeness (item 2).** Any two subsequential limits, from the same family or from different families, at the same `tau` satisfy

   `||rho_R-rho'_R||_1 <= 2D = 1170159676931825184288274812132100/42981220507576537932303142777593983768257` (about `2.72249057405e-8`).

   Here `D` is the AV1-admitted tier (ii), forward density route. The bound meets the preregistered target `2D<=1/1250000` with a margin of about 29.38. This is **uniform local closeness, not uniqueness**, and not whole-sequence convergence, translation invariance or a rate in `N`.
3. **First-order density (item 3).** The first-order density is `rho^(1)_R = (tau/72) sum_{f: M_f=R} (|W_f Omega_R><Omega_R| + h.c.)`. The sum runs over the ten omitted faces whose owner set is exactly `R`. The straddling first-order creations have zero `R`-marginal.
   - It is the same operator for every box of both families and for every subsequential limit.
   - Its trace norm is `sqrt(10)|tau|/72` (about `4.39205e-10`), and `Tr(rho^(1)_R W)=tau/144`, matching AW1.
   - The R-local second-order constant is `K_2' = 13417.5275439...` (exact rational in Section 5.5). Hence `||rho_R-rho'_R||_1 <= 2K_2' tau^2` (about `2.68350550879e-12`) for any two limits.
   - Compared with the AW1-admitted `K_2^+` (about `3354.80322946`), `K_2'` is **larger**, by a factor of about `3.9995`. A labelled orthogonal variant is larger by about `2.828`. The reason is that `K_2^+` bounds only the single observable `W`, whose overlap structure the full trace norm cannot use (Section 5.6).
4. **Mandatory sentence and gate fields (item 4).** Both are in Section 6 and are exported in `results.json`. The label is `uniform_local_closeness_not_uniqueness`.
5. **Controls (items 5–6).** All 21 contract controls are implemented as damaging mutations. So are the fixed-vector/moving-vector example and the "common enclosing interval is not equality" control. "Quantitative boundary comparison" is defined in Section 7.

**Checker.** `check.py` runs **42 exact checks**. All **21 contract controls** reject explicit damaging mutations, **97** in total. The `-B` and `-B -O` outputs are byte-identical.

**Proposed forward verdict: `accepted_within_scope` for the forward half, sub-label `uniform_local_closeness_not_uniqueness`.** The contract acceptance ("closeness inequality and the first-order density proved by both routes") also needs the reverse route and skeptical review, which are outside this producer's work.

## 1. Model, the two families, topologies and clock

**Model.** The model is fixed as in AV1/AW1. In normalized units,

\[
 h_b=8\sum_{e\in b}C_e\ \ge 6Q_b\ \ge Q_b,\qquad P_b=|1_b\rangle\langle1_b|\ (\text{Haar}),\qquad
 \phi_b=-\frac{\tau}{3}\sum_{f\in O_b}W_f,\qquad \|\phi_b\|=7|\tau| .
 \tag{HNM-AY1-F01}
\]

Here `O_b` is the set of the 21 omitted faces anchored at `b` (I1 table), and a face `f` has owner set `M_f` (I1.4). Every omitted face has `|M_f|>=2`, and `M_f` lies in `b+S` with `S={0,e_x,e_y,e_z}`. The pins, derived in `check.py` from the parsed I1 table, are:
- 49 faces per factor;
- 82 faces meeting `R`;
- 10 faces with `M_f=R`;
- 16 faces with `M_f ⊇ R`, of which 6 strictly contain `R`;
- 72 straddling faces meeting `R` (66 meeting `R` in one site);
- 33 faces per site of `R` that do not contain the other site.

A fine-lattice brute force, which does not use the table, confirms the 82 and the 10.

**The two named construction families** (read from the contract, `parameters.families`). Both use the centered coarse cubes `Lambda_N=[-N,N]^3` with `N>=2`:

\[
\begin{aligned}
 \text{F1 (AQ1):}\quad & \widehat H^{(1)}_N=\sum_{b\in\Lambda_N}h_b+\sum_{b+S\subset\Lambda_N}\phi_b ,\\
 \text{F2 (I1 §6):}\quad & \widehat H^{(2)}_N=\sum_{b\in\Lambda_N}h_b+\sum_{b\in\Lambda_N}\phi^{(\Lambda_N)}_b,\qquad
 \phi^{(B)}_b=-\frac{\tau}{3}\sum_{f\in O_b,\ M_f\subset B}W_f .
\end{aligned}
 \tag{HNM-AY1-F02}
\]

F2 keeps every omitted face whose *actual* support lies in the box, grouped at its anchor. The anchor is always in `M_f`, so no retained face has an anchor outside the box. I1 §6 pads to `B_+=union_{b in B}(b+S)` with the onsite `h_x` alone on `B_+\B`. Those sites carry no interaction, so the padded ground is `psi^(2)_N ⊗ Omega_pad`, and its `R`-density equals that of `H^(2)_N` on `Lambda_N`.

Coarse translation by `(N,N,N)` is the fine translation `(4N,2N,N)`, which preserves residues, face classes and owner sets (AV1 §1). It maps F2 on `Lambda_N` to I1's all-actual-support-contained prescription on an orthant box, literally.

The two families are compared face by face:
- F1 ⊂ F2 strictly. At `N=2` F1 has 1344 faces and F2 has 1960; at `N=3` they have 4536 and 5880.
- Both retain all 82 faces meeting `R` and the same 10 faces with `M_f=R`, for `N=2,3` and, by the geometry below, for every `N>=2`. The owner sets of faces meeting `R` lie in `[-1,1]^2×[-1,2]`, which is contained in `Lambda_2`.

**Topologies (item 1), named separately.**
- *States:* the **trace norm on `B(H_R)`**, that is, trace-norm convergence of reduced densities on the fixed finite region `R`. More generally it is local trace-norm convergence on fixed finite regions (the contract parameter).
- *Dynamics:* the **norm on compact time windows** (AQ1 §3, Nachtergaele–Sims), uniform on compact `theta` intervals for bounded local observables. It is named for completeness and used only as inherited for F1. **No dynamical statement is made for F2 limits**, and no boundary independence of the dynamics is claimed.

**Common clock.** The clock is `s=alpha t_E/hbar` and `theta=alpha t/hbar`, with `G=H/alpha`; the normalized `u=s/8` and exponent 24 are forbidden in packets (preregistration). The comparison in this loop is **static**: it compares finite-volume ground states and their limits at the same `tau`. Both families are evaluated at the same coupling, in the same unit convention (`delta=alpha/8`, face coefficient `-tau/3`), and with the same clock for any later dynamical use.

## 2. Item 1(a): F1 — the admitted chain, step by step

| step | statement used | source (hash-bound snapshot) |
|---|---|---|
| 1 | ownership, face supports (I1.4), whole stars `phi_b=-(tau/3) sum W_f`, `||phi_b||<=7|tau|` (I1.5) | I1 forward report §§2–4 |
| 2 | zero triple: `h_b=8 sum C_e>=6Q_b>=Q_b`, Haar `P_b`; `Lambda_N` is a relabelled translate of an I1 complete-factor volume | AV1 forward §1 (F01, F02) |
| 3 | AM2: `J<=28|tau|<=J_0=7/25000000` (four incident stars), `|X|<=4`, termination at order 8, `J_0G(R)<R`, `2J_0G'(R)<1`; nondegenerate ground, gap `>=1/2` per cutoff and untruncated (AM2 §6) | AM2 gate; AM2 forward (AM2.2–AM2.11) |
| 4 | AV1 tier (ii): product split `psi=psi_out+delta`, explicit density inequality `2eps(1+eps)/(1+eps^2)`, `eps=2T+T^2`, `T=t_1/(1-352J)`, `t_1=49|tau|/144`; cutoff-vector removal (Eckart, F20–F23); passage by local trace-norm convergence (F24) | AV1 gate; AV1 forward (F06–F24) |
| 5 | reset `C_F=56|tau||F|`, trace-norm compactness, diagonal extraction (AQ1.1–AQ1.2); `omega_N(h_R)<=98|tau|` (AQ2.8) | AQ1, AQ2 forward |
| 6 | norm dynamics on compact time windows (named only) | AQ1 §3 |
| 7 | `c^(1)=L_0=-(tau/72) sum_f W_f Omega_0`; amplitude lemma (F14); itemized remainder; first-order mean `+tau/144` | AW1 gate; AW1 forward (F02, F11–F15) |

`check.py` reads `D_ii`, `D_i`, the reverse refinement, `K_2^+`, `+tau/144`, the AW2 enclosure, `J_0`, `p=4`, the termination order, `R=1/64`, `G(R)<148/7`, `G'(R)<352`, `C_F=56|tau||F|` and `98|tau|` from the gate and report snapshots with regular expressions. It records the sha256 of every gate it reads. No admitted constant is typed in. For `N=2,3` it verifies that F1 retains all seven incident stars and that every retained group has 21 faces. Nothing is re-proved for F1.

## 3. Item 1(b): F2 — the padded all-contained-face family

### 3.1 AM2 hypotheses, verified for F2

AM2's proof (§§2–6) uses the interaction only through five hypotheses. I verify each for F2 at every `N`, not by analogy. `check.py` audits all five on the actual boxes `N=2,3`.

- **H1 (on-site).** `h_x=8 sum C_e`, as in F1: it is unchanged, `h_x>=Q_x`, it has the Haar vacuum, and it has compact resolvent.
- **H2 (grouping).** `V^(2)=sum_b phi_b^(Lambda_N)` is bounded and self-adjoint, and each retained face is charged exactly once, at its anchor. The group `phi_b^(Lambda_N)` acts on `X_b:=union{M_f: f in O_b, M_f ⊂ Lambda_N}`, which is contained in `(b+S) ∩ Lambda_N`.
- **H3 (support).** `|X_b|<=|S|=4=p`. AM2's counting uses `|X|<=p` only as an upper bound:
  - at most `2^{|X|}<=2^p` output sets;
  - `sum_{I∩X≠∅}||c_I||<=|X| ||c||_a<=p||c||_a`;
  - `|I_l|<=|M|+|X|<=(p+1)|M|`.

  Smaller supports are therefore covered. The checker also verifies that the majorant coefficients `2^p(2p)^k(1+k(p+1)/p)` are increasing in `p` for `p<=4`, `k<=8`. Termination at order `2p<=8`: a nested word with more than eight creations puts at least five on one side of `V_X`, all meeting a four-site set, and two of them overlap. The checker runs the exact four-site fixture (`ad_C^8(V)Omega=8!|1111>`, `ad_C^9(V)=0`) and a two-site fixture (`4!` at order 4, zero at order 5).
- **H4 (per-site sum).** If `u in X_b`, then `u in b+S`, so `b in u-S`: at most four anchors, incoming anchors included. Each group has at most 21 faces of norm `|tau|/3` (`||W_f||<=1`). Hence

\[
 J^{(2)}:=\max_u\sum_{b:\,u\in X_b}\|\phi^{(\Lambda_N)}_b\|\le 4\cdot 21\cdot\tfrac{|\tau|}{3}=28|\tau|\le J_0=\tfrac{7}{25000000}\quad(|\tau|\le10^{-8}),
 \tag{HNM-AY1-F03}
\]

  with equality at bulk sites (the enumerated maximum at `N=2,3` is exactly 28). A labelled remark, not used: grouping per face instead gives `49|tau|/3`.
- **H5 (cutoffs).** The volume is finite. Product spectral cutoffs `Q_L` commute with `H_0`, and they neither enlarge supports nor increase `J^(2)` (AM2 §6).

**Conclusion.** The AM2 constants depend only on `(p, J_0)`, so the same inequalities hold at the same `J_0`:

\[
 G(t)=16e^{8t}(1+10t),\ \ e^{1/8}<\tfrac87:\qquad J_0G(R)<\tfrac{148}{7}\cdot\tfrac{7}{25000000}=\tfrac{37}{6250000}<R=\tfrac1{64},\qquad
 2J_0G'(R)<2\cdot352\cdot\tfrac{7}{25000000}=\tfrac{77}{390625}<1 .
 \tag{HNM-AY1-F04}
\]

The checker evaluates the series enclosure `e^{1/8}<53823253862885575661009/47498854821020880076800<8/7` exactly. Consequently every F2 box, at every on-site cutoff, has:
- a fixed point `psi=e^{-C}Omega_0` with `c_I` in `⊗Q_xH_x` and `||c||_a<=1/64`;
- the majorant inequalities `||c||_a<=J G(||c||_a)` and `||c-L_0||_a<=J(G(||c||_a)-16)` (AV1 F05);
- a nondegenerate ground with full-space gap `>=1/2`.

AM2 §6 removes the cutoff verbatim: `h_x` is the same, and `V^(2)` is bounded in each box. So the untruncated `H^(2)_N` has a simple ground and `E_1-E_0>=1/2`. The ground is gauge invariant because every retained term is a Wilson loop. The damaging mutations rejected here:
- a merged two-anchor group with support 5;
- faces charged with norm 1 (`J=84|tau|>J_0`);
- a face charged in two groups;
- `J` computed from the outgoing star alone (`7|tau|`);
- the literal vertex boxes of I1 §7 relabelled as F2. Those boxes clip the on-site operator, so their reference is not Haar and they form another model.

### 3.2 The AV1 tier-(ii) inputs are identical for F2

- **The first-order coefficient.** `c^(1)=L_0=H_0^{-1}P_perp V^(2) Omega_0=-(tau/72) sum_{retained f} W_f Omega_0`. Each `W_f Omega_0` has energy 24 and norm `1/2`, and distinct faces share at most one link. The number of retained faces with `u in M_f` is at most the bulk 49, and the enumerated maximum is exactly 49. Hence `||c^(1)||_a<=t_1=49|tau|/144`.
- **The self-consistent tier.** With `J=28|tau|` it is unchanged:

\[
 T=\tfrac{t_1}{1-352J}=\tfrac{49}{14398580736},\qquad \rho:=352JT=\tfrac{3773}{11248891200000000},\qquad
 \varepsilon=2T+T^2=\tfrac{1411060914529}{207319127211110301696}\quad(\tau=\pm10^{-8}).
 \tag{HNM-AY1-F05}
\]

- **The inequality.** The AV1 product split (F06–F10), the explicit density (F11) and the inequality (F12) are algebraic consequences of H1–H4. So is the cutoff-vector removal (F20–F23), which uses the untruncated gap `1/2`; for `L>=24`, `Q_L c^(1)=c^(1)`. They therefore apply to F2 verbatim, and every F2 box `N>=2` satisfies

\[
 \|\rho^{(2)}_{N,R}-P_R\|_1\le D=\tfrac{2\varepsilon(1+\varepsilon)}{1+\varepsilon^2}
 =\tfrac{585079838465912592144137406066050}{42981220507576537932303142777593983768257}\approx1.36124528702\times10^{-8}.
 \tag{HNM-AY1-F06}
\]

The checker recomputes `D` from (F05) and requires equality with the AV1 gate's bound value.

### 3.3 Reset budget

The argument follows AQ1 §2 and AT4 F07. Reset the ground density on `R` to `P_R` and keep its exterior marginal. Onsite terms on `R` drop to 0. Terms not meeting `R` are unchanged; unbounded exterior energies cancel after bounded spectral truncation, as in AQ1. Each group meeting `R` changes by at most `2||group||`. The groups meeting `R` are exactly the seven anchors `R-S={0,-e_x,-e_y,-e_z,e_z,e_z-e_x,e_z-e_y}`, each with norm at most `7|tau|`. So

\[
 \omega^{(2)}_N(h_R)\le 2\cdot7\cdot7|\tau|=98|\tau|,\qquad \omega^{(2)}_N(h_F)\le 2\cdot4|F|\cdot7|\tau|=56|\tau||F| .
 \tag{HNM-AY1-F07}
\]

The enumeration at `N=2,3` gives exactly `98|tau|` for both families. A labelled refinement, not used: charging face by face gives `2·82·|tau|/3=164|tau|/3`. Rejected mutations: the two-anchor orthant reset (`28|tau|`), and group norms charged at 21 unscaled faces.

### 3.4 Local trace-norm compactness and subsequential limits

`h_F` has compact resolvent, and (F07) gives `Tr(rho_{N,F}(1-Q_{F,L}))<=C_F/L` with `Q_{F,L}=1_{[0,L]}(h_F)`. Purification gives `||rho-Q rho Q||_1<=sqrt(4w-3w^2)<=2 sqrt(C_F/L)`, where `w` is the tail mass. The checker verifies the exact rank-two identity on `psi=(3/5,4/5)`: the squared trace norm is `832/625=4w-3w^2`. So `{rho^(2)_{N,F}}_N` is trace-norm precompact for every finite `F`, and this is AQ1.2 verbatim. Diagonal extraction over the nested cubes then gives subsequences along which every local density of F2 converges in trace norm. The limits are compatible under partial trace, so they define locally normal states on the quasi-local algebra.

F2 subsequential limits therefore exist, and the object compared in item 2 is not empty. For F2 I construct no dynamics, no stationarity and no GNS generator. None is needed for the static comparison, and none is claimed.

## 4. Item 2: the closeness `2D`

Let `omega` and `omega'` be subsequential limits at the same `tau`: `omega` along boxes `N_k` of family `Fi`, and `omega'` along boxes `N'_k` of family `Fj`, where `i` and `j` may be equal. By (F06) for F2, and by AV1 (F23) for F1, every finite-volume density lies in the closed trace-norm ball of radius `D` around `P_R`. Trace-norm limits stay in closed balls, as in AV1 F24. Hence

\[
 \|\rho_R-\rho'_R\|_1\le\|\rho_R-P_R\|_1+\|P_R-\rho'_R\|_1\le 2D
 =\tfrac{1170159676931825184288274812132100}{42981220507576537932303142777593983768257}\approx2.72249057405\times10^{-8}\le\tfrac1{1250000}.
 \tag{HNM-AY1-F08}
\]

The margin to the target is about 29.38. The target `1/1250000` is read from the contract. For effects `0<=A<=1`, the difference is trace-zero, so `|omega(A)-omega'(A)|<=D`. `D` is increasing in `|tau|`: `D(tau)/D(tau/10)>1` and `D(tau)/D(tau/100)` is about `100.0098`. The cap values therefore bound every `|tau|<=10^-8`, at either sign. The `-tau` value is a replay of the same formula, not a second confirmation.

**Quantifiers and what is not claimed.** The statement is: every pair of subsequential limits of F1 and/or F2 at the same `tau` is `2D`-close on `R` in trace norm. This is **uniform local closeness, not uniqueness**. It is also not whole-sequence convergence, not translation invariance and not a rate in `N`; the proof uses only a bound that holds in every box, so no rate can come from it. The checker exhibits the triangle route's sharpness. The pure states `v_±=(cos phi, ±sin phi)`, with rational `cos phi=(1-m^2)/(1+m^2)` and `m=1/1000`, are each at distance `D_ex=2sin phi` from `P`, yet they are `2D_ex cos phi` apart. So two states that both satisfy the one-state bound may differ by nearly `2D`.

## 5. Item 3: the first-order reduced density

### 5.1 Derivation from the AW1-admitted `c^(1)`

With AV1's creation convention, `psi=e^{-C}Omega_0` and `<Omega_0,psi>=1`, and `c=c^(1)+(c-c^(1))` with `c^(1)=L_0=-(tau/72) sum_f W_f Omega_0` (AW1 F02). To first order,

\[
 |\psi\rangle\langle\psi|=|\Omega_0\rangle\langle\Omega_0|-\sum_I\big(|\hat c^{(1)}_I\Omega_0\rangle\langle\Omega_0|+\text{h.c.}\big)+O(\tau^2),\qquad \|\psi\|^2=1+O(\tau^2),
\]

because `<Omega_0,c_I>=0`. Take the `R`-marginal of `-(c^(1) Omega_0^* + h.c.)`.
- **Supports disjoint from `R`.** They contribute `<Omega_out, c_I>|Omega_R><Omega_R|=0`.
- **Straddling supports** (`I∩R≠∅`, `I⊄R`). `Tr_out|W_f Omega_0><Omega_0| = |<Omega_out|W_f Omega_0>><Omega_R|`. Every straddling face has at least one link owned outside `R`; the checker verifies this for all 72. Integrating that single spin-`1/2` link against the Haar vacuum gives `E[U]=0`, so the marginal vanishes. Restricting to "creations meeting `R`" is therefore the same as restricting to creations inside `R`.
- **Supports inside `R`.** They are `R` itself, `{0}` and `{e_z}`. The single-site first-order parts vanish (`c^(1)_{0}=c^(1)_{e_z}=0`), because no omitted face has a one-site owner set (I1 table).

Hence

\[
 \rho^{(1)}_R=-\big(|c^{(1)}_R\rangle\langle\Omega_R|+|\Omega_R\rangle\langle c^{(1)}_R|\big)
 =\frac{\tau}{72}\sum_{f:\,M_f=R}\big(|W_f\Omega_R\rangle\langle\Omega_R|+|\Omega_R\rangle\langle W_f\Omega_R|\big).
 \tag{HNM-AY1-F09}
\]

**The ten faces with `M_f=R`.** All are anchored at factor 0:
- the six xz faces `(r,s,0)`, `r=0,1,2`, `s=0,1`; `W` itself is xz `r=0`, `s=0`;
- the four yz faces `(r,0,0)`, `r=0,…,3`.

The coefficient `-tau/72` is the same in both unit systems: `-(tau/3)/24` normalized and `-(tau/24)/3` in `alpha` units. The mixed values `tau/576` and `tau/9` are rejected.

### 5.2 Explicit form, spectrum and checks against AW1

The ten faces pairwise share at most one link, so `<W_f Omega_R, W_g Omega_R>=delta_{fg}E[W^2]=delta_{fg}/4`. The Haar moments `E[W^n]=1,0,1/4,0,1/8,0,5/64,0,7/128` are computed two ways, by the Clebsch–Gordan count and by Weyl/Wallis. Also `<Omega_R,W_f Omega_R>=0`. With the orthonormal vectors `e_f=2W_fOmega_R`,

\[
 \rho^{(1)}_R=\frac{\tau}{144}\sum_{f:\,M_f=R}\big(|e_f\rangle\langle\Omega_R|+|\Omega_R\rangle\langle e_f|\big),
 \qquad (\rho^{(1)}_R)^3=\frac{10\tau^2}{144^2}\rho^{(1)}_R,\quad \operatorname{Tr}\rho^{(1)}_R=0,\quad \operatorname{Tr}(\rho^{(1)}_R)^2=\frac{2\cdot10\,\tau^2}{144^2}.
 \tag{HNM-AY1-F10}
\]

So `rho^(1)_R` has eigenvalues `±sqrt(10)|tau|/144` and 0 (nine-fold) on the span `{Omega_R, e_f}`, and vanishes elsewhere. Its trace norm is

`||rho^(1)_R||_1 = sqrt(10)|tau|/72`, with square `1/5184000000000000000` at the cap and directed upper bracket `52704627669473/120000000000000000000000` (about `4.39205230578e-10`).

It is self-adjoint, trace-zero and gauge invariant, and it is odd in `tau`. Consistency with AW1 and AV1:
- `Tr(rho^(1)_R W)=2(tau/144)<Omega_R|W|e_W>=tau/144`, the AW1 coefficient `+tau/144`. The sign follows from the AV1 convention and needs no reinterpretation of the contract display.
- `Tr(rho^(1)_R (W^2-1/4))=0`, by the parity rule (`E[W^2 W_f]=0` for every `f`, including `f=W`).
- `||rho^(1)_R||_1<=D`.

### 5.3 The same for every subsequential limit of either family

For every `N>=2`, both families retain exactly the same ten faces with `M_f=R`; the checker compares the four face lists for F1 and F2 at `N=2,3`. So `c^(1)_R`, and hence `rho^(1)_R`, is the **same operator** for every box of both families and every cutoff `L>=24`. For `L<24` it would be cut off, but the cutoff-vector removal takes `L→∞`. Write `rho^(1)_R=tau·rho_hat`, where `rho_hat` depends on no family, box, cutoff or subsequence.

With the uniform remainder bound of Section 5.5, every subsequential limit `omega_tau` of either family at every `|tau|<=10^-8` satisfies

\[
 \|\rho_R(\omega_\tau)-P_R-\tau\hat\rho\|_1\le K_2'\tau^2 .
 \tag{HNM-AY1-F11}
\]

Here `K_2'` is the cap value, and it bounds every smaller `|tau|` (monotonicity below). Hence, for **any** selection `tau ↦ omega_tau` of subsequential limits, even one that switches families with `tau`, the first-order coefficient of the `R`-density is `rho_hat`. This is a statement about a coefficient, not about states (Jung observation-map rule). Comparing limits at **opposite** signs is not allowed: `||rho^(1)_R(tau)-rho^(1)_R(-tau)||_1=sqrt(10)|tau|/36`, far above `2K_2' tau^2`. The `common_clock` control rejects this.

### 5.4 The exact `R`-marginal decomposition

This builds on AV1 (F07–F11). Put `n=||phi_out||`, `e=||delta||/n`, `xi=(1_R⊗<phi_out|)delta` and `sigma=Tr_out|delta><delta|`, so that

`rho_R=[P_R+(|xi><Omega_R|+h.c.)/n^2+sigma/n^2]/(1+e^2)`.

Sort `delta=-sum_{I∩R≠∅} ĉ_I psi_out + sum_{pairs} ĉ_I ĉ_J psi_out` by support. For `I ⊂ R`, `(1⊗<phi_out|)ĉ_I psi_out = n^2 (c_I ⊗ Omega_{R\I})`. With `c^(1)_{0}=c^(1)_{e_z}=0`, this gives `xi/n^2=-c^(1)_R+eta`, where

\[
 \eta=\underbrace{-(c-c^{(1)})_R-c_{\{0\}}\otimes\Omega_{e_z}-\Omega_0\otimes c_{\{e_z\}}}_{\eta_{\rm am2}}
 \ \underbrace{-\sum_{I\ \rm straddling}\frac{(1\otimes\langle\phi_{\rm out}|)\hat c_I\psi_{\rm out}}{n^2}}_{\eta_{\rm str}}
 \ +\underbrace{\sum_{\rm pairs}\frac{(1\otimes\langle\phi_{\rm out}|)\hat c_I\hat c_J\psi_{\rm out}}{n^2}}_{\eta_{\rm pair}} .
 \tag{HNM-AY1-F12}
\]

Exact algebra then gives

\[
 r_R:=\rho_R-P_R-\rho^{(1)}_R=\frac{(|\eta\rangle\langle\Omega_R|+\text{h.c.})+\sigma/n^2-e^2P_R}{1+e^2}
 +\frac{e^2}{1+e^2}\big(|c^{(1)}_R\rangle\langle\Omega_R|+\text{h.c.}\big).
 \tag{HNM-AY1-F13}
\]

The trace norm of each piece is computed exactly:
- `eta` is orthogonal to `Omega_R`, and `(|eta><Omega|+h.c.)^2=||eta||^2|Omega><Omega|+|eta><eta|`, so the first operator has trace norm `2||eta||`.
- `sigma>=0`, `P_R sigma=0` and `Tr sigma=d^2`, so `||sigma/n^2-e^2P_R||_1=2e^2`.
- The last operator has trace norm `2||c^(1)_R||<=20a`, where `a=|tau|/144` and `||c^(1)_R||=sqrt(10)a<=10a`.

**Exact finite audit.** A creation-algebra fixture, labelled `model_is_finite_graph:true` and `transfers_to_aq:false`, has two `R` sites of dimension 3, two outside sites and up to three decoupled spectators. It carries creations of every support type: inside, one-site, straddling at one site, strictly containing `R`, outside and pair. On it the checker verifies the following exactly:
- AV1 (F11), (F12) and (F13);
- the rank-two square identity;
- `P_R sigma=0` and `Tr sigma=d^2`;
- the three component bounds below, and the amplitude lemma at both outside sites;
- that `rho_R` is independent of the spectators, while the weights `Z` take four different values.

Four mutations are rejected:
- dropping `sigma`;
- dropping the straddling creations from `xi`;
- the numerator-only (unnormalized) weight, which is spectator dependent;
- dropping the two-creation term from `eta`.

### 5.5 The R-local constant `K_2'` (AW1 remainder items restricted to faces meeting `R`)

The components are bounded with the AW1 ingredients, each restricted to supports meeting `R`:
- **AM2 remainder.** `rho=352JT` bounds the anchored remainder at each site of `R`. Hence `||(c-c^(1))_R||+||c_{0}||<=rho` (site 0) and `||c_{e_z}||<=rho` (site `e_z`), so `||eta_am2||<=2rho`.
- **Straddling.** Take a straddling `I` and a site `u` in `I\R`. `c_I` is excited at `u`, so `<c_I|(v⊗phi_out)=<c_I|(v⊗(Q_u⊗1)phi_out)`. The amplitude lemma (AW1 F14) gives `||(Q_u⊗1)phi_out||<=t n<=T n`. So `||eta_str||<=T sum_{I straddling}||c_I||<=T(72a+2rho)`, where 72 is the number of straddling faces meeting `R`.
- **Pairs.** `||eta_pair||<=A_0A_{e_z}`, where `A_0=sum_{I∋0, e_z∉I}||c_I||<=33a+rho`, and the same at `e_z`.
- **Density.** `e<=epsilon_R:=82a+2rho+(33a+rho)^2`, where 82 is the number of faces meeting `R`. This is the reverse-AV1/AW1 R-pinned `epsilon`, admitted as valid in both gates.

Collecting these into (F13):

\[
 \|r_R\|_1\le \underbrace{4\rho}_{\rm am2\_remainder}+\underbrace{2T(72a+2\rho)}_{\rm straddling}+\underbrace{2(33a+\rho)^2}_{\rm two\_creation}
 +\underbrace{2\varepsilon_R^2}_{\rm density}+\underbrace{20a\,\varepsilon_R^2}_{\rm normalization\ (3rd\ order)}=:K_2'\tau^2 .
 \tag{HNM-AY1-F14}
\]

The bound holds uniformly in `N`, in the cutoff (`L>=24`) and in both families. It passes to the untruncated ground (AV1 F22) and to every subsequential limit (closed ball). At `tau=±10^-8`, with `epsilon_R=180161487949673694520081/31634388307359360000000000000000` (about `0.569512|tau|`), the items are:

| item | exact value `/tau^2` | preview | order |
|---|---|---|---|
| am2_remainder `4rho` | `94325000000/7030557` | `1.34164334347e4` | 2 |
| straddling `2T(72a+2rho)` | `538349237890625/1581719415367968` | `3.40356976502e-1` | 2 |
| two_creation `2(33a+rho)^2` | `166184094520081/1581719415367968` | `1.05065470465e-1` | 2 |
| density `2epsilon_R^2` | `32458161740240419840923214704314125168912246561/50036726179039729690656808980480000000000000000` | `6.48686759083e-1` | 2 |
| normalization `20a epsilon_R^2` | (in `results.json`) | `4.50476916030e-10` | 3 |
| **K_2'** | `966771578474926086618624139557778885954947547760216752246561/72052885697817210754545804931891200000000000000000000000` | **`1.34175275439e4`** | |

- **The binding.** Every item is tier (ii). It is built from `T` and `rho`, which the AV1 gate pins through `D`, and from the R-local pins 72, 33, 82 and 10, which are derived from the enumeration. A second code path recomputes each item directly from the pins and requires equality, which guards against the silent-undercount failure recorded in AW1 finding N8.
- **The only non-R-local inputs** are `T` and `rho`. They are anchored-norm maxima of the AM2 fixed point, uniform in `N`, exactly as in AW1.
- **A labelled variant.** `eta_am2` is a sum of three mutually orthogonal vectors (excited at both sites, at 0 only, at `e_z` only). This gives `||eta_am2||<=sqrt(2) rho` and `K_2'_orth<=683633828861684359276723400174122854120671707760216752246561/72052885697817210754545804931891200000000000000000000000` (about `9487.945`), using a directed upper bracket of `sqrt 2`.
- **Scaling.** `B(tau)/B(tau/100)` is about `10000.976`, which is quadratic. `K_2'(tau/10)` and `K_2'(tau/100)` do not exceed `K_2'(tau)`, so the cap value bounds all smaller `|tau|`.

### 5.6 Comparison with `K_2^+`

The AW1 gate binds `K_2^+=81108864767825329926713064490531229475390625/24176936535511801466930759024724079017984`, about `3354.80322946`. The checker reproduces it exactly from the AW1 skeptic itemization `[rho+T^2+T^2+eps^2+a eps^2]/tau^2` with `eps=2T+T^2`.

| quantity | value | what it bounds |
|---|---|---|
| `K_2^+` (AW1) | `3354.80322946` | `|omega(W)-tau/144|` for the one observable `W` |
| `K_2'` (headline, triangle) | `13417.5275439` (ratio `3.9994976`) | `||rho_R-P_R-rho^(1)_R||_1`, all of `B(H_R)` |
| `K_2'_orth` (labelled variant) | `9487.94517` (ratio `2.8281674`) | the same |

`K_2'` is **larger**, and the reason is structural. `W Omega_R` is excited at both sites of `R`, so `W` overlaps only `c_R`, with multiplier `2||W Omega_R||=1`; it annihilates the one-site remainders `c_{0}` and `c_{e_z}` and the 66 one-site straddling faces. The full trace norm has no such overlap structure: it pays the cross-term multiplier 2 on all three remainder components.

The R-local restriction does help where it can. `epsilon_R` (82 faces, `0.5695|tau|`) is below `2T+T^2` (98 face units, `0.6806|tau|`), and 72 and 33 replace the unpinned `T`. But the dominant item is the anchored AM2 remainder, which is not R-local: it is `rho/tau^2`, about `3354.108` in both. So restricting to faces meeting `R` cannot bring the trace-norm constant below the `W`-specific one.

Honest reading: the contract's parenthetical "(not the whole-box `K_2^+`)" is satisfied in that `K_2'` is built from R-local pins. But `K_2^+` is not a volume-dependent "whole-box" constant (it is uniform in `N`), and the R-local trace-norm constant is about 4 times larger, not smaller (Section 10, W1).

### 5.7 Second-order difference and a supplementary corollary

Since `rho^(1)_R` is common to all limits, (F11) gives, for any two subsequential limits of either family at the same `tau`,

\[
 \|\rho_R-\rho'_R\|_1\le 2K_2'\tau^2=\tfrac{966771578474926086618624139557778885954947547760216752246561}{360264428489086053772729024659456000000000000000000000000000000000000000}\approx2.68350550879\times10^{-12},
 \tag{HNM-AY1-F15}
\]

a factor of about `1.0145×10^4` below `2D`. This is the "agree to first order" part of the mandatory sentence, with `closeness_order=2`. It is still not equality, and it says nothing outside `R`.

**Supplementary corollary.** This is labelled, is not a contract target and is proposed for review only. The reverse triangle inequality applied to (F11) gives, for every subsequential limit of either family,

\[
 \tfrac{\sqrt{10}|\tau|}{72}-K_2'\tau^2\ \le\ \|\rho_R-P_R\|_1\ \le\ \tfrac{\sqrt{10}|\tau|}{72}+K_2'\tau^2,\qquad
 \text{i.e. in }[4.37863477824\times10^{-10},\,4.40546983333\times10^{-10}]\ \text{at the cap}.
 \tag{HNM-AY1-F16}
\]

The upper end is about 30.9 times below `D`: AV1's `epsilon` charges all 82 faces meeting `R` at first order, whereas only the ten inside faces survive the partial trace at first order. The lower end is a *lower* bound on `||rho_R-P_R||_1`, which the AV1 gate lists as not provided. Neither end is used anywhere in this loop. In particular the contract closeness is stated with the AV1-admitted `D`, and no other loop's constant is replaced.

## 6. Item 4: mandatory sentences and gate fields

**The Jung loop-2 template, verbatim, with the constant slot filled** (`check.py` reads the template from the snapshot and fills only the slot `<constant>(tau) [order ...]`):

> For every pair of subsequential limits `omega'`, `omega''` of the named families `F1`, `F2` at the same coupling `tau`, and for every `A` in `B(H_R)` with `||A|| <= 1` on the fixed cover `R`: `|omega'(A) - omega''(A)| <= 2D = 1170159676931825184288274812132100/42981220507576537932303142777593983768257` (about 2.72249057405e-8; order `tau^1`), and `<= 2K_2' tau^2 = 966771578474926086618624139557778885954947547760216752246561/360264428489086053772729024659456000000000000000000000000000000000000000` (about 2.68350550879e-12; order `tau^2` after subtracting the common first-order density `rho^(1)_R`). This is uniform local closeness on a fixed region at fixed coupling, inherited from a finite-volume bound that holds for every volume. It does not assert `omega' = omega''`, convergence of any whole sequence, translation invariance, boundary independence beyond `R`, or any rate in `N`; two states satisfying it may differ by the stated order on `R` and without bound elsewhere.

The constants: `F1` = centered whole-star boxes `Lambda_N` (AQ1), `F2` = all-contained-face boxes with padding (I1 §6), `R={0,e_z}`, `tau=±10^-8` (and every `|tau|<=10^-8`).

**The contract's preregistered template, verbatim,** followed by its constants (exported as `mandatory_sentence_contract_filled`):

> For every pair of subsequential limits of the named construction families F1 and F2 at the same coupling, on the fixed cover R and for the frozen observable class, the reduced densities satisfy ||rho_R - rho'_R||_1 <= 2D and agree to first order in tau; this does not assert equality of the states, whole-sequence convergence, translation invariance, boundary independence of the dynamics, or a rate in N.

Constants: F1 = centered whole-star boxes `Lambda_N` (AQ1); F2 = all-contained-face boxes with padding (I1 section 6); R = {0,e_z} (48 links, 36 endpoints); observable class `B(H_R)`; `tau = ±1/100000000` (and every `|tau| <= 1/100000000`); `2D = 1170159676931825184288274812132100/42981220507576537932303142777593983768257` (about `2.72249057405e-8`); first-order agreement `||rho_R - rho'_R||_1 <= 2K_2' tau^2` (about `2.68350550879e-12`).

**Gate fields exported in `results.json`.**
- `uniqueness_claimed: false`, `whole_sequence_claimed: false`, `rate_claimed: false`, `translation_invariance_claimed: false`, `boundary_independence_of_dynamics_claimed: false`.
- Jung's `rate_in_N_claimed: false` is exported as well.
- `states_compared: "all subsequential limits of F1 and F2 (every pair, same or different family, same tau)"`.
- `region: "R={0,e_z} fixed before production (complete cover of the original xz Wilson loop)"`.
- `topology: "trace norm on B(H_R)"`, plus `dynamics_topology_named: "norm on compact time windows (no dynamical statement)"`.
- `closeness_order: 2` (order 1 for `2D`, order 2 after the common `rho^(1)_R` cancels).
- `label: "uniform_local_closeness_not_uniqueness"`.

**Phrasing rule.** `check.py` scans this report and every exported sentence. It rejects `the AQ state`, `the thermodynamic limit`, and `unique` in a sentence without `not` (code spans, which quote contract text verbatim, are excluded). It also requires the phrase "a chosen subsequential". AQ1's state is a chosen subsequential limit of F1; every statement here holds for each such limit separately and does not identify them.

## 7. Item 6: quantitative boundary comparison; uniform in `N` is not uniform in `a`

**Definition.** In this loop a **quantitative boundary comparison** is the pair of the following two statements:
- (i) a **closeness bound**: `||rho_R-rho'_R||_1<=2D` for every pair of subsequential limits of the two named boundary prescriptions F1 and F2 at the same `tau`;
- (ii) a **matching first-order term**: the same `rho^(1)_R` for every such limit, with the second-order difference `<=2K_2' tau^2`.

It is **explicitly not a variational statement about which boundary condition the infinite-volume theory selects**. It compares no energies or free energies of the prescriptions and does not rank them. It does not say that either family's limits are ground states of a canonical infinite-volume Hamiltonian. It says nothing outside `R` or about the dynamics. A definition that claims a variational selection, or that drops the first-order term, is rejected by the checker.

**"Uniform in `N`" is not "uniform in `a`".** Every bound here is uniform in the box size `N` at **fixed lattice spacing `a`** and fixed `tau`. The AL1 dictionary (read through the AX1 gate) is `tau=96/g^4`, so `|tau|<=10^-8` means `g^4>=9.6×10^9`: extreme strong bare coupling. Already the AL1 bridge value `g^4=32` gives `tau=3`, far outside the cap, and any asymptotically free trajectory `g(a)→0` leaves the cap. The region `R` is two coarse factors, a `4a×2a×2a` fine block: fixed in lattice units, but shrinking in physical units as `a→0`. The checker rejects a claim of uniformity in `a`, and a reading of uniformity in `N` as a continuum statement.

## 8. Error ledger (preregistered terms)

| term | per limit | pair of limits | note |
|---|---|---|---|
| `state_boundary` | `D=585079838465912592144137406066050/42981220507576537932303142777593983768257` | `2D` (about `2.72249057405e-8`) | AV1 tier (ii), forward density route; uniform in `N`, cutoff and family |
| `second_order_difference` | `K_2' tau^2` (about `1.34175275439e-12`) | `2K_2' tau^2` (about `2.68350550879e-12`) | five items of (F14), added linearly |
| `arithmetic` | not applicable as a numeric cost | — | exact `Fraction`s throughout; directed upper brackets only for `sqrt 10` (the trace norm of `rho^(1)_R`) and `sqrt 2` (the labelled variant); the series enclosure `e^{1/8}<8/7` |

Deterministic terms add linearly. A root-sum-of-squares combination and division by `sqrt(N)` or by 64 are rejected.

## 9. Controls (items 5–6)

Each of the 21 contract controls is a check in `check.py` that rejects at least one damaging mutation through an explicit `AdmissionError`; nothing uses `assert`.

| control | damaging mutations rejected (check id) |
|---|---|
| `missing_incoming_stars` | the two-anchor orthant count; one star only; both families at `N=2,3` must give the 7 anchors `R-S` |
| `full_original_wilson_cover` | the four drawn links as the cover; a single-factor cover (48 links, 36 endpoints, 22+22 with 8 shared, owners `0,0,e_z,0`) |
| `wrong_delta_alpha_hbar_clock` | `tau/576` and `tau/9` (mixed units); exponent 24 in `s` (non-unit fixture `alpha=5`, `hbar=7`, `t_E=7/5`, `s=1`) |
| `vector_versus_scalar_centering` | scalar subtraction as vector centring (residues `1/10000`, `-51/10000`, `1/16`); centring imposed on the uncentered density (contract `centering: none`) |
| `first_order_mean_charged` | first-order density set to zero: contradicted because `omega(W)>=tau/144-K_2^+tau^2` (AW2 lower end) exceeds `K_2' tau^2`; `m^2<=D^2` stays charged |
| `tau_scaling_exponent` | square-root bound labelled linear; second order labelled first order; first order labelled second order (ratios: `D` about 100.0098, `K_2' tau^2` about 10000.976, `rho^(1)` squared exactly `10^4`, AT4 squared exactly 100) |
| `changed_model_relabelled` | `tau=10^-14`; a nonzero triple; the selected-strip reference; a finite-graph model id; the uniform route-B model (`J'=29|tau|`, AX1); literal vertex boxes as a family |
| `coherent_evidence_tampering` | with the packet hash rebound: a control Boolean flipped; the Jung snapshot removed; `2D` halved; `K_2'` quartered; `uniqueness_claimed` set true; one family only; a first-order face removed |
| `insufficient_verdict_retained` | a failed family relabelled accepted; a missing first-order density relabelled accepted; tier (i) retuned. Retained failures: `2D_i` about `4.73607e-5` and the AT4 `2·2sqrt(49|tau|/3)` about `1.61658e-3` both exceed `1/1250000` |
| `exact_arithmetic_admission` | float, bool, NaN and zero-denominator inputs |
| `root_n_misuse` | RSS of the two state terms; division by `sqrt(N)`; division by 64 |
| `no_priority_or_continuum_claim` | continuum, priority, uniform-Wilson or shift flag set true |
| `topology_named` | weak-* state topology; strong continuity relabelled norm; one topology for both; dynamics claimed for F2 limits |
| `two_families_named` | one family only; a third family (literal boxes); orthant boxes substituted |
| `subsequence_versus_whole_sequence` | whole-sequence convergence and a `1/N` rate claimed for an alternating sequence whose parity subsequences converge |
| `local_closeness_not_uniqueness` | `uniqueness_claimed`, `translation_invariance_claimed` or `boundary_independence_of_dynamics_claimed` set true; witness: two distinct states within `D_ex` of `P` |
| `common_clock` | F2's normalized coefficient read in `alpha` units (`8tau`); different couplings; opposite signs (first-order densities differ by `sqrt(10)|tau|/36`); a normalized clock for one family |
| `tier_mixing_rejected` | the tier-(i) value in the closeness; the reverse fidelity refinement under the density route (the density formula at the reverse `eps` exceeds it); the AT4 square-root bound labelled tier (ii); a crude item inside `K_2'`; `t=t_1` without the remainder |
| `reverse_premise_isolation` | declaration false; reverse inventory with the triage, the Jung note or the forward AY1 report |
| `padding_family_contraction_proved` | a support-five merged group; norm-one faces (`J=84|tau|`); a face in two groups; outgoing-star-only `J`; literal vertex boxes relabelled F2 |
| `not_uniform_in_a` | uniformity in `a` claimed; uniformity in `N` read as a continuum statement |

**The named item-5 examples, as separate checks.**
- `fixed_vector_versus_moving_vector_example` covers states and dynamics:
  - moving `|e_n><e_n|`: pairwise trace distance 2, weak limit 0, unbounded energy; claimed compact → rejected;
  - fixed `|e_1><e_1|`: converges;
  - `U(t)e_j=e^{ijt}e_j`, `Ae_j=e_{2j}`: the fixed vector `e_1` gives `<=4/n`, the moving `e_n` gives 2; strong continuity claimed as norm continuity → rejected.
- `common_enclosing_interval_not_equality`: two limits in the AW2 enclosure declared equal → rejected; two distinct states in the `D`-ball declared equal → rejected.

The phrasing rule of Section 6 is enforced in `mandatory_sentence_and_gate_fields`, which scans this report and the exported sentences.

**Controls that cannot be executed inside `check.py`, with reasons.**
- `reverse_premise_isolation` is only partly executable here. The declared inventories are checked: the forward inventory has 32 files, equal to AGENTS + contract + 28 shared + 2 forward-additional; the reverse list has 30 files and contains no forward-only premise. What the reverse agent actually reads is checked by `freeze.py` (reverse snapshot inventory) and by the skeptic.
- Freeze and byte-identical replays are protocol steps run by `research/round32/tools/freeze.py`, not by `check.py` itself.
- The post-comparison belongs to the skeptic, after both producers freeze.

**Source-edit audit (private scratch, not evidence).** Nine edits to a copy of `check.py`, and one to a copy of the contract snapshot, made in `/tmp/claude-0/ay1-forward-private/`, each abort at the intended check:
- `4rho` replaced by `2rho` in `K_2'`, the straddling count 72 replaced by 66, and the density item dropped: `second_order_K2prime_itemized`, through the second code path;
- the F2 rule replaced by the F1 rule, the per-site sum charged at a quarter of each group, and two straddling faces added to the first-order face list: `family_F2_padded_interaction`;
- the per-face coefficient `tau/576`: `first_order_density_explicit`;
- `uniqueness_claimed` set true, and `continuum_claim` set true: the gate-field and flag validators;
- the contract target edited to `1/125000`: the contract sha256 check, before any evaluation.

## 10. Contract wording findings (non-blocking)

- **W1.** Item 3's "(not the whole-box `K_2^+`)". `K_2^+` is uniform in `N`, not volume-dependent. It is an observable-specific bound, for `W` only. The R-local trace-norm `K_2'` is about 4.0 times larger (the orthogonal variant about 2.83 times), not smaller (Section 5.6). The requested comparison is reported as it comes out.
- **W2.** The contract's `claim_exclusions` and the preregistration's contain `uniqueness of the AQ state`. That uses the phrasing the Jung rule forbids (`the AQ state`). I quote it only verbatim, in code spans.
- **W3.** The gate-field names differ: the contract has `rate_claimed` and the Jung note has `rate_in_N_claimed`. Both are exported, as false.
- **W4.** The preregistered `state_provenance` names only the F1 construction (`AQ1_centered_whole_star_subsequence`), while the contract requires two families. F2's provenance is recorded here as the I1 §6 all-contained-face boxes on the same centered `Lambda_N`.
- **W5.** The contract does not fix F2's box geometry ("boxes"). I use the same centered `Lambda_N`. The bounds hold for any finite coarse region containing `R` (counts only decrease), and the first-order density needs only `R ⊂ B`.
- **W6.** Item 5 lists "freeze; byte-identical replays" as controls. They are not among the 21 control ids and are protocol steps (Section 9).
- **W7 (verified, no defect).** Item 3's sign `-(c^(1) Omega_0^* + h.c.)` is consistent with the AV1 creation convention and gives `+tau/144`. This is unlike AW1's item-3 display.

## 11. Exclusions, limitations and incomplete steps

**Contract exclusions (verbatim):** `uniqueness of the AQ state`; `whole-sequence convergence or a rate in N`; `translation invariance`; `continuum`; `scientific priority`.

**Preregistration exclusions (verbatim):** `free reference inside enclosure => no interaction claim`; `uniqueness of the AQ state`; `whole-sequence convergence or rate in N`; `continuum or weak coupling`; `transfer from a finite graph`; `relabelling a static shift as dynamical`; `scientific priority`.

**Additional exclusions on this route:**
- no dynamical statement for F2 limits;
- no boundary independence of the dynamics;
- not uniform in the lattice spacing `a`;
- no identification of limits with each other or with any canonical state.

**Limitations.**
1. **Scope.** Only the zero-selected patterned family, the cover `R`, fixed spacing and `|tau|<=10^-8`. Nothing transfers to nonzero selected triples (non-Haar `P_R`), to the uniform route-B model (its `K_2` was not transferred in AX1), to weak coupling or to the continuum. Only the two named families are covered. Literal vertex boxes (I1 §7, clipped on-site references), periodic boxes and other prescriptions are not.
2. **F2 via hypotheses.** For F2 the AM2 theorem is applied by verifying its hypotheses H1–H5 literally, with enumeration audits. The multilinear majorant and the exclusion argument are inherited, not re-proved line by line. The AX1 gate accepted the same `|X|<=4` monotonicity step.
3. **Inherited without re-proof:**
   - AM2's fixed point, majorant, gaps and §6 cutoff removal;
   - AV1's product split, density inequality, cutoff-vector removal and passage;
   - AQ1's compactness and diagonal extraction, and its dynamics (named only);
   - AW1's `c^(1)` and amplitude lemma;
   - the I1 dictionary.

   Peter–Weyl/Haar orthogonality and Nachtergaele–Sims are cited, not machine-checked.
4. **The constants are upper bounds**, except the labelled supplementary lower bound (F16). `K_2'` is conservative: its AM2-remainder item `4rho` is 99.99% of it.
5. **Correlation.** The mechanism of items 2 and 3 appears in the forward-only premises (the triage goal-4 note, and the Jung §3–4 notes on the coinciding first-order density). Independence is limited to derivations and code, and all agents are correlated model agents.
6. **Fixtures** are exact finite audits (`transfers_to_aq:false`), not proofs of infinite-volume statements.
7. **Scientific priority is unverified.**

**Methodological lenses (modern use of the snapshotted skills).**
- **Newton, analysis before synthesis.** The first-order density was obtained by analysing which creations survive the partial trace before any bound was written; the straddling marginals were shown to vanish, not assumed to.
- **Tesla, complete accounting.** Every channel of the `R`-marginal is charged with its tier: inside, one-site, straddling, strictly containing, pair, density and normalization.

No historical figure endorses anything here, and no historical or occult material supplies a premise.

## 12. Map of contract items and controls to proofs and checks

| contract item / control | report section | `check.py` check id(s) |
|---|---|---|
| 1 (F1 chain) | §2 | `family_F1_admitted_chain`, `premise_gates_and_reports_bound` |
| 1 (F2 contraction, supports, termination) | §3.1 | `family_F2_padded_interaction`, `padding_family_contraction_proved` |
| 1 (F2 tier-(ii) inputs) | §3.2 | `av1_tier_ii_bound_both_families` |
| 1 (reset) | §3.3 | `reset_budget_both_families` |
| 1 (compactness) | §3.4 | `trace_norm_compactness_both_families` |
| 1 (two topologies) | §1 | `topology_named`, `fixed_vector_versus_moving_vector_example` |
| 2 (closeness `2D`) | §4 | `closeness_2D_any_two_limits`, `subsequence_versus_whole_sequence`, `local_closeness_not_uniqueness`, `common_enclosing_interval_not_equality` |
| 3 (`rho^(1)_R` explicit) | §§5.1–5.2 | `first_order_density_explicit`, `first_order_marginal_straddling_zero` |
| 3 (same for all limits) | §5.3 | `first_order_density_family_independent` |
| 3 (decomposition) | §5.4 | `second_order_density_fixture` |
| 3 (`K_2'`, comparison with `K_2^+`) | §§5.5–5.6 | `second_order_K2prime_itemized` |
| 3 (`2K_2' tau^2`) | §5.7 | `second_order_difference_2K2prime` |
| 4 (sentences, gate fields, phrasing) | §6 | `mandatory_sentence_and_gate_fields` |
| 5 (controls; examples) | §9 | the 21 control ids; `fixed_vector_versus_moving_vector_example`; `common_enclosing_interval_not_equality` |
| 5 (freeze, replays) | §9, §13 | `freeze.py` |
| 6 (uniform in `N` vs `a`; definition) | §7 | `not_uniform_in_a`, `quantitative_boundary_comparison_defined` |
| preregistered error terms | §8 | `error_ledger_itemized` |
| contract binding | header | `contract_snapshot_sha256` |
| enumeration pins | §1 | `i1_table_parsed_and_geometry`, `face_enumeration_R_local`, `full_original_wilson_cover`, `missing_incoming_stars` |

## 13. Reproduction

```bash
python3 -B research/round32/forward/ay1/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/forward/ay1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round32/tools/freeze.py verify research/round32/forward/ay1
```

`check.py` verifies the contract sha256 before any evaluation and records its own sha256 before evaluation. It writes `results.json` (42 checks) and `source-manifest.json`, which records the sha256 of `check.py`, `report.md`, every `inputs/` file and `results.json`. AY1 is investigation 7 of 10 in Round32. This producer executed only the forward half of AY1.
