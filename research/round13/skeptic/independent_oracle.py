"""Independent exact positive-series oracles; no producer imports.

These are deliberately derived from integer factorial series, rather than the
producer moment recurrence or its PSD witness construction.
"""
from fractions import Fraction as Q
from math import comb, factorial


def exact_q(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise TypeError('exact rational required')
    if isinstance(value, (int, Q)):
        return Q(value)
    if isinstance(value, str):
        return Q(value)
    raise TypeError('exact rational required')


def haar(n):
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError('nonnegative moment order required')
    return Q(0) if n % 2 else Q(comb(n, n // 2), (n // 2 + 1) * 4 ** (n // 2))


def _bessel_reduced_interval(nu, k, terms):
    """I_nu(k)/(k/2)^nu, term 0 through terms inclusive."""
    k = abs(exact_q(k))
    if k == 0:
        return Q(1, factorial(nu)), Q(1, factorial(nu))
    z = k * k / 4
    term = Q(1, factorial(nu))
    total = term
    for j in range(1, terms + 1):
        term *= z / (j * (j + nu))
        total += term
    first_omitted = term * z / ((terms + 1) * (terms + nu + 1))
    following_ratio = z / ((terms + 2) * (terms + nu + 2))
    if following_ratio >= 1:
        raise ValueError('series truncation too early for geometric tail')
    return total, total + first_omitted / (1 - following_ratio)


def bessel_mean_interval(kappa, terms=100):
    """Exact enclosure for I2(kappa)/I1(kappa); zero defined by limit."""
    k = exact_q(kappa)
    if k == 0:
        return Q(0), Q(0)
    lo1, hi1 = _bessel_reduced_interval(1, k, terms)
    lo2, hi2 = _bessel_reduced_interval(2, k, terms)
    a, b = abs(k) * lo2 / (2 * hi1), abs(k) * hi2 / (2 * lo1)
    return (a, b) if k > 0 else (-b, -a)


def haar_tilt_interval(kappa, order=1, terms=200):
    """Normalized tilted-Haar moment via independently bounded exp series."""
    k = exact_q(kappa)
    if k == 0:
        return haar(order), haar(order)
    a = abs(k)
    if a >= terms + 2:
        raise ValueError('series truncation too early for geometric tail')
    weights = [Q(1)]
    for j in range(1, terms + 1):
        weights.append(weights[-1] * a / j)
    numerator = sum((t * haar(order + j) for j, t in enumerate(weights)), Q(0))
    denominator = sum((t * haar(j) for j, t in enumerate(weights)), Q(0))
    # |haar moment|<=1, and successive exp-tail ratios only decrease.
    tail = weights[-1] * a / (terms + 1) / (1 - a / (terms + 2))
    lo, hi = numerator / (denominator + tail), (numerator + tail) / denominator
    return (lo, hi) if k > 0 or order % 2 == 0 else (-hi, -lo)


def intersects(a, b):
    return max(a[0], b[0]) <= min(a[1], b[1])


def independent_moments(kappa, order):
    """Affine recurrence, represented as constant/slope pairs, independent code."""
    k = exact_q(kappa)
    if k == 0:
        return [(haar(j), Q(0)) for j in range(order + 1)]
    data = [(Q(1), Q(0)), (Q(0), Q(1))]
    for n in range(order - 1):
        previous = data[n - 1] if n else (Q(0), Q(0))
        data.append(tuple(data[n][i] + (n * previous[i] - (n + 3) * data[n + 1][i]) / k for i in range(2)))
    return data[:order + 1]


def determinant(matrix):
    a = [list(map(Q, row)) for row in matrix]
    result = Q(1)
    for i in range(len(a)):
        p = next((j for j in range(i, len(a)) if a[j][i]), None)
        if p is None:
            return Q(0)
        if p != i:
            a[i], a[p] = a[p], a[i]
            result = -result
        pivot = a[i][i]
        result *= pivot
        for j in range(i + 1, len(a)):
            ratio = a[j][i] / pivot
            for col in range(i + 1, len(a)):
                a[j][col] -= ratio * a[i][col]
    return result


def all_principal_minors_psd(matrix):
    """Exhaustive small-matrix oracle, distinct from LDL witness extraction."""
    n = len(matrix)
    if any(len(row) != n for row in matrix):
        raise ValueError('square matrix required')
    if any(matrix[i][j] != matrix[j][i] for i in range(n) for j in range(n)):
        raise ValueError('symmetric matrix required')
    for mask in range(1, 1 << n):
        sub = [[matrix[i][j] for j in range(n) if mask >> j & 1] for i in range(n) if mask >> i & 1]
        if determinant(sub) < 0:
            return False
    return True
