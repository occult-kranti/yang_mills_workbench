"""Full-operator signed-box bound conditional on the frozen B1 theorem.

Radical intervals enclose analytic bounds, never the physical gap itself.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math

SOURCE_BYTES = Path(__file__).read_bytes()
SOURCE_SHA = hashlib.sha256(SOURCE_BYTES).hexdigest()
PREMISE_FILES = {
    'b1-gate.json': '344f3e5442e63a59f51389dc7f3c8a63d3e3c6cc2ff0aac9f4672b18a8020086',
    'b1-report.md': 'b271d4f1d48da3fa01dd722b66338b31316fdfd965a3d4dbbecfb87596ad2796',
    'graph.json': '9e630191189fb3f69145e5cdbc91eceac138f95d44d7bed825b87b572b322e62',
}
TARGET = F(1, 10**12)
SAMPLES = ('0', '1/8', '1/4', '12/43', '1/3', '3/8', '2/5', '1/2')
REQUIRED_PREMISES = {
    'physical_space': 'full untruncated L2(SU2^20) with Gauss at all twelve vertices and no charges',
    'P_basis': 'bare vacuum and all eleven orthonormal fundamental face characters',
    'Q_electric_lower_over_alpha': '9/2',
    'P_face_electric_over_alpha': '3',
    'P_face_magnetic_quadratic_form': '0',
    'cross_norm_squared_over_alpha_squared_r_squared_upper': '21/4',
    'vacuum_trial_energy': '0',
    'codimension_one_space': 'psi perpendicular to the bare vacuum, not necessarily the interacting ground',
    'cross_is_full_QVP': True,
    'complement_is_full_Q': True,
    'graph_sha256': PREMISE_FILES['graph.json'],
}
_CONFIG_SNAPSHOT = json.dumps([PREMISE_FILES, REQUIRED_PREMISES, str(TARGET), SAMPLES],
                              sort_keys=True, separators=(',', ':'))


def rational(value):
    if type(value) is not str or len(value) > 1000:
        raise ValueError('canonical rational string required')
    try:
        result = F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('invalid rational') from exc
    if str(result) != value:
        raise ValueError('noncanonical rational')
    return result


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def premises(candidate=None):
    """Validate immutable source-backed premises; no caller-created pass labels."""
    root = Path(__file__).parent
    if Path(__file__).read_bytes() != SOURCE_BYTES:
        raise ValueError('loaded proof source changed')
    if canonical([PREMISE_FILES, REQUIRED_PREMISES, str(TARGET), SAMPLES]) != _CONFIG_SNAPSHOT:
        raise ValueError('loaded premise, source-pin, precision or sample declarations changed')
    for name, digest in PREMISE_FILES.items():
        if hashlib.sha256((root/'premises'/name).read_bytes()).hexdigest() != digest:
            raise ValueError('frozen B1 premise bytes changed: '+name)
    gate = json.loads((root/'premises'/'b1-gate.json').read_text())
    if gate['status'] != 'accepted' or gate['loop'] != 'b1':
        raise ValueError('B1 is not accepted')
    if gate['files']['forward/b1/report.md'] != PREMISE_FILES['b1-report.md']:
        raise ValueError('B1 proof is not bound to its gate')
    if candidate is not None and canonical(candidate) != canonical(REQUIRED_PREMISES):
        raise ValueError('missing or modified full-operator premise')
    return json.loads(canonical(REQUIRED_PREMISES))


def sqrt_bracket(value, bits=48):
    """Exact rational-square recognition, otherwise outward dyadic isqrt."""
    if type(bits) is not int or not 0 <= bits <= 256:
        raise ValueError('exact integer precision from zero through 256 required')
    q = rational(value)
    if q < 0:
        raise ValueError('negative square root')
    n, d = math.isqrt(q.numerator), math.isqrt(q.denominator)
    if n*n == q.numerator and d*d == q.denominator:
        return F(n, d), F(n, d)
    denominator = 1 << bits
    k = math.isqrt(q.numerator*denominator*denominator // q.denominator)
    lo, hi = F(k, denominator), F(k+1, denominator)
    if not (0 <= lo and lo*lo <= q <= hi*hi):
        raise RuntimeError('outward root bracket failed')
    return lo, hi


def interval(lo, hi):
    if lo > hi:
        raise ValueError('reversed interval')
    return {'lower': str(lo), 'upper': str(hi), 'width': str(hi-lo)}


def bounds(item):
    return F(item['lower']), F(item['upper'])


def scale(item, factor):
    lo, hi = bounds(item)
    if factor <= 0:
        raise ValueError('positive physical scale required')
    return interval(factor*lo, factor*hi)


def constants(bits=48):
    a, b = sqrt_bracket('70', bits)
    c, d = sqrt_bracket('3', bits)
    return {
        'sqrt70': interval(a, b), 'sqrt3': interval(c, d),
        'R_star': interval((27-3*b)/16, (27-3*a)/16),
        'star_E0_upper_formula': interval((24-15*d)/16, (24-15*c)/16),
        'D_star': interval((3+15*c-3*b)/16, (3+15*d-3*a)/16),
        'analytic_positivity': {'R_star_squared_test': '81>70',
                               'endpoint_matrix_determinant': '99/256',
                               'star_energy_negative_squared_test': '675>576'},
    }


def scalar_bound(ratio, bits=48):
    r = rational(ratio)
    if r < 0:
        raise ValueError('nonnegative maximum absolute ratio required')
    c = F(9, 2)-11*r
    b2 = 21*r*r/4
    q = (3-c)**2+4*b2
    lo, hi = sqrt_bracket(str(q), bits)
    lower, upper = (3+c-hi)/2, (3+c-lo)/2
    # PSD shift is checked without floating radicals, including b=0.
    determinant = (3-lower)*(c-lower)-b2
    if 3-lower < 0 or c-lower < 0 or determinant < 0:
        raise RuntimeError('rational scalar lower shift is not positive semidefinite')
    return {
        'r': str(r), 'c': str(c), 'b_squared': str(b2),
        'discriminant': str(q), 'sqrt_discriminant': interval(lo, hi),
        'R': interval(lower, upper), 'lower_shift_determinant': str(determinant),
        'box_member': r <= F(3, 8),
        'bound_status': 'positive' if lower > 0 else 'zero-insufficient' if lower == 0 else 'negative-insufficient',
    }


def certify(alpha, couplings, bits=48, alpha_min=None, claim_box=False, proof_premises=None):
    accepted = premises(proof_premises)
    a = rational(alpha)
    if a <= 0:
        raise ValueError('alpha must be positive')
    if type(couplings) not in (list, tuple) or len(couplings) != 11:
        raise ValueError('all eleven signed physical coefficients required')
    ls = [rational(x) for x in couplings]
    if type(claim_box) is not bool:
        raise ValueError('claim_box must be Boolean')
    amin = None if alpha_min is None else rational(alpha_min)
    if amin is not None and not 0 < amin <= a:
        raise ValueError('declared alpha_min must satisfy zero < alpha_min <= alpha')
    r = max(map(abs, ls))/a
    member = r <= F(3, 8)
    if claim_box and not member:
        raise ValueError('coefficient vector is outside the accepted signed box')
    scalar = scalar_bound(str(r), bits)
    const = constants(bits)
    qsum = sum((x*x for x in ls), F(0))
    qlo, qhi = sqrt_bracket(str(9*a*a+qsum), bits)
    e0 = interval((3*a-qhi)/2, (3*a-qlo)/2)
    e1 = scale(scalar['R'], a)
    elo, ehi = bounds(e1)
    glo, ghi = bounds(e0)
    combined = interval(elo-ghi, ehi-glo)
    endpoint = all(abs(x) == F(3, 8)*a for x in ls)
    whole = scale(const['R_star'], a) if member else None
    common = scale(const['R_star'], amin) if member and amin is not None else None
    if common is not None and F(common['lower']) < 0:
        # Positive analytic constant is known, but this enclosure is insufficient;
        # no negative coefficient is promoted using only a lower alpha bound.
        common = interval(F(0), F(common['upper']))
    return {
        'schema': 'ym18-b2-certificate-v1', 'source_sha256': SOURCE_SHA,
        'premise_sha256': PREMISE_FILES.copy(), 'proof_premises': accepted,
        'alpha': str(a), 'alpha_min': None if amin is None else str(amin),
        'couplings': list(map(str, ls)), 'precision_bits': bits,
        'requested_dimensionless_width': str(TARGET), 'claim_box': claim_box,
        'maximum_absolute_ratio': str(r), 'sum_absolute_couplings': str(sum(map(abs, ls))),
        'sum_coupling_squares': str(qsum), 'box_member': member,
        'all_endpoint_magnitudes': endpoint, 'scalar_comparison': scalar,
        'constants': const, 'full_E1_lower_formula_interval': e1,
        'star_E0_upper_formula_interval': e0,
        'instance_gap_lower_formula_interval': combined,
        'whole_box_gap_lower_formula_interval': whole,
        'common_scale_gap_lower_formula_interval': common,
        'endpoint_gap_lower_formula_interval': scale(const['D_star'], a) if endpoint else None,
        'analytic_box_status': 'positive-proved' if member else 'outside-selected-box',
        'whole_box_enclosure_status': ('not-applicable' if not member else
            'positive-target-met' if F(const['R_star']['lower']) > 0 and F(const['R_star']['width']) <= TARGET
            else 'insufficient-precision'),
        'endpoint_enclosure_status': ('not-applicable' if not endpoint else
            'positive-target-met' if F(const['D_star']['lower']) > 0 and F(const['D_star']['width']) <= TARGET
            else 'insufficient-precision'),
        'interval_semantics': 'Intervals enclose analytic lower-bound formulas or trial-energy formulas; no upper endpoint bounds the physical gap from above.',
        'scope': 'fixed actual two-cube physical operator; no homogeneous volume-uniform or continuum conclusion',
    }


def verify(certificate):
    if type(certificate) is not dict:
        raise ValueError('certificate object required')
    try:
        expected = certify(certificate['alpha'], certificate['couplings'], certificate['precision_bits'],
                           certificate['alpha_min'], certificate['claim_box'], certificate['proof_premises'])
    except KeyError as exc:
        raise ValueError('incomplete certificate') from exc
    if canonical(certificate) != canonical(expected):
        raise ValueError('certificate content mismatch')
    return True


def fixture_inputs():
    endpoint = ['3/8']*11
    return [
        ('allzero', '1', ['0']*11, 48, None, True),
        ('endpoint_allplus', '1', endpoint, 48, None, True),
        ('endpoint_allminus', '1', ['-3/8']*11, 48, None, True),
        ('endpoint_alternating', '1', ['3/8' if i % 2 == 0 else '-3/8' for i in range(11)], 48, None, True),
        ('sparse_interior', '1', ['1/8']+['0']*10, 48, None, True),
        ('mixed_signed_interior', '1', ['1/8', '-1/16', '0', '3/32', '0', '-1/32']+['0']*5, 48, None, True),
        ('scaled_double', '2', ['3/4']*11, 48, '1', True),
        ('scaled_half', '1/2', ['3/16']*11, 48, '1/4', True),
        ('coarse_endpoint', '1', endpoint, 0, None, True),
        ('outside_two_fifths', '1', ['2/5']*11, 48, None, False),
        ('outside_one_half', '1', ['1/2']*11, 48, None, False),
    ]


def controls():
    return {
        'deleted_cross_scalar': {
            'vector': '(1,sqrt(21))', 'norm_squared': '22', 'true_scalar_form': '3',
            'true_scalar_Rayleigh': '3/22', 'false_diagonal_lower': '3/8',
            'scope': 'counterexample to a scalar inference, not a computed physical excited state'},
        'missing_codimension_one': {'state': 'bare vacuum', 'actual_P_quadratic_form': '0', 'false_face_only_lower_over_alpha': '3'},
        'missing_P_face': {'actual_omitted_face_energy_over_alpha': '3', 'false_complement_lower_over_alpha': '9/2'},
        'Ritz_gap_substitution': {'full_diagonal': ['0', '1/8', '3'], 'trial_indices': [0, 2],
                                  'full_gap': '1/8', 'Ritz_gap': '3', 'scope': 'separate generic finite-matrix inference counterexample'},
        'coarse_radical_failure': {'bits': 0, 'R_star': constants(0)['R_star'], 'D_star': constants(0)['D_star'],
                                   'meaning': 'actual requested precision failure, not a theorem counterexample'},
        'matching': {'alpha': 'g^2/(2a)', 'lambda': '2/(g^2 a)', 'ratio': '4/g^4',
                     'box_condition': 'g^4>=32/3', 'weak_bare_limit_admitted': False,
                     'meaning': 'applicability obstruction for this bound, not absence of a continuum mass gap'},
    }


def collection():
    return {
        'schema': 'ym18-b2-collection-v1', 'source_sha256': SOURCE_SHA,
        'premise_sha256': PREMISE_FILES.copy(), 'physical_contract': premises(),
        'precision_bits': 48, 'dimensionless_width_target': str(TARGET),
        'frozen_box': {'coefficient_count': 11, 'maximum_absolute_ratio': '3/8', 'coverage': 'analytic whole signed box, not sampled coverage'},
        'constants': constants(48),
        'fixtures': [{'id': name, 'certificate': certify(a, ls, bits, amin, claim)}
                     for name, a, ls, bits, amin, claim in fixture_inputs()],
        'samples': [scalar_bound(r, 48) for r in SAMPLES], 'controls': controls(),
    }


def verify_collection(value):
    if type(value) is not dict or canonical(value) != canonical(collection()):
        raise ValueError('complete frozen B2 collection mismatch')
    return True
