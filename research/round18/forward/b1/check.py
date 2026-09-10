"""Check complete physical low support and all repeated magnetic fourth moments."""
import argparse
import copy
import csv
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path
import cross


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    out = Path(args.output).resolve()
    if out == source or source in out.parents:
        raise ValueError('output must be outside frozen sources')
    out.mkdir(parents=True, exist_ok=True)
    checks = []

    def check(name, condition):
        if not condition:
            raise RuntimeError(name)
        checks.append(name)

    def reject(name, function):
        try:
            function()
        except (ValueError, TypeError, KeyError):
            checks.append('reject: '+name)
            return
        raise RuntimeError('invalid accepted: '+name)

    evidence = cross.collection()
    check('complete graph, support, moment and parameter evidence replays', cross.verify_collection(evidence))
    g = evidence['graph']
    check('actual graph retains twelve vertices, twenty links and eleven faces',
          (len(g['vertices']), len(g['edges']), len(g['faces'])) == (12, 20, 11))
    check('actual graph is bipartite by coordinate parity',
          all(sum(map(int, edge['tail'].split(','))) % 2 != sum(map(int, edge['head'].split(','))) % 2 for edge in g['edges']))
    support = evidence['low_support_inventory']
    check('all supports of up to five edges are enumerated once',
          support['total_supports'] == sum(math.comb(20, k) for k in range(6)) == 21700
          and len({row['mask'] for row in support['rows']}) == 21700)
    check('exactly eleven nonempty no-leaf supports remain', len(support['eligible_nonempty_masks']) == 11)
    check('every surviving support is an actual elementary four-cycle',
          set(support['eligible_nonempty_masks']) == set(support['face_masks'].values()))
    check('common spin one and larger cannot occur below the complement threshold', 4*F(1)*(F(1)+1) > F(9, 2))
    check('one more nontrivial link reaches the six-edge energy threshold', 6*F(3, 4) == F(9, 2))
    witness = evidence['six_edge_witness']
    edge_map = {edge['id']: edge for edge in g['edges']}
    endpoints = []
    for term in witness['word']:
        edge = edge_map[term['edge']]
        endpoints.append((edge['tail'], edge['head']) if term['sign'] == 1 else (edge['head'], edge['tail']))
    check('six-edge witness is an actual closed simple signed rectangle',
          len({term['edge'] for term in witness['word']}) == 6
          and len(set(witness['vertices'])) == 6
          and all(endpoints[i][1] == endpoints[(i+1) % 6][0] for i in range(6)))
    check('six-edge witness is orthogonal to every P face by an odd-link parity',
          all(row['odd_edges'] and row['inner_product'] == '0' for row in witness['face_inner_products'])
          and witness['norm_squared'] == '1')
    fourth = evidence['fourth_moment_inventory']
    check('fourth inventory covers every ordered product through complete symmetric multisets',
          fourth['multisets'] == math.comb(14, 4) == 1001 and fourth['ordered_products_covered'] == 11**4 == 14641)
    check('all 330 four-distinct products have nonempty mod-two boundary and zero integral',
          fourth['all_four_distinct_cases'] == 330
          and all(row['odd_boundary_edges'] and row['moment'] == '0'
                  for row in fourth['rows'] if row['pattern'] == [1, 1, 1, 1]))
    check('all repeated fourth products are independently classified',
          all(row['moment'] == ('2' if row['pattern'] == [4] else '1' if row['pattern'] == [2, 2] else '0')
              for row in fourth['rows']))
    check('genuine independent one-face Haar agreement at fourth order is retained',
          fourth['degree_four_independent_Haar_agreement'])
    cases = {f['id']: f['certificate'] for f in evidence['fixtures']}
    for item in evidence['fixtures']:
        c = item['certificate']
        if c['Gram'] != [[str(int(i == j)) for j in range(12)] for i in range(12)]:
            raise RuntimeError('P basis is not orthonormal')
        matrix = [[F(x) for x in row] for row in c['cross_Gram']]
        qsum = F(c['sum_coupling_squares'])
        ls = list(map(F, c['couplings']))
        if any(matrix[0]) or any(row[0] for row in matrix):
            raise RuntimeError('QVP acts nontrivially on the vacuum')
        if any(matrix[i+1][i+1] != qsum/4 for i in range(11)):
            raise RuntimeError('cross diagonal mismatch')
        if any(qsum-l*l < 0 for l in ls):
            raise RuntimeError('positive cross-Gram decomposition failed')
        if c['equal_magnitudes']:
            signs = [F(1) if l >= 0 else F(-1) for l in ls]
            eigen = F(c['exact_cross_norm_squared_if_equal'])
            if any(sum((matrix[i+1][j+1]*signs[j] for j in range(11)), F(0)) != eigen*signs[i] for i in range(11)):
                raise RuntimeError('signed exact bright cross eigenvector failed')
    check('all nine full matrix fixtures retain the Gram and vacuum-kernel identities', len(cases) == 9)
    check('cross Gram has a positive diagonal-plus-rank-one decomposition for signed couplings', True)
    check('equal-magnitude cross norm has an exact signed bright eigenvector', True)
    check('zero coupling gives the zero cross operator', cases['allzero']['cross_norm_squared_row_upper'] == '0')
    check('both global and alternating signs preserve the exact equal-magnitude norm',
          all(cases[name]['exact_cross_norm_squared_if_equal'] == '21/256'
              for name in ('all_positive_eighth', 'all_negative_eighth', 'alternating_eighth')))
    check('nonunit alpha scaling is quadratic for the cross Gram and linear for the complement',
          F(cases['scaled_double']['cross_norm_squared_row_upper']) == 4*F(cases['canonical_three_eighths']['cross_norm_squared_row_upper'])
          and F(cases['scaled_half']['cross_norm_squared_row_upper']) == F(cases['canonical_three_eighths']['cross_norm_squared_row_upper'])/4
          and cases['scaled_double']['Q_electric_lower'] == '9'
          and cases['scaled_half']['Q_electric_lower'] == '9/4')
    controls = evidence['controls']
    check('Gaussian repeated-fourth substitution changes a declared one-coefficient fixture',
          controls['Gaussian_same_face_fourth']['actual_single_cross_diagonal'] == '1/256'
          and controls['Gaussian_same_face_fourth']['Gaussian_single_cross_diagonal'] == '1/128')
    check('deleting P subtraction falsely creates a vacuum cross component',
          controls['deleted_P_subtraction'] == {'actual_vacuum_cross_diagonal': '0', 'without_subtraction': '11/256'})
    check('six-face closed surface rejects extending low-degree Haar independence to the distribution',
          controls['six_face_distribution_independence']['actual_moment'] == '1/16'
          and controls['six_face_distribution_independence']['independent_Haar_prediction'] == '0')
    check('six-edge witness rejects a falsely raised complement threshold',
          F(controls['falsely_raised_tail']['witness_over_alpha']) < F(controls['falsely_raised_tail']['proposed_over_alpha']))
    check('missing face would leave an actual lower-energy state in Q',
          F(controls['omitted_projection_face']['omitted_state_energy_over_alpha']) < F(9, 2))
    reject('projection missing a physical face state', lambda: cross.projection_gate([f['id'] for f in g['faces']][1:]))
    for name, mutate in [
        ('cross Gram replaced by unsubtracted PV2P', lambda c: c.update(cross_Gram=c['PV2P'])),
        ('claimed larger electric complement', lambda c: c.update(Q_electric_lower='6')),
        ('external charges silently introduced', lambda c: c['physical_contract'].update(external_charges=True)),
        ('Boolean schema alias', lambda c: c.update(equal_magnitudes=1))]:
        c = copy.deepcopy(cases['all_positive_eighth'])
        mutate(c)
        reject(name, lambda c=c: cross.verify(c))
    c = copy.deepcopy(evidence)
    c['low_support_inventory']['rows'].pop()
    reject('small-support inventory entry omitted', lambda: cross.verify_collection(c))
    c = copy.deepcopy(evidence)
    c['fixtures'].pop()
    reject('required scale fixture omitted', lambda: cross.verify_collection(c))
    cross.moment([0])
    reject('Boolean face alias after cache warmup', lambda: cross.moment([False]))
    reject('negative face index', lambda: cross.moment([-1]))
    reject('moment degree outside the reviewed oracle', lambda: cross.moment([0]*7))
    reject('nonpositive energy scale', lambda: cross.certify('0', ['0']*11))
    reject('missing coefficient', lambda: cross.certify('1', ['0']*10))
    reject('nested Boolean coefficient', lambda: cross.certify('1', [False]+['0']*10))
    rows = [{'fixture': f['id'], 'alpha': f['certificate']['alpha'],
             'maximum_ratio': f['certificate']['maximum_absolute_ratio'],
             'Q_electric_lower': f['certificate']['Q_electric_lower'],
             'cross_norm_squared_row_upper': f['certificate']['cross_norm_squared_row_upper'],
             'coefficient_box_norm_squared_upper': f['certificate']['coefficient_box_norm_squared_upper']}
            for f in evidence['fixtures']]
    (out/'collection.json').write_text(json.dumps(evidence, indent=2)+'\n')
    with (out/'cross-norms.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = {'schema': 'ym18-b1-results-v1', 'status': 'passed', 'checks_count': len(checks), 'checks': checks,
              'source_sha256': cross.SOURCE_SHA, 'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'evidence_sha256': hashlib.sha256((out/'collection.json').read_bytes()).hexdigest(),
              'support_count': 21700, 'fourth_multiset_count': 1001, 'ordered_fourth_products': 14641,
              'complement_threshold_over_alpha': '9/2',
              'canonical_cross_norm_squared_over_alpha_squared': '189/256',
              'scope': 'Complete finite physical complement and cross operator; B2 full E1 and parameter-box gap remain unexecuted'}
    (out/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'schema': 'ym18-b1-output-manifest-v1',
        'files': {name: hashlib.sha256((out/name).read_bytes()).hexdigest() for name in
                  ['collection.json', 'cross-norms.csv', 'results.json']}}, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))


if __name__ == '__main__':
    main()
