#!/usr/bin/env python3
"""Round33 producer protocol helper: snapshot premises, freeze closures, verify replays.

Usage (from the repository root):
  python3 -B research/round33/tools/freeze.py snapshot research/round33/forward/av1
  python3 -B research/round33/tools/freeze.py freeze   research/round33/forward/av1 --verdict "..."
  python3 -B research/round33/tools/freeze.py verify   research/round33/forward/av1

`snapshot` copies AGENTS.md, the loop contract and every contract `shared_premises`
path byte-for-byte into <producer>/inputs/<repo-relative path>.
`freeze` runs check.py twice (normal and -O) into fresh external directories,
requires byte-identical outputs matching <producer>/output/, then writes
freeze.json binding every file in the producer directory except freeze.json.
`verify` re-checks freeze.json, snapshots and replays.

This is infrastructure shared by all producers; it computes no scientific result.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROUND = 'research/round33'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message):
    raise SystemExit('freeze.py: ' + message)


def producer_dir(value):
    p = (ROOT / value).resolve()
    rel = p.relative_to(ROOT).as_posix()
    parts = rel.split('/')
    if len(parts) != 4 or parts[0] != 'research' or parts[1] != 'round33' or parts[2] not in ('forward', 'reverse'):
        fail('producer must be research/round33/<forward|reverse>/<loop>: ' + rel)
    if not p.is_dir():
        fail('missing producer directory ' + rel)
    return p, parts[2], parts[3]


def contract_for(loop):
    path = ROOT / ROUND / 'contracts' / (loop + '.json')
    if not path.is_file():
        fail('missing contract ' + str(path.relative_to(ROOT)))
    data = json.loads(path.read_text())
    if data.get('status') != 'frozen_before_production':
        fail('contract is not frozen_before_production')
    if str(data.get('id', '')).lower() != loop:
        fail('contract id mismatch')
    return path, data


def inventory(directory, skip=()):
    files = {}
    for p in sorted(directory.rglob('*')):
        if not p.is_file():
            continue
        if '__pycache__' in p.parts or p.suffix == '.pyc':
            fail('interpreter cache inside closure: ' + str(p))
        rel = p.relative_to(ROOT).as_posix()
        if p.name in skip and p.parent == directory:
            continue
        files[rel] = sha(p)
    return files


def snapshot(p, loop):
    contract_path, contract = contract_for(loop)
    names = ['AGENTS.md', contract_path.relative_to(ROOT).as_posix()] + list(contract.get('shared_premises', []))
    if p.parent.name == 'forward':
        names += list(contract.get('forward_additional_premises', []))
    copied = []
    for name in dict.fromkeys(names):
        src = ROOT / name
        if not src.is_file() or Path(name).is_absolute() or '..' in Path(name).parts:
            fail('missing or unsafe premise ' + name)
        dst = p / 'inputs' / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        copied.append(name)
    print(json.dumps({'status': 'snapshotted', 'files': len(copied)}))


def replay(p, optimized):
    with tempfile.TemporaryDirectory(prefix='hnm-r32-freeze-') as tmp:
        target = Path(tmp) / 'out'
        cmd = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(p / 'check.py'), '--output', str(target)]
        done = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        if done.returncode != 0:
            fail(('optimized ' if optimized else 'normal ') + 'replay failed:\n' + done.stderr[-4000:])
        produced = {q.relative_to(target).as_posix(): sha(q) for q in sorted(target.rglob('*')) if q.is_file()}
    return produced


def check_snapshots(p, loop):
    contract_path, contract = contract_for(loop)
    names = ['AGENTS.md', contract_path.relative_to(ROOT).as_posix()] + list(contract.get('shared_premises', []))
    if p.parent.name == 'forward':
        names += list(contract.get('forward_additional_premises', []))
    if p.parent.name == 'reverse' and contract.get('reverse_premise_isolation'):
        actual = {q.relative_to(p / 'inputs').as_posix() for q in (p / 'inputs').rglob('*') if q.is_file()}
        if actual != set(names):
            fail('reverse premise isolation violated: ' + json.dumps(sorted(actual ^ set(names))[:6]))
    for name in dict.fromkeys(names):
        snap = p / 'inputs' / name
        if not snap.is_file() or snap.read_bytes() != (ROOT / name).read_bytes():
            fail('missing or changed premise snapshot ' + name)


def freeze(p, direction, loop, verdict):
    for required in ('check.py', 'report.md', 'output/results.json', 'inputs/AGENTS.md'):
        if not (p / required).is_file():
            fail('missing required producer file ' + required)
    check_snapshots(p, loop)
    frozen = {q.relative_to(p / 'output').as_posix(): sha(q) for q in sorted((p / 'output').rglob('*')) if q.is_file()}
    normal = replay(p, False)
    optimized = replay(p, True)
    if normal != frozen:
        fail('normal replay differs from frozen output: ' + json.dumps(sorted(set(normal) ^ set(frozen)) or [k for k in frozen if normal.get(k) != frozen[k]]))
    if optimized != frozen:
        fail('optimized replay differs from frozen output')
    results = json.loads((p / 'output/results.json').read_text())
    checks = results.get('checks')
    if not isinstance(checks, list) or not checks or not all(isinstance(c, dict) and c.get('passed') is True and isinstance(c.get('id'), str) for c in checks):
        fail('results.json must contain a non-empty checks list with passed:true entries')
    ids = [c['id'] for c in checks]
    if len(ids) != len(set(ids)):
        fail('duplicate check ids')
    data = {
        'loop': loop.upper(), 'direction': direction,
        'contract_sha256': sha(ROOT / ROUND / 'contracts' / (loop + '.json')),
        'independent_before_current_counterpart_exchange': True,
        'normal_optimized_identical': True,
        'verdict': verdict,
        'sources': inventory(p, skip=('freeze.json',)),
    }
    (p / 'freeze.json').write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'frozen', 'loop': loop, 'direction': direction, 'files': len(data['sources']), 'checks': len(ids)}))


def verify(p, direction, loop):
    fz = json.loads((p / 'freeze.json').read_text())
    if fz.get('loop') != loop.upper() or fz.get('direction') != direction:
        fail('freeze identity mismatch')
    if fz.get('contract_sha256') != sha(ROOT / ROUND / 'contracts' / (loop + '.json')):
        fail('contract changed after freeze')
    actual = inventory(p, skip=('freeze.json',))
    if actual != fz.get('sources'):
        fail('closure differs from freeze.json: ' + json.dumps(sorted(set(actual) ^ set(fz.get('sources', {})))[:10]))
    check_snapshots(p, loop)
    frozen = {q.relative_to(p / 'output').as_posix(): sha(q) for q in sorted((p / 'output').rglob('*')) if q.is_file()}
    if replay(p, False) != frozen or replay(p, True) != frozen:
        fail('replay differs from frozen output')
    print(json.dumps({'status': 'verified', 'loop': loop, 'direction': direction}))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('mode', choices=('snapshot', 'freeze', 'verify'))
    ap.add_argument('producer')
    ap.add_argument('--verdict', default='')
    a = ap.parse_args()
    p, direction, loop = producer_dir(a.producer)
    if a.mode == 'snapshot':
        snapshot(p, loop)
    elif a.mode == 'freeze':
        if not a.verdict:
            fail('--verdict text required')
        freeze(p, direction, loop, a.verdict)
    else:
        verify(p, direction, loop)


if __name__ == '__main__':
    main()
