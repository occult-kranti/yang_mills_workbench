"""Independent signed strip, universal quaternion identities and bridge bounds."""
from fractions import Fraction as F
from itertools import product


def exact(x):
    if type(x) not in (str,int,F):raise ValueError('exact rational required, not Boolean or float')
    try:return F(x)
    except (ValueError,ZeroDivisionError) as e:raise ValueError('finite rational required') from e


def graph():
    vertices=[(x,y,0) for x in range(4) for y in range(2)];edges=[];lookup={}
    for v in vertices:
        for axis,limit in ((0,4),(1,2)):
            if v[axis]+1>=limit:continue
            w=list(v);w[axis]+=1;w=tuple(w);eid=len(edges);edges.append({'id':eid,'tail':list(v),'head':list(w)})
            lookup[(v,w)]=(eid,1);lookup[(w,v)]=(eid,-1)
    faces=[]
    for x in range(3):
        vs=[(x,0,0),(x+1,0,0),(x+1,1,0),(x,1,0)]
        faces.append({'id':x,'vertices':list(map(list,vs)),'word':[list(lookup[(vs[j],vs[(j+1)%4])]) for j in range(4)]})
    return {'schema':'ym18-independent-three-face-strip-v1','vertices':list(map(list,vertices)),'edges':edges,'faces':faces}


def validate(g):
    if type(g) is not dict or g.get('schema')!='ym18-independent-three-face-strip-v1':raise ValueError('strip schema required')
    def coordinate(v):
        if type(v) is not list or len(v)!=3 or any(type(t) is not int for t in v):raise ValueError('strict integer coordinate triple required')
        return tuple(v)
    vertices=[coordinate(v) for v in g['vertices']]
    if len(vertices)!=8 or set(vertices)!={(x,y,0) for x in range(4) for y in range(2)}:raise ValueError('actual eight vertices required')
    edges={};inc={}
    for e in g['edges']:
        eid=e['id'];a,b=coordinate(e['tail']),coordinate(e['head'])
        if type(eid) is not int or eid in edges or (a,b) in edges.values() or a not in vertices or b not in vertices or tuple(y-x for x,y in zip(a,b)) not in ((1,0,0),(0,1,0)):raise ValueError('unique positive-axis strip edge required')
        edges[eid]=(a,b);inc[eid]=[]
    if len(edges)!=10:raise ValueError('all ten electric links required')
    faces={};position={}
    for i,f in enumerate(g['faces']):
        if type(f['id']) is not int or f['id']!=i:raise ValueError('ordered strict face id required')
        vs=[coordinate(v) for v in f['vertices']]
        if len(vs)!=4 or len(set(vs))!=4 or len(f['word'])!=4:raise ValueError('four distinct square vertices and edges required')
        x=min(v[0] for v in vs)
        if set(vs)!={(x,0,0),(x+1,0,0),(x+1,1,0),(x,1,0)} or x in position or not 0<=x<=2:raise ValueError('three actual distinct coordinate faces required')
        support=set()
        for j,term in enumerate(f['word']):
            if type(term) is not list or len(term)!=2:raise ValueError('signed edge pair required')
            eid,sign=term
            if type(eid) is not int or eid not in edges or type(sign) is not int or sign not in (-1,1):raise ValueError('strict signed edge required')
            ends=edges[eid] if sign==1 else edges[eid][::-1]
            if ends!=(vs[j],vs[(j+1)%4]):raise ValueError('wrong dagger or nonclosed face')
            support.add(eid);inc[eid].append(i)
        if len(support)!=4:raise ValueError('four distinct face links required')
        faces[i]=support;position[x]=i
    if len(faces)!=3:raise ValueError('all three faces required')
    return {'edges':edges,'incidence':inc,'supports':faces,'left':position[0],'middle':position[1],'right':position[2]}


def untouched_links(g,reference_faces):
    d=validate(g)
    if type(reference_faces) is not tuple or len(set(reference_faces))!=len(reference_faces) or any(type(i) is not int or i not in d['supports'] for i in reference_faces):raise ValueError('explicit distinct strict reference face tuple required')
    active=set().union(*(d['supports'][i] for i in reference_faces)) if reference_faces else set()
    free=d['supports'][d['middle']]-active
    if not free:raise ValueError('sharpened bridge identity has no untouched reference-Haar link')
    return sorted(free)


def quaternion(q):
    if type(q) is not tuple or len(q)!=4:raise ValueError('four-coordinate quaternion tuple required')
    q=tuple(exact(v) for v in q)
    if sum(x*x for x in q)!=1:raise ValueError('unit quaternion required')
    return q


def qmul(a,b):
    w,x,y,z=quaternion(a);v,p,q,r=quaternion(b)
    return (w*v-x*p-y*q-z*r,w*p+x*v+y*r-z*q,w*q-x*r+y*v+z*p,w*r+x*q-y*p+z*v)


