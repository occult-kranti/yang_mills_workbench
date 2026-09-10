"""Independent exact trace-index Haar contractions on the actual two-cube graph.

The fourth-order oracle does not use a character-fusion or disk formula.
"""
from fractions import Fraction as Q
from collections import defaultdict
from itertools import product
from math import comb


def require(condition, message):
    if not condition:
        raise ValueError(message)


def coordinates(label):
    require(type(label) is str, 'vertex label is a string')
    parts=label.split(',')
    require(len(parts)==3, 'three coordinates required')
    return tuple(map(int,parts))


def graph_data(graph):
    require(type(graph) is dict, 'graph object required')
    require(graph['schema']=='ym16-adjacent-two-cubes-v1','schema mismatch')
    verts=graph['vertices']; require(type(verts) is list and len(verts)==12,'twelve vertices required')
    expected=set(product(range(3),range(2),range(2)))
    require({coordinates(v) for v in verts}==expected,'wrong vertices')
    edges={}; edge_sets=set()
    require(len(graph['edges'])==20,'twenty edges required')
    for e in graph['edges']:
        require(e['id'] not in edges,'repeated edge')
        tail,head=coordinates(e['tail']),coordinates(e['head'])
        delta=tuple(b-a for a,b in zip(tail,head))
        require(tail in expected and head in expected,'edge endpoint absent')
        require(delta in [(1,0,0),(0,1,0),(0,0,1)],'positive coordinate edge required')
        require(type(e['axis']) is int and e['axis']==delta.index(1),'wrong edge axis')
        endpoints=frozenset((tail,head));require(endpoints not in edge_sets,'duplicate geometric edge')
        edge_sets.add(endpoints);edges[e['id']]=(e['tail'],e['head'])
    expected_edges={frozenset((a,b)) for a in expected for b in expected if sum(abs(x-y) for x,y in zip(a,b))==1}
    require(edge_sets==expected_edges,'incomplete edge graph')
    require(len(graph['faces'])==11,'eleven faces required')
    words={};regions={};face_sets=set();inc=defaultdict(list)
    for face in graph['faces']:
        key=face['id'];require(key not in words,'repeated face id')
        vs=face['vertices']; require(len(vs)==4 and len(set(vs))==4,'simple square required')
        points=[coordinates(v) for v in vs]; fs=frozenset(points)
        require(fs not in face_sets,'duplicate geometric face');face_sets.add(fs)
        ranges=[max(p[d] for p in points)-min(p[d] for p in points) for d in range(3)]
        require(sorted(ranges)==[0,1,1],'unit coordinate square required')
        normal=ranges.index(0);base=tuple(min(p[d] for p in points) for d in range(3))
        require(type(face['normal']) is int and face['normal']==normal,'face normal mismatch')
        require(type(face['base']) is list and all(type(v) is int for v in face['base']) and tuple(face['base'])==base,'face base mismatch')
        region='shared' if normal==0 and base[0]==1 else 'left' if base[0]==0 else 'right'
        require(face['region']==region,'wrong geometric region');regions[key]=region
        word=face['word']; require(len(word)==4,'four oriented terms required')
        parsed=[]
        for i,term in enumerate(word):
            eid,sign=term['edge'],term['sign']
            require(type(sign) is int and sign in (-1,1),'strict dagger sign required')
            require(eid in edges,'unknown edge');a,b=edges[eid]
            oriented=(a,b) if sign==1 else (b,a)
            require(oriented==(vs[i],vs[(i+1)%4]),'word does not follow face boundary')
            parsed.append((eid,sign));inc[eid].append((key,sign))
        words[key]=parsed
    # Independently enumerate every elementary square from the vertex graph.
    expected_faces=set()
    for p in expected:
        for a,b in ((0,1),(0,2),(1,2)):
            q=list(p);q[a]+=1;r=list(p);r[b]+=1;s=list(q);s[b]+=1
            if tuple(q) in expected and tuple(r) in expected and tuple(s) in expected:
                expected_faces.add(frozenset((p,tuple(q),tuple(r),tuple(s))))
    require(face_sets==expected_faces,'face geometry incomplete')
    shared=[f for f in words if regions[f]=='shared'];require(len(shared)==1,'unique shared face required')
    shared=shared[0];left={f for f in words if regions[f]=='left'};right={f for f in words if regions[f]=='right'}
    require(len(left)==len(right)==5,'five-face disks required')
    require(graph['shared_face']==shared,'shared metadata mismatch')
    for key,target in [('left_disk',left),('right_disk',right),('outer_faces',left|right)]:
        require(type(graph[key]) is list and len(graph[key])==len(target) and set(graph[key])==target,'disk metadata mismatch')
    shared_edges={e for e,_ in words[shared]}
    require(set(inc)==set(edges),'unused graph edge')
    require({e for e,v in inc.items() if len(v)==3}==shared_edges,'trivalent incidence mismatch')
    require(all(len(v)==(3 if e in shared_edges else 2) for e,v in inc.items()),'incidence count mismatch')
    require(all(sorted(s for f,s in terms if f!=shared)==[-1,1] for terms in inc.values()),'outer orientations mismatch')
    cells=graph['cells'];require(type(cells) is list and len(cells)==2,'two cells required')
    for cell,region,ids,orientation in zip(cells,('left','right'),(left,right),(1,-1)):
        require(cell['id']==region and len(cell['faces'])==6 and set(cell['faces'])==ids|{shared},'cell metadata mismatch')
        require(type(cell['shared_orientation']) is int and cell['shared_orientation']==orientation,'shared orientation metadata')
    require(graph['group']=='SU(2)','wrong group')
    require(graph['measure']=='independent normalized Haar on20 oriented links','wrong Haar measure')
    require(graph['full_action']=='sum over11 distinct face coefficients k_f*Tr(U_face_f)/2; internal face counted once','changed full action')
    require(graph['outer_action']=='sum over10 outer face coefficients only; shared coefficient0','changed outer action')
    require(graph['time_generator']=='none; finite Euclidean measure','unsupported time generator')
    require(graph['energy_scale']=='no Hamiltonian energy scale is defined by these Euclidean couplings','unsupported energy scale')
    return {'edges':edges,'words':words,'incidence':dict(inc),'left':left,'right':right,'shared':shared}


