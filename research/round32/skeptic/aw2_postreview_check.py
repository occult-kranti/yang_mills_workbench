#!/usr/bin/env python3
"""AW2 post-comparison skeptic checks, written after the forward AW2 freeze.

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated
ancestry (same model family as the advisor and the producer; the bound K_2^+ is
the skeptic's own AW1 itemization); not human peer review or formal verification.

AW2 is a single-direction certificate (contract producers=["forward"],
direction "single+skeptic"). Admission rests on the forward producer plus the
skeptic's frozen pre-comparison replay (aw2_check.py, aw2-independent/). This
post-comparison checker adds:
  * the provenance chain: contract and AW1 gate pins, the unchanged
    pre-comparison package, the producer freeze closure and its declared
    premise inventory, the absence of any reverse AW2 package;
  * an exact re-derivation in this file's own Fraction code: K_2^+ from the gate
    text and its itemization, the first-order sign chain (+tau/144), the frozen
    AW1 decade-grid rule, both enclosures, the exclusion and sign margins and
    their directed floors, the crude tier (retained failure), the outward
    ceiling variant, the AV1 containment and the scaling exponents;
  * exact comparison with every rational the producer exports and with the
    pre-comparison replay, and directed/tightness checks of every decimal;
  * the producer's 37 checks, the 23 contract controls as damaging mutations,
    the claim flags, the scope record, the literal-coupling protection (static
    data flow of tau_AW2 from the hash-checked gate and a functional call of the
    producer's rule), the calculator's domain and the Arb/mpmath preview's
    labelling and non-dependence;
  * source-edit mutations: the producer closure is copied to a temporary tree
    outside the checkout and edited once per run; every must-abort edit has to
    abort, an unmutated copy has to reproduce the frozen output byte for byte,
    one silent edit (a literal coupling equal to the rule value) has to be
    caught by this review's static validator, and one preview edit has to leave
    every admitted value unchanged.

Standard library only; exact Fractions decide every Boolean; failures are explicit
exceptions (never assert), so the output bytes match under python -O.

Usage: python3 -B research/round32/skeptic/aw2_postreview_check.py --output /abs/fresh/dir
"""
import argparse
import ast
import hashlib
import importlib.util
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
ROOT = HERE.parents[2]
R32 = ROOT / 'research/round32'
CONTRACT = R32 / 'contracts/aw2.json'
CONTRACT_SHA = 'aa559b18231961b5bb9dc5b7d0dd3097a1a2753916b54639eb1fd573e08368f9'
AW1_GATE = R32 / 'advisor/aw1-gate.json'
AW1_GATE_SHA = '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae'
AW1_CONTRACT_REL = 'research/round32/contracts/aw1.json'
AV1_GATE_REL = 'research/round32/advisor/av1-gate.json'
I1_REL = 'research/round21/forward/i1/report.md'
FWD = R32 / 'forward/aw2'
FWD_REL = 'research/round32/forward/aw2'
PRE_RESULTS = HERE / 'aw2-independent/results.json'
PRE_FREEZE = HERE / 'aw2-independent-freeze.json'
PRE_CHECKER = HERE / 'aw2_check.py'
# Values stated in the review request (compared after the fact, never used as inputs).
STATED_DEN = 618929575309102117553427431032936422860390400000000
STATED_LO_NUM = 42773581813770903096597852821080380528959
STATED_HI_NUM = 43188859201382168785822623711271900423873
FALSE_FLAGS = ('continuum_claim', 'uniform_wilson_claim', 'sign_certified_below_cap', 'dynamical_correction_claim',
               'scientific_priority_verified', 'mass_shift_claim', 'susceptibility_claim', 'correlation_shift_resolved',
               'uniqueness_claim', 'whole_sequence_convergence_claim', 'rate_in_N_claim', 'third_order_remainder_claim')


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


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def exponent10(x):
    x = abs(F(x))
    e = 0
    while x >= F(10) ** (e + 1):
        e += 1
    while x < F(10) ** e:
        e -= 1
    return e


