"""Validate reviewed Round26 evidence and independently replay its producers.

The replays check reproducibility; the paired reports and skeptical reviews
carry the mathematical arguments. No JSON success flag is a proof.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / 'research/round26'
LOOPS = ['ab1', 'ab2', 'ac1', 'ac2', 'ad1', 'ad2', 'ae1', 'ae2', 'af1', 'af2']


def require(ok, message):
    if not ok:
        raise ValueError(message)


def source(name):
    p = Path(name)
    require(not p.is_absolute() and '..' not in p.parts, 'unsafe source path')
    p = ROOT / p
    require(not any(q.is_symlink() for q in [p, *p.parents] if q != ROOT and q.is_relative_to(ROOT)),
            'linked source path ' + name)
    require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(ROOT),
            'missing source ' + name)
    return p


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def hashes(bindings):
    require(isinstance(bindings, dict) and bool(bindings), 'empty source inventory')
    for name, value in bindings.items():
        require(digest(source(name)) == value, 'changed source ' + name)


def metadata(g, c, loop):
    prefix = 'research/round26/'
    required = {prefix + f'contracts/{loop}.json',
                prefix + f'contracts/{loop}-freeze.json',
                prefix + f'skeptic/{loop}.md', prefix + f'skeptic/{loop}.json'}
    for direction in ['forward', 'reverse']:
        required.update(prefix + f'{direction}/{loop}/' + suffix
                        for suffix in ['report.md', 'check.py', 'output/results.json'])
    require(required <= g.get('sha256', {}).keys(), 'missing required proof or producer binding')
    require(g.get('loop') == loop and c.get('loop') == loop, 'loop identity')
    require(g.get('verdict') in ['limited', 'accepted_within_scope', 'conditional'], 'unsupported verdict')
    require(g.get('normal_optimized_equal') is True, 'interpreter comparison missing')
    require(g.get('review') == 'separate model-agent skeptic; not external peer review', 'review scope')
    require(isinstance(g.get('accepted'), str) and bool(g['accepted'].strip()), 'claim missing')
    require(isinstance(g.get('limitations'), list) and bool(g['limitations'])
            and all(isinstance(x, str) and bool(x.strip()) for x in g['limitations']), 'claim scope missing')
    require(c.get('status') == 'frozen', 'unfrozen contract')
    if loop.endswith('2'):
        first = loop[:-1] + '1'
        required_feedback = {prefix + f'advisor/{first}-gate.json', prefix + f'skeptic/{first}.json'}
        require(required_feedback <= c.get('bindings', {}).keys(), 'second loop lacks frozen review feedback')
    if loop in ['ae1', 'af1']:
        require({prefix + f'advisor/{p}2-gate.json' for p in ['ab', 'ac', 'ad']}
                <= c.get('bindings', {}).keys(), 'final goals selected before first three pairs')


def gate(loop):
    require(loop in LOOPS, 'unknown loop')
    c = json.loads((R / f'contracts/{loop}.json').read_text())
    freeze = json.loads((R / f'contracts/{loop}-freeze.json').read_text())
    g = json.loads((R / f'advisor/{loop}-gate.json').read_text())
    required = {f'research/round26/contracts/{loop}.json', *c['bindings']}
    require(required <= freeze.get('sha256', {}).keys(), 'missing frozen contract input')
    require(set(c['dependencies'] + c['instructions']) <= c['bindings'].keys(), 'missing contract dependency')
    metadata(g, c, loop)
    hashes(c['bindings']); hashes(freeze['sha256']); hashes(g['sha256'])
    review = json.loads((R / f'skeptic/{loop}.json').read_text())
    review_agreement(g, review)
    complete_bindings = dict(g['sha256'])
    repair_path = R / f'advisor/{loop}-inventory-repair.json'
    if repair_path.exists():
        repair = json.loads(repair_path.read_text())
        require(repair['original_gate_sha256'] == digest(R / f'advisor/{loop}-gate.json'), 'repair gate identity')
        require(repair['loop'] == loop and repair['changes_research_claims'] is False, 'repair scope')
        hashes(repair['additional_sha256'])
        complete_bindings.update(repair['additional_sha256'])
    for direction in ['forward', 'reverse']:
        result = json.loads((R / f'{direction}/{loop}/output/results.json').read_text())
        require(isinstance(result, dict) and bool(result), 'missing scientific output')
        bindings = producer_inventory(result)
        require(all(complete_bindings.get(p) == h for p, h in bindings.items()), 'producer source omitted from gate')
    return g


def review_agreement(g, review):
    require(isinstance(review.get('blocking_issues'), list) and not review['blocking_issues'],
            'unresolved or malformed blocking review')
    for key in ['loop', 'verdict', 'accepted', 'limitations', 'next_loop_recommendation']:
        require(g.get(key) == review.get(key), 'gate disagrees with review: ' + key)


def producer_inventory(result):
    keys = [k for k in ['bindings', 'source_inventory', 'sha256'] if k in result]
    require(bool(keys), 'missing executed source inventory')
    joined = {}
    for key in keys:
        bindings = result[key]
        require(isinstance(bindings, dict) and bool(bindings), 'empty executed source inventory')
        for name, value in bindings.items():
            require(name not in joined or joined[name] == value, 'conflicting source inventories')
            joined[name] = value
    return joined


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--optimized', action='store_true')
    p.add_argument('--loops', nargs='+', choices=LOOPS, default=LOOPS)
    a = p.parse_args()
    out = a.output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT), 'fresh external output required')
    out.mkdir(parents=True)
    records = []
    for loop in a.loops:
        g = gate(loop)
        for direction in ['forward', 'reverse']:
            dest = out / f'{loop}-{direction}'
            cmd = [sys.executable, '-B'] + (['-O'] if a.optimized else []) + [
                str(R / f'{direction}/{loop}/check.py'), '--output', str(dest)]
            run = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            (out / f'{loop}-{direction}.log').write_text(run.stdout + run.stderr)
            require(run.returncode == 0, f'producer failure {loop}/{direction}')
            expected = R / f'{direction}/{loop}/output/results.json'
            require((dest / 'results.json').read_bytes() == expected.read_bytes(),
                    f'fresh output differs {loop}/{direction}')
            records.append({'loop': loop, 'direction': direction, 'results_sha256': digest(expected),
                            'gate_sha256': digest(R / f'advisor/{loop}-gate.json')})
    receipt = {'status': 'passed', 'optimized': a.optimized, 'replays': records,
               'new_physics_loops': 0, 'scope': 'source integrity and deterministic replay'}
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': 'passed', 'producer_executions': len(records), 'optimized': a.optimized}))


if __name__ == '__main__':
    main()
