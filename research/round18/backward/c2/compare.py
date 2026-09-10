"""Full independent angular replay of the producer's two-link certificate set."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,csv,hashlib,json,subprocess,sys
import angular as a
import geometry as g

PRODUCER_SHA='7db0ba09dc0d2ef0f03a11ab2c467eafe22b51c71a7f7ffac24588abab86ea81'


def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)


def expected_graph():
    independent=g.graph()
    edges=[{'id':e['id'],'axis':e['axis'],'tail':g.name(e['tail']),'head':g.name(e['head'])} for e in sorted(independent['edges'],key=lambda e:(e['axis'],e['tail']))]
    faces=[{'id':f['id'],'axes':[j for j in range(3) if j!=f['normal']],'base':f['base'],'word':f['word']} for f in sorted(independent['faces'],key=lambda f:(-f['normal'],f['base']))]
    return {'schema':'ym18-c2-four-cube-graph-v1','vertices':list(map(g.name,independent['vertices'])),'edges':edges,'faces':faces,
      'variable_links':{'U':'e2:1,1,0','V':'e2:1,0,0'},'other_links':'identity','measure':'independent normalized Haar on U and V only'}


def realization(u,v):
    source=g.graph();geometry=g.reduce(source);rows={r['face']:r for r in geometry['reduced_faces']};values={r['face']:r['trace'] for r in g.traces(source,u,v)}
    result=[]
    for face in expected_graph()['faces']:
        r=rows[face['id']];classification='constant' if r['trace']=='1' else r['trace']
        result.append({'face':face['id'],'active_word':r['variable_word'],'classification':classification,'actual_trace':values[face['id']],'reduced_trace':values[face['id']]})
    uq,vq=g.quaternion(u),g.quaternion(v)
    return {'U':u,'V':v,'faces':result,'noncommuting':g.multiply(uq,vq)!=g.multiply(vq,uq)}


def geometry():
    graph=expected_graph();r=realization(['3/5','4/5','0','0'],['5/13','0','12/13','0'])
    categories={key:[row['face'] for row in r['faces'] if row['classification']==key] for key in ('constant','x','y','w')}
    return {'graph_sha256':hashlib.sha256(canonical(graph).encode()).hexdigest(),'counts':[len(graph['vertices']),len(graph['edges']),len(graph['faces'])],
      'categories':categories,'affected_faces':[f['id'] for f in graph['faces'] if f['id'] not in categories['constant']],
      'pointwise_noncommuting_fixture':r,'pointwise_dagger_fixture':realization(['3/5','4/5','0','0'],['3/5','4/5','0','0']),
      'constant_face_terms':14,'removed_constant_action':'14*kappa; cancels only in this conditional quotient'}


def certificate(d,k,n):
    v=a.certify(d,k,n);coeff=a.coefficients(d)
    return {'schema':'ym18-c2-certificate-v1','source_sha256':PRODUCER_SHA,'kappa':k,'V_only_coefficient':d,'degree':n,
      'target_width':v['precision'],'action':'kappa*(3*x+d*y+w)','full_six_face_action':d==2,'observable':'(4*x^2-1)^3*(4*w^2-1)/81',
      'trace_definitions':{'x':'Tr(U)/2','y':'Tr(V)/2','w':'Tr(U Vdagger)/2'},
      'numerator_coefficients':coeff['numerator_coefficients'],'partition_coefficients':coeff['partition_coefficients'],
      'coefficient_convention':'[kappa^n] includes all factorials; coefficient arrays through n8','maximum_absolute_action':v['M'],'tail':v['tail'],
      'numerator_partial':v['numerator_polynomial'],'partition_partial':v['partition_polynomial'],
      'numerator_interval':v['numerator_interval'],'partition_interval':v['partition_interval'],'expectation_interval':v['expectation_interval'],
      'width_target_met':v['width_status']=='target-met','sign_status':v['sign_status'],'status':v['width_status'],
      'scope':'normalized two-Haar-link conditional integral with all other31links fixed; no physical spectrum or full bulk claim'}


def gram(y):
    d=g.gram(y)
    return {'y':y,'kappa':d['kappa'],'gram':d['gram'],'rank':d['rank'],'direction_span_minor':str(1-F(y)**2),
      'measure':'(2/pi)*sqrt(1-y^2) dy','outer_weight':'exp(2*kappa*y)*Z_U(G(y)) for a normalized inner observable'}


def expected_collection():
    angular=a.collection();frozen=sum((c*a.semicircle(i+j) for (i,_,j),c in a.observable().items()),F(0))
    return {'schema':'ym18-c2-collection-v1','source_sha256':PRODUCER_SHA,'graph':expected_graph(),'geometry':geometry(),
      'joint_moments':[{'exponents':r['exponents'],'value':r['moment']} for r in angular['primitive_moments']],
      'coefficient_arrays':[{'V_only_coefficient':m['d'],'numerator':m['numerator_coefficients'],'partition':m['partition_coefficients']} for m in angular['models']],
      'refinements':[certificate(2,'1/64',n) for n in (0,2,4,6,8)],
      'fixtures':[{'id':f'd{d}_{s}','certificate':certificate(d,k,8)} for d in (2,1,0) for s,k in [('positive','1/64'),('zero','0'),('negative','-1/64')]],
      'central_Gram_family':[gram(y) for y in ('-1','0','3/5','1')],'frozen_V_zero_kappa_mean':str(frozen),
      'controls':{'three_independent_traces_xyw':{'actual':str(a.moment([1,1,1])),'wrong':'0'},
       'missing_dimension_divisor_xyw':{'actual':str(a.moment([1,1,1])),'wrong':'1/8'},
       'uniform_y_measure_second_moment':{'actual':str(a.moment([0,2,0])),'wrong':'1/3'},
       'pointwise_dagger':{'U_equals_V':['3/5','4/5','0','0'],'w':'1','wplus':'-7/25'},
       'consistent_dagger_substitution':'V->Vdagger preserves Haar,y and transforms wplus to w; integrated joint law is unchanged',
       'missing_inner_normalization_weight':'normalized inner averages require outer weight exp(2*kappa*y)*Z_U(G(y)), not bare surrounding Haar'},
      'scope':'conditional two-link integral; other31links fixed, all6affectedweights retained only for d2'}


def verify(v):
    if not a.strict(v,expected_collection()):raise ValueError('complete independent two-link replay differs')
    return True


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--producer',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ns=ap.parse_args()
    own=Path(__file__).resolve().parent;source=ns.producer.resolve();evidence=ns.evidence.resolve();out=ns.output.resolve()
    if out.is_relative_to(own):raise ValueError('output outside source required')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
    def gate(name,ok):
        if type(ok) is not bool or not ok:raise ValueError('failed comparison: '+name)
        checks.append({'name':name,'passed':True})
    ignored={'output','output-optimized','comparison','comparison-optimized'}
    actual_sources={str(p.relative_to(source)):sha(p) for p in source.rglob('*') if p.is_file() and p!=source/'source-manifest.json' and '__pycache__' not in p.relative_to(source).parts and p.relative_to(source).parts[0] not in ignored}
    manifest=json.loads((source/'source-manifest.json').read_text())
    gate('complete frozen source and history inventory agrees',a.strict(manifest['files'],actual_sources) and sha(source/'joint.py')==PRODUCER_SHA)
    value=json.loads((evidence/'completecollection.json').read_text());expected=expected_collection()
    gate('complete969 joint moments independently agree',a.strict(value['joint_moments'],expected['joint_moments']))
    gate('all three complete coefficient arrays independently agree',a.strict(value['coefficient_arrays'],expected['coefficient_arrays']))
    gate('actual signed graph, six-face union and pointwise fixtures independently agree',a.strict(value['graph'],expected['graph']) and a.strict(value['geometry'],expected['geometry']))
    gate('all four conditional Grams and their surrounding measure agree',a.strict(value['central_Gram_family'],expected['central_Gram_family']))
    gate('the five fixed refinements and nine ordered fixtures are complete',[x['degree'] for x in value['refinements']]==[0,2,4,6,8] and [x['id'] for x in value['fixtures']]==[x['id'] for x in expected['fixtures']])
    for x,y in zip(value['refinements'],expected['refinements']):gate('full signed tail division at degree'+str(y['degree']),a.strict(x,y))
    for x,y in zip(value['fixtures'],expected['fixtures']):gate('complete source-bound weighted fixture '+y['id'],a.strict(x,y))
    gate('full collection includes correct scope, zero branch and dagger exception',a.strict(value,expected))
    gate('separate graph JSON agrees with actual complex',a.strict(json.loads((evidence/'actualgraph.json').read_text()),expected['graph']))
    # CSV schemas are checked explicitly after independent interval reconstruction.
    csv_checks={}
    for filename in ('refinement.csv','weights.csv'):
        with (evidence/filename).open(newline='') as stream:csv_checks[filename]=list(csv.DictReader(stream))
    # Filled with the author's documented column names only, never its numerical oracle.
    refine=[{'degree':str(v['degree']),'lower':v['expectation_interval']['lower'],'upper':v['expectation_interval']['upper'],'width':v['expectation_interval']['width'],'status':v['status'],'sign_status':v['sign_status']} for v in expected['refinements']]
    weights=[{'fixture':f['id'],'kappa':f['certificate']['kappa'],'V_only_coefficient':str(f['certificate']['V_only_coefficient']),
      'degree':str(f['certificate']['degree']),'lower':f['certificate']['expectation_interval']['lower'],'upper':f['certificate']['expectation_interval']['upper'],'width':f['certificate']['expectation_interval']['width'],'status':f['certificate']['status']} for f in expected['fixtures']]
    gate('refinement CSV reproduces exact retained failures and final interval',a.strict(csv_checks['refinement.csv'],refine))
    gate('weights CSV reproduces every signed and omission fixture',a.strict(csv_checks['weights.csv'],weights))
    mutations=[('missing fixture',lambda b:b['fixtures'].pop()),('omitted V weight relabelled full model',lambda b:b['fixtures'][3]['certificate'].update(full_six_face_action=True)),
      ('wrong coupling',lambda b:b['fixtures'][0]['certificate'].update(kappa='1/32')),('wrong correlated moment',lambda b:b['joint_moments'][0].update(value='0')),
      ('forged partition normalization',lambda b:b['refinements'][-1]['partition_interval'].update(lower='1',upper='1',width='0')),
      ('coarse width falsely accepted',lambda b:b['refinements'][0].update(status='target-met',width_target_met=True)),
      ('Boolean moment exponent',lambda b:b['joint_moments'][0]['exponents'].__setitem__(0,False)),
      ('wrong graph dagger',lambda b:b['graph']['faces'][0]['word'][0].update(sign=-1)),
      ('source hash replaced',lambda b:b.update(source_sha256='0'*64)),('external passed record',lambda b:b.update(status='passed'))]
    for name,fn in mutations:
        bad=copy.deepcopy(value);fn(bad);gate('reject '+name,not a.strict(bad,expected))
    program="""import sys,json
