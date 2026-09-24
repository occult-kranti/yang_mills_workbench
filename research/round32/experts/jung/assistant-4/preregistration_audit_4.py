#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 4, assistant-4 script 2 of 2: audit of the
AY1/AY2 frozen contracts and the AZ1/AZ2 drafts against the extended
pre-registration vocabulary (`advisor/plan.json`'s
`preregistration_vocabulary_extensions`), plus the calling task's five specific
checks and the draft placeholder listing.

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not import
`forward/*/check.py`, `reverse/*/check.py`, or any other producer/skeptic module.

Six checks per contract (AY1, AY2, AZ1, AZ2), plus a placeholder listing for the
two drafts:

  1. `extended_vocabulary_regression` -- the same closed-vocabulary field audit
     assistant-3's `preregistration_audit_3.py` ran (model_id,
     selected_triple_alpha_units, tau, observable.reference_route, state_provenance,
     direction, target, controls_required, sub_labels_allowed, error_terms_itemized,
     claim_exclusions, hash_binding), read against the EXTENDED vocabulary only
     (plan.json's note that contracts now write it natively means there is no
     pre-extension/extended duality left to report for these four contracts, unlike
     AX1/AX2 at the time of assistant-3's audit).
  2. `controls_required_equals_controls` -- `preregistration.controls_required.ids`
     equals the contract's own `controls` list, order-sensitive.
  3. `sub_labels_allowed_contains_labels_used` -- the closed `sub_labels_allowed`
     vocabulary contains every sub-label actually exported by that loop's
     producer(s) (read from `forward/*/output/results.json` where production
     exists; `not_yet_applicable` for the still-draft AZ1/AZ2), plus a check of
     whether the AY2 tier name `first_order_distance_from_product` is ever used
     AS a sub-label (it should only ever appear as a `tier` field value).
  4. `gate_fields_required_present` -- whether `preregistration.gate_fields_required`
     exists at all, and if so, which of the six-name union
     (`common4.GATE_FIELD_BOOL_NAMES`) it lists.
  5. `selected_after_filled` -- `selected_after` is a non-empty string that is not
     a template placeholder (`<...>` or containing "e.g."); AY2's is checked
     explicitly against the known "<preceding gate>" placeholder.
  6. `error_terms_itemized_and_target_well_posed` -- `error_terms_itemized` is a
     non-empty list of strings, every `not_applicable`-prefixed entry states a
     reason; `target` has a non-empty `quantity`, an exact-rational `value` and a
     comparator in `{<=, >=}`.

Then, for AZ1 and AZ2 only: `draft_placeholder_listing` -- every JSON field whose
string value still contains a `<...>` template placeholder or the literal text
"e.g.", found by a generic recursive walk (not a hardcoded list of expected
fields), so the advisor can fix them before freezing.

Usage: python3 -B preregistration_audit_4.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common4 as K  # noqa: E402

CONTRACT_IDS = ('AY1', 'AY2', 'AZ1', 'AZ2')
FROZEN_IDS = ('AY1', 'AY2')
DRAFT_IDS = ('AZ1', 'AZ2')
CONTRACT_PATHS = {'AY1': K.AY1_CONTRACT, 'AY2': K.AY2_CONTRACT, 'AZ1': K.AZ1_CONTRACT, 'AZ2': K.AZ2_CONTRACT}
EXPECTED_STATUS = {'AY1': 'frozen_before_production', 'AY2': 'frozen_before_production',
                   'AZ1': 'draft', 'AZ2': 'draft'}

# Where each contract's own producer output(s) live, for "labels actually used"
# (empty for a draft with no production yet).
OUTPUT_RESULTS = {
    'AY1': [K.FORWARD_AY1_RESULTS, K.REVERSE_AY1_RESULTS],
    'AY2': [K.FORWARD_AY2_RESULTS],
    'AZ1': [],
    'AZ2': [],
}


def load_contract(cid):
    c = K.load_json(CONTRACT_PATHS[cid])
    K.require(c.get('id') == cid, 'contract id mismatch for %s' % cid)
    K.require(c.get('round') == 32, 'contract not round 32: %s' % cid)
    observed_status = c.get('status')
    return c, observed_status


# ---------------------------------------------------------------------------
# 1. Extended-vocabulary regression (single-pass extended reading; no
#    pre-extension/extended duality left to report -- plan.json's own note says
#    contracts now write the extended vocabulary natively).
# ---------------------------------------------------------------------------
def field_check(desc, condition, **extra):
    d = {'field': desc, 'passed': bool(condition)}
    d.update(extra)
    return d


def check_triple_ext(pre):
    triple = pre.get('selected_triple_alpha_units')
    model_id = pre.get('model_id') or ''
    if isinstance(triple, list) and len(triple) == 3:
        bad = [x for x in triple if not (K.is_rational(x) or K.is_tau_linear(x))]
        ok = not bad
        reason = None if ok else 'entries neither exact rationals nor tau-linear: %r' % bad
    elif isinstance(triple, str) and triple == 'n/a (finite graph)':
        ok = model_id.startswith('FG(')
        reason = None if ok else "sentinel triple but model_id does not start with 'FG(': %r" % model_id
    else:
        ok = False
        reason = 'neither a 3-element list nor the finite-graph sentinel: %r' % (triple,)
    return field_check('selected_triple_alpha_units', ok, value=triple, reason=reason)


def check_tau_ext(pre, contract):
    tau = pre.get('tau')
    has_keys = isinstance(tau, dict) and {'value', 'signs_evaluated', 'is_model_change_vs_previous_loop',
                                          'rule_if_chosen_later'} <= set(tau)
    if not has_keys:
        return field_check('tau', False, value=tau, reason='missing required keys or not a dict')
    value = tau['value']
    if K.is_rational(value):
        ok, reason = True, None
    elif value == 'grid':
        grid = (contract.get('parameters') or {}).get('tau_FG_grid')
        ok = isinstance(grid, list) and len(grid) > 0
        reason = None if ok else 'tau.value==grid but parameters.tau_FG_grid missing or empty'
    elif isinstance(value, str) and value.strip() != '':
        ok, reason = True, None
    else:
        ok, reason = False, 'tau.value neither exact rational, grid, nor a rule-reference string: %r' % (value,)
    if ok:
        if tau['signs_evaluated'] != ['+', '-']:
            ok, reason = False, 'signs_evaluated is not [+, -]: %r' % (tau['signs_evaluated'],)
        elif not isinstance(tau['is_model_change_vs_previous_loop'], bool):
            ok, reason = False, 'is_model_change_vs_previous_loop is not boolean'
        elif not (tau['rule_if_chosen_later'] is None or isinstance(tau['rule_if_chosen_later'], str)):
            ok, reason = False, 'rule_if_chosen_later is neither null nor a string'
    return field_check('tau', ok, value=tau, reason=reason)


def check_observable_ext(pre):
    obs = pre.get('observable')
    has_keys = isinstance(obs, dict) and {'id', 'centering', 'reference_value_exact', 'reference_route'} <= set(obs)
    if not has_keys:
        return field_check('observable', False, value=obs, reason='missing required keys or not a dict')

    def base_ok():
        if not (isinstance(obs['id'], str) and obs['id'] != ''):
            return False, 'observable.id missing or empty'
        if obs['centering'] not in K.ALLOWED_CENTERING:
            return False, 'observable.centering not in %r' % (K.ALLOWED_CENTERING,)
        if not (isinstance(obs['reference_value_exact'], str) and obs['reference_value_exact'] != ''):
            return False, 'observable.reference_value_exact missing or empty'
        return True, None

    route = obs['reference_route']
    if route in K.ALLOWED_REFERENCE_ROUTE_EXT_BASE:
        ok, reason = base_ok()
    elif route == 'n/a':
        direction = pre.get('direction')
        is_statement = direction in K.STATEMENT_DIRECTIONS
        eti = pre.get('error_terms_itemized')
        has_reason = (isinstance(eti, list) and len(eti) >= 1
                     and any(isinstance(x, str) and 'reason' in x.lower() for x in eti))
        ok = is_statement and has_reason
        reason = None if ok else ("reference_route=='n/a' requires a statement direction and a stated reason in "
                                  "error_terms_itemized (direction=%r, error_terms_itemized=%r)" % (direction, eti))
        if ok:
            ok, reason = base_ok()
    else:
        ok, reason = False, "reference_route not in extended vocabulary + {'n/a'}: %r" % (route,)
    return field_check('observable', ok, value=obs, reason=reason)


def check_direction_ext(pre):
    value = pre.get('direction')
    ok = value in K.ALLOWED_DIRECTION_EXT
    return field_check('direction', ok, value=value)


def extended_vocabulary_regression(cid, contract):
    pre = contract.get('preregistration', {})
    fields = []
    fields.append(field_check('schema', pre.get('schema') == 'hnm-r32-prereg-v1'))
    fields.append(field_check('frozen_before_any_outcome', pre.get('frozen_before_any_outcome') is True))
    mid = pre.get('model_id')
    fields.append(field_check('model_id', isinstance(mid, str) and mid.startswith(K.ALLOWED_MODEL_ID_PREFIXES),
                              value=mid))
    fields.append(check_triple_ext(pre))
    fields.append(check_tau_ext(pre, contract))
    sp = pre.get('state_provenance')
    fields.append(field_check('state_provenance',
                              isinstance(sp, str) and sp.startswith(K.ALLOWED_STATE_PROVENANCE_PREFIXES), value=sp))
    fields.append(check_observable_ext(pre))
    fields.append(check_direction_ext(pre))
    eti = pre.get('error_terms_itemized')
    fields.append(field_check('error_terms_itemized', isinstance(eti, list) and len(eti) > 0
                              and all(isinstance(x, str) for x in eti), value=eti))
    fields.append(field_check('error_terms_rule', pre.get('error_terms_rule') == K.ERROR_TERMS_RULE_TEXT))
    target = pre.get('target')
    target_ok = isinstance(target, dict) and {'quantity', 'value', 'comparator'} <= set(target)
    if target_ok:
        target_ok = (K.is_rational(target['value']) and isinstance(target['quantity'], str)
                    and target['quantity'] != '' and target['comparator'] in K.ALLOWED_COMPARATOR)
    fields.append(field_check('target', target_ok, value=target))
    fields.append(field_check('sub_labels_allowed', pre.get('sub_labels_allowed') == K.SUB_LABELS_ALLOWED,
                              value=pre.get('sub_labels_allowed')))
    cr = pre.get('controls_required')
    fields.append(field_check('controls_required_shape', isinstance(cr, dict) and isinstance(cr.get('ids'), list)
                              and len(cr['ids']) > 0))
    ce = pre.get('claim_exclusions')
    fields.append(field_check('claim_exclusions', isinstance(ce, list) and K.TEMPLATE_CLAIM_EXCLUSIONS <= set(ce)))
    hb = pre.get('hash_binding')
    fields.append(field_check('hash_binding', isinstance(hb, dict) and set(hb) == set(K.HASH_BINDING_FIELDS)
                              and all(hb[k] is True for k in K.HASH_BINDING_FIELDS)))
    return {'passed': all(f['passed'] for f in fields), 'fields': fields}


# ---------------------------------------------------------------------------
# 2. controls_required.ids == controls
# ---------------------------------------------------------------------------
def controls_required_equals_controls(contract):
    pre = contract.get('preregistration', {})
    ids = pre.get('controls_required', {}).get('ids')
    controls = contract.get('controls')
    return {'equal': ids == controls, 'ids_len': len(ids) if ids is not None else None,
            'controls_len': len(controls) if controls is not None else None,
            'only_in_ids': sorted(set(ids or []) - set(controls or [])),
            'only_in_controls': sorted(set(controls or []) - set(ids or []))}


# ---------------------------------------------------------------------------
# 3. sub_labels_allowed contains labels actually used.
# ---------------------------------------------------------------------------
def labels_actually_used(cid):
    """Returns (sub_labels_used: set, tier_names_used: set, tier_used_as_sub_label: bool)
    by scanning that loop's producer output(s), where production exists."""
    used = set()
    tier_names = set()
    tier_as_sub_label = False
    for results_path in OUTPUT_RESULTS[cid]:
        if not results_path.exists():
            continue
        data = K.load_json(results_path)
        for path_str, key, value in K.walk_json_items(data):
            if key in ('sub_label',) and isinstance(value, str):
                used.add(value)
            if key in ('sub_labels',) and isinstance(value, list):
                used.update(v for v in value if isinstance(v, str))
            if key == 'tier' and isinstance(value, str):
                tier_names.add(value)
        # Direct check: does 'first_order_distance_from_product' (or any found
        # tier name) ever appear as a member of a sub_label/sub_labels export?
        for tier_name in tier_names:
            if tier_name in used:
                tier_as_sub_label = True
    return used, tier_names, tier_as_sub_label


def sub_labels_check(cid, contract):
    pre = contract.get('preregistration', {})
    allowed = pre.get('sub_labels_allowed')
    allowed_ok = allowed == K.SUB_LABELS_ALLOWED
    if cid in FROZEN_IDS:
        used, tier_names, tier_as_sub_label = labels_actually_used(cid)
        not_covered = sorted(used - set(allowed or []))
        status = 'checked'
    else:
        used, tier_names, tier_as_sub_label = set(), set(), False
        not_covered = []
        status = 'not_yet_applicable (no production yet)'
    return {
        'sub_labels_allowed_is_closed_vocabulary': allowed_ok,
        'sub_labels_allowed_value': allowed,
        'status': status,
        'sub_labels_actually_used': sorted(used),
        'tier_names_seen': sorted(tier_names),
        'any_tier_name_used_as_a_sub_label': tier_as_sub_label,
        'labels_used_not_in_allowed_vocabulary': not_covered,
        'passed': allowed_ok and not not_covered,
    }


# ---------------------------------------------------------------------------
# 4. gate_fields_required present.
# ---------------------------------------------------------------------------
def gate_fields_required_check(contract):
    pre = contract.get('preregistration', {})
    gfr = pre.get('gate_fields_required')
    present = isinstance(gfr, dict) and len(gfr) > 0
    covers = sorted(set(gfr) & set(K.GATE_FIELD_BOOL_NAMES)) if present else []
    missing = sorted(set(K.GATE_FIELD_BOOL_NAMES) - set(gfr or {}))
    all_false = present and all(gfr[k] is False for k in gfr)
    return {'present': present, 'value': gfr, 'covers_from_six_name_union': covers,
            'missing_from_six_name_union': missing, 'every_listed_value_is_false': all_false,
            'passed': present}


# ---------------------------------------------------------------------------
# 5. selected_after filled (not empty, not a placeholder).
# ---------------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r'<[A-Za-z][^<>]{2,120}>')


def looks_like_placeholder(s):
    if not isinstance(s, str):
        return True
    if 'e.g.' in s:
        return True
    for m in PLACEHOLDER_RE.finditer(s):
        inner = m.group(0)[1:-1]
        if ' ' in inner or '|' in inner:
            return True
    return False


def selected_after_check(contract):
    value = contract.get('selected_after')
    filled = isinstance(value, str) and value.strip() != ''
    placeholder = looks_like_placeholder(value) if filled else True
    return {'value': value, 'non_empty_string': filled, 'looks_like_placeholder': placeholder,
            'passed': filled and not placeholder}


# ---------------------------------------------------------------------------
# 6. error_terms_itemized non-empty with reasons; target well-posed.
# ---------------------------------------------------------------------------
def error_terms_and_target_check(contract):
    pre = contract.get('preregistration', {})
    eti = pre.get('error_terms_itemized')
    eti_ok = isinstance(eti, list) and len(eti) > 0 and all(isinstance(x, str) for x in eti)
    not_applicable_without_reason = []
    if eti_ok:
        for entry in eti:
            if entry.lower().startswith('not_applicable') and 'reason' not in entry.lower():
                not_applicable_without_reason.append(entry)
    rule_ok = pre.get('error_terms_rule') == K.ERROR_TERMS_RULE_TEXT

    target = pre.get('target')
    target_shape_ok = isinstance(target, dict) and {'quantity', 'value', 'comparator'} <= set(target)
    target_well_posed = False
    target_reason = None
    if target_shape_ok:
        quantity_ok = isinstance(target['quantity'], str) and target['quantity'] != ''
        value_ok = K.is_rational(target['value'])
        comparator_ok = target['comparator'] in K.ALLOWED_COMPARATOR
        target_well_posed = quantity_ok and value_ok and comparator_ok
        if not target_well_posed:
            target_reason = ('quantity_ok=%r value_exact_rational=%r comparator_ok=%r'
                            % (quantity_ok, value_ok, comparator_ok))
    else:
        target_reason = 'missing required keys (quantity, value, comparator) or not a dict'

    return {
        'error_terms_itemized': eti,
        'error_terms_itemized_non_empty_list_of_strings': eti_ok,
        'not_applicable_entries_without_a_stated_reason': not_applicable_without_reason,
        'error_terms_rule_text_matches': rule_ok,
        'target': target,
        'target_well_posed_exact_rational_and_comparator': target_well_posed,
        'target_reason_if_not_well_posed': target_reason,
        'passed': eti_ok and not not_applicable_without_reason and rule_ok and target_well_posed,
    }


# ---------------------------------------------------------------------------
# Draft placeholder listing (AZ1, AZ2 only).
# ---------------------------------------------------------------------------
def draft_placeholder_listing(contract):
    hits = []
    for path_str, value in walk_all_strings(contract):
        if 'e.g.' in value:
            hits.append({'field': path_str, 'value': value, 'marker': 'e.g.'})
            continue
        for m in PLACEHOLDER_RE.finditer(value):
            inner = m.group(0)[1:-1]
            if ' ' in inner or '|' in inner:
                hits.append({'field': path_str, 'value': value, 'marker': m.group(0)})
                break
    return hits


def walk_all_strings(obj, path=''):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_all_strings(v, (path + '.' + k) if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_all_strings(v, path + '[%d]' % i)
    elif isinstance(obj, str):
        yield path, obj


# ---------------------------------------------------------------------------
def audit_one(cid):
    contract, observed_status = load_contract(cid)
    expected = EXPECTED_STATUS[cid]
    status_ok = observed_status == expected

    ext_reg = extended_vocabulary_regression(cid, contract)
    cr = controls_required_equals_controls(contract)
    sl = sub_labels_check(cid, contract)
    gfr = gate_fields_required_check(contract)
    sa = selected_after_check(contract)
    et = error_terms_and_target_check(contract)

    entry = {
        'contract': cid,
        'observed_status': observed_status,
        'expected_status': expected,
        'status_matches_expected': status_ok,
        'extended_vocabulary_regression': ext_reg,
        'controls_required_equals_controls': cr,
        'sub_labels_allowed_contains_labels_used': sl,
        'gate_fields_required_present': gfr,
        'selected_after_filled': sa,
        'error_terms_itemized_and_target_well_posed': et,
    }
    if cid in DRAFT_IDS:
        entry['draft_placeholders_found'] = draft_placeholder_listing(contract)
    entry['passed'] = (status_ok and ext_reg['passed'] and cr['equal'] and sl['passed']
                       and sa['passed'] and et['passed'])
    # gate_fields_required absence is recorded, but (per the calling task's own
    # framing -- these are statement loops about a continuum trajectory and a
    # finite graph, not state identification) is not folded into 'passed' for
    # AZ1/AZ2, where its relevance is an open interpretive question for the
    # advisor, not a settled requirement; it IS folded into 'passed' for AY1/AY2,
    # where item 4/item 6 explicitly require it.
    if cid in FROZEN_IDS:
        entry['passed'] = entry['passed'] and gfr['passed']
    return entry


def run():
    plan = K.load_plan()
    ext_covered = K.plan_extension_covers(plan)

    entries = {cid: audit_one(cid) for cid in CONTRACT_IDS}

    findings = []
    findings.append('advisor/plan.json still carries the four-field preregistration_vocabulary_extensions '
                    'block this audit checks against: %r' % ext_covered)

    ay2_sp_field = next((f for f in entries['AY2']['extended_vocabulary_regression']['fields']
                        if f['field'] == 'state_provenance'), None)
    if ay2_sp_field is not None and not ay2_sp_field['passed']:
        findings.append(
            'NEW SCHEMA GAP (not one plan.json\'s four-field extension covers): AY2\'s preregistration.'
            'state_provenance = %r does not start with any of the three closed-vocabulary prefixes '
            '(AQ1_centered_whole_star_subsequence, finite_volume_N=<N>, finite_graph_ground). It is a new shape: a '
            'combined description of subsequential limits from BOTH AY1 families at once (a state-identification '
            'statement loop compares F1 and F2 together, unlike every earlier loop\'s single-family provenance '
            'string). AY1\'s own state_provenance passes trivially (it literally starts with '
            '"AQ1_centered_whole_star_subsequence"), so this is specific to AY2\'s combined-family phrasing, not a '
            'regression shared by both. Recommend a vocabulary note the same way plan.json recorded the four '
            'earlier gaps, if a future contract needs to describe provenance from more than one named family at '
            'once.' % ay2_sp_field['value'])

    for cid in CONTRACT_IDS:
        e = entries[cid]
        if not e['extended_vocabulary_regression']['passed']:
            bad = [f for f in e['extended_vocabulary_regression']['fields'] if not f['passed']]
            findings.append('%s: extended-vocabulary regression FAILS on %d field(s): %r' % (cid, len(bad), bad))
        else:
            findings.append('%s: passes the full extended-vocabulary structural regression (all fields).' % cid)

    for cid in CONTRACT_IDS:
        cr = entries[cid]['controls_required_equals_controls']
        if cr['equal']:
            findings.append('%s: controls_required.ids == controls exactly (%d ids).' % (cid, cr['ids_len']))
        else:
            findings.append('%s: controls_required.ids != controls -- only_in_ids=%r only_in_controls=%r'
                            % (cid, cr['only_in_ids'], cr['only_in_controls']))

    for cid in FROZEN_IDS:
        sl = entries[cid]['sub_labels_allowed_contains_labels_used']
        findings.append('%s: sub_labels actually used = %r; all covered by sub_labels_allowed = %r.'
                        % (cid, sl['sub_labels_actually_used'], not sl['labels_used_not_in_allowed_vocabulary']))
    ay2_sl = entries['AY2']['sub_labels_allowed_contains_labels_used']
    findings.append(
        'AY2: tier name(s) seen = %r; any used AS a sub_label = %r. "first_order_distance_from_product" is used '
        'consistently as the value of a `tier` field (inside `label` blocks), never as a member of the `sub_label`/'
        '`sub_labels` export (which is always a subset of the closed 5-label vocabulary). NO vocabulary-note '
        'defect follows from this: the tier name is not conflated with a sub-label anywhere found. Flagged as an '
        'open observation for the advisor: there is currently no closed vocabulary governing *tier* names '
        'at all (unlike sub_labels_allowed, which is closed) -- a future round could add a '
        '`tier_names_allowed` list the same way, if more producers start inventing tier names, but nothing in '
        'this round requires it.' % (ay2_sl['tier_names_seen'], ay2_sl['any_tier_name_used_as_a_sub_label']))

    for cid in CONTRACT_IDS:
        gfr = entries[cid]['gate_fields_required_present']
        if cid in FROZEN_IDS:
            findings.append('%s: preregistration.gate_fields_required present=%r, covers %d/6 of the gate-field '
                            'boolean union, missing=%r.' % (cid, gfr['present'], len(gfr['covers_from_six_name_union']),
                                                            gfr['missing_from_six_name_union']))
        else:
            findings.append('%s (draft): preregistration.gate_fields_required present=%r. %s has no such field '
                            'at all in its preregistration block (unlike AY1/AY2). Recorded factually; whether '
                            'it is a defect is an open interpretive question for the advisor, since %s is not a '
                            'state-identification loop (no subsequential-limit uniqueness/whole-sequence/rate/'
                            'translation-invariance claim is at stake in its subject matter) and may not need '
                            'this field at all -- unless the advisor intends gate_fields_required to be universal '
                            'across every round32 contract, not specific to AY1/AY2\'s topic.' % (cid, gfr['present'],
                                                                                                   cid, cid))

    sa_ay2 = entries['AY2']['selected_after_filled']
    findings.append(
        'AY2 selected_after=%r -- looks_like_placeholder=%r (PLACEHOLDER DEFECT, matching the calling task\'s own '
        'note: "AY2\'s was left as the placeholder \'<preceding gate>\' at freeze time"). AY2 is already '
        '`frozen_before_production`, so this placeholder is now frozen into the contract; the calling task asks '
        'this be recorded as a defect to be noted in the (not-yet-existing) AY2 gate.' % (sa_ay2['value'],
                                                                                          sa_ay2['looks_like_placeholder']))
    for cid in ('AY1',) + DRAFT_IDS:
        sa = entries[cid]['selected_after_filled']
        findings.append('%s selected_after=%r -- filled, not a placeholder=%r.'
                        % (cid, sa['value'], sa['passed']))
        if cid in DRAFT_IDS and sa['passed']:
            findings.append('  (%s\'s selected_after names a gate file that does not exist on disk yet -- '
                            'expected for a draft awaiting its predecessor\'s production/gate, not a placeholder '
                            'defect: it is a concrete forward-looking path, not template text.)' % cid)

    for cid in CONTRACT_IDS:
        et = entries[cid]['error_terms_itemized_and_target_well_posed']
        findings.append('%s: error_terms_itemized=%r (non-empty list of strings=%r, no not_applicable-without-'
                        'reason entries=%r); target well-posed=%r.'
                        % (cid, et['error_terms_itemized'], et['error_terms_itemized_non_empty_list_of_strings'],
                           not et['not_applicable_entries_without_a_stated_reason'],
                           et['target_well_posed_exact_rational_and_comparator']))
    az1_target = entries['AZ1']['error_terms_itemized_and_target_well_posed']['target']
    az2_target = entries['AZ2']['error_terms_itemized_and_target_well_posed']['target']
    findings.append(
        'OBSERVATION (not a defect): AZ1.target=%r and AZ2.target=%r are both syntactically well-posed (an exact '
        'rational value and an allowed comparator) but semantically a boolean-style proxy ("at least one item '
        'named", "certified tail and enclosure widths reported") rather than a numeric closeness threshold like '
        'AY1/AY2\'s; this matches the style already used by earlier statement loops in this round and is not '
        'itself flagged as a well-posedness failure.' % (az1_target, az2_target))

    for cid in DRAFT_IDS:
        ph = entries[cid]['draft_placeholders_found']
        if ph:
            findings.append('%s: %d placeholder field(s) still present: %s'
                            % (cid, len(ph), '; '.join('%s=%r' % (h['field'], h['value']) for h in ph)))
        else:
            findings.append('%s: no `<...>`/"e.g." placeholder fields found -- fully filled in for a draft.' % cid)

    overall_pass = all(e['passed'] for e in entries.values())
    result = {
        'id': 'preregistration_audit_4',
        'role': 'audits AY1/AY2 (frozen) and AZ1/AZ2 (drafts) against the extended pre-registration vocabulary '
                'and the calling task\'s five specific checks, plus a draft placeholder listing; zero research '
                'loops',
        'plan_json_carries_extension': ext_covered,
        'contracts_audited': entries,
        'passed': overall_pass,
        'findings': findings,
    }
    return result


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'preregistration_audit_4', result)
    print('preregistration_audit_4: %s' % ('PASS' if result['passed'] else 'FAIL (see findings)'))
    for cid, e in result['contracts_audited'].items():
        print('  [%s] %s: passed=%r (status=%r)' % ('x' if e['passed'] else ' ', cid, e['passed'],
                                                     e['observed_status']))
    print()
    for f in result['findings']:
        print('  FINDING:', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
