#!/usr/bin/env python3
"""AV2 forward producer: exact checks for the Hruday window-kernel certificate.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production.

Standard library only (fractions, hashlib, json, argparse, re, math.isqrt via
calculator.py). Every admission Boolean is decided in exact Fraction arithmetic;
decimal strings are outward-rounded previews. Conditions raise AdmissionError
explicitly (never `assert`), so every check stays active under `python -O`.
Every number in results.json is a string.

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction as Q
from math import comb
from pathlib import Path

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))
import calculator as calc  # noqa: E402  (same producer closure; no bytecode written)

CONTRACT_REL = 'research/round32/contracts/av2.json'
CONTRACT_SHA256 = '686458cab7a4e6e65b63f0c6418d51496f66f1aada4897115ff14e8bbfad5687'
GATE_REL = 'research/round32/advisor/av1-gate.json'
AT4_FWD_REL = 'research/round31/forward/at4/report.md'


class AdmissionError(Exception):
    """An admission condition failed or a damaging mutation was accepted."""


def require(condition, message):
    if not condition:
        raise AdmissionError(message)


CHECKS = []
PENDING = []   # mutation labels rejected while the next check's condition is evaluated


def check(identity, condition, **details):
    require(condition, 'failed check ' + identity)
    require(all(c['id'] != identity for c in CHECKS), 'duplicate check id ' + identity)
    entry = {'id': identity, 'passed': True}
    entry.update(details)
    if PENDING:
        entry['rejected_mutations'] = list(PENDING)
        PENDING.clear()
    CHECKS.append(entry)


def rejected(mutation, label):
    """Run a damaging mutation; it must raise AdmissionError."""
    try:
        mutation()
    except AdmissionError:
        PENDING.append(label)
        return label
    raise AdmissionError('damaging mutation accepted: ' + label)


def calc_rejects(kwargs, label, errors=(ValueError,)):
    """A calculator call outside the proved domain must raise an input error."""
    try:
        calc.certify(**kwargs)
    except errors:
        PENDING.append(label)
        return label
    raise AdmissionError('calculator accepted an invalid case: ' + label)


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


def s_(q):
    return calc.textq(q)


def dec(q, digits=12, mode='up'):
    """Scientific decimal of an exact rational rounded outward (display only)."""
    q = Q(q)
    if q == 0:
        return '0'
    neg = q < 0
    a = abs(q)
    e = 0
    while a >= Q(10) ** (e + 1):
        e += 1
    while a < Q(10) ** e:
        e -= 1
    scaled = a / Q(10) ** (e - digits + 1)
    m = scaled.numerator // scaled.denominator
    magnitude_up = (mode == 'up') != neg
    if magnitude_up and m * scaled.denominator != scaled.numerator:
        m += 1
    if m >= 10 ** digits:
        m //= 10
        e += 1
    t = str(m)
    return ('-' if neg else '') + t[0] + '.' + t[1:] + 'e' + str(e)


def fixed(q, places, mode):
    """Fixed-point decimal rounded down or up (display only)."""
    q = Q(q) * 10 ** places
    n = q.numerator // q.denominator
    if mode == 'up' and n * q.denominator != q.numerator:
        n += 1
    sign = '-' if n < 0 else ''
    n = abs(n)
    t = str(n).rjust(places + 1, '0')
    return sign + t[:-places] + '.' + t[-places:]


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def match(pattern, text, label):
    m = re.search(pattern, text)
    require(m is not None, 'text not parsed: ' + label)
    return m


def dec_ratio(text):
    """Decimal like 0.000841519 or 1.2651e-6 as an exact rational."""
    require(re.fullmatch(r'\d+(\.\d+)?(e-?\d+)?', text) is not None, 'bad decimal ' + text)
    return Q(text)


# ---------------------------------------------------------------------------
# Contract, gate and inherited decimals: every target/reference/state value.
# ---------------------------------------------------------------------------
WORDS = {'seven': 7}


def load_contract():
    raw = (BASE / 'inputs' / CONTRACT_REL).read_bytes()
    require(sha_bytes(raw) == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen AV2 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'AV2' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return raw, c


def contract_values(c):
    p = c['parameters']
    pre = c['preregistration']
    req = c['required']
    V = {}
    V['tau'] = rat(p['tau'])
    V['control_tau'] = rat(p['control_tau'])
    require(V['control_tau'] == -V['tau'] and V['tau'] > 0, 'control coupling must mirror the frozen coupling')
    V['s'] = rat(p['s'])
    V['triple'] = [rat(x) for x in p['selected_coefficients_over_alpha']]
    require(V['triple'] == [0, 0, 0], 'zero-selected triple required')
    w = match(r'^g\(x\)=e\^\{-sx\} for x>=0; g\(x\)=e\^\{sx\}\(1-(\d+)sx\+(\d+)s\^2x\^2\) for x<0$', p['window'], 'window')
    V['window_c1_over_s'], V['window_c2_over_s2'] = int(w.group(1)), int(w.group(2))
    t = match(r'^ghat\(theta\)=(\d+)s\^3/\(pi\(s-i theta\)\^3\(s\+i theta\)\), \|ghat\|=\((\d+)s\^3/pi\)\(s\^2\+theta\^2\)\^-2, '
              r'\|\|ghat\|\|_1=(\d+), int\|theta\|\|ghat\|=(\d+)s/pi, int theta\^2\|ghat\|=(\d+)s\^2$', p['window_transform'], 'transform')
    V['ghat_coeff'], V['abs_coeff'], V['M0'], V['M1_coeff'], V['M2_coeff'] = (int(t.group(i)) for i in range(1, 6))
    k = match(r'^k=(\d+)\|tau\|/(\d+) in G=H/alpha units from \|\|B_N\|\|<=(\d+)\|tau\|/(\d+) \((\w+) stars\)$', p['duhamel_slope'], 'slope')
    V['k_over_tau'] = Q(int(k.group(1)), int(k.group(2)))
    V['B_over_tau'] = Q(int(k.group(3)), int(k.group(4)))
    V['stars'] = WORDS[k.group(5)]
    V['target'] = rat(p['absolute_target'])
    tg = pre['target']
    require(tg['quantity'] == 'radius' and tg['comparator'] == '<=' and rat(tg['value']) == V['target'], 'preregistered target differs')
    d = match(r'^D = (\d+)/(\d+) \(forward AV1 tier ii, admitted in research/round32/advisor/av1-gate\.json\); '
              r'tier \(i\) and the AT4 square-root bound must not be used$', p['state_bound'], 'state bound')
    V['D'] = Q(int(d.group(1)), int(d.group(2)))
    ri = p['retained_insufficient_controls']
    V['at4_radius_decimal'] = dec_ratio(match(r'^AT4 Poisson certificate at L=10\^(\d+) \(radius ~(0\.\d+)\)$', ri[0], 'at4').group(2))
    V['at4_L'] = Q(10) ** int(match(r'L=10\^(\d+)', ri[0], 'at4 L').group(1))
    fl = match(r'^optimized Poisson floor ~(\d\.\d+e-\d+) at L~(\d\.\d+)e(\d+) with D->0$', ri[1], 'floor')
    V['floor_decimal'] = dec_ratio(fl.group(1))
    V['floor_L_decimal'] = Q(fl.group(2)) * 10 ** int(fl.group(3))
    V['preview_radius'] = dec_ratio(match(r'^about (\d\.\d+e-\d+) \(skeptic review of AV1\); not a result$', p['preview_radius'], 'preview').group(1))
    cr = match(r'about (\d+\.\d+)-(\d+\.\d+)', req[5], 'crossover')
    V['s_star_window'] = (Q(cr.group(1)), Q(cr.group(2)))
    mo = match(r'Haar product reference C_0\(s\)=e\^\{-(\d+)s\}/(\d+)', c['model'], 'reference')
    V['free_energy'], V['free_den'] = int(mo.group(1)), int(mo.group(2))
    V['model_stars'] = WORDS[match(r'complete cover R=\{0,e_z\} with (\w+) incident stars', c['model'], 'cover').group(1)]
    ob = pre['observable']
    rf = match(r'^exp\(-(\d+)\)/(\d+) enclosed$', ob['reference_value_exact'], 'reference exact')
    require((int(rf.group(1)), int(rf.group(2))) == (V['free_energy'], V['free_den']) and ob['centering'] == 'vector'
            and ob['reference_route'] == 'haar', 'observable block differs from the model reference')
    V['model_id'] = pre['model_id']
    V['state_provenance'] = pre['state_provenance']
    V['node_s_values'] = [rat(x) for x in pre['nodes']['s_values']]
    require(V['node_s_values'] == [V['s']] and pre['nodes']['post_hoc_node_selection'] == 'forbidden', 'node declaration')
    V['error_terms'] = list(pre['error_terms_itemized'])
    V['sub_labels_allowed'] = list(pre['sub_labels_allowed'])
    V['controls'] = list(c['controls'])
    V['shared_premises'] = list(c['shared_premises'])
    V['forward_additional'] = list(c.get('forward_additional_premises', []))
    V['reverse_isolation'] = c.get('reverse_premise_isolation')
    sem = c['new_control_semantics']
    V['sign_mutation_multiplier'] = int(match(r'returns g\(-3\)/4=(\d+)e\^\{-3\}/4 on the free atom', sem['window_fourier_sign_convention'], 'sign').group(1))
    c1 = match(r'M_0=(\d+)/pi, M_1=(\d+)s/pi, M_2=infinity, negative-atom value (\d+)/e and sign-mutation value (\d+)e\^\{-3\}/4',
               sem['c1_window_preview_only'], 'c1')
    V['c1_M0_num'], V['c1_M1_coeff'], V['c1_atom'], V['c1_sign'] = (int(c1.group(i)) for i in range(1, 5))
    V['claim_exclusions'] = list(c['claim_exclusions'])
    V['prereg_exclusions'] = list(pre['claim_exclusions'])
    return V


def load_gate():
    raw = (BASE / 'inputs' / GATE_REL).read_bytes()
    g = json.loads(raw.decode('utf-8'))
    require(g.get('loop') == 'AV1' and g.get('verdict') == 'accepted_within_scope', 'AV1 gate identity/verdict')
    G = {'sha256': sha_bytes(raw)}
    dm = match(r'D_ii=(\d+)/(\d+) \(certified by both inequalities\) as the admitted state bound for AV2', g['decision'], 'gate decision')
    G['D_admitted'] = Q(int(dm.group(1)), int(dm.group(2)))
    di = match(r'D_i=(\d+)/(\d+) \(~2\.3680e-5; exact, forward\)', g['accepted'], 'gate tier i')
    G['D_tier_i'] = Q(int(di.group(1)), int(di.group(2)))
    dr = match(r'D_ii<=(\d+)/10\^40 \(~1\.1390e-8', g['accepted'], 'gate reverse refinement')
    G['D_ii_reverse_refinement'] = Q(int(dr.group(1)), 10 ** 40)
    return G


def load_at4_decimal():
    text = (BASE / 'inputs' / AT4_FWD_REL).read_text(encoding='utf-8')
    return dec_ratio(match(r'Their sum is `mathcal E\^\+≈(0\.\d+)`', text, 'AT4 radius decimal').group(1))


# ---------------------------------------------------------------------------
# Gaussian rationals and univariate polynomials (exact algebra).
# ---------------------------------------------------------------------------
def cx(re_, im_=0):
    return (Q(re_), Q(im_))


def cadd(u, v):
    return (u[0] + v[0], u[1] + v[1])


def cmul(u, v):
    return (u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def cscale(u, q):
    return (u[0] * q, u[1] * q)


def cinv(u):
    n = u[0] * u[0] + u[1] * u[1]
    require(n != 0, 'division by zero in Gaussian rationals')
    return (u[0] / n, -u[1] / n)


def cpow(u, n):
    r = (Q(1), Q(0))
    for _ in range(n):
        r = cmul(r, u)
    return r


def cabs2(u):
    return u[0] * u[0] + u[1] * u[1]


def ptrim(p):
    p = [Q(x) for x in p]
    while p and p[-1] == 0:
        p.pop()
    return p


def padd(p, q):
    n = max(len(p), len(q))
    return ptrim([(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)])


def pscale(p, a):
    return ptrim([Q(a) * x for x in p])


def psub(p, q):
    return padd(p, pscale(q, -1))


def pmul(p, q):
    p, q = ptrim(p), ptrim(q)
    if not p or not q:
        return []
    r = [Q(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            r[i + j] += x * y
    return ptrim(r)


def pder(p):
    p = ptrim(p)
    return ptrim([i * p[i] for i in range(1, len(p))])


def peval(p, x):
    return sum((c * Q(x) ** i for i, c in enumerate(ptrim(p))), Q(0))


def rderiv(r):
    num, den = r
    return (psub(pmul(pder(num), den), pmul(num, pder(den))), pmul(den, den))


def radd(r1, r2):
    return (padd(pmul(r1[0], r2[1]), pmul(r2[0], r1[1])), pmul(r1[1], r2[1]))


def requal(r1, r2):
    return ptrim(pmul(r1[0], r2[1])) == ptrim(pmul(r2[0], r1[1]))


# ---------------------------------------------------------------------------
# Window algebra: half-line transforms, matching, antiderivatives.
# ---------------------------------------------------------------------------
def family_numerator(s, c1, c2):
    """2 pi ghat * a^3 b for the left polynomial 1+c1 y+c2 y^2 (y=-x>0), a=s-i theta, b=s+i theta.

    Half-line Laplace transforms: int_0^inf e^{-(s+i theta)x}dx=1/b and
    int_0^inf y^n e^{-a y}dy=n!/a^{n+1}. With b=2s-a the numerator is
    (2s-c1)a^2+(2s c1-2c2)a+4s c2, returned as polynomial coefficients in a.
    """
    return [4 * s * c2, 2 * s * c1 - 2 * c2, 2 * s - c1]


def family_identity_in_a(s, c1, c2):
    """b(a^2+c1 a+2c2)+a^3 with b=2s-a, as a polynomial in a, equals family_numerator."""
    lhs = padd(pmul([2 * s, -1], [2 * c2, c1, 1]), [0, 0, 0, 1])
    return ptrim(lhs) == ptrim(family_numerator(s, c1, c2))


def family_identity_gaussian(s, c1, c2, theta):
    a, b = cx(s, -theta), cx(s, theta)
    lhs = cadd(cadd(cinv(b), cinv(a)), cadd(cscale(cinv(cpow(a, 2)), c1), cscale(cinv(cpow(a, 3)), 2 * c2)))
    n = family_numerator(s, c1, c2)
    num = cadd(cadd(cx(n[0]), cscale(a, n[1])), cscale(cpow(a, 2), n[2]))
    rhs = cmul(num, cinv(cmul(cpow(a, 3), b)))
    return lhs == rhs


def one_sided_derivatives(s, c1, c2, order=3):
    """g^{(n)}(0+) for e^{-sx} and g^{(n)}(0-) for e^{sx}(1-c1 x+c2 x^2), n=0..order."""
    p_derivs = [Q(1), Q(-c1), Q(2 * c2), Q(0)]
    right = [(-s) ** n for n in range(order + 1)]
    left = [sum((comb(n, j) * s ** (n - j) * p_derivs[j] for j in range(n + 1)), Q(0)) for n in range(order + 1)]
    return right, left


def antiderivative_table(s):
    """(f, rational part R, arctan coefficient B, range) with F=R+B*arctan(theta/s), F'=f."""
    S2 = [s * s, 0, 1]
    S4 = pmul(S2, S2)
    S6 = pmul(S4, S2)
    return {
        'M0_integrand_(s2+t2)^-2': (([1], S4), ([0, 1], pscale(S2, 2 * s * s)), 1 / (2 * s ** 3), 'full_line'),
        'M1_integrand_t(s2+t2)^-2': (([0, 1], S4), ([Q(-1, 2)], S2), Q(0), 'half_line'),
        'M2_integrand_t2(s2+t2)^-2': (([0, 0, 1], S4), ([0, Q(-1, 2)], S2), 1 / (2 * s), 'full_line'),
        'inversion_x0_integrand_(s2-t2)(s2+t2)^-3': (([s * s, 0, -1], S6), ([0, 3 * s * s, 0, 1], pscale(S4, 4 * s * s)), 1 / (4 * s ** 3), 'full_line'),
    }


