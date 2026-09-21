#!/usr/bin/env python3
"""Build current presentation data from admitted gates and the stop ledger."""
import json
from pathlib import Path
from admission import ROOT, digest, gate, read, require


def main():
    ledger=read(ROOT/'research/round23/advisor/progress-ledger.json')
    roadmap=read(ROOT/'research/round23/advisor/current-roadmap.json')
    require([x['loop'] for x in ledger['completed_loops']]==['s1','s2','t1','t2'],'four-loop checkpoint required')
    require(ledger['current'] is None and ledger['next_loop_started'] is False
            and ledger['cycle_complete'] is False,'stop boundary changed')
    rows=[]
    for item in ledger['completed_loops']:
        loop=item['loop'];g=gate(loop)
        sha=digest(ROOT/f'research/round23/advisor/{loop}-gate.json')
        require(sha==item['gate_sha256'] and g['status']==item['status'],'ledger differs from gate')
        rows.append({**{k:g[k] for k in ('loop','status','claim','scope','target_verdict','equations','independence','next_missing_premise')},
                     'limits':g.get('limits',[]),'gate_sha256':sha})
    data={'schema':'ym23-presentation-v1','completed':4,'planned':10,'cycle_complete':False,
          'next_started':False,'loops':rows,'roadmap':roadmap,'updated':'2026-09-21'}
    target=ROOT/'dist/research-round23-data.js'
    target.write_text('window.ROUND23_DATA = '+json.dumps(data,indent=2,sort_keys=True)+';\n')
    print(json.dumps({'status':'built','loops':4,'next_started':False}))


if __name__=='__main__': main()
