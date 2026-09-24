#!/usr/bin/env python3
"""AV2 post-comparison skeptic checks, written after both producer freezes.

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated
ancestry (same model family as the advisor, the lenses and both producers); not
human peer review or formal verification.

What this adds to the frozen pre-comparison package (av2_check.py, 69 checks):
  * an exact re-derivation, with the skeptic's own directed enclosures at 10^-70
    (Hutton pi with a Machin overlap; positive-Taylor exp with a geometric tail),
    of the radius E=2(D+D^2)+49|tau|s/pi, the datum, the interval, the free
    reference, the crossover, the retained Poisson failures and the C^1 preview,
    and a check that each producer's exported exact rational is a valid directed
    bound that is not inflated by more than 10^-40;
  * cross-producer equality of the datum (exact) and of the radius (to 10^-40;
    the two exact rationals differ by the stated rounding choices only);
  * the triple, double and simple lower-pole residues by a Leibniz formula (a
    fourth route), compared with the reverse's exported residue polynomial;
  * the pre-registration mirror discrepancy (24 controls against 23 mirrored ids)
    and whether both producers executed the missing id anyway;
  * probes of both calculators (exact inputs only, proved domain, D not an input)
    on temporary copies outside the checkout;
  * source-edit mutations: each producer closure is copied to a temporary tree
    outside the checkout, one damaging edit is applied, and the run must abort;
    an unmutated copy must reproduce the frozen results.json byte for byte.

Standard library only; exact Fractions decide every Boolean; failures are explicit
exceptions (never assert), so the output bytes match under python -O.

Usage: python3 -B research/round32/skeptic/av2_postreview_check.py --output /abs/fresh/dir
"""
import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from math import comb, factorial, isqrt
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
R32 = ROOT / 'research/round32'
CONTRACT = R32 / 'contracts/av2.json'
CONTRACT_SHA = '686458cab7a4e6e65b63f0c6418d51496f66f1aada4897115ff14e8bbfad5687'
GATE = R32 / 'advisor/av1-gate.json'
AT4_REPORT = ROOT / 'research/round31/forward/at4/report.md'
FWD = R32 / 'forward/av2'
REV = R32 / 'reverse/av2'
PRE_RESULTS = HERE / 'av2-independent/results.json'
PRE_FREEZE = HERE / 'av2-independent-freeze.json'
DATUM_TASK = '497870683678639429793424156500617766317/40000000000000000000000000000000000000000'
RADIUS_PREVIEW_TASK = '1.8319675034e-7'
DEN = 10 ** 70
G40 = 10 ** 40


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


def preview(x, digits=11):
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


