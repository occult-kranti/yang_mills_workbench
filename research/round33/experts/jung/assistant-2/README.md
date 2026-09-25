# Jung/Pauli lens, Round33 sub-round 2, assistant-2 (BB1/BB2 phrase, template, vocabulary and hypotheses audit)

This package is the Jung/Pauli lens's research-assistant audit for Round33
sub-round 2 (loops BB1 and BB2), assigned directly by the coordinating agent.
**These outputs count zero research loops.** Nothing here is a producer, a
contract, a gate or a skeptical review; nothing computed here is read back into
any contract, gate or skeptical review; nothing here decides whether BB1/BB2
are accepted. **BB1 and BB2 are not yet gated**: at the time this package was
written, no `research/round33/advisor/bb1-gate.json` or `bb2-gate.json` exists,
so every check here reads the four frozen producer packets directly, not a
gate. Human project author: Hruday N M (BUNZEEY); AI-assisted. Standard
library only (`json`, `re`, `pathlib`). Run every script with `python3 -B`.
Nothing here imports `forward/*/check.py`, `reverse/*/check.py`, any other
producer/skeptic module, or any earlier round's or sub-round's assistant
scripts; it imports `research/round33/tools/phrase_scan.py` as a library,
exactly as the calling task permits (that module is infrastructure — rule R6
of the Round32 closing panel — and computes no scientific result of its own).

This package mirrors the file layout and self-contained-closure discipline of
`research/round33/experts/jung/assistant-1/` (sub-round 1, BA1/BA2), adapted to
this sub-round's own, different task list and to BB1/BB2's narrower, ungated
input scope.

## Inputs (exactly as named by the calling task)

- `research/round33/contracts/bb1.json`, `bb2.json`
- The four frozen producer packets, **`report.md` and `output/results.json`
  only**: `research/round33/{forward,reverse}/{bb1,bb2}/`
- `research/round33/advisor/plan.json` (the closed vocabulary)
- `research/round33/skeptic/bb2-replays.json`

No gate file, no skeptic `.md`/`.json` review, no `admission-spec.json` and no
producer `check.py` is read (BB1/BB2 have no gate or skeptic verdict yet, and
`check.py` files are producer code, never imported here).

## Files

- `common2.py` — shared path constants (contracts, the four report/results
  files per loop), JSON walkers (`walk_json_items`/`walk_all_strings`/
  `find_key_occurrences`/`dicts_with_key`), and the clause-splitting helpers
  (`normalize`/`clauses`) built on the same rule `tools/phrase_scan.py` itself
  uses, so "same clause" means the same thing here as it does to the real R6
  scanner and to assistant-1's own package before it.
