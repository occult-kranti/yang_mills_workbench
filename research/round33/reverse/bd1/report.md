# Centre-symmetry transfer of the parity theorem, the link-flip lemma and the first-order Wilson mean across gauge groups — BD1 reverse (Weyl-integration route)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted reverse production: the derivations, `check.py` and this report were written by a Claude model agent acting as the BD1 reverse producer under the frozen contract `research/round33/contracts/bd1.json` (sha256 `a5c8416600c49b0728fdca05cd67c3ff2e53d9fd9e146d4305abcd2da775c1fc`). `check.py` verifies that digest before it parses any contract field. This is correlated model-agent work under reverse premise isolation, not independent human review and not formal verification. HNM labels are project aliases.

**Established mathematics used here.** None of the following is claimed as new:
- the Weyl integration formula and the Weyl character formula (determinant ratio);
- the Casimir eigenvalue `(|lambda+rho|^2-|rho|^2)/2`, i.e. the radial part of the Laplacian on class functions;
- Schur's lemma and Peter–Weyl orthogonality;
- the Rayleigh–Schrödinger, Hellmann–Feynman and Duhamel formulas, and Kato's analytic perturbation theory (cited, not machine-checked);
- centre gradings and centre-flip symmetries of lattice gauge theories, which are a known kind of argument, so no priority is claimed for either criterion.

The new work within the declared models is the exact evaluation, group by group, under the frozen convention, and the recorded obstruction cells. Scientific priority is unverified.

## 1. Verdict (reverse half) and headline

**Proposed reverse verdict: `accepted_within_scope`**, with sub-labels `transfer_to_named_model` and `obstruction_recorded`. Admission still needs three things outside this producer: the forward characters route, the exact cell-by-cell comparison of the two tables, and the skeptical review.

All statements are made under the frozen convention: per-link electric term `8 C_2`, face energy `32 C_F`, magnetic term `-(tau/3) W`, and `W = Re chi_fund/dim fund`. They hold only on the named models:
- the one-plaquette finite graphs `H_FG(G)`;
- the group-G whole-star box models `H^G_N`, box by box, inside each box's Kato radius;
- for SU(2), the zero-selected patterned family.

The results are as follows.

1. **Criterion A (flip).** If a central `z` in G has `rho_fund(z) = -I`, then `U_E` built from `z` on the links of `E_3` has the following properties:
   - it commutes with every link Casimir, every endpoint gauge action and every on-site cutoff projection;
   - it fixes the vacuum and sends every `W_f` to `-W_f`.

   Hence `U_E H^G_N(tau) U_E^* = H^G_N(-tau)` in every open centered whole-star box and every cutoff, and `U H_FG(G)(tau) U^* = H_FG(G)(-tau)`. Such a `z` exists for exactly four of the listed groups:
   - **SU(2):** `-I`;
   - **SU(4):** `-I`;
   - **U(1):** `e^{i pi}`;
   - **Z2:** the nontrivial element.

   It does not exist for SU(3), SU(5) or SO(3) (Section 5).
2. **Criterion B (parity).** When `E[W^3] = 0` and single-occurrence orthogonality holds, the following first-order τ-derivatives vanish on `H_FG(G)` and on `H^G_N` in each box:
   - of `omega(W^2)`;
   - of `C(s)` for every `s ≥ 0`;
   - of `c(theta)` for every real θ.

   The state, Duhamel, energy and centring terms each vanish separately, and the first-order splitting of the whole gauge-invariant level at `32 C_F` is zero, including `Im chi_fund`. On `H_FG(G)` these derivatives are nonzero whenever `E[W^3]` is nonzero. `E[W^3] = 0` holds exactly for SU(2), SU(4), SU(5), U(1) and Z2 (Section 6).
3. **Moments and first-order coefficients.** Both come from the Weyl-integration route, as exact rationals (Sections 3–4).

   | group | `E[W^1..4]` | first-order coefficient of `omega(W)/tau` |
   |---|---|---|
   | SU(2) | 0, 1/4, 0, 1/8 | 1/144 |
   | SU(3) | 0, 1/18, 1/108, 1/108 | 1/1152 |
   | SU(4) | 0, 1/32, 0, 7/2048 | 1/2880 |
   | SU(5) | 0, 1/50, 0, 3/2500 | 1/5760 |
   | U(1) | 0, 1/2, 0, 3/8 | 1/96 |
   | Z2 | 0, 1, 0, 1 | 1/48 |
   | SO(3) | 0, 1/9, 1/27, 1/27 | 1/864 |

   The SU(2) value 1/144 is reproduced as a check of the convention. It is not transferred to any other group.
4. **Obstruction cells** (Section 7), all on the one-plaquette models, in exact rationals:
   - **SU(3):** `E[W^3] = 1/108`, `d omega(W^2)/dtau = 1/6912` and `omega_2 = 1/589824`, both nonzero.
   - **SO(3):** `E[W^3] = 1/27`, `d omega(W^2)/dtau = 1/2592` and `omega_2 = 1/331776`, both nonzero.
   - **SU(5):** `E[W^3] = 0`, so its parity column is a transfer. `d omega(W^2)/dtau = omega_2 = 0` by the Z_5 grading. The fourth-order coefficient is `omega_4 = 1/63403380965376 = 1/(2^30 3^10)`, which is nonzero. This is the first even order the Z_5 grading allows, so it is SU(5)'s flip obstruction.
5. **Flip sets** (Section 8).
   - **E_3.** Reverse-derived as one of the exactly two one-coordinate rules that are odd on all 24 plaquette classes. Verified on `Lambda_N` for N = 2, 3, 4 (every owned plaquette and every retained face) and on seven 24-link coarse factors at both z-parities.
   - **E_2.** Meets every plaquette of `[-N,N]^2` exactly once, for N = 2, 3, 4.
   - **Periodic tori with an odd side.** Recorded as obstructions, together with their even seam plaquettes.
6. **SU(2) area parity** (Section 9). At `kappa = 0`, for every loop C bounding a surface of `A(C)` plaquettes:

   `omega_{N,-tau}(W_C) = (-1)^{A(C)} omega_{N,tau}(W_C)`.

   This holds in every open centered whole-star box and every on-site cutoff, and for the limit of the named constructions pointwise at each sign, through the admitted BB2 whole-sequence convergence.
7. **Transfer ledger** (Section 10): 7 groups × 4 equations. The AM2/AQ chain is recorded as an obligation for every group other than SU(2).
8. **Checker** (Section 13).
   - `check.py` runs **64 exact checks**.
   - All **22 contract controls** are executed as damaging mutations, **110** in total, and every one is rejected.
   - The outputs under `-B` and `-B -O` are byte-identical.

## 2. Model, convention and the reverse route

### 2.1 The frozen convention, derived before the contract text was read

`check.py` first derives the Casimir normalization on the torus and the flip-set rules (Section 8). Only then does it parse the contract, and it compares the contract text against those derived values.

**Electric term.** The per-link term is `8 C_2(r)` in `delta` units. On a plaquette character `chi_r` of the holonomy of four distinct links, it gives `32 C_2(r)`. The Casimir normalizations are:

| group | Casimir normalization | Wilson representation | `C_F` | face energy `32 C_F` |
|---|---|---|---|---|
| SU(N) | `C_2(lambda) = (abs(lambda+rho)^2 - abs(rho)^2)/2` in the trace-form metric `abs(mu)^2 = sum mu_i^2 - (sum mu_i)^2/N` | fundamental | `(N^2-1)/(2N)`: 3/4, 4/3, 15/8, 12/5 | 24, 128/3, 60, 384/5 |
| U(1) | `n^2` | charge 1 | 1 | 32 |
| Z2 | 0 on the even state, 1 on the odd state | sign | 1 | 32 |
| SO(3) | `l(l+1)` | vector | 2 | 64 |

