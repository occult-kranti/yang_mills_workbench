#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 applications stage, assistant-4 script 3 of 3:
calling task item 3 -- the applications-ledger audit of
`findings.json#/applications`.

Counts zero research loops. Not a producer, contract, gate or skeptical
review; nothing computed here is read back into any of those. Human project
author: Hruday N M (BUNZEEY); AI-assisted. Standard library only
(`json`, `re`, `hashlib`). Does not import `forward/*/check.py`,
`reverse/*/check.py`, or any other producer/skeptic module.

Three sub-checks over every entry of `findings.json#/applications`:

  (a) `schema_check` -- every entry has `loop_id` in {"bd1", "bd2"}, and
      non-empty `problem`, `equation`, `outcome`, `model`, `kind` (in
      {"transfer", "obstruction", "partial"}) and `sources` (a non-empty
      list).

  (b) `sources_bound_by_gate_check` -- every path in an entry's `sources` is
      a key of that entry's own loop's gate `bindings` dict (BD1 entries
      against `advisor/bd1-gate.json#/bindings`, BD2 entries against
      `advisor/bd2-gate.json#/bindings`), and the sha256 the gate bound for
      that path equals the sha256 of the file on disk today -- i.e. the
      ledger's cited evidence is exactly the byte-identical text the gate
      admitted, not a since-edited copy (the repository's own historical-
      immutability rule, re-verified here rather than assumed).

  (c) `numbers_cross_check` -- every entry's outcome/equation/detail text is
      scanned for exact fraction tokens (`\\d+/\\d+`, word-bounded) and for
      decimal-scientific-notation preview tokens (`\\d+(\\.\\d+)?e-?\\d+`).
      Every fraction token must appear verbatim in that entry's gate's
      `accepted`+`decision` text (exact match: the ledger states the same
      exact rational the gate does). Every decimal-preview token must match,
      within 5% relative tolerance, some decimal-preview token the gate text
      itself carries (the ledger is allowed a coarser rounding than the
      gate's own preview, and this check confirms it is still the same
      number, not merely present).

Usage: python3 -B applications_ledger_audit.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common4 as K  # noqa: E402

REQUIRED_KEYS = ('loop_id', 'problem', 'equation', 'outcome', 'model', 'kind', 'sources')
ALLOWED_KINDS = {'transfer', 'obstruction', 'partial'}


def load_applications():
    findings = K.load_findings()
    return findings['applications']


# ---------------------------------------------------------------------------
# (a) schema_check
# ---------------------------------------------------------------------------
def schema_check():
    apps = load_applications()
    rows = []
    for i, e in enumerate(apps):
        missing = [k for k in REQUIRED_KEYS if k not in e]
        empty = [k for k in REQUIRED_KEYS if k in e and not e[k]]
        loop_ok = e.get('loop_id') in K.LOOPS
        kind_ok = e.get('kind') in ALLOWED_KINDS
        sources_ok = isinstance(e.get('sources'), list) and len(e.get('sources', [])) > 0
        ok = (not missing) and (not empty) and loop_ok and kind_ok and sources_ok
        rows.append({
            'index': i, 'problem': e.get('problem'), 'loop_id': e.get('loop_id'), 'kind': e.get('kind'),
            'missing_keys': missing, 'empty_keys': empty, 'loop_id_ok': loop_ok, 'kind_ok': kind_ok,
            'sources_ok': sources_ok, 'passed': ok,
        })
    defects = [r for r in rows if not r['passed']]
    findings = [
        'Checked all %d findings.json#/applications entries for loop_id in {bd1, bd2}, non-empty problem/'
        'equation/outcome/model, kind in {transfer, obstruction, partial}, and a non-empty sources list.'
        % len(rows),
        'By loop_id: %s. By kind: %s.'
        % ({loop: sum(1 for r in rows if r['loop_id'] == loop) for loop in K.LOOPS},
           {k: sum(1 for r in rows if r['kind'] == k) for k in sorted(ALLOWED_KINDS)}),
    ]
    if defects:
        findings.append('%d schema defect(s):' % len(defects))
        for d in defects:
            findings.append('  DEFECT: entry[%d] %r :: missing=%s empty=%s loop_id_ok=%s kind_ok=%s sources_ok=%s'
                            % (d['index'], d['problem'], d['missing_keys'], d['empty_keys'], d['loop_id_ok'],
                               d['kind_ok'], d['sources_ok']))
    else:
        findings.append('0 schema defects: every entry carries all seven required fields, non-empty, with '
                        'loop_id and kind from the allowed sets.')
    return {
        'id': 'schema_check',
        'role': 'calling task item 3 (first part): every applications entry has loop_id bd1/bd2, problem, '
                'equation, outcome, model, kind in {transfer, obstruction, partial}, and sources; zero research '
                'loops',
        'rows': rows, 'passed': len(defects) == 0, 'findings': findings,
    }


