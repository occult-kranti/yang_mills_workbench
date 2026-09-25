# Jung/Pauli lens, Round33 sub-round 3, assistant-3 (BC1/BC2 phrase, vocabulary-gap, template/field and rate-range audit)

This package is the Jung/Pauli lens's research-assistant audit for Round33
sub-round 3 (loops BC1 and BC2), assigned directly by the coordinating agent.
**These outputs count zero research loops.** Nothing here is a producer, a
contract, a gate or a skeptical review; nothing computed here is read back into
any contract, gate or skeptical review; nothing here decides whether BC1/BC2
are accepted. **BC1 and BC2 are already gated `accepted_within_scope`**
(`research/round33/advisor/bc1-gate.json`, `bc2-gate.json`), so every check
here re-derives an independent audit over their already-frozen text; it neither
reopens nor could reduce either verdict. Human project author: Hruday N M
(BUNZEEY); AI-assisted. Standard library only (`json`, `re`, `pathlib`). Run
every script with `python3 -B`. Nothing here imports `forward/*/check.py`,
`reverse/*/check.py`, any other producer/skeptic module, or any earlier
round's or sub-round's assistant scripts; it imports
`research/round33/tools/phrase_scan.py` as a library, exactly as the calling
task permits (that module is infrastructure — rule R6 of the Round32 closing
panel — and computes no scientific result of its own). **This package never
reads `research/round33/forward/bd1`, `forward/bd2` or `reverse/bd1`** (the
calling task's own restriction: BD1/BD2 are in production at the time this
package was written — no `bd1-gate.json`/`bd2-gate.json` exists yet, only
mid-production `skeptic/bd*_check.py` files and pre-freeze contract-review
notes, none of which this package opens).

This package mirrors the file layout and self-contained-closure discipline of
`research/round33/experts/jung/assistant-1/` (sub-round 1) and
`.../assistant-2/` (sub-round 2), adapted to this sub-round's own, different
task list and to BC1/BC2's own scope: **BC1 and BC2 each have a forward
producer only** — no `reverse/bc1` or `reverse/bc2` directory exists
(`direction` is `"statement+skeptic"` for BC1 and `"single+skeptic"` for
BC2) — and both are already gated, so this package's phrase scan reads the
gate and review text directly rather than waiting on a future gate, unlike
assistant-2's BB1/BB2 package.

## Inputs (exactly as named by the calling task)

- `research/round33/contracts/bc1.json`, `bc2.json`
- The frozen BC1/BC2 forward packets, **`report.md` and `output/results.json`
  only**: `research/round33/forward/{bc1,bc2}/`
- The BC1/BC2 gates: `research/round33/advisor/bc1-gate.json`, `bc2-gate.json`
- The BC1/BC2 skeptical reviews: `research/round33/skeptic/bc1.json`,
  `bc1.md`, `bc2.json`, `bc2.md`
- `research/round33/advisor/plan.json` (the closed vocabulary)

For the vocabulary-gap audit specifically (calling task item 1's own
instruction: "Search all Round33 gates, reviews and reports"), the search
scope widens to every already-gated Round33 sub-round-3 loop — ba1, ba2, bb1,
bb2, bc1, bc2 — reading each one's `advisor/<loop>-gate.json` (whole object),
`skeptic/<loop>.md` (whole text) and `skeptic/<loop>.json` (whole object), and
`forward/<loop>/report.md` plus, where it exists, `reverse/<loop>/report.md`.
BD1/BD2 are excluded throughout (in production; no gate exists for either, and
the calling task forbids reading `forward/bd1`, `forward/bd2` or
`reverse/bd1` outright).

No producer `check.py` is imported anywhere in this package (producer code is
never a permitted import; only `tools/phrase_scan.py` is).

## Files

- `common3.py` — shared path constants (contracts, gates, reviews, reports for
  BC1/BC2 and, more broadly, for all six already-gated sub-round-3 loops),
  JSON walkers (`walk_json_items`/`walk_all_strings`/`find_key_occurrences`),
  and the clause-splitting helpers (`normalize`/`clauses`) built on the same
  rule `tools/phrase_scan.py` itself uses, so "same clause" means the same
  thing here as it does to the real R6 scanner and to assistant-1's and
  assistant-2's own audits before it.