def verify_antiderivative(s, entry):
    f, R, B, rng = entry
    S2 = [s * s, 0, 1]
    deriv = rderiv(R)
    total = radd(deriv, ([s * B], S2)) if B else deriv
    ok = requal(total, f)
    vanishes = len(ptrim(R[0])) < len(ptrim(R[1]))   # rational part -> 0 at +-infinity
    if rng == 'full_line':
        integral_pi_coeff, integral_rational = B, Q(0)        # B*(pi/2-(-pi/2))
    else:
        integral_pi_coeff, integral_rational = B / 2, -peval(R[0], 0) / peval(R[1], 0)
    return ok and vanishes, integral_pi_coeff, integral_rational


def window_moments_exact(s):
    """M_j = (4s^3/pi) int |theta|^j (s^2+theta^2)^-2 as {power of pi: coefficient}."""
    tab = antiderivative_table(s)
    out = {}
    ok_all = True
    for name, entry in tab.items():
        ok, pc, rc = verify_antiderivative(s, entry)
        ok_all = ok_all and ok
        out[name] = (pc, rc)
    pc0, rc0 = out['M0_integrand_(s2+t2)^-2']
    pc1, rc1 = out['M1_integrand_t(s2+t2)^-2']
    pc2, rc2 = out['M2_integrand_t2(s2+t2)^-2']
    pc3, rc3 = out['inversion_x0_integrand_(s2-t2)(s2+t2)^-3']
    require(rc0 == 0 and pc1 == 0 and rc2 == 0 and rc3 == 0, 'unexpected antiderivative structure')
    pref = 4 * s ** 3
    return ok_all, {'M0': {0: pref * pc0}, 'M1': {-1: pref * 2 * rc1}, 'M2': {0: pref * pc2}, 'int_ghat': {0: pref * pc3}}


def moment_preview(s, pi_mid, T=200, steps_per_unit=20):
    """Midpoint-rule preview (not admission) of M_0, M_1, M_2 with leading tails 1/(3T^3), 1/(2T^2), 1/T."""
    h = Q(1, steps_per_unit)
    acc = [Q(0), Q(0), Q(0)]
    for j in range(T * steps_per_unit):
        th = (j + Q(1, 2)) * h
        f = 1 / (s * s + th * th) ** 2
        acc[0] += calc.down(f * h)
        acc[1] += calc.down(th * f * h)
        acc[2] += calc.down(th * th * f * h)
    tails = [Q(1, 3 * T ** 3), Q(1, 2 * T ** 2), Q(1, T)]
    pref = 2 * 4 * s ** 3 / pi_mid
    return [pref * (acc[i] + tails[i]) for i in range(3)]


# ---------------------------------------------------------------------------
# Geometry: original Wilson cover and incident whole stars.
# ---------------------------------------------------------------------------
DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
S_STAR = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def vadd(p, q):
    return tuple(a + b for a, b in zip(p, q))


def vsub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def factor_links(b):
    return [((4 * b[0] + r, 2 * b[1] + q, b[2]), d) for r in range(4) for q in range(2) for d in 'xyz']


