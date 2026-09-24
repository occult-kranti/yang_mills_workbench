#!/usr/bin/env python3
"""AZ1 forward producer (single producer of a statement+skeptic loop): exact checks for the
Hruday continuum-trajectory statement -- the one estimate the fixed-spacing uniform Kogut-Susskind
SU(2) family supplies (the volume-uniform gap alpha/16=g^2/(32a) at fixed a, cited from the AX1
gate) and its failure point along a named trajectory (a_n,g_n) with g_n->0.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production (a Claude model agent).

Standard library only (argparse, fractions, hashlib, json, math, pathlib, re).  Every admission
Boolean is decided in exact Fraction or integer arithmetic; decimal strings are truncated previews.
Conditions raise AdmissionError explicitly (never `assert`), so every check stays active under
`python -O`.  The contract snapshot is sha256-verified before any evaluation; every admitted
constant is read from the sha256-bound snapshots in inputs/ (the frozen AZ1 contract, the AX1,
AL1 and AM2 gates and the reports they bind); the only typed values are labelled declarations (the
example spacing a_0, the reference E_star, the exact test grid, the hbar*c preview) and the identity
strings that are being verified.

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
CONTRACT_REL = 'research/round32/contracts/az1.json'
CONTRACT_SHA256 = '91c828a7aa6ef9bd4d3dbf762363b7558faa6922c23e1aff476cd098d4177078'
HUMAN_AUTHOR = 'Hruday N M (BUNZEEY)'
LABEL = 'uniform Kogut\u2013Susskind SU(2) at fixed spacing, strong bare coupling'
UNIFORM_IN_N_SCOPE = 'volume-uniform at fixed a, strong bare coupling'

P_AX1_GATE = 'research/round32/advisor/ax1-gate.json'
P_AL1_GATE = 'research/round29/advisor/al1-gate.json'
P_AM2_GATE = 'research/round29/advisor/am2-gate.json'
P_AL1F = 'research/round29/forward/al1/report.md'
P_AX1F = 'research/round32/forward/ax1/report.md'
P_AX1R = 'research/round32/reverse/ax1/report.md'
P_AX1S = 'research/round32/skeptic/ax1.md'
P_AM2R = 'research/round29/reverse/am2/report.md'
P_AM2S = 'research/round29/skeptic/am2.md'
P_AT4 = 'research/round31/forward/at4/report.md'
P_I1 = 'research/round21/forward/i1/report.md'
P_AQ1 = 'research/round29/forward/aq1/report.md'
P_SEL = 'research/round32/advisor/selection-az1.md'
P_MOD4 = 'research/round32/experts/modern/update-4.md'
P_HIS4 = 'research/round32/experts/historical/update-4.md'
P_MEMO = 'research/round32/experts/modern/memo.md'
P_SOTA = 'research/round32/experts/modern/sota-table.md'

# Declared (not admitted) example scales for the physical-units statement; E_star is a fixed positive reference.
A0_FM = Q(1, 10)                  # a_0 = 1/10 fm (declared)
E_STAR_LABEL = 'E_star = hbar*c/(1 fm) (declared fixed positive reference; about 197.327 MeV, preview)'
HBARC_MEV_FM_PREVIEW = '197.3269804'   # CODATA 2018 hbar*c in MeV fm, truncated; preview conversion only


class AdmissionError(Exception):
    """An admission condition failed or a damaging mutation was accepted."""


def require(condition, message):
    if not condition:
        raise AdmissionError(message)


CHECKS = []
PENDING = []   # labels of damaging mutations rejected since the previous recorded check


def check(identity, condition, **details):
    require(condition, 'failed check ' + identity)
    require(all(c['id'] != identity for c in CHECKS), 'duplicate check id ' + identity)
    entry = {'id': identity, 'passed': True}
    entry.update(details)
    if PENDING:
        entry['rejected_mutations'] = list(PENDING)
        del PENDING[:]
    CHECKS.append(entry)


def rejected(mutation, label):
    """Run a damaging mutation; it must raise AdmissionError."""
    try:
        mutation()
    except AdmissionError:
        PENDING.append(label)
        return label
    raise AdmissionError('damaging mutation accepted: ' + label)


def rat(value):
    """Exact rational input only: int, Fraction or an integer/ratio string."""
    if isinstance(value, bool) or isinstance(value, float):
        raise AdmissionError('non-exact input rejected: ' + repr(value))
    if isinstance(value, (int, Q)):
        return Q(value)
    if isinstance(value, str) and re.fullmatch(r'-?\d+(/\d+)?', value):
        num, _, den = value.partition('/')
        if den and int(den) == 0:
            raise AdmissionError('zero denominator rejected')
        return Q(int(num), int(den) if den else 1)
    raise AdmissionError('malformed rational rejected: ' + repr(value))


def sci(text):
    """Exact value of a premise string such as '9.6x10^9' or '10^-8' (mantissa and integer exponent)."""
    m = re.fullmatch(r'(?:(\d+)(?:\.(\d+))?x)?10\^(-?\d+)', text)
    require(m is not None, 'malformed scientific literal ' + repr(text))
    mant = Q(1)
    if m.group(1) is not None:
        frac = m.group(2) or ''
        mant = Q(int(m.group(1) + frac), 10 ** len(frac))
    return mant * Q(10) ** int(m.group(3))


def s(q):
    return str(Q(q))


def dec(q, digits=12):
    """Truncated scientific decimal preview of an exact rational (never an admission value)."""
    q = Q(q)
    if q == 0:
        return '0'
    sign = '-' if q < 0 else ''
    q = abs(q)
    e = 0
    while q >= Q(10) ** (e + 1):
        e += 1
    while q < Q(10) ** e:
        e -= 1
    scaled = q / Q(10) ** (e - digits + 1)
    m = str(scaled.numerator // scaled.denominator)
    return sign + m[0] + '.' + m[1:] + 'e' + str(e)


def preview_value(text):
    """Parse a decimal preview string into an exact Fraction (comparison/preview only, never admission)."""
    require(re.fullmatch(r'-?\d+(\.\d+)?(e-?\d+)?', text) is not None, 'malformed preview ' + text)
    mant, _, ex = text.partition('e')
    return Q(mant) * Q(10) ** int(ex or '0')


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


SQRT_SCALE = 10 ** 30


def sqrt_bracket(n, scale=SQRT_SCALE):
    """Directed rational bracket lo <= sqrt(n) <= hi of a nonnegative rational, from integer square roots."""
    n = rat(n)
    require(n >= 0, 'square root of a negative number')
    k = isqrt(n.numerator * scale * scale // n.denominator)
    while Q(k + 1, scale) ** 2 <= n:
        k += 1
    while Q(k, scale) ** 2 > n:
        k -= 1
    lo = Q(k, scale)
    hi = lo if lo * lo == n else Q(k + 1, scale)
    require(lo * lo <= n <= hi * hi and hi - lo <= Q(1, scale), 'directed square-root bracket')
    return lo, hi


def read_input(rel):
    return (BASE / 'inputs' / rel).read_text(encoding='utf-8')


def load_json_input(rel):
    return json.loads(read_input(rel))


def match(pattern, text, label, flags=0):
    m = re.search(pattern, text, flags)
    require(m is not None, 'premise text not parsed: ' + label)
    return m


def strip_code(text):
    text = re.sub(r'```.*?```', ' ', text, flags=re.S)
    return re.sub(r'`[^`\n]*`', ' ', text)


# ---------------------------------------------------------------------------
# Integer-coefficient polynomials in (g, a, c) and rational functions num/den (the symbolic route).
# c is an auxiliary scale variable used only for rescaling and homogeneity identities.
# ---------------------------------------------------------------------------
VARS = ('g', 'a', 'c')


def pnorm(p):
    return {k: v for k, v in p.items() if v != 0}


def padd(p, q):
    r = dict(p)
    for k, v in q.items():
        r[k] = r.get(k, 0) + v
    return pnorm(r)


def pmul(p, q):
    r = {}
    for k1, v1 in p.items():
        for k2, v2 in q.items():
            k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
            r[k] = r.get(k, 0) + v1 * v2
    return pnorm(r)


def pconst(k):
    require(isinstance(k, int) and not isinstance(k, bool), 'integer polynomial coefficient required: ' + repr(k))
    return pnorm({(0, 0, 0): k})


def pvar(name):
    e = [0, 0, 0]
    e[VARS.index(name)] = 1
    return {tuple(e): 1}


def rf(num, den=None):
    den = pconst(1) if den is None else den
    require(bool(den), 'zero denominator polynomial')
    return (num, den)


def rmul(x, y):
    return rf(pmul(x[0], y[0]), pmul(x[1], y[1]))


def rdiv(x, y):
    require(bool(y[0]), 'division by the zero rational function')
    return rf(pmul(x[0], y[1]), pmul(x[1], y[0]))


def radd(x, y):
    return rf(padd(pmul(x[0], y[1]), pmul(y[0], x[1])), pmul(x[1], y[1]))


def rneg(x):
    return rf({k: -v for k, v in x[0].items()}, x[1])


def rpow(x, n):
    if n < 0:
        return rpow(rdiv(rf(pconst(1)), x), -n)
    r = rf(pconst(1))
    for _ in range(n):
        r = rmul(r, x)
    return r


def req(x, y):
    """Identity of two rational functions by cross-multiplication of integer polynomials."""
    return pmul(x[0], y[1]) == pmul(y[0], x[1])


def rsubst_scale(x, var):
    """Substitute var -> c*var (multiply every monomial by c^(degree in var))."""
    idx = VARS.index(var)

    def sub(p):
        return pnorm({(k[0], k[1], k[2] + k[idx]): v for k, v in p.items()})
    return rf(sub(x[0]), sub(x[1]))


def reval(x, g2, a, c=1):
    """Exact value at rational g^2, a, c; every g exponent must be even (the dictionary is a function of g^2)."""
    g2, a, c = rat(g2), rat(a), rat(c)

    def ev(p):
        tot = Q(0)
        for (i, j, k), v in p.items():
            require(i % 2 == 0, 'odd power of g in a dictionary expression')
            tot += v * g2 ** (i // 2) * a ** j * c ** k
        return tot
    d = ev(x[1])
    require(d != 0, 'evaluation at a pole')
    return ev(x[0]) / d


TOKEN_RE = re.compile(r'\s*(\d+|[A-Za-z_]+|\^|\*|/|\(|\)|\+|-)')


def tokenize(text):
    text = text.strip()
    pos, out = 0, []
    while pos < len(text):
        m = TOKEN_RE.match(text, pos)
        require(m is not None and m.end() > pos, 'untokenizable expression: ' + text)
        out.append(m.group(1))
        pos = m.end()
    return out


def parse_rf(text, env):
    """Recursive-descent parser for the dictionary strings (implicit multiplication as in '32a', 'g^2 a')."""
    toks = tokenize(text)
    i = [0]

    def peek():
        return toks[i[0]] if i[0] < len(toks) else None

    def take():
        t = peek()
        i[0] += 1
        return t

    def atom():
        t = take()
        require(t is not None, 'unexpected end of expression: ' + text)
        if t.isdigit():
            return rf(pconst(int(t)))
        if t == '(':
            v = expr()
            require(take() == ')', 'unbalanced parenthesis: ' + text)
            return v
        if t == '-':
            return rneg(power())
        require(t in env, 'unknown symbol ' + t + ' in ' + text)
        return env[t]

    def power():
        b = atom()
        if peek() == '^':
            take()
            sign = 1
            if peek() == '-':
                take()
                sign = -1
            t = take()
            require(t is not None and t.isdigit(), 'integer exponent required: ' + text)
            b = rpow(b, sign * int(t))
        return b

    def term():
        v = power()
        while True:
            t = peek()
            if t == '*':
                take()
                v = rmul(v, power())
            elif t == '/':
                take()
                v = rdiv(v, power())
            elif t is not None and (t.isdigit() or t == '(' or re.fullmatch(r'[A-Za-z_]+', t)):
                v = rmul(v, power())
            else:
                return v

    def expr():
        v = term()
        while peek() in ('+', '-'):
            op = take()
            w = term()
            v = radd(v, w if op == '+' else rneg(w))
        return v
    v = expr()
    require(peek() is None, 'trailing tokens in ' + text)
    return v


def identity_holds(text, env):
    parts = text.split('=')
    require(len(parts) == 2, 'identity must have exactly one = : ' + text)
    return req(parse_rf(parts[0], env), parse_rf(parts[1], env))


BASE_ENV = {'g': rf(pvar('g')), 'a': rf(pvar('a')), 'c': rf(pvar('c'))}


def build_dictionary(alpha_text, lambda_text, tau_coef):
    """Primary AL1 definitions alpha, lambda; tau := tau_coef*lambda/alpha (AL1.2: nu=lambda=alpha*tau/24); r := lambda/alpha."""
    alpha = parse_rf(alpha_text, BASE_ENV)
    lam = parse_rf(lambda_text, BASE_ENV)
    env = dict(BASE_ENV)
    env['alpha'] = alpha
    env['lambda'] = lam
    env['tau'] = rdiv(rmul(rf(pconst(tau_coef)), lam), alpha)
    env['r'] = rdiv(lam, alpha)
    return env


def validate_dictionary(env, identities):
    for ident in identities:
        require(identity_holds(ident, env), 'dictionary identity fails: ' + ident)
    return True


def exponent_of(x, var, lo=-8, hi=8):
    """The integer k with x(var -> c*var) = c^k x(var), found by exact cross-multiplication; error if not homogeneous."""
    xs = rsubst_scale(x, var)
    for k in range(lo, hi + 1):
        if req(xs, rmul(x, rpow(BASE_ENV['c'], k))):
            return k
    raise AdmissionError('not homogeneous in ' + var)


# ---------------------------------------------------------------------------
# Toy-trajectory crossovers: exact integer arithmetic, two routes.
# ---------------------------------------------------------------------------
def iroot(F, p):
    """Largest integer m >= 0 with m^p <= F (p in 1, 2, 4), with an explicit bracket check."""
    require(isinstance(F, int) and F >= 0 and p in (1, 2, 4), 'integer root arguments')
    m = F if p == 1 else (isqrt(F) if p == 2 else isqrt(isqrt(F)))
    require(m ** p <= F < (m + 1) ** p, 'integer root bracket m^p<=F<(m+1)^p')
    return m


def crossover_root(g04, T, p=4):
    """First n>=1 with g04/n^p < T, by the exact integer p-th root of floor(g04/T)."""
    g04, T = rat(g04), rat(T)
    require(g04 > 0 and T > 0, 'positive coupling and threshold required')
    X = g04 / T
    if X < 1:
        n = 1
    else:
        F = X.numerator // X.denominator
        n = iroot(F, p) + 1
    require(g04 / n ** p < T and (n == 1 or g04 / (n - 1) ** p >= T), 'crossover bracket')
    return n


def crossover_scan(g04, T, limit, p=4):
    """First n>=1 with g04/n^p < T, by an exact Fraction scan (second route)."""
    g04, T = rat(g04), rat(T)
    for n in range(1, limit + 1):
        if g04 / Q(n) ** p < T:
            return n
    raise AdmissionError('no crossover within the scan limit')


def validate_crossover(g04, T, n_claim):
    """A claimed crossover index must be the FIRST n with g_n^4 = g04/n^4 strictly below T (n=1 included)."""
    g04, T = rat(g04), rat(T)
    require(isinstance(n_claim, int) and not isinstance(n_claim, bool) and n_claim >= 1, 'crossover index must be a positive integer')
    require(g04 / Q(n_claim) ** 4 < T, 'g_n^4 is not below the threshold at the claimed index')
    require(n_claim == 1 or g04 / Q(n_claim - 1) ** 4 >= T, 'the claimed index is not the first crossover')
    return True


def forward_verdict(citation_present, arithmetic_exact, overclaim):
    """Contract acceptance: insufficient on overclaim; limited when the failure point is stated without the
    supplied estimate's proof citation (or, producer reading, with inexact dictionary arithmetic);
    otherwise accepted_within_scope, which the skeptic's independent derivation and replays must still confirm."""
    if overclaim:
        return 'insufficient'
    if not citation_present or not arithmetic_exact:
        return 'limited'
    return 'accepted_within_scope'


