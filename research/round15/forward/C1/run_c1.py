import copy,csv,hashlib,json,sys
from fractions import Fraction as F
from pathlib import Path
import spectral_bound as s
out=Path(sys.argv[1] if len(sys.argv)>1 else 'output');out.mkdir(parents=True,exist_ok=True)
gates=[]
def gate(name,ok):
    if not ok:raise RuntimeError(name)
    gates.append(name)
def reject(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError):gates.append(name);return
    raise RuntimeError('invalid accepted: '+name)
cube=s.box_graph(2);fixtures=[]
for lam in ['0','1/8','1/4','1/2','3/4','-1/2']:
    c=s.certify(cube,'1',[lam]*6);gate('cube replay lambda'+lam,s.verify(c));fixtures.append(c)
    gate('cube exact lower lambda'+lam,F(c['gap_lower_bound'])==3-6*abs(F(lam)))
gate('boundary remains insufficient',fixtures[3]['status']=='zero-bound-insufficient')
gate('beyond boundary remains insufficient',fixtures[4]['status']=='negative-bound-insufficient')
gate('zero perturbation exact free gap',fixtures[0]['gap_lower_bound']=='3')
scaled=s.certify(cube,'2',['1/2']*6)
gate('rational scaling correct',scaled['gap_lower_bound']=='3')
anisotropic=s.certify(cube,'1',['1/8','-1/4','0','1/16','0','-1/16'])
gate('signed sum uses absolute values',anisotropic['total_perturbation_norm_bound']=='1/2')
forest={'vertices':['a','b','c'],'edges':[['a','b'],['b','c']],'loops':[]}
tree=s.certify(forest,'1',[]);gate('forest trivial physical sector',tree['status']=='trivial-physical-sector' and tree['gap_lower_bound'] is None)
single=s.certify(s.box_graph(1),'1',[]);gate('one vertex vacuum-only sector',single['status']=='trivial-physical-sector')
triangle={'vertices':['a','b','c'],'edges':[['a','b'],['b','c'],['c','a']],'loops':[['a','b','c']]}
tri=s.certify(triangle,'1',['1/4']);gate('triangle physical free gap',tri['free_physical_gap']=='9/4' and tri['gap_lower_bound']=='2')
dangling=copy.deepcopy(triangle);dangling['vertices'].append('d');dangling['edges'].append(['c','d'])
gate('Gauss-constrained dangling edge leaves gap',s.certify(dangling,'1',['1/4'])['free_physical_gap']=='9/4')
volumes=[]
for n in [2,3,4,6]:
    g=s.box_graph(n);p=3*n*(n-1)**2
    gate('actual box plaquette count n'+str(n),len(g['loops'])==p)
    gate('actual box edge count n'+str(n),len(g['edges'])==3*n*n*(n-1))
    c=s.certify(g,'1',['1/8']*p)
    gate('box girth n'+str(n),c['girth']==4)
    gate('actual volume norm bound n'+str(n),c['gap_lower_bound']==str(3-F(p,8)))
    volumes.append({'n':n,'vertices':len(g['vertices']),'edges':len(g['edges']),'plaquettes':p,
                    'girth':c['girth'],'lambda':'1/8','gap_lower_bound':c['gap_lower_bound'],
                    'positive_threshold_lambda_over_alpha':str(F(3,p)),'status':c['status']})
mutations=[
('Boolean girth',lambda c:c.update(girth=True)),
('forged positive boundary',lambda c:c.update(status='certified-positive-bound')),
('two norm substitution',lambda c:c.update(gap_lower_bound='-3')),
('changed alpha',lambda c:c.update(alpha='2')),
('changed source',lambda c:c.update(source_sha256='0'*64)),
('wrong physical sector',lambda c:c['scope'].update(Hilbert='ungauged')),
('invented uniform threshold',lambda c:c['scope'].update(uniform_threshold='1/2 for all volumes')),
('missing coupling',lambda c:c['couplings'].pop()),
('Boolean coupling',lambda c:c['couplings'].__setitem__(0,True)),
('extra assumption',lambda c:c.update(assume='mass gap'))]
for name,mut in mutations:
    c=copy.deepcopy(fixtures[3]);mut(c);reject(name,lambda c=c:s.verify(c))
reject('zero alpha',lambda:s.certify(cube,'0',['0']*6))
reject('negative alpha',lambda:s.certify(cube,'-1',['0']*6))
reject('Boolean alpha',lambda:s.certify(cube,True,['0']*6))
reject('float coupling',lambda:s.certify(cube,'1',[0.]*6))
reject('Boolean box size',lambda:s.box_graph(True))
reject('box cap',lambda:s.box_graph(17))
for name,mut in [
('self loop',lambda g:g['edges'].append([g['vertices'][0]]*2)),
('parallel edge',lambda g:g['edges'].append(g['edges'][0][::-1])),
('disconnected vertex',lambda g:g['vertices'].append('isolated')),
('repeated loop vertex',lambda g:g['loops'][0].append(g['loops'][0][0])),
('duplicate plaquette',lambda g:g['loops'].append(g['loops'][0][::-1])),
('missing loop edge',lambda g:g['edges'].pop(0)),
('Boolean vertex',lambda g:g['vertices'].__setitem__(0,True))]:
    g=copy.deepcopy(cube);mut(g);reject(name,lambda g=g:s.validate_graph(g))
collection={'schema':'ym15-c1-collection-v1','cube':fixtures,'scaled':scaled,'anisotropic':anisotropic,'forest':tree,'singleton':single,'triangle':tri,'volumes':volumes}
(out/'certificates.json').write_text(json.dumps(collection,indent=2)+'\n')
with (out/'volume.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(volumes[0]));w.writeheader();w.writerows(volumes)
with (out/'cube.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['lambda','alpha','free_gap','gap_lower','status'])
    for c in fixtures:w.writerow([c['couplings'][0],c['alpha'],c['free_physical_gap'],c['gap_lower_bound'],c['status']])
result={'status':'passed','gate_count':len(gates),'gates':gates,'source_sha256':s.SOURCE_SHA,
        'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'certificate_sha256':hashlib.sha256((out/'certificates.json').read_bytes()).hexdigest(),
        'original_uniform_threshold_status':'open; existential source constants not extracted',
        'finite_cube_boundary_outcome':fixtures[3]['status'],
        'interpretation':'Finite untruncated operator inequality; nonpositive estimate is insufficient, not evidence of physical gap closure.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='gates'},indent=2))
