# Hruday route-B re-derivation for the uniform Kogut–Susskind SU(2) Hamiltonian at fixed spacing — AX1 forward

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production under the frozen AX1 contract (`research/round32/contracts/ax1.json`, sha256 `bc834eec4f5377041cea9db42a8674cf1f3de0a43b7fef3696a461a011da7d8d`). It is correlated model-agent work, not independent human review.

**What this producer read.**
- The contract snapshot first. After that, only files under `inputs/`:
  - **read in full:** AGENTS.md; `selection-ax1.md`; the AV1 and AW1 contracts; the AV1, AV2, AW1 and AW2 gates (the `bindings` blocks were not printed); the forward AV1 and AW1 reports; the AM2 forward report, the AM2 gate and `skeptic/am2.md`; the AQ1, AQ2, AT4 and I1 forward reports; the AL1 report and gate; `skeptic/aw1.md`; the three forward-additional premises (skeptic triage, skeptic loop-2 response, modern loop-2 response); the paired-physics SKILL and its complete-residual reference; the Newton and Tesla SKILL files;
  - **read in part:** `skeptic/av1.md` (a keyword scan for the forward findings N1–N6);
  - **not opened:** the AM2, AV1, AV2 and AW1 reverse reports, the AV2 forward report, `skeptic/av2.md`, the AV2 and AW2 contracts, the historical-panel skill and the Newton/Tesla reference notes.
- **Outside `inputs/`, for protocol and code style only:** `research/round32/tools/README.md`, `research/round32/tools/freeze.py` and parts of `research/round32/forward/av1/check.py`. I ran `wc -l` on `research/round32/forward/aw1/check.py` but did not read it. None of these carries premise weight.
- **Nothing under `research/round32/reverse/ax1/`**, no skeptic AX1 file and no other current AX1 work was read.
- **Scratchpad disclosure (sub-round 2 rule).** My scratch work is in `/tmp/claude-0/ax1-forward-private/`. It holds a float preview, a source-mutation harness and development runs; none of it is evidence. To create that folder I listed `/tmp/claude-0/`, and the listing showed other agents' folder names (among them `ax1-reverse-private` and `skeptic-ax1-private`). **I opened no file in any other scratchpad folder**, and no file in the shared session scratchpad root. The Claude harness saved copies of three of my own `inputs/` reads to its tool-results cache; those are my reads, not other agents' files.

**Shared premises.** The selection note, the contract itself and the forward-additional premises already state route B, the per-site sum `29|tau|`, the re-freeze `J_0'=29/10^8` with its two rationals, the reset budget `102|tau|`, the incidence `51|tau|/8`, and the candidate bounds 96 and 168. On the forward route these are **shared panel premises**. Independence is claimed only for the derivations, the enumeration, the constants and the code, and even there the work is correlated model-agent production. The creation-operator expansion, the centre-flip argument and Haar parity are established kinds of mathematics. The contribution here is their re-instantiation for the named model, with exact constants. Scientific priority is unverified. HNM labels are project aliases.

## Verdict (forward route)

All ten contract items are executed on the forward route. The model throughout is **uniform Kogut–Susskind SU(2) at fixed spacing, strong bare coupling** (`g^4=96/tau`, `g^4=9.6x10^9` at the cap), handled by route B (Haar reference, selected faces moved into the interaction).

1. **Dictionary and box.** `tau=96/g^4`. The uniform triple `tau/24` lies in the admitted box for every `|tau|<=3`, and `g^4=9.6x10^9` at the cap.
2. **Route-B grouping.** Each factor carries one whole star `phi_b` (norm `7|tau|`) and one single-factor group `psi_b` (norm at most `|tau|`). The per-site sum is `J'=28|tau|+|tau|=29|tau|`. The maximal support is four sites, nested commutators terminate at order eight, and no face is charged twice.
3. **Contraction.** `J_0'=29/10^8` is re-frozen, and the AM2 conditions hold as exact rationals: `J_0'G(R)<1073/175000000<1/64` and `2J_0'G'(R)<319/1562500<1`. Every finite route-B volume therefore has a unique ground and a full-space gap of at least `1/2` normalized (`alpha/16` physical). The ground is gauge invariant and the physical excited sector is nonzero.
4. **AQ1/AQ2 checklist.** Every step is re-instantiated (table in Section 4). Five steps need a new constant: reset `102|tau|` on `R` (`58|tau||F|` on a region `F`), `||Phi'||_F<=2349|tau|`, `epsilon_R<=17|tau|`, the variance floor and the dynamics slope `k'`. The variance floor `61999/250000` survives **only through the Haar gap six**. With the gap-one route, `2 sqrt(102|tau|)` exceeds `1/500` at the cap.
5. **Incidence (itemized).** Exactly seven stars and exactly two single-factor groups meet `R`. The two groups hold the six selected faces inside `R`. Hence `||B_N||<=51|tau|/8` and `k'=51|tau|/4` in `G=H/alpha` units. A face-by-face table is exported.
6. **State lemma.** The derived count is **52 faces per factor** (49 omitted plus 3 selected), not the contract candidate 96. The candidate is valid only as a labelled bound (`4x24`), and likewise 168 (`7x24`) against the exact **88 faces meeting R**. The two tiers give, at both signs:
   - **Tier (ii):** `D'_ii=2425369125199104794263242601250/167893028420061547330293754713793182097 ≈ 1.44459192142×10^-8`. This meets `4/10^7` with a margin of about 27.7.
   - **Tier (i):** `D'_i ≈ 2.45260902280×10^-5`. This fails the target and is retained.
   - The labelled 96-bound variant gives `2.66693895224×10^-8`, which reproduces the contract's "about 2–3×10^-8".
7. **Parity and coefficient transfer (item 9), proved.** Every face coefficient is tied to `tau`, so `U_E H_N(tau) U_E^*=H_N(-tau)` for the uniform model. The link grading applies verbatim to selected faces. `omega(W)^(1)=+tau/144` is unchanged, and only `f=W` contributes. Section 7 tabulates which AW1 quantifiers transfer.
8. **Checker.** `check.py` runs **52 exact checks**. All **28 contract controls** reject explicit damaging mutations, 94 in total. The `-B` and `-B -O` outputs are byte-identical.

**Proposed forward verdict: `accepted_within_scope` for the forward half.** The contract's acceptance clause also requires the reverse route and skeptical review, which are outside this producer's work.

## 1. Dictionary, box and label (item 1)

The AL1 dictionary (Bauer et al. convention, raw magnetic term `lambda sum_p(1-W_p)`, `W_p=(1/2)Tr U_p`) reads

