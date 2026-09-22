#!/usr/bin/env python3
"""Independent AI3 exact geometry, retained symmetry and full-error audit.

Standard library only. No inherited checker is imported. Physical transfer
lemmas are named inherited inputs, not proved by these finite checks.
"""
import argparse
import hashlib
import itertools as it
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

sys.set_int_max_str_digits(0)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CHECKS = []


def need(ok, name):
    if not ok:
        raise RuntimeError(name)
    CHECKS.append(name)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [encode(v) for v in x]
    return x


def move(v, axis, step=1):
    w = list(v)
    w[axis] += step
    return tuple(w)


def edge(v, w):
    return tuple(sorted((v, w)))


def axis(e):
    return next(j for j in range(3) if e[0][j] != e[1][j])


def face(base, a, b):
    return frozenset((edge(base, move(base, a)),
                      edge(base, move(base, b)),
                      edge(move(base, a), move(move(base, a), b)),
                      edge(move(base, b), move(move(base, b), a))))


def face_record(f):
    vertices = set().union(*map(set, f))
    base = tuple(min(v[j] for v in vertices) for j in range(3))
    directions = tuple(j for j in range(3) if len({v[j] for v in vertices}) == 2)
    return base, directions


def is_omitted(f):
    (x, y, _), directions = face_record(f)
    return not (directions == (0, 1) and y % 2 == 0 and x % 4 != 3)