def boundary_rank_and_kernel(data):
    faces=list(data['words']); rows=[]
    for terms in data['incidence'].values():
        rows.append(sum(1<<faces.index(f) for f,_ in terms))
    # Column-oriented elimination, independent of producer row-pivot helper.
    columns=[]
    for j in range(len(faces)):
        columns.append(sum(((r>>j)&1)<<i for i,r in enumerate(rows)))
    basis={}
    for col in columns:
        for pivot in sorted(basis,reverse=True):
            if (col>>pivot)&1:col^=basis[pivot]
        if col:basis[col.bit_length()-1]=col
    kernel=[mask for mask in range(1<<len(faces)) if all((mask&r).bit_count()%2==0 for r in rows)]
    return len(basis),kernel,faces,rows


def orient_surface(words,selected):
    if not selected:return []
    incidence=defaultdict(list)
    for face in selected:
        for edge,sign in words[face]:incidence[edge].append((face,sign))
    if any(len(v)%2 for v in incidence.values()):return None
    require(all(len(v)==2 for v in incidence.values()),'only pairwise closed distinct-face surfaces supported')
    orientations={selected[0]:1}
    while len(orientations)<len(selected):
        changed=False
        for ((a,sa),(b,sb)) in incidence.values():
            if a in orientations and b not in orientations:orientations[b]=-sa*sb*orientations[a];changed=True
            if b in orientations and a not in orientations:orientations[a]=-sa*sb*orientations[b];changed=True
            if a in orientations and b in orientations:require(sa*orientations[a]==-sb*orientations[b],'nonorientable surface')
        if not changed and len(orientations)<len(selected):orientations[next(f for f in selected if f not in orientations)]=1
    return [words[f] if orientations[f]==1 else [(e,-s) for e,s in words[f][::-1]] for f in selected]


