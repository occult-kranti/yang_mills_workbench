# Hruday applications II in SU(2): the two-plaquette graph with independent couplings, the Z^3 1x2 Wilson loop, the electric-energy band on the cover and the 2+1D AM2 recount — BD2 forward (single producer)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production: the derivations, `check.py` and this report were written by a Claude model agent acting as the single BD2 forward producer under the frozen BD2 contract (`research/round33/contracts/bd2.json`, sha256 `783cad8054a9b7ed3f741e0c06fffd94cfa0d6fda0dcbb7aa0b464058e46f41e`). `check.py` verifies that digest before it parses any field. BD2 is a **single+skeptic** loop (investigation 8 of 8): admission also needs the skeptic's replay from the contract alone and its review. This is correlated model-agent work, not independent human review and not formal verification. HNM labels are project aliases.

**What this producer read.**
- **The contract snapshot first**, then only files under `inputs/` (35 files):
  - *read in full:* `AGENTS.md`; `selection-bd2.md`; the AZ2 forward report, the AZ2 forward `check.py` and `skeptic/az2.md`; the AM2, AQ1 and I1 forward reports; the Round11 README; the paired-physics SKILL and its complete-residual reference; the Newton and Tesla SKILL files;
  - *every field except `bindings`:* the AZ2, AW1, AV1, AV2, AY1, AY2, AM2, AQ1 and BB2 gates;
  - *read in part:* the AW1 forward report (Sections 1–7); the AY1 forward report (Sections 1–12); the AV1 forward report (header, Section 1, Sections 6.4–8); the AY2 forward report (headings and the lines on the `sqrt(10)` bracket and the tier); the BB2 forward report (header, verdict and headings); `skeptic/bb2.md` (opening and headings); the Round11 solver README (graph, parameters and certificate sections) and advisor report (Section 3 and headings); the BA1 and BB2 contracts (control lists and control semantics); the historical-panel SKILL (first forty lines);
  - *not opened:* `research/round11/solver/two_plaquette.py` (its hash is pinned and its conventions are bound by exact source strings, the list the admitted AZ2 checker uses).
- **Outside `inputs/`, for conventions only:** `research/round33/tools/README.md`, `research/round33/tools/freeze.py` and `research/round33/tools/phrase_scan.py` (its phrase list and negation frame are copied into `check.py` as infrastructure). None carries premise weight. The repository `CLAUDE.md` was in my session context; it is non-scientific.
- **Not read:** anything under `research/round33/forward/bd1/`, `research/round33/reverse/`, `research/round33/forward/bc1/`, `research/round33/forward/bc2/`, `research/round33/skeptic/` other than the snapshotted `bb2.md`, `research/round33/experts/`, `research/round33/advisor/` other than the snapshots in `inputs/`, and no other agent's scratch folder.
- **Scratchpad disclosure.** My private scratch folder is `/tmp/claude-0/bd2-forward-private/`. It holds prototype scripts (`proto*.py`, built from text copies of the AZ2 algebra), the assembly parts of `check.py` (`part*.py`, `az2_*.txt`), development drivers (`devrun.py`, `devledger.py`, a check dump), this report's draft and the production run `run1`. **None of it is evidence.** I created the folder with `mkdir -p` and did not list `/tmp/claude-0/`; I opened no file of any other agent. The Claude harness cached one of my own long reads (the AZ2 forward report) in its tool-results store; that is my own read.

**Attribution.** Rayleigh–Schrödinger and Kato perturbation theory, Rayleigh–Ritz, Weyl, Temple, Eckart, Davis–Kahan, Peter–Weyl and Haar orthogonality, trace duality and the Fuchs–van de Graaf inequality are established mathematics. The Round11 graph reduction, the AZ2 certificate code and every admitted gate are inherited. The contribution here is their application to the named new observables, couplings and dimension with exact constants. Scientific priority is unverified.

## Verdict (forward, single producer)

**Models.** (a) `FG(round11_two_plaquette_independent_couplings)`: `H_FG(l1,l2) = K - l1 W_1 - l2 W_2` in alpha units on the Round11 open two-square patch (6 vertices, 7 links, gauge-invariant sector; `K` the sum of the seven link Casimirs, rho=1), cutoffs `D` in {6, 8}. (b) `AQ_patterned_zero_selected` (AM2/AQ1 zero-selected family, `tau = ±1/100000000`), F1 and F2 boxes with `N>=2` and the limit of the named constructions (BB2). (c) The declared 2+1D model on `Z^2` (constants only).

1. **Item 1.** The exact coefficients of `<W_1>`, `<z>` and `<C_shared>` in `(l1,l2)` through total order 4 are identical at D=6 and D=8 with truncation error exactly 0. `<W_1>` is odd in `l1` (flip of `h1`, a non-shared link of face 1) and even in `l2` (flip of `h2`, a non-shared link of face 2); `<z>` is odd in each coupling; `<C_shared>` is even in each. At `l1=l2`: `<z> = (7/216) l^2 + ...` and `<C_shared> = (1/24) l^2 + ...`.
2. **Item 2.** All twelve `<z>` enclosures at `l1=l2` on the AZ2 grid exclude 0 with a certified positive sign at both cutoffs; every D=8 enclosure lies inside its D=6 one; the worst D=8 relative width is `1.79645e-17` (at `|l|=1/10`), below the frozen `1/10000000000000000` with margin 5.57.
3. **Item 3.** In the zero-selected family the 1x2 Wilson mean has first-order coefficient exactly 0 in every box, satisfies `|omega(W_{1x2})| <= K_2' tau^2` (about `1.34175e-12`) at both signs for every F1 and F2 box and for the limit, and is even in `tau` in every F1 box and for the limit. Its formal second-order coefficient is `7/124416` (label `formal_second_order_coefficient`: no sign, no certified remainder).
4. **Item 4.** For every F1 and F2 box and for the limit, at both signs, `2.87586637818e-19 <= omega(h_R) <= 9.8e-7` at `|tau| = 10^-8` (exact endpoints in Section 6).
5. **Item 5.** 2+1D recount: `p=3`, three faces per site, `J=|tau|`, termination order 6, `G_3(R) = 9 e^{3/32}`, `G_3'(R) = 118 e^{3/32}` with a directed enclosure, and the cap `|tau| <= 1580747155173/1000000000000000` (directed lower bound; the self-map condition binds). No 2+1D finite-volume theorem is claimed.
6. **Items 6–7.** Six obligation and no-transfer rows; the template once; gate fields exported; all 21 controls reject damaging mutations; `-B` and `-B -O` replays byte-identical.

