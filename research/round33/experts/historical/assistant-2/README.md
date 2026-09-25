# Historical lens (Newton/Tesla) assistant scripts -- Round33 sub-round 2

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted assistant scripts
for the Newton/Tesla historical lens, delivering three independent
cross-checks requested for this lens after BB1 and BB2 (this sub-round's two
investigations) were frozen: (1) an independent exact enumeration of the
BB1 "every-site common core" lemma for all five of the BB1 contract's named
comparisons; (2) a face-by-face independent check of BB2 item 4's
coarse-translation claim over the full fine-translation period window, plus
a deliberate demonstration of a per-anchor histogram check's false-accept
pitfall; (3) an independent, exact-arithmetic re-evaluation of the BB2
item-5 correlation-function bracket's range (best K5 on `5<=N<=14000`, and
whether the bracket exceeds 2 at `N=14419,14420,14421`).

These scripts and this note count **zero research loops**: they are
cross-checks for the lens, not a producer, skeptic or advisor artifact, and
nothing here is admission evidence. Nothing here reads or imports
`research/round33/forward/bb1/check.py`, `research/round33/reverse/bb1/
check.py`, `research/round33/forward/bb2/check.py` or `research/round33/
reverse/bb2/check.py` (or any other `check.py`); every geometric,
combinatorial and arithmetic construction below is re-derived from scratch
from the star/face definitions in `research/round21/forward/i1/report.md`
and `research/round29/forward/am2/report.md`, and from each BB1/BB2
producer's own exact `output/results.json` constants. Only the forward/
reverse producers' `report.md` prose and their exported `output/
results.json` (data, never code) are read for the numeric cross-checks,
together with `research/round33/contracts/bb1.json`, `bb2.json` and
`research/round33/advisor/ba1-gate.json`, `ba2-gate.json` (the BB1/BB2
contracts' own `shared_premises`; no `bb1-gate.json`/`bb2-gate.json` exists
yet at the time these scripts were written -- BB1 and BB2 are frozen
`status: frozen_before_production` but not yet gated).

Arithmetic: `every_site_core.py` uses plain Python `int` throughout (every
quantity it claims is an exact integer lattice coordinate, l-infinity
distance or face/anchor count; no floats, no `Fraction`).
`translation_faces.py` likewise uses plain `int` (residues, floor
divisions, translation vectors). `item5_range.py` uses
`fractions.Fraction` for every quantity that enters a pass/fail comparison,
and `decimal.Decimal` (standard library, correctly-rounded `ln`/`exp`) only
to obtain a directionally-padded, exact-Fraction-convertible enclosure of
the one transcendental ingredient `e^y`; see that script's module
docstring for the full method and its justification. No script here uses
`mpmath` or `python-flint`.

Read before writing: `research/round33/contracts/bb1.json` and `bb2.json`
(frozen), `research/round33/advisor/ba1-gate.json` and `ba2-gate.json`,
`research/round33/forward/bb1/report.md` and `output/results.json`,
`research/round33/reverse/bb1/report.md` and `output/results.json`
(Section 2's Lemma B5 and Theorem B6; Section 8's Item 4a), `research/
round33/forward/bb2/report.md` and `output/results.json`, `research/
round33/reverse/bb2/report.md` and `output/results.json` (Section 7's
Lemma 7.1/7.2; Section 8's Theorem 8.4), `research/round21/forward/i1/
report.md` (sections 2-3, the Euclidean-division/`pi` map and the 24-class
anchored face table; section 6, the F2 padding construction), `research/
round29/forward/am2/report.md` (`S={0,e_x,e_y,e_z}`, 21 omitted faces per
anchor), and `research/round33/experts/historical/assistant-1/` (this
package's README/results.json layout convention; its scripts are not
imported, only its file layout is followed).

## How to run

```bash
python3 -B research/round33/experts/historical/assistant-2/every_site_core.py
python3 -B research/round33/experts/historical/assistant-2/translation_faces.py
python3 -B research/round33/experts/historical/assistant-2/item5_range.py
```

Each script is standalone, prints its own JSON report to stdout, and exits 0
iff its `overall_pass` is `true`. All three were also run under
`python3 -B -O` and produced byte-identical stdout (`item5_range.py` takes
about 10 seconds; the other two run in well under a second).

## What each script does

**`every_site_core.py`.** Independently rebuilds, from scratch, the whole
star `S={0,e_x,e_y,e_z}`, the 21 individual omitted-face owner-set classes
of I1's anchored face table, the **F1** retention rule (`AQ1` centered
whole-star boxes: anchor `b` retained, as a single all-or-nothing unit,
iff `b+S` lies entirely inside the volume) and the **F2** retention rule
(I1 section 6's "all-actual-support-contained block prescription with
padding": an individual omitted face at anchor `b` is retained iff its
own owner set lies entirely inside the volume, independent of the rest of
`b`'s star). It then builds, for `N=2,3,4`, all five of the BB1 contract's
`parameters.comparisons`:

1. F1 on `Lambda_N` vs F1 on `Lambda_{N+1}` (source = new whole stars);
2. F2 on `Lambda_N` vs F2 on `Lambda_{N+1}` (source = new individual
   faces);
3. F1 vs F2 on the same `Lambda_N` (source = the faces F2 retains at a
   partially-covered boundary anchor that F1's all-or-nothing rule drops
   entirely -- since every F1-retained face is automatically an F2-retained
   face, this difference is one-directional);
4. two centered boxes `Lambda_M`, `Lambda_M'` with `M,M'>=N`, compared
   directly (not telescoped): one F1 example at `(M,M')=(N,N+3)`, one F2
   example at `(M,M')=(N+1,N+4)`, both distinct from the adjacent pairs of
   comparisons 1-2;
5. two one-prescription volumes containing `Lambda_N`: one F1 example on a
   genuinely non-cubic cuboid (three distinct side lengths) against
   `Lambda_{N+2}`, and one F2 example on a second, differently-shaped
   non-cubic cuboid against `Lambda_{N+3}`.

For every comparison and every site `u` of `Lambda_N` (**not only** `u` in
`R={0,e_z}`, which is all the BA1 gate's own admitted statement covers),
the script computes, for every source term, the minimum l-infinity
distance from `u` to any site of that term's support, and checks it is at
least `N-|u|_inf` -- exactly the inequality behind BB1 reverse report's
Lemma B5 ("every omitted face with a site closer than `N-|u|_inf` to `u`
belongs to a star `b+S subset Lambda_N`, hence is retained by both F1 and
F2 on every volume containing `Lambda_N`") and Theorem B6's vanishing-order
argument. It records the minimum slack (`distance - (N-|u|_inf)`) per
comparison and flags any negative slack (none were found). As an
independent sanity check on the reconstruction itself (not assumed, but
computed from the same from-scratch code), it also confirms the exact
source-term counts against the closed forms the BB1 reverse report states:
`8(3N^2+3N+1)` new F1 stars, `56(9N^2+14N+6)` new F2 faces and
`28N(5N+1)` F1-vs-F2 extra faces.

**`translation_faces.py`.** Re-derives the 24-combination
`(orientation, r, s)` face-classification table from I1 sections 2-3
(`x=4i+r`, `y=2j+s`, `pi(x,y,z)=(floor(x/4),floor(y/2),z)`), then
enumerates **all 64** fine translations `t=(tx,ty,tz)` of the period
window `[0,8)x[0,4)x[0,2)` named in the BB2 reverse report's Lemma 7.2. For
each `t` it checks, independently and face-by-face: (i) whether the
implied coarse block shift `pi(p+t)-pi(p)` is the same vector for every
residue `(r,s)` (a "uniform anchor shift"); (ii) whether the classification
(selected, or one of the six omitted owner types) of every one of the 24
`(orientation,r,s)` combinations is preserved when its residues are
shifted by `(tx,ty,tz)`. A translation is called *coarse* only if both
hold. The script confirms exactly 8 of the 64 are coarse, that these 8 are
exactly `(4v_x,2v_y,v_z)` for `v` in `{0,1}^3`, and reproduces the report's
own witness (`t=(1,0,0)` maps the selected xy face at `r=2,s=0` onto class
`r=3,s=0`, omitted with owner set `{0,e_x}`) independently from the I1
table. It then builds the task's requested "skeptic's pitfall": a
per-anchor **owner-type histogram** check (comparing only the fixed
multiplicity counts `(3,1,1,10,2,4)` over the six omitted owner types,
never individual face identity) at anchor `b` against the same histogram
at the naively-shifted anchor `b+(tx//4,ty//2,tz)`. Since this histogram is
literally the *same* dictionary at *every* anchor of the lattice (the
`(r,s)` grid and hence the class table never depend on `(i,j,k)`), the
histogram check accepts all 64 translations unconditionally, including all
56 non-coarse ones the face-by-face check correctly rejects.

**`item5_range.py`.** Independently re-evaluates the BB2 item-5 bracket

```
C_dyn/(r_N-1) + c'_site |Lambda_{r_N}| e^{|Lambda_{r_N}|/10^8} q^(N-r_N) + 2 C' q^(N-1)
```

(`r_N=floor((N-1)/2)`, `|Lambda_r|=(2r+1)^3`, `q=1/64`) at the **exact**
`C_dyn`, `C'` and `c'_site` values each BB2 producer's own frozen
`output/results.json` reports (forward's single combined `C_dyn`; the
reverse producer's `C_dyn[F1]` and `C_dyn[F2]` separately; the same `C'`,
`c'_site` for both, per the contract). It first cross-validates its own
formula against every per-N value each producer's own `results.json`
already tabulates (reverse `F1`/`F2` at `N=5,6,10,20`; forward at
`N=5,10`), finding agreement to within about `1e-9` to `3e-12` relative in
every case, before trusting the formula at the untabulated `N` the task
asks about. It then (a) finds, by exact-Fraction comparison over every
integer `N` in `[5,14000]`, the smallest `K5` such that the bracket is at
most `K5/N` throughout that range, for all three constant sets, and
compares it to the reverse producer's own `item5_K5_certified_5_to_14000`
field; and (b) evaluates the bracket (with a directionally-safe exact
lower bound, so the ">2" claim is certified rather than merely previewed)
at `N=14419`, `14420` and `14421`, for all three constant sets, plus a
wider `N=14400..14425` context scan. The method used for the one
transcendental ingredient, `e^y` with `y=|Lambda_{r_N}|/10^8-(N-r_N)ln(64)`
(chosen over a from-scratch Taylor-remainder bound, which would need tens
of thousands of exact-fraction terms at the `N` studied here), is stated in
full in the script's module docstring: Python's standard-library
`decimal.Decimal` at 60 significant digits, padded by a relative `1e-45`
safety margin in the certifying direction, then converted to an exact
`fractions.Fraction` for the actual comparison.

## What passed

All three scripts pass (`overall_pass: true` in each, and in the combined
`results.json`).

## Findings

**every_site_core.py: no discrepancy; the every-site common-core lemma
holds everywhere checked.** For all five BB1 comparisons at `N=2,3,4`
(fifteen (comparison,N) instances, using two additional non-adjacent
centered-box examples for comparison 4 and two genuinely non-cubic cuboid
examples for comparison 5), every independently-built source term lies at
coarse l-infinity distance at least `N-|u|_inf` from every site `u` of
`Lambda_N`; the minimum slack is `0` (the bound attained, exactly as the
BB1 reverse report states for the nested comparisons) for comparisons 1-3
and the F1 branch of comparison 4, and small positive integers for the more
generously-separated general-volume examples. No failure was found. The
exact source-term counts this script finds independently --
`152/296/488` new F1 stars, `3920/7224/11536` new F2 faces and
`616/1344/2352` F1-vs-F2 extra faces at `N=2,3,4` -- match the BB1 reverse
report's own closed forms `8(3N^2+3N+1)`, `56(9N^2+14N+6)` and
`28N(5N+1)` exactly, giving independent confidence in the from-scratch
reconstruction.

**translation_faces.py: no discrepancy; the coarse-translation claim and
the histogram pitfall are both confirmed exactly.** Exactly 8 of the 64
fine translations in the period window are coarse, exactly matching
`(4v_x,2v_y,v_z)` for `v` in `{0,1}^3`; the reverse report's own witness
(`t=(1,0,0)`) is reproduced independently. The requested per-anchor
owner-type histogram check is confirmed to be uninformative: it "accepts"
all 56 non-coarse translations (as well as the 8 true ones), because the
owner-type histogram is anchor-independent by construction.

**item5_range.py: two findings worth recording, neither a contradiction of
an admitted claim.** (1) This script's own certified `K5` on
`5<=N<=14000` (about `5.1e-9` to `5.5e-9`, attained at `N=5` for every
constant set) is valid but substantially **tighter** (by a factor of about
2.6) than the reverse producer's own reported
`item5_K5_certified_5_to_14000` (about `1.37e-8` to `1.42e-8`). Since this
script's per-N bracket values agree with the reverse producer's own
tabulated values to `1e-9`-`1e-12` relative precision, the gap is in how
the whole-range certificate was assembled (evidently with some extra
margin), not in any disagreement about a per-N value. (2) The bracket
**exceeds 2** (the trivial universal bound) at all three of `N=14419`,
`14420` and `14421` for every constant set checked -- not only at
`N=14421`, the single point the reverse report names as a witness that the
bound is "vacuous". A finer scan (`N=14400`-`14425`, reverse `F1`
constants) finds the bracket first exceeds 2 at `N=14419` and stays above
2 through `14425`, with no recovery in that window. This **refines** but
does not **contradict** the reverse report: the report's own certified
range stops at `N=14000`, and its "vacuous from `N=14421` on" remark never
claims `N=14421` is the *first* such point, only *a* witness of it.

## Files

- `every_site_core.py` -- independent exact enumeration (`N=2,3,4`, all
  five BB1 comparisons, every site of `Lambda_N`) of the every-site
  common-core lemma (Lemma B5 / Theorem B6, form (b) of
  `parameters.coefficient_input`).
- `translation_faces.py` -- independent face-by-face check of BB2 item 4's
  coarse-translation lemma over the full 64-translation period window, plus
  the per-anchor histogram-pitfall demonstration.
- `item5_range.py` -- independent exact-arithmetic re-evaluation of the BB2
  item-5 correlation-function bracket's range (best `K5` on
  `5<=N<=14000`; whether it exceeds 2 at `N=14419,14420,14421`).
- `results.json` -- combined pass/fail and full raw output from all three
  scripts, plus a `findings` section summarizing the two disclosed,
  non-blocking observations above.

This lens admits nothing and counts zero research loops.
