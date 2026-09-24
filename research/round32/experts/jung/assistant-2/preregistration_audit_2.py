#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 2, assistant-2 script 3 of 3: structural
pre-registration audit of AW1, AW2 (frozen) and AX1/AX2/AY1/AY2/AZ1/AZ2 (drafts).

Pre-registration audit only (`update-1.md` section 5, item 3; the calling task).
Counts zero research loops; not a producer, contract, gate or skeptical review, and
nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted. Generalises (reuses the logic of, does not
import) `research/round32/experts/jung/assistant-1/preregistration_audit.py`,
which ran the same checks against AV1/AV2 in sub-round 1.

Per contract:
  (a) every `preregistration` field present, with an allowed value from the
      closed vocabularies re-declared in `common2.py`;
  (b) `preregistration.controls_required.ids` equals the contract's `controls`
      list, byte-for-byte (order-sensitive);
  (c) `sub_labels_allowed` equals the closed five-label vocabulary;
  (d) `error_terms_itemized` is a non-empty list of strings, and
      `error_terms_rule` equals the frozen "not_applicable only with a stated
      reason" text.

For AW1 and AW2 additionally:
  (e) every producer's `output/results.json` `checks` list contains every id in
      the contract's `controls` list;
  (f) the AW1 gate's `accepted`/`limitations` equal `skeptic/aw1.json`'s
      `supported_statement`/`limitations`. AW2 has no gate or final skeptic
      verdict yet (`advisor/aw2-gate.json` and `skeptic/aw2.json` do not exist;
      only `skeptic/aw2-independent-freeze.json`, the pre-comparison package, is
      on disk) -- this sub-item is recorded as `not_yet_applicable`, not scored
      pass or fail, and is not counted in the overall `pass` boolean.

Every field-level and item-level result is reported so drift is visible even where
it does not change the aggregate PASS/FAIL, mirroring assistant-1's non-blocking
AV2 finding: a structural gap caught before production is the point of this audit.

Usage: python3 -B preregistration_audit_2.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common2 as K  # noqa: E402


def field_check(desc, condition, **extra):
    d = {'field': desc, 'passed': bool(condition)}
    d.update(extra)
    return d


