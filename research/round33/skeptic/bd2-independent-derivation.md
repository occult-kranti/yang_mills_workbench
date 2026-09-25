# BD2 independent derivation before producer comparison

**Standing.** I wrote this after the BD2 contract froze (`frozen_at` 2026-09-25T05:09:10Z, sha256 `783cad80…46f41e`) and before reading anything of the BD2 producer. BD2 is single+skeptic, so this replay is an admission input: my own code for the two-plaquette algebra, the certificate, the Z³ items and the 2+1D constants. I am a model-agent skeptic with correlated ancestry, not a human reviewer. Human project author: Hruday N M (BUNZEEY).

**Isolation, disclosed.**
- I did not open, list or read `research/round33/forward/bd2/`, `forward/bd1/` or `reverse/bd1/`, except `find` on their `inputs/` (names only) and a sha256 comparison with the repository. `forward/bd2/inputs/` holds 35 files, all byte-identical and equal to the contract-derived list.
- Name-only exposures are as in the BD1 derivation: another session's untracked `skeptic/bc1_postreview_check.py`, commit subjects up to 8fe1781, and the abbreviated `inputs/` paths in `git show --stat 9ae1160`.
- **Code independence.** The admitted AZ2 checker (`research/round32/forward/az2/check.py`) and the Round11 solver (`two_plaquette.py`) are declared premises. I hashed them and never opened, imported or executed them. The two-plaquette algebra is written from the Round11 solver README and advisor note (Q1–Q4, K1–K5, E1–E4, Theorem F) and from the AZ2 report.
- **Certificate structure.** I read the AZ2 report §2 (the five-part ledger, its Lemma 4 tail comparison and its Lemma 7 joint tail) before writing my certificate. My tail-angle lemma (§4) is of the same kind as AZ2 Lemma 7. Its proof and code are my own, and it replaces AZ2's Eckart step.
- **The pre-freeze review.** Another session of this role wrote it. Its `<z>` preview reused a scratch copy of the AZ2 checker. I read its markdown up to "Against my own record" and its JSON edit lists, determinations and freeze-run headers. I did not read the "Advisor only: previews" section, `previews_recomputed`, or anything in `/tmp/claude-0/skeptic-bd-private/`.
  - Its determinations state several structural facts before I computed them: the two-variable parities; `L_k(3) = 8·6^k(1+4k/3)`, `G_3` and `G_3'`; the band premises; the 1×2 bound; and that the D=8 width lies "several million" times below `1/10^10`.
  - My independence from that review is therefore limited to derivation and code.
- Nothing under `research/round33/experts/` was read.
- After my values were final, a `git status` filtered to exclude `forward/` and `reverse/` lines listed the untracked directories `experts/historical/assistant-3/` and `experts/modern/assistant-3/` (names only, not opened). Nothing was changed afterwards except this disclosure and the freeze hashes.
- **Scratch.** Private folder `/tmp/claude-0/skeptic-bd-replay-private/`: prototypes `graph_proto.py`, `graph_rs.py` and `graph_cert.py`, run outputs and `srcmut/`. Not evidence, not a premise.

**Sources.**
- The frozen contract, `advisor/selection-bd2.md` and `advisor/plan.json` (vocabulary recorded).
- Premises:
  - the Round11 README, advisor note and solver README;
  - the AZ2 gate, report and skeptic review;
  - the AW1, AV1, AV2, AY1, AY2, AM2, AQ1 and BB2 gates;
  - the AY1 forward report (F11–F14), the AQ1 report (HNM-AQ1.1), the AM2 report (§§1–3) and the I1 report;
  - the BA1 and BB2 contracts for the inherited control semantics.

**Exactness.** Every value is from `bd2_check.py`: 64 checks, 21 controls as 85 damaging mutations with 4 positives, byte-identical under `-B`, `-B -O` and plain `python3`. Decimals are previews.

## 1. Model

