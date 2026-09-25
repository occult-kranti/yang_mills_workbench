# BD1 independent derivation before producer comparison

**Standing.** I wrote this after the BD1 contract froze (`frozen_at` 2026-09-25T05:09:10Z, sha256 `a5c84166…75c1fc`) and before reading anything of either BD1 producer. BD1 is paired: the two producers are the admission routes, and this replay is the skeptic's independent input to the post-comparison. I am a model-agent skeptic with correlated ancestry, not a human reviewer. Human project author: Hruday N M (BUNZEEY).

**Isolation, disclosed.**
- I did not open, list or read `research/round33/forward/bd1/`, `reverse/bd1/` or `forward/bd2/`, except `find` on their `inputs/` (names only) and a sha256 comparison with the repository. Forward and reverse BD1 hold the same 23 files, all byte-identical and equal to the contract-derived list.
- Name-only exposures: `git status` at the start listed another session's untracked `skeptic/bc1_postreview_check.py` (not opened). `git log` printed commit subjects up to 8fe1781 (the BC1 gate); `git show --stat 9ae1160` printed the abbreviated paths of the BD producer `inputs/` snapshots. No producer file other than `inputs/` was named.
- **The pre-freeze review.** Another session of this role wrote `bd-contract-review.md`/`.json`. I read its markdown up to "Against my own record" and its JSON edit lists, determinations and freeze-run headers. I did not read its "Advisor only: previews" section or `previews_recomputed`. Its determinations state the closed forms of the SU(3)/SO(3) coefficients, that the SU(5) fourth-order coefficient is nonzero, the N=2 flip-set counts and the Z2 ambiguity. I read them before computing, so my independence from that review is limited to derivation and code. No code of `/tmp/claude-0/skeptic-bd-private/` was opened or reused (I saw only its directory name).
- Nothing under `research/round33/experts/` was read.
- After my values were final, a `git status` filtered to exclude `forward/` and `reverse/` lines listed the untracked directories `experts/historical/assistant-3/` and `experts/modern/assistant-3/` (names only, not opened). Nothing was changed afterwards except this disclosure and the freeze hashes.
- **Scratch.** Private folder `/tmp/claude-0/skeptic-bd-replay-private/`: prototypes `groups_proto.py` (moments and one-plaquette series), run outputs and `srcmut/` (the source-edit harness). Not evidence, not a premise.

**Sources.**
- The frozen contract, `advisor/selection-bd1.md` and `advisor/plan.json` (vocabulary recorded in the program, plan sha256 `7d71bfcb…75c9` at the freeze commit).
- Premises: the AW1 gate, the AW1 forward report §§1–4 and the AW1 reverse report and skeptic review (for the flip set, the one-plaquette fixture and the sign convention); the AW2, AZ1, AZ2, AY2 and BB2 gates; the BB2 forward report; the I1 report; the BA1 and BB2 contracts for the inherited control semantics.
- `bd1_check.py` imports nothing from any producer, tool or earlier round.

**Exactness.** Every value is from `bd1_check.py`: 57 checks, 22 controls as 88 damaging mutations with 4 positives, byte-identical under `-B`, `-B -O` and plain `python3`. Decimals are previews.

## 1. Model and frozen convention

- **One-plaquette models.** `H_FG(G) = 32 C_2 − (tau/3) W` on class functions of the holonomy, in the orthonormal character basis. `32 C_2` acts on `chi_r` by `32 C_2(r)` (four links, each `8 C_2`).
- **Casimirs.** For SU(N), with `lambda` a U(N) highest weight modulo the determinant: `C_2(lambda) = ½[Σλ_i² + Σ(N+1−2i)λ_i − (Σλ_i)²/N]`, so `C_F = (N²−1)/(2N)` and the adjoint gives `N`. For U(1), `n²`. For SO(3), `l(l+1)`. For Z2, `0` on the even state and `1` on the odd state.
- **Wilson variables.**
  - SU(N): `W = (chi_□ + chi_□*)/(2N)`.
  - U(1): `cos theta`.
  - Z2: the sign character.
  - SO(3): `chi_1/3`, where `chi_1 chi_l = chi_{l−1} + chi_l + chi_{l+1}`, so `W` has a diagonal part.
