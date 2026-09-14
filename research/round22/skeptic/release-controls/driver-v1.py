#!/usr/bin/env python3
"""Coherent mutations of actual Round22 release stages in external copies.

No scientific execution, source checkout mutation, acceptance mocking or Git
mutation is performed. Successful stage controls are not full release admission.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
AUTHOR_ROOT = Path(__file__).resolve().parents[3]
VERIFIER = 'research/round22/release/final_verify.py'
ADMISSION = 'research/round22/admission.py'
INVENTORY = 'research/round22/release/final-inventory.json'
LEDGER = 'research/round22/advisor/progress-ledger.json'
SIX = 'research/round22/skeptic/post-six-review.json'
TEN = 'research/round22/skeptic/post-ten-review.json'
SELECTION = 'research/round22/advisor/post-six-selection.json'
ROADMAP = 'research/round22/advisor/post-ten-roadmap.json'
LOOPS = ['n1', 'n2', 'o1', 'o2', 'p1', 'p2', 'q1', 'q2', 'r1', 'r2']
INHERITED = ['i1', 'i2', 'j1', 'j2', 'k1', 'k2', 'l1', 'l2', 'm1', 'm2']
ZERO = '0' * 64


def need(value, message):
    if not value:
        raise RuntimeError(message)


def safe(path):
    for part in (path, *path.parents):
        need(not part.is_symlink(), 'linked source or fixture path: ' + str(part))
    return path


def sha(path):
    return hashlib.sha256(safe(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def environment():
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return env


def git(root, *args):
    proc = subprocess.run(['git', *args], cwd=root, env=environment(), capture_output=True, text=True)
    need(proc.returncode == 0, 'candidate identity read failed: ' + proc.stderr)
    return proc.stdout.strip()


def load_actual(root, pin):
    need(sha(root / VERIFIER) == pin, 'actual verifier source pin changed')
    need('admission' not in sys.modules, 'cached admission module in worker')
    spec = importlib.util.spec_from_file_location('ym22_actual_semantic_verifier', root / VERIFIER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    need(module.ROOT == root, 'actual verifier root drift')
    need(Path(sys.modules['admission'].__file__).resolve() == root / ADMISSION, 'wrong admission checkout')
    return module


def worker(args):
    root = safe(args.root.absolute()).resolve()
    module = load_actual(root, args.verifier_sha256)
    # Failures during fixture construction/import are not successful rejection.
    payload = read(args.payload) if args.payload else None
    try:
        if args.stage == 'preflight':
            module.preflight()
        elif args.stage == 'coherence':
            for loop in LOOPS:
                module.gate(loop)
        elif args.stage == 'validate':
            module.validate(args.inventory, args.inventory_sha256)
        elif args.stage == 'replay':
            module.validate_replay_summary(payload, INHERITED if args.inherited else LOOPS, args.summary_optimized)
        elif args.stage == 'admission':
            module.validate_admission_summary(payload, args.summary_optimized)
        elif args.stage == 'c2':
            module.validate_c2_summary(payload)
        elif args.stage == 'site':
            need(not args.output.exists(), 'site output must be absent')
            args.output.mkdir(parents=True)
            module.verify_site(read(root / INVENTORY), args.output)
        else:
            raise RuntimeError('unknown actual stage')
    except (ValueError, FileNotFoundError) as error:
        result = {'accepted': False, 'exception': type(error).__name__, 'error': str(error)}
        # Paths are still in the preserved worker log; stable outcome comparison
        # uses the exception and the tested predicate rather than fixture names.
    else:
        result = {'accepted': True}
    print(json.dumps(result, sort_keys=True))


def invoke(root, pin, stage, out, optimized, payload=None, inventory=None,
           inventory_pin=None, inherited=False):
    command = [sys.executable, '-B', *(['-O'] if optimized else []), str(Path(__file__).resolve()),
               '_stage', '--root', str(root), '--verifier-sha256', pin, '--stage', stage]
    if optimized:
        command.append('--summary-optimized')
    if payload is not None:
        payload_path = out.parent / (out.name + '-payload.json')
        write(payload_path, payload)
        command += ['--payload', str(payload_path)]
    if inventory is not None:
        command += ['--inventory', str(inventory), '--inventory-sha256', inventory_pin]
    if inherited:
        command.append('--inherited')
    if stage == 'site':
        command += ['--output', str(out)]
    proc = subprocess.run(command, env=environment(), capture_output=True, text=True)
    need(proc.returncode == 0 and not proc.stderr, 'actual stage worker did not execute cleanly: ' + proc.stderr)
    result = json.loads(proc.stdout)
    write(out.parent / (out.name + '-outcome.json'), result)
    return result


def copy_candidate(candidate, target, frozen):
    need(not target.exists(), 'fixture copy already exists')
    for name in [*frozen['files'], INVENTORY]:
        rel = Path(name)
        need(not rel.is_absolute() and '..' not in rel.parts, 'unsafe inventory path')
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(safe(candidate / rel), dest)


def snapshot_json(root, frozen):
    return {name: (root / name).read_bytes() for name in frozen['files'] if name.endswith('.json')}


def rebind_json_closure(root, frozen, before):
    """Propagate changed content digests through real JSON hash declarations.

    Scientific files are changed only inside a disposable test copy. Markdown
    history is not rewritten. No actual gate predicate is replaced or disabled.
    """
    names = [n for n in frozen['files'] if n.endswith('.json')]
    prior = {n: hashlib.sha256(before[n]).hexdigest() for n in names}
    for _ in range(100):
        current = {n: sha(root / n) for n in names}
        updates = {prior[n]: current[n] for n in names if prior[n] != current[n]}
        if not updates:
            break
        pattern = re.compile('|'.join(re.escape(x) for x in updates))
        prior = current
        for name in names:
            path = root / name
            text = path.read_text()
            changed = pattern.sub(lambda match: updates[match.group()], text)
            if changed != text:
                path.write_text(changed)
    else:
        raise RuntimeError('JSON hash propagation did not reach a fixed point')
    rebound = copy.deepcopy(frozen)
    rebound['files'] = {n: sha(root / n) for n in frozen['files']}
    write(root / INVENTORY, rebound)
    return rebound


def edit(root, name, mutation):
    data = read(root / name)
    mutation(data)
    write(root / name, data)


def set_key(name, value):
    return lambda obj: obj.__setitem__(name, value)


def semantic_cases():
    # Expected text identifies the real semantic predicate. Coherent gate
    # closure is checked before each call, so stale scientific hashes cannot
    # count as the intended rejection.
    return [
        ('ledger_float_count', LEDGER, set_key('completed_research_loops', 10.0), 'exactly ten completed'),
        ('ledger_extra_loop', LEDGER, lambda d: d['loops'].append(copy.deepcopy(d['loops'][-1])), 'missing, duplicate, reordered'),
        ('ledger_reordered_loops', LEDGER, lambda d: d['loops'].reverse(), 'missing, duplicate, reordered'),
        ('ledger_missing_loop', LEDGER, lambda d: d['loops'].pop(), 'missing, duplicate, reordered'),
        ('ledger_wrong_base', LEDGER, set_key('base_commit', '0' * 40), 'recovered base identity changed'),
        ('ledger_verdict_drift', LEDGER, lambda d: d['loops'][0].__setitem__('status', 'limited'), 'ledger verdict drift'),
        ('ledger_gate_binding', LEDGER, lambda d: d['loops'][0].__setitem__('gate_sha256', ZERO), 'ledger gate binding drift'),
        ('ledger_contract_binding', LEDGER, lambda d: d['loops'][0].__setitem__('contract_sha256', ZERO), 'ledger contract binding drift'),
        ('ledger_submission_binding', LEDGER, lambda d: d['loops'][0]['forward_submission'].__setitem__('sha256', ZERO), 'ledger frozen submission binding drift'),
        ('ledger_checkpoint_order', LEDGER, lambda d: d['checkpoints'].reverse(), 'ledger checkpoint order invalid'),
        ('ledger_checkpoint_binding', LEDGER, lambda d: d['checkpoints'][-1].__setitem__('review_sha256', ZERO), 'ledger checkpoint binding changed'),
        ('checkpoint_six_false', SIX, set_key('passed', False), 'required skeptical checkpoint missing or failed'),
        ('checkpoint_six_truthy', SIX, set_key('passed', 'true'), 'required skeptical checkpoint missing or failed'),
        ('checkpoint_six_float', SIX, set_key('completed_research_loops', 6.0), 'required skeptical checkpoint missing or failed'),
        ('checkpoint_six_missing_gate', SIX, lambda d: d['reviewed_gates'].pop('n1'), 'checkpoint gate bindings incomplete'),
        ('checkpoint_six_empty_findings', SIX, set_key('findings', []), 'checkpoint review content absent'),
        ('checkpoint_six_closed_continuum', SIX, set_key('continuum_status', 'closed'), 'checkpoint review content absent'),
        ('checkpoint_six_no_ranking', SIX, set_key('ranked_candidates', []), 'six-loop ranked alternatives missing'),
        ('checkpoint_ten_wrong_map', TEN, set_key('claim_map_sha256', ZERO), 'ten-loop review lacks actual claim map'),
        ('checkpoint_ten_missing_gate', TEN, lambda d: d['reviewed_gates'].pop('r2'), 'checkpoint gate bindings incomplete'),
        ('checkpoint_ten_false', TEN, set_key('passed', False), 'required skeptical checkpoint missing or failed'),
        ('selection_empty_goal', SELECTION, lambda d: d['goals'][0].__setitem__('target', ' '), 'Q/R goal content missing'),
        ('selection_missing_gate', SELECTION, lambda d: d['reviewed_gates'].pop('n1'), 'Q/R selection does not bind all six'),
        ('selection_wrong_checkpoint', SELECTION, set_key('skeptic_review_sha256', ZERO), 'Q/R selection does not bind the six-loop'),
        ('roadmap_two_goals', ROADMAP, lambda d: d['goals'].pop(), 'exactly three next goals'),
        ('roadmap_empty_target', ROADMAP, lambda d: d['goals'][0].__setitem__('target', ' '), 'future goal content missing'),
        ('roadmap_duplicate_goal', ROADMAP, lambda d: d['goals'][1].__setitem__('id', d['goals'][0]['id']), 'duplicate future goal'),
        ('roadmap_executed', ROADMAP, set_key('executed', True), 'extra research execution not authorized'),
        ('roadmap_nonboolean_execution', ROADMAP, set_key('executed', 0), 'extra research execution not authorized'),
        ('roadmap_wrong_checkpoint', ROADMAP, set_key('skeptic_review_sha256', ZERO), 'future goals lack ten-loop feedback binding'),
    ]


def replay_fixture(root, optimized, inherited=False):
    loops = INHERITED if inherited else LOOPS
    round_name = 'round21' if inherited else 'round22'
    rows, gates = [], {}
    for loop in loops:
        gate_path = f'research/{round_name}/advisor/{loop}-gate.json'
        gate = read(root / gate_path)
        gates[loop] = sha(root / gate_path)
        for direction in ['forward', 'reverse']:
            prefix = f'research/{round_name}/{direction}/{loop}/'
            row = {'loop': loop, 'direction': direction, 'source_sha256': sha(root / (prefix + 'check.py')),
                   'result_sha256': sha(root / (prefix + 'output/results.json'))}
            if not inherited:
                row['outputs_compared'] = sum(name.startswith(prefix + 'output/') for name in gate['files'])
            rows.append(row)
    data = {'status': 'passed', 'loops': loops, 'optimized': optimized, 'executions': rows}
    if inherited:
        data['pair_comparisons'] = 10
    else:
        data.update(admitted_gates=gates, research_loops_added=0)
    return data


def admission_fixture(root, module, optimized):
    return {'status': 'passed', 'loop': 'n1', 'optimized': optimized,
            'gate_sha256': sha(root / 'research/round22/advisor/n1-gate.json'),
            'controls': [{'control': name, 'rejected': True} for name in module.ADMISSION_CONTROLS]}


def c2_fixture():
    return {'schema': 'ym21-c2-replay-v1', 'status': 'completed', 'optimized': False,
            'research_loops_added': 0, 'historical_failure': {'historical_gate_remains_failed': True},
            'replays': {'forward': {}, 'backward': {}, 'comparison': {
                'semantic_checks': 34, 'rejected_scientific_mutations': 27,
                'identical_to_historical_except_validated_absolute_paths': True}}}


def summary_cases():
    return [
        ('replay_missing_pair', 'replay', False, lambda d: d['executions'].pop()),
        ('replay_reordered_pairs', 'replay', False, lambda d: d['executions'].reverse()),
        ('replay_wrong_loop_list', 'replay', False, lambda d: d['loops'].reverse()),
        ('replay_failed_status', 'replay', False, set_key('status', 'failed')),
        ('replay_truthy_optimized', 'replay', False, set_key('optimized', 1)),
        ('replay_missing_hashes', 'replay', False, lambda d: d['executions'][0].pop('source_sha256')),
        ('replay_wrong_source_hash', 'replay', False, lambda d: d['executions'][0].__setitem__('source_sha256', ZERO)),
        ('replay_wrong_result_hash', 'replay', False, lambda d: d['executions'][0].__setitem__('result_sha256', ZERO)),
        ('replay_wrong_output_count', 'replay', False, lambda d: d['executions'][0].__setitem__('outputs_compared', 0)),
        ('replay_float_output_count', 'replay', False, lambda d: d['executions'][0].__setitem__('outputs_compared', float(d['executions'][0]['outputs_compared']))),
        ('replay_missing_gate_binding', 'replay', False, lambda d: d['admitted_gates'].pop('n1')),
        ('replay_boolean_zero_loops', 'replay', False, set_key('research_loops_added', False)),
        ('inherited_wrong_hash', 'replay', True, lambda d: d['executions'][0].__setitem__('result_sha256', ZERO)),
        ('inherited_float_paircount', 'replay', True, set_key('pair_comparisons', 10.0)),
        ('admission_missing_control', 'admission', False, lambda d: d['controls'].pop()),
        ('admission_duplicate_identity', 'admission', False, lambda d: d['controls'][1].__setitem__('control', d['controls'][0]['control'])),
        ('admission_false_rejection', 'admission', False, lambda d: d['controls'][0].__setitem__('rejected', False)),
        ('admission_truthy_rejection', 'admission', False, lambda d: d['controls'][0].__setitem__('rejected', 1)),
        ('admission_wrong_gate', 'admission', False, set_key('gate_sha256', ZERO)),
        ('c2_historical_promotion', 'c2', False, lambda d: d['historical_failure'].__setitem__('historical_gate_remains_failed', False)),
        ('c2_boolean_zero_loops', 'c2', False, set_key('research_loops_added', False)),
        ('c2_float_semantic_count', 'c2', False, lambda d: d['replays']['comparison'].__setitem__('semantic_checks', 34.0)),
        ('c2_missing_mutations', 'c2', False, lambda d: d['replays']['comparison'].__setitem__('rejected_scientific_mutations', 26)),
        ('c2_false_path_equivalence', 'c2', False, lambda d: d['replays']['comparison'].__setitem__('identical_to_historical_except_validated_absolute_paths', False)),
    ]


def main(args):
    candidate = safe(args.candidate.absolute()).resolve()
    out = safe(args.output.absolute()).resolve()
    need(not out.exists(), 'output must be fresh')
    need(candidate not in out.parents and AUTHOR_ROOT not in out.parents, 'output must be outside source worktrees')
    need(sha(candidate / INVENTORY) == args.inventory_sha256, 'external candidate inventory pin mismatch')
    need(sha(candidate / VERIFIER) == args.verifier_sha256, 'external verifier source pin mismatch')
    need(git(candidate, 'rev-parse', 'HEAD') == args.git_commit and
         git(candidate, 'rev-parse', 'HEAD^{tree}') == args.git_tree, 'candidate commit/tree mismatch')
    need(not git(candidate, 'status', '--porcelain', '--untracked-files=all'), 'candidate is dirty')
    frozen = read(candidate / INVENTORY)
    for name, digest in frozen['files'].items():
        need(sha(candidate / name) == digest, 'candidate file inventory mismatch: ' + name)
    out.mkdir(parents=True)
    positive, rows = [], []
    fixtures = out / 'fixtures'
    fixtures.mkdir()
    # Read the actual constant identities in a separate worker-facing module;
    # this parent import is never reused by a stage worker.
    module = load_actual(candidate, args.verifier_sha256)
    for optimized in [False, True]:
        mode = 'optimized' if optimized else 'normal'
        baseline = invoke(candidate, args.verifier_sha256, 'validate', out / ('positive-' + mode), optimized,
                          inventory=candidate / INVENTORY, inventory_pin=args.inventory_sha256)
        need(baseline == {'accepted': True}, 'positive complete inventory/preflight failed: ' + str(baseline))
        positive.append({'stage': 'validate', 'mode': mode, 'accepted': True})
    try:
        for name, path, mutation, error_text in semantic_cases():
            target = fixtures / name
            copy_candidate(candidate, target, frozen)
            before = snapshot_json(target, frozen)
            edit(target, path, mutation)
            rebound = rebind_json_closure(target, frozen, before)
            outcomes = []
            for optimized in [False, True]:
                mode = 'optimized' if optimized else 'normal'
                coherent = invoke(target, args.verifier_sha256, 'coherence', out / (name + '-coherence-' + mode), optimized)
                need(coherent == {'accepted': True}, name + ': stale scientific hashes mask semantic mutation: ' + str(coherent))
                observed = invoke(target, args.verifier_sha256, 'preflight', out / (name + '-' + mode), optimized)
                need(observed.get('accepted') is False and observed.get('exception') == 'ValueError'
                     and error_text in observed['error'], name + ': wrong or absent semantic rejection: ' + str(observed))
                outcomes.append(observed)
            need(outcomes[0] == outcomes[1], name + ': optimized semantic outcome differs')
            rows.append({'control': name, 'stage': 'preflight', 'rejected': True, 'normal_optimized_equal': True,
                         'gate_closure_passed_before_rejection': True, 'error': outcomes[0]['error'],
                         'rebound_inventory_sha256': sha(target / INVENTORY)})
            if not args.keep_fixtures:
                shutil.rmtree(target)

        for name, stage, inherited, mutation in summary_cases():
            outcomes = []
            for optimized in [False, True]:
                mode = 'optimized' if optimized else 'normal'
                if stage == 'replay':
                    data = replay_fixture(candidate, optimized, inherited)
                elif stage == 'admission':
                    data = admission_fixture(candidate, module, optimized)
                else:
                    data = c2_fixture()
                good = invoke(candidate, args.verifier_sha256, stage, out / (name + '-positive-' + mode), optimized,
                              payload=data, inherited=inherited)
                need(good == {'accepted': True}, name + ': positive real summary stage failed: ' + str(good))
                mutation(data)
                bad = invoke(candidate, args.verifier_sha256, stage, out / (name + '-' + mode), optimized,
                             payload=data, inherited=inherited)
                need(bad.get('accepted') is False and bad.get('exception') == 'ValueError',
                     name + ': summary mutation was not rejected: ' + str(bad))
                outcomes.append(bad)
            need(outcomes[0] == outcomes[1], name + ': summary modes differ')
            rows.append({'control': name, 'stage': stage, 'rejected': True, 'normal_optimized_equal': True,
                         'positive_summary_control_passed': True, 'error': outcomes[0]['error'],
                         'summary_fixture_from_bound_outputs_not_new_execution': True})

        run_inventory_cases(candidate, frozen, args, out, fixtures, rows)
        run_build_cases(candidate, frozen, args, out, fixtures, rows, positive)
        for name, digest in frozen['files'].items():
            need(sha(candidate / name) == digest, 'source candidate changed during fixtures: ' + name)
        need(sha(candidate / INVENTORY) == args.inventory_sha256, 'source canonical inventory changed')
        need(not git(candidate, 'status', '--porcelain', '--untracked-files=all'), 'source candidate became dirty')
        result = {'schema': 'ym22-release-semantic-build-controls-v1', 'status': 'passed', 'passed': True,
                  'candidate_commit': args.git_commit, 'candidate_tree': args.git_tree,
                  'candidate_inventory_sha256': args.inventory_sha256,
                  'source_hashes': {VERIFIER: args.verifier_sha256, ADMISSION: sha(candidate / ADMISSION),
                                    'research/round22/skeptic/check_release_semantics.py': sha(Path(__file__).resolve())},
                  'positive_stage_controls': positive, 'controls': rows, 'control_count': len(rows),
                  'normal_optimized_equal': True, 'source_candidate_preserved': True,
                  'git_mutation_cases_executed': False, 'research_producer_executions': 0,
                  'research_loops_added': 0, 'final_release_admission_claimed': False,
                  'scope': 'Actual preflight/inventory/summary/site stages only; fresh summary fixtures are not fresh producer executions',
                  'fixtures_retained': args.keep_fixtures}
        write(out / 'results.json', result)
        write(out / 'source-manifest.json', {'schema': 'ym22-source-manifest-v1', 'inputs': result['source_hashes'],
                                           'outputs': {'results.json': sha(out / 'results.json')}})
    except Exception as error:
        write(out / 'failure.json', {'status': 'failed', 'passed': False, 'completed_controls': rows,
                                    'error': str(error), 'fixtures_retained': True, 'research_loops_added': 0})
        raise
    print(json.dumps({'status': 'passed', 'controls': len(rows), 'both_python_modes': True,
                      'results_sha256': sha(out / 'results.json')}))


def run_inventory_cases(candidate, frozen, args, out, fixtures, rows):
    cases = [
        ('wrong_external_inventory_pin', 'reviewed inventory digest changed'),
        ('noncanonical_external_inventory_pin', 'invalid reviewed digest'),
        ('canonical_inventory_byte_mismatch', 'canonical in-tree inventory differs'),
        ('coherent_rebinding_does_not_replace_external_pin', 'reviewed inventory digest changed'),
        ('missing_inventory_member', 'release inventory is incomplete'),
        ('unlisted_in_tree_file', 'release inventory is incomplete'),
    ]
    for name, error_text in cases:
        target = fixtures / name
        copy_candidate(candidate, target, frozen)
        supplied = out / (name + '-inventory.json')
        shutil.copyfile(candidate / INVENTORY, supplied)
        pin = args.inventory_sha256
        if name == 'wrong_external_inventory_pin':
            pin = ZERO
        elif name == 'noncanonical_external_inventory_pin':
            pin = 'NOT-A-SHA256'
        elif name == 'canonical_inventory_byte_mismatch':
            (target / INVENTORY).write_bytes((target / INVENTORY).read_bytes() + b'\n')
        elif name == 'coherent_rebinding_does_not_replace_external_pin':
            (target / 'README.md').write_bytes((target / 'README.md').read_bytes() + b'\nRelease pin fixture.\n')
            changed = copy.deepcopy(frozen)
            changed['files']['README.md'] = sha(target / 'README.md')
            write(target / INVENTORY, changed)
            shutil.copyfile(target / INVENTORY, supplied)
        elif name == 'missing_inventory_member':
            changed = copy.deepcopy(frozen)
            changed['files'].pop('README.md')
            write(target / INVENTORY, changed)
            shutil.copyfile(target / INVENTORY, supplied)
            pin = sha(supplied)
        elif name == 'unlisted_in_tree_file':
            extra = target / 'research/round22/skeptic/unlisted_release_fixture.txt'
            need(not extra.exists(), 'extra fixture collision')
            extra.write_text('Unlisted fixture inside an inventoried tree.\n')
        outcomes = []
        for optimized in [False, True]:
            mode = 'optimized' if optimized else 'normal'
            # The actual preflight must pass, independently of the target pin
            # or inventory-membership defect.
            preflight = invoke(target, args.verifier_sha256, 'preflight', out / (name + '-preflight-' + mode), optimized)
            need(preflight == {'accepted': True}, name + ': unrelated preflight rejection')
            observed = invoke(target, args.verifier_sha256, 'validate', out / (name + '-' + mode), optimized,
                              inventory=supplied, inventory_pin=pin)
            need(observed.get('accepted') is False and observed.get('exception') == 'ValueError'
                 and error_text in observed['error'], name + ': wrong inventory rejection: ' + str(observed))
            outcomes.append(observed)
        need(outcomes[0] == outcomes[1], name + ': inventory modes differ')
        rows.append({'control': name, 'stage': 'validate', 'rejected': True, 'normal_optimized_equal': True,
                     'preflight_passed_before_rejection': True, 'error': outcomes[0]['error']})
        if not args.keep_fixtures:
            shutil.rmtree(target)


def run_build_cases(candidate, frozen, args, out, fixtures, rows, positive):
    for optimized in [False, True]:
        mode = 'optimized' if optimized else 'normal'
        observed = invoke(candidate, args.verifier_sha256, 'site', out / ('positive-site-' + mode), optimized)
        need(observed == {'accepted': True}, 'positive actual site stage failed: ' + str(observed))
        positive.append({'stage': 'verify_site', 'mode': mode, 'accepted': True})
    cases = [
        ('successful_noop_claim_map_builder', 'research/round22/build_claim_map.py', 'FileNotFoundError', None),
        ('successful_noop_round22_data_builder', 'research/round22/build_site.py', 'ValueError', 'source-built current data changed'),
        ('successful_noop_pages_builder', 'scripts/build_pages.py', 'ValueError', 'fresh Pages build differs'),
        ('stale_nested_docs_preservation', None, 'ValueError', 'fresh Pages build differs'),
    ]
    for name, builder, exception, error_text in cases:
        target = fixtures / name
        copy_candidate(candidate, target, frozen)
        before = snapshot_json(target, frozen)
        changed = copy.deepcopy(frozen)
        if builder:
            old_sha = sha(target / builder)
            (target / builder).write_text('print("successful no-op builder fixture")\n')
            new_sha = sha(target / builder)
            # Builder pins are bound in post-ten review JSON, which then changes
            # checkpoint/roadmap pins. Seed the same genuine JSON propagation.
            for json_name in before:
                path = target / json_name
                text = path.read_text()
                if old_sha in text:
                    path.write_text(text.replace(old_sha, new_sha))
        else:
            name_extra = 'docs/stale/archive/orphan.txt'
            extra = target / name_extra
            need(not extra.exists(), 'stale-doc fixture collision')
            extra.parent.mkdir(parents=True)
            extra.write_text('This nested stale asset must not survive a fresh Pages build.\n')
            changed['files'][name_extra] = sha(extra)
        # The extra stale asset is not JSON and does not affect hash propagation.
        rebound = rebind_json_closure(target, frozen, before)
        if not builder:
            rebound['files'][name_extra] = sha(extra)
            write(target / INVENTORY, rebound)
        outcomes = []
        for optimized in [False, True]:
            mode = 'optimized' if optimized else 'normal'
            valid = invoke(target, args.verifier_sha256, 'validate', out / (name + '-validate-' + mode), optimized,
                           inventory=target / INVENTORY, inventory_pin=sha(target / INVENTORY))
            need(valid == {'accepted': True}, name + ': coherent preflight/inventory did not pass: ' + str(valid))
            build_out = out / (name + '-site-' + mode)
            observed = invoke(target, args.verifier_sha256, 'site', build_out, optimized)
            need(observed.get('accepted') is False and observed.get('exception') == exception
                 and (error_text is None or error_text in observed['error']),
                 name + ': wrong or absent fresh-build rejection: ' + str(observed))
            if builder:
                log_name = {'research/round22/build_claim_map.py': 'claim-map-build.log',
                            'research/round22/build_site.py': 'data-build.log',
                            'scripts/build_pages.py': 'pages-build.log'}[builder]
                need((build_out / log_name).read_text().strip() == 'successful no-op builder fixture',
                     name + ': no-op did not actually run successfully')
            else:
                need(not (build_out / 'site-work' / name_extra).exists(), 'stale nested doc was not removed')
            outcomes.append(observed)
        # FileNotFoundError includes the separate mode-specific output path.
        need(outcomes[0]['exception'] == outcomes[1]['exception'], name + ': build exception differs by mode')
        if exception != 'FileNotFoundError':
            need(outcomes[0] == outcomes[1], name + ': build predicate differs by mode')
        rows.append({'control': name, 'stage': 'verify_site', 'rejected': True, 'normal_optimized_equal': True,
                     'inventory_and_preflight_passed_before_rejection': True,
                     'builder_exited_successfully': bool(builder), 'exception': exception,
                     'error_predicate': error_text or 'the generated claim map is absent after its successful no-op builder',
                     'rebound_inventory_sha256': sha(target / INVENTORY)})
        if not args.keep_fixtures:
            shutil.rmtree(target)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    run = sub.add_parser('run')
    run.add_argument('--candidate', type=Path, required=True)
    run.add_argument('--git-commit', required=True)
    run.add_argument('--git-tree', required=True)
    run.add_argument('--inventory-sha256', required=True)
    run.add_argument('--verifier-sha256', required=True)
    run.add_argument('--output', type=Path, required=True)
    run.add_argument('--keep-fixtures', action='store_true')
    internal = sub.add_parser('_stage')
    internal.add_argument('--root', type=Path, required=True)
    internal.add_argument('--verifier-sha256', required=True)
    internal.add_argument('--stage', choices=['preflight', 'coherence', 'validate', 'replay', 'admission', 'c2', 'site'], required=True)
    internal.add_argument('--payload', type=Path)
    internal.add_argument('--inventory', type=Path)
    internal.add_argument('--inventory-sha256')
    internal.add_argument('--output', type=Path)
    internal.add_argument('--summary-optimized', action='store_true')
    internal.add_argument('--inherited', action='store_true')
    parsed = parser.parse_args()
    worker(parsed) if parsed.mode == '_stage' else main(parsed)