- **Graph.** The Round11 two-square patch: 6 vertices, 7 links, 6 Gauss constraints, gauge-invariant sector. With the AZ2 loops `U = vM h3⁻¹ vL⁻¹ h1` and `V = h2 vR h4⁻¹ vM⁻¹`, the traces are `x = W_1 = Tr U/2`, `y = W_2 = Tr V/2` and `z = Tr UV/2` (the 1×2 loop; `vM` cancels).
- **Hamiltonian.** `H = K − l1 W_1 − l2 W_2` in alpha units, with `K` the sum of the seven link Casimirs `j(j+1)` at `rho = 1`. This is `model_is_finite_graph: true` and `transfers_to_aq: false`.
- **Cutoff.** `D` is the total polynomial degree. `P_6` has dimension 84 and `P_8` has 165.
- **Edges.** After tree reduction the graph is a theta graph with edges `e1` (h1, vL, h3; spin `j`), `vM` (spin `ℓ`) and `e2` (h2, vR, h4; spin `k`). The monomial `x^a y^b z^c` tops the sector `2j = a+c`, `2ℓ = a+b`, `2k = b+c`.

## 2. The two-plaquette algebra (own code)

1. **Haar moments, two routes** (check `haar_moments_two_routes`, 1330 monomials of degree ≤ 18).
   - Route 1 is Round11 (Q4).
   - Route 2 is my own: condition on `U₂`; then `z = ⟨U₁, conj U₂⟩ = y x + sqrt(1−y²) u'`, with `(x, u')` two orthogonal coordinates of the uniform `S³` point `U₁` and `E[u₁^{2i}u₂^{2j}] = (2i−1)!!(2j−1)!!/(2^{i+j}(i+j+1)!)`.
   - The routes agree, with `E[x²]=E[y²]=E[z²]=1/4` and `E[xyz]=E[x²y²]=1/16`.
2. **Edge Casimirs.** Each is `C = −¼ Δ_{S³}` in the two traces through the edge, with the third trace as the inner product of the two direction vectors. For example, `C_e1 = −¼[(1−x²)∂²_x + (1−z²)∂²_z + 2(y−xz)∂_x∂_z − 3x∂_x − 3z∂_z]`.
   - `K = 3C_e1 + C_vM + 3C_e2` equals Round11 (K4) on every monomial of degree ≤ 10.
   - The K5 identities hold: `K1=0`, `Kx=3x`, `Ky=3y`, `Kz=9z/2`, `K(xy)=13xy/2−z/2`.
   - Each edge Casimir is symmetric under the Haar moments (check `edge_casimirs_symmetric_under_haar`).
3. **Monic spin-network basis.** `s_abc = x^a y^b z^c + (lower degree)` is the eigenvector of the weighted Casimir `C_e1 + 121 C_vM + 14641 C_e2`. This operator is triangular in degree with spin diagonal and is nondegenerate on degree ≤ 9, so `s_abc` is obtained by back-substitution.
   - Each `s_abc` is a joint eigenvector of the three edge Casimirs.
   - Orthogonality to every other monomial of degree ≤ its own is verified with exact moments through degree 6.
   - Norms are `N_abc` (`1, 1/4, 1/4, 1/4, 1/16, 3/64, …`), and `K s_abc = ε_abc s_abc` with (E1).
   - Shell minima are `5d²/8 + 2d + 3(d mod 2)/8` (E3), strictly increasing: 3, …, **45** (d=7), **69** (d=9).
4. **Multiplication tables.** `x`, `y` and `z` act on `s_abc` by at most four moves:
   - `x`: `(a±1, b, c)`, `(a, b∓1, c±1)`;
   - `y`: `(a, b±1, c)`, `(a±1, b, c∓1)`;
   - `z`: `(a, b, c±1)`, `(a±1, b∓1, c)`.

   The raising move has coefficient 1. The tables satisfy the self-adjointness identity `c(k→k′)N(k′) = c(k′→k)N(k)` exactly. In this orthogonal basis the projection `P_D` is plain truncation, so every residual norm is an exact sum of sector weights.
5. **Flips.** On the basis:
   - `U_h1 = (−1)^{a+c}` reverses `x` and `z` and fixes `y`;
   - `U_h2 = (−1)^{b+c}` reverses `y` and `z`;
   - `U_vM = (−1)^{a+b}` reverses `x` and `y` and fixes `z`.

   The same holds on exact rational quaternions. The traces are invariant under four sets of six rational vertex gauge transformations, so the gauge projection is exactly 0.

## 3. Item 1: two-variable tables (zero truncation error)

Rayleigh–Schrödinger in `(l1, l2)` about the constant, in the orthogonal basis, at D=6 and D=8. `ψ_ij ∈ P_{i+j}`, and `K` is diagonal. The tables are identical at both cutoffs through total order 9. Along `l1 = l2`, the `<z>` series first differs between the cutoffs at order 14, so the comparison discriminates.