\[
 \alpha=\frac{g^2}{2a},\qquad \lambda=\frac{2}{g^2a},\qquad \frac{\lambda}{\alpha}=\frac{4}{g^4},\qquad
 \nu=\lambda=\frac{\alpha\tau}{24}\ \Longrightarrow\ \tau=\frac{24\lambda}{\alpha}=\frac{96}{g^4}.
 \tag{HNM-AX1-F01}
\]

**Uniform model.** In the uniform Kogut–Susskind Hamiltonian every elementary face carries the same coefficient `nu`. This includes the three selected xy faces of every factor, so the selected triple in `alpha` units is `(lambda_L,mu,lambda_R)/alpha=(tau/24,tau/24,tau/24)`.

**Box check.** The admitted box is `|lambda_L|,|lambda_R|<=alpha/2` and `|mu|<=alpha/8`. Therefore

\[
 \frac{|\tau|}{24}\le\frac18\iff|\tau|\le3,\qquad
 \frac{|\tau|}{24}\Big|_{|\tau|=10^{-8}}=\frac{1}{2400000000},\qquad
 g^4\big|_{\tau=10^{-8}}=9.6\times10^{9}\ (g^2\approx9.80\times10^4).
 \tag{HNM-AX1-F02}
\]

The AL1 bridge condition `g^4>=32` holds with a factor of `3×10^8` to spare. The checker verifies the dictionary on three exact `(g^2,a)` fixtures. It rejects a non-uniform triple, the zero triple, `tau=4` (bridge `1/6>1/8`), and the normalized `tau/3` read as `alpha` units.

**Label.** The model is **uniform Kogut–Susskind SU(2) at fixed spacing, strong bare coupling** (`g^4=96/tau`). It is never described as weak coupling or as a continuum approach. The checker scans the label and verdict strings and rejects either phrase.

**Negative sign.** For real `g`, `tau=96/g^4>0`, so `tau=-10^-8` is **not a real-g dictionary point**. In the uniform model, `H_N(-tau)=U_E H_N(tau) U_E^*` (Section 7). The `-tau` evaluation is therefore the exact unitary mirror of the `+tau` model, not a second Kogut–Susskind coupling and not a second confirmation.

## 2. Route-B grouping (item 2)

**The 24 anchored classes.** Factor `b` owns the 24 positive links with tails `(4b_x+r,2b_y+s,b_z)`, `r=0..3`, `s=0,1`. Each factor anchors 24 face classes. The checker encodes them explicitly (8 rows, expanded to 24 classes) and re-derives every support from the fine geometry, using `supp_B(f)={pi(p),pi(p+e_a),pi(p+e_c)}` (I1.4):

| orientation, phase | count | relative support | route-B group |
|---|---:|---|---|
| xy, `r=0,1,2`, `s=0` | 3 | `{0}` | single-factor `psi_b` (selected) |
| xy, `r=0,1,2`, `s=1` | 3 | `{0,e_y}` | star `phi_b` |
| xy, `r=3`, `s=0` | 1 | `{0,e_x}` | star |
| xy, `r=3`, `s=1` | 1 | `{0,e_x,e_y}` | star |
| xz, `r=0,1,2`, `s=0,1` | 6 | `{0,e_z}` | star |
| xz, `r=3`, `s=0,1` | 2 | `{0,e_x,e_z}` | star |
| yz, `r=0..3`, `s=0` | 4 | `{0,e_z}` | star |
| yz, `r=0..3`, `s=1` | 4 | `{0,e_y,e_z}` | star |

In normalized units `delta=alpha/8`, every class enters with the same coefficient `-(nu/delta)W_f=-(tau/3)W_f` (the I1.5 sign convention). The route-B Hamiltonian on a centered box `Lambda_N=[-N,N]^3` is

\[
 \widehat H'_N=\sum_{b\in\Lambda_N}h_b+\sum_{b+S\subset\Lambda_N}\phi_b+\sum_{b\in\Lambda_N}\psi_b,\qquad
 h_b=8\sum_{e\in b}C_e,\quad
 \phi_b=-\frac{\tau}{3}\sum_{f\in O_b}W_f,\quad
 \psi_b=-\frac{\tau}{3}\sum_{g\in\mathrm{Sel}_b}W_g .
 \tag{HNM-AX1-F03}
\]

Here `S={0,e_x,e_y,e_z}`, `O_b` is the set of 21 omitted faces anchored at `b`, and `Sel_b` is the set of its three selected xy faces. Whole stars are retained as in AQ1. Every single-factor group of the box is retained, because its support `{b}` always lies inside the box.

**Norms and per-site sum.** `W_f=(1/2)Tr U_f` satisfies `|W_f|<=1`, so

\[
 \|\phi_b\|\le21\cdot\tfrac{|\tau|}{3}=7|\tau|,\qquad
 \|\psi_b\|\le3\cdot\tfrac{|\tau|}{3}=|\tau|,\qquad
 J'=\max_u\sum_{X\ni u}\|V_X\|\le4\cdot7|\tau|+1\cdot|\tau|=29|\tau| .
 \tag{HNM-AX1-F04}
\]

Both norm bounds are attained at the identity configuration. A site `u` lies in exactly four stars, those anchored at `u-S` (incoming stars included), and in exactly one single-factor group, `{u}`.

**No face is charged twice.** A face's anchor is `pi(base)`, which Euclidean division makes unique. The selected predicate (xy, `p_y` even, `p_x mod 4 in {0,1,2}`) then sends the face either to the star of its anchor or to that anchor's single-factor group, never to both. A fine-lattice brute force over 3600 plaquettes, in a region made of complete coarse blocks, puts every plaquette in exactly one group. Each group comes out complete, with 21 or 3 faces, and each face support lies inside its group's support. The damaging mutations are rejected: charging the selected faces in both the star and the single group (a duplicate face, per-site sum 33), dropping them (sum 28), and merging them into the star (sum 32).

**Support and termination.** The star support `b+S` has four sites and l1-diameter 2; the single-group support `{b}` has one site. For a group with support `X`, a nonzero nested word can have at most `|X|` creations meeting `X` on each side of `V_X`, because two creations meeting the same site multiply to zero. So `ad_C^k(V_X)=0` for `k>2|X|`, and the maximal order stays **eight**. The exact fixtures give:
- four qubits: `ad_C^8(V)Omega=8!|1111>` and `ad_C^9(V)=0`;
- one qubit: `ad_C^2(V)Omega=-2|1>` and `ad_C^3(V)=0`.

**Why AM2's majorant covers `|X|=1`.** AM2's constants have the form `2^p(2p)^k(1+k(p+1)/p)`, which is increasing in `p`. The value `p=4` gives `16·8^k(1+5k/4)`. Every step of AM2's multilinear estimate uses `|X|<=p` only as an upper bound: at most `2^{|X|}` output sets, `sum_{I cap X nonempty}||c_I||<=|X| ||c||_a`, and `|I_j|<=|M|+|X|`. So single-site groups satisfy (HNM-AM2.5) unchanged:

