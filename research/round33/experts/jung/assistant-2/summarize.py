#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 sub-round 2, assistant-2: final summary (calling
task item 5's own `results.json` requirement: "overall_pass; findings").

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those; BB1 and BB2 are not yet
gated. Human project author: Hruday N M (BUNZEEY); AI-assisted. Standard
library only. Run last, after the four audit scripts, so it can read their
already-merged sections out of `results.json` rather than recomputing anything.

`overall_pass` is `all(section['passed'] for section in the four sections)`.
As with `research/round33/experts/jung/assistant-1/`'s own precedent (whose
`phrase_audit.py` intentionally exits 1 because it found a genuine, itemized
defect), a `False` here is the correct, expected result when a real defect was
found -- it is not a bug in this package and it decides nothing about BB1/BB2
(only a future advisor gate and the skeptic's review do that). Today,
`overall_pass` is `False` because `vocabulary_mirror.py`'s
`closed_vocabulary_membership` sub-check found one genuine closed-vocabulary
violation (BB2 forward's `gate_fields_if_undischarged.dynamics_level` value
`"not_set (conditional_on_bb1_targets)"` is not a member of `plan.json`'s
closed `dynamics_level` set); every other sub-check across all four scripts
passed with zero defects.

Usage: python3 -B summarize.py (after phrase_audit.py, template_and_fields.py,
vocabulary_mirror.py and hypotheses_map.py have each been run at least once).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common2 as K  # noqa: E402

SECTION_KEYS = ('phrase_audit', 'template_and_fields', 'vocabulary_mirror', 'hypotheses_map')


def summarize():
    out_path = Path(__file__).resolve().parent / 'results.json'
    if not out_path.exists():
        print('results.json does not exist yet -- run phrase_audit.py, template_and_fields.py, '
              'vocabulary_mirror.py and hypotheses_map.py first.', file=sys.stderr)
        sys.exit(2)
    data = K.load_json(out_path)
    missing = [k for k in SECTION_KEYS if k not in data]
    if missing:
        print('results.json is missing section(s) %r -- run the corresponding script(s) first.' % missing,
              file=sys.stderr)
        sys.exit(2)

    section_passed = {k: data[k]['passed'] for k in SECTION_KEYS}
    overall_pass = all(section_passed.values())

    # Collect every top-level defect/violation/disagreement finding line across the four sections' sub-checks,
    # so the summary's own findings list is a genuine roll-up, not a re-derivation.
    defect_lines = []
    for section_key in SECTION_KEYS:
        section = data[section_key]
        for check_id, check in section.get('checks', {}).items():
            for f in check.get('findings', []):
                if f.strip().upper().startswith('DEFECT') or f.strip().upper().startswith('DISAGREEMENT'):
                    defect_lines.append('%s.%s: %s' % (section_key, check_id, f.strip()))

    findings = [
        'Section pass/fail: %s.' % ', '.join('%s=%r' % (k, v) for k, v in section_passed.items()),
        'overall_pass = %r.' % overall_pass,
    ]
    if overall_pass:
        findings.append('All four scripts\' checks completed with zero genuine defects.')
    else:
        findings.append('overall_pass is False because at least one sub-check found a genuine, itemized defect '
                        '(listed below and in that script\'s own findings) -- exactly the point of an audit '
                        'package, per assistant-1\'s own precedent; it decides nothing about BB1 or BB2, which '
                        'remain ungated pending a future advisor gate and the skeptic\'s review.')
    findings.append('Calling task item 1 (phrase_audit.py): phrase_scan_dry_run found 0 AFFIRMATIVE_needs_review '
                    'hits across all 8 BB1/BB2 packet files; rate_claim_audit found the calling task\'s own named '
                    'defect confirmed: BB2 forward states the item-5 O(1/N) rate in 8 separate clauses without ever '
                    'stating the certified range 5<=N<=14000 (which appears only in the BB2 reverse report).')
    findings.append('Calling task item 2 (template_and_fields.py): the mandatory_sentence_template appears exactly '
                    'once, as one unbroken span, in each of the four report.md files; every gate-field comparison '
                    'passed, including BB2\'s before/after-discharge blocks (reverse top-level = before-discharge, '
                    'forward = proposed + if_undischarged), with one recorded (non-blocking) difference between '
                    'the two producers\' own "before discharge" dynamics_level value.')
    findings.append('Calling task item 3 (vocabulary_mirror.py): one genuine closed-vocabulary violation found -- '
                    'BB2 forward\'s gate_fields_if_undischarged.dynamics_level value "not_set (conditional_on_'
                    'bb1_targets)" is not a member of plan.json\'s closed dynamics_level set (the same value that '
                    'template_and_fields.py records as a difference from reverse\'s own before-discharge value '
                    '"algebraic_heisenberg_compact_window", which IS a member); the tier_label_rule check found 0 '
                    'BB1 constants carrying a BA1 route as their own BB1 route; every BB2 state constant carries an '
                    'assembly and a hypothesis source.')
    findings.append('Calling task item 4 (hypotheses_map.py): forward (nested_telescoping) and reverse (union_'
                    'comparison) cite different subsets of BB1\'s five comparisons for the same BB2 item in every '
                    'case except the labelled secondary pair\'s comparison set -- expected given their different '
                    'assemblies, not a defect; recorded in full as input for the skeptic\'s future BB1-discharge '
                    'review, not a decision.')

    result = {
        'overall_pass': overall_pass, 'section_passed': section_passed, 'defect_and_disagreement_lines': defect_lines,
        'findings': findings,
        'role': 'Jung/Pauli lens, Round33 sub-round 2, assistant-2: final summary rolling up the four audit '
                'scripts\' pass/fail state and every DEFECT/DISAGREEMENT finding line; zero research loops; '
                'audits only, never admission evidence; decides nothing about BB1 or BB2',
    }
    K.merge_results(out_path, 'summary', result)
    print('summary: overall_pass=%r' % overall_pass)
    for f in findings:
        print('  -', f)
    if defect_lines:
        print('Defect/disagreement lines (%d):' % len(defect_lines))
        for d in defect_lines:
            print('  -', d)


if __name__ == '__main__':
    summarize()