| observable | coefficients through total order 4 (`i,j` ↦ coefficient of `l1^i l2^j`) |
|---|---|
| `<W_1>` | 1,0: **1/6**; 3,0: **−5/864**; 1,2: **1/4212** |
| `<W_2>` | 0,1: 1/6; 0,3: −5/864; 2,1: 1/4212 |
| `<z>` | 1,1: **7/216**; 3,1: **−349/303264**; 1,3: **−349/303264** |
| `<C_shared>` | 2,0: **1/48**; 0,2: **1/48**; 4,0: **−5/4608**; 2,2: **−49/438048**; 0,4: **−5/4608** |
| `E_0` | 2,0: −1/12; 0,2: −1/12; 4,0: 5/3456; 2,2: −1/8424; 0,4: 5/3456 |

- **Parities**, checked on the table through order 9:
  - `<W_1>` has only (odd, even) monomials: odd in `l1` by the h1 flip, even in `l2` by the h2 flip.
  - `<z>` has only (odd, odd).
  - `<C_shared>` has only (even, even).
  - Every even-order coefficient of `<W_1>` at `l1=l2` vanishes.
- **AZ2 anchors at `l1 = l2`, reproduced exactly:**
  - `<W_1> = τ/6 − (187/33696)τ³ + (767713/2523156480)τ⁵`;
  - `E_0 = −τ²/6 + (187/67392)τ⁴`;
  - `<z>`: 7/216 and −349/151632;
  - `<W_1²>`: 7/576 and −787717/1261578240;
  - `<W_1W_2>`: 79/2808 and −20159/10513152;
  - `ψ₂ = x²/24 + 4xy/39 + y²/24 + 4z/351 − 1/48`.
- The one-face value `−5/864` is the `l1³` coefficient, the AW1 one-plaquette fixture under `τ_FG = τ/24`. The AZ2 second-square shift `1/4212` is the `l1 l2²` coefficient.
- **Second order at `l1=l2`:** `<z>` gives **7/216** and `<C_shared>` gives **1/24**.

## 4. Item 2: certified enclosures of `<z>` at `l1 = l2`

**Setting.**
- `H = K + V` with `V = −l(x+y)` and `v = 2|l| ≥ ‖V‖`.
- `P = P_D` and `Q = 1 − P`. `K` commutes with `P`, `QKQ ≥ Λ_D Q` with `Λ_D = m_{D+1}` (45 and 69, equal to the AZ2 gate `tail_lower`), and `E_1(K) = 3`.
- `E_1(H) ≥ 3 − v` (Weyl). The Ritz values of `PHP` satisfy `μ_1 ≥ E_1(H)` (Cauchy interlacing) and `E_0 ≤ μ_0 ≤ μ̃`.
- `φ̃ ∈ P` is my rational Ritz proposal: a fixed-point iteration rounded at `10⁻¹³⁰`, stopped at step change `< 10⁻¹²⁰`. `μ̃` is its exact Rayleigh quotient.
- `r = (H − μ̃)φ̃ = r_P + r_Q`, with `r_Q = QVφ̃` in the first omitted shell.
- `g1 = 3 − v − μ̃` and `gQ = Λ_D − v − μ̃`.

**Lemma 1 (retained angle).** `s_P := sin∠(φ̃, φ) ≤ ‖r_P‖/g1`, where `φ` is the exact Ritz vector. This is Davis–Kahan in `P`.

**Lemma 2 (tail angle).** Write the true ground state as `ψ = αφ + βχ + b`, with `χ ∈ P⊖φ` and `b ∈ Q`.
- The `Q`-projected eigen-equation `(QHQ − E_0)b = −QV(αφ + βχ)` gives `‖b‖ ≤ (‖QVφ‖ + v|β|)/gQ`.
- The `P⊖φ`-projected one, `(P′HP′ − E_0)βχ = −P′VQb`, gives `|β| ≤ v‖b‖/g1`.
- Hence `‖b‖ ≤ ‖QVφ‖/(gQ − v²/g1)` and `sin∠(φ, ψ) ≤ ‖b‖(1 + v²/g1²)^{1/2}`.

**Lemma 3.** `‖QVφ‖ ≤ ‖QVφ̃‖ + v√2 s_P`.

