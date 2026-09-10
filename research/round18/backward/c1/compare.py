"""Complete coordinate-oracle replay of the frozen Gram-recurrence evidence."""
from pathlib import Path
import argparse,copy,csv,hashlib,json,subprocess,sys
import coordinates as c

PRODUCER_SHA='4341fff1345d12e6b4f1d2d8b72f1aa40ccc04d422b2d2ef64533dcc84cb7171'


def expected_certificate(d,source_sha):
    return {'schema':'ym18-c1-certificate-v1','source_sha256':source_sha,'vectors':d['vectors'],'gram':d['joint_Gram'],
      'rank':d['admissibility']['rank'],'kappa':d['kappa'],'vector_order':['b','a1','a2','a3','a4'],
      'dimension':4,'formal_parameter':'t; not physical time','degree':6,
      'observable':'product_i(4(q dot a_i)^2-1)/81','action':'q dot b with b=sum_i kappa_i a_i',
      'numerator_coefficients':d['numerator_coefficients'],'partition_coefficients':d['partition_coefficients'],
      'primitive_moments':d['primitive_moments'],'coefficient_convention':'[t^n] includes 1/n! for exp(t q dot b)',
      'scope':'exact degree-zero-through-six diagnostics; no tail certificate or surrounding-link integration',
      'admissibility':'symmetric PSD rank<=4, unit directions, full action cross and norm constraints'}


def expected_collection():
    own=c.collection()
    return {'schema':'ym18-c1-collection-v1','source_sha256':PRODUCER_SHA,'dimension':4,'degree':6,'vector_order':['b','a1','a2','a3','a4'],
      'fixtures':[{'id':f['id'],'certificate':expected_certificate(f['data'],PRODUCER_SHA)} for f in own['fixtures']],
      'historical_convention':{'round17':'trace directions were conjugate boundary quaternions (h0,-h1,-h2,-h3)',
       'current':'base fixtures use the listed h coordinates as direction vectors',
       'common_reflection_to_round17':[['1','0','0','0'],['0','-1','0','0'],['0','0','-1','0'],['0','0','0','-1']],
       'effect':'transform every action and observable direction together; complete Gram unchanged; common scalar-axis action unchanged'},
      'isometry_scope':'full untruncated central integrals of the declared dot-product observable/action family; no transformation of surrounding-link measure',
      'coefficient_scope':'formal Taylor coefficients only; t is not physical time and no finite-t error bound is claimed'}


