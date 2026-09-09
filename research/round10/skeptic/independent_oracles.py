"""Independent exact dense inertia and radial-form references.

This file imports no production solver. Rational congruence is used in place of
the production tridiagonal Sturm sequence. Floating radial integration is an
independent normalization check, not an interval proof.
"""
from fractions import Fraction as F
import math
import numpy as np


def dense_inertia(matrix):
    """Return (negative, zero, positive) via exact symmetric congruences."""
    a = [[F(x) for x in row] for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a):
        raise ValueError("square matrix required")
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        raise ValueError("symmetric matrix required")
    neg = zero = pos = 0
    while a:
        n = len(a)
        pivots = [i for i in range(n) if a[i][i] != 0]
        if pivots:
            pivot = max(pivots, key=lambda i: abs(a[i][i]))
            order = [pivot] + [i for i in range(n) if i != pivot]
            a = [[a[i][j] for j in order] for i in order]
            d = a[0][0]
            neg += int(d < 0)
            pos += int(d > 0)
            a = [[a[i][j] - a[i][0] * a[0][j] / d
                  for j in range(1, n)] for i in range(1, n)]
            continue
        pair = next(((i, j) for i in range(n) for j in range(i + 1, n)
                     if a[i][j]), None)
        if pair is None:
            zero += n
            break
        i, j = pair
        order = [i, j] + [k for k in range(n) if k not in (i, j)]
        a = [[a[i][j] for j in order] for i in order]
        off = a[0][1]
        neg += 1
        pos += 1
        a = [[a[i][j] - (a[i][0] * a[1][j] + a[i][1] * a[0][j]) / off
              for j in range(2, n)] for i in range(2, n)]
    return neg, zero, pos


def rational_hamiltonian(alpha, lam, count, delta=F(0)):
    alpha, lam, delta = F(alpha), F(lam), F(delta)
    if isinstance(count, bool) or not isinstance(count, int) or count < 2:
        raise ValueError("integer count >=2 required")
    if alpha <= 0 or lam < 0 or delta < 0:
        raise ValueError("positive alpha and nonnegative lambda/delta required")
    a = [[F(0) for _ in range(count)] for _ in range(count)]
    for n in range(count):
        a[n][n] = alpha * n * (n + 2) + lam
        if n:
            a[n][n - 1] = a[n - 1][n] = -lam / 2
    a[-1][-1] -= delta
    return a


def shifted_inertia(matrix, x):
    x = F(x)
    shifted = [row[:] for row in matrix]
    for i in range(len(shifted)):
        shifted[i][i] -= x
    return dense_inertia(shifted)


def verifies_bracket(matrix, index, lower, upper):
    """Closed enclosure using strict count at lower, nonstrict count at upper."""
    lower, upper = F(lower), F(upper)
    if lower > upper or not 0 <= index < len(matrix):
        return False
    below_l, equal_l, _ = shifted_inertia(matrix, lower)
    below_u, equal_u, _ = shifted_inertia(matrix, upper)
    return below_l <= index and below_u + equal_u > index


def radial_form_matrix(alpha, lam, count, nodes=160):
    """Direct quadrature of a Dirichlet radial kinetic/potential quadratic form."""
    z, w = np.polynomial.legendre.leggauss(nodes)
    theta = (z + 1) * math.pi / 2
    weight = w * math.pi / 2
    indices = np.arange(1, count + 1)[:, None]
    norm = math.sqrt(2 / math.pi)
    psi = norm * np.sin(indices * theta)
    derivative = norm * indices * np.cos(indices * theta)
    kinetic = (derivative * weight) @ derivative.T - (psi * weight) @ psi.T
    potential = (psi * (weight * (1 - np.cos(theta)))) @ psi.T
    return alpha * kinetic + lam * potential


def radial_fd_energies(alpha, lam, nodes):
    """Second-order Dirichlet finite differences, kept separate from certificates."""
    from scipy.linalg import eigvalsh_tridiagonal
    spacing = math.pi / (nodes + 1)
    theta = np.arange(1, nodes + 1) * spacing
    diagonal = 2 * alpha / spacing**2 - alpha + lam * (1 - np.cos(theta))
    off = np.full(nodes - 1, -alpha / spacing**2)
    return eigvalsh_tridiagonal(diagonal, off, select="i", select_range=(0, 1))
