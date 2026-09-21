"""Build the current reading interface from source-bound project evidence."""
from pathlib import Path
import hashlib,html,json,re
ROOT=Path(__file__).resolve().parents[2]
R=ROOT/'research/round25'
def inline(s):
    s=html.escape(s)
    s=re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)',r'<a href="\2" target="_blank" rel="noopener noreferrer">\1 ↗</a>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
    return re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
def prose(text):
    blocks=[]
    for b in text.strip().split('\n\n'):
        if b.startswith('#'):
            level=min(4,len(b)-len(b.lstrip('#'))+1)
            blocks.append(f'<h{level}>'+inline(b.lstrip('# '))+f'</h{level}>')
        elif b.startswith('    '):blocks.append('<pre>'+html.escape('\n'.join(x[4:] for x in b.splitlines()))+'</pre>')
        elif b.startswith('|'):
            rows=[x for x in b.splitlines() if not re.fullmatch(r'[| :\-]+',x)]
            parts=[]
            for i,row in enumerate(rows):
                tag='th' if i==0 else 'td'
                parts.append('<tr>'+''.join(f'<{tag}>'+inline(x.strip())+f'</{tag}>' for x in row.strip('|').split('|'))+'</tr>')
            blocks.append('<div class="r23-table-wrap"><table class="r23-table">'+''.join(parts)+'</table></div>')
        elif b.startswith('- '):blocks.append('<ul>'+''.join('<li>'+inline(x[2:])+'</li>' for x in b.splitlines())+'</ul>')
        else:blocks.append('<p>'+inline(b).replace('\n',' ')+'</p>')
    return '\n'.join(blocks)
def main():
    history=json.loads((R/'all-results.json').read_text())
    for name,sha in history['source_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('history source changed '+name)
    loops=[]
    for loop in ['aa1','aa2']:
        gate=json.loads((R/f'advisor/{loop}-gate.json').read_text())
        for name,sha in gate['sha256'].items():
            if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=sha:raise ValueError('gate source changed '+name)
        loops.append({'loop':loop,'verdict':gate['verdict'],'accepted':gate['accepted'],
            'report_html':prose((R/f'solo/{loop}/report.md').read_text()),
            'gate_sha256':hashlib.sha256((R/f'advisor/{loop}-gate.json').read_bytes()).hexdigest()})
    data={'history':history,'loops':loops,'sources':json.loads((R/'sources.json').read_text()),
      'roadmap':json.loads((R/'advisor/roadmap.json').read_text()),
      'resonance_html':prose((R/'RESONANCE_AND_HISTORY.md').read_text()),
      'use_html':prose((R/'USE_AND_NEXT_GOALS.md').read_text()),
      'aa':json.loads((R/'solo/aa2/output/results.json').read_text())}
    (ROOT/'dist/research-round25-data.js').write_text('window.ROUND25_DATA = '+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/')+';\n')
    print(json.dumps({'built':'round25','history_entries':history['counts']['entries'],'new_physics_loops':2}))
if __name__=='__main__':main()
