#!/usr/bin/env python3
"""Round32 AW1 skeptic pre-comparison checker (parity, flip, 1/144, K_2).

Written after the AW1 contract freeze from the frozen contract, the AV1/AV2
gates and the premises named in the skeptic brief, before reading
research/round32/forward/aw1/ or research/round32/reverse/aw1/. Nothing is
imported from any producer or assistant. Standard library only. Every
admission Boolean is decided with fractions.Fraction; floats appear only in the
labelled 'previews' block. Every check and control raises an explicit
exception, so python -O cannot disable it. Model-agent skeptic with correlated
ancestry; not human peer review.

Routes used here (not the producers' contract routes):
  * Haar moments two ways: (i) the SU(2) character algebra chi_{1/2} chi_j =
    chi_{j-1/2}+chi_{j+1/2} in exact integers; (ii) direct integration of
    polynomials in the entries of U=[[a,-b*],[b,a*]] with the uniform-S^3
    moments E|a|^{2p}|b|^{2r}=p!r!/(p+r+1)!, applied to the actual plaquettes.
  * Parity as a Z_2^{links} grading Gamma_e=(-1)^{2j_e} (central translation
    U_e -> -U_e), of which U_E is the product over E.
  * K_2 from the product split psi=psi_out+delta with the exact numerator
    identity omega(W)=[2Re<W Omega_R,xi>+<delta,W delta>]/(|phi_out|^2(1+e^2)).

Usage: python3 -B research/round32/skeptic/aw1_check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / 'research/round32/contracts/aw1.json'
CONTRACT_SHA256 = 'c24bf7eb6a1c24034427c810a9c26c4c86d1f9c1d31b0fe36ea4cf2a796814ef'
AV1_GATE = ROOT / 'research/round32/advisor/av1-gate.json'
AV2_GATE = ROOT / 'research/round32/advisor/av2-gate.json'
I1_REPORT = ROOT / 'research/round21/forward/i1/report.md'
AM2_REPORT = ROOT / 'research/round29/forward/am2/report.md'
AT4_REPORT = ROOT / 'research/round31/forward/at4/report.md'
ERROR_TERMS = ('am2_remainder', 'two_creation', 'straddling', 'density', 'normalization_order',
               'overlap_multiplier', 'arithmetic')


class Rejected(Exception):
    """Raised by a validator that refuses a packet; controls require it."""


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
    """mutations: (label, callable, reason), each must raise Rejected(reason);
    positives: (label, callable), each must be accepted."""
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


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(x):
    return str(x)


def preview(x):
    return format(float(x), '.12e')


def fact(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def sqrt_up(n, scale=10 ** 12):
    r = isqrt(n * scale * scale)
    up = F(r if r * r == n * scale * scale else r + 1, scale)
    if not (up * up >= n and (up - F(1, scale)) ** 2 < n):
        raise CheckFailure('sqrt upper bracket')
    return up


def ceil_to(x, den=10 ** 12):
    up = F(-((-x.numerator * den) // x.denominator), den)
    if up < x:
        raise CheckFailure('ceil')
    return up


def floor_to(x, den=10 ** 12):
    dn = F((x.numerator * den) // x.denominator, den)
    if dn > x:
        raise CheckFailure('floor')
    return dn


# ---------------------------------------------------------------- geometry (I1.1, I1.4)
AXES = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
COORD = {'x': 0, 'y': 1, 'z': 2}
ORIENT = (('xy', 'x', 'y'), ('xz', 'x', 'z'), ('yz', 'y', 'z'))
OFFSET_NAMES = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}
S_STAR = frozenset(OFFSET_NAMES.values())
ORIGIN, EZ = (0, 0, 0), (0, 0, 1)
COVER = frozenset([ORIGIN, EZ])


def add(p, v):
    return tuple(a + b for a, b in zip(p, v))


def sub(p, v):
    return tuple(a - b for a, b in zip(p, v))


def coarse(v):
    return (v[0] // 4, v[1] // 2, v[2])


def tails(b):
    return [(4 * b[0] + r, 2 * b[1] + s, b[2]) for r in range(4) for s in range(2)]


def plaquette_links(p, a, c):
    """Positive links of the face at p in directions a<c (tails p, p+e_a, p+e_c, p)."""
    return ((p, a), (add(p, AXES[a]), c), (add(p, AXES[c]), a), (p, c))


def anchored_faces(b):
    out = []
    for p in tails(b):
        r, s = p[0] - 4 * b[0], p[1] - 2 * b[1]
        for name, a, c in ORIENT:
            links = plaquette_links(p, a, c)
            out.append({'orient': name, 'r': r, 's': s, 'base': p, 'dirs': (a, c), 'anchor': b,
                        'selected': name == 'xy' and s == 0 and r in (0, 1, 2),
                        'links': links, 'owners': frozenset(coarse(v) for v, _ in links)})
    return out


def parse_i1_table(text):
    row = re.compile(r'^\|\s*(xy|xz|yz):\s*r=([0-9,]+);\s*s=([0-9,]+)\s*\|\s*(\d+)\s*\|'
                     r'\s*`\{([^}]*)\}`\s*\|\s*(selected|omitted)\s*\|\s*$')
    classes = {}
    for line in text.splitlines():
        m = row.match(line.strip())
        if not m:
            continue
        rs = [int(x) for x in m.group(2).split(',')]
        ss = [int(x) for x in m.group(3).split(',')]
        if int(m.group(4)) != len(rs) * len(ss):
            raise CheckFailure('I1 table row count mismatch')
        support = frozenset(OFFSET_NAMES[x.strip()] for x in m.group(5).split(','))
        for r in rs:
            for s in ss:
                key = (m.group(1), r, s)
                if key in classes:
                    raise CheckFailure('duplicate I1 class')
                classes[key] = (support, m.group(6))
    return classes


def cube(n):
    rng = range(-n, n + 1)
    return [(x, y, z) for x in rng for y in rng for z in rng]


# ---------------------------------------------------------------- SU(2) character algebra
def times_half(cf):
    """chi_{1/2} * sum c_j chi_j via Clebsch-Gordan; keys are twice the spin."""
    out = {}
    for tj, c in cf.items():
        for nt in (tj - 1, tj + 1):
            if nt >= 0:
                out[nt] = out.get(nt, 0) + c
    return {k: v for k, v in out.items() if v}


def char_moment(n):
    cf = {0: 1}
    for _ in range(n):
        cf = times_half(cf)
    return F(cf.get(0, 0), 2 ** n), cf


def catalan(k):
    return fact(2 * k) // (fact(k + 1) * fact(k))


# ---------------------------------------------------------------- exact Haar integration on S^3
# Entries as (sign, variable); variables 0=a, 1=conj(a), 2=b, 3=conj(b).
U_ENT = (((1, 0), (-1, 3)), ((1, 2), (1, 1)))
UD_ENT = (((1, 1), (1, 3)), ((-1, 2), (1, 0)))
CONJ_VAR = {0: 1, 1: 0, 2: 3, 3: 2}


def _key(d):
    return tuple(sorted(d.items()))


def trace_poly(mats):
    poly = {}
    for idx in product(range(2), repeat=4):
        pairs = [(idx[k], idx[(k + 1) % 4]) for k in range(4)]
        sgn, ex = 1, {}
        for (lk, M), (r, c) in zip(mats, pairs):
            s, v = M[r][c]
            sgn *= s
            e = list(ex.get(lk, (0, 0, 0, 0)))
            e[v] += 1
            ex[lk] = tuple(e)
        key = _key(ex)
        poly[key] = poly.get(key, 0) + F(sgn, 2)
    return {k: v for k, v in poly.items() if v}


def pmul(p, r):
    out = {}
    for k1, v1 in p.items():
        base = dict(k1)
        for k2, v2 in r.items():
            d = dict(base)
            for lk, e in k2:
                o = d.get(lk, (0, 0, 0, 0))
                d[lk] = (o[0] + e[0], o[1] + e[1], o[2] + e[2], o[3] + e[3])
            key = _key(d)
            out[key] = out.get(key, 0) + v1 * v2
    return {k: v for k, v in out.items() if v}


def haar(p):
    tot = F(0)
    for k, v in p.items():
        val = F(1)
        for _, (pa, pab, pb, pbb) in k:
            if pa != pab or pb != pbb:
                val = F(0)
                break
            val *= F(fact(pa) * fact(pb), fact(pa + pb + 1))
        tot += v * val
    return tot


def wilson_poly(links):
    l1, l2, l3, l4 = links  # (p,a), (p+e_a,c), (p+e_c,a), (p,c)
    return trace_poly([(l1, U_ENT), (l2, U_ENT), (l3, UD_ENT), (l4, UD_ENT)])


def entry_poly(link, r, c, conj=False):
    s, v = U_ENT[r][c]
    if conj:
        v = CONJ_VAR[v]
    e = [0, 0, 0, 0]
    e[v] = 1
    return {((link, tuple(e)),): F(s)}


# ---------------------------------------------------------------- one-plaquette fixture (finite graph, labelled)
def plaquette_series(coef, order=4, nmax=8):
    """Gauge-invariant sector of ONE plaquette (class functions of the holonomy),
    G = 4C + coef*W, W chi_j=(chi_{j-1/2}+chi_{j+1/2})/2; exact Rayleigh-Schroedinger.
    Returns the Taylor coefficients of <W> and of the ground energy in the coupling
    (coef is the per-unit-coupling coefficient). Truncation nmax=8 is exact to order 4."""
    n = nmax + 1
    e0 = [F(k * (k + 2)) for k in range(n)]  # 4*j(j+1), 2j=k

    def wm(v):
        out = [F(0)] * n
        for k in range(n):
            if v[k]:
                if k + 1 < n:
                    out[k + 1] += v[k] / 2
                if k >= 1:
                    out[k - 1] += v[k] / 2
        return out

    def vm(v):
        return [coef * x for x in wm(v)]

    psi, en = [[F(1)] + [F(0)] * (n - 1)], [F(0)]
    for k in range(1, order + 1):
        en.append(vm(psi[k - 1])[0])
        rhs = [-x for x in vm(psi[k - 1])]
        for m in range(1, k + 1):
            rhs = [r + en[m] * p for r, p in zip(rhs, psi[k - m])]
        psi.append([F(0)] + [rhs[i] / (e0[i] - e0[0]) for i in range(1, n)])

    def ip(u, v):
        return sum((a * b for a, b in zip(u, v)), F(0))
    num = [sum((ip(psi[i], wm(psi[k - i])) for i in range(k + 1)), F(0)) for k in range(order + 1)]
    den = [sum((ip(psi[i], psi[k - i]) for i in range(k + 1)), F(0)) for k in range(order + 1)]
    out = []
    for k in range(order + 1):
        out.append((num[k] - sum((out[i] * den[k - i] for i in range(k)), F(0))) / den[0])
    return out, en


# ---------------------------------------------------------------- K_2 (exact tier and crude tier)
G_R_UP = F(148, 7)       # G(R) < 148/7 (AM2.9)
GP_R_UP = F(352)         # G'(R) < 352 (AM2.9)


def t_of(tier, tau_abs):
    J = 28 * tau_abs
    if tier == 'exact':
        t1 = F(49, 144) * tau_abs
        return t1 / (1 - GP_R_UP * J)
    if tier == 'crude':
        return J * G_R_UP
    raise Rejected('unknown tier')


def k2_terms(tier, tau_abs, multiplier=F(1), multiplier_label='exact'):
    J = 28 * tau_abs
    t = t_of(tier, tau_abs)
    eps = 2 * t + t * t
    terms = {
        'am2_remainder': {'value': GP_R_UP * J * t, 'tier': tier, 'order': 2,
                          'form': '||c-c^(1)||_a <= J(G(t)-16) <= 352 J t'},
        'two_creation': {'value': t * t, 'tier': tier, 'order': 2,
                         'form': 'sum over disjoint pairs I ni 0, J ni e_z: <= t^2 (conservative)'},
        'straddling': {'value': t * t, 'tier': tier, 'order': 2,
                       'form': 'I strictly containing R, paired with outside excitation: <= t * t'},
        'density': {'value': eps * eps, 'tier': tier, 'order': 2,
                    'form': '|<delta,W delta>|/|phi_out|^2 <= e^2 <= eps^2, eps=2t+t^2'},
        'normalization_order': {'value': tau_abs / 144 * eps * eps, 'tier': tier, 'order': 3,
                                'form': '(|tau|/144) e^2/(1+e^2): third order'},
        'overlap_multiplier': {'value': multiplier, 'tier': tier, 'order': 0, 'label': multiplier_label,
                               'form': '2 Re x ||W Omega_R|| = 2 x 1/2 = 1'},
        'arithmetic': {'value': F(0), 'tier': tier, 'order': 0, 'not_applicable':
                       'every term is an exact rational; no rounding enters the admission path'},
    }
    return terms, t, eps


def k2_bound(terms):
    m = terms['overlap_multiplier']['value']
    return m * (terms['am2_remainder']['value'] + terms['straddling']['value'] + terms['two_creation']['value']) \
        + terms['density']['value'] + terms['normalization_order']['value']


def validate_k2_packet(p, cap):
    if p.get('combination') != 'linear':
        raise Rejected('root-N or non-linear combination of error terms')
    terms = p['terms']
    for name in ERROR_TERMS:
        if name not in terms:
            raise Rejected('error term missing: ' + name)
    tier = p['tier']
    for name, row in terms.items():
        if not isinstance(row['value'], F):
            raise Rejected('exact arithmetic: ' + name)
        if row['tier'] != tier:
            raise Rejected('tier mixing: ' + name)
        if row['value'] == 0 and 'not_applicable' not in row:
            raise Rejected('term set to zero without reason: ' + name)
    truth, _, _ = k2_terms(tier, cap)
    for name in ('am2_remainder', 'two_creation', 'straddling', 'density', 'normalization_order'):
        if terms[name]['value'] < truth[name]['value']:
            raise Rejected('tier mixing or undercount: ' + name)
    m = terms['overlap_multiplier']
    if m['value'] != 1 and not (m['value'] > 1 and m.get('label') == 'conservative'):
        raise Rejected('overlap multiplier')
    if p['K2'] * cap * cap < k2_bound(terms):
        raise Rejected('K_2 below its itemized sum')
    if p.get('overlap_components', ['c_R']) != ['c_R']:
        raise Rejected('overlap multiplier: only c_R overlaps W Omega_R')
    return True


def aw2_rule(K2, grid_max=40):
    for k in range(8, grid_max + 1):
        tau = F(1, 10 ** k)
        if K2 * tau <= F(1, 288):
            return tau
    raise CheckFailure('no grid element satisfies the rule')


def validate_aw2(K2_tier, K2, chosen):
    if K2_tier != 'exact':
        raise Rejected('coupling rule requires the exact-tier K_2')
    if chosen != aw2_rule(K2):
        raise Rejected('coupling rule: tau_AW2 is fixed by the frozen decade grid')
    return True


# ---------------------------------------------------------------- validators for claims and packets
def validate_first_order(p, truth):
    if p['wilson_face_in_omitted_set'] is not True:
        raise Rejected('Wilson face excluded from the omitted set')
    if p['contributing_faces'] != ['W']:
        raise Rejected('wrong face: only f=W contributes at first order')
    if p['coefficient'] != truth:
        raise Rejected('first-order coefficient differs from +1/144 under I1.5')
    return True


def validate_signed(value_plus, value_minus, cap):
    if value_plus != cap / 144 or value_minus != -cap / 144:
        raise Rejected('sign flip: omega_{-tau}(W) must be -omega_tau(W) at first order')
    return True


def validate_sign_fixture(coeffs):
    if coeffs[1] <= 0:
        raise Rejected('sign convention: sign(<W>) must equal sign(tau) under I1.5')
    return True


def validate_parity_claims(p):
    for key in ('E[W^3]', 'E[W^2 W_f] all f incl W', 'first_order_C', 'first_order_W2', 'energy_first_order'):
        if p[key] != 0:
            raise Rejected('parity: nonzero first-order term claimed for ' + key)
    if p['E[W^2]'] != F(1, 4) or p['E[W^4]'] != F(1, 8):
        raise Rejected('parity: Haar moments E[W^2]=1/4, E[W^4]=1/8')
    return True


def validate_multiplet(scope, element):
    if scope == 'full_energy_24_eigenspace' and element != 0:
        raise Rejected('degenerate multiplet: zero splitting holds only on the gauge-invariant multiplet')
    if scope == 'gauge_invariant_multiplet' and element != 0:
        raise Rejected('degenerate multiplet: invariant splitting must be zero')
    return True


def validate_flip_claim(flipped, claimed_out):
    """flipped: U_E H U_E^* computed coefficientwise; claimed_out: the Hamiltonian a packet asserts."""
    if flipped != claimed_out:
        raise Rejected('flip maps kappa to -kappa; tau-antisymmetry needs kappa=0')
    return True


def validate_fixture_antisymmetry(v_plus, v_minus):
    if v_minus != -v_plus:
        raise Rejected('flip maps kappa to -kappa: fixture value is not antisymmetric')
    return True


def validate_flip_set(counts):
    if counts.get('even', 0) != 0:
        raise Rejected('odd intersection fails: some plaquette meets E evenly')
    return True


def validate_third_order(claim):
    if claim.get('remainder_order', 2) >= 3 and not claim.get('separate_proof'):
        raise Rejected('third order from oddness alone')
    return True


def validate_static(label):
    if label != 'static_equal_time_mean':
        raise Rejected('static effect relabelled as dynamical')
    return True


def validate_evidence(ev, required):
    for cid in required:
        if ev.get(cid) is not True:
            raise Rejected('required control not passed: ' + cid)
    if ev.get('contract_sha256') != CONTRACT_SHA256:
        raise Rejected('contract hash')
    return True


def validate_model(p, cap):
    if p['tau_abs'] != cap or p['triple'] != ('0', '0', '0') or p['model_id'] != 'AQ_patterned_zero_selected' \
            or p.get('finite_graph', False):
        raise Rejected('model changed and relabelled')
    return True


def validate_claims(flags):
    for key in ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift',
                'scientific_priority_verified', 'third_order_remainder_claim'):
        if flags.get(key) is not False:
            raise Rejected('forbidden claim ' + key)
    return True


def validate_scaling(kind, ratio):
    brackets = {'linear': (F(99), F(101)), 'quadratic': (F(9900), F(10100))}
    lo, hi = brackets[kind]
    if not (lo <= ratio <= hi):
        raise Rejected('tau scaling exponent')
    return True


def validate_mean(m1):
    if m1 == 0:
        raise Rejected('first-order mean not charged')
    return True


def validate_centering(kind, m, d, residue):
    truth = {'vector': d * d, 'scalar': -2 * m * d - d * d}[kind]
    if residue != truth:
        raise Rejected('centering residue')
    return True


def validate_amplitude(amp_norm, amp_alpha):
    if amp_norm != amp_alpha or amp_norm != F(1, 72):
        raise Rejected('clock or unit mixing')
    return True


def validate_free_exponent(exponent):
    if exponent != 3:
        raise Rejected('clock: free exponent is 3 in alpha units')
    return True


def validate_geometry(anchors, cover_links, endpoints, truth):
    if anchors != truth[0]:
        raise Rejected('incident stars')
    if (cover_links, endpoints) != truth[1:]:
        raise Rejected('cover')
    return True


def validate_inventory(inv, contract):
    allowed = sorted(set(['AGENTS.md', 'research/round32/contracts/aw1.json'] + contract['shared_premises']))
    if sorted(inv) != allowed:
        raise Rejected('forbidden input in reverse inventory')
    return True


def validate_retained(tier, margin, verdict):
    if margin < 2 and verdict != 'limited_retained':
        raise Rejected('insufficient tier relabelled as passing')
    return True


def validate_evidence_role(source):
    if source in ('minus_tau_replay', 'av2_interval'):
        raise Rejected('not evidence: ' + source)
    return True


def validate_face_separation(p):
    if 'W' not in p['omitted_at_anchor_0']:
        raise Rejected('Wilson face excluded from the omitted set')
    if len(p['omitted_at_anchor_0']) != 21 or p['others_at_anchor_0'] != 20:
        raise Rejected('Wilson face merged with the 20 other anchored faces')
    if p['first_order_faces'] != ['W']:
        raise Rejected('Wilson face merged with the 20 other anchored faces')
    return True


# ---------------------------------------------------------------- main computation
def execute():
    contract_bytes = CONTRACT.read_bytes()
    need(hashlib.sha256(contract_bytes).hexdigest() == CONTRACT_SHA256, 'contract_sha256_bound')
    contract = json.loads(contract_bytes)
    need(contract['id'] == 'AW1' and contract['status'] == 'frozen_before_production', 'contract_frozen_identity')
    cap = F(contract['parameters']['tau_cap'])
    target = F(contract['preregistration']['target']['value'])
    triple = tuple(contract['parameters']['selected_coefficients_over_alpha'])
    need(cap == F(1, 10 ** 8) and target == F(1, 288) and triple == ('0', '0', '0')
         and contract['preregistration']['target']['comparator'] == '<='
         and '1/288' in contract['parameters']['aw2_coupling_rule']
         and 'decade grid' in contract['parameters']['aw2_coupling_rule'],
         'contract_cap_target_rule_read', tau_cap=q(cap), target=q(target))
    need(len(contract['controls']) == 30 and contract['controls'] == contract['preregistration']['controls_required']['ids'],
         'contract_controls_equal_prereg_ids', n='30')
    need(sorted(contract['preregistration']['error_terms_itemized']) == sorted(ERROR_TERMS),
         'contract_error_terms_read')
    gate_bytes = AV1_GATE.read_bytes()
    gate = json.loads(gate_bytes)
    mD = re.search(r'D_ii=(\d+)/(\d+)', gate['accepted'])
    D_ii = F(int(mD.group(1)), int(mD.group(2)))
    need(gate['verdict'] == 'accepted_within_scope', 'av1_gate_read', D_ii=q(D_ii))

    # ---------------- I1 classes, counts and the Wilson face
    table = parse_i1_table(I1_REPORT.read_text())
    geo = {(f['orient'], f['r'], f['s']): (frozenset(sub(o, ORIGIN) for o in f['owners']),
                                          'selected' if f['selected'] else 'omitted')
           for f in anchored_faces(ORIGIN)}
    need(len(table) == 24 and table == geo, 'i1_table_equals_geometry', classes='24')
    omitted = sorted(((k, v[0]) for k, v in table.items() if v[1] == 'omitted'), key=lambda kv: kv[0])
    need(len(omitted) == 21 and all(len(s) >= 2 for _, s in omitted), 'i1_21_omitted_all_multi_site',
         note='no omitted face has single-factor support, so c^(1)_{0}=c^(1)_{e_z}=0')
    per_factor = sum(len(s) for _, s in omitted)
    owner_sets = {}
    for _, s in omitted:
        for o in s:
            key = frozenset(sub(x, o) for x in s)
            owner_sets[key] = owner_sets.get(key, 0) + 1
    mults = sorted(owner_sets.values())
    cand = re.search(r'(\d+) owner sets with multiplicities \{([^}]*)\}, (\d+) faces meeting R, (\d+) touching both',
                     ' '.join(contract['required']))
    if cand is None:
        raise CheckFailure('contract counts not found')
    c15, cm, c82, c16 = int(cand.group(1)), cand.group(2), int(cand.group(3)), int(cand.group(4))
    cmults = sorted(int(a) for a, b in (x.split('x') for x in cm.split(',')) for _ in range(int(b)))
    need(per_factor == 49 and len(owner_sets) == c15 and mults == cmults, 'derived_49_faces_15_owner_sets',
         multiplicities=[str(x) for x in mults])

    # actual faces (anchored, omitted) meeting R, over anchors in a cube that contains R-S
    faces_R = []
    for b in cube(2):
        for f in anchored_faces(b):
            if not f['selected'] and f['owners'] & COVER:
                faces_R.append(f)
    inside = [f for f in faces_R if f['owners'] <= COVER]
    contain = [f for f in faces_R if COVER <= f['owners']]
    strictly = [f for f in contain if f['owners'] != COVER]
    one_site = [f for f in faces_R if len(f['owners'] & COVER) == 1]
    need(len(faces_R) == c82 == 82 and len(contain) == c16 == 16 and len(inside) == 10
         and len(faces_R) - len(inside) == 72 and len(strictly) == 6 and len(one_site) == 66,
         'derived_82_10_16_72_6_66', meeting='82', inside='10', containing='16', straddling='72',
         strictly_containing_R='6', meeting_one_site_of_R='66')
    W_links = plaquette_links(ORIGIN, 'x', 'z')
    wil = [f for f in faces_R if f['links'] == W_links]
    need(len(wil) == 1 and wil[0]['anchor'] == ORIGIN and (wil[0]['orient'], wil[0]['r'], wil[0]['s']) == ('xz', 0, 0)
         and wil[0]['owners'] == COVER and wil[0] in inside, 'wilson_face_is_omitted_class_xz_r0_s0_at_anchor_0')
    at0 = [f for f in anchored_faces(ORIGIN) if not f['selected']]
    need(len(at0) == 21 and sum(1 for f in at0 if f['links'] == W_links) == 1
         and sum(1 for f in inside if f['links'] != W_links) == 9, 'wilson_face_separated_from_20_others',
         others_at_anchor_0='20', others_with_owner_set_R='9')
    anchors = sorted({sub(r, o) for r in COVER for o in S_STAR})
    cover_links = [(p, d) for b in COVER for p in tails(b) for d in 'xyz']
    endpoints = {v for p, d in cover_links for v in (p, add(p, AXES[d]))}
    geom_truth = (len(anchors), len(cover_links), len(endpoints))
    need(geom_truth == (7, 48, 36), 'cover_48_links_36_endpoints_7_anchors')

    # ---------------- (a) Haar moments: character algebra
    moments = {}
    for n in range(1, 9):
        val, cf = char_moment(n)
        moments[n] = val
        if n % 2 == 1 and val != 0:
            raise CheckFailure('odd moment')
        if n % 2 == 0 and val != F(catalan(n // 2), 2 ** n):
            raise CheckFailure('Catalan moment')
    w2_class = {k: F(v, 4) for k, v in char_moment(2)[1].items()}
    need(moments[1] == 0 and moments[2] == F(1, 4) and moments[3] == 0 and moments[4] == F(1, 8),
         'character_moments_exact', moments={str(n): q(v) for n, v in moments.items()},
         W2_decomposition='W^2=(chi_0+chi_1)/4 as a class function of the holonomy')
    need(w2_class == {0: F(1, 4), 2: F(1, 4)}, 'W_squared_character_decomposition')

    # ---------------- (a) Haar moments: direct S^3 integration on the actual plaquettes
    Wp = wilson_poly(W_links)
    W2p = pmul(Wp, Wp)
    W3p = pmul(W2p, Wp)
    W4p = pmul(W3p, Wp)
    sph = {1: haar(Wp), 2: haar(W2p), 3: haar(W3p), 4: haar(W4p)}
    need(all(sph[n] == moments[n] for n in (1, 2, 3, 4)), 'sphere_integration_equals_character_moments',
         values={str(n): q(v) for n, v in sph.items()},
         cross_check='free z link (0,z): the holonomy is Haar distributed (AQ2 section 5), so single-loop moments are character moments')
    ww, w2w, wf1 = {}, {}, {}
    for f in faces_R:
        fp = wilson_poly(f['links'])
        name = '%s:%s:%s' % (f['orient'], ','.join(map(str, f['base'])), ','.join(map(str, f['anchor'])))
        ww[name] = haar(pmul(Wp, fp))
        w2w[name] = haar(pmul(W2p, fp))
        wf1[name] = haar(fp)
    wname = 'xz:0,0,0:0,0,0'
    need(ww[wname] == F(1, 4) and all(v == 0 for k, v in ww.items() if k != wname), 'E_W_Wf_only_f_equals_W',
         faces='82', nonzero=[wname])
    need(all(v == 0 for v in w2w.values()) and w2w[wname] == 0, 'E_W2_Wf_zero_all_82_including_W', faces='82')
    need(all(v == 0 for v in wf1.values()), 'E_Wf_zero_energy_term', faces='82')
    # odd-multiplicity links, per term
    odd_report = {}
    for f in faces_R:
        mult = {}
        for lk in list(W_links) * 2 + list(f['links']):
            mult[lk] = mult.get(lk, 0) + 1
        odd = sorted(lk for lk, m in mult.items() if m % 2 == 1)
        if not odd:
            raise CheckFailure('even content')
        if f['links'] == W_links:
            if not (odd == sorted(W_links) and all(mult[lk] == 3 for lk in W_links)):
                raise CheckFailure('W case multiplicity')
        else:
            outside = [lk for lk in f['links'] if lk not in W_links]
            if not (odd == sorted(f['links']) and len(outside) >= 3 and all(mult[lk] == 1 for lk in outside)
                    and all(mult[lk] == 3 for lk in f['links'] if lk in W_links)):
                raise CheckFailure('f != W case multiplicity')
    shared = sorted(len(set(f['links']) & set(W_links)) for f in faces_R if f['links'] != W_links)
    need(max(shared) == 1, 'odd_link_identified_every_term', rule='f=W: all four W links carry multiplicity 3; '
         'f!=W: every link of f outside W (at least 3) carries multiplicity 1, a shared link (at most one) 3',
         max_shared_links='1', faces_sharing_one_link=str(sum(1 for x in shared if x == 1)))

    # ---------------- (a) multiplet: 4-cycles are plaquettes; invariant splitting zero; full-space counterexample
    verts = cube(1)
    vset = set(verts)
    adj = {v: [] for v in verts}
    for v in verts:
        for d in 'xyz':
            w = add(v, AXES[d])
            if w in vset:
                adj[v].append((w, (v, d)))
                adj[w].append((v, (v, d)))
    cycles = set()
    for v0 in verts:
        for v1, e1 in adj[v0]:
            for v2, e2 in adj[v1]:
                if v2 == v0:
                    continue
                for v3, e3 in adj[v2]:
                    if v3 in (v0, v1):
                        continue
                    for v4, e4 in adj[v3]:
                        if v4 == v0:
                            cycles.add(frozenset([e1, e2, e3, e4]))
    plaqs = set()
    for p in verts:
        for _, a, c in ORIENT:
            ls = plaquette_links(p, a, c)
            if all(add(lk[0], AXES[lk[1]]) in vset and lk[0] in vset for lk in ls):
                plaqs.add(frozenset(ls))
    need(cycles == plaqs and len(plaqs) == 36, 'four_cycles_are_plaquettes', n=str(len(plaqs)),
         note='even-degree 4-edge subgraphs of Z^3 are single 4-cycles (girth 4), i.e. plaquettes')
    faceset = [frozenset(f['links']) for f in faces_R] + [frozenset(plaquette_links(p, a, c)) for p in cube(1)
                                                          for _, a, c in ORIENT]
    faceset = sorted(set(faceset), key=lambda s: sorted(s))
    sizes = set()
    for i, g in enumerate(faceset):
        for h in faceset[i:]:
            sizes.add(len(g ^ h))
    need(sizes == {0, 6, 8}, 'invariant_multiplet_splitting_zero_by_grading', symmetric_difference_sizes=sorted(sizes),
         faces=str(len(faceset)), note='<W_g Omega,W_f W_h Omega>=0 needs d(g)+d(h)=d(f) of size 4: impossible')
    neighbours = []
    for lk in W_links:
        for p in cube(1):
            for _, a, c in ORIENT:
                ls = plaquette_links(p, a, c)
                if lk in ls and ls != W_links and ls not in neighbours:
                    neighbours.append(ls)
    tri, fact_tri = 0, 0
    for h in neighbours:
        wh = pmul(Wp, wilson_poly(h))
        touched = set(W_links) | set(h)
        for f in faces_R:
            if not (set(f['links']) & touched):
                # disjoint link sets factorize under the product Haar measure; E[W_f]=0 was integrated above
                if wf1['%s:%s:%s' % (f['orient'], ','.join(map(str, f['base'])), ','.join(map(str, f['anchor'])))] != 0:
                    raise CheckFailure('factorized multiplet element')
                fact_tri += 1
                continue
            if haar(pmul(wh, wilson_poly(f['links']))) != 0:
                raise CheckFailure('invariant multiplet element nonzero')
            tri += 1
    need(len(neighbours) == 12 and tri + fact_tri == 12 * 82, 'invariant_multiplet_sample_integrated',
         integrated=str(tri), factorized=str(fact_tri),
         note='<W Omega, W_f W_h Omega> for the 12 plaquettes h sharing a link with W and all 82 f meeting R')
    L5, L6 = ((5, 5, 5), 'x'), ((7, 7, 7), 'y')
    l1, l2, l3, l4 = W_links
    phi = pmul(pmul(entry_poly(l1, 0, 0), entry_poly(l2, 0, 0)), pmul(entry_poly(L5, 0, 0), entry_poly(L6, 0, 0)))
    phip_c = pmul(pmul(entry_poly(l3, 0, 0, True), entry_poly(l4, 0, 0, True)),
                  pmul(entry_poly(L5, 0, 0, True), entry_poly(L6, 0, 0, True)))
    full_elem = haar(pmul(pmul(phip_c, Wp), phi))
    full_norm = haar(pmul(pmul(entry_poly(l1, 0, 0, True), entry_poly(l1, 0, 0)),
                          pmul(entry_poly(l2, 0, 0, True), entry_poly(l2, 0, 0)))) * F(1, 4)
    need(full_elem == F(1, 128) and full_norm == F(1, 16), 'full_eigenspace_splitting_nonzero_counterexample',
         element=q(full_elem), norm_squared=q(full_norm),
         note='non-invariant energy-24 vectors U1_00 U2_00 U5_00 U6_00 and U3_00 U4_00 U5_00 U6_00: '
              'normalized <phi\',W phi>=1/8; gauge invariance is essential')

    # ---------------- (a) first-order terms of C(s), omega(W^2) and the energy
    amp = F(1, 72)                      # psi = Omega_0 + (tau/72) sum_f W_f Omega_0 + O(tau^2)
    state_C = 2 * amp * sum(w2w.values())           # x e^{-3s}
    duhamel_C = F(1, 24) * sum(w2w.values())        # x s e^{-3s}
    energy_1 = -F(1, 24) * sum(wf1.values())
    state_W2 = 2 * amp * sum(w2w.values())
    need(state_C == 0 and duhamel_C == 0 and energy_1 == 0 and state_W2 == 0, 'first_order_C_and_W2_vanish',
         state=q(state_C), duhamel=q(duhamel_C), energy=q(energy_1), mean_square='2 m0 m1 = 0 since m0 = 0',
         scope='finite-volume Taylor coefficient; uniform O(tau^2) constant for C(s) explicitly unbounded here')

    # ---------------- (b) flip set E and the flip lemma
    rules = re.findall(r'\(p,([xyz])\): p_([xyz]) even', contract['parameters']['flip_set'])
    rule = dict(rules)
    need(sorted(rule) == ['x', 'y', 'z'] and rule == {'x': 'y', 'y': 'z', 'z': 'x'}, 'flip_set_parsed_from_contract',
         rule={k: 'p_%s even' % v for k, v in sorted(rule.items())})

    def in_E(link, rl=rule, removed=()):
        if link in removed:
            return False
        p, d = link
        return p[COORD[rl[d]]] % 2 == 0

    def flip_counts(faces, **kw):
        c = {'odd1': 0, 'odd3': 0, 'even': 0}
        for ls in faces:
            n = sum(1 for lk in ls if in_E(lk, **kw))
            c['odd1' if n == 1 else 'odd3' if n == 3 else 'even'] += 1
        return c
    period = [plaquette_links(p, a, c) for p in product(range(2), repeat=3) for _, a, c in ORIENT]
    per_orient = {}
    for name, a, c in ORIENT:
        per_orient[name] = flip_counts([plaquette_links(p, a, c) for p in product(range(2), repeat=3)])
    all_box = [f['links'] for b in cube(2) for f in anchored_faces(b)]
    factor_faces = {}
    for u in ((0, 0, 0), (0, 0, 1), (1, 1, 0), (-1, 0, 1)):
        fs = [f['links'] for b in cube(3) for f in anchored_faces(b) if not f['selected'] and u in f['owners']]
        factor_faces[u] = (len(fs), flip_counts(fs))
    c_period, c_box, c_R = flip_counts(period), flip_counts(all_box), flip_counts([f['links'] for f in faces_R])
    need(validate_flip_set(c_period) and validate_flip_set(c_box) and validate_flip_set(c_R)
         and all(n == 49 and validate_flip_set(c) for n, c in factor_faces.values())
         and all(validate_flip_set(c) for c in per_orient.values()),
         'flip_set_odd_intersection_full_enumeration',
         period_cell={k: str(v) for k, v in c_period.items()},
         per_orientation={o: {k: str(v) for k, v in c.items()} for o, c in per_orient.items()},
         anchored_classes_all_24_on_cube2={k: str(v) for k, v in c_box.items()},
         faces_meeting_R={k: str(v) for k, v in c_R.items()},
         faces_per_factor={','.join(map(str, u)): {'n': str(n), 'odd1': str(c['odd1']), 'odd3': str(c['odd3'])}
                           for u, (n, c) in sorted(factor_faces.items())},
         note='membership depends only on coordinate parities; the 8x3 period cell is exhaustive; coarse e_z '
              'shifts fine z by 1, so both z-parities of the factor are enumerated')
    need(all(sum(1 for lk in f['links'] if in_E(lk)) % 2 == 1 for b in cube(2) for f in anchored_faces(b)
             if f['selected']), 'selected_faces_flip_too', note='U_E maps the selected triple kappa to -kappa')

    def flip_poly(poly):
        # (U_E psi)(U)=psi(U'), U'_e=-U_e on E: every entry of a flipped link changes sign
        out = {}
        for k, v in poly.items():
            deg = sum(sum(e) for lk, e in k if in_E(lk))
            out[k] = v * (-1) ** deg
        return out
    op_faces = [f['links'] for f in faces_R] + [f['links'] for b in (ORIGIN, EZ) for f in anchored_faces(b)]
    need(all(flip_poly(wilson_poly(ls)) == {k: -v for k, v in wilson_poly(ls).items()} for ls in op_faces)
         and flip_poly(W2p) == W2p, 'operator_level_UE_Wf_UE_equals_minus_Wf',
         faces=str(len(op_faces)), note='central flip applied to the entry polynomials; W^2 is invariant')
    cell = list(product(range(2), repeat=3))
    period_links = sorted({lk for ls in period for lk in ls})
    E_cell = frozenset(lk for lk in period_links if in_E(lk))
    cob_even, cob_equal = True, False
    for mask in range(256):
        S = {v for i, v in enumerate(cell) if mask >> i & 1}

        def inS(v):
            return (v[0] % 2, v[1] % 2, v[2] % 2) in S
        dS = frozenset(lk for lk in period_links if inS(lk[0]) != inS(add(lk[0], AXES[lk[1]])))
        if any(len(set(ls) & dS) % 2 for ls in period):
            cob_even = False
        if dS == E_cell:
            cob_equal = True
    need(cob_even and not cob_equal, 'E_not_a_coboundary', periodic_vertex_sets='256',
         reason='every Z_2 coboundary meets every plaquette evenly; E meets every plaquette oddly, so U_E is '
                'not a gauge transformation and flips gauge-invariant observables')

    # coefficient-level flip on the actual factor geometry
    def coeffs(tau_c, kappa):
        out = {}
        for f in anchored_faces(ORIGIN):
            if f['selected']:
                out[('selected', f['r'])] = -kappa[f['r']]
            else:
                out[('omitted', f['orient'], f['r'], f['s'])] = -tau_c / 3
        return out

    def flip_coeffs(cf):
        out = {}
        for f in anchored_faces(ORIGIN):
            key = ('selected', f['r']) if f['selected'] else ('omitted', f['orient'], f['r'], f['s'])
            n = sum(1 for lk in f['links'] if in_E(lk))
            out[key] = cf[key] * (-1) ** n
        return out
    kap = {0: F(1, 5), 1: F(-1, 10), 2: F(1, 7)}
    kap_neg = {k: -v for k, v in kap.items()}
    zero = {0: F(0), 1: F(0), 2: F(0)}
    h_in = coeffs(cap, kap)
    need(flip_coeffs(h_in) == coeffs(-cap, kap_neg) and flip_coeffs(h_in) != coeffs(-cap, kap)
         and flip_coeffs(coeffs(cap, zero)) == coeffs(-cap, zero), 'flip_maps_tau_kappa_to_minus_tau_minus_kappa',
         kappa_fixture={str(k): q(v) for k, v in kap.items()})

    # one-plaquette fixture (finite graph; labelled), sign convention and oddness
    ser_p, en_p = plaquette_series(F(-1, 24))
    ser_m, _ = plaquette_series(F(1, 24))
    need(ser_p == [0, F(1, 144), 0, F(-5, 11943936), 0] and ser_m == [(-1) ** k * c for k, c in enumerate(ser_p)]
         and en_p[1] == 0, 'one_plaquette_fixture_series',
         W_series=[q(c) for c in ser_p], energy_series=[q(c) for c in en_p], model='FG(one plaquette, class '
         'functions of the holonomy, G=4C-(tau/24)W); model_is_finite_graph:true, transfers_to_aq:false')
    kfix = plaquette_series(F(-1, 24))[0][1]
    fixture_sel = {'+tau,+kappa': kfix * F(1, 5), '-tau,+kappa': kfix * F(1, 5), '-tau,-kappa': -kfix * F(1, 5)}
    need(fixture_sel['-tau,+kappa'] != -fixture_sel['+tau,+kappa']
         and fixture_sel['-tau,-kappa'] == -fixture_sel['+tau,+kappa'], 'nonzero_kappa_two_plaquette_fixture',
         first_order_W_sel={k: q(v) for k, v in fixture_sel.items()},
         model='two disjoint plaquettes (selected with coefficient kappa=1/5, omitted with tau); finite graph, labelled')

    # ---------------- (c) first-order coefficient and sign chain under I1.5
    amp_norm = (F(1, 3)) / 24     # (tau/3) / 24 in delta units
    amp_alpha = (F(1, 24)) / 3    # (tau/24) / 3 in alpha units
    c1_R_overlap = -amp * ww[wname]                 # <W Omega_R, c^(1)_R>/tau with c^(1) = -(tau/72) sum W_f Omega
    coef = -2 * c1_R_overlap                        # omega(W) = -2 Re <W Omega_0, c^(1)> + O(tau^2)
    literal = 2 * c1_R_overlap                      # contract item 3 formula read literally with AM2's c^(1)
    need(amp_norm == amp_alpha == amp and coef == F(1, 144) and literal == -F(1, 144),
         'first_order_coefficient_plus_1_over_144', coefficient=q(coef),
         sign_chain='I1: +nu(1-W_f), nu=alpha tau/24; I1.5: V=-(tau/3)sum W_f (delta units); '
                    'c^(1)=H_0^{-1}P V Omega_0=-(tau/72)sum W_f Omega_0; psi=e^{-C}Omega_0=Omega_0-c^(1)+...; '
                    'omega(W)=-2Re<W Omega_0,c^(1)>=(tau/36)E[W^2]=+tau/144',
         contract_item3_literal='2<W Omega_0,c^(1)> with the AV1-admitted c^(1) gives -tau/144 (sign ambiguity)')
    need(validate_signed(coef * cap, coef * (-cap), cap), 'signed_first_order_both_signs',
         plus=q(coef * cap), minus=q(-coef * cap))
    need(D_ii >= cap / 144, 'av1_bound_compatible_with_first_order',
         ratio_D_over_first_order=q(floor_to(D_ii / (cap / 144), 10 ** 6)))

    # ---------------- (d) K_2 per tier
    tiers = {}
    for tier in ('exact', 'crude'):
        terms, t, eps = k2_terms(tier, cap)
        bound = k2_bound(terms)
        K2 = bound / (cap * cap)
        packet = {'tier': tier, 'terms': terms, 'combination': 'linear', 'K2': K2, 'overlap_components': ['c_R']}
        validate_k2_packet(packet, cap)
        small, _, _ = k2_terms(tier, cap / 100)
        ratios = {n: (terms[n]['value'] / small[n]['value']) for n in ('am2_remainder', 'two_creation', 'straddling', 'density')}
        for n, r in ratios.items():
            validate_scaling('quadratic', r)
        margin = F(1) / (144 * K2 * cap)
        tiers[tier] = {'t': t, 'eps': eps, 'terms': terms, 'K2': K2, 'margin': margin, 'ratios': ratios,
                       'bound_at_cap': bound}
    Kx, Kc = tiers['exact']['K2'], tiers['crude']['K2']
    need(F(3354) < Kx < F(3355) and tiers['exact']['margin'] >= 2, 'K2_exact_tier_itemized',
         K2=q(Kx), K2_upper_ceil_1e12=q(ceil_to(Kx)), margin_lower_1e9grid=q(floor_to(tiers['exact']['margin'], 10 ** 9)))
    need(F(7937544) < Kc < F(7937545) and tiers['crude']['margin'] < 2, 'K2_crude_tier_itemized_fails_margin',
         K2=q(Kc), K2_upper_ceil_1e12=q(ceil_to(Kc)), margin_upper_1e9grid=q(ceil_to(tiers['crude']['margin'], 10 ** 9)))
    need(all(validate_scaling('quadratic', r) for t_ in tiers.values() for r in t_['ratios'].values()),
         'each_K2_term_scales_quadratically')

    # labelled refinements at the exact tier (not the admitted headline)
    J = 28 * cap
    T = tiers['exact']['t']
    rho = GP_R_UP * J * T
    ref = {
        'am2_remainder_288_form': 288 * J * T / (1 - 8 * T),
        'straddling_enumerated_6_faces': T * (6 * cap / 144 + rho),
        'two_creation_refined': rho * rho + T ** 3,
        'density_82_faces': (F(82, 144) * cap + 2 * rho + T * T) ** 2,
        'normalization_order': tiers['exact']['terms']['normalization_order']['value'],
    }
    K_ref = sum(ref.values()) / (cap * cap)
    s2, s3, s10 = sqrt_up(2), sqrt_up(3), sqrt_up(10)
    t1g = (11 + 3 * s2 + 2 * s3 + 2 * s10) / 144 * cap
    Tg = t1g / (1 - GP_R_UP * J)
    K_grouped = (GP_R_UP * J * Tg + 2 * Tg * Tg + (2 * Tg + Tg * Tg) ** 2 + cap / 144 * (2 * Tg + Tg * Tg) ** 2) / cap ** 2
    K_grouped_288 = (288 * J * Tg / (1 - 8 * Tg) + 2 * Tg * Tg + (2 * Tg + Tg * Tg) ** 2
                     + cap / 144 * (2 * Tg + Tg * Tg) ** 2) / cap ** 2
    cons4 = {k: dict(v) for k, v in tiers['exact']['terms'].items()}
    cons4['overlap_multiplier'] = dict(cons4['overlap_multiplier'], value=F(4), label='conservative')
    K_cons4 = k2_bound(cons4) / cap ** 2
    t1_84 = F(84, 144) * cap
    T84 = t1_84 / (1 - GP_R_UP * J)
    K_84x4 = (4 * (GP_R_UP * J * T84 + 2 * T84 * T84) + (2 * T84 + T84 * T84) ** 2) / cap ** 2
    need(K_grouped_288 < K_grouped < K_ref < Kx < K_cons4 < K_84x4, 'K2_labelled_variants_ordered',
         refined_288_enumerated=q(ceil_to(K_ref)), grouped_sqrt_352=q(ceil_to(K_grouped)),
         grouped_sqrt_288=q(ceil_to(K_grouped_288)), conservative_x4=q(ceil_to(K_cons4)),
         bound84_x4=q(ceil_to(K_84x4)))
    need(ref['straddling_enumerated_6_faces'] < tiers['exact']['terms']['straddling']['value']
         and ref['density_82_faces'] < tiers['exact']['terms']['density']['value'],
         'straddling_66_one_site_faces_orthogonal_6_contribute',
         note='66 of the 72 straddling faces meet one site of R and are exactly orthogonal to W Omega_R')

    # ||W Omega_R|| and the single-component overlap
    need(sph[2] == F(1, 4), 'W_Omega_R_norm_one_half', norm_squared=q(sph[2]))
    owners_W = sorted({coarse(p) for p, _ in W_links})
    need(owners_W == sorted(COVER), 'W_Omega_R_excited_on_both_sites',
         note='link (e_z,x) is owned by e_z, so c_{0} x Omega, Omega x c_{e_z} and one-site straddling terms are orthogonal')

    # K_2 for omega(W^2) (labelled skeptic extra, not a contract target)
    A_norm_sq = sph[4] - sph[2] / 2 + F(1, 16)
    ex = tiers['exact']['terms']
    K_W2 = (2 * F(1, 4) * (ex['am2_remainder']['value'] + ex['straddling']['value'] + ex['two_creation']['value'])
            + F(3, 4) * ex['density']['value']) / cap ** 2
    need(A_norm_sq == F(1, 16), 'W2_extra_uniform_second_order_constant', A_Omega_norm='1/4', A_norm='3/4',
         K2_W2_upper_ceil_1e12=q(ceil_to(K_W2)), label='labelled skeptic extra; not a contract target')

    # ---------------- (e) AW2 decade-grid rule
    tau_aw2 = aw2_rule(Kx)
    need(validate_aw2('exact', Kx, tau_aw2) and tau_aw2 == F(1, 10 ** 8), 'aw2_tau_from_frozen_rule',
         tau_AW2=q(tau_aw2), K2_times_cap=q(Kx * cap), half_first_order='1/288',
         margin_at_cap=q(floor_to(tiers['exact']['margin'], 10 ** 9)),
         K2_threshold_for_cap=q(F(10 ** 8, 288)))
    crude_rule = aw2_rule(Kc)
    need(crude_rule == F(1, 10 ** 10), 'crude_tier_rule_comparison_only', tau_if_crude=q(crude_rule),
         label='comparison only; the frozen rule uses the exact tier')

    # ---------------- controls (30 contract ids)
    def mutate_k2(tier='exact', **changes):
        terms, _, _ = k2_terms(tier, cap)
        terms = {k: dict(v) for k, v in terms.items()}
        drop = changes.pop('drop', None)
        if drop:
            del terms[drop]
        for (name, field), val in changes.pop('set', {}).items():
            terms[name][field] = val
        pk = {'tier': tier, 'terms': terms, 'combination': changes.pop('combination', 'linear'),
              'K2': changes.pop('K2', Kx if tier == 'exact' else Kc),
              'overlap_components': changes.pop('overlap_components', ['c_R'])}
        return lambda: validate_k2_packet(pk, cap)

    crude_terms, _, _ = k2_terms('crude', cap)
    exact_terms = tiers['exact']['terms']
    control('missing_incoming_stars',
            [('orthant_two_anchors', lambda: validate_geometry(2, 48, 36, geom_truth), 'incident stars')],
            [('seven_anchors', lambda: validate_geometry(7, 48, 36, geom_truth))])
    control('full_original_wilson_cover',
            [('four_displayed_links', lambda: validate_geometry(7, 4, 4, geom_truth), 'cover')])
    control('wrong_delta_alpha_hbar_clock',
            [('mixed_tau_over_9', lambda: validate_amplitude(F(1, 3) / 3, amp_alpha), 'unit mixing'),
             ('mixed_tau_over_576', lambda: validate_amplitude(amp_norm, F(1, 24) / 24), 'unit mixing'),
             ('exponent_24_with_alpha_clock', lambda: validate_free_exponent(24), 'clock')],
            [('amplitude_tau_over_72_both_units', lambda: validate_amplitude(amp_norm, amp_alpha))])
    control('vector_versus_scalar_centering',
            [('scalar_residue_for_vector', lambda: validate_centering('vector', F(1, 4), F(1, 100), F(-51, 10000)),
              'centering'),
             ('vector_residue_for_scalar', lambda: validate_centering('scalar', F(1, 4), F(1, 100), F(1, 10000)),
              'centering')])
    control('first_order_mean_charged',
            [('mean_first_order_zero', lambda: validate_mean(F(0)), 'first-order mean not charged')],
            [('mean_tau_over_144', lambda: validate_mean(coef))], m1=q(coef),
            note='m=tau/144+O(tau^2) is first order; m^2 is second order and is charged in C(s)')
    control('tau_scaling_exponent',
            [('remainder_called_linear', lambda: validate_scaling('linear', tiers['exact']['ratios']['am2_remainder']),
              'tau scaling'),
             ('first_order_called_quadratic', lambda: validate_scaling('quadratic', (coef * cap) / (coef * cap / 100)),
              'tau scaling')],
            first_order_ratio=q((coef * cap) / (coef * cap / 100)),
            am2_ratio=q(floor_to(tiers['exact']['ratios']['am2_remainder'], 10 ** 6)))
    good_model = {'tau_abs': cap, 'triple': ('0', '0', '0'), 'model_id': 'AQ_patterned_zero_selected'}
    control('changed_model_relabelled',
            [('tau_1e-14', lambda: validate_model(dict(good_model, tau_abs=F(1, 10 ** 14)), cap), 'model changed'),
             ('nonzero_triple', lambda: validate_model(dict(good_model, triple=('0', '1/8', '0')), cap), 'model changed'),
             ('finite_graph_under_aq_label', lambda: validate_model(dict(good_model, finite_graph=True), cap),
              'model changed')],
            [('cap_model', lambda: validate_model(good_model, cap))])
    required = list(contract['controls'])
    ev_bad = {cid: True for cid in required}
    ev_bad['haar_parity_exact'] = False
    ev_bad['contract_sha256'] = CONTRACT_SHA256
    ev_nohash = {cid: True for cid in required}
    control('coherent_evidence_tampering',
            [('flip_boolean_rebind_hash', lambda: validate_evidence(ev_bad, required), 'required control not passed'),
             ('contract_hash_removed', lambda: validate_evidence(ev_nohash, required), 'contract hash')])
    control('insufficient_verdict_retained',
            [('crude_tier_called_passing', lambda: validate_retained('crude', tiers['crude']['margin'], 'accepted'),
              'insufficient tier relabelled')],
            [('crude_tier_retained', lambda: validate_retained('crude', tiers['crude']['margin'], 'limited_retained'))],
            crude_margin_upper=q(ceil_to(tiers['crude']['margin'], 10 ** 9)))
    control('exact_arithmetic_admission',
            [('float_am2_term', mutate_k2(set={('am2_remainder', 'value'): float(exact_terms['am2_remainder']['value'])}),
              'exact arithmetic')])
    control('root_n_misuse',
            [('root_sum_square', mutate_k2(combination='root_sum_square'), 'root-N'),
             ('divide_by_sqrt_volume', mutate_k2(K2=Kx / 64), 'K_2 below its itemized sum')])
    control('no_priority_or_continuum_claim',
            [(key, (lambda k=key: validate_claims({'continuum_claim': False, 'uniform_wilson_claim': False,
                                                   'resolved_interaction_shift': False,
                                                   'scientific_priority_verified': False,
                                                   'third_order_remainder_claim': False, k: True})),
              'forbidden claim ' + key)
             for key in ('continuum_claim', 'scientific_priority_verified', 'resolved_interaction_shift',
                         'uniform_wilson_claim', 'third_order_remainder_claim')])
    parity_true = {'E[W^3]': sph[3], 'E[W^2 W_f] all f incl W': sum(abs(v) for v in w2w.values()),
                   'first_order_C': state_C + duhamel_C, 'first_order_W2': state_W2, 'energy_first_order': energy_1,
                   'E[W^2]': sph[2], 'E[W^4]': sph[4]}
    control('haar_parity_exact',
            [('E_W4_as_square_of_E_W2', lambda: validate_parity_claims(dict(parity_true, **{'E[W^4]': F(1, 16)})),
              'parity'),
             ('W_face_dropped_from_W2Wf', lambda: validate_parity_claims(dict(parity_true, **{'E[W^2 W_f] all f incl W':
                                                                                              F(1, 4)})), 'parity')],
            [('exact_values', lambda: validate_parity_claims(parity_true))])
    control('first_order_shift_of_C_vanishes',
            [('duhamel_with_one_W_dropped', lambda: validate_parity_claims(dict(parity_true, first_order_C=F(1, 96))),
              'parity'),
             ('av2_interval_as_evidence', lambda: validate_evidence_role('av2_interval'), 'not evidence')])
    control('degenerate_multiplet_first_order',
            [('zero_splitting_claimed_on_full_eigenspace',
              lambda: validate_multiplet('full_energy_24_eigenspace', full_elem), 'gauge-invariant multiplet'),
             ('nonzero_invariant_splitting', lambda: validate_multiplet('gauge_invariant_multiplet', F(-1, 96)),
              'invariant splitting')],
            [('invariant_zero', lambda: validate_multiplet('gauge_invariant_multiplet', F(0)))])
    fo_good = {'wilson_face_in_omitted_set': True, 'contributing_faces': ['W'], 'coefficient': coef}
    control('wilson_mean_first_order_coefficient',
            [('missing_factor_two', lambda: validate_first_order(dict(fo_good, coefficient=F(1, 288)), coef),
              'first-order coefficient'),
             ('norm_instead_of_norm_squared', lambda: validate_first_order(dict(fo_good, coefficient=F(1, 72)), coef),
              'first-order coefficient'),
             ('literal_contract_formula_sign', lambda: validate_first_order(dict(fo_good, coefficient=literal), coef),
              'first-order coefficient')],
            [('plus_1_over_144', lambda: validate_first_order(fo_good, coef))])
    other_R = sorted(k for k in ww if k != wname)
    control('wrong_face_control',
            [('coefficient_from_other_face_in_R',
              lambda: validate_first_order(dict(fo_good, contributing_faces=['xz:0,1,0']), coef), 'wrong face'),
             ('all_ten_faces_of_R', lambda: validate_first_order(dict(fo_good, contributing_faces=['W'] * 10), coef),
              'wrong face')],
            other_faces_zero=str(sum(1 for k, v in ww.items() if k != wname and v == 0)), examples=other_R[:3])
    control('sign_flip_tau',
            [('sign_blind_replay', lambda: validate_signed(coef * cap, coef * cap, cap), 'sign flip')],
            [('signed_values', lambda: validate_signed(coef * cap, -coef * cap, cap))],
            fixture_minus_tau=[q(c) for c in ser_m])
    control('second_order_remainder_itemized',
            [('two_creation_missing', mutate_k2(drop='two_creation'), 'error term missing'),
             ('straddling_zero', mutate_k2(set={('straddling', 'value'): F(0)}), 'term set to zero'),
             ('normalization_missing', mutate_k2(drop='normalization_order'), 'error term missing')],
            [('exact_packet', mutate_k2()), ('crude_packet', mutate_k2(tier='crude'))])
    control('static_not_dynamic_effect',
            [('called_dynamical', lambda: validate_static('dynamical_correction'), 'static'),
             ('called_mass_gap', lambda: validate_static('mass_gap_shift'), 'static')],
            [('static', lambda: validate_static('static_equal_time_mean'))])
    control('wilson_overlap_single_component',
            [('factor_4_unlabelled', mutate_k2(set={('overlap_multiplier', 'value'): F(4)}), 'overlap multiplier'),
             ('single_site_terms_counted', mutate_k2(overlap_components=['c_R', 'c_0', 'c_ez']), 'overlap multiplier')],
            [('factor_4_labelled_conservative',
              mutate_k2(set={('overlap_multiplier', 'value'): F(4), ('overlap_multiplier', 'label'): 'conservative'},
                        K2=K_cons4))],
            W_Omega_R_norm='1/2')
    control('sign_convention_fixture',
            [('flipped_coefficient_convention', lambda: validate_sign_fixture(ser_m), 'sign convention')],
            [('I1.5_one_plaquette', lambda: validate_sign_fixture(ser_p))], coefficient=q(ser_p[1]),
            model='finite graph (one plaquette), labelled; not an AQ result')
    control('aw2_coupling_rule_prefrozen',
            [('chosen_after_K2_1e-9', lambda: validate_aw2('exact', Kx, F(1, 10 ** 9)), 'coupling rule'),
             ('off_grid_5e-9', lambda: validate_aw2('exact', Kx, F(5, 10 ** 9)), 'coupling rule'),
             ('crude_tier_K2', lambda: validate_aw2('crude', Kc, crude_rule), 'exact-tier')],
            [('rule_value', lambda: validate_aw2('exact', Kx, tau_aw2))])
    control('flip_set_odd_intersection',
            [('E_minus_one_link', lambda: validate_flip_set(flip_counts(period, removed=(((0, 0, 0), 'x'),))),
              'odd intersection'),
             ('y_rule_on_p_x', lambda: validate_flip_set(flip_counts(period, rl={'x': 'y', 'y': 'x', 'z': 'x'})),
              'odd intersection')])
    control('flip_breaks_at_nonzero_kappa',
            [('tau_antisymmetry_claimed_at_kappa', lambda: validate_flip_claim(flip_coeffs(h_in), coeffs(-cap, kap)),
              'kappa=0')],
            [('tau_antisymmetry_at_zero_kappa', lambda: validate_flip_claim(flip_coeffs(coeffs(cap, zero)),
                                                                            coeffs(-cap, zero)))])
    control('flip_no_third_order_claim',
            [('third_order_from_oddness', lambda: validate_third_order({'remainder_order': 3}), 'third order')],
            counterexample='r(tau)=K tau|tau| is odd and r/tau^2=K sign(tau) never tends to 0')
    control('tier_mixing_rejected',
            [('crude_density_in_exact_packet', mutate_k2(set={('density', 'tier'): 'crude',
                                                              ('density', 'value'): crude_terms['density']['value']}),
              'tier mixing'),
             ('exact_remainder_labelled_crude', mutate_k2(tier='crude', set={('am2_remainder', 'value'):
                                                                            exact_terms['am2_remainder']['value']}),
              'tier mixing')])
    control('reverse_premise_isolation',
            [('forward_additional_added',
              lambda: validate_inventory(['AGENTS.md', 'research/round32/contracts/aw1.json'] + contract['shared_premises']
                                         + contract['forward_additional_premises'][:1], contract), 'forbidden input')],
            [('declared_inventory',
              lambda: validate_inventory(['AGENTS.md', 'research/round32/contracts/aw1.json'] + contract['shared_premises'],
                                         contract))],
            limitation='shared_premises include both loop-3 sign-offs that state the flip lemma (see contract review)')
    sep_good = {'omitted_at_anchor_0': ['W'] + ['o%d' % i for i in range(20)], 'others_at_anchor_0': 20,
                'first_order_faces': ['W']}
    control('wilson_face_separated',
            [('W_excluded', lambda: validate_face_separation(dict(sep_good, omitted_at_anchor_0=sep_good['omitted_at_anchor_0'][1:])),
              'Wilson face excluded'),
             ('merged_21', lambda: validate_face_separation(dict(sep_good, first_order_faces=['W'] + ['o%d' % i for i in range(20)])),
              'merged'),
             ('W_excluded_first_order', lambda: validate_first_order(dict(fo_good, wilson_face_in_omitted_set=False,
                                                                          coefficient=F(0)), coef),
              'Wilson face excluded')],
            [('separated', lambda: validate_face_separation(sep_good))])
    control('flip_nonzero_kappa_positive_demonstration',
            [('fixture_tau_antisymmetry_at_fixed_kappa',
              lambda: validate_fixture_antisymmetry(fixture_sel['+tau,+kappa'], fixture_sel['-tau,+kappa']),
              'kappa to -kappa')],
            [('coefficients_map_to_minus_kappa', lambda: validate_flip_claim(flip_coeffs(h_in), coeffs(-cap, kap_neg))),
             ('fixture_antisymmetric_under_joint_flip',
              lambda: validate_fixture_antisymmetry(fixture_sel['+tau,+kappa'], fixture_sel['-tau,-kappa']))],
            demonstration='coefficient map on the 24 anchored classes (kappa=(1/5,-1/10,1/7)) and the two-plaquette fixture')
    control('minus_tau_replay_not_flip_evidence',
            [('minus_tau_replay_as_flip_evidence', lambda: validate_evidence_role('minus_tau_replay'), 'not evidence')])
    ids = [row['id'] for row in CHECKS if row.get('kind') == 'control']
    missing = [cid for cid in contract['controls'] if cid not in ids]
    need(not missing, 'all_contract_controls_executed', n=str(len(contract['controls'])))

    flags = {'continuum_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False,
             'scientific_priority_verified': False, 'third_order_remainder_claim': False,
             'skeptic_package_is_certificate': False}
    need(validate_claims(flags), 'claim_flags_false')

    def term_rows(terms):
        return {k: {kk: (q(vv) if isinstance(vv, F) else vv) for kk, vv in v.items()} for k, v in sorted(terms.items())}

    previews = {
        'first_order_at_cap': preview(coef * cap), 'K2_exact': preview(Kx), 'K2_crude': preview(Kc),
        'K2_refined_288_enumerated': preview(K_ref), 'K2_grouped_352': preview(K_grouped),
        'K2_grouped_288': preview(K_grouped_288), 'K2_conservative_x4': preview(K_cons4), 'K2_84_x4': preview(K_84x4),
        'K2_W2_extra': preview(K_W2),
        'margin_exact_at_cap': preview(tiers['exact']['margin']), 'margin_crude_at_cap': preview(tiers['crude']['margin']),
        'remainder_exact_at_cap': preview(tiers['exact']['bound_at_cap']),
        'remainder_crude_at_cap': preview(tiers['crude']['bound_at_cap']),
        'D_ii_over_first_order': preview(D_ii / (cap / 144)),
        'tau_margin_two_exact': preview(F(1) / (288 * Kx)),
        'label': 'floating previews only; no admission Boolean reads them',
    }
    result = {
        'loop': 'AW1', 'stage': 'pre_comparison', 'role': 'skeptic',
        'standing': 'model-agent skeptic with correlated ancestry; not human peer review, not formal verification',
        'human_author': 'Hruday N M (BUNZEEY)',
        'producer_files_read': [],
        'contract_sha256': CONTRACT_SHA256, 'av1_gate_sha256': hashlib.sha256(gate_bytes).hexdigest(),
        'av2_gate_sha256': sha(AV2_GATE), 'i1_report_sha256': sha(I1_REPORT), 'am2_report_sha256': sha(AM2_REPORT),
        'at4_report_sha256': sha(AT4_REPORT),
        'model_id': contract['preregistration']['model_id'],
        'haar': {'character_moments_E_W^n': {str(n): q(v) for n, v in moments.items()},
                 'sphere_moments_actual_W': {str(n): q(v) for n, v in sph.items()},
                 'E_W_Wf_nonzero_only_W': q(ww[wname]), 'E_W2_Wf_all_82': 'all 0', 'E_Wf_all_82': 'all 0'},
        'odd_intersection': {'period_cell': {k: str(v) for k, v in c_period.items()},
                             'cube2_all_24_classes': {k: str(v) for k, v in c_box.items()},
                             'faces_meeting_R': {k: str(v) for k, v in c_R.items()}},
        'first_order': {'coefficient': q(coef), 'value_plus_cap': q(coef * cap), 'value_minus_cap': q(-coef * cap),
                        'contributing_face': 'W only (xz, r=0, s=0, anchor 0)',
                        'fixture_one_plaquette_series': [q(c) for c in ser_p]},
        'K2': {tier: {'t': q(v['t']), 'eps': q(v['eps']), 'terms': term_rows(v['terms']), 'K2_exact': q(v['K2']),
                      'K2_upper_1e-12': q(ceil_to(v['K2'])), 'margin_at_cap_exact': q(v['margin']),
                      'bound_at_cap': q(v['bound_at_cap'])} for tier, v in tiers.items()},
        'K2_labelled_variants_upper_1e-12': {'refined_288_enumerated': q(ceil_to(K_ref)),
                                             'grouped_sqrt_352': q(ceil_to(K_grouped)),
                                             'grouped_sqrt_288': q(ceil_to(K_grouped_288)),
                                             'conservative_x4': q(ceil_to(K_cons4)), 'bound84_x4': q(ceil_to(K_84x4)),
                                             'omega_W2_extra': q(ceil_to(K_W2))},
        'aw2_rule': {'tau_AW2': q(tau_aw2), 'K2_tier': 'exact', 'K2_times_cap': q(Kx * cap), 'threshold': '1/288',
                     'margin_at_cap_lower_1e-9': q(floor_to(tiers['exact']['margin'], 10 ** 9)),
                     'crude_tier_comparison_tau': q(crude_rule)},
        'previews': previews,
        'checks': CHECKS,
    }
    result.update(flags)
    return result


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
    print(json.dumps({'checks': len(result['checks']), 'K2_exact': result['previews']['K2_exact'],
                      'K2_crude': result['previews']['K2_crude'], 'tau_AW2': result['aw2_rule']['tau_AW2'],
                      'margin': result['previews']['margin_exact_at_cap']}))


if __name__ == '__main__':
    main()
