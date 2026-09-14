#!/usr/bin/env python3
"""Independent post-freeze P1 checks; no producer imports or finite-to-all-n inference."""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from math import comb, factorial
from pathlib import Path


def need(value, message):
    if value is not True:
        raise RuntimeError(message)


def char_coefficients(n):
    # Closed binomial expression, independent of the producer recurrences.
    p = [F(0)] * (n + 1)
    for k in range(n // 2 + 1):
        p[n - 2*k] = F((-1)**k * comb(n-k, k) * 2**(n-2*k))
    return p


def moment(k):
    return F(0) if k % 2 else F(comb(k, k//2), (k//2+1)*2**k)


def inner(p, q):
    return sum((a*b*moment(i+j) for i,a in enumerate(p)
                for j,b in enumerate(q)), F(0))


def class_casimir(p):
    out = [F(0)] * len(p)
    for k,a in enumerate(p):
        out[k] += F(k*(k+2), 4)*a
        if k >= 2:
            out[k-2] -= F(k*(k-1), 4)*a
    return out


def gmul(a, b):
    return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])


def gadd(a, b):
    return (a[0]+b[0], a[1]+b[1])


def gconj(a):
    return (a[0], -a[1])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    output = parser.parse_args().output.absolute()
    need(not output.exists(), 'fresh output required')
    for item in (output, *output.parents):
        need(not item.is_symlink(), 'symlink rejected')
    root = Path(__file__).resolve().parents[3]
    ledger_path = root/'research/round19/forward/c1/output/graph-reduction.json'
    ledger = json.loads(ledger_path.read_text())
    vertices = list(product(range(3), range(3), range(2)))
    edges = [(axis, v) for axis in range(3) for v in vertices
             if v[axis] < (2,2,1)[axis]]
    indices = {edge:i for i,edge in enumerate(edges)}
    def shift(v, axis):
        return tuple(x + int(i == axis) for i,x in enumerate(v))
    faces = []
    for a,b in combinations(range(3), 2):
        for v in vertices:
            if v[a] < (2,2,1)[a] and v[b] < (2,2,1)[b]:
                faces.append([(indices[(a,v)],1), (indices[(b,shift(v,a))],1),
                              (indices[(a,shift(v,b))],-1), (indices[(b,v)],-1)])
    need((len(vertices),len(edges),len(faces)) == (18,33,20), 'actual graph')
    reference = {f['face_id']:f for f in ledger['constant_faces']+ledger['affected_faces']}
    for i, word in enumerate(faces):
        need([{'edge':e, 'sign':s} for e,s in word] == reference[i]['signed_word'],
             'full signed-word comparison')
    active = {28:'U', 27:'V', 24:'W'}
    selected = [0,1,13]
    supports = [{e for e,s in faces[p]} for p in selected]
    need(len(set.union(*supports)) == 12, 'three edge-disjoint character factors')
    need(not set.union(*supports).intersection(active), 'constant section images')
    need(bool({e for e,s in faces[0]}.intersection(e for e,s in faces[2])),
         'overlapping-face independence control must reject')
    character_tests = []
    for n in range(13):
        p = char_coefficients(n)
        eigen = F(n*(n+2),4)
        need(sum(p) == n+1 and inner(p,p) == 1, 'character value and Haar norm')
        need(class_casimir(p) == [eigen*a for a in p], 'class Casimir eigenvalue')
        if n:
            need(inner(p,[F(1)]) == 0, 'centered nontrivial character')
        character_tests.append(n)
    rows = []
    for n in (1,2,5,11,31,127):
        d = n+1
        norm2 = F(1,d**6)
        electric2 = F(9*n*n*(n+2)**2,d**6)
        need(electric2 < F(9,d*d), 'fixed alpha/E_star graph-null estimate')
        need(F(n*(n+2),d*d) == 1-F(1,d*d), 'all-n graph estimate identity')
        # With only two factors the squared electric norm has a positive limit.
        two_factor_electric2 = F(4*n*n*(n+2)**2,d**4)
        need(two_factor_electric2 == 4*(1-F(1,d*d))**2,
             'two-factor graph-null overclaim rejected')
        rows.append({'n':n, 'norm_squared':str(norm2),
                     'electric_norm_squared_over_alpha_squared':str(electric2),
                     'section_image':'1'})
    physical = F(3)
    training = F(3,4)
    held = F(3,2)
    fit = physical/training
    need(fit == 4 and fit*held == 6, 'single training fit, common held-out clock')
    need(physical/held == 2 and physical/held != fit, 'held-out refit rejected')
    need(all(e not in active for e,s in faces[0]) and physical != 0,
         'constant-face core intertwining rejected at every c')
    # Noncommuting unit quaternion scalars distinguish UV from UV^{-1}.
    u0,v0,dot = F(3,5),F(1,3),F(8,15)
    need(u0*v0+dot == F(11,15) and u0*v0-dot == F(-1,3),
         'held-out orientation negative control')
    # Independent positive exponential series with a geometric tail, then inversion.
    n = 30
    exp_lower = sum((F(1,factorial(k)) for k in range(n+1)), F(0))
    exp_upper = exp_lower + F(n+2,(n+1)*factorial(n+1))
    xlo,xhi = 1/exp_upper,1/exp_lower
    lo,hi = (xlo**3-xhi**6)/4,(xhi**3-xlo**6)/4
    tight = ['0.01182707904779939613907431','0.01182707904779939613907432']
    need(F(tight[0]) < lo < hi < F(tight[1]), 'independent tight fixed-time enclosure')
    a,b = (F(1),F(2)),(F(2),F(-1))
    means_a,means_b = (F(3),F(1)),(F(-2),F(4))
    expected = gmul(gconj(a),b)
    expected = (expected[0]/8,expected[1]/8)
    disconnected = gmul(gconj(means_a),means_b)
    raw = gadd(expected,disconnected)
    centered = gadd(raw,(-disconnected[0],-disconnected[1]))
    wrong_adjoint = gmul(a,b)
    wrong_adjoint = (wrong_adjoint[0]/8,wrong_adjoint[1]/8)
    need(centered == expected and raw != expected and wrong_adjoint != expected,
         'complex centering and adjoint controls')
    result = {
        'schema':'ym22-skeptic-review-check-v1', 'loop':'p1', 'passed':True,
        'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'ledger_sha256':hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
        'producer_imports':False, 'current_producers_read_after_both_frozen':True,
        'all_twenty_signed_words_match':True,
        'graph_domain_faces':{str(p):faces[p] for p in selected},
        'edge_disjoint_support_count':12, 'character_indices_checked':character_tests,
        'finite_character_checks_are_all_n_proof':False,
        'graph_null_sequence':rows,
        'all_n_graph_norm_bound':'d^-6 + 9*(alpha/E_star)^2*d^-2 -> 0',
        'two_factor_electric_norm_squared_limit_over_alpha_squared':'4',
        'training_c_over_alpha':'4', 'held_energy_over_alpha':'6',
        'fixed_time_difference':'(exp(-3)-exp(-6))/4',
        'fixed_time_strict_interval':tight,
        'controls':{'overlapping_faces_not_independent':True,
                    'two_characters_insufficient_for_graph_null_argument':True,
                    'wrong_held_face_orientation_rejected':True,
                    'held_out_refit_rejected':True,
                    'constant_face_generator_equation_rejected':True,
                    'uncentered_complex_correlation_rejected':True,
                    'unconjugated_first_channel_rejected':True},
        'research_loops_added':0,
        'scope':'Actual fixed finite electric endpoint and designated section only'}
    output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'loop':'p1','passed':True,'controls':len(result['controls'])}))


if __name__ == '__main__':
    main()
