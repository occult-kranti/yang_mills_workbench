#!/usr/bin/env python3
"""Replay exactly the producer directions a Round32 contract declares (skeptic tool).

Usage (repository root): python3 -B research/round32/skeptic/replay_declared.py aw2

This reuses replay_loop.py unchanged (its sha256 e627df04... is recorded in the
AV1, AV2 and AW1 skeptic bindings, so it is imported, not edited). replay_loop.py
always replays forward and reverse; a single-direction contract
(producers=["forward"], direction "single+skeptic") has no reverse package, so
this wrapper takes the direction list from the contract's `producers` field,
requires that no undeclared direction package exists, and then applies the same
steps per declared direction: replay_loop.verify_freeze (closure, digests,
snapshots against their repository sources), check.py under normal and -O Python
into fresh temporary directories outside the checkout with byte-for-byte
comparison against output/, a second verify_freeze, and
`tools/freeze.py verify`. Failures are explicit exceptions, never assert.
"""
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import replay_loop as base  # noqa: E402  (unchanged shared tool)

ROOT = base.ROOT
ROUND = base.ROUND
DIRECTIONS = ('forward', 'reverse')


def declared_directions(loop):
    _, contract = base.contract_for(loop)
    producers = contract.get('producers', list(DIRECTIONS))
    if producers not in (['forward', 'reverse'], ['forward'], ['reverse']):
        base.fail('unknown producer set: ' + repr(producers))
    if producers != ['forward', 'reverse']:
        if contract.get('direction') != 'single+skeptic' or contract.get('single_direction_independent_replay') is not True:
            base.fail('single-direction contract without a declared independent skeptic replay')
    for direction in DIRECTIONS:
        present = (ROOT / ROUND / direction / loop).exists()
        if direction not in producers and present:
            base.fail('undeclared %s package present for a single-direction loop' % direction)
        if direction in producers and not present:
            base.fail('declared %s package missing' % direction)
    return producers


def replay(loop):
    producers = declared_directions(loop)
    receipts, closures, freeze_verify, frozen_outputs = [], {}, [], {}
    for direction in producers:
        src = ROOT / ROUND / direction / loop
        closures[direction] = base.verify_freeze(src, loop)
        before = base.sha(src / 'freeze.json')
        expected = {p.relative_to(src / 'output').as_posix(): p.read_bytes()
                    for p in (src / 'output').rglob('*') if p.is_file()}
        if not expected:
            base.fail('no expected outputs')
        frozen_outputs[direction] = {n: hashlib.sha256(b).hexdigest() for n, b in sorted(expected.items())}
        for mode in ('normal', 'optimized'):
            with tempfile.TemporaryDirectory(prefix='hnm-r32-%s-%s-%s-' % (loop, direction, mode)) as temporary:
                out = Path(temporary) / 'output'
                if ROOT in out.resolve().parents:
                    base.fail('replay directory inside the checkout')
                cmd = [sys.executable, '-B'] + (['-O'] if mode == 'optimized' else []) + [str(src / 'check.py'), '--output', str(out)]
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
                if result.returncode != 0:
                    base.fail('%s/%s/%s replay failed: %s' % (loop, direction, mode, result.stderr[-2000:]))
                actual = {p.relative_to(out).as_posix(): p.read_bytes() for p in out.rglob('*') if p.is_file()}
                if actual != expected:
                    bad = sorted(n for n in set(actual) | set(expected) if actual.get(n) != expected.get(n))
                    base.fail('%s/%s/%s changed outputs: %s' % (loop, direction, mode, bad))
                receipts.append({
                    'direction': direction, 'mode': mode,
                    'command': ['python3', '-B'] + (['-O'] if mode == 'optimized' else [])
                               + [(src / 'check.py').relative_to(ROOT).as_posix(), '--output', '<fresh-external-dir>'],
                    'outputs': {n: hashlib.sha256(b).hexdigest() for n, b in sorted(actual.items())},
                    'byte_identical_to_frozen_output': True,
                    'stdout': result.stdout.strip().replace(str(out), '<fresh-external-dir>')})
        tool = [sys.executable, '-B', str(ROOT / ROUND / 'tools/freeze.py'), 'verify', src.relative_to(ROOT).as_posix()]
        done = subprocess.run(tool, capture_output=True, text=True, cwd=str(ROOT))
        if done.returncode != 0:
            base.fail('freeze.py verify failed for %s: %s' % (direction, done.stderr[-2000:]))
        freeze_verify.append({'command': 'python3 -B research/round32/tools/freeze.py verify ' + src.relative_to(ROOT).as_posix(),
                              'stdout': json.loads(done.stdout.strip().splitlines()[-1])})
        closures[direction]['freeze_json_sha256'] = before
        base.verify_freeze(src, loop)
        if base.sha(src / 'freeze.json') != before:
            base.fail('freeze changed during replay')
    return {'loop': loop.upper(), 'python': platform.python_version(), 'producers': producers,
            'closures': closures, 'frozen_outputs': frozen_outputs, 'freeze_verify': freeze_verify,
            'producer_replays': receipts,
            'tool': 'research/round32/skeptic/replay_declared.py',
            'tool_sha256': base.sha(Path(__file__).resolve()),
            'reused_tool': 'research/round32/skeptic/replay_loop.py',
            'reused_tool_sha256': base.sha(HERE / 'replay_loop.py')}


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: replay_declared.py <loop>')
    print(json.dumps(replay(sys.argv[1].lower()), indent=2, sort_keys=True))
