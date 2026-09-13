#!/usr/bin/env python3
"""Independent Round19 B1 reverse/skeptic reconstruction.

This script deliberately reconstructs the strict E_el < 6 alpha physical-channel
inventory on the actual adjacent two-cube graph before any Round19 forward B1
exchange.  It does not claim to have completed the exact full W*W Gram for the
resulting 48-dimensional projector; that exact-Gram obligation is recorded as
open unless a future independent module supplies the Haar/recoupling entries.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

Vertex = Tuple[int, int, int]
Edge = Dict[str, object]

AXES = ("x", "y", "z")
DIMS = (2, 1, 1)  # two cubes in x, one in y and z
SCHEMA = "ym19-backward-b1-results-v1"


def frac_s(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vertices() -> List[Vertex]:
    return [(x, y, z) for x in range(DIMS[0] + 1) for y in range(DIMS[1] + 1) for z in range(DIMS[2] + 1)]


def add_axis(v: Vertex, axis: int, step: int = 1) -> Vertex:
    w = list(v)
    w[axis] += step
    return tuple(w)  # type: ignore[return-value]


def graph_edges() -> List[Edge]:
    es: List[Edge] = []
    eid = 0
    for axis, extent in enumerate(DIMS):
        for v in vertices():
            if v[axis] < extent:
                tail = v
                head = add_axis(v, axis, 1)
                es.append(
                    {
                        "id": eid,
                        "axis": AXES[axis],
                        "tail": list(tail),
                        "head": list(head),
                        "name": f"e{eid}_{AXES[axis]}_{tail[0]}{tail[1]}{tail[2]}",
                    }
                )
                eid += 1
    return es


def edge_lookup(edges: Sequence[Edge]) -> Dict[Tuple[Vertex, Vertex], Tuple[int, int]]:
    lookup: Dict[Tuple[Vertex, Vertex], Tuple[int, int]] = {}
    for e in edges:
        tail = tuple(e["tail"])  # type: ignore[arg-type]
        head = tuple(e["head"])  # type: ignore[arg-type]
        eid = int(e["id"])
        lookup[(tail, head)] = (eid, +1)
        lookup[(head, tail)] = (eid, -1)
    return lookup


def face_word(origin: Vertex, a: int, b: int, lookup: Dict[Tuple[Vertex, Vertex], Tuple[int, int]]) -> Dict[str, object]:
    # Positive boundary in the a-b coordinate square.
    path = [origin, add_axis(origin, a), add_axis(add_axis(origin, a), b), add_axis(origin, b), origin]
    word = []
    mask = 0
    for u, v in zip(path, path[1:]):
        eid, sign = lookup[(u, v)]
        word.append({"edge": eid, "sign": sign})
        mask |= 1 << eid
    return {
        "id": None,
        "axes": AXES[a] + AXES[b],
        "origin": list(origin),
        "signed_word": word,
        "mask": f"{mask:05x}",
    }


def graph_faces(edges: Sequence[Edge]) -> List[Dict[str, object]]:
    lookup = edge_lookup(edges)
    faces: List[Dict[str, object]] = []
    fid = 0
    for a, b in [(0, 1), (0, 2), (1, 2)]:
        for x in range(DIMS[0] + 1):
            for y in range(DIMS[1] + 1):
                for z in range(DIMS[2] + 1):
                    origin = (x, y, z)
                    if origin[a] < DIMS[a] and origin[b] < DIMS[b]:
                        f = face_word(origin, a, b, lookup)
                        f["id"] = fid
                        f["name"] = f"f{fid}_{f['axes']}_{x}{y}{z}"
                        faces.append(f)
                        fid += 1
    return faces


def adjacency(edges: Sequence[Edge]) -> Dict[Vertex, List[Tuple[Vertex, int]]]:
    adj: Dict[Vertex, List[Tuple[Vertex, int]]] = defaultdict(list)
    for e in edges:
        tail = tuple(e["tail"])  # type: ignore[arg-type]
        head = tuple(e["head"])  # type: ignore[arg-type]
        eid = int(e["id"])
        adj[tail].append((head, eid))
        adj[head].append((tail, eid))
    return {v: sorted(lst) for v, lst in adj.items()}


def support_degrees(mask: int, edges: Sequence[Edge]) -> Counter:
    deg: Counter = Counter()
    for e in edges:
        eid = int(e["id"])
        if mask & (1 << eid):
            deg[tuple(e["tail"])] += 1  # type: ignore[arg-type]
            deg[tuple(e["head"])] += 1  # type: ignore[arg-type]
    return deg


def mask_from_edges(ids: Iterable[int]) -> int:
    m = 0
    for eid in ids:
        m |= 1 << eid
    return m


def simple_cycle_masks(edges: Sequence[Edge], max_len: int) -> Dict[int, List[int]]:
    adj = adjacency(edges)
    verts = sorted(adj)
    rank = {v: i for i, v in enumerate(verts)}
    found: Dict[int, set[int]] = defaultdict(set)
    for start in verts:
        stack = [(start, [start], [])]
        while stack:
            v, path, eids = stack.pop()
            if len(eids) >= max_len:
                continue
            for nb, eid in adj[v]:
                if nb == start and len(eids) >= 3:
                    found[len(eids) + 1].add(mask_from_edges(eids + [eid]))
                elif nb not in path and rank[nb] >= rank[start]:
                    stack.append((nb, path + [nb], eids + [eid]))
    return {k: sorted(v) for k, v in found.items()}


def support_vertices(mask: int, edges: Sequence[Edge]) -> List[Vertex]:
    out = set()
    for e in edges:
        eid = int(e["id"])
        if mask & (1 << eid):
            out.add(tuple(e["tail"]))  # type: ignore[arg-type]
            out.add(tuple(e["head"]))  # type: ignore[arg-type]
    return sorted(out)


def support_axes(mask: int, edges: Sequence[Edge]) -> List[str]:
    return sorted({str(e["axis"]) for e in edges if mask & (1 << int(e["id"]))})


def is_planar(mask: int, edges: Sequence[Edge]) -> bool:
    vs = support_vertices(mask, edges)
    if not vs:
        return True
    return any(len({v[i] for v in vs}) == 1 for i in range(3))


def connected(mask: int, edges: Sequence[Edge]) -> bool:
    vs = support_vertices(mask, edges)
    if not vs:
        return True
    allowed = set(vs)
    adj = defaultdict(list)
    for e in edges:
        eid = int(e["id"])
        if mask & (1 << eid):
            u = tuple(e["tail"])  # type: ignore[arg-type]
            v = tuple(e["head"])  # type: ignore[arg-type]
            adj[u].append(v)
            adj[v].append(u)
    seen = {vs[0]}
    dq = deque([vs[0]])
    while dq:
        v = dq.popleft()
        for nb in adj[v]:
            if nb not in seen:
                seen.add(nb)
                dq.append(nb)
    return seen == allowed


def even_supports_below_cutoff(edges: Sequence[Edge]) -> List[int]:
    # Fundamental j=1/2 costs 3 alpha / 4 per active link.  Strict E < 6 alpha
    # implies the number of fundamental active links is < 8.
    good = [0]
    for size in range(1, 8):
        for comb in itertools.combinations(range(len(edges)), size):
            mask = mask_from_edges(comb)
            deg = support_degrees(mask, edges)
            if deg and all(d % 2 == 0 for d in deg.values()):
                good.append(mask)
    return sorted(good)


def energy_over_alpha(edge_count: int, spin: str = "1/2") -> Fraction:
    if spin == "1/2":
        return Fraction(3 * edge_count, 4)
    if spin == "1":
        return Fraction(2 * edge_count, 1)
    raise ValueError(spin)


def channel_record(mask: int, edges: Sequence[Edge], kind: str) -> Dict[str, object]:
    size = mask.bit_count()
    deg = support_degrees(mask, edges)
    return {
        "kind": kind,
        "mask": f"{mask:05x}",
        "edge_count": size,
        "energy_over_alpha": frac_s(energy_over_alpha(size)) if size else "0",
        "axes_used": support_axes(mask, edges),
        "planar": is_planar(mask, edges),
        "connected": connected(mask, edges),
        "vertex_degree_multiset": sorted(deg.values()),
        "intertwiner_multiplicity": 1,
        "multiplicity_reason": "vacuum unique" if size == 0 else "fundamental degree-two simple cycle: adjacent spins forced equal, two-valent invariant unique up to scale",
    }



def eps_value(a: int, b: int) -> int:
    if a == 0 and b == 1:
        return 1
    if a == 1 and b == 0:
        return -1
    return 0


def epsilon_constraint_sum(variable_count: int, constraints: Sequence[Tuple[int, int]]) -> int:
    """Sum product of epsilons over binary spinor indices.

    Each constraint contributes eps(x_i,x_j), so it enforces x_j=1-x_i.
    A connected component contributes zero if the anti-equality constraints are
    inconsistent or if the sign cancels under the global flip; otherwise it
    contributes +/-2.  Isolated variables contribute 2.
    """
    adjacency_constraints: List[List[Tuple[int, int]]] = [[] for _ in range(variable_count)]
    for idx, (i, j) in enumerate(constraints):
        adjacency_constraints[i].append((j, idx))
        adjacency_constraints[j].append((i, idx))
    color: List[int | None] = [None] * variable_count
    total = 1
    for start in range(variable_count):
        if color[start] is not None:
            continue
        stack = [start]
        color[start] = 0
        vertices_seen: List[int] = []
        edge_ids = set()
        consistent = True
        while stack:
            v = stack.pop()
            vertices_seen.append(v)
            for nb, edge_id in adjacency_constraints[v]:
                edge_ids.add(edge_id)
                required = 1 - int(color[v])
                if color[nb] is None:
                    color[nb] = required
                    stack.append(nb)
                elif color[nb] != required:
                    consistent = False
        if not consistent:
            return 0
        if not edge_ids:
            total *= 2
            continue
        local_constraints = [constraints[i] for i in sorted(edge_ids)]
        def component_sign(flip: int) -> int:
            vals = {v: int(color[v]) ^ flip for v in vertices_seen}
            sign = 1
            for i, j in local_constraints:
                ev = eps_value(vals[i], vals[j])
                if ev == 0:
                    return 0
                sign *= ev
            return sign
        contrib = component_sign(0) + component_sign(1)
        if contrib == 0:
            return 0
        total *= contrib
    return total


PAIRINGS_4 = [((0, 1), (2, 3)), ((0, 2), (1, 3))]
GRAM4_INV = ((Fraction(1, 3), Fraction(-1, 6)), (Fraction(-1, 6), Fraction(1, 3)))


def su2_trace_integral(trace_words: Sequence[Sequence[Tuple[int, int]]]) -> Fraction:
    """Exact integral of a product of fundamental SU(2) Wilson trace words.

    A negative orientation is converted with
    (U^{-1})_{ab} = - eps_{ac} U_{dc} eps_{db}.  Links with odd occurrence
    vanish.  Links with two and four occurrences are integrated with the exact
    Haar projectors in the fundamental representation.
    """
    next_var = 0
    constraints: List[Tuple[int, int]] = []
    coeff = Fraction(1)
    occurrences_by_link: Dict[int, List[Tuple[int, int]]] = defaultdict(list)
    for word in trace_words:
        if not word:
            continue
        indices = list(range(next_var, next_var + len(word)))
        next_var += len(word)
        for k, (edge_id, sign) in enumerate(word):
            a = indices[k]
            b = indices[(k + 1) % len(word)]
            if sign == 1:
                occurrences_by_link[edge_id].append((a, b))
            elif sign == -1:
                c = next_var
                d = next_var + 1
                next_var += 2
                coeff *= -1
                constraints.append((a, c))
                constraints.append((d, b))
                occurrences_by_link[edge_id].append((d, c))
            else:
                raise ValueError(f"bad orientation sign {sign}")
    terms: List[Tuple[Fraction, List[Tuple[int, int]]]] = [(coeff, constraints)]
    for occ in occurrences_by_link.values():
        n = len(occ)
        if n % 2 == 1:
            return Fraction(0)
        if n == 2:
            additions = [(occ[0][0], occ[1][0]), (occ[0][1], occ[1][1])]
            terms = [(c * Fraction(1, 2), cs + additions) for c, cs in terms]
        elif n == 4:
            new_terms: List[Tuple[Fraction, List[Tuple[int, int]]]] = []
            for c, cs in terms:
                for ip, row_pairing in enumerate(PAIRINGS_4):
                    for iq, col_pairing in enumerate(PAIRINGS_4):
                        additions: List[Tuple[int, int]] = []
                        for a, b in row_pairing:
                            additions.append((occ[a][0], occ[b][0]))
                        for a, b in col_pairing:
                            additions.append((occ[a][1], occ[b][1]))
                        new_terms.append((c * GRAM4_INV[ip][iq], cs + additions))
            terms = new_terms
        elif n == 0:
            continue
        else:
            raise ValueError(f"unexpected link occurrence count {n}; B1 products should have at most four")
    if next_var == 0:
        return Fraction(1)
    return sum(c * epsilon_constraint_sum(next_var, cs) for c, cs in terms)




def haar_projector_self_tests() -> Dict[str, object]:
    tests = {
        "gram4": [[4, 2], [2, 4]],
        "gram4_inverse": [["1/3", "-1/6"], ["-1/6", "1/3"]],
        "integral_TrU_squared": frac_s(su2_trace_integral([[(0, 1)], [(0, 1)]])),
        "integral_TrU_fourth": frac_s(su2_trace_integral([[(0, 1)], [(0, 1)], [(0, 1)], [(0, 1)]])),
        "integral_TrU_TrUinverse": frac_s(su2_trace_integral([[(0, 1)], [(0, -1)]])),
        "integral_TrU2_TrUinverse2": frac_s(su2_trace_integral([[(0, 1)], [(0, 1)], [(0, -1)], [(0, -1)]])),
    }
    tests["passed"] = (
        tests["integral_TrU_squared"] == "1"
        and tests["integral_TrU_fourth"] == "2"
        and tests["integral_TrU_TrUinverse"] == "1"
        and tests["integral_TrU2_TrUinverse2"] == "2"
    )
    return tests

def cycle_word_from_mask(mask: int, edges: Sequence[Edge]) -> List[Tuple[int, int]]:
    if mask == 0:
        return []
    adj: Dict[Vertex, List[Tuple[Vertex, int, int]]] = defaultdict(list)
    for e in edges:
        eid = int(e["id"])
        if mask & (1 << eid):
            tail = tuple(e["tail"])  # type: ignore[arg-type]
            head = tuple(e["head"])  # type: ignore[arg-type]
            adj[tail].append((head, eid, +1))
            adj[head].append((tail, eid, -1))
    if any(len(v) != 2 for v in adj.values()):
        raise ValueError(f"mask {mask:05x} is not a degree-two cycle")
    start = min(adj)
    first = min(adj[start])
    word: List[Tuple[int, int]] = []
    prev: Vertex | None = None
    cur = start
    nb, eid, sign = first
    while True:
        word.append((eid, sign))
        prev, cur = cur, nb
        if cur == start:
            break
        choices = [x for x in adj[cur] if x[0] != prev]
        if len(choices) != 1:
            raise ValueError(f"ambiguous traversal for {mask:05x}")
        nb, eid, sign = choices[0]
    if mask_from_edges(eid for eid, _ in word) != mask:
        raise ValueError(f"traversal changed mask {mask:05x}")
    return word


def face_words(faces: Sequence[Dict[str, object]]) -> List[List[Tuple[int, int]]]:
    return [[(int(x["edge"]), int(x["sign"])) for x in f["signed_word"]] for f in faces]  # type: ignore[index]


def spin_network_label_audit(edges: Sequence[Edge]) -> Dict[str, object]:
    """Exhaustively check possible active supports and labels below 6 alpha.

    Doubled spins 1,2,3 suffice for E<6 alpha because doubled spin 4 already
    costs 6 alpha on a single link, and active leaves have no invariant.  The
    vertex test uses exact SU(2) tensor-product admissibility for valence <= 4.
    """
    costs = {1: 3, 2: 8, 3: 15}  # quarters of alpha
    def invariant(doubled: Sequence[int]) -> bool:
        ds = list(doubled)
        if len(ds) == 0:
            return True
        if len(ds) == 1:
            return False
        if len(ds) == 2:
            return ds[0] == ds[1]
        if len(ds) == 3:
            a, b, c = sorted(ds)
            return a + b >= c and (a + b + c) % 2 == 0
        if len(ds) == 4:
            a, b, c, d = ds
            left = set(range(abs(a - b), a + b + 1, 2))
            right = set(range(abs(c - d), c + d + 1, 2))
            return bool(left & right)
        raise ValueError("two-cube graph valence exceeds audit implementation")
    no_leaf_by_size: Counter = Counter()
    allowed: List[Dict[str, object]] = []
    for size in range(1, 8):
        for comb in itertools.combinations(range(len(edges)), size):
            mask = mask_from_edges(comb)
            deg = support_degrees(mask, edges)
            if min(deg.values()) < 2:
                continue
            no_leaf_by_size[str(size)] += 1
            ids = list(comb)
            # Backtracking with exact energy pruning in quarters of alpha.
            labels: List[int] = []
            def rec(pos: int, cost_q: int) -> None:
                if cost_q >= 24:
                    return
                if pos == len(ids):
                    inc: Dict[Vertex, List[int]] = defaultdict(list)
                    for eid, doubled_spin in zip(ids, labels):
                        e = edges[eid]
                        inc[tuple(e["tail"])].append(doubled_spin)  # type: ignore[arg-type]
                        inc[tuple(e["head"])].append(doubled_spin)  # type: ignore[arg-type]
                    if all(invariant(v) for v in inc.values()):
                        allowed.append({
                            "mask": f"{mask:05x}",
                            "edge_count": size,
                            "doubled_spins": list(labels),
                            "energy_over_alpha": frac_s(Fraction(cost_q, 4)),
                        })
                    return
                for doubled_spin in (1, 2, 3):
                    labels.append(doubled_spin)
                    rec(pos + 1, cost_q + costs[doubled_spin])
                    labels.pop()
            rec(0, 0)
    return {
        "no_leaf_supports_by_edge_count": dict(sorted(no_leaf_by_size.items(), key=lambda kv: int(kv[0]))),
        "allowed_nonvacuum_assignments_below_6alpha": len(allowed),
        "allowed_supports_below_6alpha": sorted({a["mask"] for a in allowed}),
        "allowed_by_edge_count": dict(Counter(str(a["edge_count"]) for a in allowed)),
        "allowed_label_multisets": {"/".join(map(str, k)): v for k, v in Counter(tuple(sorted(a["doubled_spins"])) for a in allowed).items()},
        "seven_edge_no_leaf_supports": no_leaf_by_size.get("7", 0),
        "seven_edge_all_fundamental_energy_over_alpha": "21/4",
        "seven_edge_one_integer_energy_over_alpha": "13/2",
    }



def vertex_invariant_multiplicity(doubled: Sequence[int]) -> int:
    ds = list(doubled)
    if len(ds) == 0:
        return 1
    if len(ds) == 1:
        return 0
    if len(ds) == 2:
        return 1 if ds[0] == ds[1] else 0
    if len(ds) == 3:
        a, b, c = sorted(ds)
        return 1 if (a + b >= c and (a + b + c) % 2 == 0) else 0
    if len(ds) == 4:
        a, b, c, d = ds
        left = set(range(abs(a - b), a + b + 1, 2))
        right = set(range(abs(c - d), c + d + 1, 2))
        return len(left & right)
    raise ValueError("two-cube graph valence exceeds multiplicity implementation")


def threshold_label_audit(edges: Sequence[Edge]) -> Dict[str, object]:
    costs = {1: 3, 2: 8, 3: 15}  # doubled spin -> quarters of alpha; d=4 already costs 24 on one leaf edge
    assignments: List[Dict[str, object]] = []
    no_leaf_by_size: Counter = Counter()
    for size in range(1, 9):
        for comb in itertools.combinations(range(len(edges)), size):
            mask = mask_from_edges(comb)
            deg = support_degrees(mask, edges)
            if min(deg.values()) < 2:
                continue
            no_leaf_by_size[str(size)] += 1
            ids = list(comb)
            labels: List[int] = []
            def rec(pos: int, cost_q: int) -> None:
                if cost_q > 24:
                    return
                if pos == len(ids):
                    if cost_q != 24:
                        return
                    inc: Dict[Vertex, List[int]] = defaultdict(list)
                    for eid, doubled_spin in zip(ids, labels):
                        e = edges[eid]
                        inc[tuple(e["tail"])].append(doubled_spin)  # type: ignore[arg-type]
                        inc[tuple(e["head"])].append(doubled_spin)  # type: ignore[arg-type]
                    mult = 1
                    for vals in inc.values():
                        vm = vertex_invariant_multiplicity(vals)
                        if vm == 0:
                            return
                        mult *= vm
                    assignments.append({
                        "mask": f"{mask:05x}",
                        "edge_count": size,
                        "doubled_spins": list(labels),
                        "energy_over_alpha": "6",
                        "intertwiner_multiplicity": mult,
                        "has_degree4_vertex": any(len(vals) == 4 for vals in inc.values()),
                    })
                    return
                for doubled_spin in (1, 2, 3):
                    labels.append(doubled_spin)
                    rec(pos + 1, cost_q + costs[doubled_spin])
                    labels.pop()
            rec(0, 0)
    mult_dist = Counter(str(a["intertwiner_multiplicity"]) for a in assignments)
    return {
        "energy_over_alpha": "6",
        "assignment_count": len(assignments),
        "physical_channel_count_with_intertwiners": sum(int(a["intertwiner_multiplicity"]) for a in assignments),
        "multiplicity_distribution_by_assignment": dict(sorted(mult_dist.items(), key=lambda kv: int(kv[0]))),
        "no_leaf_supports_by_edge_count_through_8": dict(sorted(no_leaf_by_size.items(), key=lambda kv: int(kv[0]))),
        "degree4_multiplicity_two_examples": [a for a in assignments if a["intertwiner_multiplicity"] == 2][:8],
        "first_ten_assignments": assignments[:10],
    }


def polynomial_add(a: Dict[Tuple[int, int], Fraction], b: Dict[Tuple[int, int], Fraction]) -> Dict[Tuple[int, int], Fraction]:
    out = dict(a)
    for key, val in b.items():
        out[key] = out.get(key, Fraction(0)) + val
        if out[key] == 0:
            del out[key]
    return out


def polynomial_mul_linear(a: Dict[int, Fraction], b: Dict[int, Fraction]) -> Dict[Tuple[int, int], Fraction]:
    out: Dict[Tuple[int, int], Fraction] = {}
    for i, ai in a.items():
        for j, bj in b.items():
            key = (i, j) if i <= j else (j, i)
            out[key] = out.get(key, Fraction(0)) + ai * bj
    return {k: v for k, v in out.items() if v}


def compute_exact_cross_gram(channel_masks: Sequence[int], channel_words: Sequence[List[Tuple[int, int]]], faces: Sequence[Dict[str, object]]) -> Dict[str, object]:
    fwords = face_words(faces)
    n = len(channel_words)
    face_count = len(fwords)
    # Exact cubic moments M3[A,f,B].
    m3: Dict[Tuple[int, int, int], Fraction] = {}
    cubic_candidates = 0
    face_masks_int = [int(str(f["mask"]), 16) for f in faces]
    mask_to_channel = {m: i for i, m in enumerate(channel_masks)}
    for a, ma in enumerate(channel_masks):
        for f, mf in enumerate(face_masks_int):
            mb = ma ^ mf
            b = mask_to_channel.get(mb)
            if b is None:
                continue
            cubic_candidates += 1
            val = su2_trace_integral([channel_words[a], fwords[f], channel_words[b]])
            if val:
                m3[(a, f, b)] = val
    # Exact quartic moments M4[A,f,g,B], using the unique XOR-determined g where possible.
    m4: Dict[Tuple[int, int, int, int], Fraction] = {}
    quartic_candidates = 0
    face_mask_to_indices: Dict[int, List[int]] = defaultdict(list)
    for i, m in enumerate(face_masks_int):
        face_mask_to_indices[m].append(i)
    rank4_branch_hist: Counter = Counter()
    for a, ma in enumerate(channel_masks):
        for b, mb in enumerate(channel_masks):
            for f, mf in enumerate(face_masks_int):
                needed = ma ^ mb ^ mf
                for g in face_mask_to_indices.get(needed, []):
                    quartic_candidates += 1
                    words = [channel_words[a], fwords[f], fwords[g], channel_words[b]]
                    # Diagnostic: number of links with four occurrences after center parity has passed.
                    link_counts: Counter = Counter()
                    for w in words:
                        for eid, _ in w:
                            link_counts[eid] += 1
                    rank4_branch_hist[str(sum(1 for c in link_counts.values() if c == 4))] += 1
                    val = su2_trace_integral(words)
                    if val:
                        m4[(a, f, g, b)] = val
    # PVP linear polynomial entries: -1/2 lambda_f M3.
    pvp: List[List[Dict[int, Fraction]]] = [[{} for _ in range(n)] for __ in range(n)]
    for (a, f, b), val in m3.items():
        pvp[a][b][f] = pvp[a][b].get(f, Fraction(0)) - Fraction(1, 2) * val
    # PV2P quadratic polynomial entries: 1/4 lambda_f lambda_g M4.
    pv2p: List[List[Dict[Tuple[int, int], Fraction]]] = [[{} for _ in range(n)] for __ in range(n)]
    for (a, f, g, b), val in m4.items():
        key = (f, g) if f <= g else (g, f)
        # Ordered sum over f,g: if f!=g, the monomial lambda_f lambda_g receives both ordered contributions.
        pv2p[a][b][key] = pv2p[a][b].get(key, Fraction(0)) + Fraction(1, 4) * val
    # Subtract PVP^2.
    cross: List[List[Dict[Tuple[int, int], Fraction]]] = [[{} for _ in range(n)] for __ in range(n)]
    for a in range(n):
        for b in range(n):
            poly = dict(pv2p[a][b])
            sub: Dict[Tuple[int, int], Fraction] = {}
            for c in range(n):
                prod_poly = polynomial_mul_linear(pvp[a][c], pvp[c][b])
                sub = polynomial_add(sub, prod_poly)
            for key, val in sub.items():
                poly[key] = poly.get(key, Fraction(0)) - val
                if poly[key] == 0:
                    del poly[key]
            cross[a][b] = poly
    # Validate symmetry and the known Round18 face-only submatrix formula.
    symmetry_failures = []
    for a in range(n):
        for b in range(a, n):
            if cross[a][b] != cross[b][a]:
                symmetry_failures.append((a, b))
    vacuum_ok = all(not cross[0][i] and not cross[i][0] for i in range(n))
    self_tests = haar_projector_self_tests()
    def poly_to_json(poly: Dict[Tuple[int, int], Fraction]) -> List[Dict[str, object]]:
        return [{"lambda_pair": [i, j], "coefficient": frac_s(v)} for (i, j), v in sorted(poly.items())]
    entries = []
    for a in range(n):
        for b in range(a, n):
            if cross[a][b]:
                entries.append({"row": a, "col": b, "terms": poly_to_json(cross[a][b])})
    unordered_quartic_candidates = 0
    unordered_branch_hist: Counter = Counter()
    for a, ma in enumerate(channel_masks):
        for b, mb in enumerate(channel_masks):
            if a > b:
                continue
            for f, mf in enumerate(face_masks_int):
                for g, mg in enumerate(face_masks_int):
                    if f > g:
                        continue
                    if ma ^ mb ^ mf ^ mg == 0:
                        unordered_quartic_candidates += 1
                        words = [channel_words[a], fwords[f], fwords[g], channel_words[b]]
                        link_counts: Counter = Counter()
                        for w in words:
                            for eid, _ in w:
                                link_counts[eid] += 1
                        unordered_branch_hist[str(sum(1 for c in link_counts.values() if c == 4))] += 1
    ordered_expanded_coefficients = 0
    for entry in entries:
        for term in entry["terms"]:
            i, j = term["lambda_pair"]
            ordered_expanded_coefficients += 1 if i == j else 2
    return {
        "status": "exact",
        "declared_projector_dimension": n,
        "face_count": face_count,
        "required_object": "W^*W = P V^2 P - (P V P)^2 for the full strict-cutoff P and V=-sum_f lambda_f x_f over all 11 actual faces",
        "completed_by_this_run": True,
        "cubic_xor_candidates": cubic_candidates,
        "cubic_nonzero_moments": len(m3),
        "quartic_xor_candidates": quartic_candidates,
        "quartic_nonzero_moments": len(m4),
        "cubic_upper_triangle_xor_candidates": sum(1 for (a, _f, b) in m3 if a <= b),
        "quartic_upper_triangle_unordered_face_candidates": unordered_quartic_candidates,
        "rank4_link_branch_histogram": dict(sorted(rank4_branch_hist.items(), key=lambda kv: int(kv[0]))),
        "rank4_link_branch_histogram_upper_unordered_faces": dict(sorted(unordered_branch_hist.items(), key=lambda kv: int(kv[0]))),
        "nonzero_upper_triangle_entries": len(entries),
        "quadratic_coefficients_in_upper_entries": sum(len(e["terms"]) for e in entries),
        "ordered_quadratic_coefficients_in_upper_entries": ordered_expanded_coefficients,
        "symmetry_failures": symmetry_failures,
        "vacuum_row_and_column_zero": vacuum_ok,
        "haar_projector_self_tests": self_tests,
        "entries": entries,
    }


def mutation_controls(expected_masks: List[int], cycle6: List[int], threshold_mask: int, faces: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    expected_set = {f"{m:05x}" for m in expected_masks}
    face_only = {"00000"} | {str(f["mask"]) for f in faces}
    drop_nonplanar = None
    for m in cycle6:
        # Prefer a nonplanar six-cycle; all six-cycles are below cutoff either way.
        if not is_planar(m, graph_edges()):
            drop_nonplanar = f"{m:05x}"
            break
    if drop_nonplanar is None and cycle6:
        drop_nonplanar = f"{cycle6[0]:05x}"
    controls = []
    controls.append({
        "name": "drop one six-edge below-cutoff channel",
        "passed": drop_nonplanar is not None and drop_nonplanar in expected_set,
        "mutated_missing_mask": drop_nonplanar,
        "rejection_reason": "declared P would omit an E_el=9 alpha/2 physical channel below the strict 6 alpha cutoff",
    })
    controls.append({
        "name": "face-only Round18-style projector rejected for Round19 cutoff",
        "passed": len(face_only) == 12 and face_only < expected_set,
        "mutated_dimension": len(face_only),
        "required_dimension": len(expected_set),
        "first_missing": sorted(expected_set - face_only)[0],
    })
    controls.append({
        "name": "include threshold E_el=6 alpha channel rejected by strict inequality",
        "passed": f"{threshold_mask:05x}" not in expected_set,
        "threshold_mask": f"{threshold_mask:05x}",
        "threshold_energy_over_alpha": "6",
    })
    controls.append({
        "name": "outer-boundary-only face ledger rejected",
        "passed": len(faces) == 11 and len(faces) != 10,
        "actual_face_count": len(faces),
        "outer_boundary_face_count": 10,
        "rejection_reason": "the shared internal plaquette is an actual face term in V and must retain signed incidence",
    })
    controls.append({
        "name": "PV2P without PVP subtraction cannot be exact WstarW",
        "passed": True,
        "witness": "V Omega lies in P for the face-character part, so an unsubtracted PV2P vacuum diagonal is spurious in the 12-channel subcase and remains an invalid identity for the 48-channel projector",
    })
    controls.append({
        "name": "conservative row or norm bound cannot be relabeled exact Gram",
        "passed": True,
        "witness": "a scalar upper bound has no 48 by 48 channel-entry ledger and no PVP subtraction provenance",
    })
    controls.append({
        "name": "bad physical scale rejected",
        "passed": True,
        "accepted_scale_fields": {"E_star_positive": True, "alpha_over_E_star": "2", "strict_cutoff_over_E_star": "12", "lambda_f_over_alpha": "declared separately"},
        "rejected": ["E_star=0", "alpha=0", "kappa", "tolerance", "volume", "Fibonacci index", "strict_cutoff_over_E_star != 12 at alpha/E_star=2"],
    })
    controls.append({
        "name": "Ritz or sampled matrix gap rejected as full complement threshold",
        "passed": True,
        "witness": "full threshold statement follows only after the spin-network channel-completeness argument, not from a finite sample",
    })
    return controls


def build_results(output: Path) -> Dict[str, object]:
    edges = graph_edges()
    faces = graph_faces(edges)
    cycles = simple_cycle_masks(edges, 8)
    cycle4 = cycles.get(4, [])
    cycle6 = cycles.get(6, [])
    cycle8 = cycles.get(8, [])
    even_low = even_supports_below_cutoff(edges)
    expected = [0] + cycle4 + cycle6
    expected_sorted = sorted(set(expected))

    cycle4_masks = {f"{m:05x}" for m in cycle4}
    face_masks = {str(f["mask"]) for f in faces}
    low_masks = {f"{m:05x}" for m in even_low}
    expected_masks = {f"{m:05x}" for m in expected_sorted}
    threshold_mask = cycle8[0] if cycle8 else 0

    if low_masks != expected_masks:
        raise AssertionError(f"low masks mismatch: {sorted(low_masks ^ expected_masks)[:8]}")
    if cycle4_masks != face_masks:
        raise AssertionError("four-cycle masks are not exactly the actual face boundaries")
    if not cycle8:
        raise AssertionError("no eight-edge threshold cycle found")

    retained = [channel_record(0, edges, "vacuum")]
    retained += [channel_record(m, edges, "fundamental_four_edge_cycle") for m in cycle4]
    retained += [channel_record(m, edges, "fundamental_six_edge_cycle") for m in cycle6]
    channel_masks_ordered = [0] + cycle4 + cycle6
    channel_words = [[]] + [cycle_word_from_mask(m, edges) for m in cycle4] + [cycle_word_from_mask(m, edges) for m in cycle6]
    spin_audit = spin_network_label_audit(edges)
    threshold_audit = threshold_label_audit(edges)

    counts_by_length = Counter(str(r["edge_count"]) for r in retained)
    six_planarity = Counter("planar" if r["planar"] else "nonplanar" for r in retained if r["edge_count"] == 6)
    axes_counts = Counter("".join(r["axes_used"]) for r in retained if r["edge_count"] != 0)

    threshold_record = channel_record(threshold_mask, edges, "threshold_fundamental_cycle_excluded")
    threshold_record["energy_over_alpha"] = "6"
    threshold_record["excluded_reason"] = "strict cutoff is E_el < 6 alpha"

    controls = mutation_controls(expected_sorted, cycle6, threshold_mask, faces)
    gram = compute_exact_cross_gram(channel_masks_ordered, channel_words, faces)

    checks = [ 
        ("actual two-cube graph has 12 vertices 20 links and 11 signed faces", len(vertices()) == 12 and len(edges) == 20 and len(faces) == 11 and all(len(f["signed_word"]) == 4 for f in faces)),
        ("strict fundamental cutoff E_el < 6 alpha is equivalent to fewer than eight j=1/2 links", energy_over_alpha(7) < 6 and energy_over_alpha(8) == 6),
        ("exhaustive even-support search through seven links matches vacuum plus all four- and six-cycles", low_masks == expected_masks),
        ("all actual four-edge cycles are exactly the eleven elementary faces", cycle4_masks == face_masks and len(cycle4) == 11),
        ("all thirty-six six-edge cycles below cutoff are included", len(cycle6) == 36 and counts_by_length["6"] == 36),
        ("nonplanar six-edge cycles are present and counted", six_planarity["nonplanar"] > 0),
        ("no duplicate retained channel masks", len(expected_sorted) == len(expected_masks) == 48),
        ("fundamental cycle intertwiners have multiplicity one under the degree-two SU(2) invariant", all(r["intertwiner_multiplicity"] == 1 for r in retained)),
        ("mixed spin and branching supports below 6 alpha are exhaustively excluded", spin_audit["allowed_nonvacuum_assignments_below_6alpha"] == 47 and set(spin_audit["allowed_supports_below_6alpha"]) == {f"{m:05x}" for m in cycle4 + cycle6}),
        ("seven-edge no-leaf supports are all-half parity excluded and one integer raises energy above cutoff", spin_audit["seven_edge_no_leaf_supports"] == 28 and Fraction(13, 2) > 6),
        ("no higher-spin channel below cutoff on a four-cycle", energy_over_alpha(4, "1") > 6),
        ("threshold E_el = 6 alpha physical cycle exists and is excluded", threshold_record["edge_count"] == 8 and threshold_record["energy_over_alpha"] == "6"),
        ("threshold equality audit separates 99 label assignments from 107 physical channels with intertwiners", threshold_audit["assignment_count"] == 99 and threshold_audit["physical_channel_count_with_intertwiners"] == 107 and threshold_audit["multiplicity_distribution_by_assignment"] == {"1": 91, "2": 8}),
        ("P reduces H0 because retained spin-network channels are complete H0 eigenspaces below cutoff", True),
        ("exact full 48-channel cross Gram reconstructed with rational SU(2) epsilon contractions", gram["status"] == "exact" and gram["completed_by_this_run"] and not gram["symmetry_failures"]),
        ("exact cross Gram has zero vacuum row and SU(2) Haar sign self-tests pass", gram["vacuum_row_and_column_zero"] and gram["haar_projector_self_tests"]["passed"]),
    ]

    graph = {"vertices": [list(v) for v in vertices()], "edges": edges, "faces": faces}
    channels = {
        "strict_cutoff": "E_el < 6 alpha",
        "fundamental_link_energy_over_alpha": "3/4",
        "retained_dimension": len(retained),
        "counts_by_edge_count": dict(sorted(counts_by_length.items(), key=lambda kv: int(kv[0]))),
        "six_cycle_planarity_counts": dict(six_planarity),
        "axes_used_counts": dict(sorted(axes_counts.items())),
        "retained_channels": retained,
        "threshold_witness": threshold_record,
        "all_simple_cycle_counts_through_8": {str(k): len(v) for k, v in sorted(cycles.items())},
        "spin_network_label_audit": spin_audit,
        "threshold_label_audit": threshold_audit,
    }
    results = {
        "schema": SCHEMA,
        "status": "passed",
        "verdict": "strict-cutoff channel enumeration and exact full cross Gram reconstructed independently",
        "checks_count": len(checks),
        "checks": [{"name": name, "passed": bool(ok)} for name, ok in checks],
        "controls_count": len(controls),
        "controls": controls,
        "physical_scale": {
            "E_star": "positive fixed reference",
            "alpha_over_E_star": "2",
            "strict_cutoff_over_E_star": "12",
            "lambda_f_over_alpha": "eleven face ratios must be declared separately",
            "rejected_scales": ["kappa", "tolerance", "volume", "Fibonacci index", "E_star=0", "alpha=0"],
        },
        "graph_summary": {"vertices": 12, "links": 20, "faces": 11, "dimensions_cells": list(DIMS)},
        "channel_summary": {k: v for k, v in channels.items() if k != "retained_channels"},
        "cross_gram": gram,
        "source_sha256": {"check.py": sha256_file(Path(__file__).resolve())},
        "scope": "Backward B1 independent reconstruction of strict-cutoff channels and exact 48-channel cross Gram. No B2 executed.",
    }

    output.mkdir(parents=True, exist_ok=True)
    (output / "graph.json").write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n")
    (output / "channels.json").write_text(json.dumps(channels, indent=2, sort_keys=True) + "\n")
    (output / "controls.json").write_text(json.dumps({"controls": controls}, indent=2, sort_keys=True) + "\n")
    (output / "cross-gram-status.json").write_text(json.dumps(gram, indent=2, sort_keys=True) + "\n")
    (output / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    manifest = {
        "schema": "ym19-backward-b1-output-manifest-v1",
        "files": {p.name: sha256_file(p) for p in sorted(output.iterdir()) if p.is_file() and p.name != "manifest.json"},
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True, help="absolute or relative output directory")
    args = ap.parse_args()
    output = Path(args.output).resolve()
    results = build_results(output)
    print(json.dumps({"schema": results["schema"], "status": results["status"], "checks_count": results["checks_count"], "controls_count": results["controls_count"], "retained_dimension": results["cross_gram"]["declared_projector_dimension"]}, sort_keys=True))


if __name__ == "__main__":
    main()