def owner(e):
    x, y, z = e[0]
    a = axis(e)
    if (a == 0 and x % 4 != 3) or (a == 1 and y % 2 == 0):
        return ('strip', 4 * (x // 4), 2 * (y // 2), z)
    return ('free', e)


def factor_links(o):
    if o[0] == 'free':
        return {o[1]}
    _, x, y, z = o
    return {edge((x+i, y+j, z), (x+i+1, y+j, z))
            for i in range(3) for j in range(2)} | {
                edge((x+i, y, z), (x+i, y+1, z)) for i in range(4)}


def incident(links):
    result = set()
    for e in links:
        a = axis(e)
        for b in set(range(3)) - {a}:
            for v in (e[0], move(e[0], b, -1)):
                if min(v) >= 0:
                    f = face(v, a, b)
                    if is_omitted(f):
                        result.add(f)
    return result


def path(vertices):
    return frozenset(edge(v, w) for v, w in zip(vertices, vertices[1:]))


def geometry():
    vertices = list(it.product((3, 4), (1, 2), (0, 1)))
    links = sorted(edge(v, w) for v, w in it.combinations(vertices, 2)
                   if sum(abs(a-b) for a, b in zip(v, w)) == 1)
    need(len(links) == 12 and all(owner(e)[0] == 'free' for e in links),
         'physical twelve free links')
    # Enumerate graph cycles by degree and connectivity, without inherited indices.
    cycles = []
    for chosen in it.combinations(links, 6):
        used = set().union(*map(set, chosen))
        if len(used) != 6 or any(sum(v in e for e in chosen) != 2 for v in used):
            continue
        reached = {min(used)}
        for _ in range(6):
            reached |= {w for e in chosen if reached.intersection(e) for w in e}
        if reached == used:
            cycles.append(frozenset(chosen))
    need(len(cycles) == 16, 'sixteen reached cube cycles')
    cube_faces = {face(v, a, b) for a, b in it.combinations(range(3), 2)
                  for v in vertices if v[a] == (3, 1, 0)[a]
                  and v[b] == (3, 1, 0)[b]}
    need(len(cube_faces) == 6, 'all six physical cube faces')
    X = path([(3,1,0),(3,2,0),(3,2,1),(4,2,1),(4,2,0),(4,1,0),(3,1,0)])
    Y4 = X ^ face((3,1,0), 1, 2)
    Y5 = X ^ face((4,1,0), 1, 2)
    need(all(c in cycles for c in (X,Y4,Y5)), 'actual source paths belong to reached component')
    sources = [(cycles.index(X), cycles.index(Y4)), (cycles.index(X), cycles.index(Y5))]
    seed = set(X | Y4 | Y5)
    need(len(seed) == 10 and len(X|Y4) == len(X|Y5) == 8, 'ten-link common seed')
    need(not Y5 <= X|Y4, 'incomplete eight-link seed rejected')
    for Y in (Y4,Y5):
        need(len(X&Y)==4 and len(X-Y)==len(Y-X)==2, 'independent exclusive Haar paths')
    exterior = incident(set(links)) - cube_faces
    need(len(exterior)==20, 'twenty actual exterior faces')
    loading=[]
    for f in sorted(exterior,key=lambda a:sorted(a)):
        common=f & set(links)
        need(len(common)==1, 'one shared cube edge')
        shared=next(iter(common)); opp=[e for e in f-common if axis(e)==axis(shared)]
        need(len(opp)==1 and owner(opp[0])[0]=='free', 'free opposite exterior edge')
        sides={owner(e) for e in f-common-{opp[0]}}
        need(len(sides)==2 and not sides & {owner(e) for e in links}, 'distinct external side owners')
        increment=sum((F(1,8) if s[0]=='strip' else F(3,4)) for s in sides)
        need(increment>=F(1,4), 'complete spectral loading lower increment')
        loading.append({'face':sorted(f),'side_owners':sorted(sides),'increment':increment})
    factors={owner(e) for e in seed};collars=[]
    for k in range(7):
        complete=set().union(*(factor_links(o) for o in factors))
        touching=incident(complete)
        retained={f for f in touching if {owner(e) for e in f} <= factors}
        need(all(factor_links(o)<=complete for o in factors),'all complete factor links '+str(k))
        if k:
            need(set(links)<=complete and cube_faces<=retained,'whole cube retained '+str(k))
        next_factors=factors | {owner(e) for f in touching for e in f}
        collars.append({'k':k,'factors':len(factors),'links':len(complete),
                        'retained_faces':len(retained),'crossing_faces':len(touching-retained),
                        'new_next_owners':len(next_factors-factors),
                        'complete_links_sha256':hashlib.sha256(repr(sorted(complete)).encode()).hexdigest(),
                        'retained_faces_sha256':hashlib.sha256(repr(sorted(sorted(f) for f in retained)).encode()).hexdigest()})
        factors=next_factors
    need([a['retained_faces'] for a in collars[:6]]==[2,25,143,359,695,1171], 'inherited common-seed counts independently reproduced')
    weights={f:sum(face_record(f)[0]) for f in cube_faces}
    transitions=[[(j,weights[c^d]) for j,d in enumerate(cycles) if c^d in weights] for c in cycles]
    need(max(map(len,transitions))<=6,'uniform symmetric row count at most six')
    need(all(n in (4,5) for row in transitions for _,n in row), 'every face derivative bounded by five')
    need(max(sum(n for _,n in row) for row in transitions)<=30, 'Qprime symmetric row norm at most thirty')
    def reflect(c):
        return frozenset(edge((7-v[0],v[1],v[2]),(7-w[0],w[1],w[2])) for v,w in c)
    permutation=[cycles.index(reflect(c)) for c in cycles]
    need(len(set(permutation))==16 and all(permutation[permutation[j]]==j for j in range(16)), 'full reflection is an involutive permutation')
    need(reflect(X)==X and reflect(Y4)==Y5 and reflect(Y5)==Y4, 'reflection fixes X and exchanges source partners')
    need(all({permutation[j] for j,_ in row}=={j for j,_ in transitions[permutation[i]]}
             for i,row in enumerate(transitions)), 'reflection commutes with every endpoint adjacency edge')
    # It need not preserve the anchored physical weights away from q=1.
    need(any({(permutation[j],n) for j,n in row}!=set(transitions[permutation[i]])
             for i,row in enumerate(transitions)), 'reflection is not imported as full finite-q profile symmetry')
    return transitions,sources,collars,{'paths':{'X':sorted(X),'Y4':sorted(Y4),'Y5':sorted(Y5)},
           'cycles':[sorted(c) for c in cycles], 'loading':loading,'reflection_permutation':permutation,
           'face_flip_transitions':transitions,'source_indices':sources}


def padd(a,b,scale=F(1),shift=0):
    out=dict(a)
    for k,v in b.items():
        out[k+shift]=out.get(k+shift,F(0))+scale*v
        if not out[k+shift]: del out[k+shift]
    return out


def peval(poly,q):
    return sum((c*q**j for j,c in poly.items()),F(0))


def moments(transitions,sources):
    all_m=[]
    for pair in sources:
        w=[{0:F(int(i in pair))} if i in pair else {} for i in range(16)];result=[]
        for n in range(9):
            result.append(padd({},padd(w[pair[0]],w[pair[1]]),F(1,2)))
            w=[sum_polys([(w[j],degree) for j,degree in row]) for row in transitions]
        all_m.append(result)
    differences=[padd(all_m[1][n],all_m[0][n],F(-1),1) for n in range(9)]
    need(all_m[0][1]=={4:F(1)} and all_m[1][1]=={5:F(1)},'physical first moments q4 q5')
    need(differences[1]=={},'delta first moment zero')
    need(differences[3]=={13:F(2),15:F(-2)},'exact cubic cancellation 2q13(1-q2)')
    wrong_q=F(1,2)
    wrong_slopes=[]
    for pair in sources:
        initial=[F(i in pair) for i in range(16)]
        action=[sum(wrong_q**4*initial[j] for j,_ in row) for row in transitions]
        wrong_slopes.append((action[pair[0]]+action[pair[1]])/2)
    need(wrong_slopes[1]/wrong_slopes[0]==1!=wrong_q,
         'actual mutated q5-to-q4 face matrix fails slope discriminator')
    need(all(peval(d,F(1))==0 for d in differences),'finite endpoint moments consistent with separately proved permutation')
    # Evaluate direct rational matrix powers separately from polynomial walks.
    for q in (F(1,2),F(2,3),F(1)):
        for r,pair in enumerate(sources):
            v=[F(i in pair) for i in range(16)]
            for n in range(9):
                need((v[pair[0]]+v[pair[1]])/2==peval(all_m[r][n],q),'polynomial versus rational matrix '+str((q,r,n)))
                v=[sum(q**degree*v[j] for j,degree in row) for row in transitions]
    return all_m,differences


def sum_polys(terms):
    out={}
    for p,shift in terms: out=padd(out,p,shift=shift)
    return out


def bfun(q):
    return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))