\[
 \|L_k(c_1,\ldots,c_k)\|_a\le J'\,16\cdot8^k\Big(1+\frac{5k}{4}\Big)\prod_j\|c_j\|_a .
 \tag{HNM-AX1-F05}
\]

## 3. Re-frozen contraction and the uniform finite-volume theorem (item 3)

The series `sum_{k<=12}(1/8)^k/k!` plus its geometric tail gives `exp(1/8)<53823253862885575661009/47498854821020880076800<8/7`. With `G(t)=16e^{8t}(1+10t)` and `G'(t)=16e^{8t}(18+80t)`,

\[
 G(\tfrac1{64})<16\cdot\tfrac87\cdot\tfrac{74}{64}=\tfrac{148}{7},\qquad
 G'(\tfrac1{64})<16\cdot\tfrac87\cdot\tfrac{77}{4}=352 .
 \tag{HNM-AX1-F06}
\]

At the cap, `J'=29·10^-8`, which exceeds AM2's frozen `J_0=7/25000000=28/10^8`, so the AM2 gate cannot be re-read. **Resolution R1** re-freezes `J_0'=29/10^8`, and the checker reads it from the hash-bound contract:

\[
 J_0'G(R)<\frac{29}{10^8}\cdot\frac{148}{7}=\frac{4292}{7\cdot10^8}=\frac{1073}{175000000}<\frac1{64},\qquad
 2J_0'G'(R)<2\cdot\frac{29}{10^8}\cdot352=\frac{20416}{10^8}=\frac{319}{1562500}<1 .
 \tag{HNM-AX1-F07}
\]

The Lipschitz constant satisfies `J_0'G'(R)<319/3125000`. The self-map inequality would allow `|tau|<=7/274688` (about `2548` times the cap), and the exclusion inequality would allow `|tau|<1/20416`. Resolution R2, capping `|tau|<=7/725000000=J_0/29`, is a changed coupling and is not selected; the `changed_model_relabelled` and `j0_resolution_declared` controls reject it under the cap label.

**On-site theorem.** Each Casimir `C_e` on `L^2(SU(2))` has spectrum `{j(j+1)}` on the Peter–Weyl blocks, and its kernel is the constants. So `h_b=8sum_e C_e>=0` has the one-dimensional kernel `Omega_b` (the Haar vector), and its next eigenvalue is `8·3/4=6`:

\[
 h_b\ge6\,Q_b\ge Q_b,\qquad P_b=|\Omega_b\rangle\langle\Omega_b|,\qquad Q_b=I-P_b .
 \tag{HNM-AX1-F08}
\]

**Theorem (route B, uniform model).** Take any nonempty finite complete-factor volume with route-B retention: whole stars `b+S` inside the volume, and every single-factor group. Take either sign with `|tau|<=10^-8`. Then:
- the full untruncated Hamiltonian has a unique ground `psi=e^{-C}Omega_0`, with `||c||_a<=1/64`;
- its full-space gap is at least `1/2` normalized;
- the ground is gauge invariant, and the physical subspace has a nonzero excited sector.

\[
 E_1-E_0\ge\tfrac12\ (\text{normalized}),\qquad \Delta_{\rm physical}\ge\frac{\alpha}{8}\cdot\frac12=\frac{\alpha}{16}.
 \tag{HNM-AX1-F09}
\]

*Proof.* This is AM2 Sections 2–6 with the new constants. It uses:
- `h_x>=Q_x` (F08);
- supports of at most four sites and termination at order eight (Section 2);
- `J<=J'<=J_0'` in every finite volume, since boundary per-site sums are at most the bulk value (checked for `N=1,2,3`);
- the self-map `J_0'G(R)<R`;
- Banach contraction with Lipschitz constant `J_0'G'(R)<1`;
- the shifted-resolvent exclusion `||b||_a<=2J_0'G'(R)||b||_a<||b||_a` for real `|z|<1/2`, from F07;
- continuity of the isolated branch from `s=0`.

AM2 Section 6 removes the cutoff, and it applies verbatim: `h_b` is a Casimir sum on a compact group with compact resolvent, and its gauge-commuting spectral projections give the form core.

*Gauge invariance.* Casimirs commute with left and right translations. `Omega_b` is constant, and each `W_f` is gauge invariant (checked on exact rational-quaternion holonomies for six faces, including `W` and selected faces). So the unique ground is fixed by the endpoint gauge group, and the physical subspace reduces `H`.

*Nonzero physical excited sector.* For a selected face `g` of any factor in the volume, `Omega_0` and `2W_gOmega_0` are orthonormal gauge-invariant vectors, because `E[W_g]=0` and `E[W_g^2]=1/4`. Hence `dim H_phys>=2` and `H_phys cap psi^perp≠{0}`, and on it the spectrum is at least `E_0+1/2`.

**Consistency with route A.** The uniform Hamiltonian is one operator however it is split. Its triple lies in the box, so the AM2 gate, with the selected-strip reference, already covers its gap. That coverage is an inherited cross-check, not a premise here. The state lemma below needs the **Haar** `P_R`, which only route B supplies.

## 4. AQ1/AQ2 re-instantiation checklist (item 4)

**Reset on the cover.** Reset the finite ground density on `R` to `P_R` and keep the exterior marginal. Every group meeting `R` then changes its expectation by at most twice its norm, and every other group is unchanged. Seven stars and two single-factor groups meet `R` (Section 5). Hence

\[
 \omega_N(h_R)\le2\big(7\cdot7|\tau|+2\cdot|\tau|\big)=102|\tau|,\qquad
 \epsilon_R=1-\operatorname{Tr}\rho_RP_R\le\frac{102|\tau|}{6}=17|\tau|,\qquad
 \|\rho_R-P_R\|_1\le2\sqrt{17|\tau|}.
 \tag{HNM-AX1-F10}
\]

At the cap the square-root bound is `2 sqrt(17/10^8)≈8.2462×10^-4`. It scales by exactly 10 under `tau->tau/100`, and it is used as a **square-root control only**: the admitted state term is the linear `D'` of Section 6.

**AQ1 constants.** On a finite region `F`, the groups meeting `F` are at most `4|F|` stars and `|F|` single-factor groups. With `F(r)=(1+r)^-4` and every group of l1-diameter at most 2,

\[
 C_F'=2(4\cdot7+1)|\tau||F|=58|\tau||F|,\qquad
 \|\Phi'\|_F\le F(2)^{-1}J'=81\cdot29|\tau|=2349|\tau|\quad(\|F\|\le7,\ \text{convolution}\le224\ \text{unchanged}).
 \tag{HNM-AX1-F11}
\]

