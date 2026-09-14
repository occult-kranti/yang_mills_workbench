#!/usr/bin/env python3
"""Exact R2 reverse controls for actual source, collars and inverse tails."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse
import ast
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT = ROOT / 'research/round22/contracts/r2.json'
CONTRACT_HASH = 'e6bd37712b4a561e332e61339da3f2d60b8cf2037c909016c9eeaebb857e4f93'
HELPER = ROOT / 'research/round22/reverse/r1/check.py'
HELPER_HASH = '26194dd48ebb6f7aeb7372dafe6a937e06352fb51d1a0ece4e323e955df5e372'
STAR = frozenset(((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)))


def need(ok, msg):
    if not ok:
        raise RuntimeError(msg)


def sha(path):
    for p in (path, *path.parents):
        need(not p.is_symlink(), 'symlink input')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, obj):
    path.write_text(json.dumps(obj, sort_keys=True, indent=2) + '\n')


def load_helper():
    need(sha(HELPER) == HELPER_HASH, 'immutable actual Haar helper changed')
    spec = importlib.util.spec_from_file_location('r1_reverse_haar_only', HELPER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def collar(y, n):
    return {tuple(x + d for x, d in zip(a, step)) for a in y
            for step in product(range(-n, n + 1), repeat=3)
            if all(x + d >= 0 for x, d in zip(a, step))}


def star(b):
    return {tuple(x + d for x, d in zip(b, s)) for s in STAR}


def meeting(y):
    return {tuple(x - d for x, d in zip(a, s)) for a in y for s in STAR
            if all(x - d >= 0 for x, d in zip(a, s))}


def collar_controls():
    rows = []
    fixtures = [('origin', {(0, 0, 0)}, range(5)),
                ('bulk', {(4, 4, 4)}, range(4)),
                ('connected_three', {(0, 0, 0), (1, 0, 0), (0, 1, 0)}, range(4))]
    for name, y, ns in fixtures:
        for n in ns:
            z, zz = collar(y, n), collar(y, n + 1)
            anchors = meeting(z)
            need(len(z) <= len(y) * (2 * n + 1) ** 3, 'general collar cover bound')
            need(len(anchors) <= 4 * len(z), 'every meeting anchor counted')
            need(all(star(b) & z and star(b) <= zz for b in anchors), 'one-collar propagation')
            if name == 'origin':
                need(len(z) == (n + 1) ** 3, 'positive-octant singleton collar')
                need(len(anchors) == len(z), 'origin incoming-boundary convention')
            if name == 'bulk':
                need(len(z) == (2 * n + 1) ** 3, 'bulk collar count')
            rows.append({'source': name, 'n': n, 'collar_size': len(z), 'meeting_stars': len(anchors)})
    origin = {(0, 0, 0)}
    need(len(collar(origin, 1)) == 8 != len(STAR), 'collar and one star are different declarations')
    center = {(1, 1, 1)}
    need(len(meeting(center)) == 4, 'form coefficient needs four incidences')
    finite = []
    for N in (0, 1, 2, 3):
        volume = collar(origin, N)
        for n in range(1, N + 1):
            aa = meeting(collar(origin, n - 1))
            need(all(star(b) <= volume for b in aa), 'all first N actions retained')
        next_anchors = meeting(collar(origin, N))
        missing = [b for b in next_anchors if not star(b) <= volume]
        need(bool(missing), 'mere containment must not imply next coefficient agrees')
        finite.append({'N': N, 'volume_size': len(volume),
                       'all_coefficients_through_N_match_geometrically': True,
                       'next_action_omitted_star_count': len(missing)})
    return {'passed': True, 'outcome': 'omitted crossing stars, incorrect octant count and premature coefficient matching rejected',
            'collars': rows, 'finite_volume_matching': finite,
            'initial_form_overlap_factor': 4, 'source_support_kept_complete': True}


def E(a, N):
    return a ** (N + 1) / (1 - a)


def T(a, N):
    g, c = 1 - a, 2 * N + 1
    return a ** (N + 1) * (F(c ** 3) / g + 6 * c * c * a / g ** 2
                            + 12 * c * a * (1 + a) / g ** 3
                            + 8 * a * (1 + 4 * a + a * a) / g ** 4)


def tail_controls():
    rows = []
    for a in (F(0), F(7, 2500), F(35, 416), F(1, 2)):
        for N in (0, 1, 4):
            e, t = E(a, N), T(a, N)
            geometric = sum((a ** n for n in range(N + 1, N + 21)), F(0))
            polynomial = sum(((2 * n - 1) ** 3 * a ** n for n in range(N + 1, N + 21)), F(0))
            need(e == geometric + E(a, N + 20), 'exact geometric tail decomposition')
            need(t == polynomial + T(a, N + 20), 'exact polynomial tail decomposition')
            need(t - T(a, N + 1) == (2 * N + 1) ** 3 * a ** (N + 1), 'graph tail index and coefficient')
            if a:
                wrong = (2 * N + 1) ** 3 * e
                need(t > wrong, 'frozen polynomial prefactor is not a graph-tail bound')
            else:
                need(e == t == 0, 'zero-coupling tails')
            if a in (F(0), F(35, 416)):
                rows.append({'a': str(a), 'N': N, 'E_N': str(e), 'T_N': str(t),
                             'finite_H_graph_error_over_r_sizeY': str(2 * t),
                             'finite_G_graph_error_over_r_sizeY': str(t)})
        need(T(a, 0) == a * (1 + 23 * a + 23 * a * a + a ** 3) / (1 - a) ** 4,
             'independent cubic generating numerator')
    need(28 * F(5, 1664) == F(35, 416), 'uniform required form endpoint')
    return {'passed': True, 'outcome': 'wrong geometric index and omitted graph-tail growth rejected; zero recovered',
            'evaluations': rows, 'H_graph_tail_sum': 'sum_(n>N)(2n-1)^3*a^n',
            'G_boundary_tail_same_sum': 'a*sum_(n>=N)(2n+1)^3*a^n',
            'global_operator_domain_equality_inferred': False}


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def plus(a, b):
    return [[x + y for x, y in zip(r, s)] for r, s in zip(a, b)]


def times(a, s):
    return [[x * s for x in row] for row in a]


def inv2(a):
    d = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    need(d != 0, 'singular exact fixture')
    return times([[a[1][1], -a[0][1]], [-a[1][0], a[0][0]]], 1 / d)


def norm2(v):
    return sum((row[0] ** 2 for row in v), F(0))


def neumann_controls():
    I = [[F(1), F(0)], [F(0), F(1)]]
    H = [[F(1), F(0)], [F(0), F(4)]]
    half = [[F(1), F(0)], [F(0), F(2)]]
    ih = inv2(half)
    h_inverse = inv2(H)
    v = [[F(1)], [F(0)]]
    rows = []
    for tau in (-F(1, 100), F(0), F(1, 100)):
        K = times([[F(1), F(1)], [F(1), F(-1)]], tau)
        D = mm(mm(half, K), half)
        G = plus(H, D)
        direct = inv2(G)
        sandwich = mm(mm(ih, inv2(plus(I, K))), ih)
        need(direct == sandwich, 'actual sandwiched plus inverse algebra')
        if tau:
            need(mm(H, D) != mm(D, H), 'fixture must discriminate commutation')
            wrong_sign = mm(mm(ih, inv2(plus(I, times(K, -1)))), ih)
            need(wrong_sign != direct, 'wrong Neumann sign')
            need(mm(h_inverse, inv2(plus(I, D))) != direct, 'incorrect inverse ordering')
        exact = mm(direct, v)
        partial = times(v, 0)
        z = mm(ih, v)
        previous = None
        aa = 2 * abs(tau)  # exact row-sum upper bound for this Hermitian K
        for n in range(7):
            coefficient = mm(ih, z)
            need(norm2(coefficient) <= aa ** (2 * n), 'coefficient geometric norm majorant')
            need(norm2(mm(half, coefficient)) <= aa ** (2 * n), 'coefficient half-energy majorant')
            if previous is not None:
                need(mm(H, coefficient) == times(mm(D, previous), -1), 'unsandwiched local recurrence')
            partial = plus(partial, coefficient)
            error = plus(exact, times(partial, -1))
            need(norm2(error) <= E(aa, n) ** 2, 'exact finite inverse tail')
            need(norm2(mm(half, error)) <= E(aa, n) ** 2, 'exact finite energy tail')
            previous = coefficient
            z = times(mm(K, z), -1)
        if tau == 0:
            need(partial == mm(h_inverse, v), 'bare inverse recovered exactly at zero')
        rows.append({'tau': str(tau), 'inverse_response': [str(x[0]) for x in exact],
                     'coefficient_and_tail_orders_checked': 7})
    return {'passed': True, 'outcome': 'opposite Neumann sign and unsandwiched ordering rejected',
            'scope': 'noncommuting finite algebra control only; not an SU2 Hamiltonian truncation', 'rows': rows}


def actual_controls(M):
    inherited = M.haar_geometry()
    need(inherited['sum_W_v_norm_squared'] == '21/4', 'actual 21-face variance')
    q2 = M.haar_moment((2, 0, 0, 0))
    mean = 2 * M.haar_moment((1, 0, 0, 0))
    chi2 = 4 * q2
    source_link, exterior_link = ((0, 0, 0), 2), ((4, 0, 0), 2)
    need(M.free(source_link) and M.free(exterior_link), 'both actual links are free z links')
    need(M.owner(source_link) == (0, 0, 0) and M.owner(exterior_link) == (1, 0, 0), 'actual exterior factor')
    need(mean == 0 and chi2 == 1, 'actual character orthonormality')
    # These four states are actual tensor products of Omega and normalized characters.
    # The matrices below restrict source operators only; G is never truncated to them.
    basis = [(0, 0), (0, 1), (1, 0), (1, 1)]
    local = [[F(int(a == 1 - c and b == d)) for c, d in basis] for a, b in basis]
    vacuum = [[F(int(a == 1 - c and b == d == 0)) for c, d in basis] for a, b in basis]
    eta = [[F(int(b == (0, 1)))] for b in basis]
    local_image, vacuum_image = mm(local, eta), mm(vacuum, eta)
    remainder = plus(local_image, times(vacuum_image, -1))
    need(norm2(vacuum_image) == 0, 'vacuum source kills excited exterior')
    need(norm2(local_image) == chi2 ** 2 == 1, 'local identity source remains nonzero')
    need(norm2(remainder) == 1, 'actual source-sector discrepancy')
    need(remainder == [[F(0)], [F(0)], [F(0)], [F(1)]], 'actual double-character output')
    need(8 * F(3, 4) == 6 and 2 * 8 * F(3, 4) == 12, 'physical reference energies')
    tau_rows = []
    for tau in (-F(5, 1664), F(0), F(5, 1664)):
        bare_amplitude = -tau / 18
        first_H_amplitude = tau / 18
        need(bare_amplitude + first_H_amplitude == 0, 'first response cancels actual boundary action')
        bare2 = F(21, 4) * bare_amplitude ** 2
        wrong2 = F(21, 4) * (2 * bare_amplitude) ** 2
        need(bare2 == F(7, 432) * tau ** 2, 'actual bare truncation error')
        need(wrong2 == F(7, 108) * tau ** 2, 'wrong first sign discrepancy')
        need((bare2 > 0 and wrong2 > 0) if tau else (bare2 == wrong2 == 0), 'coupling-sign and zero control')
        tau_rows.append({'tau': str(tau), 'bare_residual_squared': str(bare2),
                         'H_u1_squared': str(bare2), 'wrong_first_sign_H_error_squared': str(wrong2),
                         'source_sector_error_squared': '1'})
    return {'passed': True, 'outcome': 'actual omitted boundary and vacuum-projector-to-identity promotion rejected',
            'source_link': source_link, 'exterior_link': exterior_link,
            'actual_source_basis_is_SU2_character_states': True,
            'Hamiltonian_truncated_to_source_basis': False,
            'A_vac_eta_norm_squared': '0', 'A_local_eta_norm_squared': '1',
            'remaining_excited_exterior_operator': 'A_Y tensor Q_ext',
            'all_actual_faces': inherited['omitted_faces'],
            'all_Haar_cross_pairs': inherited['all_cross_pairs_checked'],
            'Haar_cross_pair_witness_sha256': inherited['cross_pair_witness_sha256'],
            'tau_rows': tau_rows, 'source_is_generated_O1_residual': False}


def weight_controls():
    tau = F(1, 10000)
    a = 28 * tau
    need(0 < tau < F(5, 1664), 'specified nonzero weight control in interval')
    terms = [F(2 ** ((n + 1) ** 3)) * a ** n for n in range(5)]
    ratios = [F(2 ** (3 * n * n + 9 * n + 7)) * a for n in range(4)]
    need(all(terms[n + 1] / terms[n] == ratios[n] for n in range(4)), 'exact volume ratio')
    need(terms[1] < terms[0] and terms[2] > terms[1], 'decreasing prefix must not certify the sum')
    need(all(ratios[n + 1] > ratios[n] for n in range(3)), 'volume ratio growth')
    need(all(a ** (n + 1) < a ** n for n in range(4)), 'unweighted majorants still decrease')
    need(8 * a < 1, 'different linear-volume declaration would change certificate')
    need((1 + 1) ** 3 != 1 + 3 * 1, 'collar support cannot be replaced by connected-word size')
    return {'passed': True, 'outcome': 'volume-weight convergence and shrinking-prefix inferences rejected',
            'mu': 'log(2)', 'tau': str(tau), 'a': str(a),
            'origin_collar_sizes': [(n + 1) ** 3 for n in range(5)],
            'weighted_upper_terms': [str(t) for t in terms],
            'successive_term_ratios': [str(t) for t in ratios],
            'general_log_summand': 'mu*(n+1)^3+n*log(a)+log(r)',
            'all_mu_positive_fixed_nonzero_tau_certificate': 'diverges',
            'zero_tau_weighted_sum_over_r': 'exp(mu*|Y|)', 'zero_source_sum': '0',
            'actual_response_norm_divergence_claimed': False,
            'all_regroupings_impossible_claimed': False,
            'local_rank_two_operator_series_norm_converges': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    out = Path(parser.parse_args().output).absolute()
    for p in (out, *out.parents):
        need(not p.is_symlink(), 'symlink output')
    need(not out.exists(), 'fresh output required')
    need(sha(CONTRACT) == CONTRACT_HASH, 'frozen R2 contract changed')
    contract = json.loads(CONTRACT.read_text())
    for rel, digest in contract['dependencies'].items():
        need(sha(ROOT / rel) == digest, 'changed inherited dependency: ' + rel)
    need(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse((HERE / 'check.py').read_text()))),
         'removable assertion in checker')
    rejected = False
    try:
        need(False, 'deliberate rejecting control')
    except RuntimeError:
        rejected = True
    need(rejected, 'explicit false condition must reject')
    M = load_helper()
    controls = {'schema': 'ym22-reverse-r2-controls-v1', 'loop': 'r2', 'direction': 'reverse',
                'status': 'passed', 'passed': True, 'collars_and_boundaries': collar_controls(),
                'explicit_tails': tail_controls(), 'noncommuting_inverse': neumann_controls(),
                'actual_SU2_source_sectors': actual_controls(M), 'volume_weight': weight_controls(),
                'disabled_assertions': {'passed': True, 'outcome': 'false condition rejected by RuntimeError; no AST Assert'}}
    results = {'schema': 'ym22-reverse-r2-results-v1', 'loop': 'r2', 'direction': 'reverse',
               'status': 'proved_initial_vacuum_response_with_graph_tails_and_scoped_weight_failure', 'passed': True,
               'claims': {'infinite_initial_form_constructed': True, 'form_coefficient': 'a=28*abs(tau)',
                          'initial_G_gap': 'g=1-a>=381/416',
                          'sandwiched_inverse': 'H^(-1/2)*(I+K)^(-1)*H^(-1/2) on Q',
                          'K_norm_upper': 'a', 'coefficient_support': 'Y^(n)',
                          'coefficient_norm_and_half_energy_upper': 'r*a^n',
                          'coefficient_H_graph_upper_n_ge_1': 'r*|Y|*(2n-1)^3*a^n',
                          'response_Hilbert_and_half_energy_tail': 'r*E_N(a)',
                          'response_H_graph_tail': 'r*|Y|*T_N(a)',
                          'response_G_graph_tail': 'r*|Y|*(2N+1)^3*a^(N+1)',
                          'E_N': 'a^(N+1)/(1-a)',
                          'T_N': 'a^(N+1)*[c^3/g+6*c^2*a/g^2+12*c*a*(1+a)/g^3+8*a*(1+4*a+a^2)/g^4], c=2N+1',
                          'response_in_DH_and_DG': True, 'global_DG_equals_DH_claimed': False,
                          'finite_volume_condition': 'Y^(N) subset Lambda',
                          'finite_norm_and_half_energy_error': '2*r*E_N(a)',
                          'finite_H_graph_error': '2*r*|Y|*T_N(a)',
                          'finite_G_graph_error': 'r*|Y|*T_N(a)',
                          'vacuum_rank_two_cancellation': 'A_Y tensor P_ext',
                          'remaining_local_source_operator': 'A_Y tensor Q_ext',
                          'actual_excited_exterior_error_squared': '1',
                          'actual_bare_response_residual_squared': '7*tau^2/432',
                          'actual_wrong_first_sign_H_error_squared': '7*tau^2/108',
                          'local_rank_two_creator_norm_series_converges': True,
                          'local_creator_identified_with_global_vacuum_generator': False,
                          'origin_collar_volume': '(n+1)^3',
                          'positive_volume_weight_upper_certificate': 'diverges for r>0 and fixed nonzero tau',
                          'actual_weighted_norm_divergence_claimed': False,
                          'all_stage_iteration_or_full_homogeneous_gap_proved': False,
                          'Q2_transfer_or_continuum_claimed': False,
                          'source_is_generated_O1_residual': False},
               'target_verdict': 'Boundary-complete initial response and graph convergence proved; source-sector promotion and specified volume-weight certificate fail.',
               'research_loop_position': 10, 'next_loop_selected': False}
    rels = list(contract['dependencies']) + contract['instruction_inputs'] + [
        'research/round22/reverse/r1/report.md', 'research/round22/reverse/r1/source-review.json',
        'research/round22/reverse/r1/output/source-manifest.json',
        'research/round22/reverse/o2/report.md',
        'research/round22/reverse/n1/inputs/advisor-finite-observations.md',
        'research/round22/reverse/n1/inputs/paired-admission-matching.md']
    inputs = [CONTRACT, HELPER, HERE / 'check.py', HERE / 'report.md', HERE / 'independence.json',
              HERE / 'source-review.json'] + [ROOT / rel for rel in rels]
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in sorted(set(inputs))}
    need(all(rel in hashes for rel in contract['instruction_inputs']), 'complete immutable instruction closure')
    out.mkdir(parents=True)
    for name, obj in [('results.json', results), ('controls.json', controls)]:
        dump(out / name, obj)
    dump(out / 'source-manifest.json', {'schema': 'ym22-source-manifest-v1', 'inputs': hashes,
                                      'outputs': {name: sha(out / name) for name in ('results.json', 'controls.json')}})
    print(json.dumps({'loop': 'r2', 'direction': 'reverse', 'status': results['status'], 'passed': True}))


if __name__ == '__main__':
    main()
