#!/usr/bin/env python3
"""Build current research presentation only from ten admitted scientific gates."""
from pathlib import Path
import json
import sys

sys.dont_write_bytecode = True
from admission import ROOT, LOOPS, digest, gate, read, require, source
from presentation_schema import loop_metadata, future_roadmap


def main():
    metadata = read(source('research/round22/site-data.json'))
    rows = []
    for loop in LOOPS:
        g = gate(loop)
        item = loop_metadata(metadata['loops'][loop], loop)
        rows.append({**item, **{k:g[k] for k in ('loop','status','claim','scope','equations',
                    'target_verdict','next_missing_premise','independence')},
                    'limitations':g.get('limits',[]),
                    'gate_sha256':digest(source(f'research/round22/advisor/{loop}-gate.json')),
                    'bound_files':len(g['files']),
                    'contract':read(source(f'research/round22/contracts/{loop}.json'))})
    ledger = read(source('research/round22/advisor/progress-ledger.json'))
    require(type(ledger['completed_research_loops']) is int and ledger['completed_research_loops'] == 10, 'cycle incomplete')
    roadmap = future_roadmap(read(source('research/round22/advisor/post-ten-roadmap.json')))
    data = {**{k:v for k,v in metadata.items() if k != 'loops'}, 'loops':rows,
            'completed':10, 'accepted':sum(r['status']=='accepted' for r in rows),
            'limited':sum(r['status']=='limited' for r in rows),
            'rejected':sum(r['status']=='rejected' for r in rows), 'next':roadmap,
            'source_sha256':digest(source('research/round22/site-data.json'))}
    text = json.dumps(data, sort_keys=True, ensure_ascii=False).replace('<','\\u003c')
    (ROOT/'dist/research-round22-data.js').write_text('window.ROUND22_DATA = '+text+';\n')
    print(json.dumps({'status':'built','reviewed_loops':10,'accepted':data['accepted'],
                      'limited':data['limited']}))


if __name__ == '__main__':
    main()