**Proposed forward verdict: `accepted_within_scope`**, sub-labels `sign_certified_finite_graph`, `transfer_to_named_model`, `obstruction_recorded`, `static_not_dynamic`. Admission needs the skeptic's replay and review.

## 1. Models, units and conventions

**The graph (items 1–2).** Vertices TL, TM, TR, BL, BM, BR; links h1 (TL→TM), h2 (TM→TR), h3 (BL→BM), h4 (BM→BR), vL (TL→BL), vM (TM→BM), vR (TR→BR). Round11 G2: `U = vM h3^-1 vL^-1 h1` (square 1), `V = h2 vR h4^-1 vM^-1` (square 2), `x = W_1 = Tr(U)/2`, `y = W_2 = Tr(V)/2`, `z = Tr(UV)/2` (the 1x2 loop, the outer boundary of both squares; `vM` cancels). Every Hamiltonian term with its coefficient (rule R3):

| term | coefficient |
|---|---|
| `K`: the seven link Casimirs `j(j+1)`, rho=1 (`K = 3 C_U + 3 C_V + C_shared`) | 1 (alpha units) |
| `W_1 = (1/2) Tr U` | `-l1` |
| `W_2 = (1/2) Tr V` | `-l2` |

`C_shared` is the Casimir of the shared link vM (Round11 K1, derivative `L_U - R_V`); in the checker it is the operator `S` with leading eigenvalue `ell(ell+1)`, `ell=(a+b)/2`, and `S z = 0`, `S x = (3/4) x`, `S(xy) = 2xy - z/2`. The decomposition `K = 3C_U + 3C_V + C_shared` is checked on every monomial of degree at most 6. The free reference is computed in the same code path (order 0 of the series and `certify(pc, 0)`): `<W_1> = <z> = <C_shared> = 0`. Negative couplings lie outside the Round11 solver API (`lambda >= 0`); nothing below needs a sign (`||x||, ||y||, ||z|| <= 1`). Flags: `model_is_finite_graph: true`, `transfers_to_aq: false`.

**The Z^3 family (items 3–4).** SU(2) Kogut–Susskind form on `Z^3` at fixed spacing; coarse 24-link factors `T_b = {(4i+r, 2j+s, k)}` (I1.1); selected triple `(0,0,0)` with Haar product reference `P_R`; 21 omitted faces per anchor entering as `-(tau/3) W_f` in delta units (`delta = alpha/8`); `h_b = 8 sum_e C_e >= 6 Q_b >= Q_b`. Cover `R = {0, e_z}` (48 links). Families F1 (AQ1 centered whole-star boxes) and F2 (I1 §6 all-contained-face boxes with padding) on `Lambda_N = [-N,N]^3`, `N >= 2`; the limit of the named constructions is BB2's whole-sequence limit (BB2 gate items 2–3 identify it with every AQ1 and every F2 subsequential limit). `tau = ±1/100000000`.

**The 2+1D model (item 5, constants only).** `Z^2`, `8 C_e` on every link, `-(tau/3) W_f` on every elementary face, no selected faces, Haar product reference, delta units.

**Parameters.** Metric: trace norm on `B(H_R)` for states, energy expectations through the on-site cutoff by monotone limits. Weights, window and clock: not applicable (no decay estimate, static expectations, no clock). `d_X` and `N_0` do not apply.

## 2. Item 1: exact coefficients with independent couplings

**Series.** With `V1 = -x` and `V2 = -y` and intermediate normalization `E[psi_mn] = 0` for `(m,n) != (0,0)`:

`K psi_mn = -V1 psi_(m-1,n) - V2 psi_(m,n-1) + sum_(i,j) E_ij psi_(m-i,n-j)`, where `E_mn` is the Haar mean of `V1 psi_(m-1,n) + V2 psi_(m,n-1)`.

`K` is triangular in degree (Round11 E2), so every `psi_mn` is solved by degree back-substitution and lies in `P_(m+n)`; the full-space equation holds **as a polynomial identity** for `m+n <= 5`. The truncation error is therefore exactly 0, and the tables computed in `P_6` and in `P_8` are identical. Expectations `<O> = <psi,Opsi>/<psi,psi>` are expanded by bivariate series division. The first vectors are `psi_10 = x/3`, `psi_01 = y/3` and `psi_11 = 4xy/39 + 4z/351`.

**The table (exact; `(m,n)` = power of `l1`, power of `l2`; every entry with `m+n <= 4` that is not listed is exactly 0; all 15 entries per observable are exported in `results.json`).**

| observable | `(1,0)` | `(0,1)` | `(2,0)` | `(1,1)` | `(0,2)` | `(3,0)` | `(1,2)` | `(3,1)` | `(1,3)` | `(4,0)` | `(2,2)` | `(0,4)` |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `<W_1>` | 1/6 | 0 | 0 | 0 | 0 | -5/864 | 1/4212 | 0 | 0 | 0 | 0 | 0 |
| `<z>` | 0 | 0 | 0 | 7/216 | 0 | 0 | 0 | -349/303264 | -349/303264 | 0 | 0 | 0 |
| `<C_shared>` | 0 | 0 | 1/48 | 0 | 1/48 | 0 | 0 | 0 | 0 | -5/4608 | -49/438048 | -5/4608 |
| `E_0` | 0 | 0 | -1/12 | 0 | -1/12 | 0 | 0 | 0 | 0 | 5/3456 | -1/8424 | 5/3456 |

`<W_2>` is the exchange mirror, `<W_2>_(m,n) = <W_1>_(n,m)`.

**Consistency checks, all exact.**
- **Hellmann–Feynman:** `<W_1>_(m,n) = -(m+1) E_(m+1,n)` and `<W_2>_(m,n) = -(n+1) E_(m,n+1)` for every `m+n <= 4` (energies through total order 5).
- **Second route for `<C_shared>` at second order:** `x` is an exact eigenvector of the rho-weighted kinetic operator with eigenvalue `3(3+rho)/4`, so `E_20(rho) = -1/(3(3+rho))` (checked at rho=1 and rho=2 against the kinetic operators); `d/drho` at rho=1 gives `1/48 = <C_shared>_(2,0)`.
- **Sections:** the `l2=0` section gives `-5/864`, the one-face coefficient of the AZ2 skeptic record, and `(1,2) = 1/4212` is the second-square term recorded there (`tau^3/4212`).
- **Diagonal `l1=l2` (consistency with the admitted AZ2 equal-coupling series, not a transfer):** `<W_1>`: `0, 1/6, 0, -187/33696, 0`; `<z>`: `0, 0, 7/216, 0, -349/151632`; `E_0`: `0, 0, -1/6, 0, 187/67392`.