def audit_preregistration_block(pre):
    """Every field of the closed pre-registration schema `hnm-r32-prereg-v1`,
    present in `pre` with an allowed value. Returns a list of per-field results
    (same checks as assistant-1's `audit_preregistration_block`, generalised
    beyond AV1/AV2)."""
    out = []
    out.append(field_check('schema', pre.get('schema') == 'hnm-r32-prereg-v1'))
    out.append(field_check('frozen_before_any_outcome', pre.get('frozen_before_any_outcome') is True))

    mid = pre.get('model_id')
    out.append(field_check('model_id', isinstance(mid, str) and mid.startswith(K.ALLOWED_MODEL_ID_PREFIXES),
                            value=mid))

    triple = pre.get('selected_triple_alpha_units')
    triple_ok = isinstance(triple, list) and len(triple) == 3
    triple_reason = None
    if triple_ok:
        bad = [x for x in triple if not K.is_rational(x)]
        if bad:
            triple_ok = False
            triple_reason = 'entries not exact rationals (symbolic/tau-dependent): %r' % bad
    else:
        triple_reason = 'not a 3-element list: %r' % (triple,)
    out.append(field_check('selected_triple_alpha_units', triple_ok, value=triple, reason=triple_reason))

    tau = pre.get('tau')
    tau_ok = isinstance(tau, dict) and {'value', 'signs_evaluated', 'is_model_change_vs_previous_loop',
                                         'rule_if_chosen_later'} <= set(tau)
    tau_reason = None
    if tau_ok:
        if not K.is_rational(tau['value']):
            tau_ok = False
            tau_reason = 'tau.value does not parse as an exact rational: %r' % (tau['value'],)
        elif tau['signs_evaluated'] != ['+', '-']:
            tau_ok = False
            tau_reason = 'signs_evaluated is not [+, -]: %r' % (tau['signs_evaluated'],)
        elif not isinstance(tau['is_model_change_vs_previous_loop'], bool):
            tau_ok = False
            tau_reason = 'is_model_change_vs_previous_loop is not boolean'
        elif not (tau['rule_if_chosen_later'] is None or isinstance(tau['rule_if_chosen_later'], str)):
            tau_ok = False
            tau_reason = 'rule_if_chosen_later is neither null nor a string'
    else:
        tau_reason = 'missing required keys or not a dict'
    out.append(field_check('tau', tau_ok, value=tau, reason=tau_reason))

    sp = pre.get('state_provenance')
    out.append(field_check('state_provenance', isinstance(sp, str) and sp.startswith(K.ALLOWED_STATE_PROVENANCE_PREFIXES),
                            value=sp))
    out.append(field_check('clock', pre.get('clock') ==
                            's=alpha*t_E/hbar, theta=alpha*t/hbar; u=s/8 and exponent 24 forbidden in packets'))

    obs = pre.get('observable')
    obs_ok = isinstance(obs, dict) and {'id', 'centering', 'reference_value_exact', 'reference_route'} <= set(obs)
    obs_reason = None
    if obs_ok:
        if not (isinstance(obs['id'], str) and obs['id'] != ''):
            obs_ok, obs_reason = False, 'observable.id missing or empty'
        elif obs['centering'] not in K.ALLOWED_CENTERING:
            obs_ok, obs_reason = False, 'observable.centering not in %r: %r' % (K.ALLOWED_CENTERING, obs['centering'])
        elif not (isinstance(obs['reference_value_exact'], str) and obs['reference_value_exact'] != ''):
            obs_ok, obs_reason = False, 'observable.reference_value_exact missing or empty'
        elif obs['reference_route'] not in K.ALLOWED_REFERENCE_ROUTE:
            obs_ok, obs_reason = False, ('observable.reference_route not in %r: %r'
                                         % (K.ALLOWED_REFERENCE_ROUTE, obs['reference_route']))
    else:
        obs_reason = 'missing required keys or not a dict'
    out.append(field_check('observable', obs_ok, value=obs, reason=obs_reason))

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
                            and all(isinstance(x, str) for x in eti), value=eti))
    out.append(field_check('error_terms_rule', pre.get('error_terms_rule') == K.ERROR_TERMS_RULE_TEXT))

    target = pre.get('target')
    target_ok = isinstance(target, dict) and {'quantity', 'value', 'comparator'} <= set(target)
    target_reason = None
    if target_ok:
        if not K.is_rational(target['value']):
            target_ok, target_reason = False, 'target.value not an exact rational: %r' % (target['value'],)
        elif not (isinstance(target['quantity'], str) and target['quantity'] != ''):
            target_ok, target_reason = False, 'target.quantity missing or empty'
        elif target['comparator'] not in K.ALLOWED_COMPARATOR:
            target_ok, target_reason = False, 'target.comparator not in %r' % (K.ALLOWED_COMPARATOR,)
    else:
        target_reason = 'missing required keys or not a dict'
    out.append(field_check('target', target_ok, value=target, reason=target_reason))

    out.append(field_check('expected_outcome_types', pre.get('expected_outcome_types') == K.EXPECTED_OUTCOME_TYPES,
                            value=pre.get('expected_outcome_types')))
    out.append(field_check('sub_labels_allowed', pre.get('sub_labels_allowed') == K.SUB_LABELS_ALLOWED,
                            value=pre.get('sub_labels_allowed')))

    cr = pre.get('controls_required')
    out.append(field_check('controls_required', isinstance(cr, dict) and isinstance(cr.get('ids'), list)
                            and len(cr['ids']) > 0 and all(isinstance(x, str) for x in cr['ids'])))

    ce = pre.get('claim_exclusions')
    out.append(field_check('claim_exclusions', isinstance(ce, list) and K.TEMPLATE_CLAIM_EXCLUSIONS <= set(ce)))

    hb = pre.get('hash_binding')
    out.append(field_check('hash_binding', isinstance(hb, dict) and set(hb) == set(K.HASH_BINDING_FIELDS)
                            and all(hb[k] is True for k in K.HASH_BINDING_FIELDS)))

    out.append(field_check('direction', pre.get('direction') in K.ALLOWED_DIRECTION, value=pre.get('direction')))
    return out


