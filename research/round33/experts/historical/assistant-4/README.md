# Historical lens (Newton/Tesla) assistant scripts -- Round33 applications stage, assistant 4

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted assistant scripts
for the Newton/Tesla historical lens, delivering three independent
cross-checks for the applications-stage investigations BD1 and BD2: (1) an
independent exact enumeration of the flip sets `E_3` (`Z^3`; the AW1 set) and
`E_2` (`Z^2`) on the named boxes, on the 24-link coarse factors, and a
genuine GF(2) solvability check of flip-set existence on five named periodic
tori; (2) an independent exact computation of `E_Haar[W^k]`, `k=1..4`, for
SU(2), U(1) and Z2 by direct integration/summation, and the first-order
coefficient under the frozen BD1 convention; (3) an independent
re-derivation of the Round11 two-plaquette graph's counts and the Z^3 1x2
rectangle's `R`-incidence face counts.

These scripts and this note count **zero research loops**: they are
cross-checks for the lens, not a producer, skeptic or advisor artifact, and
nothing here is admission evidence. Nothing here reads or imports
`research/round33/forward/bd1/check.py`, `research/round33/reverse/bd1/
check.py`, `research/round33/forward/bd2/check.py`,
`research/round11/solver/two_plaquette.py`, `research/round33/skeptic/
bd1_check.py`, `bd1_postreview_check.py`, `bd2_check.py`,
`bd2_postreview_check.py`, or any other `check.py` or solver module.
Nothing here reads any other assistant's scratch folder or script (only
`assistant-3/README.md`'s README/results.json layout convention is
followed, as its own README states of `assistant-2`, and its scripts are
not imported).

`flip_sets.py`'s membership rules, coarse-factor ownership convention,
whole-star box and periodic-torus constructions are re-derived from scratch
from the BD1 contract's own `parameters.flip_sets` text and from
`research/round21/forward/i1/report.md` sections 2-3 (the "block owns"
convention and the 24-class anchored face table, independently
transcribed, not copied from any other assistant's file); only
`research/round33/contracts/bd1.json` (frozen), `research/round33/advisor/
bd1-gate.json`, `research/round33/forward/bd1/report.md` and `output/
results.json`, and `research/round33/reverse/bd1/report.md` and `output/
results.json` (data, never code) are read for the final comparison.
`haar_moments.py` computes every moment from scratch by direct integration
(SU(2): the SU(2) Weyl density and the classical Wallis recursion; U(1):
the binomial constant term; Z2: direct summation) and only afterwards
parses `research/round33/advisor/bd1-gate.json`'s own text (by two
independent regexes, one for the moment list and one for the first-order
coefficient) for the comparison. `graph_counts.py` builds the Round11
two-plaquette graph from scratch as two unit squares glued along one edge
(never opening `research/round11/solver/two_plaquette.py`) and the Z^3 1x2
rectangle from scratch from the same I1 face table `flip_sets.py`
transcribes independently (a second, separate transcription in this
script, not a shared import), and only afterwards reads
`research/round33/forward/bd2/report.md`, `research/round11/README.md`,
`research/round33/advisor/bd2-gate.json` and `research/round33/skeptic/
bd2.md` (prose only, for the pinned face-count line) for the comparison.

Arithmetic: `flip_sets.py` uses plain Python `int` and Python's builtin
arbitrary-precision integers used as GF(2) bit-vectors (XOR/AND/bit-length
only; no floats, no `Fraction`). `haar_moments.py` uses
`fractions.Fraction` throughout for every value that enters a comparison
(no floats decide anything). `graph_counts.py` uses plain Python `int`
throughout (every quantity is an exact count; no floats, no `Fraction`).
No script here uses `mpmath` or `python-flint`.

Read before writing: `research/round33/contracts/bd1.json` and `bd2.json`
(frozen), `research/round33/advisor/bd1-gate.json` and `bd2-gate.json`,
`research/round33/forward/bd1/report.md` and `output/results.json`,
`research/round33/reverse/bd1/report.md` and `output/results.json`,
`research/round33/forward/bd2/report.md` and `output/results.json`,
`research/round21/forward/i1/report.md` (sections 2-3, prose only),
`research/round11/README.md` (prose only), `research/round33/skeptic/
bd2.md` (prose only, for the pinned face-count line), and
`research/round33/experts/historical/assistant-3/README.md` (this
package's README/results.json layout convention; its scripts are not
imported, only its file layout is followed).

## How to run

```bash
python3 -B research/round33/experts/historical/assistant-4/flip_sets.py
python3 -B research/round33/experts/historical/assistant-4/haar_moments.py
python3 -B research/round33/experts/historical/assistant-4/graph_counts.py
```

Each script is standalone, prints its own JSON report to stdout, and exits 0
iff its `overall_pass` is `true`. All three were also run under
`python3 -B -O` and produced byte-identical stdout; `results.json` combines
the three fresh runs (see "Files" below) and is itself stable across
rebuilds from either interpreter mode, since every input it assembles is
already byte-identical between `-B` and `-B -O`.

## What each script does

