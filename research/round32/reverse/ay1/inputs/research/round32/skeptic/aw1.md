# AW1 skeptical review (post-comparison)

**Verdict: accepted_within_scope, sub-label `static_not_dynamic`.** Both routes prove the three results:
- the parity theorem, from a per-link Z_2 centre grading, which is the Peter–Weyl multiplicity count;
- the flip lemma with its conditions;
- the first-order coefficient `omega_tau(W)=+tau/144+r(tau)`.

Both itemize an exact-tier `K_2^+` that is uniform in volume. The three exact-tier values are:

| Source | `K_2^+` |
|---|---|
| forward | ≈3354.6383 |
| reverse | ≈3354.4994 |
| skeptic | ≈3354.8032 |

All three are valid upper bounds, and all three give `tau_AW2=10^-8` under the frozen rule, with sign margin about 207. The crude tier (≈7.9375e6) fails at the cap and is retained. There are **no blocking issues**. No enclosure or sign of `omega(W)` is admitted, and no dynamical statement follows.

**Standing.** I am a model-agent skeptic with correlated ancestry: the same model family as the advisor, the lenses and both producers. My triage and loop-3 sign-off seeded the parity and flip mechanism, and the forward read my triage and loop-2 notes as declared premises. This is not human peer review or formal verification. Human project author: Hruday N M (BUNZEEY).

**My pre-comparison package is unchanged.** It contains:
- `aw1-independent-derivation.md`;
- `aw1_check.py` (79 checks, all 30 controls);
- `aw1-contract-review.md`;
- `aw1-independent/results.json`.

Its hashes match `aw1-independent-freeze.json`. It was committed (`7220ba6`, 23:29:16Z) before the forward (`88c4e36`, 23:33:56Z) and reverse (`857101c`, 23:37:17Z) commits.

**This review adds:**
- `aw1_postreview_check.py`: 65 exact checks, including 30 source-edit mutation receipts;
- `aw1-postreview/results.json`: byte-identical under normal and `-O` Python, sha256 `c656f267…0c6a`;
- `aw1-replays.json`.

## What is proved, with quantifiers

**Model.** The AM2/AQ1 zero-selected patterned family:
- SU(2) Kogut–Susskind form on Z^3 at fixed spacing, with coarse 24-link factors;
- selected triple exactly `(0,0,0)`, so the reference is the Haar product;
- whole stars `phi_b=-(tau/3) sum W_f` in `delta=alpha/8` units;
- both signs of `tau`, with `|tau|<=10^-8`;
- centered whole-star boxes `Lambda_N`, `N>=2`, open (no periodic identification, no frozen or gauge-fixed links);
- the original xz Wilson loop `W` with cover `R={0,e_z}`;
- clock `s=alpha t_E/hbar`, `G=H/alpha`.

**1. Parity theorem (finite boxes).** The statement holds for every `N>=2` and every on-site cutoff. The τ-derivatives at `tau=0` of the following all vanish:
- `omega_N(W^2)`;
- `c_N(theta)=<chi,e^{i theta(G-E)}chi>`, for every real `theta`;
- `C_N(s)=<chi,e^{-s(G-E)}chi>`, for every `s>=0`.

Each term vanishes separately: the state term (`c^(1)` against `W^2 Omega_0` and against `W alpha^0_theta(W) Omega_0`), the Duhamel term, the energy term, and the vector-centring term. The ingredients:
- **Haar moments.** `E[W]=E[W^3]=0`, `E[W^2]=1/4`, `E[W^4]=1/8`, and `E[W^2 W_f]=0` for every omitted `f`, including `f=W`.
- **No return to energy 24.** `P_24 V W Omega_0=0`. The `f=W` component is `(1/4)Omega_0` at energy 0 plus spin-one content at energy 64. On `Lambda_2`, the odd-link sets `W△f` have sizes 0, 6 and 8 (1, 10 and 1333 faces), never 4.
- **Multiplet.** The first-order splitting of the **gauge-invariant** energy-24 multiplet `span{W_g Omega_0}` is zero. Both producers restrict this to the invariant multiplet and do not claim it for the full energy-24 eigenspace. That restriction is correct.

