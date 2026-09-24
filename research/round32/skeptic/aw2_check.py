#!/usr/bin/env python3
"""Round32 AW2 skeptic pre-comparison independent replay (single-direction loop).

Written after the AW2 contract froze, from the frozen contract, selection-aw2.md,
the AW1 gate, the AW1 contract (rule text), the AV1 gate, the I1 report (I1.5)
and the skeptic's own AW1 files, before reading research/round32/forward/aw2/.
Nothing is imported from any producer or assistant. Standard library only.
Every admission Boolean is decided with fractions.Fraction; floats appear only
in the labelled 'previews' block. Every check and control raises an explicit
exception, so python -O cannot disable it. Model-agent skeptic with correlated
ancestry (same model family as the advisor and the producer); not human peer
review, not formal verification.

What is replayed:
  * K_2^+ is read from the hash-pinned AW1 gate (decision and accepted text),
    tied to the contract's K_2_plus string, and reconstructed from its own
    itemization (T*T straddling, T^2 pair, eps=2T+T^2 density, a*eps^2
    normalization) as a cross-check only; the gate value is the one used.
  * tau_AW2 is evaluated by the AW1 decade-grid rule parsed from the pinned AW1
    contract; the contract's literal 1/100000000 is compared afterwards only.
  * The first-order coefficient +1/144 is re-derived from the I1.5 string, the
    energy 3 of W_f Omega_0 and Haar moments from the SU(2) character recursion.
  * omega_tau(W) in [tau/144 - K tau^2, tau/144 + K tau^2] at tau=+-tau_AW2,
    strict exclusion of the free reference 0 (read from the contract), the
    exclusion margin (|tau|/144 - K tau^2)/(K tau^2) and the sign margin
    1/(144 K |tau|); decimals are widened outward and re-verified.

Usage: python3 -B research/round32/skeptic/aw2_check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REL = {
    'contract': 'research/round32/contracts/aw2.json',
    'aw1_gate': 'research/round32/advisor/aw1-gate.json',
    'aw1_contract': 'research/round32/contracts/aw1.json',
    'av1_gate': 'research/round32/advisor/av1-gate.json',
    'i1_report': 'research/round21/forward/i1/report.md',
    'skeptic_aw1': 'research/round32/skeptic/aw1.json',
    'selection': 'research/round32/advisor/selection-aw2.md',
}
PINNED = {
    'contract': 'aa559b18231961b5bb9dc5b7d0dd3097a1a2753916b54639eb1fd573e08368f9',
    'aw1_gate': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'aw1_contract': 'c24bf7eb6a1c24034427c810a9c26c4c86d1f9c1d31b0fe36ea4cf2a796814ef',
    'av1_gate': '55e03f2d9c297d41106d983cec45eaa642ca18123544f416916f94414de305a0',
    'i1_report': '836a4c7d421f0ddf3589c159d2f057839421532c88157a054a61b51c25c781a9',
    'skeptic_aw1': 'bd2ee4cdf6a355fd92f8b9f2f0fa8c11a0abab42dc1a5dd511affb31372914f2',
}
ZERO_TRIPLE = ('0', '0', '0')
BOX_R = ((0, 0, 0), (0, 0, 1))


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


def is_exact(x):
    return isinstance(x, (F, int)) and not isinstance(x, bool)


def floor_to(x, den):
    return F((x.numerator * den) // x.denominator, den)


def ceil_to(x, den):
    return F(-((-x.numerator * den) // x.denominator), den)


def dec_directed(x, up, sig=16):
    """Decimal string d.ddd...e-N rounded toward +inf (up) or -inf (down)."""
    if x == 0:
        return '0'
    neg = x < 0
    ax = -x if neg else x
    e = 0
    while ax >= F(10) ** (e + 1):
        e += 1
    while ax < F(10) ** e:
        e -= 1
    y = ax * F(10) ** (sig - 1 - e)
    mag_up = (up != neg)
    n = -((-y.numerator) // y.denominator) if mag_up else y.numerator // y.denominator
    digits = str(n)
    exp10 = e - (sig - 1) + len(digits) - 1
    s = ('-' if neg else '') + digits[0] + '.' + digits[1:] + 'e' + str(exp10)
    val = F(s)
    if (up and val < x) or ((not up) and val > x):
        raise CheckFailure('directed decimal')
    return s


def sqrt_bracket(n, scale):
    """Rational lo <= sqrt(n) <= hi for a Fraction n > 0, on the grid 1/scale."""
    num = n.numerator * scale * scale
    r = isqrt(num // n.denominator)
    lo = F(r, scale)
    while lo * lo > n:
        lo -= F(1, scale)
    hi = lo + F(1, scale)
    while hi * hi < n:
        hi += F(1, scale)
    if not (lo * lo <= n <= hi * hi):
        raise CheckFailure('sqrt bracket')
    return lo, hi


# ---------------------------------------------------------------- inputs
def load_inputs():
    raw, got = {}, {}
    for key, rel in REL.items():
        b = (ROOT / rel).read_bytes()
        raw[key] = b
        got[key] = sha_bytes(b)
    for key, pin in PINNED.items():
        if got[key] != pin:
            raise CheckFailure('hash mismatch for %s: %s' % (REL[key], got[key]))
    return raw, got


def parse_k2(gate, contract):
    m_dec = re.search(r'Bind K_2\^\+ = (\d+)/(\d+)', gate['decision'])
    m_acc = re.search(r'the bound value is K_2\^\+=(\d+)/(\d+)', gate['accepted'])
    m_con = re.match(r'(\d+)/(\d+) ', contract['parameters']['K_2_plus'])
    m_ceil = re.search(r'outward ceiling (\d+)/10\^(\d+)', contract['parameters']['K_2_plus'])
    if not (m_dec and m_acc and m_con and m_ceil):
        raise CheckFailure('K_2^+ not found in gate or contract')
    vals = [F(int(m.group(1)), int(m.group(2))) for m in (m_dec, m_acc, m_con)]
    ceil = F(int(m_ceil.group(1)), 10 ** int(m_ceil.group(2)))
    return vals, ceil, int(m_ceil.group(2))


def parse_rule(aw1c):
    rule = aw1c['parameters']['aw2_coupling_rule']
    m = re.search(r'decade grid \{10\^-(\d+), 10\^-(\d+), \.\.\.\} with K_2\^\+ \* tau <= (\d+)/(\d+) '
                  r'\(half the first-order coefficient\)', rule)
    if not m or int(m.group(2)) != int(m.group(1)) + 1:
        raise CheckFailure('AW1 rule text not parsed')
    if 'never chosen after K_2 is seen' not in rule or 'exact-tier' not in rule:
        raise CheckFailure('AW1 rule text lacks the pre-freeze or tier clause')
    return int(m.group(1)), F(int(m.group(3)), int(m.group(4))), rule


def parse_i15(text):
    i = text.index('\\tag{I1.5}')
    block = text[max(0, i - 400):i]
    m = re.search(r'=\s*([+-])\{\\tau\\over(\d+)\}\\sum_\{f\\in O_b\}W_f', block)
    if not m:
        raise CheckFailure('I1.5 display not found')
    return m.group(1), int(m.group(2)), m.group(0)


# ---------------------------------------------------------------- Haar and geometry
def haar_moments(nmax=8):
    """E[W^n] = mult(spin 0 in (1/2)^{(x)n}) / 2^n from chi_{1/2} chi_j = chi_{j-1/2} + chi_{j+1/2}."""
    mult = {0: 1}  # key 2j
    out = {}
    for n in range(1, nmax + 1):
        new = {}
        for tj, c in mult.items():
            for nj in (tj - 1, tj + 1):
                if nj >= 0:
                    new[nj] = new.get(nj, 0) + c
        mult = new
        out[n] = F(mult.get(0, 0), 2 ** n)
    return out


DIRS = {'x': (1, 0, 0), 'y': (0, 1, 0), 'z': (0, 0, 1)}


def add(p, d):
    return (p[0] + d[0], p[1] + d[1], p[2] + d[2])


def block(p):
    return (p[0] // 4, p[1] // 2, p[2])


def faces_window():
    out = []
    for x in range(-9, 10):
        for y in range(-5, 6):
            for z in range(-3, 4):
                p = (x, y, z)
                for a, c in (('x', 'y'), ('x', 'z'), ('y', 'z')):
                    selected = (a, c) == ('x', 'y') and x % 4 in (0, 1, 2) and y % 2 == 0
                    links = frozenset([(p, a), (add(p, DIRS[a]), c), (add(p, DIRS[c]), a), (p, c)])
                    owners = frozenset([block(p), block(add(p, DIRS[a])), block(add(p, DIRS[c]))])
                    out.append({'p': p, 'plane': a + c, 'selected': selected, 'links': links, 'owners': owners,
                                'anchor': block(p)})
    return out


def geometry():
    faces = faces_window()
    om = [f for f in faces if not f['selected']]
    R = frozenset(BOX_R)
    W = [f for f in om if f['p'] == (0, 0, 0) and f['plane'] == 'xz'][0]
    meet0 = [f for f in om if (0, 0, 0) in f['owners']]
    meetR = [f for f in om if f['owners'] & R]
    exactR = [f for f in om if f['owners'] == R]
    both = [f for f in om if R <= f['owners']]
    anch0 = [f for f in om if f['anchor'] == (0, 0, 0)]
    star = set()
    for f in anch0:
        star |= set(f['owners'])
    link_owner = {l: block(l[0]) for l in W['links']}
    shared_max = max(len(f['links'] & g['links']) for f in meetR for g in meetR if f is not g)
    return {'W': W, 'meet0': len(meet0), 'meetR': meetR, 'exactR': len(exactR), 'both': len(both),
            'anchored0': len(anch0), 'star': sorted(star), 'W_owners': sorted(set(link_owner.values())),
            'shared_max': shared_max}


def parity_pairing(W, faces, EW2):
    """E[W W_f]: zero unless every link of W W_f appears an even number of times (Z_2 centre grading)."""
    vals = {}
    for f in faces:
        odd = W['links'] ^ f['links']
        vals[(f['p'], f['plane'])] = EW2 if not odd else F(0)
    return vals


# ---------------------------------------------------------------- one-plaquette fixture (finite graph)
def rs_series(jmax2, order):
    """Energy series E(lam)=sum E_n lam^n for H=G0+lam*W on the one-plaquette chain j=0..jmax2/2,
    G0=4j(j+1) (alpha units), W chi_j=(chi_{j-1/2}+chi_{j+1/2})/2. Returns E_n (n<=order)."""
    dim = jmax2 + 1
    en = [F(4) * F(k, 2) * (F(k, 2) + 1) for k in range(dim)]

    def Wv(v):
        out = [F(0)] * dim
        for k in range(dim):
            if k - 1 >= 0:
                out[k - 1] += v[k] / 2
            if k + 1 < dim:
                out[k + 1] += v[k] / 2
        return out

    psi = [[F(1)] + [F(0)] * (dim - 1)]
    E = [F(0)]
    for n in range(1, order + 1):
        wv = Wv(psi[n - 1])
        E.append(wv[0])
        rhs = list(wv)
        for k in range(1, n + 1):
            rhs = [r - E[k] * s for r, s in zip(rhs, psi[n - k])]
        new = [F(0)] + [rhs[m] / (en[0] - en[m]) for m in range(1, dim)]
        psi.append(new)
    return E


def mean_W_series(E, lam_per_tau):
    """<W> = dE/dlam as a series in tau with lam = lam_per_tau * tau: coefficient of tau^(n-1)."""
    return {n - 1: n * E[n] * lam_per_tau ** (n - 1) for n in range(1, len(E))}


def two_level_bracket(tau, lam_per_tau):
    """Exact ground state of [[0,b],[b,3]], b=lam/2; <W>=bE/(b^2+E^2); rational bracket."""
    b = lam_per_tau * tau / 2
    lo_s, hi_s = sqrt_bracket(9 + 4 * b * b, 10 ** 40)
    E_lo, E_hi = (3 - hi_s) / 2, (3 - lo_s) / 2  # both negative
    if not (E_hi < 0):
        raise CheckFailure('two-level ground energy sign')
    cands = []
    for Ev in (E_lo, E_hi):
        for Ed in (E_lo, E_hi):
            cands.append(b * Ev / (b * b + Ed * Ed))
    return min(cands), max(cands)


# ---------------------------------------------------------------- validators
class Ctx:
    pass


C = Ctx()


def validate_exact(*xs):
    for x in xs:
        if not is_exact(x):
            raise Rejected('exact arithmetic: non-rational value %r' % (x,))


def enclose(tau, K=None, triple=ZERO_TRIPLE, box_N=2, tier='exact', label=None):
    """Reusable exact calculator, restricted to the proved domain."""
    validate_exact(tau)
    if K is None:
        K = C.K
    validate_exact(K)
    if tier != 'exact':
        raise Rejected('tier mixing: only the exact-tier AW1 gate constant is admitted')
    if K != C.K and not (K == C.K_ceil and label == 'outward_ceiling'):
        raise Rejected('K_2 not the AW1 gate binding')
    if tuple(triple) != ZERO_TRIPLE:
        raise Rejected('model changed: nonzero selected triple')
    if abs(tau) > C.cap:
        raise Rejected('model changed: |tau| above the cap 10^-8')
    if not (isinstance(box_N, int) and not isinstance(box_N, bool) and box_N >= 2):
        raise Rejected('box: centered whole-star box with N>=2 required')
    c = C.coef * F(tau)
    r = F(K) * F(tau) * F(tau)
    return c - r, c + r


def rule_eval(K, tier='exact'):
    if tier != 'exact':
        raise Rejected('tier mixing: the frozen rule takes the exact-tier constant')
    validate_exact(K)
    rows = []
    for k in range(C.grid_start, C.grid_start + 60):
        tau = F(1, 10 ** k)
        ok = K * tau <= C.threshold
        rows.append((k, tau, K * tau, ok))
        if ok:
            return tau, rows
    return None, rows


def validate_coupling(pk):
    if pk.get('source') != 'aw1_rule_from_gate':
        raise Rejected('coupling rule: literal or externally chosen coupling')
    tau = pk['tau']
    validate_exact(tau)
    k = 0
    t = F(tau)
    while t < 1 and t * 10 <= 1:
        t *= 10
        k += 1
    if t != 1:
        raise Rejected('coupling rule: off the decade grid')
    if k < C.grid_start:
        raise Rejected('coupling rule: above the cap')
    rule_tau, _ = rule_eval(pk.get('K', C.K), pk.get('tier', 'exact'))
    if pk.get('K', C.K) != C.K:
        raise Rejected('K_2 not the AW1 gate binding')
    if tau != rule_tau:
        raise Rejected('coupling rule: not the largest grid element passing the rule')
    return True


def exclusion_margin(tau, K):
    a, r = abs(tau) * C.coef, K * tau * tau
    return (a - r) / r


def sign_margin(tau, K):
    return 1 / (C.coef_inv * K * abs(tau))


def validate_margin(pk):
    tau, K = pk['tau'], pk['K']
    if pk.get('margin_definition') != '(|tau|/144 - K tau^2)/(K tau^2)':
        raise Rejected('margin denominator: exclusion margin must be taken against K tau^2')
    if pk['exclusion_margin'] != exclusion_margin(tau, K):
        raise Rejected('margin denominator: value differs from (|tau|/144 - K tau^2)/(K tau^2)')
    if pk['sign_margin'] != sign_margin(tau, K):
        raise Rejected('margin denominator: sign margin differs from 1/(144 K |tau|)')
    if pk['exclusion_margin'] == pk['sign_margin']:
        raise Rejected('margin denominator: sign margin reported as exclusion margin')
    return True


def validate_claims(flags):
    must_false = ('continuum_claim', 'uniform_wilson_claim', 'scientific_priority_verified',
                  'dynamical_correction_claim', 'sign_certified_below_cap', 'centered_correlation_shift_resolved',
                  'mass_gap_claim', 'uniqueness_claim')
    for k in must_false:
        if flags.get(k) is not False:
            raise Rejected('forbidden claim ' + k)
    if flags.get('static_not_dynamic') is not True:
        raise Rejected('forbidden claim static_not_dynamic missing')
    if flags.get('resolved_interaction_shift') is not C.excluded_at_cap:
        raise Rejected('forbidden claim resolved_interaction_shift without exclusion at the cap')
    return True


def validate_packet(pk):
    """Full AW2 result packet (the producer's results would be read against this)."""
    if pk.get('producers') != C.producers:
        raise Rejected('single producer: fabricated reverse package or wrong producer list')
    if 'reverse' in pk.get('packages', {}):
        raise Rejected('single producer: fabricated reverse package or wrong producer list')
    if pk.get('reverse_premise_isolation') != 'not_applicable: single producer':
        raise Rejected('single producer: reverse premise isolation must be stated not applicable')
    if pk.get('model_id') != C.model_id or tuple(pk.get('triple', ())) != ZERO_TRIPLE:
        raise Rejected('model changed: model id or selected triple')
    if pk.get('cover') != [list(r) for r in BOX_R]:
        raise Rejected('cover: the original Wilson loop needs R={0,e_z}')
    if pk.get('centering') != 'none' or 'm_hat' in pk:
        raise Rejected('centering: omega(W) is uncentered; no m_hat enters its path')
    validate_coupling(pk['coupling'])
    tau = pk['coupling']['tau']
    K = pk['K']
    if K != C.K:
        raise Rejected('K_2 not the AW1 gate binding')
    terms = pk['error_terms']
    for name in C.error_terms:
        if name not in terms:
            raise Rejected('error term missing: ' + name)
        t = terms[name]
        if t.get('status') == 'not_applicable' and not t.get('reason'):
            raise Rejected('error term not_applicable without a stated reason: ' + name)
    if terms['second_order_remainder'].get('exponent') != 2 or terms['first_order_exact'].get('exponent') != 1:
        raise Rejected('tau scaling: exponents must be 1 (first order) and 2 (remainder)')
    if terms['second_order_remainder'].get('radius_per_tau2') != K:
        raise Rejected('radius: remainder is not K_2^+ tau^2')
    mult = pk.get('overlap_multiplier', {'value': F(1)})
    if mult['value'] != 1 and mult.get('label') != 'conservative':
        raise Rejected('overlap multiplier: factor other than 1 must be labelled conservative')
    if pk.get('volume_scaling') not in (None, 'uniform'):
        raise Rejected('root-N: the remainder is uniform in the box, not averaged')
    encs = pk['enclosures']
    for sgn in ('+', '-'):
        lo, hi = encs[sgn]['lo'], encs[sgn]['hi']
        validate_exact(lo, hi)
        t = tau if sgn == '+' else -tau
        c = C.coef * t
        r = K * t * t * mult['value']
        if pk.get('first_order_coefficient') != C.coef:
            raise Rejected('first-order coefficient: not the derived +1/144')
        if (lo, hi) != (c - r, c + r):
            raise Rejected('enclosure endpoints differ from tau/144 -+ K tau^2')
        dlo, dhi = F(encs[sgn]['lo_decimal']), F(encs[sgn]['hi_decimal'])
        if dlo > lo or dhi < hi:
            raise Rejected('exact arithmetic: decimal endpoints not widened outward')
    if (encs['-']['lo'], encs['-']['hi']) != (-encs['+']['hi'], -encs['+']['lo']):
        raise Rejected('sign flip: -tau enclosure is not the negated +tau enclosure')
    if pk.get('minus_tau_role') != 'replay':
        raise Rejected('sign flip: the -tau enclosure is a replay, not a second confirmation')
    ref = C.reference
    for sgn in ('+', '-'):
        lo, hi = encs[sgn]['lo'], encs[sgn]['hi']
        inside = lo <= ref <= hi
        if inside and pk.get('resolved_interaction_shift'):
            raise Rejected('free reference inside enclosure => no interaction claim')
        if pk.get('strict_exclusion') and not (ref < lo or hi < ref):
            raise Rejected('free reference inside enclosure => strict exclusion fails')
    validate_margin(pk['margins'])
    tgt = pk['margins']['exclusion_margin'] >= C.target
    if pk.get('verdict') == 'accepted_within_scope' and not tgt:
        raise Rejected('verdict: accepted requires the exclusion margin target')
    if 'static_not_dynamic' not in pk.get('sub_labels', []):
        raise Rejected('static: sub-label static_not_dynamic required')
    if 'sign_certified_below_cap' in pk.get('sub_labels', []) and tau == C.cap:
        raise Rejected('static: sign_certified_below_cap does not apply at the cap')
    if pk.get('effect_kind') != 'static_equal_time_mean':
        raise Rejected('static: effect must be the static equal-time mean')
    validate_claims(pk['flags'])
    return True


def validate_evidence(inv):
    """inv: {'files': {rel: sha}, 'manifest_sha256': sha of canonical files json}."""
    canon = json.dumps(inv['files'], sort_keys=True).encode()
    if inv.get('manifest_sha256') != sha_bytes(canon):
        raise Rejected('evidence: manifest hash does not bind the file list')
    for key, rel in REL.items():
        if key == 'selection':
            continue
        if rel not in inv['files']:
            raise Rejected('evidence: required snapshot missing ' + rel)
        if inv['files'][rel] != PINNED[key]:
            raise Rejected('evidence: pinned hash differs for ' + rel)
    return True


def verdict_from(K, tier='exact'):
    if K is None:
        return 'insufficient', []
    tau, _ = rule_eval(K, tier)
    if tau is None:
        return 'insufficient', []
    m = exclusion_margin(tau, K)
    if tau == C.cap and m >= C.target:
        return 'accepted_within_scope', ['static_not_dynamic']
    if tau == C.cap:
        return 'limited', ['static_not_dynamic']
    return 'limited', ['static_not_dynamic', 'sign_certified_below_cap']


def validate_retained(tier, verdict, retained):
    if tier == 'crude' and verdict == 'accepted_within_scope':
        raise Rejected('insufficient tier relabelled as accepted')
    if tier == 'crude' and not retained:
        raise Rejected('insufficient tier dropped instead of retained')
    return True


def validate_effect(kind):
    if kind != 'static_equal_time_mean':
        raise Rejected('static: %s is not what the enclosure certifies' % kind)
    return True


def validate_centering(kind, value, m, a, b, x1, x2):
    """Synthetic fixture: ground e0 with P e0 = e0, P = diag(1, x1, x2), W e0 = (m, a, b).
    vector-centred <(W-m)e0, P(W-m)e0> and scalar-centred <We0, P We0> - m^2 both equal x1 a^2 + x2 b^2."""
    corr = x1 * a * a + x2 * b * b
    vec = x1 * a * a + x2 * b * b                      # (W-m)e0 = (0, a, b)
    scal = (m * m + x1 * a * a + x2 * b * b) - m * m   # <We0,PWe0> - m^2
    if vec != corr or scal != corr:
        raise CheckFailure('centering identity')
    if kind == 'vector' and value != vec:
        raise Rejected('centering: vector-centred value mismatch')
    if kind == 'scalar' and value != scal:
        raise Rejected('centering: scalar-centred value mismatch')
    return True


def validate_reference(ref, EW):
    if ref != EW or ref != C.reference:
        raise Rejected('reference: the free Haar value of omega(W) is E[W]=0')
    return True


def validate_sign_fixture(i15_sign, series):
    if i15_sign != '-':
        raise Rejected('sign convention: the frozen I1.5 string is phi_b=-(tau/3) sum W_f')
    if not series[1] > 0:
        raise Rejected('sign convention: sign(<W>) must equal sign(tau) at first order')
    return True


def validate_first_order(coef, faces):
    if faces != ['W']:
        raise Rejected('wrong face: only f=W contributes at first order')
    if coef != C.coef:
        raise Rejected('first-order coefficient: not the derived +1/144')
    return True


def validate_amplitude(v_coef, energy):
    if F(v_coef) / energy != F(-1, 72):
        raise Rejected('unit mixing: per-face creation amplitude must be -tau/72 in both unit systems')
    return True


def validate_k2_reconstruction(J_per_tau, faces_per_site):
    tau = C.cap
    J = J_per_tau * tau
    T = F(faces_per_site, 144) * tau / (1 - C.gp * J)
    rho = C.gp * J * T
    eps = 2 * T + T * T
    K = (rho + T * T + T * T + eps * eps + (tau / 144) * eps * eps) / (tau * tau)
    if K != C.K:
        raise Rejected('incident stars or face count: reconstruction differs from the AW1 gate K_2^+')
    return True


# ---------------------------------------------------------------- execution
def execute():
    raw, hashes = load_inputs()
    contract = json.loads(raw['contract'])
    gate = json.loads(raw['aw1_gate'])
    aw1c = json.loads(raw['aw1_contract'])
    av1 = json.loads(raw['av1_gate'])
    sk1 = json.loads(raw['skeptic_aw1'])
    i1 = raw['i1_report'].decode()
    selection = raw['selection'].decode()

    # ---- contract and gate provenance
    pre = contract['preregistration']
    need(contract['id'] == 'AW2' and contract['status'] == 'frozen_before_production'
         and contract['single_direction_independent_replay'] is True and contract['producers'] == ['forward']
         and contract['direction'] == 'single+skeptic', 'contract_hash_status_single_direction',
         contract_sha256=hashes['contract'], frozen_at=contract['frozen_at'])
    need(list(contract['controls']) == list(pre['controls_required']['ids']) and len(contract['controls']) == 23,
         'contract_controls_mirror_equal', n=str(len(contract['controls'])))
    need(all(p in contract['shared_premises'] for p in (REL['aw1_gate'], REL['aw1_contract'], REL['av1_gate'],
                                                        REL['i1_report'], REL['selection'])),
         'checker_inputs_are_declared_premises', note='skeptic/aw1.json is the skeptic own file, bound in the AW1 gate')
    need(gate['loop'] == 'AW1' and gate['verdict'] == 'accepted_within_scope'
         and gate['bindings'][REL['i1_report']] == hashes['i1_report']
         and gate['bindings'][REL['skeptic_aw1']] == hashes['skeptic_aw1']
         and gate['bindings'][REL['aw1_contract']] == hashes['aw1_contract']
         and gate['bindings'][REL['av1_gate']] == hashes['av1_gate'],
         'aw1_gate_hash_verdict_and_binding_chain', aw1_gate_sha256=hashes['aw1_gate'])

    C.producers = contract['producers']
    C.model_id = pre['model_id']
    C.error_terms = list(pre['error_terms_itemized'])
    tgt = pre['target']
    need(tgt['quantity'] == 'exclusion_margin' and tgt['comparator'] == '>=', 'target_read_from_contract',
         target=tgt['value'], comparator=tgt['comparator'])
    C.target = F(tgt['value'])
    ptxt = contract['parameters']['target']
    need('exclusion margin m = (|tau|/144 - K_2^+ tau^2)/(K_2^+ tau^2) >= 2' in ptxt
         and '1/(144 K_2^+ |tau|) >= 3' in ptxt and 'sign margin 1/(144 K_2^+ |tau|)' in ptxt,
         'margin_definitions_read_from_contract_text', text=ptxt)
    obs = pre['observable']
    need(obs['id'] == 'omega(W)' and obs['centering'] == 'none' and obs['reference_route'] == 'haar',
         'reference_read_from_contract', reference=obs['reference_value_exact'])
    C.reference = F(obs['reference_value_exact'])
    need(tuple(pre['selected_triple_alpha_units']) == ZERO_TRIPLE
         and tuple(contract['parameters']['selected_coefficients_over_alpha']) == ZERO_TRIPLE, 'zero_selected_triple')

    # ---- K_2^+ from the gate, two sources, outward ceiling
    vals, K_ceil, ceil_exp = parse_k2(gate, contract)
    need(vals[0] == vals[1] == vals[2], 'k2_plus_gate_decision_accepted_and_contract_equal', K2=q(vals[0]))
    K = vals[0]
    C.K, C.K_ceil = K, K_ceil
    need(K_ceil >= K and K_ceil - K < F(1, 10 ** ceil_exp) and K_ceil == ceil_to(K, 10 ** ceil_exp),
         'k2_outward_ceiling_directed', ceiling=q(K_ceil))
    fwd = F(sk1['admitted_values']['K2_exact_tier_forward'])
    rev = F(sk1['admitted_values']['K2_exact_tier_reverse'])
    need(K > fwd > rev and F(sk1['admitted_values']['K2_exact_tier_bound']) == K,
         'gate_binds_largest_valid_exact_tier_value', forward=preview(fwd), reverse=preview(rev))
    m = re.search(r't<=T=\((\d+)\|tau\|/(\d+)\)/\(1-(\d+)J\), rho=(\d+)JT, J=(\d+)\|tau\|', gate['accepted'])
    need(m is not None and m.group(3) == m.group(4), 'gate_exact_tier_formula_parsed', formula=m.group(0))
    C.gp = F(int(m.group(3)))
    C.cap = F(aw1c['parameters']['tau_cap'])
    need(C.cap == F(1, 10 ** 8), 'cap_read_from_aw1_contract', cap=q(C.cap))
    need(validate_k2_reconstruction(F(int(m.group(5))), int(m.group(1))) is True,
         'gate_k2_reconstructed_from_itemization',
         form='(rho + T*T + T^2 + eps^2 + (|tau|/144) eps^2)/tau^2, eps=2T+T^2; cross-check only, the gate value is used')

    # ---- Haar moments and geometry
    mom = haar_moments()
    need(mom[1] == 0 and mom[2] == F(1, 4) and mom[3] == 0 and mom[4] == F(1, 8) and C.reference == mom[1],
         'haar_moments_character_recursion', moments={str(n): q(v) for n, v in mom.items()})
    geo = geometry()
    need(geo['meet0'] == 49 and len(geo['meetR']) == 82 and geo['exactR'] == 10 and geo['both'] == 16
         and geo['anchored0'] == 21 and len(geo['star']) == 4 and geo['shared_max'] == 1,
         'geometry_counts_from_I1_4', faces_per_site='49', meeting_R='82', owner_set_R='10', touching_both='16',
         anchored='21', star_sites='4', max_shared_links='1')
    need(geo['W_owners'] == sorted(BOX_R), 'wilson_cover_R_from_link_owners', owners=[list(o) for o in geo['W_owners']])
    pair = parity_pairing(geo['W'], geo['meetR'], mom[2])
    nonzero = [k for k, v in pair.items() if v != 0]
    need(nonzero == [((0, 0, 0), 'xz')] and pair[((0, 0, 0), 'xz')] == F(1, 4), 'only_W_pairs_with_W',
         nonzero=[str(k) for k in nonzero], zero_faces=str(len(pair) - 1))

    # ---- first-order coefficient: sign chain from I1.5
    sgn, den, disp = parse_i15(i1)
    need(sgn == '-' and den == 3, 'i15_convention_read', display=disp)
    phi_coef = F(-1, den)                  # normalized (delta) units
    alpha_coef = phi_coef / 8              # V_b = phi_b/8 in alpha units
    energy_alpha = 4 * F(3, 4)             # four spin-1/2 links, C=j(j+1)=3/4
    energy_norm = 8 * energy_alpha
    amp = alpha_coef / energy_alpha        # c^(1) per face (creation, H0^{-1} P V Omega_0)
    need(amp == phi_coef / energy_norm == F(-1, 72), 'creation_amplitude_both_units', amplitude='-tau/72')
    coef = -2 * amp * sum(pair.values())   # omega = -2 Re <W Omega_0, c^(1)>, only f=W pairs
    need(coef == F(1, 144) and contract['parameters']['first_order'].startswith('tau/144'),
         'first_order_coefficient_plus_1_over_144', sign_chain='phi_b=-(tau/3)sum W_f; V_b=-(tau/24)sum W_f; '
         'c1=-(tau/72)sum W_f Omega_0; psi=Omega_0-c1; omega=-2Re<W Omega_0,c1>=(tau/36)E[W^2]=tau/144')
    C.coef, C.coef_inv = coef, 1 / coef
    literal = 2 * amp * sum(pair.values())
    need(literal == -coef, 'aw1_literal_display_gives_minus', literal_value=q(literal))

    # ---- one-plaquette fixture (finite graph, transfers_to_aq false)
    lam = alpha_coef                       # lam per tau, one plaquette: V=-(tau/24) W
    E6a, E6b = rs_series(6, 6), rs_series(5, 6)
    ser = mean_W_series(E6a, lam)
    need(E6a == E6b and ser[1] == F(1, 144) and ser[2] == 0 and ser[3] == F(-5, 11943936) and ser[4] == 0,
         'one_plaquette_series', series={str(k): q(v) for k, v in ser.items()},
         label='finite graph (one plaquette), transfers_to_aq false')
    bp = two_level_bracket(C.cap, lam)
    bm = two_level_bracket(-C.cap, lam)
    need(bp[0] > 0 and bm[1] < 0 and bp[0] == -bm[1] and bp[1] == -bm[0], 'one_plaquette_exact_sign_both_signs',
         plus=[dec_directed(bp[0], False), dec_directed(bp[1], True)],
         minus=[dec_directed(bm[0], False), dec_directed(bm[1], True)], label='finite graph, two-level truncation')
    ser_flip = mean_W_series(rs_series(6, 6), -lam)
    i1_flipped = i1.replace(disp, disp.replace('=-{', '=+{', 1))
    need(i1_flipped != i1 and parse_i15(i1_flipped)[0] == '+' and ser_flip[1] == -coef,
         'flipped_phi_b_mutation_constructed', flipped_first_coefficient=q(ser_flip[1]))

    # ---- AW1 rule
    C.grid_start, C.threshold, rule_text = parse_rule(aw1c)
    need(C.threshold == coef / 2, 'rule_threshold_is_half_the_derived_coefficient', threshold=q(C.threshold))
    need(F(1, 10 ** C.grid_start) == C.cap, 'rule_grid_starts_at_cap')
    tau, rows = rule_eval(K)
    need(tau == C.cap and len(rows) == 1, 'aw2_tau_from_frozen_rule', tau_AW2=q(tau),
         K2_times_tau=q(K * tau), threshold=q(C.threshold), slack=q(C.threshold - K * tau),
         ratio_threshold_over_K2tau=q(C.threshold / (K * tau)))
    lit = contract['parameters']['tau_AW2'].split(' ')[0]
    need(F(lit) == tau and F(pre['tau']['value']) == tau, 'contract_literal_matches_rule_compared_after',
         literal=lit, note='the literal is compared after evaluation, never used as input')

    # ---- enclosures, exclusion and margins
    encp = enclose(tau)
    encm = enclose(-tau)
    need(encp == (F(1, 14400000000) - K * tau * tau, F(1, 14400000000) + K * tau * tau), 'enclosure_plus_tau',
         lo=q(encp[0]), hi=q(encp[1]))
    need(encm == (-encp[1], -encp[0]), 'enclosure_minus_tau_is_flip_image', lo=q(encm[0]), hi=q(encm[1]),
         role='replay (flip image and the same |tau| formula); not a second confirmation')
    C.excluded_at_cap = bool(encp[0] > C.reference and encm[1] < C.reference)
    need(C.excluded_at_cap is True, 'strict_exclusion_of_free_reference_both_signs',
         plus_lo_positive=True, minus_hi_negative=True)
    mex = exclusion_margin(tau, K)
    msg = sign_margin(tau, K)
    need(mex == msg - 1 and mex >= C.target, 'exclusion_margin_target_met', exclusion_margin=q(mex),
         floor_1e9=q(floor_to(mex, 10 ** 9)), target='>= ' + q(C.target))
    need(msg == 1 / (144 * K * tau) and floor_to(msg, 10 ** 9) == F(41400010489, 200000000), 'sign_margin_reported',
         sign_margin=q(msg), floor_1e9=q(floor_to(msg, 10 ** 9)))
    need(exclusion_margin(-tau, K) == mex and sign_margin(-tau, K) == msg, 'margins_equal_at_minus_tau')
    need((C.target <= mex) == (msg >= 3) == (K * tau <= F(1, 432)) and (msg >= 2) == (K * tau <= C.threshold),
         'margin_equivalences', note='m>=2 <=> s>=3 <=> K|tau|<=1/432; rule K|tau|<=1/288 <=> s>=2 <=> m>=1')
    decs = {}
    for name, (lo, hi) in (('+', encp), ('-', encm)):
        dl, dh = dec_directed(lo, False), dec_directed(hi, True)
        decs[name] = (dl, dh)
        need(F(dl) <= lo and F(dh) >= hi and F(dh) - F(dl) < 2 * (hi - lo), 'decimals_outward_' +
             ('plus' if name == '+' else 'minus'), lo_decimal=dl, hi_decimal=dh)
    encc = enclose(tau, K_ceil, label='outward_ceiling')
    need(encc[0] <= encp[0] and encc[1] >= encp[1] and encc[0] > 0
         and exclusion_margin(tau, K_ceil) >= C.target, 'outward_ceiling_variant_still_excludes',
         lo=dec_directed(encc[0], False), hi=dec_directed(encc[1], True),
         exclusion_margin_floor=q(floor_to(exclusion_margin(tau, K_ceil), 10 ** 9)))
    D = F(re.search(r'D_ii=(\d+/\d+)', av1['accepted']).group(1))
    need(-D <= encm[0] and encp[1] <= D, 'av1_bound_contains_enclosure', D_ii_preview=preview(D),
         ratio_hi_over_D=preview(encp[1] / D))
    # corollary on the punctured domain: K is a bound for every |tau|<=cap, s(|tau|) is decreasing in |tau|
    samples = [C.cap / 10 ** k for k in (1, 2, 3)]
    need(all(sign_margin(t, K) >= msg and enclose(t)[0] > 0 and enclose(-t)[1] < 0 for t in samples),
         'sign_on_punctured_domain_corollary', note='0<|tau|<=10^-8: 1/(144 K |tau|) >= 207, labelled corollary')
    kt = []
    for t in samples:
        J = 28 * t
        T = F(49, 144) * t / (1 - C.gp * J)
        eps = 2 * T + T * T
        kt.append((C.gp * J * T + 2 * T * T + eps * eps + t / 144 * eps * eps) / (t * t))
    need(all(x <= K for x in kt) and kt[0] > kt[1] > kt[2], 'itemization_monotone_samples_below_gate',
         previews=[preview(x) for x in kt])
    need(enclose(tau, box_N=2) == enclose(tau, box_N=7) == encp, 'volume_uniform_same_formula_two_boxes',
         boxes=['2', '7'])
    r1 = (coef * tau) / (coef * tau / 10)
    r2 = (K * tau * tau) / (K * (tau / 10) ** 2)
    need(r1 == 10 and r2 == 100, 'scaling_exponents_1_and_2', first_order_ratio=q(r1), remainder_ratio=q(r2))

    # ---- crude tier (retained failure)
    mc = re.search(r't_c=(\d+)\|tau\|, K_2~([0-9.e]+), margin ([0-9.]+)', gate['accepted'])
    tc = int(mc.group(1)) * tau
    Jc = 28 * tau
    epc = 2 * tc + tc * tc
    Kc = (C.gp * Jc * tc + 2 * tc * tc + epc * epc + tau / 144 * epc * epc) / (tau * tau)
    need(Kc == F(sk1['admitted_values']['K2_crude_tier_forward_and_skeptic'])
         and abs(Kc - F(mc.group(2))) < F(1, 10 ** 4) * Kc, 'crude_tier_recomputed', K2_crude=q(Kc))
    crude_lo, crude_hi = coef * tau - Kc * tau * tau, coef * tau + Kc * tau * tau
    sc = sign_margin(tau, Kc)
    crude_rule, _ = rule_eval(Kc)
    need(crude_lo < 0 < crude_hi and sc < 1 and exclusion_margin(tau, Kc) < 0
         and abs(sc - F(mc.group(3))) < F(1, 10 ** 4) and crude_rule == F(1, 10 ** 10),
         'crude_tier_fails_at_cap_retained', lo=dec_directed(crude_lo, False), hi=dec_directed(crude_hi, True),
         sign_margin=dec_directed(sc, False), exclusion_margin=dec_directed(exclusion_margin(tau, Kc), False),
         rule_value_comparison_only=q(crude_rule), verdict='limited_retained (tier control, not admissible)')

    verdict, sub = verdict_from(K)
    need(verdict == 'accepted_within_scope' and sub == ['static_not_dynamic'], 'verdict_mapping',
         synthetic={'s=2.5': verdict_from(F(1) / (F(5, 2) * 144 * C.cap))[0],
                    'no_constant': verdict_from(None)[0]})
    need(verdict_from(F(1) / (F(5, 2) * 144 * C.cap)) == ('limited', ['static_not_dynamic'])
         and verdict_from(Kc) == ('limited', ['static_not_dynamic', 'sign_certified_below_cap']),
         'verdict_mapping_synthetic_fixtures', label='synthetic constants; not results')

    # ---- the good packet (what a correct producer packet must contain)
    flags = {'continuum_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': True,
             'static_not_dynamic': True, 'dynamical_correction_claim': False, 'scientific_priority_verified': False,
             'sign_certified_below_cap': False, 'centered_correlation_shift_resolved': False,
             'mass_gap_claim': False, 'uniqueness_claim': False}
    good = {
        'producers': ['forward'], 'packages': {'forward': 'check.py'},
        'reverse_premise_isolation': 'not_applicable: single producer',
        'model_id': C.model_id, 'triple': ZERO_TRIPLE, 'cover': [list(r) for r in BOX_R], 'centering': 'none',
        'coupling': {'source': 'aw1_rule_from_gate', 'tau': tau},
        'K': K, 'first_order_coefficient': coef,
        'error_terms': {'first_order_exact': {'exponent': 1, 'value_per_tau': coef},
                        'second_order_remainder': {'exponent': 2, 'radius_per_tau2': K},
                        'arithmetic': {'status': 'not_applicable', 'reason': 'exact rationals; decimals outward only'}},
        'enclosures': {'+': {'lo': encp[0], 'hi': encp[1], 'lo_decimal': decs['+'][0], 'hi_decimal': decs['+'][1]},
                       '-': {'lo': encm[0], 'hi': encm[1], 'lo_decimal': decs['-'][0], 'hi_decimal': decs['-'][1]}},
        'minus_tau_role': 'replay', 'strict_exclusion': True, 'resolved_interaction_shift': True,
        'margins': {'tau': tau, 'K': K, 'margin_definition': '(|tau|/144 - K tau^2)/(K tau^2)',
                    'exclusion_margin': mex, 'sign_margin': msg},
        'verdict': 'accepted_within_scope', 'sub_labels': ['static_not_dynamic'],
        'effect_kind': 'static_equal_time_mean', 'flags': flags,
    }
    need(validate_packet(good) is True, 'reference_packet_valid')

    def mut(**changes):
        pk = _cp(good)
        for path, val in changes.items():
            keys = path.split('__')
            tgtd = pk
            for k_ in keys[:-1]:
                tgtd = tgtd[k_]
            tgtd[keys[-1]] = val
        return lambda: validate_packet(pk)

    def with_multiplier(mval, label='conservative'):
        encs = {}
        for s_, t_ in (('+', tau), ('-', -tau)):
            lo_, hi_ = coef * t_ - mval * K * tau * tau, coef * t_ + mval * K * tau * tau
            encs[s_] = {'lo': lo_, 'hi': hi_, 'lo_decimal': dec_directed(lo_, False),
                        'hi_decimal': dec_directed(hi_, True)}
        return mut(overlap_multiplier={'value': mval, 'label': label}, enclosures=encs)

    ids = list(contract['controls'])
    # 1
    control('missing_incoming_stars',
            [('three_incoming_stars_J_21', lambda: validate_k2_reconstruction(F(21), 49), 'incident stars'),
             ('faces_per_site_21_anchored_only', lambda: validate_k2_reconstruction(F(28), 21), 'incident stars')],
            [('four_stars_49_faces', lambda: validate_k2_reconstruction(F(28), 49))],
            star_sites=str(len(geo['star'])), J='4 x 7|tau| = 28|tau| (7|tau| = 21 faces x |tau|/3, I1.5)')
    # 2
    control('full_original_wilson_cover',
            [('cover_site_0_only', mut(cover=[[0, 0, 0]]), 'cover'),
             ('cover_orthant_star', mut(cover=[[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]]), 'cover')],
            owners_of_W_links=[list(o) for o in geo['W_owners']])
    # 3
    control('wrong_delta_alpha_hbar_clock',
            [('normalized_V_over_alpha_energy', lambda: validate_amplitude(phi_coef, energy_alpha), 'unit mixing'),
             ('alpha_V_over_normalized_energy', lambda: validate_amplitude(alpha_coef, energy_norm), 'unit mixing')],
            [('alpha_units', lambda: validate_amplitude(alpha_coef, energy_alpha)),
             ('normalized_units', lambda: validate_amplitude(phi_coef, energy_norm))],
            mixed_coefficients=[q(-2 * phi_coef / energy_alpha * F(1, 4)), q(-2 * alpha_coef / energy_norm * F(1, 4))],
            clock='static mean: no clock enters omega(W); s=alpha t_E/hbar is not used')
    # 4
    fx = dict(m=F(1, 10), a=F(2, 5), b=F(1, 5), x1=F(1, 3), x2=F(1, 7))
    corr = fx['x1'] * fx['a'] ** 2 + fx['x2'] * fx['b'] ** 2
    second = fx['m'] ** 2 + fx['x1'] * fx['a'] ** 2 + fx['x2'] * fx['b'] ** 2
    control('vector_versus_scalar_centering',
            [('m_hat_in_omega_W_path', mut(m_hat=F(1, 144)), 'centering'),
             ('vector_centering_label', mut(centering='vector'), 'centering'),
             ('scalar_subtracts_m_not_m2', lambda: validate_centering('scalar', second - fx['m'], **fx), 'centering'),
             ('equal_time_variance_for_vector', lambda: validate_centering('vector', fx['a'] ** 2 + fx['b'] ** 2, **fx),
              'centering')],
            [('vector_identity_fixture', lambda: validate_centering('vector', corr, **fx)),
             ('scalar_identity_fixture', lambda: validate_centering('scalar', second - fx['m'] ** 2, **fx))],
            fixture='<(W-m)e0,P(W-m)e0> = <We0,PWe0> - m^2 = x1 a^2 + x2 b^2, P=diag(1,x1,x2), Pe0=e0; synthetic',
            omega_W_path='uncentered: centering none read from the contract; no m_hat')
    # 5
    control('first_order_mean_charged',
            [('mean_zero_at_first_order', mut(first_order_coefficient=F(0)), 'first-order coefficient')],
            [('mean_tau_over_144', lambda: validate_first_order(coef, ['W']))], m1=q(coef))
    # 6
    control('tau_scaling_exponent',
            [('remainder_called_linear', mut(error_terms__second_order_remainder__exponent=1), 'tau scaling'),
             ('first_order_called_quadratic', mut(error_terms__first_order_exact__exponent=2), 'tau scaling')],
            first_order_ratio=q(r1), remainder_ratio=q(r2))
    # 7
    control('changed_model_relabelled',
            [('nonzero_triple', lambda: enclose(tau, triple=('0', '1/8', '0')), 'model changed'),
             ('beyond_cap_2e-8', lambda: enclose(2 * tau), 'model changed'),
             ('finite_graph_relabelled', mut(model_id='one_plaquette_finite_graph'), 'model changed')],
            [('cap_model', lambda: enclose(tau))])
    # 8
    inv_files = {REL[k]: PINNED[k] for k in PINNED}
    good_inv = {'files': inv_files, 'manifest_sha256': sha_bytes(json.dumps(inv_files, sort_keys=True).encode())}
    miss = dict(inv_files)
    del miss[REL['aw1_gate']]
    miss_inv = {'files': miss, 'manifest_sha256': sha_bytes(json.dumps(miss, sort_keys=True).encode())}
    tampered_gate = raw['aw1_gate'].replace(b'81108864767825329926713064490531229475390625',
                                            b'81108864767825329926713064490531229475390624')
    tamp = dict(inv_files)
    tamp[REL['aw1_gate']] = sha_bytes(tampered_gate)
    tamp_inv = {'files': tamp, 'manifest_sha256': sha_bytes(json.dumps(tamp, sort_keys=True).encode())}
    stale_inv = {'files': inv_files, 'manifest_sha256': '0' * 64}
    control('coherent_evidence_tampering',
            [('gate_snapshot_removed_manifest_rebound', lambda: validate_evidence(miss_inv), 'required snapshot missing'),
             ('gate_K2_edited_hash_rebound', lambda: validate_evidence(tamp_inv), 'pinned hash differs'),
             ('manifest_not_rebound', lambda: validate_evidence(stale_inv), 'manifest hash')],
            [('live_inventory', lambda: validate_evidence(good_inv))],
            second_source='the edited gate value would also differ from the contract K_2_plus string')
    # 9
    control('insufficient_verdict_retained',
            [('crude_relabelled_accepted', lambda: validate_retained('crude', 'accepted_within_scope', True),
              'insufficient tier relabelled'),
             ('crude_dropped', lambda: validate_retained('crude', 'limited_retained', False), 'dropped')],
            [('crude_retained', lambda: validate_retained('crude', 'limited_retained', True))],
            crude_sign_margin=dec_directed(sc, True))
    # 10
    control('exact_arithmetic_admission',
            [('float_tau', lambda: enclose(float(tau)), 'exact arithmetic'),
             ('float_K', lambda: enclose(tau, float(K)), 'exact arithmetic'),
             ('inward_decimal_lo', mut(**{'enclosures__+__lo_decimal': dec_directed(encp[0], True)}),
              'not widened outward'),
             ('inward_decimal_hi_minus', mut(**{'enclosures__-__hi_decimal': dec_directed(encm[1], False)}),
              'not widened outward')],
            [('fraction_inputs', lambda: enclose(tau, K))],
            preview_label='float previews only in the previews block; no Arb/mpmath in this standard-library replay')
    # 11
    control('root_n_misuse',
            [('radius_over_sqrt_volume', mut(error_terms__second_order_remainder__radius_per_tau2=K / 8), 'radius'),
             ('volume_averaged', mut(volume_scaling='1/sqrt(|Lambda_N|)'), 'root-N'),
             ('box_N_1', lambda: enclose(tau, box_N=1), 'box')],
            [('uniform_N2_N7', lambda: enclose(tau, box_N=7))])
    # 12
    control('no_priority_or_continuum_claim',
            [('flag_' + k_, mut(**{'flags': dict(flags, **{k_: True})}), 'forbidden claim')
             for k_ in ('continuum_claim', 'scientific_priority_verified', 'uniform_wilson_claim',
                        'dynamical_correction_claim', 'sign_certified_below_cap', 'centered_correlation_shift_resolved')])
    # 13
    control('haar_parity_exact',
            [('E_W2_as_norm', lambda: validate_first_order(-2 * amp * F(1, 2), ['W']), 'first-order coefficient'),
             ('reference_one_quarter_W2_value', lambda: validate_reference(F(1, 4), mom[1]), 'reference'),
             ('E_W_nonzero', lambda: validate_reference(F(0), F(1, 4)), 'reference')],
            [('exact_moments', lambda: validate_first_order(-2 * amp * mom[2], ['W'])),
             ('reference_zero', lambda: validate_reference(C.reference, mom[1]))],
            moments={'E[W]': q(mom[1]), 'E[W^2]': q(mom[2]), 'E[W^3]': q(mom[3]), 'E[W^4]': q(mom[4])})
    # 14
    control('wilson_mean_first_order_coefficient',
            [('aw1_literal_display', mut(first_order_coefficient=literal), 'first-order coefficient'),
             ('missing_factor_two', mut(first_order_coefficient=F(1, 288)), 'first-order coefficient'),
             ('norm_not_norm_squared', mut(first_order_coefficient=F(1, 72)), 'first-order coefficient'),
             ('flipped_phi_b_string', lambda: validate_sign_fixture(parse_i15(i1_flipped)[0], ser_flip),
              'sign convention'),
             ('flipped_fixture_series', lambda: validate_sign_fixture(sgn, ser_flip), 'sign convention')],
            [('plus_1_over_144', lambda: validate_first_order(coef, ['W'])),
             ('i15_one_plaquette_fixture', lambda: validate_sign_fixture(sgn, ser))],
            fixture_first_coefficient=q(ser[1]), flipped_first_coefficient=q(ser_flip[1]),
            first_order_at_cap=[q(coef * tau), q(-coef * tau)])
    # 15
    control('wrong_face_control',
            [('ten_faces_of_R', lambda: validate_first_order(10 * coef, ['W'] * 10), 'wrong face'),
             ('neighbour_face', lambda: validate_first_order(coef, ['xz:(0,1,0)']), 'wrong face'),
             ('W_excluded', lambda: validate_first_order(F(0), []), 'wrong face')],
            [('only_W', lambda: validate_first_order(coef, ['W']))],
            other_faces_meeting_R_zero=str(len(pair) - 1))
    # 16
    control('sign_flip_tau',
            [('sign_blind_replay', mut(**{'enclosures': {'+': good['enclosures']['+'], '-': good['enclosures']['+']}}),
              'enclosure endpoints'),
             ('minus_tau_as_confirmation', mut(minus_tau_role='second_confirmation'), 'replay')],
            [('negated_interval', lambda: validate_packet(good))])
    # 17
    radius_big = (coef * tau / (K * tau * tau)) * 2
    control('free_reference_exclusion',
            [('crude_enclosure_claimed_resolved',
              lambda: _free_ref_check(crude_lo, crude_hi, True), 'free reference inside'),
             ('touching_zero_claimed_strict', lambda: _free_ref_check(F(0), 2 * coef * tau, True), 'free reference inside'),
             ('radius_past_zero_claimed_resolved', with_multiplier(radius_big), 'free reference inside'),
             ('margin_relative_to_first_order',
              mut(margins=dict(good['margins'], margin_definition='(|tau|/144 - K tau^2)/(|tau|/144)',
                               exclusion_margin=1 - 144 * K * tau)), 'margin denominator'),
             ('margin_as_ratio_to_1_288',
              mut(margins=dict(good['margins'], margin_definition='(1/288)/(K tau)',
                               exclusion_margin=C.threshold / (K * tau))), 'margin denominator'),
             ('sign_margin_reported_as_exclusion_margin', mut(margins=dict(good['margins'], exclusion_margin=msg)),
              'margin denominator')],
            [('cap_enclosure', lambda: _free_ref_check(encp[0], encp[1], True))],
            reference=q(C.reference), wrong_denominators={'relative_to_first_order': dec_directed(1 - 144 * K * tau, False),
                                                          'ratio_to_1_288': dec_directed(C.threshold / (K * tau), False)})
    # 18
    control('second_order_remainder_itemized',
            [('remainder_dropped', mut(error_terms={'first_order_exact': good['error_terms']['first_order_exact'],
                                                     'arithmetic': good['error_terms']['arithmetic']}),
              'error term missing'),
             ('arithmetic_na_without_reason', mut(error_terms__arithmetic={'status': 'not_applicable'}),
              'without a stated reason'),
             ('forward_aw1_K2_substituted', mut(K=fwd), 'K_2 not the AW1 gate binding'),
             ('reverse_aw1_K2_substituted', mut(K=rev), 'K_2 not the AW1 gate binding')],
            [('gate_K2', lambda: validate_packet(good))],
            itemized=C.error_terms)
    # 19
    control('static_not_dynamic_effect',
            [(k_, (lambda k2=k_: validate_effect(k2)), 'static')
             for k_ in ('dynamical_correction', 'mass_gap_shift', 'susceptibility', 'correlation_shift')]
            + [('sub_label_missing', mut(sub_labels=[]), 'static')],
            [('static_mean', lambda: validate_effect('static_equal_time_mean'))])
    # 20
    control('aw2_coupling_rule_prefrozen',
            [('literal_coupling', mut(coupling={'source': 'literal', 'tau': tau}), 'coupling rule'),
             ('chosen_1e-9', mut(coupling={'source': 'aw1_rule_from_gate', 'tau': F(1, 10 ** 9)}), 'coupling rule'),
             ('off_grid_5e-9', mut(coupling={'source': 'aw1_rule_from_gate', 'tau': F(5, 10 ** 9)}), 'coupling rule'),
             ('above_cap_1e-7', mut(coupling={'source': 'aw1_rule_from_gate', 'tau': F(1, 10 ** 7)}), 'coupling rule')],
            [('rule_value', lambda: validate_coupling({'source': 'aw1_rule_from_gate', 'tau': tau}))],
            rule=rule_text)
    # 21
    control('wilson_overlap_single_component',
            [('factor_4_unlabelled', mut(overlap_multiplier={'value': F(4)}), 'overlap multiplier'),
             ('single_site_creations_counted', lambda: validate_first_order(coef, ['W', 'c_0', 'c_ez']), 'wrong face')],
            [('factor_4_labelled_conservative', with_multiplier(F(4)))],
            W_Omega_R_norm_squared=q(mom[2]), conservative_x4_sign_margin=dec_directed(msg / 4, False))
    # 22
    control('tier_mixing_rejected',
            [('crude_K_in_calculator', lambda: enclose(tau, Kc), 'K_2 not the AW1 gate binding'),
             ('crude_label', lambda: enclose(tau, tier='crude'), 'tier mixing'),
             ('crude_rule_coupling', mut(coupling={'source': 'aw1_rule_from_gate', 'tau': crude_rule}),
              'coupling rule'),
             ('crude_rule_eval', lambda: rule_eval(Kc, 'crude'), 'tier mixing')])
    # 23
    control('single_producer_declared',
            [('fabricated_reverse', mut(producers=['forward', 'reverse'],
                                        packages={'forward': 'check.py', 'reverse': 'check.py'}), 'single producer'),
             ('reverse_isolation_claimed', mut(reverse_premise_isolation='verified'), 'single producer')],
            [('forward_only', lambda: validate_packet(good))],
            admission_requires='skeptic single_direction_independent_replay (this package)')
    extra = [row['id'] for row in CHECKS if row.get('kind') == 'control']
    need(extra == ids, 'all_contract_controls_executed_in_order', n=str(len(ids)))
    need(validate_claims(flags) is True, 'claim_flags_valid')
    need('whole set of AQ1 subsequential limits' in selection and 'not a dynamical correction' in selection,
         'selection_scope_wording_read')

    scope = ('In the AM2/AQ1 zero-selected patterned family (selected triple exactly (0,0,0), Haar reference, '
             'whole stars phi_b=-(tau/3) sum W_f, cover R={0,e_z}), at tau=+-tau_AW2=+-10^-8: every state in the '
             'whole set of AQ1 subsequential limits (and every centered whole-star box N>=2 at every cutoff) has '
             'omega_tau(W) in [tau/144-K_2^+ tau^2, tau/144+K_2^+ tau^2], so sign(omega_tau(W))=sign(tau) and the '
             'free reference 0 is strictly excluded. Static equal-time mean only (static_not_dynamic); no dynamical '
             'correction, mass shift or susceptibility; the centered correlation shift remains unresolved '
             '(AV2 reference_unresolved). The -tau enclosure is a replay, not a second confirmation. No uniqueness, '
             'rate in N, uniform Wilson, weak-coupling, continuum or priority claim.')
    previews = {
        'K2_plus': preview(K), 'first_order_at_cap': preview(coef * tau), 'radius_at_cap': preview(K * tau * tau),
        'enclosure_plus': [preview(encp[0]), preview(encp[1])], 'enclosure_minus': [preview(encm[0]), preview(encm[1])],
        'exclusion_margin': preview(mex), 'sign_margin': preview(msg),
        'crude_K2': preview(Kc), 'crude_sign_margin': preview(sc),
        'label': 'floating previews only; no admission Boolean reads them',
    }
    result = {
        'loop': 'AW2', 'stage': 'pre_comparison_independent_replay', 'role': 'skeptic',
        'standing': 'model-agent skeptic with correlated ancestry; not human peer review, not formal verification',
        'human_author': 'Hruday N M (BUNZEEY)',
        'producer_files_read': [],
        'producers': list(contract['producers']), 'direction': contract['direction'],
        'reverse_premise_isolation': 'not_applicable: single producer',
        'contract_sha256': hashes['contract'],
        'inputs_sha256': {REL[k]: hashes[k] for k in sorted(REL)},
        'read_from_contract': {'target': {'quantity': tgt['quantity'], 'value': tgt['value'],
                                          'comparator': tgt['comparator']},
                               'reference_value_exact': obs['reference_value_exact'],
                               'tau_literal_compared_after_rule': lit},
        'K2_plus': {'exact': q(K), 'source': 'AW1 gate decision and accepted text (hash-pinned), equal to the '
                                              'contract K_2_plus string', 'outward_ceiling': q(K_ceil),
                    'reconstruction_equal': True},
        'aw2_rule': {'text': rule_text, 'grid_start': q(C.cap), 'threshold': q(C.threshold),
                     'evaluations': [{'tau': q(t_), 'K2_times_tau': q(v_), 'passes': ok_} for _, t_, v_, ok_ in rows],
                     'tau_AW2': q(tau), 'slack': q(C.threshold - K * tau)},
        'first_order': {'coefficient': q(coef), 'values': {'+': q(coef * tau), '-': q(-coef * tau)},
                        'i15_display': disp, 'contributing_face': 'W only'},
        'enclosure': {'+': {'tau': q(tau), 'lo': q(encp[0]), 'hi': q(encp[1]), 'lo_decimal_outward': decs['+'][0],
                            'hi_decimal_outward': decs['+'][1], 'excludes_zero': True},
                      '-': {'tau': q(-tau), 'lo': q(encm[0]), 'hi': q(encm[1]), 'lo_decimal_outward': decs['-'][0],
                            'hi_decimal_outward': decs['-'][1], 'excludes_zero': True},
                      'minus_tau_role': 'replay (flip image), not a second confirmation',
                      'outward_ceiling_variant': [dec_directed(encc[0], False), dec_directed(encc[1], True)]},
        'margins': {'exclusion_margin': q(mex), 'exclusion_margin_floor_1e-9': q(floor_to(mex, 10 ** 9)),
                    'sign_margin': q(msg), 'sign_margin_floor_1e-9': q(floor_to(msg, 10 ** 9)),
                    'definition_exclusion': '(|tau|/144 - K_2^+ tau^2)/(K_2^+ tau^2)',
                    'definition_sign': '1/(144 K_2^+ |tau|)', 'target': '>= ' + tgt['value'], 'target_met': True},
        'crude_tier': {'K2': q(Kc), 'enclosure_at_cap': [dec_directed(crude_lo, False), dec_directed(crude_hi, True)],
                       'contains_zero': True, 'sign_margin_upper': dec_directed(sc, True),
                       'status': 'fails at the cap; retained as a limited-tier control; rule value 10^-10 comparison only'},
        'fixture_one_plaquette': {'series': {str(k_): q(v_) for k_, v_ in ser.items()},
                                  'two_level_plus': [dec_directed(bp[0], False), dec_directed(bp[1], True)],
                                  'transfers_to_aq': False},
        'scope': scope,
        'proposed_verdict': verdict, 'sub_labels': sub,
        'previews': previews,
        'checks': CHECKS,
    }
    result.update(flags)
    return result


def _cp(x):
    """Deep copy of a packet preserving Fractions and tuples."""
    if isinstance(x, dict):
        return {k: _cp(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_cp(v) for v in x]
    return x


def _free_ref_check(lo, hi, claimed):
    ref = C.reference
    if claimed and not (ref < lo or hi < ref):
        raise Rejected('free reference inside enclosure => no interaction claim')
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('--output must be an absolute path')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('--output must be fresh (absent or empty)')
    result = execute()
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checks': len(result['checks']), 'tau_AW2': result['aw2_rule']['tau_AW2'],
                      'enclosure_plus': [result['enclosure']['+']['lo_decimal_outward'],
                                         result['enclosure']['+']['hi_decimal_outward']],
                      'exclusion_margin': result['previews']['exclusion_margin'],
                      'sign_margin': result['previews']['sign_margin']}))


if __name__ == '__main__':
    main()
