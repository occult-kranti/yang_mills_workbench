"""Shared I/O only for the explicitly single-agent T2 formulations."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = 'research/round23/contracts/t2.json'
CONTRACT_SHA = '1101076213d09b08cea5f0b7e817bced95d0a79ae54bd51c65aae98fd0cd1b6d'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')


def emit(direction, results, controls):
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output
    need(out.is_absolute() and not out.exists(), 'fresh absolute output required')
    for p in (out, *out.parents):
        need(not p.is_symlink(), 'symlink output refused')
    need(digest(ROOT/CONTRACT) == CONTRACT_SHA, 'frozen T2 contract changed')
    contract = json.loads((ROOT/CONTRACT).read_text())
    for name, expected in contract['dependencies'].items():
        need(digest(ROOT/name) == expected, 'inherited dependency changed: '+name)
    base = 'research/round23/'+direction+'/t2/'
    names = set(contract['dependencies']) | set(contract['instruction_inputs']) | {
        CONTRACT, base+'check.py', base+'report.md', 'research/round23/t2_common.py',
        'research/round23/methods/t2-solo-override.md', 'research/round23/sources/t2-reading.md'}
    inputs = {n:digest(ROOT/n) for n in sorted(names)}
    shared = {'loop':'t2', 'direction':direction, 'passed':True,
              'execution_mode':'single-agent-correlated-formulations',
              'independent_agent_review':False}
    results = {**shared, 'schema':'ym23-producer-results-v1',
               'status':'checks_passed_centered_bound', **results}
    controls = {**shared, 'schema':'ym23-producer-controls-v1',
                'status':'discriminating_controls_passed', **controls}
    out.mkdir(parents=True)
    save(out/'results.json', results)
    save(out/'controls.json', controls)
    save(out/'source-manifest.json', {'schema':'ym23-producer-source-manifest-v1',
        'loop':'t2', 'direction':direction, 'inputs':inputs,
        'outputs':{n:digest(out/n) for n in ('results.json','controls.json')}})
    print(json.dumps({'loop':'t2','direction':direction,'passed':True}))
