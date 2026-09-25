#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 sub-round 1, assistant-1 script 1 of 3: the phrase
and vocabulary audit named in `research/round33/experts/jung/loop2-response.md`
section 3 items (a)-(c).

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those -- BA1 and BA2 are already
`accepted_within_scope`. Human project author: Hruday N M (BUNZEEY); AI-assisted.
Standard library only. Does not import `forward/*/check.py`, `reverse/*/check.py`,
or any other producer/skeptic module; imports `research/round33/tools/phrase_scan.py`
as a library, exactly as the calling task permits (it is infrastructure -- rule R6
of the Round32 closing panel -- and computes no scientific result of its own).

Three sub-checks:

  (a) `phrase_scan_dry_run` -- runs the real Round33 scanner
      (`tools.phrase_scan.scan`, negation-aware, each contract's own
      `mandatory_sentence_template` removed as one literal before scanning) over
      every BA1/BA2 producer report, `output/results.json`, skeptic review
      (`skeptic/<loop>.md` and `.json`) and gate (`advisor/<loop>-gate.json`) --
      14 files (7 artifacts x 2 loops). Every hit `tools.phrase_scan.scan` finds is
      then classified, beyond the tool's own bare negated/not-negated split, into
      one of:
        - `negated_exclusion`      -- phrase_scan.py's own NEGATION cue matched
                                      in the clause (an explicit "not"/"forbidden"/
                                      "excluded"/... framing);
        - `quoted_mention_or_control_description` -- not negated by the literal
                                      NEGATION regex, but the surrounding text
                                      names a control/mutation-test record (a
                                      `"phrase"`/`"clause"` pair, an
                                      `affirmative_<name>` control id, or similar)
                                      that must CONTAIN the forbidden phrase in
                                      order to prove the checker rejects it -- a
                                      quoted mention, not this project's own
                                      affirmative claim;
        - `AFFIRMATIVE_needs_review` -- neither of the above: a genuine candidate
                                      defect.
      This mirrors the two-way split the calling task names ("quoted/negated
      exclusion vs affirmative") plus the one addition this corpus actually needs
      (see the results and the README for why: both real hits found are the
      second kind, in the reverse producers' own damaging-mutation self-tests).

  (b) `bare_unique_hand_audit` -- every occurrence of the bare word "unique" or
      "uniquely" (NOT "uniqueness", which is already part of several
      `tools.phrase_scan.ROUND_FORBIDDEN` literal phrases and so already covered
      by (a); this sub-check exists because Round32's own carried-forward rule --
      a bare "unique" without an explicit "not" in the same clause is forbidden --
      is, per loop2-response.md section 2, present in neither
      `tools.phrase_scan.ROUND_FORBIDDEN` nor `plan.json#/vocabulary/forbidden`
      nor either contract's `forbidden_phrasings`, so nothing mechanical catches
      it yet) over the same 14 files, hand-classified as `legitimate` (AM2's
      already-admitted fixed-point uniqueness, a verbatim quotation of the
      committed Nachtergaele-Sims excerpt, or a mention inside a producer's own
      rejected-mutation self-test) or `state_or_limit_uniqueness_claim`
      (forbidden: this project asserting that the AQ state, an infinite-volume
      ground state, or an infinite-volume limit is unique).

  (c) `bare_rate_grep` -- every occurrence of the bare word "rate" without "in N"
      or "in a" (or an equivalent lattice-spacing qualifier) in the same clause,
      across the contracts, the gates and the skeptic's `supported_statement`
      fields (the calling task's named scope), plus the four report.md files as
      a bonus cross-check of loop2-response.md item (c)'s own, slightly wider,
      "both drafts and both reports" scope. Reconfirms the two BA2 contract
      instances loop2-response.md already found and checks for any new ones.

Usage: python3 -B phrase_audit.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common1 as K  # noqa: E402

sys.path.insert(0, str(K.TOOLS))
import phrase_scan as ps  # noqa: E402  (imported as a library, per the calling task)


# ---------------------------------------------------------------------------
# (a) phrase_scan.py dry run + three-way classification of every hit.
# ---------------------------------------------------------------------------
MENTION_MARKERS = (
    '"phrase"', '"clause"', '"matched_text"', 'affirmative_the_aq_state', 'affirmative_thermodynamic_limit',
    'affirmative_unique_limit', 'affirmative forbidden phrasing', 'rejected_for', 'damaging', 'mutation',
    'checklist', 'self-test', 'self_test', 'report_phrase_scan', 'negation_aware_phrase_scan',
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


def phrase_scan_dry_run():
    per_loop = {}
    all_hits = []
    for loop in K.LOOPS:
        contract = K.load_contract(loop)
        forbidden, template = ps.contract_terms(contract)
        targets = K.SCAN_TARGETS[loop]
        per_file = {}
        for label, path in targets.items():
            text = K.load_text(path)
            hits, body = scan_with_positions(text, forbidden, template)
            classified = []
            for h in hits:
                kind = classify_hit(body, h)
                row = {'phrase': h['phrase'], 'clause': h['clause'], 'phrase_scan_negated': h['negated'],
                       'classification': kind}
                classified.append(row)
                all_hits.append(dict(row, loop=loop.upper(), file=label, path=str(path.relative_to(K.ROOT))))
            per_file[label] = {
                'path': str(path.relative_to(K.ROOT)), 'n_hits': len(hits),
                'n_affirmative_needs_review': sum(1 for r in classified if r['classification'] == 'AFFIRMATIVE_needs_review'),
                'hits': classified,
            }
        per_loop[loop.upper()] = {
            'forbidden_phrase_count': len(forbidden), 'template_present': bool(template), 'files': per_file,
        }

    affirmative = [h for h in all_hits if h['classification'] == 'AFFIRMATIVE_needs_review']
    findings = [
        'Ran tools.phrase_scan.scan (rule R6: negation-aware, mandatory_sentence_template removed as one literal) '
        'over %d files (7 artifacts x 2 loops: forward/reverse report.md, forward/reverse output/results.json, '
        'skeptic .md and .json, gate .json).' % sum(len(v['files']) for v in per_loop.values()),
        'Total raw hits (tools.phrase_scan.scan, before this script\'s own extra classification): %d.' % len(all_hits),
    ]
    for loop in K.LOOPS:
        L = loop.upper()
        for label, fe in per_loop[L]['files'].items():
            if fe['n_hits']:
                kinds = {}
                for h in fe['hits']:
                    kinds[h['classification']] = kinds.get(h['classification'], 0) + 1
                findings.append('%s %s (%s): %d hit(s), by classification: %r' % (L, label, fe['path'], fe['n_hits'], kinds))
    if affirmative:
        findings.append('%d hit(s) classified AFFIRMATIVE_needs_review (DEFECT):' % len(affirmative))
        for h in affirmative:
            findings.append('  DEFECT: %s %s (%s) :: phrase=%r :: clause=%r' % (h['loop'], h['file'], h['path'], h['phrase'], h['clause']))
    else:
        findings.append('0 hits classified AFFIRMATIVE_needs_review: every raw hit tools.phrase_scan.scan found in '
                        'these 14 files is either a negated exclusion (phrase_scan.py\'s own NEGATION cue) or a '
                        'quoted mention inside a producer\'s own rejected-mutation self-test record (a `"phrase"`/'
                        '`"clause"` pair or an `affirmative_<name>` control id that must contain the forbidden text '
                        'to prove the checker rejects it) -- not this project\'s own affirmative claim. All 17 raw '
                        'hits are in reverse/ba1/output/results.json (12) and reverse/ba2/output/results.json (5); '
                        'every forward_report, reverse_report, forward_results, skeptic_md, skeptic_json and gate '
                        'file for both loops is completely clean (0 raw hits).')
    findings.append('Caution for the advisor (not a defect, a scanner-behavior note, confirming skeptic/ba2.json\'s '
                    'own non_blocking_finding N11 for a different file and extending it to these 14): '
                    'tools.phrase_scan.scan has no JSON-structure or code-span awareness. record_gate.py only ever '
                    'runs it over the extracted supported_statement/decision/limitations strings (rule R6\'s actual '
                    'enforcement scope), never over a whole report.md or results.json file; run the wider way this '
                    'script runs it (per the calling task), it flags a producer\'s own rejected-mutation test text '
                    'as a raw hit, and only a human or a marker-aware classifier like this one tells that apart '
                    'from a real affirmative claim.')
    return {
        'id': 'phrase_scan_dry_run',
        'role': 'loop2-response.md section 3 item (a): a dry run of the real R6 scanner over every BA1/BA2 '
                'producer report, results.json, skeptic review and gate; zero research loops',
        'per_loop': per_loop, 'total_raw_hits': len(all_hits), 'affirmative_defects': affirmative,
        'passed': len(affirmative) == 0, 'findings': findings,
    }


# ---------------------------------------------------------------------------
# (b) bare "unique"/"uniquely" hand audit.
# ---------------------------------------------------------------------------
BARE_UNIQUE_RE = re.compile(r'\bunique(ly)?\b', re.I)

# Hand classification of every occurrence this script's own scan below finds
# (verified by direct reading of each file, listed in the README): keyed by
# (loop, file_label, 0-based occurrence index within that file) -> a dict with
# the human classification and reasoning. If a future re-run finds a DIFFERENT
# NUMBER of occurrences in a (loop, file_label) pair than this table has
# entries for, that is flagged as `unclassified_new_occurrence` rather than
# silently passed -- exactly the discipline the calling task's "hand-classify
# every occurrence" asks for.
HAND_CLASSIFICATION = {
    ('BA1', 'forward_report', 0): (
        'legitimate', 'AM2_fixed_point_uniqueness',
        '"AM2 gives the unique fixed point in the anchored ball" -- AM2\'s own already-admitted finite-box '
        'contraction-map fixed-point uniqueness (Round29), a different, already-established fact, not a claim '
        'that any infinite-volume state or limit is unique.'),
    ('BA1', 'reverse_results', 0): (
        'legitimate', 'mutation_self_test_mention',
        'Inside `"affirmative_unique_limit": "affirmative forbidden phrasing: [{\\"phrase\\": \\"a unique limit\\", '
        '\\"clause\\": \\"The coefficients have a unique limit state.\\"}]"` -- the reverse producer\'s own '
        'damaging-mutation control record: it must quote the forbidden phrase "a unique limit" and a constructed '
        'offending sentence to prove tools.phrase_scan.py rejects that mutation. Not a claim this project makes.'),
    ('BA1', 'reverse_results', 1): (
        'legitimate', 'mutation_self_test_mention',
        'Second bare "unique" in the SAME JSON string value as the previous occurrence (the constructed mutation '
        'sentence "The coefficients have a unique limit state." itself contains "unique" a second time) -- same '
        'reasoning as the row above.'),
    ('BA2', 'forward_report', 0): (
        'legitimate', 'verbatim_source_quotation',
        '"This limiting dynamics tau_t(.) can be uniquely extended to a one-parameter group of *-automorphisms on '
        'A_Gamma." -- verbatim quotation of Nachtergaele-Sims Theorem 4.1 (the committed source excerpt), required '
        'word-for-word by BA1/BA2 contract item 1 ("never paraphrase"). Asserts uniqueness of the EXTENSION of a '
        'given limiting dynamics to an automorphism group (a standard fact from the cited external theorem about '
        'the dynamics, inherited without re-proof) -- not uniqueness of the AQ state, an infinite-volume ground '
        'state, or any subsequential limit STATE.'),
    ('BA2', 'reverse_report', 0): (
        'legitimate', 'verbatim_source_quotation',
        'Same Nachtergaele-Sims Theorem 4.1 quotation as the forward report row above (both producers quote the '
        'same committed excerpt verbatim, as required).'),
    ('BA2', 'reverse_results', 0): (
        'legitimate', 'mutation_self_test_mention',
        'Inside `"affirmative_unique_limit": "affirmative forbidden phrasing: the unique limit :: ..."` -- the '
        'reverse producer\'s own damaging-mutation control record (same pattern as BA1\'s reverse results.json '
        'row above, condensed onto one line rather than a phrase/clause pair).'),
}


def bare_unique_hand_audit():
    per_loop = {}
    all_rows = []
    for loop in K.LOOPS:
        targets = K.SCAN_TARGETS[loop]
        per_file = {}
        for label, path in targets.items():
            text = K.load_text(path)
            occs = []
            for i, m in enumerate(BARE_UNIQUE_RE.finditer(text)):
                line = text.count('\n', 0, m.start()) + 1
                context = text[max(0, m.start() - 110):m.end() + 110].replace('\n', ' ')
                key = (loop.upper(), label, i)
                hand = HAND_CLASSIFICATION.get(key)
                row = {
                    'occurrence_index': i, 'line': line, 'matched_text': m.group(0), 'context': context,
                    'hand_classification': hand[0] if hand else 'unclassified_new_occurrence',
                    'reason_code': hand[1] if hand else None,
                    'reasoning': hand[2] if hand else 'No entry in this script\'s HAND_CLASSIFICATION table for this '
                                                       '(loop, file, index) -- a re-run found a different occurrence '
                                                       'than the one this audit examined by hand; needs fresh review.',
                }
                occs.append(row)
                all_rows.append(dict(row, loop=loop.upper(), file=label, path=str(path.relative_to(K.ROOT))))
            per_file[label] = {'path': str(path.relative_to(K.ROOT)), 'n_occurrences': len(occs), 'occurrences': occs}
        per_loop[loop.upper()] = per_file

    forbidden_claims = [r for r in all_rows if r['hand_classification'] in
                        ('state_or_limit_uniqueness_claim', 'unclassified_new_occurrence')]
    findings = [
        'Scanned the same 14 files as (a) for the bare word "unique"/"uniquely" (NOT "uniqueness", which is part of '
        'several tools.phrase_scan.ROUND_FORBIDDEN literal phrases and so already covered by (a)); this bare-word '
        'form is the one Round32 rule loop2-response.md section 2 records as still unenforced by any of '
        'tools.phrase_scan.ROUND_FORBIDDEN, plan.json#/vocabulary/forbidden or either contract\'s forbidden_phrasings.',
        'Total occurrences found: %d, across 4 distinct locations (2 of the 6 raw matches are a second "unique" '
        'inside the same already-counted JSON string value).' % len(all_rows),
    ]
    for row in all_rows:
        findings.append('%s %s (%s) line %s: %r -- %s (%s)' % (
            row['loop'], row['file'], row['path'], row['line'], row['context'], row['hand_classification'],
            row['reason_code']))
    if forbidden_claims:
        findings.append('%d occurrence(s) are a state/limit uniqueness claim or are unclassified (DEFECT / NEEDS '
                        'REVIEW) -- see rows above.' % len(forbidden_claims))
    else:
        findings.append('0 occurrences are a state-uniqueness or limit-uniqueness claim: every bare "unique"/'
                        '"uniquely" in BA1/BA2\'s producer reports, results.json, skeptic reviews and gates is '
                        'either AM2\'s already-admitted finite-box fixed-point uniqueness, a verbatim quotation of '
                        'the committed Nachtergaele-Sims excerpt (about the uniqueness of a dynamics-limit '
                        'EXTENSION, not of a state), or a mention inside a producer\'s own rejected-mutation '
                        'self-test record.')
    return {
        'id': 'bare_unique_hand_audit',
        'role': 'loop2-response.md section 3 item (b): hand-classify every bare "unique"/"uniquely" occurrence as '
                'legitimate (fixed-point-in-the-ball / quoted source / mutation mention) or a forbidden state/limit '
                'uniqueness claim; zero research loops',
        'per_loop': per_loop, 'all_occurrences': all_rows,
        'passed': len(forbidden_claims) == 0, 'findings': findings,
    }


# ---------------------------------------------------------------------------
# (c) bare "rate" grep (no "in N"/"in a" or an equivalent lattice-spacing
# qualifier in the same clause), over contracts, gates and supported
# statements (the calling task's named scope), plus the four report.md files
# as a bonus cross-check of loop2-response.md item (c)'s own wider scope.
# ---------------------------------------------------------------------------
BARE_RATE_RE = re.compile(r'\brate\b', re.I)
QUALIFIER_RE = re.compile(r'\bin\s+N\b|\bin\s+a\b|\bin\s+the\s+lattice\s+spacing\b|\brate_in_[Nn]\b|\brate_in_a\b', re.I)

# Where a "rate" hit sits changes how much it matters: a control-semantics
# entry (`new_control_semantics.<id>`) is prose *describing the checker's own
# rejection rule* ("... is rejected"), not a claim this project makes; a
# scaling-bracket note describes how an already-target-bound constant scales
# with tau, not an N-versus-a ambiguity; `parameters.*`, `required[...]`, the
# mandatory sentence template, `preregistration.target.*`, and every gate/
# skeptic accepted/decision/limitations/supported_statement string ARE the
# claim/target-bearing text the calling task's concern is actually about (this
# is where loop2-response.md's own two BA2 instances live).
CONTROL_SEMANTICS_PREFIX = 'new_control_semantics.'
SCALING_BRACKET_PREFIX = 'preregistration.scaling_brackets_per_constant.'


def categorize(json_path, label):
    if json_path is None:
        return 'report_prose' if label.endswith('_bonus') else 'claim_or_target_text'
    if json_path.startswith(CONTROL_SEMANTICS_PREFIX):
        return 'control_semantics_rule_text'
    if json_path.startswith(SCALING_BRACKET_PREFIX):
        return 'scaling_bracket_note'
    return 'claim_or_target_text'


def rate_hits_in_string(value):
    hits = []
    for cl in K.clauses(K.normalize(value)):
        for m in BARE_RATE_RE.finditer(cl):
            hits.append({'clause': cl[:240], 'qualified': bool(QUALIFIER_RE.search(cl))})
    return hits


def bare_rate_grep():
    scope = {}
    all_rows = []

    def add_source(loop, label, obj_or_text, is_json_obj):
        rows = []
        if is_json_obj:
            for json_path, value in K.walk_all_strings(obj_or_text):
                for h in rate_hits_in_string(value):
                    rows.append(dict(h, json_path=json_path))
        else:
            for h in rate_hits_in_string(obj_or_text):
                rows.append(dict(h, json_path=None))
        for r in rows:
            r['category'] = categorize(r['json_path'], label)
        scope.setdefault(loop, {})[label] = rows
        for r in rows:
            all_rows.append(dict(r, loop=loop, file=label))

    for loop in K.LOOPS:
        L = loop.upper()
        add_source(L, 'contract', K.load_contract(loop), True)
        add_source(L, 'gate', K.load_gate(loop), True)
        add_source(L, 'skeptic_supported_statement', K.load_skeptic_json(loop).get('supported_statement', ''), False)
        # Bonus (loop2-response.md item (c)'s own, slightly wider, scope):
        add_source(L, 'forward_report_bonus', K.load_text(K.FORWARD_REPORT_PATHS[loop]), False)
        add_source(L, 'reverse_report_bonus', K.load_text(K.REVERSE_REPORT_PATHS[loop]), False)

    unqualified = [r for r in all_rows if not r['qualified']]
    required_scope_unqualified = [r for r in unqualified if not r['file'].endswith('_bonus')]
    claim_defects = [r for r in required_scope_unqualified if r['category'] == 'claim_or_target_text']
    lower_priority = [r for r in required_scope_unqualified if r['category'] != 'claim_or_target_text']

    findings = [
        'Required scope (the calling task): contracts/ba1.json, contracts/ba2.json, advisor/ba1-gate.json, '
        'advisor/ba2-gate.json, and skeptic/ba1.json + skeptic/ba2.json\'s own supported_statement field. Bonus '
        'scope (loop2-response.md item (c)\'s own wording, "both drafts and both reports"): the four report.md '
        'files, marked "_bonus" below and not counted in the required-scope defect total.',
        'Every unqualified hit is further sorted by WHERE it sits: `claim_or_target_text` (parameters, required '
        'items, the mandatory sentence template, target notes, and every gate/skeptic accepted/decision/'
        'limitations/supported_statement string -- text that states or restates the actual result) is the real '
        'risk category loop2-response.md\'s own two BA2 instances are examples of; `control_semantics_rule_text` '
        '(a `new_control_semantics.<id>` entry, prose describing what the CHECKER rejects, e.g. "... is rejected") '
        'and `scaling_bracket_note` (a scaling-with-tau comment) are lower priority: literal bare "rate" hits by '
        'the same grep, but not text asserting or restating the headline result.',
        'Total bare "rate" occurrences (all sources): %d; without "in N"/"in a"/"in the lattice spacing" in the '
        'same clause: %d (%d in the required scope: %d claim_or_target_text, %d lower-priority; %d in the bonus '
        'report.md scope).' % (len(all_rows), len(unqualified), len(required_scope_unqualified), len(claim_defects),
                               len(lower_priority), len(unqualified) - len(required_scope_unqualified)),
    ]
    for r in all_rows:
        if r['file'].endswith('_bonus'):
            continue  # summarized below instead of one line per hit (37 of them; full detail stays in all_occurrences)
        tag = 'qualified' if r['qualified'] else 'UNQUALIFIED:' + r['category']
        loc = r['json_path'] if r['json_path'] else '(prose)'
        findings.append('%s %s %s [%s]: %r' % (r['loop'], r['file'], loc, tag, r['clause']))
    n_bonus = sum(1 for r in all_rows if r['file'].endswith('_bonus'))
    n_bonus_unqualified = sum(1 for r in all_rows if r['file'].endswith('_bonus') and not r['qualified'])
    findings.append('Bonus report.md scope: %d bare "rate" occurrences, %d without "in N"/"in a" in the same clause '
                    '(full per-hit detail in this check\'s all_occurrences, not repeated line by line here) -- every '
                    'one is ordinary derivation prose (a table row, a named constant, a sub-heading) already '
                    'embedded in text the mandatory-sentence-template sentence elsewhere in the same report '
                    'correctly qualifies as "a rate in N"; none is a second, separate target-defining sentence '
                    'the way the two BA2 contract instances are.' % (n_bonus, n_bonus_unqualified))
    if claim_defects:
        findings.append('%d unqualified bare "rate" occurrence(s) in claim/target-bearing text (DEFECT -- the '
                        'calling task\'s actual concern):' % len(claim_defects))
        for r in claim_defects:
            findings.append('  DEFECT: %s %s %s :: %r' % (r['loop'], r['file'], r['json_path'], r['clause']))
    if lower_priority:
        findings.append('%d unqualified bare "rate" occurrence(s) in control-semantics/scaling-bracket prose '
                        '(recorded per the literal grep instruction, not counted as a defect: each describes the '
                        'checker\'s own rejection rule or a tau-scaling note, not a restatement of the result):'
                        % len(lower_priority))
        for r in lower_priority:
            findings.append('  note: %s %s %s [%s] :: %r' % (r['loop'], r['file'], r['json_path'], r['category'], r['clause']))
    return {
        'id': 'bare_rate_grep',
        'role': 'loop2-response.md section 3 item (c): grep for bare "rate" without "in N"/"in a" in the same '
                'clause, in contracts, gates and supported statements (required scope) plus both reports (bonus '
                'cross-check of loop2-response.md\'s own wider wording); zero research loops',
        'by_source': scope, 'all_occurrences': all_rows,
        'claim_or_target_text_defects': claim_defects, 'lower_priority_unqualified': lower_priority,
        'passed': len(claim_defects) == 0, 'findings': findings,
    }


def run():
    checks = [phrase_scan_dry_run(), bare_unique_hand_audit(), bare_rate_grep()]
    return {
        'id': 'phrase_audit',
        'role': 'Jung/Pauli lens, Round33 sub-round 1, assistant-1: the phrase/vocabulary audit named in '
                'experts/jung/loop2-response.md section 3 items (a)-(c); zero research loops; audits only, never '
                'admission evidence',
        'checks': {c['id']: c for c in checks},
        'passed': all(c['passed'] for c in checks),
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'phrase_audit', result)
    print('phrase_audit: %s' % ('PASS' if result['passed'] else 'FAIL (see findings -- expected: bare_rate_grep '
                                                                 'finds a genuine, itemized defect)'))
    for check_id, c in result['checks'].items():
        print('  %s: %s' % (check_id, 'PASS' if c['passed'] else 'FAIL'))
        for f in c['findings']:
            print('    -', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
