#!/usr/bin/env python3
"""Independent exact SU(2) two-holonomy Haar oracle, round14 loop1.

Primary implementation: tensor-power characters followed by Schur convolution.
Comparator: quaternion angular averaging, independently derived in backward.md.
No project moment implementation is imported.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import comb
from pathlib import Path
import hashlib
import json
import sys


def degree(n):
    if isinstance(n, bool) or not isinstance(n, int) or not 0 <= n <= 256:
        raise ValueError("degree must be an integer in [0,256], excluding bool")
    return n


def character_coefficients(a):
    """x**a = sum_r coefficients[r] chi_r(U), dim chi_r = r+1."""
    return _character_coefficients(degree(a))


@lru_cache(maxsize=None)
def _character_coefficients(a):
    result = []
    for j in range(a // 2 + 1):
        multiplicity = comb(a, j) - (comb(a, j - 1) if j else 0)
        result.append((a - 2 * j, Q(multiplicity, 2**a)))
    return tuple(result)


def haar_moment(a, b, c):
    """Exact E[(Tr U/2)^a (Tr V/2)^b (Tr UV/2)^c]."""
    # Validate before memoization: bool/int cache-key aliasing must not pass.
    return _haar_moment(degree(a), degree(b), degree(c))


@lru_cache(maxsize=None)
def _haar_moment(a, b, c):
    cb, cc = dict(character_coefficients(b)), dict(character_coefficients(c))
    return sum((ar * cb.get(r, 0) * cc.get(r, 0) / (r + 1)
                for r, ar in character_coefficients(a)), Q(0))


def one_haar(n):
    degree(n)
    if n % 2:
        return Q(0)
    j = n // 2
    return Q(comb(2 * j, j), (j + 1) * 4**j)


def weighted_one_haar(power, radial_power):
    degree(power)
    degree(radial_power)
    if power + 2 * radial_power > 256:
        raise ValueError("expanded angular degree exceeds 256")
    return sum(((-1)**j * comb(radial_power, j) * one_haar(power + 2*j)
                for j in range(radial_power + 1)), Q(0))


def angle_moment(a, b, c):
    """Independent z=xy-sqrt(1-x²)sqrt(1-y²)t, t uniform[-1,1]."""
    degree(a); degree(b); degree(c)
    return sum((Q(comb(c, j), j + 1)
                * weighted_one_haar(a + c - j, j // 2)
                * weighted_one_haar(b + c - j, j // 2)
                for j in range(0, c + 1, 2)), Q(0))


def chi_polynomial(r):
    """Chebyshev U_r in ascending rational coefficients, separate recurrence."""
    degree(r)
    prev, cur = [Q(1)], [Q(0), Q(2)]
    if r == 0:
        return prev
    for _ in range(1, r):
        nxt = [Q(0)] + [2*t for t in cur]
        for i, v in enumerate(prev):
            nxt[i] -= v
        prev, cur = cur, nxt
    return cur


def run_tests():
    checks = []

    def record(name, condition, details=None):
        if not condition:
            raise RuntimeError("failed: " + name)
        checks.append({"name": name, "passed": True, "details": details})

    fixtures = {(0,0,0): Q(1), (1,0,0): Q(0), (2,0,0): Q(1,4),
                (1,1,1): Q(1,16), (2,2,0): Q(1,16),
                (2,2,2): Q(1,48), (4,0,0): Q(1,8)}
    for abc, expected in fixtures.items():
        record("hand fixture " + str(abc), haar_moment(*abc) == expected)

    for a in range(25):
        expanded = [Q(0)] * (a + 1)
        for r, coefficient in character_coefficients(a):
            for i, value in enumerate(chi_polynomial(r)):
                expanded[i] += coefficient * value
        record("character polynomial identity degree " + str(a),
               expanded == [Q(0)] * a + [Q(1)])

    comparison_count = 0
    parity_count = 0
    for a in range(10):
        for b in range(10):
            for c in range(10):
                value = haar_moment(a,b,c)
                if value != angle_moment(a,b,c):
                    raise RuntimeError("independent angle disagreement " + str((a,b,c)))
                if value != haar_moment(c,a,b) or value != haar_moment(b,a,c):
                    raise RuntimeError("permutation disagreement")
                if not (a % 2 == b % 2 == c % 2):
                    parity_count += 1
                    if value != 0:
                        raise RuntimeError("center parity violation")
                comparison_count += 1
    record("independent quaternion comparison", True, {"monomials": comparison_count})
    record("permutation symmetry", True, {"monomials": comparison_count})
    record("independent center-parity zeros", True, {"monomials": parity_count})

    # Discriminating wrong formula: omission of Schur dimension denominator.
    wrong_xyz = Q(1,2)**3
    record("dimension-factor mutation rejected", wrong_xyz != haar_moment(1,1,1),
           {"wrong": str(wrong_xyz), "correct": str(haar_moment(1,1,1))})
    # Explicitly warm caches before challenging bool/int aliasing.
    haar_moment(1,0,0)
    invalid = [True, False, -1, 257, Q(1), 1.0, "1", None]
    for v in invalid:
        rejected = False
        try:
            haar_moment(v,0,0)
        except ValueError:
            rejected = True
        record("invalid degree rejected " + repr(v), rejected)

    # Derivative at all-zero source: the third cumulant reduces to E[xyz].
    record("Haar mixed response is 1/16", haar_moment(1,1,1) == Q(1,4)**2)
    # The exact eta family has E[x² y²]=(1+2 E[z²])/24;
    # test every Taylor coefficient through order 16 without normalization.
    for n in range(17):
        record("special-family fourth moment coefficient " + str(n),
               haar_moment(2,2,n) == (one_haar(n) + 2*one_haar(n+2))/24)
        record("special-family covariance coefficient " + str(n),
               haar_moment(1,1,n) == one_haar(n+1)/4)
    return checks


def main():
    checks = run_tests()
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "output"
    out.mkdir(parents=True, exist_ok=True)
    result = {"schema": "ym14-backward-character-oracle-v1", "status": "passed",
              "phase": "loop1", "check_count": len(checks), "checks": checks,
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "method": "exact tensor-power character expansion and Schur convolution",
              "independent_comparator": "exact quaternion angular average; no project oracle import",
              "scope": "normalized product Haar SU(2)^2 monomials; no spectral claim"}
    (out / "oracle_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "check_count": len(checks),
                      "comparison_monomials": 1000}))


if __name__ == "__main__":
    main()
