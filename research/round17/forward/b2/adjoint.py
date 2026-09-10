"""Exact shared-face adjoint Rayleigh repair of a finite spectral bound."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import haar_graph

SOURCE_BYTES = Path(__file__).read_bytes()
SOURCE_SHA = hashlib.sha256(SOURCE_BYTES).hexdigest()
HAAR_SHA = '13a82e2b804f07d7dbe8951f600ded429d4924b042162ec79d60c2889b767a80'
GRAPH_SHA = '9e630191189fb3f69145e5cdbc91eceac138f95d44d7bed825b87b572b322e62'
RATIO = F(12, 43)
G = F(45, 44)
ETA_MAX = F(6, 3817)
ETA_SELECTED = F(3, 3817)


def unchanged():
    root = Path(__file__).parent
    if Path(__file__).read_bytes() != SOURCE_BYTES:
        raise ValueError('adjoint source changed after load')
    if hashlib.sha256((root / 'haar_graph.py').read_bytes()).hexdigest() != HAAR_SHA:
        raise ValueError('accepted Haar source changed')
    if haar_graph.SOURCE_SHA != HAAR_SHA:
        raise ValueError('unexpected loaded Haar source')
    if hashlib.sha256((root / 'graph.json').read_bytes()).hexdigest() != GRAPH_SHA:
        raise ValueError('accepted graph bytes changed')


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


def graph():
    unchanged()
    result = json.loads((Path(__file__).parent / 'graph.json').read_text())
    haar_graph.validate_graph(result)
    return result


def shared_index():
    """Locate the internal square from three-face edge incidences."""
    g = graph()
    incidence = haar_graph.validate_graph(g)
    central_edges = {edge for edge, faces in incidence.items() if len(faces) == 3}
    candidates = [i for i, face in enumerate(g['faces'])
                  if {entry['edge'] for entry in face['word']} == central_edges]
    if len(central_edges) != 4 or len(candidates) != 1:
        raise ValueError('unique shared square not derived from incidence')
    i = candidates[0]
    if g['faces'][i]['id'] != g['shared_face']:
        raise ValueError('geometric shared square disagrees with metadata')
    return i


def index(value, maximum):
    if type(value) is not int or not 0 <= value <= maximum:
        raise ValueError('bounded integer index required, not Boolean')
    return value


def basis(index_value):
    i = index(index_value, 12)
    zero = (0,) * 11
    if i == 0:
        return ((F(1), zero),)
    powers = list(zero)
    if i < 12:
        powers[i - 1] = 1
        return ((F(2), tuple(powers)),)
    powers[shared_index()] = 2
    return ((F(4), tuple(powers)), (F(-1), zero))


def matrix_moment(i, j, face=None):
    unchanged()
    i, j = index(i, 12), index(j, 12)
    if face is not None:
        face = index(face, 10)
    return _matrix_moment(i, j, face)


@lru_cache(maxsize=None)
def _matrix_moment(i, j, face):
    total = F(0)
    for a, pi in basis(i):
        for b, pj in basis(j):
            powers = [x + y for x, y in zip(pi, pj)]
            if face is not None:
                powers[face] += 1
            total += a * b * haar_graph.moment(powers)
    return total


def matrices(alpha='1'):
    a = rational(alpha)
    if a <= 0:
        raise ValueError('positive physical alpha required')
    energies = [F(0)] + [3 * a] * 11 + [8 * a]
    gram = [[matrix_moment(i, j) for j in range(13)] for i in range(13)]
    electric = [[energies[j] * gram[i][j] for j in range(13)] for i in range(13)]
    potential = [[-a * RATIO * sum((matrix_moment(i, j, f) for f in range(11)), F(0))
                  for j in range(13)] for i in range(13)]
    h = [[electric[i][j] + potential[i][j] for j in range(13)] for i in range(13)]
    return tuple(tuple(tuple(row) for row in m) for m in (gram, electric, potential, h))


def quadratic(matrix, vector):
    return sum((x * matrix[i][j] * y for i, x in enumerate(vector)
                for j, y in enumerate(vector)), F(0))


def certify(alpha='1', eta='3/3817'):
    a, t = rational(alpha), rational(eta)
    if a <= 0:
        raise ValueError('positive physical alpha required')
    gr, electric, potential, h = matrices(alpha)
    vector = [F(1)] + [F(1, 22)] * 11 + [t]
    norm = quadratic(gr, vector)
    energy_numerator = quadratic(h, vector)
    rayleigh = energy_numerator / norm
    e1_lower = 3 * a - 11 * a * RATIO
    gap_lower = e1_lower - rayleigh
    numerator = a * (F(6, 473) * t - F(347, 43) * t * t)
    if norm != G + t * t or gap_lower != numerator / norm:
        raise ValueError('matrix Rayleigh value disagrees with proposed formula')
    state = 'positive' if gap_lower > 0 else 'zero-insufficient' if gap_lower == 0 else 'negative-insufficient'
    return {
        'schema': 'ym17-shared-adjoint-rayleigh-v1',
        'source_sha256': SOURCE_SHA, 'haar_source_sha256': HAAR_SHA,
        'graph_file_sha256': GRAPH_SHA,
        'alpha': str(a), 'eta': str(t), 'common_lambda_over_alpha': str(RATIO),
        'physical_coefficients': [str(a * RATIO)] * 11,
        'face_order': [f['id'] for f in graph()['faces']],
        'shared_face_index': shared_index(),
        'shared_face_id': graph()['faces'][shared_index()]['id'],
        'trial_vector': list(map(str, vector)),
        'gram': [[str(x) for x in row] for row in gr],
        'electric_matrix': [[str(x) for x in row] for row in electric],
        'potential_matrix': [[str(x) for x in row] for row in potential],
        'trial_H': [[str(x) for x in row] for row in h],
        'trial_norm_squared': str(norm),
        'energy_numerator': str(energy_numerator),
        'full_E0_upper': str(rayleigh),
        'full_E1_lower': str(e1_lower),
        'gap_numerator': str(numerator),
        'full_gap_lower': str(gap_lower),
        'bound_status': state, 'valid_trial': True,
        'positive_amplitude_interval': ['0', str(ETA_MAX)],
        'positive_interval_open': [True, True],
        'inside_positive_amplitude_interval': F(0) < t < ETA_MAX,
        'scope': 'Finite dense two-cube untruncated physical operator; independent full E1 lower minus actual Rayleigh E0 upper; no dense volume-uniform theorem and no physical gap upper bound'
    }


def verify(certificate):
    if type(certificate) is not dict or certificate.get('schema') != 'ym17-shared-adjoint-rayleigh-v1':
        raise ValueError('wrong certificate schema')
    expected = certify(certificate.get('alpha'), certificate.get('eta'))
    if not haar_graph.strict_equal(certificate, expected):
        raise ValueError('shared-adjoint certificate failed exact replay')
    return True
