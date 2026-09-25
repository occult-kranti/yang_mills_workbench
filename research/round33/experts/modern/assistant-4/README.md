# Round33 sub-round 4 -- modern (Penrose/Feynman) lens, assistant-4

Status: research assistant/coder cross-check tools for BD1 and BD2, per the
task's instructions, mirroring
`research/round33/experts/modern/assistant-3/` from sub-round 3.
**These outputs count zero research loops.** They are previews and
cross-checks only: `python-flint` (`fmpq` exact rationals, `arb` ball
arithmetic, FLINT/Arb library) and `sympy` (exact symbolic algebra and
integration) are independent, already-frozen open-source libraries, reused
here BY IMPORT (never reimplemented, never modified) for independent
recomputation and comparison, never for admission. **No producer `check.py`
file is ever imported or executed anywhere in this directory** (neither
`research/round33/forward/bd1/check.py`,
`research/round33/reverse/bd1/check.py`, nor
`research/round33/forward/bd2/check.py` was even read, except through the
frozen `output/results.json` and `report.md` files each publishes, which is
not the same thing). Every number this repository actually admits for BD1
and BD2 was already decided by exact `fractions.Fraction` arithmetic in
those frozen `check.py` files, never opened here.

Human project author: Hruday N M (BUNZEEY). Run everything with
`python3 -B` (also verified byte-identical under `python3 -B -O`).

## Files

- **`group_moments_flint.py`** -- BD1 task 1. Independent computation of
  `E_Haar[W^k]`, `k=1..5`, for SU(3), SU(4), SU(5) and SO(3), by methods
  DIFFERENT from both BD1 producers (forward: characters/Peter-Weyl tensor
  multiplicities; reverse: Weyl integration by Laurent-polynomial
  constant-term extraction): SO(3) by `sympy`'s own symbolic integrator on
  the literal class-angle Haar integral (exact, closed form); SU(3), SU(4),
  SU(5) by direct numerical sampling of the literal Weyl-integration-formula
  torus integral (a discrete Fourier/trapezoidal quadrature, exact up to
  floating roundoff for these band-limited trigonometric integrands, per
  the sampling theorem -- confirmed by rerunning each at a larger grid and
  checking the drift is at the roundoff floor), plus a genuinely rigorous
  `python-flint` Arb-ball version of the SU(3) quadrature at 200 bits. Also
  recomputes the closed-form first-order coefficient
  `1/(48 N (N^2-1))` for SU(N), N>=3, exactly via `flint.fmpq`, and checks
  the general symbolic identity `2(1/3)E[W^2]/(32 C_F) = 1/(48N(N^2-1))`
  with `E[W^2]=1/(2N^2)` in `sympy` for general `N`. Compares every value
  to the admitted BD1 table (`research/round33/forward/bd1/output/results.json`,
  cross-checked against the reverse packet and the BD1 gate). Self-test:
  PASS, all checks (35 moment comparisons plus the coefficient identities
  and the SU(3) Arb enclosure) pass.
- **`obstruction_series.py`** -- BD1 task 2. Independent exact
  Rayleigh-Schroedinger/Hellmann-Feynman recomputation of the SU(3) and
  SO(3) obstruction coefficients (`d omega(W^2)/d tau` at `tau=0` and the
  second-order coefficient of `omega(W)`) and the SU(5) fourth-order
  coefficient, on the one-plaquette model `H_FG(G)`, by a route neither
  producer's report states: build the EXACT finite matrix of `H_FG(G)`
  restricted to the small subspace that provably carries the whole
  perturbation series at the needed order (a closed ring of antisymmetric
  powers of the fundamental for SU(3)/SU(5), justified from Pieri's rule,
  an elementary N-ality mod-N selection argument, and a Young's-lattice
  sub-diagram argument, each derived and checked in the script itself; a
  truncated angular-momentum tower for SO(3), checked empirically
  convergent across four truncation sizes), then extract its ground
  eigenvalue's exact Taylor series in `tau` (and, via an auxiliary coupling
  `mu W^2`, in `mu`) from the EXACT characteristic polynomial by a purely
  mechanical `sympy` implicit-power-series solve -- never the producers'
  own closed-form RS shortcuts. Hellmann-Feynman
  (`d E/d tau = -(1/3) omega(W)`, elementary calculus, not a producer
  derivation) converts the eigenvalue series into the `omega(W)` and
  `omega(W^2)` Taylor coefficients needed. `python-flint` `arb` gives a
  numeric preview of each exact value. Self-test: PASS, every coefficient
  (SU(3), SO(3): 2 each; SU(5): 1) matches the admitted BD1 value bit for
  bit.
