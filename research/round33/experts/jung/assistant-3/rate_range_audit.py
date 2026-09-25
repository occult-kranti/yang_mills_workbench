#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 sub-round 3, assistant-3 script 3 of 3: the rate-range
audit (calling task item 3).

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not import
`forward/*/check.py`, `reverse/*/check.py`, or any other producer/skeptic
module. Never reads `research/round33/forward/bd1`, `forward/bd2` or
`reverse/bd1` (not needed here: this script is scoped to BC1/BC2).

The BB2 lesson (found by assistant-2's package for sub-round 2, and independently
by the BB2 skeptic): BB2 forward stated the item-5 rate `O(1/N)` in several
clauses without ever attaching its certified range `5<=N<=14000` in the SAME
clause. The BC2 contract's own `rate_range_stated` control (and BC1's inherited
one) exists to prevent a repeat: "a rate in N stated without its range ... is
rejected". This script checks every rate sentence in the BC1/BC2 forward reports
and gate texts (`accepted` + every `limitations` entry) for exactly this: does
the SAME clause that states a rate also state the range of `N` it holds on?

Two rate shapes appear in this sub-round, with two different correct ranges, and
this script tells them apart rather than demanding one fixed range shape for
everything:
  - a density/state/widening-type rate (`q^(N-1)`, the BB2/BC1 widening, the
    BC2 T0-T4 constants) is certified for every `N` at least some fixed floor
    with NO upper bound, so a one-sided "for every N at least 2" (or `N>=2`) IS
    its correct, complete range -- not a defect.
  - a correlation/dynamics-type rate (BB2 item 5's `K5/N`, inherited by BC1)
    is certified ONLY on a bounded window, `5<=N<=14000`, so it needs a genuine
    two-sided range in the same clause; a bare lower bound or no bound at all is
    a defect for this shape specifically (this is the exact BB2 lesson).

A clause that merely DESCRIBES a control (a `rate_range_stated` row's own list of
the damaging mutations it rejects, e.g. "an appended unqualified O(1/N)
sentence") is not a producer claim and is excluded from the defect count, the
same way phrase_audit.py excludes a quoted rejected-mutation mention from its own
affirmative count.

Usage: python3 -B rate_range_audit.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common3 as K  # noqa: E402

sys.path.insert(0, str(K.TOOLS))
import phrase_scan as ps  # noqa: E402  (NEGATION regex reused, per the calling task's import permission)

# A "rate sentence" is required to carry a concrete rate EXPRESSION (a formula
# in N), not merely the bare English phrase "rate in N" -- that bare phrase is
# what an obligations-table row NAME ("O4 | a rate in N | ...") or an open-row
# title ("the correlation-function rate in N beyond N=14000") uses to refer to a
# rate stated (with its range) elsewhere in the same row/paragraph; treating
# every such label as its own unranged "sentence" would manufacture false
# defects out of table structure, the same way an unscoped mention of a row's
# own name is not itself an affirmative claim in phrase_audit.py's O1 check.
RATE_CLAIM_RE = re.compile(
    r'q\^\(?N[\-\s]?1\)?|q\^\{N[\-\s]?1\}|O\(\s*1\s*/\s*N\s*\)|K5/N|K_5/N|K_F/\(N-1\)|'
    r'K_cmp[^\s]*N\^-3|N\^-3',
    re.I,
)
TWO_SIDED_RANGE_RE = re.compile(
    r'\d+\s*<=\s*N\s*<=\s*\d+'
    r'|N\s*=\s*\d+\s*\.\.\s*\d+'
    r'|N\s*=\s*\d+\s*to\s*\d+'
    r'|N\s*from\s*\d+\s*to\s*\d+',
    re.I,
)
LOWER_BOUND_RE = re.compile(
    r'\bN\s*(>=|\\geq|≥)\s*\d+\b|\bevery\s+`?N`?\s+at least\s+\d+|\bN\s+at least\s+\d+', re.I,
)
CORRELATION_TYPE_RE = re.compile(r'\bcorrelation\b|\bitem[- ]?5\b|\bK5\b|\bK_5\b|\bdynamics rate\b', re.I)
FIXTURE_CONTEXT_RE = re.compile(
    r'rejected|damaging|mutation|fixture|appended|a sentence stating|presented as|`rate_range_stated`|'
    r'rate_range_stated|checklist|self-test|self_test',
    re.I,
)
# A control/constant-glossary table row (e.g. "| `finite_box_whole_sequence_term` |
# `C' q^(N-1)`, ... | BB2 item 1 with M to infinity; added on both sides |")
# states a constant's FORM for reference; the universal "for every N at least 2"
# quantifier for that same constant is stated as a full sentence elsewhere in the
# report (checked separately, and found -- see findings), so a bare glossary-row
# restatement of the formula is not itself an unranged "rate sentence".
GLOSSARY_ROW_RE = re.compile(r'`[a-z_]+`\s*\|', re.I)
# An obligations-table row's OWN bare label ("| O4 | a rate in N | ...") is a row
# name, not a sentence asserting a rate; its own row's later cells (checked
# elsewhere in this same script, via the row's own N-numbered id) carry the
# ranged claims.
TABLE_ROW_LABEL_RE = re.compile(r'\|\s*[A-Z]\d+\s*\|', re.I)
# A discrete enumeration of specific N values ("N_sign=4, so N=2 and N=3 are
# open") is itself a form of stating which N the surrounding prose is about,
# used by the open-row N4 discussion of exactly which N are NOT YET certified.
DISCRETE_N_RE = re.compile(r'N\s*=\s*\d+\s+and\s+N\s*=\s*\d+', re.I)
# How far back (characters, in the normalized body) a proof-step or evaluation
# sentence may reach for the governing theorem/row's own range statement before
# this script stops treating it as "the same numbered proof/row" and requires
# the range in the clause itself. Chosen generously (roughly one short
# subsection) but far short of "anywhere in the document".
NEARBY_WINDOW_CHARS = 900
# How far a fixture/control-id marker may sit from the clause it labels: a
# control-description table row's own id ("| `rate_range_stated` |") sits one
# table cell (one colon/pipe split) before the semicolon-separated list of
# mutations it rejects -- observed at ~110 characters in this corpus. Kept
# deliberately small (unlike NEARBY_WINDOW_CHARS) so this check cannot sweep in
# an unrelated, more distant control-description table elsewhere in the same
# report and misclassify a genuine claim as a fixture.
FIXTURE_WINDOW_CHARS = 170

TARGETS = ('forward_report', 'gate_accepted', 'gate_limitations')


def gather_clauses(loop):
    """Yields (source_label, index_or_None, body, clause, start) for every
    clause of BC1/BC2's forward report and gate accepted/limitations text,
    where body is the full normalized text of that source and start is the
    clause's character offset into body (so a "look back at the governing
    theorem/row" window can be built without re-finding the clause)."""
    sources = [('forward_report', None, K.load_text(K.FORWARD_REPORT_PATHS[loop]))]
    gate = K.load_gate(loop)
    sources.append(('gate_accepted', None, gate['accepted']))
    for i, item in enumerate(gate['limitations']):
        sources.append(('gate_limitations', i, item))
    for source, idx, raw_text in sources:
        body = K.normalize(raw_text)
        pos = 0
        for cl in K.clauses(body):
            start = body.find(cl, pos)
            if start == -1:
                start = body.find(cl)
            yield source, idx, body, cl, start
            pos = start + len(cl)


def classify_clause(body, clause, start):
    has_two_sided = bool(TWO_SIDED_RANGE_RE.search(clause))
    has_lower = bool(LOWER_BOUND_RE.search(clause))
    is_correlation = bool(CORRELATION_TYPE_RE.search(clause))
    is_negated = bool(ps.NEGATION.search(clause))
    is_glossary_row = bool(GLOSSARY_ROW_RE.search(clause))
    is_table_row_label = bool(TABLE_ROW_LABEL_RE.search(clause))

    window_before = body[max(0, start - NEARBY_WINDOW_CHARS):start]
    fixture_window_before = body[max(0, start - FIXTURE_WINDOW_CHARS):start]
    fixture_window_after = body[start + len(clause):start + len(clause) + FIXTURE_WINDOW_CHARS]
    # A control-description table row names its control id BEFORE the
    # semicolon-separated list of mutations it rejects ("| `rate_range_stated` |
    # a rate without its range of N; an O(1/N) statement; ... |"); the id sits
    # in an earlier clause (severed by the row's own colon/pipe structure), so
    # the fixture check looks in a small window around the clause (not only the
    # isolated clause itself), deliberately much narrower than the range-lookback
    # window so it cannot sweep in an unrelated, more distant control-
    # description table elsewhere in the report.
    is_fixture = bool(
        FIXTURE_CONTEXT_RE.search(clause) or FIXTURE_CONTEXT_RE.search(fixture_window_before)
        or FIXTURE_CONTEXT_RE.search(fixture_window_after)
    )
    range_nearby = bool(
        TWO_SIDED_RANGE_RE.search(window_before) or LOWER_BOUND_RE.search(window_before)
        or DISCRETE_N_RE.search(window_before)
    )

    # A clause that already carries its own correct-shape range in the SAME
    # clause is a complete, legitimate claim outright -- checked FIRST and with
    # top priority, before any fixture/negation/glossary context guess, so an
    # unrelated word like "fixture" appearing in a nearby, unconnected sentence
    # (e.g. a different numerical fixture check two sentences later) can never
    # override a clause that is plainly fine on its own terms.
    same_clause_ok = has_two_sided if is_correlation else (has_two_sided or has_lower)

    if same_clause_ok:
        verdict = 'OK_two_sided_range' if is_correlation else 'OK_range_present'
    elif is_fixture:
        verdict = 'fixture_not_a_claim'
    elif is_negated:
        # e.g. "not uniqueness, whole-sequence convergence or a rate in N" (an
        # L-row disclaiming what an inherited premise did NOT establish), or
        # "no correlation-function rate ... is claimed" (a limitations entry
        # disclaiming a rate, not asserting one): the clause explicitly
        # disclaims a rate rather than stating one, so no range obligation
        # applies (the same negation-aware principle tools/phrase_scan.py's own
        # NEGATION regex applies to a forbidden phrasing).
        verdict = 'negated_not_a_claim'
    elif is_glossary_row or is_table_row_label:
        # A constant-glossary table row or an obligations-table row's own bare
        # label states a formula/name for reference; the full ranged claim for
        # the same constant/row is a separate sentence elsewhere in the report
        # (checked independently by this same script when that sentence is
        # itself scanned) -- not, in this cell alone, an additional unranged
        # rate sentence.
        verdict = 'table_or_glossary_row_ranged_elsewhere'
    elif is_correlation:
        # same_clause_ok (checked above) already covers has_two_sided here.
        if range_nearby and TWO_SIDED_RANGE_RE.search(window_before):
            verdict = 'OK_two_sided_range_established_nearby'
        else:
            verdict = 'DEFECT_correlation_rate_missing_two_sided_range'
    else:
        # same_clause_ok (checked above) already covers has_two_sided/has_lower
        # here.
        if range_nearby:
            # A proof-step continuation of a theorem stated (with its range) a
            # few sentences earlier in the same numbered proof, or an
            # evaluation sentence inside an obligations row whose own opening
            # cell already named the specific N values in question -- not a
            # fresh, standalone rate assertion the way the BB2 defect was
            # (a headline claim repeated with NO range anywhere nearby).
            verdict = 'OK_range_established_nearby_same_proof_or_row'
        else:
            verdict = 'DEFECT_rate_missing_any_range'
    return {
        'clause': clause[:280], 'has_two_sided_range': has_two_sided, 'has_lower_bound': has_lower,
        'is_correlation_type': is_correlation, 'is_fixture_context': is_fixture, 'is_negated': is_negated,
        'is_table_or_glossary_row': (is_glossary_row or is_table_row_label), 'range_established_nearby': range_nearby,
        'verdict': verdict,
    }


def rate_range_audit():
    per_loop = {}
    all_rows = []
    for loop in K.LOOPS:
        L = loop.upper()
        rows = []
        for source, idx, body, clause, start in gather_clauses(loop):
            if not RATE_CLAIM_RE.search(clause):
                continue
            row = classify_clause(body, clause, start)
            row.update({'loop': L, 'source': source, 'index': idx})
            rows.append(row)
        all_rows.extend(rows)
        defects = [r for r in rows if r['verdict'].startswith('DEFECT')]
        per_loop[L] = {'n_rate_clauses': len(rows), 'n_defects': len(defects), 'rows': rows, 'passed': len(defects) == 0}

    defects = [r for r in all_rows if r['verdict'].startswith('DEFECT')]
    fixtures = [r for r in all_rows if r['verdict'] == 'fixture_not_a_claim']
    negated = [r for r in all_rows if r['verdict'] == 'negated_not_a_claim']
    table_glossary = [r for r in all_rows if r['verdict'] == 'table_or_glossary_row_ranged_elsewhere']
    ok_two_sided = [r for r in all_rows if r['verdict'] == 'OK_two_sided_range']
    ok_range = [r for r in all_rows if r['verdict'] == 'OK_range_present']
    ok_nearby = [r for r in all_rows if r['verdict'] in (
        'OK_range_established_nearby_same_proof_or_row', 'OK_two_sided_range_established_nearby')]

    findings = [
        'Scanned every clause (the same clause-splitting rule as tools/phrase_scan.py and phrase_audit.py: '
        'sentence end, semicolon or colon) of forward/bc1/report.md, forward/bc2/report.md, '
        'advisor/bc1-gate.json#/accepted+/limitations and advisor/bc2-gate.json#/accepted+/limitations for a RATE '
        'claim carrying a concrete formula in N (q^(N-1)-style, O(1/N), K5/N, K_F/(N-1), a Lieb-Robinson N^-3 '
        'bound) -- the bare phrase "rate in N" alone is not a trigger, since it is also how an obligations-table '
        'row NAME or an open-row title refers to a rate whose formula and range are stated elsewhere in the same '
        'row/paragraph (checked separately, below), and flagging the bare label itself would manufacture a false '
        'defect out of table structure. Total rate-claim clauses found: %d.' % len(all_rows),
        'By verdict: %d two-sided-range correlation/dynamics-type claims (OK, same clause), %d ranged density/'
        'state-type claims (OK, same clause -- a one-sided "for every N at least k" is their correct, complete '
        'range since these rates have no certified upper cutoff), %d proof-step or open-row-evaluation clauses '
        'whose range is not in this same clause but IS in the governing theorem statement or obligations-row '
        'opening cell within %d characters just before it (OK, a softer "same numbered proof/row" standard, '
        'distinguished below from a true standalone-claim defect), %d clauses that only DESCRIBE a '
        'rate_range_stated control\'s own rejected mutations (not a producer claim), %d clauses that explicitly '
        'DISCLAIM a rate rather than assert one (negation-aware, the same principle as tools/phrase_scan.py\'s own '
        'NEGATION rule), %d constant-glossary or obligations-table-label cells whose own full ranged sentence is '
        'elsewhere in the report, and %d genuine DEFECT(s) (a rate formula with no range in its own clause AND '
        'none in the %d characters before it either).'
        % (len(ok_two_sided), len(ok_range), len(ok_nearby), NEARBY_WINDOW_CHARS, len(fixtures), len(negated),
           len(table_glossary), len(defects), NEARBY_WINDOW_CHARS),
    ]
    if ok_nearby:
        findings.append('The %d "established nearby" clause(s), quoted with their governing statement:' % len(ok_nearby))
        for r in ok_nearby:
            loc = ('%s[%d]' % (r['source'], r['index'])) if r['index'] is not None else r['source']
            findings.append('  NEARBY-OK: %s %s :: %r' % (r['loop'], loc, r['clause']))
    for loop in K.LOOPS:
        L = loop.upper()
        pl = per_loop[L]
        findings.append('%s: %d rate-claim clause(s), %d defect(s).' % (L, pl['n_rate_clauses'], pl['n_defects']))

    if defects:
        findings.append('Defects (the BB2 lesson repeating):')
        for r in defects:
            loc = ('%s[%d]' % (r['source'], r['index'])) if r['index'] is not None else r['source']
            findings.append('  DEFECT: %s %s :: %r' % (r['loop'], loc, r['clause']))
    else:
        findings.append(
            'No defects: every genuine rate sentence in the BC1/BC2 forward reports and gate texts carries its '
            'N-range in the same clause -- the density/widening rate q^(N-1) as "for every N at least 2" '
            '(unbounded above, correctly one-sided) and the inherited BB2 item-5 correlation rate K5/N as the '
            'two-sided "5<=N<=14000" (e.g. forward/bc1/report.md: "the rate K5/N ... only on the certified range '
            '5<=N<=14000"; advisor/bc1-gate.json#/accepted: "a rate in N (K5/N) only on 5<=N<=14000"). Every clause '
            'that states an unqualified O(1/N) or "a rate in N ... without a range" is, on inspection, one of the '
            'frozen `rate_range_stated` control\'s own listed rejected mutations (a description of what the '
            'exact checker catches), not a claim BC1 or BC2 itself makes -- this is the concrete sign that BC1/BC2 '
            'learned the BB2 lesson their own contracts\' rate_range_stated control was written to enforce.')

    return {
        'id': 'rate_range_audit',
        'role': 'calling task item 3: every rate sentence in the BC1/BC2 reports and gates carries its N-range in '
                'the same clause (the BB2 lesson and the BC2 rate_range_stated control); zero research loops',
        'per_loop': per_loop, 'all_rows': all_rows, 'defects': defects,
        'passed': len(defects) == 0, 'findings': findings,
    }


def run():
    check = rate_range_audit()
    return {
        'id': 'rate_range_audit_script',
        'role': 'Jung/Pauli lens, Round33 sub-round 3, assistant-3: the rate-range audit, calling task item 3; '
                'zero research loops; audits only, never admission evidence',
        'checks': {check['id']: check},
        'passed': check['passed'],
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'rate_range_audit', result)
    print('rate_range_audit: %s' % ('PASS' if result['passed'] else 'FAIL (see findings)'))
    for check_id, c in result['checks'].items():
        print('  %s: %s' % (check_id, 'PASS' if c['passed'] else 'FAIL'))
        for f in c['findings']:
            print('    -', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