**Second-order coefficients at `l1=l2` (requested record).** `<z>`: `7/216` (`= c_11`, since `c_20 = c_02 = 0`). `<C_shared>`: `1/24` (`= c_20 + c_02`, since `c_11 = 0`). The fourth-order diagonal value of `<C_shared>` is `-7997/3504384`.

## 3. Item 1: the one-link centre flips and the parity table

For a link `e`, `F_e psi(..., U_e, ...) = psi(..., -U_e, ...)`. `-1` is central, so `F_e` commutes with every Casimir (hence with `K` and `C_shared`), with all six vertex gauge actions and with the Haar measure, and `F_e W F_e = (-1)^[e in loop] W` for every loop trace. On exact rational quaternions (seven links, four gauge trials) the flips act on `(x,y,z)` as follows:

| flipped link | action | effect on `H_FG(l1,l2)` |
|---|---|---|
| `h1`, `vL` or `h3` (non-shared, face 1) | `(-x, y, -z)` | `H(-l1, l2)` |
| `h2`, `vR` or `h4` (non-shared, face 2) | `(x, -y, -z)` | `H(l1, -l2)` |
| `vM` (shared) | `(-x, -y, z)` | `H(-l1, -l2)` only |

**Proof of the parities.** For every real `(l1,l2)` the ground state of `H_FG` is simple (Round11 Theorem F; its proof uses only a bounded real potential). Since `F_h1 H(l1,l2) F_h1 = H(-l1,l2)`, `psi(-l1,l2) = F_h1 psi(l1,l2)` up to a phase, so `<x>(-l1,l2) = -<x>(l1,l2)`, `<z>(-l1,l2) = -<z>(l1,l2)` and `<C_shared>(-l1,l2) = <C_shared>(l1,l2)`. With `F_h2`: `<x>` is even in `l2`, `<z>` odd in `l2` and `<C_shared>` even in `l2`. Coefficient by coefficient, `F_h1 psi_mn = (-1)^m psi_mn` and `F_h2 psi_mn = (-1)^n psi_mn` hold exactly for every `m+n <= 5`.

**Checked on the full table.** `<W_1>` is nonzero only for `m` odd and `n` even; `<z>` only for `m` and `n` both odd; `<C_shared>` only for `m` and `n` both even. Hence every even-order coefficient of `<W_1>` at `l1=l2` vanishes (orders 0, 2 and 4 are checked). The shared-link flip alone proves only the joint statement `(l1,l2) -> (-l1,-l2)`; a two-variable parity claimed from it, or a check at `l1=l2` only, is rejected by the control.

## 4. Item 2: certified enclosures of `<z>` at `l1=l2`

At `l1 = l2 = l` the Hamiltonian is the AZ2 model `K - l(W_1+W_2)`. The ground-state certificate is the admitted AZ2 certificate code, copied verbatim (63 blocks compared textually with the snapshot); only the observable changes. The copied code reproduces the AZ2 gate enclosure of `<W_1>` at D=8, `l=+1/10` exactly.

**Enclosure.** For a rational Ritz vector `v` in `P_D` with complete residual in `P_(D+1)`, the certified gap `E_1 >= 3 - 2|l|` (Weyl), and the Davis–Kahan and Eckart angles with the Round11 tail comparison give `sin(theta) <= s`. Then `|<v,zv>/<v,v> - <psi_0,zpsi_0>| <= 2 s sigma_z + 2 s^2 ||z||` with `sigma_z = ||(z-<z>)psi_0|| <= ||z|| = 1` (vector centering). Ends are rounded outward to denominators `10^45`.

| D | `l1=l2` | lower (preview) | upper (preview) | half-width | relative width | sign |
|---|---|---|---|---|---|---|
| 6 | ±1/1000 | `3.240740510578259506053328e-8` | `3.240740510578259506055529e-8` | 1.100e-29 | 6.79043e-22 | + |
| 6 | ±1/100 | `3.240717724665334529490919e-6` | `3.240717724665334750212580e-6` | 1.103e-22 | 6.81088e-17 | + |
| 6 | ±1/10 | `3.238440859055494033169085e-4` | `3.238440859078240126201977e-4` | 1.137e-15 | 7.02377e-12 | + |
| 8 | ±1/1000 | `3.240740510578259506054428e-8` | `3.240740510578259506054428e-8` | 2.814e-39 | 1.73689e-31 | + |
| 8 | ±1/100 | `3.240717724665334639851747e-6` | `3.240717724665334639851752e-6` | 2.822e-30 | 1.74212e-24 | + |
| 8 | ±1/10 | `3.238440859066867050597032e-4` | `3.238440859066867108774029e-4` | 2.908e-21 | 1.79645e-17 | + |

Exact exported ends at `l=+1/10`:
- D=8: `[40480510738335838132462907353125470123319/125000000000000000000000000000000000000000000, 64768817181337342175480593943907904225707/200000000000000000000000000000000000000000000]`;
- D=6: `[40480510738193675414613565611132598718891/125000000000000000000000000000000000000000000, 8096102147695600315504942557313271254517/25000000000000000000000000000000000000000000]`.

**Properties.** Every enclosure excludes 0 and is positive. `<z>` is even under the shared-link flip, so the `-l` certificate, which is computed separately, equals the flip image of the `+l` one exactly. Every D=8 enclosure lies inside its D=6 enclosure (observed and checked). The free reference is `[0, 0]` at both cutoffs in the same code path. **Target:** the relative width `(upper - lower)/min(|lower|, |upper|)` at D=8 is at most `1.79645e-17` at every nonzero grid point, against the frozen `1/10000000000000000`: met, with margin 5.57, dominated by `|l| = 1/10` (the Eckart angle grows with `|l|` while `<z>` scales like `(7/216) l^2`). The D=6 widths are reported, not targeted.

**The AZ2-type itemized residual at every point** (previews; the complete ledger of all 14 points is in `results.json`):

