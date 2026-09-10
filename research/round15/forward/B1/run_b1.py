import copy,csv,hashlib,itertools,json,sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import cube
out=Path(sys.argv[1] if len(sys.argv)>1 else 'output');out.mkdir(parents=True,exist_ok=True)
gates=[]
def gate(name,ok):
    if not ok:raise RuntimeError(name)
    gates.append(name)
def reject(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError):gates.append(name);return
    raise RuntimeError('invalid accepted: '+name)
g=cube.make_graph();gate('oriented cube contract',cube.validate_graph(g))
rows=[]
for mask in range(64):
    chosen=[i for i in range(6) if mask&(1<<i)]
    degrees=[int(i in chosen) for i in range(6)]
    a=cube.moment(degrees);b=cube.subset_index_moment(chosen)
    expected=F(1) if mask==0 else F(1,1024) if mask==63 else F(0)
    gate('subset '+str(mask)+' character/index/expected',a==b==expected)
    rows.append({'mask':mask,'faces':chosen,'character':str(a),'index':str(b)})
gate('nonfactorized full product',cube.moment([1]*6)!=F(0))
pair=[];triple=[]
for p,q in itertools.product(range(6),repeat=2):
    degrees=[0]*6;degrees[p]+=1;degrees[q]+=1
    val=cube.moment(degrees,False)
    gate('character Gram '+str((p,q)),val==int(p==q));pair.append([p,q,str(val)])
for p,q,r in itertools.product(range(6),repeat=3):
    degrees=[0]*6
    for i in (p,q,r):degrees[i]+=1
    val=cube.moment(degrees,False)
    gate('character triple '+str((p,q,r)),val==0);triple.append([p,q,r,str(val)])
gate('single-face fourth Haar moment',cube.moment([4,0,0,0,0,0],False)==2)
gate('two-square fourth Haar independence',cube.moment([2,2,0,0,0,0],False)==1)
gate('six-square nonfactorized moment',cube.moment([2]*6,False)==F(82,81))
rng=np.random.default_rng(151501)
max_product=0.;max_loop=0.;max_gauge=0.;max_reverse=0.;wrong_defects=[]
for fixture in range(16):
    links={e['id']:(lambda a:a/np.linalg.norm(a))(rng.normal(size=4)) for e in g['edges']}
    matrices={e:cube.quaternion_matrix(q) for e,q in links.items()}
    transformations={v:cube.quaternion_matrix((lambda a:a/np.linalg.norm(a))(rng.normal(size=4))) for v in g['vertices']}
    gauged={e['id']:transformations[e['tail']]@matrices[e['id']]@transformations[e['head']].conj().T for e in g['edges']}
    for f in g['faces']:
        qm=cube.quaternion_matrix(cube.quaternion_loop(f['word'],links));raw=cube.matrix_loop(f['word'],matrices)
        max_loop=max(max_loop,float(np.max(np.abs(qm-raw))))
        after=cube.matrix_loop(f['word'],gauged)
        max_gauge=max(max_gauge,float(abs(np.trace(after)-np.trace(raw))))
        reverse=[{'edge':x['edge'],'sign':-x['sign']} for x in f['word'][::-1]]
        max_reverse=max(max_reverse,float(abs(np.trace(cube.matrix_loop(reverse,matrices))-np.trace(raw))))
    p,q=list(links.values())[:2]
    max_product=max(max_product,float(np.max(np.abs(cube.quaternion_matrix(cube.qmul(p,q))-cube.quaternion_matrix(p)@cube.quaternion_matrix(q)))))
    bad=copy.deepcopy(g['faces'][0]['word']);bad[0]['sign']*=-1
    wrong_defects.append(float(abs(np.trace(cube.matrix_loop(bad,matrices))-np.trace(cube.matrix_loop(bad,gauged)))))
gate('independent matrix/quaternion product',max_product<3e-15)
gate('independent matrix/quaternion loop',max_loop<5e-15)
gate('full vertex gauge invariance',max_gauge<5e-15)
gate('whole face reversal invariance',max_reverse<5e-15)
gate('wrong dagger changes gauge invariant observable',max(wrong_defects)>0.1)
for name,change in [
('single dagger graph',lambda a:a['faces'][0]['word'][0].update(sign=-a['faces'][0]['word'][0]['sign'])),
('duplicate face',lambda a:a['faces'].__setitem__(1,copy.deepcopy(a['faces'][0]))),
('Boolean sign',lambda a:a['faces'][0]['word'][0].update(sign=True)),
('Boolean axis',lambda a:a['edges'][0].update(axis=False)),
('missing edge',lambda a:a['edges'].pop()),
('changed action',lambda a:a.update(action='independent six face Haar'))]:
    a=copy.deepcopy(g);change(a);reject(name,lambda a=a:cube.validate_graph(a))
reject('Boolean character power',lambda:cube.char_power(True))
reject('Boolean moment degree',lambda:cube.moment([True,0,0,0,0,0]))
reject('float moment degree',lambda:cube.moment([1.0,0,0,0,0,0]))
reject('wrong number of faces',lambda:cube.moment([0]*5))
reject('duplicate selected face',lambda:cube.subset_index_moment([0,0]))
reject('Boolean selected face',lambda:cube.subset_index_moment([True]))
data={'subsets':rows,'character_gram':pair,'character_triples':triple,
      'six_square_character_moment':'82/81','single_fourth_character_moment':'2'}
(out/'moments.json').write_text(json.dumps(data,indent=2)+'\n')
with (out/'subsets.csv').open('w',newline='') as f:
    w=csv.writer(f);w.writerow(['mask','face_count','moment_exact']);w.writerows((x['mask'],len(x['faces']),x['character']) for x in rows)
result={'status':'passed','gate_count':len(gates),'gates':gates,'source_sha256':cube.SOURCE_SHA,'graph_hash':cube.graph_hash(),
        'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'diagnostics':{'seed':151501,'fixtures':16,'matrix_product_error':max_product,'matrix_loop_error':max_loop,
                       'gauge_error':max_gauge,'whole_reversal_error':max_reverse,'wrong_dagger_maximum_gauge_defect':max(wrong_defects)},
        'interpretation':'Exact finite spherical character moments; matrix gauge checks are floating diagnostics. No volume or continuum claim.'}
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='gates'},indent=2))
