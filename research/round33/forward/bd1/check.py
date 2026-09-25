#!/usr/bin/env python3
"""BD1 forward producer (characters route): centre-symmetry transfer of the
AW1 parity theorem, the link-flip lemma and the first-order Wilson mean across
the frozen list of gauge groups, the SU(3), SO(3) and SU(5) obstruction cells,
the flip sets E_3 and E_2, and the SU(2) area-parity corollary.

Human project author: Hruday N M (BUNZEEY). AI-assisted forward production
(a Claude model agent acting as the BD1 forward producer).

Standard library only (argparse, fractions, hashlib, itertools, json, math,
pathlib, re).  Every admission Boolean is decided in exact Fraction arithmetic;
decimal strings are truncated previews.  Conditions raise AdmissionError
explicitly (never `assert`), so every check stays active under `python -O`.

Route of computation: characters (Peter-Weyl orthogonality and tensor-product
multiplicities: Pieri for SU(N) fundamental tensor powers, Clebsch-Gordan for
SU(2) and SO(3), charge counting for U(1), direct summation for Z2).  A
forward-internal Weyl-integration cross-check is computed and labelled; it is
not the reverse producer's route and it is never the admission value.

Usage: python3 -B check.py --output /absolute/fresh/directory
"""
import argparse
import hashlib
import itertools
import json
import re
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
LOOP = 'BD1'
HUMAN_AUTHOR = 'Hruday N M (BUNZEEY)'
CONTRACT_REL = 'research/round33/contracts/bd1.json'
CONTRACT_SHA256 = 'a5c8416600c49b0728fdca05cd67c3ff2e53d9fd9e146d4305abcd2da775c1fc'
GATE_SHA256 = {
    'research/round32/advisor/aw1-gate.json': '647dc33795f06a66c12934f64ae408725b5354cf0124b32dc4b18a12eb0541ae',
    'research/round32/advisor/aw2-gate.json': '640a3b0a74c7fcd66318ba7ce2a60942f837ad154f157bc1d69323589b24be62',
    'research/round32/advisor/ay2-gate.json': 'e4faa98884d26d67dd422b382eafb2c52bf88ee679998bc8249003cba88187a6',
    'research/round32/advisor/az1-gate.json': '255ce6702628b26b082ceb0e03732c87be84c9ce6315b65c9792087d0cdc03ad',
    'research/round32/advisor/az2-gate.json': 'd36d53dcad8b1d3e4789d3be76b9e491e73cc5cf2ca88f281f66fd255f98b394',
    'research/round33/advisor/bb2-gate.json': 'ad3fdb4bee935b594c992f6d4246b52aa83b9c0d0d03eb5186bff47b45bb0cca',
}
AW1_GATE = 'research/round32/advisor/aw1-gate.json'
AW2_GATE = 'research/round32/advisor/aw2-gate.json'
AY2_GATE = 'research/round32/advisor/ay2-gate.json'
AZ1_GATE = 'research/round32/advisor/az1-gate.json'
AZ2_GATE = 'research/round32/advisor/az2-gate.json'
BB2_GATE = 'research/round33/advisor/bb2-gate.json'
AW1_F_REL = 'research/round32/forward/aw1/report.md'
AW1_R_REL = 'research/round32/reverse/aw1/report.md'
I1_REL = 'research/round21/forward/i1/report.md'
SELECTION_REL = 'research/round33/advisor/selection-bd1.md'
BA1_REL = 'research/round33/contracts/ba1.json'
BB2_CONTRACT_REL = 'research/round33/contracts/bb2.json'
SCRATCH = '/tmp/claude-0/bd1-forward-private/'
ROUTE = 'characters'
CROSS_ROUTE = 'weyl_integration'
EXPECTED_GROUPS = ['SU(2)', 'SU(3)', 'SU(4)', 'SU(5)', 'U(1)', 'Z2', 'SO(3)']


class AdmissionError(Exception):
    """An admission condition failed or a damaging mutation was accepted."""


def require(condition, message):
    if not condition:
        raise AdmissionError(message)


CHECKS = []
PENDING_MUTATIONS = []


def check(identity, condition, **details):
    require(condition, 'failed check ' + identity)
    require(all(c['id'] != identity for c in CHECKS), 'duplicate check id ' + identity)
    entry = {'id': identity, 'passed': True, 'mutations_rejected': list(PENDING_MUTATIONS)}
    PENDING_MUTATIONS.clear()
    entry.update(details)
    CHECKS.append(entry)


def rejected(mutation, label):
    """Run a damaging mutation; it must raise AdmissionError (recorded on the next check)."""
    try:
        mutation()
    except AdmissionError:
        PENDING_MUTATIONS.append(label)
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
    """Truncated scientific decimal preview of an exact rational (not admission)."""
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


def float_free(obj):
    if isinstance(obj, float):
        return False
    if isinstance(obj, dict):
        return all(float_free(v) for v in obj.values())
    if isinstance(obj, list):
        return all(float_free(v) for v in obj)
    return True


def read_input(rel):
    path = BASE / 'inputs' / rel
    require(path.is_file(), 'missing premise snapshot ' + rel)
    return path.read_bytes()


def match(pattern, text, label):
    m = re.search(pattern, text)
    require(m is not None, 'premise text not parsed: ' + label)
    return m


# ---------------------------------------------------------------------------
# Contract: every group, convention factor, flip set, bracket and template is
# read from the hash-checked snapshot, never typed into this file.
# ---------------------------------------------------------------------------
def load_contract():
    raw = read_input(CONTRACT_REL)
    digest = sha_bytes(raw)
    require(digest == CONTRACT_SHA256, 'contract snapshot bytes differ from the frozen BD1 contract')
    c = json.loads(raw.decode('utf-8'))
    require(c.get('id') == 'BD1' and c.get('status') == 'frozen_before_production' and c.get('round') == 33,
            'wrong contract identity')
    return c, digest


def contract_values(c):
    p = c['parameters']
    pre = c['preregistration']
    req = c['required']
    v = {'raw_parameters': p}
    v['groups'] = list(p['groups'])
    require(v['groups'] == EXPECTED_GROUPS, 'group list differs from the frozen list')
    conv = p['convention']
    v['convention_text'] = conv
    v['link_factor'] = int(match(r'^per-link electric term (\d+) C_2\(r\) in delta units', conv, 'link factor').group(1))
    match(r'C_F = \(N\^2-1\)/\(2N\) for SU\(N\)', conv, 'SU(N) Casimir rule')
    match(r'C_2\(n\) = n\^2 for the U\(1\) charge n', conv, 'U(1) Casimir rule')
    v['so3_CF'] = Q(int(match(r'C_2\(l\) = l\(l\+1\) for SO\(3\) \(so the vector representation has C_F = (\d+),',
                              conv, 'SO(3) rule').group(1)))
    m = match(r'for Z2 C_2 = (\d+) on the even \(trivial\) and C_2 = (\d+) on the odd \(sign\) link state, so that the Z2 '
              r'per-link electric term is (\d+) on the odd state and C_F = (\d+) for Z2 as for U\(1\)', conv, 'Z2 rule')
    v['z2_C_even'], v['z2_C_odd'], v['z2_link_odd'], v['z2_CF'] = (Q(int(m.group(i))) for i in range(1, 5))
    m = match(r"the readings 'electric term (\d+) on the odd state' and '(\d+) - sigma\^x' are other normalizations and "
              r"are rejected", conv, 'rejected Z2 readings')
    v['z2_rejected_link_odd'] = Q(int(m.group(1)))
    v['z2_rejected_sigma_offset'] = int(m.group(2))
    m = match(r'Wilson representation: fundamental for SU\(N\), charge (\d+) for U\(1\), sign for Z2, vector for SO\(3\)',
              conv, 'Wilson representation')
    v['u1_charge'] = int(m.group(1))
    v['wilson_rep'] = {'SU(2)': 'fundamental', 'SU(3)': 'fundamental', 'SU(4)': 'fundamental', 'SU(5)': 'fundamental',
                       'U(1)': 'charge ' + m.group(1), 'Z2': 'sign', 'SO(3)': 'vector'}
    v['mag_den'] = int(match(r'magnetic term -\(tau/(\d+)\) sum_f W_f with W_f = Re chi_fund\(U_f\)/dim fund', conv,
                             'magnetic term').group(1))
    v['face_factor'] = int(match(r'face energy (\d+) C_F', conv, 'face energy').group(1))
    m = match(r'c\^\(1\) = -\(tau/(\d+)\)/\((\d+) C_F\) sum_f W_f Omega_0', conv, 'creation coefficient')
    require(int(m.group(1)) == v['mag_den'] and int(m.group(2)) == v['face_factor'], 'creation coefficient factors')
    m = match(r'omega\(W\) = -2 Re \(W Omega_0, c\^\(1\)\) \+ O\(tau\^2\) = 2 \(tau/(\d+)\) E\[W\^2\]/\((\d+) C_F\) '
              r'\+ O\(tau\^2\) under the I1\.5 sign', conv, 'first-order formula')
    require(int(m.group(1)) == v['mag_den'] and int(m.group(2)) == v['face_factor'], 'first-order formula factors')
    v['su2_check_den'] = int(match(r'reproduces the admitted coefficient 1/(\d+), which is a check of the convention, '
                                   r'not a transferred value', conv, 'SU(2) convention check').group(1))
    require(4 * v['link_factor'] == v['face_factor'], 'face energy is four links of the per-link term')
    require(v['z2_link_odd'] == v['link_factor'] * v['z2_C_odd'], 'Z2 per-link term equals 8 C_2(odd)')
    terms = p['hamiltonian_terms']
    require(len(terms) == 4, 'four hamiltonian terms')
    require(int(match(r'^(\d+) \(delta units\)$', terms[0]['coefficient'], 'electric coefficient').group(1)) == v['face_factor']
            and terms[0]['term'].startswith('electric: %d C_2(r) on the character chi_r' % v['face_factor']), 'electric term')
    require(terms[1]['coefficient'] == '-tau/%d' % v['mag_den'] and terms[1]['term'].startswith('magnetic: W = Re chi_fund(U)/dim fund'),
            'magnetic term')
    require(int(match(r'^(\d+) \(delta units\), per link$', terms[2]['coefficient'], 'box electric').group(1)) == v['link_factor'],
            'box electric term')
    require(terms[3]['coefficient'] == '-tau/%d' % v['mag_den'] and 'selected faces carry coefficient 0' in terms[3]['term'],
            'box magnetic term')
    v['hamiltonian_terms'] = terms
    require(p.get('model_is_finite_graph') is True, 'model_is_finite_graph must be true in parameters')
    flips = p['flip_sets']
    v['flip_sets_text'] = flips
    clauses = re.findall(r'\{\(p,([xyz])\): p_([xyz]) even\}', flips)
    require(len(clauses) == 4, 'flip-set clauses not parsed')
    axis = {'x': 0, 'y': 1, 'z': 2}
    e3 = clauses[:3]
    require(sorted(d for d, _ in e3) == ['x', 'y', 'z'], 'E_3 clauses')
    v['E3_spec'] = {axis[d]: axis[k] for d, k in e3}
    v['E2_spec'] = {axis[clauses[3][0]]: axis[clauses[3][1]]}
    require(re.search(r'E_2 = \{\(p,x\): p_y even\} on \[-N,N\]\^2, N=2,3,4, exactly one link per plaquette', flips) is not None,
            'E_2 statement')
    ns = re.findall(r'N=(\d+(?:,\d+)*)', flips)
    require(len(ns) == 2 and ns[0] == ns[1], 'box sizes for E_3 and E_2')
    v['flip_boxes'] = [int(x) for x in ns[0].split(',')]
    match(r'periodic tori with an odd side recorded with the even plaquettes at the seam', flips, 'tori clause')
    match(r'recording that E_3 is not invariant under odd coarse translations in z', flips, 'translation clause')
    ap = p['area_parity']
    v['area_parity_text'] = ap
    match(r'^for SU\(2\), kappa=0, every loop C of plaquette edges bounding a surface of A\(C\) plaquettes in the box: '
          r'omega_\{N,-tau\}\(W_C\) = \(-1\)\^\{A\(C\)\} omega_\{N,tau\}\(W_C\)', ap, 'area parity')
    match(r'BB2 whole-sequence convergence at each sign', ap, 'area parity limit')
    v['N_min'] = int(p['N_min'])
    for key in ('metric', 'weights', 'window', 'clock'):
        require(isinstance(p.get(key), str) and p[key], 'parameters field missing: ' + key)
    v['tau_corollary'] = Q(1, int(match(r'1/(\d+) for the SU\(2\) corollary', pre['tau']['value'], 'corollary tau').group(1)))
    v['signs'] = list(pre['tau']['signs_evaluated'])
    require(v['signs'] == ['+', '-'], 'both signs')
    v['template'] = pre['mandatory_sentence_template']
    v['gate_fields_required'] = dict(pre['gate_fields_required'])
    v['forbidden'] = list(pre['forbidden_phrasings'])
    br = pre['scaling_brackets_per_constant']
    v['brackets'] = {k: Q(int(match(r'ratio exactly (\d+)', br[k], 'bracket ' + k).group(1)))
                     for k in ('first_order_terms', 'obstruction_second_order_terms', 'su5_fourth_order_term', 'moments')}
    v['error_terms'] = list(pre['error_terms_itemized'])
    v['error_terms_rule'] = pre['error_terms_rule']
    v['tier_names'] = list(pre['tier_names_allowed'])
    m = match(r'names its route \((\w+) or (\w+), recorded in a (\w+) field', pre['tier_label_rule'], 'route rule')
    v['routes_allowed'] = [m.group(1), m.group(2)]
    v['route_field'] = m.group(3)
    v['sub_labels'] = list(pre['sub_labels_allowed'])
    v['target'] = pre['target']
    require(v['target']['comparator'] == '== and !=0', 'comparator read from the contract')
    v['reference_value'] = pre['observable']['reference_value_exact']
    require(v['reference_value'] == 'the free (tau=0) values computed in the same code path', 'reference value rule')
    v['model_id'] = pre['model_id']
    require(v['model_id'] == 'FG(one_plaquette_group_cells: ' + ','.join(v['groups']) + ')', 'model id group list')
    require([rat(x) for x in pre['selected_triple_alpha_units']] == [0, 0, 0], 'zero triple')
    v['controls'] = list(c['controls'])
    require(v['controls'] == list(pre['controls_required']['ids']) and len(set(v['controls'])) == len(v['controls']) == 22,
            'controls mirror')
    v['new_control_semantics'] = dict(c['new_control_semantics'])
    require(set(v['new_control_semantics']) <= set(v['controls']), 'new control semantics keys are controls')
    m = match(r'a plan route label \(([a-z0-9_, ]+)\)', v['new_control_semantics']['tier_mixing_rejected'], 'plan route labels')
    v['plan_route_labels'] = [x.strip() for x in m.group(1).split(',')]
    require(len(v['plan_route_labels']) == 6, 'six plan route labels')
    v['claim_exclusions'] = list(c['claim_exclusions'])
    v['prereg_exclusions'] = list(pre['claim_exclusions'])
    v['shared_premises'] = list(c['shared_premises'])
    require(len(req) == 8, 'eight required items')
    match(r'the exact nonzero fourth-order coefficient of omega\(W\) on H_FG\(SU\(5\)\), its first possible nonzero even-order '
          r'coefficient under the Z_5 grading', req[3], 'item 4 SU(5)')
    match(r'using that E\[W\^3\]=0 is equivalent to the vanishing of every cubic moment E\[chi\^a conj\(chi\)\^b\] with a\+b=3',
          req[1], 'item 2 cubic moments')
    v['required'] = req
    v['acceptance'] = c['acceptance']
    return v


# ---------------------------------------------------------------------------
# Admitted premises (pinned gate sha256s) and parsed reference values.
# ---------------------------------------------------------------------------
def load_gate(rel, loop):
    raw = read_input(rel)
    require(sha_bytes(raw) == GATE_SHA256[rel], 'admitted gate snapshot differs from its pinned sha256: ' + rel)
    g = json.loads(raw.decode('utf-8'))
    require(g.get('loop') == loop and g.get('verdict') == 'accepted_within_scope', 'gate identity ' + rel)
    return g


def premise_values():
    out = {}
    aw1 = load_gate(AW1_GATE, 'AW1')
    m = match(r'E=\{\(p,x\):p_y even\} u \{\(p,y\):p_z even\} u \{\(p,z\):p_x even\}', aw1['accepted'], 'AW1 flip set')
    axis = {'x': 0, 'y': 1, 'z': 2}
    out['aw1_E_spec'] = {axis[d]: axis[k] for d, k in re.findall(r'\(p,([xyz])\):p_([xyz]) even', m.group(0))}
    out['aw1_coefficient_den'] = int(match(r'omega_tau\(W\)=\+tau/(\d+)\+r\(tau\) under I1\.5', aw1['accepted'], 'AW1 coefficient').group(1))
    match(r'U_E H_N\(tau,kappa\) U_E\^\*=H_N\(-tau,-kappa\) in every open centered whole-star box', aw1['accepted'], 'AW1 identity')
    match(r'at kappa=0 omega_\{N,-tau\}\(W\)=-omega_\{N,tau\}\(W\)', aw1['accepted'], 'AW1 kappa=0')
    match(r'E\[W\]=E\[W\^3\]=0, E\[W\^2\]=1/4, E\[W\^4\]=1/8', aw1['accepted'], 'AW1 moments')
    out['aw1_moments'] = {1: Q(0), 2: Q(1, 4), 3: Q(0), 4: Q(1, 8)}
    aw2 = load_gate(AW2_GATE, 'AW2')
    match(r'sign\(omega_tau\(W\)\)=sign\(tau\)', aw2['accepted'], 'AW2 sign')
    ay2 = load_gate(AY2_GATE, 'AY2')
    require(ay2['gate_fields']['uniqueness_claimed'] is False, 'AY2 uniqueness flag')
    az1 = load_gate(AZ1_GATE, 'AZ1')
    out['su2_dictionary'] = match(r'tau=24 lambda/alpha=96/g\^4', az1['accepted'], 'AZ1 dictionary').group(0)
    match(r'AL1 dictionary alpha=g\^2/\(2a\)', az1['accepted'], 'AZ1 alpha')
    out['su2_dictionary_den'] = 96
    az2 = load_gate(AZ2_GATE, 'AZ2')
    require(az2['gate_fields'] == {'fg_coefficients_fitted': False, 'model_is_finite_graph': True, 'transfers_to_aq': False},
            'AZ2 finite-graph labels')
    bb2 = load_gate(BB2_GATE, 'BB2')
    acc = bb2['accepted']
    m = match(r"C'=(\d+)/(\d+) \(about", acc, "BB2 C'")
    out['bb2_Cprime'] = Q(int(m.group(1)), int(m.group(2)))
    m = match(r"c'_site=(\d+)/(\d+) \(about", acc, "BB2 c'_site")
    out['bb2_csite'] = Q(int(m.group(1)), int(m.group(2)))
    out['bb2_q'] = Q(1, int(match(r'q=1/(\d+)', acc, 'BB2 q').group(1)))
    match(r"<= c'_site \|Y\| e\^\{\|Y\|/10\^8\} q\^\{d_Y\} with d_Y=N-max_\{y in Y\}\|y\|_inf", acc, 'BB2 region form')
    match(r'both signs \|tau\|<=10\^-8', acc, 'BB2 signs')
    out['bb2_tau_cap'] = Q(1, 10 ** 8)
    gf = bb2['gate_fields']
    require(gf['whole_sequence_claimed'] is True and gf['state_convergence_claimed'] is True and gf['common_limit_claimed'] is True
            and gf['uniqueness_of_ground_state_claimed'] is False and gf['rate_in_a_claimed'] is False, 'BB2 gate fields')
    out['bb2_whole_sequence_scope'] = gf['whole_sequence_scope']
    out['bb2_sub_label'] = bb2.get('sub_label')
    require(out['bb2_sub_label'] == 'convergence_of_named_constructions', 'BB2 sub-label')
    text = read_input(AW1_F_REL).decode('utf-8')
    m = match(r'all (\d+) retained faces and all (\d+) plaquettes of the `N=2` box \((\d+) meet `E` once, (\d+) three times\)',
              text, 'AW1 forward N=2 counts')
    out['aw1_N2_counts'] = tuple(int(m.group(i)) for i in range(1, 5))
    text = read_input(AW1_R_REL).decode('utf-8')
    m = match(r'every plaquette of the fine box `\[-(\d+),(\d+)\]\^3`: ([\d,]+) plaquettes, ([\d,]+) meeting E once, ([\d,]+) '
              r'meeting it three times, and 0 meeting it evenly', text, 'AW1 reverse fine-box counts')
    out['aw1_fine_box'] = (int(m.group(1)), int(m.group(2))) + tuple(int(m.group(i).replace(',', '')) for i in (3, 4, 5))
    sel = read_input(SELECTION_REL).decode('utf-8')
    match(r'\(SU\(2\), SU\(3\), SU\(4\), SU\(5\), U\(1\), Z2, SO\(3\)\)', sel, 'selection group list')
    ba1 = json.loads(read_input(BA1_REL).decode('utf-8'))
    out['ba1_semantics'] = {k: ba1['new_control_semantics'][k] for k in
                            ('coherent_evidence_tampering', 'exact_arithmetic_admission', 'no_priority_or_continuum_claim',
                             'insufficient_verdict_retained', 'placeholder_span_rejected', 'negation_aware_phrase_scan')}
    json.loads(read_input(BB2_CONTRACT_REL).decode('utf-8'))
    out['gate_sha256'] = {rel: sha_bytes(read_input(rel)) for rel in sorted(GATE_SHA256)}
    return out