# ---------------------------------------------------------------------------
# (b) sources_bound_by_gate_check
# ---------------------------------------------------------------------------
def sources_bound_by_gate_check():
    apps = load_applications()
    gates = {loop: K.load_gate(loop) for loop in K.LOOPS}
    rows = []
    for i, e in enumerate(apps):
        loop_id = e.get('loop_id')
        gate = gates.get(loop_id)
        bindings = gate['bindings'] if gate else {}
        for src in e.get('sources', []):
            in_bindings = src in bindings
            file_path = K.ROOT / src
            file_exists = file_path.exists()
            actual_sha256 = K.sha256_file(file_path) if file_exists else None
            bound_sha256 = bindings.get(src)
            sha_match = file_exists and in_bindings and (actual_sha256 == bound_sha256)
            rows.append({
                'entry_index': i, 'loop_id': loop_id, 'source': src, 'in_gate_bindings': in_bindings,
                'file_exists': file_exists, 'bound_sha256': bound_sha256, 'actual_sha256': actual_sha256,
                'sha256_match': sha_match, 'passed': in_bindings and file_exists and sha_match,
            })
    defects = [r for r in rows if not r['passed']]
    findings = [
        'Checked every source path of every applications entry against that entry\'s own loop\'s gate '
        '(advisor/bd1-gate.json or bd2-gate.json)#/bindings: the path must be a bindings key, the file must '
        'exist on disk, and its sha256 today must equal the sha256 the gate bound -- confirming the ledger cites '
        'exactly the byte-identical, gate-admitted text (historical immutability), not a since-edited copy. '
        '%d source citation(s) checked across %d entries.' % (len(rows), len(apps)),
    ]
    by_source = {}
    for r in rows:
        by_source.setdefault(r['source'], []).append(r['loop_id'])
    findings.append('Distinct sources cited: %s' % sorted(by_source.keys()))
    if defects:
        findings.append('%d defect(s):' % len(defects))
        for d in defects:
            findings.append('  DEFECT: entry[%d] (%s) source=%r in_bindings=%s file_exists=%s sha256_match=%s '
                            'bound=%s actual=%s' % (d['entry_index'], d['loop_id'], d['source'], d['in_gate_bindings'],
                                                     d['file_exists'], d['sha256_match'], d['bound_sha256'], d['actual_sha256']))
    else:
        findings.append('0 defects: every cited source is a key of its own loop\'s gate bindings, exists on '
                        'disk, and its current sha256 matches the sha256 the gate bound at freeze time.')
    return {
        'id': 'sources_bound_by_gate_check',
        'role': 'calling task item 3 (second part): every applications entry\'s sources are bound by its own '
                'gate\'s bindings (sha256 match); zero research loops',
        'rows': rows, 'passed': len(defects) == 0, 'findings': findings,
    }


# ---------------------------------------------------------------------------
# (c) numbers_cross_check
# ---------------------------------------------------------------------------
FRAC_RE = re.compile(r'(?<![\w.])-?\d[\d,]*\s*/\s*\d[\d,]*(?![\w])')
DEC_RE = re.compile(r'(?<![\w.])-?\d+\.\d+e-?\d+(?![\w])|(?<![\w.])-?\d+e-?\d+(?![\w])', re.I)
REL_TOL = 0.05


def clean_tok(tok):
    return tok.strip().strip(',.;:').replace(' ', '')


