#!/usr/bin/env python3
"""Verify the exact committed Round30 source tree from a clean checkout."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def tree_files(path):
    return {str(p.relative_to(path)): sha(p) for p in sorted(path.rglob('*')) if p.is_file()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--baseline', required=True)
    ap.add_argument('--expected-tree', required=True)
    ap.add_argument('--receipt', required=True, type=Path)
    a = ap.parse_args()
    need(a.receipt.is_absolute() and not a.receipt.exists(), 'Fresh absolute receipt required')
    need(not a.receipt.resolve().is_relative_to(ROOT.resolve()), 'Receipt must be external')
    need(not git('status', '--porcelain'), 'Release source must be clean')
    commit, tree = git('rev-parse', 'HEAD'), git('rev-parse', 'HEAD^{tree}')
    need(tree == a.expected_tree, 'Wrong committed tree')
    changed = git('diff', '--name-only', a.baseline, 'HEAD').splitlines()
    # The entire earlier science and manuscript are immutable. Only current
    # presentation integration, added current work and tests may change.
    protected = [p for p in changed if p.startswith(('research/', 'papers/', 'evidence/', '.codex/'))
                 and not p.startswith(('research/round30/', 'papers/draft-03/'))]
    need(not protected, 'Historical scientific bytes changed: ' + str(protected))
    checks = []
    with tempfile.TemporaryDirectory(prefix='hnm-round30-release-') as temporary:
        external = Path(temporary)
        archive = external / 'tree.tar'
        with archive.open('wb') as stream:
            subprocess.run(['git', 'archive', 'HEAD'], cwd=ROOT, stdout=stream, check=True)
        work = external / 'source'
        work.mkdir()
        with tarfile.open(archive) as tf:
            tf.extractall(work, filter='data')

        def run(name, command):
            done = subprocess.run(command, cwd=work, capture_output=True, text=True,
                                  env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
            need(done.returncode == 0, name + ': ' + done.stdout[-1500:] + done.stderr[-2500:])
            checks.append({'name': name, 'exit_code': done.returncode,
                           'stdout': done.stdout.strip().replace(str(external), '<external>')})

        run('three-source-bound-admissions', [sys.executable, '-B', 'research/round30/reproduce.py', '--complete', '--validate-only'])
        run('damaging-evidence-controls', [sys.executable, '-B', 'research/round30/test_admission.py'])
        run('damaging-evidence-controls-optimized', [sys.executable, '-B', '-O', 'research/round30/test_admission.py'])
        for mode in ('normal', 'optimized'):
            flags = ['-O'] if mode == 'optimized' else []
            extra = ['--optimized'] if flags else []
            run('producer-replay-' + mode, [sys.executable, '-B', *flags, 'research/round30/reproduce.py', '--complete', *extra,
                                           '--output', str(external / mode)])
        # The inherited source validator is read-only; no earlier producers are
        # rerun because their exact protected tree was separately released.
        run('inherited-round29-integrity', [sys.executable, '-B', 'research/round29/reproduce.py', '--complete', '--validate-only'])
        before_network = (work / 'research/round30/network.json').read_bytes()
        before_dist, before_docs = tree_files(work / 'dist'), tree_files(work / 'docs')
        run('network-rebuild', [sys.executable, '-B', 'research/round30/build_network.py'])
        need((work / 'research/round30/network.json').read_bytes() == before_network, 'Network rebuild differs')
        run('current-site-rebuild', [sys.executable, '-B', 'research/round30/presentation/build_site.py'])
        run('pages-rebuild', [sys.executable, '-B', 'scripts/build_pages.py'])
        need(tree_files(work / 'dist') == before_dist and tree_files(work / 'docs') == before_docs,
             'Generated site differs from committed assets')
        run('current-interface', ['node', 'tests/round30_site.mjs'])
        run('historical-round29-interface', ['node', 'tests/round29_site.mjs'])
        site_qa_path = work / 'research/round30/presentation/site-qa-final.json'
        site_qa = json.loads(site_qa_path.read_text())
        need(site_qa.get('status') == 'passed' and site_qa.get('mode') == 'final_source_render',
             'Final browser QA missing')
        need(site_qa.get('checkpoint', {}).get('completed') == 3
             and site_qa.get('pageErrors') == []
             and site_qa.get('visual_review', {}).get('status') == 'passed',
             'Incomplete browser/visual review')
        browser_sources = site_qa.get('source_sha256', {})
        required_sources = {'research/round30/presentation/build_site.py',
                            'research/round30/advisor/findings.json',
                            'research/round30/network.json',
                            'papers/draft-03/registry/hnm-registry.json',
                            'papers/draft-03/main.pdf', 'tests/round30_browser.mjs',
                            'tests/round30_site.mjs', 'scripts/build_pages.py'}
        required_sources |= {folder + '/' + name for folder in ('dist', 'docs')
                             for name in ('index.html', 'research-round30.js',
                                          'research-round30.css', 'research-round30-data.js',
                                          'hnm-registry-r30.json', 'ym-draft-03.pdf')}
        need(required_sources <= browser_sources.keys(), 'Browser QA omits current sources')
        screenshots = site_qa.get('screenshot_sha256', {})
        expected_pngs = {'home-desktop.png', 'home-mobile.png', 'sources-mobile.png',
                         'catalog-mobile.png', 'network-mobile.png', 'result-mobile.png',
                         'calculator-mobile.png'}
        need({Path(name).name for name in screenshots} == expected_pngs
             and expected_pngs <= set(site_qa['visual_review'].get('screenshots_inspected', [])),
             'Incomplete screenshot inspection')
        for name, expected in {**browser_sources, **screenshots}.items():
            need(not Path(name).is_absolute() and '..' not in Path(name).parts,
                 'Unsafe browser evidence path')
            component = work
            for part in Path(name).parts:
                component = component / part
                need(not component.is_symlink(), 'Symlink browser evidence component')
            need(component.is_file() and sha(component) == expected,
                 'Changed browser evidence: ' + name)
        checked_routes = {row['route'] for row in site_qa.get('checks', [])
                          if row.get('mobileOverflow') is False}
        expected_routes = {'home', 'drafts', 'round30-results', 'round30-roadmap',
                           'round30-sources', 'round30-proof', 'round30-calculator',
                           'hnm-findings', 'hnm-priorities', 'research-network',
                           'round29', 'round29-aq2', 'round30-at1', 'round30-at2', 'round30-at3'}
        need(expected_routes <= checked_routes, 'Browser QA omits current/archive routes')
        checks.append({'name': 'recorded-final-browser-and-visual-review',
                       'sha256': sha(site_qa_path), 'screenshots': len(screenshots),
                       'routes': len(checked_routes)})
        paper = work / 'papers/draft-03/main.pdf'
        need(paper.read_bytes().startswith(b'%PDF-'), 'Missing current PDF')
        need(paper.read_bytes() == (work / 'dist/ym-draft-03.pdf').read_bytes()
             == (work / 'docs/ym-draft-03.pdf').read_bytes(), 'PDF downloads differ')
        qa = json.loads((work / 'papers/draft-03/pdf-qa.json').read_text())
        need(qa['pdf_sha256'] == sha(paper), 'QA does not bind final PDF')
        need(qa.get('references_resolved') is True and not qa.get('overfull_warnings'), 'PDF reference/layout warnings')
        need(qa.get('status') == 'passed' and qa.get('visual_review') == 'passed', 'PDF visual review not passed')
        need(qa.get('all_page_geometry_checked') is True and not qa['geometry']['out_of_media_text'], 'PDF geometry failure')
        need(set(qa['rendered_pages']) <= set(qa['inspected_pages']), 'Rendered pages not inspected')
        manifest = json.loads((work / 'papers/draft-03/artifact-manifest.json').read_text())
        need(manifest['pdf_sha256'] == sha(paper), 'Artifact manifest binds another PDF')
        for inventory_name in ('source_inventory', 'sha256'):
            need(bool(manifest.get(inventory_name)), 'Missing artifact inventory')
            for name, expected in manifest[inventory_name].items():
                path = work / name
                need(path.resolve().is_relative_to(work.resolve()) and path.is_file()
                     and sha(path) == expected, 'Changed PDF-bound artifact: ' + name)
        need(sha(work / manifest['review_record']) == manifest['review_sha256'], 'Changed visual review record')
        checks.append({'name': 'current-pdf-and-exact-downloads', 'sha256': sha(paper), 'qa_status': qa['status']})
    need(not git('status', '--porcelain'), 'Source checkout changed during release')
    receipt = {'status': 'passed', 'commit': commit, 'tree': tree, 'baseline': a.baseline,
               'research_loops': 3, 'producer_replays': 12, 'historical_science_preserved': True,
               'checks': checks, 'scope': 'Exact source, reviewed claims, arithmetic replays, deterministic website and bound PDF. Not a formal mathematical proof or external human peer review.'}
    a.receipt.parent.mkdir(parents=True, exist_ok=True)
    a.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'checks'}))


if __name__ == '__main__':
    main()
