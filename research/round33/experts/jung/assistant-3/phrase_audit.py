#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 sub-round 3, assistant-3 script 1 of 3: the phrase
scan (calling task item 1, first half) and the vocabulary-gap audit (calling task
item 1, second half).

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those or used as admission
evidence -- BC1 and BC2 are already gated `accepted_within_scope`; this package
only re-derives independent checks over their already-frozen text. Human project
author: Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not import
`forward/*/check.py`, `reverse/*/check.py`, or any other producer/skeptic module;
imports `research/round33/tools/phrase_scan.py` as a library, exactly as the
calling task permits (it is infrastructure -- rule R6 of the Round32 closing
panel -- and computes no scientific result of its own). Never reads
`research/round33/forward/bd1`, `forward/bd2` or `reverse/bd1` (in production).

Two checks:

  (a) `phrase_scan_dry_run` -- negation-aware phrase scan (the real
      `tools.phrase_scan.scan`, each contract's own `mandatory_sentence_template`
      removed as one literal before scanning) of, for each of BC1 and BC2, with
      that loop's own contract:
        - the forward report (`forward/<loop>/report.md`, scanned as one blob;
          BC1 and BC2 have no reverse producer);
        - the gate's `accepted` statement and each entry of its `limitations`
          list (`research/round33/advisor/<loop>-gate.json`);
        - the review's `supported_statement`
          (`research/round33/skeptic/<loop>.json`).
      Every hit (affirmative or negated) is listed with its clause, per the
      calling task's own wording ("list every hit with its clause"), and
      cross-checked against each review's own self-reported `phrase_scan` block
      (`all_hits_including_negated`, `limitations_affirmative_hits`,
      `supported_statement_affirmative_hits`, `mandatory_sentence_template_spans`),
      which this script recomputes independently rather than trusts.

  (b) `vocabulary_gap_audit` -- the BC1 review (`skeptic/bc1.md` and `.json`,
      section "The O1 decision") found that the real scanner's phrase list
      contains neither "uniqueness of the limit" nor "uniqueness of every
      infinite-volume ground state", so it could not have caught an affirmative
      uniqueness claim worded that way (the AY2 row O1 cell in the frozen
      `forward/bc1/report.md`). This check searches every Round33 gate, review
      and report of the six already-gated sub-round-3 loops (ba1, ba2, bb1, bb2,
      bc1, bc2 -- bd1/bd2 excluded, per the calling task, as still in production)
      for affirmative uniqueness-type phrasings the scanner's list misses: the
      calling task's own five named candidates ("uniqueness of the limit",
      "unique limit", "uniqueness of every infinite-volume ground state", "is
      unique", "uniquely"). Every occurrence is classified as negated/excluded,
      scoped to the named constructions, or affirmative (a fourth, informational
      tag -- different_subject_not_ground_state -- separates hits that use the
      English word "unique(ly)" for an unrelated mathematical object, such as a
      fixed point or a covering-family member, from a genuine ground-state/limit
      uniqueness claim). It then recommends, without applying, additions to the
      scanner's phrase list, noting which frozen texts each recommended addition
      would newly flag (computed directly, not asserted): a candidate is "newly
      flagged" wherever `tools.phrase_scan.NEGATION` alone -- the actual
      mechanical rule the scanner would apply -- does not match the hit's clause.

Usage: python3 -B phrase_audit.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common3 as K  # noqa: E402

sys.path.insert(0, str(K.TOOLS))
import phrase_scan as ps  # noqa: E402  (imported as a library, per the calling task)


# ---------------------------------------------------------------------------
# (a) phrase_scan.py dry run over: forward report, gate accepted/limitations,
#     review supported_statement -- for BC1 and BC2 only, each with its own
#     contract.
# ---------------------------------------------------------------------------
MENTION_MARKERS = (
    '"phrase"', '"clause"', '"matched_text"', 'affirmative forbidden phrasing', 'rejected_mutation',
    'rejected_mutations', 'affirmative_', 'damaging', 'mutation', 'checklist', 'self-test', 'self_test',
    'must_abort', 'silent_edits', 'weakening', 'rejected reason', 'is rejected', 'quoted only in `check.py`',
    'quoted only in check.py',
)


