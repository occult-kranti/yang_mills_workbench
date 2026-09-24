#!/usr/bin/env python3
"""AW1 post-comparison skeptic checks, written after both producer freezes.

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated
ancestry (same model family as the advisor, the lenses and both producers); not
human peer review or formal verification.

What this adds to the frozen pre-comparison package (aw1_check.py, 79 checks):
  * an exact re-derivation of the first-order coefficient +tau/144 by three
    routes (AV1 creation-sign chain, two-level Rayleigh-Ritz in alpha units, the
    one-plaquette Rayleigh-Schroedinger series), of the contract display's
    literal value -tau/144 (a wording defect), and of both producers' signed
    first-order values;
  * the three exact-tier K_2^+ itemizations (forward, reverse, skeptic) term by
    term in exact Fractions, compared with each producer's exported rationals,
    each checked term by term against a minimal itemization the skeptic accepts
    (so each is a valid upper bound), their ordering and the source of every
    difference; the crude tier; the omega(W^2) supplementary constants;
  * the frozen AW2 decade-grid rule for every valid exact-tier value, the exact
    sign margins, the robustness threshold and the AV1 compatibility;
  * the flip-set combinatorics: odd intersection, the two one-coordinate rules
    and their center-gauge relation, the selected-face cocycle condition, both
    producers' selected-even cochains E'' and the modified set E*=E xor E'',
    and an exact 3x3 compression showing what E* does and U_E does not do;
  * parity cross-checks (Haar moments, energy content of W_f W Omega_0, odd-set
    sizes over the Lambda_2 box) and the enumeration pins;
  * both producers' claim flags, all 30 controls and their contract bindings;
  * source-edit mutations: each producer closure is copied to a temporary tree
    outside the checkout and edited once; every must-abort edit has to abort,
    an unmutated copy has to reproduce the frozen results.json byte for byte, and
    four silent value edits (not caught by the producer checkers, which only
    compute their own formulas) have to be caught by this review's term-by-term
    validator.

Standard library only; exact Fractions decide every Boolean; failures are explicit
exceptions (never assert), so the output bytes match under python -O.

Usage: python3 -B research/round32/skeptic/aw1_postreview_check.py --output /abs/fresh/dir
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
from pathlib import Path

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
R32 = ROOT / 'research/round32'
CONTRACT = R32 / 'contracts/aw1.json'
CONTRACT_SHA = 'c24bf7eb6a1c24034427c810a9c26c4c86d1f9c1d31b0fe36ea4cf2a796814ef'
AV1_GATE = R32 / 'advisor/av1-gate.json'
SELECTION = R32 / 'advisor/selection-aw1.md'
LOOP3_SKEPTIC = R32 / 'skeptic/loop3-signoff.md'
I1_REPORT = ROOT / 'research/round21/forward/i1/report.md'
FWD = R32 / 'forward/aw1'
REV = R32 / 'reverse/aw1'
PRE_RESULTS = HERE / 'aw1-independent/results.json'
PRE_FREEZE = HERE / 'aw1-independent-freeze.json'
TERMS = ('am2_remainder', 'straddling', 'two_creation', 'density', 'normalization_order')
REV_TERM = {'normalization_order': 'normalization'}


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


def ceil_to(x, den):
    x = F(x)
    return F(-((-x.numerator * den) // x.denominator), den)


def floor_to(x, den):
    x = F(x)
    return F((x.numerator * den) // x.denominator, den)


# ------------------------------------------------------------ geometry (I1.1, I1.4)
DIRS = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIENT = (('xy', 0, 1), ('xz', 0, 2), ('yz', 1, 2))
OFFSETS = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}
ORIGIN, EZ = (0, 0, 0), (0, 0, 1)
COVER = frozenset([ORIGIN, EZ])


def add(p, v):
    return (p[0] + v[0], p[1] + v[1], p[2] + v[2])


def sub(p, v):
    return (p[0] - v[0], p[1] - v[1], p[2] - v[2])


def coarse(v):
    return (v[0] // 4, v[1] // 2, v[2])


def face_links(p, a, c):
    return ((p, a), (add(p, DIRS[a]), c), (add(p, DIRS[c]), a), (p, c))


def is_selected(p, a, c):
    return (a, c) == (0, 1) and p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)


def anchored_faces(b):
    out = []
    for r in range(4):
        for s in range(2):
            p = (4 * b[0] + r, 2 * b[1] + s, b[2])
            for name, a, c in ORIENT:
                links = face_links(p, a, c)
                out.append({'key': (name, r, s), 'base': p, 'a': a, 'c': c, 'anchor': b,
                            'selected': is_selected(p, a, c), 'links': frozenset(links),
                            'owners': frozenset(coarse(t) for t, _ in links)})
    return out


def parse_i1_table(text):
    row = re.compile(r'^\|\s*(xy|xz|yz):\s*r=([0-9,]+);\s*s=([0-9,]+)\s*\|\s*(\d+)\s*\|'
                     r'\s*`\{([^}]*)\}`\s*\|\s*(selected|omitted)\s*\|\s*$')
    classes = {}
    for line in text.splitlines():
        m = row.match(line.strip())
        if not m:
            continue
        support = frozenset(OFFSETS[x.strip()] for x in m.group(5).split(','))
        for r in (int(x) for x in m.group(2).split(',')):
            for s in (int(x) for x in m.group(3).split(',')):
                classes[(m.group(1), r, s)] = (support, m.group(6))
    return classes


# ------------------------------------------------------------ SU(2) characters
def tensor_power(n):
    """Multiplicity of spin j (key 2j) in (1/2)^{(x)n}, Clebsch-Gordan."""
    cf = {0: 1}
    for _ in range(n):
        new = {}
        for tj, m in cf.items():
            for nt in (tj - 1, tj + 1):
                if nt >= 0:
                    new[nt] = new.get(nt, 0) + m
        cf = new
    return cf


def moment(n):
    return F(tensor_power(n).get(0, 0), 2 ** n)


def link_counts(faces):
    cnt = {}
    for f in faces:
        for l in f:
            cnt[l] = cnt.get(l, 0) + 1
    return cnt


def haar_vanishes(faces):
    return any(k % 2 == 1 for k in link_counts(faces).values())


def energies(faces):
    """Normalized H_0 energies 8 sum j(j+1) present in prod W_f Omega_0 (per-link CG content)."""
    opts = []
    for _, k in sorted(link_counts(faces).items()):
        opts.append([tj for tj, m in tensor_power(k).items() if m > 0])
    return sorted({sum(2 * tj * (tj + 2) for tj in combo) for combo in product(*opts)})


def plaquette_series(coef, order=5, nmax=10):
    """One gauge-invariant plaquette (finite graph): G=4C+coef*W, W chi_j=(chi_{j-1/2}+chi_{j+1/2})/2.
    Exact Rayleigh-Schroedinger coefficients of <W> and of the ground energy."""
    n = nmax + 1
    e0 = [F(k * (k + 2)) for k in range(n)]

    def wm(v):
        out = [F(0)] * n
        for k in range(n):
            if v[k]:
                if k + 1 < n:
                    out[k + 1] += v[k] / 2
                if k >= 1:
                    out[k - 1] += v[k] / 2
        return out

    def vm(v):
        return [coef * x for x in wm(v)]

    psi, en = [[F(1)] + [F(0)] * (n - 1)], [F(0)]
    for k in range(1, order + 1):
        en.append(vm(psi[k - 1])[0])
        rhs = [-x for x in vm(psi[k - 1])]
        for m in range(1, k + 1):
            rhs = [r + en[m] * p for r, p in zip(rhs, psi[k - m])]
        psi.append([F(0)] + [rhs[i] / (e0[i] - e0[0]) for i in range(1, n)])

    def ip(u, v):
        return sum((x * y for x, y in zip(u, v)), F(0))
    num = [sum((ip(psi[i], wm(psi[k - i])) for i in range(k + 1)), F(0)) for k in range(order + 1)]
    den = [sum((ip(psi[i], psi[k - i]) for i in range(k + 1)), F(0)) for k in range(order + 1)]
    out = []
    for k in range(order + 1):
        out.append((num[k] - sum((out[i] * den[k - i] for i in range(k)), F(0))) / den[0])
    return out, en


# ------------------------------------------------------------ K_2 itemizations
def k2_itemizations(tau_abs):
    a = tau_abs / 144
    J = 28 * tau_abs
    t1 = 49 * a
    T = t1 / (1 - 352 * J)
    rho = 352 * J * T
    eps_f = 2 * T + T * T
    s0 = 33 * a + rho
    s_str = 6 * a + rho
    eps_r = 82 * a + 2 * rho + s0 * s0
    eps_min = min(eps_f, eps_r)
    items = {
        'skeptic': {'am2_remainder': rho, 'straddling': T * T, 'two_creation': T * T,
                    'density': eps_f ** 2, 'normalization_order': a * eps_f ** 2},
        'forward': {'am2_remainder': rho, 'straddling': T * s_str, 'two_creation': s0 * s0,
                    'density': eps_f ** 2, 'normalization_order': a * eps_f ** 2},
        'reverse': {'am2_remainder': rho, 'straddling': T * s_str, 'two_creation': s0 * s0,
                    'density': eps_r ** 2, 'normalization_order': (eps_r + eps_r ** 2) * eps_r ** 2},
        'minimal_accepted': {'am2_remainder': rho, 'straddling': T * s_str, 'two_creation': s0 * s0,
                             'density': eps_min ** 2, 'normalization_order': a * eps_min ** 2},
    }
    inputs = {'a': a, 'J': J, 't1': t1, 'T': T, 'rho': rho, 'eps_2T_T2': eps_f, 'eps_82_face': eps_r,
              's0_33_face': s0, 's_str_6_face': s_str}
    return items, inputs


def k2_crude(tau_abs):
    a = tau_abs / 144
    J = 28 * tau_abs
    t = J * F(148, 7)
    rho = 352 * J * t
    eps = 2 * t + t * t
    base = {'am2_remainder': rho, 'straddling': t * t, 'two_creation': t * t, 'density': eps ** 2}
    return ({'forward_and_skeptic': dict(base, normalization_order=a * eps ** 2),
             'reverse': dict(base, normalization_order=(eps + eps ** 2) * eps ** 2)},
            {'t_crude': t, 'rho': rho, 'eps': eps})


def total(terms):
    return sum((terms[n] for n in TERMS), F(0))


def aw2_rule(K2, start, threshold, steps=60):
    for k in range(start, start + steps):
        tau = F(1, 10 ** k)
        if K2 * tau <= threshold:
            return tau
    raise ReviewFailure('decade grid exhausted')


def validate_producer_k2(results, direction, cap):
    """Term-by-term validator used on mutated producer outputs: every exported exact-tier term
    must be at least the minimal accepted term, and K_2 must equal the itemized sum over tau^2."""
    minimal = k2_itemizations(cap)[0]['minimal_accepted']
    if direction == 'forward':
        rec = results['k2']['exact']['+']
        terms = {n: F(rec['terms'][n]['value']) for n in TERMS}
        K2 = F(rec['K2'])
    else:
        rec = results['ledgers']['exact_plus']
        terms = {n: F(rec['terms'][REV_TERM.get(n, n)]['value']) for n in TERMS}
        K2 = F(rec['K2_exact_rational'])
    for n in TERMS:
        if terms[n] < minimal[n]:
            raise Rejected('%s %s below the minimal accepted itemization' % (direction, n))
    if K2 != total(terms) / (cap * cap):
        raise Rejected('%s K_2 differs from its itemized sum' % direction)
    return K2


# ------------------------------------------------------------ source-mutation replays
def mutated_run(direction, edits=(), extra_input=None, contract_edit=None, rehash=False):
    src = FWD if direction == 'forward' else REV
    with tempfile.TemporaryDirectory(prefix='hnm-r32-aw1-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / 'research/round32' / direction / 'aw1'
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        code = (dst / 'check.py').read_text()
        for old, new in edits:
            if code.count(old) != 1:
                raise ReviewFailure('mutation anchor not unique in %s: %r' % (direction, old[:60]))
            code = code.replace(old, new)
        if contract_edit is not None:
            cpath = dst / 'inputs/research/round32/contracts/aw1.json'
            raw = cpath.read_bytes()
            old, new = contract_edit
            if raw.count(old) < 1:
                raise ReviewFailure('contract mutation anchor missing')
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
    raw = CONTRACT.read_bytes()
    need(sha(CONTRACT) == CONTRACT_SHA, 'contract_hash', contract_sha256=CONTRACT_SHA)
    contract = json.loads(raw)
    pre_freeze = json.loads(PRE_FREEZE.read_text())
    need(all(sha(ROOT / name) == digest for name, digest in pre_freeze['files'].items())
         and pre_freeze['contract_sha256'] == CONTRACT_SHA and pre_freeze['stage'] == 'pre_comparison',
         'pre_comparison_package_unchanged', files=sorted(pre_freeze['files']))
    pre = json.loads(PRE_RESULTS.read_text())
    params = contract['parameters']
    prereg = contract['preregistration']
    cap = F(params['tau_cap'])
    target = F(prereg['target']['value'])
    mrule = re.search(r'decade grid \{10\^-(\d+), 10\^-(\d+), \.\.\.\} with K_2\^\+ \* tau <= (\d+)/(\d+)',
                      params['aw2_coupling_rule'])
    grid_start = int(mrule.group(1))
    threshold = F(int(mrule.group(3)), int(mrule.group(4)))
    mmar = re.fullmatch(r'1/\((\d+) K_2\^\+ tau\) >= (\d+) for accepted; else sign_certified_below_cap via the rule',
                        params['targets']['sign_margin_at_cap'])
    margin_den, margin_min = int(mmar.group(1)), int(mmar.group(2))
    ref = re.fullmatch(r'(\S+) and (\S+)', prereg['observable']['reference_value_exact'])
    ref_W, ref_W2 = F(ref.group(1)), F(ref.group(2))
    need(cap == F(1, 10 ** 8) and target == threshold == F(1, 288) and grid_start == 8 and int(mrule.group(2)) == 9
         and margin_den == 144 and margin_min == 2 and ref_W == 0 and ref_W2 == F(1, 4)
         and params['selected_coefficients_over_alpha'] == ['0', '0', '0'] and params['signs'] == ['+', '-'],
         'frozen_design_read_from_contract', tau_cap=q(cap), target=q(target), rule_grid_start='10^-8',
         sign_margin='1/(144 K_2^+ tau) >= 2', reference=[q(ref_W), q(ref_W2)])
    controls = list(contract['controls'])
    need(len(controls) == 30 and controls == prereg['controls_required']['ids'], 'contract_30_controls_mirror_equal')
    gate = json.loads(AV1_GATE.read_text())
    mD = re.search(r'D_ii=(\d+)/(\d+)', gate['accepted'])
    D_ii = F(int(mD.group(1)), int(mD.group(2)))

    # ---------------- producer outputs and closures
    fr = json.loads((FWD / 'output/results.json').read_text())
    rr = json.loads((REV / 'output/results.json').read_text())
    fch = {c['id']: c for c in fr['checks']}
    rch = {c['id']: c for c in rr['checks']}
    need(len(fr['checks']) == len(fch) == 41 and len(rr['checks']) == len(rch) == 57
         and all(c['passed'] is True for c in fr['checks'] + rr['checks']), 'producer_check_counts_all_passed',
         forward=41, reverse=57)
    ffz = json.loads((FWD / 'freeze.json').read_text())
    rfz = json.loads((REV / 'freeze.json').read_text())
    need(fr['contract_sha256'] == rr['contract_snapshot_sha256'] == ffz['contract_sha256'] == rfz['contract_sha256']
         == CONTRACT_SHA
         and fr['check_py_sha256_recorded_before_evaluation'] == sha(FWD / 'check.py')
         and rr['check_py_sha256'] == sha(REV / 'check.py')
         and all(sha(ROOT / n) == d for n, d in ffz['sources'].items())
         and all(sha(ROOT / n) == d for n, d in rfz['sources'].items()),
         'closures_bound_to_contract_and_checkers', forward_files=len(ffz['sources']), reverse_files=len(rfz['sources']))

    # ---------------- first-order coefficient (item 3)
    c1_norm = F(-1, 3) / 24          # L_0 per face per tau, normalized: phi=-(tau/3)W_f over energy 24
    c1_alpha = F(-1, 24) / 3         # alpha units: V=-(tau/24)W_f over energy 3
    EW2 = moment(2)
    omega1 = -2 * c1_norm * EW2      # psi=e^{-C}Omega_0=Omega_0-c^(1)+...: omega=-2Re<W Omega_0,c^(1)>
    display_literal = 2 * c1_norm * EW2
    h01 = F(-1, 24) * 2 * EW2        # <e, V Omega_0>, e=2W Omega_0 (unit), alpha units, per tau
    eps_star = -h01 / 3
    ritz_mean = 2 * eps_star * (2 * EW2)
    ser, en = plaquette_series(F(-1, 24))
    ser_hi, _ = plaquette_series(F(-1, 24), nmax=14)
    need(c1_norm == c1_alpha == F(-1, 72) and omega1 == F(1, 144) and display_literal == F(-1, 144)
         and ritz_mean == F(1, 144) and ser[:5] == [0, F(1, 144), 0, F(-5, 11943936), 0] and ser_hi[:5] == ser[:5]
         and en[:5] == [0, 0, F(-1, 6912), 0, F(5, 1146617856)],
         'first_order_coefficient_three_routes', c1_per_face=q(c1_norm), omega1=q(omega1),
         contract_display_literal_with_AV1_c1=q(display_literal), rayleigh_ritz_mean=q(ritz_mean),
         one_plaquette_series=[q(x) for x in ser], one_plaquette_energy=[q(x) for x in en],
         labels='one-plaquette fixture is a finite graph; transfers_to_aq false')
    fplus, fminus = F(fr['headline']['omega1_plus']), F(fr['headline']['omega1_minus'])
    rsig = rr['first_order_coefficient']['signed_terms_at_cap']
    need(fplus == cap * omega1 == -fminus and F(rsig[q(cap)]) == cap * omega1 and F(rsig[q(-cap)]) == -cap * omega1
         and F(rr['first_order_coefficient']['value']) == omega1 and fr['headline']['first_order_coefficient'] == '+tau/144'
         and [F(x) for x in fch['sign_convention_fixture']['rs_series_coefficients']] == ser[:5]
         and [F(x) for x in fch['sign_convention_fixture']['rs_energy_coefficients']] == [8 * x for x in en[:5]]
         and [F(x) for x in rch['one_plaquette_exact_flip_and_sign_fixture']['rs_mean_W']] == ser[:6]
         and [F(x) for x in rch['one_plaquette_exact_flip_and_sign_fixture']['rs_energy']] == en[:6],
         'first_order_signed_values_and_fixtures_match_both', plus=q(fplus), minus=q(fminus),
         forward_energy_units='normalized (8x alpha)', reverse_energy_units='alpha')
    # item-3 wording defect: both producers record it
    rev_lit = rch['wilson_mean_first_order_coefficient']['rejected_mutations']['am2_sign_literal']
    need('literal display gives ' + q(display_literal * cap) in fch['wilson_mean_first_order_coefficient']['contract_display_note']
         and 'plus_two_L0_convention_gives_minus_tau_over_144' in fch['wilson_mean_first_order_coefficient']['mutations_rejected']
         and rev_lit.startswith('first-order coefficient ' + q(display_literal) + ' differs')
         and 'contract_formula_with_am2_c1' in rch['sign_convention_fixture']['rejected_mutations'],
         'contract_item3_display_defect_recorded_by_both',
         defect='contract item 3 writes omega=2<W Omega_0,c^(1)>; with the AV1-admitted c^(1)=L_0=-(tau/72)sum W_f Omega_0 '
                'this is -tau/144; the derived value is +tau/144 (c^(1) read as the vector correction psi^(1)=-L_0)')

    # ---------------- parity cross-checks (item 1)
    moments = {n: moment(n) for n in range(9)}
    need([moments[n] for n in range(9)] == [1, 0, F(1, 4), 0, F(1, 8), 0, F(5, 64), 0, F(7, 128)]
         and {k: F(v) for k, v in rch['haar_parity_three_exact_routes']['moments'].items()} == {str(n): moments[n] for n in range(9)}
         and {k: F(v) for k, v in fr['parity_theorem']['moments'].items()} == {str(n): moments[n] for n in range(5)}
         and {k: F(v) for k, v in pre['haar']['character_moments_E_W^n'].items()} == {str(n): moments[n] for n in range(1, 9)},
         'haar_moments_equal_in_all_three_packages', moments={str(n): q(v) for n, v in moments.items()})
    ftz = fr['parity_theorem']
    need(all(F(v) == 0 for k, v in ftz['first_order_terms_bulk_82'].items() if k != 'uncentered_mean_control')
         and all(F(v) == 0 for k, v in ftz['first_order_terms_box_N2'].items() if k != 'uncentered_mean_control')
         and F(ftz['first_order_terms_bulk_82']['uncentered_mean_control']) == omega1,
         'forward_first_order_terms_zero_mean_nonzero')

    # ---------------- enumeration from the I1 table
    table = parse_i1_table(I1_REPORT.read_text())
    geo = {f['key']: (frozenset(sub(o, ORIGIN) for o in f['owners']), 'selected' if f['selected'] else 'omitted')
           for f in anchored_faces(ORIGIN)}
    need(len(table) == 24 and table == geo, 'i1_table_equals_geometry')
    omitted = [v[0] for v in table.values() if v[1] == 'omitted']
    owner_sets = {}
    for s in omitted:
        for o in s:
            key = frozenset(sub(x, o) for x in s)
            owner_sets[key] = owner_sets.get(key, 0) + 1
    mults = sorted(owner_sets.values())
    faces_R = [f for b in product(range(-2, 3), repeat=3) for f in anchored_faces(b)
               if not f['selected'] and f['owners'] & COVER]
    inside = [f for f in faces_R if f['owners'] <= COVER]
    strictly = [f for f in faces_R if COVER < f['owners']]
    straddle = [f for f in faces_R if not f['owners'] <= COVER]
    zero_only = [f for f in faces_R if ORIGIN in f['owners'] and EZ not in f['owners']]
    ez_only = [f for f in faces_R if EZ in f['owners'] and ORIGIN not in f['owners']]
    out_sites = sorted(len(f['owners'] - COVER) for f in straddle)
    W = frozenset(face_links(ORIGIN, 0, 2))
    enum = {'faces_per_factor': sum(len(s) for s in omitted), 'owner_sets': len(owner_sets), 'meet_R': len(faces_R),
            'inside_R': len(inside), 'strictly_containing_R': len(strictly), 'both_R': len(inside) + len(strictly),
            'straddling': len(straddle), 'zero_not_ez': len(zero_only), 'ez_not_zero': len(ez_only),
            'straddling_one_outside': out_sites.count(1), 'straddling_two_outside': out_sites.count(2)}
    fe = fr['enumeration']
    rd = rr['face_enumeration']['derived']
    need(enum == {'faces_per_factor': 49, 'owner_sets': 15, 'meet_R': 82, 'inside_R': 10, 'strictly_containing_R': 6,
                  'both_R': 16, 'straddling': 72, 'zero_not_ez': 33, 'ez_not_zero': 33,
                  'straddling_one_outside': 42, 'straddling_two_outside': 30}
         and mults == [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 10, 10] and fe['multiplicities'] == mults
         and [fe[k] for k in ('faces_per_factor', 'owner_sets', 'meet_R', 'inside_R', 'strictly_containing_R', 'both_R',
                              'straddling', 'zero_not_ez', 'ez_not_zero')]
         == [enum[k] for k in ('faces_per_factor', 'owner_sets', 'meet_R', 'inside_R', 'strictly_containing_R', 'both_R',
                               'straddling', 'zero_not_ez', 'ez_not_zero')]
         and fe['straddling_split_outside_sites'] == [42, 30]
         and [rd[k] for k in ('faces_per_factor', 'owner_sets_per_factor', 'faces_meeting_R', 'faces_inside_R',
                              'faces_strictly_containing_R', 'faces_touching_both', 'straddling_faces',
                              'single_site_faces_at_0', 'single_site_faces_at_e_z')]
         == [49, 15, 82, 10, 6, 16, 72, 33, 33]
         and sum(1 for f in faces_R if f['links'] == W) == 1,
         'enumeration_pins_equal_in_both', counts=enum, multiplicities=mults)
    # wrong-face and W^2 W_f parity over the 82 faces, energy content of W_f W Omega_0
    ww = [(f['links'] == W, haar_vanishes([W, f['links']])) for f in faces_R]
    w2w = [haar_vanishes([W, W, f['links']]) for f in faces_R]
    need(all(v == (not isW) for isW, v in ww) and all(w2w) and moment(3) == 0,
         'wrong_face_and_W2Wf_parity_82', E_W_Wf='1/4 for f=W only', E_W2_Wf='0 for all 82 incl f=W')
    lam2 = [f for b in product(range(-2, 2), repeat=3) for f in anchored_faces(b) if not f['selected']]
    sizes = {}
    en_sets = {}
    for f in lam2:
        k = len(W ^ f['links'])
        sizes[k] = sizes.get(k, 0) + 1
        en_sets.setdefault(k, set()).update(energies([W, f['links']]))
    need(len(lam2) == 1344 and sizes == {0: 1, 6: 10, 8: 1333}
         and {k: sorted(v) for k, v in en_sets.items()} == {0: [0, 16, 32, 48, 64], 6: [36, 52], 8: [48]}
         and {int(k): v for k, v in rch['degenerate_multiplet_zero_first_order_splitting']['odd_set_sizes_of_W_times_Wf'].items()} == sizes,
         'multiplet_no_energy_24_component_lambda2', odd_set_sizes=sizes,
         energies={str(k): sorted(v) for k, v in en_sets.items()},
         note='P_24 V W Omega_0 = 0; the f=W component is (1/4)Omega_0 (energy 0) plus spin one (energy 64)')
    plaqs = [frozenset(face_links(p, a, c)) for p in product(range(-1, 1), repeat=3) for _, a, c in ORIENT]
    diffs = sorted({len(g ^ h) for g in plaqs for h in plaqs})
    need(diffs == [0, 6, 8], 'invariant_multiplet_splitting_sizes', symmetric_difference_sizes=diffs,
         note='g^h is never a single face, so <W_g Omega_0, V W_h Omega_0>=0 on span{W_g Omega_0}')

    # ---------------- K_2 itemizations (item 4)
    items, inp = k2_itemizations(cap)
    K = {k: total(v) / cap ** 2 for k, v in items.items()}
    frec = fr['k2']['exact']['+']
    rrec = rr['ledgers']['exact_plus']
    f_terms = {n: F(frec['terms'][n]['value']) for n in TERMS}
    r_terms = {n: F(rrec['terms'][REV_TERM.get(n, n)]['value']) for n in TERMS}
    s_terms = {n: F(pre['K2']['exact']['terms'][n]['value']) for n in TERMS}
    need(f_terms == items['forward'] and r_terms == items['reverse'] and s_terms == items['skeptic']
         and F(frec['K2']) == F(fr['headline']['K2_exact_plus']) == K['forward']
         and F(rrec['K2_exact_rational']) == F(rr['K2_plus_exact_tier']['exact_rational']) == K['reverse']
         and F(pre['K2']['exact']['K2_exact']) == K['skeptic']
         and F(fr['k2']['variants']['unpinned_t_bounds']['K2']) == K['skeptic']
         and F(frec['t_bound']) == inp['T'] and F(frec['am2_remainder_rho']) == inp['rho'] and F(frec['eps']) == inp['eps_2T_T2']
         and F(rrec['inputs']['epsilon']) == inp['eps_82_face'] and F(rrec['inputs']['s_single_site']) == inp['s0_33_face']
         and F(rrec['inputs']['s_straddling_containing_R']) == inp['s_str_6_face'],
         'k2_exact_tier_recomputed_term_by_term',
         K2={k: q(v) for k, v in K.items()}, K2_preview={k: preview(v) for k, v in K.items()},
         forward_unpinned_variant_equals_skeptic=True, inputs={k: q(v) for k, v in inp.items()})
    valid = {k: all(items[k][n] >= items['minimal_accepted'][n] for n in TERMS) for k in ('forward', 'reverse', 'skeptic')}
    need(all(valid.values()) and inp['T'] == inp['t1'] + inp['rho'] and inp['eps_82_face'] < inp['eps_2T_T2']
         and K['skeptic'] > K['forward'] > K['reverse'] > K['minimal_accepted'],
         'k2_each_itemization_dominates_minimal_accepted', valid_upper_bounds=valid,
         ordering='skeptic > forward > reverse > minimal_accepted',
         minimal_accepted='rho + T(6a+rho) + (33a+rho)^2 + min(eps)^2 + a min(eps)^2')
    per = {k: {n: preview(items[k][n] / cap ** 2, 10) for n in TERMS} for k in items}
    diff_sf = K['skeptic'] - K['forward']
    diff_fr = K['forward'] - K['reverse']
    need(diff_sf == ((items['skeptic']['straddling'] - items['forward']['straddling'])
                     + (items['skeptic']['two_creation'] - items['forward']['two_creation'])) / cap ** 2
         and diff_fr == ((items['forward']['density'] - items['reverse']['density'])
                         + (items['forward']['normalization_order'] - items['reverse']['normalization_order'])) / cap ** 2
         and items['forward']['am2_remainder'] == items['reverse']['am2_remainder'] == items['skeptic']['am2_remainder'],
         'k2_differences_explained', per_term_over_tau2=per,
         skeptic_minus_forward=preview(diff_sf, 8), forward_minus_reverse=preview(diff_fr, 8),
         sources={'skeptic_vs_forward': 'straddling t*t vs T(6a+rho) (6 faces strictly containing R); two-creation t^2 vs (33a+rho)^2',
                  'forward_vs_reverse': 'density eps=2T+T^2 vs eps=82a+2rho+(33a+rho)^2 (82 faces meeting R); normalization a*eps^2 vs (eps+eps^2)eps^2',
                  'common': 'am2_remainder rho=352JT identical (99.98% of every value)'})
    ceil = {'forward_1e-40': F(fr['headline']['K2_exact_ceil_1e40']),
            'reverse_1e-40': F(rr['K2_plus_exact_tier']['ceiling_1e-40']),
            'skeptic_1e-12': F(pre['K2']['exact']['K2_upper_1e-12'])}
    need(ceil['forward_1e-40'] == ceil_to(K['forward'], 10 ** 40) and ceil['reverse_1e-40'] == ceil_to(K['reverse'], 10 ** 40)
         and ceil['skeptic_1e-12'] == ceil_to(K['skeptic'], 10 ** 12)
         and ceil['skeptic_1e-12'] > ceil['forward_1e-40'] > ceil['reverse_1e-40'],
         'k2_directed_ceilings', ceilings={k: q(v) for k, v in ceil.items()},
         rounding_grid='forward and reverse 10^-40, skeptic 10^-12; no grid was preregistered; rounding is outward and changes no decision')
    scal = {}
    for k in ('forward', 'reverse', 'skeptic'):
        lo = [total(k2_itemizations(cap / 10 ** j)[0][k]) / (cap / 10 ** j) ** 2 for j in (1, 2, 3)]
        ratio = total(items[k]) / total(k2_itemizations(cap / 100)[0][k])
        scal[k] = {'monotone': all(x <= K[k] for x in lo) and lo[0] >= lo[1] >= lo[2],
                   'ratio_tau_over_100': preview(ratio, 8), 'quadratic': F(9900) <= ratio <= F(10100)}
    need(all(v['monotone'] and v['quadratic'] for v in scal.values()), 'k2_monotone_in_tau_and_quadratic', scaling=scal)
    fminus_K = F(fr['k2']['exact']['-']['K2'])
    rminus_K = F(rr['ledgers']['exact_minus']['K2_exact_rational'])
    need(fminus_K == K['forward'] and rminus_K == K['reverse'], 'minus_tau_ledgers_are_replays',
         note='the -tau K_2 is the same |tau| formula; not evidence for the flip lemma')
    # crude tier
    cr, cinp = k2_crude(cap)
    KC = {k: total(v) / cap ** 2 for k, v in cr.items()}
    need(KC['forward_and_skeptic'] == F(fr['headline']['K2_crude']) == F(pre['K2']['crude']['K2_exact'])
         and KC['reverse'] == F(rr['K2_plus_crude_tier']['exact_rational'])
         and all(v * cap > threshold for v in KC.values())
         and all(aw2_rule(v, grid_start, threshold) == F(1, 10 ** 10) for v in KC.values()),
         'crude_tier_recomputed_and_fails', K2_crude={k: q(v) for k, v in KC.items()},
         previews={k: preview(v) for k, v in KC.items()},
         margin_at_cap={k: preview(1 / (144 * v * cap), 6) for k, v in KC.items()},
         rule_value_information_only='10^-10', t_crude=q(cinp['t_crude']))
    # omega(W^2) supplementary constants
    a, T, rho = inp['a'], inp['T'], inp['rho']
    kw2_f = (rho + T / 2 * (72 * a + 2 * rho) + F(1, 2) * (33 * a + rho) ** 2 + F(3, 4) * inp['eps_2T_T2'] ** 2) / cap ** 2
    kw2_r = (F(1, 2) * (rho + T * inp['s_str_6_face'] + inp['s0_33_face'] ** 2) + F(3, 4) * inp['eps_82_face'] ** 2) / cap ** 2
    need(kw2_f == F(fr['headline']['K_W2']) and kw2_r == F(rr['K_omega_W2_supplementary']['exact_rational'])
         and kw2_r * cap ** 2 == F(rch['omega_W2_supplementary_second_order_bound']['value_at_cap']) and kw2_f > kw2_r,
         'omega_W2_supplementary_constants', forward=preview(kw2_f), reverse=preview(kw2_r),
         note='forward charges 2 rho and all 72 straddling faces (conservative by about 2); both valid, neither a target')

    # ---------------- AW2 rule and margins (item 5)
    rule = {}
    for k in ('skeptic', 'forward', 'reverse'):
        m = 1 / (margin_den * K[k] * cap)
        rule[k] = {'K2_times_tau': q(K[k] * cap), 'tau_AW2': q(aw2_rule(K[k], grid_start, threshold)),
                   'sign_margin_exact': q(m), 'sign_margin_floor_1e-9': q(floor_to(m, 10 ** 9)),
                   'sign_margin_preview': preview(m, 10), 'ratio_to_1_288_preview': preview(threshold / (K[k] * cap), 10),
                   'feasible': K[k] * cap <= threshold, 'margin_ge_2': m >= margin_min}
    rev_margin = F(rr['feasibility']['sign_margin'])
    need(all(r['tau_AW2'] == q(cap) and r['feasible'] and r['margin_ge_2'] for r in rule.values())
         and F(fr['headline']['sign_margin']) == 1 / (144 * K['forward'] * cap)
         and abs(rev_margin - 1 / (144 * K['reverse'] * cap)) <= F(1, 10 ** 7)
         and fr['headline']['tau_AW2'] == rr['feasibility']['tau_AW2'] == q(cap)
         and F(pre['aw2_rule']['margin_at_cap_lower_1e-9']) == floor_to(1 / (144 * K['skeptic'] * cap), 10 ** 9)
         and aw2_rule(F(10 ** 8, 288), grid_start, threshold) == cap
         and aw2_rule(F(10 ** 8, 288) + F(1, 10 ** 30), grid_start, threshold) == F(1, 10 ** 9)
         and D_ii >= cap * omega1 + K['skeptic'] * cap ** 2,
         'aw2_rule_every_valid_exact_tier_value', rule=rule, robustness='every exact-tier K_2^+ <= 10^8/288 (~347222.2) gives 10^-8',
         av1_compatibility='D_ii >= tau/144 + K_2^+(skeptic) tau^2 at the cap',
         reverse_margin_103='the reverse headline margin ~103.5 is 1/(288 K_2^+ tau), the ratio to the 1/288 threshold; the contract sign margin 1/(144 K_2^+ tau) is ~207.02')

    # ---------------- flip combinatorics and the modified-flip-set remark (item 2)
    mE = re.findall(r'\{\(p,([xyz])\): p_([xyz]) even\}', params['flip_set'])
    ax = {'x': 0, 'y': 1, 'z': 2}
    spec = {ax[d]: ax[c] for d, c in mE}

    def in_rule(rl):
        return lambda l: l[0][rl[l[1]]] % 2 == 0

    inE = in_rule(spec)
    box = [(p, a, c) for p in product(range(-8, 9), range(-8, 9), range(-3, 4)) for _, a, c in ORIENT]

    def count(member, p, a, c):
        return sum(1 for l in face_links(p, a, c) if member(l))
    odd_all = all(count(inE, p, a, c) % 2 == 1 for p, a, c in box)
    residue = [(p, a, c) for p in product(range(2), repeat=3) for _, a, c in ORIENT]
    sols = [r for r in ({0: i, 1: j, 2: k} for i in range(3) for j in range(3) for k in range(3))
            if all(count(in_rule(r), p, a, c) % 2 == 1 for p, a, c in residue)]
    anti = {0: 2, 1: 0, 2: 1}
    inA = in_rule(anti)

    def g(p):
        return (p[0] * p[1] + p[1] * p[2] + p[2] * p[0]) % 2
    gauge = all((inE((p, d)) != inA((p, d))) == (g(add(p, DIRS[d])) != g(p))
                for p in product(range(-6, 7), repeat=3) for d in range(3))
    removed = ((0, 0, 0), 0)
    even_after_removal = sum(1 for p, a, c in box
                             if count(lambda l: inE(l) and l != removed, p, a, c) % 2 == 0)
    need(spec == {0: 1, 1: 2, 2: 0} and odd_all and len(sols) == 2 and spec in sols and anti in sols and gauge
         and even_after_removal == 4,
         'flip_set_odd_two_rules_center_gauge', plaquettes_checked=len(box), one_coordinate_rules_odd=2,
         anti_cyclic_minus_cyclic='coboundary of g=p_x p_y+p_y p_z+p_z p_x mod 2 (center gauge transformation)',
         E_minus_one_link_even_plaquettes=even_after_removal)
    cubes_ok = all(sum([is_selected(p, 0, 1), is_selected(add(p, DIRS[2]), 0, 1), is_selected(p, 0, 2),
                        is_selected(add(p, DIRS[1]), 0, 2), is_selected(p, 1, 2), is_selected(add(p, DIRS[0]), 1, 2)]) in (0, 2)
                   for p in product(range(-8, 8), range(-8, 8), range(-3, 3)))
    b8 = (0, 1, 0, 1, 1, 0, 1, 0)

    def epp_f(l):
        p, d = l
        return d == 0 and p[0] % 4 in (0, 1, 2) and p[1] % 4 in (1, 2)

    def epp_r(l):
        p, d = l
        if d == 0:
            return p[1] % 2 == 1 and p[0] % 4 in (0, 1, 2)
        if d == 1:
            return p[1] % 2 == 1 and b8[p[0] % 8] == 1
        return False
    cob_f = all((count(epp_f, p, a, c) % 2 == 1) == is_selected(p, a, c) for p, a, c in box)
    cob_r = all((count(epp_r, p, a, c) % 2 == 1) == is_selected(p, a, c) for p, a, c in box)
    estar_f = all((count(lambda l: inE(l) != epp_f(l), p, a, c) % 2 == 1) == (not is_selected(p, a, c)) for p, a, c in box)
    estar_r = all((count(lambda l: inE(l) != epp_r(l), p, a, c) % 2 == 1) == (not is_selected(p, a, c)) for p, a, c in box)
    cocycle_fr = all(count(lambda l: epp_f(l) != epp_r(l), p, a, c) % 2 == 0 for p, a, c in box)
    need(cubes_ok and cob_f and cob_r and estar_f and estar_r and cocycle_fr
         and fch['remark_selected_even_flip_set']['passed'] is True
         and rch['finding_selected_even_flip_cochain_not_claimed']['passed'] is True,
         'modified_flip_set_combinatorics_correct',
         cube_condition='every unit cube has 0 or 2 selected faces, so the selected indicator is a Z_2 cocycle, hence a coboundary on any box',
         forward_E2='{(p,x): p_x mod 4 in {0,1,2}, p_y mod 4 in {1,2}}',
         reverse_E2="{(p,x): p_y odd, p_x mod 4 in {0,1,2}} u {(p,y): p_y odd, b(p_x mod 8)=1}, b=(0,1,0,1,1,0,1,0)",
         both_coboundaries_equal_selected_indicator=True, E_star_odd_on_omitted_even_on_selected=True,
         forward_and_reverse_E2_differ_by_a_cocycle=True)
    # exact compression: Omega, e_f=2W Omega_0 (f=W omitted), e_g=2W_g Omega_0 (g selected, sharing link (0,x) with W)
    gsel = frozenset(face_links(ORIGIN, 0, 1))
    need(is_selected(ORIGIN, 0, 1) and len(W & gsel) == 1, 'compression_faces_share_one_link')
    Wl, gl = sorted(W), sorted(gsel)

    def ev(faces):
        if haar_vanishes(faces):
            return F(0)
        if all(f == faces[0] for f in faces):
            return moment(len(faces))
        raise ReviewFailure('Haar expectation not evaluated by this fixture')

    def Hc(t, k):
        v = F(-1, 24) * t                      # alpha units: V=-(tau/24)W - kappa W_g
        e01 = v * 2 * ev([W, W]) - k * 2 * ev([W, gsel])
        e02 = v * 2 * ev([gsel, W]) - k * 2 * ev([gsel, gsel])
        e12 = 4 * (v * ev([W, W, gsel]) - k * ev([W, gsel, gsel]))
        e11 = 3 + 4 * (v * ev([W, W, W]) - k * ev([W, gsel, W]))
        e22 = 3 + 4 * (v * ev([gsel, W, gsel]) - k * ev([gsel, gsel, gsel]))
        return [[F(0), e01, e02], [e01, e11, e12], [e02, e12, e22]]

    def conj(D, M):
        return [[D[i] * M[i][j] * D[j] for j in range(3)] for i in range(3)]

    def sign_of(member, links):
        return -1 if sum(1 for l in links if member(l)) % 2 == 1 else 1
    D_E = [1, sign_of(inE, Wl), sign_of(inE, gl)]
    D_star = [1, sign_of(lambda l: inE(l) != epp_f(l), Wl), sign_of(lambda l: inE(l) != epp_f(l), gl)]
    tk = (F(1, 10 ** 8), F(1, 7))
    need(D_E == [1, -1, -1] and D_star == [1, -1, 1]
         and conj(D_E, Hc(*tk)) == Hc(-tk[0], -tk[1]) and conj(D_E, Hc(*tk)) != Hc(-tk[0], tk[1])
         and conj(D_star, Hc(*tk)) == Hc(-tk[0], tk[1]),
         'modified_flip_set_compression_fixture', U_E='H(tau,kappa) -> H(-tau,-kappa)', U_Estar='H(tau,kappa) -> H(-tau,kappa)',
         label='exact 3x3 compression onto span{Omega_0, 2W Omega_0, 2W_g Omega_0}, alpha units, kappa a selected-face coupling; '
               'finite algebra fixture, not a proof at nonzero triples (strip operator form, reference and uniqueness there are not reviewed)')
    sel_text = SELECTION.read_text()
    loop3_text = LOOP3_SKEPTIC.read_text()
    need('antisymmetry in tau holds only at the zero selected triple' in sel_text
         and 'This gives antisymmetry in tau only when kappa=0' in loop3_text,
         'selection_wording_versus_signoff_wording',
         selection_note='"antisymmetry in tau holds only at the zero selected triple" (unqualified)',
         skeptic_loop3='"This gives antisymmetry in tau only when kappa=0" (a statement about U_E)',
         assessment='the remark does not contradict the contract or the U_E control; it shows the selection sentence is too strong '
                    'if read as a statement about omega(W) itself; nothing is admitted at nonzero triples')

    # ---------------- flags, controls and contract reads
    ff_false = ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift', 'scientific_priority_verified',
                'third_order_remainder_claim', 'omega_W_enclosure_admitted', 'sign_of_omega_W_admitted',
                'euclidean_node_certified', 'uniqueness_claimed', 'rate_in_N_claimed', 'whole_sequence_convergence_claimed')
    rf_false = ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift', 'scientific_priority_verified',
                'third_order_remainder_claim')
    need(all(fr[k] is False for k in ff_false) and all(rr[k] is False for k in rf_false)
         and fr['first_order_parity_claim'] is True and fr['flip_lemma_claim'] is True
         and rr['first_order_parity_claim'] is True and rr['flip_lemma_claim'] is True
         and fr['sub_labels'] == ['static_not_dynamic'] and rr['sub_label'] == 'static_not_dynamic',
         'claim_flags_both', forward_false=list(ff_false), reverse_false=list(rf_false),
         true=['first_order_parity_claim', 'flip_lemma_claim'])
    f_mut = {c: len(fch[c]['mutations_rejected']) for c in controls}
    r_mut = {c: len(rch[c]['rejected_mutations']) for c in controls}
    need(all(v >= 1 for v in f_mut.values()) and all(v >= 1 for v in r_mut.values())
         and all(rch[c].get('kind') == 'damaging_mutation_control' for c in controls)
         and sorted(fr['contract_controls_covered']) == sorted(controls),
         'all_30_controls_damaging_mutations_both', forward_rejections=sum(f_mut.values()),
         reverse_rejections=sum(r_mut.values()))
    fcb = fch['contract_binding']
    need(fcb['target_read_from_contract'] == q(target) and fcb['reference_values_read_from_contract'] == [q(ref_W), q(ref_W2)]
         and rr['target'] == {'comparator': '<=', 'quantity': 'K_2^+ tau at the cap',
                              'read_from': 'contract preregistration.target', 'value': q(target)}
         and rr['reference_values'] == {'omega_0(W)': q(ref_W), 'omega_0(W^2)': q(ref_W2)},
         'target_and_reference_read_from_hash_checked_snapshot')

    # ---------------- source-edit mutations on temporary copies
    base_f = mutated_run('forward')
    base_r = mutated_run('reverse')
    need(base_f[0] == 0 and base_f[1] == (FWD / 'output/results.json').read_bytes()
         and base_r[0] == 0 and base_r[1] == (REV / 'output/results.json').read_bytes(),
         'mutation_harness_unmutated_copies_reproduce_frozen_results')
    need(validate_producer_k2(json.loads(base_f[1]), 'forward', cap) == K['forward']
         and validate_producer_k2(json.loads(base_r[1]), 'reverse', cap) == K['reverse'],
         'term_validator_accepts_unmutated_outputs')
    must_abort = [
        ('forward', 'first_order_sign_flipped', {'edits': [("        return -tau * coef_norm\n", "        return tau * coef_norm\n")]}),
        ('forward', 'flip_rule_x_links_keyed_to_z',
         {'edits': [("        return p[spec[d]] % 2 == 0\n", "        return p[spec[d] if d else 2] % 2 == 0\n")]}),
        ('forward', 'density_term_dropped',
         {'edits': [("('straddling', tier, T * sup, 2), ('density', tier, eps * eps, 2),", "('straddling', tier, T * sup, 2),")]}),
        ('forward', 'overlap_multiplier_4_unlabelled',
         {'edits': [("overlap=Q(1), remainder='gate'", "overlap=Q(4), remainder='gate'")]}),
        ('forward', 'haar_E_W4_changed',
         {'edits': [("    return Q(trivial_multiplicity(n), 2 ** n)\n",
                     "    return Q(trivial_multiplicity(n) + (1 if n == 4 else 0), 2 ** n)\n")]}),
        ('forward', 'aw2_grid_start_shifted', {'edits': [("    k = V['grid_start']\n", "    k = V['grid_start'] + 1\n")]}),
        ('forward', 'third_order_flag_true',
         {'edits': [("                   'third_order_remainder_claim': False, 'omega_W_enclosure_admitted': False,",
                     "                   'third_order_remainder_claim': True, 'omega_W_enclosure_admitted': False,")]}),
        ('forward', 'crude_constant_as_headline', {'edits': [("    K_plus = K['+']['K2']\n", "    K_plus = KC['+']['K2']\n")]}),
        ('forward', 'tau_antisymmetry_allowed_at_nonzero_kappa',
         {'edits': [("        require(all(k == 0 for k in kappa), 'U_E maps kappa to -kappa: no tau-antisymmetry follows from U_E at a nonzero triple')\n",
                     "        pass\n")]}),
        ('forward', 'contract_target_relaxed_no_rehash', {'contract_edit': (b'"value": "1/288"', b'"value": "1/144"')}),
        ('forward', 'contract_reference_1_3_rehashed', {'contract_edit': (b'"0 and 1/4"', b'"0 and 1/3"'), 'rehash': True}),
        ('forward', 'undeclared_input_reverse_report', {'extra_input': 'research/round32/reverse/aw1/report.md'}),
        ('reverse', 'first_order_sign_flipped',
         {'edits': [("    return -FACE_COUPLING_PER_TAU[coupling_units] / FACE_ENERGY_BY_UNITS[energy_units]\n",
                     "    return FACE_COUPLING_PER_TAU[coupling_units] / FACE_ENERGY_BY_UNITS[energy_units]\n")]}),
        ('reverse', 'flip_rule_x_links_keyed_to_z',
         {'edits': [("    return p[rule[d]] % 2 == 0\n", "    return p[rule[d] if d else 2] % 2 == 0\n")]}),
        ('reverse', 'density_term_dropped',
         {'edits': [("            'density': Term('density', eps * eps, 'exact', 'enumeration_82_faces_meeting_R'),\n", "")]}),
        ('reverse', 'overlap_multiplier_4_unlabelled',
         {'edits': [("        multiplier = (Q(1), 'exact_single_component')\n", "        multiplier = (Q(4), 'exact_single_component')\n")]}),
        ('reverse', 'haar_E_W4_changed',
         {'edits': [("    return Q(trivial_multiplicity_chi_half_power(n), 2 ** n)\n",
                     "    return Q(trivial_multiplicity_chi_half_power(n) + (1 if n == 4 else 0), 2 ** n)\n")]}),
        ('reverse', 'aw2_grid_start_shifted', {'edits': [("    k = grid_start_exp\n", "    k = grid_start_exp + 1\n")]}),
        ('reverse', 'third_order_flag_true',
         {'edits': [("                'scientific_priority_verified': False, 'third_order_remainder_claim': False,\n",
                     "                'scientific_priority_verified': False, 'third_order_remainder_claim': True,\n")]}),
        ('reverse', 'crude_constant_as_headline', {'edits': [("    K2 = ex['K2']\n", "    K2 = cr['K2']\n")]}),
        ('reverse', 'tau_antisymmetry_allowed_at_nonzero_kappa',
         {'edits': [("    require(all(Q(k) == 0 for k in kappa),\n            'U_E maps (tau,kappa) to (-tau,-kappa): tau-antisymmetry at a nonzero selected triple is not given by U_E')\n", "")]}),
        ('reverse', 'contract_target_relaxed_no_rehash', {'contract_edit': (b'"value": "1/288"', b'"value": "1/144"')}),
        ('reverse', 'contract_target_1_144_rehashed', {'contract_edit': (b'1/288', b'1/144'), 'rehash': True}),
        ('reverse', 'contract_reference_1_3_rehashed', {'contract_edit': (b'"0 and 1/4"', b'"0 and 1/3"'), 'rehash': True}),
        ('reverse', 'skeptic_triage_added_to_inputs', {'extra_input': 'research/round32/skeptic/triage.md'}),
    ]
    receipts = []
    for direction, label, spec_m in must_abort:
        code, results, last = mutated_run(direction, **spec_m)
        need(code != 0 and results is None, 'mutation_aborts_%s_%s' % (direction, label), last_error_line=last)
        receipts.append({'direction': direction, 'mutation': label, 'producer_aborted': True, 'last_error_line': last})
    # coherent rehashed target tamper: the forward reads the target from the snapshot and records the tampered
    # value (no semantic tie to half the first-order coefficient); the reverse aborts (it ties the threshold to
    # half the derived +1/144). Either way the target is not typed into the checker.
    code, results, last = mutated_run('forward', contract_edit=(b'1/288', b'1/144'), rehash=True)
    tampered = json.loads(results) if results is not None else None
    tch = {c['id']: c for c in tampered['checks']} if tampered else {}
    need(code == 0 and tampered is not None
         and tch['contract_binding']['target_read_from_contract'] == '1/144'
         and tch['aw2_coupling_rule_prefrozen']['target'] == '1/144',
         'forward_reads_target_from_snapshot_rehashed_tamper_recorded',
         finding='forward records the tampered 1/144 target; it has no semantic check that the threshold is half the '
                 'first-order coefficient (the reverse has one); the rehash needs a check.py edit, which freeze.json binds')
    receipts.append({'direction': 'forward', 'mutation': 'contract_target_1_144_rehashed', 'producer_aborted': False,
                     'recorded_target': '1/144', 'note': 'reads-from-contract demonstration, not a rejection'})
    silent = [
        ('forward', 'density_undercount_quarter',
         {'edits': [("('straddling', tier, T * sup, 2), ('density', tier, eps * eps, 2),",
                     "('straddling', tier, T * sup, 2), ('density', tier, eps * eps / 4, 2),")]}),
        ('forward', 'two_creation_undercount_ninth',
         {'edits': [("('two_creation', tier, A0 * Az, 2),", "('two_creation', tier, A0 * Az / 9, 2),")]}),
        ('reverse', 'density_pinned_to_49_faces',
         {'edits': [("        eps = face * certified_count(COUNTS['faces_meeting_R'], 'faces meeting R')",
                     "        eps = face * certified_count(COUNTS['faces_per_factor'], 'faces meeting R')")]}),
        ('reverse', 'two_creation_undercount_ninth',
         {'edits': [("'two_creation': Term('two_creation', 2 * W_OMEGA_NORM * s_single * s_single, 'exact',",
                     "'two_creation': Term('two_creation', 2 * W_OMEGA_NORM * s_single * s_single / 9, 'exact',")]}),
    ]
    for direction, label, spec_m in silent:
        code, results, last = mutated_run(direction, **spec_m)
        caught = False
        reason = ''
        if code == 0 and results is not None:
            try:
                validate_producer_k2(json.loads(results), direction, cap)
            except Rejected as exc:
                caught, reason = True, str(exc)
        need(code == 0 and results is not None and caught
             and results != ((FWD if direction == 'forward' else REV) / 'output/results.json').read_bytes(),
             'silent_edit_caught_by_review_%s_%s' % (direction, label), producer_exit=code, review_rejection=reason)
        receipts.append({'direction': direction, 'mutation': label, 'producer_aborted': False,
                         'caught_by_skeptic_term_validator': True, 'reason': reason})

    exact = {
        'first_order_coefficient': q(omega1), 'contract_display_literal': q(display_literal),
        'first_order_at_cap': [q(cap * omega1), q(-cap * omega1)],
        'K2_exact_tier': {k: q(v) for k, v in K.items()},
        'K2_exact_tier_terms': {k: {n: q(v[n]) for n in TERMS} for k, v in items.items()},
        'K2_crude_tier': {k: q(v) for k, v in KC.items()},
        'K2_recommended_binding': {'value': q(K['skeptic']), 'outward_ceiling_1e-12': q(ceil['skeptic_1e-12']),
                                   'source': 'skeptic headline = forward labelled variant unpinned_t_bounds (exact tier)',
                                   'tau_AW2': q(aw2_rule(K['skeptic'], grid_start, threshold)),
                                   'sign_margin_exact': q(1 / (144 * K['skeptic'] * cap)),
                                   'sign_margin_floor_1e-9': q(floor_to(1 / (144 * K['skeptic'] * cap), 10 ** 9))},
        'omega_W2_constants': {'forward': q(kw2_f), 'reverse': q(kw2_r)},
        'D_ii_av1': q(D_ii),
    }
    previews = {
        'K2_exact_tier': {k: preview(v) for k, v in K.items()},
        'K2_crude_tier': {k: preview(v) for k, v in KC.items()},
        'sign_margin': {k: rule[k]['sign_margin_preview'] for k in rule},
        'first_order_at_cap': preview(cap * omega1),
        'remainder_at_cap_skeptic': preview(K['skeptic'] * cap ** 2),
        'note': 'decimal previews only; every Boolean above was decided on exact rationals',
    }
    return {
        'schema': 'hnm-r32-skeptic-postcomparison-v1', 'loop': 'AW1', 'stage': 'post_comparison',
        'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'model-agent skeptic with correlated ancestry; not human peer review or formal verification',
        'contract_sha256': CONTRACT_SHA, 'exact': exact, 'previews': previews, 'aw2_rule': rule,
        'mutation_receipts': receipts, 'passed': True, 'checks': CHECKS, 'checks_count': len(CHECKS),
    }


def main():
    ap = argparse.ArgumentParser(description='AW1 post-comparison skeptic checks')
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
    print(json.dumps({'loop': 'AW1', 'stage': 'post_comparison', 'checks': result['checks_count'],
                      'K2_exact': result['previews']['K2_exact_tier'],
                      'mutations': len(result['mutation_receipts'])}, sort_keys=True))


if __name__ == '__main__':
    main()