**Conclusions from item 1.**
- `C_N(s)=e^{-3s}/4+O_N(tau^2)`. The `tau^2` constant is **explicitly unbounded**: it is not uniform in `N`, and no AQ-level second-order statement about `C(s)` is admitted. In AQ limits only the evenness from item 2 holds.
- `omega(W^2)=1/4+O(tau^2)`, with supplementary uniform constants. These are not targets, and the free value lies inside them.

**2. Flip lemma (conditions).**
- **Odd intersection.** `E={(p,x):p_y even}∪{(p,y):p_z even}∪{(p,z):p_x even}` meets every plaquette of Z^3 in 1 or 3 links.
- **The operator.** `U_E=prod_{e in E} Gamma_e` commutes with every Casimir and every original endpoint gauge action. It fixes `Omega_0` and maps `W_f` to `-W_f` for every plaquette.
- **Hamiltonian identity.** `U_E H_N(tau,kappa) U_E^*=H_N(-tau,-kappa)`, including cutoff compressions, where `Q_L` maps to the cutoff of `h_b(-kappa)`.
- **Finite boxes at `kappa=0`.** `omega_{N,-tau}(W)=-omega_{N,tau}(W)`. `omega_N(W^2)`, `C_N` and `c_N` are even in `tau`.
- **AQ limits.** `S(-tau)=S(tau)∘alpha_E` as whole sets of subsequential limits. Pointwise antisymmetry holds only along a common subsequence.
- **Exclusions.** No `O(tau^3)` remainder follows from oddness. No τ-antisymmetry via `U_E` holds at `kappa≠0`. Odd periodic sides and frozen or gauge-fixed links are excluded.

**3. First-order coefficient.** Under I1.5 with the AV1 creation convention `c^(1)=L_0=-(tau/72) sum W_f Omega_0` and `psi=e^{-C}Omega_0`:

`omega_tau(W)=-2Re<W Omega_0,c^(1)>+O(tau^2)=+tau/144`.

Only `f=W` contributes. At the cap the first-order value is `±1/14400000000` at `tau=±10^-8`.

**4. Remainder.** `|omega(W)-tau/144|<=K_2^+ tau^2`, uniformly in `N`, the cutoff and every AQ1 subsequential limit. This is at the exact tier: `t<=T=(49|tau|/144)/(1-352J)`, `rho=352JT`, `J=28|tau|`.

## Exact numbers re-derived (my own Fraction code)

**First-order coefficient.** Three routes all give `+1/144`:
- the sign chain: `c^(1)` per face is `(-1/3)/24=(-1/24)/3=-1/72`, and `-2·(-1/72)·(1/4)=1/144`;
- two-level Rayleigh–Ritz in alpha units: `<e,VOmega_0>=-tau/48` with `e=2W Omega_0`, gap 3, `eps*=tau/144`;
- the one-plaquette series (a finite graph): `<W>=tau/144+0·tau^2-5tau^3/11943936+0·tau^4+289tau^5/6604518850560`, with `E_2=-tau^2/6912`. It is identical at truncations 10 and 14 and matches both producers term for term. The forward reports energies in normalized units (×8).

**K_2 at the exact tier (`tau=10^-8`, every entry exact; the table shows values divided by `tau^2`):**

| term | forward | reverse | skeptic (pre-comparison) | minimal form I accept |
|---|---|---|---|---|
| am2_remainder `rho=352JT` | 3354.108358 | 3354.108358 | 3354.108358 | same |
| straddling | `T(6a+rho)` 0.014191 | `T(6a+rho)` 0.014191 | `T·T` 0.115812 | `T(6a+rho)` |
| two_creation | `(33a+rho)^2` 0.052533 | same 0.052533 | `T^2` 0.115812 | `(33a+rho)^2` |
| density | `(2T+T^2)^2` 0.463247 | `(82a+2rho+(33a+rho)^2)^2` 0.324343 | `(2T+T^2)^2` 0.463247 | `min(eps)^2` |
| normalization (3rd order) | `a eps^2` 3.2e-11 | `(eps+eps^2)eps^2` 1.8e-9 | `a eps^2` 3.2e-11 | `a min(eps)^2` |
| **K_2^+** | **3354.638329662** | **3354.499425867** | **3354.803229462** | 3354.499425865 |