def verify(value):
    if not c.strict(value,expected_collection()):raise ValueError('complete independent coordinate replay differs')
    return True


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--producer',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ns=ap.parse_args()
    source,evidence,out=ns.producer.resolve(),ns.evidence.resolve(),ns.output.resolve();own=Path(__file__).resolve().parent
    if out.is_relative_to(own):raise ValueError('output outside source required')
    sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
    def gate(name,ok):
        if type(ok) is not bool or not ok:raise ValueError('failed comparison: '+name)
        checks.append({'name':name,'passed':True})
    manifest=json.loads((source/'source-manifest.json').read_text());ignored={'output','output-optimized','comparison','comparison-optimized'}
    actual={str(p.relative_to(source)):sha(p) for p in source.rglob('*') if p.is_file() and p!=source/'source-manifest.json' and '__pycache__' not in p.relative_to(source).parts and p.relative_to(source).parts[0] not in ignored}
    gate('complete frozen source inventory and reviewed Gram source match',c.strict(manifest['files'],actual) and sha(source/'gram.py')==PRODUCER_SHA)
    value=json.loads((evidence/'collection.json').read_text());expected=expected_collection()
    gate('all eleven ordered required geometries are present',c.strict([f['id'] for f in value['fixtures']],[f['id'] for f in expected['fixtures']]))
    for f,g in zip(value['fixtures'],expected['fixtures']):gate('full coordinates, Gram, 112 primitives and seven coefficient pairs: '+g['id'],c.strict(f,g))
    gate('complete source-bound schema and scientific scope agree',c.strict(value,expected))
    rows=[{'fixture':f['id'],'degree':str(n),'numerator':f['certificate']['numerator_coefficients'][n],
      'partition':f['certificate']['partition_coefficients'][n],'rank':str(f['certificate']['rank'])} for f in expected['fixtures'] for n in range(7)]
    with (evidence/'coefficients.csv').open(newline='') as stream:csv_value=list(csv.DictReader(stream))
    gate('all 77 plotted coefficient pairs agree with independent coordinate integration',c.strict(rows,csv_value))
    # Derive the historical conjugation convention by another actual common reflection.
    historical=[]
    for f in expected['fixtures'][:2]:
        original=f['certificate'];a=[[v[0]]+[str(-c.F(x)) for x in v[1:]] for v in original['vectors'][1:]]
        d=c.data(a,original['kappa']);historical.append(d['joint_Gram']==original['gram'] and d['b']==original['vectors'][0] and d['numerator_coefficients']==original['numerator_coefficients'])
    gate('historical conjugation reflection preserves complete Gram and common scalar action',all(historical))
    mutations=[('missing fixture',lambda b:b['fixtures'].pop()),
      ('changed actual action vector',lambda b:b['fixtures'][0]['certificate']['vectors'][0].__setitem__(0,'1/4')),
      ('action-only observable cache',lambda b:b['fixtures'][1]['certificate'].update(numerator_coefficients=b['fixtures'][0]['certificate']['numerator_coefficients'])),
      ('missing primitive moment',lambda b:b['fixtures'][0]['certificate']['primitive_moments'].pop()),
      ('Boolean primitive exponent alias',lambda b:b['fixtures'][0]['certificate']['primitive_moments'][0]['exponents'].__setitem__(0,False)),
      ('factorial omitted',lambda b:b['fixtures'][0]['certificate']['partition_coefficients'].__setitem__(2,'1/256')),
      ('external passed result',lambda b:b.update(status='passed')),
      ('source digest changed',lambda b:b.update(source_sha256='0'*64)),
      ('Taylor polynomial falsely called a full integral',lambda b:b.update(coefficient_scope='full weighted integral with zero error'))]
    for name,fn in mutations:
        changed=copy.deepcopy(value);fn(changed);gate('reject '+name,not c.strict(changed,expected))
    # Public-boundary probes import the producer only after independent arithmetic replay.
    # No author moment or validator supplies the independently reconstructed coefficients.
    program="""import copy,json,sys
sys.path.insert(0,sys.argv[1]);import gram
f=gram.collection()['fixtures'][0]['certificate'];g=f['gram'];k=f['kappa'];gram.moment(g,k,[0]*5);tests={}
def rejects(name,fn):
 try:fn()
 except (ValueError,TypeError,AttributeError):tests[name]=True
 else:tests[name]=False
rejects('warm Boolean exponent',lambda:gram.moment(g,k,[False,0,0,0,0]))
bad=copy.deepcopy(g);bad[1][2]=False
rejects('warm nested Boolean Gram',lambda:gram.moment(bad,k,[0]*5))
old=gram.DIMENSION
try:
 gram.DIMENSION=5
 rejects('runtime dimension change',lambda:gram.collection())
finally:gram.DIMENSION=old
num,den=gram.coefficients(g,k)
rejects('immutable coefficient assignment',lambda:num.__setitem__(0,0))
f['numerator_coefficients'][0]='0'
rejects('mutated returned evidence',lambda:gram.verify(f))
tests['defensive future certificate']=gram.certify(f['vectors'][1:],k)['numerator_coefficients'][0]=='-1/405'
print(json.dumps(tests))
"""
    child=subprocess.run([sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+['-c',program,str(source)],text=True,capture_output=True,check=True)
    for name,ok in json.loads(child.stdout).items():gate('actual producer admission: '+name,ok)
    hashes={**{'producer/'+n:d for n,d in actual.items()},'producer/source-manifest.json':sha(source/'source-manifest.json'),
      **{'evidence/'+n:sha(evidence/n) for n in ('collection.json','coefficients.csv')},
      **{'independent/'+n:sha(own/n) for n in ('coordinates.py','compare.py')}}
    result={'schema':'ym18-independent-c1-comparison-v1','status':'passed','checks_count':len(checks),'checks':checks,'input_sha256':hashes,
      'oracle':'Actual coordinate polynomial multiplication plus S3 monomial factorial formula; all principal minors and Gaussian row rank. Producer imported only for public-boundary mutation probes.',
      'scope':'Complete joint-Gram sufficiency is confined to the declared central family; finite coefficients do not supply a weighted-error certificate or surrounding-link measure reduction.'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':main()
