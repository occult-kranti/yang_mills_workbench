#!/usr/bin/env python3
"""AX1 forward producer: exact checks for the route-B re-derivation of the uniform
Kogut-Susskind SU(2) Hamiltonian at fixed spacing (strong bare coupling).

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production.

Standard library only (argparse, fractions, hashlib, json, math, pathlib, re).
Every admission Boolean is decided in exact Fraction arithmetic; decimal strings
are truncated previews.  Conditions raise AdmissionError explicitly (never
`assert`), so every check stays active under `python -O`.

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
CONTRACT_REL = 'research/round32/contracts/ax1.json'
CONTRACT_SHA256 = 'bc834eec4f5377041cea9db42a8674cf1f3de0a43b7fef3696a461a011da7d8d'


class AdmissionError(Exception):
    """An admission condition failed or a damaging mutation was accepted."""


def require(condition, message):
    if not condition:
        raise AdmissionError(message)


CHECKS = []
PENDING = []   # labels of damaging mutations rejected since the previous recorded check


def check(identity, condition, **details):
    require(condition, 'failed check ' + identity)
    require(all(c['id'] != identity for c in CHECKS), 'duplicate check id ' + identity)
    entry = {'id': identity, 'passed': True}
    entry.update(details)
    if PENDING:
        entry['rejected_mutations'] = list(PENDING)
        del PENDING[:]
    CHECKS.append(entry)


def rejected(mutation, label):
    """Run a damaging mutation; it must raise AdmissionError."""
    try:
        mutation()
    except AdmissionError:
        PENDING.append(label)
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


def sqrt_up(n, scale=10 ** 12):
    """Directed rational upper bound of sqrt(n) for a nonnegative rational n."""
    n = Q(n)
    k = isqrt(n.numerator * scale * scale // n.denominator)
    while Q(k, scale) ** 2 < n:
        k += 1
    up = Q(k, scale)
    require(up * up >= n and (up - Q(1, scale)) ** 2 < n, 'sqrt bracket')
    return up


def sqrt_down(n, scale=10 ** 12):
    n = Q(n)
    k = isqrt(n.numerator * scale * scale // n.denominator)
    while Q(k + 1, scale) ** 2 <= n:
        k += 1
    while Q(k, scale) ** 2 > n:
        k -= 1
    return Q(k, scale)


WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'six': 6, 'seven': 7, 'eight': 8}


# ---------------------------------------------------------------------------
# Contract: every target, candidate and constant is read from the sha256-bound snapshot.
# ---------------------------------------------------------------------------
def load_contract():
    raw = (BASE / 'inputs' / CONTRACT_REL).read_bytes()
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen AX1 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'AX1' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
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
    m = match(r'^tau/(\d+) for each selected face \(box check \|tau\|/(\d+)<=1/(\d+) and <=1/(\d+)\)$',
              p['uniform_selected_coefficient_over_alpha'], 'uniform coefficient')
    v['sel_over_alpha_den'] = int(m.group(1))
    require(int(m.group(2)) == v['sel_over_alpha_den'], 'box check uses the same coefficient')
    v['box_bridge'], v['box_ends'] = Q(1, int(m.group(3))), Q(1, int(m.group(4)))
    m = match(r'^(\d+)\|tau\| \((\d+) from (\w+) anchor stars \+ (\d+) from the single-factor group\)$',
              p['per_site_sum_J_prime'], 'J prime')
    v['cand_J'], v['cand_J_stars'], v['cand_stars_per_site'], v['cand_J_single'] = (
        int(m.group(1)), int(m.group(2)), WORDS[m.group(3)], int(m.group(4)))
    m = match(r"^R1: re-freeze J_0'=(\d+)/10\^(\d+) with exact contraction checks J_0'\*(\d+)/(\d+)=(\d+)/(\d+)<1/(\d+) "
              r"and 2\*J_0'\*(\d+)=(\d+)/(\d+)<1 \(alternative R2: cap \|tau\|<=(\d+)/(\d+) is a changed coupling and is not selected\)$",
              p['J0_resolution'], 'J0 resolution')
    v['J0p'] = Q(int(m.group(1)), 10 ** int(m.group(2)))
    v['GR_upper'] = Q(int(m.group(3)), int(m.group(4)))
    v['selfmap_rational'] = Q(int(m.group(5)), int(m.group(6)))
    v['R'] = Q(1, int(m.group(7)))
    v['GpR_upper'] = Q(int(m.group(8)))
    v['exclusion_rational'] = Q(int(m.group(9)), int(m.group(10)))
    v['R2_cap'] = Q(int(m.group(11)), int(m.group(12)))
    v['j0_resolution_text'] = p['J0_resolution']
    m = match(r'^omega\(h_R\)<=2\((\d+)\*(\d+)\|tau\|\+(\d+)\|tau\|\)=(\d+)\|tau\|, epsilon_R<=(\d+)\|tau\| \(square-root control only\)$',
              p['reset_budget'], 'reset budget')
    v['cand_reset_stars'], v['cand_reset_star_norm'], v['cand_reset_single'] = int(m.group(1)), int(m.group(2)), int(m.group(3))
    v['cand_reset'], v['cand_eps_R'] = int(m.group(4)), int(m.group(5))
    m = match(r"^exactly (\w+) single-factor selected groups \((\w+) faces\) meet R; \|\|B_N\|\|<=(\d+)\|tau\|/(\d+)\+(\d+)\|tau\|/(\d+)"
              r"=(\d+)\|tau\|/(\d+), k'=(\d+)\|tau\|/(\d+)$", p['incidence'], 'incidence')
    v['cand_single_groups'], v['cand_selected_faces_R'] = WORDS[m.group(1)], WORDS[m.group(2)]
    v['cand_B_stars'] = Q(int(m.group(3)), int(m.group(4)))
    v['cand_B_singles'] = Q(int(m.group(5)), int(m.group(6)))
    v['cand_B'] = Q(int(m.group(7)), int(m.group(8)))
    v['cand_k'] = Q(int(m.group(9)), int(m.group(10)))
    m = match(r'^faces owning a link of a factor bounded by (\d+) \((\w+) anchors times (\d+)\) and (\d+) for R; '
              r'omega\(W\)\^\{\(1\)\}=\+-\|tau\|/(\d+) unchanged; parity rule unchanged$', p['first_order_faces'], 'first order faces')
    v['bound_per_factor'], v['bound_anchors'], v['bound_classes'], v['bound_R'] = (
        int(m.group(1)), WORDS[m.group(2)], int(m.group(3)), int(m.group(4)))
    v['first_order_den'] = int(m.group(5))
    m = match(r'^tau=(\d+)/g\^4; at the cap g\^4=(\d+)\.(\d+)x10\^(\d+)$', p['dictionary'], 'dictionary')
    v['dict_num'] = int(m.group(1))
    v['g4_cap'] = Q(int(m.group(2) + m.group(3)), 10 ** len(m.group(3))) * 10 ** int(m.group(4))
    m = match(r"2\(D'\+D'\^2\)\+(\d+)\|tau\|/pi<=10\^-(\d+), i\.e\. D'<=(\d+)\.(\d+)x10\^-(\d+)", p['d_prime_note'], 'ax2 note')
    v['ax2_k_num'], v['ax2_goal_exp'] = int(m.group(1)), int(m.group(2))
    v['ax2_note_threshold'] = Q(int(m.group(3) + m.group(4)), 10 ** (len(m.group(4)) + int(m.group(5))))
    m = match(r'candidate about (\d+)-(\d+)x10\^-(\d+) from (\d+) faces per factor', p['d_prime_note'], 'd prime candidate')
    v['d_prime_candidate'] = (Q(int(m.group(1)), 10 ** int(m.group(3))), Q(int(m.group(2)), 10 ** int(m.group(3))))
    v['d_prime_candidate_faces'] = int(m.group(4))
    model = c['model']
    v['model_text'] = model
    v['face_den'] = int(match(r'every elementary face has coefficient nu=alpha\*tau/(\d+)', model, 'nu').group(1))
    v['model_dict_num'] = int(match(r'AL1 dictionary alpha=g\^2/\(2a\), lambda=2/\(g\^2 a\), tau=(\d+)/g\^4', model, 'dict').group(1))
    v['onsite_factor'] = int(match(r'on-site h_b=(\d+) sum_e C_e with Haar reference', model, 'onsite').group(1))
    m = match(r'whole stars phi_b \((\d+) omitted faces, norm (\d+)\|tau\|\)', model, 'stars')
    v['omitted_per_anchor'], v['star_norm'] = int(m.group(1)), int(m.group(2))
    v['selected_per_factor'] = WORDS[match(r'one single-factor group per factor for its (\w+) selected xy faces \(norm <=\|tau\|\)',
                                           model, 'single group').group(1)]
    m = match(r'\|tau\|<=10\^-(\d+) \(g\^4>=(\d+)\.(\d+)x10\^(\d+)\)', model, 'model cap')
    require(Q(1, 10 ** int(m.group(1))) == v['tau_cap'], 'model cap differs from tau_cap')
    v['g4_model'] = Q(int(m.group(2) + m.group(3)), 10 ** len(m.group(3))) * 10 ** int(m.group(4))
    require('Not weak coupling, not continuum.' in model, 'model exclusion sentence')
    m = match(r"psi_b=-\(tau/(\d+)\) sum over the (\w+) selected xy faces of factor b", req[1], 'item 2 psi')
    v['psi_den'], v['psi_faces'] = int(m.group(1)), WORDS[m.group(2)]
    v['item2_J'] = int(match(r"J'<=(\d+)\|tau\|", req[1], 'item 2 J').group(1))
    v['item2_support'] = WORDS[match(r'maximal support is still (\w+) sites', req[1], 'item 2 support').group(1)]
    v['item2_order'] = WORDS[match(r'\(at most (\w+)\)', req[1], 'item 2 order').group(1)]
    m = match(r'full-space gap >=1/(\d+) normalized \(alpha/(\d+) physical\)', req[2], 'item 3 gap')
    v['gap_normalized'], v['gap_physical_den'] = Q(1, int(m.group(1))), int(m.group(2))
    m = match(r'h_b=(\d+) sum C_e>=(\d+) Q_b', req[2], 'item 3 onsite')
    v['item3_onsite'], v['item3_gap'] = int(m.group(1)), int(m.group(2))
    m = match(r'omega\(h_R\)<=(\d+)\|tau\| with the Haar reference gap (\w+)', req[3], 'item 4 reset')
    v['item4_reset'], v['item4_gap'] = int(m.group(1)), WORDS[m.group(2)]
    m = match(r'the stars meeting R \((\w+)\), the single-factor selected groups meeting R \((\w+)\), the selected faces inside R \((\w+)\), '
              r"hence \|\|B_N\|\|<=(\d+)\|tau\|/(\d+) and k'=(\d+)\|tau\|/(\d+) in G units", req[4], 'item 5')
    v['cand_stars_R'], v['item5_singles'], v['item5_faces'] = WORDS[m.group(1)], WORDS[m.group(2)], WORDS[m.group(3)]
    v['item5_B'], v['item5_k'] = Q(int(m.group(4)), int(m.group(5))), Q(int(m.group(6)), int(m.group(7)))
    m = match(r'(\d+) anchored faces per factor, candidates (\d+) per factor owner-set count and (\d+) for R', req[5], 'item 6')
    v['anchored_classes'], v['item6_cand_factor'], v['item6_cand_R'] = int(m.group(1)), int(m.group(2)), int(m.group(3))
    v['item9_nu_den'] = int(match(r'selected faces carry the same nu=alpha\*tau/(\d+)', req[8], 'item 9 nu').group(1))
    v['item9_first'] = int(match(r'omega\(W\)\^\{\(1\)\}=\+tau/(\d+) is unchanged', req[8], 'item 9 first').group(1))
    t = pre['target']
    require(t['quantity'] == 'D_ii (uniform, route B) at the cap' and t['comparator'] == '<=', 'target quantity/comparator')
    v['target'] = rat(t['value'])
    m = match(r'D_ii<=(\d+)/10\^(\d+) at both signs', c['acceptance']['accepted_within_scope'], 'acceptance target')
    require(Q(int(m.group(1)), 10 ** int(m.group(2))) == v['target'], 'acceptance target differs from preregistration')
    v['model_id'] = pre['model_id']
    v['prereg_triple'] = list(pre['selected_triple_alpha_units'])
    v['reference_route'] = pre['observable']['reference_route']
    v['reference_values'] = pre['observable']['reference_value_exact']
    v['state_provenance'] = pre['state_provenance']
    v['clock'] = pre['clock']
    v['controls'] = list(c['controls'])
    require(v['controls'] == list(pre['controls_required']['ids']), 'controls and preregistration mirror differ')
    v['error_terms'] = list(pre['error_terms_itemized'])
    v['shared_premises'] = list(c['shared_premises'])
    v['forward_additional'] = list(c['forward_additional_premises'])
    v['reverse_isolation'] = c.get('reverse_premise_isolation')
    v['premise_note'] = c.get('premise_note', '')
    v['new_semantics'] = dict(c['new_control_semantics'])
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    return v


# ---------------------------------------------------------------------------
# Fine-lattice geometry and the explicit 24-class anchored face table (I1 Section 3).
# ---------------------------------------------------------------------------
E_UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
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
    return ((p, a), (add(p, E_UNIT[a]), c), (add(p, E_UNIT[c]), a), (p, c))


def face_support(p, a, c):
    return frozenset(owner(link[0]) for link in face_links(p, a, c))


def is_selected(p, a, c):
    return (a, c) == (0, 1) and p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)


# The 24 anchored face classes of one coarse factor, eight rows (I1 table, Section 3).
# Every class carries the same normalized coefficient -(1/3)*tau (I1.5 with nu=alpha*tau/24,
# delta=alpha/8): the uniform Kogut-Susskind assignment.
CLASS_ROWS = (
    {'orientation': 'xy', 'r': (0, 1, 2), 's': (0,), 'support': ((0, 0, 0),), 'role': 'selected'},
    {'orientation': 'xy', 'r': (0, 1, 2), 's': (1,), 'support': ((0, 0, 0), (0, 1, 0)), 'role': 'omitted'},
    {'orientation': 'xy', 'r': (3,), 's': (0,), 'support': ((0, 0, 0), (1, 0, 0)), 'role': 'omitted'},
    {'orientation': 'xy', 'r': (3,), 's': (1,), 'support': ((0, 0, 0), (1, 0, 0), (0, 1, 0)), 'role': 'omitted'},
    {'orientation': 'xz', 'r': (0, 1, 2), 's': (0, 1), 'support': ((0, 0, 0), (0, 0, 1)), 'role': 'omitted'},
    {'orientation': 'xz', 'r': (3,), 's': (0, 1), 'support': ((0, 0, 0), (1, 0, 0), (0, 0, 1)), 'role': 'omitted'},
    {'orientation': 'yz', 'r': (0, 1, 2, 3), 's': (0,), 'support': ((0, 0, 0), (0, 0, 1)), 'role': 'omitted'},
    {'orientation': 'yz', 'r': (0, 1, 2, 3), 's': (1,), 'support': ((0, 0, 0), (0, 1, 0), (0, 0, 1)), 'role': 'omitted'},
)
UNIFORM_COEFFICIENT_OVER_TAU = Q(-1, 3)   # normalized units delta=alpha/8, every class


def expand_classes(rows, roles=('omitted', 'selected')):
    out = []
    for row in rows:
        if row['role'] not in roles:
            continue
        for r in row['r']:
            for q in row['s']:
                out.append((row['orientation'], r, q, frozenset(row['support']), row['role']))
    return out


def class_label(cls):
    return '%s r=%d s=%d' % (cls[0], cls[1], cls[2])


def class_base(anchor, cls):
    orient, r, q = cls[0], cls[1], cls[2]
    return (4 * anchor[0] + r, 2 * anchor[1] + q, anchor[2]), ORIENT[orient]


def face_key(face):
    return (face[0], face[1][:3])


def owner_set(face):
    b, cls = face
    return frozenset(add(b, d) for d in cls[3])


def face_link_set(face):
    base, (a, c) = class_base(*face)
    return frozenset(face_links(base, a, c))


def faces_containing(u, classes):
    """Translation covariance: face (b,k) has u in its owner set iff b = u - d with d in K_k."""
    out = []
    for cls in classes:
        for d in sorted(cls[3]):
            out.append((sub(u, d), cls))
    return out


def group_of(face):
    """Route B: omitted faces go to the whole star of their anchor, selected faces to the single-factor group."""
    b, cls = face
    return ('star', b) if cls[4] == 'omitted' else ('single', b)


def group_support(group):
    kind, b = group
    return frozenset(add(b, d) for d in S_STAR) if kind == 'star' else frozenset([b])


def derive_counts(rows):
    classes = expand_classes(rows)
    at0 = faces_containing(ORIGIN, classes)
    sets0 = {}
    for f in at0:
        sets0[owner_set(f)] = sets0.get(owner_set(f), 0) + 1
    meet = {}
    for u in COVER_R:
        for f in faces_containing(u, classes):
            meet[face_key(f)] = f
    rset = frozenset(COVER_R)
    inside = [f for f in meet.values() if owner_set(f) <= rset]
    contain = [f for f in meet.values() if rset <= owner_set(f)]
    meet_sets = {}
    for f in meet.values():
        meet_sets[owner_set(f)] = meet_sets.get(owner_set(f), 0) + 1
    offsets = {d: sum(1 for cls in classes if d in cls[3]) for d in S_STAR}
    return {'classes': len(classes), 'faces_per_factor': len(at0), 'owner_sets_per_factor': len(sets0),
            'multiplicities': sorted(sets0.values()), 'sets_at_origin': sets0, 'offset_class_counts': offsets,
            'faces_meeting_R': len(meet), 'faces_inside_R': len(inside), 'faces_containing_R': len(contain),
            'owner_sets_meeting_R': len(meet_sets), 'meet_faces': [meet[k] for k in sorted(meet)]}


def coarse_box(N):
    rng = range(-N, N + 1)
    return frozenset((x, y, z) for x in rng for y in rng for z in rng)


def box_groups(N):
    """Route-B retention in Lambda_N: whole stars b+S inside, every single-factor group of the box."""
    box = coarse_box(N)
    stars = [('star', b) for b in sorted(box) if all(add(b, d) in box for d in S_STAR)]
    singles = [('single', b) for b in sorted(box)]
    return box, stars + singles


def brute_force_faces(xr, yr, zr):
    """Independent fine-lattice enumeration of every elementary plaquette (no class table)."""
    out = []
    for x in xr:
        for y in yr:
            for z in zr:
                p = (x, y, z)
                for a, c in ((0, 1), (0, 2), (1, 2)):
                    out.append((p, a, c, face_support(p, a, c), owner(p), is_selected(p, a, c)))
    return out


# ---------------------------------------------------------------------------
# Exact SU(2) Haar moments (Weyl integration; pi cancels) and link-parity products.
# ---------------------------------------------------------------------------
def cos_integral_over_pi(n):
    if n % 2:
        return Q(0)
    num, den = 1, 1
    for k in range(1, n + 1):
        if k % 2:
            num *= k
        else:
            den *= k
    return Q(num, den)


def haar_moment_W(n):
    """E[W^n] for W=(1/2)Tr U=cos(theta) with density (2/pi) sin^2(theta)."""
    return 2 * (cos_integral_over_pi(n) - cos_integral_over_pi(n + 2))


def haar_expect(link_sets):
    """E[prod W_f] over independent Haar links: zero if some link occurs an odd number of times
    (centre grading); powers of a single face by Weyl; other even products are not needed here."""
    counts = {}
    for f in link_sets:
        for l in f:
            counts[l] = counts.get(l, 0) + 1
    if any(n % 2 for n in counts.values()):
        return Q(0)
    if all(f == link_sets[0] for f in link_sets):
        return haar_moment_W(len(link_sets))
    raise AdmissionError('Haar product outside the implemented cases')


# ---------------------------------------------------------------------------
# Exact rational unit quaternions (SU(2) holonomy fixtures).
# ---------------------------------------------------------------------------
def qmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def qinv(p):
    return (p[0], -p[1], -p[2], -p[3])


def qneg(p):
    return tuple(-x for x in p)


UNIT_Q = [(Q(1, 2), Q(1, 2), Q(1, 2), Q(1, 2)), (Q(3, 5), Q(4, 5), Q(0), Q(0)), (Q(0), Q(3, 5), Q(0), Q(4, 5)),
          (Q(2, 3), Q(1, 3), Q(2, 3), Q(0)), (Q(1, 3), Q(2, 3), Q(0), Q(2, 3)), (Q(0), Q(0), Q(3, 5), Q(-4, 5)),
          (Q(-1, 2), Q(1, 2), Q(-1, 2), Q(1, 2))]


def holonomy_trace(p, a, c, links):
    l1, l2, l3, l4 = face_links(p, a, c)
    u = qmul(qmul(qmul(links[l1], links[l2]), qinv(links[l3])), qinv(links[l4]))
    return u[0]


def in_flip_set(link):
    p, d = link
    return (d == 0 and p[1] % 2 == 0) or (d == 1 and p[2] % 2 == 0) or (d == 2 and p[0] % 2 == 0)


# ---------------------------------------------------------------------------
# Machin pi bracket (directed).
# ---------------------------------------------------------------------------
def atan_inverse_bracket(k, terms=24):
    total, previous = Q(0), Q(0)
    for j in range(terms):
        previous = total
        term = Q(1, (2 * j + 1) * k ** (2 * j + 1))
        total = total + term if j % 2 == 0 else total - term
    return min(previous, total), max(previous, total)


def pi_bracket(denominator=10 ** 30):
    a5 = atan_inverse_bracket(5)
    a239 = atan_inverse_bracket(239)
    lo = 16 * a5[0] - 4 * a239[1]
    hi = 16 * a5[1] - 4 * a239[0]
    lo = Q((lo.numerator * denominator) // lo.denominator, denominator)
    hi = Q(-((-hi.numerator * denominator) // hi.denominator), denominator)
    require(lo < hi and hi - lo < Q(1, 10 ** 25) and Q(314159, 100000) < lo and hi < Q(314160, 100000), 'pi bracket')
    return lo, hi


# ---------------------------------------------------------------------------
# State-lemma tiers: every bound names its tier; mixing is rejected.
# ---------------------------------------------------------------------------
def eps_of(t):
    return 2 * t + t * t


def D_of(eps):
    return 2 * eps * (1 + eps) / (1 + eps * eps)


def assemble(tier, components):
    for name, label, value in components:
        require(label == tier, 'tier mixing rejected: ' + name + ' is tier ' + label + ' inside tier ' + tier)
        require(isinstance(value, Q), 'non-exact component ' + name)
    names = [n for n, _, _ in components]
    if tier == 'ii':
        require('self_consistent_t' in names and 'am2_remainder' in names, 'refined t without the self-consistent inequality')
        remainder = [val for n, _, val in components if n == 'am2_remainder'][0]
        require(remainder > 0, 'AM2 remainder set to zero')
    t = [val for n, _, val in components if n in ('t', 'self_consistent_t')][0]
    eps = eps_of(t)
    return {'t': t, 'eps': eps, 'D': D_of(eps)}


def tier_i(tau, J_per_tau, GR, R, iterate=False):
    J = J_per_tau * abs(tau)
    t = J * GR
    require(t < R, 'tier (i) self-map radius')
    comps = [('J', 'i', J), ('t', 'i', t)]
    out = {'tier': 'i', 'form': "one-step t<=J'*G(R)", 'tau': tau, 'J': J}
    if iterate:
        t2 = J * 16 * (1 + 10 * t) / (1 - 8 * t)     # e^{8t}<=1/(1-8t), directed
        require(0 < t2 <= t, 'iterated tier (i) must not exceed the one-step bound')
        comps = [('J', 'i', J), ('t', 'i', t2)]
        out['form'] = "iterated t<=J'*16*(1+10*t_i)/(1-8*t_i)"
    out.update(assemble('i', comps))
    return out


def tier_ii(tau, J_per_tau, t1_per_tau, GR, GpR, R, form, remainder='contract'):
    J = J_per_tau * abs(tau)
    t1 = t1_per_tau * abs(tau)
    ti = J * GR
    if remainder == 'contract':
        t = t1 / (1 - GpR * J)
        rem = GpR * J * t
    else:
        t = t1 / (1 - 288 * J / (1 - 8 * ti))
        rem = 288 * J * t / (1 - 8 * ti)
    require(t <= ti and t < R, 'tier (ii) t must stay inside the admitted tier (i) ball')
    require(t1 < t and t == t1 + rem, 'self-consistent identity t=t1+remainder')
    comps = [('t1', 'ii', t1), ('am2_remainder', 'ii', rem), ('self_consistent_t', 'ii', t)]
    out = {'tier': 'ii', 'form': form, 'remainder_form': remainder, 'tau': tau, 'J': J, 't1': t1, 'remainder': rem}
    out.update(assemble('ii', comps))
    return out


def tier_record(x):
    keys = ('t', 'eps', 'D', 'J', 't1', 'remainder')
    rec = {k: s(x[k]) for k in keys if k in x}
    rec.update({'tier': x['tier'], 'form': x['form'], 'tau': s(x['tau']), 'D_decimal_preview': dec(x['D']),
                'D_over_2': s(x['D'] / 2), 'two_creation_term_t2': s(x['t'] ** 2),
                'density_part_of_D': s(2 * x['eps'] ** 2 / (1 + x['eps'] ** 2))})
    if 'remainder_form' in x:
        rec['remainder_form'] = x['remainder_form']
    return rec


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q(0)) for j in range(len(b[0]))] for i in range(len(a))]


# ---------------------------------------------------------------------------
# Main computation.
# ---------------------------------------------------------------------------
def compute(check_sha):
    c, contract_digest = load_contract()
    V = contract_values(c)
    tau_cap = V['tau_cap']
    taus = {'+': tau_cap, '-': -tau_cap}
    check('contract_snapshot_sha256', contract_digest == CONTRACT_SHA256 and V['target'] == Q(1, 2500000),
          contract_sha256=contract_digest, target_read_from_contract=s(V['target']),
          reference_values_read_from_contract=V['reference_values'], J0_prime_read_from_contract=s(V['J0p']),
          contract_path=CONTRACT_REL)

    # ======================= item 1: dictionary, box, label =======================
    # AL1: alpha=g^2/(2a), lambda=2/(g^2 a); uniform face coefficient nu=lambda=alpha*tau/24.
    dict_ok = True
    for g2, a in ((Q(3), Q(5, 7)), (Q(1, 2), Q(2)), (Q(97979), Q(1, 1000))):
        alpha = g2 / (2 * a)
        lam = 2 / (g2 * a)
        tau_g = V['face_den'] * lam / alpha
        dict_ok = dict_ok and lam / alpha == 4 / g2 ** 2 and tau_g == V['dict_num'] / g2 ** 2
    g4_cap = V['dict_num'] / tau_cap
    sel_alpha = tau_cap / V['sel_over_alpha_den']        # |lambda_L|/alpha=|lambda_R|/alpha=|mu|/alpha at the cap
    tau_box_max = min(V['box_bridge'], V['box_ends']) * V['sel_over_alpha_den']

    def box_check(triple_over_alpha, tau):
        require(len(triple_over_alpha) == 3, 'three selected coefficients')
        require(all(x == tau / V['face_den'] for x in triple_over_alpha), 'triple is not the uniform value tau/24')
        lam_l, mu, lam_r = triple_over_alpha
        require(abs(lam_l) <= V['box_ends'] and abs(lam_r) <= V['box_ends'] and abs(mu) <= V['box_bridge'],
                'uniform triple outside the admitted coefficient box')
        return True
    label = {
        'model_label': 'uniform Kogut-Susskind SU(2) at fixed spacing, strong bare coupling',
        'regime': 'strong bare coupling: g^4=96/tau, g^4=9.6x10^9 at |tau|=10^-8 (g^4>=9.6x10^9 for |tau|<=10^-8)',
        'route': 'route B: Haar product reference, selected xy faces as single-factor groups',
    }
    check('dictionary_and_box',
          dict_ok and g4_cap == V['g4_cap'] == V['g4_model'] == 9600000000 and V['model_dict_num'] == V['dict_num']
          and V['face_den'] == V['sel_over_alpha_den'] == V['item9_nu_den'] == 24
          and box_check([sel_alpha] * 3, tau_cap) and box_check([-sel_alpha] * 3, -tau_cap) and tau_box_max == 3
          and g4_cap >= 32,
          dictionary='alpha=g^2/(2a), lambda=2/(g^2 a), lambda/alpha=4/g^4, tau=24 lambda/alpha=96/g^4',
          g4_at_cap=s(g4_cap), selected_over_alpha_at_cap=s(sel_alpha), box=['|lambda_L|,|lambda_R|<=alpha/2', '|mu|<=alpha/8'],
          tau_box_limit=s(tau_box_max), bridge_condition_g4_ge_32=True,
          negative_tau_note='tau=96/g^4>0 for real g; tau=-10^-8 is the U_E mirror (item 9), not a real-g dictionary point')

    def triple_mut(t3, tau):
        return lambda: box_check(t3, tau)
    check('uniform_triple_in_box',
          box_check([sel_alpha] * 3, tau_cap)
          and rejected(triple_mut([Q(4) / 24] * 3, Q(4)), 'tau_4_outside_bridge_box')
          and rejected(triple_mut([sel_alpha, Q(0), sel_alpha], tau_cap), 'nonuniform_triple_zero_bridge')
          and rejected(triple_mut([Q(0)] * 3, tau_cap), 'zero_selected_triple_is_not_uniform')
          and rejected(triple_mut([tau_cap / 3] * 3, tau_cap), 'normalized_tau_over_3_read_as_alpha_units'),
          uniform_triple_over_alpha=[s(sel_alpha)] * 3, box_margin_bridge=s(V['box_bridge'] / sel_alpha))

    # ======================= item 2: route-B grouping =======================
    classes = expand_classes(CLASS_ROWS)
    omitted = [k for k in classes if k[4] == 'omitted']
    selected = [k for k in classes if k[4] == 'selected']
    geo_ok = True
    for cls in classes:
        base, (a, cc) = class_base(ORIGIN, cls)
        geo_ok = geo_ok and face_support(base, a, cc) == cls[3] and is_selected(base, a, cc) == (cls[4] == 'selected')
    all_phases = {(o, r, q) for o in ORIENT for r in range(4) for q in range(2)}
    listed = {(k[0], k[1], k[2]) for k in classes}
    union_omitted = frozenset().union(*[k[3] for k in omitted])
    check('anchored_classes_match_fine_geometry',
          geo_ok and listed == all_phases and len(classes) == V['anchored_classes'] == 24
          and len(omitted) == V['omitted_per_anchor'] == 21 and len(selected) == V['selected_per_factor'] == V['psi_faces'] == 3
          and union_omitted == frozenset(S_STAR) and all(k[3] == frozenset([ORIGIN]) for k in selected)
          and all(len(k[3]) >= 2 for k in omitted),
          anchored_classes=len(classes), omitted_classes=len(omitted), selected_classes=len(selected),
          selected_labels=[class_label(k) for k in selected], omitted_union_support=[list(d) for d in sorted(union_omitted)])

    coeff = {class_label(k): UNIFORM_COEFFICIENT_OVER_TAU for k in classes}
    star_norm = sum((abs(coeff[class_label(k)]) for k in omitted), Q(0))     # ||W_f||<=1
    single_norm = sum((abs(coeff[class_label(k)]) for k in selected), Q(0))
    stars_per_site = len({sub(ORIGIN, d) for d in S_STAR})
    singles_per_site = 1
    J_per_tau = stars_per_site * star_norm + singles_per_site * single_norm
    max_support = max(len(S_STAR), 1)
    termination_order = 2 * max_support
    check('route_b_grouping_and_norms',
          star_norm == V['star_norm'] == 7 and single_norm == 1 and Q(1, V['psi_den']) == -UNIFORM_COEFFICIENT_OVER_TAU
          and J_per_tau == V['cand_J'] == V['item2_J'] == V['cand_J_stars'] + V['cand_J_single'] == 29
          and stars_per_site == V['cand_stars_per_site'] == 4 and max_support == V['item2_support'] == 4
          and termination_order == V['item2_order'] == 8,
          star_norm_over_abs_tau=s(star_norm), single_group_norm_over_abs_tau=s(single_norm),
          norm_argument='||W_f||<=1 for W_f=(1/2)Tr U_f; three selected faces times tau/3 give ||psi_b||<=|tau| (equality at the identity configuration)',
          J_prime_over_abs_tau=s(J_per_tau), groups_per_site={'stars': stars_per_site, 'single_factor': singles_per_site},
          max_support_sites=max_support, nested_termination_order=termination_order)

    # brute-force partition: every fine plaquette in a region lies in exactly one route-B group
    brute = brute_force_faces(range(-8, 12), range(-4, 6), range(-2, 4))
    group_faces = {}
    part_ok = True
    for (p, a, cc, supp, anc, sel) in brute:
        g = ('single', anc) if sel else ('star', anc)
        part_ok = part_ok and supp <= group_support(g) and (len(supp) == 1) == sel
        group_faces.setdefault(g, []).append((p, a, cc))
    # the region consists of complete coarse blocks, so every group seen is complete
    per_group_ok = all(len(v1) == (3 if g[0] == 'single' else 21) for g, v1 in group_faces.items())
    check('brute_force_group_partition',
          part_ok and per_group_ok and len(brute) == sum(len(v1) for v1 in group_faces.values()),
          plaquettes_enumerated=len(brute), groups_seen=len(group_faces),
          rule='anchor=owner(base point); selected xy faces (y even, x mod 4 in {0,1,2}) -> single-factor group; all others -> whole star')

    # ======================= item 3: re-frozen contraction =======================
    R = V['R']
    x8 = Q(8) * R
    lower = sum((x8 ** k / factorial(k) for k in range(13)), Q(0))
    tail = x8 ** 13 / factorial(13) / (1 - x8 / 14)
    exp_upper = lower + tail
    require(exp_upper < Q(8, 7), 'exp(1/8)<8/7')
    GR = 16 * Q(8, 7) * (1 + 10 * R)
    GpR = 16 * Q(8, 7) * (8 * (1 + 10 * R) + 10)
    J0p = V['J0p']
    Jcap = J_per_tau * tau_cap
    selfmap = J0p * GR
    exclusion = 2 * J0p * GpR
    J0_old = Q(7, 25000000)
    selfmap_tau_limit = R / GR / J_per_tau            # largest |tau| with J'G(R)<=R
    exclusion_tau_limit = 1 / (2 * GpR) / J_per_tau
    check('am2_contraction_refrozen',
          GR == V['GR_upper'] == Q(148, 7) and GpR == V['GpR_upper'] == 352 and J0p == Jcap == Q(29, 10 ** 8)
          and selfmap == V['selfmap_rational'] == Q(1073, 175000000) and selfmap < R
          and exclusion == V['exclusion_rational'] == Q(319, 1562500) and exclusion < 1 and J0p * GpR < 1,
          exp_one_eighth_upper=s(exp_upper), G_R_upper=s(GR), G_prime_R_upper=s(GpR), J0_prime=s(J0p),
          self_map=s(selfmap), self_map_bound=s(R), exclusion=s(exclusion), lipschitz=s(J0p * GpR),
          derivation="G(t)=16e^{8t}(1+10t), G'(t)=16e^{8t}(18+80t); e^{1/8}<8/7; G(1/64)<16(8/7)(1+10/64)=148/7, "
                     "G'(1/64)<16(8/7)(18+80/64)=352; J_0'G(R)<(29/10^8)(148/7)=1073/175000000; 2J_0'G'(R)<2(29/10^8)352=319/1562500",
          self_map_tau_limit=s(selfmap_tau_limit), exclusion_tau_limit=s(exclusion_tau_limit),
          slack_over_cap=dec(selfmap_tau_limit / tau_cap, 6), contract_source_sha256=contract_digest)

    # nested termination: 2p with p the support size; four-qubit (p=4) and one-qubit (p=1) fixtures
    def nested_fixture(n):
        size = 2 ** n
        full = size - 1
        Cm = [[0] * size for _ in range(size)]
        Vm = [[0] * size for _ in range(size)]
        for b in range(size):
            Vm[b ^ full][b] = 1
            for j in range(n):
                if not (b >> j) & 1:
                    Cm[b | (1 << j)][b] += 1

        def mm(a1, b1):
            return [[sum(a1[i][k] * b1[k][j] for k in range(size)) for j in range(size)] for i in range(size)]
        A = Vm
        orders = []
        for k in range(1, 2 * n + 2):
            A = [[x1 - y1 for x1, y1 in zip(r1, r2)] for r1, r2 in zip(mm(Cm, A), mm(A, Cm))]
            orders.append((k, A[full][0], all(x1 == 0 for row in A for x1 in row)))
        return orders
    f4 = nested_fixture(4)
    f1 = nested_fixture(1)

    def Lnum(p, k):
        return 2 ** p * (2 * p) ** k * (1 + Q(k * (p + 1), p))
    const_ok = all(Lnum(4, k) == 16 * 8 ** k * (1 + Q(5 * k, 4)) for k in range(9))
    mono_ok = all(Lnum(p, k) <= Lnum(4, k) for p in (1, 2, 3, 4) for k in range(9))
    check('nested_termination_fixtures',
          f4[7][1] == factorial(8) and f4[8][2] and f1[1][1] == -2 and f1[2][2] and const_ok and mono_ok,
          four_site_order8_vacuum_coefficient=f4[7][1], four_site_order9_zero=f4[8][2],
          one_site_order2_vacuum_coefficient=f1[1][1], one_site_order3_zero=f1[2][2],
          majorant='2^p(2p)^k(1+k(p+1)/p) is increasing in p; p=4 gives 16*8^k(1+5k/4) and covers |X|=1 groups')

    # on-site theorem, gauge invariance, nonzero physical excited sector
    cas = [Q(j2 * (j2 + 2), 4) for j2 in range(0, 7)]   # j=j2/2: j(j+1)=j2(j2+2)/4
    first_positive = min(x1 for x1 in cas if x1 > 0)
    onsite_gap = V['onsite_factor'] * first_positive
    gauge_ok = True
    g_links = {}
    idx = 0
    for p in [(x1, y1, z1) for x1 in range(-1, 5) for y1 in range(-1, 3) for z1 in range(-1, 3)]:
        for d in range(3):
            g_links[(p, d)] = UNIT_Q[idx % len(UNIT_Q)]
            idx += 1
    gauge = {}
    for n1, p in enumerate(sorted({l[0] for l in g_links} | {add(l[0], E_UNIT[l[1]]) for l in g_links})):
        gauge[p] = UNIT_Q[(3 * n1 + 1) % len(UNIT_Q)]
    transformed = {l: qmul(qmul(gauge[l[0]], U), qinv(gauge[add(l[0], E_UNIT[l[1]])])) for l, U in g_links.items()}
    test_faces = [((0, 0, 0), 0, 2), ((0, 0, 0), 0, 1), ((1, 0, 0), 0, 1), ((2, 0, 0), 0, 1), ((0, 0, 1), 0, 1), ((3, 1, 0), 1, 2)]
    for (p, a, cc) in test_faces:
        gauge_ok = gauge_ok and holonomy_trace(p, a, cc, g_links) == holonomy_trace(p, a, cc, transformed)
    EW, EW2 = haar_moment_W(1), haar_moment_W(2)
    check('onsite_theorem_gauge_and_excited_sector',
          first_positive == Q(3, 4) and onsite_gap == V['item3_gap'] == 6 and V['onsite_factor'] == V['item3_onsite'] == 8
          and onsite_gap >= 1 and gauge_ok and EW == 0 and EW2 == Q(1, 4),
          onsite='h_b=8 sum_e C_e on 24 Haar links; spec C_e={j(j+1)}; kernel = constants (Haar vacuum Omega_b); next eigenvalue 8*3/4=6; h_b>=6Q_b>=Q_b',
          gauge='Omega_b constant, C_e commutes with left/right translations, W_f gauge invariant (exact quaternion fixture on 6 faces incl. W and selected)',
          excited_sector='Omega_0 and 2W_g Omega_0 (g selected) are orthonormal gauge-invariant vectors (E[W]=0, E[W^2]=1/4), so H_phys has dimension>=2 and meets psi-perp',
          first_positive_casimir=s(first_positive), onsite_gap=s(onsite_gap))

    check('uniform_finite_volume_theorem',
          J_per_tau * tau_cap <= J0p and selfmap < R and exclusion < 1 and onsite_gap >= 1 and max_support <= 4
          and V['gap_normalized'] == Q(1, 2) and V['gap_physical_den'] == 2 * 8,
          statement='for every nonempty finite complete-factor volume with route-B retention (whole stars b+S inside, all single-factor groups), '
                    'both signs |tau|<=10^-8: unique ground psi=e^{-C}Omega_0, full-space gap>=1/2 normalized (alpha/16 physical), '
                    'gauge-invariant ground, nonzero physical excited sector; cutoff removal as AM2 section 6 (Casimir on-site, compact resolvent)',
          gap_physical='alpha/16', inputs=['h_b>=Q_b', 'support<=4', "J'<=J_0'=29/10^8", "J_0'G(R)<1/64", "2J_0'G'(R)<1"])

    # ======================= item 5/10: incidence, itemized =======================
    rset = frozenset(COVER_R)
    incident = sorted({sub(u, d) for u in COVER_R for d in S_STAR})
    star_groups_R = [('star', b) for b in incident]
    single_groups_R = [('single', u) for u in COVER_R]

    def group_faces_list(g):
        kind, b = g
        return [(b, k) for k in (omitted if kind == 'star' else selected)]

    def face_record(f):
        base, (a, cc) = class_base(*f)
        M = owner_set(f)
        return {'class': class_label(f[1]), 'base_fine': list(base), 'owner_set': sorted(list(y) for y in M),
                'meets_R': bool(M & rset), 'inside_R': M <= rset, 'is_wilson_W': (base, (a, cc)) == (ORIGIN, (0, 2))}
    table = []
    for g in star_groups_R + single_groups_R:
        fl = group_faces_list(g)
        recs = [face_record(f) for f in fl]
        table.append({'group': g[0], 'anchor': list(g[1]), 'support': sorted(list(y) for y in group_support(g)),
                      'R_sites_met': sorted(list(u) for u in COVER_R if u in group_support(g)),
                      'norm_over_abs_tau': s(star_norm if g[0] == 'star' else single_norm),
                      'faces': recs, 'faces_total': len(recs), 'faces_meeting_R': sum(1 for r1 in recs if r1['meets_R'])})

    def totals_from_table(tb):
        stars = [e for e in tb if e['group'] == 'star']
        singles = [e for e in tb if e['group'] == 'single']
        sel_faces = sum(e['faces_total'] for e in singles)
        B = sum((rat(e['norm_over_abs_tau']) for e in tb), Q(0)) / 8
        keys = set()
        for e in tb:
            for fr in e['faces']:
                key = (tuple(fr['base_fine']), fr['class'])
                require(key not in keys, 'face charged twice in the incidence table')
                keys.add(key)
                require(fr['meets_R'] == any(tuple(y) in rset for y in fr['owner_set']), 'face row meets_R inconsistent')
        require(all(e['R_sites_met'] for e in tb), 'a tabulated group does not meet R')
        return {'stars': len(stars), 'singles': len(singles), 'selected_faces': sel_faces, 'B_over_abs_tau': B,
                'k_over_abs_tau': 2 * B, 'star_faces_meeting_R': sum(e['faces_meeting_R'] for e in stars),
                'faces_meeting_R': sum(e['faces_meeting_R'] for e in tb), 'faces_in_groups': sum(e['faces_total'] for e in tb)}
    tot = totals_from_table(table)

    # all-size argument by translation covariance plus finite enumeration of boxes N=1..4
    covariance_ok = all((bool(group_support(g) & rset)) == (g[1] in incident) for g in
                        [('star', b) for b in coarse_box(3)]) and all(
        (bool(group_support(g) & rset)) == (g[1] in COVER_R) for g in [('single', b) for b in coarse_box(3)])
    box_counts = {}
    for N in (1, 2, 3, 4):
        box, groups = box_groups(N)
        meet = [g for g in groups if group_support(g) & rset]
        box_counts[N] = (sum(1 for g in meet if g[0] == 'star'), sum(1 for g in meet if g[0] == 'single'))
    check('incidence_all_sizes',
          covariance_ok and all(box_counts[N] == (7, 2) for N in (2, 3, 4)) and box_counts[1][0] < 7
          and tot['stars'] == V['cand_stars_R'] == 7 and tot['singles'] == V['cand_single_groups'] == V['item5_singles'] == 2
          and tot['selected_faces'] == V['cand_selected_faces_R'] == V['item5_faces'] == 6
          and tot['B_over_abs_tau'] == V['cand_B'] == V['item5_B'] == Q(51, 8)
          and 7 * star_norm / 8 == V['cand_B_stars'] and 2 * single_norm / 8 == V['cand_B_singles']
          and tot['k_over_abs_tau'] == V['cand_k'] == V['item5_k'] == Q(51, 4),
          incident_anchors=[list(b) for b in incident], box_counts={str(N): list(v1) for N, v1 in box_counts.items()},
          B_N_over_abs_tau=s(tot['B_over_abs_tau']), k_prime_over_abs_tau=s(tot['k_over_abs_tau']),
          faces_in_groups_meeting_R=tot['faces_in_groups'], faces_meeting_R_in_table=tot['faces_meeting_R'],
          argument='a star b+S meets R iff b in R-S (seven anchors, all retained for N>=2); a single-factor group {b} meets R iff b in R')

    # ======================= item 4: reset budget and the AQ1/AQ2 checklist =======================
    reset = 2 * (tot['stars'] * star_norm + tot['singles'] * single_norm)
    eps_R = reset / onsite_gap
    reset_gap_one = reset / 1
    C_F_per_site = 2 * (stars_per_site * star_norm + singles_per_site * single_norm)
    F_norm_factor = (1 + 2) ** 4
    Phi_F = F_norm_factor * J_per_tau
    sqrtD_sq = 4 * eps_R * tau_cap                        # (2 sqrt(eps))^2 at the cap
    sqrtD_gap_one_sq = 4 * reset_gap_one * tau_cap
    var_floor = Q(1, 4) - Q(1, 500) - Q(1, 500) ** 2
    checklist = [
        {'step': 'AQ1 reset energy on a finite region F', 'status': 'new constant', 'constant': "2(4*7+1)|tau||F|=58|tau||F| (was 56)"},
        {'step': 'AQ1 trace-norm compactness and diagonal extraction', 'status': 'verbatim re-application', 'constant': 'uses C_F only'},
        {'step': 'Nachtergaele-Sims placement', 'status': 'new constant', 'constant': "||F||<=7, convolution<=224 unchanged; ||Phi'||_F<=81 J'=2349|tau| (was 2268)"},
        {'step': 'AQ1 stationarity', 'status': 'verbatim re-application', 'constant': 'none'},
        {'step': 'AQ1 GNS strong continuity', 'status': 'verbatim re-application', 'constant': 'none'},
        {'step': 'AQ1 nonnegativity of H_num', 'status': 'verbatim re-application', 'constant': 'none'},
        {'step': 'AQ2 endpoint group, Haar projection, physical space', 'status': 'verbatim re-application', 'constant': 'gauge invariance of route-B H'},
        {'step': 'AQ2 physical gap alpha/16 (full GNS)', 'status': 'verbatim re-application with the re-frozen AM2 gap', 'constant': "J_0'=29/10^8"},
        {'step': 'reset on the cover R (AQ2 HNM-AQ2.8)', 'status': 'new constant', 'constant': 'omega(h_R)<=2(7*7+2*1)|tau|=102|tau| (was 98)'},
        {'step': 'reset with the Haar reference gap six (AT4 F08)', 'status': 'new constant', 'constant': 'epsilon_R<=17|tau|, D_sqrt=2 sqrt(17|tau|) (square-root control only)'},
        {'step': 'Wilson variance floor (AQ2 HNM-AQ2.10)', 'status': 'new constant (gap six required)', 'constant': '2 sqrt(17|tau|)<=1/500, floor 61999/250000; gap-one route fails 1/500'},
        {'step': 'reference moments Tr(P_R W)=0, Tr(P_R W^2)=1/4', 'status': 'verbatim re-application', 'constant': 'Haar P_R'},
        {'step': 'AT4 seven-star relative-unitary slope', 'status': 'new constant', 'constant': "||B_N||<=51|tau|/8, k'=51|tau|/4"},
        {'step': 'AV1 cutoff-vector removal', 'status': 'verbatim re-application', 'constant': 'selected face vectors also at energy 24; L>=24 keeps c^(1)'},
        {'step': 'AV1 passage to AQ subsequential limits', 'status': 'verbatim re-application', 'constant': 'local trace-norm convergence'},
    ]
    check('aq_reinstantiation_checklist',
          reset == V['cand_reset'] == V['item4_reset'] == 102 and eps_R == V['cand_eps_R'] == 17
          and V['cand_reset_stars'] == tot['stars'] and V['cand_reset_star_norm'] == star_norm and V['cand_reset_single'] == tot['singles'] * single_norm
          and V['item4_gap'] == onsite_gap and C_F_per_site == 58 and Phi_F == 2349
          and sqrtD_sq <= Q(1, 500) ** 2 and sqrtD_gap_one_sq > Q(1, 500) ** 2 and var_floor == Q(61999, 250000),
          reset_over_abs_tau=s(reset), eps_R_over_abs_tau=s(eps_R), C_F_per_site_over_abs_tau=s(C_F_per_site),
          Phi_F_norm_over_abs_tau=s(Phi_F), sqrt_control_squared_at_cap=s(sqrtD_sq),
          sqrt_control_preview=dec(sqrt_up(sqrtD_sq, 10 ** 15)), gap_one_route_squared_at_cap=s(sqrtD_gap_one_sq),
          variance_floor=s(var_floor), table=checklist)

    # ======================= item 6: per-factor enumeration and the first-order tier =======================
    counts = derive_counts(CLASS_ROWS)
    counts_omitted = derive_counts(tuple(r1 for r1 in CLASS_ROWS if r1['role'] == 'omitted'))
    bulk_sets = counts['sets_at_origin']
    check('per_factor_face_count_derived',
          counts['classes'] == 24 and counts['faces_per_factor'] == 52
          and counts['offset_class_counts'] == {ORIGIN: 24, (1, 0, 0): 4, (0, 1, 0): 8, EZ: 16}
          and counts['owner_sets_per_factor'] == 16 and counts['multiplicities'] == [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 10, 10]
          and counts['faces_meeting_R'] == 88 and counts['faces_inside_R'] == 16 and counts['faces_containing_R'] == 16
          and counts['owner_sets_meeting_R'] == 29
          and (counts_omitted['faces_per_factor'], counts_omitted['owner_sets_per_factor'], counts_omitted['faces_meeting_R'],
               counts_omitted['faces_inside_R']) == (49, 15, 82, 10)
          and counts['faces_per_factor'] <= V['bound_per_factor'] == V['item6_cand_factor'] == V['bound_anchors'] * V['bound_classes'] == 96
          and counts['faces_meeting_R'] <= V['bound_R'] == V['item6_cand_R'] == len(incident) * V['bound_classes'] == 168,
          faces_per_factor=counts['faces_per_factor'], offset_class_counts={'0': 24, 'e_x': 4, 'e_y': 8, 'e_z': 16},
          owner_sets_per_factor=counts['owner_sets_per_factor'], multiplicities=counts['multiplicities'],
          faces_meeting_R=counts['faces_meeting_R'], faces_inside_R=counts['faces_inside_R'],
          faces_containing_R=counts['faces_containing_R'], owner_sets_meeting_R=counts['owner_sets_meeting_R'],
          omitted_only_cross_reference=[49, 15, 82, 10],
          candidate_bounds={'per_factor': V['bound_per_factor'], 'R': V['bound_R'], 'status': 'labelled upper bounds (4x24, 7x24), not exact counts'},
          owner_sets_at_origin=sorted([sorted(list(y) for y in M), n] for M, n in bulk_sets.items()))

    # brute-force confirmation and boundary counts at most bulk
    b0 = [f for f in brute if ORIGIN in f[3]]
    bR = [f for f in brute if f[3] & rset]
    bsets = {}
    for f in b0:
        bsets[f[3]] = bsets.get(f[3], 0) + 1
    boundary_ok = True
    for N in (1, 2, 3):
        box, groups = box_groups(N)
        per_site = {}
        per_set = {}
        Jsite = {}
        for g in groups:
            for u in group_support(g):
                Jsite[u] = Jsite.get(u, Q(0)) + (star_norm if g[0] == 'star' else single_norm)
            for f in group_faces_list(g):
                M = owner_set(f)
                per_set[M] = per_set.get(M, 0) + 1
                for u in M:
                    per_site[u] = per_site.get(u, 0) + 1
        boundary_ok = boundary_ok and max(per_site.values()) <= 52 and max(Jsite.values()) <= J_per_tau
        for M, nM in per_set.items():
            m0 = min(M)
            canon = frozenset(sub(y, m0) for y in M)
            bulk = [n for M2, n in bulk_sets.items() if frozenset(sub(y, min(M2)) for y in M2) == canon]
            boundary_ok = boundary_ok and bool(bulk) and nM <= bulk[0]
    check('boundary_counts_at_most_bulk',
          boundary_ok and len(b0) == 52 and bsets == bulk_sets and len(bR) == 88,
          brute_force_faces_at_origin=len(b0), brute_force_faces_meeting_R=len(bR), boxes=[1, 2, 3])

    # face vectors: energy 24, norm 1/2, orthogonal (distinct faces share at most one link)
    meet_faces = counts['meet_faces']
    link_sets = [face_link_set(f) for f in meet_faces]
    max_shared = max(len(link_sets[i] & link_sets[j]) for i in range(len(link_sets)) for j in range(i + 1, len(link_sets)))
    energy = V['onsite_factor'] * 4 * Q(3, 4)
    check('face_vectors_energy_norm_orthogonality',
          energy == 24 and haar_moment_W(2) == Q(1, 4) and max_shared <= 1
          and all(haar_expect([link_sets[i], link_sets[j]]) == (Q(1, 4) if i == j else 0)
                  for i in range(len(link_sets)) for j in range(len(link_sets)) if i <= j and (i == j or len(link_sets[i] & link_sets[j]) == 1)),
          normalized_energy=s(energy), norm_WfOmega0='1/2', max_shared_links=max_shared, faces_checked=len(meet_faces),
          first_order_coefficient_per_face='-tau/72 (normalized -(tau/3)/24 = alpha units -(tau/24)/3)')

    coef = Q(1, 144)
    t1_per_tau = counts['faces_per_factor'] * coef
    grouped = sum((sqrt_up(n) for n in bulk_sets.values()), Q(0))
    t1g_per_tau = grouped * coef
    t1_96_per_tau = V['bound_per_factor'] * coef
    tiers = {}
    for sg, tv in taus.items():
        tiers[sg] = {
            'i': tier_i(tv, J_per_tau, GR, R),
            'i_iterated': tier_i(tv, J_per_tau, GR, R, iterate=True),
            'ii': tier_ii(tv, J_per_tau, t1_per_tau, GR, GpR, R, 'triangle t_1=52|tau|/144'),
            'ii_grouped': tier_ii(tv, J_per_tau, t1g_per_tau, GR, GpR, R, 'grouped sum sqrt(n_M) (directed)'),
            'ii_sharper': tier_ii(tv, J_per_tau, t1_per_tau, GR, GpR, R, 'triangle, remainder G(t)-16<=288t/(1-8t)', remainder='sharper'),
            'ii_bound96': tier_ii(tv, J_per_tau, t1_96_per_tau, GR, GpR, R, 'labelled bound t_1=96|tau|/144'),
        }
    Dp, Dm = tiers['+'], tiers['-']
    target = V['target']
    tier_ii_target_met = all(tiers[sg]['ii']['D'] <= target for sg in taus)
    check('state_lemma_tier_i',
          Dp['i']['D'] == Dm['i']['D'] and Dp['i']['t'] == selfmap and Dp['i']['D'] > target and Dp['i']['D'] > Q(1, 10 ** 6),
          D_i_plus=s(Dp['i']['D']), D_i_minus=s(Dm['i']['D']), D_i_preview=dec(Dp['i']['D']), t_i=s(Dp['i']['t']),
          meets_target=False, retained=True)
    check('state_lemma_tier_ii',
          tier_ii_target_met and Dp['ii']['D'] == Dm['ii']['D'] and t1_per_tau == Q(13, 36) and Dp['ii']['D'] < Q(1, 10 ** 6),
          D_ii_plus=s(Dp['ii']['D']), D_ii_minus=s(Dm['ii']['D']), D_ii_preview=dec(Dp['ii']['D']),
          t1_over_abs_tau=s(t1_per_tau), T=s(Dp['ii']['t']), remainder=s(Dp['ii']['remainder']), eps=s(Dp['ii']['eps']),
          target=s(target), meets_target=tier_ii_target_met, margin_preview=dec(target / Dp['ii']['D'], 6))
    check('state_lemma_variants',
          all(tiers['+'][k]['D'] <= target for k in ('ii_grouped', 'ii_sharper', 'ii_bound96'))
          and tiers['+']['ii_grouped']['D'] < tiers['+']['ii']['D'] < tiers['+']['ii_bound96']['D']
          and V['d_prime_candidate'][0] <= tiers['+']['ii_bound96']['D'] <= V['d_prime_candidate'][1]
          and not (V['d_prime_candidate'][0] <= tiers['+']['ii']['D'] <= V['d_prime_candidate'][1])
          and tiers['+']['i_iterated']['D'] > target,
          grouped_sqrt_sum_upper=s(grouped), grouped_preview=dec(tiers['+']['ii_grouped']['D']),
          sharper_preview=dec(tiers['+']['ii_sharper']['D']), bound96_preview=dec(tiers['+']['ii_bound96']['D']),
          bound96_D=s(tiers['+']['ii_bound96']['D']), iterated_tier_i_preview=dec(tiers['+']['i_iterated']['D']),
          contract_candidate_range=[s(V['d_prime_candidate'][0]), s(V['d_prime_candidate'][1])],
          note='the contract candidate 2-3x10^-8 corresponds to the labelled 96-bound; the derived 52-face count gives about 1.44x10^-8')

    # AX2 feasibility arithmetic of the contract note (not the window lemma)
    pi_lo, pi_hi = pi_bracket()
    kdyn = V['ax2_k_num'] * tau_cap
    goal = Q(1, 10 ** V['ax2_goal_exp'])

    def F_up(D):
        return 2 * (D + D * D) + kdyn / pi_lo

    def F_low(D):
        return 2 * (D + D * D) + kdyn / pi_hi
    thr_lo, thr_hi = Q(4188, 10 ** 10), Q(4189, 10 ** 10)
    check('ax2_feasibility_arithmetic',
          F_up(Dp['ii']['D']) <= goal and F_up(target) <= goal and F_up(thr_lo) <= goal and F_low(thr_hi) > goal
          and F_low(V['ax2_note_threshold']) > goal and V['ax2_k_num'] == tot['k_over_abs_tau'] * 4 and F_low(Dp['i']['D']) > goal,
          F_at_D_ii_upper_preview=dec(F_up(Dp['ii']['D']), 8), threshold_bracket=[s(thr_lo), s(thr_hi)],
          contract_note_threshold=s(V['ax2_note_threshold']),
          finding='the contract note D<=4.19x10^-7 is rounded upward: F(4.19x10^-7)>10^-6; the exact threshold lies in [4.188,4.189]x10^-7; the target 4/10^7 is below it',
          note='arithmetic of the contract statement only; the AX2 window certificate is not proved here')

    # scaling
    tau_s = tau_cap / 100
    scal = {'i': tier_i(tau_s, J_per_tau, GR, R), 'ii': tier_ii(tau_s, J_per_tau, t1_per_tau, GR, GpR, R, 'scaling')}
    ratios = {k1: Dp[k1]['D'] / scal[k1]['D'] for k1 in ('i', 'ii')}
    sq_ratio_sq = (4 * eps_R * tau_cap) / (4 * eps_R * tau_s)
    lin_ok = all(99 <= r1 <= 101 for r1 in ratios.values())
    check('tau_scaling_exponent',
          lin_ok and sq_ratio_sq == 100
          and rejected(lambda: require(Q(99) ** 2 <= sq_ratio_sq <= Q(101) ** 2, 'square-root control relabelled linear'), 'sqrt_relabelled_linear')
          and rejected(lambda: require(all(Q(99, 10) <= r1 <= Q(101, 10) for r1 in ratios.values()), 'linear bound read as square root'), 'linear_read_as_sqrt'),
          ratio_tier_i_preview=dec(ratios['i'], 9), ratio_tier_ii_preview=dec(ratios['ii'], 9), sqrt_control_ratio='10 exactly')

    # ======================= item 7/9: parity and coefficient transfer =======================
    flip_counts = {}
    for o, (a, cc) in ORIENT.items():
        for px in range(2):
            for py in range(2):
                for pz in range(2):
                    p = (px, py, pz)
                    flip_counts[(o, p)] = sum(1 for l in face_links(p, a, cc) if in_flip_set(l))
    anchored_flip = []
    for b in [(x1, y1, z1) for x1 in (-1, 0, 1) for y1 in (-1, 0, 1) for z1 in (-1, 0, 1)]:
        for k in classes:
            base, (a, cc) = class_base(b, k)
            anchored_flip.append(sum(1 for l in face_links(base, a, cc) if in_flip_set(l)))
    box_flip = [sum(1 for l in face_links(f[0], f[1], f[2]) if in_flip_set(l)) for f in brute]
    W_flip = sum(1 for l in face_links(ORIGIN, 0, 2) if in_flip_set(l))
    q_flip_ok = True
    for (p, a, cc) in test_faces:
        flipped = {l: (qneg(U) if in_flip_set(l) else U) for l, U in g_links.items()}
        q_flip_ok = q_flip_ok and holonomy_trace(p, a, cc, flipped) == -holonomy_trace(p, a, cc, g_links)
    check('flip_set_odd_all_classes',
          all(n1 in (1, 3) for n1 in flip_counts.values()) and len(flip_counts) == 24
          and all(n1 in (1, 3) for n1 in anchored_flip) and len(anchored_flip) == 27 * 24
          and all(n1 in (1, 3) for n1 in box_flip) and W_flip == 3 and q_flip_ok
          and rejected(lambda: require(all(n1 - (1 if (o, p) == ('xy', (0, 0, 0)) else 0) in (1, 3)
                                           for (o, p), n1 in flip_counts.items()), 'E minus one link'), 'E_minus_one_link'),
          parity_classes=24, anchored_faces_checked=len(anchored_flip), fine_region_plaquettes=len(box_flip),
          selected_classes_included=True, wilson_face_flip_links=W_flip, quaternion_flip_fixture=q_flip_ok,
          flip_set='E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even}')

    # 3x3 compression {Omega_0, 2W Omega_0, 2W_g Omega_0}, g a selected face of factor 0 sharing link (0,x) with W
    Wl = face_link_set((ORIGIN, [k for k in omitted if (k[0], k[1], k[2]) == ('xz', 0, 0)][0]))
    gsel = (ORIGIN, [k for k in selected if (k[0], k[1], k[2]) == ('xy', 0, 0)][0])
    Gl = face_link_set(gsel)
    basis = [[], [Wl], [Gl]]
    norms = [Q(1), Q(2), Q(2)]

    def mult_matrix(face_links_):
        return [[norms[i] * norms[j] * haar_expect(basis[i] + [face_links_] + basis[j]) for j in range(3)] for i in range(3)]
    MW, MG = mult_matrix(Wl), mult_matrix(Gl)
    gram = [[norms[i] * norms[j] * (haar_expect(basis[i] + basis[j]) if basis[i] + basis[j] else Q(1)) for j in range(3)] for i in range(3)]
    H0 = [[Q(0), Q(0), Q(0)], [Q(0), energy, Q(0)], [Q(0), Q(0), energy]]

    def Hc(tau, kappa):
        return [[H0[i][j] - tau / 3 * MW[i][j] - kappa / 3 * MG[i][j] for j in range(3)] for i in range(3)]
    Dflip = [[Q(1), Q(0), Q(0)], [Q(0), Q(-1), Q(0)], [Q(0), Q(0), Q(-1)]]

    def conj(M):
        return matmul(matmul(Dflip, M), Dflip)
    tau_f = Q(1, 7)
    uniform_ok = conj(Hc(tau_f, tau_f)) == Hc(-tau_f, -tau_f) and conj(Hc(tau_f, Q(2, 9))) == Hc(-tau_f, Q(-2, 9))

    def claim_uniform_flip(kappa_of_tau):
        require(conj(Hc(tau_f, kappa_of_tau(tau_f))) == Hc(-tau_f, kappa_of_tau(-tau_f)), 'flip identity H(tau)->H(-tau) fails: kappa not tied to tau')
        return True
    check('uniform_flip_identity',
          gram == [[1, 0, 0], [0, 1, 0], [0, 0, 1]] and uniform_ok and claim_uniform_flip(lambda t: t)
          and Wl & Gl and len(Wl & Gl) == 1,
          compression_H_tau_kappa=[[s(x1) for x1 in row] for row in Hc(tau_f, Q(2, 9))], tau_fixture=s(tau_f),
          flip_identity='U_E H_N(tau) U_E^* = H_N(-tau) for the uniform model: every face coefficient is -(tau/3) (normalized), every W_f is E-odd, '
                   'the on-site Casimir sum and its cutoffs commute with U_E',
          shared_link_W_and_selected=[list(l[0]) + [l[1]] for l in sorted(Wl & Gl)])
    check('uniform_kappa_tied_to_tau',
          claim_uniform_flip(lambda t: t)
          and rejected(lambda: claim_uniform_flip(lambda t: t + Q(1, 1000)), 'kappa_offset_from_tau')
          and rejected(lambda: claim_uniform_flip(lambda t: Q(1, 100)), 'kappa_fixed_nonzero')
          and rejected(lambda: claim_uniform_flip(lambda t: 2 * t + Q(1, 50)), 'kappa_affine_not_odd'),
          semantics=V['new_semantics']['uniform_kappa_tied_to_tau'])

    # first-order coefficient: only f=W contributes; selected faces give zero
    first = Q(0)
    contrib = []
    for f, Ls in zip(meet_faces, link_sets):
        e1 = haar_expect([Wl, Ls]) if (Ls == Wl or len(Ls & Wl) <= 1) else None
        require(e1 is not None, 'unexpected face overlap')
        term = 2 * Q(1, 72) * e1                     # omega^(1)/tau = 2 <W Omega_0, psi^(1)>/tau, psi^(1)=(tau/72) sum W_f Omega_0
        first += term
        if term:
            contrib.append(face_record(f)['class'])
    sel_meet = [f for f in meet_faces if f[1][4] == 'selected']
    sel_sharing = [f for f in sel_meet if face_link_set(f) & Wl]
    psi1 = [Q(0), Q(1, 144), Q(1, 144)]               # -H0^{-1}P V Omega_0 per unit tau (kappa=tau) in the compression
    rs_first = 2 * sum((MW[0][j] * psi1[j] for j in range(3)), Q(0))
    check('first_order_coefficient_uniform',
          first == Q(1, V['first_order_den']) == Q(1, V['item9_first']) and contrib == ['xz r=0 s=0'] and rs_first == Q(1, 144)
          and len(sel_meet) == 6 and len(sel_sharing) == 2 and all(haar_expect([Wl, face_link_set(f)]) == 0 for f in sel_meet),
          omega_W_first_order_over_tau=s(first), contributing_faces=contrib, selected_faces_meeting_R=len(sel_meet),
          selected_faces_sharing_a_link_with_W=len(sel_sharing), compression_rayleigh_schrodinger=s(rs_first),
          values={'+': s(tau_cap / 144), '-': s(-tau_cap / 144)})

    # parity rule for selected faces: E[W^2 W_g]=0 and no return of W Omega_0 to energy 24
    def energies_WgW(Ls):
        shared = len(Ls & Wl)
        require(Ls != Wl and shared <= 1, 'selected face distinct from W')
        rest = 8 - 2 * shared
        base_e = V['onsite_factor'] * rest * Q(3, 4)
        return sorted({base_e + V['onsite_factor'] * j * shared for j in (0, 2)}) if shared else [base_e]
    sel_energies = sorted({e1 for f in sel_meet for e1 in energies_WgW(face_link_set(f))})
    pair_sym = sorted({len(link_sets[i] ^ link_sets[j]) for i in range(len(link_sets)) for j in range(i, len(link_sets))})
    check('parity_rule_selected_faces',
          all(haar_expect([Wl, Wl, face_link_set(f)]) == 0 for f in sel_meet) and haar_expect([Wl, Wl, Wl]) == 0
          and 24 not in sel_energies and pair_sym == [0, 6, 8] and haar_moment_W(4) == Q(1, 8),
          E_W2_Wg=0, energies_of_Wg_W_Omega0=[s(e1) for e1 in sel_energies], symmetric_difference_sizes=pair_sym,
          statement='the Z_2 centre grading applies verbatim to selected faces (single spin-1/2 face characters)')

    transfer = [
        {'aw1_statement': 'per-link grading Pi_e commutes with Casimirs, gauge actions, cutoffs; fixes Omega_0', 'transfer': 'verbatim', 'needs': 'none'},
        {'aw1_statement': 'E meets every plaquette in 1 or 3 links', 'transfer': 'verbatim (selected classes enumerated)', 'needs': 'none'},
        {'aw1_statement': 'U_E H_N(tau,kappa) U_E^*=H_N(-tau,-kappa)', 'transfer': 'becomes U_E H_N(tau) U_E^*=H_N(-tau) (kappa tied to tau)', 'needs': 'none'},
        {'aw1_statement': 'cutoff compressions Q_L -> Q_L\'', 'transfer': 'verbatim and simpler: route-B on-site is kappa independent, Q_L\'=Q_L', 'needs': 'none'},
        {'aw1_statement': 'finite-box ground covariance and omega_{N,-tau}(W)=-omega_{N,tau}(W); evenness of omega(W^2), C_N, c_N', 'transfer': 'transfers', 'needs': "unique ground at both signs: route-B AM2 with J_0'"},
        {'aw1_statement': 'AQ passage S(-tau)=S(tau) o alpha_E (whole sets)', 'transfer': 'transfers', 'needs': "route-B AQ1 constants C_F=58|tau||F|, ||Phi'||_F<=2349|tau|"},
        {'aw1_statement': 'parity theorem: first-order vanishing for omega(W^2), c_N, C_N (finite boxes, Kato)', 'transfer': 'transfers (all plaquettes incl. selected)', 'needs': "route-B box gap (J_0')"},
        {'aw1_statement': 'omega_tau(W)=+tau/144+r(tau), only f=W', 'transfer': 'transfers (selected faces orthogonal to W Omega_0, single-factor owner sets)', 'needs': 'none for the coefficient'},
        {'aw1_statement': '|r(tau)|<=K_2^+ tau^2 uniformly in N', 'transfer': 'not transferred', 'needs': "route-B T', rho', eps' and pins (36 single-site faces per R site, 88 faces meeting R); not computed here"},
        {'aw1_statement': 'omega(W^2) uniform constant', 'transfer': 'not transferred', 'needs': 'route-B constants; c^(1)_{0}, c^(1)_{e_z} no longer vanish'},
    ]
    check('aw1_quantifier_transfer', len(transfer) == 10 and sum(1 for t1 in transfer if t1['transfer'] == 'not transferred') == 2,
          table=transfer)

    # ======================= controls: the new AX1 ids =======================
    # reference_route_declared / selected_reference_not_haar
    route_packet = {'route': 'B', 'reference_route': V['reference_route'], 'onsite': 'h_b=8 sum_e C_e', 'J_over_abs_tau': s(J_per_tau),
                    'reset_over_abs_tau': s(reset), 'onsite_gap': s(onsite_gap), 'j0': 'R1'}

    def validate_route(pk):
        require(pk['route'] == 'B' and pk['reference_route'] == 'haar', 'route/reference not declared as route B with Haar reference')
        require(pk['onsite'] == 'h_b=8 sum_e C_e' and rat(pk['onsite_gap']) == 6, 'route B needs the Casimir on-site with gap six')
        require(rat(pk['J_over_abs_tau']) == 29 and rat(pk['reset_over_abs_tau']) == 102, 'route-B constants mixed with route A')
        require(pk['j0'] == 'R1', 'J_0 resolution not declared')
        return True
    rmuts = []
    for key, val in (('route', 'A'), ('reference_route', 'selected_strip'), ('reset_over_abs_tau', '98'), ('J_over_abs_tau', '28'),
                     ('onsite', 'h_b=strip+Casimir'), ('j0', 'undeclared')):
        mp = dict(route_packet)
        mp[key] = val
        rmuts.append(rejected(lambda m=mp: validate_route(m), 'route_mix_' + key))
    check('reference_route_declared', validate_route(route_packet) and len(rmuts) == 6 and V['reference_route'] == 'haar',
          route_packet=route_packet, rejected=rmuts)

    # route-A fixture: selected face on-site (kappa=30, exact eigenvalues), reference correlation is not e^{3i theta}/4
    HA = [[H0[i][j] - Q(30) / 3 * MG[i][j] for j in range(3)] for i in range(3)]
    vA = [Q(5), Q(0), Q(1)]
    HAv = [sum((HA[i][j] * vA[j] for j in range(3)), Q(0)) for i in range(3)]
    ground_ok = HAv == [-vA[i] for i in range(3)]
    nA = sum((x1 * x1 for x1 in vA), Q(0))
    WvA = [sum((MW[i][j] * vA[j] for j in range(3)), Q(0)) for i in range(3)]
    meanA = sum((vA[i] * WvA[i] for i in range(3)), Q(0)) / nA
    chiA = [WvA[i] - meanA * vA[i] for i in range(3)]
    massA = sum((x1 * x1 for x1 in chiA), Q(0)) / nA
    excitedA = [sum((HA[i][j] * chiA[j] for j in range(3)), Q(0)) for i in range(3)]
    freqA = (energy - (-1)) / 8 if excitedA == [energy * x1 for x1 in chiA] else None

    def claim_haar_reference_correlation(mass, freq):
        require(mass == Q(1, 4) and freq == 3, 'route-A reference correlation is not e^{3i theta}/4')
        return True
    # exact sign argument at any kappa!=0 (including the uniform value kappa=tau): det of the {Omega,2W_g Omega} block <0
    offdiag_sq = [(-(kap / 3) * MG[0][2]) ** 2 for kap in (tau_cap, Q(1), Q(30))]   # det=-offdiag^2<0
    trial_lambda = tau_cap / 24                               # AT4 F01 trial energy, alpha=1: -lambda^2/(12 alpha)
    trial = 3 * (trial_lambda / 3) ** 2 / 4 - trial_lambda * (trial_lambda / 3) / 2
    check('selected_reference_not_haar',
          ground_ok and freqA == Q(25, 8) and massA == Q(25, 104) and all(d1 > 0 for d1 in offdiag_sq) and trial == -trial_lambda ** 2 / 12 < 0
          and claim_haar_reference_correlation(Q(1, 4), 3)
          and rejected(lambda: claim_haar_reference_correlation(massA, freqA), 'route_A_reference_claimed_haar_correlation'),
          fixture='finite compression onto {Omega_0,2W Omega_0,2W_g Omega_0}, route-A on-site H_0-(kappa/3)W_g with kappa=30 (outside the box; algebra only), transfers_to_route_A_value:false',
          route_A_fixture_ground_energy='-1', route_A_fixture_mass=s(massA), route_A_fixture_frequency_alpha_units=s(freqA),
          route_B_reference='mass 1/4, frequency 3: c_0(theta)=e^{3i theta}/4',
          sign_argument='for every kappa!=0 the 2x2 block [[0,-kappa/6],[-kappa/6,24]] has determinant -kappa^2/36<0, so the reference ground is not Haar',
          at4_trial_energy_uniform_cap=s(trial))

    # per_site_sum_recomputed
    def validate_J(stars, star_n, singles, single_n):
        Jv = stars * star_n + singles * single_n
        require(stars == 4 and singles == 1 and star_n == 7 and single_n == 1, 'grouping miscounted')
        require(Jv == V['cand_J'], 'per-site sum differs from 29|tau|')
        return Jv
    check('per_site_sum_recomputed',
          validate_J(stars_per_site, star_norm, singles_per_site, single_norm) == 29
          and rejected(lambda: validate_J(4, 7, 0, 1), 'selected_groups_dropped_28')
          and rejected(lambda: validate_J(1, 7, 1, 1), 'outgoing_star_only_8')
          and rejected(lambda: validate_J(4, 8, 1, 1), 'selected_in_stars_and_singles_33')
          and rejected(lambda: validate_J(4, 8, 0, 1), 'selected_merged_into_stars_32'),
          J_prime=s(J_per_tau))

    # reset_budget_recomputed
    def validate_reset(stars, star_n, singles, single_n, gap):
        rb = 2 * (stars * star_n + singles * single_n)
        require(stars == 7 and singles == 2 and rb == V['cand_reset'], 'reset budget miscounted')
        require(gap == 6 and rb / gap == V['cand_eps_R'], 'epsilon_R needs the Haar gap six')
        return rb
    check('reset_budget_recomputed',
          validate_reset(tot['stars'], star_norm, tot['singles'], single_norm, onsite_gap) == 102
          and rejected(lambda: validate_reset(7, 7, 0, 1, 6), 'selected_groups_missing_98')
          and rejected(lambda: validate_reset(7, 7, 7, 1, 6), 'single_groups_at_all_seven_anchors_112')
          and rejected(lambda: validate_reset(2, 7, 2, 1, 6), 'orthant_two_stars')
          and rejected(lambda: validate_reset(7, 7, 2, 1, 1), 'gap_one_read_as_17'),
          reset=s(reset), eps_R=s(eps_R))

    # selected_incidence_count
    def validate_incidence(singles, sel_faces, B):
        require(singles == 2 and sel_faces == 6 and B == Q(51, 8), 'selected incidence miscounted')
        return True
    check('selected_incidence_count',
          validate_incidence(tot['singles'], tot['selected_faces'], tot['B_over_abs_tau'])
          and rejected(lambda: validate_incidence(0, 0, Q(49, 8)), 'selected_groups_forgotten')
          and rejected(lambda: validate_incidence(6, 6, Q(55, 8)), 'faces_counted_as_groups')
          and rejected(lambda: validate_incidence(7, 21, Q(56, 8)), 'singles_at_star_anchors'),
          singles=tot['singles'], selected_faces=tot['selected_faces'])

    # first_order_faces_uniform
    def validate_face_count(fn):
        got = fn(CLASS_ROWS)
        require(got == 52, 'uniform per-factor count must be 52 (49 omitted + 3 selected)')
        mutated = tuple(r1 for r1 in CLASS_ROWS if r1['role'] != 'selected')
        require(fn(mutated) != got, 'count insensitive to the selected classes: hard-coded or copied')
        return got
    check('first_order_faces_uniform',
          validate_face_count(lambda rows: derive_counts(rows)['faces_per_factor']) == 52
          and rejected(lambda: validate_face_count(lambda rows: derive_counts(tuple(r1 for r1 in rows if r1['role'] == 'omitted'))['faces_per_factor']),
                       'omitted_only_49')
          and rejected(lambda: validate_face_count(lambda rows: V['bound_per_factor']), 'labelled_bound_96_as_exact')
          and rejected(lambda: validate_face_count(lambda rows: derive_counts(rows)['faces_per_factor'] + 3 * 3), 'selected_at_all_four_anchors_61'),
          derived=52, labelled_bounds=[V['bound_per_factor'], V['bound_R']])

    # uniform_label_strong_coupling
    FORBIDDEN = ('weak coupling', 'weak-coupling', 'weak bare coupling', 'continuum')

    def validate_label(lb, verdict):
        for text in list(lb.values()) + [verdict]:
            low = text.lower()
            require(not any(fb in low for fb in FORBIDDEN), 'forbidden regime label: ' + text)
        require('uniform Kogut-Susskind SU(2)' in lb['model_label'] and 'fixed spacing' in lb['model_label']
                and 'strong bare coupling' in lb['model_label'], 'label must name the uniform fixed-spacing strong-coupling model')
        return True
    verdict_line = ('forward half: accepted_within_scope proposed for the uniform Kogut-Susskind SU(2) model at fixed spacing, strong bare coupling, route B; '
                    'the gate needs the reverse route and skeptical review')

    def lab(key, val):
        m2 = dict(label)
        m2[key] = val
        return lambda: validate_label(m2, verdict_line)
    check('uniform_label_strong_coupling',
          validate_label(label, verdict_line)
          and rejected(lab('model_label', 'uniform Kogut-Susskind SU(2) at fixed spacing, weak coupling'), 'weak_coupling_label')
          and rejected(lab('regime', 'approach to the continuum at g^4=9.6x10^9'), 'continuum_label')
          and rejected(lab('model_label', 'uniform Kogut-Susskind SU(2), strong bare coupling'), 'fixed_spacing_missing')
          and rejected(lambda: validate_label(label, verdict_line + ' toward the continuum limit'), 'verdict_continuum'),
          scanned_fields=['label.*', 'proposed_forward_verdict'], forbidden=list(FORBIDDEN))

    # am2_gap_reuse_justified
    def validate_reuse(J_cap_value, J0_value, support, gap, order):
        require(support <= 4, 'AM2 majorant (p=4) needs supports of at most four sites')
        require(gap >= 1, 'AM2 needs h_x>=Q_x')
        require(order <= 8, 'nested termination beyond eight')
        require(J_cap_value <= J0_value and J0_value * GR < R and 2 * J0_value * GpR < 1, 'contraction not verified for the route-B interaction')
        return True
    check('am2_gap_reuse_justified',
          validate_reuse(Jcap, J0p, max_support, onsite_gap, termination_order)
          and rejected(lambda: validate_reuse(Jcap, J0_old, max_support, onsite_gap, termination_order), 'old_J0_7_over_25000000')
          and rejected(lambda: validate_reuse(Jcap, J0p, 5, onsite_gap, 10), 'support_five_grouping')
          and rejected(lambda: validate_reuse(Jcap, J0p, max_support, Q(0), termination_order), 'degenerate_reference_gap_zero')
          and rejected(lambda: validate_reuse(Jcap, Q(1, 1000), max_support, onsite_gap, termination_order), 'J0_too_large_contraction_fails'),
          J_cap=s(Jcap), J0_old=s(J0_old), J0_prime=s(J0p), old_J0_fails=Jcap > J0_old)

    # j0_resolution_declared
    j0_packet = {'resolution': 'R1', 'J0_prime': s(J0p), 'self_map': s(selfmap), 'exclusion': s(exclusion), 'tau_cap': s(tau_cap),
                 'contract_sha256': contract_digest}

    def validate_j0(pk):
        require(pk.get('resolution') == 'R1', 'J_0 resolution missing or not R1')
        require(rat(pk['tau_cap']) == tau_cap, 'R2 cap is a changed coupling')
        J0v = rat(pk['J0_prime'])
        require(J0v >= J_per_tau * tau_cap, 'J_0 below the route-B per-site sum at the cap')
        require(rat(pk['self_map']) == J0v * GR == V['selfmap_rational'] and rat(pk['exclusion']) == 2 * J0v * GpR == V['exclusion_rational'],
                'contraction rationals differ from the contract')
        require(pk['contract_sha256'] == CONTRACT_SHA256, 'contract source not bound')
        return True

    def j0m(**kw):
        m2 = dict(j0_packet)
        m2.update(kw)
        return lambda: validate_j0(m2)
    check('j0_resolution_declared',
          validate_j0(j0_packet) and V['R2_cap'] == J0_old / 29
          and rejected(j0m(J0_prime=s(J0_old), self_map=s(J0_old * GR), exclusion=s(2 * J0_old * GpR)), 'old_J0_at_cap')
          and rejected(j0m(resolution=None), 'resolution_missing')
          and rejected(j0m(resolution='R2', tau_cap=s(V['R2_cap'])), 'R2_changed_coupling_under_cap_label'),
          j0_packet=j0_packet, R2_cap=s(V['R2_cap']), semantics=V['new_semantics']['j0_resolution_declared'])

    # uniform_sign_convention
    def validate_signs(cmap):
        vals = set(cmap.values())
        require(vals == {UNIFORM_COEFFICIENT_OVER_TAU} and len(cmap) == 24, 'mixed face-coefficient convention')
        return True

    def cmut(which, val):
        m2 = dict(coeff)
        for k in classes:
            if k[4] == which:
                m2[class_label(k)] = val
        return lambda: validate_signs(m2)
    check('uniform_sign_convention',
          validate_signs(coeff) and V['psi_den'] == 3
          and rejected(cmut('selected', Q(1, 3)), 'selected_opposite_sign')
          and rejected(cmut('selected', Q(-1, 24)), 'selected_alpha_units_tau_over_24')
          and rejected(cmut('selected', Q(0)), 'selected_zero_patterned'),
          coefficient_all_24_classes='-(tau/3) W_f in delta=alpha/8 units', semantics=V['new_semantics']['uniform_sign_convention'])

    # tier_mixing_rejected
    def mix_crude_t():
        assemble('ii', [('t1', 'ii', Dp['ii']['t1']), ('am2_remainder', 'ii', Dp['ii']['remainder']), ('self_consistent_t', 'i', Dp['i']['t'])])

    def refined_without_remainder():
        assemble('ii', [('t1', 'ii', Dp['ii']['t1']), ('self_consistent_t', 'ii', Dp['ii']['t1'])])

    def remainder_zero():
        assemble('ii', [('t1', 'ii', Dp['ii']['t1']), ('am2_remainder', 'ii', Q(0)), ('self_consistent_t', 'ii', Dp['ii']['t1'])])
    check('tier_mixing_rejected',
          rejected(mix_crude_t, 'exact_c1_with_crude_t') and rejected(refined_without_remainder, 't_equals_t1')
          and rejected(remainder_zero, 'remainder_zero'))

    # reverse_premise_isolation (positive check of the declaration plus mutations)
    forward_list = ['AGENTS.md', CONTRACT_REL] + V['shared_premises'] + V['forward_additional']
    reverse_list = ['AGENTS.md', CONTRACT_REL] + V['shared_premises']
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    bad = ('research/round32/skeptic/triage.md', 'research/round32/skeptic/loop2-response.md', '/loop2-response.md',
           'research/round32/forward/ax1', 'research/round32/advisor/deliberation-')

    def validate_isolation(decl, note, lst):
        require(decl is True, 'contract does not declare reverse premise isolation')
        require('its inputs equal AGENTS.md, this contract and shared_premises' in note, 'premise note does not state the reverse inventory')
        for item in lst:
            require(not any(b1 in item for b1 in bad), 'reverse premise isolation violated by ' + item)
        return True
    check('reverse_premise_isolation',
          sorted(inventory) == sorted(set(forward_list)) and validate_isolation(V['reverse_isolation'], V['premise_note'], reverse_list)
          and rejected(lambda: validate_isolation(False, V['premise_note'], reverse_list), 'declaration_false')
          and rejected(lambda: validate_isolation(True, V['premise_note'], reverse_list + ['research/round32/skeptic/triage.md']), 'reverse_reads_triage')
          and rejected(lambda: validate_isolation(True, V['premise_note'], reverse_list + ['research/round32/forward/ax1/report.md']), 'reverse_reads_forward_ax1'),
          forward_inventory_files=len(inventory), reverse_premise_count=len(reverse_list),
          forward_additional_disclosed=V['forward_additional'],
          finding='the shared premises (selection-ax1.md) and the contract itself state route B and J_0\'; the reverse cannot find them independently (item 8)')

    # route_b_no_double_count
    def validate_grouping(assign):
        seen = {}
        for g, fl in assign.items():
            for f in fl:
                require(face_key(f) not in seen, 'face charged twice: ' + class_label(f[1]))
                seen[face_key(f)] = g
        Jv = Q(0)
        for g, fl in assign.items():
            if ORIGIN in group_support(g):
                Jv += sum((abs(coeff[class_label(f[1])]) for f in fl), Q(0))
        require(Jv == 29, 'per-site sum differs from 29|tau|')
        return True
    local_groups = [('star', sub(ORIGIN, d)) for d in S_STAR] + [('single', ORIGIN)]
    assign_ok = {g: group_faces_list(g) for g in local_groups}
    assign_dbl = {g: (group_faces_list(g) + ([(g[1], k) for k in selected] if g[0] == 'star' else [])) for g in local_groups}
    check('route_b_no_double_count',
          validate_grouping(assign_ok) and rejected(lambda: validate_grouping(assign_dbl), 'selected_in_star_and_single')
          and rejected(lambda: validate_grouping({g: fl for g, fl in assign_ok.items() if g[0] == 'star'}), 'selected_faces_dropped'),
          groups_at_origin=[[g[0], list(g[1])] for g in local_groups], semantics=V['new_semantics']['route_b_no_double_count'])

    # incidence_table_itemized
    def validate_table(pk):
        tb = pk.get('incidence_table')
        require(isinstance(tb, list) and tb, 'incidence totals asserted without the itemized table')
        t2 = totals_from_table(tb)
        require(t2['stars'] == pk['incidence_totals']['stars'] and t2['singles'] == pk['incidence_totals']['single_factor_groups']
                and t2['selected_faces'] == pk['incidence_totals']['selected_faces_inside_R']
                and s(t2['B_over_abs_tau']) == pk['incidence_totals']['B_N_over_abs_tau'], 'totals differ from the itemized table')
        return True
    inc_packet = {'incidence_table': table, 'incidence_totals': {'stars': 7, 'single_factor_groups': 2, 'selected_faces_inside_R': 6,
                                                                 'B_N_over_abs_tau': s(tot['B_over_abs_tau'])}}
    no_table = {'incidence_totals': inc_packet['incidence_totals']}
    short_table = {'incidence_table': table[:-1], 'incidence_totals': inc_packet['incidence_totals']}
    dup_table = {'incidence_table': table + [table[-1]], 'incidence_totals': inc_packet['incidence_totals']}
    check('incidence_table_itemized',
          validate_table(inc_packet) and rejected(lambda: validate_table(no_table), 'totals_without_table')
          and rejected(lambda: validate_table(short_table), 'single_group_missing_from_table')
          and rejected(lambda: validate_table(dup_table), 'group_listed_twice'),
          groups_tabulated=len(table), semantics=V['new_semantics']['incidence_table_itemized'])

    # ======================= the 12 universal controls =======================
    cover_links = []
    for b in COVER_R:
        for r in range(4):
            for q in range(2):
                tp = (4 * b[0] + r, 2 * b[1] + q, b[2])
                for d in range(3):
                    cover_links.append((tp, d))
    ends = {}
    for (tp, d) in cover_links:
        ends.setdefault(owner(tp), set()).update({tp, add(tp, E_UNIT[d])})
    endpoints = set().union(*ends.values())
    shared_ends = ends[ORIGIN] & ends[EZ]
    W_links = face_links(ORIGIN, 0, 2)
    W_owners = sorted(owner(l[0]) for l in W_links)
    sel_in_cover = all(face_link_set(f) <= set(cover_links) for f in sel_meet)
    check('full_original_wilson_cover',
          len(set(cover_links)) == 48 and len(endpoints) == 36 and len(ends[ORIGIN]) == 22 and len(ends[EZ]) == 22 and len(shared_ends) == 8
          and set(W_owners) == set(COVER_R) and sel_in_cover
          and rejected(lambda: require(len(set(W_links)) == 48, 'four drawn links are not the cover'), 'four_drawn_links'),
          links=48, endpoints=36, shared_endpoints=8, wilson_link_owners=[list(o) for o in W_owners],
          selected_faces_inside_cover=len(sel_meet))
    outgoing_only = [b for b in incident if b in COVER_R]

    def validate_group_count(n):
        require(n == 9, 'groups meeting R must be seven stars plus two single-factor groups')
        return True
    check('missing_incoming_stars',
          len(incident) == 7 and tot['stars'] + tot['singles'] == 9
          and rejected(lambda: require(len(outgoing_only) == 7, 'orthant two-anchor count'), 'orthant_two_anchors')
          and rejected(lambda: require(1 * star_norm + single_norm == J_per_tau, 'outgoing-only J=8|tau|'), 'outgoing_only_J_8')
          and validate_group_count(tot['stars'] + tot['singles'])
          and rejected(lambda: validate_group_count(tot['stars']), 'group_count_without_selected'),
          incident_anchors=[list(b) for b in incident], orthant_count=len(outgoing_only), groups_meeting_R=9)

    alpha_f, hbar_f, tE = Q(5), Q(7), Q(3, 2)
    s_clock = alpha_f * tE / hbar_f
    u_clock = (alpha_f / 8) * tE / hbar_f
    tau_sym = Q(1)
    v_norm = -tau_sym / 3
    v_alpha = -tau_sym / 24
    right1 = v_norm / 24
    right2 = v_alpha / 3
    k_alpha = tot['k_over_abs_tau']
    k_norm = 8 * k_alpha
    theta = Q(2, 3)
    check('wrong_delta_alpha_hbar_clock',
          right1 == right2 == -tau_sym / 72 and 3 * s_clock == 24 * u_clock and k_alpha * theta == k_norm * (theta / 8)
          and rejected(lambda: require(v_alpha / 24 == right1, 'alpha-unit V with delta-unit energy'), 'mixed_units_576')
          and rejected(lambda: require(v_norm / 3 == right1, 'delta-unit V with alpha-unit energy'), 'mixed_units_9')
          and rejected(lambda: require(24 * s_clock == 3 * s_clock, 'exponent 24 with s'), 'eightfold_clock')
          and rejected(lambda: require(k_alpha * (theta / 8) == k_alpha * theta, "k'=51|tau|/4 used with the normalized clock u"), 'k_prime_mixed_clock'),
          first_order_coefficient=s(right1), k_prime_alpha_units=s(k_alpha), nonunit_fixture={'alpha': '5', 'hbar': '7', 't_E': '3/2'})
    m_, d_ = Q(1, 4), Q(1, 100)
    check('vector_versus_scalar_centering',
          d_ ** 2 == Q(1, 10000) and -2 * m_ * d_ - d_ ** 2 == Q(-51, 10000)
          and rejected(lambda: require(d_ ** 2 == -2 * m_ * d_ - d_ ** 2, 'scalar subtraction as vector centering'), 'scalar_as_vector'),
          vector_residue=s(d_ ** 2), scalar_residue=s(-2 * m_ * d_ - d_ ** 2), uncentered_residue=s(m_ ** 2))
    check('first_order_mean_charged',
          tau_cap / 144 <= Dp['ii']['D'] and Dp['ii']['D'] ** 2 > 0
          and rejected(lambda: require(first == 0, 'zero first-order mean assumed in the uniform model'), 'zero_mean_assumed')
          and rejected(lambda: require(Q(0) >= Dp['ii']['D'] ** 2, 'm^2 charge dropped'), 'm2_dropped'),
          m2_upper_tier_ii=s(Dp['ii']['D'] ** 2), first_order_mean=s(tau_cap / 144),
          note='|omega(W)|<=D\' and |omega(W^2)-1/4|<=D\'/2 are the consequences; the first-order mean tau/144 is nonzero and compatible')

    packet_model = {'model_id': V['model_id'], 'tau': s(tau_cap), 'triple_alpha_units': V['prereg_triple'],
                    'reference_route': V['reference_route'], 'state_provenance': V['state_provenance']}

    def validate_model(pk):
        require(pk['model_id'] == 'AQ_uniform_routeB', 'model id')
        require(rat(pk['tau']) == tau_cap, 'coupling changed')
        require(pk['triple_alpha_units'] == ['tau/24', 'tau/24', 'tau/24'], 'selected triple changed')
        require(pk['reference_route'] == 'haar', 'reference route changed')
        require(pk['state_provenance'].startswith('AQ1_centered_whole_star_subsequence'), 'state provenance changed')
        return True
    muts = []
    for key, val in (('tau', '1/100000000000000'), ('tau', s(V['R2_cap'])), ('triple_alpha_units', ['0', '0', '0']),
                     ('reference_route', 'selected_strip'), ('model_id', 'FG(two_plaquette,1/2,24,I1.5,physical)'),
                     ('state_provenance', 'finite_volume_N=3')):
        mutated = dict(packet_model)
        mutated[key] = val
        muts.append(rejected(lambda m=mutated: validate_model(m), 'relabel_' + key + '_' + str(len(muts))))
    check('changed_model_relabelled', validate_model(packet_model) and len(muts) == 6, packet_model=packet_model, rejected=muts)

    def claim_tier_i_pass(tau_used):
        x = tier_i(tau_used, J_per_tau, GR, R)
        require(x['tau'] == tau_cap, 'coupling retuned under the cap label')
        require(x['D'] <= target, 'tier (i) fails the target')
        return True
    check('insufficient_verdict_retained',
          Dp['i']['D'] > target and Dm['i']['D'] > target and sqrtD_gap_one_sq > Q(1, 500) ** 2
          and rejected(lambda: claim_tier_i_pass(tau_cap / 1000), 'retune_tier_i_to_smaller_tau')
          and rejected(lambda: claim_tier_i_pass(tau_cap), 'tier_i_reported_pass_at_cap'),
          retained_failures=['tier (i) D_i fails 4/10^7 and 10^-6', 'gap-one reset route fails AQ2 1/500', 'R2 cap not selected'])

    forbidden_mods = ('mp' + 'math', 'num' + 'py', 'fl' + 'int', 'sym' + 'py', 'sci' + 'py')
    own = (BASE / 'check.py').read_text()
    imports = [ln for ln in own.splitlines() if ln.startswith('import ') or ln.startswith('from ')]
    check('exact_arithmetic_admission',
          not any(any(fb in ln for fb in forbidden_mods) for ln in imports)
          and rejected(lambda: rat(1e-08), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('NaN'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator'),
          imports=imports, decimals='previews only, truncated from exact rationals')

    B_linear = tot['B_over_abs_tau']
    B_rss_sq = (7 * star_norm ** 2 + 2 * single_norm ** 2) / 64
    check('root_n_misuse',
          B_linear ** 2 > B_rss_sq and (Q(3, 10) + Q(2, 10)) ** 2 > Q(9, 100) + Q(4, 100)
          and rejected(lambda: require(B_rss_sq == B_linear ** 2, "RSS of the nine group norms used for ||B_N||"), 'rss_group_norms')
          and rejected(lambda: require(B_linear / sqrt_down(9) == B_linear, 'division by sqrt(9 groups)'), 'divide_sqrt_N')
          and rejected(lambda: require(B_linear / 64 == B_linear, 'division by 64'), 'divide_64'),
          B_linear=s(B_linear), B_rss_squared=s(B_rss_sq))

    claim_flags = {'continuum_claim': False, 'uniform_wilson_claim': True, 'weak_coupling_claim': False,
                   'resolved_interaction_shift': False, 'scientific_priority_verified': False, 'euclidean_node_certified': False}
    REQUIRED_FLAGS = {'continuum_claim': False, 'uniform_wilson_claim': True, 'weak_coupling_claim': False,
                      'resolved_interaction_shift': False, 'scientific_priority_verified': False, 'euclidean_node_certified': False}

    def validate_flags(fl, lb):
        for k1, v1 in REQUIRED_FLAGS.items():
            require(fl.get(k1) is v1, 'claim flag ' + k1 + ' must be ' + str(v1))
        require('fixed spacing' in lb['model_label'], 'uniform_wilson_claim only for the fixed-spacing model as labelled')
        return True

    def flag_mut(**kw):
        m2 = dict(claim_flags)
        m2.update(kw)
        return lambda: validate_flags(m2, label)
    check('no_priority_or_continuum_claim',
          validate_flags(claim_flags, label)
          and rejected(flag_mut(continuum_claim=True), 'continuum_true') and rejected(flag_mut(weak_coupling_claim=True), 'weak_coupling_true')
          and rejected(flag_mut(scientific_priority_verified=True), 'priority_true') and rejected(flag_mut(resolved_interaction_shift=True), 'shift_true')
          and rejected(flag_mut(euclidean_node_certified=True), 'euclidean_node_true')
          and rejected(lambda: validate_flags(claim_flags, {'model_label': 'uniform Kogut-Susskind SU(2)'}), 'uniform_claim_without_fixed_spacing'),
          historical_or_occult_numeric_premise=False)

    # ======================= packet, error ledger, tampering =======================
    error_terms = {
        'am2_remainder': {'tier_ii_plus': s(Dp['ii']['remainder']), 'form': "352 J' T'",
                          'tier_i': 'not_applicable: tier (i) bounds the full c by J\'G(R) directly'},
        'two_creation': {'tier_i_plus': s(Dp['i']['t'] ** 2), 'tier_ii_plus': s(Dp['ii']['t'] ** 2),
                         'note': 'includes the single-site pair c_{0} x c_{e_z}, first-order nonzero in route B'},
        'straddling': {'status': 'counted inside the 2t term of eps (all supports meeting R)',
                       'first_order_straddling_faces': counts['faces_meeting_R'] - counts['faces_inside_R']},
        'density': {'tier_i_plus': s(2 * Dp['i']['eps'] ** 2 / (1 + Dp['i']['eps'] ** 2)),
                    'tier_ii_plus': s(2 * Dp['ii']['eps'] ** 2 / (1 + Dp['ii']['eps'] ** 2))},
        'onsite_cutoff_vector': 'not_applicable as a numeric cost: exact limit in each fixed box (AV1 section 7 verbatim; selected face vectors lie at energy 24, kept for L>=24)',
        'arithmetic': 'not_applicable as a numeric cost: exact Fractions; directed enclosures exp(1/8)<8/7, e^{8t}<=1/(1-8t), sqrt upper brackets, Machin pi',
    }
    require(sorted(error_terms) == sorted(V['error_terms']), 'error terms differ from preregistration')
    check('error_ledger_itemized', sorted(error_terms) == sorted(V['error_terms']) and len(error_terms) == 6,
          terms=sorted(error_terms))

    headline = {
        'J_prime_over_abs_tau': s(J_per_tau), 'J0_prime': s(J0p), 'self_map_rational': s(selfmap), 'exclusion_rational': s(exclusion),
        'faces_per_factor_uniform': counts['faces_per_factor'], 'faces_meeting_R_uniform': counts['faces_meeting_R'],
        'stars_meeting_R': tot['stars'], 'single_factor_groups_meeting_R': tot['singles'], 'selected_faces_inside_R': tot['selected_faces'],
        'B_N_over_abs_tau': s(tot['B_over_abs_tau']), 'k_prime_over_abs_tau': s(tot['k_over_abs_tau']),
        'reset_over_abs_tau': s(reset), 'eps_R_over_abs_tau': s(eps_R),
        'D_i_plus': s(Dp['i']['D']), 'D_i_minus': s(Dm['i']['D']), 'D_i_preview': dec(Dp['i']['D']),
        'D_ii_plus': s(Dp['ii']['D']), 'D_ii_minus': s(Dm['ii']['D']), 'D_ii_preview': dec(Dp['ii']['D']),
        'D_ii_bound96_preview': dec(Dp['ii_bound96']['D']), 'D_ii_grouped_preview': dec(Dp['ii_grouped']['D']),
        'omega_W_first_order': {'+': s(tau_cap / 144), '-': s(-tau_cap / 144)},
    }
    packet = {
        'loop': 'AX1', 'direction': 'forward', 'human_author': 'Hruday N M (BUNZEEY)',
        'contribution_alias': 'HNM-AX1-F forward route-B re-derivation for the uniform Kogut-Susskind SU(2) Hamiltonian at fixed spacing',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha,
        'label': label, 'model': packet_model, 'tau_values': {sg: s(tv) for sg, tv in taus.items()},
        'dictionary': {'alpha': 'g^2/(2a)', 'lambda': '2/(g^2 a)', 'tau': '96/g^4', 'g4_at_cap': s(g4_cap),
                       'selected_over_alpha_at_cap': s(sel_alpha), 'negative_tau': 'U_E mirror, no real g'},
        'j0_resolution': j0_packet,
        'constants': {'R': s(R), 'G_R_upper': s(GR), 'G_prime_R_upper': s(GpR), 'J_prime_over_abs_tau': s(J_per_tau),
                      'star_norm_over_abs_tau': s(star_norm), 'single_group_norm_over_abs_tau': s(single_norm),
                      'onsite_gap': s(onsite_gap), 'face_energy_normalized': s(energy), 'norm_WfOmega0': '1/2',
                      'first_order_coefficient_per_face': '-tau/72', 't1_over_abs_tau': s(t1_per_tau),
                      't1_grouped_upper_over_abs_tau': s(t1g_per_tau), 't1_labelled_bound_96_over_abs_tau': s(t1_96_per_tau),
                      'reset_over_abs_tau': s(reset), 'eps_R_over_abs_tau': s(eps_R), 'C_F_per_site_over_abs_tau': s(C_F_per_site),
                      'Phi_F_over_abs_tau': s(Phi_F), 'B_N_over_abs_tau': s(tot['B_over_abs_tau']), 'k_prime_over_abs_tau': s(tot['k_over_abs_tau'])},
        'face_enumeration': {'faces_per_factor': counts['faces_per_factor'], 'owner_sets_per_factor': counts['owner_sets_per_factor'],
                             'multiplicities': counts['multiplicities'], 'faces_meeting_R': counts['faces_meeting_R'],
                             'faces_inside_R': counts['faces_inside_R'], 'faces_containing_R': counts['faces_containing_R'],
                             'owner_sets_meeting_R': counts['owner_sets_meeting_R'],
                             'labelled_bounds': {'per_factor': V['bound_per_factor'], 'R': V['bound_R']},
                             'derived_from': 'explicit 24-class anchored table by translation covariance; fine-lattice brute force'},
        'incidence_table': table,
        'incidence_totals': inc_packet['incidence_totals'],
        'reinstantiation_checklist': checklist,
        'aw1_transfer': transfer,
        'tiers': {sg: {k1: tier_record(v1) for k1, v1 in tiers[sg].items()} for sg in taus},
        'scaling_tau_over_100': {k1: tier_record(v1) for k1, v1 in scal.items()},
        'headline': headline,
        'targets': {'target_D_ii': s(target), 'tier_ii_meets_target': tier_ii_target_met, 'tier_i_meets_target': False,
                    'tier_ii_meets_1e-6': True, 'tier_i_meets_1e-6': False},
        'consequences': {sg: {'abs_omega_W_upper_tier_ii': s(tiers[sg]['ii']['D']), 'omega_W2_minus_quarter_upper_tier_ii': s(tiers[sg]['ii']['D'] / 2),
                              'm2_upper_tier_ii': s(tiers[sg]['ii']['D'] ** 2)} for sg in taus},
        'error_terms_itemized': error_terms,
        'tier_ii_target_met': tier_ii_target_met,
        'uniqueness_claimed': False, 'whole_sequence_convergence_claimed': False, 'rate_in_N_claimed': False,
        'k2_uniform_claimed': False, 'wilson_mean_sign_certified': False,
        'proposed_forward_verdict': verdict_line,
        'exclusions': {'contract': V['claim_exclusions'], 'preregistration': V['prereg_exclusions']},
        'routes_executed': ['forward route B: product ordering with the enlarged creation set and explicit reduced density'],
        'routes_not_executed': ['reverse producer route (outside this producer)'],
    }
    packet.update(claim_flags)

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
        validate_flags({k1: pk[k1] for k1 in REQUIRED_FLAGS}, pk['label'])
        validate_label(pk['label'], pk['proposed_forward_verdict'])
        require(sorted(inv) == sorted(set(forward_list)), 'premise snapshot inventory incomplete')
        recomputed = tier_ii(tau_cap, J_per_tau, t1_per_tau, GR, GpR, R, 'recheck')['D']
        require(rat(pk['headline']['D_ii_plus']) == recomputed, 'headline D_ii differs from recomputation')
        require(pk['tier_ii_target_met'] is (recomputed <= target), 'target Boolean differs from recomputation')
        validate_j0(pk['j0_resolution'])
        validate_table(pk)
        return True

    base_packet = dict(packet)
    base_packet['checks'] = [dict(ch) for ch in CHECKS]
    base_packet['packet_sha256'] = packet_hash(base_packet)

    def tamper(fn):
        def run():
            pk = json.loads(json.dumps(base_packet))
            inv = dict(inventory)
            fn(pk, inv)
            pk['packet_sha256'] = packet_hash(pk)
            return validate_packet(pk, inv)
        return run

    def t_control(pk, inv):
        for ch in pk['checks']:
            if ch['id'] == 'route_b_no_double_count':
                ch['passed'] = False

    def t_snapshot(pk, inv):
        inv.pop('research/round32/advisor/selection-ax1.md')

    def t_value(pk, inv):
        pk['headline']['D_ii_plus'] = s(rat(pk['headline']['D_ii_plus']) / 2)

    def t_j0(pk, inv):
        pk['j0_resolution']['self_map'] = s(rat(pk['j0_resolution']['self_map']) / 2)

    def t_table(pk, inv):
        pk['incidence_table'] = pk['incidence_table'][:7]

    def t_flag(pk, inv):
        pk['continuum_claim'] = True
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(tamper(t_control), 'control_boolean_flipped_hash_rebound')
          and rejected(tamper(t_snapshot), 'snapshot_removed_hash_rebound')
          and rejected(tamper(t_value), 'D_ii_halved_hash_rebound')
          and rejected(tamper(t_j0), 'j0_self_map_halved_hash_rebound')
          and rejected(tamper(t_table), 'single_groups_removed_hash_rebound')
          and rejected(tamper(t_flag), 'continuum_flag_hash_rebound'))

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in V['controls'] if cid not in ids]
    require(not missing, 'contract controls without a check: ' + ','.join(missing))
    positive_only = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch.get('rejected_mutations')]
    require(not positive_only, 'contract controls without a damaging mutation: ' + ','.join(positive_only))
    require(not PENDING, 'rejected mutations not attached to a check')
    packet['checks'] = CHECKS
    packet['controls_with_damaging_mutations'] = sum(1 for ch in CHECKS if ch['id'] in V['controls'])
    packet['rejected_mutation_total'] = sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS)
    packet['contract_controls_covered'] = sorted(V['controls'])
    packet['check_count'] = len(CHECKS)
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
    ap = argparse.ArgumentParser(description='AX1 forward exact checker')
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
    manifest = {'loop': 'AX1', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AX1', 'direction': 'forward', 'checks': len(result['checks']),
                      'D_i_preview': result['headline']['D_i_preview'], 'D_ii_preview': result['headline']['D_ii_preview'],
                      'tier_ii_target_met': result['tier_ii_target_met']}, sort_keys=True))


if __name__ == '__main__':
    main()
