#!/usr/bin/env python3
"""Round33 BB1 skeptic post-comparison checker (locality of the reduced densities of F1 and F2).

Written after both BB1 producers froze and were committed (forward 33e0ae6, reverse 13ac349),
following the skeptic's pre-comparison package (09d0bdb, committed first). Standard library only;
exact Fractions decide every admission Boolean; floats appear only in labelled previews. Every
check raises an explicit exception, so python -O cannot disable it. Model-agent skeptic with
correlated ancestry; not human peer review.

What it does:
  * pins both producer freeze records and the skeptic pre-comparison freeze record, re-hashes
    every closure file, checks both 35-file input inventories against the contract (reverse
    premise isolation) and every snapshot against its repository source;
  * replays both producers (normal and -O, fresh temporary directories outside the checkout)
    and the skeptic pre-comparison program, byte-comparing with the frozen outputs;
  * re-derives every producer constant (headline C and c_site, labelled secondary pair, crude
    tier, Kotecky-Preiss and split proof constants, per comparison and per sign) and every
    tau -> tau/100 ratio exactly from the declared formulas, compares them with the
    pre-comparison predictions, and decides which constants the gate binds (the larger valid
    constant per quantity, the other route labelled);
  * re-checks, on exact finite fixtures of its own, the split identity at a two-site changed
    support, the covering-only contraction and the Y-cluster formula with vacuum probabilities;
  * runs source edits on temporary copies: an unmutated copy of each producer (must reproduce
    its frozen output), one validator weakening per contract control per producer (37 x 2; each
    must abort with 'damaging mutation accepted: <label of that control>'), and input edits;
  * rejects damaged producer packets with its own value validator;
  * checks the forward's cited Kotecky-Preiss statement (report section 6) against the Ueltschi excerpt committed
    after the freeze as a repair source (hash pinned; not a producer premise) and re-verifies the side conditions;
  * scans both reports (negation-aware, template removed as one literal, and through
    research/round33/tools/phrase_scan.py), counts the template span, and builds and scans the
    supported statement and limitations of the review.

Usage: python3 -B research/round33/skeptic/bb1_postreview_check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = 'research/round33/contracts/bb1.json'
CONTRACT_SHA256 = '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018'
PROD = {'forward': 'research/round33/forward/bb1', 'reverse': 'research/round33/reverse/bb1'}
FREEZE_SHA = {'forward': '90ddc1787b8dca35922ea5d80b01a21fa6e0a30102dba8244fe315e2d9430e1d',
              'reverse': '0e9c41d87d48449dc71b420792fb6396eb5c61cadaab0900bda6a7c628fd26b3'}
CHECK_SHA = {'forward': '7fb05c1a191ae61b29c78a34594b69816df4c63f7a0f402ce26e9f4d1af6774d',
             'reverse': 'c061105648933a059965a221ff137092544799e1b92bcce9eb31f43e805518f1'}
PRE_FREEZE_REL = 'research/round33/skeptic/bb1-independent-freeze.json'
PRE_FREEZE_SHA = '5ed6a971a20ad3b61ffea4ddf890227163ff5d0ea1e79a79252c6d55416d2f3e'
PRE_RESULTS_REL = 'research/round33/skeptic/bb1-independent/results.json'
PRE_CHECK_REL = 'research/round33/skeptic/bb1_check.py'
PHRASE_SCAN_REL = 'research/round33/tools/phrase_scan.py'
EXCERPT_REL = 'research/round33/sources/ueltschi-math-ph-0304003v3.md'
EXCERPT_SHA = '17b0b3ffe86b9a17ff8b9e24511b28e974bc0397590b75f179411f6d2c0eed66'
EXCERPT_PDF_SHA = '2cc3e036af5b2a46afe95acf0b5863fe5c7d31554debb10a2a5cade4122bdbfc'
EXCERPT_ANCHORS = ('**Theorem 1 (Cluster expansion).**', '**Theorem 3 (Decay of correlations).**',
                   '(16) \u222bd|\u00b5_b|(A\u2032) |\u03b6_c(A, A\u2032)| e^{a(A\u2032)} \u2264 a(A)',
                   '- (19) \u03a3_{n\u22651} \u222bd|\u00b5_b|(A_1)\u2026\u222bd|\u00b5_b|(A_n) (\u03a3_{i=1}^n |\u03b6_c(A, A_i)|) |\u03c6_c(A_1,\u2026,A_n)| \u2264 a(A)',
                   '\u00b5_b(A) = \u00b5(A) e^{b(A)}', '\u03b6(A, A\u2032) = \u22121 if A \u2229 A\u2032 \u2260 \u2205',
                   'Assume that |1 + \u03b6_c(A, A\u2032)| \u2264 1', '(both may vanish identically)')
FORWARD_KP_ANCHORS = ("`\u03a3_{\u03b3'\u2241\u03b3}|w(\u03b3')| e^{a(\u03b3')+d(\u03b3')} \u2264 a(\u03b3)`",
                      "`\u03a3_{X\u2241\u03b3}|\u03a6^T(X)| e^{d(X)} \u2264 a(\u03b3)` with `d(X) = \u03a3_{\u03b3'\u2208X} d(\u03b3')`",
                      'treated as a polymer of activity 0', 'apply Theorem 6.1 to the test set `{z}`')
SKEPTIC_ALLOWED = ('research/round33/skeptic/ba1.md', 'research/round33/skeptic/ba2.md', 'research/round29/skeptic/am2.md')
FORBIDDEN_IN_INPUTS = ('research/round33/skeptic/', 'research/round33/experts/', 'research/round33/forward/bb1/',
                       'research/round33/forward/bb2/', 'research/round33/reverse/bb1/', 'research/round33/reverse/bb2/',
                       'research/round33/advisor/deliberation', 'research/round33/advisor/plan', 'research/round33/advisor/brief',
                       'research/round33/advisor/panel', 'research/round33/advisor/findings')
ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state', 'uniquely determines the ground state',
    'the thermodynamic limit', 'correlation length',
]
NEGATION = re.compile(r"\b(not|never|no|nor|neither|without|excludes?|excluded|exclusion|forbidden|"
                      r"cannot|does not|is not|are not|nothing|none)\b", re.I)
G_R, GP_R, RB = F(148, 7), F(352), F(1, 64)
COMP_IDS = ('c1', 'c2', 'c3', 'c4', 'c5')
COMP_SHORT = {'c1': 'F1 on Lambda_N versus F1 on Lambda_(N+1)', 'c2': 'F2 on Lambda_N versus F2 on Lambda_(N+1)',
              'c3': 'fixed N: F1 versus F2 on the same Lambda_N', 'c4': 'any two centered boxes Lambda_M, Lambda_M\' (M, M\' at least N), '
              'F1 or F2, compared directly', 'c5': 'two finite complete-factor volumes of one prescription containing Lambda_N, compared directly'}


class ReviewFailure(RuntimeError):
    """A review check failed; the run aborts without output."""


class Rejected(Exception):
    """The review's value validator refused a packet."""


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise ReviewFailure(cid)
    if any(row['id'] == cid for row in CHECKS):
        raise ReviewFailure('duplicate check id ' + cid)
    row = {'id': cid, 'passed': True}
    row.update(detail)
    CHECKS.append(row)


def reject(ok, reason):
    if ok is not True:
        raise Rejected(reason)


def rejects(fn, reason):
    try:
        fn()
    except Rejected as exc:
        if reason not in str(exc):
            raise ReviewFailure('rejected for the wrong reason: %s (expected %s)' % (exc, reason))
        return True
    return False


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha(path):
    return sha_bytes(Path(path).read_bytes())


def q(x):
    return str(F(x))


def fq(s):
    if isinstance(s, dict):
        s = s['exact']
    if isinstance(s, (bool, float)):
        raise Rejected('non-exact value in a packet: ' + repr(s))
    return F(s)


def preview(x):
    return format(float(x), '.12e')


def short(x):
    return format(float(x), '.4e')


# ------------------------------------------------------------------ the declared formulas
def S(x):
    """sum over y in Z^3 of x^{d_inf(y,0)} (closed form, 0 <= x < 1)."""
    x = F(x)
    if not 0 <= x < 1:
        raise ReviewFailure('lattice sum domain')
    return 1 + 24 * x * (1 + x) / (1 - x) ** 3 + 2 * x / (1 - x)


def T(rho):
    """exact_first_order circle bound (49 rho/144)/(1 - 28 rho G'(R))."""
    return F(49, 144) * rho / (1 - 28 * rho * GP_R)


def Tc(rho):
    """crude_majorant circle bound 28 rho G(R)."""
    return 28 * rho * G_R


def fwd(tau, qq, K, tier='exact_first_order'):
    """Forward polymer_kp constants: report sections 0, 5-7, 9 (F09, F12, F13); weights w=3/q, v=2/q, e^b=1001/1000."""
    tau, qq, K = abs(F(tau)), F(qq), F(K)
    J, t1 = 28 * tau, F(49, 144) * tau
    w, v, eb = 3 / qq, 2 / qq, F(1001, 1000)
    wh = w * eb ** 4
    wmax = RB / (J * G_R)
    if wh > wmax:
        raise ReviewFailure('forward weight inadmissible')
    gam = J * wh * GP_R
    if tier == 'exact_first_order':
        t = t1 / (1 - 352 * J)
        tb = w * eb ** 3 * t1 / (1 - gam)
    elif tier == 'crude_majorant':
        t = J * G_R
        tb = J * wh * G_R
    else:
        raise ReviewFailure('tier')
    a = tb * tb
    svw, sqv = S(v / w), S(1 / (qq * v))
    A = 2 * tb ** 2 + a * (1 + 2 * tb ** 2 * svw)
    k0 = 4 * tb + 2 * A * (t + tb * (svw - 1))
    C = K * (1 + qq) * (2 * (1 + t) + (1 + t) ** 4 * k0 * (sqv - 1))
    cs = K * (2 + k0 * (sqv - 1))
    return {'C': C, 'c_site': cs, 'kappa0': k0, 'taubar': tb, 'a': a, 'Gamma': gam, 'loss': wh, 'w': w, 'v': v,
            'w_max': wmax, 'S_vw': svw, 'S_qv': sqv, 't': t, 'A': A}


def rev(tau, qq, K, W, tier='exact_first_order'):
    """Reverse iterated_split constants: report sections 4.5-5 (R11, R13); lambda=2/W, c_site=K(2+beta* S_lambda)."""
    tau, qq, K, W = abs(F(tau)), F(qq), F(K), F(W)
    if 28 * W * tau * G_R > RB:
        raise ReviewFailure('reverse split weight inadmissible')
    if tier == 'exact_first_order':
        t0, tW = 2 * T(tau), 2 * T(W * tau)
    elif tier == 'crude_majorant':
        t0, tW = 2 * Tc(tau), 2 * Tc(W * tau)
    else:
        raise ReviewFailure('tier')
    c1 = 4 * t0 * tW + (4 * tW + 4 * t0 * tW / (1 - t0)) / (1 - 8 * tW)
    c2 = 16 * t0 * tW + 16 * t0 * tW / ((1 - t0) * (1 - 8 * tW))
    beta = c1 / (1 - c2)
    lam = 2 / W
    if not lam < qq:
        raise ReviewFailure('split needs lambda < q')
    sl = S(lam / qq)
    cs = K * (2 + beta * sl)
    return {'C': cs * (1 + qq), 'c_site': cs, 'beta': beta, 'c1': c1, 'c2': c2, 't0': t0, 'tW': tW, 'S': sl, 'lambda': lam}


def inputs_for(tau):
    """BA1 every-site form (b) inputs at tau: headline K=2T(64|tau|), secondary K_2=2T(1/151552), crude K=2*28*64|tau|G(R)."""
    tau = abs(F(tau))
    return {'q': F(1, 64), 'q2': 151552 * tau, 'K': 2 * T(64 * tau), 'K2': 2 * T(F(1, 151552)),
            'Kc': 2 * Tc(64 * tau), 'Kc2': 2 * Tc(F(1, 151552)), 'W2': 1 / (37888 * tau)}


def all_constants(tau):
    i = inputs_for(tau)
    return {'fwd': fwd(tau, i['q'], i['K']), 'fwd2': fwd(tau, i['q2'], i['K2']),
            'fwd_crude': fwd(tau, i['q'], i['Kc'], 'crude_majorant'), 'fwd2_crude': fwd(tau, i['q2'], i['Kc2'], 'crude_majorant'),
            'rev': rev(tau, i['q'], i['K'], 1024), 'rev2': rev(tau, i['q2'], i['K2'], i['W2']),
            'rev_crude': rev(tau, i['q'], i['Kc'], 1024, 'crude_majorant'),
            'rev2_crude': rev(tau, i['q2'], i['Kc2'], i['W2'], 'crude_majorant'), 'inputs': i}


def check_by_id(res, cid):
    for c in res['checks']:
        if c['id'] == cid:
            return c
    raise Rejected('check missing: ' + cid)