The checker also verifies, exactly:
- for each SU(N), the adjoint Casimir is N;
- `C_2(Lambda^k) = k(N-k)(N+1)/(2N)`;
- the Lie-algebra sum `sum_a T_a T_a = C_F I` for generators normalized by `tr T_a T_b = delta_ab/2`.

**Magnetic term.** It is `-(tau/3) W`, with `W = Re chi_fund(U)/dim fund`:
- `W = cos theta` for U(1);
- the sign character for Z2;
- `Tr/3` of the vector representation for SO(3).

**Sign of the first-order vector.** With the AM2/AV1 creation sign `psi = e^{-C} Omega_0`, the first-order creation and the first-order mean are

`c^(1) = -(tau/3)/(32 C_F) sum_f W_f Omega_0` and `omega(W) = -2 Re (W Omega_0, c^(1)) + O(tau^2)`.

The literal display `2 (W Omega_0, c^(1))` gives the negative of every coefficient. That is the inherited AW1 wording defect, and the checker rejects it as a damaging mutation.

### 2.2 The one-plaquette model on the torus

`H_FG(G) = 32 C_2 - (tau/3) W` acts on class functions of one plaquette holonomy. It is labelled `model_is_finite_graph: true` and `transfers_to_aq: false`, and every coefficient it gives is a finite-model value.

The reverse route never uses a character table, a tensor-product multiplicity or a Clebsch–Gordan series. Its ingredients are:

- **Torus coordinates.**
  - SU(N): `x_1..x_N` with `x_1...x_N = 1`. Exponent vectors are taken modulo the diagonal, and a monomial is constant on the torus exactly when all its exponents are equal.
  - U(1): `z`.
  - Z2: `z` with `z^2 = 1`.
  - SO(3): the rotation-angle variable `z = e^{i theta}`.
- **Haar moments by Weyl integration.**
  - SU(N): `E[f] = (1/N!) CT[f prod_{i≠j}(1 - x_i/x_j)]`.
  - SO(3): `E[f] = (1/2) CT[f (2 - z - z^{-1})]`.
  - U(1): `E[cos^k] = 2^{-k} sum_j C(k,j) [2j = k]`, the binomial constant term.
  - Z2: `E[f] = (f(+1) + f(-1))/2`, direct summation.
- **Weyl numerators.** A class function f is carried as `A_f = f a_rho`.
  - For SU(N), `a_rho = sum_w sgn(w) x^{w rho}` with `rho = (N-1,...,0)`, the Vandermonde determinant.
  - For SO(3), `a_rho = 1 - z^{-1}`, the rho-shifted numerator.
  - For U(1) and Z2, `a_rho = 1`.

  By the Weyl character formula `chi_lambda = a_{lambda+rho}/a_rho` (a determinant ratio), the coefficients of `A_f` at dominant exponents are the coefficients of f on the Weyl characters. Every numerator is checked to be antisymmetric.
- **Electric operator.** The radial part of the Laplacian is conjugate by `a_rho` to the flat torus Laplacian shifted by `abs(rho)^2`. On numerators, `H_0` therefore multiplies the monomial `x^mu` by `16(abs(mu)^2 - abs(rho)^2)` for SU(N), by `32 k(k+1)` on `z^k` for SO(3), by `32 n^2` for U(1), and by 32 on the odd monomial for Z2.
- **Inner products as constant terms.** `(f,g) = (1/abs(W)) CT[conj(A_f) A_g] = (1/abs(W)) sum_mu A_f[mu] A_g[mu]`, where `abs(W)` is the Weyl-group order. This is the Weyl integration formula with `abs(a_rho)^2` as the density.
- **Rayleigh–Schrödinger, in intermediate normalization.** With `V = -(1/3)W` and `R = Q H_0^{-1} Q`:
  - `E_n = (Omega_0, V psi_{n-1})`;
  - `psi_n = R(-V psi_{n-1} + sum_{k=1}^{n-1} E_k psi_{n-k})`;
  - `omega(A)` is the quotient of the series `(psi, A psi)` and `(psi, psi)`.

  The free values `omega_0(W) = E[W]` and `omega_0(W^2) = E[W^2]` come out of the same code path.

  Hellmann–Feynman, `omega_n = -3(n+1) E_{n+1}`, gives an internal second evaluation of every coefficient through order 4. It agrees exactly for all seven groups.

**Truncation.** There is none. The numerators carry every monomial, and the order-n coefficient involves finitely many.

### 2.3 Reverse analysis: from the desired transfers back to sufficient premises

- **Flip.** The goal is a unitary that commutes with the electric term and the gauge actions, fixes `Omega_0`, and reverses every `W_f`.
  - Products of per-link central multiplications are the natural candidates. They act as scalars on Peter–Weyl blocks, and they commute with translations because they are central.
  - The requirement reduces to a central `z` with `rho_fund(z) = -I`, plus a link set E meeting every plaquette oddly.
  - **Kernel of the inverse problem (Newton lens).** E is determined only up to a centre gauge transformation: two cyclic one-coordinate rules exist (Section 8).
  - **Necessity on the models.** Any such unitary would make `omega(W)` odd in `tau`. So a nonzero even-order coefficient on `H_FG(G)` refutes every candidate unitary, not only central ones. This is how SU(3), SO(3) and SU(5) are classified: the absence of a central -1 is recorded as the reason, and the proof of non-transfer is the coefficient.
- **Parity.**
  - Every first-order term is a pairing of `W_f Omega_0` against a vector built from `W^2 Omega_0`, `W alpha_theta(W) Omega_0` or `Omega_0`.
  - After single-occurrence orthogonality, only `f = W` survives. What survives is proportional to `E[W^3]`, or to cubic moments on the complex level.
  - So `E[W^3] = 0` is sufficient. On `H_FG(G)` it is also necessary, because the state term is `(2/3)E[W^3]/(32 C_F)`.

## 3. Haar moments by Weyl integration (exact)

Every entry below is computed twice and the two computations agree exactly:
- (i) as the constant term against the full density (SU(N) and SO(3)), as the binomial constant term (U(1)), or by summation (Z2);
- (ii) as the factorized numerator constant term `(1/abs(W)) CT[conj(a_rho) W^k a_rho]`.

The route of computation is `weyl_integration` for every entry, and no entry carries a tier.

| group | Wilson rep | `E[W]` | `E[W^2]` | `E[W^3]` | `E[W^4]` |
|---|---|---|---|---|---|
| SU(2) | fundamental | 0 | 1/4 | 0 | 1/8 |
| SU(3) | fundamental | 0 | 1/18 | 1/108 | 1/108 |
| SU(4) | fundamental | 0 | 1/32 | 0 | 7/2048 |
| SU(5) | fundamental | 0 | 1/50 | 0 | 3/2500 |
| U(1) | charge 1 | 0 | 1/2 | 0 | 3/8 |
| Z2 | sign | 0 | 1 | 0 | 1 |
| SO(3) | vector | 0 | 1/9 | 1/27 | 1/27 |

For SU(5) the checker also computes the higher moments, as supplementary values: `E[W^5] = 1/50000` and `E[W^6] = 3/25000`.