- **Sign.** The creation sign is `psi = e^{−C} Omega_0`, so `c^(1) = −(tau/3)/(32 C_F) W Omega_0` and `omega(W) = −2 Re(W Omega_0, c^(1)) = +(2/3) E[W²]/(32 C_F) tau`. The literal display `2(W Omega_0, c^(1))` gives the negative of this for every group (check `creation_sign_convention`).
- **Box models.** `H^G_N` has `8 C_2` on every owned link of the open centered whole-star box and `−(tau/3) W_f` on every retained omitted face (selected faces 0). Each box has its own Kato radius; no AM2, AV1 or AQ statement is made for `G ≠ SU(2)`.

## 2. Haar moments: three routes (item 3)

| route | method |
|---|---|
| characters | `E[W^k] = ⟨chi_0, W^k chi_0⟩`: iterate `W` on the trivial character with the U(N) Pieri rule (`□`: add a box; `□*`: remove one, weights modulo the determinant), Clebsch–Gordan for SO(3), charge shifts for U(1), `sign·sign=1` for Z2 |
| weyl_integration | constant-term extraction with the one-sided Weyl factor `Π_{i<j}(1−z_j/z_i)` (valid for symmetric integrands). SU(N) keeps every monomial `z^{c(1,…,1)}` (the trivial character on the SU(N) torus); U(1) takes the constant term; SO(3) uses `CT[f(z)(1−z)]`; Z2 sums over the two elements |
| third (labelled) | Frobenius/Schur–Weyl: `E[chi^a conj(chi)^b] = Σ f^λ f^μ` over `λ⊢a, μ⊢b` (at most N rows, `λ−μ = c(1^N)`), with hook-length counts; central binomials for U(1); for SO(3), `chi_vector = chi_{1/2}² − 1` on SU(2) with Catalan moments |

All three routes agree exactly for every group and every `k ≤ 5` (check `moments_three_routes_agree`).

| G | C_F | E[W] | E[W²] | E[W³] | E[W⁴] | E[W⁵] |
|---|---|---|---|---|---|---|
| SU(2) | 3/4 | 0 | 1/4 | 0 | 1/8 | 0 |
| SU(3) | 4/3 | 0 | 1/18 | **1/108** | 1/108 | 5/1296 |
| SU(4) | 15/8 | 0 | 1/32 | 0 | 7/2048 | 0 |
| SU(5) | 12/5 | 0 | 1/50 | 0 | 3/2500 | 1/50000 |
| U(1) | 1 | 0 | 1/2 | 0 | 3/8 | 0 |
| Z2 | 1 | 0 | 1 | 0 | 1 | 0 |
| SO(3) | 2 | 0 | 1/9 | **1/27** | 1/27 | 2/81 |

- SU(2) reproduces the AW1 values `0, 1/4, 0, 1/8`.
- **Trap (labelled check `weyl_route_torus_trap`).** Extracting only the exponent 0, i.e. integrating on the U(N) torus, drops the determinant terms. It gives `E[W³]=0` for SU(3), `E[W⁴]=3/1024` instead of `7/2048` for SU(4), and `E[W⁵]=0` for SU(5). A reverse route on the wrong torus would silently turn the SU(3) obstruction into a parity transfer and erase the SU(5) fourth-order coefficient.

## 3. First-order coefficients (item 3; tier exact_first_order)

The coefficient is `c1(G) = 2(1/3)E[W²]/(32 C_F)`. Both routes give the same rational, and so does the Rayleigh–Schrödinger series on `H_FG(G)`. The reason is that `W Omega_0` is an exact `32 C_2` eigenvector at `32 C_F`, and `E[W]=0` for every group.

| SU(2) | SU(3) | SU(4) | SU(5) | U(1) | Z2 | SO(3) |
|---|---|---|---|---|---|---|
| **1/144** | **1/1152** | **1/2880** | **1/5760** | **1/96** | **1/48** | **1/864** |

- For `SU(N)` with `N ≥ 3`, `c1 = 1/(48N(N²−1))`.
- The same value holds on `H^G_N` for any retained face: `psi_1 = (1/3)Σ_f W_f Omega_0/(32 C_F)`, and single occurrence leaves only `f = W`.
- The SU(2) value `1/144` is a check of the convention, not a transferred value.
- **Z2 normalization discriminates** (check `z2_normalization_discriminates`). The rejected readings give different values: "electric term 1 on the odd state" (face energy 4) gives `1/6`, and "`1 − sigma^x`" (face energy 8) gives `1/12`.