def inverse(q):
    q=quaternion(q);return(q[0],-q[1],-q[2],-q[3])


I=(F(1),F(0),F(0),F(0))
QUATERNIONS=(I,(F(3,5),F(4,5),F(0),F(0)),(F(1,3),F(2,3),F(2,3),F(0)),(F(1,2),F(1,2),F(-1,2),F(1,2)))


def word_value(word,links):
    value=I
    for eid,sign in word:value=qmul(value,links[eid] if sign==1 else inverse(links[eid]))
    return value


def conditional_coefficients(g,links,free_edge):
    d=validate(g)
    if type(free_edge) is not int or free_edge not in d['supports'][d['middle']]:raise ValueError('actual strict bridge edge required')
    result=[]
    for i in range(4):
        changed=dict(links);changed[free_edge]=tuple(F(i==j) for j in range(4))
        result.append(word_value(g['faces'][d['middle']]['word'],changed)[0])
    return tuple(result)


def multiplication_norm_identities():
    # Each entry is one signed symbolic variable. Matrix multiplication retains
    # its exact quadratic polynomial rather than substituting test quaternions.
    L=(((0,1),(1,-1),(2,-1),(3,-1)),((1,1),(0,1),(3,-1),(2,1)),((2,1),(3,1),(0,1),(1,-1)),((3,1),(2,-1),(1,1),(0,1)))
    R=(((0,1),(1,-1),(2,-1),(3,-1)),((1,1),(0,1),(3,1),(2,-1)),((2,1),(3,-1),(0,1),(1,1)),((3,1),(2,1),(1,-1),(0,1)))
    records=[]
    for label,M in [('left',L),('right',R)]:
        for a,b in product(range(4),repeat=2):
            poly={}
            for k in range(4):
                i,s=M[k][a];j,t=M[k][b];key=tuple(sorted((i,j)));poly[key]=poly.get(key,0)+s*t
            poly={p:c for p,c in poly.items() if c};expected={(i,i):1 for i in range(4)} if a==b else {}
            if poly!=expected:raise ValueError('universal quaternion norm polynomial failed')
            records.append({'multiplication':label,'row':a,'column':b,'polynomial':[[list(k),v] for k,v in sorted(poly.items())]})
    return records


def generic_gap(reference_gap,perturbation_norm,zero_reference_mean=False):
    g,v=map(exact,(reference_gap,perturbation_norm))
    if g<=0 or v<0 or type(zero_reference_mean) is not bool:raise ValueError('positive reference gap, nonnegative norm and strict conditional flag required')
    return g-v if zero_reference_mean else g-2*v


def certify(alpha,end_couplings,mu,alpha_min=None,g=None):
    a,m=map(exact,(alpha,mu))
    if a<=0 or type(end_couplings) is not tuple or len(end_couplings)!=2:raise ValueError('positive alpha and exactly two end coefficients required')
    ends=tuple(map(exact,end_couplings));rho=max(map(abs,ends))/a
    if rho>=F(3,4):raise ValueError('outside reviewed reference-ground uniqueness domain')
    floor=None if alpha_min is None else exact(alpha_min)
    if floor is not None and not 0<floor<=a:raise ValueError('common physical floor must be positive and no greater than alpha')
    g=graph() if g is None else g;d=validate(g);active=tuple(i for i,l in zip((d['left'],d['right']),ends) if l);unused=untouched_links(g,active)
    gap=a*(F(3,4)-rho);sharp=generic_gap(gap,abs(m),True);coarse=generic_gap(gap,abs(m),False);member=rho<=F(1,2) and abs(m)<=a/8
    return {'alpha':str(a),'end_couplings':list(map(str,ends)),'mu':str(m),'alpha_min':None if floor is None else str(floor),'rho_actual':str(rho),
      'active_reference_faces':list(active),'untouched_bridge_links':unused,'reference_gap_lower':str(gap),'bridge_norm_bound':str(abs(m)),
      'conditional_bridge_mean':'0','conditional_bridge_squared_norm':'1/4','bridge_offdiagonal_norm':str(abs(m)/2),
      'sharp_gap_lower':str(sharp),'generic_gap_lower':str(coarse),'sharp_status':'positive' if sharp>0 else 'insufficient','sharp_sign':'positive' if sharp>0 else 'zero' if not sharp else 'negative',
      'primary_family_member':member,'primary_parameter_family_lower':str(a/8) if member else None,
      'common_energy_floor_lower':str(floor/8) if member and floor is not None else None,
      'scope':'Finite full link-space cluster bound, transferred to the physical sector after unique ground invariance; no repetition or dense homogeneous theorem.'}
