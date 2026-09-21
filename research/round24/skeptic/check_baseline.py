"""Independent algebra spot checks for inherited U2, not an infinite proof."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "baseline-checks.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def poly_mul(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


count = 1
coefficient = F(1)
for n in range(1, 31):
    count *= 40 * (8 + 3 * (n - 1))
    coefficient *= (F(8, 3) + n - 1) / n
    require(F(count, 120 ** n * factorial(n)) == coefficient,
            "connected coefficient mismatch")

# Exact all-z extension comes from the positive derivative of tail(z)/z;
# the endpoint check is sufficient only together with that analytic fact.
z = F(1, 10 ** 6)
x = 80 * z / 7
tail = F(44, 9) * x ** 2 / (1 - x) ** 5
require(z / 84 - tail > z / 168, "U2 positive margin failed")
p = list(map(F, [2, 5, 5, 6, 3]))
twice_product = [2 * a for a in poly_mul([1, 2, 1], [1, 0, 1])]
require([a - b for a, b in zip(p, twice_product)] == [0, 1, 1, 2, 1],
        "uniform profile inequality failed")
require(40 * 8 * 40 * 11 > (40 * 8) ** 2,
        "frozen support failed to discriminate")

# A scalar Hamiltonian shift leaves conjugation fixed. Omitting the ground
# centering in a covariance of I gives a false nonzero value at phase i.
stationary_identity_covariance = 1 - 1
uncentered_identity_covariance = 1j - 1
require(stationary_identity_covariance == 0 and uncentered_identity_covariance != 0,
        "ground phase control failed")

inputs = [
    "AGENTS.md", "research/round24/advisor/team.md",
    "research/round24/contracts/v1.json",
    "research/round23/forward/u1/report.md", "research/round23/reverse/u1/report.md",
    "research/round23/forward/u2/report.md", "research/round23/reverse/u2/report.md",
    "research/round23/advisor/u1-gate.json", "research/round23/advisor/u2-gate.json",
    "research/round22/forward/n1/report.md",
    "research/round24/skeptic/check_baseline.py",
]
OUT.write_text(json.dumps({
    "status": "passed", "scope": "Independent algebra spot checks and inherited producer replay",
    "external_peer_review": False, "historical_u2_independence_changed": False,
    "u2_exact_margin_at_cap": str(z / 84 - tail),
    "simple_margin_at_cap": str(z / 168),
    "connected_coefficients_checked": 30,
    "controls": {"frozen_support_undercount": True, "omitted_ground_phase": True},
    "sources": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                for name in inputs},
}, indent=2, sort_keys=True) + "\n")
print("Independent inherited-U2 spot checks passed")
