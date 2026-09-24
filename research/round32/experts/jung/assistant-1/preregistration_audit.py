#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 1, assistant script 3 of 3: pre-registration audit.

Pre-registration audit / test only (loop3-signoff.md section 4, item 3 is the
sign-off's summary; this is the script promised by loop2-response.md section 5 /
the calling task). Counts zero research loops; not a producer, contract, gate or
skeptical review, and nothing here is read back into any of those. Human project
author: Hruday N M (BUNZEEY); AI-assisted.

Checks, pass/fail per item:

 1-2. Every field of the Jung lens's pre-registration block (loop2-response.md
      section 2, with the skeptic's four amendments per loop3-signoff.md section 2)
      is present in the AV1 / AV2 contract's `preregistration` object with an
      allowed value.
 3-4. `preregistration.controls_required.ids` equals the contract's `controls`
      list, for AV1 and AV2.
 5-6. The AV1 forward / reverse `output/results.json` each contain every control id
      from the AV1 contract's `controls` list among their `checks` ids.
 7-8. The AV1 target `1/2500000` is read from the contract (not hard-coded) by the
      forward and the reverse `check.py`: the contract path string is present, and
      no literal `2500000` (the target's denominator) appears anywhere outside a
      value that is compared against the parsed contract target.
 9-10. The gate's `accepted` / `limitations` fields equal the corresponding fields
      in `skeptic/av1.json` (`supported_statement` / `limitations`).

Usage: python3 -B preregistration_audit.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402

ALLOWED_MODEL_ID_PREFIXES = ('AQ_patterned_zero_selected', 'AQ_uniform_routeB', 'FG(')
ALLOWED_STATE_PROVENANCE_PREFIXES = (
    'AQ1_centered_whole_star_subsequence', 'finite_volume_N=', 'finite_graph_ground')
ALLOWED_CENTERING = ('vector', 'none')
ALLOWED_REFERENCE_ROUTE = ('haar', 'selected_strip', 'own_finite_graph')
ALLOWED_COMPARATOR = ('<=', '>=')
ALLOWED_DIRECTION = ('paired', 'single+skeptic', 'statement-only')
EXPECTED_OUTCOME_TYPES = ['accepted_within_scope', 'limited', 'insufficient']
SUB_LABELS_ALLOWED = ['reference_unresolved', 'sign_certified_finite_graph', 'sign_certified_below_cap',
                       'static_not_dynamic', 'uniform_local_closeness_not_uniqueness']
TEMPLATE_CLAIM_EXCLUSIONS = {
    'free reference inside enclosure => no interaction claim', 'uniqueness of the AQ state',
    'whole-sequence convergence or rate in N', 'continuum or weak coupling',
    'transfer from a finite graph', 'relabelling a static shift as dynamical', 'scientific priority'}
HASH_BINDING_FIELDS = ('contract_sha256_in_producer_inputs', 'check_py_reads_target_and_reference_from_contract',
                        'check_py_sha256_recorded_before_full_size_evaluation')


def field_check(desc, condition):
    return {'field': desc, 'passed': bool(condition)}


def audit_preregistration_block(pre, label):
    """Every field of the Jung lens's loop2-response.md pre-registration template,
    present in `pre` with an allowed value. Returns a list of per-field results."""
    out = []
    out.append(field_check('schema', pre.get('schema') == 'hnm-r32-prereg-v1'))
    out.append(field_check('frozen_before_any_outcome', pre.get('frozen_before_any_outcome') is True))
    mid = pre.get('model_id')
    out.append(field_check('model_id', isinstance(mid, str) and mid.startswith(ALLOWED_MODEL_ID_PREFIXES)))
    triple = pre.get('selected_triple_alpha_units')
    triple_ok = isinstance(triple, list) and len(triple) == 3
    if triple_ok:
        try:
            [K.rat(x) for x in triple]
        except K.AuditError:
            triple_ok = False
    out.append(field_check('selected_triple_alpha_units', triple_ok))
    tau = pre.get('tau')
    tau_ok = isinstance(tau, dict) and {'value', 'signs_evaluated', 'is_model_change_vs_previous_loop',
                                         'rule_if_chosen_later'} <= set(tau)
    if tau_ok:
        try:
            K.rat(tau['value'])
        except K.AuditError:
            tau_ok = False
        tau_ok = tau_ok and tau['signs_evaluated'] == ['+', '-']
        tau_ok = tau_ok and isinstance(tau['is_model_change_vs_previous_loop'], bool)
        tau_ok = tau_ok and (tau['rule_if_chosen_later'] is None or isinstance(tau['rule_if_chosen_later'], str))
    out.append(field_check('tau', tau_ok))
    sp = pre.get('state_provenance')
    out.append(field_check('state_provenance', isinstance(sp, str) and sp.startswith(ALLOWED_STATE_PROVENANCE_PREFIXES)))
    out.append(field_check('clock', pre.get('clock') ==
                            's=alpha*t_E/hbar, theta=alpha*t/hbar; u=s/8 and exponent 24 forbidden in packets'))
    obs = pre.get('observable')
    obs_ok = isinstance(obs, dict) and {'id', 'centering', 'reference_value_exact', 'reference_route'} <= set(obs)
    if obs_ok:
        obs_ok = (isinstance(obs['id'], str) and obs['id'] != '' and obs['centering'] in ALLOWED_CENTERING
                  and isinstance(obs['reference_value_exact'], str) and obs['reference_value_exact'] != ''
                  and obs['reference_route'] in ALLOWED_REFERENCE_ROUTE)
    out.append(field_check('observable', obs_ok))
    nodes = pre.get('nodes')
    nodes_ok = isinstance(nodes, dict) and {'s_values', 'post_hoc_node_selection', 'pilot_runs'} <= set(nodes)
    if nodes_ok:
        pr = nodes['pilot_runs']
        nodes_ok = (isinstance(nodes['s_values'], list) and nodes['post_hoc_node_selection'] == 'forbidden'
                    and isinstance(pr, dict) and isinstance(pr.get('declared'), list)
                    and pr.get('excluded_from_count') is True)
    out.append(field_check('nodes', nodes_ok))
    eti = pre.get('error_terms_itemized')
    out.append(field_check('error_terms_itemized', isinstance(eti, list) and len(eti) > 0
                            and all(isinstance(x, str) for x in eti)))
    target = pre.get('target')
    target_ok = isinstance(target, dict) and {'quantity', 'value', 'comparator'} <= set(target)
    if target_ok:
        try:
            K.rat(target['value'])
        except K.AuditError:
            target_ok = False
        target_ok = target_ok and isinstance(target['quantity'], str) and target['quantity'] != ''
        target_ok = target_ok and target['comparator'] in ALLOWED_COMPARATOR
    out.append(field_check('target', target_ok))
    out.append(field_check('expected_outcome_types', pre.get('expected_outcome_types') == EXPECTED_OUTCOME_TYPES))
    out.append(field_check('sub_labels_allowed', pre.get('sub_labels_allowed') == SUB_LABELS_ALLOWED))
    cr = pre.get('controls_required')
    out.append(field_check('controls_required', isinstance(cr, dict) and isinstance(cr.get('ids'), list)
                            and len(cr['ids']) > 0 and all(isinstance(x, str) for x in cr['ids'])))
    ce = pre.get('claim_exclusions')
    out.append(field_check('claim_exclusions', isinstance(ce, list) and TEMPLATE_CLAIM_EXCLUSIONS <= set(ce)))
    hb = pre.get('hash_binding')
    out.append(field_check('hash_binding', isinstance(hb, dict) and set(hb) == set(HASH_BINDING_FIELDS)
                            and all(hb[k] is True for k in HASH_BINDING_FIELDS)))
    out.append(field_check('direction', pre.get('direction') in ALLOWED_DIRECTION))
    return out


def controls_required_equals_contract_controls(contract):
    pre = contract['preregistration']
    ids = pre.get('controls_required', {}).get('ids')
    controls = contract.get('controls')
    return {'equal': ids == controls, 'ids_len': len(ids) if ids is not None else None,
            'controls_len': len(controls) if controls is not None else None,
            'only_in_ids': sorted(set(ids or []) - set(controls or [])),
            'only_in_controls': sorted(set(controls or []) - set(ids or []))}


def results_contain_every_control_id(contract, results):
    controls = set(contract['controls'])
    have = set(c['id'] for c in results.get('checks', []))
    missing = sorted(controls - have)
    return {'all_present': not missing, 'missing': missing, 'n_controls': len(controls), 'n_checks': len(have)}


def target_read_from_contract(check_py_path, target_denominator='2500000'):
    text = check_py_path.read_text(encoding='utf-8')
    contract_path_present = 'research/round32/contracts/av1.json' in text
    # The target's exact denominator must not appear as a literal anywhere in the
    # source; if it did, a human reviewer would need to confirm it only appears in
    # a comparison against the parsed contract value. Here it is simply absent.
    literal_occurrences = [m.start() for m in re.finditer(re.escape(target_denominator), text)]
    return {'contract_path_present': contract_path_present,
            'target_denominator_literal_occurrences': len(literal_occurrences),
            'no_hardcoded_target_literal': len(literal_occurrences) == 0,
            'passed': contract_path_present and len(literal_occurrences) == 0}


def gate_matches_skeptic():
    gate = K.load_json(K.GATE_AV1)
    skeptic = K.load_json(K.SKEPTIC_AV1_JSON)
    accepted_match = gate.get('accepted') == skeptic.get('supported_statement')
    limitations_match = gate.get('limitations') == skeptic.get('limitations')
    return {'gate_accepted_equals_skeptic_supported_statement': accepted_match,
            'gate_limitations_equals_skeptic_limitations': limitations_match,
            'note': 'skeptic/av1.json has no "accepted" key; its "supported_statement" is the field the gate\'s '
                    '"accepted" narrative is bound to (both are the verbatim admitted sentence).'}


def run():
    c1 = K.av1_contract()
    c2 = K.av2_contract()

    items = []

    fields1 = audit_preregistration_block(c1['preregistration'], 'AV1')
    items.append({'item': 'av1_preregistration_fields_present_and_allowed',
                  'passed': all(f['passed'] for f in fields1), 'fields': fields1})

    fields2 = audit_preregistration_block(c2['preregistration'], 'AV2')
    items.append({'item': 'av2_preregistration_fields_present_and_allowed',
                  'passed': all(f['passed'] for f in fields2), 'fields': fields2})

    cr1 = controls_required_equals_contract_controls(c1)
    items.append({'item': 'av1_controls_required_ids_equals_contract_controls', 'passed': cr1['equal'], 'detail': cr1})

    cr2 = controls_required_equals_contract_controls(c2)
    items.append({'item': 'av2_controls_required_ids_equals_contract_controls', 'passed': cr2['equal'], 'detail': cr2})

    fwd_results = K.load_json(K.FORWARD_AV1_RESULTS)
    fwd_cov = results_contain_every_control_id(c1, fwd_results)
    items.append({'item': 'av1_forward_results_contain_every_control_id', 'passed': fwd_cov['all_present'], 'detail': fwd_cov})

    rev_results = K.load_json(K.REVERSE_AV1_RESULTS)
    rev_cov = results_contain_every_control_id(c1, rev_results)
    items.append({'item': 'av1_reverse_results_contain_every_control_id', 'passed': rev_cov['all_present'], 'detail': rev_cov})

    fwd_target = target_read_from_contract(K.FORWARD_AV1_CHECK)
    items.append({'item': 'av1_target_read_from_contract_not_hardcoded_forward', 'passed': fwd_target['passed'], 'detail': fwd_target})

    rev_target = target_read_from_contract(K.REVERSE_AV1_CHECK)
    items.append({'item': 'av1_target_read_from_contract_not_hardcoded_reverse', 'passed': rev_target['passed'], 'detail': rev_target})

    gs = gate_matches_skeptic()
    items.append({'item': 'gate_accepted_equals_skeptic_supported_statement',
                  'passed': gs['gate_accepted_equals_skeptic_supported_statement'], 'detail': gs})
    items.append({'item': 'gate_limitations_equals_skeptic_limitations',
                  'passed': gs['gate_limitations_equals_skeptic_limitations'], 'detail': gs})

    result = {
        'id': 'preregistration_audit',
        'role': 'pre-registration audit / test; zero research loops',
        'contracts_loaded': ['research/round32/contracts/av1.json', 'research/round32/contracts/av2.json'],
        'items': items,
        'findings': [],
    }
    if not cr2['equal']:
        result['findings'].append(
            "AV2's preregistration.controls_required.ids (23 ids) differs from AV2's contract.controls "
            "(24 ids): 'c1_window_preview_only' is in controls but not in controls_required.ids. AV1's two "
            "lists are identical. This is a genuine contract-authoring gap for AV2, not a false positive of "
            "this audit; flagged for sub-round 2 freezing (see README planning note 2).")
    result['pass'] = all(it['passed'] for it in items)
    return result


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'preregistration_audit', result)
    print('preregistration_audit: %s' % ('PASS' if result['pass'] else 'FAIL'))
    for it in result['items']:
        print('   [%s] %s' % ('x' if it['passed'] else ' ', it['item']))
    for f in result['findings']:
        print('  FINDING:', f)
    if not result['pass']:
        sys.exit(1)


if __name__ == '__main__':
    main()
