"""Exact rational falsifiers for finite Yang--Mills verification inferences.

No Yang--Mills simulation is performed. These tests check the counterexamples
derived in advisor.md using arithmetic independent of the lattice implementation.
Run: python3 check_exact_counterexamples.py
"""
from fractions import Fraction as F
import argparse
import hashlib
import json
from pathlib import Path
import sys


class GateRecorder:
    """Required checks remain executable under Python optimization."""

    def __init__(self):
        self.records = []

    def require(self, condition, name):
        passed = bool(condition)
        self.records.append({"name": name, "status": "passed" if passed else "failed"})
        if not passed:
            raise RuntimeError("required exact gate failed: " + name)


def markov_counterexample(n, c=F(1, 2), delta=F(1, 4), gates=None):
    gates = GateRecorder() if gates is None else gates
    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("n must be an integer at least 2")
    if not 0 < c < 1 or not 0 < delta < 1-c:
        raise ValueError("require 0<c<1 and 0<delta<1-c")
    block = [[F(int(i == j)) for j in range(n)] for i in range(n)]
    for i in range(2):
        for j in range(2):
            block[i][j] = F(1, 2)
    p0 = [[(1-c)*block[i][j] + c/n for j in range(n)] for i in range(n)]
    w = [F(1), F(-1)] + [F(0)]*(n-2)
    diff = [[delta*w[i]*w[j]/2 for j in range(n)] for i in range(n)]
    p1 = [[p0[i][j]+diff[i][j] for j in range(n)] for i in range(n)]
    for label, p in (("p0", p0), ("p1", p1)):
        prefix = f"n={n}/{label}/"
        gates.require(all(sum(row) == 1 for row in p), prefix + "normalized_rows")
        gates.require(all(p[i][j] == p[j][i] for i in range(n) for j in range(n)),
                      prefix + "symmetric")
        gates.require(all(value > 0 for row in p for value in row),
                      prefix + "strictly_positive_entries")
    gates.require(all(sum(diff[i][j]*w[j] for j in range(n)) == delta*w[i]
                      for i in range(n)), f"n={n}/rank_one_eigenvector")
    gates.require(all(sum(diff[i][j] for j in range(n)) == 0 for i in range(n)),
                  f"n={n}/difference_preserves_constant")
    # Density kernels K=nP with respect to uniform probability on n atoms.
    product_l1 = sum(abs(value) for row in diff for value in row)/n
    schur_row = max(sum(abs(value) for value in row) for row in diff)
    gates.require(product_l1 == 2*delta/n, f"n={n}/exact_product_l1")
    gates.require(schur_row == delta, f"n={n}/exact_schur_row")
    return {"n": n, "operator_norm_exact": str(delta),
            "kernel_product_l1_exact": str(product_l1),
            "schur_sup_row_exact": str(schur_row),
            "operator_to_product_l1_ratio_exact": str(delta/product_l1)}


def scalar_ward_counterexample(beta, gates=None):
    gates = GateRecorder() if gates is None else gates
    # Equal point masses at +I and -I, with u_a=0.
    if beta <= 0:
        raise ValueError("the discriminating fixture uses positive beta")
    scalar_residual = sum((-3*beta*u0)/2 for u0 in (F(1), F(-1)))
    inserted_residual = sum((u0*u0)/4 for u0 in (F(1), F(-1)))
    gates.require(scalar_residual == 0, f"beta={beta}/false_scalar_ward_pass")
    gates.require(inserted_residual == F(1, 2), f"beta={beta}/inserted_SD_rejects")
    return {"beta": str(beta), "scalar_ward_residual": str(scalar_residual),
            "f_equals_u0_ua_SD_residual": str(inserted_residual)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("exact_counterexample_results.json"))
    parser.add_argument("--inject-failure", action="store_true",
                        help="deliberately fail a required gate before writing a result")
    args = parser.parse_args()
    gates = GateRecorder()
    if args.inject_failure:
        gates.require(False, "deliberately_injected_failure")
    markov = [markov_counterexample(n, gates=gates) for n in (2, 4, 8, 16, 32, 64)]
    ward = [scalar_ward_counterexample(beta, gates=gates)
            for beta in (F(1, 100), F(1, 12), F(1), F(10))]
    if not gates.records or not all(record["status"] == "passed" for record in gates.records):
        raise RuntimeError("no completed, nonempty successful exact verification record")
    results = {
        "status": "passed exact rational fixture checks",
        "scope": "counterexamples to two inference rules; no continuum or lattice mass-gap proof",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_optimization": sys.flags.optimize,
        "executed_gate_count": len(gates.records),
        "executed_gates": gates.records,
        "markov_kernels": markov,
        "false_ward_pass": ward,
    }
    args.output.write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps({key: results[key] for key in
                     ("status", "executed_gate_count", "source_sha256", "python_optimization")},
                     indent=2))


if __name__ == "__main__":
    main()