**Variance floor.** AQ2 needs `||rho_R-P_R||_1<=1/500`. With the Haar gap six,

\[
 \big(2\sqrt{17\cdot10^{-8}}\big)^2=\frac{17}{25000000}\le\frac1{250000}\ \Longrightarrow\
 \operatorname{Var}_\omega(W)\ge\frac14-\frac1{500}-\frac1{250000}=\frac{61999}{250000},
 \qquad\text{while}\qquad \big(2\sqrt{102\cdot10^{-8}}\big)^2=\frac{51}{12500000}>\frac1{250000}.
 \tag{HNM-AX1-F12}
\]

So AQ2's verbatim argument, which used only `h_R>=I-P_R`, fails at `1/500` for route B, and the new constant (gap six) is required. The checker retains the gap-one failure as a control.

| step | status | constant |
|---|---|---|
| AQ1 reset energy on a region `F` | new constant | `58|tau||F|` (was `56`) |
| AQ1 trace-norm compactness, diagonal extraction | verbatim re-application | uses `C_F'` only |
| Nachtergaele–Sims placement (Section 3, Theorem 4.1) | new constant | `||Phi'||_F<=2349|tau|` (was `2268`); `||F||<=7`, `C<=224` unchanged; bounded single-site `Phi({b})` admitted |
| AQ1 stationarity | verbatim | none |
| AQ1 GNS strong continuity | verbatim | none |
| AQ1 nonnegativity of `H_num` | verbatim | none |
| AQ2 endpoint group, Haar projection, physical space | verbatim | gauge invariance of route-B `H` |
| AQ2 physical gap `alpha/16` (also full GNS) | verbatim, with the route-B full-Hilbert gap | `J_0'=29/10^8` (F07, F09) |
| reset on `R` (HNM-AQ2.8) | new constant | `102|tau|` (was `98`) |
| reset with the gap six (AT4 F08) | new constant | `epsilon_R<=17|tau|` (square-root control only) |
| Wilson variance floor (HNM-AQ2.10) | new constant (gap six required) | `61999/250000` via `2 sqrt(17|tau|)<=1/500` |
| reference moments `Tr(P_RW)=0`, `Tr(P_RW^2)=1/4` | verbatim | Haar `P_R` |
| AT4 relative-unitary slope | new constant | `||B_N||<=51|tau|/8`, `k'=51|tau|/4` |
| AV1 cutoff-vector removal | verbatim | selected face vectors also sit at energy 24; `L>=24` keeps `c^(1)` |
| AV1 passage to AQ subsequential limits | verbatim | local trace-norm convergence |

## 5. Incidence on the cover, itemized (items 5 and 10)

**All-size argument.** The Wilson loop `W=(1/2)Tr[U_{0,x}U_{e_x,z}U_{e_z,x}^{-1}U_{0,z}^{-1}]` has link owners `0,0,e_z,0`. Its cover `R={0,e_z}` has 48 links and 36 endpoints (22 per factor, 8 shared). By translation covariance:
- a star `b+S` meets `R` iff `b in R-S`, and `R-S={0,-e_x,-e_y,-e_z,e_z,e_z-e_x,e_z-e_y}`: seven anchors, all retained for `N>=2` (the farthest site needed is `2e_z`);
- a single-factor group `{b}` meets `R` iff `b in R`: exactly two groups.

The six selected faces inside `R` are the xy faces with fine bases `(0,0,0)`, `(1,0,0)`, `(2,0,0)` (factor 0) and `(0,0,1)`, `(1,0,1)`, `(2,0,1)` (factor `e_z`). All their links lie in the cover.

**Finite enumeration.** In `Lambda_N` the groups meeting `R` are 7 stars and 2 single-factor groups for `N=2,3,4`. For `N=1` only 4 stars appear, which is why the lemma requires `N>=2`.

| group | anchor | `R` sites met | faces in group | faces meeting `R` | norm |
|---|---|---|---:|---:|---|
| star | `0` | `0, e_z` | 21 | 21 | `7|tau|` |
| star | `e_z` | `e_z` | 21 | 21 | `7|tau|` |
| star | `-e_z` | `0` | 21 | 16 (every class containing `e_z`) | `7|tau|` |
| star | `-e_y` | `0` | 21 | 8 (classes containing `e_y`) | `7|tau|` |
| star | `e_z-e_y` | `e_z` | 21 | 8 | `7|tau|` |
| star | `-e_x` | `0` | 21 | 4 (classes containing `e_x`) | `7|tau|` |
| star | `e_z-e_x` | `e_z` | 21 | 4 | `7|tau|` |
| single `psi_0` | `0` | `0` | 3 (xy `r=0,1,2`, `s=0`) | 3 | `|tau|` |
| single `psi_{e_z}` | `e_z` | `e_z` | 3 (xy `r=0,1,2`, `s=0`) | 3 | `|tau|` |
| **total** | | | **153** | **88** (82 omitted + 6 selected) | |

`results.json` lists every one of the 153 faces with its class, fine base point, owner set and flags (`meets_R`, `inside_R`, `is_wilson_W`). Every total is recomputed from that table, never asserted. The `incidence_table_itemized` control rejects totals without the table, a table missing a single-factor group, and a table listing a group twice.

**Dynamics constant.** As in AT4, every group meeting `R` goes into `B_N` in full, so `A_N=G_{0,R}+G_outside` evolves `W` by the free Casimir generator on `R`. In `G=H/alpha` units (`V_X/8`, clock `theta=alpha t/hbar`):

\[
 \|B_N\|\le7\cdot\frac{7|\tau|}{8}+2\cdot\frac{|\tau|}{8}=\frac{51|\tau|}{8},\qquad
 k'=2\|B_N\|=\frac{51|\tau|}{4}.
 \tag{HNM-AX1-F13}
\]

**No double counting.** Each of the 153 faces appears once in the table. The faces anchored at `0` that also contain `e_z` belong to star `0` only, and the selected faces belong to the single-factor groups only. The per-site sum stays `29|tau|` (F04). The root-sum-of-squares of the nine group norms, `sqrt(345)/8`, is a rejected `root_n_misuse`.

## 6. State lemma for route B (item 6)

**Decomposition with the enlarged creation set.** AV1's product ordering applies verbatim to route B's AM2 creations. It uses only that the creations commute, that overlapping ones multiply to zero, and that `c_I in ⊗_{x in I}Q_xH_x` with Haar `P_x`. The creation set now includes single-site supports `{0}` and `{e_z}` that are **nonzero at first order**. They belong to `A={I: I cap R nonempty}`, and the pair `{0}×{e_z}` enters the two-creation term:

