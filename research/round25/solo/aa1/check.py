"""Exact finite geometry and spectral checks; one author, two enumeration methods."""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
from fractions import Fraction as F

def zeros(n): return [[F(0) for j in range(n)] for i in range(n)]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def mul(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def sub(a,b): return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,c): return [[x*c for x in r] for r in a]
def trace(a): return sum(a[i][i] for i in range(len(a)))
def quad(a,idx): return sum(a[i][j] for i in idx for j in idx)/2
def symmetric(a): return all(a[i][j]==a[j][i] for i in range(len(a)) for j in range(len(a)))


def require(ok, message):
    if not ok:
        raise ValueError(message)


def compute():
    vertices = list(it.product(range(2), repeat=3))
    edges = [(v, tuple(v[j] + (j == a) for j in range(3)))
             for v in vertices for a in range(3) if v[a] == 0]
    edges = sorted(edges)
    edge_index = {frozenset(e): i for i, e in enumerate(edges)}
    faces = []
    for a, b in it.combinations(range(3), 2):
        c = 3-a-b
        for side in range(2):
            face = frozenset(i for i, e in enumerate(edges)
                             if e[0][c] == e[1][c] == side)
            faces.append((a, b, c, side, face))
    cycles = []
    for subset in it.combinations(range(12), 6):
        deg = {v: 0 for v in vertices}
        for i in subset:
            for v in edges[i]: deg[v] += 1
        if sorted(deg.values()) != [0, 0, 2, 2, 2, 2, 2, 2]: continue
        seen = {next(v for v in vertices if deg[v])}
        while True:
            expanded = seen | {v for i in subset if seen.intersection(edges[i]) for v in edges[i]}
            if expanded == seen: break
            seen = expanded
        if len(seen) == 6: cycles.append(frozenset(subset))
    # Reverse construction starts from paths, rather than subsets of edges.
    graph = {v: [w for e in edges if v in e for w in e if w != v] for v in vertices}
    reverse = set()
    def walk(path):
        if len(path) == 6:
            if path[0] in graph[path[-1]]:
                reverse.add(frozenset(edge_index[frozenset((path[i],path[(i+1)%6]))] for i in range(6)))
            return
        for w in graph[path[-1]]:
            if w not in path: walk(path + [w])
    for v in vertices: walk([v])
    require(set(cycles) == reverse, 'enumerations differ')
    n=len(cycles); A=zeros(n); labels={}
    for i,c in enumerate(cycles):
        for j,d in enumerate(cycles):
            hit=[f for f in faces if c ^ d == f[-1]]
            require(len(hit)<=1, 'ambiguous face')
            if hit:
                f=hit[0]; shared=c & f[-1]
                shared_vertices=set.intersection(*(set(edges[e]) for e in shared))
                require(len(shared)==2 and len(shared_vertices)==1,'non-adjacent shared face edges')
                A[i][j]=F(1); labels[i,j]=f
    O=(0,0,0); D=(0,1,1)
    X=[O,(0,1,0),D]; Y=[O,(0,0,1),D]
    Z=[O,(1,0,0),(1,1,0),(1,1,1),D]
    def path_edges(p): return {edge_index[frozenset((a,b))] for a,b in zip(p,p[1:])}
    ux=cycles.index(frozenset(path_edges(X)|path_edges(Z)))
    uy=cycles.index(frozenset(path_edges(Y)|path_edges(Z)))
    idx=[ux,uy]; powers=[eye(n)]
    for k in range(1,7): powers.append(mul(powers[-1],A))
    moments=[quad(p,idx) for p in powers]
    exact_moments=[str(x) for x in moments]
    I=eye(n); A2=powers[2]
    # Projectors on squared eigenvalues 0,4,12 are exact rational matrices.
    P0=scale(mul(sub(A2,scale(I,4)),sub(A2,scale(I,12))),F(1,48))
    P4=scale(mul(A2,sub(A2,scale(I,12))),F(-1,32))
    P12=scale(mul(A2,sub(A2,scale(I,4))),F(1,96))
    for P in [P0,P4,P12]: require(mul(P,P)==P,'projector idempotence')
    require([trace(P) for P in [P0,P4,P12]]==[8,6,2],'spectral dimensions')
    require([quad(P,idx) for P in [P0,P4,P12]]==[F(1,3),F(1,2),F(1,6)],'even spectral weights')
    require(quad(mul(A,P4),idx)==F(1,2) and quad(mul(A,P12),idx)==F(1,2),'odd spectral weights')
    require(trace(mul(A,P4))==trace(mul(A,P12))==0,'paired multiplicities')
    measure=[{'eigenvalue':'0','multiplicity':8,'weight':'1/3'},
      {'eigenvalue':'2','multiplicity':3,'weight':'3/8'},
      {'eigenvalue':'-2','multiplicity':3,'weight':'1/8'},
      {'eigenvalue':'2*sqrt(3)','multiplicity':1,'weight':'1/12+1/(8*sqrt(3))'},
      {'eigenvalue':'-2*sqrt(3)','multiplicity':1,'weight':'1/12-1/(8*sqrt(3))'}]
    # All possible Casimir energy partitions below 18 quarter-units.
    energy_patterns=[(a,b,c) for a in range(7) for b in range(3) for c in range(2) if 3*a+8*b+15*c==18]
    require(energy_patterns==[(1,0,1),(6,0,0)],'Casimir partition changed')
    require(n==16 and symmetric(A),'cube matrix')
    require(mul(mul(A,sub(A2,scale(I,4))),sub(A2,scale(I,12)))==zeros(n),'minimal polynomial')
    require(moments[:5]==[1,1,4,8,32], 'actual U moments')
    degrees=[int(sum(A[i])) for i in range(n)]
    require(sorted(degrees)==[2]*12+[6]*4,'degree distribution')
    require(sum(A[ux][j]**2 for j in range(n) if j not in (ux,uy))>0,'two-state false closure must fail')
    return {
      'scope':'Full physical cube shell and its compression; surrounding-region closure not yet proved',
      'authors':'single agent; correlated serial constructions',
      'edges':edges,'cycles':[sorted(c) for c in cycles],
      'faces':[{'axes':[a,b],'normal':c,'side':s,'edges':sorted(f),'anchor_sum':4+s} for a,b,c,s,f in faces],
      'matrix_adjacency':[[int(A[i][j]) for j in range(n)] for i in range(n)],
      'compressed_potential':'-adjacency/96', 'u_indices':[ux,uy],
      'spectral_measure':measure,'moments':exact_moments,
      'casimir_quarter_unit_patterns':energy_patterns,
      'degree_distribution':degrees,
      'linear_disk_at_z_1e_6':'1/3528000000000000',
      'controls':{'subset_vs_path_enumeration':True,'exact_spectral_projectors':True,
        'two_state_closure_rejected':True,'all_flip_shared_edges_adjacent':True,
        'external_closure_not_assumed':True,'independent_authorship_claim_rejected':True}
    }


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    out=Path(a.output).resolve();require(not out.exists(),'output must be fresh');out.mkdir(parents=True)
    data=compute();(out/'results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':'passed','basis':len(data['cycles']),'moments':data['moments'],'output':str(out)}))
