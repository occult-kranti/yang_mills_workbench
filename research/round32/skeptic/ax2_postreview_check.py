#!/usr/bin/env python3
"""AX2 post-comparison skeptic checks, written after the single forward producer froze.

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated
ancestry (same model family as the advisor and the producer; the route-B
constants and the 1.9123e-7 feasibility value already appear in the skeptic's
own AX1 review, a shared premise); not human peer review or formal verification.

AX2 is single-direction (producers=["forward"], direction "single+skeptic"): its
admission rests on the forward producer plus the skeptic's frozen pre-comparison
replay (ax2_check.py, ax2-independent/results.json). This file adds:
  * integrity: contract, AX1 gate and AV2 gate hashes; the forward freeze closure
    file by file; the premise inventory (AGENTS.md + contract + 28 shared
    premises, each byte-identical to its repository source, no skeptic/ax2* or
    reverse/ax2 input, no reverse/ax2 package); the unchanged pre-comparison
    package;
  * an exact re-derivation in own code (nothing imported from the producer for
    it): D' from the AX1 tier-(ii) formula against the contract string and both
    gate texts; the rejected alternatives (AX1 reverse refinement, AX1 target
    4/10^7, AV1 zero-selected D, tier (i)); the route-B incidence (7 stars, 2
    single-factor groups, 153/88/82/6/16) and k'=51|tau|/4, local in N; the
    window transform and M_0=2, M_1=4s/pi by exact antiderivative identities;
    a Gauss-formula pi bracket and a power-series e^{-3} bracket (both to
    10^-60), different from the producer's Machin/alternating routines;
  * cross-checks of every exported rational: D', k', the four itemized terms,
    the exact radius and its 10^-40 ceiling, datum (= AV2 gate datum), interval,
    width, free enclosure, mirror, crossover, retained failures, tier (i),
    counts of checks and rejections, all 25 contract controls with their
    damaging-mutation labels, claim flags, label and wording;
  * the calculator's domain, exercised on a hash-verified temporary copy;
  * source-edit mutations: the producer closure is copied to a temporary tree
    outside the checkout and edited once per run; every must-abort edit has to
    abort, an unmutated copy has to reproduce the frozen outputs byte for byte,
    and the silent edits (by design) have to be caught by this review's static
    data-flow validator or be the disclosed redundant guard.

Standard library only; exact Fractions decide every Boolean; failures are explicit
exceptions (never assert), so the output bytes match under python -O.

Usage: python3 -B research/round32/skeptic/ax2_postreview_check.py --output /abs/fresh/dir
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
R32 = ROOT / 'research/round32'
CONTRACT_REL = 'research/round32/contracts/ax2.json'
CONTRACT_SHA = 'da72afe377d7601e6b6ec3835ab69d05813cb26c4b46f67485a4d8e0c055992b'
AX1_GATE_REL = 'research/round32/advisor/ax1-gate.json'
AX1_GATE_SHA = '1b8fb152696659439bb01fc7df429fc76fa3132d4936df450d8131256015d177'
AV2_GATE_REL = 'research/round32/advisor/av2-gate.json'
AV2_GATE_SHA = '5b0e3b308ccb2e2b9b8ae2db32ae5e2c2ae978b2dbf46cf83a5882b68a2f4b33'
AX1_CONTRACT_REL = 'research/round32/contracts/ax1.json'
AX1_CONTRACT_SHA = 'bc834eec4f5377041cea9db42a8674cf1f3de0a43b7fef3696a461a011da7d8d'
AX1_FWD_REPORT_REL = 'research/round32/forward/ax1/report.md'
FWD_REL = 'research/round32/forward/ax2'
FWD = ROOT / FWD_REL
FROZEN = {  # forward closure, as frozen and committed (0ae59e6)
    'freeze.json': 'b38f3a758293e194c669ec74f6b3c9dd3dc95a8ec7dc82a35d41f94c7b1e3950',
    'check.py': '73e72c9166ab2931f9cb43be012ece8c5845132a9fec294e079ac7da3acf4dec',
    'calculator.py': 'f368a3e7e73afc52a14422dd253efbc50fa5d7b59c55b3be569f48043f031f5d',
    'report.md': '225fee6aad1f90bdd53bfdf0b9ce2a55027c4b05dbdb7e799f936d2c2b801ae6',
    'output/results.json': 'ba8d36d7900d622df5bc85cca9268bddf1c70d31ca176b23ed79abc1ab6fd3a7',
    'output/source-manifest.json': 'e17de51d9c134342e87e6731b1c63223156a0d6679d06897ade4ef779fa2d7b0',
}
PRE_FREEZE_REL = 'research/round32/skeptic/ax2-independent-freeze.json'
PRE_FREEZE_SHA = 'e06bbcf7e4e002e9ab25d95fc632ab6c7deeb9df65438055665de4d97101d602'
PRE_RESULTS_REL = 'research/round32/skeptic/ax2-independent/results.json'
DEN = 10 ** 60
TAU = F(1, 10 ** 8)
TARGET = F(1, 10 ** 6)
R_OUTWARD = F(1912298807996871790146581299723633, 10 ** 40)   # both codes' 10^-40 ceiling
LABEL = 'uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling (g^4=9.6x10^9)'

DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
R_COVER = ((0, 0, 0), (0, 0, 1))


class ReviewFailure(Exception):
    pass


class Rejected(Exception):
    pass


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise ReviewFailure('check failed: ' + cid)
    if any(c['id'] == cid for c in CHECKS):
        raise ReviewFailure('duplicate check id: ' + cid)
    entry = {'id': cid, 'passed': True}
    entry.update(detail)
    CHECKS.append(entry)


def refuses(fn):
    try:
        fn()
    except Rejected:
        return True
    return False


def q(x):
    return str(F(x))


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def preview(x, digits=12, up=False):
    """Scientific decimal, truncated (or rounded up in magnitude); display only, never decides anything."""
    x = F(x)
    if x == 0:
        return '0'
    sign = '-' if x < 0 else ''
    x = abs(x)
    e = 0
    while x >= F(10) ** (e + 1):
        e += 1
    while x < F(10) ** e:
        e -= 1
    m = x / F(10) ** (e - digits + 1)
    n = m.numerator // m.denominator
    if up and n * m.denominator != m.numerator:
        n += 1
    if n >= 10 ** digits:
        n //= 10
        e += 1
    s = str(n)
    return sign + s[0] + '.' + s[1:] + 'e' + str(e)


def rdown(x, den=DEN):
    x = F(x)
    return F((x.numerator * den) // x.denominator, den)


def rup(x, den=DEN):
    x = F(x)
    return F(-((-x.numerator * den) // x.denominator), den)


# ------------------------------------------------------------ own directed enclosures
def atan_pair(x, n):
    """Last two partial sums of the alternating arctan series (0<x<1): they bracket atan x."""
    s, sums = F(0), []
    for k in range(n):
        s += (-1) ** k * x ** (2 * k + 1) / (2 * k + 1)
        sums.append(s)
    a, b = sums[-2], sums[-1]
    return min(a, b), max(a, b)


def pi_gauss():
    """Gauss: pi = 48 atan(1/18) + 32 atan(1/57) - 20 atan(1/239), outward to 10^-60."""
    a = atan_pair(F(1, 18), 34)
    b = atan_pair(F(1, 57), 24)
    c = atan_pair(F(1, 239), 16)
    lo = 48 * a[0] + 32 * b[0] - 20 * c[1]
    hi = 48 * a[1] + 32 * b[1] - 20 * c[0]
    if not (hi - lo < F(1, 10 ** 70) and F(314159, 100000) < lo < hi < F(314160, 100000)):
        raise ReviewFailure('pi bracket')
    return rdown(lo), rup(hi)


def exp_series(x, n=120):
    """e^x for 0<=x<=4: partial sum and partial sum plus geometric remainder bound."""
    x = F(x)
    s, t = F(0), F(1)
    for k in range(n):
        s += t
        t = t * x / (k + 1)
    return s, s + t / (1 - x / (n + 1))


def quarter_e_minus3():
    lo3, hi3 = exp_series(F(3))
    return rdown(1 / hi3 / 4), rup(1 / lo3 / 4)


def ln_pair(y, n=80):
    """ln y for y>=1 by halving to [1,2) and 2 atanh((m-1)/(m+1)) with geometric tail."""
    y = F(y)
    k = 0
    while y >= 2:
        y /= 2
        k += 1

    def two_atanh(m):
        z = (m - 1) / (m + 1)
        s = sum((z ** (2 * j + 1) / (2 * j + 1) for j in range(n)), F(0))
        return 2 * s, 2 * (s + z ** (2 * n + 1) / ((2 * n + 1) * (1 - z * z)))
    a, b = two_atanh(y), two_atanh(F(2))
    return rdown(a[0] + k * b[0]), rup(a[1] + k * b[1])


def sqrt_pair(x, den=10 ** 40):
    x = F(x)
    k = isqrt((x.numerator * den * den) // x.denominator)
    lo, hi = F(k, den), F(k + 1, den)
    if not (lo * lo <= x <= hi * hi):
        raise ReviewFailure('sqrt bracket')
    return lo, hi


# ------------------------------------------------------------ state tiers (own code)
def tier_ii(abs_tau, pair=True, density=True, self_consistent=True):
    J = 29 * abs_tau
    t1 = F(52, 144) * abs_tau
    T = t1 / (1 - 352 * J) if self_consistent else t1
    eps = 2 * T + (T * T if pair else 0)
    return 2 * eps * (1 + eps) / (1 + eps * eps) if density else 2 * eps


def tier_i(abs_tau):
    t = 29 * abs_tau * F(148, 7)
    eps = 2 * t + t * t
    return 2 * eps * (1 + eps) / (1 + eps * eps)


def radius_parts(D, k_over_tau, pi_lo, abs_tau=TAU, s=F(1)):
    return {'state': 2 * D, 'mean_square': 2 * D * D, 'kernel_dynamics': k_over_tau * abs_tau * 4 * s / pi_lo}


# ------------------------------------------------------------ geometry (own code)
def vadd(p, d):
    return (p[0] + d[0], p[1] + d[1], p[2] + d[2])


def face_links(p, a, c):
    return ((p, a), (vadd(p, DIRS[a]), c), (vadd(p, DIRS[c]), a), (p, c))


def factor_of(site):
    return (site[0] // 4, site[1] // 2, site[2])


def owners(p, a, c):
    return frozenset(factor_of(site) for site, _ in face_links(p, a, c))


def selected(p, a, c):
    return (a, c) == ('x', 'y') and p[1] % 2 == 0 and p[0] % 4 != 3


def anchored(b):
    return [((4 * b[0] + i, 2 * b[1] + j, b[2]), a, c) for i in range(4) for j in range(2) for a, c in ORIENT]


def groups_meeting(box_n=None):
    """Route-B groups whose support meets R: whole stars (21 omitted faces, support b+S) and
    single-factor groups (3 selected faces, support {b}); box_n restricts to Lambda_N."""
    Rset = set(R_COVER)
    stars, singles, rows = [], [], []
    rng = range(-3, 3) if box_n is None else range(-box_n, box_n + 1)
    for b in [(x, y, z) for x in rng for y in rng for z in rng]:
        faces = anchored(b)
        omitted = [f for f in faces if not selected(*f)]
        chosen = [f for f in faces if selected(*f)]
        if len(omitted) != 21 or len(chosen) != 3:
            raise ReviewFailure('anchored face split')
        star_support = {vadd(b, d) for d in S_STAR}
        if any(not owners(*f) <= star_support for f in omitted) or any(owners(*f) != {b} for f in chosen):
            raise ReviewFailure('group support')
        star_inside = box_n is None or all(-box_n <= c <= box_n for v in star_support for c in v)
        if star_inside and star_support & Rset:
            stars.append(b)
            rows += [('star', b, f) for f in omitted]
        if b in Rset:
            singles.append(b)
            rows += [('single', b, f) for f in chosen]
    meeting = [r for r in rows if owners(*r[2]) & Rset]
    inside = [r for r in rows if owners(*r[2]) <= Rset]
    return {'stars': sorted(stars), 'singles': sorted(singles), 'charged': len(rows), 'meeting': len(meeting),
            'selected_meeting': sum(1 for r in meeting if r[0] == 'single'), 'inside': len(inside),
            'per_star': sorted((sum(1 for r in meeting if r[0] == 'star' and r[1] == b) for b in stars), reverse=True)}


# ------------------------------------------------------------ window algebra (own code)
def cmul(u, v):
    return (u[0] * v[0] - u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def cinv(u):
    n = u[0] * u[0] + u[1] * u[1]
    return (u[0] / n, -u[1] / n)


def cadd(*us):
    return (sum((u[0] for u in us), F(0)), sum((u[1] for u in us), F(0)))


def window_checks(s, theta):
    """2 pi ghat from the half-line integrals versus 8s^3/(a^3 b); modulus; antiderivative identities."""
    a, b = (s, -theta), (s, theta)
    ia = cinv(a)
    half_lines = cadd(cinv(b), ia, cmul((2 * s, F(0)), cmul(ia, ia)), cmul((4 * s * s, F(0)), cmul(ia, cmul(ia, ia))))
    a3b = cmul(cmul(a, cmul(a, a)), b)
    closed = cmul((8 * s ** 3, F(0)), cinv(a3b))
    modulus = a3b[0] ** 2 + a3b[1] ** 2 == (s * s + theta * theta) ** 4
    u = s * s + theta * theta
    # d/dtheta [theta/(2s^2 u) + atan(theta/s)/(2s^3)] = u^-2 ;  d/dtheta [-1/(2u)] = theta u^-2
    d_m0 = (s * s - theta * theta) / (2 * s * s * u * u) + 1 / (2 * s * s * u)
    d_m1 = theta / (u * u)
    return half_lines == closed and modulus and d_m0 == 1 / (u * u) and d_m1 == theta / (u * u)


# ------------------------------------------------------------ gate/contract parsing (own regexes)
def parse_gate_D(ax1_gate):
    d = re.search(r"Bind the forward D'_ii = (\d+)/(\d+)", ax1_gate['decision'])
    a = re.search(r"gives the bound value D'_ii=(\d+)/(\d+)", ax1_gate['accepted'])
    rev = re.search(r"R-refinement D'_ii=(\d+)/(\d+)", ax1_gate['accepted'])
    target = re.search(r"meeting (\d+)/10\^(\d+) \(margin", ax1_gate['accepted'])
    if not (d and a and rev and target):
        raise ReviewFailure('AX1 gate text')
    return (F(int(d.group(1)), int(d.group(2))), F(int(a.group(1)), int(a.group(2))),
            F(int(rev.group(1)), int(rev.group(2))), F(int(target.group(1)), 10 ** int(target.group(2))))


def parse_av2(av2_gate):
    a = av2_gate['accepted']
    datum = re.search(r"exact rational datum d=(\d+)/\(4\*10\^40\)", a)
    D0 = re.search(r"forward tier-\(ii\) bound D=(\d+)/(\d+)", a)
    R = re.search(r"r<=R=(\d+)/10\^40", a)
    sst = re.search(r"s\* in \[(\d+\.\d+), (\d+\.\d+)\]", a)
    k = re.search(r"slope k=(\d+)\|tau\|/(\d+)", a)
    if not (datum and D0 and R and sst and k):
        raise ReviewFailure('AV2 gate text')
    return {'datum': F(int(datum.group(1)), 4 * 10 ** 40), 'D0': F(int(D0.group(1)), int(D0.group(2))),
            'R': F(int(R.group(1)), 10 ** 40), 's_star': (F(sst.group(1)), F(sst.group(2))),
            'k_over_tau': F(int(k.group(1)), int(k.group(2)))}


# ------------------------------------------------------------ value validator for exported packets
def validate_exported(res, truth):
    """Refuses a producer packet whose exported rationals differ from the own re-derivation."""
    h = res['headline']
    if F(h['D_prime']) != truth['D']:
        raise Rejected('D prime differs from the AX1 gate tier-(ii) value')
    if F(h['k_prime']) != F(51, 4) * TAU:
        raise Rejected("k' differs from 51|tau|/4")
    terms = {k: F(v['value']) for k, v in res['error_terms_itemized'].items()}
    if set(terms) != {'state', 'mean_square', 'kernel_dynamics', 'arithmetic'}:
        raise Rejected('itemized terms')
    if terms['state'] != 2 * truth['D'] or terms['mean_square'] != 2 * truth['D'] ** 2:
        raise Rejected('state or mean-square term')
    if terms['kernel_dynamics'] != 51 * TAU / truth['pi_lo_prod'] or truth['pi_lo_prod'] > truth['pi'][0]:
        raise Rejected('kernel-dynamics term')
    r = F(h['certified_absolute_error'])
    if r != sum(terms.values(), F(0)) or F(h['certified_absolute_error_outward_1e-40']) != rup(r, 10 ** 40):
        raise Rejected('radius is not the linear sum or its ceiling')
    d = F(h['certified_datum'])
    if d != truth['datum_av2']:
        raise Rejected('datum differs from the AV2 gate datum')
    lo, hi = F(h['interval']['lower']), F(h['interval']['upper'])
    if lo != d - r or hi != d + r or F(h['width']) != 2 * r:
        raise Rejected('interval')
    phi_lo, phi_hi = truth['phi']
    E_true = 2 * (truth['D'] + truth['D'] ** 2) + 51 * TAU / truth['pi'][0]
    if not (lo <= phi_lo - E_true and phi_hi + E_true <= hi):
        raise Rejected('interval does not contain every value allowed by the lemma')
    if (h['target_met'] is not True) or not (r <= TARGET):
        raise Rejected('target Boolean')
    if res['sub_labels'] != ['reference_unresolved'] or not (lo <= phi_lo and phi_hi <= hi):
        raise Rejected('free reference must lie inside (reference_unresolved)')
    if res['label'] != LABEL or any(res[f] is not False for f in FALSE_FLAGS) or res['uniform_wilson_claim'] is not True:
        raise Rejected('label or claim flags')
    if not all(wording_acceptable(hh) for hh in wording_hits(res)):
        raise Rejected('weak-coupling, continuum, K_2 or sign-rider wording outside a negation')
    return True


FALSE_FLAGS = ('continuum_claim', 'weak_coupling_claim', 'resolved_interaction_shift', 'scientific_priority_verified', 'grid_claim',
               'wilson_mean_sign_certified', 'k2_uniform_claimed', 'state_uniqueness_claim', 'independent_review_claimed',
               'mirror_is_second_confirmation')


# ------------------------------------------------------------ static data-flow review of check.py
def dataflow_ok(src):
    """D', tau, s, target and k' must flow from the contract snapshot, never from literals."""
    tree = ast.parse(src)
    if any(isinstance(n, ast.Assert) for n in ast.walk(tree)):
        return False
    fn = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    if 'compute' not in fn or 'contract_values' not in fn:
        return False

    def assigns(func, name):
        out = []
        for n in ast.walk(func):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Name) and t.id == name:
                        out.append(n.value)
                    if isinstance(t, ast.Tuple) and any(isinstance(e, ast.Name) and e.id == name for e in t.elts):
                        out.append(n.value)
        return out

    def is_v(node, key):
        return (isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == 'V'
                and isinstance(node.slice, ast.Constant) and node.slice.value == key)
    comp = fn['compute']
    dp = assigns(comp, 'D_prime')
    if len(dp) != 1 or not is_v(dp[0], 'D_prime'):
        return False
    trio = assigns(comp, 'tau')
    if len(trio) != 1 or not isinstance(trio[0], ast.Tuple) or [is_v(e, k) for e, k in zip(trio[0].elts, ('tau', 's', 'target'))] != [True] * 3:
        return False
    kp = assigns(comp, 'k_prime')
    if len(kp) != 1 or not (isinstance(kp[0], ast.BinOp) and is_v(kp[0].left, 'k_over_tau')
                            and isinstance(kp[0].right, ast.Name) and kp[0].right.id == 'tau'):
        return False
    cv = fn['contract_values']
    ok = False
    for n in ast.walk(cv):
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Subscript):
            t = n.targets[0]
            if isinstance(t.slice, ast.Constant) and t.slice.value == 'D_prime':
                ok = 'dp.group(1)' in ast.unparse(n.value) and 'dp.group(2)' in ast.unparse(n.value)
    dpm = assigns(cv, 'dp')
    return ok and len(dpm) == 1 and "p['D_prime']" in ast.unparse(dpm[0])


# ------------------------------------------------------------ source-mutation replays
def mutated_run(edits=(), input_edits=(), extra_input=None, remove_input=None, rehash=None):
    """Copy the frozen closure outside the checkout, apply one edit set, run check.py once."""
    with tempfile.TemporaryDirectory(prefix='hnm-r32-ax2-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / FWD_REL
        shutil.copytree(FWD, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        texts = {name: (dst / name).read_text() for name in ('check.py', 'calculator.py')}
        for name, old, new in edits:
            if texts[name].count(old) != 1:
                raise ReviewFailure('mutation anchor not unique in %s: %r' % (name, old[:60]))
            texts[name] = texts[name].replace(old, new)
        for rel, old, new, count in input_edits:
            path = dst / 'inputs' / rel
            raw = path.read_bytes()
            if raw.count(old) != count:
                raise ReviewFailure('input mutation anchor count differs: ' + rel)
            raw = raw.replace(old, new)
            path.write_bytes(raw)
            if rehash is not None and rehash[0] == rel:
                if texts['check.py'].count(rehash[1]) != 1:
                    raise ReviewFailure('pinned hash not unique for ' + rel)
                texts['check.py'] = texts['check.py'].replace(rehash[1], sha_bytes(raw))
        for name, text in texts.items():
            (dst / name).write_text(text)
        if extra_input is not None:
            extra = dst / 'inputs' / extra_input
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text('skeptic mutation fixture\n')
        if remove_input is not None:
            (dst / 'inputs' / remove_input).unlink()
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(dst / 'check.py'), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(repo))
        outputs = {p.name: p.read_bytes() for p in out.glob('*.json')} if out.is_dir() else {}
        last = done.stderr.strip().splitlines()[-1] if done.stderr.strip() else ''
        if any(p.name == '__pycache__' or p.suffix == '.pyc' for p in dst.rglob('*')):
            raise ReviewFailure('interpreter cache written into a mutated copy')
        return done.returncode, outputs, last.replace(tmp, '<tmp>'), texts['check.py']


CALC = 'calculator.py'
CHK = 'check.py'
GATE_D = b'2425369125199104794263242601250/167893028420061547330293754713793182097'
GATE_D_EDIT = b'2425369125199104794263242601251/167893028420061547330293754713793182097'
REV_D = '30934916107401289/2530733246376451200000000'
MUST_ABORT = [
    ('calc_single_groups_zero_slope_49', dict(edits=[(CALC, 'SINGLE_GROUPS_MEETING_R, SINGLE_NORM = 2, 1', 'SINGLE_GROUPS_MEETING_R, SINGLE_NORM = 0, 1')])),
    ('calc_pair_term_dropped', dict(edits=[(CALC, '    eps = 2 * T + T * T\n', '    eps = 2 * T\n')])),
    ('calc_density_form_2eps', dict(edits=[(CALC, '    D = 2 * eps * (1 + eps) / (1 + eps * eps)\n', '    D = 2 * eps\n')])),
    ('calc_cap_pin_removed_and_pair_dropped', dict(edits=[
        (CALC, '    eps = 2 * T + T * T\n', '    eps = 2 * T\n'),
        (CALC, "        require(D == AX1_GATE_D_PRIME, 'tier-(ii) formula differs from the AX1 gate rational at the cap')\n", '        pass\n')])),
    ('calc_effect_half_state_term', dict(edits=[(CALC, "costs = {'state': M['M0'] * D,", "costs = {'state': M['M0'] * D / 2,")])),
    ('calc_pi_upper_in_kernel_term', dict(edits=[(CALC, "'kernel_dynamics': k * M['M1_upper']}", "'kernel_dynamics': k * M['M1_lower']}")])),
    ('calc_mean_square_dropped', dict(edits=[(CALC, "'mean_square': M['M0'] * D * D,", "'mean_square': 0 * D,")])),
    ('calc_exponent_24', dict(edits=[(CALC, 'free_lo, free_hi = exp_negative(3 * clock)', 'free_lo, free_hi = exp_negative(24 * clock)')])),
    ('calc_M0_one', dict(edits=[(CALC, "return {'M0': Q(2),", "return {'M0': Q(1),")])),
    ('calc_weak_coupling_label', dict(edits=[(CALC, "fixed spacing and strong bare coupling'\n", "fixed spacing and weak coupling'\n")])),
    ('calc_continuum_flag_true', dict(edits=[(CALC, "'continuum_claim': False, 'weak_coupling_claim': False, 'grid_claim': False,",
                                              "'continuum_claim': True, 'weak_coupling_claim': False, 'grid_claim': False,")])),
    ('calc_cap_widened', dict(edits=[(CALC, "if abs(data['tau']) > CAP:", "if abs(data['tau']) > 10 * CAP:")])),
    ('calc_zero_triple_accepted', dict(edits=[(CALC, 'if value != tau / 24:', 'if value not in (tau / 24, 0):')])),
    ('calc_float_accepted', dict(edits=[(CALC, "    if isinstance(value, bool) or isinstance(value, float):\n",
                                         "    if isinstance(value, float):\n        return Q(value)\n    if isinstance(value, bool):\n")])),
    ('calc_fixed_design_unchecked', dict(edits=[(CALC, "if fixed_design and (abs(data['tau']) != FIXED['abs_tau']", "if False and (abs(data['tau']) != FIXED['abs_tau']")])),
    ('calc_mirror_flag_dropped', dict(edits=[(CALC, "'mirrored_coupling_replay': data['tau'] < 0,", "'mirrored_coupling_replay': False,")])),
    ('calc_arithmetic_term_dropped', dict(edits=[(CALC, 'radius = analytic + arithmetic', 'radius = analytic')])),
    ('calc_conjugation_factor_dropped', dict(edits=[(CALC, 'k = K_PRIME_OVER_TAU * abs_tau', 'k = B_N_OVER_TAU_G_UNITS * abs_tau')])),
    ('calc_uniform_wilson_false', dict(edits=[(CALC, "'uniform_wilson_claim': True, 'uniform_wilson_claim_scope'", "'uniform_wilson_claim': False, 'uniform_wilson_claim_scope'")])),
    ('calc_window_sign_flipped', dict(edits=[(CALC, '    if x >= 0:\n        return Q(1)\n', '    if x <= 0:\n        return Q(1)\n')])),
    ('calc_resolved_shift_claimed', dict(edits=[(CALC, "'resolved_interaction_shift': False,\n", "'resolved_interaction_shift': True,\n")])),
    ('calc_gate_constant_digit', dict(edits=[(CALC, 'Q(2425369125199104794263242601250, ', 'Q(2425369125199104794263242601251, ')])),
    ('check_state_bound_validator_weakened', dict(edits=[(CHK, "require(Dv == G1['D_prime'] == V['D_prime'] == calc.AX1_GATE_D_PRIME, ", "require(Dv <= G1['D_prime'], ")])),
    ('check_label_validator_weakened', dict(edits=[(CHK, "require('weak' not in low and 'continuum' not in low, ", 'require(True, ')])),
    ('check_claim_validator_weakened', dict(edits=[(CHK, "require(fl[name] is False, 'forbidden claim flag set: ' + name)", "require(fl[name] in (False, True), 'forbidden claim flag set: ' + name)")])),
    ('check_single_producer_validator_weakened', dict(edits=[(CHK, "require(pk['producers'] == ['forward'] == V['producers'], ", 'require(True, ')])),
    ('check_group_validator_weakened', dict(edits=[(CHK, "require(n_stars == 7 and n_groups == 2 and n_selected == 6, 'route-B incidence must be 7 stars, 2 single-factor groups, 6 selected faces')\n        require(B_over_tau == Q(7 * n_stars + n_groups, 8) == Q(51, 8), ",
                                                    'require(B_over_tau == Q(7 * n_stars + n_groups, 8), ')])),
    ('check_selected_predicate_changed', dict(edits=[(CHK, "p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)", "p[1] % 2 == 0 and p[0] % 4 in (0, 1)")])),
    ('check_incoming_star_anchors_dropped', dict(edits=[(CHK, "anchors = sorted({vsub(r, d) for r in R for d in S_STAR})", "anchors = sorted(set(R))")])),
    ('check_slope_validator_disabled', dict(edits=[(CHK, "require(len(vals) == 1, 'Duhamel slope depends on the box: extensive norm used')\n        require(vals == {k_prime}, ",
                                                    "require(True, 'Duhamel slope depends on the box: extensive norm used')\n        require(True, ")])),
    ('check_tier_i_as_state_bound', dict(edits=[(CHK, "    D_prime = V['D_prime']\n", '    D_prime = D_i_exact\n')])),
    ('check_decimal_import_added', dict(edits=[(CHK, 'import argparse\n', 'import argparse\nimport decimal\n')])),
    ('contract_byte_edit_without_rehash', dict(input_edits=[(CONTRACT_REL, b'"s": "1"', b'"s": "2"', 1)])),
    ('contract_target_1e-7_rehash', dict(input_edits=[(CONTRACT_REL, b'"1/1000000"', b'"1/10000000"', 2)], rehash=(CONTRACT_REL, CONTRACT_SHA))),
    ('contract_D_prime_reverse_refinement_rehash', dict(input_edits=[(CONTRACT_REL, GATE_D, REV_D.encode(), 1)], rehash=(CONTRACT_REL, CONTRACT_SHA))),
    ('contract_k_prime_49_rehash', dict(input_edits=[(CONTRACT_REL, b'"k_prime": "51|tau|/4"', b'"k_prime": "49|tau|/4"', 1)], rehash=(CONTRACT_REL, CONTRACT_SHA))),
    ('contract_tau_halved_rehash', dict(input_edits=[(CONTRACT_REL, b'"1/100000000"', b'"1/200000000"', 2)], rehash=(CONTRACT_REL, CONTRACT_SHA))),
    ('ax1_gate_byte_edit_without_rehash', dict(input_edits=[(AX1_GATE_REL, GATE_D, GATE_D_EDIT, 2)])),
    ('ax1_gate_D_edit_rehash', dict(input_edits=[(AX1_GATE_REL, GATE_D, GATE_D_EDIT, 2)], rehash=(AX1_GATE_REL, AX1_GATE_SHA))),
    ('av2_gate_byte_edit', dict(input_edits=[(AV2_GATE_REL, b'"verdict": "accepted_within_scope"', b'"verdict": "accepted_within_scope" ', 1)])),
    ('undeclared_skeptic_ax2_input', dict(extra_input='research/round32/skeptic/ax2-independent-derivation.md')),
    ('premise_snapshot_removed', dict(remove_input='research/round29/forward/aq2/report.md')),
]
EXPECTED_REASON = {
    'calc_single_groups_zero_slope_49': 'failed check duhamel_slope_uniform',
    'calc_pair_term_dropped': 'tier-(ii) formula differs from the AX1 gate rational at the cap',
    'calc_density_form_2eps': 'tier-(ii) formula differs from the AX1 gate rational at the cap',
    'calc_cap_pin_removed_and_pair_dropped': 'failed check ax1_gate_state_bound_bound',
    'calc_effect_half_state_term': 'failed check radius_itemized_tau_plus',
    'calc_pi_upper_in_kernel_term': 'failed check radius_itemized_tau_plus',
    'calc_mean_square_dropped': 'failed check radius_itemized_tau_plus',
    'calc_exponent_24': 'failed check radius_itemized_tau_plus',
    'calc_M0_one': 'failed check radius_itemized_tau_plus',
    'calc_weak_coupling_label': 'weak-coupling or continuum wording in label',
    'calc_continuum_flag_true': 'failed check calculator_fixed_design_matches',
    'calc_cap_widened': 'AX1 tier (ii) is admitted only for |tau|<=10^-8',
    'calc_zero_triple_accepted': 'calculator accepted an invalid case: zero_selected_triple_av2_model',
    'calc_float_accepted': 'calculator accepted an invalid case: target_float',
    'calc_fixed_design_unchecked': 'calculator accepted an invalid case: fixed_design_changed_tau',
    'calc_mirror_flag_dropped': 'failed check mirrored_coupling_replay_U_E',
    'calc_arithmetic_term_dropped': 'failed check radius_itemized_tau_plus',
    'calc_conjugation_factor_dropped': 'failed check radius_itemized_tau_plus',
    'calc_uniform_wilson_false': 'failed check calculator_fixed_design_matches',
    'calc_window_sign_flipped': 'window differs from e^{-sx} on the AQ1 support',
    'calc_resolved_shift_claimed': 'failed check free_reference_inside_reference_unresolved',
    'calc_gate_constant_digit': 'tier-(ii) formula differs from the AX1 gate rational at the cap',
    'check_state_bound_validator_weakened': 'damaging mutation accepted: ax1_reverse_R_refinement',
    'check_label_validator_weakened': 'damaging mutation accepted: continuum_in_verdict',
    'check_claim_validator_weakened': 'damaging mutation accepted: flag_continuum_claim',
    'check_single_producer_validator_weakened': 'damaging mutation accepted: reverse_route_claimed',
    'check_group_validator_weakened': 'damaging mutation accepted: selected_groups_forgotten',
    'check_selected_predicate_changed': 'failed check incidence_enumerated_route_b',
    'check_incoming_star_anchors_dropped': 'failed check incidence_enumerated_route_b',
    'check_slope_validator_disabled': 'damaging mutation accepted: extensive_total_norm',
    'check_tier_i_as_state_bound': 'failed check ax1_gate_state_bound_bound',
    'check_decimal_import_added': 'failed check exact_arithmetic_admission',
    'contract_byte_edit_without_rehash': 'contract snapshot bytes differ from the frozen AX2 contract',
    'contract_target_1e-7_rehash': 'failed check target_boolean_1e-6',
    'contract_D_prime_reverse_refinement_rehash': 'failed check ax1_gate_state_bound_bound',
    'contract_k_prime_49_rehash': 'failed check duhamel_slope_uniform',
    'contract_tau_halved_rehash': 'failed check ax1_gate_state_bound_bound',
    'ax1_gate_byte_edit_without_rehash': 'AX1 gate snapshot bytes differ from the admitted gate',
    'ax1_gate_D_edit_rehash': 'failed check ax1_gate_state_bound_bound',
    'av2_gate_byte_edit': 'snapshot not bound by the AX1 gate: research/round32/advisor/av2-gate.json',
    'undeclared_skeptic_ax2_input': 'premise snapshot not bound by a pinned hash or an admitted gate: research/round32/skeptic/ax2-independent-derivation.md',
    'premise_snapshot_removed': 'failed check premise_snapshots_bound',
}
LITERAL_D = "    D_prime = Q(2425369125199104794263242601250, 167893028420061547330293754713793182097)\n"
SILENT = [
    ('check_literal_D_prime_equal_to_gate', dict(edits=[(CHK, "    D_prime = V['D_prime']\n", LITERAL_D)]), 'caught_by_dataflow_review'),
    ('check_box_dependence_test_removed_only', dict(edits=[(CHK, "require(len(vals) == 1, 'Duhamel slope depends on the box: extensive norm used')",
                                                             "require(True, 'Duhamel slope depends on the box: extensive norm used')")]),
     'redundant_guard_disclosed_by_producer'),
]

# Reviewed wording in report.md (bound to its sha256): every line mentioning weak coupling or the
# continuum is a negation, a flag set to false, an exclusion list entry or a rejected mutation.
REPORT_WEAK_CONTINUUM_LINES = {
    79: 'checker rejects weak-coupling or continuum wording',
    300: 'not claimed: no weak-coupling or continuum statement',
    307: 'flag continuum_claim false',
    309: 'flag weak_coupling_claim false',
    356: 'control: weak-coupling label and continuum wording rejected',
    390: 'coherent tampering list: weak-coupling flag set (rejected)',
    396: 'control no_priority_or_continuum_claim (flags set true rejected)',
    414: 'private audit list of aborting edits: a weak-coupling label',
    419: 'private audit list of aborting edits: continuum_claim true',
    439: 'contract claim exclusion (verbatim)',
    447: 'preregistered claim exclusion (verbatim)',
}

# Contract control -> labels that carry its damaging meaning in the producer packet.
CONTROL_MEANING = {
    'missing_incoming_stars': ['orthant_two_anchors', 'box_N1_truncated'],
    'full_original_wilson_cover': ['four_drawn_links'],
    'wrong_delta_alpha_hbar_clock': ['exponent_24_with_s', 'normalized_group_norms_in_G_clock'],
    'vector_versus_scalar_centering': ['scalar_as_vector'],
    'first_order_mean_charged': ['zero_mean_assumed', 'finite_box_first_order_mean_as_uniform_bound'],
    'tau_scaling_exponent': ['sqrt_route_b_bound_relabelled_linear'],
    'changed_model_relabelled': ['relabel_triple_3', 'relabel_k_prime_over_abs_tau_10', 'relabel_route_5'],
    'coherent_evidence_tampering': ['control_boolean_flipped_hash_rebound', 'reverse_refinement_D_hash_rebound', 'seven_star_slope_hash_rebound'],
    'insufficient_verdict_retained': ['at4_uniform_relabelled_met', 'tier_i_relabelled_met', 'tau_retuned_to_poisson_floor_threshold'],
    'exact_arithmetic_admission': ['float_input', 'calculator_float_tau'],
    'root_n_misuse': ['root_sum_of_squares_of_terms', 'root_sum_of_squares_of_nine_group_norms'],
    'no_priority_or_continuum_claim': ['flag_continuum_claim', 'flag_weak_coupling_claim', 'flag_scientific_priority_verified', 'flag_wilson_mean_sign_certified', 'flag_k2_uniform_claimed'],
    'kernel_identity_on_support': ['symmetric_window_misreads_support'],
    'kernel_negative_atom_misread': ['negative_atom_admitted'],
    'kernel_l1_and_first_moment': ['signed_integral_as_l1_norm', 'first_moment_without_s'],
    'window_linear_in_s': ['node_s5_with_s1_radius', 'dynamics_term_dropped'],
    'local_not_extensive_duhamel': ['extensive_total_norm', 'seven_star_only_slope_changed_model', 'conjugation_factor_two_dropped'],
    'uniform_label_strong_coupling': ['weak_coupling_label', 'continuum_in_verdict', 'fixed_spacing_missing', 'strong_bare_coupling_missing'],
    'selected_incidence_count': ['selected_groups_forgotten', 'faces_counted_as_groups'],
    'j0_resolution_declared': ['old_J0_at_the_cap', 'resolution_missing'],
    'av1_tier_bound': ['ax1_reverse_R_refinement', 'ax1_target_4e-7', 'av1_zero_selected_D', 'ax1_tier_i'],
    'state_term_not_effect': ['effect_refinement_D_over_2'],
    'window_fourier_sign_convention': ['theta_to_minus_theta'],
    'tier_mixing_rejected': ['tier_i_mean_square_with_tier_ii_state', 'reverse_state_with_forward_mean_square', 'zero_selected_state_with_uniform_slope'],
    'single_producer_declared': ['reverse_route_claimed', 'replay_requirement_dropped', 'self_review_called_independent', 'mirror_as_second_confirmation'],
}


def load_calculator_copy(tmpdir):
    src = FWD / 'calculator.py'
    if sha(src) != FROZEN['calculator.py']:
        raise ReviewFailure('calculator differs from the frozen closure')
    dst = Path(tmpdir) / 'calculator.py'
    shutil.copyfile(src, dst)
    spec = importlib.util.spec_from_file_location('ax2_forward_calculator_copy', str(dst))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def calc_refuses(calc, kw):
    try:
        calc.certify(**kw)
    except (ValueError, TypeError):
        return True
    return False


def wording_hits(obj, path=''):
    """String leaves or keys mentioning weak coupling, the continuum, a K_2 or a sign rider."""
    pat = re.compile(r'weak|continuum|rider|sign certificate|sign_cert|K_2|k2_', re.I)
    hits = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if pat.search(k):
                hits.append(('key', path + '/' + k, v))
            hits += wording_hits(v, path + '/' + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            hits += wording_hits(v, path + '/' + str(i))
    elif isinstance(obj, str) and pat.search(obj):
        hits.append(('value', path, obj))
    return hits


def wording_acceptable(hit):
    kind, path, value = hit
    if kind == 'key':
        return value is False or (isinstance(value, str) and wording_acceptable(('value', path, value)))
    if re.search(r'/(claim_exclusions|preregistration_claim_exclusions|contract_controls_covered|rejected_mutations|rejected)/\d+$', path):
        return True
    if path.endswith('/id') and value == 'no_priority_or_continuum_claim':
        return True
    low = value.lower()
    return any(m in low for m in ('no uniform', 'no sign certificate', 'no uniform-model k_2', 'no uniform k_2'))


# ------------------------------------------------------------ main computation
def run():
    receipts = []
    # ================= A. integrity and bindings
    contract_raw = (ROOT / CONTRACT_REL).read_bytes()
    con = json.loads(contract_raw)
    need(sha_bytes(contract_raw) == CONTRACT_SHA and con['producers'] == ['forward'] and con['direction'] == 'single+skeptic'
         and con['single_direction_independent_replay'] is True and con['status'] == 'frozen_before_production'
         and con['controls'] == con['preregistration']['controls_required']['ids'] and len(con['controls']) == 25,
         'contract_single_direction_bound', sha256=CONTRACT_SHA, controls=len(con['controls']))
    g1_raw = (ROOT / AX1_GATE_REL).read_bytes()
    g1 = json.loads(g1_raw)
    g2_raw = (ROOT / AV2_GATE_REL).read_bytes()
    g2 = json.loads(g2_raw)
    need(sha_bytes(g1_raw) == AX1_GATE_SHA and g1['verdict'] == 'accepted_within_scope' and sha_bytes(g2_raw) == AV2_GATE_SHA
         and g1['bindings'][AV2_GATE_REL] == AV2_GATE_SHA and g1['bindings'][AX1_CONTRACT_REL] == AX1_CONTRACT_SHA
         and sha(ROOT / AX1_CONTRACT_REL) == AX1_CONTRACT_SHA and g2['verdict'] == 'accepted_within_scope',
         'gates_hash_pinned', ax1_gate_sha256=AX1_GATE_SHA, av2_gate_sha256=AV2_GATE_SHA)
    freeze_raw = (FWD / 'freeze.json').read_bytes()
    frz = json.loads(freeze_raw)
    closure = {p.relative_to(FWD).as_posix() for p in FWD.rglob('*') if p.is_file()}
    listed = {k[len(FWD_REL) + 1:] for k in frz['sources']}
    need(sha_bytes(freeze_raw) == FROZEN['freeze.json'] and closure - {'freeze.json'} == listed
         and all(sha(ROOT / k) == v for k, v in frz['sources'].items())
         and all(sha(FWD / name) == digest for name, digest in FROZEN.items())
         and not any(p.suffix == '.pyc' or p.name == '__pycache__' for p in FWD.rglob('*'))
         and frz['contract_sha256'] == CONTRACT_SHA and frz['loop'] == 'AX2' and frz['direction'] == 'forward',
         'forward_freeze_closure_verified', closure_files=len(closure), freeze_sha256=FROZEN['freeze.json'])
    inputs = sorted(p.relative_to(FWD / 'inputs').as_posix() for p in (FWD / 'inputs').rglob('*') if p.is_file())
    declared = sorted(set(['AGENTS.md', CONTRACT_REL] + con['shared_premises']))
    need(inputs == declared and len(inputs) == 30
         and all((FWD / 'inputs' / rel).read_bytes() == (ROOT / rel).read_bytes() for rel in inputs)
         and not any(rel.startswith('research/round32/skeptic/ax2') or rel.startswith('research/round32/reverse/ax2') for rel in inputs)
         and not (R32 / 'reverse/ax2').exists(),
         'premise_inventory_exact_and_isolated', inputs=len(inputs),
         note='AGENTS.md + contract + 28 shared premises, byte-identical to their sources; no skeptic/ax2* input; no reverse/ax2 package')
    manifest = json.loads((FWD / 'output/source-manifest.json').read_bytes())
    need(all(sha(FWD / k) == v for k, v in manifest['sources'].items())
         and manifest['outputs']['results.json'] == FROZEN['output/results.json'] and manifest['contract_sha256'] == CONTRACT_SHA,
         'source_manifest_consistent', sources=len(manifest['sources']))
    pre_freeze_raw = (ROOT / PRE_FREEZE_REL).read_bytes()
    pre_freeze = json.loads(pre_freeze_raw)
    need(sha_bytes(pre_freeze_raw) == PRE_FREEZE_SHA and all(sha(ROOT / k) == v for k, v in pre_freeze['files'].items())
         and pre_freeze['stage'] == 'pre_comparison' and pre_freeze['contract_sha256'] == CONTRACT_SHA
         and pre_freeze['ax1_gate_sha256'] == AX1_GATE_SHA,
         'pre_comparison_package_unchanged', files=len(pre_freeze['files']))

    res = json.loads((FWD / 'output/results.json').read_bytes())
    pre = json.loads((ROOT / PRE_RESULTS_REL).read_bytes())

    # ================= B. own exact re-derivation
    D = tier_ii(TAU)
    D_minus = tier_ii(abs(-TAU))
    gate_dec, gate_acc, gate_rev, gate_target = parse_gate_D(g1)
    m = re.match(r"^(\d+)/(\d+) \(forward AX1 tier ii", con['parameters']['D_prime'])
    D_contract = F(int(m.group(1)), int(m.group(2)))
    need(D == D_minus == gate_dec == gate_acc == D_contract == F(pre['state_values']['D_prime_bound']),
         'D_prime_equals_ax1_gate_forward_value', D_prime=q(D), preview=preview(D),
         recipe="J'=29|tau|, t1'=52|tau|/144, T'=t1'/(1-352J'), eps=2T'+T'^2, D'=2eps(1+eps)/(1+eps^2); equals the AX1 gate decision and accepted texts (sha pinned) and the contract string")
    av2 = parse_av2(g2)
    alternatives = {
        'ax1_reverse_refinement': gate_rev,
        'ax1_target': gate_target,
        'av1_zero_selected_D': av2['D0'],
        'tier_i': tier_i(TAU),
        'pair_term_dropped': tier_ii(TAU, pair=False),
        'density_form_2eps': tier_ii(TAU, density=False),
        'not_self_consistent': tier_ii(TAU, self_consistent=False),
    }
    need(all(v != D for v in alternatives.values()) and gate_target == F(4, 10 ** 7)
         and alternatives['ax1_reverse_refinement'] == F(pre['state_values']['reverse_refinement_not_used'])
         and alternatives['av1_zero_selected_D'] == F(pre['state_values']['zero_selected_D_not_used'])
         and alternatives['tier_i'] == F(pre['state_values']['tier_i_not_used'])
         and all(tier_ii(F(k, 10 ** 10)) < tier_ii(F(k + 1, 10 ** 10)) for k in (0, 1, 7, 50, 99)),
         'rejected_state_values_identified', values={k: preview(v) for k, v in alternatives.items()},
         note='each alternative differs from the bound D\'; the tier-(ii) formula increases in |tau|, so the gate value bounds every |tau|<=10^-8')
    inc = groups_meeting()
    boxes = {n: groups_meeting(n) for n in (1, 2, 3, 4)}
    k_over_tau = 2 * F(7 * len(inc['stars']) + 1 * len(inc['singles']), 8)
    need(len(inc['stars']) == 7 and inc['singles'] == sorted(R_COVER) and inc['charged'] == 153 and inc['meeting'] == 88
         and inc['selected_meeting'] == 6 and inc['meeting'] - inc['selected_meeting'] == 82 and inc['inside'] == 16
         and inc['per_star'] == [21, 21, 16, 8, 8, 4, 4] and k_over_tau == F(51, 4)
         and all((len(boxes[n]['stars']), len(boxes[n]['singles'])) == (7, 2) for n in (2, 3, 4))
         and (len(boxes[1]['stars']), len(boxes[1]['singles'])) == (4, 2),
         'incidence_seven_stars_two_groups_own_enumeration', k_prime_over_tau='51/4',
         per_star_faces_meeting_R=inc['per_star'], box_counts={str(n): [len(boxes[n]['stars']), len(boxes[n]['singles'])] for n in boxes},
         note="k'=2(7*7|tau|/8+2*|tau|/8)=51|tau|/4, identical for N=2,3,4 (local); N=1 has 4 stars")
    samples = [(F(1), F(0)), (F(1), F(1, 3)), (F(1), F(-5, 2)), (F(1, 2), F(7)), (F(2), F(-1, 9)), (F(7, 3), F(3))]
    need(all(window_checks(s_, th) for s_, th in samples),
         'window_transform_and_moments_own', ghat='4s^3/(pi(s-i theta)^3(s+i theta))', M0='2', M1='4s/pi',
         method='half-line integrals 1/b+1/a+2s/a^2+4s^2/a^3 equal 8s^3/(a^3 b) in Gaussian rationals; |a^3 b|^2=(s^2+theta^2)^4; antiderivative derivatives equal (s^2+theta^2)^-2 and theta(s^2+theta^2)^-2 (limits pi/(2s^3) and 1/(2s^2))')
    pi = pi_gauss()
    phi = quarter_e_minus3()
    pl, ph = F(res['pi_interval']['lower']), F(res['pi_interval']['upper'])
    fr = res['certificate_plus']['free_C_interval']
    f_lo, f_hi = F(fr['lower']), F(fr['upper'])
    need(pl <= pi[0] and pi[1] <= ph and f_lo <= phi[0] and phi[1] <= f_hi and ph - pl <= F(3, 10 ** 39),
         'producer_primitives_contain_own_enclosures', own_pi='Gauss 48atan(1/18)+32atan(1/57)-20atan(1/239), 10^-60',
         own_exp='e^3 power series with geometric remainder, inverted, 10^-60')

    truth = {'D': D, 'pi': pi, 'pi_lo_prod': pl, 'phi': phi, 'datum_av2': av2['datum']}
    need(validate_exported(res, truth) is True
         and F(res['headline']['certified_absolute_error_outward_1e-40']) == R_OUTWARD
         == F(pre['radius']['common_outward_bound_1e-40']),
         'exported_certificate_equals_own_rederivation', radius_outward=q(R_OUTWARD), radius_preview=preview(R_OUTWARD),
         datum=q(av2['datum']))
    h = res['headline']
    r = F(h['certified_absolute_error'])
    E_own_hi = 2 * (D + D * D) + 51 * TAU / pi[0]
    E_own_lo = 2 * (D + D * D) + 51 * TAU / pi[1]
    pre_ci = pre['radius']['common_interval']
    lo_p, hi_p = F(h['interval']['lower']), F(h['interval']['upper'])
    pre_lo, pre_hi = F(pre['radius']['interval']['lower']), F(pre['radius']['interval']['upper'])
    need(E_own_lo <= E_own_hi <= r <= R_OUTWARD and r - E_own_hi < F(1, 10 ** 38)
         and F(pre_ci['datum']) == F(h['certified_datum'])
         and F(pre_ci['lower']) <= lo_p and hi_p <= F(pre_ci['upper'])
         and lo_p <= pre_lo <= pre_hi <= hi_p and lo_p <= phi[0] - E_own_hi and phi[1] + E_own_hi <= hi_p,
         'radius_between_own_bounds_and_pre_comparison_nesting',
         analytic_own=[preview(E_own_lo, 16), preview(E_own_hi, 16)], producer_radius=preview(r, 16),
         note="the producer's exact r lies between the own analytic bound (Gauss pi) and the common ceiling R' (excess over the analytic bound below 10^-38); the pre-comparison common interval d+-R' contains the producer interval d+-r, which contains the pre-comparison 10^-60 interval")
    need(F(h['margin_target_over_radius_lower'].replace('e0', '')) <= TARGET / r
         and h['interval_preview']['lower_down'] == '0.012446575862085186' and h['interval_preview']['upper_up'] == '0.012446958321846786'
         and F(h['interval_preview']['lower_down']) <= lo_p and hi_p <= F(h['interval_preview']['upper_up'])
         and F(h['radius_preview_up'].replace('e-7', '')) / 10 ** 7 >= r,
         'decimals_outward', margin=h['margin_target_over_radius_lower'], interval_preview=[h['interval_preview']['lower_down'], h['interval_preview']['upper_up']],
         radius_preview=h['radius_preview_up'])
    cp, cm = res['certificate_plus'], res['certificate_minus_U_E_mirror_replay']
    need(cp['certified_absolute_error'] == cm['certified_absolute_error'] == h['certified_absolute_error']
         and cp['certified_datum'] == cm['certified_datum'] and cm['mirrored_coupling_replay'] is True
         and cp['mirrored_coupling_replay'] is False and 'not a second confirmation' in cm['mirror_note']
         and res['mirror_is_second_confirmation'] is False and res['tau_values'] == {'+': '1/100000000', '-': '-1/100000000'},
         'mirror_is_replay_not_confirmation', note='tau=-10^-8 is the U_E image (no real g); same |tau| formula, identical datum and radius')
    A = 2 * (D + D * D)
    s_lo_p, s_hi_p = F(res['crossover']['s_star_lower']), F(res['crossover']['s_star_upper'])
    s_true = (pi[0] * (TARGET - A) / (51 * TAU), pi[1] * (TARGET - A) / (51 * TAU))
    s_pre = (F(pre['crossover']['s_star_lower']), F(pre['crossover']['s_star_upper']))
    need(s_lo_p <= s_true[0] <= s_true[1] <= s_hi_p and s_pre[0] <= s_true[0] and s_true[1] <= s_pre[1]
         and A + 51 * TAU * s_lo_p / pl == TARGET and A + 51 * TAU * s_hi_p / ph == TARGET
         and s_hi_p < av2['s_star'][0] and res['crossover']['grid_claim'] is False and res['grid_claim'] is False,
         'crossover_nested', own=[preview(s_true[0], 14), preview(s_true[1], 14)], producer=[preview(s_lo_p, 14), preview(s_hi_p, 14)],
         pre_comparison=[q(s_pre[0]), q(s_pre[1])], av2_s_star_lower=q(av2['s_star'][0]),
         note='crossover of the linear formula only; s=1 is the only certified node')

    # retained failures (own brackets)
    kp = F(51, 4) * TAU
    rf = res['retained_failures']
    L4 = F(10) ** 4
    lg = ln_pair(1 + L4 * L4)
    sq = sqrt_pair(17 * TAU)
    Dl, Dh = 2 * sq[0], 2 * sq[1]
    at_lo = Dl + Dl * Dl + kp * lg[0] / pi[1] + (F(1, 2) + Dl / 2) * 2 / (pi[1] * L4)
    at_hi = Dh + Dh * Dh + kp * lg[1] / pi[0] + (F(1, 2) + Dh / 2) * 2 / (pi[0] * L4)
    a4 = rf['at4_poisson_L10000_uniform_slope']
    lgx = ln_pair(1 / (2 * kp))
    fl_lo = 2 * kp * (1 + lgx[0]) / pi[1]
    fl_hi = 2 * kp * (1 + lgx[1]) / pi[0]
    pf = rf['poisson_floor_uniform_slope_D_to_0']
    Ls = F(3921569)
    lgs = ln_pair(1 + Ls * Ls)
    at_Ls_lo = kp * lgs[0] / pi[1] + 1 / (pi[1] * Ls)
    pw = rf['poisson_floor_uniform_slope_with_D_prime']
    Di = tier_i(TAU)
    Ei_lo = 2 * (Di + Di * Di) + kp * 4 / pi[1]
    ti = rf['window_with_tier_i']
    need(F(a4['radius_lower']) <= at_lo <= at_hi <= F(a4['radius_upper']) and at_lo > TARGET and a4['target_met'] is False
         and F(pf['floor_lower']) <= fl_lo and fl_hi <= F(pf['floor_upper']) and at_Ls_lo <= F(pf['floor_upper'])
         and F(pf['floor_lower']) > TARGET and pf['target_met'] is False
         and F(pw['floor_lower']) == F(pf['floor_lower']) + D + D * D and pw['target_met'] is False
         and F(ti['radius_lower']) <= Ei_lo and F(ti['radius_lower']) > TARGET and ti['target_met'] is False
         and Di == F(pre['state_values']['tier_i_not_used'])
         and F(pre['poisson_retained']['poisson_floor_uniform_D0']['lower']) <= fl_lo
         and F(pre['poisson_retained']['poisson_at4_form_L1e4']['lower']) <= at_hi,
         'retained_failures_own_brackets',
         at4_type_L1e4=[preview(at_lo), preview(at_hi)], poisson_floor_D0=[preview(fl_lo), preview(fl_hi)],
         floor_with_D=preview(F(pw['floor_lower'])), tier_i_window_lower=preview(Ei_lo),
         note='all insufficient at unchanged tau and s; floor: log(1+L^2)>=2log L, minimum at L=1/(2k\'); retained, not retuned')

    at4_text = (ROOT / 'research/round31/forward/at4/report.md').read_text()
    at4_dec = F(re.search(r'Their sum is `mathcal E\^\+≈(0\.\d+)`', at4_text).group(1))
    sq49 = sqrt_pair(F(49, 3) * TAU)
    k49 = F(49, 4) * TAU
    a_lo = 2 * sq49[0] + 4 * sq49[0] ** 2 + k49 * lg[0] / pi[1] + (F(1, 2) + sq49[0]) * 2 / (pi[1] * L4)
    a_hi = 2 * sq49[1] + 4 * sq49[1] ** 2 + k49 * lg[1] / pi[0] + (F(1, 2) + sq49[1]) * 2 / (pi[0] * L4)
    need(a_lo - F(1, 10 ** 15) <= at4_dec <= a_hi + F(1, 10 ** 15) and at_lo > a_hi,
         'at4_formula_reproduced_then_uniform_inputs', at4_frozen=q(at4_dec), own_at4_inputs=[preview(a_lo, 16), preview(a_hi, 16)],
         note='the AT4 F16 formula with AT4 inputs (D=2sqrt(49|tau|/3), k=49|tau|/4, L=10^4) reproduces the frozen AT4 decimal to 10^-15; the uniform inputs give a larger, still insufficient radius')

    def E_of(sv, pdir):
        return 2 * (D + D * D) + 51 * TAU * sv / pdir

    def within(v, text):
        x = F(text.split('e')[0]) * F(10) ** int(text.split('e')[1])
        mant = text.split('e')[0].replace('.', '').lstrip('0')
        ulp = F(10) ** (int(text.split('e')[1]) - (len(mant) - 1))
        return abs(v - x) <= ulp
    report_claims = {
        'E(1/2)=1.1006086e-7': within(E_of(F(1, 2), pi[0]), '1.1006086e-7'),
        'E(2)=3.5356793e-7': within(E_of(F(2), pi[0]), '3.5356793e-7'),
        'E(5)=8.4058205e-7': within(E_of(F(5), pi[0]), '8.4058205e-7'),
        'E(128)>=2.08081e-5': E_of(F(128), pi[1]) >= F(208081, 10 ** 10),
        'state 2.88918384286e-8 (up)': 2 * D <= F(288918384286, 10 ** 19) and within(2 * D, '2.88918384286e-8'),
        'mean_square 4.17369163892e-16 (up)': 2 * D * D <= F(417369163892, 10 ** 27) and within(2 * D * D, '4.17369163892e-16'),
        'kernel 1.62338041954e-7 (up)': 51 * TAU / pi[0] <= F(162338041954, 10 ** 18) and within(51 * TAU / pi[0], '1.62338041954e-7'),
        'margin>=5.22930': TARGET / r >= F(522930, 10 ** 5),
        'excess over AV2 >=8.03e-9': r - av2['R'] >= F(803, 10 ** 11),
        'floor in [1.313477283e-6,1.313477284e-6]': F(1313477283, 10 ** 15) <= fl_lo and fl_hi <= F(1313477284, 10 ** 15),
        'floor with D >=1.3279232e-6': fl_lo + D + D * D >= F(13279232, 10 ** 13),
        'Poisson moment L=10^32 >=46.907878': ln_pair(1 + F(10) ** 64)[0] / pi[1] >= F(46907878, 10 ** 6),
        'AT4-type in [8.5790595e-4,8.5790596e-4]': F(85790595, 10 ** 11) <= at_lo and at_hi <= F(85790596, 10 ** 11),
        'tier-i window >=4.921572155e-5': Ei_lo >= F(4921572155, 10 ** 14),
        's* in [5.9820122841,5.9820122842]': F(59820122841, 10 ** 10) <= s_true[0] and s_true[1] <= F(59820122842, 10 ** 10),
        'contract preview ~1.91e-7 within 1e-9': abs(r - F(191, 10 ** 9)) <= F(1, 10 ** 9),
    }
    need(all(v is True for v in report_claims.values()), 'report_decimals_consistent_with_own_values',
         claims=sorted(report_claims), note='each decimal quoted in report.md is within one unit of its last digit of the own exact value, on the stated side')

    # counts, controls, flags, label, wording
    ctl = con['controls']
    by_id = {c['id']: c for c in res['checks']}
    ctl_rejections = sum(len(by_id[c].get('rejected_mutations', [])) for c in ctl)
    need(len(res['checks']) == 52 == int(res['check_count']) and all(c['passed'] is True for c in res['checks'])
         and all(c in by_id and by_id[c].get('rejected_mutations') for c in ctl) and sorted(res['contract_controls_covered']) == sorted(ctl)
         and ctl_rejections == 98 and len(by_id['calculator_domain_rejections']['rejected_mutations']) == 31
         and int(res['rejected_mutation_count']) == 129
         and all(set(CONTROL_MEANING[c]) <= set(by_id[c]['rejected_mutations']) for c in ctl) and set(CONTROL_MEANING) == set(ctl),
         'all_25_controls_damaging_mutations', control_rejections=ctl_rejections, calculator_domain_rejections=31, total=129,
         note='every contract id has a check with at least one rejected damaging mutation; the labels carrying each control\'s meaning are present')
    need(by_id['local_not_extensive_duhamel']['incident_by_N']['1'] == {'stars': '4', 'single_groups': '2'}
         and all(by_id['local_not_extensive_duhamel']['incident_by_N'][n] == {'stars': '7', 'single_groups': '2'} for n in ('2', '3', '4'))
         and by_id['incidence_enumerated_route_b']['faces_charged'] == '153' and by_id['incidence_enumerated_route_b']['faces_meeting_R'] == '88'
         and sorted(int(v) for v in by_id['incidence_enumerated_route_b']['star_faces_meeting_R'].values()) == sorted(inc['per_star'])
         and res['certificate_plus']['incidence'] == {'B_N_over_abs_tau_G_units': '51/8', 'k_prime_over_abs_tau': '51/4',
                                                       'single_factor_groups_meeting_R': '2', 'stars_meeting_R': '7'},
         'producer_incidence_equals_own', note='7 stars + 2 single-factor groups; box-local')
    flags_false = FALSE_FLAGS
    need(all(res[f] is False for f in flags_false) and res['uniform_wilson_claim'] is True and res['euclidean_node_certified'] is True
         and 'fixed-spacing' in res['uniform_wilson_claim_scope'] and 'no uniform Wilson-mean sign certificate' in res['uniform_wilson_claim_scope']
         and res['producers'] == ['forward'] and res['single_direction_independent_replay_required'] is True
         and res['label'] == LABEL == cp['label'] and res['model']['label'] == LABEL and cp['g4_real_image'] == '9600000000'
         and res['model']['model_id'] == 'AQ_uniform_routeB' and res['model']['route'] == 'B' and res['model']['triple'] == ['tau/24'] * 3
         and res['K_2_note'] == con['parameters']['K_2_note'] and res['claim_exclusions'] == con['claim_exclusions']
         and 'skeptic' in res['proposed_forward_verdict'] and 'independent replay' in res['proposed_forward_verdict'],
         'claim_flags_and_uniform_label', label=LABEL, false_flags=list(flags_false))
    hits = wording_hits(res)
    report = (FWD / 'report.md').read_text()
    lines = report.splitlines()
    wc = {i + 1 for i, ln in enumerate(lines) if re.search(r'weak|continuum', ln, re.I)}
    need(all(wording_acceptable(hh) for hh in hits) and len(hits) > 0
         and sha(FWD / 'report.md') == FROZEN['report.md'] and wc == set(REPORT_WEAK_CONTINUUM_LINES)
         and LABEL in report and 'reference_unresolved' in report,
         'no_weak_coupling_continuum_or_rider_wording', results_hits_reviewed=len(hits),
         report_lines_reviewed={str(k): v for k, v in sorted(REPORT_WEAK_CONTINUUM_LINES.items())},
         note='every mention is a negation, a false flag, an exclusion entry or a rejected mutation; no sign rider or K_2 value is attached')

    # calculator domain on a hash-verified copy
    with tempfile.TemporaryDirectory(prefix='hnm-r32-ax2-skeptic-calc-') as tmp:
        calc = load_calculator_copy(tmp)
        fixed_p = calc.certify(fixed_design=True)
        fixed_m = calc.certify(tau='-1/100000000', fixed_design=True)
        below = [calc.certify(tau=q(t)) for t in (F(1, 10 ** 9), F(1, 3 * 10 ** 8), F(-7, 10 ** 9))]
        zero = calc.certify(tau='0')
        zero_triple_at_zero = calc.certify(tau='0', selected=('0', '0', '0'))
        s_lin = [F(calc.certify(s=q(sv))['analytic_radius']) for sv in (F(1, 2), F(1), F(3, 2), F(2))]
        refusals = {
            'cap_exceeded_positive': {'tau': '1/99999999'}, 'cap_exceeded_negative': {'tau': '-1/99999999'},
            'zero_triple_nonzero_tau': {'selected': ('0', '0', '0')}, 'non_uniform_triple': {'selected': ('tau/24', 'tau/24', '1/2400000001')},
            'positive_triple_at_negative_tau': {'tau': '-1/100000000', 'selected': ('1/2400000000',) * 3},
            'float_tau': {'tau': 1e-8}, 'bool_s': {'s': True}, 'none_tau': {'tau': None}, 'exponent_text': {'tau': '1e-8'},
            's_zero': {'s': '0'}, 's_negative': {'s': '-1/2'}, 'alpha_zero': {'alpha': '0'}, 'target_negative': {'target': '-1'},
            'supplied_D': {'D': '1/100000000'}, 'supplied_k': {'k_prime': '49/400000000'},
            'reverse_tier': {'state_tier': 'ax1_reverse_R_refinement'}, 'av1_tier': {'state_tier': 'av1_forward_tier_ii'},
            'tier_i': {'state_tier': 'ax1_forward_tier_i'}, 'window_c1': {'window': 'C1'}, 'window_poisson': {'window': 'poisson'},
            'model_av2': {'model': 'AQ_patterned_zero_selected'}, 'fixed_design_s2': {'fixed_design': True, 's': '2'},
            'fixed_design_tau_below': {'fixed_design': True, 'tau': '1/1000000000'}, 'fixed_design_text': {'fixed_design': 'True'},
        }
        refused = {name: calc_refuses(calc, kw) for name, kw in refusals.items()}
    need(fixed_p['certified_absolute_error'] == h['certified_absolute_error'] == fixed_m['certified_absolute_error']
         and F(fixed_p['state_bound_D_prime']) == D and fixed_p['state_bound_equals_ax1_gate_value'] is True
         and all(F(b['state_bound_D_prime']) == tier_ii(abs(F(b['parameters']['tau']))) < D and b['state_bound_equals_ax1_gate_value'] is False for b in below)
         and all(v is True for v in refused.values())
         and s_lin[1] - s_lin[0] == s_lin[3] - s_lin[2] and s_lin[2] - s_lin[1] == s_lin[1] - s_lin[0],
         'calculator_domain', refused=sorted(refused), accepted_below_cap=[b['parameters']['tau'] for b in below],
         note="uniform triple only, |tau|<=10^-8 both signs, s>0; D' not an input (pinned to the gate at the cap, the tier-(ii) |tau|-form below it); window C2 only; E'(s) linear in s")
    need(zero['state_bound_D_prime'] == '0' and zero['nonzero_interacting_coupling'] is False and 'limit tau=0' in zero['label']
         and zero['target_met'] is True and zero_triple_at_zero['certified_absolute_error'] == zero['certified_absolute_error']
         and F(zero['certified_absolute_error']) == F(res['error_terms_itemized']['arithmetic']['value']),
         'calculator_tau_zero_branch_recorded',
         note='tau=0 is accepted as the free Casimir limit (D=0, radius = arithmetic half-width; the uniform triple coincides with the zero triple there); mathematically valid, but a corollary, not an AX2 admission (finding N2)')

    # static data-flow review of check.py
    chk_src = (FWD / 'check.py').read_text()
    need(dataflow_ok(chk_src) is True and 'assert ' not in (FWD / 'calculator.py').read_text(),
         'dataflow_contract_to_certificate', note="tau, s, target, D' and k' are assigned once, from the hash-checked contract snapshot; no assert statements")

    # ================= C. source-edit mutations
    rc, outs, last, _ = mutated_run()
    need(rc == 0 and outs.get('results.json') == (FWD / 'output/results.json').read_bytes()
         and outs.get('source-manifest.json') == (FWD / 'output/source-manifest.json').read_bytes(),
         'unmutated_copy_reproduces_frozen_outputs', note='copy outside the checkout; results.json and source-manifest.json byte-identical')
    aborted = 0
    for name, spec in MUST_ABORT:
        rc, outs, last, _ = mutated_run(**spec)
        intended = EXPECTED_REASON[name] in last
        receipts.append({'id': name, 'expected': 'abort', 'aborted': rc != 0 and not outs, 'intended_reason': intended,
                         'last_stderr_line': last})
        if rc != 0 and not outs and intended:
            aborted += 1
    need(aborted == len(MUST_ABORT) and set(EXPECTED_REASON) == {n for n, _ in MUST_ABORT}, 'must_abort_source_edits',
         aborted=aborted, total=len(MUST_ABORT), note='each edit aborts, and at the intended check or validator')
    silent_ok = 0
    for name, spec, handling in SILENT:
        rc, outs, last, src = mutated_run(**spec)
        caught = (dataflow_ok(src) is False) if handling == 'caught_by_dataflow_review' else True
        receipts.append({'id': name, 'expected': 'runs_to_completion', 'completed': rc == 0, 'handling': handling,
                         'caught_by_review_validator': handling == 'caught_by_dataflow_review' and caught})
        if rc == 0 and caught:
            silent_ok += 1
    need(silent_ok == len(SILENT), 'silent_edits_accounted', total=len(SILENT),
         note='a literal D\' equal to the gate value runs to completion (only the check.py sha changes) and is rejected by the data-flow review; removing only the box-dependence test is the disclosed redundant guard (the slope-value test still rejects the extensive norm)')

    # ================= D. damaging-mutation controls of this review's own validator
    bad = []
    for key, mutate in (
            ('D_reverse', lambda p: p['headline'].__setitem__('D_prime', q(gate_rev))),
            ('k_seven_star', lambda p: p['headline'].__setitem__('k_prime', q(F(49, 4) * TAU))),
            ('state_half', lambda p: p['error_terms_itemized']['state'].__setitem__('value', q(D))),
            ('radius_halved', lambda p: p['headline'].__setitem__('certified_absolute_error', q(r / 2))),
            ('datum_shifted', lambda p: p['headline'].__setitem__('certified_datum', q(av2['datum'] + F(1, 10 ** 20)))),
            ('reference_resolved', lambda p: p.__setitem__('sub_labels', ['resolved'])),
            ('weak_coupling_label', lambda p: p.__setitem__('label', LABEL.replace('strong bare coupling', 'weak coupling'))),
            ('continuum_verdict', lambda p: p.__setitem__('proposed_forward_verdict', p['proposed_forward_verdict'] + ' toward the continuum limit')),
            ('continuum_flag', lambda p: p.__setitem__('continuum_claim', True)),
            ('sign_rider_attached', lambda p: p.__setitem__('wilson_mean_sign_certified', True)),
            ('K2_rider_attached', lambda p: p.__setitem__('uniform_K2_rider', '3354.80322946'))):
        pk = json.loads(json.dumps(res))
        mutate(pk)
        bad.append(refuses(lambda pk=pk: validate_exported(pk, truth)))
    need(all(bad) and len(bad) == 11, 'own_validator_rejects_damaged_packets', rejected=11,
         note='D reverse, seven-star slope, D/2, halved radius, shifted datum, resolved reference, weak-coupling label, continuum verdict, continuum flag, sign rider, K_2 rider')

    exact = {
        'D_prime': q(D), 'k_prime': q(kp), 'radius_exact': q(r), 'radius_outward_1e-40': q(R_OUTWARD),
        'datum': q(av2['datum']), 'interval': [q(lo_p), q(hi_p)], 'own_pi': [q(pi[0]), q(pi[1])],
        'own_quarter_e_minus3': [q(phi[0]), q(phi[1])], 'own_analytic_radius': [q(E_own_lo), q(E_own_hi)],
        's_star_own': [q(s_true[0]), q(s_true[1])], 'terms': {k: v['value'] for k, v in res['error_terms_itemized'].items()},
    }
    previews = {
        'D_prime': preview(D, 12, True), 'radius': preview(R_OUTWARD, 12, True), 'interval': [preview(lo_p, 17), preview(hi_p, 17, True)],
        's_star': preview(s_true[0], 12), 'margin': preview(TARGET / r, 6), 'at4_type_L1e4': preview(at_lo, 8),
        'poisson_floor_D0': preview(fl_lo, 10), 'tier_i_window': preview(Ei_lo, 10),
        'note': 'decimal previews only; every Boolean above was decided on exact rationals',
    }
    return {
        'schema': 'hnm-r32-skeptic-postcomparison-v1', 'loop': 'AX2', 'stage': 'post_comparison',
        'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'model-agent skeptic with correlated ancestry; not human peer review or formal verification',
        'admission_basis': 'single forward producer plus the skeptic pre-comparison independent replay',
        'contract_sha256': CONTRACT_SHA, 'ax1_gate_sha256': AX1_GATE_SHA, 'av2_gate_sha256': AV2_GATE_SHA,
        'exact': exact, 'previews': previews, 'mutation_receipts': receipts,
        'passed': True, 'checks': CHECKS, 'checks_count': len(CHECKS),
    }


def main():
    ap = argparse.ArgumentParser(description='AX2 post-comparison skeptic checks')
    ap.add_argument('--output', required=True)
    a = ap.parse_args()
    out = Path(a.output)
    if not out.is_absolute() or out.exists():
        raise SystemExit('--output must be an absolute fresh directory')
    out = out.resolve()
    if out == ROOT or ROOT in out.parents:
        raise SystemExit('--output must lie outside the checkout')
    result = run()
    out.mkdir(parents=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AX2', 'stage': 'post_comparison', 'checks': result['checks_count'],
                      'radius': result['previews']['radius'], 'mutations': len(result['mutation_receipts'])}, sort_keys=True))


if __name__ == '__main__':
    main()
