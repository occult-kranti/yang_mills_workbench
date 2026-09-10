"""Two-link conditional Wilson integral by exact SU(2) character convolution."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import itertools
import json
import math

SOURCE_BYTES = Path(__file__).read_bytes()
SOURCE_SHA = hashlib.sha256(SOURCE_BYTES).hexdigest()
MAX_MOMENT = 16
DEGREES = (0, 2, 4, 6, 8)
WEIGHTS = (2, 1, 0)
TARGET = F(1, 10**12)
_DECLARED = json.dumps([SOURCE_SHA, MAX_MOMENT, DEGREES, WEIGHTS, str(TARGET)], separators=(',', ':'))


def unchanged():
    if Path(__file__).read_bytes() != SOURCE_BYTES:
        raise ValueError('loaded source changed')
    if json.dumps([SOURCE_SHA, MAX_MOMENT, DEGREES, WEIGHTS, str(TARGET)], separators=(',', ':')) != _DECLARED:
        raise ValueError('source pin or declared scientific parameters changed')


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def rational(value):
    if type(value) is not str or len(value) > 1000:
        raise ValueError('canonical rational string required')
    try:
        q = F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('invalid rational') from exc
    if str(q) != value:
        raise ValueError('noncanonical rational')
    return q


def _index(value, upper):
    if type(value) is not int or not 0 <= value <= upper:
        raise ValueError('exact integer within the declared range required')
    return value


def multiplicity(power, index):
    unchanged()
    a = _index(power, MAX_MOMENT)
    n = _index(index, MAX_MOMENT)
    if n > a or (a-n) % 2:
        return 0
    k = (a-n)//2
    return math.comb(a, k)-(math.comb(a, k-1) if k else 0)


@lru_cache(maxsize=1024)
def _moment(a, b, c):
    return sum((F(multiplicity(a, n)*multiplicity(b, n)*multiplicity(c, n), n+1)
                for n in range(min(a, b, c)+1)), F(0))/2**(a+b+c)


def moment(exponents):
    unchanged()
    if type(exponents) not in (list, tuple) or len(exponents) != 3:
        raise ValueError('exactly three exponents required')
    a, b, c = [_index(x, MAX_MOMENT) for x in exponents]
    if a+b+c > MAX_MOMENT:
        raise ValueError('total moment degree exceeds sixteen')
    return _moment(a, b, c)


def polynomial():
    """Fresh rational terms of (4x²−1)^3(4w²−1)/81."""
    return {(2*i, 0, 2*j): F(math.comb(3, i)*4**(i+j)*(-1)**(4-i-j), 81)
            for i in range(4) for j in range(2)}


def coefficients(v_only):
    unchanged()
    d = _index(v_only, 2)
    numerator, partition = [], []
    p = polynomial()
    for degree in range(9):
        nsum, zsum = F(0), F(0)
        for a in range(degree+1):
            for b in range(degree-a+1):
                c = degree-a-b
                factor = F(3**a*d**b, math.factorial(a)*math.factorial(b)*math.factorial(c))
                zsum += factor*moment([a, b, c])
                nsum += factor*sum((weight*moment([a+i, b+j, c+k]) for (i, j, k), weight in p.items()), F(0))
        numerator.append(nsum)
        partition.append(zsum)
    return tuple(numerator), tuple(partition)


def interval(lo, hi):
    if lo > hi:
        raise ValueError('reversed interval')
    return {'lower': str(lo), 'upper': str(hi), 'width': str(hi-lo)}


def divide(num, den):
    nl, nh = map(F, (num['lower'], num['upper']))
    dl, dh = map(F, (den['lower'], den['upper']))
    if nl > nh or not 0 < dl <= dh:
        raise ValueError('ordered numerator and positive denominator required')
    corners = [n/d for n in (nl, nh) for d in (dl, dh)]
    return interval(min(corners), max(corners))


def certify(kappa, v_only=2, degree=8, target='1/1000000000000'):
    unchanged()
    k = rational(kappa)
    d = _index(v_only, 2)
    n = _index(degree, 8)
    if n not in DEGREES:
        raise ValueError('degree must belong to the frozen refinement ladder')
    accuracy = rational(target)
    if accuracy <= 0:
        raise ValueError('positive requested interval width required')
    num, den = coefficients(d)
    magnitude = (4+d)*abs(k)
    if magnitude >= n+2:
        raise ValueError('geometric Taylor tail condition fails')
    tail = magnitude**(n+1)/math.factorial(n+1)/(1-magnitude/F(n+2))
    ns = sum((num[j]*k**j for j in range(n+1)), F(0))
    zs = sum((den[j]*k**j for j in range(n+1)), F(0))
    ni = interval(ns-tail, ns+tail)
    zi = interval(max(F(1), zs-tail), zs+tail)
    expectation = divide(ni, zi)
    lower, width = F(expectation['lower']), F(expectation['width'])
    return {'schema': 'ym18-c2-certificate-v1', 'source_sha256': SOURCE_SHA,
            'kappa': str(k), 'V_only_coefficient': d, 'degree': n,
            'target_width': str(accuracy), 'action': 'kappa*(3*x+d*y+w)',
            'full_six_face_action': d == 2, 'observable': '(4*x^2-1)^3*(4*w^2-1)/81',
            'trace_definitions': {'x': 'Tr(U)/2', 'y': 'Tr(V)/2', 'w': 'Tr(U Vdagger)/2'},
            'numerator_coefficients': list(map(str, num)), 'partition_coefficients': list(map(str, den)),
            'coefficient_convention': '[kappa^n] includes all factorials; coefficient arrays through n8',
            'maximum_absolute_action': str(magnitude), 'tail': str(tail),
            'numerator_partial': str(ns), 'partition_partial': str(zs),
            'numerator_interval': ni, 'partition_interval': zi, 'expectation_interval': expectation,
            'width_target_met': width <= accuracy,
            'sign_status': 'positive' if lower > 0 else 'exact-zero' if expectation['lower'] == expectation['upper'] == '0' else 'unresolved',
            'status': 'target-met' if width <= accuracy else 'insufficient-width',
            'scope': 'normalized two-Haar-link conditional integral with all other31links fixed; no physical spectrum or full bulk claim'}


def verify(certificate):
    if type(certificate) is not dict:
        raise ValueError('certificate object required')
    try:
        expected = certify(certificate['kappa'], certificate['V_only_coefficient'], certificate['degree'], certificate['target_width'])
    except KeyError as exc:
        raise ValueError('incomplete certificate') from exc
    if canonical(certificate) != canonical(expected):
        raise ValueError('certificate differs from complete exact replay')
    return True


def _vid(x):
    return ','.join(map(str, x))


def graph():
    unchanged()
    size = (3, 3, 2)
    vertices = list(itertools.product(*(range(n) for n in size)))
    edges = []
    for axis in range(3):
        for tail in vertices:
            if tail[axis]+1 < size[axis]:
                head = list(tail)
                head[axis] += 1
                edges.append({'id': 'e'+str(axis)+':'+_vid(tail), 'axis': axis,
                              'tail': _vid(tail), 'head': _vid(head)})
    faces = []
    for first, second in ((0, 1), (0, 2), (1, 2)):
        normal = 3-first-second
        for base in vertices:
            if base[first]+1 >= size[first] or base[second]+1 >= size[second]:
                continue
            plus_first, plus_second = list(base), list(base)
            plus_first[first] += 1
            plus_second[second] += 1
            faces.append({'id': 'f'+str(normal)+':'+_vid(base), 'axes': [first, second],
                          'base': list(base), 'word': [
                              {'edge': 'e'+str(first)+':'+_vid(base), 'sign': 1},
                              {'edge': 'e'+str(second)+':'+_vid(plus_first), 'sign': 1},
                              {'edge': 'e'+str(first)+':'+_vid(plus_second), 'sign': -1},
                              {'edge': 'e'+str(second)+':'+_vid(base), 'sign': -1}]})
    return {'schema': 'ym18-c2-four-cube-graph-v1', 'vertices': list(map(_vid, vertices)), 'edges': edges,
            'faces': faces, 'variable_links': {'U': 'e2:1,1,0', 'V': 'e2:1,0,0'},
            'other_links': 'identity', 'measure': 'independent normalized Haar on U and V only'}


def validate_graph(value):
    if type(value) is not dict or canonical(value) != canonical(graph()):
        raise ValueError('actual canonical oriented graph changed')
    return True


def quaternion(value):
    if type(value) not in (list, tuple) or len(value) != 4:
        raise ValueError('four rational quaternion coordinates required')
    q = tuple(rational(x) for x in value)
    if sum((x*x for x in q), F(0)) != 1:
        raise ValueError('unit quaternion required')
    return q


def multiply(q, r):
    a, b, c, d = q
    e, f, g, h = r
    return (a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)


def conjugate(q):
    return (q[0], -q[1], -q[2], -q[3])


def realization(u, v):
    g = graph()
    U, V = quaternion(u), quaternion(v)
    identity = (F(1), F(0), F(0), F(0))
    variables = {g['variable_links']['U']: U, g['variable_links']['V']: V}
    rows = []
    for face in g['faces']:
        p = identity
        active = []
        for term in face['word']:
            q = variables.get(term['edge'], identity)
            p = multiply(p, q if term['sign'] == 1 else conjugate(q))
            if term['edge'] in variables:
                active.append(term.copy())
        seen = {x['edge'] for x in active}
        classification = 'constant' if not seen else 'x' if seen == {g['variable_links']['U']} else 'y' if seen == {g['variable_links']['V']} else 'w'
        reduced = {'constant': F(1), 'x': U[0], 'y': V[0], 'w': multiply(U, conjugate(V))[0]}[classification]
        if p[0] != reduced:
            raise ValueError('actual signed word disagrees with its trace reduction')
        rows.append({'face': face['id'], 'active_word': active, 'classification': classification,
                     'actual_trace': str(p[0]), 'reduced_trace': str(reduced)})
    return {'U': list(map(str, U)), 'V': list(map(str, V)), 'faces': rows,
            'noncommuting': multiply(U, V) != multiply(V, U)}


def geometry_evidence():
    g = graph()
    r = realization(['3/5', '4/5', '0', '0'], ['5/13', '0', '12/13', '0'])
    categories = {key: [row['face'] for row in r['faces'] if row['classification'] == key]
                  for key in ('constant', 'x', 'y', 'w')}
    edges = {e['id']: e for e in g['edges']}
    for face in g['faces']:
        endpoints = [(edges[t['edge']]['tail'], edges[t['edge']]['head']) if t['sign'] == 1
                     else (edges[t['edge']]['head'], edges[t['edge']]['tail']) for t in face['word']]
        if len({t['edge'] for t in face['word']}) != 4 or any(endpoints[i][1] != endpoints[(i+1)%4][0] for i in range(4)):
            raise ValueError('face is not a simple closed signed four-cycle')
    return {'graph_sha256': hashlib.sha256(canonical(g).encode()).hexdigest(), 'counts': [len(g['vertices']), len(g['edges']), len(g['faces'])],
            'categories': categories, 'affected_faces': [f['id'] for f in g['faces'] if f['id'] not in categories['constant']],
            'pointwise_noncommuting_fixture': r,
            'pointwise_dagger_fixture': realization(['3/5', '4/5', '0', '0'], ['3/5', '4/5', '0', '0']),
            'constant_face_terms': 14, 'removed_constant_action': '14*kappa; cancels only in this conditional quotient'}


def gram_family(y, kappa='1/64'):
    unchanged()
    s, k = rational(y), rational(kappa)
    if not -1 <= s <= 1:
        raise ValueError('surrounding scalar trace must lie in [-1,1]')
    g = [[F(0)]*5 for _ in range(5)]
    g[0][0] = k*k*(10+6*s)
    for i in range(1, 5):
        g[0][i] = g[i][0] = k*(3+s) if i < 4 else k*(3*s+1)
        for j in range(1, 5):
            g[i][j] = F(1) if (i < 4 and j < 4) or i == j else s
    if any(g[0][i] != k*sum((g[j][i] for j in range(1, 5)), F(0)) for i in range(1, 5)):
        raise RuntimeError('central action cross relation failed')
    if g[0][0] != k*k*sum((g[i][j] for i in range(1, 5) for j in range(1, 5)), F(0)):
        raise RuntimeError('central action norm relation failed')
    return {'y': str(s), 'kappa': str(k), 'gram': [[str(x) for x in row] for row in g],
            'rank': 1 if abs(s) == 1 else 2, 'direction_span_minor': str(1-s*s),
            'measure': '(2/pi)*sqrt(1-y^2) dy',
            'outer_weight': 'exp(2*kappa*y)*Z_U(G(y)) for a normalized inner observable'}


def full_moment_inventory():
    return [{'exponents': [a, b, total-a-b], 'value': str(moment([a, b, total-a-b]))}
            for total in range(MAX_MOMENT+1) for a in range(total+1) for b in range(total-a+1)]


def collection():
    unchanged()
    arrays = [{'V_only_coefficient': d, 'numerator': list(map(str, coefficients(d)[0])),
               'partition': list(map(str, coefficients(d)[1]))} for d in WEIGHTS]
    fixtures = [{'id': 'd'+str(d)+'_'+name, 'certificate': certify(k, d, 8)}
                for d in WEIGHTS for name, k in [('positive', '1/64'), ('zero', '0'), ('negative', '-1/64')]]
    frozen_mean = sum((F(math.comb(4, i)*4**i*(-1)**(4-i), 81)*moment([2*i, 0, 0]) for i in range(5)), F(0))
    return {'schema': 'ym18-c2-collection-v1', 'source_sha256': SOURCE_SHA,
            'graph': graph(), 'geometry': geometry_evidence(), 'joint_moments': full_moment_inventory(),
            'coefficient_arrays': arrays, 'refinements': [certify('1/64', 2, n) for n in DEGREES],
            'fixtures': fixtures, 'central_Gram_family': [gram_family(y) for y in ('-1', '0', '3/5', '1')],
            'frozen_V_zero_kappa_mean': str(frozen_mean),
            'controls': {
                'three_independent_traces_xyw': {'actual': str(moment([1, 1, 1])), 'wrong': '0'},
                'missing_dimension_divisor_xyw': {'actual': str(moment([1, 1, 1])), 'wrong': '1/8'},
                'uniform_y_measure_second_moment': {'actual': str(moment([0, 2, 0])), 'wrong': '1/3'},
                'pointwise_dagger': {'U_equals_V': ['3/5', '4/5', '0', '0'], 'w': '1', 'wplus': '-7/25'},
                'consistent_dagger_substitution': 'V->Vdagger preserves Haar,y and transforms wplus to w; integrated joint law is unchanged',
                'missing_inner_normalization_weight': 'normalized inner averages require outer weight exp(2*kappa*y)*Z_U(G(y)), not bare surrounding Haar',
            },
            'scope': 'conditional two-link integral; other31links fixed, all6affectedweights retained only for d2'}


def verify_collection(value):
    if type(value) is not dict or canonical(value) != canonical(collection()):
        raise ValueError('complete fixed C2 graph, moment, fixture or enclosure inventory changed')
    return True
