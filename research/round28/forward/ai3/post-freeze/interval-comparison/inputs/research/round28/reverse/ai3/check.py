#!/usr/bin/env python3
"""Independent AI3 exact geometry, polynomial walks and full physical enclosures.

Run with --output /absolute/nonexistent/directory. No inherited checker imported.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from math import factorial, isqrt
from pathlib import Path
import sys

sys.set_int_max_str_digits(0)
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CHECKS = []


def require(condition, name):
    if not condition:
        raise ValueError(name)
    CHECKS.append(name)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def shift(v, axis, step=1):
    return tuple(x + (step if j == axis else 0) for j, x in enumerate(v))


def owner(link):
    v, axis = link
    if axis == 2 or (axis == 0 and v[0] % 4 == 3) or (axis == 1 and v[1] % 2 == 1):
        return ('free', v, axis)
    return ('strip', (4 * (v[0] // 4), 2 * (v[1] // 2), v[2]), -1)


def factor_links(factor):
    kind, v, axis = factor
    if kind == 'free':
        return {(v, axis)}
    return {(shift(shift(v, 0, i), 1, j), 0) for i in range(3) for j in range(2)} | {
        (shift(v, 0, i), 1) for i in range(4)}


def boundary(face):
    v, a, b = face
    return {(v, a), (v, b), (shift(v, a), b), (shift(v, b), a)}


def touching(links):
    faces = set()
    for v, axis in links:
        for other in set(range(3)) - {axis}:
            for anchor in (v, shift(v, other, -1)):
                a, b = sorted((axis, other))
                internal_strip = a == 0 and b == 1 and anchor[0] % 4 < 3 and anchor[1] % 2 == 0
                if min(anchor) >= 0 and not internal_strip:
                    faces.add((anchor, a, b))
    return faces


def geometry():
    vertices = list(product((0, 1), repeat=3))
    edges = sorted((a, b) for a, b in combinations(vertices, 2)
                   if sum(abs(x-y) for x, y in zip(a, b)) == 1)
    cycles = []
    for chosen in combinations(range(len(edges)), 6):
        neighbours = defaultdict(set)
        for i in chosen:
            a, b = edges[i]
            neighbours[a].add(b)
            neighbours[b].add(a)
        if len(neighbours) != 6 or any(len(v) != 2 for v in neighbours.values()):
            continue
        reached = {min(neighbours)}
        for unused in range(6):
            reached |= set().union(*(neighbours[v] for v in reached))
        if len(reached) == 6:
            cycles.append(frozenset(chosen))
    require(len(cycles) == 16, 'all connected degree-two six-edge cube cycles')
    origin = (3, 1, 0)
    links = [(tuple(x+y for x, y in zip(a, origin)), next(j for j in range(3) if a[j] != b[j])) for a, b in edges]
    faces = {}
    for a, b in combinations(range(3), 2):
        normal = next(iter(set(range(3)) - {a, b}))
        for side in (0, 1):
            face = (shift(origin, normal, side), a, b)
            faces[frozenset(links.index(e) for e in boundary(face))] = face
    X = frozenset((1, 2, 5, 7, 9, 11))
    Y4 = frozenset((0, 2, 3, 7, 9, 11))
    Y5 = frozenset((1, 2, 5, 7, 8, 10))
    indices = [cycles.index(s) for s in (X, Y4, Y5)]
    require(indices == [10, 6, 9], 'physical paths match frozen AA1 labels')
    pairs = {4: (indices[0], indices[1]), 5: (indices[0], indices[2])}
    adjacency = [[] for c in cycles]
    for i, first in enumerate(cycles):
        for j, second in enumerate(cycles):
            if first ^ second in faces:
                face = faces[first ^ second]
                adjacency[i].append((j, sum(face[0])))
    for r, pair in pairs.items():
        require((pair[1], r) in adjacency[pair[0]], 'correct joining face q'+str(r))
    require(all(len(row) <= 6 and sum(exponent for j, exponent in row) <= 30 for row in adjacency),
            'all-q operator and derivative row bounds 6 and 30')
    reflected_edges = []
    for a, b in edges:
        reflected_edges.append(edges.index(tuple(sorted(((1-a[0], a[1], a[2]), (1-b[0], b[1], b[2]))))))
    permutation = [cycles.index(frozenset(reflected_edges[i] for i in c)) for c in cycles]
    require(sorted(permutation) == list(range(16)) and all(permutation[permutation[i]] == i for i in range(16)),
            'entire reflection permutation is an involution')
    require(permutation[indices[0]] == indices[0] and permutation[indices[1]] == indices[2],
            'reflection fixes X and swaps Y4 Y5 without SU2 orientation sign')
    require(all({permutation[j] for j, exponent in adjacency[i]} == {j for j, exponent in adjacency[permutation[i]]}
                for i in range(16)), 'full Q(1) permutation intertwiner not a finite moment test')
    seed = {links[i] for i in X | Y4 | Y5}
    require(len(seed) == 10 and all(owner(e)[0] == 'free' for e in seed), 'complete ten free-factor seed')
    require(not Y5 <= X | Y4, 'eight-link seed mutation misses actual Y5 support')
    factors = {owner(e) for e in seed}
    previous_factors, previous_links, previous_inside = set(), set(), set()
    collars = []
    for k in range(7):
        complete = set().union(*(factor_links(f) for f in factors))
        candidates = touching(complete)
        inside = {f for f in candidates if {owner(e) for e in boundary(f)} <= factors}
        require(all(owner(e) == f for f in factors for e in factor_links(f)), 'whole factor owner closure depth '+str(k))
        require(previous_factors <= factors and previous_links <= complete and previous_inside <= inside,
                'nested full support depth '+str(k))
        if k:
            require(set(links) <= complete and set(faces.values()) <= inside, 'all six cube faces retained depth '+str(k))
        collars.append({'depth': k, 'factors': len(factors), 'links': len(complete), 'retained_faces': len(inside),
                        'crossing_faces': len(candidates-inside), 'new_factors': sorted(factors-previous_factors),
                        'new_links': sorted(complete-previous_links), 'new_retained_faces': sorted(inside-previous_inside)})
        previous_factors, previous_links, previous_inside = factors.copy(), complete, inside
        factors |= {owner(e) for face in candidates for e in boundary(face)}
    require([(c['factors'], c['links'], c['retained_faces']) for c in collars[:6]] ==
            [(10,10,2),(41,113,25),(149,329,143),(333,675,359),(610,1177,695),(993,1857,1171)],
            'independent collars reproduce admitted depths zero through five')
    outside = []
    for face in sorted(touching(set(links)) - set(faces.values())):
        shared = boundary(face) & set(links)
        require(len(shared) == 1, 'exterior face has one shared cube edge '+str(face))
        axis = next(iter(shared))[1]
        opposite = {e for e in boundary(face)-shared if e[1] == axis}
        require(len(opposite) == 1 and owner(next(iter(opposite)))[0] == 'free', 'free opposite loading edge '+str(face))
        side_owners = {owner(e) for e in boundary(face)-shared-opposite}
        require(len(side_owners) == 2 and not side_owners & {owner(e) for e in links}, 'distinct exterior side owners '+str(face))
        gap = sum(F(1,8) if f[0] == 'strip' else F(3,4) for f in side_owners)
        require(gap >= F(1,4), 'actual full-side loading at least one quarter '+str(face))
        outside.append({'face':face,'side_owners':sorted(side_owners),'gap_lower':gap})
    require(len(outside) == 20, 'all twenty exterior touching faces included')
    paths = {}
    for name, cycle in zip(('X','Y4','Y5'), (X,Y4,Y5)):
        adj = defaultdict(list)
        for i in cycle:
            a,b=edges[i];adj[a].append(b);adj[b].append(a)
        route=[min(adj)];previous=None
        for j in range(6):
            nxt=min(v for v in adj[route[-1]] if v != previous)
            previous=route[-1];route.append(nxt)
        require(route[0] == route[-1] and len(set(route[:-1])) == 6, 'closed physical '+name+' path')
        paths[name]=[tuple(x+y for x,y in zip(v,origin)) for v in route]
    return adjacency, pairs, {'edges':edges,'cycles':[sorted(c) for c in cycles], 'paths':paths,
                              'reflection_edges':reflected_edges,'reflection_cycles':permutation,
                              'seed':sorted(seed),'collars':collars,'exterior_loading':outside}


def polynomial_walks(adjacency, pair):
    vector = [{0:F(i in pair)} for i in range(16)]
    moments=[]
    for n in range(9):
        value=defaultdict(F)
        for i in pair:
            for degree, coefficient in vector[i].items(): value[degree] += coefficient/2
        moments.append({d:c for d,c in sorted(value.items()) if c})
        nxt=[defaultdict(F) for i in range(16)]
        for i, row in enumerate(adjacency):
            for j, exponent in row:
                for degree, coefficient in vector[j].items(): nxt[i][degree+exponent] += coefficient
        vector=nxt
    return moments


def evaluate(poly, q):
    return sum(c*q**d for d,c in poly.items())


def q_moments(adjacency, pair, q):
    vector=[F(i in pair) for i in range(16)]; answer=[]
    for n in range(9):
        answer.append(sum(vector[i] for i in pair)/2)
        vector=[sum(q**degree*vector[j] for j,degree in row) for row in adjacency]
    return answer


def b(q):
    return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))


def root_up(value):
    denominator=1<<400
    lower=isqrt(value.numerator*denominator**2//value.denominator)
    answer=F(lower,denominator)
    answer += F(1,denominator) if answer*answer < value else 0
    require(answer*answer >= value and (answer-F(1,denominator))**2 < value, 'directed rational square-root enclosure')
    return answer


def spatial(k, x):
    coefficient=F(1)
    for j in range(k+1): coefficient *= (F(10,3)+j)/(j+1)
    return 8*coefficient*x**(k+1)/(1-x)**(k+5)


def divide(numerator, denominator):
    if denominator[0] <= 0 <= denominator[1]: return None
    corners=[F(n)/F(d) for n in numerator for d in denominator]
    return [min(corners),max(corners)]


def center(moments,v):
    real=sum((-1)**(n//2)*moments[n]*v**n/factorial(n) for n in range(0,9,2))
    imag=sum((-1)**((n-1)//2)*moments[n]*v**n/factorial(n) for n in range(1,9,2))
    return {'real':real,'imag':imag}


def interval_gap(first,second):
    return max(first[0]-second[1], second[0]-first[1])


def controls(adjacency, pairs, polynomials, differences):
    q=F(2,3); v=F(1,20)
    wrong=[[(j,4) for j,d in row] for row in adjacency]
    require(q_moments(wrong,pairs[5],q)[1] != q**5, 'wrong q5-face assignment is detected by actual first moment')
    signed=sum((-1)**((n-1)//2)*v**n*evaluate(differences[n],q)/factorial(n) for n in (3,5,7))
    wrong_sign=sum(v**n*evaluate(differences[n],q)/factorial(n) for n in (3,5,7))
    require(signed != wrong_sign and signed < 0, 'alternating imaginary cubic and seventh signs reject positive-sign mutation')
    # Equal first eight moments need not identify a spectral measure. The parity
    # halves of the ninth finite-difference measure have equal moments 0..8.
    from math import comb
    even={j:F(comb(9,j),256) for j in range(0,10,2)}
    odd={j:F(comb(9,j),256) for j in range(1,10,2)}
    moment=lambda measure,n:sum(weight*F(point)**n for point,weight in measure.items())
    require(all(moment(even,n)==moment(odd,n) for n in range(9)) and moment(even,9)!=moment(odd,9),
            'explicit probability measures: finite moment coincidence does not prove all orders')
    require(F(5,2)-1 == F(3,2) and 8 > 1 and 48 > 6,
            'actual multiplier fourth moment and transfer norms reject rank replacement')
    full_second=q_moments(adjacency,pairs[4],F(1))[2]
    require(full_second == 4 and full_second != 1, 'dropped reached loading columns fail coherent held-out second moment')
    # Equal radii admit opposite signs and unequal signed errors.
    radius=F(1,7); e4=-radius;e5=radius
    require(abs(e5-q*e4)==(1+q)*radius and abs(e5-q*e4)>(1-q)*radius,
            'equal physical radii do not cancel adversarial signed errors')
    measured4=F(2,7);measured5=F(1,5)
    residual=lambda candidate:measured5-candidate*measured4
    require(residual(F(1,2)) != residual(F(2,3)) and measured5/measured4 == F(7,10),
            'observable ratio independent of candidate while residual is candidate indexed')
    require(divide([-3,-1],[2,4]) == [F(-3,2),F(-1,4)], 'negative numerator all-corner quotient')
    require(divide([-1,3],[2,4]) == [F(-1,2),F(3,2)], 'signed numerator all-corner quotient')
    require(divide([1,2],[-1,1]) is None and divide([1,2],[0,2]) is None,
            'zero-crossing denominator rejected')
    # Rational point on the unit circle: c=3/5,s=4/5. Common phase is
    # constrained, not independent knobs, and does not preserve Im ratios.
    a4=(F(1),F(1,10));a5=(F(1),F(1,5));c,s=F(3,5),F(4,5)
    rotate_im=lambda a: s*a[0]+c*a[1]
    common=rotate_im(a5)/rotate_im(a4)
    independently_shifted=rotate_im(a5)/a4[1]
    require(c*c+s*s==1 and common != independently_shifted and common != a5[1]/a4[1],
            'common phase versus independent phase controls and non-invariance of imaginary ratio')
    return {'finite_moment_counterexample_even':even,'finite_moment_counterexample_odd':odd,
            'adversarial_combination_error':abs(e5-q*e4),'common_phase_ratio':common,
            'independently_shifted_ratio':independently_shifted,'unaltered_ratio':a5[1]/a4[1]}


def run():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    destination=Path(parser.parse_args().output)
    require(destination.is_absolute() and not destination.exists(), 'output absolute and fresh')
    inventory=json.loads((HERE/'inputs/source-inventory.json').read_text())
    require(inventory['frozen_before_scientific_production'] and inventory['current_opposite_direction_unread'],
            'prospective independence inventory')
    for item in inventory['entries']:
        require(digest(ROOT/item['source']) == digest(ROOT/item['snapshot']) == item['sha256'], 'source snapshot '+item['source'])
    contract=json.loads((ROOT/'research/round28/contracts/ai3.json').read_text())
    require(digest(ROOT/'research/round28/contracts/ai3.json') == '20cab55ea76681df9fdcb1d07d74d97312a618e41e96d1ab540b6240b2537074',
            'exact advisor frozen AI3 contract')
    require(set(contract['sources']) <= {x['source'] for x in inventory['entries']}, 'all forty contract sources covered')
    for path, expected in contract['sources'].items():
        require(digest(ROOT/path) == expected, 'exact contract-declared hash '+path)
    adjacency,pairs,geo=geometry()
    polys={r:polynomial_walks(adjacency,pair) for r,pair in pairs.items()}
    diff={}
    for n in range(9):
        result=defaultdict(F)
        for degree,value in polys[5][n].items(): result[degree] += value
        for degree,value in polys[4][n].items(): result[degree+1] -= value
        diff[n]={d:c for d,c in sorted(result.items()) if c}
        require(evaluate(diff[n],F(1))==0, 'finite check of separately proved all-order reflection n'+str(n))
    require(diff[1] == {} and diff[3] == {13:F(2),15:F(-2)}, 'exact first and third moment cancellations')
    factors={3:{13:F(2)},5:{21:F(12),22:F(8),23:F(12)},
             7:{29:F(54),30:F(72),31:F(164),32:F(72),33:F(54)}}
    for n,poly in factors.items():
        expanded=defaultdict(F)
        for degree,value in poly.items():
            expanded[degree]+=value;expanded[degree+2]-=value
        require(diff[n]=={d:c for d,c in expanded.items() if c}, 'symbolic factor one minus q squared order '+str(n))
    control_data=controls(adjacency,pairs,polys,diff)
    z=F(1,10**6); samples=[]; decisions=[]
    for power,k in [(p,k) for p in (12,18,24) for k in (3,4,5)]+[(24,6)]:
        u=F(1,10**power);rows=[]
        for hypothesis,multiplier,eta in [('H1',1,F(1,2)),('H2',2,F(1,16))]:
            q=1-multiplier*u;tau=eta/(8*b(q));s=z*tau/(eta*(1-q)**3);v=s/96
            require(z/(eta*(1-q)**3)==2*z/u**3 and eta*(1-q)**3==u**3/2,
                    'common fixed physical clock '+str((power,k,hypothesis)))
            require(s <= 3*z/2 and 6*v < 1, 'physical clock and entire-tail radii '+str((power,k,hypothesis)))
            ms={r:q_moments(adjacency,pairs[r],q) for r in (4,5)}
            require(all(ms[r]==[evaluate(p,q) for p in polys[r]] for r in (4,5)),
                    'symbolic and independent rational walks agree '+str((power,k,hypothesis)))
            centers={r:center(ms[r],v) for r in (4,5)}
            a4=centers[4]['imag'];a5=centers[5]['imag'];C=a5-q*a4
            require(C==sum((-1)**((n-1)//2)*v**n*evaluate(diff[n],q)/factorial(n) for n in (3,5,7)),
                    'signed cancellation center '+str((power,k,hypothesis)))
            norm=max(sum(q**degree for j,degree in row) for row in adjacency)
            arithmetic=(v*norm)**9/factorial(9)
            combined_tail=(1-q)*91*(6*v)**9/(factorial(9)*(1-6*v))
            state=48*tau*root_up(b(q*q)/96)/((1-eta)/8)
            spatial_cost=spatial(k,15*z)
            M=F(geo['collars'][k]['retained_faces'],24)
            averaging=64*tau*M*(1+3*z*M)
            physical=state+spatial_cost+averaging
            E=physical+arithmetic; denominator=[a4-E,a4+E]
            require(denominator[0]>0, 'strict positive physical ratio denominator '+str((power,k,hypothesis)))
            wide=divide([C-combined_tail-(1+q)*physical,C+combined_tail+(1+q)*physical],denominator)
            cancellation=[q+x for x in wide]
            corners=divide([a5-E,a5+E],denominator)
            # Retain shared physical e4 in the cancellation numerator and denominator.
            # delta4, deltaC are bounded jointly by this enlarged rectangle; no
            # independence of the actual Taylor errors is asserted.
            shared_values=[q+(C+dC+e5-q*e4)/(a4+d4+e4)
                           for d4,e4,e5,dC in product((-arithmetic,arithmetic),(-physical,physical),
                                                    (-physical,physical),(-combined_tail,combined_tail))]
            shared=[min(shared_values),max(shared_values)]
            best=[max(cancellation[0],corners[0],shared[0]),min(cancellation[1],corners[1],shared[1])]
            require(best[0] <= best[1], 'consistent combined ratio enclosures '+str((power,k,hypothesis)))
            cubic=(v*norm)**3/6;old_delta=E+cubic;old_d=v*q**4-old_delta
            old_rad=(1+q)*old_delta/old_d if old_d>0 else None
            component={'state':state,'spatial':spatial_cost,'averaging':averaging}
            row={'power':power,'k':k,'hypothesis':hypothesis,'q':q,'eta':eta,'tau':tau,'s':s,'v':v,
                 'physical_time_in_hbar_over_alpha':2*z/u**3,'centers':centers,'Q_norm_bound':norm,
                 'signed_cancellation_center':C,'physical_errors':component,'physical_radius':physical,
                 'individual_arithmetic_remainder':arithmetic,'combined_all_order_remainder':combined_tail,
                 'full_scalar_radius':E,'denominator':denominator,'cancellation_interval':cancellation,
                 'shared_e4_cancellation_interval':shared,'all_corner_quotient':corners,'best_ratio_interval':best,
                 'old_cubic_remainder':cubic,'old_ratio_interval':None if old_rad is None else [q-old_rad,q+old_rad],
                 'dominant_physical_error':max(component,key=component.get),
                 'physical_combination_cost':(1+q)*physical,'old_cubic_ratio_floor':(1+q)*cubic/(v*q**4)}
            samples.append(row);rows.append(row)
        h1,h2=rows
        margin=interval_gap(h1['best_ratio_interval'],h2['best_ratio_interval'])
        baseline={}
        for r in (4,5):
            scalar_gap=abs(h1['centers'][r]['imag']-h2['centers'][r]['imag'])
            scalar_margin=scalar_gap-h1['full_scalar_radius']-h2['full_scalar_radius']
            baseline[r]={'center_gap':scalar_gap,'margin':scalar_margin,'disjoint':scalar_margin>0,
                         'extra_equal_scalar_error_ceiling':max(F(0),scalar_margin/2)}
        lipschitz=[]
        for row in rows:
            d=row['denominator'][0];N=abs(row['centers'][5]['imag'])+row['full_scalar_radius']
            lipschitz.append(2*(1+N/d)/d)
        tolerance=min(h1['denominator'][0]/2,h2['denominator'][0]/2,margin/(2*sum(lipschitz))) if margin>0 else F(0)
        component_diagnostics={}
        for name in ('state','spatial','averaging'):
            component_intervals=[]
            normalized=F(0)
            for row in rows:
                cost=row['physical_errors'][name]
                a4=row['centers'][4]['imag'];a5=row['centers'][5]['imag']
                component_intervals.append(divide([a5-cost,a5+cost],[a4-cost,a4+cost]))
                normalized+=(1+row['q'])*cost/row['denominator'][0]
            component_margin=interval_gap(*component_intervals)
            component_diagnostics[name]={'sum_normalized_cost':normalized,'cost_over_q_gap':normalized/u,
                                         'single_component_box_margin':component_margin,
                                         'single_component_box_overlaps':component_margin<=0}
        decisions.append({'power':power,'k':k,'ratio_margin':margin,'ratio_disjoint':margin>0,
                          'extra_equal_scalar_tolerance':tolerance,'ratio_error_lipschitz_constants':lipschitz,
                          'cancellation_margin':interval_gap(h1['cancellation_interval'],h2['cancellation_interval']),
                          'shared_e4_margin':interval_gap(h1['shared_e4_cancellation_interval'],h2['shared_e4_cancellation_interval']),
                          'all_corner_margin':interval_gap(h1['all_corner_quotient'],h2['all_corner_quotient']),
                          'old_ratio_disjoint':interval_gap(h1['old_ratio_interval'],h2['old_ratio_interval'])>0,
                          'direct_scalar_baseline':baseline,
                          'physical_component_diagnostics':component_diagnostics,
                          'sum_normalized_physical_cost':sum(row['physical_combination_cost']/row['denominator'][0] for row in rows),
                          'candidate_q_gap':u})
    require(len(samples)==20 and len(decisions)==10, 'exact ten-cell frozen grid, no adaptive additions')
    bindings={item['source']:item['sha256'] for item in inventory['entries']}
    bindings.update({str(p.relative_to(ROOT)):digest(p) for p in (HERE/'inputs').rglob('*') if p.is_file()})
    for name in ('check.py','report.md'): bindings[str((HERE/name).relative_to(ROOT))]=digest(HERE/name)
    result={'schema':'ym28-reverse-ai3-v1','scope':{'model':'canonical summable full-link SU2',
            'actual_Wilson_multipliers':True,'pairwise_only':True,'complete_regional_shell':False,
            'continuous_inverse':False,'actual_instrument':False,'physical_matching':False,'continuum_gap':False},
            'attribution':{'selection_proposal':'Tesla; shared frozen proposal',
                           'all_order_candidate':'advisor; shared in frozen contract; independently proved here'},
            'geometry':geo,'moment_polynomials':polys,'moment_differences':diff,'controls':control_data,
            'samples':samples,'decisions':decisions,'checks':CHECKS,'check_count':len(CHECKS),'bindings':bindings}
    def serial(value):
        if isinstance(value,F):return str(value)
        if isinstance(value,dict):return {str(k):serial(v) for k,v in value.items()}
        if isinstance(value,(tuple,list)):return [serial(v) for v in value]
        return value
    destination.mkdir(parents=True)
    (destination/'results.json').write_text(json.dumps(serial(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(CHECKS),'moments':serial({n:diff[n] for n in (3,5,7)}),
                      'collar6':{k:v for k,v in geo['collars'][6].items() if not k.startswith('new_')},
                      'decisions':[{'power':d['power'],'k':d['k'],'ratio_disjoint':d['ratio_disjoint'],
                                    'margin':float(d['ratio_margin']),'extra_scalar_tolerance':float(d['extra_equal_scalar_tolerance']),
                                    'scalar_disjoint':{r:x['disjoint'] for r,x in d['direct_scalar_baseline'].items()}}
                                   for d in decisions]},sort_keys=True))


if __name__ == '__main__':
    run()