# ------------------------------------------------------------------ value validators
def validate_forward(res, tau, template, comparisons, gate_fields):
    reject(res.get('contract_sha256') == CONTRACT_SHA256 and res.get('direction') == 'forward', 'forward identity')
    cc, cs = all_constants(tau), all_constants(tau / 100)
    f, f2, fc, fc2 = cc['fwd'], cc['fwd2'], cc['fwd_crude'], cc['fwd2_crude']
    h = res['headline']
    rf = h['R_form']
    reject(fq(rf['C']) == f['C'] and rf['q'] == '1/64' and rf['C_target'] == '1/250000' and rf['target_met'] is True
           and rf['tier'] == 'exact_first_order' and rf['route'] == 'polymer_kp', 'forward R_form C not reproduced')
    reject(all(fq(rf['per_sign'][s]['C']) == f['C'] for s in '+-'), 'forward R_form per-sign C')
    rg = h['region_form']
    reject(fq(rg['c_site']) == f['c_site'] and rg['c_site_target'] == '1/500000' and rg['target_met'] is True
           and rg['q'] == '1/64', 'forward region c_site not reproduced')
    reject(all(fq(rg['per_sign'][s]['c_site']) == f['c_site'] for s in '+-'), 'forward region per-sign c_site')
    comps = h['comparisons']
    reject(sorted(comps) == sorted(comparisons), 'forward comparison set')
    for name in comparisons:
        c = comps[name]
        reject(fq(c['C']) == f['C'] and fq(c['c_site']) == f['c_site'] and c['exponent_at_e_z'] == 'N-1'
               and all(fq(c['per_sign'][s]['C']) == f['C'] and fq(c['per_sign'][s]['c_site']) == f['c_site'] for s in '+-')
               and fq(c['secondary']['C']) == f2['C'] and fq(c['secondary']['c_site']) == f2['c_site']
               and fq(c['crude']['C']) == fc['C'], 'forward comparison not reproduced: ' + name[:40])
    union = comps[comparisons[4]]['labelled_union_form']
    reject(fq(union['C']) == 2 * f['C'] and fq(union['c_site']) == 2 * f['c_site'] and union['status'] == 'labelled only',
           'forward union form')
    cr = h['crude_tier']
    reject(fq(cr['C']) == fc['C'] and cr['meets_C_target'] is False and cr['tier'] == 'crude_majorant'
           and cr['region_form_available'] is False and fq(cr['secondary_crude_C']) == fc2['C'], 'forward crude tier')
    for key, val in (('headline', f), ('secondary', f2), ('headline_crude', fc)):
        kp = h['kp'][key]
        reject(fq(kp['a']) == val['a'] and fq(kp['taubar_mixed']) == val['taubar'] and fq(kp['Gamma']) == val['Gamma']
               and fq(kp['loss_w_e4b']) == val['loss'] and fq(kp['w']) == val['w'] and fq(kp['v']) == val['v']
               and fq(kp['t_anchored']) == val['t'] and fq(kp['S_v_over_w']) == val['S_vw'] and fq(kp['S_1_over_qv']) == val['S_qv']
               and fq(kp['w_max']) == val['w_max'] and val['a'] <= 2 * F(1, 1001) and val['v'] <= val['w'],
               'forward kp constants ' + key)
    for key, val in (('headline', f), ('secondary', f2), ('headline_crude', fc)):
        reject(fq(h['lemma'][key]['kappa0']) == val['kappa0'] and fq(h['lemma'][key]['eta_R']) == val['t'], 'forward lemma ' + key)
    sp = h['secondary_pair']
    reject(fq(sp['C']) == f2['C'] and fq(sp['c_site']) == f2['c_site'] and sp['targets_met'] is True
           and sp['C_target'] == '1/20000' and sp['c_site_target'] == '1/40000' and sp['status'] == 'labelled', 'forward secondary')
    sc = h['scaling']
    ratios = {'C_headline': f['C'] / cs['fwd']['C'], 'c_site': f['c_site'] / cs['fwd']['c_site'],
              'C_secondary': f2['C'] / cs['fwd2']['C'], 'c_site_secondary': f2['c_site'] / cs['fwd2']['c_site'],
              'q_secondary': cc['inputs']['q2'] / cs['inputs']['q2']}
    reject(all(fq(sc[k]) == v for k, v in ratios.items()), 'forward scaling ratios not reproduced')
    reject(all(F(95) <= ratios[k] <= F(105) for k in ('C_headline', 'c_site'))
           and all(F(99, 100) <= ratios[k] <= F(101, 100) for k in ('C_secondary', 'c_site_secondary'))
           and ratios['q_secondary'] == 100, 'forward scaling brackets')
    reject(res['mandatory_sentence'] == template, 'forward mandatory sentence')
    reject(res['gate_fields'] == gate_fields, 'forward gate fields')
    for cid in ('fixed_N_F1_versus_F2_item', 'one_prescription_volumes_compared_directly', 'untruncated_ground_vectors_at_fixed_N',
                'headline_R_form_every_comparison_both_signs', 'region_form_every_comparison_both_signs', 'every_site_coefficient_input',
                'kotecky_preiss_condition_and_tree_majorant', 'polymer_kp_lemmas_audited_on_finite_graphs'):
        reject(check_by_id(res, cid)['passed'] is True, 'forward check ' + cid)
    return True


def validate_reverse(res, tau, template, comparisons, gate_fields):
    reject(check_by_id(res, 'contract_snapshot_bound').get('contract_sha256') == CONTRACT_SHA256 and res.get('direction') == 'reverse',
           'reverse identity')
    cc, cs = all_constants(tau), all_constants(tau / 100)
    r, r2, rc, rc2 = cc['rev'], cc['rev2'], cc['rev_crude'], cc['rev2_crude']
    h = res['headline']
    st = h['statement_constants']
    reject(fq(st['C']) == r['C'] and st['q'] == '1/64' and st['target'] == '1/250000' and st['tier'] == 'exact_first_order'
           and st['route'] == 'iterated_split' and st['cover'] == 'R={0,e_z}', 'reverse statement C not reproduced')
    rg = h['region_form']
    reject(fq(rg['c_site']) == r['c_site'] and rg['q'] == '1/64' and rg['target'] == '1/500000', 'reverse region c_site not reproduced')
    rows = h['comparisons']
    seen = set()
    for row in rows:
        match = [i for i, name in enumerate(comparisons) if name.startswith(row['comparison'])]
        reject(len(match) == 1 and len(row['comparison']) >= 40, 'reverse comparison name not a unique prefix')
        reject(row['sign'] in ('+', '-') and (match[0], row['sign']) not in seen, 'reverse comparison row duplicated')
        seen.add((match[0], row['sign']))
        reject(fq(row['C']) == r['C'] and fq(row['c_site']) == r['c_site'], 'reverse comparison not reproduced')
        reject(row['in_each_Q_L'] is True and row['untruncated_at_fixed_N'] is True, 'reverse comparison regime flags')
    reject(len(rows) == 10 and len(seen) == 10, 'reverse comparisons: five comparisons times two signs')
    sp = h['secondary_pair_labelled']
    reject(fq(sp['C']) == r2['C'] and fq(sp['c_site']) == r2['c_site'] and fq(sp['K_input']) == cc['inputs']['K2']
           and sp['targets'] == ['1/20000', '1/40000'] and sp['disc_radius'] == '1/151552', 'reverse secondary not reproduced')
    cr = h['crude_tier']
    reject(fq(cr['C']) == rc['C'] and fq(cr['c_site']) == rc['c_site'] and fq(cr['secondary_C']) == rc2['C']
           and fq(cr['secondary_c_site']) == rc2['c_site'] and rc['C'] > F(1, 250000), 'reverse crude tier')
    lm = h['marginal_locality_lemma']
    reject(lm['eta'] == '0' and lm['kappa0'].startswith(q(r['beta']) + ' |Y|') and lm['w_prime'] == '512'
           and lm['route'] == 'iterated_split' and lm['p'] == '|I|', 'reverse lemma constants')
    reject(h['recursion']['per_level_factor'].endswith('8 t_W = ' + q(8 * r['tW'])) and q(8 * r['tW']) == '196/3160809',
           'reverse per-level factor')
    reject(h['every_site_form'] == 'b', 'reverse every-site form')
    rt = check_by_id(res, 'tau_scaling_every_headline_constant')
    ratios = {'C_headline': r['C'] / cs['rev']['C'], 'c_site': r['c_site'] / cs['rev']['c_site'],
              'secondary_C': r2['C'] / cs['rev2']['C'], 'secondary_c_site': r2['c_site'] / cs['rev2']['c_site'],
              'q_secondary': F(100)}
    reject(all(fq(rt['ratios'][k]) == v for k, v in ratios.items()), 'reverse ratio not reproduced')
    reject(all(F(95) <= ratios[k] <= F(105) for k in ('C_headline', 'c_site'))
           and all(F(99, 100) <= ratios[k] <= F(101, 100) for k in ('secondary_C', 'secondary_c_site')), 'reverse ratio brackets')
    reject(fq(rt['crude_labelled']['C']) == rc['C'] / cs['rev_crude']['C'], 'reverse labelled crude ratio')
    reject(res['mandatory_sentence_template'] == template, 'reverse mandatory sentence')
    reject(res['gate_fields'] == gate_fields, 'reverse gate fields')
    for cid in ('every_comparison_both_signs', 'cutoff_uniform_then_removed_at_fixed_N', 'every_site_common_core_enumerated',
                'order_versus_distance_every_site', 'fixture_split_route_identities', 'fixture_end_to_end_marginal_lemma',
                'marginal_locality_lemma_constants', 'per_site_charging_versus_growing_sizes', 'reverse_inputs_inventory_exact'):
        reject(check_by_id(res, cid)['passed'] is True, 'reverse check ' + cid)
    return True


# ------------------------------------------------------------------ own exact fixtures
def _msk(*sites):
    m = 0
    for i in sites:
        m |= 1 << i
    return m


def _cre(v, m, a):
    out = [F(0)] * len(v)
    for s, x in enumerate(v):
        if x and not (s & m):
            out[s | m] += a * x
    return out


def _state(n, coll):
    v = [F(0)] * (2 ** n)
    v[0] = F(1)
    for m, a in coll:
        c = _cre(v, m, a)
        v = [x - y for x, y in zip(v, c)]
    return v


def _ip(u, v):
    return sum(a * b for a, b in zip(u, v))


def _ptrace(u, v, keep, n):
    k = len(keep)
    M = [[F(0)] * (2 ** k) for _ in range(2 ** k)]
    for s, x in enumerate(u):
        if not x:
            continue
        a = sum(((s >> i) & 1) << j for j, i in enumerate(keep))
        rest = s & ~_msk(*keep)
        for b in range(2 ** k):
            t = rest | sum(((b >> j) & 1) << i for j, i in enumerate(keep))
            M[a][b] += x * v[t]
    return M


def _rho(v, Y, n):
    M = _ptrace(v, v, Y, n)
    z = sum(M[i][i] for i in range(len(M)))
    return [[x / z for x in row] for row in M]


