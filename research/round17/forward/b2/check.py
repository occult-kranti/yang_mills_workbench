"""Reconstruct exact shared-face trial matrix and its finite spectral certificate."""
import argparse
import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import adjoint
import haar_graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    out = Path(args.output).resolve()
    if out == source or source in out.parents:
        raise ValueError('output must be outside frozen source')
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

    g = adjoint.graph()
    s = adjoint.shared_index()
    check('actual graph retains 12 vertices, 20 links and 11 distinct faces',
          (len(g['vertices']), len(g['edges']), len(g['faces'])) == (12, 20, 11))
    check('shared square derived from incidence and interior coordinates',
          g['faces'][s]['normal'] == 0 and g['faces'][s]['base'][0] == 1)
    entries, insertions = [], []
    for i in range(13):
        for j in range(13):
            moment = adjoint.matrix_moment(i, j)
            if moment != int(i == j):
                raise RuntimeError('thirteen-state Gram identity failed')
            entries.append([i, j, str(moment)])
            for face in range(11):
                value = adjoint.matrix_moment(i, j, face)
                old_pair = (i == 0 and j == face + 1) or (j == 0 and i == face + 1)
                new_pair = face == s and ((i == 12 and j == s + 1) or (j == 12 and i == s + 1))
                expected = F(1, 2) if old_pair or new_pair else F(0)
                if value != expected:
                    raise RuntimeError('individual insertion differs from reconstructed matrix')
                insertions.append([i, j, face, str(value)])
    check('all 169 Gram entries agree with the identity', len(entries) == 169)
    check('all 1859 individual magnetic insertions reconstructed', len(insertions) == 1859)
    check('adjoint character norm from repeated shared-face powers',
          adjoint.matrix_moment(12, 12) == 1)
    check('adjoint diagonal magnetic entries vanish for every face',
          all(adjoint.matrix_moment(12, 12, f) == 0 for f in range(11)))
    shared_edges = {term['edge'] for term in g['faces'][s]['word']}
    mixed_squares = []
    for p, face in enumerate(g['faces']):
        if p == s:
            continue
        exclusive = {term['edge'] for term in face['word']} - shared_edges
        powers = [0] * 11
        powers[p] = powers[s] = 2
        mixed_squares.append(bool(exclusive) and haar_graph.moment(powers) == F(1, 16))
    check('ten exclusive-link conditional integrals supply mixed square one over sixteen',
          len(mixed_squares) == 10 and all(mixed_squares))
    gr, electric, potential, h = adjoint.matrices()
    check('adjoint electric energy is four spin-one Casimirs', electric[12][12] == 8)
    check('only new magnetic coupling is minus shared lambda over two',
          potential[12][s + 1] == -F(6, 43)
          and all(potential[12][j] == 0 for j in range(13) if j != s + 1))
    v0 = [F(1)] + [F(1, 22)] * 11
    e = -F(3, 43)
    check('B1 endpoint vector is exact eigenvector of the old twelve-state block',
          all(sum((h[i][j] * v0[j] for j in range(12)), F(0)) == e * v0[i] for i in range(12)))
    check('old vector has norm 45 over 44', sum((x * x for x in v0), F(0)) == F(45, 44))
    check('adjoint cross energy is minus 3 over 473',
          sum((h[12][j] * v0[j] for j in range(12)), F(0)) == -F(3, 473))
    check('factorized numerator proves the entire open positivity interval',
          F(347, 43) * adjoint.ETA_MAX == F(6, 473)
          and adjoint.G > 0 and adjoint.ETA_MAX > 0)
    definitions = [
        ('negative', '1', '-3/3817'), ('zero', '1', '0'),
        ('quarter', '1', '3/7634'), ('selected', '1', '3/3817'),
        ('three_quarters', '1', '9/7634'), ('endpoint', '1', '6/3817'),
        ('beyond', '1', '9/3817'), ('scaled_double', '2', '3/3817'),
        ('scaled_half', '1/2', '3/3817')]
    fixtures = []
    for name, alpha, eta in definitions:
        c = adjoint.certify(alpha, eta)
        check('certificate replay: ' + name, adjoint.verify(c))
        fixtures.append({'id': name, 'certificate': c})
    cases = {entry['id']: entry['certificate'] for entry in fixtures}
    chosen = cases['selected']
    check('selected exact amplitude strictly repairs the B1 endpoint',
          F(chosen['full_gap_lower']) > 0 and chosen['full_E1_lower'] == '-3/43')
    check('zero and upper endpoint remain valid zero-bound trials',
          all(cases[name]['valid_trial'] and cases[name]['bound_status'] == 'zero-insufficient'
              for name in ('zero', 'endpoint')))
    check('negative and beyond-endpoint amplitudes are valid insufficient trials',
          all(cases[name]['valid_trial'] and cases[name]['bound_status'] == 'negative-insufficient'
              for name in ('negative', 'beyond')))
    check('positive alpha scaling gives exactly proportional physical energies',
          all(F(cases[name]['full_gap_lower']) == factor * F(chosen['full_gap_lower'])
              and F(cases[name]['full_E0_upper']) == factor * F(chosen['full_E0_upper'])
              for name, factor in [('scaled_double', F(2)), ('scaled_half', F(1, 2))]))
    check('selected amplitude maximizes the numerator but is not a quotient optimum claim',
          F(6, 473) - 2 * F(347, 43) * adjoint.ETA_SELECTED == 0
          and -2 * adjoint.ETA_SELECTED * F(chosen['gap_numerator']) < 0)
    mutations = [
        ('wrong new electric Casimir', lambda c: c['electric_matrix'][12].__setitem__(12, '3')),
        ('missing shared magnetic cross term', lambda c: c['trial_H'][12].__setitem__(s + 1, '0')),
        ('trial second level substituted as full E1 lower', lambda c: c.update(full_E1_lower='3')),
        ('missing Rayleigh normalization', lambda c: c.update(full_E0_upper=c['energy_numerator'])),
        ('shared face relabelled without geometry', lambda c: c.update(shared_face_index=0)),
        ('valid negative trial mislabeled invalid', lambda c: c.update(valid_trial=False))]
    for name, mutate in mutations:
        c = copy.deepcopy(cases['negative'] if name.startswith('valid negative') else chosen)
        mutate(c)
        reject(name, lambda c=c: adjoint.verify(c))
    reject('Boolean amplitude', lambda: adjoint.certify('1', True))
    reject('zero energy scale', lambda: adjoint.certify('0'))
    reject('negative energy scale', lambda: adjoint.certify('-1'))
    reject('nonfinite amplitude', lambda: adjoint.certify('1', 'nan'))
    reject('Boolean cached state index', lambda: adjoint.matrix_moment(True, 0))
    rows = []
    for name, alpha, eta in definitions[:7]:
        c = cases[name]
        rows.append({'id': name, 'eta': eta, 'eta_fraction_of_endpoint': str(F(eta) / adjoint.ETA_MAX),
                     'gap_lower_over_alpha': c['full_gap_lower'], 'full_E1_lower': c['full_E1_lower'],
                     'rayleigh_E0_upper': c['full_E0_upper'], 'bound_status': c['bound_status'],
                     'valid_trial': 'true'})
    evidence = {'schema': 'ym17-b2-evidence-v1', 'source_sha256': adjoint.SOURCE_SHA,
                'gram_entries': entries, 'individual_insertions': insertions,
                'fixtures': fixtures, 'amplitude_rows': rows,
                'positive_amplitude_interval': ['0', '6/3817'],
                'selected_amplitude': '3/3817', 'physical_common_coupling_ratio': '12/43',
                'dense_uniform_goal': 'open', 'C1': 'not executed'}
    (out / 'evidence.json').write_text(json.dumps(evidence, indent=2) + '\n')
    with (out / 'amplitude.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = {'schema': 'ym17-b2-results-v1', 'status': 'passed',
              'checks_count': len(checks), 'checks': checks, 'source_sha256': adjoint.SOURCE_SHA,
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'evidence_sha256': hashlib.sha256((out / 'evidence.json').read_bytes()).hexdigest(),
              'selected_gap_lower': chosen['full_gap_lower'],
              'selected_gap_lower_float': float(F(chosen['full_gap_lower'])),
              'zero_endpoint_gap_lower': cases['endpoint']['full_gap_lower'],
              'scope': 'Exact finite physical gap lower at the old B1 zero margin; dense volume-uniform goal remains open'}
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    (out / 'manifest.json').write_text(json.dumps({
        'schema': 'ym17-b2-output-manifest-v1',
        'files': {name: hashlib.sha256((out / name).read_bytes()).hexdigest()
                  for name in ('evidence.json', 'amplitude.csv', 'results.json')}}, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))


if __name__ == '__main__':
    main()
