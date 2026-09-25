#!/usr/bin/env python3
"""BD1 obstruction coefficients (SU(3), SO(3): d omega(W^2)/d tau at 0 and the
second-order coefficient of omega(W); SU(5): the fourth-order coefficient of
omega(W)), recomputed independently by an exact finite-dimensional
Rayleigh-Schroedinger / Hellmann-Feynman calculation on the one-plaquette
model H_FG(G) = 32 C_2 - (tau/3) W.

Round33 sub-round 4, modern (Penrose/Feynman) lens, research assistant/coder
"assistant-4". **This script counts zero research loops. Nothing here is
evidence, a contract, a premise or a gate.** It never imports a producer
`check.py`. It reads only, as text/JSON, never executed:
  - `research/round33/contracts/bd1.json` (frozen convention);
  - `research/round33/forward/bd1/report.md` /`output/results.json` and
    `research/round33/reverse/bd1/report.md` / `output/results.json`
    (ADMITTED values and the producers' OWN closed-form formulas, quoted in
    this docstring for reference and comparison, never executed or copied
    into the computation below -- the computation here rebuilds the
    perturbation series from the finite-dimensional Hamiltonian, not from
    the producers' formulas);
  - `research/round33/advisor/bd1-gate.json` (gate headline, comparison).
`python-flint` (`fmpq` exact rationals, `arb` ball arithmetic) and `sympy`
(exact linear algebra and implicit power-series solving) are reused BY
IMPORT as independent, already-frozen open-source libraries.

**Method.** `H_FG(G)` acts on the class-function Hilbert space of `G`,
whose Peter-Weyl-orthonormal basis is the set of irreducible characters
`chi_lambda`, with `H_0 chi_lambda = 32 C_2(lambda) chi_lambda` and `W`
acting by character multiplication `(chi_F + chi_Fbar)/(2N)` (a "hopping"
operator between irreps related by tensoring with the fundamental or its
conjugate). Because the whole perturbation series for `omega(W)(tau)` and
`omega(W^2)(tau)` at the orders needed here provably lives inside a SMALL,
explicitly named finite subspace (justified below, group by group, from
first principles -- Pieri's rule, the SU(N) N-ality (mod N) selection rule,
and, for SU(N), a Young's-lattice sub-diagram argument), the exact ground
eigenvalue/eigenvector of `H_FG(G)` restricted to that finite subspace, as
an exact power series in `tau` (and, via an auxiliary coupling `mu W^2`,
in `mu`), reproduces the admitted Taylor coefficients exactly. The series
themselves are extracted by substituting a power-series ansatz for the
ground eigenvalue into the EXACT characteristic polynomial of the finite
matrix and solving order by order with `sympy` -- a purely mechanical
linear-algebra procedure, never the producers' closed-form shortcuts
(forward's Hellmann-Feynman/Wigner-2n+1 bracket, or the shared closed form
`d omega(W^2)/d tau = (2/3) E[W^3]/(32 C_F)`, `omega_2 = E[W^3]/(3(32C_F)^2)`
both reports independently state). Hellmann-Feynman itself
(`dE/dtau = -(1/3) omega(W)`, elementary calculus on the exact `H(tau)`, not
a producer-specific derivation) is the only textbook identity used to turn
eigenvalue Taylor coefficients into `omega(W)` Taylor coefficients; the
same trick with an auxiliary parameter (`dE/dmu|_{mu=0} = omega(W^2)`, for
`H(tau,mu) = H_0 - (tau/3) W + mu W^2`) avoids ever needing eigenVECTOR
perturbation theory to get `d omega(W^2)/d tau`.

**SU(3) and SU(5): the finite subspace is a closed ring.** For SU(N), `Fbar
= Lambda^{N-1}(F)` (the top-but-one exterior power of the fundamental), and
by Pieri's rule the ONLY representations directly reachable from
`Lambda^k(F)` by one application of `W` are `Lambda^{k+1}(F)` (via `chi_F`)
and `Lambda^{k-1}(F)` (via `chi_Fbar`) -- every OTHER Pieri term (a "hook"
partition, e.g. `Sym^2(F)` from `k=1`) is NOT itself directly coupled back
to any `Lambda^j(F)`, so it can only re-enter a return-to-vacuum amplitude
by later reaching a partition that is a SUB-DIAGRAM of the target
`Lambda^N(F) = trivial` -- and a hook or non-column partition can never be a
sub-diagram of a single column, so any path that steps off the column chain
contributes exactly zero to a return-to-vacuum amplitude of length <= N (a
direct consequence of the row-by-row monotonicity of Young's lattice under
single-box addition). Separately, giving each `chi_F`-step a "+1" and each
`chi_Fbar`-step a "-1" mod N (their N-ality), a length-n path can return to
N-ality 0 only if all n steps have the same sign (checked for n=3,5 in
`nality_selection_rule` below) -- so the two mechanisms together force every
contributing path onto the single "column chain"
`triv - Lambda^1 - ... - Lambda^{N-1} - triv`, an (N)-site RING with equal
Pieri-rule hopping weight `1/(2N)` on every edge (verified against
`E[W^2] = <triv|W^2|triv>` below) and site energies `32 C_2(Lambda^k)`,
`C_2(Lambda^k) = (k/(2N))(N^2+N-Nk-k)` (the standard SU(N) quadratic Casimir
of a single-column partition, derived from the general partition Casimir
formula `C_2(lambda) = (1/2)[sum_i lambda_i(lambda_i+N+1-2i) - |lambda|^2/N]`
and cross-checked against `C_2(Lambda^1) = C_F = (N^2-1)/(2N)` and the
`Lambda^k <-> Lambda^{N-k}` symmetry).

**SO(3): no N-ality protection (trivial centre), so the truncated tower
`l = 0..l_max` is checked EMPIRICALLY convergent** by rerunning at several
`l_max` and confirming the extracted coefficients are identical (reported
below), rather than relying on a selection-rule argument.

Run: `python3 -B obstruction_series.py`
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]

import flint  # noqa: E402
import sympy as sp  # noqa: E402

flint.ctx.prec = 300


def load_json(rel):
    return json.loads((ROOT / rel).read_text())


FWD = load_json("research/round33/forward/bd1/output/results.json")
REV = load_json("research/round33/reverse/bd1/output/results.json")
GATE = load_json("research/round33/advisor/bd1-gate.json")

ADMITTED_SU3 = {
    "d_omega_W2_dtau": FWD["cells"]["SU(3)"]["first_order_derivative_omega_W2"]["value"],
    "omega_2": FWD["cells"]["SU(3)"]["second_order_coefficient_omega_W"]["value"],
}
ADMITTED_SO3 = {
    "d_omega_W2_dtau": FWD["cells"]["SO(3)"]["first_order_derivative_omega_W2"]["value"],
    "omega_2": FWD["cells"]["SO(3)"]["second_order_coefficient_omega_W"]["value"],
}
ADMITTED_SU5_OMEGA4 = FWD["cells"]["SU(5)"]["fourth_order_coefficient_omega_W"]["value"]

assert GATE["accepted"]


# ---------------------------------------------------------------------------
# Generic exact finite-matrix perturbation solver (eigenvalue only, via the
# characteristic polynomial and an implicit power-series ansatz -- no
# eigenvectors, no hand-derived RS recursion, purely mechanical sympy algebra)
# ---------------------------------------------------------------------------
def bivariate_ground_series(H0diag, Wmat, order):
    """H(tau,mu) = diag(H0diag) - (tau/3) Wmat + mu Wmat^2.
    Returns {(i,j): c_ij} for the ground eigenvalue series
    E(tau,mu) = sum c_ij tau^i mu^j, 1<=i+j<=order, E(0,0)=0.
    H0diag[0] must be 0 (the reference/vacuum state)."""
    n = len(H0diag)
    assert H0diag[0] == 0
    tau, mu, x = sp.symbols("tau mu x")
    H0 = sp.diag(*H0diag)
    W2 = Wmat * Wmat
    H = H0 - sp.Rational(1, 3) * tau * Wmat + mu * W2
    charpoly = sp.expand((x * sp.eye(n) - H).det())

    idxs = [(i, j) for i in range(order + 1) for j in range(order + 1) if 1 <= i + j <= order]
    c = {ij: sp.symbols(f"c_{ij[0]}_{ij[1]}") for ij in idxs}
    xseries = sum(c[ij] * tau ** ij[0] * mu ** ij[1] for ij in idxs)

    solved = {}
    for deg in range(1, order + 1):
        expr = sp.expand(charpoly.subs(x, xseries))
        poly = sp.Poly(expr, tau, mu)
        eqns = [coeff for (ti, mj), coeff in poly.terms() if ti + mj == deg]
        unknowns = [c[ij] for ij in idxs if ij[0] + ij[1] == deg]
        eqns_sub = [sp.expand(e.subs(solved)) for e in eqns]
        sol = sp.solve(eqns_sub, unknowns, dict=True)
        assert len(sol) >= 1, f"no solution at degree {deg}"
        for k, v in sol[0].items():
            solved[k] = sp.nsimplify(v)
    return {ij: solved.get(c[ij], sp.Integer(0)) for ij in idxs}


def univariate_ground_series(H0diag, Wmat, order):
    """H(tau) = diag(H0diag) - (tau/3) Wmat. Returns [E_1,...,E_order]
    (ground eigenvalue Taylor coefficients, E_0=0 implicit)."""
    n = len(H0diag)
    assert H0diag[0] == 0
    tau, x = sp.symbols("tau x")
    H0 = sp.diag(*H0diag)
    H = H0 - sp.Rational(1, 3) * tau * Wmat
    charpoly = sp.expand((x * sp.eye(n) - H).det())
    c = sp.symbols(f"c1:{order + 1}")
    xseries = sum(c[k] * tau ** (k + 1) for k in range(order))
    solved = {}
    for deg in range(1, order + 1):
        expr = sp.expand(charpoly.subs(x, xseries))
        coeff = sp.expand(sp.Poly(expr, tau).nth(deg))
        unknown = c[deg - 1]
        eq = sp.expand(coeff.subs(solved))
        sol = sp.solve(eq, unknown)
        solved[unknown] = sp.nsimplify(sol[0])
    return [solved[c[k]] for k in range(order)]


# ---------------------------------------------------------------------------
# Casimir of Lambda^k(fundamental) for SU(N): derived from the general
# partition Casimir formula, cross-checked at k=1 against C_F.
# ---------------------------------------------------------------------------
def casimir_Lambda_k(N, k):
    return sp.Rational(k, 2 * N) * (N * N + N - N * k - k)


def nality_selection_rule(N, n_steps):
    """Confirm: among the 2^{n_steps} +-1 sign sequences (F-step:+1,
    Fbar-step:-1 mod N), only the all-+1 and all-(-1) sequences sum to a
    multiple of N -- the elementary fact that isolates the column chain for
    a length-n_steps closed path back to the vacuum."""
    surviving = [s for s in range(n_steps + 1) if (2 * s - n_steps) % N == 0]
    return surviving == [0, n_steps]


# ---------------------------------------------------------------------------
# SU(3): 3-state ring (triv, Lambda^1=F, Lambda^2=Fbar)
# ---------------------------------------------------------------------------
def su3_obstruction():
    N = 3
    assert nality_selection_rule(N, 3)
    C1 = casimir_Lambda_k(N, 1)
    C2 = casimir_Lambda_k(N, 2)
    assert C1 == sp.Rational(N * N - 1, 2 * N)  # = C_F, cross-check
    H0 = [sp.Integer(0), 32 * C1, 32 * C2]
    w = sp.Rational(1, 2 * N)
    W = sp.Matrix([[0, w, w], [w, 0, w], [w, w, 0]])

    # cross-check: <triv|W^2|triv> must equal the Haar second moment E[W^2]=1/18
    E_W2_check = w * w + w * w
    assert E_W2_check == sp.Rational(1, 18)

    res = bivariate_ground_series(H0, W, 3)
    E3 = res[(3, 0)]
    d_omega_W2_dtau = res[(1, 1)]  # = d^2E/(d tau d mu) at 0 = d omega(W^2)/d tau at 0
    omega_2 = sp.nsimplify(-9 * E3)  # c_2 = -3*3*E_3 (Hellmann-Feynman, c_m=-3(m+1)E_{m+1})
    return {
        "ring_energies_32C2": [str(32 * C1), str(32 * C2)],
        "ring_hop_weight": str(w),
        "E_W2_from_ring": str(E_W2_check),
        "d_omega_W2_dtau": str(d_omega_W2_dtau),
        "omega_2": str(omega_2),
    }


# ---------------------------------------------------------------------------
# SO(3): angular-momentum tower l=0..l_max, empirical truncation convergence
# ---------------------------------------------------------------------------
def so3_matrix(lmax):
    n = lmax + 1
    H0 = [sp.Rational(32 * l * (l + 1)) for l in range(n)]
    W = sp.zeros(n, n)
    for l in range(n):
        neighbors = [l + 1] if l == 0 else [l - 1, l, l + 1]
        for lp in neighbors:
            if 0 <= lp < n:
                W[l, lp] = sp.Rational(1, 3)
    return H0, W


def so3_obstruction():
    results = {}
    for lmax in (1, 2, 3, 4):
        H0, W = so3_matrix(lmax)
        res = bivariate_ground_series(H0, W, 3)
        E3 = res[(3, 0)]
        d_omega_W2_dtau = res[(1, 1)]
        omega_2 = sp.nsimplify(-9 * E3)
        results[str(lmax)] = {
            "d_omega_W2_dtau": str(d_omega_W2_dtau),
            "omega_2": str(omega_2),
        }
    values = list(results.values())
    converged = all(v == values[0] for v in values)
    return {
        "by_lmax": results,
        "truncation_converged_l1_through_l4": converged,
        "d_omega_W2_dtau": values[0]["d_omega_W2_dtau"],
        "omega_2": values[0]["omega_2"],
    }


# ---------------------------------------------------------------------------
# SU(5): 5-state ring (triv, Lambda^1..Lambda^4), eigenvalue-only, order 5
# ---------------------------------------------------------------------------
def su5_fourth_order():
    N = 5
    assert nality_selection_rule(N, 5)
    Cs = [casimir_Lambda_k(N, k) for k in range(1, 5)]
    assert Cs[0] == sp.Rational(N * N - 1, 2 * N)
    assert Cs[0] == Cs[3] and Cs[1] == Cs[2]  # Lambda^k <-> Lambda^{N-k} symmetry
    H0 = [sp.Integer(0)] + [32 * c for c in Cs]
    w = sp.Rational(1, 2 * N)
    n = 5
    W = sp.zeros(n, n)
    for a, b in [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0)]:
        W[a, b] = w
        W[b, a] = w
    coeffs = univariate_ground_series(H0, W, 5)
    E5 = coeffs[4]
    omega_4 = sp.nsimplify(-15 * E5)
    return {
        "ring_energies_32C2_Lambda1to4": [str(32 * c) for c in Cs],
        "ring_hop_weight": str(w),
        "E_coefficients_1to5": [str(e) for e in coeffs],
        "omega_4": str(omega_4),
    }


# ---------------------------------------------------------------------------
# Arb / mpmath numeric previews of each exact value
# ---------------------------------------------------------------------------
def arb_preview(frac_str):
    f = flint.fmpq(frac_str)
    return float(flint.arb(f))


def main():
    report = {
        "schema": "hnm-round33-modern-lens-assistant4-obstruction-series-v1",
        "status": "preview_and_crosscheck_only_zero_research_loops_not_a_contract_or_gate",
        "human_author": "Hruday N M (BUNZEEY)",
        "role": "modern (Penrose/Feynman) lens, research assistant/coder assistant-4",
        "round": 33,
        "subround": 4,
    }

    all_passed = True

    su3 = su3_obstruction()
    su3_pass_1 = flint.fmpq(su3["d_omega_W2_dtau"]) == flint.fmpq(ADMITTED_SU3["d_omega_W2_dtau"])
    su3_pass_2 = flint.fmpq(su3["omega_2"]) == flint.fmpq(ADMITTED_SU3["omega_2"])
    su3["admitted"] = ADMITTED_SU3
    su3["passed"] = su3_pass_1 and su3_pass_2
    su3["arb_preview"] = {
        "d_omega_W2_dtau": arb_preview(su3["d_omega_W2_dtau"]),
        "omega_2": arb_preview(su3["omega_2"]),
    }
    all_passed &= su3["passed"]
    report["SU(3)"] = su3

    so3 = so3_obstruction()
    so3_pass_1 = flint.fmpq(so3["d_omega_W2_dtau"]) == flint.fmpq(ADMITTED_SO3["d_omega_W2_dtau"])
    so3_pass_2 = flint.fmpq(so3["omega_2"]) == flint.fmpq(ADMITTED_SO3["omega_2"])
    so3["admitted"] = ADMITTED_SO3
    so3["passed"] = so3_pass_1 and so3_pass_2 and so3["truncation_converged_l1_through_l4"]
    so3["arb_preview"] = {
        "d_omega_W2_dtau": arb_preview(so3["d_omega_W2_dtau"]),
        "omega_2": arb_preview(so3["omega_2"]),
    }
    all_passed &= so3["passed"]
    report["SO(3)"] = so3

    su5 = su5_fourth_order()
    su5_pass = flint.fmpq(su5["omega_4"]) == flint.fmpq(ADMITTED_SU5_OMEGA4)
    su5["admitted"] = ADMITTED_SU5_OMEGA4
    su5["passed"] = su5_pass
    su5["arb_preview"] = {"omega_4": arb_preview(su5["omega_4"])}
    all_passed &= su5["passed"]
    report["SU(5)"] = su5

    report["all_passed"] = all_passed
    print(json.dumps(report, indent=1, default=str))
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
