#!/usr/bin/env python3
"""AX1 post-comparison skeptic checks, written after both producer freezes.

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated
ancestry (same model family as the advisor, the lenses and both producers; the
route-B mechanism and its constants came from the skeptic's own triage); not
human peer review or formal verification.

What this adds to the frozen pre-comparison package (ax1_check.py, 80 checks):
  * integrity: contract hash, both freeze closures file by file, both premise
    inventories (reverse isolation) and the unchanged pre-comparison package;
  * an exact re-derivation (own code, nothing imported from any producer) of the
    dictionary and box, the route-B partition and per-site sum 29|tau|, the
    re-frozen contraction J_0'=29/10^8 with its two rationals, the reset
    102|tau| with the Haar gap six, the AQ1 constants, the itemized incidence
    (7 stars, 2 single-factor groups, 6 selected faces, 153 faces charged, 88
    meeting R, 16 inside R) and the per-factor count 52 against the bounds
    96/168;
  * both producers' tier-(ii) values recomputed from their own formulas:
      forward  D'_ii = 2eps(1+eps)/(1+eps^2), eps = 2T'+T'^2,
      reverse  D'_ii = 2eps,                 eps = 88|tau|/144 + 2rho' + T'^2,
    with T'=(52|tau|/144)/(1-352J'), rho'=352J'T'; the exact difference
    eps_fwd-eps_rev = 16|tau|/144 (the 16 faces whose owner sets contain both
    sites of R, charged twice by 2||c^(1)||_a); validity of each; the binding
    recommendation (the larger, certified by both inequalities);
  * the crude tier, the AX2 feasibility arithmetic, linear scaling, the
    first-order coefficient +tau/144 and the flip/parity transfer;
  * cross-producer comparison of every exported constant, the two incidence
    tables, all 28 controls, claim flags and contract reads;
  * source-edit mutations: each producer closure is copied to a temporary tree
    outside the checkout and edited once; every must-abort edit has to abort, an
    unmutated copy has to reproduce the frozen results.json byte for byte, and
    silent value edits (not caught by a producer checker) have to be caught by
    this review's value validator.

Standard library only; exact Fractions decide every Boolean; failures are explicit
exceptions (never assert), so the output bytes match under python -O.

Usage: python3 -B research/round32/skeptic/ax1_postreview_check.py --output /abs/fresh/dir
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
R32 = ROOT / 'research/round32'
CONTRACT = R32 / 'contracts/ax1.json'
CONTRACT_SHA = 'bc834eec4f5377041cea9db42a8674cf1f3de0a43b7fef3696a461a011da7d8d'
AV1_GATE = R32 / 'advisor/av1-gate.json'
PLAN = R32 / 'advisor/plan.json'
FWD = R32 / 'forward/ax1'
REV = R32 / 'reverse/ax1'
PRE_RESULTS = HERE / 'ax1-independent/results.json'
PRE_FREEZE = HERE / 'ax1-independent-freeze.json'
FORBIDDEN_REVERSE = ('research/round32/skeptic/triage.md', 'research/round32/skeptic/loop2-response.md',
                     'research/round32/experts/', 'research/round32/advisor/deliberation-',
                     'research/round32/forward/ax1/', 'research/round32/skeptic/ax1')

DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}
ORIENT = (('x', 'y'), ('x', 'z'), ('y', 'z'))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN, EZ = (0, 0, 0), (0, 0, 1)
R_COVER = (ORIGIN, EZ)


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


def q(x):
    return str(F(x))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preview(x, digits=12):
    """Truncated scientific decimal (display only; never decides anything)."""
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
    s = str(m.numerator // m.denominator)
    return sign + s[0] + '.' + s[1:] + 'e' + str(e)


def sqrt_up(x, den=10 ** 15):
    x = F(x)
    k = isqrt(x.numerator * den * den // x.denominator)
    while F(k, den) ** 2 < x:
        k += 1
    return F(k, den)


def sqrt_down(x, den=10 ** 15):
    x = F(x)
    k = isqrt(x.numerator * den * den // x.denominator)
    while F(k, den) ** 2 > x:
        k -= 1
    return F(k, den)


def fact(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


# ------------------------------------------------------------ geometry (own code)
def add(a, b):
    return tuple(i + j for i, j in zip(a, b))


def sub(a, b):
    return tuple(i - j for i, j in zip(a, b))


def pi_map(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    return ((p, a), (p, c), (add(p, DIRS[a]), c), (add(p, DIRS[c]), a))


def owner_set(p, a, c):
    return frozenset(pi_map(t) for t, _ in face_links(p, a, c))


def is_selected(p, a, c):
    return (a, c) == ('x', 'y') and p[0] % 4 in (0, 1, 2) and p[1] % 2 == 0


def anchored_faces(b):
    out = []
    for r, s in product(range(4), range(2)):
        p = (4 * b[0] + r, 2 * b[1] + s, b[2])
        for a, c in ORIENT:
            out.append({'base': p, 'a': a, 'c': c, 'anchor': b, 'owners': owner_set(p, a, c),
                        'selected': is_selected(p, a, c), 'links': frozenset(face_links(p, a, c))})
    return out


def in_flip_set(link):
    p, d = link
    return (d == 'x' and p[1] % 2 == 0) or (d == 'y' and p[2] % 2 == 0) or (d == 'z' and p[0] % 2 == 0)


def box(n):
    return list(product(range(-n, n + 1), repeat=3))


def route_b_groups(n):
    inside = set(box(n))
    groups = []
    for b in box(n):
        faces = anchored_faces(b)
        if all(add(b, s) in inside for s in S_STAR):
            groups.append({'kind': 'star', 'anchor': b, 'support': frozenset(add(b, s) for s in S_STAR),
                           'faces': [f for f in faces if not f['selected']]})
        groups.append({'kind': 'single', 'anchor': b, 'support': frozenset([b]),
                       'faces': [f for f in faces if f['selected']]})
    return groups


def haar_moment(n):
    """E[W^n], W=chi_{1/2}/2: spin-0 multiplicity in (1/2)^{(x)n} over 2^n."""
    mult = {F(0): 1}
    for _ in range(n):
        nxt = {}
        for j, m in mult.items():
            for jj in (j - F(1, 2), j + F(1, 2)):
                if jj >= 0:
                    nxt[jj] = nxt.get(jj, 0) + m
        mult = nxt
    return F(mult.get(F(0), 0), 2 ** n)


def haar_product(faces_links):
    counts = {}
    for links in faces_links:
        for l in links:
            counts[l] = counts.get(l, 0) + 1
    if any(v % 2 for v in counts.values()):
        return F(0)
    if all(fl == faces_links[0] for fl in faces_links):
        return haar_moment(len(faces_links))
    raise ReviewFailure('Haar product outside the implemented cases')


# ------------------------------------------------------------ state-lemma forms
def density_form(eps):
    return 2 * eps * (1 + eps) / (1 + eps * eps)


def forms_at(abs_tau, faces_per_factor=52, faces_meeting_R=88, J_over_tau=29):
    a = F(abs_tau)
    J = J_over_tau * a
    t1 = F(faces_per_factor, 144) * a
    T = t1 / (1 - 352 * J)
    rho = 352 * J * T
    eps_fwd = 2 * T + T * T
    a1 = F(faces_meeting_R, 144) * a
    eps_rev = a1 + 2 * rho + T * T
    return {'J': J, 't1': t1, 'T': T, 'rho': rho, 'a1': a1, 'eps_fwd': eps_fwd, 'eps_rev': eps_rev,
            'D_fwd': density_form(eps_fwd), 'D_rev': 2 * eps_rev, 'D_rev_density': density_form(eps_rev),
            'two_eps_fwd': 2 * eps_fwd}


def crude_at(abs_tau):
    t = 29 * F(abs_tau) * F(148, 7)
    eps = 2 * t + t * t
    return {'t': t, 'eps': eps, 'D_fwd': density_form(eps), 'D_rev': 2 * eps}


def atan_bracket(x, terms):
    s = F(0)
    for k in range(terms):
        s += (-1) ** k * x ** (2 * k + 1) / (2 * k + 1)
    nxt = x ** (2 * terms + 1) / (2 * terms + 1)
    return (s, s + nxt) if terms % 2 == 0 else (s - nxt, s)


def pi_bracket():
    a_lo, a_hi = atan_bracket(F(1, 5), 25)
    b_lo, b_hi = atan_bracket(F(1, 239), 8)
    lo, hi = 16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo
    if not (lo < hi and hi - lo < F(1, 10 ** 25) and F(314159, 100000) < lo and hi < F(314160, 100000)):
        raise ReviewFailure('pi bracket')
    return lo, hi


# ------------------------------------------------------------ producer value validator (silent edits)
def validate_producer_values(results, direction, cap):
    """Rejects a producer packet whose headline state-lemma values differ from the producer's own
    declared formula recomputed here (so an undercount that a producer checker does not pin is caught)."""
    fm = forms_at(cap)
    cr = crude_at(cap)
    if direction == 'forward':
        h = results['headline']
        if F(h['D_ii_plus']) != fm['D_fwd'] or F(h['D_ii_minus']) != fm['D_fwd']:
            raise Rejected('forward D_ii differs from 2eps(1+eps)/(1+eps^2) with eps=2T+T^2, T=(52|tau|/144)/(1-352J)')
        if F(h['D_i_plus']) != cr['D_fwd'] or F(h['D_i_minus']) != cr['D_fwd']:
            raise Rejected('forward D_i differs from the crude density form at t=J G(R)')
        t = results['tiers']['+']['ii']
        if F(t['t']) != fm['T'] or F(t['remainder']) != fm['rho'] or F(t['eps']) != fm['eps_fwd']:
            raise Rejected('forward tier (ii) components differ')
    else:
        d = results['D_prime_ii']
        if F(d['+']) != fm['D_rev'] or F(d['-']) != fm['D_rev']:
            raise Rejected('reverse D_ii differs from 2eps with eps=88|tau|/144+2rho+T^2')
        if F(d['density_form_both_inequalities']) != fm['D_rev_density']:
            raise Rejected('reverse density form differs')
        if F(results['D_prime_i']['+']) != cr['D_rev']:
            raise Rejected('reverse D_i differs from 2eps at t=J G(R)')
        t = results['tiers']['tier_ii']['+']
        if (F(t['a1_first_order_meeting_R']) != fm['a1'] or F(t['T_self_consistent']) != fm['T']
                or F(t['remainder_anchored_upper_rho']) != fm['rho'] or F(t['epsilon']) != fm['eps_rev']):
            raise Rejected('reverse tier (ii) components differ')
    return True


# ------------------------------------------------------------ source-mutation replays
def mutated_run(direction, edits=(), extra_input=None, contract_edit=None, rehash=False):
    src = FWD if direction == 'forward' else REV
    with tempfile.TemporaryDirectory(prefix='hnm-r32-ax1-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / 'research/round32' / direction / 'ax1'
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        code = (dst / 'check.py').read_text()
        for old, new in edits:
            if code.count(old) != 1:
                raise ReviewFailure('mutation anchor not unique in %s: %r' % (direction, old[:60]))
            code = code.replace(old, new)
        if contract_edit is not None:
            cpath = dst / 'inputs/research/round32/contracts/ax1.json'
            raw = cpath.read_bytes()
            old, new = contract_edit
            if raw.count(old) != 1:
                raise ReviewFailure('contract mutation anchor not unique')
            raw = raw.replace(old, new)
            cpath.write_bytes(raw)
            if rehash:
                if code.count(CONTRACT_SHA) != 1:
                    raise ReviewFailure('contract hash constant not unique in ' + direction)
                code = code.replace(CONTRACT_SHA, hashlib.sha256(raw).hexdigest())
        (dst / 'check.py').write_text(code)
        if extra_input is not None:
            extra = dst / 'inputs' / extra_input
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text('skeptic mutation fixture\n')
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(dst / 'check.py'), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(repo))
        results = (out / 'results.json').read_bytes() if (out / 'results.json').is_file() else None
        last = done.stderr.strip().splitlines()[-1] if done.stderr.strip() else ''
        if any(p.name == '__pycache__' or p.suffix == '.pyc' for p in dst.rglob('*')):
            raise ReviewFailure('interpreter cache written into a mutated copy')
        return done.returncode, results, last.replace(tmp, '<tmp>')


# ------------------------------------------------------------ main computation
def run():
    # ================= integrity and bindings
    raw = CONTRACT.read_bytes()
    con = json.loads(raw)
    ff = json.loads((FWD / 'freeze.json').read_text())
    rf = json.loads((REV / 'freeze.json').read_text())
    pre_fz = json.loads(PRE_FREEZE.read_text())
    pre_ok = all(sha(ROOT / name) == digest for name, digest in pre_fz['files'].items()) and len(pre_fz['files']) == 4
    need(sha(CONTRACT) == CONTRACT_SHA and ff['contract_sha256'] == CONTRACT_SHA and rf['contract_sha256'] == CONTRACT_SHA
         and pre_fz['contract_sha256'] == CONTRACT_SHA and pre_ok and pre_fz['stage'] == 'pre_comparison'
         and con['status'] == 'frozen_before_production',
         'contract_freeze_and_precomparison_bindings', contract_sha256=CONTRACT_SHA,
         forward_freeze_sha256=sha(FWD / 'freeze.json'), reverse_freeze_sha256=sha(REV / 'freeze.json'),
         precomparison_files_unchanged=sorted(pre_fz['files']))

    closures = {}
    for direction, src, fz in (('forward', FWD, ff), ('reverse', REV, rf)):
        prefix = src.relative_to(ROOT).as_posix() + '/'
        files = {n[len(prefix):]: d for n, d in fz['sources'].items()}
        actual = {p.relative_to(src).as_posix() for p in src.rglob('*') if p.is_file() and p.name != 'freeze.json'}
        ok = (all(n.startswith(prefix) for n in fz['sources']) and set(files) == actual
              and all(sha(src / n) == d for n, d in files.items())
              and not any('__pycache__' in n or n.endswith('.pyc') for n in actual)
              and fz['loop'] == 'AX1' and fz['direction'] == direction and fz['normal_optimized_identical'] is True
              and fz['independent_before_current_counterpart_exchange'] is True)
        closures[direction] = {'closure_files': len(files), 'ok': ok}
    need(all(v['ok'] for v in closures.values()) and closures['forward']['closure_files'] == 45
         and closures['reverse']['closure_files'] == 42, 'producer_closures_verified_file_by_file',
         closures={k: v['closure_files'] for k, v in closures.items()})

    shared = list(con['shared_premises'])
    fadd = list(con['forward_additional_premises'])
    inv = {}
    for direction, src in (('forward', FWD), ('reverse', REV)):
        base = src / 'inputs'
        names = sorted(p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file())
        same = all((base / n).read_bytes() == (ROOT / n).read_bytes() for n in names)
        inv[direction] = (names, same)
    rev_expected = sorted(['AGENTS.md', 'research/round32/contracts/ax1.json'] + shared)
    fwd_expected = sorted(rev_expected + fadd)
    rev_forbidden = [n for n in inv['reverse'][0] if n.startswith(FORBIDDEN_REVERSE) or n in fadd]
    need(con['reverse_premise_isolation'] is True and inv['reverse'][0] == rev_expected and inv['reverse'][1]
         and rev_forbidden == [] and inv['forward'][0] == fwd_expected and inv['forward'][1]
         and len(inv['reverse'][0]) == 38 and len(inv['forward'][0]) == 41 and len(shared) == 36,
         'premise_inventories_and_reverse_isolation', reverse_inputs=len(inv['reverse'][0]),
         forward_inputs=len(inv['forward'][0]), shared_premises=len(shared), forward_additional=fadd,
         reverse_forbidden_present=rev_forbidden, snapshots_byte_identical_to_repository=True)

    fres = json.loads((FWD / 'output/results.json').read_text())
    rres = json.loads((REV / 'output/results.json').read_text())
    pre = json.loads(PRE_RESULTS.read_text())
    fch = {c['id']: c for c in fres['checks']}
    rch = {c['id']: c for c in rres['checks']}

    # ================= contract values
    par = con['parameters']
    cap = F(par['tau_cap'])
    target = F(con['preregistration']['target']['value'])
    m = re.search(r"J_0'=(\d+)/10\^(\d+)", par['J0_resolution'])
    j0p = F(int(m.group(1)), 10 ** int(m.group(2)))
    need(cap == F(1, 10 ** 8) and target == F(1, 2500000) and j0p == F(29, 10 ** 8)
         and con['controls'] == con['preregistration']['controls_required']['ids'] and len(con['controls']) == 28,
         'contract_values_read', tau_cap=q(cap), target=q(target), J0_prime=q(j0p), controls=len(con['controls']))

    # ================= item 1: dictionary and box
    dict_ok = True
    for g2, a in ((F(3), F(5, 7)), (F(1, 2), F(2)), (F(97979), F(1, 1000))):
        alpha, lam = g2 / (2 * a), 2 / (g2 * a)
        tau = 24 * lam / alpha
        dict_ok = dict_ok and tau * g2 * g2 == 96 and alpha * tau / 24 == lam and (alpha / 8) * (tau / 3) == lam
    need(dict_ok and 96 / cap == 9600000000 and cap / 24 <= F(1, 8) and F(3, 24) == F(1, 8) and F(4, 24) > F(1, 8)
         and cap / 24 == F(1, 2400000000), 'dictionary_box_and_label',
         g4_at_cap=q(96 / cap), selected_over_alpha_at_cap=q(cap / 24), box_holds_iff_abs_tau_le='3',
         label='uniform Kogut-Susskind SU(2) at fixed spacing, strong bare coupling (g^4=96/tau); never weak coupling or continuum',
         negative_tau='no real-g preimage; the U_E image of +|tau|')

    # ================= item 2 and 10: classes, partition, per-site sum
    cell = anchored_faces(ORIGIN)
    sel = [f for f in cell if f['selected']]
    om = [f for f in cell if not f['selected']]
    rel = [frozenset(f['owners']) for f in cell]
    census = {}
    for n in (1, 2, 3):
        groups = route_b_groups(n)
        keys = [(f['base'], f['a'] + f['c']) for g in groups for f in g['faces']]
        persite = {}
        faces_site = {}
        for g in groups:
            w = F(len(g['faces']), 3)
            for u in g['support']:
                persite[u] = persite.get(u, F(0)) + w
            for f in g['faces']:
                for u in f['owners']:
                    faces_site[u] = faces_site.get(u, 0) + 1
        census[n] = {'groups': groups, 'unique': len(keys) == len(set(keys)), 'faces': len(keys),
                     'maxJ': max(persite.values()), 'J0': persite[ORIGIN], 'maxfaces': max(faces_site.values()),
                     'faces0': faces_site[ORIGIN],
                     'support_ok': all(f['owners'] <= g['support'] for g in groups for f in g['faces'])}
    need(len(cell) == 24 and len(sel) == 3 and len(om) == 21
         and all(len(f['owners']) == 1 for f in sel) and all(len(f['owners']) >= 2 for f in om)
         and all(census[n]['unique'] and census[n]['support_ok'] and census[n]['maxJ'] <= 29 and census[n]['maxfaces'] <= 52
                 for n in (1, 2, 3))
         and census[3]['J0'] == 29 and census[3]['faces0'] == 52 and census[3]['faces'] == 5565
         and max(len(g['support']) for g in census[3]['groups']) == 4 and 2 * 4 == 8,
         'route_b_partition_and_per_site_sum',
         classes=24, omitted=21, selected=3, star_norm_over_tau='7', single_norm_over_tau='1', J_prime_over_tau='29',
         box_N3_faces_charged_once=census[3]['faces'], max_support=4, termination_order=8,
         double_count_alternative_J_over_tau='33 (selected in stars and singles, rejected)')

    # ================= item 3: contraction
    x = F(1, 8)
    e8 = sum((x ** k / fact(k) for k in range(13)), F(0)) + x ** 13 / fact(13) / (1 - x / 14)
    GR = 16 * e8 * (1 + F(10, 64))
    GpR = 16 * e8 * (18 + F(80, 64))
    self_map, contraction = j0p * F(148, 7), 2 * j0p * 352
    need(e8 < F(8, 7) and GR < F(148, 7) and GpR < 352 and 29 * cap <= j0p
         and self_map == F(1073, 175000000) and self_map < F(1, 64) and 1073 * 64 < 175000000
         and contraction == F(319, 1562500) and contraction < 1
         and F(7, 25000000) < 29 * cap and F(7, 725000000) * 29 == F(7, 25000000),
         'j0_prime_refreeze_contraction', exp_one_eighth_upper=q(e8), J0_prime=q(j0p), self_map=q(self_map),
         contraction=q(contraction), old_J0_below_J_at_cap=True, R2_changed_cap='7/725000000',
         am2_reuse='AM2 sections 2-6 with J_0\' (support<=4 majorant, termination 8, h_b>=6Q_b>=Q_b): unique ground, '
                   'full-space gap>=1/2 normalized (alpha/16 physical) in every finite complete-factor volume, both signs')

    # ================= item 4: reset and AQ constants
    reset = 2 * (7 * 7 + 2 * 1)
    eps_R = F(reset, 6)
    need(reset == 102 and eps_R == 17 and 4 * eps_R * cap <= F(1, 500) ** 2 and 4 * reset * cap > F(1, 500) ** 2
         and 4 * 98 * cap <= F(1, 500) ** 2 and F(1, 4) - F(1, 500) - F(1, 250000) == F(61999, 250000)
         and 2 * (4 * 7 + 1) == 58 and 81 * 29 == 2349 and max(29, 16 * 7, 81 * 7) == 567 and 2 * 7 * 7 + 2 == 100,
         'reset_gap_six_and_aq_constants', reset_over_tau=reset, eps_R_over_tau='17',
         sqrt_control_upper=preview(2 * sqrt_up(17 * cap)), gap_one_fails_1_over_500=True,
         aq2_verbatim_98_with_gap_one_passes=True, variance_floor='61999/250000', C_F_over_tau_per_site=58,
         Phi_F_crude_over_tau=2349, Phi_F_per_pair_over_tau_labelled=567, reset_refinement_labelled_over_tau=100)

    # ================= items 5 and 10: itemized incidence
    Rset = set(R_COVER)
    expect = {('star', (0, 0, 0)): (21, 10), ('star', (0, 0, 1)): (21, 0), ('star', (0, 0, -1)): (16, 0),
              ('star', (-1, 0, 0)): (4, 0), ('star', (0, -1, 0)): (8, 0), ('star', (-1, 0, 1)): (4, 0),
              ('star', (0, -1, 1)): (8, 0), ('single', (0, 0, 0)): (3, 3), ('single', (0, 0, 1)): (3, 3)}
    tables = {}
    for n in (2, 3):
        meet_groups = [g for g in census[n]['groups'] if g['support'] & Rset]
        tables[n] = {(g['kind'], g['anchor']): (sum(1 for f in g['faces'] if f['owners'] & Rset),
                                                 sum(1 for f in g['faces'] if f['owners'] <= Rset)) for g in meet_groups}
        tables[n]['charged'] = sum(len(g['faces']) for g in meet_groups)
    n1 = sum(1 for g in census[1]['groups'] if g['kind'] == 'star' and g['support'] & Rset)
    meet_faces = [f for g in census[3]['groups'] for f in g['faces'] if f['owners'] & Rset]
    contain = [f for f in meet_faces if Rset <= f['owners']]
    need(all({k: v for k, v in tables[n].items() if k != 'charged'} == expect and tables[n]['charged'] == 153 for n in (2, 3))
         and sum(v[0] for v in expect.values()) == 88 and sum(v[1] for v in expect.values()) == 16
         and sum(1 for k in expect if k[0] == 'star') == 7 and sum(1 for k in expect if k[0] == 'single') == 2
         and sum(v[0] for k, v in expect.items() if k[0] == 'single') == 6 and len(meet_faces) == 88 and len(contain) == 16
         and n1 == 4 and F(7 * 7 + 2, 8) == F(51, 8),
         'itemized_incidence_table',
         rows=[{'group': k[0], 'anchor': list(k[1]), 'faces_meeting_R': v[0], 'faces_inside_R': v[1]} for k, v in sorted(expect.items())],
         stars=7, single_factor_groups=2, selected_faces=6, faces_charged=153, faces_meeting_R=88, faces_inside_R=16,
         straddling=72, faces_containing_R=16, box_N1_stars=n1, B_N_over_tau='51/8', k_prime_over_tau='51/4',
         no_double_count='each face has one anchor pi(base) and one role; stars hold the 21 omitted classes, singles the 3 selected')

    # ================= item 6: per-factor count and bounds
    offs = {s: sum(1 for f in cell if sub(s, (0, 0, 0)) in {sub(o, (0, 0, 0)) for o in f['owners']}) for s in S_STAR}
    per_factor = sum(offs.values())
    om_factor = sum(len(f['owners']) for f in om)
    both_R = sum(1 for f in cell if Rset <= set(f['owners']))
    mult = {}
    for g in census[3]['groups']:
        for f in g['faces']:
            if ORIGIN in f['owners']:
                mult[f['owners']] = mult.get(f['owners'], 0) + 1
    need(offs == {(0, 0, 0): 24, (1, 0, 0): 4, (0, 1, 0): 8, (0, 0, 1): 16} and per_factor == 52 and om_factor == 49
         and 2 * per_factor - both_R == 88 and both_R == 16 and 4 * 24 == 96 and 7 * 24 == 168 and per_factor < 96 and 88 < 168
         and sorted(mult.values()) == [1] * 5 + [2] * 3 + [3] * 3 + [4] * 3 + [10] * 2,
         'per_factor_count_52_and_labelled_bounds', exact_per_factor=52, omitted=49, selected=3, exact_meeting_R=88,
         bound_per_factor_4x24=96, bound_R_7x24=168, owner_sets_through_site=16,
         status='52 and 88 are exact counts; 96 and 168 are valid triangle bounds only (they count the 44 anchored faces whose owner sets miss u)')

    # ================= state-lemma tiers: both producers' formulas
    fm = forms_at(cap)
    fm_m = forms_at(abs(-cap))
    cr = crude_at(cap)
    fh = fres['headline']
    rd = rres['D_prime_ii']
    need(fm['t1'] == F(13, 3600000000) and fm['T'] == F(13, 3599632512) and fm['rho'] == F(4147, 11248851600000000)
         and fm['eps_fwd'] == F(93590445481, 12957354221447430144)
         and fm['D_fwd'] == F(2425369125199104794263242601250, 167893028420061547330293754713793182097)
         and F(fh['D_ii_plus']) == fm['D_fwd'] and F(fh['D_ii_minus']) == fm_m['D_fwd']
         and F(pre['tiers']['+']['D_ii_exact52']['D_fwd']) == fm['D_fwd']
         and F(rres['tiers']['tier_ii_global_two_site']['+']['D_density_form_exact']) == fm['D_fwd'],
         'forward_D_ii_recomputed', D_ii=q(fm['D_fwd']), preview=preview(fm['D_fwd']),
         form='2eps(1+eps)/(1+eps^2), eps=2T+T^2, T=(52|tau|/144)/(1-352J\')',
         reproduced_exactly_by=['skeptic pre-comparison D_ii_exact52', 'reverse variant tier_ii_global_two_site (density form)'])
    need(fm['a1'] == F(11, 1800000000) and fm['eps_rev'] == F(30934916107401289, 5061466492752902400000000)
         and fm['D_rev'] == F(30934916107401289, 2530733246376451200000000)
         and F(rd['+']) == fm['D_rev'] and F(rd['-']) == fm_m['D_rev']
         and F(rd['density_form_both_inequalities']) == fm['D_rev_density']
         and 2 * F(pre['tiers']['+']['D_ii_R88_labelled']['eps']) == fm['D_rev']
         and F(pre['tiers']['+']['D_ii_R88_labelled']['D_fwd']) == fm['D_rev_density']
         and F(rres['tiers']['tier_ii']['+']['t1_first_order_anchored']) == fm['t1'],
         'reverse_D_ii_recomputed', D_ii=q(fm['D_rev']), preview=preview(fm['D_rev']),
         density_form=q(fm['D_rev_density']), density_form_preview=preview(fm['D_rev_density']),
         form="2eps, eps=a_1'+2rho'+T'^2 with a_1'=88|tau|/144 (faces meeting R), rho'=352J'T', t_1'=52|tau|/144",
         reproduced_exactly_by=['skeptic pre-comparison D_ii_R88_labelled (2eps and density form)'])
    diff_eps = fm['eps_fwd'] - fm['eps_rev']
    diff_D = fm['D_fwd'] - fm['D_rev']
    need(diff_eps == F(16, 144) * cap == cap / 9 and 2 * fm['t1'] - fm['a1'] == diff_eps
         and diff_D == 2 * diff_eps + (fm['D_fwd'] - fm['two_eps_fwd']) and fm['D_fwd'] - fm['two_eps_fwd'] > 0
         and fm['D_fwd'] - fm['two_eps_fwd'] < F(1, 10 ** 15),
         'D_ii_difference_explained', eps_fwd_minus_eps_rev=q(diff_eps), equals='16|tau|/144=|tau|/9',
         D_fwd_minus_D_rev=q(diff_D), D_fwd_minus_D_rev_preview=preview(diff_D),
         density_vs_2eps_part=preview(fm['D_fwd'] - fm['two_eps_fwd']),
         ratio_preview=preview(fm['D_fwd'] / fm['D_rev']),
         explanation='both use t_1\'=52|tau|/144, T\', rho\'=352J\'T\' and the pair term T\'^2; they differ in the first-order '
                     'collection over creations meeting R: forward bounds it by 2||c||_a (2t_1\'=104 faces, the 16 faces whose owner '
                     'sets contain both 0 and e_z counted twice), reverse by the R-refined 88 faces; and in the final inequality '
                     '(forward density form 2eps(1+eps)/(1+eps^2), reverse 2eps>=2eps/sqrt(1+eps^2)), which moves D by ~1e-16 only')
    # validity: fidelity form <= 2eps <= density form for 0<eps<=1; ordering
    fid = {}
    for name, eps in (('fwd', fm['eps_fwd']), ('rev', fm['eps_rev'])):
        fid[name] = 2 * eps / sqrt_down(1 + eps * eps, 10 ** 40)
    need(0 < fm['eps_rev'] < fm['eps_fwd'] <= 1 and fid['rev'] <= fm['D_rev'] and fid['fwd'] <= fm['two_eps_fwd'] + F(1, 10 ** 30)
         and fm['D_rev'] <= fm['D_rev_density'] < fm['two_eps_fwd'] <= fm['D_fwd']
         and fm['D_fwd'] <= target and fm['D_rev'] <= target and fm['D_fwd'] < F(1, 10 ** 6)
         and fm['D_fwd'] >= cap / 144 and fm['D_rev'] >= cap / 144,
         'both_D_ii_valid_upper_bounds',
         ordering='fidelity(eps_rev)<=2eps_rev=D_rev<=density(eps_rev)<2eps_fwd<=density(eps_fwd)=D_fwd<=4/10^7',
         forward_basis='sum over creations meeting R <= 2||c||_a <= 2T\' (AV1 forward split, both inequalities)',
         reverse_basis='sum over creations meeting R <= sum ||c^(1)_I|| + 2||c-c^(1)||_a <= 88|tau|/144+2rho\' (R-refined, labelled; fidelity inequality, density form also below target)',
         margins={'forward': preview(target / fm['D_fwd'], 6), 'reverse': preview(target / fm['D_rev'], 6)})
    need(cr['t'] == F(1073, 175000000) and F(fh['D_i_plus']) == cr['D_fwd'] and F(rres['D_prime_i']['+']) == cr['D_rev']
         and cr['D_rev'] < cr['D_fwd'] and cr['D_rev'] > target and cr['D_rev'] > F(1, 10 ** 6)
         and F(pre['tiers']['+']['D_i_crude']['D_fwd']) == cr['D_fwd'],
         'crude_tier_D_i_retained_failure', D_i_forward=q(cr['D_fwd']), D_i_reverse=q(cr['D_rev']),
         previews={'forward': preview(cr['D_fwd']), 'reverse': preview(cr['D_rev'])}, meets_target=False)

    # binding recommendation and the AV1 precedent
    av1 = json.loads(AV1_GATE.read_text())
    av1_d = F(re.search(r'D_ii=(\d+/\d+)', av1['accepted']).group(1))
    t_av1 = F(49, 144) * cap / (1 - 352 * 28 * cap)
    need(density_form(2 * t_av1 + t_av1 ** 2) == av1_d and 'certified by both inequalities' in av1['decision']
         and fm['D_fwd'] == max(fm['D_fwd'], fm['D_rev'], fm['D_rev_density'], fm['two_eps_fwd']),
         'binding_recommendation_forward_value',
         bind=q(fm['D_fwd']), bind_preview=preview(fm['D_fwd']),
         reason='largest valid exact-count tier-(ii) headline; certified by both inequalities (density form at eps=2T\'+T\'^2 '
                'dominates the fidelity form at the same eps); uses no R-refinement; equals the skeptic pre-comparison and the '
                'reverse global_two_site density variant exactly; same construction the AV1 gate bound (AV1 D_ii reproduced exactly '
                'from 49 faces and J=28|tau|)',
         reverse_value_status='valid labelled R-refinement (88 faces meeting R), fidelity-backed headline; its density form is also below target')

    # AX2 feasibility and the contract note
    pi_lo, pi_hi = pi_bracket()
    Fup = lambda d: 2 * (d + d * d) + 51 * cap / pi_lo
    Flo = lambda d: 2 * (d + d * d) + 51 * cap / pi_hi
    goal = F(1, 10 ** 6)
    need(Fup(fm['D_fwd']) <= goal and Fup(fm['D_rev']) <= goal and Fup(target) <= goal
         and Fup(F(41883, 10 ** 11)) <= goal and Flo(F(41884, 10 ** 11)) > goal and Flo(F(419, 10 ** 9)) > goal
         and Flo(cr['D_rev']) > goal,
         'ax2_feasibility_and_contract_note', threshold_bracket=['41883/10^11', '41884/10^11'],
         contract_note_4_19e_7_infeasible=True, radius_with_bound_preview=preview(Fup(fm['D_fwd'])),
         margin_with_bound_preview=preview(goal / Fup(fm['D_fwd']), 6))

    ratios = {}
    for name, fn in (('forward', lambda a: forms_at(a)['D_fwd']), ('reverse', lambda a: forms_at(a)['D_rev']),
                     ('crude', lambda a: crude_at(a)['D_fwd'])):
        ratios[name] = fn(cap) / fn(cap / 100)
    need(all(99 <= r <= 101 for r in ratios.values()) and (4 * 17 * cap) / (4 * 17 * cap / 100) == 100,
         'linear_scaling_both_forms', ratios={k: preview(v, 9) for k, v in ratios.items()}, sqrt_control_ratio='10')

    # ================= item 9: first order, parity, flip
    Wf = [f for f in cell if f['base'] == (0, 0, 0) and (f['a'], f['c']) == ('x', 'z')][0]
    Wl = Wf['links']
    mean1 = F(0)
    contributors = []
    for f in meet_faces:
        e = haar_product([Wl, f['links']])
        mean1 += F(2, 72) * e
        if e:
            contributors.append((f['base'], f['a'] + f['c']))
    parity_all = all(haar_product([Wl, Wl, f['links']]) == 0 for f in meet_faces)
    sel_meet = [f for f in meet_faces if f['selected']]
    sel_share = [f for f in sel_meet if f['links'] & Wl]
    flips = [sum(1 for l in face_links(p, a, c) if in_flip_set(l))
             for p in product(range(-4, 8), range(-2, 4), range(-2, 3)) for a, c in ORIENT]
    sel_flip = [sum(1 for l in f['links'] if in_flip_set(l)) for g in census[2]['groups'] for f in g['faces'] if f['selected']]
    coeff_ok = all((-1 if sum(1 for l in f['links'] if in_flip_set(l)) % 2 else 1) * (-t / 3) == -(-t) / 3
                   for g in census[2]['groups'] for f in g['faces'] for t in (cap, cap / 7))
    untied_breaks = any((-1 if sum(1 for l in f['links'] if in_flip_set(l)) % 2 else 1) * F(-1, 15) != F(-1, 15)
                        for g in census[2]['groups'] for f in g['faces'] if f['selected'])
    g0 = [f for f in cell if f['selected'] and f['base'] == (0, 0, 0)][0]
    Hc = lambda t, k: [[F(0), -t / 6, -k / 6], [-t / 6, F(24), F(0)], [-k / 6, F(0), F(24)]]
    Dm = [F(1), F(-1), F(-1)]
    conj = lambda M: [[Dm[i] * M[i][j] * Dm[j] for j in range(3)] for i in range(3)]
    tf = F(1, 7)
    need(not Wf['selected'] and Wf['owners'] == frozenset(R_COVER) and mean1 == F(1, 144) and len(contributors) == 1
         and parity_all and haar_moment(3) == 0 and haar_moment(2) == F(1, 4) and haar_moment(4) == F(1, 8)
         and len(sel_meet) == 6 and len(sel_share) == 2 and all(haar_product([Wl, f['links']]) == 0 for f in sel_meet)
         and all(v in (1, 3) for v in flips) and all(v in (1, 3) for v in sel_flip) and len(sel_flip) == 375
         and sum(1 for l in Wl if in_flip_set(l)) == 3 and sum(1 for l in g0['links'] if in_flip_set(l)) % 2 == 1
         and coeff_ok and untied_breaks and conj(Hc(tf, tf)) == Hc(-tf, -tf) and conj(Hc(tf, F(1, 100))) != Hc(-tf, F(1, 100)),
         'first_order_parity_and_flip_transfer', first_order_coefficient='+1/144',
         first_order_at_cap=[q(cap / 144), q(-cap / 144)], only_f_equals_W=True, E_W2_Wf_zero_all_88=True,
         selected_faces_meeting_R=6, selected_sharing_link_with_W=2, fine_plaquettes_checked=len(flips),
         selected_faces_box_N2=len(sel_flip), uniform_identity='U_E H(tau) U_E^*=H(-tau): every coefficient -(tau/3), every W_f E-odd, '
         'h_b tau-independent and U_E-invariant', untied_selected_coefficient_breaks_identity=True,
         K2_not_transferred='route-B T\', rho\' and single-site first-order creations change every term; not computed in AX1')

    # ================= cross-producer comparison of exported constants
    fc = fres['constants']
    fj = fres['j0_resolution']
    rj = rres['j0_resolution']
    rc = rres['reset']
    ftab = {(e['group'], tuple(e['anchor'])): (e['faces_meeting_R'], sum(1 for x in e['faces'] if x['inside_R']), e['faces_total'])
            for e in fres['incidence_table']}
    rtab = {('star' if e['kind'] == 'whole_star' else 'single', tuple(e['anchor'])):
            (e['faces_owning_link_in_R'], e['faces_inside_R'], e['n_faces'])
            for e in rch['item10_incidence_table_itemized_no_double_count']['table']}
    mine = {k: (v[0], v[1], 21 if k[0] == 'star' else 3) for k, v in expect.items()}
    need(ftab == rtab == mine, 'incidence_tables_agree_three_ways', rows=len(mine))
    fe = fres['face_enumeration']
    re_ = rres['face_enumeration']
    agree = {
        'J_prime': (F(fc['J_prime_over_abs_tau']), F(rres['grouping']['per_site_sum_per_tau']), F(29)),
        'J0_prime': (F(fj['J0_prime']), F(rj['J0_prime']), j0p),
        'self_map': (F(fj['self_map']), F(rj['self_map_upper']), self_map),
        'contraction': (F(fj['exclusion']), F(rj['contraction_upper']), contraction),
        'reset': (F(fc['reset_over_abs_tau']), F(rc['budget_per_tau']), F(reset)),
        'eps_R': (F(fc['eps_R_over_abs_tau']), F(rc['epsilon_R_per_tau']), eps_R),
        'B_N': (F(fc['B_N_over_abs_tau']), F(rch['item10_incidence_table_itemized_no_double_count']['totals']['B_N_alpha_units_per_tau']), F(51, 8)),
        'k_prime': (F(fc['k_prime_over_abs_tau']), F(rch['item10_incidence_table_itemized_no_double_count']['totals']['k_prime_per_tau']), F(51, 4)),
        'faces_per_factor': (F(fe['faces_per_factor']), F(re_['derived']['faces_per_factor']), F(52)),
        'faces_meeting_R': (F(fe['faces_meeting_R']), F(re_['derived']['faces_meeting_R']), F(88)),
        'faces_inside_R': (F(fe['faces_inside_R']), F(re_['derived']['faces_inside_R']), F(16)),
        'reference_gap': (F(fc['onsite_gap']), F(rc['reference_gap']), F(6)),
        'g4_at_cap': (F(fres['dictionary']['g4_at_cap']), F(rres['dictionary']['g4_at_cap']), 96 / cap),
        'T_prime': (F(fres['tiers']['+']['ii']['t']), F(rres['tiers']['tier_ii']['+']['T_self_consistent']), fm['T']),
        'rho_prime': (F(fres['tiers']['+']['ii']['remainder']), F(rres['tiers']['tier_ii']['+']['remainder_anchored_upper_rho']), fm['rho']),
        'C_F': (F(fc['C_F_per_site_over_abs_tau']), F(58), F(58)),
        'Phi_F': (F(fc['Phi_F_over_abs_tau']), F(2349), F(2349)),
    }
    missing = sorted(k for k, v in agree.items() if v[1] is None)
    need(missing == [] and all(v[0] == v[1] == v[2] for v in agree.values())
         and fres['headline']['omega_W_first_order'] == {'+': q(cap / 144), '-': q(-cap / 144)}
         and F(fres['dictionary']['g4_at_cap']) == 9600000000
         and '=58|tau||F|' in rch['item4_reset_budget_102_epsilon_17']['aq1_C_F'] and '=2349|tau|' in rch['item4_reset_budget_102_epsilon_17']['ns_interaction_norm'],
         'producer_constants_agree', compared=sorted(agree), values={k: q(v[2]) for k, v in sorted(agree.items())})

    # ================= controls, flags, contract reads
    ids = con['controls']
    f_mut = {c: len(fch[c]['rejected_mutations']) for c in ids}
    r_mut = {c: len(rch[c]['rejected_mutations']) for c in ids}
    extra_f = sum(len(c.get('rejected_mutations', [])) for c in fres['checks'] if c['id'] not in ids)
    need(all(v > 0 for v in f_mut.values()) and all(v > 0 for v in r_mut.values())
         and all(rch[c].get('kind') == 'damaging_mutation_control' for c in ids)
         and sum(f_mut.values()) == 93 and extra_f == 1 and fres['rejected_mutation_total'] == 94
         and fres['controls_with_damaging_mutations'] == 28 and sum(r_mut.values()) == 111
         and len(fres['checks']) == 52 and len(rres['checks']) == 58,
         'all_28_controls_damaging_mutations_both', forward_control_rejections=sum(f_mut.values()),
         forward_other_rejections=extra_f, forward_reported_total=94, reverse_control_rejections=sum(r_mut.values()),
         forward_checks=52, reverse_checks=58,
         note='the forward report says the 28 controls reject 94 mutations; 93 sit in control checks and 1 (E minus one link) in flip_set_odd_all_classes')
    req_flags = {'continuum_claim': False, 'uniform_wilson_claim': True, 'weak_coupling_claim': False,
                 'resolved_interaction_shift': False, 'scientific_priority_verified': False, 'euclidean_node_certified': False}
    labels = [fres['label']['model_label'], rres['model_label']]
    need(all(fres.get(k) is v and rres.get(k) is v for k, v in req_flags.items())
         and all(fres.get(k) is False for k in ('k2_uniform_claimed', 'uniqueness_claimed', 'rate_in_N_claimed',
                                                 'whole_sequence_convergence_claimed', 'wilson_mean_sign_certified'))
         and all(l == 'uniform Kogut-Susskind SU(2) at fixed spacing, strong bare coupling' for l in labels)
         and rres['sub_label'] == 'uniform_local_closeness_not_uniqueness',
         'claim_flags_both_producers', flags=req_flags, label=labels[0],
         uniform_wilson_claim_scope='fixed-spacing uniform Kogut-Susskind model as labelled only; not a Wilson-mean sign certificate')
    fcs = fch['contract_snapshot_sha256']
    rcr = rch['contract_candidates_compared_after_derivation']['read_from_contract']
    need(fcs['target_read_from_contract'] == q(target) and fcs['J0_prime_read_from_contract'] == q(j0p)
         and fcs['contract_sha256'] == CONTRACT_SHA and rcr['target'] == q(target) and rcr['J0_prime'] == q(j0p)
         and rcr['self_map'] == q(self_map) and rcr['contraction'] == q(contraction)
         and rres['target']['read_from'] == 'contract preregistration.target'
         and rch['contract_snapshot_bound']['contract_sha256'] == CONTRACT_SHA
         and fres['check_py_sha256_recorded_before_evaluation'] == sha(FWD / 'check.py')
         and rres['check_py_sha256'] == sha(REV / 'check.py'),
         'target_and_constants_read_from_hash_checked_snapshot')

    # ================= findings on ledger labels and a reverse mutation label
    eps2 = fm['eps_fwd']
    dp = F(fres['tiers']['+']['ii']['density_part_of_D'])
    true_part = fm['D_fwd'] - 2 * eps2
    need(dp == 2 * eps2 * eps2 / (1 + eps2 * eps2) and true_part == 2 * eps2 * eps2 * (1 - eps2) / (1 + eps2 * eps2)
         and dp - true_part == 2 * eps2 ** 3 / (1 + eps2 ** 2) and dp > true_part,
         'finding_forward_density_ledger_label', exported=q(dp), exact_D_minus_2eps=q(true_part),
         excess_preview=preview(dp - true_part),
         finding='the exported density_part_of_D=2eps^2/(1+eps^2) is an upper bound on D-2eps=2eps^2(1-eps)/(1+eps^2), not an identity; D itself is exact; non-blocking')
    msg = rch['reset_budget_recomputed']['rejected_mutations'].get('one_single_factor_group_100', '')
    need('100|tau|' in msg and 2 * 7 * 7 + 2 == 100,
         'finding_reverse_reset_100_label', reverse_message=msg,
         finding='the reverse rejects 100|tau| as a miscount (one single group); 2(7*7)+2=100|tau| is also a valid labelled refinement '
                 '(the singles lie inside R with Haar mean 0); the admitted budget stays 102|tau|; non-blocking')
    plan = json.loads(PLAN.read_text())
    ext = plan['preregistration_vocabulary_extensions']
    need('AX1 (already frozen' in ext['applies_to'] and "tau/24" in ext['selected_triple_alpha_units']
         and con['preregistration']['selected_triple_alpha_units'] == ['tau/24'] * 3,
         'finding_prereg_vocabulary_extension', applies_to=ext['applies_to'],
         finding='the symbolic triple tau/24 in the frozen AX1 preregistration is covered by the plan.json vocabulary extension recorded after the freeze (contract unamended); both checkers parse and verify it')

    # ================= source-edit mutations on temporary copies
    base_f = mutated_run('forward')
    base_r = mutated_run('reverse')
    need(base_f[0] == 0 and base_f[1] == (FWD / 'output/results.json').read_bytes()
         and base_r[0] == 0 and base_r[1] == (REV / 'output/results.json').read_bytes()
         and validate_producer_values(json.loads(base_f[1]), 'forward', cap)
         and validate_producer_values(json.loads(base_r[1]), 'reverse', cap),
         'mutation_harness_unmutated_copies_reproduce_frozen_results')
    must_abort = [
        ('forward', 'selected_row_relabelled_omitted',
         {'edits': [("{'orientation': 'xy', 'r': (0, 1, 2), 's': (0,), 'support': ((0, 0, 0),), 'role': 'selected'}",
                     "{'orientation': 'xy', 'r': (0, 1, 2), 's': (0,), 'support': ((0, 0, 0),), 'role': 'omitted'}")]}),
        ('forward', 'uniform_coefficient_quarter',
         {'edits': [("UNIFORM_COEFFICIENT_OVER_TAU = Q(-1, 3)", "UNIFORM_COEFFICIENT_OVER_TAU = Q(-1, 4)")]}),
        ('forward', 'single_groups_dropped_J_28', {'edits': [("    singles_per_site = 1\n", "    singles_per_site = 0\n")]}),
        ('forward', 'reset_with_gap_one', {'edits': [("    eps_R = reset / onsite_gap\n", "    eps_R = reset / 1\n")]}),
        ('forward', 'exp_bound_8_over_7_dropped',
         {'edits': [("    GR = 16 * Q(8, 7) * (1 + 10 * R)\n", "    GR = 16 * (1 + 10 * R)\n")]}),
        ('forward', 'incident_stars_outgoing_only',
         {'edits': [("    incident = sorted({sub(u, d) for u in COVER_R for d in S_STAR})\n",
                     "    incident = sorted({u for u in COVER_R})\n")]}),
        ('forward', 'first_order_count_49',
         {'edits': [("    t1_per_tau = counts['faces_per_factor'] * coef\n",
                     "    t1_per_tau = (counts['faces_per_factor'] - 3) * coef\n")]}),
        ('forward', 'am2_remainder_zeroed', {'edits': [("        rem = GpR * J * t\n", "        rem = 0 * J * t\n")]}),
        ('forward', 'flip_set_x_links_keyed_to_z',
         {'edits': [("(d == 0 and p[1] % 2 == 0)", "(d == 0 and p[2] % 2 == 0)")]}),
        ('forward', 'weak_coupling_flag_true',
         {'edits': [("    claim_flags = {'continuum_claim': False, 'uniform_wilson_claim': True, 'weak_coupling_claim': False,",
                     "    claim_flags = {'continuum_claim': False, 'uniform_wilson_claim': True, 'weak_coupling_claim': True,")]}),
        ('forward', 'contract_target_byte_edit_no_rehash',
         {'contract_edit': (b'"value": "1/2500000"', b'"value": "1/1000000"')}),
        ('forward', 'contract_target_rehashed_1_3000000',
         {'contract_edit': (b'"value": "1/2500000"', b'"value": "1/3000000"'), 'rehash': True}),
        ('forward', 'undeclared_input_reverse_report', {'extra_input': 'research/round32/reverse/ax1/report.md'}),
        ('reverse', 'selected_row_relabelled_omitted',
         {'edits': [("    ('xy', (0, 1, 2), (0,), 3, ((0, 0, 0),), 'selected'),\n",
                     "    ('xy', (0, 1, 2), (0,), 3, ((0, 0, 0),), 'omitted'),\n")]}),
        ('reverse', 'uniform_coefficient_quarter',
         {'edits': [("FACE_COEFF_NORMALIZED = Q(-1, 3)", "FACE_COEFF_NORMALIZED = Q(-1, 4)")]}),
        ('reverse', 'single_groups_dropped_J_28',
         {'edits': [("    single_units = Q(len(selected), 3)\n", "    single_units = Q(0) * len(selected)\n")]}),
        ('reverse', 'onsite_gap_one',
         {'edits': [("ONSITE_GAP = ALPHA_OVER_DELTA * CASIMIR_HALF ", "ONSITE_GAP = Q(1) + 0 * CASIMIR_HALF ")]}),
        ('reverse', 'am2_remainder_zeroed',
         {'edits': [("if variant == 'directed_remainder' else K * T\n", "if variant == 'directed_remainder' else 0 * K * T\n")]}),
        ('reverse', 'flip_set_links_keyed_to_own_direction',
         {'edits': [("    return p[(d + 1) % 3] % 2 == 0\n", "    return p[d] % 2 == 0\n")]}),
        ('reverse', 'weak_coupling_flag_true',
         {'edits': [("    'weak_coupling_claim': False,\n", "    'weak_coupling_claim': True,\n")]}),
        ('reverse', 'contract_target_byte_edit_no_rehash',
         {'contract_edit': (b'"value": "1/2500000"', b'"value": "1/1000000"')}),
        ('reverse', 'a1_pinned_to_52_faces',
         {'edits': [("        a1 = coeff * certified_count(COUNTS['faces_meeting_R'], 'faces meeting R')\n",
                     "        a1 = coeff * certified_count(COUNTS['faces_per_factor'], 'faces meeting R')\n")]}),
        ('reverse', 'fidelity_headline_halved',
         {'edits': [("    return 2 * eps, ceil_to(2 * eps / lo), 2 * eps * (1 + eps) / (1 + eps * eps)\n",
                     "    return eps, ceil_to(2 * eps / lo), 2 * eps * (1 + eps) / (1 + eps * eps)\n")]}),
        ('reverse', 'skeptic_triage_added_to_inputs', {'extra_input': 'research/round32/skeptic/triage.md'}),
        ('reverse', 'forward_report_added_to_inputs', {'extra_input': 'research/round32/forward/ax1/report.md'}),
    ]
    receipts = []
    for direction, label, spec in must_abort:
        code, results, last = mutated_run(direction, **spec)
        need(code != 0 and results is None, 'mutation_aborts_%s_%s' % (direction, label), last_error_line=last)
        receipts.append({'direction': direction, 'mutation': label, 'producer_aborted': True, 'last_error_line': last})

    # reads-from-contract demonstration: a coherent rehashed target 1/3000000 (still feasible, still met) is
    # recorded by the reverse, which reads the target from the snapshot; the forward aborts on its pinned target.
    code, results, last = mutated_run('reverse', contract_edit=(b'"value": "1/2500000"', b'"value": "1/3000000"'), rehash=True)
    tampered = json.loads(results) if results is not None else None
    need(code == 0 and tampered is not None and tampered['target']['value'] == '1/3000000'
         and {c['id']: c for c in tampered['checks']}['contract_candidates_compared_after_derivation']['read_from_contract']['target'] == '1/3000000',
         'reverse_reads_target_from_snapshot_rehashed_tamper_recorded',
         finding='the reverse records a coherently rehashed feasible target (1/3000000) read from the snapshot; the forward aborts on it '
                 'because it pins the target to 1/2500000 and to the acceptance text; a rehash needs a check.py edit, which freeze.json binds')
    receipts.append({'direction': 'reverse', 'mutation': 'contract_target_rehashed_1_3000000', 'producer_aborted': False,
                     'recorded_target': '1/3000000', 'note': 'reads-from-contract demonstration, not a rejection'})

    silent = [
        ('forward', 'density_form_replaced_by_2eps',
         {'edits': [("    return 2 * eps * (1 + eps) / (1 + eps * eps)\n", "    return 2 * eps\n")]}),
        ('forward', 'two_creation_term_dropped', {'edits': [("    return 2 * t + t * t\n", "    return 2 * t\n")]}),
        ('reverse', 'two_creation_term_dropped',
         {'edits': [("    return terms['a1'].value + 2 * terms['rho'].value + terms['T'].value ** 2\n",
                     "    return terms['a1'].value + 2 * terms['rho'].value\n")]}),
    ]
    for direction, label, spec in silent:
        code, results, last = mutated_run(direction, **spec)
        caught, reason = False, ''
        if code == 0 and results is not None:
            try:
                validate_producer_values(json.loads(results), direction, cap)
            except Rejected as exc:
                caught, reason = True, str(exc)
        need(code == 0 and results is not None and caught
             and results != ((FWD if direction == 'forward' else REV) / 'output/results.json').read_bytes(),
             'silent_edit_caught_by_review_%s_%s' % (direction, label), producer_exit=code, review_rejection=reason)
        receipts.append({'direction': direction, 'mutation': label, 'producer_aborted': False,
                         'caught_by_skeptic_value_validator': True, 'reason': reason})

    exact = {
        'g4_at_cap': q(96 / cap), 'J_prime_over_tau': '29', 'J0_prime': q(j0p), 'self_map': q(self_map),
        'contraction': q(contraction), 'reset_over_tau': str(reset), 'eps_R_over_tau': '17',
        'B_N_over_tau': '51/8', 'k_prime_over_tau': '51/4', 'C_F_over_tau_per_site': '58', 'Phi_F_crude_over_tau': '2349',
        'counts': {'stars_R': 7, 'single_groups_R': 2, 'selected_faces_R': 6, 'faces_charged': 153, 'faces_meeting_R': 88,
                   'faces_inside_R': 16, 'per_factor': 52, 'per_factor_bound': 96, 'R_bound': 168},
        't1_prime': q(fm['t1']), 'T_prime': q(fm['T']), 'rho_prime': q(fm['rho']), 'a1_prime': q(fm['a1']),
        'eps_forward': q(fm['eps_fwd']), 'eps_reverse': q(fm['eps_rev']),
        'D_ii_forward': q(fm['D_fwd']), 'D_ii_reverse': q(fm['D_rev']), 'D_ii_reverse_density_form': q(fm['D_rev_density']),
        'D_i_forward': q(cr['D_fwd']), 'D_i_reverse': q(cr['D_rev']),
        'D_ii_recommended_binding': q(fm['D_fwd']),
        'first_order_at_cap': [q(cap / 144), q(-cap / 144)],
        'D_ii_av1_reproduced': q(av1_d),
    }
    previews = {
        'D_ii_forward': preview(fm['D_fwd']), 'D_ii_reverse': preview(fm['D_rev']),
        'D_ii_reverse_density_form': preview(fm['D_rev_density']), 'D_i_forward': preview(cr['D_fwd']),
        'D_i_reverse': preview(cr['D_rev']), 'ratio_forward_over_reverse': preview(fm['D_fwd'] / fm['D_rev'], 9),
        'ax2_radius_with_binding': preview(Fup(fm['D_fwd'])), 'target_over_binding': preview(target / fm['D_fwd'], 6),
        'note': 'decimal previews only; every Boolean above was decided on exact rationals',
    }
    return {
        'schema': 'hnm-r32-skeptic-postcomparison-v1', 'loop': 'AX1', 'stage': 'post_comparison',
        'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'model-agent skeptic with correlated ancestry; not human peer review or formal verification',
        'contract_sha256': CONTRACT_SHA, 'exact': exact, 'previews': previews,
        'mutation_receipts': receipts, 'passed': True, 'checks': CHECKS, 'checks_count': len(CHECKS),
    }


def main():
    ap = argparse.ArgumentParser(description='AX1 post-comparison skeptic checks')
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
    print(json.dumps({'loop': 'AX1', 'stage': 'post_comparison', 'checks': result['checks_count'],
                      'D_ii_binding': result['previews']['D_ii_forward'],
                      'mutations': len(result['mutation_receipts'])}, sort_keys=True))


if __name__ == '__main__':
    main()