| point | `rho_Q^2` (complete omitted) | vM class | j (= k) class | product channel | `2XY` interference | `rho_P^2` | `sin(theta)` DK / Eckart | `T_joint` |
|---|---|---|---|---|---|---|---|---|
| D6, 1/1000 | 3.8110e-57 | 3.81e-57 | 2.89e-61 | 4.9893e-66 | 1.6859e-57 | 3.9e-199 | 2.05e-29 / 5.50e-30 | 1.37e-30 |
| D6, 1/10 | 3.8047e-29 | 3.80e-29 | 2.89e-33 | 4.9800e-34 | 1.6832e-29 | 1.8e-199 | 2.20e-15 / 5.68e-16 | 1.40e-16 |
| D8, 1/1000 | 3.9182e-76 | 3.91e-76 | 7.12e-82 | 3.3109e-85 | 1.7825e-76 | 3.0e-199 | 6.60e-39 / 1.40e-39 | 2.86e-40 |
| D8, 1/10 | 3.9113e-40 | 3.91e-40 | 7.12e-46 | 3.3044e-45 | 1.7793e-40 | 2.7e-199 | 7.05e-21 / 1.45e-21 | 2.91e-22 |

The five parts: (a) seven per-link rows (thresholds `123/2` and `96` on the non-shared links, `45` and `69` on vM); (b) the joint product channel with corner overlaps and the positive `2XY` interference; (c) the gauge projection, exactly 0 with its reason; (d) the Ritz residual with Davis–Kahan and Eckart angles, the Weyl gap `3 - 2|l|` (lower bound on `E_1 - E_0` from 2.8017 to 2.9980) and the observable step `2 s sigma_z + 2 s^2 ||z||`; (e) directed arithmetic (upward `isqrt`, outward export). `tail_lower` is 45 (D=6) and 69 (D=8).

## 5. Item 3: the Z^3 1x2 Wilson loop

**The rectangle.** In fine coordinates the original xz face `W` is `F1` at the origin (`r=0, s=0`) and the second face is `F2`, the xz face at `e_x` (`r=1, s=0`). `W_{1x2} = (1/2) Tr` of the holonomy around their union: links `(0,x)`, `(e_x,x)`, `(2e_x,z)`, `(e_x+e_z,x)`, `(e_z,x)` and `(0,z)`; the shared middle link `(e_x,z)` cancels. All six links are owned by `R` (owners `0, 0, 0, e_z, e_z, 0` under I1.1), so `W_{1x2}` is in `B(H_R)` with `||W_{1x2}|| <= 1`. Both faces are omitted with owner set exactly `R`. The fine enumeration reproduces the admitted pins: 82 faces meeting `R`, 10 inside `R`, 72 straddling, 16 containing `R`, 21 omitted faces per anchor, 49 per factor, and 33 per site of `R` without the other site. On the seven links of `F1` and `F2`, `(W_F1, W_F2, W_{1x2})` equals `(x, y, z)` of the Round11 graph (checked on exact rational quaternions).

**First order is exactly 0 in every box.** Every link of `W_{1x2}` occurs once and a single face covers at most three of its six links, so by the centre grading (AW1 F04) `E[W_{1x2} W_f] = 0` for every face and `E[W_{1x2}] = 0` (single-occurrence orthogonality; second route: the Round11 moments `E[z] = E[xz] = E[yz] = 0`). In every box of F1 and F2 the ground state is simple and isolated (AM2; AY1 item 1) and `V` is bounded, so `omega_N(W_{1x2})` is real-analytic in `tau` (Kato) with derivative at 0 equal to `2 Re<W_{1x2}Omega_0,psi_1> = (1/36) sum_f E[W_{1x2} W_f] = 0`. Also `Tr(P_R W_{1x2}) = Tr(rho^(1)_R W_{1x2}) = 0`, with `rho^(1)_R` the AY1 first-order density over the ten faces inside `R`; the positive control reproduces `Tr(rho^(1)_R W) = tau/144` (AW1).

**The admitted bound, both signs, every box and the limit.**

`omega(W_{1x2}) = Tr(P_R W_{1x2}) + Tr(rho^(1)_R W_{1x2}) + Tr((rho_R - P_R - rho^(1)_R) W_{1x2})`, so `|omega(W_{1x2})| <= ||W_{1x2}|| · ||rho_R - P_R - rho^(1)_R||_1 <= K_2' tau^2`.

- **Every F1 and F2 box** (untruncated ground vector at fixed `N`, every `N >= 2`): the per-box ball of AY1 forward HNM-AY1-F11 to F14, uniform in `N`, in the cutoff and in both families, and passed to the untruncated ground vector by AV1 F22 — a reviewed step of the admitted AY1 proof.
- **The limit of the named constructions:** the AY1/AY2 gate ball for every subsequential limit of F1 and F2, identified with the limit by BB2 gate items 2–3.
- `K_2' = 966771578474926086618624139557778885954947547760216752246561/72052885697817210754545804931891200000000000000000000000` (about `13417.5275439`; tier `exact_first_order`, the inherited AY1 constant), re-derived by a second code path from the AY1 F14 items with the enumerated pins 82, 72 and 33. At `|tau| = 10^-8`: `|omega(W_{1x2})| <= 966771578474926086618624139557778885954947547760216752246561/720528856978172107545458049318912000000000000000000000000000000000000000` (about `1.34175e-12`), at both signs. The bound carries no sign.

**Evenness in `tau` (AW1 flip lemma, area 2).** With `E = {(p,x): p_y even} u {(p,y): p_z even} u {(p,z): p_x even}`, every plaquette meets `E` in 1 or 3 links (checked on 4800 plaquettes of the window); `F1` and `F2` meet it in 3 links each and the rectangle in all 6. So `U_E W_{1x2} U_E^* = W_{1x2}` (checked on the quaternion fixture), and with `U_E H_N(tau,0) U_E^* = H_N(-tau,0)` (AW1 F09, F10), `omega_{N,-tau}(W_{1x2}) = omega_{N,tau}(W_{1x2})` in every open centered whole-star box (F1) and every on-site cutoff at `kappa = 0`. Both signs converge as whole sequences (BB2 item 1), so the limit is even as well. F2 boxes are not claimed, and evenness gives no remainder bound.

**Formal second-order coefficient (label `formal_second_order_coefficient`).** Under I1.5 with both faces at `-(tau/3) W_f` in delta units, `psi_1 = (1/72) sum_f W_f Omega_0` and `E_1 = 0`. Only the ordered pairs `(F1,F2)` and `(F2,F1)` cover the rectangle evenly, with `E[W_F1 W_F2 W_{1x2}] = E[xyz] = 1/16`, and `W_{1x2} Omega_0` has energy 36. Hence, formally,

`omega(W_{1x2}) = [2 Re<W_{1x2}Omega_0,psi_2> + <psi_1,W_{1x2}psi_1>] tau^2 + ... = (1/31104 + 1/41472) tau^2 + ... = (7/124416) tau^2 + ...`

