# Hruday exact finite-graph first- and second-order Wilson coefficients on the two-plaquette graph — AZ2 forward (single producer)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production (a Claude model agent) under the frozen AZ2 contract (`research/round32/contracts/az2.json`, sha256 `2861d5c59841b5b8e688712aab4faf3edf9f9f8ee2079d8ebbda07fabb7461c3`). AZ2 is a **single+skeptic** loop (investigation 10 of 10): this is the only producer. Admission also needs the skeptic's pre-comparison replay from the contract alone and the post-comparison review. No file under `research/round32/skeptic/` was opened. This is correlated model-agent work, not independent human review.

**What this producer read.**
- **The contract snapshot first.** After that, only files under `inputs/`, all 28 of them in full: AGENTS.md; `selection-az2.md`; the Round11 README, advisor report, solver README and `two_plaquette.py`; the modern-lens `update-4.md`, `loop2-response.md` and `loop3-signoff.md`; the AW1 gate and AW1 forward report; the complete-residual reference note; the AT4, I1, AM2 (forward and reverse), AQ1 and AQ2 reports; the AM2 gate and `skeptic/am2.md`; the four snapshotted method SKILL files and their three reference notes.
- **Outside `inputs/`, for protocol and code style only:** `research/round32/tools/README.md`, `research/round32/tools/freeze.py`, most of `research/round32/forward/ay2/check.py`, and the header and scratch-disclosure passages of `research/round32/forward/ax2/report.md`. I listed `forward/ax2/` and `forward/ay2/` and took their line counts, but did not open `ax2/check.py` or `ay2/report.md`. None of these carries premise weight. The repository `CLAUDE.md` was in my session context; it is non-scientific.
- **Not read:** anything under `research/round32/skeptic/`, `research/round32/forward/az1/`, the advisor deliberation or panel files, `research/round32/experts/` beyond the snapshots, the modern assistant-4 package that `update-4.md` describes, and any other agent's scratch folder.
- **My scratch.** It is `/tmp/claude-0/az2-forward-private/`. It holds prototype modules, value dumps, drafts of the checker continuation and development runs; the official run went to `/tmp/claude-0/az2-forward-private/run-final`. The Claude harness cached copies of some of my own reads (the Round11 README and advisor report, the AW1 forward report, the tail of the AY2 checker) and the log of my own Arb preview run. I re-read only those copies. They are my own reads, not other agents' files.

**Established mathematics, credited as such.** Kato analytic perturbation theory; Rayleigh–Ritz and min–max; Weyl's eigenvalue inequality; the Temple and Eckart inequalities; the residual (Davis–Kahan-type) angle bound; Young's inequality and the Schur-complement comparison of Round11 T1–T5; Cauchy estimates; Peter–Weyl and Clebsch–Gordan for SU(2). The graph reduction, the Haar measure, the kinetic operator, its complete spectrum and the tail threshold are **inherited Round11 results** (reviewed in Round11). The contribution here is only their assembly into exact certificates for the named finite-graph model, with exact constants. HNM labels are project aliases. Scientific priority is unverified.

## Verdict (forward, single producer)

**Model and label.** `FG(two-plaquette, D in {6,8}, tau_FG grid, I1.5, gauge-invariant)`. This is the Round11 open two-square patch: 6 vertices, 7 links and 6 Gauss constraints, in the gauge-invariant sector, with `H_FG = K - tau_FG (W_1 + W_2)` in alpha units. The flags are `model_is_finite_graph: true`, `transfers_to_aq: false` and `fg_coefficients_fitted: false`. The sub-labels are `sign_certified_finite_graph` and `static_not_dynamic`.

**Headline results (exact, full graph Hilbert space).**
1. **Derivative at zero.** `d<W_1>/dtau_FG` at `0` is exactly `1/6` at both cutoffs, with enclosure `[1/6, 1/6]`. The omitted-space tail term is exactly `0`, because `psi_1 = (W_1+W_2)/3` is an exact eigenvector combination of the full kinetic operator. A second, independent route (certified finite differences with a Cauchy-bounded bias) gives `[0.1666287349, 0.1667045873]`, which contains `1/6`.
2. **Dictionary.** Under `tau_FG = tau/24`, `1/6` becomes `1/144`, the matched Z^3 value. This is consistency only (Section 5).
3. **Enclosures of `<W_1>`.** All 12 grid points are enclosed (`tau_FG` in `{±1/1000, ±1/100, ±1/10}` at `D=6` and `D=8`), and so is the free reference. Every enclosure excludes the free reference `0` and has the sign of `tau_FG`. Half-widths run from `1.1e-15` (D=6, `|tau_FG|=1/10`) down to `2.8e-39` (D=8, `|tau_FG|=1/1000`).
4. **Second-order coefficients (finite-model values).** They are identical at both cutoffs, and their truncation error is exactly zero:
   - `<W_1>`: `0`, by the shared-link flip;
   - `E_0`: `-1/6`;
   - `<W_1^2>`: `7/576`;
   - `<W_1 W_2>`: `79/2808`;
   - outer loop `<z>`: `7/216`.

   The finite-graph remainder is third order: `<W_1> = tau_FG/6 - (187/33696) tau_FG^3 + (767713/2523156480) tau_FG^5 + ...`.
