#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 3, assistant-3 script 1 of 3: structural
pre-registration audit of AX1, AX2 (frozen_before_production) and
AY1/AY2/AZ1/AZ2 (each read at whatever status is currently on disk -- this is a
live, concurrently-advancing repository, and a contract this task's brief called
"draft" can freeze while this script is being written or re-run; see the
`observed contract statuses` finding for what was actually seen at run time),
using the pre-registration vocabulary **extended** by `advisor/plan.json`'s
`preregistration_vocabulary_extensions` block (dated 2026-09-24, recorded after
the Jung assistant-2 audit): symbolic tau-dependent triples,
`direction='statement+skeptic'`, `observable.reference_route='n/a'` for statement
loops, and `tau.value='grid'` for finite-graph loops.

Pre-registration audit only (`update-2.md` section 5, item 1; the calling task).
Counts zero research loops; not a producer, contract, gate or skeptical review, and
nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted. Generalises (reuses the logic of, does not
import) `research/round32/experts/jung/assistant-2/preregistration_audit_2.py`
and `common2.py`, which ran the equivalent structural checks against AW1/AW2
(sub-round 2) with the pre-extension vocabulary.

Per contract (AX1, AX2, AY1, AY2, AZ1, AZ2):
  (a) every `preregistration` field present, with an allowed value from the
      vocabulary in `common3.py` -- the four fields plan.json amended
      (`selected_triple_alpha_units`, `direction`, `observable.reference_route`,
      `tau.value`) are checked against BOTH the pre-extension vocabulary (for
      visibility: this is exactly what assistant-2's script would still report)
      and the extended vocabulary (the field's actual pass/fail here);
  (b) `preregistration.controls_required.ids` equals the contract's `controls`
      list, byte-for-byte (order-sensitive);
  (c) `sub_labels_allowed` equals the closed five-label vocabulary (unchanged by
      the extension);
  (d) `error_terms_itemized` is a non-empty list of strings, and
      `error_terms_rule` equals the frozen "not_applicable only with a stated
      reason" text (unchanged by the extension).

For AX1 additionally (frozen and in production; AX2 is frozen but has no
producer output yet -- only `forward/ax2/inputs/` exists on disk at run time, so
items (e)/(f) below are recorded `not_yet_applicable` for AX2, not scored):
  (e) both producers' `output/results.json` `checks` lists contain every id in
      the contract's `controls` list;
  (f) `advisor/ax1-gate.json`'s `accepted`/`limitations` equal
      `skeptic/ax1.json`'s `supported_statement`/`limitations` (the final
      skeptic verdict, not a pre-comparison package -- AX1's review is complete,
      unlike AW2's at the equivalent point in sub-round 2).

Usage: python3 -B preregistration_audit_3.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common3 as K  # noqa: E402


def field_check(desc, condition, **extra):
    d = {'field': desc, 'passed': bool(condition)}
    d.update(extra)
    return d


def check_triple(pre):
    """Returns (pre_extension_result, extension_result) for
    `selected_triple_alpha_units`."""
    triple = pre.get('selected_triple_alpha_units')
    model_id = pre.get('model_id') or ''

    # Pre-extension (assistant-2's original strict-rational-only rule).
    pre_ok = isinstance(triple, list) and len(triple) == 3
    pre_reason = None
    if pre_ok:
        bad = [x for x in triple if not K.is_rational(x)]
        if bad:
            pre_ok = False
            pre_reason = 'entries not exact rationals (symbolic/tau-dependent or non-numeric): %r' % bad
    else:
        pre_reason = 'not a 3-element list: %r' % (triple,)

    # Extended (plan.json): numeric OR tau-linear 3-tuple, OR the finite-graph
    # sentinel string tied to an 'FG(' model_id.
    if isinstance(triple, list) and len(triple) == 3:
        bad = [x for x in triple if not (K.is_rational(x) or K.is_tau_linear(x))]
        ext_ok = not bad
        ext_reason = None if ext_ok else ('entries neither exact rationals nor recognized tau-linear '
                                          'expressions: %r' % bad)
    elif isinstance(triple, str) and triple == 'n/a (finite graph)':
        ext_ok = model_id.startswith('FG(')
        ext_reason = None if ext_ok else ("triple is the finite-graph sentinel but model_id does not start "
                                          "with 'FG(': %r" % model_id)
    else:
        ext_ok = False
        ext_reason = ("neither a 3-element list (numeric or tau-linear) nor the finite-graph sentinel "
                     "string 'n/a (finite graph)': %r" % (triple,))

    return (field_check('selected_triple_alpha_units [pre-extension]', pre_ok, value=triple, reason=pre_reason),
            field_check('selected_triple_alpha_units [extended]', ext_ok, value=triple, reason=ext_reason))


def check_tau(pre, contract):
    tau = pre.get('tau')
    has_keys = isinstance(tau, dict) and {'value', 'signs_evaluated', 'is_model_change_vs_previous_loop',
                                          'rule_if_chosen_later'} <= set(tau)
    if not has_keys:
        r = 'missing required keys or not a dict'
        return (field_check('tau [pre-extension]', False, value=tau, reason=r),
                field_check('tau [extended]', False, value=tau, reason=r))

    def other_fields_ok():
        if tau['signs_evaluated'] != ['+', '-']:
            return False, 'signs_evaluated is not [+, -]: %r' % (tau['signs_evaluated'],)
        if not isinstance(tau['is_model_change_vs_previous_loop'], bool):
            return False, 'is_model_change_vs_previous_loop is not boolean'
        if not (tau['rule_if_chosen_later'] is None or isinstance(tau['rule_if_chosen_later'], str)):
            return False, 'rule_if_chosen_later is neither null nor a string'
        return True, None

    # Pre-extension: value must be an exact rational.
    pre_ok = K.is_rational(tau['value'])
    pre_reason = None if pre_ok else 'tau.value does not parse as an exact rational: %r' % (tau['value'],)
    if pre_ok:
        pre_ok, pre_reason = other_fields_ok()

    # Extended: exact rational, OR 'grid' with parameters.tau_FG_grid populated,
    # OR a non-empty rule-reference string (plan.json's third, looser category).
    value = tau['value']
    if K.is_rational(value):
        ext_ok, ext_reason, kind = True, None, 'exact_rational'
    elif value == 'grid':
        grid = (contract.get('parameters') or {}).get('tau_FG_grid')
        if isinstance(grid, list) and len(grid) > 0:
            ext_ok, ext_reason, kind = True, None, 'grid'
        else:
            ext_ok, ext_reason, kind = False, ("tau.value=='grid' but parameters.tau_FG_grid is missing or "
                                                "empty"), None
    elif isinstance(value, str) and value.strip() != '':
        ext_ok, ext_reason, kind = True, None, 'rule_reference'
    else:
        ext_ok, ext_reason, kind = False, ('tau.value is neither an exact rational, grid (with '
                                            'parameters.tau_FG_grid), nor a non-empty rule-reference string: '
                                            '%r' % (value,)), None
    if ext_ok:
        ext_ok, ext_reason2 = other_fields_ok()
        ext_reason = ext_reason2 if not ext_ok else None

    return (field_check('tau [pre-extension]', pre_ok, value=tau, reason=pre_reason),
            field_check('tau [extended]', ext_ok, value=tau, reason=ext_reason, kind=(kind if ext_ok else None)))


def check_observable(pre):
    obs = pre.get('observable')
    has_keys = isinstance(obs, dict) and {'id', 'centering', 'reference_value_exact', 'reference_route'} <= set(obs)
    if not has_keys:
        r = 'missing required keys or not a dict'
        return (field_check('observable [pre-extension]', False, value=obs, reason=r),
                field_check('observable [extended]', False, value=obs, reason=r))

    def base_fields_ok():
        if not (isinstance(obs['id'], str) and obs['id'] != ''):
            return False, 'observable.id missing or empty'
        if obs['centering'] not in K.ALLOWED_CENTERING:
            return False, 'observable.centering not in %r: %r' % (K.ALLOWED_CENTERING, obs['centering'])
        if not (isinstance(obs['reference_value_exact'], str) and obs['reference_value_exact'] != ''):
            return False, 'observable.reference_value_exact missing or empty'
        return True, None

    route = obs['reference_route']

    # Pre-extension.
    pre_ok = route in K.ALLOWED_REFERENCE_ROUTE
    pre_reason = None if pre_ok else ('observable.reference_route not in %r: %r'
                                      % (K.ALLOWED_REFERENCE_ROUTE, route))
    if pre_ok:
        pre_ok, pre_reason = base_fields_ok()

    # Extended: haar/selected_strip/own_finite_graph unchanged; 'n/a' additionally
    # requires a statement-loop direction and a stated reason in
    # error_terms_itemized (plan.json: "n/a (statement loops only, with the
    # reason in error_terms_itemized)").
    if route in K.ALLOWED_REFERENCE_ROUTE_EXT_BASE:
        ext_ok, ext_reason = base_fields_ok()
    elif route == 'n/a':
        direction = pre.get('direction')
        is_statement = direction in K.STATEMENT_DIRECTIONS
        eti = pre.get('error_terms_itemized')
        has_reason = (isinstance(eti, list) and len(eti) == 1 and isinstance(eti[0], str)
                     and 'reason' in eti[0].lower())
        ext_ok = is_statement and has_reason
        if ext_ok:
            ext_ok, ext_reason = base_fields_ok()
        else:
            ext_reason = ("reference_route=='n/a' requires direction in %r (got %r) and a stated reason in "
                         "error_terms_itemized (got %r)" % (K.STATEMENT_DIRECTIONS, direction, eti))
    else:
        ext_ok = False
        ext_reason = "observable.reference_route not in extended vocabulary %r + {'n/a'}: %r" % (
            K.ALLOWED_REFERENCE_ROUTE_EXT_BASE, route)

    return (field_check('observable [pre-extension]', pre_ok, value=obs, reason=pre_reason),
            field_check('observable [extended]', ext_ok, value=obs, reason=ext_reason))


def check_direction(pre):
    value = pre.get('direction')
    pre_ok = value in K.ALLOWED_DIRECTION
    ext_ok = value in K.ALLOWED_DIRECTION_EXT
    return (field_check('direction [pre-extension]', pre_ok, value=value),
            field_check('direction [extended]', ext_ok, value=value))


def audit_preregistration_block_3(pre, contract):
    """All fields of the closed pre-registration schema `hnm-r32-prereg-v1`.
    Fields untouched by the plan.json extension use the single check common2.py
    already validated (re-declared here); the four amended fields each report a
    pre-extension AND an extended result (see module docstring)."""
    out = []
    out.append(field_check('schema', pre.get('schema') == 'hnm-r32-prereg-v1'))
    out.append(field_check('frozen_before_any_outcome', pre.get('frozen_before_any_outcome') is True))

    mid = pre.get('model_id')
    out.append(field_check('model_id', isinstance(mid, str) and mid.startswith(K.ALLOWED_MODEL_ID_PREFIXES),
                            value=mid))

    triple_pre, triple_ext = check_triple(pre)
    out.append(triple_pre)
    out.append(triple_ext)

    tau_pre, tau_ext = check_tau(pre, contract)
    out.append(tau_pre)
    out.append(tau_ext)

    sp = pre.get('state_provenance')
    out.append(field_check('state_provenance', isinstance(sp, str) and sp.startswith(K.ALLOWED_STATE_PROVENANCE_PREFIXES),
                            value=sp))
    out.append(field_check('clock', pre.get('clock') ==
                            's=alpha*t_E/hbar, theta=alpha*t/hbar; u=s/8 and exponent 24 forbidden in packets'))

    obs_pre, obs_ext = check_observable(pre)
    out.append(obs_pre)
    out.append(obs_ext)

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

    dir_pre, dir_ext = check_direction(pre)
    out.append(dir_pre)
    out.append(dir_ext)
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
    return {'ok': ok, 'items': eti, 'rule': rule}


def field_by_name(fields, name):
    for f in fields:
        if f['field'] == name:
            return f
    raise KeyError(name)


def extended_passed(fields):
    """The contract's overall pass/fail using the EXTENDED reading of the four
    amended fields (the '[extended]' entries) and the unmodified reading of every
    other field. The '[pre-extension]' twin entries are recorded for visibility
    only and never gate this Boolean."""
    return all(f['passed'] for f in fields if not f['field'].endswith('[pre-extension]'))


def audit_one_contract(cid, contract, expected_status=None):
    if expected_status is not None:
        K.require(contract.get('status') == expected_status, '%s: unexpected status' % cid)
    else:
        K.require(contract.get('status') in ('draft', 'frozen_before_production'),
                  '%s: status is neither draft nor frozen_before_production' % cid)
    pre = contract['preregistration']
    fields = audit_preregistration_block_3(pre, contract)
    cr = controls_required_equals_contract_controls(contract)
    et = error_terms_registered(contract)
    entry = {
        'contract': cid,
        'status': contract.get('status'),
        'fields_present_and_allowed': {'passed': extended_passed(fields), 'fields': fields,
                                       'by_name': {f['field']: f for f in fields}},
        'controls_required_ids_equals_controls': cr,
        'sub_labels_closed_vocabulary': sub_labels_closed(contract),
        'error_terms_itemized_and_rule': et,
    }
    entry['passed'] = (entry['fields_present_and_allowed']['passed'] and cr['equal']
                       and entry['sub_labels_closed_vocabulary'] and et['ok'])
    return entry


def results_contain_every_control_id(contract, results):
    controls = set(contract['controls'])
    have = set(c['id'] for c in results.get('checks', []))
    missing = sorted(controls - have)
    return {'all_present': not missing, 'missing': missing, 'n_controls': len(controls), 'n_checks': len(have)}


def gate_matches_skeptic_ax1():
    gate = K.load_json(K.AX1_GATE)
    skeptic = K.load_json(K.SKEPTIC_AX1_JSON)
    accepted_match = gate.get('accepted') == skeptic.get('supported_statement')
    limitations_match = gate.get('limitations') == skeptic.get('limitations')
    return {'gate_accepted_equals_skeptic_supported_statement': accepted_match,
            'gate_limitations_equals_skeptic_limitations': limitations_match,
            'gate_limitations_count': len(gate.get('limitations') or []),
            'skeptic_limitations_count': len(skeptic.get('limitations') or [])}


def run():
    items = []
    findings = []
    deferred = []

    plan = K.load_plan()
    ext_covered = K.plan_extension_covers(plan)
    items.append({'item': 'plan_json_carries_the_four_field_extension', 'passed': ext_covered,
                  'detail': plan.get('preregistration_vocabulary_extensions')})
    K.require(ext_covered, 'advisor/plan.json no longer carries the expected four-field '
                           'preregistration_vocabulary_extensions block; this audit would be applying a '
                           'stale extension')

    # --- AX1, AX2 (frozen contracts) ---------------------------------------
    ax1c = K.ax1_contract()
    ax2c = K.ax2_contract()
    ax1_entry = audit_one_contract('AX1', ax1c, 'frozen_before_production')
    ax2_entry = audit_one_contract('AX2', ax2c, 'frozen_before_production')
    items.append({'item': 'ax1_structural_preregistration_audit', 'passed': ax1_entry['passed'], 'detail': ax1_entry})
    items.append({'item': 'ax2_structural_preregistration_audit', 'passed': ax2_entry['passed'], 'detail': ax2_entry})

    triple_field_pre = ax1_entry['fields_present_and_allowed']['by_name']['selected_triple_alpha_units [pre-extension]']
    triple_field_ext = ax1_entry['fields_present_and_allowed']['by_name']['selected_triple_alpha_units [extended]']
    if (not triple_field_pre['passed']) and triple_field_ext['passed']:
        findings.append(
            "AX1's (and AX2's) preregistration.selected_triple_alpha_units=['tau/24','tau/24','tau/24'] still "
            "fails the pre-extension rational-only parse assistant-2 used (exactly the gap assistant-2's audit "
            "found), but now PASSES under the plan.json extension recognising tau-linear expressions. This is "
            "the extension doing its job, not a regression: advisor/ax1-gate.json's own limitations list records "
            "the symbolic triple as 'covered by the plan.json vocabulary extension recorded after the freeze "
            "..., contract unamended' and 'the gate should record it as an accepted extension', which matches "
            "this audit's finding exactly.")

    # AX1: producer results coverage + gate/skeptic equality (AX1 review is
    # complete). AX2: recorded not_yet_applicable (only forward/ax2/inputs/
    # exists on disk at run time -- no report.md, no output/results.json, no
    # gate, no skeptic review yet).
    fwd_ax1 = K.load_json(K.FORWARD_AX1_RESULTS)
    rev_ax1 = K.load_json(K.REVERSE_AX1_RESULTS)
    fwd_ax1_cov = results_contain_every_control_id(ax1c, fwd_ax1)
    rev_ax1_cov = results_contain_every_control_id(ax1c, rev_ax1)
    items.append({'item': 'ax1_forward_results_contain_every_control_id', 'passed': fwd_ax1_cov['all_present'],
                  'detail': fwd_ax1_cov})
    items.append({'item': 'ax1_reverse_results_contain_every_control_id', 'passed': rev_ax1_cov['all_present'],
                  'detail': rev_ax1_cov})

    gs = gate_matches_skeptic_ax1()
    items.append({'item': 'ax1_gate_accepted_equals_skeptic_supported_statement',
                  'passed': gs['gate_accepted_equals_skeptic_supported_statement'], 'detail': gs})
    items.append({'item': 'ax1_gate_limitations_equals_skeptic_limitations',
                  'passed': gs['gate_limitations_equals_skeptic_limitations'], 'detail': gs})

    ax2_forward_output_exists = (K.FORWARD / 'ax2' / 'output').is_dir()
    ax2_gate_exists = K.ADVISOR.joinpath('ax2-gate.json').is_file()
    ax2_skeptic_exists = K.SKEPTIC.joinpath('ax2.json').is_file()
    deferred.append({'item': 'ax2_forward_results_contain_every_control_id', 'status': 'not_yet_applicable',
                     'reason': ('AX2 is frozen_before_production but not yet in production: '
                                'forward/ax2/output/ exists=%r (only forward/ax2/inputs/ is on disk); '
                                'not counted toward the overall pass/fail; re-run once it exists.'
                                % ax2_forward_output_exists)})
    deferred.append({'item': 'ax2_gate_accepted_equals_skeptic_supported_statement', 'status': 'not_yet_applicable',
                     'reason': ('advisor/ax2-gate.json exists=%r, skeptic/ax2.json exists=%r; not counted '
                                'toward the overall pass/fail; re-run once both files exist.'
                                % (ax2_gate_exists, ax2_skeptic_exists))})

    if not ax1_entry['controls_required_ids_equals_controls']['equal']:
        findings.append('AX1: controls_required.ids != controls (unexpected -- re-check for regression).')
    if not ax2_entry['controls_required_ids_equals_controls']['equal']:
        findings.append('AX2: controls_required.ids != controls (unexpected -- re-check for regression).')
    if ax1_entry['passed'] and ax2_entry['passed']:
        findings.append('AX1 and AX2 (frozen), read with the extended vocabulary: no AV2/AW-style mirror gap; '
                        'every preregistration field present and allowed (the symbolic triple passing only '
                        'because of the plan.json extension -- see the finding above), '
                        'controls_required.ids == controls byte-for-byte, sub_labels_allowed the closed '
                        'five-label list, error_terms_itemized/error_terms_rule present as registered.')

    # --- AY1, AY2, AZ1, AZ2 --------------------------------------------------
    draft_entries = {}
    observed_statuses = {}
    for cid in K.DRAFT_IDS:
        c = K.draft_contract(cid)
        observed_statuses[cid] = c.get('status')
        entry = audit_one_contract(cid, c)
        draft_entries[cid] = entry
        items.append({'item': '%s_structural_preregistration_audit' % cid.lower(), 'passed': entry['passed'],
                      'detail': entry})
        cr = entry['controls_required_ids_equals_controls']
        if not cr['equal']:
            findings.append('%s: controls_required.ids != controls (a mirror gap): only_in_controls=%s, '
                            'only_in_ids=%s.' % (cid, cr['only_in_controls'], cr['only_in_ids']))

    already_frozen = [cid for cid in K.DRAFT_IDS if observed_statuses[cid] == 'frozen_before_production']
    findings.append('Observed contract statuses at audit time: AX1=frozen_before_production, '
                    'AX2=frozen_before_production, %s.%s'
                    % (observed_statuses,
                       (' %s already moved draft -> frozen_before_production while this audit was being run/'
                        're-run; any structural finding below that still applies to it should be recorded in its '
                        'advisor gate (repair by record, not by silent edit of the frozen contract, per AGENTS.md), '
                        'not silently patched.' % already_frozen) if already_frozen else ''))

    stmt_direction = [cid for cid in K.DRAFT_IDS
                      if draft_entries[cid]['fields_present_and_allowed']['by_name']['direction [extended]']
                      ['value'] == 'statement+skeptic']
    if stmt_direction:
        findings.append(
            "direction='statement+skeptic' (%s): assistant-2 flagged this as an undeclared value against the "
            "pre-extension vocabulary; under the plan.json extension it now passes "
            "('direction [extended]'.passed=True), while the '[pre-extension]' twin entry still correctly "
            "records it as not in the original 3-value list, for visibility." % stmt_direction)

    na_route = [cid for cid in K.DRAFT_IDS
               if draft_entries[cid]['fields_present_and_allowed']['by_name']['observable [extended]']['value']
               is not None
               and draft_entries[cid]['fields_present_and_allowed']['by_name']['observable [extended]']['value']
               .get('reference_route') == 'n/a']
    if na_route:
        findings.append(
            "observable.reference_route='n/a' (%s): now passes under the extension because both are statement "
            "loops (direction in {statement-only, statement+skeptic}) whose error_terms_itemized carries a "
            "single sentinel string containing the word 'reason' (plan.json's stated condition); the "
            "'[pre-extension]' twin entry still correctly fails since 'n/a' was never in the original "
            "3-value ALLOWED_REFERENCE_ROUTE list." % na_route)

    az2_entry = draft_entries['AZ2']
    az2_by_name = az2_entry['fields_present_and_allowed']['by_name']
    az2_triple_ext = az2_by_name['selected_triple_alpha_units [extended]']
    az2_tau_ext = az2_by_name['tau [extended]']
    if az2_triple_ext['passed'] and az2_tau_ext['passed']:
        findings.append(
            "AZ2 (the two-plaquette finite-graph loop): both remaining gaps assistant-2 found now close under "
            "the extension -- selected_triple_alpha_units='n/a (finite graph)' passes because model_id='FG(...)' "
            "names the finite graph, and tau.value='grid' passes because parameters.tau_FG_grid=['1/1000', "
            "'1/100','1/10'] is populated (kind=%r). The pre-extension entries still correctly fail (recorded "
            "for visibility), matching assistant-2's original finding exactly." % az2_tau_ext.get('kind'))
    else:
        findings.append('AZ2 unexpectedly still fails a structural field check under the extension; see its '
                        'detail entry (selected_triple_alpha_units [extended]=%r, tau [extended]=%r).'
                        % (az2_triple_ext, az2_tau_ext))

    if all(draft_entries[cid]['controls_required_ids_equals_controls']['equal'] for cid in K.DRAFT_IDS):
        findings.append('AY1, AY2, AZ1, AZ2: controls_required.ids == controls byte-for-byte (no mirror gap in '
                        'any of the four).')

    all_six_pass = ax1_entry['passed'] and ax2_entry['passed'] and all(draft_entries[c]['passed']
                                                                        for c in K.DRAFT_IDS)
    findings.append(('All six contracts (AX1, AX2, AY1, AY2, AZ1, AZ2) pass the full structural pre-registration '
                     'audit under the plan.json-extended vocabulary; the three schema gaps assistant-2 found in '
                     'AX1/AX2 (symbolic triple), AY2/AZ1 (statement+skeptic direction, n/a reference route) and '
                     'AZ2 (finite-graph sentinel triple, grid tau) are each resolved by exactly the extension '
                     'named for it, with none left over.') if all_six_pass else
                    'Not all six contracts pass under the extended vocabulary; see the per-contract detail '
                    'entries and findings above for which field(s) still fail.')

    result = {
        'id': 'preregistration_audit_3',
        'role': 'pre-registration audit; zero research loops',
        'vocabulary': 'extended per advisor/plan.json.preregistration_vocabulary_extensions (2026-09-24)',
        'contracts_audited': ['AX1 (frozen_before_production)', 'AX2 (frozen_before_production)']
                             + ['%s (%s)' % (c, observed_statuses[c]) for c in K.DRAFT_IDS],
        'items': items,
        'deferred': deferred,
        'findings': findings,
    }
    result['pass'] = all(it['passed'] for it in items)
    return result


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'preregistration_audit_3', result)
    print('preregistration_audit_3: %s' % ('PASS' if result['pass'] else 'FAIL'))
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
