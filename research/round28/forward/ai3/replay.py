#!/usr/bin/env python3
"""Fresh normal/optimized replay of the frozen AI3 forward calculation."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    target = HERE / 'verification.json'
    if target.exists():
        raise ValueError('preserve existing replay evidence')
    before = {p: sha(HERE / p) for p in ('check.py', 'report.md', 'output/results.json',
                                       'inputs/source-inventory.json')}
    frozen = (HERE / 'output/results.json').read_bytes()
    results = []
    with tempfile.TemporaryDirectory(prefix='ai3-replay-', dir=HERE) as temporary:
        for label, flags in (('normal', ['-B']), ('optimized', ['-O', '-B'])):
            output = Path(temporary) / label
            command = [sys.executable, *flags, str(HERE / 'check.py'), '--output', str(output)]
            process = subprocess.run(command, capture_output=True, text=True)
            if process.returncode:
                raise ValueError(label + ' failed: ' + process.stderr)
            result_file = output / 'results.json'
            payload = result_file.read_bytes()
            if payload != frozen:
                raise ValueError(label + ' disagrees with frozen output')
            data = json.loads(payload)
            if data['checks_count'] != len(data['checks']) or data['checks_count'] != 526:
                raise ValueError('semantic active check inventory mismatch')
            if len(data['rows']) != 10 or data['all_order_reflection_proved'] is not True:
                raise ValueError('required calculation missing')
            if any(any(row['ratio_disjoint'].values()) for row in data['rows']):
                raise ValueError('unexpected ratio admission')
            positive = [(r['power'], r['k']) for r in data['rows']
                        if r['scalar_discrimination']['4']['disjoint'] and r['scalar_discrimination']['5']['disjoint']]
            if positive != [(18, 5)]:
                raise ValueError('scalar baseline admission changed')
            results.append({'mode': label, 'flags': flags, 'exit_code': process.returncode,
                            'result_sha256': sha(result_file), 'byte_equal_frozen': True,
                            'checks': data['checks_count'], 'cells': len(data['rows'])})
    after = {p: sha(HERE / p) for p in before}
    if before != after:
        raise ValueError('producer bytes changed during verification')
    target.write_text(json.dumps({'status': 'passed', 'normal_optimized_byte_equality': True,
                                 'producer_before': before, 'producer_after': after,
                                 'replay_script_sha256': sha(Path(__file__)), 'runs': results,
                                 'temporary_outputs_removed_after_comparison': True}, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'passed', 'runs': results}, indent=2))


if __name__ == '__main__':
    main()
