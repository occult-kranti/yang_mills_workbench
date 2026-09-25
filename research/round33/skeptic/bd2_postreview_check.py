#!/usr/bin/env python3
"""BD2 post-comparison skeptic checks (single+skeptic loop: the forward producer only).

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated ancestry (same model family as the advisor,
the lenses and the producer; the frozen BD2 texts carry the pre-freeze review's edits); not human peer review or formal
verification.

Commit order as it happened (UTC, git): BD1 reverse a1010a4 05:53:54; BD1 forward 5a792b0 05:54:17; BD2 forward 37fa623
06:00:06; the skeptic's pre-comparison packages bf1f531 06:10:08. Every BD2 value of the skeptic package was final at
05:55:31 (before the BD2 forward commit); the only earlier exposure was the names and hashes of the producer's inputs/.

Adds to the frozen pre-comparison package (bd2_check.py):
  * integrity: the contract hash; the unchanged pre-comparison package and a byte replay of bd2_check.py (its values are
    the reference); the forward freeze closure file by file (39 files); the inventory on the real snapshots (35 files, equal
    to the contract-derived list and to the names-only inventory recorded before production); a replay of the producer
    reproducing output/ byte for byte; the frozen artifacts pinned; no interpreter cache in the closure or under
    research/round11 and research/round32;
  * item 1: the producer's coefficient tables (every (m,n) with m+n <= 4, zeros included) against the skeptic tables, and
    the face-1 / face-2 flip parities on the full two-variable table;
  * item 2: the producer's Eckart/tail-comparison angle lemma re-evaluated in the skeptic's own orthogonal basis with the
    skeptic's own Ritz vectors (Temple, the Round11 Schur-complement comparison H >= B (+) R Q_D, Eckart, Davis-Kahan, the
    observable step), at D=6,8 and |l| = 1/10, 1/100, 1/1000; every exported angle, residual and ledger item compared; the
    skeptic's tail-comparison enclosures lie inside the producer's; the target and its margin;
  * item 3: the frozen rectangle, the face counts 82/72/33/16/10/49, the first-order zero, K_2' re-derived from the AY1
    items, the bound rows (F1, F2, the limit, both signs), evenness scope (F1 and the limit only), the formal 7/124416;
  * item 4: the band endpoints (3/2)L^2 and 98|tau| at both signs for F1, F2 and the limit, L equal to the AY2 lower end,
    the per-link formal counts n_e on the 48 links of R;
  * item 5: the 2+1D numerators, G_3, G_3', the directed e^{3/32} enclosure, the cap and the exclusion condition;
  * text: the round phrase tool on the report, the template once, the report's printed numbers against exact values,
    the producer's W1-W7 wording defects, code provenance (AZ2 algebra copied with attribution; the Round11 solver read as
    text only, never imported);
  * damaged producer packets rejected by this review's validator;
  * source-edit runs on temporary copies outside the checkout: one validator weakening per control (21), must-abort edits,
    silent edits (harmless, and damaging ones caught only by this review's validator), an unmutated copy and a run
    without -B.

Standard library only; exact Fractions decide every Boolean; failures are explicit exceptions (never assert), so the output
bytes match under python -O.

Usage: python3 -B research/round33/skeptic/bd2_postreview_check.py --output /abs/fresh/dir
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
import bd2_check as pre  # noqa: E402  (the skeptic's own frozen pre-comparison module)

ROOT = HERE.parents[2]
R33 = ROOT / 'research/round33'
CONTRACT = R33 / 'contracts/bd2.json'
CONTRACT_SHA = '783cad8054a9b7ed3f741e0c06fffd94cfa0d6fda0dcbb7aa0b464058e46f41e'
FWD = R33 / 'forward/bd2'
FWD_REL = 'research/round33/forward/bd2'
PRE_SCRIPT = HERE / 'bd2_check.py'
PRE_RESULTS = HERE / 'bd2-independent/results.json'
PRE_FREEZE = HERE / 'bd2-independent-freeze.json'
PHRASE_TOOL = R33 / 'tools/phrase_scan.py'
PHRASE_TOOL_SHA = '1c31a4958c4a44144c5d4f256db551385d216b86309eadc54a608c5e2a4ff0e2'
FROZEN = {  # frozen producer artifacts (sha256 at review time; commit 37fa623)
    'check.py': 'c0ed5a1687c574350af55f4c70f1b2ff47b88e6a3020eb13ed25c2bcb122c011',
    'report.md': '0f24f60673ffc5a904c61b7c9fe4fa65d4d788204d85d522d8682ed9a43a7733',
    'freeze.json': '1fa53dc0a799cc36337115504888e1b6f622e1f0c6614eece9ffbe20d6c80a9d',
    'output/results.json': '4e6aa2538c2211351439e956d38e5ae1600120e4dfcaead158b47e8bd86fcacd',
    'output/source-manifest.json': '91a80bd46db96a1578ff6357b1375e298f5bbf8474e985b3e651d0341b09905e',
}
TAU = F(1, 10 ** 8)
LS = [F(1, 10), F(1, 100), F(1, 1000)]
CUTOFFS = (6, 8)
TARGET = F(1, 10 ** 16)
SUB_LABELS = ['sign_certified_finite_graph', 'transfer_to_named_model', 'obstruction_recorded', 'static_not_dynamic']
OBLIGATION_IDS = ['area_law', 'certified_sign_of_the_Z3_1x2_loop', 'tight_electric_energy_enclosure',
                  'site_blocked_uniform_3p1_regime', 'finite_volume_theorem_2p1']
LINKS = ['h1', 'vL', 'h3', 'vM', 'h2', 'vR', 'h4']


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


def trunc(x, digits=12):
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


def within_ulp(s, x):
    return abs(dec(s) - F(x)) < ulp(s)


def is_truncation(s, x):
    d = dec(s)
    return d <= F(x) < d + ulp(s)


def close(a, b, rel):
    a, b = F(a), F(b)
    return abs(a - b) <= rel * max(abs(a), abs(b))


def check_by_id(res, cid):
    for c in res['checks']:
        if c['id'] == cid:
            return c
    raise Rejected('producer check missing: ' + cid)


# ------------------------------------------------------------ the skeptic's own values (nothing from the producer)
class Graph:
    """The skeptic's orthogonal spin-network basis and multiplication tables (bd2_check.py construction)."""

    def __init__(self):
        self.S = pre.build_basis(9)
        self.NORM = {m: pre.ip_mono(self.S[m], {m: F(1)}) for m in self.S}
        self.TAB = {v: {m: pre.decompose({pre.add(k, pre.SHIFT[v]): c for k, c in self.S[m].items()}, self.S)
                        for m in pre.monos(8)} for v in 'xyz'}
        self.shell_min = {d: min(pre.lam_K(m) for m in pre.monos(d) if pre.deg(m) == d) for d in range(1, 11)}

    def mul(self, v, vec, D):
        out = {}
        for k, val in vec.items():
            for k2, c in self.TAB[v][k].items():
                if pre.deg(k2) <= D:
                    out[k2] = out.get(k2, 0) + c * val
        return {k: w for k, w in out.items() if w != 0}

    def lower_adjoint(self, v, u, D):
        """P_D (v-multiplication) u for u supported on degree D+1, through self-adjointness c(k->m)N(m) = c(m->k)N(k)."""
        out = {}
        for k in pre.monos(D):
            tot = F(0)
            for m, c in self.TAB[v][k].items():
                if m in u:
                    tot += c * self.NORM[m] / self.NORM[k] * u[m]
            if tot:
                out[k] = tot
        return out

    def ipv(self, u, v):
        return sum((c * v[k] * self.NORM[k] for k, c in u.items() if k in v), F(0))

    def ritz(self, l, D):
        Z0 = (0, 0, 0)
        phi, scale = {Z0: F(1)}, 10 ** 130
        for _ in range(600):
            vphi = {}
            for v in 'xy':
                for k, w in self.mul(v, phi, D).items():
                    vphi[k] = vphi.get(k, 0) - l * w
            mu = vphi.get(Z0, F(0))
            new = {Z0: F(1)}
            for k in sorted(set(phi) | set(vphi)):
                if k != Z0:
                    val = (mu * phi.get(k, F(0)) - vphi.get(k, F(0))) / pre.lam_K(k)
                    val = F(round(val * scale), scale)
                    if val:
                        new[k] = val
            diff = max(abs(new.get(k, 0) - phi.get(k, 0)) for k in set(new) | set(phi))
            phi = new
            if diff < F(1, 10 ** 120):
                return phi
        raise ReviewFailure('Ritz iteration did not converge')

    def producer_lemma(self, l, D):
        """The producer's angle lemma evaluated with the skeptic's Ritz vector and basis."""
        phi = self.ritz(l, D)
        N = self.ipv(phi, phi)
        xp, yp = self.mul('x', phi, D + 1), self.mul('y', phi, D + 1)
        t = {k: xp.get(k, 0) + yp.get(k, 0) for k in set(xp) | set(yp)}
        t = {k: v for k, v in t.items() if v != 0}
        H = {k: pre.lam_K(k) * v for k, v in phi.items() if pre.lam_K(k)}
        for k, v in t.items():
            H[k] = H.get(k, 0) - l * v
        mu = self.ipv(phi, H) / N
        r = {k: H.get(k, 0) - mu * phi.get(k, 0) for k in set(H) | set(phi)}
        rho2 = self.ipv(r, r) / N
        Qt = {k: v for k, v in t.items() if pre.deg(k) > D}
        rhoQ2 = l * l * self.ipv(Qt, Qt) / N
        b = self.shell_min[1] - 2 * abs(l)
        tail_t = self.shell_min[D + 1] - 2 * abs(l)
        R = b
        beta0 = mu - rhoQ2 / (tail_t - R)
        cx, cy = self.lower_adjoint('x', Qt, D), self.lower_adjoint('y', Qt, D)
        CC = {k: l * l * (cx.get(k, 0) + cy.get(k, 0)) for k in set(cx) | set(cy)}
        rP = {k: pre.lam_K(k) * phi.get(k, 0) - mu * phi.get(k, 0) - l * t.get(k, 0)
              for k in set(phi) | set(t) if pre.deg(k) <= D}
        resid = {k: rP.get(k, 0) - (CC.get(k, 0) - rhoQ2 * phi.get(k, 0)) / (tail_t - R) for k in set(rP) | set(CC) | set(phi)}
        eta2 = self.ipv(resid, resid) / N
        bB = b - 4 * l * l / (tail_t - R)
        if not (mu < b and beta0 < bB):
            raise ReviewFailure('separations in the producer lemma')
        E0_temple = mu - rho2 / (b - mu)
        E0_r11 = beta0 - eta2 / (bB - beta0)
        E0_low = max(E0_temple, E0_r11)
        sA = pre.sqrt_hi(rho2) / (b - mu)
        sB = pre.sqrt_hi((mu - E0_low) / (b - mu))
        s = min(sA, sB)
        q = self.ipv(phi, self.mul('z', phi, D + 1)) / N
        wR = self.ipv(phi, xp) / N
        delta = 2 * s + 2 * s * s
        return {'mu': mu, 'rho2': rho2, 'rhoQ2': rhoQ2, 'b': b, 'tail_t': tail_t, 'eta2': eta2, 'E0_low': E0_low,
                'E0_temple': E0_temple, 'E0_r11': E0_r11, 'sA': sA, 'sB': sB, 's': s, 'q': q, 'wR': wR,
                'lo': q - delta, 'hi': q + delta, 'rel': 2 * delta / (q - delta), 'eckart_below_temple': E0_r11 > E0_temple}


