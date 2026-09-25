#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 sub-round 2, assistant-2 script 1 of 4: the phrase
scan and rate-claim audit (calling task item 1).

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not import
`forward/*/check.py`, `reverse/*/check.py`, or any other producer/skeptic module;
imports `research/round33/tools/phrase_scan.py` as a library, exactly as the
calling task permits (it is infrastructure -- rule R6 of the Round32 closing
panel -- and computes no scientific result of its own).

Two sub-checks:

  (a) `phrase_scan_dry_run` -- runs the real Round33 scanner (`tools.phrase_scan
      .scan`, negation-aware, each contract's own `mandatory_sentence_template`
      removed as one literal before scanning) with the BB1 contract over BB1's
      four packet files, and with the BB2 contract over BB2's four packet files:
      `forward/<loop>/report.md` and `reverse/<loop>/report.md` scanned as one
      text blob (as `record_gate.py` would scan a report), `forward/<loop>/
      output/results.json` and `reverse/<loop>/output/results.json` scanned
      **string field by string field** (`common2.walk_all_strings`), exactly as
      the calling task's own wording asks ("on every string field of each
      results.json") -- unlike a whole-file text scan, this keeps a "clause" a
      genuine natural-language clause, not JSON punctuation. Every hit (negated
      or not) is listed with its clause, per the calling task's own instruction
      ("list every hit (affirmative or negated) with its clause"); each is also
      classified as `negated_exclusion`, `quoted_mention_or_control_description`
      (a producer's own damaging-mutation self-test record, a `"phrase"`/
      `"clause"` pair or an `affirmative_<name>`/`rejected_mutations` control id
      that must CONTAIN the forbidden text to prove the checker rejects it -- not
      this project's own claim) or `AFFIRMATIVE_needs_review` (a genuine
      candidate defect), the same three-way split assistant-1 used for BA1/BA2.

  (b) `rate_claim_audit` -- every clause (the same clause-splitting rule as (a)
      and as `tools/phrase_scan.py` itself) in any of the four report.md files
      that states a RATE claim (contains `O(1/N)`, the bare word `geometric`,
      the bare word `decays`/`decay`, or the literal phrase `rate in N`), listed
      with whether that clause itself carries an explicit two-sided numeric
      range of `N` (a pattern such as `5<=N<=14000`, `N=5..59` or `N=5..3000`,
      not only a one-sided `N>=5` or a bare "for N"). This is the sub-check the
      calling task names directly: "the skeptic found that the BB2 forward
      states the item-5 rate O(1/N) without the certified range 5<=N<=14000;
      find every such unqualified rate sentence in all four reports."

Usage: python3 -B phrase_audit.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common2 as K  # noqa: E402

sys.path.insert(0, str(K.TOOLS))
import phrase_scan as ps  # noqa: E402  (imported as a library, per the calling task)


# ---------------------------------------------------------------------------
# (a) phrase_scan.py dry run (report.md as one blob; results.json string field
#     by string field) + three-way classification of every hit.
# ---------------------------------------------------------------------------
MENTION_MARKERS = (
    '"phrase"', '"clause"', '"matched_text"', 'affirmative forbidden phrasing', 'rejected_mutation',
    'rejected_mutations', 'affirmative_', 'damaging', 'mutation', 'checklist', 'self-test', 'self_test',
    'must_abort', 'silent_edits', 'weakening', 'rejected reason', 'is rejected',
)


