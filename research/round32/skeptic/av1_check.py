#!/usr/bin/env python3
"""Round32 AV1 skeptic pre-comparison checker.

Written after the AV1 contract freeze from the frozen contract and its shared
premises only, before reading research/round32/forward/av1/ or
research/round32/reverse/av1/. Nothing is imported from any producer.
Standard library only. Every admission Boolean is decided with
fractions.Fraction; floats appear only in the labelled 'previews' block.
Every check and control raises an explicit exception, so python -O cannot
disable it. Model-agent skeptic with correlated ancestry; not human peer review.

Usage: python3 -B research/round32/skeptic/av1_check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as F
from itertools import combinations
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / 'research/round32/contracts/av1.json'
I1_REPORT = ROOT / 'research/round21/forward/i1/report.md'


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
    """True iff fn() raises Rejected with the expected reason."""
    try:
        fn()
    except Rejected as exc:
        if reason not in str(exc):
            raise CheckFailure('rejected for the wrong reason: %s (expected %s)' % (exc, reason))
        return True
    return False


def accepts(fn):
    fn()
    return True


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(x):
    return str(x)


def preview(x):
    return format(float(x), '.12e')


# ---------------------------------------------------------------- exact tools
def exp_bounds(x, n=16):
    """Directed enclosure of exp(x) for 0 <= x <= 1/2 (Taylor + geometric tail)."""
    if not (F(0) <= x <= F(1, 2)):
        raise CheckFailure('exp argument out of range')
    s = F(0)
    term = F(1)
    for k in range(n + 1):
        s += term
        term = term * x / (k + 1)
    return s, s + term / (1 - x / (n + 2))


def arctan_bracket(x, n=30):
    """Consecutive partial sums of the alternating arctan series bracket arctan(x), 0<x<1."""
    s = F(0)
    parts = []
    for k in range(n):
        s += F((-1) ** k) * x ** (2 * k + 1) / (2 * k + 1)
        parts.append(s)
    lo, hi = sorted(parts[-2:])
    return lo, hi


def pi_bracket(den=10 ** 30):
    """Machin enclosure, then outward rounding to denominator 10^30."""
    a_lo, a_hi = arctan_bracket(F(1, 5))
    b_lo, b_hi = arctan_bracket(F(1, 239))
    lo, hi = 16 * a_lo - 4 * b_hi, 16 * a_hi - 4 * b_lo
    lo_r = F((lo.numerator * den) // lo.denominator, den)
    hi_r = F(-((-hi.numerator * den) // hi.denominator), den)
    if not (lo_r <= lo < hi <= hi_r):
        raise CheckFailure('pi rounding')
    return lo_r, hi_r


def sqrt_bracket(n, scale=10 ** 15):
    r = isqrt(n * scale * scale)
    lo, hi = F(r, scale), F(r + 1, scale)
    if r * r == n * scale * scale:
        hi = lo
    if not (lo * lo <= n <= hi * hi):
        raise CheckFailure('sqrt bracket')
    return lo, hi


# ---------------------------------------------------------------- geometry
AXES = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIENT = (('xy', 0, 1), ('xz', 0, 2), ('yz', 1, 2))
OFFSET_NAMES = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}
S_STAR = frozenset(OFFSET_NAMES.values())
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
COVER = frozenset([ORIGIN, EZ])


def add(p, v):
    return tuple(a + b for a, b in zip(p, v))


def sub(p, v):
    return tuple(a - b for a, b in zip(p, v))


def coarse(v):
    # I1.1: pi(x,y,z)=(floor(x/4),floor(y/2),z); Python // floors negatives.
    return (v[0] // 4, v[1] // 2, v[2])


def tails(b):
    return [(4 * b[0] + r, 2 * b[1] + s, b[2]) for r in range(4) for s in range(2)]


def anchored_faces(b):
    out = []
    for p in tails(b):
        r, s = p[0] - 4 * b[0], p[1] - 2 * b[1]
        for name, a, c in ORIENT:
            links = ((p, a), (p, c), (add(p, AXES[a]), c), (add(p, AXES[c]), a))
            out.append({'orient': name, 'r': r, 's': s, 'base': p,
                        'selected': name == 'xy' and s == 0 and r in (0, 1, 2),
                        'links': links,
                        'owners': frozenset(coarse(v) for v, _ in links)})
    return out


def parse_i1_table(text):
    row = re.compile(r'^\|\s*(xy|xz|yz):\s*r=([0-9,]+);\s*s=([0-9,]+)\s*\|\s*(\d+)\s*\|'
                     r'\s*`\{([^}]*)\}`\s*\|\s*(selected|omitted)\s*\|\s*$')
    classes = {}
    for line in text.splitlines():
        m = row.match(line.strip())
        if not m:
            continue
        rs = [int(x) for x in m.group(2).split(',')]
        ss = [int(x) for x in m.group(3).split(',')]
        if int(m.group(4)) != len(rs) * len(ss):
            raise CheckFailure('I1 table row count mismatch')
        support = frozenset(OFFSET_NAMES[x.strip()] for x in m.group(5).split(','))
        for r in rs:
            for s in ss:
                key = (m.group(1), r, s)
                if key in classes:
                    raise CheckFailure('duplicate I1 class')
                classes[key] = (support, m.group(6))
    return classes


def box(n):
    rng = range(-n, n + 1)
    return [(x, y, z) for x in rng for y in rng for z in rng]


def box_faces(n):
    sites = set(box(n))
    faces = []
    for b in sorted(sites):
        if all(add(b, o) in sites for o in S_STAR):
            faces += [f for f in anchored_faces(b) if not f['selected']]
    return sites, faces


# ---------------------------------------------------------------- SU(2)
def trivial_multiplicity(k):
    """Multiplicity of spin 0 in the k-fold tensor power of spin 1/2 (twice-spin DP)."""
    dist = {0: 1}
    for _ in range(k):
        new = {}
        for tj, m in dist.items():
            for nt in (tj - 1, tj + 1):
                if nt >= 0:
                    new[nt] = new.get(nt, 0) + m
        dist = new
    return dist.get(0, 0)


# ---------------------------------------------------------------- qubit creation fixtures
def vadd(u, v, c=F(1)):
    out = dict(u)
    for b, x in v.items():
        out[b] = out.get(b, F(0)) + c * x
    return {b: x for b, x in out.items() if x != 0}


def create(vec, mask, amp):
    out = {}
    for b, x in vec.items():
        if b & mask == 0:
            out[b | mask] = out.get(b | mask, F(0)) + amp * x
    return {b: x for b, x in out.items() if x != 0}


def one_minus(vec, mask, amp):
    return vadd(vec, create(vec, mask, amp), F(-1))


def product_state(creations, start=None):
    vec = {0: F(1)} if start is None else dict(start)
    for mask, amp in creations:
        vec = one_minus(vec, mask, amp)
    return vec


def inner(u, v):
    return sum((x * v.get(b, F(0)) for b, x in u.items()), F(0))


def reduced(vec, rmask, rstates):
    """Unnormalized reduced matrix on the R bits (real amplitudes)."""
    by_out = {}
    for b, x in vec.items():
        by_out.setdefault(b & ~rmask, {})[b & rmask] = x
    rho = {(i, j): F(0) for i in rstates for j in rstates}
    for comp in by_out.values():
        for i, xi in comp.items():
            for j, xj in comp.items():
                rho[(i, j)] += xi * xj
    return rho


def split_fixture(creations, rmask, rstates):
    psi = product_state(creations)
    outside = [(m, a) for m, a in creations if m & rmask == 0]
    meet = [(m, a) for m, a in creations if m & rmask]
    psi_out = product_state(outside)
    delta = vadd(psi, psi_out, F(-1))
    singles = {}
    for m, a in meet:
        singles = vadd(singles, create(psi_out, m, a))
    pairs = {}
    for (m1, a1), (m2, a2) in combinations(meet, 2):
        if m1 & m2 == 0:
            pairs = vadd(pairs, create(create(psi_out, m2, a2), m1, a1))
    triples_zero = all(not create(create(create(psi_out, m3, a3), m2, a2), m1, a1)
                       for (m1, a1), (m2, a2), (m3, a3) in combinations(meet, 3))
    n_out = inner(psi_out, psi_out)
    n_delta = inner(delta, delta)
    z = inner(psi, psi)
    rho_un = reduced(psi, rmask, rstates)
    rho = {k: v / z for k, v in rho_un.items()}
    phi_out = {b: x for b, x in psi_out.items()}
    xi = {r: F(0) for r in rstates}
    sigma = reduced(delta, rmask, rstates)
    for b, x in delta.items():
        xi[b & rmask] += x * phi_out.get(b & ~rmask, F(0))
    return {'psi': psi, 'psi_out': psi_out, 'delta': delta, 'singles': singles, 'pairs': pairs,
            'triples_zero': triples_zero, 'n_out': n_out, 'n_delta': n_delta, 'z': z,
            'rho': rho, 'rho_un': rho_un, 'xi': xi, 'sigma': sigma, 'meet': meet}


def density_from_parts(fx, rstates, drop=None):
    rho = {}
    zden = fx['n_out'] + (F(0) if drop == 'normalization' else fx['n_delta'])
    for i in rstates:
        for j in rstates:
            v = F(0)
            if i == 0 and j == 0:
                v += fx['n_out']
            if i == 0 and drop != 'bra_cross':
                v += fx['xi'][j]
            if j == 0 and drop != 'ket_cross':
                v += fx['xi'][i]
            if drop != 'sigma':
                v += fx['sigma'][(i, j)]
            rho[(i, j)] = v / zden
    return rho


def site_sums(creations, sites):
    return {u: sum((abs(a) for m, a in creations if m >> u & 1), F(0)) for u in sites}


# ---------------------------------------------------------------- linear algebra (cutoff fixture)
def mat_mul(a, b):
    n, m, p = len(a), len(b), len(b[0])
    return [[sum((a[i][k] * b[k][j] for k in range(m)), F(0)) for j in range(p)] for i in range(n)]


def mat_inv(a):
    n = len(a)
    m = [row[:] + [F(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        piv = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        pv = m[c][c]
        m[c] = [x / pv for x in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [row[n:] for row in m]


def transpose(a):
    return [list(r) for r in zip(*a)]


# ---------------------------------------------------------------- validators (explicit exceptions)
def validate_tier_packet(p):
    if p['remainder'] == 0:
        raise Rejected('remainder set to zero')
    if p['remainder_tier'] != p['first_order_tier']:
        raise Rejected('tier mixing')
    if p['t'] < p['t1'] / (1 - p['kappa']):
        raise Rejected('refined t without self-consistent inequality')
    return True


def validate_scaling(claim, ratio_lo, ratio_hi):
    band = {'linear': (F(99), F(101)), 'sqrt': (F(99, 10), F(101, 10))}[claim]
    if not (band[0] <= ratio_lo and ratio_hi <= band[1]):
        raise Rejected('scaling exponent mismatch')
    return True


def validate_model(packet, contract_tau, allowed_scaling_tau):
    if packet['triple'] != ('0', '0', '0'):
        raise Rejected('changed model')
    if packet['label'] == 'cap' and abs(packet['tau']) != contract_tau:
        raise Rejected('changed model')
    if packet['label'] == 'scaling_control' and abs(packet['tau']) != allowed_scaling_tau:
        raise Rejected('changed model')
    if packet['model_id'] != 'AQ_patterned_zero_selected':
        raise Rejected('changed model')
    return True


def validate_evidence(packet, required):
    body = json.dumps(packet['checks'], sort_keys=True)
    if hashlib.sha256(body.encode()).hexdigest() != packet['sha256']:
        raise Rejected('hash mismatch')
    got = {c['id']: c['passed'] for c in packet['checks']}
    for cid in required:
        if got.get(cid) is not True:
            raise Rejected('required control missing or false')
    return True


def validate_exact(values):
    for v in values:
        if type(v) is not F:
            raise Rejected('non-exact admission value')
    return True


def validate_claims(flags):
    for key in ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift',
                'scientific_priority_verified', 'euclidean_node_certified', 'first_order_parity_claim',
                'uniqueness_claim', 'whole_sequence_convergence_claim', 'rate_in_N_claim'):
        if flags.get(key) is not False:
            raise Rejected('forbidden claim ' + key)
    return True


def validate_uniform(values):
    if len(set(values)) != 1:
        raise Rejected('volume-dependent')
    return True


def validate_equal(candidate, truth, what):
    if candidate != truth:
        raise Rejected(what + ' mismatch')
    return True


def validate_count(claimed, derived, label):
    if label == 'labelled_bound':
        if claimed < derived:
            raise Rejected('bound below derived count')
        return True
    if claimed != derived:
        raise Rejected('count differs from derivation')
    return True


def validate_site_scope(examined, all_sites, claimed, true_max):
    if set(examined) != set(all_sites):
        raise Rejected('count restricted to a subset of sites')
    if claimed != true_max:
        raise Rejected('count differs from all-site maximum')
    return True


def validate_eps_rule(rule):
    if rule != 'linear':
        raise Rejected('deterministic terms add linearly')
    return True


def validate_premises(shared):
    bad = ('skeptic/triage.md', '/deliberation-', 'loop2-response.md', 'forward/av', 'reverse/av')
    for p in shared:
        if any(b in p for b in bad):
            raise Rejected('reverse premise isolation')
    return True


def validate_passage(argument):
    if argument['uniform_gap'] < F(1, 2):
        raise Rejected('eigenvalue convergence alone')
    if argument['topology'] != 'local_trace_norm':
        raise Rejected('wrong topology')
    return True


def validate_mean(packet):
    if packet['m_squared_charge'] == 0:
        raise Rejected('zero mean assumed')
    return True


def validate_centering(kind, m, d, residue):
    expected = d * d if kind == 'vector' else -2 * m * d - d * d
    if residue != expected:
        raise Rejected('centering residue mismatch')
    return True


def validate_units(amp_normalized, amp_alpha):
    if amp_normalized != amp_alpha:
        raise Rejected('unit mismatch')
    return True


def validate_target(tier, value, target, reported):
    if (value <= target) != reported:
        raise Rejected('target Boolean retuned')
    return True


# ---------------------------------------------------------------- main computation
def execute():
    contract_bytes = CONTRACT.read_bytes()
    contract = json.loads(contract_bytes)
    need(contract.get('id') == 'AV1' and contract.get('status') == 'frozen_before_production',
         'contract_frozen_identity')
    tau_cap = F(contract['parameters']['tau_cap'])
    target = F(contract['preregistration']['target']['value'])
    triple = tuple(contract['parameters']['selected_coefficients_over_alpha'])
    ref_w = F(contract['parameters']['reference_moments']['omega_0(W)'])
    ref_w2 = F(contract['parameters']['reference_moments']['omega_0(W^2)'])
    need(tau_cap == F(1, 10 ** 8) and target == F(4, 10 ** 7) and triple == ('0', '0', '0')
         and contract['preregistration']['target']['comparator'] == '<=',
         'contract_target_and_reference_read', target=q(target), tau_cap=q(tau_cap))
    need(len(contract['controls']) == 25 and contract['controls'] == contract['preregistration']['controls_required']['ids'],
         'contract_controls_equal_prereg_ids')

    # ---------------- I1 classes: geometry derivation versus the printed table
    table = parse_i1_table(I1_REPORT.read_text())
    geo = {}
    for f in anchored_faces(ORIGIN):
        geo[(f['orient'], f['r'], f['s'])] = (f['owners'], 'selected' if f['selected'] else 'omitted')
    need(len(table) == 24 and table == geo, 'i1_table_equals_geometry_derivation', classes='24')
    omitted = sorted(((k, v[0]) for k, v in table.items() if v[1] == 'omitted'), key=lambda kv: kv[0])
    n_omitted = len(omitted)
    need(n_omitted == 21 and sum(1 for v in table.values() if v[1] == 'selected') == 3, 'i1_21_omitted_3_selected')
    need(all(ORIGIN in s and s <= S_STAR and len(s) >= 2 for _, s in omitted), 'every_omitted_class_anchored_and_crossing')

    # ---------------- counts by translation covariance (from the table)
    per_factor = sum(len(s) for _, s in omitted)
    owner_sets = {}
    for _, s in omitted:
        for o in s:
            key = frozenset(sub(x, o) for x in s)
            owner_sets[key] = owner_sets.get(key, 0) + 1
    mults = sorted(owner_sets.values())
    meeting, inside, containing = set(), set(), set()
    for k, s in omitted:
        for rr in COVER:
            for o in s:
                b = sub(rr, o)
                support = frozenset(add(b, x) for x in s)
                meeting.add((k, b))
                if support <= COVER:
                    inside.add((k, b))
                if COVER <= support:
                    containing.add((k, b))
    n_meet, n_inside, n_contain = len(meeting), len(inside), len(containing)
    # Candidates are read from the contract text (item 11) and compared with the derivation above.
    cand = re.search(r'counts (\d+) \(omitted faces per factor\), (\d+) \(owner sets per factor\), '
                     r'(\d+) \(faces meeting R\) and (\d+) \(faces inside R\)', ' '.join(contract['required']))
    if cand is None:
        raise CheckFailure('contract candidate counts not found')
    c49, c15, c82, c10 = (int(x) for x in cand.groups())
    need(per_factor == c49 and sum(mults) == per_factor, 'derived_faces_per_factor', value=str(per_factor))
    need(len(owner_sets) == c15 and mults == [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 10, 10],
         'derived_owner_sets_per_factor', value=str(len(owner_sets)), multiplicities=[str(x) for x in mults])
    need(n_meet == 2 * per_factor - n_contain and n_meet == c82, 'derived_faces_meeting_R', value=str(n_meet))
    need(n_inside == c10 and n_contain == 16, 'derived_faces_inside_and_containing_R',
         inside=str(n_inside), containing=str(n_contain))
    n_straddle = n_meet - n_inside
    need(n_straddle == 72, 'derived_straddling_faces_meeting_R', value=str(n_straddle))
    need(4 * n_omitted == 84 and 84 >= per_factor and 2 * 84 >= n_meet, 'labelled_bounds_84_168')

    # ---------------- brute force on centered boxes, all sites
    brute = {}
    wilson = None
    for n in (1, 2, 3):
        sites, faces = box_faces(n)
        per_site = {u: {} for u in sites}
        for f in faces:
            for u in f['owners']:
                rel = frozenset(sub(x, u) for x in f['owners'])
                per_site[u][rel] = per_site[u].get(rel, 0) + 1
        dominated = all(all(owner_sets.get(rel, 0) >= c for rel, c in d.items()) for d in per_site.values())
        maxcount = max(sum(d.values()) for d in per_site.values())
        m_r = sum(1 for f in faces if f['owners'] & COVER)
        i_r = sum(1 for f in faces if f['owners'] <= COVER)
        brute[n] = {'faces': len(faces), 'max_per_site': maxcount, 'meet_R': m_r, 'inside_R': i_r,
                    'dominated': dominated, 'sites': len(sites)}
        if n == 2:
            link_faces = {}
            for idx, f in enumerate(faces):
                if len(set(f['links'])) != 4:
                    raise CheckFailure('face with repeated link')
                for l in f['links']:
                    link_faces.setdefault(l, []).append(idx)
            shared = {}
            for lst in link_faces.values():
                for i, j in combinations(sorted(lst), 2):
                    shared[(i, j)] = shared.get((i, j), 0) + 1
            max_shared = max(shared.values())
            wf = [f for f in faces if f['base'] == ORIGIN and f['orient'] == 'xz']
            wilson = wf[0] if len(wf) == 1 else None
            faces2, sites2, per_site2 = faces, sites, per_site
    need(brute[2]['max_per_site'] == per_factor and brute[3]['max_per_site'] == per_factor
         and brute[1]['max_per_site'] <= per_factor and all(b['dominated'] for b in brute.values()),
         'face_count_bulk_attained_boundary_at_most_bulk',
         max_N1=str(brute[1]['max_per_site']), max_N2=str(brute[2]['max_per_site']))
    need(brute[2]['meet_R'] == n_meet == brute[3]['meet_R'] and brute[2]['inside_R'] == n_inside
         and brute[1]['meet_R'] < n_meet, 'brute_force_R_counts_match_covariance',
         meet_R_N1=str(brute[1]['meet_R']))
    need(max_shared == 1, 'distinct_faces_share_at_most_one_link')
    need(wilson is not None and wilson['owners'] == COVER
         and [coarse(v) for v, _ in wilson['links']] == [ORIGIN, ORIGIN, ORIGIN, EZ],
         'wilson_face_is_omitted_xz_face_with_owner_set_R')

    # ---------------- SU(2) moments, eigenvalue, norms
    mom = [F(trivial_multiplicity(k), 2 ** k) for k in range(5)]
    casimir = F(1, 2) * F(3, 2)
    onsite_factor = F(8)
    energy_norm = onsite_factor * 4 * casimir
    need(mom[1] == 0 and mom[2] == F(1, 4) and mom[3] == 0 and mom[4] == F(1, 8) and ref_w == mom[1] and ref_w2 == mom[2],
         'haar_moments_exact', EW2=q(mom[2]), EW4=q(mom[4]))
    need(energy_norm == 24 and energy_norm / onsite_factor == 3 and casimir * onsite_factor == 6,
         'face_vector_H0_eigenvalue_24_gap_6')
    amp_norm = F(1, 3) / energy_norm
    amp_alpha = F(1, 24) / (energy_norm / onsite_factor)
    need(amp_norm == F(1, 72) and amp_alpha == amp_norm, 'first_order_amplitude_tau_over_72')
    face_norm = amp_norm * F(1, 2)
    need(face_norm == F(1, 144), 'face_vector_norm_tau_over_144')

    # ---------------- AM2 constants
    R = F(1, 64)
    e_lo, e_hi = exp_bounds(F(1, 8))
    need(e_hi < F(8, 7) and e_lo > 1, 'certified_exp_one_eighth_below_8_7', upper=q(e_hi))
    G_R = 16 * F(8, 7) * (1 + 10 * R)
    Gp_R = 16 * F(8, 7) * (18 + 80 * R)
    need(G_R == F(148, 7) and Gp_R == 352 and 16 * e_hi * (1 + 10 * R) < G_R and 16 * e_hi * (18 + 80 * R) < Gp_R,
         'am2_G_and_Gprime_at_R')
    star_norm = n_omitted * F(1, 3)
    J_coef = len(S_STAR) * star_norm
    J0 = J_coef * tau_cap
    need(star_norm == 7 and J_coef == 28 and J0 == F(7, 25000000), 'per_site_J_28_tau_derived')
    need(J0 * G_R == F(148, 25000000) and J0 * G_R < R and 2 * J0 * Gp_R < 1, 'am2_ball_and_contraction')
    for k in range(9):
        lk = 16 * 8 ** k * (1 + F(5 * k, 4))
        series = F(16 * 8 ** k) / fact(k) + (F(160 * 8 ** (k - 1)) / fact(k - 1) if k else 0)
        if lk / fact(k) != series:
            raise CheckFailure('am2 majorant coefficient')
    need(True, 'am2_majorant_series_coefficients')

    def G_up(t):
        return 16 * exp_bounds(8 * t)[1] * (1 + 10 * t)

    # ---------------- grouped first-order anchored norm
    sq_hi = F(0)
    sq_lo = F(0)
    for m in owner_sets.values():
        lo, hi = sqrt_bracket(m)
        sq_hi += hi
        sq_lo += lo
    need(sq_hi < per_factor and sq_lo <= sq_hi, 'grouped_sqrt_sum_below_triangle', grouped_upper=q(sq_hi))

    # ---------------- tiers
    def eps_of(t):
        return 2 * t + t * t

    def d_forward(e):
        return 2 * e * (1 + e) / (1 + e * e)

    def d_purification(e):
        # 2e/sqrt(1+e^2) lies in [2e-e^3, 2e]; verified by squaring, no series premise.
        lo = 2 * e - e ** 3
        hi = 2 * e
        if not (lo * lo * (1 + e * e) <= 4 * e * e <= hi * hi * (1 + e * e)):
            raise CheckFailure('purification bracket')
        return lo, hi

    def tiers(tau):
        a = abs(tau)
        J = J_coef * a
        out = {}
        t_i = J * G_R
        if not t_i <= R:
            raise CheckFailure('tier i outside ball')
        out['i'] = {'t': t_i, 'rule': 't<=J*G(R), J=28|tau|, G(R)<148/7'}
        T = t_i
        for _ in range(3):
            T_new = ceil_frac(J * G_up(T), 10 ** 20)
            if not T_new <= T:
                raise CheckFailure('iteration not decreasing')
            T = T_new
        out['i_iterated'] = {'t': T, 'rule': 'three iterations t<-J*G_up(t) from J*G(R), directed exp'}
        kappa = Gp_R * J
        for name, t1 in (('ii', per_factor * face_norm * a), ('ii_grouped', sq_hi * face_norm * a)):
            t = t1 / (1 - kappa)
            if not (t <= R and t1 + kappa * t == t and G_up(t) - 16 <= Gp_R * t):
                raise CheckFailure('tier ii self-consistency')
            out[name] = {'t': t, 't1': t1, 'remainder_bound': kappa * t, 'kappa': kappa,
                         'rule': 't<=t1/(1-352J); ||c-c1||_a<=352*J*t'}
        for v in out.values():
            e = eps_of(v['t'])
            v['eps'] = e
            v['D_forward'] = d_forward(e)
            v['D_purification_lo'], v['D_purification_hi'] = d_purification(e)
            if not (v['D_purification_hi'] <= v['D_forward'] and v['D_forward'] <= 2 * e + 2 * e * e):
                raise CheckFailure('route ordering')
        out['J'] = J
        return out

    taus = {'+1e-8': tau_cap, '-1e-8': -tau_cap, '+1e-10': tau_cap / 100}
    res = {k: tiers(v) for k, v in taus.items()}
    need(all(res['+1e-8'][t][f] == res['-1e-8'][t][f] for t in ('i', 'i_iterated', 'ii', 'ii_grouped')
             for f in ('t', 'eps', 'D_forward', 'D_purification_hi')), 'both_signs_identical_bounds_depend_on_abs_tau')
    cap = res['+1e-8']
    need(cap['i']['t'] == F(37, 6250000) and cap['ii']['t'] == F(49, 14398580736), 'tier_t_values_exact',
         t_i=q(cap['i']['t']), t_ii=q(cap['ii']['t']))
    for tier in ('i', 'i_iterated', 'ii', 'ii_grouped'):
        v = cap[tier]
        v['omega_W_bound'] = v['D_forward']
        v['omega_W2_bound'] = v['D_forward'] / 2
        v['m_squared_bound'] = v['D_forward'] ** 2
        v['D_meets_4e-7'] = v['D_forward'] <= target
        v['D_meets_1e-6'] = v['D_forward'] <= F(1, 10 ** 6)
        v['Dpur_meets_4e-7'] = v['D_purification_hi'] <= target
    need(cap['ii']['D_meets_4e-7'] is True and cap['ii']['D_meets_1e-6'] is True and cap['ii']['Dpur_meets_4e-7'] is True
         and cap['ii_grouped']['D_meets_4e-7'] is True, 'tier_ii_meets_av2_threshold_4e-7_and_1e-6')
    need(cap['i']['D_meets_4e-7'] is False and cap['i']['D_meets_1e-6'] is False
         and cap['i_iterated']['D_meets_1e-6'] is False, 'tier_i_fails_both_targets_retained')

    # ---------------- scaling
    small = res['+1e-10']
    scal = {}
    for tier in ('i', 'ii'):
        rf = cap[tier]['D_forward'] / small[tier]['D_forward']
        rlo = cap[tier]['D_purification_lo'] / small[tier]['D_purification_hi']
        rhi = cap[tier]['D_purification_hi'] / small[tier]['D_purification_lo']
        scal[tier] = {'forward_ratio': rf, 'purification_ratio_lo': rlo, 'purification_ratio_hi': rhi}
        need(validate_scaling('linear', rf, rf) and validate_scaling('linear', rlo, rhi),
             'scaling_ratio_linear_tier_' + tier, ratio=preview(rf))
    at4_sq_ratio = (4 * 49 * tau_cap / 3) / (4 * 49 * (tau_cap / 100) / 3)
    need(at4_sq_ratio == 100 and F(99, 10) ** 2 <= at4_sq_ratio <= F(101, 10) ** 2, 'at4_sqrt_ratio_exactly_10')

    # ---------------- AV2 feasibility
    pi_lo, pi_hi = pi_bracket()
    need(F(333, 106) < pi_lo < pi_hi < F(355, 113), 'machin_pi_bracket')
    dyn_hi = 49 * tau_cap / pi_lo
    dyn_lo = 49 * tau_cap / pi_hi

    def av2_hi(D):
        return 2 * (D + D * D) + dyn_hi

    def av2_lo(D):
        return 2 * (D + D * D) + dyn_lo

    one_e6 = F(1, 10 ** 6)
    need(av2_hi(target) <= one_e6 and av2_hi(F(422, 10 ** 9)) <= one_e6 and av2_lo(F(423, 10 ** 9)) > one_e6
         and av2_hi(cap['ii']['D_forward']) <= one_e6 and av2_lo(cap['i']['D_forward']) > one_e6,
         'av2_threshold_bracket_4.22e-7')

    # ---------------- fixture A: two-site R, straddling, two-creation, padding
    a, b1, d, e2, s, g, h = F(1, 5), F(1, 7), F(1, 11), F(1, 13), F(1, 6), F(-1, 4), F(1, 3)
    base_cr = [(0b001, a), (0b010, b1), (0b011, d), (0b101, e2), (0b110, s), (0b100, g)]
    rmask, rstates = 0b011, (0, 1, 2, 3)
    fams = []
    for pad in range(4):
        cr = base_cr + [(1 << (3 + k), h) for k in range(pad)]
        fams.append((cr, split_fixture(cr, rmask, rstates)))
    cr0, fx = fams[0]
    # e^{-C} Omega by the nilpotent series equals the ordered product
    series = {0: F(1)}
    term = {0: F(1)}
    for k in range(1, 8):
        nxt = {}
        for m, amp in cr0:
            nxt = vadd(nxt, create(term, m, amp))
        term = {bb: -x / k for bb, x in nxt.items()}
        series = vadd(series, term)
    need(not term and series == fx['psi'] and product_state(list(reversed(cr0))) == fx['psi'],
         'fixture_exp_minus_C_equals_commuting_product')
    delta_formula = vadd(fx['pairs'], fx['singles'], F(-1))
    need(fx['triples_zero'] and delta_formula == fx['delta'] and len(fx['pairs']) > 0, 'fixture_split_with_two_creation_term')
    need(inner(fx['delta'], fx['psi_out']) == 0 and fx['xi'][0] == 0 and fx['z'] == fx['n_out'] + fx['n_delta'],
         'fixture_orthogonality_and_norm_split')
    rho_dec = density_from_parts(fx, rstates)
    need(rho_dec == fx['rho'], 'fixture_reduced_density_decomposition_exact')
    e_sq = fx['n_delta'] / fx['n_out']
    need(fx['rho'][(0, 0)] == 1 / (1 + e_sq), 'fixture_vacuum_overlap_one_over_one_plus_e2', e_squared=q(e_sq))
    sums = site_sums(cr0, range(3))
    t_R = max(sums[0], sums[1])
    t_all = max(sums.values())
    meet_sum = sum((abs(amp) for m, amp in cr0 if m & rmask), F(0))
    need(meet_sum <= sums[0] + sums[1] <= 2 * t_R and meet_sum > t_R
         and fx['n_delta'] <= eps_of(t_R) ** 2 * fx['n_out'] and t_R <= t_all, 'fixture_delta_bound_2t_plus_t2')
    xi_sq = sum((x * x for x in fx['xi'].values()), F(0))
    need(xi_sq <= fx['n_out'] * fx['n_delta'] and sum((fx['sigma'][(r, r)] for r in rstates), F(0)) == fx['n_delta'],
         'fixture_forward_route_ingredients')

    # fixture B: one-site R, exact 2x2 trace norm
    crB = [(0b001, F(1, 4)), (0b011, F(1, 5)), (0b010, F(-1, 3)), (0b100, F(1, 7)), (0b110, F(1, 6))]
    fB = split_fixture(crB, 0b001, (0, 1))
    r11, r01 = fB['rho'][(1, 1)], fB['rho'][(0, 1)]
    tn_sq = 4 * (r11 * r11 + r01 * r01)
    eB = fB['n_delta'] / fB['n_out']
    e_lo_B = sqrt_bracket_frac(eB)[0]
    tB = max(site_sums(crB, range(3))[0], F(0))
    need(fB['rho'][(0, 0)] + r11 == 1 and tn_sq <= 4 * eB / (1 + eB) and tn_sq <= d_forward(e_lo_B) ** 2
         and tn_sq <= d_forward(eps_of(tB)) ** 2 and tn_sq > 0 and tn_sq >= 4 * r11 * r11,
         'fixture_exact_trace_norm_within_both_route_bounds', trace_norm_squared=q(tn_sq))

    # cutoff-vector fixture: gap inequality with a rational orthogonal frame
    A = [[F(0), F(-1, 2), F(-1, 3)], [F(1, 2), F(0), F(-1, 5)], [F(1, 3), F(1, 5), F(0)]]
    I3 = [[F(int(i == j)) for j in range(3)] for i in range(3)]
    O = mat_mul(mat_inv([[I3[i][j] - A[i][j] for j in range(3)] for i in range(3)]),
                [[I3[i][j] + A[i][j] for j in range(3)] for i in range(3)])
    need(mat_mul(transpose(O), O) == I3, 'cutoff_fixture_rational_orthogonal_frame')
    H = mat_mul(mat_mul(O, [[F(0), 0, 0], [0, F(1, 2), 0], [0, 0, F(2)]]), transpose(O))
    u = [O[i][0] for i in range(3)]
    Hu = [sum((H[i][j] * u[j] for j in range(3)), F(0)) for i in range(3)]
    phis = [[F(1), F(0), F(0)], [F(1), F(1, 10), F(-1, 20)], [F(0), F(1), F(1)]]
    ok = all(Hu[i] == 0 for i in range(3))
    for phi in phis:
        nphi = sum((x * x for x in phi), F(0))
        ov = sum((x * y for x, y in zip(u, phi)), F(0))
        energy = sum((phi[i] * H[i][j] * phi[j] for i in range(3) for j in range(3)), F(0))
        ok = ok and (nphi - ov * ov) * F(1, 2) <= energy
    need(ok, 'cutoff_fixture_gap_inequality_forces_vector_overlap')

    # ---------------------------------------------------------------- the 25 contract controls
    flags = {'continuum_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False,
             'scientific_priority_verified': False, 'euclidean_node_certified': False,
             'first_order_parity_claim': False, 'uniqueness_claim': False,
             'whole_sequence_convergence_claim': False, 'rate_in_N_claim': False}

    incident = {sub(rr, o) for rr in COVER for o in S_STAR}
    orthant = {bb for bb in incident if min(bb) >= 0}
    orthant_faces = sum(1 for k, bb in meeting if bb in orthant)
    need(len(incident) == 7 and len(orthant) == 2 and accepts(lambda: validate_count(n_meet, c82, 'exact'))
         and rejects(lambda: validate_count(orthant_faces, n_meet, 'exact'), 'count differs'),
         'missing_incoming_stars', orthant_faces=str(orthant_faces))

    links = set()
    ends = set()
    for bb in COVER:
        for p in tails(bb):
            for ax in range(3):
                links.add((p, ax))
                ends.update((p, add(p, AXES[ax])))
    need(len(links) == 48 and len(ends) == 36 and set(wilson['links']) < links
         and rejects(lambda: validate_count(len(wilson['links']), len(links), 'exact'), 'count differs'),
         'full_original_wilson_cover')

    alpha = F(24, 5)
    delta_u = alpha / 8
    need(energy_norm * delta_u == 3 * alpha and accepts(lambda: validate_units(amp_norm, amp_alpha))
         and rejects(lambda: validate_units(F(1, 3) / 3, amp_alpha), 'unit mismatch')
         and rejects(lambda: validate_units(F(1, 24) / 24, amp_alpha), 'unit mismatch'),
         'wrong_delta_alpha_hbar_clock')

    m0, d0 = F(1, 4), F(1, 100)
    need(accepts(lambda: validate_centering('vector', m0, d0, F(1, 10000)))
         and accepts(lambda: validate_centering('scalar', m0, d0, F(-51, 10000)))
         and rejects(lambda: validate_centering('scalar', m0, d0, F(1, 10000)), 'centering residue')
         and m0 * m0 == F(1, 16), 'vector_versus_scalar_centering')

    need(accepts(lambda: validate_mean({'m_squared_charge': cap['ii']['m_squared_bound']}))
         and rejects(lambda: validate_mean({'m_squared_charge': F(0)}), 'zero mean'),
         'first_order_mean_charged')

    need(rejects(lambda: validate_scaling('linear', F(10), F(10)), 'scaling exponent')
         and accepts(lambda: validate_scaling('sqrt', F(10), F(10)))
         and rejects(lambda: validate_scaling('sqrt', scal['ii']['forward_ratio'], scal['ii']['forward_ratio']), 'scaling exponent'),
         'tau_scaling_exponent')

    good = {'triple': triple, 'label': 'cap', 'tau': -tau_cap, 'model_id': contract['preregistration']['model_id']}
    need(accepts(lambda: validate_model(good, tau_cap, tau_cap / 100))
         and rejects(lambda: validate_model(dict(good, tau=F(1, 10 ** 14)), tau_cap, tau_cap / 100), 'changed model')
         and rejects(lambda: validate_model(dict(good, triple=('0', '1/8', '0')), tau_cap, tau_cap / 100), 'changed model')
         and rejects(lambda: validate_model(dict(good, label='cap', tau=tau_cap / 100), tau_cap, tau_cap / 100), 'changed model'),
         'changed_model_relabelled')

    base_checks = [{'id': c, 'passed': True} for c in ('deleted_normalization', 'straddling_supports_counted')]
    pkt = {'checks': base_checks, 'sha256': hashlib.sha256(json.dumps(base_checks, sort_keys=True).encode()).hexdigest()}
    bad_checks = [{'id': 'deleted_normalization', 'passed': False}, {'id': 'straddling_supports_counted', 'passed': True}]
    bad = {'checks': bad_checks, 'sha256': hashlib.sha256(json.dumps(bad_checks, sort_keys=True).encode()).hexdigest()}
    gone = {'checks': base_checks[1:], 'sha256': hashlib.sha256(json.dumps(base_checks[1:], sort_keys=True).encode()).hexdigest()}
    req = [c['id'] for c in base_checks]
    need(accepts(lambda: validate_evidence(pkt, req)) and rejects(lambda: validate_evidence(bad, req), 'required control')
         and rejects(lambda: validate_evidence(gone, req), 'required control'), 'coherent_evidence_tampering')

    # Tier (i) fails at the cap; retuning tau to 1e-10 (where it would pass) under the cap label is rejected.
    need(accepts(lambda: validate_target('i', cap['i']['D_forward'], target, False))
         and rejects(lambda: validate_target('i', cap['i']['D_forward'], target, True), 'retuned')
         and small['i']['D_forward'] <= target
         and rejects(lambda: validate_model(dict(good, tau=tau_cap / 100), tau_cap, tau_cap / 100), 'changed model'),
         'insufficient_verdict_retained')

    exact_vals = [cap[t][f] for t in ('i', 'ii') for f in ('t', 'eps', 'D_forward', 'D_purification_hi')]
    need(accepts(lambda: validate_exact(exact_vals))
         and rejects(lambda: validate_exact(exact_vals + [float(cap['ii']['D_forward'])]), 'non-exact'),
         'exact_arithmetic_admission')

    loose = [amp for m, amp in cr0 if m & rmask]
    vecs = [create(fx['psi_out'], m, amp) for m, amp in cr0 if m & rmask]
    tot = {}
    for v in vecs:
        tot = vadd(tot, v)
    rss_sq = sum((inner(v, v) for v in vecs), F(0))
    need(inner(tot, tot) > rss_sq and len(loose) == 5 and accepts(lambda: validate_eps_rule('linear'))
         and rejects(lambda: validate_eps_rule('root_sum_square'), 'add linearly'), 'root_n_misuse')

    need(validate_claims(flags) and rejects(lambda: validate_claims(dict(flags, continuum_claim=True)), 'forbidden claim')
         and rejects(lambda: validate_claims(dict(flags, scientific_priority_verified=True)), 'forbidden claim'),
         'no_priority_or_continuum_claim')

    rhos = [tuple(sorted(f2['rho'].items())) for _, f2 in fams]
    numerators = [f2['rho_un'][(0, 0)] for _, f2 in fams]
    znaive = [f2['rho_un'][(0, 0)] / (1 + f2['n_delta']) for _, f2 in fams]
    need(accepts(lambda: validate_uniform(rhos)) and rejects(lambda: validate_uniform(numerators), 'volume-dependent')
         and rejects(lambda: validate_uniform(znaive), 'volume-dependent')
         and numerators[1] == numerators[0] * (1 + h * h), 'deleted_normalization', padding_growth=q(1 + h * h))

    r_only = [(m, amp) for m, amp in cr0 if m & rmask]
    fr = split_fixture(r_only, rmask, rstates)
    naive_vals = []
    for cr_p, f2 in fams:
        num_r_only = split_fixture([(m, amp) for m, amp in cr_p if m & rmask], rmask, rstates)['rho_un'][(0, 0)]
        naive_vals.append(num_r_only / f2['z'])
    need(rejects(lambda: validate_equal(fr['rho'], fx['rho'], 'reduced density'), 'mismatch')
         and rejects(lambda: validate_uniform(naive_vals), 'volume-dependent'), 'outside_creations_do_not_cancel_naively')

    need(all(rejects(lambda dd=dd: validate_equal(density_from_parts(fx, rstates, dd), fx['rho'], 'reduced density'), 'mismatch')
             for dd in ('bra_cross', 'ket_cross', 'sigma', 'normalization')), 'omitted_adjoint_terms')

    def xi_sigma(s_amp, g_amp):
        crx = [(0b001, a), (0b010, b1), (0b011, d), (0b101, e2), (0b110, s_amp), (0b100, g_amp)]
        fq = split_fixture(crx, rmask, rstates)
        return ({k: v / fq['n_out'] for k, v in fq['xi'].items()}, {k: v / fq['n_out'] for k, v in fq['sigma'].items()})
    x_s0, sg_s0 = xi_sigma(s, F(0))
    x_00, sg_00 = xi_sigma(F(0), F(0))
    x_sg, _ = xi_sigma(s, g)
    x_0g, _ = xi_sigma(F(0), g)
    need(x_s0 == x_00 and sg_s0 != sg_00 and x_sg != x_0g
         and rejects(lambda: validate_count(n_inside, n_meet, 'exact'), 'count differs'),
         'straddling_supports_counted', straddling_faces=str(n_straddle))

    padded_sum = [sum(site_sums(cp, range(3 + k)).values()) for k, (cp, _) in enumerate(fams)]
    need(meet_sum <= 2 * t_R and rejects(lambda: validate_uniform(padded_sum), 'volume-dependent')
         and meet_sum > t_R and n_meet * face_norm <= 2 * per_factor * face_norm, 'anchored_norm_restricted_to_cover')

    need(G_R == F(148, 7) and Gp_R == 352 and J0 * G_R < R and cap['ii']['remainder_bound'] > 0
         and 16 * (1 + 10 * R) < 16 * e_lo * (1 + 10 * R)
         and rejects(lambda: validate_tier_packet(dict(tier_packet(cap['ii']), remainder=F(0))), 'remainder set to zero'),
         'am2_fixed_point_constants')

    need(per_factor == 49 and len(owner_sets) == 15 and energy_norm == 24 and face_norm == F(1, 144)
         and accepts(lambda: validate_count(84, per_factor, 'labelled_bound'))
         and rejects(lambda: validate_count(84, per_factor, 'exact'), 'count differs'), 'first_order_face_enumeration')

    need(accepts(lambda: validate_passage({'uniform_gap': F(1, 2), 'topology': 'local_trace_norm'}))
         and rejects(lambda: validate_passage({'uniform_gap': F(0), 'topology': 'local_trace_norm'}), 'eigenvalue convergence'),
         'cutoff_vector_removal')

    Dq = cap['ii']['D_forward']
    lim1, lim2 = (F(1) - Dq / 4, Dq / 4), (F(1) - Dq / 4, -Dq / 4)
    dist_each = 2 * (Dq / 4)
    need(dist_each <= Dq and lim1 != lim2 and 2 * (Dq / 4) * 2 <= 2 * Dq
         and rejects(lambda: validate_claims(dict(flags, uniqueness_claim=True)), 'forbidden claim')
         and rejects(lambda: validate_claims(dict(flags, rate_in_N_claim=True)), 'forbidden claim'),
         'aq_passage_trace_norm_only')

    pk = tier_packet(cap['ii'])
    mixed = dict(pk, t=pk['t1'] + pk['kappa'] * cap['i']['t'], remainder_tier='i')
    circular = dict(pk, t=pk['t1'] * (1 + pk['kappa']))
    need(accepts(lambda: validate_tier_packet(pk)) and rejects(lambda: validate_tier_packet(mixed), 'tier mixing')
         and rejects(lambda: validate_tier_packet(circular), 'self-consistent'), 'tier_mixing_rejected')

    all2 = sorted(sites2)
    true_max = max(sum(per_site2[u].values()) for u in all2)
    inhom = list(faces2) + [f for f in anchored_faces((1, 1, 1)) if not f['selected']]
    cnt = {}
    for f in inhom:
        for uu in f['owners']:
            cnt[uu] = cnt.get(uu, 0) + 1
    inhom_max = max(cnt.values())
    r_only_count = max(cnt.get(uu, 0) for uu in COVER)
    need(accepts(lambda: validate_site_scope(all2, all2, per_factor, true_max))
         and rejects(lambda: validate_site_scope(sorted(COVER), all2, r_only_count, inhom_max), 'restricted')
         and r_only_count < inhom_max, 'face_count_all_sites', inhomogeneous_max=str(inhom_max))

    need(accepts(lambda: validate_premises(contract['shared_premises']))
         and rejects(lambda: validate_premises(contract['shared_premises'] + ['research/round32/skeptic/triage.md']), 'isolation')
         and contract.get('reverse_premise_isolation') is True
         and 'research/round32/skeptic/triage.md' in contract['forward_additional_premises'], 'reverse_premise_isolation')

    need(av2_hi(target) <= one_e6 and av2_lo(F(423, 10 ** 9)) > one_e6 and av2_hi(cap['ii']['D_forward']) <= one_e6,
         'av2_feasibility_threshold', dynamics_upper=q(dyn_hi))

    ids = [c['id'] for c in CHECKS]
    missing = [c for c in contract['controls'] if c not in ids]
    need(not missing, 'all_25_contract_controls_executed')

    # ---------------------------------------------------------------- packet
    def tier_block(v):
        keys = ('t', 'eps', 'D_forward', 'D_purification_lo', 'D_purification_hi')
        blk = {k: q(v[k]) for k in keys}
        for extra in ('t1', 'remainder_bound', 'kappa', 'omega_W_bound', 'omega_W2_bound', 'm_squared_bound'):
            if extra in v:
                blk[extra] = q(v[extra])
        for flag in ('D_meets_4e-7', 'D_meets_1e-6', 'Dpur_meets_4e-7'):
            if flag in v:
                blk[flag] = v[flag]
        blk['rule'] = v['rule']
        return blk

    tiers_out = {}
    for key, rv in res.items():
        tiers_out[key] = {'J': q(rv['J']),
                          'label': 'scaling_control_only' if key == '+1e-10' else 'cap',
                          'tier_i': tier_block(rv['i']), 'tier_i_iterated': tier_block(rv['i_iterated']),
                          'tier_ii': tier_block(rv['ii']), 'tier_ii_grouped': tier_block(rv['ii_grouped'])}
    previews = {
        'D_i_forward_cap': preview(cap['i']['D_forward']),
        'D_i_purification_cap': preview(cap['i']['D_purification_hi']),
        'D_i_iterated_forward_cap': preview(cap['i_iterated']['D_forward']),
        'D_ii_forward_cap': preview(cap['ii']['D_forward']),
        'D_ii_purification_cap': preview(cap['ii']['D_purification_hi']),
        'D_ii_grouped_forward_cap': preview(cap['ii_grouped']['D_forward']),
        't_i_iterated_cap': preview(cap['i_iterated']['t']),
        't_ii_grouped_cap': preview(cap['ii_grouped']['t']),
        'scaling_ratio_tier_i': preview(scal['i']['forward_ratio']),
        'scaling_ratio_tier_ii': preview(scal['ii']['forward_ratio']),
        'av2_radius_with_D_ii': preview(av2_hi(cap['ii']['D_forward'])),
        'av2_radius_with_D_i': preview(av2_hi(cap['i']['D_forward'])),
        'note': 'binary floating previews only; no admission Boolean reads them',
    }
    result = {
        'schema': 'hnm-r32-skeptic-precomparison-v1',
        'loop': 'AV1',
        'stage': 'pre_comparison',
        'reviewer': 'model-agent skeptic with correlated ancestry; not human peer review or formal verification',
        'human_author': 'Hruday N M (BUNZEEY)',
        'route': 'purification contractivity: rho_R and P_R are the R-marginals of psi/||psi|| and psi_out/||psi_out||; forward explicit-density formula evaluated as comparator',
        'producer_files_read': [],
        'contract_sha256': hashlib.sha256(contract_bytes).hexdigest(),
        'i1_report_sha256': sha(I1_REPORT),
        'model_id': contract['preregistration']['model_id'],
        'derived_counts': {
            'omitted_classes': str(n_omitted), 'faces_per_factor': str(per_factor),
            'owner_sets_per_factor': str(len(owner_sets)), 'owner_set_multiplicities': [str(x) for x in mults],
            'faces_meeting_R': str(n_meet), 'faces_inside_R': str(n_inside), 'faces_containing_R': str(n_contain),
            'straddling_faces_meeting_R': str(n_straddle), 'incident_anchors': str(len(incident)),
            'cover_links': str(len(links)), 'cover_endpoints': str(len(ends)),
            'labelled_bound_per_factor': '84', 'labelled_bound_R': '168',
            'brute_force': {str(k): {kk: str(vv) for kk, vv in v.items()} for k, v in brute.items()},
            'method': 'I1 printed table parsed and matched to I1.1/I1.4 geometry; counts by translation covariance; all-site brute force on Lambda_N, N=1,2,3',
        },
        'am2_constants': {'R': q(R), 'J_cap': q(J0), 'G_R_upper': q(G_R), 'G_prime_R_upper': q(Gp_R),
                          'exp_one_eighth_upper': q(e_hi), 'self_map': q(J0 * G_R), 'exclusion': q(2 * J0 * Gp_R)},
        'first_order': {'H0_eigenvalue_normalized': q(energy_norm), 'H0_eigenvalue_alpha_units': q(energy_norm / onsite_factor),
                        'face_vector_norm': '1/2', 'amplitude_over_tau': q(amp_norm), 'face_norm_over_abs_tau': q(face_norm),
                        't1_triangle_over_abs_tau': q(per_factor * face_norm),
                        'grouped_sqrt_sum_upper': q(sq_hi), 'haar_moments': [q(x) for x in mom]},
        'tiers': tiers_out,
        'scaling': {k: {kk: q(vv) for kk, vv in v.items()} for k, v in scal.items()},
        'at4_sqrt_ratio_squared': q(at4_sq_ratio),
        'targets': {'av2_threshold': q(target), 'secondary': '1/1000000',
                    'D_ii_meets_4e-7': cap['ii']['D_meets_4e-7'], 'D_ii_meets_1e-6': cap['ii']['D_meets_1e-6'],
                    'D_i_meets_4e-7': cap['i']['D_meets_4e-7'], 'D_i_meets_1e-6': cap['i']['D_meets_1e-6']},
        'av2_feasibility': {'pi_lower': q(pi_lo), 'pi_upper': q(pi_hi), 'dynamics_upper': q(dyn_hi),
                            'radius_upper_at_4e-7': q(av2_hi(target)), 'D_4.22e-7_feasible': True, 'D_4.23e-7_infeasible': True},
        'fixtures': {'A_e_squared': q(e_sq), 'A_padding_growth_per_site': q(1 + h * h),
                     'A_rho_00': q(fx['rho'][(0, 0)]), 'B_trace_norm_squared': q(tn_sq), 'B_e_squared': q(eB)},
        'previews': previews,
        'checks': CHECKS,
    }
    result.update(flags)
    return result


def ceil_frac(x, den=10 ** 40):
    """Outward (upward) rounding to a fixed denominator; keeps upper bounds valid."""
    up = F(-((-x.numerator * den) // x.denominator), den)
    if up < x:
        raise CheckFailure('ceil rounding')
    return up


def fact(k):
    out = 1
    for i in range(2, k + 1):
        out *= i
    return out


def sqrt_bracket_frac(x, scale=10 ** 15):
    num, den = x.numerator, x.denominator
    r = isqrt(num * scale * scale // den)
    lo, hi = F(r, scale), F(r + 1, scale)
    if not (lo * lo <= x <= hi * hi):
        raise CheckFailure('fraction sqrt bracket')
    return lo, hi


def tier_packet(v):
    return {'t': v['t'], 't1': v['t1'], 'kappa': v['kappa'], 'remainder': v['remainder_bound'],
            'first_order_tier': 'ii', 'remainder_tier': 'ii'}


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
    print(json.dumps({'checks': len(result['checks']), 'D_ii_forward': result['previews']['D_ii_forward_cap'],
                      'D_i_forward': result['previews']['D_i_forward_cap']}))


if __name__ == '__main__':
    main()
