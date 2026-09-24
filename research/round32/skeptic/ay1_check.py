#!/usr/bin/env python3
"""Round32 AY1 skeptic pre-comparison checker (zero-selected patterned family).

Written after the AY1 contract froze, from the frozen contract, the AV1, AW1,
AX1 and AX2 gates, the AM2, AQ1, AQ2 and I1 forward reports, the AV1/AW1
producer reports and the skeptic's own notes, before reading
research/round32/forward/ay1/ or research/round32/reverse/ay1/. Nothing is
imported from any producer or assistant. Standard library only. Every admission
Boolean is decided with fractions.Fraction; floats appear only in the labelled
'previews' block. Every check and control raises an explicit exception, so
python -O cannot disable it. Model-agent skeptic with correlated ancestry; not
human peer review.

What is derived here:
  * the two construction families on centered coarse cubes Lambda_N=[-N,N]^3:
    F1 = AQ1 whole-star boxes (star at b retained iff b+S in Lambda_N) and
    F2 = I1 section-6 all-contained-face boxes (face retained iff its actual
    owner set lies in Lambda_N; grouped by anchor, padded sites decoupled);
    per-site sums, supports, all-size retained-face formulas, incidence on R;
  * the AV1 tier D (reproduced from the gate) and the pair constant 2D;
  * the first-order reduced density rho^(1)_R as the R-marginal of
    -(c^(1) Omega_0^* + h.c.), face by face (82 faces meet R, 10 survive);
  * a trace-norm, R-local second-order constant K_2' from the AW1 items, and
    its comparison with the admitted K_2^+;
  * exact fixtures: fixed-vector versus moving-vector, common enclosing
    interval versus equality, uniform in N versus uniform in a;
  * a packet validator and the 21 contract controls as damaging mutations.

Usage: python3 -B research/round32/skeptic/ay1_check.py --output /absolute/fresh/dir
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
CONTRACT = ROOT / 'research/round32/contracts/ay1.json'
CONTRACT_SHA256 = 'be9b354420e66e7edba03d59b3d194b69f26782b44cfb63cb10e176bf4879ae0'
I1_REPORT = ROOT / 'research/round21/forward/i1/report.md'
AV1_GATE = ROOT / 'research/round32/advisor/av1-gate.json'
AW1_GATE = ROOT / 'research/round32/advisor/aw1-gate.json'
AX1_GATE = ROOT / 'research/round32/advisor/ax1-gate.json'

DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
R_COVER = ((0, 0, 0), (0, 0, 1))
MODEL_ID = 'AQ_patterned_zero_selected'
TOPOLOGY_STATES = 'trace norm on B(H_R)'
TOPOLOGY_DYNAMICS = 'norm on compact time windows'
CLOCK = 's=alpha*t_E/hbar, theta=alpha*t/hbar'
UNIFORM_IN = 'N (volume) at fixed spacing'
SUB_LABEL = 'uniform_local_closeness_not_uniqueness'
QBC = ('closeness bound plus a matching first-order term; not a variational statement about which '
       'boundary condition the infinite-volume theory selects')
FORBIDDEN_PHRASES = ('the aq state', 'the thermodynamic limit', 'unique ground state of the infinite',
                     'the limit state', 'boundary independent state', 'converges as n', 'uniform in a')


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


def sqrt_up(n, scale=10 ** 12):
    r = isqrt(n * scale * scale)
    up = F(r if r * r == n * scale * scale else r + 1, scale)
    if not (up * up >= n and (up - F(1, scale)) ** 2 < n):
        raise CheckFailure('sqrt upper bracket')
    return up


def sqrt_lo(n, scale=10 ** 12):
    r = isqrt(n * scale * scale)
    lo = F(r, scale)
    if not (lo * lo <= n and (lo + F(1, scale)) ** 2 > n):
        raise CheckFailure('sqrt lower bracket')
    return lo


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
                        'links': face_links(p, a, c), 'owners': owner_set(p, a, c),
                        'selected': is_selected(p, a, c)})
    return out


def omitted_faces(b):
    """Zero-selected family: selected faces carry coefficient 0, so only the 21
    omitted faces at each anchor enter V."""
    return [f for f in anchored_faces(b) if not f['selected']]


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


def whole_star_groups(n):
    """F1 (AQ1): the star at b is retained iff b+S is in Lambda_N."""
    sites = set(box(n))
    out = []
    for b in sorted(sites):
        if all(add(b, s) in sites for s in S_STAR):
            fs = omitted_faces(b)
            out.append({'anchor': b, 'faces': fs, 'support': frozenset().union(*[f['owners'] for f in fs])})
    return out


def padded_groups(n):
    """F2 (I1 section 6): at each b in Lambda_N keep the omitted faces anchored at b
    whose actual owner set lies in Lambda_N. Padded sites of B_plus carry h_b only."""
    sites = set(box(n))
    out = []
    for b in sorted(sites):
        fs = [f for f in omitted_faces(b) if f['owners'] <= sites]
        if fs:
            out.append({'anchor': b, 'faces': fs, 'support': frozenset().union(*[f['owners'] for f in fs])})
    return out


def census(groups, n):
    sites = box(n)
    keys = [(f['base'], f['orient']) for g in groups for f in g['faces']]
    if len(keys) != len(set(keys)):
        raise CheckFailure('face charged twice')
    per_site = {}
    for u in sites:
        jsum = sum((F(len(g['faces']), 3) for g in groups if u in g['support']), F(0))
        ngroups = sum(1 for g in groups if u in g['support'])
        nfaces = sum(1 for g in groups for f in g['faces'] if u in f['owners'])
        per_site[u] = (jsum, ngroups, nfaces)
    rset = set(R_COVER)
    meet = sorted((f['base'], f['orient']) for g in groups for f in g['faces'] if f['owners'] & rset)
    inside = sorted((f['base'], f['orient']) for g in groups for f in g['faces'] if f['owners'] <= rset)
    groups_r = sorted((g['anchor'], len(g['faces'])) for g in groups if g['support'] & rset)
    return {'keys': set(keys), 'per_site': per_site, 'meet': meet, 'inside': inside, 'groups_R': groups_r,
            'max_support': max(len(g['support']) for g in groups)}


def flip_parity(links):
    """E={(p,x):p_y even} u {(p,y):p_z even} u {(p,z):p_x even} (AW1 flip set)."""
    cnt = 0
    for tail, d in links:
        if (d == 'x' and tail[1] % 2 == 0) or (d == 'y' and tail[2] % 2 == 0) or (d == 'z' and tail[0] % 2 == 0):
            cnt += 1
    return cnt


def haar_mean_of_product(face_list):
    """E[prod W_f] by the per-link Z_2 centre grading: zero if some link occurs an odd
    number of times. Only the cases used here are evaluated in closed form:
    E[W_f^2]=1/4 (a face with itself) and every product with an odd link."""
    mult = {}
    for f in face_list:
        for ln in f['links']:
            mult[ln] = mult.get(ln, 0) + 1
    if any(v % 2 for v in mult.values()):
        return F(0)
    keys = sorted({(f['base'], f['orient']) for f in face_list})
    if len(face_list) == 2 and len(keys) == 1:
        return catalan_moment(2)
    raise CheckFailure('Haar product outside the closed-form cases')


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


# ---------------------------------------------------------------- constants
def exp_eighth_upper(n=12):
    x = F(1, 8)
    s = sum((x ** k / fact(k) for k in range(n + 1)), F(0))
    tail = x ** (n + 1) / fact(n + 1) / (1 - x / (n + 2))
    return s + tail


def tier_ii(abs_tau):
    """AV1 tier (ii): t_1=49a, T=t_1/(1-352J), rho=352JT, J=28|tau|, a=|tau|/144."""
    a = abs_tau / 144
    j = 28 * abs_tau
    t1 = 49 * a
    t = t1 / (1 - 352 * j)
    rho = 352 * j * t
    eps_f = 2 * t + t * t
    eps_r = 82 * a + 2 * rho + (33 * a + rho) ** 2
    return {'a': a, 'J': j, 't1': t1, 'T': t, 'rho': rho, 'eps_F': eps_f, 'eps_R': eps_r}


def d_forward(eps):
    return 2 * eps * (1 + eps) / (1 + eps * eps)


def k2_plus_skeptic(abs_tau):
    """AW1 skeptic itemization (the admitted K_2^+): rho+T*T+T^2+eps_F^2+a eps_F^2."""
    v = tier_ii(abs_tau)
    return (v['rho'] + v['T'] * v['T'] + v['T'] ** 2 + v['eps_F'] ** 2 + v['a'] * v['eps_F'] ** 2) / abs_tau ** 2


def k2_w_rlocal(abs_tau):
    """W-projected, R-local AW1 minimal form (multiplier 2||W Omega_R||=1, one sector)."""
    v = tier_ii(abs_tau)
    a, t, rho, e = v['a'], v['T'], v['rho'], v['eps_R']
    return (rho + t * (6 * a + rho) + (33 * a + rho) ** 2 + e ** 2 + a * e ** 2) / abs_tau ** 2


def k2_prime_items(abs_tau, rho_override=None, t_override=None):
    """Trace-norm, R-local second-order constant for ||rho_R-P_R-rho^(1)_R||_1:
    2||y|| + 2e^2(1+||c^(1)_R||), y = inside-R remainder + straddling + pair term,
    triangle over the three sectors {0},{e_z},{0,e_z} of H_R."""
    v = tier_ii(abs_tau)
    a = v['a']
    rho = v['rho'] if rho_override is None else rho_override
    t = v['T'] if t_override is None else t_override
    eps_r = 82 * a + 2 * rho + (33 * a + rho) ** 2
    items = {
        'am2_remainder': 2 * (2 * rho),
        'straddling': 2 * t * (72 * a + 2 * rho),
        'two_creation': 2 * (33 * a + rho) ** 2,
        'density': 2 * eps_r ** 2,
        'normalization': 2 * eps_r ** 2 * (10 * a),
    }
    return items, eps_r


def k2_prime(abs_tau):
    items, _ = k2_prime_items(abs_tau)
    return sum(items.values(), F(0)) / abs_tau ** 2


# ---------------------------------------------------------------- validator
def reference_packet(c):
    return {
        'model_id': MODEL_ID, 'triple': ['0', '0', '0'], 'tau': c['tau'], 'model_cap': F(1, 10 ** 8),
        'families': list(c['families']), 'contract_sha256': CONTRACT_SHA256,
        'topology_states': TOPOLOGY_STATES, 'topology_dynamics': TOPOLOGY_DYNAMICS, 'clock': CLOCK,
        'same_coupling': True, 'cover': list(R_COVER), 'cover_links': 48, 'cover_endpoints': 36,
        'stars_R': 7, 'incoming_groups_per_site': {'whole_star': 4, 'padded': 4},
        'J_pad_over_tau': F(28), 'J_pad_source': 'derived', 'J0': F(7, 25000000), 'max_support_pad': 4,
        'termination_order': 8, 'G_R': F(148, 7), 'Gp_R': F(352),
        'reset_R_over_tau': F(98), 'C_F_over_tau_per_site': F(56),
        'D': c['D'], 'D_source': 'AV1 gate forward tier (ii)', 'pair_constant': 2 * c['D'], 'combine': 'triangle',
        'tiers_reported': {'ii': 2 * c['D'], 'i': 2 * c['D_i']},
        'rho1_faces': 10, 'rho1_single_site_faces': 0, 'rho1_amplitude': F(1, 72),
        'rho1_amplitude_units': {'normalized': F(1, 3) / 24, 'alpha': F(1, 24) / 3},
        'rho1_trace_W_over_tau': F(1, 144), 'first_order_density_charged': True,
        'K2_bound_applies_to': 'rho_R-P_R-rho1_R', 'K2_prime': c['K2_prime'], 'K2_prime_topology': 'trace_norm',
        'K2_prime_sectors': 3, 'K2_prime_straddling_faces': 72, 'K2_prime_multiplier': 2, 'K2_prime_tier': 'ii',
        'K2_prime_vs_K2_plus': 'larger', 'difference_constant': 2 * c['K2_prime'] * c['tau'] ** 2,
        'scaling': {'pair_constant': 1, 'rho1': 1, 'second_order_difference': 2},
        'centering': 'none', 'uniform_in': UNIFORM_IN, 'sub_label': SUB_LABEL,
        'sentence': c['sentence'], 'gate_fields': dict(c['gate_fields']), 'qbc_definition': QBC,
        'statements': ['For every pair of subsequential limits of the two named families (a chosen '
                       'subsequential limit of each), the reduced densities on R are within 2D; this is not '
                       'uniqueness.'],
        'equality_inferred_from_common_interval': False, 'trace_norm_inferred_from_fixed_observables': False,
        'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False,
                   'uniform_in_a_claim': False, 'rate_in_N_claim': False},
        'verdict': 'accepted_within_scope', 'family_premises_ok': {'whole_star': True, 'padded': True},
        'reverse_inputs': list(c['reverse_inputs']),
        'error_terms': ['state_boundary', 'second_order_difference', 'arithmetic'],
    }


def validate(pk, c):
    if pk['contract_sha256'] != CONTRACT_SHA256:
        raise Rejected('contract hash')
    if pk['model_id'] != MODEL_ID or pk['triple'] != ['0', '0', '0']:
        raise Rejected('changed model relabelled')
    if abs(pk['tau']) != pk['model_cap'] or pk['model_cap'] != c['tau']:
        raise Rejected('changed model relabelled')
    if any(isinstance(v, float) for v in (pk['D'], pk['pair_constant'], pk['K2_prime'], pk['tau'],
                                          pk['difference_constant'], pk['J0'])):
        raise Rejected('exact arithmetic')
    if pk['D'] == c['D_ax1']:
        raise Rejected('changed model relabelled: AX1 uniform D')
    if pk['D_source'] != 'AV1 gate forward tier (ii)':
        raise Rejected('tier mixing: D not the AV1 admitted tier')
    if pk['D'] != c['D']:
        if pk['D'] < c['D']:
            raise Rejected('D below the admitted gate value')
        raise Rejected('tier mixing: D not the AV1 admitted tier')
    if pk['combine'] != 'triangle':
        raise Rejected('root-N or non-linear combination')
    if pk['pair_constant'] != 2 * pk['D']:
        if pk['pair_constant'] == pk['D']:
            raise Rejected('pair constant is 2D (two states, triangle)')
        raise Rejected('root-N or non-linear combination')
    if sorted(pk['tiers_reported']) != ['i', 'ii'] or pk['tiers_reported']['i'] <= c['target']:
        raise Rejected('insufficient tier not retained')
    if pk['verdict'] == 'accepted_within_scope' and not all(pk['family_premises_ok'].values()):
        raise Rejected('insufficient verdict: a family fails the premises')
    if pk['families'] != c['families'] or len(pk['families']) != 2:
        raise Rejected('two families not named')
    if pk['topology_states'] != TOPOLOGY_STATES or pk['topology_dynamics'] != TOPOLOGY_DYNAMICS:
        raise Rejected('topology not named')
    if pk['trace_norm_inferred_from_fixed_observables']:
        raise Rejected('topology: weak-* on fixed observables is not trace norm')
    if pk['clock'] != CLOCK:
        raise Rejected('common clock')
    if not pk['same_coupling']:
        raise Rejected('common clock: families compared at different couplings')
    if pk['cover'] != list(R_COVER) or pk['cover_links'] != 48 or pk['cover_endpoints'] != 36:
        raise Rejected('cover')
    if pk['stars_R'] != 7 or any(v != 4 for v in pk['incoming_groups_per_site'].values()):
        raise Rejected('incident stars')
    if pk['J_pad_source'] != 'derived':
        raise Rejected('padding family: contraction cited, not proved')
    if pk['J_pad_over_tau'] != c['J_pad_over_tau'] or pk['max_support_pad'] > 4 or pk['termination_order'] != 8:
        raise Rejected('padding family: per-site sum or support')
    if pk['J0'] != F(7, 25000000):
        raise Rejected('padding family: J_0 changed')
    if pk['J_pad_over_tau'] * c['tau'] > pk['J0']:
        raise Rejected('insufficient verdict: a family fails the premises')
    if not (pk['J0'] * pk['G_R'] < F(1, 64) and 2 * pk['J0'] * pk['Gp_R'] < 1):
        raise Rejected('padding family: AM2 contraction fails')
    if pk['reset_R_over_tau'] != 2 * 7 * 7 or pk['C_F_over_tau_per_site'] != 2 * 4 * 7:
        raise Rejected('reset budget')
    amp = pk['rho1_amplitude_units']
    if amp['normalized'] != F(1, 72) or amp['alpha'] != F(1, 72) or pk['rho1_amplitude'] != F(1, 72):
        if pk['rho1_amplitude'] == F(-1, 72):
            raise Rejected('first-order density sign')
        raise Rejected('clock or unit mixing')
    if pk['rho1_trace_W_over_tau'] != F(1, 144):
        raise Rejected('first-order density sign')
    if pk['rho1_single_site_faces'] != 0:
        raise Rejected('changed model relabelled: single-site first-order creations')
    if pk['rho1_faces'] != 10:
        raise Rejected('first-order density: straddling faces vanish under the R-marginal')
    if not pk['first_order_density_charged'] or pk['K2_bound_applies_to'] != 'rho_R-P_R-rho1_R':
        raise Rejected('first-order mean not charged')
    if pk['centering'] != 'none':
        raise Rejected('centering: observable is uncentered by contract')
    if pk['K2_prime_topology'] != 'trace_norm':
        raise Rejected('K2 prime: W-projected constant is not a density bound')
    if pk['K2_prime'] == c['K2_plus']:
        raise Rejected('K2 prime: whole-box K_2^+ reused')
    if pk['K2_prime_sectors'] != 3 or pk['K2_prime_multiplier'] != 2 or pk['K2_prime_straddling_faces'] != 72:
        raise Rejected('K2 prime: sectors, multiplier or straddling pin')
    if pk['K2_prime_tier'] != 'ii':
        raise Rejected('tier mixing')
    if pk['K2_prime_vs_K2_plus'] != 'larger' or pk['K2_prime'] <= c['K2_plus']:
        raise Rejected('K2 prime: trace-norm constant below K_2^+ from AW1 items')
    if pk['K2_prime'] < c['K2_prime']:
        raise Rejected('K2 prime below the derived value')
    if pk['difference_constant'] != 2 * pk['K2_prime'] * pk['tau'] ** 2:
        raise Rejected('root-N or non-linear combination')
    sc = pk['scaling']
    if sc != {'pair_constant': 1, 'rho1': 1, 'second_order_difference': 2}:
        raise Rejected('tau scaling exponent')
    if pk['uniform_in'] != UNIFORM_IN or pk['claims'].get('uniform_in_a_claim') is not False:
        raise Rejected('not uniform in a')
    if pk['sub_label'] != SUB_LABEL:
        raise Rejected('local closeness is not uniqueness')
    gf = pk['gate_fields']
    for key in sorted(c['gate_fields']):
        if key not in gf:
            raise Rejected('gate field missing: ' + key)
        if gf[key] is not False:
            if key == 'uniqueness_claimed':
                raise Rejected('local closeness is not uniqueness')
            if key == 'whole_sequence_claimed':
                raise Rejected('subsequence versus whole sequence')
            raise Rejected('gate field claimed: ' + key)
    if pk['sentence'] != c['sentence']:
        raise Rejected('mandatory sentence template')
    if pk['qbc_definition'] != QBC:
        raise Rejected('quantitative boundary comparison definition')
    for text in pk['statements']:
        low = text.lower()
        for bad in FORBIDDEN_PHRASES:
            if bad in low:
                raise Rejected('forbidden phrasing: ' + bad)
    if pk['equality_inferred_from_common_interval']:
        raise Rejected('subsequence versus whole sequence: common interval is not equality')
    for key in ('continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified', 'rate_in_N_claim'):
        if pk['claims'].get(key) is not False:
            raise Rejected('forbidden claim ' + key)
    inv = pk['reverse_inputs']
    if sorted(inv) != sorted(c['reverse_inputs']):
        extra = sorted(set(inv) - set(c['reverse_inputs']))
        if any(p in c['forward_only'] or '/forward/ay1/' in p for p in extra):
            raise Rejected('reverse premise isolation')
        raise Rejected('reverse premise inventory')
    for name in ('state_boundary', 'second_order_difference', 'arithmetic'):
        if name not in pk['error_terms']:
            raise Rejected('error term missing: ' + name)
    return True


# ---------------------------------------------------------------- execute
def execute():
    contract_bytes = CONTRACT.read_bytes()
    c_sha = hashlib.sha256(contract_bytes).hexdigest()
    need(c_sha == CONTRACT_SHA256, 'contract_sha256_pinned', sha256=c_sha)
    con = json.loads(contract_bytes)
    par, pre = con['parameters'], con['preregistration']
    tau_cap = F(par['tau_cap'])
    target = F(pre['target']['value'])
    need(con['status'] == 'frozen_before_production' and tau_cap == F(1, 10 ** 8) and target == F(1, 1250000)
         and pre['target']['comparator'] == '<=' and pre['model_id'] == MODEL_ID
         and pre['selected_triple_alpha_units'] == ['0', '0', '0'], 'contract_target_cap_model_read',
         tau_cap=q(tau_cap), target=q(target), target_is_twice_av1_target=(target == 2 * F(1, 2500000)))
    need(pre['tau']['signs_evaluated'] == ['+', '-'], 'contract_both_signs')
    need(con['controls'] == pre['controls_required']['ids'] and len(con['controls']) == 21
         and len(set(con['controls'])) == 21, 'contract_control_mirror', controls=21, mirror=21)
    families = list(par['families'])
    need(len(families) == 2 and 'AQ1' in families[0] and 'I1 section 6' in families[1], 'contract_two_families',
         families=families)
    gate_fields = dict(pre['gate_fields_required'])
    need(sorted(gate_fields) == sorted(['uniqueness_claimed', 'whole_sequence_claimed', 'rate_claimed',
                                        'translation_invariance_claimed', 'boundary_independence_of_dynamics_claimed'])
         and all(v is False for v in gate_fields.values()), 'contract_gate_fields_five_false', fields=sorted(gate_fields))
    sentence = pre['mandatory_sentence_template']
    need('2D' in sentence and 'agree to first order in tau' in sentence and 'does not assert equality' in sentence,
         'contract_sentence_template_read', sentence=sentence)
    reverse_inputs = sorted(['AGENTS.md', 'research/round32/contracts/ay1.json'] + list(con['shared_premises']))
    forward_only = list(con['forward_additional_premises'])
    need(con['reverse_premise_isolation'] is True and not (set(forward_only) & set(reverse_inputs))
         and len(reverse_inputs) == 30, 'contract_reverse_inventory_derivable', reverse_inputs=len(reverse_inputs),
         forward_only=forward_only)

    # 1. face classes and zero-selected counts (all sizes)
    classes = cell_classes()
    i1 = parse_i1_table()
    need(classes == i1 and sum(classes.values()) == 24, 'face_classes_match_I1_table', classes=len(classes))
    omitted_cls = {k: v for k, v in classes.items() if not k[2]}
    need(sum(omitted_cls.values()) == 21 and all(len(k[1]) >= 2 for k in omitted_cls), 'omitted_classes_21_multi_site')
    offs = {s: sum(v for k, v in omitted_cls.items() if s in k[1]) for s in S_STAR}
    per_factor = sum(offs.values())
    both_r = sum(v for k, v in omitted_cls.items() if (0, 0, 0) in k[1] and (0, 0, 1) in k[1])
    exact_r = sum(v for k, v in omitted_cls.items() if set(k[1]) == {(0, 0, 0), (0, 0, 1)})
    need(offs == {(0, 0, 0): 21, (1, 0, 0): 4, (0, 1, 0): 8, (0, 0, 1): 16} and per_factor == 49,
         'per_factor_count_49', offsets={str(k): v for k, v in sorted(offs.items())})
    meet_r_all = 2 * per_factor - both_r
    need(both_r == 16 and exact_r == 10 and meet_r_all == 82 and both_r - exact_r == 6
         and (per_factor - both_r) == 33, 'faces_meeting_R_all_sizes', meeting=82, inside=10, containing_both=16,
         strictly_containing_R=6, single_contact_per_site=33, straddling=72)
    anchors_r = sorted({sub(r, s) for r in R_COVER for s in S_STAR})
    per_anchor = {}
    for b in anchors_r:
        per_anchor[b] = sum(1 for f in omitted_faces(b) if f['owners'] & set(R_COVER))
    expect = {(0, 0, 0): 21, (0, 0, 1): 21, (0, 0, -1): 16, (-1, 0, 0): 4, (0, -1, 0): 8,
              (-1, 0, 1): 4, (0, -1, 1): 8}
    need(len(anchors_r) == 7 and per_anchor == expect and sum(per_anchor.values()) == 82,
         'whole_star_creations_meeting_R_from_7_anchors',
         rows=[{'anchor': list(k), 'faces_meeting_R': v} for k, v in sorted(per_anchor.items())])
    osets = {}
    for b in anchors_r:
        for f in omitted_faces(b):
            if f['owners'] & set(R_COVER):
                osets[f['owners']] = osets.get(f['owners'], 0) + 1
    through0 = sorted(v for o, v in osets.items() if (0, 0, 0) in o)
    need(len(osets) == 27 and sum(osets.values()) == 82 and len(through0) == 15
         and through0 == [1] * 5 + [2] * 3 + [3] * 2 + [4] * 3 + [10] * 2
         and osets[frozenset(R_COVER)] == 10, 'owner_sets_meeting_R', owner_sets=27, straddling_owner_sets=26,
         multiplicities_through_0=through0)

    # 2. the complete Wilson cover
    links = set()
    endpoints = {}
    for b in R_COVER:
        for r, s in product(range(4), range(2)):
            p = (4 * b[0] + r, 2 * b[1] + s, b[2])
            for d in ('x', 'y', 'z'):
                links.add((p, d))
                endpoints.setdefault(b, set()).update({p, add(p, DIRS[d])})
    shared = endpoints[(0, 0, 0)] & endpoints[(0, 0, 1)]
    wf = [f for f in omitted_faces((0, 0, 0)) if f['base'] == (0, 0, 0) and f['orient'] == 'xz'][0]
    need(len(links) == 48 and len(endpoints[(0, 0, 0)] | endpoints[(0, 0, 1)]) == 36
         and len(endpoints[(0, 0, 0)]) == 22 and len(shared) == 8 and wf['owners'] == frozenset(R_COVER)
         and all(ln in links for ln in wf['links']), 'wilson_cover_48_links_36_endpoints', links=48, endpoints=36,
         per_factor=22, shared=8)

    # 3. two families on centered cubes, N=1,2,3
    fam = {}
    for n in (1, 2, 3):
        ws, pd = census(whole_star_groups(n), n), census(padded_groups(n), n)
        fam[n] = (ws, pd)
        m, mm = 2 * n, 2 * n + 1
        need(len(ws['keys']) == 21 * m ** 3 and len(pd['keys']) == 14 * m * mm ** 2 + 7 * m * m * mm
             and ws['keys'] <= pd['keys'] and len(pd['keys'] - ws['keys']) == 28 * n * (5 * n + 1),
             'families_retained_faces_N%d' % n, whole_star=len(ws['keys']), padded=len(pd['keys']),
             extra_in_padded=len(pd['keys'] - ws['keys']), formula_extra='28N(5N+1)')
        for name, cz in (('whole_star', ws), ('padded', pd)):
            mx_j = max(v[0] for v in cz['per_site'].values())
            mx_g = max(v[1] for v in cz['per_site'].values())
            mx_f = max(v[2] for v in cz['per_site'].values())
            need(mx_j <= 28 and mx_g <= 4 and mx_f <= 49 and cz['max_support'] <= 4,
                 '%s_N%d_per_site_bounded_by_bulk' % (name, n), max_J_over_tau=q(mx_j), max_groups=mx_g,
                 max_faces=mx_f, max_support=cz['max_support'])
        extra_faces = pd['keys'] - ws['keys']
        fo = {}
        for g in padded_groups(n):
            for f in g['faces']:
                fo[(f['base'], f['orient'])] = f['owners']
        dmin = min(min(max(abs(x - y) for x, y in zip(o, r)) for o in fo[k] for r in R_COVER) for k in extra_faces)
        need(dmin == n - 1, 'families_differ_only_at_distance_N_minus_1_N%d' % n, linf_distance=dmin)
    ws1, pd1 = fam[1]
    need(len(ws1['meet']) == 49 and len(pd1['meet']) == 60 and ws1['inside'] == pd1['inside']
         and len(ws1['inside']) == 10, 'N1_families_differ_on_R_but_share_inside_faces', whole_star_meet=49,
         padded_meet=60, inside=10)
    for n in (2, 3):
        ws, pd = fam[n]
        need(ws['meet'] == pd['meet'] and len(ws['meet']) == 82 and ws['inside'] == pd['inside']
             and len(ws['inside']) == 10 and ws['groups_R'] == pd['groups_R'] and len(ws['groups_R']) == 7
             and all(k == 21 for _, k in ws['groups_R']), 'N%d_identical_faces_meeting_R' % n,
             faces_meeting=82, inside=10, groups_meeting_R=7)
    need(fam[3][1]['per_site'][(0, 0, 0)][0] == 28 and fam[3][0]['per_site'][(0, 0, 0)][0] == 28,
         'bulk_J_28_both_families', J_over_tau='28')
    # owner-set grouping alternative for F2 (the native NS restriction of Phi')
    j_owner = F(49, 3)
    need(j_owner * tau_cap < F(7, 25000000) and max(len(k[1]) for k in omitted_cls) == 3,
         'owner_set_grouping_alternative', J_over_tau='49/3', max_support=3, NS_crude_over_tau=q(81 * j_owner))

    # 4. AM2 contraction at the same J_0 (applies to both families)
    e8 = exp_eighth_upper()
    g_r = 16 * e8 * (1 + F(10, 64))
    gp_r = 16 * e8 * (18 + F(80, 64))
    j0 = F(7, 25000000)
    need(e8 < F(8, 7) and g_r < F(148, 7) and gp_r < 352, 'am2_majorant_bounds', exp_one_eighth_upper=q(e8))
    need(28 * tau_cap == j0 and j0 * F(148, 7) == F(37, 6250000) and F(37, 6250000) < F(1, 64)
         and 2 * j0 * 352 == F(77, 390625) and F(77, 390625) < 1, 'am2_contraction_same_J0_padded',
         J0=q(j0), J0_G=q(j0 * F(148, 7)), two_J0_Gp=q(2 * j0 * 352), J_pad_equals_J0_at_cap=True)
    need(8 * F(3, 4) == 6 and catalan_moment(2) == F(1, 4) and catalan_moment(3) == 0 and catalan_moment(4) == F(1, 8),
         'haar_onsite_gap_and_moments', onsite_gap=6, face_energy=24)

    # 5. reset budget and compactness constants (both families)
    need(2 * 7 * 7 == 98 and 98 * tau_cap <= F(1, 10 ** 6) and 4 * 98 * tau_cap <= F(1, 500) ** 2
         and F(2 * 82, 3) < 98 and 2 * 4 * 7 == 56, 'reset_budget_both_families', reset_R_over_tau=98,
         face_level_refinement_over_tau='164/3', C_F_over_tau_per_site=56, eps_R_gap6_over_tau='49/3',
         aq2_one_over_500=True)

    # 6. AV1 tier D and the pair constant 2D
    av1 = json.loads(AV1_GATE.read_text())
    d_gate = F(re.search(r'D_ii=(\d+/\d+)', av1['accepted']).group(1))
    need(d_gate == F(585079838465912592144137406066050, 42981220507576537932303142777593983768257)
         and d_gate == F(re.search(r'D_ii=(\d+/\d+)', av1['decision']).group(1)), 'av1_gate_D_read')
    v = tier_ii(tau_cap)
    need(d_forward(v['eps_F']) == d_gate and v['T'] == F(49, 14398580736) and v['rho'] == F(3773, 11248891200000000),
         'av1_D_reproduced_from_49_faces_J28', D=q(d_gate), T=q(v['T']), rho=q(v['rho']))
    pair = 2 * d_gate
    need(pair <= target, 'pair_constant_2D_meets_target', two_D=q(pair), target=q(target),
         margin_num=q(target / pair))
    t_i = 28 * tau_cap * F(148, 7)
    d_i = d_forward(2 * t_i + t_i * t_i)
    d_i_gate = F(re.search(r'D_i=(\d+/\d+)', av1['accepted']).group(1))
    need(t_i == F(37, 6250000) and d_i == d_i_gate and 2 * d_i > target, 'tier_i_2D_fails_retained',
         D_i=q(d_i), two_D_i=q(2 * d_i))
    ax1 = json.loads(AX1_GATE.read_text())
    d_ax1 = F(re.search(r"D'_ii = (\d+/\d+)", ax1['decision']).group(1))
    need(d_ax1 != d_gate and d_ax1 > d_gate, 'ax1_uniform_D_is_a_different_model', D_ax1=q(d_ax1))
    ratio_d = d_forward(tier_ii(tau_cap)['eps_F']) / d_forward(tier_ii(tau_cap / 100)['eps_F'])
    need(99 <= ratio_d <= 101, 'pair_constant_linear_scaling', ratio=preview(ratio_d))
    d_small = d_forward(tier_ii(tau_cap / 7)['eps_F'])
    need(d_small < d_gate and d_gate + d_small <= pair, 'pair_constant_holds_across_couplings',
         D_at_tau_over_7=q(d_small), note='P_R is tau-independent: states at tau and tau/7 (or -tau) are also within '
                                          '2D, so 2D alone is not a boundary comparison')

    # 7. first-order reduced density rho^(1)_R (R-marginal of -(c^(1)Omega_0^*+h.c.))
    rset = set(R_COVER)
    faces_meet = [f for b in anchors_r for f in omitted_faces(b) if f['owners'] & rset]
    inside, vanish = [], []
    for f in faces_meet:
        owners_of_links = [pi_map(tail) for tail, _ in f['links']]
        if all(o in rset for o in owners_of_links):
            inside.append(f)
        else:
            lone_outside = [ln for ln, o in zip(f['links'], owners_of_links) if o not in rset]
            if not lone_outside:
                raise CheckFailure('straddling face without an outside link')
            vanish.append(f)
    need(len(inside) == 10 and len(vanish) == 72 and all(f['anchor'] == (0, 0, 0) for f in inside),
         'rho1_R_marginal_keeps_10_of_82', surviving=10, vanishing_straddling=72,
         surviving_faces=[{'base': list(f['base']), 'orient': f['orient']} for f in
                          sorted(inside, key=lambda f: (f['orient'], f['base']))])
    xz = sorted((f['r'], f['s']) for f in inside if f['orient'] == 'xz')
    yz = sorted((f['r'], f['s']) for f in inside if f['orient'] == 'yz')
    need(xz == [(r, s) for r in range(3) for s in range(2)] and yz == [(r, 0) for r in range(4)],
         'rho1_faces_classes', xz_r_le_2_all_s=6, yz_s_0_all_r=4)
    pair_zero = all(haar_mean_of_product([f, g]) == 0 for f in faces_meet for g in faces_meet
                    if (f['base'], f['orient']) != (g['base'], g['orient']))
    need(pair_zero and all(haar_mean_of_product([f, f]) == F(1, 4) for f in inside), 'face_vectors_orthogonal_norm_half',
         pairs_checked=82 * 81)
    kappa = F(1, 72)  # coefficient of |W_f Omega_R><Omega_R| per unit tau: -(c^(1)) with c^(1)=-(tau/72) sum W_f Omega_0
    mean_f = [haar_mean_of_product([f]) for f in faces_meet]
    need(all(m == 0 for m in mean_f), 'face_haar_means_zero', faces=len(mean_f),
         consequence='Tr rho1=P rho1 P=0; Q rho1 Q=0 by the rank-two form')
    tr_w = sum(2 * kappa * haar_mean_of_product([wf, f]) for f in inside)
    tr_w2 = sum(2 * kappa * haar_mean_of_product([wf, wf, f]) for f in inside)
    norm_sq = sum(kappa ** 2 * F(1, 4) for _ in inside)
    need(tr_w == F(1, 144) and tr_w2 == 0 and norm_sq == F(10, 20736), 'rho1_explicit_values',
         trace_rho1_W_over_tau='1/144', trace_rho1_W2=0, norm_sq_x_over_tau2='10/20736',
         rho1_trace=0, P_rho1_P=0, Q_rho1_Q=0)
    aw1 = json.loads(AW1_GATE.read_text())
    need('+tau/144' in aw1['accepted'] and 'c^(1)=L_0=-(tau/72) sum W_f Omega_0' in aw1['accepted'],
         'aw1_first_order_convention_read')
    s10_lo, s10_hi = sqrt_lo(10), sqrt_up(10)
    tn_lo, tn_hi = 2 * s10_lo * tau_cap / 144, 2 * s10_hi * tau_cap / 144
    need(tn_lo < tn_hi and tn_hi <= 20 * tau_cap / 144, 'rho1_trace_norm_sqrt10_over_72',
         trace_norm_bracket=[q(tn_lo), q(tn_hi)], triangle='5|tau|/36')
    need(-kappa * 2 * F(1, 4) == -F(1, 144), 'rho1_wrong_sign_gives_minus_1_144')
    need(all(flip_parity(f['links']) % 2 == 1 for f in faces_meet), 'rho1_odd_under_flip',
         note='U_{E cap R} rho1(tau) U* = -rho1(tau) = rho1(-tau)')
    for n in (1, 2, 3):
        for name, cz in zip(('whole_star', 'padded'), fam[n]):
            if sorted((f['base'], f['orient']) for f in inside) != cz['inside']:
                raise CheckFailure('inside faces differ in %s N=%d' % (name, n))
    need(True, 'rho1_identical_in_both_families_every_N', N=[1, 2, 3])

    # 8. R-local trace-norm K_2' and comparison with K_2^+
    k2p_gate = F(re.search(r'K_2\^\+=(\d+/\d+)', aw1['accepted']).group(1))
    need(k2_plus_skeptic(tau_cap) == k2p_gate, 'aw1_K2_plus_reproduced', K2_plus=q(k2p_gate))
    items, eps_r = k2_prime_items(tau_cap)
    k2 = k2_prime(tau_cap)
    need(all(x > 0 for x in items.values()) and k2 > k2p_gate and 3 * k2p_gate < k2 < 4 * k2p_gate,
         'K2_prime_trace_norm_R_local', K2_prime=q(k2), items_over_tau2={k: q(x / tau_cap ** 2) for k, x in items.items()},
         eps_R=q(eps_r))
    kw = k2_w_rlocal(tau_cap)
    need(kw < k2p_gate and k2p_gate - kw < F(1, 3) and k2p_gate - kw > F(3, 10), 'K2_W_projected_R_local_below_K2_plus',
         K2_W=q(kw), difference=q(k2p_gate - kw))
    rho_floor = 2 * v['rho'] / tau_cap ** 2
    t_s = v['t1'] / (1 - 288 * v['J'] / (1 - 8 * t_i))
    rho_sharp = 288 * v['J'] * t_s / (1 - 8 * t_i)
    need(rho_floor > k2p_gate and 2 * rho_sharp / tau_cap ** 2 > k2p_gate, 'any_trace_norm_K2_from_AW1_items_exceeds_K2_plus',
         floor_2rho=q(rho_floor), floor_2rho_sharp_majorant=q(2 * rho_sharp / tau_cap ** 2))
    s2_hi = sqrt_up(2)
    k2_s2 = (2 * s2_hi * v['rho'] + items['straddling'] + items['two_creation'] + items['density']
             + items['normalization']) / tau_cap ** 2
    need(k2p_gate < k2_s2 < k2, 'K2_prime_sector_orthogonal_variant', K2_prime_sqrt2_upper=q(k2_s2))
    diff = 2 * k2 * tau_cap ** 2
    need(diff < pair and diff < 2 * tn_lo, 'second_order_difference_below_2D_and_first_order',
         two_K2_prime_tau2=q(diff))
    ratio_k2 = (k2_prime(tau_cap) * tau_cap ** 2) / (k2_prime(tau_cap / 100) * (tau_cap / 100) ** 2)
    need(9900 <= ratio_k2 <= 10100 and k2_prime(tau_cap / 100) <= k2, 'K2_prime_quadratic_and_monotone',
         ratio=preview(ratio_k2))
    k2_crude, _ = k2_prime_items(tau_cap, rho_override=28 * tau_cap * (F(148, 7) - 16), t_override=t_i)
    need(sum(k2_crude.values(), F(0)) / tau_cap ** 2 > 1000 * k2, 'K2_prime_tier_mixing_visible')
    d1 = tn_hi + k2 * tau_cap ** 2
    need(d1 < d_gate and d_gate / d1 > 30, 'first_order_resolved_tier_labelled', D1_upper=q(d1),
         label='labelled observation, not the admitted AV1 tier')
    sep_lo = 2 * tn_lo - 2 * k2 * tau_cap ** 2
    need(sep_lo > 0 and 2 * tn_hi + 2 * k2 * tau_cap ** 2 <= pair, 'plus_minus_tau_states_certifiably_distinct_within_2D',
         lower=q(sep_lo))
    w_sep = 2 * (tau_cap / 144 - k2p_gate * tau_cap ** 2)
    need(w_sep > 0 and tau_cap / 144 + k2p_gate * tau_cap ** 2 <= d_gate, 'wilson_means_distinct_in_common_interval',
         lower=q(w_sep))

    # 9. exact fixtures: fixed vs moving vector, common interval, uniform in N vs a
    fixed_rows = []
    prev = None
    for n in (10, 100, 1000):
        moving_sq = (F(-1) - 1) ** 2  # ||U(pi/n)e_n-e_n||^2=|e^{i pi}-1|^2, cos(pi)=-1 exactly
        fixed_sq_upper = (F(16, 5) / n) ** 2  # ||U(pi/n)e_1-e_1||^2=2-2cos(pi/n)<=(pi/n)^2, pi<16/5
        if not (moving_sq == 4 and fixed_sq_upper < moving_sq / 10 and (prev is None or fixed_sq_upper < prev)):
            raise CheckFailure('fixed versus moving vector')
        prev = fixed_sq_upper
        fixed_rows.append({'n': n, 'moving_dist_sq': q(moving_sq), 'fixed_dist_sq_upper': q(fixed_sq_upper)})
    need(True, 'fixed_vector_versus_moving_vector', rows=fixed_rows,
         model='U(t)e_j=e^{ijt}e_j on l2(N), t=pi/n; strong continuity, no norm continuity')
    dd = F(1, 10)
    dens = lambda n, size: [1 - dd / 2 if j == 0 else (dd / 2 if j == n else F(0)) for j in range(size)]
    r5, r7 = dens(5, 9), dens(7, 9)
    tn57 = sum(abs(x - y) for x, y in zip(r5, r7))
    need(tn57 == dd and r5[0] == r7[0] and sum(r5) == 1, 'moving_vector_mass_escape',
         pairwise_trace_distance=q(tn57), weak_limit_mass=q(1 - dd / 2))
    x_p, x_m = tau_cap / 144, -tau_cap / 144
    need(abs(x_p) <= d_gate and abs(x_m) <= d_gate and x_p != x_m and abs(x_p - x_m) <= 2 * d_gate,
         'common_enclosing_interval_is_not_equality')
    need(96 / F(32) == 3 and 96 / F(9600000000) == tau_cap and 96 / F(9599999999) > tau_cap,
         'uniform_in_N_not_uniform_in_a', note='D, rho1, K2_prime have no N; every a->0, g->0 path leaves |tau|<=10^-8')

    # 10. validator and the 21 contract controls
    ctx = {'tau': tau_cap, 'families': families, 'D': d_gate, 'D_i': d_i, 'D_ax1': d_ax1, 'target': target,
           'K2_prime': k2, 'K2_plus': k2p_gate, 'J_pad_over_tau': F(28), 'sentence': sentence,
           'gate_fields': gate_fields, 'reverse_inputs': reverse_inputs, 'forward_only': forward_only}
    base = reference_packet(ctx)
    need(validate(base, ctx), 'reference_packet_accepted')

    def mut(**kw):
        pk = dict(base)
        for key in ('claims', 'gate_fields', 'incoming_groups_per_site', 'tiers_reported', 'rho1_amplitude_units',
                    'scaling', 'family_premises_ok'):
            pk[key] = dict(base[key])
        for k, val in kw.items():
            if '.' in k:
                head, tail = k.split('.', 1)
                pk[head][tail] = val
            else:
                pk[k] = val
        return lambda: validate(pk, ctx)

    ok = [('reference packet', lambda: validate(base, ctx))]
    control('missing_incoming_stars', [('orthant two anchors', mut(stars_R=2), 'incident stars'),
                                       ('outgoing padded group only', mut(**{'incoming_groups_per_site.padded': 1}),
                                        'incident stars')], ok)
    control('full_original_wilson_cover', [('R={0}', mut(cover=[(0, 0, 0)]), 'cover'),
                                           ('four drawn links', mut(cover_links=4), 'cover')], ok)
    control('wrong_delta_alpha_hbar_clock', [('clock u=s/8', mut(clock='u=s/8'), 'common clock'),
                                             ('amplitude tau/9', mut(**{'rho1_amplitude_units.normalized': F(1, 9)}),
                                              'clock or unit mixing'),
                                             ('amplitude tau/576', mut(**{'rho1_amplitude_units.alpha': F(1, 576)}),
                                              'clock or unit mixing')], ok)
    m_a, m_b = F(1, 100), F(3, 100)
    residue = (m_a - m_b) ** 2
    control('vector_versus_scalar_centering', [('vector centering', mut(centering='vector'), 'centering'),
                                               ('scalar centering', mut(centering='scalar'), 'centering')], ok,
            moving_mean_residue=q(residue), note='centering with the other state\'s mean adds (m-m\')^2')
    control('first_order_mean_charged', [('rho1 dropped', mut(first_order_density_charged=False), 'first-order mean'),
                                         ('K2 on rho-P_R', mut(K2_bound_applies_to='rho_R-P_R'), 'first-order mean')], ok)
    control('tau_scaling_exponent', [('K2 term linear', mut(scaling={'pair_constant': 1, 'rho1': 1,
                                                                     'second_order_difference': 1}), 'tau scaling'),
                                     ('2D quadratic', mut(scaling={'pair_constant': 2, 'rho1': 1,
                                                                   'second_order_difference': 2}), 'tau scaling')], ok)
    control('changed_model_relabelled', [('tau 1e-14', mut(tau=F(1, 10 ** 14), model_cap=F(1, 10 ** 14)), 'changed model'),
                                         ('uniform triple', mut(triple=['tau/24', 'tau/24', 'tau/24']), 'changed model'),
                                         ('AX1 D prime', mut(D=d_ax1, pair_constant=2 * d_ax1), 'AX1 uniform D'),
                                         ('single-site creations', mut(rho1_single_site_faces=6), 'single-site')], ok)
    control('coherent_evidence_tampering', [('rehashed contract', mut(contract_sha256='0' * 64), 'contract hash'),
                                            ('smaller D', mut(D=d_gate - F(1, 10 ** 30),
                                                              pair_constant=2 * (d_gate - F(1, 10 ** 30))), 'D below'),
                                            ('smaller K2', mut(K2_prime=k2 - F(1, 10 ** 6),
                                                               difference_constant=2 * (k2 - F(1, 10 ** 6)) * tau_cap ** 2),
                                             'K2 prime below')], ok)
    control('insufficient_verdict_retained', [('tier i dropped', mut(tiers_reported={'ii': 2 * d_gate}), 'insufficient tier'),
                                              ('tier i retuned to pass', mut(tiers_reported={'ii': 2 * d_gate, 'i': target}),
                                               'insufficient tier'),
                                              ('failing family accepted', mut(**{'family_premises_ok.padded': False}),
                                               'insufficient verdict')], ok)
    control('exact_arithmetic_admission', [('float D', mut(D=float(d_gate)), 'exact arithmetic'),
                                           ('float K2', mut(K2_prime=float(k2)), 'exact arithmetic')], ok)
    control('root_n_misuse', [('sqrt2 D', mut(combine='rss'), 'root-N'),
                              ('D alone', mut(pair_constant=d_gate), 'pair constant is 2D'),
                              ('sqrt2 K2', mut(difference_constant=k2 * tau_cap ** 2 * F(1414, 1000)), 'root-N')], ok)
    control('no_priority_or_continuum_claim',
            [('continuum', mut(**{'claims.continuum_claim': True}), 'forbidden claim continuum_claim'),
             ('weak', mut(**{'claims.weak_coupling_claim': True}), 'forbidden claim weak_coupling_claim'),
             ('priority', mut(**{'claims.scientific_priority_verified': True}), 'forbidden claim scientific_priority'),
             ('rate', mut(**{'claims.rate_in_N_claim': True}), 'forbidden claim rate_in_N')], ok)
    control('topology_named', [('weak-* states', mut(topology_states='weak-* on fixed observables'), 'topology'),
                               ('one topology', mut(topology_dynamics=TOPOLOGY_STATES), 'topology'),
                               ('fixed observables to trace norm', mut(trace_norm_inferred_from_fixed_observables=True),
                                'weak-*')], ok, fixture='fixed_vector_versus_moving_vector')
    control('two_families_named', [('one family', mut(families=families[:1]), 'two families'),
                                   ('orthant substituted', mut(families=[families[0], 'orthant boxes']), 'two families')], ok)
    control('subsequence_versus_whole_sequence',
            [('whole sequence', mut(**{'gate_fields.whole_sequence_claimed': True}), 'subsequence'),
             ('equality from interval', mut(equality_inferred_from_common_interval=True), 'common interval'),
             ('the limit state', mut(statements=['The limit state is boundary independent.']), 'forbidden phrasing')],
            ok, fixture='common_enclosing_interval_is_not_equality')
    control('local_closeness_not_uniqueness',
            [('uniqueness', mut(**{'gate_fields.uniqueness_claimed': True}), 'not uniqueness'),
             ('sub-label', mut(sub_label='uniqueness'), 'not uniqueness'),
             ('the AQ state', mut(statements=['The AQ state is identified.']), 'forbidden phrasing')], ok)
    control('common_clock', [('u clock', mut(clock='u=delta*t/hbar'), 'common clock'),
                             ('different couplings', mut(same_coupling=False), 'different couplings')], ok)
    control('tier_mixing_rejected', [('D_rev labelled as admitted', mut(D_source='AV1 reverse 82-face'), 'tier mixing'),
                                     ('D_i + D_ii', mut(D=(d_gate + d_i) / 2, pair_constant=d_gate + d_i), 'tier mixing'),
                                     ('crude K2', mut(K2_prime_tier='crude'), 'tier mixing')], ok)
    control('reverse_premise_isolation',
            [('triage in reverse', mut(reverse_inputs=reverse_inputs + ['research/round32/skeptic/triage.md']),
              'reverse premise isolation'),
             ('forward AY1 read', mut(reverse_inputs=reverse_inputs + ['research/round32/forward/ay1/report.md']),
              'reverse premise isolation')], ok, scope='synthetic inventory from the contract; producer inventories '
                                                   'are checked at post-comparison')
    control('padding_family_contraction_proved',
            [('cited AM2', mut(J_pad_source='cited_AM2_whole_star'), 'contraction cited'),
             ('one group', mut(J_pad_over_tau=F(7)), 'per-site sum'),
             ('support five', mut(max_support_pad=5), 'per-site sum or support'),
             ('J_pad above J_0', mut(J_pad_over_tau=F(29)), 'per-site sum'),
             ('AX1 J_0 prime', mut(J0=F(29, 10 ** 8)), 'J_0 changed')], ok)
    control('not_uniform_in_a', [('uniform in a', mut(uniform_in='N and a'), 'not uniform in a'),
                                 ('flag', mut(**{'claims.uniform_in_a_claim': True}), 'not uniform in a'),
                                 ('phrase', mut(statements=['The bound is uniform in a.']), 'forbidden phrasing')], ok)
    # extra controls (not contract ids)
    control('rho1_straddling_faces_vanish', [('82 faces', mut(rho1_faces=82), 'straddling faces vanish'),
                                             ('27 owner sets', mut(rho1_faces=27), 'straddling faces vanish')], ok)
    control('rho1_sign_convention', [('minus tau/72', mut(rho1_amplitude=F(-1, 72)), 'first-order density sign'),
                                     ('minus tau/144 readout', mut(rho1_trace_W_over_tau=F(-1, 144)),
                                      'first-order density sign')], ok)
    control('K2_prime_not_K2_plus', [('K2+ reused', mut(K2_prime=k2p_gate, difference_constant=2 * k2p_gate * tau_cap ** 2),
                                      'whole-box K_2^+ reused'),
                                     ('W-projected', mut(K2_prime_topology='W_only'), 'W-projected'),
                                     ('six straddling faces', mut(K2_prime_straddling_faces=6), 'straddling pin'),
                                     ('smaller than K2+', mut(K2_prime_vs_K2_plus='smaller'), 'below K_2^+')], ok)
    control('mandatory_sentence_and_gate_fields',
            [('sentence edited', mut(sentence=sentence.replace('does not assert', 'asserts')), 'mandatory sentence'),
             ('translation invariance missing', mut(gate_fields={k: False for k in gate_fields
                                                                 if k != 'translation_invariance_claimed'}),
              'gate field missing'),
             ('dynamics boundary independence', mut(**{'gate_fields.boundary_independence_of_dynamics_claimed': True}),
              'gate field claimed')], ok)
    control('quantitative_boundary_comparison_defined',
            [('variational', mut(qbc_definition='the infinite-volume theory selects the whole-star boundary'),
              'quantitative boundary comparison')], ok)

    ids = set(con['controls'])
    done = {row['id'] for row in CHECKS if row.get('kind') == 'control'}
    missing = sorted(ids - done)
    need(not missing, 'contract_controls_covered', implemented=len(ids & done), of=len(ids), deferred=missing)

    return {
        'loop': 'AY1', 'stage': 'pre_comparison', 'reviewer': 'skeptic (model agent, correlated ancestry)',
        'human_author': 'Hruday N M (BUNZEEY)', 'contract_sha256': c_sha, 'contract_frozen_at': con['frozen_at'],
        'model': MODEL_ID + ': SU(2) Kogut-Susskind form on Z^3 at fixed spacing, 24-link factors, selected triple '
                 '(0,0,0), Haar reference, 21 omitted faces per anchor with -(tau/3)W_f (I1.5); both signs '
                 '|tau|<=10^-8; cover R={0,e_z}; families F1 (AQ1 whole-star) and F2 (I1 section 6 '
                 'all-contained-face with padding) on centered cubes [-N,N]^3',
        'families': {
            'F1_whole_star': {'retained_faces': '21(2N)^3', 'J_over_tau': '28', 'max_support': 4},
            'F2_padded': {'retained_faces': '14(2N)(2N+1)^2+7(2N)^2(2N+1)', 'extra_faces': '28N(5N+1)',
                          'J_over_tau': '28 (anchor grouping) or 49/3 (owner-set grouping)', 'max_support': 4,
                          'padding': 'B_plus=union(b+S); padded sites carry h_b only; rho_R unchanged'},
            'faces_meeting_R_N1': {'F1': 49, 'F2': 60}, 'faces_meeting_R_N_ge_2': 82,
            'first_differing_face_linf_distance_from_R': 'N-1',
        },
        'counts': {'per_factor': 49, 'faces_meeting_R': 82, 'inside_R': 10, 'containing_both': 16,
                   'strictly_containing_R': 6, 'single_contact_per_site': 33, 'straddling': 72,
                   'owner_sets_meeting_R': 27, 'stars_meeting_R': 7, 'cover_links': 48, 'cover_endpoints': 36},
        'contraction': {'J0': q(j0), 'J0_G': q(j0 * F(148, 7)), 'two_J0_Gp': q(2 * j0 * 352),
                        'J_pad_over_tau': '28', 'termination_order': 8},
        'reset': {'omega_hR_over_tau': '98', 'C_F_over_tau_per_site': '56', 'face_level_refinement': '164/3'},
        'pair_constant': {'D': q(d_gate), 'two_D': q(pair), 'target': q(target), 'two_D_i': q(2 * d_i),
                          'D_ax1_not_used': q(d_ax1)},
        'first_order_density': {
            'formula': 'rho1_R = (tau/72) sum_{f in F_R} (|W_f Omega_R><Omega_R| + |Omega_R><W_f Omega_R|)',
            'faces': 10, 'faces_meeting_R_vanishing': 72, 'single_site_sectors': 0,
            'norm_x': 'sqrt(10)|tau|/144', 'trace_norm': 'sqrt(10)|tau|/72',
            'trace_norm_bracket_at_cap': [q(tn_lo), q(tn_hi)], 'trace_W': '+tau/144', 'trace_W2': '0',
            'blocks': 'off-diagonal only (P rho1 P = Q rho1 Q = 0)'},
        'second_order': {'K2_prime': q(k2), 'items_over_tau2': {k: q(x / tau_cap ** 2) for k, x in items.items()},
                         'K2_plus_gate': q(k2p_gate), 'K2_W_projected_R_local': q(kw),
                         'K2_prime_sqrt2_sector_variant_upper': q(k2_s2), 'floor_2rho': q(rho_floor),
                         'two_K2_prime_tau2': q(diff), 'first_order_resolved_tier_upper': q(d1),
                         'plus_minus_tau_separation_lower': q(sep_lo)},
        'gate_fields': dict(gate_fields), 'sentence': sentence, 'qbc_definition': QBC,
        'topology': {'states': TOPOLOGY_STATES, 'dynamics': TOPOLOGY_DYNAMICS, 'clock': CLOCK},
        'error_terms': {
            'state_boundary': '2D with D the AV1 gate forward tier (ii); holds for any pair of limits of F1, F2',
            'second_order_difference': '2 K2_prime tau^2 after subtracting the common rho1_R',
            'arithmetic': 'not_applicable: exact rationals; sqrt(10), sqrt(2) as directed brackets'},
        'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False,
                   'uniform_in_a_claim': False, 'rate_in_N_claim': False},
        'deferred_controls': {}, 'deferred_parts': {
            'reverse_premise_isolation': 'executed on a synthetic inventory derived from the contract; the actual '
                                         'producer inventories are checked at post-comparison'},
        'checks': CHECKS,
        'previews': {'D': preview(d_gate), 'two_D': preview(pair), 'target_over_two_D': preview(target / pair),
                     'two_D_i': preview(2 * d_i), 'rho1_trace_norm': preview(tn_hi), 'K2_prime': preview(k2),
                     'K2_prime_over_K2_plus': preview(k2 / k2p_gate), 'K2_plus': preview(k2p_gate),
                     'K2_W_projected': preview(kw), 'K2_prime_sqrt2_variant': preview(k2_s2),
                     'two_K2_prime_tau2': preview(diff), 'two_D_over_two_K2_prime_tau2': preview(pair / diff),
                     'first_order_resolved_tier': preview(d1), 'D_over_first_order_tier': preview(d_gate / d1),
                     'plus_minus_separation_lower': preview(sep_lo), 'pair_constant_scaling_ratio': preview(ratio_d),
                     'K2_scaling_ratio': preview(ratio_k2)},
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
    print(json.dumps({'checks': len(result['checks']), 'two_D': result['previews']['two_D'],
                      'K2_prime': result['previews']['K2_prime'], 'rho1_trace_norm': result['previews']['rho1_trace_norm']}))


if __name__ == '__main__':
    main()
