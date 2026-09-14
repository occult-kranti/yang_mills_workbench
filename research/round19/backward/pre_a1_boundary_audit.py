#!/usr/bin/env python3
"""Independent pre-contract checks for Round19 Goal A boundary restrictions.

This script deliberately does not import Round18 producer/backward modules.  It
models the literal restriction of one nonnegative-orthant infinite coefficient
assignment to finite open boxes and checks the boundary cluster taxonomy and
remaining-face unused-link witnesses.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
from typing import Iterable

SignWord = tuple[tuple[tuple[int, int, int, int], int], ...]
Face = tuple[int, int, int, int, int]  # (axis_a, axis_b, x, y, z), axis_a<axis_b
Edge = tuple[int, int, int, int]       # (axis, x, y, z)


def S(m: int) -> Fraction:
    if m < 0:
        raise ValueError("negative geometric length")
    return sum(Fraction(1, 2**k) for k in range(m))


def G(step: int, count: int) -> Fraction:
    return sum(Fraction(1, 2 ** (step * k)) for k in range(count))


def vertices(n: int) -> set[tuple[int, int, int]]:
    return {(x, y, z) for x in range(n) for y in range(n) for z in range(n)}


def edges(n: int) -> set[Edge]:
    out: set[Edge] = set()
    for axis in range(3):
        for x in range(n):
            for y in range(n):
                for z in range(n):
                    coords = [x, y, z]
                    if coords[axis] + 1 < n:
                        out.add((axis, x, y, z))
    return out


def faces(n: int) -> list[Face]:
    out: list[Face] = []
    for a, b in [(0, 1), (0, 2), (1, 2)]:
        for x in range(n):
            for y in range(n):
                for z in range(n):
                    coords = [x, y, z]
                    if coords[a] + 1 < n and coords[b] + 1 < n:
                        out.append((a, b, x, y, z))
    return out


def face_word(face: Face) -> SignWord:
    a, b, x, y, z = face
    c = [x, y, z]
    cb = c.copy(); cb[b] += 1
    ca = c.copy(); ca[a] += 1
    return (
        ((a, *c), 1),
        ((b, *ca), 1),
        ((a, *cb), -1),
        ((b, *c), -1),
    )


def weight(face: Face) -> Fraction:
    _, _, x, y, z = face
    return Fraction(1, 24 * (2 ** (x + y + z)))


def strip_role(face: Face) -> str | None:
    a, b, x, y, z = face
    if (a, b) != (0, 1):
        return None
    if y % 2:
        return None
    r = x % 4
    if r == 0:
        return "left"
    if r == 1:
        return "middle"
    if r == 2:
        return "right"
    return None


def selected_faces(n: int) -> dict[Face, str]:
    return {f: role for f in faces(n) if (role := strip_role(f)) is not None}


def cluster_id(face: Face) -> tuple[int, int, int]:
    a, b, x, y, z = face
    assert (a, b) == (0, 1) and y % 2 == 0 and x % 4 in (0, 1, 2)
    return (x // 4, y // 2, z)


def selected_edges(n: int) -> set[Edge]:
    used: set[Edge] = set()
    for f in selected_faces(n):
        for edge, _sgn in face_word(f):
            used.add(edge)
    return used


def unused_witness(face: Face, used: set[Edge]) -> tuple[Edge, str] | None:
    a, b, x, y, z = face
    word = [edge for edge, _ in face_word(face)]
    if (a, b) in [(0, 2), (1, 2)]:
        for e in word:
            if e[0] == 2 and e not in used:
                return e, "unused z-link"
    if (a, b) == (0, 1) and y % 2 == 1:
        for e in word:
            if e[0] == 1 and e[2] == y and e not in used:
                return e, "unused odd-y link"
    if (a, b) == (0, 1) and y % 2 == 0 and x % 4 == 3:
        for e in word:
            if e[0] == 0 and e[1] == x and e not in used:
                return e, "unused gap x-link"
    for e in word:
        if e not in used:
            return e, "fallback unused word link"
    return None


def boundary_s(n: int) -> Fraction:
    r = n % 4
    if r == 2:
        return Fraction(1)
    if r == 3:
        return Fraction(3, 2)
    return Fraction(0)


def selected_weight_formula(n: int) -> Fraction:
    m = n // 4
    k = n // 2
    return Fraction(1, 24) * S(n) * G(2, k) * (Fraction(7, 4) * G(4, m) + boundary_s(n) * Fraction(1, 2 ** (4 * m)))


def total_weight_formula(n: int) -> Fraction:
    return S(n - 1) * S(n - 1) * S(n) / 8


def cluster_type_counts(n: int) -> dict[str, int]:
    clusters: dict[tuple[int, int, int], list[str]] = {}
    for f, role in selected_faces(n).items():
        clusters.setdefault(cluster_id(f), []).append(role)
    labels = {("left",): "one-face-left", ("left", "middle"): "two-face-left-middle", ("left", "middle", "right"): "three-face-strip"}
    counts = {label: 0 for label in labels.values()}
    bad = []
    for roles in clusters.values():
        key = tuple(sorted(roles, key={"left": 0, "middle": 1, "right": 2}.__getitem__))
        if key not in labels:
            bad.append(key)
        else:
            counts[labels[key]] += 1
    if bad:
        raise AssertionError(f"unexpected cluster fragments {bad}")
    return counts


def analyze(n: int) -> dict:
    if isinstance(n, bool) or n < 2:
        raise ValueError("n must be an integer >=2")
    fs = faces(n)
    sel = selected_faces(n)
    used = selected_edges(n)
    missing = []
    witness_cases: dict[str, int] = {}
    for f in fs:
        if f in sel:
            continue
        got = unused_witness(f, used)
        if got is None:
            missing.append(f)
        else:
            _edge, case = got
            witness_cases[case] = witness_cases.get(case, 0) + 1
    selected_enum = sum(weight(f) for f in sel)
    total_enum = sum(weight(f) for f in fs)
    if selected_enum != selected_weight_formula(n):
        raise AssertionError((n, selected_enum, selected_weight_formula(n)))
    if total_enum != total_weight_formula(n):
        raise AssertionError((n, total_enum, total_weight_formula(n)))
    if missing:
        raise AssertionError((n, missing[:5]))
    counts = cluster_type_counts(n)
    return {
        "n": n,
        "vertices": n**3,
        "links": len(edges(n)),
        "faces": len(fs),
        "selected_faces": len(sel),
        "cluster_counts": counts,
        "selected_weight": str(selected_enum),
        "remaining_weight": str(total_enum - selected_enum),
        "remaining_weight_le_one": total_enum - selected_enum <= 1,
        "witness_cases": witness_cases,
        "cluster_gap_bounds_alpha_units": {
            "one_face_left": "free reference 3/4 - |lambda_L|/alpha >= 1/4",
            "two_face_left_middle": "free reference 3/4 - (|lambda_L|+|mu|)/alpha >= 1/8",
            "three_face_strip": "Round18 A1 dressed bridge >= 1/8",
        },
        "remainder_gap_at_tau_1_over_64": "1/8 - W_n/64 >= 7/64 since W_n<=1",
    }


def main() -> None:
    out = {
        "status": "preliminary-pass",
        "scope": "finite restrictions of one fixed nonnegative-orthant infinite coefficient assignment; no thermodynamic spectral passage certified",
        "fixed_coefficients": {
            "alpha": "one common physical electric coefficient, alpha>=alpha_min>0",
            "strip_left_right": "|lambda|<=alpha/2 on infinite xy strip offsets 0 and 2",
            "strip_middle": "|mu|<=alpha/8 on infinite xy strip offset 1",
            "remainder": "nu_f=alpha*tau*2^(-x-y-z)/24 on faces outside infinite strips",
        },
        "samples": [analyze(n) for n in range(2, 13)],
        "falsifiers": [
            "vary alpha_N or local magnetic coefficients between boxes without a declared single assignment/local limit",
            "omit n mod 4 clipped cluster types or classify their fitted faces as remainders",
            "claim the two-face boundary estimate while |lambda_L|+|mu|>5alpha/8",
            "use a dressed-zero expectation where the chosen boundary reference has no actual free Haar link",
            "promote finite uniform lower bounds to an infinite-volume Hamiltonian gap without state/dynamics/spectral convergence",
            "replace the summable dyadic remainder by a homogeneous nondecaying remainder while keeping the same norm budget",
        ],
    }
    dest = Path(__file__).with_name("pre_a1_boundary_audit.json")
    dest.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"status": out["status"], "samples": len(out["samples"]), "dest": str(dest)}, indent=2))


if __name__ == "__main__":
    main()
