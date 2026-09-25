#!/usr/bin/env python3
"""HNM-BA1 reverse producer: boundary decay of the AM2 creation coefficients of the
named construction families F1 and F2 on supports meeting the cover R={0,e_z}, by
complex-coupling analyticity of the AM2 fixed point on a disc |z|<=rho, the
order-versus-distance count and Cauchy's estimate in its maximum-modulus (Schwarz
lemma) form.

Human project author: Hruday N M (BUNZEEY). AI-assisted reverse production (Claude,
an AI model) under reverse premise isolation; HNM labels are project aliases.
Banach's fixed-point theorem, Weierstrass' theorem on uniform limits of holomorphic
functions, the maximum-modulus principle and Cauchy's estimates, and the
connected-cluster support property of perturbation expansions are established
mathematics; the commuting creation expansion is the admitted AM2 construction.
Scientific priority is unverified.

Standard library only. Exact Fraction arithmetic decides every Boolean; decimal
strings are truncated previews. Every contract control is implemented as damaging
mutations whose rejection is required. Failures are explicit exceptions (never
assert), so the run and its output bytes are identical under python -O.

Usage: python3 -B research/round33/reverse/ba1/check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import math
import re
from collections import deque
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
INPUTS = HERE / 'inputs'
CONTRACT_REL = 'research/round33/contracts/ba1.json'
CONTRACT_SHA256 = '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9'
PINNED_GATES = {
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
}
I1_REL = 'research/round21/forward/i1/report.md'
FORBIDDEN_PREFIXES = (
    'research/round33/forward/',
    'research/round33/skeptic/',
    'research/round33/experts/',
    'research/round33/advisor/deliberation-',
    'research/round33/advisor/panel',
    'research/round33/advisor/triage',
    'research/round33/reverse/',
)
F1_NAME = 'F1: AQ1 centered whole-star boxes Lambda_N=[-N,N]^3'
F2_NAME = 'F2: I1 section 6 all-contained-face boxes with padding on the same Lambda_N'
ROUTE = 'analytic_disc'
TIERS = ('crude_majorant', 'exact_first_order')
ROUTES = ('weighted_norm', 'analytic_disc')
DEN = 10 ** 40
ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state',
]
NEGATION = re.compile(r"\b(not|never|no|nor|neither|without|excludes?|excluded|exclusion|forbidden|"
                      r"cannot|does not|is not|are not|nothing|none)\b", re.I)


# ----------------------------------------------------------------- exceptions
class AdmissionError(Exception):
    """A validator refused its input: the required fate of a damaging mutation."""


class ProducerError(Exception):
    """An identity required by the proof failed; the run aborts without output."""


def require(condition, reason):
    if condition is not True:
        raise AdmissionError(reason)


def must(condition, reason):
    if condition is not True:
        raise ProducerError(reason)


CHECKS = []
MUTATION_CONTROLS = []


def check(check_id, condition, **details):
    must(condition is True, 'check failed: ' + check_id)
    must(all(c['id'] != check_id for c in CHECKS), 'duplicate check id: ' + check_id)
    entry = {'id': check_id, 'passed': True}
    entry.update(details)
    CHECKS.append(entry)


def rejected(mutation, label):
    """Run one damaging mutation (a zero-argument callable); return its rejection reason."""
    try:
        mutation()
    except AdmissionError as exc:
        return str(exc)
    raise ProducerError('damaging mutation accepted: ' + label)


def control(check_id, mutations, **details):
    """A contract control passes only if every listed damaging mutation is rejected."""
    reasons = {}
    for label, mutation in mutations:
        must(label not in reasons, 'duplicate mutation label ' + label)
        reasons[label] = rejected(mutation, label)
    must(len(reasons) > 0, 'control without mutations: ' + check_id)
    MUTATION_CONTROLS.append(check_id)
    check(check_id, True, kind='damaging_mutation_control', rejected_mutations=reasons, **details)


# ----------------------------------------------------------- exact arithmetic
def parse_q(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise AdmissionError('non-exact numeric input rejected: ' + repr(value))
    if isinstance(value, Q):
        return value
    if isinstance(value, int):
        return Q(value)
    if isinstance(value, str) and re.fullmatch(r'[+-]?[0-9]+(/[1-9][0-9]*)?', value.strip()):
        return Q(value.strip())
    raise AdmissionError('malformed rational input rejected: ' + repr(value))


def qs(x):
    return str(Q(x))


def ceil_to(x, den=DEN):
    x = Q(x)
    return Q(-((-x.numerator * den) // x.denominator), den)


def floor_to(x, den=DEN):
    x = Q(x)
    return Q((x.numerator * den) // x.denominator, den)


def factorial(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r


def exp_bounds(x, terms=24):
    """Directed enclosure of exp(x), 0<=x<=1/2: partial sum plus geometric tail."""
    x = Q(x)
    must(Q(0) <= x <= Q(1, 2), 'exponential argument outside [0,1/2]')
    partial, power = Q(0), Q(1)
    for k in range(terms + 1):
        partial += power / factorial(k)
        power *= x
    tail = power / factorial(terms + 1) / (1 - x / (terms + 2))
    return floor_to(partial), ceil_to(partial + tail)


def root4_lower(y):
    """Directed lower rational bound lo<=y^(1/4) at resolution 10^-12."""
    y = Q(y)
    den = 10 ** 12
    lo, hi = 0, den
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if Q(mid, den) ** 4 <= y:
            lo = mid
        else:
            hi = mid
    must(Q(lo, den) ** 4 <= y < Q(lo + 1, den) ** 4, 'fourth-root enclosure')
    return Q(lo, den)


def sci(x, digits=12):
    """Truncated decimal preview computed with integers only (never used to decide)."""
    x = Q(x)
    if x == 0:
        return '0'
    sign = '-' if x < 0 else ''
    x = abs(x)
    e = len(str(x.numerator)) - len(str(x.denominator))
    while Q(10) ** e > x:
        e -= 1
    while Q(10) ** (e + 1) <= x:
        e += 1
    scaled = x / Q(10) ** e * 10 ** (digits - 1)
    mant = str(scaled.numerator // scaled.denominator)
    return sign + mant[0] + '.' + mant[1:] + 'e' + str(e)


def exact(x):
    return {'exact': qs(x), 'preview': sci(x)}


def sha256_file(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ceil_div(a, b):
    return -((-a) // b)


# ------------------------------------------------------------ lattice geometry
E = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
R_COVER = (ORIGIN, EZ)
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))


def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def vsub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def coarse(p):
    """I1.1: pi(x,y,z)=(floor(x/4), floor(y/2), z); Python // is floor division."""
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    """The four positively stored links of the face at p in directions a<c (tails p, p+e_a, p+e_c, p)."""
    return ((p, a), (vadd(p, E[a]), c), (vadd(p, E[c]), a), (p, c))


def derive_classes():
    """All 24 anchored face classes derived from pi and the link tails (I1 section 3)."""
    out = []
    for a, c in (('x', 'y'), ('x', 'z'), ('y', 'z')):
        for r in range(4):
            for s in range(2):
                p = (r, s, 0)
                links = face_links(p, a, c)
                K = tuple(sorted({vsub(coarse(t), coarse(p)) for t, _ in links}))
                link_owner_counts = {}
                for t, _ in links:
                    o = vsub(coarse(t), coarse(p))
                    link_owner_counts[o] = link_owner_counts.get(o, 0) + 1
                selected = (a, c) == ('x', 'y') and s == 0 and r <= 2
                out.append({'orient': a + c, 'r': r, 's': s, 'K': K, 'selected': selected,
                            'max_links_one_owner': max(link_owner_counts.values())})
    return out


TOKENS = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}


def parse_i1_table(text):
    rows = []
    pat = re.compile(r'^\| (xy|xz|yz): r=([0-9,]+); s=([0-9,]+) \| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|\s*$')
    for line in text.splitlines():
        m = pat.match(line.strip())
        if m:
            rs = [int(v) for v in m.group(2).split(',')]
            ss = [int(v) for v in m.group(3).split(',')]
            support = tuple(sorted(TOKENS[t.strip()] for t in m.group(5).split(',')))
            rows.append({'orient': m.group(1), 'r': rs, 's': ss, 'count': int(m.group(4)),
                         'K': support, 'selected': m.group(6) == 'selected'})
    return rows


def compare_i1(rows, classes):
    seen = set()
    for row in rows:
        require(row['count'] == len(row['r']) * len(row['s']), 'I1 table row count')
        for r in row['r']:
            for s in row['s']:
                match = [c for c in classes if c['orient'] == row['orient'] and c['r'] == r and c['s'] == s]
                require(len(match) == 1 and match[0]['K'] == row['K'] and match[0]['selected'] == row['selected'],
                        'I1 table row disagrees with the derived class ' + row['orient'] + str((r, s)))
                seen.add((row['orient'], r, s))
    require(len(seen) == 24, 'I1 table does not cover the 24 classes')
    return True


CLASSES = derive_classes()
OMITTED = [c for c in CLASSES if not c['selected']]


def face_support(face):
    b, k = face
    return tuple(sorted(vadd(b, s) for s in OMITTED[k]['K']))


def box(N):
    return frozenset(product(range(-N, N + 1), repeat=3))


def prism(lo, hi):
    return frozenset(product(*[range(lo[i], hi[i] + 1) for i in range(3)]))


def f1_faces(vol):
    out = set()
    for b in vol:
        if all(vadd(b, s) in vol for s in S_STAR):
            for k in range(len(OMITTED)):
                out.add((b, k))
    return frozenset(out)


def f2_faces(vol):
    out = set()
    for b in vol:
        for k, c in enumerate(OMITTED):
            if all(vadd(b, s) in vol for s in c['K']):
                out.add((b, k))
    return frozenset(out)


def dinf(p, q):
    return max(abs(p[0] - q[0]), abs(p[1] - q[1]), abs(p[2] - q[2]))


def dl1(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1]) + abs(p[2] - q[2])


METRICS = {'linf': (dinf, 1), 'l1': (dl1, 2)}


def dist_R(Y, metric):
    m = METRICS[metric][0]
    return min(m(p, y) for p in R_COVER for y in Y)


def diam(Y, metric):
    m = METRICS[metric][0]
    return max((m(p, q) for p in Y for q in Y), default=0)


def star(b):
    return tuple(sorted(vadd(b, s) for s in S_STAR))


def pieces_f1(vol):
    return {b: frozenset(star(b)) for b in vol if all(vadd(b, s) in vol for s in S_STAR)}


def pieces_f2(vol):
    out = {}
    for b in vol:
        X = set()
        for c in OMITTED:
            if all(vadd(b, s) in vol for s in c['K']):
                X |= {vadd(b, s) for s in c['K']}
        if X:
            out[b] = frozenset(X)
    return out


NEIGHBOUR_OFFSETS = sorted({vsub(a, b) for a in S_STAR for b in S_STAR} - {ORIGIN})


def chain_orders(pieces):
    """Least connected-family size joining a piece meeting R to each piece (BFS + 1)."""
    start = [b for b in sorted(pieces) if pieces[b] & set(R_COVER)]
    level = {b: 1 for b in start}
    dq = deque(start)
    while dq:
        b = dq.popleft()
        for o in NEIGHBOUR_OFFSETS:
            b2 = vadd(b, o)
            if b2 in pieces and b2 not in level and pieces[b] & pieces[b2]:
                level[b2] = level[b] + 1
                dq.append(b2)
    return start, level


def order_distance_table(pieces, metric):
    start, level = chain_orders(pieces)
    must(len(level) == len(pieces), 'piece graph is connected to R')
    dX = METRICS[metric][1]
    rows = {}
    diams = set()
    for b in sorted(pieces):
        Y = pieces[b]
        d = dist_R(Y, metric)
        diams.add(diam(Y, metric))
        row = rows.setdefault(d, {'d': d, 'pieces': 0, 'least_order': None, 'largest_order': 0})
        row['pieces'] += 1
        row['least_order'] = level[b] if row['least_order'] is None else min(row['least_order'], level[b])
        row['largest_order'] = max(row['largest_order'], level[b])
    out = []
    for d in sorted(rows):
        row = rows[d]
        row['contract_bound_ceil_d_over_diam'] = ceil_div(d, dX)
        row['sharp_bound_one_plus_ceil'] = 1 + ceil_div(d, dX) if d >= 1 else 1
        row['lemma_holds'] = row['least_order'] >= row['sharp_bound_one_plus_ceil'] >= row['contract_bound_ceil_d_over_diam']
        row['sharp_attained'] = row['least_order'] == row['sharp_bound_one_plus_ceil']
        out.append(row)
    return {'metric': metric, 'diameter_convention': dX, 'piece_diameters': sorted(diams), 'pieces': len(pieces),
            'pieces_meeting_R': len(start), 'rows': out}


# ---------------------------------------------------------- source inventories
def validate_source(inventory, A, B, source_set, support=None):
    """The source of a comparison: exactly the terms present in one box and not the other, each once,
    each meeting the declared source set. Terms are faces (support = owner set) or whole stars (anchors)."""
    support = face_support if support is None else support
    inv = list(inventory)
    require(len(inv) == len(set(inv)), 'a source term is charged twice')
    for f in inv:
        require((f in A) != (f in B), 'source charged with a term present in both boxes (old term) ' + str(f))
        require(bool(set(support(f)) & source_set), 'source term does not meet the declared source set ' + str(f))
    require(set(inv) == set(A) ^ set(B), 'source inventory differs from the symmetric difference of the two boxes')
    return True


def certify_source_distance(inventory, claimed, metric='linf'):
    actual = min(dist_R(face_support(f), metric) for f in inventory)
    require(claimed == actual, 'claimed source distance %d differs from the enumerated %d' % (claimed, actual))
    return actual


def validate_f2_charge(charges, A, B):
    """F2 regrouping: charged face by face, each gained face exactly once, no old face."""
    require(len(charges) == len(set(charges)), 'an F2 face is charged twice')
    for f in charges:
        require(f in B and f not in A, 'F2 regrouping charged an old face of a gaining group ' + str(f))
    require(set(charges) == set(B) - set(A), 'F2 regrouping misses a gained face')
    per_site = {}
    for f in charges:
        for x in face_support(f):
            per_site[x] = per_site.get(x, 0) + 1
    require(max(per_site.values()) <= 49, 'per-site face count above 49')
    return max(per_site.values())


