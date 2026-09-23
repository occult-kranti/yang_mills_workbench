#!/usr/bin/env python3
"""Stamp a Round32 contract as frozen_before_production after validating its fields.

  python3 -B research/round32/tools/freeze_contract.py research/round32/contracts/av1.json

Required fields: id, round=32, subround, sequence, title, human_author, model,
parameters, shared_premises (existing repo-relative files), required (non-empty),
controls (non-empty), claim_exclusions (non-empty), producers (["forward","reverse"]
or ["forward"]), direction, preregistration (object), stop. The tool refuses to
re-freeze a contract whose status is already frozen.
"""
import datetime
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def main():
    path = ROOT / sys.argv[1]
    c = json.loads(path.read_text())
    if c.get('status') == 'frozen_before_production':
        raise SystemExit('already frozen: ' + str(path))
    for key in ('id', 'round', 'subround', 'sequence', 'title', 'human_author', 'model', 'parameters',
                'shared_premises', 'required', 'controls', 'claim_exclusions', 'producers', 'direction',
                'preregistration', 'stop'):
        if key not in c:
            raise SystemExit('missing field ' + key)
    if c['round'] != 32 or c['producers'] not in (['forward', 'reverse'], ['forward']):
        raise SystemExit('bad round or producers')
    for name in c['shared_premises']:
        if not (ROOT / name).is_file():
            raise SystemExit('missing premise ' + name)
    for key in ('required', 'controls', 'claim_exclusions'):
        if not c[key]:
            raise SystemExit('empty ' + key)
    c['status'] = 'frozen_before_production'
    c['frozen_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    path.write_text(json.dumps(c, indent=2) + '\n')
    print(json.dumps({'status': 'frozen', 'id': c['id'], 'premises': len(c['shared_premises'])}))


if __name__ == '__main__':
    main()
