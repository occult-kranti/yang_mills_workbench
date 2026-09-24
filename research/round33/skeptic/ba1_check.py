#!/usr/bin/env python3
"""Round33 BA1 skeptic pre-comparison checker (zero-selected patterned family).

Written after the BA1 contract froze (sha256 2c761366...2b9, frozen
2026-09-24T21:56:46Z), from the frozen contract, advisor/selection-ba1.md,
advisor/deliberation-2.md, advisor/plan.json, the skeptic's own Round33 record
and the declared premises (AM2 forward, reverse, skeptic review and gate; AQ1;
I1; AV1, AW1, AY1 and AY2 reports and gates), before reading
research/round33/forward/ba1/ or research/round33/reverse/ba1/. Nothing is
imported from any producer, assistant or tool. Standard library only. Every
admission Boolean is decided with fractions.Fraction and directed enclosures
(exp from above by its Taylor polynomial plus a geometric tail, square roots by
integer brackets); floats appear only in the labelled 'previews' block. Every
check and control raises an explicit exception, so python -O cannot disable it.
Model-agent skeptic with correlated ancestry; not human peer review.

What is derived here:
  * the I1 face classes, the star S={0,e_x,e_y,e_z} and every omitted face
    owner set with their coarse l-infinity and l1 diameters (1 and 2), the
    counts 49/15/82/10 and the incidence on R={0,e_z}, enumerated on Lambda_2
    and Lambda_3;
  * the weighted AM2 contraction in ||c||_w = max_u sum_{I ni u} w^{diam I}||c_I||
    (loss w^{d_X} once per interaction; self-map J_0 w G(R) at most R, i.e. w at
    most 390625/148; Lipschitz J_0 w G'(R)), checked on every admissible creation
    word of order at most two built from actual owner sets;
  * the order-versus-distance lemma (first nonzero Taylor order of a coefficient
    difference at u is at least 1+d(u,S)/d_X) with tables for the coarse
    l-infinity and l1 conventions on Lambda_2..Lambda_4, the exact chain orders
    by breadth-first search, and an algebraic qubit-chain fixture;
  * the boundary sources and exact distances of every comparison (F1 N to N+1,
    F2 N to N+1, F1 versus F2 with 28N(5N+1) faces, general volumes);
  * the coefficient-difference constants at the frozen headline and floor pairs
    by both routes, both signs, the crude tier, the tau/100 ratios;
  * exact fixtures for the traps, and a packet validator executing all 37
    contract controls as damaging mutations.

Usage: python3 -B research/round33/skeptic/ba1_check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from collections import deque
from fractions import Fraction as F
from itertools import combinations, product
from math import comb, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = 'research/round33/contracts/ba1.json'
CONTRACT = ROOT / CONTRACT_REL
CONTRACT_SHA256 = '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9'
PINNED = {
    'research/round21/forward/i1/report.md': '836a4c7d421f0ddf3589c159d2f057839421532c88157a054a61b51c25c781a9',
    'research/round29/forward/am2/report.md': '1b58fb9c1a199f06b156d04c2a9e89f34ba63cf675a5f7c8bfc25bb568e4e019',
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round32/advisor/av1-gate.json': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
}

DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN, E_Z = (0, 0, 0), (0, 0, 1)
R_COVER = (ORIGIN, E_Z)
MODEL_ID = 'AQ_patterned_zero_selected'
CLOCK = 's=alpha*t_E/hbar, theta=alpha*t/hbar'
WINDOW = 'not applicable (static coefficients)'
UNIFORM_IN = 'N at fixed spacing'
RATE_UNITS = 'per coarse l_inf step at fixed spacing'
R = F(1, 64)
G_R, GP_R = F(148, 7), F(352)
TIERS = ('crude_majorant', 'exact_first_order')
ROUTES = ('weighted_norm', 'analytic_disc')
# Mirror of research/round33/tools/phrase_scan.py ROUND_FORBIDDEN and NEGATION (not imported).
ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state',
]
NEGATION = re.compile(r"\b(not|never|no|nor|neither|without|excludes?|excluded|exclusion|forbidden|"
                      r"cannot|does not|is not|are not|nothing|none)\b", re.I)
# Mirror of the freezer's rule R1 detector (research/round33/tools/freeze_contract.py), not imported.
PLACEHOLDER = re.compile(r'<(?![=<>])([^<>=]*)(?<![-=|])>(?!=)')


class Rejected(Exception):
    """Raised by the validator when it refuses a packet; controls require it."""


class CheckFailure(RuntimeError):
    """Raised when a required check or control fails."""


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise CheckFailure(cid)
    if any(row['id'] == cid for row in CHECKS):
        raise CheckFailure('duplicate check id ' + cid)
    row = {'id': cid, 'passed': True}
    row.update(detail)
    CHECKS.append(row)


def rejects(fn, reason):
    try:
        fn()
    except Rejected as exc:
        if reason not in str(exc):
            raise CheckFailure('rejected for the wrong reason: %s (expected %s)' % (exc, reason))
        return True
    return False


def accepts(fn):
    try:
        fn()
    except Rejected:
        return False
    return True


def control(cid, mutations, positives=(), **detail):
    rows = []
    for label, fn, reason in mutations:
        if not rejects(fn, reason):
            raise CheckFailure('control %s: mutation %s accepted' % (cid, label))
        rows.append({'mutation': label, 'rejected_for': reason})
    pos = []
    for label, fn in positives:
        if not accepts(fn):
            raise CheckFailure('control %s: positive %s rejected' % (cid, label))
        pos.append(label)
    need(True, cid, kind='control', mutations=rows, positives=pos, **detail)


def q(x):
    return str(x)


def preview(x):
    return format(float(x), '.12e')


def fact(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def exp_up(x, n=12):
    """Directed upper bound of e^x for 0<=x<n+2: Taylor polynomial plus geometric tail."""
    x = F(x)
    if x < 0 or x >= n + 2:
        raise CheckFailure('exp_up domain')
    s = sum((x ** k / fact(k) for k in range(n + 1)), F(0))
    return s + x ** (n + 1) / fact(n + 1) / (1 - x / (n + 2))


def exp_lo(x, n=12):
    x = F(x)
    if x < 0:
        raise CheckFailure('exp_lo domain')
    return sum((x ** k / fact(k) for k in range(n + 1)), F(0))


def _order(x):
    return 12 if x >= F(1, 100) else 4


def g_up(t):
    return 16 * exp_up(8 * t, _order(8 * t)) * (1 + 10 * t)


def gp_up(t):
    return 16 * exp_up(8 * t, _order(8 * t)) * (18 + 80 * t)


def sqrt_bracket(n, scale=10 ** 12):
    r = isqrt(n * scale * scale)
    lo = F(r, scale)
    hi = lo if r * r == n * scale * scale else F(r + 1, scale)
    if not (lo * lo <= n <= hi * hi):
        raise CheckFailure('sqrt bracket')
    return lo, hi


def add(a, b):
    return tuple(i + j for i, j in zip(a, b))


def sub(a, b):
    return tuple(i - j for i, j in zip(a, b))


def dinf(p, r):
    return max(abs(x - y) for x, y in zip(p, r))


def d1(p, r):
    return sum(abs(x - y) for x, y in zip(p, r))


def diam(pts, metric):
    pts = list(pts)
    return max((metric(a, b) for a in pts for b in pts), default=0)


def set_dist(u, pts, metric):
    return min(metric(u, p) for p in pts)


def ceil_div(a, b):
    return -((-a) // b)


# ---------------------------------------------------------------- geometry (I1)
def pi_map(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    ea, ec = DIRS[a], DIRS[c]
    return ((p, a), (p, c), (add(p, ea), c), (add(p, ec), a))


def owner_set(p, a, c):
    return frozenset(pi_map(tail) for tail, _ in face_links(p, a, c))


def is_selected(p, a, c):
    return (a, c) == ('x', 'y') and p[0] % 4 in (0, 1, 2) and p[1] % 2 == 0


def anchor_classes():
    out = []
    for r, s in product(range(4), range(2)):
        p = (r, s, 0)
        for a, c in ORIENT:
            out.append({'orient': a + c, 'r': r, 's': s, 'rel': owner_set(p, a, c), 'selected': is_selected(p, a, c),
                        'links': face_links(p, a, c)})
    return out


CLASSES = anchor_classes()
OMITTED = [k for k in CLASSES if not k['selected']]


def parse_i1_table(text):
    rows = re.findall(r'^\| (xy|xz|yz): [^|]*\| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|$', text, re.M)
    names = {'0': ORIGIN, 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': E_Z}
    out = {}
    for orient, cnt, supp, role in rows:
        key = (orient, tuple(sorted(names[t.strip()] for t in supp.split(','))), role == 'selected')
        out[key] = out.get(key, 0) + int(cnt)
    return out


def class_table():
    out = {}
    for k in CLASSES:
        key = (k['orient'], tuple(sorted(k['rel'])), k['selected'])
        out[key] = out.get(key, 0) + 1
    return out


def cube(n):
    return set(product(range(-n, n + 1), repeat=3))


def cuboid(lo, hi):
    return set(product(*[range(a, b + 1) for a, b in zip(lo, hi)]))


def star_anchors(sites):
    return sorted(b for b in sites if all(add(b, s) in sites for s in S_STAR))


def f1_faces(sites):
    """F1 / whole-star prescription: the 21 omitted faces of every star b+S inside the volume."""
    out = {}
    for b in star_anchors(sites):
        for idx, k in enumerate(OMITTED):
            out[(b, idx)] = frozenset(add(b, d) for d in k['rel'])
    return out


def f2_faces(sites):
    """F2 / all-contained-face prescription (I1 section 6): every omitted face whose actual owner set lies
    inside the volume, charged at its anchor; padding sites carry h_x only."""
    out = {}
    for b in sites:
        for idx, k in enumerate(OMITTED):
            own = frozenset(add(b, d) for d in k['rel'])
            if own <= sites:
                out[(b, idx)] = own
    return out


def adjacency(supports):
    adj = {}
    for sup in supports:
        pts = list(sup)
        for p in pts:
            adj.setdefault(p, set()).update(pts)
    return adj


def bfs(adj, sources):
    dist = {s: 0 for s in sources}
    dq = deque(sorted(sources))
    while dq:
        p = dq.popleft()
        for nb in sorted(adj.get(p, ())):
            if nb not in dist:
                dist[nb] = dist[p] + 1
                dq.append(nb)
    return dist


def chain_dist(adj, u, targets):
    dist = bfs(adj, [u])
    vals = [dist[p] for p in targets if p in dist]
    if not vals:
        raise CheckFailure('target unreachable')
    return min(vals)


# ---------------------------------------------------------------- constants
def j_of(abs_tau):
    return 28 * abs_tau


def t1_of(abs_tau):
    return F(49, 144) * abs_tau


def w_max_of(abs_tau):
    return R / (j_of(abs_tau) * G_R)


def weighted_t(abs_tau, w):
    """Exact first-order tier in the weighted norm: t_w at most w t_1/(1 - J w G'(R))."""
    lip = j_of(abs_tau) * w * GP_R
    if lip >= 1:
        raise CheckFailure('weighted Lipschitz at least one')
    return w * t1_of(abs_tau) / (1 - lip)


def weighted_k(abs_tau, w, e_beta, tier, loss_charged=True):
    """Coefficient-difference constant, weighted_norm route.
    ||delta||_{B,beta} <= [source]/(1 - J e^beta G'(T)), source = e^{beta sigma}(t_1 + J(G(T)-16)) (exact tier)
    or e^{beta sigma} J G(T) (crude tier); sigma = d_X = 1 when the loss is charged (contract lemma form,
    constant multiplying q^(N-1)); the labelled sharp form divides by e^beta."""
    if not (1 <= e_beta <= w <= w_max_of(abs_tau)):
        raise CheckFailure('weights out of the admissible range')
    j = j_of(abs_tau)
    if tier == 'exact_first_order':
        t = weighted_t(abs_tau, w)
        src = t1_of(abs_tau) + j * (g_up(t) - 16)
    elif tier == 'crude_majorant':
        t = j * w * G_R
        src = j * g_up(t)
    else:
        raise CheckFailure('tier')
    if t > R:
        raise CheckFailure('weighted ball exceeds R')
    lip = j * e_beta * gp_up(t)
    if lip >= 1:
        raise CheckFailure('difference Lipschitz at least one')
    x = src / (1 - lip)
    return (e_beta * x if loss_charged else x), t


def analytic_t(rho):
    lip = 28 * rho * GP_R
    if lip >= 1:
        raise CheckFailure('disc Lipschitz at least one')
    return F(49, 144) * rho / (1 - lip)


def analytic_k(abs_tau, rho, tier, sup='two_T', count='contract', cauchy='schwarz'):
    """Coefficient-difference constant, analytic_disc route: sup over |z|<=rho of sum_{I ni u}||delta_I(z)||
    times (|tau|/rho)^{n_0}, with n_0 = N-1 (contract lemma ceil(d/diam)) or N (sharp count 1+d/diam),
    written as the constant multiplying q^(N-1)."""
    tau_star = R / (28 * G_R)
    if not (0 < rho <= tau_star):
        raise CheckFailure('disc radius')
    if 28 * rho * G_R > R:
        raise CheckFailure('disc self-map')
    qq = abs_tau / rho
    if tier == 'exact_first_order':
        t = analytic_t(rho)
        if sup == 'two_T':
            m = 2 * t
        elif sup == 'two_remainder':
            m = 2 * 28 * rho * (g_up(t) - 16)
        else:
            raise CheckFailure('sup rule')
    elif tier == 'crude_majorant':
        if sup == 'two_R':
            m = 2 * R
        elif sup == 'two_selfmap':
            m = 2 * 28 * rho * G_R
        else:
            raise CheckFailure('sup rule')
    else:
        raise CheckFailure('tier')
    k = m
    if cauchy == 'coefficientwise':
        k = k / (1 - qq)
    elif cauchy != 'schwarz':
        raise CheckFailure('cauchy rule')
    if count == 'sharp':
        k = k * qq
    elif count != 'contract':
        raise CheckFailure('count rule')
    return k


# ---------------------------------------------------------------- toy algebra (qubit chain)
def _padd(p, r, nmax):
    n = min(max(len(p), len(r)), nmax + 1)
    return [(p[i] if i < len(p) else 0) + (r[i] if i < len(r) else 0) for i in range(n)]


def _pmul(p, r, nmax):
    out = [F(0)] * min(len(p) + len(r) - 1, nmax + 1)
    for i, a in enumerate(p):
        if a == 0:
            continue
        for j, b in enumerate(r):
            if i + j <= nmax and b != 0:
                out[i + j] += a * b
    return out


def _vadd(u, v, s, nmax):
    out = dict(u)
    for k, p in v.items():
        out[k] = _padd(out.get(k, [F(0)]), [x * s for x in p], nmax)
    return out


def _apply_c(c, vec, nsite, nmax):
    out = {}
    for s, p in vec.items():
        for sup, ci in c.items():
            if all(s[i] == 0 for i in sup):
                t = tuple(1 if (i in sup or s[i]) else 0 for i in range(nsite))
                out[t] = _padd(out.get(t, [F(0)]), _pmul(p, ci, nmax), nmax)
    return out


def _apply_v(bonds, vec, nsite, nmax):
    out = {}
    for s, p in vec.items():
        for (i, j) in bonds:
            t = list(s)
            t[i] ^= 1
            t[j] ^= 1
            t = tuple(t)
            out[t] = _padd(out.get(t, [F(0)]), _pmul(p, [F(0), F(1)], nmax), nmax)
    return out


def toy_fixed_point(bonds, nsite, nmax):
    """Creation fixed point c = sum_k L_k(c,...,c)/k! for H = N_op + z sum_bonds X_i X_j on qubits
    (h_x = n_x, so H_M = |M|), as exact Taylor polynomials in z to order nmax. Finite fixture only."""
    c = {}
    vac = {tuple([0] * nsite): [F(1)]}
    for _ in range(nmax + 1):
        neg = [vac]
        for _m in range(1, 5):
            neg.append({k: [-x for x in p] for k, p in _apply_c(c, neg[-1], nsite, nmax).items()})
        total = {}
        for k in range(5):
            acc = {}
            for j in range(k + 1):
                v = _apply_v(bonds, neg[k - j], nsite, nmax)
                for _i in range(j):
                    v = _apply_c(c, v, nsite, nmax)
                acc = _vadd(acc, v, comb(k, j), nmax)
            total = _vadd(total, acc, F(1, fact(k)), nmax)
        newc = {}
        for s, p in total.items():
            sup = tuple(i for i in range(nsite) if s[i])
            if sup and any(x != 0 for x in p):
                newc[sup] = [x / len(sup) for x in p]
        c = newc
    return c


def toy_residual(c, bonds, nsite, nmax):
    vac = {tuple([0] * nsite): [F(1)]}
    psi, term = dict(vac), vac
    for m in range(1, nsite + 1):
        term = {k: [-x for x in p] for k, p in _apply_c(c, term, nsite, nmax).items()}
        psi = _vadd(psi, term, F(1, fact(m)), nmax)
    hv = {s: [x * sum(s) for x in p] for s, p in psi.items()}
    hv = _vadd(hv, _apply_v(bonds, psi, nsite, nmax), 1, nmax)
    energy = hv.get(tuple([0] * nsite), [F(0)])
    bad = 0
    for s in set(psi) | set(hv):
        r = _padd(hv.get(s, [F(0)]), [-x for x in _pmul(energy, psi.get(s, [F(0)]), nmax)], nmax)
        if any(x != 0 for x in r):
            bad += 1
    return energy, bad


def first_order(p):
    for i, x in enumerate(p):
        if x != 0:
            return i
    return None


# ---------------------------------------------------------------- other fixtures
def solve_tridiagonal(n, diag, off, rhs):
    cp, dp = [F(0)] * n, [F(0)] * n
    cp[0], dp[0] = off / diag, rhs[0] / diag
    for i in range(1, n):
        m = diag - off * cp[i - 1]
        cp[i] = off / m if i < n - 1 else F(0)
        dp[i] = (rhs[i] - off * dp[i - 1]) / m
    x = [F(0)] * n
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    for i in range(n):
        lhs = diag * x[i] + (off * x[i - 1] if i > 0 else 0) + (off * x[i + 1] if i < n - 1 else 0)
        if lhs != rhs[i]:
            raise CheckFailure('tridiagonal solve')
    return x


def creation_state(nsite, creations):
    """psi = prod_I (1 - c_I^) Omega on qubits: sum over pairwise-disjoint families."""
    psi = {}
    for k in range(len(creations) + 1):
        for fam in combinations(range(len(creations)), k):
            union, ok = set(), True
            for i in fam:
                if union & set(creations[i][0]):
                    ok = False
                    break
                union |= set(creations[i][0])
            if not ok:
                continue
            coef = F((-1) ** k)
            for i in fam:
                coef *= creations[i][1]
            key = tuple(1 if x in union else 0 for x in range(nsite))
            psi[key] = psi.get(key, F(0)) + coef
    return psi


def reduced_site0(psi):
    norm = sum(v * v for v in psi.values())
    rho = [[F(0), F(0)], [F(0), F(0)]]
    for rest in sorted({k[1:] for k in psi}):
        for a in (0, 1):
            for b in (0, 1):
                rho[a][b] += psi.get((a,) + rest, F(0)) * psi.get((b,) + rest, F(0))
    return [[x / norm for x in row] for row in rho]


def phrase_hits(text, forbidden, template=None):
    body = re.sub(r'\s+', ' ', str(text)).strip()
    if template:
        body = body.replace(re.sub(r'\s+', ' ', template).strip(), ' ')
    hits = []
    for clause in [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', body) if c.strip()]:
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                hits.append({'phrase': phrase, 'negated': bool(NEGATION.search(clause))})
    return [h for h in hits if not h['negated']]


def placeholder_spans(text):
    out = []
    for m in PLACEHOLDER.finditer(text):
        inner = m.group(1)
        if re.search(r'\s', inner) or '|' in inner or 'e.g.' in inner:
            out.append(m.group(0))
    return out


def strings_of(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings_of(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings_of(v)


# ---------------------------------------------------------------- validator
def recompute_constant(rec, abs_tau):
    inp = rec['inputs']
    if rec['route'] == 'weighted_norm':
        val, _ = weighted_k(abs_tau, inp['w'], inp['e_beta'], rec['tier'], loss_charged=inp['loss_charged'])
        return val
    return analytic_k(abs_tau, inp['rho'], rec['tier'], sup=inp['sup'], count=inp['count'], cauchy=inp['cauchy'])


def validate(pk, c):
    if pk['contract_sha256'] != CONTRACT_SHA256:
        raise Rejected('contract hash')
    if sorted(pk['controls_executed']) != sorted(c['controls']) or not all(
            v is True for v in pk['controls_executed'].values()):
        raise Rejected('control boolean')
    if sorted(pk['snapshots']) != sorted(c['inventory']):
        raise Rejected('snapshot missing')
    if any(isinstance(x, float) for x in [pk['tau_abs']] + [r['value'] for r in pk['constants']]
           + [r['q'] for r in pk['constants']] + list(pk['scaling'].values())):
        raise Rejected('exact arithmetic')
    for key in ('continuum_claim', 'scientific_priority_verified', 'weak_coupling_claim'):
        if pk['claims'].get(key) is not False:
            raise Rejected('forbidden claim ' + key)
    if pk['model_id'] != MODEL_ID or pk['triple'] != ['0', '0', '0'] or pk['tau_abs'] != c['tau_abs'] \
            or pk['signs'] != ['+', '-']:
        raise Rejected('changed model relabelled')
    if pk['families'] != ['F1', 'F2'] or pk['family_defs'] != c['family_defs']:
        raise Rejected('two families not named')
    if pk['N_min'] != 2:
        raise Rejected('changed model relabelled: N_min')
    missing = [k for k in c['parameter_keys_required'] if k not in pk['parameters_declared']]
    if missing:
        raise Rejected('parameters field missing: ' + ','.join(missing))
    if pk['clock'] != CLOCK or pk['window'] != WINDOW:
        raise Rejected('clock')
    if pk['metric'] != 'coarse_linf' or pk['d_X'] != 1 or pk['distance_metric'] != pk['metric'] \
            or pk['lemma']['convention'] != pk['metric'] or pk['l1_alternative'] != {'d_X': 2, 'labelled': True,
                                                                                         'mixed': False}:
        raise Rejected('metric')
    wt = pk['weights']
    if wt['kind'] == 'cardinality':
        raise Rejected('cardinality weight rate relabelled as the diameter rate')
    if wt['kind'] != 'diameter' or wt['star_count_mixed'] is not False:
        raise Rejected('metric: weight kind')
    if wt['direction'] != 'grows_from_source_toward_R' or wt['difference_weight'] != 'rho_B(I)=max_p d_inf(p,B)':
        raise Rejected('weight direction')
    if wt['other_creations_diameter_weighted'] is not True:
        raise Rejected('weight direction: non-submultiplicative pure distance weight')
    if wt['loss'] != 'per_interaction':
        raise Rejected('loss per interaction')
    con = pk['contraction']
    if con['cited_unweighted'] is not False or con['rechecked_in_weighted_norm'] is not True:
        raise Rejected('weighted contraction')
    if not (1 <= wt['w'] <= c['w_max']) or wt['w_max'] != c['w_max'] or wt['e_beta'] > wt['w']:
        raise Rejected('weighted contraction: weight above the admissible maximum')
    if con['selfmap'] != j_of(pk['tau_abs']) * wt['w'] * G_R or con['selfmap'] > R \
            or con['lipschitz'] != j_of(pk['tau_abs']) * wt['w'] * GP_R:
        raise Rejected('weighted contraction: inequality not re-evaluated')
    if pk['lemma']['subadditivity'] != 'd_X+sum':
        raise Rejected('diameter subadditivity')
    if pk['J_over_tau'] != 28 or pk['incoming_stars'] != 4:
        raise Rejected('incoming stars')
    fc = pk['face_counts']
    if fc != {'per_factor': 49, 'owner_sets': 15, 'meeting_R': 82, 'inside_R': 10, 'source': 'derived_I1_table'}:
        raise Rejected('face count')
    cv = pk['cover']
    if cv != {'sites': [[0, 0, 0], [0, 0, 1]], 'links': 48, 'endpoints': 36, 'anchors': 7}:
        raise Rejected('cover')
    if pk['decay_factor_source'] != 'weight_or_disc' or pk['lipschitz_decay_factor'] is not None:
        raise Rejected('global Lipschitz as decay')
    if pk['R_as_tree_ratio'] is not False or pk['headline_q_basis'] != c['headline_q_basis']:
        raise Rejected('ball radius used as tree ratio')
    an = pk['analytic']
    if an['extended_to_reduced_density'] is not False or an['zero_free_region'] is not None:
        raise Rejected('disc radius: extension to rho_R without a zero-free region')
    if an['rho_headline'] != 64 * pk['tau_abs'] or an['rho_floor'] != c['tau_star'] or an['rho_max'] != c['tau_star']:
        raise Rejected('disc radius')
    cut = pk['cutoff']
    if cut != {'statement': 'each Q_L, uniform in L', 'untruncated_claimed': False,
               'cutoff_removed_for_coefficients': False}:
        raise Rejected('untruncated coefficients')
    if pk['rate_units'] != RATE_UNITS or pk['rate_in_a'] is not False or pk['physical_length'] is not None:
        raise Rejected('rate in a')
    if pk['uniform_in'] != UNIFORM_IN:
        raise Rejected('uniform in a')
    if pk['marginal'] != {'state_decay_inferred': False, 'fixture_exhibited': True}:
        raise Rejected('marginal: coefficient decay is not marginal decay')
    if pk['combine'] != 'linear':
        raise Rejected('root-N or non-linear combination')
    # comparisons
    comps = pk['comparisons']
    if sorted(comps) != sorted(c['comparisons']):
        raise Rejected('boundary source: comparison set')
    for name, ref in c['comparisons'].items():
        got = comps[name]
        if got['new_terms_only'] is not True or got['source_count_N2'] != ref['source_count_N2'] \
                or got['source_set'] != ref['source_set']:
            if name == 'F2_nested' and got['source_count_N2'] == ref['double_charged_N2']:
                raise Rejected('F2 regrouping charged twice')
            raise Rejected('boundary source')
        if got['charged_once'] is not True or got['charging'] != ref['charging']:
            raise Rejected('F2 regrouping' if name == 'F2_nested' else 'boundary source: charging')
        if got['dist_e_z_to_B'] != ref['dist_e_z_to_B'] or got['dist_0_to_B'] != ref['dist_0_to_B'] \
                or got['exponent'] != 'N-1':
            raise Rejected('boundary distance')
    gv = pk['general_volume']
    if gv['route'] not in ('union', 'direct') or gv['factor'] != (2 if gv['route'] == 'union' else 1):
        raise Rejected('root-N or non-linear combination: general volume')
    # constants
    ids = set()
    for rec in pk['constants']:
        if rec['tier'] not in TIERS or rec['route'] not in ROUTES:
            raise Rejected('tier mixing: vocabulary')
        if rec['tier'] == 'exact_first_order' and (rec['first_order'] != 'exact_AV1'
                                                   or rec['t_rule'] != 'self_consistent'):
            raise Rejected('tier mixing')
        if rec['t_rule'] == 'crude' and rec['tier'] != 'crude_majorant':
            raise Rejected('tier mixing')
        if rec['q'] < c['q_min']:
            raise Rejected('q_min crossed')
        pair = c['pairs'].get(rec['pair'])
        if pair is None or rec['q'] != pair['q'] or rec['target'] != pair['K']:
            raise Rejected('rate constant pair not the frozen pair')
        inp = rec['inputs']
        if rec['route'] == 'weighted_norm':
            if inp['w'] > c['w_max_at'][rec['pair']]:
                raise Rejected('weighted contraction: weight above the admissible maximum')
            if F(1) / inp['e_beta'] != rec['q']:
                raise Rejected('rate constant pair: q not realized by the weight')
            if rec['form'] == 'contract_lemma' and inp['loss_charged'] is not True:
                raise Rejected('loss per interaction: source loss omitted in the contract-lemma form')
        else:
            if inp['rho'] > c['tau_star']:
                raise Rejected('disc radius')
            if pk['tau_abs'] / inp['rho'] != rec['q']:
                raise Rejected('disc radius: q is not |tau|/rho')
            if rec['form'] == 'contract_lemma' and inp['count'] != 'contract':
                raise Rejected('boundary distance: exponent form')
        if rec['form'] == 'sharp' and rec['labelled'] is not True:
            raise Rejected('insufficient verdict: sharp refinement not labelled')
        if rec['exponent'] != 'N-1':
            raise Rejected('boundary distance: exponent')
        if rec['value'] < recompute_constant(rec, pk['tau_abs']):
            raise Rejected('constant not reproduced from its declared inputs')
        if rec['meets_target'] != (rec['value'] <= rec['target']):
            raise Rejected('insufficient verdict: target flag')
        if rec['signs'] != ['+', '-']:
            raise Rejected('changed model relabelled: one sign')
        ids.add(rec['id'])
    if not {'K_headline_forward', 'K_headline_reverse', 'K_floor_forward', 'K_floor_reverse'} <= ids:
        raise Rejected('rate constant pair: headline or floor constant missing')
    if pk['q_optimized_per_N'] is not False:
        raise Rejected('rate constant pair: q optimized after the constants were seen')
    missed = [r['id'] for r in pk['constants'] if not r['meets_target']]
    if sorted(m['id'] for m in pk['missed']) != sorted(missed) or any(m['retuned'] is not False
                                                                       or not m['dominating_term']
                                                                       for m in pk['missed']):
        raise Rejected('insufficient verdict retained')
    for rec in pk['constants']:
        if rec['pair'] == 'headline' and rec['tier'] == 'exact_first_order' and rec['form'] == 'contract_lemma' \
                and not rec['meets_target'] and pk['verdict'] == 'accepted_within_scope':
            raise Rejected('insufficient verdict retained')
    # scaling
    for cid, ratio in pk['scaling'].items():
        lo, hi = c['brackets'][pk['scaling_bracket_of'][cid]]
        if pk['scaling_bracket_of'][cid] not in c['brackets'] or not (lo <= ratio <= hi):
            raise Rejected('tau scaling exponent: ' + cid)
    if pk['brackets_declared'] != c['brackets_text']:
        raise Rejected('tau scaling exponent: bracket chosen after evaluation')
    # words
    if pk['sub_labels'] != ['boundary_decay_rate_only', 'static_not_dynamic']:
        raise Rejected('gate field: sub-label')
    for text in pk['limit_statements']:
        low = text.lower()
        if 'whole sequence' not in low and 'subsequence' not in low:
            raise Rejected('subsequence versus whole sequence')
    if pk['gate_fields'].get('whole_sequence_claimed') is not False:
        raise Rejected('subsequence versus whole sequence: whole_sequence_claimed')
    if pk['gate_fields'] != c['gate_fields']:
        raise Rejected('gate field')
    if pk['sentence'] != c['sentence']:
        raise Rejected('mandatory sentence')
    for text in pk['statements']:
        if phrase_hits(text, c['forbidden'], c['sentence']):
            raise Rejected('forbidden phrasing')
        if re.search(r'\buniform in a\b', text, re.I) and not NEGATION.search(text):
            raise Rejected('uniform in a')
    for text in pk['contract_strings']:
        if placeholder_spans(text):
            raise Rejected('placeholder span')
    inv = pk['reverse_inputs']
    if sorted(inv) != sorted(c['inventory']):
        extra = sorted(set(inv) - set(c['inventory']))
        if any(('round33/skeptic/' in p or 'deliberation' in p or 'round33/experts/' in p or '/forward/ba1/' in p)
               for p in extra):
            raise Rejected('reverse premise isolation')
        raise Rejected('reverse premise inventory')
    return True


# ---------------------------------------------------------------- execute
def execute():
    contract_bytes = CONTRACT.read_bytes()
    c_sha = hashlib.sha256(contract_bytes).hexdigest()
    need(c_sha == CONTRACT_SHA256, 'contract_sha256_pinned', sha256=c_sha)
    con = json.loads(contract_bytes)
    par, pre = con['parameters'], con['preregistration']
    for rel, sha in sorted(PINNED.items()):
        got = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()
        if got != sha:
            raise CheckFailure('pinned premise changed: ' + rel)
    need(True, 'premise_sha256_pinned', files=sorted(PINNED))
    tau = F(pre['tau']['value'])
    need(con['status'] == 'frozen_before_production' and con['id'] == 'BA1' and tau == F(1, 10 ** 8)
         and pre['tau']['signs_evaluated'] == ['+', '-'] and pre['model_id'] == MODEL_ID
         and pre['selected_triple_alpha_units'] == ['0', '0', '0'] and con['direction'] == 'paired'
         and con['producers'] == ['forward', 'reverse'] and con['reverse_premise_isolation'] is True,
         'contract_model_tau_signs_read', tau=q(tau))
    head, floor = par['rate_constant_pair']['headline'], par['rate_constant_pair']['rate_floor']
    k_head, k_floor = F(head['K_target']), F(floor['K_target'])
    q_head, q_floor = F(head['q']), F(floor['q'])
    need(q_head == F(1, 64) and k_head == F(1, 2000000) and q_floor == F(148, 390625) and k_floor == F(1, 12)
         and head['tier'] == 'exact_first_order' and pre['target']['value'] == '1/2000000 and 1/12'
         and pre['target']['comparator'] == '<=', 'contract_frozen_pairs_read',
         headline=[q(q_head), q(k_head)], floor=[q(q_floor), q(k_floor)])
    controls = list(con['controls'])
    need(controls == pre['controls_required']['ids'] and len(controls) == 37 and len(set(controls)) == 37,
         'contract_control_mirror', controls=37, mirror=37)
    ncs = con['new_control_semantics']
    no_sem = sorted(set(controls) - set(ncs))
    need(no_sem == ['full_original_wilson_cover', 'gate_fields_topic_specific'] and not (set(ncs) - set(controls)),
         'contract_control_semantics_coverage', with_semantics=len(ncs), without=no_sem,
         note='full_original_wilson_cover is a Round32 universal id; gate_fields_topic_specific has no frozen '
              'semantics (reading: export exactly preregistration.gate_fields_required)')
    gate_fields = dict(pre['gate_fields_required'])
    need(len(gate_fields) == 12 and gate_fields['rate_in_N_claimed'] is True
         and gate_fields['coefficient_cauchy_claimed'] is True and gate_fields['whole_sequence_claimed'] is False
         and gate_fields['state_decay_claimed'] is False, 'contract_gate_fields_read', fields=sorted(gate_fields))
    sentence = pre['mandatory_sentence_template']
    need('K q^(N-1)' in sentence and 'uniformly in the cutoff' in sentence and 'not decay of the reduced density'
         in sentence, 'contract_sentence_template_read')
    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings'])
    tmpl_hits = phrase_hits(sentence, forbidden)
    need(tmpl_hits == [], 'template_phrase_scan_clean_without_removal', scanned_phrases=len(forbidden))
    spans = [s for text in strings_of(con) for s in placeholder_spans(text)]
    need(spans == [] and placeholder_spans('J<=28|tau| and N>=2') == []
         and placeholder_spans('<to be filled>') == ['<to be filled>'], 'contract_R1_placeholder_mirror_clean')
    inventory = sorted(['AGENTS.md', CONTRACT_REL] + list(con['shared_premises']))
    need(len(inventory) == 27 and con['forward_additional_premises'] == []
         and not any(('round33/skeptic/' in p or 'deliberation' in p or 'round33/experts/' in p) for p in inventory)
         and all((ROOT / p).is_file() for p in inventory), 'contract_reverse_inventory_derivable',
         files=len(inventory))
    brackets_text = dict(pre['scaling_brackets_per_constant'])
    need(brackets_text['K_exact_first_order_at_q_1_64'].startswith('[95,105]')
         and brackets_text['K_floor_pair'].startswith('[99/100, 101/100]')
         and brackets_text['q_min'].startswith('exactly 100'), 'contract_scaling_brackets_read')
    brackets = {'K_exact_first_order_at_q_1_64': (F(95), F(105)), 'K_floor_pair': (F(99, 100), F(101, 100)),
                'q_min': (F(100), F(100))}
    need(par['window'] == WINDOW and par['N_min'].startswith('2 ') and 'l-infinity' in par['metric']
         and 'd_X=1' in par['metric'] and 'w = e^mu = 64' in par['weights'] and '390625/148' in par['weights']
         and 'tau_star = 1/37888' in par['weights'] and 'rho = 64|tau|' in par['weights'],
         'contract_parameters_metric_weights_window_read', keys=sorted(par))
    am2 = (ROOT / 'research/round29/forward/am2/report.md').read_text()
    am2g = json.loads((ROOT / 'research/round29/advisor/am2-gate.json').read_text())
    av1g = json.loads((ROOT / 'research/round32/advisor/av1-gate.json').read_text())
    aw1g = json.loads((ROOT / 'research/round32/advisor/aw1-gate.json').read_text())
    ay1g = json.loads((ROOT / 'research/round32/advisor/ay1-gate.json').read_text())
    need('L_k^{\\rm num}=16\\,8^k(1+5k/4)' in am2 and "G(R)<148/7,\\quad G'(R)<352" in am2
         and 'G(t)=16 exp(8t)(1+10t)' in am2g['accepted'] and 't<=t_1/(1-352J)' in av1g['accepted']
         and 'first-order face coefficient |tau|/144' in av1g['accepted']
         and 'c^(1)=L_0=-(tau/72) sum W_f Omega_0' in aw1g['accepted'] and '28N(5N+1)' in ay1g['accepted']
         and 'J<=28|tau|=J_0=7/25000000' in ay1g['accepted'], 'admitted_constants_bound_to_pinned_premises')

    # 1. geometry: classes, diameters, counts, incidence
    i1 = parse_i1_table((ROOT / 'research/round21/forward/i1/report.md').read_text())
    need(class_table() == i1 and len(CLASSES) == 24 and len(OMITTED) == 21, 'face_classes_match_I1_table',
         classes=len(i1))
    star_diam = (diam(S_STAR, dinf), diam(S_STAR, d1))
    rel_diams = sorted({(diam(k['rel'], dinf), diam(k['rel'], d1)) for k in OMITTED})
    need(star_diam == (1, 2) and rel_diams == [(1, 1), (1, 2)] and all(ORIGIN in k['rel'] and len(k['rel']) >= 2
                                                                        for k in OMITTED),
         'star_and_owner_set_diameters', star_linf=1, star_l1=2, owner_set_linf=1, owner_set_l1=[1, 2])
    offs = {s: sum(1 for k in OMITTED if s in k['rel']) for s in S_STAR}
    per_factor = sum(offs.values())
    osets = {}
    for s in S_STAR:
        for k in OMITTED:
            if s in k['rel']:
                key = frozenset(sub(p, s) for p in k['rel'])
                osets[key] = osets.get(key, 0) + 1
    mults = sorted(osets.values())
    meet_r = 2 * per_factor - offs[E_Z]
    inside_r = sum(1 for k in OMITTED if k['rel'] == frozenset(R_COVER))
    need(offs == {ORIGIN: 21, (1, 0, 0): 4, (0, 1, 0): 8, E_Z: 16} and per_factor == 49 and len(osets) == 15
         and mults == [1] * 5 + [2] * 3 + [3] * 2 + [4] * 3 + [10] * 2 and meet_r == 82 and inside_r == 10,
         'counts_49_15_82_10_by_translation', per_factor=49, owner_sets=15, multiplicities=mults, meeting_R=82,
         inside_R=10)
    sqrt_sum_lo = F(11) + 2 * sqrt_bracket(3)[0] + 3 * sqrt_bracket(2)[0] + 2 * sqrt_bracket(10)[0]
    sqrt_sum_terms = sorted(osets.values())
    need(sqrt_sum_terms.count(1) == 5 and sqrt_sum_terms.count(2) == 3 and sqrt_sum_terms.count(3) == 2
         and sqrt_sum_terms.count(4) == 3 and sqrt_sum_terms.count(10) == 2 and F(25) < sqrt_sum_lo < 49,
         'grouped_first_order_norm_bracket', sum_sqrt_nM_lower=q(sqrt_sum_lo), crude=49)
    geo_rows = {}
    for n in (2, 3):
        sites = cube(n)
        anchors = star_anchors(sites)
        per_site = {u: sum(1 for b in anchors if u in {add(b, s) for s in S_STAR}) for u in sites}
        faces = f1_faces(sites)
        face_site = {}
        for own in faces.values():
            for p in own:
                face_site[p] = face_site.get(p, 0) + 1
        stars_r = [b for b in anchors if any(add(b, s) in R_COVER for s in S_STAR)]
        faces_r = [k for k, own in faces.items() if own & set(R_COVER)]
        if not all(diam([add(b, s) for s in S_STAR], dinf) == 1 and diam([add(b, s) for s in S_STAR], d1) == 2
                   for b in anchors):
            raise CheckFailure('star diameter on Lambda_%d' % n)
        if not all(diam(own, dinf) == 1 and diam(own, d1) <= 2 for own in faces.values()):
            raise CheckFailure('face owner-set diameter on Lambda_%d' % n)
        f2 = f2_faces(sites)
        if not all(diam(own, dinf) == 1 for own in f2.values()):
            raise CheckFailure('F2 owner-set diameter')
        geo_rows['Lambda_%d' % n] = {'stars': len(anchors), 'max_stars_per_site': max(per_site.values()),
                                     'interior_sites_with_4_stars': sum(1 for v in per_site.values() if v == 4),
                                     'max_faces_per_site': max(face_site.values()), 'stars_meeting_R': len(stars_r),
                                     'faces_meeting_R': len(faces_r), 'F1_faces': len(faces), 'F2_faces': len(f2)}
        need(max(per_site.values()) == 4 and max(face_site.values()) == 49 and len(stars_r) == 7
             and len(faces_r) == 82 and len(faces) == 168 * n ** 3, 'enumeration_Lambda_%d_diameter_incidence' % n,
             **geo_rows['Lambda_%d' % n])
    links, ends = set(), set()
    for b in R_COVER:
        for r_, s_ in product(range(4), range(2)):
            p = (4 * b[0] + r_, 2 * b[1] + s_, b[2])
            for dname in 'xyz':
                links.add((p, dname))
                ends.update({p, add(p, DIRS[dname])})
    anchors_r = sorted({sub(r_, s) for r_ in R_COVER for s in S_STAR})
    need(len(links) == 48 and len(ends) == 36 and len(anchors_r) == 7, 'wilson_cover_48_links_36_endpoints_7_anchors')

    # 2. weighted contraction
    e8 = exp_up(F(1, 8))
    need(e8 < F(8, 7) and g_up(R) < G_R and gp_up(R) < GP_R and exp_lo(F(1, 8)) < e8, 'am2_majorant_enclosures',
         exp_one_eighth_upper=q(e8), G_R_upper=q(g_up(R)), Gp_R_upper=q(gp_up(R)))
    j0 = j_of(tau)
    w_max = w_max_of(tau)
    tau_star = R / (28 * G_R)
    need(j0 == F(7, 25000000) and w_max == F(390625, 148) and j0 * w_max * G_R == R
         and j0 * w_max * GP_R == F(77, 296) and j0 * (w_max + F(1, 148)) * G_R > R and tau_star == F(1, 37888)
         and F(1) / w_max == q_floor and 37888 * tau == q_floor, 'weighted_selfmap_range_and_q_min',
         w_max=q(w_max), lipschitz_at_w_max=q(F(77, 296)), tau_star=q(tau_star), q_min=q(q_floor))
    w64 = F(64)
    need(j0 * w64 * G_R == F(148, 390625) and j0 * w64 * GP_R == F(2464, 390625) and j0 * w64 * G_R <= R
         and 28 * F(1, 2424832) * w64 * G_R == R, 'weighted_contraction_at_w64',
         selfmap=q(j0 * w64 * G_R), lipschitz=q(j0 * w64 * GP_R), coupling_threshold_for_w64='1/2424832')
    need(F(781250, 77) * j0 * GP_R == 1 and w_max < F(781250, 77), 'weighted_lipschitz_not_binding',
         lipschitz_limit=q(F(781250, 77)))
    # diameter subadditivity on every admissible word of order at most two with actual owner sets
    x_star = frozenset(S_STAR)
    cands = sorted({frozenset(add(b, d) for d in k['rel']) for k in OMITTED
                    for b in {sub(p, d) for p in S_STAR for d in k['rel']}
                    if frozenset(add(b, d) for d in k['rel']) & x_star}, key=lambda s: sorted(s))
    words = 0
    excess_inf, excess_1, max_shortcut_fail = set(), set(), 0
    witness = None
    for k in (0, 1, 2):
        for combo in combinations(cands, k):
            if any(a & b for a, b in combinations(combo, 2)):
                continue
            nset = frozenset().union(*combo) if combo else frozenset()
            base = nset - x_star
            for mask in range(16):
                ys = frozenset(S_STAR[i] for i in range(4) if mask >> i & 1)
                m = base | ys
                if not m or not (m <= nset | x_star):
                    continue
                words += 1
                sd_inf = sum(diam(i_, dinf) for i_ in combo)
                sd_1 = sum(diam(i_, d1) for i_ in combo)
                dm_inf, dm_1 = diam(m, dinf), diam(m, d1)
                if dm_inf > 1 + sd_inf or dm_1 > 2 + sd_1:
                    raise CheckFailure('diameter subadditivity violated')
                excess_inf.add(dm_inf - sd_inf)
                excess_1.add(dm_1 - sd_1)
                mx = max((diam(i_, dinf) for i_ in combo), default=0)
                if dm_inf > 1 + mx:
                    max_shortcut_fail += 1
                    if witness is None and m == base and k == 2:
                        witness = {'I': [sorted(list(i_)) for i_ in combo], 'M': sorted(m), 'diam_M': dm_inf}
    need(max(excess_inf) == 1 and max(excess_1) == 2 and max_shortcut_fail > 0 and witness is not None,
         'diameter_subadditivity_on_all_words_k_le_2', words=words, candidate_supports=len(cands),
         max_excess_linf=1, max_excess_l1=2, max_shortcut_failures=max_shortcut_fail,
         disconnected_witness=witness, note='the loss d_X is attained (k=0 gives diam M=1 with no creation)')

    # 3. order-versus-distance tables on Lambda_2..Lambda_4 (both conventions)
    tables = {}
    for n in (2, 3, 4):
        sites = cube(n)
        fam_terms = {'F1': list(f1_faces(sites).values()), 'F2': list(f2_faces(sites).values())}
        star_terms = [frozenset(add(b, s) for s in S_STAR) for b in star_anchors(sites)]
        adj_f1 = adjacency(fam_terms['F1'])
        adj_st = adjacency(star_terms)
        if adj_f1 != adj_st:
            raise CheckFailure('F1 face and star site graphs differ')
        tables['Lambda_%d' % n] = {}
        for fam, terms in fam_terms.items():
            dist = bfs(adjacency(terms), list(R_COVER))
            by_inf, by_1 = {}, {}
            for x in terms:
                di = min(dinf(r_, p) for r_ in R_COVER for p in x)
                dl = min(d1(r_, p) for r_ in R_COVER for p in x)
                ch = 1 + min(dist[p] for p in x)
                if ch < 1 + di or ch < 1 + ceil_div(dl, 2):
                    raise CheckFailure('order-versus-distance lemma violated')
                for tab, dd in ((by_inf, di), (by_1, dl)):
                    row = tab.setdefault(dd, [0, ch, ch])
                    row[0] += 1
                    row[1] = min(row[1], ch)
                    row[2] = max(row[2], ch)
            t_inf = {str(dd): {'terms': v[0], 'min_chain_order': v[1], 'max_chain_order': v[2],
                               'sharp_bound_1_plus_d': 1 + dd, 'contract_bound_ceil_d': dd}
                     for dd, v in sorted(by_inf.items())}
            t_1 = {str(dd): {'terms': v[0], 'min_chain_order': v[1], 'max_chain_order': v[2],
                             'sharp_bound_1_plus_ceil_d_over_2': 1 + ceil_div(dd, 2),
                             'contract_bound_ceil_d_over_2': ceil_div(dd, 2)} for dd, v in sorted(by_1.items())}
            if any(v[1] != 1 + dd for dd, v in by_inf.items()):
                raise CheckFailure('l_inf bound not attained')
            tables['Lambda_%d' % n][fam] = {'linf_d_X_1': t_inf, 'l1_d_X_2': t_1}
    l1_slack = sum(1 for n in tables for fam in tables[n] for dd, v in tables[n][fam]['l1_d_X_2'].items()
                   if v['min_chain_order'] > v['sharp_bound_1_plus_ceil_d_over_2'])
    need(True, 'order_versus_distance_tables_Lambda_2_to_4', boxes=sorted(tables),
         lemma='[z^n] delta_I = 0 unless n >= 1 + max_{u in I} ceil(d(u,S)/d_X); contract form ceil(d/diam) is '
               'valid but one order weaker; l_inf bound attained at every distance, l1 bound slack in %d rows'
               % l1_slack, proof_uses='coarse_linf, d_X=1')
    # algebraic qubit-chain fixture of the count
    toy = {}
    for nsite in (4, 5):
        old = [(i, i + 1) for i in range(nsite - 2)]
        new = old + [(nsite - 2, nsite - 1)]
        nmax = nsite
        ca, cb = toy_fixed_point(old, nsite, nmax), toy_fixed_point(new, nsite, nmax)
        for bonds, cc in ((old, ca), (new, cb)):
            _, bad = toy_residual(cc, bonds, nsite, nmax)
            if bad:
                raise CheckFailure('toy eigen-equation residual')
        orders = []
        for sup in sorted(set(ca) | set(cb)):
            if 0 in sup:
                dlt = _padd(cb.get(sup, [F(0)]), [-x for x in ca.get(sup, [F(0)])], nmax)
                o = first_order(dlt)
                if o is not None:
                    orders.append((sup, o, dlt[o]))
        dist_new = nsite - 2
        first = min(o for _, o, _ in orders)
        toy['chain_%d' % nsite] = {'distance_site0_to_new_bond': dist_new, 'first_nonzero_order': first,
                                   'contract_form_ceil_d': dist_new, 'sharp_1_plus_d': 1 + dist_new,
                                   'witness': [{'support': list(s_), 'order': o, 'coefficient': q(v)}
                                               for s_, o, v in orders if o == first]}
        if first != 1 + dist_new:
            raise CheckFailure('toy first order')
    need(True, 'order_versus_distance_algebraic_fixture', fixture=toy, model='FG(qubit_chain, H=sum n_x + z sum '
                                                                               'X_iX_{i+1})', transfers_to_aq=False,
         note='eigen-equation residual vanishes to the truncation order; first nonzero order is 1+d, one above the '
              'contract form ceil(d/diam)')

    # 4. boundary sources and exact distances
    src_rows = {}
    for n in (2, 3, 4):
        lam, lam1 = cube(n), cube(n + 1)
        f1n, f1m, f2n, f2m = f1_faces(lam), f1_faces(lam1), f2_faces(lam), f2_faces(lam1)
        shell = lam1 - lam
        layer = {p for p in lam if max(abs(x) for x in p) == n}
        if not (set(f1n) <= set(f2n) <= set(f1m) <= set(f2m)):
            raise CheckFailure('chain inclusion F1_N, F2_N, F1_N+1, F2_N+1')
        old_anchors = set(star_anchors(lam))
        new_st = [frozenset(add(b, s) for s in S_STAR) for b in star_anchors(lam1) if b not in old_anchors]
        comps = {'F1_nested': (f1n, f1m, new_st, shell, lam1), 'F2_nested': (f2n, f2m, None, shell, lam1),
                 'F1_vs_F2': (f1n, f2n, None, layer, lam)}
        src_rows['N=%d' % n] = {}
        for name, (small, big, terms, bset, bigsites) in comps.items():
            new = {k: v for k, v in big.items() if k not in small}
            supports = terms if terms is not None else list(new.values())
            svec = set().union(*supports)
            if not all(sp & bset for sp in supports):
                raise CheckFailure('a new term misses the source set')
            if terms is not None:
                star_site = {}
                for sp in terms:
                    for p in sp:
                        star_site[p] = star_site.get(p, 0) + 1
                j_new = 7 * max(star_site.values())
            else:
                j_new = None
            face_site = {}
            for own in new.values():
                for p in own:
                    face_site[p] = face_site.get(p, 0) + 1
            adj = adjacency(list(big.values()))
            row = {'new_faces': len(new), 'new_stars': len(terms) if terms is not None else None,
                   'max_new_faces_per_site': max(face_site.values()),
                   'J_new_over_tau': q(j_new) if j_new is not None else q(F(max(face_site.values()), 3)),
                   'supports_inside_source_set': all(sp <= bset for sp in supports)}
            for label, u in (('0', ORIGIN), ('e_z', E_Z)):
                row['dinf_%s_to_S' % label] = set_dist(u, svec, dinf)
                row['d1_%s_to_S' % label] = set_dist(u, svec, d1)
                row['chain_%s_to_S' % label] = chain_dist(adj, u, svec)
                row['dinf_%s_to_B' % label] = set_dist(u, bset, dinf)
                row['sharp_order_%s' % label] = 1 + row['dinf_%s_to_S' % label]
                row['contract_order_%s' % label] = row['dinf_%s_to_S' % label]
            src_rows['N=%d' % n][name] = row
            if not (row['dinf_e_z_to_S'] == n - 1 and row['dinf_0_to_S'] == n and row['chain_e_z_to_S'] == n - 1
                    and row['chain_0_to_S'] == n and row['d1_e_z_to_S'] == n - 1):
                raise CheckFailure('distance to the new supports ' + name)
        r_ = src_rows['N=%d' % n]
        m2 = 2 * n
        f2count = lambda mm: 21 * mm ** 3 + 35 * mm ** 2 + 14 * mm
        need(r_['F1_nested']['new_stars'] == 8 * (3 * n * n + 3 * n + 1)
             and r_['F1_nested']['new_faces'] == 168 * (3 * n * n + 3 * n + 1)
             and r_['F2_nested']['new_faces'] == 56 * (9 * n * n + 14 * n + 6) == f2count(m2 + 2) - f2count(m2)
             and r_['F1_vs_F2']['new_faces'] == 28 * n * (5 * n + 1) == f2count(m2) - 21 * m2 ** 3
             and r_['F1_nested']['dinf_e_z_to_B'] == n and r_['F1_nested']['dinf_0_to_B'] == n + 1
             and r_['F2_nested']['dinf_e_z_to_B'] == n and r_['F1_vs_F2']['dinf_e_z_to_B'] == n - 1
             and r_['F1_vs_F2']['dinf_0_to_B'] == n and r_['F1_vs_F2']['supports_inside_source_set'] is True
             and r_['F1_nested']['supports_inside_source_set'] is False
             and r_['F2_nested']['supports_inside_source_set'] is False
             and r_['F1_nested']['max_new_faces_per_site'] == 49 and r_['F1_nested']['J_new_over_tau'] == '28',
             'boundary_sources_N%d' % n, distances_e_z_to_new_supports=n - 1, distances_0_to_new_supports=n)
        # F1 versus F2: anchors, owner sets inside the outer layer, regrouped per anchor, charged once
        extra = {k: v for k, v in f2n.items() if k not in f1n}
        groups = {}
        for (b, idx), own in extra.items():
            sat = tuple(sorted(i for i in range(3) if b[i] == n))
            if not sat or not all(p[i] == n for p in own for i in sat[:1]):
                raise CheckFailure('extra face not anchored on the outer layer')
            groups.setdefault(b, []).append(idx)
        sizes = {}
        for b, idxs in groups.items():
            sat = ''.join('xyz'[i] for i in range(3) if b[i] == n)
            sizes.setdefault(sat, set()).add(len(idxs))
        need(sizes == {'x': {17}, 'y': {13}, 'z': {5}, 'xy': {10}, 'xz': {3}, 'yz': {1}}
             and sum(len(v) for v in groups.values()) == len(extra) == 28 * n * (5 * n + 1)
             and len({k for k in extra}) == len(extra), 'f1_vs_f2_extra_faces_regrouped_once_N%d' % n,
             group_sizes={k: sorted(v) for k, v in sorted(sizes.items())}, corner_anchor_group=0,
             count_formula='(2N)^2(17+13+5)+2N(10+3+1)=28N(5N+1)')
        # F2 nested: face-by-face charge versus double charge of whole regrouped anchors
        grp_n, grp_m = {}, {}
        for (b, idx) in f2n:
            grp_n.setdefault(b, set()).add(idx)
        for (b, idx) in f2m:
            grp_m.setdefault(b, set()).add(idx)
        changed = [b for b in grp_m if grp_m[b] != grp_n.get(b, set())]
        double = sum(len(grp_m[b]) for b in changed)
        new_f2 = r_['F2_nested']['new_faces']
        need(double > new_f2 and double - new_f2 == sum(len(grp_n.get(b, set())) for b in changed),
             'f2_nested_charged_face_by_face_once_N%d' % n, new_faces=new_f2, whole_group_recharge=double,
             old_faces_double_charged=double - new_f2)
        src_rows['N=%d' % n]['F2_nested']['double_charged_count'] = double
    # every pair of centered boxes of F1 or F2 is one nested comparison (face sets are totally ordered)
    pair_rows = []
    fams = {('F1', m): f1_faces(cube(m)) for m in (2, 3, 4)}
    fams.update({('F2', m): f2_faces(cube(m)) for m in (2, 3, 4)})
    order = [('F1', 2), ('F2', 2), ('F1', 3), ('F2', 3), ('F1', 4), ('F2', 4)]
    for i_, a_key in enumerate(order):
        for b_key in order[i_ + 1:]:
            small, big = fams[a_key], fams[b_key]
            if not set(small) <= set(big):
                raise CheckFailure('face sets not nested')
            pts = set().union(*[big[k] for k in big if k not in small])
            dz, d0 = set_dist(E_Z, pts, dinf), set_dist(ORIGIN, pts, dinf)
            if dz != a_key[1] - 1 or d0 != a_key[1]:
                raise CheckFailure('pair distance')
            pair_rows.append({'smaller': '%s_%d' % a_key, 'larger': '%s_%d' % b_key, 'dinf_e_z': dz, 'dinf_0': d0})
    need(len(pair_rows) == 15, 'all_pairs_centered_boxes_one_nested_comparison', pairs=pair_rows,
         note='F1_N in F2_N in F1_(N+1) in F2_(N+1): every pair is nested, new supports at distance N-1 from e_z and '
              'N from 0 with N the smaller size, so the same K applies without telescoping')
    # literal reading of the source set ("sites met by the new terms") versus the named shell
    for n in (2, 3):
        lam, lam1 = cube(n), cube(n + 1)
        old_anchors = set(star_anchors(lam))
        lit = set()
        for b in star_anchors(lam1):
            if b not in old_anchors:
                lit.update(add(b, s) for s in S_STAR)
        inner = lit & lam
        layer = {p for p in lam if max(abs(x) for x in p) == n}
        need(inner <= layer and (0, 0, n) in inner and set_dist(E_Z, lit, dinf) == n - 1
             and set_dist(E_Z, lam1 - lam, dinf) == n, 'source_set_literal_reading_N%d' % n,
             literal_sites_inside_Lambda_N=len(inner), dinf_e_z_literal=n - 1, dinf_e_z_shell=n,
             note='the literal set of sites met by new stars adds outer-layer sites of Lambda_N; with it the source '
                  'loss is not charged and the exponent is N-1, with the shell the loss is charged and the exponent '
                  'is N: the same bound')
    # general volumes (any two finite volumes of one prescription containing Lambda_N, through the union)
    gv_rows = {}
    for n in (2, 3):
        v1 = cuboid((-n, -n, -n), (n + 1, n, n + 2))
        v2 = cuboid((-n - 1, -n, -n), (n, n + 1, n))
        un = v1 | v2
        for pres, fn in (('F1', f1_faces), ('F2', f2_faces)):
            a, b, u_ = fn(v1), fn(v2), fn(un)
            sym = [a[k] for k in a if k not in b] + [b[k] for k in b if k not in a]
            via = [u_[k] for k in u_ if k not in a] + [u_[k] for k in u_ if k not in b]
            if not (set(a) <= set(u_) and set(b) <= set(u_)):
                raise CheckFailure('union does not contain both volumes')
            rows = {}
            for label, sups in (('direct_symmetric_difference', sym), ('through_union', via)):
                pts = set().union(*sups)
                rows[label] = {'terms': len(sups), 'dinf_e_z': set_dist(E_Z, pts, dinf),
                               'dinf_0': set_dist(ORIGIN, pts, dinf)}
                if rows[label]['dinf_e_z'] < n - 1 or rows[label]['dinf_0'] < n:
                    raise CheckFailure('general volume distance')
            gv_rows['N=%d_%s' % (n, pres)] = rows
    need(True, 'general_volume_sources_at_least_N_minus_1', cases=sorted(gv_rows),
         note='every term of one volume missing from the other contains a site outside Lambda_N, so it lies at '
              'l_inf distance at least N-1 from e_z and N from 0 (all sizes)')

    # 5. constants at both frozen pairs, both signs, both routes, crude tier
    signs = (tau, -tau)
    const = {}
    for sgn in signs:
        at = abs(sgn)
        wm = w_max_of(at)
        row = {
            'fwd_head': weighted_k(at, F(64), F(64), 'exact_first_order')[0],
            'fwd_head_sharp': weighted_k(at, F(64), F(64), 'exact_first_order', loss_charged=False)[0],
            'fwd_head_crude': weighted_k(at, F(64), F(64), 'crude_majorant')[0],
            'fwd_floor': weighted_k(at, wm, wm, 'exact_first_order')[0],
            'fwd_floor_sharp': weighted_k(at, wm, wm, 'exact_first_order', loss_charged=False)[0],
            'fwd_floor_crude': weighted_k(at, wm, wm, 'crude_majorant')[0],
            'rev_head': analytic_k(at, 64 * at, 'exact_first_order'),
            'rev_head_coefwise': analytic_k(at, 64 * at, 'exact_first_order', cauchy='coefficientwise'),
            'rev_head_sharp': analytic_k(at, 64 * at, 'exact_first_order', count='sharp'),
            'rev_head_remainder': analytic_k(at, 64 * at, 'exact_first_order', sup='two_remainder'),
            'rev_head_crude': analytic_k(at, 64 * at, 'crude_majorant', sup='two_selfmap'),
            'rev_floor': analytic_k(at, tau_star, 'exact_first_order'),
            'rev_floor_sharp': analytic_k(at, tau_star, 'exact_first_order', count='sharp'),
            'rev_floor_crude': analytic_k(at, tau_star, 'crude_majorant', sup='two_R'),
            'rev_floor_crude_coefwise': analytic_k(at, tau_star, 'crude_majorant', sup='two_R',
                                                   cauchy='coefficientwise'),
        }
        const['+' if sgn > 0 else '-'] = row
    need(const['+'] == const['-'], 'both_signs_identical', note='every bound depends on |tau| only')
    cst = const['+']
    t_head = weighted_t(tau, F(64))
    t_floor = weighted_t(tau, w_max)
    rho_an = R / (28 * g_up(R))
    need(rho_an > tau_star and 64 * tau < tau_star and 28 * 64 * tau * G_R <= R and 28 * tau_star * GP_R < 1,
         'analytic_discs_inside_contraction_domain', analyticity_radius_lower=q(rho_an),
         note='the closed disc of radius tau_star lies inside the open disc R/(28 G(R)) on which the AM2 map is a '
              'contraction, so the coefficients are analytic on a neighbourhood of both closed discs')
    need(t_head == F(49, 223580736) and t_head == analytic_t(64 * tau) and t_floor == analytic_t(tau_star),
         'weighted_T_equals_disc_T', T_w64=q(t_head), T_w_max=q(t_floor),
         note='the weight w and the disc radius w|tau| give the same exact first-order majorant')
    need(cst['fwd_head'] <= k_head and cst['rev_head'] <= k_head and cst['rev_head_coefwise'] <= k_head
         and cst['fwd_floor'] <= k_floor and cst['rev_floor'] <= k_floor and cst['fwd_floor_crude'] <= k_floor
         and cst['rev_floor_crude'] <= k_floor and cst['rev_floor_crude_coefwise'] <= k_floor
         and cst['fwd_head_crude'] > k_head and cst['rev_head_crude'] > k_head, 'frozen_targets_met_crude_fails',
         margins={k: preview(k_head / v) for k, v in cst.items() if k.endswith(('head', 'coefwise', 'sharp',
                                                                                    'remainder', 'crude'))
                  and k.startswith(('fwd_head', 'rev_head'))})
    need(cst['fwd_head_sharp'] * 64 == cst['fwd_head'] and cst['rev_head_sharp'] * 64 == cst['rev_head']
         and cst['fwd_floor_sharp'] * w_max == cst['fwd_floor'] and cst['rev_floor_sharp'] == cst['rev_floor'] * q_floor,
         'sharp_forms_differ_by_exactly_q', note='sharp count: order >= N at e_z for every comparison')
    union_fwd, union_rev = 2 * cst['fwd_head'], 2 * cst['rev_head']
    need(union_fwd <= k_head and union_rev > k_head and cst['rev_head'] <= k_head, 'general_volume_through_union',
         forward_union=q(union_fwd), reverse_union=q(union_rev),
         note='the reverse must compare general volumes directly (one sup bound, same order count) or use a sharper '
              'sup or count; through the union its contract-form constant 2x2T(64|tau|) misses 1/2000000')
    tele_fwd = cst['fwd_head'] / (1 - q_head)
    need(tele_fwd <= k_head and cst['rev_head_coefwise'] <= k_head, 'telescoped_all_pairs_constant',
         forward_K_over_1_minus_q=q(tele_fwd), note='the chain F1_N in F2_N in F1_N+1 gives every pair of centered '
                                                  'boxes in one nested comparison without the telescoping factor')
    admitted_sup = j0 * G_R / (1 - j0 * GP_R)
    need(admitted_sup == F(37, 6249384) and 2 * j0 * GP_R == F(77, 390625) and F(77, 390625) < q_floor,
         'global_lipschitz_gives_no_decay', sup_norm_difference=q(admitted_sup),
         global_lipschitz=q(F(77, 390625)), note='a per-shell factor 77/390625 would cross q_min')
    # scaling ratios
    small = tau / 100
    ratios = {
        'K_headline_forward': cst['fwd_head'] / weighted_k(small, F(64), F(64), 'exact_first_order')[0],
        'K_headline_forward_sharp': cst['fwd_head_sharp'] / weighted_k(small, F(64), F(64), 'exact_first_order',
                                                                       loss_charged=False)[0],
        'K_headline_reverse': cst['rev_head'] / analytic_k(small, 64 * small, 'exact_first_order'),
        'K_floor_forward': cst['fwd_floor'] / weighted_k(small, w_max_of(small), w_max_of(small),
                                                         'exact_first_order')[0],
        'K_floor_forward_sharp': cst['fwd_floor_sharp'] / weighted_k(small, w_max_of(small), w_max_of(small),
                                                                     'exact_first_order', loss_charged=False)[0],
        'K_floor_forward_crude': cst['fwd_floor_crude'] / weighted_k(small, w_max_of(small), w_max_of(small),
                                                                     'crude_majorant')[0],
        'K_floor_reverse': cst['rev_floor'] / analytic_k(small, tau_star, 'exact_first_order'),
        'K_floor_reverse_sharp': cst['rev_floor_sharp'] / analytic_k(small, tau_star, 'exact_first_order',
                                                                     count='sharp'),
        'K_floor_reverse_crude_coefwise': cst['rev_floor_crude_coefwise'] / analytic_k(
            small, tau_star, 'crude_majorant', sup='two_R', cauchy='coefficientwise'),
        'q_min': q_floor / (37888 * small),
    }
    hb, fb, qb = brackets['K_exact_first_order_at_q_1_64'], brackets['K_floor_pair'], brackets['q_min']
    need(hb[0] <= ratios['K_headline_forward'] <= hb[1] and hb[0] <= ratios['K_headline_reverse'] <= hb[1]
         and ratios['K_headline_forward_sharp'] == ratios['K_headline_forward']
         and ratios['K_floor_forward'] == 1 and ratios['K_floor_reverse'] == 1
         and fb[0] <= ratios['K_floor_reverse_crude_coefwise'] <= fb[1] and ratios['K_floor_forward_crude'] == 1
         and ratios['q_min'] == 100 and qb[0] == ratios['q_min'],
         'tau_scaling_contract_forms_in_brackets', ratios={k: q(v) for k, v in ratios.items()})
    need(ratios['K_floor_forward_sharp'] == 100 and ratios['K_floor_reverse_sharp'] == 100
         and not (fb[0] <= ratios['K_floor_forward_sharp'] <= fb[1]), 'floor_bracket_rejects_sharp_forms',
         note='contract defect D2: the frozen floor bracket fits only the contract-lemma form; a sharp floor '
              'constant (exact ratio 100) is a labelled refinement')

    # 6. fixtures for the traps
    # (a) weight direction: chain 0..L, source at L, delta=(I-jA)^{-1}e_L, A nearest-neighbour plus identity
    jj, qq = F(1, 10), F(1, 2)
    chain_rows, prev_good, prev_bad, prev_exact = [], None, None, None
    for ell in range(2, 9):
        rhs = [F(0)] * ell + [F(1)]
        x = solve_tridiagonal(ell + 1, 1 - jj, -jj, rhs)
        good = qq ** ell / (1 - 3 * jj / qq)
        bad = (1 / qq) ** ell / (1 - 3 * jj / qq)
        if not (0 < x[0] <= good and x[0] < bad and (prev_good is None or (good < prev_good and bad > prev_bad
                                                                           and x[0] < prev_exact))):
            raise CheckFailure('weight direction fixture')
        prev_good, prev_bad, prev_exact = good, bad, x[0]
        chain_rows.append({'L': ell, 'exact_delta_0': q(x[0]), 'weight_from_source_bound': q(good),
                           'weight_from_R_bound': q(bad)})
    need(True, 'fixture_weight_direction', rows=chain_rows, model='FG(chain, delta=e_L+jA delta, j=1/10, q=1/2)',
         transfers_to_aq=False, note='the weight growing towards R decays; the weight growing from R grows with L')
    # (b) global Lipschitz is not decay: rank-one all-to-all coupling
    mf_rows = []
    for ell in range(2, 7):
        n_ = ell + 1
        d0 = jj / ((1 - jj) * n_)
        # verify (I - jP) delta = e_L exactly with delta = e_L + j/(1-j) P e_L
        vec = [jj / ((1 - jj) * n_)] * n_
        vec[-1] += 1
        mean = sum(vec) / n_
        if any((vec[i] - jj * mean) != (1 if i == ell else 0) for i in range(n_)):
            raise CheckFailure('mean-field solve')
        claim = jj ** ell / (1 - jj)
        if not d0 > claim:
            raise CheckFailure('mean-field fixture')
        mf_rows.append({'L': ell, 'exact_delta_0': q(d0), 'lipschitz_power_claim': q(claim)})
    need(True, 'fixture_global_lipschitz_not_decay', rows=mf_rows, lipschitz=q(jj),
         model='FG(complete graph, delta=e_L+jP delta, P rank-one mean)', transfers_to_aq=False)
    # (c) per-creation loss fails on the exact first-order coefficient
    w_first = w64 * sqrt_sum_lo * tau / 144
    w_rem = j0 * w64 * (g_up(t_head) - 16)
    per_creation_claim = t1_of(tau) / (1 - j0 * gp_up(t1_of(tau)))
    need(w_first - w_rem > 3 * per_creation_claim, 'fixture_per_creation_loss_fails',
         weighted_first_order_lower=q(w_first), weighted_remainder_upper=q(w_rem),
         per_creation_claim=q(per_creation_claim),
         note='||c||_w >= ||c^(1)||_w - ||c-c^(1)||_w exceeds the per-creation claim: every first-order owner set '
              'has diameter 1 while no creation enters L_0')
    # (d) disconnected output and the max shortcut (actual owner sets)
    ex = [frozenset({(1, 0, 0), (2, 0, 0)}), frozenset({ORIGIN, (-1, 0, 0)})]
    m_out = frozenset({(2, 0, 0), (-1, 0, 0)})
    need(all(i_ & x_star for i_ in ex) and not (ex[0] & ex[1]) and diam(m_out, dinf) == 3
         == 1 + sum(diam(i_, dinf) for i_ in ex) and 1 + max(diam(i_, dinf) for i_ in ex) < 3
         and m_out == (ex[0] | ex[1]) - x_star, 'fixture_disconnected_output_equality',
         I=[sorted(i_) for i_ in ex], M=sorted(m_out))
    # (e) pure distance weight without diameter weights on the other creations
    bsrc = frozenset({(10, 0, 0)})
    rho_b = lambda st: max(set_dist(p, bsrc, dinf) for p in st)
    i_delta, i_other = frozenset({(1, 0, 0), (2, 0, 0)}), frozenset({ORIGIN, (-1, 0, 0)})
    m2_ = frozenset({(2, 0, 0), (-1, 0, 0)})
    need(rho_b(m2_) - rho_b(i_delta) == 2 == 1 + diam(i_other, dinf), 'fixture_pure_distance_weight_undercharges',
         excess=2, charged_without_diameter_weight=1)
    # (f) coefficient decay is not marginal decay (AV1 F13 type)
    a_, b_, g_ = F(1, 3), F(1, 2), F(2, 5)
    rho_b1 = reduced_site0(creation_state(3, [((0, 1), a_), ((1,), b_), ((2,), g_)]))
    rho_b0 = reduced_site0(creation_state(3, [((0, 1), a_), ((1,), F(0)), ((2,), g_)]))
    rho_g0 = reduced_site0(creation_state(3, [((0, 1), a_), ((1,), b_), ((2,), F(0))]))
    need(rho_b1 == [[F(45, 49), F(6, 49)], [F(6, 49), F(4, 49)]] and rho_b0 == [[F(9, 10), 0], [0, F(1, 10)]]
         and rho_g0 == rho_b1, 'fixture_coefficient_decay_not_marginal_decay',
         rho_r_b_half=[[q(x) for x in r_] for r_ in rho_b1], rho_r_b_zero=[[q(x) for x in r_] for r_ in rho_b0],
         note='coefficients meeting R (a) unchanged; the outside coefficient b changes rho_r through the '
              'straddling support; the decoupled g cancels', transfers_to_aq=False)
    # (g) cardinality weight and l1 alternative
    need((F(1395, 10000)) ** 4 < q_floor < (F(1396, 10000)) ** 4, 'fixture_cardinality_rate_0_1395',
         note='|X|<=4: loss w^4, rate q_min^(1/4) in (0.1395, 0.1396) per site')
    l1_lo, l1_hi = sqrt_bracket(148 * 390625, 10 ** 6)
    need(j0 * w64 ** 2 * G_R > R and (l1_lo / 390625) ** 2 <= q_floor <= (l1_hi / 390625) ** 2,
         'fixture_l1_alternative_rate', selfmap_l1_w64=q(j0 * w64 ** 2 * G_R),
         q_min_l1_bracket=[q(l1_lo / 390625), q(l1_hi / 390625)],
         note='l1 diameters (d_X=2) cannot realize q=1/64 per step; q_min per l1 step is q_min^(1/2)')
    # (h) star-count weight n(I) on the unit cube (diameter 1)
    unit = frozenset(product((0, 1), repeat=3))
    cand_b = sorted({sub(p, s) for p in unit for s in S_STAR})
    n_cube = None
    for k in range(1, 6):
        for combo in combinations(cand_b, k):
            stars = [frozenset(add(b, s) for s in S_STAR) for b in combo]
            if not unit <= frozenset().union(*stars):
                continue
            seen, stack = {0}, [0]
            while stack:
                i = stack.pop()
                for j in range(k):
                    if j not in seen and stars[i] & stars[j]:
                        seen.add(j)
                        stack.append(j)
            if len(seen) == k:
                n_cube = k
                break
        if n_cube is not None:
            break
    need(n_cube is not None and n_cube > diam(unit, dinf) == 1, 'fixture_star_count_exceeds_diameter',
         unit_cube_star_count=n_cube, unit_cube_linf_diameter=1)
    # (i) ball radius is not the tree ratio: at |tau|=1/2000000 (arithmetic fixture) w=64 fails, R does not move
    tau_x = F(1, 2000000)
    need(j_of(tau_x) * w64 * G_R > R and tau_x < tau_star, 'fixture_ball_radius_not_tree_ratio',
         selfmap_w64=q(j_of(tau_x) * w64 * G_R), note='q=1/64 is realized by w=64 only while J w G(R) <= R')
    # (j) a rate at another radius
    r_alt = F(29, 400)
    q_alt = j0 * g_up(r_alt) / r_alt
    need(j0 * g_up(r_alt) <= r_alt and j0 * gp_up(r_alt) < 1 and q_alt < q_floor, 'fixture_rate_at_other_radius',
         radius=q(r_alt), q_at_radius_upper=q(q_alt), note='below q_min at R; admissible only with its radius named')

    # 7. validator and the 37 contract controls
    f2_double_n2 = src_rows['N=2']['F2_nested']['double_charged_count']
    comparisons_ref = {
        'F1_nested': {'source_set': 'shell', 'source_count_N2': 3192, 'double_charged_N2': None,
                      'charging': 'whole_new_stars', 'dist_e_z_to_B': 'N', 'dist_0_to_B': 'N+1'},
        'F2_nested': {'source_set': 'shell', 'source_count_N2': 3920, 'double_charged_N2': f2_double_n2,
                      'charging': 'face_by_face', 'dist_e_z_to_B': 'N', 'dist_0_to_B': 'N+1'},
        'F1_vs_F2': {'source_set': 'outer_layer', 'source_count_N2': 616, 'double_charged_N2': None,
                     'charging': 'face_by_face_at_anchor', 'dist_e_z_to_B': 'N-1', 'dist_0_to_B': 'N'},
        'general_volumes': {'source_set': 'symmetric_difference', 'source_count_N2': None, 'double_charged_N2': None,
                            'charging': 'face_by_face', 'dist_e_z_to_B': 'N-1', 'dist_0_to_B': 'N'},
    }
    ctx = {
        'controls': controls, 'inventory': inventory, 'tau_abs': tau, 'w_max': w_max, 'tau_star': tau_star,
        'q_min': q_floor, 'pairs': {'headline': {'q': q_head, 'K': k_head}, 'floor': {'q': q_floor, 'K': k_floor}},
        'w_max_at': {'headline': w_max, 'floor': w_max}, 'brackets': brackets, 'brackets_text': brackets_text,
        'gate_fields': gate_fields, 'sentence': sentence, 'forbidden': forbidden,
        'family_defs': {'F1': 'AQ1 centered whole-star boxes', 'F2': 'I1 section 6 all-contained-face boxes with '
                                                                     'padding'},
        'parameter_keys_required': ['metric', 'weights', 'window', 'clock', 'N_min', 'rate_constant_pair',
                                    'comparisons', 'cutoff'],
        'comparisons': comparisons_ref, 'headline_q_basis': 'weight w=64 (forward) or disc 64|tau| (reverse)',
    }

    def rec(cid, pair, tier, route, form, value, inputs, t_rule='self_consistent', labelled=False):
        return {'id': cid, 'pair': pair, 'q': q_head if pair == 'headline' else q_floor, 'tier': tier,
                'route': route, 'form': form, 'value': value, 'inputs': inputs, 'exponent': 'N-1',
                'target': k_head if pair == 'headline' else k_floor,
                'meets_target': value <= (k_head if pair == 'headline' else k_floor),
                'first_order': 'exact_AV1' if tier == 'exact_first_order' else 'none', 't_rule': t_rule,
                'labelled': labelled, 'signs': ['+', '-']}

    wf = {'w': F(64), 'e_beta': F(64), 'loss_charged': True}
    wfl = {'w': w_max, 'e_beta': w_max, 'loss_charged': True}
    an_h = {'rho': 64 * tau, 'sup': 'two_T', 'count': 'contract', 'cauchy': 'schwarz'}
    an_f = {'rho': tau_star, 'sup': 'two_T', 'count': 'contract', 'cauchy': 'schwarz'}
    an_c = {'rho': 64 * tau, 'sup': 'two_selfmap', 'count': 'contract', 'cauchy': 'schwarz'}
    constants_ref = [
        rec('K_headline_forward', 'headline', 'exact_first_order', 'weighted_norm', 'contract_lemma',
            cst['fwd_head'], wf),
        rec('K_headline_reverse', 'headline', 'exact_first_order', 'analytic_disc', 'contract_lemma',
            cst['rev_head'], an_h),
        rec('K_floor_forward', 'floor', 'exact_first_order', 'weighted_norm', 'contract_lemma', cst['fwd_floor'], wfl),
        rec('K_floor_reverse', 'floor', 'exact_first_order', 'analytic_disc', 'contract_lemma', cst['rev_floor'],
            an_f),
        rec('K_crude_forward', 'headline', 'crude_majorant', 'weighted_norm', 'contract_lemma', cst['fwd_head_crude'],
            wf, t_rule='crude'),
        rec('K_crude_reverse', 'headline', 'crude_majorant', 'analytic_disc', 'contract_lemma', cst['rev_head_crude'],
            an_c, t_rule='crude'),
    ]
    base = {
        'contract_sha256': CONTRACT_SHA256, 'controls_executed': {cid: True for cid in controls},
        'snapshots': list(inventory), 'reverse_inputs': list(inventory),
        'claims': {'continuum_claim': False, 'scientific_priority_verified': False, 'weak_coupling_claim': False},
        'model_id': MODEL_ID, 'triple': ['0', '0', '0'], 'tau_abs': tau, 'signs': ['+', '-'],
        'families': ['F1', 'F2'], 'family_defs': dict(ctx['family_defs']), 'N_min': 2,
        'parameters_declared': sorted(par), 'clock': CLOCK, 'window': WINDOW,
        'metric': 'coarse_linf', 'd_X': 1, 'distance_metric': 'coarse_linf',
        'l1_alternative': {'d_X': 2, 'labelled': True, 'mixed': False},
        'lemma': {'convention': 'coarse_linf', 'subadditivity': 'd_X+sum'},
        'weights': {'kind': 'diameter', 'star_count_mixed': False, 'direction': 'grows_from_source_toward_R',
                    'difference_weight': 'rho_B(I)=max_p d_inf(p,B)', 'other_creations_diameter_weighted': True,
                    'loss': 'per_interaction', 'w': F(64), 'e_beta': F(64), 'w_max': w_max},
        'contraction': {'selfmap': j0 * w64 * G_R, 'lipschitz': j0 * w64 * GP_R, 'rechecked_in_weighted_norm': True,
                        'cited_unweighted': False},
        'J_over_tau': 28, 'incoming_stars': 4,
        'face_counts': {'per_factor': 49, 'owner_sets': 15, 'meeting_R': 82, 'inside_R': 10,
                        'source': 'derived_I1_table'},
        'cover': {'sites': [[0, 0, 0], [0, 0, 1]], 'links': 48, 'endpoints': 36, 'anchors': 7},
        'decay_factor_source': 'weight_or_disc', 'lipschitz_decay_factor': None, 'R_as_tree_ratio': False,
        'headline_q_basis': ctx['headline_q_basis'],
        'analytic': {'rho_headline': 64 * tau, 'rho_floor': tau_star, 'rho_max': tau_star,
                     'extended_to_reduced_density': False, 'zero_free_region': None},
        'cutoff': {'statement': 'each Q_L, uniform in L', 'untruncated_claimed': False,
                   'cutoff_removed_for_coefficients': False},
        'rate_units': RATE_UNITS, 'rate_in_a': False, 'physical_length': None, 'uniform_in': UNIFORM_IN,
        'marginal': {'state_decay_inferred': False, 'fixture_exhibited': True}, 'combine': 'linear',
        'comparisons': {k: {'new_terms_only': True, 'source_count_N2': v['source_count_N2'],
                            'source_set': v['source_set'], 'charged_once': True, 'charging': v['charging'],
                            'dist_e_z_to_B': v['dist_e_z_to_B'], 'dist_0_to_B': v['dist_0_to_B'], 'exponent': 'N-1'}
                        for k, v in comparisons_ref.items()},
        'general_volume': {'route': 'direct', 'factor': 1},
        'constants': constants_ref, 'q_optimized_per_N': False,
        'missed': [{'id': 'K_crude_forward', 'dominating_term': 'crude source J G(T) without the first-order '
                                                                'enumeration', 'retuned': False},
                   {'id': 'K_crude_reverse', 'dominating_term': 'crude disc majorant 28 rho G(R)', 'retuned': False}],
        'verdict': 'accepted_within_scope',
        'scaling': {'K_headline_forward': ratios['K_headline_forward'], 'K_headline_reverse': ratios['K_headline_reverse'],
                    'K_floor_forward': ratios['K_floor_forward'], 'K_floor_reverse': ratios['K_floor_reverse'],
                    'q_min': ratios['q_min']},
        'scaling_bracket_of': {'K_headline_forward': 'K_exact_first_order_at_q_1_64',
                               'K_headline_reverse': 'K_exact_first_order_at_q_1_64',
                               'K_floor_forward': 'K_floor_pair', 'K_floor_reverse': 'K_floor_pair',
                               'q_min': 'q_min'},
        'brackets_declared': dict(brackets_text),
        'sub_labels': ['boundary_decay_rate_only', 'static_not_dynamic'],
        'limit_statements': ['The coefficients on supports meeting R converge along the whole sequence of centered '
                             'boxes of each named construction, in each on-site cutoff space (a Cauchy bound for '
                             'coefficients only; no state limit is asserted).'],
        'gate_fields': dict(gate_fields), 'sentence': sentence,
        'statements': [sentence + ' The rate is q per coarse step at fixed spacing.',
                       'This is not the thermodynamic limit and not uniqueness of any ground state.'],
        'contract_strings': list(strings_of(con)),
    }
    need(validate(base, ctx), 'reference_packet_accepted')

    nested = ('controls_executed', 'claims', 'family_defs', 'l1_alternative', 'lemma', 'weights', 'contraction',
              'face_counts', 'cover', 'analytic', 'cutoff', 'marginal', 'general_volume', 'gate_fields',
              'scaling', 'scaling_bracket_of', 'brackets_declared')

    def mut(**kw):
        pk = dict(base)
        for key in nested:
            pk[key] = dict(base[key])
        pk['comparisons'] = {k: dict(v) for k, v in base['comparisons'].items()}
        pk['constants'] = [dict(r_, inputs=dict(r_['inputs'])) for r_ in base['constants']]
        pk['missed'] = [dict(m) for m in base['missed']]
        for k, val in kw.items():
            if k.startswith('const:'):
                _, cid, field = k.split(':')
                for r_ in pk['constants']:
                    if r_['id'] == cid:
                        if field.startswith('inputs.'):
                            r_['inputs'][field[7:]] = val
                        else:
                            r_[field] = val
            elif k.startswith('comp:'):
                _, cname, field = k.split(':')
                pk['comparisons'][cname][field] = val
            elif '.' in k:
                head_, tail = k.split('.', 1)
                pk[head_][tail] = val
            else:
                pk[k] = val
        return lambda: validate(pk, ctx)

    ok = [('reference packet', lambda: validate(base, ctx))]
    control('coherent_evidence_tampering',
            [('contract hash rebound', mut(contract_sha256='0' * 64), 'contract hash'),
             ('control Boolean flipped', mut(**{'controls_executed.q_min_not_crossed': False}), 'control boolean'),
             ('snapshot removed', mut(snapshots=inventory[:-1]), 'snapshot missing'),
             ('headline halved with hashes rebound', mut(**{'const:K_headline_forward:value': cst['fwd_head'] / 2}),
              'constant not reproduced')], ok)
    control('exact_arithmetic_admission',
            [('float headline', mut(**{'const:K_headline_forward:value': float(cst['fwd_head'])}), 'exact arithmetic'),
             ('float ratio', mut(**{'scaling.q_min': 100.0}), 'exact arithmetic')], ok)
    control('no_priority_or_continuum_claim',
            [('continuum', mut(**{'claims.continuum_claim': True}), 'forbidden claim continuum_claim'),
             ('priority', mut(**{'claims.scientific_priority_verified': True}), 'forbidden claim scientific_priority'),
             ('weak coupling', mut(**{'claims.weak_coupling_claim': True}), 'forbidden claim weak_coupling')], ok)
    control('changed_model_relabelled',
            [('tau 1e-14', mut(tau_abs=F(1, 10 ** 14)), 'changed model'),
             ('uniform triple', mut(triple=['tau/24', 'tau/24', 'tau/24']), 'changed model'),
             ('finite-graph model id', mut(model_id='FG(qubit_chain)'), 'changed model'),
             ('one sign', mut(signs=['+']), 'changed model')], ok)
    control('insufficient_verdict_retained',
            [('crude reported as meeting', mut(**{'const:K_crude_forward:meets_target': True}), 'insufficient verdict'),
             ('missed list emptied', mut(missed=[]), 'insufficient verdict'),
             ('crude retuned', mut(missed=[dict(base['missed'][0], retuned=True), base['missed'][1]]),
              'insufficient verdict')], ok)
    control('tau_scaling_exponent',
            [('square-root headline ratio 10', mut(**{'scaling.K_headline_forward': F(10)}), 'tau scaling'),
             ('sharp floor ratio 100', mut(**{'scaling.K_floor_forward': ratios['K_floor_forward_sharp']}),
              'tau scaling'),
             ('bracket chosen after evaluation', mut(brackets_declared=dict(brackets_text, K_floor_pair='[99,101]')),
              'tau scaling')], ok, ratios={k: q(v) for k, v in ratios.items()})
    control('wrong_delta_alpha_hbar_clock',
            [('u labelled theta', mut(clock='theta=delta*t/hbar'), 'clock'),
             ('window in u', mut(window='|u| at most 1'), 'clock')], ok)
    control('missing_incoming_stars',
            [('outgoing star only', mut(J_over_tau=7), 'incoming stars'),
             ('one incoming star', mut(incoming_stars=1), 'incoming stars')], ok)
    control('root_n_misuse',
            [('rss of comparisons', mut(combine='rss'), 'root-N'),
             ('union factor sqrt2', mut(general_volume={'route': 'union', 'factor': F(1414, 1000)}), 'root-N')], ok)
    control('tier_mixing_rejected',
            [('exact label on crude t', mut(**{'const:K_headline_forward:t_rule': 'crude'}), 'tier mixing'),
             ('prospective id', mut(**{'const:K_headline_forward:tier': 'weighted_ii'}), 'tier mixing'),
             ('route outside vocabulary', mut(**{'const:K_headline_reverse:route': 'polymer_kp'}), 'tier mixing'),
             ('exact tier without AV1 coefficients', mut(**{'const:K_floor_reverse:first_order': 'none'}),
              'tier mixing')], ok)
    control('reverse_premise_isolation',
            [('triage in reverse', mut(reverse_inputs=inventory + ['research/round33/skeptic/triage.md']),
              'reverse premise isolation'),
             ('deliberation in reverse', mut(reverse_inputs=inventory + ['research/round33/advisor/deliberation-2.md']),
              'reverse premise isolation'),
             ('forward BA1 file', mut(reverse_inputs=inventory + ['research/round33/forward/ba1/report.md']),
              'reverse premise isolation')], ok,
            scope='synthetic inventory from the contract; the actual producer inputs/ were listed and hashed '
                  'outside this program (27 files each, byte-identical to the repository)')
    control('face_count_all_sites',
            [('site-0-only count', mut(**{'face_counts.per_factor': 21}), 'face count'),
             ('literal source', mut(**{'face_counts.source': 'literal'}), 'face count')], ok)
    control('uniform_in_N_not_in_a',
            [('uniform in N and a', mut(uniform_in='N and a'), 'uniform in a'),
             ('unqualified phrase', mut(statements=['The constant is uniform in a.']), 'uniform in a')], ok)
    control('placeholder_span_rejected',
            [('angle placeholder', mut(contract_strings=base['contract_strings'] + ['K at most <to be derived>']),
              'placeholder span'),
             ('e.g. span', mut(contract_strings=base['contract_strings'] + ['<e.g.1/64>']), 'placeholder span')],
            ok + [('inequality digraphs', mut(contract_strings=base['contract_strings'] + ['J<=28|tau| and N>=2']))])
    control('negation_aware_phrase_scan',
            [('affirmative forbidden', mut(statements=['The thermodynamic limit of the coefficients exists.']),
              'forbidden phrasing'),
             ('the AQ state', mut(statements=['The AQ state has these coefficients.']), 'forbidden phrasing')],
            ok + [('negated mention', mut(statements=['This is not the thermodynamic limit.']))])
    control('parameters_declare_metric_weights_window',
            [('window missing', mut(parameters_declared=[k for k in sorted(par) if k != 'window']),
              'parameters field missing'),
             ('metric missing', mut(parameters_declared=[k for k in sorted(par) if k != 'metric']),
              'parameters field missing')], ok)
    control('global_lipschitz_not_decay',
            [('lipschitz as per-shell factor', mut(lipschitz_decay_factor=F(77, 390625)), 'global Lipschitz'),
             ('decay from contraction', mut(decay_factor_source='global_lipschitz'), 'global Lipschitz')], ok,
            fixture='fixture_global_lipschitz_not_decay')
    control('weighted_norm_contraction_rechecked',
            [('weight above maximum', mut(**{'weights.w': F(3000), 'weights.e_beta': F(64)}),
              'weighted contraction'),
             ('unweighted constants cited', mut(**{'contraction.cited_unweighted': True}), 'weighted contraction'),
             ('self-map not re-evaluated', mut(**{'contraction.selfmap': F(37, 6250000)}), 'weighted contraction')],
            ok)
    control('loss_per_interaction_not_per_creation',
            [('per creation', mut(**{'weights.loss': 'per_creation'}), 'loss per interaction'),
             ('source loss omitted', mut(**{'const:K_headline_forward:inputs.loss_charged': False,
                                            'const:K_headline_forward:value': cst['fwd_head_sharp']}),
              'loss per interaction')], ok, fixture='fixture_per_creation_loss_fails')
    control('diameter_subadditivity_through_interaction',
            [('max shortcut', mut(lemma={'convention': 'coarse_linf', 'subadditivity': 'd_X+max'}),
              'diameter subadditivity')], ok, fixture='fixture_disconnected_output_equality')
    control('coarse_metric_named',
            [('l1 distance with l_inf weight', mut(distance_metric='coarse_l1'), 'metric'),
             ('d_X 2 in l_inf', mut(d_X=2), 'metric'),
             ('l1 mixed', mut(l1_alternative={'d_X': 2, 'labelled': True, 'mixed': True}), 'metric')], ok)
    control('weight_direction_toward_source',
            [('weight grows from R', mut(**{'weights.direction': 'grows_from_R'}), 'weight direction'),
             ('pure distance weight', mut(**{'weights.other_creations_diameter_weighted': False}),
              'weight direction')], ok, fixtures=['fixture_weight_direction', 'fixture_pure_distance_weight_undercharges'])
    control('cardinality_weight_rate_labelled',
            [('cardinality relabelled as diameter', mut(**{'weights.kind': 'cardinality'}), 'cardinality weight')],
            ok, fixture='fixture_cardinality_rate_0_1395')
    control('boundary_distance_exact',
            [('shell off by one', mut(**{'comp:F1_nested:dist_e_z_to_B': 'N-1'}), 'boundary distance'),
             ('outer layer off by one', mut(**{'comp:F1_vs_F2:dist_e_z_to_B': 'N'}), 'boundary distance'),
             ('exponent N', mut(**{'comp:F2_nested:exponent': 'N'}), 'boundary distance')], ok)
    control('boundary_source_new_terms_only',
            [('all F2 faces charged', mut(**{'comp:F1_vs_F2:source_count_N2': 1960}), 'boundary source'),
             ('old terms admitted', mut(**{'comp:F1_nested:new_terms_only': False}), 'boundary source')], ok)
    control('f2_regrouping_charged_once',
            [('whole regrouped anchors recharged', mut(**{'comp:F2_nested:source_count_N2': f2_double_n2}),
              'F2 regrouping'),
             ('charged twice flag', mut(**{'comp:F2_nested:charged_once': False}), 'F2 regrouping')], ok)
    control('rate_constant_pair_prefrozen',
            [('target retuned', mut(**{'const:K_headline_forward:target': F(1, 1000000)}), 'rate constant pair'),
             ('q optimized per N', mut(q_optimized_per_N=True), 'rate constant pair'),
             ('headline q changed', mut(**{'const:K_headline_forward:q': F(1, 100)}), 'rate constant pair')], ok)
    control('q_min_not_crossed',
            [('global Lipschitz as rate', mut(**{'const:K_floor_forward:q': F(77, 390625)}), 'q_min crossed'),
             ('rate at other radius unnamed', mut(**{'const:K_floor_reverse:q': q_alt}), 'q_min crossed')], ok,
            fixture='fixture_rate_at_other_radius')
    control('analytic_route_disc_radius',
            [('disc beyond tau_star', mut(**{'analytic.rho_floor': 2 * tau_star}), 'disc radius'),
             ('extended to rho_R', mut(**{'analytic.extended_to_reduced_density': True}), 'disc radius'),
             ('headline radius wrong', mut(**{'const:K_headline_reverse:inputs.rho': 100 * tau}), 'disc radius')], ok)
    control('untruncated_coefficients_not_asserted',
            [('untruncated', mut(**{'cutoff.untruncated_claimed': True}), 'untruncated'),
             ('cutoff removed', mut(**{'cutoff.cutoff_removed_for_coefficients': True}), 'untruncated')], ok)
    control('decay_rate_in_N_not_a',
            [('rate per fm', mut(rate_units='per fm'), 'rate in a'),
             ('rate in a', mut(rate_in_a=True), 'rate in a'),
             ('physical length', mut(physical_length='0.3 fm'), 'rate in a')], ok)
    control('coefficient_decay_not_marginal_decay',
            [('state decay inferred', mut(**{'marginal.state_decay_inferred': True}), 'marginal'),
             ('fixture missing', mut(**{'marginal.fixture_exhibited': False}), 'marginal')], ok,
            fixture='fixture_coefficient_decay_not_marginal_decay')
    control('two_families_named',
            [('one family', mut(families=['F1']), 'two families'),
             ('orthant substituted', mut(family_defs={'F1': 'AQ1 centered whole-star boxes', 'F2': 'orthant boxes'}),
              'two families')], ok)
    control('subsequence_versus_whole_sequence',
            [('unqualified limit', mut(limit_statements=['The coefficients converge.']), 'subsequence'),
             ('whole sequence of states', mut(**{'gate_fields.whole_sequence_claimed': True}), 'subsequence')], ok)
    control('full_original_wilson_cover',
            [('one-factor cover', mut(cover={'sites': [[0, 0, 0]], 'links': 24, 'endpoints': 22, 'anchors': 4}),
              'cover'),
             ('four drawn links', mut(**{'cover.links': 4}), 'cover')], ok)
    control('gate_fields_topic_specific',
            [('scope missing', mut(gate_fields={k: v for k, v in gate_fields.items()
                                                if k != 'coefficient_cauchy_scope'}), 'gate field'),
             ('state decay claimed', mut(**{'gate_fields.state_decay_claimed': True}), 'gate field'),
             ('sub-label outside vocabulary', mut(sub_labels=['convergence_of_named_constructions']), 'gate field'),
             ('template edited', mut(sentence=sentence.replace('not decay of the reduced density', 'decay')),
              'mandatory sentence')], ok,
            reading='no frozen semantics; exported fields must equal preregistration.gate_fields_required')
    control('ball_radius_not_used_as_tree_decay_ratio',
            [('R as tree ratio', mut(R_as_tree_ratio=True), 'ball radius'),
             ('basis rewritten', mut(headline_q_basis='ball radius R=1/64 per step'), 'ball radius')], ok,
            fixture='fixture_ball_radius_not_tree_ratio')
    ids = set(controls)
    done = {row['id'] for row in CHECKS if row.get('kind') == 'control'}
    missing = sorted(ids - done)
    n_mut = sum(len(row['mutations']) for row in CHECKS if row.get('kind') == 'control')
    need(not missing, 'contract_controls_covered', implemented=len(ids & done), of=len(ids), mutations=n_mut,
         deferred=missing)

    constants_out = {k: {'value': q(v), 'preview': preview(v)} for k, v in sorted(cst.items())}
    return {
        'loop': 'BA1', 'stage': 'pre_comparison', 'reviewer': 'skeptic (model agent, correlated ancestry)',
        'human_author': 'Hruday N M (BUNZEEY)', 'contract_sha256': c_sha, 'contract_frozen_at': con['frozen_at'],
        'model': MODEL_ID + ': SU(2) Kogut-Susskind form on Z^3 at fixed spacing, coarse 24-link factors, selected '
                            'triple (0,0,0), Haar product reference, 21 omitted faces per anchor with -(tau/3)W_f; '
                            'both signs |tau|<=10^-8; AM2 creation expansion (J<=28|tau|, R=1/64, '
                            'G(t)=16e^{8t}(1+10t)) in each on-site cutoff space; families F1 (AQ1 whole-star) and F2 '
                            '(I1 section 6 all-contained-face with padding) on centered Lambda_N, N at least 2; '
                            'cover R={0,e_z}',
        'scratch': '/tmp/claude-0/skeptic-ba1-private/ (private, disclosed; not evidence)',
        'geometry': {'enumeration': geo_rows, 'star_diameters': {'linf': 1, 'l1': 2},
                     'owner_set_diameters': {'linf': 1, 'l1': [1, 2]},
                     'counts': {'per_factor': 49, 'owner_sets': 15, 'meeting_R': 82, 'inside_R': 10,
                                'grouped_sqrt_sum_lower': q(sqrt_sum_lo)}},
        'weighted_contraction': {
            'norm': '||c||_w = max_u sum_{I ni u} w^{diam_inf I} ||c_I||', 'loss': 'w^{d_X}=w once per interaction',
            'w_headline': '64', 'w_max': q(w_max), 'selfmap_w64': q(j0 * w64 * G_R), 'lipschitz_w64': q(j0 * w64 * GP_R),
            'selfmap_w_max': q(j0 * w_max * G_R), 'lipschitz_w_max': q(j0 * w_max * GP_R),
            'T_w64_exact_first_order': q(t_head), 'T_w_max_exact_first_order': q(t_floor),
            'T_w64_crude': q(j0 * w64 * G_R), 'coupling_threshold_w64': '1/2424832'},
        'order_versus_distance': {'lemma_sharp': 'first nonzero order >= 1 + ceil(d_inf(u,S)/1)',
                                  'contract_form': 'ceil(d/diam)', 'tables': tables, 'algebraic_fixture': toy},
        'boundary_sources': {'rows': src_rows, 'general_volumes': gv_rows,
                             'formulas': {'F1_nested_new_stars': '8(3N^2+3N+1)', 'F1_nested_new_faces': '168(3N^2+3N+1)',
                                          'F2_nested_new_faces': '56(9N^2+14N+6)', 'F1_vs_F2_extra_faces': '28N(5N+1)',
                                          'chain': 'F1_N in F2_N in F1_(N+1) in F2_(N+1) as face sets'},
                             'distances': {'d_inf(e_z, new supports)': 'N-1 (all comparisons)',
                                           'd_inf(0, new supports)': 'N', 'd_inf(e_z, shell)': 'N',
                                           'd_inf(0, shell)': 'N+1', 'd_inf(e_z, outer layer)': 'N-1',
                                           'd_inf(0, outer layer)': 'N'}},
        'constants': constants_out,
        'analytic_route': {'tau_star': q(tau_star), 'rho_headline': q(64 * tau), 'rho_floor': q(tau_star),
                           'selfmap_rho_headline': q(28 * 64 * tau * G_R), 'lipschitz_rho_headline': q(28 * 64 * tau * GP_R),
                           'selfmap_rho_floor': q(28 * tau_star * G_R), 'lipschitz_rho_floor': q(28 * tau_star * GP_R),
                           'T_rho_headline': q(analytic_t(64 * tau)), 'T_rho_floor': q(analytic_t(tau_star)),
                           'analyticity_radius_lower': q(R / (28 * g_up(R)))},
        'scaling': {k: q(v) for k, v in ratios.items()},
        'scaling_previews': {k: preview(v) for k, v in ratios.items()},
        'constant_labels': {
            'fwd_head': 'headline q=1/64, exact_first_order, weighted_norm w=e^beta=64, contract-lemma form (source '
                        'loss e^beta charged), multiplies q^(N-1)',
            'fwd_head_sharp': 'same, sharp form (fwd_head/64): exponent from d_inf(e_z, new supports)=N-1 without the '
                              'source loss, or d_inf(e_z, shell)=N with it; labelled refinement',
            'fwd_head_crude': 'headline, crude_majorant, weighted_norm, t_w at most J w G(R)=148/390625; reported, '
                              'not a target',
            'fwd_floor': 'floor q=148/390625, exact_first_order, weighted_norm w=e^beta=390625/148, contract-lemma form',
            'fwd_floor_sharp': 'floor, sharp form (fwd_floor times q_min); labelled; tau ratio exactly 100',
            'fwd_floor_crude': 'floor, crude_majorant, weighted_norm (t_w at most R)',
            'rev_head': 'headline, exact_first_order, analytic_disc rho=64|tau|, sup 2T(rho), Schwarz, n_0=N-1 '
                        '(contract lemma ceil(d/diam))',
            'rev_head_coefwise': 'same with coefficientwise Cauchy (factor 1/(1-q))',
            'rev_head_sharp': 'same with the sharp count n_0=N at e_z (rev_head/64); labelled',
            'rev_head_remainder': 'same with the first-order parts cancelled on supports through u in R (sup '
                                  '2J(rho)(G(T)-16)); labelled refinement',
            'rev_head_crude': 'headline, crude_majorant, analytic_disc, sup 2x28 rho G(R); reported, not a target',
            'rev_floor': 'floor, exact_first_order, analytic_disc rho=tau_star, sup 2T(tau_star), Schwarz, n_0=N-1',
            'rev_floor_sharp': 'floor, sharp count (rev_floor times q_min); labelled; tau ratio exactly 100',
            'rev_floor_crude': 'floor, crude_majorant, analytic_disc, sup 2R=1/32, Schwarz',
            'rev_floor_crude_coefwise': 'floor, crude_majorant, coefficientwise Cauchy 2R/(1-q) (the recorded '
                                        'loop-1 preview form)'},
        'general_volume': {'forward_union': q(union_fwd), 'reverse_union': q(union_rev),
                           'reverse_union_meets_target': union_rev <= k_head},
        'targets': {'headline': [q(q_head), q(k_head)], 'floor': [q(q_floor), q(k_floor)]},
        'admitted_sup_norm_difference_no_decay': q(admitted_sup),
        'gate_fields': dict(gate_fields), 'sentence': sentence,
        'continuum_claim': False, 'scientific_priority_verified': False, 'weak_coupling_claim': False,
        'state_decay_claimed': False, 'untruncated_coefficients_claimed': False,
        'controls': {'implemented': len(ids & done), 'of': len(ids), 'mutations': n_mut},
        'deferred_controls': {},
        'deferred_parts': {
            'reverse_premise_isolation': 'executed on a synthetic inventory derived from the contract; the actual '
                                         'producer inputs/ were listed and hashed outside this program',
            'negation_aware_phrase_scan': 'a mirror of tools/phrase_scan.py (lists and negation frame copied, not '
                                          'imported); the tool itself runs at gate recording',
            'placeholder_span_rejected': 'a mirror of the freezer rule R1 detector, not imported',
            'coherent_evidence_tampering': 'packet-level mutations; producer freeze inventories are checked at '
                                           'post-comparison'},
        'checks': CHECKS,
        'previews': {k: v['preview'] for k, v in constants_out.items()},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('--output must be an absolute path')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('--output must be fresh (absent or empty)')
    result = execute()
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checks': len(result['checks']), 'controls': result['controls'],
                      'K_headline_forward': result['previews']['fwd_head'],
                      'K_headline_reverse': result['previews']['rev_head']}))


if __name__ == '__main__':
    main()
