#!/usr/bin/env python3
"""Adapter mutation tests; explicit gates remain active under python -O.

Graph-only unit fixtures below bypass scientific replay intentionally to test
the planner adapter itself. They cannot produce scientific acceptance.
"""
import argparse
import copy
import json
from pathlib import Path
import tempfile
import proof_routes as p


def run(root, output):
    root = Path(root).resolve()
    frozen = {name: p.read_regular(root, name) for name in p.EXPECTED}
    accepted_ids = p.validate_ledger(frozen)
    p.specifications(frozen, accepted_ids)
    search = p.load_frozen('ym13_test_search_core', 'proof_search.py', frozen, root)
    fixture = {'status': 'passed', 'gates': sorted(p.GATES), 'reviewed_rule_ids': sorted(accepted_ids),
               'frozen_input_sha256': p.frozen_fingerprint(frozen),
               'unit_fixture_only': 'Graph-only adapter tests; not scientific acceptance.'}
    records = []

    def gate(name, passed, detail):
        if type(passed) is not bool or not passed:
            raise RuntimeError('Adapter gate failed: ' + name + ': ' + detail)
        records.append({'name': name, 'passed': True, 'detail': detail})

    def reject(name, action, exceptions=(ValueError, TypeError, KeyError)):
        try:
            action()
        except exceptions:
            gate(name, True, 'Invalid input explicitly rejected')
        else:
            gate(name, False, 'Invalid input was accepted')

    # Test every complete positive and negative route against the actual core.
    for name, goal, hypotheses, gates, expected in p.route_specs():
        library, optimization = p.make_library(frozen, fixture, goal, hypotheses, gates)
        result = search.plan(library, max_states=10000)
        gate('route_' + name, result['status'] == expected, 'Actual two-front and separate forward search')
        if expected == 'proved':
            ids = [step['rule_id'] for step in result['certified_proof']['steps']]
            checked = search.check_proof(search.load_library(library), ids)
            gate('replay_' + name, checked.passed and checked.cost == result['certified_cost'], 'Ordered proof certificate checked separately')
            gate('two_front_' + name, result.get('first_meeting_candidate', {}).get('passed') is True, 'Positive route has an actual bidirectional meeting')
        advisor_rules = json.loads(frozen['advisor/inference_rules.json'])['rules']
        retained = set(optimization['retained_rule_ids'])
        relevant_atoms = {node['id'] for node in library['nodes']}
        gate('cone_' + name, all(r['id'] in retained for r in advisor_rules if r['conclusion'] in relevant_atoms), 'No rule feeding any retained atom was discarded')

    for invalid in ('yang_mills_4d_gap', 'all_order_constraints_typo', 'moment_outer_interval', 'continuum_observables'):
        reject('reject_seed_' + invalid, lambda invalid=invalid: p.make_library(frozen, fixture, 'yang_mills_4d_gap', [invalid], []))
    reject('gate_as_hypothesis', lambda: p.make_library(frozen, fixture, 'moment_outer_interval', ['rational_exclusion_gate'], []))
    reject('all_order_as_computed_gate', lambda: p.make_library(frozen, fixture, 'hierarchy_unique', ['compact_measure'], ['all_order_constraints']))
    reject('duplicate_hypotheses', lambda: p.make_library(frozen, fixture, 'moment_outer_interval', ['compact_measure', 'compact_measure'], []))
    reject('incomplete_gate_replay', lambda: p.make_library(frozen, {**fixture, 'gates': ['path_count']}, 'moment_outer_interval', [], []))
    reject('pending_replay', lambda: p.make_library(frozen, {**fixture, 'status': 'pending'}, 'moment_outer_interval', [], []))
    reject('unknown_goal', lambda: p.make_library(frozen, fixture, 'invented_gap', [], []))

    # Preserve alternative derivations even if the first alternative is missing
    # a fact, including rules capable of deriving an already available seed.
    toy = [
        {'id': 'a', 'premises': ['p'], 'conclusion': 'g'},
        {'id': 'b', 'premises': ['q'], 'conclusion': 'g'},
        {'id': 'c', 'premises': ['r'], 'conclusion': 'q'},
        {'id': 'd', 'premises': ['s'], 'conclusion': 'unused'},
        {'id': 'e', 'premises': ['g'], 'conclusion': 'p'},
    ]
    atoms, cone = p.backward_cone(toy, 'g')
    gate('cone_alternatives_and_cycle', {x['id'] for x in cone} == {'a', 'b', 'c', 'e'} and atoms == {'p', 'q', 'r', 'g'}, 'Every alternative and a dependency cycle survive cone restriction')
    atoms, cone = p.backward_cone(toy, 'missing')
    gate('cone_unknown_terminal', atoms == {'missing'} and cone == [], 'No invented producer for an unprovided terminal')

    def mutate_json(key, mutator):
        candidate = dict(frozen)
        data = json.loads(candidate[key])
        mutator(data)
        candidate[key] = json.dumps(data).encode()
        return candidate

    reject('pending_acceptance', lambda: p.validate_ledger(mutate_json('skeptic/acceptance.json', lambda x: x.update(status='pending'))))
    reject('stale_scientific_hash', lambda: p.validate_ledger(mutate_json('skeptic/acceptance.json', lambda x: x['reviewed_source_hashes'].update({'moments/moment_bounds.py': '0' * 64}))))
    reject('missing_scientific_hash', lambda: p.validate_ledger(mutate_json('skeptic/acceptance.json', lambda x: x['reviewed_source_hashes'].pop('locality/locality.md'))))
    reject('duplicate_reviewed_rule', lambda: p.validate_ledger(mutate_json('skeptic/acceptance.json', lambda x: x['reviewed_rule_ids'].append(x['reviewed_rule_ids'][0]))))
    reject('missing_reviewed_rule', lambda: p.specifications(frozen, accepted_ids - {'M3'}))
    reject('invented_reviewed_rule', lambda: p.specifications(frozen, accepted_ids | {'MAGIC'}))
    reject('missing_rule_premise', lambda: p.specifications(mutate_json('advisor/inference_rules.json', lambda x: x['rules'][0]['premises'].append('UNDECLARED')), accepted_ids))
    reject('zero_cost_rule', lambda: p.specifications(mutate_json('advisor/inference_rules.json', lambda x: x['rules'][0].update(cost=0)), accepted_ids))
    reject('boolean_cost_rule', lambda: p.specifications(mutate_json('advisor/inference_rules.json', lambda x: x['rules'][0].update(cost=True)), accepted_ids))
    reject('unbound_evidence_rule', lambda: p.specifications(mutate_json('advisor/inference_rules.json', lambda x: x['rules'][0].update(evidence='remote-unread.md')), accepted_ids))

    # A prior passed replay must not admit different bytes, even if the same
    # rule IDs and superficially successful output metadata remain present.
    changed_rule = mutate_json('advisor/inference_rules.json', lambda x: next(r for r in x['rules'] if r['id'] == 'M8').update(premises=['compact_measure']))
    reject('post_replay_rule_change', lambda: p.make_library(changed_rule, fixture, 'hierarchy_unique', ['compact_measure'], []))
    changed_certificate = mutate_json('moments/output/certificates.json', lambda x: x['certificates'][0].update(variance_interval=['0', '0']))
    reject('post_replay_certificate_change', lambda: p.make_library(changed_certificate, fixture, 'moment_outer_interval', ['compact_measure'], ['rational_exclusion_gate']))
    changed_report = mutate_json('locality/output/results.json', lambda x: x.update(check_count=0, checks=[]))
    reject('post_replay_report_change', lambda: p.make_library(changed_report, fixture, 'bounded_local_volume_limit', [], []))
    changed_ledger = mutate_json('skeptic/acceptance.json', lambda x: x.update(status='pending'))
    reject('post_replay_acceptance_change', lambda: p.make_library(changed_ledger, fixture, 'moment_outer_interval', ['compact_measure'], []))
    reject('missing_replay_fingerprint', lambda: p.make_library(frozen, {k: v for k, v in fixture.items() if k != 'frozen_input_sha256'}, 'moment_outer_interval', ['compact_measure'], []))
    reject('changed_replay_rule_ids', lambda: p.make_library(frozen, {**fixture, 'reviewed_rule_ids': sorted(accepted_ids - {'M8'})}, 'hierarchy_unique', ['compact_measure'], []))
    # Even a manually recomputed fingerprint does not bypass current ledger
    # matching or its explicit acceptance status.
    reject('rehash_unreviewed_rule_not_accepted', lambda: p.make_library(changed_rule, {**fixture, 'frozen_input_sha256': p.frozen_fingerprint(changed_rule)}, 'hierarchy_unique', ['compact_measure'], []))
    reject('rehash_pending_acceptance_not_accepted', lambda: p.make_library(changed_ledger, {**fixture, 'frozen_input_sha256': p.frozen_fingerprint(changed_ledger)}, 'moment_outer_interval', ['compact_measure'], []))
    reject('fingerprint_missing_input', lambda: p.frozen_fingerprint({k: v for k, v in frozen.items() if k != 'response/output/results.json'}))
    reject('fingerprint_mutable_bytes', lambda: p.frozen_fingerprint({**frozen, 'advisor/advisor.md': bytearray(frozen['advisor/advisor.md'])}))

    # These mutations call the real evidence admission path. They must fail
    # before their altered output can become a proof premise.
    reject('moment_collection_missing_case', lambda: p.replay_evidence(mutate_json('moments/output/certificates.json', lambda x: x['certificates'].pop()), root))
    reject('moment_collection_duplicate_case', lambda: p.replay_evidence(mutate_json('moments/output/certificates.json', lambda x: x['certificates'].__setitem__(1, copy.deepcopy(x['certificates'][0]))), root))
    reject('moment_collection_pending', lambda: p.replay_evidence(mutate_json('moments/output/certificates.json', lambda x: x.update(status='pending')), root))
    reject('moment_changed_dual_arithmetic', lambda: p.replay_evidence(mutate_json('moments/output/certificates.json', lambda x: x['certificates'][0]['witnesses'][0].update(slope='0')), root))
    reject('moment_changed_variance', lambda: p.replay_evidence(mutate_json('moments/output/certificates.json', lambda x: x['certificates'][0].update(variance_interval=['0', '0'])), root))
    reject('locality_checks_missing', lambda: p.replay_evidence(mutate_json('locality/output/results.json', lambda x: x.update(checks=[], check_count=0)), root))
    reject('locality_csv_hash_tamper', lambda: p.replay_evidence(mutate_json('locality/output/results.json', lambda x: x['files'].update({'boundary_decay.csv': '0' * 64})), root))
    candidate = dict(frozen)
    candidate['locality/output/boundary_decay.csv'] += b'changed'
    reject('locality_csv_bytes_tamper', lambda: p.replay_evidence(candidate, root))

    base_report = {'status': 'passed', 'source_sha256': 'abc', 'check_count': 1, 'checks': [{'name': 'one', 'passed': True, 'detail': None}]}
    p.validate_report(base_report, 'abc', 'unit fixture')
    gate('check_report_valid', True, 'Minimal nonempty valid check report accepted')
    for label, mutation in [
        ('empty', {'checks': [], 'check_count': 0}),
        ('false', {'checks': [{'name': 'one', 'passed': False, 'detail': None}]}),
        ('integer_boolean', {'checks': [{'name': 'one', 'passed': 1, 'detail': None}]}),
        ('count_mismatch', {'check_count': 2}),
        ('bool_count', {'check_count': True}),
        ('stale_source', {'source_sha256': 'wrong'}),
        ('duplicate_names', {'checks': [{'name': 'one', 'passed': True, 'detail': None}] * 2, 'check_count': 2}),
    ]:
        reject('report_' + label, lambda mutation=mutation: p.validate_report({**base_report, **mutation}, 'abc', 'mutant'))
    status_report = {**base_report, 'checks': [{'name': 'one', 'status': 'passed', 'detail': None}]}
    p.validate_report(status_report, 'abc', 'response unit fixture', convention='status')
    gate('status_report_valid', True, 'Response uses its declared status schema')
    reject('boolean_schema_not_status', lambda: p.validate_report(base_report, 'abc', 'mutant', convention='status'))
    reject('status_schema_not_boolean', lambda: p.validate_report(status_report, 'abc', 'mutant'))
    reject('mixed_check_schema', lambda: p.validate_report({**status_report, 'checks': [{'name': 'one', 'status': 'passed', 'passed': True, 'detail': None}]}, 'abc', 'mutant', convention='status'))

    with tempfile.TemporaryDirectory(prefix='ym13-adapter-mutations-', dir=Path(__file__).resolve().parent) as tmp:
        tmp = Path(tmp)
        for name, data in frozen.items():
            dest = tmp / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        manifest = {'sha256': {name: p.digest(data) for name, data in frozen.items()}}
        manifest_path = tmp / 'proof_manifest.json'
        save_manifest = lambda: manifest_path.write_text(json.dumps(manifest))
        save_manifest()
        p.checked_inputs(tmp)
        gate('valid_frozen_manifest', True, 'Exact complete frozen input set accepted')
        path = tmp / 'advisor/advisor.md'
        original = path.read_bytes()
        path.write_bytes(original + b'\nchanged')
        reject('stale_frozen_bytes', lambda: p.checked_inputs(tmp))
        path.write_bytes(original)
        path.unlink()
        path.symlink_to(root / 'advisor/advisor.md')
        reject('input_symlink', lambda: p.checked_inputs(tmp))
        path.unlink()
        path.write_bytes(original)
        manifest_path.unlink()
        manifest_path.symlink_to(root / 'proof_manifest.json')
        reject('manifest_symlink', lambda: p.checked_inputs(tmp))
        manifest_path.unlink()
        save_manifest()
        bad = copy.deepcopy(manifest)
        bad['sha256']['../escape'] = '0' * 64
        manifest_path.write_text(json.dumps(bad))
        reject('manifest_extra_traversal', lambda: p.checked_inputs(tmp))
        bad = copy.deepcopy(manifest)
        bad['sha256'].pop('skeptic/acceptance.json')
        manifest_path.write_text(json.dumps(bad))
        reject('manifest_missing_acceptance', lambda: p.checked_inputs(tmp))
        bad = copy.deepcopy(manifest)
        bad['sha256']['proof_search.py'] = 'INVALID'
        manifest_path.write_text(json.dumps(bad))
        reject('manifest_digest_syntax', lambda: p.checked_inputs(tmp))
        save_manifest()
        core = tmp / 'proof_search.py'
        core.write_bytes(frozen['proof_search.py'] + b'\n# edited historical engine\n')
        manifest['sha256']['proof_search.py'] = p.digest(core.read_bytes())
        save_manifest()
        reject('rehashing_does_not_replace_historical_core', lambda: p.checked_inputs(tmp))
        core.write_bytes(frozen['proof_search.py'])
        manifest['sha256']['proof_search.py'] = p.digest(core.read_bytes())
        adapter = tmp / 'proof_routes.py'
        adapter.write_bytes(frozen['proof_routes.py'] + b'\n# swapped adapter\n')
        manifest['sha256']['proof_routes.py'] = p.digest(adapter.read_bytes())
        save_manifest()
        reject('rehashing_does_not_replace_running_adapter', lambda: p.checked_inputs(tmp))

    report = {
        'status': 'passed', 'check_count': len(records), 'checks': records,
        'source_sha256': p.digest(Path(p.__file__).read_bytes()),
        'test_source_sha256': p.digest(Path(__file__).read_bytes()),
        'scope': 'Adapter and search mutation checks. Graph-only fixtures test admission logic; they do not supply scientific acceptance.',
    }
    Path(output).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'passed', 'check_count': len(records), 'scope': report['scope']}))
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=p.HERE)
    parser.add_argument('--output', type=Path, default=p.HERE / 'proof_adapter_tests.json')
    args = parser.parse_args()
    run(args.root, args.output)
