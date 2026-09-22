"""AJ1 admission-format and semantic attacks, never scientific executions."""
import argparse
import copy
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reproduce import PREFIX, Validator, digest, semantics, require
from release.aj1_inventory_controls import fixture, put, BASE, SOURCE, INSTRUCTIONS, CONTRACT


def adapter_controls():
    rejected = []
    with tempfile.TemporaryDirectory(prefix='ym28-aj1-provenance-controls-') as directory:
        temporary = Path(directory)
        original = temporary / 'baseline'
        fixture(original)
        put(original, BASE + 'check.py', '# Synthetic fixture; never executed.\n')
        put(original, BASE + 'report.md', 'Synthetic admission fixture only.\n')
        pack_name = BASE + 'inputs/input-pack-freeze.json'
        pack = {'schema': 'ym28-aj1-forward-input-pack-freeze-v1', 'contract_sha256': digest(original / CONTRACT),
                'bindings': {str(p.relative_to(original)): digest(p) for p in (original / BASE / 'inputs').rglob('*') if p.is_file()}}
        put(original, pack_name, pack)
        provenance = {'contract_sha256': digest(original / CONTRACT), 'input_pack_sha256': digest(original / pack_name),
                      'checker_sha256': digest(original / BASE / 'check.py'), 'input_binding_count': len(pack['bindings'])}
        result = {'schema': 'synthetic-only', 'scope': {'no_physics': True}, 'provenance': provenance}
        put(original, BASE + 'output/results.json', result)
        put(original, BASE + 'output/source-manifest.json', provenance)
        def configuration(root):
            validator = Validator(root)
            closure, snapshots, _ = validator.manifests('aj1', 'forward', [SOURCE], [INSTRUCTIONS])
            frozen = {str(p.relative_to(root)): digest(p) for p in (root / BASE).rglob('*') if p.is_file() and p != root / BASE / 'freeze.json'}
            put(root, BASE + 'freeze.json', {'loop': 'aj1', 'sha256': frozen})
            spec = {'binding_field': 'aj1_provenance_pack', 'input_pack': pack_name, 'source_manifests': [SOURCE],
                    'instruction_manifests': [INSTRUCTIONS], 'required_snapshots': snapshots,
                    'freeze': BASE + 'freeze.json', 'freeze_binding_field': 'sha256', 'report_binding': 'freeze',
                    'semantic_controls': [{'id': 'no-physics', 'pointer': '/scope/no_physics', 'equals': True}],
                    'output_artifacts': {'source-manifest.json': {'sha256': digest(root / BASE / 'output/source-manifest.json'),
                                        'binding': 'freeze', 'equals_result_pointer': '/provenance'}}}
            return validator, spec, {**closure, **frozen}
        validator, spec, bindings = configuration(original)
        validator.producer('aj1', 'forward', validator.contract('aj1'), spec, bindings)
        def attack(label, change):
            root = temporary / label
            shutil.copytree(original, root)
            output = json.loads((root / BASE / 'output/results.json').read_text())
            current_pack = json.loads((root / pack_name).read_text())
            change(root, output, current_pack)
            # Deliberately bind the changed pack/output metadata coherently.
            # Missing dependencies and auxiliary mismatch must still reject.
            put(root, pack_name, current_pack)
            output['provenance']['input_pack_sha256'] = digest(root / pack_name)
            output['provenance']['input_binding_count'] = len(current_pack['bindings'])
            put(root, BASE + 'output/results.json', output)
            if label != 'auxiliary-provenance-mismatch':
                put(root, BASE + 'output/source-manifest.json', output['provenance'])
            validator, spec, bindings = configuration(root)
            if label == 'auxiliary-absent-from-freeze':
                frozen = validator.load(BASE + 'freeze.json')
                frozen['sha256'].pop(BASE + 'output/source-manifest.json')
                put(root, BASE + 'freeze.json', frozen)
            elif label == 'auxiliary-absent-from-gate':
                bindings.pop(BASE + 'output/source-manifest.json')
            elif label == 'fabricated-output-hash-pointer':
                spec['output_artifacts']['source-manifest.json']['sha256_pointer'] = '/invented_hash'
            elif label == 'wrong-auxiliary-result-projection':
                spec['output_artifacts']['source-manifest.json']['equals_result_pointer'] = '/scope'
            elif label == 'missing-input-pack-declaration':
                spec.pop('input_pack')
            try:
                validator.producer('aj1', 'forward', validator.contract('aj1'), spec, bindings)
            except ValueError:
                rejected.append(label)
            else:
                raise ValueError('invalid provenance/auxiliary adapter admitted: ' + label)
        noop = lambda root, result, pack: None
        for label, name in [('pack-omits-source-manifest', SOURCE), ('pack-omits-instruction-manifest', INSTRUCTIONS),
                            ('pack-omits-contract-copy', BASE + 'inputs/' + CONTRACT),
                            ('pack-omits-installed-instruction', BASE + 'inputs/installed-methods/synthetic-0.md')]:
            attack(label, lambda root, result, pack, name=name: pack['bindings'].pop(name))
        attack('wrong-reported-script', lambda root, result, pack: result['provenance'].__setitem__('checker_sha256', '0' * 64))
        attack('wrong-reported-contract', lambda root, result, pack: result['provenance'].__setitem__('contract_sha256', '0' * 64))
        attack('wrong-input-pack-contract', lambda root, result, pack: pack.__setitem__('contract_sha256', '0' * 64))
        attack('auxiliary-provenance-mismatch', lambda root, result, pack: put(root, BASE + 'output/source-manifest.json', {'other': 'coherently rebound output'}))
        attack('undeclared-extra-output', lambda root, result, pack: put(root, BASE + 'output/extra.json', {'scientific': 'undeclared'}))
        for label in ['auxiliary-absent-from-freeze', 'auxiliary-absent-from-gate', 'fabricated-output-hash-pointer',
                      'wrong-auxiliary-result-projection', 'missing-input-pack-declaration']:
            attack(label, noop)
    return {'status': 'passed', 'adapter_mutations_rejected': len(rejected), 'controls': rejected, 'new_research_loops': 0}