- `phrase_audit.py` — calling task item 1, two checks:
  - `phrase_scan_dry_run` (first half): the real `tools.phrase_scan.scan`
    (negation-aware, each contract's own `mandatory_sentence_template`
    removed as one literal) run with the BC1 contract over BC1's forward
    report, gate `accepted`/`limitations` and review `supported_statement`,
    and with the BC2 contract over the same four kinds of BC2 text. Every hit
    is listed with its clause, cross-checked against each review's own
    self-reported `phrase_scan` block rather than trusted.
  - `vocabulary_gap_audit` (second half): the BC1 review found that the
    scanner's vocabulary contains neither "uniqueness of the limit" nor
    "uniqueness of every infinite-volume ground state", so it could not have
    caught an affirmative uniqueness claim worded that way (the AY2 row O1
    cell in the frozen `forward/bc1/report.md`). This check searches every
    gate, review and report of the six already-gated sub-round-3 loops for
    the calling task's five named candidate phrasings ("uniqueness of the
    limit", "unique limit", "uniqueness of every infinite-volume ground
    state", "is unique", "uniquely"), classifies every occurrence as
    negated/excluded, scoped to the named constructions, or affirmative (plus
    an informational fourth tag for a hit that uses "unique(ly)" about an
    unrelated mathematical object entirely), and recommends — without
    applying — additions to the scanner's phrase list, with a computed note
    on exactly which frozen texts each recommended addition would newly flag
    (a hit is "newly flagged" wherever `tools.phrase_scan.NEGATION` alone,
    the real mechanical rule, does not match its clause).
- `template_and_fields.py` — calling task item 2, two checks:
  - `mandatory_template_span_check` (rule R7): each contract's own
    `mandatory_sentence_template` appears, verbatim after whitespace
    normalization, as exactly one unbroken span in "each report and each gate
    text" — `forward/<loop>/report.md` and
    `advisor/<loop>-gate.json#/accepted`, for both BC1 and BC2 — cross-checked
    against each forward report's own self-reported template-span check.
  - `gate_fields_comparison`: every `gate_fields` key the contract requires
    (`preregistration.gate_fields_required`) is compared, value for value,
    across the contract, the gate's exported `gate_fields` and the review's
    exported `gate_fields`, and checked against `plan.json`'s own
    `vocabulary.gate_fields` rule for that field where the rule states a
    concrete, checkable condition (e.g. "always false"). The calling task's
    two named BC1 fields (`correlation_shift_resolved`,
    `finite_box_node_claimed`) and its named BC2 field
    (`node_certificate_restated_for_limit`) each get their own dedicated,
    narrated check, plus a check of the `correlation_shift_resolved` /
    `resolved_interaction_shift` exclusivity `plan.json` describes (BC1
    restates both AV2 and AW2 and so exports the merged field; BC2 restates
    only AX2 and so exports the other one). A non-blocking, informational
    note records one structural asymmetry: the advisor gate exports
    `gate_fields` only as a nested dict, while the skeptic review
    additionally promotes every member to a flat top-level key — a
    file-format convention difference, not a value disagreement (checked
    separately, and found to agree everywhere it applies).
- `rate_range_audit.py` — calling task item 3: every rate sentence carrying a
  concrete formula in `N` (`q^(N-1)`-style, `O(1/N)`, `K5/N`, `K_F/(N-1)`, a
  Lieb–Robinson `N^-3` bound) in BC1's and BC2's forward reports and gate
  `accepted`/`limitations` text is checked for its `N`-range in the same
  clause — the BB2 lesson (a rate stated without its certified range) and the
  BC2 contract's own `rate_range_stated` control. Two rate shapes are told
  apart: a density/widening-type rate (`q^(N-1)`) is certified for every `N`
  at least a fixed floor with **no** upper bound, so a one-sided "for every
  `N` at least 2" is its correct, complete range; the inherited BB2 item-5
  correlation rate (`K5/N`) is certified only on a bounded window,
  `5<=N<=14000`, so it needs a genuine two-sided range. A clause that merely
  *describes* the `rate_range_stated` control's own rejected-mutation fixtures
  (e.g. "an appended unqualified `O(1/N)` sentence"), or that explicitly
  *disclaims* a rate rather than asserting one (negation-aware), is excluded
  from the defect count as not a producer claim. A handful of numbered-proof
  continuations state the governing theorem's range a short distance earlier
  rather than repeating it verbatim in the very next clause; these are
  recorded separately (not silently absorbed into "OK, same clause") and
  distinguished from a true standalone-claim defect.
- `summarize.py` — calling task item 4's own `results.json` requirement:
  rolls up the three scripts' `passed` flags into one `overall_pass`, and
  collects every `DEFECT`/`AFFIRMATIVE` finding line from all three scripts
  into one list, without recomputing anything.
- `results.json` — merged output of all four scripts, in the same
  read-modify-write convention as assistant-1's `common1.py` and assistant-2's
  `common2.py`. Byte-identical under normal and `-B -O` Python (checked
  directly for this run; sha256
  `ef4495397c040c6697170999e991fe34532a700207df344c88d78dda763b405f`).

