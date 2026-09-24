#!/usr/bin/env python3
"""Round33 BA2 skeptic pre-comparison checker (zero-selected patterned family).

Written after the BA2 contract froze (sha256 275ba3b0...), from the frozen
contract, advisor/selection-ba2.md, advisor/deliberation-2.md (recorded loop-1
previews), advisor/plan.json, the committed Nachtergaele-Sims excerpt
research/round33/sources/nachtergaele-sims-1410.8174v1.md and the premises
(AQ1, AM2, AY1, AY2, I1 reports and gates; Round29 source dictionary, bindings
and AQ1 review), before reading research/round33/forward/ba2/ or
research/round33/reverse/ba2/. Nothing is imported from any producer, lens or
tool. Standard library only. Every admission Boolean is decided with
fractions.Fraction and directed exponential enclosures; floats appear only in
the labelled 'previews' block. Every check and control raises an explicit
exception, so python -O cannot disable it. Model-agent skeptic with correlated
ancestry; not human peer review. Human project author: Hruday N M (BUNZEEY).

What is derived here:
  * the face classes of the coarse factor lattice from fine coordinates
    (Euclidean division), cross-checked against the I1 table; per-site pins
    49 faces / 15 owner sets / 4 incident stars, 82 faces meeting R, 10 inside R;
  * F1 (AQ1 whole-star boxes) and F2 (I1 section 6 all-contained-face boxes,
    padding factored out) on Lambda_N for N = 2..5: counts, the 28N(5N+1)
    extra faces, their classes, owners, l1 distances and exact F-weighted
    distance sums; the all-size class argument;
  * the Nachtergaele-Sims instance (Theorem 3.1, eq. (51)-(52)) with
    F(r)=(1+r)^-4, C<=224, ||Phi||_F<=2268|tau| (whole stars) and
    ||Phi'||_F<=1323|tau| (owner sets), monotonicity in C and ||Phi||;
  * the Duhamel comparison coefficient with the inner F1 evolution (forward)
    and the inner F2 evolution (reverse), the within-family Cauchy coefficients
    over all M > N, the identification of the F2 limit dynamics, tau/100 ratios
    and the reconciliation of the two recorded loop-1 previews;
  * exact fixtures for every contract trap and a packet validator that executes
    the 35 contract controls (and extras) as damaging mutations.

Usage: python3 -B research/round33/skeptic/ba2_check.py --output /absolute/fresh/dir
"""
import argparse
import copy
import hashlib
import json
import re
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = 'research/round33/contracts/ba2.json'
CONTRACT_SHA256 = '275ba3b002529b7295d0f8b91dc1cc7a96451e3c7f936ee698a932fdca54fcff'
NS_EXCERPT_REL = 'research/round33/sources/nachtergaele-sims-1410.8174v1.md'
NS_EXCERPT_SHA256 = '6a28f4cd6aa2c55286fa839d83c00356ff0709f8b02027ee5b39050df1d6c921'
NS_PDF_SHA256 = '501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba'
BINDINGS_REL = 'research/round29/experts/aq-primary-bindings.json'
GATES = {  # admitted gates read by this program, sha256 pinned (hash_binding.admitted_gate_sha256_pinned_in_check_py)
    'research/round29/advisor/aq1-gate.json': 'b4a93fd49413857af83c969de1e7b2c8a698ea8099aa9e3aea8e8c7fab0a225e',
    'research/round29/advisor/am2-gate.json': 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d',
    'research/round32/advisor/ay1-gate.json': 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
}
REPORT_BINDINGS = (  # (report, gate that binds it)
    ('research/round29/forward/aq1/report.md', 'research/round29/advisor/aq1-gate.json'),
    ('research/round32/reverse/ay1/report.md', 'research/round32/advisor/ay1-gate.json'),
    ('research/round32/forward/ay1/report.md', 'research/round32/advisor/ay1-gate.json'),
    ('research/round21/forward/i1/report.md', 'research/round32/advisor/ay1-gate.json'),
    ('research/round32/forward/ay2/report.md', 'research/round32/advisor/ay2-gate.json'),
)
DELIBERATION_REL = 'research/round33/advisor/deliberation-2.md'  # skeptic-only source of the recorded previews
DELIBERATION_SHA256 = '4bbb280e666e3844138785855620572c56ba47882eef39719def3dc4845851ea'
PHRASE_SCAN_MIRRORED_SHA256 = '028af4c14edbb2fae096a91cb723ccefb036e7550088907ef47062774871f67c'
FREEZER_MIRRORED_SHA256 = 'a33517170edb2ef9f8a1aada0e45b30f837482f3c29958e0c332dee4bea2b923'

# Producer input inventories, recorded by the skeptic on 2026-09-24 with `find` over
# research/round33/{forward,reverse}/ba2/inputs (file names only) and a sha256 comparison of each
# snapshot with the repository file: all 29 identical, for both producers. This program does not
# open those folders; it checks the recorded list against the contract-derived inventory.
OBSERVED_INPUTS = {
    'forward': 'same 29 paths as reverse, every snapshot byte-identical to the repository',
    'reverse': [
        'AGENTS.md',
        'research/round21/forward/i1/report.md',
        'research/round29/advisor/am2-gate.json',
        'research/round29/advisor/aq1-gate.json',
        'research/round29/experts/aq-primary-bindings.json',
        'research/round29/experts/aq-source-dictionary.md',
        'research/round29/forward/am2/report.md',
        'research/round29/forward/aq1/report.md',
        'research/round29/forward/aq2/report.md',
        'research/round29/reverse/am2/report.md',
        'research/round29/skeptic/am2.md',
        'research/round29/skeptic/aq1.md',
        'research/round32/advisor/av1-gate.json',
        'research/round32/advisor/ay1-gate.json',
        'research/round32/advisor/ay2-gate.json',
        'research/round32/forward/av1/report.md',
        'research/round32/forward/ay1/report.md',
        'research/round32/forward/ay2/report.md',
        'research/round32/reverse/av1/report.md',
        'research/round32/reverse/ay1/report.md',
        'research/round33/advisor/selection-ba2.md',
        'research/round33/contracts/ba2.json',
        'research/round33/methods/historical-physics-panel/SKILL.md',
        'research/round33/methods/newton-analysis-synthesis/SKILL.md',
        'research/round33/methods/paired-physics-research/SKILL.md',
        'research/round33/methods/paired-physics-research/references/complete-residual-and-error-scope.md',
        'research/round33/methods/qeg-research-advisor/references/round32-state-lemma-and-window.md',
        'research/round33/methods/tesla-mechanism-resonance/SKILL.md',
        'research/round33/sources/nachtergaele-sims-1410.8174v1.md',
    ],
}

MODEL_ID = 'AQ_patterned_zero_selected'
E = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
R_COVER = [(0, 0, 0), (0, 0, 1)]
E_Z = (0, 0, 1)
ORIGIN = (0, 0, 0)
CLOCK = 'theta=alpha*t/hbar (s=alpha*t_E/hbar Euclidean); u=theta/8=delta*t/hbar internally, delta=alpha/8'
METRIC = 'l1 on the coarse Z^3 factor lattice'
F_DECL = 'F(r)=(1+r)^-4'
FAMILIES = ['F1: AQ1 centered whole-star boxes on Lambda_N', 'F2: I1 section 6 all-contained-face boxes with padding on Lambda_N']
TOPOLOGY = 'operator norm, uniformly for |theta| at most 8, for each fixed local A (not norm continuity in time on all of B(H))'
DYNAMICS_LEVEL = 'algebraic_heisenberg_compact_window'
UNIFORM_IN = 'N (volume) at fixed spacing'
RATE_UNIT = 'per coarse step at fixed spacing (a coarse step is (4a,2a,a)); not a length scale'
SUB_LABEL = 'dynamics_on_compact_windows'
CONTROL_TIER = 'polynomial_lieb_robinson'
ROUTE_OF_INNER = {'F1': 'duhamel_inner_f1', 'F2': 'duhamel_inner_f2'}

# mirror of research/round33/tools/phrase_scan.py (sha256 above), reimplemented so that this program
# depends on no repository module; plus the skeptic's extra list for this loop
ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state',
]
EXTRA_FORBIDDEN = ['uniform in a', 'uniform in the lattice spacing', 'exponential decay in N', 'correlation length',
                   'equality of GNS dynamics', 'correlation functions coincide', 'uniform in time']
NEGATION = re.compile(r"\b(not|never|no|nor|neither|without|excludes?|excluded|exclusion|forbidden|"
                      r"cannot|does not|is not|are not|nothing|none)\b", re.I)
# mirror of the freezer rule R1 (research/round33/tools/freeze_contract.py, sha256 above)
PLACEHOLDER = re.compile(r'<(?![=<>])([^<>=]*)(?<![-=|])>(?!=)')
OLD_PLACEHOLDER = re.compile(r'<([^<>]*)>')  # the pre-fix detector that misread inequality text


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


def sha(rel):
    return hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()


def rup(x, den=10 ** 30):
    n = x * den
    fl = n.numerator // n.denominator
    return F(fl if fl == n else fl + 1, den)


