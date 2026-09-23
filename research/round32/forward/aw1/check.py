#!/usr/bin/env python3
"""AW1 forward producer: exact checks for the Hruday parity theorem, the
link-flip antisymmetry lemma, the first-order Wilson mean tau/144 and the
itemized second-order remainder K_2 (zero-selected AQ subfamily).

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production.

Standard library only (fractions, hashlib, json, argparse, re, itertools,
math.isqrt/comb/factorial).  Every admission Boolean is decided in exact
Fraction arithmetic; decimal strings are truncated previews.  Conditions
raise AdmissionError explicitly (never `assert`), so every check stays
active under `python -O`.

Inherited tooling named, not imported, and re-derived here:
  research/round32/experts/historical/assistant-1/haar_parity_exact.py
  research/round32/experts/modern/assistant-1/flip_parity_k2.py

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import hashlib
import itertools
import json
import re
from fractions import Fraction as Q
from math import comb, factorial, isqrt
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
CONTRACT_REL = 'research/round32/contracts/aw1.json'
CONTRACT_SHA256 = 'c24bf7eb6a1c24034427c810a9c26c4c86d1f9c1d31b0fe36ea4cf2a796814ef'
AV1_CONTRACT_REL = 'research/round32/contracts/av1.json'
AV1_GATE_REL = 'research/round32/advisor/av1-gate.json'
SELECTION_REL = 'research/round32/advisor/selection-aw1.md'
I1_REL = 'research/round21/forward/i1/report.md'
INHERITED_TOOLING = ['research/round32/experts/historical/assistant-1/haar_parity_exact.py',
                     'research/round32/experts/modern/assistant-1/flip_parity_k2.py']


class AdmissionError(Exception):
    """An admission condition failed or a damaging mutation was accepted."""


def require(condition, message):
    if not condition:
        raise AdmissionError(message)


CHECKS = []
PENDING_MUTATIONS = []


def check(identity, condition, **details):
    require(condition, 'failed check ' + identity)
    require(all(c['id'] != identity for c in CHECKS), 'duplicate check id ' + identity)
    entry = {'id': identity, 'passed': True, 'mutations_rejected': list(PENDING_MUTATIONS)}
    PENDING_MUTATIONS.clear()
    entry.update(details)
    CHECKS.append(entry)


def rejected(mutation, label):
    """Run a damaging mutation; it must raise AdmissionError (recorded on the next check)."""
    try:
        mutation()
    except AdmissionError:
        PENDING_MUTATIONS.append(label)
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
    """Directed rational upper bound of sqrt(n), n>=0 rational."""
    n = Q(n)
    k = isqrt(n.numerator * scale * scale // n.denominator)
    while Q(k, scale) ** 2 < n:
        k += 1
    up = Q(k, scale)
    require(up * up >= n and (up - Q(1, scale)) ** 2 < n, 'sqrt upper bracket')
    return up


def sqrt_lo(n, scale=10 ** 12):
    """Directed rational lower bound of sqrt(n), n>=0 rational."""
    n = Q(n)
    k = isqrt(n.numerator * scale * scale // n.denominator)
    while Q(k, scale) ** 2 > n:
        k -= 1
    lo = Q(k, scale)
    require(lo * lo <= n and (lo + Q(1, scale)) ** 2 > n, 'sqrt lower bracket')
    return lo


def exact_sqrt(q):
    q = Q(q)
    a, b = isqrt(q.numerator), isqrt(q.denominator)
    require(a * a == q.numerator and b * b == q.denominator, 'not a rational square')
    return Q(a, b)


def ceil_grid(q, grid=10 ** 40):
    """Outward (upward) rounding of a positive rational onto the 10^-40 grid."""
    q = Q(q)
    return Q(-((-q.numerator * grid) // q.denominator), grid)


# ---------------------------------------------------------------------------
# Contract and inherited premises: targets, references and candidates are read
# from the hash-checked snapshots, never typed into this file.
# ---------------------------------------------------------------------------
def read_input(rel):
    path = BASE / 'inputs' / rel
    require(path.is_file(), 'missing premise snapshot ' + rel)
    return path.read_bytes()


def load_contract():
    raw = read_input(CONTRACT_REL)
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen AW1 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'AW1' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return c, digest


def match(pattern, text, label):
    m = re.search(pattern, text)
    require(m is not None, 'premise text not parsed: ' + label)
    return m


def contract_values(c):
    p = c['parameters']
    pre = c['preregistration']
    req = c['required']
    v = {}
    v['tau_cap'] = rat(p['tau_cap'])
    require(list(p['signs']) == ['+', '-'], 'both signs required')
    v['triple'] = [rat(x) for x in p['selected_coefficients_over_alpha']]
    require(v['triple'] == [0, 0, 0], 'zero-selected triple required')
    m = match(r'^omega_tau\(W\)=\+tau/(\d+)\+r\(tau\) in alpha units under I1\.5 \(to be derived, not assumed\)$',
              p['first_order_candidate'], 'first-order candidate')
    v['candidate_den'] = int(m.group(1))
    clauses = re.findall(r'\{\(p,([xyz])\): p_([xyz]) even\}', p['flip_set'])
    require(len(clauses) == 3 and sorted(d for d, _ in clauses) == ['x', 'y', 'z'], 'flip set not parsed')
    axis = {'x': 0, 'y': 1, 'z': 2}
    v['flip_spec'] = {axis[d]: axis[q] for d, q in clauses}
    v['flip_set_text'] = p['flip_set']
    rule = p['aw2_coupling_rule']
    m = match(r'decade grid \{10\^-(\d+), 10\^-(\d+), \.\.\.\} with K_2\^\+ \* tau <= (\d+)/(\d+) '
              r'\(half the first-order coefficient\), K_2\^\+ the admitted exact-tier remainder constant; '
              r'frozen here, never chosen after K_2 is seen', rule, 'AW2 rule')
    v['grid_start'], grid_next = int(m.group(1)), int(m.group(2))
    require(grid_next == v['grid_start'] + 1, 'decade grid step')
    v['rule_bound'] = Q(int(m.group(3)), int(m.group(4)))
    v['rule_text'] = rule
    m = match(r'^1/\((\d+) K_2\^\+ tau\) >= (\d+) for accepted; else sign_certified_below_cap via the rule$',
              p['targets']['sign_margin_at_cap'], 'margin target')
    v['margin_den'], v['margin_min'] = int(m.group(1)), int(m.group(2))
    require(p['targets']['K_2_exact_tier_reported'] is True, 'exact-tier K_2 must be reported')
    t = pre['target']
    require(t['quantity'] == 'K_2^+ tau at the cap' and t['comparator'] == '<=', 'preregistered target quantity')
    v['target'] = rat(t['value'])
    require(v['target'] == v['rule_bound'], 'preregistered target differs from the AW2 rule bound')
    m = match(r'^(\d+) and (\d+)/(\d+)$', pre['observable']['reference_value_exact'], 'reference values')
    v['ref_W'], v['ref_W2'] = Q(int(m.group(1))), Q(int(m.group(2)), int(m.group(3)))
    m = match(r'E\[W\^3\]=(\d+), E\[W\^2 W_f\]=(\d+) for every omitted f including f=W, '
              r'E\[W\^2\]=(\d+)/(\d+), E\[W\^4\]=(\d+)/(\d+)', req[0], 'item 1 moments')
    v['ref_W3'], v['ref_W2Wf'] = Q(int(m.group(1))), Q(int(m.group(2)))
    require(Q(int(m.group(3)), int(m.group(4))) == v['ref_W2'], 'item 1 E[W^2] differs from the reference')
    v['ref_W4'] = Q(int(m.group(5)), int(m.group(6)))
    m = match(r'C\(s\)=e\^\{-(\d+)s\}/(\d+)\+O\(tau\^2\)', req[0], 'item 1 C(s)')
    v['free_exponent'], v['free_weight_den'] = int(m.group(1)), int(m.group(2))
    v['multiplet_energy'] = int(match(r'the energy-(\d+) multiplet vector W Omega_0', req[0], 'multiplet').group(1))
    v['faces_per_factor_cand'] = int(match(r'all (\d+) omitted faces of a factor', req[1], 'item 2 count').group(1))
    m = match(r'energy (\d+) in alpha units, (\d+) normalized; E\[W\^2\]=(\d+)/(\d+)\) to \+tau/(\d+) for tau>0',
              req[2], 'item 3')
    v['energy_alpha'], v['energy_norm'] = int(m.group(1)), int(m.group(2))
    require(Q(int(m.group(3)), int(m.group(4))) == v['ref_W2'] and int(m.group(5)) == v['candidate_den'], 'item 3 values')
    v['remainder_coefficient'] = int(match(r'\((\d+) J t or the sharper admitted form at the exact tier\)', req[3], 'item 4 AM2').group(1))
    m = match(r'\|\|W Omega_R\|\|=(\d+)/(\d+); a factor (\d+) is accepted only if labelled conservative', req[3], 'item 4 overlap')
    v['wilson_overlap_norm'], v['conservative_factor'] = Q(int(m.group(1)), int(m.group(2))), int(m.group(3))
    m = match(r'\((\d+) owner sets with multiplicities \{([0-9x,]+)\}, (\d+) faces meeting R, (\d+) touching both factors of R\)',
              req[3], 'item 4 enumeration')
    v['owner_sets_cand'] = int(m.group(1))
    mult = []
    for item in m.group(2).split(','):
        size, times = item.split('x')
        mult += [int(size)] * int(times)
    v['multiplicities_cand'] = sorted(mult)
    v['meet_R_cand'], v['both_R_cand'] = int(m.group(3)), int(m.group(4))
    m = match(r'one of the (\d+) omitted classes anchored at factor 0\) from the (\d+) other omitted faces', req[3], 'item 4 separation')
    v['classes_cand'], v['others_cand'] = int(m.group(1)), int(m.group(2))
    m = match(r'K_2\^\+ tau <= (\d+)/(\d+) at tau=10\^-(\d+) \(margin >= (\d+)\)', req[4], 'item 5')
    require(Q(int(m.group(1)), int(m.group(2))) == v['target'] and Q(1, 10 ** int(m.group(3))) == v['tau_cap']
            and int(m.group(4)) == v['margin_min'], 'item 5 differs from the rule and cap')
    v['phi_den'] = int(match(r'phi_b=-\(tau/(\d+)\) sum_f W_f', c['model'], 'model phi_b').group(1))
    require(Q(1, 10 ** int(match(r'\|tau\|<=10\^-(\d+)', c['model'], 'model cap').group(1))) == v['tau_cap'], 'model cap')
    v['controls'] = list(c['controls'])
    v['controls_prereg'] = list(pre['controls_required']['ids'])
    v['error_terms'] = list(pre['error_terms_itemized'])
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    v['model_id'] = pre['model_id']
    v['reference_route'] = pre['observable']['reference_route']
    v['state_provenance'] = pre['state_provenance']
    v['shared_premises'] = list(c['shared_premises'])
    v['forward_additional'] = list(c['forward_additional_premises'])
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['new_control_semantics'] = dict(c['new_control_semantics'])
    return v


def av1_values():
    gate = json.loads(read_input(AV1_GATE_REL).decode('utf-8'))
    require(gate.get('loop') == 'AV1' and gate.get('verdict') == 'accepted_within_scope', 'AV1 gate identity')
    raw = read_input(AV1_CONTRACT_REL)
    require(sha_bytes(raw) == gate['bindings'][AV1_CONTRACT_REL], 'AV1 contract snapshot differs from the AV1 gate binding')
    av1 = json.loads(raw.decode('utf-8'))
    am2 = av1['parameters']['am2_constants']
    a = {'R': rat(am2['anchored_radius_R']), 'J0': rat(am2['J0']), 'G_R_upper': rat(am2['G_at_R_upper']),
         'Gp_R_upper': rat(am2['G_prime_at_R_upper'])}
    a['J_coefficient'] = int(match(r'^<=(\d+)\|tau\|$', am2['per_site_sum_J'], 'AV1 J').group(1))
    a['delta_den'] = int(match(r'normalized units delta=alpha/(\d+)', av1['model'], 'delta').group(1))
    m = match(r'(\d+) omitted anchored faces per factor with coefficient alpha\*tau/(\d+)', av1['model'], 'faces')
    a['omitted_per_anchor'], a['face_coefficient_den'] = int(m.group(1)), int(m.group(2))
    m = match(r'D_ii=(\d+)/(\d+) \(~1\.3612e-8; exact rational, certified by both inequalities\)', gate['accepted'], 'AV1 D_ii')
    a['D_ii'] = Q(int(m.group(1)), int(m.group(2)))
    a['gate_sha256'] = sha_bytes(read_input(AV1_GATE_REL))
    return a


def selection_candidates():
    text = read_input(SELECTION_REL).decode('utf-8')
    m = match(r'enumerations \((\d+)/(\d+)/(\d+)/(\d+)/(\d+)\) are the cross-check standard', text, 'selection counts')
    return dict(zip(('faces_per_factor', 'owner_sets', 'meet_R', 'inside_R', 'straddling'), (int(m.group(i)) for i in range(1, 6))))


# ---------------------------------------------------------------------------
# Fine-lattice geometry and the I1 table parsed from the snapshot.
# ---------------------------------------------------------------------------
UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIENT = {'xy': (0, 1), 'xz': (0, 2), 'yz': (1, 2)}
OFFSET = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
COVER_R = frozenset((ORIGIN, EZ))


def add(p, q):
    return tuple(a + b for a, b in zip(p, q))


def sub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links_ordered(face):
    """I1.4: face at p in directions a<c has links (p,a),(p+e_a,c),(p+e_c,a),(p,c)."""
    p, (a, c) = face
    return ((p, a), (add(p, UNIT[a]), c), (add(p, UNIT[c]), a), (p, c))


def links_of(face):
    return frozenset(face_links_ordered(face))


def support_of(face):
    return frozenset(owner(l[0]) for l in face_links_ordered(face))


def is_selected(face):
    p, orient = face
    return orient == (0, 1) and p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)


WILSON = ((0, 0, 0), (0, 2))   # W=(1/2)Tr[U_{0,x}U_{e_x,z}U_{e_z,x}^{-1}U_{0,z}^{-1}]


def parse_i1_table():
    text = read_input(I1_REL).decode('utf-8')
    rows = re.findall(r'^\| (xy|xz|yz): r=([0-9,]+); s=([0-9,]+) \| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|$',
                      text, re.M)
    require(len(rows) == 8, 'I1 table rows')
    table = []
    for orient, rs_, ss_, count, supp, role in rows:
        r_vals = tuple(int(x) for x in rs_.split(','))
        s_vals = tuple(int(x) for x in ss_.split(','))
        require(len(r_vals) * len(s_vals) == int(count), 'I1 row count')
        table.append({'orientation': orient, 'r': r_vals, 's': s_vals,
                      'support': frozenset(OFFSET[t.strip()] for t in supp.split(',')), 'role': role})
    return table


def expand_classes(table, role='omitted'):
    out = []
    for row in table:
        if row['role'] != role:
            continue
        for r in row['r']:
            for q in row['s']:
                out.append((row['orientation'], r, q, row['support']))
    return out


def class_face(anchor, cls):
    orient, r, q, _ = cls
    return ((4 * anchor[0] + r, 2 * anchor[1] + q, anchor[2]), ORIENT[orient])


def owner_set(anchor, cls):
    return frozenset(add(anchor, d) for d in cls[3])


def faces_containing(u, classes):
    """Translation covariance: face (b,k) has owner u iff b=u-d with d in K_k."""
    return [(sub(u, d), cls) for cls in classes for d in sorted(cls[3])]


def derive_counts(classes):
    at0 = faces_containing(ORIGIN, classes)
    sets0 = {}
    for b, cls in at0:
        key = owner_set(b, cls)
        sets0[key] = sets0.get(key, 0) + 1
    meet = {}
    for u in sorted(COVER_R):
        for b, cls in faces_containing(u, classes):
            meet[class_face(b, cls)] = owner_set(b, cls)
    inside = [f for f, m in meet.items() if m <= COVER_R]
    both = [f for f, m in meet.items() if COVER_R <= m]
    strad = [f for f, m in meet.items() if not m <= COVER_R]
    return {'classes': len(classes), 'faces_per_factor': len(at0), 'owner_sets_per_factor': len(sets0),
            'multiplicities': sorted(sets0.values()), 'sets0': sets0,
            'meet_R': len(meet), 'inside_R': len(inside), 'both_R': len(both),
            'strictly_containing_R': len([f for f in both if meet[f] != COVER_R]),
            'straddling': len(strad),
            'straddling_one_outside': len([f for f in strad if len(meet[f] - COVER_R) == 1]),
            'straddling_two_outside': len([f for f in strad if len(meet[f] - COVER_R) == 2]),
            'straddling_meeting_R_once': len([f for f in strad if len(meet[f] & COVER_R) == 1]),
            'zero_not_ez': len([f for f, m in meet.items() if ORIGIN in m and EZ not in m]),
            'ez_not_zero': len([f for f, m in meet.items() if EZ in m and ORIGIN not in m]),
            'meet_faces': meet, 'inside_faces': inside, 'at0': at0}


def brute_force_counts(window=3):
    """Fine-lattice enumeration without the class table."""
    faces = []
    for x in range(-4 * window, 4 * window + 4):
        for y in range(-2 * window, 2 * window + 2):
            for z in range(-window, window + 1):
                for orient in ((0, 1), (0, 2), (1, 2)):
                    f = ((x, y, z), orient)
                    if not is_selected(f):
                        faces.append((f, support_of(f)))
    at0 = [f for f, m in faces if ORIGIN in m]
    sets0 = {}
    for f, m in faces:
        if ORIGIN in m:
            sets0[m] = sets0.get(m, 0) + 1
    meet = [(f, m) for f, m in faces if m & COVER_R]
    return {'faces_per_factor': len(at0), 'owner_sets_per_factor': len(sets0), 'multiplicities': sorted(sets0.values()),
            'meet_R': len(meet), 'inside_R': len([1 for f, m in meet if m <= COVER_R]),
            'both_R': len([1 for f, m in meet if COVER_R <= m]),
            'straddling_one_outside': len([1 for f, m in meet if len(m - COVER_R) == 1]),
            'straddling_two_outside': len([1 for f, m in meet if len(m - COVER_R) == 2])}


def coarse_box(N):
    rng = range(-N, N + 1)
    return frozenset((x, y, z) for x in rng for y in rng for z in rng)


def box_faces(N, classes):
    box = coarse_box(N)
    anchors = [b for b in sorted(box) if all(add(b, d) in box for d in S_STAR)]
    return box, anchors, [class_face(b, cls) for b in anchors for cls in classes]


def owned_links(b):
    out = []
    for r in range(4):
        for q in range(2):
            t = (4 * b[0] + r, 2 * b[1] + q, b[2])
            for d in range(3):
                out.append((t, d))
    return out


def box_links(box):
    return frozenset(l for b in box for l in owned_links(b))


def box_plaquettes(box):
    links = box_links(box)
    tails = sorted({l[0] for l in links})
    out = []
    for p in tails:
        for orient in ((0, 1), (0, 2), (1, 2)):
            f = (p, orient)
            if links_of(f) <= links:
                out.append(f)
    return out


# ---------------------------------------------------------------------------
# SU(2) character algebra in exact rationals (Peter-Weyl on each link).
# ---------------------------------------------------------------------------
def tensor_power(n):
    """Multiplicities of spin j (key 2j) in the n-fold tensor power of spin 1/2 (Clebsch-Gordan)."""
    mult = {0: 1}
    for _ in range(n):
        new = {}
        for tj, m in mult.items():
            for nj in (tj - 1, tj + 1):
                if nj >= 0:
                    new[nj] = new.get(nj, 0) + m
        mult = new
    return mult


def trivial_multiplicity(n):
    return tensor_power(n).get(0, 0)


def moment_character(n):
    """E[W^n]=2^-n E[chi_{1/2}^n]=2^-n x (multiplicity of spin 0 in (1/2)^{x n})."""
    return Q(trivial_multiplicity(n), 2 ** n)


def double_factorial(n):
    out = 1
    while n > 1:
        out *= n
        n -= 2
    return out


def moment_wallis(n):
    """Weyl integration: E[cos^n] with density (2/pi) sin^2 on [0,pi]; pi cancels (Wallis)."""
    def i_over_pi(m):
        return Q(0) if m % 2 else Q(double_factorial(m - 1), double_factorial(m))
    return 2 * (i_over_pi(n) - i_over_pi(n + 2))


def moment_sphere(n):
    """Free-link route (AQ2 section 5): U Haar = q_0+i q.sigma uniform on S^3, W=q_0; E[q_0^n] on S^3."""
    if n % 2:
        return Q(0)
    out = Q(1)
    for i in range(n // 2):
        out *= Q(2 * i + 1, 4 + 2 * i)
    return out


def link_counts(word):
    counts = {}
    for f in word:
        for l in links_of(f):
            counts[l] = counts.get(l, 0) + 1
    return counts


def haar_vanishes(word):
    """Per-link character count: the Haar integral over a link carrying k spin-1/2 factors is the
    projection onto invariants of (1/2)^{x k}; it vanishes when that multiplicity is zero."""
    return any(trivial_multiplicity(k) == 0 for k in link_counts(word).values())


def expect(word):
    """Exact Haar expectation of a product of face traces W_f (only the cases this loop needs)."""
    if not word:
        return Q(1)
    if haar_vanishes(word):
        return Q(0)
    if all(f == word[0] for f in word):
        return moment_character(len(word))
    raise AdmissionError('expectation not evaluated by this checker: ' + repr(word))


def energy_spectrum(word):
    """Possible normalized H_0 energies (8 sum j(j+1)) of the components of prod W_f Omega_0."""
    options = []
    for l, k in sorted(link_counts(word).items()):
        options.append(sorted(tj for tj, m in tensor_power(k).items() if m > 0))
    out = set()
    for combo in itertools.product(*options):
        out.add(sum(2 * tj * (tj + 2) for tj in combo))   # 8 j(j+1) with tj=2j
    return out


# ---------------------------------------------------------------------------
# The flip set E (parsed from the contract) and the per-link centre grading.
# ---------------------------------------------------------------------------
def make_in_E(spec, removed=frozenset()):
    def in_E(link):
        if link in removed:
            return False
        p, d = link
        return p[spec[d]] % 2 == 0
    return in_E


def flip_count(face, in_E):
    return sum(1 for l in face_links_ordered(face) if in_E(l))


def validate_odd(faces, in_E, label):
    for f in faces:
        require(flip_count(f, in_E) % 2 == 1, 'even intersection with E (' + label + ') at ' + repr(f))
    return True


# ---------------------------------------------------------------------------
# Exact small fixtures.
# ---------------------------------------------------------------------------
def quat_mul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def quat_inv(p):
    return (p[0], -p[1], -p[2], -p[3])


def quat_neg(p):
    return tuple(-x for x in p)


RATIONAL_SU2 = [(Q(1, 2), Q(1, 2), Q(1, 2), Q(1, 2)), (Q(3, 5), Q(4, 5), Q(0), Q(0)), (Q(0), Q(3, 5), Q(0), Q(4, 5)),
                (Q(2, 3), Q(1, 3), Q(2, 3), Q(0)), (Q(1, 3), Q(2, 3), Q(0), Q(2, 3)), (Q(2, 7), Q(3, 7), Q(6, 7), Q(0)),
                (Q(6, 11), Q(6, 11), Q(7, 11), Q(0)), (Q(-1, 2), Q(1, 2), Q(-1, 2), Q(1, 2))]


def link_matrix(link, flipset=None):
    p, d = link
    idx = (7 * p[0] + 3 * p[1] + 5 * p[2] + 2 * d) % len(RATIONAL_SU2)
    u = RATIONAL_SU2[idx]
    require(sum(x * x for x in u) == 1, 'rational unit quaternion')
    if flipset is not None and flipset(link):
        u = quat_neg(u)
    return u


def half_trace_holonomy(face, flipset=None, reverse=False, shift=0, gauge=None):
    l1, l2, l3, l4 = face_links_ordered(face)
    mats = []
    for l in (l1, l2, l3, l4):
        u = link_matrix(l, flipset)
        if gauge is not None:
            p, d = l
            u = quat_mul(quat_mul(gauge(p), u), quat_inv(gauge(add(p, UNIT[d]))))
        mats.append(u)
    seq = [mats[0], mats[1], quat_inv(mats[2]), quat_inv(mats[3])]
    seq = seq[shift:] + seq[:shift]
    h = (Q(1), Q(0), Q(0), Q(0))
    for u in seq:
        h = quat_mul(h, u)
    if reverse:
        h = quat_inv(h)
    return h[0]


def haar_monomial(exps):
    """E over (alpha,beta) uniform on S^3 subset C^2 of alpha^a abar^b beta^c bbar^d."""
    a, b, c, d = exps
    if a != b or c != d:
        return Q(0)
    return Q(factorial(a) * factorial(c), factorial(a + c + 1))


# SU(2) matrix U=[[alpha,-conj(beta)],[beta,conj(alpha)]]: entries as (sign, exponent vector).
U_ENTRY = {(0, 0): (1, (1, 0, 0, 0)), (0, 1): (-1, (0, 0, 0, 1)), (1, 0): (1, (0, 0, 1, 0)), (1, 1): (1, (0, 1, 0, 0))}


def conj_entry(e):
    sgn, (a, b, c, d) = e
    return sgn, (b, a, d, c)


def haar_product(entries):
    sign = 1
    tot = (0, 0, 0, 0)
    for sg, ex in entries:
        sign *= sg
        tot = tuple(x + y for x, y in zip(tot, ex))
    return sign * haar_monomial(tot)


def one_link_fixture():
    """Exact j<=1/2 compression on L^2(SU(2)) in the basis (1, U_11, U_12, U_21, U_22)."""
    idx = [None, (0, 0), (0, 1), (1, 0), (1, 1)]

    def bra(i):
        return [] if idx[i] is None else [conj_entry(U_ENTRY[idx[i]])]

    def ket(j):
        return [] if idx[j] is None else [U_ENTRY[idx[j]]]
    gram = [[haar_product(bra(i) + ket(j)) for j in range(5)] for i in range(5)]
    mult = {}
    for ab in ((0, 0), (0, 1), (1, 0), (1, 1)):
        mult[ab] = [[haar_product(bra(i) + [U_ENTRY[ab]] + ket(j)) for j in range(5)] for i in range(5)]
    casimir = [[(Q(3, 4) if i > 0 else Q(0)) * gram[i][j] for j in range(5)] for i in range(5)]
    parity = [1, -1, -1, -1, -1]
    return gram, mult, casimir, parity


def plaquette_character_fixture(kmax):
    """One gauge-invariant plaquette: |k>=chi_{k/2}(U_P), H_0=32 j(j+1)=8k(k+2), W|k>=(|k-1>+|k+1>)/2."""
    n = kmax + 1
    H0 = [[Q(8 * i * (i + 2)) if i == j else Q(0) for j in range(n)] for i in range(n)]
    Wm = [[Q(1, 2) if abs(i - j) == 1 else Q(0) for j in range(n)] for i in range(n)]
    return H0, Wm


def matmul(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), Q(0)) for j in range(len(B[0]))] for i in range(len(A))]


def matvec(A, v):
    return [sum((A[i][k] * v[k] for k in range(len(v))), Q(0)) for i in range(len(A))]


def diag_conj(sign, A):
    return [[sign[i] * A[i][j] * sign[j] for j in range(len(A))] for i in range(len(A))]


def rs_mean_series(kmax, order, coupling_den):
    """Rayleigh-Schrodinger series of <W> on the one-plaquette fixture, V=-(tau/coupling_den) W."""
    H0, Wm = plaquette_character_fixture(kmax)
    n = kmax + 1
    V1 = [[-x / coupling_den for x in row] for row in Wm]
    psi = [[Q(1)] + [Q(0)] * (n - 1)]
    energies = [Q(0)]
    for m in range(1, order + 1):
        energies.append(matvec(V1, psi[m - 1])[0])
        rhs = [-x for x in matvec(V1, psi[m - 1])]
        for i in range(1, m):
            rhs = [r + energies[i] * y for r, y in zip(rhs, psi[m - i])]
        psi.append([Q(0)] + [rhs[k] / H0[k][k] for k in range(1, n)])

    def ip(u, w):
        return sum((a * b for a, b in zip(u, w)), Q(0))
    num = [sum((ip(psi[i], matvec(Wm, psi[m - i])) for i in range(m + 1)), Q(0)) for m in range(order + 1)]
    den = [sum((ip(psi[i], psi[m - i]) for i in range(m + 1)), Q(0)) for m in range(order + 1)]
    series = []
    for m in range(order + 1):
        series.append((num[m] - sum((series[i] * den[m - i] for i in range(m)), Q(0))) / den[0])
    return series, energies


def two_level_mean_bracket(tau, coupling_den):
    """Exact j<=1/2 plaquette truncation H=[[0,b],[b,24]], b=-tau/(2 coupling_den); <W>=b E0/(b^2+E0^2)."""
    b = -tau / (2 * coupling_den)
    disc = 144 + b * b
    e_lo = 12 - sqrt_up(disc, 10 ** 30)
    e_hi = 12 - sqrt_lo(disc, 10 ** 30)
    require(e_lo <= e_hi < 0 and e_lo * e_lo < b * b, 'ground energy bracket (and monotonicity window |E0|<|b|)')
    vals = [b * e / (b * b + e * e) for e in (e_lo, e_hi)]
    # <W>(E0) is monotone on the bracket (E0 near -b^2/24); take the hull of the endpoint values.
    return min(vals), max(vals), (e_lo, e_hi)


# Creation-algebra fixture on qubit sites (vacuum 0, excited 1) for the overlap structure.
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


def vadd(u, w, a=1):
    out = dict(u)
    for k, x in w.items():
        out[k] = out.get(k, 0) + a * x
    return {k: x for k, x in out.items() if x != 0}


def inner(u, w):
    return sum((u[k] * w[k] for k in u if k in w), Q(0))


def product_state(n, creations):
    vec = {(0,) * n: Q(1)}
    for support, coeff in creations:
        vec = vadd(vec, c_hat(vec, support, coeff), -1)
    return vec


def apply_X(vec, r0, r1):
    """X=|11><00|+|00><11| on sites (r0,r1): the qubit analogue of W on R (moves Omega_R to the doubly excited sector)."""
    out = {}
    for bits, amp in vec.items():
        if bits[r0] == bits[r1]:
            nb = list(bits)
            nb[r0] = nb[r1] = 1 - bits[r0]
            out[tuple(nb)] = out.get(tuple(nb), 0) + amp
    return out


# ---------------------------------------------------------------------------
# Second-order remainder K_2: every term names its tier; mixing is rejected.
# ---------------------------------------------------------------------------
def assemble_k2(tier, tau, terms):
    """terms: list of (name, tier_label, value, order).  Returns K_2=sum/tau^2."""
    for name, label, value, _ in terms:
        require(label == tier, 'tier mixing rejected: ' + name + ' is tier ' + label + ' inside tier ' + tier)
        require(isinstance(value, Q) and value > 0, 'itemized term missing, zero or non-exact: ' + name)
    names = [n for n, _, _, _ in terms]
    required = ('am2_remainder', 'two_creation', 'straddling', 'density', 'normalization_order')
    require(sorted(names) == sorted(required), 'itemized terms incomplete: ' + ','.join(names))
    total = sum((v for _, _, v, _ in terms), Q(0))
    return total, total / (tau * tau)


def k2_exact(tau, V, A1, counts, overlap=Q(1), remainder='gate', pinned=True, tier='exact', t_override=None):
    a = abs(tau) * V['per_face_norm']
    J = A1['J_coefficient'] * abs(tau)
    t1 = counts['faces_per_factor'] * a
    L = Q(V['remainder_coefficient'])
    require(L == A1['Gp_R_upper'], 'remainder coefficient must be the admitted AM2 bound G\'(R)<352')
    if remainder == 'gate':
        T = t1 / (1 - L * J)
        rho = L * J * T
    else:   # sharper directed form G(t)-16<=288t/(1-8t), t<=t_i (reviewed in AV1, not the gate bound)
        ti = J * A1['G_R_upper']
        T = t1 / (1 - 288 * J / (1 - 8 * ti))
        rho = 288 * J * T / (1 - 8 * ti)
    if t_override is not None:
        T = t_override
    require(T < A1['R'], 't inside the AM2 ball')
    eps = 2 * T + T * T
    A0 = counts['zero_not_ez'] * a + rho if pinned else T
    Az = counts['ez_not_zero'] * a + rho if pinned else T
    sup = counts['strictly_containing_R'] * a + rho if pinned else T
    terms = [('am2_remainder', tier, overlap * rho, 2), ('two_creation', tier, A0 * Az, 2),
             ('straddling', tier, T * sup, 2), ('density', tier, eps * eps, 2),
             ('normalization_order', tier, a * eps * eps, 3)]
    total, K = assemble_k2(tier, tau, terms)
    return {'tier': tier, 'tau': tau, 'a': a, 'J': J, 't1': t1, 'T': T, 'rho': rho, 'eps': eps, 'A0': A0, 'Az': Az,
            'strictly_containing_sum': sup, 'terms': terms, 'total': total, 'K2': K, 'overlap': overlap,
            'remainder_form': remainder, 'pinned': pinned}


def k2_crude(tau, V, A1, tier='crude'):
    a = abs(tau) * V['per_face_norm']
    J = A1['J_coefficient'] * abs(tau)
    ti = J * A1['G_R_upper']
    require(ti < A1['R'], 'crude t inside the AM2 ball')
    rho = Q(V['remainder_coefficient']) * J * ti
    eps = 2 * ti + ti * ti
    terms = [('am2_remainder', tier, rho, 2), ('two_creation', tier, ti * ti, 2), ('straddling', tier, ti * ti, 2),
             ('density', tier, eps * eps, 2), ('normalization_order', tier, a * eps * eps, 3)]
    total, K = assemble_k2(tier, tau, terms)
    return {'tier': tier, 'tau': tau, 'a': a, 'J': J, 'T': ti, 'rho': rho, 'eps': eps, 'terms': terms, 'total': total, 'K2': K}


def k2_record(x):
    rec = {'tier': x['tier'], 'tau': s(x['tau']), 't_bound': s(x['T']), 'am2_remainder_rho': s(x['rho']), 'eps': s(x['eps']),
           'K2': s(x['K2']), 'K2_decimal_preview': dec(x['K2']), 'total_at_tau': s(x['total']),
           'terms': {n: {'tier': lab, 'value': s(val), 'over_tau2': s(val / (x['tau'] * x['tau'])),
                         'over_tau2_preview': dec(val / (x['tau'] * x['tau'])), 'order_in_tau': order}
                     for n, lab, val, order in x['terms']}}
    for k in ('remainder_form', 'pinned'):
        if k in x:
            rec[k] = x[k]
    if 'overlap' in x:
        rec['overlap_multiplier'] = s(x['overlap'])
    return rec


def aw2_rule(K, V):
    k = V['grid_start']
    while K * Q(1, 10 ** k) > V['rule_bound']:
        k += 1
        require(k <= V['grid_start'] + 60, 'decade grid exhausted')
    return Q(1, 10 ** k)


def validate_rule_choice(choice, K, V, tier):
    require(tier == 'exact', 'AW2 rule must use the exact-tier constant')
    require(choice == aw2_rule(K, V), 'AW2 coupling differs from the frozen decade-grid rule')
    return True


def float_free(obj):
    if isinstance(obj, float):
        return False
    if isinstance(obj, dict):
        return all(float_free(v) for v in obj.values())
    if isinstance(obj, list):
        return all(float_free(v) for v in obj)
    return True


# ===========================================================================
def compute(check_sha):
    c, contract_digest = load_contract()
    V = contract_values(c)
    A1 = av1_values()
    SEL = selection_candidates()
    tau_cap = V['tau_cap']
    taus = {'+': tau_cap, '-': -tau_cap}

    # -------------------- contract and premise binding --------------------
    check('contract_binding',
          V['controls'] == V['controls_prereg'] and len(set(V['controls'])) == len(V['controls']) == 30
          and V['target'] == V['rule_bound'] and 'static_not_dynamic' in V['sub_labels']
          and V['model_id'] == 'AQ_patterned_zero_selected' and V['reference_route'] == 'haar',
          contract_sha256=contract_digest, check_py_sha256_recorded_before_evaluation=check_sha,
          target_read_from_contract=s(V['target']), reference_values_read_from_contract=[s(V['ref_W']), s(V['ref_W2'])],
          flip_set_read_from_contract=V['flip_set_text'], aw2_rule_read_from_contract=V['rule_text'],
          controls_equal_preregistration_mirror=True)
    check('av1_premise_binding',
          A1['J_coefficient'] == 28 and A1['J0'] == A1['J_coefficient'] * tau_cap and A1['R'] == Q(1, 64)
          and A1['G_R_upper'] == Q(148, 7) and A1['Gp_R_upper'] == V['remainder_coefficient']
          and A1['face_coefficient_den'] == V['phi_den'] * A1['delta_den'] and A1['omitted_per_anchor'] == 21,
          av1_gate_sha256=A1['gate_sha256'], av1_contract_bound_by_gate=True, D_ii_admitted=s(A1['D_ii']),
          J=str(A1['J_coefficient']) + '|tau|', G_R_upper=s(A1['G_R_upper']), G_prime_R_upper=s(A1['Gp_R_upper']))

    # -------------------- geometry and enumeration --------------------
    table = parse_i1_table()
    classes = expand_classes(table)
    sel_classes = expand_classes(table, 'selected')
    probe_anchors = (ORIGIN, (1, -1, 2), (-2, 3, -1))
    geo_ok = all(support_of(class_face(b, cls)) == owner_set(b, cls) and not is_selected(class_face(b, cls))
                 for b in probe_anchors for cls in classes)
    geo_ok = geo_ok and all(is_selected(class_face(b, cls)) and support_of(class_face(b, cls)) == owner_set(b, cls)
                            for b in probe_anchors for cls in sel_classes)
    counts = derive_counts(classes)
    brute = brute_force_counts()
    derived = {'faces_per_factor': counts['faces_per_factor'], 'owner_sets': counts['owner_sets_per_factor'],
               'meet_R': counts['meet_R'], 'inside_R': counts['inside_R'], 'straddling': counts['straddling']}

    def compare_candidates(cnt):
        require(cnt['faces_per_factor'] == V['faces_per_factor_cand'], 'faces per factor differs from contract item 2')
        require(cnt['owner_sets_per_factor'] == V['owner_sets_cand'], 'owner sets differ from contract item 4')
        require(cnt['multiplicities'] == V['multiplicities_cand'], 'owner-set multiplicities differ from contract item 4')
        require(cnt['meet_R'] == V['meet_R_cand'] and cnt['both_R'] == V['both_R_cand'], 'R counts differ from contract item 4')
        require(cnt['classes'] == V['classes_cand'], 'class count differs')
        return True
    dropped = expand_classes([row for row in table if not (row['orientation'] == 'yz' and row['s'] == (1,))])
    check('face_enumeration_derived',
          geo_ok and len(classes) == 21 and len(sel_classes) == 3 and compare_candidates(counts)
          and derived == SEL
          and all(brute[k] == counts[k] for k in ('faces_per_factor', 'owner_sets_per_factor', 'multiplicities', 'meet_R',
                                                   'inside_R', 'both_R', 'straddling_one_outside', 'straddling_two_outside'))
          and counts['straddling'] == counts['straddling_one_outside'] + counts['straddling_two_outside']
          and counts['straddling'] == counts['straddling_meeting_R_once'] + counts['strictly_containing_R']
          and counts['both_R'] == counts['inside_R'] + counts['strictly_containing_R']
          and counts['zero_not_ez'] == counts['faces_per_factor'] - counts['both_R'] == counts['ez_not_zero']
          and rejected(lambda: compare_candidates(derive_counts(dropped)), 'table_row_dropped'),
          faces_per_factor=counts['faces_per_factor'], owner_sets_per_factor=counts['owner_sets_per_factor'],
          multiplicities=counts['multiplicities'], faces_meeting_R=counts['meet_R'], faces_inside_R=counts['inside_R'],
          faces_touching_both_factors_of_R=counts['both_R'], faces_strictly_containing_R=counts['strictly_containing_R'],
          straddling_faces=counts['straddling'], straddling_one_outside_site=counts['straddling_one_outside'],
          straddling_two_outside_sites=counts['straddling_two_outside'],
          straddling_meeting_R_in_one_site=counts['straddling_meeting_R_once'],
          faces_containing_0_not_ez=counts['zero_not_ez'], faces_containing_ez_not_0=counts['ez_not_zero'],
          derived_from='I1 table parsed from the snapshot, supports re-derived from I1.4, translation covariance; fine-lattice brute force',
          selection_cross_check_standard=SEL)

    anchor0 = [class_face(ORIGIN, cls) for cls in classes]
    others0 = [f for f in anchor0 if f != WILSON]
    w_links = face_links_ordered(WILSON)
    w_owners = [owner(l[0]) for l in w_links]
    box2, anchors2, faces2 = box_faces(2, classes)
    meet_faces = sorted(counts['meet_faces'])
    inside_faces = sorted(counts['inside_faces'])

    # -------------------- SU(2) character algebra (haar_parity_exact) --------------------
    mults = [trivial_multiplicity(n) for n in range(11)]
    catalan = [comb(n, n // 2) // (n // 2 + 1) if n % 2 == 0 else 0 for n in range(11)]
    routes = {n: (moment_character(n), moment_wallis(n), moment_sphere(n)) for n in range(9)}

    def validate_moment_table(table_mult):
        for n in range(9):
            char = Q(table_mult[n], 2 ** n)
            require(char == moment_wallis(n) == moment_sphere(n), 'character count disagrees with Weyl/free-link route at n=%d' % n)
        return True
    bad_mult = list(mults)
    bad_mult[3] = 1
    w2wf_sets = {'anchor0_21_classes_including_W': anchor0, 'faces_meeting_R_82': meet_faces, 'box_N2_retained_faces': faces2}
    w2wf_zero = all(expect([WILSON, WILSON, f]) == V['ref_W2Wf'] for fs in w2wf_sets.values() for f in fs)
    wwf_ok = all(expect([WILSON, f]) == (V['ref_W2'] if f == WILSON else 0) for fs in w2wf_sets.values() for f in fs)
    share = max(len(links_of(f) & links_of(g)) for f in meet_faces for g in meet_faces if f != g)
    check('haar_parity_exact',
          mults == catalan and validate_moment_table(mults)
          and routes[1][0] == V['ref_W'] and routes[2][0] == V['ref_W2'] and routes[3][0] == V['ref_W3'] and routes[4][0] == V['ref_W4']
          and expect([WILSON]) == V['ref_W'] and expect([WILSON] * 2) == V['ref_W2'] and expect([WILSON] * 3) == V['ref_W3']
          and expect([WILSON] * 4) == V['ref_W4'] and w2wf_zero and wwf_ok and WILSON in anchor0 and share == 1
          and rejected(lambda: validate_moment_table(bad_mult), 'odd_tensor_power_given_invariant'),
          trivial_multiplicities_n0_to_10=mults, moments={str(n): [s(x) for x in routes[n]] for n in routes},
          routes=['character count 2^-n mult(0 in (1/2)^{x n})', 'Weyl/Wallis (2/pi) int cos^n sin^2',
                  'free z link: face holonomy Haar, W=q_0 on S^3 (AQ2 section 5, named cross-check)'],
          E_W2_Wf_zero_on=sorted((k, len(v)) for k, v in w2wf_sets.items()), max_links_shared_by_distinct_faces=share,
          wilson_face_links=[[list(l[0]), 'xyz'[l[1]]] for l in w_links], wilson_owners=[list(o) for o in w_owners])

    # -------------------- parity theorem: first-order terms --------------------
    coef_norm = Q(1, V['phi_den']) / V['energy_norm']
    coef_alpha = Q(1, V['phi_den'] * A1['delta_den']) / V['energy_alpha']
    require(coef_norm == coef_alpha, 'first-order coefficient differs between unit systems')
    norm_wf = exact_sqrt(expect([WILSON, WILSON]))
    V['per_face_norm'] = coef_norm * norm_wf
    v_alpha = Q(1, V['phi_den'] * A1['delta_den'])          # V_1=-(v_alpha) sum W_f in G=H/alpha units
    m1 = 2 * coef_norm * expect([WILSON, WILSON])            # first-order mean per unit tau (derived below)

    def first_order_terms(F):
        return {
            'omega_W2_state': sum((2 * coef_norm * (expect([WILSON, WILSON, f]) - V['ref_W2'] * expect([f])) for f in F), Q(0)),
            'C_state': sum((2 * coef_norm * expect([WILSON, WILSON, f]) for f in F), Q(0)),
            'C_vector_centering': -2 * m1 * expect([WILSON]),
            'C_duhamel': sum((-v_alpha * expect([WILSON, f, WILSON]) for f in F), Q(0)),
            'energy': sum((-v_alpha * expect([f]) for f in F), Q(0)),
            'realtime_state': sum((2 * coef_norm * expect([WILSON, WILSON, f]) for f in F), Q(0)),
            'realtime_duhamel': sum((-v_alpha * expect([WILSON, f, WILSON]) for f in F), Q(0)),
            'uncentered_mean_control': sum((2 * coef_norm * expect([WILSON, f]) for f in F), Q(0)),
        }
    fo_box = first_order_terms(faces2)
    fo_bulk = first_order_terms(meet_faces)
    vanish_keys = [k for k in fo_box if k != 'uncentered_mean_control']

    def claim_first_order_vanishes(terms, keys):
        for k in keys:
            require(terms[k] == 0, 'first-order term does not vanish: ' + k)
        return True

    def parity_hypotheses(reference):
        require(reference == 'haar_zero_selected', 'parity theorem needs the centre-even Haar reference (zero selected triple)')
        return True
    check('first_order_shift_of_C_vanishes',
          claim_first_order_vanishes(fo_box, vanish_keys) and claim_first_order_vanishes(fo_bulk, vanish_keys)
          and parity_hypotheses('haar_zero_selected')
          and fo_box['uncentered_mean_control'] == fo_bulk['uncentered_mean_control'] == Q(1, V['candidate_den'])
          and rejected(lambda: claim_first_order_vanishes(fo_box, ['uncentered_mean_control']), 'parity_applied_to_uncentered_mean')
          and rejected(lambda: parity_hypotheses('selected_strip_nonzero_triple'), 'nonzero_triple_reference'),
          terms_box_N2={k: s(v) for k, v in fo_box.items()}, terms_bulk_82={k: s(v) for k, v in fo_bulk.items()},
          structure={'state': '2 Re<W^2 Omega_0, psi_1> e^{-3s}, psi_1=(1/72) sum_f W_f Omega_0',
                     'vector_centering': '-m_1 <W Omega_0, Omega_0> e^{-3s}, vanishes by E[W]=0 although m_1=1/144',
                     'duhamel': '-s e^{-3s} <W Omega_0, (V_1-E_1) W Omega_0>, V_1=-(1/24) sum_f W_f (alpha units)',
                     'energy': 'E_1=<Omega_0,V_1 Omega_0>', 'real_time': 'same face sums with e^{3i theta} and i theta e^{3i theta}'},
          C_s_statement='C_N(s)=e^{-3s}/4+O_N(tau^2) in each box; the O(tau^2) constant is not proved uniform in N (explicitly unbounded)')

    # -------------------- degenerate multiplet --------------------
    E24 = V['multiplet_energy']
    spec_faces = sorted(set(anchor0) | set(meet_faces) | set(faces2))
    spectra = {f: energy_spectrum([WILSON, f]) for f in spec_faces}
    identity_only_W = all((0 in spectra[f]) == (f == WILSON) for f in spec_faces)
    no24 = all(E24 not in spectra[f] for f in spec_faces)
    spectrum_W = sorted(spectra[WILSON])
    shared_one = sorted({tuple(sorted(spectra[f])) for f in spec_faces if len(links_of(f) & links_of(WILSON)) == 1})
    disjoint = sorted({tuple(sorted(spectra[f])) for f in spec_faces if not links_of(f) & links_of(WILSON)})
    casimir_solutions = [combo for size in range(1, 5) for combo in itertools.combinations_with_replacement((1, 2, 3), size)
                         if sum(2 * tj * (tj + 2) for tj in combo) == E24]
    steps = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    cycles = set()
    for walk in itertools.product(steps, repeat=4):
        pos = ORIGIN
        edges = []
        for st in walk:
            nxt = add(pos, st)
            edges.append(frozenset((pos, nxt)))
            pos = nxt
        if pos == ORIGIN and len(set(edges)) == 4:
            cycles.add(frozenset(edges))
    plaq_edge_sets = set()
    for orient in ((0, 1), (0, 2), (1, 2)):
        for base in itertools.product((-1, 0), repeat=3):
            f = (base, orient)
            verts = set()
            es = set()
            for (p, d) in face_links_ordered(f):
                q = add(p, UNIT[d])
                es.add(frozenset((p, q)))
                verts |= {p, q}
            if ORIGIN in verts:
                plaq_edge_sets.add(frozenset(es))
    box1 = coarse_box(1)
    plaqs1 = box_plaquettes(box1)
    link_sets1 = [links_of(g) for g in plaqs1]
    pair_sizes = set()
    for i in range(len(link_sets1)):
        for j in range(i + 1, len(link_sets1)):
            pair_sizes.add(len(link_sets1[i] ^ link_sets1[j]))
    near_w = [g for g in plaqs1 if links_of(g) & links_of(WILSON)]
    triple_zero = all(expect([g, f, h]) == 0 for g in near_w for h in near_w for f in meet_faces)
    far_face = class_face((0, 1, 0), classes[0])
    p_links = frozenset(list(w_links)[:2]) | frozenset(list(face_links_ordered(far_face))[:2])

    def claim_full_space_compression_zero(p, f):
        diff = p ^ links_of(f)
        require(not (len(p) == 4 and len(diff) == 4), 'parity allows <p xor f| W_f |p> on the full-space energy-24 multiplet')
        return True

    def claim_identity_at_24(spec):
        require(E24 in spec, 'the identity component of W^2 Omega_0 sits at energy 0, not 24')
        return True
    check('degenerate_multiplet_first_order',
          no24 and identity_only_W and 0 in spectra[WILSON] and expect([WILSON, WILSON]) == V['ref_W2']
          and casimir_solutions == [(1, 1, 1, 1)] and len(cycles) == 12 and cycles == plaq_edge_sets
          and 4 not in pair_sizes and triple_zero
          and rejected(lambda: claim_full_space_compression_zero(p_links, WILSON), 'full_space_multiplet_claimed_unsplit_by_parity')
          and rejected(lambda: claim_identity_at_24(spectra[WILSON]), 'identity_component_counted_at_24'),
          multiplet_energy_normalized=E24, spectrum_of_W2_Omega0=spectrum_W,
          spectra_faces_sharing_one_link=[list(t) for t in shared_one], spectra_disjoint_faces=[list(t) for t in disjoint],
          identity_component='(1/4) Omega_0 at energy 0, only for f=W', faces_checked=len(spec_faces),
          casimir_sum_solutions=[list(t) for t in casimir_solutions], four_cycles_through_origin=len(cycles),
          plaquette_pair_symmetric_difference_sizes=sorted(pair_sizes), plaquettes_in_box_N1=len(plaqs1),
          physical_multiplet='span{W_g Omega_0: g plaquette}; P V P=0 there (E[W_g W_f W_h]=0 since g xor h is never a face)',
          full_space_note='on non-gauge-invariant energy-24 vectors parity does not force the compression to vanish; the zero-splitting statement is for the gauge-invariant multiplet in which chi and the dynamics live')

    # -------------------- flip lemma: enumeration --------------------
    in_E = make_in_E(V['flip_spec'])
    parity_classes = []
    for oname in sorted(ORIENT):
        orient = ORIENT[oname]
        for par in itertools.product((0, 1), repeat=3):
            cnt = flip_count((par, orient), in_E)
            cov = all(flip_count((add(par, (2 * i, 2 * j, 2 * k)), orient), in_E) == cnt
                      for i in (-2, -1, 1, 3) for j in (-1, 2) for k in (-3, 1))
            parity_classes.append({'orientation': oname, 'base_parity': list(par), 'links_in_E': cnt, 'covariant': cov})
    classes_odd = all(pc['links_in_E'] % 2 == 1 and pc['covariant'] for pc in parity_classes) and len(parity_classes) == 24
    factor_probe = (ORIGIN, EZ, (1, 0, 0), (0, 1, 0), (1, 1, 1), (-1, -1, -1), (2, -3, 5))
    factor_faces = {u: [class_face(b, cls) for b, cls in faces_containing(u, classes)] for u in factor_probe}
    selected_at = {u: [class_face(u, cls) for cls in sel_classes] for u in factor_probe}
    factor_ok = all(len(fs) == V['faces_per_factor_cand'] and len(set(fs)) == len(fs) and validate_odd(fs, in_E, 'factor faces')
                    for fs in factor_faces.values())
    selected_ok = all(validate_odd(fs, in_E, 'selected faces') for fs in selected_at.values())
    plaqs2 = box_plaquettes(box2)
    hist2 = {}
    for g in plaqs2:
        k = flip_count(g, in_E)
        hist2[k] = hist2.get(k, 0) + 1
    removed_E = make_in_E(V['flip_spec'], removed=frozenset([w_links[0]]))

    def periodic_validate(sides):
        for base in itertools.product(*(range(L) for L in sides)):
            for orient in ((0, 1), (0, 2), (1, 2)):
                lk = [(tuple(x % L for x, L in zip(p, sides)), d) for p, d in face_links_ordered((base, orient))]
                require(sum(1 for l in lk if in_E(l)) % 2 == 1, 'even plaquette on the periodic box %r' % (sides,))
        return True

    def gauge_set(l):
        return ORIGIN in (l[0], add(l[0], UNIT[l[1]]))

    def claim_implements_flip(member):
        for g in plaqs2:
            require(flip_count(g, member) % 2 == 1, 'a centre gauge transformation meets plaquettes evenly and flips no W_f')
        return True

    def claim_term_flips(two_j, count):
        require((-1) ** (two_j * count) == -1, 'U_E leaves a spin-%d/2 face term invariant' % two_j)
        return True
    check('flip_set_odd_intersection',
          classes_odd and factor_ok and selected_ok and validate_odd(plaqs2, in_E, 'box N=2') and flip_count(WILSON, in_E) == 3
          and set(hist2) == {1, 3} and validate_odd(faces2, in_E, 'retained stars') and periodic_validate((4, 4, 2))
          and claim_term_flips(1, flip_count(WILSON, in_E))
          and rejected(lambda: validate_odd(plaqs2, removed_E, 'E minus one link'), 'E_minus_one_link')
          and rejected(lambda: periodic_validate((4, 3, 2)), 'odd_periodic_side')
          and rejected(lambda: claim_implements_flip(gauge_set), 'centre_gauge_transformation_as_flip')
          and rejected(lambda: claim_term_flips(2, flip_count(WILSON, in_E)), 'spin_one_term_claimed_to_flip'),
          parity_classes=parity_classes, faces_per_probed_factor={','.join(map(str, u)): len(fs) for u, fs in factor_faces.items()},
          selected_faces_odd_at_probes=True, box_N2_plaquettes=len(plaqs2), box_N2_histogram={str(k): v for k, v in sorted(hist2.items())},
          wilson_links_in_E=flip_count(WILSON, in_E),
          proof='translation by even vectors preserves E; |f cap E| depends only on orientation and base parity; all 24 classes odd')

    # -------------------- flip lemma: operator fixtures --------------------
    gram, multm, casimir, parity = one_link_fixture()
    gram_ok = all(gram[i][j] == ((Q(1) if i == 0 else Q(1, 2)) if i == j else 0) for i in range(5) for j in range(5))
    eps2 = {(0, 1): 1, (1, 0): -1}
    second_moments_ok = all(haar_product([U_ENTRY[(a1, b1)], U_ENTRY[(c1, d1)]]) == Q(eps2.get((a1, c1), 0) * eps2.get((b1, d1), 0), 2)
                            for a1, b1, c1, d1 in itertools.product((0, 1), repeat=4))
    mult_flip = all(diag_conj(parity, M) == [[-x for x in row] for row in M] and any(x != 0 for row in M for x in row)
                    for M in multm.values())
    cas_even = diag_conj(parity, casimir) == casimir

    def gauge(p):
        return RATIONAL_SU2[(3 * p[0] + 5 * p[1] + 2 * p[2] + 1) % len(RATIONAL_SU2)]
    qfaces = sorted(set(anchor0 + selected_at[ORIGIN] + factor_faces[EZ]))
    quat_rows = []
    for f in qfaces:
        w0 = half_trace_holonomy(f)
        rev = half_trace_holonomy(f, reverse=True)
        shifts = [half_trace_holonomy(f, shift=k) for k in (1, 2, 3)]
        flipped = half_trace_holonomy(f, flipset=in_E)
        gauged = half_trace_holonomy(f, gauge=gauge)
        both = half_trace_holonomy(f, flipset=in_E, gauge=gauge)
        quat_rows.append((w0, rev == w0 and all(x == w0 for x in shifts), flipped == -w0, gauged == w0, both == -w0))
    quat_ok = all(r[1] and r[2] and r[3] and r[4] for r in quat_rows) and any(r[0] != 0 for r in quat_rows)
    central_ok = all(quat_mul(quat_mul(gauge((0, 0, 0)), quat_neg(u)), quat_inv(gauge((1, 0, 0))))
                     == quat_neg(quat_mul(quat_mul(gauge((0, 0, 0)), u), quat_inv(gauge((1, 0, 0))))) for u in RATIONAL_SU2)
    H0p, Wp = plaquette_character_fixture(6)
    sgn = [(-1) ** k for k in range(7)]
    negWp = [[-x for x in row] for row in Wp]
    check('flip_operator_fixtures',
          gram_ok and second_moments_ok and mult_flip and cas_even and quat_ok and central_ok
          and diag_conj(sgn, Wp) == negWp and diag_conj(sgn, H0p) == H0p
          and rejected(lambda: require(diag_conj([1] * 7, Wp) == negWp, 'even-count plaquette is not flipped'),
                       'even_count_plaquette_claimed_flipped'),
          one_link='j<=1/2 compression of L^2(SU(2)), basis (1,U_11,U_12,U_21,U_22), Gram diag(1,1/2,1/2,1/2,1/2); centre grading diag(1,-1,-1,-1,-1) anticommutes with multiplication by each U_ab and commutes with the Casimir 3/4',
          one_plaquette='gauge-invariant character basis chi_j(U_P), j<=3; U_E=diag((-1)^{2j}) for odd |f cap E|: U W U=-W, U H_0 U=H_0',
          rational_su2_faces_checked=len(quat_rows),
          label='finite fixtures (exact algebra audits), not the infinite-volume statement')

    # -------------------- nonzero selected triple: positive demonstration --------------------
    g_sel = selected_at[ORIGIN][0]
    basis_words = [[], [WILSON], [g_sel]]
    basis_energy = [0, E24, E24]

    def compressed(tau, kap):
        return [[basis_energy[j] * expect(wi + wj) - tau / V['phi_den'] * expect(wi + [WILSON] + wj) - kap * expect(wi + [g_sel] + wj)
                 for j, wj in enumerate(basis_words)] for wi in basis_words]
    u_kappa = [1, (-1) ** flip_count(WILSON, in_E), (-1) ** flip_count(g_sel, in_E)]
    kappa_cases = [(tau_cap, Q(1, 10)), (Q(-1, 3), Q(2, 7)), (tau_cap, Q(0))]
    kappa_maps = [diag_conj(u_kappa, compressed(t0, k0)) == compressed(-t0, -k0) for t0, k0 in kappa_cases]
    kappa_breaks = [diag_conj(u_kappa, compressed(t0, k0)) != compressed(-t0, k0) for t0, k0 in kappa_cases if k0 != 0]
    def validate_kappa_map(target):
        require(diag_conj(u_kappa, compressed(tau_cap, Q(1, 10))) == target, 'U_E does not map H(tau,kappa) to the claimed operator')
        return True
    g_sel_E_link = [l for l in face_links_ordered(g_sel) if in_E(l)][0]
    check('flip_nonzero_kappa_positive_demonstration',
          all(kappa_maps) and all(kappa_breaks) and u_kappa == [1, -1, -1] and selected_ok
          and diag_conj(u_kappa, compressed(tau_cap, Q(0))) == compressed(-tau_cap, Q(0))
          and validate_kappa_map(compressed(-tau_cap, -Q(1, 10)))
          and rejected(lambda: validate_kappa_map(compressed(-tau_cap, Q(1, 10))), 'selected_coefficient_claimed_invariant')
          and rejected(lambda: validate_odd([g_sel], make_in_E(V['flip_spec'], removed=frozenset([g_sel_E_link])), 'selected face'),
                       'selected_face_treated_as_E_even'),
          fixture='exact compression of H=H_0-(tau/3)W_f-kappa W_g onto span{Omega_0, W Omega_0, W_g Omega_0}, f=W omitted, g a selected xy face of factor 0 (fixture convention for the selected coefficient)',
          selected_face=[list(g_sel[0]), 'xy'], cases=[[s(t0), s(k0)] for t0, k0 in kappa_cases],
          conclusion='U_E H(tau,kappa) U_E^* = H(-tau,-kappa); for kappa!=0 it is not H(-tau,kappa); every selected face of every probed factor meets E oddly',
          label='finite algebra fixture; nonzero selected triples are outside the AW1 model')

    def derive_tau_antisymmetry_from_UE(kappa):
        require(all(k == 0 for k in kappa), 'U_E maps kappa to -kappa: no tau-antisymmetry follows from U_E at a nonzero triple')
        return True
    check('flip_breaks_at_nonzero_kappa',
          derive_tau_antisymmetry_from_UE(V['triple']) and all(kappa_breaks)
          and rejected(lambda: derive_tau_antisymmetry_from_UE([Q(0), Q(1, 100), Q(0)]), 'tau_antisymmetry_claimed_at_nonzero_triple'),
          statement='the identity is U_E H_N(tau,kappa) U_E^* = H_N(-tau,-kappa); tau-antisymmetry via U_E only at kappa=0')

    # Remark (post-freeze observation, not a control and not claimed): a modified cochain.
    def in_E2(l):
        p, d = l
        return d == 0 and p[0] % 4 in (0, 1, 2) and p[1] % 4 in (1, 2)

    def in_Estar(l):
        return in_E(l) != in_E2(l)
    estar_ok = all((flip_count(g, in_Estar) % 2 == 1) != is_selected(g) for g in plaqs2)
    e2_cobound = all((flip_count(g, in_E2) % 2 == 1) == is_selected(g) for g in plaqs2)
    check('remark_selected_even_flip_set',
          estar_ok and e2_cobound and any(is_selected(g) for g in plaqs2),
          E2='{(p,x): p_x mod 4 in {0,1,2}, p_y mod 4 in {1,2}} has mod-2 coboundary equal to the selected-face indicator',
          Estar='E xor E2 meets every omitted plaquette oddly and every selected plaquette evenly (box N=2 enumeration)',
          status='post-freeze forward observation recorded for review; NOT claimed; nonzero selected triples are outside AW1',
          consequence_if_reviewed='U_{E*} H(tau,kappa) U_{E*}^* = H(-tau,kappa) would give tau-antisymmetry of omega(W) at every selected triple')

    # -------------------- flip: covariance, AQ passage, no third-order claim --------------------
    def pointwise_aq_antisymmetry(common_subsequence):
        require(common_subsequence, 'AQ1 chosen states at +tau and -tau use tau-dependent subsequences; pointwise only along a common one')
        return True
    check('flip_covariance_and_aq_passage',
          pointwise_aq_antisymmetry(True)
          and rejected(lambda: pointwise_aq_antisymmetry(False), 'pointwise_AQ1_antisymmetry_without_common_subsequence'),
          finite_volume='unique grounds (AM2, both signs): psi_{N,-tau}=U_E psi_{N,tau}; e^{-C(-tau)}=U_E e^{-C(tau)} U_E^*; cutoff projections are centre-even',
          consequences='omega_{N,-tau}(W)=-omega_{N,tau}(W), omega_{N,-tau}(W^2)=omega_{N,tau}(W^2), C_N and c_N even in tau',
          aq='S(-tau)=S(tau)o alpha_E for the whole set of subsequential limits; alpha_E intertwines the Nachtergaele-Sims dynamics; pointwise only along a common subsequence')

    # -------------------- first-order coefficient --------------------
    def L0_face(tau):
        """Per-face coefficient of c^(1)=L_0=H_0^{-1} P V Omega_0 (AV1/AM2 creation convention, psi=e^{-C}Omega_0)."""
        return -tau * coef_norm

    def omega1(tau, F, observable=WILSON, convention=-2):
        return sum((convention * L0_face(tau) * expect([observable, f]) for f in F), Q(0))
    om = {sg: omega1(tv, inside_faces) for sg, tv in taus.items()}
    om_box = {sg: omega1(tv, faces2) for sg, tv in taus.items()}
    per_face_inside = {f: -2 * L0_face(tau_cap) * expect([WILSON, f]) for f in inside_faces}
    per_face_anchor0 = {f: -2 * L0_face(tau_cap) * expect([WILSON, f]) for f in anchor0}
    display_sign = omega1(tau_cap, inside_faces, convention=2)
    h01 = -Q(1, V['phi_den']) * sum((expect([WILSON, f]) for f in faces2), Q(0))       # <W Omega_0, V_1 Omega_0>, normalized
    h11 = E24 * expect([WILSON, WILSON]) - Q(1, V['phi_den']) * sum((expect([WILSON, f, WILSON]) for f in faces2), Q(0))
    ritz_eps = -h01 / h11                                                               # per unit tau
    ritz_mean = 2 * ritz_eps * expect([WILSON, WILSON])
    candidate = Q(1, V['candidate_den'])

    def validate_first_order(value, tau):
        require(value == tau * candidate, 'first-order coefficient differs from the derived tau/%d' % V['candidate_den'])
        require(value == omega1(tau, faces2), 'first-order coefficient differs from the box face sum')
        return True
    check('wilson_mean_first_order_coefficient',
          validate_first_order(om['+'], tau_cap) and validate_first_order(om['-'], -tau_cap) and om_box == om
          and ritz_mean == candidate and h11 == E24 * V['ref_W2'] and m1 == candidate
          and rejected(lambda: validate_first_order(tau_cap / 72, tau_cap), 'tau_over_72')
          and rejected(lambda: validate_first_order(tau_cap / 288, tau_cap), 'tau_over_288')
          and rejected(lambda: validate_first_order(display_sign, tau_cap), 'plus_two_L0_convention_gives_minus_tau_over_144'),
          omega_first_order_plus=s(om['+']), omega_first_order_minus=s(om['-']), per_face_coefficient_of_L0='-tau/72',
          formula='omega_tau(W)=-2<W Omega_0, L_0>+O(tau^2)=2<W Omega_0, psi^(1)>+O(tau^2), psi^(1)=-L_0 the first-order ground-vector correction',
          contract_display_note='the contract writes 2<W Omega_0,c^(1)>; this holds with c^(1) read as the first-order vector correction psi^(1)=-L_0. With AV1\'s creation c^(1)=L_0 the literal display gives %s (rejected); both readings give +tau/144 once the convention is fixed' % s(display_sign),
          rayleigh_ritz_sign_rederivation={'h01_per_tau': s(h01), 'h11': s(h11), 'eps_star_per_tau': s(ritz_eps), 'mean_per_tau': s(ritz_mean)},
          units={'normalized': '(1/3)/24', 'alpha': '(1/3)/8/3', 'per_face_coefficient': s(coef_norm)})
    check('wrong_face_control',
          sum(1 for v in per_face_inside.values() if v != 0) == 1 and per_face_inside[WILSON] == tau_cap * candidate
          and all(expect([WILSON, f]) == 0 for f in meet_faces if f != WILSON)
          and rejected(lambda: validate_first_order(len(inside_faces) * tau_cap * candidate, tau_cap), 'all_ten_inside_faces_counted'),
          faces_inside_R=len(inside_faces), nonzero_contributions=1,
          per_face_inside_R=sorted([[list(f[0]), 'xyz'[f[1][0]] + 'xyz'[f[1][1]], s(v)] for f, v in per_face_inside.items()]))
    check('wilson_face_separated',
          len(anchor0) == V['classes_cand'] and len(others0) == V['others_cand'] and WILSON in anchor0
          and per_face_anchor0[WILSON] == tau_cap * candidate and all(per_face_anchor0[f] == 0 for f in others0)
          and all(expect([WILSON, WILSON, f]) == 0 for f in others0) and expect([WILSON] * 3) == 0
          and rejected(lambda: validate_first_order(sum((tau_cap * candidate for _ in anchor0), Q(0)), tau_cap), 'all_21_classes_merged')
          and rejected(lambda: validate_first_order(sum((per_face_anchor0[f] for f in others0), Q(0)), tau_cap), 'W_excluded_from_omitted_set'),
          wilson_class='xz r=0 s=0 anchored at factor 0', other_classes_at_anchor0=len(others0),
          f_equal_W={'E[W W_f]': s(expect([WILSON, WILSON])), 'E[W^2 W_f]': s(expect([WILSON] * 3))},
          f_not_W={'E[W W_f]': '0 for all 20', 'E[W^2 W_f]': '0 for all 20'})
    plane_rows = []
    for f0 in anchor0:
        plane_rows.append((f0, omega1(tau_cap, faces2, observable=f0)))
    sel_obs = omega1(tau_cap, faces2, observable=g_sel)
    orient_names = sorted({'xyz'[f0[1][0]] + 'xyz'[f0[1][1]] for f0, _ in plane_rows})
    check('orientation_invariance',
          all(v == tau_cap * candidate for _, v in plane_rows) and orient_names == ['xy', 'xz', 'yz'] and sel_obs == 0
          and all(r[1] for r in quat_rows)
          and rejected(lambda: validate_first_order(sel_obs, tau_cap), 'selected_face_observable_given_omitted_coefficient')
          and rejected(lambda: require(all(half_trace_holonomy(f, reverse=True) == -half_trace_holonomy(f) for f in qfaces),
                                       'reversal does not change the sign of a face trace'), 'orientation_reversal_claimed_to_flip'),
          traversal='(1/2)Tr is invariant under reversal (Tr U^{-1}=Tr U in SU(2)) and cyclic base-point shifts: exact rational-quaternion holonomies',
          planes='every omitted class at anchor 0 (xy, xz, yz) as observable has first-order mean +tau/144',
          selected_face_observable_first_order=s(sel_obs))

    # -------------------- sign-convention fixture (finite graph) --------------------
    series = {}
    for kmax in (4, 5, 6):
        series[kmax] = rs_mean_series(kmax, 4, V['phi_den'])
    ser = series[6][0]
    stable = all(series[k][0] == ser and series[k][1] == series[6][1] for k in (4, 5))
    brackets = {sg: two_level_mean_bracket(tv, V['phi_den']) for sg, tv in taus.items()}

    def validate_fixture_sign(first_order):
        require(first_order == ser[1], 'first-order sign convention contradicts the one-plaquette fixture')
        return True
    fixture_labels = {'model_id': 'FG(one_plaquette, character basis, single I1.5 face -(tau/3)W)', 'model_is_finite_graph': True,
                      'transfers_to_aq': False}
    check('sign_convention_fixture',
          stable and ser[1] == candidate and ser[2] == 0 and ser[0] == 0 and validate_fixture_sign(candidate)
          and 0 < brackets['+'][0] <= brackets['+'][1] and brackets['-'][0] <= brackets['-'][1] < 0
          and brackets['+'][0] == -brackets['-'][1]
          and rejected(lambda: validate_fixture_sign(display_sign / tau_cap), 'contract_display_with_L0_sign'),
          rs_series_coefficients=[s(x) for x in ser], rs_energy_coefficients=[s(x) for x in series[6][1]],
          truncation_stable_kmax=[4, 5, 6],
          two_level_mean_bracket={sg: [s(b[0]), s(b[1])] for sg, b in brackets.items()},
          two_level_mean_preview={sg: dec(b[0]) for sg, b in brackets.items()}, **fixture_labels)

    # -------------------- K_2 at both tiers --------------------
    K = {sg: k2_exact(tv, V, A1, counts) for sg, tv in taus.items()}
    KC = {sg: k2_crude(tv, V, A1) for sg, tv in taus.items()}
    K_plus = K['+']['K2']
    D_of = lambda e: 2 * e * (1 + e) / (1 + e * e)
    variants = {'sharper_remainder_288': k2_exact(tau_cap, V, A1, counts, remainder='sharper'),
                'conservative_overlap_4': k2_exact(tau_cap, V, A1, counts, overlap=Q(V['conservative_factor'])),
                'unpinned_t_bounds': k2_exact(tau_cap, V, A1, counts, pinned=False)}
    overlap_mult = 2 * norm_wf * 1       # 2 Re x ||W Omega_R|| x one contributing support (I=R)
    check('k2_exact_tier',
          K['+']['K2'] == K['-']['K2'] and D_of(K['+']['eps']) == A1['D_ii'] and overlap_mult == 1
          and K['+']['T'] == K['+']['t1'] + K['+']['rho'] and K_plus <= variants['unpinned_t_bounds']['K2']
          and variants['sharper_remainder_288']['K2'] < K_plus < variants['conservative_overlap_4']['K2'],
          K2_plus=s(K_plus), K2_plus_preview=dec(K_plus), K2_plus_ceil_1e40=s(ceil_grid(K_plus)),
          reproduces_AV1_D_ii=True, record=k2_record(K['+']),
          first_order_anchored_norm={'triangle_over_abs_tau': s(counts['faces_per_factor'] * V['per_face_norm']),
                                     'grouped_upper_over_abs_tau': s(V['per_face_norm'] * sum((sqrt_up(nm) for nm in counts['multiplicities']), Q(0))),
                                     'pinned_to': '15 owner sets per factor with multiplicities ' + str(counts['multiplicities']) + ' (sum 49)',
                                     'headline_uses': 'triangle bound 49|tau|/144 (AV1 tier-(ii) form)'})
    check('k2_crude_tier',
          KC['+']['K2'] == KC['-']['K2'] and KC['+']['K2'] > K_plus and KC['+']['T'] == A1['J0'] * A1['G_R_upper'],
          K2_crude=s(KC['+']['K2']), K2_crude_preview=dec(KC['+']['K2']), record=k2_record(KC['+']))

    def mixed_tiers():
        x = K['+']
        terms = list(x['terms'])
        terms[2] = ('straddling', 'crude', KC['+']['T'] * KC['+']['T'], 2)
        return assemble_k2('exact', tau_cap, terms)

    def refined_without_self_consistency():
        x = k2_exact(tau_cap, V, A1, counts, t_override=K['+']['t1'])
        require(x['T'] == x['t1'] + x['rho'], 'refined t used without the self-consistent inequality t<=t_1/(1-352J)')
        return x
    check('tier_mixing_rejected',
          all(lab == 'exact' for _, lab, _, _ in K['+']['terms']) and all(lab == 'crude' for _, lab, _, _ in KC['+']['terms'])
          and rejected(mixed_tiers, 'exact_terms_with_crude_straddling')
          and rejected(refined_without_self_consistency, 't_equals_t1_without_remainder')
          and rejected(lambda: validate_rule_choice(aw2_rule(K_plus, V), KC['+']['K2'], V, 'crude'), 'rule_fed_crude_constant'),
          exact_labels=sorted(n for n, _, _, _ in K['+']['terms']))

    def itemized_ok(terms):
        return assemble_k2('exact', tau_cap, terms)

    def zero_term():
        terms = list(K['+']['terms'])
        terms[3] = ('density', 'exact', Q(0), 2)
        return itemized_ok(terms)

    def missing_term():
        return itemized_ok([t for t in K['+']['terms'] if t[0] != 'two_creation'])
    check('second_order_remainder_itemized',
          itemized_ok(K['+']['terms'])[1] == K_plus and rejected(zero_term, 'density_term_set_to_zero')
          and rejected(missing_term, 'two_creation_term_missing'),
          pinned={'am2_remainder': 'rho=||c-c^(1)||_a<=352 J t, J=28|tau| (four incoming stars), t<=t_1/(1-352J), t_1=49|tau|/144 (49 faces per factor)',
                  'two_creation': '(sum_{I ni 0, e_z notin I}||c_I||)(sum_{J ni e_z, 0 notin J}||c_J||) <= (33|tau|/144+rho)^2; 33=49-16',
                  'straddling': 't x (6|tau|/144+rho): only supports strictly containing R pair with an outside excitation of amplitude <=t; 6=16-10; the 66 straddling faces meeting R once contribute exactly 0',
                  'density': '|<delta,W delta>|/||psi||^2 <= e^2 <= eps^2, eps=2t+t^2 (Tr_out|delta><delta|)',
                  'normalization_order': '(|tau|/144) eps^2: third order in tau',
                  'overlap_multiplier': '1 = 2 Re x ||W Omega_R||=1/2 x one contributing support (I=R)'})

    # -------------------- overlap structure (qubit creation fixture) --------------------
    creations = [((0, 1), Q(1, 50)), ((0,), Q(1, 60)), ((1,), Q(1, 70)), ((0, 2), Q(1, 9)), ((1, 3), Q(1, 10)),
                 ((0, 1, 2), Q(1, 11)), ((2,), Q(-1, 12)), ((3,), Q(1, 13)), ((2, 3), Q(1, 14))]
    Rq = {0, 1}
    psi = product_state(4, creations)
    psi_out = product_state(4, [cr for cr in creations if not set(cr[0]) & Rq])
    n2 = inner(psi_out, psi_out)
    delta = vadd(psi, psi_out, -1)
    e2 = inner(delta, delta) / n2
    Xpo = apply_X(psi_out, 0, 1)
    overlaps = {cr[0]: inner(Xpo, c_hat(psi_out, cr[0], cr[1])) / n2 for cr in creations if set(cr[0]) & Rq}
    omega_X = inner(psi, apply_X(psi, 0, 1)) / inner(psi, psi)
    t_fix = max(sum((abs(cf) for I, cf in creations if u in I), Q(0)) for u in range(4))
    amp2 = {u: sum((v * v for bits, v in psi_out.items() if bits[u] == 1), Q(0)) / n2 for u in (2, 3)}
    A0q = sum((abs(cf) for I, cf in creations if 0 in I and 1 not in I), Q(0))
    A1q = sum((abs(cf) for I, cf in creations if 1 in I and 0 not in I), Q(0))
    sup_q = sum((abs(cf) for I, cf in creations if Rq < set(I)), Q(0))
    main_q = -2 * Q(1, 50)
    bound_q = 2 * 1 * t_fix * sup_q + 2 * 1 * A0q * A1q + e2
    lhs_q = abs(omega_X * (1 + e2) - main_q)

    def validate_overlap_multiplier(mult, label):
        if mult == overlap_mult:
            return True
        require(mult == V['conservative_factor'] and label == 'conservative', 'overlap multiplier %s without the conservative label' % s(mult))
        return True
    check('wilson_overlap_single_component',
          norm_wf == V['wilson_overlap_norm'] and overlap_mult == 1
          and all(overlaps[I] == 0 for I in ((0,), (1,), (0, 2), (1, 3))) and overlaps[(0, 1)] == Q(1, 50)
          and overlaps[(0, 1, 2)] != 0 and all(a2 <= t_fix * t_fix for a2 in amp2.values()) and lhs_q <= bound_q
          and all(any(owner(l[0]) == xr for l in w_links) for xr in sorted(COVER_R)) and trivial_multiplicity(1) == 0
          and validate_overlap_multiplier(Q(V['conservative_factor']), 'conservative')
          and rejected(lambda: validate_overlap_multiplier(Q(V['conservative_factor']), 'unlabelled'), 'factor_4_unlabelled')
          and rejected(lambda: validate_overlap_multiplier(Q(1, 2), 'unlabelled'), 'multiplier_below_single_component'),
          norm_W_Omega_R=s(norm_wf), partial_vacuum_contractions='<Omega_x|W Omega_R>=0 for x in R: each W link owned by x carries one spin-1/2 factor',
          fixture={'omega_X': s(omega_X), 'main_term': s(main_q), 'lhs': s(lhs_q), 'bound': s(bound_q),
                   'overlaps_over_n2': {','.join(map(str, I)): s(v) for I, v in sorted(overlaps.items())},
                   'label': 'qubit creation fixture (finite algebra audit)'},
          conservative_variant_K2=s(variants['conservative_overlap_4']['K2']))

    # -------------------- omega(W^2): explicit second-order constant --------------------
    normA = exact_sqrt(expect([WILSON] * 4) - 2 * V['ref_W2'] * expect([WILSON] * 2) + V['ref_W2'] ** 2)
    opA = 1 - V['ref_W2']
    x = K['+']
    w2_terms = {'direct_remainder': 2 * normA * 2 * x['rho'],
                'straddling': 2 * normA * x['T'] * (counts['straddling'] * x['a'] + 2 * x['rho']),
                'two_creation': 2 * normA * x['A0'] * x['Az'], 'density': opA * x['eps'] ** 2}
    K_W2 = sum(w2_terms.values(), Q(0)) / tau_cap ** 2
    check('omega_W2_second_order_bound',
          normA == Q(1, 4) and opA == Q(3, 4) and fo_box['omega_W2_state'] == 0 and all(v > 0 for v in w2_terms.values()),
          K_W2=s(K_W2), K_W2_preview=dec(K_W2), terms={k: s(v) for k, v in w2_terms.items()},
          statement='|omega(W^2)-1/4|<=K_W2 tau^2 uniformly in N, cutoff and every AQ subsequential limit (exact tier); first-order coefficient 0; the free value 1/4 lies inside, no shift is resolved',
          C_s_constant='not bounded uniformly in N (explicitly unbounded)')

    # -------------------- feasibility and the AW2 rule --------------------
    lhs_cap = K_plus * tau_cap
    feasible = lhs_cap <= V['target']
    margin = 1 / (V['margin_den'] * K_plus * tau_cap)
    tau_aw2 = aw2_rule(K_plus, V)
    tau_crude_info = aw2_rule(KC['+']['K2'], V)
    check('aw2_coupling_rule_prefrozen',
          feasible and margin >= V['margin_min'] and validate_rule_choice(tau_aw2, K_plus, V, 'exact')
          and tau_aw2 == Q(1, 10 ** V['grid_start'])
          and rejected(lambda: validate_rule_choice(tau_aw2 / 10, K_plus, V, 'exact'), 'not_the_largest_grid_value')
          and rejected(lambda: validate_rule_choice(3 * tau_aw2, K_plus, V, 'exact'), 'off_grid_value')
          and rejected(lambda: validate_rule_choice(tau_crude_info, KC['+']['K2'], V, 'crude'), 'crude_constant'),
          K2_plus_tau_at_cap=s(lhs_cap), K2_plus_tau_preview=dec(lhs_cap), target=s(V['target']), feasible=feasible,
          sign_margin=s(margin), sign_margin_preview=dec(margin), tau_AW2=s(tau_aw2),
          crude_tier_rule_value_information_only=s(tau_crude_info),
          no_enclosure_admitted='the feasibility Boolean is not an enclosure of omega(W); AW2 instantiates it')
    check('av1_compatibility',
          A1['D_ii'] >= tau_cap * candidate and A1['D_ii'] >= tau_cap * candidate + K_plus * tau_cap ** 2
          and K['+']['eps'] == 2 * K['+']['T'] + K['+']['T'] ** 2,
          D_ii=s(A1['D_ii']), first_order=s(tau_cap * candidate), ratio_preview=dec(A1['D_ii'] / (tau_cap * candidate)))

    # -------------------- inherited controls re-read for AW1 --------------------
    anchors_R = sorted({sub(u, d) for u in COVER_R for d in S_STAR})
    stars_per_site = len({sub(ORIGIN, d) for d in S_STAR})
    phi_norm_per_tau = Q(len(classes), V['phi_den'])
    J_derived = stars_per_site * phi_norm_per_tau

    def validate_J(j_per_tau):
        require(j_per_tau == A1['J_coefficient'], 'per-site interaction sum differs from the four incoming stars (28|tau|)')
        return True
    check('missing_incoming_stars',
          len(anchors_R) == 7 and stars_per_site == 4 and phi_norm_per_tau == 7 and validate_J(J_derived)
          and rejected(lambda: validate_J(phi_norm_per_tau), 'one_outgoing_star_J_7tau')
          and rejected(lambda: validate_J(2 * phi_norm_per_tau), 'orthant_two_anchor_count'),
          incident_anchors_R_minus_S=[list(a) for a in anchors_R], J_per_tau=s(J_derived),
          role_in_K2='rho<=352 J t with J=28|tau|; a one-star J would understate the dominant term fourfold')
    cover_links = sorted({l for b in COVER_R for l in owned_links(b)})
    endpoints = {}
    for b in COVER_R:
        endpoints[b] = {l[0] for l in owned_links(b)} | {add(l[0], UNIT[l[1]]) for l in owned_links(b)}

    def validate_cover(links):
        require(len(links) == 48, 'the complete cover R={0,e_z} has 48 links')
        return True
    check('full_original_wilson_cover',
          validate_cover(cover_links) and len(endpoints[ORIGIN] | endpoints[EZ]) == 36
          and len(endpoints[ORIGIN]) == len(endpoints[EZ]) == 22 and len(endpoints[ORIGIN] & endpoints[EZ]) == 8
          and w_owners == [ORIGIN, ORIGIN, EZ, ORIGIN] and set(w_links) <= set(cover_links)
          and rejected(lambda: validate_cover(list(w_links)), 'four_drawn_links_as_cover'),
          links=len(cover_links), endpoints=36, per_factor=22, shared=8, wilson_owners='0,0,e_z,0')
    alpha_, hbar_, tE = Q(5), Q(7), Q(3, 2)
    s_clock = alpha_ * tE / hbar_
    u_clock = s_clock / A1['delta_den']
    mixed1 = Q(1, V['phi_den'] * A1['delta_den']) / V['energy_norm']
    mixed2 = Q(1, V['phi_den']) / V['energy_alpha']
    check('wrong_delta_alpha_hbar_clock',
          coef_norm == coef_alpha and V['energy_norm'] == A1['delta_den'] * V['energy_alpha']
          and V['free_exponent'] * s_clock == V['energy_norm'] * u_clock and V['free_exponent'] == V['energy_alpha']
          and rejected(lambda: validate_first_order(2 * mixed1 * V['ref_W2'] * tau_cap, tau_cap), 'alpha_V_with_normalized_energy_tau_over_1152')
          and rejected(lambda: validate_first_order(2 * mixed2 * V['ref_W2'] * tau_cap, tau_cap), 'normalized_V_with_alpha_energy_tau_over_18')
          and rejected(lambda: require(V['energy_norm'] * s_clock == V['free_exponent'] * s_clock, 'exponent 24 with s'), 'eightfold_clock'),
          per_face_coefficient=s(coef_norm), free_correlation='C_0(s)=e^{-%ds}/%d, s=alpha t_E/hbar' % (V['free_exponent'], V['free_weight_den']),
          nonunit_fixture={'alpha': '5', 'hbar': '7', 't_E': '3/2', 's': s(s_clock), 'u': s(u_clock)})
    m_, d_ = Q(1, 4), Q(1, 100)
    check('vector_versus_scalar_centering',
          d_ ** 2 == Q(1, 10000) and -2 * m_ * d_ - d_ ** 2 == Q(-51, 10000) and m_ ** 2 == Q(1, 16)
          and fo_box['C_vector_centering'] == 0 and m1 != 0
          and rejected(lambda: require(d_ ** 2 == -2 * m_ * d_ - d_ ** 2, 'scalar subtraction as vector centering'), 'scalar_as_vector'),
          vector_residue=s(d_ ** 2), scalar_residue=s(-2 * m_ * d_ - d_ ** 2), uncentered_residue=s(m_ ** 2),
          aw1_note='C(s) is vector-centred; its first-order centring term -m_1<W Omega_0,Omega_0> vanishes by E[W]=0 although m_1=1/144')

    def zero_mean_at_first_order(first_order):
        require(first_order == 0, 'the uncentered mean has a nonzero first-order coefficient')
        return True
    check('first_order_mean_charged',
          m1 == candidate and fo_box['uncentered_mean_control'] == candidate
          and rejected(lambda: zero_mean_at_first_order(m1), 'zero_mean_assumed_at_first_order'),
          first_order_mean_per_tau=s(m1), charge_in_C='m^2=O(tau^2) enters C(s) at second order; bounded by D_ii^2 from AV1',
          m2_upper=s(A1['D_ii'] ** 2))
    small = tau_cap / 100
    K_small = k2_exact(small, V, A1, counts)
    ratio_first = omega1(tau_cap, faces2) / omega1(small, faces2)
    term_ratios = {n: v / w for (n, _, v, _), (_, _, w, _) in zip(K['+']['terms'], K_small['terms'])}
    orders = {n: o for n, _, _, o in K['+']['terms']}

    def exponent_ok(ratio, order):
        lo, hi = {1: (99, 101), 2: (9900, 10100), 3: (990000, 1010000)}[order]
        require(lo <= ratio <= hi, 'scaling ratio outside the declared order %d' % order)
        return True
    at4_ratio = exact_sqrt(Q(100))
    check('tau_scaling_exponent',
          ratio_first == 100 and all(exponent_ok(term_ratios[n], orders[n]) for n in term_ratios)
          and rejected(lambda: exponent_ok(term_ratios['am2_remainder'], 1), 'second_order_term_relabelled_first_order')
          and rejected(lambda: exponent_ok(at4_ratio, 1), 'square_root_relabelled_linear'),
          first_order_ratio=s(ratio_first), term_ratios={n: dec(r, 10) for n, r in term_ratios.items()},
          K2_tau_over_100=s(K_small['K2']), K2_tau_over_100_preview=dec(K_small['K2']))
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
                     ('model_id', fixture_labels['model_id']), ('state_provenance', 'finite_volume_N=2')):
        mutated = dict(packet_model)
        mutated[key] = val
        muts.append(rejected(lambda m=mutated: validate_model(m), 'relabel_' + key))
    check('changed_model_relabelled', validate_model(packet_model) and len(muts) == 5 and fixture_labels['transfers_to_aq'] is False,
          packet_model=packet_model, rejected=muts)

    def retained(result_pass, label):
        require(result_pass is False or label == 'exact', 'crude-tier sign feasibility would be claimed at the cap')
        return True
    crude_feasible = KC['+']['K2'] * tau_cap <= V['target']
    check('insufficient_verdict_retained',
          crude_feasible is False and retained(crude_feasible, 'crude')
          and rejected(lambda: retained(True, 'crude'), 'crude_tier_reported_feasible')
          and rejected(lambda: validate_model(dict(packet_model, tau=s(tau_crude_info))), 'crude_retuned_to_smaller_tau_under_cap_label'),
          crude_K2_tau_at_cap=s(KC['+']['K2'] * tau_cap), crude_K2_tau_preview=dec(KC['+']['K2'] * tau_cap),
          crude_decade_information_only=s(tau_crude_info), retained='crude tier fails 1/288 at the cap; kept as a limited-tier value')
    forbidden = ('mp' + 'math', 'num' + 'py', 'fl' + 'int', 'sym' + 'py', 'sci' + 'py')
    own = (BASE / 'check.py').read_text()
    imports = [ln for ln in own.splitlines() if ln.startswith('import ') or ln.startswith('from ')]
    check('exact_arithmetic_admission',
          not any(any(fb in ln for fb in forbidden) for ln in imports)
          and rejected(lambda: rat(1e-08), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('NaN'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator'),
          imports=imports, decimals='previews only, truncated from exact rationals')
    linear = K['+']['total']
    rss_sq = sum((v * v for _, _, v, _ in K['+']['terms']), Q(0))

    def validate_combination(value_sq, label):
        require(label == 'linear' and value_sq == linear * linear, 'itemized terms must add linearly (coherent worst case)')
        return True
    check('root_n_misuse',
          validate_combination(linear * linear, 'linear') and rss_sq < linear * linear
          and rejected(lambda: validate_combination(rss_sq, 'rss'), 'root_sum_of_squares')
          and rejected(lambda: validate_combination((linear / sqrt_up(len(faces2))) ** 2, 'sqrt_N'), 'divided_by_sqrt_N')
          and rejected(lambda: validate_combination((linear / 64) ** 2, 'div64'), 'divided_by_64'),
          linear_total=s(linear), rss_preview=dec(sqrt_up(rss_sq, 10 ** 30)))

    def signed_first_order(tau):
        return omega1(tau, faces2)

    def validate_sign_flip(fn):
        require(fn(tau_cap) == -fn(-tau_cap) and fn(tau_cap) > 0, 'first-order coefficient must flip sign with tau')
        return True
    check('sign_flip_tau',
          validate_sign_flip(signed_first_order) and brackets['+'][0] > 0 > brackets['-'][1]
          and rejected(lambda: validate_sign_flip(lambda t: abs(t) * candidate), 'sign_blind_abs_tau_formula'),
          first_order={'+': s(signed_first_order(tau_cap)), '-': s(signed_first_order(-tau_cap))},
          exact_value_statement='omega_{N,-tau}(W)=-omega_{N,tau}(W) for every box and cutoff by the flip lemma; the -tau K_2 is its image, not a second confirmation')

    def validate_effect_label(label):
        require(label == 'static_not_dynamic', 'a static equal-time mean is not a dynamical or mass-gap correction')
        return True
    check('static_not_dynamic_effect',
          validate_effect_label('static_not_dynamic') and 'static_not_dynamic' in V['sub_labels'] and fo_box['C_duhamel'] == 0
          and rejected(lambda: validate_effect_label('dynamical_correction'), 'dynamical_relabel')
          and rejected(lambda: validate_effect_label('mass_gap_correction'), 'mass_gap_relabel'),
          note='the only first-order Wilson effect is the equal-time mean; the first-order term of C(s) is zero')
    r_fix = lambda t: K_plus * t * abs(t)

    def claim_third_order(fn):
        exponent_ok(fn(tau_cap) / fn(small), 3)
        return True
    check('flip_no_third_order_claim',
          r_fix(-tau_cap) == -r_fix(tau_cap) and exponent_ok(r_fix(tau_cap) / r_fix(small), 2)
          and rejected(lambda: claim_third_order(r_fix), 'oddness_claimed_to_give_tau_cubed'),
          counterexample='r(tau)=K tau|tau| is odd and exactly second order',
          note='finite-volume analyticity plus oddness kills the tau^2 Taylor coefficient of omega_N(W) for each N, but no uniform O(tau^3) remainder is claimed; K_2 bounds absolute second-order terms')
    forward_list = ['AGENTS.md', CONTRACT_REL] + V['shared_premises'] + V['forward_additional']
    reverse_list = ['AGENTS.md', CONTRACT_REL] + V['shared_premises']
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    bad_patterns = ('research/round32/skeptic/triage.md', '/loop2-response.md', 'research/round32/advisor/deliberation-',
                    'research/round32/forward/aw1', 'research/round32/skeptic/aw1')

    def validate_reverse(lst):
        for item in lst:
            require(not any(bp in item for bp in bad_patterns), 'reverse premise isolation violated by ' + item)
        return True
    check('reverse_premise_isolation',
          sorted(inventory) == sorted(set(forward_list)) and validate_reverse(reverse_list) and c.get('reverse_premise_isolation') is True
          and all(any(bp in item for bp in bad_patterns) for item in V['forward_additional'])
          and rejected(lambda: validate_reverse(reverse_list + ['research/round32/skeptic/triage.md']), 'reverse_reads_triage')
          and rejected(lambda: validate_reverse(reverse_list + ['research/round32/forward/aw1/report.md']), 'reverse_reads_forward_aw1'),
          forward_inventory_files=len(inventory), reverse_premise_count=len(reverse_list),
          forward_additional_disclosed=V['forward_additional'])
    claim_flags = {'continuum_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False,
                   'scientific_priority_verified': False, 'first_order_parity_claim': True, 'flip_lemma_claim': True,
                   'third_order_remainder_claim': False, 'omega_W_enclosure_admitted': False, 'sign_of_omega_W_admitted': False,
                   'euclidean_node_certified': False}
    must_false = ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift', 'scientific_priority_verified',
                  'third_order_remainder_claim', 'omega_W_enclosure_admitted', 'sign_of_omega_W_admitted', 'euclidean_node_certified')

    def validate_flags(fl):
        for k in must_false:
            require(fl[k] is False, 'claim flag must be false: ' + k)
        return True
    check('no_priority_or_continuum_claim',
          validate_flags(claim_flags)
          and rejected(lambda: validate_flags(dict(claim_flags, continuum_claim=True)), 'continuum_claim_true')
          and rejected(lambda: validate_flags(dict(claim_flags, scientific_priority_verified=True)), 'priority_true')
          and rejected(lambda: validate_flags(dict(claim_flags, resolved_interaction_shift=True)), 'shift_resolved_true'),
          historical_or_occult_numeric_premise=False, flags=claim_flags)

    # -------------------- assemble packet --------------------
    xe, xc = K['+'], KC['+']

    def term_value(xx, name):
        return [v for n, _, v, _ in xx['terms'] if n == name][0]
    error_terms = {
        'am2_remainder': {'exact': s(term_value(xe, 'am2_remainder')), 'crude': s(term_value(xc, 'am2_remainder')),
                          'form': 'rho=||c-c^(1)||_a<=352 J t (AV1-gate form); sharper 288-form reported as a labelled variant'},
        'two_creation': {'exact': s(term_value(xe, 'two_creation')), 'crude': s(term_value(xc, 'two_creation'))},
        'straddling': {'exact': s(term_value(xe, 'straddling')), 'crude': s(term_value(xc, 'straddling')),
                       'meeting_R_once': 'exactly 0 (partial vacuum contraction of W Omega_R vanishes)'},
        'density': {'exact': s(term_value(xe, 'density')), 'crude': s(term_value(xc, 'density'))},
        'normalization_order': {'exact': s(term_value(xe, 'normalization_order')), 'crude': s(term_value(xc, 'normalization_order')),
                                'order_in_tau': 3},
        'overlap_multiplier': {'value': s(overlap_mult), 'conservative_variant': str(V['conservative_factor']) + ' (labelled conservative)',
                               'norm_W_Omega_R': s(norm_wf)},
        'arithmetic': 'not_applicable as a numeric cost: exact Fractions throughout; the face sums use triangle bounds (no square roots); K_2^+ is also given rounded up on the 10^-40 grid',
    }
    require(sorted(error_terms) == sorted(V['error_terms']), 'error terms differ from the preregistration')
    headline = {'first_order_coefficient': '+tau/' + str(V['candidate_den']), 'omega1_plus': s(om['+']), 'omega1_minus': s(om['-']),
                'K2_exact_plus': s(K_plus), 'K2_exact_preview': dec(K_plus), 'K2_exact_ceil_1e40': s(ceil_grid(K_plus)),
                'K2_crude': s(xc['K2']), 'K2_crude_preview': dec(xc['K2']),
                'K2_sharper_288_preview': dec(variants['sharper_remainder_288']['K2']),
                'K2_conservative_overlap_4_preview': dec(variants['conservative_overlap_4']['K2']),
                'K2_unpinned_preview': dec(variants['unpinned_t_bounds']['K2']),
                'K2_plus_tau_at_cap': s(lhs_cap), 'feasible_at_cap': feasible, 'sign_margin': s(margin),
                'sign_margin_preview': dec(margin), 'tau_AW2': s(tau_aw2), 'K_W2': s(K_W2), 'K_W2_preview': dec(K_W2)}
    packet = {
        'loop': 'AW1', 'direction': 'forward', 'human_author': 'Hruday N M (BUNZEEY)',
        'contribution_alias': 'HNM-AW1-F forward parity theorem, flip lemma, first-order Wilson mean and itemized K_2',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha,
        'inherited_tooling_named_not_imported': INHERITED_TOOLING,
        'model': packet_model, 'tau_values': {sg: s(tv) for sg, tv in taus.items()},
        'sub_labels': ['static_not_dynamic'],
        'headline': headline,
        'k2': {'exact': {sg: k2_record(K[sg]) for sg in taus}, 'crude': {sg: k2_record(KC[sg]) for sg in taus},
               'variants': {k1: k2_record(v1) for k1, v1 in variants.items()}, 'tau_over_100': k2_record(K_small)},
        'error_terms_itemized': error_terms,
        'parity_theorem': {'first_order_terms_box_N2': {k: s(v) for k, v in fo_box.items()},
                           'first_order_terms_bulk_82': {k: s(v) for k, v in fo_bulk.items()},
                           'moments': {str(n): s(routes[n][0]) for n in range(5)},
                           'omega_W2': 'first-order coefficient 0; |omega(W^2)-1/4|<=K_W2 tau^2 uniformly (exact tier)',
                           'C_s': 'first-order coefficient 0 in every box (state, vector-centring, Duhamel and energy terms); C_N(s)=e^{-3s}/4+O_N(tau^2); uniform constant explicitly unbounded',
                           'real_time': 'first-order coefficient of c_N(theta) is 0 for every real theta'},
        'flip_lemma': {'flip_set': V['flip_set_text'], 'parity_classes_odd': 24, 'faces_per_factor_odd': V['faces_per_factor_cand'],
                       'identity': 'U_E H_N(tau,kappa) U_E^* = H_N(-tau,-kappa), including on-site cutoff compressions',
                       'kappa_zero': 'omega(W) odd, omega(W^2), C_N and c_N even in tau; AQ: whole-set statement',
                       'third_order': 'not claimed'},
        'enumeration': {'faces_per_factor': counts['faces_per_factor'], 'owner_sets': counts['owner_sets_per_factor'],
                        'multiplicities': counts['multiplicities'], 'meet_R': counts['meet_R'], 'inside_R': counts['inside_R'],
                        'both_R': counts['both_R'], 'strictly_containing_R': counts['strictly_containing_R'],
                        'straddling': counts['straddling'], 'straddling_split_outside_sites': [counts['straddling_one_outside'], counts['straddling_two_outside']],
                        'zero_not_ez': counts['zero_not_ez'], 'ez_not_zero': counts['ez_not_zero'],
                        'anchor0_classes': len(anchor0), 'anchor0_others': len(others0)},
        'finite_fixture_labels': fixture_labels,
        'proposed_forward_verdict': 'accepted_within_scope (forward route only; the gate also needs the reverse route and skeptical review)',
        'uniqueness_claimed': False, 'whole_sequence_convergence_claimed': False, 'rate_in_N_claimed': False,
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
        validate_flags(pk)
        require(sorted(inv) == sorted(set(forward_list)), 'premise snapshot inventory incomplete')
        kp = k2_exact(tau_cap, V, A1, counts)['K2']
        require(rat(pk['headline']['K2_exact_plus']) == kp, 'headline K_2 differs from recomputation')
        require(rat(pk['headline']['tau_AW2']) == aw2_rule(kp, V), 'tau_AW2 differs from the frozen rule')
        require(pk['headline']['feasible_at_cap'] is (kp * tau_cap <= V['target']), 'feasibility Boolean differs')
        require(rat(pk['headline']['omega1_plus']) == omega1(tau_cap, faces2), 'first-order coefficient differs from recomputation')
        return True

    base_packet = dict(packet)
    base_packet['checks'] = [dict(ch) for ch in CHECKS]
    base_packet['packet_sha256'] = packet_hash(base_packet)

    def tampered(edit, inv=None):
        pk = json.loads(json.dumps(base_packet))
        edit(pk)
        pk['packet_sha256'] = packet_hash(pk)
        return validate_packet(pk, inventory if inv is None else inv)

    def flip_control(pk):
        for ch in pk['checks']:
            if ch['id'] == 'flip_set_odd_intersection':
                ch['passed'] = False
    inv_missing = dict(inventory)
    inv_missing.pop('research/round32/methods/paired-physics-research/SKILL.md')
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(lambda: tampered(flip_control), 'control_boolean_flipped_hash_rebound')
          and rejected(lambda: tampered(lambda pk: None, inv_missing), 'snapshot_removed_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk['headline'].update(K2_exact_plus=s(K_plus / 2))), 'K2_halved_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk['headline'].update(tau_AW2=s(tau_aw2 / 10))), 'tau_AW2_changed_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk['headline'].update(omega1_plus=s(tau_cap / 72))), 'first_order_doubled_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk.update(third_order_remainder_claim=True)), 'third_order_flag_hash_rebound'))

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in V['controls'] if cid not in ids]
    require(not missing, 'contract controls without a check: ' + ','.join(missing))
    no_mutation = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch['mutations_rejected']]
    require(not no_mutation, 'contract controls without a damaging mutation: ' + ','.join(no_mutation))
    require(not PENDING_MUTATIONS, 'mutations evaluated outside a check')
    packet['checks'] = CHECKS
    packet['contract_controls_covered'] = sorted(V['controls'])
    packet['check_count'] = len(CHECKS)
    return packet


def main():
    ap = argparse.ArgumentParser(description='AW1 forward exact checker')
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
    manifest = {'loop': 'AW1', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AW1', 'direction': 'forward', 'checks': len(result['checks']),
                      'K2_exact_preview': result['headline']['K2_exact_preview'], 'K2_crude_preview': result['headline']['K2_crude_preview'],
                      'tau_AW2': result['headline']['tau_AW2'], 'first_order': result['headline']['first_order_coefficient']},
                     sort_keys=True))


if __name__ == '__main__':
    main()
