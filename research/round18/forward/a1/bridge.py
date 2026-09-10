"""A finite overlapping bridge bound around the actual dressed sparse reference."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

SOURCE_BYTES = Path(__file__).read_bytes()
SOURCE_SHA = hashlib.sha256(SOURCE_BYTES).hexdigest()
IDENTITY = (F(1), F(0), F(0), F(0))


def unchanged():
    if Path(__file__).read_bytes() != SOURCE_BYTES:
        raise ValueError('bridge source changed after load')


def strict_equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a) == set(b) and all(strict_equal(a[k], b[k]) for k in b)
    if type(a) is list:
        return len(a) == len(b) and all(strict_equal(x, y) for x, y in zip(a, b))
    return a == b


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


def make_graph():
    unchanged()
    vertices = [f'{x},{y},0' for x, y in product(range(4), range(2))]
    edges = []
    for x, y in product(range(4), range(2)):
        if x < 3:
            edges.append({'id': f'ex:{x},{y},0', 'tail': f'{x},{y},0', 'head': f'{x+1},{y},0', 'axis': 0})
        if y < 1:
            edges.append({'id': f'ey:{x},{y},0', 'tail': f'{x},{y},0', 'head': f'{x},{y+1},0', 'axis': 1})
    lookup = {(e['tail'], e['head']): (e['id'], 1) for e in edges}
    lookup.update({(e['head'], e['tail']): (e['id'], -1) for e in edges})
    faces = []
    for x, name in enumerate(('left', 'middle', 'right')):
        loop = [f'{x},0,0', f'{x+1},0,0', f'{x+1},1,0', f'{x},1,0']
        faces.append({'id': name, 'anchor': [x, 0, 0], 'vertices': loop,
                      'word': [{'edge': lookup[(loop[i], loop[(i+1) % 4])][0],
                                'sign': lookup[(loop[i], loop[(i+1) % 4])][1]} for i in range(4)]})
    return {'schema': 'ym18-three-square-strip-v1', 'vertices': vertices, 'edges': edges, 'faces': faces,
            'reference_end_faces': ['left', 'right'], 'bridge_face': 'middle',
            'group': 'SU(2)', 'measure': 'independent normalized Haar on all ten links',
            'Hilbert': 'full untruncated link Hilbert space first, then all-eight-vertex Gauss restriction',
            'electric_terms': 'alpha times the Casimir on every one of the ten links',
            'external_charges': False}


def signed_endpoints(word, edges):
    if type(word) is not list or len(word) != 4:
        raise ValueError('four-link square word required')
    result = []
    for term in word:
        if type(term) is not dict or set(term) != {'edge', 'sign'} or term['edge'] not in edges:
            raise ValueError('unknown signed link')
        if type(term['sign']) is not int or term['sign'] not in (-1, 1):
            raise ValueError('integer link orientation required, not Boolean')
        e = edges[term['edge']]
        result.append((e['tail'], e['head']) if term['sign'] == 1 else (e['head'], e['tail']))
    if any(result[i][1] != result[(i+1) % 4][0] for i in range(4)):
        raise ValueError('square word does not close')
    return result


def validate_graph(graph):
    unchanged()
    if not strict_equal(graph, make_graph()):
        raise ValueError('graph differs from the declared complete strip')
    edges = {e['id']: e for e in graph['edges']}
    supports = {}
    for f in graph['faces']:
        ends = signed_endpoints(f['word'], edges)
        if [a for a, b in ends] != f['vertices'] or len(set(f['vertices'])) != 4:
            raise ValueError('signed face does not match its four vertices')
        supports[f['id']] = {term['edge'] for term in f['word']}
    if supports['left'] & supports['right'] or len(supports['middle'] & supports['left']) != 1 or len(supports['middle'] & supports['right']) != 1:
        raise ValueError('incorrect end disjointness or bridge overlap')
    return supports


def haar_gate(graph, active_reference_faces):
    supports = validate_graph(graph)
    if type(active_reference_faces) is not list or any(type(f) is not str or f not in supports for f in active_reference_faces):
        raise ValueError('explicit known reference face list required')
    if len(active_reference_faces) != len(set(active_reference_faces)):
        raise ValueError('duplicate reference block')
    used = set()
    overlap = False
    for face in active_reference_faces:
        overlap |= bool(used & supports[face])
        used |= supports[face]
    untouched = sorted(supports['middle'] - used)
    valid = not overlap and bool(untouched)
    return {'active_reference_faces': active_reference_faces.copy(),
            'reference_support_overlap': overlap, 'untouched_bridge_links': untouched,
            'status': 'proved-conditional-Haar-moments' if valid else 'blocked-reference-factorization-or-free-link',
            'conditional_first_moment': '0' if valid else None,
            'conditional_second_moment': '1/4' if valid else None,
            'norm_x_times_reference_ground': '1/2' if valid else None,
            'reason': 'Haar invariance on an unused link; chi1 squared equals chi0 plus chi2'
                      if valid else 'the sharpened inference lacks its product-reference and untouched-link premises'}


def quaternion(q):
    if type(q) not in (tuple, list) or len(q) != 4 or any(type(x) is not F for x in q):
        raise ValueError('four exact rational quaternion coordinates required')
    if sum((x*x for x in q), F(0)) != 1:
        raise ValueError('unit quaternion required')
    return tuple(q)


def multiply(p, q):
    a, b, c, d = quaternion(p)
    e, f, g, h = quaternion(q)
    return (a*e-b*f-c*g-d*h, a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f, a*h+b*g-c*f+d*e)


def conjugate(q):
    q = quaternion(q)
    return (q[0], -q[1], -q[2], -q[3])


def word_value(word, links):
    value = IDENTITY
    for term in word:
        q = quaternion(links[term['edge']])
        value = multiply(value, q if term['sign'] == 1 else conjugate(q))
    return value


def certify(graph=None, parameters=None):
    unchanged()
    if graph is None:
        graph = make_graph()
    supports = validate_graph(graph)
    if parameters is None:
        parameters = {'alpha': '1', 'alpha_min': '1', 'lambda_left': '1/2', 'lambda_right': '1/2', 'mu': '1/8'}
    keys = {'alpha', 'alpha_min', 'lambda_left', 'lambda_right', 'mu'}
    if type(parameters) is not dict or set(parameters) != keys:
        raise ValueError('complete physical parameter dictionary required, including both end coefficients')
    p = {key: rational(value) for key, value in parameters.items()}
    alpha, amin, left, right, mu = [p[key] for key in ('alpha', 'alpha_min', 'lambda_left', 'lambda_right', 'mu')]
    if not 0 < amin <= alpha:
        raise ValueError('common physical energy scale must satisfy alpha >= alpha_min > 0')
    rho = max(abs(left), abs(right))/alpha
    if rho >= F(3, 4):
        raise ValueError('reference sparse ground theorem requires actual end ratio below three quarters')
    active = [name for name, coefficient in [('left', left), ('right', right)] if coefficient != 0]
    gate = haar_gate(graph, active)
    if gate['status'] != 'proved-conditional-Haar-moments':
        raise ValueError('sharpened bridge inference is blocked')
    delta = alpha*(F(3, 4)-rho)
    improved, generic = delta-abs(mu), delta-2*abs(mu)
    positive = improved > 0
    primary = rho <= F(1, 2) and abs(mu)/alpha <= F(1, 8)
    used = set().union(*(supports[f] for f in active)) if active else set()
    return {'schema': 'ym18-dressed-bridge-bound-v1', 'source_sha256': SOURCE_SHA,
            'graph_sha256': hashlib.sha256(json.dumps(graph, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
            'parameters': {key: str(p[key]) for key in sorted(p)},
            'actual_end_ratio': str(rho), 'bridge_ratio': str(abs(mu)/alpha),
            'active_reference_faces': active, 'reference_free_edges': sorted(e['id'] for e in graph['edges'] if e['id'] not in used),
            'haar_gate': gate, 'reference_ground': 'unique dressed product ground; wavefunction and absolute energy E_s not computed',
            'reference_gap_lower': str(delta),
            'bridge_offdiagonal_norm': str(abs(mu)/2), 'bridge_offdiagonal_norm_squared': str(mu*mu/4),
            'full_E1_minus_Es_lower': str(improved), 'full_E0_minus_Es_upper': '0',
            'full_gap_lower': str(improved), 'generic_two_norm_gap_lower': str(generic),
            'bound_status': 'positive' if positive else 'zero-insufficient' if improved == 0 else 'negative-insufficient',
            'ground_uniqueness_certified': positive, 'physical_Gauss_inclusion_certified': positive,
            'primary_family_member': primary,
            'primary_family_bound_at_alpha': str(alpha/8) if primary else None,
            'primary_family_common_bound': str(amin/8) if primary else None,
            'scope': 'Finite internally overlapping strip; full untruncated link bound followed by Gauss restriction; lower estimate not an actual computed spectrum; cluster repetition and dense uniform extensions unexecuted'}


def verify(graph, certificate):
    if type(certificate) is not dict or certificate.get('schema') != 'ym18-dressed-bridge-bound-v1':
        raise ValueError('wrong bridge certificate schema')
    if not strict_equal(certificate, certify(graph, certificate.get('parameters'))):
        raise ValueError('dressed bridge certificate failed exact replay')
    return True


def no_zero_mean_counterexample():
    g, t = F(1), F(1, 4)
    eigenvalues = sorted([t, g-t])
    return {'reference_H': [['0', '0'], ['0', '1']], 'perturbation': [['1/4', '0'], ['0', '-1/4']],
            'perturbation_norm': str(t), 'reference_expectation': str(t),
            'actual_gap': str(eigenvalues[1]-eigenvalues[0]), 'generic_valid_lower': str(g-2*t),
            'invalid_one_norm_claim': str(g-t), 'invalid_claim_exceeds_actual_gap': g-t > eigenvalues[1]-eigenvalues[0],
            'scope': 'Finite counterexample to the generic one-norm shortcut when zero reference mean is absent'}


def collection():
    graph = make_graph()
    definitions = [
        ('primary', '1', '1', '1/2', '1/2', '1/8'),
        ('negative_bridge', '1', '1', '1/2', '1/2', '-1/8'),
        ('no_bridge', '1', '1', '1/2', '1/2', '0'),
        ('zero_margin', '1', '1', '1/2', '1/2', '1/4'),
        ('beyond_margin', '1', '1', '1/2', '1/2', '3/8'),
        ('signed_ends', '1', '1', '-1/2', '1/4', '1/8'),
        ('left_end_zero', '1', '1', '0', '1/2', '1/8'),
        ('zero_ends', '1', '1', '0', '0', '1/8'),
        ('all_zero', '1', '1', '0', '0', '0'),
        ('scaled_double', '2', '1', '1', '1', '1/4'),
        ('scaled_half', '1/2', '1/4', '1/4', '1/4', '1/16')]
    fixtures = []
    for name, alpha, amin, left, right, mu in definitions:
        parameters = dict(zip(('alpha', 'alpha_min', 'lambda_left', 'lambda_right', 'mu'),
                              (alpha, amin, left, right, mu)))
        fixtures.append({'id': name, 'certificate': certify(graph, parameters)})
    rows = []
    for value in ('-3/8', '-1/4', '-1/8', '-1/16', '0', '1/16', '1/8', '1/4', '3/8'):
        c = certify(graph, {'alpha': '1', 'alpha_min': '1', 'lambda_left': '1/2', 'lambda_right': '1/2', 'mu': value})
        rows.append({'mu_over_alpha': value, 'reference_lower': c['reference_gap_lower'],
                     'generic_lower': c['generic_two_norm_gap_lower'], 'improved_lower': c['full_gap_lower'],
                     'status': c['bound_status'], 'primary_family_member': c['primary_family_member']})
    return {'schema': 'ym18-a1-evidence-v1', 'source_sha256': SOURCE_SHA,
            'graph': graph, 'fixtures': fixtures, 'mu_rows': rows,
            'missing_untouched_link_gate': haar_gate(graph, ['middle']),
            'generic_one_norm_counterexample': no_zero_mean_counterexample(),
            'primary_family': {'end_ratio_max': '1/2', 'bridge_ratio_max': '1/8',
                               'gap_lower_over_alpha': '1/8', 'common_scale_required': 'alpha >= alpha_min > 0'},
            'dressed_ground_wavefunctions_computed': False,
            'scope': 'Finite bridge bound; A2 repetition and remaining-interaction extensions not executed'}


def verify_collection(evidence):
    if not strict_equal(evidence, collection()):
        raise ValueError('complete bridge fixture and proof inventory failed replay')
    return True
