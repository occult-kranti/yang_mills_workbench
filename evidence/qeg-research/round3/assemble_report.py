#!/usr/bin/env python3
"""Assemble project-authored chapters and normalize source provenance."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
PRIOR = ROOT.parent / 'retry'

def read(name):
    return (ROOT / name).read_text()

def subordinate(text):
    return re.sub(r'^(#{1,5}) ', lambda m: m[1]+'# ', text, flags=re.M)

old_contract = (PRIOR / 'chapters/contract.md').read_text()
master = '## The target as an initial-value problem' + old_contract.split('## The target as an initial-value problem', 1)[1]
master = master.replace('### The missing causal closure', '### Causal closure and the part now computed')
master = master.replace('### Local terms and their status', 'For the displayed Dirac operator with signature $(-+++)$, choose $\\{\\gamma^\\mu,\\gamma^\\nu\\}=-2g^{\\mu\\nu}$ and $D_\\mu=\\nabla^{\\rm spin}_\\mu-ieA_\\mu$. This choice reproduces the positive-charge reduced Hamiltonian with kinetic momentum $k-eA_z$. The retarded kernels below include the invariant integration density in their second argument, so the displayed $d^4y$ denotes the density-weighted kernel convention.\n\n### Local terms and their status')
master = master.replace('The strong-field, strong-curvature kernels are the unresolved computational objects.', 'The fully strong-curvature current/stress kernels remain unresolved. The following homogeneous flat-space model now computes a restricted causal electromagnetic response and backreaction, with the metric held fixed.')
master = master.replace('Four original research fronts remain active. The new finite-field and real-time calculations below make progress on two missing mechanisms without asserting that their outputs already close the entire system.', 'The four original research fronts remain active. The following theory and numerical chapters close a restricted electromagnetic loop; the gravity chapter states the additional stress and state dependencies needed for the full system.')
(ROOT/'chapters/01_master_action.md').write_text(master)

advisor = read('advisor.md')
final_review = '## Advisor acceptance and disposition' + advisor.split('## Final review of the executed causal calculation', 1)[1]
final_review = final_review.replace('Maximum matched-current-history change', 'Maximum effective-numerator-history change')
final_review = final_review.replace('matched-current history', 'effective-numerator history')
final_review += '\nThe final nomenclature audit distinguishes the full current from the effective Maxwell numerator. For the fixed-window refinement the full matter-current difference is $1.1315\\times10^{-6}$ in $j/(em^3)$ units; the numerator difference is $1.1270\\times10^{-6}$. The detailed results chapter gives the reconstruction.\n'

names = ['chapters/00_result.md','chapters/01_master_action.md','chapters/02_fronts.md','theory.md','chapters/04_computations.md','verifier.md','chapters/06_quantum_comparator.md','gravity.md','sources_challenge.md','ai_methods.md','chapters/09_next_steps.md','astra_solver_prompt.md']
parts = []
for n in names:
    s=read(n)
    if n in ['gravity.md','sources_challenge.md','ai_methods.md']:
        s=subordinate(s)
    parts.append(s)
parts.append(final_review)
report='\n\n'.join(parts)

ledgers = ['sources_root.json','sources_theory.json','sources_verifier.json','sources_gravity.json','sources_empirical.json','sources_ai.json']
all_refs = {}
for n in ledgers:
    d=json.loads(read(n))
    entries=d.items() if isinstance(d,dict) else ((x['id'],x) for x in d)
    for ident,r in entries:
        r=dict(r)
        r.pop('id',None)
        r['date']=str(r.get('date',r.get('year','n.d.')))
        r['readdepth']=r.get('readdepth',r.get('read_depth',r.get('access','Reading depth not specified; do not assume complete reading.')))
        r['role']=r.get('role',r.get('type',r.get('claim','Primary source or documented comparison')))
        r['access']=r.get('access',r.get('limitation','See reading-depth qualification.'))
        all_refs[ident]=r
all_refs['N02']['title']='Pair creation in electric fields, renormalization, and backreaction'
all_refs['N02']['metadata_check']='Primary arXiv abstract title/authors rechecked 2026-09-09.'
old=json.loads((PRIOR/'references.json').read_text())
for k,r in old.items():
    if k not in all_refs:
        r=dict(r)
        r['readdepth']='Retained from the preceding project cycle: '+str(r.get('readdepth',r.get('access','see archived source ledger')))
        all_refs[k]=r

# Retain distinct inspected versions; merge only identical URL records.
url_id={}
aliases={}
for ident,r in all_refs.items():
    url=r.get('url','')
    if url and url in url_id:
        first=url_id[url];aliases[ident]=first
        if ident[0] in 'NCVHEA' and ident not in old:
            all_refs[first]['readdepth'] += ' Additional review ('+ident+'): '+r['readdepth']
    elif url:
        url_id[url]=ident

report=re.sub(r'\[([^\]\n]+)\]\((https?://[^\s)]+)\)',lambda m:m[1]+' [@'+url_id[m[2]]+']' if m[2] in url_id else m[0],report)
report=re.sub(r'\[@([^\]]+)\]',lambda m:'['+'; '.join('@'+aliases.get(k.strip().lstrip('@'),k.strip().lstrip('@')) for k in m[1].split(';'))+']',report)
used=[]
for block in re.findall(r'\[(@[^\]]+)\]',report):
    for k in block.split(';'):
        k=k.strip().lstrip('@')
        if k not in used:used.append(k)
missing=[k for k in used if k not in all_refs]
if missing:raise ValueError('Unknown citations '+repr(missing))
refs={k:all_refs[k] for k in used}
(ROOT/'references.json').write_text(json.dumps(refs,indent=2,ensure_ascii=False)+'\n')
(ROOT/'report.md').write_text(report)
(ROOT/'assembly_manifest.json').write_text(json.dumps({'chapter_inputs':names+['advisor.md (final review only)'],'references':len(refs),'approximate_words':len(report.split()),'missing_citations':missing,'exact_url_aliases':aliases,'retained_prior_source_ids':[k for k in refs if k in old]},indent=2)+'\n')
print(json.dumps({'references':len(refs),'words':len(report.split()),'missing':missing}))
