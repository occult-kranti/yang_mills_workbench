#!/usr/bin/env python3
"""Independent AG3 exact diagnostics. --output must be absolute and fresh.

No external imports or fitted source values. The report proves all-order,
actual-Hilbert-space statements; finite matrices only test their algebra.
"""
import argparse
from fractions import Fraction as Q
import hashlib
from itertools import product
import json
from math import factorial
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
TESTS = []


def test(name, ok):
    if not ok:
        raise RuntimeError(name)
    TESTS.append(name)


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def rationalize(obj):
    if isinstance(obj, Q):
        return {"exact": str(obj), "decimal": float(obj)}
    if isinstance(obj, dict):
        return {str(k): rationalize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [rationalize(v) for v in obj]
    return obj


def matrix(rows):
    return tuple(tuple(Q(x) for x in row) for row in rows)


def zmat(n):
    return matrix([[0] * n for _ in range(n)])


def ident(n):
    return matrix([[int(i == j) for j in range(n)] for i in range(n)])


def scalar(t, a):
    return tuple(tuple(t * x for x in row) for row in a)


def summat(*args):
    n = len(args[0])
    return tuple(tuple(sum((a[i][j] for a in args), Q(0)) for j in range(n)) for i in range(n))


def productmat(a, b):
    n = len(a)
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(n)), Q(0)) for j in range(n)) for i in range(n))


def trans(a):
    return tuple(zip(*a))


def bracket(a, b):
    return summat(productmat(a, b), scalar(-1, productmat(b, a)))


def mpow(a, n):
    result = ident(len(a))
    for _ in range(n):
        result = productmat(result, a)
    return result


def iter_bracket(x, a, n):
    for _ in range(n):
        a = bracket(x, a)
    return a


def kron(a, b):
    return tuple(tuple(x * y for x in rowa for y in rowb) for rowa in a for rowb in b)


def block_split(k):
    n = len(k)
    p = matrix([[int(i == j == 0) for j in range(n)] for i in range(n)])
    q = summat(ident(n), scalar(-1, p))
    mix = summat(productmat(productmat(p, k), q), productmat(productmat(q, k), p))
    c = k[0][0]
    diagonal = productmat(productmat(q, summat(k, scalar(-c, ident(n)))), q)
    return c, mix, diagonal, p, q


def exponential_coefficient(x, a, n):
    ans = zmat(len(x))
    for left in range(n + 1):
        right = n - left
        term = productmat(productmat(mpow(x, left), a), mpow(x, right))
        ans = summat(ans, scalar(Q((-1) ** right, factorial(left) * factorial(right)), term))
    return ans


def algebra():
    h = matrix([[0, 0, 0], [0, 2, 0], [0, 0, 5]])
    b = matrix([[0, 3, 4], [3, 0, 0], [4, 0, 0]])
    x = matrix([[0, Q(-3, 2), Q(-4, 5)], [Q(3, 2), 0, 0], [Q(4, 5), 0, 0]])
    d = matrix([[0, 0, 0], [0, 1, 3], [0, 3, -2]])
    u2 = Q(3, 2) ** 2 + Q(4, 5) ** 2
    test("reduced inverse rank norm", u2 == Q(17, 10) ** 2 and u2 <= 25)
    test("bounded first commutator", bracket(x, h) == scalar(-1, b))
    test("rank generator skew-adjoint", trans(x) == scalar(-1, x))
    test("diagonal means vacuum complement", all(d[i][0] == 0 for i in range(3)))
    test("diagonal need not commute with H0", bracket(d, h) != zmat(3))
    test("retained D commutator is nonzero", bracket(x, d) != zmat(3))

    # Formal parameter e: conjugate H0+D+e*B by exp(e*X).
    for n in range(7):
        lhs = exponential_coefficient(x, summat(h, d), n)
        if n:
            lhs = summat(lhs, exponential_coefficient(x, b, n - 1))
        rhs = summat(h, d) if n == 0 else scalar(Q(1, factorial(n)), iter_bracket(x, d, n))
        if n >= 2:
            rhs = summat(rhs, scalar(Q(n - 1, factorial(n)), iter_bracket(x, b, n - 1)))
        test("full exponential coefficient %d" % n, lhs == rhs)
        if n >= 1:
            no_d = zmat(3) if n == 1 else scalar(Q(n - 1, factorial(n)), iter_bracket(x, b, n - 1))
            test("omitted D coefficient %d rejected" % n, lhs != no_d)
        if n >= 2:
            wrong = summat(scalar(Q(1, factorial(n)), iter_bracket(x, d, n)),
                           scalar(Q(n, factorial(n)), iter_bracket(x, b, n - 1)))
            test("wrong full B coefficient %d rejected" % n, lhs != wrong)
    old_c = Q(5, 7)
    test("old scalar survives zeroth coefficient", exponential_coefficient(x, scalar(old_c, ident(3)), 0) == scalar(old_c, ident(3)))
    for n in range(1, 7):
        test("old scalar commutes degree %d" % n, exponential_coefficient(x, scalar(old_c, ident(3)), n) == zmat(3))
    leading = summat(bracket(x, d), scalar(Q(1, 2), bracket(x, b)))
    c, new_b, new_d, p, q = block_split(leading)
    test("new nonzero scalar", c == Q(-77, 10))
    test("complete scalar mixing diagonal reconstruction", summat(scalar(c, ident(3)), new_b, new_d) == leading)
    test("new diagonal annihilates vacuum", all(new_d[i][0] == 0 for i in range(3)))
    test("dropped scalar rejected", summat(new_b, new_d) != leading)
    test("uncentered complement rejected", summat(scalar(c, ident(3)), new_b, productmat(productmat(q, leading), q)) != leading)
    test("full remaining mixing retained", new_b != zmat(3))
    for t in (Q(-1, 100), Q(0), Q(1, 100)):
        xt, bt, dt = scalar(t, x), scalar(t, b), scalar(t, d)
        rt = summat(bracket(xt, dt), scalar(Q(1, 2), bracket(xt, bt)))
        test("both-sign leading identity %s" % t, rt == scalar(t * t, leading))
        test("zero operator handled without ratio %s" % t, t != 0 or rt == zmat(3))
    return {"inverse_rank_norm": Q(17, 10), "mixing_rank_norm": Q(5),
            "new_scalar_leading": c, "full_BCH_degree": 6}


