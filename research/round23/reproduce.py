#!/usr/bin/env python3
"""Fresh source replay of selected reviewed Round23 loops, including optimized Python."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
from admission import ROOT, LOOPS, digest, gate, payload, read, require, source, unlinked


def run(args, log):
    completed = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(completed.stdout+completed.stderr)
    require(completed.returncode == 0, 'replay failed: '+str(log))


def replay(loop, direction, target, g, flags):
    prefix = f'research/round23/{direction}/{loop}/'
    run([sys.executable, *flags, str(source(prefix+'check.py')), '--output', str(target)],
        target.parent/(direction+'.log'))
    expected = {p[len(prefix+'output/'):]:h for p,h in g['files'].items()
                if p.startswith(prefix+'output/')}
    actual = {str(p.relative_to(target)) for p in target.rglob('*') if p.is_file()}
    require(actual == set(expected), 'fresh output inventory drift: '+loop+'/'+direction)
    for name, sha in expected.items():
        p = unlinked(target/name)
        require(digest(p) == sha and p.read_bytes() == source(prefix+'output/'+name).read_bytes(),
                'fresh output content drift: '+loop+'/'+direction+'/'+name)
    payload(read(target/'results.json'), loop, direction, g['expected_results'][direction])
    return {'loop':loop, 'direction':direction, 'source_sha256':digest(source(prefix+'check.py')),
            'result_sha256':digest(target/'results.json'), 'outputs_compared':len(expected)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--loops', nargs='+')
    parser.add_argument('--optimized', action='store_true')
    args = parser.parse_args()
    output = unlinked(args.output.absolute())
    require(not output.exists() and ROOT not in output.parents, 'choose a fresh external output directory')
    loops = args.loops or list(LOOPS)
    require(bool(loops) and len(loops) == len(set(loops)), 'empty or duplicate loop list')
    gates = {loop:gate(loop) for loop in loops}
    hashes = {loop:digest(source(f'research/round23/advisor/{loop}-gate.json')) for loop in loops}
    output.mkdir(parents=True)
    flags = ['-B'] + (['-O'] if args.optimized else [])
    rows = []
    for loop, g in gates.items():
        for direction in ('forward', 'reverse'):
            rows.append(replay(loop, direction, output/loop/direction, g, flags))
        gate(loop)
        require(hashes[loop] == digest(source(f'research/round23/advisor/{loop}-gate.json')),
                'gate changed during replay')
    result = {'status':'passed', 'loops':loops, 'optimized':args.optimized, 'executions':rows,
              'admitted_gates':hashes, 'research_loops_added':0,
              'scope':'Byte-exact source replay supports recorded checks; mathematical proofs require the bound skeptical reviews.'}
    (output/'reproduction.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','loops':len(loops),'producer_executions':len(rows)}))


if __name__ == '__main__':
    main()
