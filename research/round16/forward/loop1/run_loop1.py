"""Run exact finite-geometry gates and independent matrix diagnostics."""
import copy,csv,hashlib,json,math,sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import two_cube as t
out=Path(sys.argv[1] if len(sys.argv)>1 else 'output');out.mkdir(parents=True,exist_ok=True)
gates=[]
def gate(name,ok):
    if not ok:raise RuntimeError(name)
    gates.append(name)
def reject(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError):gates.append(name);return
    raise RuntimeError('invalid input accepted: '+name)
g=t.make_graph();inc=t.validate_graph(g);evidence=t.exact_evidence()
gate('actual12vertex20edge11face complex',(len(g['vertices']),len(g['edges']),len(g['faces']))==(12,20,11))
gate('exactly4triply incident edges',sum(len(v)==3 for v in inc.values())==4)
gate('outer10closed sphere distinct action',len(g['outer_faces'])==10 and 12-20+10==2 and g['full_action']!=g['outer_action'])
gate('rank9 nullity2',evidence['face_edge_rank_mod2']==9 and evidence['face_edge_nullity_mod2']==2)
expected_masks={0}
for ids in [g['cells'][0]['faces'],g['cells'][1]['faces'],g['outer_faces']]:expected_masks.add(sum(1<<i for i,f in enumerate(g['faces']) if f['id'] in ids))
gate('four closed subsets exactly expected',set(evidence['closed_subset_masks'])==expected_masks)
gate('all2048subset moment/index/parity comparisons',len(evidence['subsets'])==2048)
for key,expected in [('left_cube','1/1024'),('right_cube','1/1024'),('outer10','1/262144'),('all11','0'),('outer10_shared_square','1/524288'),('outer10_shared_adjoint','1/262144')]:
    gate('exact reference '+key,evidence['references'][key]['moment']==expected)
