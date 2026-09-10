"""Complete low physical support and exact full P-to-Q magnetic cross Gram."""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import hashlib
import json
import math
import haar

SOURCE_BYTES = Path(__file__).read_bytes()
SOURCE_SHA = hashlib.sha256(SOURCE_BYTES).hexdigest()
HAAR_SHA = '13a82e2b804f07d7dbe8951f600ded429d4924b042162ec79d60c2889b767a80'
GRAPH_SHA = '9e630191189fb3f69145e5cdbc91eceac138f95d44d7bed825b87b572b322e62'


def unchanged():
    root = Path(__file__).parent
    if Path(__file__).read_bytes() != SOURCE_BYTES or haar.SOURCE_SHA != HAAR_SHA:
        raise ValueError('cross or loaded Haar source changed')
    if hashlib.sha256((root/'haar.py').read_bytes()).hexdigest() != HAAR_SHA:
        raise ValueError('accepted Haar source bytes changed')
    if hashlib.sha256((root/'graph.json').read_bytes()).hexdigest() != GRAPH_SHA:
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
    result = json.loads((Path(__file__).parent/'graph.json').read_text())
    haar.validate_graph(result)
    return result


def moment(indices):
    unchanged()
    if type(indices) not in (tuple, list) or len(indices) > 6 or any(
            type(i) is not int or not 0 <= i < 11 for i in indices):
        raise ValueError('at most six exact face indices from zero through ten required')
    return _moment(tuple(sorted(indices)))


@lru_cache(maxsize=None)
def _moment(indices):
    powers = [0]*11
    for index in indices:
        powers[index] += 1
    return 2**len(indices)*haar.moment(powers)


def support_inventory():
    g = graph()
    vertices = {name: i for i, name in enumerate(g['vertices'])}
    edges = [(vertices[e['tail']], vertices[e['head']]) for e in g['edges']]
    edge_indices = {e['id']: i for i, e in enumerate(g['edges'])}
    face_masks = {sum(1 << edge_indices[t['edge']] for t in f['word']): f['id'] for f in g['faces']}
    rows, admitted = [], []
    for size in range(6):
        for chosen in combinations(range(20), size):
            degrees = [0]*12
            for i in chosen:
                a, b = edges[i]
                degrees[a] += 1
                degrees[b] += 1
            minimum = min((x for x in degrees if x), default=None)
            mask = sum(1 << i for i in chosen)
            if not size:
                classification = 'vacuum-support'
            elif minimum >= 2:
                if size != 4 or mask not in face_masks or any(x not in (0, 2) for x in degrees):
                    raise ValueError('an additional small no-leaf support must be analyzed')
                classification = 'fundamental-face-candidate'
                admitted.append(mask)
            else:
                classification = 'rejected-by-degree-one-Gauss-obstruction'
            rows.append({'mask': mask, 'edge_count': size, 'minimum_active_degree': minimum,
                         'classification': classification})
    if set(admitted) != set(face_masks):
        raise ValueError('complete four-cycle inventory does not match all eleven faces')
    return {'edge_order': [e['id'] for e in g['edges']], 'rows': rows,
            'eligible_nonempty_masks': admitted, 'face_masks': {name: mask for mask, name in face_masks.items()},
            'total_supports': len(rows), 'empty_supports': 1,
            'interpretation': 'necessary no-leaf supports; degree-two intertwiner proof fixes a common spin, and the energy cutoff leaves only spin one half'}


def six_edge_witness():
    g = graph()
    loop = ['0,0,0', '1,0,0', '2,0,0', '2,1,0', '1,1,0', '0,1,0']
    lookup = {(e['tail'], e['head']): (e['id'], 1) for e in g['edges']}
    lookup.update({(e['head'], e['tail']): (e['id'], -1) for e in g['edges']})
    word = [{'edge': lookup[(loop[i], loop[(i+1) % 6])][0],
             'sign': lookup[(loop[i], loop[(i+1) % 6])][1]} for i in range(6)]
    support = {t['edge'] for t in word}
    parity = [{'face': f['id'], 'odd_edges': sorted(support.symmetric_difference(t['edge'] for t in f['word'])),
               'inner_product': '0'} for f in g['faces']]
    if len(support) != 6 or any(not row['odd_edges'] for row in parity):
        raise ValueError('rectangle witness is not distinct from every trial face')
    return {'vertices': loop, 'word': word, 'norm_squared': '1', 'vacuum_inner_product': '0',
            'face_inner_products': parity, 'energy_over_alpha': '9/2',
            'spin_on_each_active_edge': '1/2', 'scope': 'exact physical Wilson-loop state in Q, not a sampled tail eigenvector'}


