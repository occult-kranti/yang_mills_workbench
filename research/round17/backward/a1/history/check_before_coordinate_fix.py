"""Fresh independent A1 operator/graph/trial audit; Python standard library only."""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import argparse,copy,csv,hashlib,json


def rational(v):
    if type(v) not in (int,str,F):raise ValueError('exact rational required')
    try:return F(v)
    except (ValueError,ZeroDivisionError) as e:raise ValueError('finite rational required') from e


def extent(n):
    if type(n) is not int or not 2<=n<=8:raise ValueError('integer vertex extent2..8 required')
    return n


def build_graph(n):
    n=extent(n);vertices=list(product(range(n),repeat=3));edges=[];lookup={}
    for v in vertices:
        for a in range(3):
            if v[a]==n-1:continue
            w=list(v);w[a]+=1;w=tuple(w);key=len(edges);edges.append({'id':key,'tail':list(v),'head':list(w)})
            lookup[(v,w)]=(key,1);lookup[(w,v)]=(key,-1)
    faces=[]
    for v in vertices:
        for a,b in combinations(range(3),2):
            if v[a]==n-1 or v[b]==n-1:continue
            va=list(v);va[a]+=1;vb=list(v);vb[b]+=1;vab=va.copy();vab[b]+=1
            loop=[v,tuple(va),tuple(vab),tuple(vb)]
            faces.append({'id':len(faces),'vertices':[list(w) for w in loop],
              'word':[list(lookup[(loop[i],loop[(i+1)%4])]) for i in range(4)]})
    return {'schema':'ym17-independent-open-cubic-v1','extent':n,'vertices':[list(v) for v in vertices],'edges':edges,'faces':faces}


def validate_graph(g):
    if type(g) is not dict or g.get('schema')!='ym17-independent-open-cubic-v1':raise ValueError('graph schema')
    if type(g.get('vertices')) is not list or any(type(v) is not list or len(v)!=3 or any(type(x) is not int for x in v) for v in g['vertices']):raise ValueError('strict integer coordinate triples required')
    n=extent(g['extent']);vertices={tuple(v) for v in g['vertices']};expected=set(product(range(n),repeat=3))
    if vertices!=expected or len(g['vertices'])!=len(expected):raise ValueError('incomplete vertex box')
    edges={};geometry=set()
    for e in g['edges']:
        if type(e['id']) is not int or e['id'] in edges:raise ValueError('unique integer edge id required')
        a,b=tuple(e['tail']),tuple(e['head']);delta=tuple(y-x for x,y in zip(a,b))
        if a not in vertices or b not in vertices or delta not in ((1,0,0),(0,1,0),(0,0,1)):raise ValueError('invalid coordinate link')
        if (a,b) in geometry:raise ValueError('duplicate geometric link')
        edges[e['id']]=(a,b);geometry.add((a,b))
    needed={(a,b) for a in vertices for axis in range(3) for b in [tuple(x+(i==axis) for i,x in enumerate(a))] if b in vertices}
    if geometry!=needed:raise ValueError('incomplete link set')
    incidence={eid:[] for eid in edges};face_geometry=set();ids=set()
    for f in g['faces']:
        if type(f['id']) is not int or f['id'] in ids:raise ValueError('unique face id required')
        ids.add(f['id']);vs=[tuple(v) for v in f['vertices']]
        if len(vs)!=4 or len(set(vs))!=4 or len(f['word'])!=4:raise ValueError('simple four-link square required')
        spans=[max(v[a] for v in vs)-min(v[a] for v in vs) for a in range(3)]
        if sorted(spans)!=[0,1,1] or not set(vs)<=vertices:raise ValueError('unit coordinate square required')
        geom=frozenset(vs)
        if geom in face_geometry:raise ValueError('duplicate geometric square')
        face_geometry.add(geom)
        for i,term in enumerate(f['word']):
            if type(term) is not list or len(term)!=2:raise ValueError('edge/sign pair required')
            eid,sign=term
            if type(eid) is not int or eid not in edges or type(sign) is not int or sign not in (-1,1):raise ValueError('strict oriented edge required')
            a,b=edges[eid];ordered=(a,b) if sign==1 else (b,a)
            if ordered!=(vs[i],vs[(i+1)%4]):raise ValueError('word does not follow signed boundary')
            incidence[eid].append(f['id'])
    # Every admissible geometric square is counted independently through its minimum vertex.
    needed_faces=set()
    for v in vertices:
        for a,b in combinations(range(3),2):
            square={tuple(x+((i==a)*da+(i==b)*db) for i,x in enumerate(v)) for da,db in product((0,1),repeat=2)}
            if square<=vertices:needed_faces.add(frozenset(square))
    if face_geometry!=needed_faces:raise ValueError('incomplete elementary face set')
    return edges,incidence