**`flip_sets.py`.** Independently re-derives the flip-set membership rules
from the BD1 contract text -- `E_3={(p,x):p_y even} u {(p,y):p_z even} u
{(p,z):p_x even}` on `Z^3` (the AW1 set) and `E_2={(p,x):p_y even}` on
`Z^2` -- and:

- **All of `Z^3`/`Z^2`.** Checks all 24 `(orientation, p mod 2)` residue
  classes of `E_3` (12 meeting a plaquette once, 12 meeting it three times,
  every class covariant under even translation, checked against eight
  independent even shifts each) and all 4 classes of `E_2` (every class
  meeting exactly once).
- **The 24-link coarse factor.** Re-derives, from I1's "the block owns all
  three positively oriented links whose tail belongs to `T_b`" and its
  six/four/fourteen-link breakdown, the rule that a factor `(i,j,k)` owns,
  for each of its 8 fine points `(4i+r,2j+s,k)`, `r=0..3`, `s=0..1`, the
  x-, y- and z-link based there (24 links total), and shows `E_3` contains
  exactly 16 of these when the anchor's `z` is even and 8 when odd -- on
  the seven anchors the forward report probes and on a wide sample of
  `13x13x13` other anchors.
- **The whole-star boxes `Lambda_N`, `N=2,3,4`.** Builds `Lambda_N` as the
  union of factor links for `i,j,k` in `[-N,N]` and enumerates every
  plaquette owned by the box **two independent ways**: a raw brute-force
  scan over a padded fine window (checking all four links of every
  candidate plaquette against the owned-link set), and a closed-form sum
  over the 24-class I1 face table per anchor (an omitted face is owned
  exactly when its own owner-set's required neighbours are all inside the
  box; a face is *retained* only when the anchor's whole star is inside
  the box). The two methods are checked against each other before either
  is compared with the BD1 packets.