**Lemma 4 (observable).** `|⟨φ̃,zφ̃⟩ − ⟨ψ,zψ⟩| ≤ 2‖z‖(s_P + sin∠(φ,ψ))`, with `‖z‖ ≤ 1`. The trace norm of a difference of two rank-one projections is `2 sin` of their angle, and the angle is subadditive.

The enclosure is `[q − hw, q + hw]`, with `q = ⟨φ̃,zφ̃⟩/⟨φ̃,φ̃⟩` exact and `hw = 2s`. Square roots are rounded upward at `10⁻⁷⁰`, and the ends are rounded outward to denominators `10⁵⁰`.

**Five-part ledger (every point; values in `results.json`).**
- **(a) Seven per-link rows.** The kinetic leakage is exactly 0: every link Casimir preserves `P_D`. The thresholds of the omitted sectors exceeding `D/2` on the link are **123/2** (h1, vL, h3, h2, vR, h4) and **45** (vM) at D=6, and **96** and **69** at D=8. Each row carries the weight of `r_Q` in those sectors.
- **(b) Joint channel.**
  - `ρ_Q²` is the exact sum over shell `D+1`. At D=8, `l=1/10` it is 3.9113e-40; at D=6, `l=1/10`, 3.8048e-29.
  - The product channel `a,b,c ≥ 1` has threshold **48** (D=6) and **145/2** (D=8), with weight 3.30e-45 (D=8, 1/10).
  - The corners are `(D+1,0,0)`, `(0,D+1,0)` and `(0,0,D+1)`; the last has weight exactly 0.
  - The face channels `‖Q l x φ̃‖² = ‖Q l y φ̃‖²` ≈ 1.066e-40 each, with interference `2XY` ≈ 1.779e-40 (positive). The two faces are not in quadrature. The identity `x + y + 2XY = ρ_Q²` and "classes − corners + product = ρ_Q²" are checked exactly.
- **(c) Gauge projection:** exactly 0, with the quaternion fixture.
- **(d) Ritz part.** `ρ_P² ≤ 1.6e-244`. `g1` ranges from 2.80 to 3.00 (Weyl separation `3 − 2|l|`), and `gQ` from 44.80 (D=6) to 69.00 (D=8). The ledger records `s_P`, `s_tail` and the labelled Davis–Kahan comparison `‖r‖/g1`.
- **(e) Arithmetic:** exact Fractions, directed square roots, outward ends.

| D | l | enclosure of `<z>` (preview) | half-width | relative width |
|---|---|---|---|---|
| 6 | ±1/1000 | 3.2407405105782596695012e-8 | 2.744e-30 | 1.693e-22 |
| 6 | ±1/100 | 3.2407177246653347184682e-6 | 2.745e-23 | 1.694e-17 |
| 6 | ±1/10 | [3.2384408590641056e-4, 3.2384408590696286e-4] | 2.761e-16 | 1.705e-12 |
| 8 | ±1/1000 | 3.2407405105782596695012e-8 | 5.738e-40 | **3.541e-32** |
| 8 | ±1/100 | 3.2407177246653347184682e-6 | 5.739e-31 | **3.542e-25** |
| 8 | ±1/10 | 3.2384408590668671036605e-4 | 5.765e-22 | **3.560e-18** |

The exact D=8, `l=1/10` enclosure is `[32384408590668670739207024396909057502519141149/10^50, 8096102147667167713625899614386317677247381871/(25·10^48)]`.

- Every enclosure is positive, so it excludes 0 and the sign is certified at every grid point. `<z>` is even in `l` at `l1 = l2`.
- The `−l` certificate equals the `+l` one exactly.
- D=8 lies inside D=6 at every point (observed).
- The **maximal D=8 relative width is 3.5602e-18**, against the frozen `1/10^16`: **margin 28.09**.
- **Labelled comparison.** With the full-residual Davis–Kahan angle alone (separation `3 − 2|l|`), the D=8 relative width at `l = ±1/10` would be **8.72e-17**, a margin of only 1.147. The tail angle is more than 20 times smaller than the Davis–Kahan angle. The frozen target therefore discriminates between a tail-comparison certificate and a bare Davis–Kahan one.

## 5. Item 3: the Z³ 1×2 loop

