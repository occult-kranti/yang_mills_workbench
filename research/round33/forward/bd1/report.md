# Hruday centre-symmetry transfer of the parity theorem, the link-flip lemma and the first-order Wilson mean across gauge groups — BD1 forward (characters route)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production: the derivations, `check.py` and this report were written by a Claude model agent acting as the BD1 forward producer under the frozen BD1 contract (`research/round33/contracts/bd1.json`, sha256 `a5c8416600c49b0728fdca05cd67c3ff2e53d9fd9e146d4305abcd2da775c1fc`), which `check.py` verifies before it parses any field. It is correlated model-agent work, not independent human review and not formal verification. HNM labels are project aliases.

**What this producer read.**
- **The contract snapshot first** (every required item, every control with its `new_control_semantics`, `parameters`, the preregistration block), then only files under `inputs/`:
  - *read in full:* `AGENTS.md`; `selection-bd1.md`; the AW1 gate (every field except `bindings`); the AW1 forward report; `skeptic/aw1.md`; the I1 forward report; the BB2 gate (every field except `bindings`); the paired-physics SKILL and its complete-residual reference; the Newton and Tesla SKILL files;
  - *read in part:* the AW1 reverse report (header through the start of its Section 6); the AW2, AY2, AZ1 and AZ2 gates (`accepted`, `gate_fields`, `limitations`); the BB2 forward report (header through the start of its Section 5); `skeptic/bb2.md` (its first 80 lines); the BA1 and BB2 contracts (`controls` and `new_control_semantics` only);
  - *headings only:* the AZ2 forward report; *not opened:* the historical-panel SKILL.
- **Outside `inputs/`, for protocol and code conventions only:** `research/round33/tools/README.md`, `research/round33/tools/freeze.py`, `research/round33/tools/phrase_scan.py` (its round phrase list is copied into `check.py` as infrastructure) and `research/round32/forward/aw1/check.py` (conventions only; AW1 is gated). None of these carries premise weight.
- **Not read:** anything under `research/round33/reverse/bd1/`, `research/round33/forward/bd2/`, `research/round33/forward/bc1/`, `research/round33/forward/bc2/`, `research/round33/skeptic/` (other than the snapshot in `inputs/`), `research/round33/experts/`, `research/round33/advisor/` (other than the snapshots in `inputs/`), and no other agent's scratch folder.
- **Scratchpad disclosure.** My private scratch folder is `/tmp/claude-0/bd1-forward-private/`: one Fraction prototype (`proto1.py`: moments, one-plaquette series and the Hellmann–Feynman and Wigner cross-checks), a draft of this report, development runs `dev1` and `dev2`, and the production run `run1`. **None of it is evidence.** I created the folder with `mkdir -p` and did not list `/tmp/claude-0/`, so I saw no other agent's folder names. The Claude harness saved one of my own long reads (the AW1 forward checker, read for conventions) to its tool-results store; that is my own read.

**Attribution.** Peter–Weyl theory, Schur's lemma, the Pieri rule, the Clebsch–Gordan series, Schur–Weyl duality with the hook-length formula, the Weyl integration formula, Kato's analytic perturbation theory, Rayleigh–Schrödinger perturbation theory with the Hellmann–Feynman and Wigner 2n+1 identities, and centre symmetries of lattice gauge theories are established mathematics. The contribution here is their application to the named models with exact constants and exact obstruction coefficients. Scientific priority is unverified.

## Verdict (forward route)

Everything below is about named models: the one-plaquette finite graphs `H_FG(G)`, the group-G whole-star box models `H^G_N` (each box inside its own Kato radius), and, for SU(2) only, the admitted zero-selected family through the AW1 and BB2 gates.

1. **Criterion A (flip) is proved** on `H_FG(G)` and on every `H^G_N`, untruncated and in every on-site cutoff, for every group with a central element acting as `-I` on the Wilson representation. Such an element exists exactly for **SU(2), SU(4), U(1) and Z2**, and does not exist for SU(3), SU(5) and SO(3) (exact reasons in Section 5).
2. **Criterion B (parity) is proved** on `H_FG(G)` and on every `H^G_N`: the first-order tau-derivatives of `omega(W^2)` and of the centred Euclidean and real-time correlations vanish when `E[W^3]=0`, and so does the first-order splitting of the whole gauge-invariant level at energy `32 C_F` (including the `Im chi_F` directions for complex Wilson representations). `E[W^3]=0` holds exactly for **SU(2), SU(4), SU(5), U(1) and Z2**. On `H_FG(G)` the derivatives are nonzero whenever `E[W^3]` is nonzero.
3. **Moments and first-order coefficients** are exact for all seven groups by the character route, with three character sub-routes in agreement and a labelled forward-internal Weyl cross-check in agreement (Sections 3–4). The first-order coefficients `2 (1/3) E[W^2]/(32 C_F)` are `1/144, 1/1152, 1/2880, 1/5760, 1/96, 1/48, 1/864` for SU(2), SU(3), SU(4), SU(5), U(1), Z2, SO(3).
4. **Obstruction cells** (Section 7): SU(3) `E[W^3]=1/108`, `d omega(W^2)/d tau = 1/6912`, second-order coefficient of `omega(W)` `1/589824`; SO(3) `1/27`, `1/2592`, `1/331776`; SU(5) `E[W^3]=0`, both of those vanish by the `Z_5` grading, and the fourth-order coefficient of `omega(W)` is `1/63403380965376 = 1/(2^30 3^10)`.
5. **Flip sets** (Section 8): `E_3` meets every plaquette of the boxes `N=2,3,4` (2335, 6909, 15291 plaquettes; 1344, 4536, 10752 retained faces) and of the seven probed factors oddly; `E_2` meets every plaquette of `[-N,N]^2` exactly once; periodic tori with an odd side are recorded as an obstruction.
6. **SU(2) area parity** (Section 9) is proved in every open centered whole-star box and every on-site cutoff at `kappa=0`, and pointwise for the limit of the named constructions through BB2, at each sign.
7. **Transfer ledger** (Section 10) and **error ledger** (Section 11) are complete.
8. **Checker.** `check.py` runs **37 exact checks**; all **22 contract controls** reject explicit damaging mutations (**111** rejections in total); the `-B` and `-B -O` outputs are byte-identical.

**Proposed forward verdict: `accepted_within_scope`** (forward route only; the gate also needs the reverse route and skeptical review), sub-labels `transfer_to_named_model` and `obstruction_recorded`.

## 1. Models and the frozen convention

All values are read from `parameters.convention` and checked in `contract_binding` and `character_rules`. Energies are in delta units.

**One-plaquette model.** On class functions of the plaquette holonomy `U`, with the orthonormal character basis `chi_r`:

\[
H_{FG}(G)(\tau)=32\,C_2-\tfrac{\tau}{3}W,\qquad 32\,C_2\,\chi_r=32\,C_2(r)\,\chi_r,\qquad W=\frac{\operatorname{Re}\chi_F(U)}{\dim F}=\frac{\chi_F+\chi_{\bar F}}{2\dim F}.
\tag{HNM-BD1-F01}
\]

The electric term is four links of `8 C_2` each acting on a class function of the holonomy. `model_is_finite_graph: true`, `transfers_to_aq: false`; every value obtained on it is a finite-model value.

**Group box models.** On `L^2(G^{links of Lambda_N})` for the open centered whole-star box `Lambda_N=[-N,N]^3`, `N` at least 2, with the I1/AQ1 geometry (coarse 24-link factors, the 21 omitted faces of an anchor retained when its whole star lies in `Lambda_N`, selected faces with coefficient 0):

\[
H^G_N(\tau)=\sum_{e}8\,C_2(e)-\tfrac{\tau}{3}\sum_{f\ \mathrm{retained}}W_f ,
\tag{HNM-BD1-F02}
\]

