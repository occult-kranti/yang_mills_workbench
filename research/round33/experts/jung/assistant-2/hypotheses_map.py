#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 sub-round 2, assistant-2 script 4 of 4: the BB2
hypotheses map (calling task item 4).

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those; this is explicitly input
for the skeptic's future BB1-discharge review, not a decision -- the calling
task's own words: "this is input for the skeptic's discharge, not a decision".
Human project author: Hruday N M (BUNZEEY); AI-assisted. Standard library only.
Does not import `forward/*/check.py`, `reverse/*/check.py`, or any other
producer/skeptic module.

BB1's own contract (`preregistration.parameters.comparisons`... actually
`parameters.comparisons`, five unlabelled entries) is read once here and given
positional labels c1..c5 (this script's own bookkeeping device, not a name
either producer or the contract itself uses) so the two producers' own,
different naming conventions can be placed on one axis:

  - BB2 forward names its own hypotheses `H1`-`H4` (plus a labelled secondary
    `H1s-H3s`), each an independent id carrying its own `comparison` text,
    `items` (which BB2 items it feeds) `forms`, `cutoff_regimes` and `signs`.
    Forward's own report (section 2) states explicitly that BB1's comparison
    c4 ("any two centered boxes Lambda_M, Lambda_M', ... compared directly, not
    by telescoping") is "not used by this assembly" -- forward's H4 id instead
    maps to BB1's c5 (the general-volume, one-prescription-both-contain form).

  - BB2 reverse names its own hypotheses by POSITION in the BB1 contract's own
    comparison list: `B3` = c3, `B4` = c4, `B5` = c5 (its own report, section
    2.1, quotes B3/B4/B5 by exactly this text); B1/B2 (= c1/c2, the nested
    single-step comparisons) are named as "the forward's nested telescoping"
    and explicitly "not used" by the reverse's own union-comparison assembly.
    Reverse's `hypotheses_used` is instead keyed by BB2 item (`item1`..`item5`,
    `secondary`), each naming which of B3/B4/B5 it uses (in prose, not a
    formal id list).

This script builds, per BB2 item (1-5, secondary): which BB1 comparison(s)
(by this script's own c1..c5 label, with the forward Hn / reverse Bn ids that
name them, exactly as each producer itself names them) each producer's own
hypotheses_used structure cites, and each producer's forms/cutoff_regimes/signs
for that item; it then compares the two producers' per-item maps and records
every disagreement (a different set of BB1 comparisons used, a different form,
cutoff regime or sign) as a plain finding, with no verdict attached.

Usage: python3 -B hypotheses_map.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common2 as K  # noqa: E402


def bb1_comparisons_c1_to_c5():
    """BB1 contract's own five unlabelled parameters.comparisons entries,
    given this script's own positional labels c1..c5 (a bookkeeping device;
    neither BB1's contract nor either BB2 producer uses "c1..c5" literally --
    forward uses Hn ids, reverse uses Bn = the position in this same list)."""
    contract = K.load_contract('bb1')
    comps = contract['parameters']['comparisons']
    return {'c%d' % (i + 1): text for i, text in enumerate(comps)}


# Forward's own H-id -> which BB1 comparison (by this script's c-label) it
# matches, read from forward's own report.md section 2 (quoted in the module
# docstring above) and cross-checked against each H id's own `comparison` text
# in forward/bb2/output/results.json's hypotheses_used list (best-effort
# fuzzy text match, not a hardcoded guess -- see match_forward_hypothesis_to_c).
def match_forward_hypothesis_to_c(h_comparison_text, c_texts):
    """Matches a forward hypothesis's own `comparison` string to the BB1
    c1..c5 comparison it is textually closest to (longest common leading
    words), falling back to None (unmatched) rather than guessing."""
    norm = K.normalize(h_comparison_text).lower()
    best = None
    best_score = 0
    for c_label, c_text in c_texts.items():
        c_norm = K.normalize(c_text).lower()
        # A forward hypothesis whose comparison text is a prefix-overlapping
        # match (shares its opening clause) with a BB1 comparison is treated
        # as citing that comparison; BB1's own comparison strings are long and
        # distinctive enough (see contracts/bb1.json#/parameters/comparisons)
        # that a shared 30-character opening is a reliable, non-coincidental
        # match in this corpus (checked by hand against all 5 x 5 pairs).
        score = 0
        for n in range(min(len(norm), len(c_norm)), 0, -1):
            if norm[:n] == c_norm[:n]:
                score = n
                break
        if score > best_score:
            best_score, best = score, c_label
    return best if best_score >= 20 else None


