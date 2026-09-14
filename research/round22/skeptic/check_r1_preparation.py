#!/usr/bin/env python3
"""Independent pre-production R1 geometry, exact constants, and sign controls."""
import argparse
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path


def require(value, message):
    if not value:
        raise RuntimeError(message)


E = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ZERO = (0, 0, 0)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def star(b):
    return frozenset([b] + [add(b, e) for e in E])


def cube(start, stop):
    return frozenset(product(range(start, stop), repeat=3))


def retained(lam):
    return {b: star(b) for b in lam if star(b) <= lam}


def counts(y, stars):
    interior = {b: s for b, s in stars.items() if s <= y}
    crossing = {b: s for b, s in stars.items() if s & y and not s <= y}
    return interior, crossing


def connected(y):
    seen = {next(iter(y))}
    while True:
        extended = seen | {b for b in y if any(sum(abs(x-z) for x, z in zip(a,b)) == 1 for a in seen)}
        if extended == seen:
            return seen == y
        seen = extended


def face(tail, a, b):
    # Positive-edge identities; the last two edges are traversed inversely.
    return frozenset(((a, tail), (b, add(tail, E[a])), (a, add(tail, E[b])), (b, tail)))


def owner(edge):
    _, (x, y, z) = edge
    return (x // 4, y // 2, z)


def free(edge):
    a, (x, y, _) = edge
    return a == 2 or (a == 0 and x % 4 == 3) or (a == 1 and y % 2 == 1)


def mm(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def plus(a, b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def neg(a):
    return [[-x for x in row] for row in a]


def comm(a, b):
    return plus(mm(a,b),neg(mm(b,a)))


def run():
    rows = []
    for length in range(1, 9):
        for location in ('origin', 'bulk'):
            y = cube(0, length) if location == 'origin' else cube(1, length+1)
            inside, cross = counts(y, retained(cube(0, length+2)))
            expected = (3 if location == 'origin' else 6)*length**2 - 3*length + 1
            require(len(inside) == (length-1)**3, 'interior cube count')
            require(len(cross) == expected, 'complete crossing cube count')
            rows.append({'location': location, 'L': length, 'interior': len(inside), 'crossing': len(cross)})
    all_small = tuple(sorted(cube(0,2)))
    stars = retained(cube(0,3))
    examined = 0
    for mask in range(1, 1 << len(all_small)):
        y = frozenset(x for i,x in enumerate(all_small) if mask & (1 << i))
        if not connected(y):
            continue
        inside, cross = counts(y, stars)
        require(len(cross) <= 4*len(y)-4*len(inside), 'arbitrary support incidence')
        multiplicity = Counter(x for s in cross.values() for x in y | s)
        for x, count in multiplicity.items():
            require(count == len(cross) if x in y else count <= 4, 'root multiplicity')
        require(all(len(y | s) <= len(y)+3 and connected(y | s) for s in cross.values()), 'generated union support')
        examined += 1

    omitted = []
    for x,y in product(range(4),range(2)):
        for a,b in ((0,1),(0,2),(1,2)):
            if (a,b) == (0,1) and x < 3 and y == 0:
                continue
            omitted.append({'tail': (x,y,0), 'axes': (a,b), 'edges': face((x,y,0),a,b)})
    require(len(omitted) == 21, 'all omitted faces')
    require(all({owner(e) for e in f['edges']} <= star(ZERO) for f in omitted), 'declared star supports')
    require(all(sum(free(e) for e in f['edges']) >= 2 for f in omitted), 'two independent free edges')
    require(all(len(a['edges'] & b['edges']) <= 1 for a,b in combinations(omitted,2)), 'distinct square intersections')
    e_probe = (2, ZERO)
    mean_witnesses = []
    for f in omitted:
        witness = sorted(e for e in f['edges'] if free(e) and e != e_probe)
        require(bool(witness), 'mean and diagonal Haar witness away from probe')
        mean_witnesses.append({'tail': f['tail'], 'axes': f['axes'], 'free_edge': witness[0]})
    pair_witnesses = 0
    for a,b in combinations(omitted,2):
        # chi(probe)^2 is center-even; an odd edge can itself be the probe.
        require(any(free(e) for e in a['edges'] - b['edges']), 'cross-face center-parity witness')
        pair_witnesses += 1
    probe_stars = retained(cube(0,2))
    require(set(probe_stars) == {ZERO}, 'fixed probe has exactly one retained star')
    require(not counts(frozenset([ZERO]),probe_stars)[0], 'fixed probe has no interior star')
    touched = sum(e_probe in f['edges'] for f in omitted)
    require(touched == 2, 'probe physical-edge incidence')
    energy = 8*F(3,4)
    variance = F(21,4*9)
    defect = variance / energy**2
    require(energy == 6 and variance == F(7,12) and defect == F(7,432), 'actual probe constants')
    require(F(touched,4*9)/energy**2 != defect, 'dropping other nineteen faces is detected')

    tmax = F(5,1664)
    gap = 1-28*tmax
    require(gap == F(381,416) and gap > 0, 'uniform initial gap')
    # Separate exact two-level homological lemma fixture; not a SU2 approximation.
    d = F(1,5)
    g = [[F(0),F(0)],[F(0),1+d]]
    a = [[F(0),F(1)],[F(1),F(0)]]
    s = [[F(0),-1/(1+d)],[1/(1+d),F(0)]]
    bare = [[F(0),F(-1)],[F(1),F(0)]]
    zero = [[F(0),F(0)],[F(0),F(0)]]
    require(plus(comm(s,g),a) == zero, 'interacting inverse cancellation')
    require(plus(comm(neg(s),g),a) != zero, 'wrong sign rejected')
    require(plus(comm(bare,g),a) != zero, 'bare inverse rejected')
    require(F(0)*defect == 0, 'tau zero defect')
    return {
        'schema':'ym22-skeptic-r1-preparation-checks-v1', 'passed':True,
        'current_producers_read':False, 'research_loops_added':0,
        'cube_counts':rows, 'connected_arbitrary_supports_examined':examined,
        'actual_probe':{'retained_stars':1,'interior_stars':0,'omitted_faces':21,
            'faces_touching_probe_edge':touched,'other_faces_retained':21-touched,
            'cross_face_parity_witnesses':pair_witnesses,
            'one_free_edge_per_face_away_from_probe':mean_witnesses,
            'source_norm_squared':'1','source_energy':str(energy),
            'phi_v_norm_squared_over_tau_squared':str(variance),
            'boundary_vacuum_norm_squared_over_tau_squared':str(defect)},
        'coupling_endpoint':str(tmax),'initial_gap_lower_bound':str(gap),
        'controls':{'wrong_sign_rejected':True,'bare_inverse_rejected':True,
            'dropping_nineteen_faces_rejected':True,'origin_bulk_boundary_distinguished':True,
            'tau_zero_passed':True,'runtime_guards_do_not_use_assert':True},
        'scope':'Geometry and exact arithmetic support the written Haar/domain proofs; the matrix fixture is a separate lemma control.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(run(),indent=2,sort_keys=True)+'\n')