5. **Ledger.** The five-part residual ledger is complete at every point. The omitted residual is exactly the first omitted shell, split into 36 sectors (D=6) or 55 sectors (D=8) that are verified exactly orthogonal. It is dominated by the shared-link channel. The tail threshold `tail_lower = 45` (D=6) or `69` (D=8) certifies both the energy enclosure and the ground-state tail.

**Proposed forward verdict:** `accepted_within_scope`, with sub-labels `sign_certified_finite_graph` and `static_not_dynamic`. Admission needs the skeptic's replay and review.

> The finite-graph derivative of <W>_FG at tau_FG=0, under the stated normalization dictionary, is consistent with the matched Z^3 first-order coefficient 1/144; this is a consistency check on a different, finite model, not a prediction, not a confirmation of the Z^3 value, and it does not transfer to any subsequential limit of the AQ construction or resolve roadmap goal 2.

## 1. Model, conventions and scales

**Graph (Round11 G1–G2).** The graph has vertices TL, TM, TR, BL, BM, BR and seven oriented links, each carrying normalized SU(2) Haar measure:

| link | h1 | h2 | h3 | h4 | vL | vM | vR |
|---|---|---|---|---|---|---|---|
| orientation | TL→TM | TM→TR | BL→BM | BM→BR | TL→BL | TM→BM | TR→BR |

Independent SU(2) gauge transformations act at all six vertices; these are the **six Gauss constraints**. Base the two loops at TM:
- `U = vM h3^-1 vL^-1 h1` (square 1);
- `V = h2 vR h4^-1 vM^-1` (square 2);
- `W_1 = x = Tr(U)/2`, `W_2 = y = Tr(V)/2` and `z = Tr(UV)/2` (outer loop; `vM` cancels in `z`).

The physical Hilbert space is `L^2(Omega, (2/pi^2) dx dy dz)` (Round11 Q1–Q3).

**Hamiltonian, convention and sign.** In alpha units the Hamiltonian is

```
H_FG = K - tau_FG (W_1 + W_2),   K = sum of the seven link Casimirs j(j+1)  (Round11 rho = 1)
     = H_R11(alpha=1, lambda1=lambda2=tau_FG, rho=1) - 2 tau_FG.
```

- The constant `-2 tau_FG` shifts no state, so `<W>` is the same in both forms.
- For `tau_FG < 0` the Round11 solver API (`lambda >= 0`) does not apply. The operator identity and every bound below still hold, because they use only `||W_1+W_2|| <= 2`.
- **Sign.** The sign follows the I1.5 convention (`phi_b = -(tau/3) sum W_f`, i.e. `-(tau/24) W_f` in alpha units). So the first-order Wilson mean is **positive** for positive `tau_FG`: `<W_1> = +tau_FG/6 + O(tau_FG^3)`.
- **Scales.** Physical energies are `alpha H_FG`, with `alpha > 0` fixed; a static ground-state mean does not depend on `alpha`. The clock `s = alpha t_E/hbar`, `theta = alpha t/hbar` is named only, since this loop is static and uses no Euclidean node.
- **Dictionary.** The Z^3 face coefficient in alpha units is `nu/alpha = tau/24` (I1 §1), while the graph's coupling multiplies one face each. Hence `tau_FG = tau/24`.

**Kinetic operator.** In quotient coordinates `K = 3 C_U + 3 C_V + S`. Here `C_U` acts on `(x,z)`, `C_V` on `(y,z)`, and the shared-link term `S` (derivative `L_U - R_V`) on `(x,y)`. The checker reproduces the Round11 K5 identities exactly: `K1=0`, `Kx=3x`, `Ky=3y`, `Kz=9z/2` and `K(xy)=13xy/2 - z/2`. The last identity is the shared-link cross term.

## 2. Basis, cutoff and the complete five-part residual ledger

### 2.1 Basis, cutoff and why the residual is finite

`P_D` is spanned by the monomials `x^a y^b z^c` with `a+b+c <= D`, in Round11 `basis(D)` order. Its dimension is `C(D+3,3)`: **84** at `D=6` and **165** at `D=8`.

- `K` is triangular in degree, with diagonal `eps(a,b,c) = 3j(j+1) + 3k(k+1) + ell(ell+1)`, where `j=(a+c)/2`, `k=(b+c)/2`, `ell=(a+b)/2` (Round11 E2).
- `K` preserves every `P_d`, and multiplication by `x` or `y` raises the degree by at most one.
- **Hence, for `v` in `P_D`, `H_FG v` lies in `P_{D+1}`.** The complete full-space residual `(H - mu) v` is therefore a finite polynomial and can be computed exactly. There is no omitted component beyond shell `D+1`. `D` is the total polynomial degree; no per-link `j_max` is well-posed for this basis.

### 2.2 Exactly orthogonal sectors of the first omitted shell

For each monomial `m_s` of degree `D+1`, put `Q_D m_s = m_s - P_D m_s`.

- Peter–Weyl on each link gives the following. `m_s` has link spins at most `(j,k,ell)` coordinatewise. The monomials of a down-closed set of labels span exactly the spin networks with those labels. So `Q_D m_s` is the single spin-network sector `(j,k,ell)` of shell `D+1`.
- These vectors are mutually orthogonal. The checker verifies this exactly: the Schur complement `G_{D+1,D+1} - B^T G_D^{-1} B` has zero off-diagonal entries.
  - At `D=6`: 36 sectors and 630 pairs.
  - At `D=8`: 55 sectors and 1485 pairs.
  - The top retained shells (28 and 45 sectors) pass the same test.