## How to run

```bash
cd research/round33/experts/jung/assistant-3
rm -f results.json
python3 -B phrase_audit.py
python3 -B template_and_fields.py
python3 -B rate_range_audit.py
python3 -B summarize.py
```

Each script prints PASS/FAIL per sub-check and a findings list, and exits 0
(all four scripts pass; `overall_pass = True`). `phrase_audit.py`'s
`vocabulary_gap_audit` is a find-classify-and-recommend audit, not a pass/fail
gate on its own terms — the calling task asks to search, classify and
recommend, not to block — but it is still wired to fail if it ever finds a
bare, unscoped affirmative uniqueness claim; today it finds none.

## Results and findings

### 1(a). `phrase_audit.py` — `phrase_scan_dry_run`: PASS, 0 hits at all

Ran the real `tools.phrase_scan.scan` (negation-aware; each contract's own
`mandatory_sentence_template` removed as one literal before scanning) with the
BC1 contract over BC1's forward report, gate `accepted`, each `limitations`
entry and review `supported_statement`, and with the BC2 contract over the
same four kinds of BC2 text. **Total raw hits: 0** — not merely zero
unnegated ones, zero at all — for both loops, which matches both reviews' own
self-reported `phrase_scan` block exactly
(`all_hits_including_negated: 0, limitations_affirmative_hits: [],
supported_statement_affirmative_hits: []`, independently recomputed and
confirmed equal, for both BC1 and BC2). BC1's and BC2's forward reports do
carry occurrences of forbidden-adjacent language, but only inside their own
`negation_aware_phrase_scan` control-description rows (naming what the
checker rejects) or inside genuinely negated/excluded exclusion-list
restatements — none inside the four scanned targets themselves under the
*current* forbidden-phrase list.

### 1(b). `phrase_audit.py` — `vocabulary_gap_audit`: PASS, 0 bare affirmative hits

Searched every gate, review and report of ba1, ba2, bb1, bb2, bc1 and bc2 (42
files worth of text/JSON objects) for the calling task's five named candidate
phrasings. **Direct membership check confirmed all five are genuine gaps,
round-wide, today**: none is literally present (case-insensitive) in
`ROUND_FORBIDDEN` or in any of the six loops' own contract
`forbidden_phrasings`.

**Total occurrences found: 42**, by phrase:

| phrase | occurrences | classification |
|---|---|---|
| `uniqueness of the limit` | 10 | 6 scoped_to_named_constructions, 4 negated_excluded |
| `unique limit` | 0 | — |
| `uniqueness of every infinite-volume ground state` | 25 | 23 negated_excluded, 2 scoped_to_named_constructions |
| `is unique` | 3 | 3 different_subject_not_ground_state |
| `uniquely` | 4 | 3 different_subject_not_ground_state, 1 scoped_to_named_constructions |

**0 hits classified bare, unscoped AFFIRMATIVE** — no admitted, unscoped,
affirmative infinite-volume uniqueness claim was found anywhere in the
searched Round33 corpus.

**The calling task's own named instance** ("uniqueness of the limit", the
AY2/O1 row name): all 10 occurrences are in BC1 — the O1 obligations-table
cell in `forward/bc1/report.md` itself (`scoped_to_named_constructions`,
since its own scope qualifier, "scope: the named constructions F1 and F2
only", sits two cells later in the same table row, but a colon inside the row
splits it into a separate clause per `phrase_scan.py`'s own clause rule — so
even a smarter same-clause "does this also mention the named construction"
check would still correctly flag the row cell alone for review), plus five
quoted discussions of it in `skeptic/bc1.md`'s "The O1 decision" section and
`skeptic/bc1.json`'s `o1_decision`/`rejected_producer_wording`/
`reviewed_obligations_table` fields — never a bare unscoped claim.

**A second, general mechanism was found independently of the vocabulary gap
itself**: a "heading: list" pattern — `"Contract exclusions (verbatim):
X; Y"`, `"Not admitted: X, Y"`, `"Not inherited: X"` — puts its own
negation/exclusion cue word in a short heading clause that
`tools/phrase_scan.py`'s own `": "` clause split then severs from every item
of the list that follows, regardless of which cue word the heading used (a
plain "Not" is severed exactly as "exclusions" is). For "uniqueness of every
infinite-volume ground state" alone this affects **11 distinct frozen
locations across every one of the six loops** (ba1 forward+reverse report,
ba2 gate+reverse report+review, bb1 forward+reverse report, bb2 reverse
report, bc1 forward report+review, bc2 forward report) — 15 raw occurrences,
some files hit more than once. A second, narrower contributing factor:
`tools.phrase_scan.NEGATION`'s own `exclusion` token is singular and
word-bounded (`\bexclusion\b`), so it would not match the plural "exclusions"
these headings actually write even where no colon intervenes.