def haar_x_moment(power):
    if type(power) is not int or power<0:raise ValueError('nonnegative integer moment required')
    if power%2:return F(0)
    # Integration by parts for the normalized density proportional to sqrt(1-x²).
    value=F(1)
    for k in range(1,power//2+1):value*=F(2*k-1,2*k+2)
    return value


def trial(alpha,coupling,t):
    alpha,coupling,t=map(rational,(alpha,coupling,t))
    if alpha<=0:raise ValueError('positive physical energy normalization required')
    norm=1+t*t;electric=3*alpha*t*t/norm;magnetic=-coupling*t/norm
    ratio=None if electric==0 else magnetic/electric
    return {'alpha':str(alpha),'lambda':str(coupling),'t':str(t),'norm_squared':str(norm),
      'electric':str(electric),'magnetic':str(magnetic),'diagonal_magnetic':'0',
      'signed_ratio':None if ratio is None else str(ratio),
      'ratio_status':'undefined-zero-free-energy' if ratio is None else 'computed'}


# Gaussian rationals and 2x2 matrices provide exact, noncommuting gauge fixtures.
def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def conj(a):return a[0],-a[1]
ZERO=(F(0),F(0));ONE=(F(1),F(0));IDENTITY=((ONE,ZERO),(ZERO,ONE))


def matrix_product(a,b):
    return tuple(tuple(add(mul(a[i][0],b[0][j]),mul(a[i][1],b[1][j])) for j in range(2)) for i in range(2))


def dagger(a):return tuple(tuple(conj(a[j][i]) for j in range(2)) for i in range(2))


def su2(seed):
    t,s=F(seed+1,7),F(seed+2,11);c,d=(1-t*t)/(1+t*t),2*t/(1+t*t);z=((1-s*s)/(1+s*s),2*s/(1+s*s))
    rotation=(((c,F(0)),(d,F(0))),((-d,F(0)),(c,F(0))));phase=((z,ZERO),(ZERO,conj(z)))
    return matrix_product(rotation,phase)


def face_trace(word,links):
    result=IDENTITY
    for eid,sign in word:
        if type(sign) is not int or sign not in (-1,1):raise ValueError('strict sign required')
        result=matrix_product(result,links[eid] if sign==1 else dagger(links[eid]))
    value=add(result[0][0],result[1][1])
    if value[1]!=0:raise ValueError('SU2 trace unexpectedly complex')
    return value[0]/2


def execute(output):
    output=Path(output).resolve()
    if output.is_relative_to(Path(__file__).resolve().parent):raise ValueError('output must be outside frozen source directory')
    output.mkdir(parents=True,exist_ok=False);checks=[]
    def check(name,condition):
        if not condition:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError):check(name,True);return
        raise RuntimeError('invalid case accepted: '+name)
    check('normalized Haar mean and second moment',haar_x_moment(0)==1 and haar_x_moment(1)==0 and haar_x_moment(2)==F(1,4))
    check('character norm, vacuum coupling and cubic moment',4*haar_x_moment(2)==1 and 2*haar_x_moment(2)==F(1,2) and 4*haar_x_moment(3)==0)
    check('local QxP norm squared exactly one quarter',haar_x_moment(2)-haar_x_moment(1)**2==F(1,4))
    check('omitting normalized trace factor would change squared norm to one',4*haar_x_moment(2)==1!=F(1,4))
    # Principal character matrices test exact algebraic split, not full-space spectrum.
    for size in (2,3,5):
        x=[[F(int(abs(i-j)==1),2) for j in range(size)] for i in range(size)]
        split=[[x[i][j]*int(i!=0)*int(j!=0)+x[i][j]*int(i==0)*int(j!=0)+x[i][j]*int(i!=0)*int(j==0) for j in range(size)] for i in range(size)]
        check('principal character split size='+str(size),x==split and x[0][0]==0)
        check('dropping offdiagonal fails size='+str(size),x[0][1]!=x[0][1]*int(0!=0)*int(1!=0))
    occupation_rows=[]
    for occupations in product((0,1),repeat=4):
        q=int(any(occupations));s=sum(occupations);occupation_rows.append({'edge_excited':occupations,'Q':q,'sum_q':s})
        if q>s:raise RuntimeError('projector inequality failed')
    check('all sixteen joint projector sectors satisfy union bound',len(occupation_rows)==16)
    for n in range(1,17):
        C=F(n*(n+2),4)
        if F(4,3)*C<1 or n*(n+2)-3!=(n-1)*(n+3):raise RuntimeError('Casimir inequality')
    check('Casimir factor with exact nonnegative factorization',True)
    check('unprojected link gap is three quarters',F(1*(1+2),4)==F(3,4))
    check('physical square character has four-link energy three',4*F(3,4)==3)
    check('using physical square gap for one-link projector fails',F(3,4)/3<1)
    graph_rows=[];graphs={}
    for n in (2,3,4,6):
        g=build_graph(n);edges,inc=validate_graph(g);graphs[n]=g;counts=[len(v) for v in inc.values()]
        overlaps=[]
        for face in g['faces']:
            neighbors=set().union(*(set(inc[eid]) for eid,_ in face['word']))-{face['id']};overlaps.append(len(neighbors))
        check('actual cubic incidence at most four n='+str(n),max(counts)<=4 and min(counts)>=2)
        check('actual plaquette edge overlap at most twelve n='+str(n),max(overlaps)<=12)
        check('geometric link and face counts n='+str(n),len(edges)==3*n*n*(n-1) and len(g['faces'])==3*n*(n-1)**2)
        graph_rows.append({'n':n,'vertices':len(g['vertices']),'edges':len(edges),'faces':len(g['faces']),'minimum_incidence':min(counts),'maximum_incidence':max(counts),'maximum_other_edge_overlaps':max(overlaps)})
    _,inc=validate_graph(graphs[3]);interior=next(e for e,c in inc.items() if len(c)==4)
    check('actual single-link state saturates incidence-Casimir factor',F(len(inc[interior]),1)/F(3,4)==F(16,3))
    check('factor four-thirds without incidence factor fails',F(len(inc[interior]))>F(4,3)*F(3,4))
    check('boundary incidence is not asserted equal to bulk',graph_rows[0]['maximum_incidence']==2 and graph_rows[-1]['minimum_incidence']==2)
    # Coordinate words and their physical gauge action on one complete cube.
    cube=graphs[2];edges,_=validate_graph(cube);links={eid:su2(eid+1) for eid in edges};gauges={tuple(v):su2(i+41) for i,v in enumerate(cube['vertices'])}
    check('all exact link fixtures are unitary',all(matrix_product(dagger(U),U)==IDENTITY for U in links.values()))
    check('all exact link fixtures have determinant one',all(add(mul(U[0][0],U[1][1]),tuple(-x for x in mul(U[0][1],U[1][0])))==ONE for U in links.values()))
    transformed={eid:matrix_product(matrix_product(gauges[a],U),dagger(gauges[b])) for eid,U in links.items() for a,b in [edges[eid]]}
    for f in cube['faces']:
        trace=face_trace(f['word'],links);check('actual physical trace gauge invariant face='+str(f['id']),face_trace(f['word'],transformed)==trace)
        reverse=[[e,-s] for e,s in f['word'][::-1]];check('whole-face inverse invariant face='+str(f['id']),face_trace(reverse,links)==trace)
        wrong=copy.deepcopy(f['word']);wrong[0][1]*=-1;check('one wrong dagger discriminates face='+str(f['id']),face_trace(wrong,transformed)!=face_trace(wrong,links))
        for other in cube['faces']:
            if f['id']!=other['id'] and not ({e for e,_ in other['word']}-{e for e,_ in f['word']}):raise RuntimeError('distinct square lacks independent center edge')
    check('each other magnetic face has center-odd edge absent from selected trial',True)
    for label,change in [('missing face',lambda b:b['faces'].pop()),('duplicate face',lambda b:b['faces'].append(copy.deepcopy(b['faces'][0]))),('wrong dagger',lambda b:b['faces'][0]['word'][0].__setitem__(1,-1)),('Boolean sign',lambda b:b['faces'][0]['word'][0].__setitem__(1,True)),('missing edge',lambda b:b['edges'].pop()),('Boolean extent',lambda b:b.update(extent=True))]:
        bad=copy.deepcopy(cube);change(bad);reject('malformed graph '+label,lambda b=bad:validate_graph(b))
    trial_rows=[]
    for coupling in (F(-1),F(0),F(1)):
        for t in (F(-1),F(-1,4),F(-1,64),F(0),F(1,64),F(1,4),F(1)):
            row=trial(1,coupling,t);trial_rows.append(row)
            check('signed physical trial lambda='+str(coupling)+' t='+str(t),F(row['electric'])==3*t*t/(1+t*t) and F(row['magnetic'])==-coupling*t/(1+t*t) and (row['signed_ratio'] is None if t==0 else F(row['signed_ratio'])==-coupling/(3*t)))
    check('origin quotient remains explicitly undefined',trial(1,1,0)['signed_ratio'] is None and trial(1,0,0)['ratio_status']=='undefined-zero-free-energy')
    check('zero coupling is a true zero quotient away from origin',trial(1,0,'1/64')['signed_ratio']=='0')
    divergences=[]
    for exponent in range(1,11):
        t=F(1,2**exponent);ratio=abs(F(trial(1,1,t)['signed_ratio']));divergences.append({'t':str(t),'absolute_ratio':str(ratio)})
    check('halving trial amplitude doubles exact full-form ratio',all(F(b['absolute_ratio'])==2*F(a['absolute_ratio']) for a,b in zip(divergences,divergences[1:])))
    witness=trial(1,1,'1/64')
    check('actual physical state defeats proposed full sixteen-thirds relative bound',abs(F(witness['magnetic']))>F(16,3)*F(witness['electric']))
    check('vacuum diagonal contribution vanishes in same witness',F(witness['diagonal_magnetic'])==0 and F(witness['magnetic'])!=0)
    check('physical scale changes quotient inversely',F(trial(7,1,'1/64')['signed_ratio'])==F(witness['signed_ratio'])/7)
    check('signed trial reverses magnetic energy and keeps free energy',trial(1,1,'-1/64')['magnetic']==str(-F(witness['magnetic'])) and trial(1,1,'-1/64')['electric']==witness['electric'])
    for value in (True,0,-1,'nan','1/0',0.5):reject('invalid physical alpha '+repr(value),lambda v=value:trial(v,1,'1/2'))
    for value in (True,1,9,2.0):reject('invalid extent '+repr(value),lambda v=value:build_graph(v))
    result={'schema':'ym17-independent-a1-review-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'constants':{'QxP_norm':'1/2','single_link_gap_over_alpha':'3/4','physical_square_energy_over_alpha':'3','projector_Casimir_factor':'4/3','maximum_link_incidence':4,'diagonal_form_factor':'16/3','maximum_other_edge_overlaps':12},
      'graph_rows':graph_rows,'trial_rows':trial_rows,'divergence':divergences,'relative_bound_counterexample':witness,
      'theorem_status':'Local operator bounds and exact failure of pure full-perturbation relative form bound; dense uniform gap remains open.',
      'limits':'Analytic operator derivation plus exact finite diagnostics; character principal matrices do not replace the full operator or prove continuum statements.'}
    (output/'results.json').write_text(json.dumps(result,indent=2)+'\n');(output/'cube_graph.json').write_text(json.dumps(cube,indent=2)+'\n');(output/'projector_sectors.json').write_text(json.dumps(occupation_rows,indent=2)+'\n')
    with (output/'divergence.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=['t','absolute_ratio']);writer.writeheader();writer.writerows(divergences)
    print(json.dumps({'status':'passed','checks_count':len(checks),'counterexample_ratio':witness['signed_ratio']}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args();execute(args.output)
