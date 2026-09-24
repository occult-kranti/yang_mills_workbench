# AZ2 producer recipe -- concrete spec check

Round32, sub-round 2, modern (Penrose/Feynman) lens, assistant-2. Status:
assistant/coder planning note. Counts ZERO research loops; nothing here is a
contract, gate, freeze or admission artifact. It is a concrete, executable
recipe proposal for AZ2's actual producer (sub-round 5), grounded in code
that already runs (`research/round11/solver/two_plaquette.py`) and in the
timing rehearsal this sub-round's `rayleigh_rehearsal.py` just ran on the
same-sized matrices. Read alongside `research/round32/contracts/az2.json`
(draft), `research/round32/advisor/aw1-gate.json`, and
`research/round11/advisor/advisor.md`.

## 0. What AZ2 is and is not

AZ2 is a **different, finite-graph model** (`model_is_finite_graph:true`,
`transfers_to_aq:false`, per the contract): the Round11 two-plaquette patch
(two adjacent open squares sharing one link, seven links, six Gauss
constraints), not the Z^3 lattice AW1/AV1/AV2 work on. Its purpose (contract
`selection_reason`) is to show what a computable, exactly-solvable truncated
model's first- and second-order Wilson-loop coefficients actually look like,
as a **labelled comparison**, never a transfer, to the Z^3 result `+tau/144`
(AW1 item 3) or to `K_2^+` (AW1 item 4). Every output must carry
`no_transfer_to_aq:true` and `fg_coefficients_not_fitted:true`.

## 1. Graph, gauge-invariant basis, cutoff

Already fully specified and implemented in
`research/round11/advisor/advisor.md` sections 1-5 and
`research/round11/solver/two_plaquette.py`; AZ2 reuses it, not re-derives it:

- **Graph.** Six vertices (TL,TM,TR,BL,BM,BR), seven oriented links
  (h1,h2,h3,h4,vL,vM,vR), six independent Gauss constraints. Tree gauge on
  `T={h1,h2,h3,h4,vM}` reduces the physical Hilbert space to
  `L^2(SU(2)^2,dU dV)^{Ad,diag}` (advisor.md eq. Q1), coordinatized by the
  compact body `Omega = {(x,y,z): |x|,|y|<=1, D(x,y,z)>=0}` (eq. Q2), with
  the exact rational measure `dmu = (2/pi^2) dx dy dz` (eq. Q3) and exact
  rational moments via eq. Q4 (`two_plaquette.moment`, `haar_x_power`,
  `radial_moment`, all `Fraction`-only, `lru_cache`d).
- **Gauge-invariant basis.** All polynomials in `x,y,z` of total degree
  `<=D`, i.e. `two_plaquette.basis(D)`: monomials `x^a y^b z^c`,
  `a+b+c<=D`. Dimension `binomial(D+3,3)`.
- **Operator.** `K = 4(C_U+C_V)+2 sum_a L_U^a R_V^a` (eq. K1), built exactly
  as `two_plaquette.kinetic` (a differential-operator action on monomials,
  `Fraction` coefficients throughout, verified `K^T=K` inside
  `two_plaquette.matrices`). The full physical Hamiltonian is
  `H = alpha*K + lambda1*(1-x) + lambda2*(1-y)` (eq. H1), assembled by
  `two_plaquette.combine(G,K,MX,MY,alpha,lambda1,lambda2)`.
- **Cutoff.** Per `update-1.md` section 5's binding instruction, the
  contract's generic `j_max` is read as this polynomial-degree cutoff `D`,
  not an SU(2) spin cutoff. **D=6 primary** (dimension 84 = C(9,3)), **D=8
  certified refinement** (dimension 165 = C(11,3)), nested (`P_6 subset
  P_8`), matching `loop2-response.md` section 6 verbatim.