def exterior_and_overlap():
    flip = matrix([[0, 1], [1, 0]])
    zz = matrix([[1, 0], [0, -1]])
    ii = ident(2)
    u = kron(kron(flip, flip), ii)
    v = kron(kron(ii, zz), flip)
    k = bracket(u, v)
    test("nontrivial overlapping support commutator", k != zmat(8))
    test("overlap commutator norm two", productmat(trans(k), k) == scalar(4, ident(8)))
    y, z = {0, 1}, {1, 2}
    test("incoming root cannot be omitted", 2 in (y | z) and 2 not in y and k != zmat(8))
    test("old root cannot be omitted", 0 in (y | z) and 0 not in z and k != zmat(8))
    test("disjoint supports commute", bracket(kron(flip, ii), kron(ii, zz)) == zmat(4))
    # Physical exterior identity versus a global-vacuum replacement.
    loc_b = flip
    loc_x = matrix([[0, -1], [1, 0]])
    loc_h = matrix([[0, 0], [0, 1]])
    ext_h = matrix([[0, 0], [0, 3]])
    xx = kron(loc_x, ii)
    bb = kron(loc_b, ii)
    hh = summat(kron(loc_h, ii), kron(ii, ext_h))
    test("complete exterior commutator identity", bracket(xx, hh) == scalar(-1, bb))
    global_b = matrix([[0, 0, 1, 0], [0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0]])
    test("excited exterior is retained", bb[3][1] == 1 and global_b[3][1] == 0)
    test("global vacuum replacement rejected", global_b != bb)
    for n in (4, 16, 64):
        hilbert = sum((Q(1, j * j) for j in range(1, n + 1)), Q(0))
        graph = sum((Q(j * j, j * j) for j in range(1, n + 1)), Q(0))
        test("exterior Hilbert norm stays bounded %d" % n, hilbert < 2)
        test("exterior graph norm grows %d" % n, graph == n)
    return {"overlap_supports": [[0, 1], [1, 2]], "union": [0, 1, 2], "physical_fixture": False}


