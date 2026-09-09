#!/usr/bin/env python3
"""Bind the round13 site to reviewed source, exact certificates and recorded CSVs."""
from pathlib import Path
from fractions import Fraction as F
import csv
import hashlib
import json
import math
import shutil
import tempfile
from proof_routes import checked_inputs, execute

HERE = Path(__file__).resolve().parent
DIST = HERE.parents[1] / 'dist'


def read(name):
    return json.loads((HERE / name).read_text())


def rows(name):
    with (HERE / name).open(newline='') as stream:
        return list(csv.DictReader(stream))


def source_bindings(records, prefix=''):
    if not isinstance(records, dict) or not records:
        raise ValueError('Missing source/output bindings')
    for name, expected in records.items():
        path = HERE / prefix / name
        if not path.resolve().is_relative_to(HERE) or any(p.is_symlink() for p in (path, *path.parents)):
            raise ValueError('Unsafe input binding')
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError('Stale input: ' + str(path))


def build():
    checked_inputs()
    proof = read('proof_results.json')
    with tempfile.TemporaryDirectory(dir=HERE, prefix='site-proof-replay-') as directory:
        fresh = execute(output=Path(directory) / 'proof.json')
    if fresh != proof:
        raise ValueError('Site proof record disagrees with actual frozen-input replay')
    acceptance = read('skeptic/acceptance.json')
    if acceptance.get('status') != 'passed':
        raise ValueError('Independent acceptance incomplete')
    source_bindings(acceptance['reviewed_source_hashes'])
    adapter_review = read('skeptic/proof_adapter_review.json')
    if adapter_review.get('status') != 'passed':
        raise ValueError('Independent adapter review incomplete')
    source_bindings(adapter_review['reviewed_source_hashes'])
    adapter_tests = read('proof_adapter_tests.json')
    source_bindings({'proof_routes.py': adapter_tests['source_sha256'],
                     'test_proof_routes.py': adapter_tests['test_source_sha256']})
    if adapter_tests.get('status') != 'passed' or adapter_tests['check_count'] != len(adapter_tests['checks']) or not all(c.get('passed') is True for c in adapter_tests['checks']):
        raise ValueError('Adapter producer checks incomplete')
    if sum(r['count'] for r in acceptance['reports']) != acceptance['independent_gate_count']:
        raise ValueError('Independent gate count mismatch')
    study = read('moments/output/study.json')
    source_bindings(study['source_hashes'], 'moments')
    for name in ('tests.json', 'tests_optimized.json'):
        report = read('moments/output/' + name)
        source_bindings({'moment_bounds.py': report['source_sha256']}, 'moments')
        if report.get('status') != 'passed' or report['count'] != len(report['checks']) or not all(c.get('passed') is True for c in report['checks']):
            raise ValueError('Moment producer tests incomplete')
    source_bindings(read('response/output/SHA256SUMS.json'), 'response/output')
    locality = read('locality/output/results.json')
    response = read('response/output/results.json')
    moment_rows = rows('moments/output/bounds.csv')
    certificates = read('moments/output/certificates.json')['certificates']
    lookup = {(c['kappa'], c['level']): c for c in certificates}
    if len(moment_rows) != len(lookup) or len(lookup) != 28:
        raise ValueError('Moment chart case set mismatch')
    for row in moment_rows:
        c = lookup[(row['kappa'], int(row['level']))]
        for key, field in [('mean_interval', 'mean'), ('variance_interval', 'variance')]:
            bounds = [F(x) for x in c[key]]
            if bounds != [F(row[field + '_lower']), F(row[field + '_upper'])] or F(row[field + '_width']) != bounds[1] - bounds[0]:
                raise ValueError('Moment chart differs from exact certificate')
        width = F(row['mean_width'])
        if width == 0:
            if row['log10_mean_width'] != '':
                raise ValueError('Exact zero may not be assigned a finite logarithm')
        elif not math.isclose(float(row['log10_mean_width']), math.log10(float(width)), abs_tol=1e-13):
            raise ValueError('Moment display logarithm mismatch')
    docs = {name: (HERE / path).read_text() for name, path in {
        'advisor': 'advisor/advisor.md', 'stability': 'advisor/weak-coupling-stability.md',
        'moments': 'moments/README.md', 'locality': 'locality/locality.md',
        'response': 'response/response.md', 'skeptic': 'skeptic/REVIEW.md',
        'adapter': 'skeptic/proof_adapter_review.md',
        'readme': 'README.md', 'experiments': 'next-experiments.md'}.items()}
    docs['proof'] = json.dumps(proof, indent=2)
    docs['inventory'] = json.dumps({'theory_nodes': read('advisor/theorem_inventory.json'),
                                  'reviewed_implications': read('advisor/inference_rules.json')}, indent=2)
    docs['checks'] = json.dumps({'independent_science': acceptance, 'independent_adapter': adapter_review,
        'proof_adapter': adapter_tests, 'moment_producer': read('moments/output/tests.json'),
        'locality_producer': locality, 'response_producer': response}, indent=2)
    sources = []
    for path, key in [('advisor/sources.json', 'primary_sources'), ('response/sources.json', 'sources')]:
        for item in read(path)[key]:
            if not any(old['url'] == item['url'] for old in sources):
                sources.append({'title': item['title'], 'url': item['url'], 'use': item['supports'],
                    'depth': item['reading_depth'] + ' Limit: ' + item['limitations']})
    for source, target in [('moments/output/bounds.csv', 'exception-moments.csv'),
                           ('locality/output/boundary_decay.csv', 'exception-locality.csv'),
                           ('response/output/response_curves.csv', 'exception-response.csv')]:
        shutil.copyfile(HERE / source, DIST / target)
    shutil.copyfile(HERE / 'moments/output/certificates.json', DIST / 'research-round13-certificates.json')
    boundary = rows('locality/output/boundary_decay.csv')
    curves = rows('response/output/response_curves.csv')
    plots = {
        'moment_width': {
            'title': 'Finite hierarchy: exact certified mean-interval width',
            'xLabel': 'Hierarchy level r', 'yLabel': 'log₁₀ interval width', 'csv': '/exception-moments.csv',
            'caption': 'Each width comes from rational exclusion witnesses and feasible inner points. Level and coupling are not physical time or lattice spacing. The exact zero-width Haar case is omitted from this logarithmic plot. No uniform convergence rate is inferred.',
            'series': [{'name': 'κ=' + k, 'points': [[int(r['level']), float(r['log10_mean_width'])]
                for r in moment_rows if r['kappa'] == k]} for k in ('1', '5', '20')]},
        'locality_radius': {
            'title': 'Fixed-spacing boundary influence: explicit upper bound',
            'xLabel': 'Plaquette-chain boundary radius R', 'yLabel': 'log₁₀ observable-norm bound', 'csv': '/exception-locality.csv',
            'caption': 'Exact rational tail upper bounds for d=3, four initial links, ||A||=1 and J=1/4. These are computed bounds, not measured simulation errors. A value of 2 is the trivial cap. The estimate has no total-volume factor.',
            'series': [{'name': 'Certified boundary upper bound', 'points': [[int(r['radius']), math.log10(float(F(r['bound_rational'])))] for r in boundary]}]},
        'scalar_mean': {
            'title': 'Same coupling, different closure assumptions',
            'xLabel': 'Euclidean coupling κ', 'yLabel': 'Mean trace u(κ)', 'csv': '/exception-response.csv',
            'caption': 'The regular Riccati trajectory is compared with independent Haar quadrature. Deleting variance gives a different algebraic curve; replacing coefficient 3 by 2 describes a different uniform prior. Curves are floating diagnostics, not certified trajectory intervals.',
            'series': [{'name': label, 'points': [[float(r['kappa']), float(r[field])] for r in curves]} for label, field in [
                ('Regular scalar ODE', 'mean_ode_reflected'), ('Independent Haar quadrature', 'mean_quad'),
                ('Zero-variance closure', 'mean_zero_variance_root'), ('Coefficient 2: different prior', 'mean_wrong_coefficient_reflected')]]},
        'scalar_variance': {
            'title': 'The retained fluctuation is the coupling susceptibility',
            'xLabel': 'Euclidean coupling κ', 'yLabel': 'v(κ)=Var(x)=du/dκ', 'csv': '/exception-response.csv',
            'caption': 'Recorded quadrature values illustrate the analytically derived positive susceptibility. At κ=0 the exact Haar value is 1/4. This is not a real-time response function or a mass.',
            'series': [{'name': 'Variance of the exponential-Haar measure', 'points': [[float(r['kappa']), float(r['susceptibility_quad'])] for r in curves]}]}}
    for plot in plots.values():
        if not all(s['points'] and all(math.isfinite(v) for p in s['points'] for v in p) for s in plot['series']):
            raise ValueError('Invalid chart values')
    selected = lookup[('1', 6)]
    width = F(selected['mean_interval'][1]) - F(selected['mean_interval'][0])
    reviews = [{'name': r['name'], 'status': str(r['count']) + ' independent checks passed', 'scope': r['scope']} for r in acceptance['reports']]
    reviews += [{'name': r['name'], 'status': str(r['count']) + ' independent checks passed', 'scope': r['scope']} for r in adapter_review['reports']]
    reviews += [{'name': 'Proof adapter', 'status': str(adapter_tests['check_count']) + ' producer mutation gates passed',
                 'scope': 'Normal and optimized runs repeat the same gates. Actual reviewed-premise search and certificate replay; not a formal mathematics kernel.'},
                {'name': 'Four-dimensional continuum target', 'status': 'OPEN',
                 'scope': 'The fixed-spacing small-interaction theorem does not extend along the weak-bare-coupling continuum trajectory.'}]
    payload = {'documents': docs, 'plots': plots, 'cases': read('advisor/case_matrix.json')['cases'],
        'nodes': read('advisor/theorem_inventory.json')['claims'],
        'roadmap': read('current_roadmap.json')['items'], 'sources': sources, 'reviews': reviews,
        'routes': [{'name': name, 'status': route['result']['status'], 'cost': route['result'].get('certified_cost')} for name, route in proof['routes'].items()],
        'metrics': {'moment_width_k1_r6': f'At κ=1 and r=6, the certified mean interval has width {float(width):.6g}. Rounded displays refer to the exact rational certificate.',
            'locality_example': 'The R=48, z=8 example is bounded above by approximately ' + format(float(F(locality['fixed_budget_example']['bound_rational'])), '.6g') + '; this is not an observed error.',
            'stability_status': 'The independent skeptic accepted the primary-theorem match, boundary padding, SU(2) Gauss restriction and threshold algebra. The admissible coupling threshold remains existential and unevaluated.'}}
    (DIST / 'research-exceptions-data.js').write_text('window.OBSERVATORY_EXCEPTIONS=' + json.dumps(payload, ensure_ascii=False, separators=(',', ':'), allow_nan=False) + ';\n')
    print(json.dumps({'plots': len(plots), 'sources': len(sources), 'cases': len(payload['cases']), 'routes': len(payload['routes'])}))


if __name__ == '__main__':
    build()