def z3_geometry():
    """Own counts on the cover R={0,e_z}: omitted faces meeting R, inside R, containing R, per site; n_e per link of R."""
    R = pre.R_COVER
    anchors = sorted(b for b in product(range(-2, 3), repeat=3) if any(pre.add(b, s_) in R for s_ in pre.S_STAR))
    faces_R = []
    for b in anchors:
        for r_, s_, a, c in product(range(4), range(2), 'xyz', 'xyz'):
            if (a, c) not in pre.ORIENT:
                continue
            p = (4 * b[0] + r_, 2 * b[1] + s_, b[2])
            if not pre.is_selected(p, a, c) and pre.owner_set(p, a, c) & set(R):
                faces_R.append((p, a, c))
    inside = [f for f in faces_R if pre.owner_set(*f) == frozenset(R)]
    containing = [f for f in faces_R if pre.owner_set(*f) >= frozenset(R)]
    site0 = [f for f in faces_R if R[0] in pre.owner_set(*f)]
    n_e = {}
    for b in R:
        for r_, s_, d in product(range(4), range(2), 'xyz'):
            p = (4 * b[0] + r_, 2 * b[1] + s_, b[2])
            cnt = 0
            for a, c in pre.ORIENT:
                if d not in (a, c):
                    continue
                other = c if d == a else a
                for base in (p, pre.add(p, tuple(-x for x in pre.DIRS[other]))):
                    if (p, d) in pre.face_links(base, a, c) and not pre.is_selected(base, a, c):
                        cnt += 1
            n_e['%d,%d,%d,%s' % (p[0], p[1], p[2], d)] = cnt
    f1, f2 = ((0, 0, 0), 'x', 'z'), ((1, 0, 0), 'x', 'z')
    rect = pre.loop_links([f1, f2])
    return {'anchors': len(anchors), 'meeting': len(faces_R), 'inside': len(inside), 'containing': len(containing),
            'per_site': len(site0), 'per_site_without_other': len(site0) - len(containing), 'straddling': len(faces_R) - len(inside),
            'n_e': n_e, 'rect': sorted([list(p) + [d] for p, d in rect]), 'rect_E3': sum(1 for l in rect if pre.in_E3(l)),
            'f1_E3': sum(1 for l in pre.face_links(*f1) if pre.in_E3(l)), 'R_links': len(n_e)}


def reference(pr):
    """Own values: the replayed pre-comparison results plus the own evaluations added in this review."""
    ref = {'pre': pr}
    G = Graph()
    ref['lemma'] = {(D, l): G.producer_lemma(l, D) for D in CUTOFFS for l in LS}
    ref['tail_lower'] = {D: G.shell_min[D + 1] for D in CUTOFFS}
    ref['geo'] = z3_geometry()
    # K_2' from the AY1 items with the own counts 82, 72, 33
    g = ref['geo']
    a_ = TAU / 144
    Jt = 28 * TAU
    T_ = 49 * a_ / (1 - 352 * Jt)
    rho_ = 352 * Jt * T_
    epsR = g['meeting'] * a_ + 2 * rho_ + (g['per_site_without_other'] * a_ + rho_) ** 2
    items = {'am2_remainder_4rho': 4 * rho_, 'straddling_2T(72a+2rho)': 2 * T_ * (g['straddling'] * a_ + 2 * rho_),
             'two_creation_2(33a+rho)^2': 2 * (g['per_site_without_other'] * a_ + rho_) ** 2, 'density_2epsR^2': 2 * epsR ** 2,
             'normalization_20a_epsR^2': 20 * a_ * epsR ** 2}
    ref['K2_items'] = {k: v / TAU ** 2 for k, v in items.items()}
    ref['K2p'] = sum(ref['K2_items'].values(), F(0))
    ref['bound'] = ref['K2p'] * TAU ** 2
    ay2 = json.loads((ROOT / 'research/round32/advisor/ay2-gate.json').read_text())['accepted']
    m10 = re.search(r'sqrt\(10\) in \[(\d+/\d+), (\d+/\d+)\]', ay2)
    ref['L'] = F(m10.group(1)) * TAU / 72 - ref['K2p'] * TAU ** 2
    ref['band'] = (F(3, 2) * ref['L'] ** 2, 98 * TAU)
    ref['formal'] = F(7, 124416)
    ref['formal_band'] = sum(ref['geo']['n_e'].values()) * F(1, 3456)
    e_lo, e_hi = pre.exp_bracket(F(3, 32))
    ref['e'] = (e_lo, e_hi)
    ref['numerators'] = [2 ** 3 * 6 ** k * (1 + F(4 * k, 3)) for k in range(7)]
    ref['cap_bracket'] = (1 / (576 * e_hi), 1 / (576 * e_lo))
    ref['excl_bracket'] = (1 / (236 * e_hi), 1 / (236 * e_lo))
    return ref


