#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 5, assistant-5 script 1 of 3: the final
pre-registration integration audit over all ten Round32 contracts (panel-
update-4.md item 7, Jung update-4.md section 4 item 1-3/6, calling task item 1).

Counts zero research loops. Not a producer, contract, gate or skeptical
review; nothing computed here is read back into any of those. Human project
author: Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not
import `forward/*/check.py`, `reverse/*/check.py`, or any other
producer/skeptic module.

For all ten contracts (`research/round32/contracts/av1.json` .. `az2.json`):

  1. `frozen_status_check` -- `status == "frozen_before_production"` and
     `frozen_at` is a non-empty string, for every contract.
  2. `controls_mirror_check` -- `preregistration.controls_required.ids ==
     controls`, order-sensitive, for every contract (continuing the AV2-
     mirror-gap check lineage panel-update-4.md item 5 names).
  3. `gate_fields_required_check` -- `preregistration.gate_fields_required`
     present where the vocabulary extension requires it (AY1, AY2, AZ1, AZ2:
     the two AZ contracts use their own topic-specific unions, not the six-
     name state-identification union); for each such contract, every required
     field is checked to be exported with the required boolean value in that
     loop's own producer `output/results.json` file(s) (forward, and reverse
     where one exists), and, where the gate JSON carries a `gate_fields`
     sub-object, there too.
  4. `mandatory_sentence_template_check` -- `preregistration.
     mandatory_sentence_template` present for AZ1 and AZ2 (the calling task's
     scope; AY1/AY2's template situation was assistant-4's finding and is not
     re-litigated here beyond a one-line cross-reference), and the template
     sentence present verbatim (modulo the filled-in numeric constants) in
     every report.md AZ1/AZ2 has (each has exactly one: no reverse producer
     exists for either).
  5. `selected_after_check` -- AY2's `selected_after` is still the literal
     placeholder `"<preceding gate>"` (recorded, not fixed: AY2 is frozen and
     immutable); AZ2's `selected_after` names a gate file
     (`research/round32/advisor/az1-gate.json`) that did not yet exist on disk
     at AZ2's own freeze timestamp (recorded as the drafts' ordinary look-
     ahead convention, not a placeholder defect, by comparing AZ2's
     `frozen_at` against AZ1 gate's `completed_at`).
  6. `state_provenance_check` -- every contract's `preregistration.
     state_provenance` checked against both `advisor/plan.json`
     `preregistration_vocabulary_extensions` entries (the original three-
     prefix vocabulary, and the second extension's "may name more than one
     family at once" allowance).
  7. `aq_state_phrase_check` -- literal occurrences of "uniqueness of the AQ
     state" in each contract's `claim_exclusions`: frozen AV1-AY2 contracts
     are expected to still carry it (grandfathered, unamended, per plan.json);
     AZ1/AZ2 are expected to carry "uniqueness of any subsequential limit"
     instead and not the old phrase.
  8. `sub_labels_used_vs_allowed_check` -- for every contract,
     `sub_labels_allowed` equals the closed 5-label vocabulary, and every
     sub-label/secondary-sub-label actually exported by that loop's own
     producer(s) is a member of it.
  9. `certification_target_note_check` -- AZ1's and AZ2's
     `preregistration.target.note` states the target is a feasibility/format
     check on an admitted or rehearsed quantity, not a blind discovery
     threshold (the second plan.json extension's `target_of_a_certification_
     loop` rule), and AY2 is confirmed as the recorded accepted exception
     (its own note lacks the literal phrase; plan.json names this itself).

Usage: python3 -B final_preregistration_audit.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common5 as K  # noqa: E402

REQUIRE_GATE_FIELDS = ('AY1', 'AY2', 'AZ1', 'AZ2')
AZ_UNION = {'AZ1': K.AZ1_GATE_FIELD_NAMES, 'AZ2': K.AZ2_GATE_FIELD_NAMES}


# ---------------------------------------------------------------------------
# 1. Frozen status + frozen_at present.
# ---------------------------------------------------------------------------
def frozen_status_check():
    per = {}
    for cid in K.ALL_TEN_IDS:
        c = K.load_json(K.TEN_CONTRACT_PATHS[cid])
        status = c.get('status')
        frozen_at = c.get('frozen_at')
        ok = status == 'frozen_before_production' and isinstance(frozen_at, str) and frozen_at.strip() != ''
        per[cid] = {'status': status, 'frozen_at': frozen_at, 'passed': ok}
    passed = all(v['passed'] for v in per.values())
    findings = ['%s: status=%r frozen_at=%r passed=%r' % (cid, v['status'], v['frozen_at'], v['passed'])
                for cid, v in per.items()]
    return {'id': 'frozen_status_check', 'per_contract': per, 'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 2. controls_required.ids == controls.
# ---------------------------------------------------------------------------
def controls_mirror_check():
    per = {}
    for cid in K.ALL_TEN_IDS:
        c = K.load_json(K.TEN_CONTRACT_PATHS[cid])
        ids = c.get('preregistration', {}).get('controls_required', {}).get('ids')
        controls = c.get('controls')
        equal = ids == controls
        per[cid] = {
            'equal': equal, 'ids_len': len(ids) if ids is not None else None,
            'controls_len': len(controls) if controls is not None else None,
            'only_in_ids': sorted(set(ids or []) - set(controls or [])),
            'only_in_controls': sorted(set(controls or []) - set(ids or [])),
        }
    passed = all(v['equal'] for v in per.values())
    findings = []
    for cid, v in per.items():
        if v['equal']:
            findings.append('%s: controls_required.ids == controls exactly (%d ids).' % (cid, v['ids_len']))
        else:
            findings.append('DEFECT: %s: controls_required.ids != controls (ids_len=%r controls_len=%r) '
                            '-- only_in_ids=%r only_in_controls=%r'
                            % (cid, v['ids_len'], v['controls_len'], v['only_in_ids'], v['only_in_controls']))
    return {'id': 'controls_mirror_check', 'per_contract': per, 'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 3. gate_fields_required present + correctly exported/valued.
# ---------------------------------------------------------------------------
def required_gate_union_for(cid, contract):
    """The names+expected-values this contract's own gate_fields_required
    dict actually lists (ground truth is the contract, not a hardcoded
    union), plus, for AY1/AY2/AZ1/AZ2, the topic union the vocabulary
    extension names, recorded for comparison."""
    pre = contract.get('preregistration', {})
    gfr = pre.get('gate_fields_required')
    return gfr if isinstance(gfr, dict) else {}


def scan_bool_field_in_json(path, name):
    """All (json_path, value) occurrences of key `name` in the JSON at path."""
    if not path.exists():
        return None
    data = K.load_json(path)
    return K.find_key_occurrences(data, name)


def gate_fields_required_check():
    per = {}
    for cid in REQUIRE_GATE_FIELDS:
        contract = K.load_json(K.TEN_CONTRACT_PATHS[cid])
        gfr = required_gate_union_for(cid, contract)
        present = isinstance(gfr, dict) and len(gfr) > 0
        gate_path = K.TEN_GATE_PATHS[cid]
        gate = K.load_json(gate_path) if gate_path.exists() else None
        gate_fields = gate.get('gate_fields') if isinstance(gate, dict) else None
        gate_has_gate_fields = isinstance(gate_fields, dict)

        producer_paths = [K.TEN_FORWARD_RESULTS_PATHS[cid]]
        if cid in K.TEN_REVERSE_RESULTS_PATHS:
            producer_paths.append(K.TEN_REVERSE_RESULTS_PATHS[cid])

        per_field = {}
        all_ok = present
        for name, expected in gfr.items():
            producer_hits = {}
            producer_field_ok = True
            for p in producer_paths:
                occs = scan_bool_field_in_json(p, name)
                if occs is None:
                    producer_hits[str(p.relative_to(K.ROOT))] = {'exists': False}
                    continue
                values = [v for (_, v) in occs]
                exported = len(values) > 0
                all_expected = exported and all(v == expected for v in values)
                producer_hits[str(p.relative_to(K.ROOT))] = {
                    'exists': True, 'n_occurrences': len(occs), 'values': values, 'all_equal_expected': all_expected,
                }
                if not (exported and all_expected):
                    producer_field_ok = False
            gate_ok = None
            if gate_has_gate_fields:
                gate_val = gate_fields.get(name, '<absent>')
                gate_ok = gate_val == expected
            field_ok = producer_field_ok and (gate_ok is not False)
            per_field[name] = {
                'expected_value': expected, 'producer_hits': producer_hits, 'producer_field_ok': producer_field_ok,
                'gate_has_gate_fields': gate_has_gate_fields,
                'gate_value': gate_fields.get(name, '<absent>') if gate_has_gate_fields else None,
                'gate_field_ok': gate_ok, 'passed': field_ok,
            }
            all_ok = all_ok and field_ok

        per[cid] = {
            'gate_fields_required_present': present, 'gate_fields_required_value': gfr,
            'topic_union_from_vocabulary_extension': list(AZ_UNION.get(cid, K.GATE_FIELD_BOOL_NAMES)),
            'union_matches_topic_extension': (sorted(gfr) == sorted(AZ_UNION[cid]) if cid in AZ_UNION else None),
            'per_field': per_field, 'passed': all_ok,
        }

    passed = all(v['passed'] for v in per.values())
    findings = []
    for cid, v in per.items():
        findings.append('%s: gate_fields_required present=%r, value=%r.' % (cid, v['gate_fields_required_present'],
                                                                             v['gate_fields_required_value']))
        if cid in AZ_UNION and v['union_matches_topic_extension'] is False:
            findings.append('  DEFECT: %s gate_fields_required does not match the %s topic union named in '
                            'panel-update-4.md/Jung update-4.md section 3: expected %r, found %r.'
                            % (cid, cid, sorted(AZ_UNION[cid]), sorted(v['gate_fields_required_value'])))
        for name, f in v['per_field'].items():
            status_bits = []
            for pth, hit in f['producer_hits'].items():
                if not hit.get('exists'):
                    status_bits.append('%s: no export' % pth)
                else:
                    status_bits.append('%s: %r (all_equal_expected=%r)'
                                       % (pth, hit['values'], hit['all_equal_expected']))
            gate_bit = ('gate.gate_fields.%s=%r (ok=%r)' % (name, f['gate_value'], f['gate_field_ok'])
                       if f['gate_has_gate_fields'] else 'gate has no gate_fields sub-object')
            line = '  %s.%s: expected=%r; %s; %s' % (cid, name, f['expected_value'], '; '.join(status_bits), gate_bit)
            if not f['passed']:
                line = 'DEFECT: ' + line
            findings.append(line)
    return {'id': 'gate_fields_required_check', 'per_contract': per, 'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 4. mandatory_sentence_template present for AZ1/AZ2, verbatim modulo
#    constants in every report.md each has.
# ---------------------------------------------------------------------------
CONST_SPLIT_RE = __import__('re').compile(r'[-+]?\d[\d/^*x.,eE]*\d|\b\d\b')


def segments_modulo_constants(template):
    parts = CONST_SPLIT_RE.split(template)
    return [K.normalize_sentence(p) for p in parts if K.normalize_sentence(p)]


def sentence_present_modulo_constants(template, text):
    norm_text = K.normalize_sentence(text)
    segs = segments_modulo_constants(template)
    pos = 0
    for seg in segs:
        idx = norm_text.find(seg, pos)
        if idx == -1:
            return False, seg
        pos = idx + len(seg)
    return True, None


def mandatory_sentence_template_check():
    per = {}
    for cid in ('AZ1', 'AZ2'):
        contract = K.load_json(K.TEN_CONTRACT_PATHS[cid])
        template = contract.get('preregistration', {}).get('mandatory_sentence_template')
        template_present = isinstance(template, str) and template.strip() != ''
        report_checks = {}
        if template_present:
            report_paths = {'forward_report': K.TEN_FORWARD_REPORT_PATHS[cid]}
            if cid in K.TEN_REVERSE_REPORT_PATHS:
                report_paths['reverse_report'] = K.TEN_REVERSE_REPORT_PATHS[cid]
            for label, path in report_paths.items():
                text = K.load_text(path)
                ok, failed_seg = sentence_present_modulo_constants(template, text)
                report_checks[label] = {'path': str(path.relative_to(K.ROOT)), 'passed': ok,
                                        'first_failed_segment': failed_seg}
            # Bonus coverage: the gate's own accepted+decision text (not required
            # by the calling task, which names report.md only, but recorded since
            # both AZ1 and AZ2 gates were found to carry it -- unlike AY1/AY2).
            gate = K.load_json(K.TEN_GATE_PATHS[cid])
            gate_text = (gate.get('accepted', '') or '') + ' ' + (gate.get('decision', '') or '')
            ok, failed_seg = sentence_present_modulo_constants(template, gate_text)
            report_checks['gate_accepted_plus_decision_bonus'] = {
                'path': str(K.TEN_GATE_PATHS[cid].relative_to(K.ROOT)), 'passed': ok,
                'first_failed_segment': failed_seg,
            }
        required_ok = template_present and all(
            v['passed'] for k, v in report_checks.items() if k != 'gate_accepted_plus_decision_bonus')
        per[cid] = {'template_present': template_present, 'template': template, 'report_checks': report_checks,
                    'passed': required_ok}

    passed = all(v['passed'] for v in per.values())
    findings = ['Scope, per the calling task: mandatory_sentence_template checked for AZ1/AZ2 only '
                '(AY1/AY2\'s template situation is assistant-4\'s own finding -- see cross-reference below).']
    for cid, v in per.items():
        if not v['template_present']:
            findings.append('DEFECT: %s: preregistration.mandatory_sentence_template is absent or empty.' % cid)
            continue
        findings.append('%s: mandatory_sentence_template present.' % cid)
        for label, r in v['report_checks'].items():
            tag = 'bonus (gate)' if label == 'gate_accepted_plus_decision_bonus' else 'required'
            if r['passed']:
                findings.append('  %s [%s]: template present verbatim modulo constants.' % (r['path'], tag))
            else:
                findings.append('  %s DEFECT [%s]: template NOT found (first unmatched literal segment: %r).'
                                % (r['path'], tag, r['first_failed_segment']))
    findings.append('Cross-reference (not re-audited here): assistant-4/README.md documents that AY1\'s '
                    'preregistration.mandatory_sentence_template field exists but is a paraphrase, not the Jung '
                    'loop2-response.md verbatim form, and that AY2 has no mandatory_sentence_template field at '
                    'all; both are recorded as grandfathered, contracts unamended, in advisor/plan.json\'s second '
                    'preregistration_vocabulary_extensions entry.')
    return {'id': 'mandatory_sentence_template_check', 'per_contract': per, 'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 5. selected_after placeholders.
# ---------------------------------------------------------------------------
def selected_after_check():
    ay2 = K.load_json(K.TEN_CONTRACT_PATHS['AY2'])
    ay2_sa = ay2.get('selected_after')
    ay2_is_placeholder = ay2_sa == '<preceding gate>'

    az2 = K.load_json(K.TEN_CONTRACT_PATHS['AZ2'])
    az2_sa = az2.get('selected_after')
    az2_frozen_at = az2.get('frozen_at')
    az1_gate = K.load_json(K.TEN_GATE_PATHS['AZ1']) if K.TEN_GATE_PATHS['AZ1'].exists() else None
    az1_gate_completed_at = az1_gate.get('completed_at') if az1_gate else None
    az2_points_to_az1_gate = az2_sa == 'research/round32/advisor/az1-gate.json'
    az2_pointed_to_not_yet_existing_gate = (
        az2_points_to_az1_gate and az1_gate_completed_at is not None
        and az2_frozen_at is not None and az2_frozen_at < az1_gate_completed_at
    )

    all_sa = {}
    for cid in K.ALL_TEN_IDS:
        c = K.load_json(K.TEN_CONTRACT_PATHS[cid])
        all_sa[cid] = c.get('selected_after')

    findings = [
        'AY2 selected_after=%r -- still the literal placeholder \'<preceding gate>\'=%r. AY2 is frozen_before_'
        'production and immutable (AGENTS.md); this is recorded, not fixed, matching assistant-4\'s finding and '
        'the AY2 gate\'s own defect D1.' % (ay2_sa, ay2_is_placeholder),
        'AZ2 selected_after=%r, AZ2 frozen_at=%r; AZ1 gate completed_at=%r. AZ2\'s selected_after names the AZ1 '
        'gate, which did not yet exist on disk at AZ2\'s own freeze timestamp (frozen_at < az1-gate completed_at = '
        '%r): a real, forward-looking path to a not-yet-existing gate, matching the drafts\' ordinary look-ahead '
        'convention (assistant-4\'s README: "expected for a draft awaiting its predecessor\'s gate, not a '
        'placeholder defect"), NOT a template-placeholder defect.'
        % (az2_sa, az2_frozen_at, az1_gate_completed_at, az2_pointed_to_not_yet_existing_gate),
    ]
    for cid, sa in all_sa.items():
        if cid in ('AY2', 'AZ2'):
            continue
        findings.append('%s selected_after=%r.' % (cid, sa))

    passed = ay2_is_placeholder and az2_pointed_to_not_yet_existing_gate  # both are the EXPECTED, recorded shape
    return {
        'id': 'selected_after_check',
        'ay2_selected_after': ay2_sa, 'ay2_is_known_placeholder': ay2_is_placeholder,
        'az2_selected_after': az2_sa, 'az2_frozen_at': az2_frozen_at, 'az1_gate_completed_at': az1_gate_completed_at,
        'az2_pointed_to_not_yet_existing_gate_at_freeze_time': az2_pointed_to_not_yet_existing_gate,
        'all_selected_after': all_sa,
        'passed': passed,  # True means "matches the expected/recorded shape", not "no issue exists"
        'findings': findings,
    }


# ---------------------------------------------------------------------------
# 6. state_provenance shapes against both vocabulary extensions.
# ---------------------------------------------------------------------------
def state_provenance_check():
    plan = K.load_plan()
    ext = plan.get('preregistration_vocabulary_extensions') or []
    ext2 = next((e for e in ext if 'state_provenance' in e), None)

    per = {}
    for cid in K.ALL_TEN_IDS:
        contract = K.load_json(K.TEN_CONTRACT_PATHS[cid])
        pre = contract.get('preregistration', {})
        sp = pre.get('state_provenance')
        model_id = pre.get('model_id', '') or ''
        matches_ext1 = isinstance(sp, str) and sp.startswith(K.ALLOWED_STATE_PROVENANCE_PREFIXES)
        is_finite_graph_model = model_id.startswith('FG(')
        # Extension-2 shape: names more than one family (heuristically: mentions
        # "both" or two of the known family names/prefixes together) without
        # starting with a single closed-vocabulary prefix.
        multi_family_markers = sum(1 for marker in
                                   ('AQ1 centered whole-star', 'I1 all-contained-face', 'both')
                                   if isinstance(sp, str) and marker.lower() in sp.lower())
        looks_like_ext2_multi_family = (not matches_ext1) and multi_family_markers >= 2
        # Semantic check, independent of the structural prefix match: a
        # finite-graph model (model_id starts with "FG(") has no subsequential
        # limit at all (nothing "converges" as N grows on a fixed, closed
        # graph), so its state_provenance should use the vocabulary's own
        # 'finite_graph_ground' prefix, not an AQ1-subsequence prefix that
        # happens to match structurally only because it is boilerplate text
        # copied unedited from a subsequential-limit contract.
        uses_aq1_subsequence_prefix = isinstance(sp, str) and sp.startswith('AQ1_centered_whole_star_subsequence')
        uses_finite_graph_ground_prefix = isinstance(sp, str) and sp.startswith('finite_graph_ground')
        finite_graph_model_wrong_provenance_prefix = (
            is_finite_graph_model and uses_aq1_subsequence_prefix and not uses_finite_graph_ground_prefix)
        per[cid] = {
            'state_provenance': sp, 'model_id': model_id, 'is_finite_graph_model': is_finite_graph_model,
            'matches_extension_1_prefix': matches_ext1,
            'looks_like_extension_2_multi_family_shape': looks_like_ext2_multi_family,
            'matches_either_extension': matches_ext1 or looks_like_ext2_multi_family,
            'finite_graph_model_wrong_provenance_prefix': finite_graph_model_wrong_provenance_prefix,
        }

    findings = ['advisor/plan.json second preregistration_vocabulary_extensions entry (state_provenance clause) '
               'found: %r' % (ext2 is not None)]
    for cid, v in per.items():
        if v['matches_extension_1_prefix']:
            findings.append('%s: state_provenance matches the original 3-prefix vocabulary (structural check).'
                            % cid)
        elif v['looks_like_extension_2_multi_family_shape']:
            findings.append('%s: state_provenance matches neither closed prefix directly but is the extension-2 '
                            '"names more than one family at once" shape (%r) -- the known, recorded AY2 case.'
                            % (cid, v['state_provenance']))
        else:
            findings.append('DEFECT: %s: state_provenance=%r matches NEITHER the original 3-prefix vocabulary NOR '
                            'the extension-2 multi-family shape.' % (cid, v['state_provenance']))
        if v['finite_graph_model_wrong_provenance_prefix']:
            findings.append(
                'DEFECT (semantic, not caught by the structural prefix check above): %s: state_provenance=%r '
                'passes the structural prefix check trivially (it literally starts with '
                '"AQ1_centered_whole_star_subsequence") but this is the unmodified boilerplate used by every '
                'AQ1-subsequence contract in the round, while %s\'s own model_id=%r is a finite-graph model '
                '(starts with "FG("). Every sibling field in the same contract WAS correctly adapted for the '
                'finite-graph model (selected_triple_alpha_units="n/a (finite graph)", observable.reference_route='
                '"own_finite_graph") -- state_provenance alone reads as an unedited copy of the AQ-subsequential-'
                'limit template text. There is no subsequential limit at all in a finite, closed graph model (the '
                'Round11 two-plaquette graph: 6 vertices, 7 links, 6 Gauss constraints) -- nothing "converges" as '
                'N grows, so "via finite_volume uniform bound" is not even meaningful for this model. The closed '
                'vocabulary already names a finite_graph_ground prefix for exactly this case '
                '(ALLOWED_STATE_PROVENANCE_PREFIXES includes it, and AZ2 is the only finite-graph contract in the '
                'round) and AZ2 does not use it.' % (cid, v['state_provenance'], cid, v['model_id']))
    passed = all(v['matches_either_extension'] and not v['finite_graph_model_wrong_provenance_prefix']
                for v in per.values())
    return {'id': 'state_provenance_check', 'plan_extension_2_present': ext2 is not None, 'per_contract': per,
            'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 7. "uniqueness of the AQ state" phrase in claim_exclusions.
# ---------------------------------------------------------------------------
FROZEN_UNAMENDED_IDS = ('AV1', 'AV2', 'AW1', 'AW2', 'AX1', 'AX2', 'AY1', 'AY2')
LATER_IDS = ('AZ1', 'AZ2')
OLD_PHRASE = 'uniqueness of the AQ state'
NEW_PHRASE = 'uniqueness of any subsequential limit'


def aq_state_phrase_check():
    per = {}
    for cid in K.ALL_TEN_IDS:
        contract = K.load_json(K.TEN_CONTRACT_PATHS[cid])
        ce = contract.get('preregistration', {}).get('claim_exclusions', []) or []
        has_old = any(OLD_PHRASE in e for e in ce)
        has_new = any(NEW_PHRASE in e for e in ce)
        if cid in FROZEN_UNAMENDED_IDS:
            expected_ok = has_old and not has_new
        else:
            expected_ok = has_new and not has_old
        per[cid] = {'claim_exclusions': ce, 'has_old_phrase': has_old, 'has_new_phrase': has_new,
                    'expected_shape': ('old (grandfathered)' if cid in FROZEN_UNAMENDED_IDS else 'new'),
                    'passed': expected_ok}
    passed = all(v['passed'] for v in per.values())
    findings = []
    for cid, v in per.items():
        tag = 'OK' if v['passed'] else 'DEFECT'
        findings.append('%s: %s (expected %s) -- has_old=%r has_new=%r.'
                        % (tag, cid, v['expected_shape'], v['has_old_phrase'], v['has_new_phrase']))
    return {'id': 'aq_state_phrase_check', 'per_contract': per, 'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 8. sub_labels_allowed vs. labels actually used.
# ---------------------------------------------------------------------------
def sub_labels_used_vs_allowed_check():
    per = {}
    for cid in K.ALL_TEN_IDS:
        contract = K.load_json(K.TEN_CONTRACT_PATHS[cid])
        pre = contract.get('preregistration', {})
        allowed = pre.get('sub_labels_allowed')
        allowed_ok = allowed == K.SUB_LABELS_ALLOWED

        used = set()
        producer_paths = [K.TEN_FORWARD_RESULTS_PATHS[cid]]
        if cid in K.TEN_REVERSE_RESULTS_PATHS:
            producer_paths.append(K.TEN_REVERSE_RESULTS_PATHS[cid])
        for p in producer_paths:
            if not p.exists():
                continue
            data = K.load_json(p)
            for _, key, value in K.walk_json_items(data):
                if key == 'sub_label' and isinstance(value, str):
                    used.add(value)
                if key in ('sub_labels', 'secondary_sub_labels') and isinstance(value, list):
                    used.update(v for v in value if isinstance(v, str))
        gate_path = K.TEN_GATE_PATHS[cid]
        if gate_path.exists():
            gate = K.load_json(gate_path)
            if isinstance(gate.get('sub_label'), str):
                used.add(gate['sub_label'])
            if isinstance(gate.get('secondary_sub_labels'), list):
                used.update(v for v in gate['secondary_sub_labels'] if isinstance(v, str))

        not_covered = sorted(used - set(allowed or []))
        per[cid] = {'sub_labels_allowed': allowed, 'sub_labels_allowed_is_closed_vocabulary': allowed_ok,
                    'labels_actually_used': sorted(used), 'labels_used_not_in_allowed_vocabulary': not_covered,
                    'passed': allowed_ok and not not_covered}
    passed = all(v['passed'] for v in per.values())
    findings = ['%s: sub_labels_allowed_is_closed_vocabulary=%r; labels_actually_used=%r; not_covered=%r%s'
               % (cid, v['sub_labels_allowed_is_closed_vocabulary'], v['labels_actually_used'],
                  v['labels_used_not_in_allowed_vocabulary'], '' if v['passed'] else ' DEFECT')
               for cid, v in per.items()]
    return {'id': 'sub_labels_used_vs_allowed_check', 'per_contract': per, 'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 9. Certification-loop target note for AZ1/AZ2.
# ---------------------------------------------------------------------------
FEASIBILITY_MARKERS = ('feasibility', 'format check')


def certification_target_note_check():
    per = {}
    for cid in ('AZ1', 'AZ2'):
        contract = K.load_json(K.TEN_CONTRACT_PATHS[cid])
        target = contract.get('preregistration', {}).get('target', {}) or {}
        note = target.get('note', '') or ''
        has_marker = any(m in note.lower() for m in FEASIBILITY_MARKERS)
        has_not_blind = 'not a blind discovery threshold' in note.lower()
        per[cid] = {'target_note': note, 'has_feasibility_or_format_check_marker': has_marker,
                    'states_not_a_blind_discovery_threshold': has_not_blind,
                    'passed': has_marker and has_not_blind}
    ay2 = K.load_json(K.TEN_CONTRACT_PATHS['AY2'])
    ay2_note = ay2.get('preregistration', {}).get('target', {}).get('note', '') or ''
    ay2_has_marker = any(m in ay2_note.lower() for m in FEASIBILITY_MARKERS)

    passed = all(v['passed'] for v in per.values())
    findings = []
    for cid, v in per.items():
        tag = '' if v['passed'] else 'DEFECT: '
        findings.append('%s%s: target.note=%r -- feasibility/format-check marker present=%r, "not a blind '
                        'discovery threshold" present=%r.' % (tag, cid, v['target_note'],
                                                               v['has_feasibility_or_format_check_marker'],
                                                               v['states_not_a_blind_discovery_threshold']))
    findings.append(
        'AY2 (recorded accepted exception, plan.json target_of_a_certification_loop clause): target.note=%r -- '
        'feasibility/format-check marker present=%r (expected False: plan.json names AY2 itself as the exception '
        'to this rule, contract unamended, not a defect).' % (ay2_note, ay2_has_marker))
    return {'id': 'certification_target_note_check', 'per_contract': per, 'ay2_note': ay2_note,
            'ay2_has_marker': ay2_has_marker, 'passed': passed, 'findings': findings}


def run():
    checks = [
        frozen_status_check(), controls_mirror_check(), gate_fields_required_check(),
        mandatory_sentence_template_check(), selected_after_check(), state_provenance_check(),
        aq_state_phrase_check(), sub_labels_used_vs_allowed_check(), certification_target_note_check(),
    ]
    overall_pass = all(c['passed'] for c in checks)
    return {
        'id': 'final_preregistration_audit',
        'role': 'the final pre-registration integration audit over all ten Round32 contracts (panel-update-4.md '
                'item 7, Jung update-4.md section 4, calling task item 1); zero research loops; audits only, '
                'never admission evidence',
        'contracts_scope': list(K.ALL_TEN_IDS),
        'checks': {c['id']: c for c in checks},
        'passed': overall_pass,
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'final_preregistration_audit', result)
    print('final_preregistration_audit: %s' % ('PASS (no defects)' if result['passed'] else 'FAIL (defects found, see findings -- expected for this audit)'))
    for check_id, c in result['checks'].items():
        print('  %s: %s' % (check_id, 'PASS' if c['passed'] else 'FAIL'))
        for f in c['findings']:
            print('    -', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
