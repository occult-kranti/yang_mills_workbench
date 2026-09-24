#!/usr/bin/env python3
"""AY1 forward producer: exact checks for the uniform local closeness of all AQ-type
subsequential states (two named construction families) and the family-independent
first-order reduced density on the cover R={0,e_z}.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production.

Standard library only (argparse, fractions, hashlib, json, math, pathlib, re).
Every admission Boolean is decided in exact Fraction arithmetic; decimal strings
are truncated previews.  Conditions raise AdmissionError explicitly (never
`assert`), so every check stays active under `python -O`.

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import hashlib
import json
import re
from fractions import Fraction as Q
from math import factorial, isqrt
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
CONTRACT_REL = 'research/round32/contracts/ay1.json'
CONTRACT_SHA256 = 'be9b354420e66e7edba03d59b3d194b69f26782b44cfb63cb10e176bf4879ae0'
HUMAN_AUTHOR = 'Hruday N M (BUNZEEY)'

P_AV1_GATE = 'research/round32/advisor/av1-gate.json'
P_AW1_GATE = 'research/round32/advisor/aw1-gate.json'
P_AW2_GATE = 'research/round32/advisor/aw2-gate.json'
P_AX1_GATE = 'research/round32/advisor/ax1-gate.json'
P_AX2_GATE = 'research/round32/advisor/ax2-gate.json'
P_AM2_GATE = 'research/round29/advisor/am2-gate.json'
P_AM2 = 'research/round29/forward/am2/report.md'
P_AQ1 = 'research/round29/forward/aq1/report.md'
P_AQ2 = 'research/round29/forward/aq2/report.md'
P_AT4 = 'research/round31/forward/at4/report.md'
P_I1 = 'research/round21/forward/i1/report.md'
P_AV1F = 'research/round32/forward/av1/report.md'
P_AW1F = 'research/round32/forward/aw1/report.md'
P_JUNG = 'research/round32/experts/jung/loop2-response.md'
P_SEL = 'research/round32/advisor/selection-ay1.md'


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


def sha_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha(path):
    return sha_bytes(path.read_bytes())


def sqrt_up(n, scale=10 ** 15):
    """Directed rational upper bound of sqrt(n) for a nonnegative rational n."""
    n = Q(n)
    k = isqrt(n.numerator * scale * scale // n.denominator)
    while Q(k, scale) ** 2 < n:
        k += 1
    up = Q(k, scale)
    require(up * up >= n and (up - Q(1, scale)) ** 2 < n, 'sqrt upper bracket')
    return up


def sqrt_down(n, scale=10 ** 15):
    n = Q(n)
    k = isqrt(n.numerator * scale * scale // n.denominator)
    while Q(k + 1, scale) ** 2 <= n:
        k += 1
    while Q(k, scale) ** 2 > n:
        k -= 1
    return Q(k, scale)


def read_input(rel):
    return (BASE / 'inputs' / rel).read_text(encoding='utf-8')


def load_json_input(rel):
    return json.loads(read_input(rel))


def match(pattern, text, label, flags=0):
    m = re.search(pattern, text, flags)
    require(m is not None, 'premise text not parsed: ' + label)
    return m


# ---------------------------------------------------------------------------
# Contract: every target, template, control id and reference is read from the sha256-bound snapshot.
# ---------------------------------------------------------------------------
def load_contract():
    raw = (BASE / 'inputs' / CONTRACT_REL).read_bytes()
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen AY1 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'AY1' and c.get('status') == 'frozen_before_production', 'wrong contract identity')
    return c, digest


def contract_values(c):
    p = c['parameters']
    pre = c['preregistration']
    v = {}
    v['tau_cap'] = rat(p['tau_cap'])
    v['families'] = list(p['families'])
    require(len(v['families']) == 2, 'exactly two named families')
    m = match(r'^(trace norm on fixed finite regions); (norm on compact time windows) for dynamics$', p['topology'], 'topology')
    v['topology_states_param'], v['topology_dynamics'] = m.group(1), m.group(2)
    m = match(r'Name two topologies separately: (trace norm on B\(H_R\)) for states, and (norm on compact time windows) for dynamics',
              c['required'][0], 'item 1 topologies')
    v['topology_states'] = m.group(1)
    require(m.group(2) == v['topology_dynamics'], 'dynamics topology differs between parameters and item 1')
    require('2 D (AV1 admitted tier)' in p['constant'], 'constant names the AV1 admitted tier')
    v['model'] = c['model']
    require('|tau|<=10^-8' in v['model'] and 'common clock' in v['model'] and 'B(H_R)' in v['model'], 'model string')
    tg = pre['target']
    v['target'] = rat(tg['value'])
    require(tg['comparator'] == '<=' and '2D' in tg['quantity'], 'target comparator/quantity')
    v['target_quantity'] = tg['quantity']
    v['tau_value'] = rat(pre['tau']['value'])
    require(v['tau_value'] == v['tau_cap'], 'preregistered tau equals the cap')
    v['signs'] = list(pre['tau']['signs_evaluated'])
    require(v['signs'] == ['+', '-'], 'both signs required')
    require(pre['tau']['is_model_change_vs_previous_loop'] is False and pre['tau']['rule_if_chosen_later'] is None, 'tau rule')
    v['triple'] = [rat(x) for x in pre['selected_triple_alpha_units']]
    require(v['triple'] == [0, 0, 0], 'zero selected triple')
    v['model_id'] = pre['model_id']
    v['state_provenance'] = pre['state_provenance']
    obs = pre['observable']
    v['observable_id'] = obs['id']
    v['centering'] = obs['centering']
    v['reference_value'] = obs['reference_value_exact']
    v['reference_route'] = obs['reference_route']
    require(v['centering'] == 'none' and v['reference_value'] == 'P_R' and v['reference_route'] == 'haar', 'observable block')
    v['clock'] = pre['clock']
    m = match(r'^s=alpha\*t_E/hbar, theta=alpha\*t/hbar; u=s/(\d+) and exponent (\d+) forbidden in packets$', v['clock'], 'clock')
    v['forbidden_u_div'], v['forbidden_exponent'] = int(m.group(1)), int(m.group(2))
    v['error_terms'] = list(pre['error_terms_itemized'])
    v['error_terms_rule'] = pre['error_terms_rule']
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    v['outcomes'] = list(pre['expected_outcome_types'])
    v['template'] = pre['mandatory_sentence_template']
    v['gate_fields'] = dict(pre['gate_fields_required'])
    v['controls'] = list(c['controls'])
    require(v['controls'] == list(pre['controls_required']['ids']), 'controls list equals the preregistered ids')
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    v['acceptance'] = dict(c['acceptance'])
    v['shared'] = list(c['shared_premises'])
    v['forward_additional'] = list(c['forward_additional_premises'])
    v['reverse_isolation'] = c['reverse_premise_isolation']
    v['required'] = list(c['required'])
    v['hash_binding'] = dict(pre['hash_binding'])
    return v


# ---------------------------------------------------------------------------
# Fine-lattice geometry and the I1 anchored face table (parsed from the I1 snapshot).
# ---------------------------------------------------------------------------
E_UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIENT = {'xy': (0, 1), 'xz': (0, 2), 'yz': (1, 2)}
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN = (0, 0, 0)
EZ = (0, 0, 1)
COVER_R = (ORIGIN, EZ)
TOKEN = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}


def add(p, q):
    return tuple(a + b for a, b in zip(p, q))


def sub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(p, a, c):
    return ((p, a), (add(p, E_UNIT[a]), c), (add(p, E_UNIT[c]), a), (p, c))


def face_support(p, a, c):
    return frozenset(owner(link[0]) for link in face_links(p, a, c))


def is_selected(p, a, c):
    return (a, c) == (0, 1) and p[1] % 2 == 0 and p[0] % 4 in (0, 1, 2)


def parse_i1_table(text):
    rows = re.findall(r'^\| (xy|xz|yz): r=([\d,]+); s=([\d,]+) \| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|$', text, re.M)
    require(len(rows) == 8, 'I1 table has eight rows')
    classes = []
    for orient, rs, ss, count, supp, role in rows:
        rl = [int(x) for x in rs.split(',')]
        sl = [int(x) for x in ss.split(',')]
        require(len(rl) * len(sl) == int(count), 'I1 row count column')
        support = frozenset(TOKEN[t.strip()] for t in supp.split(','))
        for r in rl:
            for q in sl:
                classes.append((orient, r, q, support, role))
    return classes


def class_label(cls):
    return '%s r=%d s=%d' % (cls[0], cls[1], cls[2])


def class_base(anchor, cls):
    return (4 * anchor[0] + cls[1], 2 * anchor[1] + cls[2], anchor[2]), ORIENT[cls[0]]


def face_key(face):
    return (face[0], face[1][:3])


def owner_set(face):
    b, cls = face
    return frozenset(add(b, d) for d in cls[3])


def face_link_set(face):
    base, (a, c) = class_base(*face)
    return frozenset(face_links(base, a, c))


def faces_containing(u, classes):
    """Translation covariance: face (b,k) has u in its owner set iff b=u-d with d in K_k."""
    return [(sub(u, d), cls) for cls in classes for d in sorted(cls[3])]


def coarse_box(N):
    rng = range(-N, N + 1)
    return frozenset((x, y, z) for x in rng for y in rng for z in rng)


def family_faces(N, omitted, family):
    """F1: whole stars b+S inside Lambda_N (AQ1).  F2: every omitted face whose owner set lies in Lambda_N (I1 section 6)."""
    box = coarse_box(N)
    out = []
    for b in sorted(box):
        star_in = all(add(b, d) in box for d in S_STAR)
        for cls in omitted:
            f = (b, cls)
            if family == 'F1' and star_in:
                out.append(f)
            elif family == 'F2' and owner_set(f) <= box:
                out.append(f)
    return box, out


def brute_force_faces(xr, yr, zr):
    """Independent fine-lattice enumeration of every elementary plaquette (no class table)."""
    out = []
    for x in xr:
        for y in yr:
            for z in zr:
                p = (x, y, z)
                for a, c in ((0, 1), (0, 2), (1, 2)):
                    out.append((p, a, c, face_support(p, a, c), owner(p), is_selected(p, a, c)))
    return out


# ---------------------------------------------------------------------------
# Exact SU(2) Haar moments of W=(1/2)Tr U: two routes (Clebsch-Gordan count; Weyl/Wallis).
# ---------------------------------------------------------------------------
def spin_half_invariants(n):
    dist = {0: 1}
    for _ in range(n):
        new = {}
        for j2, m in dist.items():
            for j2n in (j2 - 1, j2 + 1):
                if j2n >= 0:
                    new[j2n] = new.get(j2n, 0) + m
        dist = new
    return dist.get(0, 0)


def haar_W_moment(n):
    return Q(spin_half_invariants(n), 2 ** n)


def weyl_W_moment(n):
    if n % 2:
        return Q(0)

    def wallis(m2):
        num, den = 1, 1
        for k in range(1, m2 + 1):
            if k % 2:
                num *= k
            else:
                den *= k
        return Q(num, den)
    return 2 * (wallis(n) - wallis(n + 2))


def link_parity_vanishes(face_link_sets):
    """Centre grading: a Haar product of spin-1/2 face traces vanishes if some link occurs an odd number of times."""
    count = {}
    for fl in face_link_sets:
        for link in fl:
            count[link] = count.get(link, 0) + 1
    return any(v % 2 for v in count.values())


# ---------------------------------------------------------------------------
# AV1 tier (ii) inputs, the forward density route and the R-local second-order itemization.
# Every component carries its tier label; mixing labels is rejected.
# ---------------------------------------------------------------------------
def tier_ii_inputs(tau, J_per_tau, t1_per_tau, GpR):
    J = J_per_tau * abs(tau)
    t1 = t1_per_tau * abs(tau)
    require(GpR * J < 1, 'self-consistent remainder needs 352J<1')
    T = t1 / (1 - GpR * J)
    rho = GpR * J * T
    require(rho > 0 and T == t1 + rho, 'self-consistent identity T=t1+rho with a positive remainder')
    return {'tier': 'ii', 'tau': tau, 'J': J, 't1': t1, 'T': T, 'rho': rho}


def density_route_D(inp):
    require(inp['tier'] == 'ii', 'density route uses the tier (ii) inputs')
    eps = 2 * inp['T'] + inp['T'] ** 2
    return eps, 2 * eps * (1 + eps) / (1 + eps * eps)


def assemble(tier, components):
    total = Q(0)
    for name, label, value in components:
        require(label == tier, 'tier mixing rejected: ' + name + ' is tier ' + label + ' inside tier ' + tier)
        require(isinstance(value, Q) and value >= 0, 'non-exact or negative component ' + name)
        total += value
    names = [n for n, _, _ in components]
    require(len(names) == len(set(names)), 'duplicate component')
    return total


def k2prime_items(inp, pins, am2_form='triangle', tier_labels=None):
    """R-local trace-norm remainder ||rho_R-P_R-rho1_R||_1 <= sum of items (uniform in N, cutoff, limits)."""
    tau = inp['tau']
    a = abs(tau) / 144
    T, rho = inp['T'], inp['rho']
    epsR = pins['meet'] * a + 2 * rho + (pins['single'] * a + rho) ** 2
    if am2_form == 'triangle':
        am2 = 4 * rho
    elif am2_form == 'orthogonal':
        am2 = 2 * sqrt_up(2) * rho
    else:
        raise AdmissionError('unknown am2 form')
    items = [
        ('am2_remainder', am2),
        ('straddling', 2 * T * (pins['straddling'] * a + 2 * rho)),
        ('two_creation', 2 * (pins['single'] * a + rho) ** 2),
        ('density', 2 * epsR ** 2),
        ('normalization_third_order', 2 * epsR ** 2 * pins['inside'] * a),
    ]
    labels = tier_labels or {}
    comps = [(n, labels.get(n, inp['tier']), v) for n, v in items]
    total = assemble(inp['tier'], comps)
    return {'items': dict(items), 'total': total, 'epsR': epsR, 'a': a}


# ---------------------------------------------------------------------------
# Exact finite creation-algebra fixture (audit of the R-marginal decomposition; transfers_to_aq false).
# Sites 0=r0, 1=r1 (the two-site R), 2=o1, 3=o2 (outside), 4.. decoupled spectators.
# ---------------------------------------------------------------------------
FIX_C1R = {(1, 1): Q(3, 50), (2, 1): Q(4, 50)}      # designated first-order part of c_R, norm 1/10


def fixture_creations(spectators):
    cre = {
        (0, 1): {(1, 1): Q(3, 50), (2, 1): Q(4, 50), (1, 2): Q(1, 200)},
        (0,): {(1,): Q(1, 300)},
        (1,): {(2,): Q(-1, 400)},
        (0, 2): {(1, 1): Q(1, 9)},
        (1, 3): {(2, 1): Q(1, 11)},
        (0, 1, 2): {(1, 1, 1): Q(1, 13)},
        (2,): {(1,): Q(-1, 12)},
        (3,): {(1,): Q(1, 7)},
        (2, 3): {(1, 1): Q(1, 15)},
    }
    for k in range(spectators):
        cre[(4 + k,)] = {(1,): Q(1, 5 + k)}
    return [3, 3, 2, 2] + [2] * spectators, cre


def fx_apply(cI, I, v):
    out = {}
    for key, amp in v.items():
        if all(key[x] == 0 for x in I):
            for ck, ca in cI.items():
                nk = list(key)
                for x, val in zip(I, ck):
                    nk[x] = val
                nk = tuple(nk)
                out[nk] = out.get(nk, 0) + ca * amp
    return {k: a for k, a in out.items() if a != 0}


def fx_add(u, v, c=1):
    out = dict(u)
    for k, a in v.items():
        out[k] = out.get(k, 0) + c * a
    return {k: a for k, a in out.items() if a != 0}


def fx_product(dims, cre, supports):
    v = {tuple([0] * len(dims)): Q(1)}
    for I in supports:
        v = fx_add(v, fx_apply(cre[I], I, v), -1)
    return v


def fx_norm2(v):
    return sum((a * a for a in v.values()), Q(0))


def fx_reduced(u, v):
    by = {}
    for k, a in v.items():
        by.setdefault(k[2:], []).append((k[:2], a))
    out = {}
    for k, a in u.items():
        for rk2, b in by.get(k[2:], []):
            key = (k[:2], rk2)
            out[key] = out.get(key, 0) + a * b
    return {k: x for k, x in out.items() if x != 0}


def fx_contract_out(vec, phi):
    """(1_R x <phi|) vec as a vector on H_R."""
    out = {}
    for k, a in vec.items():
        b = phi.get(k[2:])
        if b:
            out[k[:2]] = out.get(k[:2], 0) + a * b
    return {k: x for k, x in out.items() if x != 0}


def op_rank2(u, w):
    """|u><w| + |w><u| on H_R as a dict over (ket, bra)."""
    out = {}
    for k1, a in u.items():
        for k2, b in w.items():
            out[(k1, k2)] = out.get((k1, k2), 0) + a * b
            out[(k2, k1)] = out.get((k2, k1), 0) + a * b
    return {k: x for k, x in out.items() if x != 0}


def op_add(A, B, c=1):
    out = dict(A)
    for k, x in B.items():
        out[k] = out.get(k, 0) + c * x
    return {k: x for k, x in out.items() if x != 0}


def op_scale(A, c):
    return {k: c * x for k, x in A.items() if c * x != 0}


def op_mul(A, B):
    by = {}
    for (k1, k2), x in B.items():
        by.setdefault(k1, []).append((k2, x))
    out = {}
    for (i, j), x in A.items():
        for (l, y) in by.get(j, []):
            out[(i, l)] = out.get((i, l), 0) + x * y
    return {k: x for k, x in out.items() if x != 0}


def fixture_run(spectators, drop=None):
    dims, cre = fixture_creations(spectators)
    Rset = {0, 1}
    A = sorted(I for I in cre if set(I) & Rset)
    B = sorted(I for I in cre if not set(I) & Rset)
    psi = fx_product(dims, cre, A + B)
    psi_out = fx_product(dims, cre, B)
    delta = fx_add(psi, psi_out, -1)
    n2, d2, Z = fx_norm2(psi_out), fx_norm2(delta), fx_norm2(psi)
    om = (0, 0)
    phi = {k[2:]: a for k, a in psi_out.items() if k[:2] == om}
    require(all(k[:2] == om for k in psi_out), 'psi_out = Omega_R x phi_out')
    xi = fx_contract_out(delta, phi)
    sigma = fx_reduced(delta, delta)
    if drop == 'sigma':
        sigma = {}
    if drop == 'straddling_in_xi':
        inside = fx_add(fx_add(fx_apply(cre[(0, 1)], (0, 1), psi_out), fx_apply(cre[(0,)], (0,), psi_out)),
                        fx_apply(cre[(1,)], (1,), psi_out))
        xi = {k: -x for k, x in fx_contract_out(inside, phi).items()}
    rho_raw = fx_reduced(psi, psi)
    rhoR = {k: x / Z for k, x in rho_raw.items()} if drop != 'numerator_only' else rho_raw
    rec = {(om, om): n2}
    rec = op_add(rec, op_rank2({om: Q(1)}, xi))
    rec = op_add(rec, sigma)
    rec = op_scale(rec, 1 / (n2 + d2))
    return {'dims': dims, 'cre': cre, 'A': A, 'B': B, 'psi_out': psi_out, 'delta': delta, 'n2': n2, 'd2': d2, 'Z': Z,
            'phi': phi, 'xi': xi, 'sigma': sigma, 'rhoR': rhoR, 'rec': rec, 'identity': rec == rhoR}


# ---------------------------------------------------------------------------
# Main computation.
# ---------------------------------------------------------------------------
def compute(check_sha):
    c, contract_digest = load_contract()
    V = contract_values(c)
    tau_cap = V['tau_cap']
    taus = {'+': tau_cap, '-': -tau_cap}
    check('contract_snapshot_sha256',
          contract_digest == CONTRACT_SHA256 and V['target'] == Q(1, 1250000) and len(V['controls']) == 21,
          contract_sha256=contract_digest, contract_path=CONTRACT_REL, target_read_from_contract=s(V['target']),
          target_quantity=V['target_quantity'], tau_cap_read_from_contract=s(tau_cap),
          reference_read_from_contract=V['reference_value'] + ' via ' + V['reference_route'],
          families_read_from_contract=V['families'], controls_read_from_contract=len(V['controls']),
          hash_binding=V['hash_binding'])

    # ======================= premise bindings (gates and reports) =======================
    gates = {}
    for key, rel in (('AV1', P_AV1_GATE), ('AW1', P_AW1_GATE), ('AW2', P_AW2_GATE), ('AX1', P_AX1_GATE),
                     ('AX2', P_AX2_GATE), ('AM2', P_AM2_GATE)):
        gates[key] = load_json_input(rel)
        require(gates[key].get('verdict') == 'accepted_within_scope', key + ' gate verdict')
    av1 = gates['AV1']
    m = match(r'Bind the forward tier-\((ii)\) value D_ii=(\d+)/(\d+) \(certified by both inequalities\)', av1['decision'], 'AV1 D_ii')
    tier_name = m.group(1)
    D_gate = Q(int(m.group(2)), int(m.group(3)))
    m = match(r'D_i=(\d+)/(\d+) \(~2\.3680e-5; exact, forward\)', av1['accepted'], 'AV1 D_i')
    D_i_gate = Q(int(m.group(1)), int(m.group(2)))
    m = match(r'82-face refinement D_ii<=(\d+)/10\^(\d+)', av1['accepted'], 'AV1 reverse refinement')
    D_rev_gate = Q(int(m.group(1)), 10 ** int(m.group(2)))
    require('explicit-density bound 2eps(1+eps)/(1+eps^2) (forward)' in av1['accepted'], 'AV1 forward route named')
    aw1 = gates['AW1']
    m = match(r'Bind K_2\^\+ = (\d+)/(\d+) ', aw1['decision'], 'AW1 K_2^+')
    K2plus = Q(int(m.group(1)), int(m.group(2)))
    m = match(r'omega_tau\(W\)=\+tau/(\d+)\+r\(tau\)', aw1['accepted'], 'AW1 first-order coefficient')
    first_den = int(m.group(1))
    aw2 = gates['AW2']
    m = match(r'\[(\d+)/D, (\d+)/D\], D=(\d+),', aw2['accepted'], 'AW2 enclosure')
    aw2_lo, aw2_hi = Q(int(m.group(1)), int(m.group(3))), Q(int(m.group(2)), int(m.group(3)))
    m = match(r"J'=(\d+)\|tau\|", gates['AX1']['accepted'], 'AX1 route-B J')
    J_routeB = int(m.group(1))
    m = match(r'AL1 dictionary tau=(\d+)/g\^4', gates['AX1']['accepted'], 'AX1 dictionary')
    dict_num = int(m.group(1))
    am2 = read_input(P_AM2)
    m = match(r'J_0=\{(\d+)\\over(\d+)\}', am2, 'AM2 J_0')
    J0 = Q(int(m.group(1)), int(m.group(2)))
    J_per_tau = int(match(r'\\le(\d+)\|\\tau\|\\le J_0', am2, 'AM2 J per tau').group(1))
    p_support = int(match(r'\|X\|<=p=(\d+)', am2, 'AM2 support').group(1))
    order_term = int(match(r'zero for k>2p=(\d+)', am2, 'AM2 termination').group(1))
    R_ball = Q(1, int(match(r'For R=1/(\d+)', am2, 'AM2 R').group(1)))
    m = match(r"G\(R\)<(\d+)/(\d+),\\quad G'\(R\)<(\d+)", am2, 'AM2 G bounds')
    GR_rep, GpR_rep = Q(int(m.group(1)), int(m.group(2))), Q(int(m.group(3)))
    aq1 = read_input(P_AQ1)
    CF_per_site = int(match(r'8M\|F\|=(\d+)\|\\tau\|\|F\|=:C_F', aq1, 'AQ1 C_F').group(1))
    reset_R_rep = int(match(r'\\omega_N\(h_R\)\\le(\d+)\|\\tau\|', read_input(P_AQ2), 'AQ2 reset').group(1))
    at4 = read_input(P_AT4)
    m = match(r'\\le\\frac\{(\d+)\|\\tau\|\}\{(\d+)\}=\\frac\{(\d+)\|\\tau\|\}\{(\d+)\}', at4, 'AT4 eps_R')
    at4_eps_per_tau = Q(int(m.group(3)), int(m.group(4)))
    require(Q(int(m.group(1)), int(m.group(2))) == at4_eps_per_tau, 'AT4 eps_R arithmetic')
    av1f = read_input(P_AV1F)
    require('{HNM-AV1-F12}' in av1f and '{HNM-AV1-F22}' in av1f and '{HNM-AV1-F24}' in av1f, 'AV1 density, cutoff and passage tags')
    aw1f = read_input(P_AW1F)
    require('{HNM-AW1-F14}' in aw1f and '{HNM-AW1-F15}' in aw1f, 'AW1 amplitude lemma and remainder tags')
    gate_sha = {k: sha(BASE / 'inputs' / rel) for k, rel in (('AV1', P_AV1_GATE), ('AW1', P_AW1_GATE), ('AW2', P_AW2_GATE),
                                                              ('AX1', P_AX1_GATE), ('AX2', P_AX2_GATE), ('AM2', P_AM2_GATE))}
    check('premise_gates_and_reports_bound',
          tier_name == 'ii' and first_den == 144 and J0 == Q(7, 25000000) and J_per_tau == 28 and p_support == 4
          and order_term == 2 * p_support and R_ball == Q(1, 64) and GR_rep == Q(148, 7) and GpR_rep == 352
          and CF_per_site == 56 and reset_R_rep == 98 and at4_eps_per_tau == Q(49, 3) and J_routeB == 29 and dict_num == 96,
          gate_sha256=gate_sha, av1_tier_name=tier_name, av1_D_ii_forward=s(D_gate), av1_D_i=s(D_i_gate),
          av1_D_ii_reverse_refinement=s(D_rev_gate), aw1_K2_plus=s(K2plus), aw1_first_order='+tau/%d' % first_den,
          am2_J0=s(J0), am2_J_per_abs_tau=J_per_tau, am2_support_p=p_support, am2_termination_order=order_term,
          am2_R=s(R_ball), aq1_C_F_per_site=CF_per_site, aq2_reset_R=reset_R_rep,
          read_from='gate decision/accepted strings and report equations of the hash-bound snapshots; no admitted constant is typed in')

    # ======================= I1 table, geometry and R-local enumeration =======================
    classes = parse_i1_table(read_input(P_I1))
    omitted = [k for k in classes if k[4] == 'omitted']
    selected = [k for k in classes if k[4] == 'selected']
    geo_ok = True
    for cls in classes:
        base, (a1, c1) = class_base(ORIGIN, cls)
        geo_ok = geo_ok and face_support(base, a1, c1) == cls[3] and is_selected(base, a1, c1) == (cls[4] == 'selected')
    listed = {(k[0], k[1], k[2]) for k in classes}
    all_phases = {(o, r, q) for o in ORIENT for r in range(4) for q in range(2)}
    check('i1_table_parsed_and_geometry',
          geo_ok and listed == all_phases and len(classes) == 24 and len(omitted) == 21 and len(selected) == 3
          and all(len(k[3]) >= 2 for k in omitted) and frozenset().union(*[k[3] for k in omitted]) == frozenset(S_STAR),
          anchored_classes=len(classes), omitted_classes=len(omitted), selected_classes=len(selected),
          min_omitted_owner_set_size=min(len(k[3]) for k in omitted),
          note='every omitted face has at least two owners, so no first-order creation is single-site: c^(1)_{0}=c^(1)_{e_z}=0')

    Rset = frozenset(COVER_R)
    at0 = faces_containing(ORIGIN, omitted)
    sets0 = {}
    for f in at0:
        sets0[owner_set(f)] = sets0.get(owner_set(f), 0) + 1
    meet = {}
    for u in COVER_R:
        for f in faces_containing(u, omitted):
            meet[face_key(f)] = f
    meet_faces = [meet[k] for k in sorted(meet)]
    inside = [f for f in meet_faces if owner_set(f) <= Rset]
    containing = [f for f in meet_faces if Rset <= owner_set(f)]
    strictly = [f for f in containing if owner_set(f) != Rset]
    straddling = [f for f in meet_faces if not owner_set(f) <= Rset]
    one_site = [f for f in straddling if len(owner_set(f) & Rset) == 1]
    single_0 = [f for f in meet_faces if ORIGIN in owner_set(f) and EZ not in owner_set(f)]
    single_z = [f for f in meet_faces if EZ in owner_set(f) and ORIGIN not in owner_set(f)]
    owner_sets_R = {owner_set(f) for f in meet_faces}
    brute = brute_force_faces(range(-8, 12), range(-4, 6), range(-2, 4))
    brute_meet = [x for x in brute if not x[5] and (x[3] & Rset)]
    brute_inside = [x for x in brute_meet if x[3] <= Rset]
    pins = {'per_factor': len(at0), 'meet': len(meet_faces), 'inside': len(inside), 'containing': len(containing),
            'strictly_containing': len(strictly), 'straddling': len(straddling), 'one_site_straddling': len(one_site),
            'single': len(single_0), 'owner_sets_meeting_R': len(owner_sets_R)}
    check('face_enumeration_R_local',
          pins['per_factor'] == 49 and len(sets0) == 15 and sorted(sets0.values()) == [1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 10, 10]
          and pins['meet'] == 82 == len(brute_meet) and pins['inside'] == 10 == len(brute_inside) and pins['containing'] == 16
          and pins['strictly_containing'] == 6 and pins['straddling'] == 72 == pins['meet'] - pins['inside']
          and pins['one_site_straddling'] == 66 and pins['single'] == 33 == len(single_z) == pins['per_factor'] - pins['containing']
          and pins['owner_sets_meeting_R'] == 27,
          pins=pins, owner_set_multiplicities_at_0=sorted(sets0.values()),
          derived_from='I1 table parsed from its snapshot, translation covariance; fine-lattice brute force (no table) for 82 and 10')

    # the ten faces whose owner set is exactly R, and their Gram / parity data
    F_R = sorted(inside, key=face_key)
    F_R_links = [face_link_set(f) for f in F_R]
    wilson_face = (ORIGIN, [k for k in omitted if (k[0], k[1], k[2]) == ('xz', 0, 0)][0])
    W_links = face_link_set(wilson_face)
    pair_shared = [len(face_link_set(f) & face_link_set(g)) for i, f in enumerate(meet_faces) for g in meet_faces[i + 1:]]
    links_outside = {face_key(f): sum(1 for l in face_link_set(f) if owner(l[0]) not in Rset) for f in meet_faces}
    F_R_labels = ['anchor %s %s' % (f[0], class_label(f[1])) for f in F_R]

    # ======================= full cover and incident anchors =======================
    def factor_links(b):
        return {((4 * b[0] + r, 2 * b[1] + q, b[2]), d) for r in range(4) for q in range(2) for d in range(3)}

    def endpoints(links):
        return {l[0] for l in links} | {add(l[0], E_UNIT[l[1]]) for l in links}
    cover_links = factor_links(ORIGIN) | factor_links(EZ)
    e0, ez = endpoints(factor_links(ORIGIN)), endpoints(factor_links(EZ))
    W_owners = [owner(l[0]) for l in face_links((0, 0, 0), 0, 2)]

    def validate_cover(links, n_end):
        require(len(links) == 48 and n_end == 36, 'complete cover needs 48 links and 36 endpoints')
        return True
    check('full_original_wilson_cover',
          validate_cover(cover_links, len(e0 | ez)) and len(e0) == 22 and len(ez) == 22 and len(e0 & ez) == 8
          and W_owners == [ORIGIN, ORIGIN, EZ, ORIGIN] and W_links <= cover_links
          and rejected(lambda: validate_cover(set(face_links((0, 0, 0), 0, 2)), 6), 'four_drawn_links_as_cover')
          and rejected(lambda: validate_cover(factor_links(ORIGIN), len(e0)), 'single_factor_cover'),
          links=len(cover_links), endpoints=len(e0 | ez), endpoints_per_factor=[len(e0), len(ez)], shared_endpoints=len(e0 & ez),
          wilson_link_owners=[list(o) for o in W_owners])

    anchors_R = sorted({sub(u, d) for u in COVER_R for d in S_STAR})
    fam = {}
    for N in (2, 3):
        for F in ('F1', 'F2'):
            box, faces = family_faces(N, omitted, F)
            groups = {}
            for f in faces:
                groups.setdefault(f[0], []).append(f)
            fam[(F, N)] = {'box': box, 'faces': faces, 'groups': groups}

    def groups_meeting_R(F, N):
        g = fam[(F, N)]['groups']
        return sorted(b for b, fl in g.items() if any(owner_set(f) & Rset for f in fl))

    def validate_incidence(anchor_list):
        require(len(anchor_list) == 7, 'seven incident anchors R-S are required (incoming stars included)')
        return True
    check('missing_incoming_stars',
          len(anchors_R) == 7 and all(validate_incidence(groups_meeting_R(F, N)) for F in ('F1', 'F2') for N in (2, 3))
          and all(groups_meeting_R(F, N) == anchors_R for F in ('F1', 'F2') for N in (2, 3))
          and rejected(lambda: validate_incidence([ORIGIN, EZ]), 'positive_orthant_two_anchors')
          and rejected(lambda: validate_incidence([ORIGIN]), 'one_star_only'),
          incident_anchors=[list(b) for b in anchors_R], both_families_N=[2, 3])

    # ======================= item 1(a): F1 admitted chain =======================
    F1_ok = True
    for N in (2, 3):
        d = fam[('F1', N)]
        stars_R = [b for b in anchors_R if all(add(b, dd) in d['box'] for dd in S_STAR)]
        F1_ok = F1_ok and len(stars_R) == 7 and all(len(fl) == 21 for fl in d['groups'].values())
    chain = [
        {'step': 1, 'what': 'I1 dictionary: ownership, face supports (I1.4), whole stars phi_b=-(tau/3) sum W_f, ||phi_b||<=7|tau| (I1.5)', 'source': P_I1},
        {'step': 2, 'what': 'zero triple: h_b=8 sum C_e>=6Q_b>=Q_b, Haar P_b; Lambda_N is a relabelled translate of an I1 complete-factor volume', 'source': P_AV1F + ' section 1'},
        {'step': 3, 'what': 'AM2: J<=28|tau|<=J_0=7/25000000, |X|<=4, termination order 8, J_0G(R)<R, 2J_0G\'(R)<1; nondegenerate ground, gap>=1/2 per cutoff and untruncated', 'source': P_AM2_GATE},
        {'step': 4, 'what': 'AV1 tier (ii): product split, density inequality 2eps(1+eps)/(1+eps^2), cutoff-vector removal (Eckart), passage by local trace-norm convergence', 'source': P_AV1_GATE},
        {'step': 5, 'what': 'AQ1 section 2: reset C_F=56|tau||F| and trace-norm compactness, diagonal extraction; AQ2 section 4: omega_N(h_R)<=98|tau|', 'source': P_AQ1 + '; ' + P_AQ2},
        {'step': 6, 'what': 'AQ1 section 3: norm dynamics on compact time windows (Nachtergaele-Sims), named only', 'source': P_AQ1},
        {'step': 7, 'what': 'AW1: c^(1)=L_0=-(tau/72) sum W_f Omega_0, amplitude lemma (F14), itemized remainder, first-order mean +tau/144', 'source': P_AW1_GATE},
    ]
    check('family_F1_admitted_chain', F1_ok and len(chain) == 7,
          chain=chain, family=V['families'][0], retained_incident_stars_N2_N3=7,
          note='every step is an admitted gate or the named section of an admitted report; nothing is re-proved for F1')

    # ======================= item 1(b): F2 padded interaction, contraction, reset, compactness =======================
    F2_audit = {}
    F2_ok = True
    for N in (2, 3):
        d1, d2 = fam[('F1', N)], fam[('F2', N)]
        keys1 = {face_key(f) for f in d1['faces']}
        keys2 = [face_key(f) for f in d2['faces']]
        box = d2['box']
        X = {b: frozenset().union(*[owner_set(f) for f in fl]) for b, fl in d2['groups'].items()}
        J_site = {}
        Jface_site = {}
        first_site = {}
        for b, fl in d2['groups'].items():
            for u in X[b]:
                J_site[u] = J_site.get(u, Q(0)) + Q(len(fl), 3)
            for f in fl:
                for u in owner_set(f):
                    Jface_site[u] = Jface_site.get(u, Q(0)) + Q(1, 3)
                    first_site[u] = first_site.get(u, 0) + 1
        pad = frozenset(add(b, dd) for b in box for dd in S_STAR) - box
        meetR2 = [f for f in d2['faces'] if owner_set(f) & Rset]
        insideR2 = [f for f in d2['faces'] if owner_set(f) == Rset]
        meetR1 = [f for f in d1['faces'] if owner_set(f) & Rset]
        insideR1 = [f for f in d1['faces'] if owner_set(f) == Rset]
        ok = (len(keys2) == len(set(keys2)) and keys1 < set(keys2)
              and all(X[b] <= frozenset(add(b, dd) for dd in S_STAR) & box and len(X[b]) <= p_support for b in X)
              and all(len(fl) <= 21 for fl in d2['groups'].values())
              and max(J_site.values()) == J_per_tau and max(Jface_site.values()) == Q(49, 3)
              and max(first_site.values()) == pins['per_factor']
              and not any(owner_set(f) & pad for f in d2['faces'])
              and len(meetR2) == len(meetR1) == pins['meet'] and len(insideR2) == len(insideR1) == pins['inside']
              and sorted(face_key(f) for f in insideR2) == sorted(face_key(f) for f in insideR1) == sorted(face_key(f) for f in F_R))
        F2_ok = F2_ok and ok
        F2_audit[str(N)] = {'faces_F1': len(keys1), 'faces_F2': len(keys2), 'extra_F2_faces': len(keys2) - len(keys1),
                            'groups_F2': len(X), 'max_group_support': max(len(x) for x in X.values()),
                            'max_J_per_abs_tau_anchor_grouping': s(max(J_site.values())),
                            'max_J_per_abs_tau_face_grouping_remark': s(max(Jface_site.values())),
                            'max_first_order_faces_per_site': max(first_site.values()),
                            'padding_sites_B_plus_minus_B': len(pad), 'faces_meeting_R': len(meetR2), 'faces_owner_set_R': len(insideR2)}
    check('family_F2_padded_interaction', F2_ok,
          family=V['families'][1], audit=F2_audit,
          rule='retain an omitted face iff its owner set M_f lies in Lambda_N; group it at its anchor b; X_b=union M_f is inside (b+S) cap Lambda_N',
          padding='I1 section 6: on B_plus=union(b+S) the padded sites carry only h_x with vacuum Omega_x; the padded ground is psi^(2) x Omega_pad and its R-density is unchanged',
          general_bound='u in X_b forces b in u-S (4 anchors), each group has at most 21 faces of norm |tau|/3, so J^(2)<=28|tau| in every box')

    # padding_family_contraction_proved: AM2's hypotheses H1-H5 verified; constants depend only on (p, J_0)
    x8 = Q(8) * R_ball
    exp_upper = sum((x8 ** k / factorial(k) for k in range(13)), Q(0)) + x8 ** 13 / factorial(13) / (1 - x8 / 14)
    require(exp_upper < Q(8, 7), 'exp(1/8)<8/7')
    GR = 16 * Q(8, 7) * (1 + 10 * R_ball)
    GpR = 16 * Q(8, 7) * (8 * (1 + 10 * R_ball) + 10)
    J_F2_cap = J_per_tau * tau_cap

    def Lnum(pp, k):
        return 2 ** pp * (2 * pp) ** k * (1 + Q(k * (pp + 1), pp))
    const_ok = all(Lnum(4, k) == 16 * 8 ** k * (1 + Q(5 * k, 4)) for k in range(9))
    mono_ok = all(Lnum(pp, k) <= Lnum(4, k) for pp in (1, 2, 3, 4) for k in range(9))

    def nested_fixture(n):
        size = 2 ** n
        full = size - 1
        Cm = [[0] * size for _ in range(size)]
        Vm = [[0] * size for _ in range(size)]
        for b in range(size):
            Vm[b ^ full][b] = 1
            for j in range(n):
                if not (b >> j) & 1:
                    Cm[b | (1 << j)][b] += 1

        def mm(x, y):
            return [[sum(x[i][k] * y[k][j] for k in range(size)) for j in range(size)] for i in range(size)]
        Am = Vm
        out = []
        for k in range(1, 2 * n + 2):
            Am = [[p1 - q1 for p1, q1 in zip(r1, r2)] for r1, r2 in zip(mm(Cm, Am), mm(Am, Cm))]
            out.append((k, Am[full][0], all(x == 0 for row in Am for x in row)))
        return out
    f4, f2 = nested_fixture(4), nested_fixture(2)

    def validate_am2_hypotheses(pk):
        require(pk['onsite'] == 'h_x>=Q_x with Haar vacuum', 'H1 on-site operator')
        require(pk['max_support'] <= p_support, 'H3 support size exceeds the AM2 p=4')
        require(pk['J'] <= J0, 'H4 per-site sum exceeds J_0')
        require(pk['each_face_once'] is True, 'H2 every retained face charged exactly once')
        require(pk['J_counts_incoming'] is True, 'J must count every group containing the site (incoming anchors)')
        require(pk['reference'] == 'haar', 'F2 keeps the Haar product reference; clipped on-site references are a different model')
        require(GR * J0 < R_ball and 2 * GpR * J0 < 1, 'contraction at J_0')
        return True
    hyp = {'onsite': 'h_x>=Q_x with Haar vacuum', 'max_support': max(int(a1['max_group_support']) for a1 in F2_audit.values()),
           'J': J_F2_cap, 'each_face_once': True, 'J_counts_incoming': True, 'reference': 'haar'}

    def hmut(**kw):
        h2 = dict(hyp)
        h2.update(kw)
        return lambda: validate_am2_hypotheses(h2)
    check('padding_family_contraction_proved',
          validate_am2_hypotheses(hyp) and J_F2_cap == J0 and GR == GR_rep and GpR == GpR_rep and const_ok and mono_ok
          and f4[7][1] == factorial(8) and f4[8][2] and f2[3][1] == factorial(4) and f2[4][2]
          and rejected(hmut(max_support=5), 'merged_two_anchor_groups_support_five')
          and rejected(hmut(J=3 * J_per_tau * tau_cap), 'faces_charged_with_norm_one_J_84')
          and rejected(hmut(each_face_once=False), 'face_charged_in_two_groups')
          and rejected(hmut(J_counts_incoming=False), 'outgoing_star_only_J_7')
          and rejected(hmut(reference='literal_vertex_box_clipped_onsite'), 'literal_vertex_boxes_relabelled_F2'),
          hypotheses={'H1': 'h_x>=Q_x, Haar vacuum, compact resolvent (unchanged on-site operator)',
                      'H2': 'V^(2)=sum_b phi_b^(Lambda_N), bounded self-adjoint, supported in X_b, each face once',
                      'H3': 'max |X_b| <= p=4 (all smaller supports are covered: the majorant is increasing in p)',
                      'H4': "J^(2)<=28|tau|<=J_0 at the cap (equality at the bulk)",
                      'H5': 'finite volume; product spectral cutoffs commute with H_0 and do not increase J or supports'},
          exp_one_eighth_upper=s(exp_upper), G_R_upper=s(GR), G_prime_R_upper=s(GpR), J_F2_at_cap=s(J_F2_cap), J_0=s(J0),
          self_map=s(J0 * GR), self_map_bound=s(R_ball), exclusion=s(2 * J0 * GpR),
          termination_fixtures={'four_site_order8': f4[7][1], 'four_site_order9_zero': f4[8][2],
                                'two_site_order4': f2[3][1], 'two_site_order5_zero': f2[4][2]},
          consequences='fixed point e^{-C}Omega_0 with ||c||_a<=1/64, nondegenerate ground and gap>=1/2 in every cutoff; AM2 section 6 cutoff removal verbatim (same h_x, bounded V^(2) per box)')

    # reset budget (item 1b): reset R to P_R; every group meeting R changes by <=2||group||
    reset = {}
    for F in ('F1', 'F2'):
        for N in (2, 3):
            g = fam[(F, N)]['groups']
            reset[(F, N)] = sum((2 * Q(len(g[b]), 3) for b in groups_meeting_R(F, N)), Q(0))
    per_face_reset = 2 * Q(pins['meet'], 3)

    def validate_reset(anchor_count, group_norm_per_tau):
        require(anchor_count == 7 and group_norm_per_tau <= 7, 'reset must charge all seven incident groups')
        return 2 * anchor_count * group_norm_per_tau
    check('reset_budget_both_families',
          all(reset[k] == reset_R_rep for k in reset) and validate_reset(7, Q(7)) == reset_R_rep
          and CF_per_site == 2 * 4 * 7 and per_face_reset == Q(164, 3) and per_face_reset < reset_R_rep
          and rejected(lambda: validate_reset(2, Q(7)), 'orthant_two_anchor_reset_28')
          and rejected(lambda: validate_reset(7, Q(21)), 'group_norm_21_faces_unscaled'),
          reset_R_over_abs_tau={'%s_N%d' % k: s(v1) for k, v1 in sorted(reset.items())},
          general_C_F_per_site_over_abs_tau=CF_per_site,
          per_face_refinement_over_abs_tau_labelled_not_used=s(per_face_reset),
          argument='variational principle with the trial P_R x (exterior marginal); groups disjoint from R unchanged; F2 group norms <= F1 star norms')

    # trace-norm compactness (AQ1.2) with exact fixtures
    def compact_fixture(C):
        probs = [Q(1, 2), Q(1, 4), Q(1, 8), Q(1, 8)]
        energies = [Q(0), Q(6), Q(12), Q(18)]
        energy = sum((p1 * e1 for p1, e1 in zip(probs, energies)), Q(0))
        require(energy <= C, 'energy bound')
        ok = True
        for L in (Q(6), Q(12)):
            tail = sum((p1 for p1, e1 in zip(probs, energies) if e1 > L), Q(0))
            ok = ok and tail <= energy / L
        return ok
    w = Q(16, 25)
    tn2 = Q(256, 625) + 4 * Q(144, 625)      # (tr)^2-4det for [[0,12/25],[12/25,16/25]]
    check('trace_norm_compactness_both_families',
          compact_fixture(Q(6)) and tn2 == 4 * w - 3 * w * w and tn2 <= 4 * w,
          argument='Tr(rho h_F)<=C_F gives Tr rho(1-Q_L)<=C_F/L and ||rho-Q rho Q||_1<=sqrt(4w-3w^2)<=2sqrt(C_F/L); finite-rank compressions are compact; diagonal extraction over nested cubes',
          families='both: F1 by AQ1 section 2; F2 with the same C_F=56|tau||F| (group norms <= 7|tau|, anchors in F-S)',
          purification_fixture={'psi': '(3/5,4/5)', 'tail_w': s(w), 'trace_norm_squared': s(tn2), 'bound_squared': s(4 * w)})

    # topology_named and the fixed-vector versus moving-vector example
    TOP = {'states': V['topology_states'], 'dynamics': V['topology_dynamics']}

    def validate_topology(t):
        require(t.get('states') == 'trace norm on B(H_R)', 'state topology must be the trace norm on B(H_R)')
        require(t.get('dynamics') == 'norm on compact time windows', 'dynamics topology must be the norm on compact time windows')
        require(t['states'] != t['dynamics'], 'two topologies must be named separately')
        require(t.get('dynamics_statement_for_F2', False) is False, 'no dynamical statement is made for F2 limits')
        return True

    def tmut(**kw):
        t2 = dict(TOP)
        t2.update(kw)
        return lambda: validate_topology(t2)
    check('topology_named',
          validate_topology(TOP) and V['topology_states_param'] == 'trace norm on fixed finite regions'
          and rejected(tmut(states='weak-* on finite-rank observables'), 'weak_star_state_topology')
          and rejected(tmut(dynamics='strong on the GNS space'), 'strong_relabelled_as_norm_dynamics')
          and rejected(tmut(dynamics='trace norm on B(H_R)'), 'one_topology_for_both')
          and rejected(tmut(dynamics_statement_for_F2=True), 'dynamics_claimed_for_F2_limits'),
          states=TOP['states'], dynamics=TOP['dynamics'], states_contract_parameter=V['topology_states_param'])

    n_max = 8
    moving = [{(k, k): Q(1)} for k in range(1, n_max + 1)]
    moving_pair = all(sum(abs(x) for x in op_add(moving[i], moving[j], -1).values()) == 2
                      for i in range(n_max) for j in range(n_max) if i != j)
    weak_zero = all(moving[n].get((k, k), 0) == 0 for k in range(1, 4) for n in range(4, n_max))
    energies_moving = [k for k in range(1, n_max + 1)]
    Dm = Q(1, 100)
    weak_mass = 1 - Dm / 2

    def validate_compactness(energy_list, C):
        require(max(energy_list) <= C, 'no uniform energy bound: trace mass may escape (moving vectors)')
        return True
    fixed_disp = [4 * Q(1, n) for n in range(1, 50)]      # |e^{i pi/n}-1| <= pi/n <= 4/n
    moving_disp = [Q(2)] * 49                              # (e^{i pi}-1) e_{2n}: norm 2 at every n

    def validate_norm_continuity(sup_values):
        require(min(sup_values) < Q(1, 10), 'no norm continuity on all of B(H): the moving vector keeps the difference 2')
        return True
    check('fixed_vector_versus_moving_vector_example',
          moving_pair and weak_zero and validate_compactness([1] * n_max, 1) and weak_mass < 1
          and validate_norm_continuity(fixed_disp)
          and rejected(lambda: validate_compactness(energies_moving, 1), 'moving_vectors_claimed_compact')
          and rejected(lambda: validate_norm_continuity(moving_disp), 'strong_continuity_claimed_as_norm_continuity'),
          states_example='rho_n=|e_n><e_n| (moving): ||rho_n-rho_m||_1=2, weak limit 0, energy n unbounded; rho_n=|e_1><e_1| (fixed): converges; (1-D/2)|e_0><e_0|+(D/2)|e_n><e_n| has weak limit of trace 1-D/2',
          dynamics_example='U(t)e_j=e^{ijt}e_j, A e_j=e_{2j}: fixed vector e_1 gives |e^{i pi/n}-1|<=4/n; moving vector e_n gives 2 for every n',
          weak_limit_trace_example=s(weak_mass))

    # ======================= two families named; verdict logic =======================
    families_verified = {V['families'][0]: F1_ok, V['families'][1]: F2_ok}

    def forward_verdict(fv, closeness, first_order):
        require(len(fv) == 2 and set(fv) == set(V['families']), 'both contract families must be named')
        if not all(fv.values()):
            return 'insufficient'
        if not closeness or not first_order:
            return 'limited'
        return 'accepted_within_scope'

    def validate_families(names):
        require(sorted(names) == sorted(V['families']), 'families differ from the two named contract families')
        return True
    check('two_families_named',
          validate_families(list(families_verified)) and all(families_verified.values())
          and rejected(lambda: validate_families(V['families'][:1]), 'one_family_only')
          and rejected(lambda: validate_families(V['families'] + ['literal vertex boxes (I1 section 7)']), 'third_family_literal_boxes')
          and rejected(lambda: validate_families(['positive orthant boxes', V['families'][1]]), 'orthant_boxes_substituted'),
          F1=V['families'][0], F2=V['families'][1], verified=families_verified)

    # ======================= item 2: AV1 tier (ii) and the closeness 2D =======================
    per_face = Q(1, 72) * Q(1, 2)                  # coefficient tau/72 times ||W_f Omega_0||=1/2
    t1_per_tau = pins['per_factor'] * per_face
    inp = {sg: tier_ii_inputs(tv, J_per_tau, t1_per_tau, GpR) for sg, tv in taus.items()}
    eps = {}
    Dv = {}
    for sg in taus:
        eps[sg], Dv[sg] = density_route_D(inp[sg])
    D = Dv['+']
    D_scal = {k: density_route_D(tier_ii_inputs(tau_cap / k, J_per_tau, t1_per_tau, GpR))[1] for k in (10, 100)}
    check('av1_tier_ii_bound_both_families',
          per_face == Q(1, 144) and t1_per_tau == Q(49, 144) and D == Dv['-'] == D_gate
          and inp['+']['T'] == Q(49, 14398580736) and inp['+']['rho'] == Q(3773, 11248891200000000)
          and D_scal[10] < D and D_scal[100] < D_scal[10] and 99 <= D / D_scal[100] <= 101,
          tier='ii (AV1 forward density route)', T=s(inp['+']['T']), rho=s(inp['+']['rho']), eps=s(eps['+']),
          D=s(D), D_preview=dec(D), D_equals_av1_gate=True, D_ratio_tau_over_100=dec(D / D_scal[100], 10),
          families='identical inputs for F1 and F2: J<=28|tau|, first-order faces per site <=49, tau/72 per face, same Haar reference',
          sign_note='only |tau| enters; the -tau value is a replay of the same formula, not a second confirmation')

    twoD = 2 * D
    target = V['target']
    # sharpness of the triangle route: two pure states at distance D_ex from P with mutual distance 2 D_ex cos(phi)
    mm_ = Q(1, 1000)
    cph, sph = (1 - mm_ ** 2) / (1 + mm_ ** 2), 2 * mm_ / (1 + mm_ ** 2)
    vp, vm = (cph, sph), (cph, -sph)

    def proj(v):
        return [[v[i] * v[j] for j in range(2)] for i in range(2)]

    def pure_distance_sq_half(u, v):      # (trace norm)^2/4 for a rank-2 trace-zero difference: Tr(Delta^2)/2
        Pu, Pv = proj(u), proj(v)
        Dm2 = [[Pu[i][j] - Pv[i][j] for j in range(2)] for i in range(2)]
        return sum(Dm2[i][j] * Dm2[j][i] for i in range(2) for j in range(2)) / 2
    Dex = 2 * sph
    d_pm = 4 * sph * cph
    sharp_ok = (pure_distance_sq_half(vp, (Q(1), Q(0))) == (Dex / 2) ** 2 and pure_distance_sq_half(vm, (Q(1), Q(0))) == (Dex / 2) ** 2
                and pure_distance_sq_half(vp, vm) == (d_pm / 2) ** 2 and d_pm == 2 * Dex * cph and d_pm < 2 * Dex)

    def closed_ball(seq_dist, bound):
        require(all(x <= bound for x in seq_dist), 'finite-volume densities outside the ball')
        return True
    check('closeness_2D_any_two_limits',
          twoD <= target and sharp_ok and closed_ball([D, D], D)
          and rejected(lambda: closed_ball([D, 2 * D], D), 'limit_outside_closed_ball'),
          two_D=s(twoD), two_D_preview=dec(twoD), target=s(target), margin_target_over_2D=dec(target / twoD, 8),
          proof='||rho_R-rho\'_R||_1<=||rho_R-P_R||_1+||P_R-rho\'_R||_1<=D+D; each limit density is a trace-norm limit of finite-volume densities in the closed D-ball around P_R',
          quantifier='any two subsequential limits of F1 and/or F2 (same or different family) at the same tau, |tau|<=10^-8, either sign',
          effect_refinement='for 0<=A<=1: |omega(A)-omega\'(A)|<=D (trace-zero difference)',
          sharpness_example={'D_ex': s(Dex), 'mutual_distance': s(d_pm), 'ratio_to_2D_ex': s(cph)},
          statement='uniform local closeness; not uniqueness, whole-sequence convergence, translation invariance or a rate in N')

    # subsequence versus whole sequence; closeness is not uniqueness; enclosing interval is not equality
    seq = [vp if N % 2 == 0 else vm for N in range(2, 20)]
    even_const = all(seq[i] == vp for i in range(0, len(seq), 2))
    odd_const = all(seq[i] == vm for i in range(1, len(seq), 2))
    consecutive = [pure_distance_sq_half(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]

    def validate_whole_sequence(dist_sq_list):
        require(all(x == 0 for x in dist_sq_list[-4:]), 'whole sequence is not Cauchy')
        return True

    def validate_rate(dist_sq_list, C):
        for i, x in enumerate(dist_sq_list):
            require(x <= (C / (i + 2)) ** 2, 'claimed 1/N rate violated')
        return True
    check('subsequence_versus_whole_sequence',
          even_const and odd_const and all(x == (d_pm / 2) ** 2 for x in consecutive)
          and rejected(lambda: validate_whole_sequence(consecutive), 'whole_sequence_convergence_claimed')
          and rejected(lambda: validate_rate(consecutive, Dex), 'rate_in_N_claimed'),
          example='Lambda_N alternating between two densities within D_ex of P: each parity subsequence converges, the whole sequence does not; no rate in N')

    CLAIMS = {'uniqueness_claimed': False, 'whole_sequence_claimed': False, 'rate_claimed': False,
              'translation_invariance_claimed': False, 'boundary_independence_of_dynamics_claimed': False}

    def validate_claims(cl):
        for k1, v1 in V['gate_fields'].items():
            require(cl.get(k1) is v1, 'gate field ' + k1 + ' must be ' + str(v1))
        return True

    def cmut(**kw):
        c2 = dict(CLAIMS)
        c2.update(kw)
        return lambda: validate_claims(c2)
    check('local_closeness_not_uniqueness',
          validate_claims(CLAIMS) and vp != vm and pure_distance_sq_half(vp, vm) > 0 and d_pm <= 2 * Dex
          and 'uniform_local_closeness_not_uniqueness' in V['sub_labels']
          and rejected(cmut(uniqueness_claimed=True), 'uniqueness_claimed')
          and rejected(cmut(translation_invariance_claimed=True), 'translation_invariance_claimed')
          and rejected(cmut(boundary_independence_of_dynamics_claimed=True), 'boundary_independence_of_dynamics_claimed'),
          label='uniform_local_closeness_not_uniqueness',
          witness='two distinct states both within D_ex of P_R, mutual distance 2 D_ex cos(phi) > 0')

    def validate_equal(x, y):
        require(x == y, 'values in a common enclosing interval need not be equal')
        return True
    check('common_enclosing_interval_not_equality',
          aw2_lo < aw2_hi and aw2_lo <= tau_cap / 144 <= aw2_hi
          and rejected(lambda: validate_equal(aw2_lo, aw2_hi), 'two_limits_in_AW2_enclosure_declared_equal')
          and rejected(lambda: validate_equal(vp, vm), 'two_states_in_D_ball_declared_equal'),
          aw2_enclosure=[s(aw2_lo), s(aw2_hi)], aw2_width=s(aw2_hi - aw2_lo),
          note='omega(W) of every limit lies in the AW2 enclosure; two limits may still differ by up to its width; equality is never inferred')

    # ======================= item 3: the first-order reduced density =======================
    gram_ok = all(len(fl & gl) <= 1 for i, fl in enumerate(F_R_links) for gl in F_R_links[i + 1:])
    EW = [haar_W_moment(n) for n in range(9)]
    EWw = [weyl_W_moment(n) for n in range(9)]
    moments_ok = EW == EWw and EW[:5] == [1, 0, Q(1, 4), 0, Q(1, 8)] and EW[8] == Q(7, 128)
    energy_ok = all(8 * 4 * Q(3, 4) == 24 and len(fl) == 4 for fl in F_R_links)
    # orthonormal basis {Omega_R, e_f=2 W_f Omega_R}; rho1 = (tau/144) sum_f (|e_f><Omega|+|Omega><e_f|)
    nb = 1 + len(F_R)

    def rho1_matrix(tau):
        M = [[Q(0)] * nb for _ in range(nb)]
        for i in range(1, nb):
            M[0][i] = M[i][0] = tau / 144
        return M

    def mmul(A, B):
        return [[sum((A[i][k] * B[k][j] for k in range(nb)), Q(0)) for j in range(nb)] for i in range(nb)]
    M = rho1_matrix(tau_cap)
    M2 = mmul(M, M)
    M3 = mmul(M2, M)
    lam2 = len(F_R) * (tau_cap / 144) ** 2
    trM, trM2 = sum(M[i][i] for i in range(nb)), sum(M2[i][i] for i in range(nb))
    minpoly_ok = all(M3[i][j] == lam2 * M[i][j] for i in range(nb) for j in range(nb))
    tn_sq = 4 * lam2                                   # ||rho1||_1^2 = (2 lambda)^2
    tn_up = sqrt_up(10) * abs(tau_cap) / 72            # directed upper bracket of sqrt(10)|tau|/72
    require(tn_up ** 2 >= tn_sq and (tn_up - abs(tau_cap) / (72 * 10 ** 15)) ** 2 < tn_sq, 'trace-norm bracket')
    # W matrix elements: <Omega|W|e_f> = 2 E[W W_f] = (1/2) delta_{f,W}
    iW = [face_key(f) for f in F_R].index(face_key(wilson_face)) + 1
    W_el = [Q(0)] * nb
    for i, fl in enumerate(F_R_links, start=1):
        if fl == W_links:
            W_el[i] = 2 * EW[2]
        else:
            require(link_parity_vanishes([fl, W_links]), 'a face other than W must have a singly covered link against W')
            W_el[i] = Q(0)
    trW = sum((M[0][i] * W_el[i] + M[i][0] * W_el[i] for i in range(1, nb)), Q(0))
    parity_W2 = all(link_parity_vanishes([fl, W_links, W_links]) or (fl == W_links and EW[3] == 0) for fl in F_R_links)
    first_order_per_face = (Q(-1, 3) / 24, Q(-1, 24) / 3)     # normalized: -(tau/3)/24 ; alpha units: -(tau/24)/3
    check('first_order_density_explicit',
          gram_ok and moments_ok and energy_ok and trM == 0 and trM2 == 2 * lam2 and minpoly_ok and trW == tau_cap / first_den
          and parity_W2 and first_order_per_face[0] == first_order_per_face[1] == Q(-1, 72) and W_el[iW] == Q(1, 2)
          and len(F_R) == pins['inside'] == 10,
          faces_owner_set_R=F_R_labels, wilson_face_index=iW,
          formula='rho^(1)_R = -(|c^(1)_R><Omega_R| + h.c.) = (tau/72) sum_{f: M_f=R} (|W_f Omega_R><Omega_R| + h.c.) = (tau/144) sum_f (|e_f><Omega_R| + |Omega_R><e_f|), e_f=2 W_f Omega_R orthonormal',
          matrix_basis='{Omega_R, e_f (10 faces)}; first row and column tau/144, zero elsewhere',
          eigenvalues='+-sqrt(10)|tau|/144 and 0 (nine-fold): M^3=(10 tau^2/144^2) M, Tr M=0, Tr M^2=2*10 tau^2/144^2',
          trace_norm_squared=s(tn_sq), trace_norm_upper=s(tn_up), trace_norm_preview=dec(tn_up),
          tr_rho1_W=s(trW), tr_rho1_W_equals_aw1='+tau/%d' % first_den, tr_rho1_W2_minus_quarter='0 (parity)',
          haar_moments=[s(x) for x in EW], per_face_coefficient='-tau/72 (both unit systems)',
          properties='self-adjoint, trace zero, gauge invariant (Wilson loops), odd in tau')

    # marginal of straddling first-order creations vanishes (a link owned outside R has Haar mean zero)
    strad_zero = all(links_outside[face_key(f)] >= 1 for f in straddling)
    inside_all_R = all(links_outside[face_key(f)] == 0 for f in inside)

    def validate_marginal_faces(face_list):
        for f in face_list:
            require(links_outside[face_key(f)] == 0, 'a face with a link owned outside R has zero first-order R-marginal')
        require(len(face_list) == pins['inside'], 'first-order density uses exactly the faces with owner set R')
        return True
    check('first_order_marginal_straddling_zero',
          strad_zero and inside_all_R and validate_marginal_faces(inside) and max(pair_shared) <= 1
          and rejected(lambda: validate_marginal_faces(meet_faces), 'all_82_faces_in_rho1')
          and rejected(lambda: validate_marginal_faces(inside + one_site[:1]), 'straddling_face_given_identity_outside_links'),
          straddling_faces=len(straddling), min_links_outside_R_for_straddling=min(links_outside[face_key(f)] for f in straddling),
          reason='Tr_out |W_f Omega_0><Omega_0| = |<Omega_out|W_f Omega_0>><Omega_R|, and <Omega_out|W_f Omega_0>=0 when some link of f is owned outside R (E[U]=0 for a single spin-1/2 factor)',
          normalization='<Omega_0,c^(1)>=0 so the first-order norm correction vanishes')

    # family independence and sign
    fam_R = {(F, N): sorted(face_key(f) for f in fam[(F, N)]['faces'] if owner_set(f) == Rset) for F in ('F1', 'F2') for N in (2, 3)}
    same_R = len({tuple(v1) for v1 in fam_R.values()}) == 1 and fam_R[('F1', 2)] == sorted(face_key(f) for f in F_R)
    Mm = rho1_matrix(-tau_cap)
    odd_ok = all(Mm[i][j] == -M[i][j] for i in range(nb) for j in range(nb))
    rho1_hat = rho1_matrix(Q(1))
    selection_free = all(rho1_matrix(t)[0][1] == t * rho1_hat[0][1] for t in (tau_cap, tau_cap / 7, -tau_cap / 3))

    def validate_same_first_order(face_lists):
        require(len({tuple(x) for x in face_lists}) == 1, 'first-order density differs between families/boxes')
        return True
    check('first_order_density_family_independent',
          same_R and odd_ok and selection_free and validate_same_first_order(list(fam_R.values()))
          and rejected(lambda: validate_same_first_order([fam_R[('F1', 2)], fam_R[('F1', 2)][:9]]), 'boundary_dependent_first_order_density'),
          boxes_checked=['F1 N=2', 'F1 N=3', 'F2 N=2', 'F2 N=3'], faces_owner_set_R_each=len(fam_R[('F1', 2)]),
          coefficient='rho^(1)_R = tau * rho_hat with rho_hat independent of family, box, cutoff L>=24 and subsequence',
          sign='rho^(1)_R(-tau) = -rho^(1)_R(tau)',
          statement='a statement about a coefficient, not about states: every selection tau -> omega_tau of subsequential limits satisfies ||rho_R(omega_tau)-P_R-tau rho_hat||_1<=K_2\' tau^2')

    # exact creation-algebra fixture for the second-order decomposition
    runs = [fixture_run(k) for k in range(4)]
    fx = runs[0]
    om = (0, 0)
    cre = fx['cre']
    n2, d2 = fx['n2'], fx['d2']
    e2 = d2 / n2
    eta = fx_add({k: x / n2 for k, x in fx['xi'].items()}, FIX_C1R)
    remR = fx_add(cre[(0, 1)], FIX_C1R, -1)
    eta_am2 = fx_add(fx_add({k: -x for k, x in remR.items()}, {(k[0], 0): -x for k, x in cre[(0,)].items()}),
                     {(0, k[0]): -x for k, x in cre[(1,)].items()})
    strad_I = [I for I in fx['A'] if not set(I) <= {0, 1}]
    eta_str = {}
    for I in strad_I:
        eta_str = fx_add(eta_str, {k: -x / n2 for k, x in fx_contract_out(fx_apply(cre[I], I, fx['psi_out']), fx['phi']).items()})
    I0 = [I for I in fx['A'] if 0 in I and 1 not in I]
    Iz = [I for I in fx['A'] if 1 in I and 0 not in I]
    eta_pair = {}
    for I in I0:
        for J in Iz:
            if not set(I) & set(J):
                vec = fx_apply(cre[I], I, fx_apply(cre[J], J, fx['psi_out']))
                eta_pair = fx_add(eta_pair, {k: x / n2 for k, x in fx_contract_out(vec, fx['phi']).items()})
    decomp_ok = eta == fx_add(fx_add(eta_am2, eta_str), eta_pair) and eta.get(om, 0) == 0
    P = {(om, om): Q(1)}
    Y = op_rank2(FIX_C1R, {om: Q(1)})
    rho1_fx = op_scale(Y, Q(-1))
    Xop = op_rank2(eta, {om: Q(1)})
    sig = op_scale(fx['sigma'], 1 / n2)
    rhs = op_add(op_scale(op_add(op_add(Xop, sig), op_scale(P, -e2)), 1 / (1 + e2)), op_scale(Y, e2 / (1 + e2)))
    lhs = op_add(op_add(fx['rhoR'], P, -1), rho1_fx, -1)
    rR_ok = lhs == rhs
    X2 = op_mul(Xop, Xop)
    X2_ok = X2 == op_add(op_scale(P, fx_norm2(eta)), {(k1, k2): a * b for k1, a in eta.items() for k2, b in eta.items()})
    sig_ok = all(k[0] != om and k[1] != om for k in fx['sigma']) and sum((x for (k1, k2), x in fx['sigma'].items() if k1 == k2), Q(0)) == d2
    # component bounds (squared comparisons with rational norms)
    nrm = {I: sum(abs(x) for x in cI.values()) if len(cI) == 1 else None for I, cI in cre.items()}
    nrm[(0, 1)] = Q(1, 10) + Q(1, 200)
    B_am2 = Q(1, 200) + nrm[(0,)] + nrm[(1,)]
    t_u = {2: nrm[(2,)] + nrm[(2, 3)], 3: nrm[(3,)] + nrm[(2, 3)]}
    amp_ok = True
    for u in (2, 3):
        exc = {k: x for k, x in fx['psi_out'].items() if k[u] != 0}
        amp_ok = amp_ok and fx_norm2(exc) <= t_u[u] ** 2 * n2
    B_str = sum((nrm[I] * t_u[[x for x in I if x >= 2][0]] for I in strad_I), Q(0))
    A0 = sum((nrm[I] for I in I0), Q(0))
    Az = sum((nrm[I] for I in Iz), Q(0))
    B_pair = A0 * Az
    eps_fx = sum((nrm[I] for I in fx['A']), Q(0)) + A0 * Az
    bounds_ok = (fx_norm2(eta_am2) <= B_am2 ** 2 and fx_norm2(eta_str) <= B_str ** 2 and fx_norm2(eta_pair) <= B_pair ** 2
                 and e2 <= eps_fx ** 2 and amp_ok)
    spect_ok = all(r['rhoR'] == fx['rhoR'] for r in runs) and len({r['Z'] for r in runs}) == 4 and all(r['identity'] for r in runs)

    def fixture_identity(drop):
        r = fixture_run(1, drop)
        require(r['identity'], 'reduced-density identity fails: ' + drop)
        return True

    def numerator_only():
        a0, a1 = fixture_run(0, 'numerator_only'), fixture_run(2, 'numerator_only')
        require(a0['rhoR'] == a1['rhoR'], 'unnormalized R-weight depends on decoupled spectators')
        return True

    def decomposition_without_pairs():
        require(eta == fx_add(eta_am2, eta_str), 'eta decomposition misses the two-creation term')
        return True
    check('second_order_density_fixture',
          fx['identity'] and decomp_ok and rR_ok and X2_ok and sig_ok and bounds_ok and spect_ok
          and rejected(lambda: fixture_identity('sigma'), 'dropped_Tr_out_delta_delta')
          and rejected(lambda: fixture_identity('straddling_in_xi'), 'straddling_creations_dropped_from_xi')
          and rejected(numerator_only, 'numerator_only_volume_dependent')
          and rejected(decomposition_without_pairs, 'two_creation_term_dropped'),
          model_is_finite_graph=True, transfers_to_aq=False,
          identity_formula='rho_R-P_R-rho1 = [(|eta><Omega|+h.c.) + sigma/n^2 - e^2 P_R]/(1+e^2) + (e^2/(1+e^2))(|c1_R><Omega|+h.c.), exact',
          weights_Z=[s(r['Z']) for r in runs], rhoR_spectator_independent=True,
          component_bounds={'am2': s(B_am2), 'straddling': s(B_str), 'pair': s(B_pair), 'eps': s(eps_fx)},
          rank_two_fact='(|eta><Omega|+h.c.)^2 = ||eta||^2 |Omega><Omega| + |eta><eta| with eta orthogonal to Omega, so its trace norm is 2||eta||')

    # item 3: R-local K_2' and comparison with K_2^+
    K2 = {}
    for sg in taus:
        K2[sg] = k2prime_items(inp[sg], pins)
    K2p_val = K2['+']['total'] / tau_cap ** 2
    K2m_val = K2['-']['total'] / tau_cap ** 2
    K2_orth = k2prime_items(inp['+'], pins, am2_form='orthogonal')['total'] / tau_cap ** 2
    Tn, rn, en, an = inp['+']['T'], inp['+']['rho'], eps['+'], abs(tau_cap) / 144
    K2plus_recomputed = (rn + Tn * Tn + Tn * Tn + en ** 2 + an * en ** 2) / tau_cap ** 2
    K2_scal = {k: k2prime_items(tier_ii_inputs(tau_cap / k, J_per_tau, t1_per_tau, GpR), pins)['total'] for k in (10, 100)}
    ratio_B = K2['+']['total'] / K2_scal[100]
    # second code path: every item re-derived from the enumeration and the pinned T, rho (guards silent undercounts)
    n_str2 = pins['meet'] - pins['inside']
    n_one2 = pins['per_factor'] - pins['containing']
    rem0, remz = rn, rn                                   # anchored remainder at site 0 and at site e_z
    epsR2 = pins['meet'] * an + rem0 + remz + (n_one2 * an + rem0) * (n_one2 * an + remz)
    direct = {'am2_remainder': 2 * (rem0 + remz), 'straddling': 2 * Tn * (n_str2 * an + rem0 + remz),
              'two_creation': 2 * (n_one2 * an + rem0) * (n_one2 * an + remz), 'density': 2 * epsR2 * epsR2,
              'normalization_third_order': 2 * epsR2 * epsR2 * (len(F_R) * an)}
    pinned_ok = (direct == K2['+']['items'] and n_str2 == 72 and n_one2 == 33 and Tn == Q(49, 14398580736)
                 and rn == Q(3773, 11248891200000000) and K2['+']['epsR'] == epsR2)
    check('second_order_K2prime_itemized',
          pinned_ok and K2p_val == K2m_val and K2plus_recomputed == K2plus and K2p_val > K2plus and K2_orth < K2p_val
          and K2_scal[10] / (tau_cap / 10) ** 2 <= K2p_val and K2_scal[100] / (tau_cap / 100) ** 2 <= K2_scal[10] / (tau_cap / 10) ** 2
          and 9900 <= ratio_B <= 10100,
          tier='ii', pins={'faces_meeting_R': pins['meet'], 'straddling_faces_meeting_R': pins['straddling'],
                           'faces_per_R_site_not_containing_the_other': pins['single'], 'faces_owner_set_R': pins['inside']},
          items_over_tau2={k1: s(v1 / tau_cap ** 2) for k1, v1 in K2['+']['items'].items()},
          items_preview={k1: dec(v1 / tau_cap ** 2) for k1, v1 in K2['+']['items'].items()},
          eps_R=s(K2['+']['epsR']), K2_prime=s(K2p_val), K2_prime_preview=dec(K2p_val),
          K2_prime_orthogonal_variant_upper=s(K2_orth), K2_prime_orthogonal_variant_preview=dec(K2_orth),
          K2_plus=s(K2plus), K2_plus_preview=dec(K2plus), K2_plus_reproduced_from_itemization='rho+2T^2+eps^2+a*eps^2 with eps=2T+T^2 (AW1 skeptic form)',
          ratio_K2prime_over_K2plus_preview=dec(K2p_val / K2plus, 8), ratio_orth_over_K2plus_preview=dec(K2_orth / K2plus, 8),
          scaling_ratio_tau_over_100=dec(ratio_B, 10),
          why_larger='K_2^+ bounds |omega(W)-tau/144| for the single observable W, which overlaps only c_R with multiplier 2||W Omega_R||=1; the trace norm over all of B(H_R) sees the remainder at c_R, c_{0}, c_{e_z} with the cross-term multiplier 2 and the 66 one-site straddling faces that W annihilates',
          R_local='all combinatorial pins are faces meeting R; T and rho are the inherited tier-(ii) anchored-norm constants (uniform in N)')

    two_K2 = 2 * K2['+']['total']
    corollary = tn_up + K2['+']['total']
    tn_down = sqrt_down(10) * abs(tau_cap) / 72
    corollary_low = tn_down - K2['+']['total']
    check('second_order_difference_2K2prime',
          two_K2 <= twoD and corollary < D and 0 < corollary_low < tn_sq / tn_up,
          two_K2prime_tau2=s(two_K2), two_K2prime_tau2_preview=dec(two_K2), ratio_2D_over_2K2prime_tau2=dec(twoD / two_K2, 8),
          closeness_order=2,
          statement="||rho_R-rho'_R||_1 <= 2 K_2' tau^2 for any two subsequential limits (either family) at the same tau: the common rho^(1)_R cancels",
          supplementary_corollary={'bound': s(corollary), 'preview': dec(corollary), 'form': "||rho^(1)_R||_1 - K_2' tau^2 <= ||rho_R-P_R||_1 <= ||rho^(1)_R||_1 + K_2' tau^2",
                                   'lower': s(corollary_low), 'lower_preview': dec(corollary_low),
                                   'ratio_D_over_bound': dec(D / corollary, 8),
                                   'status': 'labelled supplementary consequence of item 3; not a contract target; the contract closeness uses the AV1-admitted D'})

    ledger = {
        'state_boundary': {'per_limit': s(D), 'pair': s(twoD), 'source': 'AV1 tier (ii), forward density route, uniform in N and cutoff'},
        'second_order_difference': {'per_limit': s(K2['+']['total']), 'pair': s(two_K2),
                                    'items': {k1: s(v1) for k1, v1 in K2['+']['items'].items()}},
        'arithmetic': 'not_applicable as a numeric cost: exact Fractions; directed upper brackets only for sqrt(2) (labelled variant) and sqrt(10) (trace norm of rho^(1)_R); exp(1/8)<8/7 series enclosure',
    }
    require(sorted(ledger) == sorted(V['error_terms']), 'error terms differ from preregistration')
    check('error_ledger_itemized', sorted(ledger) == sorted(V['error_terms']) and len(ledger) == 3,
          terms=sorted(ledger), rule=V['error_terms_rule'])

    # ======================= item 4: mandatory sentences and gate fields =======================
    jung = read_input(P_JUNG)
    m = match(r'Mandatory sentence template: "(.*?)" Mandatory gate fields: (.*?)\. Forbidden phrasings: (.*?); required: "(.*?)"\. Observation-map rule',
              jung, 'Jung template', re.S)
    jung_template, jung_fields_text, forbidden_text, required_phrase = m.group(1), m.group(2), m.group(3), m.group(4)
    forbidden = re.findall(r'"([^"]+)"', forbidden_text)
    require(forbidden == ['the AQ state', 'the thermodynamic limit', 'unique', 'not'], 'forbidden phrase list parsed')
    slot = '`|omega\'(A) - omega\'\'(A)| <= <constant>(tau)` [order `tau^1`, or `tau^2` after subtracting the common first-order density `rho^(1)_R`]'
    require(slot in jung_template, 'Jung constant slot')
    jung_filled = jung_template.replace(
        slot, '`|omega\'(A) - omega\'\'(A)| <= 2D = ' + s(twoD) + '` (about ' + dec(twoD) + '; order `tau^1`), and `<= 2K_2\' tau^2 = '
        + s(two_K2) + '` (about ' + dec(two_K2) + '; order `tau^2` after subtracting the common first-order density `rho^(1)_R`)')
    tpl = V['template']
    require('<= 2D and agree to first order in tau' in tpl and 'boundary independence of the dynamics' in tpl, 'contract template parsed')
    contract_filled = (tpl + ' Constants: F1 = ' + V['families'][0] + '; F2 = ' + V['families'][1]
                       + '; R = {0,e_z} (48 links, 36 endpoints); observable class B(H_R); tau = +-1/100000000 (and every |tau| <= 1/100000000); 2D = '
                       + s(twoD) + ' (about ' + dec(twoD) + '); first-order agreement: ||rho_R - rho\'_R||_1 <= 2K_2\' tau^2 = '
                       + s(two_K2) + ' (about ' + dec(two_K2) + ').')
    aq1_note = "AQ1's state is a chosen subsequential limit of F1; every statement here holds for each such limit separately and does not identify them."

    def scan_forbidden(texts):
        for t in texts:
            low = t
            require('the AQ state' not in low and 'the thermodynamic limit' not in low, 'forbidden phrasing')
            for sentence in re.split(r'(?<=[.;])\s', low):
                if 'unique' in sentence:
                    require(' not ' in ' ' + sentence + ' ', '"unique" without "not"')
        return True
    def strip_code(text):
        text = re.sub(r'```.*?```', ' ', text, flags=re.S)
        return re.sub(r'`[^`\n]*`', ' ', text)

    def scan_report(text):
        body = strip_code(text)
        require(required_phrase in body, 'required phrase missing from the report: ' + required_phrase)
        low = body.lower()
        require('the aq state' not in low and 'the thermodynamic limit' not in low, 'forbidden phrasing in the report')
        for sentence in re.split(r'(?<=[.;:!?])\s+|\n', low):
            if 'unique' in sentence:
                require(re.search(r'\bnot\b', sentence) is not None, '"unique" without "not" in the report: ' + sentence[:80])
        return True
    report_text = (BASE / 'report.md').read_text(encoding='utf-8')
    GATE = dict(CLAIMS)
    GATE.update({'states_compared': 'all subsequential limits of F1 and F2 (every pair, same or different family, same tau)',
                 'region': 'R={0,e_z} fixed before production (complete cover of the original xz Wilson loop)',
                 'topology': 'trace norm on B(H_R)', 'dynamics_topology_named': 'norm on compact time windows (no dynamical statement)',
                 'closeness_order': 2, 'rate_in_N_claimed': False, 'label': 'uniform_local_closeness_not_uniqueness'})

    def validate_gate(g):
        validate_claims(g)
        for k1 in ('states_compared', 'region', 'topology', 'closeness_order', 'label'):
            require(k1 in g, 'missing gate field ' + k1)
        require(g['topology'] == 'trace norm on B(H_R)' and g['closeness_order'] in (1, 2), 'gate topology/order')
        require(g['label'] in V['sub_labels'], 'label outside the allowed sub-labels')
        require(g['rate_in_N_claimed'] is False, 'Jung rate field')
        return True

    def gmut(**kw):
        g2 = dict(GATE)
        g2.update(kw)
        return lambda: validate_gate(g2)

    def gdrop(key):
        g2 = dict(GATE)
        g2.pop(key)
        return lambda: validate_gate(g2)
    check('mandatory_sentence_and_gate_fields',
          scan_forbidden([jung_filled, contract_filled, aq1_note]) and required_phrase in aq1_note and validate_gate(GATE)
          and scan_report(report_text)
          and rejected(lambda: scan_report(report_text + '\nThe limits define the thermodynamic limit.\n'), 'report_phrase_the_thermodynamic_limit')
          and rejected(lambda: scan_report(report_text + '\nThe limits are unique on R.\n'), 'report_unique_without_not')
          and all(f in jung_fields_text for f in ('states_compared', 'region', 'topology', 'closeness_order'))
          and rejected(lambda: scan_forbidden(['the AQ state is fixed by the box.']), 'phrase_the_AQ_state')
          and rejected(lambda: scan_forbidden(['the thermodynamic limit exists.']), 'phrase_the_thermodynamic_limit')
          and rejected(lambda: scan_forbidden(['the limits are unique on R.']), 'unique_without_not')
          and rejected(gmut(uniqueness_claimed=True), 'gate_uniqueness_true')
          and rejected(gdrop('whole_sequence_claimed'), 'gate_field_missing')
          and rejected(gmut(closeness_order=3), 'closeness_order_three')
          and rejected(gmut(topology='weak-*'), 'gate_topology_weak_star'),
          jung_sentence_filled=jung_filled, contract_sentence_filled=contract_filled, required_phrase_used=aq1_note,
          report_scan='report.md scanned with code spans removed: no "the AQ state", no "the thermodynamic limit", every sentence with "unique" contains "not", and "a chosen subsequential" present',
          gate_fields=GATE)

    # ======================= item 6: quantitative boundary comparison; not uniform in a =======================
    QBC = {'closeness_bound': "||rho_R-rho'_R||_1 <= 2D for every pair of subsequential limits of F1 and F2 at the same tau",
           'matching_first_order_term': "the same rho^(1)_R for every such limit, with ||rho_R-rho'_R||_1 <= 2K_2' tau^2",
           'variational_selection_claimed': False,
           'not': 'a variational statement about which boundary condition the infinite-volume theory selects'}

    def validate_qbc(q):
        require('closeness_bound' in q and 'matching_first_order_term' in q, 'definition needs both parts')
        require(q.get('variational_selection_claimed') is False, 'no variational boundary selection')
        return True

    def qmut(**kw):
        q2 = dict(QBC)
        q2.update(kw)
        return lambda: validate_qbc(q2)
    check('quantitative_boundary_comparison_defined',
          validate_qbc(QBC)
          and rejected(qmut(variational_selection_claimed=True), 'boundary_selected_variationally')
          and rejected(lambda: validate_qbc({'closeness_bound': QBC['closeness_bound'], 'variational_selection_claimed': False}), 'closeness_without_first_order_term'),
          definition=QBC)

    g4_cap = dict_num / tau_cap
    tau_at_bridge = Q(dict_num, 32)

    def validate_uniformity(kind):
        require(kind == 'N at fixed lattice spacing a and fixed tau', 'the bounds are uniform in N only, never in a')
        return True
    check('not_uniform_in_a',
          validate_uniformity('N at fixed lattice spacing a and fixed tau') and g4_cap == 9600000000 and tau_at_bridge > tau_cap
          and rejected(lambda: validate_uniformity('lattice spacing a'), 'uniform_in_a_claimed')
          and rejected(lambda: validate_uniformity('continuum limit'), 'uniform_in_N_read_as_continuum'),
          dictionary='tau=96/g^4 (AL1 via the AX1 gate); |tau|<=10^-8 means g^4>=%s' % s(g4_cap),
          counterpoint='at the AL1 bridge value g^4=32, tau=%s exceeds the cap; any asymptotically free trajectory g(a)->0 leaves the cap' % s(tau_at_bridge),
          region_note='R is two coarse factors (a 4a x 2a x 2a fine block): fixed in lattice units, shrinking in physical units as a->0')

    # ======================= remaining contract controls =======================
    clock_ok = V['forbidden_u_div'] == 8 and V['forbidden_exponent'] == 24
    PAIR = {'tau': (tau_cap, tau_cap), 'units': ('normalized delta=alpha/8', 'normalized delta=alpha/8'),
            'clock': ('s=alpha*t_E/hbar, theta=alpha*t/hbar',) * 2}

    def validate_pair(pk):
        require(pk['tau'][0] == pk['tau'][1], 'the two limits must be compared at the same coupling tau')
        require(pk['units'][0] == pk['units'][1], 'common unit convention')
        require(pk['clock'][0] == pk['clock'][1] and 'u=s/8' not in pk['clock'][0] + pk['clock'][1], 'common physical clock')
        return True

    def pmut(**kw):
        p2 = dict(PAIR)
        p2.update(kw)
        return lambda: validate_pair(p2)
    sign_mismatch_norm_sq = 4 * tn_sq           # ||rho1(tau)-rho1(-tau)||_1^2 = (2||rho1||_1)^2
    check('common_clock',
          validate_pair(PAIR) and clock_ok and sign_mismatch_norm_sq > (two_K2) ** 2
          and rejected(pmut(tau=(tau_cap, 8 * tau_cap)), 'F2_normalized_coefficient_read_in_alpha_units_8tau')
          and rejected(pmut(tau=(tau_cap, tau_cap / 2)), 'different_couplings')
          and rejected(pmut(tau=(tau_cap, -tau_cap)), 'opposite_signs_first_order_densities_differ')
          and rejected(pmut(clock=('s=alpha*t_E/hbar, theta=alpha*t/hbar', 'u=s/8')), 'normalized_clock_for_one_family'),
          clock=V['clock'], sign_mismatch_distance_squared=s(sign_mismatch_norm_sq),
          note='the comparison is static (ground states); the common clock fixes G=H/alpha and theta, s for any later dynamical use')

    alpha_fx, hbar_fx = Q(5), Q(7)
    tE = Q(7, 5)
    s_fx = alpha_fx * tE / hbar_fx
    rate_exponent = 3 * alpha_fx * tE / hbar_fx      # energy 3 alpha in physical units

    def validate_coeff(cf, exponent_per_s):
        require(cf == Q(-1, 72), 'first-order coefficient per face must be -tau/72')
        require(exponent_per_s == 3, 'free Wilson decay exponent is 3 in s=alpha t_E/hbar')
        return True
    check('wrong_delta_alpha_hbar_clock',
          validate_coeff(first_order_per_face[0], rate_exponent / s_fx) and s_fx == 1
          and rejected(lambda: validate_coeff(Q(-1, 24) / 24, 3), 'tau_over_576_mixed_units')
          and rejected(lambda: validate_coeff(Q(-1, 3) / 3, 3), 'tau_over_9_mixed_units')
          and rejected(lambda: validate_coeff(Q(-1, 72), 24), 'exponent_24_in_s'),
          nonunit_fixture={'alpha': '5', 'hbar': '7', 't_E': '7/5', 's': s(s_fx)},
          units='normalized: -(tau/3)/24; alpha units: -(tau/24)/3; both -tau/72')

    mean_m, dm = Q(1, 4), Q(1, 100)
    vec_res, scal_res, unc_res = dm ** 2, -2 * mean_m * dm - dm ** 2, mean_m ** 2

    def validate_centering(kind, residue):
        require(kind == V['centering'], 'the density comparison is uncentered (contract centering: none)')
        require(residue == vec_res, 'vector centering residue is d^2')
        return True
    check('vector_versus_scalar_centering',
          validate_centering('none', vec_res) and vec_res == Q(1, 10000) and scal_res == Q(-51, 10000) and unc_res == Q(1, 16)
          and rejected(lambda: validate_centering('none', scal_res), 'scalar_subtraction_as_vector_centering')
          and rejected(lambda: validate_centering('vector', vec_res), 'centering_imposed_on_density'),
          residues={'vector': s(vec_res), 'scalar': s(scal_res), 'uncentered': s(unc_res)})

    lower_W = tau_cap / 144 - K2plus * tau_cap ** 2

    def validate_first_order(rho1_trace_norm_sq):
        require(rho1_trace_norm_sq > 0, 'first-order density must be charged')
        require(lower_W > K2['+']['total'], 'zero first-order density contradicts omega(W)>=tau/144-K_2^+ tau^2')
        return True
    check('first_order_mean_charged',
          validate_first_order(tn_sq) and trW == tau_cap / 144
          and rejected(lambda: validate_first_order(Q(0)), 'first_order_density_set_to_zero'),
          omega_W_lower_from_aw1=s(lower_W), K2prime_tau2=s(K2['+']['total']), m2_upper=s(D ** 2),
          note='the nonzero first-order mean tau/144 is carried by rho^(1)_R; m^2<=D^2 remains charged')

    rho1_ratio = tn_sq / (4 * 10 * (tau_cap / 100 / 144) ** 2)
    at4_D = lambda t: 2 * sqrt_up(at4_eps_per_tau * abs(t), 10 ** 20)
    at4_ratio_sq = (at4_eps_per_tau * tau_cap) / (at4_eps_per_tau * tau_cap / 100)

    def validate_exponent(label, ratio):
        lo, hi = {'linear': (99, 101), 'quadratic': (9900, 10100), 'sqrt': (Q(99, 10), Q(101, 10))}[label]
        require(lo <= ratio <= hi, 'scaling exponent does not match its label ' + label)
        return True
    check('tau_scaling_exponent',
          validate_exponent('linear', D / D_scal[100]) and validate_exponent('quadratic', ratio_B) and rho1_ratio == 10000
          and at4_ratio_sq == 100
          and rejected(lambda: validate_exponent('linear', Q(10)), 'sqrt_bound_labelled_linear')
          and rejected(lambda: validate_exponent('linear', ratio_B), 'second_order_labelled_first_order')
          and rejected(lambda: validate_exponent('quadratic', D / D_scal[100]), 'first_order_labelled_second_order'),
          ratios={'D': dec(D / D_scal[100], 10), 'K2prime_tau2': dec(ratio_B, 10), 'rho1_trace_norm_squared': s(rho1_ratio),
                  'AT4_sqrt_squared': s(at4_ratio_sq)})

    MODEL = {'model_id': V['model_id'], 'tau': tau_cap, 'triple': (0, 0, 0), 'reference': V['reference_route'],
             'families': tuple(V['families']), 'J_per_abs_tau': J_per_tau}

    def validate_model(mdl):
        require(mdl['model_id'] == 'AQ_patterned_zero_selected', 'model id')
        require(abs(mdl['tau']) == tau_cap, 'coupling differs from the preregistered cap')
        require(mdl['triple'] == (0, 0, 0), 'nonzero selected triple is another model')
        require(mdl['reference'] == 'haar', 'selected-strip reference is another model')
        require(mdl['families'] == tuple(V['families']), 'families relabelled')
        require(mdl['J_per_abs_tau'] == J_per_tau, 'per-site sum of a different model')
        return True

    def mmut(**kw):
        m2 = dict(MODEL)
        m2.update(kw)
        return lambda: validate_model(m2)
    check('changed_model_relabelled',
          validate_model(MODEL) and validate_model(dict(MODEL, tau=-tau_cap))
          and rejected(mmut(tau=Q(1, 10 ** 14)), 'tau_1e-14')
          and rejected(mmut(triple=(Q(1, 100), 0, 0)), 'nonzero_triple')
          and rejected(mmut(reference='selected_strip'), 'selected_strip_reference')
          and rejected(mmut(model_id='FG(one_plaquette,j_max=3/2,tau_FG,I1.5,invariant)'), 'finite_graph_model')
          and rejected(mmut(model_id='AQ_uniform_routeB', J_per_abs_tau=J_routeB), 'uniform_route_B_model')
          and rejected(mmut(families=(V['families'][0], 'literal vertex boxes (I1 section 7)')), 'literal_vertex_boxes_family'),
          model_id=V['model_id'], state_provenance=V['state_provenance'])

    def validate_route(tier_label, route, value):
        require(tier_label == 'ii', 'only the AV1-admitted tier (ii) enters the closeness constant')
        require(route == 'density', 'the forward route is the explicit reduced-density inequality')
        e_, d_ = density_route_D(inp['+'])
        require(value == d_, 'value not certified by the density route at the tier (ii) eps')
        return True
    eps_rev = 82 * an + 2 * rn + Tn ** 2
    D_density_at_eps_rev = 2 * eps_rev * (1 + eps_rev) / (1 + eps_rev ** 2)
    check('tier_mixing_rejected',
          validate_route('ii', 'density', D) and D_density_at_eps_rev > D_rev_gate
          and rejected(lambda: validate_route('i', 'density', D_i_gate), 'tier_i_value_in_closeness')
          and rejected(lambda: validate_route('ii', 'density', D_rev_gate), 'reverse_fidelity_refinement_under_density_route')
          and rejected(lambda: validate_route('ii', 'density', at4_D(tau_cap)), 'AT4_sqrt_bound_labelled_tier_ii')
          and rejected(lambda: k2prime_items(inp['+'], pins, tier_labels={'density': 'i'}), 'crude_density_item_inside_K2prime')
          and rejected(lambda: tier_ii_inputs(tau_cap, J_per_tau, t1_per_tau, Q(0)), 't_equals_t1_without_remainder'),
          D_density_at_reverse_eps=s(D_density_at_eps_rev), D_reverse_refinement=s(D_rev_gate),
          note='the reverse 82-face value needs the fidelity inequality; the density formula at its eps exceeds it')

    twoD_i = 2 * D_i_gate
    twoD_at4 = 2 * at4_D(tau_cap)
    verdict = forward_verdict(families_verified, twoD <= target, same_R and rR_ok)

    def validate_verdict(reported, fv, closeness, first):
        require(reported == forward_verdict(fv, closeness, first), 'reported verdict differs from the contract acceptance rule')
        return True
    check('insufficient_verdict_retained',
          twoD_i > target and twoD_at4 > target and verdict == 'accepted_within_scope'
          and forward_verdict({V['families'][0]: True, V['families'][1]: False}, True, True) == 'insufficient'
          and forward_verdict(families_verified, True, False) == 'limited'
          and rejected(lambda: validate_verdict('accepted_within_scope', {V['families'][0]: True, V['families'][1]: False}, True, True), 'failed_family_relabelled_accepted')
          and rejected(lambda: validate_verdict('accepted_within_scope', families_verified, True, False), 'missing_first_order_relabelled_accepted')
          and rejected(lambda: require(twoD_i <= target, 'tier (i) retuned to pass'), 'tier_i_retuned'),
          tier_i_two_D=s(twoD_i), tier_i_two_D_preview=dec(twoD_i), tier_i_meets_target=False,
          at4_two_D_upper=s(twoD_at4), at4_two_D_preview=dec(twoD_at4), at4_meets_target=False,
          retained='tier (i) and the AT4 square-root bound fail the 2D target and are retained as failures, not retuned')

    check('exact_arithmetic_admission',
          rat('1/1250000') == target
          and rejected(lambda: rat(1e-8), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('nan'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator'),
          arithmetic='fractions.Fraction throughout; previews truncated from exact rationals; no numerical-library import')

    def validate_pair_sum(total, parts):
        require(total == sum(parts, Q(0)), 'deterministic errors add linearly')
        return True
    item_vals = list(K2['+']['items'].values())
    rss_sq = sum((x * x for x in item_vals), Q(0))
    check('root_n_misuse',
          validate_pair_sum(twoD, [D, D]) and validate_pair_sum(K2['+']['total'], item_vals) and K2['+']['total'] ** 2 > rss_sq
          and rejected(lambda: validate_pair_sum(sqrt_down(2) * D, [D, D]), 'rss_of_two_state_terms')
          and rejected(lambda: validate_pair_sum(D / sqrt_up(Q(2)), [D]), 'division_by_sqrt_N')
          and rejected(lambda: validate_pair_sum(twoD / 64, [D, D]), 'division_by_64'),
          note='the pair bound is D+D, the remainder is the linear item sum; neither is divided by sqrt(N) or combined in quadrature')

    FLAGS = {'continuum_claim': False, 'uniform_wilson_claim': False, 'resolved_interaction_shift': False,
             'scientific_priority_verified': False, 'weak_coupling_claim': False}

    def validate_flags(fl):
        for k1, v1 in FLAGS.items():
            require(fl.get(k1) is v1, 'claim flag ' + k1 + ' must be false')
        return True

    def fmut(**kw):
        f2_ = dict(FLAGS)
        f2_.update(kw)
        return lambda: validate_flags(f2_)
    check('no_priority_or_continuum_claim',
          validate_flags(FLAGS)
          and rejected(fmut(continuum_claim=True), 'continuum_true') and rejected(fmut(scientific_priority_verified=True), 'priority_true')
          and rejected(fmut(uniform_wilson_claim=True), 'uniform_wilson_true') and rejected(fmut(resolved_interaction_shift=True), 'shift_true'),
          historical_or_occult_numeric_premise=False)

    forward_list = ['AGENTS.md', CONTRACT_REL] + V['shared'] + V['forward_additional']
    reverse_list = ['AGENTS.md', CONTRACT_REL] + V['shared']
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    bad = ('research/round32/skeptic/triage.md', 'research/round32/experts/', 'research/round32/forward/ay1', 'deliberation-')

    def validate_isolation(decl, lst):
        require(decl is True, 'contract does not declare reverse premise isolation')
        for item in lst:
            require(not any(b1 in item for b1 in bad), 'reverse premise isolation violated by ' + item)
        return True
    check('reverse_premise_isolation',
          sorted(inventory) == sorted(set(forward_list)) and len(inventory) == 32 and validate_isolation(V['reverse_isolation'], reverse_list)
          and rejected(lambda: validate_isolation(False, reverse_list), 'declaration_false')
          and rejected(lambda: validate_isolation(True, reverse_list + ['research/round32/skeptic/triage.md']), 'reverse_reads_triage')
          and rejected(lambda: validate_isolation(True, reverse_list + ['research/round32/experts/jung/loop2-response.md']), 'reverse_reads_jung_note')
          and rejected(lambda: validate_isolation(True, reverse_list + ['research/round32/forward/ay1/report.md']), 'reverse_reads_forward_ay1'),
          forward_inventory_files=len(inventory), reverse_premise_count=len(reverse_list), forward_additional_disclosed=V['forward_additional'],
          limitation='the forward checker verifies the declared inventories only; what the reverse agent actually read is verified by freeze.py and the skeptic')

    # ======================= packet, tampering =======================
    headline = {
        'D': s(D), 'D_preview': dec(D), 'two_D': s(twoD), 'two_D_preview': dec(twoD), 'target_two_D': s(target),
        'target_met': twoD <= target, 'margin_preview': dec(target / twoD, 8),
        'K2_prime': s(K2p_val), 'K2_prime_preview': dec(K2p_val), 'K2_prime_tau2': s(K2['+']['total']),
        'two_K2_prime_tau2': s(two_K2), 'two_K2_prime_tau2_preview': dec(two_K2),
        'K2_prime_orthogonal_variant_upper': s(K2_orth), 'K2_prime_orthogonal_variant_preview': dec(K2_orth),
        'K2_plus': s(K2plus), 'K2_plus_preview': dec(K2plus), 'ratio_K2prime_over_K2plus_preview': dec(K2p_val / K2plus, 8),
        'rho1_R_coefficient_in_orthonormal_basis': 'tau/144', 'rho1_R_trace_norm_squared': s(tn_sq),
        'rho1_R_trace_norm_upper': s(tn_up), 'rho1_R_trace_norm_preview': dec(tn_up),
        'faces_owner_set_R': len(F_R), 'supplementary_single_limit_bound': s(corollary), 'supplementary_single_limit_bound_preview': dec(corollary),
        'two_family_constants': {
            'F1': {'J_per_abs_tau': s(J_per_tau), 'max_group_support': 4, 'reset_R_per_abs_tau': s(reset[('F1', 2)]), 'C_F_per_site_per_abs_tau': s(CF_per_site),
                   'first_order_faces_per_site_max': pins['per_factor'], 'faces_meeting_R': pins['meet'], 'faces_owner_set_R': pins['inside'], 'D': s(D)},
            'F2': {'J_per_abs_tau': s(max(rat(a1['max_J_per_abs_tau_anchor_grouping']) for a1 in F2_audit.values())),
                   'max_group_support': max(a1['max_group_support'] for a1 in F2_audit.values()), 'reset_R_per_abs_tau': s(reset[('F2', 2)]),
                   'C_F_per_site_per_abs_tau': s(CF_per_site), 'first_order_faces_per_site_max': max(a1['max_first_order_faces_per_site'] for a1 in F2_audit.values()),
                   'faces_meeting_R': pins['meet'], 'faces_owner_set_R': pins['inside'], 'D': s(D)},
            'J_0': s(J0), 'self_map': s(J0 * GR), 'exclusion': s(2 * J0 * GpR)},
    }
    label = 'uniform_local_closeness_not_uniqueness'
    verdict_line = (verdict + ' (forward half; the contract acceptance also requires the reverse route and skeptical review); sub-label ' + label)
    packet = {
        'loop': 'AY1', 'direction': 'forward', 'human_author': HUMAN_AUTHOR,
        'contribution_alias': 'HNM-AY1-F forward uniform local closeness of all AQ-type subsequential states and the family-independent first-order density',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha,
        'label': label, 'model': {'model_id': V['model_id'], 'statement': V['model'], 'families': {'F1': V['families'][0], 'F2': V['families'][1]},
                                  'region': 'R={0,e_z}', 'observable_class': 'B(H_R)', 'reference': 'P_R (Haar product)',
                                  'clock': V['clock'], 'boxes': 'centered Lambda_N=[-N,N]^3, N>=2, both families'},
        'tau_values': {sg: s(tv) for sg, tv in taus.items()},
        'headline': headline, 'error_terms_itemized': ledger,
        'topology': {'states': TOP['states'], 'dynamics': TOP['dynamics']},
        'states_compared': GATE['states_compared'], 'region': GATE['region'], 'closeness_order': 2,
        'mandatory_sentence_jung_filled': jung_filled, 'mandatory_sentence_contract_filled': contract_filled,
        'quantitative_boundary_comparison': QBC,
        'first_order_density': {'faces': F_R_labels, 'formula': 'rho^(1)_R = (tau/144) sum_f (|e_f><Omega_R| + |Omega_R><e_f|), e_f = 2 W_f Omega_R',
                                'trace_norm_squared': s(tn_sq), 'tr_W': s(trW)},
        'exclusions': {'contract': V['claim_exclusions'], 'preregistration': V['prereg_exclusions'],
                       'additional': ['no dynamical statement for F2 limits', 'not uniform in the lattice spacing a',
                                      'no lower bound on any distance', 'no identification of limits']},
        'routes_executed': ['forward: product-ordering split with the explicit reduced density (AV1 density route) for both families',
                            'forward: first-order density as the R-marginal of -(c^(1) Omega_0^* + h.c.) restricted to creations meeting R',
                            'forward: R-local second-order itemization K_2\' of ||rho_R-P_R-rho^(1)_R||_1'],
        'routes_not_executed': ['reverse route (vacuum-overlap/fidelity derivative; outside this producer)', 'skeptic post-comparison'],
        'controls_not_implementable_in_check_py': {
            'reverse_premise_isolation': 'declared inventories checked here; the reverse agent\'s actual reads are checked by freeze.py and the skeptic',
            'freeze_and_byte_identical_replays': 'protocol steps executed by research/round32/tools/freeze.py, not by check.py itself',
            'post_comparison': 'skeptic review after both producers freeze'},
        'proposed_forward_verdict': verdict_line,
    }
    packet.update(FLAGS)
    packet.update(CLAIMS)
    packet['rate_in_N_claimed'] = False
    packet['whole_sequence_convergence_claimed'] = False

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
        validate_claims({k1: pk[k1] for k1 in CLAIMS})
        require(sorted(inv) == sorted(set(forward_list)), 'premise snapshot inventory incomplete')
        require(rat(pk['headline']['D']) == density_route_D(inp['+'])[1] == D_gate, 'headline D differs from recomputation')
        require(rat(pk['headline']['two_D']) == 2 * rat(pk['headline']['D']), 'two_D differs from 2D')
        require(rat(pk['headline']['K2_prime']) == k2prime_items(inp['+'], pins)['total'] / tau_cap ** 2, 'K2_prime differs from recomputation')
        require(pk['headline']['target_met'] is (rat(pk['headline']['two_D']) <= target), 'target Boolean differs from recomputation')
        require(len(pk['first_order_density']['faces']) == pins['inside'], 'first-order face list changed')
        require(sorted(pk['model']['families'].values()) == sorted(V['families']), 'families changed')
        require(pk['proposed_forward_verdict'].startswith(forward_verdict(families_verified, True, True)), 'verdict changed')
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
            if ch['id'] == 'padding_family_contraction_proved':
                ch['passed'] = False

    def t_snapshot(pk, inv):
        inv.pop(P_JUNG)

    def t_twoD(pk, inv):
        pk['headline']['two_D'] = s(rat(pk['headline']['two_D']) / 2)

    def t_K2(pk, inv):
        pk['headline']['K2_prime'] = s(rat(pk['headline']['K2_prime']) / 4)

    def t_unique(pk, inv):
        pk['uniqueness_claimed'] = True

    def t_family(pk, inv):
        pk['model']['families'] = {'F1': V['families'][0]}

    def t_faces(pk, inv):
        pk['first_order_density']['faces'] = pk['first_order_density']['faces'][:9]
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(tamper(t_control), 'control_boolean_flipped_hash_rebound')
          and rejected(tamper(t_snapshot), 'jung_snapshot_removed_hash_rebound')
          and rejected(tamper(t_twoD), 'two_D_halved_hash_rebound')
          and rejected(tamper(t_K2), 'K2_prime_quartered_hash_rebound')
          and rejected(tamper(t_unique), 'uniqueness_flag_hash_rebound')
          and rejected(tamper(t_family), 'one_family_hash_rebound')
          and rejected(tamper(t_faces), 'first_order_face_removed_hash_rebound'))

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in V['controls'] if cid not in ids]
    require(not missing, 'contract controls without a check: ' + ','.join(missing))
    positive_only = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch.get('rejected_mutations')]
    require(not positive_only, 'contract controls without a damaging mutation: ' + ','.join(positive_only))
    require(not PENDING, 'rejected mutations not attached to a check')
    packet['checks'] = CHECKS
    packet['contract_controls_covered'] = sorted(V['controls'])
    packet['controls_with_damaging_mutations'] = sum(1 for ch in CHECKS if ch['id'] in V['controls'] and ch.get('rejected_mutations'))
    packet['rejected_mutation_total'] = sum(len(ch.get('rejected_mutations', [])) for ch in CHECKS)
    packet['check_count'] = len(CHECKS)
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
    ap = argparse.ArgumentParser(description='AY1 forward exact checker')
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
    manifest = {'loop': 'AY1', 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': 'AY1', 'direction': 'forward', 'checks': len(result['checks']),
                      'two_D_preview': result['headline']['two_D_preview'], 'K2_prime_preview': result['headline']['K2_prime_preview'],
                      'target_met': result['headline']['target_met']}, sort_keys=True))


if __name__ == '__main__':
    main()