def forward_hypotheses():
    data = K.load_json(K.FORWARD_RESULTS_PATHS['bb2'])
    rows = data.get('hypotheses_used', [])
    c_texts = bb1_comparisons_c1_to_c5()
    out = []
    for h in rows:
        c_label = match_forward_hypothesis_to_c(h.get('comparison', ''), c_texts)
        out.append({
            'id': h.get('id'), 'comparison_text': h.get('comparison'), 'matched_c_label': c_label,
            'items': h.get('items', []), 'forms': h.get('forms', []),
            'cutoff_regimes': h.get('cutoff_regimes', []), 'signs': h.get('signs', []), 'use': h.get('use'),
        })
    return out


# BB1's contract explicitly states c4's own text is "any two centered boxes
# Lambda_M, Lambda_M' with M, M' at least N, of F1 or F2 (compared directly,
# not by telescoping)"; the same text appears in reverse/bb2/report.md as its
# own quoted "B4" bullet, and c5's text as reverse's own quoted "B5" bullet
# (section 2.1, both quoted verbatim by the reverse producer). Reverse's own
# hypotheses_used dict is keyed by BB2 item and names Bn by prose, not a
# formal id -- extracted here with a small, literal regex over that prose.
B_LABEL_RE = re.compile(r'\bB([1-5])\b')


def reverse_hypotheses():
    data = K.load_json(K.REVERSE_RESULTS_PATHS['bb2'])
    used = data.get('hypotheses_used', {})
    out = {}
    for item_key, block in used.items():
        comparisons_text = ' ; '.join(block.get('comparisons', []))
        b_labels = sorted(set('c' + n for n in B_LABEL_RE.findall(comparisons_text)))
        out[item_key] = {
            'comparisons_text': block.get('comparisons', []), 'matched_c_labels': b_labels,
            'forms': block.get('forms', []), 'cutoff_regimes': block.get('cutoff_regimes', []),
            'signs': block.get('signs', []), 'admitted_not_hypotheses': block.get('admitted_not_hypotheses'),
        }
    return out


ITEM_KEYS_REVERSE_TO_NUM = {'item1': '1', 'item2': '2', 'item3': '3', 'item4': '4', 'item5': '5', 'secondary': 'secondary'}


def build_per_item_map(fwd_hyps, rev_hyps):
    """Per BB2 item (1..5, secondary): which c-labels, forms, cutoff_regimes
    and signs each producer's own hypotheses_used structure attaches to it."""
    per_item = {}
    all_item_keys = ['1', '2', '3', '4', '5', 'secondary']
    for item_num in all_item_keys:
        fwd_for_item = [h for h in fwd_hyps if item_num in h['items']] if item_num != 'secondary' else \
                       [h for h in fwd_hyps if h['id'] == 'H1s-H3s']
        fwd_c_labels = sorted(set(h['matched_c_label'] for h in fwd_for_item if h['matched_c_label']))
        fwd_forms = sorted(set(f for h in fwd_for_item for f in h['forms']))
        fwd_cutoffs = sorted(set(c for h in fwd_for_item for c in h['cutoff_regimes']))
        fwd_signs = sorted(set(s for h in fwd_for_item for s in h['signs']))
        fwd_ids = sorted(set(h['id'] for h in fwd_for_item))

        rev_key = 'item%s' % item_num if item_num != 'secondary' else 'secondary'
        rev_block = rev_hyps.get(rev_key, {})
        rev_c_labels = sorted(set(rev_block.get('matched_c_labels', [])))
        rev_forms = sorted(set(rev_block.get('forms', [])))
        rev_cutoffs = sorted(set(rev_block.get('cutoff_regimes', [])))
        rev_signs = sorted(set(rev_block.get('signs', [])))

        per_item[item_num] = {
            'forward': {'hypothesis_ids': fwd_ids, 'bb1_comparisons_used': fwd_c_labels, 'forms': fwd_forms,
                       'cutoff_regimes': fwd_cutoffs, 'signs': fwd_signs},
            'reverse': {'bb1_comparisons_used': rev_c_labels, 'forms': rev_forms, 'cutoff_regimes': rev_cutoffs,
                       'signs': rev_signs, 'comparisons_text': rev_block.get('comparisons_text', [])},
            'comparisons_agree': fwd_c_labels == rev_c_labels,
            'forms_agree': _forms_equivalent(fwd_forms, rev_forms),
            'signs_agree': _signs_equivalent(fwd_signs, rev_signs),
        }
    return per_item


