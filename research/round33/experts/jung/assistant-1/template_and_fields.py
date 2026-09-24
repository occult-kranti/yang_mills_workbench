#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 sub-round 1, assistant-1 script 2 of 3: template-span,
gate-field and closed-vocabulary audit named in
`research/round33/experts/jung/loop2-response.md` section 3 item (part of the
calling task's item 2, which restates and extends loop2-response.md's own R6/R7/
R9/R10 discussion in section 2).

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not import
`forward/*/check.py`, `reverse/*/check.py`, or any other producer/skeptic module.

Four sub-checks, both for BA1 and BA2:

  1. `mandatory_template_span_check` (rule R7) -- the contract's
     `preregistration.mandatory_sentence_template` appears, verbatim after
     whitespace normalization, as ONE unbroken span inside the gate's own
     `accepted` text (the field `record_gate.py` actually enforces R7 against;
     `decision` is checked too, as `record_gate.py` accepts either).

  2. `gate_fields_match_check` -- the gate's `gate_fields` dict has EXACTLY the
     key set of the contract's `preregistration.gate_fields_required`, and every
     value is not just present but equal to the frozen contract value (the
     "reviewed values": also cross-checked against the skeptic's own
     `gate_fields` in `skeptic/<loop>.json`, since the gate is supposed to copy
     the skeptic's reviewed record, not invent its own).

  3. `true_field_scope_check` -- for every `<stem>_claimed` key the contract's
     `gate_fields_required` sets to `true` AND for which the SAME
     `gate_fields_required` dict also declares a `<stem>_scope` sibling key
     (the contract's own way of saying "this claim needs a scope string"),
     confirms the gate's `gate_fields` carries that `<stem>_scope` key as a
     non-empty string equal to the frozen contract value. (`whole_sequence_scope`
     for BA2, `coefficient_cauchy_scope` for BA1 -- the two the calling task's
     own example and BA1's contract respectively name.)

  4. `closed_vocabulary_check` (rule R10) -- the contract's own
     `preregistration.tier_names_allowed` and `sub_labels_allowed` are subsets of
     `plan.json#/vocabulary/tier_names_allowed` and `sub_labels_allowed`
     (already enforced at freeze time by `tools/freeze_contract.py`; re-confirmed
     here as an independent audit, not trusted from that tool's own exit code);
     the gate's `sub_label` and every `secondary_sub_labels` entry are themselves
     members of `plan.json`'s closed sub-label vocabulary (freeze_contract.py
     only checks the CONTRACT's declared allow-list against plan.json, not that
     the gate's actually-used label is itself in that allow-list -- an
     extension, in the same spirit as Round32 assistant-5's practice of
     widening an existing check's coverage); and every `"tier"` value either
     producer actually exports in its own `output/results.json` is a member of
     `plan.json`'s closed tier vocabulary (a value the freezer never looks at,
     since it only inspects the contract's declared `tier_names_allowed` list,
     not what a producer later actually writes there).

Usage: python3 -B template_and_fields.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common1 as K  # noqa: E402

sys.path.insert(0, str(K.TOOLS))
import phrase_scan as ps  # noqa: E402


# ---------------------------------------------------------------------------
# 1. Rule R7: mandatory_sentence_template as one unbroken span.
# ---------------------------------------------------------------------------
def mandatory_template_span_check():
    per = {}
    for loop in K.LOOPS:
        L = loop.upper()
        contract = K.load_contract(loop)
        gate = K.load_gate(loop)
        template = contract['preregistration']['mandatory_sentence_template']
        accepted = gate.get('accepted', '') or ''
        decision = gate.get('decision', '') or ''
        norm_template = ps.normalize(template)
        in_accepted = norm_template in ps.normalize(accepted)
        in_decision = norm_template in ps.normalize(decision)
        per[L] = {
            'template_len': len(template), 'in_accepted': in_accepted, 'in_decision': in_decision,
            'passed': in_accepted or in_decision,
        }
    passed = all(v['passed'] for v in per.values())
    findings = ['%s: mandatory_sentence_template (%d chars) present as one unbroken normalized span in gate.accepted=%r, '
               'gate.decision=%r -- %s' % (loop, v['template_len'], v['in_accepted'], v['in_decision'],
                                           'PASS' if v['passed'] else 'DEFECT')
               for loop, v in per.items()]
    return {'id': 'mandatory_template_span_check', 'per_loop': per, 'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 2. gate.gate_fields == contract.preregistration.gate_fields_required, with
#    equal (not just present) values, cross-checked against the skeptic's own
#    reviewed gate_fields.
# ---------------------------------------------------------------------------
def gate_fields_match_check():
    per = {}
    for loop in K.LOOPS:
        L = loop.upper()
        contract = K.load_contract(loop)
        gate = K.load_gate(loop)
        skeptic = K.load_json(K.SKEPTIC_JSON_PATHS[loop])
        gfr = contract['preregistration']['gate_fields_required']
        gf = gate.get('gate_fields', {})
        sgf = skeptic.get('gate_fields', {})

        keys_match = set(gfr) == set(gf)
        only_in_contract = sorted(set(gfr) - set(gf))
        only_in_gate = sorted(set(gf) - set(gfr))
        value_mismatches = {k: {'contract': gfr[k], 'gate': gf.get(k, '<absent>')}
                            for k in gfr if k in gf and gf[k] != gfr[k]}
        skeptic_keys_match = set(gfr) == set(sgf)
        skeptic_value_mismatches = {k: {'contract': gfr[k], 'skeptic': sgf.get(k, '<absent>')}
                                    for k in gfr if k in sgf and sgf[k] != gfr[k]}
        gate_vs_skeptic_mismatches = {k: {'gate': gf.get(k, '<absent>'), 'skeptic': sgf.get(k, '<absent>')}
                                      for k in (set(gf) | set(sgf)) if gf.get(k, '<absent>') != sgf.get(k, '<absent>')}

        per[L] = {
            'contract_keys': sorted(gfr), 'gate_keys': sorted(gf), 'keys_match': keys_match,
            'only_in_contract': only_in_contract, 'only_in_gate': only_in_gate,
            'value_mismatches_contract_vs_gate': value_mismatches,
            'skeptic_keys_match_contract': skeptic_keys_match,
            'value_mismatches_contract_vs_skeptic': skeptic_value_mismatches,
            'value_mismatches_gate_vs_skeptic': gate_vs_skeptic_mismatches,
            'passed': keys_match and not value_mismatches and not gate_vs_skeptic_mismatches,
        }
    passed = all(v['passed'] for v in per.values())
    findings = []
    for loop, v in per.items():
        findings.append('%s: gate.gate_fields keys == contract.gate_fields_required keys: %r (%d keys); values equal '
                        'for every key: %r; gate.gate_fields equals skeptic.gate_fields (the reviewed record the '
                        'gate is meant to copy): %r.'
                        % (loop, v['keys_match'], len(v['contract_keys']), not v['value_mismatches_contract_vs_gate'],
                           not v['value_mismatches_gate_vs_skeptic']))
        if not v['passed']:
            if v['only_in_contract']:
                findings.append('  DEFECT: %s: required but missing from gate.gate_fields: %r' % (loop, v['only_in_contract']))
            if v['only_in_gate']:
                findings.append('  DEFECT: %s: in gate.gate_fields but not required by the contract: %r' % (loop, v['only_in_gate']))
            if v['value_mismatches_contract_vs_gate']:
                findings.append('  DEFECT: %s: contract vs gate value mismatches: %r' % (loop, v['value_mismatches_contract_vs_gate']))
            if v['value_mismatches_gate_vs_skeptic']:
                findings.append('  DEFECT: %s: gate vs skeptic value mismatches: %r' % (loop, v['value_mismatches_gate_vs_skeptic']))
    return {'id': 'gate_fields_match_check', 'per_loop': per, 'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 3. Every true `<stem>_claimed` field that the contract itself pairs with a
#    `<stem>_scope` sibling key carries a non-empty scope string in the gate.
# ---------------------------------------------------------------------------
def true_field_scope_check():
    per = {}
    for loop in K.LOOPS:
        L = loop.upper()
        contract = K.load_contract(loop)
        gate = K.load_gate(loop)
        gfr = contract['preregistration']['gate_fields_required']
        gf = gate.get('gate_fields', {})
        rows = {}
        for key, expected in gfr.items():
            if not key.endswith('_claimed') or expected is not True:
                continue
            stem = key[:-len('_claimed')]
            scope_key = stem + '_scope'
            requires_scope = scope_key in gfr
            gate_scope_value = gf.get(scope_key, '<absent>')
            ok = (not requires_scope) or (isinstance(gate_scope_value, str) and gate_scope_value.strip() != ''
                                          and gate_scope_value == gfr.get(scope_key))
            rows[key] = {
                'contract_requires_true': True, 'declares_scope_sibling_in_contract': requires_scope,
                'scope_key': scope_key if requires_scope else None,
                'gate_scope_value': gate_scope_value if requires_scope else None, 'passed': ok,
            }
        per[L] = {'rows': rows, 'passed': all(r['passed'] for r in rows.values())}
    passed = all(v['passed'] for v in per.values())
    findings = []
    for loop, v in per.items():
        for key, r in v['rows'].items():
            if not r['declares_scope_sibling_in_contract']:
                findings.append('%s: %s=true has no <stem>_scope sibling declared in this contract\'s own '
                                'gate_fields_required (not required by plan.json for this field -- see README) -- '
                                'skipped, not a defect.' % (loop, key))
            else:
                tag = 'PASS' if r['passed'] else 'DEFECT'
                findings.append('%s: %s=true, contract declares sibling %s -- gate.gate_fields.%s=%r -- %s'
                                % (loop, key, r['scope_key'], r['scope_key'], r['gate_scope_value'], tag))
    return {'id': 'true_field_scope_check', 'per_loop': per, 'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 4. Rule R10: sub-labels and tier names in the closed plan.json vocabulary.
# ---------------------------------------------------------------------------
def closed_vocabulary_check():
    plan = K.load_plan()
    tier_allowed = set(plan['vocabulary']['tier_names_allowed'])
    sub_allowed = set(plan['vocabulary']['sub_labels_allowed'])

    per = {}
    for loop in K.LOOPS:
        L = loop.upper()
        contract = K.load_contract(loop)
        gate = K.load_gate(loop)
        pre = contract['preregistration']

        contract_tiers = set(pre['tier_names_allowed'])
        contract_subs = set(pre['sub_labels_allowed'])
        contract_tiers_ok = contract_tiers <= tier_allowed
        contract_subs_ok = contract_subs <= sub_allowed

        gate_sub_label = gate.get('sub_label')
        gate_secondary = gate.get('secondary_sub_labels', [])
        gate_sub_label_ok = gate_sub_label in sub_allowed
        gate_secondary_ok = all(s in sub_allowed for s in gate_secondary)

        tiers_used = set()
        tier_locations = []
        for side, path in (('forward', K.FORWARD_RESULTS_PATHS[loop]), ('reverse', K.REVERSE_RESULTS_PATHS[loop])):
            data = K.load_json(path)
            for json_path, key, value in K.walk_json_items(data):
                if key == 'tier' and isinstance(value, str):
                    tiers_used.add(value)
                    tier_locations.append({'side': side, 'json_path': json_path, 'value': value})
        tiers_ok_vs_plan = tiers_used <= tier_allowed
        tiers_ok_vs_contract = tiers_used <= contract_tiers

        per[L] = {
            'contract_tier_names_allowed': sorted(contract_tiers), 'contract_tiers_subset_of_plan': contract_tiers_ok,
            'contract_sub_labels_allowed': sorted(contract_subs), 'contract_subs_subset_of_plan': contract_subs_ok,
            'gate_sub_label': gate_sub_label, 'gate_sub_label_in_plan_vocabulary': gate_sub_label_ok,
            'gate_secondary_sub_labels': gate_secondary, 'gate_secondary_in_plan_vocabulary': gate_secondary_ok,
            'tier_values_exported_by_producers': sorted(tiers_used), 'n_tier_export_locations': len(tier_locations),
            'tiers_subset_of_plan_vocabulary': tiers_ok_vs_plan, 'tiers_subset_of_contract_own_list': tiers_ok_vs_contract,
            'passed': (contract_tiers_ok and contract_subs_ok and gate_sub_label_ok and gate_secondary_ok
                      and tiers_ok_vs_plan and tiers_ok_vs_contract),
        }
    passed = all(v['passed'] for v in per.values())
    findings = [
        'plan.json#/vocabulary/tier_names_allowed has %d entries; sub_labels_allowed has %d entries.'
        % (len(tier_allowed), len(sub_allowed)),
    ]
    for loop, v in per.items():
        findings.append(
            '%s: contract tier_names_allowed %r subset of plan=%r; contract sub_labels_allowed %r subset of plan=%r; '
            'gate.sub_label=%r in plan vocabulary=%r; gate.secondary_sub_labels=%r all in plan vocabulary=%r; '
            'producer-exported tier values %r (from %d export sites) subset of plan=%r, subset of this contract\'s '
            'own tier_names_allowed=%r.' % (
                loop, v['contract_tier_names_allowed'], v['contract_tiers_subset_of_plan'],
                v['contract_sub_labels_allowed'], v['contract_subs_subset_of_plan'], v['gate_sub_label'],
                v['gate_sub_label_in_plan_vocabulary'], v['gate_secondary_sub_labels'],
                v['gate_secondary_in_plan_vocabulary'], v['tier_values_exported_by_producers'],
                v['n_tier_export_locations'], v['tiers_subset_of_plan_vocabulary'], v['tiers_subset_of_contract_own_list']))
        if not v['passed']:
            findings.append('  DEFECT: %s fails the closed-vocabulary check (see fields above).' % loop)
    findings.append('Note (not part of the required check, recorded for completeness): a free-text "route" key '
                    'also appears throughout both loops\' producer output/results.json, but it is NOT the same '
                    'closed 6-name route vocabulary plan.json#/vocabulary/tier_label_rule names (weighted_norm, '
                    'analytic_disc, polymer_kp, iterated_split, duhamel_inner_f1, duhamel_inner_f2) -- most "route" '
                    'values found are free descriptive prose (e.g. "forward Duhamel over the extra F2 faces"), not '
                    'single closed-vocabulary tokens. The calling task asks only about sub-labels and tier names, so '
                    'this is not scored as a defect, but the advisor may want a future R9/R10-style check for "route" '
                    'specifically if it is meant to be closed-vocabulary too.')
    return {'id': 'closed_vocabulary_check', 'per_loop': per, 'passed': passed, 'findings': findings}


def run():
    checks = [mandatory_template_span_check(), gate_fields_match_check(), true_field_scope_check(),
             closed_vocabulary_check()]
    return {
        'id': 'template_and_fields',
        'role': 'Jung/Pauli lens, Round33 sub-round 1, assistant-1: template-span (R7), gate-field-equality, '
                'true-field-scope and closed-vocabulary (R10) audit, calling task item 2; zero research loops; '
                'audits only, never admission evidence',
        'checks': {c['id']: c for c in checks},
        'passed': all(c['passed'] for c in checks),
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'template_and_fields', result)
    print('template_and_fields: %s' % ('PASS (no defects)' if result['passed'] else 'FAIL (see findings)'))
    for check_id, c in result['checks'].items():
        print('  %s: %s' % (check_id, 'PASS' if c['passed'] else 'FAIL'))
        for f in c['findings']:
            print('    -', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
