#!/usr/bin/env python3
"""External exact audit. Imports no producer or advisor implementation.

The polynomial checks establish finite algebraic identities. Operator-domain,
spectral and infinite-volume implications are reviewed separately in report.md.
"""
from fractions import Fraction as Q
from itertools import product
from math import factorial
from pathlib import Path
from collections import defaultdict
import argparse
import hashlib
import json

ZERO = (0,) * 12


def const(c):
    return {ZERO: Q(c)} if c else {}


def var(j):
    e = list(ZERO)
    e[j] = 1
    return {tuple(e): Q(1)}


def add(*polys):
    result = {}
    for p in polys:
        for e, c in p.items():
            result[e] = result.get(e, Q(0)) + c
    return {e: c for e, c in result.items() if c}


def scale(c, p):
    return {e: Q(c) * v for e, v in p.items() if c * v}


def mul(p, q):
    result = {}
    for e, a in p.items():
        for f, b in q.items():
            k = tuple(x + y for x, y in zip(e, f))
            result[k] = result.get(k, Q(0)) + a * b
    return {e: c for e, c in result.items() if c}


def derivative(p, j):
    result = {}
    for e, c in p.items():
        if e[j]:
            f = list(e)
            f[j] -= 1
            result[tuple(f)] = c * e[j]
    return result


def reduce_spheres(p):
    """Reduce modulo each fourth-coordinate sphere relation; exact polynomial division."""
    for j in (3, 7, 11):
        result = {}
        work = dict(p)
        while work:
            e, c = work.popitem()
            if e[j] < 2:
                result = add(result, {e: c})
                continue
            f = list(e)
            f[j] -= 2
            remainder = {tuple(f): c}
            for k in range(j - 3, j):
                g = list(f)
                g[k] += 2
                remainder = add(remainder, {tuple(g): -c})
            work = add(work, remainder)
        p = result
    return p


def haar(p):
    """Product S3 Haar moments using the exact isotropic even-moment formula."""
    total = Q(0)
    for e, c in p.items():
        if any(k % 2 for k in e):
            continue
        moment = Q(1)
        for start in (0, 4, 8):
            exponents = e[start:start + 4]
            degree = sum(exponents) // 2
            for k in exponents:
                for j in range(1, k, 2):
                    moment *= j
            for j in range(degree):
                moment /= 4 + 2 * j
        total += c * moment
    return total


def polynomial_audit():
    coordinates = [var(j) for j in range(12)]
    x, y, z = coordinates[0], coordinates[4], coordinates[8]
    w = add(*(mul(coordinates[j], coordinates[j + 4]) for j in range(4)))
    t = add(*(mul(coordinates[j + 4], coordinates[j + 8]) for j in range(4)))
    r = add(*(mul(coordinates[j], coordinates[j + 8]) for j in range(4)))
    action = add(scale(3, x), y, z, w, t)
    gamma, laplacian = {}, {}
    for start in (0, 4, 8):
        for i in range(start, start + 4):
            di = derivative(action, i)
            gamma = add(gamma, scale(Q(1, 4), mul(di, di)))
            laplacian = add(laplacian, scale(Q(1, 4), derivative(di, i)),
                            scale(Q(-3, 4), mul(coordinates[i], di)))
            for j in range(start, start + 4):
                xixj = mul(coordinates[i], coordinates[j])
                gamma = add(gamma, scale(Q(-1, 4), mul(xixj, mul(di, derivative(action, j)))))
                laplacian = add(laplacian, scale(Q(-1, 4), mul(xixj, derivative(di, j))))
    gamma_claim = scale(Q(1, 4), add(const(15), scale(8, y), scale(2, x),
        scale(2, z), scale(2, r), scale(-1, mul(add(scale(3, x), w), add(scale(3, x), w))),
        scale(-1, mul(add(y, w, t), add(y, w, t))), scale(-1, mul(add(z, t), add(z, t)))))
    lap_claim = scale(Q(-3, 4), add(scale(3, x), y, z, scale(2, w), scale(2, t)))
    if reduce_spheres(add(gamma, scale(-1, gamma_claim))):
        raise ValueError('global Gamma identity failed')
    if reduce_spheres(add(laplacian, scale(-1, lap_claim))):
        raise ValueError('global Laplacian identity failed')
    if haar(action) != 0 or haar(mul(action, action)) != Q(13, 4) or haar(gamma) != Q(45, 16):
        raise ValueError('Haar normalization failed')
    # Taylor upper bound independent degree. Remaining ratios <= x/(n+2).
    q, n = Q(3, 2), 20
    lower = sum((q ** j / factorial(j) for j in range(n + 1)), Q(0))
    upper = lower + q ** (n + 1) / factorial(n + 1) / (1 - q / (n + 2))
    if not 4 < lower < upper < Q(9, 2):
        raise ValueError('outward exponential check failed')
    return {'polynomial_identities': 'Gamma and Laplacian reduce identically to zero modulo three sphere constraints',
            'Haar_S': '0', 'Haar_S_squared': '13/4', 'Haar_GammaS': '45/16',
            'exp_3_over_2_lower': str(lower), 'exp_3_over_2_upper': str(upper),
            'gap_lower_over_c': str(Q(3, 4) / upper),
            'proof_scope': 'finite exact polynomial identities and outward exponential enclosure; no operator theorem inferred from fixtures'}


