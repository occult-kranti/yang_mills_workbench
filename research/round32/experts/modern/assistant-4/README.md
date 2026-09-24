# Round32 sub-round 4 -- modern (Penrose/Feynman) lens, assistant-4

Status: assistant/coder cross-check tools, per `update-3.md` (panel-update-3)
section 6 item 6 (this sub-round's proposed tests, modern share). **These
outputs count zero research loops.** They are previews and cross-checks
only: `sympy`, python-flint 0.9 (Arb) and the Round11 `two_plaquette.py`
solver module are independent, already-frozen libraries reused here BY
IMPORT (never reimplemented, never modified) for comparison and
computation, never for admission. Every number this repository actually
admits was already decided by exact `fractions.Fraction` arithmetic in a
frozen `check.py` inside `forward/`, `reverse/` or `skeptic/` -- most
directly `forward/aw1/check.py`, `forward/ay1/check.py` and
`reverse/ay1/check.py`, both already merged loops of this same round.
Nothing in this directory is imported by any of those, and nothing here
changes a verdict.

Human project author: Hruday N M (BUNZEEY). Run everything with `python3 -B`.

## Files

- `first_order_density_from_c1.py` -- update-3.md section 6 item 1:
  recomputes the first-order reduced density `rho^(1)_R` INDEPENDENTLY
  from the admitted AW1 first-order coefficient `c^(1)`
  (`forward/aw1/report.md`, `advisor/aw1-gate.json`), in four stages: (1)
  enumerates the 82 faces meeting `R={0,e_z}` from the 7 incident anchors
  `R-S` of the zero-selected patterned model by a brand-new anchor-union
  route (not assistant-3's per-site inclusion-exclusion or brute-force box
  scan), finds 10 with owner set exactly `R` and 72 straddling (zero
  `R`-marginal), and cross-checks both against assistant-3's
  `uniform_counts_from_scratch.py` (imported) and against the AY1 forward
  producer's own admitted pins and incident-anchor list; (2) re-derives
  the SU(2) Haar moments `E[W^n]` from first principles via Peter-Weyl
  character theory and the exact SU(2) Clebsch-Gordan fusion rule, both
  as a symbolic `sympy` trig identity (`chi_{1/2}*chi_{1/2}=chi_0+chi_1`,
  etc., and direct symbolic Haar integration against the class-angle
  measure `(2/pi) sin^2(theta) dtheta`) and as an exact-`Fraction` fusion
  iteration, matching the admitted `1,0,1/4,0,1/8,0,5/64,0,7/128`
  digit-for-digit; (3) builds an explicit 11-dimensional orthonormal
  tensor-product basis (one independent SU(2) class-function factor per
  face, truncated to the spins that occur) with a generic
  Clebsch-Gordan-fusion multiplication operator, verifies the 11x11 Gram
  matrix of `{Omega_R, 2 W_f Omega_R}` is the identity, that the operator
  has rank 2 with eigenvalues `+-sqrt(10) tau/144` (`sympy` exact
  eigenvalues of the shape matrix), trace norm `sqrt(10)|tau|/72`,
  `Tr(rho^(1) W)=+tau/144` and `Tr(rho^(1) W^2)=0`; (4) an Arb (256-bit)
  and directed-rational `sqrt(10)` cross-check of the trace norm at the
  cap `tau=1e-8`, matched against the AY1 gate's own preview and
  producer output. Self-test: PASS.
- `k2_prime_from_aw1_items.py` -- update-3.md section 6 item 2: rebuilds
  the R-local trace-norm constant `K_2'` from the AW1 remainder items
  (`T`, `rho=352*J*T`, `a=|tau|/144`) restricted to faces meeting `R`,
  exactly as both AY1 producers itemize it (`forward/ay1/report.md`
  section 5.5, `reverse/ay1/report.md` sections 3.6-3.9), reproduces the
  exact rational
  `966771578474926086618624139557778885954947547760216752246561/72052885697817210754545804931891200000000000000000000000`
  with plain `Fraction` arithmetic (bit-for-bit, and matching both
  producers' `results.json` headline fields), shows the five-item
  decomposition (the AM2 remainder item `4*rho` dominates at
  `99.9918%`, matching the gate's own "~99.99%" language), reproduces
  `K_2^+` the same way and the ratio `K_2'/K_2^+~3.99950`, and computes
  all four labelled variants (sqrt(2) sectors `~9487.945`, directed
  288-majorant `~10978.18`, both combined `~7763.06`, admitted-`eps`
  density `~13417.81`) with an Arb/directed-rational `sqrt(2)` cross-check.
  Self-test: PASS.
- `finite_graph_rehearsal_d8.py` -- update-3.md section 6 item 3: the
  D=8 rerun (dimension 165, one representation-degree cutoff above
  assistant-3's own D=6 rehearsal in `az2_dictionary_calc.py`) of the
  finite-graph rehearsal on the Round11 two-plaquette graph, imported by
  module (never reimplemented, never modified). Computes: (a) the exact
  derivative at zero `d<x>/d(tau_FG)|_0` two independent ways -- assistant-3's
  own regularized-solve method (imported, called at D=8, giving exactly
  `1/6`, bit-for-bit identical to its own D=6 result) and a brand-new
  exact central-second-difference check on the ground energy alone
  (using `E_0(0)=0` exactly and only the module's own certified
  `exact_bracket`/`inertia`), which converges to `1/6` with the expected
  `O(h^2)` discretization pattern; (b) exact-rational RITZ VALUES (never
  a bare floating eigenvector) for `<W>(tau_FG)` at
  `tau_FG in {1/1000,1/100,1/10}` -- AZ2's own preregistered grid -- via a
  Hellmann-Feynman/concavity sandwich built from three certified energy
  brackets per point; (c) a tail-residual discussion from
  `tail_lower(8)=69`; (d) the A2/A3 normalization dictionary
  (`tau_FG:=tau/24`, reused from assistant-3), confirming the D=8 result
  still converts to the admitted `1/144`; (e) a D=4/6/8 timing
  calibration table and full wall-clock timing of every exact-bracket
  call, for the AZ2 contract's own `j_max` feasibility decision.
  Labelled throughout `model_is_finite_graph:true`,
  `transfers_to_aq:false`. Self-test: PASS (total wall-clock 281 seconds).
- `results.json` -- combined machine-readable output of all three
  self-tests plus the planning notes below.

```
python3 -B research/round32/experts/modern/assistant-4/first_order_density_from_c1.py
python3 -B research/round32/experts/modern/assistant-4/k2_prime_from_aw1_items.py
python3 -B research/round32/experts/modern/assistant-4/finite_graph_rehearsal_d8.py
```

All three exit 0 (PASS) as of this writing; each prints its own JSON
report and exits 1 on any failed sub-check. `first_order_density_from_c1.py`
and `k2_prime_from_aw1_items.py` each run in well under a minute (~30s and
~1s respectively). `finite_graph_rehearsal_d8.py` is the slow one: its
13 exact `inertia`-based `exact_bracket` calls at D=8 (165-dimensional
Fraction Gaussian elimination) take roughly 20 seconds each, for a total
wall-clock time of about 281 seconds (4.7 minutes) on this container.

## first_order_density_from_c1.py results

- **Combinatorics.** The 7 incident anchors, derived directly as `R-S`
  (not cited), are `{(0,0,0),(-1,0,0),(0,-1,0),(0,0,-1),(0,0,1),(-1,0,1),
  (0,-1,1)}`, matching the AY1 forward producer's own `incident_anchors`
  list exactly. The from-scratch anchor-union enumeration gives 82
  faces meeting `R`, 10 with owner set exactly `R`, 72 straddling --
  matching assistant-3's two independent methods (imported), the AY1
  forward producer's `face_enumeration_R_local` pins, and (as a set) its
  explicit 10-face label list, with the first-listed face (`xz r=0 s=0`)
  identified as `W` itself, matching AY1's own `wilson_face_index`.
- **SU(2) character theory.** The exact Clebsch-Gordan fusion identities
  `chi_{1/2}*chi_{1/2}=chi_0+chi_1` and `chi_{1/2}*chi_1=chi_{1/2}+chi_{3/2}`
  both simplify to the zero function under `sympy` (a genuine symbolic
  trig-identity check, not a floating check), the SU(2) character
  orthogonality table on `{0,1/2,1,3/2}` is exactly the identity, direct
  symbolic Haar integration of `E[W^n]` for `n=0..4` agrees with the
  exact-`Fraction` Clebsch-Gordan fusion iteration for `n=0..8`, and both
  match the admitted `1,0,1/4,0,1/8,0,5/64,0,7/128` exactly.
- **Operator algebra.** In the explicit 11-dimensional orthonormal basis
  built from these moments, the Gram matrix of `{Omega_R, 2 W_f Omega_R}`
  is exactly the 11x11 identity; the operator's shape matrix has exact
  rank 2 with eigenvalues `{-sqrt(10)/144: 1, sqrt(10)/144: 1, 0: 9}`
  (i.e. `+-sqrt(10) tau/144` and 0 nine-fold once scaled by `tau`);
  `Tr(rho^(1) W)` has exact coefficient `1/144` and `Tr(rho^(1) W^2)` has
  exact coefficient `0`. All four match the AY1-admitted facts exactly.
- **Numeric/Arb.** At the cap `tau=1e-8`, my own directed `sqrt(10)`
  bracket (200-bit exact squaring, reused from assistant-1's
  `flint_harness.rational_sqrt_bracket`) gives a trace-norm bracket whose
  Arb (256-bit) cross-check is contained inside it, and whose upper end
  is below (and within `1e-20` of) the AY1 forward producer's own
  `rho1_R_trace_norm_upper`, confirming AY1's reported upper bound is a
  valid and tight rounding of the same true value this file computes
  independently.

## k2_prime_from_aw1_items.py results

- `K_2'` rebuilt from `T`, `rho=352*J*T`, `a=|tau|/144` alone (never
  citing the report's arithmetic) is exactly
  `966771578474926086618624139557778885954947547760216752246561/72052885697817210754545804931891200000000000000000000000`
  (`~13417.5275439996...`), matching the admitted value bit-for-bit and
  matching both AY1 producers' `results.json` headline `K2_prime` fields.
  `K_2^+` rebuilt the same way (`rho+2T^2+eps^2+a*eps^2`, `eps=2T+T^2`)
  matches the admitted `~3354.80322946` bit-for-bit too, and the ratio
  `K_2'/K_2^+` previews to `~3.9994976`, matching the gate.
- **Decomposition.** The five items' shares of `K_2'` are: `am2_remainder`
  `99.99185%`, `density` `0.00483%`, `straddling` `0.00254%`,
  `two_creation` `0.00078%`, `normalization_third_order`
  `~3.4e-12%`. The AM2 remainder (`4*rho`) dominates overwhelmingly,
  matching the gate's own "dominated (99.99%) by the generic AM2
  majorant" language exactly.
- **Labelled variants**, each Arb/directed-`sqrt(2)`-cross-checked:
  sqrt(2)-sectors `~9487.94517028`, directed 288-majorant
  `~10978.1762675`, both combined `~7763.06332882`, admitted-`eps`
  density variant `~13417.8053515` -- all four matching the reverse
  report's printed previews to at least 4-5 significant figures (and the
  sqrt(2) variant's upper bound matching the forward producer's own
  `K2_prime_orthogonal_variant_upper` to within `1e-20`).

## finite_graph_rehearsal_d8.py results

- **D=8 free facts, live-confirmed** (not cited): `K*x=3x` exactly,
  `<x,x>=1/4`, `free_gap()==3`, `tail_lower(6)=45`, `tail_lower(8)=69`,
  dimension 165 (`C(11,3)`).
- **Derivative at zero:** assistant-3's regularized-solve method, called
  at D=8, gives exactly `1/6` -- bit-for-bit identical to its own D=6
  result (the x-shell is an EXACT eigenvector of `K` at every truncation
  `D>=1`, so this is a D-stability confirmation, not a new derivation),
  Arb (256-bit) cross-checked. A second, brand-new method -- an exact
  central second difference of the ground energy alone
  (`E_0(0)=0` exactly; `<x>_0'(0) ~ -(E_0(h)+E_0(-h))/h^2`) -- gives
  `0.16666665...0.16666667` at `h=1/1000` (bias `2.89e-9` from `1/6`) and
  `0.16666567...0.16666767` at `h=1/10000` (bias `2.89e-11`), an exact
  `O(h^2)` convergence ratio (`0.01` for a `10x` smaller `h`, matching
  `(1/10)^2`). Both brackets contain `1/6`. Note: the CERTIFIED bracket
  width itself widens as `h` shrinks here (the `exact_bracket` width was
  held fixed at `1e-14`, so its contribution scales as `1/h^2`); `h=1/1000`
  therefore gives the tighter net bracket despite the larger bias --
  a genuine numerical trade-off, reported honestly rather than only the
  best-looking number.
- **Ritz values for `<W>(tau_FG)`** (exact rational brackets, never a
  floating eigenvector, via the Hellmann-Feynman/concavity sandwich):
  - `tau_FG=1/1000`: `[0.00016657332755496, 0.00016675999420425]`
    (first-order estimate `tau_FG/6=0.00016666...`, inside the bracket).
  - `tau_FG=1/100`: `[0.0016658265550058, 0.0016674952043117]`
    (`tau_FG/6=0.0016666...`, inside).
  - `tau_FG=1/10`: `[0.01665255834427, 0.016669207867224]`
    (`tau_FG/6=0.016666...`, inside).
  Each point took 3 exact `exact_bracket` calls (~20s each, ~60-63s per
  point).
- **Tail residual.** `tail_lower(8)=69` has no bearing on the
  derivative-at-zero result (that computation is exact and D-independent
  by construction, confirmed above); it bounds the TRUNCATION error of
  the finite-`tau_FG` Ritz brackets above, heuristically of order
  `tau_FG^2/66` (about `1.5e-4` at `tau_FG=1/10`, negligible at `1/100`
  and `1/1000`) -- reported as a heuristic estimate, not a certified
  bound.
- **Normalization dictionary.** `1/6` converted through `tau_FG:=tau/24`
  gives exactly `1/144`, matching AW1's admitted Z^3 first-order
  coefficient exactly, at D=8 as at D=6.
- **Timing / D-scaling** (for AZ2's `j_max` feasibility decision): matrix
  build + one `inertia` call: D=4 (dim 35) `0.067s+0.054s`; D=6 (dim 84)
  `0.81s` inertia (build cached); D=8 (dim 165) `6.49s` inertia (build
  cached). The scaling is close to `O(dim^3)` (time ratio `15.0` vs the
  dimension-cubed ratio `13.8` for D4->D6; time ratio `8.0` vs `7.6` for
  D6->D8). Extrapolating, D=10 (dim 286) is roughly `34s` per
  `exact_bracket`/`inertia` call and D=12 (dim 455) roughly `136s`
  (~2.3 minutes) per call. **Caveat, stated
  honestly**: AZ2's own contract parametrizes its cutoff as a
  representation label `j_max` (worked examples `3/2`, `2`), not as
  Round11's polynomial degree `D` (dimension `C(D+3,3)`); this file
  reports feasibility purely in `D`, and does not establish the
  `D<->j_max` dictionary -- AZ2's own producer must define that mapping
  before adopting a `D`-based recommendation from this rehearsal.

## Planning notes for sub-round 5

See `results.json`'s `planning_notes_for_subround_5` for the full text;
in short: (1) D<=8 is comfortably feasible for AZ2's routine exact
Ritz-value work (the full three-point-grid-plus-two-derivative-methods
rehearsal above took 281 seconds total); D=10 is marginal; D>=12 needs an
algorithmic change and should not be attempted without re-measuring at
D=10 first; the `D`-to-`j_max` dictionary itself is undefined here and is
AZ2's own job. (2) If AZ2 adopts the exact-second-difference route for
its own derivative-at-zero control, it should scale its `exact_bracket`
width with `h^2` rather than holding it fixed, or simply reuse
assistant-3's regularized-solve method (now confirmed D-stable at D=6 and
D=8) for that one number and reserve Hellmann-Feynman/concavity brackets
for the finite-`tau_FG` grid points, exactly as this file does. (3) The
double/triple-independent-method discipline assistant-3's own planning
notes recommended continues to hold: this sub-round's from-scratch
anchor-union enumeration, from-scratch `K_2'` rebuild and from-scratch
SU(2) character-theory derivation each independently reproduce an
already-admitted AY1/AW1 number, giving AY2 or any AZ-series producer two
independently-built formulas to cross-check its own live-read values
against, in addition to the admitted gate text.
