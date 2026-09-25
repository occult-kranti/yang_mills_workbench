#!/usr/bin/env python3
"""AZ2 forward producer (single producer of a single+skeptic loop): exact finite-graph Wilson
coefficients on the Round11 two-plaquette graph (seven links, six Gauss constraints, gauge-invariant
trace-monomial basis of total polynomial degree D in {6, 8}).

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production (a Claude model agent).

Standard library only (argparse, decimal, fractions, functools, hashlib, json, math, pathlib, re).
The Round11 solver module is a snapshotted premise that imports numpy/scipy; it is NOT imported here.
Its exact conventions (basis, Haar moments, kinetic operator, tail threshold) are re-implemented in
fractions.Fraction and bound to the snapshot text.  A decimal.Decimal inverse iteration only PROPOSES a
Ritz vector; every admission Boolean is decided in exact Fraction arithmetic (complete residual, exact
Gram projections, Temple/Eckart/Davis-Kahan bounds with directed square roots).  Conditions raise
AdmissionError explicitly (never `assert`), so every check stays active under `python -O`.

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import decimal
import hashlib
import json
import re
from fractions import Fraction as Q
from functools import lru_cache
from math import comb, isqrt
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
CONTRACT_REL = 'research/round32/contracts/az2.json'
CONTRACT_SHA256 = '2861d5c59841b5b8e688712aab4faf3edf9f9f8ee2079d8ebbda07fabb7461c3'
HUMAN_AUTHOR = 'Hruday N M (BUNZEEY)'

P_R11_README = 'research/round11/README.md'
P_R11_ADV = 'research/round11/advisor/advisor.md'
P_R11_SOLVER = 'research/round11/solver/two_plaquette.py'
P_R11_SOLVER_README = 'research/round11/solver/README.md'
P_AW1_GATE = 'research/round32/advisor/aw1-gate.json'
P_AW1F = 'research/round32/forward/aw1/report.md'
P_UPD4 = 'research/round32/experts/modern/update-4.md'
P_AT4 = 'research/round31/forward/at4/report.md'
P_I1 = 'research/round21/forward/i1/report.md'
P_SEL = 'research/round32/advisor/selection-az2.md'
P_RESID = 'research/round32/methods/paired-physics-research/references/complete-residual-and-error-scope.md'

LINKS = ('h1', 'h2', 'h3', 'h4', 'vL', 'vM', 'vR')
ORIENT = {'h1': ('TL', 'TM'), 'h2': ('TM', 'TR'), 'h3': ('BL', 'BM'), 'h4': ('BM', 'BR'),
          'vL': ('TL', 'BL'), 'vM': ('TM', 'BM'), 'vR': ('TR', 'BR')}
VERTICES = ('TL', 'TM', 'TR', 'BL', 'BM', 'BR')
LINK_CLASS = {'h1': 'j', 'vL': 'j', 'h3': 'j', 'h2': 'k', 'vR': 'k', 'h4': 'k', 'vM': 'ell'}


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
    if isinstance(value, bool) or isinstance(value, float) or isinstance(value, decimal.Decimal):
        raise AdmissionError('non-exact input rejected: ' + repr(value))
    if isinstance(value, (int, Q)):
        return Q(value)
    if isinstance(value, str) and re.fullmatch(r'-?\d+(/\d+)?', value):
        num, _, den = value.partition('/')
        if den and int(den) == 0:
            raise AdmissionError('zero denominator rejected')
        return Q(int(num), int(den) if den else 1)
    raise AdmissionError('malformed rational rejected: ' + repr(value))


def s(q):
    return str(Q(q))


def dec(q, digits=12):
    """Truncated scientific decimal preview of an exact rational (never an admission value)."""
    q = Q(q)
    if q == 0:
        return '0'
    sign = '-' if q < 0 else ''
    q = abs(q)
    e = len(str(q.numerator)) - len(str(q.denominator))
    while q >= Q(10) ** (e + 1):
        e += 1
    while q < Q(10) ** e:
        e -= 1
    scaled = q / Q(10) ** (e - digits + 1)
    m = str(scaled.numerator // scaled.denominator)
    return sign + m[0] + '.' + m[1:] + 'e' + str(e)


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def magnitude(q):
    """Integer e with 10^e <= |q| < 10^(e+1) (q != 0), exact."""
    q = abs(Q(q))
    e = len(str(q.numerator)) - len(str(q.denominator))
    while q >= Q(10) ** (e + 1):
        e += 1
    while q < Q(10) ** e:
        e -= 1
    return e


def sqrt_bracket(x, sig=40):
    """Directed rational bracket lo <= sqrt(x) <= hi with about `sig` significant digits (integer isqrt)."""
    x = rat(x)
    require(x >= 0, 'square root of a negative number')
    if x == 0:
        return Q(0), Q(0)
    k = sig - magnitude(x) // 2
    scale = Q(10) ** (2 * k)
    n = (x * scale).numerator // (x * scale).denominator
    r = isqrt(n)
    lo = Q(r) / Q(10) ** k
    hi = Q(r + 1) / Q(10) ** k
    require(lo * lo <= x <= hi * hi and lo >= 0, 'directed square-root bracket')
    return lo, hi


def sqrt_up(x, sig=40):
    return sqrt_bracket(x, sig)[1]


def out_dn(q, k):
    """Outward (downward) rounding to denominator 10^k."""
    q = Q(q) * Q(10) ** k
    return Q(q.numerator // q.denominator) / Q(10) ** k


def out_up(q, k):
    q = Q(q) * Q(10) ** k
    return Q(-((-q.numerator) // q.denominator)) / Q(10) ** k


def up_sig(q, sig=30):
    """Upward rounding of a nonnegative rational to about `sig` significant digits (ledger export)."""
    q = Q(q)
    require(q >= 0, 'up_sig expects a nonnegative value')
    if q == 0:
        return Q(0)
    return out_up(q, sig - 1 - magnitude(q))


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
# Contract: every target, grid value, cutoff, control id and reference is read from the sha256-bound snapshot.
# ---------------------------------------------------------------------------
def load_contract():
    raw = (BASE / 'inputs' / CONTRACT_REL).read_bytes()
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen AZ2 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'AZ2' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return c, digest


def contract_values(c):
    pre = c['preregistration']
    v = {}
    v['model'] = c['model']
    require('model_is_finite_graph:true' in v['model'] and 'transfers_to_aq:false' in v['model']
            and 'I1.5 sign convention' in v['model'] and 'seven links, six Gauss constraints' in v['model'], 'model string')
    par = c['parameters']
    require(par['graph'] == 'Round11 two-plaquette', 'graph name')
    v['grid'] = [rat(x) for x in par['tau_FG_grid']]
    require(v['grid'] == [Q(1, 1000), Q(1, 100), Q(1, 10)], 'tau_FG grid')
    v['signs'] = list(pre['tau']['signs_evaluated'])
    require(v['signs'] == ['+', '-'], 'both signs required')
    require(pre['tau']['value'] == 'grid' and pre['tau']['is_model_change_vs_previous_loop'] is True
            and pre['tau']['rule_if_chosen_later'] is None, 'tau block')
    cut = par['cutoff']
    m = match(r'^D in \{(\d+), (\d+)\}: D is the total polynomial degree', cut, 'cutoff set')
    v['cutoffs'] = [int(m.group(1)), int(m.group(2))]
    require(v['cutoffs'] == [6, 8], 'declared cutoffs')
    m = match(r'dimension C\(D\+3,3\): (\d+) at D=6, (\d+) at D=8', cut, 'dimensions')
    v['dims'] = {6: int(m.group(1)), 8: int(m.group(2))}
    m = match(r"the solver's tail_lower bound \((\d+) at D=6, (\d+) at D=8\)", cut, 'tail_lower values')
    v['tail_lower'] = {6: Q(int(m.group(1))), 8: Q(int(m.group(2)))}
    require('no per-link spin label j_max is well-posed for this basis' in cut, 'j_max caveat')
    require('D=6 is the primary cutoff and D=8 the certified refinement' in cut, 'primary/refinement roles')
    nd = par['normalization_dictionary']
    m = match(r'^tau_FG=tau/(\d+) \(every face coefficient nu=alpha\*tau/(\d+) in the Z\^3 model', nd, 'dictionary')
    v['dict_den'] = int(m.group(1))
    require(int(m.group(2)) == v['dict_den'], 'dictionary face coefficient')
    m = match(r'finite-graph first-order value (\d+)/(\d+) <-> (\d+)/(\d+); consistency only', nd, 'dictionary values')
    v['fg_first'] = Q(int(m.group(1)), int(m.group(2)))
    v['z3_first'] = Q(int(m.group(3)), int(m.group(4)))
    v['observable_param'] = par['observable']
    v['admission_param'] = par['admission']
    require('python-flint Arb as labelled cross-check only' in v['admission_param'], 'Arb is a labelled cross-check only')
    v['runtime_note'] = par['runtime_note']
    v['model_id'] = pre['model_id']
    require(v['model_id'] == 'FG(two-plaquette, D in {6,8}, tau_FG grid, I1.5, gauge-invariant)', 'model id')
    obs = pre['observable']
    v['observable_id'] = obs['id']
    v['centering'] = obs['centering']
    v['reference_value'] = obs['reference_value_exact']
    v['reference_route'] = obs['reference_route']
    require(v['centering'] == 'none' and v['reference_value'] == 'own free reference' and v['reference_route'] == 'own_finite_graph',
            'observable block')
    v['clock'] = pre['clock']
    m = match(r'^(s=alpha\*t_E/hbar, theta=alpha\*t/hbar); u=s/(\d+) and exponent (\d+) forbidden in packets$', v['clock'], 'clock')
    v['clock_common'], v['forbidden_u_div'], v['forbidden_exponent'] = m.group(1), int(m.group(2)), int(m.group(3))
    tg = pre['target']
    v['target'] = rat(tg['value'])
    v['target_quantity'] = tg['quantity']
    v['target_comparator'] = tg['comparator']
    require(v['target'] == 1 and v['target_comparator'] == '>=' and 'first-order coefficient enclosure contains 1/6' in v['target_quantity'],
            'target')
    v['error_terms'] = list(pre['error_terms_itemized'])
    require(v['error_terms'] == ['truncation_jmax', 'eigenvector_residual', 'arithmetic'], 'preregistered error terms')
    v['error_terms_rule'] = pre['error_terms_rule']
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    v['outcomes'] = list(pre['expected_outcome_types'])
    v['gate_fields'] = dict(pre['gate_fields_required'])
    require(v['gate_fields'] == {'transfers_to_aq': False, 'model_is_finite_graph': True, 'fg_coefficients_fitted': False}, 'gate fields')
    v['sentence'] = pre['mandatory_sentence_template']
    v['forbidden'] = list(pre['forbidden_phrasings'])
    require(v['forbidden'] == ['predicts', 'confirms the Z^3 value'], 'forbidden phrasings')
    v['controls'] = list(c['controls'])
    require(v['controls'] == list(pre['controls_required']['ids']) and len(v['controls']) == 20, 'controls list equals the preregistered ids')
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    v['acceptance'] = dict(c['acceptance'])
    v['shared'] = list(c['shared_premises'])
    v['required'] = list(c['required'])
    require(len(v['required']) == 6, 'six required items')
    v['hash_binding'] = dict(pre['hash_binding'])
    require(all(v['hash_binding'].get(k) is True for k in ('contract_sha256_in_producer_inputs', 'check_py_reads_target_and_reference_from_contract',
                                                          'check_py_sha256_recorded_before_full_size_evaluation')), 'hash binding')
    require(c['direction'] == 'single+skeptic' and pre['direction'] == 'single+skeptic' and c['producers'] == ['forward'], 'direction')
    require(c.get('single_direction_independent_replay') is True and c.get('reverse_premise_isolation') is False, 'replay/isolation flags')
    v['nodes'] = pre['nodes']
    require(pre['nodes']['s_values'] == [] and pre['nodes']['post_hoc_node_selection'] == 'forbidden', 'no Euclidean nodes (static loop)')
    v['state_provenance'] = pre['state_provenance']
    v['selected_after'] = c.get('selected_after')
    v['selection_reason'] = c.get('selection_reason', '')
    v['stop'] = c.get('stop', '')
    v['selected_triple'] = pre['selected_triple_alpha_units']
    return v


# ---------------------------------------------------------------------------
# Exact invariant algebra of two adjacent SU(2) plaquettes (Round11 conventions, re-implemented in Fractions).
# Coordinates x=Tr(U)/2, y=Tr(V)/2, z=Tr(UV)/2 with U=vM h3^-1 vL^-1 h1, V=h2 vR h4^-1 vM^-1 (Round11 G2).
# ---------------------------------------------------------------------------
ZERO3 = (0, 0, 0)
EX, EY, EZ = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def basis(d):
    """Round11 `basis(d)`: monomials x^a y^b z^c of total degree <= d, ordered by degree, then a, then b."""
    return [(a, b, n - a - b) for n in range(d + 1) for a in range(n + 1) for b in range(n - a + 1)]


def parity_class(m):
    a, b, c = m
    return ((a + c) % 2, (b + c) % 2)


@lru_cache(None)
def haar_x_power(n):
    """E[x^n] for a scalar coordinate of normalized Haar S^3 (Catalan(n/2)/4^(n/2))."""
    if n % 2:
        return Q(0)
    m = n // 2
    return Q(comb(2 * m, m), 4 ** m * (m + 1))


@lru_cache(None)
def radial_moment(n, k):
    return sum(((-1) ** j * comb(k, j) * haar_x_power(n + 2 * j) for j in range(k + 1)), Q(0))


@lru_cache(None)
def moment(a, b, c):
    """Haar E[x^a y^b z^c] (Round11 advisor Q4)."""
    require(min(a, b, c) >= 0, 'negative exponent')
    return sum((Q(comb(c, 2 * k), 2 * k + 1) * radial_moment(a + c - 2 * k, k) * radial_moment(b + c - 2 * k, k)
                for k in range(c // 2 + 1)), Q(0))


def padd(p, q, scale=1):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, 0) + scale * v
    return {k: Q(v) for k, v in out.items() if v}


def pscale(p, c):
    return {k: c * v for k, v in p.items() if c * v}


def pmul(p, q):
    out = {}
    for (a, b, c), u in p.items():
        for (d, e, f), w in q.items():
            k = (a + d, b + e, c + f)
            out[k] = out.get(k, 0) + u * w
    return {k: v for k, v in out.items() if v}


def pshift(p, e):
    return {(k[0] + e[0], k[1] + e[1], k[2] + e[2]): v for k, v in p.items()}


def pdeg(p):
    return max((sum(k) for k in p), default=0)


def inner(p, q):
    """Physical L^2 inner product <p,q> (real polynomials, normalized Haar measure on the quotient)."""
    tot = Q(0)
    for (a, b, c), u in p.items():
        for (d, e, f), w in q.items():
            mm = moment(a + d, b + e, c + f)
            if mm:
                tot += u * w * mm
    return tot


def proj_coeffs(bs, p):
    """c_i = <m_i, p> for the monomials of a basis."""
    out = []
    for (a, b, c) in bs:
        tot = Q(0)
        for (d, e, f), w in p.items():
            mm = moment(a + d, b + e, c + f)
            if mm:
                tot += w * mm
        out.append(tot)
    return out


def dot(u, w):
    return sum((a * b for a, b in zip(u, w) if a and b), Q(0))


def casimir_terms(m, which):
    """One-group Casimirs in quotient coordinates (Round11 K3/K4 decomposition K = 3 C_U + 3 C_V + S).
    C_U acts on (x,z), C_V on (y,z), S (shared link vM, derivative L_U - R_V) on (x,y)."""
    a, b, c = m
    out = {}

    def add(k, val):
        out[k] = out.get(k, 0) + val
    if which == 'U':
        p1, p2, coef_mixed, target = a, c, 2 * a * c, (a - 1, b + 1, c - 1)
        add(m, Q(3, 4) * (a + c))
        if a >= 2:
            add((a - 2, b, c), -Q(a * (a - 1), 4)); add(m, Q(a * (a - 1), 4))
        if c >= 2:
            add((a, b, c - 2), -Q(c * (c - 1), 4)); add(m, Q(c * (c - 1), 4))
    elif which == 'V':
        p1, p2, coef_mixed, target = b, c, 2 * b * c, (a + 1, b - 1, c - 1)
        add(m, Q(3, 4) * (b + c))
        if b >= 2:
            add((a, b - 2, c), -Q(b * (b - 1), 4)); add(m, Q(b * (b - 1), 4))
        if c >= 2:
            add((a, b, c - 2), -Q(c * (c - 1), 4)); add(m, Q(c * (c - 1), 4))
    elif which == 'S':
        p1, p2, coef_mixed, target = a, b, 2 * a * b, (a - 1, b - 1, c + 1)
        add(m, Q(3, 4) * (a + b))
        if a >= 2:
            add((a - 2, b, c), -Q(a * (a - 1), 4)); add(m, Q(a * (a - 1), 4))
        if b >= 2:
            add((a, b - 2, c), -Q(b * (b - 1), 4)); add(m, Q(b * (b - 1), 4))
    else:
        raise AdmissionError('unknown Casimir ' + which)
    if p1 >= 1 and p2 >= 1:
        add(target, -Q(coef_mixed, 4)); add(m, Q(coef_mixed, 4))
    return {k: v for k, v in out.items() if v}


KINETIC_MODELS = {
    'R11_rho1': (3, 3, 1),            # the seven-link sum: 3 C_U + 3 C_V + C_shared (Round11 K1, rho=1)
    'shared_casimir_dropped': (3, 3, 0),
    'anisotropic_rho2': (3, 3, 2),
    'independent_rotor': (4, 4, 0),   # 4(C_U + C_V): the shared-link cross term 2 L_U.R_V dropped
}


def kinetic(p, model='R11_rho1'):
    cU, cV, cS = KINETIC_MODELS[model]
    out = {}
    for m, v in p.items():
        for coef, which in ((cU, 'U'), (cV, 'V'), (cS, 'S')):
            if coef:
                for k, w in casimir_terms(m, which).items():
                    out[k] = out.get(k, 0) + coef * v * w
    return {k: v for k, v in out.items() if v}


def eps_free(a, b, c):
    """Round11 E2: 3j(j+1)+3k(k+1)+ell(ell+1), j=(a+c)/2, k=(b+c)/2, ell=(a+b)/2."""
    j, k, l = Q(a + c, 2), Q(b + c, 2), Q(a + b, 2)
    return 3 * j * (j + 1) + 3 * k * (k + 1) + l * (l + 1)


def shell_min(d):
    """Round11 E3: exact minimum free energy in the orthogonal shell of degree d."""
    return Q(5, 8) * d * d + 2 * d + Q(3, 8) * (d % 2)


# ---------------------------------------------------------------------------
# Exact Gram projections: the monomial Gram matrix is block diagonal in the four link-flip parity classes.
# ---------------------------------------------------------------------------
def ldl_exact(M):
    """Exact LDL^T of a symmetric positive definite Fraction matrix (every pivot must be positive)."""
    n = len(M)
    A = [list(r) for r in M]
    L = [[Q(0)] * n for _ in range(n)]
    d = [Q(0)] * n
    for k in range(n):
        d[k] = A[k][k]
        require(d[k] > 0, 'Gram pivot not positive')
        L[k][k] = Q(1)
        for i in range(k + 1, n):
            L[i][k] = A[i][k] / d[k]
        for i in range(k + 1, n):
            lik = L[i][k]
            if lik:
                f = lik * d[k]
                for j in range(k + 1, i + 1):
                    if L[j][k]:
                        A[i][j] -= f * L[j][k]
    return L, d


class GramSolver:
    """Exact solver for G z = c on span(basis), G_ij = <m_i, m_j>; verifies the parity-block structure."""

    def __init__(self, bs):
        self.bs = bs
        classes = {}
        for i, m in enumerate(bs):
            classes.setdefault(parity_class(m), []).append(i)
        self.blocks = [classes[k] for k in sorted(classes)]
        # the Gram matrix couples only equal parity classes (link-flip Haar symmetry); verified entrywise
        off = 0
        for i, p in enumerate(bs):
            for j, q in enumerate(bs):
                if parity_class(p) != parity_class(q) and moment(p[0] + q[0], p[1] + q[1], p[2] + q[2]):
                    off += 1
        require(off == 0, 'Gram matrix is not block diagonal in the parity classes')
        self.fac = []
        for idx in self.blocks:
            M = [[moment(bs[i][0] + bs[j][0], bs[i][1] + bs[j][1], bs[i][2] + bs[j][2]) for j in idx] for i in idx]
            self.fac.append(ldl_exact(M))

    def solve(self, c):
        x = [Q(0)] * len(c)
        for idx, (L, d) in zip(self.blocks, self.fac):
            y = [c[i] for i in idx]
            n = len(y)
            for i in range(n):
                acc = y[i]
                for j in range(i):
                    if L[i][j] and y[j]:
                        acc -= L[i][j] * y[j]
                y[i] = acc
            y = [y[i] / d[i] for i in range(n)]
            for i in range(n - 1, -1, -1):
                acc = y[i]
                for j in range(i + 1, n):
                    if L[j][i] and y[j]:
                        acc -= L[j][i] * y[j]
                y[i] = acc
            for k, i in enumerate(idx):
                x[i] = y[k]
        return x

    def poly(self, z):
        return {m: v for m, v in zip(self.bs, z) if v}


class Shell:
    """The orthogonal shell of degree d relative to P_{d-1}: the vectors Q_{d-1} m_s (a+b+c=d) must be exactly
    mutually orthogonal (one spin-network sector per monomial); verified by an exactly diagonal Schur complement."""

    def __init__(self, d, gs_below):
        self.d = d
        self.gs = gs_below
        self.sectors = [m for m in basis(d) if sum(m) == d]
        bsb = gs_below.bs
        self.B = [[moment(p[0] + t[0], p[1] + t[1], p[2] + t[2]) for p in bsb] for t in self.sectors]
        self.Y = [gs_below.solve(col) for col in self.B]
        self.sigma = []
        for i, t in enumerate(self.sectors):
            self.sigma.append(moment(2 * t[0], 2 * t[1], 2 * t[2]) - dot(self.B[i], self.Y[i]))
        require(all(x > 0 for x in self.sigma), 'shell sector norm not positive')
        self.offdiag_nonzero = 0
        self.pairs_checked = 0
        for i in range(len(self.sectors)):
            for j in range(i + 1, len(self.sectors)):
                ti, tj = self.sectors[i], self.sectors[j]
                val = moment(ti[0] + tj[0], ti[1] + tj[1], ti[2] + tj[2]) - dot(self.B[i], self.Y[j])
                self.pairs_checked += 1
                if val:
                    self.offdiag_nonzero += 1
        require(self.offdiag_nonzero == 0, 'shell sectors are not mutually orthogonal')

    def components(self, p, c_below):
        """<Q_{d-1} m_s, p> for every sector, given c_below = <m_i, p> on P_{d-1}."""
        out = []
        for i, t in enumerate(self.sectors):
            tot = Q(0)
            for (a, b, c), w in p.items():
                mm = moment(a + t[0], b + t[1], c + t[2])
                if mm:
                    tot += w * mm
            out.append(tot - dot(self.Y[i], c_below))
        return out

    def weights(self, p, c_below):
        return [g * g / sg for g, sg in zip(self.components(p, c_below), self.sigma)]


def sector_class(t, D):
    """Spin labels of a shell sector (a,b,c): j=(a+c)/2 on h1,vL,h3; k=(b+c)/2 on h2,vR,h4; ell=(a+b)/2 on vM.
    Returns the set of link classes whose spin exceeds the per-link retained maximum D/2."""
    a, b, c = t
    out = set()
    if a + c > D:
        out.add('j')
    if b + c > D:
        out.add('k')
    if a + b > D:
        out.add('ell')
    return out


def boundary_class(t, D):
    """Shell-D sectors whose link spin equals the retained maximum D/2 (the per-link boundary layer)."""
    a, b, c = t
    out = set()
    if a + c == D:
        out.add('j')
    if b + c == D:
        out.add('k')
    if a + b == D:
        out.add('ell')
    return out


# ---------------------------------------------------------------------------
# Energy thresholds of the omitted space (Round11 E2/E3), per link class and for the joint product channel.
# ---------------------------------------------------------------------------
def thresholds(D):
    """Exact minima of the free electric energy over omitted sectors (total degree >= D+1), by class.
    Enumeration stops once the shell minimum m_d (E3, increasing in d) exceeds every current class minimum."""
    preds = {
        'all': lambda a, b, c: True,
        'j': lambda a, b, c: a + c > D,
        'k': lambda a, b, c: b + c > D,
        'ell': lambda a, b, c: a + b > D,
        'product': lambda a, b, c: a + c <= D and b + c <= D and a + b <= D,
    }
    best = {k: None for k in preds}
    d = D + 1
    shells_checked = []
    while True:
        shell = [(a, b, d - a - b) for a in range(d + 1) for b in range(d - a + 1)]
        smin = min(eps_free(*t) for t in shell)
        require(smin == shell_min(d), 'E3 shell minimum formula fails at degree %d' % d)
        shells_checked.append(d)
        for key, pred in preds.items():
            for t in shell:
                if pred(*t):
                    e = eps_free(*t)
                    if best[key] is None or e < best[key][0]:
                        best[key] = (e, t)
        if all(best[k] is not None for k in best) and shell_min(d + 1) > max(best[k][0] for k in best):
            break
        d += 1
        require(d <= 6 * (D + 1), 'threshold enumeration did not terminate')
    return best, shells_checked


# ---------------------------------------------------------------------------
# Decimal Ritz proposal (a proposal only: its output is rounded to an exact integer vector and certified exactly).
# ---------------------------------------------------------------------------
DCTX = decimal.Context(prec=110, rounding=decimal.ROUND_HALF_EVEN)
RITZ_ITERATIONS = 40
RITZ_SCALE = 10 ** 100


def to_dec(x):
    x = Q(x)
    return DCTX.divide(decimal.Decimal(x.numerator), decimal.Decimal(x.denominator))


class RitzProposal:
    """Inverse iteration (A - sigma G) w = G v in 110-digit decimal arithmetic on P_D; sigma = -tau^2/6 - 1/1000."""

    def __init__(self, D):
        bs = basis(D)
        self.bs = bs
        n = len(bs)
        kp = [kinetic({q: Q(1)}) for q in bs]
        self.G = [[to_dec(moment(p[0] + q[0], p[1] + q[1], p[2] + q[2])) for q in bs] for p in bs]
        self.AK = [[to_dec(sum((v * moment(p[0] + k[0], p[1] + k[1], p[2] + k[2]) for k, v in kp[j].items()), Q(0)))
                    for j in range(n)] for p in bs]
        self.MV = [[to_dec(moment(p[0] + q[0] + 1, p[1] + q[1], p[2] + q[2]) + moment(p[0] + q[0], p[1] + q[1] + 1, p[2] + q[2]))
                    for q in bs] for p in bs]

    def vector(self, tau):
        n = len(self.bs)
        taud = to_dec(tau)
        sigma = to_dec(-tau * tau / 6 - Q(1, 1000))
        M = [[DCTX.subtract(DCTX.subtract(self.AK[i][j], DCTX.multiply(taud, self.MV[i][j])), DCTX.multiply(sigma, self.G[i][j]))
              for j in range(n)] for i in range(n)]
        L = [[decimal.Decimal(0)] * n for _ in range(n)]
        dg = [decimal.Decimal(0)] * n
        for k in range(n):
            acc = M[k][k]
            for j in range(k):
                acc = DCTX.subtract(acc, DCTX.multiply(DCTX.multiply(L[k][j], L[k][j]), dg[j]))
            dg[k] = acc
            require(acc > 0, 'decimal proposal: shifted matrix not positive definite')
            for i in range(k + 1, n):
                t = M[i][k]
                for j in range(k):
                    t = DCTX.subtract(t, DCTX.multiply(DCTX.multiply(L[i][j], L[k][j]), dg[j]))
                L[i][k] = DCTX.divide(t, acc)
        v = [decimal.Decimal(0)] * n
        v[0] = decimal.Decimal(1)
        for _ in range(RITZ_ITERATIONS):
            y = []
            for row in self.G:
                acc = decimal.Decimal(0)
                for a, b in zip(row, v):
                    if b:
                        acc = DCTX.add(acc, DCTX.multiply(a, b))
                y.append(acc)
            for i in range(n):
                acc = y[i]
                for j in range(i):
                    acc = DCTX.subtract(acc, DCTX.multiply(L[i][j], y[j]))
                y[i] = acc
            y = [DCTX.divide(y[i], dg[i]) for i in range(n)]
            for i in range(n - 1, -1, -1):
                acc = y[i]
                for j in range(i + 1, n):
                    acc = DCTX.subtract(acc, DCTX.multiply(L[j][i], y[j]))
                y[i] = acc
            v = [DCTX.divide(x, y[0]) for x in y]
        return [round(Q(x) * RITZ_SCALE) for x in v]


# ---------------------------------------------------------------------------
# Exact certificate at one (D, tau):  complete residual, itemized ledger, energy and Wilson enclosures, tails.
# ---------------------------------------------------------------------------
WEYL_FREE_GAP = Q(3)      # E_1(K) = m_1 = 3 (Round11 E3; span{x,y})
V_NORM_PER_TAU = Q(2)     # ||W_1 + W_2|| <= 2
EXPORT_DIGITS = 45        # outward rounding of exported enclosure ends to denominator 10^45


class PerCutoff:
    def __init__(self, D, tail_lower_contract):
        self.D = D
        self.bs = basis(D)
        self.gs = GramSolver(self.bs)
        self.gs_below = GramSolver(basis(D - 1))
        self.shell_next = Shell(D + 1, self.gs)          # first omitted shell (the complete leakage lives here)
        self.shell_top = Shell(D, self.gs_below)         # top retained shell (per-link boundary layers)
        self.proposal = RitzProposal(D)
        self.thr, self.thr_shells = thresholds(D)
        self.tail_lower = self.thr['all'][0]
        require(self.tail_lower == shell_min(D + 1) == tail_lower_contract, 'tail_lower differs from E3 or the contract')


def certify(pc, tau, vector=None):
    """Exact certificate for H_FG = K - tau (W_1 + W_2) on the physical space at cutoff pc.D."""
    D, bs, gs = pc.D, pc.bs, pc.gs
    tau = rat(tau)
    w = pc.proposal.vector(tau) if vector is None else vector
    vp = {m: Q(c) for m, c in zip(bs, w) if c}
    require(vp and pdeg(vp) <= D, 'Ritz vector outside P_D')
    N = inner(vp, vp)
    Kv = kinetic(vp)
    xv, yv = pshift(vp, EX), pshift(vp, EY)
    t = padd(xv, yv)
    Hv = padd(Kv, t, -tau)
    mu = inner(vp, Hv) / N
    rho2 = inner(Hv, Hv) / N - mu * mu
    wR = inner(vp, xv) / N
    wR_y = inner(vp, yv) / N
    w2R = inner(xv, xv) / N
    # retained (P_D) and omitted (Q_D) parts of the complete residual (H - mu) v
    r = padd(Hv, vp, -mu)
    cr = proj_coeffs(bs, r)
    rP2 = dot(cr, gs.solve(cr)) / N
    cx, cy = proj_coeffs(bs, xv), proj_coeffs(bs, yv)
    zx, zy = gs.solve(cx), gs.solve(cy)
    QX = (inner(xv, xv) - dot(cx, zx)) / N
    QY = (inner(yv, yv) - dot(cy, zy)) / N
    QXY = (inner(xv, yv) - dot(cx, zy)) / N
    ct = [a + b for a, b in zip(cx, cy)]
    zt = [a + b for a, b in zip(zx, zy)]
    PQ = inner(t, t) / N - dot(ct, zt) / N
    rhoQ2 = tau * tau * PQ
    sec_w = [x / N for x in pc.shell_next.weights(t, ct)]
    sec_x = [x / N for x in pc.shell_next.weights(xv, cx)]
    sec_y = [x / N for x in pc.shell_next.weights(yv, cy)]
    # per-link boundary layer of the Ritz vector (top retained shell, link spin exactly D/2)
    cvb = proj_coeffs(pc.gs_below.bs, vp)
    top_w = [x / N for x in pc.shell_top.weights(vp, cvb)]
    # certified gap (Weyl: E_1(H) >= E_1(K) - ||V||) and Temple / Davis-Kahan (complete residual)
    b = WEYL_FREE_GAP - V_NORM_PER_TAU * abs(tau)
    rho_lo, rho_up = sqrt_bracket(rho2)
    ok = mu < b
    E0_temple = mu - rho2 / (b - mu) if ok else None
    s_A = rho_up / (b - mu) if ok else None
    # Round11 tail comparison (T1-T5) with the solver's tail bound: H >= B (+) R Q_D, B = A - C C*/(tau_t - R)
    tail_t = pc.tail_lower - V_NORM_PER_TAU * abs(tau)
    R = b
    require(R < tail_t, 'comparison threshold must lie below the tail threshold')
    beta0 = mu - rhoQ2 / (tail_t - R)
    Pt = gs.poly(zt)
    Qt = padd(t, Pt, -1)
    VQt = pmul({EX: Q(1), EY: Q(1)}, Qt)
    cc = proj_coeffs(bs, VQt)
    CCv = pscale(gs.poly(gs.solve(cc)), tau * tau)             # C C* v = P_D V Q_D V v  (unnormalized)
    rPpoly = padd(padd(Kv, vp, -mu), Pt, -tau)                 # P_D (H - mu) v
    resid = padd(rPpoly, padd(CCv, vp, -rhoQ2), -1 / (tail_t - R))
    eta2 = inner(resid, resid) / N
    bB = b - V_NORM_PER_TAU ** 2 * tau * tau / (tail_t - R)    # lambda_1(B) >= lambda_1(A) - ||CC*||/(tau_t - R)
    ok = ok and beta0 < bB
    E0_r11 = beta0 - eta2 / (bB - beta0) if ok else None
    res = {'D': D, 'tau': tau, 'w': w, 'N': N, 'mu': mu, 'rho2': rho2, 'rhoP2': rP2, 'rhoQ2': rhoQ2, 'PQ': PQ,
           'QX': QX, 'QY': QY, 'QXY': QXY, 'wR': wR, 'wR_y': wR_y, 'w2R': w2R, 'sec_w': sec_w, 'sec_x': sec_x, 'sec_y': sec_y,
           'top_w': top_w, 'gap_lower_b': b, 'residual_argument_ok': ok, 'tail_t': tail_t, 'R': R, 'beta0': beta0, 'eta2': eta2,
           'bB': bB, 'rho_bracket': (rho_lo, rho_up)}
    if not ok:
        return res
    E0_low = max(E0_temple, E0_r11)
    sB2 = (mu - E0_low) / (b - mu)
    s_B = sqrt_up(sB2)
    s_used = min(s_A, s_B)
    require(s_used < 1, 'angle bound must be below one')
    delta = 2 * s_used + 2 * s_used * s_used          # |<v,Wv> - <psi0,W psi0>| <= 2 s sigma_W + 2 s^2, sigma_W <= ||W|| <= 1
    lo, hi = wR - delta, wR + delta
    # certified tails of the TRUE ground state (Lemma C and its per-link form), using the tail threshold
    rhoQ_up = sqrt_up(rhoQ2)
    T_joint = (rhoQ_up + V_NORM_PER_TAU * abs(tau) * s_used) / (tail_t - mu)
    T_link = {}
    for cls, cfac in (('j', 1), ('k', 1), ('ell', 2)):
        lam2 = sum((wt for tt, wt in zip(pc.shell_top.sectors, top_w) if cls in boundary_class(tt, D)), Q(0))
        lam_up = sqrt_up(lam2)
        t_e = pc.thr[cls][0]
        T_link[cls] = {'boundary_layer_weight': lam2, 'threshold': t_e,
                       'bound': cfac * abs(tau) * (lam_up + s_used) / (t_e - V_NORM_PER_TAU * abs(tau) - mu), 'faces_touching': cfac}
    # arithmetic: directed square-root widths and the outward export rounding
    lo_out, hi_out = out_dn(lo, EXPORT_DIGITS), out_up(hi, EXPORT_DIGITS)
    E0_lo_out, E0_hi_out = out_dn(E0_low, EXPORT_DIGITS), out_up(mu, EXPORT_DIGITS)
    res.update({'E0_temple': E0_temple, 'E0_r11': E0_r11, 'E0_low': E0_low, 's_A': s_A, 's_B': s_B, 's_used': s_used,
                'delta': delta, 'lo': lo, 'hi': hi, 'lo_out': lo_out, 'hi_out': hi_out, 'E0_lo_out': E0_lo_out, 'E0_hi_out': E0_hi_out,
                'T_joint': T_joint, 'T_link': T_link, 'rhoQ_up': rhoQ_up,
                'arith_sqrt_width': rho_up - rho_lo, 'arith_export_width': (lo - lo_out) + (hi_out - hi)})
    return res


def classify_leakage(cert, pc):
    """Per-link, product-channel and corner weights of the complete omitted residual (exact, normalized)."""
    tau2 = cert['tau'] ** 2
    per = {'j': Q(0), 'k': Q(0), 'ell': Q(0)}
    prod = Q(0)
    corners = {}
    for t, wt in zip(pc.shell_next.sectors, cert['sec_w']):
        cls = sector_class(t, pc.D)
        for c in cls:
            per[c] += tau2 * wt
        if not cls:
            prod += tau2 * wt
        if len(cls) == 2:
            corners['+'.join(sorted(cls))] = tau2 * wt
        require(len(cls) <= 2, 'a shell sector cannot exceed the per-link maximum on all three link classes')
    return per, prod, corners


# ---------------------------------------------------------------------------
# Exact Rayleigh-Schroedinger series about the free ground state (full space: every psi_n lies in P_n).
# ---------------------------------------------------------------------------
def haar_mean(p):
    return sum((v * moment(*k) for k, v in p.items()), Q(0))


def solve_kinetic(f, D, model='R11_rho1'):
    """Solve K p = f with E[p] = 0 inside P_D by degree back-substitution (K is triangular in degree with diagonal
    eps_free on the monomial quotient).  Requires E[f] = 0.  The returned p satisfies K p = f EXACTLY as
    polynomials, i.e. the full-space resolvent equation, with zero omitted-space residual."""
    require(pdeg(f) <= D, 'right-hand side leaves P_D')
    rem = dict(f)
    p = {}
    for d in range(pdeg(f), 0, -1):
        top = {k: v for k, v in rem.items() if sum(k) == d}
        step = {k: v / eps_free(*k) for k, v in top.items()}
        p = padd(p, step)
        rem = padd(rem, kinetic(step, model), -1)
        require(all(sum(k) < d for k in rem), 'kinetic operator not triangular in degree')
    require(set(rem) <= {ZERO3} and rem.get(ZERO3, 0) == 0, 'solvability: E[f] must vanish')
    p = padd(p, {ZERO3: haar_mean(p)}, -1)
    require(padd(kinetic(p, model), f, -1) == {}, 'full-space resolvent equation K p = f not exact')
    require(haar_mean(p) == 0, 'intermediate normalization')
    return p


def rs_series(order, D, faces=((1, 0, 0), (0, 1, 0)), sign=-1, model='R11_rho1'):
    """H(tau) = K + tau V, V = sign * sum of the face traces; returns psi_n (intermediate normalization) and E^(n)."""
    V = {f: Q(sign) for f in faces}
    psi = [{ZERO3: Q(1)}]
    En = [Q(0)]
    for n in range(1, order + 1):
        Vpsi = pmul(V, psi[n - 1])
        En.append(haar_mean(Vpsi))
        rhs = pscale(Vpsi, Q(-1))
        for k in range(1, n + 1):
            rhs = padd(rhs, psi[n - k], En[k])
        psi.append(solve_kinetic(rhs, D, model))
        require(pdeg(psi[n]) <= n <= D, 'psi_n must lie in P_n inside P_D')
    return psi, En


def observable_series(psi, O, order):
    A = [sum((inner(psi[i], pmul(O, psi[n - i])) for i in range(n + 1)), Q(0)) for n in range(order + 1)]
    Nn = [sum((inner(psi[i], psi[n - i]) for i in range(n + 1)), Q(0)) for n in range(order + 1)]
    out = []
    for n in range(order + 1):
        out.append((A[n] - sum((out[k] * Nn[n - k] for k in range(n)), Q(0))) / Nn[0])
    return out


# ---------------------------------------------------------------------------
# Exact SU(2) fixtures: rational unit quaternions for the seven links and the six vertex gauge transformations.
# ---------------------------------------------------------------------------
def qmul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def qinv(p):
    return (p[0], -p[1], -p[2], -p[3])


def rational_unit_quaternions(count):
    out = []
    for n in range(2, 40):
        for a in range(-n, n + 1):
            for b in range(0, n + 1):
                for c in range(0, n + 1):
                    r = n * n - a * a - b * b - c * c
                    if r < 0:
                        continue
                    d = isqrt(r)
                    if d * d == r and (b, c, d) != (0, 0, 0) and a != 0:
                        out.append((Q(a, n), Q(b, n), Q(c, n), Q(d, n)))
                        if len(out) >= count:
                            return out
    raise AdmissionError('not enough rational unit quaternions')


def holonomies(links):
    U = qmul(qmul(qmul(links['vM'], qinv(links['h3'])), qinv(links['vL'])), links['h1'])
    V = qmul(qmul(qmul(links['h2'], links['vR']), qinv(links['h4'])), qinv(links['vM']))
    return U, V


def invariants(links):
    U, V = holonomies(links)
    return (U[0], V[0], qmul(U, V)[0])     # x = Tr(U)/2, y = Tr(V)/2, z = Tr(UV)/2 (real parts of unit quaternions)


def gauge(links, g):
    return {e: qmul(qmul(g[ORIENT[e][0]], links[e]), qinv(g[ORIENT[e][1]])) for e in LINKS}


def sig_pair(q, sig=30):
    """Outward bracket of a signed rational with about `sig` significant digits (export only)."""
    q = Q(q)
    if q == 0:
        return Q(0), Q(0)
    k = sig - 1 - magnitude(q)
    return out_dn(q, k), out_up(q, k)


def forward_verdict(all_d6, all_d8, product_itemized, first_order_consistent, labels_present, residual_ok, overclaim):
    """Contract acceptance: insufficient if the residual argument fails or an excluded claim is made; limited if the
    tail is certified only at D=6 or the joint product channel is not itemized; otherwise accepted_within_scope."""
    if overclaim or not residual_ok:
        return 'insufficient'
    if not all_d6:
        return 'insufficient'
    if not all_d8 or not product_itemized:
        return 'limited'
    if not (first_order_consistent and labels_present):
        return 'limited'
    return 'accepted_within_scope'


def point_key(D, tau):
    sign = '+' if tau > 0 else ('-' if tau < 0 else '')
    return 'D%d_tau%s%s' % (D, sign, s(abs(tau)))


# ---------------------------------------------------------------------------
def compute(check_sha):
    c, contract_digest = load_contract()          # sha256 verified before any evaluation
    V = contract_values(c)
    check('contract_snapshot_sha256',
          contract_digest == CONTRACT_SHA256 and len(V['controls']) == 20 and V['target'] == 1,
          contract_sha256=contract_digest, contract_path=CONTRACT_REL, check_py_sha256_recorded_before_evaluation=check_sha,
          grid_read_from_contract=[s(x) for x in V['grid']], signs=V['signs'], cutoffs_read_from_contract=V['cutoffs'],
          dimensions_read_from_contract={str(k): v for k, v in V['dims'].items()},
          tail_lower_read_from_contract={str(k): s(v) for k, v in V['tail_lower'].items()},
          dictionary_read_from_contract='tau_FG=tau/%d; %s <-> %s' % (V['dict_den'], s(V['fg_first']), s(V['z3_first'])),
          reference_read_from_contract=V['reference_value'] + ' via ' + V['reference_route'], target_read_from_contract=s(V['target']),
          target_quantity=V['target_quantity'], hash_binding=V['hash_binding'])

    # ======================= premise inventory =======================
    expected_inputs = ['AGENTS.md', CONTRACT_REL] + V['shared']
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    check('premise_inventory_bound',
          sorted(inventory) == sorted(set(expected_inputs)) and len(inventory) == 28
          and not any('__pycache__' in k or k.endswith('.pyc') for k in inventory)
          and not any(k.startswith('research/round32/skeptic/') or k.startswith('research/round32/forward/az1') for k in inventory),
          inventory_files=len(inventory), inputs_sha256=inventory,
          isolation='inputs equal AGENTS.md + the AZ2 contract + its 26 shared premises; no current skeptic, AZ1, deliberation or panel file')

    # ======================= Round11 conventions, bound to the snapshot text =======================
    solver = read_input(P_R11_SOLVER)
    sreadme = read_input(P_R11_SOLVER_README)
    adv = read_input(P_R11_ADV)
    r11 = read_input(P_R11_README)
    solver_strings = [
        'return [(a,b,n-a-b) for n in range(d+1) for a in range(n+1) for b in range(n-a+1)]',
        'return sum((F(comb(c,2*k),2*k+1)*radial_moment(a+c-2*k,k)*radial_moment(b+c-2*k,k) for k in range(c//2+1)),F(0))',
        'return F(comb(2*m,m),4**m*(m+1))',
        "(3*(3+r)/4 if i<2 else F(9,2))", "(-(3+r)/4 if i<2 else F(-3,2))",
        'out=add(out,mul(add(Z,mul(X,Y),-1),deriv(deriv(p,0),1)),-r/2)',
        'out=add(out,mul(add(Y,mul(X,Z),-1),deriv(deriv(p,0),2)),F(-3,2))',
        'out=add(out,mul(add(X,mul(Y,Z),-1),deriv(deriv(p,1),2)),F(-3,2))',
        'return 3*j*(j+1)+3*s*(s+1)+r*ell*(ell+1)',
        'if r==1: return a*(F(5,8)*d*d+2*d+F(3,8)*(d%2))',
        '# W=-lambda1*x-lambda2*y. Constants have no P-Q coupling.',
        'import numpy as np', 'from scipy.linalg import eigh',
    ]
    missing = [x for x in solver_strings if x not in solver]
    require(not missing, 'Round11 solver snapshot lacks: ' + repr(missing[:2]))
    require('E[x²]=E[y²]=E[z²]=1/4 and E[xyz]=1/16' in sreadme and 'For ρ=1 this gives Kx=3x, Ky=3y, Kz=9z/2 and K(xy)=13xy/2−z/2' in sreadme
            and '`H = α Kρ + λ1(1−x) + λ2(1−y)`' in sreadme and "`τ/α = 5d²/8 + 2d + 3(d mod 2)/8`" in sreadme, 'Round11 solver README fixtures')
    require('K1=0,\\quad Kx=3x,\\quad Ky=3y,\\quad Kz=\\tfrac92z,' in adv and 'K(xy)=\\tfrac{13}2xy-\\tfrac12z.' in adv
            and 'm_d=\\tfrac58d^2+2d+\\tfrac38(d\\bmod2),\\qquad d\\ge0.' in adv and 'Q_D K Q_D\\ge m_{D+1}Q_D,' in adv
            and '\\mu_k(B)\\le E_k(H)\\le\\mu_k(A),\\quad k=0,1.' in adv and 'B=A-\\frac{CC^*}{\\tau-R}.' in adv
            and '\\epsilon_{abc}=3j(j+1)+3k(k+1)+\\ell(\\ell+1),' in adv, 'Round11 advisor equations K5, E2, E3, E4, T4, T5')
    require('U=v_Mh_3^{-1}v_L^{-1}h_1,' in adv and 'V=h_2v_Rh_4^{-1}v_M^{-1}.' in adv, 'Round11 loop paths G2')
    require('The physical Hilbert space is L² of' in sreadme and 'For rho=1, alpha>0 and finite lambda1,lambda2>=0' in r11, 'Round11 scope')
    X1, Y1, Z1 = {EX: Q(1)}, {EY: Q(1)}, {EZ: Q(1)}
    k5 = {'K1': kinetic({ZERO3: Q(1)}), 'Kx': kinetic(X1), 'Ky': kinetic(Y1), 'Kz': kinetic(Z1), 'Kxy': kinetic({(1, 1, 0): Q(1)})}

    def validate_k5(model):
        require(kinetic({ZERO3: Q(1)}, model) == {}, 'K1=0')
        require(kinetic(X1, model) == {EX: Q(3)} and kinetic(Y1, model) == {EY: Q(3)}, 'Kx=3x, Ky=3y (seven links, shared Casimir included)')
        require(kinetic(Z1, model) == {EZ: Q(9, 2)}, 'Kz=9z/2')
        require(kinetic({(1, 1, 0): Q(1)}, model) == {(1, 1, 0): Q(13, 2), EZ: Q(-1, 2)}, 'K(xy)=13xy/2-z/2 (shared-link cross term)')
        return True
    fixtures = {'E[x^2]': moment(2, 0, 0), 'E[y^2]': moment(0, 2, 0), 'E[z^2]': moment(0, 0, 2), 'E[xyz]': moment(1, 1, 1), 'E[x^2y^2]': moment(2, 2, 0),
                'E[x]': moment(1, 0, 0), 'E[1]': moment(0, 0, 0)}
    diag_ok = all(kinetic({m: Q(1)}).get(m, Q(0)) == eps_free(*m) and all(sum(k) < sum(m) for k in kinetic({m: Q(1)}) if k != m)
                  for m in basis(9))
    b4 = basis(4)
    sym_ok = all(inner({p: Q(1)}, kinetic({q: Q(1)})) == inner(kinetic({p: Q(1)}), {q: Q(1)}) for p in b4 for q in b4)
    parity_ok = all(moment(a, b, cc) == 0 for (a, b, cc) in basis(12) if (a + cc) % 2 or (b + cc) % 2)
    check('round11_conventions_bound',
          validate_k5('R11_rho1') and diag_ok and sym_ok and parity_ok
          and fixtures['E[x^2]'] == fixtures['E[y^2]'] == fixtures['E[z^2]'] == Q(1, 4) and fixtures['E[xyz]'] == Q(1, 16)
          and fixtures['E[x^2y^2]'] == Q(1, 16) and fixtures['E[x]'] == 0 and fixtures['E[1]'] == 1
          and all(comb(D + 3, 3) == len(basis(D)) == V['dims'][D] for D in V['cutoffs'])
          and WEYL_FREE_GAP == shell_min(1) == min(eps_free(*m) for m in basis(1) if sum(m) == 1)
          and V_NORM_PER_TAU == invariants({e_: (Q(1), Q(0), Q(0), Q(0)) for e_ in LINKS})[0] + invariants({e_: (Q(1), Q(0), Q(0), Q(0)) for e_ in LINKS})[1],
          free_gap_E1_of_K=s(WEYL_FREE_GAP), potential_norm_per_tau='sup|W_1+W_2| = 2, attained at the identity configuration',
          solver_snapshot_sha256=inventory[P_R11_SOLVER], solver_strings_bound=len(solver_strings),
          moment_fixtures={k: s(x) for k, x in fixtures.items()}, k5={k: {str(list(m)): s(x) for m, x in p.items()} for k, p in k5.items()},
          kinetic_triangular_with_eps_diagonal_through_degree=9, kinetic_symmetric_on_P4=sym_ok, parity_vanishing_through_degree=12,
          dimensions={str(D): len(basis(D)) for D in V['cutoffs']},
          not_imported='the solver module imports numpy/scipy (bound strings above); its exact conventions are re-implemented here in Fractions')

    # ======================= exact gauge-invariance fixture (ledger item c) =======================
    qs = rational_unit_quaternions(40)
    links = {e: qs[i] for i, e in enumerate(LINKS)}
    fixture_rows = []
    inv_ok = True
    open_changed = 0
    for trial in range(4):
        g = {vx: qs[7 + 6 * trial + i] for i, vx in enumerate(VERTICES)}
        gl = gauge(links, g)
        inv_ok = inv_ok and invariants(gl) == invariants(links)
        three = qmul(qmul(qinv(links['h3']), qinv(links['vL'])), links['h1'])
        three_g = qmul(qmul(qinv(gl['h3']), qinv(gl['vL'])), gl['h1'])
        open_changed += three[0] != three_g[0]
        fixture_rows.append({'x_y_z': [s(x) for x in invariants(gl)]})
    flipped = dict(links)
    flipped['vM'] = tuple(-x for x in links['vM'])
    x0, y0, z0 = invariants(links)
    xf, yf, zf = invariants(flipped)
    z_indep = all(invariants(dict(links, vM=qs[30 + i]))[2] == z0 for i in range(4))
    norms_ok = all(sum(x * x for x in qq) == 1 for qq in qs)

    def validate_gauge_item(value, reason):
        require(value == 0, 'the gauge-projection residual of a polynomial in the trace coordinates is exactly zero')
        require('traces' in reason and 'Gauss' in reason, 'the zero entry needs its stated reason')
        return True
    gauge_reason = ('every basis element is a polynomial in the traces x,y,z of closed holonomies, invariant under all six vertex SU(2) '
                    'actions (all six Gauss constraints solved by the Round11 tree reduction Q1-Q3); H commutes with the gauge action, '
                    'so v, Hv and the complete residual lie in the gauge-invariant subspace and (I-P_phys) v = 0 exactly')
    check('gauge_invariance_fixture',
          inv_ok and norms_ok and open_changed >= 1 and (xf, yf, zf) == (-x0, -y0, z0) and z_indep and validate_gauge_item(0, gauge_reason)
          and rejected(lambda: validate_gauge_item(Q(1, 10 ** 30), gauge_reason), 'nonzero_gauge_projection_residual_claimed')
          and rejected(lambda: validate_gauge_item(0, 'not applicable'), 'zero_entry_without_reason'),
          link_quaternions={e: [s(x) for x in links[e]] for e in LINKS}, invariants=[s(x0), s(y0), s(z0)], gauge_trials=fixture_rows,
          open_three_link_path_trace_changed_in_trials=open_changed, shared_link_flip='(x,y,z) -> (-x,-y,z)',
          z_independent_of_vM=z_indep, ledger_item_c={'value': '0', 'reason': gauge_reason})

    # ======================= per-cutoff exact structures =======================
    pcs = {D: PerCutoff(D, V['tail_lower'][D]) for D in V['cutoffs']}
    check('shell_sectors_orthogonal',
          all(pc.shell_next.offdiag_nonzero == 0 and pc.shell_top.offdiag_nonzero == 0 for pc in pcs.values())
          and all(len(pc.shell_next.sectors) == (D + 2) * (D + 3) // 2 and len(pc.shell_top.sectors) == (D + 1) * (D + 2) // 2 for D, pc in pcs.items()),
          shells={str(D): {'first_omitted_shell_degree': D + 1, 'sectors': len(pc.shell_next.sectors), 'pairs_checked': pc.shell_next.pairs_checked,
                           'offdiagonal_nonzero': pc.shell_next.offdiag_nonzero, 'top_retained_shell_degree': D,
                           'top_sectors': len(pc.shell_top.sectors), 'top_pairs_checked': pc.shell_top.pairs_checked,
                           'gram_parity_blocks': [len(b) for b in pc.gs.blocks]} for D, pc in pcs.items()},
          meaning='Q_D m_s (a+b+c=D+1) are exactly mutually orthogonal: one spin-network sector (j,k,ell)=((a+c)/2,(b+c)/2,(a+b)/2) per monomial, so every omitted norm is an exact sum of sector weights')

    # ======================= exact Rayleigh-Schroedinger coefficients (full space) =======================
    rs = {}
    for D in V['cutoffs']:
        psi, En = rs_series(5, D)
        rs[D] = {'psi': psi, 'E': En, 'x': observable_series(psi, X1, 5), 'y': observable_series(psi, Y1, 5),
                 'x2': observable_series(psi, {(2, 0, 0): Q(1)}, 4), 'xy': observable_series(psi, {(1, 1, 0): Q(1)}, 4),
                 'z': observable_series(psi, Z1, 4)}
    r6, r8 = rs[6], rs[8]
    same = all(r6[k] == r8[k] for k in ('E', 'x', 'y', 'x2', 'xy', 'z')) and r6['psi'] == r8['psi']
    a = r8['x']
    e = r8['E']
    hf_ok = all(a[n] == -(n + 1) * e[n + 1] / 2 for n in range(0, 5))      # <x> = -(1/2) dE/dtau (exchange symmetry)
    one_face_psi, one_face_E = rs_series(2, 6, faces=((1, 0, 0),))
    check('rs_exact_full_space',
          same and hf_ok and a[:6] == [Q(0), Q(1, 6), Q(0), Q(-187, 33696), Q(0), Q(767713, 2523156480)]
          and e[:6] == [Q(0), Q(0), Q(-1, 6), Q(0), Q(187, 67392), Q(0)] and r8['y'] == a
          and r8['x2'][:3] == [Q(1, 4), Q(0), Q(7, 576)] and r8['xy'][:3] == [Q(0), Q(0), Q(79, 2808)] and r8['z'][:3] == [Q(0), Q(0), Q(7, 216)]
          and [pdeg(p) for p in r8['psi']] == [0, 1, 2, 3, 4, 5] and one_face_E[2] == Q(-1, 12),
          psi_1={str(list(m)): s(x) for m, x in r8['psi'][1].items()}, psi_2={str(list(m)): s(x) for m, x in r8['psi'][2].items()},
          wilson_coefficients=[s(x) for x in a], energy_coefficients=[s(x) for x in e],
          W_squared_coefficients=[s(x) for x in r8['x2']], W1W2_coefficients=[s(x) for x in r8['xy']], outer_loop_z_coefficients=[s(x) for x in r8['z']],
          identical_at_cutoffs=V['cutoffs'], full_space_residual='K psi_n = rhs_n holds as a polynomial identity for n<=5 (zero omitted-space residual)',
          psi_degrees=[pdeg(p) for p in r8['psi']], hellmann_feynman='a_n = -(n+1) e_(n+1)/2 for n<=4',
          single_face_second_order_energy_control=s(one_face_E[2]))

    # ======================= certificates: free reference and the full grid, both signs, both cutoffs =======================
    taus = [Q(0)] + [sg * g for g in V['grid'] for sg in (1, -1)]
    certs = {}
    for D in V['cutoffs']:
        for tau in taus:
            certs[(D, tau)] = certify(pcs[D], tau)
    grid_pts = [(D, tau) for D in V['cutoffs'] for tau in taus if tau != 0]
    all_ok = all(certs[k]['residual_argument_ok'] for k in certs)
    require(all_ok, 'the residual argument failed at some point')
    ident_ok = True
    for k, ct in certs.items():
        ident_ok = ident_ok and ct['rho2'] == ct['rhoP2'] + ct['rhoQ2'] and ct['PQ'] == ct['QX'] + ct['QY'] + 2 * ct['QXY']
        ident_ok = ident_ok and sum(ct['sec_w'], Q(0)) == ct['PQ'] and sum(ct['sec_x'], Q(0)) == ct['QX'] and sum(ct['sec_y'], Q(0)) == ct['QY']
        ident_ok = ident_ok and ct['wR_y'] == ct['wR']
    sign_ok = all((certs[k]['lo'] > 0) if k[1] > 0 else (certs[k]['hi'] < 0) for k in grid_pts)
    flipsign = lambda m: -1 if (m[0] + m[1]) % 2 else 1     # noqa: E731  shared-link flip (x,y,z)->(-x,-y,z)
    mirror_ok = True
    for D in V['cutoffs']:
        bs = pcs[D].bs
        for g in V['grid']:
            cp, cm = certs[(D, g)], certs[(D, -g)]
            mirror_ok = mirror_ok and cm['w'] == [flipsign(m) * x for m, x in zip(bs, cp['w'])]
            mirror_ok = mirror_ok and cm['wR'] == -cp['wR'] and cm['mu'] == cp['mu'] and cm['rho2'] == cp['rho2'] and cm['lo'] == -cp['hi']
    nest_ok = all(certs[(6, t)]['lo'] <= certs[(8, t)]['lo'] and certs[(8, t)]['hi'] <= certs[(6, t)]['hi'] for t in taus)
    widths = {point_key(*k): dec(certs[k]['hi'] - certs[k]['lo'], 6) for k in grid_pts}
    check('ritz_certificates_complete',
          all_ok and ident_ok and sign_ok and mirror_ok and nest_ok,
          points=len(certs), grid_points=len(grid_pts), enclosure_widths_preview=widths,
          identities='rho^2 = rho_P^2 + rho_Q^2; ||Q_D (x+y)v||^2 = X + Y + 2 XY; each channel equals its exact sector sum; <y> = <x> (exchange)',
          mirror='the -tau certificate is computed separately and equals the shared-link flip image of the +tau certificate exactly',
          cutoff_nesting='the D=8 enclosure lies inside the D=6 enclosure at every point (observed and checked; validity does not depend on it)',
          ritz_proposal='decimal inverse iteration (110 digits, %d steps, sigma=-tau^2/6-1/1000) rounded to integers at scale 10^100; proposal only' % RITZ_ITERATIONS)
    # ======================= item 2: own free reference and the exact derivative at tau_FG = 0 =======================
    free = {D: certs[(D, Q(0))] for D in V['cutoffs']}
    free_exact = all(fc['w'][0] == RITZ_SCALE and not any(fc['w'][1:]) for fc in free.values())
    free_ok = all(fc['lo'] == 0 == fc['hi'] and fc['wR'] == 0 and fc['mu'] == 0 and fc['rho2'] == 0 for fc in free.values())
    require(moment(1, 0, 0) == 0, 'Haar symmetry E[W]=0')
    a1 = {D: rs[D]['x'][1] for D in V['cutoffs']}
    psi1_tail_zero = all(pdeg(rs[D]['psi'][1]) == 1 <= D for D in V['cutoffs'])
    check('derivative_at_zero_exact',
          free_exact and free_ok and all(a1[D] == V['fg_first'] for D in V['cutoffs']) and psi1_tail_zero
          and rs[8]['psi'][1] == {EX: Q(1, 3), EY: Q(1, 3)} and kinetic(rs[8]['psi'][1]) == {EX: Q(1), EY: Q(1)},
          derivative={str(D): {'enclosure': [s(a1[D]), s(a1[D])], 'value': s(a1[D]), 'tail_term': '0'} for D in V['cutoffs']},
          free_reference={str(D): {'enclosure': [s(free[D]['lo']), s(free[D]['hi'])], 'ritz_vector': 'the constant (exactly)', 'energy': s(free[D]['mu']),
                                   'code_path': 'certify(pc, 0): the same function as every grid point'} for D in V['cutoffs']},
          haar_reason='E[W]=E[x]=0 because the central flip of vM maps x to -x and preserves the normalized Haar measure',
          method='Kato analytic perturbation theory (isolated simple ground E0(0)=0, gap 3, bounded V); psi_1 = K^{-1}(W_1+W_2) = (W_1+W_2)/3 exactly '
                 'because span{x,y} is the exact K-eigenspace at 3; so d<W>/dtau_FG|_0 = 2<x, psi_1> = 2 E[x^2]/3 = 1/6 with zero omitted-space tail')

    # ======================= certified finite differences with the bias bounded by Cauchy estimates (route 2) =======================
    h = min(V['grid'])
    rC, gamma = Q(3, 8), Q(3, 2)
    res_bound = (1 / gamma) / (1 - rC * V_NORM_PER_TAU / gamma)      # ||(H(tau)-z)^-1|| on |z|=3/2, |tau|<=3/8
    MW, ME = gamma * res_bound, gamma * gamma * res_bound              # ||P(tau)|| and |Tr(H P)| bounds
    require(MW == 2 and ME == 3 and rC * V_NORM_PER_TAU / gamma == Q(1, 2), 'Cauchy constants')
    rq = h / rC
    T3 = MW * rq ** 3 / (1 - rq ** 2)
    T4 = MW * rq ** 4 / (1 - rq ** 2)
    T4E = ME * rq ** 4 / (1 - rq ** 2)
    route2 = {}
    for D in V['cutoffs']:
        fp, fm, f0 = certs[(D, h)], certs[(D, -h)], free[D]
        a1lo = ((fp['lo'] - fm['hi']) / 2 - T3) / h
        a1hi = ((fp['hi'] - fm['lo']) / 2 + T3) / h
        a2lo = ((fp['lo'] + fm['lo']) / 2 - f0['hi'] - T4) / h ** 2
        a2hi = ((fp['hi'] + fm['hi']) / 2 - f0['lo'] + T4) / h ** 2
        e2lo = ((fp['E0_low'] + fm['E0_low']) / 2 - f0['mu'] - T4E) / h ** 2
        e2hi = ((fp['mu'] + fm['mu']) / 2 - f0['E0_low'] + T4E) / h ** 2
        route2[D] = {'a1': (a1lo, a1hi), 'a2': (a2lo, a2hi), 'e2': (e2lo, e2hi)}
    r2_ok = all(r['a1'][0] <= Q(1, 6) <= r['a1'][1] and r['a2'][0] <= 0 <= r['a2'][1] and r['e2'][0] <= Q(-1, 6) <= r['e2'][1] for r in route2.values())
    check('route2_cauchy_certified',
          r2_ok and h < rC,
          h=s(h), cauchy_radius=s(rC), bound_W=s(MW), bound_E=s(ME),
          tails={'odd_n>=3_W': s(T3), 'even_n>=4_W': s(T4), 'even_n>=4_E': s(T4E)},
          enclosures={str(D): {k: [s(out_dn(v[0], 12)), s(out_up(v[1], 12))] for k, v in r.items()} for D, r in route2.items()},
          previews={str(D): {k: [dec(v[0], 10), dec(v[1], 10)] for k, v in r.items()} for D, r in route2.items()},
          derivation='on |tau|<=3/8 (complex) the Riesz projection P(tau) around |z|=3/2 has ||P||<=1/(1-4|tau|/3)<=2 and |Tr(H P)|<=3; '
                     'Cauchy: |a_n|<=2(8/3)^n, |e_n|<=3(8/3)^n; the odd/even parts of the certified +-h enclosures then enclose a_1, a_2, e_2',
          independence='uses only the certified +-h and free-reference enclosures and analyticity; not the Rayleigh-Schroedinger vectors')

    # ======================= energies: complete-residual Temple route and the Round11 tail-comparison route =======================
    en_ok = all(certs[k]['E0_r11'] >= certs[k]['E0_temple'] and certs[k]['E0_low'] <= certs[k]['mu'] for k in grid_pts)
    rs_E = lambda tau: rs[8]['E'][2] * tau ** 2 + rs[8]['E'][4] * tau ** 4     # noqa: E731  (preview comparison only)
    check('energy_enclosures_two_routes',
          en_ok and all(certs[k]['s_B'] <= certs[k]['s_A'] for k in grid_pts),
          routes={'ritz_upper': 'Rayleigh-Ritz: E0 <= mu', 'temple_complete_residual': 'E0 >= mu - rho^2/(b-mu), b=3-2|tau| (Weyl)',
                  'round11_tail_comparison': 'H >= B (+) R Q_D with B=A-CC*/(tail_lower-2|tau|-R), R=3-2|tau|; E0 >= lambda_0(B) >= beta0 - eta^2/(b_B-beta0) (finite Temple)'},
          sharpening_preview={point_key(*k): dec((certs[k]['mu'] - certs[k]['E0_temple']) / (certs[k]['mu'] - certs[k]['E0_r11']), 4) for k in grid_pts},
          energy_preview={point_key(*k): [dec(certs[k]['E0_low'], 22), dec(certs[k]['mu'], 22)] for k in grid_pts},
          rs_comparison_preview={point_key(*k): dec(certs[k]['mu'] - rs_E(k[1]), 4) for k in grid_pts},
          eckart='sin^2(theta) <= (mu - E0)/(E1 - E0) <= (mu - E0_low)/(b - mu): the tail-comparison energy bound sharpens the angle bound')

    # ======================= item 3: dictionary comparison (consistency only) =======================
    aw1 = load_json_input(P_AW1_GATE)
    require('(3) omega_tau(W)=+tau/144+r(tau) under I1.5' in aw1['accepted'] and aw1['verdict'] == 'accepted_within_scope', 'AW1 gate first-order value')
    i1 = read_input(P_I1)
    require('Every other elementary face has the same nonzero coefficient `nu=alpha*tau/24`.' in i1, 'I1 face coefficient')
    require('\\phi_b=-{\\nu\\over\\delta}\\sum_{f:\\pi(\\operatorname{base}f)=b,\\ f\\notin\\mathrm{selected}}W_f' in i1, 'I1.5 sign')
    upd4 = read_input(P_UPD4)
    require('converts under `tau_FG=tau/24` to `(1/6)/24=1/144`' in upd4, 'modern lens update-4 dictionary')
    z3 = V['z3_first']
    matched = a1[6] / V['dict_den']
    r2_matched = {D: (route2[D]['a1'][0] / V['dict_den'], route2[D]['a1'][1] / V['dict_den']) for D in V['cutoffs']}
    COMPARE = {'relation': 'consistent_with', 'transfers_to_aq': False, 'kind': 'consistency check on a different, finite model'}

    def validate_comparison(cmp_):
        require(cmp_['relation'] == 'consistent_with', 'the finite graph is only consistent with the matched coefficient')
        require(cmp_['transfers_to_aq'] is False, 'no transfer to the AQ construction')
        require(cmp_['kind'] == 'consistency check on a different, finite model', 'comparison kind')
        return True
    check('dictionary_consistency_not_confirmation',
          matched == z3 and all(lo <= z3 <= hi for lo, hi in r2_matched.values()) and validate_comparison(COMPARE)
          and rejected(lambda: validate_comparison(dict(COMPARE, relation='confirms')), 'comparison_relabelled_confirmation')
          and rejected(lambda: validate_comparison(dict(COMPARE, relation='prediction')), 'comparison_relabelled_prediction')
          and rejected(lambda: validate_comparison(dict(COMPARE, transfers_to_aq=True)), 'comparison_transferred_to_aq'),
          fg_derivative=s(a1[6]), dictionary='tau_FG = tau/%d' % V['dict_den'], matched_value=s(matched), z3_first_order_from_contract=s(z3),
          z3_first_order_from_aw1_gate='+tau/144 (AW1 gate item 3)', route2_matched_enclosures={str(D): [dec(v[0], 10), dec(v[1], 10)] for D, v in r2_matched.items()},
          comparison=COMPARE)

    # ======================= item 1: the five-part residual ledger at every point =======================
    for k, ct in certs.items():
        if 'T_link' in ct:
            for cls, rec in ct['T_link'].items():
                rec['used'] = min(rec['bound'], ct['T_joint'])
    records = {}
    for (D, tau), ct in sorted(certs.items(), key=lambda kv: (kv[0][0], kv[0][1])):
        pc = pcs[D]
        per, prod, cor = classify_leakage(ct, pc)
        tau2 = tau * tau
        per_link = {}
        for link in LINKS:
            cls = LINK_CLASS[link]
            per_link[link] = {
                'class': {'j': 'left three-link path h1-vL-h3 (spin j=(a+c)/2)', 'k': 'right three-link path h2-vR-h4 (spin k=(b+c)/2)',
                          'ell': 'shared link vM (spin ell=(a+b)/2)'}[cls],
                'retained_max_spin': s(Q(D, 2)),
                'threshold_free_energy': s(pc.thr[cls][0]), 'threshold_sector_abc': list(pc.thr[cls][1]),
                'ritz_leakage_weight_upper': s(up_sig(per[cls])), 'ritz_leakage_weight_preview': dec(per[cls], 6),
                'boundary_layer_weight_upper': s(up_sig(ct['T_link'][cls]['boundary_layer_weight'])),
                'faces_touching_link': ct['T_link'][cls]['faces_touching'],
                'certified_tail_per_link_route_upper': s(up_sig(ct['T_link'][cls]['bound'])),
                'certified_tail_upper': s(up_sig(ct['T_link'][cls]['used'])), 'certified_tail_preview': dec(ct['T_link'][cls]['used'], 4)}
        nz = sum(1 for x in ct['sec_w'] if x)
        largest = max(ct['sec_w']) * tau2
        joint = {
            'complete_omitted_residual_squared_upper': s(up_sig(ct['rhoQ2'])), 'complete_omitted_residual_preview': dec(ct['rhoQ2'], 6),
            'x_channel_squared_upper': s(up_sig(tau2 * ct['QX'])), 'y_channel_squared_upper': s(up_sig(tau2 * ct['QY'])),
            'interference_2XY_bracket': [s(v) for v in sig_pair(2 * tau2 * ct['QXY'])], 'interference_2XY_preview': dec(2 * tau2 * ct['QXY'], 6),
            'product_channel_weight_upper': s(up_sig(prod)), 'product_channel_preview': dec(prod, 6),
            'product_channel_threshold': s(pc.thr['product'][0]), 'product_channel_threshold_sector_abc': list(pc.thr['product'][1]),
            'per_link_class_weights_upper': {k2: s(up_sig(v)) for k2, v in per.items()},
            'corner_overlaps_upper': {k2: s(up_sig(v)) for k2, v in sorted(cor.items())},
            'sectors': len(ct['sec_w']), 'sectors_nonzero': nz, 'largest_single_sector_weight_upper': s(up_sig(largest)),
            'joint_threshold_tail_lower': s(pc.tail_lower), 'interacting_tail_threshold': s(ct['tail_t']),
            'certified_joint_tail_upper': s(up_sig(ct['T_joint'])) if 'T_joint' in ct else None,
            'identity': 'rho_Q^2 = sum of all shell-(D+1) sector weights = (j + k + ell per-link classes) + product channel - corner overlaps (exact)'}
        rec = {
            'D': D, 'tau_FG': s(tau), 'dimension': len(pc.bs),
            'wilson_ritz_preview': dec(ct['wR'], 25),
            'wilson_enclosure': [s(ct['lo_out']), s(ct['hi_out'])],
            'wilson_enclosure_preview': [dec(ct['lo_out'], 25), dec(ct['hi_out'], 25)],
            'wilson_half_width_upper': s(up_sig(ct['delta'])), 'wilson_half_width_preview': dec(ct['delta'], 4),
            'sign_certified': (ct['lo_out'] > 0) if tau > 0 else ((ct['hi_out'] < 0) if tau < 0 else None),
            'free_reference_inside_enclosure': ct['lo_out'] <= 0 <= ct['hi_out'],
            'energy_enclosure': [s(ct['E0_lo_out']), s(ct['E0_hi_out'])],
            'energy_enclosure_preview': [dec(ct['E0_lo_out'], 22), dec(ct['E0_hi_out'], 22)],
            'gap_lower_E1_minus_E0': s(out_dn(ct['gap_lower_b'] - ct['mu'], EXPORT_DIGITS)),
            'ledger': {
                'a_per_link_representation_tail': per_link,
                'b_joint_product_channel': joint,
                'c_gauge_invariant_projection': {'value': '0', 'status': 'exactly_zero', 'reason': gauge_reason},
                'd_ritz_eigenvector_residual': {
                    'retained_ritz_residual_squared_upper': s(up_sig(ct['rhoP2'])), 'retained_preview': dec(ct['rhoP2'], 3),
                    'complete_residual_squared_upper': s(up_sig(ct['rho2'])), 'complete_preview': dec(ct['rho2'], 6),
                    'certified_gap_E1_lower': s(ct['gap_lower_b']),
                    'sin_theta_davis_kahan_complete_residual_upper': s(up_sig(ct['s_A'])),
                    'sin_theta_eckart_tail_comparison_upper': s(up_sig(ct['s_B'])),
                    'sin_theta_used_upper': s(up_sig(ct['s_used'])), 'sin_theta_used_preview': dec(ct['s_used'], 4)},
                'e_arithmetic': {'directed_sqrt_width_upper': s(up_sig(ct['arith_sqrt_width'])),
                                 'export_rounding_width_upper': s(up_sig(ct['arith_export_width'])),
                                 'status': 'charged: square roots rounded upward with integer isqrt; exported ends rounded outward to 10^-%d' % EXPORT_DIGITS,
                                 'decimal_proposal': 'the 110-digit Ritz proposal is not an admission value; its rounding is measured exactly in item d'}},
        }
        if tau != 0:
            rec['remainder_over_tau3_preview'] = dec((ct['wR'] - tau / 6) / tau ** 3, 12)
        records[point_key(D, tau)] = rec
    PREREG_MAP = {'truncation_jmax': 'ledger items a+b+c (the D-cutoff truncation; no per-link j_max is well-posed for this basis)',
                  'eigenvector_residual': 'ledger item d (complete residual, Davis-Kahan and Eckart angle bounds with the certified gap)',
                  'arithmetic': 'ledger item e (directed square roots and outward export rounding)'}
    LEDGER_KEYS = ('a_per_link_representation_tail', 'b_joint_product_channel', 'c_gauge_invariant_projection',
                   'd_ritz_eigenvector_residual', 'e_arithmetic')

    # ======================= the twenty contract controls, each with damaging mutations =======================
    gp = [k for k in grid_pts]
    MODEL = {'graph': 'Round11 two-plaquette', 'links': LINKS, 'gauss_vertices': VERTICES, 'faces_coupled': ('W1', 'W2'),
             'kinetic': 'R11_rho1', 'coupling_equal_on_faces': True, 'cutoffs': tuple(V['cutoffs']), 'grid': tuple(V['grid']),
             'sign_convention': 'I1.5: H_FG = K - tau_FG (W_1 + W_2)', 'sector': 'gauge-invariant', 'model_id': V['model_id'],
             'model_is_finite_graph': True, 'transfers_to_aq': False}

    def validate_terms(faces, kin):
        require(tuple(faces) == ('W1', 'W2'), 'both faces meeting the shared link carry the coupling (W2 is incoming on vM of square 1)')
        validate_k5(kin)
        return True
    qy_ok = all(certs[k]['QY'] > 0 and certs[k]['QX'] > 0 for k in gp)
    check('missing_incoming_stars',
          validate_terms(('W1', 'W2'), 'R11_rho1') and qy_ok and one_face_E[2] != e[2]
          and rejected(lambda: validate_terms(('W1',), 'R11_rho1'), 'incoming_face_W2_coupling_omitted')
          and rejected(lambda: validate_terms(('W1', 'W2'), 'shared_casimir_dropped'), 'shared_link_casimir_dropped_rho0')
          and rejected(lambda: validate_terms(('W1', 'W2'), 'independent_rotor'), 'independent_rotor_shared_cross_term_dropped'),
          finite_graph_analogue='the interactions touching square 1 are both faces (W2 shares vM) and all seven link Casimirs; the shared-link cross term couples the loops (K(xy)=13xy/2-z/2)',
          single_face_second_order_energy=s(one_face_E[2]), both_faces_second_order_energy=s(e[2]),
          mutated_k5={'shared_casimir_dropped': {'Kx': s(kinetic(X1, 'shared_casimir_dropped').get(EX, 0))},
                      'independent_rotor': {'K(xy)': {str(list(m)): s(x) for m, x in kinetic({(1, 1, 0): Q(1)}, 'independent_rotor').items()},
                                            'Kz': s(kinetic(Z1, 'independent_rotor').get(EZ, 0))}})

    SQUARE1 = ('h1', 'h3', 'vL', 'vM')

    def validate_observable(path_links, closed, basis_has_z):
        require(tuple(sorted(path_links)) == tuple(sorted(SQUARE1)), 'the observable is the full original square W_1: all four links h1,vL,h3,vM')
        require(closed, 'an open path trace is not gauge invariant')
        require(basis_has_z, 'the basis must contain the outer-loop coordinate z: polynomials in x,y alone are not K-invariant')
        return True
    kxy = kinetic({(1, 1, 0): Q(1)})
    check('full_original_wilson_cover',
          validate_observable(SQUARE1, True, True) and EZ in kxy and inv_ok and open_changed >= 1
          and rejected(lambda: validate_observable(('h3', 'vL', 'h1'), False, True), 'three_drawn_links_open_path')
          and rejected(lambda: validate_observable(SQUARE1, True, False), 'basis_without_outer_loop_z')
          and rejected(lambda: validate_observable(('h1', 'h2', 'vR', 'h4', 'h3', 'vL'), True, True), 'outer_perimeter_used_as_one_square'),
          cover='W_1 = (1/2)Tr(vM h3^-1 vL^-1 h1): all four links of square 1; the Hilbert space is the full seven-link physical space L^2(Omega)',
          K_xy={str(list(m)): s(x) for m, x in kxy.items()}, open_path_changed_under_gauge=open_changed)

    EW2 = moment(2, 0, 0)

    def validate_units(face_coeff_per_tau, w_energy, clock):
        require(2 * face_coeff_per_tau * EW2 / w_energy == z3, 'first-order coefficient must equal the matched 1/144 in a consistent unit system')
        require(clock == V['clock_common'], 'common physical clock s=alpha*t_E/hbar')
        return True
    alpha_fx, hbar_fx, tE_fx = Q(5), Q(7), Q(7, 5)
    s_fx = alpha_fx * tE_fx / hbar_fx
    w_energy_alpha = kinetic(X1)[EX]

    def first_order_scaled(scale):
        # H -> scale * H_FG: psi_1 = (scale K)^-1 scale (x+y) = (x+y)/3, so the first-order mean is scale independent
        return 2 * (scale * EW2) / (scale * w_energy_alpha)
    check('wrong_delta_alpha_hbar_clock',
          validate_units(Q(1, V['dict_den']), w_energy_alpha, V['clock_common']) and validate_units(Q(1, 3), 8 * w_energy_alpha, V['clock_common'])
          and s_fx == 1 and first_order_scaled(alpha_fx) == first_order_scaled(Q(1)) == V['fg_first'] and V['forbidden_u_div'] == 8
          and rejected(lambda: validate_units(Q(1, 3), w_energy_alpha, V['clock_common']), 'tau_over_18_normalized_face_with_alpha_Casimir')
          and rejected(lambda: validate_units(Q(1, 24), 8 * w_energy_alpha, V['clock_common']), 'tau_over_1152_alpha_face_with_normalized_Casimir')
          and rejected(lambda: validate_units(Q(1, 24), w_energy_alpha, 'u=s/%d' % V['forbidden_u_div']), 'normalized_clock_u'),
          units='alpha units: per-face coefficient tau/24 = tau_FG, W energy 3; normalized delta=alpha/8: per-face tau/3, W energy 24; both give 1/144',
          nonunit_fixture={'alpha': s(alpha_fx), 'hbar': s(hbar_fx), 't_E': s(tE_fx), 's': s(s_fx),
                           'note': 'a static ground-state mean is unchanged by H -> alpha H; no clock enters this loop'})

    at4 = read_input(P_AT4)
    require('For the exact control `m=1/4,d=1/100`, they are respectively `+1/10000` and `-51/10000`.' in at4
            and 'retains the vacuum residue `m²=1/16`' in at4, 'AT4 centering control')
    mm, dd = Q(1, 4), Q(1, 100)
    vec_res, scal_res, unc_res = dd * dd, -2 * mm * dd - dd * dd, mm * mm
    c10 = certs[(8, Q(1, 10))]
    var_R = c10['w2R'] - c10['wR'] ** 2
    mhat = c10['wR'] + dd
    vec_fg = c10['w2R'] - 2 * mhat * c10['wR'] + mhat ** 2       # ||(W - mhat) v||^2 (vector centring)
    scal_fg = c10['w2R'] - mhat ** 2                              # scalar subtraction

    def validate_centering(obs_centering, sigma_kind, sigma_sq):
        require(obs_centering == V['centering'], 'the enclosed observable is the uncentred <W> (contract centering: none)')
        require(sigma_kind == 'vector', 'the angle-to-observable bound uses the vector-centred norm ||(W-<W>)psi0||')
        require(sigma_sq >= var_R, 'a centring bound must dominate the true vector-centred variance')
        return True
    check('vector_versus_scalar_centering',
          vec_res == Q(1, 10000) and scal_res == Q(-51, 10000) and unc_res == Q(1, 16)
          and vec_fg == var_R + dd * dd and scal_fg == var_R - 2 * c10['wR'] * dd - dd * dd
          and validate_centering('none', 'vector', Q(1))
          and rejected(lambda: validate_centering('none', 'scalar', scal_fg), 'scalar_subtraction_as_centring_bound')
          and rejected(lambda: validate_centering('vector', 'vector', Q(1)), 'observable_centred_against_contract')
          and rejected(lambda: validate_centering('none', 'vector', scal_fg), 'scalar_value_used_as_sigma_squared'),
          at4_control={'m': s(mm), 'd': s(dd), 'vector': s(vec_res), 'scalar': s(scal_res), 'uncentred_residue': s(unc_res)},
          fg_application={'point': 'D8_tau+1/10', 'variance_preview': dec(var_R, 12), 'vector_centred_preview': dec(vec_fg, 12),
                          'scalar_subtracted_preview': dec(scal_fg, 12)},
          sigma_bound_used='||(W-<W>)psi0|| <= ||W psi0|| <= ||W|| <= 1')

    def validate_first(coef, encl):
        require(coef == V['fg_first'] and coef != 0, 'the first-order Wilson mean is charged: 1/6 on the finite graph')
        for (lo_, hi_, tau_) in encl:
            require((lo_ > 0) if tau_ > 0 else (hi_ < 0), 'the enclosure must exclude the free reference with the sign of tau_FG')
        return True
    encl_list = [(certs[k]['lo_out'], certs[k]['hi_out'], k[1]) for k in gp]
    check('first_order_mean_charged',
          validate_first(a1[8], encl_list)
          and rejected(lambda: validate_first(Q(0), encl_list), 'first_order_mean_set_to_zero_by_parity')
          and rejected(lambda: validate_first(a1[8], [(-abs(t_) / 6, abs(t_) / 6, t_) for (_, _, t_) in encl_list]), 'first_order_term_absorbed_into_remainder'),
          first_order=s(a1[8]), second_order_of_W=s(a[2]), sub_label='sign_certified_finite_graph')

    def ratio_interval(num, den):
        cands = [num[0] / den[0], num[0] / den[1], num[1] / den[0], num[1] / den[1]]
        return min(cands), max(cands)
    p2, p3 = certs[(8, Q(1, 100))], certs[(8, Q(1, 1000))]
    r_first = ratio_interval((p2['lo'], p2['hi']), (p3['lo'], p3['hi']))
    r_rem = ratio_interval((p2['lo'] - Q(1, 600), p2['hi'] - Q(1, 600)), (p3['lo'] - Q(1, 6000), p3['hi'] - Q(1, 6000)))
    r_en = ratio_interval((p2['E0_low'], p2['mu']), (p3['E0_low'], p3['mu']))
    r_leak = p2['rhoQ2'] / p3['rhoQ2']
    LABELS = {'first_order': 'linear', 'remainder': 'cubic', 'energy': 'quadratic', 'leakage_squared': 'power_2(D+1)'}
    BANDS = {'linear': (Q(99, 10), Q(101, 10)), 'quadratic': (Q(99), Q(101)), 'cubic': (Q(990), Q(1010)),
             'power_2(D+1)': (Q(9, 10) * 10 ** 18, Q(11, 10) * 10 ** 18)}

    def validate_exponent(label, interval):
        lo_, hi_ = BANDS[label]
        require(lo_ <= interval[0] and interval[1] <= hi_, 'scaling exponent does not match its label ' + label)
        return True
    check('tau_scaling_exponent',
          validate_exponent('linear', r_first) and validate_exponent('cubic', r_rem) and validate_exponent('quadratic', r_en)
          and validate_exponent('power_2(D+1)', (r_leak, r_leak))
          and rejected(lambda: validate_exponent('quadratic', r_rem), 'remainder_labelled_second_order')
          and rejected(lambda: validate_exponent('quadratic', r_first), 'first_order_labelled_quadratic')
          and rejected(lambda: validate_exponent('linear', (r_leak, r_leak)), 'omitted_leakage_labelled_linear'),
          labels=LABELS, ratios_tau_1_100_over_1_1000={'first_order': [dec(r_first[0], 8), dec(r_first[1], 8)],
                                                       'remainder_W_minus_tau_over_6': [dec(r_rem[0], 8), dec(r_rem[1], 8)],
                                                       'energy': [dec(r_en[0], 8), dec(r_en[1], 8)], 'leakage_squared_D8': dec(r_leak, 8)},
          note='certified ratio intervals from the exact enclosures at D=8; the remainder is third order because the second-order coefficient of <W> vanishes')

    def validate_model(mdl):
        require(mdl['graph'] == 'Round11 two-plaquette' and len(mdl['links']) == 7 and len(mdl['gauss_vertices']) == 6, 'graph relabelled')
        require(mdl['faces_coupled'] == ('W1', 'W2') and mdl['coupling_equal_on_faces'] is True, 'face couplings changed')
        require(mdl['kinetic'] == 'R11_rho1', 'kinetic operator changed (anisotropic or missing link)')
        require(mdl['cutoffs'] == tuple(V['cutoffs']) and mdl['grid'] == tuple(V['grid']), 'undeclared cutoff or coupling')
        require(mdl['sign_convention'] == 'I1.5: H_FG = K - tau_FG (W_1 + W_2)', 'sign convention changed')
        require(mdl['sector'] == 'gauge-invariant' and mdl['model_id'] == V['model_id'], 'sector or model id changed')
        require(mdl['model_is_finite_graph'] is True and mdl['transfers_to_aq'] is False, 'finite-graph labels')
        return True

    def mmut(**kw):
        m2 = dict(MODEL)
        m2.update(kw)
        return lambda: validate_model(m2)
    check('changed_model_relabelled',
          validate_model(MODEL)
          and rejected(mmut(kinetic='anisotropic_rho2'), 'anisotropic_shared_link_rho2')
          and rejected(mmut(graph='Round11 one-plaquette', links=LINKS[:4], gauss_vertices=VERTICES[:4]), 'one_plaquette_graph')
          and rejected(mmut(cutoffs=(4, 8)), 'undeclared_cutoff_D4')
          and rejected(mmut(grid=(Q(1, 10 ** 6), Q(1, 100), Q(1, 10))), 'off_grid_coupling')
          and rejected(mmut(coupling_equal_on_faces=False), 'unequal_face_couplings')
          and rejected(mmut(model_id='AQ_patterned_zero_selected'), 'aq_model_id')
          and rejected(mmut(sign_convention='H_FG = K + tau_FG (W_1 + W_2)'), 'sign_convention_flipped'),
          model={k: (list(v) if isinstance(v, tuple) else v) for k, v in MODEL.items() if k not in ('grid',)} | {'grid': [s(x) for x in V['grid']]})

    def validate_packet_flags(fl):
        for k1, v1 in FLAGS.items():
            require(fl.get(k1) is v1, 'claim flag ' + k1 + ' changed')
        return True
    FLAGS = {'transfers_to_aq': False, 'model_is_finite_graph': True, 'fg_coefficients_fitted': False, 'continuum_claim': False,
             'uniform_wilson_claim': False, 'resolved_interaction_shift': False, 'scientific_priority_verified': False,
             'weak_coupling_claim': False, 'aq_K2_statement_from_graph': False, 'roadmap_goal_2_resolved': False}
    require(all(FLAGS[k1] is v1 for k1, v1 in V['gate_fields'].items()), 'preregistered gate fields exported unchanged')

    def fmut(**kw):
        f2 = dict(FLAGS)
        f2.update(kw)
        return lambda: validate_packet_flags(f2)
    check('no_priority_or_continuum_claim',
          validate_packet_flags(FLAGS)
          and rejected(fmut(continuum_claim=True), 'continuum_true') and rejected(fmut(scientific_priority_verified=True), 'priority_true')
          and rejected(fmut(uniform_wilson_claim=True), 'uniform_wilson_true') and rejected(fmut(weak_coupling_claim=True), 'weak_coupling_true')
          and rejected(fmut(roadmap_goal_2_resolved=True), 'roadmap_goal_2_resolved_true'),
          flags=FLAGS, historical_or_occult_numeric_premise=False)

    LABEL = {'model_id': V['model_id'], 'graph': 'Round11 two-plaquette (open two-square patch; 6 vertices, 7 links, 6 Gauss constraints)',
             'model_is_finite_graph': True, 'transfers_to_aq': False, 'fg_coefficients_fitted': False}

    def validate_label(lb):
        require(lb['model_id'] == V['model_id'], 'finite-graph model id must be the preregistered FG id')
        require(lb['graph'].startswith('Round11 two-plaquette') and '7 links' in lb['graph'] and '6 Gauss constraints' in lb['graph'], 'graph name')
        require(lb['model_is_finite_graph'] is True and lb['transfers_to_aq'] is False and lb['fg_coefficients_fitted'] is False, 'finite-graph labels')
        return True

    def lmut(**kw):
        l2 = dict(LABEL)
        l2.update(kw)
        return lambda: validate_label(l2)
    check('finite_graph_model_id',
          validate_label(LABEL)
          and rejected(lmut(model_is_finite_graph=False), 'model_is_finite_graph_false')
          and rejected(lmut(model_id='AQ_patterned_zero_selected'), 'model_id_relabelled_AQ')
          and rejected(lmut(graph='Z^3 zero-selected patterned family'), 'graph_name_removed'),
          label=LABEL)

    def validate_complete(total_sq, parts, direct=None):
        direct = ex['rho2'] if direct is None else direct
        require(total_sq == direct, 'the complete residual is the directly computed full-space ||(H-mu)v||^2 (Hv in P_{D+1})')
        require(total_sq == parts['retained'] + parts['omitted'], 'complete residual = retained + omitted (orthogonal P_D + Q_D)')
        require(parts['omitted'] == parts['sector_sum'], 'omitted residual = exact sum over all first-omitted-shell sectors')
        require(parts['channels'] == ('x', 'y'), 'both face channels must be included')
        return True
    c_ok = True
    ex = certs[(6, Q(1, 10))]
    ex_parts = {'retained': ex['rhoP2'], 'omitted': ex['rhoQ2'], 'sector_sum': ex['tau'] ** 2 * sum(ex['sec_w'], Q(0)), 'channels': ('x', 'y')}
    for k in certs:
        ctk = certs[k]
        c_ok = c_ok and validate_complete(ctk['rho2'], {'retained': ctk['rhoP2'], 'omitted': ctk['rhoQ2'],
                                                         'sector_sum': ctk['tau'] ** 2 * sum(ctk['sec_w'], Q(0)), 'channels': ('x', 'y')},
                                          direct=ctk['rho2'])
    check('complete_residual_all_channels',
          c_ok
          and rejected(lambda: validate_complete(ex['rho2'], dict(ex_parts, omitted=ex['tau'] ** 2 * ex['QX'], sector_sum=ex['tau'] ** 2 * sum(ex['sec_x'], Q(0)))), 'y_channel_dropped')
          and rejected(lambda: validate_complete(ex['rho2'], dict(ex_parts, omitted=ex['rhoQ2'] - sum((ex['tau'] ** 2 * w_ for t_, w_ in zip(pcs[6].shell_next.sectors, ex['sec_w']) if not sector_class(t_, 6)), Q(0)))), 'product_channel_sectors_dropped')
          and rejected(lambda: validate_complete(ex['rho2'], dict(ex_parts, omitted=max(ex['sec_w']) * ex['tau'] ** 2)), 'one_omitted_sector_used_as_norm')
          and rejected(lambda: validate_complete(ex['rhoP2'], dict(ex_parts, omitted=Q(0), sector_sum=Q(0))), 'finite_matrix_residual_only')
          and rejected(lambda: validate_complete(ex['rho2'], dict(ex_parts, channels=('x',))), 'single_face_channel'),
          statement='for v in P_D, Hv lies in P_{D+1}: the complete full-space residual is (P_D + (P_{D+1}-P_D))(H-mu)v, computed exactly; no omitted component beyond shell D+1 exists',
          reference_rule='one nonzero omitted matrix element proves leakage; it does not bound the omitted norm from above (the complete sector sum is used)')

    def validate_tail(D, tau, tail_value, kind):
        require(kind == 'first omitted shell minimum minus ||V||', 'the tail threshold is m_{D+1} - 2|tau_FG| for H_FG')
        require(tail_value == shell_min(D + 1) - V_NORM_PER_TAU * abs(tau) == pcs[D].tail_lower - V_NORM_PER_TAU * abs(tau), 'tail threshold value')
        return True
    t_ok = all(validate_tail(k[0], k[1], certs[k]['tail_t'], 'first omitted shell minimum minus ||V||') for k in gp)
    t_ok = t_ok and all(certs[k]['T_joint'] <= certs[k]['s_used'] for k in gp)   # the tail route beats ||Q_D psi0|| <= sin(theta)
    tau_c = Q(1, 10)
    check('certified_representation_tail',
          t_ok and all(pcs[D].tail_lower == V['tail_lower'][D] == shell_min(D + 1) for D in V['cutoffs'])
          and rejected(lambda: validate_tail(6, tau_c, shell_min(6) - 2 * tau_c, 'first omitted shell minimum minus ||V||'), 'last_retained_shell_m_D_as_tail')
          and rejected(lambda: validate_tail(6, tau_c, shell_min(7) + 2 * tau_c, 'first omitted shell minimum minus ||V||'), 'potential_diagonal_added_to_tail')
          and rejected(lambda: validate_tail(6, tau_c, shell_min(7), 'first omitted shell minimum minus ||V||'), 'potential_norm_not_subtracted')
          and rejected(lambda: validate_tail(6, tau_c, pcs[6].thr['product'][0] - 2 * tau_c, 'first omitted shell minimum minus ||V||'), 'product_channel_threshold_as_joint_tail')
          and rejected(lambda: validate_tail(6, tau_c, pcs[6].thr['j'][0] - 2 * tau_c, 'first omitted shell minimum minus ||V||'), 'nonshared_per_link_threshold_as_joint_tail')
          and rejected(lambda: validate_tail(6, tau_c, eps_free(3, 3, 1) - 2 * tau_c, 'sampled sector'), 'sampled_single_sector_tail'),
          thresholds={str(D): {k2: {'value': s(v[0]), 'sector_abc': list(v[1])} for k2, v in pcs[D].thr.items()} for D in V['cutoffs']},
          shells_enumerated={str(D): pcs[D].thr_shells for D in V['cutoffs']},
          tail_lower={str(D): s(pcs[D].tail_lower) for D in V['cutoffs']},
          certified_joint_tail_preview={point_key(*k): dec(certs[k]['T_joint'], 4) for k in gp},
          lemma='Q_D(H-E0)psi0=0 and Q_D H Q_D >= (m_{D+1}-2|tau|) Q_D give ||Q_D psi0|| <= (||Q_D V v|| + 2|tau| sin(theta))/(m_{D+1}-2|tau|-mu); '
                'per link: ||Pi_e psi0|| <= c_e |tau| (||Lambda_e v|| + sin(theta))/(t_e - 2|tau| - mu), c_e = number of faces containing the link')

    def validate_reference(ref_value, route):
        require(route == 'same_code_path', 'the free reference is computed by certify(pc, 0), the code path of every grid point')
        require(ref_value == 0 == moment(1, 0, 0), 'the free reference is exactly E[W]=0')
        return True
    check('own_free_reference',
          all(validate_reference(free[D]['wR'], 'same_code_path') and free[D]['lo_out'] == free[D]['hi_out'] == 0 for D in V['cutoffs'])
          and rejected(lambda: validate_reference(z3, 'same_code_path'), 'Z3_first_order_imported_as_reference')
          and rejected(lambda: validate_reference(EW2, 'same_code_path'), 'W_squared_mean_as_reference')
          and rejected(lambda: validate_reference(Q(0), 'imported_from_AQ_Haar_product'), 'reference_from_another_code_path'),
          free_reference={str(D): [s(free[D]['lo_out']), s(free[D]['hi_out'])] for D in V['cutoffs']},
          grid_points_excluding_reference=sum(1 for k in gp if not records[point_key(*k)]['free_reference_inside_enclosure']))

    AQ = {'transfers_to_aq': False, 'aq_statement': None}

    def validate_aq(x):
        require(x['transfers_to_aq'] is False, 'transfers_to_aq must be false')
        require(x['aq_statement'] is None, 'no statement about the AQ shift or K_2 is drawn from the graph')
        return True
    check('no_transfer_to_aq',
          validate_aq(AQ)
          and rejected(lambda: validate_aq(dict(AQ, transfers_to_aq=True)), 'transfers_to_aq_true')
          and rejected(lambda: validate_aq(dict(AQ, aq_statement='K_2 of the AQ model is bounded by the graph remainder')), 'aq_K2_statement_from_graph')
          and rejected(lambda: validate_aq(dict(AQ, aq_statement='graph resolves roadmap goal 2')), 'roadmap_goal_2_from_graph'),
          note='the graph remainder (third order, coefficient -187/33696 in tau_FG) is a finite-model value only')

    pos = [(k[1], certs[k]['wR']) for k in gp if k[0] == 8 and k[1] > 0]
    ls_slope = sum((t_ * w_ for t_, w_ in pos), Q(0)) / sum((t_ * t_ for t_, _ in pos), Q(0))
    secant = certs[(8, Q(1, 10))]['wR'] / Q(1, 10)

    def validate_coefficient(value, provenance):
        require(provenance == 'exact Rayleigh-Schroedinger (full-space residual zero)', 'coefficients come from exact perturbation theory, never a fit')
        require(value == a1[8], 'coefficient differs from the exact value')
        return True
    check('fg_coefficients_not_fitted',
          validate_coefficient(a1[8], 'exact Rayleigh-Schroedinger (full-space residual zero)') and ls_slope != a1[8]
          and rejected(lambda: validate_coefficient(ls_slope, 'least-squares fit to the grid Ritz values'), 'least_squares_slope_through_grid')
          and rejected(lambda: validate_coefficient(secant, 'exact Rayleigh-Schroedinger (full-space residual zero)'), 'secant_slope_relabelled_exact'),
          fitted_slope_preview=dec(ls_slope, 12), secant_preview=dec(secant, 12), exact=s(a1[8]), fg_coefficients_fitted=False)

    def first_order_from_convention(sign):
        # H = K + sign*tau*(x+y): psi_1 = -sign (x+y)/3, a_1 = 2<x,psi_1> = -2 sign E[x^2]/3
        return -2 * sign * EW2 / w_energy_alpha

    def validate_sign(sign, label):
        require(first_order_from_convention(sign) > 0, 'I1.5: the first-order Wilson mean is positive for positive tau_FG')
        require(label in ('I1.5', 'Round11 lambda(1-x) with lambda=tau_FG'), 'unknown convention')
        return True
    def validate_sign_record(lo_, hi_, tau_):
        require((lo_ > 0) if tau_ > 0 else (hi_ < 0), 'under I1.5 the certified mean has the sign of tau_FG')
        return True
    check('sign_convention_fixture',
          validate_sign(-1, 'I1.5') and validate_sign(-1, 'Round11 lambda(1-x) with lambda=tau_FG') and first_order_from_convention(-1) == Q(1, 6)
          and certs[(8, Q(1, 10))]['lo_out'] > 0 and certs[(8, Q(-1, 10))]['hi_out'] < 0 and rs_series(1, 6, sign=1)[0][1] == {EX: Q(-1, 3), EY: Q(-1, 3)}
          and validate_sign_record(certs[(8, Q(1, 10))]['lo_out'], certs[(8, Q(1, 10))]['hi_out'], Q(1, 10))
          and rejected(lambda: validate_sign(1, 'I1.5'), 'flipped_sign_gives_minus_one_sixth')
          and rejected(lambda: validate_sign_record(-certs[(8, Q(1, 10))]['hi_out'], -certs[(8, Q(1, 10))]['lo_out'], Q(1, 10)), 'enclosure_sign_read_against_I1_5'),
          convention='H_FG = K - tau_FG (W_1 + W_2) = Round11 H(alpha=1, lambda1=lambda2=tau_FG, rho=1) - 2 tau_FG (the constant shifts no state)',
          fixture='two-state span{1, W_1}: first-order mean +tau_FG/6; the flipped sign gives -tau_FG/6',
          exact_positive_enclosure_at_plus_one_tenth=records['D8_tau+1/10']['wilson_enclosure'])

    def validate_ledger(ld, verdict):
        for key in LEDGER_KEYS:
            require(key in ld, 'ledger item missing: ' + key)
        require(len(ld['a_per_link_representation_tail']) == 7, 'seven per-link rows required')
        require('product_channel_weight_upper' in ld['b_joint_product_channel'] and 'interference_2XY_bracket' in ld['b_joint_product_channel'],
                'joint product channel must be itemized')
        require(ld['c_gauge_invariant_projection'].get('reason'), 'a zero or not_applicable entry needs a stated reason')
        if verdict == 'accepted_within_scope':
            require(all(key in ld for key in LEDGER_KEYS), 'accepted verdict needs the complete ledger')
        return True
    L0 = records['D8_tau+1/10']['ledger']

    def lmut2(drop=None, **kw):
        l2 = json.loads(json.dumps(L0))
        if drop:
            l2.pop(drop)
        for k1, v1 in kw.items():
            l2[k1] = v1
        return lambda: validate_ledger(l2, 'accepted_within_scope')
    check('complete_residual_ledger_itemized',
          all(validate_ledger(r_['ledger'], 'accepted_within_scope') for r_ in records.values())
          and rejected(lmut2(drop='b_joint_product_channel'), 'joint_product_channel_not_itemized')
          and rejected(lmut2(c_gauge_invariant_projection={'value': '0', 'status': 'not_applicable'}), 'gauge_entry_without_reason')
          and rejected(lmut2(a_per_link_representation_tail={k1: v1 for k1, v1 in L0['a_per_link_representation_tail'].items() if k1 != 'vM'}), 'shared_link_row_removed')
          and rejected(lmut2(drop='e_arithmetic'), 'arithmetic_item_missing'),
          ledger_items=list(LEDGER_KEYS), preregistered_error_terms=V['error_terms'], mapping=PREREG_MAP, points=len(records))

    def validate_joint(total, parts):
        require(total == parts['sum_of_orthogonal_sectors'], 'squared norms add only over exactly orthogonal sectors')
        require(parts['x_channel'] + parts['y_channel'] + parts['interference'] == total, 'the x and y face channels are not orthogonal: keep 2XY')
        return True
    J0 = {'sum_of_orthogonal_sectors': ex['tau'] ** 2 * sum(ex['sec_w'], Q(0)), 'x_channel': ex['tau'] ** 2 * ex['QX'],
          'y_channel': ex['tau'] ** 2 * ex['QY'], 'interference': 2 * ex['tau'] ** 2 * ex['QXY']}
    per0, prod0, cor0 = classify_leakage(ex, pcs[6])
    check('root_n_misuse',
          validate_joint(ex['rhoQ2'], J0) and ex['QXY'] > 0 and sum(per0.values()) + prod0 - sum(cor0.values()) == ex['rhoQ2']
          and rejected(lambda: validate_joint(ex['rhoQ2'], dict(J0, interference=Q(0))), 'rss_of_face_channels_without_interference')
          and rejected(lambda: validate_joint(sum(per0.values()) / 7, J0), 'per_link_sum_divided_by_seven')
          and rejected(lambda: validate_joint(sqrt_up(sum(v * v for v in per0.values()) / 3), J0), 'root_mean_square_over_link_classes'),
          interference_sign='positive (constructive): dropping 2XY undercounts the omitted norm',
          example={'point': 'D6_tau+1/10', 'x': dec(J0['x_channel'], 6), 'y': dec(J0['y_channel'], 6), '2XY': dec(J0['interference'], 6), 'total': dec(ex['rhoQ2'], 6)})

    check('exact_arithmetic_admission',
          rat('1/6') == a1[8] and isinstance(certs[(8, Q(1, 10))]['lo'], Q)
          and rejected(lambda: rat(1 / 6), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('nan'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator')
          and rejected(lambda: rat(to_dec(certs[(8, Q(1, 10))]['wR'])), 'decimal_proposal_value_as_admission'),
          arithmetic='fractions.Fraction throughout; decimal only proposes the Ritz vector; square roots by integer isqrt with upward rounding; exports outward')

    # ======================= verdict, retained tiers and target =======================
    def certified(k):
        ct = certs[k]
        return ct['residual_argument_ok'] and 'T_joint' in ct and records[point_key(*k)]['sign_certified'] is True
    all_d6 = all(certified(k) for k in gp if k[0] == 6)
    all_d8 = all(certified(k) for k in gp if k[0] == 8)
    product_itemized = all('product_channel_weight_upper' in r_['ledger']['b_joint_product_channel'] for r_ in records.values())
    first_consistent = all(a1[D] == V['fg_first'] and route2[D]['a1'][0] <= V['fg_first'] <= route2[D]['a1'][1] for D in V['cutoffs'])
    labels_present = validate_label(LABEL) and validate_packet_flags(FLAGS)
    verdict = forward_verdict(all_d6, all_d8, product_itemized, first_consistent, labels_present, all_ok, False)

    def validate_verdict(reported, *args):
        require(reported == forward_verdict(*args), 'reported verdict differs from the contract acceptance rule')
        return True
    retained = {
        'davis_kahan_complete_residual_angle': {point_key(*k): dec(certs[k]['s_A'] / certs[k]['s_B'], 4) for k in gp},
        'temple_energy_lower_bound': 'retained; the Round11 tail comparison is sharper by the factors in energy_enclosures_two_routes',
        'route2_cauchy_intervals': 'retained; certified but wider (about 1e-4) than the exact perturbative values',
        'per_link_route_for_vM': 'retained; for the shared link the per-link bound exceeds the joint bound, and the smaller is used',
        'negative_tau_outside_solver_api': 'the Round11 solver API restricts lambda>=0; the negative-tau points are certified here by the same exact argument, which needs no sign',
    }
    check('insufficient_verdict_retained',
          verdict == 'accepted_within_scope'
          and forward_verdict(True, False, True, True, True, True, False) == 'limited'
          and forward_verdict(True, True, False, True, True, True, False) == 'limited'
          and forward_verdict(True, True, True, True, True, False, False) == 'insufficient'
          and forward_verdict(True, True, True, True, True, True, True) == 'insufficient'
          and rejected(lambda: validate_verdict('accepted_within_scope', True, False, True, True, True, True, False), 'tail_only_at_D6_relabelled_accepted')
          and rejected(lambda: validate_verdict('accepted_within_scope', True, True, False, True, True, True, False), 'product_channel_missing_relabelled_accepted')
          and rejected(lambda: validate_verdict('limited', True, True, True, True, True, False, False), 'failed_residual_argument_relabelled_limited'),
          rule='insufficient if the residual argument fails or an excluded claim is made; limited if the tail is certified only at D=6 or the joint product channel is not itemized',
          retained_weaker_tiers=retained, acceptance_clauses=V['acceptance'])

    target_metric = 1 if (all_d6 and all_d8 and first_consistent
                          and all(r_['ledger']['b_joint_product_channel']['certified_joint_tail_upper'] is not None and r_['wilson_half_width_upper'] for r_ in records.values())) else 0
    require(target_metric >= V['target'], 'preregistered feasibility target not met')

    # ======================= report: mandatory sentence, forbidden phrasings, exact values, map =======================
    report_text = (BASE / 'report.md').read_text(encoding='utf-8')
    sentence = V['sentence']
    required_values = ['1/6', '1/144', '-187/33696', '187/67392', '7/576', '79/2808', '7/216', '767713/2523156480', '123/2', '145/2']
    required_values += records['D8_tau+1/10']['wilson_enclosure'] + records['D6_tau+1/10']['wilson_enclosure']

    def scan_report(text):
        require(sentence in text, 'mandatory sentence missing from the report (verbatim)')
        body = strip_code(text).lower()
        for ph in V['forbidden']:
            require(ph.lower() not in body, 'forbidden phrasing in the report: ' + ph)
        require('consistent with' in body, 'required phrase: consistent with')
        for val in required_values:
            require(val in text, 'report does not carry the exact value ' + val[:40])
        require('transfers_to_aq' in text and 'model_is_finite_graph' in text and 'fg_coefficients_fitted' in text, 'gate fields named in the report')
        require('/tmp/claude-0/az2-forward-private/' in text, 'scratch disclosure')
        return True
    check('mandatory_sentence_and_phrasing',
          scan_report(report_text)
          and rejected(lambda: scan_report(report_text + '\nThe finite graph predicts the matched coefficient.\n'), 'report_phrase_predicts')
          and rejected(lambda: scan_report(report_text + '\nThis confirms the Z^3 value.\n'), 'report_phrase_confirms_the_Z3_value')
          and rejected(lambda: scan_report(report_text.replace(sentence, sentence.replace('not a prediction, ', ''))), 'mandatory_sentence_altered'),
          mandatory_sentence=sentence, forbidden_phrasings=V['forbidden'],
          report_scan='report.md scanned with code spans removed (case-insensitive): no forbidden phrasing; mandatory sentence verbatim; exact values present')

    def map_rows(text):
        sec = text.split('## 10. Item and control map', 1)
        require(len(sec) == 2, 'map section 10 missing')
        return [ln for ln in sec[1].split('\n## ', 1)[0].splitlines() if ln.startswith('| ')]

    def validate_map(rows):
        miss_c = [cid for cid in V['controls'] if not any(r1.startswith('| `' + cid + '` |') for r1 in rows)]
        miss_i = [k for k in range(1, 7) if not any(r1.startswith('| item %d ' % k) for r1 in rows)]
        require(not miss_c and not miss_i, 'map lacks rows for ' + ','.join(miss_c + ['item %d' % k for k in miss_i]))
        return True
    mrows = map_rows(report_text)
    check('report_item_and_control_map',
          validate_map(mrows)
          and rejected(lambda: validate_map([r1 for r1 in mrows if not r1.startswith('| `root_n_misuse` |')]), 'control_row_removed_from_map')
          and rejected(lambda: validate_map([r1 for r1 in mrows if not r1.startswith('| item 4 ')]), 'item_4_row_removed_from_map'),
          controls_in_map=len(V['controls']), items_in_map=6, map_section='report.md section 10')

    # ======================= contract wording defects (non-blocking), each a verified fact about the frozen text =======================
    defects = []
    if 'truncation_jmax' in V['error_terms'] and 'no per-link spin label j_max is well-posed' in c['parameters']['cutoff']:
        defects.append({'id': 'D1', 'field': 'preregistration.error_terms_itemized', 'defect': "'truncation_jmax' although parameters.cutoff states that no per-link j_max is well-posed; mapped to the D-cutoff truncation (ledger items a+b+c)"})
    if V['state_provenance'].startswith('AQ1_centered_whole_star_subsequence'):
        defects.append({'id': 'D2', 'field': 'preregistration.state_provenance', 'defect': "'%s' is an AQ-family provenance; the FG state is the unique ground state of H_FG on the graph's physical space (Round11 Theorem F, and E0<=mu<b<=E1 here); not used" % V['state_provenance']})
    if all(cid in V['controls'] for cid in ('missing_incoming_stars', 'full_original_wilson_cover', 'wrong_delta_alpha_hbar_clock', 'root_n_misuse')):
        defects.append({'id': 'D3', 'field': 'controls', 'defect': 'several control ids name AQ/Z^3 objects (incoming stars, the 48-link cover, the alpha/8 clock, root-N); each is given an explicit finite-graph analogue in the checker and report map'})
    if 'with the tail residual bounding the truncation error' in V['required'][3]:
        defects.append({'id': 'D4', 'field': 'required[3]', 'defect': 'the truncation error of the perturbative coefficients is exactly zero (psi_n in P_n inside P_D for n<=5), and the second-order coefficient of <W> is exactly zero by the shared-link flip; reported as such, with Cauchy-certified route-2 intervals'})
    if V['target'] == 1 and V['target_comparator'] == '>=':
        defects.append({'id': 'D5', 'field': 'preregistration.target', 'defect': "value '1' with comparator '>=' on a conjunction of conditions; evaluated as a 0/1 feasibility indicator"})
    if V['selected_after'] == 'research/round32/advisor/az1-gate.json' and V['selected_after'] not in V['shared']:
        defects.append({'id': 'D6', 'field': 'selected_after', 'defect': 'names the AZ1 gate, which is not a declared premise and was not read by this producer'})
    if 'must reproduce the matched first-order value' in V['observable_param']:
        defects.append({'id': 'D7', 'field': 'parameters.observable', 'defect': "'must reproduce the matched first-order value' reads as a target; treated strictly as the consistency comparison of item 3"})
    if V['forbidden_exponent'] == V['dict_den']:
        defects.append({'id': 'D8', 'field': 'preregistration.clock', 'defect': "'exponent 24 forbidden' coexists with the dictionary denominator 24 (tau_FG=tau/24), a coupling ratio and not a clock exponent; no Euclidean exponent of any kind appears in this static packet"})
    check('contract_wording_defects_recorded', len(defects) == 8, defects=defects, blocking=False)

    # ======================= no solver / flint import; the optional Arb preview stays a labelled preview =======================
    src_lines = [ln.strip() for ln in (BASE / 'check.py').read_text(encoding='utf-8').splitlines()]
    banned = ['import ' + 'numpy', 'from ' + 'numpy', 'import ' + 'scipy', 'from ' + 'scipy', 'import ' + 'flint', 'from ' + 'flint',
              'import ' + 'two_plaquette', 'from ' + 'two_plaquette', 'import ' + 'arb_preview', 'from ' + 'arb_preview', 'import ' + 'mpmath']
    imports_ok = not any(ln.startswith(b) for ln in src_lines for b in banned)
    prev = {'script_present': (BASE / 'arb_preview.py').is_file(), 'output_present': (BASE / 'preview' / 'arb_preview.json').is_file()}
    compared, intersect = 0, True
    if prev['script_present']:
        require('PREVIEW ONLY' in (BASE / 'arb_preview.py').read_text(encoding='utf-8'), 'arb_preview.py must carry its preview label')
    if prev['output_present']:
        pj = json.loads((BASE / 'preview' / 'arb_preview.json').read_text(encoding='utf-8'))
        require(pj.get('label') == 'PREVIEW ONLY - python-flint Arb/fmpq cross-check; never an admission value', 'preview label')
        prev['flint_version'] = pj.get('flint_version')
        for key, ball in sorted(pj.get('wilson_balls', {}).items()):
            if key in records:
                lo_b, hi_b = Q(ball[0]), Q(ball[1])
                lo_e, hi_e = Q(records[key]['wilson_enclosure'][0]), Q(records[key]['wilson_enclosure'][1])
                intersect = intersect and max(lo_b, lo_e) <= min(hi_b, hi_e)
                compared += 1
    prev['points_compared'] = compared
    prev['all_balls_intersect_exact_enclosures'] = intersect
    check('no_solver_import_and_preview_labelled',
          imports_ok and intersect,
          banned_imports_absent=True, arb_preview=prev,
          note='the Round11 solver (numpy/scipy) and python-flint are never imported; the Arb preview is compared with, never used for, admission')

    # ======================= packet, headline and coherent tampering =======================
    grid_keys = [point_key(*k) for k in gp]
    headline = {
        'observable': '<W_1>_FG = <psi_0, (1/2)Tr(U) psi_0>, U = vM h3^-1 vL^-1 h1 (square 1); <W_2> = <W_1> by the exchange symmetry',
        'hamiltonian': 'H_FG = K - tau_FG (W_1 + W_2), alpha units, K = sum of the seven link Casimirs j(j+1) (Round11 rho=1)',
        'derivative_at_zero': {str(D): [s(a1[D]), s(a1[D])] for D in V['cutoffs']},
        'derivative_tail_term': '0',
        'derivative_route2_cauchy': {str(D): [s(out_dn(route2[D]['a1'][0], 12)), s(out_up(route2[D]['a1'][1], 12))] for D in V['cutoffs']},
        'dictionary': {'tau_FG': 'tau/%d' % V['dict_den'], 'fg_first_order': s(a1[6]), 'matched_value': s(matched), 'z3_first_order': s(z3),
                       'relation': 'consistent_with'},
        'free_reference': {str(D): [s(free[D]['lo_out']), s(free[D]['hi_out'])] for D in V['cutoffs']},
        'wilson_enclosures': {k: records[k]['wilson_enclosure'] for k in grid_keys},
        'wilson_enclosures_preview': {k: records[k]['wilson_enclosure_preview'] for k in grid_keys},
        'wilson_half_width_preview': {k: records[k]['wilson_half_width_preview'] for k in grid_keys},
        'energy_enclosures_preview': {k: records[k]['energy_enclosure_preview'] for k in grid_keys},
        'second_order_coefficients': {'W_1': s(a[2]), 'E_0': s(e[2]), 'W_1_squared': s(r8['x2'][2]), 'W_1_W_2': s(r8['xy'][2]),
                                      'outer_loop_z': s(r8['z'][2])},
        'second_order_route2_cauchy': {str(D): {'W_1': [s(out_dn(route2[D]['a2'][0], 12)), s(out_up(route2[D]['a2'][1], 12))],
                                                'E_0': [s(out_dn(route2[D]['e2'][0], 12)), s(out_up(route2[D]['e2'][1], 12))]} for D in V['cutoffs']},
        'higher_order': {'W_1_tau3': s(a[3]), 'W_1_tau5': s(a[5]), 'E_0_tau4': s(e[4])},
        'truncation_error_of_coefficients': '0 (psi_n in P_n inside P_D for n<=5; full-space residual zero)',
        'tail_lower': {str(D): s(pcs[D].tail_lower) for D in V['cutoffs']},
        'certified_joint_tail_upper': {k: records[k]['ledger']['b_joint_product_channel']['certified_joint_tail_upper'] for k in grid_keys},
        'sin_theta_used_preview': {k: records[k]['ledger']['d_ritz_eigenvector_residual']['sin_theta_used_preview'] for k in grid_keys},
        'sign_certified_all_grid_points': all(records[k]['sign_certified'] for k in grid_keys),
        'target_metric': target_metric, 'target': s(V['target']), 'target_comparator': V['target_comparator'],
    }
    label_block = dict(LABEL)
    label_block.update({'sub_labels': ['sign_certified_finite_graph', 'static_not_dynamic'], 'cutoffs': V['cutoffs'],
                        'grid': [s(x) for x in V['grid']], 'signs': V['signs'], 'dictionary': 'tau_FG = tau/%d (consistency only)' % V['dict_den'],
                        'first_order_FG': s(a1[8]), 'first_order_matched_Z3': s(z3), 'relation': 'consistent_with'})
    verdict_line = (verdict + " (forward half of a single+skeptic loop; admission requires the skeptic's pre-comparison replay from the contract alone "
                    "and post-comparison review); sub-labels sign_certified_finite_graph, static_not_dynamic")
    packet = {
        'loop': 'AZ2', 'direction': 'forward', 'human_author': HUMAN_AUTHOR,
        'contribution_alias': 'HNM-AZ2-F forward exact finite-graph first- and second-order Wilson coefficients on the Round11 two-plaquette graph (D in {6,8}; complete five-part residual ledger)',
        'ai_assistance': 'AI-assisted forward production (a Claude model agent); correlated model-agent work, not independent human review',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha,
        'model': {'model_id': V['model_id'], 'statement': V['model'], 'graph': LABEL['graph'], 'links': {e_: list(ORIENT[e_]) for e_ in LINKS},
                  'loops': 'U = vM h3^-1 vL^-1 h1, V = h2 vR h4^-1 vM^-1 (Round11 G2)', 'hamiltonian': headline['hamiltonian'],
                  'round11_equivalence': 'H_FG = H_R11(alpha=1, lambda1=lambda2=tau_FG, rho=1) - 2 tau_FG',
                  'cutoffs': V['cutoffs'], 'dimensions': {str(D): len(pcs[D].bs) for D in V['cutoffs']}, 'grid': [s(x) for x in V['grid']],
                  'signs': V['signs'], 'clock': V['clock_common'] + ' (named only; static loop)'},
        'headline': headline, 'label': label_block, 'sub_labels': ['sign_certified_finite_graph', 'static_not_dynamic'],
        'points': records, 'error_terms_itemized': PREREG_MAP, 'ledger_items': list(LEDGER_KEYS),
        'rs_coefficients': {'W_1': [s(x) for x in a], 'E_0': [s(x) for x in e], 'W_1_squared': [s(x) for x in r8['x2']],
                            'W_1_W_2': [s(x) for x in r8['xy']], 'outer_loop_z': [s(x) for x in r8['z']]},
        'mandatory_sentence': sentence, 'gate_fields': dict(V['gate_fields']),
        'exclusions': {'contract': V['claim_exclusions'], 'preregistration': V['prereg_exclusions'],
                       'additional': ['no statement about the AQ model, its shift or K_2 from the graph', 'no dynamical or mass-gap reading of a static mean',
                                      'no cutoff beyond D=8; D=10 not declared', 'no per-link j_max cutoff (none is well-posed for this basis)']},
        'contract_wording_defects': defects,
        'routes_executed': ['forward: exact Rayleigh-Schroedinger series in the full graph space (polynomial resolvent, zero omitted residual)',
                            'forward: exact Ritz certificates at 14 points (free reference + grid, both signs, D=6 and D=8) with the complete shell-(D+1) residual',
                            'forward: Davis-Kahan (complete residual + Weyl gap) and Eckart (Round11 tail comparison + Weyl gap) angle bounds',
                            'forward: certified tails of the true ground state from the tail threshold, joint and per link',
                            'forward: Cauchy-certified finite differences for the first- and second-order coefficients (route 2)'],
        'routes_not_executed': ['skeptic pre-comparison replay from the contract alone and post-comparison review (single_direction_independent_replay; outside this producer)'],
        'protocol_steps_outside_check_py': {'freeze_and_byte_identical_replays': 'research/round32/tools/freeze.py',
                                            'arb_preview': 'arb_preview.py (python-flint), a labelled preview whose output is only compared'},
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
        validate_packet_flags({k1: pk[k1] for k1 in FLAGS})
        require(sorted(inv) == sorted(set(expected_inputs)) and inv.get(CONTRACT_REL) == contract_digest, 'premise snapshot inventory or contract hash')
        require(pk['contract_sha256'] == contract_digest, 'contract hash changed')
        hd = pk['headline']
        for key in grid_keys:
            require(hd['wilson_enclosures'][key] == records[key]['wilson_enclosure'] == pk['points'][key]['wilson_enclosure'], 'enclosure differs from recomputation: ' + key)
        for (D, tau) in gp:
            key = point_key(D, tau)
            require(pk['points'][key]['wilson_enclosure'] == [s(certs[(D, tau)]['lo_out']), s(certs[(D, tau)]['hi_out'])], 'enclosure ends differ from the exact certificate')
            require(pk['points'][key]['ledger']['a_per_link_representation_tail'].keys() == set(LINKS), 'per-link ledger rows changed')
        require(hd['derivative_at_zero'] == {str(D): [s(a1[D]), s(a1[D])] for D in V['cutoffs']} and hd['derivative_tail_term'] == '0', 'derivative changed')
        require(hd['second_order_coefficients']['W_1'] == s(a[2]) == '0' and hd['second_order_coefficients']['E_0'] == s(e[2]), 'second-order coefficients changed')
        require(hd['tail_lower'] == {str(D): s(pcs[D].tail_lower) for D in V['cutoffs']}, 'tail_lower changed')
        require(hd['dictionary']['matched_value'] == s(z3) and hd['dictionary']['relation'] == 'consistent_with', 'dictionary changed')
        require(hd['target_metric'] == target_metric, 'target metric changed')
        validate_label({k1: pk['label'][k1] for k1 in LABEL})
        require(pk['proposed_forward_verdict'].startswith(verdict + ' '), 'verdict changed')
        require(pk['mandatory_sentence'] == sentence, 'mandatory sentence changed')
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
            if ch['id'] == 'complete_residual_all_channels':
                ch['passed'] = False

    def t_lower(pk, inv):
        pk['points']['D8_tau+1/10']['wilson_enclosure'][0] = s(Q(pk['points']['D8_tau+1/10']['wilson_enclosure'][0]) + Q(1, 10 ** 30))
        pk['headline']['wilson_enclosures']['D8_tau+1/10'] = pk['points']['D8_tau+1/10']['wilson_enclosure']

    def t_deriv(pk, inv):
        pk['headline']['derivative_at_zero']['6'] = ['1/144', '1/144']

    def t_second(pk, inv):
        pk['headline']['second_order_coefficients']['W_1'] = '1/1000'

    def t_transfer(pk, inv):
        pk['transfers_to_aq'] = True

    def t_snapshot(pk, inv):
        inv.pop(P_R11_SOLVER)

    def t_contract(pk, inv):
        inv[CONTRACT_REL] = '0' * 64
        pk['contract_sha256'] = '0' * 64

    def t_row(pk, inv):
        pk['points']['D6_tau-1/100']['ledger']['a_per_link_representation_tail'].pop('vM')

    def t_tail(pk, inv):
        pk['headline']['tail_lower']['8'] = '56'

    def t_label(pk, inv):
        pk['label']['model_is_finite_graph'] = False

    def t_verdict(pk, inv):
        pk['proposed_forward_verdict'] = 'limited ' + pk['proposed_forward_verdict']

    def t_sentence(pk, inv):
        pk['mandatory_sentence'] = pk['mandatory_sentence'].replace('is consistent with', 'confirms')
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(tamper(t_control), 'control_boolean_flipped_hash_rebound')
          and rejected(tamper(t_lower), 'enclosure_lower_end_raised_hash_rebound')
          and rejected(tamper(t_deriv), 'derivative_replaced_by_1_144_hash_rebound')
          and rejected(tamper(t_second), 'second_order_W_coefficient_made_nonzero_hash_rebound')
          and rejected(tamper(t_transfer), 'transfers_to_aq_true_hash_rebound')
          and rejected(tamper(t_snapshot), 'solver_snapshot_removed_hash_rebound')
          and rejected(tamper(t_contract), 'contract_hash_replaced_hash_rebound')
          and rejected(tamper(t_row), 'shared_link_ledger_row_removed_hash_rebound')
          and rejected(tamper(t_tail), 'tail_lower_replaced_by_last_retained_shell_hash_rebound')
          and rejected(tamper(t_label), 'finite_graph_label_false_hash_rebound')
          and rejected(tamper(t_verdict), 'verdict_changed_hash_rebound')
          and rejected(tamper(t_sentence), 'mandatory_sentence_changed_hash_rebound'))

    ids = [ch['id'] for ch in CHECKS]
    missing_c = [cid for cid in V['controls'] if cid not in ids]
    require(not missing_c, 'contract controls without a check: ' + ','.join(missing_c))
    positive_only = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch.get('rejected_mutations')]
    require(not positive_only, 'contract controls without a damaging mutation: ' + ','.join(positive_only))
    require(not PENDING, 'rejected mutations not attached to a check')
    packet['checks'] = CHECKS
    packet['contract_controls_covered'] = sorted(V['controls'])
    packet['controls_with_damaging_mutations'] = sum(1 for ch in CHECKS if ch['id'] in V['controls'] and ch.get('rejected_mutations'))
    packet['rejected_mutations_in_control_checks'] = sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS if ch['id'] in V['controls'])
    packet['rejected_mutation_total'] = sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS)
    packet['check_count'] = len(CHECKS)
    dump = json.dumps(packet, sort_keys=True)
    require('u=s/' not in dump and 'e^(-24' not in dump and 'exp(-24' not in dump, 'forbidden normalized clock or exponent in the packet')
    return packet


def float_free(obj):
    if isinstance(obj, float):
        return False
    if isinstance(obj, dict):
        return all(float_free(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return all(float_free(v) for v in obj)
    return True


def main():
    ap = argparse.ArgumentParser(description='AZ2 forward exact checker')
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
        if p.is_file() and rel.parts[0] != 'output' and (rel.parts[0] in ('inputs', 'preview') or p.name in ('check.py', 'report.md', 'arb_preview.py')):
            sources[rel.as_posix()] = sha(p)
    manifest = {'loop': 'AZ2', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    hd = result['headline']
    print(json.dumps({'loop': 'AZ2', 'direction': 'forward', 'checks': len(result['checks']),
                      'derivative_at_zero': hd['derivative_at_zero'], 'D8_tau+1/10': hd['wilson_enclosures_preview']['D8_tau+1/10'],
                      'verdict': result['proposed_forward_verdict'].split(' ')[0]}, sort_keys=True))


if __name__ == '__main__':
    main()