## 4. One-plaquette series and the obstruction cells (items 2 and 4)

**Series.** Rayleigh–Schrödinger about the trivial character, on the class functions reachable in 6 steps (7 for the stability test). This means 7, 28, 50, 80, 13, 2 and 7 irreps. The coefficients are unchanged when the basis grows, so the truncation error is zero. Every series satisfies Hellmann–Feynman, `omega(W) = −3 dE/dtau`, order by order.

| G | ω(W): order 1 | order 2 | order 3 (labelled) | order 4 | dω(W²)/dτ at 0 |
|---|---|---|---|---|---|
| SU(2) | 1/144 | 0 | −5/11943936 | 0 | 0 |
| SU(3) | 1/1152 | **1/589824** | 13/15288238080 | −77/9393093476352 | **1/6912** |
| SU(4) | 1/2880 | 0 | 41/143327232000 | 0 | 0 |
| SU(5) | 1/5760 | 0 | 29/8026324992000 | **1/63403380965376** | 0 |
| U(1) | 1/96 | 0 | −7/7077888 | 0 | 0 |
| Z2 | 1/48 | 0 | −1/221184 | 0 | 0 |
| SO(3) | 1/864 | **1/331776** | 1/429981696 | −55/2972033482752 | **1/2592** |

- SU(2) reproduces the AW1 one-plaquette fixture `−5/11943936`, parsed from the AW1 forward report.
- **Pieri tables certified by the Weyl character formula.** For every irrep of the SU(N) bases (N = 2..5), `chi_□ chi_λ` and `chi_□* chi_λ` equal the Pieri sums as GL(N) bialternant identities at two exact rational points. That is 660 identities.

**Closed forms (SU(3), SO(3)).** `W Omega_0 = (32 C_F) R W Omega_0` exactly, so:
- `dω(W²)/dτ|₀ = 2Re⟨(W²−E[W²])Ω, ψ₁⟩ = (2/3)E[W³]/(32 C_F)`;
- `ω₂ = 2⟨WΩ, ψ₂⟩ + ⟨ψ₁, Wψ₁⟩ = E[W³]/(3(32 C_F)²)`.

From the Weyl-route moments:

| G | E[W³] | dω(W²)/dτ | ω₂ |
|---|---|---|---|
| SU(3) | 1/108 | 1/6912 ≈ 1.4468e-4 | 1/589824 ≈ 1.6954e-6 |
| SO(3) | 1/27 | 1/2592 ≈ 3.8580e-4 | 1/331776 ≈ 3.0141e-6 |

Both closed forms equal the series. Both coefficients are nonzero, so `omega(W)` is not odd in `tau` for SU(3) or SO(3), and the first-order parity fails for them.

**SU(5): parity without flip.**
- `E[W³]=0`, so the parity column is a transfer. By the `Z_5` grading (an `N`-ality count `#□ − #□* ≡ 0 mod 5` on closed paths), both SU(3)/SO(3) coefficients vanish.
- The first possible nonzero even order is 4. In the Brillouin–Wigner form, `E₅ = (−1/3)⁵⟨WΩ,(RW)⁴Ω⟩`: every product term needs a closed path of length 2 and one of length 3, and the latter vanishes. Then `ω₄ = −15E₅`.
- The only closed 5-step paths are the column path `1 → Λ¹ → Λ² → Λ³ → Λ⁴ → Λ⁵ = 1` and its conjugate, each step with multiplicity 1 and weight `1/10`. The Casimirs are `C_2(Λ^k) = 12/5, 18/5, 18/5, 12/5`.
- Hence

  `ω₄(SU(5)) = 15 · 3⁻⁵ · 2 · 10⁻⁵ · Π_k 1/(32 C_2(Λ^k)) = 1/63403380965376 ≈ 1.5772e-14`,

  equal to the series (check `su5_parity_transfer_flip_obstruction`).
