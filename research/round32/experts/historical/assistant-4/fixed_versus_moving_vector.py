#!/usr/bin/env python3
"""
fixed_versus_moving_vector.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 4.

Zero research loops: test/planning fixture for the historical
(Newton/Tesla) lens's Round32 assistant package (assistant-4), not a
producer, skeptic or advisor artifact. Does not import
research/round32/forward/ay1/check.py or research/round32/reverse/
ay1/check.py.

Task (panel-update-3.md item 6, historical share, test 2). A small
exact fixture (Fractions) illustrating the AY1 control "fixed-vector
versus moving-vector": a sequence of vectors psi_N = psi_out + delta_N
with delta_N -> delta ALONG A SUBSEQUENCE ONLY, showing:
  (a) the reduced-density bound 2eps(1+eps)/(1+eps^2) holds for every N
      (this is the AV1-admitted D-bound formula, HNM-AY1's D, applied
      per finite vector, not the doubled "2D" pairwise bound);
  (b) two different subsequential limits can differ by up to the bound
      while each is within it of the product (the reference state P);
  (c) "a common enclosing interval is not equality" -- both limits lie
      in the same D-ball around P yet are not equal to each other, nor
      to P.

This is the fixture behind the forward AY1 report's own control
`fixed_vector_versus_moving_vector_example` and
`common_enclosing_interval_not_equality`, and behind the "subsequence
versus whole sequence" control (an alternating sequence whose parity
subsequences converge, but which itself does not); it is built fresh
here (2 qubits: an "R" register and an "out" register), independent of
and smaller than the forward/reverse fixtures, and is explicitly
labelled a FIXTURE throughout, not a physical result.

Construction. Let Omega=|0>_R x |0>_out (the product reference vector,
P=|Omega><Omega|, P_R=|0><0|_R). For a unit vector (a,b) with
a^2+b^2=1 (rational, via the standard rational parametrisation of the
circle a_t=(1-t^2)/(1+t^2), b_t=2t/(1+t^2), t rational) and a fixed
small eps, put

    delta(a,b) = eps*( a|1>_R|0>_out + b|0>_R|1>_out ),   psi(a,b) =
    (Omega + delta(a,b)) / sqrt(1+eps^2)      (psi_out := Omega/sqrt(1+eps^2)
                                                is absorbed; delta is
                                                orthogonal to Omega, so
                                                this normalization is
                                                exact).

Define, for N=1,2,3,...:
    t_N = 1/N     (t_N -> 0 as N -> infinity, strictly decreasing),
    delta_N = delta(+a_{t_N}, b_{t_N})   if N even  (-> direction (+1,0)),
    delta_N = delta(-a_{t_N}, b_{t_N})   if N odd   (-> direction (-1,0)).

The whole sequence delta_N does not converge (consecutive terms
alternate between the neighbourhoods of (+1,0) and (-1,0) in the (a,b)
plane, and the squared distance between consecutive terms does not
shrink to 0 -- it grows towards 4, the squared distance between the
two limit points), but each parity SUBSEQUENCE converges (exactly,
monotonically, and rationally) to a fixed limit vector:
delta_even -> eps*(1,0), delta_odd -> eps*(-1,0).

All reduced densities and their trace norms are computed exactly:
rho_R(a,b) - P_R is a traceless 2x2 real-symmetric matrix, whose trace
norm is 2*sqrt(-det); since -det is a nonnegative Fraction, comparing
trace norms is done by comparing SQUARES (both sides nonnegative), so
every comparison in this script is an exact Fraction inequality -- no
square root is ever taken as a floating step in a pass/fail check (a
float sqrt is shown only as a human-readable decimal preview).

Run with: python3 -B fixed_versus_moving_vector.py
"""
import json
import sys
from fractions import Fraction as F


def circle_point(t):
    """Rational point on the unit circle: a=(1-t^2)/(1+t^2), b=2t/(1+t^2)."""
    a = (1 - t ** 2) / (1 + t ** 2)
    b = (2 * t) / (1 + t ** 2)
    assert a ** 2 + b ** 2 == 1
    return a, b


def rho_R(a, b, eps):
    """
    2x2 (R-register) reduced density of psi=(Omega+delta)/sqrt(1+eps^2),
    delta=eps*(a|1>_R|0>_out + b|0>_R|1>_out), a^2+b^2=1, Omega=|00>.
    Derivation (exact, by hand, reproduced in the module docstring/
    README): write psi=|0>_out x (|0>+eps a|1>)_R/norm + |1>_out x
    (eps b|0>)_R/norm, trace out "out".
    """
    n2 = 1 + eps ** 2
    return [
        [(1 + eps ** 2 * b ** 2) / n2, (eps * a) / n2],
        [(eps * a) / n2, (eps ** 2 * a ** 2) / n2],
    ]


P_R = [[F(1), F(0)], [F(0), F(0)]]


def sub(M, Nm):
    return [[M[i][j] - Nm[i][j] for j in range(2)] for i in range(2)]