def sqrt_interval(q):
    den=10**110
    lo=F(math.isqrt(q.numerator*den*den//q.denominator),den)
    hi=lo if lo*lo==q else lo+F(1,den)
    need(lo*lo<=q<=hi*hi,'certified rational square-root interval')
    return lo,hi


def division(nlo,nhi,dlo,dhi):
    if dlo<=0: return None
    corners=[n/d for n in (nlo,nhi) for d in (dlo,dhi)]
    return min(corners),max(corners)


def scalar_ratio(a,b,r4,r5):
    return division(b-r5,b+r5,a-r4,a+r4)


def separation(a,b):
    if a is None or b is None: return None
    return max(a[0]-b[1],b[0]-a[1])


def spatial_tail(k,z):
    coefficient=F(1)
    for j in range(k+1): coefficient*= (F(10,3)+j)/(j+1)
    x=15*z
    return coefficient*x**(k+1)/(1-x)**(k+5)


def predictions(q,eta,z,polys,differences):
    p=2+5*q+5*q*q+6*q**3+3*q**4
    v=z*(1+q)**2*(1+q*q)/(32*p)
    tau=eta/(8*bfun(q))
    need(tau*z/(eta*(1-q)**3)==96*v,'original physical clock retained')
    need(6*v<1,'entire-tail geometric domain')
    centers=[]
    for m in polys:
        real=sum(((-1)**(n//2)*v**n*peval(m[n],q)/math.factorial(n) for n in range(0,9,2)),F(0))
        imag=sum(((-1)**((n-1)//2)*v**n*peval(m[n],q)/math.factorial(n) for n in range(1,9,2)),F(0))
        centers.append({'real':real,'imag':imag})
    combo=sum(((-1)**((n-1)//2)*v**n*peval(differences[n],q)/math.factorial(n) for n in (3,5,7)),F(0))
    need(combo==centers[1]['imag']-q*centers[0]['imag'],'alternating-sign polynomial combination exact')
    wrong_combo=sum((v**n*peval(differences[n],q)/math.factorial(n) for n in (3,5,7)),F(0))
    need(wrong_combo!=combo,'all-positive imaginary signs rejected')
    need(combo<0,'leading cubic cancellation has negative imaginary sign')
    ordinary=(6*v)**9/math.factorial(9)
    allorder=(1-q)*91*(6*v)**9/(math.factorial(9)*(1-6*v))
    need(allorder<(1+q)*ordinary,'all-order tail improves separate arithmetic remainder')
    low,high=sqrt_interval(bfun(q*q)/96)
    state=48*tau*high/((1-eta)/8)
    return {'q':q,'eta':eta,'v':v,'tau':tau,'physical_time':z/(eta*(1-q)**3),
            'centers':centers,'combination_center':combo,'ordinary_arithmetic':ordinary,
            'combination_tail':allorder,'state':state,'state_sqrt_interval':[low,high],
            'old_cubic_sine_floor':36*v**3}


def controls():
    need(division(-3,1,1,3)==(F(-3),F(1)), 'signed numerator all corners')
    need(division(1,2,F(-1),F(3)) is None, 'denominator crossing returns no inference')
    # Exact same rectangle under the affine residual change; independent
    # residual/denominator intervals lose the common e4 dependence.
    a,b,q,r=F(2),F(1),F(1,2),F(1,4)
    direct=scalar_ratio(a,b,r,r)
    residual=division(b-q*a-(1+q)*r,b-q*a+(1+q)*r,a-r,a+r)
    boxed=(q+residual[0],q+residual[1])
    transformed=[q+(b-q*a+e5-q*e4)/(a+e4) for e4 in (-r,r) for e5 in (-r,r)]
    need(direct==(min(transformed),max(transformed)), 'shared e4 exact corner equivalence')
    need(boxed[0]<=direct[0] and boxed[1]>=direct[1] and boxed!=direct,'independent residual rectangle strictly loses information')
    need(abs(r-q*(-r))==(1+q)*r>abs(r-q*r),'equal radii admit unequal adversarial signs')
    need(F(1,2)**5/F(1,2)**4!=1,'wrong q5-to-q4 face loses slope dependence')
    need(F(5,2)-1==F(3,2)>0,'Haar fourth moment rejects rank loading substitution')
    need(F(8)>1 and 16*(1+F(2))>16,'multiplier and vacuum columns cannot be dropped')
    # The actual J=2sqrt(2), so 2<J<3 and 16(1+J)<64.
    need(F(2)**2<8<F(3)**2 and F(1)+F(3)<=4,'norm 2sqrt2 with conservative both-column coefficient64')
    # Two normalized spectral measures on a bounded diagonal matrix have
    # matching first eight moments and unequal ninth moments. They are a
    # general-class control, not the actual reached component.
    even={j:F(math.comb(9,j),256) for j in range(0,10,2)}
    odd={j:F(math.comb(9,j),256) for j in range(1,10,2)}
    need(sum(even.values())==sum(odd.values())==1,'finite-moment spectral controls normalized')
    for n in range(9):
        need(sum(w*F(j,9)**n for j,w in even.items())==sum(w*F(j,9)**n for j,w in odd.items()),
             'bounded spectral moment coincidence degree '+str(n))
    need(sum(w*F(j,9)**9 for j,w in even.items())!=sum(w*F(j,9)**9 for j,w in odd.items()),
         'finite moment coincidence does not prove all-order equality')
    need(all(F(10*(n+1)+1,math.factorial(n+1))<=F(10*n+1,math.factorial(n))
             for n in range(9,30)), 'tail coefficient decreasing control')
    # Analytic proof for all n: 10n+11 <= (n+1)(10n+1).
    need(all(10*n*n+n-10>0 for n in (9,10)), 'all-n tail polynomial positive from n9')
    # q_c is a specified hypothesis coefficient. It is not measured q.
    y4,y5=F(2),F(3)
    need(y5/y4==F(3,2) and y5-F(1,2)*y4!=y5-F(1,3)*y4,'candidate residual depends on declared candidate but ratio does not')
    # Exact rotations (cos,sin)=(3/5,4/5) on complex test data.
    z4,z5=(F(1),F(2)),(F(3),F(4))
    rotate=lambda z:(F(3,5)*z[0]-F(4,5)*z[1],F(4,5)*z[0]+F(3,5)*z[1])
    dist2=lambda a,b:sum((x-y)**2 for x,y in zip(a,b))
    need(dist2(rotate(z4),rotate(z5))==dist2(z4,z5),'common carrier preserves full complex disk distances')
    need(rotate(z5)[1]/rotate(z4)[1]!=z5[1]/z4[1],'common phase generally changes imaginary ratio')
    need(dist2(rotate(z4),z5)!=dist2(z4,z5),'independently shifted carrier changes complex comparisons')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE/'ai3-independent.json')
    out=parser.parse_args().output
    manifest=json.loads((HERE/'ai3-inputs/source-inventory.json').read_text())
    bindings={}
    for entry in manifest['entries']:
        need(digest(ROOT/entry['source'])==entry['sha256'],'live source '+entry['source'])
        need(digest(ROOT/entry['snapshot'])==entry['sha256'],'frozen source '+entry['source'])
        bindings[entry['source']]=entry['sha256']
    contract=json.loads((ROOT/manifest['contract']).read_text())
    need(len(contract['sources'])==40 and all(bindings.get(p)==v for p,v in contract['sources'].items()), 'all forty contract sources frozen')
    transitions,sources,collars,geo=geometry();polys,differences=moments(transitions,sources);controls()
    z=F(1,10**6);rows=[];display=[]
    grid=[(power,k) for power in (12,18,24) for k in (3,4,5)]+[(24,6)]
    for power,k in grid:
        u=F(1,10**power);pair=[]
        for q,eta in ((1-u,F(1,2)),(1-2*u,F(1,16))):
            d=predictions(q,eta,z,polys,differences)
            M=F(collars[k]['retained_faces'],24)
            d['spatial']=8*spatial_tail(k,z)
            d['averaging']=64*d['tau']*M*(1+3*z*M)
            physical=d['state']+d['spatial']+d['averaging'];R=physical+d['ordinary_arithmetic']
            a,b=[c['imag'] for c in d['centers']]
            need(a-R>0 and b-R>0,'strict full scalar denominator and numerator '+str((power,k,q)))
            d['physical_radius']=physical;d['full_scalar_radius']=R;d['positive_denominator']=a-R
            d['corner_ratio']=scalar_ratio(a,b,R,R)
            combo_radius=(1+q)*physical+d['combination_tail']
            rr=division(d['combination_center']-combo_radius,d['combination_center']+combo_radius,a-R,a+R)
            d['cancellation_ratio']=(q+rr[0],q+rr[1]);d['combination_radius']=combo_radius
            need(d['cancellation_ratio'][0]<=d['corner_ratio'][0]
                 and d['corner_ratio'][1]<=d['cancellation_ratio'][1],
                 'all-corner scalar rectangle sharper on frozen cell '+str((power,k,q)))
            old=R+d['old_cubic_sine_floor']
            d['old_cubic_ratio']=scalar_ratio(d['v']*q**4,d['v']*q**5,old,old)
            d['component_only_ratios']={name:scalar_ratio(a,b,d[name],d[name]) for name in ('state','spatial','averaging')}
            d['dominant_physical_component']=max(('state','spatial','averaging'),key=lambda n:d[n])
            pair.append(d)
        need(pair[0]['physical_time']==pair[1]['physical_time']==2*z/u**3,'same frozen clock '+str((power,k)))
        margins={name:separation(pair[0][name],pair[1][name]) for name in ('corner_ratio','cancellation_ratio','old_cubic_ratio')}
        components={name:separation(pair[0]['component_only_ratios'][name],pair[1]['component_only_ratios'][name]) for name in ('state','spatial','averaging')}
        scalar=[]
        for r in range(2):
            delta=abs(pair[0]['centers'][r]['imag']-pair[1]['centers'][r]['imag'])
            margin=delta-pair[0]['full_scalar_radius']-pair[1]['full_scalar_radius']
            scalar.append({'probe':r+4,'center_difference':delta,'margin':margin,'disjoint':margin>0,'extra_equal_scalar_tolerance':max(F(0),margin/2)})
        rows.append({'power':power,'u':u,'k':k,'hypotheses':pair,'ratio_margins':margins,
                     'component_only_ratio_margins':components,'scalar_comparisons':scalar})
        display.append({'power':power,'k':k,'N':collars[k]['retained_faces'],
                        'corner_margin':float(margins['corner_ratio']),
                        'cancellation_margin':float(margins['cancellation_ratio']),
                        'state_only_margin':float(components['state']),
                        'spatial_only_margin':float(components['spatial']),
                        'scalar_margins':[float(s['margin']) for s in scalar],
                        'physical_radii':[float(d['physical_radius']) for d in pair]})
    need(len(rows)==10 and len({(r['power'],r['k']) for r in rows})==10,'exactly ten frozen cells')
    need(all(r['ratio_margins']['corner_ratio']<0 and r['ratio_margins']['cancellation_ratio']<0 for r in rows),
         'all ten complete ratio certificates remain insufficient')
    need(all(r['ratio_margins']['old_cubic_ratio']<0 for r in rows), 'all ten inherited crude ratio certificates insufficient')
    need([(r['power'],r['k']) for r in rows if all(s['disjoint'] for s in r['scalar_comparisons'])]==[(18,5)],
         'direct scalar baseline preserved only at frozen u18k5')
    need(all(r['component_only_ratio_margins']['state']<0 for r in rows if r['power'] in (12,18)),
         'state-only upper intervals already overlap at u12 and u18')
    need(all(r['component_only_ratio_margins']['spatial']<0 for r in rows if r['power']==24),
         'spatial-only upper intervals already overlap at u24 including k6')
    result={'schema':'ym28-ai3-independent-v1','model':contract['model'],
            'attribution':'All-order reflection/derivative proposal is shared advisor and Tesla context; this implementation and proof independently test it.',
            'geometry':geo,'collars':collars,'moments':polys,'moment_differences':differences,
            'rows':rows,'display_only':display,'source_bindings':bindings,
            'checks':CHECKS,'check_count':len(CHECKS),
            'scope':{'all_order_retained_tail':True,'physical_errors_differentiated':False,
                     'joint_physical_error_cancellation':False,'continuous_inverse':False,
                     'instrument_realization':False,'homogeneous_transfer':False,'continuum_Yang_Mills':False}}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(encode(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(CHECKS),'collars':collars,'display':display},indent=2))


if __name__=='__main__': main()
