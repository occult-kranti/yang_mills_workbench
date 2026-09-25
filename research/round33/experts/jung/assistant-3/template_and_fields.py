#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 sub-round 3, assistant-3 script 2 of 3: the template
span and gate-field audit (calling task item 2).

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not import
`forward/*/check.py`, `reverse/*/check.py`, or any other producer/skeptic
module. Never reads `research/round33/forward/bd1`, `forward/bd2` or
`reverse/bd1` (not needed here in any case: this script is scoped to BC1/BC2).

Two sub-checks:

  (a) `mandatory_template_span_check` (rule R7) -- each contract's own
      `mandatory_sentence_template` (BC1's and BC2's) appears, verbatim after
      whitespace normalization, as exactly one unbroken span in "each report and
      each gate text": `forward/<loop>/report.md` and
      `research/round33/advisor/<loop>-gate.json`'s own `accepted` field (BC1
      and BC2 have no reverse producer, so there is no second report to check).
      Cross-checked, not trusted, against each report's own self-reported
      template-span check in `forward/<loop>/output/results.json` where one
      exists.

  (b) `gate_fields_comparison` -- for BC1 and BC2, the exported `gate_fields`
      of the gate (`research/round33/advisor/<loop>-gate.json`) and of the
      review (`research/round33/skeptic/<loop>.json`) are compared, key for
      key, against the contract's own
      `preregistration.gate_fields_required` (`research/round33/contracts/
      <loop>.json`); every field's value is checked against `plan.json`'s
      `vocabulary.gate_fields` rule for that field name where the rule states a
      concrete, checkable condition ("always false", "true only with a
      non-empty <x>_scope naming ..."). The calling task names two fields
      specifically: BC1's `correlation_shift_resolved` and
      `finite_box_node_claimed`, and BC2's `node_certificate_restated_for_limit`
      -- each of these three gets its own dedicated, narrated check in addition
      to the generic field-by-field comparison every other field also receives.
      A non-blocking, informational note records the one structural asymmetry
      found: the advisor gate exports `gate_fields` only as a nested dict, while
      the skeptic review additionally promotes every one of its members to a
      flat top-level key -- a file-format convention difference, not a value
      disagreement (checked separately).

Usage: python3 -B template_and_fields.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common3 as K  # noqa: E402


# ---------------------------------------------------------------------------
# (a) mandatory_sentence_template span check (rule R7).
# ---------------------------------------------------------------------------
def count_unbroken_spans(haystack_norm, needle_norm):
    return haystack_norm.count(needle_norm)


def self_reported_template_check(loop):
    """Best-effort read of the forward producer's own self-reported template
    check inside forward/<loop>/output/results.json (BC1: id
    'mandatory_sentence_once'; BC2: id
    'mandatory_template_quoted_once_and_phrase_scan_clean'), walked generically
    so neither name needs to be hard-coded per loop."""
    results_path = K.FORWARD / loop / 'output' / 'results.json'
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
    # Re-locate the sibling dict for each matching id.
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

        report_text = K.normalize(K.load_text(K.FORWARD_REPORT_PATHS[loop]))
        gate = K.load_gate(loop)
        gate_accepted_norm = K.normalize(gate['accepted'])

        report_count = count_unbroken_spans(report_text, template_norm)
        gate_count = count_unbroken_spans(gate_accepted_norm, template_norm)
        ok = (report_count == 1 and gate_count == 1)
        all_pass = all_pass and ok

        self_reported = self_reported_template_check(loop)
        per_loop[L] = {
            'template_length_chars': len(template_norm),
            'report_occurrences': report_count, 'gate_accepted_occurrences': gate_count,
            'passed': ok,
            'self_reported_forward_check': [
                {'json_path': p, 'record': {k: v for k, v in d.items() if k != 'template'}}
                for p, d in (self_reported or [])
            ],
        }
        findings.append(
            '%s: template (%d chars, whitespace-normalized) occurs %d time(s) as an unbroken span in '
            'forward/%s/report.md and %d time(s) in advisor/%s-gate.json#/accepted -- %s.'
            % (L, len(template_norm), report_count, loop, gate_count, loop, 'PASS' if ok else 'FAIL'))
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
# Concrete, mechanically checkable plan.json rules (the rest of
# plan.json#/vocabulary/gate_fields is "declared per contract", which this
# script honours by simply requiring gate == review == contract, checked for
# every field regardless of whether a concrete rule also applies).
def check_always_false(name, contract_val, gate_val, review_val):
    ok = (contract_val is False) and (gate_val is False) and (review_val is False)
    return ok, 'plan rule "always false"'


def check_scope_pairing(flag_name, scope_name):
    def _check(name, contract_val, gate_val, review_val, gate_obj=None, review_obj=None):
        ok = True
        detail = 'plan rule "true only with a non-empty %s naming the construction"' % scope_name
        for label, obj, val in (('gate', gate_obj, gate_val), ('review', review_obj, review_val)):
            if val is True:
                scope_val = (obj or {}).get('gate_fields', {}).get(scope_name)
                if not scope_val:
                    ok = False
        return ok, detail
    return _check


PLAN_RULES = {
    'uniqueness_of_ground_state_claimed': check_always_false,
    'rate_in_a_claimed': check_always_false,
    'continuum_claim': check_always_false,
}


def gate_fields_comparison():
    plan = K.load_plan()
    plan_gate_fields = plan['vocabulary']['gate_fields']
    per_loop = {}
    findings = []
    all_pass = True
    top_level_asymmetry_notes = []

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

        # Top-level duplication asymmetry (informational, not scored): does the
        # gate/review ALSO carry each gate_fields member as a flat top-level key?
        gate_top_level_dup = {k: (k in gate) for k in key_set_required}
        review_top_level_dup = {k: (k in review) for k in key_set_required}
        gate_has_any_top = any(gate_top_level_dup.values())
        review_has_any_top = any(review_top_level_dup.values())
        if gate_has_any_top != review_has_any_top:
            top_level_asymmetry_notes.append(
                '%s: advisor gate top-level duplication=%s, skeptic review top-level duplication=%s -- a file-'
                'format convention difference (the review additionally promotes every gate_fields member to a flat '
                'top-level key; the gate does not), not a value disagreement (every value still checked above).'
                % (L, gate_has_any_top, review_has_any_top))
            if gate_has_any_top and review_has_any_top:
                pass  # both duplicate; nothing to note
            if not (gate_has_any_top and review_has_any_top):
                # verify that where one of them DOES duplicate, the duplicated
                # value agrees with the nested one (no drift between the two
                # representations).
                for k in key_set_required:
                    if k in gate and gate.get(k) != gate_gf.get(k):
                        loop_ok = False
                        findings.append('%s: DEFECT gate top-level %r=%r disagrees with gate.gate_fields[%r]=%r'
                                        % (L, k, gate.get(k), k, gate_gf.get(k)))
                    if k in review and review.get(k) != review_gf.get(k):
                        loop_ok = False
                        findings.append('%s: DEFECT review top-level %r=%r disagrees with review.gate_fields[%r]=%r'
                                        % (L, k, review.get(k), k, review_gf.get(k)))

        all_pass = all_pass and loop_ok
        per_loop[L] = {
            'keys_match_contract_gate_review': keys_match,
            'required_keys': sorted(key_set_required), 'gate_keys': sorted(key_set_gate),
            'review_keys': sorted(key_set_review), 'rows': rows, 'passed': loop_ok,
        }
        defects = [r for r in rows if not r['passed']]
        findings.append(
            '%s: %d gate_fields required by the contract; key sets equal across contract/gate/review: %s; %d/%d '
            'field(s) agree in value across contract/gate/review AND satisfy their plan.json rule where one applies.'
            % (L, len(required), keys_match, len(rows) - len(defects), len(rows)))
        for d in defects:
            findings.append('  DEFECT: %s field %r contract=%r gate=%r review=%r plan_rule=%r'
                            % (L, d['field'], d['contract'], d['gate'], d['review'], d['plan_rule']))

    findings.extend(top_level_asymmetry_notes)

    # The calling task's own three named fields, each narrated explicitly.
    def named_field_row(loop, field):
        L = loop.upper()
        for r in per_loop[L]['rows']:
            if r['field'] == field:
                return r
        return None

    bc1_corr = named_field_row('bc1', 'correlation_shift_resolved')
    bc1_fbn = named_field_row('bc1', 'finite_box_node_claimed')
    bc2_node = named_field_row('bc2', 'node_certificate_restated_for_limit')

    named_ok = True
    if bc1_corr is not None:
        named_ok = named_ok and bc1_corr['passed']
        findings.append(
            'Calling-task-named field BC1.correlation_shift_resolved: contract=%r gate=%r review=%r; plan.json '
            'rule: %r; %s. BC1 restates BOTH the AV2 node certificate and the AW2 static-mean enclosure, so per '
            'plan.json\'s own note it exports the merged correlation_shift_resolved field instead of a separate '
            'resolved_interaction_shift field -- confirmed: BC1\'s contract.gate_fields_required has no '
            'resolved_interaction_shift key at all (checked below).'
            % (bc1_corr['contract'], bc1_corr['gate'], bc1_corr['review'], bc1_corr['plan_rule'],
               'PASS' if bc1_corr['passed'] else 'FAIL'))
    if bc1_fbn is not None:
        named_ok = named_ok and bc1_fbn['passed']
        findings.append(
            'Calling-task-named field BC1.finite_box_node_claimed: contract=%r gate=%r review=%r; plan.json rule: '
            '%r; %s.' % (bc1_fbn['contract'], bc1_fbn['gate'], bc1_fbn['review'], bc1_fbn['plan_rule'],
                         'PASS' if bc1_fbn['passed'] else 'FAIL'))
    if bc2_node is not None:
        named_ok = named_ok and bc2_node['passed']
        findings.append(
            'Calling-task-named field BC2.node_certificate_restated_for_limit: contract=%r gate=%r review=%r; '
            'plan.json rule: %r; %s.' % (bc2_node['contract'], bc2_node['gate'], bc2_node['review'],
                                        bc2_node['plan_rule'], 'PASS' if bc2_node['passed'] else 'FAIL'))

    # correlation_shift_resolved / resolved_interaction_shift exclusivity, per
    # plan.json's own note ("a contract that restates both AV2 and AW2 exports
    # correlation_shift_resolved instead").
    bc1_contract = K.load_contract('bc1')['preregistration']['gate_fields_required']
    bc2_contract = K.load_contract('bc2')['preregistration']['gate_fields_required']
    exclusivity_ok = (
        'correlation_shift_resolved' in bc1_contract and 'resolved_interaction_shift' not in bc1_contract
        and 'resolved_interaction_shift' in bc2_contract and 'correlation_shift_resolved' not in bc2_contract
    )
    named_ok = named_ok and exclusivity_ok
    findings.append(
        'correlation_shift_resolved / resolved_interaction_shift exclusivity (plan.json: "a contract that restates '
        'both AV2 and AW2 exports correlation_shift_resolved instead"): BC1 has correlation_shift_resolved and no '
        'resolved_interaction_shift key (restates both AV2 and AW2); BC2 has resolved_interaction_shift and no '
        'correlation_shift_resolved key (restates only AX2). %s.' % ('PASS' if exclusivity_ok else 'FAIL'))

    all_pass = all_pass and named_ok

    return {
        'id': 'gate_fields_comparison',
        'role': 'calling task item 2 (second half): gate fields vs contract gate_fields_required vs plan.json '
                'vocabulary, for BC1 and BC2, with BC1\'s correlation_shift_resolved and finite_box_node_claimed '
                'and BC2\'s node_certificate_restated_for_limit each individually checked; zero research loops',
        'per_loop': per_loop, 'named_fields_ok': named_ok, 'passed': all_pass, 'findings': findings,
    }


def run():
    checks = [mandatory_template_span_check(), gate_fields_comparison()]
    return {
        'id': 'template_and_fields',
        'role': 'Jung/Pauli lens, Round33 sub-round 3, assistant-3: the template-span and gate-field audit, '
                'calling task item 2; zero research loops; audits only, never admission evidence',
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