def wilson_geometry():
    links = [((0, 0, 0), 'x'), ((1, 0, 0), 'z'), ((0, 0, 1), 'x'), ((0, 0, 0), 'z')]
    owners = [owner(t) for t, _ in links]
    R = sorted(set(owners))
    cover = [lk for b in R for lk in factor_links(b)]
    endpoints = set()
    per_factor = {}
    for b in R:
        e = set()
        for t, d in factor_links(b):
            e.add(t)
            e.add(vadd(t, DIRS[d]))
        per_factor[b] = e
        endpoints |= e
    shared = per_factor[R[0]] & per_factor[R[1]]
    anchors = sorted({vsub(r, d) for r in R for d in S_STAR})
    return {'owners': owners, 'R': R, 'cover_links': len(set(cover)), 'endpoints': len(endpoints),
            'per_factor': [len(per_factor[b]) for b in R], 'shared': len(shared), 'anchors': anchors,
            'drawn_links': len(set(links))}


def retained_anchors(N):
    return [(x, y, z) for x in range(-N, N) for y in range(-N, N) for z in range(-N, N)]


def incident_in_box(N, R):
    return [b for b in retained_anchors(N) if any(vadd(b, d) in R for d in S_STAR)]


# ---------------------------------------------------------------------------
# Main computation.
# ---------------------------------------------------------------------------
def compute(check_sha, calc_sha):
    raw, c = load_contract()
    check('contract_snapshot_sha256', sha_bytes(raw) == CONTRACT_SHA256, contract=CONTRACT_REL, sha256=CONTRACT_SHA256,
          note='target, reference, D, window and slope are read from this hash-checked snapshot')
    V = contract_values(c)
    G = load_gate()
    tau, s1, target = V['tau'], V['s'], V['target']
    pi_lo, pi_hi = calc.pi_interval()
    pi_mid = (pi_lo + pi_hi) / 2

    # -------------------- window definition and C^2 matching --------------------
    svals = [Q(1, 2), Q(1), Q(2), Q(7, 3)]
    thetas = [Q(0), Q(1, 3), Q(1), Q(2), Q(-5, 7), Q(10), Q(-31, 4)]
    match_ok = True
    jumps = []
    for sv in svals:
        c1, c2 = V['window_c1_over_s'] * sv, V['window_c2_over_s2'] * sv * sv
        right, left = one_sided_derivatives(sv, c1, c2)
        match_ok = match_ok and right[:3] == left[:3] and right[3] != left[3]
        jumps.append(right[3] - left[3])
    check('window_c2_matching',
          match_ok and all(j == -8 * sv ** 3 for j, sv in zip(jumps, svals))
          and V['window_c1_over_s'] == 2 and V['window_c2_over_s2'] == 2,
          left_polynomial_parsed_from_contract='1-2sx+2s^2x^2 (x<0)',
          matched_orders='value, first and second one-sided derivatives at x=0',
          third_derivative_jump='g\'\'\'(0+)-g\'\'\'(0-)=-8s^3 (nonzero; fixes |ghat|~(4s^3/pi)theta^-4)',
          l1_norm_of_g='8/s (1/s from x>=0 plus 1/s+2/s+4/s from x<0); g continuous, positive, exponentially decaying: g in L^1 cap C_0')

    # -------------------- half-line transforms and cancellation --------------------
    fam_ok = True
    for sv in svals:
        fams = [(Q(0), Q(0)), (2 * sv, Q(0)), (2 * sv, 2 * sv * sv), (Q(1), Q(3))]
        for c1, c2 in fams:
            fam_ok = fam_ok and family_identity_in_a(sv, c1, c2)
            for th in thetas:
                fam_ok = fam_ok and family_identity_gaussian(sv, c1, c2, th)
    c2_num = [family_numerator(sv, 2 * sv, 2 * sv * sv) for sv in svals]
    check('half_line_transform_identity',
          fam_ok and all(ptrim(n) == [8 * sv ** 3] for n, sv in zip(c2_num, svals)),
          algebraic_identity='2 pi ghat = 1/(s+i theta) + 1/a + 2s/a^2 + 4s^2/a^3 = 8s^3/(a^3 b), a=s-i theta, b=s+i theta',
          verified='polynomial identity in a (b=2s-a) and Gaussian-rational evaluation at 7 theta, 4 s, 4 left polynomials',
          ghat='4s^3/(pi (s-i theta)^3 (s+i theta))', ghat_at_0='4/(pi s) = ||g||_1/(2 pi)')
    pois = family_numerator(Q(1), Q(0), Q(0))
    c1w = family_numerator(Q(1), Q(2), Q(0))
    check('theta_power_cancellation',
          ptrim(pois) == [0, 0, 2] and ptrim(c1w) == [0, 4] and ptrim(family_numerator(Q(1), Q(2), Q(2))) == [8],
          general_numerator='(2s-c1)a^2+(2s c1-2c2)a+4s c2',
          reading='a^2 coefficient <-> theta^-2 decay (kink, C^0 only); a coefficient <-> theta^-3 decay (C^1 only); C^2 matching c1=2s, c2=2s^2 leaves 8s^3 (theta^-4)',
          poisson_member='c1=c2=0 gives 2s/(ab): ghat=s/(pi(s^2+theta^2)), the Poisson kernel',
          c1_member='c1=2s, c2=0 gives 4s^2 a/(a^3 b): ghat=2s^2/(pi a^2 b)')
    mod_ok = True
    for sv in svals:
        for th in thetas:
            a, b = cx(sv, -th), cx(sv, th)
            den = cmul(cpow(a, 3), b)
            mod_ok = mod_ok and cabs2(den) == (sv * sv + th * th) ** 4
            mod_ok = mod_ok and cinv(den) == cscale(cmul(b, b), 1 / (sv * sv + th * th) ** 3)
    check('modulus_identity', mod_ok and V['abs_coeff'] == V['ghat_coeff'] == 4,
          algebraic_identity='|a^3 b|^2=(s^2+theta^2)^4, so |ghat|=(4s^3/pi)(s^2+theta^2)^-2; 1/(a^3 b)=b^2/(s^2+theta^2)^3',
          real_part='(4s^3/pi)(s^2-theta^2)/(s^2+theta^2)^3', imaginary_part='(4s^3/pi)2s theta/(s^2+theta^2)^3 (odd)')

    # -------------------- constants by antiderivatives --------------------
    anti_ok = True
    moments = {}
    for sv in svals:
        ok, mm = window_moments_exact(sv)
        anti_ok = anti_ok and ok
        moments[sv] = mm
    check('antiderivative_identities', anti_ok,
          antiderivatives={'(s^2+t^2)^-2': 't/(2s^2(s^2+t^2)) + arctan(t/s)/(2s^3)',
                           't(s^2+t^2)^-2': '-1/(2(s^2+t^2))',
                           't^2(s^2+t^2)^-2': '-t/(2(s^2+t^2)) + arctan(t/s)/(2s)',
                           '(s^2-t^2)(s^2+t^2)^-3': 't/(2(s^2+t^2)^2) + t/(4s^2(s^2+t^2)) + arctan(t/s)/(4s^3)'},
          verified='F\'=f as exact rational-function identities (with arctan\'(t/s)=s/(s^2+t^2)) at s in {1/2,1,2,7/3}; rational parts vanish at infinity')
    const_ok = all(moments[sv]['M0'] == {0: Q(2)} and moments[sv]['M1'] == {-1: 4 * sv} and moments[sv]['M2'] == {0: 2 * sv * sv}
                   for sv in svals)
    check('window_constants_exact',
          const_ok and V['M0'] == 2 and V['M1_coeff'] == 4 and V['M2_coeff'] == 2,
          M0='2 (pi cancels)', M1='4s/pi', M2='2s^2', contract_values_compared_after_derivation=True,
          M1_at_s1_interval=[s_(4 / pi_hi), s_(4 / pi_lo)])
    check('inversion_at_origin_exact', all(moments[sv]['int_ghat'] == {0: Q(1)} for sv in svals),
          statement='int ghat dtheta = g(0) = 1 while int |ghat| dtheta = 2: ghat is complex, not a positive mass-one kernel')
    check('pi_machin_directed', Q(333, 106) < pi_lo < pi_hi < Q(355, 113) and pi_hi - pi_lo <= Q(3, 10 ** 39),
          pi_interval=[s_(pi_lo), s_(pi_hi)], method='pi=16 atan(1/5)-4 atan(1/239), 80-term alternating brackets, outward to 10^-40')
    prev = moment_preview(Q(1), pi_mid)
    exact_s1 = [Q(2), 4 / pi_mid, Q(2)]
    check('constants_numerical_preview', all(abs(p - e) <= Q(1, 1000) for p, e in zip(prev, exact_s1)),
          preview_only=True, M0_preview=dec(prev[0], 8), M1_preview=dec(prev[1], 8), M2_preview=dec(prev[2], 8),
          method='midpoint rule on [0,200], step 1/20, plus leading tails; s=1; not used for admission')

    # -------------------- state bound, slope, radius --------------------
    D_formula = calc.av1_tier_ii_D(tau)
    check('av1_state_bound_recomputed',
          D_formula == V['D'] == G['D_admitted'] and V['D'] <= Q(4, 10 ** 7),
          D=s_(V['D']), D_preview=dec(V['D']), formula='J=28|tau|, t_1=49|tau|/144, T=t_1/(1-352J), eps=2T+T^2, D=2eps(1+eps)/(1+eps^2)',
          gate_sha256=G['sha256'], consequences='|m|=|omega(W)|<=D, m^2<=D^2 (trace duality, omega_0(W)=0, ||W||=1)')
    geo = wilson_geometry()
    k_contract = V['k_over_tau'] * tau
    star_norm = Q(7) * tau / 8
    B_norm = len(geo['anchors']) * star_norm
    check('duhamel_slope_seven_stars',
          len(geo['anchors']) == V['stars'] == V['model_stars'] == 7 and B_norm == V['B_over_tau'] * tau
          and 2 * B_norm == k_contract,
          star_norm_G_units='||V_b||=||phi_b||/8<=7|tau|/8', B_N='sum over the seven incident stars <= 49|tau|/8',
          k=s_(k_contract), conjugation='||U X U*-X||<=2||U-I|| ||X||, ||U-I||<=|theta| ||B_N|| (relative unitary)')

    cert_p = calc.certify(fixed_design=True)
    cert_m = calc.certify(tau=s_(V['control_tau']), fixed_design=True)
    M0 = Q(2)
    M1_up = 4 * s1 / pi_lo
    terms = {'state': M0 * V['D'], 'mean_square': M0 * V['D'] ** 2, 'kernel_dynamics': k_contract * M1_up}
    f_lo, f_hi = calc.exp_negative(V['free_energy'] * s1)
    f_lo, f_hi = f_lo / V['free_den'], f_hi / V['free_den']
    datum = (f_lo + f_hi) / 2
    terms['arithmetic'] = (f_hi - f_lo) / 2
    radius = terms['state'] + terms['mean_square'] + terms['kernel_dynamics'] + terms['arithmetic']
    cert_terms = {kk: rat(v) for kk, v in cert_p['costs'].items()}
    check('radius_itemized_tau_plus',
          cert_terms == terms and rat(cert_p['certified_absolute_error']) == radius and rat(cert_p['certified_datum']) == datum
          and rat(cert_p['state_bound_D']) == V['D'] and rat(cert_p['duhamel_slope_k']) == k_contract,
          formula='E=M_0(D+D^2)+k M_1 with M_0=2, M_1=4s/pi (pi lower bound), plus the midpoint arithmetic radius',
          terms={kk: s_(v) for kk, v in terms.items()}, radius=s_(radius), radius_preview=dec(radius, 12, 'up'))
    check('mirrored_coupling_replay',
          cert_m['certified_absolute_error'] == cert_p['certified_absolute_error'] and cert_m['certified_datum'] == cert_p['certified_datum']
          and cert_m['mirrored_coupling_replay'] is True and cert_p['mirrored_coupling_replay'] is False,
          tau=s_(V['control_tau']), note='same |tau| formula; a replay of the certificate at the mirrored coupling, not a second confirmation')
    target_met = radius <= target
    check('target_boolean_1e-6', target_met is True and cert_p['target_met'] is True and cert_m['target_met'] is True,
          target=s_(target), radius=s_(radius), margin_target_over_radius_lower=dec(target / radius, 6, 'down'))
    lo_C, hi_C = datum - radius, datum + radius
    check('free_reference_inside_reference_unresolved',
          lo_C <= f_lo and f_hi <= hi_C and cert_p['free_reference_included'] is True and cert_p['sub_label'] == 'reference_unresolved'
          and 'reference_unresolved' in V['sub_labels_allowed'] and cert_p['resolved_interaction_shift'] is False,
          free_interval=[s_(f_lo), s_(f_hi)], sub_label='reference_unresolved')
    check('rational_datum_and_arithmetic',
          datum == (f_lo + f_hi) / 2 and 0 < terms['arithmetic'] <= Q(1, 10 ** 40) and hi_C - lo_C == 2 * radius,
          datum=s_(datum), arithmetic=s_(terms['arithmetic']),
          exp_method='alternating Taylor P_41<=e^-z<=P_40 on [0,1/2], halving 3->3/8 three times, outward squaring to 10^-40')
    check('preview_radius_consistency', abs(radius - V['preview_radius']) <= Q(1, 10 ** 9),
          contract_preview=s_(V['preview_radius']), computed_preview=dec(radius, 6, 'up'), note='the contract preview is not a result')

    # -------------------- retained failures --------------------
    s1_ = s1
    D4_lo, D4_hi = calc.sqrt_interval(Q(49, 3) * tau)
    D4_lo, D4_hi = 2 * D4_lo, 2 * D4_hi
    L4 = V['at4_L']
    lg_lo, lg_hi = calc.log_positive(1 + (L4 / s1_) ** 2)

    def poisson_radius(Dv, kv, sv, Lv, lg, pi_div, pi_tail):
        return Dv + Dv * Dv + kv * sv * lg / pi_div + (Q(1, 2) + Dv / 2) * 2 * sv / (pi_tail * Lv)
    at4_hi = poisson_radius(D4_hi, k_contract, s1_, L4, lg_hi, pi_lo, pi_lo)
    at4_lo = poisson_radius(D4_lo, k_contract, s1_, L4, lg_lo, pi_hi, pi_hi)
    at4_report = load_at4_decimal()
    check('retained_at4_poisson_radius',
          at4_lo > target and abs(at4_hi - at4_report) <= Q(1, 10 ** 15) and abs(at4_hi - V['at4_radius_decimal']) <= Q(1, 10 ** 9),
          L=s_(L4), D_at4='2 sqrt(49|tau|/3)', radius_interval=[s_(at4_lo), s_(at4_hi)], radius_preview=dec(at4_hi, 12, 'up'),
          at4_report_decimal=s_(at4_report), target_met=False)
    kk2 = 2 * k_contract
    inv2k = 1 / kk2
    lgk_lo, _ = calc.log_positive(inv2k / s1_)
    floor_lo = kk2 * s1_ * (1 + lgk_lo) / pi_hi
    L_star = Q(inv2k.numerator // inv2k.denominator + 1)
    lgs_lo, lgs_hi = calc.log_positive(1 + (L_star / s1_) ** 2)
    floor_hi = k_contract * s1_ * lgs_hi / pi_lo + s1_ / (pi_lo * L_star)
    floor_with_D_lo = floor_lo + V['D'] + V['D'] ** 2
    check('retained_poisson_floor',
          target < floor_lo <= floor_hi and abs(floor_hi - V['floor_decimal']) <= Q(1, 10 ** 10)
          and abs(L_star - V['floor_L_decimal']) <= Q(1, 100) * L_star and floor_with_D_lo > target,
          lower_bound='for every L>0: (ks/pi)log(1+L^2/s^2)+s/(pi L) >= (2ks/pi)(1+log(1/(2ks))) since log(1+L^2/s^2)>=2log(L/s), minimized at L=1/(2k)',
          floor_interval=[s_(floor_lo), s_(floor_hi)], floor_preview=[dec(floor_lo, 8, 'down'), dec(floor_hi, 8, 'up')],
          L_evaluated=s_(L_star), with_admitted_D_lower=dec(floor_with_D_lo, 8, 'down'), target_met=False)
    Ls = [Q(10) ** 4, Q(10) ** 8, Q(10) ** 16, Q(10) ** 32]
    pm_lo = []
    for Lv in Ls:
        lo_, _ = calc.log_positive(1 + (Lv / s1_) ** 2)
        pm_lo.append(s1_ * lo_ / pi_hi)
    l10_lo, _ = calc.log_positive(Q(10))
    first_lo, _ = calc.log_positive(Q(65))
    window_M1_hi = 4 * s1_ / pi_lo
    grow_ok = all(pm_lo[i + 1] > pm_lo[i] for i in range(3)) and all(
        pm_lo[i] >= 2 * s1_ * (4 * 2 ** i - 1) * l10_lo / pi_hi for i in range(4))
    check('poisson_first_moment_divergence_exhibited',
          grow_ok and s1_ * first_lo / pi_hi > window_M1_hi and k_contract * pm_lo[-1] > target,
          partial_first_moment='int_{-L}^{L}|theta| s/(pi(s^2+theta^2)) = (s/pi)log(1+L^2/s^2) >= (2s/pi)log(L/s) -> infinity',
          lower_bounds={'L=10^4': dec(pm_lo[0], 8, 'down'), 'L=10^8': dec(pm_lo[1], 8, 'down'),
                        'L=10^16': dec(pm_lo[2], 8, 'down'), 'L=10^32': dec(pm_lo[3], 8, 'down')},
          window_first_moment=s_(4) + 's/pi (finite; ~' + dec(window_M1_hi, 8, 'up') + ' at s=1)',
          exceeds_window_moment_from='L=8 (log 65 > 4)', dynamics_alone_at_L_1e32_lower=dec(k_contract * pm_lo[-1], 6, 'down'))

    # -------------------- crossover --------------------
    A = 2 * (V['D'] + V['D'] ** 2)
    slope_const = V['k_over_tau'] * 4 * tau          # k*M_1/s = 49|tau|/pi times pi
    s_star_lo = pi_lo * (target - A) / slope_const
    s_star_hi = pi_hi * (target - A) / slope_const

    def E_up(sv):
        return A + slope_const * sv / pi_lo

    def E_low(sv):
        return A + slope_const * sv / pi_hi
    check('crossover_s_star',
          V['s_star_window'][0] < s_star_lo <= s_star_hi < V['s_star_window'][1]
          and E_up(s_star_lo) == target and E_low(s_star_hi) == target and E_up(Q(6)) <= target and E_low(Q(7)) > target
          and E_low(Q(128)) > target,
          s_star_interval=[s_(s_star_lo), s_(s_star_hi)], s_star_preview=[dec(s_star_lo, 10, 'down'), dec(s_star_hi, 10, 'up')],
          E_of_s='2(D+D^2)+49|tau|s/pi (analytic radius, linear in s)', E_at_128_lower=dec(E_low(Q(128)), 6, 'down'),
          grid_claim=False, note='no node other than s=1 is evaluated; no [0,128] grid claim at the cap')

    # ======================= contract controls =======================
    # kernel_identity_on_support
    xs = [Q(0), Q(1, 32), Q(1, 3), Q(1), Q(3), Q(17, 2)]

    def window_on_support(mult, sv):
        for x in xs:
            require(mult(x, sv) == 1, 'window differs from e^{-sx} on the AQ1 support [0,inf) at x=' + s_(x))
        return True
    eta_A = [(Q(2), Q(1, 8)), (Q(4), Q(1, 8))]
    eta_B = [(Q(1), Q(1, 32)), (Q(3), Q(3, 16)), (Q(5), Q(1, 32))]
    fixture_ok = all(calc.window_multiplier(x, sv) == 1 for sv in svals for x, _ in eta_A + eta_B)

    def symmetric_window(x, sv):
        y = abs(Q(x))
        return 1 + 2 * sv * y + 2 * sv * sv * y * y

    def gap_dependent_window(x, sv):
        return Q(1) if Q(x) >= Q(1, 16) else Q(2)
    check('kernel_identity_on_support',
          all(window_on_support(calc.window_multiplier, sv) for sv in svals) and fixture_ok
          and calc.window_multiplier(V['free_energy'], s1) == 1
          and rejected(lambda: window_on_support(symmetric_window, s1), 'symmetric_window_misreads_support')
          and rejected(lambda: window_on_support(gap_dependent_window, s1), 'window_matched_only_above_AQ2_gap'),
          sampled_x=[s_(x) for x in xs], g_at_3='e^{-3s} (multiplier 1)', premise='AQ1 nonnegativity only (support [0,inf)); AQ2 gap not used',
          fixtures='eta_A=(delta_2+delta_4)/8, eta_B=delta_1/32+3delta_3/16+delta_5/32: int g d eta = int e^{-sx} d eta exactly')

    # kernel_negative_atom_misread
    em_lo, em_hi = calc.exp_negative(Q(1))
    e_lo, e_hi = calc.exp_positive(Q(1))
    mult_m1 = calc.window_multiplier(Q(-1), s1)

    def lemma_measure(atoms):
        for x, w in atoms:
            require(x >= 0 and w >= 0, 'window lemma needs a positive measure on [0,inf): atom at ' + s_(x))
        return True
    taylor_ok = all((1 + 2 * sv + 2 * sv * sv) < (1 + 2 * sv + 2 * sv * sv + Q(4, 3) * sv ** 3) for sv in svals)
    check('kernel_negative_atom_misread',
          mult_m1 == 5 and mult_m1 * em_hi < e_lo and taylor_ok and lemma_measure(eta_A) and lemma_measure(eta_B)
          and rejected(lambda: lemma_measure([(Q(-1), Q(1))]), 'negative_atom_admitted'),
          window_value='g(-1)=e^{-s}(1+2s+2s^2)=5/e at s=1', heat_value='e^{s}=e', window_upper=s_(5 * em_hi), heat_lower=s_(e_lo),
          general_s='e^{2s}>=1+2s+2s^2+(4/3)s^3>1+2s+2s^2: the window under-reads every negative atom; nonnegativity is essential')

    # kernel_l1_and_first_moment
    def validate_constants(M0v, M1v_coeff, sv):
        require(M0v == moments[sv]['M0'][0], 'M_0 differs from ||ghat||_1')
        require(M1v_coeff == moments[sv]['M1'][-1], 'M_1 differs from int|theta||ghat|')
        return True
    check('kernel_l1_and_first_moment',
          all(validate_constants(Q(2), 4 * sv, sv) for sv in svals)
          and rejected(lambda: validate_constants(Q(1), Q(4), Q(1)), 'positive_kernel_mass_one')
          and rejected(lambda: validate_constants(moments[Q(1)]['int_ghat'][0], Q(4), Q(1)), 'signed_integral_as_l1_norm')
          and rejected(lambda: validate_constants(Q(2), Q(4), Q(2)), 'first_moment_without_s'),
          M0='2', M1='4s/pi', tail_bound='|theta||ghat|<=(4s^3/pi)|theta|^-3: tail beyond T is (4s^3/pi)/T^2',
          fubini='int int |ghat(theta) e^{i theta x}| dtheta d eta(x) = M_0 eta([0,inf)) < inf')

    # poisson_kink_divergence
    def require_finite_first_moment(sv, c1, c2):
        n = family_numerator(sv, c1, c2)
        require(n[2] == 0, 'kernel has a theta^-2 tail (kink): its absolute first moment diverges')
        return True
    rP, lP = one_sided_derivatives(s1, Q(0), Q(0))
    check('poisson_kink_divergence',
          rP[1] == -s1 and lP[1] == s1 and require_finite_first_moment(s1, 2 * s1, 2 * s1 * s1)
          and require_finite_first_moment(s1, 2 * s1, Q(0)) and grow_ok
          and rejected(lambda: require_finite_first_moment(s1, Q(0), Q(0)), 'window_formula_applied_to_poisson')
          and rejected(lambda: require(k_contract * pm_lo[-1] <= target, 'full-line Duhamel over Poisson'), 'full_line_poisson_duhamel_finite'),
          kink="g'(0-)=s, g'(0+)=-s for e^{-s|x|}", poisson_numerator_a2_coefficient=s_(pois[2]),
          partial_moment_lower_L_1e32=dec(pm_lo[-1], 8, 'down'))

    # window_linear_in_s
    Es = {sv: calc.certify(s=s_(sv)) for sv in [Q(1, 2), Q(1), Q(2), Q(6)]}
    lin_ok = all(rat(Es[sv]['analytic_radius']) == A + slope_const * sv / pi_lo for sv in Es) and \
        all(rat(Es[sv]['window']['M0']) == 2 for sv in Es)
    scale_ok = True
    for sv in svals:
        for th in thetas:
            val_s = 1 / (sv * sv + th * th) ** 2 * sv ** 3
            val_1 = 1 / (1 + (th / sv) ** 2) ** 2
            scale_ok = scale_ok and val_s * sv == val_1

    def validate_node_claim(sv, claimed):
        require(sv in V['node_s_values'], 'post-hoc node selection is forbidden')
        require(claimed == rat(calc.certify(s=s_(sv))['analytic_radius']), 'claimed radius differs from E(s)')
        return True
    check('window_linear_in_s',
          lin_ok and scale_ok and validate_node_claim(s1, rat(cert_p['analytic_radius']))
          and rejected(lambda: validate_node_claim(Q(7), rat(cert_p['analytic_radius'])), 'node_s7_with_s1_radius')
          and rejected(lambda: validate_node_claim(s1, A + slope_const / pi_lo * 0), 'dynamics_term_dropped'),
          E_of_s='2(D+D^2)+(49|tau|/pi)s', scaling='|ghat_s(theta)|=s^-1|ghat_1(theta/s)|: M_0 fixed, M_1 prop s, M_2 prop s^2',
          E_preview={s_(sv): dec(rat(Es[sv]['analytic_radius']), 8, 'up') for sv in Es})

    # local_not_extensive_duhamel
    Rset = set(geo['R'])
    counts_N = {N: len(incident_in_box(N, Rset)) for N in (2, 3, 4)}
    ext = {N: len(retained_anchors(N)) for N in (2, 3, 4)}

    def validate_slope(k_by_N):
        vals = set(k_by_N.values())
        require(len(vals) == 1, 'Duhamel slope depends on the box: extensive norm used')
        require(vals == {k_contract}, 'slope differs from 2*(seven stars)*(7|tau|/8)')
        return True
    u = cx(Q(3, 5), Q(4, 5))
    U_minus_I2 = cabs2(cadd(u, cx(-1)))
    conj_diff2 = cabs2(cadd(cmul(u, u), cx(-1)))
    check('local_not_extensive_duhamel',
          all(v == 7 for v in counts_N.values()) and validate_slope({N: 2 * counts_N[N] * star_norm for N in counts_N})
          and 1 < conj_diff2 / U_minus_I2 <= 4
          and rejected(lambda: validate_slope({N: 2 * ext[N] * star_norm for N in ext}), 'extensive_total_norm')
          and rejected(lambda: validate_slope({N: counts_N[N] * star_norm for N in counts_N}), 'conjugation_factor_two_dropped'),
          incident_stars_by_N={str(N): str(v) for N, v in counts_N.items()}, retained_stars_by_N={str(N): str(v) for N, v in ext.items()},
          conjugation_fixture='U=diag(u,conj u), u=(3+4i)/5, X=sigma_x: ||UXU*-X||^2/||U-I||^2=16/5 in (1,4]')

    # tau_zero_null_replay
    z = calc.certify(tau='0')
    L9 = Q(10) ** 9

    def validate_poisson_null(radius_claim, sv, Lv):
        require(radius_claim >= sv / (pi_hi * Lv), 'Poisson tail s/(pi L) missing at tau=0')
        return True

    def validate_window_null(res):
        require(rat(res['certified_absolute_error']) == rat(res['costs']['arithmetic']), 'window radius at tau=0 is not the arithmetic term alone')
        require(res['zero_coupling_branch_used'] is False, 'special zero branch used')
        return True
    fake = dict(z)
    fake['certified_absolute_error'] = s_(rat(z['costs']['arithmetic']) + s1 / (pi_lo * L4))
    p0 = {Lv: s1 / (pi_lo * Lv) for Lv in (L4, L9)}
    check('tau_zero_null_replay',
          validate_window_null(z) and all(rat(z['costs'][kk]) == 0 for kk in ('state', 'mean_square', 'kernel_dynamics'))
          and rat(z['state_bound_D']) == 0 and all(validate_poisson_null(v, s1, Lv) for Lv, v in p0.items())
          and rejected(lambda: validate_poisson_null(Q(3, 2 * 10 ** 30), s1, L4), 'poisson_null_arithmetic_only_L1e4')
          and rejected(lambda: validate_poisson_null(Q(3, 2 * 10 ** 30), s1, L9), 'poisson_null_arithmetic_only_L1e9')
          and rejected(lambda: validate_window_null(fake), 'window_null_with_fictitious_tail'),
          window_radius_tau0=z['certified_absolute_error'], window_arithmetic_tau0=z['costs']['arithmetic'],
          poisson_tail_tau0={'L=10^4': dec(p0[L4], 8, 'up'), 'L=10^9': dec(p0[L9], 8, 'up')})

    # window_fourier_sign_convention
    def reference_from_convention(sign):
        """int ghat(sign*theta) c_0(theta) dtheta = g(sign*3)/4 as a multiplier of e^{-3s}/4."""
        return calc.window_multiplier(sign * V['free_energy'], s1)

    def validate_reference(mult):
        require(mult == 1, 'reference differs from e^{-3s}/4: wrong Fourier sign convention')
        return True
    check('window_fourier_sign_convention',
          validate_reference(reference_from_convention(1)) and reference_from_convention(-1) == V['sign_mutation_multiplier'] == 25
          and rejected(lambda: validate_reference(reference_from_convention(-1)), 'theta_to_minus_theta'),
          frozen='c(theta)=<chi,e^{i theta G}chi>, ghat(theta)=(2pi)^-1 int g(x)e^{-i theta x}dx, g(x)=int ghat(theta)e^{i theta x}dtheta',
          mutation_value='g(-3)/4=25e^{-3}/4 at s=1')

    # state_term_not_effect
    Delta = [Q(1, 2), Q(-1, 2)]
    X_ne = [Q(1), Q(-1)]
    A_eff = [Q(1), Q(0)]
    tr_ne = sum(d_ * x_ for d_, x_ in zip(Delta, X_ne))
    tr_eff = sum(d_ * x_ for d_, x_ in zip(Delta, A_eff))
    norm1 = sum(abs(d_) for d_ in Delta)
    D_ = V['D']

    def validate_state_term(state_term):
        require(state_term == M0 * D_, 'state term must be M_0*D (trace duality for the non-effect W alpha^0_theta(W))')
        return True
    check('state_term_not_effect',
          abs(tr_ne) == norm1 > norm1 / 2 and abs(tr_eff) <= norm1 / 2 and validate_state_term(terms['state'])
          and rejected(lambda: validate_state_term(M0 * D_ / 2), 'effect_refinement_D_over_2'),
          fixture='Delta=diag(1/2,-1/2), ||Delta||_1=1: |Tr(Delta diag(1,-1))|=1>1/2, |Tr(Delta diag(1,0))|=1/2',
          reason='W alpha^0_theta(W) has free expectation e^{3i theta}/4 (non-real at theta=pi/6): not self-adjoint, not an effect (AT4 F12)')

    # av1_tier_bound
    t_i = 28 * tau * Q(148, 7)
    eps_i = 2 * t_i + t_i ** 2
    D_i = 2 * eps_i * (1 + eps_i) / (1 + eps_i ** 2)

    def validate_tier(Dv):
        require(Dv == G['D_admitted'] == V['D'], 'state bound is not the AV1 tier admitted for AV2')
        return True
    check('av1_tier_bound',
          validate_tier(V['D']) and validate_tier(rat(cert_p['state_bound_D'])) and D_i == G['D_tier_i']
          and rejected(lambda: validate_tier(D_i), 'tier_i_crude_majorant')
          and rejected(lambda: validate_tier(D4_hi), 'at4_square_root_bound')
          and rejected(lambda: validate_tier(G['D_ii_reverse_refinement']), 'reverse_82_face_refinement_not_bound_for_AV2')
          and calc_rejects({'state_tier': 'av1_tier_i'}, 'calculator_tier_i')
          and calc_rejects({'state_tier': 'at4_sqrt'}, 'calculator_at4')
          and calc_rejects({'D': '1/100000000'}, 'calculator_supplied_D', (ValueError, TypeError)),
          D_bound=s_(V['D']), gate_decision='forward tier (ii) bound as the admitted state bound for AV2',
          tier_i_window_radius_lower=dec(2 * D_i + slope_const / pi_hi, 8, 'down'),
          note='the reverse refinement is valid in AV1 but is not the premise bound by this contract; no switch after freeze')

    # reverse_premise_isolation
    forward_list = ['AGENTS.md', CONTRACT_REL] + V['shared_premises'] + V['forward_additional']
    reverse_list = ['AGENTS.md', CONTRACT_REL] + V['shared_premises']
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}

    def validate_reverse(lst):
        for item in lst:
            require(item not in V['forward_additional'], 'reverse list contains a forward-only premise ' + item)
            require('research/round32/forward/av2' not in item and 'research/round32/reverse/av2' not in item, 'reverse reads current AV2 work ' + item)
        return True
    check('reverse_premise_isolation',
          V['reverse_isolation'] is True and sorted(inventory) == sorted(set(forward_list)) and validate_reverse(reverse_list)
          and all(p in forward_list for p in V['forward_additional'])
          and rejected(lambda: validate_reverse(reverse_list + ['research/round32/skeptic/triage.md']), 'reverse_reads_triage')
          and rejected(lambda: validate_reverse(reverse_list + ['research/round32/forward/av2/report.md']), 'reverse_reads_forward_av2'),
          contract_declares_isolation=True, forward_inventory_files=str(len(inventory)), reverse_premise_count=str(len(reverse_list)),
          forward_additional_disclosed=V['forward_additional'])

    # c1_window_preview_only
    c1p = calc.c1_window_preview()
    c1_ident = all(family_identity_gaussian(sv, 2 * sv, Q(0), th) for sv in svals for th in thetas)
    c1_mod = all(cabs2(cmul(cpow(cx(sv, -th), 2), cx(sv, th))) == (sv * sv + th * th) ** 3 for sv in svals for th in thetas)
    pyth = [(Q(3), Q(4), Q(5)), (Q(5), Q(12), Q(13)), (Q(4), Q(3), Q(5)), (Q(8), Q(15), Q(17))]
    c1_anti = all(r * r == sv * sv + th * th and (r * r - th * th) / (sv * sv * r ** 3) == 1 / r ** 3 for sv, th, r in pyth)
    sq8_lo, sq8_hi = calc.sqrt_interval(Q(8))
    lgm2, _ = calc.log_positive(Q(10) ** 8)
    m2_lower = lgm2 / sq8_hi

    def validate_kernel(kernel):
        require(kernel == 'C2_frozen', 'kernel switch after D is known is rejected')
        return True
    check('c1_window_preview_only',
          c1p['preview_only'] is True and c1p['used_for_certificate'] is False and c1_ident and c1_mod and c1_anti
          and rat(c1p['negative_atom_multiplier_at_minus_one']) == V['c1_atom'] == 3
          and rat(c1p['sign_mutation_multiplier_at_minus_three']) == V['c1_sign'] == 7
          and V['c1_M0_num'] == 4 and V['c1_M1_coeff'] == 4 and m2_lower > 6
          and validate_kernel(cert_p['window']['id'])
          and rejected(lambda: validate_kernel('C1_preview'), 'kernel_switch_to_C1')
          and calc_rejects({'window': 'C1'}, 'calculator_C1_certificate')
          and calc_rejects({'window': 'poisson'}, 'calculator_poisson_certificate'),
          preview=c1p, preview_radius=dec(rat(c1p['preview_radius_upper']), 8, 'up'),
          M2_divergence='int_s^L theta^2(s^2+theta^2)^-3/2 >= 2^-3/2 log(L/s); >' + dec(m2_lower, 6, 'down') + ' at L=10^8, s=1',
          algebraic_identity='2 pi ghat_C1 = 4s^2/(a^2 b); |a^2 b|^2=(s^2+theta^2)^3')

    # missing_incoming_stars
    orth = [b for b in geo['anchors'] if all(x_ >= 0 for x_ in b)]
    n1 = len(incident_in_box(1, Rset))

    def validate_star_count(n):
        require(n == V['stars'], 'incident star count differs from seven')
        return True
    check('missing_incoming_stars',
          validate_star_count(len(geo['anchors'])) and len(orth) == 2 and n1 == 4
          and rejected(lambda: validate_star_count(len(orth)), 'orthant_two_anchors')
          and rejected(lambda: validate_star_count(n1), 'box_N1_truncated'),
          anchors=[list(map(str, b)) for b in geo['anchors']], orthant_count='2', N1_count='4 (N>=2 required)')

    # full_original_wilson_cover
    def validate_cover(nlinks, nend):
        require(nlinks == 48 and nend == 36, 'cover is not the complete 48-link, 36-endpoint R={0,e_z}')
        return True
    check('full_original_wilson_cover',
          geo['owners'] == [(0, 0, 0), (0, 0, 0), (0, 0, 1), (0, 0, 0)] and geo['R'] == [(0, 0, 0), (0, 0, 1)]
          and validate_cover(geo['cover_links'], geo['endpoints']) and geo['per_factor'] == [22, 22] and geo['shared'] == 8
          and rejected(lambda: validate_cover(geo['drawn_links'], 4), 'four_drawn_links'),
          owners='0,0,e_z,0', links='48', endpoints='36 (22 per factor, 8 shared)')

    # wrong_delta_alpha_hbar_clock
    alpha_, hbar_ = Q(5), Q(7)
    tE = Q(3, 2)
    s_clock = alpha_ * tE / hbar_
    u_clock = s_clock / 8
    wilson_G = 4 * Q(3, 4)
    wilson_delta = 8 * wilson_G

    def validate_clock(exponent_per_s, k_value):
        require(exponent_per_s == V['free_energy'], 'reference exponent differs from 3 per unit s')
        require(k_value == k_contract, 'Duhamel slope not in G=H/alpha units')
        return True
    scaled = calc.certify(alpha='5', hbar='7', E_star='3', lattice_spacing='2', fixed_design=True)
    check('wrong_delta_alpha_hbar_clock',
          wilson_G == 3 and wilson_delta == 24 and 3 * s_clock == 24 * u_clock and validate_clock(wilson_G, k_contract)
          and scaled['physical_Euclidean_time'] == '7/5' and scaled['certified_datum'] == cert_p['certified_datum']
          and rejected(lambda: validate_clock(wilson_delta, k_contract), 'exponent_24_with_s')
          and rejected(lambda: validate_clock(wilson_G, 2 * 7 * 7 * tau), 'normalized_star_norm_in_G_clock'),
          nonunit_fixture={'alpha': '5', 'hbar': '7', 't_E': '3/2', 's': s_(s_clock), 'u': s_(u_clock)},
          physical_Euclidean_time_at_s1='hbar/alpha=7/5')

    # vector_versus_scalar_centering
    m_, d_ = Q(1, 4), Q(1, 100)

    def validate_centering(residue):
        require(residue == d_ ** 2, 'scalar subtraction used as vector centering')
        return True
    check('vector_versus_scalar_centering',
          validate_centering(d_ ** 2) and -2 * m_ * d_ - d_ ** 2 == Q(-51, 10000) and m_ ** 2 == Q(1, 16)
          and rejected(lambda: validate_centering(-2 * m_ * d_ - d_ ** 2), 'scalar_as_vector'),
          vector_residue=s_(d_ ** 2), scalar_residue=s_(-2 * m_ * d_ - d_ ** 2), uncentered_residue=s_(m_ ** 2),
          av2_centering='chi=(W-m)Omega with the true mean; m^2<=D^2 charged with M_0')

    # first_order_mean_charged
    def validate_mean_square(ms):
        require(ms == M0 * D_ ** 2 and ms > 0, 'mean-square centering not charged at M_0*D^2')
        return True
    check('first_order_mean_charged',
          validate_mean_square(terms['mean_square']) and tau / 144 <= D_
          and rejected(lambda: validate_mean_square(Q(0)), 'zero_mean_assumed'),
          mean_square_term=s_(terms['mean_square']), candidate_first_order_mean_not_claimed=s_(tau / 144),
          unused_refinement='int ghat = g(0) = 1 would charge m^2 once instead of M_0 m^2; not used (frozen formula)')

    # tau_scaling_exponent
    E_cap = rat(calc.certify(tau=s_(tau))['analytic_radius'])
    E_100 = rat(calc.certify(tau=s_(tau / 100))['analytic_radius'])
    ratio = E_cap / E_100
    E4_cap = 2 * (D4_hi + D4_hi ** 2) + slope_const / pi_lo
    D4s_lo, D4s_hi = calc.sqrt_interval(Q(49, 3) * tau / 100)
    E4_100 = 2 * (2 * D4s_lo + 4 * D4s_lo ** 2) + slope_const / 100 / pi_hi
    ratio4 = E4_cap / E4_100

    def validate_linear(rv):
        require(99 <= rv <= 101, 'radius does not scale linearly in tau')
        return True
    check('tau_scaling_exponent',
          validate_linear(ratio) and Q(99, 10) <= ratio4 <= Q(101, 10)
          and rejected(lambda: validate_linear(ratio4), 'sqrt_state_bound_relabelled_linear'),
          ratio_E_tau_over_tau_100=dec(ratio, 10, 'down'), ratio_with_at4_sqrt_D=dec(ratio4, 8, 'down'))

    # changed_model_relabelled
    packet_model = {'model_id': V['model_id'], 'tau': s_(tau), 's': s_(s1), 'triple': [s_(q) for q in V['triple']],
                    'kernel': cert_p['window']['id'], 'reference_route': 'haar', 'state_provenance': V['state_provenance']}

    def validate_model(pk):
        require(pk['model_id'] == 'AQ_patterned_zero_selected', 'model id')
        require(rat(pk['tau']) == tau, 'coupling changed')
        require(rat(pk['s']) == s1, 'Euclidean node changed')
        require([rat(q) for q in pk['triple']] == [0, 0, 0], 'selected triple changed')
        require(pk['kernel'] == 'C2_frozen', 'kernel changed')
        require(pk['reference_route'] == 'haar', 'reference route changed')
        require(pk['state_provenance'] == 'AQ1_centered_whole_star_subsequence', 'state provenance changed')
        return True
    muts = []
    for key, val in (('tau', '1/100000000000000'), ('s', '1/2'), ('triple', ['0', '1/100', '0']),
                     ('reference_route', 'selected_strip'), ('model_id', 'FG(two_plaquette,1/2,24,I1.5,physical)'),
                     ('kernel', 'C1_preview'), ('kernel', 'poisson_L_4081633'), ('state_provenance', 'finite_volume_N=3')):
        mutated = dict(packet_model)
        mutated[key] = val
        muts.append(rejected(lambda m=mutated: validate_model(m), 'relabel_' + key + '_' + str(len(muts))))
    check('changed_model_relabelled', validate_model(packet_model) and len(muts) == 8, packet_model=packet_model, rejected=muts)

    # insufficient_verdict_retained
    retained = {
        'at4_poisson_L10000': {'radius_lower': s_(at4_lo), 'radius_upper': s_(at4_hi), 'target_met': False},
        'poisson_floor_D_to_0': {'floor_lower': s_(floor_lo), 'floor_upper': s_(floor_hi), 'target_met': False},
        'poisson_floor_with_admitted_D': {'floor_lower': s_(floor_with_D_lo), 'target_met': False},
        'window_with_tier_i': {'radius_lower': s_(2 * D_i + slope_const / pi_hi), 'target_met': False,
                               'label': 'limited-tier value; tier (i) is not the bound premise'},
    }

    def validate_retained(rec):
        require(rec['at4_poisson_L10000']['target_met'] is (at4_lo <= target), 'AT4 insufficiency relabelled')
        require(rec['poisson_floor_D_to_0']['target_met'] is (floor_lo <= target), 'Poisson floor relabelled')
        require(rec['window_with_tier_i']['target_met'] is (2 * D_i <= target), 'tier (i) relabelled')
        return True

    def validate_design(tv):
        require(tv == tau, 'coupling retuned after outcome')
        return True
    relab = json.loads(json.dumps(retained))
    relab['at4_poisson_L10000']['target_met'] = True
    check('insufficient_verdict_retained',
          validate_retained(retained) and validate_design(tau)
          and rejected(lambda: validate_retained(relab), 'at4_relabelled_met')
          and rejected(lambda: validate_design(Q(7784, 10 ** 12)), 'tau_retuned_to_poisson_threshold'),
          retained=retained)

    # exact_arithmetic_admission
    forbidden = ('mp' + 'math', 'num' + 'py', 'fl' + 'int', 'sym' + 'py', 'dec' + 'imal')
    own = (BASE / 'check.py').read_text(encoding='utf-8') + (BASE / 'calculator.py').read_text(encoding='utf-8')
    imports = sorted({ln.strip() for ln in own.splitlines() if ln.startswith('import ') or ln.startswith('from ')})
    check('exact_arithmetic_admission',
          not any(any(fb in ln for fb in forbidden) for ln in imports)
          and rejected(lambda: rat(1e-08), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('NaN'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator')
          and calc_rejects({'tau': 1e-8}, 'calculator_float_tau') and calc_rejects({'s': True}, 'calculator_bool_s'),
          imports=imports, decimals='outward-rounded display strings only')

    # root_n_misuse
    rss_sq = sum(v * v for v in terms.values())

    def validate_radius_sum(rv):
        require(rv == sum(terms.values(), Q(0)), 'radius is not the linear sum of the itemized terms')
        return True
    check('root_n_misuse',
          validate_radius_sum(radius) and rss_sq < radius ** 2
          and rejected(lambda: validate_radius_sum(calc.sqrt_interval(rss_sq)[1]), 'root_sum_of_squares')
          and rejected(lambda: validate_radius_sum(radius / 2), 'divided_by_sqrt_4')
          and rejected(lambda: validate_radius_sum(radius / 64), 'divided_by_64'),
          rss_preview=dec(calc.sqrt_interval(rss_sq)[1], 8, 'up'), linear_sum=dec(radius, 8, 'up'))

    # no_priority_or_continuum_claim
    claim_flags = {'continuum_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False,
                   'scientific_priority_verified': False, 'grid_claim': False,
                   'euclidean_node_certified': target_met}

    def validate_claims(fl):
        for name in ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift', 'scientific_priority_verified', 'grid_claim'):
            require(fl[name] is False, 'forbidden claim flag set: ' + name)
        require(fl['euclidean_node_certified'] is (radius <= target), 'node flag inconsistent with the radius')
        return True
    claim_muts = []
    for name in ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift', 'scientific_priority_verified', 'grid_claim'):
        fl = dict(claim_flags)
        fl[name] = True
        claim_muts.append(rejected(lambda f=fl: validate_claims(f), 'flag_' + name))
    flip = dict(claim_flags)
    flip['euclidean_node_certified'] = not target_met
    claim_muts.append(rejected(lambda: validate_claims(flip), 'node_flag_flipped'))
    check('no_priority_or_continuum_claim', validate_claims(claim_flags) and len(claim_muts) == 6,
          rejected=claim_muts, historical_or_occult_numeric_premise=False)

    # -------------------- calculator domain --------------------
    cases = [
        ('nonzero_selected', {'selected': ('0', '1/100', '0')}), ('selected_wrong_length', {'selected': ('0', '0')}),
        ('selected_float', {'selected': ('0', 0.0, '0')}), ('selected_nan', {'selected': ('0', 'NaN', '0')}),
        ('positive_cap_exceeded', {'tau': '1/10000000'}), ('negative_cap_exceeded', {'tau': '-1/10000000'}),
        ('tau_float', {'tau': 1e-8}), ('tau_bool', {'tau': True}), ('tau_nan', {'tau': 'NaN'}),
        ('tau_infinity', {'tau': 'Infinity'}), ('tau_empty', {'tau': ''}), ('tau_zero_denominator', {'tau': '1/0'}),
        ('tau_bad_separator', {'tau': '1//2'}), ('tau_object', {'tau': None}),
        ('s_zero', {'s': '0'}), ('s_negative', {'s': '-1'}), ('alpha_zero', {'alpha': '0'}), ('hbar_negative', {'hbar': '-1'}),
        ('E_star_zero', {'E_star': '0'}), ('lattice_spacing_zero', {'lattice_spacing': '0'}),
        ('target_zero', {'target': '0'}), ('target_float', {'target': 1e-6}),
        ('fixed_design_changed_tau', {'fixed_design': True, 'tau': '1/1000000000'}),
        ('fixed_design_changed_s', {'fixed_design': True, 's': '2'}),
        ('fixed_design_changed_target', {'fixed_design': True, 'target': '1/100'}),
        ('fixed_design_not_boolean', {'fixed_design': 'true'}),
        ('state_tier_unadmitted', {'state_tier': 'av1_reverse_82_face'}), ('window_switched', {'window': 'C1'}),
    ]
    rej = [calc_rejects(kw, name) for name, kw in cases]
    check('calculator_domain_rejections', len(rej) == len(cases), rejected_cases=rej)
    check('calculator_exact_input_forms',
          calc.exact(Q(1, 10), 'q') == calc.exact('0.1', 'decimal') == calc.exact('1/10', 'ratio') and calc.exact(1, 'int') == Q(1)
          and calc.certify(tau=Q(1, 10 ** 8))['certified_absolute_error'] == calc.certify(tau='0.00000001')['certified_absolute_error']
          == cert_p['certified_absolute_error'])
    check('calculator_fixed_design_matches', cert_p['fixed_design'] is True and rat(cert_p['certified_absolute_error']) == radius
          and cert_p['grid_claim'] is False and cert_p['continuum_claim'] is False,
          calculator_sha256=calc_sha)

    # -------------------- error ledger --------------------
    error_terms = {
        'state': {'value': s_(terms['state']), 'preview': dec(terms['state'], 12, 'up'),
                  'source': 'M_0*D, D the AV1 forward tier (ii) trace-distance bound; trace duality with ||W alpha^0_theta(W)||<=1 (no D/2)'},
        'mean_square': {'value': s_(terms['mean_square']), 'preview': dec(terms['mean_square'], 12, 'up'),
                        'source': 'M_0*m^2 with m^2<=D^2'},
        'kernel_dynamics': {'value': s_(terms['kernel_dynamics']), 'preview': dec(terms['kernel_dynamics'], 12, 'up'),
                            'source': 'k*M_1 = (49|tau|/4)(4s/pi) with the Machin pi lower bound; no cutoff, no tail'},
        'arithmetic': {'value': s_(terms['arithmetic']), 'preview': dec(terms['arithmetic'], 4, 'up'),
                       'source': 'half-width of the directed enclosure of e^{-3}/4 about the exact rational datum'},
    }
    check('error_terms_itemized_preregistered', sorted(error_terms) == sorted(V['error_terms']),
          terms=sorted(error_terms), not_applicable='none')

    # -------------------- packet --------------------
    headline = {
        'certified_datum': s_(datum), 'certified_absolute_error': s_(radius), 'radius_preview_up': dec(radius, 12, 'up'),
        'datum_preview': fixed(datum, 30, 'down'),
        'interval': {'lower': s_(lo_C), 'upper': s_(hi_C)},
        'interval_preview': {'lower_down': fixed(lo_C, 18, 'down'), 'upper_up': fixed(hi_C, 18, 'up')},
        'free_interval_preview': {'lower_down': fixed(f_lo, 30, 'down'), 'upper_up': fixed(f_hi, 30, 'up')},
        'width': s_(hi_C - lo_C), 'target': s_(target), 'target_met': target_met,
        'D': s_(D_), 'k': s_(k_contract), 'M0': '2', 'M1': '4s/pi', 'M2': '2s^2',
        'terms_preview_up': {kk: dec(v, 12, 'up') for kk, v in terms.items()},
    }
    packet = {
        'loop': 'AV2', 'direction': 'forward', 'human_author': 'Hruday N M (BUNZEEY)',
        'contribution_alias': 'HNM-AV2-F forward window-kernel certificate (half-line transforms)',
        'contract_sha256': CONTRACT_SHA256, 'check_py_sha256_recorded_before_evaluation': check_sha,
        'calculator_py_sha256_recorded_before_evaluation': calc_sha, 'av1_gate_sha256': G['sha256'],
        'model': packet_model, 'tau_values': {'+': s_(tau), '-': s_(V['control_tau'])},
        'window': {'definition': 'g(x)=e^{-sx} (x>=0); g(x)=e^{sx}(1-2sx+2s^2x^2) (x<0)',
                   'transform': 'ghat(theta)=4s^3/(pi(s-i theta)^3(s+i theta))', 'modulus': '(4s^3/pi)(s^2+theta^2)^-2',
                   'M0': '2', 'M1': '4s/pi', 'M2': '2s^2', 'convention': 'ghat(theta)=(2pi)^-1 int g(x)e^{-i theta x}dx; c(theta)=<chi,e^{i theta G}chi>'},
        'pi_interval': {'lower': s_(pi_lo), 'upper': s_(pi_hi)},
        'certificate_plus': cert_p, 'certificate_minus_replay': cert_m,
        'headline': headline, 'error_terms_itemized': error_terms,
        'retained_failures': retained,
        'crossover': {'s_star_lower': s_(s_star_lo), 's_star_upper': s_(s_star_hi),
                      'preview': [dec(s_star_lo, 10, 'down'), dec(s_star_hi, 10, 'up')], 'grid_claim': False},
        'c1_window_preview': c1p,
        'tau_zero_null_replay': {'window_radius': z['certified_absolute_error'], 'poisson_tail_L1e4_upper': s_(p0[L4])},
        'sub_labels': ['reference_unresolved'],
        'claim_exclusions': V['claim_exclusions'],
        'proposed_forward_verdict': 'accepted_within_scope (forward route only; the gate also needs the reverse residue route and skeptical review)',
        'routes_executed': ['forward half-line transforms and exact antiderivatives'],
        'routes_not_executed': ['reverse residue route (simple pole at theta=is, triple pole at theta=-is), assigned to the reverse producer'],
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
        validate_claims({k1: pk[k1] for k1 in claim_flags})
        require(sorted(inv) == sorted(set(forward_list)), 'premise snapshot inventory incomplete')
        recomputed = calc.certify(fixed_design=True)
        require(pk['headline']['certified_absolute_error'] == recomputed['certified_absolute_error'], 'radius differs from recomputation')
        require(pk['headline']['certified_datum'] == recomputed['certified_datum'], 'datum differs from recomputation')
        require(pk['headline']['target_met'] is recomputed['target_met'], 'target Boolean differs from recomputation')
        validate_tier(rat(pk['headline']['D']))
        validate_retained(pk['retained_failures'])
        validate_kernel(pk['model']['kernel'])
        return True

    base_packet = dict(packet)
    base_packet['checks'] = [dict(ch) for ch in CHECKS]
    base_packet['packet_sha256'] = packet_hash(base_packet)

    def rebound(edit, inv=None):
        def run():
            pk = json.loads(json.dumps(base_packet))
            edit(pk)
            pk['packet_sha256'] = packet_hash(pk)
            return validate_packet(pk, inventory if inv is None else inv)
        return run

    def flip_control(pk):
        for ch in pk['checks']:
            if ch['id'] == 'window_fourier_sign_convention':
                ch['passed'] = False

    def halve_radius(pk):
        pk['headline']['certified_absolute_error'] = s_(rat(pk['headline']['certified_absolute_error']) / 2)

    def tier_i(pk):
        pk['headline']['D'] = s_(D_i)

    def at4_met(pk):
        pk['retained_failures']['at4_poisson_L10000']['target_met'] = True

    def grid(pk):
        pk['grid_claim'] = True

    def kernel_c1(pk):
        pk['model']['kernel'] = 'C1_preview'
    inv_missing = dict(inventory)
    inv_missing.pop('research/round32/methods/paired-physics-research/SKILL.md')
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(rebound(flip_control), 'control_boolean_flipped_hash_rebound')
          and rejected(rebound(lambda pk: None, inv_missing), 'snapshot_removed_hash_rebound')
          and rejected(rebound(halve_radius), 'radius_halved_hash_rebound')
          and rejected(rebound(tier_i), 'tier_i_D_hash_rebound')
          and rejected(rebound(at4_met), 'at4_target_flipped_hash_rebound')
          and rejected(rebound(grid), 'grid_claim_hash_rebound')
          and rejected(rebound(kernel_c1), 'kernel_switch_hash_rebound'))

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in V['controls'] if cid not in ids]
    require(not missing, 'contract controls without a check: ' + ','.join(missing))
    unmutated = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch.get('rejected_mutations')]
    require(not unmutated, 'contract controls without a rejected damaging mutation: ' + ','.join(unmutated))
    require(not PENDING, 'mutation labels not attached to a check')
    packet['checks'] = CHECKS
    packet['contract_controls_covered'] = sorted(V['controls'])
    packet['check_count'] = str(len(CHECKS))
    return packet