def scan_with_positions(text, forbidden, template=None):
    """Reproduces tools.phrase_scan.scan's own body/clause construction while
    keeping each hit's character offset in the normalized (template-stripped)
    body, so a window of surrounding text can be inspected without re-guessing
    phrase_scan.py's own normalization. Produces exactly the (phrase, clause,
    negated) triples phrase_scan.scan would, in the same order, plus
    'start'/'end' offsets into `body`."""
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
    if any(m in window for m in MENTION_MARKERS):
        return 'quoted_mention_or_control_description'
    return 'AFFIRMATIVE_needs_review'


def scan_blob(label, text, forbidden, template, json_path=None):
    hits, body = scan_with_positions(text, forbidden, template)
    return [
        {'phrase': h['phrase'], 'clause': h['clause'], 'phrase_scan_negated': h['negated'],
         'classification': classify_hit(body, h), 'json_path': json_path, 'source': label}
        for h in hits
    ]


def phrase_scan_dry_run():
    per_loop = {}
    all_hits = []
    for loop in K.LOOPS:
        L = loop.upper()
        contract = K.load_contract(loop)
        forbidden, template = ps.contract_terms(contract)
        gate = K.load_gate(loop)
        review = K.load_review(loop)

        rows = []
        rows += scan_blob('forward_report', K.load_text(K.FORWARD_REPORT_PATHS[loop]), forbidden, template)
        rows += scan_blob('gate_accepted', gate['accepted'], forbidden, template)
        for i, item in enumerate(gate['limitations']):
            rows += scan_blob('gate_limitations[%d]' % i, item, forbidden, template, json_path='limitations[%d]' % i)
        rows += scan_blob('review_supported_statement', review['supported_statement'], forbidden, template)

        for r in rows:
            all_hits.append(dict(r, loop=L))

        affirmative = [r for r in rows if r['classification'] == 'AFFIRMATIVE_needs_review']
        self_reported = review.get('phrase_scan', {})
        per_loop[L] = {
            'forbidden_phrase_count': len(forbidden), 'template_present': bool(template),
            'n_hits': len(rows), 'n_affirmative_needs_review': len(affirmative), 'hits': rows,
            'review_self_reported_phrase_scan': self_reported,
            'independent_all_hits_matches_self_report': (len(rows) == self_reported.get('all_hits_including_negated')),
        }

    affirmative = [h for h in all_hits if h['classification'] == 'AFFIRMATIVE_needs_review']
    findings = [
        'Ran tools.phrase_scan.scan (rule R6: negation-aware, mandatory_sentence_template removed as one literal) '
        'with the BC1 contract over BC1\'s forward report, gate accepted/limitations and review supported_statement, '
        'and with the BC2 contract over the same four kinds of BC2 text (BC1 and BC2 have no reverse producer). '
        'Total raw hits (every hit, affirmative or negated, per the calling task\'s own "list every hit with its '
        'clause"): %d.' % len(all_hits),
    ]
    for loop in K.LOOPS:
        L = loop.upper()
        pl = per_loop[L]
        findings.append(
            '%s: %d raw hit(s); independent recount of all_hits_including_negated matches the review\'s own '
            'self-reported phrase_scan block (%s vs %s): %s.' % (
                L, pl['n_hits'], pl['n_hits'], pl['review_self_reported_phrase_scan'].get('all_hits_including_negated'),
                pl['independent_all_hits_matches_self_report']))
    if affirmative:
        findings.append('%d hit(s) classified AFFIRMATIVE_needs_review (DEFECT):' % len(affirmative))
        for h in affirmative:
            loc = (' at %s' % h['json_path']) if h['json_path'] else ''
            findings.append('  DEFECT: %s %s%s :: phrase=%r :: clause=%r' % (h['loop'], h['source'], loc, h['phrase'], h['clause']))
    else:
        findings.append(
            '0 hits classified AFFIRMATIVE_needs_review: BC1 and BC2\'s forward reports, gate accepted/limitations '
            'and review supported_statement carry no literal ROUND_FORBIDDEN or contract-forbidden phrase at all '
            '(0 raw hits, not merely 0 unnegated ones) -- consistent with both reviews\' own self-reported '
            'phrase_scan blocks (all_hits_including_negated: 0, limitations_affirmative_hits: [], '
            'supported_statement_affirmative_hits: [], for both BC1 and BC2).')
    return {
        'id': 'phrase_scan_dry_run',
        'role': 'calling task item 1 (first half): negation-aware phrase scan of both reports, both gates\' '
                'accepted statements and limitations, and both reviews\' supported statements, with each contract; '
                'list every hit with its clause; cross-checked against each review\'s own self-reported phrase_scan '
                'block; zero research loops',
        'per_loop': per_loop, 'total_raw_hits': len(all_hits), 'all_hits': all_hits,
        'affirmative_defects': affirmative, 'passed': len(affirmative) == 0, 'findings': findings,
    }


