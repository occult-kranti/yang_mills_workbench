# Historical lens (Newton/Tesla) assistant scripts -- Round33 sub-round 3

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted assistant scripts
for the Newton/Tesla historical lens, delivering three independent
cross-checks for this sub-round's two investigations, BC1 and BC2: (1) an
independent exact enumeration of the route-B partition, incidence and
every-site common core of the uniform model BC2 re-derives (AX1/AX2's
grouping: one whole star of 21 omitted faces plus one single-factor group
of 3 selected faces per factor); (2) an independent, exact-arithmetic
recomputation of `N_sign` (BC1's finite-box sign corollary) from `C'`, `q`
and the AW2 gate's own enclosure endpoints, plus the exact robustness range
of `C'` giving the same `N_sign`; (3) a structural audit of the reviewed
obligations table `research/round33/skeptic/bc1.json` carries, checking
gate references, stated scopes, the `O1a`/`O1b` split, and that every open
row has a missing premise and a candidate route.

These scripts and this note count **zero research loops**: they are
cross-checks for the lens, not a producer, skeptic or advisor artifact, and
nothing here is admission evidence. Nothing here reads or imports
`research/round33/forward/bc1/check.py`, `research/round33/forward/bc2/
check.py`, `research/round33/skeptic/bc1_check.py`, `research/round33/
skeptic/bc1_postreview_check.py`, `research/round33/skeptic/bc2_check.py`,
`research/round33/skeptic/bc2_postreview_check.py` or any other `check.py`.
Nothing here reads `research/round33/forward/bd1/`, `research/round33/
forward/bd2/` or `research/round33/reverse/bd1/` (in production at the time
this package was written).

`route_b_incidence.py`'s partition, per-site inputs and R-incidence
construction is re-derived from scratch from the star/face definitions in
`research/round21/forward/i1/report.md` (sections 2-3 and 6), `research/
round29/forward/am2/report.md` (`S={0,e_x,e_y,e_z}`), and `research/
round32/forward/ax1/report.md` (the route-B grouping: one whole star `phi_b`
of 21 omitted faces plus one single-factor group `psi_b` of 3 selected
faces per factor, and the incidence sentence "seven stars and exactly two
single-factor groups meet `R`"); only the frozen `research/round33/
contracts/bc2.json`, the AX1 gate and the BC2 forward producer's own
`report.md` prose and exported `output/results.json` (data, never code) are
read for the final comparison. `n_sign.py` parses `K_2^+` as an exact
rational directly out of the plain text of the hash-verified AW2 gate
(`research/round32/advisor/aw2-gate.json`) and `C'`, `q` directly out of
the hash-verified BB2 gate (`research/round33/advisor/bb2-gate.json`),
computes `N_sign` and its robustness range from scratch, and only then
compares against `research/round33/forward/bc1/report.md`, `output/
results.json` and `research/round33/advisor/bc1-gate.json` (data, never code).
`obligations_audit.py` reads only `research/round33/skeptic/bc1.json`
(its `reviewed_obligations_table`, `o1_decision` and
`obligations_reconciliation` fields) and resolves gate references by a
plain filesystem glob, never by re-deriving any admitted constant.

Arithmetic: `route_b_incidence.py` uses plain Python `int` throughout
(every quantity it claims is an exact integer lattice coordinate,
l-infinity distance or face/anchor count; no floats, no `Fraction`).
`n_sign.py` uses `fractions.Fraction` for every quantity that enters a
pass/fail comparison (no floats decide anything; decimals are labelled
previews only). `obligations_audit.py` does no numeric computation at all
(it audits JSON text and structure), so it needs neither `Fraction` nor
floating point. No script here uses `mpmath` or `python-flint`.

Read before writing: `research/round33/contracts/bc1.json` and `bc2.json`
(frozen), `research/round33/advisor/bc1-gate.json` and `bc2-gate.json`,
`research/round33/advisor/bb2-gate.json`, `research/round33/forward/bc1/
report.md` and `output/results.json`, `research/round33/forward/bc2/
report.md` and `output/results.json`, `research/round33/skeptic/bc1.json`
(the reviewed obligations table), `research/round32/advisor/ax1-gate.json`,
`ax2-gate.json`, `aw2-gate.json`, `av2-gate.json`, `research/round32/
forward/ax1/report.md`, `research/round21/forward/i1/report.md` (sections
2-3 and 6), `research/round29/forward/am2/report.md`, and `research/
round33/experts/historical/assistant-2/README.md` (this package's
README/results.json layout convention; its scripts are not imported, only
its file layout is followed).

## How to run

```bash
python3 -B research/round33/experts/historical/assistant-3/route_b_incidence.py
python3 -B research/round33/experts/historical/assistant-3/n_sign.py
python3 -B research/round33/experts/historical/assistant-3/obligations_audit.py
```

Each script is standalone, prints its own JSON report to stdout, and exits 0
iff its `overall_pass` is `true`. All three were also run under
`python3 -B -O` and produced byte-identical stdout.

## What each script does

**`route_b_incidence.py`.** Independently rebuilds, entirely from scratch,
the 24-class `(orientation, r, s)` face table of I1 sections 2-3, the six
omitted owner-set types (matching I1's `{0,e_y}` x3, `{0,e_x}` x1,
`{0,e_x,e_y}` x1, `{0,e_z}` x10, `{0,e_x,e_z}` x2, `{0,e_y,e_z}` x4) and the
route-B grouping of AX1 (one whole star of the 21 omitted faces plus one
single-factor group of the 3 selected faces, per factor). It then:

- **Partitions a genuine fine grid.** Over the 5x5x5=125 coarse anchors of
  `Lambda_2`, at every one of the 8 `(x mod 4, y mod 2)` residues and 3
  orientations (3000 plaquette instances, matching the scale of the BC2
  forward producer's own brute-force check), every plaquette is assigned
  to exactly one route-B group -- the single-factor group of its own coarse
  anchor if selected, otherwise that anchor's whole star -- giving 250
  groups (125 stars of 21 faces, 125 singles of 3 faces).
- **Per-site inputs.** For a fixed factor `u`, independently enumerates
  every face whose owner set contains `u` (52: 49 omitted from the four
  incoming stars at `u-S` plus 3 selected from the single group at `u`),
  every distinct absolute owner set containing `u` (16, with multiplicities
  `{1x5, 2x3, 3x3, 4x3, 10x2}`), and every interaction group containing `u`
  (5: 4 stars + 1 single group).
- **Incidence with `R={0,e_z}`.** Independently finds the star anchors
  `R-S` (7 distinct points) and the single anchors in `R` (2 points), then
  recomputes, face by face, the meeting/inside counts for each of the 9
  groups: 153 faces charged, 88 meeting `R`, 16 inside `R`, 72 straddling.
- **Every-site common core (Lemma D5, re-derived from scratch).** At
  `N=2,3`, for every site `u` of `Lambda_N` and every new source face
  (a newly-retained whole star's 21 faces, or a newly-retained single
  group's 3 faces) going to `Lambda_{N+1}`, confirms the face lies at
  coarse l-infinity distance at least `N-|u|_inf` from `u` (`min_slack=0`,
  the bound attained), and cross-checks the exact source-face counts
  (3846 at `N=2`, 7374 at `N=3`) against both a closed-form formula
  (`8(3N^2+3N+1)` new stars, `(2N+3)^3-(2N+1)^3` new single anchors) and
  the BC2 forward producer's own `output/results.json`.
- **Comparison.** Every one of the above numbers is checked against the
  BC2 contract's required item 1, the AX1 gate's incidence sentence, the
  AX1 forward report, and the BC2 forward report's prose and `output/
  results.json` fields (`route_b_partition_brute_force`,
  `route_b_per_site_inputs_derived`, `route_b_incidence_on_R`,
  `route_b_every_site_common_core`).

**`n_sign.py`.** Parses `K_2^+` as an exact rational directly out of the
plain text of the hash-verified AW2 gate, and `C'=4/984375`, `q=1/64`
directly out of the hash-verified BB2 gate, using patterns specific enough
to isolate the `nested_telescoping` **bound** value the BC1 contract names
(rejecting the BB2 gate's own labelled `union_comparison` value
`C'=1/250000` and its labelled re-evaluated preview, both of which a bare
`C'=<num>/<den>` pattern would also match -- confirmed live: an earlier,
unqualified version of the parser raised on exactly this ambiguity). From
these it independently recomputes `L=tau/144-K_2^+ tau^2` and
`U=tau/144+K_2^+ tau^2` at `tau=10^-8`, confirms both equal the AW2 gate's
own literal endpoint rationals bit-for-bit (via a second, independent
regex over the gate's own `[num1/D, num2/D], D=...` spelling), then finds
`N_sign` -- the least `N` at least 2 with `C' q^(N-1)` strictly below `L` --
by a monotone from-scratch scan, and tabulates the widening `C' q^(N-1)`
and the certified/not-certified flag at `N=2,3,4,5,6`. Finally, holding `q`
and `L` fixed, it computes the exact **robustness range** of `C'` giving
the same `N_sign=4`: `C' q^(N_sign-1) < L` and `C' q^(N_sign-2) >= L` give
`C'` in `[L/q^2, L/q^3)`, both endpoints computed exactly, with two
independent boundary checks (`N_sign` recomputed at the lower endpoint and
just below the upper endpoint).

**`obligations_audit.py`.** Parses the `reviewed_obligations_table` of
`research/round33/skeptic/bc1.json` (21 rows: `O1a`, `O1b`, `O2`-`O6`,
`N1`-`N14`) and checks, for every row: (i) if `status` is
`closed_within_scope`, that `closing_gate_and_scope` names at least one
`<TOKEN> gate` reference (a two-letter-plus-digit token, e.g. `BB2`) that
resolves to a real `research/round*/advisor/<token>-gate.json` file on
disk, and that the same text states an explicit scope (contains the word
"scope"); (ii) that `O1a` and `O1b` are both present, with `O1a`
`closed_within_scope` and `O1b` `open` (the BC1 gate's own reviewed split
of the AY2 row `O1`, and that the un-split producer row `O1` does not
reappear); (iii) if `status` is `open`, that `missing_premise` and
`candidate_route` are both non-blank and not literally the word "none"
(while `closing_gate_and_scope` for an open row is, correctly, "none
(open)"). It also cross-checks the table's total row count and the
closed/open partition against the skeptic packet's own
`obligations_reconciliation.reviewed_rows` field.

## What passed

All three scripts pass (`overall_pass: true` in each, and in the combined
`results.json`).

## Findings

**route_b_incidence.py: no discrepancy; every pinned route-B number holds
exactly.** The independent fine-grid partition (3000 plaquette instances,
250 groups) matches the BC2 forward producer's own brute-force check
exactly. The per-site inputs (52 faces, 16 owner sets, 5 interaction
groups, multiplicities `{1x5,2x3,3x3,4x3,10x2}`) and the `R`-incidence
(7 stars, 2 singles, 153/88/16/72) match the BC2 contract's required item
1, the AX1 gate's incidence sentence and the BC2 forward `results.json`
bit-for-bit. The every-site common core at `N=2,3` (source-face counts
3846 and 7374, `min_slack=0` throughout) matches the BC2 forward
`results.json` and this script's own closed-form cross-check exactly. No
failure was found anywhere.

**n_sign.py: no discrepancy in `N_sign`, plus one new non-blocking
finding.** `N_sign=4` is confirmed exactly, matching the BC1 forward
report, its `output/results.json` and the BC1 gate bit-for-bit; the
widening table at `N=2..6` and the certified/not-certified flags agree
with the BC1 forward `results.json` row for row. **New finding:** the
exact robustness range of `C'` giving the same `N_sign=4` (holding
`q=1/64` and `L` fixed) is `C'` in `[L/q^2, L/q^3)`, approximately
`[2.8307e-7, 1.8117e-5)` -- a factor-of-64 window, since each unit step in
`N_sign` moves the boundary by exactly one power of `q`. The BB2 gate's
actual bound value `C'=4/984375` (about `4.0635e-6`) sits comfortably
inside this range: it could increase by a factor of about 4.46 (this
figure coincides with the already-labelled ratio `L/(C' q^3)` about
`4.4584` that the BC1 report and gate record as "labelled information, not
claimed" -- confirming, from a different direction, that the two
quantities are the same ratio) or decrease by a factor of about 14.35
before `N_sign` would change. This range was not previously stated
explicitly in any BC1 or BC2 record; it is reported here as a labelled
observation, not a bound on anything admitted, and does not contradict or
extend the BC1 gate's own scope.

**obligations_audit.py: no discrepancy; the reviewed table is structurally
complete.** All 21 rows are present, matching the skeptic packet's own
stated row count. All 6 closed rows name an existing gate (`BA1`, `BA2`
and/or `BB2`, every one resolving to a real `research/round33/advisor/
<token>-gate.json` file) and state an explicit scope. `O1a` and `O1b` are
both present with the expected statuses, and the unsplit `O1` row is
correctly absent. All 15 open rows carry a genuine `missing_premise` and
`candidate_route`. No structural gap was found.

## Files

- `route_b_incidence.py` -- independent exact enumeration (fine-grid
  partition, per-site inputs, `R`-incidence, and the every-site common core
  at `N=2,3`) of the route-B uniform model's construction, compared with
  the BC2 producer results and the AX1/AX2 gates.
- `n_sign.py` -- independent exact recomputation of `N_sign` from
  `C'=4/984375`, `q=1/64` and the AW2 gate's own endpoints, the widenings
  at `N=2..6`, and the exact robustness range of `C'` giving the same
  `N_sign`, compared with the BC1 gate.
- `obligations_audit.py` -- a structural audit of the reviewed obligations
  table in `research/round33/skeptic/bc1.json`.
- `results.json` -- combined pass/fail and full raw output from all three
  scripts, plus a `findings` section summarizing the results above.

This lens admits nothing and counts zero research loops.
