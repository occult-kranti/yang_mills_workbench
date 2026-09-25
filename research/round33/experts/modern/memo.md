# Modern-methods memo for Round33, deliberation loop 1

**Status:** advisory (`round33_loop1_advisory`). Nothing in this memo is a frozen contract, an executed loop, an admitted theorem or a certificate. Human project author: **Hruday N M (BUNZEEY)**. "Penrose" and "Feynman" name documented methodological lenses. The Penrose lens means representation, analytic-structure and inner-product bookkeeping. The Feynman lens means computing the observable in a named model, building the simulator and looking for the damaging example. This lens is a model agent with ancestry shared with every other agent in the round. No historical person took part in or endorses this memo, no quotation is attributed to anyone, and this review is not external human peer review. The small computations quoted below were run in the session scratchpad, outside the checkout. Their numbers are **previews**, not enclosures, and none is evidence for any gate.

**Checkpoint read:** `research/round33/advisor/brief.md`; `research/round32/HANDOFF.md`; `advisor/roadmap.json`; my Round32 `memo.md`, `update-5.md`, `sota-closing.md`, `sota-table.md` and `sources.json`; the Round32 Jung `update-5.md` §3 (ten rules). Mathematical sources:
- the AM2 forward report (creation algebra, (HNM-AM2.4)–(AM2.11));
- the AQ1 and AQ2 forward reports (Nachtergaele–Sims placement, `F(r)=(1+r)^-4`, `C<=224`, `||Phi||_F<=2268|tau|`);
- the AV1 forward report (product ordering (F06)–(F12), cutoff-vector removal (F20)–(F24));
- the AY1 forward report (F1/F2 definitions, the F2 check of AM2's hypotheses H1–H5, the first-order density, `K_2'`);
- the AY2 forward report §§1.4–3 (the six-obligation table and the falsifying scenario);
- the AW1 amplitude lemma (F14).

`AGENTS.md` was skimmed for lens and source rules. The AY1/AY2 gates were read through the AY1/AY2 reports and the handoff; their `bindings` blocks were not opened.

---

## 1. Reading Round32 through the two lenses

**Feynman reading.** Round32 computed, at one fixed lattice model, the numbers its predecessors had only bounded. These are:
- the local state tier `D ≈ 1.36e-8`;
- the static mean `+tau/144`, sign-certified near `6.9e-11`;
- `K_2^+ ≈ 3354.8` and `K_2' ≈ 13418`;
- the Euclidean node radius `≈ 1.83e-7`;
- exact finite-graph coefficients `1/6`, `0` and `-187/33696`.

The decisive move each time was to count orders by a selection rule before budgeting an error. Center grading decided that first-order centered terms do not exist. The shared-link flip decided that the graph's second-order coefficient is exactly zero. Only then did the remainder arithmetic matter. Two of this lens's expectations were wrong and are on record: "`K_2'` strictly smaller than `K_2^+`", and the assistant-4 bracket claim. Both were wrong for the same reason: I estimated a quantity instead of computing it. What Round32 did **not** compute is how the finite-box state moves when the box grows. Every admitted bound is a one-state ball that holds in every box, so it carries no information about `N`. The natural next computation is the one a perturbation-series user would do first: at order `n` in the coupling, how far from `R` can the series reach? If a boundary at distance `N` cannot appear before order `N`, the box dependence is `O(tau^N)`, provided the series converges uniformly in the box. Section 2 turns that remark into constants.

**Penrose reading.** Structurally, Round32 organized everything around three representations:
- the `Z_2` center of SU(2) (the grading, and the link-flip set `E` with `U_E H(tau,kappa) U_E^* = H(-tau,-kappa)`);
- the vacuum/cross/excited block decomposition of the reduced density (AV1 F11);
- the dictionary geometry (`alpha*lambda*a^2 = 1`, and the lattice-unit floor `a*Delta >= g^2/32`), which shows the admitted regime is a closed strip in `g`, far from any continuum.

The missing structure is a *map between two states*. Round32 has only convex constraints that each state satisfies separately; AY2's falsifying pair is exactly what one-state balls cannot exclude. The natural bridge is analytic: treat the coupling as a complex parameter `s`. The finite-box R-marginal is then a holomorphic function on a disc. Its Taylor coefficients are local, and its size on the disc is uniform in the box. Then Cauchy's estimate converts locality into an explicit exponential rate. This is the classical route of cluster expansions (Kotecký–Preiss; Yarotsky 2005 for weak perturbations of non-interacting gapped systems), and the AM2 creation algebra already supplies most of its inputs.

---

## 2. Feasibility study

### 2.1 What AM2 proves and what it does not

AM2 proves the following for real `|s|<=1` in every finite box and every onsite cutoff. The fixed point `c = s * sum_{k<=8} L_k(c,...,c)/k!` exists uniquely in the anchored ball `||c||_a = max_u sum_{I ∋ u}||c_I|| <= R = 1/64`, with:
- the majorant `||L_k(c_1..c_k)||_a <= J * 16 * 8^k (1+5k/4) * prod ||c_j||_a`, where `G(t) = 16e^{8t}(1+10t)`, `G(R) < 148/7` and `G'(R) < 352`;
- `J <= 28|tau| <= J_0 = 7/25000000`.

The contraction holds in a **sup-type norm with no spatial weight**. It says nothing about how `c_M` depends on the box. The advisor's diagnosis is correct: *the fixed point is global*, and a boundary change could in principle move every coefficient by an amount of order `J G(R)` at once. AV1 then writes the R-marginal through the product ordering. That formula contains the normalized **outside vector** `phi_out/||phi_out||` (AV1 F07–F11; the normalization trap). So even exact knowledge of the coefficients near `R` does not fix `rho_R`. There are two layers of work:
- (a) locality of the coefficients;
- (b) locality of the normalized state built from them.

### 2.2 How `c_M` depends on `Lambda_N`: tree locality and the reach count

Expand the fixed point in powers of `s`: `c(s) = sum_{n>=1} s^n c^(n)`. The recursion is `c^(n) = sum_k (1/k!) sum_{n_1+..+n_k = n-1} L_k(c^(n_1),...,c^(n_k))`. Each `L_k` uses one interaction support `X` and requires every input creation to meet `X`. Its output `M` satisfies `N\X ⊂ M ⊂ N ∪ X`, where `N = ∪ I_j` (AM2 §2). By induction, `c^(n)_M` is a finite sum over **trees of `n` interaction supports** that are overlap-connected and whose union contains `M`. `H_M^{-1}`, `P_M` and the onsite cutoffs are local and do not depend on the box.

*Reach count (new, elementary).* A star `b+S`, `S={0,e_x,e_y,e_z}`, has ℓ∞-diameter 1, and consecutive stars in a tree overlap. So an `n`-support tree containing `u` lies within ℓ∞-distance `n` of `u`. Let `u ∈ R = {0, e_z}`:
- **F1, `N < N'`.** A star retained in `Lambda_{N'}` but not in `Lambda_N` contains a site `y` with `|y|_∞ >= N+1`, so `|y-u|_∞ >= N`. Hence `c^{(n),N}_M = c^{(n),N'}_M` for every `M ∋ u` and every `n <= N-1`.
- **F1 against F2 on the same `Lambda_N`.** An extra F2 face is anchored at `b` with `b_i = N`, and every owner site of that face keeps `|y_i| = N`. Agreement holds for `n <= N-2`.
- **F2, `N < N'`.** F2 boxes are nested (`F2(Lambda_N) ⊂ F2(Lambda_{N'})`). Agreement holds for `n <= N-1`. Taylor coefficients are multilinear in the faces, so the grouping into anchors does not matter.

### 2.3 Which per-link factor sets the rate

There are three candidate "per chain step" constants. They must not be confused. Values are at `J_0`, with the general-`tau` form alongside.

| constant | value | role |
|---|---|---|
| `J G(R)` | `< 37/6250000 ≈ 5.92e-6` (`592|tau|`) | absolute size of the coefficients (tier-i `t`) |
| `J G(R)/R` | `< 148/390625 ≈ 3.7888e-4` (`37888|tau|`) | **decay ratio per tree step** (ball condition) |
| `J G'(R)` | `< 77/781250 ≈ 9.86e-5` (`9856|tau|`) | Lipschitz constant of the fixed-point map (AM2 §3) |
| `2J G'(R)` | `< 77/390625 ≈ 1.97e-4` | excited-sector exclusion only (AM2 §4, shifted inverse) |

The decay rate is set by the **ball condition**, not by a Lipschitz constant. "`J G(R) < 1/64`" is the absolute smallness statement, not a rate (dissent 1).

*Counting chains.* A star overlaps exactly 12 others (`|S-S| = 13`), and 4 stars contain a site. A lattice-animal bound gives at most `4 (12e)^{k-1} ≈ 4·32.6^{k-1}` connected star sets of size `k` through a site. A naive chain sum `sum_k (32.6 × 3.79e-4)^k = sum_k 0.0124^k` converges with a large margin. That count is only illustrative. AM2's majorant `16·8^k(1+5k/4)` already contains the branching: the output-set count `2^p`, the `p` sites of `X`, and the four stars per site inside `J`. The clean route therefore does not count animals separately. It uses the majorant through analyticity or through a weight.

### 2.4 Coefficient decay: two equivalent routes with one constant

**(A) Complex coupling and Cauchy.** The `L_k` are complex-multilinear, and AM2's estimates use only norms. So for complex `|s| <= S` with `S J G(R) <= R`, the map `c ↦ s·sum L_k/k!` sends the anchored `R`-ball into itself. Its Lipschitz constant is `S J G'(R) <= 352·(7/148)·R = 77/296 ≈ 0.260`, independent of `tau`, when `S = R/(J_0·148/7)`. The iterates are polynomials in `s` and converge uniformly on the closed disc, so `c(s)` is holomorphic there with `||c(s)||_a <= 1/64`. The largest admissible radius is

`S_* = R/(J_0 G(R)) = 390625/148 ≈ 2639.36` at the cap, and `S_*(tau) = 1/(37888|tau|)` in general.

(This also shows the frozen cap `10^-8` has a factor of about 2600 of slack in the contraction itself; AM2's inequalities hold up to `|tau| ≈ 2.6e-5`.) Cauchy's estimate gives `||c^(n)||_a <= R S_*^{-n} = (1/64)(37888|tau|)^n`; at `n=1` this is exactly tier (i), `592|tau|`, which is a consistency check. Combining with §2.2, for `u ∈ R` and F1, `N' > N >= 2`:

`sum_{M ∋ u} ||c^{N'}_M - c^{N}_M|| <= 2R sum_{n>=N} S_*^{-n} = (1/32)(37888|tau|)^N / (1 - 37888|tau|)`.

With F2 involved, the exponent is `N-1`. Previews at the cap:

| `N` | bound (F1, exponent `N`) |
|---|---|
| 2 | `4.49e-9` |
| 3 | `1.70e-12` |
| 5 | `2.44e-19` |

**(W) A weighted anchored norm.** For a support `M`, define `sigma(M)` as the least number of star translates whose union is overlap-connected and contains `M` (a Steiner star count). Put `||c||_{sigma,w} = max_u sum_{M ∋ u} w^{sigma(M)} ||c_M||`.

*Lemma W (new; the check is short).*
- Since `M ⊂ X ∪ ∪I_j` and every `I_j` meets `X`, `sigma(M) <= 1 + sum_j sigma(I_j)`.
- Every counting step of AM2 survives multiplication by the weights: the `2^p` output sets, `sum_{I∩X≠∅} <= p||c||`, `1/|M| <= (p+1)/|I_l|`, and summing `X` meeting `I_l` at cost `J|I_l|`.
- Hence `||L_k(c_1..c_k)||_{sigma,w} <= w J L_k^num prod ||c_j||_{sigma,w}` for `w >= 1`, with **one** factor `w` per interaction.
- For `w <= S_*`, the ball `||c||_{sigma,w} <= 1/64` is invariant and the map is contractive (Lipschitz `w J G'(R) <= 77/296`).
- Because `||c||_a <= ||c||_{sigma,w}`, AM2's uniqueness identifies this fixed point with AM2's.
- Consequently `sum_{M ∋ u, sigma(M) >= m} ||c_M|| <= (1/64)(37888|tau|)^m`. The same constant appears as in route (A), as it must, because `sigma(M) <= n` at order `n`.

**Why the other weights fail.** This is the advisor's obstacle, re-checked.
- *Cardinality weights* `w^{|M|}` pick up `w^{|X|} = w^4` per step, so they allow only `w <= 2639^{1/4} ≈ 7.17`. Worse, they do not control extent: `M ⊇ N\X` lets the excited set lose sites inside each `X`, so a two-site support can span an arbitrary distance after many steps.
- *Weights by distance to `R`*, `e^{mu·dist(M,R)}`, are the wrong object. The bulk fixed point is translation covariant, with coefficients of size about `t` at every distance, so that norm diverges as `N → ∞`. Distance weights belong on the **difference** `c^{N'} - c^{N}`, measured from the boundary. That is what (A) and (W) deliver.

### 2.5 From coefficients to the R-marginal: the normalization obstacle and a polymer gas

The AV1 formula `rho_R = [n^2 P_R + |Omega_R><xi| + h.c. + sigma]/(n^2+d^2)` depends on the outside state through expectations such as `<phi_out|(...)|phi_out>/n^2` on the straddle region. Using AV1's decomposition recursively (shell by shell) multiplies factors of about `|R_k|·t`. Since `|R_k|` grows like `k^2` or `k^3`, the product behaves like `t^k (k!)^3`: astronomically small up to `k` of about `10^2`–`10^3`, but not a convergence proof. A cluster expansion is needed. The creation-product vector has an exact **hard-core polymer representation**:

- `psi(s) = sum_F (-1)^{|F|} ⊗_{I∈F} c_I(s) ⊗ Omega_rest`, summed over families `F` of pairwise disjoint supports.
- `Z(s) = <psi(s̄), psi(s)>`. The bra `<psi(s̄)|` is holomorphic in `s`, so `Z(s) = sum over compatible (site-disjoint) collections of polymers gamma = (F, F')`. Each polymer is a pair of families with the same union `X_gamma` that is overlap-connected; the excited sets must agree site by site.
- The polymer weight is `w_s(gamma) = (-1)^{|F|+|F'|} < ⊗_F c_I(s̄), ⊗_{F'} c_I(s) >`, with `|w_s(gamma)| <= prod_{I ∈ F ⊔ F'} ||c_I||`. Every polymer carries at least two creations, so it is `O(t^2)`.
- The numerator `<psi(s̄), (A⊗1) psi(s)>` has the same form, with the polymers meeting `R` glued into one `R`-polymer. This is exactly the α-modified partition function of the standard treatment (Kotecký's encyclopedia article, eqs. (42)–(48), read this loop).

*Kotecký–Preiss check (candidate constants).* Take the KP condition `sup_x sum_{gamma ∋ x} |w(gamma)| e^{a|X_gamma|} <= a`. Put `u_I = 2||c_I|| e^{(a/2)|I|}`; the 2 covers the two families, and `|X| = (1/2) sum_{F⊔F'}|I|`. The rooted-tree majorant `F_x <= sum_{I ∋ x} u_I e^{|I| F}`, together with `|I| <= 4 sigma(I)`, gives `F <= 2||c||_{sigma,w}` with `w = e^{2a+4F}`. With `a = 1/10` and `F <= 1/32`, `w = e^{0.325} < 3/2`. KP then holds with a large margin (`1/32 <= 1/10`), provided `||c(s)||_{sigma,3/2} <= 1/64`. By Lemma W at complex `s`, that holds for `|s| <= S'' = (2/3) S_*`. The ratios `Z(Lambda\X)/Z(Lambda)` are bounded by `e^{a|X|}`. Together with the `R`-polymer sum, this gives a candidate uniform bound `||rho_R(s)||_1 <= K` with `K ≈ e^{2a}(1+2F)^2 ≈ 1.4`. **I pre-register `K <= 2`.**

*Cauchy in `s` for the state.* `rho_R(s) = Tr_out |psi(s)><psi(s̄)| / Z(s)` is holomorphic on `|s| < S''` and bounded by `K`. It equals the physical R-marginal at `s = 1`, after cutoff removal as in AV1 F20–F23. Its Taylor coefficients are sums over clusters connected to `R`, with total tree order `n`, so the reach count of §2.2 applies unchanged. Hence, **candidate (route A)**:

- `||rho^{F1,N}_R - rho^{F1,N'}_R||_1 <= 2K q^N/(1-q)`;
- comparisons involving F2 use `q^{N-1}`;
- `q = 1/S'' = (3/2)·37888|tau| = 56832|tau|`, which is `222/390625 ≈ 5.68e-4` at the cap.

With `K = 2`, the bound `4 q^{N-1}/(1-q)` takes these preview values:

| `N` | bound | comparison |
|---|---|---|
| 3 | `1.29e-6` | weaker than the admitted `2D ≈ 2.72e-8`; keep `min(2D, ·)` |
| 4 | `7.3e-10` | |
| 5 | `4.2e-13` | below `2K_2' tau^2 ≈ 2.68e-12` |
| 6 | `2.4e-16` | |

Consequences, if proved:
- both whole sequences converge;
- F1 and F2 have a **common limit** `rho^∞_R`, with `||rho^{Fi,N}_R - rho^∞_R||_1 <= 2K q^{N-1}/(1-q)`;
- every subsequential limit of either family equals it on `R`. The same holds on every finite region `F`, with `K_F` about `e^{a|F|}` and the reach measured from `F`.

This settles the **literal** roadmap goal 1 ("any two subsequential limits of the named families agree on R") and AY2 obligations O2 and O4. Box-shape independence follows as well. The limit sees only the inradius around `R`, and the model is coarse-translation covariant. So `omega_∞ ∘ T_v = omega_∞` for coarse translations, which settles O3.

It does **not** give uniqueness among all infinite-volume ground states (O1 in its strong form). It says nothing uniform in the spacing, and `q ∝ |tau|` is a rate in `N` only.

### 2.6 A second, independent route (gap, Lieb–Robinson, susceptibility)

Interpolate `H(theta) = H^{F1}_N + theta·V_∂`, where `V_∂` is the F2 extra faces (or, for the Cauchy step, the stars of `Lambda_{N+1}` not in `Lambda_N` together with bare onsite terms on the new shell). Every `H(theta)` satisfies AM2's H1–H5 with `J <= 28|tau|`, so the gap `>= 1/2` is uniform in `theta` and `N`. Hellmann–Feynman for the nondegenerate ground state gives

`d/dtheta omega_theta(A) = -2 Re <A (H-E)^{-1} Q V_∂>`, with `(H-E)^{-1}Q = ∫_0^∞ e^{-b(H-E)} Q db`.

This is an imaginary-time connected correlation.

Nachtergaele–Sims 2006, Theorem 2 (read this loop), gives `|<Omega, A tau_{ib}(B) Omega>| <= c(A,B) e^{-mu d(1 + gamma^2 b^2/(4 mu^2 d^2))}` for `0 <= gamma b <= 2 mu d`, with `mu = gamma lambda/(4||Phi||_lambda + gamma)` and `c = ||A|| ||B||(1 + 2|Y|/pi + (pi mu d)^{-1/2})`. Beyond that window the bound is `e^{-gamma b}`. Substitute the F-norm analogue `||Phi||_lambda → C_F ||Phi||_{F_lambda} = 224·2268 e^{2lambda}|tau|`, with `F_lambda(r) = e^{-lambda r}(1+r)^{-4}` and `C_{F_lambda} <= 224` by the triangle inequality. With `gamma = 1/2`, the best rate at the cap is `mu_B ≈ 0.841` (at `lambda ≈ 1.34`), about `0.43^d` per coarse ℓ1 unit. Summing over the `28N(5N+1)` extra faces gives a **candidate** `||rho^{F1,N}_R - rho^{F2,N}_R||_1 <= C_B |tau| N^{5/2} e^{-mu_B(N-1)}`, with `C_B` of order `10^2`–`10^3` (to be derived). It drops below `2K_2' tau^2` only near `N ≈ 30`.

It is much weaker than route A, but its premises are independent: only the admitted gap and Lieb–Robinson locality, with no polymer gas. **Obstacle:** NS06 assumes finite-dimensional sites (its norm carries `N^{2|X|}`). The imaginary-time step must be re-done with unbounded commuting `h_x` in the interaction picture (NS14; Nachtergaele–Ogata–Sims 2006). De Roeck–Schütz (arXiv:1501.04571) give exponential, not merely subexponential, locality of gapped perturbations, and their 1512.07612 treats non-self-adjoint perturbations of non-interacting spins. Both are candidate tools for tightening this route (abstract depth only).

### 2.7 Ledger: proved versus new

| ingredient | status |
|---|---|
| multilinear majorant, anchored contraction at real `s`, termination order 8 | proved (AM2 §§2–3) |
| gap `>= 1/2`, cutoff removal for eigenvalues | proved (AM2 §§4, 6) |
| AM2 hypotheses for F2; the interpolating `H(theta)` | proved for F2 (AY1 §3.1); for `H(theta)` a one-line re-check of H1–H5 (new, trivial) |
| product-ordering density; cutoff-vector removal | proved (AV1 F06–F12, F20–F23) |
| complex-`s` contraction and holomorphy of `c(s)` | **new, easy** (norm-only estimates) |
| Steiner-star subadditivity and Lemma W | **new, short** |
| tree locality and the reach count `n_0 = N` or `N-1` | **new, elementary** (exact geometry must be checked for both families) |
| polymer representation of `Z(s)` and numerator; KP with evaluated `a`, `w`, `F` | **new, standard method** (main risk) |
| uniform `K` for the continued `rho_R(s)` | **new** (main risk) |
| assembly: Cauchy estimate, passage to limits and every finite region | new, routine |
| route B: imaginary-time clustering with unbounded onsite terms | **new** (risk: unbounded-site adaptation) |

**Verdict (boundary decay): feasible.** The coefficient part is nearly immediate from AM2. The state part is a standard cluster expansion with a large margin at the cap. The retained failure mode: if KP cannot be closed with evaluated constants, the result is "coefficient decay without state convergence" (`limited`).

### 2.8 Dynamics: Duhamel with the AQ1 constants

Work in normalized time `u` (AQ1: `u = delta t/hbar`, `delta = alpha/8`), so that `theta = alpha t/hbar = 8u`. Take `A ∈ B(H_R)` with `||A|| <= 1`. `H^{F2}_N - H^{F1}_N = sum_{f ∈ E_N} (-tau/3) W_f` over the `28N(5N+1)` extra faces (AY2). Each owner set `M_f` has at most 3 sites, all at ℓ1 distance `>= N-1` from both sites of `R`. Duhamel together with the F-norm Lieb–Robinson bound for F1 (`||[tau_r(A),B]|| <= (2||A|| ||B||/C)(e^{2||Phi||_F C|r|} - 1) sum_{x∈X,y∈Y} F(d(x,y))`, with `C = 224` and `||Phi||_F <= 2268|tau|`) gives:

`||tau^{F2,N}_u(A) - tau^{F1,N}_u(A)|| <= (|tau|/336)·[(e^{kappa|u|} - 1 - kappa|u|)/kappa]·sum_{f∈E_N} sum_{x∈R, y∈M_f} F(d(x,y))`,

where `kappa = 2·224·2268|tau| = 1016064|tau|`. Using `F(d) <= N^{-4}` and at most 6 site pairs per face, the sum is at most `168(5N+1)/N^3`. With `e^x - 1 - x <= (x^2/2)e^x`, **candidate (D1)**:

`||tau^{F2,N}_u(A) - tau^{F1,N}_u(A)|| <= 254016 tau^2 u^2 e^{1016064|tau||u|} (5N+1)/N^3`

Equivalently, in the common clock: `3969 tau^2 theta^2 e^{127008|tau||theta|} (5N+1)/N^3`.

Previews at the cap, for `|theta| <= 1`:

| `N` | bound |
|---|---|
| 2 | `5.5e-13` |
| 10 | `2.0e-14` |

The decay is `O(N^-2)`, polynomial, because `F` is polynomial. With `F_lambda`, **candidate (D2)** is: multiply by `e^{2lambda} e^{-lambda(N-1)}` and replace `kappa` by `kappa e^{2lambda}`. This is exponential in `N` on compact windows. The interactions are finite range, so `F_lambda` is admissible.

Consequences:
- **F2 dynamics.** It exists as the norm limit of the F2 box evolutions and **equals** AQ1's `T_theta`. Norm convergence along the whole F1 sequence is the NS theorem for any exhausting sequence. This closes AY2 O5 and the dynamics part of O6.
- **Cauchy in `N` for one family.** It is only `O(1/N)` with the polynomial `F`, because the new stars fill the whole exterior shell (dissent 5), and `O(e^{-lambda N})` with `F_lambda`.
- **Correlation functions of the limit.** If §2.5 succeeds, `c^{Fi,N}_A(theta) → c^∞_A(theta) = omega_∞(A* T_theta(A)) - |omega_∞(A)|^2`. The proof is: approximate `T_theta(A)` on a ball `B_r(R)` (Lieb–Robinson tail), use `||rho^N_{B_r} - rho^∞_{B_r}||_1 <= 2K_{B_r} q^{N-r-1}/(1-q)`, and choose `r ≈ N/2`. The rate is exponential in `N` with `F_lambda`, polynomial with `F`. The AQ2 gap `alpha/16` and GNS vacuum simplicity then belong to `omega_∞` itself.

**Verdict (dynamics): feasible, essentially mechanical.** The one thing to check is that the interaction-picture Lieb–Robinson bound (NS14 form, unbounded commuting `h_x`) applies to the commutator with a bounded face `W_f` exactly as written. The Round32 lead McDonough–Yin–Lucas–Zhang is not needed for these bounds.

---

## 3. Proposal: three research sub-rounds

The table ranks the loops by feasibility (1 = most feasible). The execution order follows the dependencies below.

| rank | loop | feasibility reason |
|---|---|---|
| 1 | BA2 | all constants admitted |
| 2 | BA1 | one short new lemma |
| 3 | BB1 | a standard but new polymer expansion |
| 4 | BB2 | assembly |
| 5 | BC1 | replay |
| 6 | BC2 | statement |

**Sub-round 1 (BA): locality inputs; two independent loops.**
- **BA1: Weighted creation norm and boundary decay of the AM2 coefficients.** *Paired.* Forward: Lemma W, with a boundary-weighted Lipschitz argument for the difference. Reverse: complex-`s` analyticity with Cauchy and tree locality.
  - *Target (exact):* (T1) for every F1/F2 box, every cutoff and `1 <= w <= 1/(37888|tau|)` (`= 390625/148` at the cap), `||c||_{sigma,w} <= 1/64`. (T2) For `u ∈ R`: `sum_{M∋u}||c^{N'}_M - c^N_M|| <= (1/32)(37888|tau|)^{n_0}/(1-37888|tau|)`, with `n_0 = N` (F1–F1, F2–F2) and `N-1` (F1–F2); preview `≤ 4.49e-9` at `N=2`.
  - *Retained failure:* only cardinality weights close. The outcome is then `limited`: smallness in support size, no distance decay.
  - *Mandatory label:* coefficient decay, not convergence of states.
- **BA2: Boundary independence of the dynamics on compact windows; existence of the F2 dynamics.** *Paired.* Forward uses polynomial `F`; reverse uses `F_lambda` with `lambda = 1`. Two decay functions give two bounds on one target.
  - *Target:* `sup_{|theta|<=1} ||tau^{F2,N}_theta(A) - tau^{F1,N}_theta(A)|| <= 3969 tau^2 e^{127008|tau|}(5N+1)/N^3` for `A ∈ B(H_R)`, `||A||<=1`, at every `|tau| <= 10^-8`. Plus: the F2 box dynamics converge in norm, uniformly on compact windows, to AQ1's `T_theta`.
  - *Retained failure:* the interaction-picture Lieb–Robinson form fails for the face commutator. The outcome is then `limited`, with no F2 dynamics.
- *Dependencies:* none (admitted AM2, AQ1, AY1 and AY2 only).

**Sub-round 2 (BB): the state limit and its correlations.**
- **BB1: Whole-sequence convergence of the R-marginal, common limit of F1 and F2, explicit rate.** *Paired.* Forward is route A (polymer gas plus KP plus Cauchy in `s`, using BA1). Reverse is route B (interpolation gap, `F_lambda` Lieb–Robinson from BA2, imaginary-time clustering).
  - *Target:* exact rationals `C`, `q < 1` with `||rho^{Fi,N}_R - rho^{Fj,N'}_R||_1 <= C q^{N-1}` for all `N' >= N >= 2`, `i,j ∈ {1,2}`. Tiers:
    - (a) any `q < 1`, which gives whole-sequence convergence and the common limit;
    - (b) `q <= 1/1000` and `C <= 4` at the cap (route A expectation `q = 222/390625`);
    - (c) `||rho^{F2,5}_R - rho^∞_R||_1 <= 2K_2' tau^2`.
  - *Retained failure:* KP not closable with evaluated constants (forward `limited`); `C_B` not explicit (reverse `limited`). A failed route is never evidence that the limits differ.
  - *Required sentence:* whole-sequence convergence of the named constructions, not uniqueness of infinite-volume ground states.
- **BB2: Correlation functions, gap and translation invariance of the limit.** *Single+skeptic.* Target:
  - `|c^{Fi,N}_A(theta) - c^∞_A(theta)| <=` an explicit exponential-in-`N` bound on `|theta| <= 1`;
  - `omega_∞ ∘ T_v = omega_∞` for coarse translations;
  - the AQ2 gap `alpha/16` and vacuum simplicity for `omega_∞`.
  - *Retained failure:* only polynomial-`F` rates close (`limited`: `O(1/N)`).
  - *Depends on* BA2 and BB1.

**Sub-round 3 (BC): consequences and the remaining uniqueness question.**
- **BC1: The AV2, AW2 and AX2 certificates as statements about `omega_∞`.** *Single+skeptic replay.* AX2 is the uniform model and needs BB1 re-instantiated with `J' = 29|tau|` (`S'_* = 7/(64·29·148|tau|)`).
  - *Target:* each certificate holds for `omega_∞` with its admitted radius or interval; the BB1 tail vanishes in the limit.
  - *Retained failure:* the uniform-model re-instantiation of KP does not close (AX2 transfer `limited`).
- **BC2: Uniqueness beyond the named constructions.** *Statement+skeptic, with one possible certified tier.* The tier: the same limit arises for **every** bounded boundary interaction satisfying AM2's H1–H5 with `J <= J_0` (route A covers these verbatim). The statement part is what separates this from uniqueness among all states with `omega(A*[H,A]) >= 0` (Yarotsky 2005 route; the local-gap argument is missing).
  - Deliverables: an updated obligations table and a falsifying scenario (states not arising as box limits).
  - *Target note:* the loop is a feasibility/format check for the statement and a blind threshold only for the boundary-class tier.
  - *Depends on* BB1.

The second-order constant (roadmap goal 5) stays triggered-only. The continuum goal stays statement-only; see §4 item 8 for a regime remark that changes neither.

---

## 4. Applications stage (BD1/BD2)

The admitted equations, where they apply, what must be re-derived, and the expected result or obstruction:

1. **Link-flip lemma, gauge-group transfer.**
   - *Equation:* `U_E H(tau,kappa) U_E^* = H(-tau,-kappa)`, where `E` meets every plaquette an odd number of times and `U_E` multiplies each link in `E` by a central `z`.
   - *Criterion (candidate theorem):* a central `z` with `rho(z) = -1` must exist in the Wilson-loop representation `rho`.
   - *Holds* for SU(2k), U(N), U(1), Z2, Sp(2k), and SO(2k) in the vector representation.
   - *Fails* for SU(N) with N odd (`Z_N` has no element of order 2), SO(2k+1), G2, and adjoint loops of any group.
   - *SU(3):* `-1 ∉ SU(3)` since `det(-1) = -1`. Multiplying `E` by `omega = e^{2 pi i/3}` maps `W_f = Re Tr U_f/3` to `Re(omega^{±1} Tr U_f)/3`. That is a unitary equivalence to a *flux-twisted* Hamiltonian, not a coupling sign flip. What survives for SU(3) is the `Z_3` N-ality selection rule on Haar integrals, plus charge conjugation `U → U^*` (which fixes `Re Tr`). No `tau → -tau` identity holds.
   - *Flip sets exist on Z^d boxes* (π-flux): `E = {x-links with y even}` in 2D; `E = {x-links with y+z even} ∪ {y-links with z even}` in 3D. On periodic tori, parity constraints can obstruct.
2. **Center-grading first-order parity (AW1).**
   - *Equation:* the first-order terms of `omega(W^2)`, `C(s)` and `c(theta)` vanish, using single-occurrence orthogonality and `E[W^3] = 0`.
   - *Criterion (candidate):* `E_Haar[W^3] = 0`. For SU(N), the terms `(Tr)^a (Tr^*)^b` with `a+b = 3` need `a ≡ b mod N`. So the parity **holds for every SU(N) with N ≠ 3** (including SU(5), where the flip lemma fails), and for U(N), U(1) and Z2.
   - It **fails for SU(3)**: preview Weyl integration gives `E[(Re Tr U)^n] = 1, 0, 1/2, 1/4, 3/4` for `n = 0..4`, so `E[W^3] = 1/108` with `W = Re Tr/3`. It also fails for G2 and SO(3) (cubic invariants).
   - The SU(3) obstruction is a certified **nonzero** first-order coefficient of the centered correlation, proportional to `E[W^3]/E_face`, computable exactly on an SU(3) one-plaquette graph.
3. **SU(2) corollaries of the flip lemma (exact).**
   - `omega(W_C)(-tau) = (-1)^{A(C)} omega(W_C)(tau)`. The reason: `|C ∩ E| ≡` the number of plaquettes of any spanning surface, mod 2.
   - Center-even observables (Casimirs, `W^2`) are even in `tau`.
   - On the Round11 graph with independent couplings: `<x>` is odd in `lambda_1` and even in `lambda_2`. AZ2's exact zero `a_2 = 0` is this lemma. AZ2's one-face/two-face difference `1/4212 = -187/33696 + 5/864` is the `lambda_1 lambda_2^2` coefficient. The lemma **predicts `a_4 = 0`** for `<x>`.
4. **Larger Wilson loop (1×2 rectangle).**
   - Second-order perturbation theory gives `omega(W_{1×2}) = 7 tau^2/124416 + O(tau^4)` when both faces carry `tau/3` in `delta` units. The derivation uses the Schur integral `∫ W_{f1} W_{f2} ds = W_{1×2}/4`, the rectangle energy `36 delta = 9 alpha/2`, and the two terms `2·tau^2/62208 + tau^2/41472`.
   - On the Round11 graph, `<z> = 7 lambda^2/216 + O(lambda^4)`. **Preview check:** `<z>/lambda^2` from the Round11 solver at `D = 6` is `0.0324073` at `lambda = 0.005`, against `7/216 = 0.0324074`. It is consistent with the `tau_FG = tau/24` dictionary.
5. **Electric Casimir.**
   - `omega(C_e) = n_e tau^2/27648 + O(tau^4)`, where `n_e` is the number of coupled faces containing `e`. On a graph this is `lambda^2/48` per coupled face.
   - **Preview check:** `∂E_0/∂rho` on the two-plaquette graph gives `<C_shared>/lambda^2 → 0.0416664` against `1/24`.
   - *Obstruction:* `C_e` is unbounded, so trace-norm tiers do not control it. The route is an energy-weighted anchored norm: AM2's factor `H_M^{-1}` bounds `||H_M c_M||`.
6. **Area law (conditional on BB1 route A).**
   - `|omega_∞(W_C)| <= 2K_C q^{A_min(C)}/(1-q)`: a Taylor order below the minimal area cannot close the loop under the center grading.
   - This gives a fixed-spacing string-tension lower bound `sigma a^2 >= log(1/q) ≈ 7.47` at the cap, with a perimeter correction through `K_C`. It is the Hamiltonian analogue of the classical strong-coupling area law (Osterwalder–Seiler 1978, search-summary depth). It is not continuum confinement.
7. **2+1D.**
   - AV1 F06–F12 are algebraic and transfer verbatim. The window kernel (`M_0 = 2`, `M_1 = 4s/pi`) is a one-dimensional spectral identity and transfers verbatim.
   - AM2 re-instantiates with site blocking at `p = 3`: `G_3(t) = 8e^{6t}(1+8t)`, `G_3(1/64) ≈ 9.885`, `G_3'(1/64) ≈ 129.6`, termination at order 6.
   - With 3 faces per site, `J = |tau|` and the cap is about `|tau| <= 1.58e-3`.
   - `+tau/144` transfers under the same face normalization. The first-order pins (faces per site, `t_1`, `D`, `K_2'`) must be recounted.
8. **Uniform 3+1D model with site blocking (regime remark).**
   - Per-site factors give `p = 3` and `J = 9·|tau|/3 = 3|tau|`. The candidate cap is `|tau| <= (1/64)/(3 G_3(1/64)) ≈ 5.27e-4`, which is `g^4 >= 1.82e5` in the AZ1 dictionary instead of `9.6e9`. Optimizing `R` may reach about `1e-3`.
   - This enlarges the admitted strong-coupling strip by a factor of about `5·10^4` in `tau`. **Every `g → 0` trajectory still leaves it, so the AZ1 conclusion is unchanged.**
   - It needs its own contract (new factors, new AQ chain).
9. **Finite graphs of earlier rounds.** Items 3–5 are exact predictions for the Round10/11 graphs, checkable with the Round11 solver's exact `Fraction` algebra to order 6. The Einstein–QED evidence rounds (3–7) are a different model: there is **no transfer**, recorded as an obstruction ("no shared equation").
10. **U(1) and Z2 gauge theories.**
    - The flip lemma holds. AM2 and AV1 transfer with recomputed onsite gaps: U(1) electric `n^2`; Z2 `1 - sigma^x`, gap 2, `E[W^2] = 1`.
    - 2+1D Z2 has the Wegner duality to the 2D transverse-field Ising model. That supplies an **external exact cross-check** of low-order coefficients, which the SU(2) family lacks.
11. **Site calculators.** These are display-only pages from source-bound data: a flip-parity sign table by group, the rectangle and Casimir coefficients, the rate curves `C q^{N-1}` and the (D1) bound against `N`. The site never computes an admission.

**Proposed split.**
- **BD1: Center-symmetry transfer across gauge groups and dimensions.** *Paired.* Items 1–3 and 10. Target:
  - the two criteria as theorems;
  - exact Haar moment tables (SU(2), SU(3), SU(4), SU(5), U(1), Z2);
  - flip sets verified on Z^2 and Z^3 boxes and on the 24-link factors;
  - a certified nonzero SU(3) first-order centered coefficient on the one-plaquette graph;
  - `a_4 = 0` for the Round11 `<x>`.
  - *Retained failure:* a group mis-classified by the criterion (then `limited` for that row).
- **BD2: New observables and dimensions in the admitted SU(2) models.** *Single+skeptic.* Items 4–9. Target:
  - exact coefficients `7/124416` (Z^3) and `7/216` (graph);
  - `n_e/27648`, and `1/48` per face on the graph;
  - at least one certified enclosure, on the Round11 graph at the AZ2 grid;
  - the 2+1D and site-blocked AM2 constants as exact rationals;
  - the area law only if BB1 is admitted.
  - *Retained failure:* the unbounded-Casimir step does not close (Casimir stays a labelled preview).

**Assistant computations:**
- python-flint `fmpq`: SU(N) Weyl-integration moments; exact `e^{3/32}` enclosure and `G_3` bounds.
- Round11 solver: exact Rayleigh–Schrödinger to order 6 for `<x>`, `<z>`, `<C_shared>`, with independent `lambda_1`, `lambda_2`.
- A small exact enumerator: flip sets and the reach count `n_0` for F1 and F2, including the `28N(5N+1)` faces and their exact ℓ1 distances, which sharpens `168(5N+1)/N^3`.
- mpmath previews of `mu_B(lambda)` and of the (D1)/(D2) curves.

---

## 5. State of the art, patents and programmes (this loop)

Details are in `sources.json` (27 records, 6 access failures) and `sota-table.md`.

**Directly relevant to §2.**
- **Kotecký's encyclopedia article on cluster expansion**, selected sections read through local text extraction. Its Theorem (cluster expansion) with the Dobrushin condition (24), the α-modified partition function (42)–(48) and the boundary-decay estimate (49) is exactly the template of §2.5.
- **Nachtergaele–Sims 2006, Theorems 1–2**, selected sections read. These give the clustering rate `mu = gamma lambda/(4||Phi||_lambda + gamma)` used in §2.6, but for finite-dimensional sites.
- **De Roeck–Schütz 2015 (JMP 56, 061901)**, abstract: exponential (not subexponential) locality of gapped perturbations.
- **De Roeck–Schütz 2017 (LMP 107)**, abstract: exponentially local spectral flow for possibly non-self-adjoint perturbations of **non-interacting** spins. This is the closest external structure to route A with complex `s`.
- **Yarotsky JSP 2005**, search summary; the Springer page is behind a login gate. Boundary dependence decays exponentially, and uniqueness follows for weak perturbations of non-interacting gapped systems. That is the BC2 target in its strong form. Its constants are not evaluated, and the unbounded-onsite hypotheses are unchecked.
- **Search summary only:** Kennedy–Tasaki CMP 1992 (rigorous ground-state perturbation theory near diagonal Hamiltonians); Datta–Fernández–Fröhlich (–Rey-Bellet) 1996; Kotecký–Preiss 1986 (metadata only); Ueltschi 2004 and Fernández–Procacci 2007 (abstracts, improved KP criteria); Hastings–Koma 2006 (abstract); Bravyi–Hastings–Michalakis 2010; De Roeck–Salmhofer 2019; Nachtergaele–Ogata–Sims 2006.
- **Center symmetry:** Greensite's review (search summary), Osterwalder–Seiler 1978 (search summary).

**Since 2026-09-24.**
- One item carries that date: Ciavarella–Hariprakash–Halimeh–Bauer, "Truncation uncertainties for accurate quantum simulations of lattice gauge theories", *Quantum* 10, 2216, published 2026-09-24 (arXiv:2508.00061v4; abstract read). It gives factorial truncation-error *estimates* in the electric basis for U(1) models, not enclosures.
- Nothing dated later was found.

**September 2026 discourse (leads only).**
- Zenodo records by one author claim an "unconditional" Yang–Mills mass-gap solution with Lean 4 certification (v12, 2026-09-19, abstract read; two companion records at search-summary depth). They are self-published, have no peer review and have no replayable connection to this model. They are a lead only; nothing depends on them.

**Programmes (custody only).**
- DOE Quantum Genesis Q competition: up to $215M for fault-tolerant computing with at least 100 logical qubits (2026-09-18; applications due 2026-10-19). It names no lattice-gauge deliverable.
- DOE Science Advisory Committee quantum subcommittee report (September 2026; selected passages read). It lists "lattice gauge theories" among scientific drivers and cites real-time string breaking on quantum simulators.

**Patents.** A search for SU(2) lattice-gauge simulation patents in 2026 returned only arXiv preprints; no patent record was found. Custody is not confirmation. No source here becomes a premise, and any claimed full solution is a lead only.

---

## 6. Closing

This lens admits nothing and counts zero research loops.
