#!/usr/bin/env python3
"""AV1 post-comparison skeptic checks, written after both producer freezes.

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated
ancestry; not human peer review or formal verification.

What this adds to the frozen pre-comparison package (av1_check.py):
  * exact recomputation of every exported tier constant of both producers from
    the skeptic's own formulas, with a squared comparison certifying that the
    reverse's rounded 2eps/sqrt(1+eps^2) rationals are upper bounds;
  * the relation between the two tier-(ii) numbers (eps_rev<=eps_fwd, and
    D_rev<=D_fwd; the forward value is certified by both inequalities);
  * the I1 table parsed from the report and compared with both producers'
    encoded tables, and the counts 49/15/82/10 re-derived;
  * an AST audit of how each producer implements the 25 contract control ids;
  * source-mutation replays: each producer closure is copied to a temporary
    tree outside the checkout, one damaging edit is applied, and the run must
    abort; an unmutated copy must reproduce the frozen results.json exactly.

Standard library only; exact Fractions decide every Boolean; failures are
explicit exceptions (never assert), so output bytes match under python -O.

Usage: python3 -B research/round32/skeptic/av1_postreview_check.py --output /abs/fresh/dir
"""
import argparse
import ast
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CONTRACT = ROOT / 'research/round32/contracts/av1.json'
CONTRACT_SHA = 'c7018519188b953e48e56715a72c90491389e42243ef691cb59dc5b038e91e40'
FWD = ROOT / 'research/round32/forward/av1'
REV = ROOT / 'research/round32/reverse/av1'
I1_REPORT = ROOT / 'research/round21/forward/i1/report.md'
PRE_RESULTS = HERE / 'av1-independent/results.json'
FWD_D_II_TASK = '585079838465912592144137406066050/42981220507576537932303142777593983768257'
REV_D_II_TASK = '113902305553947264976096174312887/10000000000000000000000000000000000000000'


class ReviewFailure(Exception):
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


def preview(x, digits=10):
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


# ------------------------------------------------------------ exact helpers
def exp_upper(x, n=20):
    """exp(x) upper bound for 0<=x<=1/2: partial sum plus geometric tail."""
    x = F(x)
    if not (0 <= x <= F(1, 2)):
        raise ReviewFailure('exp argument')
    s, term = F(0), F(1)
    for k in range(n + 1):
        s += term
        term = term * x / (k + 1)
    return s + term / (1 - x / (n + 2))


def pi_bracket():
    def atan_inv(k, n=30):
        a, b = F(0), F(0)
        for j in range(n):
            b = a
            a += F((-1) ** j, (2 * j + 1) * k ** (2 * j + 1))
        return min(a, b), max(a, b)
    a5, a239 = atan_inv(5), atan_inv(239)
    return 16 * a5[0] - 4 * a239[1], 16 * a5[1] - 4 * a239[0]


def f_fwd(e):
    """Forward explicit-density bound 2e(1+e)/(1+e^2)."""
    return 2 * e * (1 + e) / (1 + e * e)


def is_upper_of_g(D, e):
    """D >= 2e/sqrt(1+e^2), decided by squaring (both sides nonnegative)."""
    return D >= 0 and D * D * (1 + e * e) >= 4 * e * e


def g_bracket(e, den=10 ** 45):
    """Rational bracket of 2e/sqrt(1+e^2)."""
    y = 1 + e * e
    s = isqrt(y.numerator * den * den // y.denominator)
    lo, hi = F(s, den), F(s + 1, den)
    if not (lo * lo <= y <= hi * hi):
        raise ReviewFailure('sqrt bracket')
    return 2 * e / hi, 2 * e / lo


# ------------------------------------------------------------ I1 table
OFFSET = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}
ORIENT = {'xy': (0, 1), 'xz': (0, 2), 'yz': (1, 2)}
E3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))


def vadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def vsub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def parse_i1(text):
    row = re.compile(r'^\|\s*(xy|xz|yz):\s*r=([0-9,]+);\s*s=([0-9,]+)\s*\|\s*(\d+)\s*\|'
                     r'\s*`\{([^}]*)\}`\s*\|\s*(selected|omitted)\s*\|\s*$')
    out = set()
    for line in text.splitlines():
        m = row.match(line.strip())
        if not m:
            continue
        rs = [int(x) for x in m.group(2).split(',')]
        ss = [int(x) for x in m.group(3).split(',')]
        if int(m.group(4)) != len(rs) * len(ss):
            raise ReviewFailure('I1 row count')
        sup = frozenset(OFFSET[x.strip()] for x in m.group(5).split(','))
        for r in rs:
            for s in ss:
                out.add((m.group(1), r, s, sup, m.group(6)))
    return out