def run(spec_name):
    validator = Validator()
    spec = validator.load(spec_name)
    require(spec.get('loop') == 'aj1', 'AJ1 admission specification required')
    original = {side: validator.load(PREFIX + f'{side}/aj1/output/results.json') for side in ['forward', 'reverse']}
    rejected = []
    def attack(label, side, change, relations_only=False):
        result = copy.deepcopy(original[side]); configuration = copy.deepcopy(spec['producers'][side])
        if relations_only:
            configuration['semantic_controls'] = [{'id': 'schema-only', 'pointer': '/schema', 'equals': result['schema']}]
        semantics(result, configuration); change(result)
        try:
            semantics(result, configuration)
        except ValueError:
            rejected.append({'name': label, 'relations_only': relations_only})
        else:
            raise ValueError('AJ1 semantic attack admitted: ' + label)
    attack('omit-incoming-anchors', 'forward', lambda r: r['geometry']['fixtures'][2]['regions'][2].__setitem__('incoming_anchors', []), True)
    attack('clip-outgoing-endpoints', 'forward', lambda r: r['geometry']['fixtures'][0].__setitem__('all_endpoint_count', 64), True)
    attack('whole-star-boundary-substituted', 'forward', lambda r: r['geometry']['fixtures'][0].__setitem__('boundary_rule_difference', 0), True)
    attack('uncharged-reset-energy-cost', 'forward', lambda r: r['exact_coefficients'].__setitem__('local_energy_per_site_over_M_ceiling', {'numerator': 4, 'denominator': 1}), True)
    attack('changed-physical-clock', 'forward', lambda r: r['exact_coefficients'].__setitem__('delta_over_alpha', {'numerator': 1, 'denominator': 1}), True)
    attack('uncentered-energy', 'forward', lambda r: r['discriminating_controls']['ground_center_and_units'].__setitem__('centered_normalized_excitation', {'numerator': 9, 'denominator': 1}), True)
    attack('commuting-compression-countermodel-erased', 'forward', lambda r: r['discriminating_controls']['compression_not_reducing']['HP'][1].__setitem__(0, 0), True)
    attack('fake-domain-bound', 'reverse', lambda r: r['controls']['arbitrary_bounded_local_domain']['prefixes'][2].__setitem__('form', '1'), True)
    attack('fake-finite-rank-cutoff', 'reverse', lambda r: r['controls']['compact_local_energy_cutoffs']['fixtures'][5].__setitem__('finite_rank_upper', 1), True)
    attack('blind-gauge-replacement', 'reverse', lambda r: r['nondiscriminating_control']['replacement'].__setitem__('missing_head', r['nondiscriminating_control']['replacement']['correct']), True)
    attack('normality-from-weakstar', 'reverse', lambda r: r['controls']['weakstar_not_normal']['fixtures'][0].__setitem__('cutoff_mass', 1), True)
    attack('pointnorm-continuity-substituted', 'reverse', lambda r: r['controls']['strong_not_pointnorm']['fixtures'][3].__setitem__('conjugation_difference_norm', 0), True)
    attack('numeric-coupling-upgrade', 'forward', lambda r: r['scope'].__setitem__('numerical_nonzero_tau_certified', True))
    attack('nonzero-excitation-upgrade', 'reverse', lambda r: r['theorem']['scope'].__setitem__('nonzero_physical_excitation_witness', True))
    attack('same-representation-resolvent-upgrade', 'reverse', lambda r: r['theorem']['scope'].__setitem__('same_representation_strong_resolvent', True))
    attack('all-boundaries-upgrade', 'forward', lambda r: r['scope'].__setitem__('all_boundary_limits_equal', True))
    attack('continuum-upgrade', 'reverse', lambda r: r['theorem']['scope'].__setitem__('continuum_yang_mills', True))
    attack('Wilson-only-completion-upgrade', 'reverse', lambda r: r['theorem']['scope'].__setitem__('wilson_only_algebra_completion', True))
    evidence = next(e for e in spec['supplemental_evidence'] if e['path'].endswith('/output/geometry.json'))
    geometry = validator.load(evidence['path'])
    for label, change in [
        ('missing-owned-link', lambda g: g['fixtures'][0]['links'].pop()),
        ('same-count-incorrect-oriented-face', lambda g: g['fixtures'][0]['groups'][0]['faces'][0]['word'][0].__setitem__(1, -1)),
        ('wrong-link-owner', lambda g: g['fixtures'][0]['groups'][0]['faces'][0]['owners'][0].__setitem__(0, 1)),
        ('Boolean-endpoint-coordinate', lambda g: g['fixtures'][0]['endpoint_vertices'][0].__setitem__(0, False))]:
        changed = copy.deepcopy(geometry); change(changed)
        try:
            semantics(changed, evidence)
        except ValueError:
            rejected.append({'name': label, 'relations_only': False})
        else:
            raise ValueError('full geometry corruption admitted: ' + label)
    return {'status': 'passed', 'semantic_mutations_rejected': len(rejected), 'controls': rejected,
            'specification_sha256': digest(validator.source(spec_name)), 'new_research_loops': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--spec', default=PREFIX+'advisor/aj1-admission.json'); args=parser.parse_args()
    print(json.dumps({'adapter': adapter_controls(), 'semantics': run(args.spec)}, sort_keys=True))
