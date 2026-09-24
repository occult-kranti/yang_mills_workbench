#!/usr/bin/env python3
"""Write an advisor gate for a reviewed Round33 loop with complete evidence bindings.

  python3 -B research/round33/tools/record_gate.py av1 --sequence 1 --subround 1 \
      --verdict accepted_within_scope --title "..." --model "..." --decision "..." \
      --producers forward reverse

The accepted statement and limitations are copied from the skeptic review
(skeptic/<loop>.json: supported_statement, limitations) so the gate can never
widen the reviewed scope. Bindings hash every producer closure, the contract,
selection note, skeptic files and every declared premise.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ROUND = Path('research/round33')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('loop')
    ap.add_argument('--sequence', type=int, required=True)
    ap.add_argument('--subround', type=int, required=True)
    ap.add_argument('--verdict', required=True, choices=('accepted_within_scope', 'limited', 'insufficient'))
    ap.add_argument('--title', required=True)
    ap.add_argument('--model', required=True)
    ap.add_argument('--decision', required=True)
    ap.add_argument('--producers', nargs='+', default=('forward', 'reverse'))
    ap.add_argument('--review-fields', nargs='*', default=(),
                    help='keys copied verbatim from the skeptic review JSON (e.g. sub_label gate_fields)')
    a = ap.parse_args()
    loop = a.loop.lower()
    review = json.loads((ROOT / ROUND / 'skeptic' / (loop + '.json')).read_text())
    if review.get('blocking_issues'):
        raise SystemExit('skeptic review has blocking issues; repair before gating')
    bindings = {}
    names = set()
    names.add(str(ROUND / 'contracts' / (loop + '.json')))
    names.add(str(ROUND / 'advisor' / f'selection-{loop}.md'))
    for q in (ROOT / ROUND / 'skeptic').iterdir():
        if q.is_file() and q.name.startswith(loop) and '__pycache__' not in q.parts:
            names.add(q.relative_to(ROOT).as_posix())
        if q.is_dir() and q.name.startswith(loop):
            for r in q.rglob('*'):
                if r.is_file() and '__pycache__' not in r.parts:
                    names.add(r.relative_to(ROOT).as_posix())
    contract = json.loads((ROOT / ROUND / 'contracts' / (loop + '.json')).read_text())
    names.update(contract.get('shared_premises', []))
    names.add('AGENTS.md')
    for side in a.producers:
        p = ROOT / ROUND / side / loop
        fz = json.loads((p / 'freeze.json').read_text())
        names.update(fz['sources'])
        names.add(str(ROUND / side / loop / 'freeze.json'))
    for name in sorted(names):
        path = ROOT / name
        if not path.is_file():
            raise SystemExit('missing evidence ' + name)
        bindings[name] = sha(path)
    gate = {
        'loop': loop.upper(), 'sequence': a.sequence, 'subround': a.subround,
        'title': a.title, 'verdict': a.verdict,
        'accepted': review['supported_statement'], 'limitations': review['limitations'],
        'model': a.model, 'producers': list(a.producers),
        'reviewer_path': str(ROUND / 'skeptic' / (loop + '.md')),
        'decision': a.decision,
        'completed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'bindings': bindings,
    }
    for key in a.review_fields:
        if key not in review:
            raise SystemExit('review field missing ' + key)
        gate[key] = review[key]
    out = ROOT / ROUND / 'advisor' / f'{loop}-gate.json'
    out.write_text(json.dumps(gate, indent=2) + '\n')
    print(json.dumps({'status': 'gated', 'loop': loop, 'bindings': len(bindings)}))


if __name__ == '__main__':
    main()