def geometry_table():
    """I1.1/I1.4 from first principles: tails (4b_x+r,2b_y+s,b_z), owners of p,p+e_a,p+e_c."""
    def owner(p):
        return (p[0] // 4, p[1] // 2, p[2])
    out = set()
    for r in range(4):
        for s in range(2):
            p = (r, s, 0)
            for name, (a, c) in ORIENT.items():
                sup = frozenset(owner(x) for x in (p, vadd(p, E3[a]), vadd(p, E3[c])))
                role = 'selected' if (name == 'xy' and s == 0 and r <= 2) else 'omitted'
                out.add((name, r, s, sup, role))
    return out


def literal_table(path):
    tree = ast.parse(path.read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'I1_TABLE' for t in node.targets):
            return ast.literal_eval(node.value)
    raise ReviewFailure('I1_TABLE literal not found in ' + path.as_posix())


def expand_forward_table(rows):
    return {(r['orientation'], x, y, frozenset(r['support']), r['role']) for r in rows for x in r['r'] for y in r['s']}


def expand_reverse_table(rows):
    out = set()
    for name, rs, ss, count, sup, role in rows:
        if count != len(rs) * len(ss):
            raise ReviewFailure('reverse table count')
        for x in rs:
            for y in ss:
                out.add((name, x, y, frozenset(sup), role))
    return out


def counts_from(table):
    sups = [c[3] for c in sorted(table, key=lambda c: (c[0], c[1], c[2])) if c[4] == 'omitted']
    R = ((0, 0, 0), (0, 0, 1))

    def faces_at(u):
        return {(vsub(u, d), k) for k, S in enumerate(sups) for d in S}

    def owners(f):
        return frozenset(vadd(f[0], d) for d in sups[f[1]])
    at0 = faces_at(R[0])
    mult = {}
    for f in at0:
        mult[owners(f)] = mult.get(owners(f), 0) + 1
    meet = faces_at(R[0]) | faces_at(R[1])
    inside = [f for f in meet if owners(f) <= frozenset(R)]
    contain = [f for f in meet if frozenset(R) <= owners(f)]
    meet_sets = {}
    for f in meet:
        meet_sets[owners(f)] = meet_sets.get(owners(f), 0) + 1
    return {'omitted': len(sups), 'per_factor': len(at0), 'owner_sets': len(mult), 'meet_R': len(meet),
            'inside_R': len(inside), 'contain_R': len(contain), 'mult': sorted(mult.values()),
            'meet_sets': sorted(meet_sets.values())}


# ------------------------------------------------------------ control audit (AST)
def control_audit(path, style, ids):
    tree = ast.parse(path.read_text())
    found = {}
    # names that collect rejected(...) results, e.g. muts.append(rejected(...)) in a loop
    collectors = set()
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'append'
                and isinstance(node.func.value, ast.Name) and node.args and isinstance(node.args[0], ast.Call)
                and isinstance(node.args[0].func, ast.Name) and node.args[0].func.id == 'rejected'):
            collectors.add(node.func.value.id)
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.args
                and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str)):
            continue
        cid = node.args[0].value
        if cid not in ids:
            continue
        name = node.func.id
        if style == 'forward' and name == 'check':
            mutates = any((isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'rejected')
                          or (isinstance(n, ast.Name) and n.id in collectors)
                          for n in ast.walk(node))
            found.setdefault(cid, []).append('check+rejected' if mutates else 'check_positive_only')
        elif style == 'reverse' and name in ('control', 'record'):
            if name == 'control':
                arg = node.args[1] if len(node.args) > 1 else None
                nonempty = (isinstance(arg, ast.List) and len(arg.elts) > 0) or isinstance(arg, (ast.ListComp, ast.BinOp))
                found.setdefault(cid, []).append('control_with_mutations' if nonempty else 'control_empty')
            else:
                found.setdefault(cid, []).append('record_positive_only')
    return found


