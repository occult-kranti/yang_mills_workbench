#!/usr/bin/env python3
"""Source-bound all-output replay of current Round32 producer packages (skeptic tool).

Usage (repository root): python3 -B research/round32/skeptic/replay_loop.py av1

For each direction the frozen closure (freeze.json) is verified file by file, the
premise inventory is compared with the contract (reverse: exactly AGENTS.md +
contract + shared_premises when reverse_premise_isolation is set; forward: the
same plus forward_additional_premises), every snapshot is compared byte for byte
with its repository source, and check.py is replayed under normal and -O Python
into fresh directories outside the checkout. Every output must equal the frozen
output/ byte for byte. Failures are explicit exceptions, never assert.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import platform
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ROUND = 'research/round32'


class ReplayError(Exception):
    pass


def fail(message):
    raise ReplayError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_path(base, name):
    parsed = PurePosixPath(name)
    if parsed.is_absolute() or '..' in parsed.parts:
        fail('unsafe source path: ' + name)
    cur = base
    for part in parsed.parts:
        cur = cur / part
        if cur.is_symlink():
            fail('symlink in source closure: ' + str(cur))
    if not cur.is_file():
        fail('missing source: ' + name)
    return cur


def contract_for(loop):
    path = ROOT / ROUND / 'contracts' / (loop + '.json')
    data = json.loads(path.read_text())
    if data.get('status') != 'frozen_before_production' or str(data.get('id', '')).lower() != loop:
        fail('contract not frozen or wrong identity: ' + loop)
    return path, data


def verify_freeze(src, loop):
    cur = ROOT
    for part in src.relative_to(ROOT).parts:
        cur = cur / part
        if cur.is_symlink():
            fail('symlink producer directory')
    if (src / 'freeze.json').is_symlink():
        fail('symlink freeze')
    freeze = json.loads((src / 'freeze.json').read_text())
    if freeze.get('loop') != loop.upper() or freeze.get('direction') != src.parent.name:
        fail('wrong freeze identity: ' + str(src))
    contract_path, contract = contract_for(loop)
    if freeze.get('contract_sha256') != sha(contract_path):
        fail('contract changed after freeze')
    sources = freeze.get('sources')
    if not isinstance(sources, dict) or not sources:
        fail('missing frozen file map')
    prefix = src.relative_to(ROOT).as_posix() + '/'
    if any(not name.startswith(prefix) for name in sources):
        fail('freeze source outside producer ownership')
    files = {name[len(prefix):]: digest for name, digest in sources.items()}
    actual = {p.relative_to(src).as_posix() for p in src.rglob('*') if p.is_file() and p != src / 'freeze.json'}
    if any('__pycache__' in n or n.endswith('.pyc') for n in actual):
        fail('interpreter artifact in source closure')
    if set(files) != actual:
        fail('frozen closure mismatch: ' + str(sorted(set(files) ^ actual)))
    for name, digest in files.items():
        if sha(safe_path(src, name)) != digest:
            fail('frozen digest mismatch: ' + name)
    rel_contract = contract_path.relative_to(ROOT).as_posix()
    expected = {'AGENTS.md', rel_contract} | set(contract.get('shared_premises', []))
    if src.parent.name == 'forward':
        expected |= set(contract.get('forward_additional_premises', []))
    inventory = {p.relative_to(src / 'inputs').as_posix() for p in (src / 'inputs').rglob('*') if p.is_file()}
    isolation = src.parent.name == 'reverse' and contract.get('reverse_premise_isolation') is True
    if isolation and inventory != expected:
        fail('reverse premise isolation violated: ' + str(sorted(inventory ^ expected)))
    if not expected <= inventory:
        fail('declared premise snapshot missing: ' + str(sorted(expected - inventory)))
    for name in sorted(expected):
        if safe_path(src, 'inputs/' + name).read_bytes() != safe_path(ROOT, name).read_bytes():
            fail('changed premise snapshot: ' + name)
    for required in ('check.py', 'report.md', 'output/results.json', 'inputs/AGENTS.md'):
        if required not in files:
            fail('required source absent: ' + required)
    return {'closure_files': len(files), 'inputs': len(inventory), 'declared_premises': len(expected),
            'inventory_equals_declared': inventory == expected, 'reverse_isolation_enforced': isolation}


def replay(loop):
    receipts = []
    closures = {}
    for direction in ('forward', 'reverse'):
        src = ROOT / ROUND / direction / loop
        closures[direction] = verify_freeze(src, loop)
        before = sha(src / 'freeze.json')
        expected = {p.relative_to(src / 'output').as_posix(): p.read_bytes()
                    for p in (src / 'output').rglob('*') if p.is_file()}
        if not expected:
            fail('no expected outputs')
        for mode in ('normal', 'optimized'):
            with tempfile.TemporaryDirectory(prefix='hnm-r32-%s-%s-%s-' % (loop, direction, mode)) as temporary:
                out = Path(temporary) / 'output'
                if ROOT in out.resolve().parents:
                    fail('replay directory inside the checkout')
                cmd = [sys.executable, '-B'] + (['-O'] if mode == 'optimized' else []) + [str(src / 'check.py'), '--output', str(out)]
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
                if result.returncode != 0:
                    fail('%s/%s/%s replay failed: %s' % (loop, direction, mode, result.stderr[-2000:]))
                actual = {p.relative_to(out).as_posix(): p.read_bytes() for p in out.rglob('*') if p.is_file()}
                if actual != expected:
                    bad = sorted(n for n in set(actual) | set(expected) if actual.get(n) != expected.get(n))
                    fail('%s/%s/%s changed outputs: %s' % (loop, direction, mode, bad))
                receipts.append({
                    'direction': direction, 'mode': mode,
                    'command': ['python3', '-B'] + (['-O'] if mode == 'optimized' else [])
                               + [(src / 'check.py').relative_to(ROOT).as_posix(), '--output', '<fresh-external-dir>'],
                    'outputs': {n: hashlib.sha256(b).hexdigest() for n, b in sorted(actual.items())},
                    'byte_identical_to_frozen_output': True,
                    'stdout': result.stdout.strip().replace(str(out), '<fresh-external-dir>')})
        closures[direction]['freeze_json_sha256'] = before
        verify_freeze(src, loop)
        if sha(src / 'freeze.json') != before:
            fail('freeze changed during replay')
    return {'loop': loop.upper(), 'python': platform.python_version(), 'closures': closures, 'replays': receipts}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: replay_loop.py <loop>')
    print(json.dumps(replay(sys.argv[1].lower()), indent=2, sort_keys=True))