\[
 \psi=\psi_{\rm out}+\delta,\quad (P_R\otimes1)\psi=\psi_{\rm out},\quad
 \|\delta\|\le(2t+t^2)\|\psi_{\rm out}\|,\quad
 \|\rho_{N,R}-P_R\|_1\le D(t)=\frac{2\varepsilon(1+\varepsilon)}{1+\varepsilon^2},\ \ \varepsilon=2t+t^2,\ t=\|c\|_a .
 \tag{HNM-AX1-F14}
\]

**First order.** For every retained face `f`, omitted or selected:
- `W_fOmega_0` puts spin 1/2 on the four links of `f`;
- it lies in the sector `M_f` (its owner set);
- it has `H_0`-energy `8·4·3/4=24` and norm `1/2`;
- distinct faces share at most one link, checked over all pairs of the 88 faces meeting `R`, so their vectors are orthogonal.

A selected face has `M_g={b}`. Hence

\[
 c'^{(1)}_M=H_0^{-1}P_MV'\Omega_0=-\frac{\tau}{72}\sum_{f:\,M_f=M}W_f\Omega_0,\qquad
 \|c'^{(1)}_M\|=\frac{|\tau|\sqrt{n_M}}{144},\qquad \|c'^{(1)}_{\{b\}}\|=\frac{\sqrt3\,|\tau|}{144}.
 \tag{HNM-AX1-F15}
\]

**Per-factor count, derived from the 24-class encoding.** A face `(b,k)` has `u` in its owner set iff `b=u-d` with `d in K_k`. Summing over offsets:

\[
 \#\{f:u\in M_f\}=\sum_{d\in S}\#\{k\in\text{24 classes}:d\in K_k\}=24+4+8+16=52 .
 \tag{HNM-AX1-F16}
\]

Offset `0` lies in all 24 classes, and the selected classes contain only `0`. Further counts:
- there are **16 owner sets** containing `u`, with multiplicities `{1×5, 2×3, 3×3, 4×3, 10×2}`; relative to AV1's 15 sets, the new one is `{u}` with `n=3`;
- **faces meeting `R`:** `52+52-16=88`;
- **faces inside `R`:** 16 (10 omitted with owner set `R`, plus 6 selected);
- **faces containing `R`:** 16;
- **owner sets meeting `R`:** `16+16-3=29`.

Two cross-checks confirm these counts:
- the omitted-only sub-table reproduces AV1's `(49,15,82,10)`;
- a fine-lattice brute force without the class table reproduces 52, all 16 multiplicities and 88.

Counts in a finite box never exceed the bulk values; this is checked for `N=1,2,3`. The contract candidates **96** (`4 anchors x 24`) and **168** (`7 anchors x 24`) are valid only as labelled upper bounds. They overcount classes whose support misses the required offset. Using 96 as the exact count is a rejected mutation, and so are 49 (selected faces dropped) and 61 (selected faces counted at all four anchors).

**Anchored norm and the self-consistent remainder.** As in AV1 (F17–F18),

\[
 t_1'=\frac{|\tau|}{144}\max_u\sum_{M\ni u}\sqrt{n_M}\le\frac{52|\tau|}{144}=\frac{13|\tau|}{36},\qquad
 t\le\frac{t_1'}{1-352J'},\qquad \|c-c'^{(1)}\|_a\le J'(G(t)-16)\le352J't .
 \tag{HNM-AX1-F17}
\]

The grouped form bounds `sum_{M ni u} sqrt(n_M)=11+3sqrt2+3sqrt3+2sqrt10` by `26763348430167/10^12`, a directed upper bound. The crude tier uses `t<=J'G(R)` alone. Every component carries its tier label, and tier mixing is rejected.

**Values at `tau=±10^-8`.** Both signs are identical: the lemma depends on `|tau|`, and in the uniform model the `-tau` state is the `U_E` image, with `U_E P_R U_E^*=P_R`.

\[
\begin{aligned}
 &\text{tier (i):}\ t_i=\tfrac{1073}{175000000},\ \varepsilon_i=\tfrac{375551151329}{30625000000000000},\
 D'_i=\tfrac{23002790096235779074916932482}{937890625141038667264537458466241}\approx2.45260902280\times10^{-5};\\
 &\text{tier (ii):}\ t_1'=\tfrac{13}{3600000000},\ T'=\tfrac{13}{3599632512},\ \|c-c'^{(1)}\|_a\le\tfrac{4147}{11248851600000000},\
 \varepsilon'=\tfrac{93590445481}{12957354221447430144},\\
 &\qquad D'_{ii}=\tfrac{2425369125199104794263242601250}{167893028420061547330293754713793182097}\approx1.44459192142\times10^{-8}.
\end{aligned}
 \tag{HNM-AX1-F18}
\]

| tier / variant | `D'` at `tau=±10^-8` | `<=4/10^7` | `<=10^-6` |
|---|---|---|---|
| (i) one-step `t<=J'G(R)` | `2.45260902280e-5` | no (retained) | no |
| (i) iterated, `e^{8t}<=1/(1-8t)` | `1.85622638308e-5` | no | no |
| **(ii) `t_1'=52|tau|/144`** | **`1.44459192142e-8`** | **yes** (margin about 27.7) | yes |
| (ii) grouped sqrt | `7.43502245446e-9` | yes | yes |
| (ii) sharper remainder `288t/(1-8t)` | `1.44456511348e-8` | yes | yes |
| (ii) labelled bound `t_1=96|tau|/144` | `2.66693895224e-8` | yes | yes |

The contract's "candidate about 2–3×10^-8 from 96 faces per factor" is the labelled-bound row. The derived count gives the smaller headline.

**Consequences.** By trace duality, `|omega(W)|<=D'_ii`. By the effect refinement, `|omega(W^2)-1/4|<=D'_ii/2`, and `m^2<=D'_ii^2` is charged. The first-order mean `|tau|/144≈6.94×10^-11` lies below `D'_ii` (Section 7). The exact ratios `D'(10^-8)/D'(10^-10)` are about `100.0015` for tier (i) and `100.0101` for tier (ii), both in `[99,101]`, so both tiers are linear in `tau`; the square-root control has ratio exactly 10. The cutoff-vector removal (AV1 Section 7) and the passage to every AQ1 subsequential limit (AV1 Section 8) re-apply verbatim with the route-B gap. They give uniform local closeness only: not uniqueness, not whole-sequence convergence, not a rate in `N`.

