#!/usr/bin/env python3
"""BD1 post-comparison skeptic checks (paired loop: forward characters route, reverse weyl_integration route).

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated ancestry (same model family as the advisor,
the lenses and both producers; the frozen BD1 texts carry the pre-freeze review's edits); not human peer review or formal
verification.

Commit order as it happened (UTC, git): BD1 reverse a1010a4 05:53:54; BD1 forward 5a792b0 05:54:17; BD2 forward 37fa623
06:00:06; the skeptic's pre-comparison packages bf1f531 06:10:08. The pre-comparison values were final before any producer
text was read (the only exposure was the names and hashes of the producers' inputs/ files); the producers committed first.

Adds to the frozen pre-comparison package (bd1_check.py):
  * integrity: the contract hash; the unchanged pre-comparison package and a byte replay of bd1_check.py; both producer
    freeze closures file by file (27 files each); both input inventories on the real snapshots (23 files, equal to the
    contract-derived list and to the names-only inventory recorded before production, byte-identical to the repository);
    replays of both producers reproducing output/ byte for byte (normal, or -O when this program runs under -O); the frozen
    artifacts pinned; no interpreter cache in either closure;
  * every producer value against an independent recomputation (never from a producer value): moments by three own routes
    (characters, Weyl constant terms on the SU(N) torus, Frobenius/hook and closed-form counts), mixed cubic moments, the
    one-plaquette Rayleigh-Schroedinger series to order 5, first-order coefficients and derivatives, the SU(3), SO(3) and
    SU(5) obstruction cells, the centre data, the box sums over the 1344 retained faces of Lambda_2, the Kato radii, the
    flip-set counts on boxes, factors and tori, an own GF(2) solver for flip-set existence on tori, the BB2 constants and the
    region bounds of the SU(2) corollary, the transfer ledgers, the gate fields and the report previews;
  * exact cross-route agreement forward = reverse = the three own routes on every shared cell;
  * the tier/route labels of every exported value against the frozen control (reading R1) and the flip scope (reading R2);
  * text: the round phrase tool (subprocess) on both reports, the template once as one line, every clause mentioning
    uniqueness classified;
  * damaged producer packets rejected by this review's validators;
  * source-edit runs on temporary copies outside the checkout: one validator weakening per contract control and producer
    (44), must-abort substitutions (the U(N) torus, other normalizations, route perturbations, inputs, report), silent edits
    (harmless, and damaging ones caught only by this review's validators), unmutated copies and runs without -B.

Standard library only; exact Fractions decide every Boolean; failures are explicit exceptions (never assert), so the output
bytes match under python -O.

Usage: python3 -B research/round33/skeptic/bd1_postreview_check.py --output /abs/fresh/dir
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F
from itertools import product
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import bd1_check as pre  # noqa: E402  (the skeptic's own frozen pre-comparison module)

ROOT = HERE.parents[2]
R33 = ROOT / 'research/round33'
CONTRACT = R33 / 'contracts/bd1.json'
CONTRACT_SHA = 'a5c8416600c49b0728fdca05cd67c3ff2e53d9fd9e146d4305abcd2da775c1fc'
DIRS = {'forward': R33 / 'forward/bd1', 'reverse': R33 / 'reverse/bd1'}
RELS = {'forward': 'research/round33/forward/bd1', 'reverse': 'research/round33/reverse/bd1'}
PRE_SCRIPT = HERE / 'bd1_check.py'
PRE_RESULTS = HERE / 'bd1-independent/results.json'
PRE_FREEZE = HERE / 'bd1-independent-freeze.json'
PHRASE_TOOL = R33 / 'tools/phrase_scan.py'
PHRASE_TOOL_SHA = '1c31a4958c4a44144c5d4f256db551385d216b86309eadc54a608c5e2a4ff0e2'
FROZEN = {  # frozen producer artifacts (sha256 at review time; commits 5a792b0 forward and a1010a4 reverse)
    'forward': {
        'check.py': '84030930cb1b34db3089c9d95151f744fa190bb463ef66520c50c9aa5ed94c07',
        'report.md': 'd16d36328f12b070082bc825a542d11886149c217ca7595d093919eb875c2a8b',
        'freeze.json': 'c2c0978b017b3012dade5a82509b82629b2902756cd29183dacdc4d30a716733',
        'output/results.json': 'adfa24fb448679f759781162caf4166af6574f51801cd45ac696c700ef9be4c3',
        'output/source-manifest.json': '82a9c31c256cfb6c84dfbb95ce6aa78efde30bda9f66c1f631d6b14355c5aeb0',
    },
    'reverse': {
        'check.py': '0175b5f8d549fbed2d4b1c40dff977497a5c44f207569b5384d412123e5e296f',
        'report.md': '399d296d2baaabe56f5b5fa9c598bde750848cc657c0bd6423db7c870b5a61d1',
        'freeze.json': 'd8a612a93644c7238e8150387fae030adfce605c3ba49c8a7aec4283a9749d4c',
        'output/results.json': '8052d2e910ce491505ce93e3b1b3a4121e6fb9a66d6410060e30d035c7eb7629',
        'output/source-manifest.json': '4634dd589e5761eed4b37ae74f4801c6ab81706e8d99d9bcc96f5aa30cd67d69',
    },
}
BB2_GATE = 'research/round33/advisor/bb2-gate.json'
GROUPS = list(pre.GROUPS)
FLIP = ['SU(2)', 'SU(4)', 'U(1)', 'Z2']
PARITY = ['SU(2)', 'SU(4)', 'SU(5)', 'U(1)', 'Z2']
OBSTRUCTIONS = {'flip': ['SU(3)', 'SU(5)', 'SO(3)'], 'parity': ['SU(3)', 'SO(3)']}
PLAN_ROUTES = ['weighted_norm', 'analytic_disc', 'polymer_kp', 'iterated_split', 'duhamel_inner_f1', 'duhamel_inner_f2']
TIER = 'exact_first_order'
RECOMMENDED_SCOPE = ('SU(2), SU(4), U(1) and Z2 (central elements -I, -I, e^{i pi} and the nontrivial element, each acting as '
                     '-1 on the Wilson representation), on their one-plaquette models H_FG(G) and group-G whole-star box '
                     'models H^G_N (the operator identity in every box and cutoff; oddness of omega(W) in each box inside its '
                     'Kato radius), with the flip sets E_3 and E_2 verified; no AM2, AV1 or AQ statement for any group other '
                     'than SU(2)')
TORI = [(3, 3), (3, 4), (4, 3), (4, 4), (5, 5), (3, 5), (3, 3, 3), (3, 3, 4), (3, 4, 4), (4, 3, 4), (4, 4, 3), (4, 4, 4), (3, 4, 3)]
FACTORS = [(0, 0, 0), (0, 0, 1), (0, 1, 0), (1, 0, 0), (-1, 0, 0), (0, -1, 0), (1, 1, 1), (-1, -1, -1), (2, -3, 5),
           (-2, 1, -2), (2, -3, 1)]
W_FACE = ((0, 0, 0), 'x', 'z')  # the AW1 original xz face
KNOWN_REPORT_PREVIEW_DEFECTS = [('reverse', '1/63403380965376', '1.57720727258e-14')]


class ReviewFailure(RuntimeError):
    """A post-review check failed."""


class Rejected(Exception):
    """The skeptic's value and report validator refused a producer packet."""


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise ReviewFailure(cid)
    if any(row['id'] == cid for row in CHECKS):
        raise ReviewFailure('duplicate check id ' + cid)
    row = {'id': cid, 'passed': True}
    row.update(detail)
    CHECKS.append(row)


def expect(ok, reason):
    if ok is not True:
        raise Rejected(reason)


def q_(x):
    return str(F(x))


def preview(x, digits=12):
    return format(float(x), '.%de' % digits)


