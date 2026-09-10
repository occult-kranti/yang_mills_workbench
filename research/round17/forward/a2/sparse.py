"""Exact certificate arithmetic for the link-disjoint support exception."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
import geometry
SOURCE_BYTES=Path(__file__).read_bytes();SOURCE_SHA=hashlib.sha256(SOURCE_BYTES).hexdigest()
GEOMETRY_SHA='d17cd28f434b3de9e745e619538257a4cf89002115af07ba65b23c8c9449d673'
def unchanged():
    if Path(__file__).read_bytes()!=SOURCE_BYTES or geometry.SOURCE_SHA!=GEOMETRY_SHA or hashlib.sha256((Path(__file__).parent/'geometry.py').read_bytes()).hexdigest()!=GEOMETRY_SHA:
        raise ValueError('sparse or copied geometry source changed')
def extent(n):
    if type(n) is not int or n<2:raise ValueError('vertex extent must be an integer>=2, not Boolean')
    return n
def active_count(n):
    n=extent(n);return n*(n//2)**2
def even_anchors(n):
    n=extent(n)
    return ((x,y,z) for x in range(0,n-1,2) for y in range(0,n-1,2) for z in range(n))
def even_mask(n):
    n=extent(n)
    if n>12:raise ValueError('materialized mask cap12 matches the canonical graph cap; use lazy even_anchors for arbitrary extent')
    return ['01:'+','.join(map(str,a)) for a in even_anchors(n)]
def certify(graph,couplings,alpha='1',alpha_min='1',rho='1/2'):
    unchanged();geometry.validate_graph(graph);a,amin,r=map(geometry.rational,(alpha,alpha_min,rho))
    if a<=0 or amin<=0 or amin>a or r<0:raise ValueError('require alpha>=alpha_min>0 and rho>=0')
    if type(couplings) is not dict or any(type(k) is not str for k in couplings):raise ValueError('declared plaquette-to-rational coefficient dictionary required')
    ps={p['id']:p for p in graph['plaquettes']};ls={k:geometry.rational(v) for k,v in couplings.items()}
    if any(k not in ps for k in ls):raise ValueError('unknown plaquette in support')
    active={k:v for k,v in ls.items() if v};occupied={};blocks=[]
    for key in sorted(active):
        links=sorted(x['edge'] for x in ps[key]['word'])
        conflict=[e for e in links if e in occupied]
        if conflict:raise ValueError('nonzero plaquette supports share a link')
        for e in links:occupied[e]=key
        blocks.append({'plaquette':key,'lambda':str(active[key]),'links':links,
                       'unprojected_gap_lower':str(3*a/4-abs(active[key]))})
    ratio=max((abs(x)/a for x in active.values()),default=F(0))
    if ratio>r:raise ValueError('declared common rho does not bound all active coefficients')
    remaining=sorted(e['id'] for e in graph['edges'] if e['id'] not in occupied)
    bound=amin*(F(3,4)-r);valid=r<F(3,4)
    return {'schema':'ym17-sparse-gap-v1','source_sha256':SOURCE_SHA,'geometry_source_sha256':GEOMETRY_SHA,
      'graph_n':graph['n'],'graph_sha256':hashlib.sha256(json.dumps(graph,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
      'alpha':str(a),'alpha_min':str(amin),'rho':str(r),'couplings':{k:str(ls[k]) for k in sorted(ls)},
      'active_count':len(active),'zero_coefficients':sorted(k for k,v in ls.items() if not v),'blocks':blocks,
      'free_edges':remaining,'covered_link_count':len(occupied)+len(remaining),'actual_max_ratio':str(ratio),
      'uniform_family_lower_bound':str(bound),'ground_uniqueness_certified':valid,
      'ground_Gauss_inclusion_certified':valid,'status':'certified-positive-sparse-gap' if valid else 'insufficient-lower-bound',
      'scope':{'Hilbert':'full link tensor decomposition first; global Gauss invariant restriction afterwards',
               'graph':'original full open cubic link graph; every unlisted magnetic coefficient is0',
               'assumptions':'pairwise link-disjoint nonzero plaquettes; alpha>=alpha_min>0; max|lambda|/alpha<=rho<3/4',
               'dense_uniform_target':'open; overlapping interactions are outside this theorem'}}
def verify(graph,c):
    if type(c) is not dict or c.get('schema')!='ym17-sparse-gap-v1':raise ValueError('wrong sparse certificate schema')
    expected=certify(graph,c.get('couplings'),c.get('alpha'),c.get('alpha_min'),c.get('rho'))
    if not geometry.strict_equal(c,expected):raise ValueError('support, bound or theorem semantics failed replay')
    return True
