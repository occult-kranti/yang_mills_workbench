#!/usr/bin/env python3
"""Round32 AZ1 skeptic pre-comparison checker (statement loop, continuum-trajectory statement).

Written after the AZ1 contract froze, from the frozen contract and its pinned premises (AX1 gate, AL1 gate
and report, AM2 gate and forward report, AX1 forward and reverse reports, the skeptic AX1 review, the
modern lens's update-4 and SOTA table, the AZ1 selection note), without opening or listing anything under
research/round32/forward/az1/ except the names of its inputs/ snapshot, and without opening anything under
research/round32/forward/az2/. Nothing is imported from any producer or assistant. Standard library only.
Every admission Boolean is decided with fractions.Fraction or exact integers; floats appear only in the
labelled 'previews' block. Every check and control raises an explicit exception, so python -O cannot
disable it. Model-agent skeptic with correlated ancestry; not human peer review, not formal verification.

What is derived here:
  * the AL1 dictionary alpha=g^2/(2a), lambda=2/(g^2 a) and its consequences tau=24 lambda/alpha=96/g^4,
    alpha/16=g^2/(32a), alpha*lambda*a^2=1, r=lambda/alpha=4/g^4, nu=alpha tau/24=lambda, nu/delta=tau/3,
    7|tau|=672/g^4 and the inverse map (a^2=1/(alpha lambda), g^4=4 alpha/lambda), each verified as an
    identity of rational functions in (G=g^2, a) by polynomial cross-multiplication and again at exact
    sample points;
  * the admitted regime tau<=10^-8 <=> g^4>=9.6x10^9 (AX1 gate), the AL1 bridge r<=1/8 <=> tau<=3 <=>
    g^4>=32, the route-B contraction constants (J'=29|tau|, G(1/64)<148/7, G'(1/64)<352 with exp(1/8)<8/7
    enclosed, cap J_0'=29/10^8) and the labelled, NOT admitted, route radii |tau|<=7/274688 and <1/20416;
  * the lattice-units gap floor (a*alpha/16)^2=g^4/1024>=9375000=(1250 sqrt 6)^2 in the admitted regime,
    hence no trajectory along which a_n*Delta_n->0 can stay in it;
  * the toy trajectory g_n=g_0/n: exact first indices n* with g_n^4<9.6x10^9 and g_n^4<32 for the
    declared g_0^4=9.6x10^9 and the panel rehearsal g_0=1000, by integer roots and brute force;
  * common rescaling (a->a/s at fixed g) leaves every admission ratio unchanged and multiplies the gap
    bound by s; an independent magnetic multiplier s obeys s<=g^4/32 at the bridge and s->0 as g->0;
  * a statement-packet validator, the continuum-requirements table and the 21 contract controls as
    damaging mutations (plus labelled extra controls).

Usage: python3 -B research/round32/skeptic/az1_check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as F
from math import factorial, isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PINS = (
    ('contract', 'research/round32/contracts/az1.json',
     '91c828a7aa6ef9bd4d3dbf762363b7558faa6922c23e1aff476cd098d4177078'),
    ('ax1_gate', 'research/round32/advisor/ax1-gate.json',
     '1b8fb152696659439bb01fc7df429fc76fa3132d4936df450d8131256015d177'),
    ('al1_gate', 'research/round29/advisor/al1-gate.json',
     'e415203cc6b6ebca6cea5fcd1230a7eb0e20b7ab2d2e6c99dc8aa2dd3052a75b'),
    ('al1_report', 'research/round29/forward/al1/report.md',
     '967995f18ebda3abd1395b2775e0edd06d91c5d6ea7d6b3368d6be4850f39426'),
    ('am2_gate', 'research/round29/advisor/am2-gate.json',
     'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d'),
    ('am2_report', 'research/round29/forward/am2/report.md',
     '1b58fb9c1a199f06b156d04c2a9e89f34ba63cf675a5f7c8bfc25bb568e4e019'),
    ('ax1_forward', 'research/round32/forward/ax1/report.md',
     '2ba5e8360432755e87dab5a2c67c53617ce34494a394c3520e69818e20ce7a38'),
    ('ax1_reverse', 'research/round32/reverse/ax1/report.md',
     '9ffe3b4af78537a66e194c0d3669edd8f9a5df4a0069bd1d82bea13dad349e8e'),
    ('skeptic_ax1', 'research/round32/skeptic/ax1.md',
     '9729b61526c6c339f3d0a5793a35877fa9b93bf575d0aa4a25154d2f5abffda3'),
    ('modern_update4', 'research/round32/experts/modern/update-4.md',
     '5a0aa5077fe3e044f5c601c99cc7c978e50e54b075b869dd6d5ad659fbd0aadd'),
    ('modern_sota', 'research/round32/experts/modern/sota-table.md',
     '76f76994061579817c06cb4425a4dde888d844bcf220d1ca6875867cb2d33bd9'),
    ('selection', 'research/round32/advisor/selection-az1.md',
     'a2cf9d6ed4f4689f379bec479e5c8a7c9ef53c4dc656a9af0f478679cda7a60b'),
    ('agents', 'AGENTS.md', '870e1a6b1ff81d6e09888d7084dada2dfdb8128048d97857d9c6b1ffce1b9285'),
)
SHA = {name: digest for name, _, digest in PINS}

MODEL_ID = 'AQ_uniform_routeB along (a_n,g_n)'
MODEL_LABEL = 'uniform Kogut-Susskind SU(2) at fixed spacing, strong bare coupling'
UNIFORM_TRIPLE = ['tau/24', 'tau/24', 'tau/24']
CLOCK = 's=alpha*t_E/hbar, theta=alpha*t/hbar'
SCOPE = 'volume-uniform at fixed a, strong bare coupling'
R_COVER = [(0, 0, 0), (0, 0, 1)]
CAP_G4 = F(9600000000)
BRIDGE_G4 = F(32)
J0_PRIME = F(29, 10 ** 8)
REQ_ROWS = ('uniform_in_a_estimates', 'reconstruction_hypotheses', 'physical_scale_control')
EXTRA_ROWS = ('state_identification_at_fixed_a', 'nontriviality', 'observables_and_renormalization')
GATE_FALSE = ('continuum_claim', 'uniform_in_a_claimed', 'weak_coupling_claim', 'loop_count_fraction_claimed')
LEAD = 'Faizal-Shabir arXiv:2606.19362'


class Rejected(Exception):
    """Raised by a validator that refuses a packet; controls require it."""


class CheckFailure(RuntimeError):
    """Raised when a required check or control fails."""


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise CheckFailure(cid)
    if any(row['id'] == cid for row in CHECKS):
        raise CheckFailure('duplicate check id ' + cid)
    row = {'id': cid, 'passed': True}
    row.update(detail)
    CHECKS.append(row)


def rejects(fn, reason):
    try:
        fn()
    except Rejected as exc:
        if reason not in str(exc):
            raise CheckFailure('rejected for the wrong reason: %s (expected %s)' % (exc, reason))
        return True
    return False


def accepts(fn):
    try:
        fn()
    except Rejected:
        return False
    return True


def control(cid, mutations, positives=(), **detail):
    rows = []
    for label, fn, reason in mutations:
        if not rejects(fn, reason):
            raise CheckFailure('control %s: mutation %s accepted' % (cid, label))
        rows.append({'mutation': label, 'rejected_for': reason})
    pos = []
    for label, fn in positives:
        if not accepts(fn):
            raise CheckFailure('control %s: positive %s rejected' % (cid, label))
        pos.append(label)
    need(True, cid, kind='control', mutations=rows, positives=pos, **detail)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def q(x):
    return str(x)


def preview(x):
    return format(float(x), '.12e')


def sqrt_bracket(n, scale):
    """Directed rational bracket lo <= sqrt(n) <= hi with hi-lo <= 1/scale."""
    r = isqrt(n * scale * scale)
    lo = F(r, scale)
    hi = lo if r * r == n * scale * scale else F(r + 1, scale)
    if not (lo * lo <= n <= hi * hi and hi - lo <= F(1, scale) and lo >= 0):
        raise CheckFailure('sqrt bracket')
    return lo, hi


def exp_upper(x, terms=12):
    """Directed upper bound for exp(x), 0<=x<terms+2: Taylor sum plus geometric tail."""
    if not (0 <= x < terms + 2):
        raise CheckFailure('exp_upper domain')
    s = sum((x ** k / factorial(k) for k in range(terms + 1)), F(0))
    tail = x ** (terms + 1) / factorial(terms + 1) / (1 - x / (terms + 2))
    return s + tail


# ---------------------------------------------------------------- rational functions in G=g^2 and a
def pmul(p, r):
    out = {}
    for (i1, j1), c1 in p.items():
        for (i2, j2), c2 in r.items():
            k = (i1 + i2, j1 + j2)
            out[k] = out.get(k, F(0)) + c1 * c2
    return {k: v for k, v in out.items() if v != 0}


def padd(p, r, cr=1):
    out = dict(p)
    for k, v in r.items():
        out[k] = out.get(k, F(0)) + cr * v
    return {k: v for k, v in out.items() if v != 0}


class RF:
    """num/den with num, den polynomials {(deg_G, deg_a): Fraction}; identity test by cross-multiplication."""

    def __init__(self, num, den):
        if not den:
            raise CheckFailure('zero denominator')
        self.num, self.den = num, den

    @staticmethod
    def mono(coef, eg, ea):
        coef = F(coef)
        num = {(max(eg, 0), max(ea, 0)): coef} if coef != 0 else {}
        return RF(num, {(max(-eg, 0), max(-ea, 0)): F(1)})

    def __mul__(self, o):
        return RF(pmul(self.num, o.num), pmul(self.den, o.den))

    def __truediv__(self, o):
        if not o.num:
            raise CheckFailure('division by the zero rational function')
        return RF(pmul(self.num, o.den), pmul(self.den, o.num))

    def __sub__(self, o):
        return RF(padd(pmul(self.num, o.den), pmul(o.num, self.den), -1), pmul(self.den, o.den))

    def scale(self, c):
        c = F(c)
        return RF({k: v * c for k, v in self.num.items() if v * c != 0}, self.den)

    def same(self, o):
        return padd(pmul(self.num, o.den), pmul(o.num, self.den), -1) == {}

    def at(self, g2, a):
        def ev(p):
            return sum((c * F(g2) ** i * F(a) ** j for (i, j), c in p.items()), F(0))
        d = ev(self.den)
        if d == 0:
            raise CheckFailure('evaluation at a pole')
        return ev(self.num) / d


REF_DICT = {
    'alpha': (F(1, 2), 1, -1),       # g^2/(2a)
    'lambda': (F(2), -1, -1),        # 2/(g^2 a)
    'tau_ratio_coefficient': F(24),  # tau = 24 lambda/alpha (I1 selected/omitted face normalization)
    'delta_over_alpha': F(1, 8),
    'normalized_gap': F(1, 2),
    'claimed': {'alpha_over_16': (F(1, 32), 1, -1), 'tau': (F(96), -2, 0), 'alpha_lambda_a2': (F(1), 0, 0),
                'r': (F(4), -2, 0), 'local_norm_7tau': (F(672), -2, 0)},
}
SAMPLES = ((F(1), F(1)), (F(10 ** 5), F(1, 1000)), (F(3, 7), F(11, 5)), (F(97979), F(1)), (F(4, 9), F(10 ** 6)),
           (F(1, 10 ** 6), F(2, 3)))


def dictionary_identities(spec):
    """Every AZ1 identity as a rational-function identity in (G=g^2, a); returns {name: bool}."""
    alpha, lam = RF.mono(*spec['alpha']), RF.mono(*spec['lambda'])
    a_rf, g2 = RF.mono(1, 0, 1), RF.mono(1, 1, 0)
    cl = spec['claimed']
    tau = (lam / alpha).scale(spec['tau_ratio_coefficient'])
    delta = alpha.scale(spec['delta_over_alpha'])
    nu = (alpha * tau).scale(F(1, 24))
    out = {
        'alpha_over_16_equals_g2_over_32a': alpha.scale(F(1, 16)).same(RF.mono(*cl['alpha_over_16'])),
        'physical_gap_delta_times_normalized_gap': delta.scale(spec['normalized_gap']).same(
            RF.mono(*cl['alpha_over_16'])),
        'tau_equals_96_over_g4': tau.same(RF.mono(*cl['tau'])),
        'alpha_lambda_a2_equals_1': (alpha * lam * a_rf * a_rf).same(RF.mono(*cl['alpha_lambda_a2']))
                                    and RF.mono(*cl['alpha_lambda_a2']).same(RF.mono(1, 0, 0)),
        'r_equals_4_over_g4': (lam / alpha).same(RF.mono(*cl['r'])),
        'nu_equals_lambda': nu.same(lam),
        'nu_over_delta_equals_tau_over_3': (nu / delta).same(tau.scale(F(1, 3))),
        'local_norm_7tau_equals_672_over_g4': tau.scale(7).same(RF.mono(*cl['local_norm_7tau'])),
        'inverse_g4_equals_4alpha_over_lambda': (lam * g2 * g2).same(alpha.scale(4)),
    }
    return out


def dictionary_at_points(spec):
    ok = True
    for g2, a in SAMPLES:
        c = spec['alpha'][0] * g2 ** spec['alpha'][1] * a ** spec['alpha'][2]
        l_ = spec['lambda'][0] * g2 ** spec['lambda'][1] * a ** spec['lambda'][2]
        tau = spec['tau_ratio_coefficient'] * l_ / c
        ok = ok and c / 16 == g2 / (32 * a) and tau == 96 / g2 ** 2 and c * l_ * a * a == 1 and \
            c * spec['delta_over_alpha'] * spec['normalized_gap'] == g2 / (32 * a)
    return ok


# ---------------------------------------------------------------- toy-trajectory crossovers
def iroot(m, p):
    """floor(m^(1/p)) for an integer m >= 0, by bisection on exact integers."""
    if m < 0:
        raise CheckFailure('iroot of a negative integer')
    lo, hi = 0, 1
    while hi ** p <= m:
        hi *= 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if mid ** p <= m:
            lo = mid
        else:
            hi = mid
    return lo


def n_star(g0_4, threshold, power=4, strict=True):
    """First n>=1 with g_n^4 = g0_4/n^power below the threshold (strictly, unless strict=False)."""
    g0_4, threshold = F(g0_4), F(threshold)
    qv = g0_4 / threshold

    def below(n):
        v = g0_4 / F(n) ** power
        return v < threshold if strict else v <= threshold

    n = max(1, iroot(qv.numerator // qv.denominator, power))
    while not below(n):
        n += 1
    while n > 1 and below(n - 1):
        n -= 1
    if not (below(n) and (n == 1 or not below(n - 1))):
        raise CheckFailure('crossover definition')
    return n


def n_star_brute(g0_4, threshold, power=4, limit=10 ** 6):
    n = 1
    while F(g0_4) / F(n) ** power >= threshold:
        n += 1
        if n > limit:
            raise CheckFailure('brute-force crossover limit')
    return n


# ---------------------------------------------------------------- statement scans
def sentences(text):
    return [s for s in re.split(r'(?<=[.;])\s+', text) if s.strip()]


NEG_FRAME = re.compile(r"\bnot (a statement|a claim|claimed|asserted|shown|proved|established) that\b|"
                       r"\bno (claim|statement) that\b|\bdoes not (assert|claim|show|prove|establish) that\b")
CLAIM_PATTERNS = (
    ('the continuum limit exists', re.compile(r'\bthe continuum limit exists\b')),
    ('fraction of the problem', re.compile(r'\bfraction of the (\w+ )?problem\b|\bper ?cent of the\b|'
                                           r'\d+ ?% of\b|\b\d+ ?/ ?\d+ of the (\w+ )?(problem|proof)\b|'
                                           r'\b\d+ of \d+ of the (\w+ )?(problem|proof)\b')),
    ('the coupling is weak', re.compile(r'\bthe coupling is weak\b|\bat weak coupling the (gap|estimate) holds\b')),
)
MODEL_USE = re.compile(r'uniform (kogut|ks\b|model|hamiltonian|triple)|aq_uniform|uniform_in_n_claimed|'
                       r'uniform_in_a_claimed|uniform_label')
A_SENSE = re.compile(r'uniform(ly)?[ -](in[ -]a\b|in the lattice spacing|along a_n|along the trajectory)|'
                     r'uniform-in-a\b')
N_SENSE = re.compile(r'volume-uniform|uniform(ly)? in (n\b|the volume)|uniform-in-n\b')
NEGATOR = re.compile(r'\b(not|no|never|none|nor|fails|without)\b')
SCOPE_G0 = re.compile(r'g_n->0|g->0|g_n -> 0|named trajectory')


def uniform_tokens(sent):
    """Classify each 'uniform' token: 'N' (volume sense), 'a' (lattice-spacing sense) or 'bare'."""
    low = sent.lower()
    masked = MODEL_USE.sub(lambda m: '#' * len(m.group(0)), low)
    toks = []
    for m in re.finditer(r'uniform\w*', masked):
        start = m.start()
        if masked[max(0, start - 7):start] == 'volume-' or N_SENSE.match(masked, start):
            kind = 'N'
        elif A_SENSE.match(masked, start):
            kind = 'a'
        else:
            kind = 'bare'
        toks.append((kind, start))
    return masked, toks


def scan_statements(texts):
    for text in texts:
        for sent in sentences(text):
            masked, toks = uniform_tokens(sent)
            kinds = {k for k, _ in toks}
            if 'a' in kinds and 'bare' in kinds and 'N' not in kinds:
                raise Rejected('uniform senses share a sentence without the qualifier')
            for kind, start in toks:
                if kind == 'a':
                    prefix = masked[:start].replace('not only', '')
                    if not NEGATOR.search(prefix):
                        raise Rejected('uniform in a claimed')
                    if masked.startswith('uniform along a_n', start) and not SCOPE_G0.search(masked):
                        raise Rejected('failure not scoped to g_n->0: at fixed g the bound holds along a_n->0')
            low = sent.lower()
            for name, pat in CLAIM_PATTERNS:
                for m in pat.finditer(low):
                    if not NEG_FRAME.search(low[:m.start()]):
                        if name == 'fraction of the problem':
                            raise Rejected('loop count is not a fraction: forbidden phrasing')
                        raise Rejected('forbidden phrasing: ' + name)
    return True


# ---------------------------------------------------------------- reference tables
def reference_requirements():
    return [
        {'id': 'uniform_in_a_estimates', 'contract_row': True,
         'statement_missing': 'a lower bound on the physical gap in units of E_star, with locality and clustering '
                              'bounds, holding at every n along a trajectory with a_n->0 and g_n->0',
         'missing_premise': 'an estimate whose validity region contains g->0; the route-B contraction parameter '
                            'J\'=29|tau|=2784/g^4 grows without bound as g->0, so the AM2/AX1 fixed point and '
                            'gap exclusion cannot be continued there, and no premise supplies a weak-coupling '
                            'replacement',
         'candidate_route': 'a multiscale renormalization-group analysis (Balaban-type ultraviolet stability, '
                            'known for the Euclidean Wilson action in finite volume; not read here and not a '
                            'premise) re-derived for, or transferred with an identification theorem to, the '
                            'Kogut-Susskind family',
         'status': 'not_supplied'},
        {'id': 'reconstruction_hypotheses', 'contract_row': True,
         'statement_missing': 'the axioms of the limiting theory: Osterwalder-Schrader regularity, Euclidean '
                              'invariance, reflection positivity, symmetry and clustering for limits of '
                              'gauge-invariant Schwinger functions, or a Hamiltonian reconstruction with '
                              'identification maps between the lattice Hilbert spaces',
         'missing_premise': 'existence of the limits (tightness or convergence of correlation functions of '
                            'renormalized smeared observables), restoration of Euclidean (Poincare) invariance '
                            'from cubic lattice symmetry, and a mode of convergence that keeps the vacuum simple '
                            'and the gap open (strong-resolvent convergence alone does not)',
         'candidate_route': 'reflection positivity at each spacing (transfer matrix; OS positivity survives '
                            'limits) plus uniform-in-a moment and clustering bounds; none is available here',
         'status': 'not_supplied'},
        {'id': 'physical_scale_control', 'contract_row': True,
         'statement_missing': 'a trajectory along which a fixed physical quantity in units of E_star (the gap, or '
                              'a string tension) converges to a finite positive value while a_n->0, so '
                              'a_n*Delta_n->0',
         'missing_premise': 'a non-perturbative relation between a and g (the asymptotic-freedom form is a '
                            'hypothesis here) with two-sided bounds on the gap in units of E_star along it; in '
                            'the admitted regime a*Delta>=g^2/32>=1250*sqrt(6), about 3061.86, so no trajectory '
                            'with a_n*Delta_n->0 stays in it',
         'candidate_route': 'scale setting by a non-perturbatively bounded observable; asymptotic-freedom running '
                            'as the hypothesis to be verified, not assumed',
         'status': 'not_supplied'},
        {'id': 'state_identification_at_fixed_a', 'contract_row': False,
         'statement_missing': 'the six AY2 obligations (uniqueness, whole-sequence convergence, translation '
                              'invariance, a rate in N, boundary independence of dynamics, padded-family dynamics)',
         'missing_premise': 'unproved even at fixed a (AY2 gate); a continuum limit of states presupposes them',
         'candidate_route': 'as in the AY2 obligations table; not premises of AZ1',
         'status': 'not_supplied'},
        {'id': 'nontriviality', 'contract_row': False,
         'statement_missing': 'the limit is not a Gaussian (free) field',
         'missing_premise': 'any non-Gaussian estimate that survives a_n->0; the only rigorous non-Abelian d>2 '
                            'scaling limit in the SOTA table (Chatterjee, SU(2) Yang-Mills-Higgs) is Gaussian',
         'candidate_route': 'none in the premises',
         'status': 'not_supplied'},
        {'id': 'observables_and_renormalization', 'contract_row': False,
         'statement_missing': 'which operators converge (smeared Wilson loops, a renormalized field strength)',
         'missing_premise': 'operator renormalization with a-dependent normalization',
         'candidate_route': 'none in the premises',
         'status': 'not_supplied'},
    ]


def validate_requirements(rows):
    ids = [r.get('id') for r in rows]
    if len(ids) != len(set(ids)):
        raise Rejected('requirements table: duplicate row')
    for rid in REQ_ROWS:
        if rid not in ids:
            raise Rejected('requirements table: missing row ' + rid)
    for r in rows:
        for key in ('statement_missing', 'missing_premise', 'candidate_route'):
            if not isinstance(r.get(key), str) or len(r[key].strip()) < 12:
                raise Rejected('requirements table: empty %s in %s' % (key, r['id']))
        if r.get('status') != 'not_supplied':
            raise Rejected('requirements table: %s marked %s' % (r['id'], r.get('status')))
    return True


def validate_evidence(ev, required):
    digest = sha_bytes(json.dumps(ev['rows'], sort_keys=True).encode())
    if digest != ev['digest']:
        raise Rejected('evidence digest mismatch')
    ids = {r['id']: r for r in ev['rows']}
    for cid in required:
        if cid not in ids:
            raise Rejected('missing required control ' + cid)
        if ids[cid].get('passed') is not True:
            raise Rejected('required control not passed ' + cid)
    return True


def is_exact(v):
    return isinstance(v, (F, int)) and not isinstance(v, bool)


# ---------------------------------------------------------------- the statement-packet validator
def validate(pk, c):
    if pk['contract_sha256'] != SHA['contract']:
        raise Rejected('contract hash')
    if pk['ax1_gate_sha256'] != SHA['ax1_gate']:
        raise Rejected('AX1 gate hash')
    if pk['al1_gate_sha256'] != SHA['al1_gate']:
        raise Rejected('AL1 gate hash')
    exact = [pk['cap']['tau'], pk['cap']['g4'], pk['bridge']['g4'], pk['estimate']['value_over_alpha'],
             pk['estimate']['normalized'], pk['estimate']['delta_over_alpha'], pk['toy']['g0_4'],
             pk['toy']['n_star_cap'], pk['toy']['n_star_bridge'], pk['toy']['rehearsal']['g0'],
             pk['toy']['rehearsal']['n_star_cap'], pk['toy']['rehearsal']['n_star_bridge'],
             pk['scale_control']['lattice_gap_floor_sq'], pk['first_order_mean']['over_tau'],
             pk['admitted_tau_cap'], pk['identities_value']['alpha_lambda_a2']]
    exact += [x for v in pk['dictionary'].values() if isinstance(v, tuple) for x in v]
    exact += [x for v in pk['dictionary']['claimed'].values() for x in v]
    if any(not is_exact(v) for v in exact):
        raise Rejected('exact arithmetic')
    if pk['identity_method'] != 'rational-function identity':
        raise Rejected('exact arithmetic: identities must be proved as rational-function identities')
    if pk['model_id'] != MODEL_ID or pk['selected_triple'] != UNIFORM_TRIPLE:
        raise Rejected('changed model relabelled')
    if pk['cap']['tau'] != c['tau'] or pk['toy']['g0_4'] != c['g0_4']:
        raise Rejected('changed model relabelled')
    if pk['toy']['rule'] != 'g_n=g_0/n':
        raise Rejected('changed model relabelled: toy trajectory is g_n=g_0/n')
    lab = pk['model_label']
    if 'fixed spacing' not in lab or 'strong bare coupling' not in lab or 'weak' in lab or 'continuum' in lab:
        raise Rejected('uniform label: strong coupling at fixed spacing')
    if pk['per_site_sum_over_tau'] != 29 or pk['stars_meeting_R'] != 7 or pk['single_groups_meeting_R'] != 2:
        raise Rejected('incident stars')
    if pk['cap']['tau'] != J0_PRIME / pk['per_site_sum_over_tau']:
        raise Rejected('incident stars: cap not J_0\'/29')
    if pk['cover'] != R_COVER or pk['cover_links'] != 48 or pk['cover_endpoints'] != 36:
        raise Rejected('cover')
    if pk['clock'] != CLOCK:
        raise Rejected('clock or unit mixing')
    est = pk['estimate']
    if est['delta_over_alpha'] != F(1, 8) or est['normalized'] != F(1, 2) or \
            est['value_over_alpha'] != est['delta_over_alpha'] * est['normalized']:
        raise Rejected('clock or unit mixing: gap is (alpha/8)(1/2)=alpha/16')
    if est['units'] != 'energy, with E_star and hbar fixed' or est['uniform_in_clock_units_claimed']:
        raise Rejected('clock or unit mixing: moving clock')
    if est['centering'] != 'vector (actual ground)' or est['reference'] != 'actual ground energy':
        raise Rejected('centering: actual ground, not the scalar lambda N_p')
    fom = pk['first_order_mean']
    if fom['over_tau'] != F(1, 144) or fom['charged'] is not True or fom['extrapolated_to_weak_coupling']:
        raise Rejected('first-order mean')
    if pk['exponents'] != {'tau_in_g': -4, 'gap_in_g': 2, 'gap_in_a': -1}:
        raise Rejected('tau scaling exponent')
    ids = dictionary_identities(pk['dictionary'])
    if not all(ids.values()) or not dictionary_at_points(pk['dictionary']):
        raise Rejected('dictionary arithmetic: %s' % sorted(k for k, v in ids.items() if not v))
    if pk['dictionary'] != c['dictionary']:
        raise Rejected('dictionary arithmetic: not the AL1 dictionary')
    if pk['identities_value']['alpha_lambda_a2'] != 1:
        raise Rejected('dictionary arithmetic: alpha*lambda*a^2')
    if pk['cap']['g4'] != 96 / pk['cap']['tau']:
        raise Rejected('dictionary arithmetic: cap g^4=96/tau')
    if pk['admitted_tau_cap'] != c['tau']:
        raise Rejected('route constant is not the admitted cap')
    tr = pk['trajectory']
    if tr.get('named') is not True or tr.get('status') != 'hypothesis' or tr.get('derived') is not False \
            or tr.get('g_to_zero') is not True or 'g_n->0 as a_n->0' not in tr.get('form', ''):
        raise Rejected('trajectory named: (a_n,g_n) with g_n->0 as a hypothesis')
    if pk['toy']['label'] != 'toy' or pk['toy']['asymptotic_freedom_form'] is not False:
        raise Rejected('trajectory named: toy trajectory labelled toy, not of asymptotic-freedom form')
    if est['count'] != 1 or est['name'] != 'volume-uniform gap' or est['formula'] != 'alpha/16=g^2/(32a)':
        raise Rejected('one uniform estimate identified')
    if est['source'] != 'AX1 gate' or est['cited_not_rederived'] is not True:
        raise Rejected('one uniform estimate identified: cite the AX1 gate')
    if est['regime_g4_min'] != CAP_G4 or est['uniform_in'] != 'N (volume) at fixed a':
        raise Rejected('uniform in N, not in a: estimate scope')
    fl = pk['failure']
    if fl['uniform_along_a_supplied'] is not False or fl['eventual'] is not True or \
            sorted(fl['reasons']) != ['am2_cap', 'bridge']:
        raise Rejected('bridge obstruction retained: failure statement')
    if fl['kind'] != 'failure of a sufficient certificate' or fl['actual_gap_failure_claimed'] is not False:
        raise Rejected('failure is of a sufficient certificate, not a gap')
    br = pk['bridge']
    if br['g4'] != BRIDGE_G4 or br['retained'] is not True or br['satisfied_along_trajectory'] is not False:
        raise Rejected('bridge obstruction retained')
    if pk['common_rescaling']['repairs_bridge'] is not False or \
            pk['common_rescaling']['invariant'] != 'lambda/alpha=4/g^4':
        raise Rejected('bridge obstruction retained: common rescaling cannot repair it')
    toy = pk['toy']
    if toy['power'] != 4:
        raise Rejected('root-N misuse: g_n=g_0/n gives g_n^4=g_0^4/n^4')
    if toy['strict'] is not True:
        raise Rejected('toy crossover: strict inequality')
    if toy['n_star_cap'] != n_star(toy['g0_4'], CAP_G4) or toy['n_star_bridge'] != n_star(toy['g0_4'], BRIDGE_G4):
        raise Rejected('toy crossover')
    rh = toy['rehearsal']
    if rh['n_star_cap'] != n_star(F(rh['g0']) ** 4, CAP_G4) or \
            rh['n_star_bridge'] != n_star(F(rh['g0']) ** 4, BRIDGE_G4) or rh['g0'] != 1000:
        raise Rejected('toy crossover: rehearsal g_0=1000')
    if toy['method'] != 'exact integer comparison':
        raise Rejected('toy crossover: exact integer comparison')
    es = pk['e_star']
    if es['fixed'] is not True or es['positive'] is not True or es['moving'] is not False or pk['plateau_fit']:
        raise Rejected('E_star fixed, no plateau')
    sc = pk['scale_control']
    if sc['lattice_gap_floor_sq'] != CAP_G4 / 1024 or sc['admitted_regime_hosts_finite_mass_trajectory']:
        raise Rejected('physical scale control')
    gf = pk['gate_fields']
    for key in GATE_FALSE:
        if key not in gf:
            raise Rejected('gate field missing: ' + key)
        if gf[key] is not False:
            if key == 'uniform_in_a_claimed':
                raise Rejected('uniform in a claimed (gate field)')
            if key == 'loop_count_fraction_claimed':
                raise Rejected('loop count is not a fraction (gate field)')
            raise Rejected('forbidden claim ' + key)
    if gf.get('uniform_in_N_claimed') is not True:
        raise Rejected('gate field: uniform_in_N_claimed must be true')
    if gf.get('uniform_in_N_scope') != SCOPE:
        raise Rejected('uniform in N, not in a: scope string')
    for key in ('scientific_priority_verified', 'lead_imported_as_premise'):
        if pk['claims'].get(key) is not False:
            raise Rejected('forbidden claim ' + key)
    ld = pk['lead']
    if ld['id'] != LEAD or ld['status'] != 'unaudited lead' or ld['changes_statement'] is not False or \
            ld['disclosed_with_search_sentence'] is not True:
        raise Rejected('lead not premise')
    search = [t for t in pk['statements'] if 'source search' in t]
    if not search or not all('2606.19362' in t and 'unaudited' in t for t in search):
        raise Rejected('lead not premise: the source-search sentence must disclose the unaudited lead')
    if pk['loop_count'] != {'investigation': 9, 'of': 10, 'as_fraction_of_problem': False}:
        raise Rejected('loop count is not a fraction')
    if pk['sentence'] != c['sentence']:
        raise Rejected('mandatory sentence template')
    if c['sentence'] not in pk['statements']:
        raise Rejected('mandatory sentence template: not in the report statements')
    scan_statements(pk['statements'])
    validate_requirements(pk['requirements'])
    if pk['retained']['al1_path'] != 'violates the bridge for every n>=1' or pk['retained']['al1_path_n_star'] != 1:
        raise Rejected('insufficient verdict retained: AL1 path failure relabelled')
    dict_exact = all(ids.values())
    if pk['overclaim_found']:
        need_v = 'insufficient'
    elif est['proof_citation'] and dict_exact:
        need_v = 'accepted_within_scope'
    else:
        need_v = 'limited'
    if pk['verdict'] != need_v:
        raise Rejected('insufficient verdict retained: verdict must be ' + need_v)
    return True


# ---------------------------------------------------------------- execute
def execute():
    blobs = {}
    for name, rel, digest in PINS:
        b = (ROOT / rel).read_bytes()
        got = sha_bytes(b)
        need(got == digest, name + '_sha256_pinned', path=rel, sha256=got)
        blobs[name] = b
    checker_sha = sha_bytes(Path(__file__).read_bytes())
    con = json.loads(blobs['contract'])
    ax1 = json.loads(blobs['ax1_gate'])
    al1 = json.loads(blobs['al1_gate'])
    am2g = json.loads(blobs['am2_gate'])
    text = {k: blobs[k].decode('utf-8') for k in ('al1_report', 'am2_report', 'ax1_forward', 'ax1_reverse',
                                                  'modern_update4', 'modern_sota', 'selection', 'skeptic_ax1')}
    pre = con['preregistration']
    req = con['required']
    template = pre['mandatory_sentence_template']

    # 0. the frozen contract, read
    tau = F(pre['tau']['value'])
    need(con['id'] == 'AZ1' and con['status'] == 'frozen_before_production' and tau == F(1, 10 ** 8)
         and pre['model_id'] == MODEL_ID and con['producers'] == ['forward']
         and con['direction'] == 'statement+skeptic' and pre['direction'] == 'statement+skeptic'
         and con['single_direction_independent_replay'] is True and con['reverse_premise_isolation'] is False
         and con['selected_after'] == 'research/round32/advisor/ay2-gate.json',
         'contract_statement_loop_read', tau=q(tau), selected_after=con['selected_after'])
    need(con['controls'] == pre['controls_required']['ids'] and len(con['controls']) == 21
         and len(set(con['controls'])) == 21
         and all(x in con['controls'] for x in ('uniform_in_N_not_in_a', 'dictionary_arithmetic_exact',
                                                'toy_trajectory_crossover_exact')),
         'contract_control_mirror', controls=21, mirror=21)
    inventory = sorted(['AGENTS.md', 'research/round32/contracts/az1.json'] + list(con['shared_premises']))
    need(len(con['shared_premises']) == 27 and len(set(inventory)) == 29
         and all(rel in inventory for _, rel, _ in PINS)
         and 'research/round29/advisor/al2-gate.json' not in inventory
         and 'research/round32/contracts/ax1.json' not in inventory
         and 'research/round32/advisor/ay2-gate.json' not in inventory,
         'contract_inventory_29_derivable', inventory=len(inventory),
         pinned_here=[rel for _, rel, _ in PINS],
         not_snapshotted=['research/round29/advisor/al2-gate.json (common rescaling, AL2)',
                          'research/round32/contracts/ax1.json', 'research/round32/advisor/ay2-gate.json'])
    tgt = pre['target']
    need(tgt['value'] == '1' and tgt['comparator'] == '>=' and 'feasibility' in tgt['note']
         and 'not a blind discovery threshold' in tgt['note'], 'contract_target_is_feasibility_check',
         reading='target met iff every dictionary identity holds exactly and both crossover indices are computed; '
                 'met by construction, non-discriminating')
    need(pre['selected_triple_alpha_units'] == ['0', '0', '0'] and pre['model_id'] == MODEL_ID,
         'contract_selected_triple_defect',
         finding='non-blocking: the preregistration carries the zero triple of the patterned family under the '
                 'uniform route-B model id; the AX1 contract and gate use the symbolic uniform triple '
                 "['tau/24','tau/24','tau/24'], which this validator requires")
    need(sorted(pre['gate_fields_required']) == sorted(GATE_FALSE)
         and all(v is False for v in pre['gate_fields_required'].values())
         and 'uniform_in_N_claimed true' in req[4] and "'volume-uniform at fixed a, strong bare coupling'" in req[4],
         'contract_gate_fields_partial',
         finding='non-blocking: gate_fields_required lists four false fields; item 5 adds uniform_in_N_claimed '
                 'true with the scope string; export all five')
    low_t = template.lower()
    need('the continuum limit exists' in low_t and 'fraction of the problem' not in low_t
         and 'fraction of the continuum problem' in low_t and 'at fixed a' not in low_t
         and 'exactly one uniform estimate' in template and 'volume-uniform' in template,
         'contract_template_readings',
         findings=['the forbidden phrase "the continuum limit exists" occurs verbatim inside the template, '
                   'negated: a literal phrase scan rejects the mandatory sentence, so the scan must allow a '
                   'negated frame', 'the literal "fraction of the problem" misses the template\'s "fraction '
                   'of the continuum problem" and "90% of the problem"-type phrasings: scan by pattern',
                   'the template omits "at fixed a"; the gate scope string supplies it',
                   '"exactly one uniform estimate" counts the one necessary estimate identified, not every '
                   'volume-uniform bound AX1 admits (D\'_ii, the reset, the Nachtergaele-Sims constants are '
                   'volume-uniform too)'])
    need(pre['forbidden_phrasings'] == ['the continuum limit exists', 'fraction of the problem'] and
         accepts(lambda: scan_statements([template])), 'template_passes_negation_aware_scan')
    need('satisfying either bound uniformly was found' in req[2] and 'g_n=g_0/n at fixed E_star' in req[2],
         'contract_item3_readings',
         findings=['no sequence g_n->0 satisfies g_n^4>=c for all n, for any c>0: the "not found" sentence is '
                   'a tautology of the regime\'s shape, not a search result; the substantive statement is that '
                   'no premise supplies an estimate valid at weak coupling',
                   'the toy trajectory declares no a_n: the crossover indices are a-independent, the gap in '
                   'physical units along it is not determined',
                   'the source search did find a claimed construction (Faizal-Shabir, unaudited); the sentence '
                   'must be accompanied by that disclosure'])
    need('AM2 contraction needs tau<=10^-8' in req[1] and 'violated on every g->0 path' in req[1],
         'contract_item2_reading',
         reading='"needs" reads "is admitted only for": the frozen cap J_0\'=29/10^8 gives |tau|<=10^-8; the AX1 '
                 'route radii (7/274688, 1/20416) are not admitted; "violated on every g->0 path" means '
                 'eventually violated')
    need(pre['tau']['signs_evaluated'] == ['+', '-'], 'contract_signs_reading',
         reading='tau=96/g^4>0 for real g; -tau is the U_E mirror (AX1 gate), not a real-g trajectory point')

    # 1. pinned premise statements (cite, do not re-derive)
    acc = ax1['accepted']
    need(ax1['verdict'] == 'accepted_within_scope'
         and 'AL1 dictionary tau=96/g^4, so g^4=9.6x10^9 at the cap; never weak coupling or continuum' in acc
         and 'full-space gap >=1/2 normalized (alpha/16 physical)' in acc
         and "J_0'G(R)<1073/175000000<1/64 and 2J_0'G'(R)<319/1562500<1" in acc
         and 'the gap alpha/16' in acc and 're-frozen J_0\'=29/10^8' in acc
         and any('g^4>=9.6x10^9, |tau|<=10^-8' in lim for lim in ax1['limitations']),
         'ax1_gate_supplies_the_estimate',
         item='AX1 gate accepted (2): every finite complete-factor route-B volume has a unique gauge-invariant '
              'ground and full-space gap >=1/2 normalized (alpha/16 physical); (3): the gap alpha/16 re-applies '
              'to AQ subsequential limits')
    for name, rel, digest in PINS:
        if name in ('ax1_forward', 'ax1_reverse', 'skeptic_ax1', 'al1_gate', 'al1_report', 'am2_gate',
                    'am2_report', 'agents'):
            if ax1['bindings'].get(rel) != digest:
                raise CheckFailure('ax1 gate binding ' + rel)
    need(True, 'ax1_gate_bindings_match_pins')
    need('The actual selected bridge requires g^4>=32' in al1['accepted']
         and 'violates this sufficient condition for every n>=1' in al1['accepted']
         and any('failure of a specified sufficient certificate' in lim for lim in al1['limitations'])
         and 'test common scale changes' in al1['decision'], 'al1_gate_bridge_and_path')
    rep = text['al1_report']
    need(r'\alpha={g^2\over2a},\qquad\lambda={2\over g^2a},\qquad r={\lambda\over\alpha}={4\over g^4}.' in rep
         and r'\tau={24\lambda\over\alpha}={96\over g^4}' in rep and r'\epsilon=7|\tau|={672\over g^4}' in rep
         and r'r\le\tfrac18\quad\hbox{(bridge)}' in rep and 'H_KS = (alpha/8) H_tilde' in rep,
         'al1_report_dictionary_strings')
    need('both signs of |tau|<=1/100000000' in am2g['accepted'] and 'physical gap at least alpha/16' in am2g['accepted']
         and 'It does not interpret rejection beyond the chosen cap as actual gap failure.' in text['am2_report'],
         'am2_cap_is_sufficient_not_necessary')
    fw = text['ax1_forward']
    need(r'\Delta_{\rm physical}\ge\frac{\alpha}{8}\cdot\frac12=\frac{\alpha}{16}' in fw
         and '`|tau|<=7/274688`' in fw and '`|tau|<1/20416`' in fw
         and 'The physical gap `alpha/16` equals `g^2/(32a)`.' in text['ax1_reverse'],
         'ax1_reports_gap_and_route_radii')
    sota = text['modern_sota']
    need('Faizal-Shabir arXiv:2606.19362' in sota and 'abstract-depth reading only' in sota
         and 'first fails at **`n*=4`**' in text['modern_update4']
         and 'first fails at **`n*=421`**' in text['modern_update4'], 'modern_lens_lead_and_rehearsal_read')

    # 2. dictionary identities as rational-function identities
    ids = dictionary_identities(REF_DICT)
    need(all(ids.values()) and len(ids) == 9, 'dictionary_rational_function_identities',
         identities=sorted(ids), variables='G=g^2, a (independent indeterminates)',
         method='num1*den2-num2*den1 is the zero polynomial')
    need(dictionary_at_points(REF_DICT), 'dictionary_at_exact_sample_points',
         samples=[[q(g), q(a)] for g, a in SAMPLES])
    wrong = dict(REF_DICT)
    wrong['alpha'] = (F(1), 1, -1)
    val = (RF.mono(1, 1, -1) * RF.mono(2, -1, -1) * RF.mono(1, 0, 1) * RF.mono(1, 0, 1)).at(7, F(3, 5))
    need(val == 2 and not dictionary_identities(wrong)['alpha_lambda_a2_equals_1'],
         'cross_identity_discriminates', note='alpha=g^2/a gives alpha*lambda*a^2=2 identically')
    tau_cap_g4 = 96 / tau
    need(tau_cap_g4 == CAP_G4 and F(96) / BRIDGE_G4 == 3 and F(4) / BRIDGE_G4 == F(1, 8)
         and F(4) / 8 == F(1, 2) and F(96) / F(8) == 12,
         'admitted_regime_and_bridge_in_g', cap_g4=q(tau_cap_g4), bridge='r<=1/8 <=> tau<=3 <=> g^4>=32',
         ends='r<=1/2 <=> g^4>=8', monotone='tau*g^4=96, so tau<=10^-8 <=> g^4>=9.6x10^9')

    # 3. route-B contraction constants (recomputed) and the labelled, non-admitted route radii
    e18 = exp_upper(F(1, 8))
    g_r = 16 * e18 * (1 + F(10, 64))
    gp_r = 16 * e18 * (18 + F(80, 64))
    need(e18 < F(8, 7) and g_r < F(148, 7) and gp_r < 352 and J0_PRIME * F(148, 7) == F(1073, 175000000)
         and F(1073, 175000000) < F(1, 64) and 2 * J0_PRIME * 352 == F(319, 1562500) and F(319, 1562500) < 1
         and J0_PRIME / 29 == tau, 'route_b_contraction_recomputed', exp_one_eighth_upper=q(e18),
         J0_prime=q(J0_PRIME), per_site='J\'=4*7|tau|+|tau|=29|tau|')
    self_map = F(1, 64) / (29 * F(148, 7))
    exclusion = F(1, 2 * 29 * 352)
    g4_route = 96 / self_map
    need(self_map == F(7, 274688) and exclusion == F(1, 20416) and self_map < exclusion
         and g4_route == F(26370048, 7) and self_map / tau > 2548 and 29 * 96 == 2784,
         'route_radii_labelled_not_admitted', self_map_radius=q(self_map), exclusion_radius=q(exclusion),
         g4_route=q(g4_route), J_prime_in_g='29|tau|=2784/g^4',
         note='AX1 forward prints these radii; they are not frozen or reviewed and are never the admitted cap')

    # 4. lattice-units gap floor and physical scale control
    s6_lo, s6_hi = sqrt_bracket(6, 10 ** 40)
    floor_sq = CAP_G4 / 1024
    need(floor_sq == 9375000 and 1250 ** 2 * 6 == 9375000 and (1250 * s6_lo) ** 2 <= floor_sq <= (1250 * s6_hi) ** 2
         and F(3061) < 1250 * s6_lo and 1250 * s6_hi < F(3062), 'lattice_units_gap_floor',
         formula='(a*alpha/16)^2=g^4/1024>=9375000=(1250 sqrt 6)^2 on g^4>=9.6x10^9',
         floor_bracket=[q(1250 * s6_lo), q(1250 * s6_hi)])
    need(CAP_G4 / 4 == 2400000000 and (20000 * s6_lo) ** 2 <= 2400000000 <= (20000 * s6_hi) ** 2
         and BRIDGE_G4 / 1024 == F(1, 32), 'scale_control_incompatibility',
         statement='on the admitted regime (alpha*a)^2=g^4/4>=2.4x10^9 and a*Delta>=1250 sqrt 6; any trajectory '
                   'with a_n->0 and a_n*Delta_n->0 leaves it after finitely many n; even a hypothetical gap bound '
                   'alpha/16 on the whole bridge region would give (a*Delta)^2>=1/32')
    hbar_c = F(1973269804, 10 ** 7)       # MeV fm (CODATA 2018 value 197.3269804), illustration only
    ex_gap = F(10 ** 5) / (32 * F(1, 10)) * hbar_c
    need(F(10 ** 5) ** 2 >= CAP_G4 and 96 / F(10 ** 10) <= tau and ex_gap == 31250 * hbar_c
         and F(6166468) < ex_gap < F(6166469) and F(10 ** 5) / 32 == 3125,
         'physical_units_example', g2=q(10 ** 5), a_fm='1/10', gap_MeV=q(ex_gap), lattice_units='a*Delta>=3125',
         label='illustration of units only: no scale setting identifies a=0.1 fm with g^2=10^5')
    cap_gap_lo, cap_gap_hi = 1250 * s6_lo * hbar_c * 10, 1250 * s6_hi * hbar_c * 10
    need(F(6041880) < cap_gap_lo <= cap_gap_hi < F(6041881), 'physical_units_example_at_cap',
         gap_MeV_bracket=[q(cap_gap_lo), q(cap_gap_hi)], a_fm='1/10')
    alpha_v, hbar_v = F(5), F(7)
    need((alpha_v / 16) / hbar_v == F(5, 112) and (F(1, 2)) / hbar_v == F(1, 14) and F(5, 112) != F(1, 14),
         'clock_nonunit_fixture', physical_frequency='alpha/(16 hbar)=5/112',
         normalized_misread='(1/2)/hbar=1/14 (the eightfold-type clock error)')

    # 5. toy trajectory crossovers, exact
    g0_4 = F(96, 10) * 10 ** 9
    tstr = con['parameters']['toy_trajectory']
    need(g0_4 == CAP_G4 and 'g_0^4=9.6x10^9 (the cap) declared' in tstr and 'g_n=g_0/n' in tstr,
         'toy_trajectory_declared', g0_4=q(g0_4))
    table = {}
    for tag, g04 in (('declared', g0_4), ('rehearsal_g0_1000', F(10 ** 12))):
        row = {}
        for thr_tag, thr in (('cap', CAP_G4), ('bridge', BRIDGE_G4), ('ends_labelled', F(8)),
                             ('route_radius_labelled', g4_route), ('first_order_mean_exceeds_1_labelled', F(2, 3))):
            n1 = n_star(g04, thr)
            n2 = n_star_brute(g04, thr)
            if n1 != n2:
                raise CheckFailure('crossover methods disagree')
            prev = g04 / F(n1 - 1) ** 4 if n1 > 1 else None
            row[thr_tag] = {'n_star': n1, 'g4_at_n_star': q(g04 / F(n1) ** 4),
                            'g4_before': q(prev) if prev is not None else None}
        table[tag] = row
    d, r_ = table['declared'], table['rehearsal_g0_1000']
    need(d['cap']['n_star'] == 2 and d['bridge']['n_star'] == 132 and r_['cap']['n_star'] == 4
         and r_['bridge']['n_star'] == 421 and 131 ** 4 == 294499921 and 132 ** 4 == 303595776
         and 131 ** 4 < 300000000 < 132 ** 4 and 420 ** 4 < 31250000000 < 421 ** 4
         and 3 ** 4 < F(625, 6) < 4 ** 4 and g0_4 / 1 == CAP_G4, 'toy_trajectory_crossovers_exact',
         declared={'cap': 2, 'bridge': 132}, rehearsal_g0_1000={'cap': 4, 'bridge': 421},
         definition='n* = min{n>=1 : g_0^4/n^4 < threshold}, strict; at n=1 the declared trajectory sits exactly '
                    'on the cap (admitted)', table=table)
    need(d['ends_labelled']['n_star'] == 187 and r_['ends_labelled']['n_star'] == 595
         and d['route_radius_labelled']['n_star'] == 8 and r_['route_radius_labelled']['n_star'] == 23
         and d['first_order_mean_exceeds_1_labelled']['n_star'] == 347
         and r_['first_order_mean_exceeds_1_labelled']['n_star'] == 1107, 'toy_labelled_extra_crossovers',
         label='labelled only: ends r<=1/2; the non-admitted route radius; tau/144=2/(3g^4)>1')
    need(n_star(g0_4, CAP_G4, strict=False) == 1 and n_star(g0_4, BRIDGE_G4, power=2) == 17321
         and n_star(F(10 ** 12), BRIDGE_G4, power=2) == 176777 and n_star(F(10 ** 6), BRIDGE_G4, power=2) == 177,
         'toy_crossover_misreadings_discriminate',
         non_strict_cap=1, power2_bridge={'declared': 17321, 'g0_1000': 176777},
         g2_compared_to_32_g0_1000=177)
    al1_path = [96 * n * n for n in range(1, 6)]           # tau_n for a_n=a0/n, g_n^2=1/n
    need(all(t > 3 for t in al1_path) and n_star(1, BRIDGE_G4, power=2) == 1, 'al1_path_retained',
         path='a_n=a0/n, g_n^2=1/n: tau_n=96n^2>3 for every n>=1 (bridge violated at every n), alpha_n fixed')

    # 6. common rescaling and an independent magnetic multiplier
    g2f, af, s = F(10 ** 5), F(1), F(7)
    al_ = RF.mono(F(1, 2), 1, -1)
    lm_ = RF.mono(2, -1, -1)
    need(al_.at(g2f, af / s) == s * al_.at(g2f, af) and lm_.at(g2f, af / s) == s * lm_.at(g2f, af)
         and (lm_ / al_).at(g2f, af / s) == (lm_ / al_).at(g2f, af) == 4 / g2f ** 2
         and al_.at(g2f, af / s) / 16 == s * g2f / (32 * af), 'common_rescaling_fixture',
         statement='(alpha,lambda)->(s alpha,s lambda) is a->a/s at fixed g: tau, r and every admission ratio '
                   'are unchanged, the gap bound is multiplied by s relative to fixed E_star')
    fixed = [F(10 ** 5) / (32 * F(1, n)) for n in range(1, 11)]          # a_n=1/n at fixed g^2=10^5
    need(all(fixed[i + 1] > fixed[i] for i in range(9)) and fixed[0] == 3125
         and all(F(1, n + 1) * fixed[n] == 3125 for n in range(10)), 'fixed_g_counterexample',
         statement='at fixed g^2=10^5 (admitted) and a_n=1/n the bound g^2/(32 a_n)=3125n holds at every n and '
                   'grows: "no estimate uniform along a_n->0" is false unless scoped to g_n->0; a_n*Delta>=3125 '
                   'stays fixed, so this is common rescaling, not a finite-mass limit')
    g4_132 = g0_4 / F(132) ** 4
    need(g4_132 / 32 < 1 and all(g0_4 / F(n) ** 4 / 32 > g0_4 / F(n + 1) ** 4 / 32 for n in range(1, 50))
         and F(10 ** 12) / F(421) ** 4 / 32 < 1, 'magnetic_multiplier_bound',
         statement='lambda->s lambda at fixed alpha changes g^4 to g^4/s; the bridge needs s<=g^4/32, which '
                   'is below 1 from n*=132 on the declared toy trajectory and tends to 0 as g->0 (AL2 form, '
                   'derived here from the dictionary; AL2 gate not snapshotted)', s_max_at_n132=q(g4_132 / 32))

    # 7. validator, requirements table and controls
    ctx = {'tau': tau, 'g0_4': g0_4, 'sentence': template, 'dictionary': REF_DICT}
    statements = [
        template,
        'On every trajectory with g_n->0 the admitted regime g^4>=9.6x10^9 at fixed a is eventually left, so no '
        'estimate uniform along a_n->0 is supplied on it; this is failure of a sufficient certificate, not a '
        'no-gap theorem.',
        'On the toy trajectory g_n=g_0/n with g_0^4=9.6x10^9 (declared), g_n^4 first drops below 9.6x10^9 at '
        'n=2 and below the AL1 bridge threshold 32 at n=132; with the rehearsal value g_0=1000 the indices are 4 '
        'and 421.',
        'No rigorous construction of a genuine asymptotic-freedom trajectory satisfying either bound uniformly '
        'was found in this or any prior sub-round\'s source search; the claimed construction of Faizal and '
        'Shabir (arXiv:2606.19362) is recorded as an unaudited lead, not a premise.',
        'The gap alpha/16=g^2/(32a) is volume-uniform at fixed a and strong bare coupling, and it is not uniform '
        'in a.',
        'This is investigation 9 of 10 of Round32.',
    ]
    base = {
        'contract_sha256': SHA['contract'], 'ax1_gate_sha256': SHA['ax1_gate'], 'al1_gate_sha256': SHA['al1_gate'],
        'model_id': MODEL_ID, 'model_label': MODEL_LABEL, 'selected_triple': list(UNIFORM_TRIPLE),
        'per_site_sum_over_tau': 29, 'stars_meeting_R': 7, 'single_groups_meeting_R': 2,
        'cover': list(R_COVER), 'cover_links': 48, 'cover_endpoints': 36, 'clock': CLOCK,
        'dictionary': REF_DICT, 'identity_method': 'rational-function identity',
        'identities_value': {'alpha_lambda_a2': F(1)},
        'cap': {'tau': tau, 'g4': tau_cap_g4}, 'admitted_tau_cap': tau,
        'bridge': {'g4': BRIDGE_G4, 'retained': True, 'satisfied_along_trajectory': False, 'source': 'AL1 gate'},
        'common_rescaling': {'repairs_bridge': False, 'invariant': 'lambda/alpha=4/g^4'},
        'exponents': {'tau_in_g': -4, 'gap_in_g': 2, 'gap_in_a': -1},
        'trajectory': {'named': True, 'form': '(a_n,g_n) with g_n->0 as a_n->0', 'status': 'hypothesis',
                       'derived': False, 'g_to_zero': True},
        'estimate': {'count': 1, 'name': 'volume-uniform gap', 'formula': 'alpha/16=g^2/(32a)',
                     'value_over_alpha': F(1, 16), 'normalized': F(1, 2), 'delta_over_alpha': F(1, 8),
                     'units': 'energy, with E_star and hbar fixed', 'uniform_in_clock_units_claimed': False,
                     'centering': 'vector (actual ground)', 'reference': 'actual ground energy',
                     'source': 'AX1 gate', 'cited_not_rederived': True, 'regime_g4_min': CAP_G4,
                     'uniform_in': 'N (volume) at fixed a',
                     'proof_citation': 'AX1 gate accepted (2)-(3): AM2 with J_0\'=29/10^8, AQ2 gap alpha/16'},
        'failure': {'uniform_along_a_supplied': False, 'eventual': True, 'reasons': ['am2_cap', 'bridge'],
                    'kind': 'failure of a sufficient certificate', 'actual_gap_failure_claimed': False},
        'first_order_mean': {'over_tau': F(1, 144), 'charged': True, 'extrapolated_to_weak_coupling': False},
        'toy': {'rule': 'g_n=g_0/n', 'g0_4': g0_4, 'label': 'toy', 'asymptotic_freedom_form': False, 'power': 4,
                'strict': True, 'n_star_cap': 2, 'n_star_bridge': 132, 'method': 'exact integer comparison',
                'rehearsal': {'g0': 1000, 'n_star_cap': 4, 'n_star_bridge': 421}},
        'e_star': {'fixed': True, 'positive': True, 'moving': False}, 'plateau_fit': False,
        'scale_control': {'lattice_gap_floor_sq': CAP_G4 / 1024,
                          'admitted_regime_hosts_finite_mass_trajectory': False},
        'gate_fields': {'continuum_claim': False, 'uniform_in_a_claimed': False, 'weak_coupling_claim': False,
                        'loop_count_fraction_claimed': False, 'uniform_in_N_claimed': True,
                        'uniform_in_N_scope': SCOPE},
        'claims': {'scientific_priority_verified': False, 'lead_imported_as_premise': False},
        'lead': {'id': LEAD, 'status': 'unaudited lead', 'changes_statement': False,
                 'disclosed_with_search_sentence': True},
        'loop_count': {'investigation': 9, 'of': 10, 'as_fraction_of_problem': False},
        'sentence': template, 'statements': statements, 'requirements': reference_requirements(),
        'retained': {'al1_path': 'violates the bridge for every n>=1', 'al1_path_n_star': 1},
        'overclaim_found': False, 'verdict': 'accepted_within_scope',
    }
    need(accepts(lambda: validate(base, ctx)), 'reference_packet_accepted')

    nested = ('bridge', 'common_rescaling', 'exponents', 'trajectory', 'estimate', 'failure', 'first_order_mean',
              'toy', 'e_star', 'scale_control', 'gate_fields', 'claims', 'lead', 'loop_count', 'retained', 'cap',
              'identities_value')

    def mut(**kw):
        pk = dict(base)
        for key in nested:
            pk[key] = dict(base[key])
        pk['toy']['rehearsal'] = dict(base['toy']['rehearsal'])
        pk['requirements'] = [dict(r) for r in base['requirements']]
        pk['statements'] = list(base['statements'])
        for k, v in kw.items():
            if '.' in k:
                head, tail = k.split('.', 1)
                if '.' in tail:
                    mid, last = tail.split('.', 1)
                    pk[head][mid][last] = v
                else:
                    pk[head][tail] = v
            else:
                pk[k] = v
        return lambda: validate(pk, ctx)

    def add_stmt(s_):
        return mut(statements=base['statements'] + [s_])

    def dict_mut(**changes):
        dd = dict(REF_DICT)
        dd['claimed'] = dict(REF_DICT['claimed'])
        for k, v in changes.items():
            if k in dd['claimed']:
                dd['claimed'][k] = v
            else:
                dd[k] = v
        return mut(dictionary=dd)

    def req_edit(rid, **kw):
        rows = [dict(r) for r in base['requirements']]
        for r in rows:
            if r['id'] == rid:
                r.update(kw)
        return mut(requirements=rows)

    ok = [('reference packet', lambda: validate(base, ctx))]
    control('missing_incoming_stars',
            [('outgoing-only per-site sum 8', mut(per_site_sum_over_tau=8), 'incident stars'),
             ('selected single group dropped (28)', mut(per_site_sum_over_tau=28), 'incident stars'),
             ('orthant two stars', mut(stars_meeting_R=2), 'incident stars'),
             ('single groups forgotten', mut(single_groups_meeting_R=0), 'incident stars')], ok,
            semantics='the admitted cap is J_0\'/J\' with J\'=29|tau| (four incident stars and one single group per '
                      'site); a regime located from a smaller per-site sum is rejected')
    control('full_original_wilson_cover',
            [('R={0}', mut(cover=[(0, 0, 0)]), 'cover'), ('four drawn links', mut(cover_links=4), 'cover'),
             ('endpoints of the drawn loop', mut(cover_endpoints=4), 'cover')], ok)
    control('wrong_delta_alpha_hbar_clock',
            [('gap alpha/8 (normalized 1/2 dropped)', mut(**{'estimate.value_over_alpha': F(1, 8)}),
              'clock or unit mixing'),
             ('normalized gap 1/2 read in alpha units', mut(**{'estimate.delta_over_alpha': F(1)}),
              'clock or unit mixing'),
             ('u=s/8 clock', mut(clock='u=s/8'), 'clock or unit mixing'),
             ('gap 1/16 in theta units called uniform along the trajectory',
              mut(**{'estimate.uniform_in_clock_units_claimed': True}), 'moving clock'),
             ('gap in normalized G units', mut(**{'estimate.units': 'normalized G=H/delta'}), 'moving clock')], ok,
            fixture='alpha=5, hbar=7: alpha/(16 hbar)=5/112 versus the normalized misread 1/14')
    control('vector_versus_scalar_centering',
            [('scalar centering', mut(**{'estimate.centering': 'scalar'}), 'centering'),
             ('lambda N_p as the ground energy', mut(**{'estimate.reference': 'lambda N_p'}), 'centering')], ok)
    control('first_order_mean_charged',
            [('first-order mean dropped', mut(**{'first_order_mean.charged': False}), 'first-order mean'),
             ('density amplitude 1/72 as the mean', mut(**{'first_order_mean.over_tau': F(1, 72)}),
              'first-order mean'),
             ('tau/144=2/(3g^4) extrapolated to weak coupling',
              mut(**{'first_order_mean.extrapolated_to_weak_coupling': True}), 'first-order mean')], ok,
            note='tau/144=2/(3g^4) exceeds the bound |omega(W)|<=1 once g^4<2/3 (n=347 on the declared toy '
                 'trajectory): a fixed-a strong-coupling coefficient, never a weak-coupling value')
    control('tau_scaling_exponent',
            [('tau=96/g^2', mut(exponents={'tau_in_g': -2, 'gap_in_g': 2, 'gap_in_a': -1}), 'tau scaling'),
             ('gap g^4/a', mut(exponents={'tau_in_g': -4, 'gap_in_g': 4, 'gap_in_a': -1}), 'tau scaling'),
             ('gap g^2/a^2', mut(exponents={'tau_in_g': -4, 'gap_in_g': 2, 'gap_in_a': -2}), 'tau scaling'),
             ('dictionary tau exponent -1 in G', dict_mut(tau=(F(96), -1, 0)), 'dictionary arithmetic')], ok)
    control('changed_model_relabelled',
            [('patterned zero-selected model id', mut(model_id='AQ_patterned_zero_selected'), 'changed model'),
             ('zero triple under the uniform id', mut(selected_triple=['0', '0', '0']), 'changed model'),
             ('cap tau 10^-14', mut(cap={'tau': F(1, 10 ** 14), 'g4': F(96 * 10 ** 14)}), 'changed model'),
             ('declared g_0^4 changed silently', mut(**{'toy.g0_4': F(10 ** 12)}), 'changed model'),
             ('AL1 path relabelled as the toy trajectory', mut(**{'toy.rule': 'a_n=a0/n, g_n^2=1/n'}),
              'changed model')], ok,
            reading='the preregistration zero triple is a contract defect; the uniform triple is required')
    control('insufficient_verdict_retained',
            [('overclaim but accepted', mut(overclaim_found=True), 'verdict must be insufficient'),
             ('citation missing but accepted', mut(**{'estimate.proof_citation': ''}), 'verdict must be limited'),
             ('AL1 path relabelled passing', mut(**{'retained.al1_path': 'passes'}), 'insufficient verdict'),
             ('limited reported as accepted after a dictionary slip',
              mut(verdict='limited'), 'verdict must be accepted_within_scope')],
            ok + [('citation missing, verdict limited',
                   mut(**{'estimate.proof_citation': ''}, verdict='limited')),
                  ('overclaim, verdict insufficient', mut(overclaim_found=True, verdict='insufficient'))])
    control('exact_arithmetic_admission',
            [('float cap g^4', mut(cap={'tau': tau, 'g4': 9.6e9}), 'exact arithmetic'),
             ('float n*', mut(**{'toy.n_star_bridge': 132.0}), 'exact arithmetic'),
             ('bool as a number', mut(**{'toy.n_star_cap': True}), 'exact arithmetic'),
             ('float dictionary coefficient', dict_mut(alpha=(0.5, 1, -1)), 'exact arithmetic'),
             ('identities sampled in floating point', mut(identity_method='float sampling'), 'exact arithmetic')], ok)
    control('root_n_misuse',
            [('g_n=g_0/n read as g_n^2=g_0^2/n (power 2)', mut(**{'toy.power': 2, 'toy.n_star_bridge': 17321}),
              'root-N misuse'),
             ('power 2 with the power-4 indices kept', mut(**{'toy.power': 2}), 'root-N misuse')], ok,
            values={'power2_bridge_declared': 17321, 'power2_bridge_g0_1000': 176777})
    control('no_priority_or_continuum_claim',
            [('continuum flag', mut(**{'gate_fields.continuum_claim': True}), 'forbidden claim continuum_claim'),
             ('weak-coupling flag', mut(**{'gate_fields.weak_coupling_claim': True}),
              'forbidden claim weak_coupling_claim'),
             ('priority', mut(**{'claims.scientific_priority_verified': True}), 'forbidden claim scientific'),
             ('lead imported as premise', mut(**{'claims.lead_imported_as_premise': True}), 'forbidden claim lead'),
             ('continuum phrase', add_stmt('Along the named trajectory the continuum limit exists.'),
              'forbidden phrasing: the continuum limit exists'),
             ('false negation', add_stmt('It is not hard to see that the continuum limit exists.'),
              'forbidden phrasing: the continuum limit exists'),
             ('weak coupling phrase', add_stmt('For n>=132 the coupling is weak.'),
              'forbidden phrasing: the coupling is weak')], ok)
    control('trajectory_named',
            [('trajectory missing', mut(trajectory={}), 'trajectory named'),
             ('stated as derived', mut(**{'trajectory.derived': True}), 'trajectory named'),
             ('status theorem', mut(**{'trajectory.status': 'theorem'}), 'trajectory named'),
             ('fixed g named as the trajectory', mut(**{'trajectory.g_to_zero': False}), 'trajectory named'),
             ('toy not labelled', mut(**{'toy.label': 'trajectory'}), 'trajectory named: toy'),
             ('toy called asymptotic-freedom form', mut(**{'toy.asymptotic_freedom_form': True}),
              'trajectory named: toy')], ok)
    control('bridge_obstruction_retained',
            [('bridge dropped', mut(**{'bridge.retained': False}), 'bridge obstruction'),
             ('R18-B2 threshold 32/3', mut(**{'bridge.g4': F(32, 3)}), 'bridge obstruction'),
             ('bridge satisfied along the trajectory', mut(**{'bridge.satisfied_along_trajectory': True}),
              'bridge obstruction'),
             ('common rescaling repairs the bridge', mut(**{'common_rescaling.repairs_bridge': True}),
              'common rescaling'),
             ('only the cap reason', mut(**{'failure.reasons': ['am2_cap']}), 'bridge obstruction')], ok)
    control('one_uniform_estimate_identified',
            [('no estimate', mut(**{'estimate.count': 0}), 'one uniform estimate'),
             ('two estimates (D\'_ii as a gap estimate)', mut(**{'estimate.count': 2}), 'one uniform estimate'),
             ('wrong formula', mut(**{'estimate.formula': 'alpha/8=g^2/(16a)'}), 'one uniform estimate'),
             ('source AM2 gate (selected-strip model)', mut(**{'estimate.source': 'AM2 gate'}),
              'one uniform estimate'),
             ('re-derived, not cited', mut(**{'estimate.cited_not_rederived': False}), 'one uniform estimate'),
             ('regime from the route radius', mut(**{'estimate.regime_g4_min': g4_route}), 'estimate scope')], ok)
    control('e_star_fixed_no_plateau',
            [('moving reference E_star_n=alpha_n', mut(**{'e_star.moving': True}), 'E_star fixed'),
             ('E_star zero', mut(**{'e_star.positive': False}), 'E_star fixed'),
             ('plateau fit', mut(plateau_fit=True), 'E_star fixed')], ok)
    control('loop_count_not_fraction',
            [('flag', mut(**{'gate_fields.loop_count_fraction_claimed': True}), 'loop count is not a fraction'),
             ('9/10 of the continuum problem', add_stmt('Round32 settles 9/10 of the continuum problem.'),
              'loop count is not a fraction'),
             ('90%', add_stmt('Investigation 9 of 10 closes 90% of the problem.'), 'loop count is not a fraction'),
             ('fraction of the problem', add_stmt('The statement resolves a fraction of the problem.'),
              'loop count is not a fraction'),
             ('loop count as fraction', mut(loop_count={'investigation': 9, 'of': 10,
                                                        'as_fraction_of_problem': True}),
              'loop count is not a fraction')], ok)
    control('uniform_label_strong_coupling',
            [('weak coupling label', mut(model_label='uniform Kogut-Susskind SU(2) at fixed spacing, weak coupling'),
              'uniform label'),
             ('fixed spacing missing', mut(model_label='uniform Kogut-Susskind SU(2), strong bare coupling'),
              'uniform label'),
             ('continuum regime', mut(model_label=MODEL_LABEL + ', continuum regime'), 'uniform label')], ok)
    control('uniform_in_N_not_in_a',
            [('uniform_in_a_claimed true', mut(**{'gate_fields.uniform_in_a_claimed': True}), 'uniform in a claimed'),
             ('scope string without "at fixed a"',
              mut(**{'gate_fields.uniform_in_N_scope': 'volume-uniform, strong bare coupling'}), 'scope string'),
             ('uniform_in_N_claimed dropped', mut(**{'gate_fields.uniform_in_N_claimed': False}),
              'uniform_in_N_claimed'),
             ('estimate scope in a', mut(**{'estimate.uniform_in': 'N and a'}), 'estimate scope'),
             ('senses share a sentence', add_stmt('Along the named trajectory the family supplies exactly one uniform '
                                                  'estimate, the gap alpha/16, and fails to supply any estimate '
                                                  'uniform along a_n->0.'), 'share a sentence'),
             ('uniform in a asserted', add_stmt('The volume-uniform gap alpha/16 is uniform in a.'),
              'uniform in a claimed'),
             ('not only ... but also', add_stmt('The gap is not only volume-uniform but also uniform in a.'),
              'uniform in a claimed'),
             ('uniform along the trajectory', add_stmt('The gap alpha/16 stays uniform along the trajectory.'),
              'uniform in a claimed')], ok)
    control('dictionary_arithmetic_exact',
            [('alpha=g^2/a', dict_mut(alpha=(F(1), 1, -1)), 'dictionary arithmetic'),
             ('lambda=2/(g^4 a)', dict_mut(**{'lambda': (F(2), -2, -1)}), 'dictionary arithmetic'),
             ('alpha/16=g^2/(16a)', dict_mut(alpha_over_16=(F(1, 16), 1, -1)), 'dictionary arithmetic'),
             ('tau=24/g^4', dict_mut(tau=(F(24), -2, 0)), 'dictionary arithmetic'),
             ('tau=r (ratio coefficient 1)', dict_mut(tau_ratio_coefficient=F(1)), 'dictionary arithmetic'),
             ('cross identity 2', mut(identities_value={'alpha_lambda_a2': F(2)}), 'dictionary arithmetic'),
             ('cap g^4 one decade off', mut(cap={'tau': tau, 'g4': F(960000000)}), 'dictionary arithmetic')], ok)
    control('toy_trajectory_crossover_exact',
            [('bridge off by one (131)', mut(**{'toy.n_star_bridge': 131}), 'toy crossover'),
             ('non-strict inequality', mut(**{'toy.strict': False}), 'toy crossover'),
             ('cap index 1 (non-strict value)', mut(**{'toy.n_star_cap': 1}), 'toy crossover'),
             ('rehearsal indices swapped', mut(**{'toy.rehearsal.n_star_cap': 421, 'toy.rehearsal.n_star_bridge': 4}),
              'toy crossover'),
             ('rehearsal bridge on g^2 (177)', mut(**{'toy.rehearsal.n_star_bridge': 177}), 'toy crossover'),
             ('rehearsal g_0 changed', mut(**{'toy.rehearsal.g0': 999}), 'toy crossover'),
             ('floating fourth-root estimate', mut(**{'toy.method': 'float fourth root'}), 'toy crossover')], ok)
    # extra controls (not contract ids)
    control('failure_is_certificate_not_gap',
            [('gap failure claimed', mut(**{'failure.actual_gap_failure_claimed': True}), 'sufficient certificate'),
             ('kind no-gap theorem', mut(**{'failure.kind': 'no-gap theorem'}), 'sufficient certificate'),
             ('estimate called supplied along a_n', mut(**{'failure.uniform_along_a_supplied': True}),
              'failure statement')], ok)
    control('failure_scoped_to_g_to_zero',
            [('unscoped failure sentence', add_stmt('The fixed-spacing family supplies no estimate uniform along '
                                                    'a_n->0.'), 'not scoped to g_n->0')],
            ok + [('scoped failure sentence', add_stmt('On the named trajectory no estimate uniform along a_n->0 '
                                                       'is supplied.'))])
    control('route_constant_not_admitted',
            [('cap moved to 7/274688', mut(admitted_tau_cap=self_map), 'route constant')], ok)
    control('physical_scale_control_statement',
            [('admitted regime hosts a finite-mass trajectory',
              mut(**{'scale_control.admitted_regime_hosts_finite_mass_trajectory': True}), 'physical scale control'),
             ('floor from the bridge', mut(**{'scale_control.lattice_gap_floor_sq': F(1, 32)}),
              'physical scale control')], ok)
    control('requirements_table_complete',
            [('drop ' + rid, mut(requirements=[r for r in base['requirements'] if r['id'] != rid]),
              'requirements table') for rid in REQ_ROWS]
            + [('empty missing premise', req_edit('reconstruction_hypotheses', missing_premise=''),
                'requirements table'),
               ('row marked supplied', req_edit('uniform_in_a_estimates', status='supplied'), 'requirements table'),
               ('duplicate row', mut(requirements=base['requirements'] + [dict(base['requirements'][0])]),
                'requirements table')], ok)
    control('lead_not_premise',
            [('lead changes the statement', mut(**{'lead.changes_statement': True}), 'lead not premise'),
             ('lead called verified', mut(**{'lead.status': 'verified construction'}), 'lead not premise'),
             ('search sentence without the disclosure', mut(**{'lead.disclosed_with_search_sentence': False}),
              'lead not premise'),
             ('disclosure clause cut from the prose',
              mut(statements=[t.split('; the claimed construction')[0] + '.' if 'source search' in t else t
                              for t in base['statements']]), 'lead not premise')], ok)
    control('mandatory_sentence_template',
            [('edited', mut(sentence=template.replace('this is not a statement', 'this is a statement')),
              'mandatory sentence'),
             ('absent from the statements', mut(statements=base['statements'][1:]), 'mandatory sentence'),
             ('uniform_in_N scope missing', mut(gate_fields={k: v for k, v in base['gate_fields'].items()
                                                              if k != 'uniform_in_N_scope'}), 'scope string'),
             ('weak_coupling_claim missing', mut(gate_fields={k: v for k, v in base['gate_fields'].items()
                                                               if k != 'weak_coupling_claim'}), 'gate field missing')],
            ok)

    # coherent evidence tampering: executed last, on the evidence of every control above
    rows_ev = [dict(r) for r in CHECKS if r.get('kind') == 'control']
    required_now = [cid for cid in con['controls'] if cid != 'coherent_evidence_tampering']
    ev = {'rows': rows_ev, 'digest': sha_bytes(json.dumps(rows_ev, sort_keys=True).encode())}
    bad = [dict(r) for r in rows_ev]
    bad[[r['id'] for r in bad].index('uniform_in_N_not_in_a')]['passed'] = False
    ev_bad = {'rows': bad, 'digest': sha_bytes(json.dumps(bad, sort_keys=True).encode())}
    few = [r for r in rows_ev if r['id'] != 'toy_trajectory_crossover_exact']
    ev_few = {'rows': few, 'digest': sha_bytes(json.dumps(few, sort_keys=True).encode())}
    ev_stale = {'rows': bad, 'digest': ev['digest']}
    need(validate_evidence(ev, required_now), 'synthetic_evidence_validates', rows=len(rows_ev),
         required=len(required_now))
    control('coherent_evidence_tampering',
            [('rehashed contract', mut(contract_sha256='0' * 64), 'contract hash'),
             ('rehashed AX1 gate', mut(ax1_gate_sha256='0' * 64), 'AX1 gate hash'),
             ('rehashed AL1 gate', mut(al1_gate_sha256='0' * 64), 'AL1 gate hash'),
             ('cap and crossover rebound together', mut(cap={'tau': F(1, 10 ** 7), 'g4': F(960000000)},
                                                        admitted_tau_cap=F(1, 10 ** 7)), 'changed model'),
             ('flipped uniform-sense control, digest rebound', lambda: validate_evidence(ev_bad, required_now),
              'required control not passed'),
             ('dropped crossover control, digest rebound', lambda: validate_evidence(ev_few, required_now),
              'missing required control'),
             ('flipped control, stale digest', lambda: validate_evidence(ev_stale, required_now), 'digest mismatch')],
            ok, scope='synthetic evidence bundle of this checker; producer freeze and inventory checked at '
                      'post-comparison')

    ids_c = set(con['controls'])
    done = {row['id'] for row in CHECKS if row.get('kind') == 'control'}
    missing = sorted(ids_c - done)
    n_mut = sum(len(row['mutations']) for row in CHECKS if row.get('kind') == 'control')
    n_mut_contract = sum(len(row['mutations']) for row in CHECKS if row.get('kind') == 'control' and row['id'] in ids_c)
    n_ctrl = len(done)
    need(not missing, 'contract_controls_covered', implemented=len(ids_c & done), of=len(ids_c), deferred=missing,
         controls_total=n_ctrl, extra_controls=sorted(done - ids_c), rejected_mutations_total=n_mut,
         rejected_mutations_in_contract_controls=n_mut_contract)
    need(all(ids.values()) and d['cap']['n_star'] >= 1 and d['bridge']['n_star'] >= 1, 'target_met_feasibility',
         target='>=1 (feasibility/format check)', value=1, met_by_construction=True)

    return {
        'loop': 'AZ1', 'stage': 'pre_comparison',
        'role': 'skeptic independent derivation (single-direction admission input)',
        'reviewer': 'skeptic (model agent, correlated ancestry); not human peer review, not formal verification',
        'human_author': 'Hruday N M (BUNZEEY)', 'contract_sha256': SHA['contract'],
        'contract_frozen_at': con['frozen_at'], 'checker_sha256': checker_sha,
        'pinned_premises': {rel: digest for _, rel, digest in PINS},
        'producer_files_read': [],
        'incidental_exposure': 'names of the 29 files under research/round32/forward/az1/inputs/ listed with find '
                               'and hashed against their repository sources (all identical); one whole-tree git '
                               'status at the start of this package showed no untracked or modified path; nothing '
                               'else under research/round32/forward/az1/ and nothing under '
                               'research/round32/forward/az2/ was listed or opened',
        'scratch': '/tmp/claude-0/skeptic-az1-private/ (private; arithmetic previews and source-edit harness)',
        'model': MODEL_LABEL + ' (AX1), route B, Haar reference; along a named trajectory (a_n,g_n) with g_n->0 as '
                               'a_n->0 stated as a hypothesis of asymptotic-freedom form; E_star and hbar fixed',
        'dictionary': {'alpha': 'g^2/(2a)', 'lambda': '2/(g^2 a)', 'tau': '24 lambda/alpha = 96/g^4',
                       'r': 'lambda/alpha = 4/g^4', 'nu': 'alpha tau/24 = lambda', 'nu_over_delta': 'tau/3',
                       'gap': '(alpha/8)(1/2) = alpha/16 = g^2/(32a)', 'cross_identity': 'alpha*lambda*a^2 = 1',
                       'inverse': 'a^2 = 1/(alpha lambda), g^4 = 4 alpha/lambda', 'local_norm': '7|tau| = 672/g^4',
                       'identities_verified': sorted(ids)},
        'regime': {'admitted_tau_cap': q(tau), 'admitted_g4_min': q(tau_cap_g4), 'bridge_g4_min': '32',
                   'bridge_tau_max': '3', 'ends_g4_min_labelled': '8',
                   'route_radius_labelled_not_admitted': q(self_map), 'route_g4_labelled': q(g4_route),
                   'exclusion_radius_labelled': q(exclusion), 'J_prime_in_g': '2784/g^4',
                   'lattice_gap_floor_sq': q(floor_sq), 'lattice_gap_floor': '1250 sqrt 6',
                   'lattice_gap_floor_bracket': [q(1250 * s6_lo), q(1250 * s6_hi)]},
        'toy_trajectory': table,
        'physical_example': {'g2': '100000', 'g4': '10000000000', 'tau': q(96 / F(10 ** 10)), 'a_fm': '1/10',
                             'hbar_c_MeV_fm': q(hbar_c), 'gap_lower_MeV': q(ex_gap),
                             'cap_gap_lower_MeV_bracket_at_a_0p1fm': [q(cap_gap_lo), q(cap_gap_hi)],
                             'label': 'units illustration only; no scale setting'},
        'requirements': reference_requirements(),
        'predictions': {
            'identities': 'alpha/16=g^2/(32a), tau=96/g^4, alpha*lambda*a^2=1 as literal identities',
            'cap_g4': q(tau_cap_g4), 'bridge_g4': '32',
            'n_star_declared': {'cap': 2, 'bridge': 132}, 'n_star_g0_1000': {'cap': 4, 'bridge': 421},
            'g4_declared_n131_n132': [q(g0_4 / F(131) ** 4), q(g0_4 / F(132) ** 4)],
            'g4_g0_1000_n3_n4': [q(F(10 ** 12) / 81), q(F(10 ** 12) / 256)],
            'g4_g0_1000_n420_n421': [q(F(10 ** 12) / F(420) ** 4), q(F(10 ** 12) / F(421) ** 4)],
            'lattice_gap_floor': '1250 sqrt 6', 'gate_fields': dict(base['gate_fields'])},
        'gate_fields': dict(base['gate_fields']), 'sentence': template, 'statements': statements,
        'deferred_parts': {
            'coherent_evidence_tampering': 'executed on a synthetic evidence bundle; the producer freeze and '
                                           '29-file inventory are checked at post-comparison',
            'phrase_scans': 'forbidden-phrase, uniform-sense and fraction scans run here on reference and mutated '
                            'statements; the producer report is scanned at post-comparison',
            'requirements_table': 'executed on the skeptic reference table; the producer table is checked at '
                                  'post-comparison'},
        'checks': CHECKS,
        'previews': {
            'cap_g2': preview(20000 * s6_lo * 2), 'lattice_gap_floor': preview(1250 * s6_lo),
            'route_g4_labelled': preview(g4_route), 'route_radius_over_cap': preview(self_map / tau),
            'g4_declared_n131': preview(g0_4 / F(131) ** 4), 'g4_declared_n132': preview(g0_4 / F(132) ** 4),
            'g4_g0_1000_n3': preview(F(10 ** 12) / 81), 'g4_g0_1000_n420': preview(F(10 ** 12) / F(420) ** 4),
            'g4_g0_1000_n421': preview(F(10 ** 12) / F(421) ** 4),
            'example_gap_MeV': preview(ex_gap), 'cap_gap_MeV_at_a_0p1fm': preview(cap_gap_lo),
            'magnetic_multiplier_max_at_n132': preview(g4_132 / 32),
            'one_loop_heuristic_aLambda_at_cap': '9.998901e-01',
            'one_loop_heuristic_aLambda_at_bridge': '1.490719e-01',
            'one_loop_note': 'heuristic only, not admission: 1/g^2=2 b0 ln(1/(a Lambda)), b0=11/(24 pi^2) for SU(2); '
                             'the cap sits at a*Lambda~1 and the bridge at a*Lambda~0.149',
            'label': 'floating previews only; no admission Boolean reads them'},
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
    try:
        out.resolve().relative_to(ROOT)
        raise SystemExit('--output must lie outside the checkout')
    except ValueError:
        pass
    result = execute()
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checks': len(result['checks']),
                      'n_star': result['predictions']['n_star_declared'],
                      'n_star_g0_1000': result['predictions']['n_star_g0_1000']}))


if __name__ == '__main__':
    main()