# ------------------------------------------------------------ validator (Rejected on any disagreement)
REPORT_NUMBERS = [  # (label, regex capturing the printed decimal, key of the exact own value)
    ('K_2\' tau^2 bound', r'\(about `(1\.34175e-12)`\)', 'bound'),
    ('band lower (item 4)', r'`(2\.87586637818e-19) <= omega\(h_R\) <= 9\.8e-7`', 'band_lower'),
    ('band upper (item 4)', r'<= omega\(h_R\) <= (9\.8e-7)`', 'band_upper'),
    ('L', r'\(about `(4\.37863e-10)`\)', 'L'),
    ('K_2\'', r'\(about `(13417\.5275439)`;', 'K2p'),
    ('formal band value at the cap', r'\(about `(4\.861e-18)` at the cap\)', 'formal_band_at_cap'),
    ('bound over formal', r'exceeds the formal term by the factor `(2\.38479e8)`', 'bound_over_formal'),
    ('upper over formal band', r'exceeds the formal value by `(2\.016e11)`', 'upper_over_formal'),
    ('lower below formal band', r'lies below it by the factor (16\.9)\.', 'formal_over_lower'),
    ('band ratio', r'\(ratio about `(3\.4e12)`\)', 'band_ratio'),
    ('e^{3/32}', r'\(about `(1\.0982851403078258486)`\)', 'e'),
    ('G_3(R)', r'`G_3\(R\) = 9 e\^\{3/32\}`, about `(9\.88456626277)`', 'G3'),
    ('G_3\'(R)', r'`G_3\'\(R\) = 118 e\^\{3/32\}`, about `(129\.597646556)`', 'G3p'),
    ('exclusion cap', r'\(about `(3\.858e-3)`\)', 'excl'),
    ('cap', r'\(about `(1\.58074715517e-3)`\)', 'cap'),
]


def report_exacts(ref):
    e_mid = (ref['e'][0] + ref['e'][1]) / 2
    formal_cap = ref['formal_band'] * TAU ** 2
    return {'bound': ref['bound'], 'band_lower': ref['band'][0], 'band_upper': ref['band'][1], 'L': ref['L'], 'K2p': ref['K2p'],
            'formal_band_at_cap': formal_cap, 'bound_over_formal': ref['bound'] / (ref['formal'] * TAU ** 2),
            'upper_over_formal': ref['band'][1] / formal_cap, 'formal_over_lower': formal_cap / ref['band'][0],
            'band_ratio': ref['band'][1] / ref['band'][0], 'e': e_mid, 'G3': 9 * e_mid, 'G3p': 118 * e_mid,
            'excl': 1 / (236 * e_mid), 'cap': 1 / (576 * e_mid)}


def validate_report(report, res, ref, con):
    tpl = con['preregistration']['mandatory_sentence_template']
    expect(report.count(tpl) == 1 and sum(1 for ln in report.splitlines() if tpl in ln) == 1, 'mandatory template')
    ex = report_exacts(ref)
    rows = []
    for label, pat, key in REPORT_NUMBERS:
        m = re.search(pat, report)
        expect(m is not None, 'report number missing: ' + label)
        expect(within_ulp(m.group(1), ex[key]), 'report number differs: ' + label)
        rows.append({'printed': m.group(1), 'quantity': label})
    # the enclosure table: printed previews against the producer's exact ends, widths against its exact widths
    tab = re.findall(r'\| (6|8) \| ±1/(\d+) \| `([0-9.e-]+)` \| `([0-9.e-]+)` \| ([0-9.e-]+) \| ([0-9.e-]+) \| \+ \|', report)
    expect(len(tab) == 6, 'report enclosure table rows')
    for D, den, plo, phi_, hw, rw in tab:
        pt = res['points']['D%s_l+1/%s' % (D, den)]
        lo, hi = rat(pt['z_enclosure'][0]), rat(pt['z_enclosure'][1])
        expect(is_truncation(plo, lo) and within_ulp(phi_, hi) and within_ulp(hw, (hi - lo) / 2)
               and within_ulp(rw, rat(pt['relative_width_upper'])), 'report enclosure row D=%s l=1/%s' % (D, den))
        rows.append({'printed_row': 'D=%s, |l|=1/%s' % (D, den)})
    m = re.search(r'the worst D=8 relative width is `([0-9.e-]+)`', report)
    own = ref['lemma'][(8, F(1, 10))]['rel']
    expect(m is not None and close(dec(m.group(1)), own, F(1, 10 ** 4)), 'report worst width differs from the own evaluation of the lemma')
    return rows


