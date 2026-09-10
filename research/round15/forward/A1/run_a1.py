"""Execute deliberately coarse cover, retaining insufficient transported cells."""
import copy,csv,hashlib,json,sys
from fractions import Fraction as F
from pathlib import Path
import cover

out=Path(sys.argv[1] if len(sys.argv)>1 else 'output')
out.mkdir(parents=True,exist_ok=True)
gates=[]
def gate(name,condition):
    if not condition: raise RuntimeError(name)
    gates.append(name)
def reject(name,fn):
    try: fn()
    except (ValueError,TypeError,KeyError): gates.append(name); return
    raise RuntimeError('invalid input accepted: '+name)

c=cover.uniform(8,24)
gate('full canonical replay',cover.verify(c))
gate('requested eight closed cells',c['cell_count']==8)
gate('all midpoint point certificates positive',all(x['certificate']['status']=='certified-positive' for x in c['cells']))
gate('coarse transport correctly insufficient',c['status']=='insufficient-cover')
gate('insufficient cells retained',len(c['insufficient_indices'])>0)
mutations=[
 ('Boolean count',lambda a:a.update(cell_count=True)),
 ('Boolean degree',lambda a:a.update(degree=True)),
 ('empty cells',lambda a:a.update(cells=[])),
 ('wrong target',lambda a:a.update(target=['1/8','1/3'])),
 ('weakened Lipschitz',lambda a:a.update(lipschitz='1')),
 ('wrong parameter',lambda a:a['fixed_parameters'].update(k1='2')),
 ('wrong midpoint',lambda a:a['cells'][0].update(center='1/8')),
 ('missing cell',lambda a:a['cells'].pop(3)),
 ('gap',lambda a:a['cells'][3].update(left='3/16')),
 ('wrong left boundary',lambda a:a['cells'][0].update(left='0')),
 ('wrong source',lambda a:a.update(point_source_sha256='0'*64)),
 ('wrong derivative source',lambda a:a.update(derivative_source_sha256='0'*64)),
 ('forged positive status',lambda a:a.update(status='certified-positive-cover')),
 ('forged lower',lambda a:a['cells'][0].update(transported_lower='1')),
 ('point mutation',lambda a:a['cells'][0]['certificate']['parameters'].update(eta='1/4')),
 ('Boolean nested degree',lambda a:a['cells'][0]['certificate'].update(degree=True)),
 ('unexpected metadata',lambda a:a.update(hidden_assumption=True)),
]
for name,mutate in mutations:
    bad=copy.deepcopy(c); mutate(bad)
    reject(name,lambda bad=bad:cover.verify(bad))
reject('uniform Boolean count',lambda:cover.uniform(True))
reject('uniform zero count',lambda:cover.uniform(0))
reject('uniform float count',lambda:cover.uniform(8.0))
reject('reversed edges',lambda:cover.build(['1/8','1/4','3/16','1/4']))
reject('duplicate edge',lambda:cover.build(['1/8','1/8','1/4']))
reject('noncanonical edge',lambda:cover.build(['2/16','1/4']))
reject('float edge',lambda:cover.build([0.125,'1/4']))
cover.save(out/'cover.json',c)
with (out/'cells.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['index','left','right','center','point_lower','point_upper','transported_lower','transported_upper','status'])
    for i,cell in enumerate(c['cells']):
        lo,hi=cell['certificate']['enclosures']['covariance']
        w.writerow([i,cell['left'],cell['right'],cell['center'],lo,hi,cell['transported_lower'],cell['transported_upper'],cell['status']])
with (out/'plot_data.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['index','left','right','center','point_lower','point_upper','transported_lower','transported_upper'])
    for i,cell in enumerate(c['cells']):
        vals=[cell['left'],cell['right'],cell['center'],*cell['certificate']['enclosures']['covariance'],cell['transported_lower'],cell['transported_upper']]
        w.writerow([i,*[format(float(F(v)),'.17g') for v in vals]])
result={'status':'passed','experiment_outcome':c['status'],'gate_count':len(gates),'gates':gates,
        'cell_count':c['cell_count'],'insufficient_indices':c['insufficient_indices'],
        'minimum_lower':c['minimum_lower'],'minimum_lower_float':float(F(c['minimum_lower'])),
        'source_sha256':cover.SOURCE_SHA,'point_source_sha256':cover.POINT_SHA,
        'derivative_source_sha256':cover.THEOREM_SHA,
        'cover_sha256':hashlib.sha256((out/'cover.json').read_bytes()).hexdigest(),
        'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'interpretation':'Correctly executed coarse bound; point positivity does not certify positivity between these coarse centers.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('minimum_lower','gates')},indent=2))
