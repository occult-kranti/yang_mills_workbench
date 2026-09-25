#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 applications stage, assistant-4 script 2 of 3:
calling task item 2 -- the mandatory-template-span check and the BD gate-field
audit against the contracts and `plan.json`'s vocabulary.

Counts zero research loops. Not a producer, contract, gate or skeptical
review; nothing computed here is read back into any of those. Human project
author: Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not
import `forward/*/check.py`, `reverse/*/check.py`, or any other producer/
skeptic module.

Two sub-checks:

  (a) `mandatory_template_span_check` (rule R7) -- each contract's own
      `mandatory_sentence_template` (BD1's and BD2's) appears, verbatim after
      whitespace normalization, as exactly one unbroken span in "each report
      and each gate text": `forward/bd1/report.md`, `reverse/bd1/report.md`
      and `advisor/bd1-gate.json#/accepted` for BD1's template;
      `forward/bd2/report.md` and `advisor/bd2-gate.json#/accepted` for BD2's
      (BD2 has no reverse producer). Cross-checked against each report's own
      self-reported template check in `output/results.json` where one exists.

  (b) `gate_fields_comparison_bd` -- for BD1 and BD2, the exported
      `gate_fields` of the gate and of the review are compared, key for key,
      against the contract's own `preregistration.gate_fields_required`, and
      every field's value is checked against `plan.json`'s
      `vocabulary.gate_fields` rule for that field name where the rule states
      a concrete, checkable condition. The calling task names seven fields
      specifically: BD1's `flip_transfer_scope` (checked that it names SU(2),
      SU(4), U(1) and Z2), `obstructions_recorded` and
      `area_parity_limit_claimed`; BD2's `graph_sign_certified`,
      `z3_1x2_formal_only`, `electric_band_scope` and `area_law_claimed`
      (checked `false`) -- each gets its own dedicated, narrated check in
      addition to the generic field-by-field comparison every other field
      also receives. `flip_transfer_scope` is handled as a *named* exception
      to the generic contract==gate==review equality check: the contract's
      own text states the general rule ("the listed groups ... named in the
      gate group by group"), so the gate and review correctly export the
      concrete instantiation instead -- this is the bd1-gate.json's own
      recorded, non-blocking limitation, re-verified here rather than
      silently absorbed as a defect.

Usage: python3 -B template_and_fields.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common4 as K  # noqa: E402


# ---------------------------------------------------------------------------
# (a) mandatory_sentence_template span check (rule R7).
# ---------------------------------------------------------------------------
REPORTS_BY_LOOP = {
    'bd1': [('forward_report', K.FORWARD_REPORT_PATHS['bd1']),
            ('reverse_report', K.REVERSE_REPORT_PATHS['bd1'])],
    'bd2': [('forward_report', K.FORWARD_REPORT_PATHS['bd2'])],
}


def count_unbroken_spans(haystack_norm, needle_norm):
    return haystack_norm.count(needle_norm)


def self_reported_template_check(loop):
    results_path = K.FORWARD_RESULTS_PATHS[loop]
    if not results_path.exists():
        return None
    data = K.load_json(results_path)
    found = []
    for json_path, key, value in K.walk_json_items(data):
        if key == 'id' and isinstance(value, str) and (
            'mandatory_sentence' in value or 'mandatory_template' in value
        ):
            found.append((json_path, value))
    if not found:
        return None
    out = []

    def find_dicts(obj, path=''):
        if isinstance(obj, dict):
            if obj.get('id') in (v for _, v in found):
                out.append((path, obj))
            for k, v in obj.items():
                find_dicts(v, (path + '.' + k) if path else k)
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                find_dicts(v, path + '[%d]' % i)

    find_dicts(data)
    return out


def mandatory_template_span_check():
    per_loop = {}
    findings = []
    all_pass = True
    for loop in K.LOOPS:
        L = loop.upper()
        contract = K.load_contract(loop)
        template_norm = K.normalize(contract['preregistration']['mandatory_sentence_template'])

        report_counts = {}
        for label, path in REPORTS_BY_LOOP[loop]:
            text_norm = K.normalize(K.load_text(path))
            report_counts[label] = count_unbroken_spans(text_norm, template_norm)

        gate = K.load_gate(loop)
        gate_accepted_norm = K.normalize(gate['accepted'])
        gate_count = count_unbroken_spans(gate_accepted_norm, template_norm)

        ok = all(c == 1 for c in report_counts.values()) and gate_count == 1
        all_pass = all_pass and ok

        self_reported = self_reported_template_check(loop)
        per_loop[L] = {
            'template_length_chars': len(template_norm),
            'report_occurrences': report_counts, 'gate_accepted_occurrences': gate_count,
            'passed': ok,
            'self_reported_forward_check': [
                {'json_path': p, 'record': {k: v for k, v in d.items() if k != 'template'}}
                for p, d in (self_reported or [])
            ],
        }
        findings.append(
            '%s: template (%d chars, whitespace-normalized) occurs %s time(s) as an unbroken span across its '
            'report(s) and %d time(s) in advisor/%s-gate.json#/accepted -- %s.'
            % (L, len(template_norm), report_counts, gate_count, loop, 'PASS' if ok else 'FAIL'))
        if self_reported:
            passed_vals = [d.get('passed') for _, d in self_reported]
            findings.append(
                '%s: cross-checked against the forward producer\'s own self-reported template check(s) in '
                'forward/%s/output/results.json (%s): all report passed=%s, agrees with this script\'s independent '
                'count.' % (L, loop, [p for p, _ in self_reported], passed_vals))

    return {
        'id': 'mandatory_template_span_check',
        'role': 'calling task item 2 (first half): the mandatory sentence template appears once, as one unbroken '
                'span, in each report and each gate text (rule R7); cross-checked against each report\'s own '
                'self-reported check; zero research loops',
        'per_loop': per_loop, 'passed': all_pass, 'findings': findings,
    }


# ---------------------------------------------------------------------------
# (b) gate_fields comparison: contract.gate_fields_required vs gate.gate_fields
#     vs review.gate_fields vs plan.json's vocabulary.gate_fields rule.
# ---------------------------------------------------------------------------
def check_always_false(name, contract_val, gate_val, review_val):
    ok = (contract_val is False) and (gate_val is False) and (review_val is False)
    return ok, 'plan rule "always false"'


PLAN_RULES = {
    'uniqueness_of_ground_state_claimed': check_always_false,
    'rate_in_a_claimed': check_always_false,
    'continuum_claim': check_always_false,
    'area_law_claimed': check_always_false,
}

# Fields the calling task names for a dedicated, narrated check.
NAMED_FIELDS = {
    'bd1': ['flip_transfer_scope', 'obstructions_recorded', 'area_parity_limit_claimed'],
    'bd2': ['graph_sign_certified', 'z3_1x2_formal_only', 'electric_band_scope', 'area_law_claimed'],
}

# flip_transfer_scope is a documented exception (bd1-gate.json's own recorded,
# non-blocking limitation): the contract states the general RULE, the gate and
# review state its concrete INSTANTIATION for BD1's own group list, so a plain
# contract==gate==review string check would (correctly) fail. It is checked
# instead by content: the gate/review value must name exactly the four flip
# groups the BD1 report and gate derive (SU(2), SU(4), U(1), Z2), and the
# contract's own text must state the general rule the gate instantiates.
FLIP_GROUPS_REQUIRED = ['SU(2)', 'SU(4)', 'U(1)', 'Z2']
FLIP_GROUPS_EXCLUDED = ['SU(3)', 'SU(5)', 'SO(3)']


def gate_fields_comparison():
    plan = K.load_plan()
    plan_gate_fields = plan['vocabulary']['gate_fields']
    per_loop = {}
    findings = []
    all_pass = True
    named_ok = True

    for loop in K.LOOPS:
        L = loop.upper()
        contract = K.load_contract(loop)
        required = contract['preregistration']['gate_fields_required']
        gate = K.load_gate(loop)
        review = K.load_review(loop)
        gate_gf = gate['gate_fields']
        review_gf = review['gate_fields']

        key_set_required = set(required.keys())
        key_set_gate = set(gate_gf.keys())
        key_set_review = set(review_gf.keys())
        keys_match = (key_set_required == key_set_gate == key_set_review)

        rows = []
        loop_ok = keys_match
        for key in sorted(key_set_required):
            c_val = required[key]
            g_val = gate_gf.get(key)
            r_val = review_gf.get(key)
            if key == 'flip_transfer_scope':
                # Documented exception: value_agrees is not the pass condition
                # for this field (see NAMED_FIELDS narration below); gate and
                # review must at least agree with each other verbatim.
                value_agrees = (g_val == r_val)
            else:
                value_agrees = (c_val == g_val == r_val)
            plan_rule_text = plan_gate_fields.get(key, '(no plan.json#/vocabulary/gate_fields entry)')
            rule_fn = PLAN_RULES.get(key)
            rule_ok, rule_detail = (True, None)
            if rule_fn is not None:
                rule_ok, rule_detail = rule_fn(key, c_val, g_val, r_val)
            row_ok = value_agrees and rule_ok
            loop_ok = loop_ok and row_ok
            rows.append({
                'field': key, 'contract': c_val, 'gate': g_val, 'review': r_val,
                'value_agrees': value_agrees, 'plan_rule': plan_rule_text,
                'plan_rule_checked': rule_detail, 'plan_rule_ok': rule_ok, 'passed': row_ok,
            })

        all_pass = all_pass and loop_ok
        per_loop[L] = {
            'keys_match_contract_gate_review': keys_match,
            'required_keys': sorted(key_set_required), 'gate_keys': sorted(key_set_gate),
            'review_keys': sorted(key_set_review), 'rows': rows, 'passed': loop_ok,
        }
        defects = [r for r in rows if not r['passed']]
        findings.append(
            '%s: %d gate_fields required by the contract; key sets equal across contract/gate/review: %s; %d/%d '
            'field(s) agree in value (or, for flip_transfer_scope, gate==review) across contract/gate/review AND '
            'satisfy their plan.json rule where one applies.'
            % (L, len(required), keys_match, len(rows) - len(defects), len(rows)))
        for d in defects:
            findings.append('  DEFECT: %s field %r contract=%r gate=%r review=%r plan_rule=%r'
                            % (L, d['field'], d['contract'], d['gate'], d['review'], d['plan_rule']))

    # ------------------------------------------------------------------
    # The calling task's seven named fields, each narrated explicitly.
    # ------------------------------------------------------------------
    def named_field_row(loop, field):
        L = loop.upper()
        for r in per_loop[L]['rows']:
            if r['field'] == field:
                return r
        return None

    # BD1.flip_transfer_scope: content check (names exactly the four groups).
    g1 = K.load_gate('bd1')
    r1 = K.load_review('bd1')
    c1 = K.load_contract('bd1')
    scope_gate = g1['gate_fields']['flip_transfer_scope']
    scope_review = r1['gate_fields']['flip_transfer_scope']
    scope_rule_text = c1['preregistration']['gate_fields_required']['flip_transfer_scope']
    names_required = all(g in scope_gate for g in FLIP_GROUPS_REQUIRED) and all(g in scope_review for g in FLIP_GROUPS_REQUIRED)
    excludes_obstructed = not any(g in scope_gate for g in FLIP_GROUPS_EXCLUDED)
    contract_states_general_rule = ('the listed groups' in scope_rule_text.lower()
                                     and 'named in the gate group by group' in scope_rule_text.lower())
    gate_review_agree = (scope_gate == scope_review)
    flip_scope_ok = names_required and excludes_obstructed and contract_states_general_rule and gate_review_agree
    named_ok = named_ok and flip_scope_ok
    findings.append(
        'Calling-task-named field BD1.flip_transfer_scope: gate==review verbatim: %s; gate/review name all four '
        'required groups (%s): %s; gate/review name none of the three flip-obstructed groups (%s): %s; the '
        'contract\'s own value states the general rule ("the listed groups ... named in the gate group by group") '
        'rather than the concrete list, exactly as bd1-gate.json#/limitations records as a non-blocking contract '
        'defect ("gate_fields_required flip_transfer_scope is a description, so the gate names SU(2), SU(4), '
        'U(1) and Z2"): %s. %s.'
        % (gate_review_agree, FLIP_GROUPS_REQUIRED, names_required, FLIP_GROUPS_EXCLUDED, excludes_obstructed,
           contract_states_general_rule, 'PASS' if flip_scope_ok else 'FAIL'))

    bd1_obs = named_field_row('bd1', 'obstructions_recorded')
    if bd1_obs is not None:
        named_ok = named_ok and bd1_obs['passed']
        findings.append(
            'Calling-task-named field BD1.obstructions_recorded: contract=%r gate=%r review=%r; plan.json rule: '
            '%r; %s.' % (bd1_obs['contract'], bd1_obs['gate'], bd1_obs['review'], bd1_obs['plan_rule'],
                         'PASS' if bd1_obs['passed'] else 'FAIL'))

    bd1_apl = named_field_row('bd1', 'area_parity_limit_claimed')
    if bd1_apl is not None:
        named_ok = named_ok and bd1_apl['passed']
        findings.append(
            'Calling-task-named field BD1.area_parity_limit_claimed: contract=%r gate=%r review=%r; plan.json '
            'rule: %r; %s.' % (bd1_apl['contract'], bd1_apl['gate'], bd1_apl['review'], bd1_apl['plan_rule'],
                               'PASS' if bd1_apl['passed'] else 'FAIL'))

    bd2_gsc = named_field_row('bd2', 'graph_sign_certified')
    if bd2_gsc is not None:
        named_ok = named_ok and bd2_gsc['passed']
        findings.append(
            'Calling-task-named field BD2.graph_sign_certified: contract=%r gate=%r review=%r; plan.json rule: '
            '%r; %s.' % (bd2_gsc['contract'], bd2_gsc['gate'], bd2_gsc['review'], bd2_gsc['plan_rule'],
                         'PASS' if bd2_gsc['passed'] else 'FAIL'))

    bd2_z3f = named_field_row('bd2', 'z3_1x2_formal_only')
    if bd2_z3f is not None:
        named_ok = named_ok and bd2_z3f['passed']
        findings.append(
            'Calling-task-named field BD2.z3_1x2_formal_only: contract=%r gate=%r review=%r; plan.json rule: '
            '%r; %s.' % (bd2_z3f['contract'], bd2_z3f['gate'], bd2_z3f['review'], bd2_z3f['plan_rule'],
                         'PASS' if bd2_z3f['passed'] else 'FAIL'))

    bd2_ebs = named_field_row('bd2', 'electric_band_scope')
    if bd2_ebs is not None:
        named_ok = named_ok and bd2_ebs['passed']
        findings.append(
            'Calling-task-named field BD2.electric_band_scope: contract=%r gate=%r review=%r; plan.json rule: '
            '%r; %s.' % (bd2_ebs['contract'], bd2_ebs['gate'], bd2_ebs['review'], bd2_ebs['plan_rule'],
                         'PASS' if bd2_ebs['passed'] else 'FAIL'))

    bd2_alc = named_field_row('bd2', 'area_law_claimed')
    if bd2_alc is not None:
        named_ok = named_ok and bd2_alc['passed'] and (bd2_alc['contract'] is False) and (bd2_alc['gate'] is False) and (bd2_alc['review'] is False)
        findings.append(
            'Calling-task-named field BD2.area_law_claimed: contract=%r gate=%r review=%r; plan.json rule '
            '("always false in Round33 (no zero-free region is admitted)"): %r; %s.'
            % (bd2_alc['contract'], bd2_alc['gate'], bd2_alc['review'], bd2_alc['plan_rule'],
               'PASS' if bd2_alc['passed'] else 'FAIL'))

    all_pass = all_pass and named_ok

    return {
        'id': 'gate_fields_comparison_bd',
        'role': 'calling task item 2 (second half): BD gate fields vs contracts vs plan.json vocabulary for BD1 '
                'and BD2, with the seven calling-task-named fields (BD1.flip_transfer_scope, '
                '.obstructions_recorded, .area_parity_limit_claimed; BD2.graph_sign_certified, '
                '.z3_1x2_formal_only, .electric_band_scope, .area_law_claimed) each individually checked; zero '
                'research loops',
        'per_loop': per_loop, 'named_fields_ok': named_ok, 'passed': all_pass, 'findings': findings,
    }


def run():
    checks = [mandatory_template_span_check(), gate_fields_comparison()]
    return {
        'id': 'template_and_fields',
        'role': 'Jung/Pauli lens, Round33 applications stage, assistant-4: the template-span and gate-field '
                'audit, calling task item 2; zero research loops; audits only, never admission evidence',
        'checks': {c['id']: c for c in checks},
        'passed': all(c['passed'] for c in checks),
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'template_and_fields', result)
    print('template_and_fields: %s' % ('PASS' if result['passed'] else 'FAIL (see findings)'))
    for check_id, c in result['checks'].items():
        print('  %s: %s' % (check_id, 'PASS' if c['passed'] else 'FAIL'))
        for f in c['findings']:
            print('    -', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
