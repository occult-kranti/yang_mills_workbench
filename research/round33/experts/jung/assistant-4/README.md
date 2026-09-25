# Jung/Pauli lens, Round33 applications stage, assistant-4 (BD1/BD2 phrase,
vocabulary-gap, transfer-language, template/field and applications-ledger audit)

This package is the Jung/Pauli lens's research-assistant audit for Round33's
applications stage (loops BD1 and BD2), assigned directly by the coordinating
agent. **These outputs count zero research loops.** Nothing here is a
producer, a contract, a gate or a skeptical review; nothing computed here is
read back into any contract, gate or skeptical review; nothing here decides
whether BD1/BD2 are accepted. **BD1 and BD2 are already gated
`accepted_within_scope`** (`research/round33/advisor/bd1-gate.json`,
`bd2-gate.json`), so every check here re-derives an independent audit over
their already-frozen text; it neither reopens nor could reduce either
verdict. Human project author: Hruday N M (BUNZEEY); AI-assisted. Standard
library only (`json`, `re`, `hashlib`, `pathlib`). Run every script with
`python3 -B`. Nothing here imports `forward/*/check.py`, `reverse/*/check.py`,
any other producer/skeptic module, or any other round or assistant package's
scripts; it imports `research/round33/tools/phrase_scan.py` as a library,
exactly as the calling task permits (that module is infrastructure -- rule R6
of the Round32 closing panel -- and computes no scientific result of its
own).

This package mirrors the file layout and self-contained-closure discipline of
`research/round33/experts/jung/assistant-3/` (sub-round 3), adapted to this
package's own, different task list (a phrase scan of the BD1/BD2 packets and
the round-level `findings.json`/`roadmap.json` text; a reapplication of
sub-round-3's vocabulary-gap and heading-list-severance findings to this new
text; a new transfer-language audit; a template-and-gate-field audit against
`plan.json`'s vocabulary; and an applications-ledger audit of
`findings.json#/applications`, which did not exist when assistant-3 ran).
Round33's applications stage (BD1, BD2) is complete and both loops are
gated -- unlike assistant-3's BC1/BC2 package, this package needed no
"in-production" exclusion.

## Inputs (exactly as named by the calling task)

- `research/round33/contracts/bd1.json`, `bd2.json`
- The frozen BD1/BD2 packets, **`report.md` and `output/results.json` only**:
  `research/round33/forward/{bd1,bd2}/`, `research/round33/reverse/bd1/` (BD1
  has a reverse producer, `direction: "paired"`; BD2 does not,
  `direction: "single+skeptic"`, so no `research/round33/reverse/bd2/`
  exists)
- The BD1/BD2 gates: `research/round33/advisor/bd1-gate.json`, `bd2-gate.json`
- The BD1/BD2 reviews: `research/round33/skeptic/bd1.json`, `bd2.json` (their
  `supported_statement` field for the phrase/vocabulary audit; their whole
  object for the gate-field comparison and the applications-ledger source
  binding)
- `research/round33/advisor/findings.json` (its `applications` list,
  `summary` and `scope_statement`) and `research/round33/advisor/roadmap.json`
- `research/round33/advisor/plan.json` (the closed vocabulary)

**Scan scope, exactly as the calling task lists it** (item 1): the three BD
reports (`forward/bd1/report.md`, `reverse/bd1/report.md`,
`forward/bd2/report.md`), the two BD gates (`accepted`+`limitations`), the two
reviews' `supported_statement`, `findings.json#/summary`,
`#/scope_statement` and `#/applications`, and all of `roadmap.json`. BD-scoped
text is scanned with that loop's own contract vocabulary (`ROUND_FORBIDDEN` +
that contract's `forbidden_phrasings`, with that contract's own
`mandatory_sentence_template` removed as one literal); the round-level text
(the three `findings.json` fields and `roadmap.json`, which are not tied to
one loop) is scanned with the union of both contracts' `forbidden_phrasings`.
The two BD contracts supply this vocabulary and are not themselves scanned as
text (the same convention assistant-3 used: a contract's own
`forbidden_phrasings` array is the vocabulary declaration, not a claim about
BD1/BD2). No other round's or sub-round's loop (`bc1`, `bc2`, `ba1`, ... ) is
read here: the calling task names BD1 and BD2 only.