**Recommendations (not applied — planning only, matching the BC1 review's own
"Advice (planning only)" section)**:

1. **ADD** `"uniqueness of the limit"` to later contracts' `forbidden_phrasings`
   (as the BC1 review already advises). Would newly flag exactly 6 locations —
   the O1 row itself and the skeptic's own quoted discussion of it — all of
   which correctly deserve review; none is a bare unscoped affirmative claim.
2. **ADD** `"uniqueness of every infinite-volume ground state"` (as the BC1
   review already advises), **paired with a companion fix**, because on its
   own it would newly flag 11 distinct locations across all six loops that are
   verbatim claim-exclusion-list or "Not admitted/inherited:" restatements,
   not affirmative claims: either (a) change `tools/phrase_scan.py`'s clause
   split so a heading's negation/exclusion cue survives into the list it
   introduces (fixes the "Not admitted:"/"Not inherited:" and "exclusions"
   cases alike), or (b) widen `NEGATION` to also match the plural "exclusions"
   *and* exempt a verbatim "claim exclusions"/"contract exclusions" list the
   same way the `mandatory_sentence_template` is already exempted by name.
3. **ADD** `"unique limit"` for forward compatibility: 0 occurrences anywhere
   in the searched corpus today, so nothing frozen would be newly flagged; it
   substring-overlaps the round list's existing "a unique limit"/"the unique
   limit" (only a bare, determiner-less "unique limit" is not currently
   caught by either).
4. **Do NOT add** bare `"is unique"` or `"uniquely"`: both are used
   round-wide for unrelated mathematical objects — an AM2/route-B fixed point
   unique in its ball, a covering-family member unique through a site, the
   Bratteli–Robinson dynamics-limit theorem's own "can be uniquely extended to
   a one-parameter group of *-automorphisms" quoted verbatim in BA2/BB2
   forward and reverse, and the skeptic's own methodological "each prefix is
   unique" in the BB1 review — and would newly flag 3 and 4 locations
   respectively, none about ground-state/limit uniqueness. If a narrower need
   ever arises, use a compound phrase such as "the ground state is unique" or
   "the limit is unique" instead (0 occurrences of either today).

### 2. `template_and_fields.py`: PASS, 0 defects

**`mandatory_template_span_check` (rule R7) — PASS.** BC1's template (667
whitespace-normalized characters) and BC2's template (1036 characters) each
appear exactly once, as one unbroken span, in that loop's own
`forward/<loop>/report.md` and `advisor/<loop>-gate.json#/accepted`.
Cross-checked against each forward report's own self-reported template check
(`forward/bc1/output/results.json#/checks[20]` id `mandatory_sentence_once`;
`forward/bc2/output/results.json#/checks[52]` id
`mandatory_template_quoted_once_and_phrase_scan_clean`); both report
`passed: true`, agreeing with this script's independent count.

**`gate_fields_comparison` — PASS.** BC1 has 15 `gate_fields_required` keys,
BC2 has 18; for both loops the key set is identical across
contract/gate/review, and every field's value agrees across all three
(15/15 and 18/18). The three calling-task-named fields:

- **BC1.`correlation_shift_resolved`**: contract=gate=review=`False`.
  `plan.json`'s rule ("always false while the free reference `e^{-3}/4` lies
  inside the certified node interval") is satisfied. BC1 restates *both* the
  AV2 node certificate and the AW2 static-mean enclosure, so per `plan.json`'s
  own note it exports the merged `correlation_shift_resolved` field instead
  of a separate `resolved_interaction_shift` field — confirmed: BC1's
  `gate_fields_required` has no `resolved_interaction_shift` key at all.
- **BC1.`finite_box_node_claimed`**: contract=gate=review=`False`, matching
  `plan.json`'s explicit pin ("false in BC1: the admitted AV2 record proves
  no finite-box node").
- **BC2.`node_certificate_restated_for_limit`**: contract=gate=review=`True`,
  matching `plan.json`'s rule ("BC2: AX2 restated for the route-B limit").

**`correlation_shift_resolved`/`resolved_interaction_shift` exclusivity —
PASS.** BC1 has `correlation_shift_resolved` and no
`resolved_interaction_shift` key (restates both AV2 and AW2); BC2 has
`resolved_interaction_shift` and no `correlation_shift_resolved` key
(restates only AX2) — exactly the pairing `plan.json` describes.

