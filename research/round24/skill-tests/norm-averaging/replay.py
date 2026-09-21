#!/usr/bin/env python3
"""Portable fixed-inventory replay and mutation checks; standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


SOURCES = (
    'check.py', 'replay.py', 'report.md', 'contract.json', 'source-readings.json',
    'inputs/paired/SKILL.md',
    'inputs/paired/references/averaged-limits-and-relative-repairs.md',
    'inputs/paired/references/finite-observations-and-operator-limits.md',
    'inputs/paired/references/stationarity-support-and-admission.md',
    'inputs/project/AGENTS.md',
    'inputs/project/finite-observations-and-operator-limits.md',
    'inputs/project/stationarity-support-and-admission.md',
    'inputs/project/newton-tesla-project-method.md',
    'inputs/newton/SKILL.md', 'inputs/newton/references/research.md',
    'inputs/tesla/SKILL.md', 'inputs/tesla/references/research.md',
)
OUTPUTS = ('output/results.json', 'output/controls.json')
CHECKS = {
    'primitive_derivative_is_actual_source', 'primitive_zero_at_origin',
    'actual_average_is_zero', 'scalar_average_retained',
    'commutator_and_boundary', 'ordered_product_matches_forward_ode',
    'ordered_adjoint_matches_right_ode', 'scalar_shift_factorization',
    'rational_majorant_arithmetic',
}
CONTROLS = {
    'wrong_unaveraged_source_as_average_rejected', 'discard_scalar_average_rejected',
    'reversed_primitive_sign_rejected', 'bilateral_boundary_commutation_rejected',
    'wrong_source_phase_rejected', 'adjoint_left_multiplication_rejected',
    'scalar_shift_limit_identity_rejected', 'negative_tau_rejected',
    'negative_horizon_rejected',
}


class AdmissionError(Exception):
    pass


def require(value, message):
    if value is not True:
        raise AdmissionError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, sort_keys=True, indent=2)+'\n')


def safe_file(root, relative):
    name = Path(relative)
    require(not name.is_absolute() and '..' not in name.parts, 'unsafe relative path')
    path = root/name
    for parent in [path, *path.parents]:
        require(not parent.is_symlink(), 'symlink path component')
    require(path.is_file(), 'missing required file: '+relative)
    return path


def read_json(path):
    try:
        return json.loads(path.read_text())
    except (ValueError, OSError) as exc:
        raise AdmissionError('invalid JSON') from exc


def statuses(mapping, expected, label):
    require(type(mapping) is dict and set(mapping) == expected, label+' identities')
    require(all(value is True for value in mapping.values()), label+' exact Boolean successes')


def validate(root):
    manifest = read_json(safe_file(root, 'source-manifest.json'))
    require(manifest.get('schema') == 'norm-averaging-sources-v1', 'manifest schema')
    require(type(manifest.get('sources')) is dict and
            set(manifest['sources']) == set(SOURCES), 'complete fixed source inventory')
    require(type(manifest.get('outputs')) is dict and
            set(manifest['outputs']) == set(OUTPUTS), 'complete fixed output inventory')
    for kind in ['sources', 'outputs']:
        for name, expected in manifest[kind].items():
            require(digest(safe_file(root, name)) == expected, 'byte binding: '+name)
    contract = read_json(root/'contract.json')
    require(contract.get('physics_roadmap_loops') == 0 and
            type(contract.get('physics_roadmap_loops')) is int, 'zero physics loops')
    require(contract.get('expected_outputs') == list(OUTPUTS), 'contract output inventory')
    readings = read_json(root/'source-readings.json')
    require({row['snapshot'] for row in readings['readings']} ==
            {name for name in SOURCES if name.startswith('inputs/')}, 'all snapshots recorded')
    result = read_json(root/OUTPUTS[0])
    control = read_json(root/OUTPUTS[1])
    require(result.get('schema') == 'norm-averaging-check-v1', 'result schema')
    require(control.get('schema') == 'norm-averaging-controls-v1', 'controls schema')
    require(result.get('passed') is True and control.get('passed') is True, 'exact Boolean passed')
    require(type(result.get('degree')) is int and result['degree'] == 6, 'Taylor degree')
    statuses(result.get('checks'), CHECKS, 'checks')
    statuses(result.get('controls'), CONTROLS, 'embedded controls')
    statuses(control.get('controls'), CONTROLS, 'control file')
    return manifest


def copy_closure(root, target):
    target.mkdir()
    for name in [*SOURCES, *OUTPUTS, 'source-manifest.json']:
        destination = target/name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root/name, destination)


def admit(root, optimized):
    validate(root)
    with tempfile.TemporaryDirectory(prefix='norm-averaging-external-replay-') as tmp:
        base = Path(tmp)
        source, output = base/'source', base/'fresh-output'
        copy_closure(root, source)
        command = [sys.executable, *(['-O'] if optimized else []),
                   str(source/'check.py'), '--output', str(output)]
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        proc = subprocess.run(command, cwd=source, env=env, text=True,
                              capture_output=True, timeout=30)
        require(proc.returncode == 0, 'checker execution: '+proc.stderr)
        require({p.name for p in output.iterdir()} == {'results.json', 'controls.json'},
                'generated output inventory')
        for name in OUTPUTS:
            require((output/Path(name).name).read_bytes() == (root/name).read_bytes(),
                    'recomputed output mismatch: '+name)
    return True


def rebind(root, section, relative):
    manifest = read_json(root/'source-manifest.json')
    manifest[section][relative] = digest(root/relative)
    dump(root/'source-manifest.json', manifest)


def mutate(root, kind):
    result_path, controls_path = root/OUTPUTS[0], root/OUTPUTS[1]
    if kind == 'coherent_nonboolean_status':
        result = read_json(result_path)
        result['passed'] = 'true'
        dump(result_path, result)
        rebind(root, 'outputs', OUTPUTS[0])
    elif kind == 'coherent_failed_control':
        name = 'wrong_source_phase_rejected'
        for relative in OUTPUTS:
            result = read_json(root/relative)
            result['controls'][name] = False
            dump(root/relative, result)
            rebind(root, 'outputs', relative)
    elif kind == 'coherent_missing_snapshot':
        name = 'inputs/paired/references/averaged-limits-and-relative-repairs.md'
        (root/name).unlink()
        manifest = read_json(root/'source-manifest.json')
        del manifest['sources'][name]
        dump(root/'source-manifest.json', manifest)
    elif kind == 'coherent_changed_bound':
        result = read_json(result_path)
        result['bounds'][1]['bound'] = '999'
        dump(result_path, result)
        rebind(root, 'outputs', OUTPUTS[0])
    elif kind == 'stale_source_hash':
        with (root/'report.md').open('a') as stream:
            stream.write('\nChanged report.\n')
    elif kind == 'parent_symlink':
        old, target = root/'inputs/paired', root.parent/'relocated-paired'
        old.rename(target)
        old.symlink_to(target, target_is_directory=True)
    elif kind == 'leaf_symlink':
        old, target = root/'report.md', root.parent/'relocated-report.md'
        old.rename(target)
        old.symlink_to(target)
    else:
        raise AdmissionError('unknown mutation')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', required=True, type=Path)
    args = parser.parse_args()
    require(args.record.is_absolute(), 'record path must be absolute')
    require(not args.record.exists(), 'record must be new')
    root = Path(__file__).absolute().parent
    manifest = validate(root)
    rejected = {}
    for optimized in [False, True]:
        mode = 'optimized' if optimized else 'normal'
        admit(root, optimized)
        rejected[mode] = {}
        for kind in ['coherent_nonboolean_status', 'coherent_failed_control',
                     'coherent_missing_snapshot', 'coherent_changed_bound',
                     'stale_source_hash', 'parent_symlink', 'leaf_symlink']:
            with tempfile.TemporaryDirectory(prefix='norm-averaging-external-control-') as tmp:
                copy = Path(tmp)/'source'
                copy_closure(root, copy)
                mutate(copy, kind)
                try:
                    admit(copy, optimized)
                except AdmissionError:
                    rejected[mode][kind] = True
                else:
                    raise AdmissionError('mutation admitted: '+mode+'/'+kind)
    record = {
        'schema': 'norm-averaging-replay-v1', 'passed': True,
        'validator_optimized': bool(sys.flags.optimize),
        'source_manifest_sha256': digest(root/'source-manifest.json'),
        'bound_sources': manifest['sources'], 'compared_outputs': manifest['outputs'],
        'checker_modes': {'normal': True, 'optimized': True},
        'rejected_mutations': rejected,
        'fresh_execution': 'Every checker run used a new tempfile directory outside the source tree, with a copied relative source closure and a new output directory.',
        'command_template': 'python [-O] COPIED_SOURCE/check.py --output ABSOLUTE_FRESH_EXTERNAL_DIR',
        'mathematical_scope': 'Exact finite algebra and integrity evidence; operator theorem is in report.md.',
    }
    args.record.parent.mkdir(parents=True, exist_ok=True)
    dump(args.record, record)
    print(json.dumps({'passed': True, 'checker_modes': 2, 'rejected_mutations': 14,
                      'validator_optimized': bool(sys.flags.optimize)}, sort_keys=True))


if __name__ == '__main__':
    main()