- If a unitary `U` commuted with `32C_2` and reversed `W`, then `E(τ)` would be even and `ω(W) = −3E'(τ)` odd near 0, where the ground state is simple. So no such unitary exists on `H_FG(SU(5))`. The missing central `−1` is the reason; this coefficient is the proof.
- The same path argument gives SU(3)'s `ω₂` exactly: the 3-step column path `1 → □ → Λ² = □* → 1` gives `1/589824`.

**Flip groups.** For SU(2), SU(4), U(1) and Z2, every even-order coefficient through order 4 and `dω(W²)/dτ` vanish (check `flip_groups_even_orders_vanish`).

## 5. Criteria A and B (items 1–2)

**Criterion A (flip).** Let `z` be central with `ρ_fund(z) = −I`, and let `U_E` be the right translation by `z` on every link of `E`.
1. Since `z` is central, `U_E` commutes with left and right translations. It therefore commutes with the electric generators, every link Casimir, every function of them (the on-site cutoff projections) and every endpoint gauge action (`g(Uz)h⁻¹ = (gUh⁻¹)z`). It fixes the constant vector `Omega_0`.
2. A plaquette holonomy containing `k₊` links of `E` forward and `k₋` backward maps to `z^{k₊−k₋} U_f`. Now `ρ_fund(z^{k₊−k₋}) = (−1)^{|f∩E|}`, so `W_f → −W_f` whenever `|f∩E|` is odd.
3. Hence `U_E H^G_N(tau) U_E* = H^G_N(−tau)` in every box and cutoff. On `H_FG(G)` the grading is `(−1)^{N-ality}`, checked to anticommute with `W` for SU(2), SU(4), U(1) and Z2.
4. Inside each box's Kato radius the ground state is simple and analytic, so `omega_{−tau}(W) = −omega_tau(W)`.

Which groups have such a `z`:

| G | central −1 on the Wilson representation | reason |
|---|---|---|
| SU(2), SU(4) | yes, `z = −I` | `det(−I) = (−1)^N = 1` |
| U(1) | yes, `z = −1` | acts on charge 1 as −1 |
| Z2 | yes, the non-identity element | acts on the sign representation as −1 |
| SU(3), SU(5) | no | the centre is `N`-th roots of unity times `I`, and `−1` is not one of them (`det(−I) = −1`) |
| SO(3) | no | the centre is trivial, and the identity acts as `+1` |

**Criterion B (parity).**
- On `H_FG(G)` and on `H^G_N`, each first-order term of `ω(W²)` and of the centred correlations (state, vector-centring, Duhamel and energy terms, as in AW1 F05) is a multiple of `E[W³]`, by single occurrence: a face `f ≠ W` leaves a link covered once, and `∫ρ = 0`.
- **The complex level.** For U(1) and SU(N≥3), the gauge-invariant level at `32 C_F` in a box is spanned by `chi_□(U_g)Ω` and `chi_□*(U_g)Ω` over plaquettes `g`. Four links at `C_F` must form a gauge-invariant 4-cycle; there are no triangles or double edges in Z³. The matrix elements of `V` on this level vanish unless `g = f = h`. The surviving elements are the cubic moments `E[chi^a conj(chi)^b]`, `a+b = 3`.
- These cubic moments are nonnegative integers: SU(3) gives `(1,0,0,1)`, while SU(2), SU(4) and SU(5) give `(0,0,0,0)`. So `E[W³]=0` iff all of them vanish, iff the whole level has zero first-order splitting.
- The one-plaquette check (`criteria_a_b_one_plaquette`): the `W`-compression of the level at `32 C_F` vanishes for SU(2), SU(4), SU(5), U(1) and Z2, and not for SU(3) or SO(3). `C_F` is the minimal nontrivial Casimir in every basis.

**Columns.**

| column | transfer | obstruction |
|---|---|---|
| flip | SU(2), SU(4), U(1), Z2 | SU(3), SU(5), SO(3) |
| parity | SU(2), SU(4), SU(5), U(1), Z2 | SU(3), SO(3) |

## 6. Flip sets (item 5)

**E₃** `= {(p,x): p_y even} ∪ {(p,y): p_z even} ∪ {(p,z): p_x even}`. All 24 classes (orientation × base parity) meet it in 1 or 3 links.