def numbers_cross_check():
    apps = load_applications()
    gates = {loop: K.load_gate(loop) for loop in K.LOOPS}
    rows = []
    for i, e in enumerate(apps):
        gate = gates[e['loop_id']]
        gate_text = gate['accepted'] + ' ' + gate['decision']
        gate_text_nospace = gate_text.replace(' ', '')
        gate_decs = []
        for m in DEC_RE.finditer(gate_text):
            try:
                gate_decs.append(float(clean_tok(m.group())))
            except ValueError:
                pass

        blob = ' '.join([e.get('outcome', ''), e.get('equation', ''), e.get('detail', '')])
        fracs = sorted({clean_tok(f) for f in FRAC_RE.findall(blob)})
        decs = sorted({clean_tok(f) for f in DEC_RE.findall(blob)})

        frac_missing = [f for f in fracs if f not in gate_text_nospace]
        dec_unmatched = []
        dec_matches = {}
        for dtok in decs:
            try:
                val = float(dtok)
            except ValueError:
                dec_unmatched.append(dtok)
                continue
            matches = [gv for gv in gate_decs if val != 0 and abs(gv - val) / abs(val) < REL_TOL]
            if matches:
                dec_matches[dtok] = matches[:3]
            else:
                dec_unmatched.append(dtok)

        ok = (not frac_missing) and (not dec_unmatched)
        rows.append({
            'index': i, 'problem': e.get('problem'), 'loop_id': e.get('loop_id'),
            'fraction_tokens': fracs, 'fraction_tokens_missing_from_gate_text': frac_missing,
            'decimal_preview_tokens': decs, 'decimal_matches_in_gate_text': dec_matches,
            'decimal_tokens_unmatched': dec_unmatched, 'passed': ok,
        })
    defects = [r for r in rows if not r['passed']]
    n_fracs = sum(len(r['fraction_tokens']) for r in rows)
    n_decs = sum(len(r['decimal_preview_tokens']) for r in rows)
    findings = [
        'Extracted every word-bounded fraction token (e.g. "1/144") and decimal-scientific-notation preview '
        'token (e.g. "1.34e-12") from each entry\'s outcome+equation+detail text: %d fraction token(s) and %d '
        'decimal-preview token(s) across %d entries. Every fraction token is checked for an exact (whitespace-'
        'stripped) substring match in that entry\'s own gate\'s accepted+decision text; every decimal-preview '
        'token is checked for a same-magnitude match (relative tolerance %.0f%%) against some decimal-preview '
        'token the gate text itself carries, since the ledger is allowed a coarser rounding of the gate\'s own '
        'preview (e.g. the ledger\'s "2.88e-19" against the gate\'s "2.87586637818e-19").'
        % (n_fracs, n_decs, len(apps), REL_TOL * 100),
    ]
    for r in rows:
        if r['fraction_tokens'] or r['decimal_preview_tokens']:
            findings.append('  entry[%d] (%s, %s): fractions=%s decimals=%s -> decimal matches=%s'
                            % (r['index'], r['loop_id'], r['problem'][:30], r['fraction_tokens'],
                               r['decimal_preview_tokens'], r['decimal_matches_in_gate_text']))
    if defects:
        findings.append('%d entr(y/ies) with an unsupported number (DEFECT):' % len(defects))
        for d in defects:
            findings.append('  DEFECT: entry[%d] (%s) fractions_missing=%s decimals_unmatched=%s'
                            % (d['index'], d['problem'], d['fraction_tokens_missing_from_gate_text'],
                               d['decimal_tokens_unmatched']))
    else:
        findings.append('0 unsupported numbers: every fraction token in the ledger appears verbatim in its own '
                        'gate\'s accepted+decision text, and every decimal preview matches a gate-text preview of '
                        'the same magnitude -- the applications ledger\'s numbers are the gate\'s own numbers, not '
                        're-derived or re-rounded incorrectly.')
    return {
        'id': 'numbers_cross_check',
        'role': 'calling task item 3 (third part): cross-check each applications entry\'s numbers against its '
                'gate text; zero research loops',
        'rows': rows, 'passed': len(defects) == 0, 'findings': findings,
    }


def run():
    checks = [schema_check(), sources_bound_by_gate_check(), numbers_cross_check()]
    return {
        'id': 'applications_ledger_audit',
        'role': 'Jung/Pauli lens, Round33 applications stage, assistant-4: the applications-ledger audit of '
                'findings.json#/applications, calling task item 3; zero research loops; audits only, never '
                'admission evidence',
        'checks': {c['id']: c for c in checks},
        'passed': all(c['passed'] for c in checks),
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'applications_ledger_audit', result)
    print('applications_ledger_audit: %s' % ('PASS' if result['passed'] else 'FAIL (see findings)'))
    for check_id, c in result['checks'].items():
        print('  %s: %s' % (check_id, 'PASS' if c['passed'] else 'FAIL'))
        for f in c['findings']:
            print('    -', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
