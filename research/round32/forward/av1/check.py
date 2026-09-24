#!/usr/bin/env python3
"""AV1 forward producer: exact checks for the product-ordering local state lemma.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production.

Standard library only (fractions, hashlib, json, argparse, re, math.isqrt).
Every admission Boolean is decided in exact Fraction arithmetic; decimal
strings are truncated previews.  Conditions raise AdmissionError explicitly
(never `assert`), so every check stays active under `python -O`.

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from math import factorial, isqrt
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
CONTRACT_REL = 'research/round32/contracts/av1.json'
CONTRACT_SHA256 = 'c7018519188b953e48e56715a72c90491389e42243ef691cb59dc5b038e91e40'


class AdmissionError(Exception):
    """An admission condition failed or a damaging mutation was accepted."""


def require(condition, message):
    if not condition:
        raise AdmissionError(message)


CHECKS = []


def check(identity, condition, **details):
    require(condition, 'failed check ' + identity)
    require(all(c['id'] != identity for c in CHECKS), 'duplicate check id ' + identity)
    entry = {'id': identity, 'passed': True}
    entry.update(details)
    CHECKS.append(entry)


def rejected(mutation, label):
    """Run a damaging mutation; it must raise AdmissionError."""
    try:
        mutation()
    except AdmissionError:
        return label
    raise AdmissionError('damaging mutation accepted: ' + label)


def rat(value):
    """Exact rational input only: int, Fraction or an integer/ratio string."""
    if isinstance(value, bool) or isinstance(value, float):
        raise AdmissionError('non-exact input rejected: ' + repr(value))
    if isinstance(value, (int, Q)):
        return Q(value)
    if isinstance(value, str) and re.fullmatch(r'-?\d+(/\d+)?', value):
        num, _, den = value.partition('/')
        if den and int(den) == 0:
            raise AdmissionError('zero denominator rejected')
        return Q(int(num), int(den) if den else 1)
    raise AdmissionError('malformed rational rejected: ' + repr(value))


def s(q):
    return str(Q(q))


def dec(q, digits=12):
    """Truncated scientific decimal preview of an exact rational (not admission)."""
    q = Q(q)
    if q == 0:
        return '0'
    sign = '-' if q < 0 else ''
    q = abs(q)
    e = 0
    while q >= Q(10) ** (e + 1):
        e += 1
    while q < Q(10) ** e:
        e -= 1
    scaled = q / Q(10) ** (e - digits + 1)
    m = str(scaled.numerator // scaled.denominator)
    return sign + m[0] + '.' + m[1:] + 'e' + str(e)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def sqrt_up(n, scale=10 ** 9):
    """Directed rational upper bound of sqrt(n) for a nonnegative rational n."""
    n = Q(n)
    k = isqrt(n.numerator * scale * scale // n.denominator)
    while Q(k, scale) ** 2 < n:
        k += 1
    up = Q(k, scale)
    require(up * up >= n and (up - Q(1, scale)) ** 2 < n, 'sqrt bracket')
    return up


def exact_sqrt(q):
    q = Q(q)
    a, b = isqrt(q.numerator), isqrt(q.denominator)
    require(a * a == q.numerator and b * b == q.denominator, 'not a rational square')
    return Q(a, b)


# ---------------------------------------------------------------------------
# Contract: every target, reference and candidate value is read from it.
# ---------------------------------------------------------------------------
WORDS = {'seven': 7}


def load_contract():
    raw = (BASE / 'inputs' / CONTRACT_REL).read_bytes()
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen AV1 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'AV1' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return c, digest


def match(pattern, text, label):
    m = re.search(pattern, text)
    require(m is not None, 'contract text not parsed: ' + label)
    return m


def contract_values(c):
    p = c['parameters']
    pre = c['preregistration']
    req = c['required']
    v = {}
    v['tau_cap'] = rat(p['tau_cap'])
    v['signs'] = list(p['signs'])
    require(v['signs'] == ['+', '-'], 'both signs required')
    v['triple'] = [rat(x) for x in p['selected_coefficients_over_alpha']]
    require(v['triple'] == [0, 0, 0], 'zero-selected triple required')
    am2 = p['am2_constants']
    v['R'] = rat(am2['anchored_radius_R'])
    v['J0'] = rat(am2['J0'])
    v['G_R_upper'] = rat(am2['G_at_R_upper'])
    v['Gp_R_upper'] = rat(am2['G_prime_at_R_upper'])
    v['nested_order'] = int(am2['nested_order_termination'])
    v['J_coefficient'] = int(match(r'^<=(\d+)\|tau\|$', am2['per_site_sum_J'], 'J').group(1))
    g = match(r'^(\d+)\*exp\((\d+)t\)\*\(1\+(\d+)t\)$', am2['majorant_G'], 'G')
    v['G_prefactor'], v['G_rate'], v['G_linear'] = (int(g.group(i)) for i in (1, 2, 3))
    ref = p['reference_moments']
    v['omega0_W'] = rat(ref['omega_0(W)'])
    v['omega0_W2'] = rat(ref['omega_0(W^2)'])
    f = match(r'^(\d+) \(four j=1/2 links, Casimir (\d+)/(\d+), onsite factor (\d+)\); alpha units (\d+)$',
              p['normalized_face_energy'], 'face energy')
    v['face_energy'] = int(f.group(1))
    v['casimir_half'] = Q(int(f.group(2)), int(f.group(3)))
    v['onsite_factor'] = int(f.group(4))
    v['face_energy_alpha'] = int(f.group(5))
    cv = match(r'R=\{0,e_z\}: (\d+) links, (\d+) original endpoints, (\w+) incident anchors R-S', p['cover'], 'cover')
    v['cover_links'], v['cover_endpoints'] = int(cv.group(1)), int(cv.group(2))
    v['incident_anchors'] = WORDS[cv.group(3)]
    ev = p['evaluation_points']
    e1 = match(r'^tau=\+1/10\^(\d+)$', ev[0], 'eval+')
    e2 = match(r'^tau=-1/10\^(\d+)$', ev[1], 'eval-')
    e3 = match(r'^tau=\+1/10\^(\d+) \(scaling control only\)$', ev[2], 'eval scaling')
    require(Q(1, 10 ** int(e1.group(1))) == v['tau_cap'] and Q(1, 10 ** int(e2.group(1))) == v['tau_cap'],
            'evaluation points differ from the cap')
    v['tau_scaling'] = Q(1, 10 ** int(e3.group(1)))
    t = pre['target']
    require(t['quantity'] == 'D_ii' and t['comparator'] == '<=', 'target quantity/comparator')
    v['target'] = rat(t['value'])
    m9 = match(r'Test D_ii<=(\d+)/10\^(\d+) \(the value AV2 needs\) and also report against 10\^-(\d+)\.', req[8], 'item 9')
    require(Q(int(m9.group(1)), 10 ** int(m9.group(2))) == v['target'], 'item 9 target differs from preregistered target')
    v['secondary'] = Q(1, 10 ** int(m9.group(3)))
    m11 = match(r'derive the counts (\d+) \(omitted faces per factor\), (\d+) \(owner sets per factor\), '
                r'(\d+) \(faces meeting R\) and (\d+) \(faces inside R\)', req[10], 'item 11')
    v['cand_faces'], v['cand_owner_sets'], v['cand_meet_R'], v['cand_inside_R'] = (int(m11.group(i)) for i in (1, 2, 3, 4))
    m5 = match(r'(\d+) is accepted only as a labelled bound', req[4], 'item 5 bound')
    v['labelled_bound'] = int(m5.group(1))
    m5c = match(r'candidate (\d+)\|tau\|/(\d+)\)', req[4], 'item 5 candidate')
    v['cand_t1_num'], v['cand_t1_den'] = int(m5c.group(1)), int(m5c.group(2))
    m5r = match(r't<=t_1/\(1-(\d+)J\)', req[4], 'item 5 remainder')
    v['self_consistent_coefficient'] = int(m5r.group(1))
    m4 = match(r't<=J_0 G\(R\)<(\d+)/(\d+)', req[3], 'item 4')
    v['tier_i_cap_string'] = Q(int(m4.group(1)), int(m4.group(2)))
    model = c['model']
    v['phi_denominator'] = int(match(r'phi_b=-\(tau/(\d+)\) sum_f W_f', model, 'phi_b').group(1))
    mo = match(r'(\d+) omitted anchored faces per factor with coefficient alpha\*tau/(\d+)', model, 'faces')
    v['omitted_per_anchor'], v['face_coefficient_denominator'] = int(mo.group(1)), int(mo.group(2))
    v['delta_denominator'] = int(match(r'normalized units delta=alpha/(\d+)', model, 'delta').group(1))
    av2 = match(r'2\(D\+D\^2\)\+(\d+)\*10\^-(\d+)/pi<=10\^-(\d+) requires D<=(\d+)\.(\d+)\*10\^-(\d+)',
                c['new_control_semantics']['av2_feasibility_threshold'], 'av2 threshold')
    v['av2_k_num'], v['av2_k_exp'], v['av2_goal_exp'] = int(av2.group(1)), int(av2.group(2)), int(av2.group(3))
    v['av2_threshold'] = Q(int(av2.group(4) + av2.group(5)), 10 ** (len(av2.group(5)) + int(av2.group(6))))
    v['model_id'] = pre['model_id']
    v['reference_route'] = pre['observable']['reference_route']
    v['reference_values'] = pre['observable']['reference_value_exact']
    v['state_provenance'] = pre['state_provenance']
    v['controls'] = list(c['controls'])
    v['error_terms'] = list(pre['error_terms_itemized'])
    v['shared_premises'] = list(c['shared_premises'])
    v['forward_additional'] = list(c['forward_additional_premises'])
    return v


# ---------------------------------------------------------------------------
# Fine-lattice geometry, the I1 21-class table and translation covariance.
# ---------------------------------------------------------------------------
E = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIENT = {'xy': (0, 1), 'xz': (0, 2), 'yz': (1, 2)}
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
COVER_R = (ORIGIN, EZ)


def add(p, q):
    return tuple(a + b for a, b in zip(p, q))


def sub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    return ((p, a), (add(p, E[a]), c), (add(p, E[c]), a), (p, c))


def face_support(p, a, c):
    return frozenset(owner(link[0]) for link in face_links(p, a, c))


def is_selected(p, a, c):
    return (a, c) == (0, 1) and p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)


# Explicit encoding of the I1 table (research/round21/forward/i1/report.md, Section 3).
I1_TABLE = (
    {'orientation': 'xy', 'r': (0, 1, 2), 's': (0,), 'support': ((0, 0, 0),), 'role': 'selected'},
    {'orientation': 'xy', 'r': (0, 1, 2), 's': (1,), 'support': ((0, 0, 0), (0, 1, 0)), 'role': 'omitted'},
    {'orientation': 'xy', 'r': (3,), 's': (0,), 'support': ((0, 0, 0), (1, 0, 0)), 'role': 'omitted'},
    {'orientation': 'xy', 'r': (3,), 's': (1,), 'support': ((0, 0, 0), (1, 0, 0), (0, 1, 0)), 'role': 'omitted'},
    {'orientation': 'xz', 'r': (0, 1, 2), 's': (0, 1), 'support': ((0, 0, 0), (0, 0, 1)), 'role': 'omitted'},
    {'orientation': 'xz', 'r': (3,), 's': (0, 1), 'support': ((0, 0, 0), (1, 0, 0), (0, 0, 1)), 'role': 'omitted'},
    {'orientation': 'yz', 'r': (0, 1, 2, 3), 's': (0,), 'support': ((0, 0, 0), (0, 0, 1)), 'role': 'omitted'},
    {'orientation': 'yz', 'r': (0, 1, 2, 3), 's': (1,), 'support': ((0, 0, 0), (0, 1, 0), (0, 0, 1)), 'role': 'omitted'},
)


def expand_classes(table, role='omitted'):
    out = []
    for row in table:
        if row['role'] != role:
            continue
        for r in row['r']:
            for q in row['s']:
                out.append((row['orientation'], r, q, frozenset(row['support'])))
    return out


def class_base(anchor, cls):
    orient, r, q, _ = cls
    return (4 * anchor[0] + r, 2 * anchor[1] + q, anchor[2]), ORIENT[orient]


def faces_containing(u, classes):
    """Translation covariance: face (b,k) contains u iff b = u - d with d in K_k."""
    out = []
    for cls in classes:
        for d in sorted(cls[3]):
            b = sub(u, d)
            out.append((b, cls))
    return out


def owner_set(face):
    b, cls = face
    return frozenset(add(b, d) for d in cls[3])


def face_link_set(face):
    base, (a, c) = class_base(*face)
    return frozenset(face_links(base, a, c))


def derive_counts(table):
    classes = expand_classes(table)
    at0 = faces_containing(ORIGIN, classes)
    sets0 = {}
    for f in at0:
        sets0[owner_set(f)] = sets0.get(owner_set(f), 0) + 1
    meet = {}
    for u in COVER_R:
        for f in faces_containing(u, classes):
            meet[(f[0], f[1][:3])] = f
    rset = frozenset(COVER_R)
    inside = [f for f in meet.values() if owner_set(f) <= rset]
    contain = [f for f in meet.values() if rset <= owner_set(f)]
    meet_sets = {}
    for f in meet.values():
        meet_sets[owner_set(f)] = meet_sets.get(owner_set(f), 0) + 1
    return {'classes': len(classes), 'faces_per_factor': len(at0), 'owner_sets_per_factor': len(sets0),
            'multiplicities': sorted(sets0.values()), 'sets_at_origin': sets0,
            'faces_meeting_R': len(meet), 'faces_inside_R': len(inside), 'faces_containing_R': len(contain),
            'owner_sets_meeting_R': len(meet_sets), 'meet_faces': list(meet.values()), 'meet_sets': meet_sets}


def brute_force_faces(region_coarse=2):
    """Independent fine-lattice enumeration without the class table."""
    n = region_coarse
    faces = []
    for x in range(-4 * n, 4 * n + 4):
        for y in range(-2 * n, 2 * n + 2):
            for z in range(-n, n + 1):
                p = (x, y, z)
                for a, c in ((0, 1), (0, 2), (1, 2)):
                    if is_selected(p, a, c):
                        continue
                    faces.append((p, a, c, face_support(p, a, c), owner(p)))
    return faces


def coarse_box(N):
    rng = range(-N, N + 1)
    return frozenset((x, y, z) for x in rng for y in rng for z in rng)


def box_retained(N, classes):
    box = coarse_box(N)
    anchors = [b for b in sorted(box) if all(add(b, d) in box for d in S_STAR)]
    return box, [(b, cls) for b in anchors for cls in classes]


# ---------------------------------------------------------------------------
# Exact SU(2) Haar moments (Weyl integration formula; pi cancels exactly).
# ---------------------------------------------------------------------------
def cos_integral_over_pi(n):
    """(1/pi) * integral_0^pi cos^n(theta) d theta, exactly."""
    if n % 2:
        return Q(0)
    num = 1
    den = 1
    for k in range(1, n + 1):
        if k % 2:
            num *= k
        else:
            den *= k
    return Q(num, den)


def haar_moment_W(n):
    """E[W^n] for W=(1/2)Tr U=cos(theta), density (2/pi) sin^2(theta) on [0,pi]."""
    return 2 * (cos_integral_over_pi(n) - cos_integral_over_pi(n + 2))


def atan_inverse_bracket(k, terms=24):
    """Consecutive partial sums of the alternating arctan(1/k) series bracket its value."""
    total = Q(0)
    previous = Q(0)
    for j in range(terms):
        previous = total
        term = Q(1, (2 * j + 1) * k ** (2 * j + 1))
        total = total + term if j % 2 == 0 else total - term
    return min(previous, total), max(previous, total)


def pi_bracket(denominator=10 ** 30):
    """Machin: pi=16 atan(1/5)-4 atan(1/239), rounded outward to a fixed denominator."""
    a5 = atan_inverse_bracket(5)
    a239 = atan_inverse_bracket(239)
    lo = 16 * a5[0] - 4 * a239[1]
    hi = 16 * a5[1] - 4 * a239[0]
    lo = Q((lo.numerator * denominator) // lo.denominator, denominator)
    hi = Q(-((-hi.numerator * denominator) // hi.denominator), denominator)
    require(lo < hi and hi - lo < Q(1, 10 ** 25) and Q(314159, 100000) < lo and hi < Q(314160, 100000), 'pi bracket')
    return lo, hi


# ---------------------------------------------------------------------------
# Tiers: every bound names its tier; mixing is rejected.
# ---------------------------------------------------------------------------
def eps_of(t):
    return 2 * t + t * t


def D_of(eps):
    return 2 * eps * (1 + eps) / (1 + eps * eps)


def assemble(tier, components):
    """components: list of (name, tier_label, value); all labels must equal the tier."""
    for name, label, value in components:
        require(label == tier, 'tier mixing rejected: ' + name + ' is tier ' + label + ' inside tier ' + tier)
        require(isinstance(value, Q), 'non-exact component ' + name)
    names = [n for n, _, _ in components]
    if tier == 'ii':
        require('self_consistent_t' in names and 'am2_remainder' in names, 'refined t without self-consistent inequality')
        remainder = [v for n, _, v in components if n == 'am2_remainder'][0]
        require(remainder > 0, 'AM2 remainder set to zero')
    t = [v for n, _, v in components if n in ('t', 'self_consistent_t')][0]
    eps = eps_of(t)
    return {'t': t, 'eps': eps, 'D': D_of(eps)}


def tier_i(tau, V, iterate=False):
    J = V['J_coefficient'] * abs(tau)
    t = J * V['G_R_upper']
    require(t < V['R'], 'tier (i) self-map radius')
    comps = [('J', 'i', J), ('t', 'i', t)]
    out = {'tier': 'i', 'form': 'one-step t<=J*G(R)', 'tau': tau, 'J': J}
    if iterate:
        # e^{8t}<=1/(1-8t) for 0<=8t<1 (from e^{-x}>=1-x): directed upper bound.
        t2 = J * V['G_prefactor'] * (1 + V['G_linear'] * t) / (1 - V['G_rate'] * t)
        require(0 < t2 <= t, 'iterated tier (i) must not exceed one-step bound')
        comps = [('J', 'i', J), ('t', 'i', t2)]
        out['form'] = 'iterated t<=J*16*(1+10*t_i)/(1-8*t_i)'
    out.update(assemble('i', comps))
    return out


def tier_ii(tau, V, t1_per_tau, form, remainder='contract'):
    J = V['J_coefficient'] * abs(tau)
    t1 = t1_per_tau * abs(tau)
    ti = tier_i(tau, V)['t']
    if remainder == 'contract':
        L = Q(V['self_consistent_coefficient'])
        require(L == V['Gp_R_upper'], 'self-consistent coefficient must be the AM2 G\'(R) bound')
        t = t1 / (1 - L * J)
        rem = L * J * t
    else:
        # sharper directed form: G(t)-16<=288 t/(1-8t) and t<=t_i a priori.
        t = t1 / (1 - 288 * J / (1 - 8 * ti))
        rem = 288 * J * t / (1 - 8 * ti)
    require(t <= ti and t < V['R'], 'tier (ii) t must stay inside the admitted tier (i) ball')
    require(t1 < t and t == t1 + rem, 'self-consistent identity t=t1+remainder')
    comps = [('t1', 'ii', t1), ('am2_remainder', 'ii', rem), ('self_consistent_t', 'ii', t)]
    out = {'tier': 'ii', 'form': form, 'remainder_form': remainder, 'tau': tau, 'J': J, 't1': t1, 'remainder': rem}
    out.update(assemble('ii', comps))
    return out


def tier_record(x):
    keys = ('t', 'eps', 'D', 'J', 't1', 'remainder')
    rec = {k: s(x[k]) for k in keys if k in x}
    rec.update({'tier': x['tier'], 'form': x['form'], 'tau': s(x['tau']),
                'D_decimal_preview': dec(x['D']), 'D_over_2': s(x['D'] / 2),
                'two_creation_term_t2': s(x['t'] ** 2),
                'density_part_of_D': s(2 * x['eps'] ** 2 / (1 + x['eps'] ** 2))})
    if 'remainder_form' in x:
        rec['remainder_form'] = x['remainder_form']
    return rec


# ---------------------------------------------------------------------------
# Creation-algebra fixtures on qubit sites (vacuum 0, excited 1).
# ---------------------------------------------------------------------------
def c_hat(vec, support, coeff):
    out = {}
    for bits, amp in vec.items():
        if all(bits[i] == 0 for i in support):
            nb = list(bits)
            for i in support:
                nb[i] = 1
            nb = tuple(nb)
            out[nb] = out.get(nb, 0) + coeff * amp
    return {k: v for k, v in out.items() if v != 0}


def vadd(u, v, a=1):
    out = dict(u)
    for k, x in v.items():
        out[k] = out.get(k, 0) + a * x
    return {k: x for k, x in out.items() if x != 0}


def one_minus(vec, support, coeff):
    return vadd(vec, c_hat(vec, support, coeff), -1)


def vacuum(n):
    return {(0,) * n: Q(1)}


def product_state(n, creations):
    vec = vacuum(n)
    for support, coeff in creations:
        vec = one_minus(vec, support, coeff)
    return vec


def inner(u, v):
    return sum((u[k] * v[k] for k in u if k in v), Q(0))


def norm2(u):
    return inner(u, u)


def anchored_norm(n, creations):
    return max(sum((abs(c) for I, c in creations if u in I), Q(0)) for u in range(n))


def reduced(vec, keep):
    """Partial trace keeping the site indices in `keep` (real coefficients)."""
    rho = {}
    groups = {}
    for bits, amp in vec.items():
        kept = tuple(bits[i] for i in keep)
        rest = tuple(bits[i] for i in range(len(bits)) if i not in keep)
        groups.setdefault(rest, []).append((kept, amp))
    for rest, items in groups.items():
        for a, x in items:
            for b, y in items:
                rho[(a, b)] = rho.get((a, b), 0) + x * y
    return {k: v for k, v in rho.items() if v != 0}


def mscale(m, a):
    return {k: a * v for k, v in m.items() if a * v != 0}


def madd(m1, m2, a=1):
    out = dict(m1)
    for k, v in m2.items():
        out[k] = out.get(k, 0) + a * v
    return {k: v for k, v in out.items() if v != 0}


def mtrace(m):
    return sum((v for (a, b), v in m.items() if a == b), Q(0))


def expect(m, obs):
    """Tr(m obs) for real matrices stored as {(row, col): value}."""
    return sum((v * obs.get((b, a), 0) for (a, b), v in m.items()), Q(0))


def split_analysis(n, R, creations):
    """Product ordering psi=psi_out+delta with the creations meeting R last."""
    meet = [(I, c) for I, c in creations if set(I) & set(R)]
    far = [(I, c) for I, c in creations if not set(I) & set(R)]
    psi = product_state(n, creations)
    psi_other_order = product_state(n, list(reversed(creations)))
    psi_out = product_state(n, far)
    delta = vadd(psi, psi_out, -1)
    # explicit expansion: -sum chat_I psi_out + sum over disjoint pairs meeting distinct sites of R
    explicit = {}
    for I, c in meet:
        explicit = vadd(explicit, c_hat(psi_out, I, c), -1)
    pairs = 0
    for i, (I, c) in enumerate(meet):
        for J, d in meet[i + 1:]:
            if not set(I) & set(J):
                explicit = vadd(explicit, c_hat(c_hat(psi_out, J, d), I, c))
                pairs += 1
    outside = [i for i in range(n) if i not in R]
    n2 = norm2(psi_out)
    d2 = norm2(delta)
    # phi_out and xi = (1 (x) <phi_out|) delta on H_R
    phi_out = {}
    for bits, amp in psi_out.items():
        require(all(bits[i] == 0 for i in R), 'psi_out must be Omega_R (x) phi_out')
        phi_out[tuple(bits[i] for i in outside)] = amp
    xi = {}
    for bits, amp in delta.items():
        o = tuple(bits[i] for i in outside)
        if o in phi_out:
            r = tuple(bits[i] for i in R)
            xi[r] = xi.get(r, 0) + phi_out[o] * amp
    xi = {k: v for k, v in xi.items() if v != 0}
    omega_r = tuple(0 for _ in R)
    sigma = reduced(delta, R)
    rho_direct = mscale(reduced(psi, R), 1 / norm2(psi))
    cross = {}
    for r, v in xi.items():
        cross[(omega_r, r)] = cross.get((omega_r, r), 0) + v
        cross[(r, omega_r)] = cross.get((r, omega_r), 0) + v
    numer = madd(madd({(omega_r, omega_r): n2}, cross), sigma)
    rho_formula = mscale(numer, 1 / (n2 + d2))
    t = anchored_norm(n, creations)
    eps = (1 + t) ** len(R) - 1
    return {'psi': psi, 'psi_other_order': psi_other_order, 'psi_out': psi_out, 'delta': delta,
            'explicit': explicit, 'pairs': pairs, 'n2': n2, 'd2': d2, 'xi': xi, 'sigma': sigma,
            'cross': cross, 'rho': rho_direct, 'rho_formula': rho_formula, 't': t, 'eps': eps,
            'omega_r': omega_r, 'meet': meet, 'far': far}


def trace_bound_certificate(an):
    """Rational verification of ||rho-P_R||_1<=(2||xi||+2d^2)/(n^2+d^2)<=f(e)<=f(eps)."""
    n2, d2, xi2 = an['n2'], an['d2'], norm2(an['xi'])
    require(xi2 <= n2 * d2, 'Cauchy-Schwarz ||xi||<=||phi_out|| ||delta||')
    require(mtrace(an['sigma']) == d2, 'Tr sigma = ||delta||^2')
    require(an['xi'].get(an['omega_r'], 0) == 0, 'xi orthogonal to Omega_R')
    e2 = d2 / n2
    require(e2 <= an['eps'] ** 2, 'e<=eps')
    # f increasing on [0,1+sqrt2]; for eps>=1 the bound f(eps)>=2 is trivially valid.
    require(an['eps'] < 1 or D_of(an['eps']) >= 2, 'monotone region')
    return e2


def poly_add(p, q, a=1):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + a * (q[i] if i < len(q) else 0) for i in range(n)]


def poly_mul(p, q):
    out = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        if x:
            for j, y in enumerate(q):
                out[i + j] += x * y
    return out


def poly_state(n, creations):
    vec = {(0,) * n: [Q(1)]}
    for support, coeff in creations:
        new = dict(vec)
        for bits, amp in vec.items():
            if all(bits[i] == 0 for i in support):
                nb = list(bits)
                for i in support:
                    nb[i] = 1
                nb = tuple(nb)
                new[nb] = poly_add(new.get(nb, [Q(0)]), poly_mul(amp, [Q(0), coeff]), -1)
        vec = new
    return vec


def poly_matrix_element(vec, R, a, b):
    n = len(next(iter(vec)))
    total = [Q(0)]
    for bits, amp in vec.items():
        if tuple(bits[i] for i in R) != a:
            continue
        partner = list(bits)
        for k, i in enumerate(R):
            partner[i] = b[k]
        partner = tuple(partner)
        if partner in vec:
            total = poly_add(total, poly_mul(amp, vec[partner]))
    return total + [Q(0)] * 3


# ---------------------------------------------------------------------------
# Main computation.
# ---------------------------------------------------------------------------
def compute(check_sha):
    c, contract_digest = load_contract()
    V = contract_values(c)
    tau_cap = V['tau_cap']
    taus = {'+': tau_cap, '-': -tau_cap}
    check('contract_snapshot_sha256', contract_digest == CONTRACT_SHA256,
          contract_sha256=contract_digest, target_read_from_contract=s(V['target']),
          secondary_read_from_contract=s(V['secondary']),
          reference_moments_read_from_contract=[s(V['omega0_W']), s(V['omega0_W2'])])

    # -------------------- item 1: AM2 constants re-evaluated --------------------
    R = V['R']
    x = V['G_rate'] * R  # 8R = 1/8
    lower = sum((x ** k / factorial(k) for k in range(13)), Q(0))
    tail = x ** 13 / factorial(13) / (1 - x / 14)
    exp_upper = lower + tail
    require(exp_upper < Q(8, 7), 'exp(1/8)<8/7')
    G_R = V['G_prefactor'] * Q(8, 7) * (1 + V['G_linear'] * R)
    Gp_R = V['G_prefactor'] * Q(8, 7) * (V['G_rate'] * (1 + V['G_linear'] * R) + V['G_linear'])
    J_cap = V['J_coefficient'] * tau_cap
    Lnum = [16 * 8 ** k * (1 + Q(5 * k, 4)) for k in range(V['nested_order'] + 1)]
    gen_ok = all(Lnum[k] / factorial(k) == 16 * Q(8) ** k / factorial(k) + (160 * Q(8) ** (k - 1) / factorial(k - 1) if k else 0)
                 for k in range(V['nested_order'] + 1))
    # four-qubit termination audit of the inherited nested order (AM2 Section 2)
    size = 16
    Cm = [[0] * size for _ in range(size)]
    Vm = [[0] * size for _ in range(size)]
    for b in range(size):
        Vm[b ^ 15][b] = 1
        for j in range(4):
            if not (b >> j) & 1:
                Cm[b | (1 << j)][b] += 1

    def mm(a, b):
        return [[sum(a[i][k] * b[k][j] for k in range(size)) for j in range(size)] for i in range(size)]
    A = Vm
    for _ in range(V['nested_order']):
        A = [[x1 - y1 for x1, y1 in zip(r1, r2)] for r1, r2 in zip(mm(Cm, A), mm(A, Cm))]
    order8 = A[15][0]
    A9 = [[x1 - y1 for x1, y1 in zip(r1, r2)] for r1, r2 in zip(mm(Cm, A), mm(A, Cm))]
    zero9 = all(x1 == 0 for row in A9 for x1 in row)
    G_R_lower = V['G_prefactor'] * (1 + x) * (1 + V['G_linear'] * R)       # e^x>=1+x
    G_R_exp_dropped = V['G_prefactor'] * (1 + V['G_linear'] * R)          # damaging mutation
    t_probe = Q(1, 10 ** 9)
    remainder_lower = J_cap * V['G_prefactor'] * ((1 + V['G_rate'] * t_probe) * (1 + V['G_linear'] * t_probe) - 1)
    remainder_positive = remainder_lower > 0
    check('am2_fixed_point_constants',
          G_R == V['G_R_upper'] and Gp_R == V['Gp_R_upper'] and J_cap == V['J0'] and V['J0'] * G_R == V['tier_i_cap_string']
          and V['J0'] * G_R < R and 2 * V['J0'] * Gp_R == Q(77, 390625) and 2 * V['J0'] * Gp_R < 1 and gen_ok
          and order8 == factorial(8) and zero9 and remainder_positive
          and G_R_lower <= G_R
          and rejected(lambda: require(G_R_exp_dropped >= G_R_lower, 'G(R) with the exponential dropped is not an upper bound'), 'exp_dropped_from_G')
          and rejected(lambda: require(Q(0) >= remainder_lower, 'remainder J(G(t)-16) set to zero'), 'remainder_zero'),
          R=s(R), J0=s(V['J0']), exp_one_eighth_upper=s(exp_upper), G_R_upper=s(G_R), G_prime_R_upper=s(Gp_R),
          self_map_cap=s(V['J0'] * G_R), exclusion_cap=s(2 * V['J0'] * Gp_R), order_eight_vacuum_coefficient=order8,
          order_nine_zero=zero9, anchored_coefficients=[s(q) for q in Lnum])

    # AQ1 boxes are AM2's family: coarse translations preserve the fine structure.
    fam_ok = True
    for N in (2, 3):
        shift_fine = (4 * N, 2 * N, N)
        for p in [(x1, y1, z1) for x1 in range(-4 * N, 4 * N + 4, 3) for y1 in range(-2 * N, 2 * N + 2) for z1 in (-N, 0, N)]:
            q = add(p, shift_fine)
            fam_ok = fam_ok and owner(q) == add(owner(p), (N, N, N)) and (p[0] % 4, p[1] % 2) == (q[0] % 4, q[1] % 2)
            for a, cc in ((0, 1), (0, 2), (1, 2)):
                fam_ok = fam_ok and is_selected(p, a, cc) == is_selected(q, a, cc)
        box = coarse_box(N)
        stars = [b for b in box if all(add(b, d) in box for d in S_STAR)]
        moved = [add(b, (N, N, N)) for b in stars]
        fam_ok = fam_ok and all(min(add(b, d)) >= 0 for b in moved for d in S_STAR)
    zero_onsite = V['onsite_factor'] == V['delta_denominator'] and V['onsite_factor'] * V['casimir_half'] == 6
    check('aq1_boxes_are_am2_family', fam_ok and zero_onsite,
          statement='Lambda_N=[-N,N]^3 with stars b+S inside is a translate of an I1 complete-factor volume; '
                    'zero-selected onsite h_b=8 sum C_e with Haar vacuum and gap 6>=1',
          onsite_gap_normalized=s(V['onsite_factor'] * V['casimir_half']))

    # -------------------- geometry, cover and stars --------------------
    cover_links = []
    for b in COVER_R:
        for r in range(4):
            for q in range(2):
                tail_pt = (4 * b[0] + r, 2 * b[1] + q, b[2])
                for d in range(3):
                    cover_links.append((tail_pt, d))
    ends = {}
    for (tp, d) in cover_links:
        ends.setdefault(owner(tp), set()).update({tp, add(tp, E[d])})
    endpoints = set().union(*ends.values())
    shared = ends[ORIGIN] & ends[EZ]
    W_links = face_links(ORIGIN, 0, 2)
    W_owners = sorted(owner(l[0]) for l in W_links)
    drawn = len(set(W_links))
    check('full_original_wilson_cover',
          len(set(cover_links)) == V['cover_links'] and len(endpoints) == V['cover_endpoints']
          and len(ends[ORIGIN]) == 22 and len(ends[EZ]) == 22 and len(shared) == 8
          and set(W_owners) == set(COVER_R) and set(W_links) <= set(cover_links)
          and rejected(lambda: require(drawn == V['cover_links'], 'four drawn links are not the cover'), 'four_drawn_links'),
          links=len(set(cover_links)), endpoints=len(endpoints), per_factor_endpoints=22, shared_endpoints=len(shared),
          wilson_link_owners=[list(o) for o in W_owners])
    incident = sorted({sub(u, d) for u in COVER_R for d in S_STAR})
    outgoing_only = [b for b in incident if b in COVER_R]
    stars_per_site = len({sub(ORIGIN, d) for d in S_STAR})
    check('missing_incoming_stars',
          len(incident) == V['incident_anchors'] and stars_per_site * 7 == V['J_coefficient']
          and rejected(lambda: require(len(outgoing_only) == V['incident_anchors'], 'orthant two-anchor count'), 'orthant_two_anchors')
          and rejected(lambda: require(1 * 7 == V['J_coefficient'], 'outgoing-only J=7|tau|'), 'outgoing_only_J'),
          incident_anchors=[list(b) for b in incident], orthant_count=len(outgoing_only), stars_per_site=stars_per_site,
          star_norm_over_abs_tau=s(Q(V['omitted_per_anchor'], V['phi_denominator'])))

    # -------------------- I1 table vs geometry; translation-covariant counts --------------------
    geo_ok = True
    for row in I1_TABLE:
        a, cc = ORIENT[row['orientation']]
        for r in row['r']:
            for q in row['s']:
                p = (r, q, 0)
                geo_ok = geo_ok and face_support(p, a, cc) == frozenset(row['support'])
                geo_ok = geo_ok and is_selected(p, a, cc) == (row['role'] == 'selected')
    all_anchor0 = [(r, q) for r in range(4) for q in range(2)]
    n_all = len(all_anchor0) * 3
    n_listed = sum(len(row['r']) * len(row['s']) for row in I1_TABLE)
    counts = derive_counts(I1_TABLE)
    check('i1_table_matches_fine_geometry', geo_ok and n_all == n_listed == 24 and counts['classes'] == V['omitted_per_anchor'],
          anchored_classes=n_listed, omitted_classes=counts['classes'])
    brute = brute_force_faces()
    b0 = [f for f in brute if ORIGIN in f[3]]
    bR = [f for f in brute if ORIGIN in f[3] or EZ in f[3]]
    bsets = {}
    for f in b0:
        bsets[f[3]] = bsets.get(f[3], 0) + 1
    brute_ok = (len(b0) == counts['faces_per_factor'] and bsets == counts['sets_at_origin'] and len(bR) == counts['faces_meeting_R']
                and sorted({f[4] for f in bR}) == incident)
    check('translation_covariant_counts_match_brute_force', brute_ok,
          brute_force_faces_at_origin=len(b0), brute_force_faces_meeting_R=len(bR))
    derived = (counts['faces_per_factor'], counts['owner_sets_per_factor'], counts['faces_meeting_R'], counts['faces_inside_R'])
    candidates = (V['cand_faces'], V['cand_owner_sets'], V['cand_meet_R'], V['cand_inside_R'])

    def compare_counts(fn):
        got = fn(I1_TABLE)
        require(got == candidates, 'derived counts disagree with contract candidates')
        mutated = tuple(r for r in I1_TABLE if r['orientation'] != 'yz' or r['s'] != (1,))
        require(fn(mutated) != got, 'count insensitive to the table: hard-coded or copied')
        return got

    def derived_fn(table):
        d = derive_counts(table)
        return (d['faces_per_factor'], d['owner_sets_per_factor'], d['faces_meeting_R'], d['faces_inside_R'])

    compare_counts(derived_fn)
    restricted_site = sum(1 for f in faces_containing(ORIGIN, expand_classes(I1_TABLE)) if f[0] in COVER_R)
    restricted_R = len({(f[0], f[1][:3]) for u in COVER_R for f in faces_containing(u, expand_classes(I1_TABLE)) if f[0] in COVER_R})
    classes = expand_classes(I1_TABLE)
    bulk_sets = counts['sets_at_origin']

    def canon(M):
        m = min(M)
        return frozenset(sub(y, m) for y in M)
    bulk_canon = {}
    for M, nM in bulk_sets.items():
        require(bulk_canon.get(canon(M), nM) == nM, 'translation covariance of owner-set multiplicities')
        bulk_canon[canon(M)] = nM
    boundary_ok = True
    max_box = 0
    for N in (1, 2, 3):
        box, retained = box_retained(N, classes)
        per_site = {}
        per_set = {}
        for f in retained:
            M = owner_set(f)
            per_set[M] = per_set.get(M, 0) + 1
            for u in M:
                per_site[u] = per_site.get(u, 0) + 1
        max_box = max(max_box, max(per_site.values()))
        boundary_ok = boundary_ok and max(per_site.values()) <= counts['faces_per_factor']
        for M, nM in per_set.items():
            boundary_ok = boundary_ok and canon(M) in bulk_canon and nM <= bulk_canon[canon(M)]
    check('face_count_all_sites', boundary_ok and max_box == counts['faces_per_factor']
          and rejected(lambda: compare_counts(lambda t: candidates), 'hard_coded_or_contract_copied_count')
          and rejected(lambda: require(restricted_site == V['cand_faces'], 'count restricted to anchors 0 and e_z'), 'restricted_to_cover_anchors')
          and rejected(lambda: require(restricted_R == V['cand_meet_R'], 'R count restricted to anchors in R'), 'restricted_R_anchors')
          and 4 * V['omitted_per_anchor'] == V['labelled_bound'] and counts['faces_per_factor'] <= V['labelled_bound'],
          derived_counts=list(derived), contract_candidates=list(candidates), restricted_site_count=restricted_site,
          restricted_R_count=restricted_R, labelled_bound=V['labelled_bound'], max_count_in_boxes_N1_to_3=max_box,
          owner_set_multiplicities=counts['multiplicities'])

    # First-order face data: energy 24, norm 1/2, orthogonality.
    meet_faces = counts['meet_faces']
    link_sets = [face_link_set(f) for f in meet_faces]
    distinct4 = all(len(L) == 4 for L in link_sets)
    max_shared = max(len(link_sets[i] & link_sets[j]) for i in range(len(link_sets)) for j in range(i + 1, len(link_sets)))
    crossing = all(len(owner_set(f)) >= 2 for f in meet_faces)
    per_factor_max = max(max(sum(1 for l in L if owner(l[0]) == o) for o in {owner(l[0]) for l in L}) for L in link_sets)
    energy = 4 * V['onsite_factor'] * V['casimir_half']
    casimir = Q(1, 2) * (Q(1, 2) + 1)
    moments = [haar_moment_W(k) for k in range(5)]
    W_in_R = any(face_link_set(f) == frozenset(W_links) for f in meet_faces if owner_set(f) == frozenset(COVER_R))
    check('first_order_face_enumeration',
          distinct4 and max_shared == 1 and crossing and energy == V['face_energy'] == 8 * V['face_energy_alpha']
          and casimir == V['casimir_half'] and moments == [1, 0, Q(1, 4), 0, Q(1, 8)] and per_factor_max <= 3
          and counts['faces_meeting_R'] <= 2 * V['labelled_bound'] and W_in_R,
          H0_eigenvalue_normalized=s(energy), H0_eigenvalue_alpha_units=s(Q(energy, 8)),
          norm_WfOmega0_squared=s(moments[2]), vacuum_overlap=s(moments[1]),
          max_links_shared_by_distinct_faces=max_shared, haar_moments_W_0_to_4=[s(m) for m in moments],
          faces_meeting_R=counts['faces_meeting_R'], bound_for_R=2 * V['labelled_bound'],
          owner_sets_meeting_R=counts['owner_sets_meeting_R'])

    # -------------------- tiers --------------------
    coef = Q(1, V['phi_denominator']) / V['face_energy'] * exact_sqrt(moments[2])  # |tau|/3 /24 * 1/2 per face
    t1_per_tau = counts['faces_per_factor'] * coef
    require(t1_per_tau == Q(V['cand_t1_num'], V['cand_t1_den']), 't1 candidate 49/144 not reproduced')
    sqrt_sum_up = sum((sqrt_up(n) for n in counts['multiplicities']), Q(0))
    sqrt_sum_low = sum((sqrt_up(n) - Q(1, 10 ** 9) for n in counts['multiplicities']), Q(0))
    t1g_per_tau = sqrt_sum_up * coef
    t1_84_per_tau = V['labelled_bound'] * coef
    tiers = {}
    for sign, tau in taus.items():
        tiers[sign] = {
            'i': tier_i(tau, V),
            'i_iterated': tier_i(tau, V, iterate=True),
            'ii': tier_ii(tau, V, t1_per_tau, 'triangle over 49 face vectors, t1=49|tau|/144'),
            'ii_grouped': tier_ii(tau, V, t1g_per_tau, 'grouped owner sets, t1=(|tau|/144) sum_M sqrt(n_M), directed sqrt'),
            'ii_sharper_remainder': tier_ii(tau, V, t1_per_tau, 'triangle t1 with directed remainder 288J t/(1-8t_i)', remainder='sharper'),
            'ii_labelled_bound_84': tier_ii(tau, V, t1_84_per_tau, 'labelled bound only: t1=84|tau|/144'),
        }
    scal = {'i': tier_i(V['tau_scaling'], V), 'ii': tier_ii(V['tau_scaling'], V, t1_per_tau, 'scaling'),
            'ii_grouped': tier_ii(V['tau_scaling'], V, t1g_per_tau, 'scaling grouped')}
    Dp, Dm = tiers['+'], tiers['-']
    check('tier_i_both_signs', Dp['i']['D'] == Dm['i']['D'] and Dp['i']['t'] == V['tier_i_cap_string']
          and Dp['i_iterated']['D'] < Dp['i']['D'],
          D_i_plus=s(Dp['i']['D']), D_i_minus=s(Dm['i']['D']), D_i_preview=dec(Dp['i']['D']),
          D_i_iterated_plus=s(Dp['i_iterated']['D']), D_i_iterated_preview=dec(Dp['i_iterated']['D']))
    check('tier_ii_both_signs', Dp['ii']['D'] == Dm['ii']['D'] and Dp['ii']['t1'] == t1_per_tau * tau_cap
          and Dp['ii']['remainder'] > 0 and Dp['ii']['D'] < Dp['i']['D'],
          D_ii_plus=s(Dp['ii']['D']), D_ii_minus=s(Dm['ii']['D']), D_ii_preview=dec(Dp['ii']['D']),
          t1_over_abs_tau=s(t1_per_tau), coefficient_per_face_over_abs_tau=s(coef))
    check('tier_ii_grouped_sharpening', Dp['ii_grouped']['D'] < Dp['ii']['D'] and sqrt_sum_low < sqrt_sum_up
          and Dp['ii_sharper_remainder']['D'] <= Dp['ii']['D'] and Dp['ii_labelled_bound_84']['D'] > Dp['ii']['D'],
          sqrt_sum_upper=s(sqrt_sum_up), sqrt_sum_preview=dec(sqrt_sum_up),
          D_ii_grouped_preview=dec(Dp['ii_grouped']['D']), D_ii_sharper_remainder_preview=dec(Dp['ii_sharper_remainder']['D']),
          D_ii_labelled_84_preview=dec(Dp['ii_labelled_bound_84']['D']))

    def mix_crude_t():
        J = V['J_coefficient'] * tau_cap
        return assemble('ii', [('t1', 'ii', t1_per_tau * tau_cap), ('am2_remainder', 'i', V['Gp_R_upper'] * J * Dp['i']['t']),
                               ('self_consistent_t', 'ii', t1_per_tau * tau_cap + V['Gp_R_upper'] * J * Dp['i']['t'])])

    def refined_without_remainder():
        return assemble('ii', [('t1', 'ii', t1_per_tau * tau_cap), ('t', 'ii', t1_per_tau * tau_cap)])

    def remainder_zero():
        return assemble('ii', [('t1', 'ii', t1_per_tau * tau_cap), ('am2_remainder', 'ii', Q(0)),
                               ('self_consistent_t', 'ii', t1_per_tau * tau_cap)])
    check('tier_mixing_rejected',
          rejected(mix_crude_t, 'exact_c1_with_crude_t') and rejected(refined_without_remainder, 'refined_t_without_self_consistency')
          and rejected(remainder_zero, 'remainder_zero'),
          rule='every term names its tier; tier (ii) uses t<=t1/(1-352J) and ||c-c1||_a<=352 J t>0')

    target, secondary = V['target'], V['secondary']
    tier_ii_target_met = all(tiers[sg]['ii']['D'] <= target for sg in taus)
    check('tier_ii_target_4e-7', tier_ii_target_met and all(tiers[sg]['ii_grouped']['D'] <= target for sg in taus),
          target=s(target), comparator='<=', D_ii_plus=s(Dp['ii']['D']), margin_ratio_preview=dec(target / Dp['ii']['D'], 6))
    check('secondary_1e-6_comparison', all(tiers[sg]['ii']['D'] <= secondary for sg in taus)
          and all(tiers[sg]['i']['D'] > secondary for sg in taus),
          secondary=s(secondary), tier_ii_meets=True, tier_i_meets=False)
    D_at4_sq = 4 * Q(49, 3) * tau_cap
    check('insufficient_verdict_retained',
          all(tiers[sg]['i']['D'] > target for sg in taus) and D_at4_sq > target ** 2
          and rejected(lambda: require(tier_i(V['tau_scaling'], V)['tau'] == tau_cap, 'retuned coupling'), 'retune_tau_to_pass_tier_i'),
          tier_i_target_met=False, tier_i_status='retained limited-tier value, not retuned',
          at4_sqrt_bound_squared=s(D_at4_sq), at4_sqrt_bound_fails_target=True)

    # -------------------- consequences and scaling --------------------
    cons = {}
    for sg in taus:
        for key in ('i', 'ii'):
            D = tiers[sg][key]['D']
            cons[key + sg] = {'omega_W_interval': [s(V['omega0_W'] - D), s(V['omega0_W'] + D)],
                              'omega_W2_interval': [s(V['omega0_W2'] - D / 2), s(V['omega0_W2'] + D / 2)],
                              'mean_square_charge_m2_upper': s(D * D)}
    check('consequences_W_and_W2', V['omega0_W'] == haar_moment_W(1) and V['omega0_W2'] == haar_moment_W(2)
          and V['reference_values'] == '0 and 1/4', reference='Haar product reference P_R (zero-selected)',
          effect_refinement='|Tr[(rho-P)A]|<=D/2 for 0<=A<=I applied to W^2 only')

    def classify(ratio):
        if 99 <= ratio <= 101:
            return 'linear'
        if Q(99, 10) <= ratio <= Q(101, 10):
            return 'square_root'
        if 9900 <= ratio <= 10100:
            return 'quadratic'
        raise AdmissionError('unclassified scaling ratio')
    ratio_i = Dp['i']['D'] / scal['i']['D']
    ratio_ii = Dp['ii']['D'] / scal['ii']['D']
    ratio_iig = Dp['ii_grouped']['D'] / scal['ii_grouped']['D']
    ratio_at4 = exact_sqrt(D_at4_sq / (4 * Q(49, 3) * V['tau_scaling']))
    check('tau_scaling_exponent',
          V['tau_scaling'] * 100 == tau_cap and classify(ratio_i) == 'linear' and classify(ratio_ii) == 'linear'
          and classify(ratio_iig) == 'linear' and classify(ratio_at4) == 'square_root'
          and rejected(lambda: require(classify(ratio_at4) == 'linear', 'square-root bound relabelled linear'), 'sqrt_relabelled_linear'),
          ratio_tier_i=s(ratio_i), ratio_tier_i_preview=dec(ratio_i, 10), ratio_tier_ii=s(ratio_ii),
          ratio_tier_ii_preview=dec(ratio_ii, 10), ratio_at4_sqrt=s(ratio_at4))
    mono = [tier_ii(Q(k, 10 ** 9), V, t1_per_tau, 'mono')['D'] for k in (1, 5, 10)]
    check('monotone_in_abs_tau_samples', mono[0] < mono[1] < mono[2] == Dp['ii']['D'],
          note='illustration; monotonicity in |tau| is analytic (increasing compositions)')

    # -------------------- anchored norm restricted to the cover (actual data) --------------------
    meet_sets = counts['meet_sets']
    r_sum_triangle = sum(meet_sets.values()) * coef
    check('anchored_norm_restricted_to_cover_data',
          r_sum_triangle <= 2 * t1_per_tau and r_sum_triangle > t1_per_tau
          and rejected(lambda: require(r_sum_triangle <= 1 * t1_per_tau, 'one-site bound for the R sum'), 'one_site_R_sum'),
          R_sum_first_order_over_abs_tau=s(r_sum_triangle), two_t1_over_abs_tau=s(2 * t1_per_tau),
          straddling_owner_sets=counts['owner_sets_meeting_R'] - 1, straddling_faces=counts['faces_meeting_R'] - counts['faces_inside_R'])

    # -------------------- fixtures: three-site analytic counterexample --------------------
    a3, b3 = Q(1, 3), Q(1, 2)
    rho_vals = []
    unnorm = []
    for g in (Q(0), Q(2, 5), Q(1)):
        cr = [((0, 1), a3), ((1,), b3), ((2,), g)]
        psi = product_state(3, cr)
        rho = mscale(reduced(psi, (0,)), 1 / norm2(psi))
        rho_vals.append(rho)
        unnorm.append(sum((amp * amp for bits, amp in psi.items() if bits[0] == 0), Q(0)))
    Zab = 1 + a3 ** 2 + b3 ** 2
    expected = {((0,), (0,)): (1 + b3 ** 2) / Zab, ((0,), (1,)): a3 * b3 / Zab, ((1,), (0,)): a3 * b3 / Zab, ((1,), (1,)): a3 ** 2 / Zab}
    psi_nob = product_state(3, [((0, 1), a3), ((2,), Q(2, 5))])
    rho_nob = mscale(reduced(psi_nob, (0,)), 1 / norm2(psi_nob))
    check('three_site_model_class_counterexample',
          all(rv == expected for rv in rho_vals) and unnorm[0] < unnorm[1] < unnorm[2] and rho_nob != expected
          and rho_nob.get(((0,), (1,)), 0) == 0,
          sites='r (cover), o (outside, straddled), oprime (outside, decoupled)', a=s(a3), b=s(b3),
          rho_r=[[s(expected[((0,), (0,))]), s(expected[((0,), (1,))])], [s(expected[((1,), (0,))]), s(expected[((1,), (1,))])]],
          unnormalized_Omega_r_weight_for_g_0_2over5_1=[s(u1) for u1 in unnorm],
          lesson='rho_r is independent of the decoupled outside creation g but depends on the outside creation b '
                 'through the straddling creation a: the off-diagonal ab is second order')

    # Excitedness premise: a creation with a vacuum component breaks orthogonality.
    psi_out_bad = product_state(2, [((1,), Q(1, 2))])
    bad = dict(psi_out_bad)
    for bits, amp in psi_out_bad.items():
        if bits[0] == 0:
            nb0 = bits
            nb1 = (1,) + bits[1:]
            bad[nb0] = bad.get(nb0, 0) - Q(1, 4) * amp   # vacuum component on the cover
            bad[nb1] = bad.get(nb1, 0) - Q(1, 3) * amp
    delta_bad = vadd(bad, psi_out_bad, -1)
    check('excitedness_premise_counterexample', inner(psi_out_bad, delta_bad) != 0,
          overlap=s(inner(psi_out_bad, delta_bad)),
          lesson='c_I must lie in the excited sectors; otherwise (P_R x 1)delta != 0 and the split is not orthogonal')

    # -------------------- fixture T: R={r0,r1}, outside o, plus decoupled spectators --------------------
    base = [((0,), Q(1, 60)), ((1,), Q(1, 70)), ((0, 1), Q(1, 50)), ((0, 2), Q(1, 9)), ((1, 2), Q(1, 10)),
            ((0, 1, 2), Q(1, 11)), ((2,), Q(-1, 12))]
    Rt = (0, 1)
    fams = []
    for k in range(4):
        cr = base + [((3 + j,), Q(1, 6)) for j in range(k)]
        fams.append(split_analysis(3 + k, Rt, cr))
    an = fams[0]
    # creation algebra: commuting, nilpotent, e^{-C} equals the ordered product
    ok_alg = True
    vec0 = vacuum(3)
    for I, cI in base:
        for J, cJ in base:
            ab = c_hat(c_hat(vec0, J, cJ), I, cI)
            ba = c_hat(c_hat(vec0, I, cI), J, cJ)
            ok_alg = ok_alg and ab == ba and (ab == {} if set(I) & set(J) else True)
    series = {}
    term = vacuum(3)
    k = 0
    while term:
        series = vadd(series, term)
        k += 1
        nxt = {}
        for I, cI in base:
            nxt = vadd(nxt, c_hat(term, I, cI))
        term = mscale(nxt, Q(-1, k))
    check('creation_algebra_commuting_nilpotent', ok_alg and series == an['psi'] and an['psi'] == an['psi_other_order'],
          exponential_series_terms=k)
    check('product_split_orthogonality',
          an['explicit'] == an['delta'] and inner(an['psi_out'], an['delta']) == 0
          and all(any(bits[i] for i in Rt) for bits in an['delta']) and an['pairs'] >= 1,
          two_creation_pairs=an['pairs'], P_R_psi_equals_psi_out=True)
    e2 = trace_bound_certificate(an)
    check('explicit_reduced_density_identity', an['rho'] == an['rho_formula'] and all(f['rho'] == an['rho'] for f in fams),
          rho_R_entries={str(kk): s(vv) for kk, vv in sorted(an['rho'].items())},
          volume_family_spectators=[0, 1, 2, 3])
    check('trace_distance_inequality_fixture', e2 <= an['eps'] ** 2 and an['eps'] < 1,
          e_squared=s(e2), eps=s(an['eps']), bound=s(D_of(an['eps'])), t=s(an['t']))

    # deleted_normalization
    P_R = {((0, 0), (0, 0)): Q(1)}
    unnorm_P = [f['n2'] for f in fams]
    rho_deleted = mscale(madd(madd({((0, 0), (0, 0)): an['n2']}, an['cross']), an['sigma']), 1 / an['n2'])
    check('deleted_normalization',
          unnorm_P[0] < unnorm_P[1] < unnorm_P[2] < unnorm_P[3] and all(f['rho'] == an['rho'] for f in fams)
          and rejected(lambda: require(mtrace(rho_deleted) == 1, 'Z without ||delta||^2'), 'drop_delta_norm_from_Z')
          and rejected(lambda: require(len(set(unnorm_P)) == 1, 'unnormalized <psi,P_R psi> as a local value'), 'numerator_without_denominator'),
          unnormalized_P_R_weight_by_spectators=[s(u1) for u1 in unnorm_P], trace_with_deleted_normalization=s(mtrace(rho_deleted)))

    # outside_creations_do_not_cancel_naively
    naive_vals = []
    for k, f in enumerate(fams):
        psiA = product_state(3 + k, f['meet'])
        naive_vals.append(sum((x * x for bits, x in psiA.items() if bits[0] == 0 and bits[1] == 0), Q(0)) / norm2(f['psi']))
    true_P = an['rho'][((0, 0), (0, 0))]
    psiA0 = product_state(3, an['meet'])
    rho_self = mscale(reduced(psiA0, Rt), 1 / norm2(psiA0))
    check('outside_creations_do_not_cancel_naively',
          rejected(lambda: require(len(set(naive_vals)) == 1, 'numerator-only localisation is volume dependent'), 'numerator_only_volume_dependent')
          and rejected(lambda: require(naive_vals[0] == true_P, 'numerator-only value'), 'numerator_only_wrong_value')
          and rejected(lambda: require(rho_self == an['rho'], 'dropping outside creations everywhere'), 'drop_outside_creations_everywhere'),
          true_P_R_weight=s(true_P), naive_values_by_spectators=[dec(q1, 8) for q1 in naive_vals],
          self_normalized_naive_P_R_weight=s(rho_self[((0, 0), (0, 0))]))

    # omitted_adjoint_terms
    Om, Ex = (0, 0), (1, 1)
    A_W = {(Om, Ex): Q(1), (Ex, Om): Q(1)}
    B11 = {(Ex, Ex): Q(1)}
    Z = an['n2'] + an['d2']
    no_left = mscale(madd(madd({(Om, Om): an['n2']}, {k1: v1 for k1, v1 in an['cross'].items() if k1[0] != Om}), an['sigma']), 1 / Z)
    no_cross = mscale(madd({(Om, Om): an['n2']}, an['sigma']), 1 / Z)
    no_sigma = mscale(madd({(Om, Om): an['n2']}, an['cross']), 1 / Z)
    true_AW = expect(an['rho'], A_W)
    check('omitted_adjoint_terms',
          true_AW != 0
          and rejected(lambda: require(expect(no_left, A_W) == true_AW, 'dropped |Omega_R><xi|'), 'drop_Omega_xi')
          and rejected(lambda: require(expect(no_cross, A_W) == true_AW, 'dropped both cross terms'), 'drop_both_cross_terms')
          and rejected(lambda: require(mtrace(no_sigma) == 1 and expect(no_sigma, B11) == expect(an['rho'], B11), 'dropped Tr_out|delta><delta|'), 'drop_sigma'),
          true_W_like_value=s(true_AW), without_left_cross=s(expect(no_left, A_W)), without_sigma_trace=s(mtrace(no_sigma)))

    # straddling_supports_counted
    inside_only = [(I, cI) for I, cI in base if set(I) <= set(Rt)]
    t_in = max(sum((abs(cI) for I, cI in inside_only if u in I), Q(0)) for u in Rt)
    eps_in = eps_of(t_in)
    straddle = [(I, cI) for I, cI in base if set(I) & set(Rt) and not set(I) <= set(Rt)]
    polyfull = poly_state(3, base)
    polynostr = poly_state(3, [(I, cI) for I, cI in base if (I, cI) not in straddle])
    Nfull = poly_matrix_element(polyfull, Rt, Om, Ex)
    Nnostr = poly_matrix_element(polynostr, Rt, Om, Ex)
    diff = poly_add(Nfull, Nnostr, -1)
    d2full = [Q(0)] * 20
    d2nostr = [Q(0)] * 20
    for vecp, acc in ((polyfull, d2full), (polynostr, d2nostr)):
        for bits, amp in vecp.items():
            if any(bits[i] for i in Rt):
                sq = poly_mul(amp, amp)
                for i1, x1 in enumerate(sq):
                    acc[i1] += x1
    check('straddling_supports_counted',
          e2 > eps_in ** 2 and e2 <= an['eps'] ** 2
          and rejected(lambda: require(e2 <= eps_in ** 2, 'eps without straddling supports'), 'eps_without_straddling')
          and diff[0] == 0 and diff[1] == 0 and diff[2] != 0 and Nfull[1] == -dict(base)[(0, 1)]
          and d2full[2] > d2nostr[2],
          straddling_supports=[list(I) for I, _ in straddle], eps_inside_only=s(eps_in), e_squared=s(e2),
          W_like_element_first_order=s(Nfull[1]), straddling_change_orders_0_1_2=[s(diff[0]), s(diff[1]), s(diff[2])],
          lesson='straddling creations enter eps at first order but the W-like cross term only at second order')

    # anchored_norm_restricted_to_cover (fixture K) and extensive-sum mutation
    ck = [((0,), Q(1, 5)), ((1,), Q(1, 5)), ((2,), Q(1, 5))]
    ank = split_analysis(3, Rt, ck)
    sumR = sum((abs(cI) for I, cI in ck if set(I) & set(Rt)), Q(0))
    e2k = ank['d2'] / ank['n2']
    ext = [(3 + k) * ank['t'] for k in range(4)]
    boxes_ext = [len(coarse_box(N)) * t1_per_tau for N in (2, 3)]
    check('anchored_norm_restricted_to_cover',
          sumR <= 2 * ank['t'] and sumR > ank['t'] and e2k <= ank['eps'] ** 2
          and rejected(lambda: require(e2k <= ank['t'] ** 2, 'one site of R instead of |R|=2'), 'one_site_instead_of_two')
          and rejected(lambda: require(len(set(ext)) == 1 and boxes_ext[0] == boxes_ext[1], 'per-site maximum summed over the volume'), 'extensive_volume_sum'),
          R_sum=s(sumR), t=s(ank['t']), e_squared=s(e2k), extensive_sums_by_volume=[s(q1) for q1 in ext],
          box_extensive_first_order_over_abs_tau=[s(q1) for q1 in boxes_ext])

    # root_n_misuse (fixture C): deterministic contributions add coherently.
    cc2 = [((0,), Q(1, 5)), ((0, 1), Q(1, 5)), ((1,), Q(-1, 2))]
    anc = split_analysis(2, (0,), cc2)
    terms = [c_hat(anc['psi_out'], I, cI) for I, cI in anc['meet']]
    rss2 = sum((norm2(tv) for tv in terms), Q(0))
    lin = sum((abs(cI) for I, cI in anc['meet']), Q(0)) ** 2 * anc['n2']
    e2c = anc['d2'] / anc['n2']
    check('root_n_misuse',
          anc['d2'] > rss2 and anc['d2'] <= lin and e2c <= anc['eps'] ** 2
          and rejected(lambda: require(anc['d2'] <= rss2, 'root-sum-square of deterministic terms'), 'root_sum_square')
          and rejected(lambda: require(anc['d2'] <= lin / len(terms), 'division by sqrt(N)'), 'divide_by_sqrt_N')
          and rejected(lambda: require(anc['d2'] <= lin / 64 ** 2, 'division by 64'), 'divide_by_64'),
          delta_norm_squared=s(anc['d2']), root_sum_square=s(rss2), linear_bound_squared=s(lin), terms=len(terms))

    # -------------------- cutoff-vector removal --------------------
    U = [[Q(1, 3), Q(2, 3), Q(2, 3)], [Q(2, 3), Q(1, 3), Q(-2, 3)], [Q(2, 3), Q(-2, 3), Q(1, 3)]]
    lam = [Q(0), Q(1, 2), Q(2)]
    H = [[sum((U[i][k] * lam[k] * U[j][k] for k in range(3)), Q(0)) for j in range(3)] for i in range(3)]
    psi_g = [U[i][0] for i in range(3)]
    gap = lam[1] - lam[0]
    eck = []
    for ncut in (1, 2, 3):
        phi = [psi_g[i] if i < ncut else Q(0) for i in range(3)]
        nphi = sum((q1 * q1 for q1 in phi), Q(0))
        energy_phi = sum((phi[i] * H[i][j] * phi[j] for i in range(3) for j in range(3)), Q(0)) / nphi
        ov2 = sum((psi_g[i] * phi[i] for i in range(3)), Q(0)) ** 2 / nphi
        eck.append((1 - ov2, (energy_phi - lam[0]) / gap))
    orth = all(sum((U[i][k] * U[j][k] for k in range(3)), Q(0)) == (1 if i == j else 0) for i in range(3) for j in range(3))

    def vector_convergence(premises, gap_value):
        needed = {'untruncated_gap_from_AM2', 'rayleigh_upper_via_form_core', 'eckart_inequality', 'partial_trace_contraction'}
        require(needed <= set(premises), 'cutoff-vector step incomplete: ' + ','.join(sorted(needed - set(premises))))
        require(gap_value > 0, 'vector convergence needs a positive gap')
        return True
    degenerate_vector_overlap = Q(0)   # H'=diag(0,0,1): cutoff ground e2 has E_0 exactly but is orthogonal to e1
    check('cutoff_vector_removal',
          orth and all(lhs <= rhs for lhs, rhs in eck) and eck[-1] == (0, 0) and eck[0][1] > eck[1][1] > eck[2][1]
          and vector_convergence(['untruncated_gap_from_AM2', 'rayleigh_upper_via_form_core', 'eckart_inequality', 'partial_trace_contraction'], Q(1, 2))
          and rejected(lambda: vector_convergence(['am2_section6_eigenvalue_convergence'], Q(1, 2)), 'cite_AM2_section6_alone')
          and rejected(lambda: vector_convergence(['untruncated_gap_from_AM2', 'rayleigh_upper_via_form_core', 'eckart_inequality',
                                                   'partial_trace_contraction'], Q(0)), 'degenerate_eigenvalue_only')
          and degenerate_vector_overlap == 0,
          eckart_pairs=[[s(l1), s(r1)] for l1, r1 in eck], inequality='1-|<psi,psi_L>|^2<=(E_0L-E_0)/(E_1-E_0)<=2(E_0L-E_0)')

    # -------------------- AQ passage --------------------
    a_, b_ = Q(3, 50), Q(4, 50)
    lim_plus = {((0,), (0,)): 1 - a_, ((0,), (1,)): b_, ((1,), (0,)): b_, ((1,), (1,)): a_}
    lim_minus = {((0,), (0,)): 1 - a_, ((0,), (1,)): -b_, ((1,), (0,)): -b_, ((1,), (1,)): a_}
    tn = 2 * exact_sqrt(a_ ** 2 + b_ ** 2)
    psd = a_ * (1 - a_) >= b_ ** 2
    flags_passage = {'uniqueness_claimed': False, 'whole_sequence_convergence_claimed': False, 'rate_in_N_claimed': False}
    check('aq_passage_trace_norm_only',
          psd and tn == Q(1, 5) and lim_plus != lim_minus and all(v is False for v in flags_passage.values())
          and rejected(lambda: require(lim_plus == lim_minus, 'uniqueness inferred from a uniform bound'), 'uniqueness_from_bound')
          and rejected(lambda: require(flags_passage['rate_in_N_claimed'] is True, 'rate in N'), 'rate_in_N'),
          fixture_trace_distance=s(tn), two_distinct_subsequential_limits=True, **flags_passage,
          quantifier='every subsequence N_k>=2 along which rho_{N_k,R} converges in trace norm, in particular AQ1 diagonal extraction')

    # -------------------- units, clock and centering controls --------------------
    tau_sym = tau_cap
    v_norm = -tau_sym / V['phi_denominator']
    v_alpha = v_norm / V['delta_denominator']
    right1 = v_norm / V['face_energy']
    right2 = v_alpha / V['face_energy_alpha']
    alpha_, hbar_ = Q(5), Q(7)
    t_E = Q(3, 2)
    s_clock = alpha_ * t_E / hbar_
    u_clock = s_clock / 8
    check('wrong_delta_alpha_hbar_clock',
          right1 == right2 == -tau_sym / 72 and V['face_coefficient_denominator'] == V['phi_denominator'] * V['delta_denominator']
          and 3 * s_clock == 24 * u_clock
          and rejected(lambda: require(v_alpha / V['face_energy'] == right1, 'alpha-unit V with delta-unit energy'), 'mixed_units_576')
          and rejected(lambda: require(v_norm / V['face_energy_alpha'] == right1, 'delta-unit V with alpha-unit energy'), 'mixed_units_9')
          and rejected(lambda: require(24 * s_clock == 3 * s_clock, 'exponent 24 with s'), 'eightfold_clock'),
          first_order_coefficient=s(right1), nonunit_fixture={'alpha': '5', 'hbar': '7', 't_E': '3/2', 's': s(s_clock), 'u': s(u_clock)})
    m_, d_ = Q(1, 4), Q(1, 100)
    check('vector_versus_scalar_centering',
          d_ ** 2 == Q(1, 10000) and -2 * m_ * d_ - d_ ** 2 == Q(-51, 10000) and m_ ** 2 == Q(1, 16)
          and rejected(lambda: require(d_ ** 2 == -2 * m_ * d_ - d_ ** 2, 'scalar subtraction as vector centering'), 'scalar_as_vector'),
          vector_residue=s(d_ ** 2), scalar_residue=s(-2 * m_ * d_ - d_ ** 2), uncentered_residue=s(m_ ** 2),
          av1_centering_charge='m^2<=D^2 at each tier')
    check('first_order_mean_charged',
          all(Q(cons[k1]['mean_square_charge_m2_upper']) > 0 for k1 in cons) and tau_cap / 144 <= Dp['ii']['D']
          and rejected(lambda: require(Q(0) >= Dp['ii']['D'] ** 2, 'zero-mean assumption'), 'zero_mean_assumed'),
          m2_upper_tier_ii=s(Dp['ii']['D'] ** 2), candidate_first_order_mean_magnitude_not_claimed=s(tau_cap / 144))

    # -------------------- model relabelling, arithmetic, premises --------------------
    packet_model = {'model_id': V['model_id'], 'tau': s(tau_cap), 'triple': [s(q1) for q1 in V['triple']],
                    'reference_route': V['reference_route'], 'state_provenance': V['state_provenance']}

    def validate_model(pk):
        require(pk['model_id'] == 'AQ_patterned_zero_selected', 'model id')
        require(rat(pk['tau']) == tau_cap, 'coupling changed')
        require([rat(q1) for q1 in pk['triple']] == [0, 0, 0], 'selected triple changed')
        require(pk['reference_route'] == 'haar', 'reference route changed')
        require(pk['state_provenance'].startswith('AQ1_centered_whole_star_subsequence'), 'state provenance changed')
        return True
    muts = []
    for key, val in (('tau', '1/100000000000000'), ('triple', ['0', '1/100', '0']), ('reference_route', 'selected_strip'),
                     ('model_id', 'FG(two_plaquette,1/2,24,I1.5,physical)'), ('state_provenance', 'finite_volume_N=3')):
        mutated = dict(packet_model)
        mutated[key] = val
        muts.append(rejected(lambda m=mutated: validate_model(m), 'relabel_' + key))
    check('changed_model_relabelled', validate_model(packet_model) and len(muts) == 5, packet_model=packet_model, rejected=muts)

    forbidden = ('mp' + 'math', 'num' + 'py', 'fl' + 'int', 'sym' + 'py')
    own = (BASE / 'check.py').read_text()
    imports = [ln for ln in own.splitlines() if ln.startswith('import ') or ln.startswith('from ')]
    check('exact_arithmetic_admission',
          not any(any(fb in ln for fb in forbidden) for ln in imports)
          and rejected(lambda: rat(1e-08), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('NaN'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator'),
          imports=imports, decimals='previews only, truncated from exact rationals')

    forward_list = ['AGENTS.md', CONTRACT_REL] + V['shared_premises'] + V['forward_additional']
    reverse_list = ['AGENTS.md', CONTRACT_REL] + V['shared_premises']
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    bad_patterns = ('research/round32/skeptic/triage.md', 'research/round32/advisor/deliberation-', '/loop2-response.md', 'research/round32/forward/av')

    def validate_reverse(lst):
        for item in lst:
            require(not any(bp in item for bp in bad_patterns), 'reverse premise isolation violated by ' + item)
        return True
    check('reverse_premise_isolation',
          sorted(inventory) == sorted(set(forward_list)) and validate_reverse(reverse_list)
          and c.get('reverse_premise_isolation') is True
          and rejected(lambda: validate_reverse(reverse_list + ['research/round32/skeptic/triage.md']), 'reverse_reads_triage')
          and rejected(lambda: validate_reverse(reverse_list + ['research/round32/forward/av1/report.md']), 'reverse_reads_forward_av'),
          forward_inventory_files=len(inventory), reverse_premise_count=len(reverse_list),
          forward_additional_disclosed=V['forward_additional'])

    pi_lo, pi_hi = pi_bracket()
    kdyn = Q(V['av2_k_num'], 10 ** V['av2_k_exp'])
    goal = Q(1, 10 ** V['av2_goal_exp'])

    def F_up(D):
        return 2 * (D + D * D) + kdyn / pi_lo

    def F_low(D):
        return 2 * (D + D * D) + kdyn / pi_hi
    thr_next = V['av2_threshold'] + Q(1, 10 ** 9)
    check('av2_feasibility_threshold',
          F_up(target) <= goal and F_up(V['av2_threshold']) <= goal and F_low(thr_next) > goal
          and F_up(Dp['ii']['D']) <= goal and F_low(Dp['i']['D']) > goal and target <= V['av2_threshold'],
          pi_bracket=[s(pi_lo), s(pi_hi)], F_at_target_upper_preview=dec(F_up(target), 8),
          F_at_D_ii_upper_preview=dec(F_up(Dp['ii']['D']), 8), threshold=s(V['av2_threshold']),
          note='arithmetic of the contract feasibility statement only; the AV2 window lemma is not proved here')

    claim_flags = {'continuum_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False,
                   'scientific_priority_verified': False, 'euclidean_node_certified': False, 'first_order_parity_claim': False}
    check('no_priority_or_continuum_claim', all(v is False for v in claim_flags.values()),
          historical_or_occult_numeric_premise=False)

    # -------------------- assemble packet --------------------
    headline = {
        'D_i_plus': s(Dp['i']['D']), 'D_i_minus': s(Dm['i']['D']), 'D_i_preview': dec(Dp['i']['D']),
        'D_ii_plus': s(Dp['ii']['D']), 'D_ii_minus': s(Dm['ii']['D']), 'D_ii_preview': dec(Dp['ii']['D']),
        'D_ii_grouped_preview': dec(Dp['ii_grouped']['D']), 'D_i_iterated_preview': dec(Dp['i_iterated']['D']),
        'at4_sqrt_bound_squared': s(D_at4_sq), 'at4_sqrt_bound_preview': dec(sqrt_up(D_at4_sq, 10 ** 20)),
    }
    error_terms = {
        'am2_remainder': {'tier_ii_plus': s(Dp['ii']['remainder']), 'tier_i': 'not_applicable: tier (i) bounds the full c by J*G(R) directly'},
        'two_creation': {'tier_i_plus': s(Dp['i']['t'] ** 2), 'tier_ii_plus': s(Dp['ii']['t'] ** 2)},
        'straddling': {'status': 'counted inside the 2t term of eps (all supports meeting R, straddling included)',
                       'first_order_straddling_faces_triangle_over_abs_tau': s((counts['faces_meeting_R'] - counts['faces_inside_R']) * coef)},
        'density': {'tier_i_plus': s(2 * Dp['i']['eps'] ** 2 / (1 + Dp['i']['eps'] ** 2)),
                    'tier_ii_plus': s(2 * Dp['ii']['eps'] ** 2 / (1 + Dp['ii']['eps'] ** 2))},
        'onsite_cutoff_vector': 'not_applicable as a numeric cost: exact limit L->infinity in each fixed box, proved by Eckart plus form-core Rayleigh convergence',
        'arithmetic': 'not_applicable as a numeric cost: exact Fractions; only directed constant enclosures (exp(1/8)<8/7, e^{8t}<=1/(1-8t), sqrt upper brackets)',
    }
    require(sorted(error_terms) == sorted(V['error_terms']), 'error terms differ from preregistration')
    packet = {
        'loop': 'AV1', 'direction': 'forward', 'human_author': 'Hruday N M (BUNZEEY)',
        'contribution_alias': 'HNM-AV1-F forward product-ordering local state lemma',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha,
        'model': packet_model, 'tau_values': {sg: s(tv) for sg, tv in taus.items()}, 'tau_scaling_control': s(V['tau_scaling']),
        'constants': {'R': s(R), 'J_cap': s(J_cap), 'G_R_upper': s(G_R), 'G_prime_R_upper': s(Gp_R),
                      'tier_i_t_cap': s(Dp['i']['t']), 'face_energy_normalized': s(energy), 'norm_WfOmega0': '1/2',
                      'first_order_coefficient_per_face': '-tau/72', 'coefficient_norm_per_face_over_abs_tau': s(coef),
                      't1_triangle_over_abs_tau': s(t1_per_tau), 't1_grouped_upper_over_abs_tau': s(t1g_per_tau),
                      't1_labelled_bound_84_over_abs_tau': s(t1_84_per_tau), 'self_consistent_coefficient': str(V['self_consistent_coefficient'])},
        'face_enumeration': {'faces_per_factor': counts['faces_per_factor'], 'owner_sets_per_factor': counts['owner_sets_per_factor'],
                             'faces_meeting_R': counts['faces_meeting_R'], 'faces_inside_R': counts['faces_inside_R'],
                             'faces_containing_R': counts['faces_containing_R'], 'owner_sets_meeting_R': counts['owner_sets_meeting_R'],
                             'multiplicities': counts['multiplicities'],
                             'owner_sets_at_origin': sorted([sorted(list(y) for y in M), n] for M, n in bulk_sets.items()),
                             'derived_from': 'I1 21-class table by translation covariance; confirmed by fine-lattice brute force'},
        'tiers': {sg: {k1: tier_record(v1) for k1, v1 in tiers[sg].items()} for sg in taus},
        'scaling_tau_over_100': {k1: tier_record(v1) for k1, v1 in scal.items()},
        'headline': headline, 'consequences': cons,
        'targets': {'target_D_ii': s(target), 'secondary': s(secondary), 'tier_ii_meets_target': tier_ii_target_met,
                    'tier_ii_meets_secondary': True, 'tier_i_meets_target': False, 'tier_i_meets_secondary': False},
        'error_terms_itemized': error_terms,
        'tier_ii_target_met': tier_ii_target_met,
        'uniqueness_claimed': False, 'whole_sequence_convergence_claimed': False, 'rate_in_N_claimed': False,
        'proposed_forward_verdict': 'accepted_within_scope (forward route only; the gate also needs the reverse route and skeptical review)',
        'routes_executed': ['forward product ordering with explicit reduced density'],
        'routes_not_executed': ['reverse vacuum-overlap/fidelity route (assigned to the reverse producer)'],
    }
    packet.update(claim_flags)

    # -------------------- coherent evidence tampering --------------------
    def packet_hash(pk):
        body = {k1: v1 for k1, v1 in pk.items() if k1 != 'packet_sha256'}
        return sha_bytes(json.dumps(body, sort_keys=True).encode('utf-8'))

    def validate_packet(pk, inv):
        require(pk.get('packet_sha256') == packet_hash(pk), 'packet hash mismatch')
        ids = {ch['id']: ch for ch in pk['checks']}
        for cid in V['controls']:
            if cid == 'coherent_evidence_tampering':
                continue
            require(cid in ids and ids[cid]['passed'] is True, 'required control missing or failed: ' + cid)
        for flag in claim_flags:
            require(pk[flag] is False, 'claim flag not false: ' + flag)
        require(sorted(inv) == sorted(set(forward_list)), 'premise snapshot inventory incomplete')
        recomputed = tier_ii(tau_cap, V, t1_per_tau, 'recheck')['D']
        require(rat(pk['headline']['D_ii_plus']) == recomputed, 'headline D_ii differs from recomputation')
        require(pk['tier_ii_target_met'] is (recomputed <= target), 'target Boolean differs from recomputation')
        require(pk['targets']['tier_i_meets_target'] is (tier_i(tau_cap, V)['D'] <= target), 'tier (i) Boolean differs')
        return True

    base_packet = dict(packet)
    base_packet['checks'] = [dict(ch) for ch in CHECKS]
    base_packet['packet_sha256'] = packet_hash(base_packet)

    def tamper_control():
        pk = json.loads(json.dumps(base_packet))
        for ch in pk['checks']:
            if ch['id'] == 'deleted_normalization':
                ch['passed'] = False
        pk['packet_sha256'] = packet_hash(pk)
        return validate_packet(pk, inventory)

    def tamper_snapshot():
        inv = dict(inventory)
        inv.pop('research/round32/methods/paired-physics-research/SKILL.md')
        pk = json.loads(json.dumps(base_packet))
        pk['packet_sha256'] = packet_hash(pk)
        return validate_packet(pk, inv)

    def tamper_value():
        pk = json.loads(json.dumps(base_packet))
        pk['headline']['D_ii_plus'] = s(rat(pk['headline']['D_ii_plus']) / 2)
        pk['packet_sha256'] = packet_hash(pk)
        return validate_packet(pk, inventory)

    def tamper_tier_i_boolean():
        pk = json.loads(json.dumps(base_packet))
        pk['targets']['tier_i_meets_target'] = True
        pk['packet_sha256'] = packet_hash(pk)
        return validate_packet(pk, inventory)
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(tamper_control, 'control_boolean_flipped_hash_rebound')
          and rejected(tamper_snapshot, 'snapshot_removed_hash_rebound')
          and rejected(tamper_value, 'D_ii_halved_hash_rebound')
          and rejected(tamper_tier_i_boolean, 'tier_i_target_flipped_hash_rebound'))

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in V['controls'] if cid not in ids]
    require(not missing, 'contract controls without a check: ' + ','.join(missing))
    packet['checks'] = CHECKS
    packet['contract_controls_covered'] = sorted(V['controls'])
    return packet


def float_free(obj):
    if isinstance(obj, float):
        return False
    if isinstance(obj, dict):
        return all(float_free(v) for v in obj.values())
    if isinstance(obj, list):
        return all(float_free(v) for v in obj)
    return True


def main():
    ap = argparse.ArgumentParser(description='AV1 forward exact checker')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    require(out.is_absolute(), 'absolute output directory required')
    out = out.resolve()
    require(not out.exists(), 'fresh (non-existent) output directory required')
    require(ROOT not in out.parents and out != ROOT, 'output directory must be outside the checkout')
    check_sha = sha(BASE / 'check.py')   # recorded before any evaluation
    result = compute(check_sha)
    require(float_free(result), 'floating-point value in results')
    out.mkdir(parents=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    sources = {}
    for p in sorted(BASE.rglob('*')):
        rel = p.relative_to(BASE)
        if p.is_file() and (rel.parts[0] == 'inputs' or p.name in ('check.py', 'report.md')) and rel.parts[0] != 'output':
            sources[rel.as_posix()] = sha(p)
    manifest = {'loop': 'AV1', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AV1', 'direction': 'forward', 'checks': len(result['checks']),
                      'D_i_preview': result['headline']['D_i_preview'], 'D_ii_preview': result['headline']['D_ii_preview'],
                      'tier_ii_target_met': result['tier_ii_target_met']}, sort_keys=True))


if __name__ == '__main__':
    main()