- The Gram matrix is block diagonal in the four link-flip parity classes (blocks of 24/20/20/20 at `D=6` and 45/40/40/40 at `D=8`). Its exact LDL^T has all pivots positive.
- **Every omitted norm is therefore an exact sum of sector weights.**

### 2.3 Per-link spins, the product channel and exact thresholds

The degree-two vertices force one spin along each three-link path:
- `j` on h1, vL and h3;
- `k` on h2, vR and h4;
- `ell` on the shared link vM.

A shell-(D+1) sector exceeds the per-link retained maximum `D/2` on these links exactly as follows:
- on the `j` links iff `b = 0`;
- on the `k` links iff `a = 0`;
- on vM iff `c = 0`.

The **product channel** is the set of sectors with `a, b, c >= 1`. There every link spin is within `D/2`, yet the joint degree is omitted. These states are not implied by any per-link item.

The exact thresholds are minima of `eps` over all omitted shells. The enumeration stops once the Round11 E3 shell minimum `m_d = 5d^2/8 + 2d + 3(d mod 2)/8`, which increases with `d`, exceeds every class minimum:

| D | joint `tail_lower` (= `m_{D+1}`) | vM per-link | h1,vL,h3 (and h2,vR,h4) per-link | product channel |
|---|---|---|---|---|
| 6 | **45** at (3,4,0) | 45 at (3,4,0) | 123/2 at (6,0,1) | 48 at (3,3,1) |
| 8 | **69** at (4,5,0) | 69 at (4,5,0) | 96 at (7,0,2) | 145/2 at (4,4,1) |

Both `tail_lower` values equal the contract's 45 and 69 and the E3 formula. The lowest omitted state excites the shared link.

### 2.4 The five ledger items

Take a rational Ritz vector `v` in `P_D`, normalized to `v̂`, with Rayleigh quotient `mu` and complete residual `r = (H - mu) v̂`, `rho = ||r||`. Then `rho^2 = rho_P^2 + rho_Q^2` exactly, where `rho_P` is the retained part and `rho_Q^2 = tau_FG^2 ||Q_D (x+y) v̂||^2` is the omitted part.

- **(a) Per-link representation tail, one row for each of the seven links.** Each row gives:
  - the retained maximum spin `D/2`;
  - the exact threshold of states whose spin on that link exceeds `D/2`;
  - the exact weight of `r` in the sectors exceeding `D/2` on that link;
  - the link's **boundary layer** in `v̂` (shell-D sectors with spin exactly `D/2`);
  - the certified per-link tail of the **true** ground state (Lemma 7).
- **(b) Joint product channel across all seven links.** This item gives:
  - `rho_Q^2` as the exact sum over all shell-(D+1) sectors;
  - the product-channel weight and its threshold;
  - the corner overlaps between per-link classes;
  - the x- and y-face channels with their **interference `2XY`**. It is positive, so the face channels are not orthogonal;
  - the certified joint tail `T_joint` of the true ground state.

  The checker verifies exactly that per-link classes plus product channel minus corners equals `rho_Q^2`.
- **(c) Gauge-invariant projection: exactly 0.** Every basis element is a polynomial in traces of closed holonomies, invariant under all six vertex actions, and `H` commutes with the gauge action. An exact rational-quaternion fixture confirms this: seven rational unit quaternions give `(x,y,z) = (13/18, 1/6, -4/27)`, unchanged under four sets of six vertex transformations. The open three-link path `h3^-1 vL^-1 h1` changes under them; `z` does not depend on `vM`; and the vM flip maps `(x,y,z)` to `(-x,-y,z)`.
- **(d) Ritz/eigenvector residual.** This item gives:
  - `rho_P^2` (below `5e-199` everywhere: the Ritz proposal rounded at `10^-100`);
  - `rho^2`;
  - the certified gap;
  - the Davis–Kahan angle bound `s_A` and the Eckart/tail-comparison angle bound `s_B`.
- **(e) Arithmetic.** Everything is exact `Fraction` arithmetic.
  - The only non-rational steps are square roots, rounded upward by integer `isqrt` (width at most `1e-55`).
  - Exported enclosure ends are rounded outward to denominators `10^45`. At most about `2e-45` of the width comes from this rounding, and it is included.
  - The 110-digit `decimal` inverse iteration only **proposes** `v`. Its rounding appears, measured exactly, in item (d).

The preregistered error terms map as follows: `truncation_jmax` → items a+b+c (the D-cutoff truncation), `eigenvector_residual` → item d, `arithmetic` → item e.

### 2.5 The enclosure theorem

Write `b := 3 - 2|tau_FG|`.