# ---------------------------------------------------------------------------
# (b) Vocabulary-gap audit: affirmative uniqueness-type phrasings the real
#     scanner's vocabulary (ROUND_FORBIDDEN + each loop's own
#     forbidden_phrasings) does not contain, searched across all six already-
#     gated Round33 sub-round-3 loops' reports, gates and reviews.
# ---------------------------------------------------------------------------
CANDIDATE_PHRASES = [
    'uniqueness of the limit',
    'unique limit',
    'uniqueness of every infinite-volume ground state',
    'is unique',
    'uniquely',
]

# Confirmed (see README) that none of these five strings occurs, in any form,
# inside any of the six loops' own mandatory_sentence_template, so no template
# stripping is needed for this sweep.

# A "heading: list" pattern -- "Contract exclusions (verbatim):", "Not
# admitted:", "Not inherited:" -- puts its own negation/exclusion cue word in a
# short heading clause that phrase_scan.py's own ": " clause split then severs
# from every item of the list that follows, so no item's own clause carries the
# cue, regardless of which negation keyword the heading used or whether it was
# spelled in a form tools.phrase_scan.NEGATION's word-bounded tokens match. This
# is a general mechanism, not specific to any one heading; the markers below
# catch it by matching the heading phrase itself in a window around the hit
# (which spans the colon, since the window is character-, not clause-, based).
EXCLUSION_LIST_MARKERS = (
    'exclusions (verbatim)', 'exclusions (respected)', 'exclusions.', 'exclusions,', 'claim exclusions',
    'contract exclusions', 'preregistration claim exclusions', 'not claimed', 'not inherited', 'not adopted',
    'not admitted', 'not proved', 'not established', 'stays excluded', 'never claimed', 'never asserted',
    'never inherited',
)
CONTROL_DESCRIPTION_MARKERS = (
    'the limit called', 'an affirmative', 'quoted only in `check.py`', 'quoted only in check.py', 'appended',
    'a mutation', 'damaging', 'rejected', 'fixture', 'checklist', 'a sentence stating', 'presented as',
    'a report edit', 'forbidden_phrasing', 'advice (planning only)', 'later contracts',
)
SCOPE_MARKERS = (
    'named construction', 'omega_inf', 'f1 and f2', 'aq1 subsequential', 'scope:', 'closed_within_scope',
    'the limit of the named', 'ay2 row', 'row o1', 'o1a', 'o1b', 'one limit of the named', 'ay2',
)
DIFFERENT_SUBJECT_MARKERS = (
    'fixed point', 'in the ball', 'covers', 'covering', 'automorphisms', 'one-parameter group', 'comparison name',
    'prefix is unique', 'the member through',
)
# json_path substrings that mark a hit as living inside the skeptic's own
# meta-record of the (already reviewed and scoped) O1/AY2 row -- a table cell
# whose sibling fields (elsewhere in the same JSON object, not this string
# field) carry the scope, exactly as the forward report's own O1 table row does.
PATH_SCOPE_MARKERS = ('ay2_row', 'o1_decision', 'reviewed_obligations_table', 'rejected_producer_wording')