- **Certified tail.** Exact, via `two_plaquette.tail_lower(D, alpha, rho=1)`,
  which returns `alpha * m_{D+1}` with the exact shell-minimum formula
  `m_d = (5/8)d^2 + 2d + (3/8)(d mod 2)` (advisor.md eq. E3), proved as the
  true minimum electric eigenvalue of the first omitted shell (eq. E4:
  `Q_D K Q_D >= m_{D+1} Q_D`), i.e. this **is** the "complete residual over
  all product channels" the contract asks for -- it is not a partial-channel
  estimate, it is the shell's exact minimum, established in closed form by
  advisor.md section 5's monomial-diagonalization argument (every channel of
  the first omitted shell is accounted for, not sampled). At `alpha=1`:
  `tail_lower(D=6) = 45` exactly (first omitted degree 7:
  `m_7 = 5/8*49+14+3/8 = 45`), `tail_lower(D=8) = 69` exactly (`m_9`),
  confirmed live by this sub-round (`python3 -B -c` against the imported
  module, no admission claim made by that confirmation itself).

## 2. Matrix assembly

`bs, G, K, MX, MY = two_plaquette.matrices(D, rho=Fraction(1))`, all exact
`Fraction` (`inner(p,q)` via the eq. Q4 moment formula). `MX[i][j] =
inner(p_i, x*p_j)`, `MY` likewise for `y`; these give the exact rational
matrix elements of the two Wilson-loop-trace observables `x=(1/2)Tr(U)`,
`y=(1/2)Tr(V)` in the monomial basis, reused for both the potential term of
`H` and for evaluating `<W>=<x>` at any trial/Ritz vector via
`v^T MX v / v^T G v` (**not** `v^T MX v` alone, since the monomial basis is
not `G`-orthonormal).

## 3. `tau_FG` normalization dictionary (contract requirement 3)

The contract leaves `tau_FG`'s role in `H_FG` for the producer to fix and
declare explicitly; this is the recipe assistant-2 proposes, chosen to be
the closest structural match to the Z^3 model's own perturbation (AW1
item 3: `phi_b = -(tau/3) sum_f W_f`, a term linear in `tau` multiplying
each plaquette's own Wilson trace):

    H_FG(tau_FG) := K - tau_FG * x         (alpha=1, lambda2=0, lambda1=tau_FG)

i.e. the **same observable** `x = W` whose response is measured also
supplies its own coupling, exactly paralleling the Z^3 setup where the
observed loop `W` is one of the terms in its own perturbing sum. `y`'s
coupling (`lambda2`) is held at 0 so the "other square" stays a spectator,
the finite-graph analogue of the Z^3 loop's non-owner faces. **Declared
control variant** (`vector_versus_scalar_centering`-adjacent, for the
skeptic to require as a sensitivity check, not as the primary result):
symmetric coupling `H_FG^sym(tau_FG) := K - tau_FG*(x+y)`, testing whether
`<x>`'s first-order response changes when the spectator square is also
driven. Both variants must be run and both first-order coefficients
reported; only the asymmetric (primary) one is compared to `1/144`.

**Normalization dictionary (contract requirement 3, exact statement AZ2 must
freeze before seeing results):** the Z^3 first-order coefficient is
`d(omega_tau(W))/d(tau)|_0 = 1/144` in units where the electric term carries
coefficient 1 per link-Casimir-like normalization implicit in AV1/AW1's
`H_N(tau,kappa)`. The FG model's electric term `K` is normalized differently
(eq. K1's explicit `4(C_U+C_V)+2sum L R` combination, not a bare sum of
single-link Casimirs), so the raw FG coefficient `d<x>/d(tau_FG)|_0` is
**not** dimensionally comparable to `1/144` without an explicit conversion
factor. AZ2 must state this factor plainly (e.g. via the free-gap ratio
`free_gap_FG / free_gap_{Z^3 analogue}` or an equivalent declared
convention) and report both the raw FG number and the converted one,
labelling the comparison `consistency, not proof` (contract wording) either
way. This spec check does **not** fix that conversion factor -- doing so is
AZ2's own scientific judgment call, itemized here only so it is not silently
skipped.