def rdown(x, den=10 ** 30):
    n = x * den
    return F(n.numerator // n.denominator, den)


# ---------------------------------------------------------------- exact exponential enclosures
def exp_enclosure(x, n=30):
    """[lo, hi] for e^x with 0 <= x <= 1: Taylor sum to order n plus the geometric remainder bound."""
    if not (F(0) <= x <= 1):
        raise CheckFailure('exp enclosure domain')
    s, t = F(0), F(1)
    for k in range(n + 1):
        s += t
        t = t * x / (k + 1)
    hi = s + t * F(n + 2) / (F(n + 2) - x)  # t = x^(n+1)/(n+1)!
    return s, hi


def e2_enclosure(x):
    """[lo, hi] for E(x)/x^2 = (e^x - 1 - x)/x^2 = sum_{k>=2} x^(k-2)/k!, x > 0."""
    lo, hi = exp_enclosure(x)
    return (lo - 1 - x) / (x * x), (hi - 1 - x) / (x * x)


# ---------------------------------------------------------------- lattice geometry
def add(a, b):
    return tuple(i + j for i, j in zip(a, b))


def sub(a, b):
    return tuple(i - j for i, j in zip(a, b))


def pi_map(p):
    return (p[0] // 4, p[1] // 2, p[2])  # Euclidean (floor) division, valid for negative coordinates


def d1(a, b):
    return sum(abs(i - j) for i, j in zip(a, b))


def dinf(a):
    return max(abs(i) for i in a)


def Ff(r):
    return F(1, (1 + r) ** 4)


def anchored_faces(b):
    out = []
    for r, s in product(range(4), range(2)):
        p = (4 * b[0] + r, 2 * b[1] + s, b[2])
        for a, c in ORIENT:
            owners = frozenset({pi_map(p), pi_map(add(p, E[a])), pi_map(add(p, E[c]))})
            selected = (a, c) == ('x', 'y') and s == 0 and r <= 2
            out.append({'key': (p, a + c), 'orient': a + c, 'r': r, 's': s, 'owners': owners, 'anchor': b,
                        'selected': selected})
    return out


def omitted_faces(b):
    return [f for f in anchored_faces(b) if not f['selected']]


def rel_type(f):
    return tuple(sorted(sub(o, f['anchor']) for o in f['owners']))


def box(n):
    return set(product(range(-n, n + 1), repeat=3))


def families(n):
    lam = box(n)
    f1, f2 = [], []
    for b in sorted(lam):
        star_in = all(add(b, s) in lam for s in S_STAR)
        for f in omitted_faces(b):
            if star_in:
                f1.append(f)
            if f['owners'] <= lam:
                f2.append(f)
    keys1 = {f['key'] for f in f1}
    extra = [f for f in f2 if f['key'] not in keys1]
    return lam, f1, f2, extra


def parse_i1_table(text):
    rows = []
    pat = re.compile(r'^\| (xy|xz|yz): r=([0-9,.]+); s=([0-9,]+) \| (\d+) \| `\{([^}]*)\}` \| (\w+) \|$')
    for line in text.splitlines():
        m = pat.match(line.strip())
        if not m:
            continue
        rspec = m.group(2)
        if '..' in rspec:
            lo, hi = rspec.split('..')
            rr = list(range(int(lo), int(hi) + 1))
        else:
            rr = [int(v) for v in rspec.split(',')]
        ss = [int(v) for v in m.group(3).split(',')]
        sup = []
        for tok in m.group(5).split(','):
            tok = tok.strip()
            sup.append((0, 0, 0) if tok == '0' else E[tok[-1]])
        rows.append({'orient': m.group(1), 'r': rr, 's': ss, 'count': int(m.group(4)), 'support': sorted(sup),
                     'role': m.group(6)})
    return rows


# ---------------------------------------------------------------- small exact matrices (fixtures)
def mat(rows):
    return [[F(v) for v in row] for row in rows]


def mmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]


def madd(a, b, s=1):
    return [[a[i][j] + s * b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def kron(a, b):
    return [[a[i // len(b)][j // len(b[0])] * b[i % len(b)][j % len(b[0])] for j in range(len(a[0]) * len(b[0]))]
            for i in range(len(a) * len(b))]


def eye(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def comm(a, b):
    return madd(mmul(a, b), mmul(b, a), -1)


def is_zero(a):
    return all(v == 0 for row in a for v in row)


# ---------------------------------------------------------------- phrase scan and placeholders
def normalize(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def clauses(text):
    return [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', text) if c.strip()]


def affirmative_hits(text, forbidden, template=None):
    body = normalize(text)
    if template:
        body = body.replace(normalize(template), ' ')
    hits = []
    for clause in clauses(body):
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I) and not NEGATION.search(clause):
                hits.append(phrase)
    return hits


def placeholder_spans(text, pattern=PLACEHOLDER):
    out = []
    for m in pattern.finditer(text):
        inner = m.group(1)
        if re.search(r'\s', inner) or '|' in inner or 'e.g.' in inner:
            out.append(m.group(0))
    return out


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for k in sorted(value):
            yield from strings(value[k])
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from strings(v)


def numbers(value):
    if isinstance(value, (int, float, F)) and not isinstance(value, bool):
        yield value
    elif isinstance(value, dict):
        for k in sorted(value):
            yield from numbers(value[k])
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from numbers(v)


def packet_digest(pk):
    body = json.dumps({'inputs': sorted(pk['inputs']), 'controls': pk['controls']}, sort_keys=True)
    return hashlib.sha256(body.encode()).hexdigest()


# ---------------------------------------------------------------- validator
def validate(pk, c):
    # provenance and coherent tampering
    if pk['contract_sha256'] != CONTRACT_SHA256:
        raise Rejected('contract hash')
    if pk['ns_excerpt_sha256'] != NS_EXCERPT_SHA256 or pk['ns_pdf_sha256'] != NS_PDF_SHA256:
        raise Rejected('lieb-robinson form quoted: source hash')
    if pk['freeze_digest'] != packet_digest(pk):
        raise Rejected('coherent evidence tampering: freeze digest')
    if sorted(pk['inputs']) != sorted(c['declared_inputs']):
        extra = sorted(set(pk['inputs']) - set(c['declared_inputs']))
        if any(p in c['isolation_forbidden'] or '/forward/ba2/' in p or '/skeptic/' in p or 'deliberation' in p
               for p in extra):
            raise Rejected('reverse premise isolation')
        raise Rejected('coherent evidence tampering: snapshot inventory')
    if sorted(pk['controls']) != sorted(c['control_ids']) or any(pk['controls'][k] is not True for k in pk['controls']):
        raise Rejected('coherent evidence tampering: control booleans')
    # exact arithmetic
    if any(isinstance(v, float) for v in numbers(pk)):
        raise Rejected('exact arithmetic')
    # model
    if (pk['model_id'] != MODEL_ID or pk['triple'] != ['0', '0', '0'] or pk['group'] != 'SU(2)'
            or pk['lattice'] != 'Z^3 coarse 24-link factors' or pk['model_is_finite_graph'] is not False):
        raise Rejected('changed model relabelled')
    if pk['tau_abs'] != c['tau'] or sorted(pk['signs']) != ['+', '-']:
        raise Rejected('changed model relabelled: coupling')
    if pk['same_coupling'] is not True or pk['compared_couplings'] != ['same tau']:
        raise Rejected('cross-coupling comparison rejected')
    if pk['families'] != FAMILIES or pk['N_min'] != 2:
        raise Rejected('two families not named')
    if pk['cover'] != R_COVER or pk['cover_links'] != 48 or pk['cover_endpoints'] != 36:
        raise Rejected('full original wilson cover')
    fc = pk['face_counts']
    if (fc != {'per_site': 49, 'owner_sets_per_site': 15, 'meeting_R': 82, 'inside_R': 10}
            or pk['face_count_source'] != 'I1 table by translation covariance, all sites'):
        raise Rejected('face count all sites')
    if pk['stars_per_site'] != 4 or pk['J_over_tau'] != 28 or pk['stars_meeting_R'] != 7:
        raise Rejected('missing incoming stars: incident stars')
    par = pk['parameters']
    for key in ('metric', 'weights', 'window', 'N_min', 'clock'):
        if key not in par:
            raise Rejected('parameters must declare metric weights window: ' + key)
    if par['metric'] != METRIC:
        raise Rejected('changed model relabelled: metric')
    # Lieb-Robinson source, form, F, placement
    if pk['lr_source'] != NS_EXCERPT_REL:
        raise Rejected('lieb-robinson form quoted: second-hand source')
    if pk['lr_quote'] != c['lr_quote'] or pk['lr_theorem'] != 'Theorem 3.1, eqs. (51)-(52)' \
            or pk['limit_theorem'] != 'Theorem 4.1, eq. (77)':
        raise Rejected('lieb-robinson form quoted')
    if pk['F'] != F_DECL or pk['C_upper'] != 224 or par['weights'] != F_DECL:
        raise Rejected('lieb-robinson F declared')
    if pk['constant_substitution'] != 'upper bounds for C and ||Phi||_F justified by monotonicity':
        raise Rejected('lieb-robinson constant substitution needs monotonicity')
    ex = pk['exponential_instance']
    if ex is not None:
        if ex.get('labelled') is not True or ex.get('target') is not None or ex.get('phi_over_tau') != 'e^{2mu}*2268' \
                or ex.get('C_upper') != 224 or ex.get('admission_weight') is not False:
            raise Rejected('lieb-robinson F declared: exponential instance')
    if pk['onsite_placement'] != 'interaction picture: H_x=h_x in (44), Phi bounded' or pk['onsite_in_phi'] is not False \
            or pk['lr_applied_to'] != 'bounded interaction Phi only':
        raise Rejected('unbounded onsite: interaction picture')
    # clock and window
    if pk['clock'] != CLOCK or par['clock'] != CLOCK:
        raise Rejected('wrong delta alpha hbar clock')
    if pk['theta_max'] != 8 or pk['u_over_theta'] != F(1, 8) or pk['U'] != 1 or par['window'] != '|theta| at most 8':
        raise Rejected('wrong delta alpha hbar clock: window')
    if pk['uniform_in_time_claimed'] is not False:
        raise Rejected('time window named: uniform in time')
    if pk['topology'] != TOPOLOGY:
        raise Rejected('topology named')
    if pk['dynamics_level'] != DYNAMICS_LEVEL or pk['gns_dynamics_equality_claimed'] is not False:
        raise Rejected('algebraic not gns dynamics')
    # boundary source
    src = pk['source']
    if src['old_terms_included'] or src['terms_meet_source_set'] is not True:
        raise Rejected('boundary source new terms only')
    if src['padding_charged'] or src['padding_factorization'] != 'exact (commutes with H^(2)_N, faces and B(H_R))':
        raise Rejected('extra face count and distance: padding')
    if (src['count'] != '28N(5N+1)' or src['owners_max'] != 3 or src['dist_ez'] != 'N-1' or src['dist_0'] != 'N'
            or src['enumerated_N'] != [2, 3] and src['enumerated_N'] != [2, 3, 4]
            or src['all_size_argument'] is not True):
        raise Rejected('extra face count and distance')
    if src['each_face_once'] is not True:
        raise Rejected('f2 regrouping charged once')
    rg = pk['regrouping']
    if rg['double_charged'] or rg['per_site_face_sum_over_tau'] != F(49, 3) or rg['charging'] != 'face by face':
        raise Rejected('f2 regrouping charged once')
    # comparison
    cm = pk['comparison']
    inner, inter, phi = cm['inner_family'], cm['interaction'], cm['phi_over_tau']
    allowed = {('F1', 'Phi', 2268), ('F2', "Phi'", 1323), ('F2', 'Psi_N padded anchor groups (stated)', 2268)}
    if (inner, inter, phi) not in allowed:
        raise Rejected('duhamel inner family constants')
    if pk['route'] == 'forward' and inner != 'F1' or pk['route'] == 'reverse' and inner != 'F2':
        raise Rejected('duhamel inner family constants: route')
    if cm['tier'] not in ('polynomial_lieb_robinson',) or cm['route_label'] != ROUTE_OF_INNER[inner]:
        raise Rejected('tier mixing')
    if cm['combine'] != 'linear':
        raise Rejected('root-N misuse')
    if cm['form'] == 'leading order only':
        raise Rejected('duhamel tau order: leading form is not a bound')
    if cm['tau_order'] != 2 or cm['first_order_reason'] != 'disjoint supports: [V_f, A]=0 for N at least 2':
        raise Rejected('duhamel tau order quadratic')
    lo, hi = c['bracket']
    if not (lo <= cm['scaling_ratio'] <= hi) or pk['bracket'] != c['bracket']:
        raise Rejected('tau scaling exponent')
    kmin = c['K_min'][(inner, phi)]
    if cm['coefficient'] < kmin:
        raise Rejected('coherent evidence tampering: coefficient below the derivable value')
    if cm['n_dependence'] != '(5N+1)N^-3':
        raise Rejected('lieb-robinson polynomial tail')
    # Cauchy
    for fam in ('F1', 'F2'):
        cy = pk['cauchy'][fam]
        if cy['quantifier'] != 'all M greater than N':
            raise Rejected('lieb-robinson polynomial tail: N to N+1 bound summed')
        if cy['rate'] != '1/(N-1)':
            raise Rejected('lieb-robinson polynomial tail')
        if cy['charging'] == 'double':
            raise Rejected('f2 regrouping charged once')
        if not (lo <= cy['scaling_ratio'] <= hi):
            raise Rejected('tau scaling exponent')
        if cy['coefficient'] < c['C_min'][(fam, cy['interaction'], cy['charging'])]:
            raise Rejected('coherent evidence tampering: coefficient below the derivable value')
        if cy['tier'] != CONTROL_TIER:
            raise Rejected('tier mixing')
    if pk['cauchy']['F1']['interaction'] != 'Phi' or pk['cauchy']['F2']['interaction'] not in ("Phi'", 'via F1 triangle'):
        raise Rejected('duhamel inner family constants')
    # F2 limit dynamics and O6
    fl = pk['f2_limit']
    if fl['whole_sequence'] is True and fl['whole_sequence_via'] != 'Cauchy bound over all M greater than N':
        raise Rejected('subsequence versus whole sequence')
    if fl['identified_with'] != 'T_theta (AQ1 limit dynamics)' or fl['identification_via'] != 'comparison bound':
        raise Rejected('f2 limit dynamics equals f1')
    if fl['sections_4_5_rerun'] is not True or fl['subsequences'] != 'F2 own diagonal extraction':
        raise Rejected('f2 limit dynamics equals f1: sections 4-5 rerun')
    # targets and verdict
    met = {'comparison': cm['coefficient'] <= c['target_comparison'],
           'cauchy': all(pk['cauchy'][f]['coefficient'] <= c['target_cauchy'] for f in ('F1', 'F2'))}
    if pk['targets_met'] != met:
        raise Rejected('insufficient verdict retained: targets_met inconsistent')
    if pk['verdict'] == 'accepted_within_scope' and not all(met.values()):
        raise Rejected('insufficient verdict retained')
    if pk['verdict'] != 'accepted_within_scope' and not pk.get('dominating_term'):
        raise Rejected('insufficient verdict retained: dominating term')
    if pk['retuned'] is not False:
        raise Rejected('insufficient verdict retained: retuned')
    # wording, units, uniformity
    if pk['uniform_in'] != UNIFORM_IN:
        raise Rejected('uniform in N not in a')
    if pk['rate_unit'] != RATE_UNIT:
        raise Rejected('decay rate in N not a')
    if pk['sub_label'] != SUB_LABEL:
        raise Rejected('changed model relabelled: sub-label')
    for text in strings([pk['statements'], pk['sentence']]):
        if placeholder_spans(text):
            raise Rejected('placeholder span')
    for text in pk['statements']:
        hits = affirmative_hits(text, c['forbidden'], c['sentence'])
        if hits:
            if any(h in ('uniform in a', 'uniform in the lattice spacing') for h in hits):
                raise Rejected('uniform in N not in a: forbidden phrasing')
            raise Rejected('forbidden phrasing: ' + hits[0])
    if pk['sentence'] != c['sentence'] or pk['sentence_count'] != 1:
        raise Rejected('mandatory sentence template')
    gf = pk['gate_fields']
    for key in sorted(c['gate_fields']):
        if key not in gf:
            raise Rejected('gate fields topic specific: missing ' + key)
    if gf['whole_sequence_claimed'] is True and not gf.get('whole_sequence_scope'):
        raise Rejected('gate fields topic specific: whole_sequence_scope empty')
    if gf.get('dynamics_level') != DYNAMICS_LEVEL:
        raise Rejected('gate fields topic specific: dynamics_level')
    for key, want in sorted(c['gate_fields'].items()):
        if isinstance(want, bool) and gf[key] is not want:
            if key in ('gns_dynamics_equality_claimed', 'common_limit_claimed'):
                raise Rejected('algebraic not gns dynamics: ' + key)
            if key == 'state_convergence_claimed':
                raise Rejected('subsequence versus whole sequence: states')
            if key == 'rate_in_a_claimed':
                raise Rejected('decay rate in N not a')
            if key == 'uniform_in_time_claimed':
                raise Rejected('time window named: uniform in time')
            raise Rejected('gate field claimed: ' + key)
    for key in ('continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified', 'uniform_in_a_claimed'):
        if pk['claims'].get(key) is not False:
            raise Rejected('forbidden claim ' + key)
    for name in c['error_terms']:
        if name not in pk['error_terms']:
            raise Rejected('error term missing: ' + name)
    return True


# ---------------------------------------------------------------- execute
def execute():
    # 1. provenance -------------------------------------------------------------------------
    contract_bytes = (ROOT / CONTRACT_REL).read_bytes()
    c_sha = hashlib.sha256(contract_bytes).hexdigest()
    need(c_sha == CONTRACT_SHA256, 'contract_sha256_pinned', sha256=c_sha)
    con = json.loads(contract_bytes)
    par, pre = con['parameters'], con['preregistration']
    ns_text = (ROOT / NS_EXCERPT_REL).read_text()
    ns_sha = sha(NS_EXCERPT_REL)
    need(ns_sha == NS_EXCERPT_SHA256, 'ns_excerpt_sha256_pinned', sha256=ns_sha)
    bind = json.loads((ROOT / BINDINGS_REL).read_text())
    ns_bind = [s for s in bind['sources'] if s['id'] == 'ns-2014']
    need(len(ns_bind) == 1 and ns_bind[0]['pdf_sha256'] == NS_PDF_SHA256 and NS_PDF_SHA256 in ns_text
         and ns_bind[0]['url'] == 'https://arxiv.org/pdf/1410.8174v1' and 'https://arxiv.org/pdf/1410.8174v1' in ns_text,
         'ns_pdf_sha256_equals_round29_binding', pdf_sha256=NS_PDF_SHA256)
    gate_sha = {g: sha(g) for g in sorted(GATES)}
    need(gate_sha == GATES, 'admitted_gate_sha256_pinned', gates=gate_sha)
    bound = []
    for rep, gate in REPORT_BINDINGS:
        gb = json.loads((ROOT / gate).read_text())['bindings']
        h = sha(rep)
        if gb.get(rep) != h:
            raise CheckFailure('report not bound by gate: ' + rep)
        bound.append({'report': rep, 'gate': gate, 'sha256': h})
    need(True, 'premise_reports_bound_by_gates', reports=bound)
    delib = (ROOT / DELIBERATION_REL).read_text()
    need(sha(DELIBERATION_REL) == DELIBERATION_SHA256, 'deliberation2_sha256_pinned',
         note='skeptic-only source of the recorded loop-1 previews; not a producer premise')

    # 2. contract reading --------------------------------------------------------------------
    tau = F(pre['tau']['value'])
    tv = re.findall(r'(\d+(?:\.\d+)?)x10\^-(\d+)', pre['target']['value'])
    target_comparison = F(tv[0][0]) / 10 ** int(tv[0][1])
    target_cauchy = F(tv[1][0]) / 10 ** int(tv[1][1])
    theta_max = int(re.search(r'\|theta\|<=(\d+)', par['window']).group(1))
    br = {k: [F(int(a)), F(int(b))] for k, v in pre['scaling_brackets_per_constant'].items()
          for a, b in [re.match(r'\[(\d+),(\d+)\]', v).groups()]}
    need(con['status'] == 'frozen_before_production' and tau == F(1, 10 ** 8) and pre['tau']['signs_evaluated'] == ['+', '-']
         and pre['model_id'] == MODEL_ID and pre['selected_triple_alpha_units'] == ['0', '0', '0']
         and target_comparison == F(6, 10 ** 11) and target_cauchy == F(25, 10 ** 11) and theta_max == 8
         and '6x10^-11 (5N+1) N^-3' in par['targets']['comparison']
         and '2.5x10^-10/(N-1)' in par['targets']['within_family_cauchy']
         and 'sup over M greater than N' in par['targets']['within_family_cauchy']
         and pre['target']['comparator'] == '<=' and con['direction'] == 'paired' and con['reverse_premise_isolation'] is True
         and pre['sub_labels_allowed'] == [SUB_LABEL]
         and pre['tier_names_allowed'] == ['polynomial_lieb_robinson', 'exponential_lieb_robinson'],
         'contract_targets_cap_window_read', tau=q(tau), target_comparison=q(target_comparison),
         target_cauchy=q(target_cauchy), theta_max=theta_max, u_max=q(F(theta_max, 8)))
    need(br == {'comparison_coefficient': [F(9500), F(10500)], 'cauchy_coefficient': [F(9500), F(10500)]},
         'contract_scaling_brackets_read', brackets={k: [q(a), q(b)] for k, (a, b) in sorted(br.items())})
    control_ids = list(con['controls'])
    need(sorted(control_ids) == sorted(pre['controls_required']['ids']) and len(control_ids) == 35
         and len(set(control_ids)) == 35, 'contract_control_mirror', controls=len(control_ids))
    sem = con['new_control_semantics']
    missing_sem = sorted(set(control_ids) - set(sem))
    need(missing_sem == ['cross_coupling_comparison_rejected', 'full_original_wilson_cover', 'gate_fields_topic_specific',
                         'topology_named'] and len(sem) == 31, 'contract_defect_semantics_coverage_recorded',
         semantics_defined=len(sem), missing=missing_sem,
         reading='the four ids carry the loop-2 semantics BA2-N2 (not delivered to producers); names are self-explanatory')
    need('[9900,10100]' in sem['duhamel_tau_order_quadratic'] and br['comparison_coefficient'] == [F(9500), F(10500)]
         and '[9900,10100] would reject a valid bound' in pre['scaling_brackets_per_constant']['comparison_coefficient'],
         'contract_defect_bracket_inconsistency_recorded',
         reading='preregistration.scaling_brackets_per_constant [9500,10500] governs; the stale [9900,10100] in '
                 'new_control_semantics.duhamel_tau_order_quadratic rejects the valid (x^2/2)e^x form')
    need('parameters' in con and all(k in par for k in ('metric', 'weights', 'window')) and 'N_min' not in par
         and 'clock' not in par and 'w=e^mu' in sem['parameters_declare_metric_weights_window'],
         'contract_defect_parameters_fields_recorded',
         reading='parameters has metric, weights, window; N_0 is in model/targets prose (N at least 2) and the clock in '
                 'window and preregistration.clock; the semantics text is copied from BA1 (w=e^mu, e^beta)')
    shared = list(con['shared_premises'])
    need(all((ROOT / p).is_file() for p in shared) and len(shared) == 27 and NS_EXCERPT_REL in shared,
         'contract_shared_premises_exist', count=len(shared))
    declared_inputs = sorted(['AGENTS.md', CONTRACT_REL] + shared)
    need(sorted(OBSERVED_INPUTS['reverse']) == declared_inputs and len(declared_inputs) == 29,
         'producer_input_inventories_recorded', inventory_size=29,
         scope='recorded by name and sha256 comparison on 2026-09-24; both producers hold exactly AGENTS.md, the '
               'contract and the 27 shared premises, byte-identical to the repository')
    isolation_forbidden = ['research/round33/skeptic/triage.md', 'research/round33/skeptic/recommendation.json',
                           'research/round33/skeptic/prospective-controls.json',
                           'research/round33/skeptic/loop2-review.md', 'research/round33/skeptic/loop2-review.json',
                           'research/round33/advisor/deliberation-1.md', DELIBERATION_REL,
                           'research/round33/advisor/plan.json', 'research/round33/experts/modern/memo.md']
    need(not (set(isolation_forbidden) & set(declared_inputs)), 'reverse_inventory_excludes_forbidden_files')

    # 3. Nachtergaele-Sims excerpt: verbatim spans ---------------------------------------------
    part_a = ns_text.split('## Part B')[0]
    part_b = ns_text.split('## Part B')[1]
    quotes = {}
    for tag in ('(40)', '(41)', '(44)', '(48)', '(49)', '(50)', '(51)', '(52)', '(77)'):
        lines = [ln[2:] for ln in part_a.splitlines() if ln.startswith('- ' + tag)]
        if len(lines) != 1:
            raise CheckFailure('excerpt equation not found ' + tag)
        quotes[tag] = lines[0]
    lr_quote = quotes['(51)']
    need(lr_quote == '(51) ‖[τ_t^Λ(A), B]‖ ≤ (2‖A‖‖B‖ / C) '
                     '(e^{2‖Φ‖C|t|} − 1) D(X, Y)'
         and '(52) D(X, Y) = min{' in quotes['(52)'] and 'y∈∂_Φ Y' in quotes['(52)']
         and 'Theorem 3.1.' in part_a and 'Theorem 4.1' in part_a and 'interaction-picture dynamics (57)' in part_a
         and 'H_0 = Σ_{x∈Λ} H_x + Σ_{Z⊂X} Φ(Z) (54)' in part_a
         and '2kAkkBk 2kΦkC|t|' in part_b and '(51)' in part_b and '(77)' in part_b,
         'ns_theorem_3_1_and_4_1_quoted_verbatim', quotes=quotes,
         reading='NS t is the normalized time u=theta/8 of e^{iuH}; NS tau_t^Lambda is the evolution T, not the coupling')
    thm41 = part_a.split('**Theorem 4.1**')[1].split('In its proof')[0]
    title_clause = 'Section 4, "On the existence of the thermodynamic limit"'
    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings']) + EXTRA_FORBIDDEN
    sentence = pre['mandatory_sentence_template']
    need(title_clause in part_a and affirmative_hits(title_clause, forbidden) == ['the thermodynamic limit']
         and affirmative_hits(thm41.split('). ', 1)[1], forbidden) == [],
         'ns_section_title_phrase_scan_tension',
         reading='quote the statement of Theorem 4.1 (77) and cite its section as Section 4; the section title '
                 'contains a contract-forbidden phrasing and trips the negation-aware scan when quoted affirmatively')

    # 4. geometry from fine coordinates --------------------------------------------------------
    i1_text = (ROOT / 'research/round21/forward/i1/report.md').read_text()
    table = parse_i1_table(i1_text)
    b0 = (0, 0, 0)
    faces0 = anchored_faces(b0)
    om0 = omitted_faces(b0)
    types0 = {}
    for f in om0:
        types0[rel_type(f)] = types0.get(rel_type(f), 0) + 1
    need(len(faces0) == 24 and len(om0) == 21 and sum(f['selected'] for f in faces0) == 3
         and all(f['owners'] == frozenset({b0}) for f in faces0 if f['selected'])
         and all(b0 in f['owners'] and all(sub(o, b0) in S_STAR for o in f['owners']) for f in om0),
         'fine_face_classes_per_anchor', total=24, selected=3, omitted=21,
         owner_types={' '.join(str(t) for t in k): v for k, v in sorted(types0.items())})
    tab_ok = len(table) == 8 and sum(r['count'] for r in table) == 24
    for row in table:
        got = [f for f in faces0 if f['orient'] == row['orient'] and f['r'] in row['r'] and f['s'] in row['s']]
        if len(got) != row['count'] or any(sorted(f['owners']) != row['support'] for f in got):
            tab_ok = False
        if any(f['selected'] != (row['role'] == 'selected') for f in got):
            tab_ok = False
    need(tab_ok, 'i1_table_matches_fine_enumeration', rows=len(table))
    cov = True
    for b in product(range(-3, 4), repeat=3):
        tb = {}
        for f in omitted_faces(b):
            tb[rel_type(f)] = tb.get(rel_type(f), 0) + 1
        cov = cov and tb == types0
    need(cov, 'translation_covariance_of_owner_types', anchors_checked=343, includes_negative_coordinates=True)
    u = (0, 0, 0)
    near = [add(u, d) for d in product(range(-2, 3), repeat=3)]
    faces_u = [f for b in near for f in omitted_faces(b) if u in f['owners']]
    sets_u = {f['owners'] for f in faces_u}
    stars_u = [b for b in near if u in [add(b, s) for s in S_STAR]]
    need(len(faces_u) == 49 and len(sets_u) == 15 and len(stars_u) == 4 and sorted(stars_u) == sorted(sub(u, s) for s in S_STAR),
         'per_site_faces_owner_sets_incoming_stars', faces=49, owner_sets=15, incoming_stars=4,
         J_over_tau='28 (4 stars x 21 faces x 1/3)', face_level_sum_over_tau='49/3')
    meet = {f['key']: f for b in near for f in omitted_faces(b) if f['owners'] & set(R_COVER)}
    inside = [f for f in meet.values() if f['owners'] <= set(R_COVER)]
    anchors_R = sorted({b for b in near if any(add(b, s) in R_COVER for s in S_STAR)})
    sets_R = {f['owners'] for f in meet.values()}
    need(len(meet) == 82 and len(inside) == 10 and len(anchors_R) == 7 and len(sets_R) == 27
         and all(f['anchor'] == b0 and f['owners'] == frozenset(R_COVER) for f in inside),
         'cover_R_counts', faces_meeting_R=82, inside_R=10, incident_anchors=7, owner_sets_meeting_R=27)
    shells = {}
    for p in product(range(-13, 14), repeat=3):
        r = d1(p, ORIGIN)
        if r <= 12:
            shells[r] = shells.get(r, 0) + 1
    need(shells[0] == 1 and all(shells[r] == 4 * r * r + 2 for r in range(1, 13)), 'l1_shell_count_4r2_plus_2',
         radii='1..12')
    star_diam = max(d1(a, b) for a in S_STAR for b in S_STAR)
    own_diam = max(d1(a, b) for f in om0 for a in f['owners'] for b in f['owners'])
    need(star_diam == 2 and own_diam == 2, 'star_and_owner_set_l1_diameter_2')

    # 5. families on Lambda_N -------------------------------------------------------------------
    fam_rows = {}
    class_counts = {}
    for n in (2, 3, 4, 5):
        lam, f1, f2, extra = families(n)
        m = 2 * n
        keys1 = {f['key'] for f in f1}
        keys2 = {f['key'] for f in f2}
        anchors_ok = all(any(f['anchor'][i] == n for i in range(3)) for f in extra)
        out_ok = True
        for f in extra:
            outs = [i for i in range(3) if f['anchor'][i] == n]
            out_ok = out_ok and all(o[i] == n for o in f['owners'] for i in outs) and all(dinf(o) == n for o in f['owners'])
        dz = min(d1(y, E_Z) for f in extra for y in f['owners'])
        d0 = min(d1(y, ORIGIN) for f in extra for y in f['owners'])
        at_min = sum(1 for f in extra if any(d1(y, E_Z) == n - 1 for y in f['owners']))
        owners_total = sum(len(f['owners']) for f in extra)
        s_exact = sum((Ff(d1(x, y)) for f in extra for x in R_COVER for y in f['owners']), F(0))
        crude = F(168 * (5 * n + 1), n ** 3)
        refined = F(308 * n * n + 56 * n) * (Ff(n - 1) + Ff(n))
        padding = {add(b, s) for b in lam for s in S_STAR} - lam
        no_pad_touch = all(not (f['owners'] & padding) for f in f2)
        native_f2 = True
        for b in sorted(lam):
            for f in omitted_faces(b):
                native_f2 = native_f2 and ((f['key'] in keys2) == (f['owners'] <= lam))
        if n in (2, 3):
            for f in extra:
                outs = frozenset(i for i in range(3) if f['anchor'][i] == n)
                class_counts.setdefault(n, {})
                class_counts[n][outs] = class_counts[n].get(outs, 0) + 1
        ok = (len(f1) == 21 * m ** 3 and len(f2) == 14 * m * (m + 1) ** 2 + 7 * m * m * (m + 1) and keys1 <= keys2
              and len(extra) == 28 * n * (5 * n + 1) and anchors_ok and out_ok and dz == n - 1 and d0 == n
              and owners_total == 308 * n * n + 56 * n and max(len(f['owners']) for f in extra) == 3
              and s_exact <= refined <= crude and len(padding) == 3 * (2 * n + 1) ** 2 and no_pad_touch and native_f2
              and at_min == 11)
        if not ok:
            raise CheckFailure('family enumeration N=%d' % n)
        fam_rows[n] = {'F1_faces': len(f1), 'F2_faces': len(f2), 'extra_faces': len(extra),
                       'extra_formula': '28N(5N+1)=%d' % (28 * n * (5 * n + 1)), 'owner_incidences': owners_total,
                       'min_l1_to_e_z': dz, 'min_l1_to_0': d0, 'faces_at_min_distance': at_min,
                       'padding_sites': len(padding), 'S_exact': q(s_exact), 'S_exact_preview': preview(s_exact),
                       'S_crude_168(5N+1)N^-3': q(crude), 'S_refined_all_size': q(refined),
                       'S_exact_over_crude': preview(s_exact / crude)}
    need(True, 'families_F1_F2_extra_faces_N2_to_N5', rows={str(k): v for k, v in sorted(fam_rows.items())})
    # all-size class argument: extra faces at anchor b are the anchor types avoiding every e_i with b_i = N
    per_class = {}
    for outs in [frozenset(s) for s in ([0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2])]:
        per_class[outs] = sum(v for t, v in types0.items() if not any(E['xyz'[i]] in t for i in outs))
    closed_ok = all(4 * n * n * (per_class[frozenset([0])] + per_class[frozenset([1])] + per_class[frozenset([2])])
                    + 2 * n * (per_class[frozenset([0, 1])] + per_class[frozenset([0, 2])] + per_class[frozenset([1, 2])])
                    + per_class[frozenset([0, 1, 2])] == 28 * n * (5 * n + 1) for n in range(2, 200))
    enum_ok = all(class_counts[n][outs] == per_class[outs] * (4 * n * n if len(outs) == 1 else 2 * n if len(outs) == 2 else 1)
                  for n in (2, 3) for outs in class_counts[n])
    need([per_class[frozenset(s)] for s in ([0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2])] == [17, 13, 5, 10, 3, 1, 0]
         and closed_ok and enum_ok, 'extra_faces_all_size_class_argument',
         per_anchor_class={'x': 17, 'y': 13, 'z': 5, 'xy': 10, 'xz': 3, 'yz': 1, 'xyz': 0},
         anchors='(2N)^2 per single class, 2N per pair, 1 for xyz', total='140N^2+28N=28N(5N+1)', checked_N='2..199')
    # Cauchy geometry: new F1 stars and new F2 faces from N to M
    cg = True
    for n, mm in ((2, 3), (2, 4), (3, 4)):
        lam_n, lam_m = box(n), box(mm)
        new_stars = [b for b in lam_m if all(add(b, s) in lam_m for s in S_STAR) and not all(add(b, s) in lam_n for s in S_STAR)]
        cg = cg and all(dinf(add(b, s)) >= n for b in new_stars for s in S_STAR)
        inc = {}
        for b in new_stars:
            for s in S_STAR:
                inc[add(b, s)] = inc.get(add(b, s), 0) + 1
        cg = cg and max(inc.values()) <= 4
        new_faces = [f for b in lam_m for f in omitted_faces(b) if f['owners'] <= lam_m and not f['owners'] <= lam_n]
        cg = cg and all(dinf(o) >= n for f in new_faces for o in f['owners'])
        finc = {}
        for f in new_faces:
            for o in f['owners']:
                finc[o] = finc.get(o, 0) + 1
        cg = cg and max(finc.values()) <= 49 and not any(o in R_COVER for f in new_faces for o in f['owners'])
    need(cg, 'cauchy_new_terms_outside_sup_ball_N', pairs=[[2, 3], [2, 4], [3, 4]],
         statement='every site of a new F1 star and every owner of a new F2 face has |y|_inf at least N; per-site '
                   'incidence at most 4 stars and 49 faces; none meets R')

    # 6. Nachtergaele-Sims constants --------------------------------------------------------------
    aq1 = (ROOT / 'research/round29/forward/aq1/report.md').read_text()
    ay1r = (ROOT / 'research/round32/reverse/ay1/report.md').read_text()
    c_up = F(int(re.search(r'C<=32\|\|F\|\|<=(\d+)', aq1).group(1)))
    f_up = F(int(re.search(r'`\|\|F\|\|<=(\d+)`', aq1).group(1)))
    j_aq = F(int(re.search(r'J\\le4M=(\d+)\|\\tau\|', aq1).group(1)))
    phi_aq = F(int(re.search(r'81J\\le(\d+)\|\\tau\|', aq1).group(1)))
    phip_ay = F(int(re.search(r'81·49\|tau\|/3 = (\d+)\|tau\|', ay1r).group(1)))
    need(c_up == 224 and f_up == 7 and j_aq == 28 and phi_aq == 2268 and phip_ay == 1323
         and phi_aq == 81 * j_aq and phip_ay == 81 * F(49, 3), 'ns_constants_parsed_from_bound_premises',
         C_upper=q(c_up), F_norm_upper=q(f_up), J_over_tau=q(j_aq), phi_over_tau=q(phi_aq), phiprime_over_tau=q(phip_ay))
    g = [F(4 * r * r + 2, (1 + r) ** 4) for r in range(0, 61)]
    part = 1 + sum(g[1:], F(0))
    fnorm_hi = part + F(4, 61)  # tail sum_{r>=61} g(r) <= 4 sum_{m>=62} 1/m^2 <= 4/61
    need(all(g[r] > g[r + 1] for r in range(1, 60)) and all(4 * r * r + 2 <= 6 * (r + 1) ** 2 for r in range(1, 200))
         and part <= fnorm_hi <= f_up and F(2) < part, 'ns_F_norm_enclosure', lower=q(rdown(part, 10 ** 12)),
         upper=q(rup(fnorm_hi, 10 ** 12)), aq1_upper='7')
    need(all(Ff(F(r, 2)) <= 16 * Ff(r) for r in range(0, 400)), 'aq1_convolution_half_split_inequality',
         statement='F(r/2) <= 16 F(r), whence C <= 32||F|| <= 224 (AQ1 section 3)')
    # sharp sup-norm values at x = origin (translation covariance; labelled, not used)
    pair_stars, pair_faces = {}, {}
    for b in product(range(-2, 3), repeat=3):
        members = [add(b, s_) for s_ in S_STAR]
        if ORIGIN in members:
            for y in members:
                pair_stars[y] = pair_stars.get(y, 0) + 1
        for f in omitted_faces(b):
            if ORIGIN in f['owners']:
                for y in f['owners']:
                    pair_faces[y] = pair_faces.get(y, 0) + 1
    sup_phi = max(7 * n_ / Ff(d1(ORIGIN, y)) for y, n_ in pair_stars.items())
    sup_phip = max(F(n_, 3) / Ff(d1(ORIGIN, y)) for y, n_ in pair_faces.items())
    need(sup_phi == 567 and sup_phip == 108 and sup_phi <= phi_aq and sup_phip <= phip_ay,
         'ns_interaction_norm_sharp_values_labelled', sharp_phi_over_tau='567', sharp_phiprime_over_tau='108',
         use='labelled observation only; the contract fixes 2268|tau| and 1323|tau| for the targets')
    v_per_tau = 2 * c_up * phi_aq
    vp_per_tau = 2 * c_up * phip_ay
    v = v_per_tau * tau
    vp = vp_per_tau * tau
    need(v_per_tau == 1016064 and vp_per_tau == 592704 and v == F(3969, 390625) and vp == F(9261, 1562500),
         'lieb_robinson_velocities', v='2C||Phi||=1016064|tau| per unit u', v_prime='2C||Phi\'||=592704|tau|',
         v_cap=q(v), v_prime_cap=q(vp), per_theta='127008|tau| and 74088|tau| per unit theta')
    # monotonicity: E(x)/x^2 has nonnegative Taylor coefficients, hence increasing; spot check with enclosures
    xs = [F(1, 1000), F(1, 200), v / 2, v, 2 * v, F(1, 20)]
    encl = [e2_enclosure(x) for x in xs]
    need(all(encl[i][1] < encl[i + 1][0] for i in range(len(xs) - 1)), 'monotonicity_in_C_and_Phi',
         statement='E(vU)/(vC) = 2||Phi||U^2 E(x)/x^2 with x = 2||Phi||CU; E(x)/x^2 = sum_{k>=2} x^(k-2)/k! is '
                   'increasing, so upper bounds for C and ||Phi||_F may be substituted in (51) and in its time integral')
    lo0, hi0 = exp_enclosure(F(1, 2))
    need(lo0 < hi0 and hi0 - lo0 < F(1, 10 ** 30) and F(16487212707, 10 ** 10) < hi0 and lo0 < F(16487212708, 10 ** 10),
         'exp_enclosure_self_test', e_half=[q(rdown(lo0, 10 ** 15)), q(rup(hi0, 10 ** 15))])

    # 7. comparison coefficients ---------------------------------------------------------------
    U = F(theta_max, 8)

    def duhamel(prefactor_over_tau, phi_per_tau, t_abs):
        """sup-bound prefactor*|tau| * E(vU)/(vC) with v = 2 C phi |tau|; returns (lo, hi, closed skeptic, modern)."""
        vv = 2 * c_up * phi_per_tau * t_abs
        x = vv * U
        elo, ehi = e2_enclosure(x)
        lead = prefactor_over_tau * t_abs * 2 * phi_per_tau * t_abs * U * U  # = pref*|tau|*2||Phi||U^2
        closed = lead / (2 * (1 - x / 3))
        modern_e = lead / 2 * exp_enclosure(x)[1]
        modern_r = lead / (2 * (1 - x))
        return lead * elo, lead * ehi, closed, modern_e, modern_r, lead / 2

    comp = {}
    for name, pref, phi in (('forward_inner_F1_Phi', F(112), phi_aq), ('reverse_inner_F2_Phiprime', F(112), phip_ay)):
        lo_, hi_, cl, me, mr, lead = duhamel(pref, phi, tau)
        comp[name] = {'lo': lo_, 'hi': hi_, 'closed': cl, 'modern_e': me, 'modern_r': mr, 'lead': lead}
    fwd, rev = comp['forward_inner_F1_Phi'], comp['reverse_inner_F2_Phiprime']
    need(fwd['lead'] == 254016 * tau ** 2 and rev['lead'] == 148176 * tau ** 2
         and fwd['lo'] <= fwd['hi'] <= fwd['closed'] <= fwd['modern_e'] <= fwd['modern_r'] <= target_comparison
         and rev['lo'] <= rev['hi'] <= rev['closed'] <= rev['modern_e'] <= rev['modern_r'] <= target_comparison
         and fwd['lead'] < fwd['lo'], 'comparison_coefficients_at_cap',
         formula='b(N) = (2|tau|/(3C v)) (e^{vU}-1-vU) sum_f sum_{x in R, y in O(f)} F(d(x,y)) <= K (5N+1) N^-3, '
                 'K = 112|tau| E(vU)/(vC) = 508032 tau^2 U^2 E(x)/x^2 (inner F1)',
         forward={'enclosure': [q(rdown(fwd['lo'])), q(rup(fwd['hi']))], 'closed_skeptic_form': q(fwd['closed']),
                  'modern_form_exact_e_upper': q(rup(fwd['modern_e'])), 'modern_form_1_over_1_minus_x': q(fwd['modern_r']),
                  'leading_not_a_bound': q(fwd['lead'])},
         reverse={'enclosure': [q(rdown(rev['lo'])), q(rup(rev['hi']))], 'closed_skeptic_form': q(rev['closed']),
                  'modern_form_exact_e_upper': q(rup(rev['modern_e'])), 'leading_not_a_bound': q(rev['lead'])})
    margins = {'forward': target_comparison / fwd['hi'], 'reverse': target_comparison / rev['hi']}
    need(margins['forward'] > 2 and margins['reverse'] > 4, 'comparison_margins',
         forward=preview(margins['forward']), reverse=preview(margins['reverse']))
    need(duhamel(F(112), phi_aq, abs(-tau)) == duhamel(F(112), phi_aq, tau)
         and duhamel(F(112), phip_ay, abs(-tau)) == duhamel(F(112), phip_ay, tau), 'comparison_both_signs_replay_same_abs_tau', note='every bound depends on |tau| only; the -tau value is a '
         'replay of the same |tau| formula, not a second confirmation')
    # exact refined comparison with the enumerated distance sums (labelled refinement)
    refined_b = {}
    for n in (2, 3, 4, 5):
        s_exact = F(fam_rows[n]['S_exact'])
        refined_b[str(n)] = {'b_exact_sum_upper': q(rup(fwd['hi'] * s_exact / 168)),
                             'b_crude': q(rup(fwd['hi'] * F(5 * n + 1, n ** 3))),
                             'preview_exact': preview(fwd['hi'] * s_exact / 168),
                             'preview_crude': preview(fwd['hi'] * F(5 * n + 1, n ** 3))}
    need(all(F(r['b_exact_sum_upper']) < F(r['b_crude']) for r in refined_b.values()), 'comparison_exact_distance_sums_labelled',
         rows=refined_b, note='b_exact = K * S_N / 168 with the enumerated S_N; a labelled refinement, not the target form')
    # first order vanishes: all extra-face owner sets are disjoint from R for N >= 2
    need(all(fam_rows[n]['min_l1_to_e_z'] >= 1 for n in (2, 3, 4, 5)) and fwd['lead'] / tau ** 2 == 254016,
         'duhamel_first_order_vanishes', reason='disjoint supports: [V_f, A]=0 for N at least 2, so the integrand '
         '||[V_f, T_s(A)]|| <= (2/C)(e^{vs}-1)... vanishes at s=0; the bound is O(tau^2 U^2)',
         limit_over_tau2='254016 (forward), 148176 (reverse)')

    # 8. Cauchy coefficients --------------------------------------------------------------------
    tails_ok = all(F(4, k) >= sum((g[r] for r in range(k, 60)), F(0)) for k in range(1, 30))
    need(all(4 * r * r + 2 <= 4 * (1 + r) ** 2 for r in range(0, 500)) and tails_ok, 'shell_tail_bound_4_over_k',
         statement='sum_{r>=k}(4r^2+2)(1+r)^-4 <= 4 sum_{m>=k+1} m^-2 <= 4/k; with k=N-1 (from e_z) and k=N (from 0) '
                   'the R-sum over |y|_inf at least N is at most 4/(N-1)+4/N <= 8/(N-1)')
    cy = {}
    for name, pref, phi in (('F1_star_charged_Phi', F(448), phi_aq), ('F1_face_charged_Phi', F(784, 3), phi_aq),
                            ('F2_face_charged_Phiprime', F(784, 3), phip_ay), ('F2_group_charged_Phiprime', F(448), phip_ay)):
        lo_, hi_, cl, me, mr, lead = duhamel(pref, phi, tau)
        cy[name] = {'lo': lo_, 'hi': hi_, 'closed': cl, 'modern_e': me, 'lead': lead}
    # F2 Cauchy through F1 (forward-possible): sup_{M>N} <= [K_C1 + 2K (5N+1)(N-1)N^-3]/(N-1) <= (K_C1 + (11/4)K)/(N-1)
    fmax = max(F((5 * n + 1) * (n - 1), n ** 3) for n in range(2, 2000))
    tri = cy['F1_star_charged_Phi']['hi'] + 2 * fmax * fwd['hi']
    need(fmax == F(11, 8) and all(5 * n * n > 8 * n + 3 for n in range(2, 100))
         and all(v_['hi'] <= target_cauchy for v_ in cy.values()) and tri <= target_cauchy,
         'cauchy_coefficients_all_M', rows={k: {'enclosure': [q(rdown(v_['lo'])), q(rup(v_['hi']))],
                                                  'closed_skeptic_form': q(v_['closed']),
                                                  'lead_over_tau2': q(v_['lead'] / tau ** 2)} for k, v_ in sorted(cy.items())},
         f2_via_f1_triangle=q(rup(tri)), triangle_factor='max_N (5N+1)(N-1)/N^3 = 11/8 at N=2 (decreasing for N at least 2)',
         margins={k: preview(target_cauchy / v_['hi']) for k, v_ in sorted(cy.items())})
    ident_vals = [fwd['hi'] * F(5 * n + 1, n ** 3) + cy['F1_star_charged_Phi']['hi'] / (n - 1) for n in (2, 3, 5, 10, 100, 1000)]
    ident_n = {str(n): preview(v_) for n, v_ in zip((2, 3, 5, 10, 100, 1000), ident_vals)}
    need(all(ident_vals[i] > ident_vals[i + 1] for i in range(5)) and ident_vals[-1] < F(11, 10 ** 14)
         and cy['F2_face_charged_Phiprime']['hi'] / 999 < F(4, 10 ** 14), 'f2_limit_identification_rate', bound_via_F1=ident_n,
         bound_via_F2_own_cauchy='K_C2/(N-1) with K_C2 = %s (face charged)' % preview(cy['F2_face_charged_Phiprime']['hi']),
         statement='||T^{F2,N}_theta(A)-T_theta(A)|| <= K(5N+1)N^-3 + K_C1/(N-1) -> 0 for A in B(H_R); for A in A_Y the '
                   'same Duhamel sum with R replaced by Y tends to 0; T and the F2 limit are automorphisms equal on the '
                   'local algebra, hence equal')

    # 9. tau/100 scaling ------------------------------------------------------------------------
    def ratio(pref, phi, form):
        a = duhamel(pref, phi, tau)
        b_ = duhamel(pref, phi, tau / 100)
        if form == 'closed':
            return a[2] / b_[2]
        if form == 'modern_r':
            return a[4] / b_[4]
        if form == 'enclosure':
            return a[0] / b_[1], a[1] / b_[0]
        if form == 'modern_e':
            return a[3] / duhamel(pref, phi, tau / 100)[3]
        raise CheckFailure('form')

    rs = {'comparison_forward_closed': ratio(F(112), phi_aq, 'closed'),
          'comparison_forward_modern_1_over_1_minus_x': ratio(F(112), phi_aq, 'modern_r'),
          'comparison_reverse_closed': ratio(F(112), phip_ay, 'closed'),
          'cauchy_F1_closed': ratio(F(448), phi_aq, 'closed'),
          'cauchy_F2_face_closed': ratio(F(784, 3), phip_ay, 'closed')}
    enc_f = ratio(F(112), phi_aq, 'enclosure')
    enc_r = ratio(F(112), phip_ay, 'enclosure')
    lo_b, hi_b = br['comparison_coefficient']
    need(all(lo_b <= r_ <= hi_b for r_ in rs.values()) and lo_b <= enc_f[0] <= enc_f[1] <= hi_b
         and lo_b <= enc_r[0] <= enc_r[1] <= hi_b and not (rs['comparison_forward_modern_1_over_1_minus_x'] <= 10100)
         and rs['comparison_forward_closed'] <= 10100, 'tau_scaling_ratios_in_brackets',
         exact={k: q(v_) for k, v_ in sorted(rs.items())}, previews={k: preview(v_) for k, v_ in sorted(rs.items())},
         sharp_forward_enclosure=[preview(enc_f[0]), preview(enc_f[1])],
         sharp_reverse_enclosure=[preview(enc_r[0]), preview(enc_r[1])],
         stale_bracket_note='[9900,10100] (control semantics) rejects the valid modern form (ratio about 10101.6)')
    lin = (2 * tau * 168 * U) / (2 * (tau / 100) * 168 * U)
    need(not (lo_b <= lin <= hi_b) and lin == 100, 'linear_label_rejected_by_bracket', linear_ratio='100')

    # 10. reconciliation of the recorded loop-1 previews -----------------------------------------
    m_ = re.search(r'at \|theta\|=8: ([0-9.]+)e-11 \(skeptic\) and ([0-9.]+)e-11 \(modern', delib)
    p_s, p_m = F(m_.group(1)), F(m_.group(2))
    gap_pct = F(re.search(r'the ([0-9.]+)% gap between the two previews', delib).group(1))
    rev_prev = F(re.search(r'reverse-route preview about ([0-9.]+)e-11', delib).group(1))
    cau_prev = F(re.search(r'within-family Cauchy coefficient about ([0-9.]+)e-10', delib).group(1))
    elo, ehi = e2_enclosure(v)
    xlo, xhi = exp_enclosure(v)
    ratio_lo, ratio_hi = xlo / (2 * ehi), xhi / (2 * elo)  # M/S = e^v (v^2/2)/E(v)
    half = F(5, 10 ** 15)  # half a unit in the fourth significant digit of a value near 2.5e-11
    s_int = (p_s * F(1, 10 ** 11) - half, p_s * F(1, 10 ** 11) + half)
    m_int = (p_m * F(1, 10 ** 11) - half, p_m * F(1, 10 ** 11) + half)
    need(p_s == F('2.549') and p_m == F('2.566') and gap_pct == F('0.67')
         and s_int[0] <= fwd['hi'] <= s_int[1] and m_int[0] <= fwd['modern_e'] <= m_int[1]
         and m_int[0] / s_int[1] <= ratio_lo <= ratio_hi <= m_int[1] / s_int[0]
         and abs(rev['hi'] * 10 ** 11 - rev_prev) < F(1, 1000) and abs(cy['F1_star_charged_Phi']['hi'] * 10 ** 10 - cau_prev) < F(1, 10000),
         'loop1_preview_gap_reconciled', recorded={'skeptic': '2.549e-11', 'modern': '2.566e-11', 'gap': '0.67%'},
         exact_ratio_modern_over_skeptic=[preview(ratio_lo), preview(ratio_hi)],
         relative_gap_to_skeptic=preview(ratio_hi - 1), relative_gap_to_modern=preview(1 - 1 / ratio_hi),
         explanation='the whole gap is the exponential remainder: modern bounds e^x-1-x by (x^2/2)e^x, the skeptic by '
                     '(x^2/2)/(1-x/3), at x = vU = 3969/390625; both use the same face-distance sum 168(5N+1)N^-3 '
                     '(|R|=2, at most 3 owners, F(N-1)=N^-4)')

    # 11. fixtures ------------------------------------------------------------------------------
    # (a) polynomial versus exponential tail: T(k) >= k g(2k-1) >= 1/(4k) for every k
    poly_ok = all(k * F(4 * (2 * k - 1) ** 2 + 2, (2 * k) ** 4) >= F(1, 4 * k) for k in range(1, 300))
    cross = min(n for n in range(2, 200) if F(1, 2) ** n < F(1, 4 * (n - 1)))
    need(poly_ok and cross == 4, 'fixture_polynomial_versus_exponential_tail',
         statement='the shell tail of F(r)=(1+r)^-4 from distance k is at least 1/(4k) for every k, so the Cauchy '
                   'bound decays like 1/N and cannot be restated as K q^N; q=1/2, K=1 falls below it from N=4',
         labelled_exponential_instance='F_mu=e^{-mu r}F: C_{F_mu} <= 224, ||Phi||_{F_mu} <= e^{2mu} 2268|tau|; own labelled '
                                       'constants; no target frozen; no admission weight')
    # (b) unbounded on-site term placed in Phi: velocity grows with the spin cutoff
    jlist = [F(1, 2), F(1), F(5), F(50)]
    onsite_norm = [8 * 24 * j * (j + 1) for j in jlist]
    v_mis = [2 * c_up * 81 * (j_aq * tau + n_) for n_ in onsite_norm]
    need(all(onsite_norm[i] < onsite_norm[i + 1] for i in range(3)) and onsite_norm[0] == 144 and onsite_norm[-1] == 489600
         and all(vm / v > 10 ** 6 for vm in v_mis),
         'fixture_onsite_term_misplaced', truncated_onsite_norms=[q(x) for x in onsite_norm],
         misplaced_velocity_over_correct=[preview(vm / v) for vm in v_mis],
         statement='with h_x inside Phi the F-norm is at least ||h_x 1[spin<=j]|| = 8*24*j(j+1), unbounded in the '
                   'cutoff; with the interaction-picture placement (h_x in (44)) the velocity is 1016064|tau| at every cutoff')
    # (c) padding factorization, exact commutator series
    hin = mat([[1, F(1, 2)], [F(1, 2), 0]])
    a_op = mat([[0, 1], [1, 0]])
    hpad = mat([[0, 0, 0], [0, 1, 0], [0, 0, 2]])
    big = madd(kron(hin, eye(3)), kron(eye(2), hpad))
    x_big = kron(a_op, eye(3))
    x_small = a_op
    pad_ok = True
    for _ in range(7):
        x_big = comm(big, x_big)
        x_small = comm(hin, x_small)
        pad_ok = pad_ok and x_big == kron(x_small, eye(3))
    need(pad_ok and is_zero(comm(kron(eye(2), hpad), kron(a_op, eye(3)))), 'fixture_padding_factorizes_exactly',
         statement='ad^k_{H_in (x) 1 + 1 (x) h_pad}(A (x) 1) = (ad^k_{H_in} A) (x) 1 for k=1..7, so the padded evolution '
                   'is T^{F2,N}(A) (x) 1; charging the padding terms instead puts ||h_pad 1[<=L]|| = L into the source, '
                   'unbounded in the cutoff L, while their exact contribution is 0')
    # (d) Duhamel sign and telescoping identity on a two-site toy; first order vanishes for disjoint V
    s2 = mat([[1, 0], [0, -1]])
    sx = mat([[0, 1], [1, 0]])
    h1 = madd(madd(kron(mat([[0, 0], [0, 1]]), eye(2)), kron(eye(2), mat([[0, 0], [0, 2]]))), kron(sx, sx), F(1, 5))
    vv_ = kron(eye(2), mat([[F(1, 7), F(1, 3)], [F(1, 3), 0]]))
    h2 = madd(h1, vv_)
    a4 = kron(s2, eye(2))
    tel_ok = True
    for n_ in range(1, 7):
        lhs2, lhs1 = a4, a4
        for _ in range(n_):
            lhs2, lhs1 = comm(h2, lhs2), comm(h1, lhs1)
        lhs = madd(lhs2, lhs1, -1)
        rhs = [[F(0)] * 4 for _ in range(4)]
        for j in range(n_):
            k = n_ - 1 - j
            term = a4
            for _ in range(k):
                term = comm(h1, term)
            term = comm(vv_, term)
            for _ in range(j):
                term = comm(h2, term)
            rhs = madd(rhs, term)
        tel_ok = tel_ok and lhs == rhs
    need(tel_ok and is_zero(comm(vv_, a4)) and not is_zero(comm(vv_, comm(h1, a4))), 'fixture_duhamel_identity_exact',
         statement='Taylor coefficients of T2_u(A)-T1_u(A) and of i int_0^u T2_s([H2-H1, T1_{u-s}(A)]) ds agree to order 6 '
                   '(ad_{H2}^n - ad_{H1}^n = sum_{j+k=n-1} ad_{H2}^j ad_V ad_{H1}^k); [V,A]=0 for disjoint supports kills '
                   'the first order, while [V,[H1,A]] survives through the coupling')
    # (e) N to N+1 bound summed: harmonic divergence
    hsum, ok_h = F(0), True
    for mth in range(1, 2 ** 10 + 1):
        hsum += F(1, mth)
        if mth & (mth - 1) == 0:
            k = mth.bit_length() - 1
            ok_h = ok_h and hsum >= 1 + F(k, 2)
    need(ok_h, 'fixture_n_to_n_plus_1_bound_is_not_cauchy', statement='per-step bounds c/(N-1) sum to c H_{M-1} >= '
         'c(1+k/2) at M-1=2^k: no finite Cauchy constant; the valid estimate sums every shell beyond N-1 at once')
    # (f) fixed vector versus moving vector: U(t)e_j = e^{ijt}e_j, A e_j = e_{2j}, t = pi/n. A phase e^{i pi k/n}
    # is tracked by its index k mod 2n; it equals -1 exactly when k = n mod 2n and +1 when k = 0 mod 2n.
    ok_fm = True
    for n_ in range(1, 41):
        k_uau = (-n_ + 2 * n_) % (2 * n_)  # U A U* e_n = e^{-i n t} U e_{2n} = e^{i pi (2n-n)/n} e_{2n}
        coeff = (-1 if k_uau == n_ else 1 if k_uau == 0 else None)
        ok_fm = ok_fm and coeff is not None and coeff - 1 == -2  # (U A U* - A) e_n = -2 e_{2n}: norm 2 for every n
        ok_fm = ok_fm and (F(22, 7 * n_) < F(1, 10)) == (n_ >= 32)  # |U e_1 - e_1| <= pi/n <= 22/(7n) -> 0
    need(ok_fm, 'fixture_fixed_versus_moving_vector', statement='||U(pi/n) A U(pi/n)* - A|| = 2 for every n (witness '
         'e_n), while U(t) e_1 -> e_1: the dynamics topology is per fixed local A, uniformly on compact windows')
    # (g) cross-coupling: +tau and -tau limits are certifiably different (AY2 gate)
    ay2 = json.loads((ROOT / 'research/round32/advisor/ay2-gate.json').read_text())['accepted']
    sep = F(re.search(r"sqrt\(10\)\|tau\|/36-2K_2' tau\^2 >= (\d+/\d+)", ay2).group(1))
    need(sep > F(875, 10 ** 12), 'fixture_cross_coupling_separation', plus_minus_separation_lower=q(sep),
         preview=preview(sep), statement='a +tau/-tau comparison is not a boundary comparison')
    # (h) algebraic dynamics equality does not give equal correlation functions of different states
    z2 = mat([[1, 0], [0, -1]])
    rho1, rho2 = mat([[1, 0], [0, 0]]), mat([[0, 0], [0, 1]])
    corr1 = sum(mmul(rho1, z2)[i][i] for i in range(2))
    corr2 = sum(mmul(rho2, z2)[i][i] for i in range(2))
    need(corr1 == 1 and corr2 == -1, 'fixture_same_dynamics_different_states',
         statement='one dynamics (identity), two states: omega(Z)=+1 and omega\'(Z)=-1; equal algebraic dynamics does '
                   'not give equal correlation functions of different states (BB2 needed)')
    # (i) placeholder rule: fixed regex keeps inequality text; old regex misread it
    ineq = 'J<=28|tau| for |tau|<=10^-8 and N>=2'
    need(placeholder_spans(ineq) == [] and placeholder_spans(ineq, OLD_PLACEHOLDER) != []
         and placeholder_spans('value <to be filled>') == ['<to be filled>'] and
         all(placeholder_spans(s_) == [] for s_ in strings(con)), 'placeholder_rule_mirrored',
         freezer_sha256_mirrored=FREEZER_MIRRORED_SHA256)
    need(affirmative_hits(sentence, forbidden, sentence) == [] and
         affirmative_hits('This is not the thermodynamic limit.', forbidden) == [] and
         affirmative_hits('The thermodynamic limit of the dynamics exists.', forbidden) == ['the thermodynamic limit'],
         'phrase_scan_mirrored', phrase_scan_sha256_mirrored=PHRASE_SCAN_MIRRORED_SHA256,
         known_weakness='clause-wide negation: "X holds and not Y" passes even when X is forbidden (loop-2 tool note)')

    # 12. validator and controls ------------------------------------------------------------------
    gate_fields = dict(pre['gate_fields_required'])
    ctx = {'tau': tau, 'declared_inputs': declared_inputs, 'isolation_forbidden': isolation_forbidden,
           'control_ids': control_ids, 'lr_quote': lr_quote, 'bracket': br['comparison_coefficient'],
           'K_min': {('F1', F(2268)): fwd['lo'], ('F2', F(1323)): rev['lo'], ('F2', F(2268)): fwd['lo']},
           'C_min': {('F1', 'Phi', 'star'): cy['F1_star_charged_Phi']['lo'], ('F1', 'Phi', 'face'): cy['F1_face_charged_Phi']['lo'],
                     ('F2', "Phi'", 'face'): cy['F2_face_charged_Phiprime']['lo'],
                     ('F2', "Phi'", 'group'): cy['F2_group_charged_Phiprime']['lo'],
                     ('F2', 'via F1 triangle', 'star'): cy['F1_star_charged_Phi']['lo']},
           'target_comparison': target_comparison, 'target_cauchy': target_cauchy, 'sentence': sentence,
           'forbidden': forbidden, 'gate_fields': gate_fields,
           'error_terms': list(pre['error_terms_itemized'])}
    statements = [
        'For every A in B(H_R) and |theta| at most 8, the F1 and F2 finite-box Heisenberg evolutions on Lambda_N differ '
        'by at most K (5N+1) N^-3 ||A||; this is an algebraic comparison on a compact window, not equality of the GNS '
        'dynamics of different states.',
        'The within-family estimates hold for all M greater than N at the rate 1/(N-1) in N at fixed spacing; they are '
        'not uniform in the lattice spacing a and do not decay exponentially in N.',
        'The F2 finite-box evolutions converge as a whole sequence to the AQ1 limit dynamics; the F2 limit states are '
        'subsequential and are not identified with the AQ1 state.',
    ]

    def packet(route):
        inner = 'F1' if route == 'forward' else 'F2'
        c_ = fwd if route == 'forward' else rev
        pk = {
            'route': route, 'contract_sha256': CONTRACT_SHA256, 'ns_excerpt_sha256': NS_EXCERPT_SHA256,
            'ns_pdf_sha256': NS_PDF_SHA256, 'inputs': list(declared_inputs),
            'controls': {k: True for k in control_ids},
            'model_id': MODEL_ID, 'triple': ['0', '0', '0'], 'group': 'SU(2)', 'lattice': 'Z^3 coarse 24-link factors',
            'model_is_finite_graph': False, 'tau_abs': tau, 'signs': ['+', '-'], 'same_coupling': True,
            'compared_couplings': ['same tau'], 'families': list(FAMILIES), 'N_min': 2, 'cover': list(R_COVER),
            'cover_links': 48, 'cover_endpoints': 36,
            'face_counts': {'per_site': 49, 'owner_sets_per_site': 15, 'meeting_R': 82, 'inside_R': 10},
            'face_count_source': 'I1 table by translation covariance, all sites',
            'stars_per_site': 4, 'J_over_tau': 28, 'stars_meeting_R': 7,
            'parameters': {'metric': METRIC, 'weights': F_DECL, 'window': '|theta| at most 8', 'N_min': 2, 'clock': CLOCK},
            'lr_source': NS_EXCERPT_REL, 'lr_quote': lr_quote, 'lr_theorem': 'Theorem 3.1, eqs. (51)-(52)',
            'limit_theorem': 'Theorem 4.1, eq. (77)', 'F': F_DECL, 'C_upper': 224,
            'constant_substitution': 'upper bounds for C and ||Phi||_F justified by monotonicity',
            'exponential_instance': None,
            'onsite_placement': 'interaction picture: H_x=h_x in (44), Phi bounded', 'onsite_in_phi': False,
            'lr_applied_to': 'bounded interaction Phi only',
            'clock': CLOCK, 'theta_max': 8, 'u_over_theta': F(1, 8), 'U': 1, 'uniform_in_time_claimed': False,
            'topology': TOPOLOGY, 'dynamics_level': DYNAMICS_LEVEL, 'gns_dynamics_equality_claimed': False,
            'source': {'terms': 'faces with owner set in Lambda_N whose anchor star is not in Lambda_N',
                       'old_terms_included': False, 'terms_meet_source_set': True, 'padding_charged': False,
                       'padding_factorization': 'exact (commutes with H^(2)_N, faces and B(H_R))',
                       'count': '28N(5N+1)', 'owners_max': 3, 'dist_ez': 'N-1', 'dist_0': 'N', 'enumerated_N': [2, 3],
                       'all_size_argument': True, 'each_face_once': True},
            'regrouping': {'charging': 'face by face', 'per_site_face_sum_over_tau': F(49, 3), 'double_charged': False},
            'comparison': {'inner_family': inner, 'interaction': 'Phi' if inner == 'F1' else "Phi'",
                           'phi_over_tau': F(2268) if inner == 'F1' else F(1323), 'tier': 'polynomial_lieb_robinson',
                           'route_label': ROUTE_OF_INNER[inner], 'combine': 'linear', 'form': 'directed E(x)/x^2',
                           'tau_order': 2, 'first_order_reason': 'disjoint supports: [V_f, A]=0 for N at least 2',
                           'scaling_ratio': rs['comparison_forward_closed'] if inner == 'F1' else rs['comparison_reverse_closed'],
                           'coefficient': c_['closed'], 'n_dependence': '(5N+1)N^-3'},
            'bracket': list(br['comparison_coefficient']),
            'cauchy': {'F1': {'interaction': 'Phi', 'charging': 'star', 'coefficient': cy['F1_star_charged_Phi']['closed'],
                              'rate': '1/(N-1)', 'quantifier': 'all M greater than N', 'tier': CONTROL_TIER,
                              'scaling_ratio': rs['cauchy_F1_closed']},
                       'F2': {'interaction': "Phi'", 'charging': 'face', 'coefficient': cy['F2_face_charged_Phiprime']['closed'],
                              'rate': '1/(N-1)', 'quantifier': 'all M greater than N', 'tier': CONTROL_TIER,
                              'scaling_ratio': rs['cauchy_F2_face_closed']}},
            'f2_limit': {'whole_sequence': True, 'whole_sequence_via': 'Cauchy bound over all M greater than N',
                         'identified_with': 'T_theta (AQ1 limit dynamics)', 'identification_via': 'comparison bound',
                         'sections_4_5_rerun': True, 'subsequences': 'F2 own diagonal extraction'},
            'targets_met': {'comparison': True, 'cauchy': True}, 'verdict': 'accepted_within_scope',
            'dominating_term': None, 'retuned': False,
            'uniform_in': UNIFORM_IN, 'rate_unit': RATE_UNIT, 'sub_label': SUB_LABEL,
            'statements': list(statements), 'sentence': sentence, 'sentence_count': 1,
            'gate_fields': dict(gate_fields),
            'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False,
                       'uniform_in_a_claimed': False},
            'error_terms': list(pre['error_terms_itemized']),
        }
        pk['freeze_digest'] = packet_digest(pk)
        return pk

    base = packet('forward')
    base_rev = packet('reverse')
    need(validate(base, ctx) and validate(base_rev, ctx), 'reference_packets_accepted', routes=['forward', 'reverse'])

    def mut(src=None, rebind=True, **kw):
        src = base if src is None else src
        pk = copy.deepcopy(src)
        for k, val in kw.items():
            parts = k.split('__')
            tgt = pk
            for p_ in parts[:-1]:
                tgt = tgt[p_]
            tgt[parts[-1]] = val
        if rebind:
            pk['freeze_digest'] = packet_digest(pk)
        return lambda: validate(pk, ctx)

    ok = [('forward reference packet', lambda: validate(base, ctx)), ('reverse reference packet', lambda: validate(base_rev, ctx))]
    fwd_c, rev_c = base['comparison'], base_rev['comparison']
    control('coherent_evidence_tampering',
            [('control Boolean flipped, digest rebound', mut(controls__lieb_robinson_form_quoted=False), 'control booleans'),
             ('snapshot removed, digest rebound', mut(inputs=declared_inputs[1:]), 'snapshot inventory'),
             ('digest not rebound', mut(rebind=False, controls__topology_named=False), 'freeze digest'),
             ('coefficient below derivation', mut(comparison__coefficient=fwd['lo'] - F(1, 10 ** 20)), 'below the derivable'),
             ('contract rehashed', mut(contract_sha256='0' * 64), 'contract hash')], ok)
    control('exact_arithmetic_admission',
            [('float coefficient', mut(comparison__coefficient=float(fwd['closed'])), 'exact arithmetic'),
             ('float tau', mut(tau_abs=1e-8), 'exact arithmetic')], ok)
    control('no_priority_or_continuum_claim',
            [('continuum', mut(claims__continuum_claim=True), 'forbidden claim continuum_claim'),
             ('priority', mut(claims__scientific_priority_verified=True), 'forbidden claim scientific_priority'),
             ('weak coupling', mut(claims__weak_coupling_claim=True), 'forbidden claim weak_coupling_claim')], ok)
    control('changed_model_relabelled',
            [('tau 1e-9 under the label', mut(tau_abs=F(1, 10 ** 9)), 'changed model'),
             ('uniform triple', mut(triple=['tau/24', 'tau/24', 'tau/24']), 'changed model'),
             ('SU(3)', mut(group='SU(3)'), 'changed model'),
             ('2D lattice', mut(lattice='Z^2 single-site factors'), 'changed model'),
             ('finite graph', mut(model_is_finite_graph=True), 'changed model'),
             ('fine-site metric', mut(parameters__metric='l1 on fine sites'), 'changed model relabelled: metric')], ok)
    limited_ok = mut(comparison__coefficient=F(7, 10 ** 11), targets_met={'comparison': False, 'cauchy': True},
                     verdict='limited', dominating_term='lieb_robinson_tail at the frozen tau')
    control('insufficient_verdict_retained',
            [('missed target accepted', mut(comparison__coefficient=F(7, 10 ** 11),
                                            targets_met={'comparison': False, 'cauchy': True}), 'insufficient verdict'),
             ('limited without dominating term', mut(comparison__coefficient=F(7, 10 ** 11),
                                                     targets_met={'comparison': False, 'cauchy': True}, verdict='limited'),
              'dominating term'),
             ('retuned', mut(retuned=True), 'retuned'),
             ('targets_met misreported', mut(targets_met={'comparison': True, 'cauchy': False}), 'targets_met inconsistent')],
            ok + [('limited packet with missed target and dominating term', limited_ok)])
    control('tau_scaling_exponent',
            [('ratio of a linear bound', mut(comparison__scaling_ratio=F(100)), 'tau scaling'),
             ('bracket chosen after evaluation', mut(bracket=[F(9900), F(10100)]), 'tau scaling'),
             ('Cauchy ratio sqrt', mut(cauchy__F1__scaling_ratio=F(10)), 'tau scaling')],
            ok + [('modern form ratio 10101.6', mut(comparison__scaling_ratio=rs['comparison_forward_modern_1_over_1_minus_x']))],
            note='the modern form is accepted under the preregistered [9500,10500]; see the recorded bracket defect')
    control('wrong_delta_alpha_hbar_clock',
            [('u window labelled theta (U=8)', mut(U=8), 'window'),
             ('Round29 dictionary label s=delta*t/hbar', mut(clock='s=delta*t/hbar', parameters__clock='s=delta*t/hbar'),
              'clock'),
             ('u over theta = 8', mut(u_over_theta=F(8)), 'window')], ok)
    control('missing_incoming_stars',
            [('outgoing star only', mut(J_over_tau=7), 'incident stars'),
             ('one star per site', mut(stars_per_site=1), 'incident stars'),
             ('four stars meeting R', mut(stars_meeting_R=4), 'incident stars')], ok)
    control('root_n_misuse',
            [('sqrt of the face count', mut(comparison__combine='rss'), 'root-N')], ok)
    control('tier_mixing_rejected',
            [('exponential tier with AQ1 constants', mut(comparison__tier='exponential_lieb_robinson'), 'tier mixing'),
             ('route label of the other family', mut(comparison__route_label='duhamel_inner_f2'), 'tier mixing'),
             ('Cauchy tier missing', mut(cauchy__F1__tier='crude_majorant'), 'tier mixing')], ok)
    control('reverse_premise_isolation',
            [('triage in reverse', mut(src=base_rev, inputs=declared_inputs + ['research/round33/skeptic/triage.md']),
              'reverse premise isolation'),
             ('deliberation-2 in reverse', mut(src=base_rev, inputs=declared_inputs + [DELIBERATION_REL]),
              'reverse premise isolation'),
             ('forward BA2 report in reverse', mut(src=base_rev, inputs=declared_inputs + ['research/round33/forward/ba2/report.md']),
              'reverse premise isolation')], ok,
            scope='recorded producer inventories equal the contract inventory (29 files); the mutations run on the '
                  'contract-derived inventory')
    control('face_count_all_sites',
            [('site-0-only count', mut(face_counts={'per_site': 21, 'owner_sets_per_site': 6, 'meeting_R': 82, 'inside_R': 10}),
              'face count'),
             ('literal 84', mut(face_counts={'per_site': 84, 'owner_sets_per_site': 15, 'meeting_R': 82, 'inside_R': 10}),
              'face count'),
             ('typed literals', mut(face_count_source='typed'), 'face count')], ok)
    control('uniform_in_N_not_in_a',
            [('uniform in N and a', mut(uniform_in='N and a'), 'uniform in N not in a'),
             ('statement', mut(statements=['The constants are uniform in a.']), 'uniform in N not in a')], ok)
    control('placeholder_span_rejected',
            [('placeholder in a statement', mut(statements=statements + ['The rate is <to be filled>.']), 'placeholder span')],
            ok + [('inequality text', mut(statements=statements + ['Here J<=28|tau| for N>=2.']))])
    control('negation_aware_phrase_scan',
            [('affirmative forbidden phrase', mut(statements=['The thermodynamic limit of the dynamics exists.']),
              'forbidden phrasing'),
             ('NS section title quoted affirmatively', mut(statements=[title_clause + ' gives the limit.']),
              'forbidden phrasing'),
             ('the AQ state', mut(statements=['The AQ state is invariant.']), 'forbidden phrasing')],
            ok + [('negated mention', mut(statements=['This is not the thermodynamic limit of any state.']))])
    control('parameters_declare_metric_weights_window',
            [('window missing', mut(parameters={'metric': METRIC, 'weights': F_DECL, 'N_min': 2, 'clock': CLOCK}),
              'parameters must declare'),
             ('clock missing', mut(parameters={'metric': METRIC, 'weights': F_DECL, 'window': '|theta| at most 8',
                                               'N_min': 2}), 'parameters must declare')], ok)
    control('lieb_robinson_polynomial_tail',
            [('exponential rate in N', mut(cauchy__F1__rate='e^{-mu N}'), 'polynomial tail'),
             ('N to N+1 bound summed', mut(cauchy__F1__quantifier='N to N+1'), 'N to N+1'),
             ('comparison decays exponentially', mut(comparison__n_dependence='e^{-mu(N-1)}'), 'polynomial tail')], ok,
            fixture='fixture_polynomial_versus_exponential_tail')
    control('lieb_robinson_F_declared',
            [('F changed', mut(F='F(r)=e^{-r}'), 'F declared'),
             ('exponential instance with AQ1 constants', mut(exponential_instance={'labelled': True, 'target': None,
                                                                                    'phi_over_tau': '2268', 'C_upper': 224,
                                                                                    'admission_weight': False}),
              'exponential instance'),
             ('exponential instance given admission weight',
              mut(exponential_instance={'labelled': True, 'target': None, 'phi_over_tau': 'e^{2mu}*2268', 'C_upper': 224,
                                        'admission_weight': True}), 'exponential instance')],
            ok + [('labelled exponential extra', mut(exponential_instance={'labelled': True, 'target': None,
                                                                          'phi_over_tau': 'e^{2mu}*2268', 'C_upper': 224,
                                                                          'admission_weight': False}))])
    control('lieb_robinson_form_quoted',
            [('paraphrased (51)', mut(lr_quote='||[tau_t(A),B]|| <= 2||A|| ||B|| e^{v|t|} D(X,Y)'), 'form quoted'),
             ('quoted from the AQ1 report', mut(lr_source='research/round29/forward/aq1/report.md'), 'second-hand'),
             ('limit theorem misnamed', mut(limit_theorem='Theorem 3.1'), 'form quoted')], ok)
    control('unbounded_onsite_interaction_picture',
            [('h_x inside Phi', mut(onsite_in_phi=True), 'interaction picture'),
             ('bounded bound on the full Hamiltonian', mut(lr_applied_to='full Hamiltonian H_N'), 'interaction picture')],
            ok, fixture='fixture_onsite_term_misplaced')
    control('duhamel_inner_family_constants',
            [('inner F1 with Phi prime constants', mut(comparison__interaction="Phi'", comparison__phi_over_tau=F(1323),
                                                       comparison__coefficient=rev['closed']), 'inner family'),
             ('reverse inner F2 with Phi unstated', mut(src=base_rev, comparison__interaction='Phi',
                                                        comparison__phi_over_tau=F(2268)), 'inner family'),
             ('forward labelled with inner F2', mut(comparison__inner_family='F2', comparison__interaction="Phi'",
                                                    comparison__phi_over_tau=F(1323), comparison__route_label='duhamel_inner_f2',
                                                    comparison__coefficient=rev['closed']), 'route')],
            ok + [('reverse with stated padded anchor groups', mut(src=base_rev,
                                                                   comparison__interaction='Psi_N padded anchor groups (stated)',
                                                                   comparison__phi_over_tau=F(2268),
                                                                   comparison__coefficient=fwd['closed']))])
    control('extra_face_count_and_distance',
            [('distance N instead of N-1', mut(source__dist_ez='N'), 'extra face count and distance'),
             ('count 28N(5N+1) replaced', mut(source__count='21(2N)^2'), 'extra face count and distance'),
             ('enumeration on Lambda_2 only', mut(source__enumerated_N=[2]), 'extra face count and distance'),
             ('padding charged', mut(source__padding_charged=True), 'padding')], ok,
            fixture='fixture_padding_factorizes_exactly')
    control('duhamel_tau_order_quadratic',
            [('linear label', mut(comparison__tau_order=1), 'tau order'),
             ('no first-order reason', mut(comparison__first_order_reason=''), 'tau order'),
             ('leading form without remainder', mut(comparison__form='leading order only'), 'leading form')], ok)
    control('time_window_named_common_clock',
            [('uniform in time', mut(uniform_in_time_claimed=True), 'uniform in time'),
             ('uniform in time gate field', mut(gate_fields__uniform_in_time_claimed=True), 'uniform in time'),
             ('window dropped', mut(theta_max=None), 'window')], ok)
    control('algebraic_not_gns_dynamics',
            [('GNS equality claimed', mut(gns_dynamics_equality_claimed=True), 'algebraic not gns'),
             ('gate field GNS', mut(gate_fields__gns_dynamics_equality_claimed=True), 'algebraic not gns'),
             ('common limit of states', mut(gate_fields__common_limit_claimed=True), 'algebraic not gns')], ok,
            fixture='fixture_same_dynamics_different_states')
    control('f2_limit_dynamics_equals_f1',
            [('identification missing', mut(f2_limit__identified_with='own Nachtergaele-Sims limit only'), 'equals f1'),
             ('sections 4-5 assumed', mut(f2_limit__sections_4_5_rerun=False), 'sections 4-5'),
             ('AQ1 subsequence reused', mut(f2_limit__subsequences='AQ1 chosen subsequence'), 'sections 4-5')], ok)
    control('two_families_named',
            [('one family', mut(families=FAMILIES[:1]), 'two families'),
             ('orthant substituted', mut(families=[FAMILIES[0], 'orthant boxes']), 'two families'),
             ('N at least 1', mut(N_min=1), 'two families')], ok)
    control('subsequence_versus_whole_sequence',
            [('whole sequence from compactness', mut(f2_limit__whole_sequence_via='AQ1 compactness'), 'whole sequence'),
             ('state convergence claimed', mut(gate_fields__state_convergence_claimed=True), 'states')], ok)
    control('decay_rate_in_N_not_a',
            [('rate in fm', mut(rate_unit='per fm'), 'decay rate in N not a'),
             ('rate in a claimed', mut(gate_fields__rate_in_a_claimed=True), 'decay rate in N not a')], ok)
    control('boundary_source_new_terms_only',
            [('old terms in the source', mut(source__old_terms_included=True), 'new terms only'),
             ('new terms not meeting the source set', mut(source__terms_meet_source_set=False), 'new terms only')], ok)
    control('f2_regrouping_charged_once',
            [('face charged twice', mut(regrouping__double_charged=True), 'charged once'),
             ('per-site sum doubled', mut(regrouping__per_site_face_sum_over_tau=F(98, 3)), 'charged once'),
             ('Cauchy double charging', mut(cauchy__F2__charging='double'), 'charged once')], ok)
    control('full_original_wilson_cover',
            [('R={0}', mut(cover=[(0, 0, 0)]), 'wilson cover'),
             ('four drawn links', mut(cover_links=4), 'wilson cover')], ok)
    control('topology_named',
            [('norm continuity in time on B(H)', mut(topology='norm continuity in time on all of B(H)'), 'topology')], ok,
            fixture='fixture_fixed_versus_moving_vector')
    control('cross_coupling_comparison_rejected',
            [('different couplings', mut(same_coupling=False), 'cross-coupling'),
             ('+tau against -tau', mut(compared_couplings=['+tau', '-tau']), 'cross-coupling')], ok,
            fixture='fixture_cross_coupling_separation')
    control('gate_fields_topic_specific',
            [('dynamics_level missing', mut(gate_fields={k: v_ for k, v_ in gate_fields.items() if k != 'dynamics_level'}),
              'gate fields topic specific'),
             ('empty whole_sequence_scope', mut(gate_fields__whole_sequence_scope=''), 'gate fields topic specific'),
             ('uniqueness claimed', mut(gate_fields__uniqueness_of_ground_state_claimed=True), 'gate field claimed')], ok)
    # extra controls (not contract ids)
    control('lr_constant_substitution_monotone',
            [('C upper bound substituted without the monotonicity statement', mut(constant_substitution='C=224 inserted'),
              'monotonicity')], ok)
    control('mandatory_sentence_once',
            [('sentence edited', mut(sentence=sentence.replace('not a uniform-in-time statement', 'a statement')),
              'mandatory sentence'),
             ('sentence split', mut(sentence_count=2), 'mandatory sentence')], ok)
    control('error_terms_itemized',
            [('interaction-picture term dropped', mut(error_terms=[t for t in pre['error_terms_itemized']
                                                                    if t != 'interaction_picture_onsite']), 'error term')], ok)

    ids = set(control_ids)
    done = {row['id'] for row in CHECKS if row.get('kind') == 'control'}
    missing = sorted(ids - done)
    need(not missing, 'contract_controls_covered', implemented=len(ids & done), of=len(ids), deferred=missing)

    predictions = {
        'comparison_forward_inner_F1': {'value': preview(fwd['hi']), 'closed_form': '254016 tau^2 U^2/(1-vU/3), v=1016064|tau|',
                                        'modern_form': preview(fwd['modern_e']), 'margin': preview(margins['forward']),
                                        'ratio_tau_over_100': preview(rs['comparison_forward_closed'])},
        'comparison_reverse_inner_F2': {'value': preview(rev['hi']), 'closed_form': '148176 tau^2 U^2/(1-v\'U/3), v\'=592704|tau|',
                                        'modern_form': preview(rev['modern_e']), 'margin': preview(margins['reverse']),
                                        'ratio_tau_over_100': preview(rs['comparison_reverse_closed'])},
        'cauchy_F1_star_Phi': preview(cy['F1_star_charged_Phi']['hi']),
        'cauchy_F1_face_Phi': preview(cy['F1_face_charged_Phi']['hi']),
        'cauchy_F2_face_Phiprime': preview(cy['F2_face_charged_Phiprime']['hi']),
        'cauchy_F2_group_Phiprime': preview(cy['F2_group_charged_Phiprime']['hi']),
        'cauchy_F2_via_F1_triangle': preview(tri),
        'cauchy_ratio_tau_over_100': {'F1': preview(rs['cauchy_F1_closed']), 'F2': preview(rs['cauchy_F2_face_closed'])},
        'extra_faces': '28N(5N+1): 616, 1344, 2352, 3640 (N=2..5); 11 of them reach l1 distance N-1 from e_z',
        'exact_distance_sum_over_crude': {k: v_['S_exact_over_crude'] for k, v_ in sorted((str(a), b) for a, b in fam_rows.items())},
    }
    return {
        'loop': 'BA2', 'stage': 'pre_comparison', 'reviewer': 'skeptic (model agent, correlated ancestry)',
        'human_author': 'Hruday N M (BUNZEEY)', 'contract_sha256': c_sha, 'contract_frozen_at': con['frozen_at'],
        'ns_excerpt_sha256': ns_sha, 'ns_pdf_sha256': NS_PDF_SHA256,
        'model': MODEL_ID + ': SU(2) Kogut-Susskind form on Z^3 at fixed spacing, coarse 24-link factors, selected triple '
                 '(0,0,0), Haar reference, 21 omitted faces per anchor entering as -(tau/3)W_f (delta=alpha/8); both signs '
                 '|tau|<=10^-8; cover R={0,e_z}; families F1 (AQ1 whole-star boxes) and F2 (I1 section 6 all-contained-face '
                 'boxes with padding) on Lambda_N=[-N,N]^3, N at least 2; Heisenberg dynamics on |theta| at most 8',
        'placement': {
            'onsite': 'H_x = h_x = 8 sum_e C_e (normalized by delta=alpha/8) in NS (44); unbounded, self-adjoint, compact '
                      'resolvent; enters only the interaction picture (54),(57); never inside Phi',
            'F1': 'H^(1)_N = sum_{x in Lambda_N} h_x + sum_{b+S in Lambda_N} Phi(b+S): the native restriction of the whole-star Phi',
            'F2': 'H^(2)_N = sum_{x in Lambda_N} h_x + sum_{O in Lambda_N} Phi\'(O): the native restriction of the owner-set Phi\'; '
                  'the padded operator is H^(2)_N (x) 1 + 1 (x) sum_{pad} h_x and its evolution of A in A_{Lambda_N} is '
                  'T^{F2,N}(A) (x) 1 exactly',
            'duhamel': 'H^(2)_N - H^(1)_N = sum over the 28N(5N+1) extra faces of -(tau/3)W_f, bounded; equal on-site sums cancel',
            'time': 'NS t = u = theta/8; NS tau_t^Lambda = T^{F,N}',
        },
        'geometry': {'per_site_faces': 49, 'per_site_owner_sets': 15, 'incoming_stars': 4, 'faces_meeting_R': 82,
                     'inside_R': 10, 'owner_types_per_anchor': {' '.join(str(t) for t in k): v for k, v in sorted(types0.items())},
                     'extra_face_classes': {'x': 17, 'y': 13, 'z': 5, 'xy': 10, 'xz': 3, 'yz': 1, 'xyz': 0},
                     'families': {str(k): v for k, v in sorted(fam_rows.items())}},
        'constants': {'C_upper': '224', 'F_norm': [q(rdown(part, 10 ** 12)), q(rup(fnorm_hi, 10 ** 12))],
                      'phi_over_tau': '2268', 'phiprime_over_tau': '1323', 'sharp_labelled': {'phi': '567', 'phiprime': '108'},
                      'v_over_tau': '1016064', 'vprime_over_tau': '592704'},
        'comparison': {'forward_inner_F1': {'enclosure': [q(rdown(fwd['lo'])), q(rup(fwd['hi']))], 'closed': q(fwd['closed'])},
                       'reverse_inner_F2': {'enclosure': [q(rdown(rev['lo'])), q(rup(rev['hi']))], 'closed': q(rev['closed'])},
                       'target': q(target_comparison)},
        'cauchy': {k: {'enclosure': [q(rdown(v_['lo'])), q(rup(v_['hi']))], 'closed': q(v_['closed'])} for k, v_ in sorted(cy.items())},
        'cauchy_target': q(target_cauchy),
        'scaling': {k: q(v_) for k, v_ in sorted(rs.items())},
        'predictions': predictions,
        'contract_readings': ['R1 preregistration brackets govern (stale [9900,10100] in control semantics)',
                              'R2 four control ids without semantics read by name and loop-2 BA2-N2',
                              'R3 observable.id N to N+1 read as sup over M greater than N',
                              'R4 fine-unit conversion is display only (no constant)',
                              'R5 Theorem 4.1 cited as Section 4, not by its title',
                              'R6 route labels duhamel_inner_f1/f2 from plan tier_label_rule; tier polynomial_lieb_robinson'],
        'gate_fields': gate_fields, 'sentence': sentence,
        'claims': {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False,
                   'uniform_in_a_claimed': False, 'uniqueness_of_ground_state_claimed': False},
        'error_terms': {'lieb_robinson_tail': 'F(N-1)=N^-4 per owner, |R|=2, at most 3 owners; Cauchy shell tail 4/(N-1)+4/N',
                        'duhamel_boundary_sum': '28N(5N+1) extra faces, each once, ||V_f||<=|tau|/3',
                        'interaction_picture_onsite': 'not_applicable as an error: on-site terms cancel in H2-H1 and are '
                                                      'placed in (44); padding factors exactly',
                        'inner_family_constants': 'F1 inner: Phi 2268|tau|; F2 inner: Phi\' 1323|tau|; C<=224 by monotonicity',
                        'arithmetic': 'exact rationals; e^x by Taylor enclosure with geometric remainder (30 terms)'},
        'deferred_parts': {'reverse_premise_isolation': 'actual inventories recorded by name and hash (29 files each, '
                                                        'identical to the repository); report contents checked at post-comparison'},
        'checks': CHECKS,
        'previews': {'K_forward': preview(fwd['hi']), 'K_reverse': preview(rev['hi']),
                     'K_forward_modern': preview(fwd['modern_e']), 'K_cauchy_F1': preview(cy['F1_star_charged_Phi']['hi']),
                     'K_cauchy_F2_face': preview(cy['F2_face_charged_Phiprime']['hi']),
                     'margin_forward': preview(margins['forward']), 'margin_reverse': preview(margins['reverse']),
                     'margin_cauchy_F1': preview(target_cauchy / cy['F1_star_charged_Phi']['hi']),
                     'modern_over_skeptic': preview(ratio_hi), 'ratio_forward': preview(rs['comparison_forward_closed']),
                     'ratio_reverse': preview(rs['comparison_reverse_closed'])},
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
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True, default=str) + '\n')
    n_controls = sum(1 for row in result['checks'] if row.get('kind') == 'control')
    n_mut = sum(len(row['mutations']) for row in result['checks'] if row.get('kind') == 'control')
    print(json.dumps({'checks': len(result['checks']), 'controls': n_controls, 'mutations': n_mut,
                      'K_forward': result['previews']['K_forward'], 'K_reverse': result['previews']['K_reverse'],
                      'K_cauchy_F1': result['previews']['K_cauchy_F1']}))


if __name__ == '__main__':
    main()