def numbers_are_strings(obj):
    """No JSON number anywhere: every numeric value is an exact rational string."""
    if isinstance(obj, bool) or obj is None:
        return True
    if isinstance(obj, (int, float)):
        return False
    if isinstance(obj, dict):
        return all(isinstance(k, str) for k in obj) and all(numbers_are_strings(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(numbers_are_strings(v) for v in obj)
    return isinstance(obj, str)


def main():
    ap = argparse.ArgumentParser(description='AV2 forward exact checker')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    require(out.is_absolute(), 'absolute output directory required')
    out = out.resolve()
    require(not out.exists(), 'fresh (non-existent) output directory required')
    require(ROOT not in out.parents and out != ROOT, 'output directory must be outside the checkout')
    check_sha = sha(BASE / 'check.py')        # recorded before any evaluation
    calc_sha = sha(BASE / 'calculator.py')
    result = compute(check_sha, calc_sha)
    require(numbers_are_strings(result), 'non-string number in results')
    out.mkdir(parents=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    sources = {}
    for p in sorted(BASE.rglob('*')):
        rel = p.relative_to(BASE)
        require('__pycache__' not in rel.parts and p.suffix != '.pyc', 'interpreter cache inside the producer closure')
        if p.is_file() and (rel.parts[0] == 'inputs' or p.name in ('check.py', 'calculator.py', 'report.md')) and rel.parts[0] != 'output':
            sources[rel.as_posix()] = sha(p)
    manifest = {'loop': 'AV2', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AV2', 'direction': 'forward', 'checks': str(len(result['checks'])),
                      'radius_preview': result['headline']['radius_preview_up'], 'target_met': result['headline']['target_met'],
                      'euclidean_node_certified': result['euclidean_node_certified']}, sort_keys=True))


if __name__ == '__main__':
    main()