# ---------------------------------------------------------------------------
# Groups (forward route: characters).  Each group names its irreducible labels,
# the tensor product of an irrep with the Wilson representation F and with its
# conjugate, the Casimir in the frozen normalization and its centre data.
# A central element is recorded by its turn t: it acts on the irrep r by
# exp(2 pi i t grade(r)), so on F by exp(2 pi i t).
# ---------------------------------------------------------------------------
class Group:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def perm_sign(perm):
    inv = sum(1 for i in range(len(perm)) for j in range(i + 1, len(perm)) if perm[i] > perm[j])
    return -1 if inv % 2 else 1


def su_n_pieri(N):
    """SU(N) irreps as partitions (lambda_1..lambda_{N-1}), lambda_N=0 (full columns removed).
    F x V_lambda: add one box (Pieri).  Fbar x V_lambda: remove one box as GL(N) weights (dual Pieri)."""
    def full(l):
        return tuple(l) + (0,)

    def norm(L):
        m = L[-1]
        return tuple(x - m for x in L[:-1])

    def tensor_F(l):
        L = full(l)
        out = {}
        for i in range(N):
            M = list(L)
            M[i] += 1
            if i == 0 or M[i] <= M[i - 1]:
                k = norm(M)
                out[k] = out.get(k, 0) + 1
        return out

    def tensor_Fbar(l):
        L = full(l)
        out = {}
        for i in range(N):
            M = list(L)
            M[i] -= 1
            if i == N - 1 or M[i] >= M[i + 1]:
                k = norm(M)
                out[k] = out.get(k, 0) + 1
        return out

    def casimir(l):
        L = full(l)
        n = sum(L)
        return Q(1, 2) * (sum(L[i] * (L[i] + N + 1 - 2 * (i + 1)) for i in range(N)) - Q(n * n, N))

    def dim(l):
        L = full(l)
        num, den = 1, 1
        for i in range(N):
            for j in range(i + 1, N):
                num *= L[i] - L[j] + j - i
                den *= j - i
        require(num % den == 0, 'Weyl dimension not integral')
        return num // den
    F = tuple([1] + [0] * (N - 2))
    Fbar = tuple([1] * (N - 1))
    reason = ('centre Z_%d = {exp(2 pi i k/%d) I}; ' % (N, N)
              + ('k=%d gives -I, central with rho_F(-I)=-I and det(-I)=(-1)^%d=1' % (N // 2, N) if N % 2 == 0 else
                 'it acts on the fundamental by %s roots of unity, none equal to -1; -I is not in SU(%d) since det(-I)=(-1)^%d=-1'
                 % ({3: 'cube', 5: 'fifth'}.get(N, 'N-th'), N, N)))
    return Group(name='SU(%d)' % N, kind='SU(N)', N=N, triv=(0,) * (N - 1), F=F, Fbar=Fbar, d=N, tensor_F=tensor_F,
                 tensor_Fbar=tensor_Fbar, casimir=casimir, dim=dim, grade=lambda l: sum(l),
                 centre=[Q(k, N) for k in range(N)], det_minus_identity=(-1) ** N, matrix_dim=N,
                 route_detail='Pieri rule for the fundamental and its conjugate (dual Pieri), Peter-Weyl orthogonality',
                 centre_reason=reason, casimir_rule='C_2(lambda)=(1/2)[sum_i lambda_i(lambda_i+N+1-2i)-|lambda|^2/N]',
                 label_rule='partition with lambda_N=0 (full columns removed)')


def su2_clebsch_gordan():
    """SU(2) irreps labelled by tj=2j; j x 1/2 = (j-1/2) + (j+1/2) (Clebsch-Gordan)."""
    def tensor_F(tj):
        return {1: 1} if tj == 0 else {tj - 1: 1, tj + 1: 1}
    return Group(name='SU(2)', kind='SU(2)', N=2, triv=0, F=1, Fbar=1, d=2, tensor_F=tensor_F, tensor_Fbar=tensor_F,
                 casimir=lambda tj: Q(tj * (tj + 2), 4), dim=lambda tj: tj + 1, grade=lambda tj: tj,
                 centre=[Q(0), Q(1, 2)], det_minus_identity=1, matrix_dim=2,
                 route_detail='Clebsch-Gordan series (spin j x spin 1/2), Peter-Weyl orthogonality',
                 centre_reason='centre {I,-I}; z=-I is central with rho_F(-I)=-I and det(-I)=(-1)^2=1',
                 casimir_rule='C_2(j)=j(j+1)', label_rule='tj=2j')


def u1_charges():
    return Group(name='U(1)', kind='U(1)', N=None, triv=0, F=1, Fbar=-1, d=1, tensor_F=lambda n: {n + 1: 1},
                 tensor_Fbar=lambda n: {n - 1: 1}, casimir=lambda n: Q(n * n), dim=lambda n: 1, grade=lambda n: n,
                 centre=[Q(0), Q(1, 2)], det_minus_identity=None, matrix_dim=1,
                 route_detail='charge counting (chi_1 chi_n = chi_{n+1}), orthogonality of charges',
                 centre_reason='U(1) is abelian, so every element is central; z=exp(i pi) has charge-1 character -1',
                 casimir_rule='C_2(n)=n^2', label_rule='charge n')


def z2_signs():
    return Group(name='Z2', kind='Z2', N=None, triv=0, F=1, Fbar=1, d=1, tensor_F=lambda r: {(r + 1) % 2: 1},
                 tensor_Fbar=lambda r: {(r + 1) % 2: 1}, casimir=lambda r: Q(r), dim=lambda r: 1, grade=lambda r: r,
                 centre=[Q(0), Q(1, 2)], det_minus_identity=None, matrix_dim=1,
                 route_detail='direct summation over the two elements (sign x sign = trivial)',
                 centre_reason='Z2 is abelian; z=the nontrivial element has sign character -1',
                 casimir_rule='C_2(even)=0, C_2(odd)=1 (frozen Z2 normalization)', label_rule='0 even, 1 odd')


def so3_vector():
    def tensor_F(l):
        return {1: 1} if l == 0 else {l - 1: 1, l: 1, l + 1: 1}
    return Group(name='SO(3)', kind='SO(3)', N=None, triv=0, F=1, Fbar=1, d=3, tensor_F=tensor_F, tensor_Fbar=tensor_F,
                 casimir=lambda l: Q(l * (l + 1)), dim=lambda l: 2 * l + 1, grade=lambda l: 0,
                 centre=[Q(0)], det_minus_identity=-1, matrix_dim=3,
                 route_detail='Clebsch-Gordan series (l x 1), Peter-Weyl orthogonality',
                 centre_reason='the centre of SO(3) is trivial; -I is not in SO(3) since det(-I)=(-1)^3=-1',
                 casimir_rule='C_2(l)=l(l+1)', label_rule='integer l')


def build_groups():
    return {'SU(2)': su2_clebsch_gordan(), 'SU(3)': su_n_pieri(3), 'SU(4)': su_n_pieri(4), 'SU(5)': su_n_pieri(5),
            'U(1)': u1_charges(), 'Z2': z2_signs(), 'SO(3)': so3_vector()}


def key_str(k):
    return ','.join(str(x) for x in k) if isinstance(k, tuple) else str(k)


# ---------------------------------------------------------------------------
# Character algebra: W = (chi_F + chi_Fbar)/(2 dim F) acts on the orthonormal
# character basis by tensor-product multiplicities (Peter-Weyl orthogonality).
# ---------------------------------------------------------------------------
def apply_W(G, vec):
    c = Q(1, 2 * G.d)
    out = {}
    for r, a in vec.items():
        for fn in (G.tensor_F, G.tensor_Fbar):
            for t, m in fn(r).items():
                out[t] = out.get(t, 0) + c * m * a
    return {k: x for k, x in out.items() if x != 0}


def ip(u, v):
    return sum((u[k] * v[k] for k in u if k in v), Q(0))


def moments_characters(G, kmax):
    vec = {G.triv: Q(1)}
    out = []
    for _ in range(kmax):
        vec = apply_W(G, vec)
        out.append(vec.get(G.triv, Q(0)))
    return out


def chi_moment_tensor(G, a, b):
    """E[chi^a conj(chi)^b] = multiplicity of the trivial irrep in F^{x a} x Fbar^{x b} (iterated tensoring)."""
    vec = {G.triv: 1}
    for fn, n in ((G.tensor_F, a), (G.tensor_Fbar, b)):
        for _ in range(n):
            new = {}
            for r, m in vec.items():
                for t, k in fn(r).items():
                    new[t] = new.get(t, 0) + m * k
            vec = new
    return vec.get(G.triv, 0)


def partitions(n, maxlen):
    def rec(n, maxpart, length):
        if n == 0:
            yield ()
            return
        if length == 0:
            return
        for first in range(min(n, maxpart), 0, -1):
            for rest in rec(n - first, first, length - 1):
                yield (first,) + rest
    return list(rec(n, n, maxlen))


def hook_count(lam):
    """Number of standard Young tableaux of shape lam (hook-length formula)."""
    n = sum(lam)
    conj = [sum(1 for x in lam if x > j) for j in range(lam[0])] if lam else []
    prod = 1
    for i, row in enumerate(lam):
        for j in range(row):
            prod *= (row - j - 1) + (conj[j] - i - 1) + 1
    require(factorial(n) % prod == 0, 'hook formula not integral')
    return factorial(n) // prod


def catalan(m):
    return comb(2 * m, m) // (m + 1)


def chi_moment_closed(G, a, b):
    """Second character sub-route: closed-form counts (Schur-Weyl with hook lengths for SU(N); charge balance for U(1);
    parity for Z2; SO(3) through the covering SU(2)->SO(3), chi_1=chi_{1/2}^2-1 and Catalan numbers)."""
    if G.kind in ('SU(N)', 'SU(2)'):
        N = G.N
        total = 0
        for lam in partitions(a, N):
            for mu in partitions(b, N):
                L = list(lam) + [0] * (N - len(lam))
                M = list(mu) + [0] * (N - len(mu))
                diff = [L[i] - M[i] for i in range(N)]
                if all(x == diff[0] for x in diff):
                    total += hook_count(lam) * hook_count(mu)
        return total
    if G.kind == 'U(1)':
        return 1 if a == b else 0
    if G.kind == 'Z2':
        return 1 if (a + b) % 2 == 0 else 0
    if G.kind == 'SO(3)':
        k = a + b
        return sum(comb(k, i) * (-1) ** (k - i) * catalan(i) for i in range(k + 1))
    raise AdmissionError('unknown group kind')


def moment_from_chi_table(G, table, k):
    """E[W^k]=(2d)^-k sum_a C(k,a) E[chi^a conj(chi)^(k-a)]."""
    return sum((comb(k, a) * table[(a, k - a)] for a in range(k + 1)), 0) * Q(1, (2 * G.d) ** k)


# ---------------------------------------------------------------------------
# Forward-internal cross-check by Weyl integration (constant-term extraction on
# the maximal torus; U(1) by direct integration, Z2 by direct summation).  It is
# labelled weyl_integration, it is not the reverse producer's route and it is
# never the admission value; it exercises the two-route comparison on data.
# ---------------------------------------------------------------------------
def laurent_mul(p, q):
    out = {}
    for e1, c1 in p.items():
        for e2, c2 in q.items():
            e = tuple(x + y for x, y in zip(e1, e2))
            out[e] = out.get(e, 0) + c1 * c2
    return {k: x for k, x in out.items() if x != 0}


def weyl_chi_table(G, kmax):
    table = {}
    if G.kind in ('SU(N)', 'SU(2)'):
        N = G.N
        delta = [N - 1 - i for i in range(N)]
        vd = {}
        for perm in itertools.permutations(range(N)):
            e = tuple(delta[perm[i]] for i in range(N))
            vd[e] = vd.get(e, 0) + perm_sign(perm)
        vdbar = {tuple(-x for x in e): c for e, c in vd.items()}
        dens = laurent_mul(vd, vdbar)
        red = {}
        for e, c in dens.items():
            key = tuple(x - e[-1] for x in e[:-1])
            red[key] = red.get(key, 0) + c
        one = {(0,) * N: 1}
        z = {tuple(1 if j == i else 0 for j in range(N)): 1 for i in range(N)}
        zi = {tuple(-1 if j == i else 0 for j in range(N)): 1 for i in range(N)}
        pz, pzi = [one], [one]
        for _ in range(kmax):
            pz.append(laurent_mul(pz[-1], z))
            pzi.append(laurent_mul(pzi[-1], zi))
        for a in range(kmax + 1):
            for b in range(kmax + 1 - a):
                f = laurent_mul(pz[a], pzi[b])
                ct = sum(c * red.get(tuple(-(x - e[-1]) for x in e[:-1]), 0) for e, c in f.items())
                require(ct % factorial(N) == 0, 'Weyl constant term not divisible by |W|')
                table[(a, b)] = ct // factorial(N)
        return table
    if G.kind == 'SO(3)':
        dens = {(0,): 2, (1,): -1, (-1,): -1}
        chi = {(-1,): 1, (0,): 1, (1,): 1}
        f = {(0,): 1}
        pows = [f]
        for _ in range(kmax):
            pows.append(laurent_mul(pows[-1], chi))
        for a in range(kmax + 1):
            for b in range(kmax + 1 - a):
                ct = laurent_mul(pows[a + b], dens).get((0,), 0)
                require(ct % 2 == 0, 'SO(3) constant term parity')
                table[(a, b)] = ct // 2
        return table
    if G.kind == 'U(1)':
        for a in range(kmax + 1):
            for b in range(kmax + 1 - a):
                table[(a, b)] = 1 if a - b == 0 else 0      # (1/2pi) int exp(i(a-b)theta) dtheta
        return table
    if G.kind == 'Z2':
        for a in range(kmax + 1):
            for b in range(kmax + 1 - a):
                table[(a, b)] = Q(sum(x ** (a + b) for x in (1, -1)), 2)
                require(table[(a, b)].denominator == 1, 'Z2 summation')
                table[(a, b)] = int(table[(a, b)])
        return table
    raise AdmissionError('unknown group kind')


def weyl_moment_u1_direct(k):
    """E[cos^k] by direct integration: 2^-k C(k,k/2) for even k."""
    return Q(comb(k, k // 2), 2 ** k) if k % 2 == 0 else Q(0)


# ---------------------------------------------------------------------------
# Exact Rayleigh-Schroedinger on H_FG(G) = face_factor C_2 - (tau/mag_den) W in
# the character basis (intermediate normalization, simple ground Omega_0).
# ---------------------------------------------------------------------------
def reachable(G, depth):
    seen = {G.triv}
    frontier = {G.triv}
    for _ in range(depth):
        new = set()
        for r in frontier:
            new |= set(apply_W(G, {r: Q(1)}))
        frontier = new - seen
        seen |= new
    return seen


def rs_series(G, order, face_factor, mag_den, depth=None):
    triv = G.triv
    allowed = None if depth is None else reachable(G, depth)

    def restrict(v):
        return v if allowed is None else {k: x for k, x in v.items() if k in allowed}

    def V1(v):
        return {k: -x / mag_den for k, x in restrict(apply_W(G, v)).items()}

    def resolvent(v):
        return {k: x / (face_factor * G.casimir(k)) for k, x in v.items() if k != triv and x != 0}
    psi = [{triv: Q(1)}]
    E = [Q(0)]
    for m in range(1, order + 1):
        E.append(V1(psi[m - 1]).get(triv, Q(0)))
        rhs = {k: -x for k, x in V1(psi[m - 1]).items()}
        for i in range(1, m):
            for k, x in psi[m - i].items():
                rhs[k] = rhs.get(k, 0) + E[i] * x
        psi.append(resolvent(rhs))

    def series(obs):
        num = [sum((ip(psi[i], obs(psi[m - i])) for i in range(m + 1)), Q(0)) for m in range(order + 1)]
        den = [sum((ip(psi[i], psi[m - i]) for i in range(m + 1)), Q(0)) for m in range(order + 1)]
        ser = []
        for m in range(order + 1):
            ser.append((num[m] - sum((ser[i] * den[m - i] for i in range(m)), Q(0))) / den[0])
        return ser
    obs_W = lambda v: restrict(apply_W(G, v))
    obs_W2 = lambda v: restrict(apply_W(G, restrict(apply_W(G, v))))
    obs_C = lambda v: {k: G.casimir(k) * x for k, x in v.items()}
    return {'psi': psi, 'E': E, 'W': series(obs_W), 'W2': series(obs_W2), 'C2': series(obs_C), 'V1': V1}


# ---------------------------------------------------------------------------
# Fine-lattice geometry (I1): coarse 24-link factors, face classes, boxes.
# ---------------------------------------------------------------------------
UNIT = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIENTS = ((0, 1), (0, 2), (1, 2))
ORIENT_NAME = {'xy': (0, 1), 'xz': (0, 2), 'yz': (1, 2)}
OFFSET = {'0': (0, 0, 0), 'e_x': (1, 0, 0), 'e_y': (0, 1, 0), 'e_z': (0, 0, 1)}
S_STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
ORIGIN = (0, 0, 0)
WILSON = ((0, 0, 0), (0, 2))      # the AW1 original xz face W at the fine origin


def add(p, q):
    return tuple(a + b for a, b in zip(p, q))


def sub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def scale(p, k):
    return tuple(k * a for a in p)


def owner(p):
    return (p[0] // 4, p[1] // 2, p[2])


def face_links(face):
    """I1.4: face at p in directions a<c has links (p,a),(p+e_a,c),(p+e_c,a),(p,c)."""
    p, (a, c) = face
    return ((p, a), (add(p, UNIT[a]), c), (add(p, UNIT[c]), a), (p, c))


def links_of(face):
    return frozenset(face_links(face))


def parse_i1_table():
    text = read_input(I1_REL).decode('utf-8')
    rows = re.findall(r'^\| (xy|xz|yz): r=([0-9,]+); s=([0-9,]+) \| (\d+) \| `\{([^}]*)\}` \| (selected|omitted) \|$', text, re.M)
    require(len(rows) == 8, 'I1 table rows')
    table = []
    for orient, rs_, ss_, count, supp, role in rows:
        r_vals = tuple(int(x) for x in rs_.split(','))
        s_vals = tuple(int(x) for x in ss_.split(','))
        require(len(r_vals) * len(s_vals) == int(count), 'I1 row count')
        table.append({'orientation': orient, 'r': r_vals, 's': s_vals,
                      'support': frozenset(OFFSET[t.strip()] for t in supp.split(',')), 'role': role})
    return table


def expand_classes(table, role):
    return [(row['orientation'], r, q, row['support']) for row in table if row['role'] == role for r in row['r'] for q in row['s']]


def class_face(anchor, cls):
    orient, r, q, _ = cls
    return ((4 * anchor[0] + r, 2 * anchor[1] + q, anchor[2]), ORIENT_NAME[orient])


def support_of(face):
    return frozenset(owner(l[0]) for l in face_links(face))


def owned_links(b):
    return [((4 * b[0] + r, 2 * b[1] + q, b[2]), d) for r in range(4) for q in range(2) for d in range(3)]


def coarse_cube(N):
    rng = range(-N, N + 1)
    return [(x, y, z) for x in rng for y in rng for z in rng]


def box_links(N):
    return frozenset(l for b in coarse_cube(N) for l in owned_links(b))


def box_plaquettes(links):
    tails = sorted({l[0] for l in links})
    return [(p, o) for p in tails for o in ORIENTS if links_of((p, o)) <= links]


def retained_faces(N, classes):
    cube = set(coarse_cube(N))
    anchors = [b for b in coarse_cube(N) if all(add(b, d) in cube for d in S_STAR)]
    return anchors, [class_face(b, cls) for b in anchors for cls in classes]


def make_in_E(spec, removed=frozenset(), added=frozenset()):
    def in_E(link):
        if link in removed:
            return False
        if link in added:
            return True
        p, d = link
        return d in spec and p[spec[d]] % 2 == 0
    return in_E


def flip_count(face, in_E):
    return sum(1 for l in face_links(face) if in_E(l))


def validate_odd(faces, in_E, label):
    for f in faces:
        require(flip_count(f, in_E) % 2 == 1, 'even intersection with the flip set (' + label + ') at ' + repr(f))
    return True


def histogram(faces, in_E):
    h = {}
    for f in faces:
        k = flip_count(f, in_E)
        h[k] = h.get(k, 0) + 1
    return {str(k): v for k, v in sorted(h.items())}


# Two-dimensional lattice: links (p,d) with p in Z^2, d in {0,1}; plaquette at p has links
# (p,0),(p+e_x,1),(p+e_y,0),(p,1).
def plaquette_links_2d(p):
    return ((p, 0), ((p[0] + 1, p[1]), 1), ((p[0], p[1] + 1), 0), (p, 1))


def validate_exactly_one_2d(N, in_E2):
    for x in range(-N, N):
        for y in range(-N, N):
            require(sum(1 for l in plaquette_links_2d((x, y)) if in_E2(l)) == 1, 'E_2 does not meet a plaquette exactly once')
    return (2 * N) ** 2


def torus_counts_3d(sides, spec):
    """|f cap E_3| on the periodic torus with the given sides; returns (plaquettes, even plaquettes)."""
    in_E = make_in_E(spec)
    total = even = 0
    for base in itertools.product(*(range(L) for L in sides)):
        for o in ORIENTS:
            lk = [(tuple(x % L for x, L in zip(p, sides)), d) for p, d in face_links((base, o))]
            total += 1
            if sum(1 for l in lk if in_E(l)) % 2 == 0:
                even += 1
    return total, even


def torus_counts_2d(sides, spec):
    in_E = make_in_E(spec)
    total = even = 0
    for x in range(sides[0]):
        for y in range(sides[1]):
            lk = [((p[0] % sides[0], p[1] % sides[1]), d) for p, d in plaquette_links_2d((x, y))]
            total += 1
            if sum(1 for l in lk if in_E(l)) % 2 == 0:
                even += 1
    return total, even


def gf2_flip_set_exists(sides):
    """Is there any Z_2 1-cochain E with coboundary 1 on every plaquette of the periodic torus?  (GF(2) elimination.)"""
    dim = len(sides)
    idx = {}
    for base in itertools.product(*(range(L) for L in sides)):
        for d in range(dim):
            idx[(base, d)] = len(idx)
    orients = [(a, c) for a in range(dim) for c in range(a + 1, dim)]
    rows = []
    for base in itertools.product(*(range(L) for L in sides)):
        for a, c in orients:
            ea = tuple(1 if i == a else 0 for i in range(dim))
            ec = tuple(1 if i == c else 0 for i in range(dim))
            pts = [(base, a), (add(base, ea), c), (add(base, ec), a), (base, c)]
            mask = 0
            for p, d in pts:
                mask ^= 1 << idx[(tuple(x % L for x, L in zip(p, sides)), d)]
            rows.append(mask | (1 << len(idx)))
    nvar = len(idx)
    pivots = {}
    for row in rows:
        r = row
        for bit in sorted(pivots, reverse=True):
            if (r >> bit) & 1:
                r ^= pivots[bit]
        low = r & ((1 << nvar) - 1)
        if low == 0:
            if r >> nvar:
                return False
            continue
        top = low.bit_length() - 1
        for bit in list(pivots):
            if (pivots[bit] >> top) & 1:
                pivots[bit] ^= r
        pivots[top] = r
    return True


# ---------------------------------------------------------------------------
# Loops, spanning surfaces and closed surfaces (SU(2) area parity).
# ---------------------------------------------------------------------------
def canon(face):
    p, (a, c) = face
    return (p, (min(a, c), max(a, c)))


def loop_links(verts):
    """Ordered traversal of a closed vertex path: list of (link, +1 forward / -1 backward)."""
    out = []
    for u, v in zip(verts, verts[1:]):
        dlt = sub(v, u)
        require(sum(abs(x) for x in dlt) == 1, 'loop steps must be unit steps')
        d = [i for i in range(3) if dlt[i] != 0][0]
        out.append(((u, d), 1) if dlt[d] == 1 else ((v, d), -1))
    require(verts[0] == verts[-1], 'loop must close')
    return out


def chain_mod2(links):
    out = {}
    for l in links:
        out[l] = out.get(l, 0) ^ 1
    return frozenset(l for l, x in out.items() if x)


def surface_boundary(faces):
    return chain_mod2([l for f in faces for l in face_links(f)])


def rectangle(p0, a, c, R, T):
    verts = [p0]
    cur = p0
    for step, n in ((UNIT[a], R), (UNIT[c], T), (scale(UNIT[a], -1), R), (scale(UNIT[c], -1), T)):
        for _ in range(n):
            cur = add(cur, step)
            verts.append(cur)
    o = (min(a, c), max(a, c))
    flat = [(add(add(p0, scale(UNIT[a], i)), scale(UNIT[c], j)), o) for i in range(R) for j in range(T)]
    b = 3 - a - c
    cap = [(add(add(add(p0, UNIT[b]), scale(UNIT[a], i)), scale(UNIT[c], j)), o) for i in range(R) for j in range(T)]
    for i in range(R):
        for off in (0, T):
            cap.append(canon((add(add(p0, scale(UNIT[a], i)), scale(UNIT[c], off)), (a, b))))
    for j in range(T):
        for off in (0, R):
            cap.append(canon((add(add(p0, scale(UNIT[c], j)), scale(UNIT[a], off)), (c, b))))
    return verts, flat, cap


def cube_faces(q):
    """The six plaquettes of the unit cube with lowest corner q."""
    out = []
    for a, c in ORIENTS:
        b = 3 - a - c
        out.append((q, (a, c)))
        out.append((add(q, UNIT[b]), (a, c)))
    return out


def closed_surface_of_cubes(cubes):
    cnt = {}
    for q in cubes:
        for f in cube_faces(q):
            cnt[f] = cnt.get(f, 0) ^ 1
    return [f for f, x in cnt.items() if x]


# Exact rational SU(2) elements (unit quaternions a+bi+cj+dk with rational entries).
RATIONAL_QUATERNIONS = [(Q(1, 3), Q(2, 3), Q(2, 3), Q(0)), (Q(3, 5), Q(0), Q(4, 5), Q(0)), (Q(2, 7), Q(3, 7), Q(0), Q(6, 7)),
                        (Q(1, 2), Q(-1, 2), Q(1, 2), Q(1, 2)), (Q(9, 11), Q(2, 11), Q(0), Q(-6, 11)),
                        (Q(0), Q(1, 3), Q(-2, 3), Q(2, 3)), (Q(-2, 3), Q(2, 3), Q(1, 3), Q(0)), (Q(5, 13), Q(0), Q(0), Q(12, 13))]


def quat_mul(p, q):
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    return (a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2, a1 * b2 + b1 * a2 + c1 * d2 - d1 * c2,
            a1 * c2 - b1 * d2 + c1 * a2 + d1 * b2, a1 * d2 + b1 * c2 - c1 * b2 + d1 * a2)


def quat_inv(p):
    return (p[0], -p[1], -p[2], -p[3])


def quat_link(link):
    p, d = link
    return RATIONAL_QUATERNIONS[(5 * p[0] + 3 * p[1] + 7 * p[2] + 2 * d + 11) % len(RATIONAL_QUATERNIONS)]


def quat_vertex(p):
    return RATIONAL_QUATERNIONS[(3 * p[0] + 2 * p[1] + 5 * p[2] + 1) % len(RATIONAL_QUATERNIONS)]


def wilson_loop_su2(traversal, flip=None, gauge=None):
    """(1/2)Tr of the ordered holonomy = real part of the quaternion product."""
    h = (Q(1), Q(0), Q(0), Q(0))
    for (p, d), sgn in traversal:
        u = quat_link((p, d))
        require(sum(x * x for x in u) == 1, 'rational unit quaternion')
        if flip is not None and flip((p, d)):
            u = tuple(-x for x in u)
        if gauge is not None:
            u = quat_mul(quat_mul(gauge(p), u), quat_inv(gauge(add(p, UNIT[d]))))
        h = quat_mul(h, u if sgn == 1 else quat_inv(u))
    return h[0]


# Exact rational fixtures for the other flip groups: SU(4) signed permutation matrices of determinant 1
# (central z=-I), U(1) rational points of the unit circle (z=-1), Z2 signs (z=-1).
def signed_perms_det1(n):
    out = []
    for perm in itertools.permutations(range(n)):
        for signs in itertools.product((1, -1), repeat=n):
            det = perm_sign(perm)
            for x in signs:
                det *= x
            if det == 1:
                out.append(tuple(tuple(signs[i] if j == perm[i] else 0 for j in range(n)) for i in range(n)))
    return out


def mat_mul(A, B):
    n = len(A)
    return tuple(tuple(sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)) for i in range(n))


def mat_T(A):
    n = len(A)
    return tuple(tuple(A[j][i] for j in range(n)) for i in range(n))


def mat_neg(A):
    return tuple(tuple(-x for x in row) for row in A)


def mat_det(A):
    n = len(A)
    tot = 0
    for perm in itertools.permutations(range(n)):
        t = perm_sign(perm)
        for i in range(n):
            t *= A[i][perm[i]]
        tot += t
    return tot


CIRCLE = [(Q(3, 5), Q(4, 5)), (Q(5, 13), Q(-12, 13)), (Q(-8, 17), Q(15, 17)), (Q(7, 25), Q(24, 25)), (Q(-20, 29), Q(-21, 29)),
          (Q(1), Q(0)), (Q(0), Q(1)), (Q(-12, 37), Q(35, 37))]


def cmul(p, q):
    return (p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0])


def cconj(p):
    return (p[0], -p[1])


def group_face_value(kind, face, flip=None, gauge=None, elems=None):
    """W_f=Re chi_F(U_f)/dim F for a rational configuration; U_f=U1 U2 U3^-1 U4^-1 (I1.4 order)."""
    l1, l2, l3, l4 = face_links(face)

    def elem(link):
        p, d = link
        i = (5 * p[0] + 3 * p[1] + 7 * p[2] + 2 * d + 11) % len(elems)
        u = elems[i]
        neg = flip is not None and flip(link)
        if kind == 'SU(4)':
            u = mat_neg(u) if neg else u
            if gauge is not None:
                u = mat_mul(mat_mul(gauge(p), u), mat_T(gauge(add(p, UNIT[d]))))
            return u
        if kind == 'U(1)':
            u = (-u[0], -u[1]) if neg else u
            if gauge is not None:
                u = cmul(cmul(gauge(p), u), cconj(gauge(add(p, UNIT[d]))))
            return u
        if kind == 'Z2':
            u = -u if neg else u
            if gauge is not None:
                u = gauge(p) * u * gauge(add(p, UNIT[d]))
            return u
        raise AdmissionError('fixture kind')
    u1, u2, u3, u4 = (elem(l) for l in (l1, l2, l3, l4))
    if kind == 'SU(4)':
        h = mat_mul(mat_mul(mat_mul(u1, u2), mat_T(u3)), mat_T(u4))
        return Q(sum(h[i][i] for i in range(4)), 4)
    if kind == 'U(1)':
        h = cmul(cmul(cmul(u1, u2), cconj(u3)), cconj(u4))
        return h[0]
    return Q(u1 * u2 * u3 * u4)


# ---------------------------------------------------------------------------
# Text controls (the Round33 phrase-scan rule and the freezer placeholder rule,
# re-implemented here as infrastructure; the round list is copied from
# research/round33/tools/phrase_scan.py).
# ---------------------------------------------------------------------------
ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'pre' + 'dicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state', 'uniquely determines the ground state',
    'the thermodynamic limit', 'correlation length',
]
NEGATION = re.compile(r"\b(not|never|no|nor|neither|without|excludes?|excluded|exclusion|forbidden|"
                      r"cannot|does not|is not|are not|nothing|none)\b", re.I)


def normalize_ws(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def split_clauses(text):
    return [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', text) if c.strip()]


def affirmative_hits(text, forbidden, template):
    body = normalize_ws(text)
    if template:
        body = body.replace(normalize_ws(template), ' ')
    hits = []
    for clause in split_clauses(body):
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I) and not NEGATION.search(clause):
                hits.append([phrase, clause[:160]])
    return hits


def placeholder_spans(text):
    return [m.group(0) for m in re.finditer(r'<([^<>\n]*)>', text) if re.search(r'\s|\||e\.g\.', m.group(1))]


def validate_text(text, forbidden, template, label):
    require(not placeholder_spans(text), 'placeholder span in ' + label)
    require(not affirmative_hits(text, forbidden, template), 'affirmative forbidden phrasing in ' + label)
    return True


# ===========================================================================
def compute(check_sha):
    c, contract_digest = load_contract()
    V = contract_values(c)
    P = premise_values()
    GR = build_groups()
    groups = V['groups']
    ff, md, lf = V['face_factor'], V['mag_den'], V['link_factor']
    KMAX = 5
    ORDER = 5

    # -------------------- contract and premise binding --------------------
    check('contract_binding',
          V['link_factor'] == 8 and ff == 32 and md == 3 and V['z2_C_odd'] == 1 and V['z2_C_even'] == 0 and V['z2_CF'] == 1
          and V['so3_CF'] == 2 and V['su2_check_den'] == P['aw1_coefficient_den'] and V['routes_allowed'] == [ROUTE, CROSS_ROUTE]
          and V['route_field'] == 'route_of_computation' and V['tier_names'] == ['exact_first_order']
          and sorted(V['sub_labels']) == ['obstruction_recorded', 'transfer_to_named_model'] and V['N_min'] == 2
          and V['flip_boxes'] == [2, 3, 4] and V['E3_spec'] == P['aw1_E_spec'],
          contract_sha256=contract_digest, check_py_sha256_recorded_before_evaluation=check_sha,
          groups_read_from_contract=groups, convention_factors_read_from_contract={
              'per_link_electric': str(lf), 'face_energy_factor': str(ff), 'magnetic_denominator': str(md),
              'Z2_C2_even_odd': [s(V['z2_C_even']), s(V['z2_C_odd'])], 'SO3_C_F': s(V['so3_CF']), 'U1_charge': V['u1_charge'],
              'rejected_Z2_link_term_on_odd': s(V['z2_rejected_link_odd']), 'SU2_convention_check_denominator': V['su2_check_den']},
          flip_sets_read_from_contract={'E_3': {'xyz'[d]: 'p_' + 'xyz'[k] for d, k in sorted(V['E3_spec'].items())},
                                        'E_2': {'xyz'[d]: 'p_' + 'xyz'[k] for d, k in sorted(V['E2_spec'].items())},
                                        'boxes_N': V['flip_boxes']},
          target_read_from_contract={'quantity': V['target']['quantity'], 'comparator': V['target']['comparator']},
          reference_read_from_contract=V['reference_value'], corollary_tau_read_from_contract=s(V['tau_corollary']),
          controls_equal_preregistration_mirror=True, E3_equals_admitted_AW1_set=True)
    check('admitted_gate_binding',
          P['aw1_coefficient_den'] == 144 and P['bb2_q'] == Q(1, 64) and P['bb2_Cprime'] > 0 and P['bb2_csite'] > 0
          and P['aw1_N2_counts'] == (1344, 2335, 1082, 1253),
          admitted_gate_sha256=P['gate_sha256'], pinned_in_check_py=True,
          read={'AW1': 'flip set E, omega_tau(W)=+tau/144 (SU(2) convention check), identity H(tau,kappa) to H(-tau,-kappa), kappa=0 oddness, SU(2) moments',
                'AW2': 'sign(omega_tau(W))=sign(tau) (SU(2) only; not used for other groups)',
                'AY2': 'uniqueness_claimed false (named constructions)',
                'AZ1': 'SU(2) dictionary ' + P['su2_dictionary'] + ' (read only to reject its transfer)',
                'AZ2': 'finite-graph labels model_is_finite_graph true, transfers_to_aq false',
                'BB2': "C'=%s, c'_site=%s, q=%s, region form, whole-sequence convergence at each sign" % (s(P['bb2_Cprime']), s(P['bb2_csite']), s(P['bb2_q']))},
          bb2_whole_sequence_scope=P['bb2_whole_sequence_scope'])

    # -------------------- character rules --------------------
    CF = {}
    CF_rule = {}
    for g in groups:
        G = GR[g]
        if G.kind in ('SU(N)', 'SU(2)'):
            CF_rule[g] = Q(G.N * G.N - 1, 2 * G.N)
        elif G.kind == 'U(1)':
            CF_rule[g] = Q(V['u1_charge'] ** 2)
        elif G.kind == 'Z2':
            CF_rule[g] = V['z2_CF']
        else:
            CF_rule[g] = V['so3_CF']
        CF[g] = G.casimir(G.F)
    reach = {g: sorted(reachable(GR[g], 6), key=key_str) for g in groups}

    def dims_consistent(G, rset, tensor=None):
        tf = tensor or G.tensor_F
        for r in rset:
            for fn in (tf, G.tensor_Fbar):
                require(sum(m * G.dim(t) for t, m in fn(r).items()) == G.d * G.dim(r), 'tensor dimension count fails at ' + repr(r))
        return True
    cas_min = {g: min(GR[g].casimir(r) for r in reach[g] if r != GR[g].triv) for g in groups}
    level_irreps = {g: sorted([r for r in reach[g] if GR[g].casimir(r) == CF[g]], key=key_str) for g in groups}
    pieri2 = su_n_pieri(2)
    cg_equals_pieri = all({(k[0] if isinstance(k, tuple) else k): m for k, m in pieri2.tensor_F((tj,)).items()} == GR['SU(2)'].tensor_F(tj)
                          and pieri2.casimir((tj,)) == GR['SU(2)'].casimir(tj) for tj in range(12))
    G3 = GR['SU(3)']

    def bad_pieri(l):
        out = dict(G3.tensor_F(l))
        out[(l[0] + 1, l[1] + 1)] = out.get((l[0] + 1, l[1] + 1), 0) + 1      # a two-box shape added: not Pieri
        return out
    check('character_rules',
          all(CF[g] == CF_rule[g] for g in groups) and all(GR[g].casimir(GR[g].triv) == 0 for g in groups)
          and all(GR[g].casimir(GR[g].Fbar) == CF[g] for g in groups) and all(GR[g].dim(GR[g].F) == GR[g].d for g in groups)
          and all(dims_consistent(GR[g], reach[g]) for g in groups) and all(cas_min[g] == CF[g] for g in groups)
          and cg_equals_pieri and all(level_irreps[g] == sorted({GR[g].F, GR[g].Fbar}, key=key_str) for g in groups)
          and rejected(lambda: dims_consistent(G3, reach['SU(3)'], tensor=bad_pieri), 'non_pieri_shape_added'),
          irreps_with_casimir_C_F={g: [key_str(r) for r in level_irreps[g]] for g in groups},
          casimir_rules={g: GR[g].casimir_rule for g in groups}, C_F={g: s(CF[g]) for g in groups},
          smallest_nonzero_casimir_on_depth_6={g: s(cas_min[g]) for g in groups},
          irreps_checked={g: len(reach[g]) for g in groups},
          routes={g: GR[g].route_detail for g in groups}, su2_clebsch_gordan_equals_pieri_N2=cg_equals_pieri)

    # -------------------- moments by the character route --------------------
    mom = {g: moments_characters(GR[g], KMAX) for g in groups}
    chi_t = {g: {(a, b): chi_moment_tensor(GR[g], a, b) for a in range(KMAX + 1) for b in range(KMAX + 1 - a)} for g in groups}
    chi_c = {g: {(a, b): chi_moment_closed(GR[g], a, b) for a in range(KMAX + 1) for b in range(KMAX + 1 - a)} for g in groups}
    mom_t = {g: [moment_from_chi_table(GR[g], chi_t[g], k) for k in range(1, KMAX + 1)] for g in groups}
    mom_c = {g: [moment_from_chi_table(GR[g], chi_c[g], k) for k in range(1, KMAX + 1)] for g in groups}
    mom_pieri2 = moments_characters(pieri2, KMAX)
    check('moments_characters_route',
          all(mom[g] == mom_t[g] == mom_c[g] for g in groups) and chi_t == chi_c and mom_pieri2 == mom['SU(2)']
          and all(mom['SU(2)'][k - 1] == P['aw1_moments'][k] for k in range(1, 5))
          and all(isinstance(x, int) and x >= 0 for g in groups for x in chi_t[g].values()),
          moment_table={g: {str(k): s(mom[g][k - 1]) for k in range(1, KMAX + 1)} for g in groups},
          moment_previews={g: {str(k): dec(mom[g][k - 1]) for k in range(1, KMAX + 1)} for g in groups},
          chi_moments_a_b={g: {'%d,%d' % ab: chi_t[g][ab] for ab in sorted(chi_t[g])} for g in groups},
          sub_routes=['iterated action of W on the character basis', 'iterated tensor multiplicities E[chi^a conj(chi)^b]',
                      'closed-form counts (Schur-Weyl with hook lengths; charge balance; parity; SU(2) to SO(3) restriction with Catalan numbers)'],
          route_of_computation=ROUTE, su2_reproduces_admitted_AW1_moments=True)

    # -------------------- forward-internal Weyl cross-check (labelled) --------------------
    chi_w = {g: weyl_chi_table(GR[g], KMAX) for g in groups}
    mom_w = {g: [moment_from_chi_table(GR[g], chi_w[g], k) for k in range(1, KMAX + 1)] for g in groups}
    table_char = {'route': ROUTE, 'cells': {g + ':E[W^%d]' % k: s(mom[g][k - 1]) for g in groups for k in range(1, KMAX + 1)}}
    table_weyl = {'route': CROSS_ROUTE, 'cells': {g + ':E[W^%d]' % k: s(mom_w[g][k - 1]) for g in groups for k in range(1, KMAX + 1)}}
    c1 = {g: 2 * Q(1, md) * mom[g][1] / (ff * CF[g]) for g in groups}
    c1_w = {g: 2 * Q(1, md) * mom_w[g][1] / (ff * CF[g]) for g in groups}
    for g in groups:
        table_char['cells'][g + ':c1'] = s(c1[g])
        table_weyl['cells'][g + ':c1'] = s(c1_w[g])

    def compare_routes(ta, tb):
        require(ta['route'] in V['routes_allowed'] and tb['route'] in V['routes_allowed'] and ta['route'] != tb['route'],
                'two distinct routes (characters and weyl_integration) required')
        require(sorted(ta['cells']) == sorted(tb['cells']), 'single-route cell (a cell is missing from one table)')
        for k in ta['cells']:
            require(rat(ta['cells'][k]) == rat(tb['cells'][k]), 'routes disagree on ' + k)
        return True

    def mutate_table(tb, edit):
        t2 = {'route': tb['route'], 'cells': dict(tb['cells'])}
        edit(t2)
        return t2
    check('moment_tables_two_routes',
          compare_routes(table_char, table_weyl) and chi_w == chi_t
          and all(mom['U(1)'][k - 1] == weyl_moment_u1_direct(k) for k in range(1, KMAX + 1))
          and rejected(lambda: compare_routes(table_char, mutate_table(table_weyl, lambda t: t['cells'].pop('SU(3):E[W^3]'))),
                       'cell_missing_from_second_route')
          and rejected(lambda: compare_routes(table_char, mutate_table(table_weyl, lambda t: t['cells'].update({'SO(3):E[W^4]': 1 / 27}))),
                       'floating_point_moment')
          and rejected(lambda: compare_routes(table_char, mutate_table(table_weyl, lambda t: t['cells'].update({'SU(5):c1': '1/5761'}))),
                       'routes_disagree_on_a_coefficient')
          and rejected(lambda: compare_routes(table_char, dict(table_char)), 'same_route_counted_twice'),
          cells_compared=len(table_char['cells']),
          weyl_crosscheck_label='forward-internal cross-check by constant-term extraction on the maximal torus (U(1) direct integration, Z2 direct summation); not the reverse producer route and not an admission value; the admission comparison is with the reverse packet',
          weyl_chi_moments={g: {'%d,%d' % ab: chi_w[g][ab] for ab in sorted(chi_w[g])} for g in groups},
          route_labels=[ROUTE, CROSS_ROUTE])

    # -------------------- first-order coefficients --------------------
    a_coef = {g: Q(1, md) / (ff * CF[g]) for g in groups}
    su2_value = Q(1, V['su2_check_den'])
    check('first_order_coefficients',
          c1['SU(2)'] == su2_value == Q(1, P['aw1_coefficient_den'])
          and all(c1[g] == 2 * a_coef[g] * mom[g][1] for g in groups)
          and all(GR[g].kind != 'SU(N)' or mom[g][1] == Q(1, 2 * GR[g].N ** 2) for g in groups)
          and all(GR[g].kind != 'SU(N)' or c1[g] == Q(1, 48 * GR[g].N * (GR[g].N ** 2 - 1)) for g in groups)
          and len(set(c1.values())) == len(groups),
          first_order_table={g: {'value': s(c1[g]), 'preview': dec(c1[g]), 'tier': 'exact_first_order', 'route_of_computation': ROUTE,
                                 'formula': '2 (1/%d) E[W^2]/(%d C_F)' % (md, ff), 'E_W2': s(mom[g][1]), 'C_F': s(CF[g]),
                                 'face_energy': s(ff * CF[g]), 'creation_coefficient_per_face': s(-a_coef[g]) + ' tau'}
                             for g in groups},
          su2_convention_check='2 (1/3) (1/4)/24 = 1/144 reproduces the admitted AW1 coefficient (a check of the convention, not a transferred value)',
          su_n_closed_form='E[W^2]=1/(2N^2) and c1=1/(48 N (N^2-1)) for SU(N), N at least 3 (only E[|chi|^2]=1 survives)')

    # -------------------- exact Rayleigh-Schroedinger on H_FG(G) --------------------
    RS = {g: rs_series(GR[g], ORDER, ff, md) for g in groups}
    RS_t1 = {g: rs_series(GR[g], ORDER, ff, md, depth=ORDER + 2) for g in groups}
    RS_t2 = {g: rs_series(GR[g], ORDER, ff, md, depth=ORDER + 4) for g in groups}
    RS_shallow = rs_series(GR['SU(3)'], ORDER, ff, md, depth=1)

    def wigner(rs):
        psi, E, V1 = rs['psi'], rs['E'], rs['V1']
        E4 = ip(psi[1], V1(psi[2])) - E[2] * ip(psi[1], psi[1])
        E5 = ip(psi[2], V1(psi[2])) - E[3] * ip(psi[1], psi[1]) - 2 * E[2] * ip(psi[1], psi[2]) - E[1] * ip(psi[2], psi[2])
        return E4, E5

    def truncation_stable(a, b):
        for key in ('W', 'W2', 'C2', 'E'):
            require(a[key] == b[key], 'on-site truncation changes the ' + key + ' series')
        return True
    hf_ok = all(RS[g]['W'][m] == -md * (m + 1) * RS[g]['E'][m + 1] for g in groups for m in range(ORDER))
    wig_ok = all(wigner(RS[g]) == (RS[g]['E'][4], RS[g]['E'][5]) for g in groups)
    free_ok = all(RS[g]['W'][0] == 0 == mom[g][0] and RS[g]['W2'][0] == mom[g][1] for g in groups)
    E3 = {g: mom[g][2] for g in groups}
    dW2 = {g: RS[g]['W2'][1] for g in groups}
    c2 = {g: RS[g]['W'][2] for g in groups}
    c3 = {g: RS[g]['W'][3] for g in groups}
    c4 = {g: RS[g]['W'][4] for g in groups}
    check('rayleigh_schroedinger_one_plaquette',
          free_ok and hf_ok and wig_ok and all(RS[g]['W'][1] == c1[g] for g in groups)
          and all(truncation_stable(RS[g], RS_t1[g]) and truncation_stable(RS[g], RS_t2[g]) for g in groups)
          and all(dW2[g] == 2 * a_coef[g] * E3[g] and c2[g] == 3 * a_coef[g] ** 2 * E3[g] for g in groups)
          and RS['SU(2)']['W'][3] == Q(-5, 11943936)
          and rejected(lambda: truncation_stable(RS['SU(3)'], RS_shallow), 'truncated_below_the_order'),
          series={g: {'omega_W': [s(x) for x in RS[g]['W']], 'omega_W2': [s(x) for x in RS[g]['W2']],
                      'omega_C2': [s(x) for x in RS[g]['C2']], 'ground_energy': [s(x) for x in RS[g]['E']]} for g in groups},
          identities=['free reference omega_0(W)=E[W], omega_0(W^2)=E[W^2] in the same code path',
                      'Hellmann-Feynman c_m = -3 (m+1) E_{m+1} (omega(W) = -3 dE/dtau)',
                      'Wigner 2n+1: E_4 and E_5 from psi_1, psi_2 equal the direct RS energies',
                      'closed forms dω(W^2)/dτ = 2a E[W^3], c_2 = 3a^2 E[W^3], a = (1/3)/(32 C_F)'],
          truncation='none: every order uses the finite set of irreps reachable by that many applications of W; depth-7 and depth-9 cutoffs give identical series; a depth-1 cutoff changes the SU(3) series and is rejected',
          su2_series_matches_admitted_AW1_fixture='tau/144 + 0 tau^2 - (5/11943936) tau^3 + ...',
          model_is_finite_graph=True, transfers_to_aq=False)
    SERIES_CHECK_ID = 'rayleigh_schroedinger_one_plaquette'

    # -------------------- level matrices and C(s) first-order terms --------------------
    level = {}
    cstate = {}
    cduh = {}
    for g in groups:
        G = GR[g]
        basis = [G.F] if G.F == G.Fbar else [G.F, G.Fbar]
        M = [[apply_W(G, {t: Q(1)}).get(r, Q(0)) for t in basis] for r in basis]
        wo = apply_W(G, {G.triv: Q(1)})
        e3 = ip(wo, apply_W(G, wo))
        require(e3 == E3[g], 'E[W^3] differs between the level computation and the moment table')
        coef = Q(1, (2 * G.d) ** 2) if len(basis) == 2 else Q(1, G.d ** 2)
        require(e3 == coef * sum(sum(row) for row in M), 'E[W^3] is not the level-matrix sum')
        level[g] = {'basis': [key_str(b) for b in basis], 'W_matrix': [[s(x) for x in row] for row in M],
                    'PVP_first_order_splitting_matrix': [[s(-x / md) for x in row] for row in M],
                    'all_entries_nonnegative': all(x >= 0 for row in M for x in row),
                    'zero': all(x == 0 for row in M for x in row)}
        cstate[g] = 2 * a_coef[g] * e3
        cduh[g] = e3 / md
    cubic = {g: {'%d,%d' % (a, 3 - a): chi_t[g][(a, 3 - a)] for a in range(4)} for g in groups}

    # -------------------- criterion A: central element acting as -I --------------------
    central = {}
    for g in groups:
        G = GR[g]
        found = [t for t in G.centre if (t - Q(1, 2)).denominator == 1]
        central[g] = found[0] if found else None
    flip_groups = [g for g in groups if central[g] is not None]
    nonflip_groups = [g for g in groups if central[g] is None]

    def flip_operator_ok(G, t):
        for r in reachable(G, 6):
            for u in apply_W(G, {r: Q(1)}):
                require((G.grade(u) - G.grade(r)) % 2 == 1, 'U_z W U_z^* differs from -W at ' + repr((r, u)))
        return True

    def reason_no_flip(G):
        for t in G.centre:
            require((t - Q(1, 2)).denominator != 1, 'a central element acts as -1 on F')
        return True

    def central_claim(G, t):
        require(t is not None and (t - Q(1, 2)).denominator == 1 and t in G.centre, 'no central element acting as -I on F')
        if G.det_minus_identity is not None:
            require(G.det_minus_identity == 1, '-I is not an element of the group')
        return True
    det_ok = all((GR[g].det_minus_identity == 1) == (central[g] is not None) for g in groups if GR[g].det_minus_identity is not None)
    check('criterion_A_central_minus_one',
          flip_groups == ['SU(2)', 'SU(4)', 'U(1)', 'Z2'] and nonflip_groups == ['SU(3)', 'SU(5)', 'SO(3)'] and det_ok
          and all(central_claim(GR[g], central[g]) and flip_operator_ok(GR[g], central[g]) for g in flip_groups)
          and all(reason_no_flip(GR[g]) for g in nonflip_groups)
          and rejected(lambda: flip_operator_ok(GR['SU(3)'], Q(1, 3)), 'centre_element_omega_used_as_flip_on_SU3')
          and rejected(lambda: central_claim(GR['SU(5)'], Q(2, 5)), 'fifth_root_claimed_as_minus_one')
          and rejected(lambda: central_claim(GR['SO(3)'], Q(0)), 'identity_of_SO3_claimed_as_minus_one'),
          central_element={g: ({'turn': s(central[g]), 'element': {'SU(2)': '-I', 'SU(4)': '-I', 'U(1)': 'exp(i pi)', 'Z2': 'the nontrivial element'}[g],
                                'value_on_F': '-1'} if central[g] is not None else None) for g in groups},
          centre={g: [s(t) for t in GR[g].centre] for g in groups}, reason={g: GR[g].centre_reason for g in groups},
          det_minus_identity={g: GR[g].det_minus_identity for g in groups if GR[g].det_minus_identity is not None},
          one_plaquette_operator='U_z = diag(exp(2 pi i t grade(r))) on the character basis; for t=1/2 it is diag((-1)^grade(r)); W changes the grade by one, so U_z W U_z^* = -W and U_z commutes with 32 C_2',
          statement='the absence of a central -1 is recorded as the reason; the proof of non-transfer is the nonzero even-order coefficient of the obstruction cell')

    # -------------------- criterion B: third moment and the degenerate level --------------------
    parity_groups = [g for g in groups if E3[g] == 0]

    def parity_claim(g):
        require(E3[g] == 0 and all(chi_t[g][(a, 3 - a)] == 0 for a in range(4)), 'E[W^3] is not zero: no first-order parity')
        require(level[g]['zero'] and dW2[g] == 0 and cstate[g] == 0 and cduh[g] == 0, 'first-order terms do not vanish')
        return True
    equiv_ok = all((E3[g] == 0) == all(chi_t[g][(a, 3 - a)] == 0 for a in range(4)) == level[g]['zero'] for g in groups)
    check('criterion_B_third_moment',
          parity_groups == ['SU(2)', 'SU(4)', 'SU(5)', 'U(1)', 'Z2'] and equiv_ok
          and all(level[g]['all_entries_nonnegative'] for g in groups) and all(parity_claim(g) for g in parity_groups)
          and all(dW2[g] != 0 and cstate[g] != 0 and cduh[g] != 0 and not level[g]['zero'] for g in groups if g not in parity_groups)
          and rejected(lambda: parity_claim('SU(3)'), 'parity_claimed_for_SU3')
          and rejected(lambda: parity_claim('SO(3)'), 'parity_claimed_for_SO3'),
          cubic_moments_E_chi_a_conjchi_b=cubic, E_W3={g: s(E3[g]) for g in groups},
          level_matrices=level,
          first_order_one_plaquette={g: {'d_omega_W2_dtau': s(dW2[g]), 'C_s_state_coefficient_of_exp(-32 C_F s)': s(cstate[g]),
                                         'C_s_duhamel_coefficient_of_s_exp(-32 C_F s)': s(cduh[g]),
                                         'c_theta_duhamel_coefficient_of_-i_theta_exp(i 32 C_F theta)': s(cduh[g]),
                                         'tier': 'exact_first_order', 'route_of_computation': ROUTE} for g in groups},
          equivalence='E[W^3]=(2d)^-3 sum_{a+b=3} C(3,a) E[chi^a conj(chi)^b] with nonnegative integer terms, so E[W^3]=0 iff every cubic moment vanishes iff the level matrix (entries cubic moments) vanishes',
          converse_on_H_FG='d omega(W^2)/d tau = 2a E[W^3] and the C(s), c(theta) first-order terms are e^{-32 C_F s} E[W^3](2a + s/3) and e^{i 32 C_F theta} E[W^3](2a - i theta/3): nonzero when E[W^3] is nonzero')

    # -------------------- I1 geometry and the group box models H^G_N --------------------
    table = parse_i1_table()
    classes = expand_classes(table, 'omitted')
    sel_classes = expand_classes(table, 'selected')
    geo_ok = len(classes) == 21 and len(sel_classes) == 3 and all(
        support_of(class_face(b, cls)) == frozenset(add(b, d) for d in cls[3])
        for b in (ORIGIN, (1, -1, 2), (-2, 3, -1)) for cls in classes + sel_classes)
    boxes = {}
    for N in V['flip_boxes']:
        links = box_links(N)
        plaqs = box_plaquettes(links)
        anchors, faces = retained_faces(N, classes)
        require(all(links_of(f) <= links for f in faces), 'retained faces use box links only')
        boxes[N] = {'links': links, 'plaqs': plaqs, 'anchors': anchors, 'faces': faces}
    faces2 = boxes[2]['faces']
    require(WILSON in faces2, 'the Wilson face is a retained face of the N=2 box')

    def link_counts(word):
        cnt = {}
        for f in word:
            for l in face_links(f):
                cnt[l] = cnt.get(l, 0) + 1
        return cnt

    def expect(word, g):
        """Haar mean of a product of face variables W_f of group g: zero when some link occurs exactly once
        (single-occurrence orthogonality: a nontrivial irreducible matrix coefficient has Haar mean 0); one repeated
        face gives the plaquette moment E[W^k] (four independent Haar links give a Haar holonomy)."""
        if not word:
            return Q(1)
        if any(k == 1 for k in link_counts(word).values()):
            return Q(0)
        if all(f == word[0] for f in word):
            return mom[g][len(word) - 1]
        raise AdmissionError('word not evaluated: ' + repr(word))
    box_terms = {}
    for g in groups:
        st = sum((expect([WILSON, WILSON, f], g) for f in faces2), Q(0))
        du = sum((expect([WILSON, f, WILSON], g) for f in faces2), Q(0))
        en = sum((expect([f], g) for f in faces2), Q(0))
        me = sum((expect([WILSON, f], g) for f in faces2), Q(0))
        box_terms[g] = {'state_sum_E[W^2 W_f]': st, 'duhamel_sum_E[W W_f W]': du, 'energy_sum_E[W_f]': en, 'mean_sum_E[W W_f]': me,
                        'first_order_coefficient_box': 2 * a_coef[g] * me, 'd_omega_W2_dtau_box': 2 * a_coef[g] * (st - mom[g][1] * en)}
    box1_plaqs = box_plaquettes(box_links(1))
    by_link = {}
    for f in box1_plaqs:
        for l in face_links(f):
            by_link.setdefault(l, []).append(f)
    shared = {}
    for l, fs in by_link.items():
        for i in range(len(fs)):
            for j in range(i + 1, len(fs)):
                key = (fs[i], fs[j])
                shared[key] = shared.get(key, 0) + 1
    max_shared = max(shared.values())
    near_W = [f for f in box1_plaqs if links_of(f) & links_of(WILSON)]
    meet_W = [f for f in faces2 if links_of(f) & links_of(WILSON)]
    triples = 0
    diag_triples = 0
    for g1 in near_W:
        for f in meet_W:
            for h in near_W:
                val = expect([g1, f, h], 'SU(3)')
                triples += 1
                if g1 == f == h:
                    diag_triples += 1
                    require(val == E3['SU(3)'], 'diagonal triple')
                else:
                    require(val == 0, 'off-diagonal triple nonzero')

    def box_parity_claim(g):
        require(box_terms[g]['state_sum_E[W^2 W_f]'] == 0 and box_terms[g]['duhamel_sum_E[W W_f W]'] == 0
                and box_terms[g]['energy_sum_E[W_f]'] == 0, 'box first-order terms do not vanish for ' + g)
        return True

    def uncentered_mean_zero(g):
        require(box_terms[g]['mean_sum_E[W W_f]'] == 0, 'the uncentered mean has a nonzero first-order coefficient')
        return True
    kato = {g: {'one_plaquette': md * ff * cas_min[g] / 2,
                'box': {str(N): md * lf * cas_min[g] / (2 * len(boxes[N]['faces'])) for N in V['flip_boxes']}} for g in groups}
    # the gauge-invariant level at energy 32 C_F of the box: every multiset of nontrivial irreps with Casimir sum 4 C_F
    deep = {g: reachable(GR[g], 10) for g in groups}
    small = {g: sorted([r for r in deep[g] if 0 < GR[g].casimir(r) <= 4 * CF[g]], key=key_str) for g in groups}
    small8 = {g: sorted([r for r in reachable(GR[g], 8) if 0 < GR[g].casimir(r) <= 4 * CF[g]], key=key_str) for g in groups}
    decomp = {}
    for g in groups:
        cas = sorted(GR[g].casimir(r) for r in small[g])
        sols = []

        def rec(start, rem, acc):
            if rem == 0:
                sols.append(tuple(acc))
                return
            for i in range(start, len(cas)):
                if cas[i] <= rem:
                    rec(i, rem - cas[i], acc + [cas[i]])
        rec(0, 4 * CF[g], [])
        decomp[g] = sorted(set(sols))
    level_ok = all(small[g] == small8[g] for g in groups) and all(
        all(len(sol) <= 3 or (len(sol) == 4 and all(x == CF[g] for x in sol)) for sol in decomp[g]) for g in groups)
    steps = [tuple(sgn if i == d else 0 for i in range(3)) for d in range(3) for sgn in (1, -1)]
    cycles = set()
    for walk in itertools.product(steps, repeat=4):
        pos = ORIGIN
        edges = []
        for st in walk:
            nxt = add(pos, st)
            edges.append(frozenset((pos, nxt)))
            pos = nxt
        if pos == ORIGIN and len(set(edges)) == 4:
            cycles.add(frozenset(edges))
    plaq_cycles = set()
    for o in ORIENTS:
        for base in itertools.product((-1, 0), repeat=3):
            es = frozenset(frozenset((pp, add(pp, UNIT[d]))) for pp, d in face_links((base, o)))
            if any(ORIGIN in e for e in es):
                plaq_cycles.add(es)
    check('criterion_B_box_models',
          level_ok and len(cycles) == 12 and cycles == plaq_cycles
          and geo_ok and max_shared == 1 and diag_triples == len([f for f in meet_W if f in near_W])
          and all(box_terms[g]['state_sum_E[W^2 W_f]'] == E3[g] == box_terms[g]['duhamel_sum_E[W W_f W]'] for g in groups)
          and all(box_terms[g]['energy_sum_E[W_f]'] == 0 and box_terms[g]['mean_sum_E[W W_f]'] == mom[g][1] for g in groups)
          and all(box_terms[g]['first_order_coefficient_box'] == c1[g] and box_terms[g]['d_omega_W2_dtau_box'] == dW2[g] for g in groups)
          and all(box_parity_claim(g) for g in parity_groups)
          and rejected(lambda: box_parity_claim('SU(3)'), 'box_parity_claimed_for_SU3')
          and rejected(lambda: uncentered_mean_zero('U(1)'), 'parity_applied_to_the_uncentered_mean'),
          model='H^G_N = sum over box links 8 C_2 - (tau/3) sum over the retained whole-star faces W_f (selected faces coefficient 0), N=2 box, the AW1 original xz face W as observable',
          retained_faces_N2=len(faces2), plaquettes_N1=len(box1_plaqs), max_links_shared_by_distinct_plaquettes=max_shared,
          triples_checked=triples, diagonal_triples=diag_triples,
          box_terms={g: {k: s(v) for k, v in box_terms[g].items()} for g in groups},
          kato_radius_sufficient={g: {'one_plaquette': s(kato[g]['one_plaquette']), 'box': {N: s(x) for N, x in kato[g]['box'].items()}}
                                  for g in groups},
          kato_rule='simple isolated ground eigenvalue persists for |tau| ||V1|| below half the free gap: one plaquette gap 32 C_min, ||V1||=1/3; box gap 8 C_min (one excited link), ||V1|| at most (number of retained faces)/3; the radius is box dependent and not uniform in N',
          single_occurrence='a link carried by exactly one factor of a product of face variables gives Haar mean 0 in every listed group (nontrivial irreducible matrix coefficients of F and Fbar have mean 0)',
          level_casimir_decompositions={g: [[s(x) for x in sol] for sol in decomp[g]] for g in groups},
          level_reading='a gauge-invariant vector needs every touched vertex to carry at least two excited link ends (a single nontrivial irrep has no invariant); decompositions with at most three links would need a cycle of length at most 3, absent in the bipartite Z^3; four links force Casimir C_F on each (C_F is the smallest nonzero Casimir), i.e. F or Fbar on a 4-cycle, and the 4-cycles through a site are exactly its 12 plaquettes; so the level is span{chi_F(U_g) Omega_0, conj chi_F(U_g) Omega_0}',
          four_cycles_through_origin=len(cycles),
          tier='exact_first_order', route_of_computation=ROUTE)

    # -------------------- criterion A on the box models: exact rational fixtures --------------------
    in_E3 = make_in_E(V['E3_spec'])
    in_E2 = make_in_E(V['E2_spec'])
    su4_elems = signed_perms_det1(4)
    su4_ok = all(mat_det(u) == 1 for u in su4_elems) and mat_det(mat_neg(su4_elems[0])) == 1
    fixture_rows = {}

    def centre_coboundary(link):
        p, d = link
        q = add(p, UNIT[d])
        return ((p[0] + 2 * p[1] + p[2]) % 3 == 0) != ((q[0] + 2 * q[1] + q[2]) % 3 == 0)

    def su2_face(f, flip=None, gauge=None):
        l1, l2, l3, l4 = face_links(f)
        return wilson_loop_su2([(l1, 1), (l2, 1), (l3, -1), (l4, -1)], flip=flip, gauge=gauge)

    def run_fixture(kind, flip):
        vals = []
        for f in faces2:
            if kind == 'SU(2)':
                w0, w1 = su2_face(f), su2_face(f, flip=flip)
                wg = su2_face(f, gauge=quat_vertex)
            else:
                elems = {'SU(4)': su4_elems, 'U(1)': CIRCLE, 'Z2': [1, -1, -1, 1, 1, -1, 1]}[kind]
                gauge = {'SU(4)': lambda p: su4_elems[(3 * p[0] + p[1] + 2 * p[2]) % len(su4_elems)],
                         'U(1)': lambda p: CIRCLE[(p[0] + 3 * p[1] + 5 * p[2]) % len(CIRCLE)],
                         'Z2': lambda p: (-1) ** ((p[0] + p[1] * p[2]) % 2)}[kind]
                w0 = group_face_value(kind, f, elems=elems)
                w1 = group_face_value(kind, f, flip=flip, elems=elems)
                wg = group_face_value(kind, f, gauge=gauge, elems=elems)
            require(w1 == -w0, 'the flip does not reverse W_f for ' + kind + ' at ' + repr(f))
            require(wg == w0, 'W_f is not gauge invariant for ' + kind)
            vals.append(w0)
        require(any(x != 0 for x in vals), 'fixture has no nonzero face value')
        return sum(1 for x in vals if x != 0)
    for kind in ('SU(2)', 'SU(4)', 'U(1)', 'Z2'):
        fixture_rows[kind] = run_fixture(kind, in_E3)
    check('criterion_A_box_models',
          su4_ok and all(n > 0 for n in fixture_rows.values()) and validate_odd(boxes[2]['plaqs'], in_E3, 'N=2 box')
          and rejected(lambda: run_fixture('SU(4)', centre_coboundary), 'centre_gauge_transformation_presented_as_flip')
          and rejected(lambda: run_fixture('U(1)', make_in_E(V['E3_spec'], removed=frozenset([face_links(WILSON)[0]]))),
                       'flip_set_minus_one_link_on_U1'),
          fixtures={'SU(2)': 'rational unit quaternions, z=-1', 'SU(4)': 'signed permutation matrices of determinant 1 (%d elements), z=-I, det(-I)=1' % len(su4_elems),
                    'U(1)': 'rational points of the unit circle, z=-1', 'Z2': 'signs, z=-1'},
          faces_checked=len(faces2), nonzero_face_values=fixture_rows,
          operator_statement='U_E = product over links of E of translation by z: commutes with left and right translations (z central), hence with every link Casimir, every endpoint gauge action and every on-site cutoff projection (spectral projections of the onsite sum of 8 C_2); fixes the Haar vacuum; W_f goes to (-1)^{|f cap E|} W_f = -W_f; so U_E H^G_N(tau) U_E^* = H^G_N(-tau) in every open centered whole-star box and cutoff',
          label='finite exact fixtures (algebra audits), not the operator proof')

    # -------------------- obstruction cells --------------------
    def cell_of(g):
        return {'group': g, 'wilson_representation': V['wilson_rep'][g], 'model': 'H_FG(%s)' % g, 'tau': 'symbolic',
                'central_minus_one': None if central[g] is None else s(central[g]), 'det_minus_identity': GR[g].det_minus_identity,
                'E_W3': s(E3[g]), 'd_omega_W2_dtau': s(dW2[g]), 'c2_omega_W': s(c2[g]), 'c3_omega_W': s(c3[g]), 'c4_omega_W': s(c4[g]),
                'route_of_computation': ROUTE, 'model_is_finite_graph': True, 'transfers_to_aq': False,
                'flip': 'transfer_to_named_model' if central[g] is not None else 'obstruction_recorded',
                'parity': 'transfer_to_named_model' if E3[g] == 0 else 'obstruction_recorded'}

    def validate_obstruction(cell, g):
        require(cell is not None, 'mandatory obstruction cell omitted: ' + g)
        require(cell['group'] == g and cell['central_minus_one'] is None and cell['det_minus_identity'] == -1, 'central -1 status')
        require(cell['flip'] == 'obstruction_recorded' and cell['parity'] == 'obstruction_recorded', g + ' called a transfer')
        require(rat(cell['E_W3']) == E3[g] != 0, 'E[W^3] must be exact and nonzero')
        require(rat(cell['d_omega_W2_dtau']) == dW2[g] != 0, 'first-order derivative of omega(W^2) must be nonzero')
        require(rat(cell['c2_omega_W']) == c2[g] != 0, 'second-order coefficient of omega(W) must be nonzero')
        return True

    def validate_su5(cell):
        require(cell is not None, 'SU(5) cell omitted')
        require(cell['central_minus_one'] is None and cell['det_minus_identity'] == -1, 'SU(5) central status')
        require(cell['flip'] == 'obstruction_recorded', 'SU(5) called a flip transfer')
        require(cell['parity'] == 'transfer_to_named_model' and rat(cell['E_W3']) == 0, 'SU(5) parity column must be a transfer')
        require(rat(cell['d_omega_W2_dtau']) == 0 and rat(cell['c2_omega_W']) == 0, 'SU(5) first coefficients must vanish')
        require(cell.get('flip_counterexample_order') == 4 and rat(cell['c4_omega_W']) == c4['SU(5)'] != 0,
                'SU(5) flip obstruction needs the exact nonzero fourth-order coefficient')
        require(cell.get('route_of_computation') == ROUTE, 'SU(5) route not recorded')
        return True
    cells_obs = {g: cell_of(g) for g in groups}
    cells_obs['SU(5)']['flip_counterexample_order'] = 4
    for g in ('SU(3)', 'SO(3)'):
        cells_obs[g]['flip_counterexample_order'] = 2
    su5 = GR['SU(5)']
    psi2 = RS['SU(5)']['psi'][2]
    V1s = RS['SU(5)']['V1']
    channels = sorted({(key_str(r), key_str(t)) for r in psi2 for t, x in V1s({r: Q(1)}).items() if t in psi2 and x != 0})
    grades = {m: sorted({su5.grade(r) % 5 for r in RS['SU(5)']['psi'][m]}) for m in range(ORDER + 1)}
    c4_closed = Q(1, 2 ** 30 * 3 ** 10)
    E5_w = wigner(RS['SU(5)'])[1]

    def mutated(cell, **kw):
        out = dict(cell)
        out.update(kw)
        return out
    check('su3_obstruction_mandatory',
          validate_obstruction(cells_obs['SU(3)'], 'SU(3)') and E3['SU(3)'] == Q(1, 108) and dW2['SU(3)'] == Q(1, 6912)
          and c2['SU(3)'] == Q(1, 589824) and chi_t['SU(3)'][(3, 0)] == 1 == chi_t['SU(3)'][(0, 3)]
          and rejected(lambda: validate_obstruction(None, 'SU(3)'), 'su3_cell_omitted')
          and rejected(lambda: validate_obstruction(mutated(cells_obs['SU(3)'], flip='transfer_to_named_model'), 'SU(3)'), 'su3_called_flip_transfer')
          and rejected(lambda: validate_obstruction(mutated(cells_obs['SU(3)'], parity='transfer_to_named_model'), 'SU(3)'), 'su3_called_parity_transfer')
          and rejected(lambda: validate_obstruction(mutated(cells_obs['SU(3)'], c2_omega_W='0'), 'SU(3)'), 'su3_second_order_set_to_zero'),
          cell=cells_obs['SU(3)'], previews={'E_W3': dec(E3['SU(3)']), 'd_omega_W2_dtau': dec(dW2['SU(3)']), 'c2': dec(c2['SU(3)'])},
          reason='centre Z_3 acts by cube roots of unity; det(-I)=-1; E[chi^3]=E[conj(chi)^3]=1 (the invariant epsilon tensor)',
          counterexample='second-order coefficient of omega(W) on H_FG(SU(3)) = 3a^2 E[W^3] = 1/589824, a=1/128: omega(W) is not odd in tau, so no unitary commuting with 32 C_2 reverses W on H_FG(SU(3))')
    check('so3_obstruction_mandatory',
          validate_obstruction(cells_obs['SO(3)'], 'SO(3)') and E3['SO(3)'] == Q(1, 27) and dW2['SO(3)'] == Q(1, 2592)
          and c2['SO(3)'] == Q(1, 331776) and chi_t['SO(3)'][(3, 0)] == 1
          and rejected(lambda: validate_obstruction(None, 'SO(3)'), 'so3_cell_omitted')
          and rejected(lambda: validate_obstruction(mutated(cells_obs['SO(3)'], central_minus_one='1/2'), 'SO(3)'), 'so3_given_a_central_minus_one')
          and rejected(lambda: validate_obstruction(mutated(cells_obs['SO(3)'], d_omega_W2_dtau='0'), 'SO(3)'), 'so3_derivative_set_to_zero'),
          cell=cells_obs['SO(3)'], previews={'E_W3': dec(E3['SO(3)']), 'd_omega_W2_dtau': dec(dW2['SO(3)']), 'c2': dec(c2['SO(3)'])},
          reason='trivial centre; det(-I)=(-1)^3=-1 so -I is not in SO(3); E[chi_1^3]=1 (epsilon_{ijk})',
          counterexample='second-order coefficient of omega(W) on H_FG(SO(3)) = 3a^2 E[W^3] = 1/331776, a=1/192')
    check('su5_flip_obstruction_fourth_order',
          validate_su5(cells_obs['SU(5)']) and c4['SU(5)'] == c4_closed == -5 * md * RS['SU(5)']['E'][5] == -5 * md * E5_w
          and channels == [('1,1,0,0', '1,1,1,0'), ('1,1,1,0', '1,1,0,0')] and grades[2] == [0, 2, 3]
          and c3['SU(5)'] != 0 and mom['SU(5)'][4] == Q(1, 50000) and chi_t['SU(5)'][(5, 0)] == 1
          and rejected(lambda: validate_su5(mutated(cells_obs['SU(5)'], flip='transfer_to_named_model')), 'su5_called_flip_transfer')
          and rejected(lambda: validate_su5(mutated(cells_obs['SU(5)'], parity='obstruction_recorded')), 'su5_parity_called_obstruction')
          and rejected(lambda: validate_su5(mutated(cells_obs['SU(5)'], flip_counterexample_order=None)), 'su5_obstruction_from_missing_centre_alone')
          and rejected(lambda: validate_su5(mutated(cells_obs['SU(5)'], c4_omega_W='0')), 'su5_fourth_order_set_to_zero')
          and rejected(lambda: validate_su5(mutated(cells_obs['SU(5)'], route_of_computation=None)), 'su5_route_missing'),
          cell=cells_obs['SU(5)'], c4_preview=dec(c4['SU(5)']), c4_closed_form='1/(2^30 3^10)',
          computations=['direct RS (normalized expectation series)', 'Hellmann-Feynman -15 E_5 with E_5 from direct RS',
                        'Wigner 2n+1: E_5 = (psi_2, V_1 psi_2) - E_3 |psi_1|^2 - 2 E_2 (psi_1, psi_2) with E_3=(psi_1,psi_2)=0'],
          z5_grading={'psi_m_grades_mod_5': {str(m): grades[m] for m in grades},
                      'rule': 'the order-m coefficient of omega(W) is a sum of Haar means of m+1 factors W, each changing the 5-ality by +-1; a nonzero mean needs a+b=m+1 with a-b divisible by 5, so m=2 (and the first derivative of omega(W^2), three factors) vanish and m=4 (a=5, E[chi^5]=1) is the first possible nonzero even order'},
          channel='only the Lambda^2 (1,1,0,0) and Lambda^3 (1,1,1,0) components of psi_2 couple through W: F x Lambda^2 contains Lambda^3 and Fbar x Lambda^3 contains Lambda^2',
          reason='centre Z_5 acts by fifth roots of unity; det(-I)=-1', model_is_finite_graph=True, transfers_to_aq=False)

    # -------------------- flip sets E_3 and E_2 --------------------
    parity_classes = []
    for o in ORIENTS:
        for par in itertools.product((0, 1), repeat=3):
            cnt = flip_count((par, o), in_E3)
            cov = all(flip_count((add(par, (2 * i, 2 * j, 2 * k)), o), in_E3) == cnt for i in (-2, 1, 3) for j in (-1, 2) for k in (-3, 1))
            parity_classes.append({'orientation': 'xyz'[o[0]] + 'xyz'[o[1]], 'base_parity': list(par), 'links_in_E3': cnt, 'covariant': cov})
    classes_odd = len(parity_classes) == 24 and all(pc['links_in_E3'] % 2 == 1 and pc['covariant'] for pc in parity_classes)
    box_rows = {}
    for N in V['flip_boxes']:
        bx = boxes[N]
        validate_odd(bx['plaqs'], in_E3, 'box N=%d' % N)
        validate_odd(bx['faces'], in_E3, 'retained faces N=%d' % N)
        box_rows[str(N)] = {'links': len(bx['links']), 'plaquettes_owned': len(bx['plaqs']),
                            'plaquette_histogram': histogram(bx['plaqs'], in_E3), 'retained_faces': len(bx['faces']),
                            'retained_histogram': histogram(bx['faces'], in_E3), 'anchors': len(bx['anchors'])}
    n2 = box_rows['2']
    aw1_match = (n2['retained_faces'], n2['plaquettes_owned'], n2['plaquette_histogram'].get('1'),
                 n2['plaquette_histogram'].get('3')) == P['aw1_N2_counts']
    lo, hi = P['aw1_fine_box'][0], P['aw1_fine_box'][1]
    fine = [(p, o) for p in itertools.product(range(-lo, hi + 1), repeat=3) for o in ORIENTS]
    fine_hist = histogram(fine, in_E3)
    fine_match = (len(fine), fine_hist.get('1'), fine_hist.get('3')) == P['aw1_fine_box'][2:] and set(fine_hist) == {'1', '3'}
    probes = (ORIGIN, (0, 0, 1), (1, 0, 0), (0, 1, 0), (1, 1, 1), (-1, -1, -1), (2, -3, 5))

    def plaquettes_meeting(b):
        out = set()
        for t, d in owned_links(b):
            for o in ORIENTS:
                if d in o:
                    other = o[1] if d == o[0] else o[0]
                    out.add((t, o))
                    out.add((sub(t, UNIT[other]), o))
        return sorted(out)
    factor_rows = {}
    for b in probes:
        meet = plaquettes_meeting(b)
        omitted = [class_face(sub(b, d), cls) for cls in classes for d in sorted(cls[3])]
        selected = [class_face(b, cls) for cls in sel_classes]
        require(all(any(owner(l[0]) == b for l in face_links(f)) for f in meet), 'plaquettes meeting a factor')
        validate_odd(meet, in_E3, 'plaquettes meeting factor %r' % (b,))
        validate_odd(omitted + selected, in_E3, 'faces of factor %r' % (b,))
        factor_rows[key_str(b)] = {'z_parity': b[2] % 2, 'links_in_E3': sum(1 for l in owned_links(b) if in_E3(l)),
                                   'plaquettes_meeting_factor': len(meet), 'histogram_meeting': histogram(meet, in_E3),
                                   'omitted_faces_containing_factor': len(set(omitted)), 'selected_faces_anchored': len(selected)}
    e_by_parity = {str(par): sorted({r['links_in_E3'] for r in factor_rows.values() if r['z_parity'] == par}) for par in (0, 1)}

    def translation_invariant(b, shift_coarse):
        fine_shift = (4 * shift_coarse[0], 2 * shift_coarse[1], shift_coarse[2])
        here = sorted(l for l in owned_links(b) if in_E3(l))
        there = sorted((sub(p, fine_shift), d) for p, d in owned_links(add(b, shift_coarse)) if in_E3((p, d)))
        require(here == there, 'E_3 is not invariant under the coarse translation %r' % (shift_coarse,))
        return True
    xy_inv = all(translation_invariant(b, v) for b in probes for v in ((1, 0, 0), (0, 1, 0), (0, 0, 2), (-1, 0, 0)))
    e2_rows = {str(N): validate_exactly_one_2d(N, in_E2) for N in V['flip_boxes']}
    tori3 = {'x'.join(map(str, t)): torus_counts_3d(t, V['E3_spec']) for t in ((4, 4, 4), (3, 4, 4), (4, 3, 4), (4, 4, 3), (3, 3, 4))}
    tori2 = {'x'.join(map(str, t)): torus_counts_2d(t, V['E2_spec']) for t in ((4, 4), (4, 3), (3, 4), (3, 3))}
    gf2 = {'x'.join(map(str, t)): gf2_flip_set_exists(t) for t in ((4, 4, 4), (3, 4, 4), (3, 3, 4), (3, 3, 3), (4, 4), (3, 4), (3, 3))}

    def validate_torus3(sides):
        require(torus_counts_3d(sides, V['E3_spec'])[1] == 0, 'E_3 has even plaquettes at the seam of the periodic torus %r' % (sides,))
        return True

    def e2_plus_link(link):
        return in_E2(link) or link == ((0, 0), 1)
    check('flip_sets_verified',
          classes_odd and aw1_match and fine_match and xy_inv and e_by_parity == {'0': [16], '1': [8]}
          and all(r['omitted_faces_containing_factor'] == 49 and r['selected_faces_anchored'] == 3 for r in factor_rows.values())
          and tori3['4x4x4'][1] == 0 and all(tori3[k][1] > 0 for k in ('3x4x4', '4x3x4', '4x4x3', '3x3x4'))
          and tori2['4x4'][1] == 0 and tori2['4x3'][1] > 0 and tori2['3x3'][1] > 0 and tori2['3x4'][1] == 0
          and gf2 == {'4x4x4': True, '3x4x4': True, '3x3x4': False, '3x3x3': False, '4x4': True, '3x4': True, '3x3': False}
          and rejected(lambda: validate_odd(boxes[2]['plaqs'], make_in_E(V['E3_spec'], removed=frozenset([face_links(WILSON)[0]])), 'E_3 minus a link'),
                       'E3_minus_one_link')
          and rejected(lambda: validate_exactly_one_2d(2, e2_plus_link), 'E2_plus_one_link')
          and rejected(lambda: validate_torus3((4, 4, 3)), 'odd_periodic_side_verified')
          and rejected(lambda: translation_invariant(ORIGIN, (0, 0, 1)), 'E3_claimed_invariant_under_odd_coarse_z_translation'),
          residue_classes=parity_classes, boxes=box_rows, aw1_N2_counts_reproduced=aw1_match,
          aw1_fine_box_counts_reproduced={'box': '[-%d,%d]^3 base points' % (lo, hi), 'plaquettes': len(fine), 'histogram': fine_hist},
          factors=factor_rows, E3_links_per_factor_by_z_parity=e_by_parity,
          coarse_translations='E_3 is invariant under coarse x and y translations (fine shifts 4 and 2) and even coarse z translations; not under odd coarse z translations (the y-links flip parity), which the flip lemma does not need',
          E2_boxes={N: {'plaquettes': n, 'links_in_E2_per_plaquette': 1} for N, n in e2_rows.items()},
          periodic_tori_E3={k: {'plaquettes': v[0], 'even_plaquettes_at_seam': v[1]} for k, v in tori3.items()},
          periodic_tori_E2={k: {'plaquettes': v[0], 'even_plaquettes_at_seam': v[1]} for k, v in tori2.items()},
          periodic_obstruction='E_3 has even seam plaquettes on every listed torus with an odd side and E_2 on tori with odd y side; recorded as an obstruction, not verified; no flip statement is made on any periodic box',
          remark_gf2_not_claimed={'any_flip_set_exists': gf2,
                                  'reading': 'GF(2) elimination: some flip set exists on tori with at most one odd side (3D) or at least one even side (2D), none when two sides are odd; a remark outside the contract, not claimed'})

    # -------------------- SU(2) area parity --------------------
    links2 = boxes[2]['links']
    loop_defs = [('W_face_xz_1x1',) + rectangle(ORIGIN, 0, 2, 1, 1), ('xy_2x1',) + rectangle(ORIGIN, 0, 1, 2, 1),
                 ('xz_2x2',) + rectangle((-1, 0, -1), 0, 2, 2, 2), ('yz_3x2',) + rectangle((0, -2, -1), 1, 2, 3, 2),
                 ('xy_3x3',) + rectangle((-4, -2, 0), 0, 1, 3, 3), ('xz_1x3',) + rectangle((2, 1, -2), 0, 2, 1, 3),
                 ('yz_2x2',) + rectangle((-3, -1, 0), 1, 2, 2, 2),
                 ('bent_xy_xz', [ORIGIN, (0, 1, 0), (1, 1, 0), (1, 0, 0), (1, 0, 1), (0, 0, 1), ORIGIN],
                  [(ORIGIN, (0, 1)), (ORIGIN, (0, 2))], [((0, 0, 1), (0, 1)), ((0, 1, 0), (0, 2)), (ORIGIN, (1, 2)), ((1, 0, 0), (1, 2))]),
                 ('tripod_hexagon', [(1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 1, 1), (0, 0, 1), (1, 0, 1), (1, 0, 0)],
                  [(ORIGIN, (0, 1)), (ORIGIN, (0, 2)), (ORIGIN, (1, 2))], [((0, 0, 1), (0, 1)), ((0, 1, 0), (0, 2)), ((1, 0, 0), (1, 2))])]
    q_bb2, cs_bb2 = P['bb2_q'], P['bb2_csite']
    eps40 = Q(1, 10 ** 40)
    loop_rows = {}
    for name, verts, flat, alt in loop_defs:
        trav = loop_links(verts)
        cset = chain_mod2([l for l, _ in trav])
        require(all(l in links2 for l, _ in trav) and all(links_of(f) <= links2 for f in flat + alt), 'loop outside the N=2 box: ' + name)
        require(surface_boundary(flat) == cset == surface_boundary(alt) and set(flat).isdisjoint(alt), 'surfaces do not bound ' + name)
        nE = sum(1 for l, _ in trav if in_E3(l))
        require(nE % 2 == len(flat) % 2 == len(alt) % 2, 'area parity differs from |C cap E_3| parity for ' + name)
        w = wilson_loop_su2(trav)
        require(wilson_loop_su2(trav, flip=in_E3) == (-1) ** nE * w and wilson_loop_su2(trav, gauge=quat_vertex) == w,
                'quaternion fixture fails for ' + name)
        Y = sorted({owner(l[0]) for l, _ in trav})
        m = max(max(abs(x) for x in y) for y in Y)
        N0 = max(2, m)
        eb = 1 / (1 - Q(len(Y), 10 ** 8))
        bound = [cs_bb2 * len(Y) * eb * q_bb2 ** (N - m) for N in range(N0, N0 + 8)]
        require(all(bound[i + 1] == q_bb2 * bound[i] for i in range(len(bound) - 1)), 'BB2 region bound is not geometric in N')
        Neps = N0
        while 2 * cs_bb2 * len(Y) * eb * q_bb2 ** (Neps - m) > eps40:
            Neps += 1
        loop_rows[name] = {'links': len(trav), 'area_flat': len(flat), 'area_alternative': len(alt), 'links_in_E3': nE,
                           'sign_(-1)^A': (-1) ** len(flat), 'W_C_fixture': s(w), 'region_Y_sites': len(Y), 'max_site_linf': m,
                           'bb2_bound_at_N0': s(bound[0]), 'bb2_bound_preview_at_N0': dec(bound[0]), 'N0': N0,
                           'N_where_twice_bound_below_1e-40': Neps}
    cube_sets = {'single_cube': [ORIGIN], 'bar_2x1x1': [ORIGIN, (1, 0, 0)], 'L_tromino': [ORIGIN, (1, 0, 0), (0, 1, 0)],
                 'block_2x2x2': [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)],
                 'ring_genus_one': [(x, y, 0) for x in (-1, 0, 1) for y in (-1, 0, 1) if (x, y) != (0, 0)]}
    closed_rows = {}
    for name, cubes in cube_sets.items():
        Zs = closed_surface_of_cubes(cubes)
        require(surface_boundary(Zs) == frozenset(), 'closed surface has a boundary')
        verts = {add(add(p, scale(UNIT[a], i)), scale(UNIT[cc], j)) for p, (a, cc) in Zs for i in (0, 1) for j in (0, 1)}
        edges = {l for f in Zs for l in face_links(f)}
        closed_rows[name] = {'plaquettes': len(Zs), 'euler_characteristic': len(verts) - len(edges) + len(Zs),
                             'sum_links_in_E3': sum(flip_count(f, in_E3) for f in Zs)}
        require(len(Zs) % 2 == 0 and closed_rows[name]['sum_links_in_E3'] % 2 == 0, 'odd closed surface')
    psi_fix = [Q(1, 3), Q(2, 3), Q(-2, 3), Q(0)]
    uY = [[Q(1), Q(0)], [Q(0), Q(-1)]]
    uO = [[Q(3, 5), Q(-4, 5)], [Q(4, 5), Q(3, 5)]]

    def reduced(ps):
        return [[sum((ps[2 * i + j] * ps[2 * k + j] for j in range(2)), Q(0)) for k in range(2)] for i in range(2)]
    Ups = [sum((uY[i][i2] * uO[j][j2] * psi_fix[2 * i2 + j2] for i2 in range(2) for j2 in range(2)), Q(0)) for i in range(2) for j in range(2)]
    rho0 = reduced(psi_fix)
    partial_ok = reduced(Ups) == [[sum((uY[i][a] * rho0[a][b] * uY[k][b] for a in range(2) for b in range(2)), Q(0)) for k in range(2)] for i in range(2)]
    centre_even_ok = all(RS[g]['W'][m] == 0 for g in flip_groups for m in range(0, ORDER + 1, 2)) and all(
        RS[g]['W2'][m] == 0 and RS[g]['C2'][m] == 0 for g in flip_groups for m in range(1, ORDER + 1, 2))
    check('area_parity_box_and_limit',
          partial_ok and centre_even_ok and all(r['area_flat'] % 2 == r['links_in_E3'] % 2 for r in loop_rows.values())
          and any(r['W_C_fixture'] != '0' for r in loop_rows.values()) and closed_rows['ring_genus_one']['euler_characteristic'] == 0
          and closed_rows['single_cube']['euler_characteristic'] == 2,
          statement='for SU(2) in the zero-selected family at kappa=0: omega_{N,-tau}(W_C) = (-1)^{A(C)} omega_{N,tau}(W_C) in every open centered whole-star box and every on-site cutoff (AW1 flip lemma, AM2 simple ground), and omega^{-tau}_inf(W_C) = (-1)^{A(C)} omega^{tau}_inf(W_C) for the limit of the named constructions (BB2 whole-sequence convergence on a finite complete-factor region containing the links of C, at each sign), for |tau| at most 10^-8, evaluated at tau=+-%s' % s(V['tau_corollary']),
          loops=loop_rows, closed_surfaces=closed_rows,
          proof_of_well_definedness='sum over plaquettes p of a Z_2 2-chain S of |p cap E_3| = |S| mod 2 (each plaquette meets E_3 oddly) and = |dS cap E_3| mod 2 (interior links counted twice); for a closed S this is 0, so every closed plaquette surface has an even number of plaquettes, and A(C) mod 2 = |C cap E_3| mod 2 for every spanning surface',
          limit_passage="rho^{F1,N}_Y(-tau) = U_{E cap Y} rho^{F1,N}_Y(tau) U_{E cap Y}^* for every N (U_E is a product over links); BB2 gives trace-norm convergence of both sequences with ||rho^{F1,N}_Y - rho^inf_Y||_1 at most c'_site |Y| e^{|Y|/10^8} q^{d_Y}; hence the identity holds for the limits",
          bb2_constants_read={"c'_site": s(cs_bb2), 'q': s(q_bb2), 'e_bound': 'e^x at most 1/(1-x) for x in [0,1) (directed)'},
          partial_trace_fixture=partial_ok, centre_even_one_plaquette_fixture=centre_even_ok,
          centre_even_statement='centre-even observables are even in tau: bounded ones (W_C^2, products with an even number of E-crossings) directly; link Casimirs through their bounded spectral cutoffs 1_[0,L](C_e) C_e, which commute with U_E, and the monotone limit L to infinity',
          gate_labels={'AW1': 'accepted_within_scope', 'BB2': 'accepted_within_scope, ' + str(P['bb2_sub_label'])},
          label='the loops, surfaces and quaternion values are exact finite audits of the identity; the statement is proved in report section 9')
    area_claims = [
        {'group': 'SU(2)', 'model': 'AQ_patterned_zero_selected', 'kappa': '0', 'region': 'open_centered_whole_star_box',
         'sign_rule': '(-1)^A(C)', 'basis': 'aw1_flip_lemma_and_am2_simple_ground'},
        {'group': 'SU(2)', 'model': 'AQ_patterned_zero_selected', 'kappa': '0', 'region': 'on_site_cutoff',
         'sign_rule': '(-1)^A(C)', 'basis': 'aw1_flip_lemma_and_am2_simple_ground'},
        {'group': 'SU(2)', 'model': 'AQ_patterned_zero_selected', 'kappa': '0', 'region': 'limit_of_named_constructions',
         'sign_rule': '(-1)^A(C)', 'basis': 'bb2_whole_sequence_convergence_each_sign'}]

    def validate_area_claim(cl):
        require(cl['group'] == 'SU(2)', 'area parity is claimed for SU(2) only')
        require(cl['model'] == 'AQ_patterned_zero_selected', 'area parity model')
        require(rat(cl['kappa']) == 0, 'area parity is claimed at kappa=0 only')
        require(cl['region'] in ('open_centered_whole_star_box', 'on_site_cutoff', 'limit_of_named_constructions'),
                'boundary condition outside the claim: ' + cl['region'])
        require(cl['sign_rule'] == '(-1)^A(C)', 'sign rule')
        if cl['region'] == 'limit_of_named_constructions':
            require(cl['basis'] == 'bb2_whole_sequence_convergence_each_sign', 'pointwise limit parity needs BB2 whole-sequence convergence')
        else:
            require(cl['basis'] == 'aw1_flip_lemma_and_am2_simple_ground', 'box parity basis')
        return True
    check('area_parity_scope',
          all(validate_area_claim(cl) for cl in area_claims)
          and rejected(lambda: validate_area_claim(dict(area_claims[0], region='periodic_box_odd_side')), 'periodic_box_with_odd_side')
          and rejected(lambda: validate_area_claim(dict(area_claims[0], kappa='1/100')), 'nonzero_selected_triple')
          and rejected(lambda: validate_area_claim(dict(area_claims[0], group='U(1)')), 'other_group')
          and rejected(lambda: validate_area_claim(dict(area_claims[0], region='F2_box')), 'F2_box')
          and rejected(lambda: validate_area_claim(dict(area_claims[0], region='literal_vertex_box')), 'literal_vertex_box')
          and rejected(lambda: validate_area_claim(dict(area_claims[2], basis='aw1_whole_set_of_subsequential_limits')),
                       'pointwise_limit_parity_from_subsequences')
          and rejected(lambda: validate_area_claim(dict(area_claims[0], sign_rule='(-1)^perimeter')), 'perimeter_sign_rule'),
          claims=area_claims)

    # -------------------- transfer ledger --------------------
    OBLIGATIONS = ['AM2 re-instantiation for the group (onsite gap 8 C_min per link, majorant, fixed point, gaps, cutoff removal)',
                   'AV1 product split and anchored-norm tier for the group', 'AQ1 construction and dynamics and the AQ2 gap for the group',
                   'BB1 comparisons and BB2 whole-sequence convergence for the group',
                   'a dictionary to a bare coupling for the group', 'a group-specific selected-strip reference if a nonzero triple is used']
    ledger = []
    for g in groups:
        models = ['H_FG(%s)' % g, 'H^%s_N' % g] + (['AQ_patterned_zero_selected'] if g == 'SU(2)' else [])
        row = {'group': g, 'equation': 'flip_lemma', 'models': models}
        if central[g] is not None:
            row.update(status='transfer_to_named_model', central_element=s(central[g]), counterexample=None,
                       reason=GR[g].centre_reason + '; U_E commutes with every Casimir, gauge action and cutoff projection, fixes the vacuum and reverses every W_f; flip sets verified'
                       + ('; for SU(2) this is the admitted AW1 lemma (H^SU(2)_N is the zero-selected box Hamiltonian)' if g == 'SU(2)' else ''))
        else:
            order = 4 if g == 'SU(5)' else 2
            row.update(status='obstruction_recorded', central_element=None, reason='reason: ' + GR[g].centre_reason,
                       counterexample={'quantity': 'order-%d coefficient of omega(W) on H_FG(%s)' % (order, g), 'order': order,
                                       'value': s(RS[g]['W'][order])})
        ledger.append(row)
        row = {'group': g, 'equation': 'parity_theorem', 'models': models, 'E_W3': s(E3[g])}
        if E3[g] == 0:
            row.update(status='transfer_to_named_model', counterexample=None,
                       reason='E[W^3]=0 exactly (every cubic moment E[chi^a conj(chi)^b], a+b=3, vanishes) with single-occurrence orthogonality')
        else:
            row.update(status='obstruction_recorded', reason='E[W^3]=%s is nonzero' % s(E3[g]),
                       counterexample={'quantity': 'first-order tau-derivative of omega(W^2) on H_FG(%s)' % g, 'order': 1, 'value': s(dW2[g])})
        ledger.append(row)
        ledger.append({'group': g, 'equation': 'first_order_coefficient', 'models': models, 'status': 'transfer_to_named_model',
                       'value': s(c1[g]), 'tier': 'exact_first_order', 'route_of_computation': ROUTE, 'counterexample': None,
                       'reason': "derived in the group's own cell: 2 (1/%d) E[W^2]/(%d C_F) with E[W^2]=%s and C_F=%s" % (md, ff, s(mom[g][1]), s(CF[g]))})
        ledger.append({'group': g, 'equation': 'dictionary', 'models': models,
                       'status': 'admitted_su2_reference' if g == 'SU(2)' else 'not_asserted', 'counterexample': None,
                       'reason': 'the admitted SU(2) dictionary (AZ1/AL1) is not re-derived here' if g == 'SU(2)' else
                       'no dictionary to a bare coupling is asserted for this group (obligation)'})
        ledger.append({'group': g, 'equation': 'am2_aq_chain', 'models': models,
                       'status': 'admitted_su2_reference' if g == 'SU(2)' else 'obligation', 'counterexample': None,
                       'obligations': [] if g == 'SU(2)' else list(OBLIGATIONS),
                       'reason': 'admitted for SU(2) only' if g == 'SU(2)' else 'not claimed; recorded as obligations'})

    def validate_flip_row(row):
        g = row['group']
        require(row['status'] in V['sub_labels'], 'flip status outside the allowed sub-labels')
        require(set(row['models']) <= {'H_FG(%s)' % g, 'H^%s_N' % g, 'AQ_patterned_zero_selected'}, 'flip models')
        if row['status'] == 'transfer_to_named_model':
            require(row.get('central_element') is not None and central[g] is not None and rat(row['central_element']) == central[g],
                    'flip transfer without an exhibited central -1: ' + g)
            require(g == 'SU(2)' or 'AQ_patterned_zero_selected' not in row['models'], 'AQ model for another group')
        else:
            require(central[g] is None, 'flip obstruction recorded for a group with a central -1')
            cx = row.get('counterexample')
            require(cx is not None and cx['order'] % 2 == 0 and rat(cx['value']) == RS[g]['W'][cx['order']] != 0,
                    'flip obstruction without the exact nonzero even-order coefficient: ' + g)
        return True

    def validate_parity_row(row):
        g = row['group']
        require('E_W3' in row, 'parity row without E[W^3]')
        require(rat(row['E_W3']) == E3[g], 'parity row E[W^3] differs')
        if row['status'] == 'transfer_to_named_model':
            require(E3[g] == 0, 'parity claimed with nonzero third moment: ' + g)
        else:
            require(E3[g] != 0 and row['counterexample'] is not None and rat(row['counterexample']['value']) == dW2[g] != 0,
                    'parity obstruction without a nonzero first-order derivative: ' + g)
        return True

    def ledger_rows(eq):
        return [r for r in ledger if r['equation'] == eq]
    check('flip_criterion_central_minus_one',
          all(validate_flip_row(r) for r in ledger_rows('flip_lemma'))
          and [r['group'] for r in ledger_rows('flip_lemma') if r['status'] == 'transfer_to_named_model'] == flip_groups
          and rejected(lambda: validate_flip_row(dict(ledger_rows('flip_lemma')[1], status='transfer_to_named_model')), 'SU3_flip_transfer')
          and rejected(lambda: validate_flip_row(dict(ledger_rows('flip_lemma')[3], counterexample=None)), 'SU5_obstruction_from_missing_centre_alone')
          and rejected(lambda: validate_flip_row(dict(ledger_rows('flip_lemma')[2], central_element=None)), 'SU4_transfer_without_central_element')
          and rejected(lambda: validate_flip_row(dict(ledger_rows('flip_lemma')[6], status='transfer_to_named_model', central_element='0')), 'SO3_flip_entry')
          and rejected(lambda: validate_flip_row(dict(ledger_rows('flip_lemma')[4], models=['H_FG(U(1))', 'AQ_patterned_zero_selected'])), 'U1_flip_on_the_AQ_model'),
          flip_transfer_groups=flip_groups, flip_obstruction_groups=nonflip_groups)
    check('parity_criterion_third_moment',
          all(validate_parity_row(r) for r in ledger_rows('parity_theorem'))
          and [r['group'] for r in ledger_rows('parity_theorem') if r['status'] == 'transfer_to_named_model'] == parity_groups
          and rejected(lambda: validate_parity_row(dict(ledger_rows('parity_theorem')[1], status='transfer_to_named_model')), 'SU3_parity_transfer')
          and rejected(lambda: validate_parity_row(dict(ledger_rows('parity_theorem')[3], status='obstruction_recorded', counterexample=None)),
                       'SU5_parity_merged_with_flip_column')
          and rejected(lambda: validate_parity_row({k: v for k, v in ledger_rows('parity_theorem')[4].items() if k != 'E_W3'}), 'U1_parity_without_third_moment'),
          parity_transfer_groups=parity_groups, parity_obstruction_groups=[g for g in groups if g not in parity_groups],
          separate_columns='SU(5): parity transfer without flip')

    # -------------------- value entries: labels, tiers, convention --------------------
    TIERED = ('first_order_coefficient', 'first_order_derivative_omega_W2', 'first_order_derivative_C_state', 'first_order_derivative_C_duhamel')
    UNTIERED = ('haar_moment', 'second_order_coefficient_omega_W', 'fourth_order_coefficient_omega_W')
    entries = []
    for g in groups:
        base = {'group': g, 'wilson_representation': V['wilson_rep'][g], 'model': 'H_FG(%s)' % g, 'tau': 'symbolic', V['route_field']: ROUTE}
        for k in range(1, KMAX + 1):
            entries.append(dict(base, kind='haar_moment', k=k, value=s(mom[g][k - 1])))
        entries.append(dict(base, kind='first_order_coefficient', value=s(c1[g]), tier='exact_first_order'))
        entries.append(dict(base, kind='first_order_derivative_omega_W2', value=s(dW2[g]), tier='exact_first_order'))
        entries.append(dict(base, kind='first_order_derivative_C_state', value=s(cstate[g]), tier='exact_first_order'))
        entries.append(dict(base, kind='first_order_derivative_C_duhamel', value=s(cduh[g]), tier='exact_first_order'))
        entries.append(dict(base, kind='second_order_coefficient_omega_W', value=s(c2[g])))
        entries.append(dict(base, kind='fourth_order_coefficient_omega_W', value=s(c4[g])))
        bbase = dict(base, model='H^%s_N' % g)
        entries.append(dict(bbase, kind='first_order_coefficient', value=s(box_terms[g]['first_order_coefficient_box']), tier='exact_first_order'))
        entries.append(dict(bbase, kind='first_order_derivative_omega_W2', value=s(box_terms[g]['d_omega_W2_dtau_box']), tier='exact_first_order'))

    def expected_value(e):
        g = e['group']
        return {'haar_moment': mom[g][e.get('k', 1) - 1], 'first_order_coefficient': c1[g], 'first_order_derivative_omega_W2': dW2[g],
                'first_order_derivative_C_state': cstate[g], 'first_order_derivative_C_duhamel': cduh[g],
                'second_order_coefficient_omega_W': c2[g], 'fourth_order_coefficient_omega_W': c4[g]}[e['kind']]

    def validate_tiers(es):
        for e in es:
            require(e.get(V['route_field']) in V['routes_allowed'], 'route_of_computation outside characters/weyl_integration')
            require('hypothesis_source' not in e, 'a hypothesis source attached to a BD1 value')
            require(not any(isinstance(x, str) and x in V['plan_route_labels'] for x in e.values()), 'a plan route label attached to a BD1 value')
            require(isinstance(e['value'], str), 'a non-exact value under a tier or route')
            rat(e['value'])
            if e['kind'] in TIERED:
                require(e.get('tier') in V['tier_names'], 'a first-order value without the exact_first_order tier')
            elif e['kind'] in UNTIERED:
                require('tier' not in e, 'a tier on a moment or on a higher-order coefficient')
            else:
                raise AdmissionError('unknown value kind')
        return True

    def validate_labels(e):
        g = e['group']
        require(g in groups, 'unknown group label')
        require(e['wilson_representation'] == V['wilson_rep'][g], 'Wilson representation relabelled')
        allowed = {'H_FG(%s)' % g, 'H^%s_N' % g}
        require(e['model'] in allowed, 'model label not allowed for ' + g + ': ' + e['model'])
        if e['kind'] in ('second_order_coefficient_omega_W', 'fourth_order_coefficient_omega_W'):
            require(e['model'] == 'H_FG(%s)' % g, 'a one-plaquette value presented as a box or limit value')
        require(e['tau'] == 'symbolic', 'group cells carry symbolic tau')
        require(rat(e['value']) == expected_value(e), "value differs from the group's own cell (relabelled value)")
        return True

    def find(g, kind, model=None):
        return [e for e in entries if e['group'] == g and e['kind'] == kind and (model is None or e['model'] == model)][0]
    check('tier_mixing_rejected',
          validate_tiers(entries)
          and rejected(lambda: validate_tiers([dict(find('U(1)', 'first_order_coefficient'), route_of_computation='weighted_norm')]), 'plan_route_label')
          and rejected(lambda: validate_tiers([dict(find('Z2', 'first_order_coefficient'), hypothesis_source='bb1_frozen_targets')]), 'hypothesis_source_attached')
          and rejected(lambda: validate_tiers([dict(find('SU(4)', 'first_order_coefficient'), value=1 / 2880)]), 'floating_value_under_tier')
          and rejected(lambda: validate_tiers([dict(find('SU(3)', 'haar_moment'), tier='exact_first_order')]), 'tier_on_a_moment')
          and rejected(lambda: validate_tiers([dict(find('SO(3)', 'second_order_coefficient_omega_W'), tier='exact_first_order')]), 'tier_on_second_order')
          and rejected(lambda: validate_tiers([dict(find('SU(5)', 'first_order_derivative_omega_W2'), route_of_computation='numerical')]), 'route_outside_two_labels')
          and rejected(lambda: validate_tiers([{k: v for k, v in find('SU(2)', 'first_order_coefficient').items() if k != 'tier'}]), 'first_order_value_without_tier'),
          entries=len(entries), tiered_kinds=list(TIERED), untiered_kinds=list(UNTIERED), plan_route_labels_rejected=V['plan_route_labels'])
    check('changed_model_relabelled',
          all(validate_labels(e) for e in entries)
          and rejected(lambda: validate_labels(dict(find('SU(3)', 'first_order_coefficient'), value=s(c1['SU(2)']))), 'SU2_value_under_SU3_label')
          and rejected(lambda: validate_labels(dict(find('SU(3)', 'second_order_coefficient_omega_W'), model='H^SU(3)_N')), 'one_plaquette_value_as_box_value')
          and rejected(lambda: validate_labels(dict(find('U(1)', 'first_order_coefficient', 'H^U(1)_N'), model='AQ_patterned_zero_selected')),
                       'group_box_value_under_SU2_family_label')
          and rejected(lambda: validate_labels(dict(find('Z2', 'first_order_coefficient'), value='1/6')), 'Z2_cell_other_normalization')
          and rejected(lambda: validate_labels(dict(find('SO(3)', 'first_order_coefficient'), wilson_representation='spin 1/2')), 'Wilson_representation_relabelled'),
          every_entry_names=['group', 'wilson_representation', 'model', 'tau'], models={g: ['H_FG(%s)' % g, 'H^%s_N' % g] for g in groups},
          su2_family_label='AQ_patterned_zero_selected is used only for the SU(2) area-parity corollary')

    def conv_cell(g):
        return {'group': g, 'C_F': s(CF[g]), 'face_energy': s(ff * CF[g]), 'link_term_on_F': s(lf * CF[g]),
                'magnetic_coefficient': '-tau/%d' % md, 'E_W2': s(mom[g][1]), 'first_order_coefficient': s(c1[g])}

    def validate_convention(cell):
        g = cell['group']
        require(rat(cell['C_F']) == CF_rule[g], 'Casimir normalization differs from the frozen convention for ' + g)
        require(rat(cell['link_term_on_F']) == lf * rat(cell['C_F']) and rat(cell['face_energy']) == ff * rat(cell['C_F']),
                'electric term is not 8 C_2 per link and 32 C_F per face')
        require(cell['magnetic_coefficient'] == '-tau/%d' % md, 'magnetic term differs from -(tau/3) W')
        require(rat(cell['E_W2']) == mom[g][1], "E[W^2] is not the group's own moment")
        require(rat(cell['first_order_coefficient']) == 2 * Q(1, md) * rat(cell['E_W2']) / rat(cell['face_energy']),
                'first-order coefficient not from the frozen formula')
        return True
    z2c = conv_cell('Z2')
    C_rej1 = V['z2_rejected_link_odd'] / lf                          # 'electric term 1 on the odd state'
    C_rej2 = Q(V['z2_rejected_sigma_offset'] + 1) / lf               # '1 - sigma^x' = 2 on the odd state
    check('frozen_convention_used',
          all(validate_convention(conv_cell(g)) for g in groups)
          and rejected(lambda: validate_convention(dict(z2c, C_F=s(C_rej1), link_term_on_F=s(lf * C_rej1), face_energy=s(ff * C_rej1),
                                                        first_order_coefficient=s(2 * Q(1, md) * mom['Z2'][1] / (ff * C_rej1)))), 'Z2_electric_1_on_odd')
          and rejected(lambda: validate_convention(dict(z2c, C_F=s(C_rej2), link_term_on_F=s(lf * C_rej2), face_energy=s(ff * C_rej2),
                                                        first_order_coefficient=s(2 * Q(1, md) * mom['Z2'][1] / (ff * C_rej2)))), 'Z2_one_minus_sigma_x')
          and rejected(lambda: validate_convention(dict(conv_cell('SU(3)'), C_F='8/3', link_term_on_F='64/3', face_energy='256/3',
                                                        first_order_coefficient=s(2 * Q(1, md) * mom['SU(3)'][1] / Q(256, 3)))), 'SU3_other_casimir_normalization')
          and rejected(lambda: validate_convention(dict(conv_cell('SU(4)'), face_energy=s(lf * CF['SU(4)']))), 'face_energy_8_C_F')
          and rejected(lambda: validate_convention(dict(conv_cell('U(1)'), first_order_coefficient=s(c1['SU(2)']))), 'SU2_value_copied_to_U1'),
          cells={g: conv_cell(g) for g in groups},
          rejected_z2_readings={'electric term 1 on the odd state': 'C_2(odd)=' + s(C_rej1) + ', c1=' + s(2 * Q(1, md) / (ff * C_rej1)),
                                '1 - sigma^x': 'C_2(odd)=' + s(C_rej2) + ', c1=' + s(2 * Q(1, md) / (ff * C_rej2))})

    def validate_no_su2_constants(rows, es):
        for e in es:
            if e['group'] != 'SU(2)':
                require(rat(e['value']) == expected_value(e), 'an SU(2) value used in another group cell')
                require('dictionary' not in e and 'source' not in e, 'dictionary or SU(2) source attached to ' + e['group'])
        for r in rows:
            if r['group'] != 'SU(2)' and r['equation'] == 'dictionary':
                require(r['status'] == 'not_asserted', 'a dictionary asserted for ' + r['group'])
            if r['group'] != 'SU(2)':
                txt = json.dumps(r)
                require('96/g^4' not in txt and 'g^2/(2a)' not in txt and '1/144' not in txt, 'SU(2) constant in a ' + r['group'] + ' row')
        return True
    di_u1 = [r for r in ledger if r['group'] == 'U(1)' and r['equation'] == 'dictionary'][0]
    check('su2_constants_not_transferred',
          validate_no_su2_constants(ledger, entries) and c1['SU(2)'] == Q(1, 144) and all(c1[g] != Q(1, 144) for g in groups if g != 'SU(2)')
          and rejected(lambda: validate_no_su2_constants([dict(di_u1, status='transfer_to_named_model', reason='tau=96/g^4')], []), 'U1_dictionary_tau_96_over_g4')
          and rejected(lambda: validate_no_su2_constants([], [dict(find('SU(4)', 'first_order_coefficient'), value='1/144')]), 'SU4_given_1_over_144')
          and rejected(lambda: validate_no_su2_constants([], [dict(find('SU(3)', 'first_order_coefficient'), dictionary='alpha=g^2/(2a)')]), 'SU3_alpha_dictionary'),
          su2_constants_read_only_to_reject_transfer=['1/144', P['su2_dictionary'], 'alpha=g^2/(2a)'],
          own_cell_values={g: s(c1[g]) for g in groups})

    def fg_cell(g):
        return {'group': g, 'model': 'H_FG(%s)' % g, 'hamiltonian': {'electric': '%d C_2' % ff, 'magnetic': '-tau/%d' % md},
                'free_reference': {'omega_W': s(RS[g]['W'][0]), 'omega_W2': s(RS[g]['W2'][0])}, 'model_is_finite_graph': True,
                'transfers_to_aq': False, 'value_scope': 'finite_model'}

    def validate_fg(cell):
        g = cell['group']
        require(cell['hamiltonian'] == {'electric': '%d C_2' % ff, 'magnetic': '-tau/%d' % md}, 'one-plaquette terms differ')
        require(cell['model_is_finite_graph'] is True and cell['transfers_to_aq'] is False, 'finite-graph labels')
        require(cell['value_scope'] == 'finite_model', 'a one-plaquette coefficient presented as a lattice-limit value')
        require(rat(cell['free_reference']['omega_W']) == mom[g][0] and rat(cell['free_reference']['omega_W2']) == mom[g][1],
                'free reference not computed in the same code path')
        return True
    check('one_plaquette_model_terms',
          all(validate_fg(fg_cell(g)) for g in groups) and P['aw1_coefficient_den'] == 144
          and rejected(lambda: validate_fg(dict(fg_cell('SU(3)'), transfers_to_aq=True)), 'transfers_to_aq_true')
          and rejected(lambda: validate_fg(dict(fg_cell('U(1)'), hamiltonian={'electric': '%d C_2' % lf, 'magnetic': '-tau/%d' % md})), 'per_link_electric_on_one_plaquette')
          and rejected(lambda: validate_fg(dict(fg_cell('Z2'), hamiltonian={'electric': '%d C_2' % ff, 'magnetic': '-tau'})), 'magnetic_minus_tau')
          and rejected(lambda: validate_fg(dict(fg_cell('SO(3)'), value_scope='lattice_limit')), 'one_plaquette_value_as_limit_value')
          and rejected(lambda: validate_fg(dict(fg_cell('SU(4)'), free_reference={'omega_W': '0', 'omega_W2': '1/4'})), 'free_reference_copied_from_SU2')
          and rejected(lambda: truncation_stable(RS['SU(3)'], RS_shallow), 'truncated_one_plaquette_series'),
          cells={g: fg_cell(g) for g in groups}, model_id=V['model_id'],
          labels={'model_is_finite_graph': True, 'transfers_to_aq': False, 'az2_gate_labels_match': True})

    # -------------------- ledger controls --------------------
    VERBS = ('pre' + 'dicts', 'con' + 'firms')

    def validate_ledger_text(rows):
        for r in rows:
            txt = json.dumps(r)
            for w in VERBS:
                require(re.search(r'(?<![\w])' + w + r'(?![\w])', txt, re.I) is None, 'a transfer or non-transfer described with a forbidden verb')
            if r['status'] == 'obstruction_recorded':
                require(r.get('counterexample') is not None and rat(r['counterexample']['value']) != 0, 'non-transfer without its exact counterexample')
        return True
    fl_su4 = ledger_rows('flip_lemma')[2]
    check('no_transfer_called_prediction',
          validate_ledger_text(ledger)
          and rejected(lambda: validate_ledger_text([dict(fl_su4, reason='the character count ' + VERBS[0] + ' the flip for SU(4)')]), 'transfer_text_with_forbidden_verb')
          and rejected(lambda: validate_ledger_text([dict(ledger_rows('parity_theorem')[1], counterexample=None)]), 'non_transfer_without_counterexample'),
          rows=len(ledger), statuses=sorted({r['status'] for r in ledger}))
    am2_allowed = {'flip_lemma', 'parity_theorem', 'first_order_coefficient'}

    def validate_am2(rows):
        for r in rows:
            if r['group'] == 'SU(2)':
                continue
            if r['equation'] == 'am2_aq_chain':
                require(r['status'] == 'obligation' and r['obligations'], 'an AM2, AV1 or AQ chain claimed for ' + r['group'])
            elif r['status'] == 'transfer_to_named_model':
                require(r['equation'] in am2_allowed, 'transfer beyond flip, parity and first order for ' + r['group'])
                require('AQ_patterned_zero_selected' not in r['models'], 'AQ model named for ' + r['group'])
        return True
    am_u1 = [r for r in ledger if r['group'] == 'U(1)' and r['equation'] == 'am2_aq_chain'][0]
    check('am2_not_reinstantiated',
          validate_am2(ledger)
          and rejected(lambda: validate_am2([dict(am_u1, status='transfer_to_named_model')]), 'U1_am2_chain_transfer')
          and rejected(lambda: validate_am2([{'group': 'Z2', 'equation': 'aq_limit_state', 'status': 'transfer_to_named_model', 'models': ['H^Z2_N']}]), 'Z2_aq_statement')
          and rejected(lambda: validate_am2([dict(am_u1, obligations=[])]), 'obligations_emptied'),
          obligations=OBLIGATIONS, u1_z2_transferred_equations=sorted(am2_allowed))

    # -------------------- scaling brackets --------------------
    t0 = V['tau_corollary']
    t1 = t0 / 100
    ratios = {'first_order_terms': {g: (c1[g] * t0) / (c1[g] * t1) for g in groups},
              'obstruction_second_order_terms': {g: (c2[g] * t0 ** 2) / (c2[g] * t1 ** 2) for g in ('SU(3)', 'SO(3)')},
              'su5_fourth_order_term': {'SU(5)': (c4['SU(5)'] * t0 ** 4) / (c4['SU(5)'] * t1 ** 4)},
              'moments': {g: mom[g][1] / mom[g][1] for g in groups}}

    def validate_scaling(rt, key):
        for r in rt.values():
            require(r == V['brackets'][key], 'scaling ratio outside the preregistered bracket ' + key)
        return True
    check('scaling_brackets',
          all(validate_scaling(ratios[k], k) for k in ratios)
          and rejected(lambda: validate_scaling(ratios['obstruction_second_order_terms'], 'first_order_terms'), 'second_order_term_relabelled_first_order')
          and rejected(lambda: validate_scaling(ratios['su5_fourth_order_term'], 'obstruction_second_order_terms'), 'fourth_order_term_relabelled_second_order'),
          ratios={k: {g: s(r) for g, r in v.items()} for k, v in ratios.items()}, tau=s(t0), tau_over_100=s(t1),
          brackets={k: s(x) for k, x in V['brackets'].items()})

    # -------------------- error ledger --------------------
    error_terms = {
        'moment_arithmetic': {'status': 'zero', 'reason': 'exact Fraction arithmetic on integer multiplicities; three character sub-routes agree exactly'},
        'character_multiplicities': {'status': 'zero', 'reason': 'exact integer multiplicities from Pieri, Clebsch-Gordan, charge counting and summation, cross-checked by tensor dimension counts on %d irreps and by closed-form Schur-Weyl/hook-length, charge, parity and Catalan counts' % sum(len(reach[g]) for g in groups)},
        'weyl_constant_terms': {'status': 'not_applicable', 'reason': 'Weyl integration is the reverse route; the forward-internal labelled cross-check computes integer constant terms exactly (divisible by the Weyl group order), zero error, never an admission value'},
        'one_plaquette_truncation': {'status': 'not_applicable', 'reason': 'the character-basis Rayleigh-Schroedinger algebra is exact: order m uses only the finite set of irreps reachable by m applications of W; depth-7 and depth-9 cutoffs give identical series through order 5'},
        'flip_set_enumeration': {'status': 'zero', 'reason': 'complete finite enumeration of every plaquette of the named boxes, factors and tori; the 24 residue classes with even-shift covariance cover all of Z^3'},
        'bb2_limit_passage': {'status': 'zero', 'reason': "the parity identity holds exactly at every N and each sign; the defect of the limits is at most 2 c'_site |Y| e^{|Y|/10^8} q^{d_Y} for every N (BB2 region form), which tends to 0"},
        'arithmetic': {'status': 'not_applicable', 'reason': 'no numeric cost: exact Fractions throughout; decimals are truncated previews'},
    }

    def validate_error_terms(et):
        require(sorted(et) == sorted(V['error_terms']), 'error terms differ from the preregistration')
        for k, v in et.items():
            require(v['status'] in ('zero', 'not_applicable', 'bounded') and len(v.get('reason', '')) > 20, 'error term without a stated reason: ' + k)
        return True
    check('error_terms_itemized',
          validate_error_terms(error_terms)
          and rejected(lambda: validate_error_terms(dict(error_terms, bb2_limit_passage={'status': 'not_applicable', 'reason': ''})), 'not_applicable_without_reason')
          and rejected(lambda: validate_error_terms({k: v for k, v in error_terms.items() if k != 'flip_set_enumeration'}), 'error_term_missing'),
          error_terms=error_terms, rule=V['error_terms_rule'])

    # -------------------- verdict, gate fields, template, texts --------------------
    outcomes = {'criterion_A_proved': True, 'criterion_B_proved': True,
                'obstruction_cells_exhibited': c2['SU(3)'] != 0 and c2['SO(3)'] != 0 and c4['SU(5)'] != 0,
                'groups_classified': flip_groups == [g for g in groups if central[g] is not None] and parity_groups == [g for g in groups if E3[g] == 0],
                'routes_agree_internally': True, 'flip_sets_verified': True, 'area_parity_box': True, 'area_parity_limit': True,
                'ledger_complete': len(ledger) == 5 * len(groups)}

    def expected_verdict(o):
        if not (o['criterion_A_proved'] and o['criterion_B_proved'] and o['obstruction_cells_exhibited']):
            return 'insufficient'
        if not all(o[k] for k in ('groups_classified', 'routes_agree_internally', 'flip_sets_verified', 'area_parity_box', 'area_parity_limit', 'ledger_complete')):
            return 'limited'
        return 'accepted_within_scope'

    def validate_verdict(claimed, o):
        require(claimed == expected_verdict(o), 'claimed verdict differs from the outcome-determined verdict')
        return True
    verdict = expected_verdict(outcomes)
    check('insufficient_verdict_retained',
          verdict == 'accepted_within_scope' and validate_verdict(verdict, outcomes)
          and expected_verdict(dict(outcomes, obstruction_cells_exhibited=False)) == 'insufficient'
          and expected_verdict(dict(outcomes, area_parity_limit=False)) == 'limited'
          and rejected(lambda: validate_verdict('accepted_within_scope', dict(outcomes, obstruction_cells_exhibited=False)), 'failed_cell_reported_accepted')
          and rejected(lambda: validate_verdict('accepted_within_scope', dict(outcomes, routes_agree_internally=False)), 'route_disagreement_reported_accepted')
          and rejected(lambda: validate_verdict('limited', dict(outcomes, criterion_B_proved=False)), 'unproved_criterion_reported_limited')
          and rejected(lambda: validate_convention(dict(conv_cell('SO(3)'), C_F='1', link_term_on_F='8', face_energy='32',
                                                        first_order_coefficient=s(2 * Q(1, md) * mom['SO(3)'][1] / 32))), 'convention_retuned_to_pass'),
          outcomes=outcomes, verdict=verdict, acceptance_read_from_contract=sorted(V['acceptance']))
    gate_fields = dict(V['gate_fields_required'])
    gate_groups = {'flip_transfer_groups': flip_groups, 'parity_transfer_groups': parity_groups,
                   'obstruction_groups': {'flip': nonflip_groups, 'parity': [g for g in groups if g not in parity_groups]},
                   'flip_transfer_scope_named': 'SU(2), SU(4), U(1), Z2 on H_FG(G) and the group-G whole-star box models H^G_N (operator identity in every box and cutoff; oddness of omega(W) in each box inside its Kato radius), flip sets verified; no AM2, AV1 or AQ statement for any group other than SU(2)'}

    def validate_gate_fields(gf, vd):
        if vd == 'accepted_within_scope':
            require(gf == V['gate_fields_required'], 'gate fields differ from gate_fields_required at accepted_within_scope')
        for k in ('uniqueness_of_ground_state_claimed', 'rate_in_a_claimed', 'continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified', 'transfers_to_aq'):
            require(gf[k] is False, 'gate field must be false: ' + k)
        return True
    report_path = BASE / 'report.md'
    require(report_path.is_file(), 'report.md missing')
    report_text = report_path.read_text()
    template = V['template']

    def validate_template(text):
        require(text.count(template) == 1, 'the mandatory template must appear once as one unbroken span')
        return True
    check('mandatory_sentence_and_gate_fields',
          validate_gate_fields(gate_fields, verdict) and validate_template(report_text)
          and rejected(lambda: validate_gate_fields(dict(gate_fields, area_parity_limit_claimed=False), 'accepted_within_scope'), 'gate_field_changed_at_accepted')
          and rejected(lambda: validate_gate_fields(dict(gate_fields, uniqueness_of_ground_state_claimed=True), 'limited'), 'uniqueness_field_true')
          and rejected(lambda: validate_template(report_text.replace(template, template.replace('; SU(3) and SO(3)', ';\nSU(3) and SO(3)'))), 'template_span_broken')
          and rejected(lambda: validate_template(report_text + '\n' + template + '\n'), 'template_quoted_twice'),
          gate_fields=gate_fields, gate_field_groups=gate_groups, template_sha256=sha_bytes(template.encode('utf-8')))
    statements = [template, gate_groups['flip_transfer_scope_named']] + [r['reason'] for r in ledger]
    forbidden_all = ROUND_FORBIDDEN + V['forbidden']
    check('placeholder_span_rejected',
          not placeholder_spans(report_text) and all(not placeholder_spans(x) for x in statements)
          and rejected(lambda: validate_text('The value is <value e.g. 1/144> here.', [], None, 'fixture'), 'angle_bracket_placeholder_with_e_g')
          and rejected(lambda: validate_text('Coefficient <c1 | c2>.', [], None, 'fixture'), 'angle_bracket_with_bar'),
          scanned=['report.md', 'supported statement and ledger reasons'])
    check('negation_aware_phrase_scan',
          validate_text(report_text, forbidden_all, template, 'report.md') and all(validate_text(x, forbidden_all, template, 'statement') for x in statements)
          and validate_text('This is not the thermodynamic limit.', forbidden_all, template, 'negated fixture')
          and rejected(lambda: validate_text('The character route ' + VERBS[0] + ' the SU(3) value.', forbidden_all, template, 'fixture'), 'affirmative_forbidden_verb')
          and rejected(lambda: validate_text('We study the thermodynamic limit.', forbidden_all, template, 'fixture'), 'affirmative_forbidden_phrase'),
          forbidden_phrase_count=len(forbidden_all), forbidden_list_sha256=sha_bytes(json.dumps(forbidden_all).encode('utf-8')),
          template_removed_as_one_literal=True)
    pm = V['raw_parameters']

    def validate_parameters(pp):
        for key in ('metric', 'weights', 'window', 'clock'):
            require(isinstance(pp.get(key), str) and pp[key], 'parameters field missing: ' + key)
            if pp[key].startswith('not applicable'):
                require(len(pp[key]) > len('not applicable') + 5, 'not applicable without its reason: ' + key)
        for key in ('d_X', 'N_0'):
            require(key not in pp, key + ' does not apply to BD1')
        return True
    check('parameters_declare_metric_weights_window',
          validate_parameters(pm)
          and rejected(lambda: validate_parameters({k: v for k, v in pm.items() if k != 'window'}), 'window_field_absent')
          and rejected(lambda: validate_parameters(dict(pm, weights='not applicable')), 'not_applicable_without_reason')
          and rejected(lambda: validate_parameters(dict(pm, d_X='1')), 'd_X_declared'),
          fields={k: pm[k] for k in ('metric', 'weights', 'window', 'clock')})
    forbidden_imports = ('mp' + 'math', 'num' + 'py', 'fl' + 'int', 'sym' + 'py', 'sci' + 'py')
    own = (BASE / 'check.py').read_text()
    imports = [ln for ln in own.splitlines() if ln.startswith('import ') or ln.startswith('from ')]
    check('exact_arithmetic_admission',
          not any(any(fb in ln for fb in forbidden_imports) for ln in imports)
          and rejected(lambda: rat(1 / 144), 'float_input') and rejected(lambda: rat(True), 'bool_input')
          and rejected(lambda: rat('NaN'), 'nan_input') and rejected(lambda: rat('1/0'), 'zero_denominator'),
          imports=imports, decimals='previews only, truncated from exact rationals')
    claim_flags = {'continuum_claim': False, 'weak_coupling_claim': False, 'scientific_priority_verified': False,
                   'uniqueness_of_ground_state_claimed': False, 'rate_in_a_claimed': False, 'uniform_wilson_claim': False,
                   'resolved_interaction_shift': False, 'am2_claim_for_other_groups': False, 'dictionary_for_other_groups': False,
                   'model_is_finite_graph': True, 'transfers_to_aq': False, 'flip_transfer_claimed': True, 'parity_transfer_claimed': True,
                   'obstructions_recorded': True, 'area_parity_limit_claimed': True}
    must_false = ('continuum_claim', 'weak_coupling_claim', 'scientific_priority_verified', 'uniqueness_of_ground_state_claimed',
                  'rate_in_a_claimed', 'uniform_wilson_claim', 'resolved_interaction_shift', 'am2_claim_for_other_groups',
                  'dictionary_for_other_groups', 'transfers_to_aq')

    def validate_flags(fl):
        for k in must_false:
            require(fl[k] is False, 'claim flag must be false: ' + k)
        return True
    check('no_priority_or_continuum_claim',
          validate_flags(claim_flags)
          and rejected(lambda: validate_flags(dict(claim_flags, continuum_claim=True)), 'continuum_claim_true')
          and rejected(lambda: validate_flags(dict(claim_flags, scientific_priority_verified=True)), 'priority_true')
          and rejected(lambda: validate_flags(dict(claim_flags, weak_coupling_claim=True)), 'weak_coupling_true'),
          historical_or_occult_numeric_premise=False, flags=claim_flags)

    # -------------------- premise inventory --------------------
    expected_inv = sorted(set(['AGENTS.md', CONTRACT_REL] + V['shared_premises']))
    inventory = {p.relative_to(BASE / 'inputs').as_posix(): sha(p) for p in sorted((BASE / 'inputs').rglob('*')) if p.is_file()}
    check('premise_inventory',
          sorted(inventory) == expected_inv and len(inventory) == 23 and not c.get('forward_additional_premises'),
          inputs=len(inventory), read_policy='only these snapshots; style references outside inputs: tools/README.md, tools/freeze.py, tools/phrase_scan.py, round32/forward/aw1/check.py (conventions only)',
          scratch=SCRATCH)

    # -------------------- assemble the packet --------------------
    headline = {
        'moment_table': {g: {str(k): s(mom[g][k - 1]) for k in range(1, KMAX + 1)} for g in groups},
        'moment_previews': {g: {str(k): dec(mom[g][k - 1], 8) for k in range(1, KMAX + 1)} for g in groups},
        'first_order_coefficients': {g: s(c1[g]) for g in groups},
        'first_order_previews': {g: dec(c1[g], 8) for g in groups},
        'obstruction_values': {'SU(3)': {'E_W3': s(E3['SU(3)']), 'd_omega_W2_dtau': s(dW2['SU(3)']), 'c2_omega_W': s(c2['SU(3)'])},
                               'SO(3)': {'E_W3': s(E3['SO(3)']), 'd_omega_W2_dtau': s(dW2['SO(3)']), 'c2_omega_W': s(c2['SO(3)'])},
                               'SU(5)': {'E_W3': s(E3['SU(5)']), 'd_omega_W2_dtau': s(dW2['SU(5)']), 'c2_omega_W': s(c2['SU(5)']),
                                         'c4_omega_W': s(c4['SU(5)']), 'c4_closed_form': '1/(2^30 3^10)'}},
        'flip_transfer_groups': flip_groups, 'parity_transfer_groups': parity_groups,
        'flip_set_counts': {'E3_boxes': box_rows, 'E3_factor_links_by_z_parity': e_by_parity, 'E3_plaquettes_meeting_each_factor': 52,
                            'E2_boxes': {N: n for N, n in e2_rows.items()}, 'tori_E3_even_seam': {k: v[1] for k, v in tori3.items()},
                            'tori_E2_even_seam': {k: v[1] for k, v in tori2.items()}},
        'area_parity': {'loops_checked': len(loop_rows), 'closed_surfaces_checked': len(closed_rows), 'corollary_tau': s(t0)},
    }
    packet = {
        'loop': LOOP, 'direction': 'forward', 'human_author': HUMAN_AUTHOR,
        'contribution_alias': 'HNM-BD1-F forward centre-symmetry transfer by characters: criteria A and B, exact moments and first-order coefficients, the SU(3), SO(3) and SU(5) obstruction cells, flip sets and the SU(2) area parity',
        'ai_assistance': 'AI-assisted forward production by a Claude model agent; correlated model-agent work, not independent human review',
        'contract_sha256': contract_digest, 'check_py_sha256_recorded_before_evaluation': check_sha,
        'admitted_gate_sha256': P['gate_sha256'], 'route_of_computation': ROUTE,
        'label': 'exact one-plaquette finite-graph values (H_FG(G), model_is_finite_graph true, transfers_to_aq false), exact first-order Taylor coefficients on the group-G whole-star box models (each box inside its Kato radius), and the SU(2) area parity in the zero-selected family through the admitted AW1 and BB2 statements; no AM2, AV1 or AQ statement for any group other than SU(2)',
        'model': {'model_id': V['model_id'], 'groups': groups, 'wilson_representations': V['wilson_rep'], 'tau': 'symbolic for the group cells; ' + s(t0) + ' for the SU(2) corollary',
                  'signs': V['signs'], 'selected_triple': ['0', '0', '0'], 'convention': {'per_link_electric': '%d C_2' % lf, 'face_energy': '%d C_F' % ff, 'magnetic': '-tau/%d' % md}},
        'headline': headline,
        'cells': {g: {'group': g, 'wilson_representation': V['wilson_rep'][g], 'C_F': s(CF[g]), 'moments': headline['moment_table'][g],
                      'first_order_coefficient': {'value': s(c1[g]), 'tier': 'exact_first_order', 'route_of_computation': ROUTE},
                      'first_order_derivative_omega_W2': {'value': s(dW2[g]), 'tier': 'exact_first_order', 'route_of_computation': ROUTE},
                      'second_order_coefficient_omega_W': {'value': s(c2[g]), 'route_of_computation': ROUTE},
                      'fourth_order_coefficient_omega_W': {'value': s(c4[g]), 'route_of_computation': ROUTE},
                      'central_minus_one': None if central[g] is None else s(central[g]), 'flip': cells_obs[g]['flip'], 'parity': cells_obs[g]['parity'],
                      'kato_radius_one_plaquette': s(kato[g]['one_plaquette']), 'model_is_finite_graph': True, 'transfers_to_aq': False}
                  for g in groups},
        'value_entries': entries,
        'transfer_ledger': ledger,
        'error_terms_itemized': error_terms,
        'scaling_ratios': {k: {g: s(r) for g, r in v.items()} for k, v in ratios.items()},
        'mandatory_sentence': template,
        'supported_statement': template,
        'gate_fields': gate_fields, 'gate_field_groups': gate_groups,
        'sub_labels': ['transfer_to_named_model', 'obstruction_recorded'],
        'exclusions': V['claim_exclusions'] + [x for x in V['prereg_exclusions'] if x not in V['claim_exclusions']],
        'proposed_forward_verdict': verdict + ' (forward route only; the gate also needs the reverse route and skeptical review)',
        'scratch_disclosure': SCRATCH + ' (private; prototypes and development runs only; none of it is evidence)',
    }
    packet.update(claim_flags)

    def packet_hash(pk):
        body = {k: v for k, v in pk.items() if k != 'packet_sha256'}
        return sha_bytes(json.dumps(body, sort_keys=True).encode('utf-8'))

    def validate_packet(pk, inv):
        require(pk.get('packet_sha256') == packet_hash(pk), 'packet hash mismatch')
        ids = {ch['id']: ch for ch in pk['checks']}
        for cid in V['controls']:
            if cid == 'coherent_evidence_tampering':
                continue
            require(cid in ids and ids[cid]['passed'] is True, 'required control missing or failed: ' + cid)
        validate_flags(pk)
        validate_gate_fields(pk['gate_fields'], verdict)
        require(sorted(inv) == expected_inv, 'premise snapshot inventory incomplete')
        for g in groups:
            for k in range(1, KMAX + 1):
                require(rat(pk['headline']['moment_table'][g][str(k)]) == mom[g][k - 1], 'moment differs from recomputation')
            require(rat(pk['headline']['first_order_coefficients'][g]) == c1[g], 'first-order coefficient differs from recomputation')
        ob = pk['headline']['obstruction_values']
        for g in ('SU(3)', 'SO(3)'):
            require(rat(ob[g]['c2_omega_W']) == c2[g] != 0 and rat(ob[g]['d_omega_W2_dtau']) == dW2[g] != 0, 'obstruction value differs')
        require(rat(ob['SU(5)']['c4_omega_W']) == c4['SU(5)'] != 0, 'SU(5) fourth-order value differs')
        require(pk['headline']['flip_transfer_groups'] == flip_groups and pk['headline']['parity_transfer_groups'] == parity_groups, 'classification differs')
        require(pk['headline']['flip_set_counts']['E3_boxes'] == box_rows, 'flip-set counts differ')
        return True
    base_packet = dict(packet)
    base_packet['checks'] = [dict(ch) for ch in CHECKS]
    base_packet['packet_sha256'] = packet_hash(base_packet)

    def tampered(edit, inv=None):
        pk = json.loads(json.dumps(base_packet))
        edit(pk)
        pk['packet_sha256'] = packet_hash(pk)
        return validate_packet(pk, inventory if inv is None else inv)

    def flip_control(pk):
        for ch in pk['checks']:
            if ch['id'] == 'su3_obstruction_mandatory':
                ch['passed'] = False
    inv_missing = dict(inventory)
    inv_missing.pop('research/round33/advisor/bb2-gate.json')
    check('coherent_evidence_tampering',
          validate_packet(base_packet, inventory)
          and rejected(lambda: tampered(flip_control), 'control_boolean_flipped_hash_rebound')
          and rejected(lambda: tampered(lambda pk: None, inv_missing), 'snapshot_removed_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk['headline']['moment_table']['SU(3)'].update({'3': '0'})), 'SU3_third_moment_zeroed_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk['headline']['first_order_coefficients'].update({'U(1)': '1/144'})), 'U1_coefficient_changed_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk['headline']['obstruction_values']['SU(5)'].update({'c4_omega_W': '0'})), 'SU5_fourth_order_zeroed_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk['headline'].update({'flip_transfer_groups': flip_groups + ['SU(3)']})), 'SU3_added_to_flip_groups_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk.update({'continuum_claim': True})), 'continuum_flag_hash_rebound')
          and rejected(lambda: tampered(lambda pk: pk['gate_fields'].update({'area_parity_limit_claimed': False})), 'gate_field_flipped_hash_rebound'),
          semantic_recomputation=['every moment', 'every first-order coefficient', 'the obstruction values', 'the classification', 'the flip-set counts', 'the gate fields', 'the claim flags', 'the premise inventory'])

    ids = [ch['id'] for ch in CHECKS]
    missing = [cid for cid in V['controls'] if cid not in ids]
    require(not missing, 'contract controls without a check: ' + ','.join(missing))
    no_mutation = [ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and not ch['mutations_rejected']]
    require(not no_mutation, 'contract controls without a damaging mutation: ' + ','.join(no_mutation))
    require(not PENDING_MUTATIONS, 'mutations evaluated outside a check')
    packet['checks'] = CHECKS
    packet['check_count'] = len(CHECKS)
    packet['contract_controls_covered'] = sorted(V['controls'])
    packet['controls_with_damaging_mutations'] = sorted(ch['id'] for ch in CHECKS if ch['id'] in V['controls'] and ch['mutations_rejected'])
    packet['damaging_mutation_count'] = sum(len(ch['mutations_rejected']) for ch in CHECKS)
    packet['control_to_check'] = {cid: cid for cid in V['controls']}
    text = json.dumps(packet, sort_keys=True)
    require(not placeholder_spans(text), 'placeholder span in results')
    require(not affirmative_hits(text, forbidden_all, template), 'affirmative forbidden phrasing in results: ' + json.dumps(affirmative_hits(text, forbidden_all, template)[:3]))
    return packet


def main():
    ap = argparse.ArgumentParser(description='BD1 forward exact checker (characters route)')
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
    manifest = {'loop': LOOP, 'direction': 'forward', 'contract_sha256': CONTRACT_SHA256, 'sources': sources,
                'outputs': {'results.json': sha(out / 'results.json')}}
    (out / 'source-manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'loop': LOOP, 'direction': 'forward', 'checks': len(result['checks']),
                      'damaging_mutations': result['damaging_mutation_count'],
                      'proposed_forward_verdict': result['proposed_forward_verdict']}, sort_keys=True))


if __name__ == '__main__':
    main()
