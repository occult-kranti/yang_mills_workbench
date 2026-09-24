# Round32 sub-round 3 -- modern (Penrose/Feynman) lens, assistant-3

Status: assistant/coder cross-check tools, per `update-2.md` section 6
(this sub-round's proposed tests). **These outputs count zero research
loops.** They are previews and cross-checks only: python-flint 0.9 (Arb)
and the Round11 `two_plaquette.py` solver module are independent,
already-frozen libraries reused here BY IMPORT (never reimplemented) for
comparison and computation, never for admission. Every number this
repository actually admits is decided by exact `fractions.Fraction`
arithmetic in a frozen `check.py` inside `forward/`, `reverse/` or
`skeptic/`; nothing in this directory is imported by any of those, and
nothing here changes a verdict.

Human project author: Hruday N M (BUNZEEY). Run everything with `python3 -B`.

## Files

- `ax2_budget_actual.py` -- update-2.md section 6 item 1: re-runs the AX2
  window-budget arithmetic `E'(s)=2(D'+D'^2)+51|tau|s/pi` with AX1's
  *actual admitted* forward tier-ii `D'` (live-read from
  `forward/ax1/output/results.json headline.D_ii_plus`, cross-checked
  verbatim against `advisor/ax1-gate.json`'s own text), at `tau=1e-8`,
  `s=1`, with directed `pi` (a Machin bracket imported from the frozen,
  already-admitted `forward/av2/calculator.py::pi_interval`) and an
  independent Arb (256-bit) cross-check (`flint_harness.contains`,
  reused). Also computes the exact crossover `s*` bracket, and reports the
  reverse refinement and AX1's own (looser) `4e-7` target as explicitly
  labelled comparisons, never substituted for the pass/fail decision.
  Self-test: PASS.
- `kappa_tied_fixture.py` -- update-2.md section 6 item 2: a small, exact,
  **labelled finite-graph** toy fixture (one plaquette reduced to its
  character basis `j<=1` = `{j=0,j=1/2,j=1}`, `transfers_to_aq:false`)
  with two independent "face" operators (`T_omitted` at coefficient `nu`,
  `T_selected` at coefficient `kappa`), both built odd under a `U_E`-style
  central-flip grading (`diag(+1,-1,+1)`). Verifies, purely by exact
  matrix arithmetic: (1) `U_E H(nu,kappa) U_E = H(-nu,-kappa)` exactly,
  for every sampled `(nu,kappa)`; (2) the exact first-order coefficients
  `a,b` of `<W>^(1)=a*nu+b*kappa` (two independent derivations -- a closed
  diagonal-resolvent formula and a generic linear solve on the orthogonal
  complement -- agree, after this sub-round's own first draft caught a
  genuine sign bug via that very cross-check); (3) antisymmetry of `<W>`
  in `tau` (`nu(tau)=tau/24`) HOLDS for every fixed tie ratio
  `kappa=c*nu` tested, and FAILS by exactly the predicted nonzero amount
  `2*b*kappa0` when `kappa=kappa0` is held fixed and nonzero while `nu`
  flips -- recovering the AW1 flip-lemma's `kappa=0` special case exactly.
  Self-test: PASS.
- `uniform_counts_from_scratch.py` -- update-2.md section 6 item 3: an
  independent (of the AV1/AX1 producers AND of assistant-1's
  `flip_parity_k2.py`) re-derivation of the route-B uniform-model face
  counts, encoding the I1 24-anchored-face-class table with two
  structurally different methods -- closed-form inclusion-exclusion on
  coarse block offsets, and an independent owner-block/class-row brute
  force (no fine `(x,y,z)`/residue bookkeeping at all, unlike
  `flip_parity_k2.py`). Both methods agree, and agree with the AX1 gate,
  on **52** faces per factor (49 omitted + 3 selected), **88** faces
  meeting `R={0,e_z}` (82 omitted + 6 selected), **16** inside `R`
  (10 omitted + 6 selected), and the 6 selected-face count; widening the
  brute-force box from radius 6 to 9 changes nothing. Self-test: PASS.
- `az2_dictionary_calc.py` -- update-2.md section 6 item 4: a
  normalization-dictionary CALCULATOR for AZ2. States four explicit,
  individually-flagged assumptions (A1 `alpha=1`; A2 AW1's parity theorem,
  admitted, licenses treating the Z^3 uniform sum's cross terms as
  vanishing at first order; A3 `tau_FG:=tau/24`, the resulting dictionary
  choice; A4 the FG model's own exact free gap, `two_plaquette.free_gap()
  ==3`, confirmed live, is identified with the Z^3 side's declared
  "plaquette energy 3"), then computes the FG side's exact
  `d<x>/d(tau_FG)|_0=1/6` TWO independent ways (a closed-form eigenvector
  argument, since `Kx=3x` exactly and `<x,x>=1/4` exactly; and
  `az2_spec_check.md` section 5's own proposed regularized-singular-solve
  method at `D=6`, now actually executed in exact `Fraction` arithmetic
  and Arb-cross-checked via `flint_harness`/`flint.arb_mat.solve`, not
  merely floating-sanity-checked as before) -- both give exactly `1/6`.
  Converted through the stated dictionary, `(1/6)*(1/24)=1/144`, which
  **matches** AW1's admitted Z^3 first-order coefficient exactly
  (live-read from `forward/aw1/output/results.json`). Reported throughout,
  in bold, as a **labelled consistency observation under A1-A4, not a
  proof or a transfer** (contract wording); a contrast computation shows
  the match is not a vacuous tautology (the naive, unwarranted dictionary
  `tau_FG:=tau` does NOT reproduce `1/144`). Self-test: PASS.
- `results.json` -- combined machine-readable output of all four
  self-tests plus the three planning notes below.

```
python3 -B research/round32/experts/modern/assistant-3/ax2_budget_actual.py
python3 -B research/round32/experts/modern/assistant-3/kappa_tied_fixture.py
python3 -B research/round32/experts/modern/assistant-3/uniform_counts_from_scratch.py
python3 -B research/round32/experts/modern/assistant-3/az2_dictionary_calc.py
```

All four exit 0 (PASS) as of this writing; each prints its own JSON
report and exits 1 on any failed sub-check. Total wall-clock time is
under two seconds (the slowest step, `az2_dictionary_calc.py`'s `D=6`
regularized exact solve plus its 256-bit Arb cross-check, is well under
one second on this container).

## ax2_budget_actual.py results

- With the admitted forward `D'~1.4446e-8`: `E'~1.912e-7`, clearing
  `1e-6` with margin ratio `~5.23` (well above the "flag if margin falls
  below 2" threshold update-2.md set). Both the strict `E'<1e-6` (this
  task's own comparator) and the AX2 contract's own `E'<=1e-6` hold.
- With the reverse refinement `D'~1.2224e-8`: `E'~1.868e-7`, margin
  `~5.35` -- a labelled comparison, never substituted for the admitted
  value (the AX2 contract's `av1_tier_bound` control forbids exactly
  that substitution).
- With AX1's own preregistered target `D'<=4e-7`: `E'~9.623e-7`, margin
  ratio only `~1.039` (the `~4%` margin update-2.md section 4 warned
  about) -- confirming that warning was specifically about the *target*,
  not the *admitted exact tier*, which clears comfortably.
- Crossover `s*` (admitted `D'`, target `1e-6`): `[5.982012284..., same
  to 15+ digits]` -- a tight directed-`pi` bracket, Arb-cross-checked.

## kappa_tied_fixture.py results

- The structural sign-flip identity `U_E H(nu,kappa) U_E = H(-nu,-kappa)`
  holds exactly on every sampled point, including asymmetric and negative
  `(nu,kappa)`; `H_0` is `U_E`-even, both face operators are `U_E`-odd,
  and `U_E` is an involution -- all verified by direct matrix arithmetic,
  not assumed.
- The exact first-order coefficients are `a=-8/3` (`d<W>/d(nu)`),
  `b=-16/3` (`d<W>/d(kappa)`); the closed diagonal-resolvent formula and a
  generic linear solve on the 2-dimensional orthogonal complement agree
  exactly (this cross-check caught and fixed a sign error in the closed
  form during development -- left visible in git history of this file's
  authoring, not silently corrected).
- Tied case: for ratios `c in {1, 5/2, -3/4, 7}` and three `tau` values
  (including a negative one), `<W>^(1)(tau)+<W>^(1)(-tau)=0` exactly,
  every time.
- Fixed case: for `kappa0 in {1/50, -7/3}` (nonzero), the sum is exactly
  `2*b*kappa0 != 0` (predicted and observed identical, e.g. `16/75` and
  `-224/9`); at `kappa0=0` the sum is exactly `0`, recovering AW1's
  special case.

## uniform_counts_from_scratch.py results

- Method 1 (closed-form inclusion-exclusion on the 24-class table) and
  Method 2 (independent owner-block/class-row brute force) agree on
  every count: `49` omitted `+3` selected `=52` faces per site; `82`
  omitted `+6` selected `=88` meeting `R={0,e_z}`; `10` omitted `+6`
  selected `=16` inside `R`. All match the AX1 gate's own numbers
  exactly. Widening the brute-force box from radius 6 to 9 changes
  nothing (no boundary artifact).

## az2_dictionary_calc.py results

- Live-confirmed FG facts (never merely cited): `K*1=0` (own free
  reference), `K*x=3x` exactly, `<x,x>=1/4` exactly, `<x>=0` exactly,
  `two_plaquette.free_gap()==3` exactly, `tail_lower(D=6)=45`,
  `tail_lower(D=8)=69`.
- `d<x>/d(tau_FG)|_0 = 1/6` exactly, by two independent methods
  (closed-form eigenvector argument; `az2_spec_check.md`'s own proposed
  `D=6` regularized-singular-solve method, now executed in exact
  `Fraction` arithmetic and Arb-cross-checked at 256 bits).
- Under the stated dictionary (`tau_FG:=tau/24`, `A2`-`A4`),
  `d<x>/d(tau)|_0 = 1/144`, matching AW1's admitted Z^3 coefficient
  exactly. The naive, unwarranted dictionary `tau_FG:=tau` gives `1/6`
  instead, which does NOT match -- so the match is a genuine (if
  assumption-dependent) consequence of the stated dictionary, not a
  tautology. Labelled throughout: consistency, not proof; no transfer to
  AQ; `fg_coefficients_not_fitted`.

## Three planning notes for sub-rounds 4-5

See `results.json`'s `planning_notes_for_subrounds_4_5` for the full
text; in short:

1. **For AY1/AY2 (sub-round 4, state/density):** `ax2_budget_actual.py`'s
   live-read-never-retyped pattern is directly reusable by AY1's own
   `check.py` to bind AW1's admitted `rho^(1)_R` and `2*K_2'*tau^2`
   constant without transcription risk, exactly as update-2.md section 2
   asks. `kappa_tied_fixture.py`'s two-independent-derivations pattern
   (which caught a real sign bug in this sub-round's own first draft)
   is a template AY1's density-perturbation-theory work should budget
   time for.
2. **For AZ1/AZ2 (sub-round 5, continuum/finite graph):**
   `az2_dictionary_calc.py` turns the proposed normalization dictionary
   into an executable, fully exact calculation and finds it reproduces
   `1/144`; AZ2's own producer must still decide, independently, whether
   this is the dictionary it wants to freeze in its contract (or a
   different one), and state that choice in `az2.json`'s own
   preregistration before production, per the contract's "consistency,
   not proof" wording.
3. **For both:** `uniform_counts_from_scratch.py`'s two-structurally-
   different-methods pattern, agreeing on every count and stable under a
   widened brute-force box, is the standard of double-independent
   combinatorial checking AY1's new density bookkeeping and AZ2's own
   controls list (several of which are `not_applicable` to the finite
   graph and must be marked so with a stated reason, not silently
   dropped) should both meet.
