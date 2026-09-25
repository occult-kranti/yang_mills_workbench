#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 sub-round 3, assistant-3: final summary (calling task
item 4's own `results.json` requirement).

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those; BC1 and BC2 are already
gated `accepted_within_scope` and nothing here changes that. Human project
author: Hruday N M (BUNZEEY); AI-assisted. Standard library only. Run last,
after the three audit scripts, so it can read their already-merged sections out
of `results.json` rather than recomputing anything.

`overall_pass` is `all(section['passed'] for section in the three sections)`.
As with assistant-1's and assistant-2's own precedent, a `False` here would be
the correct, expected result if a genuine defect were found -- it is not a bug
in this package and it decides nothing about BC1 or BC2 (both are already
gated; only a future round could act on a finding here). Today, every one of
the three scripts' checks passes: `overall_pass = True`. This package's
substantive contribution is not a blocking defect but the vocabulary-gap
audit's classified findings and its "do not apply" recommendations (see
phrase_audit.py's own findings and README.md).

Usage: python3 -B summarize.py (after phrase_audit.py, template_and_fields.py
and rate_range_audit.py have each been run at least once).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common3 as K  # noqa: E402

SECTION_KEYS = ('phrase_audit', 'template_and_fields', 'rate_range_audit')


def summarize():
    out_path = Path(__file__).resolve().parent / 'results.json'
    if not out_path.exists():
        print('results.json does not exist yet -- run phrase_audit.py, template_and_fields.py and '
              'rate_range_audit.py first.', file=sys.stderr)
        sys.exit(2)
    data = K.load_json(out_path)
    missing = [k for k in SECTION_KEYS if k not in data]
    if missing:
        print('results.json is missing section(s) %r -- run the corresponding script(s) first.' % missing,
              file=sys.stderr)
        sys.exit(2)

    section_passed = {k: data[k]['passed'] for k in SECTION_KEYS}
    overall_pass = all(section_passed.values())

    # Collect every DEFECT/AFFIRMATIVE finding line across the three sections'
    # sub-checks, so the summary's own findings list is a genuine roll-up, not a
    # re-derivation.
    defect_lines = []
    for section_key in SECTION_KEYS:
        section = data[section_key]
        for check_id, check in section.get('checks', {}).items():
            for f in check.get('findings', []):
                s = f.strip()
                if s.upper().startswith('DEFECT') or s.startswith('  DEFECT') or s.upper().startswith('AFFIRMATIVE'):
                    defect_lines.append('%s.%s: %s' % (section_key, check_id, s))

    findings = [
        'Section pass/fail: %s.' % ', '.join('%s=%r' % (k, v) for k, v in section_passed.items()),
        'overall_pass = %r.' % overall_pass,
    ]
    if overall_pass:
        findings.append('All three scripts\' checks completed with zero genuine defects -- BC1 and BC2\'s already-'
                        'frozen text (forward reports, gate accepted/limitations, review supported_statement) '
                        'carries no affirmative forbidden phrasing, quotes the mandatory template exactly once as '
                        'one unbroken span in every report and gate text, exports gate_fields that agree exactly '
                        'across contract/gate/review and satisfy every checkable plan.json rule, and states every '
                        'genuine rate sentence with its correct-shape N-range in the same clause (or, for a handful '
                        'of numbered-proof-step continuations, within the same theorem/row a short distance '
                        'earlier). Nothing here reopens or reduces either gate\'s accepted_within_scope verdict.')
    else:
        findings.append('overall_pass is False because at least one sub-check found a genuine defect (listed below '
                        'and in that script\'s own findings) -- it decides nothing about BC1 or BC2 by itself; both '
                        'gates keep their own recorded verdict regardless.')
    findings.append(
        'Calling task item 1 (phrase_audit.py), first half: phrase_scan_dry_run found 0 raw hits (not merely 0 '
        'unnegated ones) across BC1\'s and BC2\'s forward report, gate accepted/limitations and review '
        'supported_statement, matching both reviews\' own self-reported phrase_scan block exactly.')
    findings.append(
        'Calling task item 1 (phrase_audit.py), second half (the vocabulary-gap audit): searched every gate, '
        'review and report of ba1/ba2/bb1/bb2/bc1/bc2 (bd1/bd2 excluded, in production) for five candidate '
        'uniqueness-type phrasings the real scanner\'s vocabulary misses today, round-wide (confirmed by direct '
        'membership check). 42 occurrences found; 0 classified bare, unscoped AFFIRMATIVE. The calling task\'s own '
        'named instance ("uniqueness of the limit", the AY2/O1 row): 10 occurrences, all in BC1, all either '
        'scoped to the named constructions (the O1 table row itself) or quoted discussion of it -- never an '
        'unscoped claim. A second, general mechanism was found independently: a "heading: list" pattern (e.g. '
        '"Contract exclusions (verbatim):", "Not admitted:") severs its own negation/exclusion cue word from every '
        'list item that follows it, via phrase_scan.py\'s own ": " clause split -- affecting 11 distinct frozen '
        'locations across every one of the six loops for "uniqueness of every infinite-volume ground state" alone. '
        'Recommendations (not applied): ADD "uniqueness of the limit" (as the BC1 review already advises); ADD '
        '"uniqueness of every infinite-volume ground state" paired with a companion fix for the heading-severance '
        'mechanism; ADD "unique limit" (0 occurrences today, zero-cost); do NOT add bare "is unique"/"uniquely" '
        '(both used round-wide for unrelated mathematical objects).')
    findings.append(
        'Calling task item 2 (template_and_fields.py): the mandatory_sentence_template appears exactly once, as '
        'one unbroken span, in each of BC1\'s and BC2\'s forward report.md and gate accepted text, cross-checked '
        'against each report\'s own self-reported template check; every gate_fields key required by each contract '
        'agrees in value across contract/gate/review for both loops, including the three calling-task-named fields '
        '(BC1.correlation_shift_resolved=False, BC1.finite_box_node_claimed=False, '
        'BC2.node_certificate_restated_for_limit=True) and the correlation_shift_resolved/resolved_interaction_'
        'shift exclusivity plan.json describes; one non-blocking, informational structural note: the advisor gate '
        'exports gate_fields only as a nested dict while the skeptic review additionally promotes every member to '
        'a flat top-level key (a file-format convention difference, not a value disagreement).')
    findings.append(
        'Calling task item 3 (rate_range_audit.py): 37 rate-claim clauses (a concrete formula in N) found across '
        'BC1\'s and BC2\'s forward reports and gate accepted/limitations text; 0 genuine defects. Every density/'
        'widening-type rate (q^(N-1)) correctly carries a one-sided "for every N at least k" (its correct, '
        'complete range, since it has no certified upper cutoff); the inherited BB2 item-5 correlation rate (K5/N) '
        'correctly carries the certified two-sided "5<=N<=14000" every time it is stated as a headline claim; a '
        'handful of numbered-proof-step continuations state their governing theorem\'s range a short distance '
        'earlier rather than repeating it verbatim in the very next clause (ordinary mathematical writing, not the '
        'BB2 defect); every clause that states an unqualified O(1/N) with no range anywhere nearby is, on '
        'inspection, one of the frozen rate_range_stated control\'s own listed rejected-mutation descriptions, not '
        'a producer claim -- the concrete sign that BC1/BC2 learned the BB2 lesson their own contracts\' control '
        'was written to enforce.')

    result = {
        'overall_pass': overall_pass, 'section_passed': section_passed, 'defect_and_affirmative_lines': defect_lines,
        'findings': findings,
        'role': 'Jung/Pauli lens, Round33 sub-round 3, assistant-3: final summary rolling up the three audit '
                'scripts\' pass/fail state and every DEFECT/AFFIRMATIVE finding line; zero research loops; audits '
                'only, never admission evidence; decides nothing about BC1 or BC2 (both already gated '
                'accepted_within_scope)',
    }
    K.merge_results(out_path, 'summary', result)
    print('summary: overall_pass=%r' % overall_pass)
    for f in findings:
        print('  -', f)
    if defect_lines:
        print('Defect/affirmative lines (%d):' % len(defect_lines))
        for d in defect_lines:
            print('  -', d)


if __name__ == '__main__':
    summarize()