def det2(M):
    return M[0][0] * M[1][1] - M[0][1] * M[1][0]


def trace_of(M):
    return M[0][0] + M[1][1]


def trace_norm_sq_traceless(M):
    """
    For a real-symmetric traceless 2x2 matrix [[-d,c],[c,d]], the
    eigenvalues are +-sqrt(d^2+c^2), so the trace norm is 2 sqrt(d^2+c^2)
    = 2 sqrt(-det(M)) (since det = -d^2-c^2). Returns (trace_norm)^2,
    an exact nonnegative Fraction, and asserts tracelessness.
    """
    tr = trace_of(M)
    assert tr == 0, "expected a traceless matrix, got trace %s" % tr
    dt = det2(M)
    assert dt <= 0
    return -4 * dt


def matrices_equal(M, Nm):
    return all(M[i][j] == Nm[i][j] for i in range(2) for j in range(2))


def main():
    eps = F(1, 10)  # small parameter for the fixture; not physical tau

    D = 2 * eps * (1 + eps) / (1 + eps ** 2)
    D_sq = D ** 2
    twoD = 2 * D
    twoD_sq = twoD ** 2

    # ---- General per-N bound (item a): for EVERY rational (a,b) on the
    # unit circle, ||rho_R(a,b)-P_R||_1 <= D. Verified exactly (squared
    # comparison) at a battery of N values covering both subsequences.
    per_N_records = []
    N_values = list(range(1, 13))
    limit_by_parity = {"even": None, "odd": None}
    deltas_ab = {}
    for N in N_values:
        t = F(1, N)
        a_t, b_t = circle_point(t)
        if N % 2 == 0:
            a, b = a_t, b_t          # -> (+1, 0)
        else:
            a, b = -a_t, b_t         # -> (-1, 0)
        deltas_ab[N] = (a, b)
        rho = rho_R(a, b, eps)
        diff = sub(rho, P_R)
        tsq = trace_norm_sq_traceless(diff)
        holds = tsq <= D_sq
        per_N_records.append({
            "N": N,
            "parity": "even" if N % 2 == 0 else "odd",
            "t_N": str(t),
            "a_N": str(a), "b_N": str(b),
            "trace_norm_sq_rho_minus_P": str(tsq),
            "trace_norm_decimal_preview": float(tsq) ** 0.5,
            "D_bound_holds": holds,
        })

    all_per_N_hold = all(r["D_bound_holds"] for r in per_N_records)

    # ---- Subsequential limits (exact, at t=0): delta_even -> eps*(1,0),
    # delta_odd -> eps*(-1,0). These are the actual (exact) limit
    # points, not just large-N previews.
    rho_even_limit = rho_R(F(1), F(0), eps)
    rho_odd_limit = rho_R(F(-1), F(0), eps)

    diff_even = sub(rho_even_limit, P_R)
    diff_odd = sub(rho_odd_limit, P_R)
    tsq_even = trace_norm_sq_traceless(diff_even)
    tsq_odd = trace_norm_sq_traceless(diff_odd)

    each_within_D_of_product = (tsq_even <= D_sq) and (tsq_odd <= D_sq)

    diff_limits = sub(rho_even_limit, rho_odd_limit)
    tsq_diff_limits = trace_norm_sq_traceless(diff_limits)
    limits_within_2D = tsq_diff_limits <= twoD_sq
    limits_not_equal = not matrices_equal(rho_even_limit, rho_odd_limit)

    # "up to the bound": report how close the realized separation comes
    # to 2D (a ratio, decimal preview only -- the pass/fail above is
    # exact).
    ratio_to_2D_decimal = (float(tsq_diff_limits) ** 0.5) / (float(twoD_sq) ** 0.5)
    ratio_each_to_D_decimal = (float(tsq_even) ** 0.5) / (float(D_sq) ** 0.5)

    # ---- (c) "a common enclosing interval is not equality": both
    # limits lie in the SAME closed trace-norm ball of radius D around
    # P_R (a common enclosing interval, in the AW2/AV1 enclosure sense),
    # yet rho_even_limit != rho_odd_limit != P_R. This is the exact
    # control the forward AY1 report calls
    # `common_enclosing_interval_not_equality`.
    common_ball_but_not_equal = bool(
        (tsq_even <= D_sq) and (tsq_odd <= D_sq)
        and not matrices_equal(rho_even_limit, rho_odd_limit)
        and not matrices_equal(rho_even_limit, P_R)
        and not matrices_equal(rho_odd_limit, P_R)
    )

    # ---- "delta_N -> delta along a subsequence only" / "subsequence
    # versus whole sequence": the FULL sequence does not converge (the
    # (a,b) points do not settle down: even/odd terms stay a fixed
    # distance apart, bounded below), while each parity subsequence
    # does converge exactly to its limit (the distance to the limit,
    # measured in the (a,b) plane, strictly decreases and -> 0).
    def ab_dist_sq(p, q):
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

    dist_to_own_limit = []
    for N in N_values:
        a, b = deltas_ab[N]
        target = (F(1), F(0)) if N % 2 == 0 else (F(-1), F(0))
        dist_to_own_limit.append({
            "N": N,
            "dist_sq_to_own_parity_limit": str(ab_dist_sq((a, b), target)),
        })
    # strictly decreasing within each parity class (monotone convergence)
    even_ds = [F(r["dist_sq_to_own_parity_limit"]) for r in dist_to_own_limit if r["N"] % 2 == 0]
    odd_ds = [F(r["dist_sq_to_own_parity_limit"]) for r in dist_to_own_limit if r["N"] % 2 == 1]
    even_decreasing = all(even_ds[i] > even_ds[i + 1] for i in range(len(even_ds) - 1))
    odd_decreasing = all(odd_ds[i] > odd_ds[i + 1] for i in range(len(odd_ds) - 1))

    consecutive_gap_sq = [
        {"N": N, "N+1": N + 1, "dist_sq_ab_N_to_Np1": str(ab_dist_sq(deltas_ab[N], deltas_ab[N + 1]))}
        for N in N_values[:-1]
    ]
    # consecutive (even,odd) pairs stay near distance^2 = 4 (i.e. near
    # the (1,0)-to-(-1,0) separation), NOT shrinking to 0: the whole
    # sequence does not converge.
    whole_sequence_gap_min = min(F(r["dist_sq_ab_N_to_Np1"]) for r in consecutive_gap_sq)
    # Bounded away from 0 throughout (in fact increasing towards 4 = the
    # squared (a,b)-plane distance between the two limit points (1,0)
    # and (-1,0)): the whole sequence has no single limit, only two
    # subsequential ones.
    whole_sequence_does_not_converge = whole_sequence_gap_min > F(1, 5)

    overall_pass = bool(
        all_per_N_hold
        and each_within_D_of_product
        and limits_within_2D
        and limits_not_equal
        and common_ball_but_not_equal
        and even_decreasing
        and odd_decreasing
        and whole_sequence_does_not_converge
    )

    result = {
        "script": "fixed_versus_moving_vector.py",
        "zero_research_loops": True,
        "label": "FIXTURE ONLY -- 2-qubit (R x out) toy model, eps=1/10 is illustrative, not tau; not a physical result",
        "arithmetic": "fractions.Fraction throughout; trace norms compared via their exact squares (traceless 2x2 real-symmetric matrix => trace_norm^2=-4*det); floats appear only as decimal previews",
        "setup": {
            "Omega": "|0>_R x |0>_out",
            "P_R": [[str(x) for x in row] for row in P_R],
            "eps": str(eps),
            "D_2eps_1pluseps_over_1pluseps2": str(D),
            "D_decimal": float(D),
            "twoD": str(twoD),
            "twoD_decimal": float(twoD),
        },
        "item_a_per_N_density_bound": {
            "records": per_N_records,
            "all_N_satisfy_D_bound": all_per_N_hold,
        },
        "item_b_two_subsequential_limits": {
            "even_limit_direction": "(a,b) -> (1,0)  [delta_even -> eps*(1,0)]",
            "odd_limit_direction": "(a,b) -> (-1,0) [delta_odd -> eps*(-1,0)]",
            "rho_even_limit": [[str(x) for x in row] for row in rho_even_limit],
            "rho_odd_limit": [[str(x) for x in row] for row in rho_odd_limit],
            "trace_norm_sq_even_minus_P": str(tsq_even),
            "trace_norm_sq_odd_minus_P": str(tsq_odd),
            "each_within_D_of_product": each_within_D_of_product,
            "ratio_each_to_D_decimal_preview": ratio_each_to_D_decimal,
            "trace_norm_sq_even_minus_odd": str(tsq_diff_limits),
            "limits_within_2D_of_each_other": limits_within_2D,
            "ratio_separation_to_2D_decimal_preview": ratio_to_2D_decimal,
            "limits_not_equal": limits_not_equal,
        },
        "item_c_common_enclosing_interval_not_equality": {
            "both_limits_in_D_ball_around_P": each_within_D_of_product,
            "rho_even_limit_equals_rho_odd_limit": matrices_equal(rho_even_limit, rho_odd_limit),
            "rho_even_limit_equals_P": matrices_equal(rho_even_limit, P_R),
            "rho_odd_limit_equals_P": matrices_equal(rho_odd_limit, P_R),
            "common_ball_but_not_equal": common_ball_but_not_equal,
        },
        "subsequence_versus_whole_sequence": {
            "dist_to_own_parity_limit_by_N": dist_to_own_limit,
            "even_subsequence_strictly_approaches_its_limit": even_decreasing,
            "odd_subsequence_strictly_approaches_its_limit": odd_decreasing,
            "consecutive_N_to_N+1_gap_in_ab_plane": consecutive_gap_sq,
            "whole_sequence_gap_min_sq": str(whole_sequence_gap_min),
            "whole_sequence_does_not_converge": whole_sequence_does_not_converge,
        },
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
