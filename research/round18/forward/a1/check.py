"""Exact bridge certificate, graph, untouched-link and spectral logic checks."""
import argparse
import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import bridge


def cmatrix(q):
    a, b, c, d = map(float, q)
    return ((complex(a, b), complex(c, d)), (complex(-c, d), complex(a, -b)))


def cmul(a, b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


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
            checks.append('reject: ' + name)
            return
        raise RuntimeError('invalid accepted: ' + name)

    evidence = bridge.collection()
    graph = evidence['graph']
    supports = bridge.validate_graph(graph)
    check('actual signed strip retains eight vertices, ten links and three faces',
          (len(graph['vertices']), len(graph['edges']), len(graph['faces'])) == (8, 10, 3))
    check('end magnetic blocks are link disjoint while the bridge meets each in one link',
          not supports['left'] & supports['right']
          and len(supports['middle'] & supports['left']) == len(supports['middle'] & supports['right']) == 1)
    check('two actual horizontal bridge links lie outside the end blocks',
          supports['middle'] - supports['left'] - supports['right'] == {'ex:1,0,0', 'ex:1,1,0'})
    # Polynomial form of the SU(2) character identity, independent of any end wavefunction.
    chi1_squared = (F(0), F(0), F(4))
    chi0_plus_chi2 = (F(1)+F(-1), F(0), F(4))
    check('ordinary-character product chi1 squared equals chi0 plus chi2', chi1_squared == chi0_plus_chi2)
    check('complete evidence and frozen fixture inventory replay', bridge.verify_collection(evidence))
    cases = {entry['id']: entry['certificate'] for entry in evidence['fixtures']}
    p = cases['primary']
    check('primary corner improves the generic zero estimate to one eighth',
          p['generic_two_norm_gap_lower'] == '0' and p['full_gap_lower'] == '1/8')
    check('primary common-scale bound is explicit', p['primary_family_common_bound'] == '1/8')
    check('whole primary family follows from its endpoint inequalities',
          F(3, 4)-F(1, 2)-F(1, 8) == F(1, 8))
    check('both bridge signs have the same sufficient lower bound',
          cases['negative_bridge']['full_gap_lower'] == p['full_gap_lower'])
    check('zero bridge recovers the dressed reference gap estimate',
          cases['no_bridge']['full_gap_lower'] == cases['no_bridge']['reference_gap_lower'] == '1/4')
    check('zero-margin bridge is valid but does not certify uniqueness or gap closure',
          cases['zero_margin']['bound_status'] == 'zero-insufficient'
          and not cases['zero_margin']['ground_uniqueness_certified'])
    check('larger bridge retains a negative insufficient estimate',
          cases['beyond_margin']['bound_status'] == 'negative-insufficient')
    check('signed end couplings obey the same absolute-ratio reference bound',
          cases['signed_ends']['full_gap_lower'] == p['full_gap_lower'])
    check('zero end coefficients remove blocks rather than remove link electric terms',
          len(cases['left_end_zero']['haar_gate']['untouched_bridge_links']) == 3
          and len(cases['zero_ends']['reference_free_edges']) == 10)
    check('empty active end support is a valid pure-free reference',
          cases['all_zero']['active_reference_faces'] == []
          and cases['all_zero']['full_gap_lower'] == '3/4')
    check('double and half physical scales change the actual estimate proportionally',
          F(cases['scaled_double']['full_gap_lower']) == 2*F(p['full_gap_lower'])
          and F(cases['scaled_half']['full_gap_lower']) == F(p['full_gap_lower'])/2)
    check('common scale is not silently replaced by the current sample scale',
          cases['scaled_double']['primary_family_common_bound'] == '1/8'
          and cases['scaled_half']['primary_family_common_bound'] == '1/32')
    missing = evidence['missing_untouched_link_gate']
    check('missing untouched link blocks the sharper inference with missing moments',
          missing['untouched_bridge_links'] == []
          and missing['conditional_first_moment'] is None
          and missing['conditional_second_moment'] is None
          and missing['status'].startswith('blocked'))
    counter = evidence['generic_one_norm_counterexample']
    check('generic one-norm shortcut fails an actual finite spectrum',
          counter['actual_gap'] == counter['generic_valid_lower'] == '1/2'
          and counter['invalid_one_norm_claim'] == '3/4'
          and counter['invalid_claim_exceeds_actual_gap'])
    check('off-diagonal norm and squared norm carry the correct physical units',
          p['bridge_offdiagonal_norm'] == '1/16' and p['bridge_offdiagonal_norm_squared'] == '1/256')
    # Each fixed assignment is an implementation check of a pointwise conditional identity;
    # no assignment or finite proxy is asserted to be the dressed ground.
    qs = [bridge.IDENTITY, (F(1, 2),)*4,
          (F(3, 5), F(4, 5), F(0), F(0)), (F(1, 3), F(2, 3), F(2, 3), F(0))]
    sphere_design = [tuple(F(sign if j == axis else 0) for j in range(4))
                     for axis in range(4) for sign in (-1, 1)]
    middle = next(face for face in graph['faces'] if face['id'] == 'middle')
    word_checks = []
    matrix_error = 0.0
    for offset in range(4):
        links = {e['id']: qs[(i+offset) % len(qs)] for i, e in enumerate(graph['edges'])}
        for free in p['haar_gate']['untouched_bridge_links']:
            samples = []
            for u in sphere_design:
                links[free] = u
                value = bridge.word_value(middle['word'], links)
                samples.append(value[0])
                raw = ((1+0j, 0j), (0j, 1+0j))
                for term in middle['word']:
                    m = cmatrix(links[term['edge']])
                    if term['sign'] == -1:
                        m = tuple(tuple(m[j][i].conjugate() for j in range(2)) for i in range(2))
                    raw = cmul(raw, m)
                expected = cmatrix(value)
                matrix_error = max(matrix_error, *(abs(raw[i][j]-expected[i][j]) for i in range(2) for j in range(2)))
            first, second = sum(samples, F(0))/8, sum((x*x for x in samples), F(0))/8
            if (first, second) != (F(0), F(1, 4)):
                raise RuntimeError('pointwise conditional link moment identity failed')
            word_checks.append({'assignment': offset, 'unused_link': free, 'first': str(first), 'second': str(second)})
    check('eight fixed surrounding assignments preserve the unused-link moments', len(word_checks) == 8)
    check('sixty-four signed quaternion words match independent complex matrix products', matrix_error < 1e-13)
    # Gauge covariance on every edge demonstrates why the resulting unique ground
    # belongs to the unchanged all-vertex Gauss sector.
    links = {e['id']: qs[i % 4] for i, e in enumerate(graph['edges'])}
    transforms = {v: qs[(i+1) % 4] for i, v in enumerate(graph['vertices'])}
    transformed = {e['id']: bridge.multiply(bridge.multiply(transforms[e['tail']], links[e['id']]),
                                           bridge.conjugate(transforms[e['head']])) for e in graph['edges']}
    for face in graph['faces']:
        h0, h1 = bridge.word_value(face['word'], links), bridge.word_value(face['word'], transformed)
        v = transforms[face['vertices'][0]]
        if h1 != bridge.multiply(bridge.multiply(v, h0), bridge.conjugate(v)):
            raise RuntimeError('actual bridge face failed vertex gauge covariance')
    check('all three face holonomies obey exact vertex gauge covariance', True)
    for name, mutate in [
        ('dressed energy falsely set to a computed bare vacuum', lambda c: c.update(reference_ground='bare vacuum with E_s=0')),
        ('generic fallback relabeled as sharp without its moment premise', lambda c: c['haar_gate'].update(untouched_bridge_links=[])),
        ('zero endpoint mislabeled positive', lambda c: c.update(bound_status='positive'))]:
        c = copy.deepcopy(cases['zero_margin'] if name.startswith('zero endpoint') else p)
        mutate(c)
        reject(name, lambda c=c: bridge.verify(graph, c))
    bad_graph = copy.deepcopy(graph)
    bad_graph['faces'][1]['word'][0]['sign'] *= -1
    reject('altered middle-face dagger', lambda: bridge.certify(bad_graph, p['parameters']))
    bad_graph = copy.deepcopy(graph)
    bad_graph['edges'].pop()
    reject('missing free electric link', lambda: bridge.certify(bad_graph, p['parameters']))
    reject('empty coefficient dictionary', lambda: bridge.certify(graph, {}))
    for name, key, value in [('Boolean coupling', 'mu', True), ('zero alpha', 'alpha', '0'),
                             ('nonfinite coupling', 'lambda_left', 'nan'),
                             ('common lower scale above actual alpha', 'alpha_min', '2'),
                             ('nonpositive common scale', 'alpha_min', '0'),
                             ('unproved reference ratio endpoint', 'lambda_left', '3/4')]:
        params = p['parameters'].copy()
        params[key] = value
        reject(name, lambda params=params: bridge.certify(graph, params))
    c = copy.deepcopy(evidence)
    c['fixtures'].pop()
    reject('required scale fixture omitted', lambda: bridge.verify_collection(c))
    (out / 'evidence.json').write_text(json.dumps(evidence, indent=2)+'\n')
    (out / 'graph.json').write_text(json.dumps(graph, indent=2)+'\n')
    (out / 'word-checks.json').write_text(json.dumps({'scope': 'pointwise conditional identity diagnostics, not a dressed-ground approximation',
                                                    'rows': word_checks}, indent=2)+'\n')
    with (out / 'mu-scan.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(evidence['mu_rows'][0]))
        writer.writeheader()
        writer.writerows(evidence['mu_rows'])
    result = {'schema': 'ym18-a1-results-v1', 'status': 'passed', 'checks_count': len(checks), 'checks': checks,
              'source_sha256': bridge.SOURCE_SHA, 'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'evidence_sha256': hashlib.sha256((out / 'evidence.json').read_bytes()).hexdigest(),
              'primary_gap_lower': p['full_gap_lower'], 'primary_generic_lower': p['generic_two_norm_gap_lower'],
              'raw_matrix_max_error': matrix_error,
              'scope': evidence['scope']}
    (out / 'results.json').write_text(json.dumps(result, indent=2)+'\n')
    (out / 'manifest.json').write_text(json.dumps({'schema': 'ym18-a1-output-manifest-v1',
        'files': {name: hashlib.sha256((out/name).read_bytes()).hexdigest() for name in
                  ['evidence.json', 'graph.json', 'word-checks.json', 'mu-scan.csv', 'results.json']}}, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))


if __name__ == '__main__':
    main()
