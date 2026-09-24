#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 2, assistant-2 script 2 of 3: one-plaquette
sign-convention fixture.

Pre-registration test only (`update-1.md` section 5, item 2; the calling task).
Counts zero research loops; not a producer, contract, gate or skeptical review.
Human project author: Hruday N M (BUNZEEY); AI-assisted.

Model (a finite graph; `model_is_finite_graph: true`, `transfers_to_aq: false` --
this is NOT an AQ-state result and is never read as one): the gauge-invariant
Hilbert space of a single SU(2) plaquette, in the character basis {chi_j(U)},
truncated at j<=1/2 (2 states: j=0,1/2) and, separately, at j<=1 (3 states:
j=0,1/2,1). Basis index t=0,1,2,... stands for 2j (so j=t/2, and half-integers
stay integers).

  * Free ("electric") part: H_0 |t> = 4*j(j+1) |t> = t(t+2) |t> (exact integer
    Casimir eigenvalues in "alpha units"; j=1/2 -> 3, matching the AW1-admitted
    "energy 3 in alpha units" gap used throughout this round).
  * Wilson operator: W = (1/2) Tr(U) = (1/2) chi_{1/2}(U). Multiplying an
    irreducible character by chi_{1/2} is the SU(2) branching rule
    chi_{1/2}*chi_j = chi_{j+1/2} + chi_{j-1/2} (Clebsch-Gordan, exact,
    coefficient 1); since {chi_j} is Haar-orthonormal, W's matrix elements in
    this basis are <t|W|t+-1> = 1/2, all other entries 0 (a real symmetric
    tridiagonal matrix with a zero diagonal).
  * Perturbation, under I1.5 (`phi_b=-(tau/3) sum W_f`; for the single face here
    the per-face creation-convention coefficient reproducing the AW1-admitted
    first-order coefficient +tau/144 on the j<=1/2 two-level truncation is
    V(tau) = -(tau/24) W -- re-derived below from second-order Rayleigh-Ritz, not
    asserted): H(tau) = H_0 + V(tau) = H_0 - (tau/24) W.
  * Centre-parity operator: Z = diag((-1)^t). Z is unitary, self-inverse, and
    satisfies Z H_0 Z = H_0 (Z is diagonal, H_0 is diagonal) and Z W Z = -W
    exactly (Z flips the sign of every entry connecting t and t+-1, since
    (-1)^t*(-1)^(t+1) = -1, for any truncation): this is the one-plaquette
    analogue of the AW1 flip lemma's U_E, and it gives
    Z H(tau) Z = H_0 - (tau/24)(-W) = H(-tau) EXACTLY, at any truncation level,
    not just perturbatively.

Checks (exact `fractions.Fraction` arithmetic only; no floats decide anything):

  1. Structural identity Z H_0 Z = H_0 and Z W Z = -W, as exact matrix equalities,
     at both truncations (j<=1/2, n=2; j<=1, n=3).
  2. Rayleigh-Schroedinger series of the ground-state mean <W>(tau), to order 5,
     at both truncations: the first-order coefficient is exactly +1/144
     (matching the AW1 gate), the zeroth-order term is exactly 0 (the Haar
     reference), and every even-order term (0,2,4) is exactly 0 -- the series is
     odd, which is what Z H(tau) Z = H(-tau) implies for <W>(tau) (ground-state
     mean commutes with the flip: <W>(-tau) = -<W>(tau)).
  3. sign(<W>(tau)) = sign(tau) at first order: evaluated at tau=+-10^-8 (the
     AW1/AW2 cap) using the order-5 truncated series, at both j_max truncations.
  4. Antisymmetry of <W> under tau -> -tau: evaluated exactly from the same
     series (odd function => W(-tau)=-W(tau) to every computed order), at both
     truncations, plus the exact structural proof of item 1 (Z-conjugation),
     which holds beyond the truncated series.
  5. Damaging-mutation controls: an even first-order coefficient, a wrong-sign
     coupling, and a non-antisymmetric perturbation are each rejected.

