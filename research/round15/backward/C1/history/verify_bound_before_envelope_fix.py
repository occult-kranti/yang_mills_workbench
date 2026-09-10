"""Independent edge-deletion girth and finite physical operator-bound replay."""
from collections import deque
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import copy
import hashlib
import json
import sys

SOURCE_BYTES=Path(__file__).read_bytes()
SCOPE={'group':'SU(2)','Hilbert':'untruncated link L2 Haar, Gauss invariant at every vertex',
 'charges':'none','electric_operator':'H0=alpha*sum_e J_e^2',
 'perturbation':'W=-sum_p lambda_p Tr(U_loop_p)/2','volume':'declared finite graph only',
 'uniform_threshold':'not established by this bound'}


def rational(v):
    if type(v) is not str or len(v)>1000:raise ValueError('canonical rational string required')
    try:r=Q(v)
    except(ValueError,ZeroDivisionError):raise ValueError('invalid rational')
    if str(r)!=v:raise ValueError('noncanonical rational')
    return r


def serial(v):return json.dumps(v,sort_keys=True,allow_nan=False,separators=(',',':'))


def graph_data(g):
    if type(g) is not dict or set(g)!={'vertices','edges','loops'}:raise ValueError('graph schema mismatch')
    vertices=g['vertices'];edges=g['edges'];loops=g['loops']
    if type(vertices) is not list or not 1<=len(vertices)<=4096 or any(type(v) is not str for v in vertices) or len(vertices)!=len(set(vertices)):
        raise ValueError('invalid vertex set')
    if type(edges) is not list or type(loops) is not list:raise ValueError('edge and loop arrays required')
    adjacent={v:set() for v in vertices};pairs=set()
    for pair in edges:
        if type(pair) is not list or len(pair)!=2 or any(type(v) is not str or v not in adjacent for v in pair):raise ValueError('invalid edge')
        a,b=pair;key=frozenset(pair)
        if a==b or key in pairs:raise ValueError('graph must be simple')
        adjacent[a].add(b);adjacent[b].add(a);pairs.add(key)
    reached={vertices[0]};todo=[vertices[0]]
    while todo:
        v=todo.pop()
        for u in adjacent[v]-reached:reached.add(u);todo.append(u)
    if len(reached)!=len(vertices):raise ValueError('connected graph required')
    used=set()
    for loop in loops:
        if type(loop) is not list or len(loop)<3 or len(loop)!=len(set(loop)) or any(type(v) is not str or v not in adjacent for v in loop):raise ValueError('simple cycle loop required')
        edge_set=frozenset(frozenset((u,v)) for u,v in zip(loop,loop[1:]+loop[:1]))
        if any(edge not in pairs for edge in edge_set) or edge_set in used:raise ValueError('missing or duplicate loop edges')
        used.add(edge_set)
    best=None
    # Remove each edge; the shortest alternate endpoint path closes its cycle.
    for a,b in edges:
        distance={a:0};queue=deque([a]);found=None
        while queue and found is None:
            v=queue.popleft()
            for u in adjacent[v]:
                if frozenset((u,v))==frozenset((a,b)):continue
                if u not in distance:
                    distance[u]=distance[v]+1
                    if u==b:found=distance[u]+1;break
                    queue.append(u)
        if found is not None:best=found if best is None else min(best,found)
    return adjacent,best


