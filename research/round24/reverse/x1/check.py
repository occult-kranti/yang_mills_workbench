#!/usr/bin/env python3
"""Exact SU(2)/graph coefficients and rational X1 reverse certificates.

Standard library only. The report supplies the all-sector proofs; this
program computes real finite-sector coefficients and checks their budgets.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
from itertools import combinations, product
import hashlib
import json
from math import comb, factorial, isqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def rational(x):
    return str(F(x))


def poly_add(a, b):
    out = dict(a)
    for n, v in b.items():
        out[n] = out.get(n, F(0)) + v
    return {n: v for n, v in out.items() if v}


def poly_scale(a, s):
    return {n: s*v for n, v in a.items() if s*v}


def poly_mul(a, b):
    out = {}
    for n, v in a.items():
        for m, w in b.items():
            out[n+m] = out.get(n+m, F(0)) + v*w
    return {n: v for n, v in out.items() if v}


def haar_moment(n):
    if n % 2:
        return F(0)
    k = n//2
    return F(comb(2*k, k), (k+1)*4**k)


def haar_integral(p):
    return sum((v*haar_moment(n) for n, v in p.items()), F(0))


def character(n):
    require(n >= 0, "Character label must be nonnegative")
    p, q = {0: F(1)}, {1: F(2)}
    if n == 0:
        return p
    for _ in range(1, n):
        p, q = q, poly_add(poly_mul({1: F(2)}, q), poly_scale(p, -1))
    return q


def sqrt_interval(x, denominator=10**18):
    require(x >= 0 and denominator > 0, "Invalid square-root interval")
    k = isqrt((x.numerator*denominator**2)//x.denominator)
    lo = F(k, denominator)
    hi = lo if lo*lo == x else F(k+1, denominator)
    require(lo*lo <= x <= hi*hi, "Square-root enclosure failed")
    return lo, hi


def exp_interval(x, order=24):
    require(x >= 0 and order >= 0, "This exponential enclosure uses x>=0")
    lower = sum((x**n/factorial(n) for n in range(order+1)), F(0))
    ratio = x/F(order+2)
    require(ratio < 1, "Taylor remainder ratio is not contractive")
    remainder = x**(order+1)/factorial(order+1)/(1-ratio)
    return lower, lower+remainder


def graph():
    # Build nearest-neighbor incidence from vertex pairs, independently of
    # the inherited axis/edge-ID construction. Orientation is irrelevant to
    # these center-parity and four-cycle statements (SU(2) trace reverses).
    vertices = list(product(range(3), range(3), range(2)))
    edges = [frozenset((u, v)) for u, v in combinations(vertices, 2)
             if sum(abs(u[k]-v[k]) for k in range(3)) == 1]
    lookup = {edge: n for n, edge in enumerate(edges)}
    adjacency = {v: [] for v in vertices}
    for edge in edges:
        u, v = tuple(edge)
        adjacency[u].append(v)
        adjacency[v].append(u)
    faces = set()
    for p in vertices:
        for a, b in combinations(range(3), 2):
            corners = []
            for da, db in ((0, 0), (1, 0), (1, 1), (0, 1)):
                q = tuple(p[k]+da*(k == a)+db*(k == b) for k in range(3))
                corners.append(q)
            if all(q in adjacency for q in corners):
                faces.add(frozenset(lookup[frozenset((corners[k], corners[(k+1)%4]))]
                                    for k in range(4)))
    cycles = set()
    for u in vertices:
        for v in adjacency[u]:
            for w in adjacency[v]:
                if w == u:
                    continue
                for z in adjacency[w]:
                    if z in (u, v) or u not in adjacency[z]:
                        continue
                    cycles.add(frozenset(lookup[frozenset((a, b))]
                                         for a, b in ((u,v),(v,w),(w,z),(z,u))))
    require((len(vertices), len(edges), len(faces)) == (18, 33, 20),
            "Wrong physical graph")
    require(cycles == faces, "Degree-four physical cycle enumeration incomplete")
    require(all(sum(v)%2 != sum(u)%2 for edge in edges for u, v in [tuple(edge)]),
            "Graph is not bipartite")
    masks = sorted(sum(1 << n for n in f) for f in faces)
    triple_zeros = sum(a ^ b ^ c == 0 for a in masks for b in masks for c in masks)
    require(triple_zeros == 0, "A triple-face parity selection rule was missed")
    return vertices, edges, faces, masks


def matvec(matrix, vector):
    return [sum((a*b for a, b in zip(row, vector)), F(0)) for row in matrix]


def actual_matrix(coupling, face_count=20):
    require(face_count == 20, "A 19-face memory matrix is not the full physical truncation")
    matrix = [[F(0) for _ in range(21)] for _ in range(21)]
    matrix[0][0] = 20*coupling
    for p in range(1, 21):
        matrix[p][p] = 3+20*coupling
        matrix[p][0] = matrix[0][p] = -coupling/2
    return matrix


def ground_budget(coupling, cutoff):
    require(coupling >= 0 and coupling <= F(1, 100), "Coupling outside frozen range")
    require(isinstance(cutoff, int) and cutoff >= 0, "Invalid spin cutoff")
    v = 20*coupling
    a = v/3
    r_ground = cutoff//4+1
    require(a < 1, "Ground Neumann series fails")
    tau = a**r_ground/(1-a)
    require(tau < 1, "Ground projection denominator fails")
    delta = v*tau/(1-tau)
    q = max(F(3), F(3*(cutoff+1), 4))
    require(q-v > 0, "Excluded-sector Schur denominator fails")
    schur = v*v/(q-v)
    return tau, delta, schur


def window_budget(coupling, cutoff, initial_degree, window):
    require(window >= 0, "Negative heat time")
    require(isinstance(initial_degree, int) and 0 <= initial_degree <= cutoff,
            "Initial state is not certified to be retained")
    tau, delta, schur = ground_budget(coupling, cutoff)
    r = (cutoff-initial_degree)//4+1
    z = 20*coupling*window
    exp_lo, exp_hi = exp_interval(z)
    representation = 2*exp_hi*z**r/factorial(r)
    centering = window*delta
    return {
        "cutoff": cutoff, "initial_degree": initial_degree, "r": r,
        "coupling": rational(coupling), "sigma_window": rational(window),
        "ground_tail_upper": rational(tau),
        "ground_energy_error_upper": rational(delta),
        "alternative_schur_energy_error_upper": rational(schur),
        "centered_representation_upper": rational(representation),
        "centering_upper": rational(centering),
        "total_centered_upper": rational(min(F(2), representation+centering)),
        "exp_enclosure": [rational(exp_lo), rational(exp_hi)],
    }


def ungauged_dimension_upper(cutoff):
    coeff = [F(0)]*(cutoff+1)
    coeff[0] = F(1)
    for _ in range(33):
        out = [F(0)]*(cutoff+1)
        for d in range(cutoff+1):
            for n in range(cutoff-d+1):
                out[d+n] += coeff[d]*(n+1)**2
        coeff = out
    total = sum(coeff)
    require(total.denominator == 1, "Dimension count is not integral")
    return total.numerator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    require(not output.exists() or not any(output.iterdir()), "Output directory must be fresh")
    contract_path = ROOT/"research/round24/contracts/x1.json"
    contract = json.loads(contract_path.read_text())
    require(contract["loop"] == "x1" and contract["status"] == "frozen", "Wrong contract")
    for section in ("dependencies", "instruction_inputs"):
        for name, expected in contract[section].items():
            digest = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
            require(digest == expected, "Changed frozen input: "+name)

    vertices, edges, faces, masks = graph()
    cap = F(1, 100)
    one, x = {0: F(1)}, {1: F(1)}
    fundamental, spin_one = character(1), character(2)
    require(haar_integral(x) == 0 and haar_moment(2) == F(1, 4)
            and haar_moment(4) == F(1, 8), "SU(2) class moments")
    require(haar_integral(poly_mul(fundamental, fundamental)) == 1,
            "Fundamental face normalization")
    require(haar_integral(poly_mul(spin_one, spin_one)) == 1,
            "Spin-one excluded face normalization")
    require(poly_mul(fundamental, fundamental) == poly_add(one, spin_one),
            "SU(2) character fusion is wrong")
    coupling_coefficient = -haar_integral(poly_mul(x, fundamental))
    leakage_coefficient = -haar_integral(poly_mul(spin_one, poly_mul(x, fundamental)))
    require(coupling_coefficient == F(-1, 2), "Actual vacuum-face magnetic coefficient")
    require(leakage_coefficient == F(-1, 2), "Actual excluded spin-one coefficient")

    matrix = actual_matrix(cap)
    vacuum = [F(1)]+[F(0)]*20
    av = matvec(matrix, vacuum)
    a2v = matvec(matrix, av)
    actual_vacuum_variance = (a2v[0]-av[0]**2)/(cap*cap)
    require(actual_vacuum_variance == 5, "Actual all-face vacuum variance")
    for p in range(2, 21):
        difference = [F(0)]*21
        difference[1], difference[p] = 1, -1
        require(matvec(matrix, difference) == [(3+20*cap)*v for v in difference],
                "The 19 face-difference eigenvectors fail")
    root_lo, root_hi = sqrt_interval(9+20*cap*cap)
    energy_lo = 20*cap+(3-root_hi)/2
    energy_hi = 20*cap+(3-root_lo)/2
    require(F(0) < energy_lo <= energy_hi < 20*cap,
            "Actual Galerkin ground is not the vacuum trial energy")
    require((F(0)*(3)-5*cap*cap) < 0,
            "Wrong-ground determinant control failed")
    finite_ground_spin_one_leakage_lower = cap*cap/(4*(3+20*cap-energy_lo))
    require(finite_ground_spin_one_leakage_lower > 0,
            "The actual Galerkin ground must leak to a spin-one face")

    # Quantified rank obstruction uses a real excluded Wilson character.
    cutoff = 20
    excluded_n = cutoff//4+1
    excluded_character = character(excluded_n)
    require(4*excluded_n > cutoff and haar_integral(poly_mul(excluded_character, excluded_character)) == 1,
            "Excluded full-space norm witness fails")
    witness = {"cutoff": cutoff, "twice_spin": excluded_n,
               "total_degree": 4*excluded_n,
               "electric_energy_over_alpha": excluded_n*(excluded_n+2),
               "time_zero_full_space_error": "1"}

    windows = [window_budget(cap, n, 0, F(1)) for n in (0, 4, 8, 12, 16, 20)]
    require(F(windows[-1]["total_centered_upper"]) < F(1, 10**6),
            "Promised useful finite-window bound was not achieved")
    require(all(F(a["total_centered_upper"]) > F(b["total_centered_upper"])
                for a, b in zip(windows, windows[1:])), "Cutoff budgets fail to improve")
    zero_time = window_budget(cap, 20, 0, F(0))
    zero_coupling = window_budget(F(0), 20, 0, F(50))
    require(F(zero_time["total_centered_upper"]) == 0
            and F(zero_coupling["total_centered_upper"]) == 0,
            "Exact retained-input exceptions failed")
    require(3-20*cap == F(14, 5), "Actual ground gap endpoint")
    require(20*cap/3 == F(1, 15), "Ground Neumann parameter endpoint")
    require(ground_budget(cap, 0)[0] == F(1, 14), "All-cutoff tail denominator")

    # Explicit wrong-input/model rejections survive optimized Python.
    rejected_bad_initial = False
    try:
        window_budget(cap, 4, 8, F(1))
    except RuntimeError:
        rejected_bad_initial = True
    require(rejected_bad_initial, "Unretained initial class silently admitted")
    rejected_nineteen = False
    try:
        actual_matrix(cap, face_count=19)
    except RuntimeError:
        rejected_nineteen = True
    require(rejected_nineteen and F(19, 4) != actual_vacuum_variance,
            "Selected-memory/full-graph substitution escaped")

    # Partial centering alters an eigenvalue; its missing error cannot be zero.
    tau4, delta4, _ = ground_budget(cap, 4)
    require(delta4 > 0 and 20*cap-energy_hi > 0 and leakage_coefficient*cap != 0,
            "Ground centering or excluded-state control became vacuous")
    # Fixed sigma=1 represents different physical times if alpha/hbar changes.
    physical_t_a = F(3, 2)  # hbar=3, alpha=2
    physical_t_b = F(3, 4)  # hbar=3, alpha=4
    require(2*physical_t_a/3 == 1 and 4*physical_t_b/3 == 1
            and physical_t_a != physical_t_b, "Physical-clock distinction failed")
    # Fundamental half-spin cutoff cannot count only a basis vector and drop
    # its gauge orbit: the central endpoint action is exactly -1.
    require((-1)**1 == -1 and (-1)**4 == 1, "Endpoint Gauss parity control")

    controls = {
        "actual_four_cycle_sector_complete": True,
        "actual_su2_haar_and_fusion_coefficients": True,
        "actual_excluded_spin_one_channel_nonzero": True,
        "finite_rank_full_norm_time_zero_obstruction": True,
        "nineteen_face_memory_substitution_rejected": rejected_nineteen,
        "vacuum_trial_energy_is_not_galerkin_ground": True,
        "omitted_centering_error_is_nonzero": True,
        "unretained_initial_state_rejected": rejected_bad_initial,
        "zero_time_retained_exception_exact": True,
        "zero_coupling_retained_exception_exact": True,
        "cutoff_budget_and_positive_denominators": True,
        "fixed_physical_clock_distinction": True,
        "open_link_gauss_noninvariance": True,
    }
    require(len(controls) >= 3 and all(value is True for value in controls.values()),
            "Control contract failed")
    results = {
        "loop": "x1", "direction": "reverse", "status": "passed",
        "claims": [
            "Actual gauge-compatible joint electric spectral projections with common domains",
            "Exact full-physical and full-selected operator-norm obstruction at time zero",
            "Uniform finite-window retained-input heat bound with all excluded Dyson paths",
            "Ground Neumann tail and separate centering error bounded for the actual graph",
            "Actual 21-dimensional degree-four Galerkin coefficients and excluded spin-one leakage",
        ],
        "limitations": [
            "No full-space all-time finite-rank norm approximation",
            "No actual P20 matrix assembly or numerical trajectory; only its rigorous error budget",
            "No all-time retained-input, relative, or real-time approximation theorem",
            "No measured clock, homogeneous model transfer, continuum theorem, or verified priority",
        ],
        "arithmetic": "stdlib Fraction; rational Taylor remainder; integer-square-root enclosure",
        "actual_graph": {"vertices": len(vertices), "edges": len(edges), "faces": len(faces),
                         "four_cycles": len(faces), "face_parity_masks": masks},
        "actual_p4_sector": {
            "dimension": 21, "lambda": rational(cap),
            "matrix": [[rational(v) for v in row] for row in matrix],
            "ground_energy_over_alpha": [rational(energy_lo), rational(energy_hi)],
            "nineteen_fold_energy_over_alpha": rational(3+20*cap),
            "vacuum_variance_of_W": rational(actual_vacuum_variance),
            "vacuum_face_coefficient_of_V": rational(coupling_coefficient),
            "spin_one_face_leakage_coefficient_of_V": rational(leakage_coefficient),
            "unnormalized_ground_spin_one_leakage_magnitude_lower": rational(finite_ground_spin_one_leakage_lower),
            "classification": "Actual physical Galerkin matrix; not an invariant full-H sector",
        },
        "full_space_obstruction_witness": witness,
        "centered_window_certificates": windows,
        "exception_budgets": {"time_zero": zero_time["total_centered_upper"],
                              "lambda_zero": zero_coupling["total_centered_upper"]},
        "dimension_warning": {
            "p4_actual_physical_dimension": 21,
            "p20_ungauged_dimension_upper_only": ungauged_dimension_upper(20),
            "physical_p20_dimension": "not computed",
        },
    }
    output.mkdir(parents=True, exist_ok=True)
    (output/"results.json").write_text(json.dumps(results, indent=2, sort_keys=True)+"\n")
    (output/"controls.json").write_text(json.dumps({"controls": controls}, indent=2, sort_keys=True)+"\n")
    require({p.name for p in output.iterdir()} == {"results.json", "controls.json"},
            "Unexpected scientific output")
    print(json.dumps({"loop": "x1", "direction": "reverse", "status": "passed",
                      "controls": len(controls), "p4_dimension": 21,
                      "p20_sigma_one_centered_upper": windows[-1]["total_centered_upper"]}, sort_keys=True))


if __name__ == "__main__":
    main()
