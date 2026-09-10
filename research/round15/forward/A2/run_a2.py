import copy,csv,hashlib,json,sys
from fractions import Fraction as F
from pathlib import Path
import refine
out=Path(sys.argv[1] if len(sys.argv)>1 else 'output');out.mkdir(parents=True,exist_ok=True)
gates=[]
def gate(name,ok):
    if not ok:raise RuntimeError(name)
    gates.append(name)
def reject(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError):gates.append(name);return
    raise RuntimeError('invalid evidence accepted: '+name)
record=refine.run()
gate('complete adaptive replay',refine.verify(record))
gate('all final transported margins positive',record['status']=='certified-positive-cover')
gate('original coarse failure retained',record['levels'][0]['status']=='insufficient-cover')
gate('all prefinal failures retained',all(x['status']=='insufficient-cover' for x in record['levels'][:-1]))
gate('initial frozen evidence unchanged',refine.digest(refine.A1/'output/cover.json')==refine.A1_EVIDENCE_SHA)
gate('A1 evaluator unchanged',refine.digest(refine.A1/'cover.py')==refine.A1_COVER_SHA)
for cap,expected in [(0,'iteration-cap'),(1,'iteration-cap')]:
    r=refine.run(cap)
    gate('iteration cap '+str(cap)+' explicit insufficiency',r['stop_reason']==expected and r['status']=='insufficient-cover')
    (out/('cap'+str(cap)+'.json')).write_text(json.dumps(r,indent=2)+'\n')
r=refine.run(8,8)
gate('cell cap explicit insufficiency',r['stop_reason']=='cell-cap' and r['status']=='insufficient-cover')
(out/'cell_cap.json').write_text(json.dumps(r,indent=2)+'\n')
reject('Boolean iteration cap',lambda:refine.run(True))
reject('negative iteration cap',lambda:refine.run(-1))
reject('Boolean cell cap',lambda:refine.run(8,True))
reject('too-small cell cap',lambda:refine.run(8,7))
mutations=[
('omitted refinement',lambda a:a['levels'].pop(1)),
('wrong bisection indices',lambda a:a['transitions'][0].update(bisected_indices=[])),
('forged final count',lambda a:a.update(final_cell_count=True)),
('forged policy',lambda a:a.update(policy='silently shortened interval')),
('changed midpoint',lambda a:a['levels'][-1]['cells'][0].update(center='1/8')),
('changed parameter',lambda a:a['levels'][-1]['cells'][0]['certificate']['parameters'].update(k1='2')),
('missing final cell',lambda a:a['levels'][-1]['cells'].pop(1)),
('overlapping cell',lambda a:a['levels'][-1]['cells'][1].update(left='1/8')),
('forged minimum',lambda a:a.update(final_minimum_lower='1')),
('unknown assumption',lambda a:a.update(extra='unreviewed')),
]
for name,mutate in mutations:
    a=copy.deepcopy(record);mutate(a);reject(name,lambda a=a:refine.verify(a))
(out/'refinement.json').write_text(json.dumps(record,indent=2)+'\n')
for i,level in enumerate(record['levels']):
    (out/f'level{i}.json').write_text(json.dumps(level,indent=2)+'\n')
(out/'final_cover.json').write_text(json.dumps(record['levels'][-1],indent=2)+'\n')
with (out/'refinement.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['level','cell_count','insufficient_cells','minimum_lower_exact','minimum_lower_float','status'])
    for i,level in enumerate(record['levels']):w.writerow([i,level['cell_count'],len(level['insufficient_indices']),level['minimum_lower'],float(F(level['minimum_lower'])),level['status']])
with (out/'final_cells.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['index','left','right','center','point_lower','point_upper','transported_lower','transported_upper'])
    for i,c in enumerate(record['levels'][-1]['cells']):
        w.writerow([i,c['left'],c['right'],c['center'],*c['certificate']['enclosures']['covariance'],c['transported_lower'],c['transported_upper']])
result={'status':'passed','gate_count':len(gates),'gates':gates,'scientific_status':record['status'],
        'final_cell_count':record['final_cell_count'],'completed_refinements':record['completed_refinements'],
        'total_evaluated_cells':record['total_evaluated_cells'],
        'minimum_lower_exact':record['final_minimum_lower'],'minimum_lower_float':float(F(record['final_minimum_lower'])),
        'source_sha256':refine.SOURCE_SHA,'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'refinement_sha256':hashlib.sha256((out/'refinement.json').read_bytes()).hexdigest()}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('gates','minimum_lower_exact')},indent=2))
