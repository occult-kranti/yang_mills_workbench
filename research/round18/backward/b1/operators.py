"""Independent complete low-support and Haar cross-block construction."""
from collections import Counter
from fractions import Fraction as F
from itertools import product,combinations,combinations_with_replacement


def rational(x):
    if type(x) not in (str,int,F):raise ValueError('exact rational required')
    return F(x)


def strict(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict(a[k],b[k]) for k in a)
    if type(a) in (tuple,list):return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b


def graph():
    dims=(3,2,2);vertices=list(product(*(range(n) for n in dims)));edges=[]
    for v in vertices:
        for axis in range(3):
            if v[axis]+1<dims[axis]:
                w=list(v);w[axis]+=1;edges.append({'id':len(edges),'axis':axis,'tail':list(v),'head':w})
    lookup={}
    for e in edges:lookup[tuple(e['tail']),tuple(e['head'])]=(e['id'],1);lookup[tuple(e['head']),tuple(e['tail'])]=(e['id'],-1)
    faces=[]
    for normal in range(3):
        a,b=[i for i in range(3) if i!=normal]
        for v in vertices:
            if v[a]+1>=dims[a] or v[b]+1>=dims[b]:continue
            va=list(v);va[a]+=1;vab=va.copy();vab[b]+=1;vb=list(v);vb[b]+=1;loop=[v,tuple(va),tuple(vab),tuple(vb)]
            faces.append({'id':len(faces),'normal':normal,'anchor':list(v),'vertices':[list(w) for w in loop],
                          'word':[list(lookup[loop[i],loop[(i+1)%4]]) for i in range(4)]})
    return {'schema':'ym18-independent-two-cube-graph-v1','vertices':[list(v) for v in vertices],'edges':edges,'faces':faces}


def validate(g):
    if not strict(g,graph()):raise ValueError('actual signed two-cube graph mismatch')
    return True


def supports(g):return [frozenset(e for e,s in f['word']) for f in g['faces']]


def support_inventory(g):
    validate(g);ends={e['id']:(tuple(e['tail']),tuple(e['head'])) for e in g['edges']};records=[];retained=[]
    for size in range(6):
        for ids in combinations(range(20),size):
            degrees=Counter(v for e in ids for v in ends[e]);mindeg=min(degrees.values(),default=0);admissible=(size==0 or mindeg>=2)
            row={'mask':format(sum(1<<e for e in ids),'05x'),'size':size,'active_vertices':len(degrees),'minimum_active_degree':mindeg,'passes_Gauss_necessary_degree':admissible}
            records.append(row)
            if admissible:retained.append(list(ids))
    return records,retained


def cycles_of_length(g,length):
    if type(length) is not int or not 3<=length<=6:raise ValueError('bounded exact cycle length required')
    validate(g);adj={tuple(v):[] for v in g['vertices']}
    for e in g['edges']:
        a,b=tuple(e['tail']),tuple(e['head']);adj[a].append((b,e['id']));adj[b].append((a,e['id']))
    found=set()
    for origin in sorted(adj):
        def walk(path,ids):
            if len(path)==length:
                for nxt,e in adj[path[-1]]:
                    if nxt==origin:found.add(tuple(sorted((*ids,e))))
                return
            for nxt,e in adj[path[-1]]:
                if nxt not in path and nxt>=origin:walk((*path,nxt),(*ids,e))
        walk((origin,),())
    return sorted(found)


def six_loop(g):
    validate(g);v=[(0,0,0),(1,0,0),(2,0,0),(2,1,0),(1,1,0),(0,1,0)];lookup={}
    for e in g['edges']:
        a,b=tuple(e['tail']),tuple(e['head']);lookup[a,b]=(e['id'],1);lookup[b,a]=(e['id'],-1)
    word=[lookup[v[i],v[(i+1)%6]] for i in range(6)];active={e for e,s in word};orthogonal=[]
    for f,s in zip(g['faces'],supports(g)):
        difference=sorted(active^s)
        if not difference:raise ValueError('six loop was silently included in P')
        orthogonal.append({'face':f['id'],'odd_edge_witness':difference[0]})
    return {'vertices':[list(x) for x in v],'word':[list(x) for x in word],'active_edges':sorted(active),'norm_squared':'1',
      'electric_energy_over_alpha':'9/2','vacuum_odd_edge_witness':min(active),'face_orthogonality_witnesses':orthogonal,
      'scope':'Actual closed fundamental six-edge loop in the full physical Q space; no higher tail threshold is valid for this P.'}


def moment(g,indices):
    validate(g)
    if type(indices) not in (list,tuple) or len(indices)>4 or any(type(i) is not int or not 0<=i<11 for i in indices):raise ValueError('up to four exact face indices required')
    if not indices:return F(1)
    s=supports(g);odd=set()
    for i in indices:odd.symmetric_difference_update(s[i])
    if odd:return F(0)
    multiplicities=sorted(Counter(indices).values())
    if multiplicities==[2]:return F(1)
    if multiplicities==[4]:return F(2)
    if multiplicities==[2,2]:
        a,b=sorted(set(indices))
        if not s[a]-s[b]:raise ValueError('exclusive conditional Haar integration unavailable')
        return F(1)
    raise ValueError('unexpected closed low-degree channel requires a new Haar derivation')