- **`E_2` boxes, `N=2,3,4`.** The literal `[-N,N]^2` box, no coarsening.
- **Periodic tori.** A genuine GF(2) Gaussian-elimination solvability
  check (bit-packed Python integers, not the closed-form "at most one odd
  side" rule) for whether *some* link set meets every plaquette of a torus
  oddly, on the five named tori (`4x3x4`, `3x3x4` for `E_3`; `4x3`, `3x3`,
  `3x4` for `E_2`), plus the literal keyed `E_3`/`E_2` rule's own seam
  defect (evaluated with periodic wraparound, not solved for).

**`haar_moments.py`.** Computes `E_Haar[W^k]`, `k=1..4`:

- **SU(2), direct integration.** The SU(2) Weyl density
  `(2/pi) sin^2(theta) dtheta` on `theta` in `[0,pi]`, with
  `W=cos(theta)`; the classical Wallis recursion for
  `J_n=integral_0^{pi/2} cos^n(theta) dtheta` gives an exact rational
  `C_m=J_{2m}/pi` (checked two independent ways -- the recursion and the
  closed double-factorial form -- and against the literature constants
  `C_1=1/4`, `C_2=3/16`, `C_3=5/32`), and `E[W^{2m}]=4(C_m-C_{m+1})` with
  `pi` cancelled exactly.
- **U(1), the binomial constant term.** `cos^k(theta)` expanded by the
  binomial theorem in `e^{+-i theta}`; the Haar average keeps only the
  frequency-0 term, giving `E[W^k]=C(k,k/2)/2^k` for even `k`, `0` for odd.
- **Z2, direct summation.** `E[W^k]=(1^k+(-1)^k)/2` over the two group
  elements.
- **First-order coefficient.** `2(1/3)E[W^2]/(32 C_F)` under the frozen
  convention, with `C_F` read from the contract (`3/4` for SU(2), `1` for
  U(1) and Z2).

**`graph_counts.py`.**

- **The Round11 graph.** Built from scratch as two unit squares glued
  along one shared edge (never reading `two_plaquette.py`); gives 6
  vertices and 7 links by direct count and, independently, by
  inclusion-exclusion over the two squares' own vertex/edge sets. One
  local Gauss constraint per vertex (standard lattice gauge theory, and
  `research/round11/README.md`'s own "all six local Gauss constraints")
  gives 6 Gauss constraints. The shared edge is identified as the one edge
  common to both squares.
- **The Z^3 1x2 rectangle.** Re-derives the I1 24-class face table (a
  second, independent transcription from `flip_sets.py`'s, not a shared
  import) and builds the rectangle as the union of the xz faces at the
  origin and at `e_x`, minus their shared middle link, giving its six
  links and, via the I1.1 `(floor(x/4),floor(y/2),z)` owner rule, their
  owning factors.
- **`R`-incidence.** For `R={0,e_z}`, an owner-set search (never importing
  the route-B grouping any other assistant script uses) counts faces "at"
  each site of `R`, "containing" `R`, "inside" `R` (owner set exactly `R`)
  and "meeting" `R` (by direct intersection, and independently by
  inclusion-exclusion over the two sites), giving the straddling and
  single-site counts by subtraction.

## What passed

All three scripts pass (`overall_pass: true` in each, and in the combined
`results.json`).

## Findings

**flip_sets.py: no discrepancy; every pinned flip-set number holds
exactly, and one script bug was found and fixed in development.** The
independent enumeration reproduces, for `N=2,3,4`: owned links
`3000/8232/17496` (`=24(2N+1)^3`), owned plaquettes `2335/6909/15291` with
meet-once/meet-three histograms `1082/1253`, `3630/3279`, `7348/7943`,
retained faces `1344/4536/10752` (`=21(2N)^3`, exactly half meeting once
and half meeting three times in every case) -- all matching the forward
and reverse BD1 packets' own `results.json` fields bit-for-bit, by two
mutually independent counting methods that also agree with each other.
The 24-link coarse factor gives 16 links in `E_3` at even anchor `z` and 8
at odd `z`, matching the forward report's per-factor table (including the
seven specific probed anchors) and the reverse's `even_z_links`/
`odd_z_links` fields. `E_2` meets every plaquette of `[-N,N]^2` exactly
once for `N=2,3,4`, matching both packets. The GF(2) solvability check
(Gaussian elimination, not the closed-form rule) finds a flip set exists
on `4x3x4`, `4x3` and `3x4` (one odd side each) and does not exist on
`3x3x4` and `3x3` (two odd sides each), agreeing exactly with the reverse
packet's `finding_torus_flip_set_existence_gf2` and
`periodic_tori_odd_side_recorded` checks and with the forward report's
`remark_gf2_not_claimed` entries where it names that torus; the keyed
rule's own seam defects (16, 24, 4, 3, 0 even plaquettes respectively)
match the forward report and the BD1 gate's limitations text exactly.
**Bug found and fixed (this script only, before any comparison was run):**
an early version of the GF(2) elimination's final contradiction test used
a self-referential shift comparison that never actually detected the
all-variables-zero/RHS-one row, so every torus initially reported
"solvable" -- including `3x3` and `3x3x4`, contradicting a direct parity
argument (an odd number of plaquette equations with every link's total
degree even forces `0=1` when both sides of a torus are odd). The test was
corrected and re-checked against that independent parity argument before
being used for any comparison; the corrected script's output is what is
reported here and it matches both producers exactly.

**haar_moments.py: no discrepancy.** SU(2), U(1) and Z2 moments
`E[W^k]`, `k=1..4`, computed by three different from-scratch routes
(Weyl-density integration, binomial constant term, direct summation)
equal `0,1/4,0,1/8`, `0,1/2,0,3/8` and `0,1,0,1` respectively, matching
the BD1 gate's stated moments exactly (parsed independently from the
gate's own text). The first-order coefficients `1/144`, `1/96` and `1/48`
match the gate's decision-field values bit-for-bit.

**graph_counts.py: no discrepancy, and one script bug was found and fixed
in development.** The from-scratch two-square construction gives 6
vertices, 7 links (both confirmed by inclusion-exclusion) and 6 Gauss
constraints, with the one shared edge matching the BD2 report's `vM`,
consistent with `research/round11/README.md`'s "seven-link SU(2) operator
on two adjacent open squares, including all six local Gauss constraints
and the shared-link interaction" and the BD2 gate's and forward report's
own "6 vertices, 7 links" phrasing. The Z^3 1x2 rectangle's six links and
their owners (`0,0,0,e_z,e_z,0`, all inside `R`) match the BD2 forward
report's own description exactly. The `R`-incidence counts -- 49 per site,
16 containing `R`, 10 inside `R`, 82 meeting `R`, 72 straddling, 33 at one
site without the other -- reproduce the BD2 skeptic review's line ("My
enumeration gives 82 omitted faces meeting R, 10 inside R, 16 containing R
and 49 per site. That leaves 33 at one site without the other, and 72
straddling") exactly, cross-checked internally by inclusion-exclusion
(`49+49-16=82`) and subtraction (`82-10=72`, `49-16=33`). **Bug found and
fixed (this script only, before any comparison was run):** an early
version compared the rectangle's single shared link (a one-element list
from a `sorted()` call) against its expected value as a Python set, which
is never equal regardless of content and so always failed; the comparison
was corrected to compare sets, and the corrected script's output is what
is reported here.

## Files

- `flip_sets.py` -- independent exact enumeration of the flip sets `E_3`
  and `E_2` on the named boxes, the 24-link coarse factors, and a GF(2)
  solvability check on five named periodic tori, compared with the BD1
  contract, gate, and forward/reverse packets.
- `haar_moments.py` -- independent exact computation of `E_Haar[W^k]`,
  `k=1..4`, for SU(2), U(1) and Z2, and the frozen-convention first-order
  coefficient, compared with the BD1 gate.
- `graph_counts.py` -- independent re-derivation of the Round11
  two-plaquette graph's counts and the Z^3 1x2 rectangle's `R`-incidence
  face counts, compared with the BD2 report, gate and skeptic review.
- `results.json` -- combined pass/fail and full raw output from all three
  scripts, plus a `findings` section summarizing the results above.

This lens admits nothing and counts zero research loops.
