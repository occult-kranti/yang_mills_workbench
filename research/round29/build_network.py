#!/usr/bin/env python3
"""Append admitted findings to the inherited evidence network."""
import json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
R=ROOT/'research/round29'
p=json.loads((ROOT/'research/round28/network.json').read_text())
f=json.loads((R/'advisor/findings.json').read_text())
registry=json.loads((ROOT/'papers/draft-02/registry/hnm-registry.json').read_text())
contributions=registry['contributions']
equation_registry=registry['equations']
done={x['id'][:2].lower() for x in f['loops']}
for n in p['nodes']:
    if n.get('kind') in ('history','equation','loop'):
        n['legacy_title']=n['title']
        matches=[row for row in contributions if set(row.get('source_paths',[])) & set(n.get('sources',[]))]
        if not matches:
            match=re.fullmatch(r'r(\d+)-(.+)',n['id'])
            if match:
                matches=[row for row in contributions if row.get('round')==int(match.group(1)) and str(row.get('legacy_id','')).lower()==match.group(2)]
        n['hnm_aliases']=[row['id'] for row in matches]
        n['hnm_alias']=matches[0]['id'] if len(matches)==1 else 'HNM-N-'+n['id'].upper()
        n['title']=matches[0]['display_name'] if len(matches)==1 else 'HNM · '+n['title']
    if n['id'].startswith('r28-next-') and (n['id'].split('-')[-1] in done or f.get('planned_next')):
        n['status']='historical-plan'
        n['detail']+=' Current continuation is recorded in Round29; this node preserves the earlier planning record.'
sources=[('src-clay','Clay: continuum existence and physical mass gap','https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf','Official target, not a certificate supplied by this workbench.'),('src-gauvin-v3','Gauvin v3: regulated certificates and conditional transfer','https://arxiv.org/abs/2503.15539v3','External preprint; authorship and model-specific hypotheses remain external. No automatic SU(3) to SU(2) transfer.'),('src-htw','Henheik–Teufel–Wessel: local stability','https://arxiv.org/abs/2106.13780','External theorem application requires matched hypotheses and additional symbolic smallness.')]
if any(row['id'].startswith('AQ') for row in f['loops']):
    sources.append(('src-ns','Nachtergaele–Sims: thermodynamic dynamics','https://arxiv.org/abs/1410.8174v1','Primary unbounded-onsite dynamics theorem used in AQ1. The complete model, interaction norm and physical clock must satisfy its hypotheses.'))
    sources.append(('src-nsy','Nachtergaele–Sims–Young: unbounded-onsite dynamics','https://arxiv.org/abs/1810.02428v2','External local dynamics theorem. Norm convergence for each local observable does not imply norm time continuity on the entire bounded local algebra.'))
for ident,title,url,detail in sources:
    p['nodes'].append({'id':ident,'title':title,'kind':'source','status':'external-source','summary':detail,'detail':detail,'sources':[url],'route':'round29-sources'})
deps={'AL1':['r21-i1','r18-b2'],'AL2':['r29-al1'],'AM1':['r21-i1','r21-i2','src-gauvin-v3'],'AM2':['r29-am1','r28-ag3'],'AN1':['r21-i1','r28-aj1','src-htw'],'AN2':['r29-an1'],'AO1':['r28-ak1','r28-ak2'],'AO2':['r29-ao1','r28-ak2'],'AQ1':['r29-am2','src-gauvin-v3','src-ns','src-nsy'],'AQ2':['r29-aq1','r29-am2','r28-ak1']}
for row in f['loops']:
    ident='r29-'+row['id'].lower()
    p['nodes'].append({'id':ident,'title':row['title'],'hnm_alias':'HNM-C-'+row['id'],'hnm_aliases':['HNM-C-'+row['id']],'kind':'loop','status':row['status'],'summary':row['accepted'],'detail':'\n'.join(row['limitations']),'sources':[row['evidence'],f'research/round29/forward/{row["id"].lower()}/report.md',f'research/round29/reverse/{row["id"].lower()}/report.md'],'route':'round29-'+row['id'].lower()})
    for parent in deps.get(row['id'],[]):
        p['edges'].append({'from':parent,'to':ident,'type':'source-dependency','label':'scoped input','detail':'Inspect the declared source/model map; this edge does not transfer every parent conclusion.'})
    p['edges'].append({'from':ident,'to':'src-clay','type':'scope-boundary','label':'continuum obligations remain','detail':'This investigation is not a continuum Yang–Mills construction.'})
    report=ROOT/f'research/round29/forward/{row["id"].lower()}/report.md'
    for block in re.findall(r'\\\[(.*?)\\\]',report.read_text(),flags=re.S):
        match=re.search(r'\\tag\{(HNM-[^}]+)\}',block)
        if not match: continue
        alias=match.group(1); formula=re.sub(r'\\tag\{[^}]+\}','',block).strip()
        eqid=ident+'-eq-'+alias.rsplit('.',1)[-1].lower()
        records=[item for item in equation_registry if item.get('printed_locator')==alias and 'HNM-C-'+row['id'] in item.get('contribution_ids',[])]
        canonical=records[0]['id'] if len(records)==1 else alias
        p['nodes'].append({'id':eqid,'title':canonical,'hnm_alias':canonical,'hnm_aliases':list(dict.fromkeys([canonical,alias])),'document_locator':alias,'kind':'equation','status':row['status'],'summary':formula,'equation':formula,'detail':'Printed equation '+alias+'. Document alias within the parent loop’s admitted scope. '+ ' '.join(row['limitations']),'sources':[str(report.relative_to(ROOT)),row['evidence']],'route':'round29-'+row['id'].lower()})
        p['edges'].append({'from':ident,'to':eqid,'type':'recorded-equation','label':'scoped equation','detail':'Read the parent proof and limitations; an equation label does not establish priority.'})
for goal in f.get('planned_next',[]):
    ident='r29-next-'+goal['id'].lower()
    p['nodes'].append({'id':ident,'title':'Planned · '+goal['title'],'kind':'open','status':'planned-not-executed','hnm_alias':'HNM-PLAN-'+goal['id'],'summary':goal['target'],'detail':goal.get('missing_premise','')+' '+goal.get('reason_for_rank',''),'sources':['research/round29/advisor/roadmap.json'],'route':'round29-roadmap'})
    for parent in goal.get('dependencies',[]):
        p['edges'].append({'from':parent,'to':ident,'type':'proposed-transfer','label':'planned investigation','detail':'A future question selected after the ten-loop review; this edge is not an established transfer or a completed result.'})
ids=[n['id'] for n in p['nodes']]
if len(ids)!=len(set(ids)): raise ValueError('Duplicate network IDs')
missing={x[k] for x in p['edges'] for k in ('from','to')}-set(ids)
if missing: raise ValueError(f'Dangling network IDs {missing}')
(R/'network.json').write_text(json.dumps(p,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'nodes':len(ids),'edges':len(p['edges']),'reviewed_loops':len(f['loops'])}))
