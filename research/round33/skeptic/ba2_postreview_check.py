#!/usr/bin/env python3
"""BA2 post-comparison skeptic checks, written after both producer freezes.

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated
ancestry (same model family as the advisor, the lenses and both producers; the
route, the loop-1 previews and most of the frozen control semantics came from
the skeptic's own triage and loop-2 review); not human peer review or formal
verification.

What this adds to the frozen pre-comparison package (ba2_check.py, 95 checks,
committed at 7daf273 before the reverse 9f207fe and the forward 302347b):
  * integrity: contract hash; the unchanged pre-comparison package and a byte
    replay of ba2_check.py; both freeze closures file by file; both premise
    inventories on the real snapshots (29 files each = AGENTS.md + contract +
    27 shared premises, byte-identical to the repository; reverse isolation);
    each producer's check.py sha256 recorded before evaluation; normal and -O
    replays of both producers reproducing output/ byte for byte;
  * every producer headline compared exactly with the skeptic's independent
    values (the pre-comparison module's geometry and enclosures, never a
    producer value): forward K_cmp, K_c1, K_c2; reverse K_cmp, c1, c2 with the
    E_up remainder reconciled against the skeptic's closed form and sharp
    enclosure; the tau/100 ratios; the extra-face enumeration and all-size
    formula; exact distance sums; padding; the sharp (48) supremum observation;
  * the Nachtergaele-Sims passages quoted in both reports matched line by line
    against the committed excerpt; gate fields and claim flags; the round tool
    research/round33/tools/phrase_scan.py on both reports; the mandatory sentence
    as one unbroken span; the O6 rerun and the identification on local algebras;
  * source-edit runs on temporary copies outside the checkout: one validator
    weakening per contract control per producer (70 runs; the producer checker
    must then abort with 'damaging mutation accepted: <label>'), must-abort
    headline and provenance edits, unmutated copies that must reproduce the
    frozen results byte for byte, and silent edits that the producer checkers do
    not pin, which this review's value validator must catch.

Standard library only; exact Fractions decide every Boolean; failures are explicit
exceptions (never assert), so the output bytes match under python -O.

Usage: python3 -B research/round33/skeptic/ba2_postreview_check.py --output /abs/fresh/dir
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
import ba2_check as pre  # noqa: E402  (the skeptic's own frozen pre-comparison module)

ROOT = HERE.parents[2]
R33 = ROOT / 'research/round33'
CONTRACT = R33 / 'contracts/ba2.json'
CONTRACT_SHA = '275ba3b002529b7295d0f8b91dc1cc7a96451e3c7f936ee698a932fdca54fcff'
NS_EXCERPT = R33 / 'sources/nachtergaele-sims-1410.8174v1.md'
FWD = R33 / 'forward/ba2'
REV = R33 / 'reverse/ba2'
SIDES = {'forward': FWD, 'reverse': REV}
PRE_RESULTS = HERE / 'ba2-independent/results.json'
PRE_FREEZE = HERE / 'ba2-independent-freeze.json'
PHRASE_SCAN = R33 / 'tools/phrase_scan.py'
PHRASE_SCAN_SHA = '028af4c14edbb2fae096a91cb723ccefb036e7550088907ef47062774871f67c'
FROZEN = {  # frozen producer artifacts (sha256 at review time; commits 302347b forward, 9f207fe reverse)
    'forward': {'output/results.json': '4e85123b1a386d514fa709652706dd6227e55d6190989c50bfa04805c20d5cf9',
                'output/source-manifest.json': '73925914d27f602a180cfa15bfde21829ab481d95c11c98f57a1834125744b04',
                'freeze.json': '255988f344f5e900092dca1a2bd9ff591618b620072c3d783af8a9e09e0fe058',
                'check.py': '2b36f3e9e6db17613637f84778ce69b2a861b5b7eebf4e048a935de66f549f71',
                'report.md': '101b404ce2aea29ed6bfd7264f6b4527c7decb73aea9386ce0885fa9b72f7d98'},
    'reverse': {'output/results.json': 'ac9b5cf7fae17be35b5922ff72d19c6b7a4e45707394843aa14098c7dac6625c',
                'output/source-manifest.json': '91e45888bb4ef3df573d2b20da10bd6440ed4785d4d5a0453e5f02a23bf33ff4',
                'freeze.json': '4dfc52788c7adfc78b0a1dcb8d961764c022cb415ae6fcb97eff6b586eb8ceeb',
                'check.py': '7fc29c0b5136572f23b8da18d823b1d564ec5709cc9e3a8d20f59d13a8ab3ca6',
                'report.md': 'b6615292a7c1f418d567cd17b989605634b2610fc8b1fe30c313d4a3a6cb1ff4'},
}
FORBIDDEN_IN_REVERSE = ('research/round33/skeptic/', 'research/round33/experts/', 'research/round33/forward/',
                        'research/round33/advisor/deliberation', 'research/round33/advisor/plan.json',
                        'research/round33/advisor/panel')


class ReviewFailure(RuntimeError):
    """A post-review check failed."""


class Rejected(Exception):
    """The skeptic value validator refused a producer results packet."""


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise ReviewFailure(cid)
    if any(row['id'] == cid for row in CHECKS):
        raise ReviewFailure('duplicate check id ' + cid)
    row = {'id': cid, 'passed': True}
    row.update(detail)
    CHECKS.append(row)


def q(x):
    return str(x)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def factorial(n):
    out = 1
    for k in range(2, n + 1):
        out *= k
    return out


def preview(x, digits=12):
    return format(float(x), '.%de' % digits)


def dec_forward(value, digits=12):
    """Replica of the forward producer's truncated preview format (used only to compare its exported strings)."""
    value = F(value)
    if value == 0:
        return '0'
    sign = '-' if value < 0 else ''
    value = abs(value)
    e = 0
    while value >= F(10) ** (e + 1):
        e += 1
    while value < F(10) ** e:
        e -= 1
    scaled = value / F(10) ** (e - digits + 1)
    m = str(scaled.numerator // scaled.denominator)
    return sign + m[0] + '.' + m[1:] + 'e' + str(e)


# ------------------------------------------------------------ skeptic reference values
TAU = F(1, 10 ** 8)
U = F(1)
C = F(224)
X_PHI = 2 * C * 2268 * TAU * U          # 3969/390625
X_PHIP = 2 * C * 1323 * TAU * U         # 9261/1562500


def e_up(y):
    """The reverse producer's rational remainder, re-derived: E(y)=2(e^y-1-y)/y^2 <= 1+y/3+y^2/(12(1-y/5))."""
    return 1 + y / 3 + y * y / (12 * (1 - y / 5))


def closed(lead, x):
    return lead * TAU ** 2 / (1 - x / 3)


def reference():
    ref = {}
    s_lo, s_hi = pre.e2_enclosure(X_PHI)      # (e^x-1-x)/x^2
    p_lo, p_hi = pre.e2_enclosure(X_PHIP)
    ref['sharp'] = {
        'fwd_cmp': (508032 * TAU ** 2 * s_lo, 508032 * TAU ** 2 * s_hi),
        'rev_cmp': (296352 * TAU ** 2 * p_lo, 296352 * TAU ** 2 * p_hi),
        'c1_star': (2032128 * TAU ** 2 * s_lo, 2032128 * TAU ** 2 * s_hi),
        'c1_face': (1185408 * TAU ** 2 * s_lo, 1185408 * TAU ** 2 * s_hi),
        'c2_face': (691488 * TAU ** 2 * p_lo, 691488 * TAU ** 2 * p_hi),
    }
    ref['closed'] = {'fwd_cmp': closed(254016, X_PHI), 'rev_cmp': closed(148176, X_PHIP), 'c1_star': closed(1016064, X_PHI),
                     'c1_face': closed(592704, X_PHI), 'c2_face': closed(345744, X_PHIP)}
    ref['closed']['fwd_c2'] = ref['closed']['c1_face'] + F(11, 8) * ref['closed']['fwd_cmp']
    ref['eup'] = {'rev_cmp': 148176 * TAU ** 2 * e_up(X_PHIP), 'rev_c1': 1016064 * TAU ** 2 * e_up(X_PHI),
                  'rev_c2': 345744 * TAU ** 2 * e_up(X_PHIP)}
    ref['eup_at_x'] = {'x_phi': e_up(X_PHI), 'x_phiprime': e_up(X_PHIP)}
    ref['e2_sharp'] = {'x_phi': (2 * s_lo, 2 * s_hi), 'x_phiprime': (2 * p_lo, 2 * p_hi)}
    t100 = TAU / 100
    ref['ratios'] = {
        'fwd_closed': ref['closed']['fwd_cmp'] / (254016 * t100 ** 2 / (1 - X_PHI / 300)),
        'rev_cmp': 10 ** 4 * e_up(X_PHIP) / e_up(X_PHIP / 100),
        'rev_c1': 10 ** 4 * e_up(X_PHI) / e_up(X_PHI / 100),
    }
    fams = {}
    for n in (2, 3, 4, 5):
        lam, f1, f2, extra = pre.families(n)
        owners = [y for f in extra for y in f['owners']]
        fams[n] = {'F1': len(f1), 'F2': len(f2), 'extra': len(extra), 'incidences': len(owners),
                   'min_ez': min(pre.d1(y, pre.E_Z) for y in owners), 'min_0': min(pre.d1(y, pre.ORIGIN) for y in owners),
                   'max_owners': max(len(f['owners']) for f in extra),
                   'S': sum((pre.Ff(pre.d1(x, y)) for f in extra for x in pre.R_COVER for y in f['owners']), F(0)),
                   'padding': len({pre.add(b, s) for b in lam for s in pre.S_STAR} - lam),
                   'partial_groups': len({f['anchor'] for f in extra})}
    ref['families'] = fams
    return ref


# ------------------------------------------------------------ producer value validator
def check_map(results):
    return {c['id']: c for c in results['checks']}


def validate_producer_values(results, direction, ref):
    """Reject a producer results packet whose exported values differ from the skeptic's exact derivation."""
    cl, eup, fam = ref['closed'], ref['eup'], ref['families']
    if results.get('contract_sha256') != CONTRACT_SHA:
        raise Rejected('contract sha256')
    if direction == 'forward':
        h, cm = results['headline'], check_map(results)
        if F(h['comparison']['K_cmp']) != cl['fwd_cmp']:
            raise Rejected('forward K_cmp differs from the skeptic closed form')
        if F(h['cauchy_F1']['K_c1']) != cl['c1_face']:
            raise Rejected('forward K_c1 differs from the skeptic face-charged closed form')
        if F(h['cauchy_F2']['K_c2']) != cl['fwd_c2']:
            raise Rejected('forward K_c2 differs from K_c1 + (11/8) K_cmp')
        for key in ('cmp', 'c1', 'c2'):
            if F(cm['tau_scaling_exponent']['ratios'][key]['exact']) != ref['ratios']['fwd_closed']:
                raise Rejected('forward tau/100 ratio differs')
        if F(cm['insufficient_verdict_retained']['retained_labelled_weaker_bound']['coefficient']) != 2 * cl['c1_face']:
            raise Rejected('retained triangle coefficient differs from 2 K_c1')
        prev = cm['comparison_bound_all_N']['b_N_all_size_preview']
        for n in range(2, 11):
            if prev[str(n)] != dec_forward(cl['fwd_cmp'] * F(5 * n + 1, n ** 3)):
                raise Rejected('b(N) all-size preview differs at N=%d' % n)
        refine = cm['comparison_bound_all_N']['labelled_refinement_enumerated_sum']
        enum = cm['extra_face_count_and_distance']['enumeration']
        for n in (2, 3, 4):
            e = enum[str(n)]
            if (e['F1'], e['F2'], e['extra'], e['incidences'], e['min_l1_from_e_z'], e['min_l1_from_0'], e['max_owners']) != (
                    fam[n]['F1'], fam[n]['F2'], fam[n]['extra'], fam[n]['incidences'], fam[n]['min_ez'], fam[n]['min_0'],
                    fam[n]['max_owners']):
                raise Rejected('forward enumeration differs at N=%d' % n)
            if F(e['S_b_exact']) != fam[n]['S']:
                raise Rejected('forward exact distance sum differs at N=%d' % n)
            if F(refine[str(n)]['b_N']) != cl['fwd_cmp'] * fam[n]['S'] / 168:
                raise Rejected('forward labelled refinement differs at N=%d' % n)
        if '567|tau|' not in cm['missing_incoming_stars']['labelled_observation']:
            raise Rejected('forward sharp (48) supremum observation differs')
    else:
        h, cm = results['headline'], check_map(results)
        if F(h['comparison_coefficient']['exact']) != eup['rev_cmp']:
            raise Rejected('reverse K_cmp differs from 148176 tau^2 E_up(x)')
        if F(h['cauchy_coefficient_F1']['exact']) != eup['rev_c1']:
            raise Rejected('reverse c1 differs from 1016064 tau^2 E_up(x)')
        if F(h['cauchy_coefficient_F2']['exact']) != eup['rev_c2']:
            raise Rejected('reverse c2 differs from 345744 tau^2 E_up(x)')
        sc = results['scaling']
        if (F(sc['comparison_coefficient']['exact']) != ref['ratios']['rev_cmp'] or F(sc['cauchy_coefficient_F2']['exact'])
                != ref['ratios']['rev_cmp'] or F(sc['cauchy_coefficient_F1']['exact']) != ref['ratios']['rev_c1']):
            raise Rejected('reverse tau/100 ratio differs')
        for n, v in h['b_N_values'].items():
            if F(v['exact']) != eup['rev_cmp'] * F(5 * int(n) + 1, int(n) ** 3):
                raise Rejected('reverse b(N) differs at N=' + n)
        for n, v in h['labelled_weaker_triangle_bound'].items():
            if F(v['triangle_through_limits']['exact']) != (eup['rev_c1'] + eup['rev_c2']) / (int(n) - 1):
                raise Rejected('reverse triangle bound differs at N=' + n)
        pref = 2 * 1323 * TAU * e_up(X_PHIP) * (TAU / 3)
        for n, v in h['labelled_sharper_enumerated_comparison'].items():
            if F(v['exact_boundary_sum']['exact']) != fam[int(n)]['S']:
                raise Rejected('reverse exact distance sum differs at N=' + n)
            if F(v['labelled_comparison_value']['exact']) != pref * fam[int(n)]['S']:
                raise Rejected('reverse labelled sharper comparison value differs at N=' + n)
        for n, v in cm['item4_limit_identification']['general_X_example_Lambda_1']['b_X'].items():
            if F(v['exact']) != pref * 28 * int(n) * (5 * int(n) + 1) * 3 * 27 * pre.Ff(int(n) - 1):
                raise Rejected('reverse general-X example differs at N=' + n)
        en = results['boundary_source']['enumerated']
        for n in (2, 3):
            e = en[str(n)]
            if (e['count'], e['min_dist_0'], e['min_dist_e_z'], e['max_owners'], e['padding_sites'], e['partial_groups']) != (
                    fam[n]['extra'], fam[n]['min_0'], fam[n]['min_ez'], fam[n]['max_owners'], fam[n]['padding'],
                    fam[n]['partial_groups']):
                raise Rejected('reverse enumeration differs at N=%d' % n)
        sharp48 = cm['item1_interaction_norms_Phi_and_Phi_prime']['labelled_exact_48_norms_not_used']
        if (sharp48['owner_set_per_tau'], sharp48['whole_star_per_tau']) != ('108', '567'):
            raise Rejected('reverse sharp (48) norms differ')
    con = json.loads(CONTRACT.read_text())
    if results['gate_fields'] != con['preregistration']['gate_fields_required']:
        raise Rejected('gate fields differ from the contract')
    for key in ('continuum_claim', 'scientific_priority_verified', 'gns_dynamics_equality_claimed', 'uniform_in_time_claimed',
                'rate_in_a_claimed', 'uniqueness_of_ground_state_claimed', 'weak_coupling_claim', 'common_limit_claimed',
                'state_convergence_claimed'):
        if results.get(key) is not False:
            raise Rejected('claim flag ' + key)
    return True


# ------------------------------------------------------------ report text checks
def normalize(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def forward_quote_lines(report):
    body = report.split('### 2.1 Verbatim quotations')[1].split('### 2.2')[0]
    blocks = re.findall(r'```text\n(.*?)```', body, re.S)
    if len(blocks) != 2:
        raise ReviewFailure('forward quotation blocks')
    return [ln for ln in blocks[0].splitlines() if ln.strip()], [ln for ln in blocks[1].splitlines() if ln.strip()]


def reverse_quote_lines(report):
    body = report.split('### 1.1 Verbatim quotation')[1].split('### 1.2')[0]
    quoted = [ln[2:] for ln in body.splitlines() if ln.startswith('> ') and ln[2:].strip()]
    blocks = re.findall(r'```text\n(.*?)```', body, re.S)
    if len(blocks) != 1:
        raise ReviewFailure('reverse (47) block')
    return quoted, [ln for ln in blocks[0].splitlines() if ln.strip()]


# ------------------------------------------------------------ source-mutation replays
def mutated_run(direction, edits=(), extra_input=None, contract_edit=None, rehash=False, report_edits=(), report_append=None):
    src = SIDES[direction]
    with tempfile.TemporaryDirectory(prefix='hnm-r33-ba2-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / 'research/round33' / direction / 'ba2'
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        code = (dst / 'check.py').read_text()
        for old, new in edits:
            if code.count(old) != 1:
                raise ReviewFailure('mutation anchor not unique in %s: %r' % (direction, old[:70]))
            code = code.replace(old, new)
        if contract_edit is not None:
            cpath = dst / 'inputs/research/round33/contracts/ba2.json'
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
        if report_edits or report_append is not None:
            rp = dst / 'report.md'
            text = rp.read_text()
            for old, new in report_edits:
                if text.count(old) != 1:
                    raise ReviewFailure('report mutation anchor not unique in %s: %r' % (direction, old[:70]))
                text = text.replace(old, new)
            if report_append is not None:
                text += report_append
            rp.write_text(text)
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


def replay(script, optimized):
    with tempfile.TemporaryDirectory(prefix='hnm-r33-ba2-skeptic-replay-') as tmp:
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if optimized else [])
        done = subprocess.run([sys.executable] + flags + [str(script), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(ROOT))
        if done.returncode != 0:
            raise ReviewFailure('replay failed: ' + str(script))
        return {p.relative_to(out).as_posix(): sha(p) for p in sorted(out.rglob('*')) if p.is_file()}, done.stdout.strip()


def verify_closure(direction, con):
    src = SIDES[direction]
    freeze = json.loads((src / 'freeze.json').read_text())
    prefix = src.relative_to(ROOT).as_posix() + '/'
    sources = freeze['sources']
    files = {p.relative_to(ROOT).as_posix() for p in src.rglob('*') if p.is_file() and p != src / 'freeze.json'}
    ok = (freeze['loop'] == 'BA2' and freeze['direction'] == direction and freeze['contract_sha256'] == CONTRACT_SHA
          and all(n.startswith(prefix) for n in sources) and set(sources) == files
          and all(sha(ROOT / n) == d for n, d in sources.items())
          and not any('__pycache__' in n or n.endswith('.pyc') for n in files)
          and freeze['normal_optimized_identical'] is True)
    inputs = sorted(p.relative_to(src / 'inputs').as_posix() for p in (src / 'inputs').rglob('*') if p.is_file())
    declared = sorted(['AGENTS.md', 'research/round33/contracts/ba2.json'] + list(con['shared_premises']))
    snapshots_equal = all((src / 'inputs' / n).read_bytes() == (ROOT / n).read_bytes() for n in inputs)
    return ok, inputs, declared, snapshots_equal, len(sources)


def weaken(line, indent_to='require(True, '):
    """Replace a validator's require(<condition>, head by require(True, (the continuation line is kept)."""
    head = line[:len(line) - len(line.lstrip())]
    rest = line.lstrip()
    if not rest.startswith('require('):
        raise ReviewFailure('not a require line')
    tail = rest[len('require('):]
    # keep the message argument: the comma that ends the condition at bracket depth 0, outside string literals
    depth, cut, quote, i = 0, None, None, 0
    while i < len(tail):
        ch = tail[i]
        if quote:
            if ch == '\\':
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in '\'"':
            quote = ch
        elif ch in '([{':
            depth += 1
        elif ch in ')]}':
            depth -= 1
        elif ch == ',' and depth == 0:
            cut = i
            break
        i += 1
    if cut is None:
        raise ReviewFailure('require line without a message argument')
    return (line, head + indent_to + tail[cut + 1:].lstrip())


# one weakening per contract control and producer: (control id, edits, damaging-mutation label that must then be accepted)
FWD_WEAK = [
    ('coherent_evidence_tampering', [weaken("        require(rat(pk['headline']['comparison']['K_cmp']) == coeff_at(tau_cap, 'cmp'), 'K_cmp differs from recomputation')")],
     'K_cmp_halved_hash_rebound'),
    ('exact_arithmetic_admission', [("        raise AdmissionError('non-exact input rejected: ' + repr(value))", "        return Q(value)")], 'float_input'),
    ('no_priority_or_continuum_claim', [weaken("            require(fl.get(k1) is v1, 'claim flag ' + k1 + ' must be false')")], 'continuum_true'),
    ('changed_model_relabelled', [weaken("        require(mdl == MODEL and mdl['model_id'] == V['model_id'] and rat(mdl['tau']) == tau_cap, 'model packet differs from the contract')")],
     'tau_changed'),
    ('insufficient_verdict_retained', [weaken("        require(label == forward_verdict(*flags), 'verdict label differs from the acceptance rule')")],
     'missed_comparison_relabelled_accepted'),
    ('tau_scaling_exponent', [weaken("        require(br[0] <= ratio <= br[1], 'scaling ratio outside the preregistered bracket')")], 'linear_order_bound'),
    ('wrong_delta_alpha_hbar_clock', [weaken("        require(u_v == theta_v / V['u_div'], 'u = delta t/hbar = theta/8 (delta = alpha/8)')")],
     'eightfold_u_labelled_theta'),
    ('missing_incoming_stars', [weaken("        require(stars_counted == 4 and J_per_tau == 28, 'per-site sum must include the incoming stars (4 x 7|tau|)')"),
                                weaken("        require(V['phi_factor_contract'] * J_per_tau == V['phi_contract'], '||Phi||_F <= 81 J with the complete J')")],
     'outgoing_star_only_J_7'),
    ('root_n_misuse', [weaken("        require(total * scale == sum(parts), 'deterministic face bounds add linearly')")], 'division_by_isqrt_of_616_faces'),
    ('tier_mixing_rejected', [weaken("                require(r['phi_F_per_abs_tau'] not in (V['phi_contract'], V['phiprime_contract']), 'exponential tier with polynomial constants')")],
     'exponential_label_on_polynomial_constants'),
    ('reverse_premise_isolation', [weaken("        require(decl is True, 'contract does not declare reverse premise isolation')")], 'declaration_false'),
    ('face_count_all_sites', [weaken("        require(derived_from == 'I1 table, translation covariance, both sites of R', 'pins must be derived at every site of R')"),
                              weaken("        require(pins == derived_pins, 'face pins differ from the I1 derivation')")],
     'site_0_only_count'),
    ('uniform_in_N_not_in_a', [weaken("            require(not bad, 'unqualified uniformity statement in ' + name + ': ' + (bad[0] if bad else ''))")],
     'uniform_in_a_claimed'),
    ('placeholder_span_rejected', [weaken("            require(not spans, 'placeholder span in ' + name + ': ' + (spans[0] if spans else ''))")],
     'whitespace_placeholder'),
    ('negation_aware_phrase_scan', [weaken("            require(not hits, 'affirmative forbidden phrasing in ' + name + ': ' + (hits[0]['phrase'] if hits else ''))")],
     'affirmative_thermodynamic_limit'),
    ('parameters_declare_metric_weights_window', [weaken("            require(key in params and params[key], 'parameters field missing: ' + key)"),
                                                  weaken("        require('theta=alpha t/hbar' in params['window'] and clock.startswith('s=alpha*t_E/hbar'), 'window and clock declared')")],
     'window_field_absent'),
    ('lieb_robinson_polynomial_tail', [weaken("        require(kind == 'sup_over_all_M', 'a Cauchy estimate is a bound for all M greater than N; an N to N+1 bound is not')")],
     'N_to_N_plus_1_bound_as_cauchy'),
    ('lieb_robinson_F_declared', [weaken("            require(phi_upper != V['phi_contract'], \"exponential instance must carry its own ||Phi||_{F_mu} = e^{2mu} 81 J, not AQ1's\")")],
     'exponential_instance_with_AQ1_Phi_norm'),
    ('lieb_robinson_form_quoted', [weaken("            require(q in report, 'verbatim quotation missing from report: ' + key)")], 'velocity_factor_2_dropped'),
    ('unbounded_onsite_interaction_picture', [weaken("        require(onsite_in == 'H_x', 'unbounded onsite Casimirs enter as the local Hamiltonians H_x of (44), never inside Phi')"),
                                              ("        return validate_source_bounded(source_terms)", "        return True")],
     'onsite_in_bounded_interaction'),
    ('duhamel_inner_family_constants', [weaken("        require(record['interaction'] == want[0] and record['phi_F_per_abs_tau'] == want[1], 'constants are not those of the inner family')")],
     'F1_inner_with_owner_set_1323_unstated'),
    ('extra_face_count_and_distance', [weaken("        require(all(count_fn(N) == 28 * N * (5 * N + 1) for N in (2, 3, 4)), 'extra-face count differs from 28N(5N+1)')")],
     'padding_sites_counted_as_faces'),
    ('duhamel_tau_order_quadratic', [weaken("        require(label_order == 2, 'the dynamics difference is labelled quadratic in tau')")],
     'quadratic_bound_labelled_linear'),
    ('time_window_named_common_clock', [weaken("        require(uniform_in_time is False, 'no uniform-in-time claim')")], 'uniform_in_time_claimed'),
    ('algebraic_not_gns_dynamics', [weaken("        require(fields['gns_dynamics_equality_claimed'] is False, 'no equality of GNS dynamics')")],
     'gns_dynamics_equality_claimed'),
    ('f2_limit_dynamics_equals_f1', [weaken("        require(record['basis'] == 'comparison_bound_and_cauchy', 'identification must come through the comparison bound')")],
     'identified_by_local_terms_only'),
    ('two_families_named', [weaken("        require(all('Lambda_N' in x and 'orthant' not in x and 'literal' not in x for x in fam.values()), 'centered boxes only')")],
     'orthant_boxes'),
    ('subsequence_versus_whole_sequence', [weaken("                require(basis == 'cauchy_bound', 'whole-sequence claims come only from a Cauchy bound: ' + obj)")],
     'alternating_sequence_parity_limits'),
    ('decay_rate_in_N_not_a', [weaken("        require(unit == 'per coarse step at fixed spacing', 'rates are per coarse step at fixed spacing and strong bare coupling')")],
     'conversion_to_fm'),
    ('boundary_source_new_terms_only', [weaken("        require(set(charged) == set(outer) - set(inner), 'source must equal the new terms (outer minus inner), no old term, none missing')")],
     'new_star_dropped'),
    ('f2_regrouping_charged_once', [weaken("        require(len(charged) == len(set(charged)), 'a term is charged twice')")], 'face_charged_twice'),
    ('full_original_wilson_cover', [weaken("        require(owners_ == set(COVER_R) and len(cover_links) == 48, 'the cover is the complete factor cover {0,e_z}: 48 links')")],
     'four_drawn_links_as_cover'),
    ('topology_named', [weaken("        require(t['dynamics'] == TOP['dynamics'], 'dynamics topology is the operator norm, uniformly on the compact window')")],
     'strong_relabelled_norm'),
    ('cross_coupling_comparison_rejected', [weaken("        require(tau2 == tau1, 'F1 and F2 are compared at the same coupling')"),
                                            weaken("        require(source_faces_meeting_R(tau2, tau1) == 0, 'the source must be disjoint from R')")],
     'opposite_signs_compared'),
    ('gate_fields_topic_specific', [weaken("        require(sorted(g) == sorted(V['gate_fields']), 'gate fields must be exactly the contract fields')")], 'field_missing'),
]
REV_WEAK = [
    ('coherent_evidence_tampering', [weaken("    require(data.get('reverse_premise_isolation') is True, 'reverse premise isolation flag')")],
     'isolation_flag_flipped_rehashed'),
    ('exact_arithmetic_admission', [("        raise AdmissionError('non-exact numeric input rejected: ' + repr(value))", "        return Q(value)")], 'float_tau'),
    ('no_priority_or_continuum_claim', [weaken("        require(flags.get(key) is False, 'claim flag must be exactly false: ' + key)")], 'continuum_true'),
    ('changed_model_relabelled', [weaken("    require(parse_q(rec.get('tau')) == contract_tau, 'packet tau differs from the contract (retuning or changed model)')")],
     'tau_1e-7'),
    ('insufficient_verdict_retained', [weaken("    require(recorded == want, 'recorded verdict ' + str(recorded) + ' differs from the rule (' + want + ')')")],
     'missed_comparison_relabelled_accepted'),
    ('tau_scaling_exponent', [weaken("    require(lo <= ratio <= hi, 'tau -> tau/100 ratio outside its preregistered bracket')")], 'linear_order_bound'),
    ('wrong_delta_alpha_hbar_clock', [weaken("    require(parse_q(U) == Q(parse_q(theta_window), 8), 'normalized window must be U=Theta/8 (u=theta/8, delta=alpha/8)')")],
     'u_window_labelled_theta'),
    ('missing_incoming_stars', [weaken("    require(stars_per_site == 4, 'per-site sums must count all four incident stars (incoming anchors)')"),
                                weaken("    require(parse_q(j_per_tau) == stars_per_site * parse_q(star_norm_per_tau) == 28, 'J=28|tau|')")],
     'outgoing_star_J'),
    ('root_n_misuse', [weaken("    require(False, 'division by sqrt(N) or sqrt(#faces) rejected for deterministic bounds')")], 'divide_by_sqrt_faces'),
    ('tier_mixing_rejected', [weaken("    require(rec.get('tier') == TIER, 'tier must be named polynomial_lieb_robinson (AQ1 F)')")],
     'exponential_tier_with_polynomial_F'),
    ('reverse_premise_isolation', [weaken("        require(not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in reverse inputs: ' + f)"),
                                   ("    require(sorted(files) == sorted(expected) and len(files) == len(expected),", "    require(True,")],
     'forward_ba2_report_added'),
    ('face_count_all_sites', [weaken("    require(pins.get('provenance') == 'derived from the I1 table by translation covariance', 'face counts must be derived')")],
     'literal_counts'),
    ('uniform_in_N_not_in_a', [("    require(re.search(r'uniform(ly)? in (the )?(lattice spacing|a)(?![a-z0-9_])', low) is None,", "    require(True,")],
     'uniform_in_lattice_spacing'),
    ('placeholder_span_rejected', [weaken("            require(not (re.search(r'\\s', span) or '|' in span or 'e.g.' in span), 'placeholder span blocks the freeze: ' + span[:60])")],
     'placeholder_gate'),
    ('negation_aware_phrase_scan', [weaken("    require(hits == [], 'affirmative forbidden phrasing: ' + (hits[0] if hits else ''))")],
     'affirmative_thermodynamic_limit'),
    ('parameters_declare_metric_weights_window', [weaken("    require('clock' in pre and 'theta=alpha*t/hbar' in pre['clock'] and 'u=theta/8' in pre['clock'], 'clock field')")],
     'clock_removed'),
    ('lieb_robinson_polynomial_tail', [("    require(rec.get('comparison_exponent') == 2 and rec.get('cauchy_exponent') == 1,", "    require(True,")],
     'comparison_N_minus_4'),
    ('lieb_robinson_F_declared', [("    require(inst.get('norm_factor') == 'e^{2 mu} 81 J' and inst.get('C_source') == 'own C_{F_mu}<=224',", "    require(True,")],
     'F_mu_with_AQ1_norm'),
    ('lieb_robinson_form_quoted', [weaken("    require(source_label == NS_REL, 'the Lieb-Robinson form must be quoted from the committed excerpt, not second-hand')")],
     'second_hand_source_aq1'),
    ('unbounded_onsite_interaction_picture', [weaken("    require(rec.get('onsite_in_interaction') is False, 'unbounded on-site term placed inside the bounded interaction')")],
     'onsite_inside_Phi'),
    ('duhamel_inner_family_constants', [weaken("    require(lr['inner_family'] == src['family'], 'a within-family Cauchy estimate uses its own family inside the integral')")],
     'f2_cauchy_with_f1_inner'),
    ('extra_face_count_and_distance', [("        require(data['count'] == 28 * N * (5 * N + 1) and rec.get('count_formula') == '28N(5N+1)',", "        require(True,")],
     'count_140N2_formula'),
    ('duhamel_tau_order_quadratic', [weaken("    require(label == 'quadratic', 'the dynamics difference is O(tau^2 U^2); a linear label is rejected')")], 'linear_label'),
    ('time_window_named_common_clock', [weaken("    require(rec.get('uniform_in_time') is False, 'uniform-in-time claim rejected (bound grows like U^2 e^{vU})')")],
     'uniform_in_time'),
    ('algebraic_not_gns_dynamics', [("    require(rec.get('gns_equality') is False and rec.get('correlation_equality') is False,", "    require(True,")],
     'gns_equality'),
    ('f2_limit_dynamics_equals_f1', [("    require(rec.get('source') == 'comparison bound b(N) -> 0 along the whole sequence',", "    require(True,")],
     'identified_from_static_closeness'),
    ('two_families_named', [weaken("    require(rec == [F1_NAME, F2_NAME], 'exactly the two named families F1 and F2 are compared')")], 'single_family'),
    ('subsequence_versus_whole_sequence', [weaken("        require(rec.get('from') == 'Cauchy bound', 'whole-sequence claims come only from a Cauchy bound')")],
     'states_whole_sequence_from_compactness'),
    ('decay_rate_in_N_not_a', [weaken("        require(re.search(r'(?<![a-z])' + re.escape(bad) + r'(?![a-z])', low) is None, 'rate converted to a physical length or to a')")],
     'converted_to_fm'),
    ('boundary_source_new_terms_only', [weaken("    require(set(source_terms) == set(new_terms), 'boundary source must contain exactly the new terms (no old terms, none missing)')")],
     'comparison_source_short_one'),
    ('f2_regrouping_charged_once', [weaken("    require(charged == new_faces, 'F2 regrouped clipped groups charged more than once (old faces recharged)')")],
     'whole_group_recharge'),
    ('full_original_wilson_cover', [weaken("    require(tuple(sorted(cover)) == COVER, 'cover must be the complete factor cover R={0,e_z} of W')"),
                                    weaken("    require(n_links == 48 and n_endpoints == 36, 'complete cover has 48 links and 36 endpoints')")],
     'cover_zero_only'),
    ('topology_named', [weaken("    require(rec.get('time_continuity') == GNS_TOPOLOGY, 'norm continuity in theta on all of B(H_R) is not claimed')")],
     'norm_continuity_in_theta'),
    ('cross_coupling_comparison_rejected', [weaken("    require(parse_q(tau1) == parse_q(tau2), 'cross-coupling comparison rejected: both families at the same tau')")],
     'plus_versus_minus_tau'),
    ('gate_fields_topic_specific', [weaken("        require(exported[key] is False, 'gate field must be false: ' + key)")], 'gns_equality_true'),
]
TARGET_ANCHOR = (b'<= 6x10^-11 (5N+1) N^-3 ||A||', b'<= 9x10^-11 (5N+1) N^-3 ||A||')
Q51_ANCHOR = '(51) ‖[τ_t^Λ(A), B]‖ ≤ (2‖A‖‖B‖ / C) (e^{2‖Φ‖C|t|} − 1) D(X, Y)'
Q51_PARA = '(51) ‖[τ_t^Λ(A), B]‖ ≤ (2‖A‖‖B‖ / C) (e^{‖Φ‖C|t|} − 1) D(X, Y)'
MUST_ABORT = [
    ('forward', 'comparison_face_sum_168_to_84', {'edits': [("        Kc[sg] = {'cmp': duhamel_coefficient(tv, U, 168, phi_abs, Cc),",
                                                              "        Kc[sg] = {'cmp': duhamel_coefficient(tv, U, 84, phi_abs, Cc),")]},
     'failed check comparison_bound_all_N'),
    ('forward', 'cauchy_face_sum_392_to_196', {'edits': [("                  'c1': duhamel_coefficient(tv, U, 392, phi_abs, Cc)}",
                                                           "                  'c1': duhamel_coefficient(tv, U, 196, phi_abs, Cc)}")]},
     'failed check within_family_cauchy_and_limits'),
    ('forward', 'lr_time_integral_factor_2_dropped', {'edits': [("    return 2 * phi_F * U * U / (1 - x / 3)", "    return phi_F * U * U / (1 - x / 3)")]},
     'failed check comparison_bound_all_N'),
    ('forward', 'contract_byte_edit_no_rehash', {'contract_edit': TARGET_ANCHOR}, 'contract snapshot bytes differ'),
    ('forward', 'contract_target_rehashed_9e-11', {'contract_edit': TARGET_ANCHOR, 'rehash': True}, 'failed check contract_snapshot_sha256'),
    ('forward', 'undeclared_input_reverse_report', {'extra_input': 'research/round33/reverse/ba2/report.md'}, 'failed check reverse_premise_isolation'),
    ('forward', 'report_forbidden_phrase', {'report_append': '\nThe thermodynamic limit of the dynamics exists.\n'},
     'affirmative forbidden phrasing in report.md'),
    ('forward', 'report_quote_51_paraphrased', {'report_edits': [(Q51_ANCHOR, Q51_PARA)]}, 'verbatim quotation missing from report: 51'),
    ('forward', 'report_template_removed', {'report_edits': [('mandatory_sentence_template_placeholder', '')]}, 'failed check mandatory_sentence_verbatim_once'),
    ('reverse', 'E_up_quadratic_term_dropped', {'edits': [("    return 1 + x / 3 + x * x / (12 * (1 - x / 5))", "    return 1 + x / 3")]},
     'check failed: item3_duhamel_comparison_inner_F2'),
    ('reverse', 'geometry_coefficient_168_to_84', {'edits': [("'dist_e_z': 'N-1', 'dist_0': 'N', 'geometry_coefficient': '168'}",
                                                               "'dist_e_z': 'N-1', 'dist_0': 'N', 'geometry_coefficient': '84'}")]},
     'geometry coefficient 3*28*2=168'),
    ('reverse', 'F2_per_site_face_sum_to_7', {'edits': [("per_site_per_tau='49/3'", "per_site_per_tau='7'")]},
     'per-site source sum must be J=28|tau| (F1) or 49|tau|/3 (F2)'),
    ('reverse', 'tail_coefficient_8_to_4', {'edits': [("'incoming_included': True, 'per_site_per_tau': '28', 'tail_coefficient': '8', 'rate': '1/(N-1)'}",
                                                        "'incoming_included': True, 'per_site_per_tau': '28', 'tail_coefficient': '4', 'rate': '1/(N-1)'}")]},
     'polynomial tail: 4/N+4/(N-1)<=8/(N-1)'),
    ('reverse', 'contract_byte_edit_no_rehash', {'contract_edit': TARGET_ANCHOR}, 'contract snapshot hash differs from the bound constant'),
    ('reverse', 'contract_target_rehashed_9e-11', {'contract_edit': TARGET_ANCHOR, 'rehash': True}, 'preregistered target values'),
    ('reverse', 'skeptic_triage_added_to_inputs', {'extra_input': 'research/round33/skeptic/triage.md'},
     'forbidden premise in reverse inputs: research/round33/skeptic/triage.md'),
    ('reverse', 'forward_report_added_to_inputs', {'extra_input': 'research/round33/forward/ba2/report.md'},
     'forbidden premise in reverse inputs: research/round33/forward/ba2/report.md'),
    ('reverse', 'report_forbidden_phrase', {'report_append': '\nThe thermodynamic limit of the dynamics exists.\n'}, 'affirmative forbidden phrasing'),
    ('reverse', 'report_quote_51_paraphrased', {'report_edits': [(Q51_ANCHOR, Q51_PARA)]}, 'Nachtergaele-Sims passage not quoted verbatim'),
]
SILENT = [
    ('forward', 'retained_triangle_coefficient_tripled', {'edits': [("    triangle = 2 * K['c1']", "    triangle = 3 * K['c1']")]},
     'retained triangle coefficient differs'),
    ('forward', 'b_N_preview_shape_5N', {'edits': [("    b_of_N = {N: K['cmp'] * Q(5 * N + 1, N ** 3) for N in range(2, 11)}",
                                                     "    b_of_N = {N: K['cmp'] * Q(5 * N, N ** 3) for N in range(2, 11)}")]},
     'b(N) all-size preview differs'),
    ('reverse', 'labelled_sharper_value_halved', {'edits': [("        s = lr_prefactor(1323 * TAU, 224, U) * (TAU / 3) * enum[N]['exact_sum']",
                                                              "        s = lr_prefactor(1323 * TAU, 224, U) * (TAU / 3) * enum[N]['exact_sum'] / 2")]},
     'labelled sharper comparison value differs'),
    ('reverse', 'general_X_example_26_sites', {'edits': [("        genX[str(N)] = exact(base * 28 * N * (5 * N + 1) * 3 * 27 * F(N - 1))",
                                                           "        genX[str(N)] = exact(base * 28 * N * (5 * N + 1) * 3 * 26 * F(N - 1))")]},
     'general-X example differs'),
    ('reverse', 'triangle_bound_over_N', {'edits': [("    tri = {str(N): {'triangle_through_limits': exact((c1 + c2) / (N - 1)),",
                                                      "    tri = {str(N): {'triangle_through_limits': exact((c1 + c2) / N),")]},
     'triangle bound differs'),
]


# ------------------------------------------------------------ main computation
def run():
    raw = CONTRACT.read_bytes()
    con = json.loads(raw)
    pr = con['preregistration']
    need(sha(CONTRACT) == CONTRACT_SHA and con['status'] == 'frozen_before_production' and pr['target']['value'] == '6x10^-11 and 2.5x10^-10',
         'contract_sha256_and_targets', contract_sha256=CONTRACT_SHA)
    template = pr['mandatory_sentence_template']

    # ---- the pre-comparison package is unchanged and replays byte for byte
    fz = json.loads(PRE_FREEZE.read_text())
    unchanged = fz['contract_sha256'] == CONTRACT_SHA and all(sha(ROOT / n) == d for n, d in fz['files'].items())
    pre_bytes = PRE_RESULTS.read_bytes()
    pre_replay, _ = replay(HERE / 'ba2_check.py', bool(sys.flags.optimize))
    need(unchanged and pre_replay == {'results.json': hashlib.sha256(pre_bytes).hexdigest()} and fz['stage'] == 'pre_comparison',
         'pre_comparison_package_unchanged_and_replayed', freeze_record=PRE_FREEZE.relative_to(ROOT).as_posix(),
         results_sha256=hashlib.sha256(pre_bytes).hexdigest(), files=len(fz['files']))
    prer = json.loads(pre_bytes)

    # ---- closures, inventories, snapshots, recorded check.py hashes, frozen artifacts
    rows = {}
    for side in ('forward', 'reverse'):
        ok, inputs, declared, snaps, n_files = verify_closure(side, con)
        frozen_ok = all(sha(SIDES[side] / rel) == d for rel, d in FROZEN[side].items())
        res = json.loads((SIDES[side] / 'output/results.json').read_text())
        rec_sha = res['check_py_sha256_recorded_before_evaluation']
        rows[side] = {'closure_files': n_files, 'inputs': len(inputs), 'inventory_equals_declared': inputs == declared,
                      'snapshots_byte_identical': snaps, 'check_py_sha256_recorded': rec_sha == FROZEN[side]['check.py'],
                      'frozen_artifacts_pinned': frozen_ok}
        if not (ok and inputs == declared and snaps and frozen_ok and rec_sha == FROZEN[side]['check.py'] and len(inputs) == 29
                and n_files == 33):
            raise ReviewFailure('closure or inventory failed: ' + side)
    rev_inputs = verify_closure('reverse', con)[1]
    need(not any(p.startswith(FORBIDDEN_IN_REVERSE) for p in rev_inputs) and rows['forward']['inputs'] == rows['reverse']['inputs'] == 29,
         'closures_inventories_and_reverse_isolation', closures=rows,
         reverse_inputs='AGENTS.md + contract + 27 shared premises exactly; no skeptic, lens, deliberation, plan or forward file')

    # ---- normal and -O replays of both producers
    receipts = []
    for side in ('forward', 'reverse'):
        for opt in (False, True):
            outputs, stdout = replay(SIDES[side] / 'check.py', opt)
            frozen = {rel[len('output/'):]: d for rel, d in FROZEN[side].items() if rel.startswith('output/')}
            same = outputs == frozen
            receipts.append({'direction': side, 'mode': 'optimized' if opt else 'normal', 'byte_identical_to_frozen_output': same,
                             'outputs': outputs, 'stdout': stdout})
            if not same:
                raise ReviewFailure('replay differs: %s %s' % (side, opt))
    need(True, 'producer_replays_byte_identical', runs=len(receipts), receipts=receipts)

    # ---- exact headline comparison with the skeptic's derivation
    ref = reference()
    fres = json.loads((FWD / 'output/results.json').read_text())
    rres = json.loads((REV / 'output/results.json').read_text())
    need(validate_producer_values(fres, 'forward', ref) and validate_producer_values(rres, 'reverse', ref),
         'producer_values_validated_exactly')
    cl, sh, eup = ref['closed'], ref['sharp'], ref['eup']
    t_cmp, t_cau = F(6, 10 ** 11), F(25, 10 ** 11)
    pre_cmp = prer['comparison']
    pre_closed_ok = (F(pre_cmp['forward_inner_F1']['closed']) == cl['fwd_cmp'] and F(pre_cmp['reverse_inner_F2']['closed']) == cl['rev_cmp']
                     and F(prer['cauchy']['F1_face_charged_Phi']['closed']) == cl['c1_face']
                     and F(prer['cauchy']['F1_star_charged_Phi']['closed']) == cl['c1_star']
                     and F(prer['cauchy']['F2_face_charged_Phiprime']['closed']) == cl['c2_face'])
    need(pre_closed_ok and sh['fwd_cmp'][1] <= cl['fwd_cmp'] <= t_cmp and sh['c1_face'][1] <= cl['c1_face'] <= t_cau
         and cl['fwd_c2'] <= t_cau and cl['fwd_c2'] >= sh['c1_face'][0] + F(11, 8) * sh['fwd_cmp'][0]
         and cl['fwd_c2'] == F(117747, 1245766400000000) and cl['fwd_cmp'] == F(3969, 155720800000000)
         and cl['c1_face'] == F(9261, 155720800000000),
         'forward_headlines_equal_skeptic_closed_forms',
         K_cmp={'forward': q(cl['fwd_cmp']), 'skeptic_pre_closed': pre_cmp['forward_inner_F1']['closed'], 'equal': True},
         K_c1={'forward_face_charged': q(cl['c1_face']), 'skeptic_pre_closed_face_charged': prer['cauchy']['F1_face_charged_Phi']['closed']},
         K_c2={'forward': q(cl['fwd_c2']), 'composition': 'K_c1 (face) + (11/8) K_cmp, both skeptic closed forms; one F1-inner Duhamel '
               'F2(M) against F1(N) plus the comparison at N; (5N+1)(N-1)N^-3 at most 11/8'},
         margins={'K_cmp': preview(t_cmp / cl['fwd_cmp'], 6), 'K_c1': preview(t_cau / cl['c1_face'], 6), 'K_c2': preview(t_cau / cl['fwd_c2'], 6)})
    rev_rat = {'K_cmp': F(rres['headline']['comparison_coefficient']['exact']), 'c1': F(rres['headline']['cauchy_coefficient_F1']['exact']),
               'c2': F(rres['headline']['cauchy_coefficient_F2']['exact'])}
    bracket_ok = (sh['rev_cmp'][1] <= rev_rat['K_cmp'] <= cl['rev_cmp'] and sh['c1_star'][1] <= rev_rat['c1'] <= cl['c1_star']
                  and sh['c2_face'][1] <= rev_rat['c2'] <= cl['c2_face'])
    eup_valid = (ref['e2_sharp']['x_phi'][1] <= ref['eup_at_x']['x_phi'] <= 1 / (1 - X_PHI / 3)
                 and ref['e2_sharp']['x_phiprime'][1] <= ref['eup_at_x']['x_phiprime'] <= 1 / (1 - X_PHIP / 3)
                 and all(F(24) * 5 ** (j - 2) <= factorial(j + 2) for j in range(2, 60)))
    need(bracket_ok and eup_valid and rev_rat['K_cmp'] == F(452554889222515527, 30481402343750000000000000000)
         and all(v <= (t_cmp if k == 'K_cmp' else t_cau) for k, v in rev_rat.items()),
         'reverse_headlines_reconciled_with_skeptic',
         K_cmp={'reverse': q(rev_rat['K_cmp']), 'skeptic_closed': q(cl['rev_cmp']), 'skeptic_sharp_upper': q(pre.rup(sh['rev_cmp'][1])),
                'relative_excess_of_closed_over_reverse': preview(cl['rev_cmp'] / rev_rat['K_cmp'] - 1, 6),
                'relative_excess_of_reverse_over_sharp': preview(rev_rat['K_cmp'] / sh['rev_cmp'][1] - 1, 6)},
         c1={'reverse': q(rev_rat['c1']), 'skeptic_closed_star': q(cl['c1_star'])},
         c2={'reverse': q(rev_rat['c2']), 'skeptic_closed_face': q(cl['c2_face'])},
         E_up={'x_phiprime': q(ref['eup_at_x']['x_phiprime']), 'x_phi': q(ref['eup_at_x']['x_phi'])},
         reconciliation='both are directed upper bounds of the same quantity 2||Phi||U^2 E(x)/x^2-type integral: the reverse bounds the '
                        'remainder e^x-1-x by (x^2/2)(1+x/3+x^2/(12(1-x/5))) ((j+2)! at least 24*5^(j-2)), the skeptic closed form by '
                        '(x^2/2)/(1-x/3) (k! at least 2*3^(k-2)); sharp enclosure <= reverse <= closed; the difference is in the fourth '
                        'order of the exponential remainder, relative size about 1e-6 of the constant',
         margins={k: preview((t_cmp if k == 'K_cmp' else t_cau) / v, 6) for k, v in sorted(rev_rat.items())})
    fr = check_map(fres)['tau_scaling_exponent']['ratios']
    rsc = rres['scaling']
    ratios = {'forward': F(fr['cmp']['exact']), 'reverse_cmp_and_F2': F(rsc['comparison_coefficient']['exact']),
              'reverse_F1': F(rsc['cauchy_coefficient_F1']['exact'])}
    need(all(9500 <= v <= 10500 for v in ratios.values()) and all(9900 <= v <= 10100 for v in ratios.values())
         and ratios['forward'] == F(1953058850, 194651),
         'tau_scaling_ratios_in_preregistered_bracket', ratios={k: q(v) for k, v in ratios.items()},
         previews={k: preview(v, 9) for k, v in ratios.items()},
         stale_bracket_note='every producer ratio also lies in the stale [9900,10100] of the control semantics (defect D1 did not bite)')

    # ---- extra faces, all-size formula, distance sums, padding
    fam = ref['families']
    rcounts = check_map(rres)['item2_extra_faces_enumerated_and_all_size']['counts_N2_to_6']
    counts_ok = all(rcounts[str(n)] == {'F1': fam[n]['F1'], 'F2': fam[n]['F2'], 'extra': fam[n]['extra']} for n in (2, 3, 4, 5)) and \
        rcounts['6'] == {'F1': 168 * 216, 'F2': 28 * 6 * 13 * 19, 'extra': 28 * 6 * 31}
    need(counts_ok and all(fam[n]['extra'] == 28 * n * (5 * n + 1) and fam[n]['incidences'] == 28 * n * (11 * n + 2)
                           and fam[n]['min_ez'] == n - 1 and fam[n]['min_0'] == n for n in fam),
         'extra_face_enumeration_and_all_size_formula',
         skeptic={str(n): {k: (q(v) if isinstance(v, F) else v) for k, v in fam[n].items()} for n in sorted(fam)},
         forward_enumerated='N=2,3,4 identical (F1, F2, extra, incidences 28N(11N+2), distances, exact distance sums)',
         reverse_enumerated='N=2,3 identical (count, distances, 60/126 partial groups, 75/147 padding sites); counts to N=6 match 168N^3 and 28N(2N+1)(3N+1)',
         all_size='per-anchor classes 17/13/5 (one coordinate equal to N), 10/3/1 (two), 0 (corner): 140N^2+28N')
    fpad = check_map(fres)['padding_onsite_terms_factor_out']
    rpad = check_map(rres)['item2_padding_factorization']
    hin = pre.mat([[1, F(1, 2)], [F(1, 2), 0]])
    a_op = pre.mat([[0, 1], [1, 0]])
    hpad = pre.mat([[0, 0, 0], [0, 1, 0], [0, 0, 2]])
    big = pre.madd(pre.kron(hin, pre.eye(3)), pre.kron(pre.eye(2), hpad))
    xb, xs, pad_ok = pre.kron(a_op, pre.eye(3)), a_op, True
    for _ in range(7):
        xb, xs = pre.comm(big, xb), pre.comm(hin, xs)
        pad_ok = pad_ok and xb == pre.kron(xs, pre.eye(3))
    need(pad_ok and fpad['passed'] and rpad['passed'] and rpad['padding_sites'] == {'2': 75, '3': 147}
         and '75 at N=2, 147 at N=3' in fpad['padding_sites'] and fam[2]['padding'] == 75 and fam[3]['padding'] == 147,
         'padding_factorization_both_routes', forward_fixture=fpad['fixture'], reverse_statement=rpad['statement'],
         skeptic_fixture='ad^k_{H_in (x) 1 + 1 (x) h_pad}(A (x) 1) = (ad^k_{H_in} A) (x) 1, k=1..7 (exact)')

    # ---- Nachtergaele-Sims passages byte for byte
    ns = NS_EXCERPT.read_text()
    ns_nobold = ns.replace('**', '')
    part_b = ns.split('## Part B')[1]
    ftext = (FWD / 'report.md').read_text()
    rtext = (REV / 'report.md').read_text()
    fq, f47 = forward_quote_lines(ftext)
    edited_heading = 'Theorem 4.1 (section title omitted). '
    f_verbatim, f_edited = [], []
    for ln in fq:
        if ln.startswith(edited_heading):
            f_edited.append(ln[:len(edited_heading)])
            if ln[len(edited_heading):] not in ns:
                raise ReviewFailure('forward Theorem 4.1 statement not verbatim')
        elif ln in ns:
            f_verbatim.append(ln)
        elif ln in ns_nobold:
            f_edited.append('markdown bold markers removed: ' + ln[:40])
        else:
            raise ReviewFailure('forward quotation not in the excerpt: ' + ln[:60])
    f47_ok = all(ln in part_b for ln in f47)
    rq, r47 = reverse_quote_lines(rtext)
    r_ok = all(ln in ns for ln in rq) and all(ln in part_b for ln in r47)
    need(f47_ok and r_ok and Q51_ANCHOR in ftext and Q51_ANCHOR in rtext and 'Setting (Section 3).' in rtext
         and ftext.count('On the existence of the thermodynamic limit') == 0 and rtext.count('On the existence of the thermodynamic limit') == 0,
         'ns_passages_match_committed_excerpt',
         forward={'lines': len(fq), 'verbatim': len(f_verbatim), 'edited_heading_or_markdown': f_edited, 'part_b_47_lines': len(f47)},
         reverse={'lines': len(rq), 'verbatim': len(rq), 'part_b_47_lines': len(r47)},
         finding='the forward block is described as copied byte for byte; two headings differ from the excerpt bytes (the bold markers '
                 'of Theorem 3.1 and the Theorem 4.1 parenthetical replaced by "(section title omitted)"); every statement sentence '
                 'and equation is verbatim; neither report quotes the section title')

    # ---- gate fields, claims, template span, round phrase-scan tool
    gf = pr['gate_fields_required']
    need(fres['gate_fields'] == gf and rres['gate_fields'] == gf, 'gate_fields_equal_contract_both', gate_fields=gf)
    spans = {}
    for side, text in (('forward', ftext), ('reverse', rtext)):
        lines = [ln for ln in text.splitlines() if template in ln]
        spans[side] = {'occurrences': text.count(template), 'normalized_occurrences': normalize(text).count(normalize(template)),
                       'single_line': len(lines) == 1}
    need(all(v == {'occurrences': 1, 'normalized_occurrences': 1, 'single_line': True} for v in spans.values())
         and fres['mandatory_sentence'] == template and rres['mandatory_sentence_template'] == template,
         'mandatory_sentence_one_unbroken_span', spans=spans)
    need(sha(PHRASE_SCAN) == PHRASE_SCAN_SHA, 'phrase_scan_tool_pinned', tool=PHRASE_SCAN.relative_to(ROOT).as_posix(), sha256=PHRASE_SCAN_SHA)
    scan = {}
    for side in ('forward', 'reverse'):
        done = subprocess.run([sys.executable, '-B', str(PHRASE_SCAN), str(CONTRACT), str(SIDES[side] / 'report.md')],
                              capture_output=True, text=True, cwd=str(ROOT))
        out = json.loads(done.stdout)
        scan[side] = {'exit': done.returncode, 'affirmative_hits': sum(len(v) for v in out.values())}
    need(all(v == {'exit': 0, 'affirmative_hits': 0} for v in scan.values()), 'round_phrase_scan_tool_on_both_reports', scan=scan)

    # ---- O6 rerun and identification on the local algebra
    fcm, rcm = check_map(fres), check_map(rres)
    f_o6 = fcm['f2_limit_dynamics_equals_f1']['o6_rerun']
    r_o6 = rres['o6']
    need(sorted(f_o6) == ['gns_unitaries', 'nonnegative_generator', 'physical_sector', 'stationarity', 'strong_continuity']
         and fcm['o6_limit_state_properties_rerun']['passed']
         and all(v == {'status': 'rerun', 'subsequence': 'F2 own subsequence', 'dynamics': 'AQ1 T_theta, identified with the F2 limit'}
                 for v in r_o6.values()) and len(r_o6) == 4
         and rres['identification']['general_local_X'] is True
         and 'For a general local `A` in `B(H_X)`' in ftext and 'on the whole quasi-local algebra' in ftext
         and 'For a general local `A in A_X`' in rtext and "F2's own subsequences" in ftext and "**F2's own subsequence**" in rtext,
         'o6_rerun_and_local_algebra_identification_both',
         forward_steps=sorted(f_o6), reverse_steps=sorted(r_o6),
         stationarity={'forward': '|omega(T_u A)-omega(A)| <= 2 eps_n with eps_n=sup||T_u(A)-T^{F2,n}_u(A)||',
                       'reverse': '|omega(T_theta A)-omega(A)| <= 2c2/(L-1)'},
         identification='both routes identify the F2 limit with T_theta on every local observable (R replaced by a finite X), then on the '
                        'quasi-local algebra; skeptic reading R7 met')

    # ---- labelled sharp (48) supremum observation
    need('567|tau|' in fcm['missing_incoming_stars']['labelled_observation']
         and rcm['item1_interaction_norms_Phi_and_Phi_prime']['labelled_exact_48_norms_not_used']['owner_set_per_tau'] == '108'
         and prer['constants']['sharp_labelled'] == {'phi': '567', 'phiprime': '108'},
         'sharp_48_supremum_observation_agrees', whole_star='567|tau| (admitted 2268|tau|)', owner_set="108|tau| (admitted 1323|tau|)",
         use='labelled observation only; no constant, target or gate value uses it')
    need(fres['controls_with_damaging_mutations'] == 35 and fres['rejected_mutation_total'] == 116
         and sorted(rres['controls_with_damaging_mutations']) == sorted(con['controls']) and rres['damaging_mutations_rejected'] == 149
         and rres['controls_not_implementable_as_mutations'] == [],
         'producer_control_coverage', forward={'controls': 35, 'rejections': 116}, reverse={'controls': 35, 'rejections': 149})

    # ---- mutation harness
    base = {s: mutated_run(s) for s in ('forward', 'reverse')}
    need(all(base[s][0] == 0 and base[s][1] == (SIDES[s] / 'output/results.json').read_bytes() for s in base),
         'mutation_harness_unmutated_copies_reproduce_frozen_results')
    mreceipts = []
    for side, table in (('forward', FWD_WEAK), ('reverse', REV_WEAK)):
        ids = [row[0] for row in table]
        if sorted(ids) != sorted(con['controls']):
            raise ReviewFailure('weakening table does not cover the 35 controls: ' + side)
        for cid, edits, label in table:
            code, results, last = mutated_run(side, edits=edits)
            ok = code != 0 and results is None and last.endswith('damaging mutation accepted: ' + label)
            need(ok, 'control_weakening_%s_%s' % (side, cid), last_error_line=last)
            mreceipts.append({'direction': side, 'kind': 'control_validator_weakening', 'control': cid, 'producer_aborted': True,
                              'accepted_mutation': label})
    template_line = template
    for side, label, spec, expect in MUST_ABORT:
        spec = dict(spec)
        if spec.get('report_edits') and spec['report_edits'][0][0] == 'mandatory_sentence_template_placeholder':
            spec['report_edits'] = [(template_line, '')]
        code, results, last = mutated_run(side, **spec)
        need(code != 0 and results is None and expect in last, 'mutation_aborts_%s_%s' % (side, label), last_error_line=last)
        mreceipts.append({'direction': side, 'kind': 'must_abort', 'mutation': label, 'producer_aborted': True})
    for side, label, spec, expect in SILENT:
        code, results, last = mutated_run(side, **spec)
        caught, reason = False, ''
        if code == 0 and results is not None:
            try:
                validate_producer_values(json.loads(results), side, ref)
            except Rejected as exc:
                caught, reason = True, str(exc)
        need(code == 0 and results is not None and caught and expect in reason
             and results != (SIDES[side] / 'output/results.json').read_bytes(),
             'silent_edit_caught_by_review_%s_%s' % (side, label), producer_exit=code, review_rejection=reason)
        mreceipts.append({'direction': side, 'kind': 'silent_edit', 'mutation': label, 'producer_aborted': False,
                          'caught_by_skeptic_value_validator': True, 'reason': reason})

    exact = {
        'forward': {'K_cmp': q(cl['fwd_cmp']), 'K_c1': q(cl['c1_face']), 'K_c2': q(cl['fwd_c2']),
                    'ratio_tau_over_100': q(ratios['forward']), 'retained_triangle_2K_c1': q(2 * cl['c1_face'])},
        'reverse': {'K_cmp': q(rev_rat['K_cmp']), 'c1': q(rev_rat['c1']), 'c2': q(rev_rat['c2']),
                    'ratio_cmp_and_c2': q(ratios['reverse_cmp_and_F2']), 'ratio_c1': q(ratios['reverse_F1'])},
        'skeptic_closed': {k: q(v) for k, v in sorted(cl.items())},
        'skeptic_sharp_upper': {k: q(pre.rup(v[1])) for k, v in sorted(sh.items())},
        'targets': {'comparison': q(t_cmp), 'cauchy': q(t_cau)},
        'exact_distance_sums': {str(n): q(fam[n]['S']) for n in sorted(fam)},
    }
    previews = {'forward_K_cmp': preview(cl['fwd_cmp']), 'forward_K_c1': preview(cl['c1_face']), 'forward_K_c2': preview(cl['fwd_c2']),
                'reverse_K_cmp': preview(rev_rat['K_cmp']), 'reverse_c1': preview(rev_rat['c1']), 'reverse_c2': preview(rev_rat['c2']),
                'note': 'decimal previews only; every Boolean above was decided on exact rationals'}
    counts = {'weakenings': sum(1 for r in mreceipts if r['kind'] == 'control_validator_weakening'),
              'must_abort': sum(1 for r in mreceipts if r['kind'] == 'must_abort'),
              'silent': sum(1 for r in mreceipts if r['kind'] == 'silent_edit'), 'unmutated': 2}
    return {
        'schema': 'hnm-r33-skeptic-postcomparison-v1', 'loop': 'BA2', 'stage': 'post_comparison',
        'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'model-agent skeptic with correlated ancestry; not human peer review or formal verification',
        'contract_sha256': CONTRACT_SHA, 'pre_comparison_module_sha256': sha(HERE / 'ba2_check.py'),
        'frozen_producer_artifacts': FROZEN, 'exact': exact, 'previews': previews, 'mutation_counts': counts,
        'mutation_receipts': mreceipts, 'passed': True, 'checks': CHECKS, 'checks_count': len(CHECKS),
    }


def main():
    ap = argparse.ArgumentParser(description='BA2 post-comparison skeptic checks')
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
    print(json.dumps({'loop': 'BA2', 'stage': 'post_comparison', 'checks': result['checks_count'],
                      'mutations': result['mutation_counts'], 'forward_K_cmp': result['previews']['forward_K_cmp'],
                      'reverse_K_cmp': result['previews']['reverse_K_cmp']}, sort_keys=True))


if __name__ == '__main__':
    main()