def validate_producer(res, report, ref, con):
    pr = ref['pre']
    expect(res.get('contract_sha256') == CONTRACT_SHA and res.get('loop') == 'BD2' and res.get('direction') == 'forward',
           'forward identity')
    for k in ('area_law_claimed', 'continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified',
              'uniqueness_of_ground_state_claimed', 'rate_in_a_claimed', 'rate_in_N_claimed', 'transfers_to_aq',
              'uniform_wilson_claim', 'resolved_interaction_shift', 'z3_1x2_sign_claimed', 'tight_electric_enclosure_claimed',
              'finite_volume_theorem_2p1_claimed', 'aq_statement_2p1_claimed', 'fg_coefficients_fitted'):
        expect(res.get(k) is False, 'forward claim flag ' + k)
    expect(res.get('model_is_finite_graph') is True and res.get('graph_sign_certified') is True and res.get('z3_1x2_formal_only') is True
           and res.get('electric_band_claimed') is True, 'forward claimed items')
    expect(res['gate_fields'] == con['preregistration']['gate_fields_required'], 'gate fields')
    expect(res['label']['sub_labels'] == SUB_LABELS and res['mandatory_sentence'] == con['preregistration']['mandatory_sentence_template'],
           'labels or template in the results')
    # item 1: tables with zeros, parities
    mine = pr['graph_tables']
    rules = {'W_1': (1, 0), 'z': (1, 1), 'C_shared': (0, 0), 'E_0': (0, 0)}
    for name, tab in res['coefficient_tables'].items():
        own = {k: F(v) for k, v in mine[name].items()}
        top = 5 if name == 'E_0' else 4
        expect(sorted(tab) == sorted('%d,%d' % (i, j) for i in range(top + 1) for j in range(top + 1 - i)), 'table index set ' + name)
        for k, v in tab.items():
            i, j = (int(x) for x in k.split(','))
            want = own.get(k, F(0)) if i + j <= 4 else F(0)
            expect(rat(v) == want, 'coefficient %s %s' % (name, k))
            expect(rat(v) == 0 or (i % 2, j % 2) == rules[name], 'flip parity %s %s' % (name, k))
    rs = check_by_id(res, 'rs2_tables_exact')
    expect({k: F(v) for k, v in rs['W_2'].items() if F(v) != 0} == {k: F(v) for k, v in mine['W_2'].items()}
           and rs['second_order_at_l1_eq_l2'] == {'C_shared': pr['predictions']['C_shared_second_order_diag'],
                                                 'z': pr['predictions']['z_second_order_diag']}
           and rs['identical_at_cutoffs'] == [6, 8] and rs['total_order'] == 4, 'W_2 table or l1=l2 second order')
    fl = check_by_id(res, 'independent_coupling_flip')
    expect(fl['parity_rules'] == {'C_shared': ['even', 'even'], 'W_1': ['odd', 'even'], 'z': ['odd', 'odd']}, 'flip parity rules')
    # item 2: enclosures and the angle lemma
    worst = F(0)
    for D in CUTOFFS:
        for l in LS:
            own = ref['lemma'][(D, l)]
            mine_enc = pr['enclosures']['%d,%s' % (D, l)]
            m_lo, m_hi = F(mine_enc['lower']), F(mine_enc['upper'])
            for sgn in (1, -1):
                key = 'D%d_l%s1/%d' % (D, '+' if sgn > 0 else '-', l.denominator)
                pt = res['points'][key]
                lo, hi = rat(pt['z_enclosure'][0]), rat(pt['z_enclosure'][1])
                led = pt['ledger']
                dr = led['d_ritz_eigenvector_residual']
                expect(0 < lo <= m_lo and m_hi <= hi and lo <= own['q'] <= hi, 'enclosure %s does not contain the own enclosure' % key)
                expect(pt['z_sign_certified'] is True and pt['D'] == D and rat(pt['l1_eq_l2']) == sgn * l, 'enclosure record ' + key)
                expect(rat(dr['certified_gap_E1_lower']) == own['b'] and rat(led['b_joint_product_channel']['joint_threshold_tail_lower'])
                       == ref['tail_lower'][D] and rat(led['b_joint_product_channel']['interacting_tail_threshold']) == own['tail_t'],
                       'gap or tail threshold ' + key)
                sB, sA = rat(dr['sin_theta_eckart_tail_comparison_upper']), rat(dr['sin_theta_davis_kahan_complete_residual_upper'])
                expect(close(sB, own['sB'], F(1, 10 ** 8)) and close(sA, own['sA'], F(1, 10 ** 8))
                       and rat(dr['sin_theta_used_upper']) == min(sA, sB) and sB < sA, 'forward Eckart angle ' + key)
                expect(close(rat(dr['complete_residual_squared_upper']), own['rho2'], F(1, 10 ** 8))
                       and close(rat(led['b_joint_product_channel']['complete_omitted_residual_squared_upper']), own['rhoQ2'], F(1, 10 ** 8)),
                       'forward residual ' + key)
                rel = (hi - lo) / lo
                expect(rel <= rat(pt['relative_width_upper']) and close(rel, own['rel'], F(1, 10 ** 6)), 'forward width ' + key)
                if D == 8:
                    worst = max(worst, rel)
            own_rows = {r_['link']: r_ for r_ in mine_enc['residual_ledger']['a_per_link_rows']}
            pled = res['points']['D%d_l+1/%d' % (D, l.denominator)]['ledger']
            for link in LINKS:
                row = pled['a_per_link_representation_tail'][link]
                expect(rat(row['threshold_free_energy']) == F(own_rows[link]['threshold']), 'per-link threshold %s D=%d' % (link, D))
            # the itemized sector weights of the complete omitted residual against the own ledger (13-digit previews)
            jb, ob = pled['b_joint_product_channel'], mine_enc['residual_ledger']['b_joint_channel']
            pairs = [(jb['per_link_class_weights_upper']['j'], own_rows['h1']['residual_weight_preview']),
                     (jb['per_link_class_weights_upper']['ell'], own_rows['vM']['residual_weight_preview']),
                     (jb['per_link_class_weights_upper']['k'], own_rows['h2']['residual_weight_preview']),
                     (jb['product_channel_weight_upper'], ob['product_channel_preview']),
                     (jb['x_channel_squared_upper'], ob['x_face_preview']), (jb['y_channel_squared_upper'], ob['y_face_preview']),
                     (jb['interference_2XY_bracket'][1], ob['interference_2XY_preview']),
                     (jb['corner_overlaps_upper']['ell+j'], ob['corners_preview']['e1&vM']),
                     (jb['corner_overlaps_upper']['ell+k'], ob['corners_preview']['e2&vM']),
                     (jb['corner_overlaps_upper']['j+k'], ob['corners_preview']['e1&e2']),
                     (jb['complete_omitted_residual_squared_upper'], ob['rho_Q2_preview'])]
            expect(all(within_ulp(p_.replace('e+', 'e'), rat(v_)) if rat(v_) != 0 else dec(p_.replace('e+', 'e')) == 0 for v_, p_ in pairs)
                   and rat(jb['product_channel_threshold']) == F(ob['product_threshold']), 'residual ledger items D=%d l=%s' % (D, l))
    expect(worst <= TARGET, 'target')
    tw = check_by_id(res, 'target_relative_width_D8')
    expect(tw['target'] == '1/10000000000000000' and within_ulp(tw['margin'], TARGET / rat(tw['rows']['D8_l+1/10']['relative_width_upper'])),
           'target record')
    # item 3
    z = res['z3_1x2']
    geo = ref['geo']
    expect(all(rat(r_['bound']) == ref['bound'] and r_['tier'] == 'exact_first_order' for r_ in z['bound_rows'])
           and sorted((r_['family'], r_['sign']) for r_ in z['bound_rows'])
           == sorted((f_, s_) for f_ in ('F1 boxes', 'F2 boxes', 'limit of the named constructions') for s_ in ('+', '-')),
           'W_1x2 bound rows')
    expect({k: rat(v) for k, v in z['K2prime_items_over_tau2'].items()} == ref['K2_items'], "K_2' items")
    ev, fm = z['evenness'], z['formal']
    expect(ev['F2_boxes_claimed'] is False and ev['remainder_from_evenness'] is None and ev['kappa'] == 0
           and ev['limit'].startswith('through BB2 at each sign'), 'evenness scope')
    expect(rat(fm['value']) == ref['formal'] == F(pr['z3_1x2']['formal_second_order_coefficient']) and fm['label'] == 'formal_second_order_coefficient'
           and fm['sign_of_omega_claimed'] is False and fm['certified_third_order_remainder'] is None
           and fm['certified_value_of_omega'] is None and fm['bound_encloses_formal_coefficient'] is False
           and sorted([list(p) + [d] for p, d in fm['rectangle']]) == geo['rect'], 'formal coefficient record')
    zg = check_by_id(res, 'z3_rectangle_geometry')
    expect(zg['counts'] == {'R_links': geo['R_links'], 'faces_containing_R': geo['containing'], 'faces_inside_R': geo['inside'],
                            'faces_meeting_R': geo['meeting'], 'faces_per_factor': geo['per_site'],
                            'faces_per_site_of_R_without_the_other_site': geo['per_site_without_other'], 'omitted_per_anchor': 21,
                            'straddling_meeting_R': geo['straddling']}, 'rectangle counts')
    z0 = check_by_id(res, 'z3_first_order_zero')
    expect(z0['trace_rho1_R_W12'] == '0' and z0['trace_P_R_W12'] == '0' and pr['z3_1x2']['first_order'] == '0', 'first-order zero')
    # item 4
    band = res['electric_band']
    expect(len(band['rows']) == 6 and all(rat(r_['lower']) == ref['band'][0] and rat(r_['upper']) == ref['band'][1]
                                          and r_['lower_tier'] == 'first_order_distance_from_product' and r_['upper_tier'] == 'crude_majorant'
                                          for r_ in band['rows'])
           and ref['band'][0] == F(pr['band']['lower']) and ref['band'][1] == F(pr['band']['upper'])
           and sorted((r_['family'], r_['sign']) for r_ in band['rows'])
           == sorted((f_, s_) for f_ in ('F1 boxes', 'F2 boxes', 'limit of the named constructions') for s_ in ('+', '-')), 'band rows')
    rt = band['route']
    expect(rt['upper_passage'] == 'lower semicontinuity' and rt['bounded_constant_applied_to_h_R'] is False and rt['fvdg_constant'] == '1/2'
           and rt['lower_gap'] == '6' and rt['upper_coefficient'] == '98' and rt['lower_distance_source_limit'] == 'AY2 gate item (2)'
           and rt['lower_distance_source_boxes'] == 'AY1 forward HNM-AY1-F11..F14 per-box ball', 'band route')
    plf = band['per_link_formal']
    expect({k: (v['omitted_faces'], rat(v['formal_coefficient'])) for k, v in plf.items()}
           == {k: (n, F(n, 3456)) for k, n in geo['n_e'].items()}, 'per-link formal counts')
    bs = check_by_id(res, 'band_both_signs')
    expect(rat(bs['L_distance_lower']) == ref['L'], 'band L')
    # item 5
    d = res['dimension_2p1']
    e_lo, e_hi = ref['e']
    expect(d['p'] == 3 and d['termination_order'] == 6 and d['faces_per_site'] == 3 and rat(d['J_over_tau']) == 1
           and [rat(x) for x in d['numerators']] == ref['numerators'] and d['exp_argument'] == '3/32' and d['tier'] is None
           and d['dictionary'].startswith('own contract'), '2+1D counts')
    xe = [rat(x) for x in d['exp_bracket']]
    g3, g3p, tb = [rat(x) for x in d['G3_R']], [rat(x) for x in d['G3prime_R']], [rat(x) for x in d['tau_star_bracket']]
    cap = rat(d['cap_directed_lower'])
    expect(xe[0] <= e_lo and e_hi <= xe[1] and g3 == [9 * xe[0], 9 * xe[1]] and g3p == [118 * xe[0], 118 * xe[1]]
           and cap <= ref['cap_bracket'][0] and tb[0] <= ref['cap_bracket'][0] and ref['cap_bracket'][1] <= tb[1]
           and cap * 9 * xe[1] <= F(1, 64) and 2 * cap * 118 * xe[1] < 1, '2+1D constants')
    dr_ = check_by_id(res, 'dimension_recount')
    expect(within_ulp(dr_['cap']['exclusion_alone_lower'], ref['excl_bracket'][0]), '2+1D exclusion condition')
    # item 6-7
    expect([r_['id'] for r_ in res['obligations']][:5] == OBLIGATION_IDS and all(r_['claimed'] is False and r_['missing_premise']
                                                                                   for r_ in res['obligations']), 'obligations')
    expect([w['id'] for w in res['contract_wording_defects']] == ['W%d' % i for i in range(1, 8)], 'wording defects W1-W7')
    ids = {c['id']: c for c in res['checks']}
    expect(all(c.get('passed') is True for c in res['checks']) and all(k in ids for k in con['controls']), 'controls')
    # provenance
    prov = check_by_id(res, 'az2_algebra_copied_verbatim')
    expect(prov['differing'] == [] and prov['blocks_compared'] == 63 and prov['source'] == 'research/round32/forward/az2/check.py'
           and 'copied verbatim' in prov['attribution'], 'AZ2 copy attribution')
    expect(check_by_id(res, 'no_repository_or_numerical_import')['banned_imports_absent'] is True, 'no repository import')
    validate_report(report, res, ref, con)
    return True


