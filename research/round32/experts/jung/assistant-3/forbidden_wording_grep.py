#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 3, assistant-3 script 2 of 3: forbidden-
wording grep and scratch-disclosure check for AX1 (`update-2.md` section 5,
item 3, extended per the calling task to the gate and the final skeptic review
as well as the two reports and both results.json files).

Counts zero research loops; not a producer, contract, gate or skeptical review,
and nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted.

**What this does.** Greps six required files for the two forbidden strings
"weak coupling" and "continuum" (and their `weak_coupling`/`continuum_claim`-style
identifier spellings), case-insensitively:

  - `forward/ax1/report.md`, `reverse/ax1/report.md`  (the AX1 reports)
  - `forward/ax1/output/results.json`, `reverse/ax1/output/results.json`
  - `advisor/ax1-gate.json`  (the gate)
  - `skeptic/ax1.json`  (the skeptic review's structured verdict)

`skeptic/ax1.md` (the skeptic's narrative review) is also scanned, as
additional, non-required coverage, reported separately.

Every occurrence is printed with a context window and classified as:

  - `negation_or_exclusion` -- the term appears inside a claim-exclusion list
    (contract `claim_exclusions`/`preregistration.claim_exclusions`, a results
    packet's `exclusions`/`forbidden` array), as a rejected-mutation label or
    table entry ("a 'weak coupling' label" listed among what a control rejects),
    or next to an explicit negation cue (never, not, false, reject(ed/s),
    forbidden, exclu*, without) -- i.e. the term is being named in order to rule
    it out, not asserted as a property of the result;
  - `AFFIRMATIVE` -- none of the above cues are present nearby, i.e. the term
    reads as an actual claim. Any `AFFIRMATIVE` occurrence fails this script.

The classification is a text heuristic (context-window cue search), not a
semantic parse; every occurrence and its full context is printed so a human (or
a future assistant) can re-check the classification directly rather than trust
the label alone. Human project author: Hruday N M (BUNZEEY); AI-assisted.

Usage: python3 -B forbidden_wording_grep.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common3 as K  # noqa: E402

WEAK_RE = re.compile(r'weak[ _-]?(bare[ _-]?)?coupling', re.I)
CONTINUUM_RE = re.compile(r'continuum', re.I)

NEGATION_CUES = (
    'never', 'not ', 'not\n', 'no ', "n't", 'false', 'reject', 'forbidden', 'exclu', 'without',
    'labelled', 'label"', "a \"weak", "a 'weak", 'damaging', 'mutation', 'tamper', 'rebound',
    'is never described', 'checker rejects', 'checker scans',
    'no_priority_or_continuum_claim', 'claim_exclusions', 'claim exclusions', 'forbidden":',
    '"forbidden"',
)

# JSON files nest the enclosing key ("rejected_mutations", "forbidden", "exclusions", ...)
# further back than a local character window reliably reaches (e.g. a six-item
# "rejected_mutations" array before the matched string). For .json files, the
# nearest preceding `"key":` label (unbounded backward search within the file)
# is folded into the classification text as well as the local window, so the
# key name itself (not just nearby prose) can supply a negation cue.
JSON_KEY_RE = re.compile(r'"([A-Za-z0-9_]+)"\s*:')

REQUIRED_FILES = {
    'forward_report': K.FORWARD_AX1_REPORT,
    'reverse_report': K.REVERSE_AX1_REPORT,
    'forward_results': K.FORWARD_AX1_RESULTS,
    'reverse_results': K.REVERSE_AX1_RESULTS,
    'gate': K.AX1_GATE,
    'skeptic_review_json': K.SKEPTIC_AX1_JSON,
}
BONUS_FILES = {
    'skeptic_review_md': K.SKEPTIC_AX1_MD,
}

CONTEXT_RADIUS = 180


def line_of(text, offset):
    return text.count('\n', 0, offset) + 1


def classify(window):
    w = window.lower()
    hits = [cue for cue in NEGATION_CUES if cue in w]
    if hits:
        return 'negation_or_exclusion', hits
    return 'AFFIRMATIVE', []


def nearest_json_key(text, pos):
    m = None
    for cand in JSON_KEY_RE.finditer(text, 0, pos):
        m = cand
    return m.group(1) if m else None


def scan_file(label, path):
    text = K.load_text(path)
    is_json = path.suffix == '.json'
    occurrences = []
    for term_name, pattern in (('weak coupling', WEAK_RE), ('continuum', CONTINUUM_RE)):
        for m in pattern.finditer(text):
            start = max(0, m.start() - CONTEXT_RADIUS)
            end = min(len(text), m.end() + CONTEXT_RADIUS)
            window = text[start:end].replace('\n', ' ')
            key = nearest_json_key(text, m.start()) if is_json else None
            classify_input = ((key + ' ') if key else '') + window
            kind, cues = classify(classify_input)
            occurrences.append({
                'term': term_name,
                'matched_text': m.group(0),
                'line': line_of(text, m.start()),
                'enclosing_json_key': key,
                'context': window.strip(),
                'classification': kind,
                'cues_found': cues,
            })
    affirmative = [o for o in occurrences if o['classification'] == 'AFFIRMATIVE']
    return {
        'file': label,
        'path': str(path.relative_to(K.ROOT)),
        'n_occurrences': len(occurrences),
        'n_affirmative': len(affirmative),
        'occurrences': occurrences,
        'passed': len(affirmative) == 0,
    }


SCRATCH_DISCLOSURE_CUES = (
    'scratchpad disclosure', 'my scratch work', 'scratch work stayed', 'private subfolder',
    'private folder', '-private/', 'ax1-forward-private', 'ax1-reverse-private',
)


def scratch_disclosure_check(label, path):
    text = K.load_text(path)
    lower = text.lower()
    found_cues = [c for c in SCRATCH_DISCLOSURE_CUES if c.lower() in lower]
    has_private_path = bool(re.search(r'/tmp/[\w./-]*-private', text))
    has_disclosure_heading = bool(re.search(r'scratch', lower))
    passed = bool(found_cues) and has_private_path
    return {
        'file': label,
        'path': str(path.relative_to(K.ROOT)),
        'passed': passed,
        'cues_found': found_cues,
        'private_subfolder_path_present': has_private_path,
        'mentions_scratch_at_all': has_disclosure_heading,
    }


def run():
    file_results = []
    for label, path in REQUIRED_FILES.items():
        file_results.append(scan_file(label, path))
    bonus_results = []
    for label, path in BONUS_FILES.items():
        bonus_results.append(scan_file(label, path))

    scratch_checks = [
        scratch_disclosure_check('forward_report', K.FORWARD_AX1_REPORT),
        scratch_disclosure_check('reverse_report', K.REVERSE_AX1_REPORT),
    ]

    wording_pass = all(r['passed'] for r in file_results)
    scratch_pass = all(c['passed'] for c in scratch_checks)

    total_occurrences = sum(r['n_occurrences'] for r in file_results)
    total_affirmative = sum(r['n_affirmative'] for r in file_results)

    findings = []
    findings.append('Scanned %d required files for "weak coupling" and "continuum" (case-insensitive, plus '
                    'underscore/hyphen identifier spellings): %d total occurrences, %d classified '
                    'AFFIRMATIVE.' % (len(file_results), total_occurrences, total_affirmative))
    if total_affirmative == 0:
        findings.append('Every occurrence in the AX1 reports, both results.json files, the gate and the '
                        'skeptic review is inside a claim-exclusion list, a rejected-mutation/control-table '
                        'entry, an explicit false claim flag ("continuum_claim":false / '
                        '"weak_coupling_claim":false), or a direct negation ("never described as weak '
                        'coupling or as a continuum approach"). None reads as an affirmative claim.')
    for r in file_results:
        if not r['passed']:
            findings.append('FAIL: %s has %d affirmative occurrence(s); see occurrences for detail.'
                            % (r['file'], r['n_affirmative']))

    if scratch_pass:
        findings.append('Both AX1 producer reports carry the sub-round-2 scratch-isolation disclosure rule: '
                        'each names its own private-subfolder scratch path (forward: '
                        '/tmp/claude-0/ax1-forward-private/; reverse: /tmp/claude-0/ax1-reverse-private/) and '
                        'states what was and was not read from other agents\' scratch.')
    else:
        for c in scratch_checks:
            if not c['passed']:
                findings.append('FAIL: %s is missing a private-subfolder scratch-disclosure line.' % c['file'])

    bonus_affirmative = sum(r['n_affirmative'] for r in bonus_results)
    findings.append('Bonus (non-required) coverage: skeptic/ax1.md scanned as well -- %d occurrences, %d '
                    'affirmative.' % (sum(r['n_occurrences'] for r in bonus_results), bonus_affirmative))

    result = {
        'id': 'forbidden_wording_grep',
        'role': 'forbidden-wording grep and scratch-disclosure check; zero research loops',
        'terms_grepped': ['weak coupling', 'continuum'],
        'files_required': [r['file'] for r in file_results],
        'files_bonus': [r['file'] for r in bonus_results],
        'file_results': file_results,
        'bonus_file_results': bonus_results,
        'scratch_disclosure_checks': scratch_checks,
        'total_occurrences': total_occurrences,
        'total_affirmative': total_affirmative,
        'findings': findings,
        'wording_pass': wording_pass,
        'scratch_pass': scratch_pass,
    }
    result['pass'] = wording_pass and scratch_pass
    return result


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'forbidden_wording_grep', result)
    print('forbidden_wording_grep: %s' % ('PASS' if result['pass'] else 'FAIL'))
    print('  wording_pass=%r (%d/%d occurrences affirmative)' % (result['wording_pass'], result['total_affirmative'],
                                                                  result['total_occurrences']))
    print('  scratch_pass=%r' % result['scratch_pass'])
    for r in result['file_results']:
        print('   [%s] %s: %d occurrences, %d affirmative' % ('x' if r['passed'] else ' ', r['file'],
                                                                r['n_occurrences'], r['n_affirmative']))
    for c in result['scratch_disclosure_checks']:
        print('   [%s] scratch disclosure: %s' % ('x' if c['passed'] else ' ', c['file']))
    print()
    for f in result['findings']:
        print('  FINDING:', f)
    if not result['pass']:
        sys.exit(1)


if __name__ == '__main__':
    main()