- `phrase_audit.py` — calling task item 1: (a) a dry run of the real
  `tools.phrase_scan.scan` with each contract over its own loop's four packet
  files (`forward`/`reverse` `report.md` scanned as one blob each;
  `forward`/`reverse` `output/results.json` scanned **string field by string
  field**, per the calling task's own wording), listing every hit — affirmative
  or negated — with its clause, each further classified as `negated_exclusion`,
  `quoted_mention_or_control_description` (a producer's own damaging-mutation
  self-test record) or `AFFIRMATIVE_needs_review`; (b) a rate-claim audit over
  every clause of all four `report.md` files for `O(1/N)`, the bare word
  "geometric"/"geometrically", the bare word "decay"/"decays", or the literal
  phrase "rate in N", flagging whether that clause carries an explicit
  two-sided numeric range of N (e.g. `5<=N<=14000` or `N=5..59`) — separating
  out the frozen `mandatory_sentence_template`'s own quotation (contract
  wording, not a producer's prose) from genuine producer prose, and checking
  the calling task's own named instance directly.
- `template_and_fields.py` — calling task item 2: rule R7 (the contract's
  `mandatory_sentence_template` appears exactly once, as one unbroken
  normalized span, in each packet's own `report.md`), cross-checked against
  each producer's own self-reported occurrence count where one exists; a
  gate-field comparison against each contract's `gate_fields_required`,
  handling BB2's before/after-discharge blocks exactly as the calling task
  names them (reverse's top-level `gate_fields` = before-discharge, its
  `gate_fields_after_discharge` = after; forward's top-level `gate_fields` =
  its own `gate_fields_proposed` = after-discharge shape, its
  `gate_fields_if_undischarged` = before), plus a cross-producer comparison of
  the two "before discharge" blocks against each other.
- `vocabulary_mirror.py` — calling task item 3: every `tier`, `route`,
  `assembly`, `sub_label` (the document's own top-level `label` and
  `secondary_sub_labels` fields — the bare key `"label"` is heavily overloaded
  elsewhere in these `results.json` files for unrelated descriptive tags, so
  only the top-level fields are read as a sub_label) and `dynamics_level`
  value used anywhere in the four `output/results.json` files, checked against
  `plan.json`'s closed vocabulary and each contract's own declared subset; the
  `tier_label_rule` check that no BB1 constant's `route` field is a BA1-only
  route (`analytic_disc`, `weighted_norm`); a check that every BB2 state
  constant (tier `exact_first_order`/`crude_majorant`) carries a sibling
  `assembly` and hypothesis-source marker; a non-blocking transparency note on
  which sub_label each producer of each loop actually picked.
- `hypotheses_map.py` — calling task item 4: extracts BB2 forward's own
  `H1`–`H4` (+ labelled secondary `H1s`–`H3s`) hypotheses list and BB2
  reverse's own `item1`–`item5`/`secondary`-keyed `hypotheses_used` dict
  (which names BB1 comparisons by position, `B3`/`B4`/`B5`), maps both onto
  this script's own `c1`–`c5` positional labelling of BB1's five unlabelled
  `parameters.comparisons` entries, tabulates per BB2 item which BB1
  comparisons, forms, cutoff regimes and signs each producer uses, and
  compares the two producers' maps. **This is input for the skeptic's future
  BB1-discharge review, not a decision** (the calling task's own words) — it
  records disagreements, it does not adjudicate them.
- `summarize.py` — calling task item 5's own `results.json` requirement
  ("overall_pass; findings"): rolls up the four scripts' `passed` flags into
  one `overall_pass`, and collects every `DEFECT`/`DISAGREEMENT` finding line
  from all four scripts into one list, without recomputing anything.
- `results.json` — merged output of all five scripts, in the same
  read-modify-write convention as assistant-1's `common1.py`. Byte-identical
  under normal and `-B -O` Python (checked directly for this run;
  sha256 `89c2a23b7ac657d181cf246c38307fea659ee48b41db1eac0825a8033df96b8f`).

## How to run

```bash
cd research/round33/experts/jung/assistant-2
rm -f results.json
python3 -B phrase_audit.py
python3 -B template_and_fields.py
python3 -B vocabulary_mirror.py
python3 -B hypotheses_map.py
python3 -B summarize.py
```

Each script prints PASS/FAIL (or, for `hypotheses_map.py`, "recorded") per
sub-check and a findings list. `template_and_fields.py` exits 0 (no defects).
`hypotheses_map.py` always exits 0 by design — it tabulates disagreements for
the skeptic's discharge, it never blocks. `phrase_audit.py` exits 0 (its
`phrase_scan_dry_run` finds 0 `AFFIRMATIVE_needs_review` hits and its
`rate_claim_audit` is a find-and-tabulate check, not a gate — it records every
unqualified rate clause, including the calling task's own named BB2-forward
defect, without failing). **`vocabulary_mirror.py` exits 1**: its
`closed_vocabulary_membership` sub-check finds one genuine, itemized
closed-vocabulary defect (below). A non-zero exit here is expected and is the
point of this tool, exactly as assistant-1's own README states for its
sub-round: the job is to surface real, itemized defects, not to gate
admission. BB1 and BB2 are not gated by this package or by anything it reads;
only a future advisor gate and the skeptic's review decide their outcome.

## Results and every defect/disagreement found

### 1. `phrase_audit.py`

**(a) `phrase_scan_dry_run` — PASS, 0 affirmative defects.** Ran the real
`tools.phrase_scan.scan` (negation-aware; each contract's own
`mandatory_sentence_template` removed as one literal before scanning) with the
BB1 contract over BB1's 4 packet files and with the BB2 contract over BB2's 4
packet files (`report.md` scanned as one blob; `output/results.json` scanned
string field by string field). 46 raw hits total, every one in
`reverse/bb1/report.md` (8, all `negated_exclusion`),
`reverse/bb1/output/results.json` (13, all `quoted_mention_or_control_
description`), `reverse/bb2/report.md` (4, all `negated_exclusion`) and
`reverse/bb2/output/results.json` (21, all `quoted_mention_or_control_
description`); every forward file and every BB1/BB2 `output/results.json`
scanned string field by string field elsewhere is completely clean. Every one
of the 46 hits is either an explicit negation (the reverse reports' own
"never"/"not"/"rejected" framing of a forbidden phrasing, e.g. "coefficient
decay is never called state decay") or a quoted mention inside a producer's
own damaging-mutation self-test record (a `"phrase"`/`"clause"` pair or an
`affirmative_<name>`/`rejected_mutations` entry that must literally CONTAIN
the forbidden text to prove `tools/phrase_scan.py` correctly rejects that
hypothetical mutation) — none is this project's own affirmative claim.

**(b) `rate_claim_audit` — 50 rate-claim clauses found across all four
reports; 45 without a two-sided numeric range of N in the same clause, of
which 4 are the frozen `mandatory_sentence_template` itself (BB1's and BB2's
own template both say "at a rate in N" with no range — contract wording, not a
per-report defect) and 41 are producer prose.** The calling task's own named
instance is confirmed exactly: **BB2 forward states the item-5 O(1/N) rate in
8 separate clauses and never once states the certified range `5<=N<=14000`
anywhere in its report** — including the headline restatement ("the rate is
`O(1/N)`."), the dedicated "**Rate.**" paragraph ("The rate in `N` is
`O(1/N)`: ..."), the "**Meaning.**" paragraph, the scaling-section summary line
("geometric `q = 1/64` ..., `O(1/N)` for correlations with the polynomial
`F`"), and even a numerical illustration ("`N` times the bracket is at most
`6x10^-9` for `N = 5..59`", a demonstration range, not the certified one). By
contrast, **BB2 reverse's report carries the certified range explicitly, in
one clause each, six times** ("Certified O(1/N) on `5<=N<=14000`",
"**8.5 Rate in N** ... certified range and where the frozen form stops being
useful", "**Item 5 rate range.** The frozen bracket is O(1/N) only on the
certified range `5<=N<=14000`", etc.) — but the reverse report *also* restates
the bare O(1/N) claim several times without repeating the range in that same
clause (e.g. "The rate is O(1/N) because the Lieb–Robinson function ... is
polynomial", "no exponential rate in `N` is claimed for item 5"), so even the
producer that proves the range does not attach it to every restatement — the
calling task's actual point is narrower and confirmed as stated: BB2 forward
never states the range anywhere, not even once. BB1 reverse carries two
unqualified "rate in N" clauses outside its own template quotation (both
one-line restatements of the headline meaning, e.g. "This is locality of the
reduced densities of the named constructions at a rate in `N`"); BB1 forward
carries none outside its own template quotation. Both BB1 reports also carry a
scattering of unrelated "decay"/"geometric" clauses about coefficient decay,
the global Lipschitz constant, or Weierstrass convergence — none of these is a
rate-of-N-decay claim the way the BB2 item-5 dynamics rate is; full detail
(every clause, tagged) is in `results.json`.

### 2. `template_and_fields.py` — PASS, 0 defects

**`mandatory_template_span_check` (rule R7) — PASS.** Each of the four
packets' own `mandatory_sentence_template` (BB1's 621 characters, BB2's 827)
appears, verbatim after whitespace normalization, as exactly one unbroken span
in that packet's own `report.md`. BB2 forward's own self-reported
`mandatory_sentence_verbatim_once` check (`occurrences_in_report: 1, passed:
true`) is cross-checked, not trusted, and agrees; the other three packets
carry no such self-reported check, so this script's own independent count is
the only record for them.

**`gate_fields_comparison` — PASS.** BB1 has no discharge complexity: both
producers' single `gate_fields` block has exactly the 11 keys of
`contracts/bb1.json#/preregistration/gate_fields_required`, every value equal,
and forward's block equals reverse's block field for field. **BB2's
before/after-discharge blocks, exactly as the calling task names them:**
reverse's top-level `gate_fields` (before-discharge: every BB1-dependent field
false, `dynamics_level` at the BA2 algebraic level) has the full 16-key set
(value differences from the contract are the intended before-discharge state,
not scored); reverse's `gate_fields_after_discharge` equals
`contracts/bb2.json#/preregistration/gate_fields_required` exactly; forward's
`gate_fields` equals its own `gate_fields_proposed` exactly, and that block
also equals the contract's `gate_fields_required` exactly (the after-discharge
shape); forward's `gate_fields_if_undischarged` has the full 16-key set (same
before-discharge treatment as reverse's top level). **One recorded, non-
blocking difference**: comparing the two producers' own "before discharge"
blocks field for field (forward's `gate_fields_if_undischarged` vs reverse's
top-level `gate_fields`) finds all 16 keys present on both sides with every
value equal **except `dynamics_level`**: forward writes
`"not_set (conditional_on_bb1_targets)"`, reverse writes
`"algebraic_heisenberg_compact_window"` (the BA2 algebraic level).
`vocabulary_mirror.py` below shows that reverse's value is a member of
`plan.json`'s closed `dynamics_level` set and forward's is not — this is the
one genuine defect this package found.

### 3. `vocabulary_mirror.py` — 1 genuine defect

**`closed_vocabulary_membership` — FAIL, 1 defect.** Every `tier` value used
(BB1: `crude_majorant`, `exact_first_order`; BB2: `exact_first_order`,
`polynomial_lieb_robinson`), every `route` value used (BB1:
`iterated_split`, `polymer_kp`; BB2: `duhamel_inner_f1`, `duhamel_inner_f2`),
every `assembly` value used (BB2: `nested_telescoping`, `union_comparison`)
and every top-level `label`/`secondary_sub_labels` sub_label value used (BB1:
`boundary_decay_rate_only`, `static_not_dynamic`; BB2:
`common_limit_of_named_constructions`, `convergence_of_named_constructions`)
is a member of `plan.json`'s closed vocabulary and of each contract's own
declared subset. **The one exception**: BB2 forward's
`gate_fields_if_undischarged.dynamics_level` value **`"not_set
(conditional_on_bb1_targets)"`** is **not** a member of `plan.json#/
vocabulary/gate_fields/dynamics_level`'s own two-value closed set
(`algebraic_heisenberg_compact_window`, `correlation_functions_compact_window`)
— the same value `template_and_fields.py` already flagged as differing from
reverse's own before-discharge value, which *is* a member of that set. This is
a real, itemized cross-file defect: forward invented a third `dynamics_level`
string for the "not yet discharged" state instead of reusing the plan's own
`algebraic_heisenberg_compact_window` (the value reverse and the BA2 contract
both already use for exactly this state).

**`tier_label_rule_bb1` — PASS, 0 violations.** No BB1 constant's `route`
field is a BA1-only route: forward's 19 `route` export sites are all
`polymer_kp` (BB1 forward's own route); reverse's 6 export sites are all
`iterated_split` (BB1 reverse's own route). BA1 route names (`analytic_disc`)
appear only inside descriptive `ba1_input` strings (e.g. `"gate bound value
K=49/111790368 (analytic_disc)"`), exactly the use the contract's own
`tier_label_rule` permits ("the BA1 route of the input is recorded as the
input, never as the BB1 route") — never as the `route` field itself.

**`bb2_state_constant_assembly_and_hypothesis_source` — PASS, 0 violations.**
Every BB2 state constant (9 in forward, 4 in reverse, each carrying tier
`exact_first_order`) has a sibling `assembly` field and a sibling
`hypothesis_source`/`source` field equal to `"bb1_frozen_targets"`.

**`sub_label_agreement_note` — informational, not scored.** BB1 forward and
reverse pick *different* members of the same allowed 2-entry list
(`static_not_dynamic` vs `boundary_decay_rate_only`) — both legitimate per the
contract, recorded for transparency, not a violation. BB2 forward and reverse
agree exactly (`convergence_of_named_constructions`, with
`common_limit_of_named_constructions` as the shared secondary sub_label).

### 4. `hypotheses_map.py` — a tabulation, not a decision

BB1's contract lists five unlabelled comparisons, given this script's own
`c1`–`c5` positional labels. **Forward** names its own hypotheses `H1`–`H4`
(`H1`=`c1`, `H2`=`c2`, `H3`=`c3`, `H4`=`c5`) plus a labelled secondary
`H1s`–`H3s`; its own report states explicitly that BB1's `c4` ("any two
centered boxes `Lambda_M`, `Lambda_M'` ..., compared directly, not by
telescoping") is **not used** by its nested-telescoping assembly — confirmed
here (no forward hypothesis matches `c4`). **Reverse** names its own
hypotheses by BB1 comparison-list position (`B3`=`c3`, `B4`=`c4`, `B5`=`c5`);
its own report states `c1`/`c2` (its own `B1`/`B2`, "the forward's nested
telescoping") are **not used** by its union-comparison assembly. Per BB2 item,
the two producers cite **different subsets** of BB1's comparisons in every
case except the labelled secondary pair: item 1 forward=`{c1,c2}` vs
reverse=`{c4,c5}`; item 2 forward=`{c1,c2,c3}` vs reverse=`{c3}`; item 3
forward=`{c1,c2,c3}` vs reverse=`{c3,c4,c5}`; item 4 forward=`{c1,c5}` vs
reverse=`{c5}`; item 5 forward=`{c1,c2,c3}` vs reverse=`{c4,c5}`. Every
`forms` set agrees once cosmetic annotation differences are normalized away
(forward's bare `R`/`region` vs reverse's `R (C_h)`/`region (c_h)` etc.), and
every `signs` set agrees except the labelled secondary pair (forward states
`+`/`-` explicitly; reverse's `secondary` block does not list signs). **These
disagreements are expected, not defects**: they follow directly from the two
producers' different, contractually-independent assemblies (forward:
nested_telescoping, chaining single-step comparisons `c1`/`c2`; reverse:
union_comparison, using the general two-volume comparisons `c4`/`c5`
directly, with `c1`/`c2` treated as their own nested special case and not
separately invoked). This map is recorded in full, per item, in
`results.json`, as **input for the skeptic's future BB1-discharge review, not
a decision** — exactly as the calling task frames it.

## Summary (`summarize.py`, `results.json#/summary`)

`overall_pass = false`. `phrase_audit=True`, `template_and_fields=True`,
`vocabulary_mirror=False`, `hypotheses_map=True`. The one thing that makes
`overall_pass` false is `vocabulary_mirror.py`'s single genuine defect (BB2
forward's `"not_set (conditional_on_bb1_targets)"` dynamics_level value, not
in `plan.json`'s closed vocabulary) — exactly as intended: this package's job
is to surface real, itemized defects and disagreements for the advisor and the
skeptic, never to gate BB1/BB2's admission itself. The rate-claim audit's 8
BB2-forward "DEFECT (per calling task)" lines and the hypotheses map's 6
"DISAGREEMENT" lines are both find-and-tabulate results (their own scripts'
`passed` stayed `True`), collected into `results.json#/summary/
defect_and_disagreement_lines` alongside the one true `vocabulary_mirror`
defect for the advisor's convenience, not conflated with it.

## Note on the occult reading ledger

No occult or mystical source was read to produce this package (the calling
task's own instruction: append to `research/round33/experts/occult/reading-
ledger.md` only if one was; none was, so it is untouched). This package reads
only the contracts, the four producer packets, `plan.json` and
`skeptic/bb2-replays.json`, exactly as the calling task names.

**This is a live, concurrently-advancing repository.** `git status` at the end
of this work confirms every file this session touched is under
`research/round33/experts/jung/assistant-2/`.