| N | plaquettes owned | met once | met three times | retained whole-star faces |
|---|---|---|---|---|
| 2 | 2335 | 1082 | 1253 | 1344 |
| 3 | 6909 | 3630 | 3279 | 4536 |
| 4 | 15291 | 7348 | 7943 | 10752 |

- N=2 reproduces AW1.
- **Coarse factors** (7 factors, including negative coordinates and `(2,−3,5)`): E₃ meets a 24-link factor in 16 links when `b_z` is even and in 8 when it is odd. So E₃ is not invariant under odd coarse z-translations, which the lemma does not need. All 52 faces meeting a factor are met oddly.
- **E₂** `= {(p,x): p_y even}` on `[−N,N]²`, N = 2, 3, 4 (16, 36 and 64 plaquettes): exactly one link per plaquette.
- **Periodic tori** (check `periodic_odd_side_obstruction`):
  - E₃ on sides (4,4,4) has 0 even plaquettes; on (3,4,4), (4,3,4) and (4,4,3) it has 16 each.
  - E₂ on (4,4) and (3,4) has 0; on (4,3), with the odd side in y, it has 4.
  - These are recorded obstructions, never verifications.

## 7. SU(2) area parity (item 6)

- **Rule.** `U_E W_C U_E* = (−1)^{|C∩E₃|} W_C`. For any spanning surface `S` (a plaquette set with mod-2 boundary `C`), `Σ_{f∈S}|f∩E₃| ≡ |C∩E₃| mod 2`, because interior links are counted twice. Each `|f∩E₃|` is odd, so `A(S) ≡ |C∩E₃|`.
- **Surface independence** needs no homology argument: `|C∩E₃|` depends on `C` alone. A spanning surface exists because the box is contractible.
- **Enumeration** (`area_parity_rule_enumerated`): 216 planar rectangles (1..3 × 1..3, three planes, eight offsets), each also with an alternative surface differing by a cube boundary, plus a bent five-face loop, an L-shape, the W face (3 links in E₃, odd) and the 1×2 rectangle (6 links, even).
- **Boxes.** AW1 F09–F10 at `kappa=0` give `ω_{N,−τ}(W_C) = (−1)^{A(C)} ω_{N,τ}(W_C)` in every open centered whole-star box and on-site cutoff. For the untruncated vectors this uses AM2 uniqueness.
- **Limit.** BB2 item 1 gives whole-sequence trace-norm convergence, at each sign separately, on a finite complete-factor region `Y ⊃ links(C)`. `W_C ∈ B(H_Y)` is bounded, and `U_{E∩Y}` is the same for every `N`, so the identity passes to the limit pointwise. No common subsequence is needed.
- **Centre-even observables** are even in `τ`. Bounded ones follow directly. The Casimirs go through their bounded spectral cutoffs (which commute with `U_E`) and the monotone limit, because trace-norm convergence does not pass an unbounded expectation.
- **Not claimed** for periodic boxes with an odd side, at `kappa ≠ 0`, for F2 or for literal vertex boxes.

## 8. Transfer ledger and obligations (item 7)

- **Ledger.** 28 rows: 7 groups × {flip lemma, parity theorem, first-order coefficient, dictionary}.
  - Each obstruction row names its counterexample: SU(3) and SO(3) by `ω₂`, SU(5) by `ω₄` (flip), and `dω(W²)/dτ` (parity).
  - The dictionary `tau = 96/g⁴`, `alpha = g²/(2a)` is an AZ1/AL1 statement for SU(2) only. It is "not asserted" for every other group.
- **Obligations** (11): the AM2 re-instantiation for each of the six other groups; the AQ chain and dictionary for every group other than SU(2); SU(2) at a nonzero selected triple; periodic odd sides; F2 and literal vertex boxes.

## 9. Scaling (`tau → tau/100`)

| term | ratio |
|---|---|
| first-order terms | exactly 100 |
| SU(3)/SO(3) second-order terms | exactly 10000 |
| SU(5) quartic term | exactly 10⁸ |
| moments | 1 |

## 10. Predictions (the post-comparison flags any difference)