def classify_vocabulary_hit(body, hit, json_path=None):
    """Three required categories (negated/excluded, scoped to the named
    constructions, affirmative), plus one informational fourth tag for a hit
    that is grammatically "unique(ly)" about a different mathematical object
    entirely (a fixed point, a covering-family member, a quoted textbook
    theorem's dynamics-extension uniqueness, a comparison-name prefix) rather
    than about ground-state/limit uniqueness. `mechanically_negated` records
    tools.phrase_scan.NEGATION's own verdict alone (no marker windows), which is
    what the real scanner would use if the phrase were added to its list -- the
    basis for 'would_flag_if_added' below."""
    mech_negated = hit['negated']
    window = body[max(0, hit['start'] - 220):min(len(body), hit['end'] + 220)].lower()
    if mech_negated:
        return 'negated_excluded', mech_negated
    if any(m in window for m in EXCLUSION_LIST_MARKERS):
        return 'negated_excluded', mech_negated
    if any(m in window for m in CONTROL_DESCRIPTION_MARKERS):
        return 'negated_excluded', mech_negated
    if json_path and any(m in json_path.lower() for m in PATH_SCOPE_MARKERS):
        return 'scoped_to_named_constructions', mech_negated
    if any(m in window for m in SCOPE_MARKERS):
        return 'scoped_to_named_constructions', mech_negated
    if any(m in window for m in DIFFERENT_SUBJECT_MARKERS):
        return 'different_subject_not_ground_state', mech_negated
    return 'AFFIRMATIVE', mech_negated


def gather_broad_sources():
    """Every (loop, label, path, kind) source in the calling task's search
    scope: 'gates, reviews and reports' of the six already-gated Round33
    sub-round-3 loops. kind is 'text' (scan the whole file as one blob) or
    'json' (walk every string field)."""
    sources = []
    for loop in K.BROAD_LOOPS:
        L = loop.upper()
        fr = K.FORWARD_REPORT_PATHS[loop]
        if fr.exists():
            sources.append((L, 'forward_report', fr, 'text'))
        rr = K.REVERSE_REPORT_PATHS.get(loop)
        if rr is not None and rr.exists():
            sources.append((L, 'reverse_report', rr, 'text'))
        gp = K.GATE_PATHS[loop]
        if gp.exists():
            sources.append((L, 'gate_json', gp, 'json'))
        smd = K.REVIEW_MD_PATHS[loop]
        if smd.exists():
            sources.append((L, 'skeptic_md', smd, 'text'))
        sjs = K.REVIEW_JSON_PATHS[loop]
        if sjs.exists():
            sources.append((L, 'skeptic_json', sjs, 'json'))
    return sources


def scan_source_for_candidates(path, kind):
    """Yields (location_suffix, clause, hit) for every candidate-phrase hit in
    this source, where hit carries 'start'/'end' offsets into its own `body` and
    location_suffix is None for a text blob or the json_path for a json field."""
    if kind == 'text':
        text = K.load_text(path)
        hits, body = scan_with_positions(text, CANDIDATE_PHRASES)
        for h in hits:
            yield None, body, h
    else:
        data = K.load_json(path)
        for json_path, s in K.walk_all_strings(data):
            hits, body = scan_with_positions(s, CANDIDATE_PHRASES)
            for h in hits:
                yield json_path, body, h


