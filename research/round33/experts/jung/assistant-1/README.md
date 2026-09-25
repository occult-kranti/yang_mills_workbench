# Jung/Pauli lens, Round33 sub-round 1, assistant-1 (phrase/vocabulary audit)

The research-assistant audit `research/round33/experts/jung/loop2-response.md`
section 3 asks for ("What this lens's research assistant should test after
sub-round 1"), items (a)-(d). **These outputs count zero research loops.**
Nothing here is a producer, a contract, a gate or a skeptical review; nothing
computed here is read back into any contract, gate or skeptical review; nothing
here decides whether BA1/BA2 are accepted (both are already
`accepted_within_scope`, per `research/round33/advisor/ba1-gate.json` and
`ba2-gate.json` -- only the advisor's gates and the skeptic's reviews ever did
that). Human project author: Hruday N M (BUNZEEY); AI-assisted. Standard
library only (`json`, `re`, `pathlib`). Run every script with `python3 -B`.
Nothing here imports `forward/*/check.py`, `reverse/*/check.py`, any other
producer/skeptic module, or any earlier round's assistant scripts; it imports
`research/round33/tools/phrase_scan.py` as a library, exactly as the calling
task permits (that module is infrastructure -- rule R6 of the Round32 closing
panel -- and computes no scientific result of its own).

Read before this work: `research/round33/experts/jung/loop2-response.md`
(section 3 is the calling task's own source); `research/round33/advisor/plan.json`;
`research/round33/contracts/ba1.json` and `ba2.json`; `research/round33/advisor/
ba1-gate.json` and `ba2-gate.json`; `research/round33/skeptic/ba1.md`, `ba1.json`,
`ba2.md`, `ba2.json`; `research/round33/tools/phrase_scan.py`, `record_gate.py`
and `freeze_contract.py`; the four producer files `research/round33/forward/ba1/
report.md`, `reverse/ba1/report.md`, `forward/ba2/report.md`, `reverse/ba2/
report.md` and their `output/results.json` companions; `research/round32/experts/
jung/assistant-5/` (the layout and self-contained-closure discipline this package
mirrors, adapted from Round32's ten-investigation, whole-round scope down to
Round33's two-loop, one-sub-round scope).

## Files

- `common1.py` -- shared path constants (contracts, gates, skeptic reviews,
  producer reports/results for BA1 and BA2), JSON walkers
  (`walk_json_items`/`walk_all_strings`/`find_key_occurrences`), and the
  clause-splitting helpers (`normalize`/`clauses`) built on the same rule
  `tools/phrase_scan.py` itself uses, so "same clause" means the same thing
  here as it does to the real R6 scanner.
- `phrase_audit.py` -- calling task item 1 / loop2-response.md section 3 items
  (a)-(c): a dry run of the real `tools.phrase_scan.scan` over every BA1/BA2
  producer report, `output/results.json`, skeptic review and gate (14 files),
  with every hit classified beyond the tool's own negated/not-negated split; a
  hand audit of every bare "unique"/"uniquely" occurrence over the same 14
  files; a grep for bare "rate" without "in N"/"in a" in the same clause, in
  contracts, gates and skeptic supported-statements (required scope), plus
  both reports as a bonus cross-check of loop2-response.md's own slightly
  wider wording.
- `template_and_fields.py` -- calling task item 2: rule R7 (mandatory sentence
  template as one unbroken span in the gate's `accepted`/`decision` text);
  `gate.gate_fields` equals `contract.preregistration.gate_fields_required`'s
  keys with equal, reviewed values (cross-checked against the skeptic's own
  `gate_fields`); every field a contract pairs with a `<stem>_scope` sibling
  carries that scope string, non-empty, when the `<stem>_claimed` field is
  true; rule R10 (sub-labels and tier names in `plan.json`'s closed vocabulary),
  extended past what `tools/freeze_contract.py` already checks at freeze time.
- `vocabulary_mirror.py` -- calling task item 3 (rule R9 pilot):
  `plan.json#/vocabulary/forbidden` vs `tools/phrase_scan.py#ROUND_FORBIDDEN`
  vs each contract's own `forbidden_phrasings`; lists every disagreement,
  blocks nothing.
- `results.json` -- merged output of all three scripts. Produced by
  `rm -f results.json && python3 -B phrase_audit.py && python3 -B
  template_and_fields.py && python3 -B vocabulary_mirror.py`. Byte-identical
  (SHA-256 `47663bf7970ea48774f63b0e06f2f4c2da02c8766ed2c29fb848fe7abff75f7a`)
  under normal and `-B -O` Python, checked directly for this run.

## How to run

```bash
cd research/round33/experts/jung/assistant-1
rm -f results.json
python3 -B phrase_audit.py
python3 -B template_and_fields.py
python3 -B vocabulary_mirror.py
```

Each script prints PASS/FAIL per sub-check and a findings list.
`template_and_fields.py` exits 0 (no defects). `vocabulary_mirror.py` always
exits 0 by design -- an R9 sweep records disagreements, it never blocks (the
calling task's own words: "list disagreements", "as a one-loop pilot ... writing
disagreements to a file without blocking anything"). `phrase_audit.py` exits 1:
its `bare_rate_grep` sub-check finds four genuine, itemized instances of a bare
"rate" without "in N"/"in a" in claim-bearing contract text (below); its other
two sub-checks (`phrase_scan_dry_run`, `bare_unique_hand_audit`) both pass with
zero defects. A non-zero exit here is expected and is the point of this tool,
exactly as Round32 assistant-5's own README states for its whole-round sweep:
the job is to surface real, itemized defects, not to gate admission. BA1 and
BA2 are already `accepted_within_scope`; nothing here reopens that.

## Results and every defect found

### 1. `phrase_audit.py`

**(a) `phrase_scan_dry_run` -- PASS, 0 affirmative defects.** Ran the real
`tools.phrase_scan.scan` (negation-aware; each contract's own
`mandatory_sentence_template` removed as one literal before scanning) over 14
files: `forward/<loop>/report.md`, `reverse/<loop>/report.md`,
`forward/<loop>/output/results.json`, `reverse/<loop>/output/results.json`,
`skeptic/<loop>.md`, `skeptic/<loop>.json`, `advisor/<loop>-gate.json`, for
`<loop>` in `{ba1, ba2}`. 17 raw hits total, ALL in
`reverse/ba1/output/results.json` (12) and `reverse/ba2/output/results.json`
(5); every other one of the 14 files is completely clean (0 raw hits). Every
one of the 17 raw hits was classified `quoted_mention_or_control_description`
(none `AFFIRMATIVE_needs_review`): each is inside the reverse producer's own
damaging-mutation self-test record -- a `{"phrase": "<forbidden phrase>",
"clause": "<a constructed offending sentence>"}` pair, or an
`affirmative_<name>` control id -- that must literally CONTAIN the forbidden
text (`the AQ state`, `the thermodynamic limit`, `a unique limit`/`the unique
limit`, `predicts`) in order to prove `tools/phrase_scan.py` correctly rejects
that hypothetical mutation. None is this project's own affirmative claim.

**Caution for the advisor (not a defect, a scanner-behavior note).**
`tools.phrase_scan.scan` has no JSON-structure or code-span awareness.
`record_gate.py` only ever runs it over the three EXTRACTED strings
(`supported_statement`, `decision`, `limitations`) -- rule R6's actual, narrow
enforcement scope -- never over a whole `report.md` or `results.json` file. Run
the wider way the calling task asks (and this script does), it flags a
producer's own rejected-mutation test text as a raw "hit", and only a human or
a marker-aware classifier (built here) tells that apart from a genuine
affirmative claim. This is not a new discovery: `skeptic/ba2.json`'s own
`non_blocking_findings` item N11 already recorded exactly this phenomenon for
a *different* file (the frozen `skeptic/ba2-independent-derivation.md`, "a
producer-error checklist item quoting two phrases"). This script confirms the
same behavior independently, in the 14 files the calling task actually names,
and finds it is entirely confined to the two reverse producers' own
`output/results.json` self-tests -- nowhere in a report, a skeptic review or a
gate.

**(b) `bare_unique_hand_audit` -- PASS, 0 forbidden claims.** The bare word
"unique"/"uniquely" (deliberately NOT "uniqueness", which is already part of
several `tools.phrase_scan.ROUND_FORBIDDEN` literal phrases and so already
covered by (a) -- this sub-check exists specifically because Round32's own
carried-forward rule, a bare "unique" without an explicit "not" in the same
clause is forbidden, is -- per `loop2-response.md` section 2 and reconfirmed by
`vocabulary_mirror.py` below -- present as a literal token in none of
`tools.phrase_scan.ROUND_FORBIDDEN`, `plan.json#/vocabulary/forbidden`, or
either contract's `forbidden_phrasings`) appears exactly 6 times across the 14
files, at 4 distinct locations, hand-classified as follows:

1. `forward/ba1/report.md` line 53: "AM2 gives **the unique fixed point** in
   the anchored ball" -- **legitimate**: AM2's own already-admitted,
   finite-box contraction-map fixed-point uniqueness (Round29), a different,
   already-established fact, not a claim that any infinite-volume state or
   limit is unique.
2. `reverse/ba1/output/results.json` line 1611 (2 occurrences in one JSON
   string value): inside `"affirmative_unique_limit": "affirmative forbidden
   phrasing: [{\"phrase\": \"a unique limit\", \"clause\": \"The coefficients
   have a unique limit state.\"}]"` -- **legitimate**: the reverse producer's
   own damaging-mutation self-test record (same category as (a)'s finding).
3. `forward/ba2/report.md` line 85 and `reverse/ba2/report.md` line 83 (same
   sentence, quoted independently by both producers): "This limiting dynamics
   tau_t(.) can be **uniquely extended** to a one-parameter group of
   *-automorphisms on A_Gamma." -- **legitimate**: a verbatim quotation of
   Nachtergaele-Sims Theorem 4.1 (the committed source excerpt), required
   word-for-word by BA1/BA2 contract item 1 ("never paraphrase"). Asserts
   uniqueness of the EXTENSION of a given limiting dynamics to an automorphism
   group -- a standard fact from the cited external theorem about the
   *dynamics*, inherited without re-proof -- not uniqueness of the AQ state,
   an infinite-volume ground state, or any subsequential limit STATE.
4. `reverse/ba2/output/results.json` line 827: inside
   `"affirmative_unique_limit": "affirmative forbidden phrasing: the unique
   limit :: ..."` -- **legitimate**: same self-test category as item 2.

Zero occurrences are a state-uniqueness or limit-uniqueness claim by this
project.

**(c) `bare_rate_grep` -- FAIL, 4 genuine defects (2 already known, 2 new).**
Grepped for the bare word "rate" without "in N"/"in a"/"in the lattice
spacing" in the same clause (the same clause-splitting rule `tools/
phrase_scan.py` uses), in the calling task's named scope
(`contracts/ba1.json`, `contracts/ba2.json`, `advisor/ba1-gate.json`,
`advisor/ba2-gate.json`, and `skeptic/ba1.json`/`ba2.json`'s own
`supported_statement` field), plus both reports as a bonus cross-check of
`loop2-response.md` item (c)'s own slightly wider "both drafts and both
reports" wording. 77 total bare "rate" occurrences; 48 without a qualifier;
every hit is further sorted by WHERE it sits, since that changes how much it
matters:

- **`claim_or_target_text`** (parameters, required items, the mandatory
  sentence template, target notes, and every gate/skeptic
  accepted/decision/limitations/supported_statement string -- text that
  states or restates the actual result): **4 unqualified hits, all DEFECTS**:
  - `BA2 contracts/ba2.json#/parameters/targets/within_family_cauchy`:
    "...the O(1/N) rate is the honest polynomial-F rate; an N to N+1 bound
    alone is not a Cauchy estimate" (the bare word "rate" occurs twice in this
    one clause). **This is `loop2-response.md`'s own first flagged instance,
    STILL PRESENT, UNCHANGED, in the frozen contract** -- the proposed edit
    ("the O(1/N) rate in N is the honest polynomial-F rate in N") was never
    applied before BA2 froze.
  - `BA2 contracts/ba2.json#/required[3]` (item 4): "...at the honest
    polynomial rate and meet 2.5x10^-10/(N-1)...". **This is
    `loop2-response.md`'s own second flagged instance, STILL PRESENT,
    UNCHANGED, in the frozen contract** -- same unapplied proposed edit
    ("...at the honest polynomial rate in N and meet...").
  - `BA1 contracts/ba1.json#/parameters/rate_constant_pair/rate_floor/note`:
    "q_min = 37888|tau| = |tau|/tau_star at the cap; **the floor rate scales
    with |tau|**" -- **a new instance this audit found, not named by
    `loop2-response.md`** (whose own item (b)/(c) scoped its search to the
    BA2 drafts only). Lower real-world risk than the two BA2 instances: this
    sentence is about how the rate value scales with the *coupling* tau, not
    about the lattice-spacing-vs-N ambiguity the rule exists to catch, but it
    is a literal, unqualified "rate" in claim-bearing contract text by the
    calling task's own grep rule, so it is recorded as a defect, not silently
    excused.
- **`control_semantics_rule_text`** (a `new_control_semantics.<id>` entry --
  prose describing what the CHECKER rejects, e.g. "... is rejected") and
  **`scaling_bracket_note`** (a tau-scaling comment): **7 unqualified hits,
  recorded per the literal grep instruction, NOT counted as defects** -- each
  describes the checker's own rejection rule or how an already-target-bound
  constant scales with tau, not a restatement of the headline result (e.g.
  BA1's `cardinality_weight_rate_labelled`, `rate_constant_pair_prefrozen`,
  `q_min_not_crossed`; BA2's `lieb_robinson_polynomial_tail`).
- **Bonus report.md scope (not required, not counted in the defect total):**
  37 unqualified hits, all ordinary derivation prose (a table row, a named
  constant, a sub-heading) in text whose governing mandatory-sentence-template
  sentence, elsewhere in the same report, already correctly says "a rate in
  N"; none is a second, separate target-defining sentence the way the two BA2
  contract instances are.

No unqualified "rate" was found in either gate's `accepted`/`decision`/
`limitations` text or in either skeptic review's `supported_statement` --
every occurrence there already carries "rate in N" or an equivalent
qualifier.

### 2. `template_and_fields.py` -- PASS, 0 defects

**`mandatory_template_span_check` (rule R7) -- PASS.** Both BA1's and BA2's
`preregistration.mandatory_sentence_template` appear, verbatim after
whitespace normalization, as one unbroken span inside their own gate's
`accepted` text (not needed in `decision`, though `record_gate.py` accepts
either).

**`gate_fields_match_check` -- PASS.** For both loops, `gate.gate_fields`
has EXACTLY the same key set as `contract.preregistration.gate_fields_required`
(12 keys for BA1, 16 for BA2), and every value is equal, not merely present:
contract-frozen expected value = gate's exported value = the skeptic's own
reviewed `gate_fields` value, for every key. The gate never widened,
narrowed or silently diverged from what the contract required or the skeptic
reviewed.

**`true_field_scope_check` -- PASS.** BA1's `coefficient_cauchy_claimed: true`
carries its contract-declared sibling `coefficient_cauchy_scope` in the gate,
non-empty, equal to the frozen value ("AM2 creation coefficients of F1 and F2
on supports meeting R, in each on-site cutoff space"). BA2's
`whole_sequence_claimed: true` carries `whole_sequence_scope` the same way
("finite-box Heisenberg evolutions of F1 and F2 of A in B(H_R), in norm,
uniformly for |theta| at most 8; dynamics only, no state") -- this is the
calling task's own named example. Three other `true`-valued `_claimed` fields
(`rate_in_N_claimed` in both loops, `dynamics_limit_identified_claimed` in
BA2) have no `<stem>_scope` sibling declared in either contract's own
`gate_fields_required` at all, so the check correctly does not require one for
them (`plan.json#/vocabulary/gate_fields` only names a scope requirement for
`whole_sequence_claimed` and `translation_invariance_claimed`, the latter
always false in both loops) -- recorded as informational rows, not defects.

**`closed_vocabulary_check` (rule R10) -- PASS.** Both contracts' own
`tier_names_allowed` and `sub_labels_allowed` are subsets of
`plan.json#/vocabulary`'s closed lists (already enforced at freeze time by
`tools/freeze_contract.py`, re-confirmed here independently). Both gates'
`sub_label` and `secondary_sub_labels` are themselves members of
`plan.json`'s closed sub-label vocabulary -- a check `freeze_contract.py`
itself does NOT make (it only checks the contract's declared allow-list
against `plan.json`, never what the gate actually exports), so this is new
coverage, not a re-run of an existing one. Every `"tier"` value either
producer actually exports in its own `output/results.json` (BA1:
`crude_majorant`, `exact_first_order`, 23 export sites; BA2:
`polynomial_lieb_robinson`, 17 export sites) is a member of both
`plan.json`'s closed tier vocabulary and each contract's own, narrower,
declared subset -- again new coverage beyond what the freezer checks (it never
looks at what a producer later actually writes). **Bonus, non-defect note:** a
free-text `"route"` key appears throughout both loops' producer output, but it
is NOT the same closed 6-name route vocabulary `plan.json#/vocabulary/
tier_label_rule` names (`weighted_norm`, `analytic_disc`, `polymer_kp`,
`iterated_split`, `duhamel_inner_f1`, `duhamel_inner_f2`); most `"route"`
values are free descriptive prose ("forward Duhamel over the extra F2
faces"). The calling task asks only about sub-labels and tier names, so this
is not scored as a defect, but a future R9/R10-style check for `"route"`
specifically may be worth the advisor's attention if it is meant to be
closed-vocabulary too.

### 3. `vocabulary_mirror.py` -- rule R9 pilot, records disagreements, blocks nothing

`plan.json#/vocabulary/forbidden` (9 entries) and `tools/phrase_scan.py`'s
`ROUND_FORBIDDEN` (16 entries) share only 3 entries (`predicts`, `the
infinite-volume ground state`, `uniqueness of the infinite-volume ground
state`). Confirming `loop2-response.md` section 2's own reading: the 6
plan-only entries (`boundary independent (unqualified)`, `confirms`,
`correlation length`, `rate (without in N or in a)`, `uniform in a
(unqualified)`, and **`the thermodynamic limit`**) are mostly descriptive
rule-labels rather than literal scannable phrases -- **except**
`the thermodynamic limit`, which IS a literal phrase and genuinely is missing
from the round-wide scanner list (dedicated finding below). The 13
round-only entries are literal phrases the real scanner enforces round-wide
that `plan.json`'s own planning list never mentions at all (`the AQ state`,
the mass-gap-solved/proved family, the Z^3-value-confirmation phrase, the
continuum-limit-exists phrase, the fraction-of-the-problem phrase, and 6 of
the "unique ..." phrases added 2026-09-24T21:37:52Z).

**Dedicated finding 1 -- `loop2-response.md`'s own proposed fix was only
one-third applied.** `loop2-response.md` section 2 proposed adding four
SCOPED phrases -- `"unique ground state"`, `"a unique limit"`, `"unique
infinite-volume"`, `"uniquely determines the ground state"` -- to **all
three** of `ROUND_FORBIDDEN`, `plan.json#/vocabulary/forbidden`, and both
contracts' `forbidden_phrasings`, "closing the actual risk ... without
penalizing AM2's already-admitted uniqueness-of-fixed-point language." Git
history (`git log --follow -p`) shows: `loop2-response.md` was committed at
`ea3242c` (2026-09-24T21:37:29Z); `tools/phrase_scan.py` was edited 23 seconds
later at `7c4c344` (2026-09-24T21:37:52Z, commit message "scanner adds scoped
'unique' phrasings (Jung loop-2 response)"), adding 3 of the 4 proposed
phrases to `ROUND_FORBIDDEN` (`unique ground state`, `a unique limit`,
`unique infinite-volume` -- **not** `uniquely determines the ground state`,
which appears in none of the three vocabularies to this day).
`plan.json#/vocabulary/forbidden` and both `contracts/ba1.json` and
`ba2.json`'s `forbidden_phrasings` were edited again about 19 minutes later,
at `a4ff218` (2026-09-24T21:56:57Z, "deliberation loop 2 synthesis, plan v2 ...
BA1 and BA2 frozen") -- **but none of the four proposed phrases were added to
either file**, even though that same commit demonstrably touched both
`plan.json` and the two contracts for other reasons. Net effect: the fix
landed in the code every gate actually scans against (good), but the planning
document (`plan.json`) and the contracts' own extension lists were never
brought into agreement with it -- exactly the kind of divergence R9 exists to
catch, now itemized rather than described only in prose.

**Dedicated finding 2 -- a round-wide phrase plan.json names but the scanner
never carries.** `plan.json#/vocabulary/forbidden` lists `"the thermodynamic
limit"` as a round-wide forbidden phrase, but `tools/phrase_scan.py`'s
`ROUND_FORBIDDEN` has **never** contained it (checked against both its
original commit `10c01a1` and its one later edit `7c4c344` -- neither version
adds it). It is currently scanned for BA1 and BA2 only because BOTH
contracts happen to separately re-list it in their own
`preregistration.forbidden_phrasings`. A future contract that simply forgets
to re-list it would have this phrase silently NOT scanned at all for that
loop, contrary to what `plan.json`'s own vocabulary implies is a round-wide
rule.

**Dedicated finding 3 (re-confirms `loop2-response.md` section 2's own,
still-open point) -- the bare "unique" rule remains entirely unenforced
mechanically.** Round32's carried-forward rule ("a bare 'unique' without an
explicit 'not' in the same clause is forbidden") is present as a literal bare
token in NONE of `ROUND_FORBIDDEN`, `plan.json#/vocabulary/forbidden`, or
either contract's `forbidden_phrasings` -- every entry that mentions "unique"
is a longer, scoped phrase, never the bare word alone. `phrase_audit.py`'s
`bare_unique_hand_audit` (above) is this package's own manual stand-in for
this still-missing mechanical rule, exactly as `loop2-response.md` item (b)
asked for.

Both BA1's and BA2's `forbidden_phrasings` (identical 4-entry lists:
`the AQ state`, `the infinite-volume ground state`, `the thermodynamic
limit`, `uniqueness of the infinite-volume ground state`) are otherwise fully
redundant with `ROUND_FORBIDDEN` -- except for `the thermodynamic limit`
(dedicated finding 2): for that one phrase, the contract-level list is not
redundant at all, it is the ONLY place the phrase is actually enforced for
that loop.

## Summary of every defect found (for the advisor)

1. **Bare "rate" without "in N"/"in a" in claim-bearing text, 4 instances**
   (`phrase_audit.py`'s `bare_rate_grep`): `BA2 contracts/ba2.json#/
   parameters/targets/within_family_cauchy` and `BA2 contracts/ba2.json#/
   required[3]` are `loop2-response.md`'s own two previously-flagged
   instances, confirmed STILL PRESENT and UNFIXED in the frozen contract; `BA1
   contracts/ba1.json#/parameters/rate_constant_pair/rate_floor/note` ("the
   floor rate scales with |tau|") is a new instance this audit found (lower
   real-world risk: about tau-scaling, not the lattice-spacing ambiguity the
   rule targets, but literally unqualified per the calling task's own grep
   rule).
2. **`plan.json#/vocabulary/forbidden` names `"the thermodynamic limit"` as a
   round-wide rule but `tools/phrase_scan.py`'s `ROUND_FORBIDDEN` has never
   contained it** (`vocabulary_mirror.py` dedicated finding 2): it is only
   scanned today because both BA1 and BA2 happen to re-list it themselves; a
   future contract that omits it from its own `forbidden_phrasings` would not
   have it scanned at all.
3. **`loop2-response.md`'s own proposed scoped "unique ..." phrase fix was
   applied to only one of the three vocabularies it named** (`vocabulary_mirror.py`
   dedicated finding 1): `tools/phrase_scan.py`'s `ROUND_FORBIDDEN` got 3 of
   the 4 proposed phrases 23 seconds after the response was committed;
   `plan.json#/vocabulary/forbidden` and both contracts' `forbidden_phrasings`
   were edited again ~19 minutes later (freezing BA1/BA2) without ever
   receiving any of the four, and `"uniquely determines the ground state"`
   was never added anywhere.
4. **Round32's carried-forward "bare unique without an explicit not" rule
   remains mechanically unenforced** in all three vocabularies
   (`vocabulary_mirror.py` dedicated finding 3, re-confirming
   `loop2-response.md` section 2's own still-open point) -- `phrase_audit.py`'s
   hand audit substitutes for it this sub-round, finding 0 forbidden claims,
   but nothing mechanical will catch a future one.

Non-defect notes, recorded for completeness, not action: `tools.phrase_scan.scan`
run over a whole `results.json` (rather than only the narrow
`supported_statement`/`decision`/`limitations` fields `record_gate.py` itself
scans) surfaces a producer's own rejected-mutation self-test text as a raw
hit, confirmed here for all 14 files and traced to exactly 2 of them
(`reverse/ba1/output/results.json`, `reverse/ba2/output/results.json`), which
is the same behavior `skeptic/ba2.json`'s own N11 finding already documented
for a different file; a free-text `"route"` key in producer output is not the
same thing as the closed `tier_label_rule` route vocabulary and was not
scored as a defect since the calling task did not name it.

**This is a live, concurrently-advancing repository.** `git status` at the
end of this work confirms every file this session touched is under
`research/round33/experts/jung/assistant-1/`.