def controls_required_equals_contract_controls(contract):
    pre = contract['preregistration']
    ids = pre.get('controls_required', {}).get('ids')
    controls = contract.get('controls')
    return {'equal': ids == controls, 'ids_len': len(ids) if ids is not None else None,
            'controls_len': len(controls) if controls is not None else None,
            'only_in_ids': sorted(set(ids or []) - set(controls or [])),
            'only_in_controls': sorted(set(controls or []) - set(ids or []))}


def sub_labels_closed(contract):
    pre = contract['preregistration']
    return pre.get('sub_labels_allowed') == K.SUB_LABELS_ALLOWED


def error_terms_registered(contract):
    pre = contract['preregistration']
    eti = pre.get('error_terms_itemized')
    rule = pre.get('error_terms_rule')
    ok = (isinstance(eti, list) and len(eti) > 0 and all(isinstance(x, str) for x in eti)
          and rule == K.ERROR_TERMS_RULE_TEXT)
    is_statement_sentinel = (len(eti) == 1 and isinstance(eti[0], str) and eti[0].startswith('not_applicable:')
                             if isinstance(eti, list) and eti else False)
    return {'ok': ok, 'items': eti, 'rule': rule, 'is_single_not_applicable_sentinel': is_statement_sentinel}


def results_contain_every_control_id(contract, results):
    controls = set(contract['controls'])
    have = set(c['id'] for c in results.get('checks', []))
    missing = sorted(controls - have)
    return {'all_present': not missing, 'missing': missing, 'n_controls': len(controls), 'n_checks': len(have)}


def gate_matches_skeptic():
    gate = K.load_json(K.AW1_GATE)
    skeptic = K.load_json(K.SKEPTIC_AW1_JSON)
    accepted_match = gate.get('accepted') == skeptic.get('supported_statement')
    limitations_match = gate.get('limitations') == skeptic.get('limitations')
    return {'gate_accepted_equals_skeptic_supported_statement': accepted_match,
            'gate_limitations_equals_skeptic_limitations': limitations_match}


def field_by_name(fields, name):
    for f in fields:
        if f['field'] == name:
            return f
    raise KeyError(name)


def audit_one_contract(cid, contract, expected_status):
    K.require(contract.get('status') == expected_status, '%s: unexpected status' % cid)
    pre = contract['preregistration']
    fields = audit_preregistration_block(pre)
    cr = controls_required_equals_contract_controls(contract)
    et = error_terms_registered(contract)
    entry = {
        'contract': cid,
        'status': contract.get('status'),
        'fields_present_and_allowed': {'passed': all(f['passed'] for f in fields), 'fields': fields,
                                       'by_name': {f['field']: f for f in fields}},
        'controls_required_ids_equals_controls': cr,
        'sub_labels_closed_vocabulary': sub_labels_closed(contract),
        'error_terms_itemized_and_rule': et,
    }
    entry['passed'] = (entry['fields_present_and_allowed']['passed'] and cr['equal']
                       and entry['sub_labels_closed_vocabulary'] and et['ok'])
    return entry