- **Geometry** (check `z3_rectangle_geometry`). The rectangle is the xz face `W` at the fine origin plus the xz face at `e_x`. Its six links are `(0,x)`, `(0,z)`, `(e_z,x)`, `(e_x,x)`, `(e_x+e_z,x)` and `(2e_x,z)`, all owned by `R = {0, e_z}`.
  - Both faces are omitted (xz faces are never selected), anchored at 0, and among the 10 faces with owner set exactly `R`.
  - Seven anchors are incident on `R`, and 82 omitted faces meet `R`.
  - No face has the rectangle as its link set, so `E[W_{1×2} W_f] = 0` for every `f`.
- **First order.** `Tr(P_R W_{1×2}) = Tr(ρ^(1)_R W_{1×2}) = 0`, so the first-order coefficient is exactly 0 in every box, by single occurrence and centre grading, with Kato per box.
- **Bound.** `|ω(W_{1×2})| = |Tr((ρ_R − P_R − ρ^(1)_R)W_{1×2})| ≤ K_2′τ²`, with `K_2′` read from the AY1 gate and recomputed from its five items (equal). This holds for every F1 and F2 box (AY1 forward F11–F14, uniform in N and cutoff, passed to the untruncated vector by AV1 F22) and for the limit (the AY1/AY2 ball). At the cap it is ≈ **1.34175e-12**, tier `exact_first_order`, with no sign.
- **Evenness.** `|C ∩ E₃| = 6` (area 2), so the AW1 flip lemma gives evenness in every open centered whole-star box and on-site cutoff at `kappa=0`. BB2 item 1 at each sign gives the limit. F2 is not claimed. Evenness gives no remainder bound.
- **Formal second-order coefficient** (`formal_second_order_coefficient`, no sign, no third-order remainder), by two routes:
  - Route 1, Z³ Rayleigh–Schrödinger with both faces at `−(τ/3)W_f`: energies 24 and 36 in delta units give `2⟨W_{1×2}Ω,ψ₂⟩ + ⟨ψ₁,W_{1×2}ψ₁⟩ = E[xyz](4/7776 + 3/7776) = 7/124416`.
  - Route 2: the graph coefficient `7/216` of `l1 l2` under `τ_FG = τ/24` gives `7/216/576 = 7/124416` ≈ 5.6263e-5.

## 6. Item 4: the electric band on R

- **Lower endpoint** (tier `first_order_distance_from_product`):
  - `h_R ≥ 6Q_R`, from I1: one link at `j=1/2` costs `8·¾ = 6` delta.
  - The pure-reference Fuchs–van de Graaf inequality `(½)‖ρ−P‖₁ ≤ sqrt(Tr Qρ)`. For pure `ρ` it is the rank-one formula. For mixed `ρ` it follows by convexity and concavity of `sqrt`. It is checked on exact qubit fixtures, where it is equivalent to `|c|² ≤ p(1−p)`.
  - Together these give `ω(h_R) ≥ (3/2)‖ρ_R − P_R‖₁²`.
  - The distance satisfies `‖ρ_R − P_R‖₁ ≥ L = sqrt10_lo·|τ|/72 − K_2′τ²`. This is exactly the AY2 gate lower end, for the limit (AY2 item 2 with BB2 items 2–3), and the same rational bounds every F1 and F2 box (AY1 F11–F14, AV1 F22).
- **Upper endpoint** (tier `crude_majorant`): AQ1 HNM-AQ1.1 with the 7 incident anchors gives `2·7·(7|τ|) = 98|τ|`. The generic `56|τ||R| = 112|τ|` is valid but not frozen. It passes to the limit by lower semicontinuity: each `Tr(ρ h_R Q_L)` is trace-norm continuous and at most 98|τ|, and the supremum over `L` is the monotone limit.
- **Exact endpoints at τ = ±10⁻⁸** (identical at both signs, for every F1 and F2 box and the limit):
  - lower `(3/2)L²` = 99536…281/346107…000 ≈ **2.875866e-19** (full rational in `results.json`);
  - upper **49/50000000** = 9.8e-7.
- **Formal per-link values** (labelled formal).
  - For a link `e`, the second-order value of `8C_e` is `n_e τ²/3456`, with `n_e` the number of omitted faces through `e`: 4 minus the selected faces through it.
  - On the 48 links of `R` the histogram is `n_e = 2`: 4 links (the y-links at `r=1,2`, `s=0`), `3`: 16, `4`: 28, with `Σn_e = 168`.
  - The formal total is **`7τ²/144`** ≈ 4.861e-18 at the cap, inside the band.
  - The obstruction to a tight enclosure: the only admitted upper end for the unbounded `h_R` is first order.

