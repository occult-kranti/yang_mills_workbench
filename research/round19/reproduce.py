#!/usr/bin/env python3
"""Replay the declared Round19 scientific commands in a fresh output directory.

Gate hashes establish which sources were reviewed; fresh forward and independent
calculations establish reproducibility. Neither substitutes for the written proofs.
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
LOOPS = ('a1', 'a2', 'b1', 'b2', 'c1', 'c2')

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def checked_path(relative):
    p = HERE / relative
    if Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise ValueError('nonlocal gate path: ' + relative)
    if p.is_symlink() or any(x.is_symlink() for x in p.parents if x != HERE.parent):
        raise ValueError('symlink gate path: ' + relative)
    if not p.is_file():
        raise ValueError('missing gate file: ' + relative)
    return p

def verify_gate(loop):
    gate_path = HERE / 'advisor' / (loop + '-gate.json')
    gate = json.loads(gate_path.read_text())
    if gate.get('loop') != loop or gate.get('status') not in ('accepted', 'limited'):
        raise ValueError('unadmitted loop: ' + loop)
    files = gate.get('files')
    if not isinstance(files, dict) or not files:
        raise ValueError('missing reviewed inventory: ' + loop)
    for name, expected in files.items():
        if not isinstance(expected, str) or len(expected) != 64 or digest(checked_path(name)) != expected:
            raise ValueError('stale reviewed file: ' + name)
    return gate

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--optimized', action='store_true')
    ap.add_argument('--through', choices=LOOPS, default='c2')
    ap.add_argument('--from-loop', choices=LOOPS, default='a1', help='Replay only this loop onward; still verify all earlier reviewed gates')
    args = ap.parse_args()
    out = args.output.resolve()
    if out.exists() or HERE == out or HERE in out.parents:
        raise ValueError('choose a new output directory outside research/round19')
    start, end = LOOPS.index(args.from_loop), LOOPS.index(args.through)+1
    if start >= end:
        raise ValueError('--from-loop must not follow --through')
    dependencies = LOOPS[:end]
    selected = LOOPS[start:end]
    specifications = json.loads((HERE / 'execution.json').read_text())
    if tuple(specifications['order']) != LOOPS:
        raise ValueError('unexpected loop order')
    gates = {loop: verify_gate(loop) for loop in dependencies}
    out.mkdir(parents=True)
    executions = []
    flags = ['-B'] + (['-O'] if args.optimized else [])
    for loop in selected:
        spec = specifications['loops'][loop]
        for task in spec['tasks']:
            name = task['name']
            target = out / loop / name
            script = checked_path(task['script'])
            argv = [sys.executable, *flags, str(script)]
            argv += [s.replace('{output}', str(target)).replace('{run_root}', str(out)).replace('{round_root}', str(HERE)) for s in task['args']]
            process = subprocess.run(argv, cwd=HERE.parent.parent, text=True, capture_output=True)
            (out / loop).mkdir(exist_ok=True)
            (out / loop / (name + '.log')).write_text(process.stdout + process.stderr)
            if process.returncode:
                raise RuntimeError(loop + '/' + name + ' failed; see saved log')
            comparisons = []
            for relative in task.get('identical_files', []):
                expected = checked_path(task['accepted_output'] + '/' + relative)
                actual = target / relative
                same = actual.is_file() and actual.read_bytes() == expected.read_bytes()
                comparisons.append({'file':relative, 'identical':same})
                if not same:
                    raise ValueError('replay differs: ' + loop + '/' + name + '/' + relative)
            for result_name, field, allowed in task.get('semantic_gates', []):
                data = json.loads((target / result_name).read_text())
                if data.get(field) not in allowed:
                    raise ValueError('semantic replay failed: ' + loop + '/' + name)
            if not comparisons and not task.get('semantic_gates'):
                raise ValueError('execution has no evidence check: ' + name)
            executions.append({'loop':loop,'task':name,'status':'passed','comparisons':comparisons})
        verify_gate(loop)
    result = {'status':'passed','loops_replayed':list(selected),'reviewed_gate_dependencies':list(dependencies),'optimized':args.optimized,'repeat_counting':'optimized execution is not an additional research loop or independent formulation','executions':executions}
    (out / 'reproduction.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status':'passed','loops':len(selected),'executions':len(executions)}))

if __name__ == '__main__':
    main()
