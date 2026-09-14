#!/usr/bin/env python3
"""Exercise the real release git_state in disposable external Git repositories.

This is a stage-specific infrastructure harness, never final release admission.
No source-worktree mutations, commits, pushes or mocked predicates are used.
"""
from pathlib import Path
from types import SimpleNamespace
import argparse
import hashlib
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
AUTHORING_ROOT = HERE.parents[2]
VERIFIER = 'research/round22/release/final_verify.py'
ADMISSION = 'research/round22/admission.py'
INVENTORY = 'research/round22/release/final-inventory.json'
PINNED_VERIFIER = '55946920fcc75bf6d06d81c5ee7fa7c6854640ad219ed9c0aace13f6c8a64419'
RECOVERED_BASE = '382e61571b029e198d87abbeec99d88157d3c168'
BYTE_TARGET = 'README.md'
HISTORICAL_TARGET = 'research/round21/release/final-inventory.json'
IGNORED_TARGET = 'research/round22/reverse/release_git_ignored_probe.txt'
UNINVENTORIED_TARGET = 'release_git_uninventoried_probe.txt'
CASES = (
    ('attached_head', 'release worktree must have detached HEAD'),
    ('wrong_commit', 'reviewed Git commit changed'),
    ('wrong_tree', 'reviewed Git tree changed'),
    ('ignored_inventoried_extra', 'inventoried file is absent from Git tree: ' + IGNORED_TARGET),
    ('assume_unchanged_bytes', 'disk bytes differ from committed blob: ' + BYTE_TARGET),
    ('skip_worktree_bytes', 'disk bytes differ from committed blob: ' + BYTE_TARGET),
    ('hidden_executable_mode', 'disk executable mode differs from committed mode: ' + BYTE_TARGET),
    ('committed_historical_change', 'historical research changed after recovered base'),
    ('committed_uninventoried_change', 'changed published file lies outside reviewed inventory'),
)


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def unlinked(path):
    for p in (path, *path.parents):
        need(not p.is_symlink(), 'symlink fixture/source component: ' + str(p))
    return path


def sha(path):
    return hashlib.sha256(unlinked(path).read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')


def safe_environment():
    # Inherited index/worktree/object variables must never redirect fixture writes.
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_TERMINAL_PROMPT='0', GIT_AUTHOR_NAME='Round22 isolated fixture',
               GIT_AUTHOR_EMAIL='fixture@example.invalid',
               GIT_COMMITTER_NAME='Round22 isolated fixture',
               GIT_COMMITTER_EMAIL='fixture@example.invalid',
               GIT_AUTHOR_DATE='2000-01-01T00:00:00+0000',
               GIT_COMMITTER_DATE='2000-01-01T00:00:00+0000',
               PYTHONDONTWRITEBYTECODE='1')
    return env


def git(root, *args):
    proc = subprocess.run(['git', '-c', 'core.hooksPath=' + os.devnull,
                           '-c', 'commit.gpgsign=false', *args], cwd=root,
                          env=safe_environment(), text=True, capture_output=True)
    need(proc.returncode == 0, 'fixture Git command failed: ' + repr(args) + ': ' + proc.stderr.strip())
    return proc.stdout.strip()


