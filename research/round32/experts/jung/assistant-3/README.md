# Jung/Pauli lens, Round32 sub-round 3, assistant-3

Pre-registration audits and tests for the lens (`update-2.md` section 5, the three
tests requested after sub-round 2; the calling task). **These outputs count zero
research loops.** Nothing here is a producer, a contract, a gate or a skeptical
review; nothing computed here is read back into any contract, gate or skeptical
review. Human project author: Hruday N M (BUNZEEY); AI-assisted. Standard library
only (`fractions`, `json`, `re`, `pathlib`, `datetime`). Run every script with
`python3 -B`.

Read before this work: `research/round32/experts/jung/update-2.md` section 5,
`research/round32/experts/jung/assistant-2/` (reused its `preregistration_audit_2.py`
and `common2.py` structural-check logic, generalised from AW1/AW2/AX1..AZ2 with
the pre-extension vocabulary; re-implemented, not imported, exactly as
assistant-2's own docstring generalised assistant-1's `common.py`),
`research/round32/advisor/plan.json` (the pre-registration vocabulary extension
recorded 2026-09-24, after the Jung assistant-2 audit), `research/round32/
contracts/ax1.json` and `ax2.json` (both `frozen_before_production`),
`research/round32/advisor/ax1-gate.json`, `research/round32/skeptic/ax1.json`
(and `ax1.md`, read as bonus coverage), `research/round32/forward/ax1/report.md`
and `output/results.json`, `research/round32/reverse/ax1/report.md` and
`output/results.json`, and the draft contracts `ay1.json`, `ay2.json`, `az1.json`,
`az2.json`.

## Files

- `common3.py` -- shared helpers: `AuditError`/`require`/`expect_rejected`,
  `load_json`/`rat`/`is_rational`/`s`/`merge_results`, generic contract loaders
  for any round-32 contract at either `draft` or `frozen_before_production`
  status, the closed pre-registration vocabularies re-declared from common2.py,
  and the plan.json extension's new pieces: `is_tau_linear` (a narrow regex for
  exact tau-linear expressions like `'tau/24'`), `ALLOWED_DIRECTION_EXT`,
  `ALLOWED_REFERENCE_ROUTE_EXT_BASE` + the `'n/a'` rule, and `plan_extension_covers`
  (a defensive check that `advisor/plan.json` still carries the four-field
  extension this module implements). Does **not** import `forward/*/check.py`,
  `reverse/*/check.py`, or assistant-1's/assistant-2's scripts.
- `preregistration_audit_3.py` -- script 1/3 (item 1 of the calling task).
- `forbidden_wording_grep.py` -- script 2/3 (item 2).
- `j0_prereg_constant.py` -- script 3/3 (item 3).
- `results.json` -- merged output of all three scripts. Produced by
  `rm -f results.json && python3 -B preregistration_audit_3.py &&
  python3 -B forbidden_wording_grep.py && python3 -B j0_prereg_constant.py`.
  Byte-identical under normal and `-O` Python (checked; stdout is also
  byte-identical under both).

## Results

### 1. `preregistration_audit_3.py` -- PASS

Re-runs assistant-2's structural pre-registration audit on AX1, AX2 (both
`frozen_before_production`) and the four sub-round-4/5 drafts AY1, AY2, AZ1, AZ2
(each read at whatever status is on disk; all four were still `draft` at run
time), using the vocabulary `advisor/plan.json`'s
`preregistration_vocabulary_extensions` block adds on top of assistant-2's
closed schema:

- `selected_triple_alpha_units` may be a 3-element list of exact-rational OR
  tau-linear strings (`'tau/24'`), or the sentinel string `'n/a (finite graph)'`
  tied to an `'FG('`-prefixed `model_id`;
- `direction` gains `'statement+skeptic'`;
- `observable.reference_route` gains `'n/a'`, restricted to statement loops
  (`direction` in `{statement-only, statement+skeptic}`) with the reason stated
  in `error_terms_itemized`;
- `tau.value` may be `'grid'` with `parameters.tau_FG_grid` populated (finite-
  graph loops), in addition to an exact rational.

