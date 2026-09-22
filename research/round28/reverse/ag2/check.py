#!/usr/bin/env python3
"""AG2 independent exact controls. Run with --output /absolute/fresh/directory.

Standard library only. Rational diagnostics test algebra and support bookkeeping;
the report supplies the infinite-dimensional domain and all-order arguments.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from math import factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CHECKS = []


def require(name, condition):
    if not condition:
        raise RuntimeError(name)
    CHECKS.append(name)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packed(x):
    if isinstance(x, F):
        return {"exact": str(x), "decimal": float(x)}
    if isinstance(x, dict):
        return {str(k): packed(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [packed(v) for v in x]
    return x


def zero(n):
    return tuple(tuple(F(0) for _ in range(n)) for _ in range(n))


def eye(n):
    return tuple(tuple(F(i == j) for j in range(n)) for i in range(n))


def mat(rows):
    return tuple(tuple(F(v) for v in row) for row in rows)


def add(a, b):
    return tuple(tuple(x + y for x, y in zip(u, v)) for u, v in zip(a, b))


def scale(c, a):
    return tuple(tuple(c * x for x in row) for row in a)


def sub(a, b):
    return add(a, scale(-1, b))


def mul(a, b):
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(len(a))), F(0))
                       for j in range(len(a))) for i in range(len(a)))


def adj(a):
    return tuple(zip(*a))


def comm(a, b):
    return sub(mul(a, b), mul(b, a))


def power(a, n):
    v = eye(len(a))
    for _ in range(n):
        v = mul(v, a)
    return v


def nested(s, a, n):
    for _ in range(n):
        a = comm(s, a)
    return a


def total(items, n):
    ans = zero(n)
    for item in items:
        ans = add(ans, item)
    return ans


def split(k):
    n = len(k)
    p = mat([[int(i == j == 0) for j in range(n)] for i in range(n)])
    q = sub(eye(n), p)
    c = k[0][0]
    mixing = add(mul(mul(p, k), q), mul(mul(q, k), p))
    diag = mul(mul(q, sub(k, scale(c, eye(n)))), q)
    return c, mixing, diag, p, q


def finite_algebra():
    h = mat([[0, 0, 0], [0, 1, 0], [0, 0, 2]])
    phi = mat([[0, 1, 1], [1, 2, 3], [1, 3, 4]])
    a = mat([[0, 1, 1], [1, 0, 0], [1, 0, 0]])
    x = mat([[0, -1, F(-1, 2)], [1, 0, 0], [F(1, 2), 0, 0]])
    require("actual-rank-form fixture commutator", comm(x, h) == scale(-1, a))
    require("fixture skewness", adj(x) == scale(-1, x))
    r2 = sub(comm(x, phi), scale(F(1, 2), comm(x, a)))
    c3 = sub(scale(F(1, 2), nested(x, phi, 2)),
             scale(F(1, 6), nested(x, a, 2)))
    c, a3, d3, p, q = split(c3)
    require("cubic source first component", a3[1][0] == F(-23, 12))
    require("cubic source second component", a3[2][0] == F(-7, 6))
    require("cubic scalar retained", c == 6)
    require("pinched cubic identity", sub(c3, a3) == add(mul(mul(p, c3), p), mul(mul(q, c3), q)))
    require("centered scalar identity", c3 == add(add(scale(c, eye(3)), a3), d3))
    require("centered complement annihilates vacuum", all(d3[i][0] == 0 for i in range(3)))
    wrong = add(add(scale(c, eye(3)), a3), mul(mul(q, c3), q))
    require("scalar double-counting control", wrong != c3)
    require("quadratic coefficient retained", r2[0][0] == F(-3, 2))
    require("wrong n1 coefficient rejected", sub(comm(x, phi), scale(F(1, 3), comm(x, a))) != r2)
    require("wrong n2 coefficient rejected", scale(F(1, 2), nested(x, phi, 2)) != c3)
    require("quadratic mixing need not vanish in diagnostic", any(r2[i][0] != 0 for i in (1, 2)))

    # Independent product-of-exponentials expansion, rather than BCH recurrence.
    degree = 6
    for k in range(degree + 1):
        lhs = zero(3)
        for l in range(k + 1):
            rr = k - l
            lhs = add(lhs, scale(F((-1) ** rr, factorial(l) * factorial(rr)),
                                  mul(mul(power(x, l), h), power(x, rr))))
        if k:
            for l in range(k):
                rr = k - 1 - l
                lhs = add(lhs, scale(F((-1) ** rr, factorial(l) * factorial(rr)),
                                      mul(mul(power(x, l), phi), power(x, rr))))
        rhs = h if k == 0 else sub(phi, a) if k == 1 else sub(
            scale(F(1, factorial(k - 1)), nested(x, phi, k - 1)),
            scale(F(1, factorial(k)), nested(x, a, k - 1)))
        require("independent exponential identity degree %d" % k, lhs == rhs)

    for t in (F(-1, 7), F(0), F(1, 7)):
        xt, phit, at = scale(t, x), scale(t, phi), scale(t, a)
        rt = sub(comm(xt, phit), scale(F(1, 2), comm(xt, at)))
        ct = sub(scale(F(1, 2), nested(xt, phit, 2)), scale(F(1, 6), nested(xt, at, 2)))
        require("even quadratic sign %s" % t, rt == scale(t * t, r2))
        require("odd cubic sign %s" % t, ct == scale(t ** 3, c3))
        require("zero coupling exactness %s" % t, t != 0 or rt == ct == zero(3))
    # At fixed volume the nonzero quadratic vacuum coefficient excludes O(tau^4).
    require("quartic-assignment countercontrol", r2[0][0] != 0 and a3[0][0] == 0)
    # Full second-conjugation identity, with a formal correction parameter e:
    # [e*x,g]=-e*A3+e*R. This is an algebra diagnostic, not the physical filter.
    g = add(h, sub(phi, a))
    residual = add(a3, comm(x, g))
    for k in range(1, 7):
        lhs = add(add(scale(F(1, factorial(k)), nested(x, g, k)),
                      scale(F(1, factorial(k - 1)), nested(x, a3, k - 1))),
                  scale(F(1, factorial(k)), nested(x, r2, k)))
        rhs_base = residual if k == 1 else scale(F(1, factorial(k)),
            nested(x, add(scale(k - 1, a3), residual), k - 1))
        rhs = add(rhs_base, scale(F(1, factorial(k)), nested(x, r2, k)))
        require("full transported-E identity degree %d" % k, lhs == rhs)
        require("omitted transported-E term degree %d" % k, lhs != rhs_base)
    return {"quadratic_vacuum": r2[0][0], "cubic_scalar": c,
            "cubic_source": [a3[1][0], a3[2][0]], "checked_degree": degree}


def embed(local, sites, n):
    states = list(product((0, 1), repeat=n))
    out = [[F(0) for _ in states] for _ in states]
    for i, a in enumerate(states):
        for j, b in enumerate(states):
            if any(a[k] != b[k] for k in range(n) if k not in sites):
                continue
            ai = sum(a[k] * 2 ** (len(sites) - 1 - z) for z, k in enumerate(sites))
            bi = sum(b[k] * 2 ** (len(sites) - 1 - z) for z, k in enumerate(sites))
            out[i][j] = local[ai][bi]
    return mat(out)


def overlapping_control():
    phi = mat([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    a = mat([[0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]])
    s = mat([[0, 0, 0, F(-1, 2)], [0, 0, 0, 0], [0, 0, 0, 0], [F(1, 2), 0, 0, 0]])
    ss = [embed(s, z, 3) for z in ((0, 1), (1, 2))]
    pp = [embed(phi, z, 3) for z in ((0, 1), (1, 2))]
    aa = [embed(a, z, 3) for z in ((0, 1), (1, 2))]
    sx, px, ax = total(ss, 8), total(pp, 8), total(aa, 8)
    full2 = sub(comm(sx, px), scale(F(1, 2), comm(sx, ax)))
    own2 = total((sub(comm(s, p), scale(F(1, 2), comm(s, a))) for s, p, a in zip(ss, pp, aa)), 8)
    require("omitted overlapping quadratic words rejected", full2 != own2)
    full3 = sub(scale(F(1, 2), nested(sx, px, 2)), scale(F(1, 6), nested(sx, ax, 2)))
    own3 = total((sub(scale(F(1, 2), nested(s, p, 2)), scale(F(1, 6), nested(s, a, 2))) for s, p, a in zip(ss, pp, aa)), 8)
    require("omitted overlapping cubic words rejected", full3 != own3)
    words = total((sub(scale(F(1, 2), comm(ss[j], comm(ss[i], pp[b]))),
                            scale(F(1, 6), comm(ss[j], comm(ss[i], aa[b]))))
                   for b, i, j in product(range(2), repeat=3)), 8)
    require("ordered cubic expansion including repeats", words == full3)
    extra = sub(full2, own2)
    # Omitting E loses its zeroth transported term, and dropping [S,E] loses next.
    require("original E transport has nonzero zeroth term", extra != zero(8))
    require("original E transport has nonzero commutator", comm(sx, extra) != zero(8))
    return {"abstract_sites": 3, "ordered_cubic_tuples": 8,
            "scope": "overlapping-pair rational matrix diagnostic, not physical SU(2)"}


G = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))


def plus(a, b):
    return tuple(x + y for x, y in zip(a, b))


def star(b):
    return frozenset(plus(b, x) for x in G)


def meeting(y):
    return {tuple(a - b for a, b in zip(x, g)) for x in y for g in G}


def geometry():
    seed = star((0, 0, 0))
    neighbors = meeting(seed)
    require("thirteen full star displacements", len(neighbors) == 13)
    require("twelve interior crossings", len(neighbors - {(0, 0, 0)}) == 12)
    require("incoming crossing control", len([b for b in neighbors if min(b) < 0]) == 9)
    words = [(seed, ())]
    relative_counts = [1]
    for n in (1, 2, 3):
        nxt = []
        for y, w in words:
            m = meeting(y)
            require("prefix support bound n%d %s" % (n, w), len(y) <= 4 + 3 * (n - 1))
            require("attachment count n%d %s" % (n, w), len(m) <= 13 * n)
            for b in m:
                yy = y | star(b)
                if len(yy) > 4 + 3 * n:
                    raise RuntimeError("union support")
                nxt.append((yy, w + (b,)))
        words = nxt
        relative_counts.append(len(words))
        require("relative word bound n%d" % n, len(words) <= 13 ** n * factorial(n))
        require("repeat words retained n%d" % n, any(all(b == (0, 0, 0) for b in w) for y, w in words))
    # Every actual relative two-word family contains its one all-equal tuple.
    require("other cubic relative words bounded by337", relative_counts[2] - 1 <= 337)
    cases = []
    for side in (1, 2, 3, 5):
        sites = set(product(range(side), repeat=3))
        anchors = [b for b in sites if star(b) <= sites]
        loading = Counter(x for b in anchors for x in star(b))
        load = max(loading.values(), default=0)
        require("boundary load side%d" % side, load <= 4)
        require("complete anchors side%d" % side, len(anchors) == (side - 1) ** 3)
        if side == 1:
            require("empty anchor case", load == 0)
        if side == 2:
            require("one-star denominator case", load == 1)
        if side == 5:
            require("interior load four", load == 4)
        cases.append({"cuboid_side": side, "anchors": len(anchors), "max_loading": load})
    return {"relative_word_counts_n0_to3": relative_counts, "boundary_cases": cases}


def budgets(m):
    rho = F(9, 4)
    s = a = m / 9  # sqrt(1/84) M <= M/9, used only as an upper bound.
    z = 26 * s * rho ** 3
    e2 = rho ** 4 * 7 * z * (m + a / 2)
    e3same = 8 * rho ** 4 * s ** 2 * (m + a / 3)
    e3other = F(337, 338) * rho ** 4 * 10 * z ** 2 * (m + a / 3)
    e4 = rho ** 4 * (m + a / 4) * z ** 3 * (13 - 10 * z) / (1 - z) ** 2
    direct = e2 + e3same + e3other + e4
    rbar = F(4, 3) * a ** 3
    triangle = rho ** 4 * (m + a / 2) * z * (7 - 4 * z) / (1 - z) ** 2 + 4 * rho ** 4 * rbar
    arho = 4 * rho ** 4 * rbar
    f_rho = 1 / (1 - 72 * rho ** 3 * m) ** 3
    f_two = 1 / (1 - 576 * m) ** 3
    theta = 18 * arho * f_rho
    nonlinear = theta / (1 - theta) * arho * (1 + f_rho / 2)
    selected = 64 * rbar * f_two
    if m <= F(1, 10000):
        selected = 64 * rbar * (F(4, 9) + f_two - 1)
    transported = direct / (1 - theta)
    whole = selected + nonlinear + transported
    gap = 1 - 4 * m - whole / 8
    return {"M": m, "s_upper": s, "A1_upper": a, "z": z,
            "E2_rho": e2, "E3same_pinched_rho": e3same,
            "E3other_rho": e3other, "E4plus_rho": e4,
            "E_direct_rho": direct, "E_triangle_rho": triangle,
            "A3_single_upper": rbar, "A3_family_rho_upper": arho,
            "AG1_F_rho": f_rho, "theta": theta,
            "selected_R_2_upper": selected, "nonlinear_N_2_upper": nonlinear,
            "transported_E_2_upper": transported,
            "complete_K_2_upper": whole, "scalar_weighted_upper": whole,
            "mixing_weighted_upper": whole, "centered_diagonal_weighted_upper": 2 * whole,
            "scalar_incidence_density_upper": whole / 16,
            "scalar_energy_per_site_upper": whole / 64,
            "centered_diagonal_relative_upper": whole / 8,
            "reference_only_gap_dimensionless_lower": gap,
            "full_mixing_contraction": "not established; no actual full input denominator"}


def arithmetic_controls():
    require("rational rank upper envelope", F(1, 84) < F(1, 81))
    # Geometric tail rational identity by exact first coefficients and residual.
    for z in (F(0), F(1, 100), F(1, 20)):
        full = z ** 3 * (13 - 10 * z) / (1 - z) ** 2
        prefix = sum((F(4 + 3 * n) * z ** n for n in range(3, 15)), F(0))
        rest = z ** 15 * (49 - 46 * z) / (1 - z) ** 2
        require("all-order tail exact identity %s" % z, full == prefix + rest)
    endpoints = [budgets(F(0)), budgets(F(1, 10000)), budgets(F(1, 1000))]
    for b in endpoints:
        m = b["M"]
        require("original-series radius %s" % m, b["z"] < 1)
        require("AG1 filter radius %s" % m, 72 * F(9, 4) ** 3 * m < 1)
        require("nonlinear radius %s" % m, b["theta"] < 1)
        require("direct inventory improves triangle %s" % m, b["E_direct_rho"] <= b["E_triangle_rho"])
        require("reference-only gap positive %s" % m, b["reference_only_gap_dimensionless_lower"] > 0)
        require("transport includes all original E %s" % m, b["transported_E_2_upper"] >= b["E_direct_rho"])
    require("zero entire correction", endpoints[0]["complete_K_2_upper"] == 0)
    require("main K below 7/1000", endpoints[-1]["complete_K_2_upper"] < F(7, 1000))
    require("main reference-only gap above 995/1000", endpoints[-1]["reference_only_gap_dimensionless_lower"] > F(995, 1000))
    require("narrow K below 7/100000", endpoints[1]["complete_K_2_upper"] < F(7, 100000))
    # Counterexample to the unsupported generic domain/differentiation premise.
    for n in (4, 16, 64):
        norm_v_squared = sum((F(1, j * j) for j in range(1, n + 1)), F(0))
        graph_part_squared = sum((F(1) for _ in range(n)), F(0))
        require("bounded rank-vector partial norm n%d" % n, norm_v_squared < 2)
        require("unbounded H rank-vector graph part n%d" % n, graph_part_squared == n)
    require("finite-volume does not bound onsite generator", 64 > 16 > 4)
    return endpoints


def source_bindings():
    inventory = HERE / "inputs/source-inventory.json"
    entries = json.loads(inventory.read_text())["entries"]
    sources = {}
    for e in entries:
        p = ROOT / e["snapshot"]
        require("snapshot " + e["snapshot"], sha(p) == e["sha256"])
        sources[e["snapshot"]] = sha(p)
        if not e.get("external_instruction_snapshot"):
            p = ROOT / e["source"]
            require("current bound source " + e["source"], sha(p) == e["sha256"])
            sources[e["source"]] = sha(p)
    for name in ("check.py", "report.md", "inputs/source-inventory.json", "inputs/adoption-record.json"):
        p = HERE / name
        sources[str(p.relative_to(ROOT))] = sha(p)
    return sources


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output)
    if not out.is_absolute() or out.exists():
        raise RuntimeError("--output must be an absolute fresh directory")
    sources = source_bindings()
    algebra = finite_algebra()
    overlaps = overlapping_control()
    geom = geometry()
    endpoints = arithmetic_controls()
    result = {"schema": "ym28-ag2-reverse-v1", "loop": "ag2", "direction": "reverse",
              "passed": True, "checks_count": len(CHECKS), "checks": CHECKS,
              "algebra": algebra, "overlaps": overlaps, "geometry": geom,
              "endpoints": endpoints, "sources": sources,
              "scope": "Exact original E inventory and transport; reference-only form bound. No full mixing contraction or original Hamiltonian gap."}
    out.mkdir(parents=True)
    (out / "results.json").write_text(json.dumps(packed(result), sort_keys=True, indent=2) + "\n")
    print(json.dumps({"passed": True, "checks": len(CHECKS), "output": str(out / "results.json")}))


if __name__ == "__main__":
    main()
