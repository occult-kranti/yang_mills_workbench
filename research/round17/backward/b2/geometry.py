"""Graph construction and strict validation from the frozen independent B1 implementation."""
from fractions import Fraction as F
from itertools import product,combinations
from math import isqrt
from pathlib import Path
from collections import deque
import argparse,copy,hashlib,json


def exact(v):
    if type(v) not in (str,int,F):raise ValueError('exact rational required')
    try:return F(v)
    except (ValueError,ZeroDivisionError) as e:raise ValueError('finite rational required') from e


def graph():
    vertices=list(product(range(3),range(2),range(2)));edges=[];lookup={}
    for v in vertices:
        for axis,limit in enumerate((3,2,2)):
            if v[axis]+1>=limit:continue
            w=list(v);w[axis]+=1;w=tuple(w);eid=len(edges);edges.append({'id':eid,'tail':list(v),'head':list(w)})
            lookup[(v,w)]=(eid,1);lookup[(w,v)]=(eid,-1)
    faces=[]
    for v in vertices:
        for a,b in combinations(range(3),2):
            va=list(v);va[a]+=1;vb=list(v);vb[b]+=1;vab=va.copy();vab[b]+=1;loop=[v,tuple(va),tuple(vab),tuple(vb)]
            if not set(loop)<=set(vertices):continue
            faces.append({'id':len(faces),'axes':[a,b],'base':list(v),'vertices':list(map(list,loop)),
              'word':[list(lookup[(loop[i],loop[(i+1)%4])]) for i in range(4)]})
    return {'schema':'ym17-independent-dense-two-cube-v1','vertices':list(map(list,vertices)),'edges':edges,'faces':faces}


def geometry(g):
    if type(g) is not dict or g.get('schema')!='ym17-independent-dense-two-cube-v1':raise ValueError('fixed graph schema')
    vertices=g['vertices']
    if any(type(v) is not list or len(v)!=3 or any(type(x) is not int for x in v) for v in vertices):raise ValueError('strict vertex coordinates')
    if len(vertices)!=12 or set(map(tuple,vertices))!=set(product(range(3),range(2),range(2))):raise ValueError('actual twelve-vertex box required')
    edges={};inc={};adj={tuple(v):set() for v in vertices}
    for e in g['edges']:
        if type(e['id']) is not int or e['id'] in edges:raise ValueError('unique integer edge required')
        if any(type(v) is not list or len(v)!=3 or any(type(x) is not int for x in v) for v in (e['tail'],e['head'])):raise ValueError('strict edge coordinates')
        a,b=tuple(e['tail']),tuple(e['head'])
        if a not in adj or b not in adj or tuple(y-x for x,y in zip(a,b)) not in ((1,0,0),(0,1,0),(0,0,1)):raise ValueError('invalid coordinate link')
        if (a,b) in edges.values():raise ValueError('duplicate link')
        edges[e['id']]=(a,b);inc[e['id']]=[];adj[a].add(b);adj[b].add(a)
    if len(edges)!=20:raise ValueError('twenty links required')
    if len(g['faces'])!=11:raise ValueError('eleven distinct faces required')
    face_sets=set()
    for i,f in enumerate(g['faces']):
        if type(f['id']) is not int or f['id']!=i:raise ValueError('ordered face ids required')
        if any(type(v) is not list or len(v)!=3 or any(type(x) is not int for x in v) for v in f['vertices']):raise ValueError('strict face coordinates')
        vs=list(map(tuple,f['vertices']));fs=frozenset(vs)
        if len(vs)!=4 or len(fs)!=4 or fs in face_sets:raise ValueError('distinct simple squares required')
        face_sets.add(fs)
        spans=[max(v[a] for v in vs)-min(v[a] for v in vs) for a in range(3)]
        if sorted(spans)!=[0,1,1]:raise ValueError('coordinate unit square required')
        if type(f['axes']) is not list or any(type(v) is not int for v in f['axes']) or f['axes']!=[a for a in range(3) if spans[a]]:raise ValueError('strict geometric axes required')
        if type(f['base']) is not list or any(type(v) is not int for v in f['base']) or f['base']!=[min(v[a] for v in vs) for a in range(3)]:raise ValueError('strict geometric face base required')
        if len(f['word'])!=4:raise ValueError('four signed terms required')
        for j,(eid,sign) in enumerate(f['word']):
            if type(eid) is not int or eid not in edges or type(sign) is not int or sign not in (-1,1):raise ValueError('strict signed edge')
            ends=edges[eid] if sign==1 else edges[eid][::-1]
            if ends!=(vs[j],vs[(j+1)%4]):raise ValueError('incorrect dagger or path')
            inc[eid].append(i)
    # Shortest path between each edge's endpoints after deleting that edge.
    girth=100
    for a,b in edges.values():
        queue=deque([(a,0)]);seen={a}
        while queue:
            v,d=queue.popleft()
            if v==b:girth=min(girth,d+1);break
            for w in adj[v]:
                if {v,w}=={a,b} or w in seen:continue
                seen.add(w);queue.append((w,d+1))
    return inc,girth