# --------------------------------------------------------- creation-algebra fixtures
def mat_mul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n) if A[i][k]) for j in range(n)] for i in range(n)]


def mat_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A))] for i in range(len(A))]


def four_qubit_termination():
    """C = sum_x sigma^+_x, V = prod_x sigma^-_x on four qubits: ad_C^8(V)Omega = 8!|1111>, ad_C^9(V) = 0."""
    n = 16
    C = [[0] * n for _ in range(n)]
    for s in range(n):
        for x in range(4):
            if not (s >> x) & 1:
                C[s | (1 << x)][s] += 1
    V = [[0] * n for _ in range(n)]
    V[0][n - 1] = 1
    out = {}
    A = V
    for k in range(1, 10):
        A = mat_sub(mat_mul(C, A), mat_mul(A, C))
        out[k] = A[n - 1][0]
        if k == 9:
            out['ad9_zero'] = all(v == 0 for row in A for v in row)
    return out


def set_partitions(items):
    items = list(items)
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in set_partitions(rest):
        yield [[first]] + p
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]


def chain_rs(nsites, bonds, order):
    """Rayleigh-Schroedinger ground vector (intermediate normalization) of H0=sum n_x, V=sum X_iX_j."""
    def apply_V(vec):
        out = {}
        for s, a in vec.items():
            for (i, j) in bonds:
                t = s ^ (1 << i) ^ (1 << j)
                out[t] = out.get(t, 0) + a
        return {k: v for k, v in out.items() if v != 0}
    psi, energy = [{0: Q(1)}], [Q(0)]
    for n in range(1, order + 1):
        Vp = apply_V(psi[n - 1])
        energy.append(Vp.get(0, Q(0)))
        rhs = {}
        for j in range(1, n + 1):
            for s, a in psi[n - j].items():
                rhs[s] = rhs.get(s, 0) + energy[j] * a
        for s, a in Vp.items():
            rhs[s] = rhs.get(s, 0) - a
        psi.append({s: a / bin(s).count('1') for s, a in rhs.items() if s != 0 and a != 0})
    return psi


def chain_creations(psi, nsites, order):
    """Creation coefficients from psi = prod_I (1 - c_I a_I) Omega (qubits): cumulant inversion order by order."""
    def mul(a, b):
        out = [Q(0)] * (order + 1)
        for i, x in enumerate(a):
            if x == 0:
                continue
            for j, y in enumerate(b):
                if i + j > order:
                    break
                out[i + j] += x * y
        return out
    c = {}
    for size in range(1, nsites + 1):
        for M in combinations(range(nsites), size):
            acc = [Q(0)] * (order + 1)
            for part in set_partitions(M):
                if len(part) < 2:
                    continue
                prod_ = [Q(1)] + [Q(0)] * order
                for Bk in part:
                    prod_ = mul(prod_, [-x for x in c[tuple(sorted(Bk))]])
                acc = [u + v for u, v in zip(acc, prod_)]
            mask = sum(1 << i for i in M)
            c[M] = [-(psi[n].get(mask, Q(0)) - acc[n]) for n in range(order + 1)]
    return c


def chain_fixture(L=4, order=6):
    """Sites 0..L, R={0}; box A = all bonds; box B_d = box A without bond (d,d+1). The first order at which
    a creation coefficient on a support containing 0 differs is 1+d (sharp order-versus-distance)."""
    ns = L + 1
    bondsA = [(i, i + 1) for i in range(L)]
    cA = chain_creations(chain_rs(ns, bondsA, order), ns, order)
    rows = []
    for d in range(1, L):
        bondsB = [b for b in bondsA if b != (d, d + 1)]
        cB = chain_creations(chain_rs(ns, bondsB, order), ns, order)
        first, witness = None, None
        for M in sorted(cA):
            if 0 not in M:
                continue
            for n in range(order + 1):
                if cA[M][n] != cB[M][n]:
                    if first is None or n < first:
                        first, witness = n, (M, cA[M][n], cB[M][n])
                    break
        rows.append({'source_bond': [d, d + 1], 'source_distance_from_R': d, 'first_differing_order': first,
                     'witness_support': list(witness[0]), 'witness_values': [qs(witness[1]), qs(witness[2])],
                     'sharp_order_one_plus_d': 1 + d, 'contract_order_ceil_d': d,
                     'far_endpoint_distance': d + 1})
    first_order = {'support': [0, 1], 'order_1_coefficient': qs(cA[(0, 1)][1]), 'creations': 0, 'interactions': 1,
                   'support_diameter': 1}
    return rows, first_order


def certify_vanishing_order(claimed_n0, observed_first):
    require(claimed_n0 <= observed_first, 'claimed vanishing through order %d is falsified: nonzero difference at order %d'
            % (claimed_n0 - 1, observed_first))
    return True


