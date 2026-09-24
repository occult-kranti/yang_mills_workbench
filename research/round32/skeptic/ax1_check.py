#!/usr/bin/env python3
"""Round32 AX1 skeptic pre-comparison checker (uniform model, route B).

Written after the AX1 contract freeze from the frozen contract, the AV1, AV2,
AW1 and AW2 gates, the AM2, AL1, AQ1, AQ2 and I1 forward reports and the
skeptic's own notes, before reading research/round32/forward/ax1/ or
research/round32/reverse/ax1/. Nothing is imported from any producer or
assistant. Standard library only. Every admission Boolean is decided with
fractions.Fraction; floats appear only in the labelled 'previews' block. Every
check and control raises an explicit exception, so python -O cannot disable
it. Model-agent skeptic with correlated ancestry; not human peer review.

Routes used here:
  * Face classes derived from the I1.1 ownership map and the I1.4 owner-set
    rule on a fundamental cell, cross-checked against the printed I1 table.
  * Incidence and per-site sums by brute force on centered boxes N=1,2,3 plus
    the all-size offset argument (classes containing each offset of S).
  * State-lemma tiers from the AV1 product split (psi=psi_out+delta,
    eps=2t+t^2) with the forward density bound 2eps(1+eps)/(1+eps^2) and the
    purification bracket [2eps-eps^3, 2eps].

Usage: python3 -B research/round32/skeptic/ax1_check.py --output /absolute/fresh/dir
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
CONTRACT = ROOT / 'research/round32/contracts/ax1.json'
CONTRACT_SHA256 = 'bc834eec4f5377041cea9db42a8674cf1f3de0a43b7fef3696a461a011da7d8d'
I1_REPORT = ROOT / 'research/round21/forward/i1/report.md'
AV1_GATE = ROOT / 'research/round32/advisor/av1-gate.json'
AW1_GATE = ROOT / 'research/round32/advisor/aw1-gate.json'

DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
R_COVER = ((0, 0, 0), (0, 0, 1))
ERROR_TERMS = ('am2_remainder', 'two_creation', 'straddling', 'density', 'onsite_cutoff_vector', 'arithmetic')
LABEL = 'uniform Kogut-Susskind SU(2) at fixed spacing, strong bare coupling, g^4=96/tau'


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


def add(a, b):
    return tuple(i + j for i, j in zip(a, b))


def sub(a, b):
    return tuple(i - j for i, j in zip(a, b))


# ---------------------------------------------------------------- geometry
def pi_map(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    ea, ec = DIRS[a], DIRS[c]
    return ((p, a), (p, c), (add(p, ea), c), (add(p, ec), a))


def owner_set(p, a, c):
    return frozenset(pi_map(tail) for tail, _ in face_links(p, a, c))


def is_selected(p, a, c):
    return (a, c) == ('x', 'y') and p[0] % 4 in (0, 1, 2) and p[1] % 2 == 0


def anchored_faces(b):
    out = []
    for r, s in product(range(4), range(2)):
        p = (4 * b[0] + r, 2 * b[1] + s, b[2])
        for a, c in ORIENT:
            out.append({'base': p, 'orient': a + c, 'r': r, 's': s, 'anchor': b,
                        'owners': owner_set(p, a, c), 'selected': is_selected(p, a, c)})
    return out


def cell_classes():
    classes = {}
    for f in anchored_faces((0, 0, 0)):
        rel = tuple(sorted(f['owners']))
        key = (f['orient'], rel, f['selected'])
        classes[key] = classes.get(key, 0) + 1
    return classes


def parse_i1_table():
    text = I1_REPORT.read_text()
    rows = re.findall(r'^\| (xy|xz|yz): [^|]*\| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|$', text, re.M)
    out = {}
    for orient, cnt, supp, role in rows:
        sites = []
        for tok in [s.strip() for s in supp.split(',')]:
            sites.append({'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}[tok])
        key = (orient, tuple(sorted(sites)), role == 'selected')
        out[key] = out.get(key, 0) + int(cnt)
    return out


def box(n):
    return [b for b in product(range(-n, n + 1), repeat=3)]


def in_box(b, n):
    return all(-n <= v <= n for v in b)


def retained_groups(n):
    """Route B: whole stars (21 omitted faces, retained iff b+S in box) and one
    single-factor group per factor (its 3 selected faces). Each face is charged
    to exactly one group: (anchor=pi(base), role)."""
    groups = []
    for b in box(n):
        faces = anchored_faces(b)
        om = [f for f in faces if not f['selected']]
        se = [f for f in faces if f['selected']]
        if all(in_box(add(b, s), n) for s in S_STAR):
            groups.append({'kind': 'star', 'anchor': b, 'support': frozenset(add(b, s) for s in S_STAR),
                           'faces': om, 'norm_over_tau': F(len(om), 3)})
        groups.append({'kind': 'single', 'anchor': b, 'support': frozenset([b]),
                       'faces': se, 'norm_over_tau': F(len(se), 3)})
    return groups


def box_census(n):
    groups = retained_groups(n)
    face_keys = []
    for g in groups:
        for f in g['faces']:
            face_keys.append((f['base'], f['orient']))
    if len(face_keys) != len(set(face_keys)):
        raise CheckFailure('face charged twice')
    sites = box(n)
    per_site = {}
    for u in sites:
        jsum = sum((g['norm_over_tau'] for g in groups if u in g['support']), F(0))
        om = sum(1 for g in groups if g['kind'] == 'star' for f in g['faces'] if u in f['owners'])
        se = sum(1 for g in groups if g['kind'] == 'single' for f in g['faces'] if u in f['owners'])
        per_site[u] = (jsum, om, se)
    Rset = set(R_COVER)
    stars_R = [g for g in groups if g['kind'] == 'star' and g['support'] & Rset]
    singles_R = [g for g in groups if g['kind'] == 'single' and g['support'] & Rset]
    faces_all = [(g, f) for g in groups for f in g['faces']]
    meet = [(g, f) for g, f in faces_all if f['owners'] & Rset]
    inside = [(g, f) for g, f in meet if f['owners'] <= Rset]
    table = []
    for g in sorted(stars_R + singles_R, key=lambda g: (g['kind'], g['anchor'])):
        m = [f for f in g['faces'] if f['owners'] & Rset]
        table.append({'group': g['kind'], 'anchor': list(g['anchor']), 'faces_in_group': len(g['faces']),
                      'norm_over_tau': q(g['norm_over_tau']), 'faces_meeting_R': len(m),
                      'faces_inside_R': sum(1 for f in m if f['owners'] <= Rset),
                      'faces': [{'base': list(f['base']), 'orient': f['orient'], 'r': f['r'], 's': f['s'],
                                 'owners': sorted(list(o) for o in f['owners']),
                                 'meets_R': bool(f['owners'] & Rset)} for f in g['faces']]})
    return {
        'groups': groups, 'per_site': per_site, 'stars_R': stars_R, 'singles_R': singles_R,
        'meet': meet, 'inside': inside, 'table': table,
    }


def flip_parity(p, a, c):
    """E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even}."""
    cnt = 0
    for tail, d in face_links(p, a, c):
        if (d == 'x' and tail[1] % 2 == 0) or (d == 'y' and tail[2] % 2 == 0) or (d == 'z' and tail[0] % 2 == 0):
            cnt += 1
    return cnt


# ---------------------------------------------------------------- constants
def exp_eighth_upper(n=12):
    x = F(1, 8)
    s = sum((x ** k / fact(k) for k in range(n + 1)), F(0))
    tail = x ** (n + 1) / fact(n + 1) / (1 - x / (n + 2))
    return s + tail


def atan_bracket(x, terms):
    s = F(0)
    for k in range(terms):
        s += (-1) ** k * x ** (2 * k + 1) / (2 * k + 1)
    nxt = x ** (2 * terms + 1) / (2 * terms + 1)
    return (s, s + nxt) if terms % 2 == 0 else (s - nxt, s)


def pi_bracket():
    a_lo, a_hi = atan_bracket(F(1, 5), 25)
    b_lo, b_hi = atan_bracket(F(1, 239), 8)
    lo, hi = 16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo
    den = 10 ** 30
    lo = F((lo.numerator * den) // lo.denominator, den)
    hi = F(-((-hi.numerator * den) // hi.denominator), den)
    if not (hi - lo <= F(3, 10 ** 30) and lo < F(314159265358979, 10 ** 14) + F(4, 10 ** 14) and hi > F(314159265358979, 10 ** 14)):
        raise CheckFailure('pi bracket')
    return lo, hi


def catalan_moment(k):
    """E[W^k], W=chi_{1/2}/2: multiplicity of spin 0 in (1/2)^{(x)k} over 2^k."""
    mult = {F(0): 1}
    for _ in range(k):
        nxt = {}
        for j, m in mult.items():
            for jj in ((j - F(1, 2)), (j + F(1, 2))):
                if jj >= 0:
                    nxt[jj] = nxt.get(jj, 0) + m
        mult = nxt
    return F(mult.get(F(0), 0), 2 ** k)


def tier_values(t):
    eps = 2 * t + t * t
    d_fwd = 2 * eps * (1 + eps) / (1 + eps * eps)
    return {'t': t, 'eps': eps, 'D_fwd': d_fwd, 'D_pur_upper': 2 * eps, 'D_pur_lower': 2 * eps - eps ** 3}


def t_tier_i(abs_tau):
    return 29 * abs_tau * F(148, 7)


def t_tier_ii(abs_tau, face_count):
    t1 = F(face_count, 144) * abs_tau
    return t1 / (1 - 352 * 29 * abs_tau)


# ---------------------------------------------------------------- validator
def reference_packet(c):
    return {
        'route': 'B', 'reference': 'haar', 'reference_correlation': 'exp(-3s)/4',
        'label': LABEL, 'tau': c['tau'], 'model_cap': F(1, 10 ** 8),
        'face_coeff_normalized': {'omitted': F(-1, 3), 'selected': F(-1, 3)},
        'selected_over_alpha': F(1, 24), 'J_over_tau': F(29), 'J0': F(29, 10 ** 8),
        'star_faces': 21, 'single_faces': 3,
        'G_R': F(148, 7), 'Gp_R': F(352), 'reset_over_tau': F(102), 'eps_R_over_tau': F(17),
        'onsite_gap': F(6), 'cover': list(R_COVER), 'stars_R': 7, 'singles_R': 2, 'selected_faces_R': 6,
        'incidence_table': [(row['group'], tuple(row['anchor']), row['faces_meeting_R']) for row in c['table']],
        'faces_meeting_R_total': 88, 'B_over_tau': F(51, 8), 'k_over_tau': F(51, 4), 'clock_units': 'G=H/alpha',
        'faces_per_factor': 52, 'faces_per_factor_label': 'exact', 't1_rule': 'exact_first_order',
        't_rule': 'self_consistent', 'D_ii': c['D_ii'], 'D_i': c['D_i'], 'tiers_reported': ['i', 'ii'],
        'combine': 'linear', 'scaling_exponent': 1, 'first_order_charged': True,
        'kappa_tied_to_tau': True, 'contract_sha256': CONTRACT_SHA256, 'error_terms': list(ERROR_TERMS),
        'claims': dict(CLAIMS),
    }


CLAIMS = {'continuum_claim': False, 'weak_coupling_claim': False, 'resolved_interaction_shift': False,
          'scientific_priority_verified': False, 'uniform_wilson_claim': True}


def validate(pk, c):
    if pk['route'] != 'B':
        raise Rejected('reference route not declared as B')
    if pk['reference'] != 'haar' or pk['reference_correlation'] != 'exp(-3s)/4':
        raise Rejected('selected reference mixed with Haar route')
    if pk['reset_over_tau'] == 98:
        raise Rejected('selected reference mixed with Haar route')
    lab = pk['label'].lower()
    if 'weak coupling' in lab.replace('strong bare coupling', '') or 'continuum' in lab or 'fixed spacing' not in lab:
        raise Rejected('label must be uniform Kogut-Susskind at fixed spacing, strong coupling')
    if abs(pk['selected_over_alpha']) * abs(pk['tau']) > F(1, 8) or pk['selected_over_alpha'] != F(1, 24):
        raise Rejected('uniform triple outside box or not tau/24')
    if abs(pk['tau']) != pk['model_cap'] or pk['model_cap'] != F(1, 10 ** 8):
        raise Rejected('changed model relabelled')
    fc = pk['face_coeff_normalized']
    if fc['selected'] != fc['omitted'] or fc['omitted'] != F(-1, 3):
        raise Rejected('uniform sign convention')
    if not pk['kappa_tied_to_tau']:
        raise Rejected('kappa not tied to tau: no uniform flip identity')
    if pk['star_faces'] != 21 or pk['single_faces'] != 3:
        raise Rejected('double count: a face charged in two groups')
    j = F(4 * pk['star_faces'], 3) + F(pk['single_faces'], 3)
    if pk['J_over_tau'] != j or j != 29:
        raise Rejected('per-site sum')
    if pk['J0'] == F(7, 25000000):
        raise Rejected('J0 resolution: old J_0 below J at the cap')
    if pk['J0'] < pk['J_over_tau'] * abs(pk['tau']):
        raise Rejected('J0 resolution: J_0 below J at the cap')
    if not (pk['J0'] * pk['G_R'] < F(1, 64) and 2 * pk['J0'] * pk['Gp_R'] < 1):
        raise Rejected('AM2 contraction fails')
    if pk['onsite_gap'] != 6:
        raise Rejected('reset: Haar gap six')
    if pk['cover'] != list(R_COVER):
        raise Rejected('cover')
    if pk['stars_R'] != 7:
        raise Rejected('incident stars')
    if pk['singles_R'] != 2 or pk['selected_faces_R'] != 6:
        raise Rejected('selected incidence count')
    if not pk['incidence_table']:
        raise Rejected('incidence table missing')
    if sum(row[2] for row in pk['incidence_table']) != pk['faces_meeting_R_total']:
        raise Rejected('incidence table does not sum')
    if sum(1 for row in pk['incidence_table'] if row[0] == 'star') != pk['stars_R']:
        raise Rejected('incidence table does not sum')
    reset = 2 * (pk['stars_R'] * 7 + pk['singles_R'] * 1)
    if pk['reset_over_tau'] != reset:
        raise Rejected('reset budget')
    if pk['eps_R_over_tau'] != F(reset) / pk['onsite_gap']:
        raise Rejected('reset: Haar gap six')
    if pk['clock_units'] != 'G=H/alpha':
        raise Rejected('clock or unit mixing')
    b_n = F(pk['stars_R'] * 7 + pk['singles_R'], 8)
    if pk['B_over_tau'] != b_n or pk['k_over_tau'] != 2 * b_n:
        raise Rejected('clock or unit mixing')
    if pk['faces_per_factor'] == 49:
        raise Rejected('first-order faces: selected faces omitted')
    if pk['faces_per_factor'] == 96 and pk['faces_per_factor_label'] == 'exact':
        raise Rejected('first-order faces: 96 is a four-anchor bound')
    if pk['faces_per_factor'] not in (52, 96):
        raise Rejected('first-order faces: count not derived')
    if pk['t1_rule'] == 'exact_first_order' and pk['t_rule'] != 'self_consistent':
        raise Rejected('tier mixing')
    if not pk['first_order_charged']:
        raise Rejected('first-order mean not charged')
    if pk['combine'] != 'linear':
        raise Rejected('root-N or non-linear combination of error terms')
    if pk['scaling_exponent'] != 1:
        raise Rejected('tau scaling exponent')
    if any(isinstance(v, float) for v in (pk['D_ii'], pk['D_i'], pk['J0'], pk['tau'])):
        raise Rejected('exact arithmetic')
    if pk['D_ii'] < c['D_ii_floor']:
        raise Rejected('D_ii below the derived tier value')
    if 'i' not in pk['tiers_reported']:
        raise Rejected('insufficient tier not retained')
    if pk['contract_sha256'] != CONTRACT_SHA256:
        raise Rejected('contract hash')
    for name in ERROR_TERMS:
        if name not in pk['error_terms']:
            raise Rejected('error term missing: ' + name)
    for key in ('continuum_claim', 'weak_coupling_claim', 'resolved_interaction_shift', 'scientific_priority_verified'):
        if pk['claims'].get(key) is not False:
            raise Rejected('forbidden claim ' + key)
    return True


def flip_coefficients(coeffs, parity):
    return {f: v * (-1 if parity[f] % 2 else 1) for f, v in coeffs.items()}


def uniform_flip_ok(coeff_fn, faces, parity, taus):
    for tau in taus:
        lhs = flip_coefficients({f: coeff_fn(f, tau) for f in faces}, parity)
        rhs = {f: coeff_fn(f, -tau) for f in faces}
        if lhs != rhs:
            raise Rejected('kappa not tied to tau: no uniform flip identity')
    return True


# ---------------------------------------------------------------- execute
def execute():
    contract_bytes = CONTRACT.read_bytes()
    c_sha = hashlib.sha256(contract_bytes).hexdigest()
    need(c_sha == CONTRACT_SHA256, 'contract_sha256_pinned', sha256=c_sha)
    con = json.loads(contract_bytes)
    par = con['parameters']
    tau_cap = F(par['tau_cap'])
    target = F(con['preregistration']['target']['value'])
    need(con['status'] == 'frozen_before_production' and tau_cap == F(1, 10 ** 8) and target == F(1, 2500000)
         and con['preregistration']['target']['comparator'] == '<=', 'contract_target_and_cap_read',
         tau_cap=q(tau_cap), target=q(target))
    need(par['signs'] == ['+', '-'], 'contract_both_signs')

    # 1. dictionary and box
    g4 = 96 / tau_cap
    need(g4 == 9600000000 and tau_cap / 24 <= F(1, 8) and tau_cap / 24 <= F(1, 2) and F(3, 24) == F(1, 8),
         'dictionary_and_box', g4_at_cap=q(g4), r_selected=q(tau_cap / 24), box_holds_for_abs_tau_le='3')
    # lambda/alpha=4/g^4, tau=24 lambda/alpha, nu=alpha tau/24 = lambda; normalized nu/delta = tau/3
    need(24 * F(4) / g4 == tau_cap and (tau_cap / 24) / F(1, 8) == tau_cap / 3, 'dictionary_normalization')

    # 2. face classes
    classes = cell_classes()
    i1 = parse_i1_table()
    need(classes == i1 and sum(classes.values()) == 24, 'face_classes_match_I1_table', classes=len(classes))
    sel = sum(v for k, v in classes.items() if k[2])
    need(sel == 3 and all(len(k[1]) == 1 for k in classes if k[2]) and all(len(k[1]) >= 2 for k in classes if not k[2]),
         'selected_iff_single_factor_support', selected=sel, omitted=24 - sel)
    offs = {s: sum(v for k, v in classes.items() if s in k[1]) for s in S_STAR}
    per_factor = sum(offs.values())
    per_factor_om = sum(v * len(k[1]) for k, v in classes.items() if not k[2])
    both_R = sum(v for k, v in classes.items() if (0, 0, 0) in k[1] and (0, 0, 1) in k[1])
    need(offs == {(0, 0, 0): 24, (1, 0, 0): 4, (0, 1, 0): 8, (0, 0, 1): 16} and per_factor == 52 and per_factor_om == 49,
         'per_factor_owner_count_all_sizes', offsets={str(k): v for k, v in offs.items()}, exact=per_factor,
         omitted=per_factor_om, selected=per_factor - per_factor_om, bound_four_anchors=4 * 24)
    anchors_R = sorted({sub(r, s) for r in R_COVER for s in S_STAR})
    faces_R = 2 * per_factor - both_R
    need(len(anchors_R) == 7 and both_R == 16 and faces_R == 88, 'faces_meeting_R_all_sizes',
         anchors=[list(a) for a in anchors_R], exact=faces_R, bound_seven_anchors=7 * 24, containing_R=both_R)

    # 3. brute force on boxes
    census = {}
    for n in (1, 2, 3):
        cz = box_census(n)
        mx_j = max(v[0] for v in cz['per_site'].values())
        mx_f = max(v[1] + v[2] for v in cz['per_site'].values())
        census[n] = cz
        need(mx_j <= 29 and mx_f <= 52 and all(v[2] <= 3 and v[1] <= 49 for v in cz['per_site'].values()),
             'box_N%d_per_site_bounded_by_bulk' % n, max_J_over_tau=q(mx_j), max_faces=mx_f)
    c2, c3 = census[2], census[3]
    u0 = c3['per_site'][(0, 0, 0)]
    need(u0 == (F(29), 49, 3) and max(v[0] for v in c3['per_site'].values()) == 29, 'bulk_J_prime_29',
         J_over_tau='29', faces=(u0[1], u0[2]))
    for n, cz in ((2, c2), (3, c3)):
        need(len(cz['stars_R']) == 7 and len(cz['singles_R']) == 2 and len(cz['meet']) == 88
             and sum(1 for g, f in cz['meet'] if f['selected']) == 6 and len(cz['inside']) == 16
             and sum(1 for g, f in cz['inside'] if f['selected']) == 6,
             'incidence_R_box_N%d' % n, stars=7, single_groups=2, faces_meeting=88, selected_faces=6,
             inside=16, straddling=len(cz['meet']) - len(cz['inside']))
    c1 = census[1]
    n1 = {'stars': len(c1['stars_R']), 'singles': len(c1['singles_R']), 'faces_meeting': len(c1['meet'])}
    need(n1 == {'stars': 4, 'singles': 2, 'faces_meeting': 55}, 'incidence_R_box_N1_boundary', **n1)
    tab = c3['table']
    per_anchor = {(row['group'], tuple(row['anchor'])): row['faces_meeting_R'] for row in tab}
    expect = {('star', (0, 0, 0)): 21, ('star', (0, 0, 1)): 21, ('star', (0, 0, -1)): 16,
              ('star', (-1, 0, 0)): 4, ('star', (0, -1, 0)): 8, ('star', (-1, 0, 1)): 4, ('star', (0, -1, 1)): 8,
              ('single', (0, 0, 0)): 3, ('single', (0, 0, 1)): 3}
    need(per_anchor == expect and sum(expect.values()) == 88
         and sum(row['faces_in_group'] for row in tab) == 7 * 21 + 2 * 3, 'incidence_table_census',
         rows=[{'group': k[0], 'anchor': list(k[1]), 'faces_meeting_R': v} for k, v in sorted(expect.items())],
         faces_charged_in_B=7 * 21 + 2 * 3)
    keys = [(f['base'], f['orient']) for g in c3['groups'] for f in g['faces']]
    need(len(keys) == len(set(keys)) and all(not f['selected'] for g in c3['groups'] if g['kind'] == 'star' for f in g['faces'])
         and all(f['selected'] for g in c3['groups'] if g['kind'] == 'single' for f in g['faces']),
         'route_b_partition_census', faces=len(keys))
    b_norm = F(7 * 7 + 2 * 1, 8)
    need(b_norm == F(51, 8) and 2 * b_norm == F(51, 4) and sum(g['norm_over_tau'] for g in c3['stars_R'] + c3['singles_R']) == 51,
         'B_N_and_k_prime', B_over_tau=q(b_norm), k_over_tau=q(2 * b_norm))
    mult = {}
    for g in c3['groups']:
        for f in g['faces']:
            if (0, 0, 0) in f['owners']:
                mult[f['owners']] = mult.get(f['owners'], 0) + 1
    mults = sorted(mult.values())
    need(mults == [1] * 5 + [2] * 3 + [3] * 3 + [4] * 3 + [10] * 2 and sum(mults) == 52
         and mult[frozenset([(0, 0, 0)])] == 3, 'owner_sets_through_bulk_site', owner_sets=len(mults), multiplicities=mults)

    # 4. contraction (R1), termination, onsite
    e8 = exp_eighth_upper()
    g_r = 16 * e8 * (1 + F(10, 64))
    gp_r = 16 * e8 * (18 + F(80, 64))
    need(e8 < F(8, 7) and g_r < F(148, 7) and gp_r < 352, 'am2_majorant_bounds', exp_eighth_upper=q(e8))
    j0p = F(int(par['J0_resolution'].split("J_0'=")[1].split(' ')[0].replace('/10^8', '')), 10 ** 8)
    c1r, c2r = j0p * F(148, 7), 2 * j0p * 352
    need(j0p == F(29, 10 ** 8) and c1r == F(1073, 175000000) and c1r < F(1, 64) and c2r == F(319, 1562500) and c2r < 1,
         'j0_prime_contraction', J0_prime=q(j0p), J0p_G=q(c1r), two_J0p_Gp=q(c2r))
    j0_old = F(7, 25000000)
    need(j0_old < 29 * tau_cap and F(7, 725000000) * 29 == j0_old, 'j0_old_fails_at_cap', J0_old=q(j0_old),
         R2_cap=q(F(7, 725000000)))
    slack_tau = min(F(1, 64) / F(148, 7), F(1, 704)) / 29
    need(slack_tau == F(7, 274688) and slack_tau / tau_cap > 2500, 'contraction_slack', max_abs_tau=q(slack_tau))
    need(max(len(g['support']) for g in c3['groups']) == 4 and 2 * 4 == 8, 'support_and_termination',
         max_support=4, termination_order=8)
    need(8 * F(3, 4) == 6 and catalan_moment(2) == F(1, 4) and catalan_moment(4) == F(1, 8)
         and catalan_moment(1) == 0 and catalan_moment(3) == 0 and 8 * 4 * F(3, 4) == 24, 'onsite_gap_six_and_haar',
         face_energy=24, face_vector_norm_sq=q(catalan_moment(2)))

    # 5. reset, square-root control, AQ constants
    reset = 2 * (7 * 7 + 2 * 1)
    need(reset == 102 and F(reset, 6) == 17 and F(17, 10 ** 8) <= F(1, 10 ** 6) and F(102, 10 ** 8) > F(1, 10 ** 6),
         'reset_budget_and_gap_six', reset_over_tau=reset, eps_R_over_tau=17,
         aq2_one_over_500_needs_gap_six=True, tighter_inside_R_over_tau=2 * 49 + 2)
    sq = sqrt_up(68) / 10 ** 4
    need(sq < F(1, 500), 'sqrt_control_value', two_sqrt_17tau_upper=q(sq))
    phi_crude = 81 * 29
    phi_pair = max(29, 16 * 7, 81 * 7)
    need(phi_crude == 2349 and phi_pair == 567 and phi_pair <= 2268 and 58 == 2 * (4 * 7 + 1), 'aq1_constants',
         Phi_F_crude=phi_crude, Phi_F_per_pair=phi_pair, C_F_over_tau_per_site=58)

    # 6. first order and flip transfer
    wf = [f for f in anchored_faces((0, 0, 0)) if f['base'] == (0, 0, 0) and f['orient'] == 'xz'][0]
    need(not wf['selected'] and wf['owners'] == frozenset(R_COVER) and flip_parity((0, 0, 0), 'x', 'z') == 3,
         'wilson_face_is_omitted_xz_and_flipped', first_order_coefficient='+1/144')
    om1 = F(2, 72) * catalan_moment(2)
    need(om1 == F(1, 144) and om1 * tau_cap == F(1, 14400000000), 'first_order_wilson_mean', plus=q(om1 * tau_cap),
         minus=q(-om1 * tau_cap))
    par_counts = [0, 0]
    faces_c2 = [f for g in c2['groups'] for f in g['faces']]
    extra = [f for b in box(2) for f in anchored_faces(b)]
    for f in extra:
        k = flip_parity(f['base'], f['orient'][0], f['orient'][1])
        if k % 2 == 0:
            raise CheckFailure('even plaquette')
        par_counts[0 if k == 1 else 1] += 1
    need(par_counts[0] + par_counts[1] == 3000 and all(flip_parity(f['base'], f['orient'][0], f['orient'][1]) % 2 == 1
                                                     for f in faces_c2 if f['selected']),
         'flip_set_odd_on_all_plaquettes', one_link=par_counts[0], three_links=par_counts[1])
    fkeys = [(f['base'], f['orient']) for f in faces_c2]
    parity = {(f['base'], f['orient']): flip_parity(f['base'], f['orient'][0], f['orient'][1]) for f in faces_c2}
    uniform = lambda f, tau: -tau / 3
    need(uniform_flip_ok(uniform, fkeys, parity, (tau_cap, tau_cap / 7)), 'uniform_flip_identity_coefficients')

    # 7. state lemma tiers; first reproduce the AV1-admitted zero-selected D_ii
    av1 = json.loads(AV1_GATE.read_text())['accepted']
    av1_d = F(re.search(r'D_ii=(\d+/\d+)', av1).group(1))
    t_av1 = F(49, 144) * tau_cap / (1 - 352 * 28 * tau_cap)
    need(tier_values(t_av1)['D_fwd'] == av1_d, 'av1_zero_selected_D_ii_reproduced', D_ii_av1=q(av1_d))
    aw1 = json.loads(AW1_GATE.read_text())['accepted']
    need('+tau/144' in aw1 and 'only f=W contributes' in aw1, 'aw1_first_order_source_read')
    out_tiers = {}
    for sign in (1, -1):
        tau = sign * tau_cap
        a = abs(tau)
        rows = {
            'D_i_crude': tier_values(t_tier_i(a)),
            'D_ii_exact52': tier_values(t_tier_ii(a, 52)),
            'D_ii_bound96': tier_values(t_tier_ii(a, 96)),
        }
        s2, s3, s10 = sqrt_up(2), sqrt_up(3), sqrt_up(10)
        t1g = (11 + 3 * s2 + 3 * s3 + 2 * s10) / 144 * a
        tg = t1g / (1 - 352 * 29 * a)
        rows['D_ii_grouped_labelled'] = tier_values(tg)
        t52 = t_tier_ii(a, 52)
        eps_r = F(88, 144) * a + 2 * 352 * 29 * a * t52 + t52 * t52
        rows['D_ii_R88_labelled'] = {'t': t52, 'eps': eps_r, 'D_fwd': 2 * eps_r * (1 + eps_r) / (1 + eps_r ** 2),
                                     'D_pur_upper': 2 * eps_r, 'D_pur_lower': 2 * eps_r - eps_r ** 3}
        out_tiers['+' if sign > 0 else '-'] = rows
    plus = out_tiers['+']
    need(out_tiers['+'] == out_tiers['-'], 'both_signs_same_abs_tau_formula')
    need(plus['D_i_crude']['t'] == F(1073, 175000000), 'tier_i_t')
    need(plus['D_ii_exact52']['t'] == F(13, 3599632512), 'tier_ii_t_exact52')
    for name, row in plus.items():
        need(row['D_pur_lower'] <= row['D_fwd'] and row['D_fwd'] <= row['D_pur_upper'] + row['eps'] ** 2 * 2
             and row['eps'] <= 1, 'bracket_' + name)
    d_ii, d_i = plus['D_ii_exact52']['D_fwd'], plus['D_i_crude']['D_fwd']
    need(d_ii <= target and plus['D_ii_bound96']['D_fwd'] <= target and d_ii <= F(1, 10 ** 6), 'D_ii_meets_target',
         D_ii=q(d_ii), D_ii_bound96=q(plus['D_ii_bound96']['D_fwd']))
    need(d_i > target and d_i > F(1, 10 ** 6), 'D_i_fails_target_retained', D_i=q(d_i))
    need(plus['D_ii_grouped_labelled']['D_fwd'] < plus['D_ii_R88_labelled']['D_fwd'] < d_ii
         < plus['D_ii_bound96']['D_fwd'], 'tier_ordering')
    ratios = {}
    for name, fn in (('i', lambda a: t_tier_i(a)), ('ii52', lambda a: t_tier_ii(a, 52)), ('ii96', lambda a: t_tier_ii(a, 96))):
        r = tier_values(fn(tau_cap))['D_fwd'] / tier_values(fn(tau_cap / 100))['D_fwd']
        ratios[name] = r
        need(99 <= r <= 101, 'linear_scaling_' + name, ratio=preview(r))
    at4 = F(4 * 17) * tau_cap  # (2 sqrt(17 tau))^2
    need(at4 / (at4 / 100) == 100, 'sqrt_control_scaling_is_root')

    # 8. AX2 feasibility (window budget 2(D+D^2)+51|tau|/pi at s=1)
    pi_lo, pi_hi = pi_bracket()
    dyn_up = 51 * tau_cap / pi_lo
    dyn_lo = 51 * tau_cap / pi_hi
    feas = lambda d: 2 * (d + d * d) + dyn_up <= F(1, 10 ** 6)
    infeas = lambda d: 2 * (d + d * d) + dyn_lo > F(1, 10 ** 6)
    need(feas(d_ii) and feas(plus['D_ii_bound96']['D_fwd']) and feas(F(4, 10 ** 7)) and feas(F(41883, 10 ** 11))
         and infeas(F(41884, 10 ** 11)) and infeas(F(419, 10 ** 9)), 'ax2_feasibility_threshold',
         threshold_bracket=['41883/10^11', '41884/10^11'], contract_note_419e_9_infeasible=True)
    e_prev = 2 * (d_ii + d_ii ** 2) + dyn_up

    # 9. controls
    ctx = {'tau': tau_cap, 'table': tab, 'D_ii': d_ii, 'D_i': d_i, 'D_ii_floor': d_ii}
    base = reference_packet(ctx)
    need(validate(base, ctx), 'reference_packet_accepted')

    def mut(**kw):
        pk = dict(base)
        pk['claims'] = dict(base['claims'])
        pk['face_coeff_normalized'] = dict(base['face_coeff_normalized'])
        for k, v in kw.items():
            if k.startswith('claims.'):
                pk['claims'][k[7:]] = v
            elif k.startswith('fc.'):
                pk['face_coeff_normalized'][k[3:]] = v
            else:
                pk[k] = v
        return lambda: validate(pk, ctx)

    ok = [('reference packet', lambda: validate(base, ctx))]
    control('missing_incoming_stars', [('anchor star only', mut(stars_R=2), 'incident stars'),
                                       ('J from one star', mut(J_over_tau=F(8)), 'per-site sum')], ok)
    control('full_original_wilson_cover', [('R={0}', mut(cover=[(0, 0, 0)]), 'cover')], ok)
    control('wrong_delta_alpha_hbar_clock', [('normalized units', mut(B_over_tau=F(51)), 'clock or unit mixing'),
                                             ('clock label', mut(clock_units='G=H'), 'clock or unit mixing')], ok)
    control('first_order_mean_charged', [('first order dropped', mut(first_order_charged=False),
                                          'first-order mean not charged')], ok)
    control('tau_scaling_exponent', [('square root', mut(scaling_exponent=F(1, 2)), 'tau scaling exponent')], ok)
    control('changed_model_relabelled', [('R2 cap as 10^-8', mut(tau=F(7, 725000000)), 'changed model relabelled')], ok)
    control('coherent_evidence_tampering', [('rehashed contract', mut(contract_sha256='0' * 64), 'contract hash'),
                                            ('retargeted D', mut(D_ii=d_ii - F(1, 10 ** 20)), 'D_ii below')], ok)
    control('insufficient_verdict_retained', [('tier i dropped', mut(tiers_reported=['ii']), 'insufficient tier')], ok)
    control('exact_arithmetic_admission', [('float D', mut(D_ii=float(d_ii)), 'exact arithmetic')], ok)
    control('root_n_misuse', [('root-sum-square eps', mut(combine='rss'), 'root-N or non-linear')], ok)
    control('no_priority_or_continuum_claim',
            [('continuum', mut(**{'claims.continuum_claim': True}), 'forbidden claim continuum_claim'),
             ('weak', mut(**{'claims.weak_coupling_claim': True}), 'forbidden claim weak_coupling_claim'),
             ('shift', mut(**{'claims.resolved_interaction_shift': True}), 'forbidden claim resolved_interaction_shift'),
             ('priority', mut(**{'claims.scientific_priority_verified': True}), 'forbidden claim scientific_priority')], ok)
    control('uniform_triple_in_box', [('triple tau/3', mut(selected_over_alpha=F(1, 3)), 'uniform triple'),
                                      ('tau=4', mut(tau=F(4), model_cap=F(4)), 'uniform triple')], ok)
    control('selected_reference_not_haar', [('strip reference', mut(reference='selected_strip'), 'selected reference mixed'),
                                            ('AQ2 98 budget', mut(reset_over_tau=F(98)), 'selected reference mixed')], ok)
    control('reference_route_declared', [('route A', mut(route='A'), 'reference route')], ok)
    control('per_site_sum_recomputed', [('J=28', mut(J_over_tau=F(28)), 'per-site sum')], ok)
    control('reset_budget_recomputed', [('charged once per group', mut(reset_over_tau=F(51)), 'reset budget'),
                                        ('no gap six', mut(eps_R_over_tau=F(102)), 'Haar gap six')], ok)
    control('selected_incidence_count', [('one group', mut(singles_R=1), 'selected incidence'),
                                         ('three faces', mut(selected_faces_R=3), 'selected incidence')], ok)
    control('first_order_faces_uniform', [('49 zero-selected', mut(faces_per_factor=49), 'selected faces omitted'),
                                          ('96 as exact', mut(faces_per_factor=96), 'four-anchor bound'),
                                          ('84 asserted', mut(faces_per_factor=84), 'count not derived')],
            ok + [('96 labelled bound', mut(faces_per_factor=96, faces_per_factor_label='bound'))])
    control('uniform_label_strong_coupling', [('weak', mut(label='uniform SU(2) at weak coupling, fixed spacing'), 'label'),
                                              ('continuum', mut(label='uniform continuum SU(2), fixed spacing'), 'label')], ok)
    control('am2_gap_reuse_justified', [('J0 below J', mut(J0=F(28, 10 ** 8) + F(1, 10 ** 9)), 'J_0 below J'),
                                        ('no contraction', mut(Gp_R=F(10 ** 7)), 'contraction fails')], ok)
    control('j0_resolution_declared', [('old J0', mut(J0=F(7, 25000000)), 'old J_0')], ok)
    control('uniform_sign_convention', [('selected +tau/3', mut(**{'fc.selected': F(1, 3)}), 'uniform sign convention'),
                                        ('selected tau/24 normalized', mut(**{'fc.selected': F(-1, 24)}),
                                         'uniform sign convention')], ok)
    control('tier_mixing_rejected', [('exact t1 with crude t', mut(t_rule='crude'), 'tier mixing')], ok)
    parity_sel = {(f['base'], f['orient']): f['selected'] for f in faces_c2}
    untied = lambda f, tau: F(-1, 15) if parity_sel.get(f) else -tau / 3
    control('uniform_kappa_tied_to_tau',
            [('fixed kappa', lambda: uniform_flip_ok(untied, fkeys, parity, (tau_cap,)), 'kappa not tied'),
             ('packet flag', mut(kappa_tied_to_tau=False), 'kappa not tied')],
            ok + [('tied', lambda: uniform_flip_ok(uniform, fkeys, parity, (tau_cap,)))])
    control('route_b_no_double_count', [('selected in stars', mut(star_faces=24), 'double count')], ok)
    control('incidence_table_itemized', [('asserted totals', mut(incidence_table=[]), 'incidence table missing'),
                                         ('table short', mut(incidence_table=base['incidence_table'][:-1]),
                                          'incidence table does not sum')], ok)
    not_impl = {
        'vector_versus_scalar_centering': 'preregistration observable centering is none; applies to AX2 windows',
        'reverse_premise_isolation': 'concerns producer inventories; checked at post-comparison review',
    }
    for name in ERROR_TERMS:
        if name not in base['error_terms']:
            raise CheckFailure('ledger')
    control('error_terms_itemized', [('ledger short', mut(error_terms=list(ERROR_TERMS[:-1])), 'error term missing')], ok)

    ids = set(con['controls'])
    done = {row['id'] for row in CHECKS if row.get('kind') == 'control'}
    missing = sorted(ids - done)
    need(set(missing) <= {'vector_versus_scalar_centering', 'reverse_premise_isolation'}, 'contract_controls_covered',
         implemented=len(ids & done), of=len(ids), deferred=missing)

    def tier_json(rows):
        return {k: {kk: q(vv) for kk, vv in v.items()} for k, v in rows.items()}

    return {
        'loop': 'AX1', 'stage': 'pre_comparison', 'reviewer': 'skeptic (model agent, correlated ancestry)',
        'human_author': 'Hruday N M (BUNZEEY)', 'contract_sha256': c_sha, 'contract_frozen_at': con['frozen_at'],
        'model': 'AQ_uniform_routeB: ' + LABEL + '; Haar reference; whole stars plus single-factor selected groups; '
                 'both signs |tau|<=10^-8; centered whole-star boxes N>=2; cover R={0,e_z}',
        'dictionary': {'tau': '96/g^4', 'g4_at_cap': q(g4), 'selected_over_alpha': 'tau/24',
                       'normalized_face_coefficient': '-tau/3 (every face, I1.5)',
                       'negative_tau': 'no real-g preimage; U_E image of +|tau| in open boxes'},
        'route_b': {'star_faces': 21, 'star_norm_over_tau': '7', 'single_faces': 3, 'single_norm_over_tau': '1',
                    'J_prime_over_tau': '29', 'max_support': 4, 'termination_order': 8},
        'contraction': {'J0_prime': q(j0p), 'J0p_times_148_over_7': q(c1r), 'two_J0p_times_352': q(c2r),
                        'J0_old': q(j0_old), 'R2_cap': '7/725000000', 'max_abs_tau_self_map': q(slack_tau),
                        'exp_one_eighth_upper': q(e8)},
        'reset': {'omega_hR_over_tau': '102', 'eps_R_over_tau': '17', 'sqrt_control_upper': q(sq),
                  'tighter_labelled_over_tau': '100', 'aq2_98_is_selected_reference': True},
        'aq_reinstantiation': {'C_F_over_tau_per_factor': '58', 'Phi_F_crude_over_tau': '2349',
                               'Phi_F_per_pair_over_tau': '567', 'convolution_constant': '224 (unchanged)',
                               'variance_floor': '61999/250000 verbatim once 2sqrt(17|tau|)<=1/500'},
        'counts': {'per_factor_exact': 52, 'per_factor_omitted': 49, 'per_factor_selected': 3,
                   'per_factor_bound': 96, 'faces_meeting_R_exact': 88, 'faces_meeting_R_omitted': 82,
                   'faces_meeting_R_selected': 6, 'faces_meeting_R_bound': 168, 'faces_inside_R': 16,
                   'faces_inside_R_selected': 6, 'straddling': 72, 'stars_meeting_R': 7,
                   'single_groups_meeting_R': 2, 'faces_charged_in_B': 153, 'owner_sets_through_site': 16,
                   'box_N1': n1, 'B_N_over_tau': '51/8', 'k_prime_over_tau': '51/4'},
        'incidence_table': tab,
        'first_order': {'face_energy_normalized': 24, 'amplitude': 'tau/72', 'per_face_norm': '|tau|/144',
                        'omega_W_first_order': '+tau/144', 'plus': q(om1 * tau_cap), 'minus': q(-om1 * tau_cap),
                        'flip_counts_box2': {'one_link': par_counts[0], 'three_links': par_counts[1]}},
        'tiers': {'+': tier_json(out_tiers['+']), '-': tier_json(out_tiers['-'])},
        'headline': {'D_prime_ii': q(d_ii), 'D_prime_ii_bound96': q(plus['D_ii_bound96']['D_fwd']),
                     'D_prime_i': q(d_i), 'target': q(target), 'D_prime_ii_meets_target': True,
                     'D_prime_i_meets_target': False},
        'ax2_feasibility': {'pi_lo': q(pi_lo), 'pi_hi': q(pi_hi), 'threshold_bracket': ['41883/10^11', '41884/10^11'],
                            'contract_note_4.19e-7_feasible': False},
        'error_terms': {
            'am2_remainder': '352 J t inside t<=t_1/(1-352J), J=29|tau|',
            'two_creation': 't^2 in eps; first order nonzero in route B (single-factor c^(1)_{0}, c^(1)_{e_z})',
            'straddling': 'inside 2t (every I meeting R, norm ||c_I||)',
            'density': 'Tr_out|delta><delta| inside 2eps(1+eps)/(1+eps^2)',
            'onsite_cutoff_vector': 'not_applicable as an additive term: uniform gap 1/2 moves the vector (AV1 section 7)',
            'arithmetic': 'not_applicable: exact rationals; purification form bracketed [2eps-eps^3,2eps]'},
        'claims': dict(CLAIMS, uniform_wilson_claim_scope='fixed-spacing uniform model as labelled only'),
        'deferred_controls': not_impl,
        'checks': CHECKS,
        'previews': {'D_ii_52': preview(d_ii), 'D_ii_96': preview(plus['D_ii_bound96']['D_fwd']),
                     'D_ii_grouped': preview(plus['D_ii_grouped_labelled']['D_fwd']),
                     'D_ii_R88': preview(plus['D_ii_R88_labelled']['D_fwd']), 'D_i': preview(d_i),
                     'ax2_radius_with_D_ii_52': preview(e_prev), 'ax2_margin': preview(F(1, 10 ** 6) / e_prev),
                     'target_over_D_ii': preview(target / d_ii), 'sqrt_control': preview(sq),
                     'scaling_ratios': {k: preview(v) for k, v in ratios.items()}},
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
    print(json.dumps({'checks': len(result['checks']), 'D_prime_ii': result['previews']['D_ii_52'],
                      'D_prime_ii_96': result['previews']['D_ii_96'], 'D_prime_i': result['previews']['D_i']}))


if __name__ == '__main__':
    main()
