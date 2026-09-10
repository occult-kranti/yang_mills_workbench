"""Actual four-cube complex and its complete four-adjoint Haar projector."""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from pathlib import Path
import hashlib
import math

SOURCE_BYTES = Path(__file__).read_bytes()
SOURCE_SHA = hashlib.sha256(SOURCE_BYTES).hexdigest()
IDENTITY = (F(1), F(0), F(0), F(0))
TETRAHEDRAL = tuple(tuple(F(x, 2) for x in signs) for signs in
                    ((1, 1, 1, 1), (1, 1, -1, -1),
                     (1, -1, 1, -1), (1, -1, -1, 1)))


def unchanged():
    if Path(__file__).read_bytes() != SOURCE_BYTES:
        raise ValueError('central source changed after load')


def strict_equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(strict_equal(a[k], b[k]) for k in b)
    if type(a) is list:
        return len(a) == len(b) and all(strict_equal(x, y) for x, y in zip(a, b))
    return a == b


def vertex_name(v):
    return ','.join(map(str, v))


def make_graph():
    unchanged()
    extents = (3, 3, 2)
    vertices = [vertex_name(v) for v in product(*(range(n) for n in extents))]
    edges = []
    for v in product(*(range(n) for n in extents)):
        for axis, extent in enumerate(extents):
            if v[axis] + 1 < extent:
                w = list(v)
                w[axis] += 1
                edges.append({'id': 'e' + str(axis) + ':' + vertex_name(v),
                              'tail': vertex_name(v), 'head': vertex_name(w), 'axis': axis})
    lookup = {(e['tail'], e['head']): (e['id'], 1) for e in edges}
    lookup.update({(e['head'], e['tail']): (e['id'], -1) for e in edges})
    faces = []
    for normal in range(3):
        axes = [a for a in range(3) if a != normal]
        ranges = [range(extents[a] if a == normal else extents[a] - 1) for a in range(3)]
        for base in product(*ranges):
            first = list(base)
            first[axes[0]] += 1
            opposite = first.copy()
            opposite[axes[1]] += 1
            last = list(base)
            last[axes[1]] += 1
            loop = list(map(vertex_name, (base, first, opposite, last)))
            word = [{'edge': lookup[(loop[i], loop[(i + 1) % 4])][0],
                     'sign': lookup[(loop[i], loop[(i + 1) % 4])][1]} for i in range(4)]
            adjacent = []
            for x, y in product(range(2), range(2)):
                cell = (x, y, 0)
                if base[normal] in (cell[normal], cell[normal] + 1) and all(
                        base[a] == cell[a] for a in axes):
                    adjacent.append('c:' + vertex_name(cell))
            faces.append({'id': 'f' + str(normal) + ':' + vertex_name(base),
                          'normal': normal, 'base': list(base), 'vertices': loop,
                          'word': word, 'incident_cells': adjacent})
    cells = [{'id': 'c:' + vertex_name((x, y, 0)), 'base': [x, y, 0],
              'faces': [f['id'] for f in faces if 'c:' + vertex_name((x, y, 0)) in f['incident_cells']]}
             for x, y in product(range(2), range(2))]
    return {'schema': 'ym17-four-cube-complex-v1', 'vertices': vertices,
            'edges': edges, 'faces': faces, 'cells': cells,
            'group': 'SU(2)', 'measure': 'normalized Haar on the central link conditional on all other links',
            'scope': 'Static conditional central-link tensor; not a bulk amplitude or a physical Hamiltonian gap'}


def word_endpoints(word, edge_map):
    endpoints = []
    if type(word) is not list or not word:
        raise ValueError('nonempty signed word required')
    for term in word:
        if type(term) is not dict or set(term) != {'edge', 'sign'}:
            raise ValueError('invalid signed word entry')
        if type(term['sign']) is not int or term['sign'] not in (-1, 1):
            raise ValueError('integer orientation sign required')
        if term['edge'] not in edge_map:
            raise ValueError('unknown edge')
        edge = edge_map[term['edge']]
        endpoints.append((edge['tail'], edge['head']) if term['sign'] == 1
                         else (edge['head'], edge['tail']))
    if any(endpoints[i][1] != endpoints[(i + 1) % len(endpoints)][0]
           for i in range(len(endpoints))):
        raise ValueError('signed boundary word is not closed')
    return endpoints


