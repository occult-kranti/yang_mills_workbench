"""Finite two-cube Wilson complex: exact geometry, character fusion and Haar moments."""
from fractions import Fraction as F
from collections import deque
from itertools import product
from pathlib import Path
from functools import lru_cache
import hashlib,json,math

SOURCE_BYTES=Path(__file__).read_bytes();SOURCE_SHA=hashlib.sha256(SOURCE_BYTES).hexdigest()
def unchanged():
    if Path(__file__).read_bytes()!=SOURCE_BYTES:raise ValueError('source changed after load')
def name(v):return ','.join(map(str,v))
def make_graph():
    vertices=[name(v) for v in product(range(3),range(2),range(2))];edges=[]
    for v in product(range(3),range(2),range(2)):
        for axis,extent in enumerate((3,2,2)):
            if v[axis]+1<extent:
                w=list(v);w[axis]+=1
                edges.append({'id':'e'+str(axis)+':'+name(v),'tail':name(v),'head':name(w),'axis':axis})
    lookup={(e['tail'],e['head']):(e['id'],1) for e in edges}
    lookup.update({(e['head'],e['tail']):(e['id'],-1) for e in edges})
    faces=[]
    for normal in range(3):
        tangents=[i for i in range(3) if i!=normal]
        ranges=[range((3,2,2)[i]) if i==normal else range((3,2,2)[i]-1) for i in range(3)]
        for base in product(*ranges):
            a=list(base);a[tangents[0]]+=1
            b=a.copy();b[tangents[1]]+=1
            c=list(base);c[tangents[1]]+=1
            loop=list(map(name,(base,a,b,c)))
            orientation=-1 if base[normal]==0 else 1
            cross_sign=1 if normal in (0,2) else -1
            if cross_sign!=orientation:loop=[loop[0],*loop[:0:-1]]
            word=[{'edge':lookup[(loop[i],loop[(i+1)%4])][0],'sign':lookup[(loop[i],loop[(i+1)%4])][1]} for i in range(4)]
            shared=normal==0 and base[0]==1
            region='shared' if shared else 'left' if (normal==0 and base[0]==0) or (normal!=0 and base[0]==0) else 'right'
            faces.append({'id':'f'+str(normal)+':'+name(base),'normal':normal,'base':list(base),'vertices':loop,'word':word,'region':region})
    left=[f['id'] for f in faces if f['region']=='left'];right=[f['id'] for f in faces if f['region']=='right'];shared=[f['id'] for f in faces if f['region']=='shared'][0]
    return {'schema':'ym16-adjacent-two-cubes-v1','vertices':vertices,'edges':edges,'faces':faces,
      'left_disk':left,'right_disk':right,'shared_face':shared,'outer_faces':left+right,
      'cells':[{'id':'left','faces':left+[shared],'shared_orientation':1},
               {'id':'right','faces':right+[shared],'shared_orientation':-1}],
      'group':'SU(2)','measure':'independent normalized Haar on20 oriented links',
      'full_action':'sum over11 distinct face coefficients k_f*Tr(U_face_f)/2; internal face counted once',
      'outer_action':'sum over10 outer face coefficients only; shared coefficient0',
      'time_generator':'none; finite Euclidean measure',
      'energy_scale':'no Hamiltonian energy scale is defined by these Euclidean couplings'}
def strict_equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict_equal(a[k],b[k]) for k in b)
    if type(a) is list:return len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b))
    return a==b
def validate_graph(g):
    unchanged()
    if not strict_equal(g,make_graph()):raise ValueError('graph differs from reviewed two-cube contract')
    edge_map={e['id']:e for e in g['edges']};inc={x:[] for x in edge_map}
    for i,f in enumerate(g['faces']):
        if len(set(f['vertices']))!=4:raise ValueError('face is not simple')
        for j,x in enumerate(f['word']):
            e=edge_map[x['edge']];ends=(e['tail'],e['head']) if x['sign']==1 else (e['head'],e['tail'])
            if ends!=(f['vertices'][j],f['vertices'][(j+1)%4]):raise ValueError('nonclosed boundary word')
            inc[x['edge']].append((i,x['sign']))
    shared=next(f for f in g['faces'] if f['id']==g['shared_face']);boundary={x['edge'] for x in shared['word']}
    if {e for e,v in inc.items() if len(v)==3}!=boundary or any(len(v)!=(3 if e in boundary else 2) for e,v in inc.items()):raise ValueError('wrong edge incidence')
    outer=set(g['outer_faces'])
    if any(sorted(s for i,s in v if g['faces'][i]['id'] in outer)!=[-1,1] for v in inc.values()):raise ValueError('outer faces fail closed orientation')
    if len(g['vertices'])-len(g['edges'])+len(g['outer_faces'])!=2:raise ValueError('outer sphere Euler mismatch')
    return inc
