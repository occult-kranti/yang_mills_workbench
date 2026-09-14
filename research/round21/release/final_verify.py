#!/usr/bin/env python3
"""Round21 final release verification; candidate creation is a separate command.

No research sources, gates, expected outputs or legacy repair files are modified.
All generated files must be outside the source tree. See the companion protocol.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

# Preflight imports trusted source modules but must never write interpreter
# caches into the release, even if the caller omitted Python's -B flag.
sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LOOPS = tuple(letter + number for letter in 'ijklm' for number in '12')
INVENTORY_LOCATION = 'research/round21/release/final-inventory.json'
SCHEMA = 'ym21-final-release-inventory-v1'
TREES = ('research/round21', '.codex/skills', 'scripts', 'tests', 'dist', 'docs')
FIXED = ('AGENTS.md', 'README.md', 'package.json', 'research/round21/reproduce.py',
         'research/round21/release/final_verify.py',
         'research/round21/release/final-verification-protocol.md')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON object key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=no_duplicate_keys)


def unlinked(path):
    for part in (path, *path.parents):
        require(not part.is_symlink(), 'symlink path component: ' + str(part))
    return path


def relative_name(name):
    require(type(name) is str and bool(name), 'empty or nonstring path')
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts and '.' not in path.parts,
            'unsafe relative path: ' + name)
    require(str(path) == name and '\\' not in name, 'noncanonical relative path: ' + name)
    require('__pycache__' not in path.parts and path.suffix not in ('.pyc', '.pyo'),
            'interpreter cache cannot enter release inventory')
    return name


def source(name):
    path = unlinked(ROOT / relative_name(name))
    require(path.is_file(), 'missing release source: ' + name)
    return path


def fresh_external(path):
    lexical = unlinked(path.absolute())
    resolved = lexical.resolve()
    require(resolved != ROOT and ROOT not in resolved.parents, 'output must be outside source tree')
    require(not resolved.exists(), 'output must be fresh: ' + str(resolved))
    return resolved


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def ledger_check(ledger):
    require(type(ledger) is dict and ledger.get('schema') == 'ym21-execution-v1', 'wrong execution schema')
    completed = ledger.get('completed_loops')
    require(type(completed) is list and all(type(n) is str for n in completed), 'malformed completed loops')
    require(len(completed) == len(set(completed)), 'duplicate completed loops')
    missing = sorted(set(LOOPS) - set(completed))
    extra = sorted(set(completed) - set(LOOPS))
    require(len(completed) == 10 and not missing and not extra,
            'exactly ten admitted loops required; missing=' + ','.join(missing) + '; extra=' + ','.join(extra))
    require(type(ledger.get('planned_research_loops')) is int and ledger['planned_research_loops'] == 10,
            'planned research loop count must be integer ten')
    require(ledger.get('repairs_count_as_research_loops') is False, 'repair executions cannot count as research loops')
    return ledger


def preflight():
    ledger = ledger_check(read_json(source('research/round21/execution.json')))
    admitted = set()
    for path in (ROOT / 'research/round21/advisor').glob('*-gate.json'):
        match = re.fullmatch(r'([a-z][12])-gate\.json', path.name)
        if match:
            data = read_json(unlinked(path))
            if data.get('status') in ('accepted', 'limited'):
                admitted.add(match.group(1))
    require(admitted == set(LOOPS), 'admitted gate set differs from the ten-loop contract')
    reproduce = module('ym21_final_reproduce', source('research/round21/reproduce.py'))
    gates = {}
    for loop in LOOPS:
        gates[loop] = reproduce.gate(loop)
        # Parse the key trust-boundary files strictly, in addition to the replay's
        # input/output-closure and dependency validation.
        read_json(source('research/round21/advisor/' + loop + '-gate.json'))
        for direction in ('forward', 'reverse'):
            read_json(source('research/round21/' + direction + '/' + loop + '/output/source-manifest.json'))
    repair = module('ym21_final_c2_repair', source('research/round21/release/replay_c2.py'))
    c2 = repair.validate_inventory(ROOT, source('research/round21/release/reviewed-inventory.json'))
    return ledger, gates, c2


def collect_files(gates, c2):
    names = set(FIXED)
    for tree in TREES:
        directory = unlinked(ROOT / tree)
        require(directory.is_dir(), 'missing inventory tree: ' + tree)
        for path in directory.rglob('*'):
            unlinked(path)
            if path.is_file():
                name = str(path.relative_to(ROOT))
                if name != INVENTORY_LOCATION:
                    names.add(relative_name(name))
    for data in gates.values():
        names.update(data['files'])
    names.update(c2['files'])
    return {name: sha(source(name)) for name in sorted(names)}


def inventory_candidate():
    ledger, gates, c2 = preflight()
    return {'schema': SCHEMA, 'review_status': 'candidate_requires_external_digest_review',
            'loops': list(LOOPS), 'base_commit': ledger['base_commit'],
            'excluded_self_referential_path': INVENTORY_LOCATION,
            'infrastructure_trees': list(TREES),
            'files': collect_files(gates, c2),
            'trust': 'External reviewed SHA-256 required by verify; this file is not a signature or its own admission.'}


def check_inventory(path, expected_digest):
    require(type(expected_digest) is str and re.fullmatch('[0-9a-f]{64}', expected_digest), 'invalid reviewed inventory digest')
    unlinked(path.absolute())
    require(sha(path) == expected_digest, 'reviewed final inventory digest mismatch')
    data = read_json(path)
    require(data.get('schema') == SCHEMA and data.get('loops') == list(LOOPS), 'wrong final inventory schema or loop set')
    require(data.get('excluded_self_referential_path') == INVENTORY_LOCATION, 'unreviewed inventory exclusion')
    require(data.get('infrastructure_trees') == list(TREES), 'inventory infrastructure roots changed')
    files = data.get('files')
    require(type(files) is dict and bool(files), 'empty release inventory')
    for name, wanted in files.items():
        relative_name(name)
        require(type(wanted) is str and re.fullmatch('[0-9a-f]{64}', wanted), 'invalid release digest')
    ledger, gates, c2 = preflight()
    require(data.get('base_commit') == ledger['base_commit'], 'base commit mismatch')
    actual = collect_files(gates, c2)
    require(set(files) == set(actual), 'release inventory is incomplete or has unexpected files')
    drift = [name for name in actual if files[name] != actual[name]]
    require(not drift, 'release source bytes changed: ' + ','.join(drift[:8]))
    return data, ledger


def run(command, log, cwd=ROOT):
    log.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    log.write_text(proc.stdout + proc.stderr)
    require(proc.returncode == 0, 'command failed; see ' + str(log))
    return {'command': command, 'returncode': proc.returncode, 'log_sha256': sha(log)}


def check_reproduction(path, optimized):
    record = read_json(path / 'reproduction.json')
    require(record.get('status') == 'passed' and record.get('loops') == list(LOOPS), 'full replay did not pass all ten loops')
    require(record.get('optimized') is optimized and record.get('pair_comparisons') == 10, 'replay mode or comparison count wrong')
    rows = record.get('executions')
    require(type(rows) is list and len(rows) == 20, 'replay did not execute twenty producers')
    require({(r.get('loop'), r.get('direction')) for r in rows} ==
            {(n, d) for n in LOOPS for d in ('forward', 'reverse')}, 'missing or repeated scientific execution')
    return record


def historical_base_check(ledger, out):
    require((ROOT / '.git').exists() and shutil.which('git'), 'base comparison requires a Git checkout; omit --check-base for an archive')
    base = ledger['base_commit']
    require(re.fullmatch('[0-9a-f]{40}', base), 'invalid historical base commit')
    record = run(['git', 'diff', '--exit-code', base, '--', 'research/round19', 'research/round20'], out / 'historical-base.log')
    proc = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard', '--', 'research/round19', 'research/round20'],
                          cwd=ROOT, text=True, capture_output=True)
    require(proc.returncode == 0 and not proc.stdout.strip(), 'untracked historical files prevent an unchanged-history claim')
    return {'status': 'passed', 'base_commit': base, 'command': record}


def site_check(data, out, tests):
    # The existing builder has a fixed ROOT/docs destination; run its actual
    # source in a complete bound-file mirror outside the source tree.
    mirror = out / 'site-work'
    for name in data['files']:
        target = mirror / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source(name), target)
    require('research/round21/build_site.py' in data['files'], 'Round21 renderer is not bound')
    round21_build = run([sys.executable, '-B', str(mirror / 'research/round21/build_site.py')],
                       out / 'round21-site-build.log', mirror)
    rendered = read_json(out / 'round21-site-build.log')
    require(type(rendered.get('loops')) is int and rendered['loops'] == 10 and
            type(rendered.get('verified')) is int and rendered['verified'] == 10,
            'Round21 renderer did not source-verify all ten displayed loops')
    for asset in ('dist/research-round21.js', 'dist/research-round21.css', 'dist/index.html'):
        require(asset in data['files'] and (mirror / asset).is_file(), 'required Round21 site asset missing: ' + asset)
        require(sha(mirror / asset) == data['files'][asset], 'Round21 rendering differs from bound asset: ' + asset)
    expected_dist = {name[len('dist/'):]: wanted for name, wanted in data['files'].items() if name.startswith('dist/')}
    actual_dist = {str(p.relative_to(mirror / 'dist')): sha(p) for p in (mirror / 'dist').rglob('*') if p.is_file()}
    require(actual_dist == expected_dist, 'Round21 rendering changed another bound dist asset or introduced an unbound asset')
    build = run([sys.executable, '-B', str(mirror / 'scripts/build_pages.py')], out / 'site-build.log', mirror)
    expected = {name[len('docs/'):]: wanted for name, wanted in data['files'].items() if name.startswith('docs/')}
    actual = {str(p.relative_to(mirror / 'docs')): sha(p) for p in (mirror / 'docs').rglob('*') if p.is_file()}
    require(actual == expected, 'fresh site build differs from bound docs; build and review site before freezing inventory')
    node = shutil.which('node')
    executed = []
    if node:
        names = tests or ['tests/test_workbench.mjs']
        for index, name in enumerate(names):
            relative_name(name)
            require(name in data['files'], 'site test is not bound: ' + name)
            executed.append(run([node, str(mirror / name)], out / ('site-test-' + str(index) + '.log'), mirror))
    return {'round21_build': round21_build, 'round21_displayed_gates_verified': 10,
            'rebuilt_dist_identical': True, 'build': build, 'rebuilt_docs_identical': True,
            'node_tests': executed, 'node_status': 'executed' if node else 'unavailable; tests not run',
            'scope': 'Static build and chosen Node checks; no browser visual audit.'}


def verify(args):
    data, ledger = check_inventory(args.inventory, args.inventory_sha256)
    out = fresh_external(args.output)
    out.mkdir(parents=True)
    result = {'schema': 'ym21-final-verification-v1', 'status': 'running',
              'inventory_sha256': args.inventory_sha256, 'source_file_count': len(data['files']),
              'loops': list(LOOPS), 'research_loops_added_by_verification': 0}
    try:
        if args.check_base:
            result['historical_base'] = historical_base_check(ledger, out)
        else:
            result['historical_base'] = {'status': 'not requested; source hashes and repaired historical inventory still verified'}
        rows = []
        for optimized in (False, True):
            name = 'optimized' if optimized else 'normal'
            flags = ['-B'] + (['-O'] if optimized else [])
            command = [sys.executable, *flags, str(source('research/round21/reproduce.py')),
                       '--output', str(out / name), '--loops', *LOOPS]
            if optimized:
                command.append('--optimized')
            result[name] = run(command, out / (name + '.log'))
            record = check_reproduction(out / name, optimized)
            rows.append(record['executions'])
        require(rows[0] == rows[1], 'normal and optimized scientific execution hashes differ')
        result['normal_optimized_scientific_hashes_equal'] = True
        result['c2_command'] = run([sys.executable, '-B', str(source('research/round21/release/replay_c2.py')),
                                    '--output', str(out / 'c2')], out / 'c2.log')
        c2 = read_json(out / 'c2/replay.json')
        require(c2.get('status') == 'completed' and c2.get('research_loops_added') == 0 and
                c2.get('historical_failure', {}).get('historical_gate_remains_failed') is True,
                'C2 repaired replay semantics failed')
        result['c2_replay_sha256'] = sha(out / 'c2/replay.json')
        result['site'] = site_check(data, out, args.site_test) if args.site else {'status': 'not requested'}
        check_inventory(args.inventory, args.inventory_sha256)
        result['status'] = 'passed'
    except Exception as error:
        result['status'] = 'failed'
        result['error'] = str(error)
        write_json(out / 'final-verification.json', result)
        raise
    write_json(out / 'final-verification.json', result)
    print(json.dumps({'status': 'passed', 'loops': 10, 'research_producer_executions': 40,
                      'pair_comparisons': 20, 'c2_repair_replays': 1, 'output': str(out)}))


def structural_controls():
    base = {'schema': 'ym21-execution-v1', 'completed_loops': list(LOOPS),
            'planned_research_loops': 10, 'repairs_count_as_research_loops': False}
    ledger_check(base)
    cases = {
        'missing_m2': {**base, 'completed_loops': list(LOOPS[:-1])},
        'duplicate_loop': {**base, 'completed_loops': [*LOOPS[:-1], 'i1']},
        'unexpected_loop': {**base, 'completed_loops': [*LOOPS[:-1], 'n1']},
        'boolean_loop_count': {**base, 'planned_research_loops': True},
        'repair_counted_as_loop': {**base, 'repairs_count_as_research_loops': True},
    }
    results = []
    for name, value in cases.items():
        try:
            ledger_check(value)
        except ValueError as error:
            results.append({'name': name, 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('structural rejection failed: ' + name)
    for name in ('../escape', '/absolute', 'x/__pycache__/a.pyc', 'x/../a', 'a\\b', ''):
        try:
            relative_name(name)
        except ValueError as error:
            results.append({'name': 'unsafe_path:' + name, 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('unsafe inventory path accepted')
    try:
        json.loads('{"a":1,"a":2}', object_pairs_hook=no_duplicate_keys)
    except ValueError:
        results.append({'name': 'duplicate_json_key', 'rejected': True})
    else:
        raise ValueError('duplicate JSON key accepted')
    return {'status': 'passed', 'controls': results, 'scope': 'Structural controls only; not a scientific replay.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    for mode in ('inventory', 'preflight', 'self-test'):
        command = sub.add_parser(mode)
        command.add_argument('--output', type=Path, required=True)
    command = sub.add_parser('verify')
    command.add_argument('--inventory', type=Path, required=True)
    command.add_argument('--inventory-sha256', required=True)
    command.add_argument('--output', type=Path, required=True)
    command.add_argument('--site', action='store_true')
    command.add_argument('--site-test', action='append', default=[], help='repeatable bound repo-relative Node test; implies --site')
    command.add_argument('--check-base', action='store_true', help='compare Round19/20 with execution.json base in a Git checkout')
    args = parser.parse_args()
    if args.mode == 'verify':
        args.site = args.site or bool(args.site_test)
        verify(args)
        return
    out = fresh_external(args.output)
    try:
        if args.mode == 'inventory':
            data = inventory_candidate()
        elif args.mode == 'self-test':
            data = structural_controls()
        else:
            _, gates, _ = preflight()
            data = {'status': 'passed', 'loops': list(LOOPS), 'gates': {n: g['status'] for n, g in gates.items()},
                    'scope': 'Admission/source closure checked; executions not yet run.'}
        write_json(out, data)
    except Exception as error:
        write_json(out, {'status': 'failed', 'mode': args.mode, 'error': str(error)})
        raise
    print(json.dumps({'status': data.get('status', 'candidate'), 'output': str(out), 'sha256': sha(out)}))


if __name__ == '__main__':
    main()