There is no normalization term because `E[W_{1x2}] = 0`. As a labelled consistency identity only, `7/124416 = (7/216)/24^2`: the graph coefficient of `<z>` under `tau_FG = tau/24` (same two-face algebra and energies; no transfer). **Obstruction:** no certified third-order remainder exists; the only certified size statement is the bound above, which exceeds the formal term by the factor `2.38479e8`. No sign or value of `omega(W_{1x2})` is claimed.

## 6. Item 4: the electric-energy band on `R`

**The observable.** `h_R = 8 sum C_e` over the 48 links of `R` (delta units, zero-selected) is nonnegative and unbounded. `omega(h_R)` is defined as the monotone limit over the spectral projections `Q_L` of `h_R` of `Tr(rho_R h_R Q_L)` (nondecreasing in `L`, with value in `[0, infinity]`).

**Lower endpoint (tier `first_order_distance_from_product`).**
1. *Operator inequality.* The spectrum of `h_R` is `{0} u [6, infinity)` with kernel `P_R`: the smallest nonzero value of `8 sum_e j_e(j_e+1)` is `8 · 3/4 = 6` (I1: free Casimir gap `6 delta`). So `h_R Q_L >= 6(Q_L - P_R)` for `L >= 6`, and letting `L -> infinity`, `omega(h_R) >= 6 Tr(Q_R rho_R)` with `Q_R = I - P_R`.
2. *Fuchs–van de Graaf for the pure reference (proved inline).* For unit vectors, `(1/2)||P_phi - P_Omega||_1 = sqrt(1 - |<Omega,phi>|^2)`. For `rho = sum p_i P_(phi_i)`, convexity of the trace norm and concavity of the square root give `(1/2)||rho_R - P_R||_1 <= sum p_i sqrt(1 - |<Omega,phi_i>|^2) <= sqrt(Tr(Q_R rho_R))`. Exact 2x2 fixtures check equality for a pure state (`16/25 = 16/25`) and strict inequality for a mixed one (`3088/4225` below `3152/4225`); the constant 1 in place of 1/2 is rejected on the pure fixture.
3. *Distance from the product.* For the limit: the AY2 gate item (2) lower end `L = 315493271189404369878663368737136921794795815043212654249128159/720528856978172107545458049318912000000000000000000000000000000000000000` (about `4.37863e-10`). For every finite F1 and F2 box: the same number from the AY1 per-box ball, `||rho_{N,R} - P_R||_1 >= ||rho^(1)_R||_1 - K_2' tau^2 >= sqrt(10)_lo |tau|/72 - K_2' tau^2`, with the AY1 gate constant and the AY2 directed bracket of `sqrt(10)` — a reviewed step of the admitted AY1 proof, not an AY1 or AY2 gate sentence.
4. Hence `omega(h_R) >= 6 (L/2)^2 = (3/2) L^2 = 99536004165791049425300773950650456874015451568973476245606417493434267637549163914243518625682267830963863935112811606729281/346107889158847464132330923015611755407765743694640423831387242496000000000000000000000000000000000000000000000000000000000000000000000000000000` (about `2.87586637818e-19`).

**Upper endpoint (tier `crude_majorant`).** The AQ1 reset HNM-AQ1.1 on `F = R`: the incident anchors are exactly the seven sites `R - S`, each whole star has norm `21 · |tau|/3 = 7|tau|`, so `omega_N(h_R) <= 2 · 7 · 7|tau| = 98|tau| = 49/50000000` at `|tau| = 10^-8`, for every F1 box; for F2 boxes the same budget is the AY1 gate item (1). (The generic `56|tau||F| = 112|tau|` is valid but is not the frozen endpoint.) **Passage to the limit by lower semicontinuity:** for each `L`, `h_R Q_L` is bounded, so `Tr(rho_R h_R Q_L) = lim_k Tr(rho_{N_k,R} h_R Q_L) <= liminf_k omega_{N_k}(h_R) <= 98|tau|`; the supremum over `L` gives `omega(h_R) <= 98|tau|`. An exact fixture shows why only this direction passes: `rho_k = (1-1/k) P_0 + (1/k) P_k` with `h = diag(n)` has energy 1 for every `k` and trace-norm limit `P_0` with energy 0. The lower endpoint is therefore proved at the limit directly.

**The band (both signs; the `-tau` rows are the mirror replay of the same `|tau|` formula).**

| family | lower | upper | lower source | upper source |
|---|---|---|---|---|
| F1 boxes (every `N>=2`, untruncated) | `(3/2) L^2`, about 2.87586637818e-19 | `49/50000000` | AY1 per-box ball (reviewed step) | AQ1.1 |
| F2 boxes (every `N>=2`, untruncated) | same | same | AY1 per-box ball (reviewed step) | AY1 gate item (1) |
| limit of the named constructions | same | same | AY2 gate item (2), BB2 items 2–3 | AQ1.1 and lower semicontinuity |

**Formal second-order value per link (labelled formal).** `<psi_1,(8C_e)psi_1> = n_e/3456` per link (`1/3456` per omitted face through the link), with `n_e` the number of omitted faces containing link `e` (selected faces carry coefficient 0 at the zero triple). From the I1 face classes: 28 links with `n_e = 4` (`1/864` each: x-links with `r=3`, y-links with `s=1`, all z-links), 16 with `n_e = 3` (`1/1152`: x-links with `r <= 2`, y-links with `s=0` and `r` in {0, 3}), and 4 with `n_e = 2` (`1/1728`: y-links with `s=0` and `r` in {1, 2}). The total is `168/3456 = 7/144`, so formally `omega(h_R) = (7/144) tau^2 + ...` (about `4.861e-18` at the cap). **Obstruction to a tight enclosure:** the upper budget is first order and exceeds the formal value by `2.016e11`; the lower end lies below it by the factor 16.9. A tight enclosure needs a second-order upper bound on an unbounded observable (an energy-weighted state estimate), which is not admitted.

## 7. Item 5: the 2+1-dimensional recount

**Declared factorization.** Single-site factors own `(p,x)` and `(p,y)`; the face at base `p` has links `(p,x)`, `(p+e_x,y)`, `(p+e_y,x)`, `(p,y)` and owner set `{p, p+e_x, p+e_y}`; each face is its own interaction term `V_X = -(tau/3) W_f` with `||V_X|| = |tau|/3`.