def fourth_inventory():
    g = graph()
    incidence = haar.validate_graph(g)
    rows = []
    for indices in combinations_with_replacement(range(11), 4):
        counts = Counter(indices)
        odd = [edge for edge, faces in incidence.items() if sum(counts[i] for i, sign in faces) % 2]
        pattern = sorted(counts.values(), reverse=True)
        expected = F(2) if pattern == [4] else F(1) if pattern == [2, 2] else F(0)
        value = _moment(indices)
        if value != expected or (pattern not in ([4], [2, 2]) and not odd):
            raise ValueError('fourth-moment or complete boundary classification failed')
        multiplicity = math.factorial(4)//math.prod(math.factorial(x) for x in counts.values())
        rows.append({'indices': list(indices), 'multiplicity': multiplicity, 'pattern': pattern,
                     'odd_boundary_edges': odd, 'moment': str(value)})
    return {'rows': rows, 'multisets': len(rows), 'ordered_products_covered': sum(row['multiplicity'] for row in rows),
            'all_four_distinct_cases': sum(row['pattern'] == [1, 1, 1, 1] for row in rows),
            'degree_four_independent_Haar_agreement': True,
            'reason': 'this low-order agreement follows from actual graph integration; it is not a full distribution factorization'}


def matrices(alpha, couplings):
    unchanged()
    a = rational(alpha)
    if a <= 0:
        raise ValueError('positive physical alpha required')
    if type(couplings) not in (list, tuple) or len(couplings) != 11:
        raise ValueError('eleven physical magnetic coefficients required')
    ls = tuple(rational(x) for x in couplings)
    basis_indices = [()] + [(i,) for i in range(11)]
    gram, potential, squared = [], [], []
    for bi in basis_indices:
        gr, vr, sr = [], [], []
        for bj in basis_indices:
            base = bi+bj
            gr.append(_moment(tuple(sorted(base))))
            vr.append(-sum((lp*_moment(tuple(sorted(base+(p,))))/2 for p, lp in enumerate(ls)), F(0)))
            sr.append(sum((lp*lq*_moment(tuple(sorted(base+(p, q))))/4
                           for p, lp in enumerate(ls) for q, lq in enumerate(ls)), F(0)))
        gram.append(gr)
        potential.append(vr)
        squared.append(sr)
    subtraction = [[sum((potential[i][k]*potential[k][j] for k in range(12)), F(0)) for j in range(12)] for i in range(12)]
    cross = [[squared[i][j]-subtraction[i][j] for j in range(12)] for i in range(12)]
    return a, ls, tuple(tuple(tuple(row) for row in m) for m in (gram, potential, squared, subtraction, cross))


def certify(alpha='1', couplings=None):
    if couplings is None:
        couplings = ['1/8']*11
    a, ls, (gram, potential, squared, subtraction, cross) = matrices(alpha, couplings)
    qsum = sum((x*x for x in ls), F(0))
    expected = tuple(tuple(F(0) if i == 0 or j == 0 else qsum/4 if i == j else ls[i-1]*ls[j-1]/4
                           for j in range(12)) for i in range(12))
    if cross != expected:
        raise ValueError('full P subtraction disagrees with cross-Gram formula')
    row_bound = max(sum((abs(x) for x in row), F(0)) for row in cross)
    ratio = max(map(abs, ls))/a
    box_bound = 21*a*a*ratio*ratio/4
    if row_bound > box_bound:
        raise ValueError('coefficient-box norm-squared upper bound failed')
    same_magnitudes = len(set(map(abs, ls))) == 1
    return {'schema': 'ym18-physical-complement-cross-v1', 'source_sha256': SOURCE_SHA,
            'haar_source_sha256': HAAR_SHA, 'graph_file_sha256': GRAPH_SHA,
            'physical_contract': {'Hamiltonian': 'alpha sum_e C_e minus sum_p lambda_p x_p',
                'Hilbert': 'untruncated L2 of SU(2)^20 restricted to all-vertex Gauss invariants',
                'external_charges': False, 'Casimir': 'j(j+1)',
                'normalization': 'x_p=Tr(U_p)/2; ordinary fundamental chi_p=2x_p',
                'projection': 'vacuum and all eleven fundamental face characters',
                'operator_domain': 'elliptic electric domain; bounded Wilson perturbation'},
            'alpha': str(a), 'couplings': list(map(str, ls)), 'face_order': [f['id'] for f in graph()['faces']],
            'Gram': [[str(x) for x in row] for row in gram],
            'PVP': [[str(x) for x in row] for row in potential],
            'PV2P': [[str(x) for x in row] for row in squared],
            'P_subtraction': [[str(x) for x in row] for row in subtraction],
            'cross_Gram': [[str(x) for x in row] for row in cross],
            'Q_electric_lower': str(9*a/2), 'Q_full_lower_from_norm': str(9*a/2-sum(map(abs, ls), F(0))),
            'sum_coupling_squares': str(qsum), 'maximum_absolute_ratio': str(ratio),
            'cross_norm_squared_row_upper': str(row_bound), 'coefficient_box_norm_squared_upper': str(box_bound),
            'equal_magnitudes': same_magnitudes,
            'exact_cross_norm_squared_if_equal': str(21*ls[0]*ls[0]/4) if same_magnitudes else None,
            'scope': 'Complete finite-graph physical complement and QVP Gram; scalar E1 optimization and B2 parameter-box gap not executed'}


