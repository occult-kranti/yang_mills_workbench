#!/usr/bin/env python3
"""Package an advisor's explicit reviewed decision; does not generate a verdict."""
import argparse
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from admission import ROOT, digest, gate, read, require, source


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--decision', required=True)
    args = parser.parse_args()
    decision = read(source(args.decision))
    loop = decision['loop']
    target = ROOT/f'research/round23/advisor/{loop}-gate.json'
    require(not target.exists(), 'never overwrite an admitted gate')
    require(decision.get('skeptic_review_frozen') is True, 'skeptical review is not frozen')
    files = {}
    def add(name, expected=None):
        actual = digest(source(name))
        require(expected is None or expected == actual, 'source binding mismatch: '+name)
        require(name not in files or files[name] == actual, 'conflicting source binding')
        files[name] = actual
    for name in decision['review_inputs']:
        add(name)
    add(args.decision)
    add(f'research/round23/contracts/{loop}.json')
    for direction in ('forward','reverse'):
        base=f'research/round23/{direction}/{loop}/'
        manifest = read(source(base+'output/source-manifest.json'))
        for name, expected in manifest['inputs'].items():
            add(name, expected)
        for name, expected in manifest['outputs'].items():
            add(base+'output/'+name, expected)
        add(base+'output/source-manifest.json')
        add(base+'submission.json')
    g = {k:v for k,v in decision.items() if k not in ('review_inputs','skeptic_review_frozen')}
    g.update(schema='ym23-gate-v1', files=files)
    target.write_text(json.dumps(g, indent=2, sort_keys=True)+'\n')
    # A packaging error must remain a visible candidate failure, not an admitted result.
    gate(loop)
    print(json.dumps({'loop':loop,'status':g['status'],'files':len(files),'sha256':digest(target)}))


if __name__ == '__main__':
    main()
