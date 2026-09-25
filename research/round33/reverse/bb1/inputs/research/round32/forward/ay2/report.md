# Hruday statement on state identification: what the closeness lemma does and does not establish — AY2 forward (single producer)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted forward production (a Claude model agent) under the frozen AY2 contract (`research/round32/contracts/ay2.json`, sha256 `8e55e8e9d54b26520ab0fa10c1c6a967a616aabb4dc8c47988ff687d14d96b38`). AY2 is a `statement+skeptic` loop: this is the only producer, and admission also needs the skeptic's independent derivation and replays (`single_direction_independent_replay`). This is correlated model-agent work, not independent human review and not formal verification.

**What this producer read.**
- **The contract snapshot first.** `check.py` verifies its sha256 before any evaluation. After that, only files under `inputs/`:
  - **read in full:** `AGENTS.md`; `selection-ay2.md`; the AY1 gate (every field, including `bindings`); the AY1 forward report; the AY1 reverse report; `skeptic/ay1.md`; the AM2 gate; `skeptic/am2.md`; the I1 forward report; the AQ1 forward report; the paired-physics SKILL and its complete-residual reference; the Newton, Tesla and historical-panel SKILL files;
  - **read in part:** the AQ2 forward report (its first 40 lines and headings); the AT4 forward report (sections 3–5, headings, one control paragraph); the AM2 forward report (headings and keyword-search lines); the AM2 reverse report (keyword-search lines only);
  - **not opened:** the Newton and Tesla `references/research.md` notes and the historical-panel `lenses-and-evidence.md` (their line counts only). The checker hashes all 23 snapshots.
- **Outside `inputs/`, for protocol and code style only:** `research/round32/tools/README.md`, `research/round32/tools/freeze.py`, parts of `research/round32/forward/ay1/check.py` (helpers, contract parsing, the sentence and control sections and the packet assembly), the first 60 lines of `research/round32/forward/ax2/report.md`, the file names in `research/round32/forward/ax2/` and `research/round32/forward/ay1/`, and the line counts of `research/round32/forward/ax2/check.py`, `research/round32/forward/ax2/report.md` and `research/round32/forward/ay1/check.py`. I did not open `research/round32/forward/ax2/check.py`. None of these carries premise weight.
- **Not read:** nothing under `research/round32/skeptic/` other than the snapshot of `ay1.md` in `inputs/`; nothing under `research/round32/experts/`; no `advisor/deliberation-*.md` or `panel*.md`; no other agent's scratch folder.
- **Scratchpad disclosure (sub-round 2 rule).** My scratch work is in `/tmp/claude-0/ay2-forward-private/`: a Fraction/float preview of the gate recomputation (`prelim.py`), a development importer of `check.py` that writes no bytecode (`devrun.py`), a sentence printer (`sentence.py`), development runs and the production run `run1`. **None of it is evidence.** I created the folder directly with `mkdir -p` and did not list `/tmp/claude-0/` or the shared session scratchpad root, so I saw no other agent's folder names. **I opened no file in any other agent's scratchpad folder.** The Claude harness saved a copy of one of my own long reads (the AY1 forward report) to its tool-results cache; that is my own read, not another agent's file.

**Shared premises and attribution.** Every constant in the statement is AY1's, admitted by the AY1 gate after two producers and a skeptic reached the same rationals. The two-sided distance was already written down in AY1: forward F16, a reverse remark, and exact ends verified by the AY1 skeptic. The AY1 gate recorded it as a labelled observation only. AY2 contributes:
- the certification of that tier under its own contract, with an exact re-verification of the rank-two structure;
- the falsifying-scenario witness;
- the obligations table;
- the corrected wording.

The mathematics used is standard: the reverse triangle inequality, SU(2) Haar orthogonality, and the spectral theorem for finite-rank Hermitian operators. The candidate routes name established theorems (Nachtergaele–Sims via AQ1 §3, the Yarotsky dictionary of I1 §5, and HTW-type and Dobrushin-type conditions as named in the contract and the AM2 gate). None is evaluated here. Scientific priority is unverified. HNM labels are project aliases.

## Verdict (forward, single producer)

1. **Statement (item 1).** For the set of subsequential limits of the two named families, three things are proved (Section 1), all with the AY1 gate constants as exact rationals:
   - uniform local closeness `2D` on `R` in trace norm at fixed `tau`;
   - a common first-order density `rho^(1)_R`;
   - a second-order difference bound `2K_2' tau^2`.

   The mandatory sentence is filled in §1.4. Each statement holds for a chosen subsequential limit of either family, every one separately.
2. **Obligations (item 2).** The table in Section 2 has the six rows of contract item 2. All six are unproved, each with its missing premise, a candidate route and the constant that route would have to evaluate.
3. **Falsifying scenario (item 3).** Two limits may differ on `R` by up to `2K_2' tau^2`. An exact witness pair of density matrices on `H_R` satisfies every admitted constraint and differs by at least `(1-2·10^-6)·2K_2' tau^2`. Separately, `2D` also bounds the `+tau` and `-tau` limits, which differ by at least `8.75726955649e-10`; `2D` alone is therefore not a boundary comparison (Section 3).
4. **Tier (item 4), certified.** For every subsequential limit of either family at `|tau|=10^-8`:

   `315493271189404369878663368737136921794795815043212654249128159/720528856978172107545458049318912000000000000000000000000000000000000000 <= ||rho_R - P_R||_1 <= 317426814346354222051900617016352553019063789598114401371582241/720528856978172107545458049318912000000000000000000000000000000000000000`

   That is, `[4.37863477824e-10, 4.40546983333e-10]`. The relative width is at most `6.10991245541e-3`, against the preregistered `1/100` (margin about `1.6367`). The label is `first_order_distance_from_product`, a static property of the state on `R`.
5. **`K_2'` versus `K_2^+` (item 5).** This is recorded with its fixed direction, and the AY1 wording is corrected (Section 5).
6. **Checker (item 6).** `check.py` runs **42 exact checks**. All **21 contract controls** reject explicit damaging mutations (**85** rejections inside the control checks, **114** in the whole checker), and none is deferred. The `-B` and `-B -O` outputs are byte-identical.