sys.path.insert(0,sys.argv[1]);import joint
tests={}
def reject(name,fn):
 try:fn()
 except (ValueError,TypeError,AttributeError):tests[name]=True
 else:tests[name]=False
joint.moment([0,0,0]);reject('warm Boolean exponent',lambda:joint.moment([False,0,0]))
reject('Boolean interval endpoint',lambda:joint.divide({'lower':True,'upper':True,'width':'0'},{'lower':'1','upper':'1','width':'0'}))
reject('noncanonical interval endpoint',lambda:joint.divide({'lower':'2/2','upper':'1','width':'0'},{'lower':'1','upper':'1','width':'0'}))
reject('forged interval width',lambda:joint.divide({'lower':'0','upper':'1','width':'0'},{'lower':'1','upper':'1','width':'0'}))
old=joint.WEIGHTS
try:
 joint.WEIGHTS=(2,)
 reject('runtime fixture inventory mutation',lambda:joint.collection())
finally:joint.WEIGHTS=old
print(json.dumps(tests))
"""
    child=subprocess.run([sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+['-c',program,str(source)],text=True,capture_output=True,check=True)
    for name,ok in json.loads(child.stdout).items():gate('actual repaired producer admission: '+name,ok)
    hashes={**{'producer/'+n:d for n,d in actual_sources.items()},'producer/source-manifest.json':sha(source/'source-manifest.json'),
      **{'evidence/'+n:sha(evidence/n) for n in ('completecollection.json','actualgraph.json','refinement.csv','weights.csv')},
      **{'independent/'+n:sha(own/n) for n in ('angular.py','geometry.py','compare.py')}}
    result={'schema':'ym18-independent-c2-comparison-v1','status':'passed','checks_count':len(checks),'checks':checks,'input_sha256':hashes,
      'oracle':'Conditional uniform angular moments and exact semicircle polynomial moments; actual signed geometry independently rebuilt. Producer imported only for repaired public-boundary controls.',
      'scope':'Full rigorous tail bound on a conditional two-link expectation; no complete20facebulk or physical spectral conclusion.'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':main()
