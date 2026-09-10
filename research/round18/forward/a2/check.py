"""Exact finite ledgers check the implementation of an all-volume analytic bound."""
import argparse
import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import summable


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

    evidence = summable.collection()
    check('complete fixed graph and parameter inventory replays', summable.verify_collection(evidence))
    cases = {f['id']: f['certificate'] for f in evidence['fixtures']}
    volumes = []
    for n in range(2, 10):
        g = evidence['graphs'][str(n)]
        c = cases[f'volume_{n}']
        if (len(g['vertices']), len(g['edges']), len(g['faces'])) != (n**3, 3*(n-1)*n*n, 3*n*(n-1)**2):
            raise RuntimeError('actual box counts disagree')
        if c['cluster_count'] != n*(n//4)*(n//2):
            raise RuntimeError('cluster count formula failed')
        occupied = set()
        for block in c['clusters']:
            if len(block['edges']) != 10 or occupied.intersection(block['edges']):
                raise RuntimeError('ten-link cluster overlap')
            occupied.update(block['edges'])
        for row in c['face_ledger']:
            if row['kind'] == 'remaining':
                face = next(f for f in g['faces'] if f['id'] == row['face'])
                if row['untouched_link'] in occupied or row['untouched_link'] not in {term['edge'] for term in face['word']}:
                    raise RuntimeError('actual untouched-link witness failed')
        if len(occupied)+len(c['reference_free_links']) != len(g['edges']):
            raise RuntimeError('an electric link was lost')
        sums = summable.weight_formulas(n)
        if not 0 <= sums['remaining'] <= sums['total'] < 1:
            raise RuntimeError('positive orthant bound failed')
        homogeneous_count = c['remaining_face_count']
        volumes.append({'n': n, 'vertices': len(g['vertices']), 'links': len(g['edges']), 'faces': len(g['faces']),
            'clusters': c['cluster_count'], 'remaining_faces': homogeneous_count,
            'remaining_weight': c['remaining_face_weight'], 'finite_gap_lower': c['finite_gap_lower'],
            'uniform_common_gap_lower': c['common_gap_lower'], 'generic_uniform_lower': c['generic_uniform_bound_at_alpha'],
            'full_support': c['actual_full_face_support'],
            'homogeneous_remainder_norm_budget': str(F(homogeneous_count, 64)),
            'homogeneous_finite_comparison': str(F(1, 8)-F(homogeneous_count, 64))})
    check('all eight actual box counts and cluster counts agree with their formulas', len(volumes) == 8)
    check('every sampled cluster has ten disjoint links and all electric links remain', True)
    check('every sampled remaining face has an actual link outside all clusters', True)
    check('finite ledgers obey the safe positive orthant bound', True)
    check('small boxes without clusters use a conservative consequence of the free gap',
          all(cases[f'volume_{n}']['reference_is_pure_free']
              and cases[f'volume_{n}']['pure_free_gap_if_no_clusters'] == '3/4'
              and cases[f'volume_{n}']['reference_gap_lower_used'] == '1/8' for n in (2, 3)))
    check('complete and incomplete strip boundaries are covered',
          [cases[f'volume_{n}']['cluster_count'] for n in (4, 5, 6, 7, 8, 9)] == [8, 10, 18, 21, 64, 72])
    check('the all-orientation infinite orthant sum is exactly one', F(3*2**3, 24) == 1)
    check('primary improved and generic uniform bounds have correct coefficients',
          F(1, 8)-F(1, 64) == F(7, 64) and F(1, 8)-2*F(1, 64) == F(3, 32))
    check('every canonical volume fixture has full actual-face support',
          all(cases[f'volume_{n}']['actual_full_face_support'] for n in range(2, 10)))
    check('signed remainder uses its absolute norm budget',
          cases['negative_tau']['finite_gap_lower'] == cases['volume_5']['finite_gap_lower'])
    check('signed nonzero cluster coefficients retain full support and the common lower bound',
          cases['signed_cluster']['actual_full_face_support'] and cases['signed_cluster']['common_gap_lower'] == '7/64')
    check('zero remainder is valid but not full support',
          cases['tau_zero']['common_gap_lower'] == '1/8' and not cases['tau_zero']['actual_full_face_support'])
    check('zero selected coefficient is valid but blocks full-support classification',
          not cases['zero_cluster_coefficient']['actual_full_face_support'])
    endpoint = cases['tau_boundary']
    check('uniform zero estimate remains insufficient while its finite estimate is positive',
          endpoint['uniform_bound_status'] == 'zero-insufficient' and endpoint['common_gap_lower'] == '0'
          and endpoint['finite_bound_status'] == 'positive' and endpoint['finite_ground_Gauss_inclusion_certified'])
    check('nonunit scales preserve instance scaling and separate common normalization',
          F(cases['scaled_double']['finite_gap_lower']) == 2*F(cases['volume_4']['finite_gap_lower'])
          and F(cases['scaled_half']['finite_gap_lower']) == F(cases['volume_4']['finite_gap_lower'])/2
          and cases['scaled_double']['common_gap_lower'] == '7/64'
          and cases['scaled_half']['common_gap_lower'] == '7/256')
    parameters = cases['volume_4']['parameters'].copy()
    parameters['tau'] = '1/4'
    negative = summable.certify(evidence['graphs']['4'], parameters)
    check('negative uniform coefficient never becomes an alpha-min common bound',
          negative['uniform_bound_status'] == 'negative-insufficient' and negative['common_gap_lower'] is None)
    gate = evidence['nonzero_homogeneous_remainder_gate']
    check('nonzero homogeneous remainder is rejected as uniformly summable',
          gate['status'].startswith('blocked') and gate['dimensionless_norm_upper'] is None)
    check('the number of untouched vertical-face remainder terms grows without a fixed budget',
          all(row['remaining_faces'] >= 2*row['n']*(row['n']-1)**2 for row in volumes)
          and volumes[-1]['homogeneous_finite_comparison'].startswith('-'))
    check('zero homogeneous coefficients are the trivial summable exception',
          summable.schedule_gate('homogeneous', '0')['dimensionless_norm_upper'] == '0')
    reclass = evidence['boundary_reclassification']
    check('an existing boundary face changes coefficient when its full strip later fits',
          reclass == [{'n': 6, 'face': 'f2:4,0,0', 'kind': 'remaining', 'physical_coefficient': '1/24576'},
                      {'n': 8, 'face': 'f2:4,0,0', 'kind': 'cluster', 'physical_coefficient': '1/2'}]
          and not evidence['finite_volume_family_is_nested_restriction'])
    large = 10**9
    check('arbitrary-size lazy count and first anchor do not materialize a box',
          summable.cluster_count(large) == large*(large//4)*(large//2)
          and next(summable.anchors(large)) == (0, 0, 0))
    check('arbitrary-size witness rules preserve incomplete-block cases',
          summable.untouched_witness(large+2, 2, (large, 0, 0)) == f'e0:{large},0,0'
          and summable.untouched_witness(large+2, 2, (0, 1, 0)) == 'e1:0,1,0'
          and summable.untouched_witness(large+2, 0, (0, 0, 0)) == 'e2:0,0,0')
    for name, mutate in [
        ('generic two-norm formula substituted for improved bound', lambda c: c.update(uniform_bound_at_alpha=c['generic_uniform_bound_at_alpha'])),
        ('uniform limit substituted for proved orthant upper bound', lambda c: c.update(orthant_weight_upper='107/135')),
        ('remaining face coefficient omitted', lambda c: c['face_ledger'].pop()),
        ('unknown free-link expectation fabricated', lambda c: c.update(reference_remainder_expectation='not computed'))]:
        c = copy.deepcopy(cases['volume_4'])
        mutate(c)
        reject(name, lambda c=c: summable.verify(evidence['graphs']['4'], c))
    bad = copy.deepcopy(evidence['graphs']['4'])
    bad['faces'][0]['word'][0]['sign'] *= -1
    reject('altered signed face word', lambda: summable.certify(bad, cases['volume_4']['parameters']))
    reject('unbounded materialized cluster list', lambda: summable.materialized_clusters(large))
    reject('unbounded full graph allocation', lambda: summable.make_graph(large))
    reject('unbounded rational exponent allocation', lambda: summable.geometric_sum(large))
    reject('Boolean extent alias', lambda: summable.cluster_count(True))
    reject('Boolean face coordinate alias', lambda: summable.untouched_witness(4, 2, (False, 0, 0)))
    reject('negative face coordinate', lambda: summable.untouched_witness(4, 2, (-1, 0, 0)))
    reject('Boolean normal alias', lambda: summable.untouched_witness(4, True, (0, 0, 0)))
    for name, key, value in [('Boolean ratio', 'tau', False), ('missing common scale', 'alpha_min', '0'),
                             ('too large common lower scale', 'alpha_min', '2'),
                             ('cluster outside accepted bridge interval', 'bridge_ratio', '1/4')]:
        parameters = cases['volume_4']['parameters'].copy()
        parameters[key] = value
        reject(name, lambda parameters=parameters: summable.certify(evidence['graphs']['4'], parameters))
    c = copy.deepcopy(evidence)
    c['fixtures'].pop()
    reject('required scale fixture removed', lambda: summable.verify_collection(c))
    (out/'collection.json').write_text(json.dumps(evidence, indent=2)+'\n')
    with (out/'volume.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(volumes[0]))
        writer.writeheader()
        writer.writerows(volumes)
    (out/'beyond-uniform-control.json').write_text(json.dumps(negative, indent=2)+'\n')
    result = {'schema': 'ym18-a2-results-v1', 'status': 'passed', 'checks_count': len(checks), 'checks': checks,
              'source_sha256': summable.SOURCE_SHA, 'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'evidence_sha256': hashlib.sha256((out/'collection.json').read_bytes()).hexdigest(),
              'primary_uniform_common_lower': '7/64', 'primary_generic_lower': '3/32',
              'volume_fixture_count': 8, 'parameter_fixture_count': len(evidence['fixtures']),
              'scope': 'Full-support spatially decaying finite-volume family with a proved all-volume lower bound; not homogeneous dense Yang-Mills or a thermodynamic spectral construction'}
    (out/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    (out/'manifest.json').write_text(json.dumps({'schema': 'ym18-a2-output-manifest-v1',
        'files': {name: hashlib.sha256((out/name).read_bytes()).hexdigest() for name in
                  ['collection.json', 'volume.csv', 'beyond-uniform-control.json', 'results.json']}}, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'checks'}, indent=2))


if __name__ == '__main__':
    main()
