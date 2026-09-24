# Jung/Pauli lens, Round32 sub-round 5, assistant-5 (final integration audit)

The final pre-registration integration audit for Round32 (`advisor/panel-
update-4.md` item 7; `experts/jung/update-4.md` section 4, "Proposed
assistant tests after sub-round 5"). **These outputs count zero research
loops.** Nothing here is a producer, a contract, a gate or a skeptical
review; nothing computed here is read back into any contract, gate or
skeptical review; nothing here decides whether AV1-AZ2 are accepted (all
ten are already `accepted_within_scope`, per every gate and `research/
round32/HANDOFF.md`) -- only the advisor's gates and the skeptic's reviews
ever did that. Human project author: Hruday N M (BUNZEEY); AI-assisted.
Standard library only (`json`, `re`, `hashlib`, `pathlib`, `fractions`). Run
every script with `python3 -B`. Nothing here imports `forward/*/check.py`,
`reverse/*/check.py`, or any other producer/skeptic module.

Read before this work: `research/round32/experts/jung/assistant-4/` (its
`README.md`, `common4.py`, `sentence_and_gate_field_audit.py`,
`preregistration_audit_4.py` and `results.json`, per the calling task);
`research/round32/experts/jung/update-4.md` section 4 (the calling task's own
source: it lists six proposed assistant tests -- this package implements
items 1-4 (the round-wide control mirror, gate-field and forbidden-phrase
sweeps, and the AY1/AY2 shared-vocabulary check); items 5-6 (a fourth
independent recomputation of `2D`/`rho^(1)_R`/`K_2'` by the modern lens, and
confirming AZ2's `j_max`/cutoff pinning) are outside the Jung lens's scope
and are not attempted here); `advisor/panel-update-4.md` (item 7 is the
calling task in the advisor's own words); all ten Round32 contracts, gates
and skeptic reviews; `research/round32/HANDOFF.md` and `advisor/roadmap.json`
(both read for context; neither is audited by name -- they fell naturally
into the whole-round forbidden-phrase sweep's filesystem walk).

## Files

- `common5.py` -- copy of `assistant-4/common4.py` (per the calling task),
  with its header updated and these additions: `ALL_TEN_IDS` and per-id path
  constants (contract/gate/forward/reverse/skeptic) for every one of AV1
  through AZ2, not just AY1/AY2/AZ1/AZ2; `AZ1_GATE_FIELD_NAMES`/
  `AZ2_GATE_FIELD_NAMES` (the topic-specific gate-field unions
  panel-update-4.md decisions 2-3 add, distinct from the six-name
  state-identification union `GATE_FIELD_BOOL_NAMES` inherited from
  common4.py); `round_wide_md_and_json_paths()` (a filesystem walk of every
  `research/round32/**/*.md` and `**/*.json` file, not a hardcoded list),
  `addendum_tex_paths()`, `extra_readme_paths()`; `sentence_has_not` and
  `walk_all_strings` (moved here, unchanged, from assistant-4's own script
  bodies, since two sub-round-5 scripts now need them); the nine
  `FORBIDDEN_PHRASE_PATTERNS_R5` phrase patterns. Does **not** import
  `forward/*/check.py`, `reverse/*/check.py`, or any earlier assistant's
  scripts.
- `final_preregistration_audit.py` -- calling task item 1: nine checks over
  all ten contracts (frozen status, controls mirror, `gate_fields_required`
  presence+export+value, `mandatory_sentence_template` presence+verbatim
  match for AZ1/AZ2, `selected_after` placeholders, `state_provenance`
  shapes, the `"uniqueness of the AQ state"`/`"uniqueness of any
  subsequential limit"` split, sub-labels used vs. allowed, the
  certification-loop target note).
- `forbidden_phrase_sweep.py` -- calling task item 2: a whole-round,
  content-deduplicated sweep of every `research/round32/**/*.md` and
  `**/*.json` file, every `papers/round32-addendum/*.tex` file and both
  README.md files, for the nine named phrase patterns, each occurrence
  classified quoted/excluded, negated, or affirmative (a defect).
- `shared_vocabulary_fields.py` -- calling task item 3: the AY1/AY2
  `states_compared`/`region`/`topology`/`closeness_order` mirror check across
  forward/reverse/skeptic/gate, implementing `panel-update-4.md` item 3's own
  rule ("either byte-identical, or the checker must record which producer's
  exact string the gate adopts and treat the rest as a named wording
  variant").
- `results.json` -- merged output of all three scripts. Produced by
  `rm -f results.json && python3 -B final_preregistration_audit.py &&
  python3 -B forbidden_phrase_sweep.py && python3 -B
  shared_vocabulary_fields.py`. Byte-identical (SHA-256
  `6ad4f9fa13d0d45cce5b0c133ad9c5980a9bd7a714b4ba1fabc87e55714804a4`) under
  normal and `-B -O` Python, checked directly for this run.

## How to run

```bash
cd research/round32/experts/jung/assistant-5
rm -f results.json
python3 -B final_preregistration_audit.py
python3 -B forbidden_phrase_sweep.py
python3 -B shared_vocabulary_fields.py
```

Each script prints PASS/FAIL per sub-check and a findings list, and exits
with status 1 when a sub-check finds a defect. **A FAIL here is expected and
is the point of this tool**, exactly as assistant-4's own README states for
sub-round 4: this audit's job is to surface real, itemised defects (nine of
them, below), not to gate admission. All ten investigations are already
`accepted_within_scope`; nothing here reopens that.

## Results and every defect found

### 1. `final_preregistration_audit.py` -- 9 checks over all ten contracts

**`frozen_status_check` -- PASS.** Every one of the ten contracts
(`av1.json`..`az2.json`) has `status: "frozen_before_production"` and a
non-empty `frozen_at` timestamp (AV1 `2026-09-23T21:23:47Z` through AZ2
`2026-09-24T04:29:40.693167Z`, AZ1 and AZ2 frozen 32 microseconds apart).

**`controls_mirror_check` -- FAIL on one contract (a known, already-recorded,
non-blocking defect, not a new finding).** `preregistration.
controls_required.ids == controls` exactly for nine of ten contracts. **AV2**
fails: `controls_required.ids` lists 23 ids, `controls` lists 24 --
`c1_window_preview_only` is present in `controls` but missing from
`controls_required.ids`. This is `advisor/av2-gate.json`'s own recorded
"Pre-registration mirror" clerical defect from sub-round 1 (both producers
executed the missing id as a damaging mutation regardless; `freeze_contract.py`
was updated after this freeze to enforce the equality going forward; the
frozen contract itself is not amended, per `AGENTS.md`'s immutability rule).
Re-confirmed here as the first item of the "AV2-mirror-gap check lineage"
`panel-update-4.md` item 5 names, extended for the first time to all ten
contracts rather than AV2 alone: no other contract has this gap.

**`gate_fields_required_check` -- PASS.** `preregistration.gate_fields_required`
is present for exactly the four contracts the two `advisor/plan.json`
vocabulary extensions require it for (AY1, AY2: the six-name state-
identification union, 5-of-6 present -- `rate_in_N_claimed` missing, an
already-recorded gap, see assistant-4's README; AZ1: the four continuum-
trajectory flags; AZ2: the three finite-graph flags), and every one of those
21 (field, contract) pairs is exported with its required value (`False`
throughout, except `AZ2.model_is_finite_graph = True`, as the AZ2 contract
itself requires) in that loop's own producer `output/results.json` (AY1:
both forward and reverse; AY2/AZ1/AZ2: forward only, matching each
contract's own `direction`), **and**, where the gate carries a `gate_fields`
sub-object (all four do), there too. No violation found.

**`mandatory_sentence_template_check` -- PASS (calling task scope: AZ1/AZ2
only).** Both AZ1's and AZ2's `preregistration.mandatory_sentence_template`
fields are present, and the template text is present verbatim modulo the
filled-in numeric constants in the one report.md each has (`forward/az1/
report.md`, `forward/az2/report.md` -- neither has a reverse producer). Bonus
coverage (not required by the calling task, checked anyway): the AZ2 gate's
`accepted`+`decision` text also carries the template verbatim; the **AZ1
gate's does not** -- it restates the same content interwoven with an added
parenthetical ("-- a hypothesis of asymptotic-freedom form..., not derived
--" and a re-description of "the fixed-spacing family") rather than as one
contiguous quoted sentence, so the segment-order verbatim-modulo-constants
match fails on the gate text specifically (report.md is unaffected). This is
recorded as a bonus finding, not a required-scope failure, since the calling
task names report.md, not the gate, for this check. Cross-referenced, not
re-audited: assistant-4's own AY1/AY2 finding (AY1's field is a paraphrase,
not the Jung verbatim form; AY2 has no such field at all) stays as assistant-4
recorded it; both are grandfathered in `advisor/plan.json`'s second
`preregistration_vocabulary_extensions` entry, contracts unamended.

**`selected_after_check` -- PASS (both are the expected, already-understood
shapes, not new problems).** AY2's `selected_after` is still the literal
placeholder `"<preceding gate>"`, frozen and immutable, matching assistant-4's
finding and the AY2 gate's own defect D1. AZ2's `selected_after` names
`research/round32/advisor/az1-gate.json`, which genuinely did not exist on
disk yet at AZ2's own freeze timestamp (AZ2 froze
`2026-09-24T04:29:40.693167Z`; the AZ1 gate did not complete until
`2026-09-24T05:18:19.053664Z`, about 49 minutes later) -- a real,
forward-looking path, exactly the drafts' ordinary look-ahead convention
assistant-4 already documented, not a template placeholder.

**`state_provenance_check` -- FAIL on one contract (a genuine, newly-found
defect).** Nine of ten contracts' `preregistration.state_provenance` either
match the original three-prefix closed vocabulary (`AV1`, `AV2`, `AW1`,
`AW2`, `AX1`, `AX2`, `AY1`, `AZ1`) or match the second `plan.json` extension's
"names more than one family at once" shape (`AY2`, the already-known case).
**AZ2 is a new, distinct problem, found here for the first time**: its
`state_provenance` is `"AQ1_centered_whole_star_subsequence via
finite_volume uniform bound"` -- the same unedited boilerplate every
AQ1-subsequence contract in the round carries -- even though AZ2's own
`model_id` is `"FG(two-plaquette, D in {6,8}, tau_FG grid, I1.5,
gauge-invariant)"`, a **finite-graph** model (the Round11 two-plaquette
graph: 6 vertices, 7 links, 6 Gauss constraints, no subsequential limit of
anything). Every sibling field in the *same* contract *was* correctly
adapted for the finite-graph model (`selected_triple_alpha_units = "n/a
(finite graph)"`, `observable.reference_route = "own_finite_graph"`) --
`state_provenance` alone was left as an apparently-unedited copy. The closed
vocabulary already contains a `finite_graph_ground` prefix for exactly this
case (`common5.ALLOWED_STATE_PROVENANCE_PREFIXES`); AZ2 does not use it. This
passes the narrow structural prefix check trivially (the string literally
starts with an allowed prefix), which is why neither assistant-3's nor
assistant-4's audits (scoped to AX1/AX2/AY1/AY2 and AY1/AY2/AZ1/AZ2/draft
placeholders respectively) surfaced it: it only appears once every one of the
ten contracts is checked at once, which is this script's own extension.
Since AZ2 is already frozen and gated (`accepted_within_scope`), this is a
repair-by-record item for the advisor (`AGENTS.md`'s rule), not something to
edit into the frozen contract.

**`aq_state_phrase_check` -- PASS.** Every one of the eight frozen-before-2026-
09-24 contracts (AV1 through AY2) still carries the literal `"uniqueness of
the AQ state"` in its `claim_exclusions` (grandfathered, unamended, per
`plan.json`'s second extension) and neither carries the new phrase. Both AZ1
and AZ2 carry `"uniqueness of any subsequential limit"` and neither carries
the old phrase. Exactly the recorded, intended shape.

**`sub_labels_used_vs_allowed_check` -- PASS.** `sub_labels_allowed` equals
the closed 5-label vocabulary in all ten contracts, and every sub-label or
secondary sub-label any producer, skeptic review or gate actually exports for
that loop (from a fresh key-walk of every `output/results.json` and every
gate) is a member of it. AZ1 exports no sub-label at all (its gate's own
`sub_label` field is also unset) -- recorded as a fact, not a gap: AZ1 is a
continuum-trajectory statement, not a state-comparison loop, and nothing in
the round requires a sub-label from it.

**`certification_target_note_check` -- PASS.** Both AZ1's and AZ2's
`preregistration.target.note` state, in as many words, that the target is a
"feasibility/format check" and "not a blind discovery threshold" -- the
second `plan.json` extension's `target_of_a_certification_loop` rule. AY2's
own note lacks this literal phrasing, exactly as expected: `plan.json` names
AY2 itself, by id, as the recorded accepted exception to this rule (contract
unamended).

### 2. `forbidden_phrase_sweep.py` -- whole-round sweep

Scanned 153 distinct-content markdown/tex files (500 total paths before
content-hash deduplication -- the same handful of shared premise files, e.g.
`research/round21/forward/i1/report.md`, are snapshotted byte-identically
into ten-plus producers' `inputs/` trees by `AGENTS.md`'s own design) and 150
distinct-content JSON files (230 total paths), under `research/round32/**`,
`papers/round32-addendum/*.tex` and both README.md files. This script's own
directory is excluded from the swept set (scanning a results.json this same
run is still writing would be circular).

**Six occurrences classified `AFFIRMATIVE_needs_review` -- every one listed,
none is a false alarm from an earlier, cruder version of this classifier**
(see "Classifier design notes" below for what was tuned out and why):

1. `papers/round32-addendum/state-lemma.tex:356` -- section heading
   `\subsection{From the cutoff box to the AQ state}`.
2. `papers/round32-addendum/state-lemma.tex:387` -- paragraph heading
   `\paragraph{Passage to the AQ state.}`.
3. `research/round32/experts/historical/memo.md:128` -- `"(H4) passage to
   the AQ state;"`, a bare list item naming a proof hypothesis.
4. `research/round32/experts/historical/recommendation.json`
   `goal_pairs[0].model` -- `"...; passage to the AQ state by local
   trace-norm convergence."`

Items 1-4 are the same defect in four places: the literal, unquoted,
un-negated definite-article phrase `"the AQ state"` (loop2-response.md
section 4's own forbidden phrasing -- forbidden precisely because "the"
presupposes a single, unique state, the vocabulary's own required
replacement is `"a chosen subsequential [limit/state]"`). None asserts a
false claim -- each is a naming convention for the constructed object in
mathematical prose (a section title, a proof-hypothesis label, a one-line
provenance description) -- but each is the literal phrase the panel's own
sweep instruction exists to catch, in files this round-wide extension is the
first assistant package to actually scan (assistant-4 scoped its own scan to
AY1/AY2 files; these four are the addendum manuscript and two other lenses'
own memos).

5. `research/round32/advisor/findings.json` `loops[1].applications[0]` --
   `"Supplies the first certified actual-state Euclidean node at the
   original coupling cap."` (AV2's own entry).
6. `research/round32/advisor/findings.json` `loops[5].applications[0]` --
   `"First certified actual-state Euclidean node for uniform Kogut-Susskind
   SU(2) at fixed spacing..."` (AX1's own entry).

**`"first certified"` -- always flagged per the calling task, whatever its
classification** (2 occurrences, both above, both in `findings.json`).
**Git-history check** (`git log -p -S"first certified" -- research/round32`):
the phrase was **added exactly once** (commit `fd6770a`, gating AV2) and
**never removed** anywhere in Round32's history -- so this script's finding
does **not** literally corroborate "the advisor removed one overclaim" by
that phrase's own text. A nearby, related edit *was* found in the same file's
history: an earlier sentence, `"The certified positive lower bound on
||rho_R-P_R||_1 is the first static lower bound in the programme..."`, was
rewritten (not merely reworded) to `"The certified two-sided trace-norm
distance of every limit from the Haar product on R is the first such
two-sided tier in the programme..."` when AY2 was gated -- still uses "first",
just scoped more precisely ("in the programme", i.e. within this project's
own sequence, not a claim of external scientific priority, which every gate
separately and explicitly records as unverified). Recorded factually, for
the advisor to read against its own memory of what was meant: this script
does not resolve the ambiguity in the calling task's own parenthetical.

**No other affirmative defect.** 98 bare `unique`/`uniqueness` occurrences
and 1 `predicts` occurrence, that an earlier, cruder pass of this classifier
did flag, are legitimately off-topic (a different, already-admitted fact;
literature about a cited external paper; or an unrelated ordinary use of the
word) -- see "Classifier design notes". Zero occurrences of `"the continuum
limit exists"`, `"fraction of the problem"`, `"confirms the Z^3 value"`, or
`"solves"`/`"solved"` in the same sentence as `"mass gap"` were classified
affirmative anywhere in the round.

**Classifier design notes (what was tuned, and why, to avoid both false
alarms and silently hiding a real one).** A first pass of this sweep, using
only assistant-4's own code-span/negation-cue classifier extended naively
to the whole round, found **458** affirmative `bare_unique` hits and **122**
affirmative hits overall. Manually reading a sample showed nearly all were
legitimate uses this project itself makes throughout -- "a unique ground
state", "a unique fixed point", "unique i,r with x=4i+r" (Euclidean
division), an external paper's own "unique infinite-volume limit"
(`experts/modern/sota-table.md`, `sources.json`), a roadmap goal's own title
naming a *not-yet-proved* future target (`advisor/roadmap.json`,
`network.json`, both `status: "planned_not_executed"`), or a LaTeX quoted
`` ``...'' `` span wrapping a physical line break the original line-scoped
quote detector missed. Each was traced to a concrete cause and a targeted,
documented fix (topic-relevance windows scoped to the enclosing `\item` or
paragraph, not a blanket radius; an immediate-modifier check for "unique
ground/fixed point/..."; paragraph-scoped LaTeX/double-quote detection;
fenced-code-block detection; a table-header exclusion check for
`papers/round32-addendum/limits.tex`'s own "Excluded by the contract"
column; file-based literature/roadmap short-circuits) -- documented in full,
with the reasoning for each, in `forbidden_phrase_sweep.py`'s own docstrings
and comments, not just asserted here. The final classifier was then spot-
checked again on a random sample of the remaining "off-topic" bucket (86
`bare_unique` + 12 `third_party_literature_description`, `predicts` × 1) to
confirm none of the excluded readings was actually concerning. **No
occurrence was hidden by being reclassified out of the sweep's raw output**:
`results.json`'s `forbidden_phrase_sweep.all_occurrences` still lists every
single hit, with its classification and the reasoning category, so the
advisor can re-run the same scan and audit the classifier's own calls, not
just its conclusion.

**One non-defect design note.** Assistant-4's markdown code-span detector
assumed "none of the scanned files put these phrases inside fenced code
blocks" (true for its own AY1/AY2 scope). That assumption does not hold
round-wide: `experts/jung/update-4.md` embeds the entire second
`preregistration_vocabulary_extensions` JSON entry, including the literal
string `'uniqueness of the AQ state'`, inside a fenced ` ```json ` block.
This script adds fenced-block detection (`in_fenced_code_block`) so that
occurrence is correctly excluded rather than flagged.

### 3. `shared_vocabulary_fields.py` -- AY1/AY2 mirror check

Implements `panel-update-4.md` item 3's own rule verbatim: for each of
`states_compared`/`region`/`topology`/`closeness_order`, either every source
is byte-identical, or the gate's own value is the adopted canonical string
and every other source is recorded as a same-type named wording variant (not
a defect) -- **except** a source whose JSON *type* differs from the gate's,
which the rule does not cover and this script reports as an actual rule
violation.

**AY1 (sources: `forward/ay1/output/results.json`, `reverse/ay1/output/
results.json`, `skeptic/ay1.json`, `advisor/ay1-gate.json`) -- 2 genuine
DEFECTs, 2 named wording variants, re-confirming and formally classifying
assistant-4's own finding against the update-4 rule for the first time:**

- `states_compared`, `region`: forward and skeptic agree with the gate
  exactly; **reverse** carries a shorter same-type string in both cases (a
  named wording variant -- satisfies the rule's "OR" clause, not a defect).
- **`topology` -- DEFECT.** skeptic agrees with the gate exactly (`"trace
  norm on B(H_R); dynamics named in the norm on compact time windows (no
  dynamical statement)"`); reverse carries the shorter `"trace norm on
  B(H_R)"` (a named wording variant); **forward exports a `dict`**
  (`{"dynamics": "norm on compact time windows", "states": "trace norm on
  B(H_R)"}`) where every other source exports a `str`. A JSON type mismatch
  is not resolvable as "a named wording variant of the same string" -- the
  rule is not satisfied for this field.
- **`closeness_order` -- DEFECT.** reverse and skeptic agree with the gate
  exactly (`[1, 2]`); **forward exports the bare scalar `2`** where every
  other source exports a two-element list. Another type mismatch, same
  conclusion.

**AY2 (sources: `forward/ay2/output/results.json`, the skeptic's
pre-comparison `skeptic/ay2-independent/results.json`, the now-existing
final skeptic postreview `skeptic/ay2.json`, `advisor/ay2-gate.json`) -- 0
type mismatches (rule satisfied), but a nuance beyond what assistant-4 could
see (its own AY2 audit ran before the postreview existed):**

- `states_compared`, `region`: forward and the **final** skeptic postreview
  agree with the gate exactly (the longer form, with `"48 links, 36
  endpoints"`); the pre-comparison skeptic package alone carries the shorter
  paraphrase assistant-4 already found -- still a named wording variant.
- `topology`: **the final skeptic postreview now agrees with the gate**
  (the long form, with the dynamics clause) -- unlike at assistant-4's own
  audit time, when only the gate carried it. Both forward's own producer
  text and the pre-comparison skeptic package still carry the shorter
  `"trace norm on B(H_R)"` (both same-type wording variants of the gate's
  adopted string, not a defect): a clean 2-2 split by *when* the text was
  written (forward + pre-comparison, both written before the AY2 gate, vs.
  final postreview + gate, both written at or after it), not a 3-way
  disagreement as assistant-4 recorded when the postreview did not yet
  exist.
- `closeness_order`: all four sources agree byte-for-byte.

Two files were checked directly and confirmed to export none of the four
fields at all (`skeptic/ay1-independent/results.json`,
`skeptic/ay1-postreview/results.json`, `skeptic/ay2-postreview/results.json`
-- these are per-check exact-arithmetic output files, not the consolidated
skeptic record; `results.json`'s `checked_but_empty_sources` records the
key-occurrence counts found by a full recursive key-walk, not an assumption).

## Summary of every defect found (for the advisor)

1. **AV2's `controls_required.ids` omits `c1_window_preview_only`** (23 vs.
   24 in `controls`) -- already recorded in `advisor/av2-gate.json` as a
   non-blocking clerical defect from sub-round 1; `freeze_contract.py` now
   enforces this equality; re-confirmed here as still present in the frozen
   contract (expected: immutability).
2. **AZ2's `preregistration.state_provenance` is the unedited AQ1-
   subsequence boilerplate, despite AZ2 being the round's only finite-graph
   contract** (`model_id` starts with `FG(`) -- a genuine, newly-found
   wording/schema inconsistency; every sibling field in the same contract
   *was* correctly adapted; the closed vocabulary already has a
   `finite_graph_ground` prefix for this case that AZ2 does not use.
3. **The literal phrase `"the AQ state"` (unquoted, un-negated) appears in
   four places**: `papers/round32-addendum/state-lemma.tex` (two section/
   paragraph headings), `experts/historical/memo.md` (one hypothesis-list
   item), `experts/historical/recommendation.json` (one model-description
   field). None asserts a false claim; all are naming-convention usages the
   panel's own forbidden-phrasing rule (loop2-response.md section 4) still
   catches.
4. **`"first certified"` appears twice, in `advisor/findings.json`**
   (AV2's and AX1's own `applications` entries) -- always flagged per the
   calling task; git history shows the phrase was added once and never
   literally removed, so this script cannot confirm which prior overclaim
   the calling task's parenthetical refers to; a nearby, related sentence in
   the same file *was* reworded (not to remove "first", but to scope it more
   precisely) when AY2 was gated.
5. **AY1's `topology` and `closeness_order` fields are not just wording
   variants but JSON *type* mismatches**: the forward producer exports
   `topology` as a `dict` (every other source: `str`) and `closeness_order`
   as the bare scalar `2` (every other source: the list `[1, 2]`) --
   already known from assistant-4's own work, now explicitly checked against
   `panel-update-4.md` item 3's own byte-identical-or-named-variant rule and
   confirmed to be the one case in the round that rule, as stated, does not
   cover.
6. **AY1's `states_compared`/`region` and AY2's `states_compared`/`region`/
   `topology` carry same-type wording variants** across forward/reverse/
   skeptic/gate -- not a rule violation (the rule's "OR" clause is satisfied:
   the gate's adopted string is named and every variant is recorded), but a
   real, itemised difference worth the advisor's attention if a future round
   wants byte-identical mirrors for these fields the way `controls ==
   controls_required.ids` already is.

Non-defect notes, recorded for completeness, not action: the AZ1 gate's
`accepted`+`decision` text restates the mandatory sentence template with an
inserted parenthetical rather than as one verbatim span (bonus coverage,
report.md is unaffected, not the calling task's required scope); AZ1
exports no sub-label at all (expected -- it is not a state-comparison loop);
AY2's target note correctly lacks the "feasibility/format check" phrase
(plan.json names AY2 itself as the recorded exception); `research/round32/
HANDOFF.md` appeared on disk partway through this work (a live,
concurrently-advancing repository, the same situation assistant-4 documented
for `ay2-gate.json`) and was picked up automatically by this script's
filesystem-walk design, with no code change needed.

**This is a live, concurrently-advancing repository.** `git status` at the
end of this work confirms every file this session touched is under
`research/round32/experts/jung/assistant-5/`.