def verify(certificate):
    if type(certificate) is not dict or certificate.get('schema') != 'ym18-physical-complement-cross-v1':
        raise ValueError('wrong complement certificate schema')
    if not haar.strict_equal(certificate, certify(certificate.get('alpha'), certificate.get('couplings'))):
        raise ValueError('complement or cross-operator replay failed')
    return True


def projection_gate(face_ids):
    expected = [f['id'] for f in graph()['faces']]
    if type(face_ids) is not list or any(type(x) is not str for x in face_ids) or sorted(face_ids) != sorted(expected):
        raise ValueError('complete projection requires all eleven physical fundamental face states')
    return True


def collection():
    g = graph()
    definitions = [('allzero', '1', ['0']*11),
                   ('all_positive_eighth', '1', ['1/8']*11),
                   ('all_negative_eighth', '1', ['-1/8']*11),
                   ('alternating_eighth', '1', ['1/8' if i % 2 == 0 else '-1/8' for i in range(11)]),
                   ('single_eighth', '1', ['1/8']+['0']*10),
                   ('mixed_signed_zero', '1', ['1/8', '-1/16', '0', '3/32', '0', '-1/32', '0', '0', '0', '0', '0']),
                   ('canonical_three_eighths', '1', ['3/8']*11),
                   ('scaled_double', '2', ['3/4']*11),
                   ('scaled_half', '1/2', ['3/16']*11)]
    fixtures = [{'id': name, 'certificate': certify(alpha, ls)} for name, alpha, ls in definitions]
    face_index = {f['id']: i for i, f in enumerate(g['faces'])}
    six_faces = [face_index[name] for name in g['cells'][0]['faces']]
    sixth = moment(six_faces)
    single = fixtures[4]['certificate']
    gaussian_single = (F(3)-F(1))*F(single['couplings'][0])**2/4
    positive = fixtures[1]['certificate']
    return {'schema': 'ym18-b1-collection-v1', 'source_sha256': SOURCE_SHA, 'graph': g,
            'low_support_inventory': support_inventory(), 'six_edge_witness': six_edge_witness(),
            'fourth_moment_inventory': fourth_inventory(), 'fixtures': fixtures,
            'controls': {'Gaussian_same_face_fourth': {'actual': '2', 'Gaussian': '3',
                'actual_single_cross_diagonal': single['cross_Gram'][1][1],
                'Gaussian_single_cross_diagonal': str(gaussian_single)},
                'deleted_P_subtraction': {'actual_vacuum_cross_diagonal': positive['cross_Gram'][0][0],
                                          'without_subtraction': positive['PV2P'][0][0]},
                'six_face_distribution_independence': {'face_indices': six_faces, 'actual_moment': str(sixth),
                                                       'independent_Haar_prediction': '0'},
                'omitted_projection_face': {'face': g['faces'][0]['id'], 'omitted_state_energy_over_alpha': '3',
                                            'invalid_complement_threshold_over_alpha': '9/2'},
                'falsely_raised_tail': {'proposed_over_alpha': '6', 'witness_over_alpha': '9/2'}},
            'status': 'computed-for-independent-review',
            'B2': 'not executed'}


def verify_collection(evidence):
    if not haar.strict_equal(evidence, collection()):
        raise ValueError('complete support, moment or required fixture inventory failed replay')
    return True
