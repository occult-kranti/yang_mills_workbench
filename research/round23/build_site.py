#!/usr/bin/env python3
"""Build current presentation data from admitted gates and the stop ledger."""
import json
import html
import re
from pathlib import Path
from admission import ROOT, digest, gate, read, require


def prose(text):
    """Render the small trusted Markdown subset used in these research essays."""
    def inline(s):
        s=html.escape(s)
        s=re.sub(r'\[([^\]]+)\]\((https://(?:[^\s()]|\([^()]*\))+)\)',r'<a href="\2">\1 ↗</a>',s)
        s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
        return re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    blocks=[]
    for block in text.strip().split('\n\n'):
        if block.startswith('#'):
            level=min(4,len(block)-len(block.lstrip('#'))+1)
            blocks.append(f'<h{level}>'+inline(block.lstrip('# '))+f'</h{level}>')
        elif block.startswith('    '):
            blocks.append('<pre>'+html.escape('\n'.join(x[4:] for x in block.splitlines()))+'</pre>')
        else:
            blocks.append('<p>'+inline(block).replace('\n','<br>')+'</p>')
    return '\n'.join(blocks)


def main():
    ledger=read(ROOT/'research/round23/advisor/progress-ledger.json')
    roadmap=read(ROOT/'research/round23/advisor/current-roadmap.json')
    require([x['loop'] for x in ledger['completed_loops']]==['s1','s2','t1','t2','u1','u2'],'six-loop checkpoint required')
    require(ledger['current'] is None and ledger['next_loop_started'] is False
            and ledger['cycle_complete'] is False,'stop boundary changed')
    rows=[]
    for item in ledger['completed_loops']:
        loop=item['loop'];g=gate(loop)
        sha=digest(ROOT/f'research/round23/advisor/{loop}-gate.json')
        require(sha==item['gate_sha256'] and g['status']==item['status'],'ledger differs from gate')
        rows.append({**{k:g[k] for k in ('loop','status','claim','scope','target_verdict','equations','independence','next_missing_premise')},
                     'limits':g.get('limits',[]),'gate_sha256':sha})
    documents={}
    for key,name in {
        'newton':'research/round23/methods/u-v1/newton-analysis-synthesis-research.md',
        'tesla':'research/round23/methods/u-v1/tesla-mechanism-resonance-research.md',
        'u1':'research/round23/forward/u1/report.md',
        'u2':'research/round23/forward/u2/report.md'}.items():
        documents[key]={'path':name,'sha256':digest(ROOT/name),'html':prose((ROOT/name).read_text())}
    cert=read(ROOT/'research/round23/forward/u2/output/results.json')
    data={'schema':'ym23-presentation-v1','completed':6,'planned':10,'cycle_complete':False,
          'next_started':False,'loops':rows,'roadmap':roadmap,'updated':'2026-09-21',
          'documents':documents,'endpoint_certificates':cert['finite_q_certificates'],
          'liminf_lower_at_cap':cert['liminf_lower_at_cap']}
    target=ROOT/'dist/research-round23-data.js'
    target.write_text('window.ROUND23_DATA = '+json.dumps(data,indent=2,sort_keys=True)+';\n')
    print(json.dumps({'status':'built','loops':6,'next_started':False}))


if __name__=='__main__': main()