| quantity | prediction |
|---|---|
| moments | the table of §2 (k=1..4 required; k=5 recorded) |
| first-order coefficients | 1/144, 1/1152, 1/2880, 1/5760, 1/96, 1/48, 1/864 |
| SU(3) | E[W³]=1/108; dω(W²)/dτ=1/6912; ω₂=1/589824 |
| SO(3) | E[W³]=1/27; dω(W²)/dτ=1/2592; ω₂=1/331776 |
| SU(5) | E[W³]=0; ω₂=0; dω(W²)/dτ=0; **ω₄=1/63403380965376** (≈1.5772e-14, positive) |
| flip transfer / obstruction | SU(2), SU(4), U(1), Z2 / SU(3), SU(5), SO(3) |
| parity transfer / obstruction | SU(2), SU(4), SU(5), U(1), Z2 / SU(3), SO(3) |
| E₃ counts (N=2,3,4) | 2335/1082/1253/1344; 6909/3630/3279/4536; 15291/7348/7943/10752 |
| E₃ on factors | 16 links (b_z even) / 8 (b_z odd); 52 faces per factor, all odd |
| gate scope | names exactly SU(2), SU(4), U(1), Z2 |

**Flagged as errors:**
- any cell rational different from these;
- `1/144` or `96/g⁴` under another group;
- Z2 at `1/6` or `1/12`;
- `E[W³]=0` for SU(3) (the U(N)-torus trap);
- a zero or negative SU(5) `ω₄`;
- SU(5) called a flip transfer, a parity obstruction, or a flip obstruction resting on the centre alone;
- SO(3) given a central `−1`.

## 11. What I will require of the producers

1. The frozen convention stated with the creation sign and the Z2 reading `C_2 = 1` on the odd state; each cell labelled `H_FG(G)` with `model_is_finite_graph: true` and `transfers_to_aq: false`, its free reference computed in the same code path.
2. Moments `k=1..4` exact by the packet's route. The reverse must integrate on the **SU(N) torus**, keeping `z^{c(1,…,1)}`.
3. Each first-order coefficient and each first-order `tau`-derivative with tier `exact_first_order` and `route_of_computation ∈ {characters, weyl_integration}`. The second- and fourth-order coefficients carry no tier but do carry a `route_of_computation` from the same two values (frozen `tier_mixing_rejected`). A label such as `rayleigh_schroedinger` is rejected.
4. The obstruction cells with nonzero exact values, the SU(5) fourth order included, and the argument that a nonzero even-order coefficient excludes any flip unitary on `H_FG(G)`.
5. Criteria A and B proved on `H_FG(G)` and on `H^G_N`, each box inside its Kato radius. The complex level must be treated whole, with the cubic moments as nonnegative integers.
6. The flip sets enumerated on N=2,3,4 and on the coarse factors, E₂ on `[−N,N]²`, and the odd tori recorded as obstructions.
7. The area parity with surface independence proved, the BB2 passage at each sign, and the Casimirs through bounded cutoffs, in the frozen scope only.
8. The 28-row ledger, the obligations, the template once, the gate fields as frozen with `flip_transfer_scope` naming the four flip groups, and every control as a damaging mutation.

## 12. Producer-error checklist

1. **Wrong Wilson variable:**
   - `W = e^{iθ}` for U(1) gives `E[W²]=0`;
   - `W = chi/N` without `Re` for SU(N≥3) gives `E[W²]=0`;
   - `W = chi_1` without `/3` for SO(3).
2. **Wrong torus** (U(N) instead of SU(N)): drops the determinant terms.
3. **A basis truncated below four steps from the trivial class** for SU(5), which changes `ω₄`.
4. **Casimir normalizations:**
   - the `SU(2)`-adjoint rule applied to SO(3) with `C_2 = l(l+1)/2`;
   - Z2 at 1 or `1−σ^x`;
   - `8 C_F` instead of `32 C_F` for the face energy.
5. **The literal AW1 display sign** (`−c1`).
6. **A central `−1` asserted for SU(5), or an obstruction taken from the centre alone.**
7. **Area parity:** claimed at `kappa ≠ 0`, for odd tori or F2, or taken to the limit through AQ subsequences instead of BB2.
8. **Wording:** "predicts", "confirms", or the forbidden phrases unnegated.

## 13. Replay

`python3 -B research/round33/skeptic/bd1_check.py --output <absolute fresh dir>`. Normal, `-O` and no-`-B` runs are byte-identical and write no cache. Twelve source-edit mutations of scratch copies all abort (contract review §5).