def cube_boundary_contraction(g):
    """Actual signed fundamental matrix indices, using only U/conjugate-U Haar pairs."""
    validate(g);chosen=[f for f in g['faces'] if all(v[0]<=1 for v in f['vertices'])]
    if len(chosen)!=6:raise ValueError('left cube boundary not identified')
    parent=list(range(24));occurrences={};words=[]
    def find(i):
        while parent[i]!=i:i=parent[i]
        return i
    def join(i,j):parent[find(i)]=find(j)
    for j,f in enumerate(chosen):
        outward=1 if f['anchor'][f['normal']]==1 else -1
        orientation=(-1)**f['normal'];word=[tuple(x) for x in f['word']]
        if outward!=orientation:word=[(e,-s) for e,s in reversed(word)]
        words.append({'face':f['id'],'word':[list(x) for x in word]})
        for k,(e,s) in enumerate(word):occurrences.setdefault(e,[]).append((s,4*j+k,4*j+(k+1)%4))
    pairs=[]
    for e,rows in sorted(occurrences.items()):
        if len(rows)!=2 or sorted(r[0] for r in rows)!=[-1,1]:raise ValueError('oriented edge must have one U and one conjugate-U')
        plus=next(r for r in rows if r[0]==1);minus=next(r for r in rows if r[0]==-1)
        join(plus[1],minus[2]);join(plus[2],minus[1]);pairs.append({'edge':e,'delta_pairs':[[plus[1],minus[2]],[plus[2],minus[1]]],'Haar_factor':'1/2'})
    components=sorted([sorted(i for i in range(24) if find(i)==root) for root in {find(i) for i in range(24)}])
    value=F(2**len(components),2**len(pairs))
    return {'faces':[f['id'] for f in chosen],'outward_words':words,'edge_pairings':pairs,'index_components':components,
            'ordinary_character_moment':str(value),'independent_centered_face_value':'0',
            'scope':'Fresh actual six-face contraction, separate from the degree-four cross Gram.'}


def fourth_inventory(g):
    validate(g);rows=[]
    for idx in combinations_with_replacement(range(11),4):
        odd=set()
        for i in idx:odd.symmetric_difference_update(supports(g)[i])
        typ=sorted(Counter(idx).values());witness=None
        if typ==[2,2]:a,b=sorted(set(idx));witness=min(supports(g)[a]-supports(g)[b])
        rows.append({'faces':list(idx),'multiplicity_type':typ,'value':str(moment(g,idx)),
          'odd_edge_witness':min(odd) if odd else None,'exclusive_square_edge':witness})
    return rows


def matrix_strings(a):return [[str(x) for x in row] for row in a]


def matrices(g,alpha,couplings):
    validate(g);alpha=rational(alpha)
    if alpha<=0:raise ValueError('positive physical scale required')
    if type(couplings) not in (list,tuple) or len(couplings)!=11:raise ValueError('eleven actual face couplings required')
    lam=[rational(x) for x in couplings];basis=[(),*((i,) for i in range(11))]
    moments={idx:moment(g,idx) for degree in range(5) for idx in combinations_with_replacement(range(11),degree)}
    get=lambda idx:moments[tuple(sorted(idx))]
    gram=[[get((*p,*q)) for q in basis] for p in basis]
    if gram!=[[F(i==j) for j in range(12)] for i in range(12)]:raise ValueError('ordinary matrix P subtraction requires the complete orthonormal basis')
    V=[[sum((-lam[f]*get((*p,*q,f))/2 for f in range(11)),F(0)) for q in basis] for p in basis]
    V2=[[sum((lam[f]*lam[h]*get((*p,*q,f,h))/4 for f in range(11) for h in range(11)),F(0)) for q in basis] for p in basis]
    sub=[[sum((V[i][k]*V[k][j] for k in range(12)),F(0)) for j in range(12)] for i in range(12)]
    cross=[[V2[i][j]-sub[i][j] for j in range(12)] for i in range(12)]
    total=sum((x*x for x in lam),F(0));L=sum(map(abs,lam),F(0));rho=max(map(abs,lam))/alpha
    expected=[[F(0) for _ in range(12)] for _ in range(12)]
    for i in range(11):
        for j in range(11):expected[i+1][j+1]=total/4 if i==j else lam[i]*lam[j]/4
    if cross!=expected:raise ValueError('full P subtraction disagrees with independently reduced cross formula')
    rowbound=max(sum(map(abs,row),F(0)) for row in cross)
    homogeneous=all(abs(x)==abs(lam[0]) for x in lam)
    return {'alpha':str(alpha),'couplings':list(map(str,lam)),'P_dimension':12,'Gram':matrix_strings(gram),'PVP':matrix_strings(V),
      'PV2P':matrix_strings(V2),'PVP_squared':matrix_strings(sub),'cross_Gram':matrix_strings(cross),
      'full_electric_complement_lower':str(9*alpha/2),'QHQ_lower':str(9*alpha/2-L),
      'sum_absolute_couplings':str(L),'sum_squared_couplings':str(total),'rho_max':str(rho),'cross_row_sum_bound':str(rowbound),
      'box_cross_norm_squared_upper':str(21*(alpha*rho)**2/4),
      'homogeneous_magnitude_cross_norm_squared':str(21*lam[0]**2/4) if homogeneous else None,
      'scope':'Full finite-graph physical Q complement and exact bounded QVP norm information; scalar B2 gap estimate unexecuted.'}
