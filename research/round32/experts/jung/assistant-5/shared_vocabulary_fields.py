#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 5, assistant-5 script 3 of 3: the
shared-vocabulary field mirror check for AY1/AY2 (panel-update-4.md item 3's
own rule, item 5, item 7; calling task item 3).

Counts zero research loops. Not a producer, contract, gate or skeptical
review; nothing computed here is read back into any of those. Human project
author: Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not
import `forward/*/check.py`, `reverse/*/check.py`, or any other
producer/skeptic module.

**The rule this script implements**, quoted from `advisor/panel-update-4.md`
item 3 (itself citing `experts/jung/assistant-4/README.md`'s AY1 finding):
"extend the mirror check already used for `controls ==
preregistration.controls_required.ids` to the shared-vocabulary field names a
contract requires from every producer (`states_compared`, `region`,
`topology`, `closeness_order`); either they must be byte-identical, or the
checker must record which producer's exact string the gate adopts and treat
the rest as a named wording variant, the same way headline numeric constants
are already bound to one exact rational with variants labelled."

For AY1: `forward/ay1/output/results.json`, `reverse/ay1/output/
results.json`, `skeptic/ay1.json` (the consolidated skeptic record -- not the
raw `skeptic/ay1-independent/results.json`/`skeptic/ay1-postreview/
results.json` files, which were checked directly and found not to export
these four fields at all) and `advisor/ay1-gate.json`.

For AY2 (no reverse producer): `forward/ay2/output/results.json`, the
skeptic's pre-comparison `skeptic/ay2-independent/results.json` (assistant-4's
own AY2 source, from before the final postreview existed), the now-existing
final skeptic record `skeptic/ay2.json` (the postreview, `skeptic/ay2-
postreview/results.json` checked directly and found not to export these
fields either) and `advisor/ay2-gate.json`.

For each of the four fields, per contract: every source's exact value AND
Python type are recorded; if not byte-identical, the gate's own value is
named as the adopted canonical string, every OTHER source whose value
(exact string, not just informal content) equals the gate's is recorded as
"agrees with the gate", and every source whose value differs is recorded as
a distinct, named wording variant -- unless its Python TYPE differs from the
gate's (e.g. a dict where every other source has a string, or a bare int
where every other source has a list), which is recorded as a stronger,
separate `type_mismatch` finding, since a JSON type difference is not
resolvable by "the gate adopts one wording among several" the way a string
paraphrase is.

Usage: python3 -B shared_vocabulary_fields.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common5 as K  # noqa: E402

FIELDS = ('states_compared', 'region', 'topology', 'closeness_order')

AY1_SOURCES = {
    'forward': K.FORWARD / 'ay1' / 'output' / 'results.json',
    'reverse': K.REVERSE / 'ay1' / 'output' / 'results.json',
    'skeptic': K.SKEPTIC / 'ay1.json',
    'gate': K.ADVISOR / 'ay1-gate.json',
}
AY2_SOURCES = {
    'forward': K.FORWARD / 'ay2' / 'output' / 'results.json',
    'skeptic_independent_precomparison': K.SKEPTIC / 'ay2-independent' / 'results.json',
    'skeptic_final_postreview': K.SKEPTIC / 'ay2.json',
    'gate': K.ADVISOR / 'ay2-gate.json',
}
# Files checked directly and confirmed NOT to export these four fields at all
# (recorded for the README/audit trail, not used as comparison sources).
CHECKED_BUT_EMPTY = {
    'ay1': [K.SKEPTIC / 'ay1-independent' / 'results.json', K.SKEPTIC / 'ay1-postreview' / 'results.json'],
    'ay2': [K.SKEPTIC / 'ay2-postreview' / 'results.json'],
}


def field_value(data, field):
    src = data.get('gate_fields') if isinstance(data.get('gate_fields'), dict) else data
    return src.get(field)


def load_sources(sources_map):
    out = {}
    for label, path in sources_map.items():
        out[label] = {'path': str(path.relative_to(K.ROOT)), 'exists': path.exists(),
                      'data': K.load_json(path) if path.exists() else None}
    return out


def compare_field(loaded, field, gate_label):
    values = {}
    for label, entry in loaded.items():
        if not entry['exists']:
            values[label] = {'present': False}
            continue
        v = field_value(entry['data'], field)
        values[label] = {'present': v is not None, 'value': v, 'type': type(v).__name__}

    present_labels = [l for l, v in values.items() if v.get('present')]
    distinct_reprs = []
    for l in present_labels:
        r = repr(values[l]['value'])
        if r not in distinct_reprs:
            distinct_reprs.append(r)
    all_byte_identical = len(distinct_reprs) <= 1

    gate_entry = values.get(gate_label, {})
    gate_value = gate_entry.get('value') if gate_entry.get('present') else None
    gate_type = gate_entry.get('type')

    agrees_with_gate, wording_variants, type_mismatches = [], [], []
    for l in present_labels:
        if l == gate_label:
            continue
        v = values[l]
        if v['value'] == gate_value and v['type'] == gate_type:
            agrees_with_gate.append(l)
        elif v['type'] != gate_type:
            type_mismatches.append({'source': l, 'type': v['type'], 'gate_type': gate_type, 'value': v['value']})
        else:
            wording_variants.append({'source': l, 'value': v['value']})

    return {
        'field': field, 'all_byte_identical': all_byte_identical, 'n_distinct_values': len(distinct_reprs),
        'values_by_source': values, 'gate_value': gate_value, 'gate_type': gate_type,
        'sources_agreeing_with_gate_exactly': agrees_with_gate,
        'sources_with_named_wording_variant': wording_variants,
        'sources_with_type_mismatch_vs_gate': type_mismatches,
        # The panel-update-4.md rule is satisfied when EITHER all sources are
        # byte-identical, OR every non-identical source is at least a
        # same-type wording variant that this record now names (a type
        # mismatch is NOT covered by "named wording variant" and fails the
        # rule as stated).
        'rule_satisfied': all_byte_identical or not type_mismatches,
    }


def audit_contract(cid, sources_map, gate_label='gate'):
    loaded = load_sources(sources_map)
    fields = {f: compare_field(loaded, f, gate_label) for f in FIELDS}
    passed = all(fe['rule_satisfied'] for fe in fields.values())
    return {'contract': cid, 'sources': {l: {'path': e['path'], 'exists': e['exists']} for l, e in loaded.items()},
            'fields': fields, 'passed': passed}


def render_findings(cid, entry):
    out = []
    for f, fe in entry['fields'].items():
        if fe['all_byte_identical']:
            out.append('%s %s: all %d source(s) agree byte-for-byte (value=%r, type=%s).'
                       % (cid, f, len(fe['sources_agreeing_with_gate_exactly']) + 1, fe['gate_value'], fe['gate_type']))
            continue
        out.append('%s %s: NOT byte-identical (%d distinct value(s)). Gate (%s) value=%r (type=%s).'
                   % (cid, f, fe['n_distinct_values'], 'adopted-canonical', fe['gate_value'], fe['gate_type']))
        if fe['sources_agreeing_with_gate_exactly']:
            out.append('    agrees with the gate exactly: %s' % ', '.join(fe['sources_agreeing_with_gate_exactly']))
        for v in fe['sources_with_named_wording_variant']:
            out.append('    named wording variant (%s): %r' % (v['source'], v['value']))
        for v in fe['sources_with_type_mismatch_vs_gate']:
            out.append('    TYPE MISMATCH vs gate (%s, type=%s, gate type=%s): %r'
                       % (v['source'], v['type'], v['gate_type'], v['value']))
        if not fe['rule_satisfied']:
            out.append('    DEFECT (panel-update-4.md item 3 rule not satisfied: a type mismatch is not a named '
                       'wording variant): %s.%s' % (cid, f))
    return out


def run():
    ay1 = audit_contract('AY1', AY1_SOURCES)
    ay2 = audit_contract('AY2', AY2_SOURCES)

    checked_empty = {}
    for cid, paths in CHECKED_BUT_EMPTY.items():
        rows = []
        for p in paths:
            occ_counts = {}
            if p.exists():
                data = K.load_json(p)
                for f in FIELDS:
                    occ_counts[f] = len(K.find_key_occurrences(data, f))
            rows.append({'path': str(p.relative_to(K.ROOT)), 'exists': p.exists(), 'field_key_occurrences': occ_counts})
        checked_empty[cid] = rows

    findings = []
    findings.append('Sources for AY1: %s' % {l: e['path'] for l, e in ay1['sources'].items()})
    findings.extend(render_findings('AY1', ay1))
    findings.append('Sources for AY2: %s' % {l: e['path'] for l, e in ay2['sources'].items()})
    findings.extend(render_findings('AY2', ay2))
    findings.append('Checked directly and confirmed NOT to export any of the four fields (not used as comparison '
                    'sources, recorded for the audit trail): %r' % checked_empty)

    passed = ay1['passed'] and ay2['passed']
    return {
        'id': 'shared_vocabulary_fields',
        'role': 'the shared-vocabulary field mirror check for AY1/AY2 (states_compared/region/topology/'
                'closeness_order) across forward/reverse/skeptic/gate, per panel-update-4.md item 3\'s rule; zero '
                'research loops; audits only, never admission evidence',
        'fields_checked': list(FIELDS),
        'ay1': ay1, 'ay2': ay2, 'checked_but_empty_sources': checked_empty,
        'passed': passed,
        'findings': findings,
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'shared_vocabulary_fields', result)
    print('shared_vocabulary_fields: %s' % ('PASS (rule satisfied for every field)' if result['passed']
                                            else 'FAIL (a type mismatch was found; see findings)'))
    for f in result['findings']:
        print('  -', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
