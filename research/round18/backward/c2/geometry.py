"""Independent actual square-loop reconstruction for two variable vertical links."""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
from angular import rational,strict

_SOURCE=Path(__file__).read_bytes()


def unchanged():
    if Path(__file__).read_bytes()!=_SOURCE:raise ValueError('geometry source changed after loading')


def name(v):return ','.join(map(str,v))


def graph():
    unchanged();vs=list(product(range(3),range(3),range(2)));edges=[];pairs={}
    for v in vs:
        for axis in range(3):
            w=list(v);w[axis]+=1;w=tuple(w)
            if w not in vs:continue
            eid=f'e{axis}:'+name(v);edges.append({'id':eid,'tail':list(v),'head':list(w),'axis':axis})
            pairs[(v,w)]=(eid,1);pairs[(w,v)]=(eid,-1)
    faces=[]
    for v in vs:
        for a,b in combinations(range(3),2):
            va=list(v);va[a]+=1;vb=list(v);vb[b]+=1;vab=va.copy();vab[b]+=1
            loop=[v,tuple(va),tuple(vab),tuple(vb)]
            if any(w not in vs for w in loop):continue
            normal=3-a-b
            faces.append({'id':f'f{normal}:'+name(v),'normal':normal,'base':list(v),'vertices':list(map(list,loop)),
              'word':[{'edge':pairs[(loop[j],loop[(j+1)%4])][0],'sign':pairs[(loop[j],loop[(j+1)%4])][1]} for j in range(4)]})
    faces.sort(key=lambda f:(f['normal'],f['base']))
    return {'schema':'ym18-independent-two-link-complex-v1','vertices':list(map(list,vs)),'edges':edges,'faces':faces}


def validate(g):
    unchanged()
    if not strict(g,graph()):raise ValueError('actual signed four-cube geometry differs from canonical reconstruction')
    return True


def reduce(g):
    validate(g);U='e2:1,1,0';V='e2:1,0,0';rows=[];incU=[];incV=[]
    for f in g['faces']:
        word=[t for t in f['word'] if t['edge'] in (U,V)]
        if any(t['edge']==U for t in word):incU.append(f['id'])
        if any(t['edge']==V for t in word):incV.append(f['id'])
        if not word:trace='1'
        elif len(word)==1:trace='x' if word[0]['edge']==U else 'y'
        elif len(word)==2 and {t['edge'] for t in word}=={U,V} and word[0]['sign']==-word[1]['sign']:trace='w'
        else:raise ValueError('unproved two-link word reduction')
        rows.append({'face':f['id'],'variable_word':word,'trace':trace})
    return {'U':U,'V':V,'U_faces':incU,'V_faces':incV,'affected_faces':[r['face'] for r in rows if r['trace']!='1'],
      'constant_faces':[r['face'] for r in rows if r['trace']=='1'],'reduced_faces':rows,
      'trace_counts':{t:sum(r['trace']==t for r in rows) for t in ('x','y','w','1')}}


def quaternion(value):
    if type(value) not in (list,tuple) or len(value)!=4:raise ValueError('four exact quaternion coordinates required')
    q=tuple(rational(v) for v in value)
    if sum(v*v for v in q)!=1:raise ValueError('unit quaternion required')
    return q


def multiply(a,b):
    w,x,y,z=a;v,p,q,r=b
    return (w*v-x*p-y*q-z*r,w*p+x*v+y*r-z*q,w*q-x*r+y*v+z*p,w*r+x*q-y*p+z*v)


def dagger(a):return (a[0],-a[1],-a[2],-a[3])


def traces(g,U,V):
    info=reduce(g);U=quaternion(U);V=quaternion(V);identity=(F(1),F(0),F(0),F(0));links={e['id']:identity for e in g['edges']};links[info['U']]=U;links[info['V']]=V
    result=[]
    for f in g['faces']:
        q=identity
        for term in f['word']:
            v=links[term['edge']];q=multiply(q,v if term['sign']==1 else dagger(v))
        result.append({'face':f['id'],'trace':str(q[0])})
    return result


def gram(y,kappa='1/64'):
    y=rational(y);k=rational(kappa)
    if not -1<=y<=1:raise ValueError('semicircle coordinate outside [-1,1]')
    G=[[F(0) for _ in range(5)] for _ in range(5)];G[0][0]=k*k*(10+6*y)
    for i in range(1,4):G[0][i]=G[i][0]=k*(3+y)
    G[0][4]=G[4][0]=k*(3*y+1)
    for i in range(1,5):
        for j in range(1,5):G[i][j]=y if (i==4)!=(j==4) else F(1)
    return {'y':str(y),'kappa':str(k),'gram':[[str(v) for v in row] for row in G],'rank':1 if abs(y)==1 else 2,
      'action_norm_squared':str(G[0][0]),'central_coefficients':[str(k)]*4,
      'measure':'(2/pi)*sqrt(1-y^2) dy on[-1,1]',
      'denominator':'integral rho(y) exp(2*kappa*y) Z_U(G(y)) dy',
      'numerator':'integral rho(y) exp(2*kappa*y) N_U(G(y)) dy'}
