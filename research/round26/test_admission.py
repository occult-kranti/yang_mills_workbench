"""Discriminating structural mutations of current admission metadata."""
import copy
import json
import tempfile
from pathlib import Path
from admission import ROOT, R, LOOPS, metadata, review_agreement, require, hashes, gate, producer_inventory, source


def reject(f):
    try:
        f()
    except (ValueError, KeyError):
        return
    raise ValueError('invalid evidence was admitted')


def main():
    checked = 0
    for loop in LOOPS:
        if not (R / f'advisor/{loop}-gate.json').exists():
            continue
        g = gate(loop)
        c = json.loads((R / f'contracts/{loop}.json').read_text())
        review = json.loads((R / f'skeptic/{loop}.json').read_text())
        for suffix in [f'forward/{loop}/report.md', f'reverse/{loop}/check.py',
                       f'skeptic/{loop}.md', f'contracts/{loop}-freeze.json',
                       f'forward/{loop}/output/results.json']:
            bad = copy.deepcopy(g); bad['sha256'].pop('research/round26/' + suffix)
            reject(lambda: metadata(bad, c, loop)); checked += 1
        for key, value in [('normal_optimized_equal', False), ('verdict', 'solved_yang_mills'),
                           ('limitations', []), ('limitations', 'none'), ('accepted', True),
                           ('review', 'independent peer review')]:
            bad = copy.deepcopy(g); bad[key] = value
            reject(lambda: metadata(bad, c, loop)); checked += 1
        bad = copy.deepcopy(g); bad['accepted'] = 'The continuum problem is solved.'
        reject(lambda: review_agreement(bad, review)); checked += 1
        bad_review = copy.deepcopy(review); bad_review['blocking_issues'] = ['missing exterior channel']
        reject(lambda: review_agreement(g, bad_review)); checked += 1
        for malformed in ['', None, {}]:
            bad_review = copy.deepcopy(review); bad_review['blocking_issues'] = malformed
            reject(lambda: review_agreement(g, bad_review)); checked += 1
        if loop.endswith('2'):
            bad_c = copy.deepcopy(c)
            bad_c['bindings'].pop(f'research/round26/advisor/{loop[:-1]}1-gate.json')
            reject(lambda: metadata(g, bad_c, loop)); checked += 1
        if loop in ['ae1', 'af1']:
            bad_c = copy.deepcopy(c); bad_c['bindings'].pop('research/round26/advisor/ad2-gate.json')
            reject(lambda: metadata(g, bad_c, loop)); checked += 1
    reject(lambda: hashes({})); checked += 1
    reject(lambda: hashes({'../untrusted': '0' * 64})); checked += 1
    reject(lambda: producer_inventory({'bindings': {'p': 'a'}, 'source_inventory': {'p': 'b'}})); checked += 1
    with tempfile.TemporaryDirectory(prefix='admission-link-test-', dir=R) as temp:
        link = Path(temp) / 'linked-parent'; link.symlink_to(R, target_is_directory=True)
        reject(lambda: source(str((link / 'contracts/ab1.json').relative_to(ROOT)))); checked += 1
    require(checked > 2, 'no gates tested')
    print(json.dumps({'status': 'passed', 'rejected_mutations': checked,
                      'scope': 'missing proofs, scope inflation, discarded review objections and feedback order'}))


if __name__ == '__main__':
    main()