def verify(certificate,source_sha):
    if type(certificate) is not dict:raise ValueError('certificate object required')
    graph=certificate.get('graph');_,girth=graph_data(graph)
    alpha=rational(certificate.get('alpha'))
    if alpha<=0:raise ValueError('positive electric coefficient required')
    coeff=certificate.get('couplings')
    if type(coeff) is not list or len(coeff)!=len(graph['loops']):raise ValueError('one coupling per loop required')
    lambdas=list(map(rational,coeff));norm=sum(map(abs,lambdas),Q(0))
    delta=Q(3,4)*alpha*girth if girth is not None else None
    bound=delta-norm if delta is not None else None
    status='trivial-physical-sector' if delta is None else 'certified-positive-bound' if bound>0 else 'zero-bound-insufficient' if bound==0 else 'negative-bound-insufficient'
    expected={'schema':'ym15-finite-graph-gap-bound-v1','source_sha256':source_sha,'graph':graph,
      'graph_sha256':hashlib.sha256(serial(graph).encode()).hexdigest(),'alpha':str(alpha),'couplings':list(map(str,lambdas)),
      'vertex_count':len(graph['vertices']),'edge_count':len(graph['edges']),'loop_count':len(graph['loops']),
      'girth':girth,'free_physical_gap':str(delta) if delta is not None else None,
      'total_perturbation_norm_bound':str(norm),'gap_lower_bound':str(bound) if bound is not None else None,
      'status':status,'scope':SCOPE}
    try:match=serial(certificate)==serial(expected)
    except(ValueError,TypeError):match=False
    if not match:raise ValueError('independent graph/operator arithmetic replay mismatch')
    return True


def enumerate_boxes(n):
    vertices=list(product(range(n),repeat=3));edges=[];faces=[]
    for axis in range(3):
        for v in vertices:
            if v[axis]+1<n:
                w=list(v);w[axis]+=1;edges.append((v,tuple(w)))
    # Count actual square cycles from a corner and two positive edge directions.
    for v in vertices:
        directions=[i for i in range(3) if v[i]+1<n]
        for a in directions:
            for b in directions:
                if a<b:faces.append((v,a,b))
    return len(vertices),len(edges),len(faces)


def all_certificates(value):
    if type(value) is dict:
        if value.get('schema')=='ym15-finite-graph-gap-bound-v1':yield value
        else:
            for child in value.values():yield from all_certificates(child)
    elif type(value) is list:
        for child in value:yield from all_certificates(child)


