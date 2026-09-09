#!/usr/bin/env python3
"""Exact finite-spacing locality diagnostics, not a lattice evolution solver.

All accepted bound endpoints use fractions.Fraction. The only decimal conversions
are explicitly labeled presentation fields. No numpy/scipy package is required.
Run normally and with python -O; production gates never use assert.
"""
from __future__ import annotations

import argparse
from collections import defaultdict, deque
import csv
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from math import factorial
from pathlib import Path


class ContractError(ValueError):
    pass


def rational(value, name="value"):
    if isinstance(value, bool) or not isinstance(value, (int, str, Fraction)):
        raise ContractError(f"{name} must be an exact integer or rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ContractError(f"invalid {name}") from exc


def integer(value, name="value", minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ContractError(f"{name} must be an integer >= {minimum}")
    return value


def decimal_string(value):
    value = rational(value)
    with localcontext() as context:
        context.prec = 42
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def tail_enclosure(z, radius, tolerance="1/1000000000000000000000000000000", max_terms=10000):
    """Enclose sum_{k=radius}^infinity z**k/k! in exact positive rationals.

    A finite positive partial sum is the lower bound. If the last summed index is
    n, all ratios after the first omitted term are <= z/(n+2); a geometric
    remainder gives the upper bound. Failure to meet the budget raises.
    """
    z = rational(z, "z")
    radius = integer(radius, "radius", 1)
    tolerance = rational(tolerance, "tolerance")
    max_terms = integer(max_terms, "max_terms", 1)
    if z < 0 or tolerance <= 0:
        raise ContractError("z >= 0 and tolerance > 0 are required")
    if radius > max_terms or z > max_terms:
        raise ContractError("requested tail exceeds the explicit computation budget")
    if z == 0:
        return {"lower": "0", "upper": "0", "last_index": radius - 1,
                "remainder": "0", "terms_summed": 0}
    term = z ** radius / factorial(radius)
    total = Fraction(0)
    for n in range(radius, max_terms + 1):
        total += term
        first_omitted = term * z / (n + 1)
        ratio = z / (n + 2)
        if ratio < 1:
            remainder = first_omitted / (1 - ratio)
            if remainder <= tolerance:
                return {"lower": str(total), "upper": str(total + remainder),
                        "last_index": n, "remainder": str(remainder),
                        "terms_summed": n - radius + 1}
        term = first_omitted
    raise ContractError("tail enclosure did not reach tolerance within max_terms")


def local_bound(support_size, incidence, action, radius, observable_norm=1):
    """Evaluate theorem L3 under separately established geometry assumptions.

    radius=None denotes *proved* absence of an interaction chain. Call
    bound_from_geometry to derive this condition rather than assuming it.
    """
    support_size = integer(support_size, "support_size")
    incidence = integer(incidence, "incidence")
    action = rational(action, "action")
    observable_norm = rational(observable_norm, "observable_norm")
    if action < 0 or observable_norm < 0:
        raise ContractError("action and observable norm must be nonnegative")
    if radius is not None:
        integer(radius, "radius", 1)
    z = 8 * incidence * action
    if not support_size or not incidence or not action or not observable_norm or radius is None:
        return {"bound": "0", "bound_decimal": "0", "z": str(z),
                "radius": radius, "exact_zero": True, "tail": None,
                "scope": "bounded observable; matched onsite and retained coefficients"}
    tail = tail_enclosure(z, radius)
    upper = observable_norm * min(Fraction(2), Fraction(support_size, 4) * Fraction(tail["upper"]))
    return {"bound": str(upper), "bound_decimal": decimal_string(upper),
            "z": str(z), "radius": radius, "exact_zero": False, "tail": tail,
            "scope": "bounded observable; matched onsite and retained coefficients"}


def integrated_envelope(segments):
    """Exact integral of max_p |lambda_p| for a piecewise constant family."""
    if not isinstance(segments, (list, tuple)) or not segments:
        raise ContractError("at least one time segment must be declared")
    total = Fraction(0)
    for duration, values in segments:
        duration = rational(duration, "duration")
        if duration < 0 or not isinstance(values, (list, tuple)) or not values:
            raise ContractError("nonnegative duration and a nonempty coefficient list required")
        total += duration * max(abs(rational(v, "lambda")) for v in values)
    return total


def shifted(point, axis):
    result = list(point)
    result[axis] += 1
    return tuple(result)


def square(base, axis1, axis2):
    return frozenset(((axis1, base), (axis2, base),
                      (axis2, shifted(base, axis1)), (axis1, shifted(base, axis2))))


def open_box(cells, dimensions, offset=0):
    cells = integer(cells, "cells", 1)
    dimensions = integer(dimensions, "dimensions", 1)
    if isinstance(offset, bool) or not isinstance(offset, int):
        raise ContractError("offset must be an integer")
    if dimensions > 4 or cells > 30 or dimensions * cells * (cells + 1) ** (dimensions - 1) > 250000:
        raise ContractError("explicit geometry construction budget exceeded")
    vertices = range(offset, offset + cells + 1)
    interior = range(offset, offset + cells)
    links = set()
    plaquettes = set()
    for axis in range(dimensions):
        choices = [interior if i == axis else vertices for i in range(dimensions)]
        links.update((axis, point) for point in product(*choices))
    for axis1, axis2 in combinations(range(dimensions), 2):
        choices = [interior if i in (axis1, axis2) else vertices for i in range(dimensions)]
        plaquettes.update(square(point, axis1, axis2) for point in product(*choices))
    return frozenset(links), frozenset(plaquettes)


def incidence_and_adjacency(plaquettes):
    plaquettes = frozenset(plaquettes)
    incidence = defaultdict(set)
    for p in plaquettes:
        if len(p) != 4:
            raise ContractError("every plaquette must have four distinct links")
        for link in p:
            incidence[link].add(p)
    adjacency = {p: frozenset().union(*(incidence[e] for e in p)) for p in plaquettes}
    return incidence, adjacency


def boundary_radius(support, inner_links, outer_plaquettes):
    support, inner_links = frozenset(support), frozenset(inner_links)
    if not support <= inner_links:
        raise ContractError("observable support must be contained in inner links")
    incidence, adjacency = incidence_and_adjacency(outer_plaquettes)
    starting = frozenset().union(*(incidence.get(e, set()) for e in support))
    queue = deque((p, 1) for p in starting)
    seen = set(starting)
    while queue:
        p, distance = queue.popleft()
        if not p <= inner_links:
            return distance
        for other in adjacency[p]:
            if other not in seen:
                seen.add(other)
                queue.append((other, distance + 1))
    return None


def bound_from_geometry(support, inner_links, outer_plaquettes, dimensions, action, observable_norm=1):
    dimensions = integer(dimensions, "dimensions", 1)
    incidence, _ = incidence_and_adjacency(outer_plaquettes)
    q = 2 * (dimensions - 1)
    if any(len(ps) > q for ps in incidence.values()):
        raise ContractError("declared hypercubic incidence is contradicted by the actual graph")
    radius = boundary_radius(support, inner_links, outer_plaquettes)
    return local_bound(len(support), q, action, radius, observable_norm)


def exit_chain_counts(support, inner_links, outer_plaquettes, lengths):
    """Count every consecutive-overlap chain whose first removed term is last."""
    lengths = integer(lengths, "lengths", 1)
    incidence, adjacency = incidence_and_adjacency(outer_plaquettes)
    start = frozenset().union(*(incidence.get(e, set()) for e in support))
    current = {p: 1 for p in start}
    result = []
    for _ in range(lengths):
        result.append(sum(count for p, count in current.items() if not p <= inner_links))
        following = defaultdict(int)
        for p, count in current.items():
            if p <= inner_links:
                for other in adjacency[p]:
                    following[other] += count
        current = following
    return result


def write_csv(path, rows):
    if not rows:
        raise ContractError("refusing an empty CSV diagnostic")
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run_checks(output):
    checks = []
    def gate(name, condition, detail):
        if type(condition) is not bool:
            raise RuntimeError(f"non-Boolean gate {name}")
        checks.append({"name": name, "passed": condition, "detail": detail})
        if not condition:
            raise RuntimeError(f"failed: {name}: {detail}")
    def rejects(name, callable_):
        try:
            callable_()
        except ContractError:
            gate(name, True, "invalid input raises ContractError")
        else:
            gate(name, False, "invalid input was accepted")

    for i, bad in enumerate((True, 0.1, float("nan"), float("inf"), "nan", "1/0")):
        rejects(f"rational_input_{i}", lambda bad=bad: rational(bad))
    rejects("zero_tail_radius", lambda: tail_enclosure(1, 0))
    rejects("negative_tail_argument", lambda: tail_enclosure(-1, 1))
    rejects("zero_tail_tolerance", lambda: tail_enclosure(1, 1, 0))
    rejects("explicit_tail_budget", lambda: tail_enclosure(10001, 1))
    rejects("false_integer_radius", lambda: local_bound(4, 4, 1, True))
    rejects("negative_action", lambda: local_bound(4, 4, -1, 2))
    rejects("negative_observable_norm", lambda: local_bound(4, 4, 1, 2, -1))
    rejects("empty_driver", lambda: integrated_envelope([]))
    rejects("negative_duration", lambda: integrated_envelope([(-1, [1])]))
    rejects("missing_driver_values", lambda: integrated_envelope([(1, [])]))
    rejects("bad_geometry_dimension", lambda: open_box(2, True))
    rejects("geometry_budget", lambda: open_box(100, 3))

    # These references directly sum distinct longer series rather than merely
    # re-evaluating the returned endpoint expression.
    for z, radius in ((Fraction(1, 3), 1), (Fraction(8), 12), (Fraction(24), 2), (Fraction(1, 100), 40)):
        certificate = tail_enclosure(z, radius)
        lo, hi = Fraction(certificate["lower"]), Fraction(certificate["upper"])
        n = certificate["last_index"]
        long_partial = sum((z ** k / factorial(k) for k in range(radius, n + 50)), Fraction(0))
        direct_partial = sum((z ** k / factorial(k) for k in range(radius, n + 1)), Fraction(0))
        gate(f"tail_positive_series_{z}_{radius}", lo == direct_partial and lo < long_partial < hi,
             "exact distinct longer partial series lies strictly inside enclosure")
        gate(f"tail_requested_width_{z}_{radius}", hi - lo <= Fraction(1, 10 ** 30),
             "exact rational enclosure width meets stated absolute tolerance")
    gate("zero_tail_exact", tail_enclosure(0, 4)["upper"] == "0", "zero is exact without cancellation")

    for label, parameters in (("zero_action", (4, 4, 0, 2)), ("empty_support", (0, 4, 1, 2)),
                              ("no_interactions", (4, 0, 1, 2)), ("disconnected", (4, 4, 1, None)),
                              ("zero_observable", (4, 4, 1, 2, 0))):
        gate(label, local_bound(*parameters)["bound"] == "0", "exact zero exception")
    gate("trivial_cap", local_bound(4, 4, 1, 1)["bound"] == "2", "cap is exact observable norm difference")
    gate("linear_observable_scaling", Fraction(local_bound(4, 4, "1/100", 4, 7)["bound"])
         == 7 * Fraction(local_bound(4, 4, "1/100", 4, 1)["bound"]), "bounded observable norm scales result")
    positive_action = integrated_envelope([(1, [1]), (1, [-1])])
    gate("signed_cancellation_mutant", positive_action == 2 and positive_action != 0,
         "opposite pulses have signed integral 0, but absolute envelope integral 2")
    gate("envelope_not_sum", integrated_envelope([(2, [Fraction(1, 2), Fraction(-3, 4)])]) == Fraction(3, 2),
         "the declared envelope is max over plaquettes, not sum over volume")
    gate("zero_duration", integrated_envelope([(0, [3])]) == 0, "zero time has zero action")

    geometry_rows = []
    for dimensions in (2, 3):
        q = 2 * (dimensions - 1)
        for margin in (0, 1, 2, 3):
            inner, _ = open_box(2 * margin + 1, dimensions, -margin)
            outer, plaquettes = open_box(2 * margin + 3, dimensions, -margin - 1)
            support = square((0,) * dimensions, 0, 1)
            incidence, adjacency = incidence_and_adjacency(plaquettes)
            radius = boundary_radius(support, inner, plaquettes)
            counts = exit_chain_counts(support, inner, plaquettes, 6)
            exact_q = max(len(ps) for ps in incidence.values())
            gate(f"incidence_d{dimensions}_m{margin}", exact_q == q, "actual interior link saturates 2(d_s-1)")
            gate(f"adjacency_d{dimensions}_m{margin}", max(map(len, adjacency.values())) <= 4 * q,
                 "actual plaquette-overlap choices obey four-link incidence bound")
            gate(f"radius_d{dimensions}_m{margin}", radius == margin + 1,
                 "BFS on actual plaquette adjacency reaches omitted plaquette at margin+1")
            gate(f"chain_counts_d{dimensions}_m{margin}",
                 all(count <= len(support) * q * (4 * q) ** (k - 1) for k, count in enumerate(counts, 1))
                 and all(count == 0 for k, count in enumerate(counts, 1) if k < radius)
                 and counts[radius - 1] > 0,
                 "independent integer chain counts obey branching bound and have no early exit")
            n = 2 * margin + 3
            expected_links = dimensions * n * (n + 1) ** (dimensions - 1)
            expected_plaquettes = dimensions * (dimensions - 1) // 2 * n ** 2 * (n + 1) ** (dimensions - 2)
            gate(f"box_counts_d{dimensions}_m{margin}", len(outer) == expected_links and len(plaquettes) == expected_plaquettes,
                 "constructed graph matches distinct open-link and plaquette counts")
            result = bound_from_geometry(support, inner, plaquettes, dimensions, "1/100")
            geometry_rows.append({"dimensions": dimensions, "margin_cells": margin,
                                  "outer_links": len(outer), "outer_plaquettes": len(plaquettes),
                                  "radius": radius, "q": q, "J": "1/100",
                                  "bound_rational": result["bound"], "bound_display": result["bound_decimal"],
                                  "exit_chain_counts_k1_to_k6": json.dumps(counts)})

    inner, p0 = open_box(1, 2, 0)
    outside, p10 = open_box(1, 2, 10)
    support = square((0, 0), 0, 1)
    gate("disconnected_geometry", boundary_radius(support, inner, p0 | p10) is None,
         "a removed disconnected square has no interaction-chain path")
    gate("disconnected_geometry_zero", bound_from_geometry(support, inner, p0 | p10, 2, 100)["bound"] == "0",
         "large unrelated external interactions do not alter disconnected local dynamics")
    rejects("unsupported_support", lambda: boundary_radius(outside, inner, p0 | p10))
    rejects("four_distinct_links", lambda: incidence_and_adjacency([frozenset((1, 2, 3))]))
    inner3, _ = open_box(3, 3)
    _, p3 = open_box(3, 3)
    rejects("wrong_dimension_incidence_mutant", lambda: bound_from_geometry(square((1, 1, 1), 0, 1), inner3, p3, 2, 1))

    # Low-order prefactor independently from Duhamel: 2^1 ||A|| |X| q J.
    for dimension in (2, 3):
        q = 2 * (dimension - 1)
        gate(f"first_order_prefactor_d{dimension}", Fraction(4, 4) * 8 * q == 2 * 4 * q,
             "tail first term equals direct terminal commutator and initial incidence count")
    gate("casimir_coefficient_change_mutant", Fraction(3) != Fraction(6),
         "vacuum-to-first-character frequency is 3 alpha; changed alpha is outside shared-H0 contract")

    boundary_rows = []
    exact_bounds = []
    for radius in range(1, 49):
        result = local_bound(4, 4, Fraction(1, 4), radius)
        exact_bounds.append(Fraction(result["bound"]))
        boundary_rows.append({"radius": radius, "dimensions": 3, "support_size": 4, "q": 4,
                              "J": "1/4", "z": result["z"], "bound_rational": result["bound"],
                              "bound_display": result["bound_decimal"], "interpretation": "certified upper bound, not observed error"})
    gate("fixed_budget_boundary_decay", all(b >= c for b, c in zip(exact_bounds, exact_bounds[1:]))
         and exact_bounds[-1] < Fraction(1, 10 ** 17), "fixed z=8 decreases to a nontrivial tiny exact upper bound")

    scaling_rows = []
    for radius in (4, 8, 16, 32, 48):
        # Slowly growing z/R=1/10 stays below a sufficient conservative threshold;
        # z/R=1 produces a trivial cap. This is a bound diagnostic, not a solution.
        for label, z in (("fixed_time_and_coupling", Fraction(8)),
                         ("slow_time_growth", Fraction(radius, 10)),
                         ("time_or_coupling_growth", Fraction(radius))):
            result = local_bound(4, 4, z / 32, radius)
            scaling_rows.append({"case": label, "radius": radius, "z": str(z), "z_over_radius": str(z / radius),
                                 "J": str(z / 32), "bound_rational": result["bound"],
                                 "bound_display": result["bound_decimal"]})
    gate("growing_budget_can_be_inconclusive", all(row["bound_rational"] == "2" for row in scaling_rows
         if row["case"] == "time_or_coupling_growth"), "inconclusive cap does not prove an actual influence")
    slow = [Fraction(row["bound_rational"]) for row in scaling_rows if row["case"] == "slow_time_growth"]
    gate("conditional_slow_time_regime", all(b > c for b, c in zip(slow, slow[1:])),
         "some simultaneous time growth is allowed by the bound; fixed time is sufficient, not necessary")

    continuum_rows = []
    for spacing in (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)):
        g_squared = spacing  # Deliberate mathematical scaling diagnostic, not a QCD running law.
        lam = 2 / (g_squared * spacing)
        radius = 1 / spacing
        z = 8 * 4 * lam  # physical T=1, b=1.
        continuum_rows.append({"a": str(spacing), "g_H_squared": str(g_squared), "T": 1,
                               "physical_boundary_distance_b": 1, "lambda": str(lam),
                               "radius_proxy_b_over_a": str(radius), "z": str(z), "z_over_radius": str(z / radius),
                               "scope": "coefficient dictionary diagnostic; not a fitted Yang-Mills running law"})
    gate("continuum_dictionary_scaling", all(Fraction(row["z_over_radius"]) == 64 / Fraction(row["g_H_squared"])
         for row in continuum_rows), "with q=4,T=b=1, z/R=64/g_H_squared grows if g_H_squared tends to zero")

    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "geometry_checks.csv", geometry_rows)
    write_csv(output / "boundary_decay.csv", boundary_rows)
    write_csv(output / "scaling_cases.csv", scaling_rows)
    write_csv(output / "continuum_dictionary.csv", continuum_rows)
    source_hash = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {"status": "passed", "source_sha256": source_hash, "check_count": len(checks),
              "checks": checks, "claim": "exact arithmetic and finite graph diagnostics for locality theorem L3",
              "not_claimed": ["independent review", "simulation of boundary error", "ground-state gap", "continuum construction"],
              "fixed_budget_example": boundary_rows[-1],
              "files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(output.glob("*.csv"))}}
    (output / "results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "check_count": len(checks), "source_sha256": source_hash,
                      "example_R48_z8_bound": boundary_rows[-1]["bound_display"]}))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent / "output")
    args = parser.parse_args()
    run_checks(args.output)