# ------------------------------------------------------------ closure, replays, mutation harness
def verify_closure():
    freeze = json.loads((FWD / 'freeze.json').read_text())
    sources = freeze['sources']
    files = {p.relative_to(ROOT).as_posix() for p in FWD.rglob('*') if p.is_file() and p != FWD / 'freeze.json'}
    ok = (freeze['loop'] == 'BD2' and freeze['direction'] == 'forward' and freeze['contract_sha256'] == CONTRACT_SHA
          and all(n.startswith(FWD_REL + '/') for n in sources) and set(sources) == files and len(sources) == 39
          and all(sha(ROOT / n) == h for n, h in sources.items())
          and not any('__pycache__' in n or n.endswith('.pyc') for n in files)
          and freeze['normal_optimized_identical'] is True and freeze['independent_before_current_counterpart_exchange'] is True
          and freeze['verdict'].startswith('accepted_within_scope'))
    inputs = sorted(p.relative_to(FWD / 'inputs').as_posix() for p in (FWD / 'inputs').rglob('*') if p.is_file())
    snaps = all((FWD / 'inputs' / n).read_bytes() == (ROOT / n).read_bytes() for n in inputs)
    return ok, inputs, snaps, freeze


def caches():
    roots = [FWD, ROOT / 'research/round11', ROOT / 'research/round32']
    return sorted({p.relative_to(ROOT).as_posix() for r in roots for p in r.rglob('*')
                   if p.name == '__pycache__' or p.suffix == '.pyc'})


def replay(script, pre_mode=False):
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bd2-skeptic-replay-') as tmp:
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(script), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(ROOT))
        if done.returncode != 0:
            raise ReviewFailure('replay failed: ' + str(script) + ' ' + done.stderr[-300:])
        return {p.relative_to(out).as_posix(): sha(p) for p in sorted(out.rglob('*')) if p.is_file()}, \
            ((out / 'results.json').read_bytes() if pre_mode else None)