def float_free(obj):
    if isinstance(obj, float):
        return False
    if isinstance(obj, dict):
        return all(float_free(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(float_free(v) for v in obj)
    return True


# ---------------------------------------------------------------------------
# I1 coarse geometry (owner map, factor links, face supports) for the inherited incidence controls.
# ---------------------------------------------------------------------------
E_UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
PAIRS = ((0, 1), (0, 2), (1, 2))


def vadd(p, q):
    return tuple(x + y for x, y in zip(p, q))


def vsub(p, q):
    return tuple(x - y for x, y in zip(p, q))


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def tails(b):
    return [(4 * b[0] + r, 2 * b[1] + t, b[2]) for r in range(4) for t in range(2)]


def factor_links(b):
    return [(tl, d) for tl in tails(b) for d in range(3)]


def face_support(p, a, c):
    return frozenset({owner(p), owner(vadd(p, E_UNIT[a])), owner(vadd(p, E_UNIT[c]))})


def is_selected(p, a, c):
    return (a, c) == (0, 1) and p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)


def incidence(region, anchors, single_groups):
    """Faces charged by whole stars anchored at `anchors` and by the single-factor groups at `single_groups`."""
    out = {'stars': len(anchors), 'groups': len(single_groups), 'charged': 0, 'meet': 0, 'meet_omitted': 0,
           'meet_selected': 0, 'inside': 0}
    for b in sorted(anchors):
        for p in tails(b):
            for a, c in PAIRS:
                if is_selected(p, a, c):
                    continue
                sp = face_support(p, a, c)
                out['charged'] += 1
                if sp & region:
                    out['meet'] += 1
                    out['meet_omitted'] += 1
                if sp <= region:
                    out['inside'] += 1
    for b in sorted(single_groups):
        for p in tails(b):
            for a, c in PAIRS:
                if not is_selected(p, a, c):
                    continue
                sp = face_support(p, a, c)
                out['charged'] += 1
                if sp & region:
                    out['meet'] += 1
                    out['meet_selected'] += 1
                if sp <= region:
                    out['inside'] += 1
    return out


# ---------------------------------------------------------------------------
# Contract: every target, control id, template and phrase is read from the sha256-bound snapshot.
# ---------------------------------------------------------------------------
def load_contract():
    raw = (BASE / 'inputs' / CONTRACT_REL).read_bytes()
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen AZ1 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'AZ1' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return c, digest


def contract_values(c):
    pre = c['preregistration']
    v = {}
    v['model'] = c['model']
    require('uniform Kogut-Susskind SU(2) family (AX1)' in v['model'] and 'E_star fixed' in v['model'] and 'no plateau fit' in v['model'], 'model string')
    v['tau_cap'] = rat(pre['tau']['value'])
    require(v['tau_cap'] == Q(1, 10 ** 8), 'preregistered tau')
    v['signs'] = list(pre['tau']['signs_evaluated'])
    require(v['signs'] == ['+', '-'], 'both signs recorded')
    require(pre['tau']['is_model_change_vs_previous_loop'] is False and pre['tau']['rule_if_chosen_later'] is None, 'tau rule')
    v['triple'] = [rat(x) for x in pre['selected_triple_alpha_units']]
    v['model_id'] = pre['model_id']
    require(v['model_id'] == 'AQ_uniform_routeB along (a_n,g_n)', 'model id')
    v['state_provenance'] = pre['state_provenance']
    obs = pre['observable']
    v['observable_id'] = obs['id']
    v['centering'] = obs['centering']
    require(obs['id'] == 'statement' and obs['centering'] == 'none' and obs['reference_value_exact'] == 'n/a' and obs['reference_route'] == 'n/a', 'observable block')
    v['clock'] = pre['clock']
    m = match(r'^(s=alpha\*t_E/hbar, theta=alpha\*t/hbar); u=s/(\d+) and exponent (\d+) forbidden in packets$', v['clock'], 'clock')
    v['clock_common'], v['forbidden_u_div'], v['forbidden_exponent'] = m.group(1), int(m.group(2)), int(m.group(3))
    tg = pre['target']
    v['target'] = rat(tg['value'])
    v['target_quantity'] = tg['quantity']
    v['target_comparator'] = tg['comparator']
    require(tg['comparator'] == '>=' and 'crossover indices' in tg['quantity'] and 'dictionary identities' in tg['quantity'], 'target comparator/quantity')
    v['error_terms'] = list(pre['error_terms_itemized'])
    require(len(v['error_terms']) == 1 and v['error_terms'][0].startswith('not_applicable: statement loop (reason:'), 'one error term, not_applicable with a reason')
    v['error_terms_rule'] = pre['error_terms_rule']
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    v['outcomes'] = list(pre['expected_outcome_types'])
    v['gate_fields'] = dict(pre['gate_fields_required'])
    v['template'] = pre['mandatory_sentence_template']
    v['forbidden'] = list(pre['forbidden_phrasings'])
    require(v['forbidden'] == ['the continuum limit exists', 'fraction of the problem'], 'forbidden phrasings')
    v['controls'] = list(c['controls'])
    require(v['controls'] == list(pre['controls_required']['ids']) and len(v['controls']) == 21, 'controls list equals the preregistered ids')
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    v['acceptance'] = dict(c['acceptance'])
    v['shared'] = list(c['shared_premises'])
    v['required'] = list(c['required'])
    require(len(v['required']) == 6, 'six required items')
    v['hash_binding'] = dict(pre['hash_binding'])
    require(all(v['hash_binding'].get(k) is True for k in ('contract_sha256_in_producer_inputs', 'check_py_reads_target_and_reference_from_contract',
                                                          'check_py_sha256_recorded_before_full_size_evaluation')), 'hash binding')
    require(c['direction'] == 'statement+skeptic' and pre['direction'] == 'statement+skeptic' and c['producers'] == ['forward'], 'direction')
    require(c.get('single_direction_independent_replay') is True, 'single-direction independent replay declared')
    par = c['parameters']
    v['par'] = par
    v['dictionary_text'] = par['dictionary']
    defs = dict(x.split('=', 1) for x in par['dictionary'].split(', '))
    require(sorted(defs) == ['alpha', 'lambda', 'tau'], 'dictionary parameter names')
    v['alpha_text'], v['lambda_text'], v['tau_text'] = defs['alpha'], defs['lambda'], defs['tau']
    v['identities'] = list(par['dictionary_identities'])
    require(v['identities'] == ['alpha/16=g^2/(32a)', 'tau=96/g^4', 'alpha*lambda*a^2=1'], 'dictionary identities')
    v['toy_text'] = par['toy_trajectory']
    m = match(r'g_n=g_0/n, n>=1, at fixed E_star; g_0\^4=([\dx.^]+) \(the cap\) declared', v['toy_text'], 'toy trajectory declaration')
    v['toy_g04'] = sci(m.group(1))
    v['supplied_text'] = par['supplied']
    m = match(r'^volume-uniform gap (alpha/16=g\^2/\(32a\)) for g\^4>=([\dx.^]+) at fixed a$', v['supplied_text'], 'supplied estimate')
    v['supplied_identity'], v['supplied_g4'] = m.group(1), sci(m.group(2))
    v['failed_text'] = par['failed']
    m = match(r'the AM2 contraction needs tau<=(10\^-\d+) i\.e\. g\^4>=([\dx.^]+), violated on every g->0 path; the AL1 bridge condition g\^4>=(\d+) also fails',
              v['failed_text'], 'failed estimate')
    v['failed_tau'], v['failed_g4'], v['bridge_g4'] = sci(m.group(1)), sci(m.group(2)), rat(m.group(3))
    m = match(r'additionally require \(([^)]*)\) with the missing premise for each', v['required'][3], 'continuum requirement names')
    v['requirement_names'] = [x.strip() for x in m.group(1).split(',')]
    require(v['requirement_names'] == ['uniform-in-a estimates', 'reconstruction hypotheses', 'physical scale control'], 'three requirement names')
    m = match(r"uniform_in_N_claimed true with the scope string '([^']+)'", v['required'][4], 'uniform_in_N scope string')
    v['scope_from_contract'] = m.group(1)
    require(v['scope_from_contract'] == UNIFORM_IN_N_SCOPE, 'scope string')
    v['selected_after'] = c.get('selected_after')
    v['nodes'] = pre['nodes']
    require(pre['nodes']['s_values'] == [] and pre['nodes']['post_hoc_node_selection'] == 'forbidden' and pre['nodes']['pilot_runs']['declared'] == [],
            'no Euclidean nodes, no post-hoc node selection, no pilot runs')
    return v


# ---------------------------------------------------------------------------
def compute(check_sha):
    c, contract_digest = load_contract()          # sha256 verified before any evaluation
    V = contract_values(c)
    tau_cap = V['tau_cap']
    target = V['target']
    check('contract_snapshot_sha256',
          contract_digest == CONTRACT_SHA256 and target == 1 and len(V['controls']) == 21 and len(V['requirement_names']) == 3,
          contract_sha256=contract_digest, contract_path=CONTRACT_REL, target_read_from_contract=s(target),
          target_comparator=V['target_comparator'], target_quantity=V['target_quantity'], tau_read_from_contract=s(tau_cap),
          signs=V['signs'], reference_read_from_contract='n/a (statement loop; observable id statement, centering none)',
          dictionary_read_from_contract=V['dictionary_text'], identities_read_from_contract=V['identities'],
          controls_read_from_contract=len(V['controls']), hash_binding=V['hash_binding'])

    # ======================= premise inventory and gate bindings =======================
    expected_inputs = ['AGENTS.md', CONTRACT_REL] + V['shared']
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    ax1_sha = inventory.get(P_AX1_GATE)
    check('premise_inventory_bound',
          sorted(inventory) == sorted(set(expected_inputs)) and len(inventory) == 29 and ax1_sha is not None
          and not any('__pycache__' in k or k.endswith('.pyc') for k in inventory),
          inventory_files=len(inventory), ax1_gate_sha256=ax1_sha, inputs_sha256=inventory,
          isolation='inputs equal AGENTS.md + the AZ1 contract + its 27 shared premises; no current skeptic, expert (beyond these snapshots), deliberation, panel or AZ2 file')

    ax1 = load_json_input(P_AX1_GATE)
    al1 = load_json_input(P_AL1_GATE)
    am2 = load_json_input(P_AM2_GATE)
    bound = sorted(k for k in inventory if k in ax1['bindings'])
    mismatched = [k for k in bound if ax1['bindings'][k] != inventory[k]]
    check('gate_bindings_match_snapshots',
          len(bound) == 22 and not mismatched and al1['bindings'][P_AL1F] == inventory[P_AL1F]
          and ax1['bindings'][P_AL1_GATE] == inventory[P_AL1_GATE] and ax1['bindings'][P_AM2_GATE] == inventory[P_AM2_GATE]
          and all(k in bound for k in (P_AX1F, P_AX1R, P_AX1S, P_AL1F, P_I1, P_AT4)),
          snapshots_bound_by_ax1_gate=len(bound), mismatched=mismatched,
          al1_report_bound_by_al1_gate=al1['bindings'][P_AL1F] == inventory[P_AL1F],
          not_bound_by_ax1_gate=sorted(k for k in inventory if k not in ax1['bindings']),
          note='the AX1 forward, reverse and skeptic reports, the AL1 report and gate, the AM2 gate and the I1, AT4, AQ1, AQ2 reports snapshotted here are the bytes the AX1 gate binds')

    acc_ax1, dec_ax1, lim_ax1, mod_ax1 = ax1['accepted'], ax1['decision'], ' '.join(ax1['limitations']), ax1['model']
    m = match(r'AL1 dictionary tau=96/g\^4, so g\^4=([\dx.^]+) at the cap; never weak coupling or continuum', acc_ax1, 'AX1 dictionary and cap')
    g4_gate = sci(m.group(1))
    m = match(r"so every finite complete-factor route-B volume has a unique gauge-invariant ground and full-space gap >=(\d+)/(\d+) normalized \(alpha/(\d+) physical\)",
              acc_ax1, 'AX1 gap')
    gap_norm_gate, gap_phys_den_gate = Q(int(m.group(1)), int(m.group(2))), int(m.group(3))
    m = match(r"J'=(\d+)\|tau\|; support 4 and termination order 8 unchanged", acc_ax1, "AX1 J'")
    J_per_tau_gate = int(m.group(1))
    m = match(r"whole stars phi_b \((\d+) omitted faces, norm (\d+)\|tau\|\) plus one single-factor group psi_b=-\(tau/3\) sum of the three selected xy faces \(support \{b\}, \|\|psi_b\|\|<=\|tau\|\)",
              acc_ax1, 'AX1 star and group norms')
    star_faces_gate, star_norm_gate, group_norm_gate = int(m.group(1)), int(m.group(2)), 1
    require(star_faces_gate * Q(1, 3) == star_norm_gate, 'star norm = 21 faces x |tau|/3')
    m = match(r"J_0'=(\d+)/10\^(\d+) \(R1\) the exact inequalities J_0'G\(R\)<(\d+)/(\d+)<1/64 and 2J_0'G'\(R\)<(\d+)/(\d+)<1 hold", acc_ax1, 'AX1 contraction')
    J0p_gate = Q(int(m.group(1)), 10 ** int(m.group(2)))
    selfmap_gate, excl_gate = Q(int(m.group(3)), int(m.group(4))), Q(int(m.group(5)), int(m.group(6)))
    m = match(r'exactly (\d+) whole stars \(anchors R-S\) and (\d+) single-factor groups meet R, charging (\d+) faces, (\d+) meeting R \((\d+) omitted \+ (\d+) selected, the 6 selected being the two single groups\) and (\d+) inside R, none twice',
              acc_ax1, 'AX1 incidence')
    inc_gate = {'stars': int(m.group(1)), 'groups': int(m.group(2)), 'charged': int(m.group(3)), 'meet': int(m.group(4)),
                'meet_omitted': int(m.group(5)), 'meet_selected': int(m.group(6)), 'inside': int(m.group(7))}
    m = match(r'omega\(W\)\^\{\(1\)\}=\+tau/(\d+) \(\+-1/(\d+)\) is unchanged', acc_ax1, 'AX1 first-order mean')
    fo_den_gate, fo_cap_den_gate = int(m.group(1)), int(m.group(2))
    ax1_admits = ('the gap alpha/16, cutoff-vector removal and AQ passage re-apply verbatim' in acc_ax1
                  and 'weak-coupling, continuum, uniqueness, rate or priority statement is admitted' in acc_ax1
                  and 'uniform_wilson_claim:true means only that the model is the uniform fixed-spacing Kogut-Susskind model as labelled' in acc_ax1)
    check('ax1_gate_fields_and_verdict',
          ax1['loop'] == 'AX1' and ax1['verdict'] == 'accepted_within_scope' and ax1_admits
          and 'both signs |tau|<=10^-8' in acc_ax1 and 'at fixed spacing and strong bare coupling' in acc_ax1
          and 'g^4>=9.6x10^9, |tau|<=10^-8' in lim_ax1 and 'never weak coupling or continuum' in lim_ax1
          and 'No Euclidean node, K_2, uniform sign certificate, weak-coupling or continuum statement is admitted' in dec_ax1
          and 'tau=96/g^4; g^4=9.6x10^9 at the cap' in mod_ax1
          and g4_gate == 96 / tau_cap and gap_norm_gate == Q(1, 2) and gap_phys_den_gate == 16 and J_per_tau_gate == 29
          and J0p_gate == J_per_tau_gate * tau_cap and fo_den_gate == 144 and fo_cap_den_gate == 144 * 10 ** 8,
          ax1_gate_sha256=ax1_sha, ax1_verdict=ax1['verdict'], g4_at_cap_from_gate=s(g4_gate),
          gap_from_gate='>=' + s(gap_norm_gate) + ' normalized (alpha/' + str(gap_phys_den_gate) + ' physical)',
          J_per_abs_tau_from_gate=J_per_tau_gate, J0_prime=s(J0p_gate), selfmap_rational=s(selfmap_gate), exclusion_rational=s(excl_gate),
          incidence_from_gate=inc_gate, first_order_mean_from_gate='+tau/' + str(fo_den_gate),
          read_from='the accepted/decision/limitations/model strings of the hash-bound AX1 gate snapshot; no constant is typed in')

    # AL1 gate and report
    al1_acc = al1['accepted']
    al1f = read_input(P_AL1F)
    m = match(r'The complete uniform SU\(2\) bulk dictionary gives r=(\d+)/g\^4, tau=(\d+)/g\^4 and local norm (\d+)/g\^4\. The actual selected bridge requires g\^4>=(\d+); '
              r'the frozen a_n=a0/n, g_n\^2=1/n path violates this sufficient condition for every n>=1\.', al1_acc, 'AL1 gate accepted')
    r_num_al1, tau_num_al1, eps_num_al1, bridge_al1 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
    m = match(r'\\alpha=\{g\^2\\over(\d+)a\},\\qquad\\lambda=\{(\d+)\\over g\^2a\},\\qquad r=\{\\lambda\\over\\alpha\}=\{(\d+)\\over g\^4\}', al1f, 'AL1.1')
    al1_alpha_den, al1_lam_num, al1_r_num = int(m.group(1)), int(m.group(2)), int(m.group(3))
    m = match(r'\\tau=\{(\d+)\\lambda\\over\\alpha\}=\{(\d+)\\over g\^4\},\\qquad\s*\\epsilon=(\d+)\|\\tau\|=\{(\d+)\\over g\^4\}', al1f, 'AL1.2')
    tau_coef, al1_tau_num, eps_mult, al1_eps_num = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
    m = match(r'r\\le\\tfrac(\d)(\d)\\quad\\hbox\{\(ends\)\},\\qquad r\\le\\tfrac(\d)(\d)\\quad\\hbox\{\(bridge\)\}', al1f, 'AL1.3')
    ends_r, bridge_r = Q(int(m.group(1)), int(m.group(2))), Q(int(m.group(3)), int(m.group(4)))
    m = match(r'\\alpha_n=\{1\\over2a_0\},\\quad\\lambda_n=\{2n\^2\\over a_0\},\\quad\s*r_n=4n\^2,\\quad\\tau_n=96n\^2,\\quad\\epsilon_n=672n\^2', al1f, 'AL1.4 path')
    al1_general = 'More generally every path with `g->0` eventually violates the bridge condition.' in al1f
    al1_sufficient = al1['limitations'][0] == 'This is failure of a specified sufficient certificate, not a no-gap or continuum-impossibility theorem.'
    check('al1_gate_and_report_parsed',
          al1['loop'] == 'AL1' and al1['verdict'] == 'accepted_within_scope' and al1_general and al1_sufficient
          and r_num_al1 == al1_r_num == 4 and tau_num_al1 == al1_tau_num == 96 and eps_num_al1 == al1_eps_num == 672 and eps_mult == 7
          and bridge_al1 == 32 and bridge_r == Q(1, 8) and ends_r == Q(1, 2) and tau_coef == 24 and al1_alpha_den == 2 and al1_lam_num == 2
          and 'Equivalently the selected bridge requires `g^4>=32`' in al1f,
          dictionary_from_al1={'alpha': 'g^2/(%da)' % al1_alpha_den, 'lambda': '%d/(g^2 a)' % al1_lam_num, 'r': '%d/g^4' % al1_r_num,
                               'tau': '%d*lambda/alpha=%d/g^4' % (tau_coef, al1_tau_num), 'epsilon': '%d|tau|=%d/g^4' % (eps_mult, al1_eps_num)},
          bridge='r<=' + s(bridge_r) + ' <=> g^4>=' + str(bridge_al1), ends='r<=' + s(ends_r),
          al1_limitation=al1['limitations'][0], al1_general_statement='every path with g->0 eventually violates the bridge condition')

    am2_acc = am2['accepted']
    am2r = read_input(P_AM2R)
    check('am2_gate_cap_and_gap',
          am2['verdict'] == 'accepted_within_scope' and 'both signs of |tau|<=1/100000000 admit a unique ground and a physical gap at least alpha/16' in am2_acc
          and 'No weak-bare-coupling continuum bridge or continuum mass-gap construction follows.' in ' '.join(am2['limitations'])
          and 'It does not establish a sharp threshold' in am2r and rat('1/100000000') == tau_cap,
          am2_cap='1/100000000', am2_gap='alpha/16', sharp_threshold=False,
          note='10^-8 is the preregistered cap at which the AM2 and AX1 certificates are admitted; the AM2 reverse report states it is not a sharp threshold')

    # ======================= dictionary identities: symbolic route =======================
    require(V['alpha_text'] == 'g^2/(2a)' and V['lambda_text'] == '2/(g^2 a)', 'contract dictionary strings')
    env = build_dictionary(V['alpha_text'], V['lambda_text'], tau_coef)
    al1_alpha = parse_rf('g^2/(%da)' % al1_alpha_den, BASE_ENV)
    al1_lam = parse_rf('%d/(g^2 a)' % al1_lam_num, BASE_ENV)
    same_as_al1 = req(env['alpha'], al1_alpha) and req(env['lambda'], al1_lam)
    ax1r = read_input(P_AX1R)
    ax1f = read_input(P_AX1F)
    ax1s = read_input(P_AX1S)
    m = match(r'The physical gap `alpha/16` equals `(g\^2/\(32a\))`\.', ax1r, 'AX1 reverse gap identity')
    ax1r_gap_rhs = m.group(1)
    template = V['template']
    m = match(r'the volume-uniform gap (alpha/16=g\^2/\(32a\)) for g\^4>=([\dx.^]+),', template, 'template identity')
    tmpl_identity, tmpl_g4 = m.group(1), sci(m.group(2))
    EXTRA = ['r=%d/g^4' % al1_r_num,                         # AL1.1
             'alpha*tau/24=lambda',                           # AX1 F01: nu = lambda = alpha*tau/24
             '(alpha/8)*(tau/3)=lambda',                      # I1.5: coefficient -(tau/3) in delta=alpha/8 units
             '%d*tau=%d/g^4' % (eps_mult, al1_eps_num),       # AL1.2 local norm epsilon
             'tau/144=2/(3g^4)',                              # AX1 first-order Wilson mean in the dictionary
             '(alpha/8)/2=g^2/(32a)',                         # normalized gap 1/2 in delta=alpha/8 units
             'a*alpha/16=g^2/32',                             # the gap in lattice units
             'tau*g^4=96',
             'alpha/16=' + ax1r_gap_rhs,                      # AX1 reverse report
             tmpl_identity,                                   # mandatory template
             V['supplied_identity']]                          # contract parameters.supplied
    ID_SOURCES = {'contract parameters.dictionary_identities': list(V['identities']),
                  'contract parameters.dictionary (tau)': ['tau=' + V['tau_text']],
                  'AX1 reverse report (gap)': ['alpha/16=' + ax1r_gap_rhs],
                  'mandatory sentence template': [tmpl_identity],
                  'contract parameters.supplied': [V['supplied_identity']],
                  'producer-added (AL1, AX1, I1 premises)': EXTRA[:8]}
    ALL_IDS = list(dict.fromkeys(x for v_ in ID_SOURCES.values() for x in v_))
    require(len(ALL_IDS) == 11, 'eleven distinct identities')
    tau_times_g4 = rmul(env['tau'], rpow(env['g'], 4))
    const96 = req(tau_times_g4, rf(pconst(96)))
    # rescaling (common scale changes) and homogeneity, by substitution var -> c*var
    tau_a_invariant = req(rsubst_scale(env['tau'], 'a'), env['tau'])
    alpha_a = req(rsubst_scale(env['alpha'], 'a'), rdiv(env['alpha'], env['c']))
    lam_a = req(rsubst_scale(env['lambda'], 'a'), rdiv(env['lambda'], env['c']))
    r_common = req(rdiv(rmul(env['c'], env['lambda']), rmul(env['c'], env['alpha'])), env['r'])
    gap_rf = rdiv(env['alpha'], rf(pconst(16)))
    gap_a = req(rsubst_scale(gap_rf, 'a'), rdiv(gap_rf, env['c']))
    check('dictionary_identities_symbolic',
          validate_dictionary(env, ALL_IDS) and same_as_al1 and const96 and tau_a_invariant and alpha_a and lam_a and r_common and gap_a,
          identities=ALL_IDS, identity_sources=ID_SOURCES, route='integer-coefficient polynomials in (g, a, c); each identity lhs=rhs checked as num_l*den_r == num_r*den_l',
          primary_definitions={'alpha': V['alpha_text'], 'lambda': V['lambda_text'], 'tau': '%d*lambda/alpha (AL1.2)' % tau_coef},
          tau_polynomial_form={'numerator': sorted([list(k), v] for k, v in env['tau'][0].items()),
                               'denominator': sorted([list(k), v] for k, v in env['tau'][1].items())},
          rescaling={'tau(c*a)=tau(a)': tau_a_invariant, 'alpha(c*a)=alpha(a)/c': alpha_a, 'lambda(c*a)=lambda(a)/c': lam_a,
                     'r(c*alpha,c*lambda)=r': r_common, 'gap(c*a)=gap(a)/c': gap_a},
          sources={'alpha/16=g^2/(32a)': 'contract, template, parameters.supplied, AX1 reverse report', 'tau=96/g^4': 'contract; AL1.2; AX1 gate',
                   'alpha*lambda*a^2=1': 'contract (cross-identity)'})

    # ======================= dictionary identities: rational-grid route =======================
    ad = int(match(r'^g\^2/\((\d+)a\)$', V['alpha_text'], 'alpha denominator').group(1))
    ln = int(match(r'^(\d+)/\(g\^2 a\)$', V['lambda_text'], 'lambda numerator').group(1))
    G2S = [Q(1, 7), Q(1), Q(3, 2), Q(97979), Q(10 ** 5), Q(10 ** 6), Q(2 ** 20, 3)]
    AS = [Q(1, 1000), Q(1, 10), Q(1), Q(7, 3), Q(1000)]
    CS = [Q(1, 3), Q(5)]

    def grid_point(g2, a, ad_=ad, ln_=ln, tc=tau_coef):
        alpha = g2 / (ad_ * a)
        lam = ln_ / (g2 * a)
        tau = tc * lam / alpha
        res = {'alpha/16=g^2/(32a)': alpha / 16 == g2 / (32 * a), 'tau=96/g^4': tau == Q(96) / g2 ** 2,
               'alpha*lambda*a^2=1': alpha * lam * a * a == 1, 'r=4/g^4': lam / alpha == Q(4) / g2 ** 2,
               'alpha*tau/24=lambda': alpha * tau / 24 == lam, '7*tau=672/g^4': 7 * tau == Q(672) / g2 ** 2,
               'tau/144=2/(3g^4)': tau / 144 == Q(2) / (3 * g2 ** 2), 'a*alpha/16=g^2/32': a * alpha / 16 == g2 / 32}
        for cc in CS:
            ca = cc * a
            alpha_c = g2 / (ad_ * ca)
            lam_c = ln_ / (g2 * ca)
            res['tau(c*a)=tau(a) at c=%s' % s(cc)] = tc * lam_c / alpha_c == tau
            res['r(c*alpha,c*lambda)=r at c=%s' % s(cc)] = (cc * lam) / (cc * alpha) == lam / alpha
        return res

    def validate_grid(points, **kw):
        for g2, a in points:
            g2, a = rat(g2), rat(a)
            require(g2 > 0 and a > 0, 'positive g^2 and a required')
            res = grid_point(g2, a, **kw)
            require(all(res.values()), 'grid identity fails at g^2=%s, a=%s: %s' % (s(g2), s(a), [k for k, v in res.items() if not v]))
        return True
    POINTS = [(g2, a) for g2 in G2S for a in AS]
    grid = [(g2, a, grid_point(g2, a)) for g2, a in POINTS]
    grid_ok = validate_grid(POINTS) and all(all(r.values()) for _, _, r in grid)
    agree = all(reval(parse_rf(ident.split('=')[0], env), g2, a) == reval(parse_rf(ident.split('=')[1], env), g2, a)
                for ident in V['identities'] for g2 in G2S for a in AS)
    check('dictionary_identities_rational_grid',
          grid_ok and agree and len(grid) == 35,
          grid_points=len(grid), g2_values=[s(x) for x in G2S], a_values=[s(x) for x in AS], rescale_factors=[s(x) for x in CS],
          identities_per_point=sorted(grid[0][2]),
          route='direct Fraction arithmetic with the constants parsed from the contract strings (alpha denominator %d, lambda numerator %d) and tau=%d*lambda/alpha; independently of the polynomial parser, and the parsed rational functions evaluated at the same points agree' % (ad, ln, tau_coef))

    check('dictionary_arithmetic_exact',
          validate_dictionary(env, ALL_IDS) and grid_ok and agree
          and rejected(lambda: validate_dictionary(build_dictionary('g^2/a', V['lambda_text'], tau_coef), V['identities']), 'alpha_without_factor_two (alpha=g^2/a)')
          and rejected(lambda: validate_dictionary(build_dictionary(V['alpha_text'], '1/(g^2 a)', tau_coef), V['identities']), 'lambda_numerator_one (lambda=1/(g^2 a))')
          and rejected(lambda: validate_dictionary(build_dictionary(V['alpha_text'], V['lambda_text'], 12), ['tau=96/g^4']), 'tau_coefficient_12_instead_of_24')
          and rejected(lambda: validate_dictionary(env, ['alpha/16=g^2/(16a)']), 'gap_written_g2_over_16a')
          and rejected(lambda: validate_dictionary(env, ['alpha*lambda*a^2=2']), 'cross_identity_value_2')
          and rejected(lambda: validate_grid(POINTS, ad_=1), 'grid_alpha_denominator_1')
          and rejected(lambda: validate_grid([(1e5, Q(1, 10))]), 'grid_float_coupling')
          and rejected(lambda: validate_dictionary(env, ['g^4=96/tau/10']), 'cap_decade_shift'),
          identities=ALL_IDS, routes=['integer-polynomial cross-multiplication (dictionary_identities_symbolic)', 'exact Fraction grid (dictionary_identities_rational_grid)'],
          cap='tau=96/g^4 gives g^4=96/tau=9600000000 at tau=10^-8 (cited: AX1 gate)')

    # ======================= admitted regime: tau cap <=> g^4 at fixed a =======================
    g4_cap = tau_num_al1 / tau_cap          # tau*g^4 = 96 (AL1 gate), proved as a polynomial identity above
    samples = [Q(1, 10 ** 9), Q(1, 10 ** 8), Q(3, 10 ** 8), Q(1, 100), Q(1)]
    equiv = all((t <= tau_cap) == (96 / t >= g4_cap) for t in samples)
    check('cap_coupling_equivalence',
          g4_cap == 9600000000 and g4_cap == g4_gate == V['supplied_g4'] == V['failed_g4'] == tmpl_g4 == V['toy_g04']
          and V['failed_tau'] == tau_cap and equiv and '| `g^4` at the cap | 9600000000 |' in ax1s,
          g4_at_cap=s(g4_cap), tau_cap=s(tau_cap),
          equivalence='for real g, tau=96/g^4>0; for T>0: tau<=T <=> g^4>=96/T (multiply by g^4/T>0); at T=10^-8: g^4>=9600000000',
          negative_tau='tau<0 has no real g; in the uniform model it is the U_E mirror of +|tau| (AX1 gate item 7), not a trajectory point',
          g4_sources=['contract parameters.supplied', 'contract parameters.failed', 'contract parameters.toy_trajectory', 'mandatory template', 'AX1 gate', 'AX1 skeptic table'])

    # ======================= physical units: the supplied gap at a declared (a, g) =======================
    g2_ex = Q(10 ** 6)                    # g_0 = 1000 (the panel rehearsal) at n=1; g^4 = 10^12 >= 9.6x10^9
    alpha_ex = g2_ex / (ad * A0_FM)       # in 1/fm (hbar = c = 1)
    gap_ex = alpha_ex / 16
    hbarc_prev = preview_value(HBARC_MEV_FM_PREVIEW)
    lo_cap, hi_cap = sqrt_bracket(g4_cap)  # g^2 at the cap: sqrt(9.6x10^9) = 40000*sqrt(6)
    gap_cap_lo = lo_cap / (32 * A0_FM)
    check('gap_physical_units_example',
          g2_ex ** 2 >= g4_cap and gap_ex == g2_ex / (32 * A0_FM) and gap_ex == 312500 and alpha_ex == 5000000
          and lo_cap ** 2 <= g4_cap <= hi_cap ** 2 and gap_cap_lo > 30618 and reval(gap_rf, g2_ex, A0_FM) == gap_ex,
          declared_example={'a': s(A0_FM) + ' fm', 'g^2': s(g2_ex), 'g^4': s(g2_ex ** 2), 'tau': s(96 / g2_ex ** 2), 'in_admitted_regime': g2_ex ** 2 >= g4_cap},
          alpha=s(alpha_ex) + ' fm^-1', gap_lower_bound=s(gap_ex) + ' fm^-1 (hbar=c=1)', gap_over_E_star=s(gap_ex), E_star=E_STAR_LABEL,
          gap_MeV_preview=dec(gap_ex * hbarc_prev, 8) + ' MeV (preview with hbar*c=' + HBARC_MEV_FM_PREVIEW + ' MeV fm, truncated CODATA 2018)',
          cap_example={'g^4': s(g4_cap), 'g^2_bracket': [s(lo_cap), s(hi_cap)], 'a': s(A0_FM) + ' fm',
                       'gap_over_E_star_lower': s(gap_cap_lo), 'gap_over_E_star_lower_preview': dec(gap_cap_lo)},
          note='the estimate is cited from the AX1 gate (gap >=1/2 normalized, alpha/16 physical), not re-derived; the numbers here only evaluate the dictionary')

    # lattice-units floor inside the admitted regime: a*Delta >= g^2/32 >= sqrt(9.6x10^9)/32
    floor_lo = lo_cap / 32
    a_seq = [A0_FM / n for n in (1, 10, 100, 1000)]
    div_seq = [floor_lo / an for an in a_seq]
    check('admitted_regime_lattice_units_floor',
          floor_lo > 3061 and floor_lo < 3062 and all(div_seq[k + 1] == 10 * div_seq[k] for k in range(3))
          and identity_holds('a*alpha/16=g^2/32', env),
          lattice_units_floor_lower=s(floor_lo), lattice_units_floor_preview=dec(floor_lo),
          statement='for every (a,g) in the admitted regime, a*Delta >= g^2/32 >= sqrt(9.6x10^9)/32 > 3061 (lattice units); a trajectory with a_n->0 that stayed in the admitted regime would have certified Delta_n >= 3061/a_n, divergent in units of the fixed E_star; a finite physical gap as a_n->0 requires leaving the admitted regime',
          divergence_example={'a_n (fm)': [s(x) for x in a_seq], 'Delta_n lower (fm^-1)': [dec(x, 8) for x in div_seq]})

    # ======================= the toy trajectories and crossovers =======================
    mod4 = read_input(P_MOD4)
    m = match(r'Taking the illustrative integer `g_0=(\d+)` \(so `g_n\^4=10\^(\d+)/n\^4`', mod4, 'panel rehearsal g_0')
    g0_panel = int(m.group(1))
    require(g0_panel ** 4 == 10 ** int(m.group(2)), 'rehearsal g_0^4')
    m1 = match(r'first fails at \*\*`n\*=(\d+)`\*\* \(`g_4\^4=10\^12/256=(\d+)` exactly', mod4, 'rehearsal cap crossover')
    m2 = match(r'holds through `n=(\d+)` \(`g_420\^4=10\^12/(\d+)~[\d.]+>=32`\) and first fails at \*\*`n\*=(\d+)`\*\* \(`g_421\^4=10\^12/(\d+)~', mod4, 'rehearsal bridge crossover')
    m3 = match(r'`g_3\^4=10\^12/81=(\d+)\+(\d+)/81', mod4, 'rehearsal g_3^4')
    panel_claims = {'cap': int(m1.group(1)), 'g4_4': int(m1.group(2)), 'bridge_last': int(m2.group(1)), 'n420_4': int(m2.group(2)),
                    'bridge': int(m2.group(3)), 'n421_4': int(m2.group(4)), 'g3_4_int': int(m3.group(1)), 'g3_4_rem': int(m3.group(2))}
    g3_exact = Q(10 ** 12, 81)
    g3_int, g3_rem = divmod(10 ** 12, 81)
    panel_g3_note = {'id': 'P1', 'source': P_MOD4 + ' section 3 (panel rehearsal)',
                     'claimed': 'g_3^4=10^12/81=%d+%d/81' % (panel_claims['g3_4_int'], panel_claims['g3_4_rem']),
                     'exact': 'g_3^4=10^12/81=%d+%d/81' % (g3_int, g3_rem),
                     'claimed_correct': panel_claims['g3_4_int'] == g3_int and panel_claims['g3_4_rem'] == g3_rem,
                     'effect': 'none on any crossover index: g_3^4 is above 9.6x10^9 either way; only the mixed-number remainder is wrong'}
    TOYS = {'cap_declared': {'g0_4': V['toy_g04'], 'g0_2': None, 'label': 'g_0^4=9.6x10^9 (the cap), declared primary (contract parameters.toy_trajectory)'},
            'panel_rehearsal': {'g0_4': Q(g0_panel) ** 4, 'g0_2': Q(g0_panel) ** 2, 'label': 'g_0=%d, the panel rehearsal (modern update-4 section 3), labelled second example' % g0_panel}}
    THRESH = {'cap': g4_cap, 'bridge': V['bridge_g4']}
    cross = {}
    for name, toy in TOYS.items():
        row = {}
        for tname, T in THRESH.items():
            n_root = crossover_root(toy['g0_4'], T)
            n_scan = crossover_scan(toy['g0_4'], T, 1000)
            require(n_root == n_scan, 'the two crossover routes disagree')
            validate_crossover(toy['g0_4'], T, n_root)
            last = n_root - 1
            row[tname] = {'threshold_g4': s(T), 'n_star': n_root, 'g_n_star^4': s(toy['g0_4'] / Q(n_root) ** 4),
                          'g_n_star^4_preview': dec(toy['g0_4'] / Q(n_root) ** 4),
                          'last_n_at_or_above': last, 'g_last^4': (s(toy['g0_4'] / Q(last) ** 4) if last >= 1 else None),
                          'g_last^4_preview': (dec(toy['g0_4'] / Q(last) ** 4) if last >= 1 else None),
                          'tau_n_star': s(96 * Q(n_root) ** 4 / toy['g0_4']), 'tau_n_star_preview': dec(96 * Q(n_root) ** 4 / toy['g0_4'])}
        cross[name] = row
    cd, pr = cross['cap_declared'], cross['panel_rehearsal']
    toy_ok = (cd['cap']['n_star'] == 2 and cd['bridge']['n_star'] == 132 and pr['cap']['n_star'] == 4 and pr['bridge']['n_star'] == 421
              and V['toy_g04'] / Q(2) ** 4 == V['toy_g04'] / 16 and V['toy_g04'] / 1 == g4_cap)
    panel_ok = (panel_claims['cap'] == pr['cap']['n_star'] and panel_claims['bridge'] == pr['bridge']['n_star']
                and panel_claims['g4_4'] == Q(10 ** 12, 256) and panel_claims['n420_4'] == 420 ** 4 and panel_claims['n421_4'] == 421 ** 4
                and panel_claims['g3_4_int'] == g3_int and panel_claims['bridge_last'] == 420 and g3_exact >= g4_cap)

    def toy_law(g0_4, n, p=4):
        return rat(g0_4) / Q(n) ** p
    law_ok = all(toy_law(TOYS['panel_rehearsal']['g0_4'], n) == (Q(g0_panel) / n) ** 4 for n in range(1, 30))
    check('toy_trajectory_crossover_exact',
          toy_ok and panel_ok and law_ok
          and rejected(lambda: validate_crossover(V['toy_g04'], g4_cap, 1), 'cap_boundary_n1_counted_as_crossover (g_1^4 equals the cap; |tau|<=10^-8 is inclusive)')
          and rejected(lambda: validate_crossover(V['toy_g04'], V['bridge_g4'], 131), 'bridge_index_off_by_one_low_131')
          and rejected(lambda: validate_crossover(V['toy_g04'], V['bridge_g4'], 133), 'bridge_index_not_first_133')
          and rejected(lambda: validate_crossover(TOYS['panel_rehearsal']['g0_4'], g4_cap, 3), 'rehearsal_cap_index_3')
          and rejected(lambda: validate_crossover(TOYS['panel_rehearsal']['g0_4'], V['bridge_g4'], 420), 'rehearsal_bridge_index_420')
          and rejected(lambda: validate_crossover(TOYS['panel_rehearsal']['g0_4'], Q(32, 3), 421), 'R18_B2_threshold_32_over_3_substituted')
          and rejected(lambda: validate_crossover(V['toy_g04'] / 10, g4_cap, 2), 'cap_decade_wrong_9.6x10^8'),
          declared_trajectory='g_n=g_0/n, a_n=a_0/n, n>=1, E_star fixed; g_n^4=g_0^4/n^4 exactly',
          toys={k: t['label'] for k, t in TOYS.items()}, crossovers=cross,
          routes=['exact integer fourth root: n*=iroot4(floor(g_0^4/T))+1 with m^4<=F<(m+1)^4 checked', 'exact Fraction scan n=1,2,... (limit 1000)'],
          panel_rehearsal_reproduced={'n*_cap': panel_claims['cap'], 'n*_bridge': panel_claims['bridge'], 'g_3^4_exact': s(g3_exact),
                                      '420^4': panel_claims['n420_4'], '421^4': panel_claims['n421_4'], 'indices_agree': panel_ok},
          premise_arithmetic_note=panel_g3_note,
          boundary_rule='crossover = first n with g_n^4 strictly below the threshold; g_n^4 equal to the cap (|tau|=10^-8) is inside the admitted regime')

    # gap along the toy where the estimate is supplied; beyond the crossover nothing is certified (not zero)
    along = []
    for n in range(1, pr['cap']['n_star'] + 2):
        in_reg = TOYS['panel_rehearsal']['g0_4'] / Q(n) ** 4 >= g4_cap
        bound_n = (TOYS['panel_rehearsal']['g0_2'] / Q(n) ** 2) / (32 * (A0_FM / n)) if in_reg else None
        along.append({'n': n, 'in_admitted_regime': in_reg, 'gap_over_E_star_lower': (s(bound_n) if in_reg else None),
                      'certificate': ('AX1 volume-uniform gap at fixed a_n' if in_reg else 'none supplied (not a statement that the gap vanishes)')})
    check('toy_gap_along_path',
          [x['in_admitted_regime'] for x in along] == [True, True, True, False, False]
          and along[0]['gap_over_E_star_lower'] == '312500' and along[2]['gap_over_E_star_lower'] == '312500/3'
          and all(x['gap_over_E_star_lower'] is None for x in along[3:]),
          rehearsal_toy='g_0=1000, a_n=(1/10 fm)/n, E_star=hbar*c/(1 fm)', along=along,
          note='Delta_n/E_star >= g_0^2/(32 a_0 n E_star) = 312500/n for n<4; from n=4 on the family supplies no certificate; failure of a sufficient certificate is not absence of a gap (AL1 limitation)')

    # every g->0 path leaves both regimes at a finite index; the AL1 frozen path fails the bridge at every n
    al1_path = []
    ok_path = True
    for n in range(1, 1001):
        g2n = Q(1, n)
        a_n = Q(1, n)            # a_0 = 1 (any a_0 > 0 gives the same tau)
        alpha_n = g2n / (ad * a_n)
        tau_n = tau_coef * (ln / (g2n * a_n)) / alpha_n
        ok_path = ok_path and tau_n == 96 * n * n and g2n ** 2 < V['bridge_g4'] and alpha_n == Q(1, 2) and g2n ** 2 < g4_cap
        if n <= 3:
            al1_path.append({'n': n, 'g_n^4': s(g2n ** 2), 'tau_n': s(tau_n), 'alpha_n*a_0': s(alpha_n)})
    slow = {tn: crossover_root(Q(g0_panel) ** 4, T, p=1) for tn, T in THRESH.items()}
    slow_ok = all(Q(g0_panel) ** 4 / slow[tn] < T and Q(g0_panel) ** 4 / (slow[tn] - 1) >= T for tn, T in THRESH.items())
    eps_list = [Q(1), Q(1, 10 ** 6), Q(1, 10 ** 30)]
    lemma = all(crossover_root(V['toy_g04'], e) >= 1 for e in eps_list)
    check('any_g_to_zero_path_leaves_regime',
          ok_path and slow == {'cap': 105, 'bridge': 31250000001} and slow_ok and lemma,
          lemma='if g_n->0 then for every threshold T>0 there is n0 with g_n^4<T for all n>=n0 (definition of the limit); so every such path leaves g^4>=9.6x10^9 and g^4>=32 at finite indices',
          al1_frozen_path={'law': 'a_n=a_0/n, g_n^2=1/n', 'tau_n': '96n^2', 'bridge_fails_for_every_n_checked': ok_path, 'first_rows': al1_path,
                           'all_n': 'g_n^4=1/n^2<=1<32 for every n>=1'},
          slower_toy={'law': 'g_n^4=g_0^4/n (g_0=1000)', 'n*_cap': slow['cap'], 'n*_bridge': slow['bridge'], 'route': 'exact integer (p=1) root with bracket'},
          i1_omitted_conditions='g^4>672/c1 and g^4>1344c2 with c1(S), c2(S) unevaluated (AL1.3): for any fixed positive values the same lemma gives a finite crossover')

    # fixed-cap sensitivity: the contraction-only margins recorded in the AX1 forward report (NOT admitted)
    m = match(r'The self-map inequality would allow `\|tau\|<=(\d+)/(\d+)` \(about `(\d+)` times the cap\), and the exclusion inequality would allow `\|tau\|<1/(\d+)`', ax1f, 'AX1 forward margins')
    tau_selfmap, tau_excl = Q(int(m.group(1)), int(m.group(2))), Q(1, int(m.group(4)))
    am2f = read_input('research/round29/forward/am2/report.md')
    m = match(r"G\(R\)<(\d+)/(\d+),\\quad G'\(R\)<(\d+),\\quad", am2f, 'AM2.9 G(R), G\'(R) bounds')
    G_R, Gp_R = Q(int(m.group(1)), int(m.group(2))), Q(int(m.group(3)))
    selfmap_recomputed = Q(1, 64) / (J_per_tau_gate * G_R)
    excl_recomputed = Q(1) / (2 * J_per_tau_gate * Gp_R)
    sens = {}
    for tn, t in (('selfmap_only', tau_selfmap), ('exclusion_only', tau_excl)):
        T = 96 / t
        sens[tn] = {'tau_bound': s(t), 'g4_threshold': s(T), 'g4_threshold_preview': dec(T), 'admitted': False,
                    'n*_cap_declared_toy': crossover_root(V['toy_g04'], T), 'n*_panel_toy': crossover_root(Q(g0_panel) ** 4, T)}
    check('fixed_cap_sensitivity_not_admitted',
          selfmap_recomputed == tau_selfmap and excl_recomputed == tau_excl and J_per_tau_gate * tau_cap * G_R == selfmap_gate
          and 2 * J_per_tau_gate * tau_cap * Gp_R == excl_gate and all(x['admitted'] is False for x in sens.values())
          and sens['selfmap_only']['n*_cap_declared_toy'] == 8 and sens['exclusion_only']['n*_panel_toy'] == 27,
          sensitivity=sens, G_R_bound=s(G_R), Gp_R_bound=s(Gp_R),
          note='NOT admitted regimes: the AX1 chain (reset, variance floor, AQ passage) was evaluated only at the cap; these rows show that the failure point does not depend on where a fixed cap sits')

    # ======================= inherited geometry controls =======================
    R = frozenset({ORIGIN, EZ})
    anchors_full = frozenset(vsub(r_, s_) for r_ in R for s_ in S_STAR)
    inc_full = incidence(R, anchors_full, [b for b in sorted(R)])
    stars_per_site = len({vsub((5, -3, 2), s_) for s_ in S_STAR})
    J_full = stars_per_site * star_norm_gate + group_norm_gate

    def validate_incidence(inc, j_per_tau):
        require(inc == inc_gate, 'incidence differs from the AX1 gate itemization')
        require(j_per_tau == J_per_tau_gate, "per-site sum differs from the AX1 gate J'=29|tau|")
        require(j_per_tau * tau_cap * G_R == selfmap_gate, 'self-map rational differs from the AX1 gate')
        return True
    inc_out = incidence(R, frozenset(R), [b for b in sorted(R)])
    check('missing_incoming_stars',
          validate_incidence(inc_full, J_full) and len(anchors_full) == 7 and stars_per_site == 4
          and rejected(lambda: validate_incidence(inc_out, 1 * star_norm_gate + group_norm_gate), 'outgoing_stars_only (2 anchors, per-site sum 8|tau|)')
          and rejected(lambda: validate_incidence(inc_full, stars_per_site * star_norm_gate), 'single_factor_groups_dropped (per-site sum 28|tau|, the patterned-model value)')
          and rejected(lambda: validate_incidence(incidence(R, frozenset([ORIGIN]), [ORIGIN]), 8), 'single_star_at_0_only'),
          anchors=sorted(list(a_) for a_ in anchors_full), incidence=inc_full, stars_per_site=stars_per_site, J_per_abs_tau=J_full,
          outgoing_only=inc_out, note="the supplied gap is AX1's, computed with complete incoming-star incidence J'=29|tau|; dropping incoming stars changes the self-map rational")

    Wface = [(ORIGIN, 0), ((1, 0, 0), 2), (EZ, 0), (ORIGIN, 2)]
    w_owners = frozenset(owner(l_[0]) for l_ in Wface)
    cover_links = [l_ for b in sorted(R) for l_ in factor_links(b)]
    endpoints = {l_[0] for l_ in cover_links} | {vadd(l_[0], E_UNIT[l_[1]]) for l_ in cover_links}
    at4 = read_input(P_AT4)
    at4_cover = 'This cover contains 48 links and 36 distinct original endpoints.' in at4

    def validate_cover(region, links):
        require(w_owners <= region, 'the original xz Wilson loop is not covered by complete factors of the region')
        require(sorted(links) == sorted(l_ for b in sorted(region) for l_ in factor_links(b)), 'the cover must consist of complete 24-link factors')
        require(len(links) == 48, 'the complete cover has 48 links')
        return True
    check('full_original_wilson_cover',
          validate_cover(R, cover_links) and len(endpoints) == 36 and w_owners == R and at4_cover
          and rejected(lambda: validate_cover(frozenset([ORIGIN]), factor_links(ORIGIN)), 'single_factor_cover_0')
          and rejected(lambda: validate_cover(R, Wface), 'four_drawn_links_as_cover'),
          cover='R={0,e_z}', links=len(cover_links), endpoints=len(endpoints), wilson_owners=sorted(list(x) for x in w_owners),
          note='the model cited by AZ1 (AX1) keeps the original xz Wilson loop with its complete cover; AZ1 adds no observable')

    # ======================= clock, units, centering, first order =======================
    def validate_clock(clk):
        require(clk == V['clock_common'], 'common physical clock s=alpha*t_E/hbar, theta=alpha*t/hbar required')
        return True

    def validate_gap_units(normalized_gap, unit_over_alpha):
        require(normalized_gap == gap_norm_gate, 'normalized gap differs from the AX1 gate')
        require(unit_over_alpha == Q(1, 8), 'the normalized unit is delta=alpha/8')
        require(normalized_gap * unit_over_alpha == Q(1, gap_phys_den_gate), 'physical gap must be alpha/16')
        return True
    alpha_fx, hbar_fx, tE_fx = Q(5), Q(7), Q(7, 5)
    s_fx = alpha_fx * tE_fx / hbar_fx
    check('wrong_delta_alpha_hbar_clock',
          validate_clock(V['clock_common']) and validate_gap_units(Q(1, 2), Q(1, 8)) and s_fx == 1
          and identity_holds('(alpha/8)/2=g^2/(32a)', env) and V['forbidden_u_div'] == 8 and V['forbidden_exponent'] == 24
          and '(alpha/8)(H_tilde-E_tilde)' in al1f
          and rejected(lambda: validate_gap_units(Q(1, 2), Q(1)), 'normalized_gap_read_in_alpha_units (alpha/2)')
          and rejected(lambda: validate_gap_units(Q(1), Q(1, 8)), 'gap_one_route (alpha/8)')
          and rejected(lambda: validate_gap_units(Q(6), Q(1, 8)), 'haar_onsite_gap_six_as_the_interacting_gap')
          and rejected(lambda: validate_clock('normalized clock u=s/%d' % V['forbidden_u_div']), 'normalized_clock_u')
          and rejected(lambda: validate_dictionary(env, ['(alpha/8)/2=g^2/(16a)']), 'delta_alpha_mixed_gap_g2_over_16a'),
          clock=V['clock_common'], nonunit_fixture={'alpha': '5', 'hbar': '7', 't_E': '7/5', 's': s(s_fx)},
          units='hbar=c=1 in the dictionary; restoring units, alpha=hbar*c*g^2/(2a) and the gap bound is hbar*c*g^2/(32a); E_star fixed',
          note='the statement is static; the clock is fixed only so that the gap alpha/16 is an energy in the same units as E_star')

    mm, dd = Q(1, 4), Q(1, 100)
    vec_res, scal_res, unc_res = dd * dd, -2 * mm * dd - dd * dd, mm * mm
    at4_ok = ('For the exact control `m=1/4,d=1/100`, they are respectively `+1/10000` and `-51/10000`.' in at4
              and 'retains the vacuum residue `m\u00b2=1/16`' in at4)
    E0_fx, E1_fx, raw_shift = Q(3, 2), Q(2), Q(7)

    def validate_centering(kind):
        require(kind == V['centering'], 'AZ1 observable is the statement itself (contract centering: none)')
        return True

    def validate_gap_reference(e_low, e_high, reference):
        require(reference == 'actual ground energy', 'the gap is measured from the actual ground energy of the centered operator')
        return e_high - e_low
    gap_fx = validate_gap_reference(E0_fx + raw_shift, E1_fx + raw_shift, 'actual ground energy')
    check('vector_versus_scalar_centering',
          validate_centering('none') and at4_ok and vec_res == Q(1, 10000) and scal_res == Q(-51, 10000) and unc_res == Q(1, 16)
          and gap_fx == Q(1, 2)
          and rejected(lambda: validate_centering('vector'), 'vector_centering_imposed_on_a_statement')
          and rejected(lambda: validate_centering('scalar'), 'scalar_subtraction_imposed')
          and rejected(lambda: validate_gap_reference(0, E1_fx + raw_shift, 'zero reference energy'), 'uncentered_raw_scalar_as_gap_reference'),
          residues={'vector': s(vec_res), 'scalar': s(scal_res), 'uncentered': s(unc_res)},
          gap_fixture={'E0_raw': s(E0_fx + raw_shift), 'E1_raw': s(E1_fx + raw_shift), 'gap': s(gap_fx), 'label': 'two-level exact fixture; not AQ data'},
          note='AL1: the raw magnetic scalar lambda*N_p cancels under actual ground centering; the cited gap is a difference of the two lowest eigenvalues')

    def validate_first_order(coef_over_tau):
        require(coef_over_tau != 0, 'the first-order Wilson mean +tau/144 must be charged (AX1 gate item 7)')
        require(coef_over_tau == Q(1, fo_den_gate), 'first-order coefficient differs from the AX1 gate +tau/144')
        return True
    fo_cap = tau_cap / fo_den_gate
    fo_along = [s(Q(96) * Q(n) ** 4 / V['toy_g04'] / fo_den_gate) for n in (1, 2, 3)]
    check('first_order_mean_charged',
          validate_first_order(Q(1, 144)) and fo_cap == Q(1, fo_cap_den_gate) and identity_holds('tau/144=2/(3g^4)', env)
          and fo_cap == Q(2) / (3 * g4_cap)
          and rejected(lambda: validate_first_order(Q(0)), 'first_order_mean_set_to_zero')
          and rejected(lambda: validate_first_order(Q(-1, 72)), 'sign_slip_minus_tau_over_72')
          and rejected(lambda: validate_first_order(Q(1, 72)), 'missing_factor_two_tau_over_72'),
          first_order_mean='+tau/144 = 2/(3g^4) (AX1 gate; dictionary)', at_cap=s(fo_cap),
          along_cap_declared_toy={'n=1,2,3': fo_along},
          note='the first-order coefficient grows like n^4 along g_n=g_0/n: the expansion parameter itself leaves the admitted cap at n=2')

    # scaling exponents measured by exact substitution
    EXPECTED_EXP = {'tau': {'g': -4, 'a': 0}, 'alpha': {'g': 2, 'a': -1}, 'lambda': {'g': -2, 'a': -1},
                    'gap alpha/16': {'g': 2, 'a': -1}, 'lattice gap a*alpha/16': {'g': 2, 'a': 0}}
    OBJ = {'tau': env['tau'], 'alpha': env['alpha'], 'lambda': env['lambda'], 'gap alpha/16': gap_rf,
           'lattice gap a*alpha/16': rmul(env['a'], gap_rf)}
    measured = {k: {'g': exponent_of(x, 'g'), 'a': exponent_of(x, 'a')} for k, x in OBJ.items()}

    def validate_exponents(claimed):
        for k1, e in claimed.items():
            require(measured[k1] == e, 'scaling exponent label differs from exact substitution: ' + k1)
        return True
    check('tau_scaling_exponent',
          validate_exponents(EXPECTED_EXP) and measured == EXPECTED_EXP
          and rejected(lambda: validate_exponents({'tau': {'g': -2, 'a': 0}}), 'tau_read_as_96_over_g2')
          and rejected(lambda: validate_exponents({'tau': {'g': -4, 'a': 1}}), 'tau_read_as_a_dependent (common rescaling moves tau)')
          and rejected(lambda: validate_exponents({'lattice gap a*alpha/16': {'g': 2, 'a': -1}}), 'lattice_gap_read_as_physical')
          and rejected(lambda: validate_dictionary(env, ['tau=96/g^2']), 'dictionary_tau_96_over_g2'),
          exponents=measured, crossover_scaling='n* = iroot4(floor(g_0^4/T))+1, i.e. n* grows like (g_0^4/T)^(1/4)')

    # ======================= model, trajectory, estimate =======================
    MODEL = {'model_id': V['model_id'], 'label': LABEL, 'tau_cap': s(tau_cap), 'J_per_abs_tau': J_per_tau_gate,
             'reference': 'haar (route B)', 'selected_coefficient_alpha_units': 'tau/24', 'admitted_g4_min': s(g4_cap),
             'finite_graph': False, 'negative_tau_is_real_g_point': False, 'fixed_spacing': True}

    def validate_model(mdl):
        require(mdl['model_id'] == V['model_id'], 'model id')
        require(mdl['label'] == LABEL, 'model label')
        require(rat(mdl['tau_cap']) == tau_cap, 'coupling cap differs from the preregistered cap')
        require(mdl['J_per_abs_tau'] == J_per_tau_gate, 'per-site sum of a different model (patterned J=28 or other)')
        require(mdl['reference'] == 'haar (route B)', 'selected-strip reference is route A / another model')
        require(mdl['selected_coefficient_alpha_units'] == 'tau/24', 'selected faces must carry the uniform coefficient tau/24')
        require(rat(mdl['admitted_g4_min']) == g4_cap, 'a point below g^4=9.6x10^9 relabelled as admitted')
        require(mdl['finite_graph'] is False, 'a finite graph is another model')
        require(mdl['negative_tau_is_real_g_point'] is False, 'tau<0 has no real g (U_E mirror)')
        require(mdl['fixed_spacing'] is True, 'the admitted model is at fixed spacing')
        return True

    def mmut(**kw):
        m2 = dict(MODEL)
        m2.update(kw)
        return lambda: validate_model(m2)
    check('changed_model_relabelled',
          validate_model(MODEL) and V['triple'] == [0, 0, 0]
          and rejected(mmut(J_per_abs_tau=28, model_id='AQ_patterned_zero_selected', selected_coefficient_alpha_units='0'), 'patterned_zero_selected_model')
          and rejected(mmut(admitted_g4_min=s(V['toy_g04'] / 16)), 'toy_point_n2_relabelled_admitted (tau=16x10^-8)')
          and rejected(mmut(admitted_g4_min='1'), 'al1_frozen_path_point_relabelled_admitted')
          and rejected(mmut(negative_tau_is_real_g_point=True), 'negative_tau_as_real_g_coupling')
          and rejected(mmut(finite_graph=True), 'finite_graph_relabelled')
          and rejected(mmut(reference='selected_strip'), 'selected_strip_reference')
          and rejected(mmut(fixed_spacing=False), 'trajectory_points_relabelled_one_model'),
          model=MODEL, triple_note='preregistration selected_triple ["0","0","0"] read as the route-B Haar reference; the selected faces carry tau/24 in psi_b (AX1)')

    TRAJ = {'name': 'H_AF: (a_n, g_n), n>=1, with a_n -> 0 and g_n -> 0',
            'status': 'hypothesis of asymptotic-freedom form, not derived here',
            'form': 'g(a)^2 ~ 1/(2 b_0 log(1/(a Lambda))) as a -> 0 with b_0 > 0 (qualitative; no numerical b_0 is used or source-audited)',
            'derived': False, 'claimed_physical_trajectory': False,
            'toy': {'g_n': 'g_0/n', 'a_n': 'a_0/n', 'E_star': 'fixed'}, 'E_star_fixed': True, 'plateau_fit': False,
            'post_hoc_node_selection': 'forbidden'}

    def validate_trajectory(tr):
        require('hypothesis' in tr['status'] and 'not derived' in tr['status'] and tr['derived'] is False, 'the trajectory is a hypothesis, not derived')
        require(tr['claimed_physical_trajectory'] is False, 'no trajectory is claimed to be the physical renormalization trajectory')
        require(set(tr['toy']) == {'g_n', 'a_n', 'E_star'} and tr['toy']['E_star'] == 'fixed', 'toy trajectory must name g_n, a_n and a fixed E_star')
        law = {'g_0/n': 1, 'g_0': 0}.get(tr['toy']['g_n'])
        require(law == 1, 'toy g_n must tend to zero (g_0/n)')
        require(tr['toy']['a_n'] == 'a_0/n', 'toy a_n must tend to zero (declared a_0/n)')
        return True

    def tmut(**kw):
        t2 = json.loads(json.dumps(TRAJ))
        t2.update(kw)
        return lambda: validate_trajectory(t2)
    check('trajectory_named',
          validate_trajectory(TRAJ) and all(Q(1, n + 1) < Q(1, n) for n in range(1, 50))
          and rejected(tmut(status='derived from the two-loop beta function', derived=True), 'trajectory_claimed_derived')
          and rejected(tmut(toy={'g_n': 'g_0/n', 'E_star': 'fixed'}), 'a_n_unnamed')
          and rejected(tmut(toy={'g_n': 'g_0', 'a_n': 'a_0/n', 'E_star': 'fixed'}), 'g_constant_not_to_zero')
          and rejected(tmut(claimed_physical_trajectory=True), 'the_renormalization_trajectory_claimed'),
          trajectory=TRAJ, note='the crossovers do not depend on a_n because tau=96/g^4 is independent of a (rescaling invariance)')

    ESTIMATE = {'id': 'E1', 'name': 'volume-uniform gap at fixed a',
                'statement': 'every finite complete-factor route-B volume (every N) of the uniform Kogut-Susskind SU(2) model at fixed spacing a has a unique gauge-invariant ground and full-space gap >= 1/2 normalized = alpha/16 = g^2/(32a); the gap passes to the AQ subsequential states',
                'regime': '|tau|<=10^-8, i.e. g^4>=9.6x10^9, at fixed a', 'regime_g4': s(g4_cap),
                'citation': P_AX1_GATE, 'citation_sha256': ax1_sha, 'cited_not_rederived': True,
                'uniform_in': 'N (volume) at fixed a', 'uniform_along_a_n': False,
                'failure_point': 'every (a_n,g_n) with g_n->0 leaves g^4>=9.6x10^9 at a finite index (declared toy n*=2); the AL1 bridge g^4>=32 fails at a later finite index (n*=132)'}
    OTHER_FIXED_A = ["D'_ii state bound (AX1 gate item 6)", 'reset budget 102|tau| (AX1 gate item 3)', "|omega(W)|<=D' (AX1 gate item 6)"]

    def validate_estimates(lst):
        require(len(lst) == 1, 'exactly one necessary estimate must be identified')
        e = lst[0]
        require(e['citation'] == P_AX1_GATE and e['citation_sha256'] == ax1_sha, 'the estimate must be cited from the hash-bound AX1 gate')
        require(e['cited_not_rederived'] is True, 'the estimate is cited, not re-derived')
        require(e['uniform_along_a_n'] is False and e['uniform_in'] == 'N (volume) at fixed a', 'the estimate is volume-uniform at fixed a only')
        require('alpha/16' in e['statement'] and rat(e['regime_g4']) == g4_cap, 'estimate value or regime')
        return True
    check('one_uniform_estimate_identified',
          validate_estimates([ESTIMATE]) and gap_norm_gate == Q(1, 2)
          and rejected(lambda: validate_estimates([]), 'no_estimate_identified')
          and rejected(lambda: validate_estimates([ESTIMATE, dict(ESTIMATE, id='E2', name="D'_ii along a_n")]), 'second_estimate_added')
          and rejected(lambda: validate_estimates([dict(ESTIMATE, citation='research/round29/advisor/am2-gate.json')]), 'patterned_model_gate_cited')
          and rejected(lambda: validate_estimates([dict(ESTIMATE, uniform_along_a_n=True)]), 'estimate_read_along_a_n')
          and rejected(lambda: validate_estimates([dict(ESTIMATE, cited_not_rederived=False)]), 'estimate_rederived_instead_of_cited'),
          estimate=ESTIMATE, other_fixed_a_constants_not_selected=OTHER_FIXED_A,
          reading="'exactly one' = exactly one necessary estimate (item 2); the AX1 gate also admits other volume-uniform constants at fixed a, none of which is uniform along a_n->0")

    # E_star fixed, no plateau fit
    def validate_scales(e_star, e_star_varies, plateau_fit, node_selection):
        require(rat(e_star) > 0, 'E_star must be a fixed positive physical reference, never zero')
        require(e_star_varies is False, 'E_star must not vary along the trajectory')
        require(plateau_fit is False, 'no plateau fit (contract model)')
        require(node_selection == V['nodes']['post_hoc_node_selection'] == 'forbidden', 'post-hoc node selection forbidden')
        return True
    check('e_star_fixed_no_plateau',
          validate_scales(1, False, False, 'forbidden') and 'no plateau fit' in V['model'] and 'Positive `E_star` is a physical reference, never a regulator chosen as zero.' in al1f
          and rejected(lambda: validate_scales(0, False, False, 'forbidden'), 'E_star_zero')
          and rejected(lambda: validate_scales(1, True, False, 'forbidden'), 'E_star_n_equal_1_over_a_n')
          and rejected(lambda: validate_scales(1, False, True, 'forbidden'), 'plateau_fit_of_gap_over_E_star')
          and rejected(lambda: validate_scales(1, False, False, 'allowed'), 'post_hoc_node_selection'),
          E_star=E_STAR_LABEL, plateau_fit=False, nodes=V['nodes'])

    # label
    def validate_label(lb):
        low = lb.lower()
        require('fixed spacing' in low and 'strong bare coupling' in low, 'label must say fixed spacing and strong bare coupling')
        require('weak coupling' not in low and 'continuum' not in low, 'weak-coupling or continuum label')
        return True
    check('uniform_label_strong_coupling',
          validate_label(LABEL) and 'uniform Kogut-Susskind SU(2) model at fixed spacing and strong bare coupling' in lim_ax1
          and rejected(lambda: validate_label('uniform Kogut\u2013Susskind SU(2), weak coupling'), 'weak_coupling_label')
          and rejected(lambda: validate_label('uniform Kogut\u2013Susskind SU(2) at fixed spacing, strong bare coupling, continuum trajectory'), 'continuum_label')
          and rejected(lambda: validate_label('uniform Kogut\u2013Susskind SU(2), strong bare coupling'), 'fixed_spacing_missing')
          and rejected(lambda: validate_label('uniform Kogut\u2013Susskind SU(2) at fixed spacing'), 'strong_bare_coupling_missing'),
          label=LABEL)

    # ======================= report scans =======================
    report_text = (BASE / 'report.md').read_text(encoding='utf-8')
    N_TOK = [r'volume-uniform', r'uniform in n\b', r'uniformly in n\b', r'uniform-in-n\b']
    A_TOK = [r'uniform in a(?:_n)?\b', r'uniformly in a(?:_n)?\b', r'uniform-in-a\b',
             r'uniform(?:ly)? along (?:a_n|the trajectory|any trajectory|every trajectory|a trajectory)',
             r'uniform in the lattice spacing']
    M_TOK = [r'uniform kogut', r'uniform model', r'uniform triple', r'uniform coefficients?', r'uniform fixed-spacing']
    ALL_TOK = re.compile('|'.join('(?:%s)' % t for t in (N_TOK + A_TOK + M_TOK)))
    A_RE = re.compile('|'.join('(?:%s)' % t for t in A_TOK))
    NEG = re.compile(r"\b(not|no|never|none|nor|fails?|failed|failure|without|false|missing|requires?|required|would|unproved|lacks?|absent|excluded?|exclusions?|forbidden|cannot)\b")
    CONJ = re.compile(r'uniform(?:ly)? in n (?:and|or|hence|therefore|thus|so) (?:in )?a\b|uniform(?:ly)? in a (?:and|or) (?:in )?n\b|in both n and a\b')

    def sentences(text):
        return [x for x in re.split(r'(?<=[.;!?])\s+|\n', text) if x.strip()]

    def body_of(text):
        return strip_code(text.replace(template, ' '))

    def uniform_violations(text):
        bad = []
        for sent in sentences(body_of(text).lower()):
            occ = len(re.findall(r'uniform', sent))
            qual = len(ALL_TOK.findall(sent))
            if occ != qual:
                bad.append(('unqualified', sent[:100]))
            if A_RE.search(sent) and not NEG.search(sent):
                bad.append(('a-sense without negation or requirement', sent[:100]))
            if CONJ.search(sent):
                bad.append(('two senses conjoined', sent[:100]))
        return bad

    def scan_uniform(text):
        bad = uniform_violations(text)
        require(not bad, 'uniform qualifier rule violated: ' + repr(bad[:3]))
        return True

    REQ_BODY = ['hypothesis of asymptotic-freedom form', 'not derived here', 'no rigorous construction of a genuine asymptotic-freedom trajectory',
                'unaudited', 'not imported', 'not absence of a gap', 'no number in this report is a fraction of the continuum problem']

    def scan_report(text):
        require(template in text, 'mandatory sentence (contract template) missing from the report')
        require(LABEL in text and UNIFORM_IN_N_SCOPE in text, 'model label or uniform_in_N scope string missing')
        body = body_of(text)
        low = re.sub(r'\s+', ' ', body.lower())
        for ph in V['forbidden']:
            require(ph not in low, 'forbidden phrasing in the report: ' + ph)
        for sent in sentences(body.lower()):
            if 'limit exists' in sent:
                require(NEG.search(sent) is not None or 'whether' in sent, '"limit exists" asserted without negation: ' + sent[:90])
        for ph in REQ_BODY:
            require(ph in low, 'required statement missing: ' + ph)
        for n_ in (cd['cap']['n_star'], cd['bridge']['n_star'], pr['cap']['n_star'], pr['bridge']['n_star']):
            require(re.search(r'n\*=%d\b' % n_, text) is not None, 'crossover index missing from the report: %d' % n_)
        for val in (s(g4_cap), '312500', s(floor_lo)):
            require(val in text, 'report does not carry the exact value ' + val[:30])
        scan_uniform(text)
        return True
    tmpl_low = template.lower()
    tmpl_uniform = {'occurrences': len(re.findall(r'uniform', tmpl_low)), 'qualified_in_place': len(ALL_TOK.findall(tmpl_low)),
                    'n_sense_qualifier': 'volume-uniform' in tmpl_low, 'a_sense_negated': bool(A_RE.search(tmpl_low)) and bool(NEG.search(tmpl_low)),
                    'reading': "'exactly one uniform estimate' is qualified by its apposition 'the volume-uniform gap'; both a-sense occurrences are negated"}
    check('mandatory_sentence_and_phrasing',
          scan_report(report_text) and tmpl_uniform['n_sense_qualifier'] and tmpl_uniform['a_sense_negated']
          and rejected(lambda: scan_report(report_text + '\nThe continuum limit exists along the toy.\n'), 'report_phrase_the_continuum_limit_exists')
          and rejected(lambda: scan_report(report_text + '\nThis loop settles a fraction of the problem.\n'), 'report_phrase_fraction_of_the_problem')
          and rejected(lambda: scan_report(report_text + '\nA continuum limit exists.\n'), 'report_limit_exists_asserted')
          and rejected(lambda: scan_report(report_text.replace(template, template.replace('this is not a statement', 'this is a statement'))), 'mandatory_sentence_negation_removed')
          and rejected(lambda: scan_report(report_text.replace('not derived here', 'derived here')), 'hypothesis_status_removed'),
          mandatory_sentence=template, template_uniform_qualification=tmpl_uniform, forbidden_phrasings=V['forbidden'],
          report_scan='report.md scanned with the mandatory sentence and code spans removed: no forbidden phrasing, every "limit exists" sentence negated, required statements present, crossover indices and exact values present')

    check('uniform_in_N_not_in_a',
          scan_uniform(report_text)
          and rejected(lambda: scan_uniform(report_text + '\nThe gap is uniform.\n'), 'unqualified_uniform_sentence')
          and rejected(lambda: scan_uniform(report_text + '\nThe gap is uniform in a.\n'), 'positive_uniform_in_a_sentence')
          and rejected(lambda: scan_uniform(report_text + '\nThe gap is uniform in N and in a.\n'), 'two_senses_conjoined')
          and rejected(lambda: scan_uniform(report_text + '\nThe estimate holds uniformly along the trajectory.\n'), 'positive_uniformly_along_the_trajectory'),
          rule='every occurrence of "uniform" in a sentence of report.md (template and code spans removed) is qualified in place as N-sense (volume-uniform, uniform in N), a-sense (uniform in a, uniform-in-a, uniform along a_n/the trajectory) or model-sense (uniform Kogut-Susskind, uniform model/triple/coefficient); every a-sense sentence carries a negation or requirement word; the two senses are never conjoined',
          N_tokens=N_TOK, a_tokens=A_TOK, model_tokens=M_TOK)

    # continuum requirements table (section 4.3)
    def parse_requirements(text):
        sec = text.split('### 4.3 ', 1)
        require(len(sec) == 2, 'requirements section 4.3 missing')
        body = sec[1].split('\n### ', 1)[0]
        out = []
        for ln_ in body.splitlines():
            if re.match(r'^\| R\d \|', ln_):
                cols = [x.strip() for x in ln_.strip().strip('|').split(' | ')]
                require(len(cols) == 5, 'requirement row must have five columns')
                out.append({'id': cols[0], 'requirement': cols[1], 'supplied_at_fixed_a': cols[2], 'missing_premise': cols[3], 'status': cols[4]})
        return out
    KEYS = [('a_n', 'E_star'), ('Osterwalder', 'Hamiltonian'), ('E_star', 'a_n')]

    def validate_requirements(rows):
        require(len(rows) == 3, 'exactly three requirement rows')
        for k, (row, name, keys) in enumerate(zip(rows, V['requirement_names'], KEYS)):
            require(row['id'] == 'R%d' % (k + 1) and row['requirement'] == name, 'requirement row name/order differs from contract item 4: ' + row['requirement'])
            require(row['status'] == 'missing', 'every continuum requirement stays missing')
            require(len(row['missing_premise']) > 60 and len(row['supplied_at_fixed_a']) > 20, 'empty column')
            joined = row['supplied_at_fixed_a'] + ' ' + row['missing_premise']
            require(all(key in joined for key in keys), 'requirement row lacks its content: ' + name)
        return True
    req_rows = parse_requirements(report_text)
    check('continuum_requirements_listed',
          validate_requirements(req_rows)
          and rejected(lambda: validate_requirements(req_rows[:2]), 'physical_scale_row_removed')
          and rejected(lambda: validate_requirements([dict(r_, status='supplied') if i == 0 else r_ for i, r_ in enumerate(req_rows)]), 'uniform_in_a_marked_supplied')
          and rejected(lambda: validate_requirements([dict(r_, missing_premise='') if i == 1 else r_ for i, r_ in enumerate(req_rows)]), 'reconstruction_premise_emptied'),
          rows=len(req_rows), names=[r_['requirement'] for r_ in req_rows], statuses=[r_['status'] for r_ in req_rows],
          source='the three names are read from contract item 4; the table is parsed from report.md section 4.3')

    # unaudited lead (Faizal-Shabir) recorded, not imported
    sota = read_input(P_SOTA)
    his4 = read_input(P_HIS4)
    memo = read_input(P_MEMO)
    lead_ok = ('Faizal-Shabir arXiv:2606.19362' in sota and 'read at abstract level only, no priority or correctness statement follows' in sota
               and 'It is recorded as provenance and a lead for a future round, nothing more' in mod4
               and 'found no rigorous uniform-in-`a` result for this or a comparable strong-coupling lattice family to import instead' in his4
               and 'What it fails to supply: any estimate uniform along a -> 0 with g(a) -> 0' in memo)
    IMPORTED = sorted(set(expected_inputs))
    LEADS = [{'source': 'Faizal & Shabir, arXiv:2606.19362 (Fortschr. Phys. 74 (2026) e70097)', 'claim': 'strong-coupling and asymptotically-free continuum limits coincide',
              'reading_depth': 'abstract only (modern lens)', 'audited': False, 'imported': False}]

    def validate_leads(imported, leads):
        require(all('2606.19362' not in x for x in imported), 'an unaudited claimed construction imported as a premise')
        for ld in leads:
            require(ld['audited'] is False and ld['imported'] is False, 'an unaudited lead relabelled audited or imported')
        return True
    check('unaudited_lead_not_imported',
          lead_ok and validate_leads(IMPORTED, LEADS)
          and rejected(lambda: validate_leads(IMPORTED + ['arXiv:2606.19362'], LEADS), 'faizal_shabir_imported_as_premise')
          and rejected(lambda: validate_leads(IMPORTED, [dict(LEADS[0], audited=True)]), 'faizal_shabir_marked_audited'),
          leads=LEADS, source_search='this producer ran no source search of its own; the statement rests on the searches recorded in the snapshotted modern memo, modern update-4 and historical update-4')

    # ======================= flags and gate fields =======================
    FLAGS = {'continuum_claim': False, 'uniform_in_a_claimed': False, 'weak_coupling_claim': False, 'loop_count_fraction_claimed': False,
             'uniform_in_N_claimed': True, 'uniform_in_N_scope': UNIFORM_IN_N_SCOPE, 'uniform_wilson_claim': False,
             'resolved_interaction_shift': False, 'scientific_priority_verified': False}

    def validate_flags(fl):
        for k1, v1 in FLAGS.items():
            require(fl.get(k1) == v1 and type(fl.get(k1)) is type(v1), 'claim flag ' + k1 + ' must be ' + repr(v1))
        return True

    def fmut(**kw):
        f2_ = dict(FLAGS)
        f2_.update(kw)
        return lambda: validate_flags(f2_)
    gate_fields = {k1: FLAGS[k1] for k1 in ('continuum_claim', 'uniform_in_a_claimed', 'weak_coupling_claim', 'loop_count_fraction_claimed',
                                            'uniform_in_N_claimed', 'uniform_in_N_scope')}
    check('gate_fields_exported',
          validate_flags(FLAGS) and all(FLAGS[k1] is v1 for k1, v1 in V['gate_fields'].items()) and sorted(V['gate_fields']) == sorted(
              ['continuum_claim', 'uniform_in_a_claimed', 'weak_coupling_claim', 'loop_count_fraction_claimed'])
          and FLAGS['uniform_in_N_scope'] == V['scope_from_contract']
          and rejected(fmut(uniform_in_N_scope='uniform in a'), 'uniform_in_N_scope_changed')
          and rejected(fmut(uniform_in_N_claimed=False), 'uniform_in_N_dropped'),
          gate_fields=gate_fields, source='preregistration.gate_fields_required plus required item 5 (uniform_in_N_claimed with its scope string)')

    check('no_priority_or_continuum_claim',
          validate_flags(FLAGS)
          and rejected(fmut(continuum_claim=True), 'continuum_true') and rejected(fmut(scientific_priority_verified=True), 'priority_true')
          and rejected(fmut(weak_coupling_claim=True), 'weak_coupling_true') and rejected(fmut(uniform_wilson_claim=True), 'uniform_wilson_true')
          and rejected(fmut(resolved_interaction_shift=True), 'shift_true') and rejected(fmut(uniform_in_a_claimed=True), 'uniform_in_a_true'),
          historical_or_occult_numeric_premise=False,
          uniform_wilson_note='AX1 exported uniform_wilson_claim:true meaning only the uniform-model label; AZ1 makes no Wilson-mean claim, so it is false here and the uniform-model meaning is carried by the label')

    def validate_no_fraction(pk):
        require(pk.get('loop_count_fraction_claimed') is False, 'loop count claimed as a fraction')
        for k1 in pk:
            require('percent' not in k1 and 'fraction_of' not in k1, 'a fraction/percentage field of the continuum problem: ' + k1)
        return True
    check('loop_count_not_fraction',
          validate_no_fraction(FLAGS) and c['sequence'] == 9 and c['stop'] == 'Investigation 9 of 10.'
          and rejected(fmut(loop_count_fraction_claimed=True), 'loop_count_fraction_true')
          and rejected(lambda: validate_no_fraction(dict(FLAGS, continuum_fraction_of_problem='9/10')), 'investigation_index_as_fraction_field')
          and rejected(lambda: scan_report(report_text + '\nNine of ten loops settle 90 percent; a fraction of the problem is done.\n'), 'fraction_sentence_in_report'),
          investigation_index='9 of 10 (an index of executed Round32 investigations, not a measure of the continuum problem)')

    # ======================= bridge obstruction and common rescaling =======================
    def validate_bridge(threshold, retained, rescaling_moves_tau):
        require(retained is True, 'the AL1 bridge obstruction must be retained')
        require(rat(threshold) == bridge_al1 == V['bridge_g4'], 'bridge threshold differs from AL1 (g^4>=32)')
        require(rat(threshold) * bridge_r == r_num_al1, 'bridge r<=1/8 <=> g^4>=32')
        require(rescaling_moves_tau is False and tau_a_invariant and r_common, 'a common rescaling cannot move tau (tau depends on g only)')
        return True
    check('bridge_obstruction_retained',
          validate_bridge(32, True, False) and ok_path and al1_general
          and rejected(lambda: validate_bridge(32, False, False), 'bridge_obstruction_dropped')
          and rejected(lambda: validate_bridge(Q(32, 3), True, False), 'R18_B2_bound_32_over_3_substituted')
          and rejected(lambda: validate_bridge(32, True, True), 'common_rescaling_claimed_to_reach_the_cap')
          and rejected(lambda: validate_dictionary(env, ['tau=96*a/g^4']), 'a_dependent_tau'),
          bridge='r=4/g^4<=1/8 <=> g^4>=32 (AL1); on the AL1 frozen path g_n^4=1/n^2<32 for every n>=1; on the declared toy it fails from n*=132 on',
          common_rescaling='tau(c*a)=tau(a) and r(c*alpha,c*lambda)=r exactly: rescaling a, E_star or the whole Hamiltonian cannot move tau; only g does (derived here from the AL1 dictionary; the AL2 result is not a shared premise)')

    # ======================= arithmetic, roots, verdict =======================
    check('exact_arithmetic_admission',
          rat('1/100000000') == tau_cap and sci('9.6x10^9') == g4_cap and sci('10^-8') == tau_cap
          and rejected(lambda: rat(9.6e9), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('nan'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator')
          and rejected(lambda: rat(pr['cap']['g_n_star^4_preview']), 'decimal_preview_as_admission_value')
          and rejected(lambda: validate_crossover(9.6e9, g4_cap, 2), 'float_coupling_in_crossover')
          and rejected(lambda: pconst(Q(1, 2)), 'non_integer_polynomial_coefficient'),
          arithmetic='fractions.Fraction and Python integers throughout; integer square/fourth roots with explicit brackets; previews truncated from exact rationals')

    def validate_root_route(kind, n_claim, g04, T):
        require(kind == 'exact integer fourth root', 'crossover must use the exact integer fourth root of g_0^4/T')
        return validate_crossover(g04, T, n_claim)
    F_panel = (TOYS['panel_rehearsal']['g0_4'] / g4_cap).numerator // (TOYS['panel_rehearsal']['g0_4'] / g4_cap).denominator

    def validate_volume_factor(factors):
        require(all(f == 1 for f in factors), 'the cited gap is volume-uniform: no N-dependent (root-N) degradation')
        return True
    check('root_n_misuse',
          validate_root_route('exact integer fourth root', 4, TOYS['panel_rehearsal']['g0_4'], g4_cap) and validate_volume_factor([Q(1)] * 5)
          and rejected(lambda: validate_root_route('square root', isqrt(F_panel) + 1, TOYS['panel_rehearsal']['g0_4'], g4_cap), 'square_root_index_11')
          and rejected(lambda: validate_crossover(TOYS['panel_rehearsal']['g0_4'], g4_cap, crossover_root(TOYS['panel_rehearsal']['g0_4'], g4_cap, p=2)), 'g_n4_read_as_g0_4_over_n2')
          and rejected(lambda: validate_volume_factor([Q(1, isqrt(N_) if isqrt(N_) ** 2 == N_ else 1) for N_ in (1, 4, 9, 16, 25)]), 'gap_divided_by_root_N'),
          note='n* uses the exact fourth root because g_n^4=g_0^4/n^4; the gap is volume-uniform (every N), with no statistical or root-N factor')

    overclaim = any(FLAGS[k1] is True for k1 in ('continuum_claim', 'uniform_in_a_claimed', 'weak_coupling_claim', 'loop_count_fraction_claimed',
                                                 'uniform_wilson_claim', 'resolved_interaction_shift', 'scientific_priority_verified'))
    verdict = forward_verdict(True, True, overclaim)
    RETAINED = {'cap_declared_toy_leaves_admitted_regime': 'n*=%d' % cd['cap']['n_star'],
                'cap_declared_toy_leaves_bridge': 'n*=%d' % cd['bridge']['n_star'],
                'panel_toy_leaves_admitted_regime': 'n*=%d' % pr['cap']['n_star'], 'panel_toy_leaves_bridge': 'n*=%d' % pr['bridge']['n_star'],
                'al1_frozen_path_fails_bridge_every_n': 'g_n^4=1/n^2<32', 'i1_omitted_conditions_unevaluated': 'c1(S), c2(S) unevaluated',
                'no_estimate_along_a_n': 'none supplied'}

    def validate_verdict(reported, *args):
        require(reported == forward_verdict(*args), 'reported verdict differs from the contract acceptance rule')
        return True

    def validate_retained(rt):
        require(sorted(rt) == sorted(RETAINED), 'a retained failure was dropped')
        require(all(v1 == RETAINED[k1] for k1, v1 in rt.items()), 'a retained failure was altered')
        return True
    check('insufficient_verdict_retained',
          verdict == 'accepted_within_scope' and forward_verdict(False, True, False) == 'limited' and forward_verdict(True, True, True) == 'insufficient'
          and validate_retained(RETAINED)
          and rejected(lambda: validate_verdict('accepted_within_scope', False, True, False), 'missing_citation_relabelled_accepted')
          and rejected(lambda: validate_verdict('limited', True, True, True), 'overclaim_relabelled_limited')
          and rejected(lambda: validate_verdict('accepted_within_scope', True, False, False), 'inexact_arithmetic_relabelled_accepted')
          and rejected(lambda: validate_retained({k1: v1 for k1, v1 in RETAINED.items() if k1 != 'al1_frozen_path_fails_bridge_every_n'}), 'al1_path_failure_dropped')
          and rejected(lambda: validate_retained(dict(RETAINED, no_estimate_along_a_n='supplied')), 'failure_point_relabelled_resolved'),
          retained_failures=RETAINED, rule=V['acceptance'],
          producer_reading='inexact dictionary arithmetic is read as limited (the contract names only the citation case); an overclaim is insufficient')

    # ======================= error ledger =======================
    ledger = {'not_applicable': {'status': 'not_applicable', 'reason': 'statement loop: exact integer/rational dictionary arithmetic and exact crossover indices only; no enclosure; the only irrational quantity (g^2 at the cap, sqrt(9.6x10^9)) is bracketed by directed integer square roots of width 10^-30 and enters only as a lower bound'}}
    check('error_ledger_itemized',
          V['error_terms'][0].startswith('not_applicable') and 'stated reason' in V['error_terms_rule'] and 'reason' in ledger['not_applicable'],
          ledger=ledger, preregistered=V['error_terms'])

    # ======================= contract wording defects (non-blocking) =======================
    defects = []
    if 'the continuum limit exists' in template and 'the continuum limit exists' in V['forbidden']:
        defects.append({'id': 'D1', 'field': 'preregistration.mandatory_sentence_template', 'defect': "the template contains the forbidden phrase 'the continuum limit exists' (negated); the report scan removes the template's verbatim occurrence before scanning"})
    if 'supplies exactly one uniform estimate' in template and "D'_ii" in acc_ax1 and '102|tau|' in acc_ax1:
        defects.append({'id': 'D2', 'field': 'preregistration.mandatory_sentence_template', 'defect': "'supplies exactly one uniform estimate': the AX1 gate also admits other volume-uniform constants at fixed a (D'_ii, reset 102|tau|); read with item 2 as 'exactly one necessary estimate'; none of them is uniform along a_n->0"})
    if 'the AM2 contraction needs tau<=10^-8' in V['failed_text'] and 'It does not establish a sharp threshold' in am2r:
        defects.append({'id': 'D3', 'field': 'parameters.failed', 'defect': "'the AM2 contraction needs tau<=10^-8': 10^-8 is the preregistered cap at which the AM2/AX1 certificates are admitted, not a sharp threshold (AM2 reverse; AX1 forward records contraction-only margins 7/274688 and 1/20416, not admitted); the failure point holds for every fixed cap"})
    if 'failure of common rescaling' in V['required'][3] and not any('/al2' in x for x in V['shared']):
        defects.append({'id': 'D4', 'field': 'required[3]', 'defect': "'the failure of common rescaling' refers to work after AL1 (the AL1 gate selected AL2 to test common scale changes) that is not a shared premise; the invariance is derived here from the AL1 dictionary"})
    if 'the AL1 bridge condition g^4>=32 also fails' in V['failed_text']:
        defects.append({'id': 'D5', 'field': 'parameters.failed', 'defect': "'the AL1 bridge condition g^4>=32 also fails': on a g_n->0 path it fails from a finite index on (declared toy n*=132, rehearsal n*=421), not at every n; it fails at every n only on the AL1 frozen path"})
    if V['triple'] == [0, 0, 0]:
        defects.append({'id': 'D6', 'field': 'preregistration.selected_triple_alpha_units', 'defect': '["0","0","0"] is read as the route-B Haar reference; in the uniform model every selected face carries tau/24 in alpha units, held in psi_b (AX1 gate)'})
    if 'a_n' not in V['toy_text']:
        defects.append({'id': 'D7', 'field': 'parameters.toy_trajectory', 'defect': 'names g_n and a fixed E_star but not a_n; a_n=a_0/n is declared here; the crossovers do not depend on a_n (tau is independent of a)'})
    if V['signs'] == ['+', '-']:
        defects.append({'id': 'D8', 'field': 'preregistration.tau.signs_evaluated', 'defect': 'a real-g trajectory has tau=96/g^4>0; tau<0 is the U_E mirror of +|tau| (AX1), not a trajectory point; both signs share the cap'})
    if 'finite_volume uniform bound' in V['state_provenance']:
        defects.append({'id': 'D9', 'field': 'preregistration.state_provenance', 'defect': "'finite_volume uniform bound' carries an unqualified 'uniform'; read as volume-uniform at fixed a"})
    relayed = [{'id': 'R1', 'source': 'relayed task instruction (not contract text)', 'note': "uniform_wilson_claim is exported false as instructed; the AX1 gate's true meant only the uniform-model label, which AZ1 carries in its label"},
               {'id': 'R2', 'source': 'relayed task instruction (not contract text)', 'note': "the relayed freeze command omits --verdict, which research/round32/tools/freeze.py requires; the proposed forward verdict text is passed"}]
    check('contract_wording_defects_recorded', len(defects) == 9 and panel_g3_note['claimed_correct'] is False,
          defects=defects, relayed_instruction_notes=relayed, premise_arithmetic_notes=[panel_g3_note], blocking=False)

    # ======================= map table in the report =======================
    def map_rows(text):
        sec = text.split('### 5.9 ', 1)
        require(len(sec) == 2, 'map section 5.9 missing')
        return [ln_ for ln_ in sec[1].split('\n### ', 1)[0].splitlines() if ln_.startswith('| ')]

    def validate_map(rows):
        missing_ids = [cid for cid in V['controls'] if not any(r1.startswith('| `' + cid + '` |') for r1 in rows)]
        missing_items = [k for k in range(1, 7) if not any(r1.startswith('| item %d ' % k) for r1 in rows)]
        require(not missing_ids and not missing_items, 'map lacks rows for ' + ','.join(missing_ids + ['item %d' % k for k in missing_items]))
        return True
    mrows = map_rows(report_text)
    check('report_item_and_control_map',
          validate_map(mrows)
          and rejected(lambda: validate_map([r1 for r1 in mrows if not r1.startswith('| `toy_trajectory_crossover_exact` |')]), 'control_row_removed_from_map')
          and rejected(lambda: validate_map([r1 for r1 in mrows if not r1.startswith('| item 3 ')]), 'item_3_row_removed_from_map'),
          controls_in_map=len(V['controls']), items_in_map=6, map_section='report.md section 5.9')

    # ======================= packet, tampering =======================
    identities_verified = ALL_IDS
    headline = {
        'dictionary': 'alpha=g^2/(2a), lambda=2/(g^2 a), tau=24*lambda/alpha=96/g^4 (AL1), hbar=c=1',
        'identities_verified': identities_verified, 'identity_routes': ['integer-polynomial cross-multiplication in (g, a, c)', 'exact Fraction grid, 35 points'],
        'tau_cap': s(tau_cap), 'g4_at_cap': s(g4_cap), 'admitted_regime': '|tau|<=10^-8 <=> g^4>=9600000000 at fixed a (strong bare coupling)',
        'supplied_estimate': 'volume-uniform gap alpha/16=g^2/(32a) for g^4>=9.6x10^9 at fixed a (AX1 gate, cited)',
        'gap_example': {'a_fm': s(A0_FM), 'g2': s(g2_ex), 'gap_fm_inverse': s(gap_ex), 'gap_over_E_star': s(gap_ex),
                        'gap_MeV_preview': dec(gap_ex * hbarc_prev, 8)},
        'lattice_units_floor_lower': s(floor_lo), 'lattice_units_floor_preview': dec(floor_lo),
        'crossovers': {'cap_declared_g0^4=9600000000': {'g0_4': s(TOYS['cap_declared']['g0_4']), 'n*_cap': cd['cap']['n_star'], 'n*_bridge': cd['bridge']['n_star']},
                       'panel_rehearsal_g0=1000': {'g0_4': s(TOYS['panel_rehearsal']['g0_4']), 'n*_cap': pr['cap']['n_star'], 'n*_bridge': pr['bridge']['n_star']}},
        'bridge_g4': s(V['bridge_g4']),
        'target': {'value': s(target), 'comparator': '>=', 'achieved': len(identities_verified) + 4, 'met': len(identities_verified) + 4 >= target},
    }
    verdict_line = verdict + " (forward half of a statement+skeptic loop; admission requires the skeptic's independent derivation and replays); no sub-label proposed"
    packet = {
        'loop': 'AZ1', 'direction': 'forward', 'human_author': HUMAN_AUTHOR,
        'contribution_alias': 'HNM-AZ1-F forward continuum-trajectory statement: the one estimate the fixed-spacing family supplies (the volume-uniform gap alpha/16=g^2/(32a) at fixed a, cited from AX1) and its failure point along a named (a_n,g_n) with exact toy crossovers',
        'ai_assistance': 'AI-assisted forward production (a Claude model agent); correlated model-agent work, not independent human review',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha, 'ax1_gate_sha256': ax1_sha,
        'al1_gate_sha256': inventory[P_AL1_GATE], 'am2_gate_sha256': inventory[P_AM2_GATE],
        'label': LABEL, 'model': MODEL, 'trajectory': TRAJ, 'estimates': [ESTIMATE], 'headline': headline,
        'mandatory_sentence': template, 'requirements': req_rows, 'leads_recorded': LEADS, 'retained_failures': RETAINED,
        'error_terms_itemized': ledger, 'gate_fields': gate_fields,
        'exclusions': {'contract': V['claim_exclusions'], 'preregistration': V['prereg_exclusions'],
                       'additional': ['no statement about the actual gap where the certificate does not apply (failure of a sufficient certificate is not absence of a gap)',
                                      'no asymptotic-freedom trajectory is derived; no numerical beta-function coefficient is used',
                                      'the unaudited Faizal-Shabir construction is recorded as a lead, not imported',
                                      'the contraction-only margins of the AX1 forward report are not admitted regimes',
                                      'no estimate is volume-uniform and uniform in a at once']},
        'contract_wording_defects': defects, 'relayed_instruction_notes': relayed, 'premise_arithmetic_notes': [panel_g3_note],
        'routes_executed': ['forward: dictionary identities as integer-polynomial rational-function identities (cross-multiplication) in (g, a, c)',
                            'forward: the same identities by direct exact Fraction arithmetic on a 35-point grid',
                            'forward: admitted regime, supplied estimate and first-order mean parsed from the hash-bound AX1/AL1/AM2 gates and reports',
                            'forward: toy-trajectory crossovers by exact integer fourth roots and by exact Fraction scans; panel rehearsal reproduced',
                            'forward: inherited incidence and cover geometry recomputed from the I1 owner map',
                            'forward: report scan (mandatory sentence, forbidden phrasings, uniform qualifier rule, requirement table, map)'],
        'routes_not_executed': ['skeptic independent derivation and replays (single_direction_independent_replay; outside this producer)'],
        'controls_deferred': {},
        'protocol_steps_outside_check_py': {'freeze_and_byte_identical_replays': 'research/round32/tools/freeze.py',
                                            'skeptic_review': 'independent derivation and replays by the skeptic'},
        'proposed_forward_verdict': verdict_line,
    }
    packet.update(FLAGS)

    def packet_hash(pk):
        body = {k1: v1 for k1, v1 in pk.items() if k1 != 'packet_sha256'}
        return sha_bytes(json.dumps(body, sort_keys=True).encode('utf-8'))

    def validate_packet(pk, inv):
        require(pk.get('packet_sha256') == packet_hash(pk), 'packet hash mismatch')
        ids = {ch['id']: ch for ch in pk['checks']}
        for cid in V['controls']:
            if cid == 'coherent_evidence_tampering':
                continue
            require(cid in ids and ids[cid]['passed'] is True, 'required control missing or failed: ' + cid)
        validate_flags({k1: pk[k1] for k1 in FLAGS})
        require(sorted(inv) == sorted(set(expected_inputs)), 'premise snapshot inventory incomplete')
        require(pk['ax1_gate_sha256'] == inv[P_AX1_GATE] == ax1_sha, 'AX1 gate hash changed')
        require(pk['al1_gate_sha256'] == inv[P_AL1_GATE], 'AL1 gate hash changed')
        hd = pk['headline']
        require(rat(hd['g4_at_cap']) == 96 / rat(hd['tau_cap']) == g4_cap, 'cap coupling differs from recomputation')
        for key, toy in (('cap_declared_g0^4=9600000000', TOYS['cap_declared']), ('panel_rehearsal_g0=1000', TOYS['panel_rehearsal'])):
            row = hd['crossovers'][key]
            require(rat(row['g0_4']) == toy['g0_4'], 'toy coupling changed')
            validate_crossover(toy['g0_4'], g4_cap, row['n*_cap'])
            validate_crossover(toy['g0_4'], rat(hd['bridge_g4']), row['n*_bridge'])
        require(rat(hd['bridge_g4']) == bridge_al1, 'bridge threshold changed')
        ge = hd['gap_example']
        require(rat(ge['gap_fm_inverse']) == rat(ge['g2']) / (32 * rat(ge['a_fm'])) == gap_ex, 'gap example differs from recomputation')
        require(rat(hd['lattice_units_floor_lower']) == floor_lo, 'lattice-units floor differs')
        require(pk['mandatory_sentence'] == template, 'mandatory sentence differs from the contract template')
        require(pk['label'] == LABEL and pk['uniform_in_N_scope'] == UNIFORM_IN_N_SCOPE, 'label or scope changed')
        validate_estimates(pk['estimates'])
        validate_trajectory(pk['trajectory'])
        validate_model(pk['model'])
        validate_requirements(pk['requirements'])
        validate_retained(pk['retained_failures'])
        validate_leads(sorted(inv), pk['leads_recorded'])
        require(ids['toy_trajectory_crossover_exact']['crossovers']['cap_declared']['bridge']['n_star'] == hd['crossovers']['cap_declared_g0^4=9600000000']['n*_bridge'],
                'crossover details differ from the headline')
        require(pk['proposed_forward_verdict'].startswith(forward_verdict(True, True, False) + ' '), 'verdict changed')
        return True

    base_packet = dict(packet)
    base_packet['checks'] = [dict(ch) for ch in CHECKS]
    base_packet['packet_sha256'] = packet_hash(base_packet)

    def tamper(fn):
        def run():
            pk = json.loads(json.dumps(base_packet))
            inv = dict(inventory)
            fn(pk, inv)
            pk['packet_sha256'] = packet_hash(pk)
            return validate_packet(pk, inv)
        return run

    def t_control(pk, inv):
        for ch in pk['checks']:
            if ch['id'] == 'bridge_obstruction_retained':
                ch['passed'] = False

    def t_bridge(pk, inv):
        pk['headline']['crossovers']['cap_declared_g0^4=9600000000']['n*_bridge'] = 131

    def t_cap_n(pk, inv):
        pk['headline']['crossovers']['cap_declared_g0^4=9600000000']['n*_cap'] = 1

    def t_g4(pk, inv):
        pk['headline']['g4_at_cap'] = '960000000'

    def t_ua(pk, inv):
        pk['uniform_in_a_claimed'] = True

    def t_scope(pk, inv):
        pk['uniform_in_N_scope'] = 'uniform in N and in a'

    def t_gate(pk, inv):
        inv[P_AX1_GATE] = '0' * 64
        pk['ax1_gate_sha256'] = '0' * 64

    def t_snapshot(pk, inv):
        inv.pop(P_AL1_GATE)

    def t_sentence(pk, inv):
        pk['mandatory_sentence'] = pk['mandatory_sentence'].replace('fails to supply', 'supplies')

    def t_gap(pk, inv):
        pk['headline']['gap_example']['gap_fm_inverse'] = s(2 * gap_ex)

    def t_est(pk, inv):
        pk['estimates'].append(dict(pk['estimates'][0], id='E2'))

    def t_traj(pk, inv):
        pk['trajectory']['derived'] = True

    def t_req(pk, inv):
        pk['requirements'][0]['status'] = 'supplied'

    def t_verdict(pk, inv):
        pk['proposed_forward_verdict'] = 'limited (tampered)'

    def t_continuum(pk, inv):
        pk['continuum_claim'] = True

    def t_retained(pk, inv):
        pk['retained_failures'].pop('no_estimate_along_a_n')
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(tamper(t_control), 'control_boolean_flipped_hash_rebound')
          and rejected(tamper(t_bridge), 'bridge_crossover_131_hash_rebound')
          and rejected(tamper(t_cap_n), 'cap_crossover_1_hash_rebound')
          and rejected(tamper(t_g4), 'g4_cap_decade_hash_rebound')
          and rejected(tamper(t_ua), 'uniform_in_a_flag_hash_rebound')
          and rejected(tamper(t_scope), 'uniform_in_N_scope_hash_rebound')
          and rejected(tamper(t_gate), 'ax1_gate_hash_replaced_hash_rebound')
          and rejected(tamper(t_snapshot), 'al1_gate_snapshot_removed_hash_rebound')
          and rejected(tamper(t_sentence), 'mandatory_sentence_altered_hash_rebound')
          and rejected(tamper(t_gap), 'gap_example_doubled_hash_rebound')
          and rejected(tamper(t_est), 'second_estimate_added_hash_rebound')
          and rejected(tamper(t_traj), 'trajectory_marked_derived_hash_rebound')
          and rejected(tamper(t_req), 'requirement_marked_supplied_hash_rebound')
          and rejected(tamper(t_verdict), 'verdict_changed_hash_rebound')
          and rejected(tamper(t_continuum), 'continuum_flag_hash_rebound')
          and rejected(tamper(t_retained), 'retained_failure_dropped_hash_rebound'))

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in V['controls'] if cid not in ids]
    require(not missing, 'contract controls without a check: ' + ','.join(missing))
    positive_only = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch.get('rejected_mutations')]
    require(not positive_only, 'contract controls without a damaging mutation: ' + ','.join(positive_only))
    require(not PENDING, 'rejected mutations not attached to a check')
    packet['checks'] = CHECKS
    packet['contract_controls_covered'] = sorted(V['controls'])
    packet['controls_with_damaging_mutations'] = sum(1 for ch in CHECKS if ch['id'] in V['controls'] and ch.get('rejected_mutations'))
    packet['rejected_mutations_in_control_checks'] = sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS if ch['id'] in V['controls'])
    packet['rejected_mutation_total'] = sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS)
    packet['check_count'] = len(CHECKS)
    dumped = json.dumps(packet, sort_keys=True)
    require('u=s/' not in dumped and 'exp(-24' not in dumped and 'e^{-24' not in dumped, 'forbidden normalized clock or exponent in the packet')
    return packet