def worker(root, commit, tree, verifier_sha):
    """Load the untouched actual module in this new interpreter and call git_state."""
    root = unlinked(root.absolute()).resolve()
    need(sha(root / VERIFIER) == verifier_sha, 'loaded verifier does not match reviewed source pin')
    need('admission' not in sys.modules, 'worker must start without cached admission module')
    spec = importlib.util.spec_from_file_location('ym22_actual_git_verifier', root / VERIFIER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    need(module.ROOT == root, 'actual verifier loaded from the wrong root')
    need(Path(sys.modules['admission'].__file__).resolve() == root / ADMISSION,
         'actual admission imported from another checkout')
    frozen = module.read(root / INVENTORY)
    # Import/setup failures above are not successful rejections. Catch only the
    # real acceptance exception from the actual target call.
    try:
        receipt = module.git_state(SimpleNamespace(git_commit=commit, git_tree=tree), frozen)
    except ValueError as error:
        print(json.dumps({'accepted': False, 'exception': 'ValueError', 'error': str(error)}, sort_keys=True))
    else:
        print(json.dumps({'accepted': True, 'receipt': receipt}, sort_keys=True))


def invoke(root, commit, tree, verifier_sha, optimized):
    command = [sys.executable, '-B', *(['-O'] if optimized else []), str(Path(__file__).resolve()),
               '_git-state', '--root', str(root), '--git-commit', commit, '--git-tree', tree,
               '--verifier-sha256', verifier_sha]
    proc = subprocess.run(command, env=safe_environment(), text=True, capture_output=True)
    need(proc.returncode == 0, 'actual git_state worker failed to execute: ' + proc.stderr.strip())
    need(not proc.stderr.strip(), 'unexpected worker stderr: ' + proc.stderr.strip())
    return json.loads(proc.stdout)


def both_modes(root, commit, tree, verifier_sha):
    normal = invoke(root, commit, tree, verifier_sha, False)
    optimized = invoke(root, commit, tree, verifier_sha, True)
    need(normal == optimized, 'ordinary/optimized git_state outcomes differ')
    return normal


def disk_inventory_coherent(root, frozen):
    for name, expected in frozen['files'].items():
        p = Path(name)
        need(not p.is_absolute() and '..' not in p.parts, 'unsafe fixture inventory path')
        need(sha(root / p) == expected, 'fixture inventory is not coherent with disk: ' + name)
    return True


def commit_fixture(root, paths, message):
    git(root, 'add', '--', *paths)
    git(root, 'commit', '--quiet', '--no-gpg-sign', '-m', 'Round22 Git fixture: ' + message)
    return git(root, 'rev-parse', 'HEAD'), git(root, 'rev-parse', 'HEAD^{tree}')


def rebind(root, name):
    frozen = json.loads((root / INVENTORY).read_text())
    frozen['files'][name] = sha(root / name)
    write(root / INVENTORY, frozen)


def mutate(root, case, pinned_commit, pinned_tree):
    commit, tree = pinned_commit, pinned_tree
    if case == 'attached_head':
        git(root, 'switch', '--quiet', '-c', 'fixture-attached')
    elif case == 'wrong_commit':
        need(pinned_commit != RECOVERED_BASE, 'candidate must differ from recovered base')
        commit = RECOVERED_BASE
    elif case == 'wrong_tree':
        tree = git(root, 'rev-parse', RECOVERED_BASE + '^{tree}')
        need(tree != pinned_tree, 'candidate tree must differ from recovered base')
    elif case == 'ignored_inventoried_extra':
        target = root / IGNORED_TARGET
        need(not target.exists(), 'ignored fixture path already exists')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b'Ignored but coherently inventoried fixture.\n')
        exclude = Path(git(root, 'rev-parse', '--git-path', 'info/exclude'))
        if not exclude.is_absolute():
            exclude = root / exclude
        with exclude.open('ab') as stream:
            stream.write(b'\n/' + IGNORED_TARGET.encode() + b'\n')
        need(git(root, 'check-ignore', '--', IGNORED_TARGET) == IGNORED_TARGET, 'fixture is not actually ignored')
        rebind(root, IGNORED_TARGET)
        commit, tree = commit_fixture(root, [INVENTORY], case)
        need(not git(root, 'ls-files', '--', IGNORED_TARGET), 'ignored extra was accidentally committed')
    elif case in ('assume_unchanged_bytes', 'skip_worktree_bytes'):
        flag = '--assume-unchanged' if case.startswith('assume') else '--skip-worktree'
        git(root, 'update-index', flag, '--', BYTE_TARGET)
        target = root / BYTE_TARGET
        target.write_bytes(target.read_bytes() + b'\nCoherently rebound hidden disk-byte fixture.\n')
        rebind(root, BYTE_TARGET)
        # Only commit the inventory. The hidden source index entry retains the
        # original blob, while disk and the newly committed inventory agree.
        commit, tree = commit_fixture(root, [INVENTORY], case)
        tag = git(root, 'ls-files', '-v', '--', BYTE_TARGET).split(' ', 1)[0]
        need(tag == ('h' if case.startswith('assume') else 'S'), 'index hiding flag did not survive fixture commit')
        committed = subprocess.run(['git', 'show', 'HEAD:' + BYTE_TARGET], cwd=root,
                                   env=safe_environment(), capture_output=True)
        need(committed.returncode == 0 and committed.stdout != target.read_bytes(), 'hidden disk mutation was committed')
    elif case == 'hidden_executable_mode':
        git(root, 'config', 'core.fileMode', 'false')
        target = root / BYTE_TARGET
        old = target.stat().st_mode
        target.chmod(old ^ 0o100)
        need(bool(target.stat().st_mode & 0o100) != bool(old & 0o100), 'executable bit did not change')
    elif case == 'committed_historical_change':
        target = root / HISTORICAL_TARGET
        target.write_bytes(target.read_bytes() + b'\n')
        rebind(root, HISTORICAL_TARGET)
        commit, tree = commit_fixture(root, [HISTORICAL_TARGET, INVENTORY], case)
    elif case == 'committed_uninventoried_change':
        target = root / UNINVENTORIED_TARGET
        need(not target.exists(), 'uninventoried fixture path already exists')
        target.write_bytes(b'Committed fixture outside the reviewed inventory.\n')
        commit, tree = commit_fixture(root, [UNINVENTORIED_TARGET], case)
        need(UNINVENTORIED_TARGET not in json.loads((root / INVENTORY).read_text())['files'], 'uninventoried fixture was rebound')
    else:
        raise RuntimeError('unknown fixture case')
    status = git(root, 'status', '--porcelain', '--untracked-files=all')
    need(not status, 'dirty status would mask the intended rejection: ' + case + ': ' + status)
    frozen = json.loads((root / INVENTORY).read_text())
    disk_inventory_coherent(root, frozen)
    return commit, tree, {'git_status_clean': True, 'disk_inventory_coherent': True,
                          'canonical_inventory_sha256': sha(root / INVENTORY),
                          'actual_commit': git(root, 'rev-parse', 'HEAD'),
                          'actual_tree': git(root, 'rev-parse', 'HEAD^{tree}'),
                          'supplied_commit': commit, 'supplied_tree': tree}