def own_fixtures():
    """Qubit chain of five sites, eight supports; the reverse split identity (R07) at the two-site changed
    support J={2,3}, the covering-only contraction (R09) and the forward Y-cluster formula (F06)."""
    n = 5
    col = {_msk(0): F(1, 5), _msk(0, 1): F(1, 3), _msk(1, 2): F(-1, 4), _msk(2, 3): F(1, 6), _msk(3): F(1, 7),
           _msk(3, 4): F(2, 9), _msk(1): F(1, 8), _msk(2, 3, 4): F(-1, 10)}
    Y = [0]
    J = _msk(2, 3)
    cJ, cJp = col[J], F(-1, 11)
    cp = dict(col)
    cp[J] = cJp
    psi, psip = _state(n, list(col.items())), _state(n, list(cp.items()))
    lhs = [[a - b for a, b in zip(r1, r2)] for r1, r2 in zip(_rho(psi, Y, n), _rho(psip, Y, n))]
    miss = [(m, a) for m, a in col.items() if not (m & J)]
    meet = [(m, a) for m, a in col.items() if (m & J) and m != J]
    phi = _state(n, miss)
    n2 = _ip(phi, phi)
    EJ = phi
    for m, a in meet:
        c = _cre(EJ, m, a)
        EJ = [x - y for x, y in zip(EJ, c)]
    dpsi = [x - y for x, y in zip(EJ, phi)]
    delta = cJ - cJp
    g = [F(0)] * len(dpsi)
    for s, x in enumerate(dpsi):
        if x and (s & J) == J:
            g[s & ~J] += delta * x
    gam = _ptrace(phi, g, Y, n)
    trg = sum(gam[i][i] for i in range(len(gam)))
    rp, rphi = _rho(psip, Y, n), _rho(phi, Y, n)
    Z = _ip(psi, psi)
    a = cJ ** 2 - cJp ** 2
    k = len(gam)
    rhs = [[(a * n2 * (rphi[i][j] - rp[i][j]) - (gam[i][j] - trg * rp[i][j]) - (gam[j][i] - trg * rp[j][i])) / Z
            for j in range(k)] for i in range(k)]
    fams = []
    for size in range(1, len(meet) + 1):
        for comb in combinations(meet, size):
            ms = [m for m, _ in comb]
            if any(ms[i] & ms[j] for i in range(len(ms)) for j in range(i + 1, len(ms))):
                continue
            fams.append(comb)
    full, covonly = [F(0)] * len(dpsi), [F(0)] * len(dpsi)
    covering = 0
    for comb in fams:
        v = phi
        union = 0
        for m, amp in comb:
            v = _cre(v, m, amp)
            union |= m
        sgn = (-1) ** len(comb)
        covering += 1 if (union & J) == J else 0
        for s, x in enumerate(v):
            if x and (s & J) == J:
                full[s & ~J] += sgn * delta * x
                if (union & J) == J:
                    covonly[s & ~J] += sgn * delta * x
    # forward (F06): rho_Y = sum_eta rho_eta pi(supp eta) with pi(S) = Z(Lambda \ S)/Z(Lambda)
    sup = list(col.items())
    allf = []
    for size in range(len(sup) + 1):
        for comb in combinations(range(len(sup)), size):
            ms = [sup[i][0] for i in comb]
            if not any(ms[i] & ms[j] for i in range(len(ms)) for j in range(i + 1, len(ms))):
                allf.append(comb)

    def exc(fam):
        u = 0
        for i in fam:
            u |= sup[i][0]
        return u

    def famvec(fam):
        v = [F(0)] * (2 ** n)
        v[0] = F(1)
        for i in fam:
            v = _cre(v, sup[i][0], sup[i][1])
        return v

    def zof(region):
        v = _state(n, [(m, amp) for m, amp in sup if (m & ~region) == 0])
        return _ip(v, v)
    full_mask = (1 << n) - 1
    f06 = {}
    for Yl in ([0], [0, 1]):
        Ym = _msk(*Yl)
        clusters = set()
        for fa in allf:
            for fb in allf:
                if (exc(fa) & ~Ym) != (exc(fb) & ~Ym):
                    continue
                verts = [('L', i) for i in fa] + [('R', i) for i in fb]
                comp = set(x for x in verts if sup[x[1]][0] & Ym)
                stack = list(comp)
                while stack:
                    x = stack.pop()
                    for y in verts:
                        if y not in comp and y[0] != x[0] and (sup[y[1]][0] & sup[x[1]][0]):
                            comp.add(y)
                            stack.append(y)
                clusters.add((tuple(sorted(i for s_, i in comp if s_ == 'L')), tuple(sorted(i for s_, i in comp if s_ == 'R'))))
        tot = [[F(0)] * (2 ** len(Yl)) for _ in range(2 ** len(Yl))]
        zl = zof(full_mask)
        for f0, f1 in sorted(clusters):
            sgn = (-1) ** (len(f0) + len(f1))
            supp = Ym | exc(f0) | exc(f1)
            M = _ptrace(famvec(f1), famvec(f0), Yl, n)
            pi = zof(full_mask & ~supp) / zl
            if not F(0) < pi <= 1:
                raise ReviewFailure('vacuum probability outside (0,1]')
            for i in range(len(tot)):
                for j in range(len(tot)):
                    tot[i][j] += sgn * M[i][j] * pi
        f06[str(Yl)] = {'identity': tot == _rho(psi, Yl, n), 'y_clusters': len(clusters)}
    # (P3) coverings: Cov(T) <= t_0 for every nonempty region T of the chain (majorant m = |c|)
    t0 = max(sum(abs(amp) for m, amp in sup if m & (1 << x)) for x in range(n))
    cov_ok = True
    for size in range(1, n + 1):
        for T_ in combinations(range(n), size):
            Tm = _msk(*T_)
            tot_cov = F(0)
            for fam in allf:
                if fam and (exc(fam) & Tm) == Tm and all(sup[i][0] & Tm for i in fam):
                    prod = F(1)
                    for i in fam:
                        prod *= abs(sup[i][1])
                    tot_cov += prod
            cov_ok = cov_ok and tot_cov <= t0
    return {'R07_identity': lhs == rhs, 'Z_at_least_n2': Z >= n2, 'covering_only': full == g and covonly == g,
            'families_meeting_J': len(fams), 'covering_families': covering, 'F06': f06, 'P3_coverings': cov_ok, 't0': q(t0)}


