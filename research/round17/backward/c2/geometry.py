"""Independent signed four-cube complex and realizable conditional boundary."""
from itertools import product,combinations
from fractions import Fraction as F


def strict(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict(a[k],b[k]) for k in a)
    if type(a) in (list,tuple):return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b


def graph():
    vertices=list(product(range(3),range(3),range(2)));edges=[];lookup={}
    for v in vertices:
        for axis,limit in enumerate((3,3,2)):
            if v[axis]+1>=limit:continue
            w=list(v);w[axis]+=1;w=tuple(w);eid=len(edges)
            edges.append({'id':eid,'tail':list(v),'head':list(w)})
            lookup[(v,w)]=(eid,1);lookup[(w,v)]=(eid,-1)
    faces=[]
    for v in vertices:
        for a,b in combinations(range(3),2):
            va=list(v);va[a]+=1;vb=list(v);vb[b]+=1;vab=va.copy();vab[b]+=1;loop=[v,tuple(va),tuple(vab),tuple(vb)]
            if not set(loop)<=set(vertices):continue
            faces.append({'id':len(faces),'vertices':list(map(list,loop)),
              'word':[list(lookup[(loop[i],loop[(i+1)%4])]) for i in range(4)]})
    return {'schema':'ym17-independent-four-cube-v1','vertices':list(map(list,vertices)),'edges':edges,'faces':faces}


def validate(g):
    if type(g) is not dict or g.get('schema')!='ym17-independent-four-cube-v1':raise ValueError('four-cube schema required')
    def coordinate(v):
        if type(v) is not list or len(v)!=3 or any(type(t) is not int for t in v):raise ValueError('strict integer coordinates required')
        return tuple(v)
    vs=[coordinate(v) for v in g['vertices']]
    if len(vs)!=18 or set(vs)!=set(product(range(3),range(3),range(2))):raise ValueError('actual eighteen vertices required')
    edges={};inc={}
    for e in g['edges']:
        if type(e['id']) is not int or e['id'] in edges:raise ValueError('unique integer edge')
        a,b=coordinate(e['tail']),coordinate(e['head'])
        if a not in vs or b not in vs or tuple(y-x for x,y in zip(a,b)) not in ((1,0,0),(0,1,0),(0,0,1)) or (a,b) in edges.values():raise ValueError('distinct positive-axis unit edge required')
        edges[e['id']]=(a,b);inc[e['id']]=[]
    if len(edges)!=33:raise ValueError('thirty-three edges required')
    face_sets={}
    for i,f in enumerate(g['faces']):
        if type(f['id']) is not int or f['id']!=i:raise ValueError('ordered integer face ids')
        fv=[coordinate(v) for v in f['vertices']];key=frozenset(fv)
        if len(fv)!=4 or len(key)!=4 or key in face_sets:raise ValueError('unique four-vertex face')
        span=[max(v[a] for v in fv)-min(v[a] for v in fv) for a in range(3)]
        if sorted(span)!=[0,1,1] or len(f['word'])!=4:raise ValueError('unit coordinate square required')
        for j,term in enumerate(f['word']):
            if type(term) is not list or len(term)!=2:raise ValueError('signed edge pair required')
            eid,sign=term
            if type(eid) is not int or eid not in edges or type(sign) is not int or sign not in (-1,1):raise ValueError('strict signed edge required')
            ends=edges[eid] if sign==1 else edges[eid][::-1]
            if ends!=(fv[j],fv[(j+1)%4]):raise ValueError('wrong dagger or nonclosed path')
            inc[eid].append(i)
        face_sets[key]=i
    if len(face_sets)!=20:raise ValueError('twenty distinct faces required')
    cells=[];occupancy=[0]*20
    for bx,by in product(range(2),repeat=2):
        cell=[]
        for axis in range(3):
            others=[a for a in range(3) if a!=axis]
            for side in (0,1):
                corners=[]
                for u,v in product((0,1),repeat=2):
                    c=[bx,by,0];c[axis]+=side;c[others[0]]+=u;c[others[1]]+=v;corners.append(tuple(c))
                key=frozenset(corners)
                if key not in face_sets:raise ValueError('missing geometric cell face')
                fi=face_sets[key];cell.append(fi);occupancy[fi]+=1
        cells.append(cell)
    central=[eid for eid,(a,b) in edges.items() if a==(1,1,0) and b==(1,1,1)]
    if len(central)!=1:raise ValueError('one actual central vertical link required')
    central=central[0];outer=[i for i,n in enumerate(occupancy) if n==1];internal=[i for i,n in enumerate(occupancy) if n==2]
    oe={eid for i in outer for eid,_ in g['faces'][i]['word']};ov={v for eid in oe for v in edges[eid]}
    if sorted(occupancy)!=[1]*16+[2]*4 or sorted(inc[central])!=internal:raise ValueError('actual four-face central incidence required')
    return {'edges':edges,'incidence':inc,'cells':cells,'occupancy':occupancy,'central':central,'internal_faces':internal,'outer_faces':outer,'outer_edges':sorted(oe),'outer_vertices':sorted(ov)}


def qmul(a,b):
    w,x,y,z=a;v,p,q,r=b
    return (w*v-x*p-y*q-z*r,w*p+x*v+y*r-z*q,w*q-x*r+y*v+z*p,w*r+x*q-y*p+z*v)


def inverse(q):return (q[0],-q[1],-q[2],-q[3])


IDENTITY=(F(1),F(0),F(0),F(0))
TETRA=tuple(tuple(F(x,2) for x in q) for q in ((1,1,1,1),(1,1,-1,-1),(1,-1,1,-1),(1,-1,-1,1)))


def boundary(g,holonomies=TETRA):
    data=validate(g);central=data['central']
    if type(holonomies) not in (tuple,list) or len(holonomies)!=4:raise ValueError('four unit quaternions required')
    for q in holonomies:
        if len(q)!=4 or any(type(t) not in (int,F) for t in q) or sum(t*t for t in q)!=1:raise ValueError('exact unit quaternion required')
    links={eid:IDENTITY for eid in data['edges']};paths=[];chosen=[];used=set()
    for fi,H in zip(data['internal_faces'],holonomies):
        word=[list(t) for t in g['faces'][fi]['word']]
        position=next(j for j,t in enumerate(word) if t[0]==central)
        if word[position][1]==-1:word=[[eid,-sign] for eid,sign in reversed(word)]
        position=next(j for j,t in enumerate(word) if t[0]==central);word=word[position:]+word[:position]
        if word[0]!=[central,1]:raise ValueError('whole-face reorientation failed')
        surrounding={eid for eid,_ in word[1:]}
        if len(surrounding)!=3 or used&surrounding:raise ValueError('outer paths must be edge-disjoint')
        used|=surrounding
        vertical=[(eid,sign) for eid,sign in word[1:] if data['edges'][eid][0][2]!=data['edges'][eid][1][2]]
        if len(vertical)!=1:raise ValueError('unique outside vertical edge required')
        eid,sign=vertical[0];links[eid]=H if sign==1 else inverse(H);chosen.append(eid);paths.append({'face':fi,'word':word,'assigned_edge':eid})
    return links,paths,chosen


def word_holonomy(word,links):
    value=IDENTITY
    for eid,sign in word:value=qmul(value,links[eid] if sign==1 else inverse(links[eid]))
    return value