Here `a=|tau|/144`. The exact rationals:
- **Forward:** `81104877995836618199905135109761286809699489/24176936535511801466930759024724079017984`.
- **Reverse:** a 114-digit numerator; its outward `10^-40` ceiling is `33544994258669290845093439980837832702606211/10^40`.
- **Skeptic:** `81108864767825329926713064490531229475390625/24176936535511801466930759024724079017984`, with outward `10^-12` ceiling `3354803229461691/10^12`. It equals, exactly, the forward's labelled variant `unpinned_t_bounds`.

Every exported term equals my recomputation of its producer's formula exactly.

**Why the three values differ.**
- **Rounding grid.** Forward and reverse ceil to `10^-40`; the skeptic ceils to `10^-12`. No grid was preregistered, and the rounding changes no decision.
- **Straddling and pair terms (skeptic minus forward = 0.16490).**
  - Both producers pin the straddling pairing to the **6** faces that strictly contain R (owner sets `{0,e_x,e_z}` ×2 and `{0,e_y,e_z}` ×4), each paired with an outside excitation of amplitude at most `T` (lemma F14/R15).
  - My pre-comparison headline charged the conservative `t·t` instead, without the count.
  - Both producers pin the two-creation term to the **33** single-site faces at each site of R. I charged `t^2`.
- **Density term (forward minus reverse = 0.13890).**
  - The forward uses AV1's `eps=2T+T^2`.
  - The reverse pins `eps` to the **82** faces meeting R: `eps=82a+2rho+(33a+rho)^2`. This is the AV1-reviewed labelled 82-face refinement, now applied inside the density term. It is sharper because `2T≈98a>82a`.
  - The reverse's normalization charge `(|X|+|Y|)e^2<=(e+e^2)e^2` is looser than `a e^2` (the leading term is exactly `tau/144`, so only `a e^2` is needed), but it is still valid.

**Validity.** I accept the minimal form in the last column:
- `rho` bounds `||(c-c^(1))_R||` through the anchored norm;
- the multiplier is `2||W Omega_R||=1`, because only `c_R` overlaps `W Omega_R`;
- `|<delta,W delta>|<=e^2` with `e<=min(eps_F,eps_R)`;
- the normalization term is bounded by `a e^2/(1+e^2)`.

Every term of all three itemizations is at least the corresponding minimal term, so **all three are valid exact-tier upper bounds**. The ordering is skeptic > forward > reverse > minimal.

**Further checks.**
- **Scaling.** Each `K_2(tau)` is nondecreasing in `|tau|` (checked at `tau/10`, `tau/100` and `tau/1000`). Each ratio `B(tau)/B(tau/100)` is 10000.98, which is quadratic.
- **Minus `tau`.** The `-tau` ledgers equal the `+tau` ledgers. They are a replay, not evidence for the flip lemma.
- **AV1 binding.** The forward's `eps` reproduces the AV1 gate `D_ii` exactly.
- **Crude tier (`t_c=592|tau|`).**
  - Forward and skeptic: `1937877026146766159414097129/244140625000000000000` (7937544.29909).
  - Reverse: 7937560.89731. The difference is the normalization charge only.
  - Both fail `1/288` at the cap (sign margin 0.0874885). The rule would give `10^-10`, which is information only.
- **`omega(W^2)` supplementary constants (valid, not targets).** Forward 3354.567, reverse 1677.331, skeptic 1677.518. The forward charges `2rho` and all 72 straddling faces, which makes it conservative by a factor of about 2.

**AW2 rule** (read from the contract: largest `10^-k`, `k>=8`, with `K_2^+tau<=1/288`):

| K_2^+ | `K_2^+tau` at the cap | `tau_AW2` | sign margin `1/(144K_2^+tau)` | ratio to `1/288` |
|---|---|---|---|---|
| skeptic 3354.8032 | 3.35480e-5 | `10^-8` | 207.0000524 (floor `41400010489/200000000`) | 103.50003 |
| forward 3354.6383 | 3.35464e-5 | `10^-8` | 207.0102277 | 103.50511 |
| reverse 3354.4994 | 3.35450e-5 | `10^-8` | 207.0187996 | 103.50940 |

- **Robustness.** Every exact-tier `K_2^+<=10^8/288≈347222` gives `10^-8`.
- **AV1 compatibility.** `D_ii≈1.3612e-8>=tau/144+K_2^+tau^2` holds for the largest value.
- **The reverse's "margin ≈103.5".** This is the ratio to the `1/288` threshold. The contract's sign margin is `1/(144K_2^+tau)≈207.02`, which the reverse also reports.