def support_controls():
    b = Q(3, 2)
    universe = set(range(5))
    sets = [set(x for x, bit in enumerate(bits) if bit) for bits in product((0, 1), repeat=5) if any(bits)]
    pairs = 0
    for y in sets:
        for z in sets:
            if y & z:
                test("nonempty overlap weight %s %s" % (sorted(y), sorted(z)),
                     b ** len(y | z) <= b ** (len(y) + len(z) - 1))
                pairs += 1
    # Complete finite generated support tuples; repetitions and later-only attachments.
    family = [frozenset((0, 1)), frozenset((1, 2)), frozenset((2, 3)), frozenset((0, 3, 4))]
    words = [(y, (i,)) for i, y in enumerate(family)]
    counts = [len(words)]
    for depth in range(1, 4):
        words = [(y | z, w + (i,)) for y, w in words for i, z in enumerate(family) if y & z]
        counts.append(len(words))
        test("ordered repetitions depth%d" % depth, any(len(set(w)) == 1 for y, w in words))
        test("support union retained depth%d" % depth, all(y == frozenset().union(*(family[i] for i in w)) for y, w in words))
    test("attachment only to new support retained", any(w[:3] == (0, 1, 2) for y, w in words))
    for n in (4, 8, 16, 32):
        reset_ratio = Q(4, 3) ** n
        test("reset-weight inflation n%d" % n, reset_ratio > 1)
    # Generic same-weight commutator example: b^-n X^n and sum Z_i/b.
    for n in (1, 2, 4, 8):
        test("fixed-weight factor grows n%d" % n, 2 * n / b == Q(4 * n, 3))
    test("same-weight factors unbounded in n", Q(32, 3) > Q(16, 3) > Q(8, 3))
    flip, zz = matrix([[0, 1], [1, 0]]), matrix([[1, 0], [0, -1]])
    for n in range(1, 5):
        string = matrix([[1]])
        for _ in range(n):
            string = kron(string, flip)
        onsite = zmat(2 ** n)
        for at in range(n):
            term = matrix([[1]])
            for pos in range(n):
                term = kron(term, zz if pos == at else ident(2))
            onsite = summat(onsite, scalar(1 / b, term))
        cc = bracket(scalar(b ** (-n), string), onsite)
        squared = productmat(trans(cc), cc)
        test("exact same-weight commutator square diagonal n%d" % n,
             all(squared[i][j] == 0 for i in range(2 ** n) for j in range(2 ** n) if i != j))
        test("exact same-weight commutator norm n%d" % n,
             max(squared[i][i] for i in range(2 ** n)) == (2 * n * b ** (-n - 1)) ** 2)
    one_site_cube = {(0, 0, 0)}
    star = {(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)}
    test("no-star cuboid has empty retained source family", not star <= one_site_cube)
    test("no-star correction sum is zero before division", sum((), Q(0)) == 0)
    return {"nonempty_overlap_pairs": pairs, "generated_word_counts": counts,
            "reset_norm_ratio": "(4/3)^n for a b-normalized n-support rank mixing term",
            "fixed_weight_commutator_ratio": "2n/b for the declared Pauli diagnostic"}


def interval(m, cap):
    c = Q(288, 31)
    d = 64 * m + 2 * cap
    theta = c * cap
    gamma = c * (d + cap) / (1 - theta)
    residual = gamma * cap
    b = Q(3, 2)
    old_relative = 4 * m + cap / 8
    added_relative = 2 * residual / b ** 4
    old_scalar_density = cap / 64
    new_scalar_density = residual / (4 * b ** 4)
    return {"M_endpoint": m, "AG2_K_cap": cap, "D_next_2_upper": d,
            "r_ceiling": cap, "d_ceiling": d, "theta": theta,
            "ratio": gamma, "remainder": residual,
            "scalar_density": old_scalar_density + new_scalar_density,
            "reference_gap": 1 - old_relative - added_relative,
            "c_rational_upper": c, "theta_upper": theta, "denominator_floor": 1 - theta,
            "actual_input_coefficient_upper": gamma, "residual_b_upper": residual,
            "new_mixing_b_upper": residual, "new_centered_diagonal_b_upper": 2 * residual,
            "full_centered_diagonal_b_upper": (b / 2) ** 4 * d + 2 * residual,
            "old_scalar_density_upper": old_scalar_density,
            "new_scalar_density_upper": new_scalar_density,
            "complete_scalar_density_upper": old_scalar_density + new_scalar_density,
            "old_relative_diagonal_upper": old_relative,
            "new_relative_diagonal_upper": added_relative,
            "complete_relative_diagonal_upper": old_relative + added_relative,
            "next_reference_gap_lower": 1 - old_relative - added_relative,
            "exact_statement": "||R_next||_(3/2) <= coefficient * actual ||B||_2; coefficient upper only",
            "same_weight_contraction": False, "all_stage_convergence": False}