def lattice_audit():
    def geom(q, n):
        return (1 - q ** n) / (1 - q)
    def closed(q, L):
        g = geom(q, L + 1)
        even = geom(q * q, L // 2 + 1)
        separator = q ** 3 * geom(q ** 4, (L + 1) // 4)
        return (2 * g ** 3 + g * (g - even) * g + separator * even * g) / 24
    rows = []
    for q in (Q(1, 4), Q(1, 2), Q(2, 3), Q(3, 4)):
        total = (Q(3)/(1-q)**3 - (1+q+q*q)/((1-q**4)*(1-q*q)*(1-q))) / 24
        for L in range(6):
            direct = sum((q ** (x+y+z) / 24 for axis_pair in ((0,1),(0,2),(1,2))
                          for x,y,z in product(range(L+1), repeat=3)
                          if axis_pair != (0,1) or y % 2 or x % 4 == 3), Q(0))
            if direct != closed(q, L) or not 0 < direct < total:
                raise ValueError('omitted-class ledger failed')
            rows.append({'q':str(q), 'L':L, 'retained':str(direct), 'tail':str(total-direct)})
        if q == Q(1,2) and total != Q(107,135):
            raise ValueError('inherited dyadic weight mismatch')
    # Symbolic leading q->1 coefficient: three orientations minus selected fraction3/8.
    leading = (Q(3) - Q(3,8)) / 24
    if leading != Q(7,64):
        raise ValueError('summability asymptotic coefficient')
    return {'rows':rows, 'limit_of_one_minus_q_cubed_times_omitted_budget':'7/64',
            'proof_scope':'exact finite ledgers; infinite tail and limit justified by geometric series in report'}


def two_witness_variance_audit():
    def edges(f):
        a, b, *p = f
        pa, pb = p.copy(), p.copy()
        pa[a] += 1
        pb[b] += 1
        return {(a, *p), (b, *pa), (a, *pb), (b, *p)}
    def free(e):
        axis, x, y, z = e
        return axis == 2 or (axis == 1 and y % 2 == 1) or (axis == 0 and x % 4 == 3)
    faces = [(*ab, *p) for ab in ((0, 1), (0, 2), (1, 2))
             for p in product(range(9), repeat=3)
             if ab != (0, 1) or p[1] % 2 or p[0] % 4 == 3]
    incidence = defaultdict(set)
    supports = {}
    witness_counts = []
    for i, f in enumerate(faces):
        supports[i] = edges(f)
        witness_counts.append(sum(free(e) for e in supports[i]))
        if witness_counts[-1] < 2:
            raise ValueError('omitted face lacks two free witnesses')
        for edge in supports[i]:
            incidence[edge].add(i)
    maximum_shared = 0
    for i, es in supports.items():
        candidates = set().union(*(incidence[e] for e in es)) - {i}
        for j in candidates:
            common = len(es & supports[j])
            maximum_shared = max(maximum_shared, common)
            if common > 1 or not any(free(e) and e not in supports[j] for e in es):
                raise ValueError('distinct face pair has no unmatched free witness')
    def budget(q):
        return (2/(1-q)**3 + q/((1-q)**2*(1-q*q))
                + q**3/((1-q)*(1-q*q)*(1-q**4)))/24
    rays = []
    for eta in (Q(1, 4), Q(1, 2), Q(3, 4)):
        for q in (Q(1, 2), Q(3, 4), Q(7, 8), Q(15, 16), Q(31, 32)):
            tau = eta/(8*budget(q))
            variance = tau*tau*budget(q*q)/96
            floor = (1-eta)/8
            conservative = Q(5, 6)*tau*tau/(1-q*q)**3
            if variance > conservative:
                raise ValueError('exact variance exceeds conservative covariance bound')
            rays.append({'q':str(q), 'eta':str(eta), 'tau':str(tau),
                         'variance_over_alpha_squared':str(variance),
                         'projector_distance_squared_bound':str(min(Q(1), variance/floor**2)),
                         'ground_energy_magnitude_bound_over_alpha':str(variance/floor),
                         'constant_operator_norm_over_alpha':str(eta/8)})
    # From B(q)~(7/64)(1-q)^-3 and B(q^2)~(7/512)(1-q)^-3.
    variance_coefficient = Q(7, 512)/(64*96*Q(7,64)**2)
    if variance_coefficient != Q(1,5376):
        raise ValueError('canonical-ray exact variance asymptotic coefficient')
    return {'omitted_face_count':len(faces), 'minimum_free_witness_count':min(witness_counts),
            'maximum_pair_shared_links':maximum_shared,
            'exact_variance_identity':'alpha^2 tau(q)^2 B(q^2)/96',
            'canonical_ray_variance_leading_coefficient_over_alpha_squared_eta_squared':'1/5376',
            'ray_fixtures':rays,
            'proof_scope':'finite two-witness geometry fixtures and exact ray arithmetic; general plaquette intersection and conditional Haar proof in report'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('choose a fresh output file')
    result = {'status':'passed', 'producer_imports':False,
              'polynomial_audit':polynomial_audit(), 'lattice_audit':lattice_audit(),
              'two_witness_variance_audit':two_witness_variance_audit(),
              'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status':'passed', 'global_polynomial_identities':2,
                      'exact_weight_fixtures':24, 'two_witness_faces':1872,
                      'canonical_ray_fixtures':15}))


if __name__ == '__main__':
    main()