Usage: python3 -B sign_convention_fixture.py
"""
import sys
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common2 as K  # noqa: E402

TAU_CAP = Q(1, 10 ** 8)
COUPLING_COEFFICIENT = Q(-1, 24)   # V(tau) = COUPLING_COEFFICIENT * tau * W


# ---------------------------------------------------------------------------
# Finite matrices over Fraction (no numpy; this is a 2x2 / 3x3 fixture).
# ---------------------------------------------------------------------------
def zeros(n, m=None):
    m = n if m is None else m
    return [[Q(0)] * m for _ in range(n)]


def matmul(a, b):
    n, k, m = len(a), len(b), len(b[0])
    out = zeros(n, m)
    for i in range(n):
        for j in range(m):
            out[i][j] = sum(a[i][t] * b[t][j] for t in range(k))
    return out


def madd(a, b, scale_b=Q(1)):
    return [[a[i][j] + scale_b * b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mscale(s, a):
    return [[Q(s) * v for v in row] for row in a]


def mat_eq(a, b):
    return a == b


def one_plaquette(n):
    """Gauge-invariant one-plaquette space truncated to n states t=0..n-1
    (j=t/2). Returns (H0, W, Z)."""
    h0 = [[Q(t * (t + 2)) if i == t else Q(0) for i in range(n)] for t in range(n)]
    w = zeros(n)
    for t in range(n - 1):
        w[t][t + 1] = w[t + 1][t] = Q(1, 2)
    z = [[Q((-1) ** t) if i == t else Q(0) for i in range(n)] for t in range(n)]
    return h0, w, z


def check_flip_structure(n, label):
    h0, w, z = one_plaquette(n)
    zh0z = matmul(matmul(z, h0), z)
    zwz = matmul(matmul(z, w), z)
    neg_w = mscale(-1, w)
    K.require(mat_eq(zh0z, h0), '%s: Z H0 Z != H0' % label)
    K.require(mat_eq(zwz, neg_w), '%s: Z W Z != -W' % label)
    # Damaging mutation: an even-|f cap E| analogue (Z replaced by identity) must
    # NOT reproduce the flip identity (a positive control that the check is not
    # vacuous).
    ident = [[Q(1) if i == j else Q(0) for j in range(n)] for i in range(n)]

    def trivial_flip_claim():
        trivial = matmul(matmul(ident, w), ident)
        K.require(mat_eq(trivial, neg_w), 'identity is not a flip: I W I == -W is false, as required')
    rejected_trivial = K.expect_rejected(trivial_flip_claim)
    return {'ZH0Z_equals_H0': True, 'ZWZ_equals_negW': True,
            'trivial_operator_correctly_fails_to_flip': rejected_trivial}


# ---------------------------------------------------------------------------
# Exact Rayleigh-Schroedinger series of the ground-state expectation of W.
# ---------------------------------------------------------------------------
def rs_series_of_W(n, order=5):
    """Exact RS series of <psi(tau)|W|psi(tau)>/<psi(tau)|psi(tau)> in powers of
    tau, for H(tau) = H0 + tau*COUPLING_COEFFICIENT*W, ground state at tau=0 is
    the n-dim basis vector t=0 (nondegenerate: h0 diag is strictly increasing)."""
    h0, w, _ = one_plaquette(n)
    h0diag = [h0[t][t] for t in range(n)]
    K.require(all(h0diag[i] > h0diag[0] for i in range(1, n)), 'nondegenerate ground required')
    v = mscale(COUPLING_COEFFICIENT, w)   # the tau-linear perturbation, per unit tau

    psis = [[Q(1)] + [Q(0)] * (n - 1)]
    energies = [Q(h0diag[0])]
    for k in range(1, order + 1):
        vp = [sum(v[i][j] * psis[k - 1][j] for j in range(n)) for i in range(n)]
        energies.append(vp[0])
        new = [Q(0)] * n
        for i in range(1, n):
            acc = -vp[i] + sum(energies[m] * psis[k - m][i] for m in range(1, k))
            new[i] = acc / (h0diag[i] - h0diag[0])
        psis.append(new)

    def ip(u, m, x):
        return sum(u[i] * sum(m[i][j] * x[j] for j in range(n)) for i in range(n))

    ident = [[Q(1) if i == j else Q(0) for j in range(n)] for i in range(n)]
    num = [sum(ip(psis[a], w, psis[k - a]) for a in range(k + 1)) for k in range(order + 1)]
    den = [sum(ip(psis[a], ident, psis[k - a]) for a in range(k + 1)) for k in range(order + 1)]
    out = []
    for k in range(order + 1):
        out.append((num[k] - sum(den[m] * out[k - m] for m in range(1, k + 1))) / den[0])
    return out   # out[k] is the coefficient of tau^k in <W>(tau)


def eval_series(series, tau):
    tau = Q(tau)
    total = Q(0)
    p = Q(1)
    for c in series:
        total += c * p
        p *= tau
    return total


def sign_of(q):
    if q > 0:
        return 1
    if q < 0:
        return -1
    return 0


def run_truncation(n, label, order=5):
    struct = check_flip_structure(n, label)
    series = rs_series_of_W(n, order=order)

    even_zero = all(series[k] == 0 for k in range(0, order + 1, 2))
    first_order_ok = series[1] == Q(1, 144)

    w_plus = eval_series(series, TAU_CAP)
    w_minus = eval_series(series, -TAU_CAP)
    sign_match_plus = sign_of(w_plus) == sign_of(TAU_CAP) == 1
    sign_match_minus = sign_of(w_minus) == sign_of(-TAU_CAP) == -1
    antisymmetric = w_minus == -w_plus

    # Damaging mutations.
    def even_first_order_claim():
        K.require(series[1] == Q(0), 'mutation: claiming the first-order coefficient is 0 (it is +1/144)')
    rej_even = K.expect_rejected(even_first_order_claim)

    def wrong_sign_coupling_claim():
        wrong_series = rs_series_of_W_with_coefficient(n, -COUPLING_COEFFICIENT, order=order)
        K.require(sign_of(eval_series(wrong_series, TAU_CAP)) == 1,
                  'wrong-sign coupling: sign(<W>) at tau>0 is not +1 under the flipped-sign convention')
    rej_wrong_sign = K.expect_rejected(wrong_sign_coupling_claim)

    def non_antisymmetric_claim():
        K.require(w_minus == w_plus, 'mutation: claiming <W>(-tau) == <W>(+tau) (it is -<W>(+tau))')
    rej_non_anti = K.expect_rejected(non_antisymmetric_claim)

    return {
        'truncation': label, 'n_states': n, 'order': order,
        'series_coefficients': [K.s(c) for c in series],
        'first_order_coefficient_is_plus_1_over_144': first_order_ok,
        'even_order_coefficients_all_zero': even_zero,
        'W_at_plus_cap': K.s(w_plus), 'W_at_minus_cap': K.s(w_minus),
        'sign_W_plus_cap_is_plus1': sign_match_plus, 'sign_W_minus_cap_is_minus1': sign_match_minus,
        'antisymmetric_W_minus_tau_equals_minus_W_plus_tau': antisymmetric,
        'structural_flip_identity': struct,
        'rejected_even_first_order_claim': rej_even,
        'rejected_wrong_sign_coupling_claim': rej_wrong_sign,
        'rejected_non_antisymmetric_claim': rej_non_anti,
        'passed': (first_order_ok and even_zero and sign_match_plus and sign_match_minus and antisymmetric),
    }


def rs_series_of_W_with_coefficient(n, coefficient, order=5):
    h0, w, _ = one_plaquette(n)
    h0diag = [h0[t][t] for t in range(n)]
    v = mscale(coefficient, w)
    psis = [[Q(1)] + [Q(0)] * (n - 1)]
    energies = [Q(h0diag[0])]
    for k in range(1, order + 1):
        vp = [sum(v[i][j] * psis[k - 1][j] for j in range(n)) for i in range(n)]
        energies.append(vp[0])
        new = [Q(0)] * n
        for i in range(1, n):
            acc = -vp[i] + sum(energies[m] * psis[k - m][i] for m in range(1, k))
            new[i] = acc / (h0diag[i] - h0diag[0])
        psis.append(new)

    def ip(u, m, x):
        return sum(u[i] * sum(m[i][j] * x[j] for j in range(n)) for i in range(n))
    ident = [[Q(1) if i == j else Q(0) for j in range(n)] for i in range(n)]
    num = [sum(ip(psis[a], w, psis[k - a]) for a in range(k + 1)) for k in range(order + 1)]
    den = [sum(ip(psis[a], ident, psis[k - a]) for a in range(k + 1)) for k in range(order + 1)]
    out = []
    for k in range(order + 1):
        out.append((num[k] - sum(den[m] * out[k - m] for m in range(1, k + 1))) / den[0])
    return out


def run():
    j_half = run_truncation(2, 'j<=1/2 (2 states: j=0,1/2)')
    j_one = run_truncation(3, 'j<=1 (3 states: j=0,1/2,1)')

    # Monotone-convergence cross-check (bonus, not required by the calling task's
    # literal spec but corroborates update-1.md sec.5 item 2's j_max in {1/2,1,3/2}
    # wording): a third truncation j<=3/2 should agree with the first two on the
    # first-order coefficient (a structural fact: only the two states t=0,1
    # contribute at first order in RS perturbation theory) and preserve the
    # oddness/sign properties.
    j_three_half = run_truncation(4, 'j<=3/2 (4 states: j=0,1/2,1,3/2) [bonus check]')
    first_order_matches_across_truncations = (
        j_half['series_coefficients'][1] == j_one['series_coefficients'][1]
        == j_three_half['series_coefficients'][1] == K.s(Q(1, 144)))

    items = [
        {'item': 'flip_and_series_j_le_half', 'passed': j_half['passed'], 'detail': j_half},
        {'item': 'flip_and_series_j_le_one', 'passed': j_one['passed'], 'detail': j_one},
        {'item': 'monotone_convergence_bonus_j_le_three_half', 'passed': j_three_half['passed'],
         'detail': j_three_half},
        {'item': 'first_order_coefficient_stable_across_truncations',
         'passed': first_order_matches_across_truncations,
         'detail': {'j_le_half': j_half['series_coefficients'][1], 'j_le_one': j_one['series_coefficients'][1],
                    'j_le_three_half': j_three_half['series_coefficients'][1]}},
    ]

    result = {
        'id': 'sign_convention_fixture',
        'role': 'pre-registration test; zero research loops; one-plaquette exact fixture',
        'model_is_finite_graph': True,
        'transfers_to_aq': False,
        'graph_name': 'one_plaquette_character_truncation',
        'convention': 'I1.5 (phi_b=-(tau/3) sum W_f); single-face coupling V(tau)=-(tau/24) W re-derived here '
                       'from second-order Rayleigh-Ritz to reproduce the AW1-admitted first-order coefficient '
                       '+tau/144 on the j<=1/2 truncation, then reused unchanged at j<=1 and (bonus) j<=3/2',
        'tau_cap_evaluated': K.s(TAU_CAP),
        'items': items,
    }
    result['pass'] = all(it['passed'] for it in items)
    return result


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'sign_convention_fixture', result)
    print('sign_convention_fixture: %s' % ('PASS' if result['pass'] else 'FAIL'))
    for it in result['items']:
        print('   [%s] %s' % ('x' if it['passed'] else ' ', it['item']))
    if not result['pass']:
        sys.exit(1)


if __name__ == '__main__':
    main()