- **Lemma 1 (complete residual).** For `v` in `P_D`, `r = (H-mu)v̂` lies in `P_{D+1}`, and `rho^2 = <Hv̂,Hv̂> - mu^2` is exact.
- **Lemma 2 (certified gap, Weyl).** `E_1(H_FG) >= E_1(K) - ||tau_FG(W_1+W_2)|| >= 3 - 2|tau_FG| =: b`. Here `E_1(K) = 3` comes from the complete free spectrum (Round11 E3, with `span{x,y}` at 3). Also `E_0 <= mu` (Rayleigh–Ritz). At every point `mu < b`. So the ground state is simple and `E_1 - E_0 >= b - mu`, which ranges from 2.80 to 3.00.
- **Lemma 3 (Davis–Kahan and Temple).** If `sin(theta)` is the angle between `v̂` and the ground state, then `sin(theta) <= rho/(b-mu) =: s_A` and `E_0 >= mu - rho^2/(b-mu)`.
- **Lemma 4 (Round11 tail comparison with the solver's tail bound).** Let `tau_t = tail_lower - 2|tau_FG|`, so that `Q_D H Q_D >= tau_t Q_D` (E4), and take `R = b < tau_t`. Young's inequality gives `H >= B (+) R Q_D`, with `B = A - C C*/(tau_t - R)`, `A = P_D H P_D` and `C C* = P_D V Q_D V P_D`. Then:
  - `E_0 >= lambda_0(B)`, because `lambda_0(B) <= mu < R`;
  - `beta_0 = <v̂,Bv̂> = mu - rho_Q^2/(tau_t - R)`;
  - finite Temple gives `lambda_0(B) >= beta_0 - eta^2/(b_B - beta_0)`, with `eta = ||(B - beta_0)v̂||` computed exactly and `b_B = b - 4 tau_FG^2/(tau_t - R) <= lambda_1(B)`.

  This energy bound is **14–24 times sharper** than Temple's, because the omitted leakage is divided by `tau_t - R`, about 42 (D=6) or 66 (D=8), instead of `b - mu`, about 2.8.
- **Lemma 5 (Eckart).** `sin^2(theta) <= (mu - E_0)/(E_1 - E_0) <= (mu - E_0^low)/(b - mu) =: s_B^2`. At every grid point `s_B < s_A`, by a factor of 3.7–4.9. **The headline enclosure therefore uses the solver's tail bound together with the certified gap.**
- **Lemma 6 (observable).** With `||W_1|| <= 1`, `|<v̂,W_1 v̂> - <psi_0,W_1 psi_0>| <= 2 s sigma + 2 s^2 <= 2s + 2s^2`, where `s = min(s_A, s_B)` and `sigma = ||(W_1 - <W_1>)psi_0|| <= 1` (vector centering).
- **Lemma 7 (certified tails of the true ground state).**
  - **Joint:** `Q_D(H-E_0)psi_0 = 0` and `Q_D H Q_D >= tau_t Q_D` give `||Q_D psi_0|| <= (rho_Q + 2|tau_FG| s)/(tau_t - mu)`.
  - **Per link class `e`:** `Pi_e` is the projector onto spin above `D/2`; it commutes with `K`, and its range lies in `Q_D` by the triangle inequality. Let `c_e` be the number of faces containing the link and `Lambda_e` the spin-exactly-`D/2` layer. Then `||Pi_e psi_0|| <= c_e |tau_FG| (||Lambda_e v̂|| + s)/(t_e - 2|tau_FG| - mu)`.
  - The smaller of the per-link and joint bounds is reported. For vM the joint bound is smaller; for the other six links the per-link bound is smaller by factors of about 50–140.

**Theorem.** At every grid point and cutoff, `<W_1>_FG` lies in `[w_R - (2s+2s^2), w_R + (2s+2s^2)]`, rounded outward. `E_0` lies in `[max(Temple, tail comparison), mu]`. The ground state's omitted weight is at most `T_joint`.

## 3. Results at the grid

### 3.1 Enclosures of `<W_1>_FG`

These are previews truncated from the exact exported rationals in `output/results.json`:

| D | tau_FG | enclosure of <W_1> (lower, preview) | (upper, preview) | half-width (preview) | sign certified |
|---|---|---|---|---|---|
| 6 | 0 | `0` | `0` | 0 | free reference |
| 8 | 0 | `0` | `0` | 0 | free reference |
| 6 | 1/1000 | `1.666666611170468379800822e-4` | `1.666666611170468379800823e-4` | 1.100e-29 | yes |
| 6 | -1/1000 | `-1.666666611170468379800823e-4` | `-1.666666611170468379800822e-4` | 1.100e-29 | yes |
| 6 | 1/100 | `1.666661117076960223897330e-3` | `1.666661117076960224118052e-3` | 1.103e-22 | yes |
| 6 | -1/100 | `-1.666661117076960224118052e-3` | `-1.666661117076960223897330e-3` | 1.103e-22 | yes |
| 6 | 1/10 | `1.666112008741082417265341e-2` | `1.666112008741309878195670e-2` | 1.137e-15 | yes |
| 6 | -1/10 | `-1.666112008741309878195670e-2` | `-1.666112008741082417265341e-2` | 1.137e-15 | yes |
| 8 | 1/1000 | `1.666666611170468379800823e-4` | `1.666666611170468379800823e-4` | 2.814e-39 | yes |
| 8 | -1/1000 | `-1.666666611170468379800823e-4` | `-1.666666611170468379800823e-4` | 2.814e-39 | yes |
| 8 | 1/100 | `1.666661117076960224007691e-3` | `1.666661117076960224007691e-3` | 2.822e-30 | yes |
| 8 | -1/100 | `-1.666661117076960224007691e-3` | `-1.666661117076960224007691e-3` | 2.822e-30 | yes |
| 8 | 1/10 | `1.666112008741196147439620e-2` | `1.666112008741196148021390e-2` | 2.908e-21 | yes |
| 8 | -1/10 | `-1.666112008741196148021390e-2` | `-1.666112008741196147439620e-2` | 2.908e-21 | yes |

Exact exported enclosures, as examples:
- D=6, `tau_FG = +1/10`: `[833056004370541208632670685210085603968639/50000000000000000000000000000000000000000000, 4165280021853274695489175720401295534950583/250000000000000000000000000000000000000000000]`.
- D=8, `tau_FG = +1/10`: `[8330560043705980737198104247838582935020907/500000000000000000000000000000000000000000000, 16661120087411961480213908206571701630183797/1000000000000000000000000000000000000000000000]`.

Properties of the enclosures:
- The D=8 enclosures lie inside the D=6 enclosures at every point.
- The `-tau_FG` certificate is computed separately. It equals the vM-flip image of the `+tau_FG` certificate exactly: same Ritz vector up to the signs `(-1)^(a+b)`, same `mu` and `rho`, negated `<W_1>`.
- The exchange symmetry gives `<W_2> = <W_1>` exactly.

### 3.2 Energies and gaps

The table below gives the energy enclosures (previews). The E_0 enclosure width is below 22 digits at every point. The Temple widths are `1.4e-29` (D=6, 1/10) and `1.4e-40` (D=8, 1/10); the tail-comparison widths are `9.1e-31` and `5.9e-42`.

| D | tau_FG | E_0 enclosure (preview; lower, upper) | E_1 - E_0 lower bound |
|---|---|---|---|
| 6 | ±1/1000 | `-1.666666638918567016122e-7`, `-1.666666638918567016122e-7` | 2.99800017 |
| 6 | ±1/100 | `-1.666663891866742375134e-5`, `-1.666663891866742375134e-5` | 2.98001667 |
| 6 | ±1/10 | `-1.666389287037545016204e-3`, `-1.666389287037545016204e-3` | 2.80166639 |
| 8 | ±1/1000 | `-1.666666638918567016122e-7`, `-1.666666638918567016122e-7` | 2.99800017 |
| 8 | ±1/100 | `-1.666663891866742375134e-5`, `-1.666663891866742375134e-5` | 2.98001667 |
| 8 | ±1/10 | `-1.666389287037545016204e-3`, `-1.666389287037545016204e-3` | 2.80166639 |

Labelled comparison: `E_0 - (-tau_FG^2/6 + (187/67392) tau_FG^4)` is about `-1.0e-10` at `1/10`, consistent with a sixth-order term.

### 3.3 Residual ledger values

These are upward-rounded previews; the `-tau_FG` rows are identical. The per-link weights are the Ritz leakage in sectors that exceed `D/2` on that link. The "T per link" column gives the certified tail of the true ground state for the h1/vL/h3 class and for vM (h2/vR/h4 equals h1/vL/h3).

| point | rho_Q^2 (complete omitted) | vM class | j (= k) class | product channel | 2XY interference | rho_P^2 (retained) | sin(theta) DK / Eckart | T_joint | T per link j / vM |
|---|---|---|---|---|---|---|---|---|---|
| D6, 1/1000 | 3.81105e-57 | 3.811e-57 | 2.897e-61 | 4.98938e-66 | 1.68597e-57 | 3.93e-199 | 2.059e-29 / 5.502e-30 | 1.372e-30 | 1.759e-32 / 1.372e-30 |
| D6, 1/100 | 3.81098e-43 | 3.811e-43 | 2.897e-47 | 4.98929e-50 | 1.68594e-43 | 1.57e-199 | 2.072e-22 / 5.518e-23 | 1.375e-23 | 1.840e-25 / 1.374e-23 |
| D6, 1/10 | 3.80477e-29 | 3.805e-29 | 2.894e-33 | 4.98003e-34 | 1.68320e-29 | 1.80e-199 | 2.202e-15 / 5.687e-16 | 1.402e-16 | 2.682e-18 / 1.402e-16 |
| D8, 1/1000 | 3.91821e-76 | 3.918e-76 | 7.128e-82 | 3.31098e-85 | 1.78252e-76 | 3.02e-199 | 6.603e-39 / 1.407e-39 | 2.869e-40 | 5.708e-43 / 2.869e-40 |
| D8, 1/100 | 3.91814e-58 | 3.918e-58 | 7.128e-64 | 3.31092e-65 | 1.78249e-58 | 4.86e-199 | 6.642e-30 / 1.411e-30 | 2.874e-31 | 7.033e-34 / 2.873e-31 |
| D8, 1/10 | 3.91131e-40 | 3.911e-40 | 7.122e-46 | 3.30449e-45 | 1.77939e-40 | 2.79e-199 | 7.059e-21 / 1.454e-21 | 2.917e-22 | 2.075e-24 / 2.916e-22 |

Readings:
- **Channels.** The omitted residual is dominated by the **shared-link channel**: sectors `x^a y^b` with `a+b = D+1`, where vM carries spin `(D+1)/2`. The corner `z^{D+1}` has exactly zero weight, since it cannot be reached from shell `D` in one step. The product channel is small but nonzero, and it is itemized.
- **Scaling.** `rho_Q^2` scales as `tau_FG^{2(D+1)}`; the certified ratio between `1/100` and `1/1000` at D=8 is `9.99983e17`.
- **Tail sharpening.** `T_joint` is 4–5 times smaller than `sin(theta)`, which shows how the tail threshold sharpens the omitted weight.

## 4. Item 2: the derivative at `tau_FG = 0` and the own free reference

**Free reference.** `certify(pc, 0)` is the same function that is used at every grid point. It returns the constant as the Ritz vector (exactly: the rounded proposal is `10^100` times the constant monomial), with `mu = 0`, `rho = 0` and enclosure `[0, 0]` at both cutoffs. The value is exactly `E[W] = E[x] = 0` by Haar symmetry: the central flip of vM maps `x` to `-x` and preserves the normalized Haar measure.

**Exact derivative.**
- Setup: `H_FG(tau) = K + tau V` with `V = -(W_1+W_2)` bounded; the ground state `E_0(0) = 0` is simple, with gap 3. Kato analyticity then makes `<W_1>(tau)` real-analytic near 0, with Rayleigh–Schrödinger coefficients.
- The first-order vector `psi_1 = K^{-1} Q_0 (W_1+W_2) = (W_1+W_2)/3` holds exactly in the **full** space, since `span{x,y}` is the exact K-eigenspace at 3. So the finite-basis resolvent on `P_D` coincides with the full resolvent, and the tail term is `0`.
- Therefore `d<W_1>/dtau_FG = 2<x, psi_1> = 2 E[x^2]/3 = 1/6` exactly, at `D=6` and `D=8` alike.

**Second route (certified finite differences, independent of the Rayleigh–Schrödinger vectors).**
- For complex `|tau| <= 3/8`, the Riesz projection around `|z| = 3/2` satisfies `||(H(tau)-z)^{-1}|| <= (2/3)/(1-4|tau|/3) = 4/3`. Hence `||P(tau)|| <= 2` and `|Tr(H P)| <= 3`.
- Cauchy's estimate gives `|a_n| <= 2 (8/3)^n` and `|e_n| <= 3 (8/3)^n`.
- The odd part of the certified `±1/1000` enclosures then encloses `a_1` in `[166628734921/1000000000000, 166704587313/1000000000000]`, about `[0.1666287, 0.1667046]`, at both cutoffs. This contains `1/6`; the bias is fully bounded.

## 5. Item 3: comparison with the matched Z^3 coefficient (consistency only)

The dictionary `tau_FG = tau/24` comes from the contract and from I1's `nu = alpha tau/24` per face. The graph's first-order value `1/6` therefore corresponds to `(1/6)/24 = 1/144`. That is the AW1-admitted Z^3 first-order coefficient (`omega_tau(W) = +tau/144 + r(tau)` under I1.5). The route-2 enclosure divided by 24 is `[6.9428640e-3, 6.9460245e-3]`, which also contains `1/144`. The finite graph is only **consistent with** the matched coefficient. The mandatory sentence, verbatim:

> The finite-graph derivative of <W>_FG at tau_FG=0, under the stated normalization dictionary, is consistent with the matched Z^3 first-order coefficient 1/144; this is a consistency check on a different, finite model, not a prediction, not a confirmation of the Z^3 value, and it does not transfer to any subsequential limit of the AQ construction or resolve roadmap goal 2.

Two facts make the agreement expected rather than informative:
- Both models share the per-link Casimir normalization: `W Omega` has energy 3 in alpha units in both.
- In both, the first-order mean is `2 × coefficient × E[W^2] / 3`.

Nothing about the AQ model's shift, its remainder constant or roadmap goal 2 is inferred.

## 6. Item 4: second-order coefficients as finite-model values

**Exact series.** The Rayleigh–Schrödinger series about the free ground state is computed exactly by polynomial back-substitution (`K` is triangular in degree):
- Every `psi_n` lies in `P_n`.
- The full-space equation `K psi_n = -V psi_{n-1} + sum_k E^(k) psi_{n-k}` holds **as a polynomial identity** for `n <= 5`.
- The coefficients are therefore identical at `D=6` and `D=8`, and the truncation error is exactly zero, not merely bounded.

The vectors are `psi_1 = (x+y)/3` and `psi_2 = x^2/24 + 4xy/39 + y^2/24 + 4z/351 - 1/48`. The coefficients are:

| quantity | order 1 | order 2 | order 3 | order 4 | order 5 |
|---|---|---|---|---|---|
| `<W_1>` | 1/6 | **0** | -187/33696 | 0 | 767713/2523156480 |
| `E_0` | 0 | **-1/6** | 0 | 187/67392 | 0 |
| `<W_1^2>` (order 0: 1/4) | 0 | **7/576** | 0 | -787717/1261578240 | — |
| `<W_1 W_2>` | 0 | **79/2808** | 0 | -20159/10513152 | — |
| `<z>` | 0 | **7/216** | 0 | -349/151632 | — |

Consistency checks on the table:
- **Hellmann–Feynman.** `a_n = -(n+1) e_{n+1}/2` holds exactly for `n <= 4`.
- **Why the second-order `<W_1>` coefficient vanishes.** The shared-link flip `U_E` (with `E = {vM}`, which meets both faces once) sends both `W_f` to `-W_f` and commutes with every Casimir and gauge action. So `<W_1>(-tau) = -<W_1>(tau)`.
- **Second route for the second-order values.** The even parts of the `±1/1000` enclosures give `a_2` in `[-1.0114e-4, 1.0114e-4]` and `e_2` in `[-0.16681837, -0.16651496]`, at both cutoffs. These contain `0` and `-1/6`.
- **Grid remainder.** `(<W_1> - tau_FG/6)/tau_FG^3` evaluates to `-5.54961982868e-3` at `1/1000` and `-5.54657925470e-3` at `1/10`, against `-187/33696 = -5.5496201e-3`. This is a labelled comparison.

These are finite-model values only; no remainder constant of any other model is bounded or estimated from them.

## 7. Symmetries and the Arb preview

The optional `arb_preview.py` is labelled **PREVIEW ONLY**; `check.py` never imports it.
- **Method.** It rebuilds the Haar moments (Q4) and the kinetic operator directly from the Round11 K4 differential formula, not from `check.py`'s Casimir decomposition, as FLINT `fmpq` matrices, using python-flint 0.9.0. It then runs Arb-ball inverse iteration at 400 bits and records balls for the Ritz `<W_1>` and `E_0` at all 14 points.
- **Output.** The file `preview/arb_preview.json` took about 4 minutes to produce.
- **Comparison.** `check.py` reads the file only to compare. All 14 Wilson balls intersect the exact enclosures, and the ball widths are at most `6e-60`.
- **Limit.** A finite-matrix value is not a full-space certificate; the preview never decides admission.

## 8. Checker, controls and runtime

`check.py --output <absolute fresh dir>` uses only the standard library. It never imports numpy, scipy, python-flint, `two_plaquette.py` or `arb_preview.py`.
- It verifies the contract sha256 and reads from the contract the grid, cutoffs, dimensions, `tail_lower`, dictionary, target, gate fields, mandatory sentence and forbidden phrasings.
- It records its own sha256 before evaluation. It binds the Round11 solver's exact source strings (basis, moments, kinetic coefficients, tail formula) to the snapshot.
- It writes `results.json` (35 checks) and `source-manifest.json`.
- All 20 contract controls reject damaging mutations through explicit exceptions (80 mutations in the control checks, 90 in total).
- The contract target (a 0/1 feasibility indicator) evaluates to 1.
- **Private source-edit audit (scratch, not evidence).** On copies of the closure in `/tmp/claude-0/az2-forward-private/mutaudit/`, each of these edits of `check.py` aborts with an `AdmissionError`:
  - the y face dropped from `H v`;
  - `||W_1+W_2||` set to 1 or to 3;
  - the shared-link Casimir weight set to 2;
  - `tail_lower` taken from the last retained shell;
  - the free gap set to 4;
  - the Haar moment normalization changed.

  The free-gap edit was first caught only through the report's bound exact values. The checker now ties the free gap to `m_1 = 3` and the potential norm to the identity configuration, and both edits abort at `round11_conventions_bound`.
- Runtime is about 41 s per replay: 14 certificates and a 110-digit Ritz proposal of about 4 s each at `D=8`. Normal and `-O` replays are byte-identical.

## 9. Limitations, exclusions and wording defects

**Contract claim exclusions, verbatim:**
- any statement about the AQ model's shift or K_2 from the graph;
- resolution of roadmap goal 2;
- continuum;
- scientific priority;
- the forbidden phrases `predicts` and `confirms the Z^3 value`.

**Preregistration exclusions also apply:**
- a free reference inside an enclosure means no interaction claim (here the finite-graph enclosures exclude it, which gives the sub-label `sign_certified_finite_graph` for **this graph only**);
- no uniqueness of any subsequential limit;
- no whole-sequence convergence or rate in `N`;
- no continuum or weak coupling;
- no transfer from a finite graph;
- no static-to-dynamic relabelling;
- no priority.

The exported flags are `transfers_to_aq: false`, `model_is_finite_graph: true`, `fg_coefficients_fitted: false`, `continuum_claim: false`, `uniform_wilson_claim: false`, `resolved_interaction_shift: false` (this refers to the AQ/Z^3 interaction shift) and `scientific_priority_verified: false`.

**Stated honestly:**
1. **Inherited without re-proof.** The Round11 reduction (Q1–Q3), the kinetic operator (K1–K4), the complete spectrum and tail (E1–E4) and Theorem F are inherited. The checker re-verifies the K5 identities, the E3 shell minima, the Q4 moment fixtures and the Gram structure, not the reduction itself.
2. **Retained weaker tiers.** These are all valid and retained:
   - the Davis–Kahan angle, weaker than Eckart by 3.7–4.9 times;
   - Temple's energy bound, weaker than the tail comparison by 14–24 times;
   - the route-2 intervals, about `1e-4` wide;
   - for vM, the per-link tail route, which is weaker than the joint route.
3. **Scope of the grid.** The negative-`tau_FG` points lie outside the Round11 solver API's `lambda >= 0` contract. The certificates need no sign.
4. **Cutoffs.** No cutoff beyond `D=8` is computed, and `D=10` is not declared. `D` is a joint polynomial-degree cutoff, not a per-link `j_max`.
5. **Static only.** No dynamical statement, correlator, clock or mass-gap reading is made.

**Contract wording defects (non-blocking; each is a verified fact about the frozen text and is recorded in `results.json`):**
- **D1.** `truncation_jmax` is preregistered, although `parameters.cutoff` says no `j_max` is well-posed. It is mapped to ledger items a+b+c.
- **D2.** `state_provenance` is an AQ-family string. The FG state is the unique ground state of `H_FG`.
- **D3.** Several control ids name AQ/Z^3 objects. Each is given a finite-graph analogue (Section 10).
- **D4.** Item 4 asks for a tail residual bounding the truncation error. That error is exactly zero, and the second-order `<W>` coefficient is exactly zero.
- **D5.** The target `1`/`>=` is evaluated as a feasibility indicator.
- **D6.** `selected_after` names the AZ1 gate, which is not a premise and was not read.
- **D7.** `parameters.observable` says "must reproduce". This is treated only as the item-3 consistency comparison.
- **D8.** The clock's "exponent 24" coexists with the dictionary denominator 24, which is a coupling ratio, not an exponent.

**Methodological lenses.**
- **Newton, analysis before synthesis:** the representation content (which links a face multiplication excites, which sectors are reachable) was worked out before any budget.
- **Tesla, complete accounting:** every channel is charged, including both faces, the shared link, the product channel, the interference term and the arithmetic.

These are modern uses of the snapshotted skills. No historical figure endorses anything here, and no historical or occult material supplies a premise.

## 10. Item and control map

| entry | where | what executes it |
|---|---|---|
| item 1 | §2, §3.3 | `shell_sectors_orthogonal`, `ritz_certificates_complete`, `complete_residual_ledger_itemized`, `certified_representation_tail`, `gauge_invariance_fixture` |
| item 2 | §3.1, §4 | `ritz_certificates_complete`, `derivative_at_zero_exact`, `own_free_reference`, `route2_cauchy_certified` |
| item 3 | §5 | `dictionary_consistency_not_confirmation`, `mandatory_sentence_and_phrasing` |
| item 4 | §6 | `rs_exact_full_space`, `route2_cauchy_certified` |
| item 5 | §1, §7–§9 | all twenty controls below; `no_solver_import_and_preview_labelled`; gate fields exported |
| item 6 | §5, §9 | `mandatory_sentence_and_phrasing` (forbidden-phrase scan, code spans removed) |
| `missing_incoming_stars` | §1 | FG analogue: both faces coupled (W_2 touches vM of square 1) and all seven Casimirs; rejects W_2 omitted, rho=0 and the independent rotor |
| `full_original_wilson_cover` | §1, §2.4(c) | W_1 uses all four links of square 1 in the full seven-link space; rejects the open three-link path, a basis without z and the outer perimeter |
| `wrong_delta_alpha_hbar_clock` | §1 | alpha units (tau/24, energy 3) and normalized units (tau/3, energy 24) both give 1/144; rejects tau/18, tau/1152 and the u-clock; nonunit fixture alpha=5, hbar=7 |
| `vector_versus_scalar_centering` | §2.5 | AT4 control (+1/10000, -51/10000, 1/16) reproduced; Lemma 6 uses vector centering; rejects scalar subtraction |
| `first_order_mean_charged` | §4 | 1/6 is charged, and the enclosures exclude 0; rejects a zero first order and a first order absorbed into the remainder |
| `tau_scaling_exponent` | §3.3, §6 | certified ratios: linear, cubic remainder, quadratic energy, leakage `tau^{2(D+1)}`; rejects mislabels |
| `changed_model_relabelled` | §1 | rejects rho=2, one plaquette, D=4, off-grid tau, unequal faces, the AQ id and a flipped sign |
| `coherent_evidence_tampering` | §8 | 12 coherent rehash tamperings are rejected by exact recomputation |
| `insufficient_verdict_retained` | §9 | acceptance rule; retained weaker tiers; rejects relabelled verdicts |
| `exact_arithmetic_admission` | §2.4(e) | rejects float, bool, NaN, a zero denominator and the decimal proposal |
| `root_n_misuse` | §2.4(b) | the face channels interfere (2XY > 0); rejects RSS without interference, division by 7 and RMS over link classes |
| `no_priority_or_continuum_claim` | §9 | flags false; rejects continuum, priority, uniform Wilson, weak coupling and goal 2 |
| `finite_graph_model_id` | Verdict | FG id, graph name and labels; rejects the flag false, the AQ id and a missing graph name |
| `complete_residual_all_channels` | §2.1–2.4 | the complete residual equals retained plus omitted, which equals the exact sector sum; rejects a dropped y channel, dropped product sectors, one sector as the norm, the finite-matrix residual and one face only |
| `certified_representation_tail` | §2.3, §2.5 | tail_lower 45/69 exact; T_joint and per-link tails; rejects m_D, an added diagonal, an unsubtracted potential, the product or per-link threshold used as the joint one, and a sampled sector |
| `own_free_reference` | §4 | the same code path gives [0,0] = E[W]; rejects 1/144, 1/4 and another path |
| `no_transfer_to_aq` | §5, §9 | transfers_to_aq false; rejects K_2 or goal-2 statements from the graph |
| `fg_coefficients_not_fitted` | §4, §6 | exact Rayleigh–Schrödinger values; rejects the least-squares slope (0.1666117...) and the secant |
| `sign_convention_fixture` | §1 | the two-state fixture gives +1/6 under I1.5 and -1/6 when flipped; positive exact enclosure at +1/10; rejects the flipped reading |
| `complete_residual_ledger_itemized` | §2.4 | five items at 14 points; rejects missing (b) or (e), a zero entry without a reason and a missing vM row |

## 11. Reproduction

```bash
python3 -B research/round32/forward/az2/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/forward/az2/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round32/forward/az2/arb_preview.py                              # optional labelled preview (python-flint)
python3 -B research/round32/tools/freeze.py verify research/round32/forward/az2
```