- **`bd2_numbers.py`** -- BD2 task 3. `python-flint` Arb (300-bit)
  enclosures of the BD2 electric-band endpoints (`(3/2)L^2` with `L` the
  AY2 lower distance, and `98|tau|`), the 1x2-loop bound `K_2' tau^2`, and
  the 2+1D constants `G_3(1/64)=9e^{3/32}`, `G_3'(1/64)=118e^{3/32}` and
  the admissible-coupling cap `1/(576 e^{3/32})`, each checked to contain
  (or, for the exact rationals, match bit for bit) the frozen admitted
  value; `e^{3/32}` is computed with Arb's own built-in `exp()`, independent
  of any producer-written Machin/Taylor bracket; the self-map
  (`tau G_3(R)<=R`) and exclusion (`2 tau G_3'(R)<1`) conditions are also
  reconfirmed at the admitted directed-lower cap in ball arithmetic, and
  the `8e^{6t}(1+8t)`/`8e^{6t}(14+48t)` closed forms are cross-checked
  against the `9e^{3/32}`/`118e^{3/32}` simplification. `L` and `K_2'`
  themselves are reused as already-reviewed AY1/AY2-gate constants (as
  `assistant-3/bc2_arb.py` reuses route constants such as `G(R)=148/7`),
  not re-derived here -- what is independently checked is the ARITHMETIC
  combining them into the four BD2 quantities, in a different arithmetic
  engine (Arb balls, not `fractions.Fraction`). Self-test: PASS, all
  checks (band endpoints, loop bound, four 2+1D constants and two
  admissibility conditions) pass.
- **`sota_note.md`** -- BD2 task 4. A short placement of BD1/BD2 relative
  to literature this lens already reads (`research/round33/experts/modern/sources.json`):
  centre symmetry and N-ality (Greensite's confinement review, already on
  file, background only); strong-coupling expansions (both BD1 and BD2 are
  Hamiltonian strong-coupling perturbation theory in the Kogut-Susskind
  sense, though no Kogut-Susskind-era source is itself on file); and
  Wegner duality for Z2 (BD1's Z2 cell), for which **no source is recorded
  in `sources.json` at any depth** -- listed as a genuine reading request,
  nothing fetched. No scientific-priority claim anywhere.
- **`results.json`** -- combined machine-readable output of the three
  scripts' self-tests (`all_passed` plus every individual check, under
  `tools`).

```
python3 -B research/round33/experts/modern/assistant-4/group_moments_flint.py
python3 -B research/round33/experts/modern/assistant-4/obstruction_series.py
python3 -B research/round33/experts/modern/assistant-4/bd2_numbers.py
```

All three exit 0 (PASS) as of this writing; each prints its own JSON report
and exits 1 on any failed sub-check. All three run in well under a minute
(`obstruction_series.py` is the slowest, about 18s, from the `sympy`
implicit-series solves) and were also verified under `python3 -B -O`
(byte-identical output to the `-B`-only run for all three files, apart from
timing fields).

## Findings

### 1. `group_moments_flint.py`

**Every Haar moment `E[W^k]`, k=1..5, this script independently computes
for SU(3), SU(4), SU(5) and SO(3) agrees with the admitted BD1 forward/
reverse table**, by a mechanism neither producer used: SO(3) exactly, via
`sympy`'s own symbolic integrator on the class-angle Haar density
`(1-cos theta)/pi`; SU(3), SU(4), SU(5) to double-precision floating
accuracy (worst observed deviation about `1.7e-14`, at the roundoff floor,
confirmed stable when the sampling grid is enlarged) via literal numerical
sampling of the Weyl integration formula, plus a genuinely rigorous
200-bit Arb-ball version for SU(3) that CONTAINS every admitted moment
with a ball radius of order `1e-58` or smaller. The closed-form first-order
coefficient `1/(48N(N^2-1))` matches the admitted `1/1152`, `1/2880`,
`1/5760` for SU(3), SU(4), SU(5) exactly (`flint.fmpq`), and the general
symbolic identity with `2(1/3)E[W^2]/(32C_F)` holds for every `N` (not just
the three checked), confirming the BD1 report's own stated simplification.

