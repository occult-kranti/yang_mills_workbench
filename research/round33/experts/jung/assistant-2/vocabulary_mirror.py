#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 sub-round 2, assistant-2 script 3 of 4: the closed-
vocabulary and tier/route-labelling audit (calling task item 3).

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not import
`forward/*/check.py`, `reverse/*/check.py`, or any other producer/skeptic module.

Four sub-checks:

  1. `closed_vocabulary_membership` -- every `tier`, `route`, `assembly`,
     `sub_label`/`label`/`secondary_sub_labels` and `dynamics_level` value used
     anywhere in the four `output/results.json` files must be a member of
     `plan.json#/vocabulary`'s closed lists (`tier_names_allowed` covers both
     tier AND route tokens in this sub-round's contracts -- BB1's and BB2's own
     `preregistration.tier_names_allowed` mix tier names with route names, e.g.
     `polymer_kp`/`iterated_split`/`duhamel_inner_f1` sit in the same list as
     `exact_first_order`/`crude_majorant`; `plan.json`'s own `tier_names_allowed`
     is the same kind of combined list) and of each contract's own, narrower,
     declared `tier_names_allowed`/`sub_labels_allowed`; `assembly` values must
     be in `plan.json#/vocabulary/assembly_values`; `dynamics_level` values must
     be in the two-value set `plan.json#/vocabulary/gate_fields/dynamics_level`
     names in its own descriptive text (`algebraic_heisenberg_compact_window`,
     `correlation_functions_compact_window`).

  2. `tier_label_rule_bb1` -- no BB1 constant's own `route` field is a BA1-only
     route (`analytic_disc` or `weighted_norm`); every BB1 `route` value is one
     of BB1's own two routes (`polymer_kp` for forward, `iterated_split` for
     reverse). A BA1 route may legitimately appear inside a `ba1_input`
     descriptive STRING (naming the BA1 input, exactly as the contract's
     `tier_label_rule` requires -- "the BA1 route of the input is recorded as
     the input, never as the BB1 route"); only the `route` JSON field itself is
     checked here.

  3. `bb2_state_constant_assembly_and_hypothesis_source` -- every BB2 state
     constant (a dict carrying `"tier": "exact_first_order"` or `"crude_
     majorant"`) carries sibling `assembly` (`nested_telescoping` or
     `union_comparison`) and a hypothesis-source marker (`hypothesis_source:
     "bb1_frozen_targets"` as a sibling key, or, for the top-level hypotheses
     block, a `source: "bb1_frozen_targets"` sibling), per the contract's own
     `tier_label_rule` ("every state constant carries exactly one tier ..., the
     assembly ... and the hypothesis source bb1_frozen_targets"). BB2 dynamics
     constants (tier `polynomial_lieb_robinson`) are excluded from this
     requirement (the same tier_label_rule instead requires a BA2 `route` for
     those, checked as part of sub-check 1's route membership).

  4. `sub_label_agreement_note` -- records, without judging, which sub_label
     each producer of each loop actually used (BB1 forward and reverse are free
     to pick different members of the same allowed list; this only becomes a
     violation if a value falls outside the allowed set, which sub-check 1
     already catches) -- a non-blocking cross-producer transparency note in the
     spirit of the calling task's "list violations" (a same-loop sub_label
     disagreement is recorded here, not scored as a defect, since the contract
     does not require the two producers to pick the same allowed label).

Usage: python3 -B vocabulary_mirror.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common2 as K  # noqa: E402

# BA1's own two routes (Round33 sub-round 1); never legitimate as a BB1 "route"
# JSON field value (tier_label_rule: "the BA1 route of the input is recorded as
# the input, never as the BB1 route").
BA1_ONLY_ROUTES = {'analytic_disc', 'weighted_norm'}
BB1_OWN_ROUTES = {'polymer_kp', 'iterated_split'}

# Parsed from plan.json#/vocabulary/gate_fields/dynamics_level's own descriptive
# text ("values: algebraic_heisenberg_compact_window (BA2), correlation_
# functions_compact_window (BB2)") rather than hardcoded blind, so a future edit
# to that text is picked up by the parser below, not silently missed by a stale
# literal copy.
DYNAMICS_LEVEL_TOKEN_RE = re.compile(r'([a-z][a-z0-9_]*_compact_window)')

STATE_TIERS = {'exact_first_order', 'crude_majorant'}
DYNAMICS_TIER = 'polynomial_lieb_robinson'


def dynamics_level_allowed_from_plan(plan):
    text = plan['vocabulary']['gate_fields'].get('dynamics_level', '')
    return set(DYNAMICS_LEVEL_TOKEN_RE.findall(text))


# ---------------------------------------------------------------------------
# 1. Closed-vocabulary membership for tier / route / assembly / sub_label /
#    dynamics_level values actually used in the four results.json files.
# ---------------------------------------------------------------------------
def closed_vocabulary_membership():
    plan = K.load_plan()
    tier_allowed_plan = set(plan['vocabulary']['tier_names_allowed'])
    sub_allowed_plan = set(plan['vocabulary']['sub_labels_allowed'])
    assembly_allowed = set(plan['vocabulary'].get('assembly_values', []))
    dynamics_allowed = dynamics_level_allowed_from_plan(plan)

    per_loop = {}
    violations = []
    for loop in K.LOOPS:
        L = loop.upper()
        contract = K.load_contract(loop)
        pre = contract['preregistration']
        contract_tiers = set(pre.get('tier_names_allowed', []))
        contract_subs = set(pre.get('sub_labels_allowed', []))
        contract_tiers_ok = contract_tiers <= tier_allowed_plan
        contract_subs_ok = contract_subs <= sub_allowed_plan

        used = {'tier': set(), 'route': set(), 'assembly': set(), 'sub_label': set(), 'dynamics_level': set()}
        locations = {k: [] for k in used}
        for side, path in (('forward', K.FORWARD_RESULTS_PATHS[loop]), ('reverse', K.REVERSE_RESULTS_PATHS[loop])):
            data = K.load_json(path)
            for json_path, key, value in K.walk_json_items(data):
                if key in ('tier',) and isinstance(value, str):
                    used['tier'].add(value); locations['tier'].append((side, json_path, value))
                elif key in ('route',) and isinstance(value, str):
                    used['route'].add(value); locations['route'].append((side, json_path, value))
                elif key in ('assembly',) and isinstance(value, str):
                    used['assembly'].add(value); locations['assembly'].append((side, json_path, value))
                elif key in ('dynamics_level',) and isinstance(value, str):
                    used['dynamics_level'].add(value); locations['dynamics_level'].append((side, json_path, value))
            # sub_label is a per-loop, per-producer classification, exported ONLY at the document's own top level
            # as "label" (plus "secondary_sub_labels"); the bare key "label" is heavily overloaded elsewhere in
            # these results.json files (e.g. "conditional_on_bb1_targets", "labelled secondary pair", "labelled
            # only" -- free descriptive tags on unrelated dicts, not sub_labels), so only the top-level fields are
            # read here, not every "label" occurrence anywhere in the document.
            top_label = data.get('label')
            if isinstance(top_label, str):
                used['sub_label'].add(top_label); locations['sub_label'].append((side, 'label', top_label))
            for v in data.get('secondary_sub_labels', []) or []:
                if isinstance(v, str):
                    used['sub_label'].add(v); locations['sub_label'].append((side, 'secondary_sub_labels', v))

        # kind -> (its checked values, the location-keys to search for a matching value)
        not_in_plan = {
            'tier_or_route_(tier_names_allowed)': (sorted((used['tier'] | used['route']) - tier_allowed_plan), ('tier', 'route')),
            'sub_label': (sorted(used['sub_label'] - sub_allowed_plan), ('sub_label',)),
            'assembly': (sorted(used['assembly'] - assembly_allowed) if assembly_allowed else sorted(used['assembly']), ('assembly',)),
            'dynamics_level': (sorted(used['dynamics_level'] - dynamics_allowed) if dynamics_allowed else sorted(used['dynamics_level']), ('dynamics_level',)),
        }
        not_in_contract_tier_list = sorted((used['tier'] | used['route']) - contract_tiers)
        not_in_contract_sub_list = sorted(used['sub_label'] - contract_subs)

        loop_violations = []
        for kind, (vals, loc_keys) in not_in_plan.items():
            for v in vals:
                locs = [l for lk in loc_keys for l in locations[lk] if l[2] == v]
                loop_violations.append({'loop': L, 'kind': kind, 'value': v, 'not_in_plan_vocabulary': True, 'locations': locs})
        violations.extend(loop_violations)
        not_in_plan = {k: v[0] for k, v in not_in_plan.items()}

        per_loop[L] = {
            'contract_tiers_allowed': sorted(contract_tiers), 'contract_tiers_subset_of_plan': contract_tiers_ok,
            'contract_subs_allowed': sorted(contract_subs), 'contract_subs_subset_of_plan': contract_subs_ok,
            'tier_values_used': sorted(used['tier']), 'route_values_used': sorted(used['route']),
            'assembly_values_used': sorted(used['assembly']), 'sub_label_values_used': sorted(used['sub_label']),
            'dynamics_level_values_used': sorted(used['dynamics_level']),
            'not_in_plan_vocabulary': not_in_plan,
            'tier_or_route_not_in_this_contract_own_list': not_in_contract_tier_list,
            'sub_label_not_in_this_contract_own_list': not_in_contract_sub_list,
            'passed': (contract_tiers_ok and contract_subs_ok and not any(not_in_plan.values())
                      and not not_in_contract_tier_list and not not_in_contract_sub_list),
        }

    passed = all(v['passed'] for v in per_loop.values())
    findings = [
        'plan.json#/vocabulary/tier_names_allowed has %d entries (covers both tier and route tokens for this '
        'sub-round\'s contracts); sub_labels_allowed has %d entries; assembly_values has %d entries %r; '
        'dynamics_level closed set parsed from plan.json\'s own descriptive text: %r.'
        % (len(tier_allowed_plan), len(sub_allowed_plan), len(assembly_allowed), sorted(assembly_allowed), sorted(dynamics_allowed)),
    ]
    for loop, v in per_loop.items():
        findings.append(
            '%s: tier values used %r, route values used %r (both checked against the single combined '
            'tier_names_allowed vocabulary); assembly values used %r; sub_label values used %r; dynamics_level '
            'values used %r.' % (loop, v['tier_values_used'], v['route_values_used'], v['assembly_values_used'],
                                 v['sub_label_values_used'], v['dynamics_level_values_used']))
        if not v['passed']:
            findings.append('  DEFECT: %s closed-vocabulary violations: %r; not in this contract\'s own tier list: '
                            '%r; not in this contract\'s own sub_label list: %r'
                            % (loop, {k: vv for k, vv in v['not_in_plan_vocabulary'].items() if vv},
                               v['tier_or_route_not_in_this_contract_own_list'], v['sub_label_not_in_this_contract_own_list']))
    if violations:
        findings.append('Itemized violations (value used, not in plan.json\'s closed vocabulary for its kind):')
        for viol in violations:
            findings.append('  DEFECT: %s %s=%r used at %r' % (viol['loop'], viol['kind'], viol['value'], viol['locations']))
    else:
        findings.append('0 closed-vocabulary violations for tier, route, assembly or sub_label across both loops.')

    return {
        'id': 'closed_vocabulary_membership', 'per_loop': per_loop, 'violations': violations,
        'passed': passed, 'findings': findings,
    }


# ---------------------------------------------------------------------------
# 2. tier_label_rule: no BB1 constant carries a BA1 route as its own route.
# ---------------------------------------------------------------------------
def tier_label_rule_bb1():
    loop = 'bb1'
    per_side = {}
    violations = []
    for side, path in (('forward', K.FORWARD_RESULTS_PATHS[loop]), ('reverse', K.REVERSE_RESULTS_PATHS[loop])):
        data = K.load_json(path)
        routes_seen = set()
        rows = []
        for json_path, key, value in K.walk_json_items(data):
            if key == 'route' and isinstance(value, str):
                routes_seen.add(value)
                rows.append({'json_path': json_path, 'route': value})
                if value in BA1_ONLY_ROUTES:
                    violations.append({'side': side, 'json_path': json_path, 'route': value,
                                       'reason': 'a BA1-only route used as a BB1 route JSON field'})
        expected_own_route = 'polymer_kp' if side == 'forward' else 'iterated_split'
        off_route = sorted(routes_seen - {expected_own_route})
        per_side[side] = {
            'routes_used': sorted(routes_seen), 'expected_own_route': expected_own_route,
            'routes_other_than_own': off_route, 'n_route_export_sites': len(rows),
            'passed': not (routes_seen & BA1_ONLY_ROUTES) and not off_route,
        }
    passed = all(v['passed'] for v in per_side.values()) and not violations
    findings = []
    for side, v in per_side.items():
        tag = 'PASS' if v['passed'] else 'DEFECT'
        findings.append('BB1 %s: route values used %r (%d export sites), expected own route %r, any other route '
                        'used %r -- %s' % (side, v['routes_used'], v['n_route_export_sites'], v['expected_own_route'], v['routes_other_than_own'], tag))
    if violations:
        for viol in violations:
            findings.append('  DEFECT: BB1 %s at %s carries BA1-only route %r as its own route field' % (viol['side'], viol['json_path'], viol['route']))
    else:
        findings.append('0 BB1 constants carry a BA1 route (analytic_disc, weighted_norm) as their own BB1 route '
                        'field; BA1 route names appear only inside descriptive ba1_input strings (the contract\'s '
                        'own permitted use), never as the route field itself.')
    return {'id': 'tier_label_rule_bb1', 'per_side': per_side, 'violations': violations, 'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 3. Every BB2 state constant carries assembly and hypothesis_source.
# ---------------------------------------------------------------------------
def bb2_state_constant_assembly_and_hypothesis_source():
    loop = 'bb2'
    per_side = {}
    violations = []
    for side, path in (('forward', K.FORWARD_RESULTS_PATHS[loop]), ('reverse', K.REVERSE_RESULTS_PATHS[loop])):
        data = K.load_json(path)
        rows = []
        for json_path, d in K.dicts_with_key(data, 'tier'):
            tier = d.get('tier')
            if tier not in STATE_TIERS:
                continue
            has_assembly = isinstance(d.get('assembly'), str) and d.get('assembly') != ''
            has_hyp_source = (d.get('hypothesis_source') == 'bb1_frozen_targets') or (d.get('source') == 'bb1_frozen_targets')
            ok = has_assembly and has_hyp_source
            rows.append({'json_path': json_path, 'tier': tier, 'has_assembly': has_assembly,
                        'has_hypothesis_source': has_hyp_source, 'passed': ok})
            if not ok:
                violations.append({'side': side, 'json_path': json_path, 'tier': tier,
                                   'has_assembly': has_assembly, 'has_hypothesis_source': has_hyp_source})
        per_side[side] = {'n_state_constants_found': len(rows), 'rows': rows, 'passed': all(r['passed'] for r in rows)}
    passed = all(v['passed'] for v in per_side.values())
    findings = []
    for side, v in per_side.items():
        tag = 'PASS' if v['passed'] else 'DEFECT'
        findings.append('BB2 %s: %d state-tier (exact_first_order/crude_majorant) constants found; every one '
                        'carries a sibling assembly and hypothesis_source/source=bb1_frozen_targets -- %s'
                        % (side, v['n_state_constants_found'], tag))
    if violations:
        for viol in violations:
            findings.append('  DEFECT: BB2 %s at %s (tier=%s) has_assembly=%r has_hypothesis_source=%r'
                            % (viol['side'], viol['json_path'], viol['tier'], viol['has_assembly'], viol['has_hypothesis_source']))
    else:
        findings.append('0 BB2 state constants missing an assembly or hypothesis_source sibling.')
    return {'id': 'bb2_state_constant_assembly_and_hypothesis_source', 'per_side': per_side, 'violations': violations,
            'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 4. Non-blocking transparency note: which sub_label each producer picked.
# ---------------------------------------------------------------------------
def sub_label_agreement_note():
    per_loop = {}
    for loop in K.LOOPS:
        L = loop.upper()
        fwd = K.load_json(K.FORWARD_RESULTS_PATHS[loop])
        rev = K.load_json(K.REVERSE_RESULTS_PATHS[loop])
        fwd_label = fwd.get('label')
        rev_label = rev.get('label')
        per_loop[L] = {
            'forward_label': fwd_label, 'reverse_label': rev_label, 'agree': fwd_label == rev_label,
            'forward_secondary_sub_labels': fwd.get('secondary_sub_labels', []),
            'reverse_secondary_sub_labels': rev.get('secondary_sub_labels', []),
        }
    findings = []
    for loop, v in per_loop.items():
        note = 'agree' if v['agree'] else 'DIFFER (both members of the contract\'s own allowed list; not a violation by itself, recorded for transparency)'
        findings.append('%s: forward label=%r, reverse label=%r -- %s; forward secondary_sub_labels=%r, reverse '
                        'secondary_sub_labels=%r' % (loop, v['forward_label'], v['reverse_label'], note,
                                                     v['forward_secondary_sub_labels'], v['reverse_secondary_sub_labels']))
    return {'id': 'sub_label_agreement_note', 'per_loop': per_loop, 'passed': True, 'findings': findings}


def run():
    checks = [closed_vocabulary_membership(), tier_label_rule_bb1(),
              bb2_state_constant_assembly_and_hypothesis_source(), sub_label_agreement_note()]
    return {
        'id': 'vocabulary_mirror',
        'role': 'Jung/Pauli lens, Round33 sub-round 2, assistant-2: closed-vocabulary, tier_label_rule and '
                'assembly/hypothesis-source audit, calling task item 3; zero research loops; audits only, never '
                'admission evidence',
        'checks': {c['id']: c for c in checks},
        'passed': all(c['passed'] for c in checks),
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'vocabulary_mirror', result)
    print('vocabulary_mirror: %s' % ('PASS (no violations)' if result['passed'] else 'FAIL (see findings)'))
    for check_id, c in result['checks'].items():
        print('  %s: %s' % (check_id, 'PASS' if c['passed'] else 'FAIL'))
        for f in c['findings']:
            print('    -', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