| constant | 2+1D value (recounted) | 3+1D value (not reused) |
|---|---|---|
| owner set and star | `{p, p+e_x, p+e_y}`; star `{0, e_x, e_y}` (one face per anchor) | `S = {0, e_x, e_y, e_z}`, 21 faces per anchor |
| faces per site (terms whose owner set contains the site) | 3 (incoming stars `u - {0, e_x, e_y}`) | 4 stars, 49 faces |
| per-site sum `J` | `3 · |tau|/3 = |tau|` | `28|tau|` |
| maximal support `p` | 3 | 4 |
| termination order `2p` | 6 | 8 |
| numerators `L_k^num = 2^p (2p)^k (1 + k(p+1)/p)`, `k=0..6` | 8, 112, 1056, 8640, 65664, 476928, 3359232 | `16·8^k(1+5k/4)` |
| `G_p(t)` | `8 e^{6t}(1+8t)`; `G_3'(t) = 8 e^{6t}(14+48t)` | `16 e^{8t}(1+10t)` |

The numerators come from the AM2 counting (two root placements, `2^p` output sets, `(2p)^k` from the commutator expansion and the sums over creations meeting `X`, and `1/|M| <= (p+1)/|I_l|`). The checker reproduces the AM2 `p=4` formula, verifies that `k!` times the Taylor coefficients of `2^p e^{2pt}(1+2(p+1)t)` equal the numerators for `k <= 12` at `p = 3` and `p = 4`, and checks the derivative coefficients. **Termination:** an exact three-qubit creation fixture gives `ad_C^6(V) Omega = -720|111>` and `ad_C^7(V) = 0` (the four-qubit fixture has `ad_C^7(V) != 0`).

**Directed exponential (own enclosure).** `e^{3/32}` is bracketed by the 25-term series with its geometric tail, rounded outward to `10^-40`: `[5491425701539129243251049671283933594049/5000000000000000000000000000000000000000, 10982851403078258486502099342567867188099/10000000000000000000000000000000000000000]` (about `1.0982851403078258486`). With `R = 1/64`: `G_3(R) = 9 e^{3/32}`, about `9.88456626277`, and `G_3'(R) = 118 e^{3/32}`, about `129.597646556` (exact brackets in `results.json`; AM2 normalization `h_x >= Q_x`; the free gap 6 is not used).

**Admissible cap.** The self-map condition `J G_3(R) <= R` gives `|tau| <= 1/(576 e^{3/32})`; the exclusion condition `2 J G_3'(R) < 1` gives `|tau|` below `1/(236 e^{3/32})` (about `3.858e-3`), so the self-map condition binds. Directed rational lower bound: **`|tau| <= 1580747155173/1000000000000000`** (about `1.58074715517e-3`); at this value `J G_3(R) <= 0.015624999999994 <= 1/64` and `2 J G_3'(R) <= 0.40972`. The largest admissible `|tau|` lies in `[1580747155173/10^15, 1580747155174/10^15]`. A labelled variant using the terminating sum over `k <= 6` in place of `G_3` gives `790373577671/500000000000000`; it is not the headline. These constants carry no tier and are `tau`-independent (`J/|tau| = 1`).

**What transfers verbatim (algebraic):** the SU(2) centre grading and Haar moments (AW1 F04); the AM2 creation algebra and its counting for general `p`; the AV2 window-kernel constants `M_0 = 2`, `M_1 = 4s/pi`, `M_2 = 2s^2` (a one-dimensional spectral identity, dimension-independent); trace duality, Fuchs–van de Graaf and the monotone cutoff passage; the Round11 graph algebra. **What needs its own contract:** the finite-volume ground-state and gap theorem in 2+1 dimensions (missing: a 2D finite-volume prescription, the on-site domains of `8(C_(p,x) + C_(p,y))`, and AM2 sections 4–6 re-verified); the AQ chain (AQ1, AQ2, AV1, AW1, AY1/AY2, BB1/BB2); the Euclidean node certificate; and the dictionary, since in 2+1 dimensions `g^2` has mass dimension and the 3+1D coupling dictionary does not apply. **No finite-volume ground-state or gap statement in 2+1 dimensions is claimed; the recounted constants are not a theorem.**

## 8. Item 6: obligations and no-transfer rows

| row | status | missing premise |
|---|---|---|
| area law | not proved, not claimed (`area_law_claimed: false`) | analyticity of the reduced density in a complex `tau`-disc uniformly in `N` (a zero-free region for the complexified normalization) and a family of growing loops; no zero-free region is admitted |
| certified sign of the Z^3 1x2 mean | not proved | a uniform remainder `|omega(W_{1x2}) - (7/124416) tau^2| <= K_4 tau^4` with `K_4 tau^2` below `7/124416` (the third order vanishes by evenness for F1 boxes and the limit; F2 boxes would need a third-order remainder); the admitted `K_2' tau^2` is `2.38479e8` times the formal term |
| tight electric-energy enclosure | not proved | a second-order upper bound on the unbounded `omega(h_R)` (an energy-weighted or relative-form state estimate); the reset budget is first order |
| site-blocked uniform 3+1D regime | not in this packet | its own contract |
| finite-volume theorem in 2+1D | not proved | a 2D finite-volume prescription, the on-site domains and AM2 sections 4–6 re-verified; then the AQ chain, node and dictionary |
| Einstein–QED evidence rounds | no-transfer row | none: they share no equation with this SU(2) chain; recorded, not compared |

Also not claimed: uniqueness of any ground state, any estimate uniform in the lattice spacing, a rate in `N` (BD2 makes no new claim of a rate in `N`; the BB2 limit is used only for its identification), continuum or weak coupling, and scientific priority.

## 9. Error ledger (preregistered terms)

| term | value | reason |
|---|---|---|
| `graph_truncation_zero` | 0 | `psi_mn` in `P_(m+n)` inside `P_6`; polynomial identity; tables identical at D=6 and D=8 |
| `graph_residual_itemized` | per point | five-part AZ2-type ledger at all 14 points (Section 4) |
| `flip_parity_graph` | 0 | exact identities: the flips act by signs, commute with `K` and `C_shared` and preserve Haar; parity coefficient by coefficient |
| `z3_formal_coefficient` | `7/124416` (formal) | no certified third-order remainder; certified size only `K_2' tau^2` |
| `band_lower_trace_duality` | `(3/2) L^2` | `h_R >= 6 Q_R`, Fuchs–van de Graaf, `L` from AY2 (limit) or the AY1 per-box ball (boxes); the `sqrt(10)` bracket width is charged in `L` |
| `band_upper_energy_budget` | `49/50000000` | AQ1 reset `2·7·7|tau|`; F2 through the AY1 gate; limit by lower semicontinuity |
| `cutoff_monotone_passage` | not_applicable | no numeric cost: monotone convergence and lower semicontinuity are exact |
| `dimension_recount` | exp bracket width about `2e-40` | directed series enclosure of `e^{3/32}`; counts exact |
| `arithmetic` | charged | exact Fractions; directed `isqrt`; outward export to `10^-45` |

