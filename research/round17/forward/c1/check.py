"""Exact complete tensor checks plus signed-link matrix realization controls."""
import argparse
import copy
import csv
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import central


def cmatrix(q):
    a, b, c, d = map(float, q)
    return ((complex(a, b), complex(c, d)), (complex(-c, d), complex(a, -b)))


def cmul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))


def cdagger(a):
    return tuple(tuple(a[j][i].conjugate() for j in range(2)) for i in range(2))


def complex_word(word, links):
    value = ((1+0j, 0j), (0j, 1+0j))
    for term in word:
        m = cmatrix(links[term['edge']])
        value = cmul(value, m if term['sign'] == 1 else cdagger(m))
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    out = Path(args.output).resolve()
    if out == source or source in out.parents:
        raise ValueError('output must be outside frozen source')
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
            checks.append('reject: ' + name)
            return
        raise RuntimeError('invalid accepted: ' + name)

    graph = central.make_graph()
    incidence = central.validate_graph(graph)
    info = central.geometry(graph)
    check('actual four-cube complex counts 18 vertices, 33 edges and 20 faces',
          (len(graph['vertices']), len(graph['edges']), len(graph['faces']), len(graph['cells'])) == (18, 33, 20, 4))
    check('outer surface has 18 vertices, 32 edges and 16 faces',
          (len(info['outer_vertices']), len(info['outer_edge_ids']), len(info['outer_face_ids'])) == (18, 32, 16))
    check('four internal faces meet the actual central link',
          len(info['internal_face_ids']) == 4 and len(info['central_face_indices']) == 4
          and info['central_edge'] == 'e2:1,1,0')
    check('central link is precisely the edge absent from the outer graph',
          {e['id'] for e in graph['edges']} - set(info['outer_edge_ids']) == {info['central_edge']})
    words = central.central_words(graph)
    edge_map = {e['id']: e for e in graph['edges']}
    check('every fully reoriented face remains a closed signed square',
          all(central.word_endpoints(entry['word'], edge_map) and entry['word'][0] ==
              {'edge': info['central_edge'], 'sign': 1} for entry in words))
    check('four surrounding three-link paths have disjoint link support',
          len({term['edge'] for entry in words for term in entry['boundary_path']}) == 12)
    links, choices = central.realize_boundary()
    check('actual surrounding link assignments realize every requested H',
          all(central.product_word(entry['boundary_path'], links) == h
              for entry, h in zip(words, central.TETRAHEDRAL)))
    check('tetrahedral boundary holonomies are noncommuting',
          central.multiply(central.TETRAHEDRAL[0], central.TETRAHEDRAL[1]) !=
          central.multiply(central.TETRAHEDRAL[1], central.TETRAHEDRAL[0]))
    directions = [(h[0], -h[1], -h[2], -h[3]) for h in central.TETRAHEDRAL]
    check('the four quaternion trace directions are orthonormal',
          all(sum((a*b for a, b in zip(x, y)), F(0)) == int(i == j)
              for i, x in enumerate(directions) for j, y in enumerate(directions)))
    basis, gram, inverse, projector, wrong, one = central.invariant_data()
    check('Gram has exact diagonal nine and off-diagonal three',
          gram == tuple(tuple(F(9) if i == j else F(3) for j in range(3)) for i in range(3)))
    eye3 = tuple(tuple(F(i == j) for j in range(3)) for i in range(3))
    check('the stated inverse is the exact full Gram inverse', central.matmul(gram, inverse) == eye3)
    check('the full 81 by 81 Haar tensor is self-adjoint', projector == central.transpose(projector))
    check('the full Haar tensor is idempotent', central.matmul(projector, projector) == projector)
    check('trace and projector rank are three', sum(projector[i][i] for i in range(81)) == 3)
    check('all invariant basis vectors are fixed by the tensor', central.matmul(projector, basis) == basis)
    q = (F(1, 3), F(2, 3), F(2, 3), F(0))
    rotation = central.rotation(q)
    check('exact nontrivial adjoint matrix is orthogonal',
          central.matmul(rotation, central.transpose(rotation)) == eye3)
    tensor = central.tensor([rotation] * 4)
    check('full tensor is invariant under a dense rational adjoint rotation',
          central.matmul(tensor, projector) == projector and central.matmul(projector, tensor) == projector)
    check('omitting off-diagonal inverse terms fails the projector identity',
          central.matmul(wrong, wrong) != wrong)
    check('one valid channel is rank one and misses the full invariant space',
          central.matmul(one, one) == one and sum(one[i][i] for i in range(81)) == 1 and one != projector)
    check('complete normalized tetrahedral contraction is minus one over 405',
          central.contract(projector) == -F(1, 405))
    check('diagonal-only inverse produces the wrong positive sign', central.contract(wrong) == F(2, 405))
    check('one-channel shortcut also gives a false positive contraction', central.contract(one) == F(1, 729))
    check('identity boundary normalization recovers three invariants over 81',
          central.contract(projector, [central.IDENTITY] * 4) == F(1, 27))
    u_fixtures = [central.IDENTITY, central.TETRAHEDRAL[0],
                  (F(3, 5), F(4, 5), F(0), F(0)), q]
    maximum_error = 0.0
    for u in u_fixtures:
        ls, _ = central.realize_boundary(u)
        for face in graph['faces']:
            exact = central.product_word(face['word'], ls)
            raw = complex_word(face['word'], ls)
            expect = cmatrix(exact)
            maximum_error = max(maximum_error, *(abs(raw[i][j] - expect[i][j]) for i in range(2) for j in range(2)))
        for entry, h, direction in zip(words, central.TETRAHEDRAL, directions):
            exact = central.product_word(entry['word'], ls)
            if exact != central.multiply(u, h) or exact[0] != sum((x*y for x, y in zip(u, direction)), F(0)):
                raise RuntimeError('actual conditional face does not equal U H')
    check('80 actual face words agree with an independent raw complex matrix calculation', maximum_error < 1e-13)
    check('four fixed central samples realize x_i as the stated quaternion dot product', True)
    # The gauge check uses every oriented link, including all background identities.
    links, _ = central.realize_boundary(q)
    transformations = {v: u_fixtures[i % len(u_fixtures)] for i, v in enumerate(graph['vertices'])}
    transformed = {e['id']: central.multiply(central.multiply(transformations[e['tail']], links[e['id']]),
                                           central.conjugate(transformations[e['head']])) for e in graph['edges']}
    for face in graph['faces']:
        h0 = central.product_word(face['word'], links)
        h1 = central.product_word(face['word'], transformed)
        base = transformations[face['vertices'][0]]
        if h1 != central.multiply(central.multiply(base, h0), central.conjugate(base)):
            raise RuntimeError('actual signed holonomy failed gauge covariance')
    check('all twenty signed face holonomies satisfy exact vertex gauge covariance', True)
    for entry in words:
        reversed_word = [{'edge': t['edge'], 'sign': -t['sign']} for t in entry['word'][::-1]]
        x = central.product_word(entry['word'], links)[0]
        y = central.product_word(reversed_word, links)[0]
        if x != y:
            raise RuntimeError('complete face reversal changed its real character')
    check('complete face reversal preserves the real character', True)
    broken_word = copy.deepcopy(words[0]['word'])
    broken_word[1]['sign'] *= -1
    reject('single dagger change is not a closed face reorientation', lambda: central.word_endpoints(broken_word, edge_map))
    certificate = central.certify()
    check('complete certificate replays with source and geometry', central.verify(certificate))
    for name, mutate in [
        ('incomplete invariant tensor', lambda c: c['projector'][0].__setitem__(0, '0')),
        ('adjoint normalization factor omitted', lambda c: c.update(conditional_joint='-1/5')),
        ('twenty-face bulk result substituted for conditional scope', lambda c: c.update(scope='full bulk partition result')),
        ('boundary assignment removed', lambda c: c['boundary_assignments'].pop(choices[0]['edge']))]:
        c = copy.deepcopy(certificate)
        mutate(c)
        reject(name, lambda c=c: central.verify(c))
    reject('non-unit boundary quaternion', lambda: central.rotation((F(1), F(1), F(0), F(0))))
    rows = [{'method': 'complete rank-three projector', 'normalized_joint': '-1/405', 'accepted': 'true'},
            {'method': 'off-diagonal inverse deleted', 'normalized_joint': '2/405', 'accepted': 'false'},
            {'method': 'only one normalized channel', 'normalized_joint': '1/729', 'accepted': 'false'},
            {'method': 'product of four individual means', 'normalized_joint': '0', 'accepted': 'false'}]
    (out / 'evidence.json').write_text(json.dumps(certificate, indent=2) + '\n')
    (out / 'graph.json').write_text(json.dumps(graph, indent=2) + '\n')
    with (out / 'channel.csv').open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = {'schema': 'ym17-c1-results-v1', 'status': 'passed', 'checks_count': len(checks),
              'checks': checks, 'source_sha256': central.SOURCE_SHA,
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'evidence_sha256': hashlib.sha256((out / 'evidence.json').read_bytes()).hexdigest(),
              'matrix_comparison_max_error': maximum_error, 'complete_tensor_entries': 81*81,
              'normalized_joint': certificate['conditional_joint'],
              'wrong_diagonal_joint': certificate['wrong_diagonal_inverse_joint'],
              'scope': certificate['scope']}
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    (out / 'manifest.json').write_text(json.dumps({'schema': 'ym17-c1-output-manifest-v1',
        'files': {name: hashlib.sha256((out / name).read_bytes()).hexdigest()
                  for name in ('evidence.json', 'graph.json', 'channel.csv', 'results.json')}}, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, indent=2))


if __name__ == '__main__':
    main()