def trunc(x, digits=12):
    """Truncated scientific preview with the given number of significant digits (the producers' convention)."""
    x = F(x)
    if x == 0:
        return '0'
    sign, x = ('-' if x < 0 else ''), abs(x)
    e = 0
    while x >= F(10) ** (e + 1):
        e += 1
    while x < F(10) ** e:
        e -= 1
    m = str((x / F(10) ** (e - digits + 1)).__floor__())
    return sign + m[0] + '.' + m[1:] + 'e' + str(e)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rat(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise Rejected('non-exact value in producer results: ' + repr(value))
    if isinstance(value, int):
        return F(value)
    if isinstance(value, str) and re.fullmatch(r'-?\d+(/\d+)?', value):
        return F(value)
    raise Rejected('malformed exact value: ' + repr(value))


def dec(s):
    m = re.fullmatch(r'(-?\d+)(?:\.(\d+))?(?:e([+-]?\d+))?', s)
    if m is None:
        raise Rejected('malformed decimal: ' + repr(s))
    frac = m.group(2) or ''
    return F(int(m.group(1) + frac), 10 ** len(frac)) * F(10) ** int(m.group(3) or 0)


def ulp(s):
    m = re.fullmatch(r'-?\d+(?:\.(\d+))?(?:e([+-]?\d+))?', s)
    return F(10) ** (int(m.group(2) or 0) - len(m.group(1) or ''))


def is_truncation(s, x):
    x = F(x)
    if x == 0:
        return s == '0'
    d = dec(s)
    return d <= x < d + ulp(s) if x > 0 else d - ulp(s) < x <= d


def within_ulp(s, x):
    return abs(dec(s) - F(x)) < ulp(s)


def check_by_id(res, cid):
    for c in res['checks']:
        if c['id'] == cid:
            return c
    raise Rejected('producer check missing: ' + cid)


def groups_named(text):
    """Which of the seven listed groups a scope text names (whole-token match), before its '; no AM2' exclusion clause."""
    text = text.split('; no AM2')[0]
    return [g for g in GROUPS if re.search(r'(?<![\w(])' + re.escape(g) + r'(?![\w)])', text)]


# ------------------------------------------------------------ the skeptic's own values (nothing from the producers)
def torus_geometry(sides):
    dim = len(sides)
    idx = {}
    for p in product(*[range(L) for L in sides]):
        for d in range(dim):
            idx[(p, d)] = len(idx)
    faces = []
    for p in product(*[range(L) for L in sides]):
        for a in range(dim):
            for c in range(a + 1, dim):
                pa = tuple((p[i] + (1 if i == a else 0)) % sides[i] for i in range(dim))
                pc = tuple((p[i] + (1 if i == c else 0)) % sides[i] for i in range(dim))
                faces.append(((p, a), (pa, c), (pc, a), (p, c)))
    return idx, faces


def e3_int(link):
    p, d = link
    return p[(1, 2, 0)[d]] % 2 == 0  # x-links keyed to p_y, y-links to p_z, z-links to p_x


def e2_int(link):
    p, d = link
    return d == 0 and p[1] % 2 == 0


def gf2_solvable(sides):
    """Own GF(2) elimination: is there a link set meeting every plaquette of the torus an odd number of times?"""
    idx, faces = torus_geometry(sides)
    pivots = {}
    for f in faces:
        mask, rhs = 0, 1
        for l in f:
            mask ^= 1 << idx[l]
        while mask:
            b = mask.bit_length() - 1
            if b not in pivots:
                pivots[b] = (mask, rhs)
                break
            mask ^= pivots[b][0]
            rhs ^= pivots[b][1]
        if mask == 0 and rhs == 1:
            return False
    return True


def reference():
    ref = {'g': {}}
    trap = {g: pre.moments_weyl(g, 6, unitary_torus=True) for g in ('SU(3)', 'SU(4)', 'SU(5)')}
    for g in GROUPS:
        grp = pre.group(g)
        mA, mB, mC = pre.moments_characters(grp, 6), pre.moments_weyl(g, 6), pre.moments_third(g, 6)
        if not (mA == mB == mC):
            raise ReviewFailure('own moment routes disagree for ' + g)
        a8, a9 = pre.one_plaquette_rs(grp, 5, 8), pre.one_plaquette_rs(grp, 5, 9)
        if a8[:3] != a9[:3]:
            raise ReviewFailure('own one-plaquette series not stable in the basis depth for ' + g)
        omW, omW2, E, _ = a8
        omC2 = [F(0)] + [(E[m] + omW[m - 1] / 3) / 32 for m in range(1, 6)]
        CF = grp.CF
        a = F(1, 3) / (32 * CF)
        E3 = mA[2]
        if g.startswith('SU('):
            n = int(g[3:-1])
            mixed = {(x, y): pre.mixed_moment_frobenius(n, x, y) for x in range(6) for y in range(6 - x)}
        elif g == 'U(1)':
            mixed = {(x, y): int(x == y) for x in range(6) for y in range(6 - x)}
        elif g == 'Z2':
            mixed = {(x, y): int((x + y) % 2 == 0) for x in range(6) for y in range(6 - x)}
        else:  # SO(3): real vector character, E[chi^k] = 3^k E[W^k]
            mixed = {(x, y): (1 if x + y == 0 else int(3 ** (x + y) * mA[x + y - 1])) for x in range(6) for y in range(6 - x)}
        ref['g'][g] = {
            'CF': CF, 'mom': mA, 'omW': omW, 'omW2': omW2, 'E': E[:6], 'omC2': omC2, 'E3': E3,
            'c1': 2 * F(1, 3) * mA[1] / (32 * CF), 'dW2': omW2[1], 'duhamel': E3 / 3, 'a': a,
            'central': pre.group(g).centre()['minus_one_element'] is not None,
            'kato_fg': 48 * CF, 'mixed': mixed,
        }
        R = ref['g'][g]
        if not (R['c1'] == omW[1] and R['dW2'] == 2 * a * E3 and omW[2] == 3 * a * a * E3 and omW[0] == mA[0]
                and omW2[0] == mA[1]):
            raise ReviewFailure('own closed forms differ from the own series for ' + g)
    if ref['g']['SU(5)']['omW'][4] != F(1, 2 ** 30 * 3 ** 10):
        raise ReviewFailure('own SU(5) fourth order')
    ref['trap'] = trap
    ref['flip'] = [g for g in GROUPS if ref['g'][g]['central']]
    ref['parity'] = [g for g in GROUPS if ref['g'][g]['E3'] == 0]
    # boxes, retained faces and the N=2 box sums ---------------------------------------------------------------------------
    boxes = {}
    for n in (2, 3, 4):
        plaqs, retained = pre.box_data(n)
        cnt = [sum(1 for l in pre.face_links(*f) if pre.in_E3(l)) for f in plaqs]
        rcnt = [sum(1 for l in pre.face_links(*f) if pre.in_E3(l)) for f in retained]
        boxes[n] = {'anchors': (2 * n) ** 3, 'links': 24 * (2 * n + 1) ** 3, 'plaquettes': len(plaqs), 'once': cnt.count(1),
                    'three': cnt.count(3), 'even': sum(1 for k in cnt if k % 2 == 0), 'retained': len(retained),
                    'retained_once': rcnt.count(1), 'retained_three': rcnt.count(3)}
        if n == 2:
            ret2 = retained
    wl = set(pre.face_links(*W_FACE))
    shared = [len(wl & set(pre.face_links(*f))) for f in ret2 if f != W_FACE]
    ref['box_sums'] = {'W_retained': W_FACE in ret2, 'faces': len(ret2), 'max_shared_links': max(shared),
                       'sharing_one_link': shared.count(1)}
    for g in GROUPS:
        R = ref['g'][g]
        # single occurrence: a retained face f != W shares at most one link with W, so E[W W_f] = E[W^2 W_f] = 0
        R['box'] = {'mean_sum': R['mom'][1], 'state_sum': R['E3'], 'duhamel_sum': R['E3'], 'energy_sum': F(0),
                    'c1_box': 2 * F(1, 3) * R['mom'][1] / (32 * R['CF']), 'dW2_box': 2 * R['a'] * R['E3'],
                    'kato_box': {n: 12 * R['CF'] / boxes[n]['retained'] for n in (2, 3, 4)}}
    ref['boxes'] = boxes
    # factors -------------------------------------------------------------------------------------------------------------
    factors = {}
    for b in FACTORS:
        links = [((4 * b[0] + r, 2 * b[1] + s, b[2]), d) for r in range(4) for s in range(2) for d in 'xyz']
        lset = set(links)
        faces = set()
        for (p, d) in links:
            for a_, c_ in pre.ORIENT:
                if d not in (a_, c_):
                    continue
                other = c_ if d == a_ else a_
                for base in (p, pre.add(p, tuple(-x for x in pre.DIRS[other]))):
                    if (p, d) in pre.face_links(base, a_, c_):
                        faces.add((base, a_, c_))
        hist = {}
        for f in faces:
            k = sum(1 for l in pre.face_links(*f) if pre.in_E3(l))
            hist[k] = hist.get(k, 0) + 1
        sel = sum(1 for f in faces if pre.is_selected(*f))
        factors[b] = {'E3_links': sum(1 for l in links if pre.in_E3(l)), 'faces': len(faces), 'selected': sel,
                      'omitted': len(faces) - sel, 'hist': {str(k): v for k, v in sorted(hist.items())}, 'z_parity': b[2] % 2}
    ref['factors'] = factors
    # tori ------------------------------------------------------------------------------------------------------------------
    tori = {}
    for sides in TORI:
        _, faces = torus_geometry(sides)
        rule = e3_int if len(sides) == 3 else e2_int
        tori[sides] = {'plaquettes': len(faces), 'even': sum(1 for f in faces if sum(1 for l in f if rule(l)) % 2 == 0),
                       'gf2': gf2_solvable(sides)}
        odd = sum(1 for L in sides if L % 2)
        if tori[sides]['gf2'] != (odd <= 1):  # every coordinate plane has an even plaquette count
            raise ReviewFailure('GF(2) existence differs from the plane-parity rule at %r' % (sides,))
    ref['tori'] = tori
    # BB2 constants and the W-face region -----------------------------------------------------------------------------
    if sha(ROOT / BB2_GATE) != pre.GATES[BB2_GATE]:
        raise ReviewFailure('BB2 gate hash')
    acc = json.loads((ROOT / BB2_GATE).read_text())['accepted']
    m = re.search(r"<= c'_site \|Y\| e\^\{\|Y\|/10\^8\} q\^\{d_Y\} with d_Y=N-max_\{y in Y\}\|y\|_inf and c'_site=(\d+)/(\d+) ", acc)
    mq = re.search(r'the R form C q\^\(N-1\) with q=1/(\d+) ', acc)
    if m is None or mq is None or 'both signs |tau|<=10^-8' not in acc:
        raise ReviewFailure('BB2 region form not parsed')
    ref['bb2'] = {'csite': F(int(m.group(1)), int(m.group(2))), 'q': F(1, int(mq.group(1)))}
    Y = sorted({pre.pi_map(p) for p, _ in pre.face_links(*W_FACE)})
    ref['w_region'] = {'Y': len(Y), 'm': max(max(abs(x) for x in y) for y in Y)}
    return ref


def bb2_bound(ref, Ysize, m, N):
    return ref['bb2']['csite'] * Ysize / (1 - F(Ysize, 10 ** 8)) * ref['bb2']['q'] ** (N - m)


# ------------------------------------------------------------ report previews
PREVIEW_PATTERNS = {
    'forward': [
        (r'\| \*\*(\d+/\d+)\*\* \| ([0-9.]+e-?\d+) \|', 7),
        (r'`E\[W\^3\] = (1/\d+)` \(≈ ([0-9.]+e-?\d+)\)', 2),
        (r'= 2a E\[W\^3\] = (1/\d+)` \(≈ ([0-9.]+e-?\d+)\)|`d omega\(W\^2\)/d tau = (1/\d+)` \(≈ ([0-9.]+e-?\d+)\)', 2),
        (r'\*\*(1/\d+)\*\* \(≈ ([0-9.]+e-?\d+)\), nonzero', 2),
        (r'\*\*(1/\d+) = 1/\(2\^30 3\^10\)\*\* \(≈ ([0-9.]+e-?\d+)\)', 1),
    ],
    'reverse': [
        (r'\| (\d+/\d+) \| ([0-9.]+e-?\d+) \|', 7),
        (r'= (1/\d+)`, preview `([0-9.]+e-?\d+)`', 4),
        (r'`omega_4 = (1/\d+) = 1/\(2\^30 3\^10\)`, preview `([0-9.]+e-?\d+)`', 1),
    ],
}
FORWARD_NAMED_PREVIEWS = [('SU(3)', 3, 'SU\\(3\\) `E\\[W\\^3\\] ≈ ([0-9.]+e-?\\d+)`'), ('SU(4)', 4, 'SU\\(4\\) `E\\[W\\^4\\] ≈ ([0-9.]+e-?\\d+)`'),
                          ('SU(5)', 4, 'SU\\(5\\) `E\\[W\\^4\\] = ([0-9.]+e-?\\d+)`'), ('SU(5)', 5, '`E\\[W\\^5\\] = ([0-9.]+e-?\\d+)`'),
                          ('SO(3)', 3, 'SO\\(3\\) `E\\[W\\^3\\] ≈ ([0-9.]+e-?\\d+)`')]


def report_previews(side, report, ref):
    """Every (exact, preview) pair the report prints next to each other; returns (rows, mismatches)."""
    known = {q_(ref['g'][g][k]) for g in GROUPS for k in ('c1', 'dW2')} | {q_(ref['g'][g]['omW'][2]) for g in GROUPS} \
        | {q_(ref['g'][g]['E3']) for g in GROUPS} | {q_(ref['g']['SU(5)']['omW'][4])}
    rows, bad = [], []
    for pat, count in PREVIEW_PATTERNS[side]:
        found = []
        for m in re.finditer(pat, report):
            groups = [x for x in m.groups() if x is not None]
            found.append((groups[0], groups[1]))
        if len(found) != count:
            raise Rejected('%s report: preview pattern count %d != %d (%s)' % (side, len(found), count, pat[:40]))
        for ex, pv in found:
            if ex not in known:
                raise Rejected('%s report: printed exact value not recomputed: %s' % (side, ex))
            ok = within_ulp(pv, F(ex))
            rows.append({'exact': ex, 'preview': pv, 'within_last_digit': ok})
            if not ok:
                bad.append((side, ex, pv))
    if side == 'forward':
        for g, k, pat in FORWARD_NAMED_PREVIEWS:
            m = re.search(pat, report)
            if m is None:
                raise Rejected('forward report: moment preview missing for %s E[W^%d]' % (g, k))
            ok = within_ulp(m.group(1), ref['g'][g]['mom'][k - 1])
            rows.append({'exact': q_(ref['g'][g]['mom'][k - 1]), 'preview': m.group(1), 'within_last_digit': ok})
            if not ok:
                bad.append((side, q_(ref['g'][g]['mom'][k - 1]), m.group(1)))
    return rows, bad


# ------------------------------------------------------------ validators (Rejected on any disagreement)
def labelled(entry, value, tiered, route, where):
    expect(isinstance(entry, dict) and isinstance(entry.get('value'), str), 'non-exact or missing entry: ' + where)
    expect(rat(entry['value']) == value, 'value differs: ' + where)
    expect(entry.get('route_of_computation') == route, 'route label: ' + where)
    if tiered:
        expect(entry.get('tier') == TIER, 'first-order value without exact_first_order: ' + where)
    else:
        expect('tier' not in entry, 'tier on a moment or a higher-order coefficient: ' + where)
    expect('hypothesis_source' not in entry and not any(isinstance(x, str) and x in PLAN_ROUTES for x in entry.values()),
           'plan route label or hypothesis source: ' + where)


def common_text(res, report, con, side):
    tpl = con['preregistration']['mandatory_sentence_template']
    expect(res.get('mandatory_sentence') == tpl, side + ' template in the results')
    expect(res.get('sub_labels') == ['transfer_to_named_model', 'obstruction_recorded'], side + ' sub-labels')
    expect(report.count(tpl) == 1 and sum(1 for ln in report.splitlines() if tpl in ln) == 1, side + ' mandatory template')
    ids = {c['id']: c for c in res['checks']}
    expect(all(c.get('passed') is True for c in res['checks']), side + ' check not passed')
    expect(all(k in ids for k in con['controls']), side + ' control missing')


def validate_forward(res, report, ref, con):
    G = ref['g']
    expect(res.get('contract_sha256') == CONTRACT_SHA and res.get('loop') == 'BD1' and res.get('direction') == 'forward'
           and res.get('route_of_computation') == 'characters', 'forward identity')
    for k in ('continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified', 'uniqueness_of_ground_state_claimed',
              'transfers_to_aq', 'rate_in_a_claimed', 'uniform_wilson_claim', 'resolved_interaction_shift',
              'am2_claim_for_other_groups', 'dictionary_for_other_groups'):
        expect(res.get(k) is False, 'forward claim flag ' + k)
    expect(res.get('model_is_finite_graph') is True and res.get('flip_transfer_claimed') is True
           and res.get('parity_transfer_claimed') is True and res.get('obstructions_recorded') is True
           and res.get('area_parity_limit_claimed') is True, 'forward claimed columns')
    for g in GROUPS:
        R, c = G[g], res['cells'][g]
        expect(rat(c['C_F']) == R['CF'], 'forward C_F ' + g)
        expect({k: rat(v) for k, v in c['moments'].items()} == {str(k): R['mom'][k - 1] for k in range(1, 6)}, 'forward moments ' + g)
        labelled(c['first_order_coefficient'], R['c1'], True, 'characters', 'forward c1 ' + g)
        labelled(c['first_order_derivative_omega_W2'], R['dW2'], True, 'characters', 'forward dW2 ' + g)
        labelled(c['second_order_coefficient_omega_W'], R['omW'][2], False, 'characters', 'forward omega_2 ' + g)
        labelled(c['fourth_order_coefficient_omega_W'], R['omW'][4], False, 'characters', 'forward omega_4 ' + g)
        expect(c['flip'] == ('transfer_to_named_model' if g in FLIP else 'obstruction_recorded')
               and c['parity'] == ('transfer_to_named_model' if g in PARITY else 'obstruction_recorded'), 'forward classification ' + g)
        expect(c['central_minus_one'] == ('1/2' if R['central'] else None), 'forward centre ' + g)
        expect(rat(c['kato_radius_one_plaquette']) == R['kato_fg'], 'forward Kato one-plaquette ' + g)
        expect(c['wilson_representation'] == pre.WILSON_REP[g] and c['model_is_finite_graph'] is True
               and c['transfers_to_aq'] is False, 'forward cell labels ' + g)
    tiered = ('first_order_coefficient', 'first_order_derivative_omega_W2', 'first_order_derivative_C_state',
              'first_order_derivative_C_duhamel')
    want = {'haar_moment': None, 'first_order_coefficient': 'c1', 'first_order_derivative_omega_W2': 'dW2',
            'first_order_derivative_C_state': 'dW2', 'first_order_derivative_C_duhamel': 'duhamel'}
    seen = {}
    for e in res['value_entries']:
        g, kind = e['group'], e['kind']
        expect(g in G and e.get('tau') == 'symbolic' and e.get('wilson_representation') == pre.WILSON_REP[g], 'forward entry labels')
        R = G[g]
        if kind == 'haar_moment':
            val = R['mom'][e['k'] - 1]
        elif kind == 'second_order_coefficient_omega_W':
            val = R['omW'][2]
        elif kind == 'fourth_order_coefficient_omega_W':
            val = R['omW'][4]
        else:
            expect(kind in want, 'forward entry kind ' + kind)
            val = R[want[kind]]
        box = e['model'] == 'H^%s_N' % g
        expect(e['model'] == 'H_FG(%s)' % g or (box and kind in ('first_order_coefficient', 'first_order_derivative_omega_W2')),
               'forward entry model ' + e['model'])
        labelled(e, val, kind in tiered, 'characters', 'forward entry %s %s %s' % (g, kind, e['model']))
        seen[(g, kind, e['model'])] = seen.get((g, kind, e['model']), 0) + 1
    expect(len(res['value_entries']) == 91 and len(seen) == 63, 'forward value entries incomplete')
    hl = res['headline']
    expect({g: rat(v) for g, v in hl['first_order_coefficients'].items()} == {g: G[g]['c1'] for g in GROUPS}, 'forward headline first-order')
    expect(all(is_truncation(hl['first_order_previews'][g], G[g]['c1']) for g in GROUPS), 'forward headline previews')
    expect({g: {k: rat(v) for k, v in hl['moment_table'][g].items()} for g in GROUPS}
           == {g: {str(k): G[g]['mom'][k - 1] for k in range(1, 6)} for g in GROUPS}, 'forward headline moments')
    expect(all(is_truncation(hl['moment_previews'][g][str(k)], G[g]['mom'][k - 1]) for g in GROUPS for k in range(1, 6)),
           'forward moment previews')
    expect(hl['flip_transfer_groups'] == FLIP and hl['parity_transfer_groups'] == PARITY, 'forward classification')
    ob = hl['obstruction_values']
    expect(all(rat(ob[g]['E_W3']) == G[g]['E3'] and rat(ob[g]['c2_omega_W']) == G[g]['omW'][2]
               and rat(ob[g]['d_omega_W2_dtau']) == G[g]['dW2'] for g in ('SU(3)', 'SO(3)', 'SU(5)'))
           and rat(ob['SU(5)']['c4_omega_W']) == G['SU(5)']['omW'][4] and ob['SU(5)']['c4_closed_form'] == '1/(2^30 3^10)',
           'forward obstruction values')
    fc = hl['flip_set_counts']
    B = ref['boxes']
    expect(all(fc['E3_boxes'][str(n)] == {'anchors': B[n]['anchors'], 'links': B[n]['links'], 'plaquettes_owned': B[n]['plaquettes'],
                                            'plaquette_histogram': {'1': B[n]['once'], '3': B[n]['three']},
                                            'retained_faces': B[n]['retained'],
                                            'retained_histogram': {'1': B[n]['retained_once'], '3': B[n]['retained_three']}}
               for n in (2, 3, 4)), 'forward box counts')
    expect(fc['E2_boxes'] == {str(n): (2 * n) ** 2 for n in (2, 3, 4)} and fc['E3_factor_links_by_z_parity'] == {'0': [16], '1': [8]}
           and fc['E3_plaquettes_meeting_each_factor'] == 52, 'forward factor counts')
    T = ref['tori']
    expect(fc['tori_E3_even_seam'] == {'x'.join(map(str, s)): T[s]['even'] for s in ((4, 4, 4), (3, 4, 4), (4, 3, 4), (4, 4, 3), (3, 3, 4))}
           and fc['tori_E2_even_seam'] == {'x'.join(map(str, s)): T[s]['even'] for s in ((4, 4), (4, 3), (3, 4), (3, 3))},
           'forward tori')
    expect(rat(hl['area_parity']['corollary_tau']) == F(1, 10 ** 8) and hl['area_parity']['loops_checked'] == 9
           and hl['area_parity']['closed_surfaces_checked'] == 5, 'forward area-parity headline')
    # gate fields: the literal frozen value, and the groups named in gate_field_groups
    expect(res['gate_fields'] == con['preregistration']['gate_fields_required'], 'forward gate fields')
    gg = res['gate_field_groups']
    expect(gg['flip_transfer_groups'] == FLIP and gg['parity_transfer_groups'] == PARITY and gg['obstruction_groups'] == OBSTRUCTIONS
           and groups_named(gg['flip_transfer_scope_named']) == FLIP, 'forward flip scope groups')
    # checks with values
    rs = check_by_id(res, 'rayleigh_schroedinger_one_plaquette')['series']
    for g in GROUPS:
        R, s_ = G[g], rs[g]
        expect([rat(x) for x in s_['ground_energy']] == R['E'] and [rat(x) for x in s_['omega_W']] == R['omW']
               and [rat(x) for x in s_['omega_W2']] == R['omW2'] and [rat(x) for x in s_['omega_C2']] == R['omC2'],
               'forward RS series ' + g)
    cb = check_by_id(res, 'criterion_B_box_models')
    for g in GROUPS:
        bt, Rb = cb['box_terms'][g], G[g]['box']
        expect(rat(bt['mean_sum_E[W W_f]']) == Rb['mean_sum'] and rat(bt['state_sum_E[W^2 W_f]']) == Rb['state_sum']
               and rat(bt['duhamel_sum_E[W W_f W]']) == Rb['duhamel_sum'] and rat(bt['energy_sum_E[W_f]']) == Rb['energy_sum']
               and rat(bt['first_order_coefficient_box']) == Rb['c1_box'] and rat(bt['d_omega_W2_dtau_box']) == Rb['dW2_box'],
               'forward box terms ' + g)
        kr = cb['kato_radius_sufficient'][g]
        expect(rat(kr['one_plaquette']) == G[g]['kato_fg'] and {n: rat(v) for n, v in kr['box'].items()}
               == {str(n): v for n, v in Rb['kato_box'].items()}, 'forward Kato ' + g)
    expect(cb['max_links_shared_by_distinct_plaquettes'] == 1 == ref['box_sums']['max_shared_links'], 'forward single occurrence')
    expect(check_by_id(res, 'criterion_A_box_models')['faces_checked'] == ref['box_sums']['faces'], 'forward fixture faces')
    fs = check_by_id(res, 'flip_sets_verified')
    for key, row in fs['factors'].items():
        b = tuple(int(x) for x in key.split(','))
        Rf = ref['factors'][b]
        expect(row['links_in_E3'] == Rf['E3_links'] and row['plaquettes_meeting_factor'] == Rf['faces']
               and row['selected_faces_anchored'] == Rf['selected'] and row['omitted_faces_containing_factor'] == Rf['omitted']
               and row['histogram_meeting'] == Rf['hist'] and row['z_parity'] == Rf['z_parity'], 'forward factor ' + key)
    for key, row in list(fs['periodic_tori_E3'].items()) + list(fs['periodic_tori_E2'].items()):
        s_ = tuple(int(x) for x in key.split('x'))
        expect(row == {'plaquettes': T[s_]['plaquettes'], 'even_plaquettes_at_seam': T[s_]['even']}, 'forward tori ' + key)
    su5 = check_by_id(res, 'su5_flip_obstruction_fourth_order')
    expect(rat(su5['cell']['c4_omega_W']) == G['SU(5)']['omW'][4] and rat(su5['cell']['c3_omega_W']) == G['SU(5)']['omW'][3]
           and is_truncation(su5['c4_preview'], G['SU(5)']['omW'][4]), 'forward SU(5) cell')
    ap = check_by_id(res, 'area_parity_box_and_limit')
    expect(ap['bb2_constants_read']["c'_site"] == q_(ref['bb2']['csite']) and ap['bb2_constants_read']['q'] == q_(ref['bb2']['q']),
           'forward BB2 constants')
    eps = F(1, 10 ** 40)
    for name, row in ap['loops'].items():
        A, Ys, m = row['area_flat'], row['region_Y_sites'], row['max_site_linf']
        expect(row['links_in_E3'] % 2 == A % 2 == row['area_alternative'] % 2 and row['sign_(-1)^A'] == (-1) ** A,
               'forward loop parity ' + name)
        N0 = max(2, m)
        expect(row['N0'] == N0 and rat(row['bb2_bound_at_N0']) == bb2_bound(ref, Ys, m, N0)
               and is_truncation(row['bb2_bound_preview_at_N0'], bb2_bound(ref, Ys, m, N0)), 'forward BB2 bound ' + name)
        Ne = row['N_where_twice_bound_below_1e-40']
        expect(2 * bb2_bound(ref, Ys, m, Ne) <= eps and (Ne == N0 or 2 * bb2_bound(ref, Ys, m, Ne - 1) > eps),
               'forward BB2 bound N ' + name)
    wrow = ap['loops']['W_face_xz_1x1']
    expect(wrow['region_Y_sites'] == ref['w_region']['Y'] and wrow['max_site_linf'] == ref['w_region']['m'], 'forward W-face region')
    expect(all(v['plaquettes'] % 2 == 0 and v['sum_links_in_E3'] % 2 == 0 for v in ap['closed_surfaces'].values()),
           'forward closed surfaces')
    led = {(r['group'], r['equation']): r for r in res['transfer_ledger']}
    for g in GROUPS:
        expect(led[(g, 'flip_lemma')]['status'] == ('transfer_to_named_model' if g in FLIP else 'obstruction_recorded')
               and led[(g, 'parity_theorem')]['status'] == ('transfer_to_named_model' if g in PARITY else 'obstruction_recorded')
               and rat(led[(g, 'first_order_coefficient')]['value']) == G[g]['c1']
               and led[(g, 'dictionary')]['status'] == ('admitted_su2_reference' if g == 'SU(2)' else 'not_asserted')
               and led[(g, 'am2_aq_chain')]['status'] == ('admitted_su2_reference' if g == 'SU(2)' else 'obligation'),
               'forward ledger ' + g)
    expect(res.get('supported_statement') == con['preregistration']['mandatory_sentence_template'], 'forward supported statement')
    common_text(res, report, con, 'forward')
    _, bad = report_previews('forward', report, ref)
    expect(bad == [], 'forward report preview differs: %r' % (bad[:1],))
    return True


def validate_reverse(res, report, ref, con):
    G = ref['g']
    expect(res.get('contract_snapshot_sha256') == CONTRACT_SHA and res.get('loop') == 'BD1' and res.get('direction') == 'reverse'
           and res.get('route_of_computation') == 'weyl_integration', 'reverse identity')
    for k in ('continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified', 'uniqueness_of_ground_state_claimed',
              'transfers_to_aq', 'rate_in_a_claimed', 'uniform_wilson_claim', 'resolved_interaction_shift',
              'historical_or_occult_provenance_premise'):
        expect(res.get(k) is False, 'reverse claim flag ' + k)
    rt = 'weyl_integration'
    for g in GROUPS:
        R, mt = G[g], res['moment_table'][g]
        ks = range(1, 7) if g == 'SU(5)' else range(1, 5)
        expect(sorted(mt) == sorted('E[W^%d]' % k for k in ks), 'reverse moment cells ' + g)
        for k in ks:
            labelled(mt['E[W^%d]' % k], R['mom'][k - 1], False, rt, 'reverse moment %s k=%d' % (g, k))
        fo = res['first_order_coefficients'][g]
        labelled(fo, R['c1'], True, rt, 'reverse c1 ' + g)
        expect('H_FG(%s)' % g in fo['models'] and 'H^{%s}_N' % g in fo['models'], 'reverse first-order models ' + g)
        ser = res['one_plaquette_series'][g]
        expect([rat(x) for x in ser['energy']] == R['E'] and [rat(x) for x in ser['omega_W']] == R['omW'][:5]
               and [rat(x) for x in ser['omega_W2']] == R['omW2'][:3], 'reverse one-plaquette series ' + g)
        ft = res['first_order_terms'][g]
        labelled(ft['d_omega_W2_dtau'], R['dW2'], True, rt, 'reverse dW2 ' + g)
        labelled(ft['state_term_coefficient'], R['dW2'], True, rt, 'reverse state term ' + g)
        labelled(ft['duhamel_coefficient'], R['duhamel'], True, rt, 'reverse Duhamel term ' + g)
        expect(ft['energy_term_E1'] == '0' and ft['parity_holds'] is (R['E3'] == 0), 'reverse first-order terms ' + g)
        cm = res['cubic_moments'][g]
        expect({(int(k[6]), int(k[-2])): v for k, v in cm.items()} == {(a, 3 - a): R['mixed'][(a, 3 - a)] for a in range(4)},
               'reverse cubic moments ' + g)
        expect(res['centre'][g]['central_minus_one'] is R['central'], 'reverse centre ' + g)
        expect(res['level_splitting'][g]['zero_first_order_splitting'] is (R['E3'] == 0), 'reverse level splitting ' + g)
        kr = res['kato_radii'][g]
        expect(rat(kr['one_plaquette_radius']) == R['kato_fg']
               and all(rat(kr['box_radius_N%d' % n]) == R['box']['kato_box'][n] for n in (2, 3, 4)), 'reverse Kato ' + g)
    for g in ('SU(3)', 'SO(3)'):
        R, c = G[g], res['obstruction_cells'][g]
        expect(rat(c['E_W3']) == R['E3'] and rat(c['d_omega_W2_dtau']) == R['dW2'] and rat(c['omega_2']) == R['omW'][2]
               and rat(c['omega_3']) == R['omW'][3] and rat(c['omega_4']) == R['omW'][4] and c['central_minus_one'] is False
               and c['status'] == 'obstruction' and c['omega_W_odd_in_tau'] is False and c['first_order_parity_holds'] is False,
               'reverse obstruction cell ' + g)
        labelled(c['d_omega_W2_dtau_entry'], R['dW2'], True, rt, 'reverse obstruction dW2 ' + g)
        labelled(c['omega_2_entry'], R['omW'][2], False, rt, 'reverse obstruction omega_2 ' + g)
        expect(is_truncation(c['previews']['d_omega_W2_dtau'], R['dW2']) and is_truncation(c['previews']['omega_2'], R['omW'][2]),
               'reverse obstruction previews ' + g)
    c5, R5 = res['obstruction_cells']['SU(5)'], G['SU(5)']
    expect(rat(c5['E_W3']) == 0 and rat(c5['omega_2']) == 0 and rat(c5['d_omega_W2_dtau']) == 0
           and rat(c5['omega_3']) == R5['omW'][3] and rat(c5['omega_4']) == R5['omW'][4] and c5['omega_4_factored'] == '1/(2^30 3^10)'
           and c5['flip_status'] == 'obstruction' and c5['parity_status'] == 'transfer' and c5['central_minus_one'] is False
           and is_truncation(c5['omega_4_preview'], R5['omW'][4]), 'reverse SU(5) cell')
    labelled(c5['omega_4_entry'], R5['omW'][4], False, rt, 'reverse SU(5) omega_4')
    fs, B, T = res['flip_sets'], ref['boxes'], ref['tori']
    expect(fs['E_2_boxes'] == {'N=%d' % n: (2 * n) ** 2 for n in (2, 3, 4)}
           and all(fs['E_3_boxes']['N=%d' % n] == {'anchors': B[n]['anchors'], 'meet_once': B[n]['once'], 'meet_three_times': B[n]['three'],
                                                    'owned_plaquettes': B[n]['plaquettes'], 'retained_faces': B[n]['retained']}
                   for n in (2, 3, 4)), 'reverse box counts')
    for key, row in fs['E_3_factors'].items():
        b = tuple(int(x) for x in key.strip('()').split(','))
        Rf = ref['factors'][b]
        expect(row == {'E3_links_in_factor': Rf['E3_links'], 'omitted_faces_meeting': Rf['omitted'], 'selected_faces': Rf['selected'],
                       'z_parity': Rf['z_parity']}, 'reverse factor ' + key)
    for key, row in fs['tori'].items():
        s_ = tuple(int(x) for x in key.split(' on ')[1].split('x'))
        expect(key.startswith('E_3 on ' if len(s_) == 3 else 'E_2 on ')
               and row == {'any_flip_set_exists_gf2': T[s_]['gf2'], 'even_plaquettes': T[s_]['even']}, 'reverse tori ' + key)
    gf = res['gate_fields']
    req = con['preregistration']['gate_fields_required']
    expect(sorted(set(gf) - set(req)) == ['obstructions', 'parity_transfer_scope'] and set(req) <= set(gf)
           and all(gf[k] == v for k, v in req.items() if k != 'flip_transfer_scope'), 'reverse gate fields')
    expect(groups_named(gf['flip_transfer_scope']) == FLIP and 'central' in gf['flip_transfer_scope']
           and groups_named(gf['parity_transfer_scope']) == PARITY and gf['flip_transfer_scope'] == res['flip_transfer_scope'],
           'reverse flip scope groups')
    ap = res['area_parity']
    expect(ap['claim']['group'] == 'SU(2)' and ap['claim']['kappa'] == '0' and rat(ap['tau']) == F(1, 10 ** 8)
           and all(rat(v['W_flipped']) == (-1) ** v['area'] * rat(v['W']) for v in ap['fixture'].values()), 'reverse area fixture')
    for row in res['transfer_ledger']:
        g = row['group']
        expect(row['flip_lemma']['status'] == ('transfer' if g in FLIP else 'obstruction')
               and row['parity_theorem']['status'] == ('transfer' if g in PARITY else 'obstruction')
               and rat(row['first_order_coefficient']['value']) == G[g]['c1'] and row['first_order_coefficient']['tier'] == TIER
               and (g == 'SU(2)' or row['dictionary']['status'] == 'not_asserted'), 'reverse ledger ' + g)
    expect(sorted(r['group'] for r in res['transfer_ledger']) == sorted(GROUPS), 'reverse ledger groups')
    common_text(res, report, con, 'reverse')
    _, bad = report_previews('reverse', report, ref)
    expect(sorted(bad) == sorted(KNOWN_REPORT_PREVIEW_DEFECTS), 'reverse report preview differs: %r' % (bad[:2],))
    return True


VALIDATORS = {'forward': validate_forward, 'reverse': validate_reverse}


# ------------------------------------------------------------ closure, replays, mutation harness
def verify_closure(side):
    d, rel = DIRS[side], RELS[side]
    freeze = json.loads((d / 'freeze.json').read_text())
    sources = freeze['sources']
    files = {p.relative_to(ROOT).as_posix() for p in d.rglob('*') if p.is_file() and p != d / 'freeze.json'}
    ok = (freeze['loop'] == 'BD1' and freeze['direction'] == side and freeze['contract_sha256'] == CONTRACT_SHA
          and all(n.startswith(rel + '/') for n in sources) and set(sources) == files and len(sources) == 27
          and all(sha(ROOT / n) == h for n, h in sources.items())
          and not any('__pycache__' in n or n.endswith('.pyc') for n in files)
          and freeze['normal_optimized_identical'] is True and freeze['independent_before_current_counterpart_exchange'] is True
          and freeze['verdict'].startswith('accepted_within_scope'))
    inputs = sorted(p.relative_to(d / 'inputs').as_posix() for p in (d / 'inputs').rglob('*') if p.is_file())
    snaps = all((d / 'inputs' / n).read_bytes() == (ROOT / n).read_bytes() for n in inputs)
    return ok, inputs, snaps, freeze


def caches():
    return sorted({p.relative_to(ROOT).as_posix() for d in DIRS.values() for p in d.rglob('*')
                   if p.name == '__pycache__' or p.suffix == '.pyc'})


def replay(script, pre_mode=False):
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bd1-skeptic-replay-') as tmp:
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(script), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(ROOT))
        if done.returncode != 0:
            raise ReviewFailure('replay failed: ' + str(script) + ' ' + done.stderr[-300:])
        return {p.relative_to(out).as_posix(): sha(p) for p in sorted(out.rglob('*')) if p.is_file()}, \
            ((out / 'results.json').read_bytes() if pre_mode else None)