## 7. Item 5: 2+1 dimensions (declared model)

- **Factorization** (check `dimension_2p1_factorization`):
  - single-site factors own `(p,x)` and `(p,y)`;
  - each face is its own term on the owner set `{p, p+e_x, p+e_y}`;
  - three faces per site; star = union of the owner sets through a site = 7 sites;
  - each interior link lies in two faces; maximal support `p = 3`;
  - per-site sum `J = 3·|τ|/3 = |τ|`, with the AM2 unit on-site gap (the free gap 6 is not used).
- **AM2 counting for general `p`** (AM2 report §2): `2^p` output supports, `p‖c‖_a` per collection, `(p+1)/|I_l|` for the second placement. This gives

  `L_k(p) = 2^p (2p)^k (1 + k(p+1)/p)`, `G_p(t) = 2^p e^{2pt}(1 + 2(p+1)t)`, `G_p′(t) = 2^p e^{2pt}((4p+2) + 4p(p+1)t)`,

  checked coefficient-wise to order 30. At `p = 4` these reproduce AM2's `16·8^k(1+5k/4)`, `16e^{8t}(1+10t)` and `16e^{8t}(18+80t)`, and `148/7` and `352` from `e^{1/8} < 8/7`.
- **p = 3:** `L_k = 8·6^k(1+4k/3)`, `G_3 = 8e^{6t}(1+8t)` and `G_3′ = 8e^{6t}(14+48t)`.
- **Termination order 6.** The creation-algebra fixture gives `ad_C⁶(V)Ω = −6!|111⟩` (sign `(−1)^p`) and `ad_C⁷(V) = 0`. The p=4 anchor gives `ad_C⁸(V)Ω = 8!|1111⟩` and `ad_C⁹ = 0`.
- **At R = 1/64:**
  - `G_3(R) = 9e^{3/32} ≤ 9.884566262770`;
  - `G_3′(R) = 118e^{3/32} ≤ 129.5976465563`;
  - `e^{3/32}` is bracketed by a 40-term Taylor sum with a geometric tail; its 32nd power brackets `e³`, which pins the exponent.
- **Cap.** The self-map `J G_3(R) ≤ R` binds: `|τ| ≤ 1/(576e^{3/32})`, with directed lower bound **cap ≈ 1.580747155e-3** (exact rational in `results.json`). Both conditions hold there. The exclusion `2J G_3′(R) < 1` alone would allow up to `1/(236e^{3/32})` ≈ 3.8581e-3.
- **Not claimed.** No finite-volume ground-state or gap theorem in 2+1D (obligation).
- **What transfers.**
  - Verbatim, being algebraic: the E₂ flip identity, the SU(2) Peter–Weyl parity algebra, the AM2 counting (recounted) and the AV2 window kernel (a one-dimensional spectral identity).
  - Needing their own contracts: the finite-volume theorem, the AQ chain, the node and the dictionary (`g²` has mass dimension).

## 8. Item 6: obligations and no-transfer rows

**Obligations.**
- The area law: no zero-free region of the reduced density is admitted.
- A certified sign of the Z³ 1×2 mean: a uniform fourth-order remainder is needed, since the third order vanishes by evenness.
- A tight electric enclosure: a second-order upper bound for the unbounded `h_R`.
- The site-blocked uniform 3+1D regime: its own contract.
- The 2+1D finite-volume theorem: a 2D finite-volume prescription, the on-site domains and AM2 §§4–6 re-verified.
- The 2+1D AQ chain, node and dictionary.

**No-transfer row.** The Einstein–QED rounds share no equation with this chain.

## 9. Scaling (`τ → τ/100`)

| quantity | ratio | bracket |
|---|---|---|
| band lower | ≈ 9939.60 | [9500, 10500] ✓ |
| band upper | exactly 100 | ✓ |
| Z³ formal term | exactly 10⁴ | ✓ |
| graph coefficients, 2+1D constants | 1 | ✓ |

## 10. Predictions (the post-comparison flags any difference)