**Cubic moments.** Write `m_{a,b} = E[chi^a conj(chi)^b]` with `a + b = 3`. These are constant terms, and each is a nonnegative integer. The checker verifies that `E[W^3] = (2d)^{-3} sum_a C(3,a) m_{a,3-a}`, and hence that `E[W^3] = 0` exactly when every `m_{a,b}` vanishes. The values are:
- **SU(3):** `m_{3,0} = m_{0,3} = 1` and `m_{2,1} = m_{1,2} = 0`;
- **SO(3):** all four are 1;
- **SU(2), SU(4), SU(5), U(1), Z2:** all vanish.

## 4. First-order coefficients (tier `exact_first_order`, route `weyl_integration`)

The formula is `2 (1/3) E[W^2]/(32 C_F)`. For each group the checker computes it three ways, and all three are equal: from the moment, as the torus Rayleigh–Schrödinger `omega_1`, and as the Hellmann–Feynman value `-6 E_2`. The decimals are truncated previews only.

| group | `E[W^2]` | `32 C_F` | coefficient | preview |
|---|---|---|---|---|
| SU(2) | 1/4 | 24 | 1/144 | 6.94444444444e-3 |
| SU(3) | 1/18 | 128/3 | 1/1152 | 8.68055555555e-4 |
| SU(4) | 1/32 | 60 | 1/2880 | 3.47222222222e-4 |
| SU(5) | 1/50 | 384/5 | 1/5760 | 1.73611111111e-4 |
| U(1) | 1/2 | 32 | 1/96 | 1.04166666666e-2 |
| Z2 | 1 | 32 | 1/48 | 2.08333333333e-2 |
| SO(3) | 1/9 | 64 | 1/864 | 1.15740740740e-3 |

**Where the coefficients live.** Each coefficient is a value on `H_FG(G)`. In `H^G_N` with W a retained face, only `f = W` pairs with W, by single-occurrence orthogonality (Section 6). The first-order coefficient of `omega_N(W)` is therefore the same number, in each box inside its Kato radius. It is never a lattice-limit value for any group other than SU(2).

