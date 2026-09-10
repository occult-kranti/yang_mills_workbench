"""Validate central Gram sufficiency fixtures and exact recurrence diagnostics."""
import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import math
import tempfile
from fractions import Fraction as F
from pathlib import Path
import gram


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    out = Path(args.output).resolve()
    if out == source or out in source.parents:
        raise ValueError('output cannot overwrite the source directory or an ancestor')
    # A dedicated child output/ is supported by the accepted archival layout.
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

    collection = gram.collection()
    check('complete source-bound eleven-fixture collection replays', gram.verify_collection(collection))
    cases = {f['id']: f['certificate'] for f in collection['fixtures']}
    check('the full declared eleven-fixture inventory is retained', len(cases) == 11)
    for c in cases.values():
        gram.verify(c)
        if len(c['primitive_moments']) != 112:
            raise RuntimeError('incomplete primitive inventory')
        for n in range(7):
            rows = c['primitive_moments'][16*n:16*(n+1)]
            if [row['subset_mask'] for row in rows] != list(range(16)) or any(row['degree'] != n for row in rows):
                raise RuntimeError('primitive inventory order changed')
            reconstructed = sum((F(4**row['subset_mask'].bit_count()*(-1)**(4-row['subset_mask'].bit_count()), 81)*F(row['moment']) for row in rows), F(0))/math.factorial(n)
            if str(reconstructed) != c['numerator_coefficients'][n]:
                raise RuntimeError('numerator does not include the correct formal Taylor normalization')
            if F(rows[0]['moment'])/math.factorial(n) != F(c['partition_coefficients'][n]):
                raise RuntimeError('partition coefficient mismatch')
    check('all1232 primitive moments reconstruct every numerator and partition coefficient including factorials', True)
    check('odd formal degrees vanish for this even central observable and its partition',
          all(c['numerator_coefficients'][n] == c['partition_coefficients'][n] == '0' for c in cases.values() for n in (1, 3, 5)))
    for base in ('tetra', 'commuting'):
        for suffix in ('hadamard', 'reflected'):
            original, changed = cases[base+'_common'], cases[base+'_'+suffix]
            if not (original['gram'] == changed['gram'] and original['vectors'] != changed['vectors']
                    and original['numerator_coefficients'] == changed['numerator_coefficients']
                    and original['partition_coefficients'] == changed['partition_coefficients']
                    and original['primitive_moments'] == changed['primitive_moments']):
                raise RuntimeError('a common orthogonal transformation changed a declared invariant')
    check('common Hadamard and reflection transform all five vectors and preserve all Gram diagnostics', True)
    tetra, commuting = cases['tetra_common'], cases['commuting_common']
    check('equal action vectors and partition data do not imply an equal joint observable',
          tetra['vectors'][0] == commuting['vectors'][0] == ['1/8', '0', '0', '0']
          and tetra['partition_coefficients'] == commuting['partition_coefficients']
          and tetra['gram'] != commuting['gram']
          and tetra['numerator_coefficients'][0] == '-1/405'
          and commuting['numerator_coefficients'][0] == '13/1215')
    historic = collection['historical_convention']['common_reflection_to_round17']
    historical = [gram.certify(gram.transform(c['vectors'][1:], historic), c['kappa']) for c in (tetra, commuting)]
    check('historical conjugate-quaternion convention differs by one common reflection with unchanged Gram and scalar action',
          all(old['gram'] == current['gram'] and old['vectors'][0] == current['vectors'][0]
              and old['numerator_coefficients'] == current['numerator_coefficients']
              for old, current in zip(historical, (tetra, commuting))))
    check('rank1 and rank2 geometries are admitted without Gram inversion',
          cases['rank1_equal']['rank'] == 1 and cases['rank2']['rank'] == 2
          and cases['rank1_equal']['numerator_coefficients'][0] == '1/27')
    check('both rank4 tetrahedral and rank2 commuting cases satisfy complete action constraints',
          tetra['rank'] == 4 and commuting['rank'] == 2)
    zero = cases['commuting_zero_b_nonzero_kappa']
    check('zero action with nonzero cancelling coefficients is a valid exact Haar branch',
          zero['vectors'][0] == ['0']*4 and any(F(k) for k in zero['kappa'])
          and zero['partition_coefficients'] == ['1']+['0']*6
          and zero['numerator_coefficients'] == ['13/1215']+['0']*6)
    check('vanishing coefficients and signed coefficients are separate valid cases',
          cases['tetra_zero_kappa']['numerator_coefficients'] == ['-1/405']+['0']*6
          and cases['tetra_signed_kappa']['numerator_coefficients'][2] != '0')
    check('zero-multiplicity recurrence branch gives the exact orthogonal mixed moment',
          gram.moment(tetra['gram'], tetra['kappa'], [0, 1, 1, 0, 0]) == 0)
    check('sphere one-direction second and fourth moments match independent low-order identities',
          gram.moment(tetra['gram'], tetra['kappa'], [0, 2, 0, 0, 0]) == F(1, 4)
          and gram.moment(tetra['gram'], tetra['kappa'], [0, 4, 0, 0, 0]) == F(1, 8))
    # All leading minors vanish, yet a non-leading 2x2 minor is negative.
    bad = [[str(int(i == j and i > 0)) for j in range(5)] for i in range(5)]
    bad[1][2] = bad[2][1] = '2'
    check('leading-principal-minor shortcut has an explicit indefinite zero-first-row counterexample',
          bad[0] == ['0']*5 and F(bad[1][1])*F(bad[2][2])-F(bad[1][2])**2 == -3)
    reject('indefinite Gram despite all leading minors zero', lambda: gram.validate(bad, ['0']*4))
    identity5 = [[str(int(i == j)) for j in range(5)] for i in range(5)]
    reject('positive rank5 Gram exceeds ambient dimension', lambda: gram.validate(identity5, ['0']*4))
    bad = copy.deepcopy(cases['tetra_zero_kappa']['gram'])
    bad[1][1] = '2'
    reject('nonunit direction', lambda: gram.validate(bad, ['0']*4))
    bad = copy.deepcopy(tetra['gram'])
    bad[1][2] = '1'
    reject('asymmetric Gram', lambda: gram.validate(bad, tetra['kappa']))
    other = gram.vector_data(tetra['vectors'][1:], ['1/8']*4)
    reject('forged action cross relation with otherwise valid vector geometry', lambda: gram.validate(other['gram'], tetra['kappa']))
    bad = copy.deepcopy(commuting['gram'])
    bad[0][0] = str(F(bad[0][0])+1)
    reject('forged action norm while all cross constraints still agree', lambda: gram.validate(bad, commuting['kappa']))
    gram.moment(tetra['gram'], tetra['kappa'], [0, 0, 0, 0, 0])
    bad = copy.deepcopy(tetra['gram'])
    bad[1][2] = False
    reject('nested Boolean Gram entry after warmed cache', lambda: gram.moment(bad, tetra['kappa'], [0]*5))
    reject('Boolean exponent after warmed zero-moment cache', lambda: gram.moment(tetra['gram'], tetra['kappa'], [False, 0, 0, 0, 0]))
    reject('negative exponent', lambda: gram.moment(tetra['gram'], tetra['kappa'], [-1, 1, 0, 0, 0]))
    reject('wrong exponent dimension', lambda: gram.moment(tetra['gram'], tetra['kappa'], [0]*4))
    reject('moment beyond degree14 budget', lambda: gram.moment(tetra['gram'], tetra['kappa'], [16, 0, 0, 0, 0]))
    reject('wrong Gram dimension', lambda: gram.validate(tetra['gram'][:4], tetra['kappa']))
    reject('Boolean coefficient', lambda: gram.validate(tetra['gram'], [False]+tetra['kappa'][1:]))
    num, den = gram.coefficients(tetra['gram'], tetra['kappa'])
    check('public coefficient results are immutable tuples of exact Fractions',
          type(num) is tuple and type(den) is tuple and all(type(x) is F for x in num+den))
    reject('cached-result assignment', lambda: num.__setitem__(0, F(0))) if hasattr(num, '__setitem__') else check('immutable coefficient tuple has no assignment operation', True)
    bad = copy.deepcopy(tetra)
    bad['numerator_coefficients'][0] = '0'
    reject('returned certificate mutation', lambda: gram.verify(bad))
    check('mutated returned certificate cannot poison future cached results',
          gram.certify(tetra['vectors'][1:], tetra['kappa'])['numerator_coefficients'][0] == '-1/405')
    for name, mutate in [('source hash', lambda x: x.update(source_sha256='0'*64)),
                         ('schema', lambda x: x.update(schema='ym18-c1-certificate-v2')),
                         ('missing primitive moment', lambda x: x['primitive_moments'].pop())]:
        bad = copy.deepcopy(tetra)
        mutate(bad)
        reject(name, lambda bad=bad: gram.verify(bad))
    bad = copy.deepcopy(collection)
    bad['fixtures'].pop()
    reject('required rank or zero-action fixture omitted', lambda: gram.verify_collection(bad))
    old = gram.DIMENSION
    try:
        gram.DIMENSION = 4.0
        reject('runtime dimension type alias', lambda: gram.collection())
    finally:
        gram.DIMENSION = old
    # Source-file mutation is tested on a temporary copy, never the frozen file.
    with tempfile.TemporaryDirectory(dir=out) as directory:
        p = Path(directory)/'gram.py'
        p.write_bytes((source/'gram.py').read_bytes())
        spec = importlib.util.spec_from_file_location('c1_source_mutation_probe', p)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        p.write_bytes(p.read_bytes()+b'\n')
        reject('source changed after import', lambda: module.collection())
    (out/'collection.json').write_text(json.dumps(collection, indent=2)+'\n')
    rows = [{'fixture': name, 'degree': n, 'numerator': c['numerator_coefficients'][n],
             'partition': c['partition_coefficients'][n], 'rank': c['rank']}
            for name, c in cases.items() for n in range(7)]
    with (out/'coefficients.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = {'schema': 'ym18-c1-results-v1', 'status': 'passed', 'checks_count': len(checks), 'checks': checks,
              'source_sha256': gram.SOURCE_SHA, 'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'evidence_sha256': hashlib.sha256((out/'collection.json').read_bytes()).hexdigest(),
              'fixture_count': 11, 'primitive_moment_count': 1232,
              'scope': 'author exact arithmetic and implementation checks; independent acceptance is separate'}
    (out/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name != 'manifest.json'}
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({'status': 'passed', 'checks_count': len(checks), 'evidence_sha256': result['evidence_sha256']}))


if __name__ == '__main__':
    main()
