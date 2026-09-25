#!/usr/bin/env python3
"""BB2 post-comparison skeptic checks (stage 1: producers; stage 2: the discharge against the BB1 gate).

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated ancestry (same model family as the advisor,
the lenses and both producers; the frozen BB2 targets, brackets and conditional semantics came from the skeptic's own BB
pre-freeze review); not human peer review or formal verification.

Stage 1 adds to the frozen pre-comparison package (bb2_check.py, committed at 8921539 before either producer was read):
  * integrity: both contract hashes; the unchanged pre-comparison package and a byte replay of bb2_check.py; both freeze
    closures file by file (42 files each); both premise inventories on the real snapshots (38 files each, equal to the
    contract-derived inventory and to the inventory recorded before production, byte-identical to the repository);
    normal and -O replays of both producers reproducing output/ byte for byte; the frozen artifacts pinned;
  * every producer headline recomputed independently (never from a producer value) and compared exactly: C', c'_site and
    the secondary pair under each assembly, C_dyn from the pinned BA2 gate values (forward 2K_F1+K_cmp/4 with its lemma
    (5N+1)(r_N-1)<=N^3/4 re-proved by the identity N^3-10N^2+28N+6 = N(N-5)^2+3N+6; reverse 2K per family), the item-5
    values, the reverse K_reg, K_R, K5, the item-4 rows and the union fallback, the tau/100 ratios;
  * the item-5 rate range certified independently (a convex-derivative envelope, not the reverse's blocks) on
    5<=N<=14000, and vacuity certified by a logarithmic comparison with a series enclosure of ln 2 at N=14419, 14420 and
    for every N>=14421 (monotone lower envelope); the forward's unqualified O(1/N) statement is recorded as an overclaim;
  * text: the round phrase rule (mirrored) on both reports, the mandatory sentence once as one unbroken line in each, every
    quoted Nachtergaele-Sims block line a verbatim substring of the committed excerpt, gate-field blocks before and after
    the discharge;
  * source-edit runs on temporary copies outside the checkout: one validator weakening per contract control and producer
    (68 runs; the producer checker must abort with 'damaging mutation accepted: <label>'), must-abort edits, unmutated
    copies that reproduce output/ byte for byte, and silent edits that the producer checkers do not pin, which this
    review's value validator must catch.
Stage 2 (the BB1 gate exists: sha256 18141fea..., commit eef57b4, accepted_within_scope) runs by default and adds:
  * bb2-bb1-admission.json, the skeptic's transcription of the constants the BB1 gate admits, pinned by sha256; every
    constant, bound shape, q, comparison label (also equal to the BB1 contract list), sign and regime must be a verbatim
    substring of the gate text, and every cell equals the BB1 review's admitted_values table (bb1.json, pinned);
  * the pre-registered discharge protocol (bb2_check.discharge) on the admitted constants, on the labelled secondary pair
    and on the self-contained iterated_split values; each producer's own hypothesis map (forward H1-H4, reverse B3-B5 with
    its item references) discharged cell by cell (comparison x form x regime x sign), cross-checked against the Jung
    assistant-2 table (pinned);
  * the constants at the hypothesis values (bound by the gate) beside the constants re-evaluated at the admitted values
    (labelled); the item-5 range, the bracket below 2 on 14001<=N<=14418 (fine logarithms) and at least 2 from N=14419 for
    both constant sets; the gate fields from the discharge engine; 18 in-memory damaging edits of the gate and admission.

Standard library only; exact Fractions decide every Boolean; failures are explicit exceptions (never assert), so the
output bytes match under python -O.

Usage: python3 -B research/round33/skeptic/bb2_postreview_check.py --output /abs/fresh/dir
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
import bb2_check as pre  # noqa: E402  (the skeptic's own frozen pre-comparison module)

ROOT = HERE.parents[2]
R33 = ROOT / 'research/round33'
CONTRACT = R33 / 'contracts/bb2.json'
CONTRACT_SHA = 'ed5c0b24b16b19f0db2c16a437ee37608552e1a1cf0629494792aa877d95ad35'
BB1_CONTRACT = R33 / 'contracts/bb1.json'
BB1_CONTRACT_SHA = '30400d2eeea733a49ef66e0ed7ed735aa8d603581948650e6ef6ac61f8e55018'
NS_EXCERPT = R33 / 'sources/nachtergaele-sims-1410.8174v1.md'
BA2_GATE = R33 / 'advisor/ba2-gate.json'
FWD = R33 / 'forward/bb2'
REV = R33 / 'reverse/bb2'
SIDES = {'forward': FWD, 'reverse': REV}
PRE_SCRIPT = HERE / 'bb2_check.py'
PRE_RESULTS = HERE / 'bb2-independent/results.json'
PRE_FREEZE = HERE / 'bb2-independent-freeze.json'
FROZEN = {  # frozen producer artifacts (sha256 at review time; commits d05efda forward, 17c0ecf reverse)
    'forward': {'output/results.json': 'b87fea90d8b12aff3924039f31f89893c9979bfb509635c281a717bf3b93753a',
                'output/source-manifest.json': 'b7aedea826a4a61faa4a5e504e2350ab78ff9b40b01ea31eff474ada142636b1'},
    'reverse': {'output/results.json': '51613bda49c2b7333ab1e5374329fca9b5b2d3f0e7591262c234c640db0d0bbe',
                'output/source-manifest.json': 'dc4da2b7b14e002f586214d81f43e08f7ef6ee8b2b797d08f3341a317d8eeb02'},
}
COMMITS = {  # recorded from git at review time (not read at run time)
    'skeptic_pre_comparison': {'commit': '8921539', 'time': '2026-09-25T00:14:56Z'},
    'forward_producer': {'commit': 'd05efda', 'time': '2026-09-25T00:10:26Z'},
    'reverse_producer': {'commit': '17c0ecf', 'time': '2026-09-25T00:18:36Z'},
    'plan_d8_repair': {'commit': '43eb922', 'note': 'plan history BB1/BB2 freeze entry with the plan sha256 (skeptic defect D8)'},
    'skeptic_post_comparison_stage_1': {'commit': 'e2a9ed2'},
    'bb1_gate': {'commit': 'eef57b4', 'note': 'the BB1 gate; stage 2 read it only after this commit'},
}
TEMPLATE_KEY = 'mandatory_sentence_template'


class ReviewFailure(RuntimeError):
    """A post-review check failed."""


class Rejected(Exception):
    """The skeptic's value validator refused a producer results file."""


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
    return str(F(x))


