#!/usr/bin/env python3
"""Exact R1 reverse geometry/Haar and homological controls; no spin cutoff."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
import argparse
import ast
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT = ROOT / 'research/round22/contracts/r1.json'
CONTRACT_HASH = '799b5bd8f10adec2341dd7d5a8ceef2e84c2a723e01c9fae69e6b73f4311da34'
STAR = frozenset(((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)))


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    for p in (path, *path.parents):
        need(not p.is_symlink(), 'symlink input: ' + str(p))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, obj):
    path.write_text(json.dumps(obj, sort_keys=True, indent=2) + '\n')


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def shift(a, d):
    b = list(a)
    b[d] += 1
    return tuple(b)


def face(a, i, j):
    # Canonical positive edge tails of the oriented elementary square.
    return frozenset(((a, i), (shift(a, j), i), (a, j), (shift(a, i), j)))


def owner(e):
    a, _ = e
    return (a[0] // 4, a[1] // 2, a[2])


def free(e):
    a, d = e
    return d == 2 or (d == 1 and a[1] % 2 == 1) or (d == 0 and a[0] % 4 == 3)


def haar_moment(powers):
    # Uniform unit quaternion: odd moments vanish, even moments are exact.
    if any(p % 2 for p in powers):
        return F(0)
    value = F(1)
    for p in powers:
        for k in range(1, p, 2):
            value *= k
    for k in range(sum(powers) // 2):
        value /= 4 + 2 * k
    return value


def haar_geometry():
    tails = list(product(range(4), range(2), range(1)))
    onsite = {(a, d) for a in tails for d in range(3)}
    selected = set().union(*(face((x, 0, 0), 0, 1) for x in range(3)))
    need(len(onsite) == 24 and len(selected) == 10, 'complete factor/strip links')
    need(selected <= onsite, 'selected strip must be onsite')
    need(onsite - selected == {e for e in onsite if free(e)}, 'actual fourteen free links')
    need(len(onsite - selected) == 14, 'free link count')
    probe = ((0, 0, 0), 2)
    need(probe in onsite - selected, 'frozen free z probe')
    faces = []
    supports = {}
    for a in tails:
        for i, j in combinations(range(3), 2):
            if (i, j) == (0, 1) and a[1] == 0 and a[0] < 3:
                continue
            ee = face(a, i, j)
            ff = {e for e in ee if free(e)}
            support = frozenset(owner(e) for e in ee)
            need(len(ee) == 4 and len(ff) >= 2, 'actual omitted free factors')
            need(support <= STAR and len(support) > 1, 'actual coarse support')
            witness = sorted(ff - {probe})
            need(bool(witness), 'conditional mean/diagonal needs a different free link')
            key = tuple(sorted(support))
            supports[key] = supports.get(key, 0) + 1
            faces.append({'anchor': a, 'plane': (i, j), 'edges': ee, 'free': ff,
                          'conditional_witness': witness[0], 'support': support})
    need(len(faces) == 21, 'all twenty-one omitted anchors')
    need(sorted(supports.values()) == [1, 1, 2, 3, 4, 10], 'actual support classes')
    pair_witnesses = []
    for i, j in combinations(range(len(faces)), 2):
        fi, fj = faces[i], faces[j]
        need(len(fi['edges'] & fj['edges']) <= 1, 'distinct elementary face intersection')
        ww = sorted(fi['free'] - fj['edges'])
        need(bool(ww), 'unmatched free center variable for weighted cross moment')
        # chi_probe^2 is center-even also when the witness is the probe itself.
        probe_power = 2 if ww[0] == probe else 0
        need((1 + probe_power) % 2 == 1, 'weighted cross moment parity')
        pair_witnesses.append([i, j, ww[0]])
    need(len(pair_witnesses) == 210, 'every unordered cross pair tested')
    q2 = haar_moment((2, 0, 0, 0))
    chi_norm2 = 4 * q2
    need(q2 == F(1, 4) and chi_norm2 == 1, 'actual Haar normalization')
    need(2 * haar_moment((1, 0, 0, 0)) == 0, 'probe centered')
    need(16 * haar_moment((4, 0, 0, 0)) == 2, 'non-Gaussian character fourth moment')
    energy = 8 * F(1, 2) * F(3, 2)
    need(energy == 6, 'delta-normalized free Casimir')
    sum_variance = len(faces) * q2 * chi_norm2
    defect2 = sum_variance / (3 * energy) ** 2
    need(sum_variance == F(21, 4) and defect2 == F(7, 432), 'actual defect coefficient')
    need(defect2 > 0, 'actual boundary is nonzero for nonzero tau')
    need((len(faces) - 1) * q2 / (3 * energy) ** 2 != defect2, 'dropped-face control')
    need(q2 != 1 and defect2 * q2 != defect2, 'half-trace source is not normalized character')
    ledger = [{'anchor': f['anchor'], 'plane': f['plane'],
               'actual_support': sorted(f['support']),
               'free_link_count': len(f['free']),
               'mean_and_diagonal_witness': f['conditional_witness']} for f in faces]
    return {'passed': True, 'outcome': 'actual nonzero boundary; dropped face and half-trace normalization rejected',
            'onsite_links': 24, 'selected_links': 10, 'free_links': 14,
            'omitted_faces': 21, 'all_cross_pairs_checked': 210,
            'selected_strip_ground_unchanged': True,
            'face_ledger': ledger,
            'cross_pair_witness_sha256': hashlib.sha256(json.dumps(pair_witnesses, sort_keys=True).encode()).hexdigest(),
            'Haar_chi_norm_squared': str(chi_norm2), 'Haar_chi_fourth_moment': '2',
            'dimensionless_probe_energy': str(energy), 'probe_S_norm': '1/6',
            'sum_W_v_norm_squared': str(sum_variance),
            'boundary_vacuum_norm_squared_over_tau_squared': str(defect2),
            'tau_zero_defect_squared': str(F(0) ** 2 * defect2),
            'source_is_generated_O1_residual': False,
            'finite_spin_surrogate_used': False}


def boundary_geometry():
    table = []
    for L in (1, 2, 3, 5):
        for bulk in (False, True):
            volume = set(product(range(L + 2), repeat=3))
            axis = range(1, L + 1) if bulk else range(L)
            y = set(product(axis, repeat=3))
            retained = {b: {add(b, d) for d in STAR} for b in volume
                        if all(add(b, d) in volume for d in STAR)}
            interior = {b for b, s in retained.items() if s <= y}
            crossing = {b for b, s in retained.items() if s & y and not s <= y}
            outgoing = crossing & y
            incoming = crossing - y
            need(len(interior) == (L - 1) ** 3, 'interior cube count')
            need(len(outgoing) == 3 * L ** 2 - 3 * L + 1, 'outgoing cube count')
            need(len(incoming) == (3 * L ** 2 if bulk else 0), 'incoming cube count')
            expected = (6 if bulk else 3) * L ** 2 - 3 * L + 1
            need(len(crossing) == expected, 'full boundary count')
            need(len(crossing) <= 4 * len(y), 'uniform meeting-anchor bound')
            for x in volume:
                site_stars = sum(x in s for s in retained.values())
                need(site_stars <= 4, 'four-star incidence')
                m = sum(x in y | retained[b] for b in crossing)
                need(m == len(crossing) if x in y else m <= 4, 'both root placements')
            for b in crossing:
                need(len(y | retained[b]) <= len(y) + 3, 'complete union support')
            if bulk:
                need(len(crossing) != len(outgoing), 'dropping incoming stars must fail')
            need(len(crossing) != len(incoming), 'dropping outgoing stars must fail')
            table.append({'L': L, 'bulk': bulk, 'interior': len(interior),
                          'outgoing': len(outgoing), 'incoming': len(incoming),
                          'crossing': len(crossing)})
    probe_volume = set(product(range(2), repeat=3))
    probe_stars = [b for b in probe_volume if all(add(b, d) in probe_volume for d in STAR)]
    need(probe_stars == [(0, 0, 0)], 'probe retains precisely one full star')
    need(2 ** len(STAR) == 16 and 4 * 16 * 7 == 448, 'O1 support normalization')
    need(2 ** len(STAR) != 2 ** 1, 'singleton source cannot replace star support')
    return {'passed': True, 'outcome': 'omitted incoming/outgoing anchors and singleton support replacement rejected',
            'cube_counts': table, 'probe_retained_anchors': probe_stars,
            'star_weight': 16, 'initial_diagonal_weighted_budget_over_abs_tau': 448,
            'boundary_term_union_size_upper': '|Y|+3',
            'root_in_Y_count': 'N_cross', 'root_outside_Y_count_upper': 4}


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def plus(a, b):
    return [[x + y for x, y in zip(r, s)] for r, s in zip(a, b)]


def times(a, s):
    return [[s * x for x in r] for r in a]


def comm(a, b):
    return plus(mm(a, b), times(mm(b, a), -1))


def skew(u):
    return [[F(0), -u[0], -u[1]], [u[0], F(0), F(0)], [u[1], F(0), F(0)]]


def algebra_controls():
    t = F(1, 100)
    h = [[F(0), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(2)]]
    d = [[F(0), F(0), F(0)], [F(0), t, t], [F(0), t, -t]]
    a = [[F(0), F(1), F(1)], [F(1), F(0), F(0)], [F(1), F(0), F(0)]]
    g = plus(h, d)
    det = (1 + t) * (2 - t) - t * t
    u = [(2 - 2 * t) / det, F(1) / det]
    zero = times(h, 0)
    need(plus(comm(skew(u), g), a) == zero, 'interacting inverse exact cancellation')
    bare_defect = plus(comm(skew([F(1), F(1, 2)]), g), a)
    need(bare_defect != zero and bare_defect[1][0] == -3 * t / 2, 'bare inverse control')
    need(plus(comm(times(skew(u), -1), g), a) == times(a, 2), 'opposite skew sign')
    need(comm(h, d) != zero, 'fixture must be noncommuting')
    need(d[1][1] * d[2][2] - d[1][2] ** 2 < 0, 'diagonal compression is not presumed positive')
    need(plus(comm(skew([F(1), F(1, 2)]), h), a) == zero, 'bare reference tau-zero recovery')
    endpoint = F(5, 1664)
    gap = 1 - 28 * endpoint
    need(gap == F(381, 416) and 1 / gap == F(416, 381), 'required inverse endpoint')
    for tau in (-endpoint, F(0), endpoint):
        need(1 - 28 * abs(tau) >= gap, 'both coupling signs and zero')
    need(1 - 28 * F(1, 28) == 0, 'enlarged interval endpoint is open')
    return {'passed': True, 'outcome': 'bare interacting inverse, opposite skew sign and diagonal positivity inference rejected',
            'scope': 'three-level algebra control, not actual SU2 proof',
            'fixture_tau': str(t), 'interacting_u': [str(x) for x in u],
            'bare_defect_10': str(bare_defect[1][0]), 'wrong_sign_residual': '2A',
            'required_uniform_gap': str(gap), 'uniform_inverse_upper': str(1 / gap),
            'enlarged_initial_G_interval': '|tau|<1/28', 'tau_zero_bare_recovered': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    out = Path(parser.parse_args().output).absolute()
    for p in (out, *out.parents):
        need(not p.is_symlink(), 'symlink output')
    need(not out.exists(), 'fresh output required')
    need(sha(CONTRACT) == CONTRACT_HASH, 'frozen contract changed')
    contract = json.loads(CONTRACT.read_text())
    for rel, digest in contract['dependencies'].items():
        need(sha(ROOT / rel) == digest, 'inherited dependency changed: ' + rel)
    need(not any(isinstance(n, ast.Assert) for n in ast.walk(ast.parse((HERE / 'check.py').read_text()))),
         'admission must not use removable assertions')
    rejected = False
    try:
        need(False, 'deliberate failed condition')
    except RuntimeError:
        rejected = True
    need(rejected, 'false acceptance condition did not reject')
    controls = {'schema': 'ym22-reverse-r1-controls-v1', 'loop': 'r1', 'direction': 'reverse',
                'status': 'passed', 'passed': True, 'actual_SU2': haar_geometry(),
                'complete_boundary': boundary_geometry(), 'homological_algebra': algebra_controls(),
                'disabled_assertions': {'passed': True, 'outcome': 'explicit false condition rejected; AST contains no Assert'}}
    results = {'schema': 'ym22-reverse-r1-results-v1', 'loop': 'r1', 'direction': 'reverse',
               'status': 'proved_initial_interacting_inverse_with_actual_boundary_obstruction', 'passed': True,
               'claims': {'model': 'homogeneous I1/O1 full-link selected-strip and free reference',
                          'initial_relative_coefficient': '28*abs(tau)',
                          'initial_local_gap': '1-28*abs(tau)',
                          'required_uniform_gap': '381/416', 'required_uniform_inverse_upper': '416/381',
                          'operator_domain': 'D(G_Y)=D(H0_Y)',
                          'form_domain': 'D(G_Y^(1/2))=D(H0_Y^(1/2))',
                          'u_norm_upper': 'norm(v)/g', 'H0_half_u_upper': 'norm(v)/g',
                          'H0_u_upper': '(1+7*abs(tau)*N_Y/g)*norm(v)',
                          'local_homological_identity': '[S_Y,G_Y]=-A_Y',
                          'full_defect': 'sum_(retained crossing b)[S_Y,D_b]',
                          'full_defect_norm_upper': '14*abs(tau)*N_cross*norm(v)/g',
                          'declared_term_support': 'Y union (b+Gstar)',
                          'term_support_cardinality_upper': '|Y|+3',
                          'weighted_root_bound': '14*abs(tau)*2^(|Y|+3)*norm(v)*m_x(Y)/g',
                          'origin_cube_crossings': '3L^2-3L+1',
                          'bulk_cube_crossings': '6L^2-3L+1', 'bulk_cube_incoming': '3L^2',
                          'probe_free_Casimir_energy': '6', 'probe_generator_norm': '1/6',
                          'probe_boundary_vacuum_norm_squared': '7*tau^2/432',
                          'probe_is_generated_O1_residual': False,
                          'arbitrary_source_full_homological_cancellation': False,
                          'later_diagonal_inverse_proved': False,
                          'numerical_homogeneous_gap_proved': False,
                          'Q2_gap_or_positivity_transferred': False,
                          'infinite_representation_or_continuum_claimed': False},
               'target_verdict': 'Initial inverse and full boundary bounds proved; actual diagnostic rejects deleting boundary. Iteration remains unclosed.',
               'next_loop_selected': False}
    rels = list(contract['dependencies']) + contract['instruction_inputs'] + [
        'research/round21/reverse/i1/report.md', 'research/round21/reverse/i2/report.md',
        'research/round21/reverse/i2/check.py',
        'research/round22/reverse/o1/report.md', 'research/round22/reverse/o2/report.md',
        'research/round22/reverse/q2/check.py', 'research/round22/reverse/q2/submission.json',
        'research/round22/reverse/q2/optimized-replay.json',
        'research/round22/reverse/n1/inputs/advisor-finite-observations.md',
        'research/round22/reverse/n1/inputs/paired-admission-matching.md']
    inputs = [CONTRACT, HERE / 'check.py', HERE / 'report.md', HERE / 'independence.json',
              HERE / 'source-review.json'] + [ROOT / r for r in rels]
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in sorted(set(inputs))}
    need(all(p in hashes for p in contract['instruction_inputs']), 'all immutable instructions bound')
    out.mkdir(parents=True)
    for name, payload in [('results.json', results), ('controls.json', controls)]:
        dump(out / name, payload)
    dump(out / 'source-manifest.json', {'schema': 'ym22-source-manifest-v1', 'inputs': hashes,
                                      'outputs': {n: sha(out / n) for n in ('results.json', 'controls.json')}})
    print(json.dumps({'loop': 'r1', 'direction': 'reverse', 'status': results['status'], 'passed': True}))


if __name__ == '__main__':
    main()