| quantity | prediction |
|---|---|
| `<W_1>` table | 1/6, −5/864 (l1³), 1/4212 (l1 l2²); nothing else through order 4 |
| `<z>` table | 7/216 (l1 l2), −349/303264 (l1³l2 and l1 l2³) |
| `<C_shared>` table | 1/48 (l1², l2²), −5/4608 (l1⁴, l2⁴), −49/438048 (l1²l2²) |
| second order at l1=l2 | `<z>` 7/216; `<C_shared>` 1/24 |
| D=8 relative widths | ≈ 3.5e-32, 3.5e-25, 3.56e-18 (ratio to target ≤ 1/28) with a tail-comparison certificate; ≈ 1.8e-17 expected with an AZ2-type Eckart angle; ≈ 8.7e-17 with bare Davis–Kahan |
| `<z>` centres | 3.2407405105782597e-8, 3.2407177246653347e-6, 3.2384408590668671e-4 |
| Z³ 1×2 | first order 0; formal 7/124416 (label formal); bound K_2′τ² ≈ 1.34175e-12 |
| band at ±10⁻⁸ | [≈2.875866e-19, 9.8e-7]; formal 7τ²/144 |
| 2+1D | J=\|τ\|, p=3, 3 faces/site, 7-site star, termination order 6, G_3(R) ≈ 9.88457, G_3′(R) ≈ 129.598, cap ≈ 1.58075e-3 |

**Flagged as errors:**
- a table entry that differs from these, or differs between D=6 and D=8;
- a parity claimed from the vM flip alone;
- an enclosure disjoint from mine;
- a D=8 width above `1/10^16` labelled as meeting it;
- a formal Z³ coefficient other than 7/124416, or one given a sign;
- a band upper end `112|τ|`;
- a lower end with `K_2′τ²/2` or from the AY2 limit distance asserted as a gate sentence for a finite box;
- 3+1D constants (28|τ|, 148/7, 352, order 8, `e^{1/8}`) under the 2+1D label.

## 11. What I will require of the producer

1. The graph Hamiltonian terms named with their coefficients, the free reference in the same code path, zero truncation shown at both cutoffs, never fitted.
2. The two one-link flips (h1 for `l1`, h2 for `l2`) and the parities checked on the two-variable table.
3. Every enclosure with the five-part ledger, its exact Ritz inputs and a gap lemma that states `3 − 2|l|` and the tail `m_{D+1}`. Widths are reported at D=6 and targeted at D=8.
4. The 1×2 rectangle exactly as frozen, its first order 0, the AY1/AY2 bound with source and tier, evenness from AW1 and BB2 only (F1 and the limit), and the formal coefficient labelled.
5. The band with the frozen premises, the inline Fuchs–van de Graaf proof, the cutoff passage and lower semicontinuity made explicit, exact endpoints at both signs, and the formal per-link values from the I1 classes.
6. The 2+1D recount from the AM2 counting with its own directed exponential, the cap under both conditions at `R = 1/64`, and the obligation row.
7. The template once, the gate fields as frozen, and every control as a damaging mutation.

## 12. Producer-error checklist

1. **Wrong graph:**
   - the one-face or equal-coupling tables under the independent-coupling label;
   - `rho ≠ 1`;
   - a Casimir sum with the shared link counted as `4C_U + 4C_V` without the cross term.
2. **A parity "proved" at `l1=l2`, or from the vM flip.**
3. **A residual that omits the `x`–`y` interference** (quadrature), the product channel, or the retained Ritz part.
4. **Moments on a cube instead of the constrained body Ω** (Round11 Q2–Q3).
5. **The 1×2 rectangle:**
   - anchored at `−e_x` (owner outside `R`);
   - its bound presented as an enclosure of the formal coefficient;
   - evenness claimed for F2.
6. **Band:**
   - a bounded-observable trace-norm constant applied to `h_R`;
   - the generic AQ1 budget;
   - the triage's four coupled faces per link (`Σn_e = 192`, formal `τ²/18`) instead of 168.
7. **2+1D:** the 3+1D radius exponent, `J = 28|τ|`, termination order 8, or a finite-volume gap claimed.
8. **Wording:** "rate" unqualified, "area law" or "string tension" affirmative, the forbidden phrases unnegated.

## 13. Replay

`python3 -B research/round33/skeptic/bd2_check.py --output <absolute fresh dir>` (about 6 s). Normal, `-O` and no-`-B` runs are byte-identical and write no cache. Fourteen source-edit mutations of scratch copies all abort (contract review §5).