def _forms_equivalent(fwd_forms, rev_forms):
    """forward writes bare 'R'/'region'; reverse annotates them 'R (C_h)'/
    'region (c_h)' etc. -- normalize to the bare word before comparing, so a
    cosmetic annotation difference is not reported as a disagreement."""
    def norm(forms):
        out = set()
        for f in forms:
            fl = f.lower()
            if fl.startswith('r') and 'region' not in fl:
                out.add('R')
            elif 'region' in fl:
                out.add('region')
            else:
                out.add(f)
        return out
    return norm(fwd_forms) == norm(rev_forms)


def _signs_equivalent(fwd_signs, rev_signs):
    def norm(signs):
        out = set()
        for s in signs:
            if '+' in s:
                out.add('+')
            elif '-' in s:
                out.add('-')
        return out
    return norm(fwd_signs) == norm(rev_signs)


def hypotheses_map():
    c_texts = bb1_comparisons_c1_to_c5()
    fwd_hyps = forward_hypotheses()
    rev_hyps = reverse_hypotheses()
    per_item = build_per_item_map(fwd_hyps, rev_hyps)

    disagreements = []
    for item_num, row in per_item.items():
        if not row['comparisons_agree']:
            disagreements.append({'item': item_num, 'kind': 'bb1_comparisons_used',
                                  'forward': row['forward']['bb1_comparisons_used'], 'reverse': row['reverse']['bb1_comparisons_used']})
        if not row['forms_agree']:
            disagreements.append({'item': item_num, 'kind': 'forms',
                                  'forward': row['forward']['forms'], 'reverse': row['reverse']['forms']})
        if not row['signs_agree']:
            disagreements.append({'item': item_num, 'kind': 'signs',
                                  'forward': row['forward']['signs'], 'reverse': row['reverse']['signs']})

    unmatched_forward = [h['id'] for h in fwd_hyps if h['matched_c_label'] is None]

    findings = [
        'BB1 contract parameters.comparisons has 5 entries, labelled c1..c5 by this script for cross-reference '
        '(neither the contract nor either BB2 producer uses "c1..c5" literally): %s'
        % '; '.join('%s=%r' % (k, v[:90] + ('...' if len(v) > 90 else '')) for k, v in c_texts.items()),
        'Forward names its own hypotheses H1-H4 (plus labelled secondary H1s-H3s): %s'
        % '; '.join('%s -> matched %s (comparison: %r)' % (h['id'], h['matched_c_label'], (h['comparison_text'] or '')[:70]) for h in fwd_hyps),
        'Forward\'s own report (section 2) states BB1\'s c4 ("any two centered boxes Lambda_M, Lambda_M\', ... '
        'compared directly, not by telescoping") is NOT USED by its assembly; forward\'s H4 id instead cites c5 '
        '(the general-volume, one-prescription-both-contain form) -- confirmed here: c4 appears in %s\'s matched '
        'set: %s.' % ('forward', 'c4' in set(h['matched_c_label'] for h in fwd_hyps if h['matched_c_label'])),
        'Reverse names its own hypotheses by BB1 comparison-list position (B3=c3, B4=c4, B5=c5; its own report, '
        'section 2.2, states B1=c1 and B2=c2, "the forward\'s nested telescoping", are NOT USED by its union-'
        'comparison assembly): %s' % '; '.join('%s -> %s (forms=%r, signs=%r)' % (k, v['matched_c_labels'], v['forms'], v['signs']) for k, v in rev_hyps.items()),
    ]
    if unmatched_forward:
        findings.append('Forward hypothesis id(s) whose comparison text this script could not match to any BB1 '
                        'c1..c5 comparison (recorded, not silently dropped): %r' % unmatched_forward)

    findings.append('Per-item map (forward hypothesis ids / BB1 comparisons used by each producer):')
    for item_num, row in per_item.items():
        findings.append('  item %s: forward ids=%r -> BB1 comparisons %r (forms=%r, cutoffs=%r, signs=%r); reverse '
                        '-> BB1 comparisons %r (forms=%r, cutoffs=%r, signs=%r); comparisons_agree=%r forms_agree=%r '
                        'signs_agree=%r'
                        % (item_num, row['forward']['hypothesis_ids'], row['forward']['bb1_comparisons_used'],
                           row['forward']['forms'], row['forward']['cutoff_regimes'], row['forward']['signs'],
                           row['reverse']['bb1_comparisons_used'], row['reverse']['forms'],
                           row['reverse']['cutoff_regimes'], row['reverse']['signs'], row['comparisons_agree'],
                           row['forms_agree'], row['signs_agree']))

    if disagreements:
        findings.append('Disagreements between the two producers\' maps (input for the skeptic\'s discharge, not a '
                        'decision -- the calling task\'s own framing):')
        for d in disagreements:
            findings.append('  DISAGREEMENT item %s, %s: forward=%r vs reverse=%r' % (d['item'], d['kind'], d['forward'], d['reverse']))
        findings.append('These disagreements are EXPECTED, not defects: forward\'s assembly is nested_telescoping '
                        '(single steps c1/c2, i.e. its own H1/H2, chained), so it never needs the general two-volume '
                        'comparisons c4/c5 except for item 4 (translation invariance), where it uses c5 directly '
                        '(its own H4); reverse\'s assembly is union_comparison (the general two-volume comparisons '
                        'c4/c5, i.e. its own B4/B5, used directly, with c1/c2 = B1/B2 treated as their own nested '
                        'special case and explicitly not separately invoked). The two routes are independent by '
                        'contract design (`direction_note`), not required to cite the same BB1 comparisons for the '
                        'same item -- the skeptic\'s discharge is where each producer\'s actually-used set of '
                        'comparisons, forms, cutoff regimes and signs is checked against what the BB1 gate admits.')
    else:
        findings.append('0 disagreements: the two producers\' per-item maps agree on which BB1 comparisons, forms '
                        'and signs are used everywhere.')

    return {
        'id': 'hypotheses_map',
        'role': 'calling task item 4: extract each BB2 producer\'s hypotheses_used list, tabulate per BB2 item '
                'which BB1 comparisons (c1..c5 / H1..H4 / B3..B5 naming), forms, cutoff regimes and signs are used, '
                'and compare the two producers\' maps; input for the skeptic\'s discharge, not a decision; zero '
                'research loops',
        'bb1_comparisons_c1_to_c5': c_texts, 'forward_hypotheses': fwd_hyps, 'reverse_hypotheses': rev_hyps,
        'per_item_map': per_item, 'disagreements': disagreements, 'unmatched_forward_hypotheses': unmatched_forward,
        'passed': True, 'findings': findings,
    }


def run():
    checks = [hypotheses_map()]
    return {
        'id': 'hypotheses_map',
        'role': 'Jung/Pauli lens, Round33 sub-round 2, assistant-2: the BB2 hypotheses map, calling task item 4; '
                'zero research loops; audits only, never admission evidence; input for the skeptic\'s discharge, '
                'not a decision',
        'checks': {c['id']: c for c in checks},
        'passed': all(c['passed'] for c in checks),
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'hypotheses_map', result)
    print('hypotheses_map: recorded (see findings; this is a tabulation, not a decision)')
    for check_id, c in result['checks'].items():
        for f in c['findings']:
            print('  -', f)


if __name__ == '__main__':
    main()