No producer `check.py` is imported anywhere in this package (producer code is
never a permitted import; only `tools/phrase_scan.py` is).

## Files

- `common4.py` -- shared path constants (contracts, gates, reviews, reports
  for BD1/BD2; `findings.json`/`roadmap.json`/`plan.json`), JSON walkers
  (`walk_json_items`/`walk_all_strings`/`find_key_occurrences`), a `sha256_file`
  helper, and the clause-splitting helpers (`normalize`/`clauses`) built on
  the same rule `tools/phrase_scan.py` itself uses, so "same clause" means the
  same thing here as it does to the real R6 scanner and to every earlier
  assistant package's own audits.
- `phrase_audit.py` -- calling task item 1, four checks:
  - `phrase_scan_dry_run` -- the real `tools.phrase_scan.scan`
    (negation-aware) run over the exact scan scope above. **Total raw hits: 0**
    (not merely 0 unnegated ones), cross-checked against each review's own
    self-reported `phrase_scan` block over the sub-scope it covers
    (`limitations` + `supported_statement`) and found equal.
  - `vocabulary_gap_audit_bd` -- reapplies assistant-3's sub-round-3
    vocabulary-gap audit (the real scanner's vocabulary contains neither
    "uniqueness of the limit" nor "uniqueness of every infinite-volume ground
    state") to this package's own scan scope. **4 occurrences found, all
    inside `roadmap.json`, 0 classified bare affirmative**: one genuinely
    negated exclusion clause (`roadmap.json#/goals[1]/limitations[1]`) and
    three occurrences of the same forward-looking vocabulary-list mention in
    `roadmap.json#/methods_decision` (the note recommending exactly these
    phrasings be added to the scanner before Round34 -- itself written in
    response to assistant-3's own finding).
  - `heading_list_severance_check` -- reapplies assistant-3's second,
    independently found mechanism (a `"... exclusions (verbatim): item;
    item; ..."` heading severs its own negation/exclusion cue from every
    list item that follows it, via `phrase_scan.py`'s own `": "` clause
    split) to the three BD reports. **Found 3 such headings** (BD1 forward:
    7 items; BD1 reverse: 1 item; BD2 forward: 8 items) and mechanically
    checked every list item against the union of `ROUND_FORBIDDEN`, both BD
    contracts' `forbidden_phrasings` and the five uniqueness candidates:
    **0 collisions** -- the mechanism is present here exactly as in
    sub-round 3, but causes no false negative in this corpus today.
  - `transfer_language_audit` -- new to this package: every
    `findings.json#/applications` entry of `kind: "transfer"` (4 of 12
    entries) names one of the five canonical BD models (one-plaquette model,
    group-G box, finite graph, Z^3 family, 2+1D constants) in its own `model`
    field; the scan scope is searched for "predicts", "confirms",
    "universal", "string tension" and "confinement" -- **0 occurrences at
    all** (these words appear only inside the BD1/BD2 contracts' own
    `forbidden_phrasings` arrays, outside the scan scope by the same
    contracts-supply-vocabulary convention); and the three BD reports are
    searched for a one-plaquette or graph value phrased as a lattice-limit
    value -- **0 bare affirmative occurrences** (two are mechanically negated
    by the real `NEGATION` rule; two more are markdown rejected-mutation
    table rows, confirmed by a `| \`control_id\` |` structural marker rather
    than assumed, since the mechanical rule alone does not classify a bare
    table cell).
- `template_and_fields.py` -- calling task item 2, two checks:
  - `mandatory_template_span_check` (rule R7) -- each contract's own
    `mandatory_sentence_template` appears, verbatim after whitespace
    normalization, as exactly one unbroken span in every one of that loop's
    reports (`forward/bd1/report.md` and `reverse/bd1/report.md` for BD1;
    `forward/bd2/report.md` for BD2) and in `advisor/<loop>-gate.json#/accepted`,
    cross-checked against each forward report's own self-reported
    template-span check (`forward/bd1/output/results.json#/checks[29]`;
    BD2's own id not separately located but the direct count still applies).
  - `gate_fields_comparison_bd` -- every `gate_fields` key the contract
    requires (`preregistration.gate_fields_required`; 12 keys for both BD1
    and BD2) is compared, value for value, across the contract, the gate's
    exported `gate_fields` and the review's exported `gate_fields`, and
    checked against `plan.json`'s own `vocabulary.gate_fields` rule for that
    field where the rule states a concrete, checkable condition (BD1's
    `uniqueness_of_ground_state_claimed`/`rate_in_a_claimed`/`continuum_claim`
    and BD2's `area_law_claimed` each carry plan.json's "always false" rule).
    The calling task's seven named fields each get their own dedicated,
    narrated check: BD1's `flip_transfer_scope`, `obstructions_recorded` and
    `area_parity_limit_claimed`; BD2's `graph_sign_certified`,
    `z3_1x2_formal_only`, `electric_band_scope` and `area_law_claimed`.
    `flip_transfer_scope` is a documented exception: the contract's own text
    states the *general rule* ("the listed groups ... named in the gate
    group by group"), while the gate and review correctly export the
    *concrete instantiation* (SU(2), SU(4), U(1), Z2) instead -- exactly the
    non-blocking contract defect `bd1-gate.json#/limitations` itself
    records, re-verified here by content (gate and review agree verbatim,
    name all four required groups, name none of the three flip-obstructed
    groups SU(3)/SU(5)/SO(3), and the contract text is confirmed to state
    the general rule) rather than flagged as a spurious contract/gate string
    mismatch.
- `applications_ledger_audit.py` -- calling task item 3, three checks:
  - `schema_check` -- every one of the 12 `findings.json#/applications`
    entries (6 BD1, 6 BD2; 4 `transfer`, 4 `obstruction`, 4 `partial`) has
    non-empty `loop_id` (in `{bd1, bd2}`), `problem`, `equation`, `outcome`,
    `model`, `kind` (in `{transfer, obstruction, partial}`) and a non-empty
    `sources` list. **0 schema defects.**
  - `sources_bound_by_gate_check` -- every one of the 30 source citations
    across those 12 entries is a key of its own loop's gate `bindings` dict,
    the file exists on disk, and its sha256 today equals the sha256 the gate
    bound at freeze time (the repository's own historical-immutability rule,
    re-verified rather than assumed). **0 defects**; the 5 distinct sources
    cited are `forward/bd1/report.md`, `reverse/bd1/report.md`,
    `skeptic/bd1.md`, `forward/bd2/report.md` and `skeptic/bd2.md`.
  - `numbers_cross_check` -- every exact fraction token (17 total, e.g.
    `1/589824`) in an entry's `outcome`/`equation`/`detail` text is checked
    for a verbatim (whitespace-stripped) substring match in its own gate's
    `accepted`+`decision` text; every decimal-scientific-notation preview
    token (6 total, e.g. `1.34e-12`) is checked for a same-magnitude match
    (relative tolerance 5%) against a preview the gate text itself carries,
    since the ledger rounds more coarsely than the gate (e.g. the ledger's
    `2.88e-19` against the gate's own `2.87586637818e-19`). **0 unsupported
    numbers.**
- `summarize.py` -- calling task item 4's own `results.json` requirement:
  rolls up the three scripts' `passed` flags into one `overall_pass`, and
  collects every `DEFECT` finding line from all three scripts into one list,
  without recomputing anything.
- `results.json` -- merged output of all four scripts, in the same
  read-modify-write convention as every earlier assistant package's common
  module. Byte-identical under normal and `-B -O` Python (checked directly
  for this run; sha256
  `3a13b2c32c5e8d5d04390713d7f91ba4f9a299405e8bb341bec3e5bc73e84d57`).

## How to run

```bash
cd research/round33/experts/jung/assistant-4
rm -f results.json
python3 -B phrase_audit.py
python3 -B template_and_fields.py
python3 -B applications_ledger_audit.py
python3 -B summarize.py
```

Each script prints PASS/FAIL per sub-check and a findings list, and exits 0
(all four scripts pass; `overall_pass = True`).

## Results and findings

### 1(a). `phrase_audit.py` -- `phrase_scan_dry_run`: PASS, 0 hits at all

Ran the real `tools.phrase_scan.scan` (negation-aware) over the three BD
reports, both gates' `accepted`/`limitations`, both reviews'
`supported_statement`, `findings.json`'s `summary`/`scope_statement`/
`applications`, and every string field of `roadmap.json`. **Total raw hits:
0** for the entire scan scope -- not merely zero unnegated ones, zero at all.
Independently recomputed the sub-scope each review's own `phrase_scan` block
covers (`limitations` + `supported_statement`) and found it equal to the
review's own self-reported `all_hits_including_negated` (0 for both BD1 and
BD2).

### 1(b). `phrase_audit.py` -- `vocabulary_gap_audit_bd`: PASS, 0 bare affirmative hits

Reapplied assistant-3's five candidate phrasings ("uniqueness of the limit",
"unique limit", "uniqueness of every infinite-volume ground state", "is
unique", "uniquely") to this package's own scan scope. **4 occurrences
found, all inside `roadmap.json`**, none in the BD1/BD2 reports, gates,
reviews or `findings.json`'s three scoped fields:

| location | phrase | classification |
|---|---|---|
| `roadmap.json#/goals[1]/limitations[1]` | uniqueness of every infinite-volume ground state | negated_excluded |
| `roadmap.json#/methods_decision` | uniqueness of the limit | vocabulary_list_mention |
| `roadmap.json#/methods_decision` | unique limit | vocabulary_list_mention |
| `roadmap.json#/methods_decision` | uniqueness of every infinite-volume ground state | vocabulary_list_mention |

The negated occurrence ("Uniqueness on R within a named class is not
uniqueness of every infinite-volume ground state.") is genuinely negated in
its own clause by the mechanical `NEGATION` rule. The three
`methods_decision` occurrences are the roadmap's own forward-looking note --
"extend the phrase scanner's list with 'uniqueness of the limit' and 'unique
limit', and add 'uniqueness of every infinite-volume ground state' only
together with a fix for the heading-list clause severance found by the Jung
assistant (experts/jung/assistant-3)" -- quoting exactly the phrases
assistant-3 recommended adding, as a vocabulary-planning mention, not a claim
about any loop's ground state or limit. **0 hits classified bare
AFFIRMATIVE.**

### 1(b, continued). `heading_list_severance_check`: PASS, 0 collisions

Searched the three BD reports for the `"<...> exclusions (verbatim): item;
item; ..."` heading-list pattern assistant-3 found independently. Found 3
such headings: `forward/bd1/report.md`'s "Claim exclusions (contract,
verbatim)" (7 items), `reverse/bd1/report.md`'s "Claim exclusions, exactly as
the contract lists them" (1 item, itself introducing a further bulleted
list), and `forward/bd2/report.md`'s "Contract exclusions (verbatim)" (8
items). Mechanically checked every list item against the union of
`ROUND_FORBIDDEN`, both BD contracts' `forbidden_phrasings` and the five
uniqueness candidates: **0 collisions** -- none of these BD1/BD2 exclusion
items happens to equal a forbidden or candidate phrase today (for example
"any AM2, AV1 or AQ statement for a group other than SU(2)" does not equal
the forbidden phrase "the AQ state", and "any estimate uniform in the
lattice spacing a" does not equal the forbidden phrase "uniform in a"), so
the severance mechanism, present here exactly as in sub-round 3, causes no
false negative in this corpus.

### 1(c). `transfer_language_audit`: PASS, 0 defects

**Model-naming.** All 4 `kind: "transfer"` applications entries name a
canonical model: the flip-lemma and parity-theorem transfer entries (BD1)
name "one-plaquette model" and "group-G box"; the SU(2) area-parity entry
(BD1) names "Z^3 family" (the zero-selected SU(2) family on Z^3); the
two-plaquette-graph entry (BD2) names "finite graph".

**Forbidden words.** Searched the scan scope for "predicts", "confirms",
"universal", "string tension" and "confinement": **0 occurrences at all**
(these words occur only inside the BD1/BD2 contracts' own
`forbidden_phrasings` arrays and one contract control description
containing the word "forbidden" in the same clause -- both outside this
package's scan scope, since contracts supply vocabulary here and are not
scanned as text, the same convention assistant-3 used).

**Lattice-limit-value phrasing.** Searched the three BD reports for "(a/the)
lattice-limit value" and "a limit value": 4 occurrences. Two
(`reverse/bd1/report.md`) are mechanically negated by the real `NEGATION`
rule ("It is never a lattice-limit value for any group other than SU(2)."
and a run-on table-row clause that happens to also contain the word
"forbidden"). Two more (`forward/bd1/report.md`'s
`one_plaquette_model_terms` row and `reverse/bd1/report.md`'s
`changed_model_relabelled` row) are **not** mechanically negated in their
own semicolon-split clause alone -- but both are confirmed, by a `| `
`control_id` ` |` markdown-table-row structural marker (not merely assumed
from context), to be rejected-mutation table cells, not producer claims.
**0 bare AFFIRMATIVE occurrences.**

### 2. `template_and_fields.py`: PASS, 0 defects

**`mandatory_template_span_check` (rule R7) -- PASS.** BD1's template (1070
whitespace-normalized characters) occurs exactly once in
`forward/bd1/report.md`, exactly once in `reverse/bd1/report.md`, and exactly
once in `advisor/bd1-gate.json#/accepted`; BD2's template (847 characters)
occurs exactly once in `forward/bd2/report.md` (BD2 has no reverse report)
and exactly once in `advisor/bd2-gate.json#/accepted`. Cross-checked against
BD1's forward producer's own self-reported template check
(`forward/bd1/output/results.json#/checks[29]`, `passed: true`), agreeing
with this script's independent count.

**`gate_fields_comparison_bd` -- PASS.** BD1 and BD2 each have 12
`gate_fields_required` keys; for both loops the key set is identical across
contract/gate/review, and every field's value agrees across all three (12/12
and 12/12), except `flip_transfer_scope` (handled as its own dedicated
check below). The seven calling-task-named fields:

- **BD1.`flip_transfer_scope`**: gate and review agree verbatim, both
  naming SU(2), SU(4), U(1) and Z2 (and none of the flip-obstructed SU(3),
  SU(5), SO(3)); the contract's own value is confirmed to state the general
  rule ("the listed groups ... named in the gate group by group") rather
  than the concrete list -- exactly the non-blocking contract defect
  `bd1-gate.json#/limitations` records ("gate_fields_required
  flip_transfer_scope is a description, so the gate names SU(2), SU(4),
  U(1) and Z2"), re-verified here rather than mis-flagged as a plain
  contract/gate mismatch.
- **BD1.`obstructions_recorded`**: contract=gate=review=`True`, matching
  `plan.json`'s note ("BD1: the SU(3) and SO(3) cells are mandatory").
- **BD1.`area_parity_limit_claimed`**: contract=gate=review=`True`,
  matching `plan.json`'s note ("BD1: SU(2) area parity pointwise for the
  limit of the named constructions through BB2").
- **BD2.`graph_sign_certified`**: contract=gate=review=`True`, matching
  `plan.json`'s note ("BD2: finite graph only").
- **BD2.`z3_1x2_formal_only`**: contract=gate=review=`True`, matching
  `plan.json`'s note ("BD2: the Z^3 1x2 coefficient is a labelled formal
  coefficient").
- **BD2.`electric_band_scope`**: contract=gate=review agree verbatim
  ("omega(h_R) for every finite box of F1 and F2 (untruncated at fixed N)
  and the limit of the named constructions, both signs").
- **BD2.`area_law_claimed`**: contract=gate=review=`False`, matching
  `plan.json`'s explicit "always false in Round33 (no zero-free region is
  admitted)" rule.

### 3. `applications_ledger_audit.py`: PASS, 0 defects

**`schema_check` -- PASS.** All 12 `findings.json#/applications` entries (6
BD1, 6 BD2; 4 `transfer`, 4 `obstruction`, 4 `partial`) carry `loop_id`,
`problem`, `equation`, `outcome`, `model`, `kind` and a non-empty `sources`
list, every one non-empty and `loop_id`/`kind` from their allowed sets.

**`sources_bound_by_gate_check` -- PASS.** All 30 source citations across
those 12 entries are keys of their own loop's gate `bindings` dict, every
cited file exists on disk, and every current sha256 equals the sha256 the
gate bound at freeze time -- the applications ledger cites exactly the
byte-identical, gate-admitted text, not a since-edited copy. The 5 distinct
sources cited: `forward/bd1/report.md`, `reverse/bd1/report.md`,
`skeptic/bd1.md`, `forward/bd2/report.md`, `skeptic/bd2.md`.

**`numbers_cross_check` -- PASS.** 17 fraction tokens (e.g. `1/144`,
`1/63403380965376`, `7/124416`) all appear verbatim in their own entry's
gate `accepted`+`decision` text; 6 decimal-scientific-notation preview
tokens (e.g. `1.8e-17`, `1.34e-12`, `2.88e-19`, `3.4e12`, `9.8e-7`, `1.58e-3`)
all match, within 5% relative tolerance, a same-magnitude preview the gate
text itself carries (e.g. the ledger's `2.88e-19` against the gate's own,
finer `2.87586637818e-19`). **0 unsupported numbers.**

## Summary (`summarize.py`, `results.json#/summary`)

`overall_pass = true`. `phrase_audit=True`, `template_and_fields=True`,
`applications_ledger_audit=True`. Every one of the three scripts' checks
completed with zero genuine defects. This package's substantive contribution
is not a blocking defect (there is none to find in BD1/BD2's already-gated,
already-reviewed text) but the confirmation that the sub-round-3
vocabulary-gap and heading-list-severance mechanisms, reapplied to this new
text, find no bare affirmative uniqueness claim and no exploitable list-item
collision; that every transfer claim names its model and the corpus never
uses the newly forbidden words affirmatively; that the BD gate-field export
matches the plan's vocabulary field by field, including the one documented
description-vs-instantiation exception; and that the applications ledger's
evidence and numbers are exactly what its own gates recorded.

## Note on the occult reading ledger

No occult or mystical source was read to produce this package (the calling
task's own instruction: append to
`research/round33/experts/occult/reading-ledger.md` only if one was; none
was, so it is untouched). This package reads only the BD1/BD2 contracts, the
BD1/BD2 frozen packets (`report.md` and `output/results.json`), the BD1/BD2
gates and skeptical reviews, `findings.json`, `roadmap.json` and
`plan.json`, exactly as the calling task names or permits.

**This is a live, concurrently-advancing repository.** `git status` at the
end of this work confirms every file this session touched is under
`research/round33/experts/jung/assistant-4/`.