**Arithmetic of the AX2 note (not the window lemma).** With a Machin `pi` bracket, `F(D)=2(D+D^2)+51|tau|/pi` at `|tau|=10^-8` satisfies:
- `F(D'_ii)<=1.9123×10^-7`, and `F(4/10^7)<=10^-6`;
- the exact threshold lies in `[4.188,4.189]×10^-7`.

The contract note "`D'<=4.19x10^-7`" is **rounded upward**, since `F(4.19×10^-7)>10^-6`. This is a non-blocking clerical finding: the target `4/10^7` sits below the true threshold. The crude `D'_i` is infeasible.

**Itemized error terms** (preregistered list):
- `am2_remainder`: `352J'T'=4147/11248851600000000` at tier (ii); not applicable at tier (i), which bounds the whole `c`.
- `two_creation`: `t^2`, which includes the first-order-nonzero pair `c_{0}⊗c_{e_z}`.
- `straddling`: inside the `2t` term; 72 first-order straddling faces (88 minus 16).
- `density`: `2eps^2/(1+eps^2)`.
- `onsite_cutoff_vector`: not a numeric cost; an exact limit in each box.
- `arithmetic`: not a numeric cost; exact Fractions with directed enclosures (`exp(1/8)<8/7`, `e^{8t}<=1/(1-8t)`, square-root brackets, Machin `pi`).

## 7. Parity and first-order transfer (items 7 and 9)

**Every coefficient is tied to `tau`.** In the uniform model the selected faces carry the same `nu=alpha tau/24` as the omitted faces (F01). In route B all 24 classes therefore enter as `-(tau/3)W_f`, and the selected coefficient, AW1's `kappa`, **equals `tau`**. A mixed convention is a rejected `uniform_sign_convention` mutation: selected faces with the opposite sign, with `tau/24` read in `delta` units, or with the zero triple.

**Flip identity (proved here, not cited).** Let `Pi_e psi(...,U_e,...)=psi(...,-U_e,...)`, and let `U_E=prod_{e in E cap Lambda}Pi_e` with `E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even}`. The following hold:
1. **`U_E` commutes with `H_0`, its cutoffs and the gauge actions.** `-1` is central, so `Pi_e` commutes with left and right translations. Hence it commutes with each `C_e`, with `h_b`, with every spectral cutoff `Q_L` of `h_b`, and with every endpoint gauge action. It also fixes `Omega_0`.
2. **Every plaquette meets `E` oddly.** `U_e` appears once in `W_f`, and `(-U)^{-1}=-U^{-1}`, so `Pi_e W_f Pi_e=(-1)^{[e in f]}W_f`. Take a plaquette with directions `a<c`. Each direction keys to the parity of the next coordinate cyclically (`x->p_y`, `y->p_z`, `z->p_x`). In each orientation one parallel pair differs in its keyed parity, so exactly one of its links lies in `E`. The other pair shares its keyed parity and contributes 0 or 2. So `|f cap E| in {1,3}`.
3. **Enumeration.** The checker covers:
   - all 24 (orientation, base-parity) classes;
   - all 24 anchored classes at 27 anchors (648 faces), the selected classes included;
   - all 3600 plaquettes of the fine region.

   The Wilson face meets `E` in 3 links, and exact rational-quaternion holonomies show the trace flips. The mutation removing one link of `E` is rejected.
4. **The identity.** Since every coefficient is linear in `tau` with one common sign,

\[
 U_E\,\widehat H'_N(\tau)\,U_E^*=\widehat H'_N(-\tau),\qquad U_E\,Q_L\widehat H'_NQ_L\,U_E^*=Q_L\widehat H'_N(-\tau)Q_L\quad(\text{every centered box, every cutoff}).
 \tag{HNM-AX1-F19}
\]

**Consequences.** The route-B AM2 ground is unique at both signs, `U_EOmega_0=Omega_0`, and the intermediate normalization is `<Omega_0,psi>=1`. Hence `e^{-C(-tau)}Omega_0=U_Ee^{-C(tau)}Omega_0` and, in every box,

\[
 \omega_{N,-\tau}(W)=-\omega_{N,\tau}(W),\qquad \omega_{N,-\tau}(W^2)=\omega_{N,\tau}(W^2),\qquad
 C_{N,-\tau}=C_{N,\tau},\ \ c_{N,-\tau}=c_{N,\tau},\qquad \rho_{N,R}(-\tau)=U_E\rho_{N,R}(\tau)U_E^* .
 \tag{HNM-AX1-F20}
\]

**Exact fixture.** The finite compression onto `{Omega_0, 2W Omega_0, 2W_g Omega_0}` takes `g` to be the selected face of factor 0 that shares the link `(0,x)` with `W`. Its entries come from Haar moments and link parity: `H=[[0,-tau/6,-kappa/6],[-tau/6,24,0],[-kappa/6,0,24]]`, and `U_E` acts as `diag(1,-1,-1)`. The compression satisfies `D H(tau,kappa) D=H(-tau,-kappa)`. With `kappa=tau` this is `H(tau)->H(-tau)`. The `uniform_kappa_tied_to_tau` control rejects the claimed uniform identity for `kappa=tau+1/1000`, for `kappa=1/100` and for `kappa=2tau+1/50`: a coefficient not tied to `tau` breaks the uniform flip identity. This is a finite compression, an audit of the algebra only.

**Link grading on selected faces.** Each `W_g` is a single spin-1/2 face character, so AW1's grading (F04: a Haar integral of products of spin-1/2 matrix elements vanishes unless every link occurs an even number of times) applies **verbatim**. For every selected `g` meeting `R`:

\[
 E[W\,W_g]=0,\qquad E[W^2W_g]=0,\qquad E[W^3]=0,\qquad
 H_0\text{-energies of }W_gW\Omega_0\in\{36,48,52\}\not\ni24,\qquad |g\triangle h|\in\{0,6,8\}.
 \tag{HNM-AX1-F21}
\]

In particular `P_24V'WOmega_0=0` still holds with the selected faces included, and the gauge-invariant multiplet splitting is still zero, since `E[W_gW_fW_h]=0` for all plaquettes.

**First-order coefficient.** The first-order vector is `psi^(1)=-H_0^{-1}P_perp V'Omega_0=(tau/72) sum_f W_fOmega_0`, summed over all retained faces, omitted and selected. By Kato analyticity (bounded `V'`, simple isolated ground with gap at least `1/2` from F09), in every box,

\[
 \omega_{N,\tau}(W)=2\langle W\Omega_0,\psi^{(1)}\rangle+O_N(\tau^2)=\frac{\tau}{36}\sum_fE[WW_f]=\frac{\tau}{36}\cdot\frac14=+\frac{\tau}{144}.
 \tag{HNM-AX1-F22}
\]