def graph_hash():return hashlib.sha256(json.dumps(make_graph(),sort_keys=True,separators=(',',':')).encode()).hexdigest()
def bounded_int(v,maximum=48):
    if type(v) is not int or not 0<=v<=maximum:raise ValueError('bounded nonnegative integer required, not Boolean')
    return v
def char_power(power):
    return _char_power(bounded_int(power,16))
@lru_cache(maxsize=None)
def _char_power(power):
    coeff={0:F(1)}
    for _ in range(power):
        nxt={}
        for n,c in coeff.items():
            nxt[n+1]=nxt.get(n+1,F(0))+c/2
            if n:nxt[n-1]=nxt.get(n-1,F(0))+c/2
        coeff=nxt
    return coeff
def fusion(n,m,k):
    n,m,k=[bounded_int(v,32) for v in (n,m,k)]
    return int(abs(n-m)<=k<=n+m and (n+m+k)%2==0)
def validate_degrees(powers):
    if type(powers) is not list or len(powers)!=11:raise ValueError('eleven face powers required')
    values=[bounded_int(v,16) for v in powers]
    if sum(values)>64:raise ValueError('total moment degree cap64')
    return values
def center_parity(powers):
    values=validate_degrees(powers);g=make_graph();inc=validate_graph(g)
    return {e:sum(values[i] for i,_ in terms)%2 for e,terms in inc.items()}
def moment(powers):
    """Normalized trace powers on all11 faces via two5-face disks and SU2 fusion."""
    unchanged();values=validate_degrees(powers);g=make_graph();coef=[char_power(p) for p in values]
    left=[i for i,f in enumerate(g['faces']) if f['region']=='left'];right=[i for i,f in enumerate(g['faces']) if f['region']=='right'];shared=next(i for i,f in enumerate(g['faces']) if f['region']=='shared')
    def disk(ids):
        labels=set.intersection(*(set(coef[i]) for i in ids))
        return {n:math.prod(coef[i][n] for i in ids)/F((n+1)**4) for n in labels}
    lc,rc=disk(left),disk(right)
    return sum((a*b*c*fusion(n,m,k) for n,a in lc.items() for m,b in rc.items() for k,c in coef[shared].items()),F(0))
def gf2_rank(rows):
    if type(rows) is not list or any(type(r) is not int or r<0 for r in rows):raise ValueError('nonnegative integer bit rows required')
    pivots={}
    for r in rows:
        while r:
            p=r.bit_length()-1
            if p not in pivots:pivots[p]=r;break
            r^=pivots[p]
    return len(pivots)
def index_subset(selected):
    """Independent pairwise fundamental Haar contractions for closed Z2 face subsets."""
    if type(selected) is not list or any(type(i) is not int or not 0<=i<11 for i in selected) or len(set(selected))!=len(selected):raise ValueError('distinct integer face indices required')
    g=make_graph();inc=validate_graph(g);occ={e:[(i,s) for i,s in x if i in selected] for e,x in inc.items()}
    if any(len(x)%2 for x in occ.values()):return F(0)
    flips={}
    for start in selected:
        if start in flips:continue
        flips[start]=1;queue=deque([start])
        while queue:
            i=queue.popleft()
            for terms in occ.values():
                if len(terms)!=2 or all(j!=i for j,_ in terms):continue
                (a,sa),(b,sb)=terms;j=b if a==i else a
                need=-sa*sb*flips[i]
                if j in flips and flips[j]!=need:raise ValueError('selected surface not orientable')
                if j not in flips:flips[j]=need;queue.append(j)
    parent={};edge_terms={e:[] for e in inc}
    for i in selected:
        word=g['faces'][i]['word']
        if flips[i]==-1:word=[{'edge':x['edge'],'sign':-x['sign']} for x in word[::-1]]
        for j,x in enumerate(word):
            a=(i,j);b=(i,(j+1)%4);parent[a]=a;parent[b]=b
            edge_terms[x['edge']].append((x['sign'],a,b))
    def find(a):
        while parent[a]!=a:a=parent[a]
        return a
    def union(a,b):parent[find(a)]=find(b)
    used=0
    for vals in edge_terms.values():
        if not vals:continue
        if len(vals)!=2 or vals[0][0]+vals[1][0]!=0:raise ValueError('invalid paired Haar contraction')
        (_,a,b),(_,c,d)=vals;union(a,d);union(b,c);used+=1
    free=len({find(x) for x in parent})
    return F(2**free,2**(used+len(selected)))