def scan_with_positions(text, forbidden, template=None):
    """Re-implements tools.phrase_scan.scan's own body/clause construction but
    keeps track of each hit's character offset in the normalized (and, if a
    template is given, template-stripped) body, so this script can inspect the
    text immediately around a hit without re-guessing phrase_scan.py's own
    normalization. Produces exactly the same (phrase, clause, negated) triples
    `phrase_scan.scan` would, in the same order; adds 'start'/'end' in `body`."""
    body = ps.normalize(text)
    if template:
        body = body.replace(ps.normalize(template), ' ')
    hits = []
    search_from = 0
    for clause in ps.clauses(body):
        idx = body.find(clause, search_from)
        if idx == -1:
            idx = body.find(clause)
        for phrase in forbidden:
            pat = re.compile(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', re.I)
            for m in pat.finditer(clause):
                hits.append({
                    'phrase': phrase, 'clause': clause[:240], 'negated': bool(ps.NEGATION.search(clause)),
                    'start': idx + m.start(), 'end': idx + m.end(),
                })
        search_from = idx + len(clause)
    return hits, body


def classify_hit(body, hit):
    if hit['negated']:
        return 'negated_exclusion'
    window = body[max(0, hit['start'] - 200):min(len(body), hit['end'] + 200)].lower()
    markers = [m for m in MENTION_MARKERS if m in window]
    if markers:
        return 'quoted_mention_or_control_description'
    return 'AFFIRMATIVE_needs_review'


def scan_report(loop, label, path, forbidden, template):
    text = K.load_text(path)
    hits, body = scan_with_positions(text, forbidden, template)
    rows = []
    for h in hits:
        rows.append({'phrase': h['phrase'], 'clause': h['clause'], 'phrase_scan_negated': h['negated'],
                     'classification': classify_hit(body, h), 'json_path': None})
    return rows


def scan_results_json(loop, label, path, forbidden, template):
    data = K.load_json(path)
    rows = []
    for json_path, value in K.walk_all_strings(data):
        hits, body = scan_with_positions(value, forbidden, template)
        for h in hits:
            rows.append({'phrase': h['phrase'], 'clause': h['clause'], 'phrase_scan_negated': h['negated'],
                         'classification': classify_hit(body, h), 'json_path': json_path})
    return rows


def phrase_scan_dry_run():
    per_loop = {}
    all_hits = []
    for loop in K.LOOPS:
        L = loop.upper()
        contract = K.load_contract(loop)
        forbidden, template = ps.contract_terms(contract)
        targets = K.SCAN_TARGETS[loop]
        per_file = {}
        for label, path in targets.items():
            if label.endswith('_results'):
                rows = scan_results_json(loop, label, path, forbidden, template)
            else:
                rows = scan_report(loop, label, path, forbidden, template)
            for r in rows:
                all_hits.append(dict(r, loop=L, file=label, path=str(path.relative_to(K.ROOT))))
            per_file[label] = {
                'path': str(path.relative_to(K.ROOT)), 'n_hits': len(rows),
                'n_affirmative_needs_review': sum(1 for r in rows if r['classification'] == 'AFFIRMATIVE_needs_review'),
                'hits': rows,
            }
        per_loop[L] = {'forbidden_phrase_count': len(forbidden), 'template_present': bool(template), 'files': per_file}

    affirmative = [h for h in all_hits if h['classification'] == 'AFFIRMATIVE_needs_review']
    findings = [
        'Ran tools.phrase_scan.scan (rule R6: negation-aware, mandatory_sentence_template removed as one literal) '
        'with the BB1 contract over BB1\'s 4 packet files (forward/reverse report.md as one blob each; forward/'
        'reverse output/results.json string field by string field) and with the BB2 contract over BB2\'s 4 packet '
        'files the same way -- 8 files total (2 reports scanned whole, 2 results.json scanned string field by '
        'string field, per loop).',
        'Total raw hits (every hit tools.phrase_scan.scan found, affirmative or negated, listed per the calling '
        'task\'s own instruction): %d.' % len(all_hits),
    ]
    for loop in K.LOOPS:
        L = loop.upper()
        for label, fe in per_loop[L]['files'].items():
            if fe['n_hits']:
                kinds = {}
                for h in fe['hits']:
                    kinds[h['classification']] = kinds.get(h['classification'], 0) + 1
                findings.append('%s %s (%s): %d hit(s), by classification: %r' % (L, label, fe['path'], fe['n_hits'], kinds))
    if not any(per_loop[loop.upper()]['files'][label]['n_hits'] for loop in K.LOOPS for label in K.SCAN_TARGETS[loop]):
        findings.append('0 raw hits in any of the 8 files: neither BB1 nor BB2\'s forward/reverse report.md or '
                        'output/results.json (scanned string field by string field) contains any literal '
                        'ROUND_FORBIDDEN or contract-forbidden phrase, negated or not.')
    if affirmative:
        findings.append('%d hit(s) classified AFFIRMATIVE_needs_review (DEFECT):' % len(affirmative))
        for h in affirmative:
            loc = (' at %s' % h['json_path']) if h['json_path'] else ''
            findings.append('  DEFECT: %s %s (%s)%s :: phrase=%r :: clause=%r' % (h['loop'], h['file'], h['path'], loc, h['phrase'], h['clause']))
    else:
        findings.append('0 hits classified AFFIRMATIVE_needs_review: every raw hit (if any) is either a negated '
                        'exclusion (phrase_scan.py\'s own NEGATION cue) or a quoted mention inside a producer\'s own '
                        'rejected-mutation self-test record -- not this project\'s own affirmative claim.')
    return {
        'id': 'phrase_scan_dry_run',
        'role': 'calling task item 1 (first half): negation-aware phrase scan with each contract on each of the '
                'four reports and on every string field of each results.json; list every hit (affirmative or '
                'negated) with its clause; zero research loops',
        'per_loop': per_loop, 'total_raw_hits': len(all_hits), 'all_hits': all_hits,
        'affirmative_defects': affirmative, 'passed': len(affirmative) == 0, 'findings': findings,
    }


# ---------------------------------------------------------------------------
# (b) rate-claim audit: every clause in the four reports stating O(1/N),
#     "geometric", "decays"/"decay", or "rate in N", with whether that clause
#     carries an explicit two-sided numeric range of N.
# ---------------------------------------------------------------------------
RATE_CLAIM_RE = re.compile(
    r'O\(\s*1\s*/\s*N\s*\)|\bgeometric(?:ally)?\b|\bdecays?\b|\brate in `?N`?\b',
    re.I,
)
# A genuine two-sided range: both a lower and an upper numeric bound on N in
# the SAME clause, e.g. "5<=N<=14000", "5 <= N <= 464", "N=5..59", "N = 5..3000",
# "N from 5 to 59". A bare "N>=5", "for N" or "at fixed N" is NOT counted as a
# range (it names N, not a bound on how far the claim is certified).
TWO_SIDED_RANGE_RE = re.compile(
    r'\d+\s*<=\s*N\s*<=\s*\d+'
    r'|N\s*=\s*\d+\s*\.\.\s*\d+'
    r'|N\s*=\s*\d+\s*to\s*\d+'
    r'|N\s*from\s*\d+\s*to\s*\d+',
    re.I,
)
LOWER_BOUND_ONLY_RE = re.compile(r'\bN\s*(>=|\\geq|≥)\s*\d+\b|\bN\s*\\geq', re.I)

REPORT_LABELS = {'bb1': ('forward', 'reverse'), 'bb2': ('forward', 'reverse')}


def rate_claim_audit():
    per_loop = {}
    all_rows = []
    for loop in K.LOOPS:
        L = loop.upper()
        contract = K.load_contract(loop)
        template_norm = K.normalize(contract['preregistration']['mandatory_sentence_template'])
        per_side = {}
        for side, path in (('forward', K.FORWARD_REPORT_PATHS[loop]), ('reverse', K.REVERSE_REPORT_PATHS[loop])):
            text = K.load_text(path)
            body = K.normalize(text)
            rows = []
            for cl in K.clauses(body):
                if RATE_CLAIM_RE.search(cl):
                    two_sided = bool(TWO_SIDED_RANGE_RE.search(cl))
                    lower_only = bool(LOWER_BOUND_ONLY_RE.search(cl)) and not two_sided
                    # The mandatory_sentence_template itself is frozen contract text, quoted verbatim once per
                    # report (rule R7, checked by template_and_fields.py); it is not this producer's own prose
                    # about the item-5 rate, so it is flagged separately and excluded from the calling task's
                    # named "unqualified rate sentence" tally below (both BB1's and BB2's templates say "a rate
                    # in N" with no range, by contract design -- that is a round-wide contract wording choice,
                    # not a per-report defect to attribute to one producer).
                    # A markdown-bold marker directly after the heading's colon ("...once):** For the
                    # zero-selected...") stops phrase_scan.py's own ": " clause break from firing, fusing the
                    # "Mandatory sentence (...)" heading onto the template's first segment in one clause; a
                    # straight two-way substring test misses that fused case, so a match on the template's own
                    # opening words is accepted too.
                    template_prefix = template_norm[:60].lower()
                    is_template = template_norm in cl or cl in template_norm or template_prefix in cl.lower()
                    rows.append({
                        'clause': cl[:400], 'has_two_sided_range': two_sided,
                        'has_lower_bound_only': lower_only, 'is_mandatory_template_clause': is_template,
                        'matched_keywords': sorted(set(m.group(0).lower() for m in RATE_CLAIM_RE.finditer(cl))),
                    })
            per_side[side] = rows
            for r in rows:
                all_rows.append(dict(r, loop=L, side=side, path=str(path.relative_to(K.ROOT))))
        per_loop[L] = per_side

    unqualified = [r for r in all_rows if not r['has_two_sided_range']]
    unqualified_prose = [r for r in unqualified if not r['is_mandatory_template_clause']]
    bb2_forward_unqualified = [r for r in unqualified_prose if r['loop'] == 'BB2' and r['side'] == 'forward']

    findings = [
        'Scanned every clause (phrase_scan.py\'s own clause-splitting rule: sentence end, semicolon or colon) of all '
        'four report.md files for a RATE claim: O(1/N), the bare word "geometric"/"geometrically", the bare word '
        '"decay"/"decays", or the literal phrase "rate in N". Total rate-claim clauses found: %d; without an '
        'explicit two-sided numeric range of N (e.g. "5<=N<=14000" or "N=5..59") in the SAME clause: %d, of which '
        '%d are the frozen mandatory_sentence_template itself (quoted verbatim, contract wording, not counted '
        'below as a producer-authored unqualified sentence) and %d are the producer\'s own prose.'
        % (len(all_rows), len(unqualified), len(unqualified) - len(unqualified_prose), len(unqualified_prose)),
        'The calling task\'s own named instance: the skeptic found the BB2 forward states the item-5 rate O(1/N) '
        'without the certified range 5<=N<=14000 (that range appears only in the BB2 reverse report, sections 8/8.5, '
        'never in the BB2 forward report). BB2 forward unqualified prose rate-claim clauses found here: %d.'
        % len(bb2_forward_unqualified),
    ]
    for r in all_rows:
        tag = 'QUALIFIED(two-sided range)' if r['has_two_sided_range'] else (
            'mandatory_sentence_template (frozen wording, not a producer claim)' if r['is_mandatory_template_clause'] else (
                'lower-bound-only (still UNQUALIFIED as a range)' if r['has_lower_bound_only'] else 'UNQUALIFIED'))
        findings.append('%s %s (%s) [%s] keywords=%r :: %r' % (r['loop'], r['side'], r['path'], tag, r['matched_keywords'], r['clause']))

    if bb2_forward_unqualified:
        findings.append('BB2 forward unqualified prose rate-claim clauses (matches the calling task\'s own named defect):')
        for r in bb2_forward_unqualified:
            findings.append('  DEFECT (per calling task): BB2 forward :: %r' % r['clause'])
    findings.append('Every other report\'s (BB1 forward, BB1 reverse, BB2 reverse) unqualified prose rate-claim '
                    'clauses are listed above with tag UNQUALIFIED or lower-bound-only; BB2 reverse alone carries '
                    'explicit two-sided ranges (5<=N<=14000, and per-block 5<=N<=464) alongside its own unqualified '
                    'restatements of the same headline claim (e.g. "The rate is O(1/N) because ... is polynomial", '
                    'section 8.5) -- so even the producer that proves the range restates the bare claim elsewhere '
                    'without repeating it; the calling task\'s point is that BB2 forward never states the range '
                    'anywhere in its report, not even once.')

    return {
        'id': 'rate_claim_audit',
        'role': 'calling task item 1 (second half): every clause stating a RATE claim (O(1/N), geometric, decays, '
                'rate in N) with whether it carries an explicit range of N; find every unqualified rate clause in '
                'all four reports, specifically checking the calling task\'s own named BB2-forward item-5 instance; '
                'zero research loops',
        'per_loop': per_loop, 'all_rows': all_rows, 'unqualified': unqualified,
        'unqualified_prose': unqualified_prose, 'bb2_forward_unqualified': bb2_forward_unqualified,
        # This is a find-and-tabulate audit, not a pass/fail gate (the calling task asks to "find every such
        # unqualified rate sentence", not to block on finding one); recorded true, findings carry every instance.
        'passed': True, 'findings': findings,
    }


def run():
    checks = [phrase_scan_dry_run(), rate_claim_audit()]
    return {
        'id': 'phrase_audit',
        'role': 'Jung/Pauli lens, Round33 sub-round 2, assistant-2: the phrase/rate-claim audit, calling task item '
                '1; zero research loops; audits only, never admission evidence',
        'checks': {c['id']: c for c in checks},
        'passed': all(c['passed'] for c in checks),
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'phrase_audit', result)
    print('phrase_audit: %s' % ('PASS' if result['passed'] else 'FAIL (see findings)'))
    for check_id, c in result['checks'].items():
        print('  %s: %s' % (check_id, 'PASS' if c['passed'] else 'FAIL'))
        for f in c['findings']:
            print('    -', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