def mutated_run(side, edits=(), report_edits=(), report_append=None, extra_input=None, input_edit=None, no_b=False):
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bd1-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / RELS[side]
        shutil.copytree(DIRS[side], dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        code = (dst / 'check.py').read_text()
        for old, new in edits:
            if code.count(old) != 1:
                raise ReviewFailure('mutation anchor not unique (%d): %r' % (code.count(old), old[:80]))
            code = code.replace(old, new)
        (dst / 'check.py').write_text(code)
        if report_edits or report_append is not None:
            rp = dst / 'report.md'
            text = rp.read_text()
            for old, new in report_edits:
                if text.count(old) != 1:
                    raise ReviewFailure('report mutation anchor not unique: %r' % old[:70])
                text = text.replace(old, new)
            if report_append is not None:
                text += report_append
            rp.write_text(text)
        if extra_input is not None:
            extra = dst / 'inputs' / extra_input
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text('skeptic mutation fixture\n')
        if input_edit is not None:
            rel, old, new = input_edit
            ip = dst / 'inputs' / rel
            raw = ip.read_bytes()
            if raw.count(old) != 1:
                raise ReviewFailure('input mutation anchor not unique: ' + rel)
            ip.write_bytes(raw.replace(old, new))
        out = Path(tmp) / 'out'
        flags = ([] if no_b else ['-B']) + (['-O'] if sys.flags.optimize else [])
        env = None
        if no_b:
            env = {k: v for k, v in os.environ.items() if k != 'PYTHONDONTWRITEBYTECODE'}
        done = subprocess.run([sys.executable] + flags + [str(dst / 'check.py'), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(repo), env=env)
        results = json.loads((out / 'results.json').read_text()) if (out / 'results.json').is_file() else None
        outputs = {p.name: p.read_bytes() for p in sorted(out.glob('*.json'))} if out.is_dir() else {}
        report = (dst / 'report.md').read_text()
        err = done.stderr.strip()
        last = err.splitlines()[-1] if err else ''
        ctl = re.findall(r"control\('([a-z0-9_]+)'", err)
        cache = sorted(p.relative_to(repo).as_posix() for p in repo.rglob('*') if p.name == '__pycache__' or p.suffix == '.pyc')
        return done.returncode, results, outputs, report, last.replace(tmp, '<tmp>'), cache, (ctl[-1] if ctl else None)


def parallel(fn, jobs):
    with ThreadPoolExecutor(max_workers=4) as ex:
        return list(ex.map(fn, jobs))


def tru(anchor):
    """Validator weakening: insert 'True or ' into the require(...) at the anchor."""
    if not anchor.lstrip().startswith('require('):
        raise ReviewFailure('weakening anchor is not a require: ' + anchor[:60])
    return [(anchor, anchor.replace('require(', 'require(True or ', 1))]


WEAK_F = [  # forward: the producer aborts with 'damaging mutation accepted: <label>'
    ('coherent_evidence_tampering', tru("            require(cid in ids and ids[cid]['passed'] is True, 'required control missing or failed: ' + cid)"),
     'control_boolean_flipped_hash_rebound'),
    ('exact_arithmetic_admission', [("        raise AdmissionError('non-exact input rejected: ' + repr(value))", "        return Q(value)")],
     'float_input'),
    ('no_priority_or_continuum_claim', tru("            require(fl[k] is False, 'claim flag must be false: ' + k)"), 'continuum_claim_true'),
    ('changed_model_relabelled', tru("        require(rat(e['value']) == expected_value(e), \"value differs from the group's own cell (relabelled value)\")"),
     'SU2_value_under_SU3_label'),
    ('insufficient_verdict_retained', tru("        require(claimed == expected_verdict(o), 'claimed verdict differs from the outcome-determined verdict')"),
     'failed_cell_reported_accepted'),
    ('placeholder_span_rejected', tru("    require(not placeholder_spans(text), 'placeholder span in ' + label)"), 'angle_bracket_placeholder_with_e_g'),
    ('negation_aware_phrase_scan', tru("    require(not affirmative_hits(text, forbidden, template), 'affirmative forbidden phrasing in ' + label)"),
     'affirmative_forbidden_verb'),
    ('parameters_declare_metric_weights_window',
     tru("                require(len(pp[key]) > len('not applicable') + 5, 'not applicable without its reason: ' + key)"),
     'not_applicable_without_reason'),
    ('tier_mixing_rejected', tru("            require('hypothesis_source' not in e, 'a hypothesis source attached to a BD1 value')"),
     'hypothesis_source_attached'),
    ('frozen_convention_used', tru("        require(rat(cell['C_F']) == CF_rule[g], 'Casimir normalization differs from the frozen convention for ' + g)"),
     'Z2_electric_1_on_odd'),
    ('su2_constants_not_transferred',
     tru("                require('dictionary' not in e and 'source' not in e, 'dictionary or SU(2) source attached to ' + e['group'])"),
     'SU3_alpha_dictionary'),
    ('flip_criterion_central_minus_one',
     tru("            require(row.get('central_element') is not None and central[g] is not None and rat(row['central_element']) == central[g],"),
     'SU3_flip_transfer'),
    ('parity_criterion_third_moment', tru("            require(E3[g] == 0, 'parity claimed with nonzero third moment: ' + g)"), 'SU3_parity_transfer'),
    ('moment_tables_two_routes', tru("            require(rat(ta['cells'][k]) == rat(tb['cells'][k]), 'routes disagree on ' + k)"),
     'floating_point_moment'),
    ('su3_obstruction_mandatory',
     tru("        require(cell['flip'] == 'obstruction_recorded' and cell['parity'] == 'obstruction_recorded', g + ' called a transfer')"),
     'su3_called_flip_transfer'),
    ('so3_obstruction_mandatory',
     tru("        require(cell['group'] == g and cell['central_minus_one'] is None and cell['det_minus_identity'] == -1, 'central -1 status')"),
     'so3_given_a_central_minus_one'),
    ('flip_sets_verified', tru("        require(flip_count(f, in_E) % 2 == 1, 'even intersection with the flip set (' + label + ') at ' + repr(f))"),
     'E3_minus_one_link'),
    ('area_parity_scope',
     tru("        require(cl['region'] in ('open_centered_whole_star_box', 'on_site_cutoff', 'limit_of_named_constructions'),"),
     'periodic_box_with_odd_side'),
    ('one_plaquette_model_terms',
     tru("        require(cell['model_is_finite_graph'] is True and cell['transfers_to_aq'] is False, 'finite-graph labels')"),
     'transfers_to_aq_true'),
    ('no_transfer_called_prediction',
     tru("                require(re.search(r'(?<![\\w])' + w + r'(?![\\w])', txt, re.I) is None, 'a transfer or non-transfer described with a forbidden verb')"),
     'transfer_text_with_forbidden_verb'),
    ('am2_not_reinstantiated',
     tru("                require(r['status'] == 'obligation' and r['obligations'], 'an AM2, AV1 or AQ chain claimed for ' + r['group'])"),
     'U1_am2_chain_transfer'),
    ('su5_flip_obstruction_fourth_order', tru("        require(cell['flip'] == 'obstruction_recorded', 'SU(5) called a flip transfer')"),
     'su5_called_flip_transfer'),
]
WEAK_R = [  # reverse: the producer aborts with 'damaging mutation accepted by <validator>' inside control('<id>', ...)
    ('coherent_evidence_tampering', tru("        require(c is not None and c.get('passed') is True and c.get('kind') == 'damaging_mutation_control'"),
     'validate_results_controls'),
    ('exact_arithmetic_admission', [("        raise Rejected('non-exact numeric input rejected')", "        return Q(value)")], 'parse_q'),
    ('no_priority_or_continuum_claim', tru("        require(flags.get(k) is False, 'claim flag must be false: ' + k)"), 'validate_claim_flags'),
    ('changed_model_relabelled',
     tru("    require(parse_q(cell.get('value')) == ref['value'], 'value under this group label is not the value computed for it')"),
     'validate_cell'),
    ('insufficient_verdict_retained', tru("    require(recorded == producer_outcome(inp), 'recorded outcome differs from the frozen outcome rule')"),
     'certify_outcome'),
    ('placeholder_span_rejected', tru("    require(bad == [], 'angle-bracket placeholder span rejected (%d spans)' % len(bad))"), 'certify_no_placeholder'),
    ('negation_aware_phrase_scan', tru("    require(aff == [], 'affirmative forbidden phrase rejected (list indices %s)' % sorted(set(aff)))"),
     'certify_phrase_scan'),
    ('parameters_declare_metric_weights_window', tru("            require(len(txt[len('not applicable'):].strip(' ;,')) >= 8,"),
     'validate_parameters'),
    ('tier_mixing_rejected', tru("    require('hypothesis_source' not in entry, 'hypothesis source attached to a BD1 value')"), 'validate_value_entry'),
    ('frozen_convention_used',
     tru("    require(parse_q(value) == first_order_from_convention(E_W2, C_F), 'first-order cell not computed under the frozen convention')"),
     'certify_first_order_cell'),
    ('su2_constants_not_transferred',
     tru("        require(entry.get('dictionary') is None, 'dictionary to a bare coupling asserted for a group other than SU(2)')"),
     'certify_no_su2_constant'),
    ('flip_criterion_central_minus_one', tru("        require(flip_sets_ok is True, 'flip claimed without verified flip sets')"), 'certify_flip_entry'),
    ('parity_criterion_third_moment', tru("        require(e_w3[g] == 0, 'parity claimed with a nonzero third moment')"), 'certify_parity_entry'),
    ('moment_tables_two_routes', tru("        require(parse_q(t1[k]) == parse_q(t2[k]), 'routes disagree on a cell')"), 'compare_route_tables'),
    ('su3_obstruction_mandatory',
     tru("    require(cell.get('group') == name and cell.get('status') == 'obstruction', 'obstruction cell called a transfer')"),
     'certify_obstruction_cell'),
    ('so3_obstruction_mandatory', tru("    require(cell.get('central_minus_one') is False, 'obstruction cell with a central -1')"),
     'certify_obstruction_cell'),
    ('flip_sets_verified',
     tru("        require(all(c % 2 == 1 for c in counts), 'flip set meets %d plaquettes evenly' % sum(1 for c in counts if c % 2 == 0))"),
     'certify_flip_set'),
    ('area_parity_scope',
     tru("    require(all(b in AREA_BOXES for b in claim.get('boxes', [])) and len(claim.get('boxes', [])) > 0, 'area parity claimed for another boundary condition or box family')"),
     'certify_area_parity_claim'),
    ('one_plaquette_model_terms',
     tru("    require(model.get('model_is_finite_graph') is True and model.get('transfers_to_aq') is False, 'finite-graph labels')"),
     'certify_fg_model'),
    ('no_transfer_called_prediction', tru("        require(re.search(r'(?<![\\w])' + v + r'(?![\\w])', text, re.I) is None,"),
     'certify_no_forbidden_verbs'),
    ('am2_not_reinstantiated',
     tru("            require(claims.get(k) is False, 'AM2/AV1/AQ chain or dictionary statement for a group other than SU(2) rejected')"),
     'certify_chain_claims'),
    ('su5_flip_obstruction_fourth_order', tru("    require(cell.get('flip_status') == 'obstruction', 'SU(5) called a flip transfer')"),
     'certify_su5_cell'),
]
WEYL_KEY = "            key = tuple(x - e[-1] for x in e[:-1])"
WEYL_CT = "                ct = sum(c * red.get(tuple(-(x - e[-1]) for x in e[:-1]), 0) for e, c in f.items())"
TEMPLATE_ANCHOR = 'Under the frozen convention, the link-flip lemma transfers exactly to the listed gauge groups'
MUST_ABORT = [  # (side, label, kwargs, expected fragment of the last stderr line)
    ('forward', 'forward-internal Weyl cross-check on the U(N) torus (exponent 0 only)',
     {'edits': [(WEYL_KEY, "            key = tuple(e)"), (WEYL_CT, WEYL_CT.replace("tuple(-(x - e[-1]) for x in e[:-1])", "tuple(-x for x in e)"))]},
     'routes disagree on SU(2):E[W^2]'),
    ('forward', 'SU(3) third moment zeroed in the characters route',
     {'edits': [("        out.append(vec.get(G.triv, Q(0)))",
                 "        out.append(Q(0) if (G.name == 'SU(3)' and len(out) == 2) else vec.get(G.triv, Q(0)))")]},
     'failed check moments_characters_route'),
    ('forward', 'Z2 odd-state Casimir 1/4 (another normalization)',
     {'edits': [("tensor_Fbar=lambda r: {(r + 1) % 2: 1}, casimir=lambda r: Q(r),", "tensor_Fbar=lambda r: {(r + 1) % 2: 1}, casimir=lambda r: Q(r, 4),")]},
     'failed check character_rules'),
    ('forward', 'flip-set membership without x-links (E_3 and E_2)', {'edits': [("        return d in spec and p[spec[d]] % 2 == 0", "        return d != 0 and d in spec and p[spec[d]] % 2 == 0")]},
     'the flip does not reverse W_f for SU(2)'),
    ('forward', 'input: BB2 gate c\'_site edited', {'input_edit': (BB2_GATE, b"|y|_inf and c'_site=2/984375 (about", b"|y|_inf and c'_site=1/500000 (about")},
     'admitted gate snapshot differs from its pinned sha256'),
    ('forward', 'input: contract snapshot edited', {'input_edit': ('research/round33/contracts/bd1.json', b'"N_min": "2"', b'"N_min": "3"')},
     'contract snapshot bytes differ from the frozen BD1 contract'),
    ('forward', 'input: undeclared skeptic file', {'extra_input': 'research/round33/skeptic/bd1-independent-derivation.md'},
     'failed check premise_inventory'),
    ('forward', 'report: forbidden phrase appended', {'report_append': '\nThe limit of the named constructions is the thermodynamic limit.\n'},
     'affirmative forbidden phrasing in report.md'),
    ('forward', 'report: template altered', {'report_edits': [(TEMPLATE_ANCHOR, 'Under the frozen convention, the link-flip lemma transfers to the listed gauge groups')]},
     'the mandatory template must appear once as one unbroken span'),
    ('reverse', 'Weyl integration on the U(N) torus (exponents not reduced modulo the diagonal)',
     {'edits': [("        m = min(e)", "        m = 0")]}, 'check failed: haar_moments_weyl_integration'),
    ('reverse', 'first-order formula with face energy 24 C_F', {'edits': [("def first_order_from_convention(E_W2, C_F, per_link=8,", "def first_order_from_convention(E_W2, C_F, per_link=6,")]},
     'first-order coefficient: closed form, torus RS and Hellmann-Feynman'),
    ('reverse', 'SU(5) closed form perturbed by 10^-30', {'edits': [("    w4_closed = Q(10, 81) * Q(1, 10 ** 5) / prodE", "    w4_closed = Q(10, 81) * Q(1, 10 ** 5) / prodE + Q(1, 10 ** 30)")]},
     'SU(5) fourth-order coefficient'),
    ('reverse', 'input: BB2 gate c\'_site edited', {'input_edit': (BB2_GATE, b"|y|_inf and c'_site=2/984375 (about", b"|y|_inf and c'_site=1/500000 (about")},
     'gate bytes do not match the pinned hash'),
    ('reverse', 'input: contract snapshot edited', {'input_edit': ('research/round33/contracts/bd1.json', b'"N_min": "2"', b'"N_min": "3"')},
     'contract snapshot hash differs from the pinned value'),
    ('reverse', 'input: undeclared skeptic file', {'extra_input': 'research/round33/skeptic/bd1-independent-derivation.md'},
     'inputs inventory differs from AGENTS.md, the contract and shared_premises'),
    ('reverse', 'report: forbidden phrase appended', {'report_append': '\nThe limit of the named constructions is the thermodynamic limit.\n'},
     'affirmative forbidden phrase rejected'),
    ('reverse', 'report: template altered', {'report_edits': [(TEMPLATE_ANCHOR, 'Under the frozen convention, the link-flip lemma transfers to the listed gauge groups')]},
     'mandatory template must appear exactly once as one unbroken span'),
]
SILENT = [  # (side, label, kwargs, reason the review validator must give, or None for a harmless edit)
    ('forward', 'harmless: second RS stability depth ORDER+5', {'edits': [("depth=ORDER + 4)", "depth=ORDER + 5)")]}, None),
    ('forward', "BB2 c'_site read as the labelled union-comparison value 1/500000",
     {'edits': [("    out['bb2_csite'] = Q(int(m.group(1)), int(m.group(2)))", "    out['bb2_csite'] = Q(1, 500000)")]}, 'forward BB2 constants'),
    ('forward', 'region bound without the factor e^{|Y|/10^8}', {'edits': [("        eb = 1 / (1 - Q(len(Y), 10 ** 8))", "        eb = 1")]},
     'forward BB2 bound'),
    ('reverse', 'harmless: previews with 13 digits', {'edits': [("PREVIEW_DIGITS = 12", "PREVIEW_DIGITS = 13")]}, None),
    ('reverse', 'box Kato radius at N=2 doubled',
     {'edits': [("'box_radius_N2': qs(12 * cmin[name] / box_stats['N=2']['retained_faces']),",
                 "'box_radius_N2': qs(24 * cmin[name] / box_stats['N=2']['retained_faces']),")]}, 'reverse Kato'),
    ('reverse', 'one-plaquette Kato radius 96 C_min', {'edits': [("        kato[name] = {'one_plaquette_radius': qs(48 * cmin[name]),",
                                                                  "        kato[name] = {'one_plaquette_radius': qs(96 * cmin[name]),")]},
     'reverse Kato'),
]


def uniqueness_clauses(report, template, exclusions):
    body = pre.normalize(report).replace(pre.normalize(template), ' ')
    cls = pre.clauses(body)
    out = []
    for cl in cls:
        if not re.search(r'unique', cl, re.I):
            continue
        low = cl.lower()
        if 'uniqueness_of_ground_state_claimed' in cl or 'uniqueness_field_true' in cl:
            kind = 'field or mutation identifier'
        elif cl.strip() in exclusions:
            kind = 'claim-exclusion list quoted verbatim'
        elif pre.NEGATION.search(cl) or 'exclusion' in low or 'excluded' in low:
            kind = 'negated or excluded'
        elif 'simplicity' in low or 'simple' in low:
            kind = 'read as simplicity of the finite-box ground eigenvalue'
        elif 'unique' in low and ('path' in low or 'column' in low or 'z_5' in low):
            kind = 'combinatorial (the single Z_5 column path)'
        else:
            kind = 'other'
        out.append({'clause': cl[:170], 'kind': kind})
    return out


def run(args):
    # 1. contract, pre-comparison package unchanged and replayed ------------------------------------------------------
    need(sha(CONTRACT) == CONTRACT_SHA, 'contract_sha256_pinned', sha256=CONTRACT_SHA)
    con = json.loads(CONTRACT.read_text())
    pf = json.loads(PRE_FREEZE.read_text())
    ok_pf = pf['contract_sha256'] == CONTRACT_SHA and pf['loop'] == 'BD1' and pf['stage'] == 'pre_comparison' \
        and all(sha(ROOT / p) == h for p, h in pf['files'].items())
    _, pre_bytes = replay(PRE_SCRIPT, pre_mode=True)
    need(ok_pf and pre_bytes == PRE_RESULTS.read_bytes(), 'pre_comparison_package_unchanged_and_replayed',
         freeze=pf['files'], note='the committed pre-comparison package (bf1f531, 06:10:08Z, after both BD1 producer commits '
                                  'a1010a4 and 5a792b0) is unchanged; bd1_check.py reproduces bd1-independent/results.json '
                                  'byte for byte in this interpreter mode')

    # 2. closures, inventories, replays, pinned artifacts, caches -----------------------------------------------------
    declared = sorted(set(['AGENTS.md', 'research/round33/contracts/bd1.json'] + con['shared_premises']))
    res, reports, closure_rows = {}, {}, {}
    for side in ('forward', 'reverse'):
        ok, inputs, snaps, freeze = verify_closure(side)
        need(ok and inputs == declared and snaps and inputs == sorted(pre.OBSERVED_INPUTS)
             and all(sha(DIRS[side] / 'inputs' / n) == pre.OBSERVED_INPUTS[n] for n in inputs),
             side + '_closure_and_inventory', closure_files=len(freeze['sources']), inputs=len(inputs),
             note='27 closure files verified one by one; 23 inputs equal the contract-derived list and the names-only '
                  'inventory recorded before production; every snapshot byte-identical to the repository')
        need(all(sha(DIRS[side] / p) == h for p, h in FROZEN[side].items()), side + '_frozen_artifacts_pinned', pinned=FROZEN[side])
        outs, _ = replay(DIRS[side] / 'check.py')
        frozen_out = {p: sha(DIRS[side] / 'output' / p) for p in ('results.json', 'source-manifest.json')}
        need(outs == frozen_out and frozen_out['results.json'] == FROZEN[side]['output/results.json'],
             side + '_replay_byte_identical', outputs=outs,
             note='the producer replay in this interpreter mode (-B, or -B -O when this program runs under -O) reproduces output/')
        res[side] = json.loads((DIRS[side] / 'output/results.json').read_text())
        reports[side] = (DIRS[side] / 'report.md').read_text()
        closure_rows[side] = len(freeze['sources'])
    need(caches() == [], 'no_interpreter_cache_in_either_closure', checked=[RELS['forward'] + '/', RELS['reverse'] + '/'])

    # 3. values against the independent recomputation ---------------------------------------------------------------------
    ref = reference()
    G = ref['g']
    for side in ('forward', 'reverse'):
        need(VALIDATORS[side](res[side], reports[side], ref, con) is True, side + '_values_equal_independent_recomputation',
             note='every exported moment, coefficient, series, obstruction cell, centre datum, Kato radius, box sum, flip-set '
                  'count, torus count, GF(2) existence value, BB2 constant and bound, ledger status, label and gate field '
                  'equals the own recomputation; nothing is read from either producer to compute a reference value')

    # 4. exact cross-route agreement ------------------------------------------------------------------------------------------
    fw, rv = res['forward'], res['reverse']
    cells = 0
    table = {}
    for g in GROUPS:
        R = G[g]
        rs_f = check_by_id(fw, 'rayleigh_schroedinger_one_plaquette')['series'][g]
        row = {}
        for k in range(1, 5):
            f_, r_ = rat(fw['cells'][g]['moments'][str(k)]), rat(rv['moment_table'][g]['E[W^%d]' % k]['value'])
            own = (pre.moments_characters(pre.group(g), k)[k - 1], pre.moments_weyl(g, k)[k - 1], pre.moments_third(g, k)[k - 1])
            if not (f_ == r_ == own[0] == own[1] == own[2]):
                raise ReviewFailure('cross-route moment disagreement %s k=%d' % (g, k))
            row['E[W^%d]' % k] = q_(f_)
            cells += 1
        pairs = [('c1', rat(fw['cells'][g]['first_order_coefficient']['value']), rat(rv['first_order_coefficients'][g]['value']), R['c1']),
                 ('d omega(W^2)/dtau', rat(fw['cells'][g]['first_order_derivative_omega_W2']['value']),
                  rat(rv['first_order_terms'][g]['d_omega_W2_dtau']['value']), R['dW2'])]
        pairs += [('omega_%d' % m, rat(rs_f['omega_W'][m]), rat(rv['one_plaquette_series'][g]['omega_W'][m]), R['omW'][m]) for m in range(5)]
        pairs += [('E_%d' % m, rat(rs_f['ground_energy'][m]), rat(rv['one_plaquette_series'][g]['energy'][m]), R['E'][m]) for m in range(6)]
        pairs += [('omega(W^2)_%d' % m, rat(rs_f['omega_W2'][m]), rat(rv['one_plaquette_series'][g]['omega_W2'][m]), R['omW2'][m]) for m in range(3)]
        for name, f_, r_, own in pairs:
            if not (f_ == r_ == own):
                raise ReviewFailure('cross-route disagreement %s %s' % (g, name))
            cells += 1
        row.update({'c1': q_(R['c1']), 'd omega(W^2)/dtau': q_(R['dW2']), 'omega_2': q_(R['omW'][2]), 'omega_4': q_(R['omW'][4])})
        table[g] = row
    su5_5 = rat(fw['cells']['SU(5)']['moments']['5']) == rat(rv['moment_table']['SU(5)']['E[W^5]']['value']) == G['SU(5)']['mom'][4]
    need(su5_5 and cells == 7 * (4 + 2 + 5 + 6 + 3), 'cross_route_exact_agreement', cells_compared=cells + 1, table=table,
         obstruction_values={g: {'E[W^3]': q_(G[g]['E3']), 'd omega(W^2)/dtau': q_(G[g]['dW2']), 'omega_2': q_(G[g]['omW'][2])}
                             for g in ('SU(3)', 'SO(3)')},
         su5_fourth_order={'exact': q_(G['SU(5)']['omW'][4]), 'factored': '1/(2^30 3^10)', 'preview': trunc(G['SU(5)']['omW'][4])},
         note='forward (characters), reverse (weyl_integration) and the three own routes (characters, Weyl constant terms on '
              'the SU(N) torus, Frobenius/hook and closed-form counts) agree exactly on every moment k=1..4 of the seven '
              'groups, every first-order coefficient and first-order derivative of omega(W^2), the one-plaquette series '
              'omega_0..omega_4, E_0..E_5 and omega(W^2)_0..2, and SU(5) E[W^5]; no cell is single-route')
    pr = json.loads(PRE_RESULTS.read_text())
    pd = pr['predictions']
    need(all(F(pd['first_order'][g]) == G[g]['c1'] for g in GROUPS)
         and all(F(pd[g][k]) == v for g in ('SU(3)', 'SO(3)') for k, v in
                 (('E[W^3]', G[g]['E3']), ('d omega(W^2)/dtau at 0', G[g]['dW2']), ('second_order_omega_W', G[g]['omW'][2])))
         and F(pd['SU(5)_fourth_order_omega_W']) == G['SU(5)']['omW'][4] and pd['flip_transfer'] == FLIP == fw['headline']['flip_transfer_groups']
         and pd['parity_transfer'] == PARITY == fw['headline']['parity_transfer_groups']
         and pr['flip_sets']['periodic_even_plaquettes']['E2_sides_3_4'] == ref['tori'][(3, 4)]['even'] == 0
         and pr['flip_sets']['periodic_even_plaquettes']['E2_sides_4_3'] == ref['tori'][(4, 3)]['even'] == 4,
         'pre_comparison_predictions_equal_exactly',
         equal=['seven first-order coefficients', 'SU(3) and SO(3) E[W^3], d omega(W^2)/dtau, omega_2', 'SU(5) omega_4',
                'flip and parity columns', 'box, factor and torus counts'],
         note='the frozen pre-comparison rationals equal both producers digit for digit')

    # 5. D1 (R1): tier and route labels of every exported value ---------------------------------------------------------------
    def label_table(entries):
        out = {}
        for kind, e in entries:
            key = (kind, e.get('tier', 'none'), e.get('route_of_computation'))
            out[key] = out.get(key, 0) + 1
        return [{'kind': k[0], 'tier': k[1], 'route_of_computation': k[2], 'entries': v} for k, v in sorted(out.items())]
    f_entries = [(e['kind'], e) for e in fw['value_entries']]
    r_entries = [('haar_moment', e) for g in GROUPS for e in rv['moment_table'][g].values()]
    r_entries += [('first_order_coefficient', rv['first_order_coefficients'][g]) for g in GROUPS]
    r_entries += [('first_order_derivative_omega_W2', rv['first_order_terms'][g]['d_omega_W2_dtau']) for g in GROUPS]
    r_entries += [('first_order_derivative_C_state', rv['first_order_terms'][g]['state_term_coefficient']) for g in GROUPS]
    r_entries += [('first_order_derivative_C_duhamel', rv['first_order_terms'][g]['duhamel_coefficient']) for g in GROUPS]
    r_entries += [('second_order_coefficient_omega_W', rv['obstruction_cells'][g]['omega_2_entry']) for g in ('SU(3)', 'SO(3)')]
    r_entries += [('first_order_derivative_omega_W2', rv['obstruction_cells'][g]['d_omega_W2_dtau_entry']) for g in ('SU(3)', 'SO(3)')]
    r_entries += [('fourth_order_coefficient_omega_W', rv['obstruction_cells']['SU(5)']['omega_4_entry'])]
    ft, rt_ = label_table(f_entries), label_table(r_entries)
    first = ('first_order_coefficient', 'first_order_derivative_omega_W2', 'first_order_derivative_C_state', 'first_order_derivative_C_duhamel')
    ok_labels = all((r['tier'] == TIER) == (r['kind'] in first) for r in ft + rt_) \
        and {r['route_of_computation'] for r in ft} == {'characters'} and {r['route_of_computation'] for r in rt_} == {'weyl_integration'}
    tier_rule = con['preregistration']['tier_label_rule']
    ctl = con['new_control_semantics']['tier_mixing_rejected']
    need(ok_labels and tier_rule.startswith('every group coefficient carries the tier exact_first_order')
         and 'a tier on a moment or on a higher-order coefficient' in ctl, 'reading_R1_tier_labels_both_producers',
         forward=ft, reverse=rt_,
         contract_texts={'preregistration.tier_label_rule': tier_rule[:120] + '...',
                         'new_control_semantics.tier_mixing_rejected (excerpt)': 'Haar moments and the second- and fourth-order '
                         'one-plaquette coefficients of the obstruction cells are exact finite-model rationals with a '
                         'route_of_computation and no tier; ... a tier on a moment or on a higher-order coefficient ... is rejected'},
         note='both producers put exact_first_order on every first-order coefficient and first-order derivative and no tier on '
              'moments or on second- and fourth-order coefficients, each with its own route label; neither packet is rejected by '
              'the control; the literal tier_label_rule ("every group coefficient carries the tier") conflicts with the control '
              'for higher-order coefficients: a contract defect, resolved by the more specific control (reading R1)')

    # 6. D2 (R2): the flip scope ---------------------------------------------------------------------------------------------------
    lit = con['preregistration']['gate_fields_required']['flip_transfer_scope']
    need(groups_named(lit) == [] and fw['gate_fields']['flip_transfer_scope'] == lit
         and groups_named(fw['gate_field_groups']['flip_transfer_scope_named']) == FLIP
         and groups_named(rv['gate_fields']['flip_transfer_scope']) == FLIP
         and groups_named(RECOMMENDED_SCOPE) == FLIP and 'central' in RECOMMENDED_SCOPE
         and 'names the groups found' in con['preregistration']['gate_fields_rule'], 'reading_R2_flip_scope_names_four_groups',
         frozen_description_names=groups_named(lit), forward_gate_field=('literal frozen description (names no group); the groups '
                                                                          'are in gate_field_groups.flip_transfer_scope_named'),
         forward_named=fw['gate_field_groups']['flip_transfer_scope_named'], reverse_gate_field=rv['gate_fields']['flip_transfer_scope'],
         reverse_extra_fields=sorted(set(rv['gate_fields']) - set(con['preregistration']['gate_fields_required'])),
         recommended_gate_text=RECOMMENDED_SCOPE,
         note='the gate must export flip_transfer_scope naming exactly SU(2), SU(4), U(1) and Z2 (gate_fields_rule: "names the '
              'groups found"); the frozen value is a description; the forward exports it literally (its validator requires the '
              'frozen dict at accepted) and names the groups beside it; the reverse names them in the field and adds two fields '
              'outside the contract list (obstructions, parity_transfer_scope), which belong in the accepted text')

    # 7. Kato radii, "unique" as simplicity, box sums over the 1344 faces ------------------------------------------------------------
    bs = ref['box_sums']
    kato = {g: {'one_plaquette': q_(G[g]['kato_fg']), 'box': {str(n): q_(v) for n, v in G[g]['box']['kato_box'].items()}} for g in GROUPS}
    need(bs['W_retained'] is True and bs['faces'] == 1344 and bs['max_shared_links'] == 1
         and all(ref['boxes'][n]['retained'] == 21 * (2 * n) ** 3 for n in (2, 3, 4))
         and all(G[g]['box']['c1_box'] == G[g]['c1'] and G[g]['box']['dW2_box'] == G[g]['dW2'] for g in GROUPS),
         'kato_radii_and_box_sums', kato=kato, faces_sharing_one_link_with_W=bs['sharing_one_link'],
         box_first_order={g: q_(G[g]['box']['c1_box']) for g in GROUPS},
         note='H_0 on the full box space has the simple vacuum and gap 8 C_min (one excited link; C_min = C_F for all seven '
              'groups); ||V_1|| <= F_N/3 with F_N = 21(2N)^3 retained faces (1344, 4536, 10752 by own enumeration); the '
              'Riesz projection on |z| = 4 C_F is analytic and of rank one for |tau| F_N/3 < 4 C_F, i.e. |tau| < 12 C_F/F_N, '
              'so the ground eigenvalue is simple and lowest (spectrum moves by at most |tau| ||V_1||); the one-plaquette radius '
              'is 48 C_F; "unique" in contract items 1 and 6 is simplicity of the finite-box ground eigenvalue, not the excluded '
              'uniqueness of any ground state; with W the retained xz face at the origin every other retained face shares at '
              'most one link with W (own enumeration), so the N=2 sums over the 1344 faces reduce to f=W and the box first-order '
              'coefficients and d omega(W^2)/dtau equal the one-plaquette values')
    unq = {side: uniqueness_clauses(reports[side], con['preregistration']['mandatory_sentence_template'], con['claim_exclusions'])
           for side in ('forward', 'reverse')}
    need(all(u['kind'] != 'other' for v in unq.values() for u in v), 'uniqueness_wording_classified', clauses=unq,
         note='every clause mentioning uniqueness in either report is negated or excluded, a field or mutation identifier, or '
              'the contract claim-exclusion item quoted verbatim; no clause asserts uniqueness of any ground state')

    # 8. tori and GF(2) --------------------------------------------------------------------------------------------------------------
    T = ref['tori']
    need(T[(3, 4)]['even'] == 0 and T[(4, 3)]['even'] == 4 and T[(4, 4, 4)]['even'] == 0 and T[(3, 4, 4)]['even'] == 16
         and T[(3, 4)]['gf2'] is True and T[(3, 3)]['gf2'] is False and T[(3, 4, 4)]['gf2'] is True and T[(3, 3, 4)]['gf2'] is False,
         'periodic_tori_reading', tori={'x'.join(map(str, s)): v for s, v in T.items()},
         note='E_3 and E_2 fail at the seam exactly when the keyed coordinate has an odd side; E_2 on the 3x4 torus (odd x side, '
              'even y side) meets every plaquette once, so it is a valid flip set there; own GF(2) elimination: some flip set '
              'exists iff every coordinate plane has an even plaquette count (2D: L_x L_y even; 3D: at most one odd side); the '
              'contract "obstruction" is a statement about E_3/E_2 at the seam, and "not statements for periodic boxes with an '
              'odd side" is a scope exclusion, not a proof that the flip lemma fails there')

    # 9. area parity through BB2 at each sign --------------------------------------------------------------------------------------
    ap = check_by_id(fw, 'area_parity_box_and_limit')
    own_loops = next(c for c in pr['checks'] if c['id'] == 'area_parity_rule_enumerated')
    need(ref['bb2']['csite'] == F(2, 984375) and ref['bb2']['q'] == F(1, 64) and own_loops['planar_loops'] == 216
         and 'both sequences' in ap['limit_passage']
         and 'along the whole sequence at each sign' in check_by_id(rv, 'area_parity_box_and_limit')['limit_statement'],
         'area_parity_limit_through_bb2', bb2={"c'_site": q_(ref['bb2']['csite']), 'q': q_(ref['bb2']['q'])},
         forward_read=ap['bb2_constants_read'], w_face_region={'|Y|': ref['w_region']['Y'], 'max |y|_inf': ref['w_region']['m']},
         own_planar_loops=own_loops['planar_loops'], reverse_rectangles=check_by_id(rv, 'area_parity_surface_parity')['rectangles_tested'],
         note='for each N and each sign, rho^{F1,N}_Y(-tau) = U_{E cap Y} rho^{F1,N}_Y(tau) U_{E cap Y}^* (AW1, U_E a product over '
              'links); BB2 item 1 bounds ||rho^{F,M}_Y - rho^{F,N}_Y||_1 by c\'_site |Y| e^{|Y|/10^8} q^{d_Y} along the whole '
              'sequence at both signs; conjugation is trace-norm continuous, so the identity passes to the limit pointwise; the '
              'forward read c\'_site = 2/984375 and q = 1/64 from the gate (not the labelled union value 1/500000)')

    # 10. the SU(3) torus trap ---------------------------------------------------------------------------------------------------------
    rcode = (DIRS['reverse'] / 'check.py').read_text()
    fcode = (DIRS['forward'] / 'check.py').read_text()
    tr = ref['trap']
    need(tr['SU(3)'][2] == 0 != rat(rv['moment_table']['SU(3)']['E[W^3]']['value']) and tr['SU(4)'][3] == F(3, 1024)
         and rat(rv['moment_table']['SU(4)']['E[W^4]']['value']) == F(7, 2048) and tr['SU(5)'][4] == 0
         and '"""SU(N) maximal torus: x_1..x_N with x_1...x_N=1; exponents taken modulo the diagonal."""' in rcode
         and "        m = min(e)" in rcode and WEYL_KEY in fcode, 'su3_torus_trap_avoided',
         unitary_torus_values={g: [q_(x) for x in v[:5]] for g, v in tr.items()},
         reverse_values={'SU(3) E[W^3]': rv['moment_table']['SU(3)']['E[W^3]']['value'],
                         'SU(4) E[W^4]': rv['moment_table']['SU(4)']['E[W^4]']['value']},
         note='the reverse reduces exponents modulo the diagonal (the SU(N) torus, x_1...x_N = 1), so z^{c(1,...,1)} counts as '
              'the trivial character; the U(N) torus would give SU(3) E[W^3] = 0 and SU(4) E[W^4] = 3/1024; the forward-internal '
              'labelled Weyl cross-check reduces the same way; both substitutions are exercised below and abort')

    # 11. text: phrase tool, template, previews -----------------------------------------------------------------------------------------
    need(sha(PHRASE_TOOL) == PHRASE_TOOL_SHA, 'phrase_tool_pinned')
    tool = {}
    for side in ('forward', 'reverse'):
        done = subprocess.run([sys.executable, '-B', str(PHRASE_TOOL), str(CONTRACT), str(DIRS[side] / 'report.md')],
                              capture_output=True, text=True, cwd=str(ROOT))
        tool[side] = (done.returncode, list(json.loads(done.stdout).values()))
    tpl = con['preregistration']['mandatory_sentence_template']
    forbidden = pre.ROUND_FORBIDDEN + con['preregistration']['forbidden_phrasings']
    need(all(v == (0, [[]]) for v in tool.values())
         and all(pre.affirmative_hits(reports[s], forbidden, tpl) == [] and reports[s].count(tpl) == 1 for s in reports),
         'phrase_scan_and_template_both_reports', tool_exit={s: v[0] for s, v in tool.items()}, template_spans=1)
    prev = {side: report_previews(side, reports[side], ref) for side in ('forward', 'reverse')}
    need(prev['forward'][1] == [] and prev['reverse'][1] == KNOWN_REPORT_PREVIEW_DEFECTS
         and rv['obstruction_cells']['SU(5)']['omega_4_preview'] == '1.57720295790e-14', 'report_previews_checked',
         forward_rows=len(prev['forward'][0]), reverse_rows=len(prev['reverse'][0]),
         reverse_report_defect={'exact': '1/63403380965376', 'printed_preview': '1.57720727258e-14',
                                'correct_preview_truncated': trunc(G['SU(5)']['omW'][4]), 'results_json_preview': '1.57720295790e-14'},
         note='every exact value printed next to a decimal in either report is recomputed; all forward previews and all but '
              'one reverse preview are within one unit of their last digit; the reverse report prints 1.57720727258e-14 for '
              'omega_4 (section 7.3), while its results.json carries the correct 1.57720295790e-14: a non-blocking text defect')

    # 12. damaged packets rejected -------------------------------------------------------------------------------------------------------
    def damaged(side, fn):
        pk = json.loads(json.dumps(res[side]))
        fn(pk)
        try:
            VALIDATORS[side](pk, reports[side], ref, con)
        except Rejected as exc:
            return str(exc)
        return None

    def setp(path, value):
        def fn(pk):
            node = pk
            for key in path[:-1]:
                node = check_by_id(pk, key[6:]) if isinstance(key, str) and key.startswith('check:') else node[key]
            node[path[-1]] = value(node[path[-1]]) if callable(value) else value
        return fn
    tpl_cut = tpl.replace(' not uniqueness of any ground state,', '')
    dmg = [
        ('forward', 'SU(3) E[W^3] zeroed in its cell', setp(['cells', 'SU(3)', 'moments', '3'], '0'), 'forward moments SU(3)'),
        ('forward', 'U(1) coefficient replaced by the SU(2) value', setp(['headline', 'first_order_coefficients', 'U(1)'], '1/144'),
         'forward headline first-order'),
        ('forward', 'SO(3) second-order coefficient under a tier', setp(['cells', 'SO(3)', 'second_order_coefficient_omega_W', 'tier'], TIER),
         'tier on a moment or a higher-order coefficient'),
        ('forward', 'Z2 first-order coefficient without its tier', lambda pk: pk['cells']['Z2']['first_order_coefficient'].pop('tier'),
         'first-order value without exact_first_order'),
        ('forward', 'SU(3) added to the flip groups', setp(['headline', 'flip_transfer_groups'], FLIP + ['SU(3)']), 'forward classification'),
        ('forward', 'Z2 dropped from the named flip scope', setp(['gate_field_groups', 'flip_transfer_scope_named'],
                                                                 'SU(2), SU(4), U(1) on H_FG(G) and H^G_N'), 'forward flip scope groups'),
        ('forward', 'E_2 on the 3x4 torus recorded with 3 even plaquettes', setp(['headline', 'flip_set_counts', 'tori_E2_even_seam', '3x4'], 3),
         'forward tori'),
        ('forward', "BB2 c'_site read as 1/500000", setp(['check:area_parity_box_and_limit', 'bb2_constants_read', "c'_site"], '1/500000'),
         'forward BB2 constants'),
        ('forward', 'box Kato radius at N=2 doubled', setp(['check:criterion_B_box_models', 'kato_radius_sufficient', 'SU(3)', 'box', '2'], '1/42'),
         'forward Kato SU(3)'),
        ('forward', 'uniqueness flag true', setp(['uniqueness_of_ground_state_claimed'], True), 'forward claim flag'),
        ('forward', 'template trimmed in the supported statement', setp(['supported_statement'], tpl_cut), 'forward supported statement'),
        ('forward', 'SU(5) fourth order zeroed', setp(['cells', 'SU(5)', 'fourth_order_coefficient_omega_W', 'value'], '0'), 'forward omega_4 SU(5)'),
        ('forward', 'SU(4) omega_3 altered in the RS series',
         setp(['check:rayleigh_schroedinger_one_plaquette', 'series', 'SU(4)', 'omega_W', 3], '41/143327232001'), 'forward RS series SU(4)'),
        ('forward', 'U(1) box mean sum zeroed', setp(['check:criterion_B_box_models', 'box_terms', 'U(1)', 'mean_sum_E[W W_f]'], '0'),
         'forward box terms U(1)'),
        ('reverse', 'SU(3) moments from the U(N) torus', setp(['moment_table', 'SU(3)', 'E[W^3]', 'value'], q_(ref['trap']['SU(3)'][2])),
         'value differs: reverse moment SU(3) k=3'),
        ('reverse', 'SU(5) omega_4 preview as printed in the report', setp(['obstruction_cells', 'SU(5)', 'omega_4_preview'], '1.57720727258e-14'),
         'reverse SU(5) cell'),
        ('reverse', 'SO(3) omega_2 entry under a tier', setp(['obstruction_cells', 'SO(3)', 'omega_2_entry', 'tier'], TIER),
         'tier on a moment or a higher-order coefficient'),
        ('reverse', 'flip scope without Z2', setp(['gate_fields', 'flip_transfer_scope'], 'SU(2), SU(4) and U(1) (central -I, -I, e^{i pi})'),
         'reverse flip scope groups'),
        ('reverse', 'GF(2) existence on 3x3x4 set true', setp(['flip_sets', 'tori', 'E_3 on 3x3x4', 'any_flip_set_exists_gf2'], True),
         'reverse tori E_3 on 3x3x4'),
        ('reverse', 'Kato radius of SU(3) at N=2 doubled', setp(['kato_radii', 'SU(3)', 'box_radius_N2'], '1/42'), 'reverse Kato SU(3)'),
        ('reverse', 'SU(5) omega_4 zeroed', setp(['obstruction_cells', 'SU(5)', 'omega_4'], '0'), 'reverse SU(5) cell'),
        ('reverse', 'SO(3) given a central -1', setp(['centre', 'SO(3)', 'central_minus_one'], True), 'reverse centre SO(3)'),
        ('reverse', 'SU(4) coefficient replaced by the SU(2) value', setp(['first_order_coefficients', 'SU(4)', 'value'], '1/144'),
         'value differs: reverse c1 SU(4)'),
        ('reverse', 'area fixture 3x1 sign not flipped', setp(['area_parity', 'fixture', '3x1', 'W_flipped'], '-45274/238875'),
         'reverse area fixture'),
        ('reverse', 'continuum flag true', setp(['continuum_claim'], True), 'reverse claim flag continuum_claim'),
        ('reverse', 'template altered in the results', setp(['mandatory_sentence'], tpl_cut), 'reverse template in the results'),
        ('reverse', 'SU(3) cubic moment E[chi^3] zeroed', setp(['cubic_moments', 'SU(3)', 'E[chi^3 conj(chi)^0]'], 0), 'reverse cubic moments SU(3)'),
    ]
    rows_d = []
    for side, label, fn, reason in dmg:
        got = damaged(side, fn)
        if got is None or reason not in got:
            raise ReviewFailure('damaged packet accepted or rejected for another reason: %s %s (%s)' % (side, label, got))
        rows_d.append({'producer': side, 'mutation': label, 'rejected_for': reason})
    need(len(rows_d) == len(dmg), 'damaged_packets_rejected_by_review_validators', rows=rows_d)

    # 13. source-edit runs --------------------------------------------------------------------------------------------------------------------
    for table in (WEAK_F, WEAK_R):
        if sorted(w[0] for w in table) != sorted(con['controls']):
            raise ReviewFailure('weakening table does not cover the 22 controls')
    fsets = {c['id']: c.get('mutations_rejected', []) for c in fw['checks']}
    for cid, _, label in WEAK_F:
        if label not in fsets.get(cid, []):
            raise ReviewFailure('expected label is not a forward mutation of the control: %s %s' % (cid, label))
    frozen_bytes = {s: {p.name: p.read_bytes() for p in sorted((DIRS[s] / 'output').glob('*.json'))} for s in DIRS}
    base_rows = []
    for side in ('forward', 'reverse'):
        base = mutated_run(side)
        nob = mutated_run(side, no_b=True)
        if not (base[0] == 0 and base[2] == frozen_bytes[side] and base[5] == [] and nob[0] == 0 and nob[2] == frozen_bytes[side]
                and nob[5] == []):
            raise ReviewFailure('unmutated copy or run without -B differs: ' + side)
        base_rows += [{'producer': side, 'run': 'unmutated copy'}, {'producer': side, 'run': 'without -B and PYTHONDONTWRITEBYTECODE'}]
    need(len(base_rows) == 4, 'unmutated_copies_and_runs_without_B', rows=base_rows,
         note='an unmutated copy of each producer outside the checkout reproduces its frozen output byte for byte; a run without '
              '-B reproduces it too and writes no __pycache__ or .pyc anywhere in the copy')
    jobs = [('forward', w) for w in WEAK_F] + [('reverse', w) for w in WEAK_R]
    outs = parallel(lambda j: mutated_run(j[0], edits=j[1][1]), jobs)
    weak_rows = []
    for (side, (cid, _, label)), (rc, _, o, _, last, cache, ctl) in zip(jobs, outs):
        if side == 'forward':
            expect_msg = 'damaging mutation accepted: ' + label
            ok = rc != 0 and not o and not cache and last.endswith(expect_msg)
        else:
            expect_msg = 'damaging mutation accepted by ' + label
            ok = rc != 0 and not o and not cache and last.endswith(expect_msg) and ctl == cid
        if not ok:
            raise ReviewFailure('weakening of %s (%s) not exposed as expected: %s / %s' % (cid, side, last[-200:], ctl))
        weak_rows.append({'producer': side, 'control': cid, 'aborted_with': expect_msg})
    need(len(weak_rows) == 44, 'control_validator_weakenings_both_producers', runs=len(weak_rows), rows=weak_rows,
         note='one validator weakened per contract control and producer on a temporary copy ("True or " inserted into the '
              'require that rejects a labelled mutation, or the float branch returning a Fraction); each forward run aborts '
              'naming a mutation of that control; each reverse run aborts naming the validator, inside the control(...) call of '
              'that control (read from the traceback)')
    ab_out = parallel(lambda t: mutated_run(t[0], **t[2]), MUST_ABORT)
    ab_rows = []
    for (side, label, _, frag), (rc, _, o, _, last, cache, _) in zip(MUST_ABORT, ab_out):
        if rc == 0 or o or frag not in last or cache:
            raise ReviewFailure('edit ran or aborted elsewhere: %s %s: %s' % (side, label, last[-200:]))
        ab_rows.append({'producer': side, 'edit': label, 'aborted_with': last[-160:]})
    need(len(ab_rows) == len(MUST_ABORT), 'must_abort_substitutions', runs=len(ab_rows), rows=ab_rows,
         note='the U(N) torus in either route, a zeroed SU(3) third moment in the characters route, other normalizations, an '
              'E_3 without its x-links, a perturbed SU(5) closed form, edited premise snapshots, an undeclared input and report '
              'edits all abort without output')
    sil_out = parallel(lambda t: mutated_run(t[0], **t[2]), SILENT)
    silent_rows = []
    for (side, label, _, expect_reason), (rc, out_res, _, out_report, last, cache, _) in zip(SILENT, sil_out):
        if rc != 0 or out_res is None or cache:
            raise ReviewFailure('silent edit aborted: %s %s: %s' % (side, label, last))
        try:
            VALIDATORS[side](out_res, out_report, ref, con)
        except Rejected as exc:
            if expect_reason is None or expect_reason not in str(exc):
                raise ReviewFailure('silent edit rejected for the wrong reason: %s: %s' % (label, exc))
            silent_rows.append({'producer': side, 'edit': label, 'producer_run': 'completed', 'review_validator': 'rejected: ' + expect_reason})
            continue
        if expect_reason is not None:
            raise ReviewFailure('silent edit not caught by the review validator: ' + label)
        silent_rows.append({'producer': side, 'edit': label, 'producer_run': 'completed',
                            'review_validator': 'accepted (non-damaging: every exported admitted value unchanged)'})
    need(len(silent_rows) == len(SILENT), 'silent_edits_accounted', rows=silent_rows)
    need(caches() == [], 'no_interpreter_cache_after_all_runs', checked=[RELS['forward'] + '/', RELS['reverse'] + '/'])

    n_runs = len(base_rows) + len(weak_rows) + len(ab_rows) + len(silent_rows)
    return {
        'loop': 'BD1', 'stage': 'post_comparison', 'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'skeptic (model agent, correlated ancestry; not human review)',
        'contract_sha256': CONTRACT_SHA, 'producers': ['forward (characters)', 'reverse (weyl_integration)'],
        'commit_order_utc': [{'commit': 'a1010a4', 'time': '05:53:54', 'what': 'BD1 reverse producer'},
                             {'commit': '5a792b0', 'time': '05:54:17', 'what': 'BD1 forward producer'},
                             {'commit': '37fa623', 'time': '06:00:06', 'what': 'BD2 forward producer'},
                             {'commit': 'bf1f531', 'time': '06:10:08', 'what': 'skeptic BD1 and BD2 pre-comparison packages'}],
        'source_edit_runs': n_runs,
        'source_edit_breakdown': {'unmutated_and_no_B': len(base_rows), 'control_validator_weakenings': len(weak_rows),
                                  'must_abort_substitutions': len(ab_rows), 'silent_edits': len(silent_rows)},
        'damaged_packets': len(rows_d),
        'checks': CHECKS,
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
    result = run(args)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True, default=str) + '\n')
    print(json.dumps({'checks': len(result['checks']), 'source_edit_runs': result['source_edit_runs'],
                      'damaged_packets': result['damaged_packets']}))


if __name__ == '__main__':
    main()