def raw_integral(trace_words,projector='correct'):
    """Matrix-index integration up to two U and two conjugate(U) per edge.

    Complete trace reversal supplies a balanced presentation for our SU2 fixtures.
    Each trace is normalized by 1/2. Four-Haar coefficients are inverse Gram.
    """
    if trace_words is None:return {'value':Q(0),'branches':0,'paired_edges':0,'fourth_edges':0}
    occurrences=defaultdict(list);count=sum(len(w) for w in trace_words);parent=list(range(count));offset=0
    for word in trace_words:
        for i,(edge,sign) in enumerate(word):
            require(type(sign) is int and sign in (-1,1),'strict sign required')
            a,b=offset+i,offset+(i+1)%len(word)
            occurrences[edge].append((sign,a,b) if sign==1 else (sign,b,a))
        offset+=len(word)
    def join(p,a,b):
        while p[a]!=a:a=p[a]
        while p[b]!=b:b=p[b]
        p[a]=b
    fourth=[];pairs=0
    for edge,terms in occurrences.items():
        plus=[(a,b) for s,a,b in terms if s==1];minus=[(a,b) for s,a,b in terms if s==-1]
        require(len(plus)==len(minus) and len(plus) in (1,2),'balanced order two or four Haar required')
        if len(plus)==1:
            join(parent,plus[0][0],minus[0][0]);join(parent,plus[0][1],minus[0][1]);pairs+=1
        else:fourth.append((plus,minus))
    # Inverse of Gram [[4,2],[2,4]].
    determinant=Q(4*4-2*2);diag=Q(4)/determinant;off=-Q(2)/determinant
    if projector=='drop_negative':off=Q(0)
    elif projector=='independent_pairs':diag=Q(1,4);off=Q(0)
    elif projector!='correct':raise ValueError('unknown projector')
    total=Q(0);positive=Q(0);negative=Q(0)
    for choices in product(range(4),repeat=len(fourth)):
        p=parent.copy();weight=Q(1)
        for (plus,minus),choice in zip(fourth,choices):
            row_swap,col_swap=divmod(choice,2);weight*=diag if row_swap==col_swap else off
            for i in (0,1):
                join(p,plus[i][0],minus[i^row_swap][0]);join(p,plus[i][1],minus[i^col_swap][1])
        roots=set()
        for i in range(count):
            while p[i]!=i:i=p[i]
            roots.add(i)
        term=weight*Q(2)**(len(roots)-pairs-len(trace_words));total+=term
        if term>0:positive+=term
        else:negative+=term
    return {'value':total,'branches':4**len(fourth),'paired_edges':pairs,'fourth_edges':len(fourth),'positive_sum':positive,'negative_sum':negative}


def character_polynomial(n):
    require(type(n) is int and n>=0,'nonnegative label required')
    # chi_n(t) with t=Tr U: chi_(n+1)=t chi_n-chi_(n-1).
    a,b=[1],[0,1]
    if n==0:return a
    for _ in range(1,n):
        nxt=[0]+b
        for i,c in enumerate(a):nxt[i]-=c
        a,b=b,nxt
    return b


def character_triple(n,m,k):
    poly=[1]
    for label in (n,m,k):
        factor=character_polynomial(label);out=[0]*(len(poly)+len(factor)-1)
        for i,a in enumerate(poly):
            for j,b in enumerate(factor):out[i+j]+=a*b
        poly=out
    # Exact semicircle/Haar moment of Tr U: Catalan number for even powers.
    return sum((Q(c*comb(2*(i//2),i//2),i//2+1) for i,c in enumerate(poly) if i%2==0),Q(0))