# ------------------------------------------------------------ source-mutation replays
def mutated_run(src, direction, edits=(), extra_input=None, contract_replace=None):
    with tempfile.TemporaryDirectory(prefix='hnm-r32-av1-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / 'research/round32' / direction / 'av1'
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        code = (dst / 'check.py').read_text()
        for old, new in edits:
            if code.count(old) != 1:
                raise ReviewFailure('mutation anchor not unique in %s check.py: %r' % (direction, old[:60]))
            code = code.replace(old, new)
        (dst / 'check.py').write_text(code)
        if extra_input is not None:
            extra = dst / 'inputs' / extra_input
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text('skeptic mutation fixture\n')
        if contract_replace is not None:
            cpath = dst / 'inputs/research/round32/contracts/av1.json'
            raw = cpath.read_bytes()
            old, new = contract_replace
            if raw.count(old) != 1:
                raise ReviewFailure('contract mutation anchor not unique')
            cpath.write_bytes(raw.replace(old, new))
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(dst / 'check.py'), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(repo))
        results = (out / 'results.json').read_bytes() if (out / 'results.json').is_file() else None
        last = done.stderr.strip().splitlines()[-1] if done.stderr.strip() else ''
        return done.returncode, results, last.replace(tmp, '<tmp>')


def run():
    raw = CONTRACT.read_bytes()
    need(sha(CONTRACT) == CONTRACT_SHA, 'contract_hash', contract_sha256=CONTRACT_SHA)
    contract = json.loads(raw)
    target = F(contract['preregistration']['target']['value'])
    secondary = F(1, 10 ** int(re.search(r'report against 10\^-(\d+)', contract['required'][8]).group(1)))
    tau = F(contract['parameters']['tau_cap'])
    tau_s = tau / 100
    fr = json.loads((FWD / 'output/results.json').read_text())
    rr = json.loads((REV / 'output/results.json').read_text())
    pre = json.loads(PRE_RESULTS.read_text())
    need(fr['contract_sha256'] == CONTRACT_SHA and rr['contract_snapshot_sha256'] == CONTRACT_SHA,
         'both_producers_bound_to_frozen_contract')
    need(target == F(1, 2500000) and secondary == F(1, 10 ** 6)
         and fr['targets']['target_D_ii'] == q(target) and rr['target']['value'] == q(target)
         and fr['targets']['secondary'] == q(secondary) and rr['secondary_comparison']['value'] == q(secondary),
         'target_and_secondary_read_from_contract_by_both', target=q(target), secondary=q(secondary))

    # ---------------- I1 table and counts
    parsed = parse_i1(I1_REPORT.read_text())
    geo = geometry_table()
    ft = expand_forward_table(literal_table(FWD / 'check.py'))
    rt = expand_reverse_table(literal_table(REV / 'check.py'))
    need(len(parsed) == 24 and parsed == geo == ft == rt, 'i1_table_report_geometry_and_both_encodings_agree',
         classes=len(parsed), omitted=sum(1 for c in parsed if c[4] == 'omitted'))
    cnt = counts_from(parsed)
    derived = (cnt['per_factor'], cnt['owner_sets'], cnt['meet_R'], cnt['inside_R'])
    need(derived == (49, 15, 82, 10) and cnt['contain_R'] == 16 and cnt['mult'] == [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 10, 10]
         and len(cnt['meet_sets']) == 27 and sum(cnt['meet_sets']) == 82,
         'counts_49_15_82_10_rederived', derived=list(derived), faces_containing_R=cnt['contain_R'],
         owner_set_multiplicities=cnt['mult'], owner_sets_meeting_R=len(cnt['meet_sets']))
    fe = fr['face_enumeration']
    rd = rr['face_enumeration']['derived']
    need((fe['faces_per_factor'], fe['owner_sets_per_factor'], fe['faces_meeting_R'], fe['faces_inside_R']) == derived
         and (rd['faces_per_factor'], rd['owner_sets_per_factor'], rd['faces_meeting_R'], rd['faces_inside_R']) == derived
         and fe['multiplicities'] == cnt['mult'] and sorted(rr['face_enumeration']['owner_set_face_counts_at_origin'].values()) == cnt['mult'],
         'both_producers_export_the_derived_counts')

    # ---------------- AM2 constants
    e8 = exp_upper(F(1, 8))
    GR = 16 * e8 * (1 + 10 * F(1, 64))
    GpR = 16 * e8 * (18 + 80 * F(1, 64))
    J = 4 * 21 * F(1, 3) * tau
    need(e8 < F(8, 7) and GR < F(148, 7) and GpR < 352 and J == F(7, 25000000) and J * F(148, 7) < F(1, 64)
         and 2 * J * 352 < 1, 'am2_constants_rechecked', exp_one_eighth_upper=q(e8), J0=q(J))
    k = 1
    ok_coeff = True
    while k <= 40:
        c = F(16 * 8 ** k) * (1 + F(5 * k, 4))
        ok_coeff = ok_coeff and c / (8 ** k) / _fact(k) <= 36
        k += 1
    need(ok_coeff and all(5 * kk * kk + 4 * kk - 5 >= 0 for kk in range(1, 200)),
         'forward_sharper_remainder_majorant_valid',
         statement='G(t)-16<=288t/(1-8t): coefficient 16(1+5k/4)/k! <= 36 at k=1 and decreasing (ratio (5k+9)/((5k+4)(k+1))<=1)')

    # ---------------- tier (i)
    t_i = J * F(148, 7)
    eps_i = 2 * t_i + t_i * t_i
    need(fr['tiers']['+']['i']['t'] == q(t_i) and fr['tiers']['+']['i']['eps'] == q(eps_i)
         and F(fr['tiers']['+']['i']['D']) == f_fwd(eps_i) and fr['tiers']['-']['i']['D'] == fr['tiers']['+']['i']['D'],
         'forward_tier_i_exact', D_i=fr['tiers']['+']['i']['D'], preview=preview(f_fwd(eps_i)))
    Dri = F(rr['D_i']['+'])
    need(rr['tiers']['tier_i']['+']['epsilon'] == q(eps_i) and is_upper_of_g(Dri, eps_i)
         and not is_upper_of_g(Dri - F(1, 10 ** 40), eps_i) and rr['D_i']['-'] == rr['D_i']['+'],
         'reverse_tier_i_directed_upper', D_i=q(Dri), preview=preview(Dri))
    need(f_fwd(eps_i) > target and Dri > target and f_fwd(eps_i) > secondary and Dri > secondary,
         'tier_i_fails_both_targets_in_both_producers')
    fi_it = F(fr['tiers']['+']['i_iterated']['t'])
    fi_it_expected = J * 16 * (1 + 10 * t_i) / (1 - 8 * t_i)
    ri_it = [F(x) for x in rr['tiers']['tier_i_iterated']['+']['t_iterates']]
    need(fi_it == fi_it_expected and fi_it < t_i and all(ri_it[i + 1] <= ri_it[i] for i in range(len(ri_it) - 1))
         and all(ri_it[i + 1] >= J * 16 * (1 + 10 * ri_it[i]) for i in range(len(ri_it) - 1)),
         'iterated_tier_i_steps_valid_directions', forward_t=q(fi_it), reverse_t=q(ri_it[-1]))

    # ---------------- tier (ii): forward
    t1 = 49 * tau / 144
    T = t1 / (1 - 352 * J)
    rho = 352 * J * T
    eps_f = 2 * T + T * T
    Df = f_fwd(eps_f)
    fii = fr['tiers']['+']['ii']
    need(q(Df) == FWD_D_II_TASK and fii['D'] == q(Df) and fr['tiers']['-']['ii']['D'] == q(Df)
         and fii['t1'] == q(t1) and fii['t'] == q(T) and fii['remainder'] == q(rho) and fii['eps'] == q(eps_f)
         and T == t1 + rho and pre['tiers']['+1e-8']['tier_ii']['D_forward'] == q(Df),
         'forward_tier_ii_exact_and_equals_skeptic_precomparison', D_ii=q(Df), preview=preview(Df), eps=q(eps_f),
         t=q(T), remainder=q(rho))
    # ---------------- tier (ii): reverse
    a1 = 82 * tau / 144
    eps_r = a1 + 2 * rho + T * T
    Dr = F(rr['D_ii']['+'])
    rii = rr['tiers']['tier_ii']['+']
    need(q(Dr) == REV_D_II_TASK and rii['epsilon'] == q(eps_r) and rii['a1_first_order_meeting_R'] == q(a1)
         and rii['remainder_anchored_upper'] == q(rho) and rii['T_self_consistent'] == q(T)
         and rr['D_ii']['-'] == rr['D_ii']['+'] and is_upper_of_g(Dr, eps_r)
         and not is_upper_of_g(Dr - F(1, 10 ** 40), eps_r),
         'reverse_tier_ii_directed_upper_rechecked', D_ii=q(Dr), preview=preview(Dr), eps=q(eps_r), a1=q(a1))
    g_f = g_bracket(eps_f)
    need(eps_r < eps_f and a1 < 2 * t1 and 2 * t1 + 2 * rho == 2 * T and Dr < Df and g_f[1] <= Df
         and f_fwd(eps_r) > Dr,
         'tier_ii_relation_between_routes', eps_ratio_preview=preview(eps_f / eps_r),
         D_ratio_preview=preview(Df / Dr), fidelity_at_forward_eps_upper=q(g_f[1]),
         forward_formula_at_reverse_eps=preview(f_fwd(eps_r)),
         statement='eps_rev=a1+2rho+T^2<=2T+T^2=eps_fwd because 82<98; the forward D_ii is certified by both inequalities; '
                   'the reverse D_ii needs the fidelity (or purification) inequality, since 2e(1+e)/(1+e^2) at eps_rev exceeds it')
    need(Df <= target and Dr <= target and Df <= secondary and Dr <= secondary, 'tier_ii_meets_4e-7_and_1e-6_both_producers',
         margin_forward=preview(target / Df, 6), margin_reverse=preview(target / Dr, 6))

    # ---------------- scaling
    t_s = 49 * tau_s / 144 / (1 - 352 * 28 * tau_s)
    ratio_f = Df / f_fwd(2 * t_s + t_s * t_s)
    ti_s = 28 * tau_s * F(148, 7)
    ratio_fi = f_fwd(eps_i) / f_fwd(2 * ti_s + ti_s * ti_s)
    tsc = next(c for c in fr['checks'] if c['id'] == 'tau_scaling_exponent')
    Js = 28 * tau_s
    Ts = 49 * tau_s / 144 / (1 - 352 * Js)
    eps_rs = 82 * tau_s / 144 + 2 * 352 * Js * Ts + Ts * Ts
    gs = g_bracket(eps_rs)
    gr = g_bracket(eps_r)
    rev_ratio_bracket = (gr[0] / gs[1], gr[1] / gs[0])
    need(tsc['ratio_tier_ii'] == q(ratio_f) and tsc['ratio_tier_i'] == q(ratio_fi)
         and 99 <= ratio_f <= 101 and 99 <= ratio_fi <= 101 and 99 <= rev_ratio_bracket[0] and rev_ratio_bracket[1] <= 101
         and rr['tiers']['tier_ii']['scaling_point']['epsilon'] == q(eps_rs),
         'scaling_ratios_linear_rechecked', forward_ii=preview(ratio_f, 9), forward_i=preview(ratio_fi, 9),
         reverse_ii_bracket=[preview(rev_ratio_bracket[0], 9), preview(rev_ratio_bracket[1], 9)], at4_ratio='10')

    # ---------------- AV2 arithmetic
    plo, phi = pi_bracket()

    def Fup(D):
        return 2 * (D + D * D) + F(49, 10 ** 8) / plo

    def Flo(D):
        return 2 * (D + D * D) + F(49, 10 ** 8) / phi
    goal = F(1, 10 ** 6)
    need(F(314159, 100000) < plo < phi < F(314160, 100000) and Fup(Df) <= goal and Fup(Dr) <= goal
         and Fup(target) <= goal and Fup(F(422, 10 ** 9)) <= goal and Flo(F(423, 10 ** 9)) > goal
         and Flo(f_fwd(eps_i)) > goal, 'av2_feasibility_rechecked',
         radius_with_forward_D_ii=preview(Fup(Df), 8), radius_with_reverse_D_ii=preview(Fup(Dr), 8))

    # ---------------- consequences
    fc, rc = fr['consequences']['ii+'], rr['consequences']['tier_ii+']
    need(fc['omega_W_interval'] == [q(-Df), q(Df)] and fc['omega_W2_interval'] == [q(F(1, 4) - Df / 2), q(F(1, 4) + Df / 2)]
         and fc['mean_square_charge_m2_upper'] == q(Df * Df)
         and rc['abs_omega_W_upper'] == q(Dr) and rc['omega_W2_interval'] == [q(F(1, 4) - Dr / 2), q(F(1, 4) + Dr / 2)]
         and F(rc['variance_interval'][0]) <= F(1, 4) - Dr / 2 - Dr * Dr,
         'consequences_rechecked_tier_ii')

    # ---------------- claim flags
    six = ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift', 'scientific_priority_verified',
           'euclidean_node_certified', 'first_order_parity_claim')
    need(all(fr[k] is False and rr[k] is False for k in six)
         and fr['uniqueness_claimed'] is False and fr['whole_sequence_convergence_claimed'] is False
         and fr['rate_in_N_claimed'] is False and 'uniqueness_claimed' not in rr,
         'claim_flags_false', reverse_extra_passage_flags_absent=True)

    # ---------------- control audit
    ids = list(contract['controls'])
    fa = control_audit(FWD / 'check.py', 'forward', ids)
    ra = control_audit(REV / 'check.py', 'reverse', ids)
    f_positive = sorted(c for c in ids if fa.get(c) == ['check_positive_only'])
    f_mut = sorted(c for c in ids if fa.get(c) == ['check+rejected'])
    r_mut = sorted(c for c in ids if ra.get(c) == ['control_with_mutations'])
    fids = {c['id'] for c in fr['checks']}
    rids = {c['id'] for c in rr['checks']}
    need(set(ids) <= fids and set(ids) <= rids and len(ids) == 25, 'all_25_control_ids_executed_by_both')
    need(len(r_mut) == 25 and all(c.get('kind') == 'damaging_mutation_control' and c.get('rejected_mutations')
                                  for c in rr['checks'] if c['id'] in ids),
         'reverse_all_25_controls_are_damaging_mutations')
    need(len(f_mut) == 22 and f_positive == ['av2_feasibility_threshold', 'first_order_face_enumeration',
                                             'no_priority_or_continuum_claim'],
         'forward_22_mutation_controls_3_positive_only', forward_positive_only=f_positive,
         note='finding: these three forward ids are exact positive checks without a rejected(...) mutation')
    need('error_terms_itemized' in fr and sorted(fr['error_terms_itemized']) == sorted(contract['preregistration']['error_terms_itemized'])
         and 'error_terms_itemized' not in rr, 'error_ledger_forward_present_reverse_absent',
         note='finding: the reverse charges every term in its text but exports no six-name ledger')
    fsrc, rsrc = (FWD / 'check.py').read_text(), (REV / 'check.py').read_text()
    need("(BASE / 'inputs' / CONTRACT_REL).read_bytes()" in fsrc and "pre['target']" in fsrc
         and "(INPUTS / CONTRACT_REL).read_bytes()" in rsrc and "contract['preregistration']['target']['value']" in rsrc
         and '2500000' not in fsrc and '2500000' not in rsrc, 'contract_snapshot_read_path_and_no_target_literal')

    # ---------------- source-mutation replays
    base_f = mutated_run(FWD, 'forward')
    base_r = mutated_run(REV, 'reverse')
    need(base_f[0] == 0 and base_f[1] == (FWD / 'output/results.json').read_bytes()
         and base_r[0] == 0 and base_r[1] == (REV / 'output/results.json').read_bytes(),
         'mutation_harness_unmutated_copies_reproduce_frozen_results')
    mutations = [
        ('forward', 'count_derivation_drops_a_face', {'edits': [('    at0 = faces_containing(ORIGIN, classes)\n',
                                                                 '    at0 = faces_containing(ORIGIN, classes)[1:]\n')]}),
        ('forward', 't1_count_copied_as_48', {'edits': [("t1_per_tau = counts['faces_per_factor'] * coef",
                                                          't1_per_tau = 48 * coef')]}),
        ('forward', 'remainder_set_to_zero', {'edits': [('        rem = L * J * t\n', '        rem = 0 * L * J * t\n')]}),
        ('forward', 'continuum_claim_true', {'edits': [("claim_flags = {'continuum_claim': False,", "claim_flags = {'continuum_claim': True,")]}),
        ('forward', 'extra_undeclared_input', {'extra_input': 'research/round32/reverse/av1/report.md'}),
        ('forward', 'contract_target_relaxed', {'contract_replace': (b'"value": "1/2500000"', b'"value": "1/1000"')}),
        ('reverse', 'count_derivation_drops_a_face', {'edits': [('    at0 = faces_touching(ORIGIN, supports)\n',
                                                                 '    at0 = faces_touching(ORIGIN, supports)[1:]\n')]}),
        ('reverse', 'i1_table_row_dropped', {'edits': [("    ('yz', (0, 1, 2, 3), (1,), 4, ((0, 0, 0), (0, 1, 0), (0, 0, 1)), 'omitted'),\n", '')]}),
        ('reverse', 'remainder_set_to_zero', {'edits': [('        rho = K * T\n', '        rho = 0 * K * T\n')]}),
        ('reverse', 'continuum_claim_true', {'edits': [("    'continuum_claim': False,\n", "    'continuum_claim': True,\n")]}),
        ('reverse', 'skeptic_triage_added_to_inputs', {'extra_input': 'research/round32/skeptic/triage.md'}),
        ('reverse', 'contract_target_relaxed', {'contract_replace': (b'"value": "1/2500000"', b'"value": "1/1000"')}),
    ]
    receipts = []
    for direction, label, spec in mutations:
        code, results, last = mutated_run(FWD if direction == 'forward' else REV, direction, **spec)
        need(code != 0 and results is None, 'mutation_rejected_%s_%s' % (direction, label), last_error_line=last)
        receipts.append({'direction': direction, 'mutation': label, 'rejected': True, 'last_error_line': last})

    # ---------------- report text
    ftxt, rtxt = (FWD / 'report.md').read_text(), (REV / 'report.md').read_text()
    need('\\tfrac{585079838465912592144137406066050}{42981220507576537932303142777593983768257}' in ftxt
         and '113902305553947264976096174312887/10^40' in rtxt
         and 'Every control is a damaging mutation that must raise an explicit exception.' in ftxt
         and 'no parity argument removes a first-order mean' in rtxt,
         'report_sentences_located', forward_overstatement='Every control is a damaging mutation that must raise an explicit exception.',
         reverse_wording='no parity argument removes a first-order mean')

    exact = {
        'tau': q(tau), 'J0': q(J), 'tier_i_t': q(t_i), 'tier_i_eps': q(eps_i),
        'D_i_forward': q(f_fwd(eps_i)), 'D_i_reverse_upper': q(Dri),
        't1': q(t1), 'T': q(T), 'remainder_352JT': q(rho), 'a1_82_faces': q(a1),
        'eps_ii_forward': q(eps_f), 'eps_ii_reverse': q(eps_r),
        'D_ii_forward': q(Df), 'D_ii_reverse_upper': q(Dr),
        'fidelity_at_forward_eps_bracket': [q(g_f[0]), q(g_f[1])],
    }
    previews = {'D_i_forward': preview(f_fwd(eps_i)), 'D_i_reverse': preview(Dri), 'D_ii_forward': preview(Df),
                'D_ii_reverse': preview(Dr), 'eps_ii_forward': preview(eps_f), 'eps_ii_reverse': preview(eps_r),
                'ratio_forward_over_reverse_D_ii': preview(Df / Dr), 'note': 'decimal previews only'}
    return {
        'schema': 'hnm-r32-skeptic-postcomparison-v1', 'loop': 'AV1', 'stage': 'post_comparison',
        'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'model-agent skeptic with correlated ancestry; not human peer review or formal verification',
        'contract_sha256': CONTRACT_SHA, 'exact': exact, 'previews': previews,
        'forward_controls_positive_only': f_positive, 'mutation_receipts': receipts,
        'passed': True, 'checks': CHECKS, 'checks_count': len(CHECKS),
    }


def _fact(n):
    r = 1
    for i in range(2, n + 1):
        r *= i
    return r


def main():
    ap = argparse.ArgumentParser(description='AV1 post-comparison skeptic checks')
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
    print(json.dumps({'loop': 'AV1', 'stage': 'post_comparison', 'checks': result['checks_count'],
                      'D_ii_forward': result['previews']['D_ii_forward'], 'D_ii_reverse': result['previews']['D_ii_reverse']},
                     sort_keys=True))


if __name__ == '__main__':
    main()
