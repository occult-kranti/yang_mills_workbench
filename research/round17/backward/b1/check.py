"""Independent dense two-cube matrix and full-gap bound, exact arithmetic."""
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


def haar(power):
    if power%2:return F(0)
    value=F(1)
    for k in range(1,power//2+1):value*=F(2*k-1,2*k+2)
    return value


def moment(powers,inc):
    if any(type(p) is not int or p<0 for p in powers) or len(powers)!=11:raise ValueError('eleven exact multiplicities required')
    if any(sum(powers[p] for p in faces)%2 for faces in inc.values()):return F(0)
    active=[p for p in powers if p]
    if not active:return F(1)
    if len(active)==1:return haar(active[0])
    raise ValueError('moment outside the reviewed low-degree parity/single-face domain')


def trial_entries(g):
    inc,girth=geometry(g);gram=[];magnetic=[[] for _ in range(11)]
    for i in range(12):
        row=[];magrows=[[] for _ in range(11)]
        for j in range(12):
            powers=[0]*11;factor=1
            for index in (i,j):
                if index:powers[index-1]+=1;factor*=2
            row.append(factor*moment(powers,inc))
            for f in range(11):
                inserted=powers.copy();inserted[f]+=1;magrows[f].append(factor*moment(inserted,inc))
        gram.append(row)
        for f in range(11):magnetic[f].append(magrows[f])
    return gram,magnetic


def determinant(matrix):
    a=[list(map(F,row)) for row in matrix];sign=1;value=F(1)
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:return F(0)
        if pivot!=j:a[pivot],a[j]=a[j],a[pivot];sign=-sign
        term=a[j][j];value*=term
        for i in range(j+1,len(a)):
            ratio=a[i][j]/term
            for k in range(j,len(a)):a[i][k]-=ratio*a[j][k]
    return sign*value


def sqrt_bracket(q,precision='1/1000000000000',max_steps=32):
    q,tol=map(exact,(q,precision))
    if q<0 or tol<=0 or type(max_steps) is not int or not 0<=max_steps<=64:raise ValueError('nonnegative radicand, positive precision and bounded strict step count required')
    num,den=isqrt(q.numerator),isqrt(q.denominator)
    if num*num==q.numerator and den*den==q.denominator:return {'lower':str(F(num,den)),'upper':str(F(num,den)),'steps':0,'precision_status':'met','method':'exact rational square'}
    grid=1
    while F(1,grid)>tol/100:
        grid*=10
        if grid>10**60:raise ValueError('decimal enclosure precision cap')
    upper=max(F(1),q);steps=0
    for _ in range(max_steps):
        proposal=(upper+q/upper)/2;scaled=proposal*grid
        upper=F((scaled.numerator+scaled.denominator-1)//scaled.denominator,grid);steps+=1
        lower=(q/upper*grid).__floor__()/F(grid)
        if upper-lower<=tol:break
    lower=(q/upper*grid).__floor__()/F(grid)
    if not 0<=lower<=upper or lower*lower>q or upper*upper<q:raise ValueError('invalid outward root bracket')
    return {'lower':str(lower),'upper':str(upper),'steps':steps,'precision_status':'met' if upper-lower<=tol else 'insufficient','method':'directed decimal Newton upper and reciprocal lower'}


def bound(alpha,couplings,precision='1/1000000000000',max_steps=32):
    a=exact(alpha)
    if a<=0 or type(couplings) is not list or len(couplings)!=11:raise ValueError('positive alpha and eleven coefficients required')
    ls=list(map(exact,couplings));delta=3*a;L=sum(map(abs,ls));Q=sum(v*v for v in ls);root=sqrt_bracket(delta*delta+Q,precision,max_steps);lo,hi=map(F,(root['lower'],root['upper']))
    interval=((delta+lo)/2-L,(delta+hi)/2-L);ground=((delta-hi)/2,(delta-lo)/2)
    return {'alpha':str(a),'couplings':list(map(str,ls)),'delta':str(delta),'L':str(L),'Q':str(Q),'radicand':str(delta*delta+Q),'sqrt':root,
      'trial_ground_interval':list(map(str,ground)),'full_ground_upper':str(ground[1]),'full_E1_lower':str(delta-L),
      'full_gap_bound_interval':list(map(str,interval)),'status':'positive' if interval[0]>0 and root['precision_status']=='met' else 'insufficient',
      'sign_status':'positive' if interval[0]>0 else 'zero' if interval[0]==interval[1]==0 else 'negative' if interval[1]<0 else 'inconclusive',
      'scope':'Finite full physical lower bound from separate min-max E1 lower and trial E0 upper; no sparse or volume-uniform theorem.'}


def execute(output):
    output=Path(output).resolve()
    if output.is_relative_to(Path(__file__).resolve().parent):raise ValueError('output outside source required')
    output.mkdir(parents=True,exist_ok=False);checks=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError):check(name,True);return
        raise RuntimeError('invalid premise accepted '+name)
    g=graph();inc,girth=geometry(g);gram,magnetic=trial_entries(g)
    check('actual two-cube counts and girth',len(g['vertices'])==12 and len(g['edges'])==20 and len(g['faces'])==11 and girth==4)
    check('four internal-boundary links have incidence three',sorted(map(len,inc.values()))==[2]*16+[3]*4)
    check('all 144 Gram entries from multiplicities and Haar',gram==[[F(i==j) for j in range(12)] for i in range(12)])
    expected=[[[F(1,2) if (i==0 and j==f+1) or (j==0 and i==f+1) else F(0) for j in range(12)] for i in range(12)] for f in range(11)]
    check('all 1584 magnetic entries including repeated indices',magnetic==expected)
    check('repeated Haar entries are not replaced by distinct sets',4*haar(2)==1 and 16*haar(4)==2 and haar(1)==0)
    check('physical free gap differs from unprojected single-link gap',girth*F(3,4)==3 and F(3,4)<3)
    fixtures={'zero':bound(1,[0]*11),'old_boundary':bound(1,['3/11']*11),'new_boundary':bound(1,['12/43']*11),'beyond':bound(1,['1']*11),
      'signed_unequal':bound(1,['1/5','-1/7','0','1/11','-1/13','1/17','0','-1/19','1/23','0','1/29']),
      'scaled':bound(2,['6/11']*11),'coarse':bound(1,['3/11']*11,max_steps=0)}
    for name,c in fixtures.items():
        a=F(c['alpha']);ls=list(map(F,c['couplings']));delta=3*a;Q=sum(x*x for x in ls)
        H=[[F(0) if i==j==0 else delta if i==j else -sum(ls[f]*magnetic[f][i][j] for f in range(11)) for j in range(12)] for i in range(12)]
        for z in (-a,F(0),delta,2*delta):
            shifted=[[x-z*int(i==j) for j,x in enumerate(row)] for i,row in enumerate(H)]
            if determinant(shifted)!=(delta-z)**10*(z*z-delta*z-Q/4):raise RuntimeError('independent determinant mismatch '+name)
    check('full exact matrices have rank-two characteristic factor for every fixture',True)
    check('zero-coupling exception recovers physical free gap',fixtures['zero']['full_gap_bound_interval']==['3','3'])
    check('old sufficient endpoint gains positive full bound',fixtures['old_boundary']['full_E1_lower']=='0' and fixtures['old_boundary']['status']=='positive')
    check('new endpoint radical exact and bound zero',fixtures['new_boundary']['sqrt']['lower']==fixtures['new_boundary']['sqrt']['upper']=='135/43' and fixtures['new_boundary']['full_gap_bound_interval']==['0','0'] and fixtures['new_boundary']['status']=='insufficient')
    check('large positive trial gap does not certify full gap',F(fixtures['beyond']['delta'])-F(fixtures['beyond']['full_ground_upper'])>0 and fixtures['beyond']['sign_status']=='negative')
    check('coarse root cap explicitly fails precision',fixtures['coarse']['sqrt']['precision_status']=='insufficient' and fixtures['coarse']['status']=='insufficient')
    check('scaled physical bracket contains twice old-boundary bracket midpoint',F(fixtures['scaled']['full_gap_bound_interval'][0])<=sum(map(F,fixtures['old_boundary']['full_gap_bound_interval']))<=F(fixtures['scaled']['full_gap_bound_interval'][1]))
    signed=bound(1,[('-' if i%2 else '')+'3/11' for i in range(11)])
    check('signed equal magnitudes preserve the valid lower bound',signed['full_gap_bound_interval']==fixtures['old_boundary']['full_gap_bound_interval'])
    for r in (F(0),F(1,4),F(3,11),F(12,43),F(1,3),F(1)):
        polynomial=9+11*r*r-(22*r-3)**2
        if polynomial!=11*r*(12-43*r):raise RuntimeError('threshold polynomial factorization')
    check('exact threshold factorization includes sign restriction before squaring',True)
    bad=copy.deepcopy(g);bad['faces'][0]['word'][0][1]*=-1;reject('wrong signed face word',lambda:geometry(bad))
    bad=copy.deepcopy(g);bad['faces'].pop();reject('omitted internal or outer face',lambda:geometry(bad))
    bad=copy.deepcopy(g);bad['edges'][0]['head'][0]=True;reject('Boolean link coordinate rejected',lambda:geometry(bad))
    reject('eleven physical coefficients required',lambda:bound(1,[0]*10))
    reject('Boolean alpha rejected',lambda:bound(True,[0]*11))
    reject('nonpositive alpha rejected',lambda:bound(0,[0]*11))
    reject('Boolean iteration cap rejected',lambda:sqrt_bracket(2,max_steps=True))
    reject('nonpositive requested precision rejected',lambda:sqrt_bracket(2,0))
    result={'schema':'ym17-independent-b1-results-v1','status':'passed','checks_count':len(checks),'checks':checks,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'gram_entry_count':144,'magnetic_entry_count':1584,'girth':girth,'physical_free_gap_over_alpha':'3','common_ratio_threshold':'12/43','fixtures':fixtures,
      'scope':'Finite dense two-cube physical variational/min-max bound; A2 sparse theorem not applied; B2 unexecuted.'}
    encode=lambda obj: [[str(x) for x in row] for row in obj]
    (output/'results.json').write_text(json.dumps(result,indent=2)+'\n');(output/'graph.json').write_text(json.dumps(g,indent=2)+'\n')
    (output/'matrices.json').write_text(json.dumps({'Gram':encode(gram),'magnetic_face_insertions':[encode(M) for M in magnetic]},indent=2)+'\n')
    print(json.dumps({'status':'passed','checks_count':len(checks),'old_boundary_lower':fixtures['old_boundary']['full_gap_bound_interval'][0]}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();execute(a.output)