# ------------------------------------------------------------------ source-edit tables (anchors in each producer check.py)
FWD = [
 ('changed_model_relabelled', [("    require(m.get('model_id') == 'AQ_patterned_zero_selected', 'model id changed')",
   "    require(True or m.get('model_id') == 'AQ_patterned_zero_selected', 'model id changed')")],
  'finite_graph_model_id'),
 ('coefficient_decay_not_marginal_decay', [("        require(not (coeff_diff_on_R == 0 and r1 != r2), 'equal coefficients on supports meeting R do not give equal marginals')",
   "        require(True or not (coeff_diff_on_R == 0 and r1 != r2), 'equal coefficients on supports meeting R do not give equal marginals')")],
  'state_decay_inferred_from_equal_coefficients'),
 ('coherent_evidence_tampering', [("            require(cid in ids and ids[cid]['passed'] is True and ids[cid].get('rejected_mutations'), 'required control missing or failed: ' + cid)",
   "            require(True or cid in ids and ids[cid]['passed'] is True and ids[cid].get('rejected_mutations'), 'required control missing or failed: ' + cid)")],
  'control_boolean_flipped_hash_rebound'),
 ('common_clock', [("        require(rec['coupling'] == 'the same tau for both boxes of every comparison', 'common coupling')",
   "        require(True or rec['coupling'] == 'the same tau for both boxes of every comparison', 'common coupling')")],
  'different_couplings_per_box'),
 ('cutoff_limit_order', [("        require(rec == ['L to infinity at fixed N', 'bound passes to the untruncated vector', 'N fixed throughout'], 'limit order')",
   "        require(True or rec == ['L to infinity at fixed N', 'bound passes to the untruncated vector', 'N fixed throughout'], 'limit order')")],
  'n_and_l_limits_exchanged'),
 ('cutoff_uniform_then_removed', [("        require(rec['order'][0].startswith('each on-site cutoff space Q_L') and rec['order'][1].startswith('then L to infinity at fixed N'),",
   "        require(True or rec['order'][0].startswith('each on-site cutoff space Q_L') and rec['order'][1].startswith('then L to infinity at fixed N'),")],
  'limits_reversed'),
 ('cutoff_vector_removal', [("        require(gap > 0, 'vector removal needs a positive untruncated gap')",
   "        require(True or gap > 0, 'vector removal needs a positive untruncated gap')"), ("        require(overlap_defect <= energy_excess / gap, 'overlap defect above the Eckart bound')",
   "        require(True or overlap_defect <= energy_excess / gap, 'overlap defect above the Eckart bound')")],
  'eigenvalue_convergence_used_for_vectors_without_gap'),
 ('decay_rate_in_N_not_a', [("        require(unit.startswith('per coarse l-infinity step in N at fixed spacing'), 'rate unit must be per coarse step in N at fixed spacing')",
   "        require(True or unit.startswith('per coarse l-infinity step in N at fixed spacing'), 'rate unit must be per coarse step in N at fixed spacing')")],
  'rate_per_fm'),
 ('every_site_coefficient_input', [("        require(rec.get('scope', '').startswith('every site u of the smaller box'), 'coefficient input used at every site')",
   "        require(True or rec.get('scope', '').startswith('every site u of the smaller box'), 'coefficient input used at every site')")],
  'r_only_input_used_at_far_sites'),
 ('exact_arithmetic_admission', [("        raise AdmissionError('non-exact input rejected: ' + repr(value))",
   '        return Q(value)')],
  'float_constant'),
 ('fixture_polymer_identity', [("        require(Zp == Z4_brute, 'polymer sum differs from the brute-force norm')",
   "        require(True or Zp == Z4_brute, 'polymer sum differs from the brute-force norm')")],
  'polymers_without_overlap_connectivity'),
 ('fixture_second_order_propagation', [("        require(claimed == dN01_dg, 'claimed propagation polynomial differs from the exact -a b')",
   "        require(True or claimed == dN01_dg, 'claimed propagation polynomial differs from the exact -a b')")],
  'first_order_propagation_claim'),
 ('fixture_split_lipschitz_and_trace', [("        require(tn2_sq(drho) <= factor ** 2 * tn2_sq(Nd), 'normalization Lipschitz ||rho(w)-rho(w\\')|| <= 2||N(w-w\\')||')",
   "        require(True or tn2_sq(drho) <= factor ** 2 * tn2_sq(Nd), 'normalization Lipschitz ||rho(w)-rho(w\\')|| <= 2||N(w-w\\')||')")],
  'normalization_lipschitz_factor_quartered'),
 ('global_fidelity_orthogonality_catastrophe', [("        require(all(values[ks[i + 1]] <= values[ks[i]] for i in range(len(ks) - 1)), 'a bound through the global overlap does not decay in N')",
   "        require(True or all(values[ks[i + 1]] <= values[ks[i]] for i in range(len(ks) - 1)), 'a bound through the global overlap does not decay in N')")],
  'bound_through_global_overlap'),
 ('global_lipschitz_not_decay', [("        require(source == 'q from the every-site coefficient input and v^{-d} from the polymer weights', 'decay must not come from a Lipschitz constant')",
   "        require(True or source == 'q from the every-site coefficient input and v^{-d} from the polymer weights', 'decay must not come from a Lipschitz constant')")],
  'map_lipschitz_as_per_shell_factor'),
 ('insufficient_verdict_retained', [("        require(verdict_for(C, cs, rate_ok, True, True) == claimed, 'verdict does not follow from the constants')",
   "        require(True or verdict_for(C, cs, rate_ok, True, True) == claimed, 'verdict does not follow from the constants')")],
  'crude_tier_relabelled_accepted'),
 ('marginal_locality_constants_explicit', [("            require(rec.get(key), 'marginal-locality lemma constant missing: ' + key)",
   "            require(True or rec.get(key), 'marginal-locality lemma constant missing: ' + key)")],
  'kp_criterion_asserted_without_activity_bounds'),
 ('mixed_weight_lemma_proved', [("    require(what <= wmax, 'proof weight outside the admissible range after the cardinality loss')",
   "    require(True or what <= wmax, 'proof weight outside the admissible range after the cardinality loss')")],
  'creation_weight_beyond_w_max'),
 ('named_construction_not_uniqueness', [("    require(not bad, 'affirmative forbidden phrase in ' + label + ': ' + json.dumps(bad[:2]))",
   "    require(True or not bad, 'affirmative forbidden phrase in ' + label + ': ' + json.dumps(bad[:2]))")],
  'thermodynamic_limit_phrase'),
 ('negation_aware_phrase_scan', [('NEGATION = re.compile(r"\\b(not|never|',
   'NEGATION = re.compile(r"\\b(gives|not|never|')],
  'affirmative_thermodynamic_limit'),
 ('no_priority_or_continuum_claim', [("            require(cl.get(k) is val, 'claim flag ' + k + ' must be ' + str(val))",
   "            require(True or cl.get(k) is val, 'claim flag ' + k + ' must be ' + str(val))")],
  'continuum_claim_true'),
 ('normalization_couples_supports', [("        require(keep_straddling, 'straddling supports dropped from the split')",
   "        require(True or keep_straddling, 'straddling supports dropped from the split')")],
  'straddling_supports_dropped'),
 ('outside_vector_not_ground_state', [("        require(not rec.get('gap_argument_applied_to_phi_out'), 'a gap argument applied to the outside vector')",
   "        require(True or not rec.get('gap_argument_applied_to_phi_out'), 'a gap argument applied to the outside vector')")],
  'outside_gap_argument'),
 ('parameters_declare_metric_weights_window', [("            require(key in p and p[key], 'contract parameters lack ' + key)",
   "            require(True or key in p and p[key], 'contract parameters lack ' + key)")],
  'metric_removed'),
 ('placeholder_span_rejected', [("        require(not (re.search(r'\\s', inner) or '|' in inner or 'e.g.' in inner),",
   "        require(True or not (re.search(r'\\s', inner) or '|' in inner or 'e.g.' in inner),")],
  'angle_span_with_whitespace'),
 ('rate_constant_pair_prefrozen', [("        require(q_reported in (V['q_head'], 'secondary'), 'reported rate must be a frozen pair')",
   "        require(True or q_reported in (V['q_head'], 'secondary'), 'reported rate must be a frozen pair')")],
  'rate_optimized_after_constants'),
 ('region_constant_scales_with_Y', [("        require((1 + pc['t']) ** 2 <= 1 + rate, 'region exponential rate exceeds 1/10^8')",
   "        require(True or (1 + pc['t']) ** 2 <= 1 + rate, 'region exponential rate exceeds 1/10^8')")],
  'hybrid_collection_rate_4t_exceeds_frozen_rate'),
 ('reverse_premise_isolation', [("        require(sorted(invlist) == expected, 'reverse inventory must equal AGENTS.md, the contract and shared_premises exactly')",
   "        require(True or sorted(invlist) == expected, 'reverse inventory must equal AGENTS.md, the contract and shared_premises exactly')"), ("        require(not bad, 'forbidden file in the reverse inventory')",
   "        require(True or not bad, 'forbidden file in the reverse inventory')")],
  'skeptic_triage_added'),
 ('root_n_misuse', [("        require(total == led['L1'] + led['L2'] + led['L3'] + led['L4'] + led['L5'], 'deterministic terms add linearly')",
   "        require(True or total == led['L1'] + led['L2'] + led['L3'] + led['L4'] + led['L5'], 'deterministic terms add linearly')")],
  'root_sum_of_squares_style_combination'),
 ('subsequence_versus_whole_sequence', [("        require(gf == V['gate_fields'], 'gate fields differ from the contract gate_fields_required')",
   "        require(True or gf == V['gate_fields'], 'gate fields differ from the contract gate_fields_required')"), ("        require(gf['whole_sequence_claimed'] is False and gf['common_limit_claimed'] is False, 'no whole-sequence or common-limit claim')",
   "        require(True or gf['whole_sequence_claimed'] is False and gf['common_limit_claimed'] is False, 'no whole-sequence or common-limit claim')")],
  'whole_sequence_claimed_from_per_comparison_bounds'),
 ('tau_scaling_exponent', [("        require(brackets['C_headline'] == V['bracket_C'] and brackets['c_site'] == V['bracket_cs']",
   "        require(True or brackets['C_headline'] == V['bracket_C'] and brackets['c_site'] == V['bracket_cs']")],
  'bracket_narrowed_after_evaluation'),
 ('tier_mixing_rejected', [("        require(tier in ('exact_first_order', 'crude_majorant'), 'BB1 tier must be exact_first_order or crude_majorant')",
   "        require(True or tier in ('exact_first_order', 'crude_majorant'), 'BB1 tier must be exact_first_order or crude_majorant')")],
  'lieb_robinson_tier'),
 ('topology_named', [("        require(top.startswith('trace norm on B(H_Y)'), 'state topology must be the trace norm on B(H_Y)')",
   "        require(True or top.startswith('trace norm on B(H_Y)'), 'state topology must be the trace norm on B(H_Y)')")],
  'wrong_state_topology'),
 ('two_families_named', [("    require(m.get('families') == ['F1', 'F2'], 'families changed')",
   "    require(True or m.get('families') == ['F1', 'F2'], 'families changed')")],
  'one_family_only'),
 ('uniform_in_N_not_in_a', [("            require(ok, 'unqualified uniformity statement in ' + label + ': ' + sentence[:160])",
   "            require(True or ok, 'unqualified uniformity statement in ' + label + ': ' + sentence[:160])")],
  'unqualified_uniform_rate'),
 ('wrong_delta_alpha_hbar_clock', [("        require(rec['clock'].startswith('s=alpha*t_E/hbar (Euclidean), theta=alpha*t/hbar (real time)'), 'round clock')",
   "        require(True or rec['clock'].startswith('s=alpha*t_E/hbar (Euclidean), theta=alpha*t/hbar (real time)'), 'round clock')")],
  'normalized_u_labelled_theta'),
 ('zero_free_region_required', [("        require(not (rec['reduced_density_analyticity_claimed'] and not rec['zero_free_region_proved']),",
   "        require(True or not (rec['reduced_density_analyticity_claimed'] and not rec['zero_free_region_proved']),")],
  'analyticity_claimed_without_zero_free_region'),
]
REV = [
 ('changed_model_relabelled', [("    require(abs(parse_q(pk['tau'])) <= parse_q(pre['tau']['value']), 'coupling above the admitted cap')",
   "    require(True or abs(parse_q(pk['tau'])) <= parse_q(pre['tau']['value']), 'coupling above the admitted cap')")],
  'coupling_above_cap'),
 ('coefficient_decay_not_marginal_decay', [("        require(not (coefficient_difference == 0 and trace_norm_sq > 0), 'state decay inferred from coefficient decay')",
   "        require(True or not (coefficient_difference == 0 and trace_norm_sq > 0), 'state decay inferred from coefficient decay')")],
  'state_decay_from_zero_coefficient_difference'),
 ('coherent_evidence_tampering', [("    require(rc['headline']['q'] == '1/64' and rc['headline']['C_target'] == '1/250000'",
   "    require(True or rc['headline']['q'] == '1/64' and rc['headline']['C_target'] == '1/250000'")],
  'C_target_relaxed'),
 ('common_clock', [("    require(record['coupling_F1'] == record['coupling_F2'], 'the two families at different couplings')",
   "    require(True or record['coupling_F1'] == record['coupling_F2'], 'the two families at different couplings')")],
  'different_couplings'),
 ('cutoff_limit_order', [("    require(order == 'cutoff_L_to_infinity_at_fixed_N_then_bound_in_N', 'N and cutoff limits exchanged')",
   "    require(True or order == 'cutoff_L_to_infinity_at_fixed_N_then_bound_in_N', 'N and cutoff limits exchanged')")],
  'limits_exchanged'),
 ('cutoff_uniform_then_removed', [("    require(rec['constants_depend_on_L'] is False, 'constants depend on the on-site cutoff')",
   "    require(True or rec['constants_depend_on_L'] is False, 'constants depend on the on-site cutoff')")],
  'constants_depend_on_L'),
 ('cutoff_vector_removal', [("    require(method == 'ground_vector_eckart_with_untruncated_gap', 'cutoff removal by eigenvalues only (degenerate counterexample)')",
   "    require(True or method == 'ground_vector_eckart_with_untruncated_gap', 'cutoff removal by eigenvalues only (degenerate counterexample)')")],
  'eigenvalues_only'),
 ('decay_rate_in_N_not_a', [("    require(unit == 'per coarse l-infinity step in N at fixed spacing', 'rate unit is not the coarse step in N at fixed spacing')",
   "    require(True or unit == 'per coarse l-infinity step in N at fixed spacing', 'rate unit is not the coarse step in N at fixed spacing')")],
  'per_fm'),
 ('every_site_coefficient_input', [("    require(rec['sites'] == 'every site of the union volume', 'R-only coefficient input used at far sites')",
   "    require(True or rec['sites'] == 'every site of the union volume', 'R-only coefficient input used at far sites')")],
  'R_only_input_at_far_sites'),
 ('exact_arithmetic_admission', [("        raise AdmissionError('non-exact numeric input rejected: ' + repr(value))",
   '        return Q(value)')],
  'float_input'),
 ('fixture_polymer_identity', [("    require(uses_cardinality_factor is True, 'cardinality factor dropped from the tree majorant (underestimates the cluster sum)')",
   "    require(True or uses_cardinality_factor is True, 'cardinality factor dropped from the tree majorant (underestimates the cluster sum)')")],
  'cardinality_dropped'),
 ('fixture_second_order_propagation', [("    require(claim['order_in_straddling_amplitudes'] == 2, 'first-order propagation claim rejected (exact polynomial is a*b)')",
   "    require(True or claim['order_in_straddling_amplitudes'] == 2, 'first-order propagation claim rejected (exact polynomial is a*b)')")],
  'first_order_claim'),
 ('fixture_split_lipschitz_and_trace', [("    require(all(v == vals[0] for v in vals), 'split charge grows with depth (product of growing region sizes)')",
   "    require(True or all(v == vals[0] for v in vals), 'split charge grows with depth (product of growing region sizes)')")],
  'growing_region_sizes'),
 ('global_fidelity_orthogonality_catastrophe', [("    require(route != 'global_overlap', 'bound through the global overlap of the two box vectors (orthogonality catastrophe)')",
   "    require(True or route != 'global_overlap', 'bound through the global overlap of the two box vectors (orthogonality catastrophe)')"), ("    require(route in ('per_support_telescoping', 'iterated_split'), 'unknown bound route')",
   "    require(True or route in ('per_support_telescoping', 'iterated_split'), 'unknown bound route')")],
  'global_overlap_route'),
 ('global_lipschitz_not_decay', [("    require(provenance not in ('global_lipschitz_fixed_point', 'no_decay_bound_37/6249384', 'density_lipschitz_in_coefficients',",
   "    require(True or provenance not in ('global_lipschitz_fixed_point', 'no_decay_bound_37/6249384', 'density_lipschitz_in_coefficients',"), ("    require(provenance in ('covering_chain_weights_and_site_potential', 'ba1_every_site_vanishing_order'), 'unknown decay provenance')",
   "    require(True or provenance in ('covering_chain_weights_and_site_potential', 'ba1_every_site_vanishing_order'), 'unknown decay provenance')")],
  'fixed_point_lipschitz'),
 ('insufficient_verdict_retained', [("    require(recorded == producer_outcome(flags), 'recorded outcome differs from the executed evidence')",
   "    require(True or recorded == producer_outcome(flags), 'recorded outcome differs from the executed evidence')")],
  'R_form_only_relabelled'),
 ('marginal_locality_constants_explicit', [("    require(lem['p'] == '|I|', 'polynomial p not explicit')",
   "    require(True or lem['p'] == '|I|', 'polynomial p not explicit')")],
  'polynomial_unstated'),
 ('mixed_weight_lemma_proved', [("    require(rec['proved_in_packet'] is True and rec['cited_from'] != 'BA1', 'mixed-weight contraction cited instead of proved')",
   "    require(True or rec['proved_in_packet'] is True and rec['cited_from'] != 'BA1', 'mixed-weight contraction cited instead of proved')")],
  'cited_from_BA1'),
 ('named_construction_not_uniqueness', [('NEGATION = re.compile(r"\\b(not|never|',
   'NEGATION = re.compile(r"\\b(gives|not|never|')],
  'uniqueness_phrase'),
 ('negation_aware_phrase_scan', [("    require(bad == [], 'affirmative forbidden phrasing: ' + (bad[0]['phrase'] if bad else ''))",
   "    require(True or bad == [], 'affirmative forbidden phrasing: ' + (bad[0]['phrase'] if bad else ''))")],
  'thermodynamic_limit'),
 ('no_priority_or_continuum_claim', [("        require(flags.get(k) is False, 'claim flag must be false: ' + k)",
   "        require(True or flags.get(k) is False, 'claim flag must be false: ' + k)")],
  'continuum_true'),
 ('normalization_couples_supports', [("    require(includes_straddling is True, 'straddling supports dropped from the split')",
   "    require(True or includes_straddling is True, 'straddling supports dropped from the split')")],
  'straddling_dropped'),
 ('outside_vector_not_ground_state', [("    require(uses_gap_of_outside_vector is False, 'gap argument applied to the outside vector (it is not a ground state)')",
   "    require(True or uses_gap_of_outside_vector is False, 'gap argument applied to the outside vector (it is not a ground state)')")],
  'gap_argument_on_outside_vector'),
 ('parameters_declare_metric_weights_window', [("        require(k in p and bool(p[k]), 'contract parameters must declare ' + k)",
   "        require(True or k in p and bool(p[k]), 'contract parameters must declare ' + k)"), ("    require('coarse l-infinity' in p['metric'], 'metric not declared')",
   "    require(True or 'coarse l-infinity' in p['metric'], 'metric not declared')")],
  'metric_removed'),
 ('placeholder_span_rejected', [("    require(re.search(r'<[^<>]*(\\s|\\||e\\.g\\.)[^<>]*>', s) is None, 'placeholder span in an exported statement')",
   "    require(True or re.search(r'<[^<>]*(\\s|\\||e\\.g\\.)[^<>]*>', s) is None, 'placeholder span in an exported statement')")],
  'angle_space'),
 ('rate_constant_pair_prefrozen', [("    require(0 <= x < 1, 'lattice sum ratio not below one (split weight too small for the rate)')",
   "    require(True or 0 <= x < 1, 'lattice sum ratio not below one (split weight too small for the rate)')")],
  'split_weight_too_small_for_rate'),
 ('region_constant_scales_with_Y', [("    require(rec.get('Y_factor') == '|Y|', 'region bound without the |Y| factor (R constant reused)')",
   "    require(True or rec.get('Y_factor') == '|Y|', 'region bound without the |Y| factor (R constant reused)')")],
  'R_constant_reused'),
 ('reverse_premise_isolation', [("        require(not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in reverse inputs: ' + f)",
   "        require(True or not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in reverse inputs: ' + f)"), ('    require(sorted(files) == sorted(expected) and len(files) == len(expected),',
   '    require(set(expected) <= set(files),')],
  'forward_bb1_added'),
 ('root_n_misuse', [("    require(combine == 'linear', 'deterministic terms must add linearly (no root sums)')",
   "    require(True or combine == 'linear', 'deterministic terms must add linearly (no root sums)')")],
  'root_sum_of_squares'),
 ('subsequence_versus_whole_sequence', [("    require(obj.get('whole_sequence') is False, 'whole-sequence convergence of states claimed (BB2)')",
   "    require(True or obj.get('whole_sequence') is False, 'whole-sequence convergence of states claimed (BB2)')")],
  'whole_sequence_claimed'),
 ('tau_scaling_exponent', [("    require(bracket[0] <= Q(ratio) <= bracket[1], 'tau/100 ratio outside the prefrozen bracket')",
   "    require(True or bracket[0] <= Q(ratio) <= bracket[1], 'tau/100 ratio outside the prefrozen bracket')")],
  'quadratic_headline'),
 ('tier_mixing_rejected', [("    require(rec['tier'] in TIERS, 'tier outside {exact_first_order, crude_majorant}')",
   "    require(True or rec['tier'] in TIERS, 'tier outside {exact_first_order, crude_majorant}')")],
  'lieb_robinson_tier'),
 ('topology_named', [("    require(t == 'trace norm on B(H_Y)', 'state topology not the trace norm on B(H_Y)')",
   "    require(True or t == 'trace norm on B(H_Y)', 'state topology not the trace norm on B(H_Y)')")],
  'weak_operator'),
 ('two_families_named', [("    require(families == [F1_NAME, F2_NAME], 'the two named families F1 and F2 must both be named')",
   "    require(True or families == [F1_NAME, F2_NAME], 'the two named families F1 and F2 must both be named')")],
  'single_family'),
 ('uniform_in_N_not_in_a', [("        require('fixed spacing' in stripped or 'cutoff' in stripped, 'unqualified uniformity next to a rate')",
   "        require(True or 'fixed spacing' in stripped or 'cutoff' in stripped, 'unqualified uniformity next to a rate')")],
  'unqualified_uniform'),
 ('wrong_delta_alpha_hbar_clock', [("    require(table.get(label) == formula, 'clock label and formula disagree')",
   "    require(True or table.get(label) == formula, 'clock label and formula disagree')")],
  'u_labelled_theta'),
 ('zero_free_region_required', [("        require(zero_free_region_proved is True, 'analyticity of the reduced density without a zero-free region')",
   "        require(True or zero_free_region_proved is True, 'analyticity of the reduced density without a zero-free region')")],
  'reduced_density_analytic'),
]


