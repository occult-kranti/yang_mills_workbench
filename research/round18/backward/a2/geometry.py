"""Independent integer geometry and rational strip-family bounds; no author imports."""
from fractions import Fraction as F
from itertools import product
import copy


def integer(x,minimum=0,maximum=None):
    if type(x) is not int or x<minimum or (maximum is not None and x>maximum):raise ValueError('exact bounded integer required')
    return x


def rational(x):
    if type(x) not in (int,str,F):raise ValueError('exact rational required')
    return F(x)


def cluster_count(n):
    integer(n,2)
    return n*(n//4)*(n//2)


def anchors(n):
    integer(n,2)
    for i in range(n//4):
        for j in range(n//2):
            for z in range(n):yield (4*i,2*j,z)


def advance(v,axis):
    w=list(v);w[axis]+=1;return tuple(w)


def face_word(face):
    validate_face(face)
    a,b,x,y,z=face;v=(x,y,z);va=advance(v,a);vb=advance(v,b)
    return [([a,*v],1),([b,*va],1),([a,*vb],-1),([b,*v],-1)]


def validate_face(face,n=None):
    if type(face) not in (list,tuple) or len(face)!=5:raise ValueError('five exact face coordinates required')
    for q in face:integer(q)
    a,b,x,y,z=face
    if not 0<=a<b<=2:raise ValueError('ordered tangent axes required')
    if n is not None:
        integer(n,2);v=(x,y,z)
        if any(v[k]>=n-(k in (a,b)) for k in range(3)):raise ValueError('face lies outside actual box')


def build(n):
    integer(n,2,12)
    vertices=list(product(range(n),repeat=3));edges=[];faces=[]
    for v in vertices:
        for axis in range(3):
            if v[axis]<n-1:edges.append((axis,*v))
    for a,b in ((0,1),(0,2),(1,2)):
        for v in vertices:
            if v[a]<n-1 and v[b]<n-1:faces.append((a,b,*v))
    return {'schema':'ym18-independent-open-box-v1','n':n,'vertices':[list(v) for v in vertices],
      'edges':[list(e) for e in edges],'faces':[{'face':list(f),'word':[[e,s] for e,s in face_word(f)]} for f in faces]}


def strict(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict(a[k],b[k]) for k in a)
    if type(a) in (list,tuple):return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b


def validate(g):
    if type(g) is not dict or 'n' not in g:raise ValueError('graph schema required')
    if not strict(g,build(g['n'])):raise ValueError('canonical signed open-box graph mismatch')
    return True


def partition(n,g=None):
    g=build(n) if g is None else g;validate(g)
    if g['n']!=n:raise ValueError('graph size mismatch')
    selected={};used=set();clusters=[]
    for anchor in anchors(n):
        x,y,z=anchor;faces=[(0,1,x+t,y,z) for t in range(3)]
        support={tuple(e) for f in faces for e,_ in face_word(f)}
        if len(support)!=10 or used&support:raise ValueError('cluster link partition fails')
        used|=support
        for t,f in enumerate(faces):selected[f]={'anchor':list(anchor),'role':('left','middle','right')[t]}
        clusters.append({'anchor':list(anchor),'faces':[list(f) for f in faces],'edges':[list(e) for e in sorted(support)]})
    remaining=[]
    for row in g['faces']:
        f=tuple(row['face'])
        if f in selected:continue
        unused=[tuple(e) for e,_ in row['word'] if tuple(e) not in used]
        if not unused:raise ValueError('remaining face has no unused Haar link')
        witness=arithmetic_witness(n,f)
        if witness not in unused:raise ValueError('analytic witness is not an actual unused face link')
        remaining.append({'face':list(f),'unused_edge':list(witness),'case':witness_case(n,f)})
    return {'clusters':clusters,'selected':selected,'used':used,'free':[tuple(e) for e in g['edges'] if tuple(e) not in used],'remaining':remaining}


def witness_case(n,face):
    """Classify all possible missing faces by the analytic all-n proof."""
    validate_face(face,n)
    a,b,x,y,z=face
    if b==2:return 'unused z-link'
    if y%2:return 'unused odd y-interval'
    if x%4==3:return 'unused separating x-interval'
    if x//4>=n//4:return 'unused incomplete boundary x-interval'
    raise ValueError('a selected xy face was presented as remaining')


def arithmetic_witness(n,face):
    case=witness_case(n,face);axis=2 if case=='unused z-link' else 1 if case=='unused odd y-interval' else 0
    return (axis,*face[2:])


def weight(face):
    validate_face(face)
    return F(1,24*(1<<sum(face[2:])))


def series(m,step=1):
    integer(m,0,4096);integer(step,1,4)
    return (1-F(1,1<<(step*m)))/(1-F(1,1<<step))


def weights_formula(n):
    integer(n,2,4096)
    total=series(n-1)**2*series(n)/8
    selected=F(7,96)*series(n//4,4)*series(n//2,2)*series(n)
    return {'total':total,'selected':selected,'remaining':total-selected}


def schedule(kind):
    if kind!='dyadic_orthant':raise ValueError('no volume-independent summable budget for requested schedule')
    return F(3)*F(1,24)*(1/(1-F(1,2)))**3


def certify(n,alpha='1',alpha_min='1',left='1/2',right='1/2',middle='1/8',tau='1/64',g=None):
    alpha,alpha_min,left,right,middle,tau=map(rational,(alpha,alpha_min,left,right,middle,tau))
    if not 0<alpha_min<=alpha:raise ValueError('common positive physical scale required')
    if max(abs(left),abs(right))>alpha/2 or abs(middle)>alpha/8:raise ValueError('A1 canonical reference family not established')
    p=partition(n,g);form=weights_formula(n);total=sum((weight(tuple(r['face'])) for r in (build(n) if g is None else g)['faces']),F(0))
    selected=sum((weight(f) for f in p['selected']),F(0));remaining=sum((weight(tuple(r['face'])) for r in p['remaining']),F(0))
    if (total,selected,remaining)!=(form['total'],form['selected'],form['remaining']):raise ValueError('independent weight sum mismatch')
    baseline=alpha/8;beta=alpha*abs(tau)*remaining;uniform=F(1,8)-abs(tau)
    finite=baseline-beta;common=alpha_min*uniform if uniform>=0 else None
    full=tau!=0 and (not p['clusters'] or (left!=0 and right!=0 and middle!=0))
    return {'n':n,'alpha':str(alpha),'alpha_min':str(alpha_min),'left':str(left),'right':str(right),'middle':str(middle),'tau':str(tau),
      'counts':{'vertices':n**3,'edges':3*n*n*(n-1),'faces':3*n*(n-1)**2,'clusters':len(p['clusters']),
                'selected_faces':len(p['selected']),'cluster_edges':len(p['used']),'free_edges':len(p['free']),'remaining_faces':len(p['remaining'])},
      'weights':{k:str(v) for k,v in form.items()},'reference_actual_free_gap_if_no_clusters':str(3*alpha/4) if not p['clusters'] else None,
      'reference_conservative_lower':str(baseline),'remainder_norm_bound':str(beta),'finite_one_norm_lower':str(finite),'finite_two_norm_lower':str(baseline-2*beta),
      'uniform_one_norm_over_alpha':str(uniform),'uniform_two_norm_over_alpha':str(F(1,8)-2*abs(tau)),
      'uniform_lower_at_alpha':str(alpha*uniform),'common_physical_lower':str(common) if common is not None else None,
      'uniform_status':'positive' if uniform>0 else 'zero-insufficient' if uniform==0 else 'negative-insufficient',
      'finite_status':'positive' if finite>0 else 'insufficient','full_actual_face_support':full,
      'scope':'Full-support only when every actual coefficient is nonzero; inhomogeneous summable remainder; no homogeneous dense or continuum theorem.'}


def coefficient_ledger(n,alpha='1',left='1/2',right='1/2',middle='1/8',tau='1/64'):
    alpha,left,right,middle,tau=map(rational,(alpha,left,right,middle,tau));p=partition(n);rows=[]
    roles={'left':left,'right':right,'middle':middle}
    for row in build(n)['faces']:
        f=tuple(row['face']);w=weight(f);role=p['selected'][f]['role'] if f in p['selected'] else 'remainder'
        rows.append({'face':list(f),'role':role,'weight':str(w),'coefficient':str(roles[role] if role!='remainder' else alpha*tau*w)})
    return rows
