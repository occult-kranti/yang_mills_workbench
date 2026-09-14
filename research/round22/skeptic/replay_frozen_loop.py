#!/usr/bin/env python3
"""Independent source-bound producer replays with temporary output trees."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).absolute().parents[3]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    for component in (path, *path.parents):
        require(not component.is_symlink(), 'symlink input: '+str(path))
    require(path.is_file(), 'missing input: '+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    return json.loads(path.read_text(), object_pairs_hook=pairs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--loop', required=True)
    parser.add_argument('--forward-hash', required=True)
    parser.add_argument('--reverse-hash', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'summary must be fresh')
    contract_name = f'research/round22/contracts/{args.loop}.json'
    contract = read(ROOT/contract_name)
    records = {}
    for direction, expected in [('forward', args.forward_hash), ('reverse', args.reverse_hash)]:
        prefix = f'research/round22/{direction}/{args.loop}/'
        base = ROOT/prefix
        require(digest(base/'submission.json') == expected, 'submission changed: '+direction)
        submitted = read(base/'submission.json')
        for name, value in submitted['files'].items():
            require(digest(ROOT/name) == value, 'submitted file changed: '+name)
        manifest = read(base/'output/source-manifest.json')
        required = {prefix+'check.py', prefix+'report.md', contract_name}
        required.update(contract['instruction_inputs'])
        required.update(contract['dependencies'])
        require(required <= manifest['inputs'].keys(), 'required input omitted')
        for name, value in manifest['inputs'].items():
            require(digest(ROOT/name) == value, 'source manifest drift: '+name)
        for name, value in contract['dependencies'].items():
            require(manifest['inputs'][name] == value, 'dependency expectation drift')
        require(set(manifest['outputs']) == {'results.json', 'controls.json'}, 'scientific output set changed')
        for name, value in manifest['outputs'].items():
            require(digest(base/'output'/name) == value, 'frozen output drift')
        records[direction] = {
            'submission_sha256': expected,
            'submitted_files': submitted['files'],
            'source_inputs': manifest['inputs'],
            'replays': {},
        }
        for optimized in [False, True]:
            with tempfile.TemporaryDirectory(prefix='ym22-skeptic-replay-') as folder:
                out = Path(folder)/'fresh-output'
                command = [sys.executable, '-B']+(['-O'] if optimized else [])
                command += [str(base/'check.py'), '--output', str(out)]
                run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
                require(run.returncode == 0, run.stdout+run.stderr)
                output_hashes = {}
                for name in ['results.json', 'controls.json', 'source-manifest.json']:
                    require((out/name).read_bytes() == (base/'output'/name).read_bytes(), 'replay byte mismatch: '+name)
                    output_hashes[name] = digest(out/name)
                for name in ['results.json', 'controls.json']:
                    payload = read(out/name)
                    require(payload.get('loop') == args.loop and payload.get('direction') == direction, 'output identity')
                    require(payload.get('passed') is True, 'output must pass explicitly')
                records[direction]['replays']['optimized' if optimized else 'normal'] = {
                    'command_template': command[:-1]+['FRESH_TEMPORARY_OUTPUT'],
                    'exit_code': run.returncode, 'stdout': run.stdout.strip(),
                    'all_declared_outputs_match_frozen': True, 'outputs': output_hashes,
                }
    summary = {'schema': 'ym22-skeptic-replays-v1', 'loop': args.loop, 'status': 'passed',
               'replay_driver_sha256': digest(Path(__file__).absolute()),
               'replay_trees_retained': False, 'directions': records}
    args.output.write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'loop': args.loop, 'status': 'passed', 'replays': 4}))


if __name__ == '__main__':
    main()