### 2. `obstruction_series.py`

**Every SU(3) and SO(3) obstruction coefficient, and the SU(5) fourth-order
coefficient, matches the admitted BD1 value exactly**, computed from an
EXPLICIT finite matrix (a 3-state or 5-state ring for SU(3)/SU(5), an
empirically-convergent truncated tower for SO(3)) via a purely mechanical
`sympy` characteristic-polynomial power-series solve, never the producers'
own closed-form RS/Hellmann-Feynman shortcuts: SU(3) `d omega(W^2)/d tau =
1/6912`, second-order coefficient `1/589824`; SO(3) `1/2592` and
`1/331776`; SU(5) fourth-order coefficient `1/63403380965376`. Two
byproduct cross-checks worth recording: (a) the ring's own
`<triv|W^2|triv>` reproduces the independently-known Haar second moments
`E[W^2]=1/18` (SU(3)) exactly, confirming the hopping-weight bookkeeping;
(b) the elementary N-ality selection-rule argument (`nality_selection_rule`)
that isolates the column-chain ring for SU(N) is checked computationally
for both `n_steps=3` (SU(3)) and `n_steps=5` (SU(5)), confirming only the
all-ascending or all-descending sign sequences survive, exactly matching
the BD1 forward/reverse reports' own stated (but not re-derived-here)
"only the column chains ... (and conjugates) return to the trivial class"
claim -- this script derives that fact independently rather than assuming
it.

### 3. `bd2_numbers.py`

**Every BD2 quantity checked here -- the electric-band endpoints, the
1x2-loop bound, and the four 2+1D constants -- is contained in (or, for the
exact rationals, matches bit for bit) its independent Arb enclosure**: the
electric-band lower endpoint `(3/2)L^2` and upper endpoint `98|tau|` match
the admitted `output/results.json` rows exactly and their Arb balls
(300-bit, essentially zero-width) contain both; `K_2' tau^2 =
966771578474926086618624139557778885954947547760216752246561/720528856978172107545458049318912000000000000000000000000000000000000000`
(about `1.34e-12`) matches the admitted `z3_1x2` bound exactly and, as an
extra check, is confirmed to strictly dominate the (formal, unsigned)
second-order term `7 tau^2/124416`; `G_3(1/64)=9e^{3/32}` (about `9.8846`)
and `G_3'(1/64)=118e^{3/32}` (about `129.598`), computed from Arb's own
`exp()`, lie strictly inside the admitted directed rational brackets, and
the alternative closed forms `8e^{6t}(1+8t)`/`8e^{6t}(14+48t)` reproduce
them exactly; the admitted directed-lower cap
`1580747155173/10^15 approx 0.0015807...` is confirmed to be a genuine
(provable) lower bound on the true cap `1/(576e^{3/32})`, and, at that
directed-lower value, the self-map condition `tau G_3(R)<=R` and the
exclusion condition `2 tau G_3'(R)<1` both hold in ball arithmetic (the
self-map binds with essentially no slack, the exclusion condition with
substantial room, exactly as the BD2 gate's own "the self-map binds"
remark states).

### 4. `sota_note.md`

Places BD1's centre-symmetry/N-ality mechanism next to Greensite's
confinement review (already on file, background/genre-level only — BD1's
own wording already disclaims that the transfer criteria are its own
derivation, not taken from the review), and BD2's obligation row for an
area law next to Osterwalder-Seiler's classical strong-coupling area-law
theorem (again background only, since BD2 claims no area law). Both BD1
and BD2 are, in genre, Kogut-Susskind-style Hamiltonian strong-coupling
perturbation theory, but no Kogut-Susskind-era source is itself recorded
in this lens's `sources.json`. Wegner duality for the BD1 Z2 cell has **no
source on file at all**; two concrete reading requests are listed, nothing
fetched. No priority claim is made anywhere.

## Scope note

Every check in this directory is a **comparison or an independent
re-derivation** of a quantity already computed, by a different route, in a
frozen `report.md` and already admitted by the BD1 or BD2 gate. None of it
is a research loop, none of it is evidence, and none of it changes any
BD1, BD2, AY1, AY2, or BB2 verdict. The four-dimensional Yang-Mills
existence and mass-gap problem remains open.