## Route differences

**Parity.**
- Forward: per-link grading `Pi_e`, with an explicit energy-content argument for `W_f W Omega_0` (energies 0–64 in steps of 16, `{36,52}`, 48).
- Reverse: the same grading, but the triple statement `E[W_gW_fW_h]=0` uses the flip set itself: `E` meets `g+f+h` oddly. It also enumerates 95,284 triples.
- Mine: the grading plus direct `S^3` polynomial integration over all 82 faces meeting R.

All three agree on the moments through `n=8` and on the pairings. The contract's named cross-check (the free z link, so `W` is Haar-distributed) is carried by the free-link sphere moments in both producers.

**Flip set.**
- Forward: parses `E` from the contract and enumerates all 24 residue classes, the 49 faces of seven factors at both z-parities, and the whole `N=2` box.
- Reverse: **reconstructs** `E` before parsing. Exactly two of the 27 one-coordinate rules are odd on every plaquette: the cyclic `E` and the anti-cyclic `E'`. These differ by the coboundary of `g=p_xp_y+p_yp_z+p_zp_x mod 2`, a centre gauge transformation. I verified the count (2 of 27) and the coboundary identity link by link.
- Both reject `E` minus one link (4 even plaquettes), odd periodic sides and a spin-one term.

**First-order sign.**
- Forward: sign chain, a two-dimensional Rayleigh–Ritz, and a normalized one-plaquette fixture.
- Reverse: the `psi^(1)` versus `L_0` convention, an alpha-unit fixture, and exact `Q(sqrt D)` ground values at both signs.

**K_2.**
- Forward: the triangle anchored norm.
- Reverse: a reverse analysis, from the desired quadratic remainder back to the missing outside-excitation lemma (R15), plus a four-site creation-algebra fixture auditing the decomposition identity.

## Contract item-3 sign shorthand (wording defect, non-blocking)

Item 3 writes `omega_tau(W)=2<W Omega_0, c^(1)>`. With the AV1-admitted `c^(1)=L_0=H_0^{-1}PVOmega_0=-(tau/72)sum W_f Omega_0`, the literal display evaluates to **`-tau/144`**. I computed that value exactly, and so did both producers.

The correct identity is `omega=-2Re<W Omega_0,c^(1)>=2Re<W Omega_0,psi^(1)>` with `psi^(1)=-L_0`. Both producers:
- derive **`+tau/144`** with the full sign chain from I1.5;
- record the shorthand as a convention finding;
- reject the literal reading as a damaging mutation (forward: `plus_two_L0_convention_gives_minus_tau_over_144`; reverse: `am2_sign_literal`, `contract_formula_with_am2_c1`).

I recorded the same defect before production (`aw1-contract-review.md`, item 1). It is a wording defect in the frozen contract. It is non-blocking because the derived value is `+tau/144` in both routes. The contract is not amended, and the gate should not repeat the display.

## The modified-flip-set remark (assessed, not admitted)

Both producers record, unclaimed, a set `E*=E xor E''`, where `delta E''` equals the selected-face indicator:
- the forward's `E''` uses x-links with `p_x mod 4 in {0,1,2}` and `p_y mod 4 in {1,2}`;
- the reverse's is a period-8 x/y cochain.

Such an `E*` would meet omitted faces oddly and selected faces evenly, so `U_{E*}H(tau,kappa)U_{E*}^*=H(-tau,kappa)`.

**The combinatorics are correct. I checked them independently:**
- every unit cube has 0 or 2 selected faces, so the selected indicator is a Z_2 cocycle and therefore a coboundary on every box;
- both `E''` have exactly that coboundary on a 17×17×7 fine box;
- both `E*` are odd on omitted and even on selected faces;
- the two `E''` differ by a cocycle (a gauge transformation);
- an exact 3×3 compression onto `{Omega_0, 2W Omega_0, 2W_g Omega_0}` (g a selected face sharing a link with W) gives `D_E H(tau,kappa) D_E=H(-tau,-kappa)` and `D_{E*} H(tau,kappa) D_{E*}=H(-tau,kappa)`.

The finding is also consistent with the selected-face fixtures, mine and the reverse's. There `<W_g>` is unchanged under `tau->-tau`, as `E*` predicts, because `E*` does not flip selected faces.

