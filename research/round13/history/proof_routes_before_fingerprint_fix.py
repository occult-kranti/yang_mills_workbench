#!/usr/bin/env python3
"""Frozen, reviewed Horn replay for round 13; not a formal mathematics kernel.

All-order statements are explicit route hypotheses. Finite data, locality and
shared variable names cannot be promoted into a continuum or gap theorem.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile
import types

HERE = Path(__file__).resolve().parent
EXECUTING_ADAPTER_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
CORE_SHA256 = '07b5b397af86b6bf5a481b114844c6252046e8ca2b5604dac7d158091632be94'
REVIEWED_FILES = {
    'advisor/advisor.md', 'advisor/theorem_inventory.json', 'advisor/inference_rules.json',
    'advisor/weak-coupling-stability.md',
    'moments/moment_bounds.py', 'locality/locality.md', 'locality/locality_checks.py',
    'response/response.md', 'response/response_checks.py',
}
LOCALITY_CSV = {'geometry_checks.csv', 'boundary_decay.csv', 'scaling_cases.csv', 'continuum_dictionary.csv'}
EXPECTED = REVIEWED_FILES | {
    'moments/output/certificates.json', 'locality/output/results.json',
    'response/output/results.json', 'skeptic/acceptance.json',
    'proof_routes.py', 'proof_search.py',
} | {'locality/output/' + name for name in LOCALITY_CSV}
MATHEMATICAL_HYPOTHESES = {
    'compact_measure', 'link_tensor', 'onsite_selfadjoint', 'bounded_plaquettes',
    'bounded_incidence', 'gauge_invariance', 'exponential_family_differentiation',
    'all_order_constraints', 'nested_compact_relaxations', 'vanishing_optimizer_slack',
    'yarotsky_primary', 'electric_product_vacuum', 'finite_range_static_norm',
    'stability_smallness', 'admissible_stability_boundary', 'gauge_vacuum_restriction',
}
GATES = {'rational_exclusion_gate', 'variance_image_gate', 'path_count', 'boundary_shell_sum'}
OPEN = {'same_geometry_state_scale', 'continuum_observables', 'reconstruction_axioms',
        'nontrivial_finite_energy', 'uniform_physical_decay', 'yang_mills_4d_gap'}
MOMENT_CASES = {(str(k), r, 56) for k in (1, 5, 20) for r in range(1, 7)} | {
    (k, 4, 56) for k in ('0', '-1/1000', '1/1000', '-1/100', '1/100', '-1', '-5', '-20', '-100', '100')
}


class ContractError(ValueError):
    pass


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_regular(root, relative):
    root = Path(root).resolve()
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ContractError('A relative input path is required')
    if any(part in ('..', '.') for part in Path(relative).parts):
        raise ContractError('Input traversal rejected')
    path = root
    for part in Path(relative).parts:
        path = path / part
        if path.is_symlink():
            raise ContractError('Symlink input rejected: ' + relative)
    if not path.resolve().is_relative_to(root) or not path.is_file():
        raise ContractError('Missing regular input: ' + relative)
    return path.read_bytes()


def checked_inputs(root=HERE):
    manifest = json.loads(read_regular(root, 'proof_manifest.json'))
    if not isinstance(manifest, dict) or set(manifest) != {'sha256'} or not isinstance(manifest['sha256'], dict) or set(manifest['sha256']) != EXPECTED:
        raise ContractError('The complete exact manifest input set is required')
    frozen = {}
    for rel, recorded in manifest['sha256'].items():
        if not isinstance(recorded, str) or not re.fullmatch('[0-9a-f]{64}', recorded):
            raise ContractError('Invalid SHA256 syntax')
        raw = read_regular(root, rel)
        if digest(raw) != recorded:
            raise ContractError('Stale or changed source: ' + rel)
        frozen[rel] = raw
    if digest(frozen['proof_search.py']) != CORE_SHA256:
        raise ContractError('The independently reviewed historical search core changed')
    if digest(frozen['proof_routes.py']) != EXECUTING_ADAPTER_SHA256:
        raise ContractError('Manifest adapter differs from the code loaded for this replay')
    return manifest, frozen


def load_frozen(name, relative, frozen, root=HERE):
    module = types.ModuleType(name)
    module.__file__ = str(Path(root) / relative)
    sys.modules[name] = module
    exec(compile(frozen[relative], module.__file__, 'exec'), module.__dict__)
    return module


def validate_ledger(frozen):
    ledger = json.loads(frozen['skeptic/acceptance.json'])
    if not isinstance(ledger, dict) or ledger.get('status') != 'passed':
        raise ContractError('Independent scientific acceptance is absent or incomplete')
    reviewed = ledger.get('reviewed_source_hashes')
    if not isinstance(reviewed, dict) or not REVIEWED_FILES <= set(reviewed):
        raise ContractError('Independent review did not identify every scientific source')
    for rel in REVIEWED_FILES:
        if reviewed[rel] != digest(frozen[rel]):
            raise ContractError('Independent review is stale: ' + rel)
    ids = ledger.get('reviewed_rule_ids')
    if not isinstance(ids, list) or any(not isinstance(x, str) for x in ids) or len(ids) != len(set(ids)):
        raise ContractError('An explicit nonduplicated reviewed rule list is required')
    return frozenset(ids)


def validate_report(report, source_digest, label, convention='boolean'):
    if not isinstance(report, dict):
        raise ContractError(label + ' must be a report object')
    checks = report.get('checks')
    if report.get('status') != 'passed' or report.get('source_sha256') != source_digest:
        raise ContractError(label + ' is stale or incomplete')
    if convention not in ('boolean', 'status'):
        raise ContractError('Unknown check report convention')
    field, accepted = ('passed', True) if convention == 'boolean' else ('status', 'passed')
    def successful(check):
        if not isinstance(check, dict) or set(check) != {'name', field, 'detail'} or not isinstance(check['name'], str) or not check['name']:
            return False
        return check[field] is True if convention == 'boolean' else check[field] == accepted
    if not isinstance(checks, list) or not checks or not all(successful(c) for c in checks):
        raise ContractError(label + ' has absent or failing checks')
    if type(report.get('check_count')) is not int or report['check_count'] != len(checks):
        raise ContractError(label + ' count does not match actual checks')
    if len({c.get('name') for c in checks}) != len(checks):
        raise ContractError(label + ' contains repeated check names')


def replay_evidence(frozen, root=HERE):
    """Recheck exact stored witnesses and regenerate exact locality diagnostics.

    The response check report is source-bound provenance only: floating ODE
    agreement does not prove the scalar identity or all-order hierarchy.
    """
    reviewed_rules = validate_ledger(frozen)
    moments = load_frozen('ym13_moment_frozen', 'moments/moment_bounds.py', frozen, root)
    moments.source_hash = lambda: digest(frozen['moments/moment_bounds.py'])
    collection = json.loads(frozen['moments/output/certificates.json'])
    if not isinstance(collection, dict) or set(collection) != {'status', 'source_sha256', 'certificates'} or collection['status'] != 'passed' or collection['source_sha256'] != moments.source_hash():
        raise ContractError('Moment collection source/schema mismatch')
    certificates = collection['certificates']
    if not isinstance(certificates, list) or len(certificates) != len(MOMENT_CASES):
        raise ContractError('Complete moment case set is required')
    observed = []
    for certificate in certificates:
        if moments.verify(certificate) is not True:
            raise ContractError('Exact moment replay failed')
        observed.append((certificate['kappa'], certificate['level'], certificate['bits']))
    if len(set(observed)) != len(observed) or set(observed) != MOMENT_CASES:
        raise ContractError('The declared moment case set changed')

    locality_report = json.loads(frozen['locality/output/results.json'])
    validate_report(locality_report, digest(frozen['locality/locality_checks.py']), 'Locality diagnostics')
    if set(locality_report.get('files', {})) != LOCALITY_CSV:
        raise ContractError('Locality output file set changed')
    for name in LOCALITY_CSV:
        if locality_report['files'][name] != digest(frozen['locality/output/' + name]):
            raise ContractError('Locality CSV hash mismatch: ' + name)
    # Materialize frozen bytes in an isolated temporary directory because the
    # producer deliberately hashes __file__. No live scientific input is reread.
    with tempfile.TemporaryDirectory(prefix='ym13-locality-replay-', dir=HERE) as temporary:
        temporary = Path(temporary)
        local_source = temporary / 'locality_checks.py'
        local_source.write_bytes(frozen['locality/locality_checks.py'])
        locality = load_frozen('ym13_locality_frozen', 'locality/locality_checks.py', frozen, root)
        locality.__file__ = str(local_source)
        fresh = locality.run_checks(temporary / 'output')
        if fresh != locality_report:
            raise ContractError('Locality recorded checks disagree with frozen-source replay')
        for name in LOCALITY_CSV:
            if (temporary / 'output' / name).read_bytes() != frozen['locality/output/' + name]:
                raise ContractError('Locality recorded CSV disagrees with exact replay: ' + name)

    response = json.loads(frozen['response/output/results.json'])
    if response.get('schema') != 'ym13-response-v1':
        raise ContractError('Response diagnostic schema changed')
    validate_report(response, digest(frozen['response/response_checks.py']), 'Response diagnostics', convention='status')
    return {
        'status': 'passed', 'exact_moment_certificates_replayed': len(certificates),
        'locality_checks_regenerated': locality_report['check_count'],
        'response_checks_source_bound_only': response['check_count'],
        'gates': sorted(GATES), 'reviewed_rule_ids': sorted(reviewed_rules),
        'not_admitted': ['all_order_constraints', 'vanishing_optimizer_slack', *sorted(OPEN)],
        'limits': 'Exact finite witnesses and source-bound reviewed lemmas; finite output does not establish infinitely many constraints or a continuum theory.',
    }


def specifications(frozen, reviewed_rule_ids):
    inventory = json.loads(frozen['advisor/theorem_inventory.json'])
    rules_doc = json.loads(frozen['advisor/inference_rules.json'])
    entries = inventory.get('claims')
    rules = rules_doc.get('rules')
    if not isinstance(entries, list) or not entries or not isinstance(rules, list):
        raise ContractError('Advisor inventory/rules schema')
    claims = {}
    for claim in entries:
        if not isinstance(claim, dict) or not isinstance(claim.get('id'), str) or claim['id'] in claims or not isinstance(claim.get('statement'), str):
            raise ContractError('Invalid or duplicate advisor claim')
        claims[claim['id']] = claim
    if not MATHEMATICAL_HYPOTHESES | GATES | OPEN <= set(claims):
        raise ContractError('The declared gate/hypothesis/target inventory is incomplete')
    seen = set()
    for rule in rules:
        if not isinstance(rule, dict) or not isinstance(rule.get('id'), str) or rule['id'] in seen:
            raise ContractError('Duplicate or invalid advisor rule')
        seen.add(rule['id'])
        premises = rule.get('premises')
        if not isinstance(premises, list) or not premises or any(not isinstance(x, str) for x in premises) or len(premises) != len(set(premises)):
            raise ContractError('Rule premises must be explicit and nonduplicated')
        if not (set(premises) | {rule.get('conclusion')}) <= set(claims):
            raise ContractError('Rule mentions an undeclared atom')
        if type(rule.get('cost')) is not int or rule['cost'] <= 0:
            raise ContractError('Rule costs must be positive integers')
        if rule.get('evidence') not in ('advisor.md', 'weak-coupling-stability.md'):
            raise ContractError('Unsupported advisor evidence reference')
        if rule['id'] not in reviewed_rule_ids:
            raise ContractError('Rule has no independent acceptance: ' + rule['id'])
    if set(reviewed_rule_ids) != seen:
        raise ContractError('Reviewed rule list and complete advisor rules disagree')
    return claims, rules


def backward_cone(rules, goal):
    """Retain every rule whose conclusion can feed the goal, even at seed atoms."""
    atoms = {goal}
    selected = set()
    changed = True
    while changed:
        changed = False
        for rule in rules:
            if rule['conclusion'] in atoms and rule['id'] not in selected:
                selected.add(rule['id'])
                atoms.update(rule['premises'])
                changed = True
    return atoms, [rule for rule in rules if rule['id'] in selected]


def make_library(frozen, replay, goal, hypotheses=(), gates=()):
    if replay.get('status') != 'passed' or set(replay.get('gates', [])) != GATES:
        raise ContractError('Completed source-bound replay is required')
    if not isinstance(hypotheses, (list, tuple, set, frozenset)) or not isinstance(gates, (list, tuple, set, frozenset)):
        raise ContractError('Explicit hypothesis and gate lists are required')
    if len(hypotheses) != len(set(hypotheses)) or len(gates) != len(set(gates)):
        raise ContractError('Duplicate seed declarations')
    hypotheses, gates = set(hypotheses), set(gates)
    if not hypotheses <= MATHEMATICAL_HYPOTHESES or not gates <= GATES:
        raise ContractError('Only fixed declared hypotheses and replayed gates may seed a route')
    claims, rules = specifications(frozen, replay['reviewed_rule_ids'])
    if goal not in claims:
        raise ContractError('Unknown proof goal')
    atoms, selected = backward_cone(rules, goal)
    available = hypotheses | gates
    seeds = available & atoms
    # Record all transitive explicit hypotheses for each conclusion. A missing
    # seed remains a required hypothesis in metadata; it never becomes a fact.
    producers = {a: [r for r in selected if r['conclusion'] == a] for a in atoms}
    dependencies = {a: ({a} if not producers[a] and a in MATHEMATICAL_HYPOTHESES | GATES | OPEN else set()) for a in atoms}
    changed = True
    while changed:
        changed = False
        for atom in sorted(atoms):
            if not producers[atom]:
                continue
            alternatives = [set().union(*(dependencies[p] for p in rule['premises'])) for rule in producers[atom]]
            # Node metadata records assumptions common to every derivation.
            # Actual route certificates retain all explicit premises used.
            inherited = set.intersection(*alternatives)
            changed |= inherited != dependencies[atom]
            dependencies[atom] = inherited
    nodes = []
    for atom in sorted(atoms):
        kind = 'target' if atom in OPEN else 'declared_hypothesis' if atom in MATHEMATICAL_HYPOTHESES else 'theorem'
        nodes.append({
            'id': atom, 'statement': claims[atom]['statement'], 'scope': 'R13', 'kind': kind,
            'assumption_ids': sorted(dependencies[atom] - {atom}),
            'verification': 'Source-bound scientific review; exact finite gate replay; explicit mathematical hypotheses retained.',
            'source': 'advisor/advisor.md', 'version': '13.1',
        })
    library = {
        'nodes': nodes,
        'rules': [{'id': r['id'], 'premises': r['premises'], 'conclusion': r['conclusion'], 'cost': r['cost'],
                   'scope': 'R13', 'proof_ref': 'advisor/' + r['evidence'] + '; rule ' + r['id'], 'review_status': 'reviewed'} for r in selected],
        'initial_facts': sorted(seeds), 'goals': [goal], 'conditional_assumptions': [], 'blocked_goals': [],
    }
    optimization = {
        'method': 'complete backward dependency cone; no stopping at available seeds',
        'all_advisor_rules': len(rules), 'retained_rule_ids': [r['id'] for r in selected],
        'discarded_rule_ids': sorted(r['id'] for r in rules if r not in selected),
        'available_hypotheses': sorted(hypotheses), 'available_replayed_gates': sorted(gates),
        'retained_seed_ids': sorted(seeds),
        'scope': 'Every rule capable of feeding this goal is retained; irrelevant interleavings are omitted. Optimality applies only to the finite supplied rule library.',
    }
    return library, optimization


def route_specs():
    moment = {'compact_measure'}
    locality = {'link_tensor', 'onsite_selfadjoint', 'bounded_plaquettes', 'bounded_incidence', 'gauge_invariance'}
    all_order = moment | {'all_order_constraints'}
    convergence = all_order | {'nested_compact_relaxations'}
    rational = {'rational_exclusion_gate', 'variance_image_gate'}
    local_gates = {'path_count', 'boundary_shell_sum'}
    stability = {'yarotsky_primary', 'electric_product_vacuum', 'finite_range_static_norm',
                 'stability_smallness', 'admissible_stability_boundary', 'gauge_vacuum_restriction'}
    return [
        ('moment_interval', 'moment_outer_interval', moment, rational, 'proved'),
        ('variance_interval', 'variance_outer_interval', moment, rational, 'proved'),
        ('conditional_all_order_uniqueness', 'hierarchy_unique', all_order, set(), 'proved'),
        ('conditional_hierarchy_convergence', 'hierarchy_interval_convergence', convergence, set(), 'proved'),
        ('conditional_algorithm_convergence', 'algorithm_interval_convergence', convergence | {'vanishing_optimizer_slack'}, set(), 'proved'),
        ('scalar_susceptibility', 'susceptibility_identity', moment | {'exponential_family_differentiation'}, set(), 'proved'),
        ('regular_scalar_riccati', 'coupling_riccati', moment | {'exponential_family_differentiation'}, set(), 'proved'),
        ('fixed_spacing_local_volume_limit', 'bounded_local_volume_limit', locality, local_gates, 'proved'),
        ('physical_local_bound', 'physical_local_bound', locality, local_gates, 'proved'),
        ('conditional_uniform_lattice_hamiltonian_gap', 'uniform_physical_hamiltonian_gap', stability, set(), 'proved'),
        ('conditional_canonical_physical_gap', 'canonical_physical_gap', stability, set(), 'proved'),
        ('stability_without_smallness', 'uniform_physical_hamiltonian_gap', stability - {'stability_smallness'}, set(), 'not_derivable'),
        ('canonical_gap_without_smallness', 'canonical_physical_gap', stability - {'stability_smallness'}, set(), 'not_derivable'),
        ('without_psd_witness', 'moment_outer_interval', moment, rational - {'rational_exclusion_gate'}, 'not_derivable'),
        ('without_variance_image', 'variance_outer_interval', moment, rational - {'variance_image_gate'}, 'not_derivable'),
        ('without_boundary_tail', 'bounded_local_volume_limit', locality, local_gates - {'boundary_shell_sum'}, 'not_derivable'),
        ('without_path_count', 'bounded_local_volume_limit', locality, local_gates - {'path_count'}, 'not_derivable'),
        ('finite_constraints_not_all_orders', 'hierarchy_unique', moment, rational, 'not_derivable'),
        ('without_nested_relaxations', 'hierarchy_interval_convergence', all_order, rational, 'not_derivable'),
        ('finite_optimizer_slack_not_asymptotic', 'algorithm_interval_convergence', convergence, rational, 'not_derivable'),
        ('locality_does_not_supply_decay', 'uniform_physical_decay', locality, local_gates, 'not_derivable'),
        ('lattice_does_not_supply_continuum', 'continuum_observables', locality, local_gates, 'not_derivable'),
        ('shared_symbols_do_not_match_states', 'same_geometry_state_scale', locality | moment, local_gates | rational, 'not_derivable'),
        ('four_dimensional_mass_gap', 'yang_mills_4d_gap', locality | convergence | stability | {'vanishing_optimizer_slack', 'exponential_family_differentiation'}, local_gates | rational, 'not_derivable'),
    ]


def execute(root=HERE, output=None):
    root = Path(root).resolve()
    manifest, frozen = checked_inputs(root)
    replay = replay_evidence(frozen, root)
    search = load_frozen('ym13_proof_search_frozen', 'proof_search.py', frozen, root)
    routes = {}
    for name, goal, hypotheses, gates, expected in route_specs():
        library, optimization = make_library(frozen, replay, goal, hypotheses, gates)
        result = search.plan(library, max_states=10000, max_backward_states=10000)
        if result['status'] != expected:
            raise ContractError('Unexpected route outcome: ' + name + ': ' + result['status'])
        if expected == 'proved':
            ids = [step['rule_id'] for step in result['certified_proof']['steps']]
            independent_replay = search.check_proof(search.load_library(library), ids)
            if not independent_replay.passed or independent_replay.cost != result['certified_cost']:
                raise ContractError('Final ordered certificate replay failed: ' + name)
            if not result.get('first_meeting_candidate', {}).get('passed'):
                raise ContractError('A positive route lacked an actual two-front meeting: ' + name)
            result['separate_certificate_replay'] = independent_replay.as_dict()
        routes[name] = {'library': library, 'optimization': optimization, 'result': result}
    document = {
        'status': 'passed', 'manifest': manifest, 'arithmetic': replay, 'routes': routes,
        'scope': 'Actual finite ground-Horn two-front search and ordered certificate replay. Reviewed conventional mathematical arguments are not formal-kernel proofs. All-order and asymptotic hypotheses are explicitly conditional.',
        'publication_limits': ['No all-order premise comes from finitely many stored certificates.',
                               'The Euclidean compact measure is not identified with a Hamiltonian state.',
                               'Fixed-spacing local dynamics does not imply a spectral gap or continuum construction.'],
    }
    target = Path(output) if output else root / 'proof_results.json'
    target.write_text(json.dumps(document, indent=2, allow_nan=False) + '\n')
    print(json.dumps({'status': 'passed', 'routes': {name: {'status': r['result']['status'], 'cost': r['result'].get('certified_cost')} for name, r in routes.items()}, 'bytes': target.stat().st_size}))
    return document


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=HERE)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    execute(args.root, args.output)
