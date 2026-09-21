#!/usr/bin/env python3
"""Build Round24 pages only from independently reviewed, admitted evidence."""
import html,json,re
from admission import ROOT,ROUND,LOOPS,gate,digest,read,require

def prose(text):
    def inline(s):
        s=html.escape(s)
        s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
        return re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    blocks=[]
    for b in text.strip().split('\n\n'):
        if b.startswith('#'):
            level=min(4,len(b)-len(b.lstrip('#'))+1)
            blocks.append(f'<h{level}>'+inline(b.lstrip('# '))+f'</h{level}>')
        elif b.startswith('    '): blocks.append('<pre>'+html.escape('\n'.join(x[4:] for x in b.splitlines()))+'</pre>')
        else: blocks.append('<p>'+inline(b).replace('\n','<br>')+'</p>')
    return '\n'.join(blocks)

def main():
    summary=read(ROOT/f'{ROUND}/advisor/contributions.json')
    require([item['loop'] for item in summary['loops']]==list(LOOPS),'final site requires each of the ten reviewed loops exactly once')
    review=read(ROOT/f'{ROUND}/advisor/presentation-review.json')
    require(review.get('reviewed') is True and review.get('reviewer')=='root advisor','missing presentation review')
    require(f'{ROUND}/advisor/contributions.json' in review['files'],'unbound presentation claims')
    for name,expected in review['files'].items():require(digest(ROOT/name)==expected,'presentation changed after review: '+name)
    rows=[]
    for item in summary['loops']:
        loop=item['loop'];g=gate(loop)
        require(item['verdict']==g['verdict'],'presentation verdict mismatch')
        rows.append({**item,'gate_sha256':digest(ROOT/f'{ROUND}/advisor/{loop}-gate.json'),
            'forward_html':prose((ROOT/f'{ROUND}/forward/{loop}/report.md').read_text()),
            'reverse_html':prose((ROOT/f'{ROUND}/reverse/{loop}/report.md').read_text()),
            'review_html':prose((ROOT/f'{ROUND}/skeptic/{loop}-review.md').read_text())})
    data={**summary,'loops':rows,'roadmap':read(ROOT/f'{ROUND}/advisor/roadmap.json')}
    (ROOT/'dist/research-round24-data.js').write_text('window.ROUND24_DATA = '+json.dumps(data,indent=2,sort_keys=True)+';\n')
    print(json.dumps({'status':'built','reviewed_loops':len(rows)}))
if __name__=='__main__': main()