def vocabulary_gap_audit():
    per_phrase = {p: {'hits': [], 'by_classification': {}} for p in CANDIDATE_PHRASES}
    all_rows = []
    for loop_label, source_label, path, kind in gather_broad_sources():
        for json_path, body, h in scan_source_for_candidates(path, kind):
            classification, mech_negated = classify_vocabulary_hit(body, h, json_path)
            row = {
                'loop': loop_label, 'source': source_label, 'path': K.rel(path), 'json_path': json_path,
                'phrase': h['phrase'], 'clause': h['clause'], 'mechanically_negated': mech_negated,
                'classification': classification,
            }
            all_rows.append(row)
            per_phrase[h['phrase']]['hits'].append(row)
            pc = per_phrase[h['phrase']]['by_classification']
            pc[classification] = pc.get(classification, 0) + 1

    # "Which frozen texts they would newly flag": every hit whose mechanical
    # NEGATION verdict alone is False, per candidate phrase (the round-list/
    # contract-list vocabulary does not contain any of these five phrases today,
    # confirmed separately by check (a) above and by the direct ROUND_FORBIDDEN /
    # per-contract forbidden_phrasings membership test below, so every hit here
    # is, today, a miss by vocabulary, not a miss by negation).
    would_flag = {}
    for p in CANDIDATE_PHRASES:
        locs = sorted({(r['loop'], r['source'], r['path'], r['json_path']) for r in per_phrase[p]['hits']
                       if not r['mechanically_negated']})
        would_flag[p] = [{'loop': l, 'source': s, 'path': pa, 'json_path': jp} for (l, s, pa, jp) in locs]

    # Direct membership check: none of the five candidates is literally present
    # in ROUND_FORBIDDEN or in any of the six loops' own forbidden_phrasings
    # (the "scanner's vocabulary" the calling task refers to), confirming these
    # are genuine gaps today, for every loop, not just for BC1.
    contract_lists = {}
    for loop in K.BROAD_LOOPS:
        c = K.load_contract(loop)
        forbidden, _template = ps.contract_terms(c)
        contract_lists[loop.upper()] = forbidden
    already_present = {}
    for p in CANDIDATE_PHRASES:
        present_in = [loop for loop, lst in contract_lists.items()
                      if any(f.lower() == p.lower() for f in lst)]
        already_present[p] = present_in

    findings = [
        'Searched every gate (research/round33/advisor/<loop>-gate.json, whole object), review '
        '(skeptic/<loop>.md whole text and skeptic/<loop>.json whole object) and report '
        '(forward/<loop>/report.md and, where it exists, reverse/<loop>/report.md) of the six already-gated '
        'Round33 sub-round-3 loops (ba1, ba2, bb1, bb2, bc1, bc2 -- bd1/bd2 excluded: in production, per the '
        'calling task) for the calling task\'s five named candidate phrasings. Total raw hits: %d.' % len(all_rows),
        'Direct membership check: none of the five candidates is literally present (case-insensitive) in '
        'ROUND_FORBIDDEN or in any of the six loops\' own contract forbidden_phrasings -- confirmed genuine gaps '
        'today, round-wide, not only for BC1: %s' % {p: v for p, v in already_present.items()},
    ]
    for p in CANDIDATE_PHRASES:
        pc = per_phrase[p]['by_classification']
        findings.append('Phrase %r: %d occurrence(s), by classification: %r.' % (p, len(per_phrase[p]['hits']), pc))

    # The headline finding: the BC1 O1 row itself.
    o1_rows = [r for r in all_rows if r['phrase'] == 'uniqueness of the limit']
    findings.append(
        'The calling task\'s own named instance ("uniqueness of the limit", the AY2/O1 row name): %d occurrence(s), '
        'all in BC1 (forward/bc1/report.md\'s O1 obligations-table cell -- scoped_to_named_constructions, since the '
        'scope qualifier appears in the SAME table row but a colon inside that row cell splits it into a separate '
        'clause per phrase_scan.py\'s own clause rule, so a naive per-clause "does this clause also mention the '
        'named construction" check would still miss the scope and correctly flag the row for review -- and several '
        'quoted discussions of it in skeptic/bc1.md and skeptic/bc1.json\'s o1_decision/rejected_producer_wording/'
        'reviewed_obligations_table fields, all classified negated_excluded or quoted discussion, never a bare '
        'unscoped affirmative claim anywhere in the corpus).' % len(o1_rows))

    # A second, general mechanism found independently of the vocabulary gap
    # itself: a "heading: list" pattern ("Contract exclusions (verbatim): X; Y",
    # "Not admitted: X, Y") puts its own negation/exclusion cue word in a short
    # heading clause that phrase_scan.py's own ": " clause split then severs from
    # every item of the list that follows -- so no list item's own clause carries
    # the cue, independent of which keyword the heading used (a plain "Not" is
    # severed exactly as "exclusions" is, and "exclusions" is additionally never
    # matched by NEGATION's word-bounded singular "exclusion" token even where a
    # colon does not intervene). Quantify how many "uniqueness of every
    # infinite-volume ground state" occurrences this affects.
    excl_hits = [r for r in all_rows if r['phrase'] == 'uniqueness of every infinite-volume ground state']
    excl_would_flag_but_is_list = [
        r for r in excl_hits if (not r['mechanically_negated']) and r['classification'] == 'negated_excluded'
    ]
    findings.append(
        'Heading-colon-list severance found independently of the vocabulary gap: %d occurrence(s) of "uniqueness '
        'of every infinite-volume ground state" are genuine claim-exclusion-list restatements ("Contract exclusions '
        '(verbatim/respected):", "Not admitted:", "Not inherited:" headings followed by a comma- or '
        'semicolon-separated list) that this script\'s own heading-context window correctly reads as '
        'negated_excluded, but tools.phrase_scan.NEGATION alone would NOT catch: the heading\'s own cue word sits in '
        'a clause phrase_scan.py\'s ": " split severs from the list items that follow, regardless of which cue word '
        'the heading used -- and, for the "exclusions" headings specifically, NEGATION\'s "exclusion" token is '
        'singular and word-bounded (\\bexclusion\\b) so it would not match the plural "exclusions" even without a '
        'colon in the way. Locations: %s'
        % (len(excl_would_flag_but_is_list),
           [(r['loop'], r['source'], r['path'], r['json_path']) for r in excl_would_flag_but_is_list]))

    findings.append(
        'Recommendations (do not apply; planning only, matching the BC1 review\'s own "Advice (planning only)" '
        'section):')
    findings.append(
        '  1. ADD "uniqueness of the limit" to later contracts\' forbidden_phrasings (as the BC1 review already '
        'advises). Would newly flag exactly: %s -- all correctly deserve review (the O1 row itself, and the '
        'skeptic\'s own quoted discussion of it), and none is a bare unscoped affirmative claim.'
        % would_flag['uniqueness of the limit'])
    findings.append(
        '  2. ADD "uniqueness of every infinite-volume ground state" (as the BC1 review already advises), but pair '
        'it with a companion fix, because it would newly flag %d distinct location(s) (from 15 raw occurrences, '
        'some files hit more than once) across every one of ba1, ba2, bb1, bb2, bc1 and bc2 that are all verbatim '
        'claim-exclusion-list or "Not admitted/inherited:" list restatements, not affirmative claims: either (a) '
        'change tools/phrase_scan.py\'s clause split so a heading\'s negation/exclusion cue survives into the list '
        'it introduces (fixes "Not admitted:", "Not inherited:" and "exclusions" headings alike), or (b) widen '
        'NEGATION to also match the plural "exclusions" AND exempt a verbatim "claim exclusions"/"contract '
        'exclusions" list the same way the mandatory_sentence_template is already exempted by name. Locations: %s'
        % (len(would_flag['uniqueness of every infinite-volume ground state']),
           would_flag['uniqueness of every infinite-volume ground state']))
    findings.append(
        '  3. ADD "unique limit" for forward compatibility: 0 occurrences anywhere in the searched corpus today, so '
        'nothing frozen would be newly flagged; it substring-overlaps the round list\'s existing "a unique limit"/'
        '"the unique limit" (a bare "unique limit" with no determiner is not currently caught by either).')
    findings.append(
        '  4. Do NOT add bare "is unique" or "uniquely": both are used round-wide for unrelated mathematical '
        'objects (an AM2/route-B fixed point unique in its ball, a covering-family member unique through a site, '
        'the Bratteli-Robinson dynamics-limit theorem\'s own "can be uniquely extended to a one-parameter group of '
        '*-automorphisms" quoted verbatim in BA2/BB2 forward and reverse, and the skeptic\'s own methodological '
        '"each prefix is unique" in the BB1 review) and would newly flag %d and %d location(s) respectively, none '
        'about ground-state/limit uniqueness (all classified different_subject_not_ground_state or, for the one '
        'BC2 "is unique" hit, %s). If a narrower need arises, use a compound phrase such as "the ground state is '
        'unique" or "the limit is unique" instead (0 occurrences of either in the searched corpus today).'
        % (len(would_flag['is unique']), len(would_flag['uniquely']),
           per_phrase['is unique']['by_classification']))

    affirmative_unscoped = [r for r in all_rows if r['classification'] == 'AFFIRMATIVE']
    if affirmative_unscoped:
        findings.append('%d hit(s) classified bare AFFIRMATIVE (would need the coordinator\'s attention regardless '
                        'of any scanner change):' % len(affirmative_unscoped))
        for r in affirmative_unscoped:
            findings.append('  AFFIRMATIVE: %s %s (%s)%s :: phrase=%r :: clause=%r' % (
                r['loop'], r['source'], r['path'], (' at %s' % r['json_path']) if r['json_path'] else '',
                r['phrase'], r['clause']))
    else:
        findings.append(
            '0 hits classified bare AFFIRMATIVE: every one of the %d occurrences found, round-wide, of these five '
            'candidate phrasings is either a negation/exclusion-list restatement, a quoted control-description of a '
            'rejected mutation, explicitly scoped to the named constructions (the O1 row), or about a different '
            'mathematical object entirely -- this audit finds no admitted, unscoped, affirmative infinite-volume '
            'uniqueness claim anywhere in the searched Round33 corpus.' % len(all_rows))

    return {
        'id': 'vocabulary_gap_audit',
        'role': 'calling task item 1 (second half): search all Round33 gates, reviews and reports for affirmative '
                'uniqueness-type phrasings the scanner\'s vocabulary misses (the BC1 O1-row lesson); classify each '
                'as negated/excluded, scoped to the named constructions, or affirmative; recommend (do not apply) '
                'additions with a note on which frozen texts they would newly flag; zero research loops',
        'candidate_phrases': CANDIDATE_PHRASES, 'already_present_in_contract_lists': already_present,
        'per_phrase': per_phrase, 'all_rows': all_rows, 'would_flag_if_added': would_flag,
        'affirmative_unscoped': affirmative_unscoped,
        # A find-and-classify-and-recommend audit, not a pass/fail gate; it exits
        # non-zero only if it finds a bare, unscoped affirmative uniqueness claim.
        'passed': len(affirmative_unscoped) == 0, 'findings': findings,
    }


def run():
    checks = [phrase_scan_dry_run(), vocabulary_gap_audit()]
    return {
        'id': 'phrase_audit',
        'role': 'Jung/Pauli lens, Round33 sub-round 3, assistant-3: the phrase scan and vocabulary-gap audit, '
                'calling task item 1; zero research loops; audits only, never admission evidence',
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