def validate_graph(g):
    unchanged()
    if not strict_equal(g, make_graph()):
        raise ValueError('graph differs from the canonical four-cube contract')
    edges = {e['id']: e for e in g['edges']}
    incidence = {edge: [] for edge in edges}
    for i, face in enumerate(g['faces']):
        ends = word_endpoints(face['word'], edges)
        if [a for a, b in ends] != face['vertices'] or len(set(face['vertices'])) != 4:
            raise ValueError('face vertices disagree with its signed square')
        for term in face['word']:
            incidence[term['edge']].append(i)
    if any(len(cell['faces']) != 6 for cell in g['cells']):
        raise ValueError('each actual cube must have six faces')
    return incidence


def geometry(g=None):
    if g is None:
        g = make_graph()
    incidence = validate_graph(g)
    central = [edge for edge, fs in incidence.items() if len(fs) == 4]
    if len(central) != 1:
        raise ValueError('unique four-face central link required')
    outer_faces = [f for f in g['faces'] if len(f['incident_cells']) == 1]
    outer_edges = sorted({term['edge'] for face in outer_faces for term in face['word']})
    edge_map = {e['id']: e for e in g['edges']}
    outer_vertices = sorted({v for name in outer_edges for v in (edge_map[name]['tail'], edge_map[name]['head'])})
    return {'central_edge': central[0], 'central_face_indices': incidence[central[0]],
            'outer_face_ids': [f['id'] for f in outer_faces], 'outer_edge_ids': outer_edges,
            'outer_vertices': outer_vertices,
            'internal_face_ids': [f['id'] for f in g['faces'] if len(f['incident_cells']) == 2]}


def central_words(g=None):
    if g is None:
        g = make_graph()
    info = geometry(g)
    output = []
    for face_index in info['central_face_indices']:
        original = g['faces'][face_index]['word']
        sign = next(t['sign'] for t in original if t['edge'] == info['central_edge'])
        word = ([{'edge': t['edge'], 'sign': -t['sign']} for t in original[::-1]]
                if sign == -1 else [dict(t) for t in original])
        offset = next(i for i, t in enumerate(word) if t['edge'] == info['central_edge'])
        word = word[offset:] + word[:offset]
        output.append({'face_index': face_index, 'face_id': g['faces'][face_index]['id'],
                       'whole_face_reversed': sign == -1, 'word': word,
                       'boundary_path': word[1:]})
    return output


def quaternion(q):
    if type(q) not in (tuple, list) or len(q) != 4 or any(type(x) is not F for x in q):
        raise ValueError('four exact rational quaternion coordinates required')
    if sum((x*x for x in q), F(0)) != 1:
        raise ValueError('unit quaternion required')
    return tuple(q)


def multiply(p, q):
    p, q = quaternion(p), quaternion(q)
    a, b, c, d = p
    e, f, g, h = q
    return (a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)


def conjugate(q):
    q = quaternion(q)
    return (q[0], -q[1], -q[2], -q[3])


def rotation(q):
    a, b, c, d = quaternion(q)
    return ((1-2*(c*c+d*d), 2*(b*c-a*d), 2*(b*d+a*c)),
            (2*(b*c+a*d), 1-2*(b*b+d*d), 2*(c*d-a*b)),
            (2*(b*d-a*c), 2*(c*d+a*b), 1-2*(b*b+c*c)))


def product_word(word, links):
    value = IDENTITY
    for term in word:
        q = links[term['edge']]
        value = multiply(value, q if term['sign'] == 1 else conjugate(q))
    return value


