"""Disjoint interacting strips plus a summable full-support remainder."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import cluster

SOURCE_BYTES = Path(__file__).read_bytes()
SOURCE_SHA = hashlib.sha256(SOURCE_BYTES).hexdigest()
CLUSTER_SHA = 'e511485e4dfbc0f54aa08fc4d0ba7c255485e7a98eedf46f35199bfaad94a6e0'


def unchanged():
    if Path(__file__).read_bytes() != SOURCE_BYTES:
        raise ValueError('summable source changed after load')
    if cluster.SOURCE_SHA != CLUSTER_SHA or hashlib.sha256(
            (Path(__file__).parent/'cluster.py').read_bytes()).hexdigest() != CLUSTER_SHA:
        raise ValueError('accepted finite-cluster source changed')


def extent(n, cap=None):
    if type(n) is not int or n < 2 or (cap is not None and n > cap):
        raise ValueError('integer extent at least two within the declared materialization cap required')
    return n


def cluster_count(n):
    n = extent(n)
    return n*(n//4)*(n//2)


def anchors(n):
    n = extent(n)
    return ((x, y, z) for x in range(0, 4*(n//4), 4)
            for y in range(0, 2*(n//2), 2) for z in range(n))


def vertex(v):
    return ','.join(map(str, v))


def edge_name(axis, base):
    return f'e{axis}:' + vertex(base)


def face_name(normal, base):
    return f'f{normal}:' + vertex(base)


def face_data(n, normal, base):
    n = extent(n)
    if type(normal) is not int or not 0 <= normal < 3:
        raise ValueError('normal index zero through two required, not Boolean')
    if type(base) not in (tuple, list) or len(base) != 3 or any(type(x) is not int for x in base):
        raise ValueError('three exact integer face coordinates required')
    if any(not 0 <= base[a] < (n if a == normal else n-1) for a in range(3)):
        raise ValueError('face is outside the box')
    return n, normal, tuple(base)


def selected(n, normal, base):
    n, normal, (x, y, z) = face_data(n, normal, base)
    return normal == 2 and y % 2 == 0 and x//4 < n//4 and x % 4 < 3


def untouched_witness(n, normal, base):
    n, normal, base = face_data(n, normal, base)
    if selected(n, normal, base):
        return None
    if normal != 2:
        return edge_name(2, base)
    if base[1] % 2:
        return edge_name(1, base)
    return edge_name(0, base)


def make_graph(n):
    unchanged()
    n = extent(n, 12)
    vertices = [vertex(v) for v in product(range(n), repeat=3)]
    edges = []
    for base in product(range(n), repeat=3):
        for axis in range(3):
            if base[axis] + 1 < n:
                head = list(base)
                head[axis] += 1
                edges.append({'id': edge_name(axis, base), 'axis': axis,
                              'tail': vertex(base), 'head': vertex(head)})
    lookup = {(e['tail'], e['head']): (e['id'], 1) for e in edges}
    lookup.update({(e['head'], e['tail']): (e['id'], -1) for e in edges})
    faces = []
    for normal in range(3):
        tangents = [a for a in range(3) if a != normal]
        for base in product(*(range(n if a == normal else n-1) for a in range(3))):
            a = list(base)
            a[tangents[0]] += 1
            b = a.copy()
            b[tangents[1]] += 1
            c = list(base)
            c[tangents[1]] += 1
            loop = list(map(vertex, (base, a, b, c)))
            faces.append({'id': face_name(normal, base), 'normal': normal, 'anchor': list(base),
                          'vertices': loop,
                          'word': [{'edge': lookup[(loop[i], loop[(i+1) % 4])][0],
                                    'sign': lookup[(loop[i], loop[(i+1) % 4])][1]} for i in range(4)]})
    return {'schema': 'ym18-open-cubic-link-graph-v1', 'n': n, 'vertices': vertices, 'edges': edges, 'faces': faces,
            'group': 'SU(2)', 'Gauss': 'all vertices, no external charges',
            'electric_terms': 'alpha times every link Casimir; no links removed'}


def validate_graph(graph):
    if type(graph) is not dict or not cluster.strict_equal(graph, make_graph(graph.get('n'))):
        raise ValueError('graph differs from the complete canonical open box')
    edges = {e['id']: e for e in graph['edges']}
    for face in graph['faces']:
        ends = cluster.signed_endpoints(face['word'], edges)
        if [a for a, b in ends] != face['vertices']:
            raise ValueError('face vertices do not match their signed boundary')
    return True


def materialized_clusters(n):
    n = extent(n, 12)
    original = cluster.make_graph()
    result = []
    for anchor in anchors(n):
        links = []
        for edge in original['edges']:
            tail = tuple(int(x) for x in edge['tail'].split(','))
            shifted = tuple(x+y for x, y in zip(tail, anchor))
            links.append(edge_name(edge['axis'], shifted))
        x, y, z = anchor
        result.append({'anchor': list(anchor), 'edges': sorted(links),
                       'faces': [face_name(2, (x+t, y, z)) for t in range(3)]})
    return result


def weight(normal, base):
    if type(normal) is not int or not 0 <= normal < 3 or type(base) not in (tuple, list) or len(base) != 3:
        raise ValueError('valid orientation and three weight coordinates required')
    if any(type(x) is not int or not 0 <= x <= 1024 for x in base):
        raise ValueError('bounded nonnegative integer weight coordinates required')
    return F(1, 24*2**sum(base))


def geometric_sum(count, stride=1):
    if type(count) is not int or not 0 <= count <= 1024 or type(stride) is not int or not 1 <= stride <= 4:
        raise ValueError('bounded exact geometric series parameters required')
    q = F(1, 2**stride)
    return (1-q**count)/(1-q)


def weight_formulas(n):
    n = extent(n, 1024)
    sn, sm = geometric_sum(n), geometric_sum(n-1)
    total = sm*sm*sn/8
    chosen = F(7, 96)*geometric_sum(n//4, 4)*geometric_sum(n//2, 2)*sn
    return {'total': total, 'selected': chosen, 'remaining': total-chosen}


def schedule_gate(kind, tau):
    t = cluster.rational(tau)
    if type(kind) is not str or kind not in ('dyadic-orthant', 'homogeneous'):
        raise ValueError('declared remainder schedule required')
    if kind == 'dyadic-orthant' or t == 0:
        return {'status': 'summable', 'dimensionless_norm_upper': str(abs(t)),
                'reason': 'three orientations times the positive orthant sum divided by twenty-four equals one'
                          if kind == 'dyadic-orthant' else 'zero coefficients'}
    return {'status': 'blocked-volume-uniform-summability', 'dimensionless_norm_upper': None,
            'reason': 'at least two n(n-1)^2 remaining faces have the same nonzero absolute coefficient'}


def certify(graph, parameters):
    unchanged()
    validate_graph(graph)
    keys = {'alpha', 'alpha_min', 'left_ratio', 'right_ratio', 'bridge_ratio', 'tau'}
    if type(parameters) is not dict or set(parameters) != keys:
        raise ValueError('complete physical ratio and scale dictionary required')
    p = {key: cluster.rational(value) for key, value in parameters.items()}
    a, amin, left, right, middle, tau = [p[key] for key in
                                      ('alpha', 'alpha_min', 'left_ratio', 'right_ratio', 'bridge_ratio', 'tau')]
    if not 0 < amin <= a:
        raise ValueError('common physical normalization requires alpha >= alpha_min > 0')
    if max(abs(left), abs(right)) > F(1, 2) or abs(middle) > F(1, 8):
        raise ValueError('cluster coefficients must stay within the accepted primary A1 family')
    local = cluster.certify(parameters={'alpha': str(a), 'alpha_min': str(amin),
        'lambda_left': str(a*left), 'lambda_right': str(a*right), 'mu': str(a*middle)})
    if F(local['full_gap_lower']) < a/8:
        raise ValueError('accepted cluster bound is below the declared reference baseline')
    n = graph['n']
    blocks = materialized_clusters(n)
    occupied = set()
    selected_map = {}
    for block in blocks:
        if occupied & set(block['edges']):
            raise ValueError('distinct interacting clusters share links')
        occupied.update(block['edges'])
        for face, ratio in zip(block['faces'], (left, middle, right)):
            selected_map[face] = ratio
    ledger = []
    remaining_weight = F(0)
    for face in graph['faces']:
        w = weight(face['normal'], face['anchor'])
        chosen = face['id'] in selected_map
        if chosen != selected(n, face['normal'], face['anchor']):
            raise ValueError('arithmetic selector disagrees with translated actual strips')
        witness = untouched_witness(n, face['normal'], face['anchor'])
        if not chosen:
            if witness in occupied or witness not in {t['edge'] for t in face['word']}:
                raise ValueError('remaining face lacks its declared free Haar link')
            remaining_weight += w
        coefficient = a*selected_map[face['id']] if chosen else a*tau*w
        ledger.append({'face': face['id'], 'normal': face['normal'], 'anchor': face['anchor'],
                       'kind': 'cluster' if chosen else 'remaining', 'weight': str(w),
                       'physical_coefficient': str(coefficient), 'untouched_link': witness})
    sums = weight_formulas(n)
    if remaining_weight != sums['remaining'] or sum((F(row['weight']) for row in ledger), F(0)) != sums['total']:
        raise ValueError('finite weight ledger disagrees with exact geometric sums')
    beta = a*abs(tau)*remaining_weight
    finite = a/8-beta
    coefficient = F(1, 8)-abs(tau)
    uniform = a*coefficient
    common = amin*coefficient if coefficient >= 0 else None
    return {'schema': 'ym18-summable-cluster-bound-v1', 'source_sha256': SOURCE_SHA,
            'cluster_source_sha256': CLUSTER_SHA,
            'graph_n': n, 'graph_sha256': hashlib.sha256(json.dumps(graph, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
            'parameters': {key: str(p[key]) for key in sorted(p)},
            'cluster_count': len(blocks), 'clusters': blocks,
            'reference_free_links': sorted(e['id'] for e in graph['edges'] if e['id'] not in occupied),
            'reference_is_pure_free': not blocks,
            'local_cluster_gap_lower': local['full_gap_lower'],
            'local_cluster_template_graph_sha256': local['graph_sha256'],
            'reference_gap_lower_used': str(a/8),
            'pure_free_gap_if_no_clusters': str(3*a/4) if not blocks else None,
            'face_ledger': ledger, 'face_count': len(ledger), 'remaining_face_count': sum(row['kind'] == 'remaining' for row in ledger),
            'total_face_weight': str(sums['total']), 'selected_face_weight': str(sums['selected']),
            'remaining_face_weight': str(remaining_weight), 'orthant_weight_upper': '1',
            'remainder_norm_upper': str(beta), 'reference_remainder_expectation': '0',
            'finite_gap_lower': str(finite), 'finite_bound_status': 'positive' if finite > 0 else 'zero-insufficient' if finite == 0 else 'negative-insufficient',
            'uniform_bound_at_alpha': str(uniform), 'common_gap_lower': str(common) if common is not None else None,
            'uniform_bound_status': 'positive' if coefficient > 0 else 'zero-insufficient' if coefficient == 0 else 'negative-insufficient',
            'generic_uniform_bound_at_alpha': str(a*(F(1, 8)-2*abs(tau))),
            'finite_ground_Gauss_inclusion_certified': finite > 0,
            'uniform_ground_Gauss_inclusion_certified': coefficient > 0,
            'actual_full_face_support': all(F(row['physical_coefficient']) != 0 for row in ledger),
            'schedule': schedule_gate('dyadic-orthant', str(tau)),
            'scope': 'All-volume inhomogeneous summable-remainder exception in a common energy convention; internally overlapping strips have disjoint link supports; homogeneous dense Yang-Mills remains open'}


def verify(graph, certificate):
    if type(certificate) is not dict or certificate.get('schema') != 'ym18-summable-cluster-bound-v1':
        raise ValueError('wrong summable cluster certificate schema')
    if not cluster.strict_equal(certificate, certify(graph, certificate.get('parameters'))):
        raise ValueError('cluster, untouched-link, coefficient or bound replay failed')
    return True


def collection():
    base = {'alpha': '1', 'alpha_min': '1', 'left_ratio': '1/2', 'right_ratio': '1/2', 'bridge_ratio': '1/8', 'tau': '1/64'}
    graphs = {str(n): make_graph(n) for n in range(2, 10)}
    definitions = [(f'volume_{n}', n, {}) for n in range(2, 10)] + [
        ('negative_tau', 5, {'tau': '-1/64'}),
        ('signed_cluster', 5, {'left_ratio': '-1/2', 'right_ratio': '1/4', 'bridge_ratio': '-1/8'}),
        ('tau_zero', 5, {'tau': '0'}), ('tau_boundary', 5, {'tau': '1/8'}),
        ('zero_cluster_coefficient', 5, {'left_ratio': '0'}),
        ('scaled_double', 4, {'alpha': '2'}),
        ('scaled_half', 4, {'alpha': '1/2', 'alpha_min': '1/4'})]
    fixtures = []
    for name, n, changes in definitions:
        parameters = {**base, **changes}
        fixtures.append({'id': name, 'certificate': certify(graphs[str(n)], parameters)})
    boundary_rows = []
    for n in (6, 8):
        certificate = next(f['certificate'] for f in fixtures if f['id'] == f'volume_{n}')
        row = next(row for row in certificate['face_ledger'] if row['face'] == 'f2:4,0,0')
        boundary_rows.append({'n': n, 'face': row['face'], 'kind': row['kind'],
                              'physical_coefficient': row['physical_coefficient']})
    return {'schema': 'ym18-a2-collection-v1', 'source_sha256': SOURCE_SHA,
            'graphs': graphs, 'fixtures': fixtures,
            'all_volume_cluster_count': 'n floor(n/4) floor(n/2)',
            'orthant_weight_sum': '1',
            'primary_common_gap_over_alpha_min': '7/64',
            'primary_generic_gap_over_alpha': '3/32',
            'nonzero_homogeneous_remainder_gate': schedule_gate('homogeneous', '1/64'),
            'boundary_reclassification': boundary_rows,
            'finite_volume_family_is_nested_restriction': False,
            'scope': 'All-volume theorem is proved analytically; n2 through n9 are implementation checks; post-A B/C goals unexecuted'}


def verify_collection(evidence):
    if not cluster.strict_equal(evidence, collection()):
        raise ValueError('complete cluster and parameter collection failed replay')
    return True