**One non-blocking, informational structural note**: the advisor gate exports
`gate_fields` only as a nested dict, while the skeptic review additionally
promotes every one of its members to a flat top-level key as well (e.g.
`skeptic/bc1.json` has both a top-level `correlation_shift_resolved` key and
a nested `gate_fields.correlation_shift_resolved` key, always equal; the
advisor gate has only the nested form). This is a file-format convention
difference between the two document types, not a value disagreement — checked
separately, and found consistent everywhere it applies, for both loops.

### 3. `rate_range_audit.py`: PASS, 0 defects

37 rate-claim clauses (carrying a concrete formula in `N`) found across
`forward/bc1/report.md`, `forward/bc2/report.md`,
`advisor/bc1-gate.json#/accepted`+`/limitations` and
`advisor/bc2-gate.json#/accepted`+`/limitations`. By verdict: 6 two-sided-range
correlation/dynamics-type claims (OK, same clause), 20 ranged density/state-type
claims (OK, same clause), 5 numbered-proof-step or open-row-evaluation clauses
whose range is not in the very same clause but *is* in the governing theorem
statement or obligations-row opening cell a short distance (within 900
characters) before it (recorded separately as `OK_range_established_nearby_
same_proof_or_row`/`OK_two_sided_range_established_nearby`, distinguished from
a true standalone-claim defect), 4 clauses that only describe the
`rate_range_stated` control's own rejected-mutation fixtures, 1 clause that
explicitly disclaims a rate rather than asserting one, 1 constant-glossary
table-row restatement of a formula whose full ranged sentence is elsewhere in
the report, and **0 genuine defects**.

Concretely: the density/widening rate `q^(N-1)` (BC1's finite-box-sign
corollary, BC2's T0–T4 constants) is stated with "for every `N` at least 2"
every time it is a standalone claim — its correct, complete range, since this
rate has no certified upper cutoff. The inherited BB2 item-5 correlation rate
`K5/N` is stated with the certified two-sided range every time it appears as a
headline claim, in both the report and the gate text (e.g.
`forward/bc1/report.md`: *"it gives the rate `K5/N` ... only on the certified
range `5<=N<=14000`"*; `advisor/bc1-gate.json#/accepted`: *"a rate in N (K5/N)
only on 5<=N<=14000"*). The five "established nearby" clauses are ordinary
proof-step continuations of Theorem HNM-BC1-F04 (stated a few lines above with
its own "for every `N` at least 2") and one evaluation sentence inside the
open obligations row N4 (which names the two specific out-of-range `N` values,
2 and 3, a clause earlier) — not fresh, unranged standalone rate assertions
the way the BB2 defect was (a headline claim repeated with **no** range
*anywhere* nearby, in *any* clause of the whole report). Every clause stating
an unqualified `O(1/N)` is, on inspection, one of the `rate_range_stated`
control's own listed rejected-mutation descriptions (e.g. *"an appended
unqualified `O(1/N)` sentence"*, *"a sentence stating the `O(1/N)` rate with
no range appended"*) — not a claim BC1 or BC2 itself makes. This is the
concrete, itemized sign that BC1 and BC2 learned the BB2 lesson their own
contracts' `rate_range_stated` control (BC2) and its inherited form (BC1) were
written to enforce.

## Summary (`summarize.py`, `results.json#/summary`)

`overall_pass = true`. `phrase_audit=True`, `template_and_fields=True`,
`rate_range_audit=True`. Every one of the three scripts' checks completed
with zero genuine defects. This package's substantive contribution is not a
blocking defect (there is none to find in BC1/BC2's already-gated,
already-reviewed text) but the vocabulary-gap audit's classified,
computed-not-asserted findings and its four "do not apply" recommendations
above, plus the independently found heading-colon-list severance mechanism
and the confirmation that BC1/BC2's rate sentences carry their `N`-ranges
correctly by rate type.

## Note on the occult reading ledger

No occult or mystical source was read to produce this package (the calling
task's own instruction: append to
`research/round33/experts/occult/reading-ledger.md` only if one was; none
was, so it is untouched). This package reads only the contracts, the BC1/BC2
forward packets (`report.md` and `output/results.json`), the BC1/BC2 gates
and skeptical reviews, `plan.json`, and — for the vocabulary-gap sweep only —
the equivalent gate/review/report text of ba1, ba2, bb1 and bb2, exactly as
the calling task names or permits.

**This is a live, concurrently-advancing repository.** `git status` at the end
of this work confirms every file this session touched is under
`research/round33/experts/jung/assistant-3/`.