def mutated_run(edits=(), report_edits=(), report_append=None, extra_input=None, input_edit=None, no_b=False):
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bd2-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / FWD_REL
        shutil.copytree(FWD, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
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
        last = done.stderr.strip().splitlines()[-1] if done.stderr.strip() else ''
        cache = sorted(p.relative_to(repo).as_posix() for p in repo.rglob('*') if p.name == '__pycache__' or p.suffix == '.pyc')
        return done.returncode, results, outputs, report, last.replace(tmp, '<tmp>'), cache


def parallel(fn, jobs):
    with ThreadPoolExecutor(max_workers=4) as ex:
        return list(ex.map(fn, jobs))


def tru(anchor):
    """Validator weakening: insert 'True or ' into the require(...) at the anchor."""
    if not anchor.lstrip().startswith('require('):
        raise ReviewFailure('weakening anchor is not a require: ' + anchor[:60])
    return [(anchor, anchor.replace('require(', 'require(True or ', 1))]


COPIED_HEAD = "    copied = ['def rat(', 'def s(',"
WEAK = [
    ('coherent_evidence_tampering', tru("            require(cid in ids and ids[cid]['passed'] is True, 'required control missing or failed: ' + cid)"),
     'control_boolean_flipped_hash_rebound'),
    ('exact_arithmetic_admission', [("        raise AdmissionError('non-exact input rejected: ' + repr(value))", "        return Q(value)"),
                                    (COPIED_HEAD, "    copied = ['def s(',")], 'float_input'),
    ('no_priority_or_continuum_claim', tru("            require(fl.get(k1) is v1, 'claim flag ' + k1 + ' changed')"), 'continuum_true'),
    ('changed_model_relabelled', tru("            require(mdl.get(key) in allowed, 'value relabelled to another model: ' + key)"),
     'graph_value_presented_as_Z3_value'),
    ('insufficient_verdict_retained',
     tru("        require(reported == forward_verdict(*args), 'reported verdict differs from the contract acceptance rule')"),
     'missed_width_target_relabelled_accepted'),
    ('placeholder_span_rejected',
     tru("        require(not placeholder_spans(text), 'placeholder span in the report: ' + (placeholder_spans(text) or [''])[0])"),
     'placeholder_with_whitespace'),
    ('negation_aware_phrase_scan', tru("        require(not hits, 'affirmative forbidden phrasing: ' + (hits[0]['phrase'] if hits else ''))"),
     'affirmative_thermodynamic_limit'),
    ('parameters_declare_metric_weights_window',
     tru("            require(m_na is not None, 'parameters.' + key + \": 'not applicable' needs its reason\")"), 'not_applicable_without_reason'),
    ('tier_mixing_rejected', tru("        require(t['band_lower']['tier'] == 'first_order_distance_from_product', 'band lower endpoint tier')"),
     'band_lower_under_the_upper_tier'),
    ('graph_couplings_named', tru("        require(gm['couplings'] == 'independent (l1,l2)', 'independent couplings')"),
     'equal_coupling_model_under_independent_label'),
    ('exact_rs_zero_truncation', tru("        require(tab6 == tab8, 'a coefficient differs between the cutoffs D=6 and D=8')"),
     'coefficient_differs_between_cutoffs'),
    ('independent_coupling_flip',
     tru("        require(cl['checked_on'] == 'full (m,n) table', 'parities must be checked on the full two-variable table, not only at l1=l2')"),
     'parity_checked_at_l1_eq_l2_only'),
    ('enclosure_itemized_residual', tru("        require(ld['c_gauge_invariant_projection'].get('reason'), 'a zero entry needs a stated reason')"),
     'gauge_entry_without_reason'),
    ('formal_coefficient_labelled',
     tru("        require(fm['label'] == 'formal_second_order_coefficient', 'the Z^3 second-order coefficient must carry the formal label')"),
     'formal_coefficient_presented_as_certified_value'),
    ('evenness_from_flip',
     tru("        require(e['F2_boxes_claimed'] is False, 'the AW1 flip lemma is admitted for F1 boxes only; F2 boxes are not claimed')"),
     'evenness_claimed_for_F2_boxes'),
    ('unbounded_observable_handled',
     tru("        require(b['bounded_constant_applied_to_h_R'] is False, 'a bounded-observable trace-norm constant cannot be applied to the unbounded h_R')"),
     'bounded_trace_norm_constant_applied_to_h_R'),
    ('band_both_signs',
     tru("            require(twin['lower'] == r_['lower'] and twin['upper'] == r_['upper'], 'the -tau row is the mirror replay of the +tau row')"),
     'minus_tau_row_not_a_mirror'),
    ('dimension_recount',
     tru("        require(rat(d['J_over_tau']) == J2_per_tau == 1, 'the 2+1D per-site sum is |tau| (three faces of norm |tau|/3; 28|tau| is 3+1D)')"),
     'three_plus_one_per_site_sum_28_tau_reused'),
    ('no_area_law_claim',
     tru("        require(a['area_law_claimed'] is False and a['string_tension_statement'] is None, 'no area-law or string-tension statement')"),
     'area_law_claimed_true'),
    ('no_transfer_to_eqed',
     tru("        require(r_['relation'] == 'no_shared_equation' and r_['comparison'] is None, 'recorded as a no-transfer row, not as a comparison')"),
     'eqed_comparison_drawn'),
    ('rate_range_stated', tru("            require(r_.get('range_of_N'), 'every rate in N carries its range of N in the same clause')"),
     'rate_without_range'),
]
TEMPLATE_ANCHOR = 'On the Round11 two-plaquette graph with independent couplings, the exact low-order coefficients'
MUST_ABORT = [
    ('Weyl free gap 3 replaced by 4 in the copied certificate constants', {'edits': [("WEYL_FREE_GAP = Q(3) ", "WEYL_FREE_GAP = Q(4) ")]},
     'failed check az2_algebra_copied_verbatim'),
    ('Eckart angle from the Temple bound only (tail comparison dropped; copy binding kept)',
     {'edits': [("    E0_low = max(E0_temple, E0_r11)", "    E0_low = E0_temple")]}, 'failed check az2_algebra_copied_verbatim'),
    ('band upper budget 56|tau| (two anchors per link pair) in place of the frozen 98|tau|',
     {'edits': [("    upper_coeff = 2 * len(stars_meeting_R) * star_norm", "    upper_coeff = 2 * 4 * star_norm")]},
     'failed check unbounded_observable_handled'),
    ('Fuchs-van de Graaf without the one half in the band lower end',
     {'edits': [("    lower_lim = V['band_gap'] * (L_ay2 / 2) ** 2", "    lower_lim = V['band_gap'] * L_ay2 ** 2")]},
     'failed check unbounded_observable_handled'),
    ('2+1D exponent with the 3+1D support p=4', {'edits': [("    x_exp = 2 * p2 * V['R_am2']", "    x_exp = 2 * (p2 + 1) * V['R_am2']")]},
     'failed check dimension_recount'),
    ("K_2' straddling item with rho in place of 2 rho",
     {'edits': [("2 * T_ * (geom['straddling_meeting_R'] * a_ + 2 * rho_)", "2 * T_ * (geom['straddling_meeting_R'] * a_ + rho_)")]},
     'failed check z3_bound_K2prime'),
    ("input: AY1 gate K_2' edited", {'input_edit': ('research/round32/advisor/ay1-gate.json', b"K_2'=", b"K_2' =")},
     'pinned premise hash differs: research/round32/advisor/ay1-gate.json'),
    ('input: contract snapshot edited', {'input_edit': ('research/round33/contracts/bd2.json', b'"frozen_before_any_outcome": true',
                                                        b'"frozen_before_any_outcome": false')},
     'contract snapshot bytes differ from the frozen BD2 contract'),
    ('input: undeclared skeptic file', {'extra_input': 'research/round33/skeptic/bd2-independent-derivation.md'},
     'inputs differ from AGENTS.md + contract + shared premises'),
    ('report: forbidden phrase appended', {'report_append': '\nThe positive <z> confirms an area law.\n'},
     'affirmative forbidden phrasing: confirms'),
    ('Eckart angle from the Temple bound only, with the verbatim binding of certify removed',
     {'edits': [("    E0_low = max(E0_temple, E0_r11)", "    E0_low = E0_temple"),
                ("'class PerCutoff:', 'def certify(', ", "'class PerCutoff:', ")]}, 'failed check z_certificates_complete'),
    ('report: template altered', {'report_edits': [(TEMPLATE_ANCHOR, 'On the Round11 two-plaquette graph, the exact low-order coefficients')]},
     'the mandatory template must appear exactly once as one unbroken span'),
]
SILENT = [
    ('harmless: exclusion-condition preview with 13 digits', {'edits': [("'exclusion_alone_lower': dec(excl_lo, 12),", "'exclusion_alone_lower': dec(excl_lo, 13),")]},
     None),
    ('interacting tail threshold exported without the -2|l| correction',
     {'edits': [("'interacting_tail_threshold': s(ct['tail_t']),", "'interacting_tail_threshold': s(ct['tail_t'] + 2 * abs(ct['tau'])),")]},
     'gap or tail threshold'),
    ('exclusion condition recorded with 3 J G_3\'(R) in place of 2 J G_3\'(R)',
     {'edits': [("    excl_lo = 1 / (2 * J2_per_tau * G3p[1])", "    excl_lo = 1 / (3 * J2_per_tau * G3p[1])")]}, '2+1D exclusion condition'),
]


def run(args):
    # 1. contract, pre-comparison package unchanged and replayed (the replayed bytes are the reference) ---------------------
    need(sha(CONTRACT) == CONTRACT_SHA, 'contract_sha256_pinned', sha256=CONTRACT_SHA)
    con = json.loads(CONTRACT.read_text())
    pf = json.loads(PRE_FREEZE.read_text())
    ok_pf = pf['contract_sha256'] == CONTRACT_SHA and pf['loop'] == 'BD2' and pf['stage'] == 'pre_comparison' \
        and all(sha(ROOT / p) == h for p, h in pf['files'].items())
    _, pre_bytes = replay(PRE_SCRIPT, pre_mode=True)
    need(ok_pf and pre_bytes == PRE_RESULTS.read_bytes(), 'pre_comparison_package_unchanged_and_replayed', freeze=pf['files'],
         note='the committed pre-comparison package (bf1f531, 06:10:08Z, after the BD2 forward commit 37fa623 06:00:06Z; values '
              'final at 05:55:31Z) is unchanged; bd2_check.py reproduces bd2-independent/results.json byte for byte in this mode')
    pr = json.loads(pre_bytes)

    # 2. closure, inventory, replay, pinned artifacts, caches ---------------------------------------------------------------
    ok, inputs, snaps, freeze = verify_closure()
    declared = sorted(set(['AGENTS.md', 'research/round33/contracts/bd2.json'] + con['shared_premises']))
    need(ok and inputs == declared and snaps and inputs == sorted(pre.OBSERVED_INPUTS)
         and all(sha(FWD / 'inputs' / n) == pre.OBSERVED_INPUTS[n] for n in inputs), 'producer_closure_and_inventory',
         closure_files=len(freeze['sources']), inputs=len(inputs),
         note='39 closure files verified one by one; 35 inputs equal the contract-derived list and the names-only inventory '
              'recorded before production; every snapshot byte-identical to the repository')
    need(all(sha(FWD / p) == h for p, h in FROZEN.items()), 'frozen_artifacts_pinned', pinned=FROZEN)
    outs, _ = replay(FWD / 'check.py')
    frozen_out = {p: sha(FWD / 'output' / p) for p in ('results.json', 'source-manifest.json')}
    need(outs == frozen_out and frozen_out['results.json'] == FROZEN['output/results.json'], 'producer_replay_byte_identical',
         outputs=outs, note='the producer replay in this interpreter mode (-B, or -B -O under -O) reproduces output/')
    res = json.loads((FWD / 'output/results.json').read_text())
    report = (FWD / 'report.md').read_text()
    need(caches() == [], 'no_interpreter_cache', checked=[FWD_REL + '/', 'research/round11/', 'research/round32/'])

    # 3. values against the own recomputation ----------------------------------------------------------------------------------
    ref = reference(pr)
    need(validate_producer(res, report, ref, con) is True, 'producer_values_equal_independent_recomputation',
         note='tables, parities, enclosures, angles, residuals, thresholds, the rectangle and its counts, K_2\' and its items, '
              'the bound rows, evenness scope, the formal coefficient, the band rows and route, the per-link counts, the 2+1D '
              'constants, obligations, W1-W7, provenance records and the report numbers equal or contain the own values')

    # 4. item 1 -------------------------------------------------------------------------------------------------------------------
    tabs = res['coefficient_tables']
    nz = {name: {k: v for k, v in t.items() if F(v) != 0} for name, t in tabs.items()}
    need(all(nz[name] == pr['graph_tables'][name] for name in ('W_1', 'z', 'C_shared', 'E_0')), 'item1_tables_and_flip_parities',
         entries_compared={name: len(t) for name, t in tabs.items()}, nonzero=nz,
         parities={'W_1': 'odd in l1 (flip of h1), even in l2 (flip of h2)', 'z': 'odd in each', 'C_shared': 'even in each'},
         note='every entry with m+n <= 4 (E_0 to 5), zeros included, equals the own table at D=6 and D=8; nonzero entries obey '
              'the face-1 (h1) and face-2 (h2) flip parities; the vM flip alone would only give the l1=l2 statement')

    # 5. item 2 --------------------------------------------------------------------------------------------------------------------
    rows = {}
    for (D, l), own in sorted(ref['lemma'].items()):
        pt = res['points']['D%d_l+1/%d' % (D, l.denominator)]
        mine = pr['enclosures']['%d,%s' % (D, l)]
        rows['D%d,|l|=1/%d' % (D, l.denominator)] = {
            'producer_relative_width': pt['relative_width_preview'], 'own_evaluation_of_producer_lemma': trunc((own['rel']), 6),
            'own_tail_comparison_certificate': mine['relative_width_preview'],
            'eckart_sin_theta_own': trunc(own['sB'], 8), 'davis_kahan_sin_theta_own': trunc(own['sA'], 8),
            'schur_complement_bound_above_temple': own['eckart_below_temple']}
    own8 = ref['lemma'][(8, F(1, 10))]
    need(own8['rel'] <= TARGET and all(r_['schur_complement_bound_above_temple'] for r_ in rows.values()),
         'item2_producer_lemma_reevaluated', rows=rows, target=q_(TARGET), own_worst_D8_of_producer_lemma=trunc(own8['rel'], 6),
         own_tail_certificate_worst_D8=pr['predictions']['max_relative_width_D8'],
         margin_producer=trunc(TARGET / own8['rel'], 4),
         note='the producer lemma is valid: Weyl E_1 >= 3-2|l| (||W_1+W_2|| <= 2); Temple E_0 >= mu - rho^2/(b-mu); the '
              'Round11 comparison H >= B (+) R Q_D with B = A - C C*/(tau_t - R), tau_t = tail_lower - 2|l| (45, 69), R = b, '
              'lambda_1(B) >= b - 4l^2/(tau_t - R) by interlacing and ||C|| <= 2|l|, and Temple on B; Eckart sin^2 <= '
              '(mu - E0_low)/(b - mu); Davis-Kahan sin <= rho/(b - mu); the observable step 2 s sigma + 2 s^2 ||z|| with '
              '||z|| = 1; evaluated with the own basis and Ritz vectors it reproduces every exported angle and residual to 8 '
              'digits; the own tail-comparison enclosures (3.56e-18 worst) lie inside the producer enclosures (1.80e-17 worst)')

    # 6. items 3-5 ----------------------------------------------------------------------------------------------------------------------
    geo = ref['geo']
    need(geo['rect_E3'] == 6 and geo['f1_E3'] == 3 and (geo['meeting'], geo['inside'], geo['containing'], geo['per_site'],
                                                         geo['per_site_without_other'], geo['straddling']) == (82, 10, 16, 49, 33, 72)
         and ref['K2p'] == F(re.search(r"K_2'=(\d+/\d+)", json.loads((ROOT / 'research/round32/advisor/ay1-gate.json').read_text())['accepted']).group(1))
         and ref['formal'] == F(7, 216) / 576, 'item3_rectangle_bound_evenness_formal',
         rectangle=geo['rect'], counts={'meeting_R': 82, 'inside_R': 10, 'containing_R': 16, 'per_site': 49, 'per_site_without_other': 33,
                                        'straddling': 72},
         K2_prime=q_(ref['K2p']), bound=q_(ref['bound']), bound_preview=trunc(ref['bound'], 6), formal=q_(ref['formal']),
         note='the rectangle is the frozen one (six links owned by R, both faces omitted with owner set R, |C cap E_3| = 6); '
              'first order 0 by single occurrence; K_2\' from the AY1 items with the own counts equals the AY1 gate rational; '
              'the bound K_2\' tau^2 holds for F1 and F2 boxes and the limit at both signs; evenness (AW1 flip lemma) only for F1 '
              'boxes and the limit (F2 not admitted); 7/124416 = (7/216)/24^2 is labelled formal, with no sign and no remainder')
    hist = {}
    for n in geo['n_e'].values():
        hist[n] = hist.get(n, 0) + 1
    need(ref['band'][0] == F(3, 2) * ref['L'] ** 2 and ref['band'][1] == F(49, 50000000) and hist == {2: 4, 3: 16, 4: 28}
         and ref['formal_band'] == F(7, 144) and ref['band'][0] < ref['formal_band'] * TAU ** 2 < ref['band'][1],
         'item4_band', lower=q_(ref['band'][0]), lower_preview=trunc(ref['band'][0]), upper=q_(ref['band'][1]), L=q_(ref['L']),
         n_e_histogram={str(k): v for k, v in sorted(hist.items())}, formal_total='7/144',
         note='h_R >= 6 Q_R (free Casimir gap 6 delta), Fuchs-van de Graaf with the pure reference: omega(h_R) >= 6 (L/2)^2 = '
              '(3/2)L^2 with L the AY2 lower end (limit) and the same rational from the AY1 F11-F14 per-box ball (boxes); upper '
              '2*7*7|tau| = 98|tau| (AQ1 reset, F2: AY1 item (1)), passed to the limit by lower semicontinuity of the monotone '
              'cutoff limit; the lower end is proved at the limit directly')
    need(ref['numerators'] == [8, 112, 1056, 8640, 65664, 476928, 3359232] and ref['cap_bracket'][0] > F(158074715517, 10 ** 14)
         and ref['excl_bracket'][0] > 2 * ref['cap_bracket'][1], 'item5_2p1_recount',
         numerators=[q_(x) for x in ref['numerators']], G3='9 e^{3/32}', G3_prime='118 e^{3/32}',
         e_bracket=[q_(x) for x in ref['e']], cap_bracket_preview=[trunc(x) for x in ref['cap_bracket']],
         exclusion_bracket_preview=[trunc(x) for x in ref['excl_bracket']],
         note='L_k(3) = 8*6^k*(1+4k/3), termination order 6, G_3(R) = 9e^{3/32}, G_3\'(R) = 118e^{3/32} at R = 1/64; the '
              'self-map J G_3(R) <= R binds: cap 1/(576 e^{3/32}); the exclusion 2 J G_3\'(R) < 1 allows 1/(236 e^{3/32}); the '
              'producer\'s directed brackets contain the own ones; no 2+1D finite-volume theorem is claimed')

    # 7. provenance, text, W1-W7 ----------------------------------------------------------------------------------------------------------
    code = (FWD / 'check.py').read_text()
    imports = sorted(set(re.findall(r'^(?:import|from) ([\w.]+)', code, re.M)))
    need(imports == ['argparse', 'decimal', 'fractions', 'functools', 'hashlib', 'json', 'math', 'pathlib', 're']
         and "solver = read_input(P_R11_SOLVER)" in code and 'importlib' not in code and 'exec(' not in code
         and 'not opened:* `research/round11/solver/two_plaquette.py`' in report, 'code_provenance',
         imports=imports, az2_blocks_copied=63,
         note='standard-library imports only; the AZ2 forward algebra is copied verbatim with attribution and compared block by '
              'block with the snapshot (63 blocks); the Round11 solver snapshot is read as bytes to bind 13 exact source strings '
              '(the list the AZ2 checker uses), never imported or executed; the producer agent reports it did not open that file; '
              'the skeptic hashed it only (pre-comparison) and this review does not open it either')
    need(sha(PHRASE_TOOL) == PHRASE_TOOL_SHA, 'phrase_tool_pinned')
    done = subprocess.run([sys.executable, '-B', str(PHRASE_TOOL), str(CONTRACT), str(FWD / 'report.md')],
                          capture_output=True, text=True, cwd=str(ROOT))
    tool_out = json.loads(done.stdout)
    tpl = con['preregistration']['mandatory_sentence_template']
    forbidden = pre.ROUND_FORBIDDEN + con['preregistration']['forbidden_phrasings']
    rep_rows = validate_report(report, res, ref, con)
    need(done.returncode == 0 and list(tool_out.values()) == [[]] and pre.affirmative_hits(report, forbidden, tpl) == []
         and report.count(tpl) == 1, 'phrase_scan_template_and_report_numbers', tool_exit=done.returncode, printed_numbers=rep_rows)
    wd = {w['id']: w['defect'] for w in res['contract_wording_defects']}
    need(len(wd) == 7 and 'F2 boxes a third-order remainder' in wd['W3'] and 'three owner sets' in wd['W4'] and 'J = |tau|' in wd['W5']
         and 'tier-(ii)' in wd['W6'] and 'lambda >= 0' in wd['W7'], 'wording_defects_W1_W7_adjudicated',
         adjudication={'W1': 'correct: the model id names the graph only; each value carries its own model label',
                       'W2': 'correct: the zero triple belongs to the Z^3 family',
                       'W3': 'correct and new: a fourth-order remainder presupposes evenness, admitted for F1 and the limit only',
                       'W4': 'correct: three faces per site = faces whose owner set contains the site (= own count)',
                       'W5': 'correct: J = |tau| is linear; J/|tau| = 1 and the G, counts and cap are tau-independent',
                       'W6': 'correct (labelling only): AY1 tier (ii) = the BD2 tier name exact_first_order for K_2\'',
                       'W7': 'correct: the Round11 API sign restriction is irrelevant to the exact certificates'})

    # 8. damaged packets --------------------------------------------------------------------------------------------------------------------
    def damaged(fn):
        pk = json.loads(json.dumps(res))
        fn(pk)
        try:
            validate_producer(pk, report, ref, con)
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
    dmg = [
        ('z coefficient (1,1) changed', setp(['coefficient_tables', 'z', '1,1'], '7/215'), 'coefficient z 1,1'),
        ('<W_1> given an (even, even) term', setp(['coefficient_tables', 'W_1', '2,0'], '1/7'), 'coefficient W_1 2,0'),
        ('D8 |l|=1/10 lower end raised above the own enclosure', setp(['points', 'D8_l+1/10', 'z_enclosure', 0], pr['enclosures']['8,1/10']['upper']),
         'does not contain the own enclosure'),
        ('Eckart angle replaced by the Davis-Kahan angle', setp(['points', 'D8_l+1/10', 'ledger', 'd_ritz_eigenvector_residual',
                                                               'sin_theta_eckart_tail_comparison_upper'],
                                                              lambda v: res['points']['D8_l+1/10']['ledger']['d_ritz_eigenvector_residual']['sin_theta_davis_kahan_complete_residual_upper']),
         'forward Eckart angle'),
        ('product-channel weight doubled at D=8, |l|=1/10',
         setp(['points', 'D8_l+1/10', 'ledger', 'b_joint_product_channel', 'product_channel_weight_upper'], lambda v: q_(2 * F(v))),
         'residual ledger items'),
        ('tail threshold 70 at D=8', setp(['points', 'D8_l+1/100', 'ledger', 'b_joint_product_channel', 'joint_threshold_tail_lower'], '70'),
         'gap or tail threshold'),
        ('W_1x2 bound quartered on the F2 row', lambda pk: pk['z3_1x2']['bound_rows'][2].update({'bound': q_(ref['bound'] / 4)}), 'W_1x2 bound rows'),
        ('evenness claimed for F2 boxes', setp(['z3_1x2', 'evenness', 'F2_boxes_claimed'], True), 'evenness scope'),
        ('formal coefficient relabelled certified', setp(['z3_1x2', 'formal', 'label'], 'certified_second_order_value'), 'formal coefficient record'),
        ('band lower replaced by the formal value', lambda pk: pk['electric_band']['rows'][0].update({'lower': q_(F(7, 144) * TAU ** 2)}), 'band rows'),
        ('band upper passed by continuity', setp(['electric_band', 'route', 'upper_passage'], 'trace-norm continuity'), 'band route'),
        ('per-link count of a z-link set to 3', setp(['electric_band', 'per_link_formal', '0,0,0,z', 'omitted_faces'], 3), 'per-link formal counts'),
        ('2+1D cap above the true cap', setp(['dimension_2p1', 'cap_directed_lower'], '1581/1000000'), '2+1D constants'),
        ('2+1D numerators with p=4', setp(['dimension_2p1', 'numerators'], ['16', '160', '1792', '18432', '180224', '1703936', '15728640']),
         '2+1D counts'),
        ('area law claimed', setp(['area_law_claimed'], True), 'forward claim flag area_law_claimed'),
        ('gate field z3_1x2_formal_only false', setp(['gate_fields', 'z3_1x2_formal_only'], False), 'gate fields'),
        ('obligation row dropped', lambda pk: pk['obligations'].pop(1), 'obligations'),
        ('wording defect W3 dropped', lambda pk: pk['contract_wording_defects'].pop(2), 'wording defects W1-W7'),
        ('AZ2 copy with a differing block', setp(['check:az2_algebra_copied_verbatim', 'differing'], ['def certify(']), 'AZ2 copy attribution'),
    ]
    rows_d = []
    for label, fn, reason in dmg:
        got = damaged(fn)
        if got is None or reason not in got:
            raise ReviewFailure('damaged packet accepted or rejected for another reason: %s (%s)' % (label, got))
        rows_d.append({'mutation': label, 'rejected_for': reason})
    need(len(rows_d) == len(dmg), 'damaged_packets_rejected_by_review_validator', rows=rows_d)

    # 9. source-edit runs ------------------------------------------------------------------------------------------------------------------------
    if sorted(w[0] for w in WEAK) != sorted(con['controls']):
        raise ReviewFailure('weakening table does not cover the 21 controls')
    label_sets = {c['id']: c.get('rejected_mutations', []) for c in res['checks']}
    for cid, _, label in WEAK:
        if label not in label_sets.get(cid, []):
            raise ReviewFailure('expected label is not a mutation of the control: %s %s' % (cid, label))
    frozen_bytes = {p.name: p.read_bytes() for p in sorted((FWD / 'output').glob('*.json'))}
    jobs = [('base', {}), ('nob', {'no_b': True})] + [('weak', {'edits': w[1]}) for w in WEAK] \
        + [('abort', t[1]) for t in MUST_ABORT] + [('silent', t[1]) for t in SILENT]
    outs = parallel(lambda j: mutated_run(**j[1]), jobs)
    base, nob = outs[0], outs[1]
    need(base[0] == 0 and base[2] == frozen_bytes and base[5] == [] and nob[0] == 0 and nob[2] == frozen_bytes and nob[5] == [],
         'unmutated_copy_and_run_without_B',
         note='an unmutated copy outside the checkout reproduces the frozen output byte for byte; a run without -B (and without '
              'PYTHONDONTWRITEBYTECODE) reproduces it too and writes no __pycache__ or .pyc anywhere in the copy')
    k = 2
    weak_rows = []
    for (cid, _, label), (rc, _, o, _, last, cache) in zip(WEAK, outs[k:k + len(WEAK)]):
        expect_msg = 'damaging mutation accepted: ' + label
        if rc == 0 or o or not last.endswith(expect_msg) or cache:
            raise ReviewFailure('weakening of %s not exposed as expected: %s' % (cid, last[-200:]))
        weak_rows.append({'control': cid, 'aborted_with': expect_msg})
    k += len(WEAK)
    need(len(weak_rows) == 21, 'control_validator_weakenings', runs=len(weak_rows), rows=weak_rows,
         note='one validator weakened per contract control on a temporary copy ("True or " inserted into the require that '
              'rejects a labelled mutation; for exact arithmetic the float branch returns a Fraction and rat is removed from the '
              'verbatim-copy list, which would otherwise expose the edit one check earlier); each run aborts naming a mutation of '
              'that control')
    ab_rows = []
    for (label, _, frag), (rc, _, o, _, last, cache) in zip(MUST_ABORT, outs[k:k + len(MUST_ABORT)]):
        if rc == 0 or o or frag not in last or cache:
            raise ReviewFailure('edit ran or aborted elsewhere: %s: %s' % (label, last[-200:]))
        ab_rows.append({'edit': label, 'aborted_with': last[-170:]})
    k += len(MUST_ABORT)
    need(len(ab_rows) == len(MUST_ABORT), 'must_abort_edits', runs=len(ab_rows), rows=ab_rows)
    silent_rows = []
    for (label, _, reason), (rc, out_res, _, out_report, last, cache) in zip(SILENT, outs[k:]):
        if rc != 0 or out_res is None or cache:
            raise ReviewFailure('silent edit aborted: %s: %s' % (label, last))
        try:
            validate_producer(out_res, out_report, ref, con)
        except Rejected as exc:
            if reason is None or reason not in str(exc):
                raise ReviewFailure('silent edit rejected for the wrong reason: %s: %s' % (label, exc))
            silent_rows.append({'edit': label, 'producer_run': 'completed', 'review_validator': 'rejected: ' + reason})
            continue
        if reason is not None:
            raise ReviewFailure('silent edit not caught by the review validator: ' + label)
        silent_rows.append({'edit': label, 'producer_run': 'completed',
                            'review_validator': 'accepted (non-damaging: every exported admitted value unchanged)'})
    need(len(silent_rows) == len(SILENT), 'silent_edits_accounted', rows=silent_rows,
         note='two export-only edits run to completion and are caught only by the review validator (an interacting tail '
              'threshold without the -2|l| correction; the exclusion condition with 3 J G_3\'(R)); dropping the tail comparison '
              'with the verbatim binding removed is not silent: the producer aborts at z_certificates_complete (its copied code '
              'must reproduce the AZ2 gate enclosure of <W_1> exactly)')
    need(caches() == [], 'no_interpreter_cache_after_all_runs', checked=[FWD_REL + '/', 'research/round11/', 'research/round32/'])

    n_runs = 2 + len(weak_rows) + len(ab_rows) + len(silent_rows)
    return {
        'loop': 'BD2', 'stage': 'post_comparison', 'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'skeptic (model agent, correlated ancestry; not human review)',
        'contract_sha256': CONTRACT_SHA, 'producer': 'forward (single producer, single+skeptic)',
        'commit_order_utc': [{'commit': 'a1010a4', 'time': '05:53:54', 'what': 'BD1 reverse producer'},
                             {'commit': '5a792b0', 'time': '05:54:17', 'what': 'BD1 forward producer'},
                             {'commit': '37fa623', 'time': '06:00:06', 'what': 'BD2 forward producer'},
                             {'commit': 'bf1f531', 'time': '06:10:08', 'what': 'skeptic BD1 and BD2 pre-comparison packages'}],
        'source_edit_runs': n_runs,
        'source_edit_breakdown': {'unmutated_and_no_B': 2, 'control_validator_weakenings': len(weak_rows),
                                  'must_abort_edits': len(ab_rows), 'silent_edits': len(silent_rows)},
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
