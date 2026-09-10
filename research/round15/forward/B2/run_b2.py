import copy,csv,hashlib,json,sys
from fractions import Fraction as F
from pathlib import Path
import series
out=Path(sys.argv[1] if len(sys.argv)>1 else 'output');out.mkdir(parents=True,exist_ok=True)
gates=[]
def gate(name,ok):
    if not ok:raise RuntimeError(name)
    gates.append(name)
def reject(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError):gates.append(name);return
    raise RuntimeError('invalid accepted: '+name)
certificates=[]
for n in (0,6,12,18,24):
    c=series.certify(n=n);gate('exact replay N'+str(n),series.verify(c));certificates.append(c)
gate('coarse width failures retained',all(c['expectation_status']=='insufficient-width' for c in certificates[:3]))
gate('degree18 and24 width targets',all(c['expectation_status']=='target-certified' for c in certificates[3:]))
gate('degree12 onward strict excess',all(c['partition_excess_status']=='certified-positive' for c in certificates[2:]))
gate('coarse excess inconclusive retained',all(c['partition_excess_status']=='inconclusive' for c in certificates[:2]))
gate('width decreases each refinement',all(F(a['expectation_width'])>F(b['expectation_width']) for a,b in zip(certificates,certificates[1:])))
zero=series.certify('0',0)
gate('exact Haar six-face baseline',zero['enclosures']['expectation']==['1/1024','1/1024'])
gate('zero coupling no partition excess',zero['enclosures']['partition_excess']==['0','0'])
negative=series.certify('-1/4',24)
gate('common signed coupling symmetry',negative['enclosures']==certificates[-1]['enclosures'])
gate('signed certificate replay',series.verify(negative))
f=certificates[-1]
mutations=[
('wrong dimension polynomial',lambda a:a['polynomial_coefficients']['Aproduct'].__setitem__(0,'1/64')),
('diagonal derivative convention',lambda a:a.update(derivative_convention='sixth common coupling derivative')),
('diagonal derivative insertion',lambda a:a['polynomial_values'].update(Aproduct='6')),
('missing numerator tail',lambda a:a['enclosures'].update(Aproduct=[a['polynomial_values']['Aproduct']]*2)),
('missing normalization error',lambda a:a['enclosures'].update(Z=[a['polynomial_values']['Z']]*2)),
('dropped baseline tail',lambda a:a['enclosures'].update(Zindependent=[a['polynomial_values']['Zindependent']]*2)),
('wrong graph hash',lambda a:a.update(graph_file_sha256='0'*64)),
('wrong source hash',lambda a:a.update(source_sha256='0'*64)),
('Boolean degree',lambda a:a.update(degree=True)),
('Boolean nested degree',lambda a:a['tail'].update(first_omitted_degree=True)),
('wrong coupling',lambda a:a.update(k='1/3')),
('forged width',lambda a:a.update(expectation_width='0')),
('unknown premise',lambda a:a.update(hidden='unreviewed')),
('forged positive excess',lambda a:a['enclosures'].update(partition_excess=['1','2']))]
for name,mut in mutations:
    a=copy.deepcopy(f);mut(a);reject(name,lambda a=a:series.verify(a))
reject('Boolean coupling',lambda:series.certify(True))
reject('float coupling',lambda:series.certify(0.25))
reject('noncanonical coupling',lambda:series.certify('2/8'))
reject('coupling implementation cap',lambda:series.certify('2'))
reject('Boolean degree API',lambda:series.certify(n=True))
reject('degree cap',lambda:series.certify(n=49))
reject('zero precision',lambda:series.certify(precision='0'))
reject('negative precision',lambda:series.certify(precision='-1'))
reject('tail ratio failure',lambda:series.certify('1',0))
series.polynomials(1)
reject('cached Boolean degree',lambda:series.polynomials(True))
reject('Boolean character index',lambda:series.character_series(True,6))
reject('negative normalization',lambda:series.divide_positive((F(0),F(1)),(F(-1),F(2))))
collection={'schema':'ym15-cube-series-collection-v1','certificates':certificates,'zero':zero,'negative':negative}
(out/'certificates.json').write_text(json.dumps(collection,indent=2)+'\n')
with (out/'refinement.csv').open('w',newline='') as h:
    w=csv.writer(h);w.writerow(['degree','expectation_lower','expectation_upper','width_exact','width_float','excess_lower','excess_upper','width_status','excess_status'])
    for c in certificates:w.writerow([c['degree'],*c['enclosures']['expectation'],c['expectation_width'],float(F(c['expectation_width'])),*c['enclosures']['partition_excess'],c['expectation_status'],c['partition_excess_status']])
result={'status':'passed','gate_count':len(gates),'gates':gates,'source_sha256':series.SOURCE_SHA,'graph_file_sha256':series.GRAPH_SHA,
        'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'final_expectation_midpoint_float':float(sum(map(F,f['enclosures']['expectation']))/2),
        'final_width_float':float(F(f['expectation_width'])),
        'final_partition_excess_lower_float':float(F(f['enclosures']['partition_excess'][0])),
        'certificate_collection_sha256':hashlib.sha256((out/'certificates.json').read_bytes()).hexdigest()}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='gates'},indent=2))