Each of the four amended fields is checked **twice** per contract -- a
`[pre-extension]` entry (assistant-2's original rule, kept for visibility) and
an `[extended]` entry (the one that actually gates pass/fail here) -- so the
extension's effect is visible in `results.json`, not just its outcome.

**All six contracts pass** (`preregistration_audit_3.pass == true`):

- **AX1, AX2**: `preregistration.selected_triple_alpha_units=['tau/24','tau/24',
  'tau/24']` fails `[pre-extension]` (exactly the gap assistant-2 found) and
  passes `[extended]`. This matches `advisor/ax1-gate.json`'s own limitations
  entry verbatim: "the symbolic tau-dependent selected triple in the frozen AX1
  preregistration is covered by the plan.json vocabulary extension recorded
  after the freeze ..., contract unamended; the gate should record it as an
  accepted extension" -- which the gate does. Every other field, including
  `controls_required.ids == controls` (28/28 for AX1, 25/25 for AX2,
  byte-for-byte), passes unchanged.
- **AY1**: passes every field under either reading (it reuses the AV1/AW1 model
  shape unmodified: numeric zero triple, `paired` direction, `haar` route), same
  as assistant-2 found for it against the pre-extension vocabulary.
- **AY2, AZ1**: `direction='statement+skeptic'` and `observable.reference_route
  ='n/a'` both fail `[pre-extension]` (assistant-2's flagged gaps) and pass
  `[extended]` -- the `'n/a'` route passes because both are statement loops
  whose sole `error_terms_itemized` entry is `"not_applicable: statement loop
  (reason: no new numerical certificate)"`, which states the required reason.
- **AZ2**: `selected_triple_alpha_units='n/a (finite graph)'` (tied to
  `model_id='FG(two-plaquette, j_max, tau_FG, I1.5, gauge-invariant)'`) and
  `tau.value='grid'` (tied to `parameters.tau_FG_grid=['1/1000','1/100','1/10']`)
  both fail `[pre-extension]` and pass `[extended]` -- the two remaining gaps
  assistant-2 found, both closed by exactly the extension named for each.

**AX1-specific items** (production is complete; AX2 is frozen but not yet in
production -- only `forward/ax2/inputs/` exists on disk, no `report.md`,
`output/`, gate or skeptic review yet, so the equivalent AX2 items are recorded
`not_yet_applicable`, mirroring assistant-2's AW2 treatment at the same point in
sub-round 2, and are not counted toward the overall pass/fail):

- Both `forward/ax1/output/results.json` (52 checks) and
  `reverse/ax1/output/results.json` (58 checks) contain every one of AX1's 28
  control ids; no gap.
- `advisor/ax1-gate.json.accepted` equals `skeptic/ax1.json.supported_statement`
  **exactly** (string equality), and `advisor/ax1-gate.json.limitations` equals
  `skeptic/ax1.json.limitations` **exactly** (17/17 entries, same order) -- the
  final skeptic verdict, not the pre-comparison package assistant-2 had to defer
  on for AW2. No mirror gap here.

Full per-field, per-contract detail (including every `[pre-extension]`/
`[extended]` pair and its reason string) is in `results.json`.

### 2. `forbidden_wording_grep.py` -- PASS

Greps six required AX1 files, case-insensitively, for `"weak coupling"` and
`"continuum"` (regex also catches `weak-coupling`/`weak_coupling` and
`continuum_claim`-style identifier spellings): `forward/ax1/report.md`,
`reverse/ax1/report.md`, `forward/ax1/output/results.json`,
`reverse/ax1/output/results.json`, `advisor/ax1-gate.json`, `skeptic/ax1.json`.
(`skeptic/ax1.md`, the narrative review, is scanned too as bonus, non-required
coverage.)

**79 occurrences across the six required files, 0 classified `AFFIRMATIVE`.**
Every occurrence prints with a ~360-character context window (plus, for `.json`
files, the nearest enclosing key found by an unbounded backward scan -- needed
because e.g. a `"rejected_mutations"` array's key sits well outside a fixed
character radius from the string it lists) and is classified by a cue search
(`never`, `not`, `no`, `false`, `reject*`, `exclu*`, `forbidden`, `mutation`,
`tamper`, `rebound`, `claim_exclusions`, ...). Every one of the 79 falls into one
of: an explicit false claim flag (`"continuum_claim": false`,
`"weak_coupling_claim": false`), a `claim_exclusions`/`exclusions`/`forbidden`
list entry, a rejected-mutation table/array entry (e.g. `uniform_label_
strong_coupling`'s rejected mutations `"weak_coupling_label"`,
`"continuum_label"`; `coherent_evidence_tampering`'s `"continuum_flag_hash_
rebound"`), or a direct negation ("It is never described as weak coupling or as
a continuum approach... The checker scans the label and verdict strings and
rejects either phrase"). None reads as an affirmative claim. (Two occurrences in
the bonus `skeptic/ax1.md` scan needed the same "false" cue and are likewise
`negation_or_exclusion`.)

Also confirms the sub-round-2 scratch-isolation disclosure rule (`update-2.md`
section 1, "Rule to add") is honoured by both AX1 producers: `forward/ax1/
report.md` names `/tmp/claude-0/ax1-forward-private/` as its private scratch
subfolder, and `reverse/ax1/report.md` names `/tmp/claude-0/ax1-reverse-private/`
-- both pass a check for a private-subfolder path plus a disclosure-cue phrase
("scratchpad disclosure", "my scratch work", "scratch work stayed", ...).

### 3. `j0_prereg_constant.py` -- PASS

Independently replays `update-2.md` section 5, item 2, without importing either
producer's `check.py`:

1. **Contract text.** `contracts/ax1.json.parameters.J0_resolution` states
   Resolution R1 (`J_0'=29/10^8`) with both exact contraction inequalities
   written out, and names Resolution R2 (`|tau|<=7/725000000`) as a named,
   excluded alternative -- "not selected" in the contract's own words, i.e.
   named and excluded in advance rather than chosen after the fact.
   `preregistration.frozen_before_any_outcome` is `true`.
2. **Recomputed from scratch as exact `Fraction`s** (not parsed from the
   contract's text): `J_0' * 148/7 = 1073/175000000 < 1/64` and
   `2 * J_0' * 352 = 319/1562500 < 1`, both confirmed. Also confirms the
   re-freeze is substantive, not cosmetic: the route-B per-site sum
   `29 * 10^-8 = 29/10^8` genuinely exceeds AM2's old `J_0=7/25000000` at the
   cap, so the old constant really would fail here.
3. **Timestamps.** Neither `forward/ax1/freeze.json` nor `reverse/ax1/
   freeze.json` carries an internal timestamp field (their keys are
   `contract_sha256`, `direction`, `independent_before_current_counterpart_
   exchange`, `loop`, `normal_optimized_identical`, `sources`, `verdict`) --
   recorded explicitly, since the calling task's "if present" timestamp
   condition therefore has nothing to compare on either side. As a
   supplementary, non-cryptographic ordering signal, the filesystem mtimes of
   both `freeze.json` files and both `output/results.json` files (all four
   timestamped `2026-09-24T01:0x`-`01:08Z`) fall after the contract's own
   `frozen_at` (`2026-09-24T00:40:52.514703+00:00`), consistent with production
   happening after the pre-registered freeze; this is explicitly labelled a
   weaker check than the `contract_sha256` agreement (both `freeze.json` files
   record the same hash, matching the current `contracts/ax1.json` content),
   which is the load-bearing evidence.
4. **Reproduced exactly.** Both `forward/ax1/output/results.json` and
   `reverse/ax1/output/results.json`'s `j0_resolution` blocks carry
   `J0_prime=29/100000000`, `resolution='R1'`, and the self-map/contraction
   values equal to `1073/175000000`/`319/1562500` respectively (compared as
   `Fraction`s), and each has a passing `j0_resolution_declared` control check.

## Three planning notes for the lens about sub-round 4

**1. The mandatory sentence template for AY1/AY2 needs a named, checkable form
before AY1 leaves draft, the same way the J_0 re-freeze needed one before AX1's
producers wrote `check.py`.** `contracts/ay1.json` item 4 already requires "the
mandatory sentence template (Jung loop-2 response) in the report and the gate
fields `uniqueness_claimed:false`, `whole_sequence_claimed:false`,
`rate_claimed:false`," and `ay2.json`'s statement-loop deliverable includes "a
small exact checker verifying the constants and the mandatory sentence fields" --
but this task's reading list does not include `loop2-response.md`'s exact
sentence text verbatim, so a future assistant cannot yet confirm the template is
reproduced word-for-word rather than paraphrased. Before AY1/AY2 leave draft:
pin the exact sentence text (quoted, not summarized) as a contract parameter or
a `preregistration` field, the same way `ax1.json.parameters.J0_resolution`
pins the exact inequality text, so a `check.py` (and a later audit) can grep for
it verbatim instead of trusting a paraphrase. This sub-round's
`preregistration_audit_3.py` already confirms the *structural* half (the three
gate-field names exist in `ay1.json`'s required items); the *content* half (the
sentence's exact wording) is the open item.

**2. `uniqueness_claimed:false` and its siblings belong in `preregistration`,
not only in `required`/prose, so they are machine-checkable the same way
`continuum_claim`/`weak_coupling_claim` already are for AX1/AX2.** This audit's
`forbidden_wording_grep.py` could grep AX1's reports and results for "weak
coupling"/"continuum" precisely because those are recorded as explicit Boolean
claim flags (`"continuum_claim": false`) inside `output/results.json`, not just
mentioned in prose. `ay1.json`/`ay2.json` currently state
`uniqueness_claimed`/`whole_sequence_claimed`/`rate_claimed` (and AY1's
`local_closeness_not_uniqueness` control) only in `required` items and
`claim_exclusions` text. Before AY1/AY2 freeze: add these three gate-field names
explicitly to `preregistration` (e.g. a `gate_fields_required` list, parallel to
`hash_binding`), so a sub-round-5 assistant can grep `output/results.json` for
`"uniqueness_claimed": false` the exact same mechanical way this sub-round's
script 2 grepped for the forbidden wording, rather than having to trust prose
alone.

**3. Two named families frozen before comparison (AY1) sets a precedent worth
re-using explicitly for AZ1's trajectory and AZ2's finite graph, so "before
comparison" stays checkable, not just asserted.** `ay1.json.parameters.families`
already names both families before any producer runs ("centered whole-star boxes
Lambda_N (AQ1)"; "all-contained-face boxes with padding (I1 section 6)"), and its
controls `two_families_named`/`topology_named` exist precisely so a producer
cannot introduce a third, undeclared family mid-derivation or silently swap one
family's definition after seeing the other's result -- the same "frozen before
outcome" discipline the J_0 re-freeze needed and this sub-round's script 3
verified for it. AZ1 (`(a_n, g_n)` trajectory) and AZ2 (Round11 two-plaquette
graph) are each single-family statement/single-producer loops, so the analogous
risk is smaller, but AZ1's `trajectory_named` control and AZ2's
`finite_graph_model_id` control should be checked the same way once they leave
draft: confirm the trajectory/graph definition is pinned in `parameters` (not
just `model`/prose) *before* `forward/az1/report.md` or `forward/az2/report.md`
exists, using the same before/after file-timestamp method script 3 used for
AX1's `J0_resolution` (with the same mtime caveat: a supplementary signal, not a
substitute for checking the definition text itself did not change).

## Reproducing

```bash
cd research/round32/experts/jung/assistant-3
rm -f results.json
python3 -B preregistration_audit_3.py
python3 -B forbidden_wording_grep.py
python3 -B j0_prereg_constant.py
```

All three exit 0 (PASS). Byte-identical under `python3 -B` and `python3 -B -O`
(checked for all three scripts' stdout and the merged `results.json`).

Note: this repository is a live, concurrently-advancing workbench.
`preregistration_audit_3.py` reads AY1/AY2/AZ1/AZ2 at whatever status is
currently on disk (recorded per contract in `results.json`'s
`preregistration_audit_3.contracts_audited` and in the "observed contract
statuses" finding) rather than assuming `draft`; at the time this sub-round-3
audit was run, all four were still `draft` and AX2 was `frozen_before_production`
but not yet in production (no `forward/ax2/report.md` or `output/` on disk),
recorded as `not_yet_applicable` rather than scored.