**Proposed forward verdict: `accepted_within_scope`** (forward half), with sub-labels `uniform_local_closeness_not_uniqueness` and `static_not_dynamic`. The contract's acceptance ("verified by the skeptic with exact arithmetic") needs the skeptic's independent derivation and replays, which are outside this producer's work.

## 1. The statement

### 1.1 Model and the set of states

**Model:** `AQ_patterned_zero_selected`, the AM2/AQ1 zero-selected patterned family.
- SU(2) Kogut–Susskind form on `Z^3` at fixed spacing, with coarse 24-link factors.
- The selected triple is exactly `(0,0,0)`, so the reference is the Haar product `P_R=|Omega_R><Omega_R|`.
- The 21 omitted faces per anchor enter as `-(tau/3)W_f` in normalized units `delta=alpha/8`.
- Both signs of `tau`, with `|tau|<=10^-8`. The constants are evaluated at the cap `tau=±1/100000000`; the cap values bound every smaller `|tau|` (§4.2).
- Cover `R={0,e_z}`: 48 links, 36 endpoints, 7 incident anchors. Observable class `B(H_R)` with `H_R=L^2(SU(2)^48)`.
- Common clock `s=alpha t_E/hbar`, `theta=alpha t/hbar`. Every statement here is static; the clock is fixed only for later use.

**The two named families** use the same centered cubes `Lambda_N=[-N,N]^3`, `N>=2`:
- **F1** = centered whole-star boxes `Lambda_N` (AQ1);
- **F2** = all-contained-face boxes with padding (I1 section 6).

F2 retains `28N(5N+1)` boundary faces more than F1. Both retain the same 82 faces meeting `R`.

**The set of states.** At fixed `tau`, let `Sigma_tau` be the set of all locally normal states obtained as local trace-norm limits of the ground states of F1, or of F2, along some subsequence `N_k→∞` (AQ1 §2; AY1 §3.4 for F2). `Sigma_tau` is non-empty. **Nothing proved so far decides whether it has one element or many.** Every statement below holds for a chosen subsequential limit of either family, every one separately.

### 1.2 Constants (exact rationals from the AY1 gate; previews are labelled truncations)

| symbol | exact | preview | meaning |
|---|---|---|---|
| `D` | `585079838465912592144137406066050/42981220507576537932303142777593983768257` | `1.36124528702e-8` | AV1 forward tier (ii): `||rho_R-P_R||_1<=D` for every limit |
| **`2D`** | `1170159676931825184288274812132100/42981220507576537932303142777593983768257` | **`2.72249057405e-8`** | any two limits at the same `tau` (order `tau^1`) |
| **`rho^(1)_R`** | `(tau/72) sum_{f in F_R}(|W_f Omega_R><Omega_R| + |Omega_R><W_f Omega_R|)` over the 10 faces with owner set exactly `R` | — | the common first-order density |
| `||rho^(1)_R||_1` | `sqrt(10)|tau|/72`, square `10 tau^2/5184` | `4.39205230578e-10` at the cap | eigenvalues `±sqrt(10) tau/144` (§4.2) |
| `Tr(rho^(1)_R W)` | `+tau/144` | — | the AW1 first-order Wilson mean |
| **`K_2'`** | `966771578474926086618624139557778885954947547760216752246561/72052885697817210754545804931891200000000000000000000000` | **`1.34175275439e4`** | `||rho_R-P_R-rho^(1)_R||_1<=K_2' tau^2` for every limit |
| `K_2' tau^2` | `966771578474926086618624139557778885954947547760216752246561/720528856978172107545458049318912000000000000000000000000000000000000000` | `1.34175275439e-12` | single state against `P_R+rho^(1)_R` |
| **`2K_2' tau^2`** | `966771578474926086618624139557778885954947547760216752246561/360264428489086053772729024659456000000000000000000000000000000000000000` | **`2.68350550879e-12`** | any two limits (order `tau^2`) |
| `K_2^+` | `81108864767825329926713064490531229475390625/24176936535511801466930759024724079017984` | `3.35480322946e3` | AW1: the single observable `W` only |

`check.py` reads each rational from the hash-bound AY1 gate snapshot. It also recomputes each one from the gate's own itemization (`T=(49a)/(1-352J)`, `rho=352JT`, `a=|tau|/144`, `J=28|tau|`, `eps=2T+T^2`, `D=2eps(1+eps)/(1+eps^2)`, `eps_R=82a+2rho+(33a+rho)^2`, the five `K_2'` items, and `K_2^+ tau^2=rho+T·T+T^2+eps^2+a·eps^2`) and requires equality. The pins 82, 72, 33 and 10 are re-derived from the I1 table.

### 1.3 What is proved (AY1, restated with quantifiers)

For every `omega, omega'` in `Sigma_tau` (same family or different families, the same `tau`):

- **(a) Uniform local closeness:** `||rho_R(omega)-rho_R(omega')||_1 <= 2D`.
- **(b) Common first-order density:** `||rho_R(omega)-P_R-rho^(1)_R||_1 <= K_2' tau^2`, where `rho^(1)_R=tau·rho_hat` is the same operator for every box of both families and hence for every limit.
- **(c) Second-order difference:** `||rho_R(omega)-rho_R(omega')||_1 <= 2K_2' tau^2`, by (b) and the triangle inequality.
- **(d) The AY2 tier (Section 4):** `sqrt(10)|tau|/72-K_2' tau^2 <= ||rho_R(omega)-P_R||_1 <= sqrt(10)|tau|/72+K_2' tau^2`.

(a) and (c) are uniform local closeness on a fixed region at fixed coupling. (b) fixes a first-order coefficient, not a state. It is not a `tau`-derivative of a subsequential limit, because subsequences may depend on `tau`.

### 1.4 The mandatory sentence (template filled with the constants)

> For every pair of subsequential limits `omega'`, `omega''` of the named families `F1`, `F2` at the same coupling `tau`, and for every `A` in `B(H_R)` with `||A|| <= 1` on the fixed cover `R`: `|omega'(A) - omega''(A)| <= 2D = 1170159676931825184288274812132100/42981220507576537932303142777593983768257` (about 2.72249057405e-8; order `tau^1`), and `<= 2K_2' tau^2 = 966771578474926086618624139557778885954947547760216752246561/360264428489086053772729024659456000000000000000000000000000000000000000` (about 2.68350550879e-12; order `tau^2` after subtracting the common first-order density `rho^(1)_R`). This is uniform local closeness on a fixed region at fixed coupling, inherited from a finite-volume bound that holds for every volume. It does not assert `omega' = omega''`, convergence of any whole sequence, translation invariance, boundary independence beyond `R`, or any rate in `N`; two states satisfying it may differ by the stated order on `R` and without bound elsewhere.

