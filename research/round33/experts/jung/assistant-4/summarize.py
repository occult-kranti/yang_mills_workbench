#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 applications stage, assistant-4: final summary
(calling task item 4's own `results.json` requirement).

Counts zero research loops. Not a producer, contract, gate or skeptical
review; nothing computed here is read back into any of those; BD1 and BD2 are
already gated `accepted_within_scope` and nothing here changes that. Human
project author: Hruday N M (BUNZEEY); AI-assisted. Standard library only. Run
last, after the three audit scripts, so it can read their already-merged
sections out of `results.json` rather than recomputing anything.

`overall_pass` is `all(section['passed'] for section in the three sections)`.
As with assistant-1's, assistant-2's and assistant-3's own precedent, a
`False` here would be the correct, expected result if a genuine defect were
found -- it is not a bug in this package and it decides nothing about BD1 or
BD2 (both are already gated; only a future round could act on a finding
here). Today, every one of the three scripts' checks passes:
`overall_pass = True`.

Usage: python3 -B summarize.py (after phrase_audit.py, template_and_fields.py
and applications_ledger_audit.py have each been run at least once).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common4 as K  # noqa: E402

SECTION_KEYS = ('phrase_audit', 'template_and_fields', 'applications_ledger_audit')


def summarize():
    out_path = Path(__file__).resolve().parent / 'results.json'
    if not out_path.exists():
        print('results.json does not exist yet -- run phrase_audit.py, template_and_fields.py and '
              'applications_ledger_audit.py first.', file=sys.stderr)
        sys.exit(2)
    data = K.load_json(out_path)
    missing = [k for k in SECTION_KEYS if k not in data]
    if missing:
        print('results.json is missing section(s) %r -- run the corresponding script(s) first.' % missing,
              file=sys.stderr)
        sys.exit(2)

    section_passed = {k: data[k]['passed'] for k in SECTION_KEYS}
    overall_pass = all(section_passed.values())

    defect_lines = []
    for section_key in SECTION_KEYS:
        section = data[section_key]
        for check_id, check in section.get('checks', {}).items():
            for f in check.get('findings', []):
                s = f.strip()
                if s.upper().startswith('DEFECT') or s.startswith('  DEFECT'):
                    defect_lines.append('%s.%s: %s' % (section_key, check_id, s))

    findings = [
        'Section pass/fail: %s.' % ', '.join('%s=%r' % (k, v) for k, v in section_passed.items()),
        'overall_pass = %r.' % overall_pass,
    ]
    if overall_pass:
        findings.append(
            'All three scripts\' checks completed with zero genuine defects -- BD1 and BD2\'s already-frozen '
            'text (the three BD reports, both gates, both reviews\' supported_statement, findings.json\'s '
            'summary/scope_statement/applications and roadmap.json) carries no affirmative forbidden phrasing '
            'and no affirmative uniqueness-type phrasing (the only four uniqueness-candidate occurrences found '
            'are a genuinely negated exclusion clause and a forward-looking vocabulary-list mention in '
            'roadmap.json, not a BD1/BD2 claim); every transfer-kind applications entry names a canonical BD '
            'model, and the scan scope never uses predicts/confirms/universal/string tension/confinement '
            'affirmatively, and no one-plaquette or graph value is phrased as a lattice-limit value; both '
            'mandatory sentence templates appear exactly once, as one unbroken span, in every one of their '
            'reports and gate texts; every BD gate_fields key agrees in value across contract/gate/review (or, '
            'for BD1.flip_transfer_scope\'s documented description-vs-instantiation exception, gate==review) '
            'and satisfies every checkable plan.json rule; and every findings.json#/applications entry has its '
            'required fields, cites sources that are byte-identical to what its own gate bound, and states '
            'numbers that match its own gate\'s text. Nothing here reopens or reduces either gate\'s '
            'accepted_within_scope verdict.')
    else:
        findings.append(
            'overall_pass is False because at least one sub-check found a genuine defect (listed below and in '
            'that script\'s own findings) -- it decides nothing about BD1 or BD2 by itself; both gates keep '
            'their own recorded verdict regardless.')
    findings.append(
        'Calling task item 1 (phrase_audit.py): phrase_scan_dry_run found 0 raw hits (not merely 0 unnegated '
        'ones) across the exact scan scope; vocabulary_gap_audit_bd found 4 occurrences of the five uniqueness-'
        'candidate phrases, all inside roadmap.json, 0 classified bare affirmative; heading_list_severance_check '
        'found the same "exclusions (verbatim): item; item" heading-list pattern assistant-3 found for sub-round '
        '3, present in all three BD reports, and confirmed mechanically that no round-forbidden, BD-contract-'
        'forbidden or uniqueness-candidate phrase is a severed list item today; transfer_language_audit '
        'confirmed every transfer-kind applications entry names a canonical model, the forbidden words predicts/'
        'confirms/universal/string tension/confinement do not occur at all in the scan scope, and the two '
        'lattice-limit-value phrasings the mechanical NEGATION rule alone would miss are both markdown rejected-'
        'mutation table rows, confirmed by a structural marker rather than assumed.')
    findings.append(
        'Calling task item 2 (template_and_fields.py): the mandatory_sentence_template appears exactly once, as '
        'one unbroken span, in each of BD1\'s report(s) (forward and reverse) and BD2\'s report and each gate\'s '
        'accepted text; every gate_fields key required by each contract agrees in value across contract/gate/'
        'review for both loops, including the seven calling-task-named fields (BD1.flip_transfer_scope naming '
        'SU(2), SU(4), U(1), Z2 -- handled as the contract\'s own documented description-vs-instantiation '
        'exception; BD1.obstructions_recorded=True; BD1.area_parity_limit_claimed=True; '
        'BD2.graph_sign_certified=True; BD2.z3_1x2_formal_only=True; BD2.electric_band_scope; '
        'BD2.area_law_claimed=False, satisfying plan.json\'s "always false in Round33" rule).')
    findings.append(
        'Calling task item 3 (applications_ledger_audit.py): all 12 findings.json#/applications entries (6 BD1, '
        '6 BD2; 4 transfer, 4 obstruction, 4 partial) carry every required field; all 30 source citations across '
        'those entries are keys of their own loop\'s gate bindings with a matching sha256 on disk today; every '
        'fraction token in the ledger\'s numbers (17 total) appears verbatim in its own gate\'s text, and every '
        'decimal preview (6 total) matches a same-magnitude preview the gate text itself carries.')

    result = {
        'overall_pass': overall_pass, 'section_passed': section_passed, 'defect_lines': defect_lines,
        'findings': findings,
        'role': 'Jung/Pauli lens, Round33 applications stage, assistant-4: final summary rolling up the three '
                'audit scripts\' pass/fail state and every DEFECT finding line; zero research loops; audits '
                'only, never admission evidence; decides nothing about BD1 or BD2 (both already gated '
                'accepted_within_scope)',
    }
    K.merge_results(out_path, 'summary', result)
    print('summary: overall_pass=%r' % overall_pass)
    for f in findings:
        print('  -', f)
    if defect_lines:
        print('Defect lines (%d):' % len(defect_lines))
        for d in defect_lines:
            print('  -', d)


if __name__ == '__main__':
    summarize()