gate('mixed fusion channels0and2 required',t.fusion(1,1,0)==t.fusion(1,1,2)==1 and t.fusion(1,1,1)==0)
gate('missing mixed channel falsifier',F(1,4)*F(evidence['references']['outer10']['moment'])!=F(evidence['references']['outer10_shared_square']['moment']))
gate('character coefficient normalization chi1',2*t.char_power(1)[1]==1)
gate('extra dimension normalization falsifier',2*(2*t.char_power(1)[1])==2 and 2*(2*t.char_power(1)[1])!=1)
# Independent one-Haar character triple integration by raw Chebyshev polynomials.
def chebyshev(n):return {n-2*j:F((-1)**j*math.comb(n-j,j)*2**(n-2*j)) for j in range(n//2+1)}
def multiply(a,b):
    c={}
    for i,x in a.items():
        for j,y in b.items():c[i+j]=c.get(i+j,F(0))+x*y
    return c
def haar_x(n):return F(math.comb(n,n//2),(n//2+1)*4**(n//2)) if n%2==0 else F(0)
comparisons=0
for n in range(7):
    for m in range(7):
        for k in range(7):
            poly=multiply(multiply(chebyshev(n),chebyshev(m)),chebyshev(k))
            result=sum((x*haar_x(p) for p,x in poly.items()),F(0))
            if result!=t.fusion(n,m,k):raise RuntimeError('independent Chebyshev Haar triple mismatch')
            comparisons+=1
gate('343independent fusion Haar integrations',comparisons==343)
# Regression of the actual preacceptance mutable-cache failure.
coeff=t.char_power(1);coeff[1]=F(1)
gate('returned character coefficients cannot poison cache',t.char_power(1)[1]==F(1,2) and t.moment(evidence['references']['left_cube']['powers'])==F(1,1024))
reject('Boolean cached power',lambda:t.char_power(True))
reject('Boolean fusion label',lambda:t.fusion(True,1,0))
reject('negative fusion label',lambda:t.fusion(-1,1,0))
reject('fusion cap',lambda:t.fusion(33,1,0))
reject('Boolean moment power',lambda:t.moment([True]+[0]*10))
reject('float moment power',lambda:t.moment([1.]+[0]*10))
reject('wrong face count',lambda:t.moment([0]*10))
reject('total power cap',lambda:t.moment([6]*11))
reject('duplicate subset',lambda:t.index_subset([0,0]))
reject('Boolean subset',lambda:t.index_subset([True]))
reject('Boolean rank row',lambda:t.gf2_rank([True]))
for label,mutate in [
('missing internal face',lambda a:a['faces'].pop(1)),
('duplicate internal face',lambda a:a['faces'].append(copy.deepcopy(a['faces'][1]))),
('single wrong dagger',lambda a:a['faces'][0]['word'][0].update(sign=-a['faces'][0]['word'][0]['sign'])),
('Boolean sign',lambda a:a['faces'][0]['word'][0].update(sign=True)),
('wrong shared identity',lambda a:a.update(shared_face=a['faces'][0]['id'])),
('wrong disk partition',lambda a:a['left_disk'].__setitem__(0,a['right_disk'][0])),
('changed measure',lambda a:a.update(measure='independent11face Haar'))]:
    a=copy.deepcopy(g);mutate(a);reject(label,lambda a=a:t.validate_graph(a))
# Quaternion code and raw complex products are separate arithmetic formulations.
def qmul(p,q):
    a,b,c,d=p;w,x,y,z=q
    return np.array([a*w-b*x-c*y-d*z,a*x+b*w+c*z-d*y,a*y+c*w+d*x-b*z,a*z+d*w+b*y-c*x])
def qdag(q):return np.array([q[0],-q[1],-q[2],-q[3]])
def matrix(q):
    a,b,c,d=q;return np.array([[a+1j*b,c+1j*d],[-c+1j*d,a-1j*b]])
def loop_m(word,links):
    value=np.eye(2,dtype=complex)
    for x in word:value=value@(links[x['edge']] if x['sign']==1 else links[x['edge']].conj().T)
    return value
def loop_q(word,links):
    value=np.array([1.,0,0,0])
    for x in word:value=qmul(value,links[x['edge']] if x['sign']==1 else qdag(links[x['edge']]))
    return value
rng=np.random.default_rng(160910);diagnostics={k:0. for k in ['unitarity','determinant','quaternion_matrix','gauge','reversal','center_prediction','wrong_dagger_defect']}
shared_edges=[x['edge'] for x in next(f for f in g['faces'] if f['id']==g['shared_face'])['word']]
for fixture in range(12):
    quats={e['id']:(lambda a:a/np.linalg.norm(a))(rng.normal(size=4)) for e in g['edges']};links={k:matrix(v) for k,v in quats.items()}
    gauge={v:matrix((lambda a:a/np.linalg.norm(a))(rng.normal(size=4))) for v in g['vertices']}
    transformed={e['id']:gauge[e['tail']]@links[e['id']]@gauge[e['head']].conj().T for e in g['edges']}
    center=dict(links);center[shared_edges[0]]=-center[shared_edges[0]]
    for value in links.values():
        diagnostics['unitarity']=max(diagnostics['unitarity'],float(np.max(np.abs(value.conj().T@value-np.eye(2)))))
        diagnostics['determinant']=max(diagnostics['determinant'],float(abs(np.linalg.det(value)-1)))
    for f in g['faces']:
        raw=loop_m(f['word'],links);qm=matrix(loop_q(f['word'],quats));after=loop_m(f['word'],transformed)
        rev=[{'edge':x['edge'],'sign':-x['sign']} for x in f['word'][::-1]]
        centered=loop_m(f['word'],center);sgn=-1 if any(x['edge']==shared_edges[0] for x in f['word']) else 1
        diagnostics['quaternion_matrix']=max(diagnostics['quaternion_matrix'],float(np.max(np.abs(raw-qm))))
        diagnostics['gauge']=max(diagnostics['gauge'],float(abs(np.trace(raw)-np.trace(after))))
        diagnostics['reversal']=max(diagnostics['reversal'],float(abs(np.trace(raw)-np.trace(loop_m(rev,links)))))
        diagnostics['center_prediction']=max(diagnostics['center_prediction'],float(abs(np.trace(centered)-sgn*np.trace(raw))))
    bad=copy.deepcopy(g['faces'][0]['word']);bad[0]['sign']*=-1
    diagnostics['wrong_dagger_defect']=max(diagnostics['wrong_dagger_defect'],float(abs(np.trace(loop_m(bad,links))-np.trace(loop_m(bad,transformed)))))
for key in diagnostics:
    gate('matrix diagnostic '+key,diagnostics[key]>0.1 if key=='wrong_dagger_defect' else diagnostics[key]<7e-15)
gate('canonical exact evidence replay',t.verify(evidence))
for label,mutate in [
('missing subset evidence',lambda a:a['subsets'].pop()),
('forged rank',lambda a:a.update(face_edge_rank_mod2=True)),
('forged mixed moment',lambda a:a['references']['outer10_shared_square'].update(moment='1/1048576')),
('unmatched source',lambda a:a.update(source_sha256='0'*64)),
('assumed physical gap',lambda a:a.update(assumption='mass gap'))]:
    a=copy.deepcopy(evidence);mutate(a);reject(label,lambda a=a:t.verify(a))
(out/'exact_evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
with (out/'subsets.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['mask','face_count','odd_edge_count','moment_exact']);w.writerows((r['mask'],len(r['selected_faces']),len(r['odd_edges']),r['moment']) for r in evidence['subsets'])
with (out/'references.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['reference','moment_exact','moment_float']);w.writerows((k,v['moment'],float(F(v['moment']))) for k,v in evidence['references'].items())
result={'status':'passed','gate_count':len(gates),'gates':gates,'source_sha256':t.SOURCE_SHA,'graph_sha256':t.graph_hash(),
 'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'evidence_sha256':hashlib.sha256((out/'exact_evidence.json').read_bytes()).hexdigest(),
 'subset_comparisons':2048,'fusion_polynomial_comparisons':343,'matrix_fixtures':12,'matrix_seed':160910,'matrix_diagnostics':diagnostics,
 'references':{k:v['moment'] for k,v in evidence['references'].items()},
 'interpretation':'Loop1 exact finite-complex representation identities; matrix checks are diagnostics; Loop2 nonzero-coupling integral not yet executed.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='gates'},indent=2))