def phrase_hits(text, forbidden, template=None):
    body = re.sub(r'\s+', ' ', str(text)).strip()
    if template:
        body = body.replace(re.sub(r'\s+', ' ', template).strip(), ' ')
    hits = []
    for clause in [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', body) if c.strip()]:
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                if not NEGATION.search(clause):
                    hits.append({'phrase': phrase, 'clause': clause[:160]})
    return hits


def phrase_scan_tool(paths):
    flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
    done = subprocess.run([sys.executable] + flags + [str(ROOT / PHRASE_SCAN_REL), str(ROOT / CONTRACT_REL)] + [str(p) for p in paths],
                          capture_output=True, text=True, cwd=str(ROOT))
    out = json.loads(done.stdout)
    return done.returncode, sum(len(v) for v in out.values())


# ------------------------------------------------------------------ mutation harness
def mutated_run(direction, edits=(), extra_input=None, contract_append=None):
    src = ROOT / PROD[direction]
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bb1-review-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / PROD[direction]
        dst.mkdir(parents=True)
        shutil.copyfile(src / 'check.py', dst / 'check.py')
        shutil.copyfile(src / 'report.md', dst / 'report.md')
        shutil.copytree(src / 'inputs', dst / 'inputs')
        text = (dst / 'check.py').read_text(encoding='utf-8')
        for old, new in edits:
            if text.count(old) != 1:
                raise ReviewFailure('mutation anchor not unique in %s: %r' % (direction, old[:60]))
            text = text.replace(old, new)
        (dst / 'check.py').write_text(text, encoding='utf-8')
        if extra_input is not None:
            p = dst / 'inputs' / extra_input
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('skeptic mutation fixture\n')
        if contract_append is not None:
            p = dst / 'inputs' / CONTRACT_REL
            p.write_bytes(p.read_bytes() + contract_append)
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(dst / 'check.py'), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(repo))
        outputs = {p.name: p.read_bytes() for p in sorted(out.glob('*.json'))} if out.is_dir() else {}
        last = done.stderr.strip().splitlines()[-1] if done.stderr.strip() else ''
        if any(p.name == '__pycache__' or p.suffix == '.pyc' for p in repo.rglob('*')):
            raise ReviewFailure('interpreter cache written into a mutated copy')
        return done.returncode, outputs, last.replace(tmp, '<tmp>')


