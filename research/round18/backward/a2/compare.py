"""Complete independent producer-collection replay; never imports producer code."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,csv,hashlib,json
from geometry import build,partition,certify,weight,strict,advance,arithmetic_witness

ACCEPTED_CLUSTER_SHA='e511485e4dfbc0f54aa08fc4d0ba7c255485e7a98eedf46f35199bfaad94a6e0'
ACCEPTED_TEMPLATE_SHA='b81d917ac81541b132a1d808b181e654a692a06300a94858da1b9591dea8dded'


def vertex(v):return ','.join(map(str,v))
def edge(e):return 'e'+str(e[0])+':'+vertex(e[1:])
def face(f):return 'f'+str(3-f[0]-f[1])+':'+vertex(f[2:])
def digest(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def named_graph(n):
    g=build(n);edges=[];faces=[]
    for e in g['edges']:
        edges.append({'id':edge(e),'axis':e[0],'tail':vertex(e[1:]),'head':vertex(advance(e[1:],e[0]))})
    for row in sorted(g['faces'],key=lambda r:(3-r['face'][0]-r['face'][1],*r['face'][2:])):
        f=row['face'];a,b=f[:2];v=tuple(f[2:]);va=advance(v,a);vab=advance(va,b);vb=advance(v,b)
        faces.append({'id':face(f),'normal':3-a-b,'anchor':list(v),'vertices':[vertex(w) for w in (v,va,vab,vb)],
                      'word':[{'edge':edge(e),'sign':s} for e,s in row['word']]})
    return {'schema':'ym18-open-cubic-link-graph-v1','n':n,'vertices':[vertex(v) for v in g['vertices']],'edges':edges,'faces':faces,
            'group':'SU(2)','Gauss':'all vertices, no external charges','electric_terms':'alpha times every link Casimir; no links removed'}


def expected_certificate(n,parameters,source_sha):
    keys={'alpha','alpha_min','left_ratio','right_ratio','bridge_ratio','tau'}
    if type(parameters) is not dict or set(parameters)!=keys or any(type(v) is not str or str(F(v))!=v for v in parameters.values()):raise ValueError('complete canonical coefficient ratios and energy scale required')
    a,amin,l,r,m,t=(F(parameters[k]) for k in ('alpha','alpha_min','left_ratio','right_ratio','bridge_ratio','tau'))
    c=certify(n,a,amin,a*l,a*r,a*m,t);p=partition(n);g=named_graph(n);blocks=[]
    for b in p['clusters']:blocks.append({'anchor':b['anchor'],'edges':sorted(edge(e) for e in b['edges']),'faces':[face(f) for f in b['faces']]})
    ledger=[];role={'left':l,'right':r,'middle':m}
    for row in g['faces']:
        tangents=tuple(i for i in range(3) if i!=row['normal']);f=(*tangents,*row['anchor']);chosen=f in p['selected']
        value=a*role[p['selected'][f]['role']] if chosen else a*t*weight(f)
        ledger.append({'face':row['id'],'normal':row['normal'],'anchor':row['anchor'],'kind':'cluster' if chosen else 'remaining',
          'weight':str(weight(f)),'physical_coefficient':str(value),'untouched_link':None if chosen else edge(arithmetic_witness(n,f))})
    finite=F(c['finite_one_norm_lower']);uniform=F(c['uniform_one_norm_over_alpha'])
    return {'schema':'ym18-summable-cluster-bound-v1','source_sha256':source_sha,'cluster_source_sha256':ACCEPTED_CLUSTER_SHA,
      'graph_n':n,'graph_sha256':digest(g),'parameters':{k:parameters[k] for k in sorted(parameters)},'cluster_count':len(blocks),'clusters':blocks,
      'reference_free_links':sorted(edge(e) for e in p['free']),'reference_is_pure_free':not blocks,
      'local_cluster_gap_lower':str(a*(F(3,4)-max(abs(l),abs(r))-abs(m))),'local_cluster_template_graph_sha256':ACCEPTED_TEMPLATE_SHA,
      'reference_gap_lower_used':c['reference_conservative_lower'],'pure_free_gap_if_no_clusters':c['reference_actual_free_gap_if_no_clusters'],
      'face_ledger':ledger,'face_count':c['counts']['faces'],'remaining_face_count':c['counts']['remaining_faces'],
      'total_face_weight':c['weights']['total'],'selected_face_weight':c['weights']['selected'],'remaining_face_weight':c['weights']['remaining'],
      'orthant_weight_upper':'1','remainder_norm_upper':c['remainder_norm_bound'],'reference_remainder_expectation':'0','finite_gap_lower':str(finite),
      'finite_bound_status':'positive' if finite>0 else 'zero-insufficient' if finite==0 else 'negative-insufficient',
      'uniform_bound_at_alpha':c['uniform_lower_at_alpha'],'common_gap_lower':c['common_physical_lower'],'uniform_bound_status':c['uniform_status'],
      'generic_uniform_bound_at_alpha':str(a*F(c['uniform_two_norm_over_alpha'])),'finite_ground_Gauss_inclusion_certified':finite>0,
      'uniform_ground_Gauss_inclusion_certified':uniform>0,'actual_full_face_support':c['full_actual_face_support'],
      'schedule':{'status':'summable','dimensionless_norm_upper':str(abs(t)),
                  'reason':'three orientations times the positive orthant sum divided by twenty-four equals one'},
      'scope':'All-volume inhomogeneous summable-remainder exception in a common energy convention; internally overlapping strips have disjoint link supports; homogeneous dense Yang-Mills remains open'}


def expected_collection(source_sha):
    base={'alpha':'1','alpha_min':'1','left_ratio':'1/2','right_ratio':'1/2','bridge_ratio':'1/8','tau':'1/64'}
    inventory=[('volume_'+str(n),n,{}) for n in range(2,10)]+[
      ('negative_tau',5,{'tau':'-1/64'}),('signed_cluster',5,{'left_ratio':'-1/2','right_ratio':'1/4','bridge_ratio':'-1/8'}),
      ('tau_zero',5,{'tau':'0'}),('tau_boundary',5,{'tau':'1/8'}),('zero_cluster_coefficient',5,{'left_ratio':'0'}),
      ('scaled_double',4,{'alpha':'2'}),('scaled_half',4,{'alpha':'1/2','alpha_min':'1/4'})]
    fixtures=[{'id':name,'certificate':expected_certificate(n,{**base,**changes},source_sha)} for name,n,changes in inventory]
    boundary=[]
    for n in (6,8):
        f=(0,1,4,0,0);p=partition(n);chosen=f in p['selected'];coeff=F(1,2) if chosen else F(1,64)*weight(f)
        boundary.append({'n':n,'face':face(f),'kind':'cluster' if chosen else 'remaining','physical_coefficient':str(coeff)})
    return {'schema':'ym18-a2-collection-v1','source_sha256':source_sha,'graphs':{str(n):named_graph(n) for n in range(2,10)},'fixtures':fixtures,
      'all_volume_cluster_count':'n floor(n/4) floor(n/2)','orthant_weight_sum':'1','primary_common_gap_over_alpha_min':'7/64','primary_generic_gap_over_alpha':'3/32',
      'nonzero_homogeneous_remainder_gate':{'status':'blocked-volume-uniform-summability','dimensionless_norm_upper':None,
        'reason':'at least two n(n-1)^2 remaining faces have the same nonzero absolute coefficient'},
      'boundary_reclassification':boundary,'finite_volume_family_is_nested_restriction':False,
      'scope':'All-volume theorem is proved analytically; n2 through n9 are implementation checks; post-A B/C goals unexecuted'}


def verify_collection(value,source_sha):
    if not strict(value,expected_collection(source_sha)):raise ValueError('complete independent A2 replay mismatch')
    return True


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--producer',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ns=ap.parse_args()
    source=ns.producer.resolve();evidence=ns.evidence.resolve();out=ns.output.resolve();own=Path(__file__).resolve().parent
    if out.is_relative_to(own):raise ValueError('output outside source required')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();source_sha=sha(source/'summable.py')
    value=json.loads((evidence/'collection.json').read_text());expected=expected_collection(source_sha);checks=[]
    def gate(name,condition):
        if type(condition) is not bool or not condition:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    m=json.loads((source/'source-manifest.json').read_text())
    gate('producer complete source manifest and accepted A1 source agree',strict(m['files'],{n:sha(source/n) for n in ('summable.py','cluster.py','check.py','report.md')}) and sha(source/'cluster.py')==ACCEPTED_CLUSTER_SHA)
    gate('all eight actual signed open-box graphs independently reconstructed',strict(value['graphs'],expected['graphs']))
    gate('entire required fifteen-fixture inventory is bound',strict([f['id'] for f in value['fixtures']],[f['id'] for f in expected['fixtures']]))
    for a,b in zip(value['fixtures'],expected['fixtures']):gate('complete independent geometry coefficients and bound: '+b['id'],strict(a,b))
    gate('incomplete boundary coefficient reclassification preserved',strict(value['boundary_reclassification'],expected['boundary_reclassification']))
    gate('nonzero homogeneous tail explicitly fails uniform summability',strict(value['nonzero_homogeneous_remainder_gate'],expected['nonzero_homogeneous_remainder_gate']))
    gate('entire collection matches fresh independent arithmetic and schema',strict(value,expected))
    beyond=json.loads((evidence/'beyond-uniform-control.json').read_text())
    beyond_p={'alpha':'1','alpha_min':'1','left_ratio':'1/2','right_ratio':'1/2','bridge_ratio':'1/8','tau':'1/4'}
    gate('separate negative-uniform control retains a missing common bound',strict(beyond,expected_certificate(4,beyond_p,source_sha)))
    rows=[]
    for n,row in zip(range(2,10),expected['fixtures']):
        c=row['certificate'];count=c['remaining_face_count']
        rows.append({k:str(v) for k,v in {'n':n,'vertices':n**3,'links':3*n*n*(n-1),'faces':3*n*(n-1)**2,
          'clusters':c['cluster_count'],'remaining_faces':count,'remaining_weight':c['remaining_face_weight'],'finite_gap_lower':c['finite_gap_lower'],
          'uniform_common_gap_lower':c['common_gap_lower'],'generic_uniform_lower':c['generic_uniform_bound_at_alpha'],'full_support':c['actual_full_face_support'],
          'homogeneous_remainder_norm_budget':F(count,64),'homogeneous_finite_comparison':F(1,8)-F(count,64)}.items()})
    with (evidence/'volume.csv').open(newline='') as f:actual_rows=list(csv.DictReader(f))
    gate('plotted volume CSV agrees with independent exact coefficient ledger',strict(actual_rows,rows))
    mutations=[]
    def mutate(name,fn):
        v=copy.deepcopy(value);fn(v);mutations.append((name,v))
    mutate('omitted boundary-size fixture rejected',lambda v:v['fixtures'].pop(1))
    mutate('changed common scale rejected',lambda v:v['fixtures'][-1]['certificate'].update(common_gap_lower='7/128'))
    mutate('orthant bound replaced by unproved limit rejected',lambda v:v['fixtures'][0]['certificate'].update(orthant_weight_upper='107/135'))
    mutate('uniform endpoint promoted by finite positivity rejected',lambda v:v['fixtures'][11]['certificate'].update(uniform_ground_Gauss_inclusion_certified=True))
    mutate('zero selected interaction falsely labelled full support rejected',lambda v:v['fixtures'][12]['certificate'].update(actual_full_face_support=True))
    mutate('Boolean signed graph coordinate alias rejected',lambda v:v['graphs']['4']['faces'][0]['word'][0].update(sign=True))
    mutate('missing actual unused-link witness rejected',lambda v:v['fixtures'][0]['certificate']['face_ledger'][0].update(untouched_link=None))
    mutate('changed source binding rejected',lambda v:v.update(source_sha256='0'*64))
    mutate('forged external passed metadata rejected',lambda v:v.update(status='passed'))
    for name,v in mutations:gate(name,not strict(v,expected))
    hashes={**{'producer/'+n:sha(source/n) for n in ('summable.py','cluster.py','check.py','report.md','source-manifest.json')},
            **{'evidence/'+n:sha(evidence/n) for n in ('collection.json','beyond-uniform-control.json','volume.csv')},
            **{'independent/'+n:sha(own/n) for n in ('geometry.py','check.py','compare.py')}}
    result={'schema':'ym18-independent-a2-comparison-v1','status':'passed','checks_count':len(checks),'checks':checks,'input_sha256':hashes,
      'oracle':'Own integer graph and all-n arithmetic witness, direct positive weight enumeration, separate geometric sums and rational gap inequalities; no producer module imported.',
      'scope':'Complete all-volume inhomogeneous exception fixture inventory; homogeneous dense and thermodynamic spectral claims remain unproved.'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':main()
