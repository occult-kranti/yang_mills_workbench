#!/usr/bin/env python3
"""BB2 post-comparison skeptic checks (stage 1: producers; discharge part: the BB1 gate).

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
The discharge part needs --bb1-gate and --bb1-admission (the skeptic's transcription of the gate's admitted constants,
each anchored to a verbatim gate substring) and applies the pre-registered protocol (bb2_check.discharge); without them it
is not run and says so.

Standard library only; exact Fractions decide every Boolean; failures are explicit exceptions (never assert), so the
output bytes match under python -O.

Usage: python3 -B research/round33/skeptic/bb2_postreview_check.py --output /abs/fresh/dir
       [--bb1-gate research/round33/advisor/bb1-gate.json --bb1-admission research/round33/skeptic/bb2-bb1-admission.json]
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


# ------------------------------------------------------------ discharge part
def discharge_stage(gate_path, admission_path, ref):
    gate_bytes = Path(gate_path).read_bytes()
    gate_sha = hashlib.sha256(gate_bytes).hexdigest()
    gate = json.loads(gate_bytes)
    adm = json.loads(Path(admission_path).read_text())
    if gate.get('loop') != 'BB1':
        raise ReviewFailure('the supplied gate is not the BB1 gate')
    if adm.get('bb1_gate_sha256') != gate_sha or adm.get('verdict') != gate.get('verdict'):
        raise ReviewFailure('admission record does not match the BB1 gate (sha256 or verdict)')
    text = ' '.join([str(gate.get('accepted', '')), str(gate.get('decision', '')), ' '.join(gate.get('limitations', []))])
    text_n = re.sub(r'\s+', ' ', text)
    admitted = {}
    anchors = 0
    for comp in pre.COMPARISONS:
        forms = (adm.get('admitted') or {}).get(comp)
        if forms is None:
            admitted[comp] = None
            continue
        admitted[comp] = {}
        for form in ('R', 'Y'):
            e = forms.get(form)
            if e is None:
                admitted[comp][form] = None
                continue
            anchor = re.sub(r'\s+', ' ', e['gate_text'])
            if anchor not in text_n or e['c'] not in anchor:
                raise ReviewFailure('admitted constant not anchored in the BB1 gate text: %s %s' % (comp, form))
            anchors += 1
            admitted[comp][form] = {'c': F(e['c']), 'shape': {'q': F(e['q']), 'exponent_shift': int(e['exponent_shift']),
                                                              'Y_power': int(e['Y_power']), 'Y_exp_rate': F(e['Y_exp_rate'])}}
    record = {'verdict': gate['verdict'], 'admitted': admitted, 'regimes': list(adm['regimes']), 'signs': list(adm['signs'])}
    hyp = {'q': ref['q'], 'const': {'R': ref['C_h'], 'Y': ref['c_h']},
           'shape': {'R': {'q': ref['q'], 'exponent_shift': 0, 'Y_power': 0, 'Y_exp_rate': F(0)},
                     'Y': {'q': ref['q'], 'exponent_shift': 0, 'Y_power': 1, 'Y_exp_rate': F(1, 10 ** 8)}}}
    res = pre.discharge(record, hyp, cutoff_routes=tuple(adm.get('routes_with_own_cutoff_removal', ['forward'])))
    reeval = {k: q(v) for k, v in res['reevaluated'].items()}
    c5 = (admitted.get('c5_one_prescription_volumes') or {}).get('R')
    return {'bb1_gate_sha256': gate_sha, 'bb1_verdict': gate['verdict'], 'anchored_constants': anchors,
            'items': res['items'], 'items_by_sign': res['items_by_sign'], 'bb2_verdict_from_discharge': res['verdict'],
            'unconditional': res['unconditional'], 'gate_fields': res['gate_fields'], 'reevaluated_constants': reeval,
            'item4_constant_reevaluated': q(c5['c']) if c5 else None,
            'bb1_route_of_bound_value': adm.get('bb1_route_of_bound_value'),
            'rule': 'unconditional only when, at both signs, some BB2 route proves the item from BB1 comparisons admitted at q=1/64 '
                    'with a bound dominated pointwise by the hypothesis form and a constant at most the hypothesis value'}


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

    # 8. discharge part
    if args.bb1_gate is None and args.bb1_admission is None:
        discharge = {'status': 'not run: the BB1 gate is not yet supplied (stage 1); run with --bb1-gate and --bb1-admission'}
    elif args.bb1_gate is None or args.bb1_admission is None:
        raise SystemExit('the discharge part needs both --bb1-gate and --bb1-admission')
    else:
        discharge = discharge_stage(args.bb1_gate, args.bb1_admission, ref)
        need(True, 'bb1_discharge', **discharge)

    return {
        'loop': 'BB2', 'stage': 'post_comparison_stage_1' if 'status' in discharge else 'post_comparison_with_discharge',
        'reviewer': 'skeptic (model agent, correlated ancestry)', 'human_author': 'Hruday N M (BUNZEEY)',
        'contract_sha256': CONTRACT_SHA, 'bb1_contract_sha256': BB1_CONTRACT_SHA,
        'binding_recommendation': {
            'C_prime': q(fw['C_prime']) + ' (forward, nested telescoping; valid under either discharge because it dominates C_h); '
                       'labelled second route ' + q(rv['C_prime']) + ' (reverse, direct nested comparison)',
            'c_site_prime': q(fw['c_site_prime']) + ' (forward); labelled second route ' + q(rv['c_site_prime']) + ' (reverse)',
            'C_dyn': q(fw['C_dyn']) + ' (forward, 2K_F1+K_cmp/4, duhamel_inner_f1, one constant for both families); labelled '
                     'second route per family ' + q(rv['C_dyn_F1']) + ' (F1, duhamel_inner_f1) and ' + q(rv['C_dyn_F2'])
                     + ' (F2, duhamel_inner_f2)',
            'item4': 'C_h q^(N-|v|_inf-1) (direct general-volume comparison, both routes); union two-step labelled only'},
        'discharge': discharge,
        'checks': CHECKS,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', required=True)
    ap.add_argument('--bb1-gate', default=None)
    ap.add_argument('--bb1-admission', default=None)
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
                      'source_edit_runs': [c for c in result['checks'] if c['id'] == 'source_edit_runs'][0]['weakenings']}))


if __name__ == '__main__':
    main()