def run():
    items = []
    findings = []
    deferred = []

    # --- AW1, AW2 (frozen) -------------------------------------------------
    aw1c = K.aw1_contract()
    aw2c = K.aw2_contract()
    aw1_entry = audit_one_contract('AW1', aw1c, 'frozen_before_production')
    aw2_entry = audit_one_contract('AW2', aw2c, 'frozen_before_production')
    items.append({'item': 'aw1_structural_preregistration_audit', 'passed': aw1_entry['passed'], 'detail': aw1_entry})
    items.append({'item': 'aw2_structural_preregistration_audit', 'passed': aw2_entry['passed'], 'detail': aw2_entry})

    fwd_aw1 = K.load_json(K.FORWARD_AW1_RESULTS)
    rev_aw1 = K.load_json(K.REVERSE_AW1_RESULTS)
    fwd_aw1_cov = results_contain_every_control_id(aw1c, fwd_aw1)
    rev_aw1_cov = results_contain_every_control_id(aw1c, rev_aw1)
    items.append({'item': 'aw1_forward_results_contain_every_control_id', 'passed': fwd_aw1_cov['all_present'],
                  'detail': fwd_aw1_cov})
    items.append({'item': 'aw1_reverse_results_contain_every_control_id', 'passed': rev_aw1_cov['all_present'],
                  'detail': rev_aw1_cov})

    fwd_aw2 = K.load_json(K.FORWARD_AW2_RESULTS)
    fwd_aw2_cov = results_contain_every_control_id(aw2c, fwd_aw2)
    items.append({'item': 'aw2_forward_results_contain_every_control_id', 'passed': fwd_aw2_cov['all_present'],
                  'detail': fwd_aw2_cov})

    gs = gate_matches_skeptic()
    items.append({'item': 'aw1_gate_accepted_equals_skeptic_supported_statement',
                  'passed': gs['gate_accepted_equals_skeptic_supported_statement'], 'detail': gs})
    items.append({'item': 'aw1_gate_limitations_equals_skeptic_limitations',
                  'passed': gs['gate_limitations_equals_skeptic_limitations'], 'detail': gs})

    aw2_gate_exists = K.ADVISOR.joinpath('aw2-gate.json').is_file()
    aw2_skeptic_final_exists = K.SKEPTIC.joinpath('aw2.json').is_file()
    deferred.append({'item': 'aw2_gate_accepted_equals_skeptic_supported_statement',
                     'status': 'not_yet_applicable',
                     'reason': ("AW2 review is pending (provisional, per the calling task): "
                                "advisor/aw2-gate.json exists=%r, skeptic/aw2.json exists=%r; only "
                                "skeptic/aw2-independent-freeze.json (the pre-comparison package) is on disk. "
                                "Not counted toward the overall pass/fail; re-run this item once both files "
                                "exist." % (aw2_gate_exists, aw2_skeptic_final_exists))})

    if not aw1_entry['controls_required_ids_equals_controls']['equal']:
        findings.append('AW1: controls_required.ids != controls (unexpected; update-1.md reported these as equal '
                        '28/28 -- re-check for regression).')
    if not aw2_entry['controls_required_ids_equals_controls']['equal']:
        findings.append('AW2: controls_required.ids != controls (unexpected; update-1.md reported these as equal '
                        '22/22 -- re-check for regression).')
    if aw1_entry['passed'] and aw2_entry['passed']:
        findings.append('AW1 and AW2 (frozen): no AV2-style mirror gap; every preregistration field present and '
                        'allowed, controls_required.ids == controls byte-for-byte, sub_labels_allowed the closed '
                        'five-label list, error_terms_itemized/error_terms_rule present as registered.')

    # --- AX1, AX2, AY1, AY2, AZ1, AZ2 (draft) -------------------------------
    draft_entries = {}
    for cid in K.DRAFT_IDS:
        c = K.draft_contract(cid)
        entry = audit_one_contract(cid, c, 'draft')
        draft_entries[cid] = entry
        items.append({'item': '%s_structural_preregistration_audit' % cid.lower(), 'passed': entry['passed'],
                      'detail': entry})
        cr = entry['controls_required_ids_equals_controls']
        if not cr['equal']:
            findings.append('%s: controls_required.ids != controls (an AV2-style mirror gap): only_in_controls=%s, '
                            'only_in_ids=%s.' % (cid, cr['only_in_controls'], cr['only_in_ids']))

    # Cross-cutting findings across the six drafts (the reason for running this
    # audit before AX1..AZ2 leave `status: draft`): three distinct schema/
    # vocabulary gaps, each affecting a genuinely new model shape introduced in
    # sub-rounds 3-5 that the sub-round-1 template (as validated by assistant-1
    # against AV1/AV2, and consistent with `recommendation.json`'s own use of
    # "statement-only") did not anticipate.
    symbolic_triple = [cid for cid in ('AX1', 'AX2')
                       if not draft_entries[cid]['fields_present_and_allowed']['by_name']
                       ['selected_triple_alpha_units']['passed']]
    if symbolic_triple:
        findings.append(
            "Symbolic (tau-proportional) selected triple: %s's preregistration.selected_triple_alpha_units is "
            "['tau/24','tau/24','tau/24'] -- each entry is a formula in tau, not an exact-rational constant like "
            "AV1/AW1's ['0','0','0']. This fails the closed schema's strict rational-only parse (`common2.rat`), "
            "which was designed for a fixed numeric triple. It is a legitimate model need (route B's uniform "
            "coefficient nu=alpha*tau/24 scales with tau by construction, per ax1.json's own model text), not an "
            "authoring error, but the schema has not been extended to accept a formula-valued triple. Flag for "
            "sign-off before AX1/AX2 leave draft: either register an explicit 'formula-valued triple' variant of "
            "the schema (naming which formulas are allowed) or record the triple as informational text elsewhere "
            "and keep selected_triple_alpha_units numeric (e.g. by fixing tau first and reporting the resulting "
            "numeric triple at the cap)." % symbolic_triple)

    stmt_direction = [cid for cid in ('AY2', 'AZ1')
                      if draft_entries[cid]['fields_present_and_allowed']['by_name']['direction']['value']
                      == 'statement+skeptic']
    if stmt_direction:
        findings.append(
            "Undeclared direction value 'statement+skeptic': %s use direction='statement+skeptic' (both at the "
            "contract's top level and inside preregistration), but the closed ALLOWED_DIRECTION vocabulary this "
            "audit inherits from assistant-1's sub-round-1 script (itself matching the lens's own loop1 "
            "`recommendation.json`, whose R32-J5-DICTIONARY goal pair used direction='statement-only') contains "
            "'statement-only', not 'statement+skeptic'. Both drafts are internally consistent (top-level and "
            "preregistration agree with each other), so this looks like a deliberate, consistent new convention "
            "for the newly-introduced 'statement loop' investigation type -- named consistently with "
            "'single+skeptic' -- rather than a typo. This task's reading list does not include loop2-response.md "
            "/ loop3-signoff.md section 2 verbatim, so whether this is a signed-off vocabulary amendment cannot "
            "be confirmed here. Flag for sign-off before AY2/AZ1 leave draft: either amend the closed direction "
            "vocabulary explicitly (the same way a sixth sub-label would need a Jung-lens sign-off note, per "
            "assistant-1's README planning note 2) to admit 'statement+skeptic', or rename these two contracts' "
            "direction back to 'statement-only'." % stmt_direction)

    na_reference_route = [cid for cid in ('AY2', 'AZ1')
                          if draft_entries[cid]['fields_present_and_allowed']['by_name']['observable']['value']
                          is not None
                          and draft_entries[cid]['fields_present_and_allowed']['by_name']['observable']['value']
                          .get('reference_route') == 'n/a']
    if na_reference_route:
        findings.append(
            "Same two statement loops (%s) also set observable.reference_route='n/a', which is not in the closed "
            "ALLOWED_REFERENCE_ROUTE vocabulary {haar, selected_strip, own_finite_graph}. This is the same root "
            "cause as the direction finding above: a 'statement loop' with no numerical certificate has no "
            "reference to route, and the template's observable schema was not given an explicit accommodation "
            "for that case (contrast AZ2, a genuine finite-graph loop, which correctly uses the pre-anticipated "
            "'own_finite_graph' value rather than 'n/a'). Bundle the fix with the direction finding above." % na_reference_route)

    az2_entry = draft_entries['AZ2']
    az2_by_name = az2_entry['fields_present_and_allowed']['by_name']
    az2_triple_field = az2_by_name['selected_triple_alpha_units']
    az2_tau_field = az2_by_name['tau']
    if not az2_triple_field['passed'] or not az2_tau_field['passed']:
        findings.append(
            "AZ2 (the two-plaquette finite-graph loop) fails two schema fields that its own model_id already "
            "anticipated needing a finite-graph variant for: preregistration.selected_triple_alpha_units='n/a "
            "(finite graph)' is a string, not the required 3-element numeric list (reason: %s), and "
            "preregistration.tau.value='grid' does not parse as an exact rational (reason: %s) because AZ2 "
            "evaluates a declared grid (parameters.tau_FG_grid=['1/1000','1/100','1/10']), not one fixed coupling. "
            "Note the asymmetry: ALLOWED_MODEL_ID_PREFIXES already includes 'FG(' and ALLOWED_REFERENCE_ROUTE "
            "already includes 'own_finite_graph' -- both correctly used by AZ2 -- so the schema partially "
            "anticipated a finite-graph loop, but selected_triple_alpha_units and tau.value were not given a "
            "parallel finite-graph/grid accommodation. Also note AZ2's state_provenance is still the "
            "'AQ1_centered_whole_star_subsequence...' boilerplate text (it passes only because that prefix is "
            "one of three the schema permits, not because a 'finite_graph_ground...' provenance, the prefix the "
            "schema separately anticipates for this case, was actually used); this is a content mismatch worth "
            "correcting even though it does not fail the structural check. Flag for sign-off before AZ2 leaves "
            "draft: register an explicit grid-tau / non-triple schema variant for finite-graph loops (AZ2 is not "
            "the first FG( loop the schema expected, so this variant should probably have existed already)."
            % (az2_triple_field.get('reason'), az2_tau_field.get('reason')))

    if all(draft_entries[cid]['controls_required_ids_equals_controls']['equal'] for cid in K.DRAFT_IDS):
        findings.append('All six drafts (AX1,AX2,AY1,AY2,AZ1,AZ2): controls_required.ids == controls byte-for-byte '
                        '(no AV2-style mirror gap in any draft).')

    ay1_only_clean = draft_entries['AY1']['passed']
    findings.append('Of the six drafts, only AY1 passes every structural field check unmodified; AX1, AX2, AY2, '
                    'AZ1 and AZ2 each hit exactly one of the three schema-vocabulary gaps above (AY1 is the only '
                    'draft that reuses the AV1/AW1 model shape (AQ_patterned_zero_selected, numeric zero triple, '
                    'haar reference, statement-standard direction) without any new field shape).'
                    if ay1_only_clean else
                    'AY1 unexpectedly also fails a structural field check; see its detail entry.')

    result = {
        'id': 'preregistration_audit_2',
        'role': 'pre-registration audit; zero research loops',
        'contracts_audited': ['AW1 (frozen)', 'AW2 (frozen)'] + ['%s (draft)' % c for c in K.DRAFT_IDS],
        'items': items,
        'deferred': deferred,
        'findings': findings,
    }
    result['pass'] = all(it['passed'] for it in items)
    return result


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'preregistration_audit_2', result)
    print('preregistration_audit_2: %s' % ('PASS' if result['pass'] else 'FAIL'))
    for it in result['items']:
        print('   [%s] %s' % ('x' if it['passed'] else ' ', it['item']))
    for d in result['deferred']:
        print('   [.] %s: %s' % (d['item'], d['status']))
    print()
    for f in result['findings']:
        print('  FINDING:', f)
    if not result['pass']:
        sys.exit(1)


if __name__ == '__main__':
    main()
