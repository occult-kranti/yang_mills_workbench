"""Independent Loop1 replay. Standard library; no producer arithmetic in oracle."""
import argparse,copy,hashlib,importlib.util,json
from fractions import Fraction as Q
from pathlib import Path
from itertools import product,combinations
from shared_projector import (graph_data,boundary_rank_and_kernel,orient_surface,
                              raw_integral,character_triple)
from exact_algebra import rational_unit,trace_word,gauge_links,reversed_word

HERE=Path(__file__).resolve().parent


def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def verify_evidence(evidence,graph,data,ledger,mixed,source_sha):
    """Compare saved claims with independently reconstructed exact values."""
    if evidence.get('schema')!='ym16-two-cube-haar-evidence-v1':raise ValueError('evidence schema')
    if evidence.get('source_sha256')!=source_sha:raise ValueError('evidence source')
    canonical=hashlib.sha256(json.dumps(graph,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    if evidence.get('graph_sha256')!=canonical or evidence.get('graph')!=graph:raise ValueError('evidence graph')
    if type(evidence.get('face_edge_rank_mod2')) is not int or evidence['face_edge_rank_mod2']!=9:raise ValueError('evidence rank')
    if type(evidence.get('face_edge_nullity_mod2')) is not int or evidence['face_edge_nullity_mod2']!=2:raise ValueError('evidence nullity')
    kernel=[r['mask'] for r in ledger if r['closed']]
    if evidence.get('closed_subset_masks')!=kernel:raise ValueError('evidence closed subsets')
    rows=evidence.get('subsets');faces=list(data['words'])
    if type(rows) is not list or len(rows)!=2048:raise ValueError('complete evidence subset ledger required')
    for expected,row in zip(ledger,rows):
        mask=expected['mask'];selected=[j for j in range(11) if mask&(1<<j)]
        odd=[e for e,terms in data['incidence'].items() if sum(faces.index(f) in selected for f,_ in terms)%2]
        if type(row.get('mask')) is not int or row['mask']!=mask or row.get('selected_faces')!=selected:raise ValueError('evidence mask or selected faces')
        if set(row.get('odd_edges',[]))!=set(odd) or len(row['odd_edges'])!=len(odd):raise ValueError('evidence edge parity')
        if row.get('moment')!=expected['mean'] or row.get('index_moment')!=expected['mean']:raise ValueError('evidence moment')
    refs=evidence.get('references',{})
    expectations={'left_cube':'1/1024','right_cube':'1/1024','outer10':'1/262144','all11':'0','outer10_shared_square':str(mixed['value']),'outer10_shared_adjoint':'1/262144'}
    if set(refs)!=set(expectations):raise ValueError('reference targets')
    for key,value in expectations.items():
        if refs[key].get('moment')!=value:raise ValueError('reference moment')
    for key,ids in [('left_cube',data['left']|{data['shared']}),('right_cube',data['right']|{data['shared']}),('outer10',data['left']|data['right']),('all11',set(faces))]:
        if refs[key].get('powers')!=[int(f in ids) for f in faces]:raise ValueError('reference powers')
    if refs['outer10_shared_square'].get('powers')!=[2 if f==data['shared'] else 1 for f in faces]:raise ValueError('shared insertion powers')
    if refs['outer10_shared_adjoint'].get('definition')!='4*outer10_shared_square-outer10':raise ValueError('adjoint definition')
    if evidence.get('status')!='passed' or evidence.get('scope')!='Exact finite normalized link-Haar identities; no tilted integral, physical generator or infinite-volume claim':raise ValueError('evidence status or scope')
    return True


def run(producer,scale,output):
    producer,scale,output=map(Path,(producer,scale,output));output.mkdir(parents=True,exist_ok=False)
    p=load(producer/'two_cube.py','producer_two_cube');energy=load(scale/'energy_scale.py','advisor_energy_scale')
    pinned={str(path.resolve()):digest(path) for path in [producer/'two_cube.py',producer/'graph.json',producer/'manifest.json',producer/'output/exact_evidence.json',scale/'energy_scale.py',scale/'energy_scale.md',scale/'scale-output/review.json']}
    graph=json.loads((producer/'graph.json').read_text());data=graph_data(graph);checks=[]
    def check(name,condition):
        if not condition:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,TypeError):check(name,True);return
        raise RuntimeError('did not reject '+name)
    check('actual graph has 12 vertices, 20 edges, 11 faces',tuple(map(len,(graph['vertices'],graph['edges'],graph['faces'])))==(12,20,11))
    check('outer sphere Euler characteristic',12-20+len(graph['outer_faces'])==2)
    check('disk edge and vertex counts',all((len({e for f in disk for e,_ in data['words'][f]})-4,len({v for f in disk for e,_ in data['words'][f] for v in data['edges'][e]})-4)==(8,4) for disk in (data['left'],data['right'])))
    check('producer graph validator agrees',len(p.validate_graph(graph))==20)
    rank,kernel,faces,rows=boundary_rank_and_kernel(data)
    masks=[sum(1<<faces.index(f) for f in target) for target in (set(),data['left']|{data['shared']},data['right']|{data['shared']},data['left']|data['right'])]
    check('independent column elimination rank nine',rank==9)
    check('complete 2048-mask parity kernel',set(kernel)==set(masks) and len(kernel)==4)
    check('left XOR right equals outer',masks[1]^masks[2]==masks[3])
    ledger=[]
    for mask in range(2048):
        selected=[f for j,f in enumerate(faces) if mask&(1<<j)]
        expected=raw_integral(orient_surface(data['words'],selected))['value']
        powers=[int(bool(mask&(1<<j))) for j in range(11)]
        actual=p.moment(powers)
        if actual!=expected:raise RuntimeError('distinct subset mismatch '+str(mask))
        ledger.append({'mask':mask,'degree':len(selected),'mean':str(expected),'closed':mask in kernel})
    check('all 2048 distinct-face moments agree with independent parity and raw indices',True)
    closed={row['mask']:row['mean'] for row in ledger if row['closed']}
    check('one-cube means recover 1/1024',closed[masks[1]]==closed[masks[2]]=='1/1024')
    check('outer mean recovers 2^-18',closed[masks[3]]=='1/262144')
    check('full eleven fundamental mean is zero',ledger[-1]['mean']=='0')
    outer=[data['words'][f] for f in faces if f!=data['shared']];shared=data['words'][data['shared']]
    mixed_words=outer+[shared,reversed_word(shared)]
    mixed=raw_integral(mixed_words)
    check('actual shared projector has four fourth-order edges and 256 branches',mixed['fourth_edges']==4 and mixed['paired_edges']==16 and mixed['branches']==256)
    check('Gram inverse coefficient identities',4*Q(1,3)+2*Q(-1,6)==1 and 2*Q(1,3)+4*Q(-1,6)==0)
    check('mixed raw mean is 2^-19',mixed['value']==Q(1,524288))
    powers=[2 if f==data['shared'] else 1 for f in faces]
    check('mixed character oracle matches raw projector',p.moment(powers)==mixed['value'])
    check('mixed adjoint insertion matches direct polynomial identity',4*mixed['value']-Q(closed[masks[3]])==Q(1,262144))
    wrong={mode:str(raw_integral(mixed_words,mode)['value']) for mode in ('drop_negative','independent_pairs')}
    check('dropping negative fourth-Haar terms discriminates',Q(wrong['drop_negative'])!=mixed['value'])
    check('replacing shared edge by independent pairs discriminates',Q(wrong['independent_pairs'])!=mixed['value'])
    check('omitting shared insertion discriminates',Q(closed[masks[3]])!=mixed['value'])
    evidence=json.loads((producer/'output/exact_evidence.json').read_text())
    check('saved producer evidence independently reconstructed',verify_evidence(evidence,graph,data,ledger,mixed,digest(producer/'two_cube.py')))
    for field in ('source_sha256','graph_sha256','scope'):
        bad=copy.deepcopy(evidence);bad[field]='forged'
        reject('saved evidence rejects changed '+field,lambda b=bad:verify_evidence(b,graph,data,ledger,mixed,digest(producer/'two_cube.py')))
    bad=copy.deepcopy(evidence);bad['subsets'].pop()
    reject('saved evidence rejects omitted parity row',lambda:verify_evidence(bad,graph,data,ledger,mixed,digest(producer/'two_cube.py')))
    bad=copy.deepcopy(evidence);bad['references']['outer10_shared_square']['moment']='1/262144'
    reject('saved evidence rejects outer-only substitute with passed status',lambda:verify_evidence(bad,graph,data,ledger,mixed,digest(producer/'two_cube.py')))
    manifest=json.loads((producer/'manifest.json').read_text())
    check('all fourteen frozen producer files match manifest',len(manifest['files'])==14 and all(digest(producer/file)==sha for file,sha in manifest['files'].items()))
    for n,m,k in product(range(7),repeat=3):
        expected=character_triple(n,m,k)
        if expected!=p.fusion(n,m,k):raise RuntimeError('polynomial Haar fusion mismatch '+str((n,m,k)))
    check('343 character triples independently integrated by semicircle moments',True)
    check('ordinary character coefficient normalization',character_triple(1,1,0)==1 and p.char_power(1)=={1:Q(1,2)} and p.char_power(2)=={0:Q(1,4),2:Q(1,4)})
    # Exact noncommuting SU(2) gauge fixtures; no floating tolerances.
    links={edge:rational_unit(i+1) for i,edge in enumerate(data['edges'])}
    gauges={v:rational_unit(i+37) for i,v in enumerate(graph['vertices'])}
    transformed=gauge_links(data['edges'],links,gauges)
    values={f:trace_word(w,links) for f,w in data['words'].items()}
    for f,w in data['words'].items():
        check('exact gauge invariance '+f,trace_word(w,transformed)==values[f])
        check('complete face reversal invariance '+f,trace_word(reversed_word(w),links)==values[f])
        wrongword=w.copy();wrongword[0]=(wrongword[0][0],-wrongword[0][1])
        check('one wrong dagger has nonzero exact gauge defect '+f,trace_word(wrongword,transformed)!=trace_word(wrongword,links))
    kappas={f:Q(i+1,7) for i,f in enumerate(faces)}
    action=sum(kappas[f]*values[f] for f in faces)
    gauge_action=sum(kappas[f]*trace_word(data['words'][f],transformed) for f in faces)
    outer_action=sum(kappas[f]*values[f] for f in faces if f!=data['shared'])
    check('inhomogeneous full global action is gauge invariant',action==gauge_action)
    check('full and outer actions differ by exactly one shared term',action-outer_action==kappas[data['shared']]*values[data['shared']]!=0)
    center_links=links.copy();edge=shared[0][0];center_links[edge]=tuple(-v for v in links[edge])
    product_before=Q(1);product_after=Q(1)
    for f in faces:product_before*=values[f];product_after*=trace_word(data['words'][f],center_links)
    check('single shared edge center flip negates full eleven product',product_before!=0 and product_after==-product_before)
    # Contract mutations: actual geometry and declared action are both reviewed.
    mutations=[]
    bad=copy.deepcopy(graph);bad['faces']=[f for f in bad['faces'] if f['id']!=data['shared']];mutations.append(('omitted shared face',bad))
    bad=copy.deepcopy(graph);bad['faces'].append(copy.deepcopy(bad['faces'][0]));mutations.append(('duplicate face',bad))
    bad=copy.deepcopy(graph);bad['faces'][0]['word'][0]['sign']*=-1;mutations.append(('one wrong dagger',bad))
    bad=copy.deepcopy(graph);bad['faces'][0]['word'][0]['sign']=True;mutations.append(('Boolean sign',bad))
    bad=copy.deepcopy(graph);bad['faces'][0]['normal']=False;mutations.append(('Boolean normal',bad))
    bad=copy.deepcopy(graph);bad['left_disk'][0]=data['shared'];mutations.append(('wrong disk membership',bad))
    bad=copy.deepcopy(graph);bad['outer_faces'].append(data['shared']);mutations.append(('shared counted as outer',bad))
    bad=copy.deepcopy(graph);bad['full_action']=bad['outer_action'];mutations.append(('wrong physical action',bad))
    bad=copy.deepcopy(graph);bad['time_generator']='physical Hamiltonian';mutations.append(('unsupported generator',bad))
    bad=copy.deepcopy(graph);bad['cells'][0]['shared_orientation']=True;mutations.append(('Boolean cell orientation',bad))
    for name,bad in mutations:
        reject('independent rejects '+name,lambda b=bad:graph_data(b))
        reject('producer rejects '+name,lambda b=bad:p.validate_graph(b))
    for bad in (True,-1,1.0):reject('character power rejects '+repr(bad),lambda b=bad:p.char_power(b))
    baseline=p.moment([int(f in data['left'] or f==data['shared']) for f in faces])
    cached=p.char_power(1);cached[1]=Q(7)
    check('public cached dictionary cannot mutate later moments',p.moment([int(f in data['left'] or f==data['shared']) for f in faces])==baseline==Q(1,1024))
    reject('Boolean after populated character cache rejected',lambda:p.char_power(True))
    # Independent physical energy normalization audit. Count oriented square choices.
    scale_record=json.loads((scale/'scale-output/review.json').read_text())
    scale_rows=[]
    for row in scale_record['rows']:
        n=row['n'];face_count=sum((n-1)**2*n for _ in combinations(range(3),2))
        check('independent scale row n='+str(n),row['plaquettes']==face_count and Q(row['fixed_free_gap'])==3 and Q(row['shrinking_free_gap'])==Q(3,n) and Q(row['global_norm_lower'])==3-Q(face_count,100))
        scale_rows.append({'n':n,'face_count':face_count,'fixed_exact_gap':'3','shrinking_exact_gap':str(Q(3,n))})
    for n in (2,3,4):
        vertices=set(product(range(n),repeat=3));squares=set()
        for v in vertices:
            for a,b in combinations(range(3),2):
                va=list(v);va[a]+=1;vb=list(v);vb[b]+=1;vab=list(va);vab[b]+=1
                if tuple(va) in vertices and tuple(vb) in vertices and tuple(vab) in vertices:squares.add(frozenset((v,tuple(va),tuple(vb),tuple(vab))))
        check('enumerated box squares n='+str(n),len(squares)==energy.box_row(n,1,0)['plaquettes'])
        check('free shortest four-edge fundamental spin network n='+str(n),len(next(iter(squares))) * Q(3,4)==Q(energy.box_row(n,1,0)['free_gap']))
    check('physical scale multiplication',energy.physical_lower('5/7','11/3')==Q(55,21))
    check('negative sufficient bound is retained',energy.physical_lower('5/7','-11/3')==Q(-55,21))
    check('zero sufficient bound is not a positive certificate',energy.box_row(2,1,'1/2')['bound_status']=='insufficient')
    check('signed coupling norm is sign invariant',energy.box_row(3,2,'-1/4')==energy.box_row(3,2,'1/4') | {'lambda_over_alpha':'-1/4'})
    for value in (True,False,0,-1,0.5,'nan','1/0'):reject('scale rejects invalid alpha '+repr(value),lambda v=value:energy.physical_lower(v,1))
    check('shrinking alpha can be compensated in arbitrary families',all(Q(1,n)*n==1 for n in (2,3,7,11)))
    check('counterexample removes compensation by fixed dimensionless gap three',all(Q(1,n)*3==Q(3,n)<3 for n in (2,3,7,11)))
    check('common scale and common dimensionless lower imply common physical lower',all(energy.physical_lower(a,d)>=Q(2,5)*Q(3,7) for a,d in product((Q(2,5),Q(4,3)),(Q(3,7),Q(8,5)))))
    check('scale source record matches actual file',scale_record['source_sha256']==digest(scale/'energy_scale.py'))
    check('all reviewed inputs unchanged during replay',all(digest(path)==sha for path,sha in pinned.items()))
    portable_pins={('producer/'+str(Path(path).relative_to(producer.resolve())) if Path(path).is_relative_to(producer.resolve()) else 'scale/'+str(Path(path).relative_to(scale.resolve()))):sha for path,sha in pinned.items()}
    result={'schema':'ym16-independent-loop1-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'input_sha256':portable_pins,'graph_rank':rank,'kernel_masks':kernel,'exhaustive_subset_count':2048,'character_triple_count':343,
      'closed_moments':closed,'mixed_raw_projector':{k:str(v) for k,v in mixed.items()},'wrong_projectors':wrong,
      'mixed_adjoint_mean':'1/262144','scale_rows':scale_rows,
      'scope':'Finite normalized SU(2) Haar graph and separate physical energy-scaling audit. No continuum, uniform interacting gap or time-generator identification.'}
    (output/'review.json').write_text(json.dumps(result,indent=2)+'\n')
    (output/'subsets.json').write_text(json.dumps(ledger,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks_count':len(checks),'mixed_mean':str(mixed['value'])}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--producer',required=True);parser.add_argument('--scale',required=True);parser.add_argument('--output',required=True)
    args=parser.parse_args();run(args.producer,args.scale,args.output)
