#!/usr/bin/env python3
"""AY1 post-comparison skeptic checks, written after both producer freezes.

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated
ancestry (same model family as the advisor, the lenses and both producers; the
2D observation and the goal-4 controls came from the skeptic's own triage); not
human peer review or formal verification.

What this adds to the frozen pre-comparison package (ay1_check.py, 96 checks,
committed at 55be992 before either producer):
  * integrity: contract hash; the unchanged pre-comparison package; both freeze
    closures file by file; both premise inventories on the real snapshots
    (reverse = AGENTS.md + contract + 28 shared premises, 30 files; forward =
    those plus triage.md and the Jung loop-2 response, 32 files); snapshots equal
    to their repository sources; each check.py sha256 recorded before evaluation;
  * every producer headline compared with the skeptic's independent values
    (imported from the frozen ay1_check.py, never from a producer): D, 2D, 2D_i,
    the face counts 49/82/10/72/66/33/16/6/27, the two families on N=2,3, the
    per-site sum 28|tau|=J_0, the reset 98|tau|, rho^(1)_R (10 faces, trace norm
    sqrt(10)|tau|/72, Tr(rho^(1)W)=+tau/144), K_2' and all five items, K_2^+,
    the labelled variants, 2K_2'tau^2, the reverse Bures and fidelity constants,
    and the supplementary two-sided observation on ||rho_R-P_R||_1;
  * gate fields, claim flags, sentence templates and a forbidden-phrase scan of
    both reports;
  * source-edit mutations on temporary copies outside the checkout: every
    must-abort edit has to abort, unmutated copies have to reproduce the frozen
    results.json byte for byte, and silent edits that a producer checker does
    not pin have to be caught by this review's value validator.

Standard library only; exact Fractions decide every Boolean; failures are explicit
exceptions (never assert), so the output bytes match under python -O.

Usage: python3 -B research/round32/skeptic/ay1_postreview_check.py --output /abs/fresh/dir
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
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import ay1_check as pre  # noqa: E402  (the skeptic's own frozen pre-comparison module)

ROOT = HERE.parents[2]
R32 = ROOT / 'research/round32'
CONTRACT = R32 / 'contracts/ay1.json'
CONTRACT_SHA = 'be9b354420e66e7edba03d59b3d194b69f26782b44cfb63cb10e176bf4879ae0'
FWD = R32 / 'forward/ay1'
REV = R32 / 'reverse/ay1'
PRE_RESULTS = HERE / 'ay1-independent/results.json'
PRE_FREEZE = HERE / 'ay1-independent-freeze.json'
AV1_GATE = R32 / 'advisor/av1-gate.json'
AW1_GATE = R32 / 'advisor/aw1-gate.json'
FORBIDDEN_REVERSE = ('research/round32/skeptic/triage.md', 'research/round32/skeptic/loop2-response.md',
                     'research/round32/skeptic/ay1', 'research/round32/experts/', 'research/round32/advisor/deliberation-',
                     'research/round32/advisor/panel', 'research/round32/forward/ay1/')
TEMPLATE_CLAUSES = ('For every pair of subsequential limits of the named construction families F1',
                    'at the same coupling', 'on the fixed cover R and for the frozen observable class, the reduced densities satisfy '
                    "||rho_R - rho'_R||_1 <= 2D", 'and agree to first order in tau',
                    'this does not assert equality of the states, whole-sequence convergence, translation invariance, '
                    'boundary independence of the dynamics, or a rate in N.')


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


# ------------------------------------------------------------ skeptic reference values (own code)
def reference(cap):
    v = pre.tier_ii(cap)
    items, eps_r = pre.k2_prime_items(cap)
    k2p = pre.k2_prime(cap)
    rest = items['straddling'] + items['two_creation'] + items['density'] + items['normalization']
    t_i = 28 * cap * F(148, 7)
    return {'v': v, 'items': items, 'eps_R': eps_r, 'K2p': k2p, 'rest': rest,
            'D': pre.d_forward(v['eps_F']), 'D_i': pre.d_forward(2 * t_i + t_i * t_i),
            'K2plus': pre.k2_plus_skeptic(cap), 'K2W': pre.k2_w_rlocal(cap),
            'tn_sq': F(10, 5184) * cap * cap}


def directed_upper_sqrt_ok(value, target_sq):
    """value >= sqrt(target_sq), decided exactly."""
    return value >= 0 and value * value >= target_sq


def validate_producer_values(results, direction, cap):
    """Rejects a producer packet whose exported constants differ from the skeptic's independent
    values, or whose labelled directed bounds are not bounds (silent undercounts are caught here)."""
    ref = reference(cap)
    tau2 = cap * cap
    if direction == 'forward':
        h = results['headline']
        if F(h['D']) != ref['D'] or F(h['two_D']) != 2 * ref['D']:
            raise Rejected('forward D or 2D differs from the AV1 tier (ii) density form')
        if F(h['K2_prime']) != ref['K2p'] or F(h['two_K2_prime_tau2']) != 2 * ref['K2p'] * tau2:
            raise Rejected("forward K_2' differs from the skeptic's R-local trace-norm itemization")
        items = results['error_terms_itemized']['second_order_difference']['items']
        mine = {'am2_remainder': ref['items']['am2_remainder'], 'straddling': ref['items']['straddling'],
                'two_creation': ref['items']['two_creation'], 'density': ref['items']['density'],
                'normalization_third_order': ref['items']['normalization']}
        if {k: F(x) for k, x in items.items()} != mine:
            raise Rejected("forward K_2' items differ")
        orth = F(h['K2_prime_orthogonal_variant_upper']) * tau2
        x = (orth - ref['rest']) / (2 * ref['v']['rho'])
        if not (x > 0 and x * x >= 2):
            raise Rejected('forward orthogonal variant is not an upper bound (sqrt 2 rounded down)')
        tn_up = F(h['rho1_R_trace_norm_upper'])
        if not directed_upper_sqrt_ok(tn_up, ref['tn_sq']) or F(h['rho1_R_trace_norm_squared']) != ref['tn_sq']:
            raise Rejected('forward rho^(1) trace norm bracket invalid')
        sup = {c['id']: c for c in results['checks']}['second_order_difference_2K2prime']['supplementary_corollary']
        hi, lo = F(sup['bound']), F(sup['lower'])
        k2t = ref['K2p'] * tau2
        if not directed_upper_sqrt_ok(hi - k2t, ref['tn_sq']) or F(h['supplementary_single_limit_bound']) != hi:
            raise Rejected('forward supplementary upper end is not an upper bound')
        if not (lo > 0 and (lo + k2t) ** 2 <= ref['tn_sq']):
            raise Rejected('forward supplementary lower end is not a lower bound')
    else:
        h = results['headline']
        if F(h['D']['exact']) != ref['D'] or F(h['two_D']['exact']) != 2 * ref['D']:
            raise Rejected('reverse D or 2D differs from the AV1 tier (ii) density form')
        if F(h['K2_prime']['exact']) != ref['K2p'] or F(h['two_K2_prime_tau_squared_at_cap']['exact']) != 2 * ref['K2p'] * tau2:
            raise Rejected("reverse K_2' differs from the skeptic's R-local trace-norm itemization")
        ch = {c['id']: c for c in results['checks']}
        led = ch['item3_second_order_ledger_K2_prime']['ledger']
        mine = dict(ref['items'])
        if {k: F(x['exact']) for k, x in led['items'].items()} != mine or F(led['eps']['exact']) != ref['eps_R']:
            raise Rejected("reverse K_2' items or eps_R differ")
        eps = ref['v']['eps_F']
        cl = ch['item2_pairwise_closeness_2D']
        if F(cl['bures_pairwise']['exact']) != 4 * eps / (1 + eps * eps) or F(cl['fidelity_floor']['exact']) != 1 / (1 + eps * eps):
            raise Rejected('reverse Bures or fidelity constants differ')
        dfu = F(cl['D_fidelity_upper']['exact'])
        if not (dfu * dfu * (1 + eps * eps) >= 4 * eps * eps and dfu <= ref['D']):
            raise Rejected('reverse fidelity bound is not a directed upper bound below D')
        var = ch['item3_K2_prime_versus_K2_plus']['variants']
        orth = F(var['orthogonal_in_R_sectors_sqrt2']['K2_prime']['exact']) * tau2
        x = (orth - ref['rest']) / (2 * ref['v']['rho'])
        if not (x > 0 and x * x >= 2):
            raise Rejected('reverse orthogonal variant is not an upper bound')
        fo = ch['item3_first_order_density_explicit']
        lo_b, hi_b = (F(t) for t in fo['trace_norm_bracket'])
        if not (lo_b * lo_b <= F(10, 5184) <= hi_b * hi_b) or F(fo['trace_norm_squared']) != F(10, 5184):
            raise Rejected('reverse rho^(1) trace norm bracket invalid')
        low = F(ch['first_order_mean_charged']['proved_first_order_lower']['exact'])
        k2t = ref['K2p'] * tau2
        if not (low > 0 and (low + k2t) ** 2 <= ref['tn_sq']):
            raise Rejected('reverse first-order lower bound is not a lower bound')
        sep = F(ch['common_clock']['plus_minus_tau_first_order_separation_lower']['exact'])
        if sep != 2 * low:
            raise Rejected('reverse +-tau separation differs from twice the lower bound')
    return True


# ------------------------------------------------------------ phrasing and template
def strip_code(text):
    text = re.sub(r'```.*?```', ' ', text, flags=re.S)
    return re.sub(r'`[^`\n]*`', ' ', text)


def phrase_scan(text):
    """Code spans removed; per line: no 'the thermodynamic limit'; 'the AQ state' only inside the negated
    verbatim contract exclusion; every line with 'uniq' contains 'not'. Returns the offending lines."""
    bad = []
    for line in strip_code(text).splitlines():
        low = line.lower()
        if 'the thermodynamic limit' in low:
            bad.append(line)
        elif 'the aq state' in low and not ('uniqueness of the aq state' in low and re.search(r'\bnot\b', low)):
            bad.append(line)
        elif 'uniq' in low and re.search(r'\bnot\b', low) is None:
            bad.append(line)
    return bad


def template_in_order(text):
    pos = 0
    for clause in TEMPLATE_CLAUSES:
        i = text.find(clause, pos)
        if i < 0:
            return False
        pos = i + len(clause)
    return True


# ------------------------------------------------------------ source-mutation replays
def mutated_run(direction, edits=(), extra_input=None, contract_edit=None, rehash=False, report_append=None):
    src = FWD if direction == 'forward' else REV
    with tempfile.TemporaryDirectory(prefix='hnm-r32-ay1-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / 'research/round32' / direction / 'ay1'
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        code = (dst / 'check.py').read_text()
        for old, new in edits:
            if code.count(old) != 1:
                raise ReviewFailure('mutation anchor not unique in %s: %r' % (direction, old[:60]))
            code = code.replace(old, new)
        if contract_edit is not None:
            cpath = dst / 'inputs/research/round32/contracts/ay1.json'
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
        if report_append is not None:
            rp = dst / 'report.md'
            rp.write_text(rp.read_text() + report_append)
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


def verify_closure(src, contract):
    freeze = json.loads((src / 'freeze.json').read_text())
    prefix = src.relative_to(ROOT).as_posix() + '/'
    sources = freeze['sources']
    files = {p.relative_to(ROOT).as_posix() for p in src.rglob('*') if p.is_file() and p != src / 'freeze.json'}
    ok = (freeze['loop'] == 'AY1' and freeze['direction'] == src.parent.name and freeze['contract_sha256'] == CONTRACT_SHA
          and all(n.startswith(prefix) for n in sources) and set(sources) == files
          and all(sha(ROOT / n) == d for n, d in sources.items())
          and not any('__pycache__' in n or n.endswith('.pyc') for n in files))
    inputs = sorted(p.relative_to(src / 'inputs').as_posix() for p in (src / 'inputs').rglob('*') if p.is_file())
    snapshots_equal = all((src / 'inputs' / n).read_bytes() == (ROOT / n).read_bytes() for n in inputs)
    return ok, inputs, snapshots_equal, len(sources)


# ------------------------------------------------------------ main computation
def run():
    raw = CONTRACT.read_bytes()
    con = json.loads(raw)
    pr = con['preregistration']
    cap = F(con['parameters']['tau_cap'])
    target = F(pr['target']['value'])
    need(sha(CONTRACT) == CONTRACT_SHA and con['status'] == 'frozen_before_production' and cap == F(1, 10 ** 8)
         and target == F(1, 1250000), 'contract_sha256_and_target', contract_sha256=CONTRACT_SHA, target=q(target))

    # ================= pre-comparison package unchanged
    pf = json.loads(PRE_FREEZE.read_text())
    need(pf['contract_sha256'] == CONTRACT_SHA and pf['stage'] == 'pre_comparison'
         and all(sha(ROOT / p) == d for p, d in pf['files'].items()) and len(pf['files']) == 4,
         'pre_comparison_package_unchanged', files=sorted(pf['files']))
    prer = json.loads(PRE_RESULTS.read_text())

    # ================= closures and inventories
    shared = list(con['shared_premises'])
    fwd_only = list(con['forward_additional_premises'])
    declared_rev = sorted(['AGENTS.md', 'research/round32/contracts/ay1.json'] + shared)
    declared_fwd = sorted(declared_rev + fwd_only)
    okf, inv_f, snap_f, nf = verify_closure(FWD, con)
    okr, inv_r, snap_r, nr = verify_closure(REV, con)
    need(okf and okr and snap_f and snap_r, 'both_freeze_closures_verified', closure_files={'forward': nf, 'reverse': nr},
         snapshots_equal_repository_sources=True)
    skeptic_in_rev = sorted(n for n in inv_r if n.startswith('research/round32/skeptic/'))
    need(inv_r == declared_rev and len(inv_r) == 30 and not any(n.startswith(p) for n in inv_r for p in FORBIDDEN_REVERSE)
         and not (set(fwd_only) & set(inv_r)) and skeptic_in_rev == ['research/round32/skeptic/av1.md', 'research/round32/skeptic/aw1.md']
         and set(skeptic_in_rev) <= set(shared) and not any(n.startswith('research/round32/experts/') for n in inv_r),
         'reverse_premise_isolation_real_inventory', inputs=30, skeptic_files_are_declared_shared_premises=skeptic_in_rev,
         forbidden_prefixes_checked=list(FORBIDDEN_REVERSE))
    need(inv_f == declared_fwd and len(inv_f) == 32 and 'research/round32/skeptic/triage.md' in inv_f
         and 'research/round32/experts/jung/loop2-response.md' in inv_f and not any(n.startswith('research/round32/reverse/ay1/') for n in inv_f),
         'forward_inventory_declared', inputs=32, forward_additional=fwd_only)
    rf = json.loads((FWD / 'output/results.json').read_text())
    rr = json.loads((REV / 'output/results.json').read_text())
    need(rf['check_py_sha256_recorded_before_evaluation'] == sha(FWD / 'check.py')
         and rr['check_py_sha256_recorded_before_evaluation'] == sha(REV / 'check.py')
         and rf['contract_sha256'] == CONTRACT_SHA == rr['contract_sha256'], 'check_py_sha_recorded_and_contract_bound')
    cf = [c for c in rf['checks']]
    cr = [c for c in rr['checks']]
    ids = set(con['controls'])
    need(len(cf) == 42 and len(cr) == 41 and all(c['passed'] is True for c in cf + cr)
         and ids <= {c['id'] for c in cf} and ids <= {c['id'] for c in cr}
         and sorted(rf['contract_controls_covered']) == sorted(ids) and rf['controls_with_damaging_mutations'] == 21
         and rf['rejected_mutation_total'] == 97 and sorted(rr['controls_with_damaging_mutations']) == sorted(ids)
         and rr['controls_not_implementable_as_mutations'] == [], 'producer_checks_and_21_controls',
         forward_checks=42, reverse_checks=41, forward_rejected_mutations=97)

    # ================= constants compared with the skeptic's independent values
    ref = reference(cap)
    av1 = json.loads(AV1_GATE.read_text())
    d_gate = F(re.search(r'D_ii=(\d+/\d+)', av1['decision']).group(1))
    aw1 = json.loads(AW1_GATE.read_text())
    k2p_gate = F(re.search(r'K_2\^\+=(\d+/\d+)', aw1['accepted']).group(1))
    hf, hr = rf['headline'], rr['headline']
    need(ref['D'] == d_gate == F(hf['D']) == F(hr['D']['exact']) == F(prer['pair_constant']['D']),
         'D_equal_gate_forward_reverse_skeptic', D=q(d_gate))
    two_d = 2 * d_gate
    need(two_d == F(hf['two_D']) == F(hr['two_D']['exact']) == F(prer['pair_constant']['two_D']) and two_d <= target
         and hf['target_met'] is True and hr['two_D']['target_met'] is True, 'two_D_equal_and_meets_target',
         two_D=q(two_d), margin=preview(target / two_d, 8))
    need(2 * ref['D_i'] == F(rr['tier_i_retained']['two_D_i']['exact']) == F(prer['pair_constant']['two_D_i'])
         and 2 * ref['D_i'] > target and rr['tier_i_retained']['meets_target'] is False, 'tier_i_retained_both',
         two_D_i=q(2 * ref['D_i']))
    pins_f = {c['id']: c for c in cf}['face_enumeration_R_local']['pins']
    cnt_r = {c['id']: c for c in cr}['face_counts_R_local']['counts']
    need(pins_f == {'per_factor': 49, 'meet': 82, 'inside': 10, 'containing': 16, 'strictly_containing': 6, 'straddling': 72,
                    'one_site_straddling': 66, 'single': 33, 'owner_sets_meeting_R': 27}
         and cnt_r == {'containing_0_not_e_z': 33, 'containing_both_sites': 16, 'containing_e_z_not_0': 33, 'faces_meeting_R': 82,
                       'faces_per_factor': 49, 'owner_set_exactly_R': 10, 'owner_sets_meeting_R': 27, 'owner_sets_per_factor': 15,
                       'straddling': 72}
         and prer['counts']['faces_meeting_R'] == 82 and prer['counts']['inside_R'] == 10 and prer['counts']['straddling'] == 72
         and prer['counts']['single_contact_per_site'] == 33, 'face_counts_equal_82_10_72_33')
    # families on N=2,3 (own enumeration)
    fam = {}
    for n in (2, 3):
        ws, pd = pre.whole_star_groups(n), pre.padded_groups(n)
        cw, cp = pre.census(ws, n), pre.census(pd, n)
        partial = sum(1 for g in pd if 0 < len(g['faces']) < 21)
        bplus = len(set(pre.box(n)) | {pre.add(b, s) for b in pre.box(n) for s in pre.S_STAR})
        fam[n] = {'F1': len(cw['keys']), 'F2': len(cp['keys']), 'extra': len(cp['keys'] - cw['keys']), 'groups_F2': len(pd),
                  'partial_F2': partial, 'B_plus': bplus, 'J_max': max(v[0] for v in cp['per_site'].values()),
                  'faces_max': max(v[2] for v in cp['per_site'].values()), 'support_max': cp['max_support'],
                  'reset_R': 2 * sum(k for _, k in cp['groups_R']) * F(1, 3)}
    audit_f = {c['id']: c for c in cf}['family_F2_padded_interaction']['audit']
    boxes_r = {c['id']: c for c in cr}['item1_F2_padded_am2_contraction']['boxes']
    agree = True
    for n in (2, 3):
        a, b, m = audit_f[str(n)], boxes_r[str(n)], fam[n]
        agree = agree and (a['faces_F1'] == b['F1_faces'] == m['F1'] and a['faces_F2'] == b['F2_faces'] == m['F2']
                           and a['extra_F2_faces'] == b['F2_minus_F1'] == m['extra'] and a['groups_F2'] == m['groups_F2']
                           and b['F2_partial_groups'] == m['partial_F2'] and b['am2_volume_sites'] == m['B_plus']
                           and a['padding_sites_B_plus_minus_B'] == m['B_plus'] - (2 * n + 1) ** 3
                           and F(a['max_J_per_abs_tau_anchor_grouping']) == F(b['padded_J_per_tau']) == m['J_max'] == 28
                           and a['max_first_order_faces_per_site'] == b['max_faces_per_site_F2'] == m['faces_max'] == 49
                           and a['max_group_support'] == m['support_max'] == 4 and b['padded_termination'] == 8
                           and F(b['padded_reset_R_per_tau']) == m['reset_R'] == 98)
    need(agree and 28 * cap == F(7, 25000000), 'families_F1_F2_and_padded_constants_agree',
         skeptic={str(n): {k: q(v) if isinstance(v, F) else v for k, v in fam[n].items()} for n in (2, 3)})
    rs = {c['id']: c for c in cf}['reset_budget_both_families']['reset_R_over_abs_tau']
    two_fam = hf['two_family_constants']
    need(all(F(x) == 98 for x in rs.values()) and all(F(two_fam[k]['J_per_abs_tau']) == 28 and F(two_fam[k]['reset_R_per_abs_tau']) == 98
                                                     and F(two_fam[k]['C_F_per_site_per_abs_tau']) == 56 for k in ('F1', 'F2'))
         and F(two_fam['self_map']) == F(37, 6250000) and F(two_fam['exclusion']) == F(77, 390625), 'reset_98_J_28_C_F_56_contraction')
    # rho^(1)_R
    fo_f = {c['id']: c for c in cf}['first_order_density_explicit']
    fo_r = {c['id']: c for c in cr}['item3_first_order_density_explicit']
    faces_f = sorted(fo_f['faces_owner_set_R'])
    faces_r = sorted({c['id']: c for c in cr}['face_counts_R_local']['F_R'])
    mine = sorted('%s r=%d s=%d' % (f['orient'], f['r'], f['s']) for f in pre.omitted_faces((0, 0, 0))
                  if f['owners'] == frozenset(pre.R_COVER))
    need(len(mine) == 10 and sorted(re.search(r'(xy|xz|yz) r=\d s=\d', x).group(0) for x in faces_f) == mine
         and all('anchor (0, 0, 0)' in x for x in faces_f) and all('anchor=(0, 0, 0)' in x for x in faces_r)
         and sorted(x.split(' anchor')[0] for x in faces_r) == mine, 'rho1_ten_faces_identical', faces=mine)
    need(F(fo_f['tr_rho1_W']) == cap / 144 and F(fo_r['Tr_rho1_W']) == F(1, 144) and F(fo_f['trace_norm_squared']) == ref['tn_sq']
         and F(fo_r['trace_norm_squared']) == F(10, 5184) and fo_f['tr_rho1_W_equals_aw1'] == '+tau/144'
         and '+tau/144' in aw1['accepted'], 'rho1_trace_W_and_trace_norm', trace_norm='sqrt(10)|tau|/72', trace_norm_sq_at_cap=q(ref['tn_sq']))
    # K_2'
    k2p = ref['K2p']
    need(k2p == F(hf['K2_prime']) == F(hr['K2_prime']['exact']) == F(prer['second_order']['K2_prime'])
         and ref['K2plus'] == k2p_gate == F(hf['K2_plus']) == F(hr['K2_plus']['exact']) and k2p > k2p_gate
         and F(hr['K2_prime_over_K2_plus']['exact']) == k2p / k2p_gate, 'K2_prime_identical_in_three_computations',
         K2_prime=q(k2p), K2_plus=q(k2p_gate), ratio=preview(k2p / k2p_gate, 9))
    need(validate_producer_values(rf, 'forward', cap) and validate_producer_values(rr, 'reverse', cap),
         'producer_value_validator_accepts_frozen_packets')
    var = {c['id']: c for c in cr}['item3_K2_prime_versus_K2_plus']['variants']
    v = ref['v']
    t_d = v['T']
    rho288 = 288 * v['J'] * t_d / (1 - 8 * t_d)
    items288, _ = pre.k2_prime_items(cap, rho_override=rho288)
    k288 = sum(items288.values(), F(0)) / cap ** 2
    eps_adm = v['eps_F']
    adm = (ref['items']['am2_remainder'] + ref['items']['straddling'] + ref['items']['two_creation']
           + 2 * eps_adm ** 2 + 2 * eps_adm ** 2 * 10 * v['a']) / cap ** 2
    both = F(var['both_refinements']['K2_prime']['exact']) * cap ** 2
    rest288 = items288['straddling'] + items288['two_creation'] + items288['density'] + items288['normalization']
    xb = (both - rest288) / (2 * rho288)
    need(F(var['directed_am2_remainder_288']['K2_prime']['exact']) == k288 and F(var['admitted_eps_in_density']['K2_prime']['exact']) == adm
         and xb > 0 and xb * xb >= 2 and k2p_gate < both / cap ** 2 < k288 < k2p < adm, 'reverse_labelled_variants_valid',
         K2_288=preview(k288), K2_both=preview(both / cap ** 2), K2_admitted_eps=preview(adm),
         note='every labelled variant exceeds K_2^+; the 288 form uses G(t)-16<=288t/(1-8t) with t<=T')
    floor = 2 * v['rho'] / cap ** 2
    need(floor > k2p_gate and 2 * rho288 / cap ** 2 > k2p_gate, 'trace_norm_K2_floor_exceeds_K2_plus',
         floor_2rho=preview(floor), floor_2rho_288=preview(2 * rho288 / cap ** 2))
    need(ref['K2W'] < k2p_gate and k2p_gate - ref['K2W'] < F(1, 3), 'W_projected_R_local_below_K2_plus', K2_W=preview(ref['K2W']))
    # supplementary observation
    sup = {c['id']: c for c in cf}['second_order_difference_2K2prime']['supplementary_corollary']
    lo_f, hi_f = F(sup['lower']), F(sup['bound'])
    lo_r = F({c['id']: c for c in cr}['first_order_mean_charged']['proved_first_order_lower']['exact'])
    need(F(43786, 10 ** 14) <= lo_f and F(43786, 10 ** 14) <= lo_r and hi_f <= F(44055, 10 ** 14) and lo_f < hi_f
         and hi_f <= F(prer['second_order']['first_order_resolved_tier_upper']) and hi_f < d_gate / 30,
         'supplementary_two_sided_observation_in_bracket', lower_forward=preview(lo_f), lower_reverse=preview(lo_r),
         upper_forward=preview(hi_f), bracket=['4.3786e-10', '4.4055e-10'],
         status='labelled observation only; not a contract target, not an admitted tier')
    sep = F({c['id']: c for c in cr}['common_clock']['plus_minus_tau_first_order_separation_lower']['exact'])
    need(sep == 2 * lo_r and abs(sep - F(prer['second_order']['plus_minus_tau_separation_lower'])) < F(1, 10 ** 20) and sep < two_d,
         'plus_minus_tau_separation_agrees', separation=preview(sep))
    need(2 * k2p * cap ** 2 == F(hf['two_K2_prime_tau2']) and 2 * k2p * cap ** 2 < two_d, 'two_K2_prime_tau2_equal',
         value=q(2 * k2p * cap ** 2), ratio_2D=preview(two_d / (2 * k2p * cap ** 2), 8))

    # ================= gate fields, flags, sentences, phrasing
    gate_keys = sorted(pr['gate_fields_required'])
    need(all(rf[k] is False and rr[k] is False for k in gate_keys) and rf['rate_in_N_claimed'] is False
         and 'rate_in_N_claimed' not in rr, 'gate_fields_false_in_both', fields=gate_keys,
         finding='reverse does not export rate_in_N_claimed (Jung field, not contract-required)')
    flags = ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift', 'scientific_priority_verified')
    need(all(rf[k] is False and rr[k] is False for k in flags) and rf['label'] == rr['label'] == 'uniform_local_closeness_not_uniqueness'
         and rf['topology']['states'] == rr['topologies']['states'] == 'trace norm on B(H_R)'
         and 'compact time windows' in rf['topology']['dynamics'] and 'compact time windows' in rr['topologies']['dynamics'],
         'claim_flags_label_topologies')
    tmpl = pr['mandatory_sentence_template']
    rep_f = (FWD / 'report.md').read_text()
    rep_r = (REV / 'report.md').read_text()
    need(tmpl in rep_f and rf['mandatory_sentence_contract_filled'].startswith(tmpl) and template_in_order(rr['mandatory_sentence_contract_template'])
         and template_in_order(rep_r) and not template_in_order(tmpl.replace('does not assert', 'asserts')),
         'mandatory_sentence_template_present', forward='verbatim', reverse='filled in order (clauses verbatim, constants inserted)')
    bad_f, bad_r = phrase_scan(rep_f), phrase_scan(rep_r)
    need(bad_f == [] and bad_r == [] and 'a chosen subsequential' in rep_f and 'a chosen subsequential' in rep_r
         and phrase_scan('The AQ state is identified.') != [] and phrase_scan('A unique limit exists.') != [],
         'forbidden_phrase_scan_both_reports', rule='code spans removed; the AQ state only in the negated verbatim exclusion')
    qf, qr = rf['quantitative_boundary_comparison'], rr['quantitative_boundary_comparison_definition']
    need('variational' in qf['not'] and qf['variational_selection_claimed'] is False and 'not a variational statement' in qr,
         'quantitative_boundary_comparison_defined_both')

    # ================= source-edit mutations
    base_f = mutated_run('forward')
    base_r = mutated_run('reverse')
    need(base_f[0] == 0 and base_f[1] == (FWD / 'output/results.json').read_bytes()
         and base_r[0] == 0 and base_r[1] == (REV / 'output/results.json').read_bytes(),
         'mutation_harness_unmutated_copies_reproduce_frozen_results')
    must_abort = [
        ('forward', 'am2_item_halved', {'edits': [("        am2 = 4 * rho\n", "        am2 = 2 * rho\n")]}),
        ('forward', 'straddling_pin_66', {'edits': [("        ('straddling', 2 * T * (pins['straddling'] * a + 2 * rho)),\n",
                                                     "        ('straddling', 2 * T * ((pins['straddling'] - 6) * a + 2 * rho)),\n")]}),
        ('forward', 'density_item_zeroed', {'edits': [("        ('density', 2 * epsR ** 2),\n", "        ('density', 0 * epsR ** 2),\n")]}),
        ('forward', 'F2_rule_replaced_by_F1', {'edits': [("            elif family == 'F2' and owner_set(f) <= box:\n",
                                                          "            elif family == 'F2' and star_in:\n")]}),
        ('forward', 'amplitude_tau_over_576', {'edits': [("    per_face = Q(1, 72) * Q(1, 2)", "    per_face = Q(1, 576) * Q(1, 2)")]}),
        ('forward', 'straddling_faces_in_rho1', {'edits': [("    F_R = sorted(inside, key=face_key)\n",
                                                            "    F_R = sorted(inside + straddling[:2], key=face_key)\n")]}),
        ('forward', 'uniqueness_claimed_true', {'edits': [("    CLAIMS = {'uniqueness_claimed': False,", "    CLAIMS = {'uniqueness_claimed': True,")]}),
        ('forward', 'continuum_flag_true', {'edits': [("    FLAGS = {'continuum_claim': False,", "    FLAGS = {'continuum_claim': True,")]}),
        ('forward', 'contract_target_byte_edit_no_rehash', {'contract_edit': (b'"value": "1/1250000"', b'"value": "1/125000"')}),
        ('forward', 'contract_target_rehashed_1_125000', {'contract_edit': (b'"value": "1/1250000"', b'"value": "1/125000"'),
                                                          'rehash': True}),
        ('forward', 'undeclared_input_reverse_report', {'extra_input': 'research/round32/reverse/ay1/report.md'}),
        ('forward', 'report_forbidden_phrase', {'report_append': '\nThe AQ state is unique.\n'}),
        ('reverse', 'am2_item_halved', {'edits': [("        Term('am2_remainder', 2 * in_R,", "        Term('am2_remainder', in_R,")]}),
        ('reverse', 'F2_rule_replaced_by_F1', {'edits': [("            if all(o in sites for o in owners):\n",
                                                          "            if all(vadd(b, v) in sites for v in STAR):\n")]}),
        ('reverse', 'padding_removed', {'edits': [("    return {'volume_B': B, 'am2_volume': Bplus,", "    return {'volume_B': B, 'am2_volume': B,")]}),
        ('reverse', 'bures_bound_doubled', {'edits': [("    return 4 * eps / (1 + eps ** 2)\n", "    return 8 * eps / (1 + eps ** 2)\n")]}),
        ('reverse', 'continuum_flag_true', {'edits': [("    validate_claim_flags(dict(gate_fields, continuum_claim=False,",
                                                       "    validate_claim_flags(dict(gate_fields, continuum_claim=True,")]}),
        ('reverse', 'contract_target_byte_edit_no_rehash', {'contract_edit': (b'"value": "1/1250000"', b'"value": "1/125000"')}),
        ('reverse', 'contract_target_rehashed_1_125000', {'contract_edit': (b'"value": "1/1250000"', b'"value": "1/125000"'),
                                                          'rehash': True}),
        ('reverse', 'skeptic_triage_added_to_inputs', {'extra_input': 'research/round32/skeptic/triage.md'}),
        ('reverse', 'forward_report_added_to_inputs', {'extra_input': 'research/round32/forward/ay1/report.md'}),
        ('reverse', 'report_forbidden_phrase', {'report_append': '\nThe AQ state is unique.\n'}),
    ]
    receipts = []
    for direction, label, spec in must_abort:
        code, results, last = mutated_run(direction, **spec)
        need(code != 0 and results is None, 'mutation_aborts_%s_%s' % (direction, label), last_error_line=last)
        receipts.append({'direction': direction, 'mutation': label, 'producer_aborted': True, 'last_error_line': last})
    silent = [
        ('forward', 'supplementary_lower_uses_half_K2', {'edits': [("    corollary_low = tn_down - K2['+']['total']\n",
                                                                     "    corollary_low = tn_down - K2['+']['total'] / 2\n")]}),
        ('forward', 'orthogonal_variant_sqrt2_rounded_down', {'edits': [("        am2 = 2 * sqrt_up(2) * rho\n",
                                                                          "        am2 = 2 * sqrt_down(2) * rho\n")]}),
        ('reverse', 'eps_R_pinned_to_49_faces', {'edits': [("    return 82 * a + 2 * rho + (33 * a + rho) ** 2\n",
                                                             "    return 49 * a + 2 * rho + (33 * a + rho) ** 2\n")]}),
        ('reverse', 'straddling_pinned_to_66_faces', {'edits': [("eps_mode='R_local', straddle_faces=72,",
                                                                  "eps_mode='R_local', straddle_faces=66,")]}),
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
        'D': q(d_gate), 'two_D': q(two_d), 'target': q(target), 'two_D_i': q(2 * ref['D_i']),
        'J_pad_over_tau': '28', 'J0': '7/25000000', 'self_map': '37/6250000', 'exclusion': '77/390625',
        'reset_R_over_tau': '98', 'C_F_over_tau_per_site': '56',
        'counts': {'per_factor': 49, 'faces_meeting_R': 82, 'inside_R': 10, 'straddling': 72, 'one_site_straddling': 66,
                   'single_contact_per_site': 33, 'containing_both': 16, 'strictly_containing': 6, 'owner_sets_meeting_R': 27},
        'families': {str(n): {k: q(val) if isinstance(val, F) else val for k, val in fam[n].items()} for n in (2, 3)},
        'rho1_R': '(tau/72) sum over the 10 faces with owner set {0,e_z} of (|W_f Omega_R><Omega_R| + h.c.)',
        'rho1_trace_norm_sq_at_cap': q(ref['tn_sq']), 'tr_rho1_W_at_cap': q(cap / 144),
        'K2_prime': q(k2p), 'K2_prime_items_over_tau2': {k: q(x / cap ** 2) for k, x in ref['items'].items()},
        'K2_plus': q(k2p_gate), 'K2_prime_over_K2_plus': q(k2p / k2p_gate), 'two_K2_prime_tau2': q(2 * k2p * cap ** 2),
        'K2_W_projected': q(ref['K2W']), 'K2_288': q(k288), 'K2_admitted_eps': q(adm), 'floor_2rho': q(floor),
        'bures_pairwise': q(4 * eps_adm / (1 + eps_adm ** 2)), 'fidelity_floor': q(1 / (1 + eps_adm ** 2)),
        'supplementary_lower_forward': q(lo_f), 'supplementary_lower_reverse': q(lo_r), 'supplementary_upper_forward': q(hi_f),
        'plus_minus_separation_lower': q(sep),
    }
    previews = {
        'D': preview(d_gate), 'two_D': preview(two_d), 'target_over_two_D': preview(target / two_d, 8),
        'two_D_i': preview(2 * ref['D_i']), 'K2_prime': preview(k2p), 'K2_plus': preview(k2p_gate),
        'K2_prime_over_K2_plus': preview(k2p / k2p_gate, 9), 'K2_prime_orthogonal_forward': preview(F(hf['K2_prime_orthogonal_variant_upper'])),
        'K2_288': preview(k288), 'K2_both_refinements': preview(both / cap ** 2), 'K2_admitted_eps': preview(adm),
        'K2_W_projected': preview(ref['K2W']), 'two_K2_prime_tau2': preview(2 * k2p * cap ** 2),
        'rho1_trace_norm_upper_forward': preview(F(hf['rho1_R_trace_norm_upper'])),
        'supplementary_bracket': [preview(lo_f), preview(hi_f)], 'plus_minus_separation': preview(sep),
        'bures_pairwise': preview(4 * eps_adm / (1 + eps_adm ** 2)),
        'note': 'decimal previews only; every Boolean above was decided on exact rationals',
    }
    return {
        'schema': 'hnm-r32-skeptic-postcomparison-v1', 'loop': 'AY1', 'stage': 'post_comparison',
        'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'model-agent skeptic with correlated ancestry; not human peer review or formal verification',
        'contract_sha256': CONTRACT_SHA, 'pre_comparison_module_sha256': sha(HERE / 'ay1_check.py'),
        'exact': exact, 'previews': previews, 'mutation_receipts': receipts, 'passed': True,
        'checks': CHECKS, 'checks_count': len(CHECKS),
    }


def main():
    ap = argparse.ArgumentParser(description='AY1 post-comparison skeptic checks')
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
    print(json.dumps({'loop': 'AY1', 'stage': 'post_comparison', 'checks': result['checks_count'],
                      'two_D': result['previews']['two_D'], 'K2_prime': result['previews']['K2_prime'],
                      'mutations': len(result['mutation_receipts'])}, sort_keys=True))


if __name__ == '__main__':
    main()
