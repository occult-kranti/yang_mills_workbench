"""An explicit finite-graph operator bound, not a uniform local-stability constant."""
from collections import deque
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json
SOURCE_BYTES=Path(__file__).read_bytes();SOURCE_SHA=hashlib.sha256(SOURCE_BYTES).hexdigest()
def unchanged():
    if Path(__file__).read_bytes()!=SOURCE_BYTES:raise ValueError('source changed')
def rational(v):
    if type(v) is not str or len(v)>1000:raise ValueError('canonical rational string required')
    try:x=F(v)
    except (ValueError,ZeroDivisionError) as exc:raise ValueError('invalid rational') from exc
    if str(x)!=v:raise ValueError('noncanonical rational')
    return x
def validate_graph(g):
    if type(g) is not dict or set(g)!={'vertices','edges','loops'}:raise ValueError('wrong finite graph schema')
    v=g['vertices'];e=g['edges'];loops=g['loops']
    if type(v) is not list or not 1<=len(v)<=4096 or any(type(x) is not str for x in v) or len(set(v))!=len(v):raise ValueError('invalid vertices')
    if type(e) is not list or type(loops) is not list:raise ValueError('edges and loops must be lists')
    adjacency={x:set() for x in v};seen=set()
    for pair in e:
        if type(pair) is not list or len(pair)!=2 or any(type(x) is not str or x not in adjacency for x in pair):raise ValueError('invalid edge')
        a,b=pair;key=tuple(sorted(pair))
        if a==b or key in seen:raise ValueError('graph must be simple')
        seen.add(key);adjacency[a].add(b);adjacency[b].add(a)
    reached={v[0]};queue=deque(reached)
    while queue:
        for b in adjacency[queue.popleft()]:
            if b not in reached:reached.add(b);queue.append(b)
    if len(reached)!=len(v):raise ValueError('graph must be connected')
    loopkeys=set()
    for loop in loops:
        if type(loop) is not list or len(loop)<3 or any(type(x) is not str or x not in adjacency for x in loop) or len(set(loop))!=len(loop):raise ValueError('simple distinct-link loop required')
        keys=[]
        for a,b in zip(loop,loop[1:]+loop[:1]):
            key=tuple(sorted((a,b)))
            if key not in seen:raise ValueError('loop uses missing edge')
            keys.append(key)
        canonical=tuple(sorted(keys))
        if canonical in loopkeys:raise ValueError('duplicate loop term; combine coefficients explicitly')
        loopkeys.add(canonical)
    return adjacency
def girth(g):
    adjacency=validate_graph(g);best=None
    for root in adjacency:
        dist={root:0};parent={root:None};queue=deque([root])
        while queue:
            a=queue.popleft()
            for b in adjacency[a]:
                if b not in dist:dist[b]=dist[a]+1;parent[b]=a;queue.append(b)
                elif parent[a]!=b:
                    size=dist[a]+dist[b]+1
                    if best is None or size<best:best=size
    return best
def box_graph(n):
    if type(n) is not int or not 1<=n<=16:raise ValueError('box vertices-per-axis must be integer1..16')
    name=lambda v:','.join(map(str,v))
    vertices=[name(v) for v in product(range(n),repeat=3)];edges=[];loops=[]
    for v in product(range(n),repeat=3):
        for axis in range(3):
            if v[axis]+1<n:
                w=list(v);w[axis]+=1;edges.append([name(v),name(w)])
        for a,b in ((0,1),(0,2),(1,2)):
            if v[a]+1<n and v[b]+1<n:
                x=list(v);x[a]+=1;y=x.copy();y[b]+=1;z=list(v);z[b]+=1
                loops.append(list(map(name,(v,x,y,z))))
    return {'vertices':vertices,'edges':edges,'loops':loops}
def certify(graph,alpha='1',couplings=None):
    unchanged();girth_value=girth(graph);a=rational(alpha)
    if a<=0:raise ValueError('alpha must be strictly positive')
    if type(couplings) is not list or len(couplings)!=len(graph['loops']):raise ValueError('one exact coupling per loop required')
    lambdas=list(map(rational,couplings));total=sum(map(abs,lambdas),F(0))
    delta=F(3,4)*a*girth_value if girth_value else None
    lower=delta-total if delta is not None else None
    status='trivial-physical-sector' if delta is None else 'certified-positive-bound' if lower>0 else 'zero-bound-insufficient' if lower==0 else 'negative-bound-insufficient'
    return {'schema':'ym15-finite-graph-gap-bound-v1','source_sha256':SOURCE_SHA,'graph':graph,
      'graph_sha256':hashlib.sha256(json.dumps(graph,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
      'alpha':str(a),'couplings':list(map(str,lambdas)),'vertex_count':len(graph['vertices']),'edge_count':len(graph['edges']),
      'loop_count':len(graph['loops']),'girth':girth_value,'free_physical_gap':str(delta) if delta is not None else None,
      'total_perturbation_norm_bound':str(total),'gap_lower_bound':str(lower) if lower is not None else None,'status':status,
      'scope':{'group':'SU(2)','Hilbert':'untruncated link L2 Haar, Gauss invariant at every vertex',
               'charges':'none','electric_operator':'H0=alpha*sum_e J_e^2',
               'perturbation':'W=-sum_p lambda_p Tr(U_loop_p)/2',
               'volume':'declared finite graph only','uniform_threshold':'not established by this bound'}}
def typed_equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(typed_equal(a[k],b[k]) for k in b)
    if type(a) is list:return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b
def verify(c):
    if type(c) is not dict or c.get('schema')!='ym15-finite-graph-gap-bound-v1':raise ValueError('wrong schema')
    expected=certify(c.get('graph'),c.get('alpha'),c.get('couplings'))
    if not typed_equal(c,expected):raise ValueError('operator bound or contract failed replay')
    return True
