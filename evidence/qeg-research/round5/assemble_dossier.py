"""Assemble the reviewed round-5 chapters, without editing prior research."""
from pathlib import Path
from collections import OrderedDict
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent


def main():
    refs = OrderedDict()
    aliases = {}
    urls = {}
    def add(alias, row):
        url = row.get('url', '').rstrip('/')
        if url and url in urls:
            aliases[alias] = urls[url]
            return
        ident = f'D{len(refs)+1:03d}'
        aliases[alias] = ident
        if url: urls[url] = ident
        depth = row.get('read_depth') or row.get('reading_depth') or row.get('readdepth') or row.get('access', '')
        access = row.get('reading_provenance', '')
        limit = row.get('limitation') or row.get('limitations') or row.get('does_not_support', '')
        refs[ident] = {
            'title': row.get('title', alias),
            'authors': row.get('authors', row.get('author', 'Project research record')),
            'date': str(row.get('date') or row.get('year') or 'Date not specified'),
            'url': row.get('url', ''),
            'role': row.get('use') or row.get('supports') or row.get('role', ''),
            'readdepth': 'Reading scope: ' + str(depth),
            'access': ' '.join(str(x) for x in [access, limit] if x),
        }
    for row in json.loads((ROOT/'theorem_advisor_sources.json').read_text()): add(row['id'],row)
    for row in json.loads((ROOT/'search_sources.json').read_text())['sources']: add(row['id'],row)
    for row in json.loads((ROOT/'bridge_sources.json').read_text()): add('BR:'+row['id'],row)
    mapping=json.loads((ROOT/'theory_map.json').read_text())
    for ident,row in mapping['sources'].items():
        if ident not in aliases: add(ident,row)

    def normalize(text, chapter=True):
        def link(m):
            ident=urls.get(m.group(2).rstrip('/'))
            return m.group(1)+' [@'+ident+']' if ident else m.group(0)
        text=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',link,text)
        text=re.sub(r'\[([A-Za-z][A-Za-z0-9:]+)\](?!\()',lambda m:'[@'+aliases[m.group(1)]+']' if m.group(1) in aliases else m.group(0),text)
        if chapter: text=re.sub(r'(?m)^(#{1,5})(\s+)',r'#\1\2',text)
        return text.strip()

    chapters=['overview.md','theory_map.md','theorem_advisor.md','proof_critique.md','search_contract.md','execution_review.md','research_bridge.md','targeted_solver_prompt.md']
    parts=[]
    for name in chapters:
        text=(ROOT/name).read_text()
        if name=='theory_map.md': text=text.split('## Source keys')[0]
        if name=='search_contract.md':
            text=re.sub(r'(?ms)^## 6\..*?(?=^## 8\.)','',text)
        parts.append(normalize(text,chapter=name!='overview.md'))
    guide='\n\n\n'.join(parts)+'\n'
    # TeX ignores this source newline, but the fallback renderer uses physical
    # rows. Keep the two multiplicative factors of T12 visibly together.
    guide=guide.replace(r'\le\frac{|F|}{\sqrt{2z_*}}'+'\n'+r'\sqrt{\frac{W}{W+\epsilon}}',r'\le\frac{|F|}{\sqrt{2z_*}}\sqrt{\frac{W}{W+\epsilon}}')
    guide=guide.replace(r'1+\widehat\chi-\widehat{e^2}\sum_i'+'\n'+r'\frac{\widehat w_i}{4\widehat M_i^3}>3/4.',r'1+\widehat\chi-\widehat{e^2}\sum_i\frac{\widehat w_i}{4\widehat M_i^3}>3/4.')
    # Presentation-only line wrapping for a long map summary equation.
    guide=guide.replace(r'\[ Z(a)>\frac34,\qquad W=\frac12Zx^2+e^2U,\qquad \dot W=xF,\qquad |x(t)|\le\sqrt{\frac{2W_0}{z_*}}+\frac{\|F\|_{L^1(0,t)}}{z_*}. \]',r'\[ Z(a)>\frac34,\qquad W=\frac12Zx^2+e^2U,\qquad \dot W=xF. \]'+ '\n\n' +r'\[ |x(t)|\le\sqrt{\frac{2W_0}{z_*}}+\frac{\|F\|_{L^1(0,t)}}{z_*}. \]')
    used=set(re.findall(r'@([A-Za-z][A-Za-z0-9]+)',guide))
    missing=used-set(refs)
    if missing: raise ValueError(missing)
    (ROOT/'guide.md').write_text(guide)
    (ROOT/'guide_references.json').write_text(json.dumps(refs,indent=2,ensure_ascii=False)+'\n')
    manifest={'date':'2026-09-09','words':len(guide.split()),'sources':len(refs),'cited_ids':sorted(used),'missing_citations':sorted(missing),'inputs':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in chapters},'normalizations':['Consolidated source identifiers and URLs','Chapter heading levels shifted','Map source definitions replaced by consolidated bibliography','Duplicated search-contract theorem sections6–7 omitted; full contract in package','Long map display equation split without algebra changes']}
    (ROOT/'assembly_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'words':manifest['words'],'sources':len(refs),'missing_citations':sorted(missing)}))


if __name__=='__main__': main()
