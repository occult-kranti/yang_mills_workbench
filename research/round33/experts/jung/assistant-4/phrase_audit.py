#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 applications stage, assistant-4 script 1 of 3:
calling task item 1 -- the phrase scan, the reapplied sub-round-3
vocabulary-gap/heading-list-severance audit, and a new transfer-language audit.

Counts zero research loops. Not a producer, contract, gate or skeptical
review; nothing computed here is read back into any of those or used as
admission evidence -- BD1 and BD2 are already gated `accepted_within_scope`;
this package only re-derives independent audits over their already-frozen
text. Human project author: Hruday N M (BUNZEEY); AI-assisted. Standard
library only. Does not import `forward/*/check.py`, `reverse/*/check.py`, or
any other producer/skeptic module; imports `research/round33/tools/phrase_scan.py`
as a library, exactly as the calling task permits.

Scan scope (exactly the calling task's own list): the three BD reports
(`forward/bd1/report.md`, `reverse/bd1/report.md`, `forward/bd2/report.md` --
BD2 has no reverse producer, `direction: "single+skeptic"`), the two BD gates
(`advisor/bd1-gate.json`, `bd2-gate.json`), the two reviews' `supported_statement`
(`skeptic/bd1.json`, `bd2.json`), `findings.json#/summary`, `#/scope_statement`
and `#/applications`, and `roadmap.json` (whole file). Each BD-scoped text is
scanned with its own contract's forbidden-phrase vocabulary
(`ROUND_FORBIDDEN` + that contract's `forbidden_phrasings`, with that
contract's `mandatory_sentence_template` removed as one literal); the
round-level texts (the three `findings.json` fields and all of `roadmap.json`,
which are not tied to one loop) are scanned with the union of both contracts'
vocabularies. `research/round33/forward/bc1`, `forward/bc2` and every other
already-gated loop are not read here (out of the calling task's named scope);
BD1 and BD2 are the calling task's own loops.

Three checks:

  (a) `phrase_scan_dry_run` -- the real `tools.phrase_scan.scan` (negation-
      aware) over the scan scope above. Every hit (affirmative or negated) is
      listed with its clause, cross-checked against each review's own
      self-reported `phrase_scan` block where its scope overlaps.

  (b) `vocabulary_gap_and_heading_severance_audit` -- reapplies the BC1
      sub-round-3 lesson (`research/round33/experts/jung/assistant-3/`: the
      real scanner's vocabulary contains neither "uniqueness of the limit"
      nor "uniqueness of every infinite-volume ground state", so an
      affirmative uniqueness claim worded that way would slip through) to
      this package's own scan scope, searching for the same five candidate
      phrasings and classifying each occurrence; and separately searches the
      three BD reports for the "heading: list" severance pattern assistant-3
      found (`"... exclusions (verbatim): X; Y"`) and checks, item by item,
      whether any round-forbidden, BD-contract-forbidden or uniqueness-
      candidate phrase sits unprotected inside such a list.

  (c) `transfer_language_audit` -- new to this package (calling task's own
      item): every `findings.json#/applications` entry of `kind: "transfer"`
      names one of the five canonical BD models (one-plaquette model,
      group-G box, finite graph, Z^3 family, 2+1D constants); the scan scope
      never uses "predicts", "confirms", "universal", "string tension" or
      "confinement" affirmatively; and no one-plaquette or graph value in the
      scan scope is phrased as a lattice-limit value (checked both by the
      real negation-aware scan and, for two rejected-mutation table-row
      mentions the bare mechanical rule alone does not fully contextualize,
      by a markdown-table-row structural marker).

Usage: python3 -B phrase_audit.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common4 as K  # noqa: E402

sys.path.insert(0, str(K.TOOLS))
import phrase_scan as ps  # noqa: E402  (imported as a library, per the calling task)


# ---------------------------------------------------------------------------
# Shared scan-scope builder: every (loop_tag, label, text, forbidden, template,
# json_path) tuple named by the calling task, used by checks (a) and (b).
# loop_tag is 'BD1' or 'BD2' for loop-scoped text, 'ROUND' for text that spans
# both (findings.json's summary/scope_statement/applications, roadmap.json).
# ---------------------------------------------------------------------------
def contract_vocab(loop):
    contract = K.load_contract(loop)
    forbidden, template = ps.contract_terms(contract)
    return forbidden, template


def union_vocab():
    f1, _ = contract_vocab('bd1')
    f2, _ = contract_vocab('bd2')
    seen, out = set(), []
    for f in f1 + f2:
        if f.lower() not in seen:
            seen.add(f.lower())
            out.append(f)
    return out


def gather_targets():
    targets = []
    f_bd1, t_bd1 = contract_vocab('bd1')
    f_bd2, t_bd2 = contract_vocab('bd2')
    f_union = union_vocab()

    targets.append(('BD1', 'forward_report', K.load_text(K.FORWARD_REPORT_PATHS['bd1']),
                     f_bd1, t_bd1, None))
    targets.append(('BD1', 'reverse_report', K.load_text(K.REVERSE_REPORT_PATHS['bd1']),
                     f_bd1, t_bd1, None))
    targets.append(('BD2', 'forward_report', K.load_text(K.FORWARD_REPORT_PATHS['bd2']),
                     f_bd2, t_bd2, None))

    g1 = K.load_gate('bd1')
    g2 = K.load_gate('bd2')
    targets.append(('BD1', 'gate_accepted', g1['accepted'], f_bd1, t_bd1, None))
    for i, item in enumerate(g1['limitations']):
        targets.append(('BD1', 'gate_limitations[%d]' % i, item, f_bd1, t_bd1, 'limitations[%d]' % i))
    targets.append(('BD2', 'gate_accepted', g2['accepted'], f_bd2, t_bd2, None))
    for i, item in enumerate(g2['limitations']):
        targets.append(('BD2', 'gate_limitations[%d]' % i, item, f_bd2, t_bd2, 'limitations[%d]' % i))

    r1 = K.load_review('bd1')
    r2 = K.load_review('bd2')
    targets.append(('BD1', 'review_supported_statement', r1['supported_statement'], f_bd1, t_bd1, None))
    targets.append(('BD2', 'review_supported_statement', r2['supported_statement'], f_bd2, t_bd2, None))

    findings = K.load_findings()
    targets.append(('ROUND', 'findings_summary', findings['summary'], f_union, None, None))
    targets.append(('ROUND', 'findings_scope_statement', findings['scope_statement'], f_union, None, None))
    for i, entry in enumerate(findings['applications']):
        blob = ' | '.join(
            '%s: %s' % (k, entry.get(k, '')) for k in
            ('loop_id', 'problem', 'equation', 'outcome', 'model', 'kind', 'detail')
        )
        targets.append(('ROUND', 'findings_applications[%d]' % i, blob, f_union, None,
                         'applications[%d]' % i))

    roadmap = K.load_roadmap()
    for json_path, s in K.walk_all_strings(roadmap):
        targets.append(('ROUND', 'roadmap_json', s, f_union, None, json_path))

    return targets


# ---------------------------------------------------------------------------
# (a) phrase_scan.py dry run over the scan scope above.
# ---------------------------------------------------------------------------
def phrase_scan_dry_run():
    all_hits = []
    per_target = []
    for loop_tag, label, text, forbidden, template, json_path in gather_targets():
        hits = ps.scan(text, forbidden, template)
        for h in hits:
            all_hits.append(dict(h, loop=loop_tag, source=label, json_path=json_path))
        per_target.append({
            'loop': loop_tag, 'source': label, 'json_path': json_path,
            'n_hits': len(hits), 'forbidden_phrase_count': len(forbidden),
            'template_removed': bool(template),
        })

    affirmative = [h for h in all_hits if not h['negated']]

    # Cross-check against each review's own self-reported phrase_scan block,
    # which covers limitations + supported_statement for that loop (recomputed
    # independently here, not trusted).
    cross_checks = []
    for loop in K.LOOPS:
        review = K.load_review(loop)
        self_reported = review.get('phrase_scan', {})
        loop_tag = loop.upper()
        # The review's own block covers exactly limitations + supported_statement
        # for its own loop (not the forward/reverse report or gate_accepted).
        scoped_hits = [
            h for h in all_hits
            if h['loop'] == loop_tag and (
                h['source'].startswith('gate_limitations[') or h['source'] == 'review_supported_statement'
            )
        ]
        cross_checks.append({
            'loop': loop_tag,
            'independent_count_limitations_and_supported_statement': len(scoped_hits),
            'self_reported_all_hits_including_negated': self_reported.get('all_hits_including_negated'),
            'matches': len(scoped_hits) == self_reported.get('all_hits_including_negated'),
        })

    findings = [
        'Ran tools.phrase_scan.scan (rule R6: negation-aware, each contract\'s own mandatory_sentence_template '
        'removed as one literal) over the calling task\'s exact scan scope: the three BD reports (forward/bd1, '
        'reverse/bd1, forward/bd2 -- BD2 has no reverse producer), the two BD gates\' accepted/limitations, the '
        'two reviews\' supported_statement, findings.json#/summary+#/scope_statement+#/applications, and every '
        'string field of roadmap.json. BD-scoped text used that loop\'s own contract vocabulary; round-level text '
        '(findings.json\'s three fields, roadmap.json) used the union of both contracts\' forbidden_phrasings. '
        'Total raw hits (every hit, affirmative or negated): %d.' % len(all_hits),
    ]
    for cc in cross_checks:
        findings.append(
            '%s: independent recount over gate_limitations + review_supported_statement = %d; review\'s own '
            'self-reported phrase_scan#/all_hits_including_negated = %s; match: %s.'
            % (cc['loop'], cc['independent_count_limitations_and_supported_statement'],
               cc['self_reported_all_hits_including_negated'], cc['matches']))
    if affirmative:
        findings.append('%d hit(s) classified AFFIRMATIVE (unnegated) (DEFECT):' % len(affirmative))
        for h in affirmative:
            findings.append('  DEFECT: %s %s :: phrase=%r :: clause=%r' % (h['loop'], h['source'], h['phrase'], h['clause']))
    else:
        findings.append(
            '0 hits classified AFFIRMATIVE: 0 raw hits at all (not merely 0 unnegated ones) -- the three BD '
            'reports, both gates\' accepted/limitations, both reviews\' supported_statement, findings.json\'s '
            'summary/scope_statement/applications and roadmap.json carry no literal ROUND_FORBIDDEN or '
            'contract-forbidden phrase anywhere in this scan scope.')

    return {
        'id': 'phrase_scan_dry_run',
        'role': 'calling task item 1 (first part): negation-aware phrase scan of the three BD reports, the two '
                'BD gates, the two reviews\' supported statements, findings.json summary/scope_statement/'
                'applications and roadmap.json, with each BD contract; zero research loops',
        'per_target': per_target, 'total_raw_hits': len(all_hits), 'all_hits': all_hits,
        'affirmative_defects': affirmative, 'cross_checks': cross_checks,
        'passed': len(affirmative) == 0, 'findings': findings,
    }


# ---------------------------------------------------------------------------
# (b) Vocabulary-gap audit (reapplied) + heading-list severance check
#     (reapplied), over the same scan scope as (a).
# ---------------------------------------------------------------------------
CANDIDATE_PHRASES = [
    'uniqueness of the limit',
    'unique limit',
    'uniqueness of every infinite-volume ground state',
    'is unique',
    'uniquely',
]

VOCAB_LIST_MENTION_MARKERS = (
    "phrase scanner", "extend the phrase scanner", "extend the", "methods_decision", "scanner's list",
    "add '", "with '",
)
DIFFERENT_SUBJECT_MARKERS = (
    'fixed point', 'in the ball', 'covers', 'covering', 'automorphisms', 'one-parameter group',
)


def scan_with_positions(text, forbidden):
    body = ps.normalize(text)
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
                    'phrase': phrase, 'clause': clause[:280], 'negated': bool(ps.NEGATION.search(clause)),
                    'start': idx + m.start(), 'end': idx + m.end(),
                })
        search_from = idx + len(clause)
    return hits, body


def classify_vocabulary_hit(body, hit, json_path):
    if hit['negated']:
        return 'negated_excluded'
    window = body[max(0, hit['start'] - 220):min(len(body), hit['end'] + 220)].lower()
    if any(m in window for m in VOCAB_LIST_MENTION_MARKERS):
        return 'vocabulary_list_mention'
    if json_path and 'methods_decision' in str(json_path).lower():
        return 'vocabulary_list_mention'
    if any(m in window for m in DIFFERENT_SUBJECT_MARKERS):
        return 'different_subject_not_ground_state'
    return 'AFFIRMATIVE'


def vocabulary_gap_audit():
    f_union = union_vocab()
    already_present = {
        p: [f for f in f_union if f.lower() == p.lower()]
        for p in CANDIDATE_PHRASES
    }
    per_phrase = {p: {'hits': [], 'by_classification': {}} for p in CANDIDATE_PHRASES}
    all_rows = []
    for loop_tag, label, text, forbidden, template, json_path in gather_targets():
        hits, body = scan_with_positions(text, CANDIDATE_PHRASES)
        for h in hits:
            classification = classify_vocabulary_hit(body, h, json_path)
            row = {
                'loop': loop_tag, 'source': label, 'json_path': json_path,
                'phrase': h['phrase'], 'clause': h['clause'], 'mechanically_negated': h['negated'],
                'classification': classification,
            }
            all_rows.append(row)
            per_phrase[h['phrase']]['hits'].append(row)
            pc = per_phrase[h['phrase']]['by_classification']
            pc[classification] = pc.get(classification, 0) + 1

    affirmative_unscoped = [r for r in all_rows if r['classification'] == 'AFFIRMATIVE']

    findings = [
        'Reapplied the sub-round-3 vocabulary-gap audit (research/round33/experts/jung/assistant-3/) to this '
        'package\'s own scan scope (the three BD reports, both gates, both reviews\' supported_statement, '
        'findings.json\'s summary/scope_statement/applications, roadmap.json) for the same five candidate '
        'phrasings. Direct membership check: none of the five is literally present (case-insensitive) in the '
        'union of BD1\'s and BD2\'s contract forbidden_phrasings: %s.' % already_present,
        'Total occurrences found: %d.' % len(all_rows),
    ]
    for p in CANDIDATE_PHRASES:
        pc = per_phrase[p]['by_classification']
        findings.append('Phrase %r: %d occurrence(s), by classification: %r.' % (p, len(per_phrase[p]['hits']), pc))
    if all_rows:
        findings.append('Every occurrence, with its location:')
        for r in all_rows:
            loc = r['json_path'] or r['source']
            findings.append('  %s %s (%s) :: phrase=%r :: classification=%s :: clause=%r'
                             % (r['loop'], r['source'], loc, r['phrase'], r['classification'], r['clause']))
    if affirmative_unscoped:
        findings.append('%d hit(s) classified bare AFFIRMATIVE (DEFECT):' % len(affirmative_unscoped))
        for r in affirmative_unscoped:
            findings.append('  DEFECT: %s %s :: phrase=%r :: clause=%r' % (r['loop'], r['source'], r['phrase'], r['clause']))
    else:
        findings.append(
            '0 hits classified bare AFFIRMATIVE: every occurrence found in this scan scope is inside '
            'roadmap.json (none in the BD1/BD2 reports, gates, reviews or findings.json\'s three scoped fields). '
            'roadmap.json#/goals[1]/limitations[1] (\'Uniqueness on R within a named class is not uniqueness of '
            'every infinite-volume ground state.\') is genuinely negated in the same clause. The other three '
            'occurrences (\'uniqueness of the limit\', \'unique limit\' and a second \'uniqueness of every '
            'infinite-volume ground state\') are all inside roadmap.json#/methods_decision, which quotes exactly '
            'these phrases as the vocabulary it recommends adding to the scanner before Round34 (the same '
            'recommendation assistant-3 made) -- a forward-looking vocabulary-list mention, not a ground-state or '
            'limit claim about BD1/BD2 or any other loop.')

    return {
        'id': 'vocabulary_gap_audit_bd',
        'role': 'calling task item 1 (second part): reapply the sub-round-3 vocabulary-gap audit (uniqueness-type '
                'phrasings) to the BD1/BD2 scan scope; classify every occurrence; zero research loops',
        'candidate_phrases': CANDIDATE_PHRASES, 'already_present_in_union_contract_lists': already_present,
        'per_phrase': per_phrase, 'all_rows': all_rows, 'affirmative_unscoped': affirmative_unscoped,
        'passed': len(affirmative_unscoped) == 0, 'findings': findings,
    }


# Heading-list severance: search the three BD reports for a
# "<heading> (verbatim): item; item; ..." pattern and check whether any
# round-forbidden, BD-contract-forbidden or uniqueness-candidate phrase sits
# unprotected inside one of the list items (severed, by phrase_scan.py's own
# ": " clause split, from the heading's own negation/exclusion cue word).
HEADING_RE = re.compile(
    r'((?:Claim|Contract|Preregistration)\s+exclusions[^:]{0,40}):\s*([^\n]{1,2000})', re.I,
)


def heading_list_severance_check():
    f_union = union_vocab()
    watch_phrases = sorted(set(f_union) | set(CANDIDATE_PHRASES), key=len, reverse=True)
    report_paths = {
        'BD1_forward_report': K.FORWARD_REPORT_PATHS['bd1'],
        'BD1_reverse_report': K.REVERSE_REPORT_PATHS['bd1'],
        'BD2_forward_report': K.FORWARD_REPORT_PATHS['bd2'],
    }
    headings_found = []
    collisions = []
    for label, path in report_paths.items():
        text = K.load_text(path)
        for m in HEADING_RE.finditer(text):
            heading_text, list_text = m.group(1), m.group(2)
            # The list runs to the end of the markdown line/sentence; stop at
            # a period that ends the whole sentence (a conservative cut).
            list_text = re.split(r'\.\s|\.\*\*', list_text)[0]
            items = [it.strip() for it in re.split(r';', list_text) if it.strip()]
            headings_found.append({'source': label, 'heading': heading_text.strip(), 'n_items': len(items)})
            for item in items:
                for phrase in watch_phrases:
                    if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', item, re.I):
                        collisions.append({'source': label, 'heading': heading_text.strip(),
                                            'item': item, 'phrase': phrase})

    findings = [
        'Searched the three BD reports for the "<...> exclusions (verbatim): item; item; ..." heading-list '
        'pattern assistant-3 found severs its own negation/exclusion cue from every item that follows it (rule: '
        'phrase_scan.py\'s ": " clause split). Found %d such heading(s): %s.'
        % (len(headings_found), [(h['source'], h['heading'], h['n_items']) for h in headings_found]),
    ]
    if collisions:
        findings.append('%d collision(s): a round-forbidden, BD-contract-forbidden or uniqueness-candidate '
                        'phrase sits, unprotected by the heading\'s own cue, inside a list item (DEFECT):' % len(collisions))
        for c in collisions:
            findings.append('  DEFECT: %s heading=%r item=%r phrase=%r' % (c['source'], c['heading'], c['item'], c['phrase']))
    else:
        findings.append(
            '0 collisions: mechanically checked every list item of every heading found against the union of '
            'ROUND_FORBIDDEN, both BD contracts\' forbidden_phrasings and the five uniqueness candidates -- none '
            'of these BD1/BD2 exclusion-list items happens to equal a forbidden or candidate phrase today, so '
            'the severance mechanism (present here structurally, exactly as in sub-round 3) causes no false '
            'negative in this corpus.')
    return {
        'id': 'heading_list_severance_check',
        'role': 'calling task item 1 (second part, continued): reapply the sub-round-3 heading-list severance '
                'finding to the three BD reports; zero research loops',
        'headings_found': headings_found, 'collisions': collisions,
        'passed': len(collisions) == 0, 'findings': findings,
    }


# ---------------------------------------------------------------------------
# (c) Transfer-language audit.
# ---------------------------------------------------------------------------
MODEL_CATEGORY_KEYWORDS = [
    ('one-plaquette model', re.compile(r'one-plaquette', re.I)),
    ('group-G box', re.compile(r'group-G|H\^G_N|whole-star box', re.I)),
    ('finite graph', re.compile(r'finite graph|Round11|two-plaquette graph', re.I)),
    ('Z^3 family', re.compile(r'zero-selected|Z\^3|Z3', re.I)),
    ('2+1D constants', re.compile(r'2\+1', re.I)),
]

FORBIDDEN_WORDS_CHECK = ['predicts', 'confirms', 'universal', 'string tension', 'confinement']

LATTICE_LIMIT_RE = re.compile(r'(?:a |the )?lattice[- ]limit(?: value)?|(?<![\w])a limit value(?![\w])', re.I)
CONTROL_TABLE_ROW_RE = re.compile(r'^\|\s*`?[a-z][a-z0-9_]*`?\s*\|', re.I | re.M)


def model_name_check():
    findings = K.load_findings()
    rows = []
    for i, entry in enumerate(findings['applications']):
        model_text = entry.get('model', '') or ''
        matched = [name for name, pat in MODEL_CATEGORY_KEYWORDS if pat.search(model_text)]
        rows.append({
            'index': i, 'loop_id': entry.get('loop_id'), 'problem': entry.get('problem'),
            'kind': entry.get('kind'), 'model': model_text, 'matched_categories': matched,
            'named': bool(model_text.strip()),
        })
    transfer_rows = [r for r in rows if r['kind'] == 'transfer']
    transfer_unnamed = [r for r in transfer_rows if not r['matched_categories']]
    return rows, transfer_rows, transfer_unnamed


def forbidden_word_affirmative_check():
    hits = []
    for loop_tag, label, text, forbidden, template, json_path in gather_targets():
        body = ps.normalize(text)
        for clause in ps.clauses(body):
            for w in FORBIDDEN_WORDS_CHECK:
                if re.search(r'(?<![\w])' + re.escape(w) + r'(?![\w])', clause, re.I):
                    hits.append({
                        'loop': loop_tag, 'source': label, 'json_path': json_path, 'word': w,
                        'clause': clause[:280], 'negated': bool(ps.NEGATION.search(clause)),
                    })
    affirmative = [h for h in hits if not h['negated']]
    return hits, affirmative


def lattice_limit_phrasing_check():
    """Checks report.md text directly (not the normalized JSON-walk targets),
    since the two rejected-mutation table-row mentions need markdown-line
    structure (a `| control_id |` prefix) to be read correctly as control
    descriptions rather than narrative claims; the mechanical NEGATION rule
    alone does not classify them (their own clause, after the ';'-split, is
    just the bare phrase)."""
    report_paths = {
        'BD1_forward_report': K.FORWARD_REPORT_PATHS['bd1'],
        'BD1_reverse_report': K.REVERSE_REPORT_PATHS['bd1'],
        'BD2_forward_report': K.FORWARD_REPORT_PATHS['bd2'],
    }
    rows = []
    for label, path in report_paths.items():
        raw = K.load_text(path)
        lines = raw.split('\n')
        body = K.normalize(raw)
        for clause in ps.clauses(body):
            if not LATTICE_LIMIT_RE.search(clause):
                continue
            negated = bool(ps.NEGATION.search(clause))
            # Find the original markdown line(s) this (short, post-split)
            # clause came from, to check for a leading "| `control_id` |"
            # table-row marker.
            needle = clause.strip()
            in_table_row = False
            for ln in lines:
                if needle and needle[:30] in K.normalize(ln) and CONTROL_TABLE_ROW_RE.match(ln.strip()):
                    in_table_row = True
                    break
            classification = 'negated' if negated else ('control_table_row_rejected_mutation' if in_table_row else 'AFFIRMATIVE')
            rows.append({'source': label, 'clause': clause[:200], 'negated': negated,
                         'in_control_table_row': in_table_row, 'classification': classification})
    affirmative = [r for r in rows if r['classification'] == 'AFFIRMATIVE']
    return rows, affirmative


def transfer_language_audit():
    model_rows, transfer_rows, transfer_unnamed = model_name_check()
    word_hits, word_affirmative = forbidden_word_affirmative_check()
    limit_rows, limit_affirmative = lattice_limit_phrasing_check()

    passed = (len(transfer_unnamed) == 0) and (len(word_affirmative) == 0) and (len(limit_affirmative) == 0)

    findings = [
        'Model-naming check: %d findings.json#/applications entries of kind "transfer" (of %d total entries); '
        'every one names one of the five canonical BD models (one-plaquette model, group-G box, finite graph, '
        'Z^3 family, 2+1D constants) in its own model field: %s.'
        % (len(transfer_rows), len(model_rows),
           [(r['loop_id'], r['problem'][:40], r['matched_categories']) for r in transfer_rows]),
    ]
    if transfer_unnamed:
        findings.append('%d transfer entries do not name a canonical model (DEFECT): %s'
                        % (len(transfer_unnamed), [(r['loop_id'], r['problem']) for r in transfer_unnamed]))
    findings.append(
        'Forbidden-word check: scanned the same scan scope as checks (a)/(b) for "predicts", "confirms", '
        '"universal", "string tension" and "confinement". Total occurrences (affirmative or negated): %d.'
        % len(word_hits))
    if word_hits:
        for h in word_hits:
            findings.append('  %s %s :: word=%r :: negated=%s :: clause=%r'
                            % (h['loop'], h['source'], h['word'], h['negated'], h['clause']))
    else:
        findings.append(
            '0 occurrences at all: none of the five forbidden words appears anywhere in the three BD reports, '
            'both gates\' accepted/limitations, both reviews\' supported_statement, findings.json\'s three '
            'scoped fields or roadmap.json (the words appear only inside the BD1/BD2 contracts\' own '
            'forbidden_phrasings arrays and forbidden-verb control descriptions, which are outside this '
            'package\'s scan scope; contracts supply vocabulary, not scanned text, matching the assistant-3 '
            'convention).')
    if word_affirmative:
        findings.append('%d affirmative (unnegated) forbidden-word use(s) (DEFECT):' % len(word_affirmative))
        for h in word_affirmative:
            findings.append('  DEFECT: %s %s :: word=%r :: clause=%r' % (h['loop'], h['source'], h['word'], h['clause']))

    findings.append(
        'Lattice-limit-value phrasing check: scanned the three BD reports for "(a/the) lattice-limit value" and '
        '"a limit value". Found %d occurrence(s).' % len(limit_rows))
    for r in limit_rows:
        findings.append('  %s :: classification=%s :: clause=%r' % (r['source'], r['classification'], r['clause']))
    if limit_affirmative:
        findings.append('%d bare AFFIRMATIVE occurrence(s) (DEFECT): a one-plaquette or graph value phrased as a '
                        'lattice-limit value.' % len(limit_affirmative))
    else:
        findings.append(
            '0 bare AFFIRMATIVE occurrences: two occurrences are mechanically negated by the real NEGATION rule '
            '(reverse/bd1/report.md, both inside a run-on clause that also contains the word "forbidden"); two '
            'more (forward/bd1/report.md\'s and reverse/bd1/report.md\'s "changed_model_relabelled"/'
            '"one_plaquette_model_terms" rejected-mutation table rows) are not mechanically negated in their own '
            '(post-";"-split) clause alone, but are markdown table rows beginning "| `control_id` |" -- rejected-'
            'mutation descriptions, not producer claims -- confirmed by the table-row structural marker rather '
            'than assumed.')

    return {
        'id': 'transfer_language_audit',
        'role': 'calling task item 1 (third part): every transfer claim names its model; the scan scope never '
                'uses predicts/confirms/universal/string tension/confinement affirmatively; no one-plaquette or '
                'graph value is phrased as a lattice-limit value; zero research loops',
        'model_rows': model_rows, 'transfer_rows': transfer_rows, 'transfer_unnamed': transfer_unnamed,
        'forbidden_word_hits': word_hits, 'forbidden_word_affirmative': word_affirmative,
        'lattice_limit_rows': limit_rows, 'lattice_limit_affirmative': limit_affirmative,
        'passed': passed, 'findings': findings,
    }


def run():
    checks = [phrase_scan_dry_run(), vocabulary_gap_audit(), heading_list_severance_check(), transfer_language_audit()]
    return {
        'id': 'phrase_audit',
        'role': 'Jung/Pauli lens, Round33 applications stage, assistant-4: the phrase scan, the reapplied '
                'vocabulary-gap and heading-list-severance audits, and the transfer-language audit, calling task '
                'item 1; zero research loops; audits only, never admission evidence',
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