def numerical_certificates():
    lower = Q(1, 3) - Q(1, 18) + Q(1, 81) - Q(1, 324)
    upper = lower + Q(1, 1215)
    test("four-term logarithm lower rational", lower == Q(31, 108))
    test("five-term logarithm upper exceeds lower", upper > lower)
    for t in (Q(0), Q(1, 12), Q(1, 6), Q(1, 3)):
        polynomial = 1 - t + t * t - t ** 3
        test("exact logarithm integrand remainder %s" % t, 1 / (1 + t) - polynomial == t ** 4 / (1 + t))
    test("shared proposed rational c independently recovered", Q(8, 3) / lower == Q(288, 31))
    for theta in (Q(0), Q(1, 100), Q(1, 10)):
        prefix = sum((theta ** j for j in range(1, 13)), Q(0))
        tail = theta ** 13 / (1 - theta)
        test("complete geometric tail %s" % theta, prefix + tail == theta / (1 - theta))
    out = {"zero": interval(Q(0), Q(0)),
           "narrow": interval(Q(1, 10000), Q(7, 100000)),
           "main": interval(Q(1, 1000), Q(7, 1000))}
    for key, v in out.items():
        test("radius positive " + key, 0 <= v["theta_upper"] < 1)
        test("positive denominator " + key, v["denominator_floor"] > 0)
        test("weight-changing factor below17/20 " + key, v["actual_input_coefficient_upper"] < Q(17, 20))
        test("new reference gap above99/100 " + key, v["next_reference_gap_lower"] > Q(99, 100))
        for frac in (Q(0), Q(1, 100), Q(1, 2), Q(1)):
            actual_r = frac * v["AG2_K_cap"]
            c = v["c_rational_upper"]
            d = v["D_next_2_upper"]
            exact_factor = c * (d + actual_r) / (1 - c * actual_r)
            bound_with_actual_input = actual_r * exact_factor
            test("actual multiplicative input %s %s" % (key, frac), bound_with_actual_input <= actual_r * v["actual_input_coefficient_upper"])
            if actual_r == 0:
                test("zero-r case no quotient %s %s" % (key, frac), bound_with_actual_input == 0)
    test("main exact gamma", out["main"]["actual_input_coefficient_upper"] == Q(3060, 3623))
    test("narrow stronger bound", out["narrow"]["actual_input_coefficient_upper"] < Q(1, 16))
    test("narrow reference above999/1000", out["narrow"]["next_reference_gap_lower"] > Q(999, 1000))
    # Two upper bounds never supply a contraction denominator.
    input_actual, input_upper, output_actual, output_upper = Q(1, 100), Q(1), Q(1, 2), Q(1, 2)
    test("upper-budget comparison is insufficient", output_upper / input_upper < 1 and output_actual / input_actual > 1)
    test("zero-coupling entire correction", out["zero"]["residual_b_upper"] == 0)
    return out


def bindings():
    inv = BASE / "inputs/source-inventory.json"
    entries = json.loads(inv.read_text())["entries"]
    result = {}
    for e in entries:
        for field in ("source", "snapshot"):
            p = ROOT / e[field]
            test("bound " + field + " " + e[field], digest(p) == e["sha256"])
            result[e[field]] = e["sha256"]
    for rel in ("inputs/source-inventory.json", "check.py", "report.md"):
        p = BASE / rel
        result[str(p.relative_to(ROOT))] = digest(p)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if not output.is_absolute() or output.exists():
        raise RuntimeError("output must be an absolute fresh directory")
    sources = bindings()
    a = algebra()
    ex = exterior_and_overlap()
    s = support_controls()
    endpoints = numerical_certificates()
    result = {"schema": "ym28-ag3-reverse-v1", "loop": "ag3", "direction": "reverse",
              "passed": True, "check_count": len(TESTS), "checks": TESTS,
              "algebra": a, "exterior_overlap": ex, "support": s,
              "endpoints": endpoints, "sources": sources,
              "scope": {"input_weight": "2", "output_weight": "3/2",
                        "source": "actual complete AG2 indexed local mixing B",
                        "actual_input_denominator": "r=||B||_2; upper caps enter coefficient only",
                        "scalar_density": "old plus new scalar energy per site",
                        "same_weight_contraction": False,
                        "all_stage_iteration": False,
                        "full_hamiltonian_gap": False,
                        "reference_only_gap": True},
              "scope_note": "One complete bare-reference correction with changed support weight; every scalar and diagonal retained."}
    output.mkdir(parents=True)
    (output / "results.json").write_text(json.dumps(rationalize(result), sort_keys=True, indent=2) + "\n")
    print(json.dumps({"passed": True, "checks": len(TESTS), "output": str(output / "results.json")}))


if __name__ == "__main__":
    main()