**The operator consequence at `kappa≠0` is not reviewed.** It needs:
- the on-site operator at a nonzero triple to contain only Casimirs, selected face traces and scalars. That is the I1.3 strip form, with `H_strip` inherited from A1, which neither producer read and I did not review;
- cutoffs that are spectral projections of `h_b(kappa)`;
- the triple held fixed independently of `tau`;
- a unique ground state and AM2 applicability with the non-Haar reference (AT4 F01 warns that Haar is not the ground there).

**Relation to the selection note.** The remark does **not** contradict the contract or the control `flip_breaks_at_nonzero_kappa`, both of which concern `U_E`. My own loop-3 condition read "This gives antisymmetry in tau only when kappa=0", which is a statement about `U_E`. The selection note paraphrases it as "antisymmetry in tau holds only at the zero selected triple", without the `U_E` qualifier. Read literally, as a statement about `omega(W)` itself, that sentence is **too strong** if the remark survives review.

`selection-aw1.md` is historical and must not be edited. The gate should record, in a new file, the qualified wording: "via `U_E`, antisymmetry holds only at `kappa=0`". Nothing at nonzero triples is admitted. The remark would need its own contract, since it is a model change.

## Review against the eight required items (both producers)

1. **Parity theorem: complete in both.**
   - The state, Duhamel, energy and vector-centring terms each vanish separately.
   - `E[W^3]=0`, `E[W^2W_f]=0` including `f=W`, `E[W^2]=1/4`, `E[W^4]=1/8`.
   - The `f=W` identity component is kept.
   - The multiplet statement is restricted to the gauge-invariant multiplet.
   - The `C(s)` constant is explicitly unbounded and not uniform in `N`.
   - The named free-link cross-check is present.
2. **Flip lemma: complete in both.**
   - The odd-intersection enumeration is full: all three orientations; the 49 faces of factors at both z-parities (forward: seven factors; reverse: factors 0 and `e_z`); whole boxes.
   - The commutation facts, the cutoff compressions, the `(tau,kappa)->(-tau,-kappa)` identity, the whole-set AQ statement and the absence of an `O(tau^3)` claim are all present.
   - The `kappa≠0` positive demonstrations and rejections are present.
   - Reverse wording: it says `U_E` "commutes with every on-site spectral cutoff" and "fixes `P_R`". That holds at `kappa=0`; at `kappa≠0` those objects map to their `-kappa` versions, as the forward states with `Q_L'`. This is non-blocking.
3. **Coefficient.** `+tau/144` in both, with the wrong-face control (the 81 other faces meeting R, and the 9 others with owner set R, contribute zero) and the orientation control (every omitted class at anchor 0 in xy, xz and yz gives `+tau/144`; reversal invariance).
4. **K_2.**
   - Itemized, with every prereg term and its tier named, and tier mixing rejected.
   - The pins 15/{1×5,2×3,3×2,4×3,10×2}/82/16 are derived from the I1 snapshot in both, and I re-derived them: 49, 10, 6, 72=42+30, 33+33.
   - `||W Omega_R||=1/2`, the multiplier is 1, and the conservative ×4 variant is labelled (forward 13416.96, reverse 13416.82).
   - `f=W` is separated from the 20 others at its anchor (9 inside R, 6 strictly containing R, 5 single-site).
   - The normalization term is third order.
5. **Feasibility.** `K_2^+tau<=1/288` at `10^-8` in both; `tau_AW2=10^-8`; no enclosure is admitted.
6. **Consistency.**
   - The sign flip is shown with signed values and signed fixtures, not only magnitudes.
   - The AV1 bound is compatible.
   - Haar parity is computed from exact character tables. Neither producer uses sympy or floats in the admission path.
7. **Checkers.**
   - **Forward:** 41 checks, 68 rejected mutations.
   - **Reverse:** 57 checks, 107 rejected mutations.
   - All 30 control ids are damaging mutations in both.
   - Flags in both producers:
     - false: `continuum_claim`, `uniform_wilson_claim`, `resolved_interaction_shift`, `scientific_priority_verified`, `third_order_remainder_claim`;
     - true: `first_order_parity_claim` (item 1 is complete) and `flip_lemma_claim`.
   - The forward also sets `omega_W_enclosure_admitted`, `sign_of_omega_W_admitted`, `euclidean_node_certified`, uniqueness, rate and whole-sequence flags false.
   - Replays are byte-identical, and both freezes use `freeze.py`.
