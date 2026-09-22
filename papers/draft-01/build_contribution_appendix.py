#!/usr/bin/env python3
"""Render source-bound contribution rows without inventing missing fields."""
from pathlib import Path
import json,re,hashlib
from build_appendices import tex
HERE=Path(__file__).resolve().parent

def strval(x):
    if isinstance(x,list): return '; '.join(map(str,x))
    if isinstance(x,dict): return '; '.join(f'{k}: {v}' for k,v in x.items())
    return str(x) if x is not None else ''

def from_contribution(c,period):
    return {'id':c.get('id',c.get('ID')), 'period':period,
       'group':c.get('group',period), 'title':c.get('title'),
       'status':c.get('classification',c.get('status','See scoped statement in text')),
       'equation_labels':c.get('equation_labels',[]),
       'section_label':c.get('section_label'),
       'application':strval(c.get('application',c.get('applications'))),
       'changed':strval(c.get('changed_understanding',c.get('changed'))),
       'limitation':strval(c.get('limitations',c.get('limitation'))),
       'next':strval(c.get('next_obligation',c.get('next'))),
       'source_paths':c.get('source_paths',[]),
       'rationale':c.get('public_mathematical_rationale',c.get('rationale'))}

def main():
    rows=[];inputs={}
    for name,period in [('early','Origins and finite gauge benchmarks'),('middle','Static, spectral, and local-limit development'),('recent','Full-source, observable, and computed-heat results')]:
        p=HERE/'audit'/f'{name}-ledger.json';d=json.loads(p.read_text());inputs[str(p.relative_to(HERE))]=hashlib.sha256(p.read_bytes()).hexdigest()
        if 'contributions' in d:
            rows.extend(from_contribution(c,period) for c in d['contributions'])
        else:
            for e in d['entries']:
                loc=e['derivation_location']
                rows.append({'id':e['ID'],'period':period,'group':e['group'],
                 'title':e['audit'].get('historical_title',e['ID']),
                 'status':e['status'],'equation_labels':re.findall(r'(?:eq|early|recent):[\w:-]+',e['equation']),
                 'section_label':loc.get('section_label'),'application':e['application'],
                 'changed':e['changed'],'limitation':e['limitation'],'next':e['next'],
                 'source_paths':e['source_paths'],'assumptions':e['assumptions']})
    group_order={}
    for r in rows:
        group_order.setdefault((r['period'],strval(r['group'])),len(group_order))
    rows.sort(key=lambda r:group_order[(r['period'],strval(r['group']))])
    groups={}
    for row in rows:groups.setdefault((row['period'],strval(row['group'])),[]).append(row)
    rows=[row for grouped in groups.values() for row in grouped]
    ids=[r['id'] for r in rows];assert len(ids)==len(set(ids))
    alltex='\n'.join(p.read_text() for p in (HERE/'sections').glob('*.tex') if p.name!='contribution-appendix.tex')
    labels=set(re.findall(r'\\label\{([^}]+)\}',alltex))
    for r in rows:
        for field in ['id','title','application','changed','limitation','next']:
            if not r.get(field):raise ValueError(f'Missing {field} in {r}')
        for label in r['equation_labels']:
            if label not in labels:raise ValueError('Unresolved equation '+label)
        if r['section_label'] and r['section_label'] not in labels:raise ValueError('Unresolved section '+r['section_label'])
    data={'scope':'Grouped workbench contributions and scoped loop increments; not a count of discoveries',
       'count':len(rows),'star_meaning':'Original-to-workbench only; scientific priority unverified',
       'input_sha256':inputs,'contributions':rows}
    (HERE/'audit/contribution-catalog.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    out=[r'\section{Contribution catalog, applications, and remaining obligations}',r'\label{app:contributions}',
       'The double star marks workbench derivation, computation, repair, or specialization; it does not assert literature priority. Related early studies are consolidated; later loop increments remain separately indexed and grouped by subject. Every row points to a derivation or source and states a possible application, the change from earlier understanding, and a remaining obligation. Application means a supported mathematical use or proposed use within the stated model, not a measured technological benefit. The separate skeptical ledger records the level of fresh verification. Additional claim details and source paths are retained in '+r'\repo{audit/contribution-catalog.json}'+'.',
       r'\begingroup\footnotesize\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.14}',
       r'\begin{longtable}{@{}p{.29\textwidth}p{.32\textwidth}p{.34\textwidth}@{}}',
       r'\caption{Organized contributions and their limits.}\label{tab:contributions}\\',
       r'\toprule Contribution and derivation & Application and change & Limitation and next obligation \\ \midrule\endfirsthead',
       r'\toprule Contribution and derivation & Application and change & Limitation and next obligation \\ \midrule\endhead',
       r'\midrule\multicolumn{3}{r}{Continued on next page}\\\endfoot',r'\bottomrule\endlastfoot']
    last=None
    for r in rows:
        group=r['period']+' / '+strval(r['group']) if r['group']!=r['period'] else r['period']
        if group!=last:
            out.append(r'\multicolumn{3}{@{}p{.98\textwidth}@{}}{\textbf{'+tex(group)+r'}}\\*\addlinespace');last=group
        a=r'\textbf{'+tex(r['id'])+r'}\workstar\par '+tex(r['title'])
        if r['equation_labels']:
            a+=r'\par Eqs. '+', '.join(r'\eqref{'+x+'}' for x in r['equation_labels'])+'.'
        elif r['section_label']:a+=r'\par Section~\ref{'+r['section_label']+'}.'
        a+=r'\par\emph{Scope:} '+tex(r['status'])
        b=r'\emph{Use:} '+tex(r['application'])+r'\par\emph{Change:} '+tex(r['changed'])
        c=tex(r['limitation'])+r'\par\emph{Next:} '+tex(r['next'])
        if r['source_paths']:a+=r'\par\repo{'+r['source_paths'][0]+'}'
        out.append(a+' & '+b+' & '+c+r' \\ \addlinespace')
    out.append(r'\end{longtable}\endgroup')
    (HERE/'sections/contribution-appendix.tex').write_text('\n'.join(out)+'\n')
    print(json.dumps({'contributions':len(rows),'source_ledgers':len(inputs),'equation_refs':sum(len(r['equation_labels']) for r in rows)}))

if __name__=='__main__':main()
