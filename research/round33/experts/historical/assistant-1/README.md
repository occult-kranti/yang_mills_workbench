# Historical lens (Newton/Tesla) assistant scripts -- Round33 sub-round 1

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted assistant scripts
for the Newton/Tesla historical lens, delivering the three tests this lens's
own `research/round33/experts/historical/loop2-response.md` section 3 asked
for after BA1 and BA2 (this sub-round's two investigations) were frozen and
gated: (1) an independent exact enumeration of the whole-star supports, their
diameters, incidence and the F1/F2 boundary sources on the coarse factor
lattice; (2) a padding audit (folded into the same enumeration script, since
both concern the same F1/F2 box construction); (3) a ledger-completeness and
tier/route-labelling auditor over the BA1/BA2 producer reports and gates.

These scripts and this note count **zero research loops**: they are
cross-checks and previews for the lens, not a producer, skeptic or advisor
artifact, and nothing here is admission evidence. Nothing here reads or
imports `research/round33/forward/ba1/check.py`, `research/round33/reverse/
ba1/check.py`, `research/round33/forward/ba2/check.py` or `research/round33/
reverse/ba2/check.py` (or any other `check.py`); every geometric and
combinatorial construction is re-derived from scratch from the star
definition and the 21-omitted-face table in `research/round21/forward/i1/
report.md` sections 3 and 6, and from `research/round29/forward/am2/
report.md`. Only the forward/reverse producers' `report.md` prose and their
exported `output/results.json` (data, never code) are read for the final
comparison, together with `research/round33/advisor/ba1-gate.json`,
`ba2-gate.json`, `research/round33/contracts/ba1.json`, `ba2.json` and
`research/round33/advisor/plan.json` (the tier/route vocabulary).

Arithmetic: `diameters_and_sources.py` uses plain Python `int` throughout
(every quantity it claims is an exact integer count or lattice distance; no
`Fraction` is needed since nothing irrational or rational-but-non-integer
appears in this script's task). `ledger_audit.py` does no numeric
recomputation at all (it compares strings, sets and JSON structure), so it
needs neither `Fraction` nor floating point. Neither script uses `mpmath` or
`python-flint` (no irrational bound appears in either task).

Read before writing: `research/round33/experts/historical/loop2-response.md`
section 3, `research/round33/experts/historical/update-1.md`,
`research/round21/forward/i1/report.md` sections 3 and 6, `research/round29/
forward/am2/report.md`, `research/round33/contracts/ba1.json` and `ba2.json`
(frozen), `research/round33/advisor/plan.json`, `research/round33/advisor/
ba1-gate.json` and `ba2-gate.json`, `research/round33/forward/ba1/report.md`
and `output/results.json`, `research/round33/reverse/ba1/report.md` and
`output/results.json`, `research/round33/forward/ba2/report.md` and
`output/results.json`, `research/round33/reverse/ba2/report.md` and
`output/results.json`, and `research/round32/experts/historical/assistant-4/`
(this package's README/results.json layout convention; its scripts are not
imported, only its file layout is followed).

## How to run

```bash
python3 -B research/round33/experts/historical/assistant-1/diameters_and_sources.py
python3 -B research/round33/experts/historical/assistant-1/ledger_audit.py
```

Each script is standalone, prints its own JSON report to stdout, and exits 0
iff its `overall_pass` is `true`. Both were also run under `python3 -B -O`
and produced byte-identical stdout.

## What each script does

**`diameters_and_sources.py`.** Reconstructs, entirely independently of any
producer code, the whole star `S = {0,e_x,e_y,e_z}` and the 21 individual
omitted-face entries of I1's anchored face table (six distinct owner-set
types: `{0,e_y}` x3, `{0,e_x}` x1, `{0,e_x,e_y}` x1, `{0,e_z}` x10,
`{0,e_x,e_z}` x2, `{0,e_y,e_z}` x4), then on `Lambda_N = [-N,N]^3` for
`N = 2, 3, 4`:

- **Diameters.** Confirms by enumeration that the whole star has
  l-infinity diameter 1 and l1 diameter 2 (matching the star diameter
  `d_X=1` named in the BA1 gate's model field and the l1 diameter 2 stated
  in the BA1 forward report), and that every one of the six owner-set
  types has l-infinity diameter at most 1 and l1 diameter at most 2.
- **Incidence.** Confirms every bulk site is met by exactly 4 stars
  (`u in b+S` iff `b in u-S`, incoming anchors included -- the fact behind
  `J<=28|tau|`), that exactly 7 distinct anchors' stars meet
  `R={0,e_z}` (`(0-S) union (e_z-S)`, matching AY1/round32's incident-anchor
  count independently re-derived here for round33), that 49 individual
  faces touch each of `0` and `e_z` (16 touching both), giving 82 faces
  meeting `R` and 10 with owner set exactly inside `R`, and that there are
  exactly 15 distinct owner-set "shapes" as seen translated to one site --
  all of these are the literal pins named in both contracts'
  `face_count_all_sites` control ("49 faces per factor, 15 owner sets, 82
  meeting R, 10 inside R").
- **F1-versus-F2 extra faces.** Independently enumerates, at each
  `N = 2, 3, 4`, every face retained by F2 but not by F1 (owner set inside
  `Lambda_N`, whole star not inside `Lambda_N`): the count (616, 1344,
  2352, matching the closed form `28N(5N+1)`), the anchors (60, 126, 216 --
  `(2N+1)^3-(2N)^3-1`, confirming the sole "zero-face" anchor is the corner
  `(N,N,N)`), the per-anchor-type class table (17, 13, 5 faces when
  exactly one coordinate equals `N`; 10, 3, 1 when two do; 0 at the
  corner -- matching the BA2 gate's own class table literally), and the
  exact l1 and l-infinity distances of every owner-set point from `0` and
  from `e_z` (minimum `N` from `0`, `N-1` from `e_z`, in *both* metrics,
  both attained -- matching the BA1 forward report's "l1 gives the same
  values" remark and the BA2 reports' l1-only derivation).
- **F2 padding sites.** Independently rebuilds `B_+ = union_{b in
  Lambda_N}(b+S)` (the full-star union, not the F2-retained union) and
  confirms `|B_+ \ Lambda_N| = 3(2N+1)^2` (75, 147, 243 at `N=2,3,4`),
  matching the BA2 reverse report's stated formula and its `N=2,3` literal
  values.
- **Nested-comparison sources.** Independently counts the new F1 whole
  stars from `Lambda_N` to `Lambda_{N+1}` (152, 296, 488, matching
  `8(3N^2+3N+1)`) and the new F2 faces (3920, 7224, 11536, matching
  `56(9N^2+14N+6)`), both confirmed as well by direct subtraction of the
  two independently-checked closed forms `(2N)^3` (F1) and
  `28N(2N+1)(3N+1)` (F2).
- **Comparison.** Every one of the above numbers is checked against the
  BA1/BA2 gates' text and the four producers' `report.md` prose (the
  literal instance counts live in the reports; the gates state the general
  formulas, which is also checked).

**`ledger_audit.py`.** Two audits, for BA1 and BA2 separately:

- **Ledger completeness.** Every entry of the frozen contract's
  `preregistration.error_terms_itemized` (BA1: `weighted_contraction_loss`,
  `boundary_source_terms`, `order_versus_distance_count`,
  `exact_first_order_remainder`, `cutoff_uniformity`, `arithmetic`; BA2:
  `lieb_robinson_tail`, `duhamel_boundary_sum`, `interaction_picture_onsite`,
  `inner_family_constants`, `arithmetic`) is checked to appear as a table
  row in *both* the forward and reverse `report.md`, and as a populated key
  of *both* producers' `output/results.json` ledger dict
  (`error_terms_itemized` forward, `error_ledger` reverse; an entry charged
  `not_applicable` with a stated reason still counts, per the contracts'
  own `error_terms_rule`).
- **Tier/route labelling.** `plan.json`'s vocabulary is read directly from
  its own `tier_label_rule` sentence (with an assertion that the two sets it
  names -- 5 tiers, 6 routes -- partition its `tier_names_allowed` list
  exactly, so the script fails loudly rather than silently if that
  vocabulary is ever edited without updating the rule text). The script
  checks (i) every tier/route word occurring anywhere in a gate's
  `accepted`+`decision` text is a member of the correct vocabulary set, and
  (ii) every explicit `K...=<fraction>` (or `K'_...`) constant is
  co-located, in the same sentence, with at least one tier word and one
  route word.

## What passed

Both scripts pass (`overall_pass: true` in each, and in the combined
`results.json`).

## Findings (no discrepancy in any numeric quantity)

**Numeric agreement is exact and complete.** Every quantity independently
recomputed by `diameters_and_sources.py` -- the star/owner-set diameters,
the 4-star and 7-anchor incidence counts, the 49/82/16/10/15 face-incidence
pins, the `28N(5N+1)` extra-face count and its 17/13/5/10/3/1/0 class table,
the `3(2N+1)^2` padding-site count, and the `8(3N^2+3N+1)` /
`56(9N^2+14N+6)` nested-comparison counts, all at `N=2,3,4` -- agrees
bit-for-bit with the BA1 and BA2 gates and with the forward and reverse
producer reports. No numeric disagreement was found anywhere.

**Ledger completeness is exact.** Every one of BA1's six and BA2's five
itemized error terms is charged (or explicitly marked `not_applicable` with
a stated reason) in both producers' report tables and both producers'
exported `results.json` ledgers, for both loops. No channel is silently
folded into another or left empty.

**Tier/route labelling: one non-blocking, disclosed gap.** No
out-of-vocabulary or swapped-set tier/route word was found anywhere in
either gate's text. Within BA1's gate text, all 6 explicit `K...=<fraction>`
constants are co-located, in the same sentence, with both a tier word and a
route word. Within **BA2's** gate text, only 2 of 5 explicit constants
(`K_cmp`, in both the `accepted` and `decision` fields) are co-located with
a tier word; `K'_cmp` is co-located with its route (`duhamel_inner_f2`) but
not with a tier word in the same sentence; and the two within-family Cauchy
constants `K_F1` and `K_F2` are named in the gate text only with descriptive
phrases ("forward, faces charged once, inner F1", "reverse, whole stars,
inner F1 on `Lambda_M`", etc.), never repeating the literal vocabulary words
`polynomial_lieb_robinson`, `duhamel_inner_f1` or `duhamel_inner_f2` in the
same sentence as the number. This is a **syntactic** finding about the
gate's own prose, not a semantic one: both underlying producer reports carry
an explicit table row naming the tier `polynomial_lieb_robinson` for the
corresponding constants (`K_cmp`/`c1`/`c2` in the reverse report, lines
298-300; `K_cmp`/`K_c1`/`K_c2` in the forward report), so the frozen
evidence trail itself is fully labelled -- it is only the gate's summary
prose that elides the repeated vocabulary word for the within-family
constants. Separately, BA1's *decision* text paraphrases the crude tier as
"crude tiers" rather than repeating the literal word `crude_majorant` (which
does appear in BA1's `accepted` text); the same observation applies. Both
are recorded here as findings for the record, not as defects this
zero-research-loop package can or should adjudicate.

## Files

- `diameters_and_sources.py` -- independent exact enumeration (`N=2,3,4`) of
  the whole-star and owner-set diameters, the per-site and per-`R`
  incidence, the F1-versus-F2 extra-face source (count, anchors, class
  table, distances), the F2 padding-site count, and the nested-comparison
  new-star/new-face counts; cross-checked against the BA1/BA2 gates and the
  four producers' reports.
- `ledger_audit.py` -- ledger-completeness and tier/route-labelling auditor
  over the BA1/BA2 contracts, gates and the four producers' reports/
  `results.json`.
- `results.json` -- combined pass/fail and full raw output from both
  scripts, plus a `findings` section summarizing the one disclosed,
  non-blocking tier/route-labelling gap above.

This lens admits nothing and counts zero research loops.
