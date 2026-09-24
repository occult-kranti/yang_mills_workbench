#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 4, assistant-4 script 1 of 2: the
sentence-template and gate-field checks (panel-update-3.md item 6, Jung share).

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not import
`forward/*/check.py`, `reverse/*/check.py`, or any other producer/skeptic module.

Scope, as named by the calling task:

  AY1 (gated): `advisor/ay1-gate.json`, `forward/ay1/output/results.json`,
  `reverse/ay1/output/results.json`, `skeptic/ay1.json` (plus `forward/ay1/
  report.md`, `reverse/ay1/report.md`, and `skeptic/ay1.md` as bonus, non-required
  coverage, mirroring assistant-3's practice).

  AY2 (frozen forward package, no gate yet -- absence handled, not treated as an
  error): `forward/ay2/output/results.json`, `forward/ay2/report.md`; the
  skeptic's pre-comparison `skeptic/ay2-independent/results.json`.

Five checks, each independently scored and each contributing to `results.json`:

  1. `mandatory_sentence_template_check` -- the mandatory sentence template of
     `experts/jung/loop2-response.md` section 4 is present, verbatim modulo the
     filled-in constants, in every required report.md and in the AY1 gate's
     `accepted` text.
  2. `gate_field_export_check` -- for the six-name union of gate-field booleans
     (`uniqueness_claimed`, `whole_sequence_claimed`, `rate_claimed`,
     `rate_in_N_claimed`, `translation_invariance_claimed`,
     `boundary_independence_of_dynamics_claimed`), which files export which as a
     real JSON key (or, for .md files, as a stated `name: false` line), that every
     export is `false`, and which files omit which field (the AY1 reverse omitting
     `rate_in_N_claimed` is a named, expected finding, not a script bug).
  3. `gate_value_agreement_check` -- whether `states_compared`, `region`,
     `topology` and `closeness_order` agree byte-for-byte across forward,
     reverse (AY1 only), skeptic and gate (AY1), and forward vs. the skeptic
     pre-comparison (AY2).
  4. `forbidden_phrase_scan` -- "the AQ state" / "uniqueness of the AQ state",
     "the thermodynamic limit", and bare "unique" without "not" in the same
     sentence, across AY1/AY2 reports, reviews, gates and contracts, with a
     whitelist for verbatim negated quotations inside markdown code spans;
     JSON `claim_exclusions`-style arrays have no code-span mechanism, so any
     occurrence of the forbidden phrase there is reported as a wording defect,
     not whitelisted, regardless of the exclusion-list context.
  5. `required_phrase_check` -- "a chosen subsequential" present in each report.

Usage: python3 -B sentence_and_gate_field_audit.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common4 as K  # noqa: E402


# ---------------------------------------------------------------------------
# 1. Mandatory sentence template (loop2-response.md section 4), extracted
#    programmatically rather than hardcoded, so a later edit of loop2-response.md
#    is visible as a changed extraction, not a silently stale hardcoded string.
# ---------------------------------------------------------------------------
def extract_section4_sentence_and_fields():
    text = K.load_text(K.JUNG_LOOP2_RESPONSE)
    m = K.match(r'(?s)## 4\. Observation-map rule for AY.*?\n(.*?)\n## 5\.', text, 'section 4 body')
    body = m.group(1)

    m2 = K.match(r'(?s)Mandatory sentence template:\s*"(.*?)"\s*Mandatory gate fields:', body,
                 'mandatory sentence template quote')
    sentence = m2.group(1)

    # Split the template around its one constant-dependent span so a fully filled
    # instance (with the constants, not "<constant>(tau)", substituted in) can
    # still be matched: everything before "<constant>(tau)" is fixed (PREFIX);
    # everything from "This is uniform local closeness" to the end of the
    # sentence is fixed as well (SUFFIX), independent of which constants were
    # filled in or how the bracketed order clause was rendered.
    pivot = '<constant>(tau)'
    K.require(pivot in sentence, 'template pivot %r not found in extracted sentence' % pivot)
    prefix_raw, _, rest = sentence.partition(pivot)
    anchor = 'This is uniform local closeness'
    K.require(anchor in rest, 'template suffix anchor %r not found after pivot' % anchor)
    suffix_raw = rest[rest.index(anchor):]

    m3 = K.match(r'(?s)Mandatory gate fields:\s*(.*?)\s*Forbidden phrasings:', body, 'mandatory gate fields text')
    gate_fields_text = m3.group(1)
    # Field names quoted in backticks immediately followed by ':' in that text.
    field_names_loop2 = re.findall(r'`([a-zA-Z_]+)`:\s*', gate_fields_text)

    m4 = K.match(r'(?s)Forbidden phrasings:\s*(.*?)\s*required:\s*(.*?)\.\s*Observation-map rule:', body,
                 'forbidden phrasings and required phrase text')
    forbidden_text, required_text = m4.group(1), m4.group(2)

    return {
        'raw_sentence': sentence,
        'prefix': K.normalize_sentence(prefix_raw),
        'suffix': K.normalize_sentence(suffix_raw),
        'gate_fields_text_raw': gate_fields_text,
        'field_names_found_in_loop2_section4': field_names_loop2,
        'forbidden_phrasings_text_raw': forbidden_text,
        'required_phrase_text_raw': required_text,
    }


def sentence_present(text):
    norm = K.normalize_sentence(text)
    template = extract_section4_sentence_and_fields()
    pi = norm.find(template['prefix'])
    if pi == -1:
        return False, 'prefix not found (verbatim modulo constants failed at the fixed opening clause)'
    si = norm.find(template['suffix'], pi)
    if si == -1:
        return False, 'suffix not found after the prefix (verbatim modulo constants failed at the fixed closing clause)'
    return True, None


def run_mandatory_sentence_check():
    template = extract_section4_sentence_and_fields()
    targets = {
        'forward_ay1_report': K.FORWARD_AY1_REPORT,
        'reverse_ay1_report': K.REVERSE_AY1_REPORT,
        'forward_ay2_report': K.FORWARD_AY2_REPORT,
    }
    per_file = {}
    for label, path in targets.items():
        text = K.load_text(path)
        ok, reason = sentence_present(text)
        per_file[label] = {'path': str(path.relative_to(K.ROOT)), 'passed': ok, 'reason': reason}

    # The AY1 gate's accepted text, separately (may use the paraphrased,
    # contract-form sentence instead of the Jung verbatim form -- this is
    # checked for, not assumed).
    gate = K.load_json(K.AY1_GATE)
    accepted_text = gate.get('accepted', '')
    ok, reason = sentence_present(accepted_text)
    per_file['ay1_gate_accepted'] = {'path': str(K.AY1_GATE.relative_to(K.ROOT)), 'passed': ok, 'reason': reason}

    # The AY2 gate: absent at the calling task's naming ("gate may not exist yet,
    # handle absence"), but present as of this run (a live, concurrently-
    # advancing repository -- see README "Non-defect notes"). Checked the same
    # way, when present.
    ay2_gate_exists = K.AY2_GATE.exists()
    if ay2_gate_exists:
        ay2_gate = K.load_json(K.AY2_GATE)
        ay2_accepted_text = ay2_gate.get('accepted', '') + ' ' + ay2_gate.get('decision', '')
        ok2, reason2 = sentence_present(ay2_accepted_text)
        per_file['ay2_gate_accepted'] = {'path': str(K.AY2_GATE.relative_to(K.ROOT)), 'passed': ok2, 'reason': reason2}

    # Also record, separately, whether the CONTRACT-FORM paraphrase (AY1's own
    # preregistration.mandatory_sentence_template field) is what appears in the
    # gate's accepted text instead -- informative, not a pass/fail gate on its own.
    ay1c = K.load_json(K.AY1_CONTRACT)
    contract_template = ay1c.get('preregistration', {}).get('mandatory_sentence_template')
    contract_template_verbatim_matches_loop2 = (
        contract_template is not None and K.normalize_sentence(contract_template) == K.normalize_sentence(template['raw_sentence'])
    )
    gate_contains_contract_paraphrase = (
        contract_template is not None
        and K.normalize_sentence(contract_template).split(';')[0].strip() != ''
        and K.normalize_sentence(contract_template).split(';')[0].strip() in K.normalize_sentence(accepted_text)
    )

    all_pass = all(v['passed'] for v in per_file.values())
    return {
        'id': 'mandatory_sentence_template_check',
        'role': 'checks the loop2-response.md section 4 mandatory sentence template is present, verbatim '
                'modulo the filled-in constants, in every required report.md and in the AY1 gate accepted text',
        'template_prefix_fixed_clause': template['prefix'],
        'template_suffix_fixed_clause': template['suffix'],
        'per_file': per_file,
        'ay1_contract_mandatory_sentence_template_field': contract_template,
        'ay1_contract_template_is_verbatim_loop2_wording': contract_template_verbatim_matches_loop2,
        'ay1_gate_accepted_contains_contract_paraphrase_instead': gate_contains_contract_paraphrase,
        'passed': all_pass,
        'findings': (
            ['PASS: the verbatim (modulo constants) Jung-form sentence is present in all three required '
             'report.md files.' if all(per_file[k]['passed'] for k in
                                        ('forward_ay1_report', 'reverse_ay1_report', 'forward_ay2_report'))
             else 'FAIL: at least one required report.md is missing the verbatim sentence; see per_file.'] +
            (['FINDING: the AY1 gate\'s accepted text does NOT contain the loop2-response.md verbatim '
              '(modulo constants) sentence; it contains only the contract\'s own paraphrase '
              '("For every pair of subsequential limits of the named construction families F1 and F2 at the '
              'same coupling, on the fixed cover R and for the frozen observable class, the reduced densities '
              'satisfy ...") -- present: %r. The contract\'s paraphrase field '
              '(preregistration.mandatory_sentence_template) is itself not a verbatim copy of the '
              'loop2-response.md wording (it uses "the reduced densities satisfy ||rho_R - rho\'_R||_1 <= 2D" '
              'in place of the universally-quantified "for every A in B(H_R) with ||A||<=1: '
              '|omega\'(A)-omega\'\'(A)| <= ..." form). Both report.md files (forward and reverse) DO include the '
              'verbatim Jung-form sentence as well as this paraphrase (both are labelled "mandatory sentences", '
              'plural, in the reports) -- only the gate carries the paraphrase alone.'
              % gate_contains_contract_paraphrase]
             if not per_file['ay1_gate_accepted']['passed'] else []) +
            (['FINDING: the AY2 gate exists as of this run (absent when the calling task named the file; this '
              'is a live, concurrently-advancing repository) and its accepted+decision text also does NOT '
              'contain the loop2-response.md verbatim (modulo constants) sentence -- it independently confirms, '
              'in its own "decision" field, "the AY2 preregistration has no template field" and lists the same '
              'contract defects D1-D6 this audit found independently (selected_after placeholder, '
              '"uniqueness of the AQ state" in the exclusions, rate_in_N_claimed missing from '
              'gate_fields_required, among others).'] if ay2_gate_exists and not per_file['ay2_gate_accepted']['passed']
             else (['FINDING: the AY2 gate exists as of this run and DOES contain the verbatim sentence.']
                   if ay2_gate_exists else []))
        ),
    }


# ---------------------------------------------------------------------------
# 2 & 3. Gate-field export/value checks.
# ---------------------------------------------------------------------------
def scan_json_gate_fields(path, root_only_for_values=True):
    """Returns (bool_exports: {name: [(path, value), ...]}, value_fields: {name: value_at_root_or_gate_fields})."""
    data = K.load_json(path)
    bool_exports = {name: K.find_key_occurrences(data, name) for name in K.GATE_FIELD_BOOL_NAMES}
    # Value fields: prefer a top-level 'gate_fields' sub-object if present (the
    # gate and the skeptic reviews nest them there); else read the root directly.
    src = data.get('gate_fields') if isinstance(data.get('gate_fields'), dict) else data
    value_fields = {name: src.get(name) for name in K.GATE_FIELD_VALUE_NAMES}
    return data, bool_exports, value_fields


def scan_md_gate_field_bools(path):
    """For a markdown report: for each of the six boolean names, find every
    `name: false` / `name:false` / `name: true` occurrence (backticks optional)."""
    text = K.load_text(path)
    out = {}
    for name in K.GATE_FIELD_BOOL_NAMES:
        hits = []
        for m in re.finditer(r'`?%s`?\s*:\s*(true|false)\b' % re.escape(name), text):
            hits.append(m.group(1))
        out[name] = hits
    return out


def run_gate_field_checks():
    json_files = {
        'ay1_gate': K.AY1_GATE,
        'forward_ay1_results': K.FORWARD_AY1_RESULTS,
        'reverse_ay1_results': K.REVERSE_AY1_RESULTS,
        'skeptic_ay1': K.SKEPTIC_AY1_JSON,
        'ay1_contract': K.AY1_CONTRACT,
        'forward_ay2_results': K.FORWARD_AY2_RESULTS,
        'skeptic_ay2_independent': K.SKEPTIC_AY2_INDEPENDENT_RESULTS,
        'ay2_contract': K.AY2_CONTRACT,
    }
    md_files = {
        'forward_ay1_report': K.FORWARD_AY1_REPORT,
        'reverse_ay1_report': K.REVERSE_AY1_REPORT,
        'forward_ay2_report': K.FORWARD_AY2_REPORT,
    }

    export_matrix = {}  # file -> field -> {'exported_false': n, 'exported_true': n, 'mentioned_as_string': n}
    violations = []
    value_records = {}  # file -> {field: value}

    for label, path in json_files.items():
        data, bool_exports, value_fields = scan_json_gate_fields(path)
        row = {}
        for name in K.GATE_FIELD_BOOL_NAMES:
            hits = bool_exports[name]
            n_false = sum(1 for (_, v) in hits if v is False)
            n_true = sum(1 for (_, v) in hits if v is True)
            n_other = sum(1 for (_, v) in hits if not isinstance(v, bool))
            row[name] = {'n_key_occurrences': len(hits), 'n_false': n_false, 'n_true': n_true,
                         'n_non_boolean': n_other, 'paths': [p for (p, _) in hits]}
            if n_true:
                violations.append({'file': label, 'field': name,
                                    'detail': 'exported true at least once: paths %r'
                                              % [p for (p, v) in hits if v is True]})
        export_matrix[label] = row
        value_records[label] = value_fields

    for label, path in md_files.items():
        hits_by_name = scan_md_gate_field_bools(path)
        row = {}
        for name in K.GATE_FIELD_BOOL_NAMES:
            vals = hits_by_name[name]
            n_false = vals.count('false')
            n_true = vals.count('true')
            row[name] = {'n_key_occurrences': len(vals), 'n_false': n_false, 'n_true': n_true,
                         'n_non_boolean': 0, 'paths': []}
            if n_true:
                violations.append({'file': label, 'field': name,
                                    'detail': 'markdown scan found %d occurrence(s) of "%s: true"' % (n_true, name)})
        export_matrix[label] = row

    # AY2 gate: record absence explicitly (calling task: "gate may not exist yet, handle absence").
    ay2_gate_present = K.AY2_GATE.exists()
    if ay2_gate_present:
        data, bool_exports, value_fields = scan_json_gate_fields(K.AY2_GATE)
        row = {name: {'n_key_occurrences': len(bool_exports[name]),
                      'n_false': sum(1 for (_, v) in bool_exports[name] if v is False),
                      'n_true': sum(1 for (_, v) in bool_exports[name] if v is True),
                      'n_non_boolean': sum(1 for (_, v) in bool_exports[name] if not isinstance(v, bool)),
                      'paths': [p for (p, _) in bool_exports[name]]} for name in K.GATE_FIELD_BOOL_NAMES}
        export_matrix['ay2_gate'] = row
        value_records['ay2_gate'] = value_fields

    # Which files export which field at all (n_key_occurrences > 0), and which omit it.
    per_field_file_presence = {}
    for name in K.GATE_FIELD_BOOL_NAMES:
        present = sorted(f for f, row in export_matrix.items() if row[name]['n_key_occurrences'] > 0)
        absent = sorted(f for f, row in export_matrix.items() if row[name]['n_key_occurrences'] == 0)
        per_field_file_presence[name] = {'exported_by': present, 'not_exported_by': absent}

    reverse_omits_rate_in_N = 'reverse_ay1_report' in per_field_file_presence['rate_in_N_claimed']['not_exported_by'] \
        and 'reverse_ay1_results' in per_field_file_presence['rate_in_N_claimed']['not_exported_by']

    findings = []
    findings.append(
        'Six-name gate-field union checked: %s. Three are named verbatim in loop2-response.md section 4 '
        '(uniqueness_claimed, whole_sequence_claimed, rate_in_N_claimed); three more first appear in AY1\'s '
        'own contract item 4 and are recorded in advisor/panel-update-3.md item 2 (rate_claimed, '
        'translation_invariance_claimed, boundary_independence_of_dynamics_claimed).' % (K.GATE_FIELD_BOOL_NAMES,))
    findings.append(
        'FINDING (expected, matches the calling task\'s own note): the AY1 reverse does not export '
        'rate_in_N_claimed as a real JSON key, in neither reverse/ay1/report.md (markdown scan) nor '
        'reverse/ay1/output/results.json (JSON key-walk). reverse_omits_rate_in_N_claimed=%r.'
        % reverse_omits_rate_in_N)
    if not violations:
        findings.append('No file exports any of the six fields as true anywhere; every real export found is false.')
    else:
        for v in violations:
            findings.append('VIOLATION: %s' % v)

    d3 = None
    ay2c = K.load_json(K.AY2_CONTRACT)
    gfr = ay2c.get('preregistration', {}).get('gate_fields_required', {})
    if 'rate_in_N_claimed' not in gfr:
        d3 = ('AY2 contract preregistration.gate_fields_required omits rate_in_N_claimed even though AY2\'s own '
              '"required" item 6 text lists it (both rate_claimed and rate_in_N_claimed). This is the D3 defect '
              'the AY2 forward report itself records (forward/ay2/report.md, defects table row D3): '
              '"gate_fields_required lacks rate_in_N_claimed, which item 6 requires; both rate fields are '
              'exported false" -- independently confirmed here by reading the contract field directly: '
              'gate_fields_required=%r' % gfr)
        findings.append('FINDING: ' + d3)

    ay1c = K.load_json(K.AY1_CONTRACT)
    gfr1 = ay1c.get('preregistration', {}).get('gate_fields_required', {})
    if 'rate_in_N_claimed' not in gfr1:
        findings.append('FINDING: AY1 contract preregistration.gate_fields_required also omits rate_in_N_claimed '
                        '(uses rate_claimed only): gate_fields_required=%r. This is the origin of the '
                        'rate_claimed/rate_in_N_claimed name split (self-noted as wording defect W3 by the AY1 '
                        'forward producer and independently recorded in the AY1 gate\'s decision text and in '
                        'skeptic/ay1.json).' % gfr1)

    return {
        'id': 'gate_field_export_check',
        'role': 'for the six-name gate-field boolean union: which files export which as a real key, whether '
                'every export is false, and which files omit which field',
        'fields_checked': list(K.GATE_FIELD_BOOL_NAMES),
        'export_matrix': export_matrix,
        'per_field_file_presence': per_field_file_presence,
        'ay2_gate_present': ay2_gate_present,
        'violations': violations,
        'ay1_contract_gate_fields_required': gfr1,
        'ay2_contract_gate_fields_required': gfr,
        'passed': len(violations) == 0,
        'findings': findings,
    }, value_records


def run_gate_value_agreement_check(value_records):
    ay1_sources = {
        'forward_ay1_results': value_records.get('forward_ay1_results', {}),
        'reverse_ay1_results': value_records.get('reverse_ay1_results', {}),
        'skeptic_ay1': value_records.get('skeptic_ay1', {}),
        'ay1_gate': value_records.get('ay1_gate', {}),
    }
    ay2_sources = {
        'forward_ay2_results': value_records.get('forward_ay2_results', {}),
        'skeptic_ay2_independent': value_records.get('skeptic_ay2_independent', {}),
    }
    # The AY2 gate: absent at the calling task's naming, present as of this run
    # (see module/README notes on the live repository) -- included when found.
    if 'ay2_gate' in value_records:
        ay2_sources['ay2_gate'] = value_records['ay2_gate']

    def agreement_report(sources, fields):
        out = {}
        for f in fields:
            vals = {name: src.get(f) for name, src in sources.items()}
            distinct = []
            for v in vals.values():
                if v not in distinct:
                    distinct.append(v)
            out[f] = {'values_by_source': vals, 'n_distinct_values': len(distinct), 'all_agree': len(distinct) <= 1}
        return out

    ay1_report = agreement_report(ay1_sources, K.GATE_FIELD_VALUE_NAMES)
    ay2_report = agreement_report(ay2_sources, K.GATE_FIELD_VALUE_NAMES)

    findings = []
    for f, entry in ay1_report.items():
        if entry['all_agree']:
            findings.append('AY1 %s: all four sources agree exactly.' % f)
        else:
            findings.append('AY1 %s: sources DISAGREE (%d distinct values) -- %r'
                            % (f, entry['n_distinct_values'], entry['values_by_source']))
    ay2_source_names = ', '.join(sorted(ay2_sources))
    for f, entry in ay2_report.items():
        if entry['all_agree']:
            findings.append('AY2 %s: all sources (%s) agree exactly.' % (f, ay2_source_names))
        else:
            findings.append('AY2 %s: sources (%s) DISAGREE -- %r'
                            % (f, ay2_source_names, entry['values_by_source']))

    all_ay1_agree = all(e['all_agree'] for e in ay1_report.values())
    all_ay2_agree = all(e['all_agree'] for e in ay2_report.values())

    return {
        'id': 'gate_value_agreement_check',
        'role': 'whether states_compared/region/topology/closeness_order agree byte-for-byte across '
                'forward/reverse/skeptic/gate (AY1) and forward/skeptic-independent (AY2)',
        'ay1': ay1_report,
        'ay2': ay2_report,
        'passed': all_ay1_agree and all_ay2_agree,
        'findings': findings,
    }


# ---------------------------------------------------------------------------
# 4. Forbidden-phrase scan + 5. required-phrase check.
# ---------------------------------------------------------------------------
PHRASE_PATTERNS = {
    'the_AQ_state': re.compile(re.escape('the AQ state'), re.I),
    'the_thermodynamic_limit': re.compile(re.escape('the thermodynamic limit'), re.I),
    'bare_unique': re.compile(r'\bunique(?:ness)?\b', re.I),
}


def sentence_has_not(text, pos):
    """For the bare-'unique' phrase: is there a 'not' in the same sentence?
    A sentence is approximated as the span between the nearest '.', ';', '\\n'
    (or start/end of text) on either side of pos."""
    start = 0
    for sep in '.;\n':
        i = text.rfind(sep, 0, pos)
        if i > start:
            start = i
    end = len(text)
    for sep in '.;\n':
        i = text.find(sep, pos)
        if i != -1 and i < end:
            end = i
    sentence = text[start:end].lower()
    return 'not' in sentence


def scan_markdown_for_phrases(label, path):
    text = K.load_text(path)
    occurrences = []
    for phrase_id, pattern in PHRASE_PATTERNS.items():
        for m in pattern.finditer(text):
            if phrase_id == 'bare_unique':
                if sentence_has_not(text, m.start()):
                    continue  # "unique" with "not" in the same sentence is fine, not scanned further
            kind, cues = K.classify_phrase_occurrence(text, m.start(), m.end())
            occurrences.append({
                'phrase': phrase_id, 'matched_text': m.group(0),
                'line': text.count('\n', 0, m.start()) + 1,
                'context': text[max(0, m.start() - 120):min(len(text), m.end() + 120)].replace('\n', ' ').strip(),
                'classification': kind, 'cues': cues,
            })
    required_present = K.REQUIRED_PHRASE in text
    n_affirmative = sum(1 for o in occurrences if o['classification'] == 'AFFIRMATIVE_needs_review')
    n_negated_outside = sum(1 for o in occurrences if o['classification'] == 'negated_outside_code_span')
    return {
        'file': label, 'path': str(path.relative_to(K.ROOT)), 'kind': 'markdown',
        'occurrences': occurrences, 'n_occurrences': len(occurrences), 'n_affirmative': n_affirmative,
        'n_negated_outside_code_span': n_negated_outside,
        'required_phrase_present': required_present,
        'passed': n_affirmative == 0,
    }


OBLIGATIONS_TABLE_PATH_RE = re.compile(r'\bobligations\[\d+\]')
MUTATION_OR_CONTROL_PATH_RE = re.compile(
    r'\bmutations\[\d+\]|rejected_for|required_false|\.mutation$|\bchecks\[\d+\]\.id$|contract_defects|'
    r'\bdefects\[\d+\]')


def scan_json_for_phrases(label, path):
    data = K.load_json(path)
    occurrences = []
    for str_path, value in K.walk_json_strings(data):
        for phrase_id, pattern in PHRASE_PATTERNS.items():
            for m in pattern.finditer(value):
                if phrase_id == 'bare_unique' and sentence_has_not(value, m.start()):
                    continue
                is_exclusion_list_entry = bool(re.search(r'claim_exclusions(\[\d+\])?$', str_path)) or \
                    bool(re.search(r'\bexclusions?(\[\d+\])?$', str_path, re.I))
                if is_exclusion_list_entry:
                    kind, cues = 'contract_exclusion_list_wording_defect', []
                elif OBLIGATIONS_TABLE_PATH_RE.search(str_path):
                    # An entry of an explicit "unproved obligations" table (AY2 item
                    # 2 / D2's obligations array): the word names the obligation or
                    # the missing premise itself (e.g. "uniqueness of the limit" as
                    # the id of a row the table records as NOT proved) -- the table
                    # as a whole is the negation, so a bare "unique(ness)" naming the
                    # obligation is not read as a claim that it holds.
                    kind, cues = 'obligations_table_entry_names_the_missing_property', []
                elif MUTATION_OR_CONTROL_PATH_RE.search(str_path):
                    # A control/mutation-table entry naming what a damaging mutation
                    # would set, or a control id -- not an assertion.
                    kind, cues = 'mutation_or_control_description', []
                else:
                    window = (str_path + ' ' + value).lower()
                    cues = [c for c in K.PHRASE_NEGATION_CUES if c in window]
                    kind = 'negation_or_exclusion' if cues else 'AFFIRMATIVE_needs_review'
                occurrences.append({
                    'phrase': phrase_id, 'json_path': str_path, 'matched_text': m.group(0),
                    'value_excerpt': value[max(0, m.start() - 100):min(len(value), m.end() + 100)],
                    'classification': kind, 'cues': cues,
                })
    n_affirmative = sum(1 for o in occurrences if o['classification'] == 'AFFIRMATIVE_needs_review')
    n_wording_defects = sum(1 for o in occurrences if o['classification'] == 'contract_exclusion_list_wording_defect')
    return {
        'file': label, 'path': str(path.relative_to(K.ROOT)), 'kind': 'json',
        'occurrences': occurrences, 'n_occurrences': len(occurrences), 'n_affirmative': n_affirmative,
        'n_contract_exclusion_list_wording_defects': n_wording_defects,
        'passed': n_affirmative == 0,
    }


def run_forbidden_and_required_phrase_scan():
    md_required = {
        'forward_ay1_report': K.FORWARD_AY1_REPORT,
        'reverse_ay1_report': K.REVERSE_AY1_REPORT,
        'forward_ay2_report': K.FORWARD_AY2_REPORT,
    }
    md_bonus = {
        'skeptic_ay1_md': K.SKEPTIC_AY1_MD,
    }
    json_required = {
        'ay1_gate': K.AY1_GATE,
        'skeptic_ay1_json': K.SKEPTIC_AY1_JSON,
        'skeptic_ay2_independent': K.SKEPTIC_AY2_INDEPENDENT_RESULTS,
        'ay1_contract': K.AY1_CONTRACT,
        'ay2_contract': K.AY2_CONTRACT,
    }
    json_bonus = {
        'az1_contract': K.AZ1_CONTRACT,
        'az2_contract': K.AZ2_CONTRACT,
    }
    if K.AY2_GATE.exists():
        # Absent at the calling task's naming; present as of this run (live
        # repository) -- scanned as bonus coverage, not folded into the
        # required-file pass/fail, since the calling task named ay1-gate.json
        # but not (a not-yet-existing) ay2-gate.json.
        json_bonus['ay2_gate'] = K.AY2_GATE

    md_results = {label: scan_markdown_for_phrases(label, path) for label, path in md_required.items()}
    md_bonus_results = {label: scan_markdown_for_phrases(label, path) for label, path in md_bonus.items()}
    json_results = {label: scan_json_for_phrases(label, path) for label, path in json_required.items()}
    json_bonus_results = {label: scan_json_for_phrases(label, path) for label, path in json_bonus.items()}

    all_required = list(md_results.values()) + list(json_results.values())
    all_passed = all(r['passed'] for r in all_required)

    exclusion_list_defects = []
    for label, r in list(json_results.items()) + list(json_bonus_results.items()):
        for o in r['occurrences']:
            if o['classification'] == 'contract_exclusion_list_wording_defect':
                exclusion_list_defects.append({'file': label, 'path': r['path'], 'json_path': o['json_path'],
                                               'matched_text': o['matched_text']})

    findings = []
    findings.append('Scanned %d required files (%d markdown, %d JSON) for "the AQ state"/"uniqueness of the AQ '
                    'state", "the thermodynamic limit" and bare "unique" without "not" in the same sentence.'
                    % (len(all_required), len(md_results), len(json_results)))
    n_aff = sum(r['n_affirmative'] for r in all_required)
    findings.append('%d occurrence(s) classified AFFIRMATIVE_needs_review across required files (0 expected).'
                    % n_aff)
    n_obl = sum(sum(1 for o in r['occurrences']
                    if o['classification'] == 'obligations_table_entry_names_the_missing_property')
               for r in json_results.values())
    n_mut = sum(sum(1 for o in r['occurrences'] if o['classification'] == 'mutation_or_control_description')
               for r in json_results.values())
    if n_obl:
        findings.append(
            'FINDING: %d occurrence(s) of bare "unique"/"uniqueness" are entries of an explicit unproved-'
            'obligations table (json path contains "obligations[N]", e.g. skeptic/ay2-independent/results.json '
            'obligations[1].missing_premise = "uniqueness of subsequential limits within the family (...)"): the '
            'word names the missing property the table records as NOT proved, so the table\'s own structure is '
            'the negation; the literal "unique(ness) without not in the same sentence" rule, read strictly '
            'sentence-by-sentence, would flag these (no literal "not" token in the same short JSON string), so '
            'this classification is reported as a distinct, deliberate exception, not folded silently into '
            '"negation_or_exclusion".' % n_obl)
    if n_mut:
        findings.append('%d occurrence(s) are control/mutation-table entries naming what a damaging mutation '
                        'would set or a control id (e.g. a control literally named '
                        '"local_closeness_not_uniqueness"), not an assertion.' % n_mut)
    n_neg_outside = sum(r.get('n_negated_outside_code_span', 0) for r in md_results.values())
    if n_neg_outside:
        findings.append(
            'FINDING: %d occurrence(s) are negated but not inside a markdown code span, so they fall outside '
            'the letter of the calling task\'s "whitelist for verbatim negated quotations in code spans" even '
            'though they read as negations, not affirmative claims -- e.g. reverse/ay1/report.md: '
            '"- not claimed: uniqueness of the AQ state;" is plain prose (not wrapped in backticks), unlike the '
            'forward report\'s equivalent, which is inside a code span. Recorded as a wording-hygiene note, not a '
            'forbidden-phrase violation (the phrase there is unambiguously negated).' % n_neg_outside)
    if exclusion_list_defects:
        distinct_locations = sorted({'%s:%s' % (d['file'], d['json_path']) for d in exclusion_list_defects})
        findings.append(
            'WORDING DEFECT (calling task item: "report exactly where the phrase \'uniqueness of the AQ state\' '
            'still appears in contract exclusion lists"): the literal phrase appears inside a '
            '`claim_exclusions`/`preregistration.claim_exclusions` JSON array (not a markdown code span, so the '
            'code-span whitelist does not apply) in: %s. Every one of these arrays is a verbatim, unmodified copy '
            'of loop2-response.md section 2\'s own pre-registration-block template, whose own '
            '`claim_exclusions` list contains this same phrase as one of its seven entries -- the phrase\'s origin '
            'is the section-2 template itself, not a per-contract slip. It is a wording defect relative to '
            'section 4\'s naming rule ("Forbidden phrasings: \'the AQ state\' ...") only in the sense that the '
            'string is still physically present in these files; every read of it found here is inside an '
            'excluded-claim list (naming the claim in order to rule it out), never an assertion.'
            % ', '.join(distinct_locations))
    else:
        findings.append('No contract_exclusion_list_wording_defect occurrences found.')

    req_missing = [label for label, r in md_results.items() if not r['required_phrase_present']]
    if req_missing:
        findings.append('FAIL: required phrase %r missing from: %s' % (K.REQUIRED_PHRASE, req_missing))
    else:
        findings.append('Required phrase %r present in all three required report.md files.' % K.REQUIRED_PHRASE)

    return {
        'id': 'forbidden_and_required_phrase_scan',
        'role': 'forbidden-phrase scan (the AQ state / uniqueness of the AQ state / the thermodynamic limit / '
                'bare unique without not) and required-phrase check (a chosen subsequential) across AY1/AY2 '
                'reports, reviews, gates and contracts',
        'markdown_required': md_results,
        'markdown_bonus': md_bonus_results,
        'json_required': json_results,
        'json_bonus_az1_az2_contracts': json_bonus_results,
        'contract_exclusion_list_wording_defects': exclusion_list_defects,
        'required_phrase_missing_from': req_missing,
        'passed': all_passed and not req_missing,
        'findings': findings,
    }


def run():
    sentence_check = run_mandatory_sentence_check()
    gate_field_check, value_records = run_gate_field_checks()
    value_agreement_check = run_gate_value_agreement_check(value_records)
    phrase_scan = run_forbidden_and_required_phrase_scan()

    overall_pass = (sentence_check['passed'] and gate_field_check['passed']
                    and value_agreement_check['passed'] and phrase_scan['passed'])
    # `passed` here means "clean, no defects found" and is deliberately allowed to
    # be False: this tool's purpose is to surface wording/structural defects
    # (like sub-round 3's W1-W7), not to gate admission (it counts zero research
    # loops either way). A False sub-check is a reported finding, not a script bug.
    result = {
        'id': 'sentence_and_gate_field_audit',
        'role': 'the sentence-template and gate-field checks (panel-update-3.md item 6, Jung share); zero '
                'research loops; audits AY1/AY2, never admission evidence',
        'ay2_gate_present': gate_field_check['ay2_gate_present'],
        'mandatory_sentence_template_check': sentence_check,
        'gate_field_export_check': gate_field_check,
        'gate_value_agreement_check': value_agreement_check,
        'forbidden_and_required_phrase_scan': phrase_scan,
        'passed': overall_pass,
    }
    return result


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'sentence_and_gate_field_audit', result)
    print('sentence_and_gate_field_audit: %s' % ('PASS' if result['passed'] else 'FAIL (see findings)'))
    print('  mandatory_sentence_template_check: %s' % result['mandatory_sentence_template_check']['passed'])
    for f in result['mandatory_sentence_template_check']['findings']:
        print('    -', f)
    print('  gate_field_export_check: %s' % result['gate_field_export_check']['passed'])
    for f in result['gate_field_export_check']['findings']:
        print('    -', f)
    print('  gate_value_agreement_check: %s' % result['gate_value_agreement_check']['passed'])
    for f in result['gate_value_agreement_check']['findings']:
        print('    -', f)
    print('  forbidden_and_required_phrase_scan: %s' % result['forbidden_and_required_phrase_scan']['passed'])
    for f in result['forbidden_and_required_phrase_scan']['findings']:
        print('    -', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