def main():
    ap = argparse.ArgumentParser(description='AZ1 forward exact checker')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    require(out.is_absolute(), 'absolute output directory required')
    out = out.resolve()
    require(not out.exists(), 'fresh (non-existent) output directory required')
    require(ROOT not in out.parents and out != ROOT, 'output directory must be outside the checkout')
    check_sha = sha(BASE / 'check.py')   # recorded before any evaluation
    result = compute(check_sha)
    require(float_free(result), 'floating-point value in results')
    out.mkdir(parents=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    sources = {}
    for p in sorted(BASE.rglob('*')):
        rel = p.relative_to(BASE)
        if p.is_file() and (rel.parts[0] == 'inputs' or p.name in ('check.py', 'report.md')) and rel.parts[0] != 'output':
            sources[rel.as_posix()] = sha(p)
    manifest = {'loop': 'AZ1', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    hd = result['headline']
    print(json.dumps({'loop': 'AZ1', 'direction': 'forward', 'checks': len(result['checks']), 'g4_at_cap': hd['g4_at_cap'],
                      'crossovers': hd['crossovers'], 'controls_with_damaging_mutations': result['controls_with_damaging_mutations'],
                      'verdict': result['proposed_forward_verdict']}, sort_keys=True))


if __name__ == '__main__':
    main()
