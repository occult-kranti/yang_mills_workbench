"""Exact local constants and trial diagnostics for the declared rotor Hamiltonian."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json
SOURCE_BYTES=Path(__file__).read_bytes();SOURCE_SHA=hashlib.sha256(SOURCE_BYTES).hexdigest()
def unchanged():
    if Path(__file__).read_bytes()!=SOURCE_BYTES:raise ValueError('source changed after import')
def rational(v):
    if type(v) is not str or len(v)>1000:raise ValueError('canonical rational string required')
    try:x=F(v)
    except (ValueError,ZeroDivisionError) as exc:raise ValueError('invalid rational') from exc
    if str(x)!=v:raise ValueError('noncanonical rational')
    return x
def strict_equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict_equal(a[k],b[k]) for k in b)
    if type(a) is list:return len(a)==len(b) and all(strict_equal(x,y) for x,y in zip(a,b))
    return a==b
def trace_haar_moment(power):
    if type(power) is not int or not 0<=power<=32:raise ValueError('trace power must be integer0..32')
    if power%2:return F(0)
    import math
    return F(math.comb(power,power//2),(power//2+1)*4**(power//2))
def trial(alpha,lam,t):
    unchanged();a,l,s=map(rational,(alpha,lam,t))
    if a<=0:raise ValueError('alpha must be positive')
    norm=1+s*s;free=3*a*s*s/norm;magnetic=-l*s/norm
    return {'schema':'ym17-one-plaquette-trial-v1','source_sha256':SOURCE_SHA,
      'alpha':str(a),'lambda':str(l),'t':str(s),'norm_squared_before_normalization':str(norm),
      'free_energy':str(free),'magnetic_energy':str(magnetic),'total_energy':str(free+magnetic),
      'absolute_relative_ratio':str(abs(magnetic)/free) if free else None,
      'vacuum_image_norm_squared':str(l*l/4),
      'ratio_status':'defined' if free else 'undefined-zero-free-energy',
      'scope':'normalized physical trial (Omega+t*chi_p)/sqrt(1+t^2), one nonzero simple-plaquette coefficient; full rotor Hilbert retained'}
def verify_trial(c):
    if type(c) is not dict or c.get('schema')!='ym17-one-plaquette-trial-v1':raise ValueError('wrong trial schema')
    if not strict_equal(c,trial(c.get('alpha'),c.get('lambda'),c.get('t'))):raise ValueError('trial arithmetic or scope changed')
    return True
def local_constants(alpha,lam):
    unchanged();a,l=map(rational,(alpha,lam))
    if a<=0:raise ValueError('alpha must be positive')
    return {'alpha':str(a),'lambda':str(l),'PXP':'0','QXP_norm':'1/2','offdiagonal_X_norm':'1/2',
      'diagonal_X_norm_upper':'1','full_link_free_gap':str(3*a/4),'fundamental_loop_energy':str(3*a),
      'max_plaquettes_per_link':4,'max_touching_plaquettes_including_self':13,
      'max_other_touching_plaquettes':12,
      'diagonal_form_coefficient_against_sum_C':str(F(16,3)*abs(l)),
      'diagonal_relative_coefficient_against_H0':str(F(16,3)*abs(l)/a),
      'full_perturbation_pure_relative_bound':'not established; false for nonzero lambda without an additive/vacuum term'}
def name(v):return ','.join(map(str,v))
def box(n):
    if type(n) is not int or not 2<=n<=12:raise ValueError('vertex extent must be integer2..12, not Boolean')
    vertices=[name(v) for v in product(range(n),repeat=3)];edges=[];plaquettes=[]
    for v in product(range(n),repeat=3):
        for axis in range(3):
            if v[axis]+1<n:
                w=list(v);w[axis]+=1;edges.append({'id':str(axis)+':'+name(v),'tail':name(v),'head':name(w)})
    lookup={(e['tail'],e['head']):(e['id'],1) for e in edges};lookup.update({(e['head'],e['tail']):(e['id'],-1) for e in edges})
    for v in product(range(n),repeat=3):
        for a,b in ((0,1),(0,2),(1,2)):
            if v[a]+1<n and v[b]+1<n:
                x=list(v);x[a]+=1;y=x.copy();y[b]+=1;z=list(v);z[b]+=1
                loop=list(map(name,(v,x,y,z)))
                word=[{'edge':lookup[(loop[i],loop[(i+1)%4])][0],'sign':lookup[(loop[i],loop[(i+1)%4])][1]} for i in range(4)]
                plaquettes.append({'id':str(a)+str(b)+':'+name(v),'vertices':loop,'word':word})
    return {'schema':'ym17-open-cubic-link-graph-v1','n':n,'vertices':vertices,'edges':edges,'plaquettes':plaquettes,
            'Gauss':'all vertices; no external charges','boundary':'open spatial graph'}
def validate_graph(g):
    unchanged()
    if type(g) is not dict or not strict_equal(g,box(g.get('n'))):raise ValueError('graph differs from declared open cube contract')
    emap={e['id']:e for e in g['edges']};inc={e:[] for e in emap}
    for p in g['plaquettes']:
        if len(p['word'])!=4 or len(set(x['edge'] for x in p['word']))!=4:raise ValueError('plaquette must have four distinct links')
        for i,x in enumerate(p['word']):
            e=emap[x['edge']];ends=(e['tail'],e['head']) if x['sign']==1 else (e['head'],e['tail'])
            if ends!=(p['vertices'][i],p['vertices'][(i+1)%4]):raise ValueError('invalid signed closed word')
            inc[x['edge']].append(p['id'])
    if max(map(len,inc.values()))>4:raise ValueError('cubic link incidence exceeded')
    return inc
def overlap(g,p,q):
    validate_graph(g);pmap={x['id']:x for x in g['plaquettes']}
    if type(p) is not str or type(q) is not str or p not in pmap or q not in pmap:raise ValueError('declared plaquette identifiers required')
    a,b=pmap[p],pmap[q]
    links=sorted({x['edge'] for x in a['word']}&{x['edge'] for x in b['word']});vertices=sorted(set(a['vertices'])&set(b['vertices']))
    return {'left':p,'right':q,'shared_links':links,'shared_vertices':vertices,
            'relation':'same' if p==q else 'shared-link' if links else 'shared-vertex-only' if vertices else 'disjoint'}
def graph_audit(n):
    g=box(n);inc=validate_graph(g);touch=[]
    for p in g['plaquettes']:
        neighbors=set()
        for x in p['word']:neighbors.update(inc[x['edge']])
        touch.append(len(neighbors))
    return {'n':n,'vertices':len(g['vertices']),'edges':len(g['edges']),'plaquettes':len(g['plaquettes']),
      'maximum_link_incidence':max(map(len,inc.values())),
      'maximum_overlapping_plaquettes_including_self':max(touch),
      'maximum_other_overlapping_plaquettes':max(touch)-1,
      'graph_sha256':hashlib.sha256(json.dumps(g,sort_keys=True,separators=(',',':')).encode()).hexdigest()}