def preview(x, digits=12):
    return format(float(x), '.%de' % digits)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rat(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise Rejected('non-exact value in producer results: ' + repr(value))
    if isinstance(value, dict) and 'exact' in value:
        value = value['exact']
    if isinstance(value, str) and re.fullmatch(r'-?\d+(/\d+)?', value):
        return F(value)
    if isinstance(value, int):
        return F(value)
    raise Rejected('malformed exact value: ' + repr(value))


# ------------------------------------------------------------ enclosures independent of both producers
def ln2_enclosure(n=140):
    """ln 2 = sum_{k>=1} 1/(k 2^k): partial sum (lower) and partial sum + 1/((n+1) 2^n) (upper)."""
    s = F(0)
    for k in range(1, n + 1):
        s += F(1, k * 2 ** k)
    return s, s + F(1, (n + 1) * 2 ** n)


E_UP_SK = F(27183, 10000)   # e < 27183/10000, certified below from the Taylor enclosure
E_LO_SK = F(2718, 1000)     # e > 2718/1000, certified below


def ln_lower_integer(y):
    """Largest integer m with E_UP_SK^m <= y (so ln y > m) for y >= 1."""
    m = 0
    while E_UP_SK ** (m + 1) <= y:
        m += 1
    return m


def ln_upper_integer(y):
    """Smallest integer m with E_LO_SK^m >= y (so ln y < m) for y >= 1."""
    m = 0
    while E_LO_SK ** m < y:
        m += 1
    return m


def r_N(n):
    return (n - 1) // 2


def region_value_upper(n, csp):
    """c'_site |Lambda_r| e^{|Lambda_r|/10^8} q^(N-r) with the skeptic's 30-term Taylor upper enclosure (|Lambda_r|<10^8)."""
    r = r_N(n)
    lam = (2 * r + 1) ** 3
    return csp * lam * pre.e_region_hi(lam) * F(1, 64) ** (n - r)


def vacuous_at(n, csp, l2):
    """Certify c'_site |Lambda_r| e^{|Lambda_r|/10^8} q^(N-r) >= 2 by logarithms: m + x - (N-r) 6 ln2_up >= ln2_up,
    with m < ln(c'_site |Lambda_r|) from E_UP_SK powers and x = |Lambda_r|/10^8 exact."""
    r = r_N(n)
    lam = (2 * r + 1) ** 3
    m = ln_lower_integer(csp * lam)
    return m + F(lam, 10 ** 8) - (n - r) * 6 * l2[1] >= l2[1]


def region_below_two(n, csp, l2):
    """Certify the region term < 2: ln(c'|Y|) < m (E_LO_SK powers), e^x <= e^{ceil x} <= E_UP_SK^{ceil x}, ln 64 >= 6 ln2_lo."""
    r = r_N(n)
    lam = (2 * r + 1) ** 3
    m = ln_upper_integer(csp * lam)
    # ln(region) < m + |Lambda_r|/10^8 - (N-r) 6 ln2_lo, and region < 2 follows from that bound being below ln2_lo
    return m + F(lam, 10 ** 8) - (n - r) * 6 * l2[0] < l2[0]


# ------------------------------------------------------------ independent reference values
def reference():
    con = json.loads(CONTRACT.read_bytes())
    tau = F(1, 10 ** 8)
    q_ = F(1, 64)
    Ch, ch = F(1, 250000), F(1, 500000)
    C2h, c2h = F(1, 20000), F(1, 40000)
    q2 = 151552 * tau
    ba2 = json.loads(BA2_GATE.read_text())['accepted']

    def fwd(L, t):
        return L * t * t / (1 - 338688 * t)

    def eup(y):
        return 1 + y / 3 + y * y / (12 * (1 - y / 5))

    def rev(L, v, t):
        return L * t * t * eup(v * t)
    K = {'cmp_fwd': fwd(254016, tau), 'cmp_rev': rev(148176, 592704, tau), 'c1_fwd': fwd(592704, tau),
         'c1_rev': rev(1016064, 1016064, tau), 'c2_fwd': fwd(941976, tau), 'c2_rev': rev(345744, 592704, tau)}
    for k, v in K.items():
        if q(v) not in ba2:
            raise ReviewFailure('BA2 gate value not found verbatim: ' + k)
    ref = {
        'q': q_, 'tau': tau, 'C_h': Ch, 'c_h': ch, 'C_2h': C2h, 'c_2h': c2h, 'q2': q2, 'K': K,
        'forward': {'C_prime': Ch / (1 - q_), 'c_site_prime': ch / (1 - q_), 'C_prime_2': C2h / (1 - q2),
                    'c_site_prime_2': c2h / (1 - q2), 'C_dyn_F1': 2 * K['c1_fwd'], 'C_dyn': 2 * K['c1_fwd'] + K['cmp_fwd'] / 4,
                    'C_dyn_ratio': (2 * fwd(592704, tau) + fwd(254016, tau) / 4) / (2 * fwd(592704, tau / 100) + fwd(254016, tau / 100) / 4)},
        'reverse': {'C_prime': Ch, 'c_site_prime': ch, 'C_prime_2': C2h, 'c_site_prime_2': c2h,
                    'C_dyn_F1': 2 * K['c1_fwd'], 'C_dyn_F2': 2 * K['c2_rev'],
                    'C_dyn_F1_ratio': fwd(592704, tau) / fwd(592704, tau / 100),
                    'C_dyn_F2_ratio': rev(345744, 592704, tau) / rev(345744, 592704, tau / 100)},
        'targets': {'C_prime': F(1, 100000), 'c_site_prime': F(1, 200000), 'C_dyn': F(1, 2000000000), 'C_prime_2': F(1, 8000)},
        'template': con['preregistration'][TEMPLATE_KEY],
        'forbidden': pre.ROUND_FORBIDDEN + list(con['preregistration']['forbidden_phrasings']),
        'gate_fields': con['preregistration']['gate_fields_required'],
        'secondary_ratio_telescoped': (C2h / (1 - q2)) / (C2h / (1 - q2 / 100)),
    }
    return ref


def forward_bracket(n, cdyn, csp, cp):
    """The forward's own evaluation form: e^x <= 1/(1-x) (valid for x<1)."""
    r = r_N(n)
    lam = (2 * r + 1) ** 3
    x = F(lam, 10 ** 8)
    if not x < 1:
        raise ReviewFailure('forward enclosure outside its radius')
    return cdyn / (r - 1) + csp * lam * (1 / (1 - x)) * F(1, 64) ** (n - r) + 2 * cp * F(1, 64) ** (n - 1)


def reverse_region(n, csp):
    """The reverse's own evaluation form: E_UP^floor(x) times a 24-term series upper bound (x<1 here), on the 10^-40 grid."""
    r = r_N(n)
    lam = (2 * r + 1) ** 3
    x = F(lam, 10 ** 8)
    partial, power, fact = F(0), F(1), 1
    for k in range(25):
        if k > 0:
            fact *= k
        partial += power / fact
        power *= x
    fact25 = fact * 25
    upper = partial + power / fact25 / (1 - x / 26)
    val = csp * lam * upper * F(1, 64) ** (n - r)
    den = 10 ** 40
    return F(-((-val.numerator * den) // val.denominator), den), val


# ------------------------------------------------------------ the skeptic's value validator (catches silent edits)
def validate_producer_values(res, direction, ref):
    h = res['headline']
    if direction == 'forward':
        fw = ref['forward']
        pairs = [('C_prime', h['C_prime']['value'], fw['C_prime']), ('c_site_prime', h['c_site_prime']['value'], fw['c_site_prime']),
                 ('C_dyn', h['C_dyn']['value'], fw['C_dyn']), ('C_dyn_F1', h['C_dyn']['F1_value'], fw['C_dyn_F1']),
                 ('C_prime_2', h['secondary']['C_prime_2'], fw['C_prime_2']),
                 ('c_site_prime_2', h['secondary']['c_site_prime_2'], fw['c_site_prime_2']),
                 ('item4_constant', h['item4']['constant'], ref['C_h']),
                 ('ba2_K_F1', h['C_dyn']['ba2_gate_values']['K_F1'], ref['K']['c1_fwd']),
                 ('ba2_K_cmp', h['C_dyn']['ba2_gate_values']['K_cmp'], ref['K']['cmp_fwd']),
                 ('item5_sum_N5', h['item5_sums']['N5'], forward_bracket(5, fw['C_dyn'], fw['c_site_prime'], fw['C_prime'])),
                 ('item5_sum_N10', h['item5_sums']['N10'], forward_bracket(10, fw['C_dyn'], fw['c_site_prime'], fw['C_prime']))]
        checks = {c['id']: c for c in res['checks']}
        f1s = checks['item5_rate_and_sums']['sums_F1']
        pairs += [('item5_F1_sum_N5', f1s['5']['total_exact'], forward_bracket(5, fw['C_dyn_F1'], fw['c_site_prime'], fw['C_prime'])),
                  ('item5_F1_sum_N10', f1s['10']['total_exact'], forward_bracket(10, fw['C_dyn_F1'], fw['c_site_prime'], fw['C_prime']))]
        rat_tab = checks['tau_scaling_exponent']['ratios']
        pairs += [('ratio_C_dyn', rat_tab['C_dyn']['exact'], fw['C_dyn_ratio']),
                  ('ratio_secondary', rat_tab['secondary_C_prime']['exact'], ref['secondary_ratio_telescoped']),
                  ('ratio_C_prime', rat_tab['C_prime']['exact'], F(1))]
    else:
        rv = ref['reverse']
        pairs = [('C_prime', h['C_prime']['exact'], rv['C_prime']), ('c_site_prime', h['c_site_prime']['exact'], rv['c_site_prime']),
                 ('C_dyn_F1', h['C_dyn']['F1']['exact'], rv['C_dyn_F1']), ('C_dyn_F2', h['C_dyn']['F2']['exact'], rv['C_dyn_F2']),
                 ('C_prime_2', h['secondary_labelled']['C_prime_2'], rv['C_prime_2']),
                 ('c_site_prime_2', h['secondary_labelled']['c_site_prime_2'], rv['c_site_prime_2']),
                 ('ratio_F1', h['C_dyn']['F1']['tau_over_100_ratio']['exact'], rv['C_dyn_F1_ratio']),
                 ('ratio_F2', h['C_dyn']['F2']['tau_over_100_ratio']['exact'], rv['C_dyn_F2_ratio'])]
        for key, row in h['item4_rows'].items():
            m = re.fullmatch(r'N=(\d+),v=\((-?\d+), (-?\d+), (-?\d+)\)', key)
            if m is None:
                raise Rejected('item-4 row key malformed: ' + key)
            n, v = int(m.group(1)), tuple(int(m.group(i)) for i in (2, 3, 4))
            k = max(abs(x) for x in v)
            want = ref['C_h'] * ref['q'] ** (n - k - 1)
            pairs.append(('item4 ' + key, row['exact'], want))
            if row['union_fallback_labelled'] != sci_like(2 * want):
                raise Rejected('item-4 union fallback differs from 2 C_h q^(N-|v|-1): ' + key)
        checks = {c['id']: c for c in res['checks']}
        rate = checks['item5_rate_in_N_certified_range']
        k_reg, k_r = rat(rate['K_reg']), rat(rate['K_R'])
        # validity, not only equality: K_reg must dominate N*region(N) at its maximum (N=5), K_R must equal 10 C' q^4
        if k_reg < 5 * region_value_upper(5, rv['c_site_prime']):
            raise Rejected('reverse K_reg below the maximum of N*region(N) (certificate invalid)')
        if k_reg != rv['c_site_prime'] * 625 * F(27183, 10000) * F(1, 8) ** 6:
            raise Rejected('reverse K_reg differs from its stated formula c_site*625*E_UP*8^-6')
        if k_r != 10 * rv['C_prime'] * ref['q'] ** 4:
            raise Rejected('reverse K_R differs from 10 C_prime q^4')
        for fam in ('F1', 'F2'):
            want = 10 * rv['C_dyn_' + fam] + k_reg + k_r
            pairs.append(('K5_' + fam, rate['K5'][fam]['exact'], want))
        for key, row in h['item5_values'].items():
            fam, n = key.split(',N=')
            n = int(n)
            dyn = rv['C_dyn_' + fam] / (r_N(n) - 1)
            reg_up, reg_raw = reverse_region(n, rv['c_site_prime'])
            mean = 2 * rv['C_prime'] * ref['q'] ** (n - 1)
            pairs.append(('item5 dynamics ' + key, row['C_dyn/(r_N-1)']['exact'], dyn))
            pairs.append(('item5 mean ' + key, row["2C'q^(N-1)"]['exact'], mean))
            reg_key = [k_ for k_ in row if k_.startswith("c'_site")][0]
            pairs.append(('item5 region ' + key, row[reg_key]['exact'], reg_up))
            lam = (2 * r_N(n) + 1) ** 3
            true_lower = rv['c_site_prime'] * lam * pre.exp_enclosure(F(lam, 10 ** 8))[0] * ref['q'] ** (n - r_N(n))
            if rat(row[reg_key]['exact']) < true_lower:
                raise Rejected('reverse region value below a lower enclosure of the true value: ' + key)
            den = 10 ** 40
            tot = dyn + reg_raw + mean
            pairs.append(('item5 sum ' + key, row['sum (directed upper)']['exact'], F(-((-tot.numerator * den) // tot.denominator), den)))
    for name, got, want in pairs:
        if rat(got) != want:
            raise Rejected('value differs from the independent recomputation: ' + direction + ' ' + name)
    return len(pairs)


def sci_like(x, digits=12):
    """The reverse's truncated preview format (integer arithmetic, 12 significant digits)."""
    x = F(x)
    e = len(str(x.numerator)) - len(str(x.denominator))
    while F(10) ** e > x:
        e -= 1
    while F(10) ** (e + 1) <= x:
        e += 1
    scaled = x / F(10) ** e * 10 ** (digits - 1)
    mant = str(scaled.numerator // scaled.denominator)
    return mant[0] + '.' + mant[1:] + 'e' + str(e)


# ------------------------------------------------------------ closures, replays, mutated copies
def verify_closure(direction):
    src = SIDES[direction]
    freeze = json.loads((src / 'freeze.json').read_text())
    prefix = src.relative_to(ROOT).as_posix() + '/'
    sources = freeze['sources']
    files = {p.relative_to(ROOT).as_posix() for p in src.rglob('*') if p.is_file() and p != src / 'freeze.json'}
    ok = (freeze['loop'] == 'BB2' and freeze['direction'] == direction and freeze['contract_sha256'] == CONTRACT_SHA
          and all(n.startswith(prefix) for n in sources) and set(sources) == files and len(sources) == 42
          and all(sha(ROOT / n) == d for n, d in sources.items())
          and not any('__pycache__' in n or n.endswith('.pyc') for n in files)
          and freeze['normal_optimized_identical'] is True and freeze['independent_before_current_counterpart_exchange'] is True
          and 'conditional_on_bb1_targets' in freeze['verdict'])
    inputs = sorted(p.relative_to(src / 'inputs').as_posix() for p in (src / 'inputs').rglob('*') if p.is_file())
    snapshots_equal = all((src / 'inputs' / n).read_bytes() == (ROOT / n).read_bytes() for n in inputs)
    return ok, inputs, snapshots_equal, freeze


def replay(script, optimized):
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bb2-skeptic-replay-') as tmp:
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if optimized else [])
        done = subprocess.run([sys.executable] + flags + [str(script), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(ROOT))
        if done.returncode != 0:
            raise ReviewFailure('replay failed: ' + str(script) + ' ' + done.stderr[-300:])
        return {p.relative_to(out).as_posix(): sha(p) for p in sorted(out.rglob('*')) if p.is_file()}


def mutated_run(direction, edits=(), extra_input=None, contract_edit=None, report_edits=(), report_append=None):
    src = SIDES[direction]
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bb2-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / 'research/round33' / direction / 'bb2'
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        code = (dst / 'check.py').read_text()
        for old, new in edits:
            if code.count(old) != 1:
                raise ReviewFailure('mutation anchor not unique in %s (%d): %r' % (direction, code.count(old), old[:80]))
            code = code.replace(old, new)
        (dst / 'check.py').write_text(code)
        if contract_edit is not None:
            cpath = dst / 'inputs/research/round33/contracts/bb2.json'
            raw = cpath.read_bytes()
            old, new = contract_edit
            if raw.count(old) != 1:
                raise ReviewFailure('contract mutation anchor not unique')
            cpath.write_bytes(raw.replace(old, new))
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


def weaken(line):
    """Replace a validator's require(<condition>, <message>) by require(True, <message>)."""
    head = line[:len(line) - len(line.lstrip())]
    rest = line.lstrip()
    if not rest.startswith('require('):
        raise ReviewFailure('not a require line')
    tail = rest[len('require('):]
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
    return (line, head + 'require(True, ' + tail[cut + 1:].lstrip())


FWD_WEAK = [
    ('coherent_evidence_tampering', [weaken("            require(cid in ids and ids[cid]['passed'] is True, 'required control missing or failed: ' + cid)")],
     'control_boolean_flipped_hash_rebound'),
    ('exact_arithmetic_admission', [("        raise AdmissionError('non-exact input rejected: ' + repr(value))", "        return Q(value)")], 'float_input'),
    ('no_priority_or_continuum_claim', [weaken("            require(fl.get(k1) is v1, 'claim flag ' + k1 + ' must be false')")], 'continuum_true'),
    ('changed_model_relabelled', [weaken("        require(mdl == MODEL and rat(mdl['tau']) == tau_cap, 'model packet differs from the contract')")], 'tau_changed'),
    ('insufficient_verdict_retained', [weaken("        require(label == forward_verdict(cauchy_closed, im, discharge), 'verdict label differs from the acceptance rule')")],
     'missed_item_relabelled_accepted'),
    ('tau_scaling_exponent', [weaken("        require(br[0] <= ratio <= br[1], 'scaling ratio outside its bracket: ' + name)")], 'C_dyn_linear_order'),
    ('wrong_delta_alpha_hbar_clock', [weaken("        require(u_v == theta_v / 8, 'u = delta t/hbar = theta/8 (delta = alpha/8)')")], 'eightfold_u_labelled_theta'),
    ('root_n_misuse', [weaken("        require(total == sum(parts), 'deterministic step bounds add linearly')")], 'division_by_isqrt_of_10_steps'),
    ('tier_mixing_rejected', [weaken("            require(r.get('tier') in ('exact_first_order', 'crude_majorant'), 'state constant tier: ' + n_)")],
     'state_constant_LR_tier'),
    ('reverse_premise_isolation', [weaken("        require(sorted(set(lst)) == sorted(set(['AGENTS.md', CONTRACT_REL] + V['shared'])), 'reverse inventory must equal AGENTS, contract and shared premises')"),
                                   weaken("            require(not any(b1_ in item for b1_ in bad_parts), 'reverse premise isolation violated by ' + item)")],
     'reads_bb1_producer'),
    ('uniform_in_N_not_in_a', [weaken("            require(not bad, 'unqualified uniformity statement in ' + name + ': ' + (bad[0] if bad else ''))")],
     'uniform_in_a_claimed'),
    ('placeholder_span_rejected', [weaken("            require(not spans and '<' not in body, 'placeholder span in ' + name + ': ' + (spans[0] if spans else '<'))")],
     'whitespace_placeholder'),
    ('negation_aware_phrase_scan', [weaken("            require(not hits, 'affirmative forbidden phrasing in ' + name + ': ' + (hits[0]['phrase'] if hits else ''))")],
     'affirmative_thermodynamic_limit'),
    ('parameters_declare_metric_weights_window', [weaken("            require(key in params and params[key], 'parameters field missing: ' + key)")],
     'window_field_absent'),
    ('rate_constant_pair_prefrozen', [weaken("        require(qq == V['q'] and target_Cp == V['target_Cp'] and target_cp == V['target_cp'], 'q and targets are the frozen ones')")],
     'q_retuned'),
    ('decay_rate_in_N_not_a', [weaken("        require(unit == 'per coarse step at fixed spacing', 'rates are per coarse step at fixed spacing')")], 'conversion_to_fm'),
    ('topology_named', [weaken("        require(t == TOP, 'topologies named: trace norm for states, operator norm on the window for dynamics, GNS strong for representations')")],
     'weak_star_relabelled_trace_norm'),
    ('two_families_named', [weaken("        require(all('Lambda_N' in x and 'orthant' not in x and 'literal' not in x for x in fam.values()), 'centered boxes only')")],
     'orthant_boxes'),
    ('subsequence_versus_whole_sequence', [weaken("                require(basis == 'cauchy_bound', 'whole-sequence claims come only from a Cauchy bound: ' + obj)")],
     'whole_sequence_from_compactness'),
    ('common_clock', [weaken("        require(rec['tau_F1'] == rec['tau_F2'] == rec['tau_limit'], 'both families and the limit at the same coupling')")],
     'F2_at_opposite_sign'),
    ('named_construction_not_uniqueness', [weaken("        require(rec['uniqueness_of_ground_state_claimed'] is False, 'no uniqueness of any ground state')")],
     'uniqueness_claimed'),
    ('cauchy_estimate_not_compactness', [weaken("        require(b == 'explicit_cauchy_bound_and_trace_class_completeness', 'whole-sequence convergence from an explicit Cauchy bound')")],
     'compactness_plus_closeness'),
    ('limit_identified_with_aq1_limits', [weaken("        require(steps_.index('identify') < steps_.index('inherit'), 'inherit only after identification')")], 'inherit_first'),
    ('translation_invariance_separate_item', [weaken("        require(basis == 'general_volume_comparison', 'translation invariance only from the general-volume comparison')")],
     'invariance_from_nested_cubes'),
    ('region_constant_scales_with_Y', [weaken("        require(val >= honest, 'a region bound must carry |Y| and d_Y (a constant proved for R reused on Y is rejected)')")],
     'R_constant_reused_on_Lambda_2'),
    ('cutoff_uniform_then_removed', [weaken("        require(order == ['bound in each Q_L', 'L to infinity at fixed N and M', 'sup over M', 'N to infinity'], 'L is removed at fixed N before any N limit')")],
     'N_limit_taken_in_Q_L_first'),
    ('algebraic_not_gns_dynamics', [weaken("        require(fields['gns_dynamics_equality_claimed'] is False, 'no equality of GNS dynamics of different states')")],
     'gns_dynamics_equality_claimed'),
    ('lieb_robinson_polynomial_tail', [weaken("        require(form == 'C_dyn/(r_N-1)', 'with F(r)=(1+r)^-4 the dynamics term is polynomial in N; an exponential tail is not available')")],
     'exponential_tail_with_polynomial_F'),
    ('time_window_named_common_clock', [weaken("        require(uniform_in_time is False, 'no uniform-in-time claim')")], 'uniform_in_time_claimed'),
    ('fixture_whole_sequence_vs_subsequence', [weaken("        require(evidence in ('sup_over_M_cauchy_bound',), 'convergence needs a sup-over-M Cauchy bound')")],
     'one_state_ball_read_as_convergence'),
    ('fixture_translation_residues', [weaken("        require(ok and vc is not None, 'not a coarse translation: residues or face classes broken by ' + str(w))")],
     'fine_x_shift_by_1'),
    ('fixture_correlation_centering', [weaken("        require(val[1] == 0 and val == variance and val[0] >= 0, 'centering must use |omega(A)|^2: the value at theta=0 is the variance')")],
     'centering_with_omega_A_squared'),
    ('conditional_on_bb1_targets', [weaken("        require(rec['C_h'] == V['C_h'] and rec['c_h'] == V['c_h'], 'BB1 values must be the frozen targets')")],
     'bb1_value_other_than_frozen_target'),
    ('r_N_prefrozen', [weaken("        require(all(fn(N) == (N - 1) // 2 for N in range(5, 300)), 'r_N must be floor((N-1)/2) as frozen')")],
     'post_hoc_optimized_r_N'),
]
REV_WEAK = [
    ('coherent_evidence_tampering', [weaken("    require(data.get('reverse_premise_isolation') is True, 'reverse premise isolation flag')")],
     'isolation_flag_flipped_rehashed'),
    ('exact_arithmetic_admission', [("        raise AdmissionError('non-exact numeric input rejected: ' + repr(value))", "        return Q(value)")], 'float_constant'),
    ('no_priority_or_continuum_claim', [weaken("        require(flags.get(key) is False, 'claim flag must be exactly false: ' + key)")], 'continuum_true'),
    ('changed_model_relabelled', [weaken("    require(parse_q(rec.get('tau')) == contract_tau, 'packet tau differs from the contract (retuning or changed model)')")],
     'tau_1e-7'),
    ('insufficient_verdict_retained', [weaken("    require(recorded == want, 'recorded verdict ' + str(recorded) + ' differs from the rule (' + want + ')')")],
     'missed_C_prime_relabelled_accepted'),
    ('tau_scaling_exponent', [weaken("    require(lo <= ratio <= hi, 'tau -> tau/100 ratio outside its preregistered bracket')")], 'C_dyn_linear_order'),
    ('wrong_delta_alpha_hbar_clock', [weaken("    require(parse_q(U) == Q(parse_q(theta_window), 8), 'normalized window must be U=Theta/8 (u=theta/8, delta=alpha/8)')")],
     'u_window_labelled_theta'),
    ('root_n_misuse', [weaken("    require(combine == 'linear', 'root-sum-square or root-N assembly rejected')")], 'item5_terms_in_quadrature'),
    ('tier_mixing_rejected', [weaken("    require(rec.get('tier') in STATE_TIERS, 'state constant must carry exactly one state tier (exact_first_order or crude_majorant)')")],
     'state_constant_lr_tier'),
    ('reverse_premise_isolation', [weaken("        require(not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in reverse inputs: ' + f)"),
                                   ("    require(sorted(files) == sorted(expected) and len(files) == len(expected),", "    require(True,")],
     'forward_bb2_report_added'),
    ('uniform_in_N_not_in_a', [("    require(re.search(r'uniform(ly)? in (the )?(lattice spacing|a)(?![a-z0-9_])', low) is None,", "    require(True,")],
     'uniform_in_lattice_spacing'),
    ('placeholder_span_rejected', [weaken("            require(not (re.search(r'\\s', span) or '|' in span or 'e.g.' in span), 'placeholder span blocks the freeze: ' + span[:60])")],
     'placeholder_gate'),
    ('negation_aware_phrase_scan', [weaken("    require(hits == [], 'affirmative forbidden phrasing: ' + (hits[0] if hits else ''))")], 'affirmative_thermodynamic_limit'),
    ('parameters_declare_metric_weights_window', [("        require(isinstance(p.get(key), str) and bool(p.get(key)), 'parameters must declare ' + key + ' as a field (not prose)')",
                                                   "        require((isinstance(p.get(key), str) and bool(p.get(key))) or key == 'weights', 'parameters must declare ' + key + ' as a field (not prose)')")],
     'weights_removed'),
    ('rate_constant_pair_prefrozen', [weaken("    require(rec.get('q_per_N') is False, 'optimizing q per N rejected')")], 'q_optimized_per_N'),
    ('decay_rate_in_N_not_a', [weaken("        require(re.search(r'(?<![a-z])' + re.escape(bad) + r'(?![a-z])', low) is None, 'rate converted to a physical length or to a')")],
     'converted_to_fm'),
    ('topology_named', [weaken("    require(rec.get('representations') == GNS_TOPOLOGY, 'representations: GNS strong continuity only')")], 'norm_continuity_in_theta'),
    ('two_families_named', [weaken("    require(rec == [F1_NAME, F2_NAME], 'exactly the two named families F1 and F2')")], 'single_family'),
    ('subsequence_versus_whole_sequence', [weaken("        require(rec.get('from') == 'Cauchy bound', 'whole-sequence claims come only from a Cauchy bound')")],
     'states_whole_sequence_from_compactness'),
    ('common_clock', [weaken("    require(parse_q(tau1) == parse_q(tau2), 'cross-coupling comparison rejected: every comparison at the same tau')")],
     'plus_versus_minus_tau'),
    ('named_construction_not_uniqueness', [("    require(hits == [], 'affirmative forbidden phrasing: ' + (hits[0] if hits else ''))",
                                            "    require(hits == [] or len(text) < 400, 'affirmative forbidden phrasing: ' + (hits[0] if hits else ''))")],
     'the_infinite_volume_ground_state'),
    ('cauchy_estimate_not_compactness', [("    require(rec.get('limit_from') == 'Cauchy bound and completeness of the trace class',", "    require(True,")],
     'compactness_plus_closeness'),
    ('limit_identified_with_aq1_limits', [("    require(rec.get('order') == ['whole-sequence limit', 'identified with every AQ1 and every F2 subsequential limit',",
                                           "    require(True or ['whole-sequence limit',")],
     'inherit_before_identification'),
    ('translation_invariance_separate_item', [("    require(rec.get('source') == 'bb1 general-volume comparison: Lambda_N+v versus Lambda_N, both containing Lambda_(N-|v|_inf)',",
                                               "    require(True,")],
     'from_nested_cubes'),
    ('region_constant_scales_with_Y', [weaken("    require(rec.get('constant') == 'c_site_prime', 'a constant proved for R reused on a region Y')")],
     'R_constant_reused_on_Y'),
    ('cutoff_uniform_then_removed', [weaken("    require(rec.get('order') == CUTOFF_ORDER, 'the N and L limits are never exchanged (uniform in L, then L at fixed N)')")],
     'limits_exchanged'),
    ('algebraic_not_gns_dynamics', [weaken("    require(rec.get('gns_equality_of_different_states') is False, 'equality of GNS dynamics of different states rejected')")],
     'gns_equality_finite_versus_limit'),
    ('lieb_robinson_polynomial_tail', [weaken("    require(rng[1] <= certified_max, 'O(1/N) claimed beyond the certified range: the frozen bound is vacuous at N=' + str(vacuous_at))")],
     'O_one_over_N_for_all_N'),
    ('time_window_named_common_clock', [weaken("    require(rec.get('uniform_in_time') is False, 'uniform-in-time claim rejected (the BA2 bounds grow like U^2/(1-vU/3))')")],
     'uniform_in_time'),
    ('fixture_whole_sequence_vs_subsequence', [("        require(s <= bound(N), 'tail supremum exceeds the claimed Cauchy bound at N=' + str(N))",
                                                "        require(s <= bound(N) or bound(N) == bound(N + 1), 'tail supremum exceeds the claimed Cauchy bound at N=' + str(N))"),
                                               ("    require(bound(last) <= Q(1, 1000), 'the claimed bound does not tend to zero')",
                                                "    require(bound(last) <= Q(1, 1000) or bound(last) == bound(last + 1), 'the claimed bound does not tend to zero')")],
     'alternating_one_state_ball_as_convergent'),
    ('fixture_translation_residues', [weaken("    require(preserved is True and is_coarse_fine_translation(t), 'a non-coarse fine translation is not a symmetry of the patterned model')")],
     'fine_x_by_1'),
    ('fixture_correlation_centering', [("    require(parse_q(omega_AA[0]) - parse_q(centering_value) == var_vector and omega_AA[1] == 0,", "    require(True,")],
     'real_square_centering'),
    ('conditional_on_bb1_targets', [weaken("        require(parse_q(rec.get(key)) == frozen[key], 'a BB1 value other than the frozen target: ' + key)")],
     'bb1_value_other_than_target'),
    ('r_N_prefrozen', [weaken("        require(rule(N) == (N - 1) // 2, 'r_N differs from floor((N-1)/2) at N=' + str(N))")], 'r_N_N_minus_2'),
]
TEMPLATE_LINE_ANCHOR = 'For the zero-selected patterned family at the same coupling |tau|<=10^-8, under the BB1 locality bounds'
CONTRACT_ANCHOR = (b'"C_prime_target": "1/100000"', b'"C_prime_target": "1/90000"')
MUST_ABORT = [
    ('forward', 'C_prime_function_coefficient_changed', {'edits': [("        return Ch / (1 - q)", "        return Ch / (1 - 2 * q)")]},
     'failed check item1_whole_sequence_cauchy_R'),
    ('forward', 'lemma_F08_quarter_to_eighth', {'edits': [("    lem_exact = all(Q((5 * N + 1) * (rN(N) - 1)) <= Q(N ** 3, 4) for N in range(5, 3001))",
                                                            "    lem_exact = all(Q((5 * N + 1) * (rN(N) - 1)) <= Q(N ** 3, 8) for N in range(5, 3001))")]},
     'failed check item5_correlation_bound'),
    ('forward', 'C_dyn_K_cmp_over_8', {'edits': [("    Cdyn_F2 = 2 * K_F1 + K_cmp / 4", "    Cdyn_F2 = 2 * K_F1 + K_cmp / 8")]}, 'failed check'),
    ('forward', 'contract_byte_edit', {'contract_edit': CONTRACT_ANCHOR}, 'contract snapshot bytes differ from the frozen BB2 contract'),
    ('forward', 'undeclared_input_bb1_forward_report', {'extra_input': 'research/round33/forward/bb1/report.md'}, 'failed check reverse_premise_isolation'),
    ('forward', 'report_forbidden_phrase', {'report_append': '\nThe thermodynamic limit of the named constructions exists.\n'},
     'affirmative forbidden phrasing in report.md'),
    ('forward', 'report_template_removed', {'report_edits': [(TEMPLATE_LINE_ANCHOR, 'For the patterned family, under the BB1 locality bounds')]},
     'failed check mandatory_sentence_verbatim_once'),
    ('reverse', 'dynamics_ratio_10_to_2', {'edits': [("    ratio_dyn_ok = all(N * 1 <= 10 * (rN(N) - 1) for N in range(5, RATE_CERTIFIED_MAX + 1))",
                                                       "    ratio_dyn_ok = all(N * 1 <= 2 * (rN(N) - 1) for N in range(5, RATE_CERTIFIED_MAX + 1))")]},
     'check failed: item5_rate_in_N_certified_range'),
    ('reverse', 'vacuous_at_14415', {'edits': [("RATE_VACUOUS_AT = 14421", "RATE_VACUOUS_AT = 14415")]},
     'check failed: item5_rate_in_N_certified_range'),
    ('reverse', 'contract_byte_edit', {'contract_edit': CONTRACT_ANCHOR}, 'contract'),
    ('reverse', 'skeptic_triage_added_to_inputs', {'extra_input': 'research/round33/skeptic/triage.md'}, 'triage'),
    ('reverse', 'report_forbidden_phrase', {'report_append': '\nThe thermodynamic limit of the named constructions exists.\n'},
     'affirmative forbidden phrasing'),
    ('reverse', 'report_template_removed', {'report_edits': [(TEMPLATE_LINE_ANCHOR, 'For the patterned family, under the BB1 locality bounds')]},
     'mandatory'),
]
SILENT = [
    ('forward', 'item5_F1_sums_with_the_F2_constant', {'edits': [("    sums_F1 = {N: bracket_sum(N, Cdyn_F1) for N in (5, 10)}",
                                                                   "    sums_F1 = {N: bracket_sum(N, Cdyn) for N in (5, 10)}")]},
     'item5_F1_sum_N5'),
    ('forward', 'secondary_c_site_factor_doubled', {'edits': [("        return V['c_2h'] / (1 - q2_at(t))", "        return V['c_2h'] / (1 - 2 * q2_at(t))")]},
     'c_site_prime_2'),
    ('reverse', 'K_R_coefficient_10_to_5', {'edits': [("    K_R = 10 * Cp * q ** 4", "    K_R = 5 * Cp * q ** 4")]}, 'K_R differs'),
    ('reverse', 'K_reg_without_the_e_factor', {'edits': [("    K_reg = cs * 625 * E_UP * Q(1, 8) ** 6", "    K_reg = cs * 625 * Q(1, 8) ** 6")]},
     'K_reg below the maximum'),
    ('reverse', 'C_prime_function_doubled', {'edits': [("        return 1 * C_h", "        return 2 * C_h")]}, 'C_prime'),
    ('reverse', 'item4_union_fallback_factor_3', {'edits': [("union_fallback_labelled=sci(2 * Ch * q ** (N - linf(v) - 1)))",
                                                              "union_fallback_labelled=sci(3 * Ch * q ** (N - linf(v) - 1)))")]},
     'union fallback differs'),
]


# ------------------------------------------------------------ discharge part (stage 2: the BB1 gate exists)
BB1_GATE = R33 / 'advisor/bb1-gate.json'
BB1_GATE_SHA = '18141fea672e5bae09024a5fddc56ea7102aae56ecca16fbb30d67a1354a3827'   # commit eef57b4
BB1_REVIEW = HERE / 'bb1.json'
BB1_REVIEW_SHA = '5e5235c8be37fdab8878e1b913cae8bcbc3eb257078f18150f34434aa0031235'  # commit 092f862
ADMISSION = HERE / 'bb2-bb1-admission.json'
ADMISSION_SHA = '6eb6e3bed86fc069ab8905f108759aee0b7a8d8c9705e545f82cf443dda946f6'
JUNG_A2 = R33 / 'experts/jung/assistant-2/results.json'
JUNG_A2_SHA = '89c2a23b7ac657d181cf246c38307fea659ee48b41db1eac0825a8033df96b8f'   # commit bffcb6f
SHORT = dict(zip(pre.COMPARISONS, ('c1', 'c2', 'c3', 'c4', 'c5')))
# verbatim gate phrases and the bound shape each one fixes (the admission may cite only these)
SHAPE_OF_TEXT = {
    'differ by at most C q^(N-1) in trace norm': {'exponent_shift': 0, 'Y_power': 0, 'Y_exp_rate': F(0)},
    '<= c_site |Y| e^{|Y|/10^8} q^{d_Y} with d_Y=N-max_{y in Y}|y|_inf': {'exponent_shift': 0, 'Y_power': 1,
                                                                         'Y_exp_rate': F(1, 10 ** 8)},
}
SIGNS_OF_TEXT = {'Constants (exact; both signs;': ('+', '-'), 'at both signs, in each on-site cutoff space': ('+', '-')}
REGIMES_OF_TEXT = {'in each on-site cutoff space with constants independent of the cutoff, and at fixed N for the untruncated '
                   'ground vectors': ('Q_L', 'untruncated')}
DISCHARGE_RULE = ('an item is unconditional only when, at both signs, some BB2 route proves it from BB1 comparisons admitted at '
                  'q=1/64 in a bound dominated pointwise by the hypothesis form with a constant at most the hypothesis value, '
                  'in the untruncated regime or in Q_L for a route that removes the cutoff itself (pre-registered in bb2_check.py, '
                  'committed at 8921539 before either producer or the BB1 gate was read)')


def gate_text_of(gate):
    return re.sub(r'\s+', ' ', ' '.join([str(gate.get('accepted', '')), str(gate.get('decision', '')),
                                         ' '.join(gate.get('limitations', []))]))


def read_admission(gate_bytes, adm, bb1_comparisons, ref):
    """Turn the admission record into the discharge engine's record; every entry must be anchored in the gate text."""
    gate = json.loads(gate_bytes)
    if gate.get('loop') != 'BB1':
        raise ReviewFailure('the supplied gate is not the BB1 gate')
    if adm.get('bb1_gate_sha256') != hashlib.sha256(gate_bytes).hexdigest() or adm.get('verdict') != gate.get('verdict'):
        raise ReviewFailure('admission record does not match the BB1 gate (sha256 or verdict)')
    text = gate_text_of(gate)

    def anchored(s, what):
        if not isinstance(s, str) or not s or re.sub(r'\s+', ' ', s) not in text:
            raise ReviewFailure('not anchored in the BB1 gate text: ' + what)
    signs, regimes = set(), set()
    for s in adm['signs_gate_text']:
        anchored(s, 'signs')
        signs |= set(SIGNS_OF_TEXT.get(s, ()))
    for s in adm['regimes_gate_text']:
        anchored(s, 'regimes')
        regimes |= set(REGIMES_OF_TEXT.get(s, ()))
    if not set(adm['signs']) <= signs or not set(adm['regimes']) <= regimes:
        raise ReviewFailure('signs or regimes claimed beyond the gate text')
    anchored(adm['comparisons_gate_text'], 'comparison list')
    anchored(adm['q_gate_text'], 'q')
    m = re.fullmatch(r'q=(\d+/\d+)', adm['q_gate_text'])
    if m is None:
        raise ReviewFailure('q anchor malformed')
    q_gate = F(m.group(1))
    anchors = 0

    def entry(f, what):
        nonlocal anchors
        anchored(f['gate_text'], what)
        if not re.sub(r'\s+', ' ', f['gate_text']).endswith('=' + f['c']):
            raise ReviewFailure('admitted constant not anchored in the BB1 gate text: ' + what)
        anchors += 1
        return F(f['c'])
    admitted, also = {}, {}
    for i, comp in enumerate(pre.COMPARISONS):
        e = (adm.get('admitted') or {}).get(comp)
        if e is None:
            admitted[comp] = also[comp] = None
            continue
        anchored(e['gate_scope_text'], comp)
        if not e['gate_scope_text'].startswith(SHORT[comp] + ' ') or e['bb1_contract_comparison'] != bb1_comparisons[i]:
            raise ReviewFailure('comparison label differs from the BB1 gate or contract: ' + comp)
        admitted[comp], also[comp] = {}, {}
        for form in ('R', 'Y'):
            f = e.get(form)
            if f is None:
                admitted[comp][form] = also[comp][form] = None
                continue
            anchored(f['shape_text'], comp + ' ' + form + ' shape')
            shp = SHAPE_OF_TEXT.get(f['shape_text'])
            if shp is None or (form == 'R') != (shp['Y_power'] == 0):
                raise ReviewFailure('shape text does not fix a bound of this form: ' + comp + ' ' + form)
            claimed = {'exponent_shift': int(f['exponent_shift']), 'Y_power': int(f['Y_power']), 'Y_exp_rate': F(f['Y_exp_rate'])}
            if claimed != shp or F(f['q']) != q_gate:
                raise ReviewFailure('shape differs from the gate text: ' + comp + ' ' + form)
            shape = dict(shp, q=q_gate)
            admitted[comp][form] = {'c': entry(f, comp + ' ' + form), 'shape': shape}
            anchored(f['route'], 'route')
            a = f.get('also_certified_by')
            if a is not None:
                anchored(a['route'], 'route')
            also[comp][form] = None if a is None else {'c': entry(a, comp + ' ' + form + ' also'), 'shape': shape,
                                                       'route': a['route']}
    sec = adm['secondary_labelled']
    anchored(sec['q_gate_text'], 'secondary q')
    anchored(sec['targets_gate_text'], 'secondary targets')
    if F(sec['q_at_cap']) != ref['q2'] or '151552|tau|' not in sec['q_gate_text']:
        raise ReviewFailure('secondary q differs from 151552|tau| at the cap')
    q2 = ref['q2']
    secondary = {}
    for comp in pre.COMPARISONS:
        if admitted[comp] is None:
            secondary[comp] = None
            continue
        secondary[comp] = {}
        for form in ('R', 'Y'):
            base = admitted[comp][form]
            secondary[comp][form] = None if base is None else {
                'c': entry(sec[form], 'secondary ' + form), 'shape': dict(base['shape'], q=q2)}
    return {'gate': gate, 'text': text, 'anchors': anchors, 'signs': sorted(adm['signs']), 'regimes': sorted(adm['regimes']),
            'admitted': admitted, 'also': also, 'secondary': secondary}


def hyp_primary(ref):
    return {'q': ref['q'], 'const': {'R': ref['C_h'], 'Y': ref['c_h']},
            'shape': {'R': {'q': ref['q'], 'exponent_shift': 0, 'Y_power': 0, 'Y_exp_rate': F(0)},
                      'Y': {'q': ref['q'], 'exponent_shift': 0, 'Y_power': 1, 'Y_exp_rate': F(1, 10 ** 8)}}}


def hyp_secondary(ref):
    h = hyp_primary(ref)
    return {'q': ref['q2'], 'const': {'R': ref['C_2h'], 'Y': ref['c_2h']},
            'shape': {k: dict(v, q=ref['q2']) for k, v in h['shape'].items()}}


def engine(rec, admitted, hyp):
    record = {'verdict': rec['gate']['verdict'], 'admitted': admitted, 'regimes': rec['regimes'], 'signs': rec['signs']}
    return pre.discharge(record, hyp)


# ---- the producers' own hypothesis maps
def _regime(s):
    s = s.strip()
    if s.startswith('each on-site cutoff space Q_L') or s.startswith('each Q_L'):
        return 'Q_L'
    if 'untruncated' in s:
        return 'untruncated'
    raise ReviewFailure('unreadable cutoff regime: ' + s)


def _form(s):
    if s.startswith('R'):
        return 'R'
    if s.startswith('region'):
        return 'Y'
    raise ReviewFailure('unreadable form: ' + s)


def _sign(s):
    if s in ('+', '+tau'):
        return '+'
    if s in ('-', '-tau'):
        return '-'
    raise ReviewFailure('unreadable sign: ' + s)


def forward_map(res, bb1_comparisons):
    comp_of = {t: pre.COMPARISONS[i] for i, t in enumerate(bb1_comparisons)}
    items = {k: {'hypotheses': [], 'cells': set()} for k in ('1', '2', '3', '4', '5', 'secondary')}
    by_id = {}
    for h in res['hypotheses_used']:
        if h['id'] == 'H1s-H3s':
            if h['comparison'] != 'as H1-H3, secondary pair':
                raise ReviewFailure('forward secondary hypothesis text changed')
            comps = [by_id[i] for i in ('H1', 'H2', 'H3')]
            targets = ['secondary']
        else:
            if h['comparison'] not in comp_of:
                raise ReviewFailure('forward hypothesis not a BB1 contract comparison: ' + h['id'])
            comps = [comp_of[h['comparison']]]
            by_id[h['id']] = comps[0]
            targets = list(h['items'])
        for it in targets:
            items[it]['hypotheses'].append(h['id'])
            for comp in comps:
                for form in h['forms']:
                    for reg in h['cutoff_regimes']:
                        for sg in h['signs']:
                            items[it]['cells'].add((comp, _form(form), _regime(reg), _sign(sg)))
    return items, by_id


def reverse_map(res, bb1_comparisons):
    comp_of = {t: pre.COMPARISONS[i] for i, t in enumerate(bb1_comparisons)}
    b_comp = {b: comp_of[t] for b, t in res['bb1_comparisons'].items()}
    hu = res['hypotheses_used']
    literal, refs = {}, {}
    for k in ('1', '2', '3', '4', '5', 'secondary'):
        row = hu['item' + k] if k != 'secondary' else hu['secondary']
        text = ' '.join(row['comparisons'])
        literal[k] = sorted({b_comp['B' + b] for b in re.findall(r'\bB([1-5])\b', text)})
        rr = set()
        for a, b in re.findall(r'\bitems? (\d)(?:-(\d))?', text):
            rr |= set(str(i) for i in range(int(a), int(b or a) + 1))
        refs[k] = sorted(rr - {k})
    closure = {}

    def close(k, seen=()):
        out = set(literal[k])
        for r in refs[k]:
            if r not in seen:
                out |= close(r, seen + (k,))
        return out
    for k in literal:
        closure[k] = sorted(close(k))
    items = {}
    for k in literal:
        row = hu['item' + k] if k != 'secondary' else hu['secondary']
        forms = [_form(f) for f in row['forms']]
        regs = [_regime(r) for r in row.get('cutoff_regimes', [])] or ['Q_L', 'untruncated']
        sgs = [_sign(s) for s in row.get('signs', [])] or ['+', '-']
        cells = {(c, f, r, s) for c in closure[k] for f in forms for r in regs for s in sgs}
        items[k] = {'literal': literal[k], 'item_references': refs[k], 'closure': closure[k], 'cells': cells,
                    'regimes_listed': bool(row.get('cutoff_regimes')), 'signs_listed': bool(row.get('signs'))}
    return items


def discharge_cells(cells, rec, admitted, hyp):
    """Every (comparison, form, regime, sign) cell used must be admitted with a dominated bound (conservative: alternatives
    such as the reverse's 'B4 ... equivalently B5' are all required)."""
    missing = []
    for comp, form, reg, sg in sorted(cells):
        e = (admitted.get(comp) or {}).get(form)
        if not (reg in rec['regimes'] and sg in rec['signs'] and pre.dominated(e, form, hyp)):
            missing.append('%s %s %s %s' % (SHORT[comp], form, reg, sg))
    return missing


def map_rows(items_cells, rec, admitted, hyp, extra=None):
    rows = {}
    for k, v in items_cells.items():
        cells = v['cells']
        missing = discharge_cells(cells, rec, admitted, hyp)
        row = {'comparisons': sorted({SHORT[c] for c, _, _, _ in cells}), 'forms': sorted({f for _, f, _, _ in cells}),
               'regimes': sorted({r for _, _, r, _ in cells}), 'signs': sorted({s for _, _, _, s in cells}),
               'cells': len(cells), 'cells_discharged': len(cells) - len(missing), 'missing': missing,
               'status': 'discharged' if not missing and cells else 'conditional_on_bb1_targets'}
        for key in (extra or ()):
            row[key] = [SHORT[c] for c in v[key]] if key in ('literal', 'closure') else v[key]
        rows[k] = row
    return rows


# ---- item-5 range, vacuity and first exceedance at a given constant set
def ln_enclosure(z, l2, terms=40, den=10 ** 45):
    """Directed enclosure of ln z (z > 0 rational): z = 2^k w with 1 <= w < 2 and ln w = 2 atanh t, t = (w-1)/(w+1) < 1/3,
    the atanh series with the geometric remainder; ln 2 from the 140-term series enclosure; results on a 10^-45 grid."""
    z = F(z)
    if z <= 0:
        raise ReviewFailure('ln domain')
    k = 0
    while z >= 2:
        z /= 2
        k += 1
    while z < 1:
        z *= 2
        k -= 1
    t = (z - 1) / (z + 1)
    s, p, t2 = F(0), t, t * t
    for j in range(terms):
        s += p / (2 * j + 1)
        p *= t2
    lo = 2 * s + k * (l2[0] if k >= 0 else l2[1])
    hi = 2 * (s + p / (2 * terms + 1) / (1 - t2)) + k * (l2[1] if k >= 0 else l2[0])
    n_lo = lo * den
    n_hi = hi * den
    return F(n_lo.numerator // n_lo.denominator, den), F(-((-n_hi.numerator) // n_hi.denominator), den)


def item5_profile(cdyn, csp, cp, q_, l2):
    """For one constant set: range certificate on 5<=N<=14000 (the envelope of check 4), bracket < 2 on 14001<=N<=14418
    (fine logarithms), bracket >= 2 at 14419, 14420 and every N >= 14421 (coarse logarithms and the monotone envelope)."""
    g5_up = 625 * pre.e_region_hi(125) / 8 ** 6
    k5 = 10 * cdyn + csp * g5_up + 10 * cp * q_ ** 4
    eps = F(1, 10 ** 6)
    small = cdyn + 2 * cp * q_ ** 4 <= eps          # dynamics and mean terms together, for every N >= 5
    ln_c = ln_enclosure(csp, l2)
    ln2_minus = l2[0] - (eps / 2) / (1 - eps / 2)   # ln(2 - eps) >= ln 2 - (eps/2)/(1-eps/2)
    below = small
    worst = None
    for n in range(14001, 14419):
        r = r_N(n)
        lam = (2 * r + 1) ** 3
        up = ln_c[1] + ln_enclosure(lam, l2)[1] + F(lam, 10 ** 8) - (n - r) * 6 * l2[0]
        margin = ln2_minus - up
        if worst is None or margin < worst[1]:
            worst = (n, margin)
        below = below and margin > 0
    vac = {'14419': vacuous_at(14419, csp, l2), '14420': vacuous_at(14420, csp, l2)}
    lam = 14420 ** 3
    m = ln_lower_integer(csp * lam)
    vac['all_N_from_14421'] = (m + F(lam, 10 ** 8) - (F(14421, 2) + 1) * 6 * l2[1] >= l2[1]) and 14420 ** 2 >= 10 ** 8 * l2[1]
    return {'K5_upper_on_5_to_14000': pre.rup(k5), 'K5_preview': preview(k5, 6),
            'bracket_N5_upper': pre.rup(pre.item5_terms(5, cdyn, csp, cp, q_)['sum']),
            'bracket_N5_preview': preview(pre.item5_terms(5, cdyn, csp, cp, q_)['sum'], 6),
            'bracket_N10_upper': pre.rup(pre.item5_terms(10, cdyn, csp, cp, q_)['sum']),
            'bracket_N10_preview': preview(pre.item5_terms(10, cdyn, csp, cp, q_)['sum'], 6),
            'below_2_on_14001_to_14418': below, 'tightest_below_2': {'N': worst[0], 'log_margin_lower': preview(worst[1], 6)},
            'vacuous': vac, 'first_exceedance_of_2': 14419 if below and all(vac.values()) else None}


# ---- the whole stage
def discharge_stage(gate_bytes, adm, review, jung, ref, results, bb1_comparisons, contract):
    rec = read_admission(gate_bytes, adm, bb1_comparisons, ref)
    hyp, hyp2 = hyp_primary(ref), hyp_secondary(ref)
    main = engine(rec, rec['admitted'], hyp)
    sec = engine(rec, rec['secondary'], hyp2)
    alt = engine(rec, rec['also'], hyp)
    # the producers' maps, item by item
    fmap, fids = forward_map(results['forward'], bb1_comparisons)
    rmap = reverse_map(results['reverse'], bb1_comparisons)
    frows = map_rows({k: v for k, v in fmap.items() if k != 'secondary'}, rec, rec['admitted'], hyp, extra=('hypotheses',))
    rrows = map_rows({k: v for k, v in rmap.items() if k != 'secondary'}, rec, rec['admitted'], hyp,
                     extra=('literal', 'item_references', 'closure'))
    fsec = map_rows({'secondary': fmap['secondary']}, rec, rec['secondary'], hyp2, extra=('hypotheses',))['secondary']
    rsec = map_rows({'secondary': rmap['secondary']}, rec, rec['secondary'], hyp2,
                    extra=('literal', 'item_references', 'closure', 'regimes_listed', 'signs_listed'))['secondary']
    # the reverse item-5 reading: its F2 part needs the F2 limit identified with the common limit (item 2, hence c3)
    r5_read = {c for c, _, _, _ in rmap['5']['cells']} | {c for c, _, _, _ in rmap['2']['cells']}
    r5_cells = {(c, f, r, s) for c in r5_read for (_, f, r, s) in rmap['5']['cells']}
    r5_missing = discharge_cells(r5_cells, rec, rec['admitted'], hyp)
    # the Jung assistant-2 table (a lens input, not a decision) against these parsed maps
    pim = jung['hypotheses_map']['checks']['hypotheses_map']['per_item_map']
    jung_eq = {'forward': all(sorted(pim[k]['forward']['bb1_comparisons_used']) == frows[k]['comparisons'] for k in '12345'),
               'reverse_literal': all(sorted(pim[k]['reverse']['bb1_comparisons_used']) == rrows[k]['literal'] for k in '12345'),
               'forward_ids': {h: SHORT[c] for h, c in sorted(fids.items())}}
    # the BB1 review's admitted_values table cell by cell
    av = review['admitted_values']
    cells_checked = 0
    for comp in pre.COMPARISONS:
        s = SHORT[comp]
        for form, rkey, ckey, skey in (('R', 'R', 'C', 'C2'), ('Y', 'region', 'c_site', 'c_site2')):
            a = adm['admitted'][comp][form]
            for regime in ('each_Q_L_uniform_in_L', 'untruncated_fixed_N'):
                for sg in ('+', '-'):
                    cell = av[s][rkey][regime][sg]
                    if not (cell[ckey] == a['c'] and cell['route'] == a['route'] and cell['meets_target'] is True
                            and cell['sign'] == sg and cell['tier'] == a['tier']
                            and cell['also_certified_by'][ckey] == a['also_certified_by']['c']
                            and cell['also_certified_by']['route'] == a['also_certified_by']['route']
                            and cell['secondary_labelled'][skey] == adm['secondary_labelled'][form]['c']
                            and cell['secondary_labelled']['route'] == adm['secondary_labelled'][form]['route']):
                        raise ReviewFailure('admission differs from the BB1 review admitted_values: %s %s %s %s' % (s, form, regime, sg))
                    cells_checked += 1
    rb = review['recommended_bound']
    rb_equal = (rb['C']['value'] == adm['admitted'][pre.COMPARISONS[0]]['R']['c']
                and rb['c_site']['value'] == adm['admitted'][pre.COMPARISONS[0]]['Y']['c']
                and rb['secondary_labelled']['C2'] == adm['secondary_labelled']['R']['c']
                and rb['secondary_labelled']['c_site2'] == adm['secondary_labelled']['Y']['c'])
    # constants: hypothesis values (bound by the BB2 gate) and re-evaluated at the admitted values (labelled)
    Ca, ca = F(adm['admitted'][pre.COMPARISONS[0]]['R']['c']), F(adm['admitted'][pre.COMPARISONS[0]]['Y']['c'])
    C2a, c2a = F(adm['secondary_labelled']['R']['c']), F(adm['secondary_labelled']['Y']['c'])
    q_, q2 = ref['q'], ref['q2']
    fw, rv = ref['forward'], ref['reverse']
    re_fw = {'C_prime': pre.cprime('nested_telescoping', Ca, q_), 'c_site_prime': pre.csite_prime('nested_telescoping', ca, q_),
             'C_prime_2': C2a / (1 - q2), 'c_site_prime_2': c2a / (1 - q2)}
    re_rv = {'C_prime': pre.cprime('union_comparison', Ca, q_), 'c_site_prime': pre.csite_prime('union_comparison', ca, q_),
             'C_prime_2': C2a, 'c_site_prime_2': c2a}
    engine_re = main['reevaluated']
    consistent = all(engine_re['%s_%s_forward' % (fam, form)] == (re_fw['C_prime'] if form == 'R' else re_fw['c_site_prime'])
                     and engine_re['%s_%s_reverse' % (fam, form)] == (re_rv['C_prime'] if form == 'R' else re_rv['c_site_prime'])
                     for fam in ('F1', 'F2') for form in ('R', 'Y'))

    def exact_and_preview(d):
        return {k: {'exact': q(v), 'preview': preview(v)} for k, v in d.items()}
    l2 = ln2_enclosure()
    profiles = {
        'hypothesis_values': {
            'forward': item5_profile(fw['C_dyn'], fw['c_site_prime'], fw['C_prime'], q_, l2),
            'reverse_F1': item5_profile(rv['C_dyn_F1'], rv['c_site_prime'], rv['C_prime'], q_, l2),
            'reverse_F2': item5_profile(rv['C_dyn_F2'], rv['c_site_prime'], rv['C_prime'], q_, l2)},
        'admitted_values_labelled': {
            'forward': item5_profile(fw['C_dyn'], re_fw['c_site_prime'], re_fw['C_prime'], q_, l2),
            'reverse_F1': item5_profile(rv['C_dyn_F1'], re_rv['c_site_prime'], re_rv['C_prime'], q_, l2),
            'reverse_F2': item5_profile(rv['C_dyn_F2'], re_rv['c_site_prime'], re_rv['C_prime'], q_, l2)}}
    profiles_ok = all(p['below_2_on_14001_to_14418'] and all(p['vacuous'].values()) and p['first_exceedance_of_2'] == 14419
                      for grp in profiles.values() for p in grp.values())
    # gate fields: the engine's fields plus the contract scopes of the discharged items
    gf = dict(main['gate_fields'])
    req = contract['preregistration']['gate_fields_required']
    if main['items']['1'] == 'full':
        gf['whole_sequence_scope'] = req['whole_sequence_scope']
    if main['items']['4'] == 'full':
        gf['translation_invariance_scope'] = req['translation_invariance_scope']
    return {
        'bb1_gate': {'path': 'research/round33/advisor/bb1-gate.json', 'sha256': hashlib.sha256(gate_bytes).hexdigest(),
                     'commit': 'eef57b4', 'verdict': rec['gate']['verdict'], 'sub_label': rec['gate'].get('sub_label')},
        'admission': {'path': 'research/round33/skeptic/bb2-bb1-admission.json', 'anchored_entries': rec['anchors'],
                      'signs': rec['signs'], 'regimes': rec['regimes'],
                      'anchor_rule': 'every constant, bound shape, q, comparison label, sign and regime is a verbatim substring '
                                     'of the gate accepted/decision/limitations text (whitespace-normalized); each constant '
                                     'anchor ends with =<the exact constant>; comparison labels also equal the BB1 contract list'},
        'bb1_review_cross_check': {'path': 'research/round33/skeptic/bb1.json', 'cells_equal': cells_checked,
                                   'recommended_bound_equal': rb_equal},
        'protocol': {'rule': DISCHARGE_RULE, 'items': main['items'], 'items_by_sign': main['items_by_sign'],
                     'routes_at_plus': main['routes_plus'], 'verdict': main['verdict'], 'unconditional': main['unconditional'],
                     'map': {'1': 'c1 and c2 (forward, nested telescoping) or c4 (reverse, direct centered comparison), R and '
                                  'region forms, both families', '2': 'item 1 and c3', '3': 'item 2 (per_family from item 1 alone)',
                             '4': 'c5 in R and region form and item 1', '5': 'items 1-2 (region form at Lambda_rN, R form) and BA2'}},
        'producer_maps': {'forward': frows, 'reverse': rrows,
                          'reverse_item5_with_item2': {'comparisons': sorted(SHORT[c] for c in r5_read),
                                                       'cells': len(r5_cells), 'missing': r5_missing,
                                                       'note': 'the reverse lists item 5 as through item 1 only; its F2 part '
                                                               'also needs the F2 limit identified with the common limit '
                                                               '(item 2, hence c3), which is admitted'},
                          'jung_assistant_2_cross_check': jung_eq},
        'secondary_labelled': {'q': '151552|tau| = 592/390625 at the cap', 'items': sec['items'], 'verdict': sec['verdict'],
                               'forward_map': fsec, 'reverse_map': rsec,
                               'hypotheses': {'C_2h': q(ref['C_2h']), 'c_2h': q(ref['c_2h'])},
                               'admitted': {'C_2': q(C2a), 'c_site_2': q(c2a), 'route': 'iterated_split'}},
        'iterated_split_alternative_labelled': {'items': alt['items'], 'verdict': alt['verdict'],
                                                'note': 'the self-contained BB1 route (no Kotecky-Preiss citation) also '
                                                        'discharges every item'},
        'constants': {
            'hypothesis_values_bound_at_the_gate': {
                'forward': {'C_prime': q(fw['C_prime']), 'c_site_prime': q(fw['c_site_prime']), 'C_dyn': q(fw['C_dyn']),
                            'C_prime_2': q(fw['C_prime_2']), 'c_site_prime_2': q(fw['c_site_prime_2']),
                            'item4': 'C_h q^(N-|v|_inf-1), C_h = ' + q(ref['C_h'])},
                'reverse_labelled': {'C_prime': q(rv['C_prime']), 'c_site_prime': q(rv['c_site_prime']),
                                     'C_dyn_F1': q(rv['C_dyn_F1']), 'C_dyn_F2': q(rv['C_dyn_F2']),
                                     'C_prime_2': q(rv['C_prime_2']), 'c_site_prime_2': q(rv['c_site_prime_2'])}},
            'reevaluated_at_admitted_values_labelled': {
                'forward_nested_telescoping': exact_and_preview(re_fw),
                'reverse_union_comparison': exact_and_preview(re_rv),
                'item4_constant': {'exact': q(Ca), 'preview': preview(Ca), 'form': 'C q^(N-|v|_inf-1) with the admitted c5 C'},
                'C_dyn': 'unchanged (BA2 gate constants; not a BB1 quantity)',
                'engine_reevaluated_consistent': consistent},
            'bb1_route_of_bound_value': adm['bb1_route_of_bound_value'],
            'admitted_below_hypothesis': {'C': Ca <= ref['C_h'], 'c_site': ca <= ref['c_h'], 'C_2': C2a <= ref['C_2h'],
                                          'c_site_2': c2a <= ref['c_2h'],
                                          'margins_preview': {'C': preview(ref['C_h'] / Ca, 6), 'c_site': preview(ref['c_h'] / ca, 6),
                                                              'C_2': preview(ref['C_2h'] / C2a, 6),
                                                              'c_site_2': preview(ref['c_2h'] / c2a, 6)}}},
        'item5': {'profiles': profiles, 'all_profiles_first_exceedance_14419': profiles_ok,
                  'statement': 'the inequality holds for every N >= 5; N * bracket <= K5 on 5<=N<=14000 (rate O(1/N) there only); '
                               'the bracket is below 2 on 14001<=N<=14418 and at least 2 at N=14419, 14420 and every N>=14421, '
                               'at the hypothesis values and at the admitted values alike; the correlation functions converge '
                               'along the whole sequence for every N without a rate'},
        'gate_fields': gf, 'gate_fields_equal_contract': gf == req,
        'bb2_verdict_from_discharge': main['verdict'],
        '_ok': (main['verdict'] == 'accepted_within_scope' and all(v == 'full' for v in main['items'].values())
                and sec['verdict'] == 'accepted_within_scope' and alt['verdict'] == 'accepted_within_scope'
                and all(r['status'] == 'discharged' for r in frows.values()) and all(r['status'] == 'discharged' for r in rrows.values())
                and fsec['status'] == 'discharged' and rsec['status'] == 'discharged' and not r5_missing
                and jung_eq['forward'] and jung_eq['reverse_literal'] and cells_checked == 40 and rb_equal and consistent
                and profiles_ok and gf == req and Ca <= ref['C_h'] and ca <= ref['c_h'] and C2a <= ref['C_2h'] and c2a <= ref['c_2h']),
    }


def discharge_controls(gate_bytes, adm, ref, bb1_comparisons):
    """Damaging edits of the gate and the admission record, each with the packet hash rebound unless stated: the engine
    must refuse, or return the stated verdict and item statuses."""
    C = adm['admitted'][pre.COMPARISONS[0]]['R']['c']
    hyp = hyp_primary(ref)

    def variant(gate_edit=None, adm_edit=None, rebind=True):
        gate = json.loads(gate_bytes)
        if gate_edit is not None:
            gate_edit(gate)
        gb = json.dumps(gate, sort_keys=True).encode() if gate_edit is not None else gate_bytes
        a = json.loads(json.dumps(adm))
        if rebind:
            a['bb1_gate_sha256'] = hashlib.sha256(gb).hexdigest()
        if adm_edit is not None:
            adm_edit(a)
        return gb, a

    def each_form(a, form, fn):
        for comp in pre.COMPARISONS:
            if a['admitted'][comp] is not None and a['admitted'][comp][form] is not None:
                fn(a['admitted'][comp][form])

    def raise_C(g):
        g['accepted'] = g['accepted'].replace('q=1/64 and C=' + C, 'q=1/64 and C=1/200000')

    def raise_C_adm(a):
        each_form(a, 'R', lambda f: f.update(c='1/200000', gate_text='q=1/64 and C=1/200000'))

    def q32(g):
        g['accepted'] = g['accepted'].replace('q=1/64 and C=', 'q=1/32 and C=')

    def q32_adm(a):
        a['q_gate_text'] = 'q=1/32'
        each_form(a, 'R', lambda f: f.update(q='1/32', gate_text=f['gate_text'].replace('q=1/64', 'q=1/32')))
        each_form(a, 'Y', lambda f: f.update(q='1/32'))

    def one_sign(g):
        for key in ('accepted', 'decision'):
            g[key] = g[key].replace('Constants (exact; both signs;', 'Constants (exact; +tau;').replace(
                'at both signs, in each on-site cutoff space', 'at +tau, in each on-site cutoff space')

    def drop(comp):
        return lambda a: a['admitted'].__setitem__(comp, None)

    def drop_region(a):
        for comp in pre.COMPARISONS:
            a['admitted'][comp]['Y'] = None

    def insufficient(g):
        g['verdict'] = 'insufficient'

    specs = [
        ('R_constant_above_hypothesis', dict(gate_edit=raise_C, adm_edit=raise_C_adm), ('verdict', 'insufficient', {'1': 'conditional'})),
        ('q_retuned_to_1_over_32', dict(gate_edit=q32, adm_edit=q32_adm), ('verdict', 'insufficient', {'1': 'conditional'})),
        ('region_form_not_admitted', dict(adm_edit=drop_region),
         ('verdict', 'limited', {'1': 'R_only', '2': 'R_only', '3': 'R_marginals', '4': 'R_translate_covariance', '5': 'dropped'})),
        ('c5_general_volume_not_admitted', dict(adm_edit=drop(pre.COMPARISONS[4])), ('verdict', 'limited', {'4': 'dropped', '1': 'full'})),
        ('c3_same_N_not_admitted', dict(adm_edit=drop(pre.COMPARISONS[2])),
         ('verdict', 'limited', {'2': 'conditional', '3': 'per_family', '5': 'per_family'})),
        ('c1_c2_nested_and_c4_not_admitted', dict(adm_edit=lambda a: [drop(pre.COMPARISONS[i])(a) for i in (0, 1, 3)]),
         ('verdict', 'insufficient', {'1': 'conditional'})),
        ('c4_only_dropped_forward_route_suffices', dict(adm_edit=drop(pre.COMPARISONS[3])),
         ('verdict', 'accepted_within_scope', {'1': 'full', '5': 'full'})),
        ('minus_sign_not_admitted', dict(adm_edit=lambda a: a.update(signs=['+'])),
         ('verdict', 'limited', {k: 'conditional' for k in '12345'})),
        ('gate_verdict_insufficient', dict(gate_edit=insufficient, adm_edit=lambda a: a.update(verdict='insufficient')),
         ('verdict', 'insufficient', {k: 'conditional' for k in '12345'})),
        ('both_signs_claimed_beyond_gate', dict(gate_edit=one_sign), ('refused', 'not anchored in the BB1 gate text: signs')),
        ('smaller_constant_not_anchored', dict(adm_edit=lambda a: a['admitted'][pre.COMPARISONS[0]]['R'].update(
            c=a['admitted'][pre.COMPARISONS[0]]['R']['also_certified_by']['c'])), ('refused', 'admitted constant not anchored')),
        ('region_shape_without_exponential', dict(adm_edit=lambda a: a['admitted'][pre.COMPARISONS[0]]['Y'].update(Y_exp_rate='0')),
         ('refused', 'shape differs from the gate text')),
        ('R_shape_text_on_region_entry', dict(adm_edit=lambda a: a['admitted'][pre.COMPARISONS[1]]['Y'].update(
            shape_text='differ by at most C q^(N-1) in trace norm')), ('refused', 'shape text does not fix a bound of this form')),
        ('gate_edited_sha_not_rebound', dict(gate_edit=lambda g: g.update(decision=g['decision'] + ' '), rebind=False),
         ('refused', 'admission record does not match the BB1 gate')),
        ('comparison_label_swapped', dict(adm_edit=lambda a: a['admitted'][pre.COMPARISONS[3]].update(
            gate_scope_text='c5 two finite complete-factor volumes of one prescription containing Lambda_N compared directly')),
         ('refused', 'comparison label differs')),
        ('bb1_contract_comparison_text_changed', dict(adm_edit=lambda a: a['admitted'][pre.COMPARISONS[1]].update(
            bb1_contract_comparison='F2 on Lambda_N versus F2 on Lambda_{N+2}')), ('refused', 'comparison label differs')),
        ('secondary_q_off_the_cap', dict(adm_edit=lambda a: a['secondary_labelled'].update(q_at_cap='1/600')),
         ('refused', 'secondary q differs')),
        ('regime_claimed_beyond_gate', dict(adm_edit=lambda a: a.update(regimes=['Q_L', 'untruncated', 'thermodynamic'])),
         ('refused', 'signs or regimes claimed beyond the gate text')),
    ]
    rows = []
    for name, kw, want in specs:
        gb, a = variant(**kw)
        try:
            rec = read_admission(gb, a, bb1_comparisons, ref)
            out = engine(rec, rec['admitted'], hyp)
        except ReviewFailure as exc:
            if want[0] != 'refused' or want[1] not in str(exc):
                raise ReviewFailure('discharge control %s: refused for the wrong reason: %s' % (name, exc))
            rows.append({'control': name, 'outcome': 'refused', 'reason': str(exc)})
            continue
        if want[0] != 'verdict' or out['verdict'] != want[1] or any(out['items'][k] != v for k, v in want[2].items()):
            raise ReviewFailure('discharge control %s: engine returned %s %s' % (name, out['verdict'], out['items']))
        rows.append({'control': name, 'outcome': out['verdict'], 'items': out['items']})
    return rows


# ------------------------------------------------------------ main computation
def run(args):
    ref = reference()
    raw = CONTRACT.read_bytes()
    con = json.loads(raw)
    need(sha(CONTRACT) == CONTRACT_SHA and sha(BB1_CONTRACT) == BB1_CONTRACT_SHA, 'contracts_pinned',
         bb2=CONTRACT_SHA, bb1=BB1_CONTRACT_SHA)
    template = ref['template']

    # 1. the pre-comparison package is unchanged and replays byte for byte
    fr = json.loads(PRE_FREEZE.read_text())
    unchanged = fr['contract_sha256'] == CONTRACT_SHA and all(sha(ROOT / p) == h for p, h in fr['files'].items())
    rep = replay(PRE_SCRIPT, bool(sys.flags.optimize))
    need(unchanged and rep == {'results.json': sha(PRE_RESULTS)}, 'pre_comparison_package_unchanged_and_replayed',
         files=sorted(fr['files']), commits=COMMITS,
         commit_order='forward d05efda (00:10:26) before the skeptic package 8921539 (00:14:56) before the reverse 17c0ecf '
                      '(00:18:36); the skeptic read no producer file before its commit (disclosure); the forward could not '
                      'have read the package, which did not exist when it committed')

    # 2. closures, inventories, replays, pinned artifacts
    closures = {}
    for side in ('forward', 'reverse'):
        ok, inputs, snap_eq, fz = verify_closure(side)
        declared = sorted(['AGENTS.md', 'research/round33/contracts/bb2.json'] + list(con['shared_premises']))
        closures[side] = {'closure_ok': ok, 'inputs': len(inputs), 'inputs_equal_declared': inputs == declared,
                          'inputs_equal_recorded_before_production': inputs == sorted(pre.OBSERVED_INPUTS),
                          'snapshots_byte_identical': snap_eq,
                          'bb1_snapshot_sha256': sha(SIDES[side] / 'inputs/research/round33/contracts/bb1.json'),
                          'frozen_artifacts_pinned': all(sha(SIDES[side] / p) == h for p, h in FROZEN[side].items())}
    rev_inputs = [p.relative_to(REV / 'inputs').as_posix() for p in (REV / 'inputs').rglob('*') if p.is_file()]
    isolation_ok = not any(p.startswith(pre_) for p in rev_inputs for pre_ in pre.ISOLATION_FORBIDDEN_PREFIXES)
    need(all(v['closure_ok'] and v['inputs'] == 38 and v['inputs_equal_declared'] and v['inputs_equal_recorded_before_production']
             and v['snapshots_byte_identical'] and v['bb1_snapshot_sha256'] == BB1_CONTRACT_SHA and v['frozen_artifacts_pinned']
             for v in closures.values()) and isolation_ok, 'closures_inventories_isolation', closures=closures,
         reverse_isolation='inventory = AGENTS.md + contract + 36 shared premises; no triage, plan, deliberation, lens file, '
                           'proposal, BB contract review, forward file or BB1 producer, skeptic or gate file',
         name_only_exposures={'forward': 'saw the untracked names research/round33/reverse/bb2/check.py and '
                                         'research/round33/skeptic/bb2_check.py after its first freeze; opened neither',
                              'reverse': 'saw the untracked names research/round33/forward/bb1/check.py and '
                                         'research/round33/skeptic/bb1_check.py after its first freeze; opened neither',
                              'assessment': 'name-only; every value was fixed before the listing (disclosed); the BB2 state '
                                            'constants are determined by the frozen contract, so no numeric channel exists'})
    replays = {}
    for side in ('forward', 'reverse'):
        recorded = {p.relative_to(SIDES[side] / 'output').as_posix(): sha(p)
                    for p in sorted((SIDES[side] / 'output').rglob('*')) if p.is_file()}
        replays[side] = {'normal': replay(SIDES[side] / 'check.py', False) == recorded,
                         'optimized': replay(SIDES[side] / 'check.py', True) == recorded}
    need(all(v['normal'] and v['optimized'] for v in replays.values()), 'producer_replays_byte_identical', replays=replays)

    # 3. headline values against the independent recomputation
    results = {side: json.loads((SIDES[side] / 'output/results.json').read_text()) for side in SIDES}
    n_pairs = {side: validate_producer_values(results[side], side, ref) for side in SIDES}
    fw, rv, tg = ref['forward'], ref['reverse'], ref['targets']
    lemma = all(n ** 3 - 10 * n ** 2 + 28 * n + 6 == n * (n - 5) ** 2 + 3 * n + 6 for n in range(0, 50)) \
        and all(2 * (r_N(n) - 1) <= n - 3 for n in range(5, 4000)) \
        and all(F((5 * n + 1) * (r_N(n) - 1)) <= F(n ** 3, 4) for n in range(5, 4000))
    need(lemma and fw['C_dyn'] == F(78057, 622883200000000) and fw['C_dyn'] >= 2 * ref['K']['c2_rev']
         and all(x <= tg['C_dyn'] for x in (fw['C_dyn'], rv['C_dyn_F1'], rv['C_dyn_F2']))
         and fw['C_prime'] <= tg['C_prime'] and fw['c_site_prime'] <= tg['c_site_prime'] and rv['C_prime'] <= tg['C_prime']
         and fw['C_prime_2'] <= tg['C_prime_2'] and F(9500) <= fw['C_dyn_ratio'] <= F(10500)
         and F(9500) <= rv['C_dyn_F2_ratio'] <= F(10500), 'headlines_match_independent_values',
         compared_values=n_pairs,
         forward={'C_prime': q(fw['C_prime']), 'c_site_prime': q(fw['c_site_prime']), 'C_dyn': q(fw['C_dyn']),
                  'C_dyn_preview': preview(fw['C_dyn']), 'C_dyn_F1': q(fw['C_dyn_F1']), 'C_dyn_margin': preview(tg['C_dyn'] / fw['C_dyn'], 6),
                  'C_dyn_ratio': q(fw['C_dyn_ratio']), 'secondary': [q(fw['C_prime_2']), q(fw['c_site_prime_2'])]},
         reverse={'C_prime': q(rv['C_prime']), 'c_site_prime': q(rv['c_site_prime']), 'C_dyn_F1': q(rv['C_dyn_F1']),
                  'C_dyn_F2': q(rv['C_dyn_F2']), 'C_dyn_F2_preview': preview(rv['C_dyn_F2'])},
         lemma_F08='(5N+1)(r_N-1) <= (5N+1)(N-3)/2 <= N^3/4 because N^3-10N^2+28N+6 = N(N-5)^2+3N+6 > 0 (skeptic identity; '
                   'the forward used g(5)=21 and g\'>=3)',
         predictions='C\', c\'_site, C\'_2, c\'_2 and the reverse C_dyn values equal the pre-comparison predictions exactly; the '
                     'forward C_dyn is a valid assembly between the pre-comparison refined (72/343) and unrefined (11/8) inner-F1 '
                     'values and above the floor 2K_c2_rev')

    # 4. item-5 rate: independent certification of the range and of vacuity
    l2 = ln2_enclosure()
    e_lo, e_hi = pre.exp_enclosure(F(1))
    e_ok = E_LO_SK < e_lo and e_hi < E_UP_SK and l2[1] - l2[0] < F(1, 10 ** 40)
    g5_up = 625 * pre.e_region_hi(125) / 8 ** 6
    # envelope g(x) = x^4 e^{x^3/10^8} 8^{-(x+1)}: phi=d ln g/dx = 4/x+3x^2/10^8-ln 8 is convex, phi(5)<0, so g decreases
    # then increases on [5,14000]; hence max g over the range is max(g(5), g(14000)); g(14000) below g(5) exactly:
    phi5_neg = F(4, 5) + F(3 * 25, 10 ** 8) < 1  # < ln 8 since 8 > e
    g14000_small = 14000 ** 4 * 27183 ** 27440 * 8 ** 6 <= 625 * 10000 ** 27440 * 8 ** 14001
    envelope_ok = e_ok and phi5_neg and g14000_small and all((2 * r_N(n) + 1) ** 3 <= n ** 3 and 2 * (n - r_N(n)) >= n + 1 for n in range(5, 14001))
    k5 = {}
    for side, cdyn, csp, cp in (('forward', fw['C_dyn'], fw['c_site_prime'], fw['C_prime']),
                                ('reverse_F1', rv['C_dyn_F1'], rv['c_site_prime'], rv['C_prime']),
                                ('reverse_F2', rv['C_dyn_F2'], rv['c_site_prime'], rv['C_prime'])):
        k5[side] = 10 * cdyn + csp * g5_up + 10 * cp * ref['q'] ** 4
    dyn_ratio_ok = all(n <= 10 * (r_N(n) - 1) for n in range(5, 14001))
    rev_k5 = {fam: rat(results['reverse']['headline']['item5_K5_certified_5_to_14000'][fam]) for fam in ('F1', 'F2')}
    vac = {}
    for side, csp in (('forward', fw['c_site_prime']), ('reverse', rv['c_site_prime'])):
        vac[side] = {'14419': vacuous_at(14419, csp, l2), '14420': vacuous_at(14420, csp, l2), '14421': vacuous_at(14421, csp, l2),
                     '14417_below_2': region_below_two(14417, csp, l2), '14418_below_2': region_below_two(14418, csp, l2)}
        # every N >= 14421: lower envelope h(x)=c'(x-1)^3 e^{(x-1)^3/10^8} 64^{-(x/2+1)} increases for x>=14421 and h(14421)>=2
        lam = 14420 ** 3
        m = ln_lower_integer(csp * lam)
        h_ok = m + F(lam, 10 ** 8) - (F(14421, 2) + 1) * 6 * l2[1] >= l2[1]
        mono = 14420 ** 2 >= 10 ** 8 * l2[1]   # (x-1)^2 >= 10^8 ln 2 makes d ln h/dx = 3/(x-1)+3(x-1)^2/10^8-3 ln 2 positive
        vac[side]['all_N_from_14421'] = h_ok and mono
    fwd_report = (FWD / 'report.md').read_text()
    fwd_overclaim = ('the state terms decay geometrically in' in fwd_report.replace('\n', ' ')
                     and '**Rate.** The rate in `N` is `O(1/N)`' in fwd_report)
    fwd_enclosure_radius = (2 * r_N(464) + 1) ** 3 < 10 ** 8 <= (2 * r_N(465) + 1) ** 3
    need(envelope_ok and dyn_ratio_ok and all(k5[s] <= rev_k5['F1'] for s in ('reverse_F1',)) and k5['reverse_F2'] <= rev_k5['F2']
         and all(all(v.values()) for v in vac.values()) and fwd_overclaim and fwd_enclosure_radius,
         'item5_rate_range_and_vacuity_independent',
         certified_range='5<=N<=14000: N*bracket <= K5 = 10 C_dyn + c_site*g(5) + 10 C_prime q^4 (skeptic envelope; the reverse '
                         'certifies the same range by integer blocks with larger K_reg)',
         K5_skeptic={k: preview(v) for k, v in k5.items()}, K5_reverse={k: preview(v) for k, v in rev_k5.items()},
         vacuity=vac, vacuity_method='ln(region) >= m + |Lambda_r|/10^8 - (N-r) 6 ln2_up with E_UP^m <= c_site|Lambda_r| and a '
                                   '140-term series enclosure of ln 2; for all N >= 14421 a monotone lower envelope',
         forward_overclaim={'quoted': "The rate in N is O(1/N): ... while the state terms decay geometrically in N (the cube volume "
                                      "grows only like N^3)",
                            'finding': 'false for N >= 14419 (odd) and every N >= 14421: e^{|Lambda_rN|/10^8} with |Lambda_rN| ~ N^3 '
                                       'beats q^(N-r_N); the forward checker evaluates only N <= 59 and its enclosure e^x <= 1/(1-x) '
                                       'is invalid from N=465'},
         honest_statement='the item-5 inequality holds for every N >= 5; it gives |c^{F,N}-c^inf| <= K5/N ||A||^2 on 5<=N<=14000; '
                          'the bracket exceeds the trivial bound 2 for N=14419, 14420 and every N>=14421; the correlation functions '
                          'converge along the whole sequence for every N without a rate (fixed-r argument, reverse Corollary 8.6)')

    # 5. text: phrase rule, template span, verbatim quotation blocks
    ns = NS_EXCERPT.read_text()
    text_rows = {}
    for side in SIDES:
        rep_text = (SIDES[side] / 'report.md').read_text()
        hits = pre.affirmative_hits(rep_text, ref['forbidden'], template)
        lines = [ln for ln in rep_text.splitlines() if template in ln]
        blocks = re.findall(r'```text\n(.*?)```', rep_text, re.S)
        block_lines = [ln for b in blocks for ln in b.splitlines() if ln.strip()]
        text_rows[side] = {'affirmative_hits': hits, 'template_count': rep_text.count(template), 'template_lines': len(lines),
                           'quoted_block_lines': len(block_lines),
                           'quoted_lines_verbatim': all(ln in ns for ln in block_lines)}
    need(all(r['affirmative_hits'] == [] and r['template_count'] == 1 and r['template_lines'] == 1 and r['quoted_lines_verbatim']
             and r['quoted_block_lines'] > 0 for r in text_rows.values()), 'report_text_checks', text=text_rows,
         note='the round phrase rule is mirrored (bb2_check affirmative_hits with the round list and the contract list); the '
              'tool run itself is recorded in bb2-replays.json')

    # 6. gate-field blocks before and after the discharge
    gf = ref['gate_fields']
    dep = ['whole_sequence_claimed', 'common_limit_claimed', 'state_convergence_claimed', 'translation_invariance_claimed',
           'rate_in_N_claimed']
    rf, ff = results['reverse'], results['forward']
    rev_ok = rf['gate_fields_after_discharge'] == gf and all(rf['gate_fields'][k] is False for k in dep) \
        and rf['gate_fields']['dynamics_level'] != 'correlation_functions_compact_window'
    fwd_ok = ff['gate_fields'] == gf and all(ff['gate_fields_if_undischarged'][k] is False for k in dep) \
        and not str(ff['gate_fields_if_undischarged']['dynamics_level']).startswith('correlation') \
        and ff['gate_fields_status'].startswith('proposed')
    need(rev_ok and fwd_ok, 'gate_field_blocks',
         reverse='top level = before the discharge (dependent fields false; dynamics_level algebraic_heisenberg_compact_window); '
                 'gate_fields_after_discharge = the contract values',
         forward='top level = the contract values labelled proposed; gate_fields_if_undischarged = dependent fields false and '
                 'dynamics_level not set (non-blocking presentation difference from gate_fields_rule)')

    # 7. source-edit runs
    runs = []
    for side, table in (('forward', FWD_WEAK), ('reverse', REV_WEAK)):
        ids = [cid for cid, _, _ in table]
        if sorted(ids) != sorted(json.loads(CONTRACT.read_text())['controls']) or len(ids) != 34:
            raise ReviewFailure('weakening table does not cover the 34 controls: ' + side)
        for cid, edits, label in table:
            rc, res_bytes, last = mutated_run(side, edits=edits)
            want = 'damaging mutation accepted: ' + label
            if rc == 0 or want not in last:
                raise ReviewFailure('weakening did not produce the expected abort: %s %s -> %s' % (side, cid, last[-200:]))
            runs.append({'kind': 'weakening', 'producer': side, 'control': cid, 'expected': want, 'abort': last[-200:]})
    for side, name, kw, want in MUST_ABORT:
        rc, res_bytes, last = mutated_run(side, **kw)
        if rc == 0 or want not in last:
            raise ReviewFailure('must-abort edit not caught: %s %s -> %s' % (side, name, last[-200:]))
        runs.append({'kind': 'must_abort', 'producer': side, 'edit': name, 'expected': want, 'abort': last[-200:]})
    for side in ('forward', 'reverse'):
        rc, res_bytes, last = mutated_run(side)
        if rc != 0 or hashlib.sha256(res_bytes).hexdigest() != FROZEN[side]['output/results.json']:
            raise ReviewFailure('unmutated copy does not reproduce the frozen results: ' + side)
        runs.append({'kind': 'unmutated_copy', 'producer': side, 'results_sha256': FROZEN[side]['output/results.json']})
    for side, name, kw, want in SILENT:
        rc, res_bytes, last = mutated_run(side, **kw)
        if rc != 0 or res_bytes is None:
            runs.append({'kind': 'silent_or_abort', 'producer': side, 'edit': name, 'caught_by': 'producer checker', 'abort': last[-160:]})
            continue
        try:
            validate_producer_values(json.loads(res_bytes), side, ref)
        except Rejected as exc:
            if want not in str(exc):
                raise ReviewFailure('silent edit caught for the wrong reason: %s %s: %s' % (side, name, exc))
            runs.append({'kind': 'silent', 'producer': side, 'edit': name, 'caught_by': 'skeptic value validator', 'reason': str(exc)})
            continue
        raise ReviewFailure('silent edit passed both the producer checker and the skeptic validator: %s %s' % (side, name))
    validator_caught = {side: sum(1 for r in runs if r['kind'] == 'silent' and r['producer'] == side) for side in SIDES}
    need(all(v >= 1 for v in validator_caught.values()), 'source_edit_runs', runs=runs,
         weakenings=sum(1 for r in runs if r['kind'] == 'weakening'), silent_caught_by_skeptic_validator=validator_caught,
         must_abort=sum(1 for r in runs if r['kind'] == 'must_abort'),
         silent=sum(1 for r in runs if r['kind'].startswith('silent')))

    # 8. discharge (stage 2): the BB1 gate, the anchored admission record, the BB1 review table, the producers' maps
    pins = {'bb1_gate': sha(BB1_GATE) == BB1_GATE_SHA, 'admission': sha(ADMISSION) == ADMISSION_SHA,
            'bb1_review': sha(BB1_REVIEW) == BB1_REVIEW_SHA, 'jung_assistant_2': sha(JUNG_A2) == JUNG_A2_SHA}
    if not all(pins.values()):
        raise ReviewFailure('stage-2 input differs from its pinned sha256: ' + ', '.join(k for k, v in pins.items() if not v))
    bb1_comparisons = json.loads(BB1_CONTRACT.read_text())['parameters']['comparisons']
    gate_bytes = BB1_GATE.read_bytes()
    adm = json.loads(ADMISSION.read_text())
    discharge = discharge_stage(gate_bytes, adm, json.loads(BB1_REVIEW.read_text()), json.loads(JUNG_A2.read_text()), ref,
                                results, bb1_comparisons, con)
    ok = discharge.pop('_ok')
    need(ok, 'bb1_discharge', pinned={'bb1_gate': BB1_GATE_SHA, 'admission': ADMISSION_SHA, 'bb1_review': BB1_REVIEW_SHA,
                                       'jung_assistant_2': JUNG_A2_SHA},
         verdict=discharge['bb2_verdict_from_discharge'], items=discharge['protocol']['items'],
         forward_map={k: v['status'] for k, v in discharge['producer_maps']['forward'].items()},
         reverse_map={k: v['status'] for k, v in discharge['producer_maps']['reverse'].items()},
         secondary=discharge['secondary_labelled']['verdict'],
         iterated_split_alternative=discharge['iterated_split_alternative_labelled']['verdict'],
         bb1_review_cells_equal=discharge['bb1_review_cross_check']['cells_equal'],
         item5_first_exceedance=14419, gate_fields_equal_contract=discharge['gate_fields_equal_contract'])
    controls = discharge_controls(gate_bytes, adm, ref, bb1_comparisons)
    outcomes = [r['outcome'] for r in controls]
    need(len(controls) == 18 and outcomes.count('refused') == 9 and outcomes.count('accepted_within_scope') == 1,
         'discharge_controls', controls=controls, refused=outcomes.count('refused'),
         downgraded=sum(1 for o in outcomes if o in ('limited', 'insufficient')),
         accepted=outcomes.count('accepted_within_scope'),
         note='in-memory edits of the gate and the admission record (packet hash rebound unless stated); the engine must '
              'refuse the record or return the stated verdict and item statuses')

    return {
        'loop': 'BB2', 'stage': 'post_comparison_with_discharge',
        'reviewer': 'skeptic (model agent, correlated ancestry)', 'human_author': 'Hruday N M (BUNZEEY)',
        'contract_sha256': CONTRACT_SHA, 'bb1_contract_sha256': BB1_CONTRACT_SHA, 'bb1_gate_sha256': BB1_GATE_SHA,
        'binding_recommendation': {
            'C_prime': q(fw['C_prime']) + ' (forward, nested telescoping, evaluated at the hypothesis value C_h; valid under '
                       'the discharge because the admitted C is below C_h); labelled second route ' + q(rv['C_prime'])
                       + ' (reverse, direct comparison)',
            'c_site_prime': q(fw['c_site_prime']) + ' (forward); labelled second route ' + q(rv['c_site_prime']) + ' (reverse)',
            'C_dyn': q(fw['C_dyn']) + ' (forward, 2K_F1+K_cmp/4, duhamel_inner_f1, one constant for both families); labelled '
                     'second route per family ' + q(rv['C_dyn_F1']) + ' (F1, duhamel_inner_f1) and ' + q(rv['C_dyn_F2'])
                     + ' (F2, duhamel_inner_f2)',
            'secondary': q(fw['C_prime_2']) + ' and ' + q(fw['c_site_prime_2']) + ' at q_2=151552|tau| (forward; labelled)',
            'item4': 'C_h q^(N-|v|_inf-1) (direct general-volume comparison c5, both routes); union two-step labelled only',
            'bb1_route_of_bound_value': 'polymer_kp for C and c_site; iterated_split for the secondary pair (BB1 gate)',
            'reevaluated_at_admitted_values': 'labelled only (discharge.constants)'},
        'discharge': discharge,
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
    print(json.dumps({'checks': len(result['checks']), 'stage': result['stage'],
                      'discharge': result['discharge']['bb2_verdict_from_discharge'],
                      'source_edit_runs': [c for c in result['checks'] if c['id'] == 'source_edit_runs'][0]['weakenings']}))


if __name__ == '__main__':
    main()