## 4. Observable computation at the tau_FG grid (contract requirement 2)

For each `tau_FG` in `{1/1000, 1/100, 1/10}` and each `D` in `{6,8}`:

1. Build `H_FG(tau_FG) = K - tau_FG*MX` exactly (`Fraction`).
2. Seed a seed a trial ground eigenvector via `scipy.linalg.eigh` on the
   floating generalized problem `(H_FG, G)` (float; never admitted),
   round to a rational vector at denominator `10^7` (the same convention
   used throughout this sub-round's `rayleigh_rehearsal.py` and
   assistant-1's `flint_harness.py` self-test).
3. Refine to an **exact** Ritz vector: either (a) Round11's own exact
   rational inverse iteration / `exact_bracket`+`inertia` congruence
   machinery (`two_plaquette.exact_bracket`, already implemented and used
   by `certificate()`), which isolates the exact eigenvalue to a target
   rational width by exact-Fraction symmetric congruence (no floating
   round-off anywhere in the isolation), or (b) the directed
   generalized-Rayleigh/residual bound this sub-round's
   `rayleigh_rehearsal.py` implements and validated (`mu = v^T H v/v^T G v`,
   residual bound `sqrt(r^T G^{-1} r)/sqrt(v^T G v)` via
   `two_plaquette.solve_exact` + `flint_harness.rational_sqrt_bracket`),
   whichever the producer finds gives a tighter width at acceptable runtime
   (both are exact; (a) is Round11's own certified congruence method and
   should be preferred as the primary route per contract admission wording
   "exact rational linear algebra (Fractions) with Ritz plus
   residual/Davis-Kahan or exact shell residual"; (b) is a fast preliminary
   bracket and a genuine independent cross-check of (a) since it uses a
   different exact algorithm (perturbation bound vs. congruence inertia)).
4. Report `<x>(tau_FG) = v^T MX v / v^T G v` exactly, with the eigenvector
   residual converted to an observable error bar via
   `|<x>_v - <x>_true| <= 2 sin(theta) <= 2*(residual bound)/(l_1^B - mu)`
   (`update-1.md` section 5's own stated formula; `l_1^B` from the
   boundary-corrected block `B` of Round11 section 7 / `tail_lower`, exactly
   as `two_plaquette.certificate` already assembles it).
5. Repeat at `-tau_FG` for the sign pair, per this workbench's universal
   convention (both signs evaluated, contract `preregistration.tau.
   signs_evaluated`).

## 5. Derivative at `tau_FG=0` (contract requirement 2, second half)

`tau_FG=0` is **exactly solvable in closed form**, no perturbation needed
for the value: the ground state is the constant function `1` (`K*1=0`
exactly, advisor.md eq. K5), giving `<x>(0) = moment((1,0,0)) = 0` exactly
(confirmed live this sub-round: `two_plaquette.moment((1,0,0)) == 0`) --
this is the FG model's **own free reference**, computed in the same code
path as everything else (contract label `own_free_reference`), not merely
asserted.

For the **derivative**, AZ2's producer has two options, both to be reported:

- **Secant/grid estimate** (cheap, already available from step 4): the sign
  antisymmetry expected of `<x>(tau_FG)` (odd function, by the same
  `x -> -x, tau_FG -> -tau_FG` structural symmetry of `H_FG`) means
  `<x>(tau_FG)/tau_FG` at the smallest grid point `tau_FG=1/1000`
  already estimates the derivative to `O(tau_FG^2)`; report it with an
  explicit, itemized `O(tau_FG^2)` remainder bound (not dropped silently).
- **Exact first-order perturbative solve** (preferred, not yet executed
  here -- flagged as AZ2's own work, not preview-tool work): with `E_0=0`,
  `v_0=` the constant vector, `E_1 = -<x>(0) = 0` (Hellmann-Feynman,
  confirmed exactly as above), the first-order eigenvector correction `v_1`
  solves `K v_1 = MX v_0` in the subspace `G`-orthogonal to `v_0` (Fredholm
  solvability holds exactly because `v_0^T (MX v_0) = <x> = 0`). This is a
  **singular** linear solve (`K` has a 1-dimensional exact null space
  spanned by `v_0`); the standard exact fix is to solve the regularized,
  nonsingular system `(K + G v_0 v_0^T G^T / (v_0^T G v_0)) v_1 = MX v_0`
  by `two_plaquette.solve_exact` (all `Fraction`, no floats), which agrees
  with the true `v_1` on `v_0`'s `G`-orthogonal complement and is
  automatically `G`-orthogonal to `v_0` in the regularized solution (the
  added rank-1 term only acts along `v_0`). Then
  `d<x>/d(tau_FG)|_0 = 2*(v_0^T MX v_1)/(v_0^T G v_0)` exactly. This spec
  check states the method precisely enough to implement directly; it has
  **not** been executed here in exact `Fraction` arithmetic (it is AZ2's
  scientific content, not a zero-loop preview), so no admitted numeric value
  is claimed. As a floating-point-only sanity check of the *recipe itself*
  (not of any number -- this is not even a preview tier, purely a
  did-the-linear-algebra-work check run for this spec document): the
  regularized-solve construction at D=6 gives `d<x>/d(tau_FG)|_0 ~
  0.1666666...`, matching a plain finite-difference `<x>(tau_FG)/tau_FG` at
  `tau_FG=1e-4,1e-3,1e-2` to 5+ digits (apparently `1/6` exactly, consistent
  with `x` lying entirely in the `K`-eigenvalue-3 shell `span{x,y}` of
  advisor.md's table and `<x^2>=1/4`, giving `2*(1/3)*(1/4)=1/6` by the
  standard sum-over-states formula) -- confirming the method is internally
  consistent before AZ2 spends a production loop on the exact-`Fraction`
  version. This number is explicitly **not admitted, not exact, and not a
  labelled preview tier**; it exists only to validate this recipe document.

## 6. Second-order coefficients (contract requirement 4)

Report as **finite-model values only**, explicitly labelled
`fg_coefficients_not_fitted:true` and not compared to `K_2^+`: either (a) a
second finite difference across the `tau_FG` grid (crude, cheap, itemize the
truncation order), or (b) the analogous second-order perturbative solve
(`v_2` from `K v_2 - MX v_1 = E_2 G v_0 + E_1 G v_1`, `E_2` from the usual
second-order formula), which needs the same regularized-solve trick as
step 5 applied one order further. Either way: **no claim about the AQ
model's shift or `K_2`** may be drawn from this number (contract
`claim_exclusions`); it exists purely as "what does the truncated graph's
own second-order term look like".

## 7. Arb preview (contract requirement 5, "Arb cross-check")

Exactly the pattern this sub-round's `rayleigh_rehearsal.py` already
exercised and validated at both D=6 (84x84) and D=8 (165x165): build
`M = solve_exact(G, H_FG(tau_FG))` (exact rational `G^{-1}H_FG`, via
`two_plaquette.solve_exact`, reused verbatim), then
`flint_harness.arb_eig_preview(flint_harness.exact_matrix_from_rows(M),
prec=256)` for the eigenvalue balls of the *same* generalized problem,
UNCHANGED from `flint_harness.py`'s own API (no fork, no reimplementation).
Labelled preview only, per `flint_harness.py`'s own scope statement and this
contract's `admission` field ("python-flint Arb as labelled cross-check
only").

## 8. Labels and controls (contract requirement 5)

Every AZ2 result record must carry, verbatim:
`finite_graph_model_id: "FG(two-plaquette, D, tau_FG, I1.5, gauge-invariant)"`,
`complete_residual_all_channels: true` (true because `tail_lower` is the
exact shell minimum, not a sampled subset -- see section 1),
`certified_representation_tail: true`, `own_free_reference: true` (the
exact `moment((1,0,0))=0` computation of section 5),
`no_transfer_to_aq: true`, `fg_coefficients_not_fitted: true`. The full
`controls` list of `az2.json` (19 entries, including
`missing_incoming_stars`, `full_original_wilson_cover`,
`wrong_delta_alpha_hbar_clock`, `vector_versus_scalar_centering`,
`sign_convention_fixture`, etc.) needs one short itemized sentence each in
the producer's `report.md`, per this workbench's universal control-coverage
convention; several (e.g. `missing_incoming_stars`,
`wrong_delta_alpha_hbar_clock`) are Z^3-model controls that are
**not applicable** here and must be marked so with a stated reason (contract
preregistration's `error_terms_rule`), not silently dropped.

## 9. Matrix-size and runtime estimate

Measured live this sub-round on this container (`rayleigh_rehearsal.py`,
same construction, `alpha=1,lambda1=lambda2=1` -- representative of the
per-grid-point cost since `H_FG` assembly and the Ritz/residual/Arb pipeline
have the same shape regardless of the specific coupling values):

| Step | D=6 (84x84) | D=8 (165x165) |
|---|---:|---:|
| `matrices()` build (G,K,MX,MY) | 0.51 s | 2.0 s |
| generalized Rayleigh + exact residual (one trial vector) | 0.12 s | 0.69 s |
| `solve_exact(G,H)` (for the Arb-comparison matrix) | 0.88 s | 6.5 s |
| `arb_eig_preview` at 256 bits (full spectrum) | 1.2 s | 17.0 s |
| **per-grid-point total (approx.)** | **~2.7 s** | **~26 s** |

AZ2 needs this per grid point **and per sign** (`+-tau_FG`, 3 grid points x
2 signs = 6 evaluations) **and per cutoff** (D=6, D=8) **and per variant**
(asymmetric primary + symmetric control, section 3) -- **24 grid-point
evaluations total**, plus the exact-inverse-iteration refinement pass
(Round11's own `certificate()`/`exact_bracket` congruence route, not timed
here but bounded by the same `matrices()` build cost plus a handful of
`inertia()` calls, each `O(n^3)` exact-Fraction Gaussian elimination --
`n=84` or `165`; `inertia` was not separately timed this sub-round and
should be rehearsed once more before AZ2 commits to a width target,
since exact-Fraction pivoting on numerators/denominators that can grow
during elimination is the one step whose cost is hardest to predict from
matrix size alone). **Estimate: a full AZ2 run (both cutoffs, both
variants, all grid points and signs, Arb previews included) completes in
well under 15 minutes of wall-clock CPU time** on hardware comparable to
this container, with the D=8 Arb-eig calls (`~17 s` each, 12 of them if run
at every grid point/sign/variant, `~3.4 min` total) as the dominant cost;
this is the step most worth pruning first (e.g. running the Arb preview only
at the extreme grid point and at zero, not at every point) if a tighter
budget is needed. **No scaling blocker was found up to 165x165** in this
sub-round's rehearsal.

## 10. Freeze and skeptic replay

Standard workbench pattern (`AGENTS.md`): `two_plaquette.py`'s own
`source_sha256`/`verify_certificate` mechanism already gives AZ2 a
ready-made freeze/replay primitive for anything built from `certificate()`;
the additional `tau_FG`-grid/derivative/second-order layer this document
proposes needs its own `check.py` (per this workbench's universal pattern)
that recomputes every grid point, the zero-point derivative and the
second-order coefficient from the frozen `two_plaquette.py` snapshot and the
frozen contract, and compares byte-for-byte against `output/results.json`.