def main(args):
    candidate = unlinked(args.candidate.absolute()).resolve()
    out = unlinked(args.output.absolute()).resolve()
    need(not out.exists(), 'output must be fresh')
    for source_root in (candidate, AUTHORING_ROOT):
        need(out != source_root and source_root not in out.parents, 'fixtures must be outside source worktrees')
    need(re.fullmatch('[0-9a-f]{40}', args.git_commit) is not None and
         re.fullmatch('[0-9a-f]{40}', args.git_tree) is not None, 'exact externally supplied commit/tree required')
    need(re.fullmatch('[0-9a-f]{64}', args.inventory_sha256) is not None, 'external inventory SHA256 required')
    need(sha(candidate / INVENTORY) == args.inventory_sha256, 'supplied inventory pin does not match candidate')
    need(sha(candidate / VERIFIER) == args.verifier_sha256, 'reviewed verifier source changed')
    frozen = json.loads((candidate / INVENTORY).read_text())
    need(frozen['base_commit'] == RECOVERED_BASE, 'fixture candidate lacks anchored recovered base')
    need(BYTE_TARGET in frozen['files'] and HISTORICAL_TARGET in frozen['files'], 'required mutation targets not inventoried')
    disk_inventory_coherent(candidate, frozen)
    initial_source_hashes = {VERIFIER: sha(candidate / VERIFIER), ADMISSION: sha(candidate / ADMISSION),
                             INVENTORY: sha(candidate / INVENTORY),
                             'research/round22/reverse/check_release_git.py': sha(Path(__file__).resolve())}
    positive = both_modes(candidate, args.git_commit, args.git_tree, args.verifier_sha256)
    need(positive.get('accepted') is True, 'positive candidate Git-stage control failed: ' + str(positive))
    out.mkdir(parents=True)
    fixtures = out / 'fixtures'
    fixtures.mkdir()
    seed = fixtures / 'seed.git'
    # No hard links or writes into the candidate's object store. Per-case clones
    # may borrow only from this independent disposable seed, never the source.
    git(fixtures, 'clone', '--bare', '--no-hardlinks', '--quiet', str(candidate), str(seed))
    need(git(seed, 'cat-file', '-t', args.git_commit) == 'commit', 'seed lacks pinned candidate commit')
    rows = []
    try:
        for case, expected in CASES:
            target = fixtures / case
            git(fixtures, 'clone', '--shared', '--no-checkout', '--quiet', str(seed), str(target))
            git(target, 'checkout', '--detach', '--quiet', args.git_commit)
            # Require each independent clone to pass before its own mutation.
            baseline = both_modes(target, args.git_commit, args.git_tree, args.verifier_sha256)
            need(baseline == positive, 'unmodified fixture differs from positive candidate')
            commit, tree, setup = mutate(target, case, args.git_commit, args.git_tree)
            observed = both_modes(target, commit, tree, args.verifier_sha256)
            need(observed == {'accepted': False, 'exception': 'ValueError', 'error': expected},
                 'wrong or missing Git-stage rejection for ' + case + ': ' + str(observed))
            rows.append({'control': case, 'rejected': True, 'expected_error': expected,
                         'actual_outcome': observed, 'normal_optimized_equal': True, 'setup': setup})
        # The original candidate is read again after all disposable mutations.
        need(both_modes(candidate, args.git_commit, args.git_tree, args.verifier_sha256) == positive,
             'source candidate Git state changed during fixtures')
        disk_inventory_coherent(candidate, frozen)
        need(sha(candidate / INVENTORY) == args.inventory_sha256, 'source inventory changed during fixtures')
        result = {'schema': 'ym22-release-git-controls-v1', 'status': 'passed', 'passed': True,
                  'scope': 'actual git_state stage only; no final release admission or publication test',
                  'candidate_commit': args.git_commit, 'candidate_tree': args.git_tree,
                  'candidate_inventory_sha256': args.inventory_sha256,
                  'source_hashes': initial_source_hashes, 'positive_git_stage': positive['receipt'],
                  'controls': rows, 'control_count': len(CASES),
                  'normal_optimized_equal': True, 'source_candidate_preserved': True,
                  'fixtures_retained': args.keep_fixtures,
                  'semantic_checkpoint_build_stages_executed': False,
                  'research_loops_added': 0, 'final_release_admission_claimed': False}
        write(out / 'results.json', result)
        write(out / 'source-manifest.json', {'schema': 'ym22-source-manifest-v1',
              'inputs': initial_source_hashes, 'outputs': {'results.json': sha(out / 'results.json')}})
    except Exception as error:
        write(out / 'failure.json', {'status': 'failed', 'passed': False, 'completed_controls': rows,
                                     'error': str(error), 'fixtures_retained': True, 'research_loops_added': 0})
        raise
    else:
        if not args.keep_fixtures:
            shutil.rmtree(fixtures)
    print(json.dumps({'status': 'passed', 'controls': len(CASES), 'both_python_modes': True,
                      'final_release_admission_claimed': False, 'results_sha256': sha(out / 'results.json')}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    run = sub.add_parser('run')
    run.add_argument('--candidate', type=Path, required=True)
    run.add_argument('--git-commit', required=True)
    run.add_argument('--git-tree', required=True)
    run.add_argument('--inventory-sha256', required=True)
    run.add_argument('--verifier-sha256', default=PINNED_VERIFIER)
    run.add_argument('--output', type=Path, required=True)
    run.add_argument('--keep-fixtures', action='store_true')
    internal = sub.add_parser('_git-state')
    internal.add_argument('--root', type=Path, required=True)
    internal.add_argument('--git-commit', required=True)
    internal.add_argument('--git-tree', required=True)
    internal.add_argument('--verifier-sha256', required=True)
    parsed = parser.parse_args()
    if parsed.mode == '_git-state':
        worker(parsed.root, parsed.git_commit, parsed.git_tree, parsed.verifier_sha256)
    else:
        main(parsed)