**SU(2) convention check.** The torus route reproduces the admitted SU(2) values: `omega_1 = 1/144` (AW1 gate); `omega_3 = -5/11943936` and `omega(W^2)_2 = 7/331776` (AW1 reverse report); `omega_5 = 289/6604518850560` and `E_2 = -1/864` in `delta` units (the AW1 skeptic's `-tau^2/6912` in alpha units, times 8). These are read from the snapshots and used only as a check of the convention on SU(2). No SU(2) value (1/144, `tau = 96/g^4`, `alpha = g^2/(2a)`) is used for another group.

## 5. Criterion A: the flip lemma

**Theorem A.** Let G be listed with Wilson representation `rho`, and suppose a central `z` in G has `rho(z) = -I`. Let E be a set of links that meets every plaquette of the box in an odd number of links. Put `(Gamma_l psi)(...,U_l,...) = psi(...,z U_l,...)` and `U_E = prod_{l in E} Gamma_l`. Then:

1. **Unitarity and the vacuum.** `U_E` is unitary, because Haar measure is invariant under multiplication by `z`. It fixes the vacuum `Omega_0 = 1`.
2. **Casimirs and cutoffs.** On the Peter–Weyl block of an irrep r at link l, `Gamma_l` acts as the scalar `rho_r(z)` (Schur's lemma, z central). Therefore `U_E` commutes with every link Casimir, with every function of the Casimirs (including every on-site spectral cutoff projection), and with `H_0`.
3. **Gauge actions.** z is central, so `Gamma_l` commutes with left and right translations. `U_E` therefore commutes with every endpoint gauge action.
4. **Face terms.** For a face `U_f = U_1 U_2 U_3^{-1} U_4^{-1}`, the map `U_l -> z U_l` on `f cap E` gives `U_f -> z^s U_f`, where s is the signed count. Since `rho(z^{±1}) = -I`, we have `W_f -> (-1)^{abs(f cap E)} W_f = -W_f`.

Consequently:
- `U_E H^G_N(tau) U_E^* = H^G_N(-tau)` in every open centered whole-star box `Lambda_N`, and every on-site cutoff compression commutes with `U_E`;
- on the one-plaquette model, `U H_FG(G)(tau) U^* = H_FG(G)(-tau)` with `(U f)(U_P) = f(z U_P)`.

Wherever the ground eigenvalue is simple, `U_E psi(tau)` is a phase multiple of `psi(-tau)`. Hence `omega(W)` is odd in `tau`, and `omega(W^2)`, `C(s)` and `c(theta)` are even. By Kato analyticity inside the radius, the even Taylor coefficients of `omega(W)` vanish.

**Kato radii (explicit, box-dependent, not uniform in N).**
- **One-plaquette model.** The ground of `H_0` is simple, with gap `32 C_min`, and `norm(V)` is at most `abs(tau)/3`. The ground is therefore simple for `abs(tau)` below `48 C_min`: SU(2) 36, SU(3) 64, SU(4) 90, SU(5) 576/5, U(1) 48, Z2 48, SO(3) 96.
- **Box model `H^G_N`.** The full-space gap is `8 C_min`, and `norm(V)` is at most `abs(tau) F_N/3` with `F_N = 21(2N)^3` retained faces. The ground is simple for `abs(tau)` below `12 C_min/F_N`. At `N = 2` this is 3/448 for SU(2), 1/84 for SU(3), 15/896 for SU(4), 3/140 for SU(5), 1/112 for U(1) and for Z2, and 1/56 for SO(3). N = 3 and N = 4 are in `results.json`.
- **Minimal Casimir.** `C_min = C_F` for every listed group. For SU(N) this follows because `C(lambda + omega_j) = C(lambda) + C(omega_j) + (lambda, omega_j)`, with all `(omega_i, omega_j)` positive (exact inverse Cartan matrix), and because `C(omega_k) = k(N-k)(N+1)/(2N)` is minimal exactly at `k = 1` and `k = N-1`. This was checked on every dominant label with `lambda_1` at most 3.

**Group by group (exact reasons).** The checker determines each centre exactly by computing a commutant. For SU(N) it uses the Givens rotations with cosine 3/5 and sine 4/5 together with `diag(i, -i, 1, ..., 1)`; for SO(3), two rational rotations about different axes. In both cases the commutant has complex dimension 1, so a central element is a scalar.

| group | central element acting as -1 | exact reason | flip column |
|---|---|---|---|
| SU(2) | `-I` | `det(-I) = (-1)^2 = 1` | transfer |
| SU(3) | none | centre `{zeta I : zeta^3 = 1}` and `rho(zeta I) = zeta I`; `det(-I) = -1` | obstruction: `omega_2 = 1/589824` |
| SU(4) | `-I` | `(-1)^4 = 1` | transfer |
| SU(5) | none | centre acts by fifth roots of unity, none equal to -1 | obstruction: `omega_4 = 1/(2^30 3^10)` |
| U(1) | `e^{i pi}` | abelian; the charge-1 representation sends it to -1 | transfer |
| Z2 | the nontrivial element | the sign character sends it to -1 | transfer |
| SO(3) | none | trivial centre: `c I` with `c^3 = 1` and c real gives `c = 1`, and `rho_vector(I) = I` | obstruction: `omega_2 = 1/331776` |

**Torus reading.** The map `x -> -x` preserves `x_1...x_N = 1` only when `(-1)^N = 1`. The checker records that it is not a map of the SU(3) or SU(5) torus.

**Exact demonstrations for the four flip groups.**
- **One-plaquette model.** `U` fixes `a_rho`, commutes with `H_0`, sends W to -W, and satisfies `U psi_n = (-1)^n psi_n` for n = 0..5. The even coefficients of `omega(W)` vanish through order 4, and the odd coefficients of `omega(W^2)` through order 3.
- **Box faces.** On `Lambda_N` (N = 2, 3, 4), every retained face meets `E_3` in 1 or 3 links (Section 8).
- **Exact holonomy fixtures on the xz face at the origin** (`abs(f cap E_3) = 3`). Each flip sends the Wilson variable to its negative:
  - U(1), with Gaussian-rational links: `W = 26664/27625`;
  - SU(2), with rational unit quaternions: `W = 304/525`;
  - SU(4), with an exact SO(4) element whose trace is 126/85.

## 6. Criterion B: the first-order parity theorem

**Single-occurrence orthogonality.** Suppose a link carries exactly one fundamental (or conjugate) matrix element in a product of face functions. Its Haar integral is then the projector onto the invariants of `rho`. The trace of that projector is `E[chi_fund]`, which is 0 as a constant term, so the integral is 0.

Two distinct plaquettes share at most one link. The checker verifies this on all 2335 owned plaquettes of `Lambda_2`. It follows that:
- for `f ≠ g`, the face f has at least 3 links outside g;
- in any triple of faces that are not all equal, some link occurs exactly once.

The checker also enumerates all 117480 multisets of three faces meeting `R = {0, e_z}` (88 faces, 49 omitted and 3 selected per factor) and finds no exception.

**Theorem B (one-plaquette and box models).** Let `E[W^3] = 0`. Then on `H_FG(G)`, and on `H^G_N` in every box and cutoff inside its Kato radius for any face observable `W = W_g`, the first-order `tau`-derivatives at 0 of the following vanish:
- `omega(W^2)`;
- `C(s) = (chi, e^{-s(H-E)} chi)` for every `s ≥ 0`;
- `c(theta) = (chi, e^{i theta(H-E)} chi)` for every real θ.

Here `chi = (W - omega(W)) psi/norm(psi)`. The four terms vanish separately:
- **state term:** `2 Re (psi^(1), W^2 Omega_0) = (2/3)(32 C_F)^{-1} sum_f E[W_f W^2] = (2/3) E[W^3]/(32 C_F)`, since only `f = W` survives;
- **Duhamel term:** `-s e^{-32 C_F s} (W Omega_0, (V - E_1) W Omega_0) = s e^{-32 C_F s} E[W^3]/3`; the real-time version is `-i theta e^{i 32 C_F theta} E[W^3]/3`;
- **energy term:** `E_1 = -(1/3) sum_f E[W_f] = 0`;
- **vector-centring term:** `omega_1 E[W] = 0`.

`W Omega_0` is an `H_0` eigenvector at `32 C_F`; every numerator monomial of `W a_rho` has that energy, as the checker verifies.

**The whole level, including `Im chi_fund`.** The gauge-invariant level at `32 C_F` is spanned by `chi_fund(U_h) Omega_0` and its conjugate, over the plaquettes h of the box. For complex representations this is `W_h Omega_0` together with `Im chi_fund(U_h) Omega_0`. The reason: `sum_e 8 C(r_e) = 32 C_F` with `C(r)` at least `C_F` on every nontrivial link forces four links with Casimir `C_F`. These are `F` or its conjugate for SU(N), charge ±1 for U(1), the odd state for Z2, and `l = 1` for SO(3). Gauge invariance then forces degree at least 2 at every vertex. Four links with that property form a 4-cycle, and the 4-cycles of `Z^3` are the plaquettes. The checker finds exactly 12 through the origin and no triangles.

By single-occurrence orthogonality, the first-order compression of V to this level is `-(tau/3)` times the cubic moments of each retained face. It is therefore zero on the whole level exactly when `E[W^3] = 0`. The matrix of W on `{chi, conj(chi)}` is:
- **SU(4), SU(5), U(1):** zero;
- **SU(3):** `[[0, 1/6], [1/6, 0]]`, which is `+1/6` on `Re chi` and `-1/6` on `Im chi`. The level splits at first order into shifts `-tau/18` and `+tau/18`;
- **SO(3)** (real, one state per plaquette): W acts as 1/3, a shift of `-tau/9`;
- **SU(2), Z2:** zero.

**Nonvanishing when `E[W^3]` is nonzero (on `H_FG(G)`).** Here `d/dtau C(s) = e^{-32 C_F s}(alpha + beta s)` and `d/dtau c(theta) = e^{i 32 C_F theta}(alpha - i beta theta)`, where `alpha = d omega(W^2)/dtau = (2/3) E[W^3]/(32 C_F)` and `beta = E[W^3]/3`. The two coefficients have the same sign as `E[W^3]`:
- **SU(3):** `alpha = 1/6912`, `beta = 1/324`;
- **SO(3):** `alpha = 1/2592`, `beta = 1/81`.

**Box remark (derived, not a contract item).** With W a retained face of `H^G_N`, the same pairings give `d omega_N(W^2)/dtau = (2/3) E[W^3]/(32 C_F)` in each box inside its Kato radius. They also give `omega_{N,2} = E[W^3]/(3 (32 C_F)^2)`, because `(psi^(1), W psi^(1))` and `2 (W Omega_0, psi^(2))` both reduce to `f = g = W` by the triple lemma. So the SU(3) and SO(3) obstructions are not artifacts of the one-plaquette graph. This remark is checked only through the moments. The contract cells below are the one-plaquette ones.

## 7. Obstruction cells (one-plaquette models, exact; route `weyl_integration`)

### 7.1 SU(3) (mandatory)

- **No central -1.** `det(-I) = -1`, and the centre is `{zeta I : zeta^3 = 1}`.
- **Third moment.** `E[W^3] = 1/108`, because `E[chi^3] = E[conj(chi)^3] = 1`.
- **First-order derivative.** `d omega(W^2)/dtau at 0 = 1/6912`, preview `1.44675925925e-4`. The tier is `exact_first_order`.
- **Second-order coefficient.** `omega_2 = 1/589824`, preview `1.69542100694e-6`. It carries no tier.
- **Closed forms, obtained by reverse analysis of the series `N(tau)/D(tau)`.** They equal the torus Rayleigh–Schrödinger values exactly:
  - `d omega(W^2)/dtau = (2/3) E[W^3]/(32 C_F)`;
  - `omega_2 = E[W^3]/(3 (32 C_F)^2)`, from `N_2 = 2 (W, psi_2) + (psi_1, W psi_1)` with `D_1 = 0`.
- **Recorded.** `omega(W)` is not odd in `tau` on `H_FG(SU(3))`, and the first-order parity fails. The series is `omega = tau/1152 + tau^2/589824 + 13 tau^3/15288238080 - 77 tau^4/9393093476352 + ...`.

### 7.2 SO(3) (mandatory)

- **No central element acting as -1.** The centre is trivial.
- **Third moment.** `E[W^3] = 1/27`, because `E[chi_1^3] = 1`.
- **First-order derivative.** `d omega(W^2)/dtau = 1/2592`, preview `3.85802469135e-4`.
- **Second-order coefficient.** `omega_2 = 1/331776`, preview `3.01408179012e-6`.
- **Closed forms.** The same two closed forms hold with `32 C_F = 64`.
- **Recorded.** `omega(W)` is not odd in `tau`, and the first-order parity fails. The series is `omega = tau/864 + tau^2/331776 + tau^3/429981696 - 55 tau^4/2972033482752 + ...`.

### 7.3 SU(5) (mandatory flip obstruction at fourth order)

- **No central element acting as -1.** The centre acts by fifth roots of unity.
- **Parity column: a transfer.** Every cubic moment vanishes, so `E[W^3] = 0`, and Theorem B applies.
- **Vanishing lower coefficients.** `d omega(W^2)/dtau = 0` and `omega_2 = 0`. The reason is the Z_5 grading: W changes N-ality by ±1, and the order-2m coefficient pairs `2m+1` such steps returning to 0 mod 5. For odd N the first even order that can be nonzero is therefore `N - 1`, which is 4 here. The checker verifies the grade content of every `psi_n`.
- **Fourth-order coefficient.** `omega_4 = 1/63403380965376 = 1/(2^30 3^10)`, preview `1.57720727258e-14`. It is nonzero and carries no tier. Three evaluations agree exactly:
  1. the torus Rayleigh–Schrödinger series;
  2. Hellmann–Feynman, `omega_4 = -15 E_5`;
  3. a closed form from the grading.

  **The closed form.** For SU(5), `E_1 = E_3 = 0`, and three-step closed paths vanish, so `E_5 = (Omega_0, V R V R V R V R V Omega_0)`. Only the words `chi^5` and `conj(chi)^5` return to the trivial class. In five one-box steps, the only chain ending at the trivial class `(1^5)` is the column chain `Lambda^1 -> Lambda^2 -> Lambda^3 -> Lambda^4 -> trivial`. The checker verifies on the torus that each step occurs with multiplicity 1 and that `(Omega_0, chi Lambda^4) = 1`. Hence

  `omega_4 = (10/81) 10^{-5} / prod_k E(Lambda^k)` with `E(Lambda^k) = 384/5, 576/5, 576/5, 384/5`.
- **Recorded.** `omega(W)` is not odd in `tau` on `H_FG(SU(5))`. No unitary commuting with the electric term and reversing W exists on that model: such a unitary would fix the simple vacuum and make every even coefficient vanish. For completeness, the third-order coefficient is `29/8026324992000`.

## 8. Flip sets (exact enumeration)

**E_3 is reverse-derived.** The checker searches all 27 rules of the form "link (p,d) in E iff `p_{sigma(d)}` is even". Exactly two are odd on all 24 plaquette classes (3 orientations × `p mod 2`):
- the cyclic rule: x-links keyed to `p_y`, y-links to `p_z`, z-links to `p_x`;
- the anticyclic rule.

They differ by a centre gauge transformation, which is the kernel of the inverse problem. The contract's `E_3` was parsed only after this search, and it is the cyclic rule.

| box (open centered whole-star) | owned plaquettes | met once | met three times | retained faces (all odd) |
|---|---|---|---|---|
| `Lambda_2` | 2335 | 1082 | 1253 | 1344 |
| `Lambda_3` | 6909 | 3630 | 3279 | 4536 |
| `Lambda_4` | 15291 | 7348 | 7943 | 10752 |

My own enumeration of `Lambda_2` gives the same histogram as the AW1 forward report, a declared premise, which I compared only afterwards.

**Coarse factors.** Seven 24-link factors were checked, with negative coordinates and both z-parities: `(0,0,0)`, `(0,0,1)`, `(1,0,0)`, `(0,1,0)`, `(-1,-1,-1)`, `(2,-3,1)` and `(-2,1,-2)`. Each is met by 52 faces, 49 omitted and 3 selected, and all 52 meet `E_3` in 1 or 3 links.

`E_3 cap factor` has 16 links for even z and 8 for odd z. It is unchanged by coarse x and y translations, which are even fine shifts. Between the two z-parities, the 8 y-links switch. So `E_3` is not invariant under odd coarse translations in z, and the flip lemma does not need that invariance.

**E_2.** `{(p,x) : p_y even}` meets every plaquette of `[-N,N]^2` exactly once: 16, 36 and 64 plaquettes for N = 2, 3, 4. A reverse search finds four one-direction solutions, and `E_2` is one of them.

**Periodic tori with an odd side (obstruction recorded, not verified).** The counts of plaquettes met evenly are:
- `E_2`: 4 on 4×3 (the seam row), 3 on 3×3, 5 on 5×5, and 0 on 3×4 (odd x side; `E_2` is keyed to y);
- `E_3`: 16 on 4×3×4 (the y-seam, as in AW1), 16 on 3×4×4, 24 on 3×3×4, 27 on 3×3×3, and 0 on 4×4×4.

No flip or parity statement is made on any periodic box with an odd side.

**Finding (recorded, not claimed).** Over GF(2), a link set that is odd on every plaquette of a torus exists iff every coordinate 2-plane has an even number of plaquettes. In 2D that means `L_x L_y` even; in 3D, at most one odd side. Exact elimination gives:
- solvable: 4×3, 3×4, 4×3×4, 3×4×4 and 4×4×4;
- unsolvable: 3×3, 5×5, 3×3×4 and 3×3×3.

So the contract's "periodic tori with an odd side" is an exact obstruction for the rules `E_3` and `E_2` at the seam, not for every flip set (Section 14).

## 9. SU(2) area parity (zero-selected family, `kappa = 0`, `abs(tau)` at most `10^-8`, both signs)

**Surface parity.** Take a loop C of plaquette edges and a spanning surface `Sigma` with `A(C)` plaquettes. The boundary map is linear over GF(2), and every `abs(f cap E_3)` is odd, so

`abs(C cap E_3) = sum_{f in Sigma} abs(f cap E_3) = A(C) (mod 2)`.

The parity is well defined. Two spanning surfaces differ by a closed Z_2 surface z, and `abs(z) = abs(boundary(z) cap E_3) = 0 (mod 2)`. Equivalently, every 2-cycle is a sum of cube boundaries, each with 6 plaquettes. The checker verifies this on the fine box `[0,2]^3`: its cycle space and the span of the cube boundaries both have dimension 8.

The checker also tests:
- all 6480 rectangles with sides 1 to 3, in the three planes, at positions around the origin;
- 400 pseudo-random surfaces;
- one loop spanned by 1 and by 5 plaquettes, and another by 4 and by 8;
- a bent six-link loop with area 2.

**Exact holonomy fixture.** Rational unit quaternions are placed on the links, and the links of `E_3` are then flipped.

| loop | area | W before the flip | W after the flip |
|---|---|---|---|
| plaquette | 1 | 304/525 | -304/525 |
| 2×1 | 2 | 7264/12285 | unchanged |
| 3×1 | 3 | -45274/238875 | 45274/238875 |
| 2×2 | 4 | -384194/429975 | unchanged |
| 3×2 | 6 | 267632/1535625 | unchanged |

**Box statement (AW1 flip lemma, admitted).** This holds in every open centered whole-star box `Lambda_N` (N at least 2), every on-site cutoff, at `kappa = 0` and `abs(tau)` at most `10^-8`:
- `U_E` commutes with the cutoff projections and fixes `Omega_0`;
- the finite-box ground eigenvalue is simple (AM2, inherited through the AW1 gate), in every cutoff space and for the untruncated vector;
- therefore `U_E psi_N(tau)` is a phase multiple of `psi_N(-tau)`, and `omega_{N,-tau}(W_C) = (-1)^{abs(C cap E_3)} omega_{N,tau}(W_C) = (-1)^{A(C)} omega_{N,tau}(W_C)`.

**Limit of the named constructions (BB2, admitted).** Let Y be a finite complete-factor region containing the owners of the links of C. For the 3×2 fixture loop, Y is the six coarse sites `(-1,0,0..2)` and `(0,0,0..2)`. Then:
1. In every box, `rho^{N,-tau}_Y = U_{E cap Y} rho^{N,tau}_Y U_{E cap Y}^*`.
2. The BB2 gate admits trace-norm convergence of `rho^{N,tau}_Y` along the whole sequence of N, at each sign separately (`whole_sequence_claimed: true`, both signs, every finite region, F1 and F2 to one common limit).
3. Conjugation is trace-norm continuous, so `omega^{-tau}_inf(W_C) = (-1)^{A(C)} omega^{tau}_inf(W_C)` pointwise for the limit of the named constructions.

No common-subsequence caveat is needed, because each sign converges as a whole sequence.

**Centre-even observables are even in `tau`.** A bounded observable with `alpha_E(A) = A` satisfies `omega_{-tau}(A) = omega_tau(A)`. This covers `W_C` with even `A(C)` and `W^2`. A Casimir enters through `1_[0,L](C_e) C_e`, which is a function of `C_e` and commutes with `U_E`, together with the monotone limit in L.

On `H_FG(G)` for the four flip groups, the odd coefficients of `omega(C_2)` and of `omega(W^2)` vanish through order 3, as the checker verifies.

**Scope.** SU(2) only; the zero-selected family only; `kappa = 0` only; open centered whole-star boxes, their cutoffs and the limit of the named constructions only. The following are excluded:
- other boundary conditions;
- F2 or literal vertex boxes at box level;
- periodic boxes with an odd side;
- nonzero selected triples.

## 10. Transfer ledger

`T` is a transfer (a labelled statement on the named models, with its own exact checks). `O` is an obstruction, with its exact counterexample.

| group | flip lemma | parity theorem | first-order coefficient | dictionary |
|---|---|---|---|---|
| SU(2) | T: `-I`; `H_FG(SU(2))`, `H^{SU(2)}_N`, and the admitted AW1 patterned family | T: `E[W^3] = 0` | T: 1/144 (convention check) | admitted SU(2) dictionary `tau = 96/g^4` (AZ1 gate text), inherited, not re-derived |
| SU(3) | O: `omega_2 = 1/589824` on `H_FG(SU(3))`; reason: no central -1 | O: `d omega(W^2)/dtau = 1/6912`; reason: `E[W^3] = 1/108` | T: 1/1152 | not asserted (exclusion; obligation) |
| SU(4) | T: `-I`; `H_FG(SU(4))`, `H^{SU(4)}_N` | T: `E[W^3] = 0` | T: 1/2880 | not asserted |
| SU(5) | O: `omega_4 = 1/63403380965376`; reason: centre acts by fifth roots | T: `E[W^3] = 0` | T: 1/5760 | not asserted |
| U(1) | T: `e^{i pi}`; `H_FG(U(1))`, `H^{U(1)}_N` | T: `E[W^3] = 0` | T: 1/96 | not asserted |
| Z2 | T: the nontrivial element; `H_FG(Z2)`, `H^{Z2}_N` | T: `E[W^3] = 0` | T: 1/48 | not asserted |
| SO(3) | O: `omega_2 = 1/331776`; reason: trivial centre | O: `d omega(W^2)/dtau = 1/2592`; reason: `E[W^3] = 1/27` | T: 1/864 | not asserted |

**AM2/AQ chain, as obligations.** For every group other than SU(2), none of the following is claimed; each is recorded as an obligation:
- the AM2 fixed point and simple ground;
- the AV1 product split;
- the AQ1 construction and dynamics;
- BB2-type whole-sequence convergence;
- a dictionary to a bare coupling.

The U(1) and Z2 transfers are of the flip lemma, the parity theorem and the first-order coefficient only.

## 11. Error ledger and scaling

**Error ledger** (every term named in the preregistration):

| term | value | reason |
|---|---|---|
| moment_arithmetic | 0 | exact Fractions; the two constant-term evaluations agree exactly |
| character_multiplicities | not_applicable | the reverse route computes no tensor-product multiplicity; the cubic moments are constant terms whose integrality is checked |
| weyl_constant_terms | 0 | finite Laurent polynomials; the Weyl density is expanded completely and the constant term is exact |
| one_plaquette_truncation | 0 | no basis cutoff: the numerators carry every monomial, and the order-n coefficient involves finitely many |
| flip_set_enumeration | 0 | exhaustive on the named boxes, factors and tori; the residue-class count covers every plaquette of Z^3 |
| bb2_limit_passage | 0 | an exact identity in every box, passed through the admitted BB2 trace-norm convergence at each sign; no numerical term |
| arithmetic | 0 | exact rationals throughout; decimals are truncated previews only |

**Scaling.** Under `tau -> tau/100` at `tau = 1/100000000`, the ratios are:
- first-order term: exactly 100;
- SU(3) and SO(3) second-order terms: exactly 10000;
- SU(5) fourth-order term: exactly 100000000;
- moments: exactly 1.

These brackets were preregistered.

## 12. Mandatory sentence

Under the frozen convention, the link-flip lemma transfers exactly to the listed gauge groups that have a central element acting as -1 on the Wilson representation and the first-order parity theorem exactly to those with vanishing third Haar moment of W, each with its own first-order Wilson coefficient, on one-plaquette models and on group box models in each box separately; SU(3) and SO(3) are recorded obstructions with exact nonzero coefficients, and SU(5) is a recorded flip obstruction with an exact nonzero fourth-order coefficient; for SU(2) in the zero-selected family at kappa=0 the Wilson-loop mean is odd or even in tau according to the parity of the number of plaquettes of any spanning surface of the loop, in every open centered whole-star box and for the limit of the named constructions; these are statements about named models and one-plaquette finite graphs, not AM2 or continuum statements for other groups, not statements for periodic boxes with an odd side, not uniqueness of any ground state, and not a statement uniform in the lattice spacing a.

## 13. Checker, controls and the item/control map

`check.py --output ABS_FRESH_DIR` uses the standard library only.

**Before any evaluation it:**
1. records its own sha256 (`check_py_sha256_recorded_before_evaluation`);
2. verifies the contract snapshot hash;
3. derives the Casimir normalization and the flip-set rules;
4. only then parses the contract, reading the target, the comparators (`==` and `!=0`), the reference (free values in the same code path, Haar), the coupling of the SU(2) corollary and every normalization. It validates each of these semantically.

**Pins.** It pins the sha256 of six admitted gates: AW1, AW2, AY2, AZ1, AZ2 and BB2. It checks that `AGENTS.md` equals the AW1 binding. It verifies that the inputs inventory is exactly `AGENTS.md`, the contract and the 21 shared premises.

**Arithmetic and outputs.**
- Exact `Fraction` arithmetic decides every Boolean.
- Every failure is an explicit exception; the checker never uses `assert`.
- It writes `results.json` and `source-manifest.json`.
- The claim flags are all false: `continuum_claim`, `weak_coupling_claim`, `rate_in_a_claimed`, `uniqueness_of_ground_state_claimed`, `transfers_to_aq`, `uniform_wilson_claim`, `resolved_interaction_shift`, `scientific_priority_verified`, and a historical-provenance flag.
- It also writes every gate field, together with `headline`, `label` (`HNM-BD1-R`), `contract_controls_covered`, `controls_with_damaging_mutations` (22), `route_of_computation` (`weyl_integration`), `exclusions`, `direction` (`reverse`), `loop` (`BD1`), `human_author`, `contribution_alias` and `proposed_reverse_verdict`.

It also scans this report and its own results text:
- the negation-aware phrase scan, with the round list and the contract's forbidden phrasings, and the template removed as one literal;
- a scan for placeholder spans;
- a scan for the two verbs the contract forbids.

**Controls.** Each control below is executed as damaging mutations, and every mutation must raise a rejection.

| control | damaging mutations rejected |
|---|---|
| coherent_evidence_tampering | a byte change without a rehash. Rehashed tampers of the contract: the group list without SO(3); the convention with face energy `24 C_F`; E_3 x-links keyed to `p_z`; a control removed from both lists; the gate field `flip_transfer_claimed` false; the template without its SU(5) clause. A rehashed BB2 gate with `whole_sequence_claimed` false. A declared snapshot removed. A required control Boolean flipped |
| exact_arithmetic_admission | a float moment; a bool; NaN; a decimal string; a float obstruction coefficient |
| no_priority_or_continuum_claim | continuum, priority or weak-coupling flag true; historical provenance used as a premise |
| changed_model_relabelled | an SU(2) value under the SU(3) label; a one-plaquette value presented as a box value; a one-plaquette value presented as a limit value; a group box value under the SU(2) patterned label; a Z2 cell under another normalization |
| insufficient_verdict_retained | `accepted` with the SU(3) cell missing; `accepted` with criterion B unproved; `accepted` with only the box-level area parity; `accepted` with a route disagreement; a retuned group list |
| placeholder_span_rejected | a group-name placeholder; a vertical-bar placeholder; an e.g. placeholder |
| negation_aware_phrase_scan | affirmative uses of four forbidden phrases (a negated clause passes) |
| parameters_declare_metric_weights_window | weights missing; window "not applicable" with no reason; clock empty; `d_X` declared |
| tier_mixing_rejected | a plan route label; a float under the tier; a tier on a moment; a tier on the fourth-order coefficient; an unlisted route; a hypothesis source attached; a first-order value without its tier |
| frozen_convention_used | SU(3) with face energy `24 C_F`; the SU(2) value copied into U(1); Z2 with "electric 1 on the odd state"; Z2 with "1 - sigma^x"; the literal display sign |
| su2_constants_not_transferred | an SU(3) coefficient of 1/144; `tau = 96/g^4` asserted for U(1); `alpha = g^2/(2a)` asserted for SU(4); a Z2 value sourced from SU(2) |
| flip_criterion_central_minus_one | an SU(3) flip transfer; an SU(5) obstruction resting on the missing centre alone; an SU(4) transfer without its element; an SO(3) counterexample of zero; a U(1) flip claimed outside the named models; a Z2 flip claimed without verified flip sets |
| parity_criterion_third_moment | an SU(3) parity transfer; an SU(5) parity obstruction; U(1) without single-occurrence orthogonality; an SO(3) derivative of zero; the flip and parity columns conflated |
| moment_tables_two_routes | a single-route cell; a float moment cell; two evaluations that disagree; a cross-route table that disagrees in one cell |
| su3_obstruction_mandatory | the cell omitted; SU(3) called a transfer; a second-order coefficient of zero; `E[W^3]` set to 0 |
| so3_obstruction_mandatory | the cell omitted; SO(3) called a transfer; a first-order derivative of zero; a central -1 claimed |
| flip_sets_verified | E_3 minus one link; an anticyclic rule on x-links only; E_2 plus y-links; E_3 on the 4×3×4 torus; a periodic odd side called verified |
| area_parity_scope | nonzero kappa; a periodic odd-side box; F2 boxes; literal vertex boxes; a perimeter sign rule; another group |
| one_plaquette_model_terms | a single-link electric term; the alpha-unit magnetic term used as a delta-unit term; `transfers_to_aq` true; a free reference computed elsewhere; a lattice-limit value |
| no_transfer_called_prediction | each of the two forbidden verbs; a non-transfer recorded without its counterexample |
| am2_not_reinstantiated | AM2 for U(1); AQ for Z2; AV1 for SU(4); an AQ1 construction transferred for Z2; a dictionary for U(1) |
| su5_flip_obstruction_fourth_order | the cell omitted; SU(5) called a flip transfer; an SU(5) parity obstruction; an obstruction resting on the missing centre alone; `omega_4` of zero; `omega_4` as a float; the route missing |

**Item/control map.**

| contract item | sections | checks | controls |
|---|---|---|---|
| 1 Criterion A | 5, 8 | `criterion_A_centre_analysis`, `criterion_A_one_plaquette_flip_operator`, `criterion_A_box_operator_identity`, `kato_radii_explicit` | flip_criterion_central_minus_one, flip_sets_verified, frozen_convention_used |
| 2 Criterion B | 6 | `criterion_B_one_plaquette_first_order_terms`, `criterion_B_complex_level_zero_splitting`, `criterion_B_single_occurrence_orthogonality`, `criterion_B_gauge_invariant_level_is_plaquette_characters`, `minimal_casimir_and_fundamental_level` | parity_criterion_third_moment |
| 3 Moments and coefficients | 3, 4 | `haar_moments_weyl_integration`, `cubic_moments_constant_terms`, `casimir_normalization_torus_laplacian`, `first_order_coefficients_all_groups`, `su2_convention_check_admitted_series`, `tier_labels` | moment_tables_two_routes, su2_constants_not_transferred, tier_mixing_rejected, exact_arithmetic_admission |
| 4 Obstruction cells | 7 | `obstruction_cell_su3`, `obstruction_cell_so3`, `obstruction_cell_su5_fourth_order`, `zn_grading_even_orders` | su3_obstruction_mandatory, so3_obstruction_mandatory, su5_flip_obstruction_fourth_order, one_plaquette_model_terms |
| 5 Flip sets | 8 | `flip_set_e3_reverse_derived`, `flip_set_e3_boxes_and_retained_faces`, `flip_set_e3_coarse_factors`, `flip_set_e2_boxes`, `periodic_tori_odd_side_recorded`, `finding_torus_flip_set_existence_gf2` | flip_sets_verified |
| 6 SU(2) area parity | 9 | `area_parity_surface_parity`, `closed_surfaces_even`, `area_parity_exact_su2_holonomy_fixture`, `area_parity_box_and_limit`, `centre_even_observables_even` | area_parity_scope |
| 7 Transfer ledger | 10 | `transfer_ledger_complete` | am2_not_reinstantiated, no_transfer_called_prediction, changed_model_relabelled |
| 8 Template, gate fields, controls, replay | 12–15 | `report_template_phrase_placeholder`, `gate_fields_exported`, `error_ledger_itemized`, `scaling_brackets`, `results_text_scanned`, `contract_fields_read_and_validated`, `admitted_gate_sha256_pinned`, `reverse_premise_inventory_exact` | coherent_evidence_tampering, placeholder_span_rejected, negation_aware_phrase_scan, parameters_declare_metric_weights_window, insufficient_verdict_retained, no_priority_or_continuum_claim |

## 14. Exclusions, limitations and contract wording findings

**Claim exclusions, exactly as the contract lists them:**
- any AM2, AV1 or AQ statement for a group other than SU(2)
- a dictionary to a bare coupling for a group other than SU(2)
- weak coupling or continuum
- uniqueness of any ground state
- any estimate uniform in the lattice spacing a
- scientific priority
- a flip or parity statement for SU(2) at a nonzero selected triple, in periodic boxes with an odd side, or in F2 or literal vertex boxes

**Limitations:**
- **Scope of the group statements.** They are statements about named finite models: `H_FG(G)`, and `H^G_N` box by box inside a box-dependent Kato radius (not uniform in N). One-plaquette coefficients are finite-model values, and nothing about them transfers to an AQ-type limit for any group other than SU(2).
- **Inheritance.** The SU(2) corollary inherits, without re-proof:
  - AM2's simple finite-box ground, in each cutoff and untruncated, through the AW1 gate;
  - the AW1 flip lemma;
  - BB2's whole-sequence convergence at each sign.
- **Cited, not machine-checked:** Kato analyticity, Schur's lemma, the Weyl integration and character formulas, and the radial Laplacian identity behind the Casimir normalization. The checker verifies their finite consequences: antisymmetry of the numerators, `C_F`, the adjoint and `Lambda^k` Casimirs, and the Lie-algebra sum.
- **Independence** is limited to route and code. The forward and reverse producers share the contract, the admitted AW1 structure and the premises that state the mechanism. The cross-route agreement of the moment and coefficient tables is for the exchange, and this producer read no forward file.
- **Upper-level statements are not made.** There is no enclosure, no sign certificate for any group other than SU(2), no remainder bound for other groups, and no dynamical or mass-gap statement.

**Contract wording findings (non-blocking):**
1. **Periodic tori.** "Periodic tori with an odd side ... as an obstruction" is exact for the rules `E_3` and `E_2` at the seam of the keyed coordinate. It is not exact for every flip set. A GF(2) solution exists iff every coordinate 2-plane has an even plaquette count: for example 4×3×4, where `E_3` has 16 even seam plaquettes, and 4×3 in 2D. On a 3×4 torus, `E_2` itself works. This is recorded, not claimed, and no periodic statement is made.
2. **Moment tables.** `moment_tables_two_routes` asks every moment to be computed "by both routes" and to agree. A single producer supplies one route: here, two exact constant-term evaluations inside `weyl_integration`. The cross-route equality is the exchange's cell-by-cell comparison, and `compare_route_tables` in `check.py` is provided for it.
3. **The AW1 display defect.** The contract's convention text records the inherited AW1 wording defect in the literal display `2 (W Omega_0, c^(1))`. The reverse uses `-2 Re (W Omega_0, c^(1))` and rejects the literal sign.
4. **The SU(2) corollary coupling.** The preregistration names `1/100000000` as the corollary coupling. The corollary holds for every `abs(tau)` at most `10^-8` at each sign, which is the admitted AW1/BB2 range. The sign-flip identity is exact, and the scaling check uses `1/100000000`.
5. **The level at `32 C_F`.** "The gauge-invariant level at energy `32 C_F` contains `Im chi_fund(U_g) Omega_0`" is read as the full span over all plaquettes of the box, retained or not. The zero-splitting proof covers that whole span.

## 15. Proposed reverse verdict and gate fields

**Proposed reverse verdict: `accepted_within_scope`** (sub-labels `transfer_to_named_model`, `obstruction_recorded`). This is the rule in `check.py`:
- **insufficient** if criterion A or B, or an obstruction cell, is missing;
- **limited** if a group cell is missing or misclassified, the routes disagree, or only the box-level area parity is proved;
- **accepted_within_scope** otherwise.

Every input of that rule holds on this route. The cross-route equality remains a condition of the gate.

**Gate fields exported:**
- `model_is_finite_graph: true`
- `transfers_to_aq: false`
- `flip_transfer_claimed: true`
- `flip_transfer_scope`: SU(2), SU(4), U(1) and Z2, on `H_FG(G)` and `H^G_N`, with `E_3` and `E_2` verified; no AM2, AV1 or AQ statement for any group other than SU(2)
- `parity_transfer_claimed: true` (SU(2), SU(4), SU(5), U(1), Z2)
- `obstructions_recorded: true`
- `area_parity_limit_claimed: true`
- `uniqueness_of_ground_state_claimed: false`
- `rate_in_a_claimed: false`
- `continuum_claim: false`
- `weak_coupling_claim: false`
- `scientific_priority_verified: false`

**Contribution classification (paired-physics method):**
- **A known theorem applied here:** Weyl integration and character formulas, Schur, Kato, and centre flips.
- **A new derivation within the declared models:** the exact group-by-group cells, the SU(5) column-chain closed form and the explicit Kato radii.
- **A proved obstruction on a named finite model:** the SU(3), SO(3) and SU(5) flip entries, and the SU(3) and SO(3) parity entries.
- **Not a conjecture:** nothing here is presented as one.

**Method lenses.** These are modern methodological uses of the frozen skills; no historical figure endorses anything here.
- **Newton:** every inverse problem is stated with its kernel. The flip set is determined up to a centre gauge transformation, and E_2 has four solutions.
- **Tesla:** the selection rules and degenerate matrix elements are computed on the whole level, including `Im chi`.

## 16. Premises read, isolation and scratch disclosure

**Read in full:**
- the contract snapshot (first);
- `AGENTS.md`;
- `selection-bd1.md`;
- the AW1 gate;
- the AW1 reverse report, the AW1 forward report and `skeptic/aw1.md`;
- the I1 report;
- the BB2 gate (every field; its 135-entry `bindings` list only counted);
- the paired-physics SKILL and its complete-residual reference;
- the Newton, Tesla and historical-panel SKILL files.

**Read in part:**
- the AW2, AY2, AZ1 and AZ2 gates (verdict, title, the first 3000 characters of `accepted`, and `gate_fields`);
- the BB2 forward report (the header, the verdict and sections 0–1);
- `skeptic/bb2.md` (its headings, the lines mentioning signs, and "What is proved");
- the BA1 and BB2 contracts (their control-semantics blocks only).

**Not opened:** the AZ2 forward report. It was not needed.

**Outside `inputs/`, for protocol and conventions only.** None of these carries premise weight.
- `research/round33/tools/README.md`, `freeze.py` and `phrase_scan.py` (its phrase list is copied into `check.py` as infrastructure);
- portions of `research/round32/reverse/aw1/check.py`: its header, its structure outline, `compute()`'s opening, and its output code;
- the first 80 lines of `research/round33/tools/freeze_contract.py`, read for the placeholder regex of rule R1, which the inherited control `placeholder_span_rejected` names. This file was outside the list the advisor named, and it contains no scientific content;
- a directory listing of `research/round33/tools/`, which showed the names `arb_crosscheck.py`, `record_gate.py`, `freeze_contract.py` and a `__pycache__` folder;
- the repository's `CLAUDE.md`, which was supplied to me as session instructions.

**Not read.** I opened, listed and read nothing under any of these:
- `research/round33/forward/bd1/`, `forward/bd2/`, `forward/bc1/` or `forward/bc2/`;
- `research/round33/skeptic/` (other than the snapshots), `research/round33/experts/`, or `research/round33/advisor/` (other than the snapshots);
- any other agent's scratch folder.

**Scratch disclosure.**
- My private scratch folder is `/tmp/claude-0/bd1-reverse-private/`.
- It holds:
  - `proto1.py`, a Fraction prototype of the torus engine;
  - `draft.txt`, this report with a marker for the template, which a helper script replaced with the verbatim contract template;
  - development runs `dev1` to `dev4` and `dev3o`;
  - the production run `run1`.
- **None of it is evidence.**
- I created the folder with `mkdir -p` and listed only that folder. The listing printed the parent directory's metadata line (its permissions and link count), not its contents. I did not list `/tmp/claude-0/` or the shared scratchpad root, and I opened no file of any other agent.
- The Claude harness saved one of my own long reads (the AW1 reverse report snapshot) to its tool-results store, and I read it back there; that is my own read.

## 17. Reproduction

```bash
python3 -B research/round33/reverse/bd1/check.py --output /absolute/fresh/dir
python3 -B -O research/round33/reverse/bd1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round33/tools/freeze.py verify research/round33/reverse/bd1
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/bd1.json research/round33/reverse/bd1/report.md
```