## 10. Mandatory sentence, gate fields and labels (item 7)

The mandatory sentence template, quoted once:

> On the Round11 two-plaquette graph with independent couplings, the exact low-order coefficients of the face mean, the 1x2 loop and the shared-link Casimir are computed with zero truncation error, the face mean is odd in its own coupling and even in the other, and the 1x2 loop has a certified sign at every grid point; in the zero-selected SU(2) family the 1x2 Wilson mean vanishes at first order and is even in tau, with only a formal second-order coefficient, the electric energy on the cover lies in a certified two-sided band for every box and for the limit of the named constructions, and the 2+1-dimensional AM2 constants are recounted; these are statements about named models and a finite graph, not an area law, not a certified sign of the 1x2 mean, not uniqueness of any ground state, and not a statement uniform in the lattice spacing a.

The evenness clause holds for F1 boxes and the limit (F2 boxes are not claimed), and the band clause's "every box" means every finite box of F1 and F2 at every `N >= 2`.

**Gate fields exported:** `model_is_finite_graph: true`, `transfers_to_aq: false`, `graph_sign_certified: true`, `z3_1x2_formal_only: true`, `electric_band_claimed: true`, `electric_band_scope: "omega(h_R) for every finite box of F1 and F2 (untruncated at fixed N) and the limit of the named constructions, both signs"`, `area_law_claimed: false`, `uniqueness_of_ground_state_claimed: false`, `rate_in_a_claimed: false`, `continuum_claim: false`, `weak_coupling_claim: false`, `scientific_priority_verified: false`. Additional flags, all false: `rate_in_N_claimed`, `z3_1x2_sign_claimed`, `tight_electric_enclosure_claimed`, `finite_volume_theorem_2p1_claimed`, `aq_statement_2p1_claimed`, `fg_coefficients_fitted`.

**Tiers:** band lower end `first_order_distance_from_product` (AY2 for the limit, AY1 per box); band upper end `crude_majorant` (AQ1 reset); the `W_{1x2}` bound `exact_first_order` (inherited `K_2'`); the graph coefficients and enclosures, the formal Z^3 coefficient and the 2+1D constants carry no tier and name their source.

## 11. Exclusions, limitations and contract wording findings

**Contract exclusions (verbatim):** a certified value or sign of the Z^3 1x2 Wilson mean; no area law and no string-tension statement; a tight enclosure of the electric energy; an AQ chain, node or dictionary in 2+1 dimensions; uniqueness of any ground state; any estimate uniform in the lattice spacing a; continuum or weak coupling; scientific priority. **Preregistration exclusions:** a certified 1x2 value or sign in Z^3; an area law; a tight electric enclosure; 2+1D AQ statements; continuum or weak coupling; scientific priority.

**Limitations.**
1. The graph results hold for the Round11 two-square patch only, at D in {6, 8} and the declared grid; they are static means with no dynamics or mass-gap reading, and nothing transfers to the AQ construction (`transfers_to_aq: false`).
2. The Z^3 results hold for the zero-selected family at `|tau| <= 10^-8` only, on the fixed cover `R` and at fixed spacing; the bounds hold uniformly in `N` at fixed spacing and not uniformly in the lattice spacing. Evenness is not claimed for F2 boxes.
3. The band is two-sided but loose (ratio about `3.4e12`); the formal values of items 3–4 are labelled formal and carry no certified remainder.
4. Inherited without re-proof: the Round11 reduction, spectrum and Theorem F; the AZ2 certificate (copied, not re-derived); AM2, AV1 F22, AQ1.1, AW1 F04/F09/F10, AY1 F11–F14 and the AY1/AY2/BB2 gate statements. Kato, Peter–Weyl, Weyl, Temple, Eckart and Davis–Kahan are cited.
5. Correlation: the contract, the selection note and the admitted gates state the mechanisms; the independence of the skeptic's replay is limited to its route and code.

**Contract wording findings (non-blocking; each verified in `contract_wording_defects_recorded`).**
- **W1.** `preregistration.model_id` and `model_is_finite_graph` name only the graph model; items 3–5 concern the Z^3 family and the declared 2+1D model. Every value here carries its own model label.
- **W2.** `selected_triple_alpha_units` (the zero triple) belongs to the Z^3 family; the graph has no selected faces.
- **W3.** Item 6's "a uniform fourth-order remainder" presupposes evenness, admitted for F1 boxes and the limit only; F2 boxes would need a third-order remainder (recorded so in Section 8).
- **W4.** "three faces per site" is read as the number of faces whose owner set contains the site (each site anchors one face and lies in three owner sets); this is what the per-site sum uses.
- **W5.** "dimension_constants: tau-independent" holds for `G_3(R)`, `G_3'(R)`, the counts and the cap; the per-site sum is `J = |tau|`, and `J/|tau| = 1` is what is `tau`-independent.
- **W6.** The AY1 gate and report call `K_2'` a tier-(ii) constant; the BD2 tier name `exact_first_order` is used for the same constant.
- **W7.** The Round11 solver API restricts `lambda >= 0`; negative couplings and grid points lie outside it; the certificates and the series need no sign.

**Methodological lenses (modern use of the snapshotted skills).** Newton, analysis before synthesis: which faces can cover the rectangle evenly, and which links carry which spins, was settled before any bound was written. Tesla, complete accounting: every channel is charged, including both faces, the shared link, the product channel, the interference, the incoming anchors of the reset and the arithmetic. No historical figure endorses anything here, and no historical or occult material supplies a premise.

## 12. Proposed verdict

**`accepted_within_scope`** (forward half of a single+skeptic loop). Items 1–5 are proved or computed exactly as stated; the item-2 enclosures meet the frozen relative width at D=8 and exclude 0 at every grid point at both cutoffs; the band has exact endpoints at both signs for every F1 and F2 box and for the limit from the frozen premises; the `W_{1x2}` bound holds for every box and the limit; item 6 lists every obligation with its missing premise, including the finite-volume theorem in 2+1 dimensions. Sub-labels: `sign_certified_finite_graph` (the graph only), `transfer_to_named_model`, `obstruction_recorded`, `static_not_dynamic`. The acceptance rule is executed in `check.py` (`insufficient_verdict_retained`); a missed width target or a band for finite boxes only would have been reported as `limited` at the unchanged grid, cutoffs and target.