8. **Premises.**
   - The reverse inputs are exactly AGENTS.md, the contract and the 29 shared premises: 31 files, and none of triage, loop-2, deliberation, the forward-only premises, forward AW1 or skeptic AW1.
   - The reverse derives the parity theorem and the flip lemma from the character structure. Because the shared premises state the flip idea (both loop-3 sign-offs, `selection-aw1.md`, `skeptic/av2.md`), its independence is limited to its routes, reconstruction and code (contract-review item 7).

**Contract binding.**
- Both checkers verify the snapshot's sha256 before parsing, and both read `1/288`, the rule and the reference `0 and 1/4` from it. The forward records `target_read_from_contract=1/288` and `reference_values_read_from_contract=[0,1/4]`; the reverse records `read_from: contract preregistration.target`.
- A byte edit without a rehash aborts both. A coherent rehashed edit of the reference to `1/3` aborts both on semantic validation.
- A coherent rehashed edit of the target to `1/144`:
  - is **rejected by the reverse**, which ties the threshold to half the derived `1/144`;
  - is **recorded by the forward**, which reads `1/144` and completes. That shows the value is read from the snapshot and not typed in, but the forward has no semantic tie to the coefficient.

  A rehash requires editing `check.py`, which `freeze.json` and the recorded `check.py` sha256 bind, so this is non-blocking.

**Reads.**
- **Reverse.** It read the AV2 forward report and `skeptic/av2.md` only partially (a keyword search plus my "advice for AW1" section). Both are declared shared premises, so this is allowed. It also read portions of `reverse/av1/check.py` and the line count of `reverse/av2/check.py`, for style only.
- **Forward.** Undeclared, disclosed reads: `tools/README.md` and `freeze.py`, AV1 forward `check.py`, and two assistant scripts, named and not imported. The modern assistant's `flip_parity_k2.py` holds only the old loop-2 `K_2` tiers (1.65e7, 1.88e4, 1.10e4), not the AW1 formula.
- **Scratchpad (N1 below).** Neither producer says whether it read the shared scratchpad, which my pre-comparison package asked them to state.

## Replays, closures and isolation

`replay_loop.py aw1` produces the same output under normal and `-O` Python. It verifies both closures, compares every premise snapshot with its repository source, and replays each producer under normal and `-O` Python into fresh external directories. All four runs reproduce `output/` byte for byte:

| Output | sha256 |
|---|---|
| forward `results.json` | `289e8ba3…6f54` |
| reverse `results.json` | `1b1f3bf5…3ce8` |

`freeze.py verify` returns `verified` for both. The closures have 39 files (forward) and 35 (reverse).

**Mutation harness.**
- Unmutated copies reproduce the frozen `results.json` exactly.
- **25 source edits abort** at the intended check:
  - first-order sign flipped;
  - x-links keyed to `p_z`;
  - density term dropped;
  - multiplier 4 unlabelled;
  - `E[W^4]` changed;
  - AW2 grid start shifted;
  - third-order flag set true;
  - crude constant used as the headline;
  - τ-antisymmetry allowed at `kappa≠0`;
  - contract byte change;
  - rehashed reference `1/3`;
  - undeclared input;
  - rehashed target (reverse only).
- **Four silent value edits** (forward density /4, forward pair /9, reverse density pinned to 49 faces, reverse pair /9) run to completion in the producer checkers, which compute only their own formulas. My term-by-term validator rejects all four, and so would the cross-producer comparison.

## Blocking issues

None.

## Non-blocking findings

**N1. Undisclosed shared-scratchpad use.** The shared session scratchpad root holds files written between 23:14Z and 23:20Z, before either producer commit, whose content matches:
- **the forward:**
  - `k2.py` holds exactly the forward's `K_2` and `K_W2` formulas;
  - `estar.py` holds the forward's `E''` remark;
  - `plaq.py` holds its normalized one-plaquette fixture;
- **the reverse:**
  - `rs.py` holds the alpha-unit one-plaquette series;
  - `fixture.py` holds the four-site creation-algebra fixture, dimensions 3,3,2,2.

The forward's `k2.py` (23:17:31Z) overwrote my own pre-comparison scratch `k2.py` at the same path. That is the overwrite my derivation disclosed. Whether any agent read another's scratch file cannot be determined from the files.

