"""Build the additive Round27 presentation from three reviewed gates."""
from pathlib import Path
import json
from hashlib import sha256

ROOT=Path(__file__).resolve().parents[2]
R=ROOT/'research/round27'

def digest(path): return sha256(path.read_bytes()).hexdigest()
def load(path): return json.loads(path.read_text())
def require(ok, message):
    if not ok: raise ValueError(message)

def build():
    summaries=load(R/'advisor/summaries.json')
    sequence=load(R/'advisor/sequence.json')['loops']
    require(len(sequence)==3 and len(set(sequence))==3,'exactly three loops required')
    network=load(ROOT/'research/round26/network.json')
    loops=[]
    for loop in sequence:
        gate=load(R/f'advisor/{loop}-gate.json')
        require(gate['verdict'].startswith('accepted'),'reviewed scoped gate required')
        for name, expected in gate['bindings'].items():
            require(digest(ROOT/name)==expected,'changed gate input '+name)
        row={**summaries[loop], 'id':loop, 'verdict':gate['verdict'],
             'accepted':gate['accepted'], 'limitations':gate['limitations'],
             'sources':[f'research/round27/{side}/{loop}/report.md' for side in ['forward','reverse']]+[f'research/round27/skeptic/{loop}.md',f'research/round27/advisor/{loop}-gate.json']}
        loops.append(row)
        node='r27-'+loop
        network['nodes'].append({'id':node,'title':loop.upper()+' · '+row['title'],'kind':'loop','status':'limited',
              'summary':row['accepted'],'detail':'\n'.join(row['limitations']),'sources':row['sources'],'route':'round27-'+loop,'model':gate['model']})
        for dep in gate['network_dependencies']:
            network['edges'].append({'from':dep,'to':node,'type':'review-selection' if dep.startswith('r27-') else 'proven-dependency',
                                    'label':'Reviewed selection' if dep.startswith('r27-') else 'Declared model input'})
        for i,equation in enumerate(row.get('equations',[])):
            eid=node+'-eq'+str(i+1)
            network['nodes'].append({'id':eid,'title':equation['label'],'kind':'equation','status':'proved-in-model',
                  'summary':equation['expression'],'equation':equation['expression'],
                  'detail':'Use the assumptions, model and limits in the two reports. Scientific priority unverified.',
                  'sources':row['sources'][:3],'route':'round27-'+loop})
            network['edges'].append({'from':node,'to':eid,'type':'proven-dependency','label':'Scoped derivation'})
    experts=[]
    names={'newton':'Newton','tesla':'Tesla','jung':'Jung / Pauli','penrose':'Penrose','feynman':'Feynman'}
    descriptions={
        'newton':'Inverse causes, explicit hypotheses, synthesis and retained exceptions.',
        'tesla':'Phase, source, load, receiver and physical scale.',
        'jung':'Interpretation, pattern selection and indistinguishable explanations.',
        'penrose':'Geometric and algebraic structure, model dimension and complete physical spaces.',
        'feynman':'Computable observables, discriminating countermodels and simulator limits.'}
    for lens in ['newton','tesla','jung','penrose','feynman']:
        require((R/f'experts/{lens}/final-review.md').is_file(),'missing final expert review '+lens)
        original=load(R/f'experts/{lens}/sources.json')['sources']
        rows=[]
        for s in original:
            rows.append({'title':s['title'],'url':s['url'],
                'depth':s.get('reading_depth',s.get('read_depth',s.get('inspected',s.get('reading','Reading limits in source report.')))),
                'status':s.get('status',s.get('admission',s.get('claim_scope',s.get('supports',s.get('scope','Source lead; consult report.')))))})
        experts.append({'id':lens,'name':names[lens],'summary':descriptions[lens], 'sources':rows,
                        'report':f'research/round27/experts/{lens}/report.md',
                        'final_review':f'research/round27/experts/{lens}/final-review.md'})
    progress=load(R/'advisor/progress.json')
    require(progress['completed']==3 and progress['requested']==3,'execution count')
    roadmap=load(R/'advisor/roadmap.json')
    for inherited in network['nodes']:
        if inherited['id'] in ['next-ai','next-ag']:
            inherited['status']='limited'
            inherited['detail']+=' Round27 addresses a scoped part of this goal; consult its current gates and roadmap for the remaining obligations.'
            inherited['sources'].append('research/round27/advisor/roadmap.json')
    for goal in roadmap['next_goals']:
        node='r27-next-'+goal['id'].lower()
        network['nodes'].append({'id':node,'title':goal['id']+' · '+goal['title'],
            'kind':'open','status':'planned','summary':goal['target'],
            'detail':'Planned after the three-loop review; no contract is frozen and no additional loop was executed.',
            'sources':['research/round27/advisor/roadmap.json'],'route':'round27-roadmap'})
        for dep in goal.get('dependencies',[]):
            network['edges'].append({'from':dep,'to':node,'type':'proposed-transfer','label':'Unproved next step'})
    data={'title':'What the readout tells us. What the proof still needs.',
          'summary':'Three adaptive investigations, five historical research lenses, separately authored derivations and skeptical checks. The four-dimensional Yang–Mills construction remains open.',
          'loops':loops,'experts':experts,'roadmap':roadmap,'progress':progress,
          'addendum':{'url':'ym-round27-addendum.pdf','title':'Round27 research addendum'},
          'network':network}
    ids=[n['id'] for n in network['nodes']]
    require(len(ids)==len(set(ids)),'duplicate network nodes')
    require(all(e['from'] in ids and e['to'] in ids for e in network['edges']),'dangling network edge')
    for n in network['nodes']:
        for s in n.get('sources',[]):
            if isinstance(s,str) and not s.startswith('https:'): require((ROOT/s).is_file(),'missing network source '+s)
    (R/'network.json').write_text(json.dumps(network,indent=2,ensure_ascii=False)+'\n')
    encoded=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/')
    (ROOT/'dist/research-round27-data.js').write_text('window.ROUND27_DATA = '+encoded+';\nif(window.ROUND26_DATA) window.ROUND26_DATA.network = window.ROUND27_DATA.network;\n')
    print(json.dumps({'loops':len(loops),'expert_source_records':sum(len(x['sources']) for x in experts),'network_nodes':len(ids),'network_edges':len(network['edges'])}))

if __name__=='__main__': build()