`check.py` takes the template's fixed text from the AY1 forward report snapshot and finds it identical (code spans removed) in the AY1 reverse snapshot. It then requires this filled sentence verbatim in this report.

### 1.5 What the statement does not say

It does **not** say any of the following:
- that `Sigma_tau` has a single element, or that two limits coincide on `R` or anywhere else;
- that any whole sequence of boxes converges;
- that any limit is translation invariant;
- that anything holds at a rate in `N`;
- that the dynamics of F1 and F2 agree on compact time windows, or that F2 has a dynamics at all;
- that anything holds outside `R`.

All of these are obligations (Section 2). The closeness is also not a variational statement about which boundary condition the infinite-volume theory selects.

## 2. Obligations table

| id | obligation | status | missing premise | candidate route | constant that would have to be evaluated |
|---|---|---|---|---|---|
| O1 | uniqueness of the limit | unproved | Not available: a two-state estimate, or a classification of every state in the class, that forces two subsequential limits to agree on R; every admitted bound is a one-state ball, and uniqueness is not implied by closeness. | HTW-type local stability with evaluated constants (the AM2 gate records that the HTW boundary constants are not evaluated and that the HTW symbolic smallness condition is separate from the numerical cap), or a Dobrushin-type uniqueness condition at the cap (not yet formulated for this model); the Yarotsky theorem dictionary-matched in I1 section 5, named by the AY1 skeptic as a candidate, gives nothing numerical because its constants are not evaluated. | c_1(S) and c_2(S) of I1 section 5 with tau_* = (1/7)min{c_1(S), 1/(2c_2(S))} shown above 10^-8; or explicit HTW boundary constants; or a Dobrushin influence row sum below 1 at J_0=7/25000000. |
| O2 | whole-sequence convergence | unproved | A Cauchy estimate in N for the reduced densities of each family on R (and on every finite region); the admitted bounds hold with one constant in every box and say nothing about how the box density moves with N, and compactness yields subsequences only. | A Cauchy estimate in N from a boundary-influence (locality) refinement of the AM2 fixed point: the creation coefficients on supports near R should depend on the box only through chains of overlapping supports that reach the boundary at distance N-1; missing. | A per-shell decay factor kappa<1 and a prefactor C with the R-densities of the boxes N and N+1 within C kappa^(N-1) in trace norm; the AM2 contraction constant 2J_0G'(R)<77/390625 is a global Lipschitz bound and does not by itself give decay in distance. |
| O3 | translation invariance | unproved | Not available: translation covariance of the construction together with O1 or O2. The model is coarse-translation covariant (a coarse translation is a fine translation preserving residues, face classes and owner sets), but the centered boxes are not, and a translated box sequence is a different sequence whose limits are not shown to coincide with the originals. | Translation covariance plus O1 in the form that covers every exhausting sequence of boxes, translated ones included (the translate of a limit is a limit along translated boxes), or translation covariance plus a van Hove boundary estimate comparing each box with its translate; missing. | The O2 boundary-influence constants (a box and its translate differ only near their boundaries), or the O1 constants. |
| O4 | a rate in N | unproved | Any N-dependent estimate: every admitted constant (D, K_2', the reset budget 98abs(tau)) is uniform in N, so no rate can be read from them, and the subsequence construction has none. | A quantitative form of the O2 Cauchy estimate; summing its tail would give a rate for the whole sequence and for the limit; missing. | The O2 constants C and kappa (or C and an exponent p for a bound C N^-p), plus the passage from the Cauchy bound to the limit. |
| O5 | boundary independence of dynamics on compact time windows | unproved | A comparison of the F1 and F2 finite-volume dynamics of local observables near R, uniform on compact time windows; AY1 names the topology (norm on compact time windows) but constructs no F2 dynamics, and no locality estimate compares the two prescriptions. | A Lieb-Robinson locality argument with the AM2 constants: by Duhamel, the difference of the two box evolutions of a local A is a time integral of commutators of the 28N(5N+1) extra F2 boundary faces with the evolved A, and a Lieb-Robinson bound makes each small at distance N-1 from R; not executed. | The Nachtergaele-Sims prefactor and velocity for the whole-star interaction (AQ1: F(r)=(1+r)^-4, C<=224, interaction norm <=81J<=2268abs(tau) from the AM2 per-site sum J<=28abs(tau)) and for the owner-set interaction (norm <=1323abs(tau), AY1 reverse, named only); the face count 28N(5N+1); the distance N-1; the decay F(N-1)=N^-4. |
| O6 | dynamics of the padded family itself | unproved | An infinite-volume dynamics for F2: AQ1 section 3 places F1 in the Nachtergaele-Sims theorem, but for the padded family no such application is made, and no stationarity of its limits, GNS continuity or generator positivity is proved. | Nachtergaele-Sims Theorem 4.1 applied to the owner-set interaction, whose native restrictions are exactly the F2 box Hamiltonians (padding sites carry onsite terms only), followed by AQ1 sections 4-5 for the F2 limits; not executed. | The owner-set interaction norm (at most 1323abs(tau) with F(r)=(1+r)^-4, AY1 reverse, named only) and the convolution constant C<=224; the compact-window norm-convergence bound; stationarity of each F2 subsequential limit. |

**Notes on the table.**
- The row names are read from contract item 2, and `check.py` requires exactly these six rows, in this order, all `unproved`.
- O5 and O6 are linked. A Lieb–Robinson comparison that goes to zero with `N`, uniformly on compact windows, would also produce F2's limiting dynamics as the same norm limit. That is a candidate, not a result.
- O1, O2 and O3 are linked through the same missing input: an estimate that compares two boxes, two families or two subsequences directly, instead of comparing each with a fixed centre.

## 3. The falsifying scenario

### 3.1 The scenario

Two subsequential limits at the same `tau`, for example one of F1 and one of F2, may have `R`-densities that:
- agree to first order (both carry `rho^(1)_R`);
- differ at second order by up to `2K_2' tau^2 = 2.68350550879e-12` (preview) on `R`;
- differ without bound outside `R`.

Nothing in the admitted material excludes this. The scenario is **not asserted to occur**: the limits may coincide. The present bounds are silent on the question.

### 3.2 Why the present bounds cannot exclude it

Every constraint the admitted material places on a subsequential limit `omega` is a **one-state** condition. Each is proved box by box and passed to limits through a closed set:
1. `||rho_R-P_R||_1<=D` (AV1 tier ii);
2. `||rho_R-P_R-rho^(1)_R||_1<=K_2' tau^2` (AY1);
3. `|omega(W)-tau/144|<=K_2^+ tau^2` (AW1, as bound in the AY1 gate);
4. the reset energy `omega(h_R)<=98|tau|` (normalized units);
5. gauge invariance;
6. positivity and unit trace.

None of them compares two boxes, two families or two subsequences. A set cut out by one-state conditions around a common centre contains distinct points: its diameter is the only thing the triangle inequality controls.

**Exact witness** (`falsifying_scenario_witness`). Take `e_f=2W_fOmega_R` for the ten faces with owner set `R`. Put `v=sum_f e_f` and `w'=e_{yz0}-e_{yz1}+e_{yz2}-e_{yz3}` (the four yz faces), and

`psi_± = Omega_R + (tau/144) v ± nu w'`,  `nu = K_2' tau^2 (1-10^-6)/4`,  `rho_± = |psi_±><psi_±|/||psi_±||^2`.

These are genuine density matrices on `H_R`. In exact arithmetic on the 11-dimensional span, the checker verifies each constraint:
- `||rho_±-P_R-rho^(1)_R||_1 <= K_2' tau^2`. This is certified by an exact decomposition of `||psi||^2(rho-P_R-rho^(1)_R)` into six rank-one or rank-two pieces, with directed square roots for their trace norms; the upper bound is `1.34175150939e-12`.
- `||rho_±-P_R||_1<=D`.
- `Tr(rho_± W)=(tau/144)/||psi||^2`, inside the AW1 band.
- An energy of `3(||psi||^2-1)/||psi||^2` alpha-units, far below `98|tau|/8` alpha-units.
- Gauge invariance, since `Omega_R` and the `W_f Omega_R` are gauge-invariant functions.

Yet `rho_+ ≠ rho_-`. Exactly, `||psi||^2(rho_+-rho_-)=2nu(|w'><x|+|x><w'|)` with `x=Omega_R+(tau/144)v ⊥ w'`, a rank-two operator. This gives

`||rho_+-rho_-||_1 >= 483384822465884568383225451154749885198587818932560615906528253439/180132214244543026886364512329728000000000000000000000000000000000000000000000` (about `2.68350014178e-12`), that is, at least `(1-2·10^-6)·2K_2' tau^2`.

So `2K_2' tau^2` is, up to `2·10^-6`, the diameter that the admitted constraints allow. The witness is not a constructed limit (`transfers_to_aq: false`). It shows only what the bounds leave open. Excluding the scenario needs a two-state input (O1 or O2).

### 3.3 `2D` is not a boundary comparison; the `±tau` limits

The first-order densities at `+tau` and `-tau` are opposite: `||rho^(1)_R(tau)-rho^(1)_R(-tau)||_1=sqrt(10)|tau|/36` (AY1). With (b) at both signs, any limit at `+tau` and any limit at `-tau` satisfy

`||rho_R(+)-rho_R(-)||_1 >= sqrt(10)|tau|/36 - 2K_2' tau^2 >= 315493271189404369878663368737136921794795815043212654249128159/360264428489086053772729024659456000000000000000000000000000000000000000` (about `8.75726955649e-10`, directed with the lower `sqrt(10)` bracket).

Yet each lies within `D≈1.36124528702e-8` of `P_R`, so the pair also lies within `2D`. The contract's "both lie within `2D` of the product" should read "each lies within `D` of the product", so the pair is within `2D` (wording note D4). Because `P_R` does not depend on `tau`, `2D` bounds pairs at different couplings as well. `2D` alone is a common enclosing ball, not a boundary comparison.

The boundary-comparison content is the **matching first-order term** `rho^(1)_R` together with the `2K_2' tau^2` difference. That bound fails across signs by a factor of about 326, which is why every statement fixes the same coupling.

## 4. The two-sided first-order distance tier `first_order_distance_from_product`

### 4.1 Statement

For every subsequential limit of either family, at `|tau|=10^-8` and either sign:

\[
 \frac{\sqrt{10}\,|\tau|}{72}-K_2'\tau^2\ \le\ \|\rho_R-P_R\|_1\ \le\ \frac{\sqrt{10}\,|\tau|}{72}+K_2'\tau^2 ,
\]

certified with directed rational brackets as

- **lower** `L = 315493271189404369878663368737136921794795815043212654249128159/720528856978172107545458049318912000000000000000000000000000000000000000` (about `4.37863477824e-10`);
- **upper** `U = 317426814346354222051900617016352553019063789598114401371582241/720528856978172107545458049318912000000000000000000000000000000000000000` (about `4.40546983333e-10`);
- **relative width** `(U-L)/(sqrt10_lower·|tau|/72) <= 966771578474926086618624139607815612133987277450873561227041/158230021383939647982640996438347350340375381295486435500687360` (about `6.10991245541e-3`). This is at most the preregistered target `1/100` (read from the contract), with margin about `1.6366846`. The ideal value `2K_2' tau^2/(sqrt(10)|tau|/72)=144K_2'|tau|/sqrt(10)` is at most the same bound.

The `-tau` interval is the same: it replays the same `|tau|` formula and is not a second confirmation.

### 4.2 Proof

**Step 1: the first-order density is rank two, with trace norm `sqrt(10)|tau|/72`.** I verified this myself in exact arithmetic (`first_order_vectors_orthonormal`, `first_order_density_rank_two`):
- The ten faces with owner set exactly `R` are all anchored at 0: xz `r=0,1,2`, `s=0,1`, and yz `r=0..3`, `s=0`. `check.py` derives them from the parsed I1 table and the fine-lattice link tails. Each has four distinct links, and the original `W` is xz `r=0`, `s=0`.
- `W_f=(1/2)Tr U_f` is real with `|W_f|<=1` (I1 §4).
- The Haar moments `E[W^n]` agree by two routes, the Clebsch–Gordan invariant count and Weyl/Wallis. In particular `E[W]=0` and `E[W^2]=1/4`.
- For `f≠g`, a link of `f` not in `g` occurs once in `W_fW_g`. The centre grading `U_e→-U_e` then kills the Haar integral, so `E[W_fW_g]=0`. For `f=g`, the holonomy of four distinct Haar links is Haar, so `E[W_f^2]=1/4`.
- Hence `e_f=2W_fOmega_R` are orthonormal and orthogonal to `Omega_R`.
- So `rho^(1)_R=(tau/72)sum_f(|W_fOmega_R><Omega_R|+h.c.)=(tau/144)(|v><Omega_R|+|Omega_R><v|)` with `v=sum_f e_f` and `||v||^2=10`, by Pythagoras over the orthonormal `e_f`. This is exact orthogonality, not a statistical root-N.
- With `u=v/sqrt(10)`, `rho^(1)_R=(sqrt(10)tau/144)(|u><Omega_R|+|Omega_R><u|)`. It has eigenvalues `±sqrt(10)tau/144`, each simple, and 0 on the orthogonal complement. Its trace norm is `2·sqrt(10)|tau|/144=sqrt(10)|tau|/72`.
- The checker verifies `rho_hat^3=(10/144^2)rho_hat`, `Tr rho_hat=0` and `Tr rho_hat^2=20/144^2`. For a real symmetric `A`, `A^3=c^2A` puts every eigenvalue in `{0,±c}`. The zero trace pairs `+c` with `-c`, and `Tr A^2=2c^2` leaves exactly one pair. Also `Tr(rho^(1)_R W)=+tau/144` exactly (AW1).

**Correction to the relayed wording.** The instruction I received described "ten rank-one pieces" combining to a rank-two operator "with eigenvalues ±sqrt(10)tau/72". The exact statement is as follows:
- each piece `(tau/72)(|W_fOmega_R><Omega_R|+h.c.)` is itself **rank two** (a rank-one operator plus its adjoint), with eigenvalues `±tau/144`;
- the sum is rank two because all ten pieces share `Omega_R`;
- its eigenvalues are `±sqrt(10)tau/144`, not `±sqrt(10)tau/72`;
- the trace norm `sqrt(10)|tau|/72` is the sum of their absolute values, as the AY1 packages state.

The checker rejects the `±sqrt(10)tau/72` spectrum and the rank-one reading as damaging mutations. The contract text itself states only the trace norm, which is correct.

**Step 2: the single-state remainder `K_2' tau^2` is justified from the AY1 report items, not assumed** (`single_state_remainder_justified`).
- AY1 forward F13 is an exact decomposition of `r_R=rho_R-P_R-rho^(1)_R` in every box of either family at every cutoff `L>=24`.
- F14 bounds `||r_R||_1` item by item: `4rho+2T(72a+2rho)+2(33a+rho)^2+2eps_R^2+20a·eps_R^2=K_2' tau^2`, uniformly in `N`, cutoff and family. The AY1 reverse reaches the same ledger through its own identity.
- AV1 F22 (cutoff-vector removal) passes the bound to the untruncated ground.
- The set `{X: ||X-P_R-rho^(1)_R||_1<=K_2' tau^2}` is closed in trace norm, and its centre is the same operator for every box (both families retain the same ten faces for `N>=2`). The bound therefore passes to every subsequential limit.
- The AY1 gate admits exactly this single-state form ("for every subsequential limit of either family `||rho_R-P_R-rho^(1)_R||_1<=K_2' tau^2`").
- `2K_2' tau^2` is the pair bound obtained by the triangle inequality. The tier concerns one state, so it uses `K_2' tau^2`. The checker rejects both the halved remainder and the pair constant in its place.
- **Monotonicity.** Each item divided by `tau^2` is a sum of products of nonnegative nondecreasing functions of `|tau|`: `T/|tau|=(49/144)/(1-9856|tau|)`, `rho/|tau|=9856·T`, and `eps_R/|tau|`. So `K_2'(|tau|)` is nondecreasing, and the cap value bounds every smaller `|tau|`. The checker confirms the order exactly at `tau`, `tau/10`, `tau/100` and `tau/1000` (about 13417.528, 13416.337, 13416.218, 13416.206).

**Step 3: the reverse triangle inequality.** `| ||rho_R-P_R||_1 - ||rho^(1)_R||_1 | <= ||rho_R-P_R-rho^(1)_R||_1 <= K_2' tau^2`.

**Step 4: directed arithmetic.**
- `sqrt(10)` lies in `[lo, hi]` with `lo=floor(sqrt(10)·10^30)/10^30` from the integer square root of `10·10^60`, and `hi=lo+10^-30`. The checker verifies `lo^2<10<hi^2`.
- `L=lo|tau|/72-K_2' tau^2` and `U=hi|tau|/72+K_2' tau^2`, checked as squares: `(L+K_2' tau^2)^2 <= 10tau^2/5184 <= (U-K_2' tau^2)^2`.
- Rounding `sqrt(10)` the wrong way, a halved remainder, and a dropped remainder are each rejected.

### 4.3 Consistency with AY1

- The AY1 gate's recorded observation `[4.3786e-10, 4.4055e-10]` matches `L` and `U` to its printed digits.
- The AY1 skeptic's exact forward ends agree with `L` and `U` to within `10^-22`. The small differences come from the `sqrt(10)` brackets.
- The upper end is about 30.9 times below `D`.

### 4.4 Reading

- The label is **`first_order_distance_from_product`**. It is a **static property of the state on `R`**: the size, in trace norm, of the deviation of the reduced density from the Haar product.
- It is **not** an interaction-shift claim; `resolved_interaction_shift` stays false, since that flag concerns the Euclidean and dynamical shift.
- It is **not** a Euclidean-node statement; there are no `s` nodes, and the preregistered node list is empty.
- It is **not** a dynamical claim.
- **The lower bound `L>0`** shows that no subsequential limit of either family coincides with the Haar product `P_R` on `R`, at either sign. More generally, for every `0<|tau|<=10^-8`, `||rho_R-P_R||_1 >= |tau|(lo/72-K_2'·10^-8)` with `lo/72-K_2'·10^-8≈4.3786e-2>0`.
- **It does not identify the limit.** The two witness states of §3.2 both lie in the tier. So do the `+tau` and `-tau` limits of §3.3, which differ by about `8.757e-10`. The tier is a scalar distance and is blind to direction and sign.

## 5. `K_2'` versus `K_2^+`

| constant | value | what it bounds |
|---|---|---|
| `K_2^+` (AW1, bound in the AY1 gate) | `3.35480322946e3` | `|omega(W)-tau/144|`: one observable `W`; uniform in `N` |
| `K_2'` (AY1, headline, triangle) | `1.34175275439e4` | `||rho_R-P_R-rho^(1)_R||_1 = sup_{A in B(H_R), ||A||<=1}|Tr(r_R A)|` |
| ratio `K_2'/K_2^+` | `3867086313899704346474496558231115543819790191040867008986244/966893014524284957965768152362480514948256313800811767578125` (about `3.9994976`) | |

- **The direction is fixed by duality.** We have `||W||<=1`, `Tr(P_R W)=E[W]=0` and `Tr(rho^(1)_R W)=tau/144`. So `|omega(W)-tau/144|=|Tr(r_R W)|<=||r_R||_1`. Every valid trace-norm constant is therefore a valid `W` constant, and the smallest valid trace-norm constant is at least the smallest valid `W` constant. A trace-norm constant over all of `B(H_R)` can never be sharper than the best single-observable constant.
- **The AM2 remainder dominates both.**
  - `rho/tau^2 = 3354.108…` is 99.979% of `K_2^+`; `4rho/tau^2 = 13416.43…` is 99.992% of `K_2'`.
  - `W` pairs only with the two-site sector, with multiplier `2||WOmega_R||=1`. The trace norm pays the multiplier 2 and also charges the one-site remainders.
  - With the admitted remainder `rho=352JT`, every trace-norm constant assembled from the AW1 items is at least `2rho/tau^2=47162500000/7030557` (about `6708.2167`), which already exceeds `K_2^+`.
  - Face restriction changes only the count-dependent items (straddling `0.340`, two-creation `0.105`, density `0.649`; about `1.09` in total). It cannot touch the dominant item. So face restriction cannot make `K_2'` smaller than `K_2^+`.
- **Labelled variants, as previews only.** These are recomputed here and match the gate previews: the `sqrt 2` sectors variant `≈9487.94517`, the 288-majorant variant `≈10978.1762`, both refinements `≈7763.06332`, and the admitted-`eps` variant `≈13417.8053`. All are valid upper bounds and all exceed `K_2^+`. **None is admitted, and none enters the tier.**
- **Correction of the AY1 contract wording** "not the whole-box `K_2^+`". `K_2^+` is **not** a whole-box, volume-dependent constant: it is volume-uniform and `W`-specific. What distinguishes `K_2'` is that it is built from `R`-local face pins (82, 72, 33, 10) and bounds the full trace norm on `B(H_R)`. It is **larger**, by the factor above, not smaller.

## 6. Model label, exclusions, verdict, controls and map

### 6.1 Model label

`AQ_patterned_zero_selected`. The selected triple is `(0,0,0)` (Haar reference `P_R`); `tau=±1/100000000` (every `|tau|<=10^-8` through monotonicity); families F1 and F2 on centered `Lambda_N`, `N>=2`; cover `R={0,e_z}`; observable class `B(H_R)`; clock `s=alpha t_E/hbar`, `theta=alpha t/hbar`.

Topologies:
- states and the tier: the trace norm on `B(H_R)`;
- dynamics: the norm on compact time windows, named only, with no dynamical statement.

Every bound is uniform in `N` at fixed lattice spacing `a` and fixed `tau`, and none is uniform in `a`. By the AL1 dictionary `tau=96/g^4` (a different model, as quoted in AY1), the cap means `g^4>=9.6·10^9`: extreme strong bare coupling.

### 6.2 Exclusions

- **Contract (verbatim):** `uniqueness`; `whole-sequence convergence or a rate in N`; `translation invariance`; `boundary independence of dynamics`; `interaction shift or dynamical claim from the static tier`; `continuum`; `scientific priority`.
- **Preregistration (verbatim):** `free reference inside enclosure => no interaction claim`; `uniqueness of the AQ state`; `whole-sequence convergence or rate in N`; `continuum or weak coupling`; `transfer from a finite graph`; `relabelling a static shift as dynamical`; `scientific priority`.
- **Additional:**
  - no identification of any limit;
  - no dynamical, Euclidean-node or interaction-shift reading of the tier;
  - nothing outside `R`;
  - not uniform in `a`;
  - the witness of §3.2 is not a constructed limit.

**Claim flags, all false:** `continuum_claim`, `uniform_wilson_claim`, `resolved_interaction_shift`, `scientific_priority_verified`, `weak_coupling_claim`, `uniqueness_claimed`, `whole_sequence_claimed`, `rate_claimed`, `rate_in_N_claimed`, `translation_invariance_claimed`, `boundary_independence_of_dynamics_claimed`.

**Also exported:** `states_compared`, `region`, `topology`, `closeness_order: [1, 2]` (order 1 for `2D`, order 2 after `rho^(1)_R` cancels), and the `label` block with the tier data.

### 6.3 Contract wording defects (non-blocking; each verified against the frozen text in `contract_wording_defects_recorded`)

| id | field | defect |
|---|---|---|
| D1 | `selected_after` | the placeholder `<preceding gate>` was left unfilled (the preceding gate is AY1) |
| D2 | preregistration `claim_exclusions` | contains `uniqueness of the AQ state`, the definite phrasing that item 1 forbids; quoted only verbatim in code spans and never asserted |
| D3 | `gate_fields_required` | lacks `rate_in_N_claimed`, which item 6 requires; both rate fields are exported false |
| D4 | item 3 | "both lie within 2D of the product": each limit lies within `D` of `P_R`, so the pair is within `2D`; "at least 8.7e-10" is the preview of `sqrt(10)|tau|/36-2K_2' tau^2≈8.757e-10` |
| D5 | item 5 | the AY1 wording "not the whole-box `K_2^+`" is corrected as instructed (Section 5) |
| D6 | `selection_reason` | "a certified two-sided distance" anticipates AY2: the AY1 gate recorded it as a labelled observation only, and it is certified here under the AY2 contract |
| R1 | relayed instruction (not contract text) | "ten rank-one pieces … eigenvalues `±sqrt(10)tau/72`" is corrected in §4.2 |

### 6.4 Error ledger (preregistered terms)

| term | value | note |
|---|---|---|
| `first_order_term` | `sqrt(10)|tau|/72` in `[lo|tau|/72, hi|tau|/72]` (about `4.39205230578e-10`) | directed: the lower end of the tier uses `lo`, the upper end uses `hi` |
| `second_order_remainder` | `K_2' tau^2≈1.34175275439e-12` (single state); `2K_2' tau^2≈2.68350550879e-12` (two limits) | AY1 gate headline; items added linearly |
| no other terms | `not_applicable`, with the stated reason: this is a statement loop, and the only new certificate is the tier | all arithmetic exact except the `sqrt(10)` bracket, whose `10^-30` width is charged in `L` and `U` |

### 6.5 Controls (every one a damaging mutation in `check.py`; none deferred)

| control | damaging mutations rejected |
|---|---|
| `missing_incoming_stars` | outgoing stars only (42 faces meeting `R` instead of 82, so the recomputed `K_2'` differs from the gate); a single star at 0 |
| `full_original_wilson_cover` | a single-factor cover `{0}`; the four drawn links as the cover (48 links and 36 endpoints required) |
| `wrong_delta_alpha_hbar_clock` | per-face coefficients `tau/576` and `tau/9` (mixed units); a normalized clock; a tier centre with a mixed-unit coefficient |
| `vector_versus_scalar_centering` | vector or scalar centering imposed on the uncentered density (AT4 residues `1/10000`, `-51/10000`, `1/16` recomputed); the scalar Wilson mean `tau/144` as the tier centre |
| `first_order_mean_charged` | first-order density set to zero (contradicted by `omega(W)>=tau/144-K_2^+ tau^2>K_2' tau^2`); tier lower end set to zero |
| `tau_scaling_exponent` | first-order term labelled second order; second-order remainder labelled first order; relative width labelled `tau`-independent |
| `changed_model_relabelled` | `tau` above the cap; a nonzero triple; the selected-strip reference; the uniform route-B model; literal vertex boxes as a family; the falsifier fixture relabelled as AQ data |
| `coherent_evidence_tampering` | with the packet hash rebound: a control flipped; the tier lower end raised; `K_2'` quartered; the relative width halved; an obligation row removed; `uniqueness_claimed` true; the AY1 gate hash replaced; the AY1 skeptic snapshot removed; the falsifier separation doubled; the label-block lower end doubled; the ledger single-state remainder halved (exported values are pinned to the headline and recomputed) |
| `insufficient_verdict_retained` | a missing obligation relabelled accepted; an overclaim relabelled limited; an uncertified tier relabelled accepted; the `D`-ball tier retuned to pass. Retained failures: the `[0,D]` tier (relative width about 31) and `[tau/144-K_2^+ tau^2, D]` both fail `1/100` |
| `exact_arithmetic_admission` | float, bool, NaN and zero-denominator inputs; a decimal preview as an admission value |
| `root_n_misuse` | root-sum-square of two single-state remainders; division by `sqrt` of the face count; `sqrt(10)` read as a statistical root-N; the linear face sum `10|tau|/72` as the trace norm |
| `no_priority_or_continuum_claim` | continuum, priority, uniform-Wilson, shift or weak-coupling flag set true |
| `topology_named` | weak-* for states; the tier claimed in the dynamics topology; one topology for both; a dynamical statement added |
| `two_families_named` | one family only; a third family (literal vertex boxes); "all boundary conditions" |
| `subsequence_versus_whole_sequence` | whole-sequence convergence or a `1/N` rate inferred from uniform bounds (witness: the alternating sequence `rho_+, rho_-, …` obeys every one-state bound and has two limits); `whole_sequence_claimed` true |
| `local_closeness_not_uniqueness` | equality inferred from `2K_2' tau^2`-closeness; equality inferred from a common tier; `uniqueness_claimed` true |
| `common_clock` | opposite signs (separated by about `8.757e-10`); different couplings; mixed units for one family; a normalized clock for one family |
| `tier_mixing_rejected` | `K_2^+` (W only) as the trace-norm remainder; a labelled variant as the headline; the pair constant `2K_2'` as the single-state remainder; `D` as a second-order remainder; the lower end from `K_2^+` with the upper end from `K_2'` |
| `not_uniform_in_a` | uniformity in `a` claimed; uniformity in `N` read as a continuum statement |
| `lower_bound_is_static_not_dynamic` | the tier relabelled as dynamical, as an interaction shift or as a Euclidean node; the lower bound read as an identification; `resolved_interaction_shift` true |
| `obligations_table_complete` | the padded-family dynamics row removed; the O1 row (uniqueness, not proved) marked proved; the Cauchy route emptied; a seventh row added; rows reordered |

**Source-edit audit (private scratch, not evidence).** I ran sixteen damaging edits, each on a mirrored copy of this directory in `/tmp/claude-0/ay2-forward-private/audit/`, plus one unmutated copy. Every damaging edit aborts, and the unmutated copy reproduces the run. The edits and where they abort:
- **Tier ends:** the lower end with half the remainder, and `sqrt(10)` rounded the wrong way. Both abort at the directed tier test.
- **Constants and pins:** the AM2 item `4rho` replaced by `2rho` aborts because `K_2'` then differs from the gate. Dropping the incoming stars aborts at the face enumeration. The per-face coefficient `tau/576` aborts at the rank-two check.
- **Witness and separation:** the witness moved twice as far aborts because it leaves the `K_2'` ball. A `±tau` separation that is not a lower bound also aborts.
- **Flags and exported values:** `uniqueness_claimed` set true, a headline lower end edited, and a label-block lower end edited all abort in the packet validators.
- **Report edits:** row O6 renamed, row O1 marked proved, the thermodynamic-limit phrase appended, and the sentence's negation removed all abort. So does removing one control row from the §6.7 map.
- **Contract:** a byte edit aborts at the sha256 check.

Disclosure: the map test first accepted any backticked occurrence of a control id anywhere in the report, so a copy that removed the map row ran silently. `report_item_and_control_map` now requires one row per control and per item inside §6.7, and that edit aborts.

### 6.6 Proposed verdict

**`accepted_within_scope` (forward half),** with sub-labels `uniform_local_closeness_not_uniqueness` and `static_not_dynamic`. The rule in `check.py` follows the contract acceptance:
- `insufficient` on any overclaim flag;
- `limited` if an obligation row is missing, a constant is inexact, or the tier is uncertified;
- otherwise `accepted_within_scope`, which the skeptic's independent derivation and replays must still confirm.

If the skeptic finds the tier or a constant uncertified, `limited` is the correct outcome.

### 6.7 Map of required items and controls to statements and checks

| item / control | where stated | `check.py` check id(s) |
|---|---|---|
| item 1 (statement, constants, sentence, phrasing) | §§1.1–1.5 | `ay1_gate_constants_parsed_exact`, `ay1_gate_constants_recomputed`, `two_limits_second_order_bound`, `mandatory_sentence_and_phrasing` |
| item 2 (obligations table) | §2 | `obligations_table_complete` |
| item 3 (falsifying scenario; `2D` across couplings) | §3 | `falsifying_scenario_witness`, `plus_minus_tau_separation` |
| item 4 (two-sided tier) | §4 | `i1_face_enumeration_R_local`, `haar_moments_two_routes`, `first_order_vectors_orthonormal`, `first_order_density_rank_two`, `sqrt10_enclosure`, `single_state_remainder_justified`, `first_order_distance_tier_certified` |
| item 5 (`K_2'` versus `K_2^+`) | §5 | `k2prime_versus_k2plus` |
| item 6 (checker, gate fields, controls) | §§6.2, 6.5 | `gate_fields_exported`, `ay1_gate_fields_and_verdict`, the 21 control ids, `error_ledger_itemized`, `contract_wording_defects_recorded`, `report_item_and_control_map` |
| contract and premise binding | header | `contract_snapshot_sha256`, `premise_inventory_bound` |
| `missing_incoming_stars` | §6.5 | `missing_incoming_stars` |
| `full_original_wilson_cover` | §§1.1, 6.5 | `full_original_wilson_cover` |
| `wrong_delta_alpha_hbar_clock` | §§1.1, 6.5 | `wrong_delta_alpha_hbar_clock` |
| `vector_versus_scalar_centering` | §§4.2, 6.5 | `vector_versus_scalar_centering` |
| `first_order_mean_charged` | §§4.4, 6.5 | `first_order_mean_charged` |
| `tau_scaling_exponent` | §6.5 | `tau_scaling_exponent` |
| `changed_model_relabelled` | §6.1 | `changed_model_relabelled` |
| `coherent_evidence_tampering` | §6.5 | `coherent_evidence_tampering` |
| `insufficient_verdict_retained` | §6.6 | `insufficient_verdict_retained` |
| `exact_arithmetic_admission` | §§4.2, 6.4 | `exact_arithmetic_admission` |
| `root_n_misuse` | §§4.2, 6.4 | `root_n_misuse` |
| `no_priority_or_continuum_claim` | header, §6.2 | `no_priority_or_continuum_claim` |
| `topology_named` | §6.1 | `topology_named` |
| `two_families_named` | §1.1 | `two_families_named` |
| `subsequence_versus_whole_sequence` | §§1.5, 3.2 | `subsequence_versus_whole_sequence` |
| `local_closeness_not_uniqueness` | §§1.3, 3.2, 4.4 | `local_closeness_not_uniqueness` |
| `common_clock` | §3.3 | `common_clock` |
| `tier_mixing_rejected` | §§4.2, 5 | `tier_mixing_rejected` |
| `not_uniform_in_a` | §6.1 | `not_uniform_in_a` |
| `lower_bound_is_static_not_dynamic` | §4.4 | `lower_bound_is_static_not_dynamic` |
| `obligations_table_complete` | §2 | `obligations_table_complete` |

### 6.8 Limitations

1. **Scope.**
   - Covered: only the zero-selected patterned family, the cover `R`, fixed spacing and `|tau|<=10^-8`, with the two named families on centered cubes, `N>=2`.
   - Not covered: literal vertex boxes, periodic or orthant boxes, nonzero selected triples, the uniform route-B model, weak coupling and the continuum.
2. **Inherited without re-proof.** The following are bound through the AY1 gate:
   - AM2's majorant, fixed point, exclusion and cutoff passage;
   - AV1's split and cutoff-vector removal;
   - AY1's F13 decomposition and F14 items;
   - AQ1's compactness and extraction;
   - the I1 dictionary.

   SU(2) Haar orthogonality and the spectral theorem are standard. Nachtergaele–Sims, the Yarotsky theorem, and HTW- and Dobrushin-type conditions are only named as candidate routes.
3. **Not new.** The tier is not a new result: AY1's forward, reverse and skeptic already wrote it down. AY2 certifies it under its own contract with a re-verified rank-two structure.
4. **The witness** of §3.2 is a density matrix on `H_R`, not a constructed limit. It shows what the admitted bounds leave open, nothing more.
5. **The constants are upper bounds**, apart from the certified lower end `L`. `K_2'` is 99.99% the generic AM2 majorant.
6. **Correlation.** This is a single producer, and all agents are correlated model agents. The skeptic's independent derivation is the second admission input.
7. **Priority.** Scientific priority is unverified.

**Methodological lenses** (modern use of the snapshotted skills):
- **Newton, analysis before synthesis.** The obligations table names what the observations, here the one-state balls, cannot identify, before any route is proposed.
- **Tesla, complete accounting.** The witness is checked against every admitted constraint, not just the one being discussed.

No historical figure endorses anything here, and no historical or occult material supplies a premise.

### 6.9 Reproduction

```bash
python3 -B research/round32/forward/ay2/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/forward/ay2/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round32/tools/freeze.py verify research/round32/forward/ay2
```

`check.py` verifies the contract sha256 before any evaluation, and it records its own sha256 before evaluation. It writes `results.json` and `source-manifest.json`; the manifest records the sha256 of `check.py`, `report.md`, every `inputs/` file and `results.json`. AY2 is investigation 8 of 10 in Round32. This producer executed only the forward statement of AY2.