untruncated and in every on-site cutoff (spectral projections of each factor's `sum 8 C_2`). For SU(2) this is exactly the AW1 box Hamiltonian of the zero-selected family (at the zero triple the onsite operator is the Casimir sum). For every other group it carries **no** AM2, AV1 or AQ statement.

| group | Wilson representation | `W` | Casimir rule | `C_F` | face energy `32 C_F` | `a=(1/3)/(32 C_F)` |
|---|---|---|---|---|---|---|
| SU(2) | fundamental | `(1/2)Tr U` | `j(j+1)` | 3/4 | 24 | 1/72 |
| SU(3) | fundamental | `Re Tr U/3` | `(1/2)[sum_i lambda_i(lambda_i+N+1-2i) - (sum_i lambda_i)^2/N]` | 4/3 | 128/3 | 1/128 |
| SU(4) | fundamental | `Re Tr U/4` | same | 15/8 | 60 | 1/180 |
| SU(5) | fundamental | `Re Tr U/5` | same | 12/5 | 384/5 | 5/1152 |
| U(1) | charge 1 | `cos theta` | `n^2` | 1 | 32 | 1/96 |
| Z2 | sign | sign character | 0 (even), 1 (odd) | 1 | 32 | 1/96 |
| SO(3) | vector | `Tr U/3` | `l(l+1)` | 2 | 64 | 1/192 |

The Z2 normalization is the frozen one (`8 C_2 = 8` on the odd link state). The readings "electric term 1 on the odd state" (`C_2(odd)=1/8`, first-order coefficient `1/6`) and "`1 - sigma^x`" (`C_2(odd)=1/4`, coefficient `1/12`) are rejected by `frozen_convention_used`.

## 2. The character route

**Peter–Weyl.** Class functions have the orthonormal basis `chi_r`, and multiplication by `chi_F` acts by tensor multiplicities, `chi_F chi_r = sum_s N^s_{F r} chi_s`. Hence

\[
W\chi_r=\frac{1}{2\dim F}\sum_s\big(N^s_{F r}+N^s_{\bar F r}\big)\chi_s,\qquad
\mathbb E[W^k]=\big(\chi_0,\,W^k\chi_0\big)_{L^2} .
\tag{HNM-BD1-F03}
\]

The multiplicities come from:
- **SU(N), N=3,4,5 (Pieri):** irreps are partitions `lambda` with `lambda_N=0` (full columns removed); `F x V_lambda` adds one box in every admissible row, and `Fbar x V_lambda` removes one box as a GL(N) weight (dual Pieri), both with multiplicity 1, followed by column normalization.
- **SU(2) (Clebsch–Gordan):** `j x 1/2 = (j-1/2) + (j+1/2)`, `Fbar = F`. The SU(N) Pieri code at `N=2` gives the same rule and Casimirs (`su2_clebsch_gordan_equals_pieri_N2`).
- **SO(3) (Clebsch–Gordan):** `l x 1 = (l-1)+l+(l+1)` for `l` at least 1, `0 x 1 = 1`.
- **U(1) (charge counting):** `chi_1 chi_n = chi_{n+1}`, `conj(chi_1) chi_n = chi_{n-1}`.
- **Z2 (direct summation):** `sign x sign = trivial`.

`character_rules` checks the dimension count `sum_s N^s_{F r} dim s = dim F dim r` for every irrep within six steps of the trivial one (7, 28, 50, 80, 13, 2, 7 irreps for SU(2), SU(3), SU(4), SU(5), U(1), Z2, SO(3)), `C_2(F)=C_2(Fbar)=C_F` against the contract rule, and rejects a non-Pieri shape added to the SU(3) rule.

**Lemma 2.1 (smallest nonzero Casimir).** For every listed group, `C_F` is the smallest nonzero Casimir, attained exactly by `F` and `Fbar`.
*Proof.* U(1): `n^2` is at least 1 with equality at `n=±1`. Z2: the only nonzero value is 1. SO(3): `l(l+1)` is at least 2 with equality at `l=1`. SU(N): in the convention's normalization `C_2(lambda)=(1/2)(lambda, lambda+2rho)` for an invariant form in which the fundamental weights have positive mutual products `(omega_i, omega_j)` and positive `(omega_j, rho)`. Write `lambda=sum m_i omega_i` with nonnegative integers `m_i`, some `m_i` at least 1. Then `(lambda,lambda)` is at least `(omega_i,omega_i)` and `(lambda,2rho)` is at least `(omega_i,2rho)`, so `C_2(lambda)` is at least `C_2(Lambda^i)=i(N-i)(N+1)/(2N)`, which is at least `C_F=(N^2-1)/(2N)`, with equality only for `i=1` or `i=N-1`; equality throughout forces `lambda=omega_1` or `omega_{N-1}`, that is `F` or `Fbar`. ∎ The checker records the irreps of Casimir `C_F` within six steps: exactly `{F, Fbar}` for every group.

## 3. Haar moments (item 3)

Every entry is an exact rational by the character route (`route_of_computation: characters`, no tier). Decimal previews are truncated and are not admission values.

| group | `E[W]` | `E[W^2]` | `E[W^3]` | `E[W^4]` | `E[W^5]` |
|---|---|---|---|---|---|
| SU(2) | 0 | 1/4 | 0 | 1/8 | 0 |
| SU(3) | 0 | 1/18 | 1/108 | 1/108 | 5/1296 |
| SU(4) | 0 | 1/32 | 0 | 7/2048 | 0 |
| SU(5) | 0 | 1/50 | 0 | 3/2500 | 1/50000 |
| U(1) | 0 | 1/2 | 0 | 3/8 | 0 |
| Z2 | 0 | 1 | 0 | 1 | 0 |
| SO(3) | 0 | 1/9 | 1/27 | 1/27 | 2/81 |

Previews: SU(3) `E[W^3] ≈ 9.2592592e-3`; SU(4) `E[W^4] ≈ 3.4179687e-3`; SU(5) `E[W^4] = 1.2e-3`, `E[W^5] = 2e-5`; SO(3) `E[W^3] ≈ 3.7037037e-2`.

**Cubic moments.** `E[chi^a conj(chi)^b]` with `a+b=3` is the multiplicity of the trivial irrep in `F^{x a} x Fbar^{x b}`, a nonnegative integer:

| group | (3,0) | (2,1) | (1,2) | (0,3) |
|---|---|---|---|---|
| SU(2), SU(4), SU(5), U(1), Z2 | 0 | 0 | 0 | 0 |
| SU(3) | 1 | 0 | 0 | 1 |
| SO(3) | 1 | 1 | 1 | 1 |

(SU(3): the invariant epsilon tensor in `F^{x3}`; SO(3): `epsilon_{ijk}`, the vector representation being real.)

**Three character sub-routes, one route label.** `moments_characters_route` requires exact agreement of (i) the iterated action (F03) of `W` on the character basis; (ii) iterated tensor multiplicities `E[chi^a conj(chi)^b]` inserted into `E[W^k]=(2 dim F)^{-k} sum_a C(k,a) E[chi^a conj(chi)^{k-a}]`; (iii) closed-form counts: Schur–Weyl duality with the hook-length formula for SU(N) (`E[chi^a conj(chi)^b] = sum f_lambda f_mu` over partitions `lambda` of `a` and `mu` of `b` with at most `N` rows and `lambda-mu` a multiple of `(1,...,1)`), charge balance for U(1), parity for Z2, and for SO(3) the covering `SU(2) → SO(3)` with `chi_1 = chi_{1/2}^2-1` and Catalan numbers. The SU(2) row reproduces the admitted AW1 moments `0, 1/4, 0, 1/8` read from the AW1 gate.

**Forward-internal Weyl cross-check (labelled).** `check.py` also evaluates every `E[chi^a conj(chi)^b]` with `a+b` at most 5 by constant-term extraction on the maximal torus (`CT[f |Delta|^2]/|W|` with the monomials in `Z(1,...,1)` retained for SU(N); `(1/2) CT[f (2-z-1/z)]` for SO(3); direct integration for U(1); direct summation for Z2), and compares the two tables cell by cell (35 moment cells and 7 coefficient cells) in `moment_tables_two_routes`. **This is not the reverse producer's route and it is never the admission value**; it exercises the two-route comparison on real data. The admission comparison of the contract is between this packet and the reverse packet.

## 4. First-order coefficients (item 3)

**Derivation under the frozen convention.** `W Omega_0 = (chi_F + chi_Fbar)/(2 dim F)` is an eigenvector of `32 C_2` with eigenvalue `32 C_F` (both `F` and `Fbar` have Casimir `C_F`), and `E[W]=0`. With the AM2/AV1 creation sign `psi = e^{-C} Omega_0`, the first-order creation is `c^(1) = -(tau/3)/(32 C_F) W Omega_0` on the one plaquette (`-(tau/3)/(32 C_F) sum_f W_f Omega_0` in a box), and

\[
\omega_\tau(W)=-2\operatorname{Re}\,(W\Omega_0,c^{(1)})+O(\tau^2)=2\,\frac{\tau}{3}\,\frac{\mathbb E[W^2]}{32\,C_F}+O(\tau^2)=2a\,\mathbb E[W^2]\,\tau+O(\tau^2).
\tag{HNM-BD1-F04}
\]

The literal display `2 (W Omega_0, c^(1))` has the opposite sign; this is the AW1 wording defect recorded in the contract, and the convention above is the one used.

| group | `E[W^2]` | `C_F` | first-order coefficient of `omega(W)/tau` | preview |
|---|---|---|---|---|
| SU(2) | 1/4 | 3/4 | **1/144** | 6.9444444e-3 |
| SU(3) | 1/18 | 4/3 | **1/1152** | 8.6805555e-4 |
| SU(4) | 1/32 | 15/8 | **1/2880** | 3.4722222e-4 |
| SU(5) | 1/50 | 12/5 | **1/5760** | 1.7361111e-4 |
| U(1) | 1/2 | 1 | **1/96** | 1.0416666e-2 |
| Z2 | 1 | 1 | **1/48** | 2.0833333e-2 |
| SO(3) | 1/9 | 2 | **1/864** | 1.1574074e-3 |

Every entry carries `tier: exact_first_order` and `route_of_computation: characters`. For SU(N), N at least 3, only `E[|chi_F|^2]=1` survives in `E[W^2]` (`E[chi_F^2]=0` since `F x F` has no invariant), so `E[W^2]=1/(2N^2)` and the coefficient is `1/(48 N (N^2-1))`. The SU(2) value `1/144` reproduces the admitted AW1 coefficient (read from the AW1 gate and from the contract); **this is a check of the convention, not a transferred value**, and no SU(2) value enters any other cell.

**The same coefficient on the box models.** In `H^G_N` with `W` a retained face (the AW1 original xz face, retained for `N` at least 2), `psi_1 = a sum_f W_f Omega_0` and `(W Omega_0, W_f Omega_0) = E[W W_f] = E[W^2] delta_{f,W}`: two distinct plaquettes share at most one link, so a face `f` other than `W` has at least three links carried once and the Haar mean vanishes (single-occurrence orthogonality, Lemma 6.1). The first-order Taylor coefficient of `omega_N(W)` is therefore the same `2a E[W^2]` in every box (`criterion_B_box_models`: box sums over the 1344 retained faces of `Lambda_2` for all seven groups), as a finite-box Taylor coefficient inside that box's Kato radius.

**Series on the one plaquette.** Exact Rayleigh–Schrödinger in the character basis gives, through order 5 (finite-model values):

| group | coefficients of `omega(W)` at `tau^1 … tau^5` |
|---|---|
| SU(2) | 1/144, 0, -5/11943936, 0, 289/6604518850560 |
| SU(3) | 1/1152, 1/589824, 13/15288238080, -77/9393093476352, -2017/67630273029734400 |
| SU(4) | 1/2880, 0, 41/143327232000, 0, -2699161/14280026477926809600000 |
| SU(5) | 1/5760, 0, 29/8026324992000, 1/63403380965376, 9248293/13779127087624146124800000 |
| U(1) | 1/96, 0, -7/7077888, 0, 29/195689447424 |
| Z2 | 1/48, 0, -1/221184, 0, 1/679477248 |
| SO(3) | 1/864, 1/331776, 1/429981696, -55/2972033482752, -49/570630428688384 |

The SU(2) row reproduces the admitted AW1 one-plaquette fixture (`tau/144 + 0 tau^2 - (5/11943936) tau^3`). Each series is certified three ways in `rayleigh_schroedinger_one_plaquette`: the free reference (`omega_0(W)=E[W]`, `omega_0(W^2)=E[W^2]`) is computed in the same code path; the Hellmann–Feynman identity `c_m = -3(m+1)E_{m+1}` (from `dE/dtau = -(1/3) omega(W)`) holds for `m=0..4` against the separately computed energy series; and Wigner's 2n+1 rule reproduces `E_4` and `E_5` from `psi_1, psi_2` alone.

## 5. Criterion A: a central element acting as -I (item 1)

**Theorem A.** Let `z` be central in `G` with `rho_F(z) = -I`. For a set `E` of links meeting every plaquette an odd number of times, let `U_E = prod_{e in E} Pi_e` with `(Pi_e psi)(…,U_e,…) = psi(…, z U_e, …)`. Then `U_E` is unitary, commutes with every link Casimir, every endpoint gauge action and every on-site cutoff projection, fixes the vacuum `Omega_0`, and `U_E W_f U_E^* = -W_f` for every plaquette `f`. Hence

\[
U_E\,H^G_N(\tau)\,U_E^*=H^G_N(-\tau)\quad\text{in every open centered whole-star box and every on-site cutoff},\qquad U\,H_{FG}(G)(\tau)\,U^*=H_{FG}(G)(-\tau),
\tag{HNM-BD1-F05}
\]

with `(Uf)(U_P) = f(z U_P)` on the one plaquette, and `omega_{-tau}(W) = -omega_tau(W)` wherever the ground eigenvalue is simple: on the one plaquette for `|tau|` below `48 C_F`, and in the box `Lambda_N` for `|tau|` below the box-dependent radius `12 C_F/(21 (2N)^3)`.

*Proof.* Haar measure is invariant under multiplication by `z`, so `Pi_e` is unitary and fixes the constant function `Omega_0`. Because `z` is central, `Pi_e` commutes with every left and right translation of `U_e`. On the Peter–Weyl block of the irrep `r` at the link `e`, `Pi_e` acts by the scalar by which `z` acts on `r` (Schur), so it commutes with `C_2(e)` and with every function of the link Casimirs, including every on-site spectral cutoff projection; commuting with translations, it commutes with the endpoint gauge actions `U_e ↦ g_x U_e g_y^{-1}`. If `e` is a link of `f`, replacing `U_e` by `z U_e` multiplies the holonomy `U_f` by `z` or `z^{-1}` (centrality), so `chi_F(U_f)` becomes `-chi_F(U_f)` and `W_f` becomes `-W_f`; with `|f cap E|` odd, `U_E W_f U_E^* = -W_f`. The electric terms are fixed, so (F05) holds, and in each cutoff space it holds for the compressions. If the ground eigenvalue of `H(tau)` is simple, `U_E psi(tau)` spans the ground space of `H(-tau)`, so `omega_{-tau}(A) = omega_tau(U_E^* A U_E)` for every bounded `A`, and `omega_{-tau}(W) = -omega_tau(W)`. On the one plaquette the same argument uses the translation of the holonomy by `z`, which is diagonal on characters. ∎

**Kato radius.** The free gap is `8 C_F` in the box (one excited link, Lemma 2.1) and `32 C_F` on the one plaquette; `||W_f||` is at most 1. A simple isolated ground eigenvalue persists, analytically in complex `tau`, while `|tau| ||V_1||` is below half the gap: `|tau|` below `48 C_F` on the one plaquette and below `12 C_F/F_N` in `Lambda_N` with `F_N = 21 (2N)^3` retained faces. The box radii for `N=2,3,4` are `3/448, 1/504, 3/3584` (SU(2)), `1/84, 2/567, 1/672` (SU(3)), `15/896, 5/1008, 15/7168` (SU(4)), `3/140, 2/315, 3/1120` (SU(5)), `1/112, 1/378, 1/896` (U(1) and Z2) and `1/56, 1/189, 1/448` (SO(3)). **They shrink with `N`: no statement holding for all `N` at once is made for any group other than SU(2)**, whose AM2 regime `|tau|` at most `10^-8` is admitted separately.

**Which groups have such `z` (exact reasons).**

| group | centre | element with `rho_F(z) = -I` | reason |
|---|---|---|---|
| SU(2) | `{I, -I}` | `-I` | `det(-I) = (-1)^2 = 1` |
| SU(3) | `Z_3 = {e^{2 pi i k/3} I}` | none | cube roots of unity are never -1; `det(-I) = (-1)^3 = -1` |
| SU(4) | `Z_4` | `-I = e^{2 pi i 2/4} I` | `det(-I) = (-1)^4 = 1` |
| SU(5) | `Z_5` | none | fifth roots of unity are never -1; `det(-I) = -1` |
| U(1) | all of U(1) | `e^{i pi}` | charge-1 character value -1 |
| Z2 | Z2 | the nontrivial element | sign character value -1 |
| SO(3) | trivial | none | `-I` is not in SO(3): `det(-I) = (-1)^3 = -1` |

`criterion_A_central_minus_one` verifies these facts exactly (central elements as turns `t`, value `e^{2 pi i t}` on `F`, equal to -1 exactly when `t - 1/2` is an integer), checks on the one-plaquette character basis that `U_z W U_z^* = -W` and that `U_z` commutes with `32 C_2` for the four flip groups (W changes the grade by one), and rejects the SU(3) element `e^{2 pi i/3} I`, a fifth root for SU(5) and the identity of SO(3) presented as `-I`. The absence of a central `-1` is **recorded as the reason**; the **proof** of non-transfer for SU(3), SO(3) and SU(5) is the nonzero even-order coefficient of Section 7.

**Exact fixtures on the box.** `criterion_A_box_models` evaluates all 1344 retained faces of `Lambda_2` in rational configurations of SU(2) (unit quaternions), SU(4) (signed permutation matrices of determinant 1, `z=-I`), U(1) (rational points of the unit circle) and Z2 (signs), and checks `W_f(zU on E) = -W_f(U)` and gauge invariance face by face. A centre gauge transformation (a coboundary, even on every plaquette) presented as the flip, and `E_3` minus one link, are rejected. These are finite algebra audits, not the operator proof.

## 6. Criterion B: the third moment (item 2)

**Lemma 6.1 (single-occurrence orthogonality).** In every listed group, a product of face variables `W_{f_1} … W_{f_k}` has Haar mean 0 if some link lies in exactly one of the `f_i`. *Proof.* As a function of that link's `U_e`, the product is a linear combination of matrix coefficients of `F` and of `Fbar` (a single factor `Re chi_F(U_f)` is linear in the `rho_F` or `rho_Fbar` entries of each of its links), and the Haar mean of a matrix coefficient of a nontrivial irrep vanishes. ∎ Distinct plaquettes share at most one link (`criterion_B_box_models`: every pair among the 417 plaquettes of `Lambda_1`).

**Lemma 6.2 (the degenerate level).** The gauge-invariant eigenspace of `sum 8 C_2` at energy `32 C_F` in `H^G_N` is spanned by `chi_F(U_g) Omega_0` and `conj(chi_F(U_g)) Omega_0` over the plaquettes `g` of the box (one vector per plaquette when `F` is self-conjugate).
*Proof.* A vector in the level has excited links with Casimir sum `4 C_F`; by Lemma 2.1 each excited link contributes at least `C_F`, so at most four links are excited. Gauge invariance at a vertex touched by exactly one excited link fails (a nontrivial irrep has no invariant), so the excited links form a simple graph with every degree at least 2 and at most four edges: a cycle of length at most 4. `Z^3` is bipartite, so there is no cycle of length 3, and the cycle has four links, each of Casimir exactly `C_F`, hence carrying `F` or `Fbar` (Lemma 2.1). The 4-cycles through a site are exactly its 12 plaquettes (enumerated), and gauge invariance at the four degree-2 vertices leaves exactly the two orientations `chi_F(U_g)` and `conj(chi_F(U_g))`. ∎ `criterion_B_box_models` records every Casimir decomposition of `4 C_F` over the irreps within ten steps of the trivial one (stable from eight steps): besides four copies of `C_F`, they are single links of Casimir `4 C_F` (for instance SU(3) `(3,1)` and its conjugate, SU(5) `S^3` and its conjugate, U(1) charge 2; SU(4) also has irreps of Casimir `15/2`), two links (SO(3) `l=2` with `l=1`) and three links (SU(4) three copies of `Lambda^2`; SU(5) `F, Lambda^2, Lambda^2`), all excluded by the degree and bipartite argument. This is why the level contains `Im chi_F(U_g) Omega_0` as well as `W_g Omega_0` for U(1) and for SU(N), N at least 3.

**Theorem B.** On `H_FG(G)` and on every `H^G_N` (each box inside its Kato radius, `W` a retained face, cutoffs included), if `E[W^3] = 0` then the first-order tau-derivatives at 0 of `omega(W^2)`, of the centred Euclidean correlation `C(s) = (chi, e^{-s(H-E)} chi)` (every `s` at least 0) and of the centred real-time correlation `c(theta) = (chi, e^{i theta(H-E)} chi)` (every real `theta`) vanish, with `chi = (W - omega(W)) psi/||psi||`, and the first-order splitting of the whole level of Lemma 6.2 vanishes. If `E[W^3]` is nonzero, the derivatives are nonzero on `H_FG(G)`.

*Proof.* Write `epsilon = 32 C_F` and `psi_1 = a sum_f W_f Omega_0` (one term on the one plaquette). Every first-order term is a Haar mean of three face variables:
- state term: `2 e^{-epsilon s} Re (W^2 Omega_0, psi_1) = 2a e^{-epsilon s} sum_f E[W^2 W_f]`;
- vector-centring term: `-2 m_1 e^{-epsilon s} E[W] = 0`, although `m_1 = 2a E[W^2]` is not zero;
- Duhamel term (exact at first order because `W Omega_0` is an eigenvector of the free part): `-s e^{-epsilon s}(W Omega_0, (V_1 - E_1) W Omega_0) = (s/3) e^{-epsilon s} sum_f E[W W_f W]`;
- energy term: `E_1 = -(1/3) sum_f E[W_f] = 0`;
- `omega(W^2)`: `d/dtau = 2a sum_f E[W^2 W_f]`;
- real time: the same sums with `e^{i epsilon theta}` and `-(i theta/3) e^{i epsilon theta}`.

By Lemma 6.1 every sum reduces to its `f = W` term, `E[W^3]`. On the level of Lemma 6.2 the matrix elements `(chi^s(U_g) Omega_0, W_f chi^t(U_h) Omega_0)` vanish unless `g = f = h` (for `g ≠ h`, `g xor h` has at least six links and `f` covers at most four; for `g = h ≠ f`, three links of `f` are carried once), and for `g = f = h` they are cubic moments `E[chi^a conj(chi)^b]`, `a+b = 3`, of one Haar holonomy. Since `E[W^3] = (2 dim F)^{-3} sum_a C(3,a) E[chi^a conj(chi)^{3-a}]` is a sum of nonnegative integers with positive weights, `E[W^3] = 0` exactly when every cubic moment vanishes, and then the whole level has zero first-order splitting. Kato analyticity in each box turns the vanishing Taylor coefficients into vanishing derivatives. Conversely on `H_FG(G)`: `d omega(W^2)/d tau = 2a E[W^3]`, `C(s)` has first-order term `e^{-epsilon s} E[W^3](2a + s/3)` and `c(theta)` has `e^{i epsilon theta} E[W^3](2a - i theta/3)`, nonzero for every `s` at least 0 and every real `theta` when `E[W^3]` is nonzero. ∎

| group | `E[W^3]` | level matrix `(chi_s, W chi_t)` on `{F, Fbar}` | `d omega(W^2)/d tau` | `C(s)`: coefficient of `e^{-epsilon s}` / of `s e^{-epsilon s}` |
|---|---|---|---|---|
| SU(2) | 0 | `[0]` | 0 | 0 / 0 |
| SU(3) | 1/108 | `[[0, 1/6], [1/6, 0]]` | **1/6912** | 1/6912 / 1/324 |
| SU(4) | 0 | `[[0,0],[0,0]]` | 0 | 0 / 0 |
| SU(5) | 0 | `[[0,0],[0,0]]` | 0 | 0 / 0 |
| U(1) | 0 | `[[0,0],[0,0]]` | 0 | 0 / 0 |
| Z2 | 0 | `[0]` | 0 | 0 / 0 |
| SO(3) | 1/27 | `[1/3]` | **1/2592** | 1/2592 / 1/81 |

All first-order derivatives carry `tier: exact_first_order` and `route_of_computation: characters`. On `Lambda_2` the box sums reproduce the one-plaquette values for every group (state sum = Duhamel sum = `E[W^3]`, energy sum 0, mean sum `E[W^2]`). Flip and parity are separate columns: **SU(5) has parity without flip**.

## 7. Obstruction cells (item 4)

The relevant fact is this: **if a unitary `U` commuting with `32 C_2` and reversing `W` existed on `H_FG(G)`, then `U H(tau) U^* = H(-tau)`, the simple ground eigenvalue would give `omega_{-tau}(W) = -omega_tau(W)`, and every even Taylor coefficient of the analytic function `omega(W)` would vanish.** A nonzero even-order coefficient is therefore an exact counterexample that excludes every such unitary on that model.

### 7.1 SU(3)
- No central `-I` (Section 5); `det(-I) = -1`.
- `E[W^3] = 1/108` (≈ 9.2593e-3): `E[chi^3] = E[conj(chi)^3] = 1` from the epsilon tensor.
- `d omega(W^2)/d tau = 2a E[W^3] = 1/6912` (≈ 1.4468e-4), with `a = 1/128`.
- Second-order coefficient of `omega(W)`: `(psi_1, W psi_1) + 2 (W Omega_0, psi_2) = a^2 E[W^3] + 2a^2 E[W^3] = 3a^2 E[W^3] =` **1/589824** (≈ 1.6954e-6), nonzero.
- Hence `omega(W)` is not odd in `tau` on `H_FG(SU(3))`, the first-order parity fails, and the level `{chi_F, chi_Fbar}` splits at first order by `±1/18` (the matrix `-(1/3)[[0,1/6],[1/6,0]]`).

### 7.2 SO(3)
- Trivial centre; `-I` is not in SO(3).
- `E[W^3] = 1/27` (≈ 3.7037e-2): `E[chi_1^3] = 1` (`epsilon_{ijk}`).
- `d omega(W^2)/d tau = 1/2592` (≈ 3.8580e-4), with `a = 1/192`.
- Second-order coefficient of `omega(W)`: `3a^2 E[W^3] =` **1/331776** (≈ 3.0141e-6), nonzero; the level `{chi_1}` shifts at first order by `-1/9`.

### 7.3 SU(5)
- No central `-I`: the centre `Z_5` acts on `F` by fifth roots of unity; `det(-I) = -1`.
- `E[W^3] = 0`, so **the parity column is a transfer** (Theorem B).
- **`Z_5` grading.** Each application of `W` changes the 5-ality by `±1`, so the order-`m` coefficient of `omega(W)` is a combination of Haar means of `m+1` factors `chi_F` or `conj(chi_F)`, nonzero only if `a+b = m+1` with `a-b` divisible by 5. For `m = 2` (three factors, `a-b` in `{±1, ±3}`) every term vanishes, and so does `d omega(W^2)/d tau` (three factors). The first possible nonzero even order is `m = 4`, with `(a,b) = (5,0)` or `(0,5)` and `E[chi^5] = 1`. The checker records the 5-alities of `psi_m`: `{0}, {1,4}, {0,2,3}, {1,2,3,4}`, then all five.
- **Fourth-order coefficient.** `c_4 =` **1/63403380965376 = 1/(2^30 3^10)** (≈ 1.5772e-14), nonzero, computed three ways: the direct Rayleigh–Schrödinger expectation series; Hellmann–Feynman `c_4 = -15 E_5` with `E_5` from the direct energy series; and Wigner's 2n+1 rule `E_5 = (psi_2, V_1 psi_2) - E_3 ||psi_1||^2 - 2E_2 (psi_1, psi_2) - E_1 ||psi_2||^2` with `E_1 = E_3 = (psi_1, psi_2) = 0`. The only channel is `Lambda^2 = (1,1,0,0)` ↔ `Lambda^3 = (1,1,1,0)` inside `psi_2` (`F x Lambda^2` contains `Lambda^3`, `Fbar x Lambda^3` contains `Lambda^2`): with `a = 5/1152`, the `Lambda^2` and `Lambda^3` components of `psi_2` are each `1/7962624` and the connecting matrix element of `W` is `1/10`, giving `E_5 = -1/951050714480640` and `c_4 = 1/(2^30 3^10)`. `route_of_computation: characters`; no tier.
- Hence `omega(W)` is not odd in `tau` on `H_FG(SU(5))`, and no unitary commuting with `32 C_2` and reversing `W` exists on that model: **SU(5) is a recorded flip obstruction, with the parity column a transfer.** The odd coefficient `c_3 = 29/8026324992000` is also recorded.

**Supplementary remark (not the exhibited counterexample).** On `H_FG(G)` a unitary with `U W U^* = -W` needs the spectrum of the multiplication operator `W`, which is the range `W(G)`, to be symmetric, hence `-1` in `W(G)`, that is some `g` with `rho_F(g) = -I`. For SU(3) the range is `[-1/2, 1]` (the minimum at `e^{2 pi i/3} I`), for SO(3) `[-1/3, 1]`, and for SU(5) the value `-1` is not attained (`rho_F(g) = -I` forces `g = -I`, of determinant -1). This remark is a second argument and is not used in place of the coefficients.

## 8. Flip sets (item 5)

`E_3 = {(p,x): p_y even} u {(p,y): p_z even} u {(p,z): p_x even}` and `E_2 = {(p,x): p_y even}` are parsed from the contract; `E_3` equals the admitted AW1 set read from the AW1 gate.

**All of Z^3.** `|f cap E_3|` depends only on the orientation and on `p mod 2` (even translations preserve `E_3`); the 24 classes are enumerated with covariance under 12 even shifts each, and every class meets `E_3` in 1 or 3 links.

**Boxes** (every plaquette whose four links the box owns, and every retained whole-star face):

| `N` | owned links | plaquettes | meeting `E_3` once / three times | retained faces | once / three times |
|---|---|---|---|---|---|
| 2 | 3000 | 2335 | 1082 / 1253 | 1344 | 672 / 672 |
| 3 | 8232 | 6909 | 3630 / 3279 | 4536 | 2268 / 2268 |
| 4 | 17496 | 15291 | 7348 / 7943 | 10752 | 5376 / 5376 |

The `N=2` counts reproduce the AW1 forward report (1344, 2335, 1082, 1253), and the fine box `[-9,9]^3` of base points reproduces the AW1 reverse counts (20577 plaquettes, 10830 once, 9747 three times); both are parsed from the snapshots.

**Coarse factors.** For the seven probed factors `(0,0,0), (0,0,1), (1,0,0), (0,1,0), (1,1,1), (-1,-1,-1), (2,-3,5)`: `E_3` contains 16 of the 24 links of a factor with even `z` (4 x-links, 8 y-links, 4 z-links) and 8 with odd `z` (no y-link); each of the 52 plaquettes meeting a factor (19 once and 33 three times at even `z`, 33 and 19 at odd `z`), each of its 49 omitted faces and each of its 3 selected faces meets `E_3` oddly. **`E_3` is not invariant under odd coarse translations in `z`** (the y-links change parity); it is invariant under coarse x and y translations (fine shifts 4 and 2) and even z translations. The flip lemma does not need translation invariance.

**Two dimensions.** On `[-N,N]^2`, `N=2,3,4` (16, 36, 64 plaquettes), `E_2` contains exactly one link of every plaquette (one of its two x-links; no y-link).

**Periodic tori (recorded as an obstruction, not verified).**
- `E_3`: 0 even plaquettes on `4x4x4`; 16 even seam plaquettes on each of `3x4x4`, `4x3x4` and `4x4x3`; 24 on `3x3x4`.
- `E_2`: 0 on `4x4`; 4 on `4x3` (odd y side); 3 on `3x3`; and 0 on `3x4` (odd x side, even y side), because `E_2` is keyed to `p_y` only.
- *Remark, not claimed:* GF(2) elimination shows that some flip set exists on tori with at most one odd side (3D) or at least one even side (2D), and none when two sides are odd (`3x3x4`, `3x3x3`, `3x3`). **No flip or parity statement is made on any periodic box.**

Damaging mutations: `E_3` minus one link, `E_2` plus one link, an odd periodic side presented as verified, and `E_3` claimed invariant under an odd coarse z translation.

## 9. SU(2) area parity (item 6)

Model: the AM2/AQ1 zero-selected patterned family (`AQ_patterned_zero_selected`: selected triple `(0,0,0)`, Haar reference, whole stars `-(tau/3) sum W_f`), `kappa = 0`, both signs, `|tau|` at most `10^-8` (evaluated at `tau = ±1/100000000`), with the admitted AW1 and BB2 statements under their own gate labels. `W_C = (1/2) Tr` of the ordered holonomy of a closed path `C` of plaquette edges.

**Lemma 9.1 (surface parity).** For every finite set `S` of plaquettes of `Z^3` (a `Z_2` 2-chain), the sum over `p` in `S` of `|p cap E_3|` is congruent to `|S|` mod 2 (each plaquette meets `E_3` oddly) and to `|dS cap E_3|` (a link interior to `S` is counted an even number of times). Hence every closed surface of plaquettes has an even number of plaquettes, and for every spanning surface `S` of `C` (`dS = C` mod 2), `A(C) = |S|` is congruent to `|C cap E_3|` mod 2, independently of `S`. ∎

**Theorem 9.2 (boxes and cutoffs).** In every open centered whole-star box `Lambda_N`, `N` at least 2, in every on-site cutoff and for the untruncated ground vectors, `omega_{N,-tau}(W_C) = (-1)^{A(C)} omega_{N,tau}(W_C)` for every loop `C` of plaquette edges in the box.
*Proof.* AW1 (admitted): `U_E H_N(tau) U_E^* = H_N(-tau)` at `kappa = 0`, including every on-site cutoff compression, and `U_E Omega_0 = Omega_0`. AM2 (admitted): the ground eigenvalue is simple in every box and cutoff at both signs, so `psi_N(-tau)` is `U_E psi_N(tau)` up to a phase and `omega_{N,-tau}(A) = omega_{N,tau}(U_E^* A U_E)`. Since `-1` is central in SU(2), flipping a traversed link multiplies the holonomy by `-1` once per traversal, so `U_E^* W_C U_E = (-1)^{|C cap E_3|} W_C` (traversals counted), and Lemma 9.1 gives `(-1)^{A(C)}`. ∎

**Theorem 9.3 (the limit of the named constructions).** For the limit `omega_inf^{±tau}` of the named constructions (BB2 gate, whole-sequence convergence of F1 and F2 at each sign), `omega_inf^{-tau}(W_C) = (-1)^{A(C)} omega_inf^{tau}(W_C)` pointwise for every loop `C`; more generally `omega_inf^{-tau} = omega_inf^{tau} ∘ alpha_E` on the quasi-local algebra.
*Proof.* Let `Y` be the finite complete-factor region of the owners of the links of `C`; `W_C` lies in `B(H_Y)`. `U_E` is a product over links, so `U_E = U_{E cap Y} ⊗ U_{E \ Y}` and, for every `N` with `Y` inside `Lambda_N`, `rho^{F1,N}_Y(-tau) = U_{E cap Y} rho^{F1,N}_Y(tau) U_{E cap Y}^*`. BB2 gives, **at each sign separately and along the whole sequence**, `||rho^{F1,N}_Y(±tau) - rho^inf_Y(±tau)||_1` at most `c'_site |Y| e^{|Y|/10^8} q^{d_Y}` with `c'_site = 2/984375`, `q = 1/64` and `d_Y = N - max_{y in Y}|y|_inf` (read from the BB2 gate). Conjugation is trace-norm continuous, so the identity passes to the limits. No common subsequence is needed, because both sequences converge; the AW1 whole-set statement alone would give only `S(-tau) = S(tau) ∘ alpha_E` as sets, and the mutation that uses it for a pointwise claim is rejected. ∎

**Centre-even observables are even in `tau`.** A bounded local `A` with `U_E^* A U_E = A` (for example `W_C^2`, or `W_C W_{C'}` with `A(C)+A(C')` even) has `omega(A)` even in `tau`, in every box and cutoff and for the limit. The link Casimirs are reached through their bounded spectral cutoffs `C_e 1_[0,L](C_e)`, which commute with `U_E`, and the monotone limit `L → infinity`. The one-plaquette fixtures of the four flip groups show the same pattern exactly: odd series for `omega(W)`, even series for `omega(W^2)` and for `omega(C_2)`.

**Exact audits (`area_parity_box_and_limit`).** Nine loops in `Lambda_2` — the W face (area 1), rectangles `xy 2x1`, `xz 2x2`, `yz 3x2`, `xy 3x3`, `xz 1x3` and `yz 2x2`, a bent loop (area 2) and a hexagon around a cube corner (area 3) — each with two disjoint spanning surfaces (flat and a cap, or the complementary cube faces) whose `Z_2` boundary is `C`: `|C cap E_3|`, `|S|` and `|S'|` have equal parity in every case, and the rational-quaternion value of `W_C` changes by `(-1)^{A(C)}` under the flip and not under a gauge transformation. Five closed surfaces (a cube, a `2x1x1` bar, an L tromino, a `2x2x2` block, and a ring of eight cubes of Euler characteristic 0) have 6, 10, 14, 24 and 32 plaquettes. For each loop the BB2 bound `2 c'_site |Y| e^{|Y|/10^8} q^{d_Y}` on the parity defect of the limit is exactly geometric in `N` (ratio `q`) and falls below `10^-40` by `N = 20` to `22`; the defect is therefore 0. A 2x2 partial-trace fixture checks `rho_Y(U psi) = u_Y rho_Y(psi) u_Y^*` for a product unitary exactly.

**Scope.** Claimed only for SU(2), the zero-selected family, `kappa = 0`, open centered whole-star boxes, on-site cutoffs and the limit of the named constructions; **not** for periodic boxes with an odd side, F2 or literal vertex boxes, nonzero selected triples, or any other group (`area_parity_scope` rejects each).

## 10. Transfer ledger (item 7)

Status labels: `transfer_to_named_model` (a labelled statement about `H_FG(G)` and `H^G_N`, with its own exact checks), `obstruction_recorded` (with its exact counterexample), `admitted_su2_reference`, `not_asserted`, `obligation`.

| group | flip lemma | parity theorem | first-order coefficient | dictionary | AM2/AQ chain |
|---|---|---|---|---|---|
| SU(2) | transfer (`z=-I`; the admitted AW1 lemma) | transfer (`E[W^3]=0`) | 1/144 (convention check) | admitted SU(2) reference (AZ1/AL1), not re-derived | admitted SU(2) reference |
| SU(3) | **obstruction**: `c_2 = 1/589824` (reason: `Z_3`) | **obstruction**: `d omega(W^2)/d tau = 1/6912` (`E[W^3]=1/108`) | 1/1152 | not asserted | obligation |
| SU(4) | transfer (`z=-I`, `det(-I)=1`) | transfer | 1/2880 | not asserted | obligation |
| SU(5) | **obstruction**: `c_4 = 1/63403380965376` (reason: `Z_5`) | transfer | 1/5760 | not asserted | obligation |
| U(1) | transfer (`z=e^{i pi}`) | transfer | 1/96 | not asserted | obligation |
| Z2 | transfer (nontrivial element) | transfer | 1/48 | not asserted | obligation |
| SO(3) | **obstruction**: `c_2 = 1/331776` (reason: trivial centre) | **obstruction**: `1/2592` (`E[W^3]=1/27`) | 1/864 | not asserted | obligation |

Every transfer is to `H_FG(G)` and `H^G_N` (the operator identity in every box and cutoff; oddness and first-order statements in each box inside its Kato radius). **For every group other than SU(2) the AM2/AQ chain is an obligation**: AM2 re-instantiation (onsite gap `8 C_min`, majorant, fixed point, gaps, cutoff removal), the AV1 product split and anchored-norm tier, the AQ1 construction and dynamics with the AQ2 gap, BB1/BB2 comparisons, a dictionary to a bare coupling, and a group-specific selected-strip reference if a nonzero triple is ever used. The SU(2) constants `1/144`, `tau = 96/g^4` and `alpha = g^2/(2a)` are read from the gates only to reject their transfer.

## 11. Error ledger (preregistered terms)

| term | status | reason |
|---|---|---|
| `moment_arithmetic` | zero | exact Fractions on integer multiplicities; three character sub-routes agree exactly |
| `character_multiplicities` | zero | exact integer multiplicities (Pieri, Clebsch–Gordan, charge counting, summation), dimension counts on 187 irreps, closed-form Schur–Weyl/hook-length, charge, parity and Catalan counts |
| `weyl_constant_terms` | not_applicable | the Weyl route is the reverse route; the labelled forward-internal cross-check computes integer constant terms exactly (divisibility by the Weyl group order checked) and is never an admission value |
| `one_plaquette_truncation` | not_applicable | the character-basis algebra is exact: order `m` uses only irreps reachable by `m` applications of `W`; depth-7 and depth-9 cutoffs give identical series through order 5, and a depth-1 cutoff is rejected |
| `flip_set_enumeration` | zero | complete enumeration of every plaquette of the named boxes, factors and tori; the 24 residue classes with even-shift covariance cover `Z^3` |
| `bb2_limit_passage` | zero | the parity identity holds exactly at every `N` and each sign; the limit defect is at most `2 c'_site |Y| e^{|Y|/10^8} q^{d_Y}` for every `N`, which tends to 0 |
| `arithmetic` | not_applicable | no numeric cost: exact Fractions throughout; decimals are truncated previews |

## 12. Scaling brackets

Evaluated exactly at `tau = 1/100000000` and `tau/100`: every first-order term `c_1 tau` has ratio exactly **100**; the obstruction second-order terms `c_2 tau^2` (SU(3), SO(3)) exactly **10000**; the SU(5) fourth-order term `c_4 tau^4` exactly **100000000**; the moments exactly **1** (tau-independent). A second-order term relabelled first order and a fourth-order term relabelled second order are rejected.

## 13. Mandatory sentence and gate fields

The frozen template, quoted once as one unbroken span:

Under the frozen convention, the link-flip lemma transfers exactly to the listed gauge groups that have a central element acting as -1 on the Wilson representation and the first-order parity theorem exactly to those with vanishing third Haar moment of W, each with its own first-order Wilson coefficient, on one-plaquette models and on group box models in each box separately; SU(3) and SO(3) are recorded obstructions with exact nonzero coefficients, and SU(5) is a recorded flip obstruction with an exact nonzero fourth-order coefficient; for SU(2) in the zero-selected family at kappa=0 the Wilson-loop mean is odd or even in tau according to the parity of the number of plaquettes of any spanning surface of the loop, in every open centered whole-star box and for the limit of the named constructions; these are statements about named models and one-plaquette finite graphs, not AM2 or continuum statements for other groups, not statements for periodic boxes with an odd side, not uniqueness of any ground state, and not a statement uniform in the lattice spacing a.

Gate fields exported (equal to `gate_fields_required`): `model_is_finite_graph: true`, `transfers_to_aq: false`, `flip_transfer_claimed: true`, `flip_transfer_scope` as frozen, with the groups named as **SU(2), SU(4), U(1), Z2** on `H_FG(G)` and `H^G_N`; `parity_transfer_claimed: true` (**SU(2), SU(4), SU(5), U(1), Z2**); `obstructions_recorded: true` (flip: SU(3), SU(5), SO(3); parity: SU(3), SO(3)); `area_parity_limit_claimed: true`; and `uniqueness_of_ground_state_claimed`, `rate_in_a_claimed`, `continuum_claim`, `weak_coupling_claim`, `scientific_priority_verified` all `false`.

## 14. Exclusions, limitations and contract wording findings

**Claim exclusions (contract, verbatim):** any AM2, AV1 or AQ statement for a group other than SU(2); a dictionary to a bare coupling for a group other than SU(2); weak coupling or continuum; uniqueness of any ground state; any estimate uniform in the lattice spacing a; scientific priority; a flip or parity statement for SU(2) at a nonzero selected triple, in periodic boxes with an odd side, or in F2 or literal vertex boxes.

**Limitations.**
1. The group-cell statements are about `H_FG(G)` (finite graphs) and `H^G_N` (each box separately, inside a box-dependent Kato radius that shrinks with `N`). Nothing is claimed for all `N` at once for any group other than SU(2), and no limit state is constructed for any other group.
2. Simplicity of the finite-box ground eigenvalue (Kato; AM2 for SU(2)) is a hypothesis of every oddness statement, not a claimed result about any infinite-volume state.
3. The SU(2) corollary inherits without re-proof the AW1 flip lemma, AM2 simplicity and cutoff removal, and BB2 whole-sequence convergence, with BB2's own limitations (named constructions only; no statement about other states or boundary conditions).
4. Kato's theorem, Peter–Weyl, the Weyl integration formula and Schur–Weyl duality are cited, not machine-checked; the finite enumerations and fixtures audit the identities and do not replace the proofs.
5. Independence from the reverse producer is limited to route and code; both routes use the admitted AW1 argument for the SU(2) structure, and the contract, selection note and gates state the mechanism.

**Contract wording findings (non-blocking).**
- `flip_sets` says periodic tori with an odd side are "recorded with the even plaquettes at the seam". For `E_2`, keyed to `p_y` only, a torus with an odd x side and even y side has no even plaquette (`3x4`: 0 of 12). It is recorded as such; no flip statement is made on any periodic box.
- `moment_tables_two_routes` asks for both routes per cell, while this producer's route is characters. The forward packet exports its character table and exercises the exact two-route comparison on a labelled forward-internal Weyl cross-check; the contract's comparison is with the reverse packet.
- Item 1 speaks of the ground state "being unique" while `uniqueness of any ground state` is excluded; this report reads it as simplicity of the finite-box ground eigenvalue used as a hypothesis (limitation 2).
- The model fixes no numerical Kato radius; the sufficient radii used are stated in Section 5.

**Methodological lenses (modern uses of the snapshotted skills).** *Newton, analysis before synthesis:* the representation content (5-ality, cubic moments, Casimir decompositions of the level) is analysed before any coefficient is written, and each obstruction is synthesized as an exact even-order coefficient rather than inferred from a missing symmetry. *Tesla, complete accounting:* every first-order channel (state, Duhamel, energy, vector centring, the whole degenerate level including the `Im chi_F` directions) is charged separately. No historical figure endorses anything here, and no historical or occult material supplies a premise.

## 15. Proposed verdict

**`accepted_within_scope`** for the forward route: criteria A and B are proved on the named models; every moment and first-order coefficient is exact on the character route (with the reverse comparison outstanding); the SU(3), SO(3) and SU(5) obstruction cells are exhibited with exact nonzero coefficients; the flip sets are verified; the SU(2) area parity holds in every open centered whole-star box and cutoff and pointwise for the limit of the named constructions; the transfer ledger is complete. The gate also needs the reverse route, the exact cross-route comparison and skeptical review.

## 16. Item and control map

| item | sections | checks |
|---|---|---|
| 1 criterion A | 5, 8 | `criterion_A_central_minus_one`, `criterion_A_box_models`, `flip_criterion_central_minus_one` |
| 2 criterion B | 6 | `criterion_B_third_moment`, `criterion_B_box_models`, `parity_criterion_third_moment` |
| 3 moments and coefficients | 3, 4 | `moments_characters_route`, `moment_tables_two_routes`, `first_order_coefficients`, `rayleigh_schroedinger_one_plaquette` |
| 4 obstruction cells | 7 | `su3_obstruction_mandatory`, `so3_obstruction_mandatory`, `su5_flip_obstruction_fourth_order` |
| 5 flip sets | 8 | `flip_sets_verified` |
| 6 SU(2) area parity | 9 | `area_parity_box_and_limit`, `area_parity_scope` |
| 7 transfer ledger | 10 | `flip_criterion_central_minus_one`, `parity_criterion_third_moment`, `am2_not_reinstantiated`, `no_transfer_called_prediction` |
| 8 template, gate fields, controls, replay | 13, 17 | `mandatory_sentence_and_gate_fields`, every control check, `coherent_evidence_tampering` |

| control | damaging mutations rejected |
|---|---|
| `coherent_evidence_tampering` | control Boolean flipped, snapshot removed, SU(3) third moment zeroed, U(1) coefficient set to 1/144, SU(5) fourth order zeroed, SU(3) added to the flip groups, continuum flag, gate field flipped — each with the hash rebound |
| `exact_arithmetic_admission` | float, bool, NaN, zero denominator |
| `no_priority_or_continuum_claim` | continuum, priority, weak-coupling flag set true |
| `changed_model_relabelled` | SU(2) value under the SU(3) label; one-plaquette value as a box value; group box value under the SU(2) family label; Z2 under another normalization; Wilson representation relabelled |
| `insufficient_verdict_retained` | failed cell reported accepted; route disagreement reported accepted; unproved criterion reported limited; convention retuned to pass |
| `placeholder_span_rejected` | angle-bracket placeholder containing "e.g."; angle-bracket span with a bar |
| `negation_aware_phrase_scan` | affirmative forbidden verb; affirmative forbidden phrase (a negated clause passes) |
| `parameters_declare_metric_weights_window` | window absent; not applicable without a reason; `d_X` declared |
| `tier_mixing_rejected` | plan route label; hypothesis source; floating value under a tier; tier on a moment; tier on a second-order coefficient; route outside the two labels; first-order value without tier |
| `frozen_convention_used` | Z2 "electric term 1 on the odd state"; Z2 "1 - sigma^x"; SU(3) other Casimir normalization; face energy `8 C_F`; SU(2) value copied to U(1) |
| `su2_constants_not_transferred` | U(1) dictionary `tau=96/g^4`; SU(4) given 1/144; SU(3) `alpha=g^2/(2a)` |
| `flip_criterion_central_minus_one` | SU(3) flip transfer; SU(5) obstruction from the missing centre alone; SU(4) transfer without the central element; SO(3) flip entry; U(1) flip on the AQ model |
| `parity_criterion_third_moment` | SU(3) parity transfer; SU(5) parity merged with the flip column; U(1) parity without its third moment |
| `moment_tables_two_routes` | cell missing from the second route; floating moment; routes disagree; the same route counted twice |
| `su3_obstruction_mandatory` | cell omitted; called flip transfer; called parity transfer; second order set to 0 |
| `so3_obstruction_mandatory` | cell omitted; given a central -1; derivative set to 0 |
| `flip_sets_verified` | `E_3` minus a link; `E_2` plus a link; odd periodic side verified; odd coarse z invariance claimed |
| `area_parity_scope` | periodic odd side; nonzero triple; other group; F2 box; literal vertex box; pointwise limit from subsequences; perimeter sign rule |
| `one_plaquette_model_terms` | `transfers_to_aq` true; per-link electric term on the plaquette; magnetic `-tau`; value presented as a limit value; free reference copied from SU(2); truncated series |
| `no_transfer_called_prediction` | transfer text with a forbidden verb; non-transfer without counterexample |
| `am2_not_reinstantiated` | U(1) AM2 chain as transfer; Z2 AQ statement; obligations emptied |
| `su5_flip_obstruction_fourth_order` | called flip transfer; parity called obstruction; obstruction from the missing centre alone; fourth order set to 0; route missing |

Non-control checks: `contract_binding`, `admitted_gate_binding` (pinned sha256 of the AW1, AW2, AY2, AZ1, AZ2 and BB2 gates), `character_rules`, `moments_characters_route`, `first_order_coefficients`, `rayleigh_schroedinger_one_plaquette`, `criterion_A_central_minus_one`, `criterion_B_third_moment`, `criterion_B_box_models`, `criterion_A_box_models`, `area_parity_box_and_limit`, `scaling_brackets`, `error_terms_itemized`, `mandatory_sentence_and_gate_fields`, `premise_inventory`.

## 17. Reproduction

```bash
python3 -B research/round33/forward/bd1/check.py --output /absolute/fresh/dir
python3 -B -O research/round33/forward/bd1/check.py --output /absolute/fresh/dir2    # byte-identical
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/bd1.json research/round33/forward/bd1/report.md
python3 -B research/round33/tools/freeze.py verify research/round33/forward/bd1
```