def replay(rel_script, optimized):
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bb1-replay-') as tmp:
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if optimized else [])
        done = subprocess.run([sys.executable] + flags + [str(ROOT / rel_script), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(ROOT))
        if done.returncode != 0:
            raise ReviewFailure('replay failed: ' + rel_script + ' ' + done.stderr[-400:])
        return {p.name: sha(p) for p in sorted(out.glob('*.json'))}


def parallel(fn, jobs):
    with ThreadPoolExecutor(max_workers=4) as ex:
        return list(ex.map(fn, jobs))


# ------------------------------------------------------------------ execute
def execute():
    contract_bytes = (ROOT / CONTRACT_REL).read_bytes()
    need(sha_bytes(contract_bytes) == CONTRACT_SHA256, 'contract_sha256_pinned', sha256=CONTRACT_SHA256)
    con = json.loads(contract_bytes)
    pre = con['preregistration']
    tau = F(pre['tau']['value'])
    template = pre['mandatory_sentence_template']
    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings'])
    rc = con['parameters']['rate_constant_pair']
    comparisons = list(con['parameters']['comparisons'])
    gate_fields = dict(pre['gate_fields_required'])
    targets = {'C': F(rc['headline']['C_target']), 'c_site': F(rc['region_form']['c_site_target']),
               'C2': F(rc['secondary']['C_target']), 'c_site2': F(rc['secondary']['c_site_target'])}
    need(targets == {'C': F(1, 250000), 'c_site': F(1, 500000), 'C2': F(1, 20000), 'c_site2': F(1, 40000)}
         and rc['headline']['q'] == rc['region_form']['q'] == '1/64' and rc['secondary']['q'].startswith('151552|tau|')
         and tau == F(1, 10 ** 8) and pre['tau']['signs_evaluated'] == ['+', '-'] and len(comparisons) == 5
         and len(con['controls']) == 37 and con['reverse_premise_isolation'] is True, 'contract_pairs_read',
         targets={k: q(v) for k, v in targets.items()}, comparisons=5, controls=37)

    # 1. closures, inventories, isolation, snapshots
    inventory = sorted(['AGENTS.md', CONTRACT_REL] + list(con['shared_premises']))
    closures, res, inv_lists = {}, {}, {}
    for d, rel in sorted(PROD.items()):
        base = ROOT / rel
        fz_bytes = (base / 'freeze.json').read_bytes()
        if sha_bytes(fz_bytes) != FREEZE_SHA[d]:
            raise ReviewFailure('freeze record changed: ' + d)
        fz = json.loads(fz_bytes)
        files = sorted(p.relative_to(ROOT).as_posix() for p in base.rglob('*') if p.is_file() and p.name != 'freeze.json')
        if any('__pycache__' in f or f.endswith('.pyc') for f in files):
            raise ReviewFailure('interpreter cache inside closure ' + d)
        if files != sorted(fz['sources']) or any(sha(ROOT / f) != h for f, h in fz['sources'].items()):
            raise ReviewFailure('closure differs from freeze.json: ' + d)
        inputs = sorted(p.relative_to(base / 'inputs').as_posix() for p in (base / 'inputs').rglob('*') if p.is_file())
        if inputs != inventory:
            raise ReviewFailure('input inventory differs from AGENTS.md + contract + shared_premises: ' + d)
        if any((base / 'inputs' / f).read_bytes() != (ROOT / f).read_bytes() for f in inputs):
            raise ReviewFailure('snapshot differs from its repository source: ' + d)
        forbidden_present = [f for f in inputs if f.startswith(FORBIDDEN_IN_INPUTS) and f not in SKEPTIC_ALLOWED]
        if forbidden_present:
            raise ReviewFailure('isolation: ' + d + ' ' + json.dumps(forbidden_present))
        if fz['contract_sha256'] != CONTRACT_SHA256 or fz['loop'] != 'BB1' or fz['direction'] != d \
                or fz['normal_optimized_identical'] is not True:
            raise ReviewFailure('freeze identity ' + d)
        if sha(base / 'check.py') != CHECK_SHA[d]:
            raise ReviewFailure('check.py hash ' + d)
        res[d] = json.loads((base / 'output/results.json').read_text())
        inv_lists[d] = inputs
        closures[d] = {'closure_files': len(fz['sources']), 'inputs': len(inputs), 'freeze_json_sha256': FREEZE_SHA[d],
                       'results_sha256': sha(base / 'output/results.json'),
                       'source_manifest_sha256': sha(base / 'output/source-manifest.json'),
                       'check_py_sha256': CHECK_SHA[d], 'report_sha256': sha(base / 'report.md'),
                       'checks': len(res[d]['checks']),
                       'skeptic_files_in_inputs': [f for f in inputs if '/skeptic/' in f]}
    need(len(inventory) == 35 and inv_lists['forward'] == inv_lists['reverse']
         and closures['forward']['closure_files'] == closures['reverse']['closure_files'] == 39,
         'closures_inventories_and_reverse_isolation', closures=closures, inventory=35,
         note='both inputs/ equal AGENTS.md + contract + the 33 shared premises byte for byte (identical lists); the only '
              'skeptic files are the declared gated reviews (Round29 am2.md, Round33 ba1.md and ba2.md); no Round33 BB1/BB2 '
              'producer, skeptic triage, expert, deliberation, plan, brief, panel or findings file in either inventory')
    need(res['forward']['check_py_sha256_recorded_before_evaluation'] == CHECK_SHA['forward']
         and check_by_id(res['reverse'], 'check_py_sha256_recorded_before_evaluation')['check_py_sha256'] == CHECK_SHA['reverse'],
         'check_py_sha256_recorded_before_evaluation_matches_frozen')

    # 2. replays: both producers and the skeptic pre-comparison program, normal and -O
    replays = {}
    for d, rel in sorted(PROD.items()):
        frozen = {p.name: sha(p) for p in sorted((ROOT / rel / 'output').glob('*.json'))}
        runs = dict(zip(('normal', 'optimized'), parallel(lambda m: replay(rel + '/check.py', m == 'optimized'), ('normal', 'optimized'))))
        if runs['normal'] != frozen or runs['optimized'] != frozen:
            raise ReviewFailure('producer replay differs from frozen output: ' + d)
        replays[d] = {'frozen_outputs': frozen, 'normal_and_optimized_byte_identical_to_frozen': True}
    pre_fz_bytes = (ROOT / PRE_FREEZE_REL).read_bytes()
    pre_fz = json.loads(pre_fz_bytes)
    if sha_bytes(pre_fz_bytes) != PRE_FREEZE_SHA or pre_fz['contract_sha256'] != CONTRACT_SHA256 \
            or any(sha(ROOT / f) != h for f, h in pre_fz['files'].items()):
        raise ReviewFailure('skeptic pre-comparison package changed after its freeze')
    pre_runs = dict(zip(('normal', 'optimized'), parallel(lambda m: replay(PRE_CHECK_REL, m == 'optimized'), ('normal', 'optimized'))))
    if pre_runs['normal'] != {'results.json': sha(ROOT / PRE_RESULTS_REL)} or pre_runs['optimized'] != pre_runs['normal']:
        raise ReviewFailure('skeptic pre-comparison replay differs')
    replays['skeptic_pre_comparison'] = {'results_sha256': sha(ROOT / PRE_RESULTS_REL), 'freeze_record_sha256': PRE_FREEZE_SHA,
                                         'files_unchanged': sorted(pre_fz['files']),
                                         'normal_and_optimized_byte_identical_to_frozen': True}
    need(True, 'replays_byte_identical', replays=replays)

    # 3. values: every producer constant re-derived; predictions; binding
    need(validate_forward(res['forward'], tau, template, comparisons, gate_fields), 'forward_values_reproduced_exactly',
         note='R form, region form, five comparisons x two signs, secondary pair, crude tier (headline and secondary), '
              'KP constants (a=taubar^2, Gamma, loss w e^{4b}, S_{2/3}=725, S_{1/2}=147), kappa_0 per tier, union form 2C '
              '(labelled), tau ratios; F09, F12, F13 of the forward report')
    need(validate_reverse(res['reverse'], tau, template, comparisons, gate_fields), 'reverse_values_reproduced_exactly',
         note='statement C, region c_site, ten comparison rows (each Q_L and untruncated at fixed N), secondary pair, crude '
              'tier (headline and secondary), beta*=c1/(1-c2), per-level factor 8t_W=196/3160809, S_lambda=2169/343, tau '
              'ratios including the labelled crude ratio; R11, R13 of the reverse report; the reverse exports comparison '
              'names truncated to 80 characters, each a unique prefix of one contract comparison')
    cc = all_constants(tau)
    cs100 = all_constants(tau / 100)
    fw, fw2, rv, rv2 = cc['fwd'], cc['fwd2'], cc['rev'], cc['rev2']
    K, K2 = cc['inputs']['K'], cc['inputs']['K2']
    pre_res = json.loads((ROOT / PRE_RESULTS_REL).read_text())
    pc = {k: F(v['value']) for k, v in pre_res['constants'].items()}
    near = 2 * K * (1 + RB)
    rel = lambda a, b: abs(a - b) / b
    need(K == F(49, 111790368) and K2 == F(49, 10202112) and cc['inputs']['Kc'] == F(296, 390625) and cc['inputs']['Kc2'] == F(1, 128)
         and near == F(3185, 3577291776) and near < pc['C_b_every_site'] < rv['C'] < fw['C']
         and rel(fw['C'], pc['C_b_every_site']) < F(2, 10000) and rel(rv['C'], pc['C_b_every_site']) < F(1, 10000)
         and 2 * K < pc['c_site_b'] < rv['c_site'] < fw['c_site'] and rel(fw['c_site'], pc['c_site_b']) < F(2, 10000)
         and pc['C_secondary_every_site'] < fw2['C'] < rv2['C'] and pc['c_site_secondary'] < fw2['c_site'] < rv2['c_site']
         and rel(rv2['C'], pc['C_secondary_every_site']) < F(1, 100) and rel(rv2['c_site'], pc['c_site_secondary']) < F(1, 100)
         and pc['C_crude_every_site'] < cc['rev_crude']['C'] < cc['fwd_crude']['C'] and pc['C_crude_every_site'] > targets['C'],
         'producers_against_pre_comparison_predictions',
         near_term_2K_1_plus_q=q(near),
         C={'skeptic': preview(pc['C_b_every_site']), 'forward': preview(fw['C']), 'reverse': preview(rv['C']),
            'forward_rel_diff': preview(rel(fw['C'], pc['C_b_every_site'])), 'reverse_rel_diff': preview(rel(rv['C'], pc['C_b_every_site']))},
         c_site={'skeptic': preview(pc['c_site_b']), 'forward': preview(fw['c_site']), 'reverse': preview(rv['c_site'])},
         secondary={'skeptic': [preview(pc['C_secondary_every_site']), preview(pc['c_site_secondary'])],
                    'forward': [preview(fw2['C']), preview(fw2['c_site'])], 'reverse': [preview(rv2['C']), preview(rv2['c_site'])]},
         crude_C={'skeptic': preview(pc['C_crude_every_site']), 'forward': preview(cc['fwd_crude']['C']),
                  'reverse': preview(cc['rev_crude']['C'])},
         reason='all three share the near term 2K(1+q) from the every-site input (q^N at 0, q^(N-1) at e_z) and differ only '
                'in the far-site majorant: skeptic truncated-correlation recursion (weight 64, A=2M/(eps e-2M)), forward '
                'KP/Y-cluster kappa_0 with v=128, reverse covering chains with lambda=1/512; every value is a valid upper '
                'bound of its own proof')
    need(pc['C_b_R_only'] > 19 * fw['C'] / 10 and pc['C_b_R_only'] > 19 * rv['C'] / 10, 'R3_both_use_q_to_the_N_at_u_0',
         skeptic_R_only_input=preview(pc['C_b_R_only']),
         note='both packets charge the site 0 at q^N through the every-site form (b) (factor 1+q), not the R-only gate '
              'statement (factor 2 at exponent N-1)')
    bind = {'C': max(fw['C'], rv['C']), 'c_site': max(fw['c_site'], rv['c_site']),
            'C2': max(fw2['C'], rv2['C']), 'c_site2': max(fw2['c_site'], rv2['c_site'])}
    need(bind['C'] == fw['C'] and bind['c_site'] == fw['c_site'] and bind['C2'] == rv2['C'] and bind['c_site2'] == rv2['c_site']
         and all(bind[k] <= targets[k] for k in bind) and rv['C'] <= bind['C'] and rv['c_site'] <= bind['c_site'],
         'binding_larger_valid_constant_per_quantity',
         C=q(bind['C']), c_site=q(bind['c_site']), C2=q(bind['C2']), c_site2=q(bind['c_site2']),
         margins={k: preview(targets[k] / bind[k]) for k in bind},
         note='headline C and c_site bind the polymer_kp values (larger); the secondary pair binds the iterated_split values '
              '(larger); every bound value is at least the self-contained iterated_split value of the same quantity, so '
              'each bound value is proved by the reverse route alone as well')
    ratios_bind = {'C': fw['C'] / cs100['fwd']['C'], 'c_site': fw['c_site'] / cs100['fwd']['c_site'],
                   'C2': rv2['C'] / cs100['rev2']['C'], 'c_site2': rv2['c_site'] / cs100['rev2']['c_site'],
                   'q2': cc['inputs']['q2'] / cs100['inputs']['q2']}
    need(all(F(95) <= ratios_bind[k] <= F(105) for k in ('C', 'c_site'))
         and all(F(99, 100) <= ratios_bind[k] <= F(101, 100) for k in ('C2', 'c_site2')) and ratios_bind['q2'] == 100
         and all(v > targets['C'] for v in (cc['fwd_crude']['C'], cc['rev_crude']['C'], cc['rev_crude']['c_site'])),
         'bound_constants_scaling_and_crude_tier', ratios={k: preview(v) for k, v in ratios_bind.items()},
         crude={'forward_C': preview(cc['fwd_crude']['C']), 'reverse_C': preview(cc['rev_crude']['C']),
                'reverse_c_site': preview(cc['rev_crude']['c_site']),
                'forward_c_site_not_in_frozen_form': preview(cc['fwd_crude']['c_site'])})
    t_f = fw['t']
    need((1 + t_f) ** 2 <= 1 + F(1, 10 ** 8) and (1 + cc['fwd_crude']['t']) ** 2 > 1 + F(1, 10 ** 8)
         and fw['a'] <= 2 * F(1, 1001) and fw2['a'] <= 2 * F(1, 1001) and fw['a'] == fw['taubar'] ** 2
         and fw['loss'] <= fw['w_max'] and fw2['loss'] <= fw2['w_max'] and fw['v'] <= fw['w'] and fw['v'] * RB == 2
         and 28 * 1024 * tau * G_R <= RB and 28 * cc['inputs']['W2'] * tau * G_R <= RB and rv['lambda'] < RB
         and rv2['lambda'] < cc['inputs']['q2'] and 8 * rv['tW'] == F(196, 3160809) and rv['S'] == F(2169, 343)
         and rv2['S'] == 147 and fw['S_vw'] == 725 and fw['S_qv'] == 147, 'R6_R7_R8_side_conditions',
         forward={'(1+t)^2-1': preview((1 + t_f) ** 2 - 1), 'a': preview(fw['a']), 'loss': preview(fw['loss']),
                  'Gamma': preview(fw['Gamma'])},
         reverse={'t0': q(rv['t0']), 'tW': q(rv['tW']), 'beta_star': q(rv['beta']), 'per_level_8tW': '196/3160809'},
         note='R7: the forward region form absorbs (1+t)^{2|Y|} into e^{|Y|/10^8} because 2t+t^2<10^-8 at every d_Y; the '
              'reverse has eta=0 and no exponential; R8: the crude anchored norm gives (1+t)^2-1 above 10^-8, so the forward '
              'reports its crude c_site outside the frozen form, while the reverse crude c_site is in the frozen form (eta=0) '
              'and fails; R6: forward normalization through vacuum probabilities pi<=1 and KP-truncated differences, reverse '
              'through orthogonality at J (Z>=n^2) and covering-only records with Cov<=t_0 and per-site charging; all '
              'constants independent of N and L')
    excerpt = (ROOT / EXCERPT_REL).read_bytes()
    etext = excerpt.decode('utf-8')
    ftext = (ROOT / PROD['forward'] / 'report.md').read_text(encoding='utf-8')
    tiers = {'headline': fw, 'secondary': fw2, 'headline_crude': cc['fwd_crude']}
    hard_core = all(abs(1 + zeta) <= 1 for zeta in (0, -1))
    need(sha_bytes(excerpt) == EXCERPT_SHA and EXCERPT_PDF_SHA in etext and all(etext.count(t) == 1 for t in EXCERPT_ANCHORS)
         and all(ftext.count(t) == 1 for t in FORWARD_KP_ANCHORS)
         and all(EXCERPT_REL not in inv_lists[d] for d in PROD) and hard_core
         and all(v_['a'] == v_['taubar'] ** 2 and v_['a'] <= 2 * F(1, 1001) and 1 <= v_['v'] <= v_['w'] for v_ in tiers.values()),
         'kp_citation_checked_against_committed_excerpt',
         excerpt={'path': EXCERPT_REL, 'sha256': EXCERPT_SHA, 'pdf_sha256': EXCERPT_PDF_SHA,
                  'status': 'committed after both BB1 freezes (cca0584); not in either producer inventory; not a premise'},
         dictionary={'polymers': 'counting measure times w(gamma) on the finite polymer set of Lambda\'',
                     'zeta': 'hard core: -1 if supports meet, else 0 (so |1+zeta|<=1 identically)', 'c': '0',
                     'b': 'd(gamma)=ln(v) sum_{K in gamma} diam K >= 0 (v>=1)', 'a': 'a|supp gamma| with a=taubar^2',
                     'test_sets': 'finite site sets adjoined as atoms of mu-mass 0 with a(S)=a|S|'},
         side_conditions={k: {'a': q(v_['a']), 'a_le_2_over_1001': True, 'v': q(v_['v']), 'w': q(v_['w'])} for k, v_ in tiers.items()},
         result='Ueltschi (16) is the forward hypothesis; Theorem 1 gives Z(Lambda\')=exp(sum Phi^T) for every Lambda\'; (19) gives '
                'sum_{X incompatible with gamma}|Phi^T(X)|e^{d(X)}<=a(gamma) with the same weight e^{d(X)}=prod e^{d(gamma\')} '
                '(mu_b weighting) and an incompatibility count of at least one; the test-set clause is the mass-zero-atom instance; '
                'Corollary 6.3 and Lemma 6.4 add only the forward\'s own elementary steps; no missing factor '
                '(research/round33/skeptic/bb1-kp-repair.md)')
    rows = pre_res['coefficient_input']['every_site_rows']
    fixed_n = [r_ for r_ in rows if r_['smaller'].split('_')[1] == r_['larger'].split('_')[1]]
    gv = pre_res['coefficient_input']['general_volumes']
    need(len(rows) == 27 and all(r_['min_source_norm_inf'] >= int(r_['smaller'].split('_')[1]) for r_ in rows)
         and sorted((int(r_['smaller'].split('_')[1]), r_['source_faces']) for r_ in fixed_n) == [(2, 616), (3, 1344), (4, 2352)]
         and all(28 * n_ * (5 * n_ + 1) == sf for n_, sf in ((2, 616), (3, 1344), (4, 2352)))
         and all(v['min_source_norm_inf'] >= int(k.split('_')[0][2:]) for k, v in gv.items()),
         'fixed_N_and_general_volume_source_distances',
         note='the skeptic pre-comparison enumeration (27 centred pairs including the fixed-N F1-versus-F2 pairs with '
              '28N(5N+1) extra faces, and one-prescription cuboids) has every source site at l-infinity norm at least N; '
              'both producers prove the same common-core lemma (forward Lemma 8.6, reverse Lemma B5) for any two volumes '
              'of either prescription containing Lambda_N and run the density lemma once on the union volume, so c3 and c5 '
              'are proved by the general theorem (forward Theorem 8.1 with 9.1 and Corollaries 9.2-9.3; reverse Theorems B6 '
              'and 5.1), each with its own enumeration audit')
    fx = own_fixtures()
    need(fx['R07_identity'] is True and fx['Z_at_least_n2'] is True and fx['covering_only'] is True
         and fx['families_meeting_J'] > fx['covering_families'] > 0 and all(v['identity'] is True for v in fx['F06'].values())
         and fx['P3_coverings'] is True, 'own_exact_fixtures_split_and_cluster_identities', fixtures=fx,
         model_is_finite_graph=True, transfers_to_aq=False,
         note='a five-site qubit chain with eight supports; changed support J={2,3} (two sites), so non-covering families '
              'exist and cancel exactly under the contraction with delta_J; the Y-cluster formula with vacuum '
              'probabilities in (0,1] reproduces rho_Y for Y={0} and {0,1}; the covering sums are at most t_0')
    card = all((d_ + 1) ** 3 <= 8 * 2 ** d_ for d_ in range(0, 401))
    lat = all(sum((24 * r_ * r_ + 2) * F(x) ** r_ for r_ in range(1, 200)) + 1 <= S(x) for x in (F(2, 3), F(1, 2), F(1, 8)))
    need(card and lat and S(F(2, 3)) == 725 and S(F(1, 2)) == 147 and S(F(1, 8)) == F(2169, 343), 'cardinality_charge_and_lattice_sums',
         note='|I|<=(diam I+1)^3<=8*2^{diam I} for diameters 0..400; the closed-form lattice sums dominate their partial sums')

    # 4. damaged packets rejected by this review's validator
    def damaged(direction, fn):
        pk = json.loads(json.dumps(res[direction]))
        fn(pk)
        v = validate_forward if direction == 'forward' else validate_reverse
        return lambda: v(pk, tau, template, comparisons, gate_fields)

    def setp(path, value):
        def fn(pk):
            node = pk
            for key in path[:-1]:
                node = node[key]
            node[path[-1]] = value(node[path[-1]]) if callable(value) else value
        return fn

    def r_row(pk):
        for row in pk['headline']['comparisons']:
            if row['comparison'].startswith('F1 versus F2') and row['sign'] == '-':
                row['untruncated_at_fixed_N'] = False

    def r_ratio(pk):
        check_by_id(pk, 'tau_scaling_every_headline_constant')['ratios']['C_headline']['exact'] = '100'

    def r_drop_row(pk):
        pk['headline']['comparisons'] = [row for row in pk['headline']['comparisons'] if not row['comparison'].startswith('two finite')]
    c3 = comparisons[2]
    dmg = [('forward', 'headline_C_halved', setp(['headline', 'R_form', 'C'], lambda v: q(F(v) / 2)), 'R_form C'),
           ('forward', 'minus_sign_c_site_doubled', setp(['headline', 'region_form', 'per_sign', '-', 'c_site'], lambda v: q(F(v) * 2)), 'per-sign c_site'),
           ('forward', 'crude_marked_met', setp(['headline', 'crude_tier', 'meets_C_target'], True), 'crude tier'),
           ('forward', 'kp_a_halved', setp(['headline', 'kp', 'headline', 'a'], lambda v: q(F(v) / 2)), 'kp constants'),
           ('forward', 'fixed_N_secondary_replaced_by_reverse', setp(['headline', 'comparisons', c3, 'secondary', 'c_site'], q(rv2['c_site'])), 'comparison not reproduced'),
           ('forward', 'q_secondary_ratio_99', setp(['headline', 'scaling', 'q_secondary'], '99'), 'scaling'),
           ('forward', 'template_trimmed', setp(['mandatory_sentence'], template.replace('not uniqueness of any ground state, ', '')), 'mandatory sentence'),
           ('reverse', 'fixed_N_untruncated_false', r_row, 'regime flags'),
           ('reverse', 'one_prescription_rows_dropped', r_drop_row, 'five comparisons'),
           ('reverse', 'C_replaced_by_skeptic_prediction', setp(['headline', 'statement_constants', 'C', 'exact'], q(pc['C_b_every_site'])), 'statement C'),
           ('reverse', 'secondary_c_site_scaled', setp(['headline', 'secondary_pair_labelled', 'c_site', 'exact'], lambda v: q(F(v) * 99 / 100)), 'secondary'),
           ('reverse', 'crude_c_site_changed', setp(['headline', 'crude_tier', 'c_site', 'exact'], q(2 * K)), 'crude tier'),
           ('reverse', 'eta_nonzero', setp(['headline', 'marginal_locality_lemma', 'eta'], '1/1000'), 'lemma constants'),
           ('reverse', 'C_ratio_100', r_ratio, 'ratio not reproduced'),
           ('reverse', 'template_trimmed', setp(['mandatory_sentence_template'], template.replace('not uniqueness of any ground state, ', '')), 'mandatory sentence')]
    rows_d = []
    for d, label, fn, reason in dmg:
        if not rejects(damaged(d, fn), reason):
            raise ReviewFailure('damaged packet accepted: ' + label)
        rows_d.append({'producer': d, 'mutation': label, 'rejected_for': reason})
    need(len(rows_d) == 15, 'damaged_packets_rejected_by_review_validator', rows=rows_d)

    # 5. source-edit runs on temporary copies
    runs = []
    unmutated = parallel(lambda d: (d, mutated_run(d)), ('forward', 'reverse'))
    for d, (code, outs, last) in unmutated:
        frozen = {p.name: p.read_bytes() for p in sorted((ROOT / PROD[d] / 'output').glob('*.json'))}
        if code != 0 or outs != frozen:
            raise ReviewFailure('unmutated copy does not reproduce the frozen output: ' + d)
        runs.append({'producer': d, 'edit': 'unmutated copy', 'outcome': 'reproduces frozen output byte for byte'})
    label_sets = {}
    for d in ('forward', 'reverse'):
        labels = {}
        for c in res[d]['checks']:
            rm = c.get('rejected_mutations')
            if rm:
                labels[c['id']] = sorted(rm)
        label_sets[d] = labels
    controls = list(con['controls'])
    jobs = []
    for d, table in (('forward', FWD), ('reverse', REV)):
        if sorted(t[0] for t in table) != sorted(controls):
            raise ReviewFailure('weakening table does not cover the 37 controls: ' + d)
        for cid, edits, label in table:
            if label not in label_sets[d].get(cid, []):
                raise ReviewFailure('expected label is not a mutation of the control: %s %s %s' % (d, cid, label))
            jobs.append((d, cid, edits, label))
    outcomes = parallel(lambda j: mutated_run(j[0], edits=j[2]), jobs)
    for (d, cid, edits, label), (code, outs, last) in zip(jobs, outcomes):
        m = re.search(r'damaging mutation accepted: (\S+)$', last)
        if code == 0 or outs or m is None or m.group(1) != label:
            raise ReviewFailure('weakening not caught at the intended control: %s %s (%s)' % (d, cid, last[-160:]))
        runs.append({'producer': d, 'control': cid, 'edit': 'validator weakened (%d anchor%s)' % (len(edits), 's' if len(edits) > 1 else ''),
                     'aborted_with': 'damaging mutation accepted: ' + label})
    input_edits = [
        ('forward', 'contract byte edit without rehash', dict(contract_append=b' ')),
        ('reverse', 'contract byte edit without rehash', dict(contract_append=b' ')),
        ('forward', 'undeclared skeptic file in inputs', dict(extra_input='research/round33/skeptic/bb1-triage.md')),
        ('reverse', 'undeclared skeptic file in inputs', dict(extra_input='research/round33/skeptic/bb1-triage.md')),
        ('reverse', 'forward BB1 report in inputs', dict(extra_input='research/round33/forward/bb1/report.md')),
        ('forward', 'BB2 reverse report in inputs', dict(extra_input='research/round33/reverse/bb2/report.md')),
    ]
    edit_out = parallel(lambda e: mutated_run(e[0], **e[2]), input_edits)
    for (d, label, kw), (code, outs, last) in zip(input_edits, edit_out):
        if code == 0 or outs:
            raise ReviewFailure('input edit not caught: %s %s' % (d, label))
        runs.append({'producer': d, 'edit': label, 'outcome': 'aborted without output'})
    n_weak = sum(1 for r_ in runs if 'control' in r_)
    need(n_weak == 74, 'source_edit_runs', weakenings=n_weak, unmutated=2, input_edits=len(input_edits), runs=runs,
         note='each weakening inserts "True or " into the require(...) sites that reject that control\'s first damaging '
              'mutation (two sites where two validators guard it), or, for exact arithmetic, returns a Fraction of the '
              'float instead of raising, or, for negation-aware scans, adds a non-negation word to the negation lexicon, or, '
              'for the reverse isolation control, relaxes inventory equality to inclusion; every run aborts naming a '
              'mutation of the intended control')

    # 6. reports: phrase scan, template span, checker counts
    scan = {}
    report_paths = [ROOT / PROD[d] / 'report.md' for d in ('forward', 'reverse')]
    code, tool_hits = phrase_scan_tool(report_paths)
    for d in ('forward', 'reverse'):
        text = (ROOT / PROD[d] / 'report.md').read_text(encoding='utf-8')
        hits = phrase_hits(text, forbidden, template)
        count = text.count(template)
        if hits or count != 1:
            raise ReviewFailure('report scan or template span: ' + d)
        scan[d] = {'affirmative_hits': 0, 'template_spans': 1}
    fwd_ctrl = [c for c in res['forward']['checks'] if c['id'] in controls]
    rev_ctrl = [c for c in res['reverse']['checks'] if c['id'] in controls]
    n_f = sum(len(c['rejected_mutations']) for c in fwd_ctrl)
    n_r = sum(len(c['rejected_mutations']) for c in rev_ctrl)
    need(code == 0 and tool_hits == 0 and len(fwd_ctrl) == 37 == len(rev_ctrl) and all(c.get('rejected_mutations') for c in fwd_ctrl + rev_ctrl)
         and res['forward']['rejected_mutation_total'] == 107 == n_f and res['reverse']['damaging_mutations_total'] == 132 == n_r
         and len(res['forward']['checks']) == 51 and len(res['reverse']['checks']) == 78,
         'reports_scanned_and_checker_counts', scan=scan, phrase_scan_tool={'exit_code': 0, 'affirmative_hits': 0},
         forward={'checks': 51, 'controls': 37, 'rejected_mutations': 107},
         reverse={'checks': 78, 'controls': 37, 'rejected_mutations': 132})
    need(res['forward']['gate_fields'] == gate_fields == res['reverse']['gate_fields'], 'gate_fields_equal_contract',
         fields=sorted(gate_fields))

    # 7. the review statement, limitations and exported values
    vals = {'fC': fw['C'], 'fc': fw['c_site'], 'rC': rv['C'], 'rc': rv['c_site'], 'fC2': fw2['C'], 'fc2': fw2['c_site'],
            'rC2': rv2['C'], 'rc2': rv2['c_site'], 'fCc': cc['fwd_crude']['C'], 'rCc': cc['rev_crude']['C'],
            'ratio_C': ratios_bind['C'], 'ratio_c': ratios_bind['c_site'], 'ratio_C2': ratios_bind['C2'], 'ratio_c2': ratios_bind['c_site2']}
    statement = supported_statement(template, vals)
    lims = limitations()
    hits = phrase_hits(statement, forbidden, template) + [h for x in lims for h in phrase_hits(x, forbidden, template)]
    norm = lambda s_: re.sub(r'\s+', ' ', s_).strip()
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bb1-scan-') as tmp:
        p1, p2 = Path(tmp) / 'statement.txt', Path(tmp) / 'limitations.txt'
        p1.write_text(statement + '\n')
        p2.write_text('\n'.join(lims) + '\n')
        code2, tool_hits2 = phrase_scan_tool([p1, p2])
    need(hits == [] and code2 == 0 and tool_hits2 == 0 and norm(template) in norm(statement) and statement.count(template) == 1
         and not any(norm(template) in norm(x) for x in lims), 'review_statement_scanned_template_one_span',
         phrase_scan_tool={'exit_code': 0, 'affirmative_hits': 0})
    admitted = admitted_values(vals, targets)
    return {
        'loop': 'BB1', 'stage': 'post_comparison', 'reviewer': 'skeptic (model agent, correlated ancestry)',
        'human_author': 'Hruday N M (BUNZEEY)', 'contract_sha256': CONTRACT_SHA256,
        'verdict': 'accepted_within_scope', 'sub_label': 'boundary_decay_rate_only',
        'secondary_sub_labels': ['static_not_dynamic'], 'blocking_issues': [],
        'supported_statement': statement, 'limitations': lims, 'gate_fields': gate_fields,
        'recommended_bound': recommended_bound(vals, targets, cc, ratios_bind),
        'admitted_values': admitted,
        'proof_constants': {
            'forward_polymer_kp': {'t': q(fw['t']), 'taubar': q(fw['taubar']), 'a': q(fw['a']), 'Gamma': q(fw['Gamma']),
                                   'loss_w_e4b': q(fw['loss']), 'kappa0': q(fw['kappa0']), 'w': q(fw['w']), 'v': q(fw['v']),
                                   'S_v_over_w': q(fw['S_vw']), 'S_1_over_qv': q(fw['S_qv'])},
            'reverse_iterated_split': {'t0': q(rv['t0']), 'tW': q(rv['tW']), 'c1': q(rv['c1']), 'c2': q(rv['c2']),
                                       'beta_star': q(rv['beta']), 'lambda': q(rv['lambda']), 'S_lambda': q(rv['S']),
                                       'W': '1024', 'per_level_factor_8tW': q(8 * rv['tW'])},
            'inputs': {'K': q(K), 'K2': q(K2), 'K_crude': q(cc['inputs']['Kc']), 'K2_crude': q(cc['inputs']['Kc2'])}},
        'closures': closures, 'replays': replays,
        'continuum_claim': False, 'scientific_priority_verified': False, 'weak_coupling_claim': False,
        'uniqueness_of_ground_state_claimed': False, 'whole_sequence_claimed': False, 'common_limit_claimed': False,
        'checks': CHECKS,
        'previews': {'bound_C': preview(fw['C']), 'bound_c_site': preview(fw['c_site']), 'bound_C2': preview(rv2['C']),
                     'bound_c_site2': preview(rv2['c_site']), 'reverse_C': preview(rv['C']), 'reverse_c_site': preview(rv['c_site']),
                     'forward_C2': preview(fw2['C']), 'forward_c_site2': preview(fw2['c_site']),
                     'margin_C': preview(targets['C'] / fw['C']), 'margin_c_site': preview(targets['c_site'] / fw['c_site'])},
    }


def leaf(form, sign, regime, vals, targets):
    both = 'the same constant for both signs (the -tau value replays the same |tau| formula)'
    reg = ('in each on-site cutoff space Q_L, constant independent of L' if regime == 'each_Q_L_uniform_in_L'
           else 'untruncated finite-box ground vectors at fixed N (AV1 F20-F23; AY1 for F2), the bound passing through the closed ball')
    if form == 'R':
        return {'bound': '||rho^box1_R - rho^box2_R||_1 <= C q^(N-1), q=1/64, R={0,e_z}', 'sign': sign, 'regime': reg,
                'C': q(vals['fC']), 'C_preview': preview(vals['fC']), 'route': 'polymer_kp', 'tier': 'exact_first_order',
                'target': '1/250000', 'meets_target': vals['fC'] <= targets['C'],
                'also_certified_by': {'route': 'iterated_split', 'C': q(vals['rC']), 'C_preview': preview(vals['rC'])},
                'secondary_labelled': {'q': '151552|tau|', 'C2': q(vals['rC2']), 'C2_preview': preview(vals['rC2']),
                                       'route': 'iterated_split', 'target': '1/20000', 'meets_target': vals['rC2'] <= targets['C2'],
                                       'also_certified_by': {'route': 'polymer_kp', 'C2': q(vals['fC2'])}},
                'note': both}
    return {'bound': '||rho^box1_Y - rho^box2_Y||_1 <= c_site |Y| e^{|Y|/10^8} q^{d_Y}, d_Y = N - max_{y in Y}|y|_inf, every '
                     'finite complete-factor region Y inside Lambda_N', 'sign': sign, 'regime': reg,
            'c_site': q(vals['fc']), 'c_site_preview': preview(vals['fc']), 'route': 'polymer_kp', 'tier': 'exact_first_order',
            'target': '1/500000', 'meets_target': vals['fc'] <= targets['c_site'],
            'also_certified_by': {'route': 'iterated_split', 'c_site': q(vals['rc']), 'c_site_preview': preview(vals['rc']),
                                  'stronger_form': 'c_site sum_{y in Y} q^(N-|y|_inf), no exponential factor (eta=0)'},
            'secondary_labelled': {'q': '151552|tau|', 'c_site2': q(vals['rc2']), 'c_site2_preview': preview(vals['rc2']),
                                   'route': 'iterated_split', 'target': '1/40000', 'meets_target': vals['rc2'] <= targets['c_site2'],
                                   'also_certified_by': {'route': 'polymer_kp', 'c_site2': q(vals['fc2'])}},
            'note': both}


def admitted_values(vals, targets):
    out = {}
    for cid in COMP_IDS:
        entry = {'comparison': COMP_SHORT[cid], 'N': 'the smaller box size, N at least 2'}
        for form in ('R', 'region'):
            entry[form] = {regime: {sign: leaf(form, sign, regime, vals, targets) for sign in ('+', '-')}
                           for regime in ('each_Q_L_uniform_in_L', 'untruncated_fixed_N')}
        if cid == 'c5':
            entry['union_route_labelled_only'] = {'C': q(2 * vals['fC']), 'c_site': q(2 * vals['fc']),
                                                  'note': 'each volume against the union, then the triangle inequality; labelled, not bound'}
            entry['reading'] = ('for F2 volumes other than centred cubes the AY1 itemization H1-H5 is applied as a local reading '
                                '(both producers; reviewed as correct), not as a gated statement')
        if cid == 'c3':
            entry['source'] = 'the 28N(5N+1) extra F2 faces on the outer layer of Lambda_N (616, 1344, 2352 at N=2,3,4)'
        out[cid] = entry
    return out


def recommended_bound(vals, targets, cc, ratios):
    return {
        'rule': 'the larger valid constant per quantity is bound; the other route is labelled',
        'C': {'q': '1/64', 'value': q(vals['fC']), 'preview': preview(vals['fC']), 'route': 'polymer_kp', 'tier': 'exact_first_order',
              'ba1_input': 'gate bound value K=49/111790368 through the every-site form (b), proved in both packets',
              'target': '1/250000', 'margin_preview': preview(targets['C'] / vals['fC']), 'tau_ratio_preview': preview(ratios['C']),
              'also_certified_by': {'route': 'iterated_split', 'value': q(vals['rC']), 'preview': preview(vals['rC'])}},
        'c_site': {'q': '1/64', 'value': q(vals['fc']), 'preview': preview(vals['fc']), 'route': 'polymer_kp', 'tier': 'exact_first_order',
                   'form': 'c_site |Y| e^{|Y|/10^8} q^{d_Y}', 'target': '1/500000',
                   'margin_preview': preview(targets['c_site'] / vals['fc']), 'tau_ratio_preview': preview(ratios['c_site']),
                   'also_certified_by': {'route': 'iterated_split', 'value': q(vals['rc']), 'preview': preview(vals['rc'])}},
        'secondary_labelled': {'q': '151552|tau| (592/390625 at the cap)', 'K2': '49/10202112',
                               'C2': q(vals['rC2']), 'C2_preview': preview(vals['rC2']), 'c_site2': q(vals['rc2']),
                               'c_site2_preview': preview(vals['rc2']), 'route': 'iterated_split', 'tier': 'exact_first_order',
                               'targets': ['1/20000', '1/40000'], 'tau_ratios_preview': [preview(ratios['C2']), preview(ratios['c_site2'])],
                               'also_certified_by': {'route': 'polymer_kp', 'C2': q(vals['fC2']), 'c_site2': q(vals['fc2'])}},
        'crude_majorant_reported': {'C_forward': q(vals['fCc']), 'C_reverse': q(vals['rCc']),
                                    'c_site_reverse': q(cc['rev_crude']['c_site']), 'meets_C_target': False,
                                    'note': 'the forward crude c_site has no frozen-form value ((1+t)^2-1 above 10^-8)'},
        'q2_tau_ratio': '100',
    }


def supported_statement(template, v):
    return ('In the AM2/AQ1 zero-selected patterned family (model AQ_patterned_zero_selected: SU(2) Kogut-Susskind form '
            'on Z^3 at fixed spacing, coarse 24-link factors, selected triple exactly (0,0,0) with Haar product reference, '
            '21 omitted faces per anchor entering as -(tau/3)W_f in normalized units delta=alpha/8; both signs '
            '|tau|<=10^-8; AM2 creation expansion with J<=28|tau|, R=1/64, G(t)=16e^{8t}(1+10t); cover R={0,e_z}; '
            'coarse l-infinity metric with star diameter 1; trace norm on B(H_Y)), with the named construction families '
            'F1 = AQ1 centered whole-star boxes Lambda_N=[-N,N]^3 and F2 = I1 section 6 all-contained-face boxes with '
            'padding on the same Lambda_N, N at least 2, and with the BA1 gate bound value K=49/111790368 used at every '
            'site of the union volume through the every-site form (b), proved in both packets: ' + template +
            ' Constants (exact; both signs; each of the five comparisons of the contract, namely c1 F1 on Lambda_N versus '
            'Lambda_(N+1), c2 F2 on Lambda_N versus Lambda_(N+1), c3 F1 versus F2 on the same Lambda_N, c4 any two '
            'centered boxes of size at least N compared directly, and c5 two finite complete-factor volumes of one '
            'prescription containing Lambda_N compared directly; in each on-site cutoff space with constants independent '
            'of the cutoff, and at fixed N for the untruncated ground vectors): q=1/64 and C=' + q(v['fC']) + ' (about '
            + short(v['fC']) + '; exact_first_order tier, polymer_kp route; margin about 4.49 against the frozen 1/250000); '
            'the iterated_split route proves the smaller C=' + q(v['rC']) + ' (about ' + short(v['rC']) + ', labelled). '
            'Region form: for every finite complete-factor region Y inside Lambda_N, ||rho^box1_Y-rho^box2_Y||_1 <= '
            'c_site |Y| e^{|Y|/10^8} q^{d_Y} with d_Y=N-max_{y in Y}|y|_inf and c_site=' + q(v['fc']) + ' (about '
            + short(v['fc']) + '; polymer_kp; margin about 2.28 against the frozen 1/500000); iterated_split proves the '
            'smaller c_site=' + q(v['rc']) + ' (about ' + short(v['rc']) + ', labelled). Labelled secondary '
            'pair at q_2=151552|tau| with the re-instantiated input K_2=49/10202112 (disc radius 1/151552, proved in both '
            'packets): C_2=' + q(v['rC2']) + ' (about ' + short(v['rC2']) + ') and c_site,2=' + q(v['rc2']) + ' (about '
            + short(v['rc2']) + '), iterated_split, meeting 1/20000 and 1/40000; polymer_kp proves the smaller values '
            'C_2 about ' + short(v['fC2']) + ' and c_site,2 about ' + short(v['fc2']) + ' (labelled). The crude_majorant tier at '
            'q=1/64 (C about ' + short(v['fCc']) + ' polymer_kp and ' + short(v['rCc']) + ' iterated_split) misses '
            '1/250000 and is retained. The tau to tau/100 ratios of the bound constants are about '
            + format(float(v['ratio_C']), '.6f') + ' for C and ' + format(float(v['ratio_c']), '.6f') + ' for c_site, about ' + format(float(v['ratio_C2']), '.6f')
            + ' and ' + format(float(v['ratio_c2']), '.6f') + ' for the secondary pair, and exactly 100 for q_2. The rate is '
            'per coarse l-infinity step in N at fixed spacing, with constants uniform in N and in the cutoff; no limit '
            'object, whole-sequence convergence, common limit or translation statement is formed, and no dynamics is '
            'asserted.')


def limitations():
    return [
        'Scope: only the zero-selected patterned family (selected triple (0,0,0), Haar reference), fixed spacing, '
        '|tau|<=10^-8, the named families F1 and F2 on centered cubes Lambda_N with N at least 2, finite complete-factor '
        'volumes of one prescription containing Lambda_N, the cover R={0,e_z} and finite complete-factor regions inside '
        'Lambda_N; nothing transfers to other boundary conditions, nonzero selected triples, literal vertex boxes, weak '
        'coupling or the continuum; the constants are uniform in N at fixed spacing and in the cutoff, never in the '
        'lattice spacing.',
        'Static statement about reduced densities of finite-box ground vectors per comparison: no dynamics, no limit '
        'object, no whole-sequence convergence or common limit (BB2), no translation statement, no uniqueness of any '
        'ground state and no analyticity of the reduced density in the coupling (no zero-free region is proved; the '
        'forward uses a real-parameter derivative and the reverse single-support telescoping).',
        'The polymer_kp route uses the Kotecky-Preiss criterion (cited as Kotecky-Preiss 1986 in the form of Ueltschi 2004) '
        'as an external theorem that the frozen packet transcribes without a committed source excerpt (the plan rule that '
        'an external theorem is quoted from a committed excerpt with its PDF hash was not carried into the BB1 contract); '
        'its exploration-tree lemmas bound polymer sums, not the Ursell-weighted cluster sums behind Corollary 6.3 and '
        'Lemma 6.4. The citation was checked post hoc against the Ueltschi excerpt committed after the freeze '
        '(research/round33/sources/ueltschi-math-ph-0304003v3.md, arXiv:math-ph/0304003v3, PDF sha256 '
        '2cc3e036af5b2a46afe95acf0b5863fe5c7d31554debb10a2a5cade4122bdbfc; repair record bb1-kp-repair.md): with hard-core '
        'zeta in {0,-1}, c=0, b equal to the forward distance weight d and a(gamma)=a|supp gamma|, Theorem 3 (16) is the '
        'forward hypothesis, (19) gives its conclusion with the same weight e^{d(X)}, Theorem 1 gives the cluster '
        'expansion of every Z(Lambda\'), and the test sets enter as mass-zero atoms; no factor is missing, so the cited '
        'statement and its use are covered. The excerpt is not a premise of the frozen packet, the original '
        'Kotecky-Preiss paper is neither committed nor needed, and every bound value is at least the value proved by the '
        'self-contained iterated_split route.',
        'F2 volumes other than centred cubes (fifth comparison): the AY1 itemization H1-H5 is gated for F2 on Lambda_N; '
        'both producers apply it to every F2 volume containing Lambda_N as a local reading (on-site operator, per-anchor '
        'grouping inside the star, |X_b|<=4, per-site sum through b in u-S, cutoff compression), reviewed here as '
        'correct but not a gated statement.',
        'Inherited without re-proof: the AM2 multilinear majorant, fixed point, uniqueness in the ball and section 6 '
        'facts; the AV1 product-ordering split, first-order coefficient (49 faces per site) and cutoff-vector removal '
        'F20-F23; the AY1 F2 itemization; the I1 dictionary; Banach, Weierstrass and the maximum principle are standard '
        'and not machine-checked. The every-site coefficient input (form (b)) and the secondary input K_2=49/10202112 '
        'are BB1 lemmas proved in both packets, not admitted BA1 statements.',
        'Upper bounds only; the -tau values replay the same |tau| formula. The near term 2K(1+q)=3185/3577291776 is '
        'almost the whole headline constant (the far-site terms are about 10^-4 of C), so the constants are governed by '
        'the BA1 input; the region margin (about 2.28) is the binding one. The forward, reverse and skeptic derivations '
        'agree to within 2 parts in 10^4 on C and c_site.',
        'Contract wording read as follows: at first order only supports contained in R move rho_R, and every straddling '
        'support, including the 6 of the 72 straddling faces that strictly contain R, has zero first-order R-marginal '
        '(D1); the lemma constant kappa_0 carries the factor |Y|; union-volume sites outside Lambda_N use the exponent '
        '(N-|u|_inf)_+=0; the reverse split weight is read as W<=1/(37888|tau|); tier, route and BA1 input are three '
        'separate labels.',
        'Independence is limited to derivations, constants and code: the contract and selection note name both '
        'mechanisms and the frozen targets, the skeptic triage and pre-freeze review shaped the parameters, all agents '
        'are correlated model agents, isolation is verified for repository inputs only, and the reverse packet does not '
        'itself record its heredoc report write or the file names it saw.',
        'Scientific priority is unverified.',
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('--output must be an absolute path')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('--output must be fresh (absent or empty)')
    if ROOT == out.resolve() or ROOT in out.resolve().parents:
        raise SystemExit('--output must lie outside the checkout')
    result = execute()
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checks': len(result['checks']), 'verdict': result['verdict'],
                      'bound_C': result['previews']['bound_C'], 'bound_c_site': result['previews']['bound_c_site']}))


if __name__ == '__main__':
    main()
