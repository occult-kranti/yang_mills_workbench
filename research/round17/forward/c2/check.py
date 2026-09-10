"""Reproduce exact conditional comparisons, retained insufficiencies and controls."""
import argparse
import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import conditional
import geometry


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

    evidence = conditional.collection()
    check('complete fixed refinement and fixture collection replays', conditional.verify_collection(evidence))
    check('fixed degree sequence is retained without skipped coarse results', evidence['degree_sequence'] == [0, 4, 8, 12, 16])
    check('degrees zero, four and eight remain insufficient',
          [r['status'] for r in evidence['refinements'][:3]] == ['insufficient']*3)
    check('degrees twelve and sixteen meet all three sign and precision targets',
          [r['status'] for r in evidence['refinements'][3:]] == ['accepted']*2)
    final = evidence['refinements'][-1]
    check('final common action vector is one quarter along the scalar axis',
          final['tetrahedral']['action_vector'] == final['commuting']['action_vector'] == ['1/4', '0', '0', '0'])
    check('common partition coefficients and intervals agree exactly',
          final['tetrahedral']['partition_coefficients'] == final['commuting']['partition_coefficients']
          and final['tetrahedral']['partition_interval'] == final['commuting']['partition_interval'])
    check('relative direction Gram matrices differ despite matched action',
          final['tetrahedral']['direction_gram'] != final['commuting']['direction_gram'])
    check('joint observable polynomials are different central-link functions',
          final['tetrahedral']['observable_polynomial'] != final['commuting']['observable_polynomial'])
    cases = {f['id']: f['certificate'] for f in evidence['fixtures']}
    check('zero action reproduces the complete tetrahedral Haar tensor value',
          cases['zero_tetrahedral']['expectation_interval'] == ['-1/405', '-1/405'])
    check('zero commuting action has exact joint thirteen over 1215',
          cases['zero_commuting']['expectation_interval'] == ['13/1215', '13/1215'])
    check('zero-action contrast is exactly sixteen over 1215',
          conditional.contrast(cases['zero_tetrahedral'], cases['zero_commuting'])['interval'] == ['16/1215', '16/1215'])
    z = cases['zero_b_nonzero_coefficients']
    check('nonzero coefficients with zero b use the exact Haar branch without division',
          any(F(x) for x in z['kappas']) and z['action_branch'] == 'zero-vector Haar'
          and z['tail'] == '0' and z['partition_interval'] == ['1', '1']
          and z['expectation_interval'] == cases['zero_commuting']['expectation_interval'])
    check('all-zero coefficients are explicit retained fixtures',
          cases['zero_tetrahedral']['kappas'] == cases['zero_commuting']['kappas'] == ['0']*4)
    check('signed common coupling gives identical even-observable intervals',
          all(cases['negative_' + name]['expectation_interval'] == final[name]['expectation_interval']
              for name in ('tetrahedral', 'commuting')))
    check('half coupling changes the finite joint observable',
          all(cases['half_' + name]['expectation_interval'] != final[name]['expectation_interval']
              for name in ('tetrahedral', 'commuting')))
    check('tetrahedral individual angular polynomials vanish identically',
          evidence['tetrahedral_individual_angular_polynomials'] == [['0', '0']]*4)
    check('zero individual means do not imply a zero joint mean',
          F(final['tetrahedral']['expectation_interval'][1]) < 0)
    control = evidence['action_only_cache_control']
    check('actual action-only cache control is rejected by disjoint intervals',
          control['same_action'] and control['same_partition'] and control['intervals_disjoint'] and control['status'] == 'rejected')
    check('contrast uses the full doubled numerator tail and the common denominator',
          F(final['contrast']['numerator_difference_tail']) == 2*F(final['tetrahedral']['tail'])
          and final['contrast']['common_partition_interval'] == final['tetrahedral']['partition_interval'])
    check('signed interval division preserves negative numerator endpoints',
          conditional.divide_interval((F(-2), F(-1)), (F(2), F(4))) == (F(-1), F(-1, 4)))
    check('complete tail at zero action is exactly zero', conditional.remainder(F(0), 0) == 0)
    graph = geometry.make_graph()
    info = geometry.geometry(graph)
    words = geometry.central_words(graph)
    central_edge = info['central_edge']
    check('exactly sixteen other face terms are constant in this conditional integral',
          sum(all(t['edge'] != central_edge for t in f['word']) for f in graph['faces']) == 16)
    u = (F(1, 3), F(2, 3), F(2, 3), F(0))
    for name, hs in [('tetrahedral', conditional.TETRA), ('commuting', conditional.COMMUTING)]:
        certificate = final[name]
        ls = {key: tuple(map(F, q)) for key, q in certificate['actual_boundary_realization']['all_link_assignments'].items()}
        ls[central_edge] = u
        actual_x = []
        for entry, target in zip(words, conditional.boundaries(hs)):
            q = geometry.product_word(entry['word'], ls)
            if q != geometry.multiply(u, target):
                raise RuntimeError('actual boundary path does not realize the specified central function')
            actual_x.append(q[0])
        check('actual signed paths realize the ' + name + ' boundary and common action',
              sum(actual_x, F(0))/8 == u[0]/4)
    for name, mutate in [
        ('matched action used to replace the observable coefficients',
         lambda c: c.update(numerator_coefficients=final['tetrahedral']['numerator_coefficients'])),
        ('partition remainder omitted',
         lambda c: c.update(partition_interval=[c['partition_partial']]*2)),
        ('adjoint normalization removed',
         lambda c: c.update(numerator_partial=str(81*F(c['numerator_partial'])))),
        ('boundary realization omitted', lambda c: c.pop('actual_boundary_realization'))]:
        c = copy.deepcopy(final['commuting'])
        mutate(c)
        reject(name, lambda c=c: conditional.verify(c))
    c = copy.deepcopy(evidence)
    c['fixtures'].pop()
    reject('zero-b nonzero-coefficient fixture removed', lambda: conditional.verify_collection(c))
    c = copy.deepcopy(evidence)
    c['refinements'] = c['refinements'][3:]
    reject('coarse insufficiencies removed', lambda: conditional.verify_collection(c))
    # Warm caches before checking Python's Boolean/integer alias edge case.
    conditional.sphere_moment((0, 0, 0, 0))
    conditional.observable(conditional.COMMUTING)
    helper_poly = (((2, 0, 0, 0), F(1)),)
    conditional.integrate(helper_poly, 0)
    check('declared list and tuple polynomial encodings integrate identically',
          conditional.integrate([([2, 0, 0, 0], F(1))], 0) == conditional.integrate(helper_poly, 0))
    reject('Boolean scalar-power alias in warmed integration helper', lambda: conditional.integrate(helper_poly, False))
    reject('negative scalar power hidden by a positive polynomial exponent', lambda: conditional.integrate(helper_poly, -1))
    reject('Boolean polynomial exponent before helper arithmetic', lambda: conditional.integrate((((False, 0, 0, 0), F(1)),)))
    bad = [list(q) for q in conditional.COMMUTING]
    bad[0][0] = True
    reject('nested Boolean boundary alias after cache warmup', lambda: conditional.observable(bad))
    reject('Boolean power alias after cache warmup', lambda: conditional.sphere_moment((False, 0, 0, 0)))
    reject('negative monomial index', lambda: conditional.sphere_moment((-2, 0, 0, 0)))
    reject('malformed coordinate tuple', lambda: conditional.observable([('1', '0', '0')]*4))
    reject('nonunit boundary quaternion', lambda: conditional.observable([('1', '1', '0', '0')]*4))
    reject('Boolean Taylor degree', lambda: conditional.certify(order=True))
    reject('negative Taylor degree', lambda: conditional.certify(order=-1))
    reject('Taylor cap exceeded', lambda: conditional.certify(order=17))
    reject('non-axis action cannot be silently rotated',
           lambda: conditional.certify(conditional.TETRA, ('1/8', '0', '0', '0')))
    reject('Boolean coefficient alias', lambda: conditional.certify(kappas=(True, '1/8', '1/8', '1/8')))
    refinement_rows = []
    for r in evidence['refinements']:
        refinement_rows.append({'degree': r['degree'], 'status': r['status'],
            'tetra_lower': r['tetrahedral']['expectation_interval'][0], 'tetra_upper': r['tetrahedral']['expectation_interval'][1],
            'commuting_lower': r['commuting']['expectation_interval'][0], 'commuting_upper': r['commuting']['expectation_interval'][1],
            'contrast_lower': r['contrast']['interval'][0], 'contrast_upper': r['contrast']['interval'][1],
            'width': r['contrast']['width']})
    coupling_rows = []
    for k, t, c in [('-1/8', cases['negative_tetrahedral'], cases['negative_commuting']),
                     ('0', cases['zero_tetrahedral'], cases['zero_commuting']),
                     ('1/16', cases['half_tetrahedral'], cases['half_commuting']),
                     ('1/8', final['tetrahedral'], final['commuting'])]:
        d = conditional.contrast(t, c)
        coupling_rows.append({'common_kappa': k, 'degree': 16,
            'tetra_lower': t['expectation_interval'][0], 'tetra_upper': t['expectation_interval'][1],
            'commuting_lower': c['expectation_interval'][0], 'commuting_upper': c['expectation_interval'][1],
            'contrast_lower': d['interval'][0], 'contrast_upper': d['interval'][1]})
    (out / 'collection.json').write_text(json.dumps(evidence, indent=2) + '\n')
    for filename, rows in [('refinement.csv', refinement_rows), ('coupling.csv', coupling_rows)]:
        with (out / filename).open('w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    result = {'schema': 'ym17-c2-results-v1', 'status': 'passed', 'checks_count': len(checks),
              'checks': checks, 'source_sha256': conditional.SOURCE_SHA,
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'evidence_sha256': hashlib.sha256((out / 'collection.json').read_bytes()).hexdigest(),
              'final_tetra_interval': final['tetrahedral']['expectation_interval'],
              'final_commuting_interval': final['commuting']['expectation_interval'],
              'final_contrast_interval': final['contrast']['interval'],
              'final_contrast_width': final['contrast']['width'],
              'final_contrast_lower_float': float(F(final['contrast']['interval'][0])),
              'retained_insufficient_degrees': [r['degree'] for r in evidence['refinements'] if r['status'] == 'insufficient'],
              'scope': evidence['scope']}
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    (out / 'manifest.json').write_text(json.dumps({'schema': 'ym17-c2-output-manifest-v1',
        'files': {name: hashlib.sha256((out / name).read_bytes()).hexdigest()
                  for name in ('collection.json', 'refinement.csv', 'coupling.csv', 'results.json')}}, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key not in
                    ('checks', 'final_tetra_interval', 'final_commuting_interval', 'final_contrast_interval')}, indent=2))


if __name__ == '__main__':
    main()