- **Only `f=W` contributes.** This is checked face by face over the 88 faces meeting `R`. The two selected faces that share a link with `W` contribute exactly 0.
- **The compression agrees.** Rayleigh–Schrödinger on the fixture reproduces `1/144`, with the `W_g` direction contributing 0.
- **Product-split reading.** Only `c_R` overlaps `W Omega_R`. Its first-order part is unchanged, because the 10 faces with owner set `R` are all omitted. The new single-site creations `c_{0}` and `c_{e_z}` are orthogonal to `W Omega_R`, because `W` carries one spin-1/2 factor on a link of each site (AW1's single-component overlap, verbatim).
- **Values.** `omega^(1)=±1/14400000000` at `tau=±10^-8`.

Charging the selected faces at first order is a rejected mutation.

**Which AW1 quantifiers transfer.**

| AW1 statement | uniform route B | needs |
|---|---|---|
| per-link grading `Pi_e`; commutes with Casimirs, gauge actions and cutoffs; fixes `Omega_0` | verbatim | none |
| `E` meets every plaquette in 1 or 3 links | verbatim (selected classes enumerated) | none |
| `U_E H_N(tau,kappa)U_E^*=H_N(-tau,-kappa)` | becomes `H_N(tau)->H_N(-tau)`, because `kappa` is tied to `tau` | none |
| cutoff compressions `Q_L->Q_L'` | simpler: route-B on-site is `kappa`-independent, so `Q_L'=Q_L` | none |
| finite-box ground covariance; `omega_N(W)` odd; `omega_N(W^2)`, `C_N`, `c_N` even | transfers | unique ground at both signs: route-B AM2 with `J_0'` |
| AQ passage `S(-tau)=S(tau) o alpha_E` (whole sets; pointwise only along a common subsequence) | transfers | route-B AQ1 constants `58|tau||F|` and `2349|tau|` |
| parity theorem, first-order vanishing for `omega(W^2)`, `c_N`, `C_N` (finite boxes, Kato; `tau^2` constant for `C` unbounded) | transfers (all plaquettes, selected included) | route-B box gap |
| `omega_tau(W)=+tau/144+r(tau)`, only `f=W` | transfers | none for the coefficient |
| `|r(tau)|<=K_2^+tau^2` uniformly in `N` | **not transferred** | route-B `T'`, `rho'`, `eps'`, plus the new pins (36 single-site faces per site of `R` instead of 33; 88 faces meeting `R`); not computed here |
| uniform `omega(W^2)` constant `K_W2` | **not transferred** | route-B constants; AW1's step "first-order parts of `c_{0}`, `c_{e_z}` vanish" is false in route B |

AW1's remark about a modified flip set `E*` is not needed: in the uniform model `kappa` is tied to `tau`, and `U_E` alone suffices.

## 8. Controls (item 7 of the contract; task item 9)

`check.py --output <absolute fresh dir>` uses only the standard library. It:
- verifies the contract snapshot's sha256 before parsing;
- reads the target `1/2500000` and every candidate constant from the contract (`J_0'`, the two rationals, the reset, the incidence, the bounds 96 and 168, the dictionary, the AX2 note);
- records its own sha256 before any evaluation;
- derives every count from the explicit 24-class encoding;
- writes `results.json` (sorted keys, no floats) and `source-manifest.json`.

Its 52 checks include all 28 contract controls. **Every control rejects at least one explicit damaging mutation through an exception** (94 in total, listed per check in `results.json`). No check uses `assert`, so all of them stay active under `-O`.

| control | damaging mutations rejected |
|---|---|
| `uniform_triple_in_box` | `tau=4` outside the bridge box; a non-uniform triple; the zero triple; `tau/3` read as `alpha` units |
| `selected_reference_not_haar` | the route-A fixture (selected face on-site, `kappa=30`, exact ground `-1`) has reference correlation of mass `25/104` and frequency `25/8`, not `e^{3i theta}/4`; claiming the Haar correlation there is rejected. For every `kappa≠0` the reference block has negative determinant `-kappa^2/36`, and the AT4 trial energy at the uniform cap is `-1/69120000000000000000·alpha` |
| `reference_route_declared` | route A; a selected-strip reference; budget `98`; `J=28`; a strip on-site; an undeclared `J_0` resolution |
| `per_site_sum_recomputed` | 28 (selected groups dropped); 8 (outgoing only); 33 (double counted); 32 (merged into stars) |
| `reset_budget_recomputed` | 98; 112 (single groups at all seven anchors); orthant two stars; the gap-one budget read as 17 |
| `selected_incidence_count` | selected groups forgotten; faces counted as groups; single groups at the star anchors |
| `first_order_faces_uniform` | 49 (omitted only); 96 used as exact; 61 |
| `uniform_label_strong_coupling` | a "weak coupling" label; a "continuum" regime; "fixed spacing" missing; "continuum" in the verdict |
| `am2_gap_reuse_justified` | the old `J_0=7/25000000`; a support-five grouping; a degenerate reference; `J_0=1/1000` (contraction fails) |
| `j0_resolution_declared` | the old `J_0` at the cap; resolution missing; R2 under the cap label |
| `uniform_sign_convention` | selected faces with the opposite sign; with `tau/24` in `delta` units; with zero |
| `tier_mixing_rejected` | exact `c^(1)` with the crude `t`; `t=t_1`; a zero remainder |
| `reverse_premise_isolation` | declaration false; reverse reads the triage; reverse reads forward AX1 (plus a positive check that the contract declares isolation and the forward inventory equals its declared list, 41 files) |
| `uniform_kappa_tied_to_tau` | `kappa=tau+1/1000`; `kappa=1/100`; `kappa=2tau+1/50` |
| `route_b_no_double_count` | selected faces in both a star and a single group; selected faces dropped |
| `incidence_table_itemized` | totals without the table; a group missing; a group listed twice |
| `missing_incoming_stars` | the orthant two-anchor count; outgoing-only `J=8|tau|`; a group count without the selected groups (7 instead of 9) |
| `full_original_wilson_cover` | the four drawn links (48 links, 36 endpoints, selected faces inside the cover) |
| `wrong_delta_alpha_hbar_clock` | `tau/576`; `tau/9`; exponent 24 with `s`; `k'` with the normalized clock (non-unit fixture `alpha=5`, `hbar=7`) |
| `vector_versus_scalar_centering` | scalar subtraction used as vector centring (`1/10000` versus `-51/10000`) |
| `first_order_mean_charged` | a zero first-order mean in the uniform model; `m^2` dropped |
| `tau_scaling_exponent` | the square root relabelled linear; linear read as square root |
| `changed_model_relabelled` | `tau=10^-14`; the R2 cap; the zero triple; a strip reference; a finite-graph id; a finite-volume provenance |
| `coherent_evidence_tampering` | a control Boolean, a snapshot, `D'_ii`, the `J_0'` self-map rational, the incidence table or a continuum flag changed with the packet hash rebound |
| `insufficient_verdict_retained` | tier (i) retuned to a smaller `tau`; tier (i) reported as passing |
| `exact_arithmetic_admission` | float, bool, `NaN` and zero-denominator inputs; no numerical-library imports |
| `root_n_misuse` | RSS of the nine group norms; division by `sqrt 9`; division by 64 |
| `no_priority_or_continuum_claim` | continuum, weak-coupling, priority, shift or Euclidean-node flags true; `uniform_wilson_claim` without the fixed-spacing label |

The 24 non-control checks are:
- binding and model: `contract_snapshot_sha256`, `dictionary_and_box`;
- grouping and contraction: `anchored_classes_match_fine_geometry`, `route_b_grouping_and_norms`, `brute_force_group_partition`, `am2_contraction_refrozen`, `nested_termination_fixtures`, `onsite_theorem_gauge_and_excited_sector`, `uniform_finite_volume_theorem`;
- incidence and re-instantiation: `incidence_all_sizes`, `aq_reinstantiation_checklist`;
- enumeration: `per_factor_face_count_derived`, `boundary_counts_at_most_bulk`, `face_vectors_energy_norm_orthogonality`;
- state lemma: `state_lemma_tier_i`, `state_lemma_tier_ii`, `state_lemma_variants`, `ax2_feasibility_arithmetic`;
- parity and transfer: `flip_set_odd_all_classes`, `uniform_flip_identity`, `first_order_coefficient_uniform`, `parity_rule_selected_faces`, `aw1_quantifier_transfer`;
- ledger: `error_ledger_itemized`.

The `J_0'` resolution packet pins `J_0'=29/100000000`, `1073/175000000` and `319/1562500` together with the contract sha256 (item 10).

**Source-edit audit (private scratch, not evidence).** Twelve edits to a copy of `check.py` each abort at the intended check. The edits were:
- deleting the selected row, or relabelling it omitted;
- changing the coefficient to `-1/4`;
- setting single groups per site to 0;
- zeroing the remainder;
- restricting the anchors to the orthant;
- dropping `8/7` from `G(R)`;
- a weak-coupling label;
- `continuum_claim:true`;
- on-site gap 1;
- charging selected faces at first order;
- changing the flip set.

**Claim flags:**
- `continuum_claim:false`;
- `uniform_wilson_claim:true`, for the fixed-spacing model as labelled only;
- `weak_coupling_claim:false`;
- `resolved_interaction_shift:false`;
- `scientific_priority_verified:false`;
- `euclidean_node_certified:false`.

The packet also sets `uniqueness_claimed`, `whole_sequence_convergence_claimed`, `rate_in_N_claimed`, `k2_uniform_claimed` and `wilson_mean_sign_certified` false.

## 9. Scope, limitations, incomplete steps and reproduction

**Claim exclusions, verbatim from the contract:**
- weak coupling or continuum
- a uniform-model Euclidean datum (AX2)
- a uniform Wilson-mean sign certificate
- AQ uniqueness or a rate in N
- scientific priority

**Preregistration claim exclusions, verbatim:**
- free reference inside enclosure => no interaction claim
- uniqueness of the AQ state
- whole-sequence convergence or rate in N
- continuum or weak coupling
- transfer from a finite graph
- relabelling a static shift as dynamical
- scientific priority

**Limits of this producer's evidence:**
1. **Forward half only.** The reverse route and skeptical review are outside this producer. The contract's `accepted_within_scope` needs both routes.
2. **Model scope.**
   - The model is the uniform Kogut–Susskind SU(2) Hamiltonian at fixed spacing and strong bare coupling (`g^4>=9.6×10^9`), with the whole-star-plus-single-group boundary prescription on centered boxes.
   - Bulk coefficients are uniform. Finite boxes drop the non-whole stars at the boundary. This is not identified with the all-contained-plaquette boundary (AL1); no boundary-state identification is claimed.
   - `tau<0` has no real `g`; it is the `U_E` mirror.
3. **Inherited without re-proof, and applied with the new constants.** These are:
   - AM2's multilinear majorant, fixed point, exclusion and cutoff-removal arguments;
   - AV1's product split, cutoff-vector removal and AQ passage;
   - AQ1's compactness, the Nachtergaele–Sims dynamics and GNS construction;
   - AQ2's gauge averaging and Fourier gap passage;
   - AT4's reset and relative-unitary arguments;
   - the I1 dictionary; AW1's character-multiplicity rule.

   Kato perturbation theory, Peter–Weyl and Nachtergaele–Sims are cited, not machine-checked. The checklist states the constant each step needs.
4. **Upper certificates only.** Nothing lower-bounds `||rho_R-P_R||_1`. No value or sign of `omega(W)` beyond `|omega(W)|<=D'` and the finite-box first-order coefficient is claimed. The uniform-in-`N` `K_2` is **not** computed for route B (see the transfer table).
5. **Fixtures are exact finite audits.** These are the 3×3 compressions, the qubit termination fixtures, the quaternion holonomies and the route-A `kappa=30` compression (outside the box, algebra only). None of them is a proof of an infinite-volume statement.
6. **Findings for the reviewer (non-blocking).**
   - (a) The contract's "96 per factor" and "168 for R" are labelled bounds. The exact counts are 52 and 88.
   - (b) The note "`D'<=4.19x10^-7`" is rounded upward (true threshold `[4.188,4.189]×10^-7`).
   - (c) AQ2's `1/500` does not survive the gap-one reset in route B; it needs the gap six.
   - (d) Item 8 asks the reverse producer to find route B and the `J_0` issue itself. But the shared premise `selection-ax1.md`, the contract text and its `J0_resolution` parameter state both. Reverse independence can therefore extend only to derivations and code.
   - (e) Tier (i) fails `4/10^7` and `10^-6`. It is retained and not retuned.

**Methodological lenses.**
- **Newton, analysis before synthesis.** The uniform Hamiltonian is analysed into its 24 classes and two group types before any constant is synthesized, and the synthesis is tested by breaking it: double counting, dropped groups, the gap-one reset, `kappa` untied.
- **Tesla, complete accounting.** All nine groups meeting `R` are charged in the reset and dynamics loads, the 153 faces are itemized, and every tier and error term is named.

These are modern methodological uses of the snapshotted skills. They carry no historical endorsement, and no historical or occult material supplies a premise.

**Reproduce** (fresh absolute output directories outside the checkout):

```bash
python3 -B research/round32/forward/ax1/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/forward/ax1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round32/tools/freeze.py verify research/round32/forward/ax1
```