def preview(x, digits=12):
    """Truncated scientific decimal (display only; never decides anything)."""
    x = F(x)
    if x == 0:
        return '0'
    sign = '-' if x < 0 else ''
    x = abs(x)
    e = exponent10(x)
    m = x / F(10) ** (e - digits + 1)
    s = str(m.numerator // m.denominator)
    return sign + s[0] + '.' + s[1:] + 'e' + str(e)


def directed(x, up, digits=12):
    """Directed scientific decimal: toward +inf (up) or -inf (down); display only."""
    x = F(x)
    if x == 0:
        return '0'
    e = exponent10(x)
    y = x / F(10) ** (e - digits + 1)
    n = -((-y.numerator) // y.denominator) if up else y.numerator // y.denominator
    body = str(abs(n))
    out = ('-' if n < 0 else '') + body[0] + '.' + body[1:] + 'e' + str(e - digits + len(body))
    if (up and F(out) < x) or ((not up) and F(out) > x):
        raise ReviewFailure('directed decimal')
    return out


def floor_to(x, den):
    x = F(x)
    return F((x.numerator * den) // x.denominator, den)


def ceil_to(x, den):
    x = F(x)
    return F(-((-x.numerator * den) // x.denominator), den)


def decimal_directed(text, exact, upward, sig):
    """Exact parse of a decimal string: correct side of `exact` and within one unit of its last digit."""
    if not re.fullmatch(r'-?\d\.\d+e-?\d+', text) or len(text.split('e')[0].lstrip('-').replace('.', '')) != sig:
        return False
    back = F(text)
    ulp = F(10) ** (exponent10(exact) - sig + 1)
    return (back >= exact and back - exact < ulp) if upward else (back <= exact and exact - back < ulp)


# ------------------------------------------------------------ own exact derivation
def parse_gate_constants(gate):
    """This reviewer's own regexes over the AW1 gate text (not the producer's)."""
    dec, acc = gate['decision'], gate['accepted']
    m1 = re.search(r'Bind K_2\^\+ = (\d+)/(\d+) .*?outward ceiling (\d+)/10\^(\d+)\)', dec)
    m2 = re.search(r'the bound value is K_2\^\+=(\d+)/(\d+) \(~[0-9.]+, outward (\d+)/10\^(\d+);', acc)
    m3 = re.search(r'\(t<=T=\((\d+)\|tau\|/(\d+)\)/\(1-(\d+)J\), rho=(\d+)JT, J=(\d+)\|tau\|\)', acc)
    m4 = re.search(r'omega_tau\(W\)=\+tau/(\d+)\+r\(tau\)', acc)
    m5 = re.search(r'The crude tier \(t_c=(\d+)\|tau\|', acc)
    m6 = re.search(r'directed floor (\d+)/(\d+)\)', acc)
    if not all((m1, m2, m3, m4, m5, m6)):
        raise ReviewFailure('AW1 gate text not parsed')
    return {'K_decision': F(int(m1.group(1)), int(m1.group(2))), 'ceiling': F(int(m1.group(3)), 10 ** int(m1.group(4))),
            'ceiling_digits': int(m1.group(4)),
            'K_accepted': F(int(m2.group(1)), int(m2.group(2))), 'ceiling_accepted': F(int(m2.group(3)), 10 ** int(m2.group(4))),
            'faces': int(m3.group(1)), 'face_den': int(m3.group(2)), 'L': int(m3.group(3)), 'L_rho': int(m3.group(4)),
            'Jc': int(m3.group(5)), 'c1_den': int(m4.group(1)), 'crude_tc': int(m5.group(1)),
            'sign_floor': F(int(m6.group(1)), int(m6.group(2)))}


def itemization(tau_abs, faces, face_den, L, Jc, crude_tc=None):
    """K_2 tau^2 = rho + T*T (straddling) + T^2 (two-creation) + eps^2 (density) + (|tau|/144) eps^2 (normalization)."""
    a = tau_abs / face_den
    J = Jc * tau_abs
    T = crude_tc * tau_abs if crude_tc is not None else faces * a / (1 - L * J)
    rho = L * J * T
    eps = 2 * T + T * T
    terms = {'am2_remainder': rho, 'straddling': T * T, 'two_creation': T * T, 'density': eps * eps,
             'normalization_order': a * eps * eps}
    return terms, sum(terms.values(), F(0)) / (tau_abs * tau_abs), T


def haar_moment(n):
    mult = {0: 1}
    for _ in range(n):
        new = {}
        for tj, c in mult.items():
            for nj in (tj - 1, tj + 1):
                if nj >= 0:
                    new[nj] = new.get(nj, 0) + c
        mult = new
    return F(mult.get(0, 0), 2 ** n)


def rule(K, start, threshold, steps=60):
    for k in range(start, start + steps):
        t = F(1, 10 ** k)
        if K * t <= threshold:
            return t
    raise ReviewFailure('decade grid exhausted')


def interval(tau, K, c1):
    first = c1 * tau
    rad = K * tau * tau
    return first - rad, first + rad, first, rad


# ------------------------------------------------------------ static data-flow validator
def _assigns(body, name):
    """Assignments to `name` in a function body, not descending into nested functions or lambdas."""
    out = []
    stack = list(body)
    while stack:
        node = stack.pop()
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef)):
            continue
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                names = [tgt] if isinstance(tgt, ast.Name) else (list(tgt.elts) if isinstance(tgt, ast.Tuple) else [])
                for i, n in enumerate(names):
                    if isinstance(n, ast.Name) and n.id == name:
                        val = node.value
                        if isinstance(tgt, ast.Tuple):
                            val = node.value.elts[i] if isinstance(node.value, ast.Tuple) else node.value
                        out.append(ast.unparse(val))
        stack.extend(ast.iter_child_nodes(node))
    return out


def validate_coupling_dataflow(check_src, calc_src):
    """tau_AW2 must be the frozen rule evaluated on K_2^+ parsed from the hash-verified AW1 gate snapshot."""
    tree = ast.parse(check_src)
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    consts = {t.id: n.value.value for n in tree.body if isinstance(n, ast.Assign)
              for t in n.targets if isinstance(t, ast.Name) and isinstance(n.value, ast.Constant)}
    if consts.get('AW1_GATE_SHA256') != AW1_GATE_SHA or consts.get('AW1_GATE_REL') != 'research/round32/advisor/aw1-gate.json':
        raise Rejected('gate pin or path differs from the reviewed AW1 gate')
    if consts.get('AW1_CONTRACT_REL') != AW1_CONTRACT_REL:
        raise Rejected('rule source is not the AW1 contract')
    body = funcs['compute'].body
    expect = {'tau_aw2': ['aw2_rule(K, R)'], 'K': ["G['K']"], 'G': ['parse_gate(gate_raw)'],
              'gate_raw': ['read_input(AW1_GATE_REL)'], 'R': ['parse_aw1_rule(read_input(AW1_CONTRACT_REL), G)']}
    for name, value in expect.items():
        got = _assigns(body, name)
        if got != value:
            raise Rejected('%s is not assigned from the gate chain: %r' % (name, got))
    gate_src = ast.unparse(funcs['parse_gate'])
    if "require(sha_bytes(raw) == AW1_GATE_SHA256" not in gate_src or "G['K'] = Q(int(m.group(1)), int(m.group(2)))" not in gate_src:
        raise Rejected('parse_gate does not hash-verify the gate or does not parse K from it')
    rule_consts = sorted({repr(n.value) for n in ast.walk(funcs['aw2_rule']) if isinstance(n, ast.Constant)})
    if rule_consts != sorted(["'bound'", "'decade grid exhausted'", "'start'", '1', '10', '60', 'True']):
        raise Rejected('aw2_rule carries a literal beyond the grid mechanics: %r' % rule_consts)
    ctree = ast.parse(calc_src)
    cfun = {n.name: n for n in ctree.body if isinstance(n, ast.FunctionDef)}
    if _assigns(cfun['enclose'].body, 'tau_aw2') != ['coupling_rule(G)'] or _assigns(cfun['enclose'].body, 'G') != ['gate_constants()']:
        raise Rejected('calculator coupling is not the rule evaluated from the gate constants')
    return {'tau_aw2': 'aw2_rule(K, R)', 'K': "G['K']", 'G': 'parse_gate(gate_raw)', 'gate_raw': 'read_input(AW1_GATE_REL)',
            'R': 'parse_aw1_rule(read_input(AW1_CONTRACT_REL), G)', 'aw2_rule_constants': rule_consts,
            'calculator': 'tau_aw2, steps = coupling_rule(G), G = gate_constants()'}


def forbidden_imports(src):
    bad = ('mpmath', 'flint', 'numpy', 'scipy', 'sympy', 'arb_preview')
    names = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Import):
            names += [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            names.append(n.module or '')
    return sorted(x for x in names if any(b in x for b in bad)), sorted(set(names))


# ------------------------------------------------------------ source-mutation replays
def mutated_run(edits=None, file_edits=None, remove=(), extra_input=None, rehash_contract=False, rehash_gate=False):
    """Copy the producer closure outside the checkout, apply one edit set, run check.py; return (code, results, manifest, last)."""
    with tempfile.TemporaryDirectory(prefix='hnm-r32-aw2-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / FWD_REL
        shutil.copytree(FWD, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        for name, pairs in (edits or {}).items():
            text = (dst / name).read_text()
            for old, new in pairs:
                if text.count(old) != 1:
                    raise ReviewFailure('mutation anchor not unique in %s: %r' % (name, old[:70]))
                text = text.replace(old, new)
            (dst / name).write_text(text)
        for name, fn in (file_edits or {}).items():
            raw = (dst / name).read_bytes()
            new = fn(raw)
            if new == raw:
                raise ReviewFailure('file mutation had no effect: ' + name)
            (dst / name).write_bytes(new)
        for name in remove:
            (dst / name).unlink()
        if rehash_contract:
            new_sha = sha(dst / 'inputs/research/round32/contracts/aw2.json')
            text = (dst / 'check.py').read_text()
            if text.count(CONTRACT_SHA) != 1:
                raise ReviewFailure('contract pin not unique')
            (dst / 'check.py').write_text(text.replace(CONTRACT_SHA, new_sha))
        if rehash_gate:
            new_sha = sha(dst / 'inputs/research/round32/advisor/aw1-gate.json')
            for name in ('check.py', 'calculator.py'):
                text = (dst / name).read_text()
                if text.count(AW1_GATE_SHA) != 1:
                    raise ReviewFailure('gate pin not unique in ' + name)
                (dst / name).write_text(text.replace(AW1_GATE_SHA, new_sha))
        if extra_input is not None:
            extra = dst / 'inputs' / extra_input
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text('skeptic mutation fixture\n')
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(dst / 'check.py'), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(repo))
        results = (out / 'results.json').read_bytes() if (out / 'results.json').is_file() else None
        manifest = (out / 'source-manifest.json').read_bytes() if (out / 'source-manifest.json').is_file() else None
        last = done.stderr.strip().splitlines()[-1] if done.stderr.strip() else ''
        if any(p.name == '__pycache__' or p.suffix == '.pyc' for p in dst.rglob('*')):
            raise ReviewFailure('interpreter cache written into a mutated copy')
        src_after = (dst / 'check.py').read_text(), (dst / 'calculator.py').read_text()
        return done.returncode, results, manifest, last.replace(tmp, '<tmp>'), src_after


def json_diff(a, b, path=''):
    if type(a) is not type(b):
        return [path]
    if isinstance(a, dict):
        out = []
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(path + '/' + k)
            else:
                out += json_diff(a[k], b[k], path + '/' + k)
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [path]
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            label = x.get('id', str(i)) if isinstance(x, dict) else str(i)
            out += json_diff(x, y, path + '/' + label)
        return out
    return [] if a == b else [path]


# ------------------------------------------------------------ main computation
def run():
    contract_raw = CONTRACT.read_bytes()
    contract = json.loads(contract_raw)
    gate_raw = AW1_GATE.read_bytes()
    gate = json.loads(gate_raw)
    prereg = contract['preregistration']
    controls = list(contract['controls'])

    # ---------------- provenance
    need(sha_bytes(contract_raw) == CONTRACT_SHA and contract['status'] == 'frozen_before_production'
         and contract['producers'] == ['forward'] and contract['direction'] == 'single+skeptic'
         and contract['single_direction_independent_replay'] is True and len(controls) == 23
         and prereg['controls_required']['ids'] == controls and len(set(controls)) == 23,
         'contract_pin_single_direction_and_controls', contract_sha256=CONTRACT_SHA, controls=str(len(controls)))
    gb = gate['bindings']
    need(sha_bytes(gate_raw) == AW1_GATE_SHA and gate['loop'] == 'AW1' and gate['verdict'] == 'accepted_within_scope'
         and all(sha(ROOT / rel) == gb[rel] for rel in (AW1_CONTRACT_REL, AV1_GATE_REL, I1_REL)),
         'aw1_gate_pin_and_binding_chain', aw1_gate_sha256=AW1_GATE_SHA,
         chain_verified=[AW1_CONTRACT_REL, AV1_GATE_REL, I1_REL])
    pre_freeze = json.loads(PRE_FREEZE.read_text())
    pre = json.loads(PRE_RESULTS.read_text())
    need(pre_freeze['stage'] == 'pre_comparison_independent_replay' and pre_freeze['contract_sha256'] == CONTRACT_SHA
         and all(sha(ROOT / rel) == d for rel, d in pre_freeze['files'].items()) and len(pre_freeze['files']) == 4
         and pre['producer_files_read'] == [] and not any('forward/aw2' in k for k in pre['inputs_sha256'])
         and pre['stage'] == 'pre_comparison_independent_replay',
         'pre_comparison_package_unchanged', files=sorted(pre_freeze['files']))
    with tempfile.TemporaryDirectory(prefix='hnm-r32-aw2-skeptic-pre-') as tmp:
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(PRE_CHECKER), '--output', str(Path(tmp) / 'o')],
                              capture_output=True, text=True, cwd=str(ROOT))
        pre_replay = (Path(tmp) / 'o/results.json').read_bytes() if done.returncode == 0 else None
    need(pre_replay == PRE_RESULTS.read_bytes(), 'pre_comparison_replay_reproduces', results_sha256=sha(PRE_RESULTS))

    freeze = json.loads((FWD / 'freeze.json').read_text())
    closure = {p.relative_to(ROOT).as_posix() for p in FWD.rglob('*') if p.is_file() and p != FWD / 'freeze.json'}
    need(freeze['loop'] == 'AW2' and freeze['direction'] == 'forward' and freeze['contract_sha256'] == CONTRACT_SHA
         and set(freeze['sources']) == closure and all(sha(ROOT / n) == d for n, d in freeze['sources'].items())
         and FWD_REL + '/report.md' in freeze['sources'] and FWD_REL + '/check.py' in freeze['sources']
         and not any('__pycache__' in n or n.endswith('.pyc') for n in closure)
         and freeze['normal_optimized_identical'] is True,
         'producer_freeze_closure_verified', closure_files=str(len(closure)), freeze_sha256=sha(FWD / 'freeze.json'))
    declared = {'AGENTS.md', 'research/round32/contracts/aw2.json'} | set(contract['shared_premises'])
    inv = {p.relative_to(FWD / 'inputs').as_posix() for p in (FWD / 'inputs').rglob('*') if p.is_file()}
    need(inv == declared and all((FWD / 'inputs' / n).read_bytes() == (ROOT / n).read_bytes() for n in inv)
         and not any(re.search(r'skeptic/aw2|reverse/aw2|forward/aw1/output', n) for n in inv)
         and not (R32 / 'reverse/aw2').exists(),
         'producer_inputs_equal_declared_and_no_reverse_package', inputs=str(len(inv)),
         undeclared=[], reverse_package_present=False)

    # ---------------- own exact derivation
    gc = parse_gate_constants(gate)
    K = gc['K_decision']
    mK = re.match(r'(\d+)/(\d+) \(AW1 gate;', contract['parameters']['K_2_plus'])
    K_contract = F(int(mK.group(1)), int(mK.group(2)))
    need(K == gc['K_accepted'] == K_contract and gc['ceiling'] == gc['ceiling_accepted']
         and gc['ceiling'] == ceil_to(K, 10 ** gc['ceiling_digits']) and gc['ceiling'] - K < F(1, 10 ** 12),
         'k2_plus_from_gate_text', K_2_plus=q(K), outward_ceiling=q(gc['ceiling']))
    i1_text = (ROOT / I1_REL).read_text()
    i15 = re.search(r'=\s*-\{\\tau\\over(\d+)\}\\sum_\{f\\in O_b\}W_f', i1_text)
    phi_den = int(i15.group(1))                                     # phi_b = -(tau/3) sum W_f
    alpha_div = int(re.search(r'V_b=phi_b/(\d+)\)', contract['parameters']['first_order']).group(1))
    v_face = -F(1, phi_den * alpha_div)                             # V per face per tau, alpha units: -1/24
    energy_face = 4 * F(3, 4)                                       # four spin-1/2 links, Casimir 3/4 each (alpha units)
    c_face = v_face / energy_face                                   # c^(1) per face per tau: -1/72
    EW2 = haar_moment(2)
    c1 = -2 * c_face * EW2                                          # omega = -2 Re<W Omega_0, c^(1)>
    literal_display = 2 * c_face * EW2
    pg = {c['id']: c for c in pre['checks']}['geometry_counts_from_I1_4']   # frozen pre-comparison I1.4 enumeration
    faces_per_factor = int(pg['faces_per_site'])                    # 49 omitted faces per coarse site
    J_per_tau = int(pg['star_sites']) * F(int(pg['anchored']), 3)  # four incoming stars x 21 anchored faces x 1/3
    need(phi_den == 3 and alpha_div == 8 and v_face == F(-1, 24) and c_face == F(-1, 72) and EW2 == F(1, 4)
         and c1 == F(1, 144) == F(1, gc['c1_den']) and literal_display == F(-1, 144)
         and [haar_moment(n) for n in range(1, 9)] == [0, F(1, 4), 0, F(1, 8), 0, F(5, 64), 0, F(7, 128)],
         'first_order_sign_chain_plus_tau_over_144', V_per_face_alpha='-tau/24', energy_alpha='3',
         creation_per_face='-tau/72', coefficient=q(c1), literal_display_value=q(literal_display))
    need(gc['faces'] == faces_per_factor and gc['face_den'] == 144 and gc['Jc'] == J_per_tau and gc['L'] == gc['L_rho'] == 352,
         'gate_exact_tier_constants_match_own_counts', faces_per_factor='49', J='28|tau|', L='352 (AM2, inherited)')
    cap = F(1, 10 ** int(re.search(r'\|tau\|<=10\^-(\d+):', gate['accepted']).group(1)))
    terms, K_item, T = itemization(cap, gc['faces'], gc['face_den'], gc['L'], gc['Jc'])
    need(K_item == K and all(v > 0 for v in terms.values()) and terms['am2_remainder'] / sum(terms.values(), F(0)) > F(9997, 10000),
         'k2_plus_itemization_replay', terms_at_cap={k: q(v) for k, v in terms.items()}, T=q(T),
         am2_share_preview=preview(terms['am2_remainder'] / sum(terms.values(), F(0)), 6))
    aw1c = json.loads((ROOT / AW1_CONTRACT_REL).read_text())
    mr = re.search(r'decade grid \{10\^-(\d+), 10\^-(\d+), \.\.\.\} with K_2\^\+ \* tau <= (\d+)/(\d+) \(half the first-order coefficient\)',
                   aw1c['parameters']['aw2_coupling_rule'])
    start, threshold = int(mr.group(1)), F(int(mr.group(3)), int(mr.group(4)))
    tau = rule(K, start, threshold)
    _, K_crude, T_crude = itemization(cap, gc['faces'], gc['face_den'], gc['L'], gc['Jc'], crude_tc=gc['crude_tc'])
    need(int(mr.group(2)) == start + 1 and threshold == c1 / 2 and F(1, 10 ** start) == F(aw1c['parameters']['tau_cap']) == cap
         and tau == cap == F(1, 10 ** 8) and rule(1000 * K, start, threshold) == F(1, 10 ** 9)
         and rule(K_crude, start, threshold) == F(1, 10 ** 10),
         'aw2_rule_own_evaluation', tau_AW2=q(tau), threshold=q(threshold), K_tau=q(K * tau),
         slack=q(threshold - K * tau), threshold_over_K_tau=q(threshold / (K * tau)),
         functional='1000 K_2^+ -> 10^-9 (K_2^+ tau has a factor ~103.5 of slack at the cap); crude K_2 -> 10^-10 (information only)')
    lo, hi, first, rad = interval(tau, K, c1)
    lo_m, hi_m, first_m, rad_m = interval(-tau, K, c1)
    need(F(lo).denominator == STATED_DEN and F(lo).numerator == STATED_LO_NUM and F(hi).denominator == STATED_DEN
         and F(hi).numerator == STATED_HI_NUM and first == F(1, 14400000000) and rad == K / 10 ** 16
         and lo_m == -hi and hi_m == -lo and hi - lo == 2 * rad,
         'enclosure_exact_endpoints_both_signs', plus=[q(lo), q(hi)], minus=[q(lo_m), q(hi_m)],
         stated_endpoints_equal=True)
    S = first / rad
    m = (first - rad) / rad
    need(lo > 0 and hi_m < 0 and m == S - 1 and m >= 2 and S >= 3 and S == 1 / (144 * K * tau)
         and floor_to(S, 10 ** 9) == gc['sign_floor'] == F(41400010489, 200000000)
         and floor_to(m, 10 ** 9) == F(41200010489, 200000000)
         and F(20600005, 100000) < m < F(20600006, 100000) and F(20700005, 100000) < S < F(20700006, 100000)
         and (first_m + rad_m) / rad_m == -(m) and lo / first == 1 - 1 / S,
         'strict_exclusion_and_margins', exclusion_margin=q(m), sign_margin=q(S),
         exclusion_margin_floor_1e_9=q(floor_to(m, 10 ** 9)), sign_margin_floor_1e_9=q(floor_to(S, 10 ** 9)),
         target='>= 2 (contract)', lower_over_first=q(lo / first))
    need(threshold / (K * tau) == S / 2 and (first - threshold * tau) / (threshold * tau) == 1,
         'rule_implies_only_m_ge_1_target_tested_separately',
         note='K|tau|<=1/288 gives S>=2, m>=1; the target m>=2 needs S>=3 (K|tau|<=1/432) and is tested on its own')
    clo, chi_, cfirst, crad = interval(tau, K_crude, c1)
    need(clo < 0 < chi_ and cfirst / crad < 1 and (cfirst - crad) / crad < 0
         and K_crude == F(1937877026146766159414097129, 244140625000000000000) and T_crude == 592 * cap,
         'crude_tier_fails_at_cap', K_crude=q(K_crude), enclosure=[q(clo), q(chi_)],
         sign_margin=q(cfirst / crad), exclusion_margin_preview=preview((cfirst - crad) / crad, 6))
    olo, ohi, _, orad = interval(tau, gc['ceiling'], c1)
    need(0 < olo < lo and ohi > hi and (first - orad) / orad >= 2 and orad - rad < F(1, 10 ** 28),
         'outward_ceiling_variant_still_excludes', widening=q(orad - rad))
    av1 = json.loads((ROOT / AV1_GATE_REL).read_text())
    md = re.search(r'D_ii=(\d+)/(\d+) \(~1\.3612e-8', av1['accepted'])
    D_ii = F(int(md.group(1)), int(md.group(2)))
    eps = 2 * T + T * T
    need(max(abs(lo), abs(hi)) <= D_ii and 2 * eps * (1 + eps) / (1 + eps * eps) == D_ii,
         'av1_containment_and_same_T', D_ii=q(D_ii), ratio_preview=preview(D_ii / hi, 6))
    slo, shi, sfirst, srad = interval(tau / 100, K, c1)
    _, K_small, _ = itemization(cap / 100, gc['faces'], gc['face_den'], gc['L'], gc['Jc'])
    need(first / sfirst == 100 and rad / srad == 10000 and K_small < K,
         'scaling_exponents_1_and_2_and_monotone_constant', K2_itemized_at_tau_over_100_preview=preview(K_small))

    # ---------------- comparison with the producer's exported rationals
    res_raw = (FWD / 'output/results.json').read_bytes()
    res = json.loads(res_raw)
    ch = {c['id']: c for c in res['checks']}
    hl = res['headline']
    need(F(hl['K_2_plus']) == K and F(hl['tau_AW2']) == tau and hl['first_order_coefficient'] == '+tau/144'
         and [F(hl['enclosure_plus']['lower']), F(hl['enclosure_plus']['upper'])] == [lo, hi]
         and [F(hl['enclosure_minus']['lower']), F(hl['enclosure_minus']['upper'])] == [lo_m, hi_m]
         and F(hl['exclusion_margin']) == m and F(hl['sign_margin']) == S and F(hl['target_exclusion_margin']) == 2,
         'producer_headline_equals_own_exact_values')
    enc = res['enclosures']
    need(all(F(enc[sg]['tau']) == t and F(enc[sg]['first_order_value']) == c1 * t and F(enc[sg]['second_order_radius']) == rad
             and F(enc[sg]['lower']) == a and F(enc[sg]['upper']) == b and enc[sg]['excludes_zero_strictly'] is True
             and enc[sg]['sign_of_omega_W'] == sg and F(enc[sg]['exclusion_margin']) == m and F(enc[sg]['sign_margin']) == S
             for sg, t, a, b in (('+', tau, lo, hi), ('-', -tau, lo_m, hi_m))),
         'producer_enclosure_records_equal')
    dec_pairs = [(hl['enclosure_plus_decimal_outward']['lower'], lo, False), (hl['enclosure_plus_decimal_outward']['upper'], hi, True),
                 (hl['enclosure_minus_decimal_outward']['lower'], lo_m, False), (hl['enclosure_minus_decimal_outward']['upper'], hi_m, True),
                 (hl['exclusion_margin_decimal_down'], m, False), (hl['sign_margin_decimal_down'], S, False),
                 (hl['K_2_plus_decimal_up'], K, True)]
    need(all(decimal_directed(t, x, up, 12) for t, x, up in dec_pairs)
         and all(decimal_directed(enc[sg][k], F(enc[sg][k.split('_decimal')[0]]), k.endswith('_up'), 12)
                 for sg in enc for k in ('lower_decimal_outward_down', 'upper_decimal_outward_up')),
         'producer_decimals_directed_and_within_one_ulp', decimals=[t for t, _, _ in dec_pairs])
    pe = pre['enclosure']
    need(F(pe['+']['lo']) == lo and F(pe['+']['hi']) == hi and F(pe['-']['lo']) == lo_m and F(pe['-']['hi']) == hi_m
         and F(pre['margins']['exclusion_margin']) == m and F(pre['margins']['sign_margin']) == S
         and F(pre['K2_plus']['exact']) == K and F(pre['crude_tier']['K2']) == K_crude and F(pre['aw2_rule']['tau_AW2']) == tau
         and F(pre['aw2_rule']['slack']) == threshold - K * tau
         and F(hl['enclosure_plus_decimal_outward']['lower']) <= F(pe['+']['lo_decimal_outward']) <= lo
         and hi <= F(pe['+']['hi_decimal_outward']) <= F(hl['enclosure_plus_decimal_outward']['upper'])
         and pre['proposed_verdict'] == 'accepted_within_scope' and pre['sub_labels'] == ['static_not_dynamic'],
         'pre_comparison_equal_to_producer_and_own',
         nesting='producer 12-digit outward decimals contain the pre-comparison 16-digit outward decimals, which contain the exact endpoints')
    ra = ch['aw2_coupling_rule_prefrozen']['rule_arithmetic']
    need(F(ra['K_2_plus_tau']) == K * tau and F(ra['slack']) == threshold - K * tau and F(ra['bound']) == threshold
         and F(ra['bound_over_K_2_plus_tau']) == threshold / (K * tau) and len(ra['steps']) == 1
         and ra['steps'][0]['satisfied'] is True and F(ch['aw2_coupling_rule_prefrozen']['tau_AW2']) == tau
         and ch['aw2_coupling_rule_prefrozen']['rule_text'] == aw1c['parameters']['aw2_coupling_rule'],
         'producer_rule_arithmetic_equal')
    tm, ivr, fre = ch['tier_mixing_rejected'], ch['insufficient_verdict_retained'], ch['free_reference_exclusion']
    need(F(tm['crude_K_2']) == K_crude and [F(tm['crude_enclosure_at_cap']['lower']), F(tm['crude_enclosure_at_cap']['upper'])] == [clo, chi_]
         and fre['crude_tier_enclosure_at_cap']['contains_zero'] is True
         and ivr['retained_outcomes']['crude_tier_at_cap'] == 'no exclusion (limited-tier control, retained)'
         and F(ivr['retained_outcomes']['crude_rule_decade_information_only']) == F(1, 10 ** 10)
         and tm['crude_status'].startswith('fails at the cap (enclosure contains 0') and F(hl['K_2_plus']) != K_crude,
         'producer_crude_tier_retained_as_failure', crude_status=tm['crude_status'])
    wf = ch['wrong_face_control']
    hp = ch['haar_parity_exact']
    need(F(ch['wilson_mean_first_order_coefficient']['first_order_plus']) == c1 * tau
         and F(ch['wilson_mean_first_order_coefficient']['first_order_minus']) == -c1 * tau
         and {k: F(v) for k, v in ch['sign_convention_fixture']['one_plaquette_series'].items()}
         == {k: F(v) for k, v in pre['fixture_one_plaquette']['series'].items()}
         and [wf['faces_per_factor'], wf['faces_meeting_R'], wf['faces_with_owner_set_R'], wf['faces_touching_both_sites_of_R'], wf['omitted_classes']]
         == [pg['faces_per_site'], pg['meeting_R'], pg['owner_set_R'], pg['touching_both'], pg['anchored']]
         and hp['max_links_shared_with_W'] == pg['max_shared_links'] and hp['nonzero_pairings_with_W'] == '1'
         and {k: F(v) for k, v in hp['moments_character_route'].items() if k != '0'} == {str(n): haar_moment(n) for n in range(1, 9)},
         'producer_first_order_geometry_and_fixture_equal_to_pre_comparison',
         counts={'faces_per_factor': '49', 'meeting_R': '82', 'owner_set_R': '10', 'touching_both': '16', 'omitted_classes': '21'})
    ids = [c['id'] for c in res['checks']]
    need(len(ids) == 37 == int(res['check_count']) and len(set(ids)) == 37 and all(c['passed'] is True for c in res['checks'])
         and sum(len(c['mutations_rejected']) for c in res['checks']) == 116 == int(res['mutations_rejected_count'])
         and sha_bytes(res_raw) == 'ec09f259e0956eb347a792098b5a9af32e4563ca3cba25b38cfc189b1136abe0',
         'producer_37_checks_passed_116_mutations')
    per_control = {cid: len(ch[cid]['mutations_rejected']) for cid in controls if cid in ch}
    need(len(per_control) == 23 and all(v >= 1 for v in per_control.values())
         and res['contract_controls_covered'] == sorted(controls),
         'all_23_contract_controls_damaging_mutations', per_control={k: str(v) for k, v in per_control.items()},
         total=str(sum(per_control.values())))
    cp = ch['aw2_coupling_rule_prefrozen']['mutations_rejected']
    need(all(x in cp for x in ('literal_coupling_supplied', 'contract_text_used_as_coupling', 'not_the_largest_decade',
                               'off_grid_coupling', 'recomputed_forward_headline_constant', 'crude_constant_fed_to_rule',
                               'rule_bound_not_half_coefficient')),
         'producer_rejects_literal_and_non_rule_couplings', rejected=cp)
    need(all(res[k] is False for k in FALSE_FLAGS) and res['resolved_interaction_shift'] is True and res['static_not_dynamic'] is True
         and res['producers'] == ['forward'] and res['single_direction_independent_replay_required'] is True
         and res['minus_tau_status'] == 'replay' and res['sub_labels'] == ['static_not_dynamic']
         and res['reverse_premise_isolation'].startswith('not_applicable: single producer')
         and (lo > 0 and hi_m < 0 and tau == cap) is res['resolved_interaction_shift']
         and 'centered_correlation_shift_resolved' not in res
         and ch['static_not_dynamic_effect']['centered_correlation_shift'] == 'unresolved (AV2 reference_unresolved)',
         'producer_claim_flags', false_flags=list(FALSE_FLAGS), true_flags=['resolved_interaction_shift', 'static_not_dynamic'],
         naming_note='the producer carries correlation_shift_resolved:false and centered_correlation_shift "unresolved (AV2 reference_unresolved)"; '
                     'the key centered_correlation_shift_resolved is absent (same meaning; the pre-comparison replay carries it false)')
    sc = res['scope']
    need(sc['set'] == 'whole set of AQ1 subsequential limits' and sc['triple'] == ['0', '0', '0'] and sc['uniform_in_N'] is True
         and sc['passage'].startswith('local trace-norm convergence') and sc['effect'] == 'static equal-time mean'
         and sc['uniqueness_claimed'] is False and sc['rate_in_N_claimed'] is False and sc['whole_sequence_convergence_claimed'] is False
         and sc['finite_graph_transfer'] is False and sc['minus_tau_pointwise'].startswith('only along a common subsequence')
         and res['model']['model_id'] == 'AQ_patterned_zero_selected' and res['model']['cover'] == 'R={0,e_z}'
         and res['finite_fixture_labels']['transfers_to_aq'] is False,
         'producer_scope_record')

    # ---------------- literal-coupling protection, calculator, preview
    check_src = (FWD / 'check.py').read_text()
    calc_src = (FWD / 'calculator.py').read_text()
    flow = validate_coupling_dataflow(check_src, calc_src)
    asserts = [n for src in (check_src, calc_src) for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Assert)]
    need(isinstance(flow, dict) and asserts == [],
         'static_dataflow_tau_from_hash_checked_gate', dataflow=flow, asserts='none (controls survive -O)')
    bad_c, names_c = forbidden_imports(check_src)
    bad_k, names_k = forbidden_imports(calc_src)
    need(bad_c == [] and bad_k == [] and 'import flint' in (FWD / 'arb_preview.py').read_text(),
         'admission_path_imports_standard_library_only', check_imports=names_c, calculator_imports=names_k)
    calc_cases = {}
    with tempfile.TemporaryDirectory(prefix='hnm-r32-aw2-skeptic-imp-') as tmp:
        dst = Path(tmp) / 'repo' / FWD_REL
        shutil.copytree(FWD, dst, ignore=shutil.ignore_patterns('output', '__pycache__'))
        saved_path, saved_calc = list(sys.path), sys.modules.pop('calculator', None)
        try:
            spec = importlib.util.spec_from_file_location('aw2_forward_check_copy', dst / 'check.py')
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            calc = sys.modules['calculator']
            G = mod.parse_gate((dst / 'inputs/research/round32/advisor/aw1-gate.json').read_bytes())
            Rr = mod.parse_aw1_rule((dst / 'inputs' / AW1_CONTRACT_REL).read_bytes(), G)
            functional = [mod.aw2_rule(G['K'], Rr)[0], mod.aw2_rule(1000 * G['K'], Rr)[0], mod.aw2_rule(K_crude, Rr)[0]]
            need(G['K'] == K and functional == [F(1, 10 ** 8), F(1, 10 ** 9), F(1, 10 ** 10)],
                 'producer_rule_function_evaluates_its_argument', values=[q(x) for x in functional])

            def call(label, expect_error=None, **kw):
                try:
                    out = calc.enclose(**kw)
                except (ValueError, TypeError) as exc:
                    calc_cases[label] = type(exc).__name__
                    return exc if expect_error == type(exc).__name__ else None
                calc_cases[label] = 'accepted'
                return out if expect_error is None else None
            p = call('plus_fixed', tau='1/100000000', fixed_design=True)
            mi = call('minus_fixed', tau='-1/100000000', fixed_design=True)
            dt = call('decimal_text', tau='0.00000001')
            sc5 = call('scales', tau='1/100000000', fixed_design=True, alpha='5', hbar='7', E_star='11/2', lattice_spacing='3')
            bl = call('below_cap_reusable', tau='1/1000000000')
            rej = [call('above_cap', 'ValueError', tau='100000001/10000000000000000'), call('zero', 'ValueError', tau='0'),
                   call('float_tau', 'ValueError', tau=1e-08), call('bool_tau', 'ValueError', tau=True),
                   call('exponent_text', 'ValueError', tau='1e-8'), call('nonzero_triple', 'ValueError', tau='1/100000000', selected=('0', '0', '1/1000')),
                   call('float_triple', 'ValueError', tau='1/100000000', selected=('0', 0.0, '0')),
                   call('crude_tier', 'ValueError', tau='1/100000000', tier='crude'),
                   call('K_argument', 'TypeError', tau='1/100000000', K_2_plus='1'),
                   call('m_hat_argument', 'TypeError', tau='1/100000000', m_hat='0'),
                   call('zero_alpha', 'ValueError', tau='1/100000000', alpha='0'), call('negative_hbar', 'ValueError', tau='1/100000000', hbar='-1'),
                   call('fixed_design_wrong_tau', 'ValueError', tau='1/1000000000', fixed_design=True),
                   call('fixed_design_int', 'ValueError', tau='1/100000000', fixed_design=1)]
            gate_copy = dst / 'inputs/research/round32/advisor/aw1-gate.json'
            gate_copy.write_bytes(gate_copy.read_bytes().replace(b'81108864767825329926713064490531229475390625/',
                                                                 b'81108864767825329926713064490531229475390626/'))
            try:
                calc.enclose(tau='1/100000000')
                tamper = 'accepted'
            except calc.CalculatorError:
                tamper = 'CalculatorError'
            calc_cases['gate_snapshot_tampered'] = tamper
        finally:
            sys.path[:] = saved_path
            sys.modules.pop('calculator', None)
            if saved_calc is not None:
                sys.modules['calculator'] = saved_calc
    need(all(x is not None and not isinstance(x, Exception) for x in (p, mi, dt, sc5, bl))
         and [F(p['enclosure']['lower']), F(p['enclosure']['upper'])] == [lo, hi]
         and [F(mi['enclosure']['lower']), F(mi['enclosure']['upper'])] == [lo_m, hi_m]
         and dt['enclosure'] == p['enclosure'] and sc5['enclosure'] == p['enclosure']
         and F(p['exclusion_margin']) == m and F(p['sign_margin']) == S and p['sub_labels'] == ['static_not_dynamic']
         and p['sign_certified_below_cap'] is False and p['resolved_interaction_shift_at_cap'] is True and mi['mirrored_coupling_replay'] is True
         and bl['sub_labels'] == ['static_not_dynamic', 'sign_certified_below_cap'] and bl['resolved_interaction_shift_at_cap'] is False
         and F(bl['sign_margin']) == 10 * S and all(isinstance(x, Exception) for x in rej) and tamper == 'CalculatorError'
         and p['dynamical_correction_claim'] is False and p['continuum_claim'] is False,
         'calculator_domain_own_calls', cases=calc_cases,
         note='reusable mode below the cap is a corollary of the AW1 gate bound for |tau|<=10^-8; it is not an AW2 admission')
    pv_raw = (FWD / 'arb-preview.json').read_bytes()
    pv = json.loads(pv_raw)
    exact_q = {'+': {'lower': lo, 'upper': hi, 'sign_margin': S, 'exclusion_margin': m},
               '-': {'lower': lo_m, 'upper': hi_m, 'sign_margin': S, 'exclusion_margin': m}}
    need(pv['preview_only'] is True and pv['used_for_admission'] is False and pv['label'].startswith('PREVIEW ONLY')
         and all(F(pv['quantities'][sg][n][b]['lower']) <= x <= F(pv['quantities'][sg][n][b]['upper'])
                 for sg in exact_q for n, x in exact_q[sg].items() for b in ('arb_ball_bounds', 'mpmath_iv_bounds'))
         and ch['arb_mpmath_preview_labelled']['preview_sha256'] == sha_bytes(pv_raw)
         and "PREVIEW_FILE" not in ''.join(ast.unparse(fn) for fn in ast.parse(calc_src).body),
         'preview_labelled_and_contains_exact_values', libraries=pv['libraries'], precision_bits=pv['precision_bits'])

    # ---------------- source-edit mutations on temporary copies
    code0, base_res, base_man, last0, _ = mutated_run()
    need(code0 == 0 and base_res == res_raw and base_man == (FWD / 'output/source-manifest.json').read_bytes(),
         'mutation_harness_unmutated_copy_reproduces_frozen_output')

    def contract_target_300(raw):
        out = raw
        for old, new in ((b'"value": "2"', b'"value": "300"'),
                         (b'(K_2^+ tau^2) >= 2 (equivalently 1/(144 K_2^+ |tau|) >= 3)', b'(K_2^+ tau^2) >= 300 (equivalently 1/(144 K_2^+ |tau|) >= 301)'),
                         (b'margin >=2 at both signs', b'margin >=300 at both signs')):
            if out.count(old) != 1:
                raise ReviewFailure('contract target anchor not unique')
            out = out.replace(old, new)
        return out

    def preview_promoted(raw):
        return raw.replace(b'"used_for_admission": false', b'"used_for_admission": true')

    def preview_shifted(raw):
        d = json.loads(raw)
        d['quantities']['+']['lower']['arb_ball_bounds'] = {'lower': q(lo + F(1, 10 ** 20)), 'upper': q(lo + F(2, 10 ** 20))}
        return (json.dumps(d, indent=2, sort_keys=True) + '\n').encode()
    kn = str(K.numerator).encode()
    GATE = 'inputs/research/round32/advisor/aw1-gate.json'
    CON = 'inputs/research/round32/contracts/aw2.json'
    must_abort = [
        ('first_order_sign_flipped', {'edits': {'check.py': [("    first = c1 * tau\n", "    first = -c1 * tau\n")]}}),
        ('literal_coupling_1e-9', {'edits': {'check.py': [("    tau_aw2, steps = aw2_rule(K, R)\n",
                                                          "    tau_aw2, steps = Q(1, 10 ** 9), [(Q(1, 10 ** 9), K * Q(1, 10 ** 9), True)]\n")]}}),
        ('K_halved_after_gate_read', {'edits': {'check.py': [("    K, c1, cap = G['K'], G['c1'], G['cap']\n",
                                                              "    K, c1, cap = G['K'] / 2, G['c1'], G['cap']\n")]}}),
        ('radius_halved', {'edits': {'check.py': [("    radius = K * tau * tau\n", "    radius = K * tau * tau / 2\n")]}}),
        ('exclusion_margin_over_first_order', {'edits': {'check.py': [("'exclusion_margin': (f - r) / r}", "'exclusion_margin': (f - r) / f}")]}}),
        ('minus_enclosure_sign_blind', {'edits': {'check.py': [("'-': enclosure(-tau_aw2, K, c1)}", "'-': enclosure(tau_aw2, K, c1)}")]}}),
        ('crude_reported_excluding_zero', {'edits': {'check.py': [("    rep = {'crude_excludes_zero_at_cap': False,", "    rep = {'crude_excludes_zero_at_cap': True,")]}}),
        ('below_cap_flag_true', {'edits': {'check.py': [("'static_not_dynamic': True, 'sign_certified_below_cap': False,",
                                                         "'static_not_dynamic': True, 'sign_certified_below_cap': True,")]}}),
        ('dynamical_correction_flag_true', {'edits': {'check.py': [("'sign_certified_below_cap': False, 'dynamical_correction_claim': False,",
                                                                    "'sign_certified_below_cap': False, 'dynamical_correction_claim': True,")]}}),
        ('static_not_dynamic_flag_false', {'edits': {'check.py': [("'static_not_dynamic': True, 'sign_certified_below_cap': False,",
                                                                   "'static_not_dynamic': False, 'sign_certified_below_cap': False,")]}}),
        ('correlation_shift_resolved_true', {'edits': {'check.py': [("'correlation_shift_resolved': False, 'uniqueness_claim': False,",
                                                                     "'correlation_shift_resolved': True, 'uniqueness_claim': False,")]}}),
        ('rule_threshold_equal_to_coefficient', {'edits': {'check.py': [("'bound': Q(int(m.group(3)), int(m.group(4))),", "'bound': Q(1, 144),")]}}),
        ('rule_grid_start_shifted', {'edits': {'check.py': [("    k = R['start']\n", "    k = R['start'] + 1\n")]}}),
        ('decimal_lower_rounded_inward', {'edits': {'check.py': [("'lower_decimal_outward_down': dec_down(E['lower'])", "'lower_decimal_outward_down': dec_up(E['lower'])")]}}),
        ('mirror_counted_as_independent', {'edits': {'check.py': [("'reverse_premise_isolation': reverse_isolation, 'minus_tau_status': 'replay',\n",
                                                                   "'reverse_premise_isolation': reverse_isolation, 'minus_tau_status': 'independent_confirmation',\n")]}}),
        ('mpmath_import_in_admission_path', {'edits': {'check.py': [("import json\nimport re\n", "import json\nimport mpmath\nimport re\n")]}}),
        ('validator_strict_exclusion_weakened', {'edits': {'check.py': [("            require(lo > V['reference'], ", "            require(lo >= V['reference'], ")]}}),
        ('validator_incoming_stars_disabled', {'edits': {'check.py': [("        require(k2_replay(tau_aw2, G, stars_per_site=stars)['K'] == K, 'J must count all four incoming stars (J=28|tau|)')\n",
                                                                       "        pass\n")]}}),
        ('validator_below_cap_label_disabled', {'edits': {'check.py': [("        require(('sign_certified_below_cap' in labels) == (t < cap), ",
                                                                        "        require(True or ('sign_certified_below_cap' in labels) == (t < cap), ")]}}),
        ('validator_claim_flags_disabled', {'edits': {'check.py': [("            require(fl[k] is False, 'claim flag must be false: ' + k)\n", "            pass\n")]}}),
        ('calculator_accepts_float', {'edits': {'calculator.py': [("    if isinstance(value, bool) or isinstance(value, float):\n",
                                                                   "    if isinstance(value, float):\n        return Q(value)\n    if isinstance(value, bool):\n")]}}),
        ('calculator_cap_check_removed', {'edits': {'calculator.py': [("    if abs(t) > G['cap']:\n", "    if False:\n")]}}),
        ('calculator_nonzero_triple_allowed', {'edits': {'calculator.py': [("    if any(triple):\n", "    if False:\n")]}}),
        ('gate_K_digit_edited_no_rehash', {'file_edits': {GATE: lambda raw: raw.replace(kn + b'/', str(K.numerator + 1).encode() + b'/')}}),
        ('gate_K_doubled_rehashed_in_check_and_calculator', {'file_edits': {GATE: lambda raw: raw.replace(kn + b'/', str(2 * K.numerator).encode() + b'/')},
                                                             'rehash_gate': True}),
        ('contract_target_300_rehashed', {'file_edits': {CON: contract_target_300}, 'rehash_contract': True}),
        ('contract_reference_nonzero_rehashed', {'file_edits': {CON: lambda raw: raw.replace(b'"reference_value_exact": "0"', b'"reference_value_exact": "1/144"')},
                                                 'rehash_contract': True}),
        ('contract_edited_no_rehash', {'file_edits': {CON: lambda raw: raw.replace(b'"value": "2"', b'"value": "1"')}}),
        ('i1_phi_sign_flipped_no_rehash', {'file_edits': {'inputs/' + I1_REL: lambda raw: raw.replace(b'=-{\\tau\\over3}\\sum_{f\\in O_b}W_f', b'=+{\\tau\\over3}\\sum_{f\\in O_b}W_f')}}),
        ('undeclared_input_skeptic_aw2', {'extra_input': 'research/round32/skeptic/aw2-independent-derivation.md'}),
        ('premise_snapshot_removed', {'remove': ('inputs/research/round32/skeptic/aw1.md',)}),
        ('preview_promoted_to_admission', {'file_edits': {'arb-preview.json': preview_promoted}}),
        ('preview_bound_excluding_exact_endpoint', {'file_edits': {'arb-preview.json': preview_shifted}}),
    ]
    receipts = []
    for label, spec_m in must_abort:
        code, results, _, last, _ = mutated_run(**spec_m)
        need(code != 0 and results is None, 'mutation_aborts_' + label, last_error_line=last)
        receipts.append({'mutation': label, 'producer_aborted': True, 'last_error_line': last})
    target_receipt = [r for r in receipts if r['mutation'] == 'contract_target_300_rehashed'][0]
    need(target_receipt['last_error_line'] == 'AdmissionError: failed check zero_exclusion_and_margins',
         'target_read_from_contract_demonstration',
         finding='with the contract target raised to 300 and the pin rehashed, the producer fails exactly at the exclusion-margin check: '
                 'the target is read from the contract snapshot, not typed into check.py')

    # silent edit: a literal coupling equal to the rule value runs to completion; only source review catches it
    code, results, _, last, (msrc, mcalc) = mutated_run(edits={'check.py': [("    tau_aw2, steps = aw2_rule(K, R)\n",
                                                                              "    tau_aw2, steps = Q(1, 10 ** 8), [(Q(1, 10 ** 8), K * Q(1, 10 ** 8), True)]\n")]})
    caught, reason = False, ''
    try:
        validate_coupling_dataflow(msrc, mcalc)
    except Rejected as exc:
        caught, reason = True, str(exc)
    diff = json_diff(res, json.loads(results)) if results is not None else ['<no output>']
    need(code == 0 and caught and all(('check_py_sha256' in d) for d in diff) and len(diff) >= 1,
         'silent_literal_coupling_caught_by_static_review', producer_exit=str(code), review_rejection=reason, changed_fields=diff)
    receipts.append({'mutation': 'literal_coupling_equal_to_rule_value', 'producer_aborted': False,
                     'caught_by_skeptic_dataflow_validator': True, 'reason': reason, 'changed_fields': diff})

    # preview non-dependence: exact point balls in place of the stored previews change no admitted value
    def preview_points(raw):
        d = json.loads(raw)
        for sg in exact_q:
            for n, x in exact_q[sg].items():
                for b in ('arb_ball_bounds', 'mpmath_iv_bounds'):
                    d['quantities'][sg][n][b] = {'lower': q(x), 'upper': q(x)}
        return (json.dumps(d, indent=2, sort_keys=True) + '\n').encode()
    code, results, _, last, _ = mutated_run(file_edits={'arb-preview.json': preview_points})
    diff = json_diff(res, json.loads(results)) if results is not None else ['<no output>']
    need(code == 0 and diff == ['/checks/arb_mpmath_preview_labelled/preview_sha256'],
         'preview_non_dependence_of_admitted_values', changed_fields=diff)
    receipts.append({'mutation': 'preview_replaced_by_exact_point_balls', 'producer_aborted': False,
                     'changed_fields': diff, 'note': 'no admitted value, flag or verdict depends on the preview'})
    code, results, _, last, _ = mutated_run(remove=('arb-preview.json',))
    need(code != 0 and results is None and last.startswith('FileNotFoundError'),
         'preview_absence_aborts_veto_only', last_error_line=last,
         note='the checker reads the stored preview as a labelled comparison: a missing or inconsistent preview aborts the run '
              '(veto only); it never supplies an admitted value')
    receipts.append({'mutation': 'preview_file_removed', 'producer_aborted': True, 'last_error_line': last,
                     'note': 'veto-only dependency'})

    exact = {
        'K_2_plus': q(K), 'K_2_plus_outward_ceiling': q(gc['ceiling']), 'first_order_coefficient': q(c1),
        'contract_display_literal': q(literal_display), 'tau_AW2': q(tau), 'rule_threshold': q(threshold),
        'rule_K_tau': q(K * tau), 'rule_slack': q(threshold - K * tau),
        'enclosure_plus': [q(lo), q(hi)], 'enclosure_minus': [q(lo_m), q(hi_m)], 'first_order_plus': q(first),
        'radius': q(rad), 'exclusion_margin': q(m), 'sign_margin': q(S),
        'exclusion_margin_floor_1e-9': q(floor_to(m, 10 ** 9)), 'sign_margin_floor_1e-9': q(floor_to(S, 10 ** 9)),
        'crude_K2': q(K_crude), 'crude_enclosure': [q(clo), q(chi_)], 'crude_sign_margin': q(cfirst / crad),
        'D_ii_av1': q(D_ii), 'itemization_terms_at_cap': {k: q(v) for k, v in terms.items()},
    }
    previews = {
        'enclosure_plus': [directed(lo, False), directed(hi, True)], 'enclosure_minus': [directed(lo_m, False), directed(hi_m, True)],
        'exclusion_margin': directed(m, False), 'sign_margin': directed(S, False), 'K_2_plus': directed(K, True),
        'crude_enclosure': [directed(clo, False), directed(chi_, True)], 'crude_sign_margin': directed(cfirst / crad, True),
        'note': 'directed 12-digit decimals (enclosures widened outward, margins rounded down, K_2^+ up); '
                'display only; every Boolean above was decided on exact rationals',
    }
    return {
        'schema': 'hnm-r32-skeptic-postcomparison-v1', 'loop': 'AW2', 'stage': 'post_comparison',
        'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'model-agent skeptic with correlated ancestry; not human peer review or formal verification',
        'contract_sha256': CONTRACT_SHA, 'aw1_gate_sha256': AW1_GATE_SHA, 'producer_results_sha256': sha_bytes(res_raw),
        'exact': exact, 'previews': previews, 'mutation_receipts': receipts, 'passed': True,
        'checks': CHECKS, 'checks_count': len(CHECKS),
        'must_abort_mutations_aborted': sum(1 for r in receipts if r['producer_aborted'] and r['mutation'] != 'preview_file_removed'),
    }


def main():
    ap = argparse.ArgumentParser(description='AW2 post-comparison skeptic checks')
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
    print(json.dumps({'loop': 'AW2', 'stage': 'post_comparison', 'checks': result['checks_count'],
                      'enclosure_plus': result['previews']['enclosure_plus'],
                      'exclusion_margin': result['previews']['exclusion_margin'],
                      'sign_margin': result['previews']['sign_margin'],
                      'mutations': len(result['mutation_receipts'])}, sort_keys=True))


if __name__ == '__main__':
    main()
