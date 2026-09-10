"""Oriented cube boundary and exact spherical SU(2) character moments."""
from fractions import Fraction as F
from itertools import product
import hashlib,json,math
from pathlib import Path
import numpy as np

SOURCE_BYTES=Path(__file__).read_bytes();SOURCE_SHA=hashlib.sha256(SOURCE_BYTES).hexdigest()
def _unchanged():
    if Path(__file__).read_bytes()!=SOURCE_BYTES:raise ValueError('cube source changed')
def vertex(v):return ''.join(map(str,v))
def make_graph():
    vertices=[vertex(v) for v in product((0,1),repeat=3)]
    edges=[]
    for v in product((0,1),repeat=3):
        for axis in range(3):
            if v[axis]==0:
                w=list(v);w[axis]=1
                edges.append({'id':vertex(v)+':'+str(axis),'tail':vertex(v),'head':vertex(w),'axis':axis})
    lookup={(e['tail'],e['head']):(e['id'],1) for e in edges}
    lookup.update({(e['head'],e['tail']):(e['id'],-1) for e in edges})
    faces=[]
    for normal in range(3):
        tangents=[i for i in range(3) if i!=normal]
        for side in (0,1):
            v=[0,0,0];v[normal]=side
            a=v.copy();a[tangents[0]]=1
            b=a.copy();b[tangents[1]]=1
            c=v.copy();c[tangents[1]]=1
            loop=list(map(vertex,(v,a,b,c)))
            cross_sign=1 if normal in (0,2) else -1
            if cross_sign!=(1 if side else -1):loop=[loop[0],*loop[:0:-1]]
            word=[{'edge':lookup[(loop[i],loop[(i+1)%4])][0],'sign':lookup[(loop[i],loop[(i+1)%4])][1]} for i in range(4)]
            faces.append({'id':str(normal)+':'+str(side),'vertices':loop,'word':word})
    return {'schema':'ym15-oriented-cube-v1','vertices':vertices,'edges':edges,'faces':faces,
            'group':'SU(2)','measure':'independent normalized Haar on12 oriented links',
            'action':'sum_f k_f * Tr(U_face_f)/2','geometry':'closed oriented boundary of one cube; sphere topology'}

def validate_graph(g):
    _unchanged()
    if type(g) is not dict or g!=make_graph():
        raise ValueError('graph must exactly match reviewed oriented cube contract')
    # Exact contract equality alone allows bool/int equality: check semantic types.
    for e in g['edges']:
        if type(e['axis']) is not int:raise ValueError('axis must be integer')
    for f in g['faces']:
        if len(set(f['vertices']))!=4:raise ValueError('face repeats vertex')
        for x in f['word']:
            if type(x['sign']) is not int or x['sign'] not in (-1,1):raise ValueError('invalid traversal sign')
    incident={e['id']:[] for e in g['edges']}
    edge_map={e['id']:e for e in g['edges']}
    for f in g['faces']:
        for i,x in enumerate(f['word']):
            e=edge_map[x['edge']];tail,head=(e['tail'],e['head']) if x['sign']==1 else (e['head'],e['tail'])
            if (tail,head)!=(f['vertices'][i],f['vertices'][(i+1)%4]):raise ValueError('boundary word endpoint mismatch')
            incident[x['edge']].append(x['sign'])
    if any(sorted(v)!=[-1,1] for v in incident.values()):raise ValueError('not a closed oriented surface')
    if len(g['vertices'])-len(g['edges'])+len(g['faces'])!=2:raise ValueError('Euler characteristic mismatch')
    return True

def char_power(n):
    if type(n) is not int or not 0<=n<=32:raise ValueError('power must be integer0..32')
    coeff={0:1}
    for _ in range(n):
        nxt={}
        for r,c in coeff.items():
            nxt[r+1]=nxt.get(r+1,0)+c
            if r:nxt[r-1]=nxt.get(r-1,0)+c
        coeff=nxt
    return coeff

def moment(degrees,normalized=True):
    _unchanged()
    if type(degrees) not in (tuple,list) or len(degrees)!=6 or type(normalized) is not bool:
        raise ValueError('six face degrees and Boolean normalization required')
    coeffs=[char_power(n) for n in degrees]
    common=set.intersection(*(set(c) for c in coeffs))
    result=sum((F(math.prod(c[r] for c in coeffs),(r+1)**4) for r in common),F(0))
    return result/F(2**sum(degrees)) if normalized else result

def subset_index_moment(selected):
    """Fundamental U/U* index gluing, independent of character coefficients."""
    if type(selected) not in (list,tuple) or any(type(i) is not int or not 0<=i<6 for i in selected) or len(set(selected))!=len(selected):
        raise ValueError('distinct integer face indices required')
    g=make_graph();occ={e['id']:[] for e in g['edges']}
    parent={}
    for fno in selected:
        f=g['faces'][fno]
        for i,x in enumerate(f['word']):
            a=(fno,i);b=(fno,(i+1)%4);parent[a]=a;parent[b]=b
            occ[x['edge']].append((x['sign'],a,b))
    def find(x):
        while parent[x]!=x:x=parent[x]
        return x
    def union(a,b):parent[find(a)]=find(b)
    used=0
    for values in occ.values():
        if len(values)==1:return F(0)
        if not values:continue
        if len(values)!=2 or values[0][0]+values[1][0]!=0:raise ValueError('not opposite fundamental traversals')
        (_,a,b),(_,c,d)=values
        union(a,d);union(b,c);used+=1
    loops=len({find(x) for x in parent})
    return F(2**loops,2**(used+len(selected)))

def quaternion_matrix(q):
    a,b,c,d=q
    return np.array([[a+1j*b,c+1j*d],[-c+1j*d,a-1j*b]],dtype=complex)
def qmul(p,q):
    # Independent explicit component multiplication for this matrix convention.
    a,b,c,d=p;w,x,y,z=q
    return np.array([a*w-b*x-c*y-d*z,a*x+b*w+c*z-d*y,
                     a*y+c*w+d*x-b*z,a*z+d*w+b*y-c*x])
def qdag(q):return np.array([q[0],-q[1],-q[2],-q[3]])
def matrix_loop(word,links):
    u=np.eye(2,dtype=complex)
    for item in word:
        link=links[item['edge']];u=u@(link if item['sign']==1 else link.conj().T)
    return u
def quaternion_loop(word,links):
    u=np.array([1.,0.,0.,0.])
    for item in word:
        link=links[item['edge']];u=qmul(u,link if item['sign']==1 else qdag(link))
    return u

def graph_hash():
    return hashlib.sha256(json.dumps(make_graph(),sort_keys=True,separators=(',',':')).encode()).hexdigest()