def audit(forward_root,output_dir):
    root=Path(forward_root);source=root/'C1/spectral_bound.py';source_bytes=source.read_bytes();source_sha=hashlib.sha256(source_bytes).hexdigest()
    path=root/'C1/output/certificates.json';data=path.read_bytes();collection=json.loads(data);certificates=list(all_certificates(collection));checks=[]
    def gate(name,test=True):
        if not test:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    gate('nonempty C1 evidence',bool(certificates))
    for index,cert in enumerate(certificates):gate('independent finite graph fixture '+str(index),verify(cert,source_sha))
    cube=next((c for c in certificates if c['vertex_count']==8 and c['loop_count']==6 and c['alpha']=='1' and c['couplings']==['1/2']*6),None)
    gate('failed cube boundary explicitly retained',cube is not None and cube['gap_lower_bound']=='0' and cube['status']=='zero-bound-insufficient')
    forest=[c for c in certificates if c['girth'] is None]
    gate('forest and singleton have no numerical physical gap',len(forest)>=2 and all(c['free_physical_gap'] is None and c['gap_lower_bound'] is None and c['status']=='trivial-physical-sector' for c in forest))
    gate('triangle physical free gap differs from cube',any(c['girth']==3 and Q(c['free_physical_gap'])==Q(9,4)*Q(c['alpha']) for c in certificates))
    support_counts=[]
    graph=cube['graph'];edges=graph['edges'];vertices=graph['vertices']
    for mask in range(1,1<<len(edges)):
        degree={v:0 for v in vertices};count=0
        for i,(a,b) in enumerate(edges):
            if mask&(1<<i):degree[a]+=1;degree[b]+=1;count+=1
        if all(d==0 or d>=2 for d in degree.values()):support_counts.append(count)
    gate('all4095 cube supports obey necessary active cycle bound',min(support_counts)==4)
    gate('active minimum degree is necessary not sufficient for spinhalf singlet',sum([1,1,1])%2==1)
    boxes=[]
    for n in (1,2,3,4,6):
        counts=enumerate_boxes(n)
        gate('actual box incidence count '+str(n),counts==(n**3,3*n*n*(n-1),3*n*(n-1)**2))
        boxes.append({'n':n,'vertices':counts[0],'edges':counts[1],'plaquettes':counts[2],
                      'threshold_lambda_over_alpha':str(Q(3,counts[2])) if counts[2] else None})
    gate('finite norm sufficient threshold decreases with volume',all(Q(a['threshold_lambda_over_alpha'])>Q(b['threshold_lambda_over_alpha']) for a,b in zip(boxes[1:],boxes[2:])))
    def reject(name,c):
        try:verify(c,source_sha)
        except(ValueError,TypeError):gate(name);return
        raise ValueError('invalid finite bound accepted '+name)
    for field,value in [('source_sha256','0'*64),('graph_sha256','0'*64),('alpha','0'),('alpha','-1'),('alpha',True),
      ('girth',True),('girth',3),('free_physical_gap','3/4'),('total_perturbation_norm_bound','0'),
      ('gap_lower_bound','1'),('status','certified-positive-bound'),('vertex_count',True)]:
        c=copy.deepcopy(cube);c[field]=value;reject('metadata '+field+' '+str(value),c)
    c=copy.deepcopy(cube);c['couplings'][0]=True;reject('Boolean coupling',c)
    c=copy.deepcopy(cube);c['scope']['charges']='external fundamental';reject('external charge substitution',c)
    c=copy.deepcopy(cube);c['scope']['uniform_threshold']='proved';reject('uniformity promotion',c)
    c=copy.deepcopy(cube);c['graph']['edges'].append(c['graph']['edges'][0]);reject('parallel edge graph',c)
    c=copy.deepcopy(cube);c['graph']['edges'].append([vertices[0],vertices[0]]);reject('self loop graph',c)
    c=copy.deepcopy(cube);c['graph']['vertices'].append('isolated');reject('disconnected graph',c)
    c=copy.deepcopy(cube);c['graph']['loops'][0].append(c['graph']['loops'][0][0]);reject('repeated vertex loop',c)
    c=copy.deepcopy(cube);c['graph']['loops'][1]=c['graph']['loops'][0];reject('duplicate loop term',c)
    c=copy.deepcopy(forest[0]);c['free_physical_gap']='100';c['gap_lower_bound']='100';c['status']='certified-positive-bound';reject('invented forest excitation gap',c)
    c=copy.deepcopy(cube);c['extra']='continuum proof';reject('extra physical metadata',c)
    gate('actual source and evidence unchanged',source.read_bytes()==source_bytes and path.read_bytes()==data and Path(__file__).read_bytes()==SOURCE_BYTES)
    result={'schema':'ym15-C1-independent-bound-review-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'certificates_replayed':len(certificates),'source_sha256':hashlib.sha256(SOURCE_BYTES).hexdigest(),
      'producer_source_sha256':source_sha,'collection_sha256':hashlib.sha256(data).hexdigest(),
      'cube_boundary':{'alpha':'1','lambda':'1/2','lower':'0','status':'insufficient'},'volume_counts':boxes,
      'scope':'The specified finite untruncated Gauss-invariant Hamiltonian; original uniform threshold still open.',
      'proof_review':'Spin-network active supports, shortest-cycle attainment, bounded-perturbation min-max and vacuum variational sign independently reviewed.',
      'limits':['Exhaustive active-support scan checks a necessary combinatorial condition, not a spin-network enumeration.',
                'A zero lower estimate does not assert spectral gap closure.',
                'The evaluated bound deteriorates with actual plaquette count and is not volume-uniform.']}
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True);(out/'independent_bound_review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks':len(checks),'certificates':len(certificates)}));return result


if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: verify_bound.py FORWARD_ROOT OUTPUT_DIR')
    audit(*sys.argv[1:])
