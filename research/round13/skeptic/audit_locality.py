"""Independent locality geometry, factorial tail, and false-transfer controls."""
from pathlib import Path
from fractions import Fraction as Q
from math import factorial
from itertools import combinations, product
import argparse, csv, hashlib, importlib.util, json

p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('--label',default='locality_normal');args=p.parse_args()
source=Path(args.source).resolve();before=hashlib.sha256(source.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('locality_producer',source);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
checks=[];failures=[]
def check(name,ok,detail=''):
    row={'name':name,'status':'passed' if ok else 'failed','detail':detail};checks.append(row)
    if not ok:failures.append(row)
def reject(name,f):
    try:f()
    except (ValueError,TypeError,ArithmeticError,RuntimeError):check(name,True);return
    check(name,False,'Unexpected acceptance')

def independent_tail(z,r,N):
    # Independently enclose exp(z), then exactly subtract its initial polynomial.
    z=Q(z);e=sum((z**j/factorial(j) for j in range(N+1)),Q(0))
    prefix=sum((z**j/factorial(j) for j in range(r)),Q(0))
    rest=z**(N+1)/factorial(N+1)/(1-z/Q(N+2))
    return e-prefix,e+rest-prefix

for z,r in [(Q(0),1),(Q(1,100),40),(Q(1,3),1),(Q(8),12),(Q(24),2),(Q(64),48)]:
    c=m.tail_enclosure(z,r);lo,hi=Q(c['lower']),Q(c['upper'])
    oracle=independent_tail(z,r,c['last_index']+40)
    check('tail_exp_subtraction_'+str(z)+'_'+str(r),lo<=oracle[0]<=oracle[1]<=hi)
    check('tail_width_'+str(z)+'_'+str(r),hi-lo<=Q(1,10**30))
    check('tail_count_'+str(z)+'_'+str(r),c['terms_summed']==max(0,c['last_index']-r+1))
    if z:check('tail_strict_positive_'+str(z)+'_'+str(r),0<lo<hi)

# Coordinates represented as unordered vertex endpoint pairs, independently.
def vadd(v,axis):return tuple(x+(i==axis) for i,x in enumerate(v))
def edge(v,axis):return tuple(sorted((v,vadd(v,axis))))
def independent_box(n,d,offset):
    vertices=list(product(range(offset,offset+n+1),repeat=d));links=set();ps=set()
    for v in vertices:
        for a in range(d):
            if v[a]<offset+n:links.add(edge(v,a))
        for a,b in combinations(range(d),2):
            if v[a]<offset+n and v[b]<offset+n:
                ps.add(frozenset([edge(v,a),edge(v,b),edge(vadd(v,a),b),edge(vadd(v,b),a)]))
    return links,ps

def convert_link(e):return edge(e[1],e[0])
def convert_p(p):return frozenset(map(convert_link,p))
def reach_radius(x,inner,ps):
    reach=set(x);seen=set()
    for r in range(1,len(ps)+2):
        frontier={p for p in ps if p&reach}-seen
        if any(not p<=inner for p in frontier):return r
        if not frontier:return None
        for p in frontier:reach.update(p)
        seen.update(frontier)
    raise RuntimeError('finite graph reachability did not terminate')

for d in (2,3):
    for margin in (0,1,2):
        inner,_=m.open_box(2*margin+1,d,-margin);outer,ps=m.open_box(2*margin+3,d,-margin-1)
        il,ip=independent_box(2*margin+3,d,-margin-1)
        check(f'independent_box_d{d}_m{margin}',set(map(convert_link,outer))==il and set(map(convert_p,ps))==ip)
        x=m.square((0,)*d,0,1);ii=set(map(convert_link,inner));xx=set(map(convert_link,x))
        expected=reach_radius(xx,ii,ip);got=m.boundary_radius(x,inner,ps)
        check(f'independent_radius_d{d}_m{margin}',expected==got==margin+1)
        result=m.bound_from_geometry(x,inner,ps,d,'1/100')
        generator=m.bound_from_geometry((e for e in x),(e for e in inner),(p for p in ps),d,'1/100')
        check(f'generator_regression_d{d}_m{margin}',generator==result and Q(result['bound'])>0)
        # Direct exhaustive path enumeration, intentionally small k only.
        previous=[(p,) for p in ps if p&x];counts=[]
        for k in range(1,4):
            counts.append(sum(1 for chain in previous if not chain[-1]<=inner))
            previous=[chain+(q,) for chain in previous if chain[-1]<=inner for q in ps if q&chain[-1]]
        check(f'independent_path_counts_d{d}_m{margin}',counts==m.exit_chain_counts(x,inner,ps,3))
        check(f'degree_count_d{d}_m{margin}',all(n<=len(x)*2*(d-1)*(8*(d-1))**(k-1) for k,n in enumerate(counts,1)))

inner,p0=m.open_box(1,2,0);_,p10=m.open_box(1,2,10);x=m.square((0,0),0,1)
check('disconnected_zero',m.bound_from_geometry(x,inner,p0|p10,2,100)['bound']=='0')
check('same_volume_zero',m.bound_from_geometry(x,inner,p0,2,100)['bound']=='0')
check('empty_support_zero',m.bound_from_geometry(set(),inner,p0|p10,2,100)['bound']=='0')
check('zero_action',m.local_bound(4,4,0,1)['bound']=='0')
check('zero_norm',m.local_bound(4,4,100,1,0)['bound']=='0')
check('zero_incidence',m.local_bound(4,0,1,1)['bound']=='0')
check('signed_envelope',m.integrated_envelope([(Q(1,3),[2,-5]),(Q(2,3),[-2,5])])==5)
check('volume_envelope',m.integrated_envelope([(1,[1]*100)])==1)
check('amplitude_scale',Q(m.local_bound(4,4,Q(1,100),3,7)['bound'])==7*Q(m.local_bound(4,4,Q(1,100),3)['bound']))
check('trivial_cap',m.local_bound(4,4,1,1)['bound']=='2')
for bad in [True,False,1.0,float('nan'),float('inf'),None,[],{},'nan','1/0']:
    reject('invalid_rational_'+repr(bad),lambda bad=bad:m.tail_enclosure(bad,2))
for bad in [0,-1,True,1.0,None]:reject('invalid_radius_'+repr(bad),lambda bad=bad:m.tail_enclosure(1,bad))
reject('negative_action',lambda:m.local_bound(4,4,-1,2))
reject('negative_norm',lambda:m.local_bound(4,4,1,2,-1))
reject('bad_incidence',lambda:m.local_bound(4,False,1,2))
reject('outside_support',lambda:m.boundary_radius({('alien',0)},inner,p0))
reject('three_link_term',lambda:m.incidence_and_adjacency([frozenset([1,2,3])]))
reject('negative_tolerance',lambda:m.tail_enclosure(1,1,-1))
reject('unmet_computation_budget',lambda:m.tail_enclosure(5,1,max_terms=5))

# False-transfer control with fixed local coefficients and unique vacuum.
# Fermion modes of the positive Dirichlet chain have epsilon_j=2−2cos(j*pi/(n+1)).
# Rational variational alternative avoids needing any floating eigenvalue:
# in the one-particle sector, vector v_i=i(n+1-i) has an exact Rayleigh quotient.
rayleigh=[]
for n in [4,8,16,32,64]:
    v=[Q(i*(n+1-i)) for i in range(1,n+1)]
    numerator=sum((2*a*a for a in v),Q(0))-2*sum((a*b for a,b in zip(v,v[1:])),Q(0))
    quotient=numerator/sum((a*a for a in v),Q(0));rayleigh.append(quotient)
    check('gapless_chain_rayleigh_n'+str(n),0<quotient<=Q(12,(n+1)**2))
check('locality_does_not_imply_gap',all(a>b for a,b in zip(rayleigh,rayleigh[1:])) and rayleigh[-1]<Q(1,300))

output=source.parent/'output'/'results.json'
if output.exists():
    data=json.loads(output.read_text());check('recorded_source_hash',data['source_sha256']==before)
    for name,digest in data['files'].items():check('output_hash_'+name,hashlib.sha256((output.parent/name).read_bytes()).hexdigest()==digest)
    rows=list(csv.DictReader((output.parent/'boundary_decay.csv').open()))
    for i in [0,11,23,47]:
        row=rows[i];r=int(row['radius']);z=Q(row['z']);bound=Q(row['bound_rational'])
        oracle=independent_tail(z,r,r+120)
        check('recorded_bound_'+str(r),min(Q(2),oracle[1])<=bound)
check('unchanged_source',before==hashlib.sha256(source.read_bytes()).hexdigest())
out={'status':'passed' if not failures else 'failed','source':str(source),'source_sha256':before,'count':len(checks),'checks':checks,'failures':failures,'scope':'Exact finite-time locality bound arithmetic and graph contract; analytic theorem independently reviewed. No observed Yang-Mills boundary-error simulation or mass gap.'}
Path(__file__).with_name(args.label+'_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'count':len(checks),'failures':failures},indent=2))
if failures:raise SystemExit(1)
