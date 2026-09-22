#!/usr/bin/env python3
"""AG2 forward exact controls and rational upper budgets; standard library only."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import itertools
import json
from math import factorial
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
RHO = F(9, 4)
STAR = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))
CHECKS = []


def require(name, condition):
    if not condition:
        raise RuntimeError("FAILED: " + name)
    CHECKS.append(name)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(obj):
    if isinstance(obj, F):
        return {"numerator": obj.numerator, "denominator": obj.denominator}
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(v) for v in obj]
    return obj


def addv(a, b):
    return tuple(x + y for x, y in zip(a, b))


def subv(a, b):
    return tuple(x - y for x, y in zip(a, b))


def star(b):
    return frozenset(addv(b, z) for z in STAR)


def incoming(union):
    return sorted({subv(y, z) for y in union for z in STAR})


def geometry():
    # Every possible incoming anchor is exactly y-z with y in old union,z in STAR.
    y0 = star((0, 0, 0))
    relative = {0: Counter({4: 1}), 1: Counter(), 2: Counter()}
    for b in incoming(y0):
        y1 = y0 | star(b)
        relative[1][len(y1)] += 1
        for c in incoming(y1):
            relative[2][len(y1 | star(c))] += 1
    require("complete_relative_difference_set_13", len(incoming(y0)) == 13)
    require("depth_one_same_and_twelve_cross", relative[1] == Counter({4: 1, 7: 12}))
    require("one_depth_two_all_equal_word", relative[2][4] == 1)
    require("depth_two_support_at_most_10", max(relative[2]) <= 10)
    require("depth_two_nontrivial_cross_words", sum(relative[2].values()) > 13)

    boundary = []
    for shape in ((1, 1, 1), (2, 2, 2), (3, 3, 3)):
        sites = set(itertools.product(*(range(n) for n in shape)))
        anchors = sorted(b for b in sites if star(b) <= sites)
        roots = {n: defaultdict(Counter) for n in range(3)}
        for b in anchors:
            y0b = star(b)
            for x in y0b:
                roots[0][x][4] += 1
            for c in anchors:
                if not (star(c) & y0b):
                    continue
                y1 = y0b | star(c)
                for x in y1:
                    roots[1][x][len(y1)] += 1
                for d in anchors:
                    if not (star(d) & y1):
                        continue
                    y2 = y1 | star(d)
                    for x in y2:
                        roots[2][x][len(y2)] += 1
        for n in range(3):
            for a in (F(2), RHO):
                bound = sum(count * size * a**size for size, count in relative[n].items())
                actual_max = max((sum(count * a**size for size, count in v.items())
                                  for v in roots[n].values()), default=F(0))
                require(f"complete_boundary_{shape}_depth{n}_weight{a}", actual_max <= bound)
        boundary.append({"shape": shape, "anchors": len(anchors),
                         "max_star_incidence": max((sum(v.values()) for v in roots[0].values()), default=0)})
    require("empty_boundary_has_no_source", boundary[0]["anchors"] == 0)
    require("one_star_boundary", boundary[1]["anchors"] == 1)
    require("interior_four_incoming_roots", boundary[2]["max_star_incidence"] == 4)
    sites4 = set(itertools.product(range(4), repeat=3))
    all4 = {b for b in sites4 if star(b) <= sites4}
    inner = (1, 1, 1)
    cross = [b for b in all4 if b != inner and star(b) & star(inner)]
    require("interior_twelve_crossings", len(cross) == 12)
    return relative, boundary


def qpoly(table, a):
    return sum(F(count * size) * a**size for size, count in table.items())


def budgets(M, relative, narrow=False):
    s = sigma = F(4, 35) * M
    x = 24 * s * RHO**3
    require(f"O1_complete_tail_radius_{M}", 0 <= x < 1)
    Q1 = qpoly(relative[1], RHO)
    Q2 = qpoly(relative[2], RHO)
    E2 = 2 * s * (M + sigma / 2) * Q1
    cubic_unit = 4 * s**2 * (M / 2 + sigma / 6)
    E3same = cubic_unit * 4 * RHO**4
    E3other = cubic_unit * (Q2 - 4 * RHO**4)
    tail_series = (1 - x)**-3 - 1 - 3 * x - 6 * x**2
    tail = 4 * RHO**4 * (M + sigma / 4) * tail_series
    E = E2 + E3same + E3other + tail
    fullR = 4 * RHO**4 * (M + sigma / 2) * ((1 - x)**-3 - 1)
    rbd = M**3 / 567
    A3rho = 4 * RHO**4 * rbd
    triangle = fullR + A3rho
    Fag = (1 - 72 * RHO**3 * M)**-3
    S = A3rho * Fag
    theta = 18 * S
    require(f"AG1_transport_radius_{M}", 0 <= theta < 1)
    Etransport = E / (1 - theta)
    N = theta / (1 - theta) * A3rho * (1 + Fag / 2)
    A3two = 64 * rbd
    Ftwo = (1 - 576 * M)**-3
    if narrow:
        require(f"narrow_filter_scope_{M}", M <= F(1, 10000))
        R = A3two * (F(4, 9) + Ftwo - 1)
    else:
        R = A3two * Ftwo
    K = Etransport + R + N
    kappa = 4 * M + K / 8
    require(f"nonnegative_inventory_{M}", min(E2, E3same, E3other, tail, E) >= 0)
    require(f"direct_inventory_no_larger_than_triangle_at_{M}", E <= triangle)
    return {"M": M, "tau_absolute": M / 7, "narrow_free_filter": narrow,
            "x_O1": x, "Q1_rho": Q1, "Q2_rho": Q2,
            "E2_rho": E2, "E3_same_rho": E3same, "E3_other_rho": E3other,
            "E_ge4_rho": tail, "E_direct_rho": E, "full_R_rho_upper": fullR,
            "E_triangle_rho": triangle, "selected_A3_rho_upper": A3rho,
            "theta": theta, "transported_E_two": Etransport,
            "selected_R_two": R, "selected_N_two": N, "complete_K_two": K,
            "scalar_density": K / 64, "complete_mixing_two": K,
            "centered_diagonal_increment_two": 2 * K,
            "full_diagonal_two": 64 * M + 2 * K,
            "diagonal_relative_kappa": kappa, "reference_gap_lower": 1 - kappa,
            "full_mixing_contraction": "not established: actual full input denominator absent"}


def zero(n):
    return tuple(tuple(F(0) for _ in range(n)) for _ in range(n))


def eye(n):
    return tuple(tuple(F(i == j) for j in range(n)) for i in range(n))


def scale(a, c):
    return tuple(tuple(c * x for x in row) for row in a)


def plus(*args):
    n = len(args[0])
    return tuple(tuple(sum(a[i][j] for a in args) for j in range(n)) for i in range(n))


def mul(a, b):
    n = len(a)
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)) for i in range(n))


def transpose(a):
    return tuple(zip(*a))


def comm(a, b):
    return plus(mul(a, b), scale(mul(b, a), -1))


def nested(a, b, n):
    for _ in range(n):
        b = comm(a, b)
    return b


def diagonal(vals):
    return tuple(tuple(F(vals[i]) if i == j else F(0) for j in range(len(vals))) for i in range(len(vals)))


def column_mix(a):
    n = len(a)
    return tuple(tuple(a[i][j] if (i == 0) != (j == 0) else F(0) for j in range(n)) for i in range(n))


def homological(phi, energies):
    n = len(phi)
    u = [F(0)] + [phi[i][0] / energies[i] for i in range(1, n)]
    return tuple(tuple(u[i] if j == 0 else (-u[j] if i == 0 else F(0)) for j in range(n)) for i in range(n))


def exponential_coeff(a, n):
    out = eye(len(a))
    for _ in range(n):
        out = mul(out, a)
    return scale(out, F(1, factorial(n)))


def conjugated_coefficient(S, terms, degree):
    n = len(S)
    out = zero(n)
    for k, Hk in terms.items():
        if k > degree:
            continue
        for i in range(degree - k + 1):
            j = degree - k - i
            out = plus(out, mul(mul(exponential_coeff(S, i), Hk),
                                exponential_coeff(scale(S, -1), j)))
    return out


def embed_pair(local, pair):
    out = []
    for i in range(8):
        bits_i = [(i >> (2 - k)) & 1 for k in range(3)]
        row = []
        for j in range(8):
            bits_j = [(j >> (2 - k)) & 1 for k in range(3)]
            exterior = ({0, 1, 2} - set(pair)).pop()
            li = 2 * bits_i[pair[0]] + bits_i[pair[1]]
            lj = 2 * bits_j[pair[0]] + bits_j[pair[1]]
            row.append(local[li][lj] if bits_i[exterior] == bits_j[exterior] else F(0))
        out.append(tuple(row))
    return tuple(out)


def algebra():
    H = diagonal([0, 1, 3])
    phi = tuple(tuple(F(x) for x in row) for row in ((0, 1, 1), (1, 2, 1), (1, 1, 0)))
    A1 = column_mix(phi)
    X = homological(phi, [0, 1, 3])
    D = plus(phi, scale(A1, -1))
    require("O1_first_commutator_sign", comm(X, H) == scale(A1, -1))
    require("O1_generator_skew", transpose(X) == scale(X, -1))
    R2 = plus(comm(X, phi), scale(comm(X, A1), F(-1, 2)))
    require("retained_D_quadratic_identity", R2 == plus(comm(X, D), scale(comm(X, A1), F(1, 2))))
    C = plus(scale(nested(X, phi, 2), F(1, 2)), scale(nested(X, A1, 2), F(-1, 6)))
    A3 = column_mix(C)
    c = C[0][0]
    comp = plus(C, scale(A3, -1))
    P = diagonal([1, 0, 0])
    Q = diagonal([0, 1, 1])
    Z = mul(mul(Q, plus(C, scale(eye(3), -c))), Q)
    require("same_anchor_compression_identity", comp == plus(mul(mul(P, C), P), mul(mul(Q, C), Q)))
    require("same_anchor_scalar_centered_diagonal", C == plus(scale(eye(3), c), A3, Z))
    require("same_anchor_has_no_omitted_mixing", column_mix(comp) == zero(3))
    require("scalar_double_count_control_discriminates", C != plus(scale(eye(3), c), A3, mul(mul(Q, C), Q)))
    require("actual_fixture_quadratic_vacuum_nonzero", R2[0][0] == F(-4, 3))
    require("quadratic_mixing_need_not_vanish", column_mix(R2) != zero(3))
    require("selected_cubic_fixture_nonzero", A3 != zero(3))
    require("wrong_n1_A_coefficient_rejected", R2 != plus(comm(X, phi), scale(comm(X, A1), F(-1, 3))))
    require("wrong_n2_phi_coefficient_rejected", C != plus(scale(nested(X, phi, 2), F(1, 3)), scale(nested(X, A1, 2), F(-1, 6))))
    require("wrong_n2_A_coefficient_rejected", C != plus(scale(nested(X, phi, 2), F(1, 2)), scale(nested(X, A1, 2), F(-1, 4))))
    for sign in (-1, 0, 1):
        sx, sp, sa = scale(X, sign), scale(phi, sign), scale(A1, sign)
        for degree in range(7):
            got = conjugated_coefficient(sx, {0: H, 1: sp}, degree)
            if degree == 0:
                expected = H
            elif degree == 1:
                expected = scale(D, sign)
            else:
                n = degree - 1
                expected = plus(scale(nested(sx, sp, n), F(1, factorial(n))),
                                scale(nested(sx, sa, n), F(-1, factorial(n + 1))))
            require(f"independent_O1_exponential_sign{sign}_degree{degree}", got == expected)
        require(f"cubic_parity_sign{sign}", plus(scale(nested(sx, sp, 2), F(1, 2)), scale(nested(sx, sa, 2), F(-1, 6))) == scale(C, sign**3))
    # Overlapping pairs: all local operators extended by the exterior identity.
    pl = tuple(tuple(F(x) for x in row) for row in ((0, 1, 1, 1), (1, 1, 1, 0), (1, 1, 2, 1), (1, 0, 1, 1)))
    sl = homological(pl, [0, 1, 1, 2])
    al = column_mix(pl)
    Ss = [embed_pair(sl, p) for p in ((0, 1), (1, 2))]
    Ps = [embed_pair(pl, p) for p in ((0, 1), (1, 2))]
    As = [embed_pair(al, p) for p in ((0, 1), (1, 2))]
    sx, ph, a1 = plus(*Ss), plus(*Ps), plus(*As)
    quadratic = plus(comm(sx, ph), scale(comm(sx, a1), F(-1, 2)))
    samequadratic = plus(*(plus(comm(Ss[i], Ps[i]), scale(comm(Ss[i], As[i]), F(-1, 2))) for i in range(2)))
    require("omitted_cross_quadratic_discriminates", quadratic != samequadratic)
    allcubic = plus(scale(nested(sx, ph, 2), F(1, 2)), scale(nested(sx, a1, 2), F(-1, 6)))
    samecubic = plus(*(plus(scale(nested(Ss[i], Ps[i], 2), F(1, 2)), scale(nested(Ss[i], As[i], 2), F(-1, 6))) for i in range(2)))
    ordered = zero(8)
    for b0, b1, b2 in itertools.product(range(2), repeat=3):
        ordered = plus(ordered, scale(comm(Ss[b2], comm(Ss[b1], Ps[b0])), F(1, 2)),
                       scale(comm(Ss[b2], comm(Ss[b1], As[b0])), F(-1, 6)))
    require("all_ordered_cubic_words_exact", ordered == allcubic)
    require("omitted_cross_cubic_discriminates", allcubic != samecubic)
    # AG1 coefficient identity is algebraic for any bounded pair obeying [S,G]=-A+R.
    G = plus(H, scale(D, F(1, 7)))
    S = scale(X, F(1, 5))
    A = A3
    R = plus(A, comm(S, G))
    E = R2
    for degree in range(7):
        direct = conjugated_coefficient(S, {0: G, 1: A, 2: E}, degree)
        rhs = G if degree == 0 else (R if degree == 1 else zero(3))
        if degree >= 2:
            n = degree - 1
            rhs = plus(rhs, scale(nested(S, plus(scale(A, n), R), n), F(1, factorial(n + 1))),
                       scale(nested(S, E, degree - 2), F(1, factorial(degree - 2))))
        require(f"complete_AG1_plus_E_identity_degree{degree}", direct == rhs)
    require("missing_E_transport_discriminates", E != zero(3) and comm(S, E) != zero(3))
    require("unsupported_quartic_E_discriminates", R2[0][0] != 0 and A3[0][0] == 0)
    require("wrong_G_only_nonlinear_coefficient_discriminates", comm(S, A) != zero(3))
    return {"fixture_quadratic_vacuum_coefficient": R2[0][0],
            "fixture_same_cubic_scalar": c,
            "role": "Exact finite algebra controls; not physical SU(2) approximation or cutoff evidence."}


def analytic_controls():
    p = F(8, 3)
    kp = F(1)
    for n in range(1, 33):
        kp *= (p + n - 1) / n
        require(f"all_order_tail_coefficient_illustration_{n}", kp <= F((n + 1) * (n + 2), 2))
    # The report proves all n by factorwise comparison; this finite prefix is a control.
    require("exact_first_binomial_coefficient", p == F(8, 3))
    require("exact_second_binomial_coefficient", p * (p + 1) / 2 == F(44, 9))
    require("O1_general_weight_matches_inherited_weight2", 8 * F(2)**3 == 64)
    for size in range(4, 65):
        require(f"scalar_support_density_cost_{size}", F(1, size * 2**size) <= F(1, 64))
        require(f"diagonal_relative_support_cost_{size}", F(2, 2**size) <= F(1, 8))
    # A bounded rank-two operator taking e0 to v_j=1/j need not preserve D(diag(j)).
    partial_norm2 = sum(F(1, j*j) for j in range(1, 65))
    partial_graph2 = sum(F(j*j, j*j) for j in range(1, 65))
    require("bounded_operator_domain_shortcut_control", partial_norm2 < 2 and partial_graph2 == 64)
    # Build exact Taylor coefficients of f_n(t)=sin(nt)/n; its uniform bound is1/n.
    sine_coeff = {n: {2*k+1: F((-1)**k * n**(2*k+1), n*factorial(2*k+1))
                     for k in range(4)} for n in (8, 64)}
    require("differentiate_value_bound_shortcut_control",
            F(1, 64) < F(1, 8) and sine_coeff[64][1] == sine_coeff[8][1] == 1
            and sine_coeff[64][3] != sine_coeff[8][3])
    require("input_weight_cannot_be_reset", (RHO / 2)**64 > 1000)
    require("upper_bound_not_lower_denominator", F(2, 3) * F(1, 100) < F(1, 10) < F(2, 3))
    return {"domain_counterexample": "v_j=1/j is in l2, H v not in l2; finite prefix corroborates the explicit series proof.",
            "derivative_counterexample": "sin(nt)/n ->0 uniformly but derivatives at0 equal1; no dynamics-derivative inference used."}


def bindings():
    sources = json.loads((HERE / "inputs/source-inventory.json").read_text())
    contract = json.loads((ROOT / "research/round28/contracts/ag2.json").read_text())
    require("all_contract_sources_required", all(sources.get(p) == h for p, h in contract["sources"].items()))
    require("contract_bound_as_source", sources.get("research/round28/contracts/ag2.json") == sha(ROOT / "research/round28/contracts/ag2.json"))
    for p, digest in sources.items():
        require("live_source:" + p, sha(ROOT / p) == digest)
        require("snapshot_source:" + p, sha(HERE / "inputs" / p) == digest)
    instructions = json.loads((HERE / "inputs/instruction-inventory.json").read_text())
    for p, rec in instructions.items():
        require("instruction:" + p, sha(HERE / "inputs/instructions" / p) == rec["sha256"])
    own = {}
    for p in ("check.py", "report.md", "adoption.json", "inputs/source-inventory.json", "inputs/instruction-inventory.json"):
        own[p] = sha(HERE / p)
    return {"sources": sources, "instructions": instructions, "producer": own}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if not args.output.is_absolute() or args.output.exists():
        raise SystemExit("--output must be a fresh absolute directory")
    source = bindings()
    relative, boundary = geometry()
    end = {"zero": budgets(F(0), relative),
           "main": budgets(F(1, 1000), relative),
           "narrow": budgets(F(1, 10000), relative, narrow=True)}
    require("zero_budget_exact", end["zero"]["complete_K_two"] == 0)
    require("main_reference_positive", end["main"]["reference_gap_lower"] > F(99, 100))
    require("narrow_reference_positive", end["narrow"]["reference_gap_lower"] > F(999, 1000))
    for name, Kceil, Cceil, gapfloor in (
        ("main", F(6168, 10**6), F(9637, 10**8), F(995229, 10**6)),
        ("narrow", F(59689, 10**9), F(9327, 10**10), F(9995925, 10**7))):
        require(name + "_displayed_E_bound", end[name]["E_direct_rho"] < Kceil)
        require(name + "_displayed_K_bound", end[name]["complete_K_two"] < Kceil)
        require(name + "_displayed_scalar_bound", end[name]["scalar_density"] < Cceil)
        require(name + "_displayed_reference_gap", end[name]["reference_gap_lower"] > gapfloor)
    # Positive-coefficient formulae prove monotonicity continuously in the report.
    matrix = algebra()
    analytic = analytic_controls()
    out = {"schema": "ag2-forward-exact-v1", "status": "passed", "model": contract_model(),
           "geometry": {"relative_words_by_union_size": relative, "boundary_controls": boundary},
           "endpoints": end, "algebra": matrix, "analytic_controls": analytic,
           "checks": CHECKS, "check_count": len(CHECKS), "bindings": source,
           "scope": {"complete_E_inventory": True, "complete_transport": True,
                     "reference_only_gap": True, "full_mixing_contraction": False,
                     "homogeneous_full_gap": False, "continuum_Yang_Mills": False}}
    args.output.mkdir(parents=True)
    (args.output / "results.json").write_text(json.dumps(encode(out), sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": "passed", "checks": len(CHECKS), "results_sha256": sha(args.output / "results.json")}))


def contract_model():
    return "Original homogeneous O1 Hamiltonian; full E through actual admitted selected-source AG1 correction, fixed delta=alpha/8."


if __name__ == "__main__":
    main()
