"""Validate AH1's exact generated span and sparse action, not its analytic proof.

The fixed graph/conventions below are those of the frozen AH1 contract and
reviewed derivations. This release check is source-bound by the admission spec;
its execution is neither a new physical fixture nor an independent discovery.
"""
import argparse
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError("AH1 structure: " + message)


def rational(value):
    if isinstance(value, dict):
        require(set(value) == {"numerator", "denominator"}, "rational fields")
        require(type(value["numerator"]) is int and type(value["denominator"]) is int and value["denominator"] > 0,
                "rational integer components")
        return Fraction(value["numerator"], value["denominator"])
    require(type(value) in (str, int), "exact rational value")
    return Fraction(value)


def identical(left, right):
    """Schema equality must not identify Boolean labels with integer indices."""
    return json.dumps(left, sort_keys=True, separators=(",", ":"), allow_nan=False) == json.dumps(
        right, sort_keys=True, separators=(",", ":"), allow_nan=False)


def verify(result, side, artifacts=None):
    require(side in ("forward", "reverse"), "direction")
    artifacts = artifacts or {}
    require(not artifacts if side == "forward" else set(artifacts) == {"graph.json", "basis.json", "magnetic.json"},
            "complete declared artifact set")
    graph = result["graph"] if side == "forward" else artifacts["graph.json"]
    basis_record = result["enrichment"] if side == "forward" else artifacts["basis.json"]
    magnetic = result["retained_magnetic"] if side == "forward" else artifacts["magnetic.json"]
    extent = (3, 2, 1)
    vertices = list(product(range(4), range(3), range(2)))
    require(identical(graph["vertices"], [list(v) for v in vertices]), "all lexicographic physical vertices")
    vertex_ids = {v: i for i, v in enumerate(vertices)}
    links = []
    for vertex in vertices:
        for axis in range(3):
            if vertex[axis] < extent[axis]:
                head = list(vertex)
                head[axis] += 1
                links.append((vertex, axis, tuple(head)))
    link_ids = {(v, a): i for i, (v, a, _) in enumerate(links)}
    signs = [1 if a == 0 else (-1) ** (v[0] if a == 1 else v[0] + v[1]) for v, a, _ in links]
    if side == "forward":
        expected_links = [{"id": i, "axis": a, "tail": list(v), "head": list(h), "center_sign": signs[i]}
                          for i, (v, a, h) in enumerate(links)]
        require(identical(graph["edges"], expected_links), "all physical links/orientations/center signs")
    else:
        expected_links = [{"id": i, "axis": a, "tail": vertex_ids[v], "head": vertex_ids[h],
                           "tail_coordinate": list(v), "head_coordinate": list(h)} for i, (v, a, h) in enumerate(links)]
        require(identical(graph["links"], expected_links) and identical(graph["center_signs"], signs),
                "all physical links/orientations/center signs")
        incidence = [[] for _ in vertices]
        for i, (v, _, h) in enumerate(links):
            incidence[vertex_ids[v]].append([i, 1])
            incidence[vertex_ids[h]].append([i, -1])
        require(identical(graph["vertex_incidence"], incidence), "every vertex Gauss incidence")
    faces, masks, face_edges, face_vertices, internal = [], [], [], [], []
    for vertex in vertices:
        for a, b in combinations(range(3), 2):
            if vertex[a] == extent[a] or vertex[b] == extent[b]:
                continue
            va, vb = list(vertex), list(vertex)
            va[a] += 1
            vb[b] += 1
            word = [[link_ids[vertex, a], 1], [link_ids[tuple(va), b], 1],
                    [link_ids[tuple(vb), a], -1], [link_ids[vertex, b], -1]]
            identifier = len(faces)
            normal = next(c for c in range(3) if c not in (a, b))
            interior = 0 < vertex[normal] < extent[normal]
            if interior:
                internal.append(identifier)
            mask = sum(1 << edge for edge, _ in word)
            require(len({edge for edge, _ in word}) == 4, "distinct edges of each face")
            require(product_sign(signs[e] for e, _ in word) == -1, "coordinate center oddness on every face")
            expected = {"id": identifier, "axes": [a, b], "word": word, "mask": mask,
                        "tail" if side == "forward" else "base": list(vertex)}
            if side == "forward":
                expected["internal"] = interior
            faces.append(expected)
            masks.append(mask)
            face_edges.append({e for e, _ in word})
            face_vertices.append({end for e, _ in word for end in (links[e][0], links[e][2])})
    require(identical(graph["faces"], faces), "every internal/external face word and mask")
    require(identical(graph["internal_face_ids" if side == "forward" else "internal_faces"], internal),
            "exact internal-face set")
    require((len(vertices), len(links), len(faces), len(links) - len(vertices) + 1) == (24, 46, 29, 23),
            "contract graph and cycle rank")
    n = len(faces)
    expected_basis = [("vacuum", [], Fraction(1), Fraction(0), {})]
    for p in range(n):
        expected_basis.append(("face", [p], Fraction(1), Fraction(3), {str(e): 1 for e in face_edges[p]}))
    for p in range(n):
        expected_basis.append(("spin1", [p], Fraction(1), Fraction(8), {str(e): 2 for e in face_edges[p]}))
    pairs, mask_owner, expected_pair_rows = [], {}, {}
    geometry_counts = {"shared_edge": 0, "vertex_only": 0, "vertex_disjoint": 0}
    for p, q in combinations(range(n), 2):
        shared = face_edges[p] & face_edges[q]
        require(len(shared) <= 1, "distinct elementary face intersections")
        mask = masks[p] ^ masks[q]
        require(mask and mask not in mask_owner and mask not in masks, "independent pair masks, beyond global parity")
        mask_owner[mask] = (p, q)
        overlap = len(face_vertices[p] & face_vertices[q])
        geometry = "shared_edge" if shared else "vertex_only" if overlap else "vertex_disjoint"
        geometry_counts[geometry] += 1
        edge = next(iter(shared)) if shared else None
        rows = []
        spins = {str(e): 1 for e in face_edges[p] ^ face_edges[q]}
        for kind, metric, energy in [("singlet", 1, Fraction(9, 2)), ("triplet", 3, Fraction(13, 2))] if shared else [("pair", 1, 6)]:
            rows.append(len(expected_basis))
            expected_basis.append((kind, [p, q], Fraction(metric), Fraction(energy),
                                   {**spins, str(edge): 2} if kind == "triplet" else dict(spins)))
        pair = {"faces": [p, q], "mask": mask, "shared_edge": edge,
                "basis_rows" if side == "forward" else "basis_ids": rows}
        if side == "forward":
            pair.update(common_vertex_count=overlap, geometry=geometry)
            if shared:
                pair["shared_orientation_signs"] = [dict(faces[r]["word"])[edge] for r in (p, q)]
        pairs.append(pair)
        expected_pair_rows[p, q] = rows
    require(identical(basis_record["pairs"] if side == "forward" else graph["face_pairs"], pairs),
            "all unordered pair masks, geometry and channel labels")
    require(geometry_counts == {"shared_edge": 96, "vertex_only": 64, "vertex_disjoint": 246}, "pair geometry")
    basis = basis_record["basis"]
    require(len(basis) == len(expected_basis) == 561, "full individually resolved generated basis")
    aliases = {"fundamental": "face", "spin_one": "spin1", "product": "pair"}
    functions = {"vacuum": "1", "face": "2 W_p", "spin1": "4 W_p^2 - 1", "pair": "4 W_p W_q",
                 "singlet": "8 E_common[W_p W_q]", "triplet": "8 (I-E_common)[W_p W_q]"}
    metric, energies = [], []
    for i, (record, (kind, fs, weight, energy, spins)) in enumerate(zip(basis, expected_basis)):
        require(type(record["id"]) is int and record["id"] == i and aliases.get(record["kind"], record["kind"]) == kind and identical(record["faces"], fs),
                "ordered physical basis identity")
        actual_weight = rational(record["norm2" if side == "forward" else "metric"])
        actual_energy = rational(record["energy" if side == "forward" else "electric"])
        require(actual_weight == weight > 0 and actual_energy == energy, "physical Haar Gram and electric action")
        parity = 1 if kind == "face" else 0
        require(identical(record["parity"], parity) if side == "forward" else identical(record["center_parity"], (-1) ** parity),
                "basis center character")
        if side == "reverse":
            require(identical(record["twice_edge_spins"], spins) and record["function"] == functions[kind], "actual functions/representation support")
            require(sum((Fraction(j * (j + 2), 4) for j in spins.values()), Fraction(0)) == energy,
                    "Casimir sum on every active representation support")
        metric.append(weight)
        energies.append(energy)
    if side == "forward":
        require(basis_record["rank"] == 561 and basis_record["nullity"] == 0, "positive Gram quotient")
        require(basis_record["duplicate_control_null"] == [1, -1], "duplicated-vector null control")
    else:
        require(basis_record["dimension"] == basis_record["quotient_rank"] == 561 and basis_record["Gram_nullspace"] == [],
                "positive Gram quotient")
    expected_action = {}
    def column_entry(row, column, value):
        require((row, column) not in expected_action, "nonduplicated complete old column")
        expected_action[row, column] = value
    for p in range(n):
        column_entry(0, p + 1, Fraction(1, 2))
        column_entry(n + 1 + p, p + 1, Fraction(1, 2))
    for (p, q), rows in expected_pair_rows.items():
        coefficient = Fraction(1, 4) if len(rows) == 2 else Fraction(1, 2)
        for row in rows:
            column_entry(row, p + 1, coefficient)
            column_entry(row, q + 1, coefficient)
    for (i, j), coefficient in list(expected_action.items()):
        column_entry(j, i, coefficient * metric[i] / metric[j])
    actual_action = {}
    for entry in magnetic["entries"]:
        require(isinstance(entry, list) and len(entry) == 3 and type(entry[0]) is int and type(entry[1]) is int,
                "sparse entry shape")
        i, j, value = entry
        require(0 <= i < 561 and 0 <= j < 561 and (i, j) not in actual_action, "valid unique sparse indices")
        value = rational(value)
        require(value != 0, "no stored structural zero")
        actual_action[i, j] = value
    # Exact dictionary equality covers every nonzero and every absent/structural
    # zero, including all newly retained input columns, not just P0 columns.
    require(actual_action == expected_action, "entire S action, including structural zeros/new inputs")
    require(all(metric[i] * value == metric[j] * actual_action[j, i] for (i, j), value in actual_action.items()),
            "physical metric self-adjointness")
    require(magnetic["nonzero_count" if side == "forward" else "nonzero_entries"] == len(actual_action) == 2124,
            "actual sparse support")
    require(magnetic["zero_count" if side == "forward" else "zero_entries"] == 561 ** 2 - len(actual_action) == 312597,
            "actual structural zero count")
    coefficients = [Fraction(0) if kind in ("vacuum", "face") else Fraction(1, 2) if kind == "pair" else Fraction(1, 4)
                    for kind, *_ in expected_basis]
    residual_norm = sum((a * a * m for a, m in zip(coefficients, metric)), Fraction(0))
    residual_energy = sum((a * a * m * k for a, m, k in zip(coefficients, metric, energies)), Fraction(0))
    require(residual_norm == Fraction(1653, 16) and residual_energy == Fraction(1247, 2), "complete residual channels")
    return {"basis_dimension": 561, "pair_masks": 406, "magnetic_nonzero_entries": 2124,
            "structural_zeros": 312597, "scope": "exact generated-span and sparse-action verification; no new physical investigation"}


def product_sign(values):
    answer = 1
    for value in values:
        answer *= value
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", choices=["forward", "reverse"], required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    output = root / "research/round28" / args.side / "ah1/output"
    result = json.loads((output / "results.json").read_text())
    artifacts = {name: json.loads((output / name).read_text()) for name in ["graph.json", "basis.json", "magnetic.json"]} if args.side == "reverse" else {}
    print(json.dumps(verify(result, args.side, artifacts), sort_keys=True))


if __name__ == "__main__":
    main()