**Checker.** `check.py --output <absolute-fresh-dir>` uses only the standard library, verifies the contract sha256 before evaluation, pins the gate and premise-code sha256s, records its own sha256 first, and writes `results.json` and `source-manifest.json`. It runs 41 exact checks; all 21 contract controls reject damaging mutations (101 rejections in the control checks, 107 in total); the `-B` and `-B -O` outputs are byte-identical. Runtime is about 30 s per replay.

**Private source-edit audit (scratch, not evidence).** On copies of the closure in `/tmp/claude-0/bd2-forward-private/mutaudit/`, each of these edits of `check.py` aborts with an `AdmissionError` at the named check: the second face uncoupled in the series (`rs2_tables_exact`); `||z||` set to 1/2 (`round11_conventions_bound`); the rectangle energy 36 replaced by the face energy 24 (`formal_coefficient_labelled`); the free Casimir gap 6 replaced by 8 (`unbounded_observable_handled`); four faces per site in 2+1D (`dimension_recount`); the flip set keyed wrongly on z-links (`z3_rectangle_geometry`); the reset charged at two anchors (`unbounded_observable_handled`); the upper `sqrt(10)` bracket used for the lower end (`unbounded_observable_handled`).

## 13. Item and control map

| entry | where | what executes it |
|---|---|---|
| item 1 | §2, §3 | `rs2_tables_exact`, `exact_rs_zero_truncation`, `independent_coupling_flip`, `gauge_invariance_and_one_link_flips`, `round11_conventions_bound`, `graph_couplings_named` |
| item 2 | §4 | `z_certificates_complete`, `enclosure_itemized_residual`, `target_relative_width_D8`, `shell_sectors_orthogonal`, `az2_algebra_copied_verbatim` |
| item 3 | §5 | `z3_rectangle_geometry`, `z3_first_order_zero`, `z3_bound_K2prime`, `evenness_from_flip`, `formal_coefficient_labelled` |
| item 4 | §6 | `unbounded_observable_handled`, `band_both_signs`, `scaling_brackets_per_constant` |
| item 5 | §7 | `dimension_recount`, `dimension_transfer_rows` |
| item 6 | §8 | `obligations_and_no_transfer_rows`, `no_area_law_claim`, `no_transfer_to_eqed` |
| item 7 | §10, §12 | `negation_aware_phrase_scan` (template once), `placeholder_span_rejected`, `coherent_evidence_tampering` and the gate fields in the packet; freeze and byte-identical replays by `research/round33/tools/freeze.py` |
| `coherent_evidence_tampering` | §12 | 13 coherent rehash tamperings rejected by recomputation (a control Boolean, a `<z>` end, a coefficient, the bound, the formal label, a band end, the 2+1D support, a snapshot, the contract hash, a gate field, the verdict, the sentence, an obligation row) |
| `exact_arithmetic_admission` | §4, §9 | rejects float, bool, NaN, a zero denominator and the decimal proposal |
| `no_priority_or_continuum_claim` | §10 | flags false; rejects continuum, priority, weak coupling, rate in a and uniqueness set true |
| `changed_model_relabelled` | §1 | rejects a graph value under the Z^3 label, a 3+1D constant under 2+1D, an F1 value under F2, a finite-box value under the limit, and equal-coupling or one-face values under the independent label |
| `insufficient_verdict_retained` | §12 | acceptance rule; rejects a missed width target, a finite-box-only band or incomplete 2+1D constants relabelled accepted, and a failed graph algebra relabelled limited |
| `placeholder_span_rejected` | §10 | report, exported texts, every contract string and every results string scanned; rejects whitespace, bar and e.g. spans |
| `negation_aware_phrase_scan` | §10 | round list plus the contract list with the template removed as one literal; rejects affirmative hits, an altered template and a doubled template |
| `parameters_declare_metric_weights_window` | §1 | metric, weights, window and clock declared; rejects an absent window, a bare not-applicable and a declared `N_0` |
| `tier_mixing_rejected` | §10 | rejects swapped band tiers, a tier on a graph coefficient or a 2+1D constant, a Lieb-Robinson tier, a hypothesis source and a plan route label |
| `graph_couplings_named` | §1 | every term with its coefficient; rejects the one-face and equal-coupling models, rho=2, the independent rotor, the AQ id, a transfer and an imported free reference |
| `exact_rs_zero_truncation` | §2 | rejects a coefficient that differs between cutoffs, a fitted provenance and a vector outside `P_(m+n)` |
| `independent_coupling_flip` | §3 | rejects a two-variable parity from the vM flip, a check at `l1=l2` only and flips from the wrong face |
| `enclosure_itemized_residual` | §4 | five parts at all 14 points; rejects an enclosure without ledger, a missing joint channel, a missing vM row, a reasonless gauge entry and missing arithmetic |
| `formal_coefficient_labelled` | §5 | rejects the formal coefficient as a certified value, a sign, the bound as its enclosure, a third-order remainder and a rectangle outside `R` |
| `evenness_from_flip` | §5 | rejects evenness for F2 boxes, a remainder from evenness, the area-1 loop and `kappa != 0` |
| `unbounded_observable_handled` | §6 | rejects a bounded constant applied to `h_R`, the AY2 distance for a finite box, the 112 and 28 budgets, passage by continuity and Fuchs–van de Graaf without the 1/2 |
| `band_both_signs` | §6 | rejects a missing `-tau` F2 row, a finite-box-only band, a float endpoint and a non-mirror `-tau` row |
| `dimension_recount` | §7 | rejects `p=4`, `J=28|tau|`, termination order 8, `G(R) <= 148/7`, the 3+1D dictionary and a tier on a 2+1D constant |
| `no_area_law_claim` | §8 | rejects `area_law_claimed: true` and a string-tension statement drawn from the 1x2 loop |
| `no_transfer_to_eqed` | §8 | rejects a comparison and a claimed shared equation |
| `rate_range_stated` | §8 | no new rate in `N`; rejects a rate without its range and `rate_in_N_claimed: true` |

## 14. Reproduction

```bash
python3 -B research/round33/forward/bd2/check.py --output /absolute/fresh/dir
python3 -B -O research/round33/forward/bd2/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round33/tools/phrase_scan.py research/round33/contracts/bd2.json research/round33/forward/bd2/report.md
python3 -B research/round33/tools/freeze.py verify research/round33/forward/bd2
```
