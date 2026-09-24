# Jung/Pauli lens, Round32 sub-round 4, assistant-4

The sentence-template and gate-field checks (`advisor/panel-update-3.md` item 6,
Jung share: "the sentence-template and gate-field checks"; the calling task).
**These outputs count zero research loops.** Nothing here is a producer, a
contract, a gate or a skeptical review; nothing computed here is read back into
any contract, gate or skeptical review. Human project author: Hruday N M
(BUNZEEY); AI-assisted. Standard library only (`json`, `re`, `pathlib`).
Run every script with `python3 -B`. Nothing here imports `forward/*/check.py`,
`reverse/*/check.py`, or any other producer/skeptic module.

Read before this work: `research/round32/experts/jung/assistant-3/` (read its
`README.md`, `common3.py`, `preregistration_audit_3.py`,
`forbidden_wording_grep.py` and `results.json`, per the calling task; `common4.py`
started as a literal copy of `common3.py`, then extended -- see its module
docstring for exactly what changed), `research/round32/experts/jung/
loop2-response.md` section 4 (the mandatory sentence template and the
observation-map rule for AY -- the source of everything script 1 checks),
`research/round32/advisor/panel-update-3.md` (item 6 is the calling task; item 2
records that AY1's own contract added three gate-field names beyond
loop2-response.md's three), `research/round32/advisor/plan.json`'s
`preregistration_vocabulary_extensions`, the AY1 contract/gate/reports/skeptic
review, the AY2 contract/report/skeptic pre-comparison, and the AZ1/AZ2 draft
contracts.

## Files

- `common4.py` -- copy of `assistant-3/common3.py` (per the calling task), with
  its header updated and these additions: path constants for every AY1/AY2
  forward/reverse/gate/skeptic artifact the calling task names (AZ1/AZ2 contract
  paths too); `GATE_FIELD_BOOL_NAMES` (the six-name union) and
  `GATE_FIELD_VALUE_NAMES` (`states_compared`/`region`/`topology`/
  `closeness_order`); a generic recursive JSON key-walker (`walk_json_items`,
  `walk_json_strings`, `find_key_occurrences`) that distinguishes a real
  `{"key": value}` export from the key's name occurring only as a string value
  elsewhere; a markdown code-span detector and forbidden/required-phrase
  classifier (`in_code_span`, `classify_phrase_occurrence`,
  `PHRASE_NEGATION_CUES`) adapted from assistant-3's `forbidden_wording_grep.py`
  `classify()` for a different phrase set; `normalize_sentence` (strips
  backticks, collapses whitespace) for the verbatim-modulo-constants sentence
  match. Does **not** import `forward/*/check.py`, `reverse/*/check.py`, or any
  earlier assistant's scripts.
- `sentence_and_gate_field_audit.py` -- script 1/2 (calling task item 1).
- `preregistration_audit_4.py` -- script 2/2 (calling task item 2).
- `results.json` -- merged output of both scripts. Produced by
  `rm -f results.json && python3 -B sentence_and_gate_field_audit.py &&
  python3 -B preregistration_audit_4.py`. Byte-identical under normal and `-O`
  Python (checked for both scripts' stdout and the merged `results.json`).

## How to run

```bash
cd research/round32/experts/jung/assistant-4
rm -f results.json
python3 -B sentence_and_gate_field_audit.py
python3 -B preregistration_audit_4.py
```

Both scripts print PASS/FAIL per sub-check and a findings list, and both exit
with status 1 when a sub-check finds a defect. **A FAIL here is expected and is
the point of this tool**: sub-round 4 has real, documented wording and schema
defects (the same kind as sub-round 3's contract-wording findings W1-W7), and
this audit's job is to surface them, not to gate admission. Nothing here decides
whether AY1/AY2/AZ1/AZ2 are accepted; only the advisor's gates and the skeptic's
reviews do that.

## Results and every defect found

### 1. `sentence_and_gate_field_audit.py`

**`mandatory_sentence_template_check` -- FAIL (one real gap).** The
loop2-response.md section 4 sentence, extracted programmatically (not
hardcoded) and matched verbatim-modulo-constants (its fixed opening clause
through `for every A in B(H_R) ... |omega'(A) - omega''(A)| <=`, and its fixed
closing clause from `This is uniform local closeness ...` to the end, both
found regardless of backtick markup), **is present in all three required
report.md files** (`forward/ay1/report.md` section 6, `reverse/ay1/report.md`
section 4, `forward/ay2/report.md` section 1.4). **It is absent from the AY1
gate's `accepted` text.** The gate's `accepted` field instead contains only the
*contract's own paraphrase* ("the reduced densities satisfy
`||rho_R - rho'_R||_1 <= 2D` and agree to first order in tau..."), which is
itself not a verbatim copy of the Jung-form sentence -- it restates the same
content using reduced-density notation instead of the universally-quantified
`for every A in B(H_R) with ||A||<=1: |omega'(A)-omega''(A)|<=...` form. Both
report.md files carry *both* sentences side by side (each report labels them
"mandatory sentences", plural); only the gate carries the paraphrase alone.
This is exactly the "content half" assistant-3's planning note 1 flagged as
still open (assistant-3 could confirm only that the gate-field *names* existed,
not that the sentence *text* was pinned and reproduced verbatim); it is now
confirmed present verbatim in every report, and confirmed **absent** from the
gate.

**The AY2 gate appeared on disk while this audit was in progress** (`advisor/
ay2-gate.json` did not exist when the calling task named the file -- "gate may
not exist yet, handle absence" -- but does exist as of this run; see "Non-defect
notes" below). It is checked the same way as the AY1 gate: its `accepted`+
`decision` text also does **not** contain the loop2-response.md verbatim
(modulo constants) sentence. Independently, and without this audit having fed
anything back into it, the AY2 gate's own `decision` field states outright
"the AY2 preregistration has no template field" and separately lists
"contract defects D1-D6", naming the same defects this audit's two scripts
found independently: `selected_after` left as the placeholder `"<preceding
gate>"` at freeze time, `"uniqueness of the AQ state"` in the exclusions, and
`rate_in_N_claimed` missing from `gate_fields_required`. This is strong,
independent corroboration of items 2, 6 and 7 in the defect summary below.

**`gate_field_export_check` -- PASS (no field ever exported true), with three
contract-level findings.** For the six-name union (`uniqueness_claimed`,
`whole_sequence_claimed`, `rate_claimed`, `rate_in_N_claimed`,
`translation_invariance_claimed`, `boundary_independence_of_dynamics_claimed`):
every real JSON-key export and every markdown `name: false` line found is
`false`; none is ever `true`. Three are named verbatim in loop2-response.md
section 4 (`uniqueness_claimed`, `whole_sequence_claimed`, `rate_in_N_claimed`);
the other three first appear in AY1's own contract item 4 and are recorded as a
panel decision in `advisor/panel-update-3.md` item 2. As the calling task
anticipated: **the AY1 reverse does not export `rate_in_N_claimed`** as a real
key, in neither `reverse/ay1/report.md` nor `reverse/ay1/output/results.json`
(confirmed by both a markdown regex scan and a JSON key-walk); the AY1 gate
itself supplies `rate_in_N_claimed: false` at its own `gate_fields` level
(`closeness_order: [1, 2]` adopted instead), so the field is not simply missing
from the admitted record, only from the reverse producer's own export. Two
further findings, both already self-noted by the producers and independently
reconfirmed here by reading the contracts directly: **AY1's**
`preregistration.gate_fields_required` lists only 5 of the 6 names (uses
`rate_claimed`, omits `rate_in_N_claimed` -- the origin of the name split, wording
defect W3 in `forward/ay1/report.md`); **AY2's** `gate_fields_required` has the
same 5-of-6 gap even though AY2's own "required" item 6 text lists both
`rate_claimed` *and* `rate_in_N_claimed` (AY2's own defect D3, in
`forward/ay2/report.md`'s defects table).

**`gate_value_agreement_check` -- documented drift, not byte-identical (see
below).** `states_compared`/`region`/`topology`/`closeness_order`, compared at
the root of each results.json (or the `gate_fields` sub-object where a file
nests them there):

  - **AY1** -- forward, `skeptic/ay1.json`'s `gate_fields`, and the gate's own
    `gate_fields` all agree exactly on all four fields. **The reverse disagrees
    with all three on three of the four:** `states_compared` (reverse drops the
    "(every pair, same or different family, same tau)" clause), `region`
    (reverse: `"R fixed before production"` -- omits the actual definition
    `R={0,e_z}` that every other source states), and, most substantively,
    **`topology`**: the forward's own root-level `topology` field is a **dict**
    (`{"dynamics": ..., "states": ...}`), the reverse's is a **bare string**
    (`"trace norm on B(H_R)"`, dropping the dynamics clause), and the gate's and
    skeptic's is a **different string** that includes the dynamics clause -- no
    two of the three representations agree, and forward's is not even the same
    JSON type as the other two. **`closeness_order`**: forward exports a scalar
    `2`; reverse, skeptic and the gate all export the list `[1, 2]` -- forward is
    the outlier here as well.
  - **AY2** -- three sources compared once the gate appeared (forward, the
    skeptic's pre-comparison `skeptic/ay2-independent/results.json`, and the
    now-existing `advisor/ay2-gate.json`). `closeness_order` agrees across all
    three. `states_compared` and `region`: the gate matches the **forward's**
    longer form exactly; the skeptic's pre-comparison alone carries a shorter
    paraphrase (e.g. region: skeptic `"R={0,e_z} fixed before production"` vs.
    forward's and the gate's longer `"... (complete cover of the original xz
    Wilson loop; 48 links, 36 endpoints)"`) -- not byte-identical across all
    three, though not contradictory in content, unlike AY1's `topology`/
    `closeness_order` type/value mismatches. `topology`: forward and the
    skeptic's pre-comparison agree on the short form `"trace norm on B(H_R)"`;
    the gate alone adds the dynamics clause (`"...; dynamics named in the norm
    on compact time windows (no dynamical statement)"`), so it is again a
    3-way disagreement, this time with the gate as the odd one out rather than
    the earlier-written pre-comparison.

None of this is scored as a forbidden-phrase or gate-field-boolean violation
(this check is reported as its own, separate finding), but it is a real,
itemised answer to the calling task's "check ... values agree ... across
forward/reverse/skeptic/gate": for AY1 they do **not**, on all four fields, with
the reverse (and, for `closeness_order`, the forward) each the odd one out on
different fields; for AY2, two of four agree and two do not.

**`forbidden_and_required_phrase_scan` -- PASS**, with the exact contract
locations recorded. Scanned `forward/ay1/report.md`, `reverse/ay1/report.md`,
`forward/ay2/report.md` (required), `skeptic/ay1.md` (bonus), `advisor/
ay1-gate.json`, `skeptic/ay1.json`, `skeptic/ay2-independent/results.json`,
`contracts/ay1.json`, `contracts/ay2.json` (required), and `contracts/az1.json`,
`contracts/az2.json` (bonus, beyond the calling task's AY1/AY2 scope, included
for completeness since the same pattern recurs there) for `"the AQ state"`
(catches `"uniqueness of the AQ state"` as a substring too), `"the thermodynamic
limit"`, and bare `unique`/`uniqueness` without `not` in the same sentence.
**Zero occurrences classified `AFFIRMATIVE_needs_review`** in any required
file. Classification detail:

  - Markdown occurrences inside a backtick code span with a nearby negation cue
    are whitelisted, per the calling task's rule. One occurrence is **negated but
    not inside a code span**: `reverse/ay1/report.md`'s
    `"- not claimed: uniqueness of the AQ state;"` is plain prose, unlike the
    forward's equivalent (which is inside a code span). It reads unambiguously
    as a negation, but falls outside the letter of the "whitelist ... in code
    spans" rule -- recorded as a wording-hygiene note, not a violation.
  - **WORDING DEFECT, exactly as the calling task asked to be reported:** the
    literal phrase `"uniqueness of the AQ state"` is still present inside a
    `claim_exclusions`/`preregistration.claim_exclusions` JSON array (which has
    no code-span mechanism, so the whitelist does not apply there) in:
    `ay1_contract:claim_exclusions[0]`, `ay1_contract:preregistration.
    claim_exclusions[1]`, `ay2_contract:claim_exclusions[0]`, `ay2_contract:
    preregistration.claim_exclusions[1]`, and, beyond the calling task's stated
    scope but found in the same pass, `az1_contract:preregistration.
    claim_exclusions[1]` and `az2_contract:preregistration.claim_exclusions[1]`.
    Every one of these arrays is a verbatim, unmodified copy of
    loop2-response.md **section 2**'s own pre-registration-block template,
    whose own `claim_exclusions` list contains this exact phrase as one of its
    seven entries -- the phrase's origin is the section-2 template itself
    (which predates section 4's naming rule), not a per-contract slip. Every
    read of it here is inside an excluded-claim list (naming the claim in order
    to rule it out), never an assertion.
  - Nine bare `"uniqueness"` occurrences in `skeptic/ay2-independent/
    results.json`'s `obligations[N]` array (e.g. `obligations[1].missing_premise
    = "uniqueness of subsequential limits within the family (...)"`) name the
    *missing property* an explicit unproved-obligations table records as **not**
    proved; the table's own structure is the negation. Read strictly
    sentence-by-sentence, the literal rule would flag these (no `not` token in
    the same short JSON string), so this classification is reported as a
    distinct, deliberate exception rather than silently merged into
    "negation_or_exclusion".
  - Three occurrences are control/mutation-table entries naming what a damaging
    mutation would set, or a control literally named
    `local_closeness_not_uniqueness` -- not assertions.
  - The required phrase `"a chosen subsequential"` is present in all three
    required report.md files.

### 2. `preregistration_audit_4.py`

**AY1 -- passes every check** (structural regression, `controls_required.ids ==
controls` for all 21 ids, sub-label used (`uniform_local_closeness_not_uniqueness`)
covered by the closed vocabulary, `gate_fields_required` present (5/6, missing
`rate_in_N_claimed` -- recorded, folded into AY1's own `passed` since item 4
requires it), `selected_after` filled with a real path, `error_terms_itemized`
non-empty with no unreasoned `not_applicable` entries, `target` well-posed).

**AY2 -- FAILS on two independent points**, both real defects:

1. **A new schema gap plan.json's four-field extension does not cover.**
   `preregistration.state_provenance` = `"subsequential limits of both AY1
   families (AQ1 centered whole-star boxes; I1 all-contained-face boxes with
   padding) via finite-volume uniform bounds"` does not start with any of the
   three closed-vocabulary prefixes (`AQ1_centered_whole_star_subsequence`,
   `finite_volume_N=<N>`, `finite_graph_ground`). It is a new shape: a
   *combined* description of subsequential limits from **both** AY1 families at
   once, because AY2 is a state-identification statement loop comparing F1 and
   F2 together -- every earlier loop's `state_provenance` names one family.
   AY1's own `state_provenance` passes trivially (it literally starts with the
   allowed prefix), so this is specific to AY2's combined-family phrasing, not a
   shared regression. Recommend the advisor add a vocabulary note for this shape
   the same way `plan.json` recorded the four earlier gaps, if a future
   contract needs to name more than one family's provenance at once.
2. `selected_after` is **still the literal placeholder text `"<preceding
   gate>"`**, exactly as the calling task named it -- and AY2 is already
   `status: frozen_before_production`, so this placeholder is now frozen into
   the contract. Recorded here as the defect to be noted in the (not yet
   existing) AY2 gate.

**AZ1, AZ2 (drafts) -- pass every check that applies to a draft** (structural
regression against the extended vocabulary; `controls_required.ids ==
controls`, 18/18 and 19/19; `selected_after` filled with a real, if
not-yet-existing, forward-looking gate path in both cases -- expected for a
draft awaiting its predecessor's gate, not a placeholder defect;
`error_terms_itemized` non-empty, AZ1's sole `not_applicable` entry states its
reason inline; `target` syntactically well-posed for both, though both use a
boolean-style proxy value (`>= 1`) rather than a numeric closeness threshold --
recorded as an observation, matching the style of earlier statement loops, not
a well-posedness failure).

**`sub_labels_allowed` vs. the tier name `first_order_distance_from_product`.**
AY2 actually exports `sub_labels = ["uniform_local_closeness_not_uniqueness",
"static_not_dynamic"]`, both members of the closed 5-label vocabulary --
**no gap**. `first_order_distance_from_product` is used consistently as the
value of a `tier` field (inside `label` blocks), **never** as a member of the
`sub_label`/`sub_labels` export. **No vocabulary-note defect follows**: the tier
name and the sub-label vocabulary are never conflated anywhere found. Flagged
as an open observation only: there is currently no closed vocabulary governing
*tier* names at all (unlike `sub_labels_allowed`), so nothing currently stops a
future producer from choosing an arbitrary tier name; a `tier_names_allowed`
list, added the same way plan.json added the four field extensions, is a
plausible future step but is not required by anything found in this round.

**`gate_fields_required` present -- AY1/AY2 yes (with the gap above), AZ1/AZ2
no.** Neither AZ1 nor AZ2's `preregistration` block has a `gate_fields_required`
key at all. Recorded factually; **not** folded into AZ1/AZ2's `passed` (unlike
AY1/AY2, where item 4/item 6 explicitly require it), because whether AZ1/AZ2
need this field is an open interpretive question: neither is a
state-identification loop (no subsequential-limit uniqueness / whole-sequence /
rate / translation-invariance claim is at stake in a continuum-trajectory
statement or a finite-graph computation), so its absence may be intentional
rather than a gap -- unless the advisor intends `gate_fields_required` to be
universal across every round32 contract.

**Draft placeholder listing (calling task item 2, final bullet).**

  - **AZ1: none found.** Every field is filled with a concrete value (the earlier
    apparent `<...>` hits from a first-pass regex, e.g. inside `<=10^-8 i.e.
    g^4>=...`, were math notation -- `<=`, `<W>` -- not template placeholders;
    the final placeholder detector requires a multi-word or `|`-separated span
    inside the angle brackets, or the literal text `e.g.`, and finds nothing in
    AZ1).
  - **AZ2: one placeholder remains.** `parameters.j_max =
    "<declared, e.g. 3/2 and 2 with certified tail>"` is still template text (the
    contract's own model description elsewhere already promises "representation
    cutoff j_max with certified tail" but the concrete cutoff values are not yet
    pinned). This must be filled with actual exact values before AZ2 freezes,
    the same way AX1's `J0_resolution` needed pinning before its producers wrote
    `check.py` (assistant-3's planning note 1, same discipline).

## Summary of every defect found (for the advisor)

1. The AY1 gate's `accepted` text does not contain the loop2-response.md
   verbatim (modulo constants) mandatory sentence -- only the contract's
   paraphrase. Both report.md files correctly carry both forms. The AY2 gate
   (which appeared during this audit; see below) has the same gap, and its own
   `decision` text separately states "the AY2 preregistration has no template
   field".
2. `rate_claimed`/`rate_in_N_claimed` name split: AY1's and AY2's
   `preregistration.gate_fields_required` both list `rate_claimed` and omit
   `rate_in_N_claimed`, even though AY2's own "required" item 6 text lists both
   names (AY2's self-recorded defect D3) and loop2-response.md section 4 names
   only `rate_in_N_claimed`. The AY1 reverse's producer output correspondingly
   omits `rate_in_N_claimed` as an export (expected, given the contract it read
   from).
3. AY1's `states_compared`/`region`/`topology`/`closeness_order` are not
   byte-identical across forward/reverse/skeptic/gate: the reverse disagrees on
   three of four fields, and the forward disagrees on `closeness_order`
   (exports a scalar `2` where reverse/skeptic/gate export `[1, 2]`) and uses a
   different JSON type for `topology` (a dict, not a string) than either other
   source.
4. AY2's `states_compared`/`region`/`topology` are not byte-identical across
   forward, the skeptic's pre-comparison and the gate: the gate matches
   forward's longer `states_compared`/`region` text (the skeptic's
   pre-comparison alone is a shorter paraphrase), but the gate alone adds a
   dynamics clause to `topology` that neither forward nor the skeptic's
   pre-comparison has. Not contradictory in content, just not identical.
5. The phrase `"uniqueness of the AQ state"` is still physically present, inside
   `claim_exclusions` arrays (not code spans, so not whitelisted by the
   code-span rule), in the AY1 and AY2 contracts (in scope) and, beyond scope,
   also in the AZ1 and AZ2 drafts -- all inherited unchanged from
   loop2-response.md section 2's own template. Always inside an excluded-claim
   list, never asserted.
6. AY2's `preregistration.state_provenance` does not match any of the three
   closed-vocabulary prefixes -- a new "both families at once" shape plan.json's
   four-field extension does not cover.
7. AY2's `selected_after` is still the literal placeholder `"<preceding gate>"`,
   already frozen into a `frozen_before_production` contract.
8. AZ2's `parameters.j_max` is still a template placeholder
   (`"<declared, e.g. 3/2 and 2 with certified tail>"`); must be pinned before
   freezing.
9. AZ1 and AZ2 have no `gate_fields_required` field at all (unlike AY1/AY2) --
   recorded as an open interpretive question for the advisor, not asserted as a
   defect.

**Independent corroboration.** The AY2 gate (`advisor/ay2-gate.json`) appeared
on disk after this audit's analysis was substantially complete, naming its own
"contract defects D1-D6" list: `selected_after` left as `"<preceding gate>"`
(defect 7 above), `"uniqueness of the AQ state"` in the exclusions (defect 5),
and `rate_in_N_claimed` missing from `gate_fields_required` (defect 2) all
appear in it, reached independently of this audit's scripts. This is not this
audit reading its own conclusions back out of the gate: the gate's `completed_at`
timestamp and this directory's own analysis were produced independently (the
gate names three further wording defects of its own, D4-D6, outside this
audit's scope, e.g. "'within 2D' should read 'within D'").

Non-defect notes: one negated `"uniqueness of the AQ state"` occurrence in
`reverse/ay1/report.md` is plain prose, not inside a code span (wording hygiene,
not a violation); the `first_order_distance_from_product` tier name is never
confused with a sub-label; AZ1/AZ2's boolean-style `target` values are
syntactically well-posed.

**This is a live, concurrently-advancing repository.** While this sub-round-4
audit was in progress, several files this audit does not itself modify appeared
or changed on disk: `skeptic/ay2.json`/`ay2.md`/`ay2-replays.json`/
`ay2-postreview/` (the AY2 *final* skeptic review, distinct from the
`ay2-independent` pre-comparison the calling task names as this audit's
input), `advisor/ay2-gate.json` (absent at the calling task's naming --
"gate may not exist yet, handle absence" -- but present by the time this audit
finished; both scripts now read it, guarded by an existence check, and both are
updated above to report on it), `advisor/admission-spec.json` and `advisor/
findings.json` (updated by the advisor to record sub-round 4's outcome), and
`research/round32/experts/historical/assistant-4/` (a sibling lens's own
sub-round-4 work). None of these were written by this audit; `git status`
confirms every file this session touched is under `research/round32/experts/
jung/assistant-4/`. `preregistration_audit_4.py` audits only the four
*contracts* (ay1.json, ay2.json, az1.json, az2.json), which did not change
during this run, so its results are unaffected by the AY2 gate's appearance;
`sentence_and_gate_field_audit.py` was updated once the gate appeared, and its
results above reflect it.
