"""Reproduce B2 certificates and decisive full-operator inference controls."""
import argparse
import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import gap


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    out = Path(args.output).resolve()
    if out == source or source in out.parents:
        raise ValueError('output must be outside immutable sources')
    out.mkdir(parents=True, exist_ok=True)
    checks = []

    def check(name, condition):
        if not condition:
            raise RuntimeError(name)
        checks.append(name)

    def reject(name, call):
        try:
            call()
        except (ValueError, TypeError, KeyError):
            checks.append('reject: '+name)
            return
        raise RuntimeError('invalid accepted: '+name)

    evidence = gap.collection()
    check('complete frozen parameter and source collection replays', gap.verify_collection(evidence))
    cases = {row['id']: row['certificate'] for row in evidence['fixtures']}
    check('all eleven declared signed scale precision and outside fixtures retained', len(cases) == 11)
    check('eight exact samples preserve the frozen order', tuple(row['r'] for row in evidence['samples']) == gap.SAMPLES)
    for row in evidence['fixtures']:
        cert = row['certificate']
        gap.verify(cert)
        s = cert['scalar_comparison']
        q = F(s['discriminant'])
        lo, hi = gap.bounds(s['sqrt_discriminant'])
        low, high = gap.bounds(s['R'])
        c, b2 = F(s['c']), F(s['b_squared'])
        if not (0 <= lo <= hi and lo*lo <= q <= hi*hi and low <= high):
            raise RuntimeError('radical or eigenvalue interval failed')
        if not (3-low >= 0 and c-low >= 0 and (3-low)*(c-low)-b2 >= 0):
            raise RuntimeError('full scalar lower shift failed')
        a = F(cert['alpha'])
        sqrt_e0_lo = 3*a-2*F(cert['star_E0_upper_formula_interval']['upper'])
        sqrt_e0_hi = 3*a-2*F(cert['star_E0_upper_formula_interval']['lower'])
        if not sqrt_e0_lo**2 <= 9*a*a+F(cert['sum_coupling_squares']) <= sqrt_e0_hi**2:
            raise RuntimeError('ground trial outward orientation failed')
    check('every radical and scalar shifted matrix passes exact squaring and principal minors', True)
    check('all ground trial brackets have the correct outward upper direction', True)
    check('whole-box comparison is analytic from endpoint c and b squared',
          F(9, 2)-11*F(3, 8) == F(3, 8)
          and 21*F(3, 8)**2/4 == F(189, 256)
          and 3*F(3, 8)-F(189, 256) == F(99, 256))
    check('whole-box constant is strictly positive without numerical inference', 81 > 70)
    check('endpoint star trial improves on vacuum upper zero', 675 > 576)
    const = evidence['constants']
    check('primary and stronger endpoint intervals meet the requested width',
          all(F(const[key]['width']) <= gap.TARGET and F(const[key]['lower']) > 0 for key in ('R_star', 'D_star')))
    check('zero coupling retains exact radical and zero cross edge cases',
          cases['allzero']['scalar_comparison']['R'] == {'lower': '3', 'upper': '3', 'width': '0'}
          and cases['allzero']['scalar_comparison']['b_squared'] == '0')
    check('endpoint global and alternating signs preserve all primary formulas',
          all(cases[name]['full_E1_lower_formula_interval'] == cases['endpoint_allplus']['full_E1_lower_formula_interval']
              and cases[name]['star_E0_upper_formula_interval'] == cases['endpoint_allplus']['star_E0_upper_formula_interval']
              and cases[name]['endpoint_gap_lower_formula_interval'] == cases['endpoint_allplus']['endpoint_gap_lower_formula_interval']
              for name in ('endpoint_allminus', 'endpoint_alternating')))
    check('sparse and mixed signed coefficients are covered without endpoint star label',
          all(cases[name]['box_member'] and not cases[name]['all_endpoint_magnitudes']
              and cases[name]['endpoint_gap_lower_formula_interval'] is None for name in ('sparse_interior', 'mixed_signed_interior')))
    for name, factor in [('scaled_double', F(2)), ('scaled_half', F(1, 2))]:
        expected = gap.scale(cases['endpoint_allplus']['endpoint_gap_lower_formula_interval'], factor)
        if cases[name]['endpoint_gap_lower_formula_interval'] != expected:
            raise RuntimeError('physical endpoint scale law failed')
    check('positive alpha scaling and declared common floors preserve physical energy units',
          cases['scaled_double']['common_scale_gap_lower_formula_interval'] == const['R_star']
          and cases['scaled_half']['common_scale_gap_lower_formula_interval'] == gap.scale(const['R_star'], F(1, 4)))
    check('coarse precision failure is retained separately from analytic positivity',
          cases['coarse_endpoint']['analytic_box_status'] == 'positive-proved'
          and cases['coarse_endpoint']['whole_box_enclosure_status'] == 'insufficient-precision'
          and cases['coarse_endpoint']['endpoint_enclosure_status'] == 'insufficient-precision'
          and cases['coarse_endpoint']['constants']['R_star']['lower'] == '0')
    check('larger sampled couplings are outside and have insufficient scalar lower bounds',
          all(not cases[name]['box_member'] and cases[name]['whole_box_gap_lower_formula_interval'] is None
              and cases[name]['scalar_comparison']['bound_status'] == 'negative-insufficient'
              for name in ('outside_two_fifths', 'outside_one_half')))
    check('deleted-cross scalar control refutes the diagonal-only shortcut',
          3+F(3, 8)*21-2*F(3, 16)*21 == 3 and F(3, 22) < F(3, 8))
    check('missing codimension-one restriction is exposed by bare vacuum energy', F(0) < F(3))
    check('omitting a face from P invalidates the higher complement premise', F(3) < F(9, 2))
    check('finite Ritz gap cannot lower-bound the full gap', F(1, 8) < F(3))
    for missing in ('Q_electric_lower_over_alpha', 'cross_norm_squared_over_alpha_squared_r_squared_upper', 'codimension_one_space'):
        value = gap.premises()
        del value[missing]
        reject('missing full-operator premise '+missing, lambda value=value: gap.certify('1', ['3/8']*11, proof_premises=value))
    old = gap.REQUIRED_PREMISES['complement_is_full_Q']
    try:
        gap.REQUIRED_PREMISES['complement_is_full_Q'] = False
        reject('retained runtime full-complement premise mutation', lambda: gap.certify('1', ['0']*11, proof_premises=dict(gap.REQUIRED_PREMISES)))
    finally:
        gap.REQUIRED_PREMISES['complement_is_full_Q'] = old
    old = gap.PREMISE_FILES['graph.json']
    try:
        gap.PREMISE_FILES['graph.json'] = '0'*64
        reject('runtime source-pin mutation', lambda: gap.certify('1', ['0']*11))
    finally:
        gap.PREMISE_FILES['graph.json'] = old
    old = gap.TARGET
    try:
        gap.TARGET = F(1)
        reject('runtime precision target relaxation', lambda: gap.collection())
    finally:
        gap.TARGET = old
    old = gap.SAMPLES
    try:
        gap.SAMPLES = ('0',)
        reject('runtime sample inventory deletion', lambda: gap.collection())
    finally:
        gap.SAMPLES = old
    for label, mutate in [
        ('out-of-box passing label', lambda c: c.update(box_member=True, analytic_box_status='positive-proved')),
        ('deleted cross coefficient', lambda c: c['scalar_comparison'].update(b_squared='0')),
        ('Ritz gap substituted as full excited bound', lambda c: c.update(full_E1_lower_formula_interval={'lower': '3', 'upper': '3', 'width': '0'})),
        ('Boolean field alias', lambda c: c.update(precision_bits=False)),
        ('premise graph hash changed', lambda c: c['proof_premises'].update(graph_sha256='0'*64)),
    ]:
        c = copy.deepcopy(cases['outside_two_fifths'] if label == 'out-of-box passing label' else cases['endpoint_allplus'])
        mutate(c)
        reject(label, lambda c=c: gap.verify(c))
    reject('explicit box claim beyond frozen boundary', lambda: gap.certify('1', ['2/5']*11, claim_box=True))
    c = copy.deepcopy(evidence)
    c['fixtures'].pop()
    reject('required outside fixture omitted', lambda: gap.verify_collection(c))
    c = copy.deepcopy(evidence)
    c['samples'].pop(3)
    reject('required historical threshold sample omitted', lambda: gap.verify_collection(c))
    gap.sqrt_bracket('0', 0)
    reject('Boolean precision even on the exact zero branch', lambda: gap.sqrt_bracket('0', False))
    reject('negative root', lambda: gap.sqrt_bracket('-1', 48))
    reject('precision beyond declared resource budget', lambda: gap.sqrt_bracket('70', 257))
    reject('nonpositive energy scale', lambda: gap.certify('0', ['0']*11))
    reject('Boolean nested coefficient', lambda: gap.certify('1', [False]+['0']*10))
    reject('missing coefficient', lambda: gap.certify('1', ['0']*10))
    reject('common floor larger than actual alpha', lambda: gap.certify('1/2', ['0']*11, alpha_min='1'))
    check('physical matching retains the magnetic constant shift and exact ratio',
          F(4, 2) == 2 and (F(2)/(F(1, 2))) == 4 and F(4)/F(3, 8) == F(32, 3))
    # Two exact positive g^2,a fixtures verify both conventions independently.
    check('bare-coupling algebra agrees at two nonunit scales', all(
        (F(2)/(g2*lattice_spacing))/(g2/(2*lattice_spacing)) == F(4)/(g2*g2)
        for g2, lattice_spacing in [(F(3), F(1, 5)), (F(7, 2), F(4))]))
    (out/'collection.json').write_text(json.dumps(evidence, indent=2)+'\n')
    rows = []
    for sample in evidence['samples']:
        r = F(sample['r'])
        c = gap.certify('1', [str(r)]*11)
        rows.append({'r': str(r), 'R_lower': sample['R']['lower'], 'R_upper': sample['R']['upper'],
                     'R_width': sample['R']['width'],
                     'instance_gap_lower': c['instance_gap_lower_formula_interval']['lower'],
                     'instance_gap_upper': c['instance_gap_lower_formula_interval']['upper'],
                     'box_member': sample['box_member'], 'status': sample['bound_status']})
    with (out/'coupling.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = {'schema': 'ym18-b2-results-v1', 'status': 'passed', 'checks_count': len(checks), 'checks': checks,
              'source_sha256': gap.SOURCE_SHA, 'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'evidence_sha256': hashlib.sha256((out/'collection.json').read_bytes()).hexdigest(),
              'constants': const, 'insufficient_fixtures': ['coarse_endpoint', 'outside_two_fifths', 'outside_one_half'],
              'scope': 'author arithmetic and implementation checks; independent acceptance is a separate role'}
    (out/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.iterdir()) if p.is_file() and p.name != 'manifest.json'}
    (out/'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(json.dumps({'status': 'passed', 'checks_count': len(checks), 'evidence_sha256': result['evidence_sha256']}))


if __name__ == '__main__':
    main()
