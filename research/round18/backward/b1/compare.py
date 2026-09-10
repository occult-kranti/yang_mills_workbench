"""Complete independent replay of the B1 full-space finite-graph evidence."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from math import factorial
import argparse,copy,csv,hashlib,json
from operators import graph,supports,support_inventory,six_loop,fourth_inventory,matrices,cube_boundary_contraction,strict
from check import DEFINITIONS

HAAR_SHA='13a82e2b804f07d7dbe8951f600ded429d4924b042162ec79d60c2889b767a80'
GRAPH_SHA='9e630191189fb3f69145e5cdbc91eceac138f95d44d7bed825b87b572b322e62'
SOURCE_FILES=('haar.py','graph.json','cross.py','check.py','report.md','review-context/authorized-contract.md','review-context/accepted-control-amendment.md')
def vertex(v):return ','.join(map(str,v))
def edge(e):return 'e'+str(e['axis'])+':'+vertex(e['tail'])


def named_graph():
    g=graph();emap={e['id']:edge(e) for e in g['edges']};faces=[]
    for f in g['faces']:
        n=f['normal'];base=f['anchor'];loop=f['vertices'];word=f['word']
        if (-1)**n!=(-1 if base[n]==0 else 1):loop=[loop[0],*loop[:0:-1]];word=[(e,-s) for e,s in reversed(word)]
        region='shared' if n==0 and base[0]==1 else 'left' if base[0]==0 else 'right'
        faces.append({'id':'f'+str(n)+':'+vertex(base),'normal':n,'base':base,'vertices':[vertex(v) for v in loop],
                      'word':[{'edge':emap[e],'sign':s} for e,s in word],'region':region})
    left=[f['id'] for f in faces if f['region']=='left'];right=[f['id'] for f in faces if f['region']=='right'];shared=next(f['id'] for f in faces if f['region']=='shared')
    return {'schema':'ym16-adjacent-two-cubes-v1','vertices':[vertex(v) for v in g['vertices']],
      'edges':[{'id':edge(e),'tail':vertex(e['tail']),'head':vertex(e['head']),'axis':e['axis']} for e in g['edges']],'faces':faces,
      'left_disk':left,'right_disk':right,'shared_face':shared,'outer_faces':left+right,
      'cells':[{'id':'left','faces':left+[shared],'shared_orientation':1},{'id':'right','faces':right+[shared],'shared_orientation':-1}],
      'group':'SU(2)','measure':'independent normalized Haar on20 oriented links',
      'full_action':'sum over11 distinct face coefficients k_f*Tr(U_face_f)/2; internal face counted once',
      'outer_action':'sum over10 outer face coefficients only; shared coefficient0','time_generator':'none; finite Euclidean measure',
      'energy_scale':'no Hamiltonian energy scale is defined by these Euclidean couplings'}


def expected_supports():
    g=graph();ng=named_graph();raw,retained=support_inventory(g);rows=[]
    for r in raw:
        rows.append({'mask':int(r['mask'],16),'edge_count':r['size'],'minimum_active_degree':r['minimum_active_degree'] if r['size'] else None,
          'classification':'vacuum-support' if not r['size'] else 'fundamental-face-candidate' if r['passes_Gauss_necessary_degree'] else 'rejected-by-degree-one-Gauss-obstruction'})
    return {'edge_order':[e['id'] for e in ng['edges']],'rows':rows,
      'eligible_nonempty_masks':[sum(1<<i for i in r) for r in retained if r],
      'face_masks':{f['id']:sum(1<<i for i in s) for f,s in zip(ng['faces'],supports(g))},'total_supports':len(rows),'empty_supports':1,
      'interpretation':'necessary no-leaf supports; degree-two intertwiner proof fixes a common spin, and the energy cutoff leaves only spin one half'}


def expected_six():
    g=graph();ng=named_graph();w=six_loop(g);emap={e['id']:edge(e) for e in g['edges']};active=set(w['active_edges'])
    return {'vertices':[vertex(v) for v in w['vertices']],'word':[{'edge':emap[e],'sign':s} for e,s in w['word']],
      'norm_squared':'1','vacuum_inner_product':'0','face_inner_products':[{'face':f['id'],'odd_edges':sorted(emap[e] for e in active^sup),'inner_product':'0'} for f,sup in zip(ng['faces'],supports(g))],
      'energy_over_alpha':'9/2','spin_on_each_active_edge':'1/2','scope':'exact physical Wilson-loop state in Q, not a sampled tail eigenvector'}


def expected_fourth():
    g=graph();emap={e['id']:edge(e) for e in g['edges']};sup=supports(g);rows=[]
    for r in fourth_inventory(g):
        idx=r['faces'];odd=set()
        for i in idx:odd.symmetric_difference_update(sup[i])
        counts=Counter(idx);mult=factorial(4)
        for k in counts.values():mult//=factorial(k)
        rows.append({'indices':idx,'multiplicity':mult,'pattern':sorted(counts.values(),reverse=True),'odd_boundary_edges':[emap[e] for e in sorted(odd)],'moment':r['value']})
    return {'rows':rows,'multisets':1001,'ordered_products_covered':sum(r['multiplicity'] for r in rows),'all_four_distinct_cases':sum(r['pattern']==[1,1,1,1] for r in rows),
      'degree_four_independent_Haar_agreement':True,'reason':'this low-order agreement follows from actual graph integration; it is not a full distribution factorization'}


def expected_certificate(alpha,couplings,source_sha):
    c=matrices(graph(),alpha,couplings)
    return {'schema':'ym18-physical-complement-cross-v1','source_sha256':source_sha,'haar_source_sha256':HAAR_SHA,'graph_file_sha256':GRAPH_SHA,
      'physical_contract':{'Hamiltonian':'alpha sum_e C_e minus sum_p lambda_p x_p','Hilbert':'untruncated L2 of SU(2)^20 restricted to all-vertex Gauss invariants',
         'external_charges':False,'Casimir':'j(j+1)','normalization':'x_p=Tr(U_p)/2; ordinary fundamental chi_p=2x_p',
         'projection':'vacuum and all eleven fundamental face characters','operator_domain':'elliptic electric domain; bounded Wilson perturbation'},
      'alpha':c['alpha'],'couplings':c['couplings'],'face_order':[f['id'] for f in named_graph()['faces']],
      'Gram':c['Gram'],'PVP':c['PVP'],'PV2P':c['PV2P'],'P_subtraction':c['PVP_squared'],'cross_Gram':c['cross_Gram'],
      'Q_electric_lower':c['full_electric_complement_lower'],'Q_full_lower_from_norm':c['QHQ_lower'],'sum_coupling_squares':c['sum_squared_couplings'],
      'maximum_absolute_ratio':c['rho_max'],'cross_norm_squared_row_upper':c['cross_row_sum_bound'],'coefficient_box_norm_squared_upper':c['box_cross_norm_squared_upper'],
      'equal_magnitudes':c['homogeneous_magnitude_cross_norm_squared'] is not None,'exact_cross_norm_squared_if_equal':c['homogeneous_magnitude_cross_norm_squared'],
      'scope':'Complete finite-graph physical complement and QVP Gram; scalar E1 optimization and B2 parameter-box gap not executed'}


def expected_collection(source_sha):
    ng=named_graph();fixtures=[{'id':name,'certificate':expected_certificate(a,ls,source_sha)} for name,a,ls in DEFINITIONS]
    sixth=cube_boundary_contraction(graph())['ordinary_character_moment'];byname={f['id']:i for i,f in enumerate(ng['faces'])}
    return {'schema':'ym18-b1-collection-v1','source_sha256':source_sha,'graph':ng,'low_support_inventory':expected_supports(),
      'six_edge_witness':expected_six(),'fourth_moment_inventory':expected_fourth(),'fixtures':fixtures,
      'controls':{'Gaussian_same_face_fourth':{'actual':'2','Gaussian':'3','actual_single_cross_diagonal':'1/256','Gaussian_single_cross_diagonal':'1/128'},
        'deleted_P_subtraction':{'actual_vacuum_cross_diagonal':'0','without_subtraction':'11/256'},
        'six_face_distribution_independence':{'face_indices':[byname[n] for n in ng['cells'][0]['faces']],'actual_moment':sixth,'independent_Haar_prediction':'0'},
        'omitted_projection_face':{'face':ng['faces'][0]['id'],'omitted_state_energy_over_alpha':'3','invalid_complement_threshold_over_alpha':'9/2'},
        'falsely_raised_tail':{'proposed_over_alpha':'6','witness_over_alpha':'9/2'}},
      'status':'computed-for-independent-review','B2':'not executed'}


def verify_collection(value,source_sha):
    if not strict(value,expected_collection(source_sha)):raise ValueError('complete independent B1 replay mismatch')
    return True


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--producer',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ns=ap.parse_args()
    source=ns.producer.resolve();evidence=ns.evidence.resolve();out=ns.output.resolve();own=Path(__file__).resolve().parent
    if out.is_relative_to(own):raise ValueError('output outside source required')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();source_sha=sha(source/'cross.py')
    value=json.loads((evidence/'collection.json').read_text());expected=expected_collection(source_sha);checks=[]
    def gate(name,ok):
        if type(ok) is not bool or not ok:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    m=json.loads((source/'source-manifest.json').read_text())
    gate('complete frozen source and amended contract inventory agrees',strict(m['files'],{n:sha(source/n) for n in SOURCE_FILES}) and sha(source/'haar.py')==HAAR_SHA and sha(source/'graph.json')==GRAPH_SHA)
    for key,name in [('graph','entire signed graph and its original geometric metadata'),('low_support_inventory','all 21700 low-support records'),('six_edge_witness','actual six-edge saturation and every face orthogonality witness'),('fourth_moment_inventory','all 1001 fourth multisets and complete odd boundaries')]:
        gate('independently reconstructed '+name,strict(value[key],expected[key]))
    gate('complete fixed nine-fixture inventory bound',strict([f['id'] for f in value['fixtures']],[f['id'] for f in expected['fixtures']]))
    for a,b in zip(value['fixtures'],expected['fixtures']):gate('exact full matrices and physical coefficients: '+b['id'],strict(a,b))
    gate('corrected fourth and sixth order controls agree',strict(value['controls'],expected['controls']))
    gate('complete source premises support data and matrix collection replay',strict(value,expected))
    csv_rows=[]
    for f in expected['fixtures']:
        c=f['certificate'];csv_rows.append({'fixture':f['id'],'alpha':c['alpha'],'maximum_ratio':c['maximum_absolute_ratio'],'Q_electric_lower':c['Q_electric_lower'],
          'cross_norm_squared_row_upper':c['cross_norm_squared_row_upper'],'coefficient_box_norm_squared_upper':c['coefficient_box_norm_squared_upper']})
    with (evidence/'cross-norms.csv').open(newline='') as f:actual_csv=list(csv.DictReader(f))
    gate('exact plotted norm CSV independently agrees',strict(actual_csv,csv_rows))
    changes=[]
    def mutate(name,fn):
        v=copy.deepcopy(value);fn(v);changes.append((name,v))
    mutate('missing support row rejected',lambda v:v['low_support_inventory']['rows'].pop())
    mutate('Gaussian fourth passed as exact Haar rejected',lambda v:v['fourth_moment_inventory']['rows'][0].update(moment='3'))
    mutate('deleted P subtraction passed as exact cross rejected',lambda v:v['fixtures'][1]['certificate'].update(cross_Gram=v['fixtures'][1]['certificate']['PV2P']))
    mutate('falsely raised omitted threshold rejected',lambda v:v['fixtures'][1]['certificate'].update(Q_electric_lower='6'))
    mutate('omitted projection face channel rejected',lambda v:v['fixtures'][1]['certificate']['face_order'].pop())
    mutate('missing physical scale fixture rejected',lambda v:v['fixtures'].pop())
    mutate('Boolean signed graph alias rejected',lambda v:v['graph']['faces'][1]['word'][0].update(sign=True))
    mutate('changed source binding rejected',lambda v:v.update(source_sha256='0'*64))
    mutate('forged caller pass object rejected',lambda v:v.update(status='passed'))
    for name,v in changes:gate(name,not strict(v,expected))
    hashes={**{'producer/'+n:sha(source/n) for n in (*SOURCE_FILES,'source-manifest.json')},
      **{'evidence/'+n:sha(evidence/n) for n in ('collection.json','cross-norms.csv')},**{'independent/'+n:sha(own/n) for n in ('operators.py','check.py','compare.py')}}
    result={'schema':'ym18-independent-b1-comparison-v1','status':'passed','checks_count':len(checks),'checks':checks,'input_sha256':hashes,
      'oracle':'Own complete graph support enumeration, S3 repeated Haar moments and actual six-face matrix-index contraction, followed by full matrix subtraction; no producer module imported.',
      'scope':'Complete finite physical complement and exact cross Gram; B2 not executed.'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':main()
