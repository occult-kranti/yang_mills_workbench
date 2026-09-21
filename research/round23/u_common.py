"""I/O only for the explicitly correlated U formulations; no physics calculations."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, obj):
    p.write_text(json.dumps(obj, indent=2, sort_keys=True)+'\n')


def emit(loop, direction, contract_sha, results, controls):
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    out = parser.parse_args().output
    need(out.is_absolute() and not out.exists(), 'fresh absolute output required')
    need(not any(p.is_symlink() for p in (out, *out.parents)), 'symlink output refused')
    name = f'research/round23/contracts/{loop}.json'
    need(digest(ROOT/name) == contract_sha, 'frozen contract changed')
    c = json.loads((ROOT/name).read_text())
    for n, h in c['dependencies'].items():
        need(digest(ROOT/n) == h, 'inherited source changed: '+n)
    base = f'research/round23/{direction}/{loop}/'
    names = set(c['dependencies']) | set(c['instruction_inputs']) | {
        name, base+'report.md', base+'check.py', 'research/round23/u_common.py'}
    shared = dict(loop=loop, direction=direction, passed=True,
                  execution_mode='single-agent-correlated-formulations',
                  independent_agent_review=False)
    out.mkdir(parents=True)
    save(out/'results.json', dict(shared, schema='ym23-producer-results-v1', **results))
    save(out/'controls.json', dict(shared, schema='ym23-producer-controls-v1',
                                  status='discriminating_controls_passed', **controls))
    save(out/'source-manifest.json', dict(schema='ym23-producer-source-manifest-v1',
         loop=loop, direction=direction, inputs={n:digest(ROOT/n) for n in sorted(names)},
         outputs={n:digest(out/n) for n in ('results.json','controls.json')}))
    print(json.dumps(dict(loop=loop, direction=direction, passed=True)))