# ------------------------------------------------------------ directed enclosures (10^-70)
def fl(x, den=DEN):
    x = F(x)
    return F((x.numerator * den) // x.denominator, den)


def ce(x, den=DEN):
    x = F(x)
    return F(-((-x.numerator * den) // x.denominator), den)


def atan_inv(n, terms):
    """atan(1/n): consecutive alternating partial sums bracket the value."""
    s, prev = F(0), F(0)
    for j in range(terms):
        prev = s
        s += F((-1) ** j, (2 * j + 1) * n ** (2 * j + 1))
    return min(prev, s), max(prev, s)


def pi_bracket():
    a3, a7 = atan_inv(3, 90), atan_inv(7, 60)            # Hutton 8atan(1/3)+4atan(1/7)
    lo, hi = fl(8 * a3[0] + 4 * a7[0]), ce(8 * a3[1] + 4 * a7[1])
    m5, m239 = atan_inv(5, 70), atan_inv(239, 20)        # Machin overlap
    mlo, mhi = 16 * m5[0] - 4 * m239[1], 16 * m5[1] - 4 * m239[0]
    if not (mlo <= hi and lo <= mhi and hi - lo <= F(2, DEN)):
        raise ReviewFailure('pi bracket')
    return lo, hi


def exp_bracket(z, terms=60):
    """e^z for rational z>=0: positive Taylor partial sum plus a geometric tail, halving, outward squaring."""
    z = F(z)
    if z < 0:
        raise ReviewFailure('exp argument')
    h = 0
    while z > F(1, 2):
        z /= 2
        h += 1
    s, t = F(0), F(1)
    for k in range(terms + 1):
        s += t
        t = t * z / (k + 1)
    tail = t / (1 - z / (terms + 2))
    lo, hi = fl(s), ce(s + tail)
    for _ in range(h):
        lo, hi = fl(lo * lo), ce(hi * hi)
    return lo, hi


def exp_neg(z):
    lo, hi = exp_bracket(z)
    return fl(1 / hi), ce(1 / lo)


def log_small(y, terms=80):
    y = F(y)
    if not (1 <= y <= 2):
        raise ReviewFailure('log_small domain')
    z = (y - 1) / (y + 1)
    part = 2 * sum((z ** (2 * j + 1) / (2 * j + 1) for j in range(terms)), F(0))
    tail = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
    return part, part + tail


def log_bracket(y):
    y = F(y)
    if y < 1:
        raise ReviewFailure('log domain')
    k = max(0, y.numerator.bit_length() - y.denominator.bit_length() - 1)
    r = y / F(2) ** k
    while r >= 2:
        r /= 2
        k += 1
    lo, hi = log_small(r)
    l2lo, l2hi = log_small(F(2))
    return fl(lo + k * l2lo), ce(hi + k * l2hi)


def sqrt_bracket(y):
    y = F(y)
    r = isqrt((y.numerator * DEN * DEN) // y.denominator)
    lo = F(r, DEN)
    hi = lo if lo * lo == y else F(r + 1, DEN)
    if not (lo * lo <= y <= hi * hi):
        raise ReviewFailure('sqrt bracket')
    return lo, hi


# ------------------------------------------------------------ Gaussian rationals: Leibniz residues
def cmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def cpow(a, n):
    r = (F(1), F(0))
    for _ in range(n):
        r = cmul(r, a)
    return r


def cinv(a):
    n = a[0] * a[0] + a[1] * a[1]
    return (a[0] / n, -a[1] / n)


I_UNIT = (F(0), F(1))


def lower_pole_polynomial(n, s):
    """x<0 branch of int K_n(theta)e^{i theta x}dtheta, K_n=N_n/((s+i theta)(s-i theta)^n), 2 pi N_n=(2s)^n.

    Close below (clockwise): -2 pi i Res_{theta=-is}. With (s-i theta)^n=(-i)^n(theta+is)^n and
    h(theta)=N_n e^{i theta x}/((-i)^n (s+i theta)), Res=h^{(n-1)}(-is)/(n-1)!, expanded by Leibniz:
    d^m/dtheta^m (s+i theta)^-1 = (-1)^m m! i^m (s+i theta)^-(m+1), s+i(-is)=2s, e^{i(-is)x}=e^{sx}.
    Returns (polynomial coefficients of e^{-sx}... times e^{sx}, residue coefficients without N_n/pi).
    """
    s = F(s)
    minus_i_pow = cpow((F(0), F(-1)), n)
    pref = cmul((F(0), F(-1)), cinv(minus_i_pow))                 # -i/(-i)^n
    pref = (pref[0] * (2 * s) ** n / factorial(n - 1), pref[1] * (2 * s) ** n / factorial(n - 1))
    poly = []
    res_rational = []
    for j in range(n):
        m = n - 1 - j
        c = cmul(cpow(I_UNIT, j), cpow(I_UNIT, m))
        c = (c[0] * comb(n - 1, j) * (-1) ** m * factorial(m) / (2 * s) ** (m + 1),
             c[1] * comb(n - 1, j) * (-1) ** m * factorial(m) / (2 * s) ** (m + 1))
        poly.append(cmul(pref, c))
        # residue of e^{i theta x}/((s+i theta)(s-i theta)^n) (the part without N_n): h without N_n
        r = cmul(cinv(minus_i_pow), c)
        res_rational.append((r[0] / factorial(n - 1), r[1] / factorial(n - 1)))
    return poly, res_rational


# ------------------------------------------------------------ source-mutation replays
def mutated_run(src, direction, edits=(), calc_edits=(), extra_input=None, contract_replace=None):
    with tempfile.TemporaryDirectory(prefix='hnm-r32-av2-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / 'research/round32' / direction / 'av2'
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        for fname, changes in (('check.py', edits), ('calculator.py', calc_edits)):
            code = (dst / fname).read_text()
            for old, new in changes:
                if code.count(old) != 1:
                    raise ReviewFailure('mutation anchor not unique in %s %s: %r' % (direction, fname, old[:60]))
                code = code.replace(old, new)
            (dst / fname).write_text(code)
        if extra_input is not None:
            extra = dst / 'inputs' / extra_input
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text('skeptic mutation fixture\n')
        if contract_replace is not None:
            cpath = dst / 'inputs/research/round32/contracts/av2.json'
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
        if any(p.name == '__pycache__' or p.suffix == '.pyc' for p in dst.rglob('*')):
            raise ReviewFailure('interpreter cache written into a mutated copy')
        return done.returncode, results, last.replace(tmp, '<tmp>')


def load_calculator(src, name, tmp):
    dst = Path(tmp) / name
    dst.mkdir()
    shutil.copy2(src / 'calculator.py', dst / 'calculator.py')
    spec = importlib.util.spec_from_file_location(name, str(dst / 'calculator.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def raises(fn, errors):
    try:
        fn()
    except errors as exc:
        return type(exc).__name__
    raise ReviewFailure('calculator accepted an out-of-domain call')


# ------------------------------------------------------------ main computation
def run():
    raw = CONTRACT.read_bytes()
    need(sha(CONTRACT) == CONTRACT_SHA, 'contract_hash', contract_sha256=CONTRACT_SHA)
    contract = json.loads(raw)
    pre_freeze = json.loads(PRE_FREEZE.read_text())
    need(all(sha(ROOT / name) == digest for name, digest in pre_freeze['files'].items())
         and pre_freeze['contract_sha256'] == CONTRACT_SHA and pre_freeze['stage'] == 'pre_comparison',
         'pre_comparison_package_unchanged', files=sorted(pre_freeze['files']))
    pre = json.loads(PRE_RESULTS.read_text())
    params = contract['parameters']
    tau = F(params['tau'])
    s = F(params['s'])
    target = F(contract['preregistration']['target']['value'])
    need(target == F(params['absolute_target']) == F(1, 10 ** 6) and tau == F(1, 10 ** 8) and s == 1
         and F(params['control_tau']) == -tau, 'frozen_design_read_from_contract',
         tau=q(tau), s=q(s), target=q(target))

    # ---------------- pre-registration mirror discrepancy
    controls = list(contract['controls'])
    mirror = list(contract['preregistration']['controls_required']['ids'])
    missing = [c for c in controls if c not in mirror]
    extra = [c for c in mirror if c not in controls]
    need(len(controls) == 24 and len(mirror) == 23 and missing == ['c1_window_preview_only'] and extra == []
         and [c for c in controls if c in mirror] == mirror and controls.index('c1_window_preview_only') == 23
         and 'c1_window_preview_only' in contract['new_control_semantics']
         and any('C^1 window is registered as a preview-only control' in r for r in contract['required']),
         'preregistration_mirror_discrepancy_located', controls=24, mirrored_ids=23, missing_from_mirror=missing,
         position_in_controls=24, defined_in=['required item 10', 'new_control_semantics.c1_window_preview_only'])

    # ---------------- both producers' outputs
    fr = json.loads((FWD / 'output/results.json').read_text())
    rr = json.loads((REV / 'output/results.json').read_text())
    fch = {c['id']: c for c in fr['checks']}
    rch = {c['id']: c for c in rr['checks']}
    need(len(fr['checks']) == 50 and len(rr['checks']) == 50 and len(fch) == 50 and len(rch) == 50
         and all(c['passed'] is True for c in fr['checks'] + rr['checks']), 'both_producers_50_checks_all_passed')
    f_mut = {c: len(fch[c]['rejected_mutations']) for c in controls if c in fch and fch[c].get('rejected_mutations')}
    r_mut = {c: len(rch[c]['rejected_mutations']) for c in controls
             if c in rch and rch[c].get('kind') == 'damaging_mutation_control' and rch[c].get('rejected_mutations')}
    need(len(f_mut) == 24 and len(r_mut) == 24 and sum(f_mut.values()) == 68 and sum(r_mut.values()) == 80,
         'all_24_controls_are_damaging_mutations_in_both', forward_mutations=sum(f_mut.values()),
         reverse_mutations=sum(r_mut.values()))
    need(sorted(fch['c1_window_preview_only']['rejected_mutations'])
         == ['calculator_C1_certificate', 'calculator_poisson_certificate', 'kernel_switch_to_C1']
         and sorted(rch['c1_window_preview_only']['rejected_mutations'])
         == ['c1_residue_modulus', 'calculator_c1_certificate', 'kernel_switch_after_D_known']
         and sorted(fr['contract_controls_covered']) == sorted(controls),
         'missing_mirror_id_executed_by_both_anyway', forward=sorted(fch['c1_window_preview_only']['rejected_mutations']),
         reverse=sorted(rch['c1_window_preview_only']['rejected_mutations']))
    fsrc, rsrc = (FWD / 'check.py').read_text(), (REV / 'check.py').read_text()
    need("V['controls'] = list(c['controls'])" in fsrc and "for cid in V['controls']" in fsrc
         and "'controls_required'" not in fsrc
         and "for cid in contract['controls'] if cid not in ids" in rsrc
         and "set(prereg) <= set(ids)" in rsrc,
         'both_checkers_iterate_the_24_id_controls_list',
         forward='iterates contract controls; never reads controls_required',
         reverse='iterates contract controls; requires controls_required.ids to be a subset of controls')

    # ---------------- contract binding in the checkers (target, reference, D)
    need("(BASE / 'inputs' / CONTRACT_REL).read_bytes()" in fsrc and 'CONTRACT_SHA256 = ' + repr(CONTRACT_SHA) in fsrc
         and "V['target'] = rat(p['absolute_target'])" in fsrc and "pre['target']" in fsrc
         and "p['state_bound']" in fsrc and "Haar product reference C_0" in fsrc
         and "(INPUTS / CONTRACT_REL).read_bytes()" in rsrc and 'CONTRACT_SHA256 = ' + repr(CONTRACT_SHA) in rsrc
         and "TARGET = parse_q(contract_json['preregistration']['target']['value'])" in rsrc
         and "D = contract_state_bound(params['state_bound'])" in rsrc and "Haar product reference C_0" in rsrc,
         'checkers_read_target_reference_D_from_hash_checked_snapshot',
         forward_reference='parsed from the contract model string and cross-checked with preregistration.observable',
         reverse_reference='calculator constants 3 and 1/4 validated against the contract model string')
    lit_target = re.compile(r"['\"]1/1000000['\"]|Q\(1, *10 \*\* 6\)|F\(1, *10 \*\* 6\)")
    d_num = '585079838465912592144137406066050'
    rcalc_src = (REV / 'calculator.py').read_text()
    need(not lit_target.search(fsrc) and not lit_target.search(rsrc) and d_num not in fsrc and d_num not in rsrc
         and d_num in rcalc_src and d_num not in (FWD / 'calculator.py').read_text(),
         'no_target_or_D_literal_in_either_checker',
         note='the reverse calculator carries the gate-bound D at the cap only as an equality cross-check of its formula')

    # ---------------- D, k and the skeptic's own enclosures
    J = 28 * tau
    t1 = F(49, 144) * tau
    T = t1 / (1 - 352 * J)
    eps = 2 * T + T * T
    D = 2 * eps * (1 + eps) / (1 + eps * eps)
    gate = json.loads(GATE.read_text())
    gd = re.search(r'D_ii=(\d+)/(\d+) \(certified by both inequalities\) as the admitted state bound for AV2', gate['decision'])
    cd = re.match(r'D = (\d+)/(\d+) \(forward AV1 tier ii', params['state_bound'])
    need(gd is not None and cd is not None and D == F(int(gd.group(1)), int(gd.group(2))) == F(int(cd.group(1)), int(cd.group(2)))
         and F(fr['headline']['D']) == D and F(rr['state_bound']['D']) == D
         and F(fr['certificate_plus']['state_bound_D']) == D, 'D_equals_av1_formula_gate_contract_and_both_producers',
         D=q(D), preview=preview(D))
    k = F(49, 4) * tau
    need(F(rr['duhamel_slope']['k']) == k == F(fr['certificate_plus']['duhamel_slope_k']), 'duhamel_slope_both', k=q(k))
    PI_LO, PI_HI = pi_bracket()
    e3 = exp_neg(3 * s)
    ref_lo, ref_hi = e3[0] / 4, e3[1] / 4
    A = 2 * (D + D * D)
    E_lo, E_hi = A + 49 * tau * s / PI_HI, A + 49 * tau * s / PI_LO
    need(E_hi - E_lo < F(1, 10 ** 70) and E_hi <= target, 'analytic_radius_enclosed_skeptic',
         E_lower=q(E_lo), E_upper=q(E_hi), preview=preview(E_hi))

    # ---------------- datum
    df, dr = F(fr['certificate_plus']['certified_datum']), F(rr['certificate']['+']['datum'])
    m = df * 4 * G40
    need(df == dr == F(DATUM_TASK) and m.denominator == 1
         and F(m.numerator - 1, G40) < e3[0] and e3[1] < F(m.numerator + 1, G40)
         and max(abs(df - ref_lo), abs(df - ref_hi)) <= F(1, 4 * G40),
         'datum_identical_and_rederived', datum=q(df), datum_numerator_over_4e40=str(m.numerator),
         distance_to_free_value_at_most=preview(max(abs(df - ref_lo), abs(df - ref_hi)), 4),
         statement='d=m/(4*10^40), m=round(e^{-3}*10^40); the directed e^{-3} bracket is [(m-1),(m+1)]/10^40 in both producers')
    free_f = (F(fr['certificate_plus']['free_C_interval']['lower']), F(fr['certificate_plus']['free_C_interval']['upper']))
    rfree = rch['arithmetic_enclosure_e_minus_3']['calculator_enclosure']
    free_r = (F(rfree['lower']), F(rfree['upper']))
    need(free_f == free_r == (F(m.numerator - 1, 4 * G40), F(m.numerator + 1, 4 * G40))
         and free_f[0] <= ref_lo and ref_hi <= free_f[1], 'free_brackets_identical_and_contain_skeptic_enclosure')

    # ---------------- radius: itemized costs, validity and tightness in each producer
    cf = {n: F(v) for n, v in fr['certificate_plus']['costs'].items()}
    cr = {n: F(v) for n, v in rr['certificate']['+']['costs'].items()}
    radius_f = F(fr['certificate_plus']['certified_absolute_error'])
    radius_r = F(rr['certificate']['+']['radius'])
    arith = F(1, 4 * G40)
    for tag, c, r in (('forward', cf, radius_f), ('reverse', cr, radius_r)):
        need(sorted(c) == ['arithmetic', 'kernel_dynamics', 'mean_square', 'state'] and c['state'] == 2 * D
             and c['mean_square'] == 2 * D * D and c['arithmetic'] == arith and r == sum(c.values(), F(0))
             and c['kernel_dynamics'] >= 49 * tau * s / PI_LO and c['kernel_dynamics'] - 49 * tau * s / PI_HI <= F(1, G40),
             'itemized_costs_exact_and_directed_' + tag, state=q(c['state']), mean_square=q(c['mean_square']),
             kernel_dynamics=q(c['kernel_dynamics']), arithmetic=q(c['arithmetic']))
        need(r >= E_hi + max(abs(df - ref_lo), abs(df - ref_hi)) and r - E_lo <= F(1, G40) and r <= target
             and target / r > F(54586, 10000), 'radius_valid_and_not_inflated_' + tag,
             radius=q(r), overshoot_over_exact_E_at_most=preview(r - E_lo, 4), margin=preview(target / r, 6))
    pi_f = (F(fr['pi_interval']['lower']), F(fr['pi_interval']['upper']))
    pi_r_floor = fl(PI_LO, G40)
    need(fl(PI_HI, G40) == pi_r_floor and pi_f[0] <= PI_LO and PI_HI <= pi_f[1]
         and cf['kernel_dynamics'] == 49 * tau * s / pi_f[0]
         and cr['kernel_dynamics'] == ce(49 * tau * s / pi_r_floor, G40),
         'kernel_term_rounding_choices_identified', forward_pi_lower=q(pi_f[0]), reverse_pi_lower=q(pi_r_floor),
         forward='49|tau|/pi_lo exactly, pi_lo from Machin with each arctan rounded to 10^-40 before scaling (pi-pi_lo<2e-39)',
         reverse='49|tau|/floor_{10^-40}(pi) rounded up to the 10^-40 grid')
    diff = radius_r - radius_f
    need(0 < diff < F(1, G40) and preview(radius_f) == preview(radius_r) == RADIUS_PREVIEW_TASK
         and F(fr['certificate_minus_replay']['certified_absolute_error']) == radius_f
         and F(fr['certificate_minus_replay']['certified_datum']) == df
         and F(rr['certificate']['-']['radius']) == radius_r and F(rr['certificate']['-']['datum']) == dr,
         'cross_producer_radius_agreement_and_mirrored_replays', radius_reverse_minus_forward=q(diff),
         difference_preview=preview(diff, 4), both_previews=RADIUS_PREVIEW_TASK,
         note='identical datum; radii differ only by the pi rounding choice; -tau is a replay of the same |tau| formula')
    r_pre = F(pre['radius']['radius_exact'])
    need(abs(radius_f - r_pre) < F(1, G40) and abs(radius_r - r_pre) < F(1, G40) and r_pre <= radius_f,
         'agreement_with_pre_comparison_radius', pre_radius_preview=preview(r_pre),
         forward_minus_pre=preview(radius_f - r_pre, 4), reverse_minus_pre=preview(radius_r - r_pre, 4))
    R40 = ce(max(radius_f, radius_r), G40)
    need(R40 >= radius_r >= radius_f and R40 - radius_f < F(2, G40) and R40 <= target,
         'common_outward_radius_at_1e-40', R40=q(R40), preview=preview(R40, 12))
    for tag, iv, d, r in (('forward', fr['certificate_plus']['actual_C_interval'], df, radius_f),
                          ('reverse', rr['certificate']['+']['interval'], dr, radius_r)):
        lo, hi = F(iv['lower']), F(iv['upper'])
        need(lo == d - r and hi == d + r and lo <= ref_lo and ref_hi <= hi, 'interval_exact_and_free_value_inside_' + tag,
             lower_preview=preview(lo, 16), upper_preview=preview(hi, 16))
    need(fr['sub_labels'] == ['reference_unresolved'] and rr['sub_label'] == 'reference_unresolved'
         and fr['resolved_interaction_shift'] is False and rr['resolved_interaction_shift'] is False,
         'reference_unresolved_both')

    # ---------------- sign-blind scaling (tau_scaling_exponent) with the skeptic's pi
    tau100 = tau / 100
    J2 = 28 * tau100
    T2 = F(49, 144) * tau100 / (1 - 352 * J2)
    e2 = 2 * T2 + T2 * T2
    D2 = 2 * e2 * (1 + e2) / (1 + e2 * e2)
    E2_lo, E2_hi = 2 * (D2 + D2 * D2) + 49 * tau100 / PI_HI, 2 * (D2 + D2 * D2) + 49 * tau100 / PI_LO
    ratio = (E_lo / E2_hi, E_hi / E2_lo)
    s3lo, s3hi = sqrt_bracket(F(49, 3) * tau)
    s4lo, s4hi = sqrt_bracket(F(49, 3) * tau100)
    Ds_lo, Ds_hi, Ds2_lo, Ds2_hi = 2 * s3lo, 2 * s3hi, 2 * s4lo, 2 * s4hi
    sq_ratio_hi = (2 * (Ds_hi + Ds_hi ** 2) + 49 * tau / PI_LO) / (2 * (Ds2_lo + Ds2_lo ** 2) + 49 * tau100 / PI_HI)
    need(F(99) <= ratio[0] and ratio[1] <= F(101) and sq_ratio_hi < F(11), 'tau_scaling_linear_window_radius',
         ratio=[preview(ratio[0], 8), preview(ratio[1], 8)], sqrt_D_ratio_upper=preview(sq_ratio_hi, 6))

    # ---------------- crossover
    s_lo, s_hi = PI_LO * (target - A) / (49 * tau), PI_HI * (target - A) / (49 * tau)
    fx = (F(fr['crossover']['s_star_lower']), F(fr['crossover']['s_star_upper']))
    rx = tuple(F(v) for v in rr['crossover']['s_star_bracket'])
    px = (F(pre['crossover']['s_star_lower']), F(pre['crossover']['s_star_upper']))
    need(fx[0] <= s_lo and s_hi <= fx[1] and rx[0] <= s_lo and s_hi <= rx[1] and px[0] <= s_lo and s_hi <= px[1]
         and F(61, 10) < s_lo and s_hi < F(63, 10) and fx[1] - fx[0] < F(1, 10 ** 11) and rx[1] - rx[0] <= F(1, 10 ** 9)
         and fr['crossover']['grid_claim'] is False and fr['grid_claim'] is False and rr['grid_claim'] is False
         and contract['preregistration']['nodes']['s_values'] == ['1'],
         'crossover_enclosures_contain_skeptic_s_star', s_star=[preview(s_lo, 13), preview(s_hi, 13)],
         forward=[preview(fx[0], 13), preview(fx[1], 13)], reverse=[q(rx[0]), q(rx[1])],
         scope='crossover of the analytic formula only; s=1 is the only certified node; no grid or [0,128] claim')

    # ---------------- retained Poisson failures
    L4 = F(10) ** 4
    Da_lo, Da_hi = 2 * s3lo, 2 * s3hi
    lg4 = log_bracket(1 + L4 * L4)
    at4_lo = Da_lo + Da_lo ** 2 + k * lg4[0] / PI_HI + (F(1, 2) + Da_lo / 2) * 2 / (PI_HI * L4)
    at4_hi = Da_hi + Da_hi ** 2 + k * lg4[1] / PI_LO + (F(1, 2) + Da_hi / 2) * 2 / (PI_LO * L4)
    at4_text = re.search(r'Their sum is `mathcal E\^\+≈(0\.\d+)`', AT4_REPORT.read_text(encoding='utf-8'))
    fat4 = fr['retained_failures']['at4_poisson_L10000']
    rat4 = F(rr['retained_failures']['at4_poisson_L1e4_radius'])
    need(at4_text is not None and abs(at4_hi - F(at4_text.group(1))) < F(1, 10 ** 17)
         and F(fat4['radius_lower']) <= at4_lo and at4_hi <= F(fat4['radius_upper']) and at4_hi <= rat4
         and at4_lo > target and fat4['target_met'] is False, 'retained_at4_poisson_L1e4_both',
         skeptic=[preview(at4_lo, 16), preview(at4_hi, 16)], at4_report=at4_text.group(1))
    lk = log_bracket(1 / (2 * k))
    floor_formula_lo = 2 * k * (1 + lk[0]) / PI_HI
    floor_formula_hi = 2 * k * (1 + lk[1]) / PI_LO

    def F_hi(L):
        return k * log_bracket(1 + F(L) ** 2)[1] / PI_LO + 1 / (PI_LO * F(L))

    def F_lo(L):
        return k * log_bracket(1 + F(L) ** 2)[0] / PI_HI + 1 / (PI_HI * F(L))
    ff = fr['retained_failures']['poisson_floor_D_to_0']
    rf_ = rch['retained_poisson_floor_optimized']
    need(F(ff['floor_lower']) <= floor_formula_lo and F(rf_['floor_lower']) <= floor_formula_lo
         and F(ff['floor_upper']) >= F_hi(4081633) and F(rf_['floor_upper']) >= F_hi(4081632)
         and floor_formula_lo > target and F(rf_['floor_lower']) > target and F(ff['floor_lower']) > target
         and F_lo(4081633) - floor_formula_hi < F(1, 10 ** 18)
         and floor_formula_lo + D + D * D > target and F(pre['poisson_retained']['optimized_floor_D0']['lower']) <= floor_formula_lo,
         'retained_poisson_floor_all_L_both',
         statement='for every L>0: (k/pi)log(1+L^2)+1/(pi L) >= (2k/pi)(1+log(1/(2k))) (log(1+L^2)>=2log L, minimized at L=1/(2k))',
         skeptic_floor=[preview(floor_formula_lo, 13), preview(F_hi(4081633), 13)],
         forward=[preview(F(ff['floor_lower']), 13), preview(F(ff['floor_upper']), 13)],
         reverse=[preview(F(rf_['floor_lower']), 13), preview(F(rf_['floor_upper']), 13)],
         with_admitted_D_lower=preview(floor_formula_lo + D + D * D, 8))
    l10 = log_bracket(F(10))
    need(2 * l10[0] / PI_HI > 4 / PI_LO and 2 * 682190 * l10[0] / PI_HI > 10 ** 6 and 2 * 682188 * l10[1] / PI_LO < 10 ** 6,
         'poisson_first_moment_divergence', statement='(1/pi)log(1+L^2)>=(2/pi)log L: already above 4/pi at L=10; above 10^6 at L=10^682190',
         window_M1='4s/pi finite')
    gi = re.search(r'D_i=(\d+)/(\d+) \(~2\.3680e-5; exact, forward\)', gate['accepted'])
    if gi is None:
        raise ReviewFailure('gate tier (i) value not found')
    D_i = F(int(gi.group(1)), int(gi.group(2)))
    Ei_lo = 2 * (D_i + D_i * D_i) + 49 * tau / PI_HI
    fwd_i = F(fr['retained_failures']['window_with_tier_i']['radius_lower'])
    need(fwd_i <= Ei_lo and fwd_i == 2 * D_i + 49 * tau / pi_f[1] and Ei_lo > target
         and rch['tier_i_preview_retained_limited']['radius_preview'] == '4.751779428e-5' and preview(Ei_lo, 10) == '4.751779428e-5',
         'tier_i_window_retained_limited_both', exact_tier_i_radius_preview=preview(Ei_lo, 10),
         forward_note='the forward exports the lower value 2D_i+49|tau|/pi_hi (omits 2D_i^2); labelled; both exceed 10^-6')

    # ---------------- C^1 preview (labelled preview only)
    c1_lo = F(4) * (D + D * D) / PI_HI + 49 * tau / PI_HI
    c1_hi = F(4) * (D + D * D) / PI_LO + 49 * tau / PI_LO
    fc1, rc1 = fr['c1_window_preview'], rr['c1_window_preview']
    need(fc1['preview_only'] is True and fc1['used_for_certificate'] is False and rc1['certified'] is False
         and rc1['label'] == 'preview_only_not_a_certificate'
         and c1_hi <= F(fc1['preview_radius_upper']) <= c1_hi + F(1, 10 ** 38)
         and c1_hi <= F(rc1['radius_preview_upper']) <= c1_hi + F(1, 10 ** 38)
         and c1_hi < E_lo and fc1['negative_atom_multiplier_at_minus_one'] == '3'
         and fc1['sign_mutation_multiplier_at_minus_three'] == '7' and fc1['M2'] == 'infinite' and rc1['M2'] == 'infinity',
         'c1_preview_values_and_labels_both', c1_radius=preview(c1_hi, 10), c2_radius=preview(E_hi, 10),
         note='the C^1 preview radius is smaller than the frozen C^2 radius, so rejecting a post-hoc kernel switch is not vacuous')

    # ---------------- residues by Leibniz (fourth route) and the reverse's exported polynomial
    expect = {1: [1], 2: [1, -2], 3: [1, -2, 2]}
    leib = {}
    for sv in (F(1, 3), F(1), F(2), F(7)):
        for n in (1, 2, 3):
            poly, _ = lower_pole_polynomial(n, sv)
            if any(c[1] != 0 for c in poly) or [c[0] for c in poly] != [F(e) * sv ** j for j, e in enumerate(expect[n])]:
                raise ReviewFailure('Leibniz lower-pole polynomial n=%d s=%s' % (n, sv))
            leib.setdefault(q(sv), {})[str(n)] = [q(c[0]) for c in poly]
    _, res3 = lower_pole_polynomial(3, F(1))
    rev_upper = rch['residue_kernel_family_reconstructed']['family']['3']['residues'][0]['residue_without_coef_over_pi']
    rev_res = rch['residue_kernel_family_reconstructed']['family']['3']['residues'][1]['residue_without_coef_over_pi']
    parsed = [F(v) for v in re.findall(r'\(\(([-0-9/]+)\)\*i\)', rev_res)]
    need(all(c[0] == 0 for c in res3) and [c[1] for c in res3] == parsed == [F(1, 8), F(-1, 4), F(1, 4)]
         and rch['window_regularity_C2_and_L1']['derivatives_at_0_minus'] == ['1', '-1', '1', '7']
         and rch['window_regularity_C2_and_L1']['third_derivative_jump'] == '-8'
         and [F(v) for v in re.findall(r'\(\(([-0-9/]+)\)\*i\)', rev_upper)] == [cinv((F(0), F(8)))[1]],
         'lower_pole_residues_leibniz_route', polynomials=leib, reverse_triple_pole_residue_s1=rev_res,
         reverse_upper_pole_residue_s1=rev_upper,
         upper_pole='Res_{theta=is}=e^{-sx}/(i(2s)^n), so 2 pi i N_n Res=e^{-sx} with 2 pi N_n=(2s)^n; at s=1, n=3: 1/(8i)=-i/8')
    need(fr['window']['M0'] == rr['constants']['M0'] == '2' and fr['window']['M1'] == rr['constants']['M1'] == '4s/pi'
         and fr['window']['M2'] == rr['constants']['M2'] == '2s^2'
         and fr['window']['transform'] == rr['window']['ghat'] == 'ghat(theta)=4s^3/(pi(s-i theta)^3(s+i theta))'
         and pre['kernel']['C2']['moments'] == {'0': '2', '1': '4s/pi', '2': '2s^2'}
         and 'ghat(theta)=' + pre['kernel']['C2']['transform'] == fr['window']['transform']
         and pre['kernel']['C1']['M2'] == 'infinity' and pre['kernel']['poisson']['moments']['1'] == 'infinity',
         'constants_identical_across_three_routes', routes=['forward half-line transforms', 'reverse residues',
                                                             'skeptic annihilator-jump plus Wallis (pre-comparison)'])

    # ---------------- claim flags
    for tag, res in (('forward', fr), ('reverse', rr)):
        need(res['continuum_claim'] is False and res['uniform_wilson_claim'] is False and res['resolved_interaction_shift'] is False
             and res['scientific_priority_verified'] is False and res['grid_claim'] is False
             and res['euclidean_node_certified'] is True, 'claim_flags_' + tag)

    # ---------------- calculators on temporary copies
    probes = {}
    with tempfile.TemporaryDirectory(prefix='hnm-r32-av2-skeptic-calc-') as tmp:
        fc = load_calculator(FWD, 'fwd_calculator_av2', tmp)
        rc = load_calculator(REV, 'rev_calculator_av2', tmp)
        bad_f = [dict(tau=1e-8), dict(s=True), dict(tau='NaN'), dict(tau='Infinity'), dict(tau='1/0'), dict(tau=''),
                 dict(selected=('0', '1/100', '0')), dict(tau='1/10000000'), dict(tau='-1/10000000'), dict(s='0'),
                 dict(s='-1'), dict(alpha='0'), dict(hbar='-1'), dict(target='0'), dict(state_tier='av1_tier_i'),
                 dict(state_tier='at4_sqrt'), dict(window='C1'), dict(window='poisson'),
                 dict(fixed_design=True, s='2'), dict(D='1/100000000')]
        bad_r = [dict(tau=1e-8), dict(s=True), dict(tau='NaN'), dict(tau='Infinity'), dict(tau='1/0'), dict(tau=''),
                 dict(selected=('0', '1/100', '0')), dict(tau='1/10000000'), dict(tau='-1/10000000'), dict(s='0'),
                 dict(s='-1'), dict(alpha='0'), dict(hbar='-1'), dict(target='0'), dict(state_tier='i'),
                 dict(state_tier='ii_reverse'), dict(kernel='C1_window'), dict(kernel='poisson'),
                 dict(fixed_design=True, s='2'), dict(D='1/100000000')]
        probes['forward_rejections'] = [raises(lambda kw=kw: fc.certify(**kw), (ValueError, TypeError)) for kw in bad_f]
        probes['reverse_rejections'] = [raises(lambda kw=kw: rc.certify(**kw), (ValueError, TypeError)) for kw in bad_r]
        f_fix, r_fix = fc.certify(fixed_design=True), rc.certify(fixed_design=True)
        f_forms = {fc.certify(tau=v)['certified_absolute_error'] for v in (F(1, 10 ** 8), '1/100000000', '0.00000001')}
        r_forms = {rc.certify(tau=v)['certified_radius'] for v in (F(1, 10 ** 8), '1/100000000', '0.00000001')}
        f0, r0 = fc.certify(tau='0'), rc.certify(tau='0')
        t9 = F(1, 10 ** 9)
        J9 = 28 * t9
        T9 = F(49, 144) * t9 / (1 - 352 * J9)
        e9 = 2 * T9 + T9 * T9
        D9 = 2 * e9 * (1 + e9) / (1 + e9 * e9)
        f9, r9 = fc.certify(tau='1/1000000000'), rc.certify(tau='-1/1000000000')
        c1f, c1r = fc.c1_window_preview(), rc.preview_c1_window()
        need(F(f_fix['certified_absolute_error']) == radius_f and F(r_fix['certified_radius']) == radius_r
             and F(f_fix['certified_datum']) == F(r_fix['certified_datum']) == df
             and f_forms == {f_fix['certified_absolute_error']} and r_forms == {r_fix['certified_radius']}
             and F(f0['certified_absolute_error']) == F(f0['costs']['arithmetic']) and F(f0['state_bound_D']) == 0
             and F(r0['certified_radius']) == F(r0['costs']['arithmetic']) and F(r0['state_bound_D']) == 0
             and F(f9['state_bound_D']) == F(r9['state_bound_D']) == D9 < D
             and c1f['used_for_certificate'] is False and c1r['certified'] is False
             and len(probes['forward_rejections']) == len(bad_f) and len(probes['reverse_rejections']) == len(bad_r),
             'calculators_domain_exact_inputs_and_fixed_design', forward_rejected=len(bad_f), reverse_rejected=len(bad_r),
             tau_zero_radius_equals_arithmetic=True, D_below_cap='AV1 tier-(ii) formula at |tau| (equal in both)',
             supplied_D_rejected=[probes['forward_rejections'][-1], probes['reverse_rejections'][-1]])
    if any(p.name == '__pycache__' for d in (FWD, REV) for p in d.rglob('*')):
        raise ReviewFailure('interpreter cache written into a producer closure')

    # ---------------- source-edit mutations on temporary copies
    base_f = mutated_run(FWD, 'forward')
    base_r = mutated_run(REV, 'reverse')
    need(base_f[0] == 0 and base_f[1] == (FWD / 'output/results.json').read_bytes()
         and base_r[0] == 0 and base_r[1] == (REV / 'output/results.json').read_bytes(),
         'mutation_harness_unmutated_copies_reproduce_frozen_results')
    mutations = [
        ('forward', 'calc_state_term_halved_D_over_2',
         {'calc_edits': [("    costs = {'state': M['M0'] * D,\n", "    costs = {'state': M['M0'] * D / 2,\n")]}),
        ('forward', 'calc_mean_square_dropped',
         {'calc_edits': [("             'mean_square': M['M0'] * D * D,\n", "             'mean_square': 0 * D,\n")]}),
        ('forward', 'calc_pi_direction_flipped',
         {'calc_edits': [("             'kernel_dynamics': k * M['M1_upper']}", "             'kernel_dynamics': k * M['M1_lower']}")]}),
        ('forward', 'calc_duhamel_factor_two_dropped',
         {'calc_edits': [("    k = Q(49, 4) * abs_tau\n    pi_lo, pi_hi = pi_interval()\n    M = window_constants(",
                          "    k = Q(49, 8) * abs_tau\n    pi_lo, pi_hi = pi_interval()\n    M = window_constants(")]}),
        ('forward', 'calc_c2_left_coefficient_changed',
         {'calc_edits': [("        return 1 + 2 * s * y + 2 * s * s * y * y\n", "        return 1 + 2 * s * y + s * s * y * y\n")]}),
        ('forward', 'calc_av1_coefficient_doubled',
         {'calc_edits': [("    t1 = Q(49, 144) * abs_tau\n", "    t1 = Q(49, 72) * abs_tau\n")]}),
        ('forward', 'sign_convention_flipped',
         {'edits': [("        return calc.window_multiplier(sign * V['free_energy'], s1)\n",
                     "        return calc.window_multiplier(-sign * V['free_energy'], s1)\n")]}),
        ('forward', 'grid_claim_true',
         {'edits': [("                   'scientific_priority_verified': False, 'grid_claim': False,\n",
                     "                   'scientific_priority_verified': False, 'grid_claim': True,\n")]}),
        ('forward', 'poisson_floor_halved',
         {'edits': [("    floor_lo = kk2 * s1_ * (1 + lgk_lo) / pi_hi\n", "    floor_lo = kk2 * s1_ * (1 + lgk_lo) / (2 * pi_hi)\n")]}),
        ('forward', 'c1_M0_in_radius',
         {'edits': [("    M0 = Q(2)\n    M1_up = 4 * s1 / pi_lo\n", "    M0 = 4 / pi_hi\n    M1_up = 4 * s1 / pi_lo\n")]}),
        ('forward', 'contract_target_relaxed',
         {'contract_replace': (b'"absolute_target": "1/1000000"', b'"absolute_target": "1/1000"')}),
        ('forward', 'undeclared_input_reverse_report', {'extra_input': 'research/round32/reverse/av2/report.md'}),
        ('reverse', 'calc_state_term_halved_D_over_2',
         {'calc_edits': [("        'state': WINDOW_M0 * D,\n", "        'state': WINDOW_M0 * D / 2,\n")]}),
        ('reverse', 'calc_mean_square_dropped',
         {'calc_edits': [("        'mean_square': WINDOW_M0 * D * D,\n", "        'mean_square': 0 * D,\n")]}),
        ('reverse', 'calc_M0_signed_integral_one',
         {'calc_edits': [("WINDOW_M0 = Q(2)                 # ||ghat||_1\n", "WINDOW_M0 = Q(1)                 # ||ghat||_1\n")]}),
        ('reverse', 'calc_duhamel_factor_two_dropped',
         {'calc_edits': [("    k = 2 * INCIDENT_STARS * STAR_NORM_PER_TAU * abs_tau\n    pi_lo, pi_hi = pi_interval()\n",
                          "    k = INCIDENT_STARS * STAR_NORM_PER_TAU * abs_tau\n    pi_lo, pi_hi = pi_interval()\n")]}),
        ('reverse', 'calc_av1_coefficient_doubled',
         {'calc_edits': [("    t1 = Q(49, 144) * abs_tau\n", "    t1 = Q(49, 72) * abs_tau\n")]}),
        ('reverse', 'calc_c1_kernel_admitted',
         {'calc_edits': [("CERTIFIED_KERNELS = ('C2_window',)\n", "CERTIFIED_KERNELS = ('C2_window', 'C1_window')\n")]}),
        ('reverse', 'free_atom_read_mirrored',
         {'edits': [("    free_value = readout(K3, Q(3), calc.FREE_VARIANCE)\n", "    free_value = readout(K3, Q(-3), calc.FREE_VARIANCE)\n")]}),
        ('reverse', 'residue_window_coefficient_edited',
         {'edits': [("        window_poly_int[p] = int(c / S0 ** p)\n",
                     "        window_poly_int[p] = int(c / S0 ** p) + (1 if p == 2 else 0)\n")]}),
        ('reverse', 'grid_claim_true',
         {'edits': [("    flags = {name: False for name in UNIVERSAL_FLAGS}\n",
                     "    flags = {name: name == 'grid_claim' for name in UNIVERSAL_FLAGS}\n")]}),
        ('reverse', 'poisson_floor_halved',
         {'edits': [("    lower = floor_to(k * log_lo_a / pi_hi + Q(1) / (pi_hi * hi))\n",
                     "    lower = floor_to((k * log_lo_a / pi_hi + Q(1) / (pi_hi * hi)) / 2)\n")]}),
        ('reverse', 'contract_target_relaxed',
         {'contract_replace': (b'"value": "1/1000000"', b'"value": "1/1000"')}),
        ('reverse', 'skeptic_triage_added_to_inputs', {'extra_input': 'research/round32/skeptic/triage.md'}),
    ]
    receipts = []
    for direction, label, spec in mutations:
        code, results, last = mutated_run(FWD if direction == 'forward' else REV, direction, **spec)
        need(code != 0 and results is None, 'mutation_rejected_%s_%s' % (direction, label), last_error_line=last)
        receipts.append({'direction': direction, 'mutation': label, 'rejected': True, 'last_error_line': last})

    exact = {
        'D': q(D), 'k': q(k), 'datum': q(df),
        'radius_forward': q(radius_f), 'radius_reverse': q(radius_r), 'radius_reverse_minus_forward': q(diff),
        'radius_common_outward_1e-40': q(R40),
        'interval_common_outward': [q(df - R40), q(df + R40)],
        'E_analytic_skeptic': [q(E_lo), q(E_hi)],
        'free_value_skeptic': [q(ref_lo), q(ref_hi)],
        'pi_skeptic': [q(PI_LO), q(PI_HI)],
        's_star_skeptic': [q(s_lo), q(s_hi)],
        'poisson_floor_all_L_lower_skeptic': q(floor_formula_lo),
        'at4_L1e4_radius_skeptic': [q(at4_lo), q(at4_hi)],
        'tier_i_window_radius_lower_skeptic': q(Ei_lo),
        'c1_preview_radius_upper_skeptic': q(c1_hi),
    }
    previews = {
        'radius_forward': preview(radius_f, 12), 'radius_reverse': preview(radius_r, 12),
        'radius_common_outward': preview(R40, 12), 'difference': preview(diff, 4),
        'datum': preview(df, 16), 'interval': [preview(df - R40, 16), preview(df + R40, 16)],
        'margin_target_over_radius': preview(target / R40, 6), 's_star': preview(s_lo, 12),
        'poisson_floor': preview(floor_formula_lo, 12), 'at4_radius': preview(at4_hi, 12),
        'tier_i_window_radius': preview(Ei_lo, 10), 'c1_preview_radius': preview(c1_hi, 10),
        'note': 'decimal previews only; every Boolean above was decided on exact rationals',
    }
    return {
        'schema': 'hnm-r32-skeptic-postcomparison-v1', 'loop': 'AV2', 'stage': 'post_comparison',
        'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'model-agent skeptic with correlated ancestry; not human peer review or formal verification',
        'contract_sha256': CONTRACT_SHA, 'exact': exact, 'previews': previews,
        'mirror_discrepancy': {'controls': 24, 'preregistration_controls_required_ids': 23,
                               'missing_from_mirror': 'c1_window_preview_only',
                               'forward_executed': sorted(fch['c1_window_preview_only']['rejected_mutations']),
                               'reverse_executed': sorted(rch['c1_window_preview_only']['rejected_mutations'])},
        'calculator_probes': probes, 'mutation_receipts': receipts,
        'passed': True, 'checks': CHECKS, 'checks_count': len(CHECKS),
    }


def main():
    ap = argparse.ArgumentParser(description='AV2 post-comparison skeptic checks')
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
    print(json.dumps({'loop': 'AV2', 'stage': 'post_comparison', 'checks': result['checks_count'],
                      'radius_forward': result['previews']['radius_forward'],
                      'radius_reverse': result['previews']['radius_reverse'],
                      'mutations_rejected': len(result['mutation_receipts'])}, sort_keys=True))


if __name__ == '__main__':
    main()