def realize_boundary(central_value=IDENTITY):
    g = make_graph()
    info = geometry(g)
    words = central_words(g)
    edge_map = {e['id']: e for e in g['edges']}
    links = {e['id']: IDENTITY for e in g['edges']}
    links[info['central_edge']] = quaternion(central_value)
    choices = []
    used = set()
    for entry, holonomy in zip(words, TETRAHEDRAL):
        path = entry['boundary_path']
        support = {t['edge'] for t in path}
        if len(support) != 3 or used & support:
            raise ValueError('surrounding paths are not disjoint outside the central edge')
        used |= support
        vertical = [t for t in path if edge_map[t['edge']]['axis'] == 2]
        if len(vertical) != 1:
            raise ValueError('one outer vertical link per surrounding path required')
        chosen = vertical[0]
        links[chosen['edge']] = holonomy if chosen['sign'] == 1 else conjugate(holonomy)
        choices.append({'edge': chosen['edge'], 'path_sign': chosen['sign'],
                        'target_H': list(map(str, holonomy)), 'face_id': entry['face_id']})
    return links, choices


INDICES = tuple(product(range(3), repeat=4))


def transpose(matrix):
    return tuple(zip(*matrix))


def matmul(left, right):
    columns = transpose(right)
    return tuple(tuple(sum((a*b for a, b in zip(row, col) if a and b), F(0))
                       for col in columns) for row in left)


@lru_cache(maxsize=1)
def invariant_data():
    basis = tuple((F(a == b and c == d), F(a == c and b == d), F(a == d and b == c))
                  for a, b, c, d in INDICES)
    gram = matmul(transpose(basis), basis)
    inverse = tuple(tuple(F(2, 15) if i == j else F(-1, 30) for j in range(3)) for i in range(3))
    projector = matmul(matmul(basis, inverse), transpose(basis))
    diagonal_only = tuple(tuple(inverse[i][j] if i == j else F(0) for j in range(3)) for i in range(3))
    wrong = matmul(matmul(basis, diagonal_only), transpose(basis))
    channel_one = tuple(tuple(F(1, 9) if i == j == 0 else F(0) for j in range(3)) for i in range(3))
    one = matmul(matmul(basis, channel_one), transpose(basis))
    return basis, gram, inverse, projector, wrong, one


def tensor(rotations):
    if len(rotations) != 4:
        raise ValueError('four rotation matrices required')
    return tuple(tuple(math.prod(rotations[k][i[k]][j[k]] for k in range(4))
                       for j in INDICES) for i in INDICES)


def contract(projector, boundaries=TETRAHEDRAL):
    if type(boundaries) not in (tuple, list) or len(boundaries) != 4:
        raise ValueError('four boundary holonomies required')
    matrices = [rotation(q) for q in boundaries]
    return sum((projector[a][b] * math.prod(matrices[k][j[k]][i[k]] for k in range(4))
                for a, i in enumerate(INDICES) for b, j in enumerate(INDICES) if projector[a][b]), F(0)) / 81


def certify():
    unchanged()
    basis, gram, inverse, projector, wrong, one = invariant_data()
    g = make_graph()
    info = geometry(g)
    links, choices = realize_boundary()
    return {'schema': 'ym17-central-four-adjoint-v1', 'source_sha256': SOURCE_SHA,
            'graph': g, 'geometry': info, 'central_words': central_words(g),
            'boundary_assignments': {key: list(map(str, value)) for key, value in links.items()},
            'chosen_boundary_links': choices, 'boundary_H': [list(map(str, q)) for q in TETRAHEDRAL],
            'tensor_index_order': [list(i) for i in INDICES],
            'basis': [[str(x) for x in row] for row in basis],
            'gram': [[str(x) for x in row] for row in gram],
            'gram_inverse': [[str(x) for x in row] for row in inverse],
            'projector': [[str(x) for x in row] for row in projector],
            'invariant_dimension': 3, 'pair_channels': [0, 1, 2],
            'adjoint_normalization_per_face': '3',
            'conditional_joint': str(contract(projector)),
            'wrong_diagonal_inverse_joint': str(contract(wrong)),
            'wrong_one_channel_joint': str(contract(one)),
            'individual_conditional_means': ['0'] * 4,
            'central_action': '0', 'C2_nonzero_action': 'not executed',
            'scope': 'Complete central-link conditional Haar tensor and realizable fixed boundary; not twenty-face bulk integration or a spectral theorem'}


def verify(certificate):
    if not strict_equal(certificate, certify()):
        raise ValueError('central tensor or boundary contract failed exact replay')
    return True