The routes and code differ materially:
- two different `E''` constructions;
- two different density `eps`;
- different fixtures.

Independence is therefore not refuted, but the isolation verified here covers the **repository inputs only**. Future contracts should require private per-agent scratch folders and a scratch-read disclosure line.

**N2. Contract item-3 sign shorthand.** See the section above.

**N3. Selection-note wording.** "Only at the zero selected triple" should be read as "via `U_E`". See the remark section.

**N4. The reverse's "margin ≈103.5"** is the ratio to `1/288`. The contract's sign margin is ≈207.02, and the gate should quote `1/(144K_2^+tau)`.

**N5. The forward's `K_W2≈3354.57`** is valid but about twice the reverse's 1677.33, because it charges `2rho` and all 72 straddling faces. It is supplementary, not a target.

**N6. Reverse κ-wording.** The reverse's commutation and `P_R` wording holds at `kappa=0` only (item 2 above).

**N7. The forward's missing semantic tie of the target to the coefficient.** A rehashed `1/144` target is recorded rather than rejected. It is protected by the closure hash.

**N8. Producer checkers do not pin individual term values.** Silent undercounts are caught only by the cross-producer and skeptic comparison. AW2's checker should bind `K_2^+` to the gate's exact rational rather than recompute it.

**N9. The modern loop-3 sign-off's "direct remainder is O(tau^3)" sentence** is used by neither producer (the reverse says so explicitly) and must not be admitted.

## Limitations

- **Scope.** Only this family, the cover R, fixed spacing and `|tau|<=10^-8`. Nothing transfers to nonzero selected triples, uniform Wilson theory, weak coupling or the continuum.
- **Parity.** A finite-volume Taylor statement for `C(s)` and `c(theta)`, with the τ² constant explicitly unbounded. In AQ limits only set-level evenness holds.
- **Flip lemma.** It needs open boxes and `kappa=0`. The `kappa≠0` identity rests on the inherited strip-operator form.
- **Remainder.** `K_2^+` is an absolute upper bound. It gives no sign of `r(tau)` and no third-order remainder. The AM2 generic majorant `352JT` is 99.98% of it.
- **Inherited without re-proof:**
  - AM2's fixed point, majorant, gaps and ground uniqueness;
  - AV1's product split, anchored-norm tier, cutoff removal and AQ passage;
  - AQ1's construction and dynamics;
  - the I1 dictionary.

  Kato analytic perturbation theory and Peter–Weyl are cited, not machine-checked.
- **Fixtures** are finite graphs or finite algebras, `transfers_to_aq:false`.
- **Independence** is limited to routes and code, because the premises share the mechanism and the scratchpad channel (N1) is unaudited.
- **Priority.** Scientific priority is unverified.

## Advice for AW2 (planning only)

1. **Bind the largest valid exact-tier value.** That is the skeptic's `K_2^+=81108864767825329926713064490531229475390625/24176936535511801466930759024724079017984` (≈3354.80322946), or its outward ceiling `3354803229461691/10^12`.
   - It is the forward's exported labelled variant `unpinned_t_bounds`, exactly.
   - It uses only `T`, `rho` and `eps=2T+T^2`, with no 6-, 33- or 82-face refinement, so it stays valid even if every refinement were disputed.
   - It dominates the forward (3354.6383) and the reverse (3354.4994).

   If the gate prefers a producer headline, the forward's 3354.6383 is the larger of the two.
2. **`tau_AW2=10^-8` exactly** (the cap), by the frozen rule, whichever valid value is bound. The sign margin at the cap is `1/(144K_2^+tau)=42981220507576535941210238266176140476416/207638693805632844612385445095759947457≈207.00005`, with directed floor `41400010489/200000000`.
   - The implied enclosure `tau/144 ± K_2^+tau^2` is ≈`6.9444e-11 ± 3.355e-13`. This is AW2's to certify; it is not admitted here.
3. **The `-tau` enclosure** is the flip image of the `+tau` one, for paired states along a common subsequence. It is not a second confirmation.
4. **Checker bindings.** AW2's checker should:
   - read `K_2^+`, `tau_AW2` and `D_ii` from the hash-checked AW1 and AV1 gates;
   - reject any recomputed or smaller `K_2`;
   - carry the `static_not_dynamic` label;
   - make no dynamical, mass-gap, third-order, uniqueness or rate claim.