# --------------------------------------------------------- other exact fixtures
def solve_linear(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col] / M[col][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return [M[i][n] / M[i][i] for i in range(n)]


def nonlocal_lipschitz_fixture(n=6, lam=Q(1, 2), sigma=Q(1)):
    """T(c)_i = lam*mean(c) + s_i: sup-norm Lipschitz lam, yet c_0 does not decay with the source distance."""
    values = {}
    for d in range(1, n):
        A = [[(1 if i == j else 0) - lam / n for j in range(n)] for i in range(n)]
        s = [sigma if i == d else Q(0) for i in range(n)]
        c = solve_linear(A, s)
        values[d] = c[0]
    return values


def certify_decay_claim(value_at_R, claimed_bound):
    require(abs(value_at_R) <= claimed_bound, 'claimed decay bound ' + sci(claimed_bound, 6) + ' is below the exact value '
            + sci(abs(value_at_R), 6))
    return True


def chain_weight_fixture(n=4, lam=Q(1, 4), sigma=Q(1)):
    """Linear nearest-neighbour map on sites 0..n (R=0, source B={n}); returns the exact fixed point."""
    size = n + 1
    A = [[(1 if i == j else 0) - (lam if abs(i - j) == 1 else 0) for j in range(size)] for i in range(size)]
    s = [sigma if i == n else Q(0) for i in range(size)]
    return solve_linear(A, s)


def weighted_bound_at_R(weights, lam, sigma, n):
    """Weighted-norm contraction bound for |Delta_0| with weight omega_i (exact); rejects non-contractive weights."""
    lip = max(lam * sum(weights[i] / weights[j] for j in (i - 1, i + 1) if 0 <= j <= n) for i in range(n + 1))
    require(lip < 1, 'weight is not submultiplicative along the chain: weighted Lipschitz bound ' + sci(lip, 6) + ' >= 1')
    return sigma * weights[n] / (1 - lip) / weights[0], lip


def certify_weight_direction(weights, lam, sigma, n, unweighted):
    bound, lip = weighted_bound_at_R(weights, lam, sigma, n)
    require(bound < unweighted, 'the weighted bound at R, ' + sci(bound, 6) + ', exceeds the unweighted bound '
            + sci(unweighted, 6) + ': no decay (weight grows with distance from R, not towards R from the source)')
    require(all(weights[i] >= weights[i + 1] for i in range(n)), 'difference weight grows with distance from R '
            '(it must grow with distance from the source B, towards R)')
    return bound, lip


def gauss_mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def normalization_pole_fixture(a=Q(2), disc=Q(1)):
    """psi(z)=Omega - a z|11> on (r,o): the creation coefficient a z is entire, but the complexified
    normalization 1 + a^2 z^2 vanishes at z = i/a inside the disc |z|<=1 (a=2)."""
    z0 = (Q(0), 1 / a)
    z0sq = gauss_mul(z0, z0)
    norm = (1 + a * a * z0sq[0], a * a * z0sq[1])
    return {'pole': ['0', qs(1 / a)], 'pole_modulus': qs(1 / a), 'disc_radius': qs(disc),
            'normalization_at_pole': [qs(norm[0]), qs(norm[1])], 'inside_disc': (1 / a) < disc and norm == (Q(0), Q(0))}


def certify_analytic_object(obj, zero_free_region_proved):
    require(obj == 'AM2 creation coefficients' or zero_free_region_proved is True,
            'analyticity on the disc is proved for the creation coefficients only; ' + obj
            + ' needs a zero-free region of the complexified normalization, which is not proved')
    return True


def marginal_fixture():
    """AV1 F13 type: qubits r,o,o'; creations c_{r,o}=a (straddling), c_o=b, c_o'=g. Coefficients meeting R={r}
    are unchanged when b changes, yet rho_r changes."""
    def rho_r(a, b):
        z = 1 + a * a + b * b
        return ((1 + b * b) / z, a * b / z, a * a / z)
    a = Q(1, 3)
    r1, r2 = rho_r(a, Q(1, 2)), rho_r(a, Q(0))
    d00, d01 = r1[0] - r2[0], r1[1] - r2[1]
    tn_sq = 4 * (d00 * d00 + d01 * d01)       # traceless 2x2 Hermitian: ||X||_1^2 = 4(x^2+y^2)
    return {'rho_r_b_half': [qs(r1[0]), qs(r1[1]), qs(r1[2])], 'rho_r_b_zero': [qs(r2[0]), qs(r2[1]), qs(r2[2])],
            'coefficients_meeting_R_difference': '0', 'trace_norm_squared_difference': qs(tn_sq), 'tn_sq': tn_sq}


def certify_state_inference(coefficient_difference, state_trace_norm_sq, inference):
    if inference == 'state decay from coefficient decay':
        require(coefficient_difference != 0 or state_trace_norm_sq == 0,
                'coefficient decay on supports meeting R does not bound the reduced density (normalization and '
                'straddling contractions couple all supports; BB1)')
    return True


# ------------------------------------------------------- set-geometry fixtures
def subadditivity_ok(X, Is, M, rule, metric='linf'):
    dX = diam(X, metric)
    ds = [diam(I, metric) for I in Is]
    bound = dX + (sum(ds) if rule == 'sum' else max(ds, default=0))
    require(diam(M, metric) <= bound, 'output diameter %d exceeds the %s-rule bound %d' % (diam(M, metric), rule, bound))
    return True


def outputs(X, Is):
    N = set().union(*[set(I) for I in Is]) if Is else set()
    base = N - set(X)
    extra = sorted(set(X))
    for r in range(len(extra) + 1):
        for sub in combinations(extra, r):
            M = base | set(sub)
            if M:
                yield tuple(sorted(M))


def exhaustive_subadditivity():
    X = star(ORIGIN)
    supports = set()
    for b in product(range(-2, 2), repeat=3):
        for k, c in enumerate(OMITTED):
            Y = face_support((b, k))
            if set(Y) & set(X):
                supports.add(Y)
        if set(star(b)) & set(X):
            supports.add(star(b))
    supports = sorted(supports)
    dX = diam(X, 'linf')
    dia = {Y: diam(Y, 'linf') for Y in supports}
    count = 0
    for I1 in supports:
        for M in outputs(X, [I1]):
            subadditivity_ok(X, [I1], M, 'sum')
            count += 1
    for I1, I2 in combinations(supports, 2):
        whole = tuple(sorted(set(X) | set(I1) | set(I2)))      # every admissible output M lies inside N u X
        require(diam(whole, 'linf') <= dX + dia[I1] + dia[I2], 'subadditivity fails on a pair')
        count += 1
    return len(supports), count


def certify_reach(rule, n_interactions, k_creations, out_diam, dX):
    budget = n_interactions * dX if rule == 'per_interaction' else k_creations * dX
    require(out_diam <= budget, 'reach charged %s gives %d < output diameter %d' % (rule, budget, out_diam))
    return True


# --------------------------------------------------------------- claim validators
GATE_FIELD_KEYS = ('uniqueness_of_ground_state_claimed', 'whole_sequence_claimed', 'state_decay_claimed',
                   'rate_in_N_claimed', 'rate_in_a_claimed', 'continuum_claim', 'scientific_priority_verified',
                   'translation_invariance_claimed', 'common_limit_claimed', 'weak_coupling_claim',
                   'coefficient_cauchy_claimed', 'coefficient_cauchy_scope')
FALSE_FLAGS = ('continuum_claim', 'uniqueness_of_ground_state_claimed', 'state_decay_claimed', 'rate_in_a_claimed',
               'scientific_priority_verified', 'whole_sequence_claimed', 'translation_invariance_claimed',
               'common_limit_claimed', 'weak_coupling_claim')


def validate_claim_flags(flags):
    for k in FALSE_FLAGS:
        require(flags.get(k) is False, 'claim flag must be false: ' + k)
    require(flags.get('rate_in_N_claimed') is True and flags.get('coefficient_cauchy_claimed') is True,
            'rate in N and coefficient Cauchy property are the topic of this loop')
    return True


def certify_gate_fields(fields, required):
    require(sorted(fields) == sorted(required), 'gate fields are not the contract topic-specific set')
    for k, v in required.items():
        require(fields[k] == v, 'gate field value differs from the contract: ' + k)
    return True


def certify_premise_provenance(kind):
    require(kind in ('admitted gate', 'shared premise report', 'standard mathematics'),
            'historical, occult or governmental provenance supplies no premise: ' + kind)
    return True


def certify_packet_model(pk, contract):
    pre = contract['preregistration']
    require(pk['model_id'] == pre['model_id'], 'model id relabelled: ' + pk['model_id'])
    require(tuple(parse_q(x) for x in pk['triple']) == (0, 0, 0), 'nonzero selected triple: P_R is not Haar (changed model)')
    require(abs(parse_q(pk['tau'])) <= parse_q(pre['tau']['value']), 'coupling above the preregistered cap')
    require(pk['group'] == 'SU(2)' and pk['dimension'] == 3, 'other group or dimension relabelled as the patterned family')
    require(pk['J_per_tau'] == 28, 'interaction family changed (per-site sum %s|tau|)' % pk['J_per_tau'])
    require(pk['families'] == [F1_NAME, F2_NAME], 'construction family changed')
    require(pk['metric'] == 'coarse l-infinity, d_X=1', 'metric changed from the contract parameters')
    require(pk['disc_rule'] == {'headline': '64|tau|', 'floor': 'tau_star=1/37888'}, 'disc radius rule (weights) changed')
    require(pk['window'] == contract['parameters']['window'], 'window changed from the contract parameters')
    require(pk['model_class'] == 'patterned zero-selected family', 'finite-graph or uniform-model result under the patterned label')
    return True


def certify_uniformity_statement(s):
    low = s.lower()
    require('lattice spacing' not in low.replace('not a statement uniform in the lattice spacing', ''),
            'uniformity claimed in the lattice spacing a')
    if 'uniform' in low:
        require('in n at fixed spacing' in low or 'uniformly in the cutoff' in low, 'unqualified uniformity word next to a rate')
    return True


def certify_rate_unit(unit):
    require(unit == 'per coarse step at fixed spacing (a coarse step is (4a,2a,a))',
            'q is a rate per coarse step at fixed spacing, not ' + unit)
    return True


def certify_limit_statement(obj, quantifier, basis):
    require(quantifier in ('whole sequence', 'subsequence'), 'limit statement without a whole-sequence/subsequence quantifier')
    if quantifier == 'whole sequence':
        require(basis == 'Cauchy bound' and obj == 'AM2 creation coefficients on supports meeting R in each Q_L',
                'whole-sequence claim for ' + obj + ' is not supported by a Cauchy bound')
    return True


def certify_families(families):
    require(list(families) == [F1_NAME, F2_NAME], 'exactly the two named construction families: ' + json.dumps(list(families)))
    return True


def certify_family_is_F2(face_set, f2_set, f1_set):
    require(face_set == f2_set, 'face set is not the all-contained-face family (I1 section 6)')
    require(face_set != f1_set, 'family collapsed onto F1: not the named F2')
    return True


def certify_cover(cover, n_links, n_endpoints):
    require(tuple(sorted(cover)) == tuple(sorted(R_COVER)), 'cover is not the complete factor cover of W')
    require(n_links == 48 and n_endpoints == 36, 'cover must be the complete factors (48 links, 36 endpoints), not drawn links')
    return True


def certify_scope_statement(s):
    low = s.lower()
    require('each on-site cutoff space' in low, 'coefficient statement without the on-site cutoff space Q_L')
    for m in re.finditer(r'untruncated', low):
        window = low[max(0, m.start() - 40):m.start()]
        require('not' in window or 'no ' in window, 'untruncated creation coefficients asserted')
    require('cutoff removed' not in low, 'cutoff removal applied to coefficients')
    return True


def certify_rate_provenance(prov):
    require(prov in ('disc radius rho=64|tau| (q=|tau|/rho), disc contraction checked',
                     'disc radius rho=tau_star=1/37888 (q=|tau|/rho=37888|tau|), disc contraction checked'),
            'rate provenance must be a checked disc radius, not ' + prov)
    return True


def certify_decay_factor(provenance, factor, q):
    require(provenance == 'analytic_disc ratio |tau|/rho', 'decay factor from ' + provenance + ' is rejected (global Lipschitz is not decay)')
    require(factor == q, 'decay factor differs from q=|tau|/rho')
    return True


def certify_metric(distance_metric, diameter_convention):
    require(distance_metric in METRICS, 'unknown metric')
    require(METRICS[distance_metric][1] == diameter_convention, 'metric mixing: %s distances with diameter %d'
            % (distance_metric, diameter_convention))
    return True


def certify_exponent_basis(basis):
    require(basis == 'distance from R to the nearest source term', 'vanishing order must be counted from R to the source; '
            + basis + ' is the reversed or wrong direction')
    return True


def certify_card_rate(label, rate, loss_exponent, q_min, q_card_lower):
    if label == 'cardinality':
        require(loss_exponent == 4, 'cardinality weight loses e^{4mu} per interaction')
        require(rate >= q_card_lower, 'cardinality rate ' + sci(rate, 6) + ' is below q_min^(1/4)')
    else:
        require(label == 'diameter' and loss_exponent == 1 and rate >= q_min, 'diameter rate mislabelled')
    return True


def certify_disc(rho, G_up, Gp_up, R, tau_star, cited):
    require(cited == 'evaluated at the declared rho', 'disc contraction cited from ' + cited + ' instead of re-evaluated')
    require(rho <= tau_star, 'disc radius above tau_star=1/37888')
    require(28 * rho * G_up <= R, 'disc self-map 28 rho G(R) <= R fails')
    require(28 * rho * Gp_up < 1, 'disc Lipschitz 28 rho G\'(R) < 1 fails')
    return 28 * rho * Gp_up


def certify_lipschitz_value(rho, claimed, Gp_up):
    require(claimed == 28 * rho * Gp_up, 'disc Lipschitz constant must be 28 rho G\'(R) at the declared rho')
    return True


def certify_rate_floor(q, q_min, radius):
    require(q >= q_min, 'rate ' + sci(q, 6) + ' crosses the proved minimum q_min=' + sci(q_min, 6) + ' at radius ' + radius)
    return True


def certify_rho_rule(rule):
    require(rule in ('64|tau|', 'tau_star=1/37888'), 'disc radius must be the frozen rule, not ' + rule)
    return True


def certify_pair(q, K_target, contract, which):
    pair = contract['parameters']['rate_constant_pair']['headline' if which == 'headline' else 'rate_floor']
    require(parse_q(pair['q']) == q and parse_q(pair['K_target']) == K_target, 'rate/constant pair differs from the frozen pair')
    return True


def certify_J(stars_per_site, star_norm_per_tau=7):
    require(stars_per_site == 4, 'per-site sum must include incoming stars (4 stars, 28|tau|), not %d' % stars_per_site)
    return stars_per_site * star_norm_per_tau


def certify_source_site_count(count):
    require(count == 49, 'per-site face count must include incoming anchors (49), not %d' % count)
    return True


def certify_l1(value, count, per):
    require(value >= count * per, 'anchored sum is an l1 sum over faces; ' + sci(value, 6) + ' < ' + sci(count * per, 6))
    return True


def certify_combination(values, combine):
    require(combine == 'linear', 'deterministic bounds add linearly, not by ' + combine)
    return sum(values)


def certify_no_volume_division(divisor):
    require(divisor is None, 'no division by sqrt(N) or sqrt(#faces): the bound is uniform in N')
    return True


def certify_tier_constant(label, route, t_kind, M_kind):
    require(label in TIERS, 'tier outside the closed vocabulary: ' + str(label))
    require(route in ROUTES, 'route outside the closed vocabulary: ' + str(route))
    if label == 'exact_first_order':
        require(t_kind == 'self_consistent_T(rho)' and M_kind == 'two_balls', 'exact_first_order constant mixes tiers: '
                + t_kind + '/' + M_kind)
    else:
        require(t_kind == 'crude_592_rho' and M_kind == 'two_balls', 'crude constant mislabelled')
    return True


def certify_scaling(ratio, bracket):
    lo, hi = bracket
    require(lo <= ratio <= hi, 'tau -> tau/100 ratio ' + sci(ratio, 8) + ' outside the prefrozen bracket')
    return True


def certify_bracket_prefrozen(bracket, contract_bracket):
    require(bracket == contract_bracket, 'bracket chosen after evaluation (differs from preregistration)')
    return True


def certify_clock(label, formula):
    require((label, formula) in (('theta', 'alpha*t/hbar'), ('s', 'alpha*t_E/hbar'), ('u', 'theta/8')),
            'clock mislabelled: ' + label + '=' + formula)
    return True


def certify_first_order_amplitude(value, tau):
    require(value == -tau / 72, 'first-order face amplitude must be -tau/72 in both unit systems')
    return True


def producer_outcome(disc_contraction, global_lipschitz_decay, pairs, comparisons, tier, metric_closes):
    if not disc_contraction or global_lipschitz_decay:
        return 'insufficient'
    if pairs != {'headline', 'floor'} or comparisons != 4 or tier != 'exact_first_order' or metric_closes != 'linf':
        return 'limited'
    return 'accepted_within_scope'


def certify_outcome(recorded, inputs):
    require(recorded == producer_outcome(**inputs), 'recorded outcome differs from the rule-derived outcome')
    return recorded


def certify_no_retuning(tau_used, tau_contract):
    require(tau_used == tau_contract, 'tau retuned after the constants were seen')
    return True


def admit_bound(value, target):
    require(isinstance(value, Q) and not isinstance(value, bool), 'admission requires an exact Fraction')
    require(value <= target, 'bound exceeds target')
    return True


def certify_face_counts(counts, derivation, recomputed):
    require(derivation == 'translation covariance over the anchors u-S from the I1 table', 'face counts must be derived, not '
            + derivation)
    require(counts == recomputed, 'face counts differ from the derivation')
    return True


# ------------------------------------------------------- phrasing validators
def normalize(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def phrase_hits(text, forbidden, template):
    body = normalize(text)
    if template:
        body = body.replace(normalize(template), ' ')
    hits = []
    for clause in [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', body) if c.strip()]:
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                if not NEGATION.search(clause):
                    hits.append({'phrase': phrase, 'clause': clause[:200]})
    return hits


def certify_phrasing(text, forbidden, template):
    hits = phrase_hits(text, forbidden, template)
    require(hits == [], 'affirmative forbidden phrasing: ' + json.dumps(hits[:2]))
    return True


PLACEHOLDER = re.compile(r'<([^<>]*)>')


def certify_no_placeholder(s):
    for m in PLACEHOLDER.finditer(s):
        inner = m.group(1)
        require(not (re.search(r'\s', inner) or '|' in inner or 'e.g.' in inner), 'placeholder span: <' + inner + '>')
    return True


def certify_template_once(text, template):
    require(text.count(template) == 1, 'mandatory sentence template must be quoted exactly once as one unbroken span')
    return True


def table_row_text(N, tables):
    def cell(t):
        return ', '.join('`%d:%d/%d/%d(%d)`' % (r['d'], r['least_order'], r['contract_bound_ceil_d_over_diam'],
                                               r['sharp_bound_one_plus_ceil'], r['pieces']) for r in t['rows'])
    return '| `Lambda_%d` | %s | %s |' % (N, cell(tables['Lambda_%d/F1_stars/linf' % N]), cell(tables['Lambda_%d/F1_stars/l1' % N]))


def certify_report_pins(report, pins):
    missing = [p for p in pins if p not in report]
    require(missing == [], 'report does not carry the checker value(s): ' + json.dumps(missing[:4]))
    return True


# ------------------------------------------------------ contract and premises
PARAM_KEYS = ('metric', 'weights', 'rate_constant_pair', 'comparisons', 'cutoff', 'window', 'N_min', 'clock')


def validate_contract(data):
    require(data.get('id') == 'BA1' and data.get('round') == 33 and data.get('status') == 'frozen_before_production',
            'contract identity or status')
    require(data.get('human_author') == 'Hruday N M (BUNZEEY)', 'human author')
    p = data['parameters']
    for k in PARAM_KEYS:
        require(k in p and bool(p[k]), 'contract parameters must declare ' + k)
    require('coarse l-infinity' in p['metric'] and 'd_X=1' in p['metric'], 'metric/diameter not declared')
    require('tau_star = 1/37888' in p['weights'] and 'rho = 64|tau|' in p['weights'] and 'rho = tau_star' in p['weights'],
            'reverse disc radii not declared in weights')
    rc = p['rate_constant_pair']
    require(rc['headline']['q'] == '1/64' and rc['headline']['K_target'] == '1/2000000'
            and rc['headline']['tier'] == 'exact_first_order', 'headline pair')
    require(rc['rate_floor']['q'] == '148/390625' and rc['rate_floor']['K_target'] == '1/12', 'floor pair')
    require(len(p['comparisons']) == 4, 'four comparisons')
    require(p['window'].startswith('not applicable'), 'window')
    pre = data['preregistration']
    require(pre['model_id'] == 'AQ_patterned_zero_selected', 'model id')
    require([parse_q(x) for x in pre['selected_triple_alpha_units']] == [0, 0, 0], 'selected triple')
    require(pre['tau']['value'] == '1/100000000' and pre['tau']['signs_evaluated'] == ['+', '-'], 'tau value or signs')
    require(pre['target']['value'] == '1/2000000 and 1/12' and pre['target']['comparator'] == '<=', 'target')
    require(pre['observable']['reference_value_exact'] == '0', 'reference value')
    hb = pre['hash_binding']
    require(all(hb[k] is True for k in hb) and len(hb) == 4, 'hash-binding flags must all be true')
    gf = pre['gate_fields_required']
    require(sorted(gf) == sorted(GATE_FIELD_KEYS), 'gate field set')
    require(gf['rate_in_N_claimed'] is True and gf['coefficient_cauchy_claimed'] is True
            and all(gf[k] is False for k in FALSE_FLAGS if k in gf), 'gate field values')
    require(pre['error_terms_itemized'] == ['weighted_contraction_loss', 'boundary_source_terms', 'order_versus_distance_count',
                                             'exact_first_order_remainder', 'cutoff_uniformity', 'arithmetic'], 'error terms')
    require(set(pre['scaling_brackets_per_constant']) == {'K_exact_first_order_at_q_1_64', 'K_floor_pair', 'q_min'}, 'brackets')
    ids = data['controls']
    require(ids == pre['controls_required']['ids'] and len(set(ids)) == len(ids) == 37, 'controls list differs from preregistration')
    require(set(ids) == set(data['new_control_semantics']) | {'full_original_wilson_cover', 'gate_fields_topic_specific'},
            'control semantics')
    require(data.get('reverse_premise_isolation') is True, 'reverse premise isolation flag')
    require('analytic_disc' in pre['tier_names_allowed'], 'tier vocabulary')
    return True


def validate_contract_bytes(raw, expected_sha):
    require(hashlib.sha256(raw).hexdigest() == expected_sha, 'contract bytes do not match the bound hash')
    data = json.loads(raw)
    validate_contract(data)
    return data


def validate_inventory(files, contract):
    expected = {'AGENTS.md', CONTRACT_REL} | set(contract['shared_premises'])
    for f in files:
        require(not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in reverse inputs: ' + f)
        require(not (f.startswith('research/round33/advisor/') and f != 'research/round33/advisor/selection-ba1.md'),
                'advisor file other than the selection note: ' + f)
    require(sorted(files) == sorted(expected) and len(files) == len(expected),
            'reverse inputs inventory differs from AGENTS.md + contract + shared_premises')
    return True


def validate_pinned(rel, raw):
    require(hashlib.sha256(raw).hexdigest() == PINNED_GATES[rel], 'admitted gate bytes differ from the pinned sha256: ' + rel)
    return True


def parse_bracket(text):
    if text.startswith('exactly'):
        v = parse_q(text.split()[1])
        return (v, v)
    m = re.match(r'\[\s*([0-9/]+)\s*,\s*([0-9/]+)\s*\]', text)
    must(m is not None, 'bracket parse')
    return (parse_q(m.group(1)), parse_q(m.group(2)))


# ==================================================================== compute
def compute():
    check_py_sha = sha256_file(HERE / 'check.py')            # recorded before any evaluation
    raw = (INPUTS / CONTRACT_REL).read_bytes()
    contract_sha = hashlib.sha256(raw).hexdigest()
    must(contract_sha == CONTRACT_SHA256, 'contract snapshot hash differs from the bound constant')
    contract = validate_contract_bytes(raw, CONTRACT_SHA256)
    check('contract_snapshot_bound', contract_sha == CONTRACT_SHA256, contract_sha256=contract_sha,
          source='inputs/' + CONTRACT_REL, verified='before any evaluation')
    check('check_py_sha256_recorded_before_evaluation', len(check_py_sha) == 64, check_py_sha256=check_py_sha)
    cache = sorted(p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if '__pycache__' in p.parts or p.suffix == '.pyc')
    check('no_interpreter_cache_in_closure', cache == [])
    gates = {}
    for rel in sorted(PINNED_GATES):
        blob = (INPUTS / rel).read_bytes()
        must(validate_pinned(rel, blob), 'pinned gate')
        gates[rel] = json.loads(blob)
        must(gates[rel]['verdict'] == 'accepted_within_scope', 'gate verdict ' + rel)
    check('admitted_gate_sha256_pinned', True, pinned=dict(PINNED_GATES))
    inventory = sorted(p.relative_to(INPUTS).as_posix() for p in INPUTS.rglob('*') if p.is_file())
    must(validate_inventory(inventory, contract), 'inventory')

    params, pre = contract['parameters'], contract['preregistration']
    am2 = gates['research/round29/advisor/am2-gate.json']
    m = re.search(r'\|tau\|<=1/(\d+)', am2['accepted'])
    must(m is not None, 'AM2 cap')
    TAU = parse_q(pre['tau']['value'])
    must(TAU == Q(1, int(m.group(1))), 'contract tau equals the admitted AM2 cap')
    targets = {'headline': (parse_q(params['rate_constant_pair']['headline']['q']),
                            parse_q(params['rate_constant_pair']['headline']['K_target'])),
               'floor': (parse_q(params['rate_constant_pair']['rate_floor']['q']),
                         parse_q(params['rate_constant_pair']['rate_floor']['K_target']))}
    brackets = {k: parse_bracket(v) for k, v in pre['scaling_brackets_per_constant'].items()}
    template = pre['mandatory_sentence_template']

    # ------------------------------------------------ AM2 constants (re-derived)
    e_lo, e_hi = exp_bounds(Q(1, 8))
    must(e_hi < Q(8, 7), 'exp(1/8)<8/7')
    R = Q(1, 64)
    G_up = 16 * Q(8, 7) * (1 + 10 * R)
    Gp_up = 16 * Q(8, 7) * (18 + 80 * R)
    G_lo = 16 * e_lo * (1 + 10 * R)
    taylor_ok = all(16 * 8 ** k * (1 + Q(5 * k, 4)) == factorial(k) * 16 * (Q(8 ** k, factorial(k))
                    + (10 * Q(8 ** (k - 1), factorial(k - 1)) if k > 0 else 0)) for k in range(9))
    term = four_qubit_termination()
    J0 = 28 * TAU
    check('am2_constants_rederived',
          G_up == Q(148, 7) and Gp_up == 352 and J0 == Q(7, 25000000) and J0 * G_up < R and taylor_ok
          and term[8] == factorial(8) and term['ad9_zero'] is True and term[7] == 0 and G_lo < G_up,
          exp_one_eighth_enclosure=[qs(e_lo), qs(e_hi)], G_R_upper=qs(G_up), G_prime_R_upper=qs(Gp_up),
          G_R_lower_preview=sci(G_lo), J0=qs(J0), four_qubit_termination={'ad8_coefficient': term[8], 'ad9_zero': True},
          note='G(t)=16e^{8t}(1+10t); k![t^k]G=16*8^k(1+5k/4) for k<=8; termination 2|X|=8 for |X|=4 (z-free algebra)')

    # ------------------------------------------------ I1 table and face counts
    i1_text = (INPUTS / I1_REL).read_text()
    rows = parse_i1_table(i1_text)
    must(len(rows) == 8 and compare_i1(rows, CLASSES), 'I1 table')
    must(len(CLASSES) == 24 and len(OMITTED) == 21, 'class counts')
    per_class_sizes = [len(c['K']) for c in OMITTED]
    through_u = sum(per_class_sizes)
    owner_sets = {}
    for c in OMITTED:
        for s in c['K']:
            M = tuple(sorted(vsub(t, s) for t in c['K']))
            owner_sets[M] = owner_sets.get(M, 0) + 1
    faces_0 = {(vsub(ORIGIN, s), k) for k, c in enumerate(OMITTED) for s in c['K']}
    faces_z = {(vsub(EZ, s), k) for k, c in enumerate(OMITTED) for s in c['K']}
    meeting_R = faces_0 | faces_z
    inside_R = {f for f in meeting_R if set(face_support(f)) <= set(R_COVER)}
    counts = {'faces_per_factor': through_u, 'owner_sets_per_factor': len(owner_sets), 'faces_meeting_R': len(meeting_R),
              'faces_inside_R': len(inside_R)}
    must(certify_face_counts(counts, 'translation covariance over the anchors u-S from the I1 table',
                             {'faces_per_factor': 49, 'owner_sets_per_factor': 15, 'faces_meeting_R': 82, 'faces_inside_R': 10}),
         'face counts')
    max_links = max(c['max_links_one_owner'] for c in OMITTED)
    check('i1_table_derived_and_face_counts', True, i1_rows_parsed=len(rows), classes=24, omitted=21, counts=counts,
          owner_set_multiplicities=sorted(owner_sets.values()),
          cutoff_note='a face vector W_f Omega_0 puts at most %d links (site energy %d<=24) on one factor, so Q_L keeps it '
                      'exactly for L>=24 and first-order counts only decrease for L<24' % (max_links, 6 * max_links))

    # ------------------------------------------------ F1/F2 boxes, stars, incidence
    boxes = {N: box(N) for N in (2, 3, 4, 5)}
    F1 = {N: f1_faces(boxes[N]) for N in boxes}
    F2 = {N: f2_faces(boxes[N]) for N in boxes}
    ay1 = gates['research/round32/advisor/ay1-gate.json']
    must('28N(5N+1)' in ay1['accepted'] and '82 faces meeting R' in ay1['accepted'], 'AY1 gate pins')
    box_rows = {}
    for N in (2, 3, 4):
        P1, P2 = pieces_f1(boxes[N]), pieces_f2(boxes[N])
        stars_per_site = max(sum(1 for b in P1 if u in P1[b]) for u in boxes[N])
        groups_per_site = max(sum(1 for b in P2 if u in P2[b]) for u in boxes[N])
        faces_per_site_f2 = max(sum(1 for f in F2[N] if u in face_support(f)) for u in (ORIGIN, EZ, (N, N, N), (0, 0, N)))
        incident = sorted(b for b in P1 if P1[b] & set(R_COVER))
        must(F1[N] < F2[N], 'F1 is a strict subset of F2')
        must(len(F2[N] - F1[N]) == 28 * N * (5 * N + 1), 'extra F2 faces 28N(5N+1)')
        must(len({f for f in F1[N] if set(face_support(f)) & set(R_COVER)}) == 82
             and len({f for f in F2[N] if set(face_support(f)) & set(R_COVER)}) == 82, '82 faces meeting R retained')
        must(all(diam(P1[b], 'linf') == 1 and diam(P1[b], 'l1') == 2 for b in P1), 'star diameters')
        must(all(diam(face_support(f), 'linf') == 1 for f in F2[N]), 'face diameters')
        box_rows[str(N)] = {'sites': len(boxes[N]), 'stars_F1': len(P1), 'groups_F2_nonempty': len(P2), 'faces_F1': len(F1[N]),
                            'faces_F2': len(F2[N]), 'F2_minus_F1': len(F2[N] - F1[N]), 'formula_28N_5N_plus_1': 28 * N * (5 * N + 1),
                            'max_stars_per_site': stars_per_site, 'max_groups_per_site': groups_per_site,
                            'incident_stars_meeting_R': len(incident), 'star_linf_diameter': 1, 'star_l1_diameter': 2,
                            'max_F2_faces_through_sampled_sites': faces_per_site_f2}
        must(stars_per_site == 4 and groups_per_site == 4 and len(incident) == 7, 'incidence')
    check('stars_supports_diameter_and_incidence', True, boxes=box_rows,
          all_size_argument='S-S={0,+-e_i,+-(e_i-e_j)} has l-infinity norms 0,1 and l1 norms 0,1,2, so every star b+S has '
                            'l-infinity diameter 1 and l1 diameter 2 for every b; faces and clipped groups are subsets')

    # ------------------------------------------------ disc constants (item 1)
    tau_star = R / (28 * G_up)
    must(tau_star == Q(1, 37888), 'tau_star derived as R/(28*148/7)')
    must('tau_star = 1/37888' in params['weights'], 'tau_star read from contract weights')
    rho = {'headline': 64 * TAU, 'floor': tau_star}
    disc = {}
    for which in ('headline', 'floor'):
        r = rho[which]
        kappa = certify_disc(r, G_up, Gp_up, R, tau_star, 'evaluated at the declared rho')
        t1 = 49 * r / 144
        T = t1 / (1 - 28 * r * Gp_up)
        disc[which] = {'rho': r, 'q': TAU / r, 'self_map_value': 28 * r * G_up, 'kappa': kappa, 't1': t1, 'T': T,
                       'remainder': 28 * r * Gp_up * T, 't_crude': 28 * r * G_up}
        must(T <= R and disc[which]['t_crude'] <= R, 'circle bounds inside the ball')
    must(disc['headline']['q'] == targets['headline'][0], 'headline q=|tau|/(64|tau|)=1/64')
    q_min = 28 * TAU * G_up / R
    must(q_min == Q(148, 390625) and disc['floor']['q'] == q_min == targets['floor'][0], 'floor q = q_min = 37888|tau|')
    check('disc_contraction_rechecked', True,
          tau_star=qs(tau_star), q_min_at_cap=qs(q_min),
          discs={w: {'rho': exact(d['rho']), 'q': qs(d['q']), 'self_map_28rhoG': exact(d['self_map_value']), 'ball_R': '1/64',
                     'lipschitz_kappa_28rhoGprime': exact(d['kappa'])} for w, d in disc.items()},
          itemized_z_dependence='in HNM-AM2.5 only ||V_X(z)||=|z| ||V_X(1)|| depends on z (creation algebra, output sets, '
                                'H_M^{-1}, counting and termination are z-free; no self-adjointness is used)')
    check('coefficient_map_analytic_on_disc', True,
          argument='iterates c^(m+1)(z)=F_z(c^(m)(z)), c^(0)=0, are polynomials in z in the finite-dimensional coefficient '
                   'space of each Q_L; they stay in the ball and converge uniformly on |z|<=rho with ratio kappa<1, so the '
                   'limit is continuous on the closed disc and holomorphic inside (Weierstrass); at real z=tau it is the '
                   'AM2 fixed point by uniqueness in the ball',
          headline_kappa=qs(disc['headline']['kappa']), floor_kappa=qs(disc['floor']['kappa']))
    check('tiers_on_the_circle', True,
          tiers={w: {'t1_rho': exact(d['t1']), 'T_rho_exact_first_order': exact(d['T']), 'remainder_352J_T': exact(d['remainder']),
                     't_crude_28rhoG': exact(d['t_crude'])} for w, d in disc.items()},
          identity='T(rho)=t1(rho)/(1-28 rho G\'(R)) equals w t_1/(1-J w G\'(R)) with J=28|tau|, w=rho/|tau| (the tier rule, '
                   're-derived in the anchored norm at complex coupling on the circle)')

    # ------------------------------------------------ order-versus-distance tables (item 2)
    tables = {}
    for N in (2, 3, 4):
        for fam, P in (('F1_stars', pieces_f1(boxes[N])), ('F2_groups', pieces_f2(boxes[N]))):
            for metric in ('linf', 'l1'):
                t = order_distance_table(P, metric)
                must(all(r['lemma_holds'] for r in t['rows']), 'order-versus-distance lemma on ' + fam)
                tables['Lambda_%d/%s/%s' % (N, fam, metric)] = t
    linf_sharp_attained = all(r['sharp_attained'] for k, t in tables.items() if k.endswith('linf') and 'F1' in k
                              for r in t['rows'] if r['d'] <= int(k.split('/')[0].split('_')[1]) - 1)
    must(linf_sharp_attained, 'sharp l-infinity order attained along the z-axis chain')
    chain_rows, chain_first = chain_fixture()
    must(all(r['first_differing_order'] == r['sharp_order_one_plus_d'] for r in chain_rows), 'chain fixture sharpness')
    check('order_versus_distance_lemma', True,
          statement='a creation coefficient on a support meeting R depends on a piece at coarse l-infinity distance d>=1 '
                    'from R only at order >= 1+ceil(d/diam) >= ceil(d/diam); diam=1 (l-infinity, used by the proof); '
                    'the l1 alternative has diam=2',
          tables_summary={k: [[r['d'], r['least_order'], r['contract_bound_ceil_d_over_diam'], r['sharp_bound_one_plus_ceil']]
                              for r in t['rows']] for k, t in tables.items()},
          proof_uses='linf')
    check('order_sharpness_chain_fixture', True, rows=chain_rows, model_is_finite_graph=True, transfers_to_aq=False,
          note='qubit chain 0..4 with bonds X_iX_{i+1}, R={0}; removing bond (d,d+1) changes a coefficient on a support '
               'containing 0 first at order exactly 1+d')

    # ------------------------------------------------ boundary sources (item 3)
    shell_dist = {}
    sources = {}
    for N in (2, 3, 4):
        shell = boxes[N + 1] - boxes[N]
        shell_dist[N] = {'e_z': min(dinf(EZ, p) for p in shell), '0': min(dinf(ORIGIN, p) for p in shell)}
        must(shell_dist[N] == {'e_z': N, '0': N + 1}, 'shell distances')
        outer = {p for p in boxes[N] if max(p) == N}
        stars_old, stars_new = set(pieces_f1(boxes[N])), set(pieces_f1(boxes[N + 1]))
        inv_stars = sorted(stars_new - stars_old)
        inv1 = sorted(F1[N + 1] - F1[N])
        inv2 = sorted(F2[N + 1] - F2[N])
        inv3 = sorted(F2[N] - F1[N])
        must(validate_source(inv_stars, stars_old, stars_new, set(shell), support=star), 'F1 nested source (whole stars)')
        must(validate_source(inv1, F1[N], F1[N + 1], set(shell) | outer), 'F1 nested source (faces of new stars)')
        inside_faces = [f for f in inv1 if not set(face_support(f)) & set(shell)]
        must(len(inside_faces) > 0 and all(set(face_support(f)) <= outer for f in inside_faces), 'inside faces of new stars')
        must(set(inside_faces) == set(F2[N]) - set(F1[N]), 'new F1 faces inside Lambda_N are exactly the extra F2 faces')
        must(min(dist_R(star(b), 'linf') for b in inv_stars) == N - 1, 'new-star distance')
        must(validate_source(inv2, F2[N], F2[N + 1], set(shell)), 'F2 nested source')
        must(validate_source(inv3, F1[N], F2[N], outer), 'F1/F2 source')
        d1_ = certify_source_distance(inv1, N - 1)
        d2_ = certify_source_distance(inv2, N - 1)
        d3_ = certify_source_distance(inv3, N - 1)
        old_anchors = {g[0] for g in F2[N]}
        gaining = sorted({f[0] for f in inv2 if f[0] in old_anchors})
        f2_site_max = validate_f2_charge(inv2, F2[N], F2[N + 1])
        anchors3 = {f[0] for f in inv3}
        must(all(max(b) == N for b in anchors3), 'F1/F2 extra faces are anchored on the positive outer faces')
        wit1 = ((0, 0, N), [k for k, c in enumerate(OMITTED)][0])
        must(wit1 in F1[N + 1] and wit1 not in F1[N] and dist_R(face_support(wit1), 'linf') == N - 1, 'F1 witness')
        kz = next(k for k, c in enumerate(OMITTED) if c['K'] == ((0, 0, 0), (0, 0, 1)))
        kx = next(k for k, c in enumerate(OMITTED) if c['K'] == ((0, 0, 0), (1, 0, 0)))
        must(((0, 0, N), kz) in inv2 and ((0, 0, N), kx) in inv3, 'F2 witnesses')
        sources[str(N)] = {
            'F1_nested': {'new_stars': len(inv_stars), 'new_faces': len(inv1), 'min_linf_distance': d1_,
                          'min_l1_distance': min(dist_R(face_support(f), 'l1') for f in inv1),
                          'new_faces_inside_Lambda_N': len(inside_faces),
                          'inside_faces_equal_F2_minus_F1_on_Lambda_N': True,
                          'sites_met_by_new_terms': 'shell Lambda_{N+1} minus Lambda_N plus the positive outer layer '
                                                    '{max_i p_i = N} of Lambda_N',
                          'witness': 'star (0,0,N)+S contains (0,0,N) at l-infinity distance N-1 from e_z'},
            'F2_nested': {'new_faces': len(inv2), 'min_linf_distance': d2_, 'gaining_groups': len(gaining),
                          'max_new_faces_through_a_site': f2_site_max,
                          'witness': 'face anchored at (0,0,N) with owner set {(0,0,N),(0,0,N+1)}'},
            'F1_vs_F2': {'extra_faces': len(inv3), 'formula': 28 * N * (5 * N + 1), 'min_linf_distance': d3_,
                         'anchors': len(anchors3),
                         'witness': 'face anchored at (0,0,N) with owner set {(0,0,N),(1,0,N)}'},
            'shell_distance': shell_dist[N]}
        must(len(inv_stars) == (2 * N + 2) ** 3 - (2 * N) ** 3 and len(inv1) == 21 * len(inv_stars), 'F1 nested count')
    check('boundary_sources_identified', True, sources=sources,
          all_size_argument='a face at l-infinity distance <= N-2 from R has a point q in Lambda_{N-1}; its anchor b=q-s, s in S, '
                            'has b_i in [-N,N-1], so b+S lies in Lambda_N: every such face is retained by F1 and F2 on every '
                            'complete-factor volume containing Lambda_N; every source term is therefore at distance >= N-1, and '
                            'the witnesses attain N-1 in all three named comparisons')
    core_ok = {}
    for N in (2, 3, 4):
        big = F2[5]
        near = [f for f in big if dist_R(face_support(f), 'linf') <= N - 2]
        core_ok[str(N)] = {'faces_within_N_minus_2': len(near),
                           'all_in_F1_Lambda_N': all(f in F1[N] for f in near)}
        must(core_ok[str(N)]['all_in_F1_Lambda_N'], 'common core')
    gen_vols = {'F1(Lambda_2) vs F2(Lambda_4)': (F1[2], F2[4], 2), 'F2(Lambda_3) vs F1(Lambda_4)': (F2[3], F1[4], 3),
                'F1([-2,3]x[-2,2]x[-2,4]) vs F2(Lambda_3)': (f1_faces(prism((-2, -2, -2), (3, 2, 4))), F2[3], 2),
                'F2([-3,2]x[-2,3]x[-2,2]) vs F2(Lambda_2)': (f2_faces(prism((-3, -2, -2), (2, 3, 2))), F2[2], 2)}
    gen = {}
    for name, (A, B, N) in gen_vols.items():
        inv = sorted(set(A) ^ set(B))
        dmin = min(dist_R(face_support(f), 'linf') for f in inv)
        must(dmin >= N - 1, 'general comparison source distance')
        gen[name] = {'N': N, 'source_faces': len(inv), 'min_linf_distance': dmin}
    check('common_core_and_general_volumes', True, common_core=core_ok, general=gen)

    # ------------------------------------------------ Cauchy bounds (item 4)
    def K_of(which, tier, tau_abs):
        r = 64 * tau_abs if which == 'headline' else tau_star
        if tier == 'exact_first_order':
            return 2 * (49 * r / 144) / (1 - 28 * r * Gp_up)
        return 2 * 28 * r * G_up

    pairs = {}
    for which in ('headline', 'floor'):
        q = disc[which]['q']
        for tier in TIERS:
            must(certify_tier_constant(tier, ROUTE, 'self_consistent_T(rho)' if tier == 'exact_first_order' else 'crude_592_rho',
                                       'two_balls'), 'tier')
            K = K_of(which, tier, TAU)
            meets = K <= targets[which][1]
            pairs[(which, tier)] = {'q': q, 'K': K, 'meets': meets}
    must(pairs[('headline', 'exact_first_order')]['meets'] and pairs[('floor', 'exact_first_order')]['meets'], 'targets')
    must(not pairs[('headline', 'crude_majorant')]['meets'] and pairs[('floor', 'crude_majorant')]['meets'], 'crude tier')
    comp_names = ('F1 N vs N+1', 'F2 N vs N+1', 'F1 vs F2 same Lambda_N', 'general volumes containing Lambda_N')
    bounds = {}
    for cname in comp_names:
        bounds[cname] = {}
        for N in (2, 3, 4):
            d = N - 1
            n0_contract, n0_sharp = ceil_div(d, 1), 1 + d
            must(n0_contract >= N - 1 and n0_sharp == N, 'vanishing order')
            per = {}
            for (which, tier), v in pairs.items():
                val = v['K'] * v['q'] ** n0_contract
                must(val <= v['K'] * v['q'] ** (N - 1), 'exponent')
                per[which + '/' + tier] = sci(val, 8)
            bounds[cname][str(N)] = {'source_distance': d, 'vanishing_order_contract_form': n0_contract,
                                     'vanishing_order_sharp': n0_sharp, 'K_q_pow_N_minus_1_previews': per}
    for sign in ('+', '-'):
        for which in ('headline', 'floor'):
            r = 64 * abs(TAU if sign == '+' else -TAU) if which == 'headline' else tau_star
            must(K_of(which, 'exact_first_order', abs(-TAU if sign == '-' else TAU)) == pairs[(which, 'exact_first_order')]['K']
                 and r == rho[which], 'sign replay')
    Kh, Kf = pairs[('headline', 'exact_first_order')]['K'], pairs[('floor', 'exact_first_order')]['K']
    must(Kh == Q(49, 111790368) and Kf == Q(49, 2018304), 'headline constants')
    must(pairs[('headline', 'crude_majorant')]['K'] == Q(296, 390625) and pairs[('floor', 'crude_majorant')]['K'] == Q(1, 32),
         'crude constants')
    check('coefficient_difference_bound_all_comparisons', True, comparisons=bounds,
          theorem='for u in R: sum_{I containing u} ||c^A_I(tau)-c^B_I(tau)|| <= 2 t(rho) (|tau|/rho)^{n_0}, n_0 >= N-1 '
                  '(contract form; sharp N), every comparison, every Q_L, both signs',
          schwarz='g(z)=(c^A_I(z)-c^B_I(z))_{I containing u} is holomorphic on |z|<rho, continuous on |z|<=rho, vanishes to '
                  'order n_0 at 0; the maximum-modulus principle applied to g(z)/z^{n_0} gives ||g(tau)|| <= (|tau|/rho)^{n_0} '
                  'max_{|w|=rho} ||g(w)|| <= (|tau|/rho)^{n_0} 2 t(rho)')
    check('headline_pair_met', admit_bound(Kh, targets['headline'][1]), q='1/64', K=exact(Kh), target='1/2000000',
          margin=sci(targets['headline'][1] / Kh, 8), tier='exact_first_order', route=ROUTE, rho='64|tau|')
    check('floor_pair_met', admit_bound(Kf, targets['floor'][1]), q='148/390625', K=exact(Kf), target='1/12',
          margin=sci(targets['floor'][1] / Kf, 8), tier='exact_first_order', route=ROUTE, rho='tau_star=1/37888')
    crude_h, crude_f = pairs[('headline', 'crude_majorant')]['K'], pairs[('floor', 'crude_majorant')]['K']
    check('crude_tier_reported', crude_h > targets['headline'][1] and crude_f <= targets['floor'][1],
          headline_crude=dict(exact(crude_h), meets_headline_target=False, status='reported, not a target'),
          floor_crude=dict(exact(crude_f), meets_floor_target=True))

    # ------------------------------------------------ labelled refinements
    q_h = disc['headline']['q']
    refA_h, refA_f = Kh * q_h, Kf * disc['floor']['q']
    refB_h, refB_f = 2 * disc['headline']['remainder'], 2 * disc['floor']['remainder']
    refC_h = Kh / (1 - q_h)
    telesc_h = Kh * (2 - q_h) / (1 - q_h)
    telesc_sharp_h = Kh * q_h * (2 - q_h) / (1 - q_h)
    refB_ratio = (2 * 28 * 64 * TAU * Gp_up * (49 * 64 * TAU / 144) / (1 - 28 * 64 * TAU * Gp_up)) / \
        (2 * 28 * 64 * (TAU / 100) * Gp_up * (49 * 64 * (TAU / 100) / 144) / (1 - 28 * 64 * (TAU / 100) * Gp_up))
    check('labelled_refinements', refA_h < Kh and refB_h < Kh and refC_h > Kh and telesc_h > targets['headline'][1] > telesc_sharp_h,
          sharp_exponent={'headline_K_times_q': exact(refA_h), 'floor_K_times_q_min': exact(refA_f),
                          'label': 'labelled refinement (exponent N from the sharp lemma); not headline: absorbing q_min '
                                   'makes the floor constant linear in tau, against the prefrozen bracket'},
          first_order_cancellation={'headline': exact(refB_h), 'floor': exact(refB_f), 'tau_ratio_headline': sci(refB_ratio, 8),
                                    'label': 'labelled refinement: the exact first-order parts on supports containing u in R '
                                             'coincide (common core), so the circle bound is 2*28 rho G\'(R) T(rho); quadratic '
                                             'in tau, outside the prefrozen linear bracket; not headline'},
          cauchy_coefficient_form={'headline': exact(refC_h), 'label': 'weaker alternative M q^{n_0}/(1-q)'},
          telescoped_general={'headline': exact(telesc_h), 'meets_headline_target': telesc_h <= targets['headline'][1],
                              'headline_with_sharp_exponent': exact(telesc_sharp_h),
                              'label': 'telescoping route named in the contract: K(2-q)/(1-q) exceeds 1/2000000 at exponent N-1; '
                                       'the direct union comparison gives K, and the telescoped sum with the sharp exponent '
                                       'meets the target'})

    # ------------------------------------------------ scaling (item 6)
    ratios = {'K_exact_first_order_at_q_1_64': K_of('headline', 'exact_first_order', TAU) / K_of('headline', 'exact_first_order', TAU / 100),
              'K_floor_pair': K_of('floor', 'exact_first_order', TAU) / K_of('floor', 'exact_first_order', TAU / 100),
              'q_min': (28 * TAU * G_up / R) / (28 * (TAU / 100) * G_up / R)}
    for k, v in ratios.items():
        must(certify_scaling(v, brackets[k]), 'scaling ' + k)
    check('tau_scaling_per_constant', True, ratios={k: exact(v) for k, v in ratios.items()},
          brackets={k: [qs(v[0]), qs(v[1])] for k, v in brackets.items()},
          crude_ratios={'headline_crude': qs(K_of('headline', 'crude_majorant', TAU) / K_of('headline', 'crude_majorant', TAU / 100)),
                        'floor_crude': qs(K_of('floor', 'crude_majorant', TAU) / K_of('floor', 'crude_majorant', TAU / 100))})

    # ------------------------------------------------ coefficient Cauchy property
    series_tail = Kh * q_h ** 1 / (1 - q_h)
    check('coefficient_cauchy_in_N', series_tail < 1 and Kh * q_h ** 3 < Kh,
          statement='for N<=M<=M\' the direct comparison gives ||c(Lambda_M)-c(Lambda_M\')||_u <= K q^{N-1}; the whole '
                    'coefficient sequence on supports meeting R is Cauchy in each Q_L (from a Cauchy bound); no state, reduced '
                    'density or untruncated coefficient follows',
          rate_per_coarse_step='q=1/64 (headline) or 148/390625 (floor), per coarse step at fixed spacing')

    # ------------------------------------------------ fixtures
    nl = nonlocal_lipschitz_fixture()
    must(len(set(nl.values())) == 1, 'nonlocal fixture: value independent of the source distance')
    wf = chain_weight_fixture()
    n_w, lam_w = 4, Q(1, 4)
    toward = [Q(2) ** (n_w - i) for i in range(n_w + 1)]
    away = [Q(2) ** i for i in range(n_w + 1)]
    quad = [Q(2) ** ((n_w - i) ** 2) for i in range(n_w + 1)]
    unweighted = Q(1) / (1 - 2 * lam_w)
    b_toward, lip_toward = certify_weight_direction(toward, lam_w, Q(1), n_w, unweighted)
    must(abs(wf[0]) <= b_toward, 'toward-source weight bound holds')
    pole = normalization_pole_fixture()
    must(pole['inside_disc'] is True, 'normalization zero inside the disc')
    marg = marginal_fixture()
    must(marg['tn_sq'] > 0, 'marginal fixture')
    subX = ((0, 0, 0), (1, 0, 0))
    subI = [((-1, 0, 0), (0, 0, 0)), ((1, 0, 0), (2, 0, 0))]
    subM = ((-1, 0, 0), (2, 0, 0))
    must(subadditivity_ok(subX, subI, subM, 'sum') and diam(subM, 'linf') == 3, 'subadditivity fixture')
    n_supports, n_configs = exhaustive_subadditivity()
    kW = next(k for k, c in enumerate(OMITTED) if c['orient'] == 'xz' and c['r'] == 0 and c['s'] == 0)
    W_support = face_support((ORIGIN, kW))
    must(W_support == R_COVER and certify_reach('per_interaction', 1, 0, diam(W_support, 'linf'), 1), 'first-order reach')
    check('trap_fixtures_exact', True,
          nonlocal_lipschitz={'values_c0_by_source_distance': {str(d): qs(v) for d, v in nl.items()}, 'lipschitz': '1/2'},
          weight_direction={'fixed_point': [qs(x) for x in wf], 'toward_source_bound_at_R': qs(b_toward),
                            'toward_source_lipschitz': qs(lip_toward), 'unweighted_bound': qs(unweighted)},
          normalization_pole=pole, marginal={k: v for k, v in marg.items() if k != 'tn_sq'},
          subadditivity={'X': subX, 'creations': subI, 'M_disconnected': subM, 'diam_M': 3, 'sum_bound': 3, 'max_bound': 2,
                         'exhaustive_supports': n_supports, 'exhaustive_configurations': n_configs},
          first_order_reach={'support': W_support, 'interactions': 1, 'creations': 0, 'diameter': 1},
          chain_first_order=chain_first, model_is_finite_graph=True, transfers_to_aq=False)

    # ------------------------------------------------ Wilson cover
    kWf = kW
    links_R = [((4 * b[0] + r_, 2 * b[1] + s_, b[2]), j) for b in R_COVER for r_ in range(4) for s_ in range(2) for j in 'xyz']
    endpoints = {t for t, _ in links_R} | {vadd(t, E[j]) for t, j in links_R}
    W_links = face_links((0, 0, 0), 'x', 'z')
    W_owners = tuple(sorted({coarse(t) for t, _ in W_links}))
    must(certify_cover(W_owners, len(links_R), len(endpoints)), 'Wilson cover')

    # ------------------------------------------------ statements, gate fields, phrasing
    gate_fields = dict(pre['gate_fields_required'])
    flags = dict(gate_fields)
    must(validate_claim_flags(flags), 'claim flags')
    supported = ('For the zero-selected patterned family at the same coupling |tau| at most 10^-8 and the named construction '
                 'families F1 and F2 on centered coarse cubes Lambda_N, N at least 2, in each on-site cutoff space and uniformly in '
                 'the cutoff, the AM2 creation coefficients on supports containing a site u of R differ between two boxes by '
                 'at most K q^(N-1) in the anchored norm, with (q,K)=(1/64, 49/111790368) at the exact_first_order tier by '
                 'the analytic_disc route with rho=64|tau|, and (q,K)=(148/390625, 49/2018304) at the exact_first_order tier '
                 'with rho=tau_star=1/37888, for every comparison and both signs; the rate is in N at fixed spacing; this is '
                 'decay of coefficients, not decay of the reduced density, not a statement about untruncated creation '
                 'coefficients, not uniqueness of any ground state and not a statement uniform in the lattice spacing a.')
    for s in (supported, template, gate_fields['coefficient_cauchy_scope']):
        must(certify_no_placeholder(s), 'placeholder')
    must(certify_scope_statement(supported) and certify_uniformity_statement(supported), 'scope statement')
    report = (HERE / 'report.md').read_text()
    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings'])
    must(certify_phrasing(report, forbidden, template) and certify_phrasing(supported, forbidden, template), 'phrasing')
    must(certify_template_once(report, template), 'template quoted once')
    check('mandatory_template_and_statements', True, template_quoted_once_in_report=True, supported_statement=supported,
          phrase_scan='negation-aware whole-clause scan of report.md and the supported statement with the template removed: '
                      'no affirmative hit')

    # ================================================================ controls
    base = json.loads(raw)

    def coherent(mut):
        doc = json.loads(json.dumps(base))
        mut(doc)
        blob = json.dumps(doc, indent=2).encode()
        return blob, hashlib.sha256(blob).hexdigest()

    tampers = {
        'headline_K_target_relaxed': coherent(lambda d: d['parameters']['rate_constant_pair']['headline'].__setitem__('K_target', '1/1000')),
        'headline_q_changed': coherent(lambda d: d['parameters']['rate_constant_pair']['headline'].__setitem__('q', '1/32')),
        'gate_field_rate_in_a_true': coherent(lambda d: d['preregistration']['gate_fields_required'].__setitem__('rate_in_a_claimed', True)),
        'control_removed': coherent(lambda d: d['controls'].pop()),
        'isolation_flag_false': coherent(lambda d: d.__setitem__('reverse_premise_isolation', False)),
        'hash_binding_boolean_flipped': coherent(lambda d: d['preregistration']['hash_binding'].__setitem__(
            'check_py_sha256_recorded_before_full_size_evaluation', False)),
        'tau_changed': coherent(lambda d: d['preregistration']['tau'].__setitem__('value', '1/10000000')),
    }
    av1_rel = 'research/round32/advisor/av1-gate.json'
    av1_raw = (INPUTS / av1_rel).read_bytes()
    control('coherent_evidence_tampering',
            [(label, (lambda b=blob, h=digest: validate_contract_bytes(b, h))) for label, (blob, digest) in sorted(tampers.items())]
            + [('byte_change_without_rehash', lambda: validate_contract_bytes(raw + b' ', CONTRACT_SHA256)),
               ('declared_snapshot_removed', lambda: validate_inventory([f for f in inventory if 'am2-gate' not in f], contract)),
               ('admitted_gate_edited', lambda: validate_pinned(av1_rel, av1_raw.replace(b'585079838465912592144137406066050',
                                                                                          b'585079838465912592144137406066049')))],
            note='each tampered contract copy is rehashed coherently; semantic validation still rejects it')
    control('exact_arithmetic_admission', [
        ('float_tau', lambda: parse_q(1e-08)),
        ('bool_value', lambda: parse_q(True)),
        ('nan_string', lambda: parse_q('NaN')),
        ('zero_denominator', lambda: parse_q('1/0')),
        ('float_bound_admission', lambda: admit_bound(float(Kh), targets['headline'][1])),
    ], note='every Boolean is decided on Fraction values; decimal strings are truncated previews; no numerical library')
    control('no_priority_or_continuum_claim', [
        ('continuum_true', lambda: validate_claim_flags(dict(flags, continuum_claim=True))),
        ('priority_true', lambda: validate_claim_flags(dict(flags, scientific_priority_verified=True))),
        ('weak_coupling_true', lambda: validate_claim_flags(dict(flags, weak_coupling_claim=True))),
        ('historical_lens_as_premise', lambda: certify_premise_provenance('historical lens (Newton/Tesla)')),
        ('government_record_as_premise', lambda: certify_premise_provenance('governmental record')),
    ], flags={k: flags[k] for k in ('continuum_claim', 'scientific_priority_verified')})
    pk = {'model_id': 'AQ_patterned_zero_selected', 'triple': ['0', '0', '0'], 'tau': '1/100000000', 'group': 'SU(2)',
          'dimension': 3, 'J_per_tau': 28, 'families': [F1_NAME, F2_NAME], 'metric': 'coarse l-infinity, d_X=1',
          'disc_rule': {'headline': '64|tau|', 'floor': 'tau_star=1/37888'}, 'window': params['window'],
          'model_class': 'patterned zero-selected family'}
    must(certify_packet_model(pk, contract), 'packet model')
    control('changed_model_relabelled', [
        ('coupling_above_cap', lambda: certify_packet_model(dict(pk, tau='1/10000000'), contract)),
        ('nonzero_triple', lambda: certify_packet_model(dict(pk, triple=['0', '1/100', '0']), contract)),
        ('model_id_relabelled', lambda: certify_packet_model(dict(pk, model_id='AQ_uniform_route_B'), contract)),
        ('uniform_model_J_29', lambda: certify_packet_model(dict(pk, J_per_tau=29), contract)),
        ('other_group_SU3', lambda: certify_packet_model(dict(pk, group='SU(3)'), contract)),
        ('two_dimensional_lattice', lambda: certify_packet_model(dict(pk, dimension=2), contract)),
        ('finite_graph_result', lambda: certify_packet_model(dict(pk, model_class='finite graph (qubit chain fixture)'), contract)),
        ('metric_l1_relabelled', lambda: certify_packet_model(dict(pk, metric='coarse l1, d_X=2'), contract)),
        ('disc_rule_changed', lambda: certify_packet_model(dict(pk, disc_rule={'headline': '128|tau|', 'floor': 'tau_star=1/37888'}), contract)),
        ('window_changed', lambda: certify_packet_model(dict(pk, window='compact time window theta in [0,1]'), contract)),
    ], packet=pk)
    good = dict(disc_contraction=True, global_lipschitz_decay=False, pairs={'headline', 'floor'}, comparisons=4,
                tier='exact_first_order', metric_closes='linf')
    outcome = certify_outcome(producer_outcome(**good), good)
    must(outcome == 'accepted_within_scope', 'outcome')
    floor_only = dict(good, pairs={'floor'})
    crude_only = dict(good, tier='crude_majorant')
    l1_only = dict(good, metric_closes='l1')
    lip = dict(good, global_lipschitz_decay=True)
    nodisc = dict(good, disc_contraction=False)
    control('insufficient_verdict_retained', [
        ('floor_only_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', floor_only)),
        ('crude_only_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', crude_only)),
        ('l1_only_relabelled_accepted', lambda: certify_outcome('accepted_within_scope', l1_only)),
        ('global_lipschitz_relabelled_limited', lambda: certify_outcome('limited', lip)),
        ('failed_disc_relabelled_limited', lambda: certify_outcome('limited', nodisc)),
        ('crude_headline_admitted', lambda: admit_bound(crude_h, targets['headline'][1])),
        ('tau_retuned_for_crude_headline', lambda: certify_no_retuning(Q(1, 10 ** 12), TAU)),
    ], retained={'crude_headline_K': exact(crude_h), 'crude_headline_meets_target': False,
                 'rule': 'floor only, one comparison, crude only or l1 only -> limited; failed disc contraction or '
                         'global-Lipschitz decay -> insufficient'})
    quad_ratio = refB_ratio
    floor_absorbed_ratio = (Kf * 37888 * TAU) / (Kf * 37888 * (TAU / 100))
    control('tau_scaling_exponent', [
        ('first_order_cancellation_as_headline', lambda: certify_scaling(quad_ratio, brackets['K_exact_first_order_at_q_1_64'])),
        ('floor_constant_absorbing_q_min', lambda: certify_scaling(floor_absorbed_ratio, brackets['K_floor_pair'])),
        ('q_min_square_root_law', lambda: certify_scaling(Q(10), brackets['q_min'])),
        ('bracket_chosen_after_evaluation', lambda: certify_bracket_prefrozen((Q(9000), Q(11000)), brackets['K_exact_first_order_at_q_1_64'])),
    ], ratios={k: sci(v, 10) for k, v in ratios.items()})
    alpha_f, hbar_f = Q(5), Q(7)
    amp_norm = (-TAU / 3) / 24
    amp_alpha = (-TAU / 24) / 3
    must(certify_first_order_amplitude(amp_norm, TAU) and certify_first_order_amplitude(amp_alpha, TAU), 'amplitude')
    must(certify_clock('theta', 'alpha*t/hbar') and certify_clock('u', 'theta/8'), 'clock')
    control('wrong_delta_alpha_hbar_clock', [
        ('mixed_units_tau_over_9', lambda: certify_first_order_amplitude((-TAU / 3) / 3, TAU)),
        ('mixed_units_tau_over_576', lambda: certify_first_order_amplitude((-TAU / 24) / 24, TAU)),
        ('u_window_labelled_theta', lambda: certify_clock('theta', 'theta/8')),
        ('delta_clock_labelled_theta', lambda: certify_clock('theta', 'delta*t/hbar')),
    ], non_unit_fixture={'alpha': qs(alpha_f), 'hbar': qs(hbar_f), 'theta_per_t': qs(alpha_f / hbar_f),
                         'u_per_t': qs(alpha_f / 8 / hbar_f), 'u_over_theta': qs((alpha_f / 8) / alpha_f)},
        note='static coefficients carry no clock; the amplitude -tau/72 is unit-consistent in both systems')
    J_star = certify_J(4)
    control('missing_incoming_stars', [
        ('outgoing_star_only_J_7', lambda: certify_J(1)),
        ('orthant_two_stars', lambda: certify_J(2)),
        ('source_count_outgoing_anchor_only', lambda: certify_source_site_count(21)),
        ('disc_radius_from_J_7', lambda: certify_disc(4 * tau_star, G_up, Gp_up, R, tau_star, 'evaluated at the declared rho')),
    ], J_per_tau=J_star, enumerated_max_stars_per_site=4)
    control('root_n_misuse', [
        ('sqrt49_first_order', lambda: certify_l1(7 * TAU / 144, 49, TAU / 144)),
        ('sqrt82_R_sum', lambda: certify_l1(10 * TAU / 144, 82, TAU / 144)),
        ('rss_of_two_balls', lambda: certify_combination([disc['headline']['T'], disc['headline']['T']], 'rss')),
        ('division_by_sqrt_N', lambda: certify_no_volume_division(2)),
    ], linear_two_balls=exact(2 * disc['headline']['T']))
    control('tier_mixing_rejected', [
        ('first_order_cancellation_with_crude_t_labelled_exact', lambda: certify_tier_constant('exact_first_order', ROUTE, 'crude_592_rho', 'two_balls')),
        ('t1_without_self_consistency', lambda: certify_tier_constant('exact_first_order', ROUTE, 't1_only', 'two_balls')),
        ('tier_outside_vocabulary', lambda: certify_tier_constant('weighted_ii', ROUTE, 'self_consistent_T(rho)', 'two_balls')),
        ('route_outside_vocabulary', lambda: certify_tier_constant('exact_first_order', 'lieb_robinson', 'self_consistent_T(rho)', 'two_balls')),
        ('crude_constant_labelled_exact', lambda: certify_tier_constant('crude_majorant', ROUTE, 'self_consistent_T(rho)', 'two_balls')),
    ], constants={'headline': 'exact_first_order/analytic_disc', 'floor': 'exact_first_order/analytic_disc',
                  'crude': 'crude_majorant/analytic_disc (reported separately)'})
    control('reverse_premise_isolation', [
        ('forward_ba1_added', lambda: validate_inventory(inventory + ['research/round33/forward/ba1/report.md'], contract)),
        ('skeptic_triage_added', lambda: validate_inventory(inventory + ['research/round33/skeptic/triage.md'], contract)),
        ('deliberation_added', lambda: validate_inventory(inventory + ['research/round33/advisor/deliberation-2.md'], contract)),
        ('lens_memo_added', lambda: validate_inventory(inventory + ['research/round33/experts/newton/memo.md'], contract)),
        ('premise_missing', lambda: validate_inventory(inventory[1:], contract)),
    ], inventory_size=len(inventory))
    recomputed = {'faces_per_factor': 49, 'owner_sets_per_factor': 15, 'faces_meeting_R': 82, 'faces_inside_R': 10}
    control('face_count_all_sites', [
        ('literal_counts', lambda: certify_face_counts(recomputed, 'literal copied from the contract', counts)),
        ('site_0_anchor_only', lambda: certify_face_counts(dict(counts, faces_per_factor=21),
                                                           'translation covariance over the anchors u-S from the I1 table', recomputed)),
        ('anchors_in_R_as_meeting_R', lambda: certify_face_counts(dict(counts, faces_meeting_R=42),
                                                                  'translation covariance over the anchors u-S from the I1 table', recomputed)),
    ], derived=counts)
    control('uniform_in_N_not_in_a', [
        ('uniform_in_lattice_spacing', lambda: certify_uniformity_statement('the bound is uniform in the lattice spacing a')),
        ('unqualified_uniform_rate', lambda: certify_uniformity_statement('the rate q=1/64 is uniform')),
    ], statement='every uniformity statement reads: in N at fixed spacing (and uniformly in the cutoff)')
    control('placeholder_span_rejected', [
        ('angle_span_with_space', lambda: certify_no_placeholder(supported.replace('49/111790368', '<K value>'))),
        ('angle_span_with_bar', lambda: certify_no_placeholder('rate <q|K> frozen')),
        ('angle_span_eg', lambda: certify_no_placeholder('radius <e.g.64tau>')),
    ])
    control('negation_aware_phrase_scan', [
        ('affirmative_thermodynamic_limit', lambda: certify_phrasing(report + '\nThe thermodynamic limit of the coefficients exists.', forbidden, template)),
        ('affirmative_AQ_state', lambda: certify_phrasing(supported + ' It identifies the AQ state.', forbidden, template)),
        ('affirmative_unique_limit', lambda: certify_phrasing('The coefficients have a unique limit state.', forbidden, template)),
    ], negated_accepted=certify_phrasing('This is not the thermodynamic limit.', forbidden, template))

    def drop_param(key):
        return coherent(lambda d: d['parameters'].pop(key))
    control('parameters_declare_metric_weights_window', [
        ('metric_removed', lambda: validate_contract_bytes(*drop_param('metric'))),
        ('weights_removed', lambda: validate_contract_bytes(*drop_param('weights'))),
        ('window_removed', lambda: validate_contract_bytes(*drop_param('window'))),
        ('clock_removed', lambda: validate_contract_bytes(*drop_param('clock'))),
    ], declared=list(PARAM_KEYS))
    no_decay = J0 * G_up / (1 - J0 * Gp_up)
    must(no_decay == Q(37, 6249384), 'no-decay global bound')
    control('global_lipschitz_not_decay', [
        ('lipschitz_power_as_decay_factor', lambda: certify_decay_factor('global Lipschitz 2J_0G\'(R)', 2 * J0 * Gp_up, q_h)),
        ('nonlocal_fixture_lipschitz_power_claim', lambda: certify_decay_claim(nl[5], Q(1, 2) ** 5)),
        ('no_decay_bound_as_rate', lambda: certify_decay_factor('global Lipschitz J_0G\'(R)', no_decay, q_h)),
    ], no_decay_bound=exact(no_decay), N_dependence='none (the same number for every N)',
        nonlocal_fixture={'c0': qs(nl[5]), 'claimed_L_power_5': qs(Q(1, 2) ** 5)})
    control('weighted_norm_contraction_rechecked', [
        ('real_cap_constants_cited_for_disc', lambda: certify_disc(tau_star, G_up, Gp_up, R, tau_star, 'AM2 real cap J_0G(R)<R')),
        ('radius_above_tau_star', lambda: certify_disc(2 * tau_star, G_up, Gp_up, R, tau_star, 'evaluated at the declared rho')),
        ('unweighted_lipschitz_for_disc', lambda: certify_lipschitz_value(tau_star, Q(77, 781250), Gp_up)),
    ], disc_values={w: {'self_map': qs(d['self_map_value']), 'kappa': qs(d['kappa'])} for w, d in disc.items()})
    control('loss_per_interaction_not_per_creation', [
        ('per_creation_reach_first_order_face', lambda: certify_reach('per_creation', 1, 0, diam(W_support, 'linf'), 1)),
        ('per_creation_reach_chain_first_order', lambda: certify_reach('per_creation', 1, 0, 1, 1)),
    ], fixture='first-order face vector W Omega_0 on {0,e_z}: one interaction, zero creations, output diameter 1 = d_X')
    control('diameter_subadditivity_through_interaction', [
        ('max_instead_of_sum', lambda: subadditivity_ok(subX, subI, subM, 'max')),
    ], fixture={'X': subX, 'I': subI, 'M_equals_N_minus_X': subM, 'disconnected': True, 'diam_M': 3},
        exhaustive={'supports': n_supports, 'configurations': n_configs, 'sum_rule_holds': True})
    control('coarse_metric_named', [
        ('l1_distance_with_linf_diameter', lambda: certify_metric('l1', 1)),
        ('linf_distance_with_l1_diameter', lambda: certify_metric('linf', 2)),
    ], metric='coarse l-infinity on factor sites, d_X=1 (l1 alternative d_X=2 tabulated, never mixed)')
    control('weight_direction_toward_source', [
        ('weight_growing_from_R', lambda: certify_weight_direction(away, lam_w, Q(1), n_w, unweighted)),
        ('non_submultiplicative_quadratic_weight', lambda: weighted_bound_at_R(quad, lam_w, Q(1), n_w)),
        ('exponent_from_observed_support', lambda: certify_exponent_basis('distance of the observed support from R')),
    ], toward_source={'bound_at_R': qs(b_toward), 'lipschitz': qs(lip_toward)},
        reversed_weight_bound_at_R=qs(Q(1) * away[n_w] / (1 - Q(5, 8)) / away[0]), unweighted=qs(unweighted))
    q_card_lower = root4_lower(q_min)
    control('cardinality_weight_rate_labelled', [
        ('cardinality_relabelled_diameter_rate', lambda: certify_card_rate('cardinality', q_min, 4, q_min, q_card_lower)),
        ('cardinality_loss_e_mu', lambda: certify_card_rate('cardinality', q_card_lower, 1, q_min, q_card_lower)),
    ], cardinality_rate_lower=exact(q_card_lower), note='order >= |I|/4 gives the per-site rate q^(1/4) >= 0.1395 at the floor '
                                                         'disc; not used')
    N0 = 3
    inv1 = sorted(F1[N0 + 1] - F1[N0])
    stars_o, stars_n = set(pieces_f1(boxes[N0])), set(pieces_f1(boxes[N0 + 1]))
    inv_st = sorted(stars_n - stars_o)
    shell0 = set(boxes[N0 + 1] - boxes[N0])
    inv3 = sorted(F2[N0] - F1[N0])
    control('boundary_distance_exact', [
        ('nested_shell_distance_N', lambda: certify_source_distance(inv1, N0)),
        ('f2_outer_layer_at_N', lambda: certify_source_distance(inv3, N0)),
        ('shell_distance_sharp_exponent_in_chain_fixture', lambda: certify_vanishing_order(
            1 + chain_rows[-1]['far_endpoint_distance'], chain_rows[-1]['first_differing_order'])),
    ], derived={'nested_source_terms': N0 - 1, 'shell_e_z': N0, 'shell_0': N0 + 1, 'f2_outer_layer': N0 - 1})
    old_star = (0, 0, 0)
    control('boundary_source_new_terms_only', [
        ('old_star_charged', lambda: validate_source(inv_st + [old_star], stars_o, stars_n, shell0, support=star)),
        ('source_missing_a_new_star', lambda: validate_source(inv_st[1:], stars_o, stars_n, shell0, support=star)),
        ('term_not_meeting_source_set', lambda: validate_source(inv_st + [old_star], stars_o - {old_star}, stars_n, shell0,
                                                                support=star)),
        ('old_face_charged_f2', lambda: validate_source(sorted(F2[N0 + 1] - F2[N0]) + [next(iter(sorted(F2[N0])))],
                                                        F2[N0], F2[N0 + 1], shell0)),
    ], terms='F1 nested: whole stars (each meets the shell); F2 nested: faces (each meets the shell); F1 vs F2: faces '
             '(each meets the positive outer layer)')
    inv2 = sorted(F2[N0 + 1] - F2[N0])
    gaining_anchor = (0, 0, N0)
    whole_group = sorted(set(inv2) | {f for f in F2[N0] if f[0] == gaining_anchor})
    control('f2_regrouping_charged_once', [
        ('gaining_group_charged_whole', lambda: validate_f2_charge(whole_group, F2[N0], F2[N0 + 1])),
        ('face_charged_twice', lambda: validate_f2_charge(inv2 + [inv2[0]], F2[N0], F2[N0 + 1])),
    ], per_site_face_sum='at most 49|tau|/3 (face by face) <= J=28|tau|')
    control('rate_constant_pair_prefrozen', [
        ('headline_q_optimized', lambda: certify_pair(Q(1, 128), targets['headline'][1], contract, 'headline')),
        ('floor_K_target_changed', lambda: certify_pair(targets['floor'][0], Q(1, 4), contract, 'floor')),
        ('rho_optimized_per_N', lambda: certify_rho_rule('argmin over rho of 2T(rho)(|tau|/rho)^(N-1)')),
    ], frozen={'headline': ['1/64', '1/2000000'], 'floor': ['148/390625', '1/12']})
    control('q_min_not_crossed', [
        ('rate_half_q_min', lambda: certify_rate_floor(q_min / 2, q_min, 'R=1/64')),
        ('disc_twice_tau_star', lambda: certify_disc(2 * tau_star, G_up, Gp_up, R, tau_star, 'evaluated at the declared rho')),
    ], q_min=exact(q_min), floor_q=exact(disc['floor']['q']))
    control('analytic_route_disc_radius', [
        ('reduced_density_analytic_on_disc', lambda: certify_analytic_object('reduced density rho_R', False)),
        ('normalization_analytic_on_disc', lambda: certify_analytic_object('complexified normalization', False)),
        ('radius_rho_R_beyond_tau_star', lambda: certify_disc(Q(1, 30000), G_up, Gp_up, R, tau_star, 'evaluated at the declared rho')),
    ], pole_fixture=pole, disc_radii={'headline': '64|tau|', 'floor': '1/37888'})
    control('untruncated_coefficients_not_asserted', [
        ('untruncated_asserted', lambda: certify_scope_statement('the untruncated creation coefficients differ by at most K q^(N-1) in each on-site cutoff space')),
        ('no_cutoff_named', lambda: certify_scope_statement('the creation coefficients differ by at most K q^(N-1)')),
        ('cutoff_removed_for_coefficients', lambda: certify_scope_statement('in each on-site cutoff space, and then with the cutoff removed')),
    ])
    control('decay_rate_in_N_not_a', [
        ('per_fermi', lambda: certify_rate_unit('per fm')),
        ('per_lattice_spacing', lambda: certify_rate_unit('per lattice spacing a as a -> 0')),
        ('physical_length_scale', lambda: certify_rate_unit('physical correlation length')),
    ], unit='per coarse step at fixed spacing (a coarse step is (4a,2a,a))')
    control('coefficient_decay_not_marginal_decay', [
        ('state_decay_inferred', lambda: certify_state_inference(0, marg['tn_sq'], 'state decay from coefficient decay')),
    ], fixture={k: v for k, v in marg.items() if k != 'tn_sq'})
    control('two_families_named', [
        ('single_family', lambda: certify_families([F1_NAME])),
        ('unfrozen_class', lambda: certify_families([F1_NAME, 'all boundary conditions'])),
        ('F2_collapsed_onto_F1', lambda: certify_family_is_F2(F1[2], F2[2], F1[2])),
    ], families=[F1_NAME, F2_NAME])
    control('subsequence_versus_whole_sequence', [
        ('whole_sequence_states', lambda: certify_limit_statement('reduced density on R', 'whole sequence', 'Cauchy bound')),
        ('whole_sequence_without_cauchy', lambda: certify_limit_statement('AM2 creation coefficients on supports meeting R in each Q_L',
                                                                          'whole sequence', 'uniform bound')),
        ('unquantified_limit', lambda: certify_limit_statement('AM2 creation coefficients on supports meeting R in each Q_L', 'the limit', 'Cauchy bound')),
    ], allowed='whole sequence of coefficients from the Cauchy bound; states: none')
    control('full_original_wilson_cover', [
        ('four_drawn_links', lambda: certify_cover(W_owners, 4, 6)),
        ('single_factor', lambda: certify_cover((ORIGIN,), 24, 22)),
    ], cover={'owners_of_W_links': W_owners, 'links': len(links_R), 'endpoints': len(endpoints)})
    control('gate_fields_topic_specific', [
        ('ay1_fields_reused', lambda: certify_gate_fields({'uniqueness_claimed': False, 'whole_sequence_claimed': False,
                                                           'rate_claimed': False}, pre['gate_fields_required'])),
        ('coefficient_cauchy_missing', lambda: certify_gate_fields({k: v for k, v in gate_fields.items() if k != 'coefficient_cauchy_claimed'},
                                                                   pre['gate_fields_required'])),
        ('rate_in_N_false', lambda: certify_gate_fields(dict(gate_fields, rate_in_N_claimed=False), pre['gate_fields_required'])),
        ('state_decay_true', lambda: certify_gate_fields(dict(gate_fields, state_decay_claimed=True), pre['gate_fields_required'])),
    ], gate_fields=gate_fields)
    control('ball_radius_not_used_as_tree_decay_ratio', [
        ('ball_radius_as_ratio', lambda: certify_rate_provenance('ball radius R=1/64 as per-step tree ratio')),
        ('unchecked_disc', lambda: certify_rate_provenance('disc radius 64|tau| without contraction check')),
    ], provenance={'headline': 'disc radius rho=64|tau| (q=|tau|/rho), disc contraction checked',
                   'floor': 'disc radius rho=tau_star=1/37888 (q=|tau|/rho=37888|tau|), disc contraction checked'})
    must(certify_rate_provenance('disc radius rho=64|tau| (q=|tau|/rho), disc contraction checked'), 'provenance')
    must(certify_decay_factor('analytic_disc ratio |tau|/rho', q_h, q_h), 'decay factor')

    n_mut = sum(len(c.get('rejected_mutations', {})) for c in CHECKS)
    pins = [qs(Kh), qs(Kf), qs(crude_h), qs(crude_f), qs(ratios['K_exact_first_order_at_q_1_64']), qs(no_decay),
            qs(disc['headline']['kappa']), qs(disc['floor']['kappa']), qs(disc['headline']['T']), qs(disc['floor']['T']),
            qs(disc['headline']['t1']), qs(disc['floor']['t1']), qs(refA_h), qs(refA_f), qs(refB_h), qs(refB_f), qs(refC_h),
            qs(telesc_h), qs(telesc_sharp_h), qs(disc['headline']['remainder']), qs(disc['floor']['remainder']),
            qs(targets['headline'][1] / Kh), qs(e_hi), qs(tau_star), qs(q_min), qs(marg['tn_sq']), qs(wf[0]),
            'on %d supports meeting a star and on %d configurations' % (n_supports, n_configs),
            '**%d exact checks**' % (len(CHECKS) + 1), '(%d mutations in total)' % n_mut,
            '(82, 1044 and 3910 faces within distance `N-2`)'] + [table_row_text(N, tables) for N in (2, 3, 4)]
    must(core_ok['2']['faces_within_N_minus_2'] == 82 and core_ok['3']['faces_within_N_minus_2'] == 1044
         and core_ok['4']['faces_within_N_minus_2'] == 3910, 'core counts')
    must(certify_report_pins(report, pins), 'report pins')
    control_free_check_ok = rejected(lambda: certify_report_pins(report.replace(qs(Kh), '49/111790369'), pins), 'edited report')
    check('report_carries_checker_values', True, pins=len(pins), edited_report_rejected=control_free_check_ok,
          note='every headline constant, ratio, refinement, the order-versus-distance table rows, the fixture counts and the '
               'check/mutation counts appear verbatim in report.md')
    ids = [c['id'] for c in CHECKS]
    missing = [c for c in contract['controls'] if c not in ids]
    must(missing == [], 'contract controls without a check: ' + ','.join(missing))
    must(sorted(MUTATION_CONTROLS) == sorted(contract['controls']), 'every contract control carries damaging mutations')

    def pair_json(which, tier):
        v = pairs[(which, tier)]
        return {'q': qs(v['q']), 'K': exact(v['K']), 'K_target': qs(targets[which][1]), 'target_comparator': '<=',
                'target_met': v['meets'], 'margin': sci(targets[which][1] / v['K'], 8), 'tier': tier, 'route': ROUTE,
                'disc_radius': '64|tau| (1/1562500 at the cap)' if which == 'headline' else 'tau_star=1/37888',
                'contraction_kappa': qs(disc[which]['kappa']), 'self_map_28rhoG': qs(disc[which]['self_map_value']),
                'signs': {'+': v['meets'], '-': v['meets']}, 'sign_note': 'the -tau value replays the same |tau| formula'}

    headline = {
        'headline_pair': pair_json('headline', 'exact_first_order'),
        'floor_pair': pair_json('floor', 'exact_first_order'),
        'crude_tier_headline_q': pair_json('headline', 'crude_majorant'),
        'crude_tier_floor_q': pair_json('floor', 'crude_majorant'),
        'exponent': 'N-1 (order-versus-distance count in the contract form; the sharp count gives N, labelled refinement)',
        'source_distance_all_comparisons': 'N-1 (coarse l-infinity), derived by enumeration (N=2,3,4) and the common-core argument',
        'diameter_convention': 'l-infinity, d_X=1, used by the proof; l1 (d_X=2) tabulated as the labelled alternative',
    }
    result = {
        'loop': 'BA1', 'direction': 'reverse',
        'route': 'complex-coupling analyticity of the AM2 fixed point on |z|<=rho, order-versus-distance count, '
                 'Cauchy estimate (maximum-modulus/Schwarz form)',
        'human_author': contract['human_author'],
        'ai_assistance': 'AI-assisted reverse production (Claude, an AI model); correlated model-agent work, not human review',
        'contribution_alias': 'HNM-BA1-R reverse analytic-disc boundary decay of AM2 creation coefficients',
        'attribution': {
            'analysis': 'standard: Banach fixed point, Weierstrass uniform limits of holomorphic maps, maximum modulus and Cauchy '
                        'estimates, connected-cluster support of perturbation expansions',
            'creation_expansion': 'admitted AM2 construction (Bravyi-DiVincenzo-Loss lineage; Gauvin arXiv:2503.15539v3 '
                                  'A.6-A.8 as AM2 template)',
            'scientific_priority': 'unverified'},
        'contract_sha256': contract_sha,
        'check_py_sha256_recorded_before_evaluation': check_py_sha,
        'admitted_gate_sha256_pinned': dict(PINNED_GATES),
        'model': contract['model'],
        'families': {'F1': F1_NAME, 'F2': F2_NAME},
        'cover': 'R={0,e_z} (complete cover of the original xz Wilson loop: 48 links, 36 endpoints, 7 incident anchors)',
        'metric': 'coarse l-infinity on factor sites, d_X=1',
        'disc_radii': {'headline': '64|tau|', 'floor': 'tau_star=1/37888'},
        'label': 'boundary_decay_rate_only',
        'secondary_label': 'static_not_dynamic',
        'headline': headline,
        'targets_read_from_contract': {'headline': [qs(targets['headline'][0]), qs(targets['headline'][1])],
                                       'floor': [qs(targets['floor'][0]), qs(targets['floor'][1])],
                                       'reference_value_exact': pre['observable']['reference_value_exact']},
        'order_versus_distance_tables': tables,
        'error_ledger': {
            'weighted_contraction_loss': {'reading': 'disc contraction (reverse analogue of the weighted loss)',
                                          'headline': {'self_map': qs(disc['headline']['self_map_value']), 'kappa': qs(disc['headline']['kappa']),
                                                       'circle_factor_rho_over_tau': '64'},
                                          'floor': {'self_map': qs(disc['floor']['self_map_value']), 'kappa': qs(disc['floor']['kappa']),
                                                    'circle_factor_rho_over_tau': '37888 at |tau|=1, i.e. 1/q_min'}},
            'boundary_source_terms': {'value': 'enters only through its distance N-1 (vanishing order); no norm charge in K',
                                      'audit': 'face-by-face per-site source sum at most 49|tau|/3 <= J'},
            'order_versus_distance_count': {'exponent_used': 'N-1', 'sharp_exponent': 'N (labelled refinement)'},
            'exact_first_order_remainder': {'headline_per_box': exact(disc['headline']['remainder']),
                                            'floor_per_box': exact(disc['floor']['remainder']),
                                            'note': '28 rho G\'(R) T(rho), included in T(rho) and therefore in K'},
            'cutoff_uniformity': {'value': 'not_applicable as a numeric cost',
                                  'reason': 'every constant is independent of L; first-order face vectors are kept exactly '
                                            'for L>=24 and first-order counts only decrease for L<24'},
            'arithmetic': {'value': 'not_applicable as a numeric cost',
                           'reason': 'exact Fractions; the only enclosure is the directed exp(1/8)<8/7; decimals are '
                                     'truncated previews'}},
        'supported_statement': supported,
        'mandatory_sentence_template': template,
        'gate_fields': gate_fields,
        'contract_controls_covered': list(contract['controls']),
        'controls_with_damaging_mutations': sorted(MUTATION_CONTROLS),
        'controls_not_implementable_as_mutations': [],
        'routes_executed': [
            'item 1: complexified AM2 map on |z|<=rho; itemized z-dependence of HNM-AM2.5; exact disc self-map and Lipschitz at '
            'rho=64|tau| and rho=tau_star; analyticity by uniform limits of polynomial iterates; tiers on the circle',
            'item 2: connected-family lemma and order-versus-distance count (contract form ceil(d/diam), sharp 1+ceil(d/diam)); '
            'tables on Lambda_2..Lambda_4 for l-infinity and l1; qubit-chain sharpness fixture',
            'item 3: exact source inventories and distances for F1 nested, F2 nested (face by face), F1 vs F2 (28N(5N+1)) and '
            'general volumes; common-core all-size argument',
            'item 4: Schwarz-lemma form of Cauchy estimate with the two-ball circle bound; headline and floor pairs at both '
            'signs; crude tier reported; labelled refinements',
            'item 5: coefficient decay versus reduced-density decay fixture; mandatory template quoted once; gate fields',
            'item 6: tau/100 scaling per constant; exact trap fixtures; 37 contract controls as damaging mutations'],
        'exclusions': {'contract': contract['claim_exclusions'], 'preregistration': pre['claim_exclusions']},
        'sub_labels': ['boundary_decay_rate_only', 'static_not_dynamic'],
        'proposed_reverse_verdict': outcome,
        'damaging_mutations_total': sum(len(c.get('rejected_mutations', {})) for c in CHECKS),
        'outcome_note': 'proposed for the reverse half only; acceptance needs both routes and skeptical review',
        'checks': CHECKS,
    }
    result.update({'continuum_claim': False, 'uniqueness_of_ground_state_claimed': False, 'state_decay_claimed': False,
                   'rate_in_a_claimed': False, 'scientific_priority_verified': False})
    for k, v in gate_fields.items():
        must(result['gate_fields'][k] == v, 'gate field export')
    return result


def main():
    ap = argparse.ArgumentParser(description='HNM-BA1 reverse producer checker (exact arithmetic)')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('check.py: --output must be an absolute path')
    if out.exists():
        raise SystemExit('check.py: --output must be a fresh directory')
    resolved = out.resolve()
    if resolved == ROOT or ROOT in resolved.parents:
        raise SystemExit('check.py: --output must lie outside the checkout')
    result = compute()
    out.mkdir(parents=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    sources = {p.relative_to(HERE).as_posix(): sha256_file(p) for p in sorted(HERE.rglob('*'))
               if p.is_file() and (p.relative_to(HERE).parts[0] == 'inputs' or p.name in ('check.py', 'report.md'))
               and p.relative_to(HERE).parts[0] != 'output'}
    manifest = {'loop': 'BA1', 'direction': 'reverse', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha256_file(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    hp = result['headline']
    print(json.dumps({'loop': 'BA1', 'direction': 'reverse', 'checks': len(result['checks']),
                      'headline_K': hp['headline_pair']['K']['preview'], 'floor_K': hp['floor_pair']['K']['preview'],
                      'controls': len(result['controls_with_damaging_mutations']),
                      'outcome': result['proposed_reverse_verdict']}, sort_keys=True))


if __name__ == '__main__':
    main()
