"""Exact S3 polynomial integration with complete finite-action remainder bounds."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import math
import geometry

SOURCE_BYTES = Path(__file__).read_bytes()
SOURCE_SHA = hashlib.sha256(SOURCE_BYTES).hexdigest()
GEOMETRY_SHA = '0b59a11ceae543e2a5683609797bf06e6d0112cef784cf67e32a93b72c0c7a2f'
DEGREES = (0, 4, 8, 12, 16)
PRECISION = F(1, 10**12)
TETRA = tuple(tuple(str(x) for x in q) for q in geometry.TETRAHEDRAL)
COMMUTING = (('1', '0', '0', '0'), ('1', '0', '0', '0'),
             ('0', '1', '0', '0'), ('0', '-1', '0', '0'))


def unchanged():
    if Path(__file__).read_bytes() != SOURCE_BYTES:
        raise ValueError('conditional source changed after load')
    if geometry.SOURCE_SHA != GEOMETRY_SHA or hashlib.sha256(
            (Path(__file__).parent / 'geometry.py').read_bytes()).hexdigest() != GEOMETRY_SHA:
        raise ValueError('frozen central geometry changed')


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


def degree(value):
    if type(value) is not int or not 0 <= value <= 16:
        raise ValueError('integer Taylor degree from zero through sixteen required')
    return value


def boundaries(values):
    if type(values) not in (list, tuple) or len(values) != 4:
        raise ValueError('four boundary quaternions required')
    result = []
    for row in values:
        if type(row) not in (list, tuple) or len(row) != 4:
            raise ValueError('four coordinates per boundary quaternion required')
        result.append(geometry.quaternion(tuple(rational(x) for x in row)))
    return tuple(result)


def parameters(hs, kappas, order):
    unchanged()
    n = degree(order)
    h = boundaries(hs)
    if type(kappas) not in (list, tuple) or len(kappas) != 4:
        raise ValueError('four individual Euclidean coefficients required')
    k = tuple(rational(x) for x in kappas)
    directions = tuple((q[0], -q[1], -q[2], -q[3]) for q in h)
    b = tuple(sum((k[i] * directions[i][j] for i in range(4)), F(0)) for j in range(4))
    if any(b[1:]):
        raise ValueError('this certified routine requires scalar-axis action; directions are not silently rotated')
    if abs(b[0]) >= n + 2:
        raise ValueError('geometric remainder requires action magnitude below N+2')
    return h, k, directions, b, n


def sphere_moment(powers):
    if type(powers) not in (list, tuple) or len(powers) != 4 or any(
            type(v) is not int or v < 0 for v in powers) or sum(powers) > 24:
        raise ValueError('four nonnegative integer powers with total at most twenty-four required')
    return _sphere_moment(tuple(powers))


@lru_cache(maxsize=None)
def _sphere_moment(powers):
    if any(p % 2 for p in powers):
        return F(0)
    half = [p // 2 for p in powers]
    total = sum(half)
    return F(math.prod(math.factorial(2*a) for a in half),
             4**total * math.prod(math.factorial(a) for a in half) * math.factorial(total + 1))


def poly_product(left, right):
    result = {}
    for a, x in left.items():
        for b, y in right.items():
            key = tuple(u + v for u, v in zip(a, b))
            result[key] = result.get(key, F(0)) + x*y
    return {k: v for k, v in result.items() if v}


@lru_cache(maxsize=None)
def _observable(hs):
    result = {(0, 0, 0, 0): F(1, 81)}
    for h in hs:
        a = (h[0], -h[1], -h[2], -h[3])
        linear = {}
        for j, value in enumerate(a):
            powers = [0]*4
            powers[j] = 1
            if value:
                linear[tuple(powers)] = value
        factor = {key: 4*value for key, value in poly_product(linear, linear).items()}
        factor[(0, 0, 0, 0)] = -F(1)
        result = poly_product(result, factor)
    return tuple(sorted(result.items()))


def observable(hs):
    unchanged()
    return _observable(boundaries(hs))


def integrate(poly, scalar_power=0):
    scalar_power = degree(scalar_power)
    if type(poly) not in (tuple, list):
        raise ValueError('explicit polynomial term sequence required')
    for term in poly:
        if type(term) not in (tuple, list) or len(term) != 2:
            raise ValueError('polynomial terms require powers and coefficient')
        powers, coefficient = term
        if type(powers) not in (tuple, list) or len(powers) != 4 or any(
                type(p) is not int or p < 0 for p in powers) or sum(powers) > 8:
            raise ValueError('four nonnegative integer polynomial powers of total at most eight required')
        if type(coefficient) is not F:
            raise ValueError('exact rational polynomial coefficient required')
    return sum((coefficient * sphere_moment((powers[0] + scalar_power,) + tuple(powers[1:]))
                for powers, coefficient in poly), F(0))


def remainder(magnitude, order):
    if type(magnitude) is not F or magnitude < 0:
        raise ValueError('nonnegative rational action magnitude required')
    n = degree(order)
    if magnitude >= n + 2:
        raise ValueError('geometric remainder denominator must be positive')
    return magnitude**(n+1) / math.factorial(n+1) / (1 - magnitude/F(n+2))


def divide_interval(numerator, denominator):
    lo, hi = numerator
    dl, dh = denominator
    if lo > hi or dl <= 0 or dl > dh:
        raise ValueError('ordered numerator and positive ordered denominator required')
    values = [lo/dl, lo/dh, hi/dl, hi/dh]
    return min(values), max(values)


def realization(hs):
    h = boundaries(hs)
    graph = geometry.make_graph()
    words = geometry.central_words(graph)
    edge_map = {e['id']: e for e in graph['edges']}
    links = {e['id']: geometry.IDENTITY for e in graph['edges']}
    records = []
    for entry, target in zip(words, h):
        vertical = [term for term in entry['boundary_path'] if edge_map[term['edge']]['axis'] == 2]
        if len(vertical) != 1:
            raise ValueError('unique surrounding vertical link required')
        selected = vertical[0]
        links[selected['edge']] = target if selected['sign'] == 1 else geometry.conjugate(target)
        records.append({'face_id': entry['face_id'], 'edge': selected['edge'],
                        'sign': selected['sign'], 'target_H': list(map(str, target))})
    if any(geometry.product_word(entry['boundary_path'], links) != target
           for entry, target in zip(words, h)):
        raise ValueError('actual surrounding paths failed boundary realization')
    return {'chosen_links': records,
            'all_link_assignments': {key: list(map(str, value)) for key, value in links.items()}}


def certify(hs=TETRA, kappas=('1/8',)*4, order=16):
    h, k, directions, b, n = parameters(hs, kappas, order)
    poly = _observable(h)
    weights = [b[0]**j / math.factorial(j) for j in range(n+1)]
    numerator = [weight*integrate(poly, j) for j, weight in enumerate(weights)]
    partition = [weight*sphere_moment((j, 0, 0, 0)) for j, weight in enumerate(weights)]
    r = remainder(abs(b[0]), n)
    anum, znum = sum(numerator, F(0)), sum(partition, F(0))
    z = (max(F(1), znum-r), znum+r)
    a = (anum-r, anum+r)
    expectation = divide_interval(a, z)
    return {'schema': 'ym17-axis-conditional-v1', 'source_sha256': SOURCE_SHA,
            'geometry_source_sha256': GEOMETRY_SHA,
            'boundary_H': [list(map(str, row)) for row in h], 'kappas': list(map(str, k)), 'degree': n,
            'trace_directions': [list(map(str, row)) for row in directions],
            'direction_gram': [[str(sum((x*y for x, y in zip(p, q)), F(0))) for q in directions] for p in directions],
            'action_vector': list(map(str, b)), 'action_magnitude': str(abs(b[0])),
            'action_branch': 'zero-vector Haar' if not any(b) else 'scalar-axis',
            'observable_polynomial': [[list(p), str(c)] for p, c in poly],
            'numerator_coefficients': list(map(str, numerator)), 'partition_coefficients': list(map(str, partition)),
            'numerator_partial': str(anum), 'partition_partial': str(znum), 'tail': str(r),
            'numerator_interval': list(map(str, a)), 'partition_interval': list(map(str, z)),
            'expectation_interval': list(map(str, expectation)), 'width': str(expectation[1]-expectation[0]),
            'precision': str(PRECISION), 'precision_status': 'target-met' if expectation[1]-expectation[0] <= PRECISION else 'insufficient-width',
            'sign_status': 'positive' if expectation[0] > 0 else 'negative' if expectation[1] < 0 else 'sign-inconclusive',
            'actual_boundary_realization': realization(hs),
            'scope': 'Finite central-link conditional integral on the actual four-cube graph, axis-aligned action, normalized adjoint product; not a bulk result or a physical spectral gap'}


def verify(certificate):
    if type(certificate) is not dict or certificate.get('schema') != 'ym17-axis-conditional-v1':
        raise ValueError('wrong conditional certificate schema')
    expected = certify(certificate.get('boundary_H'), certificate.get('kappas'), certificate.get('degree'))
    if not geometry.strict_equal(certificate, expected):
        raise ValueError('conditional coefficient, boundary or interval replay failed')
    return True


def contrast(tetra, commuting):
    verify(tetra)
    verify(commuting)
    if tetra['degree'] != commuting['degree'] or tetra['action_vector'] != commuting['action_vector']:
        raise ValueError('matched action and Taylor degree required')
    if tetra['partition_coefficients'] != commuting['partition_coefficients']:
        raise ValueError('matched partition coefficients required')
    d = F(commuting['numerator_partial']) - F(tetra['numerator_partial'])
    tail = F(commuting['tail']) + F(tetra['tail'])
    interval = divide_interval((d-tail, d+tail), tuple(map(F, tetra['partition_interval'])))
    width = interval[1] - interval[0]
    return {'degree': tetra['degree'], 'definition': 'commuting expectation minus tetrahedral expectation',
            'common_action_vector': tetra['action_vector'], 'common_partition_interval': tetra['partition_interval'],
            'numerator_difference_partial': str(d), 'numerator_difference_tail': str(tail),
            'interval': list(map(str, interval)), 'width': str(width),
            'sign_status': 'positive' if interval[0] > 0 else 'negative' if interval[1] < 0 else 'sign-inconclusive',
            'precision_status': 'target-met' if width <= PRECISION else 'insufficient-width'}


def individual_angular_polynomials(hs):
    """Coefficients of 1 and q0 squared after scalar-axis rotational averaging."""
    result = []
    for h in boundaries(hs):
        spatial_squared = sum((x*x for x in h[1:]), F(0))
        result.append(((4*spatial_squared/3 - 1)/3,
                       4*(h[0]*h[0] - spatial_squared/3)/3))
    return tuple(result)


def collection():
    unchanged()
    refinements = []
    for n in DEGREES:
        t, c = certify(TETRA, ('1/8',)*4, n), certify(COMMUTING, ('1/8',)*4, n)
        d = contrast(t, c)
        accepted = t['precision_status'] == c['precision_status'] == d['precision_status'] == 'target-met'
        accepted &= t['sign_status'] == 'negative' and c['sign_status'] == d['sign_status'] == 'positive'
        refinements.append({'degree': n, 'tetrahedral': t, 'commuting': c, 'contrast': d,
                            'status': 'accepted' if accepted else 'insufficient'})
    fixtures = []
    for name, hs, ks in [('zero_tetrahedral', TETRA, ('0',)*4), ('zero_commuting', COMMUTING, ('0',)*4),
                         ('negative_tetrahedral', TETRA, ('-1/8',)*4), ('negative_commuting', COMMUTING, ('-1/8',)*4),
                         ('half_tetrahedral', TETRA, ('1/16',)*4), ('half_commuting', COMMUTING, ('1/16',)*4),
                         ('zero_b_nonzero_coefficients', COMMUTING, ('1/8', '-1/8', '1/8', '1/8'))]:
        fixtures.append({'id': name, 'certificate': certify(hs, ks, 16)})
    final = refinements[-1]
    cached = final['tetrahedral']['expectation_interval']
    actual = final['commuting']['expectation_interval']
    shortcut = {'definition': 'cache the joint observable using only b and reuse the tetrahedral value for the commuting boundary',
                'same_action': final['tetrahedral']['action_vector'] == final['commuting']['action_vector'],
                'same_partition': final['tetrahedral']['partition_interval'] == final['commuting']['partition_interval'],
                'predicted_commuting_interval': cached, 'actual_commuting_interval': actual,
                'intervals_disjoint': F(cached[1]) < F(actual[0]) or F(actual[1]) < F(cached[0]),
                'status': 'rejected' if F(cached[1]) < F(actual[0]) else 'not-resolved'}
    return {'schema': 'ym17-c2-collection-v1', 'source_sha256': SOURCE_SHA,
            'degree_sequence': list(DEGREES), 'precision': str(PRECISION),
            'refinements': refinements, 'fixtures': fixtures,
            'tetrahedral_individual_angular_polynomials': [list(map(str, row)) for row in individual_angular_polynomials(TETRA)],
            'action_only_cache_control': shortcut,
            'status': refinements[-1]['status'],
            'scope': 'Same central action and partition with distinct boundary-dependent joint observables; no action-only observable closure or bulk/spectral conclusion'}


def verify_collection(evidence):
    if not geometry.strict_equal(evidence, collection()):
        raise ValueError('required fixture inventory, refinements or evidence failed replay')
    return True
