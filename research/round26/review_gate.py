"""Seal a reviewed loop after fresh normal/optimized replay of both directions."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from admission import ROOT, R, LOOPS, require, digest, hashes, metadata, producer_inventory


def main():
    p = argparse.ArgumentParser()
    p.add_argument('loop', choices=LOOPS)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    out = a.output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT), 'fresh external output required')
    out.mkdir(parents=True)
    loop = a.loop
    target = R / f'advisor/{loop}-gate.json'
    require(not target.exists(), 'historical gate immutable')
    review = json.loads((R / f'skeptic/{loop}.json').read_text())
    require(review['loop'] == loop and not review['blocking_issues'], 'unresolved blocking review')
    hashes(review['sha256'])
    contract = json.loads((R / f'contracts/{loop}.json').read_text())
    bindings = dict(contract['bindings'])
    bindings.update(review['sha256'])
    inputs = [R / f'contracts/{loop}.json', R / f'contracts/{loop}-freeze.json',
              R / f'skeptic/{loop}.md', R / f'skeptic/{loop}.json']
    for direction in ['forward', 'reverse']:
        work = R / direction / loop
        for mode in ['normal', 'optimized']:
            dest = out / f'{direction}-{mode}'
            cmd = [sys.executable, '-B'] + (['-O'] if mode == 'optimized' else []) + [
                str(work / 'check.py'), '--output', str(dest)]
            result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            (out / f'{direction}-{mode}.log').write_text(result.stdout + result.stderr)
            require(result.returncode == 0, f'producer failed {direction}/{mode}')
            require((dest / 'results.json').read_bytes() == (work / 'output/results.json').read_bytes(),
                    'fresh result differs')
        expected = json.loads((work / 'output/results.json').read_text())
        producer_bindings = producer_inventory(expected)
        if producer_bindings:
            hashes(producer_bindings); bindings.update(producer_bindings)
        inputs.extend(p for p in work.rglob('*') if p.is_file() and p.suffix in ['.py', '.md', '.json'])
    for f in inputs:
        bindings[str(f.relative_to(ROOT))] = digest(f)
    g = {'schema': 'ym26-reviewed-gate-v1', 'loop': loop,
         'verdict': review['verdict'], 'accepted': review['accepted'],
         'limitations': review['limitations'],
         'review': 'separate model-agent skeptic; not external peer review',
         'normal_optimized_equal': True,
         'next_loop_recommendation': review['next_loop_recommendation'],
         'sha256': dict(sorted(bindings.items()))}
    metadata(g, contract, loop); hashes(g['sha256'])
    target.write_text(json.dumps(g, indent=2) + '\n')
    (out / 'receipt.json').write_text(json.dumps({'loop': loop, 'gate_sha256': digest(target),
        'producer_replays': 4, 'status': 'passed'}, indent=2) + '\n')
    print(json.dumps({'loop': loop, 'verdict': g['verdict'], 'bindings': len(bindings)}))


if __name__ == '__main__':
    main()
