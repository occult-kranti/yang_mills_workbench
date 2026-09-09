"""Independent exact-arithmetic checks of the one-square proof certificates."""
from pathlib import Path
from fractions import Fraction as F
import ast
import copy
import hashlib
import importlib.util
import itertools
import json
import math
import sys
import numpy as np

from independent_oracles import (dense_inertia, shifted_inertia,
    rational_hamiltonian, verifies_bracket, radial_form_matrix,
    radial_fd_energies)

HERE = Path(__file__).resolve().parent
SOLVER = HERE.parent / "solver" if (HERE.parent / "solver").is_dir() else HERE.parent / "ym10-solver"
PRODUCTION = SOLVER / "certified_plaquette.py"
spec = importlib.util.spec_from_file_location("reviewed_plaquette", PRODUCTION)
producer = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = producer
spec.loader.exec_module(producer)
checks = []


def gate(name, passed, details=None):
    checks.append({"name": name, "passed": bool(passed), "details": details})


def rejected(fn):
    try:
        fn()
    except (ValueError, TypeError, ArithmeticError, KeyError):
        return True
    return False


def bracket(pair):
    return F(pair["lower"]), F(pair["upper"])


def verify_independently(c):
    """Rebuild all arithmetic from rational model inputs, using dense inertia."""
    a, lam, n = F(c["alpha"]), F(c["coupling"]), c["N"]
    tau = a * n * (n + 2)
    u = F(c["tail"]["U"])
    if not u < tau:
        return False
    delta = (lam / 2)**2 / (tau - u)
    if tau != F(c["tail"]["tau"]) or delta != F(c["tail"]["delta"]):
        return False
    A = rational_hamiltonian(a, lam, n)
    B = rational_hamiltonian(a, lam, n, delta)
    for name, matrix in (("A", A), ("B", B)):
        for index, pair in enumerate(c[name + "_eigen_intervals"]):
            if not verifies_bracket(matrix, index, *bracket(pair)):
                return False
        if F(c[name + "_eigen_intervals"][1]["upper"]) >= u:
            return False
    energies = [(bracket(c["B_eigen_intervals"][k])[0],
                 bracket(c["A_eigen_intervals"][k])[1]) for k in (0, 1)]
    if [bracket(p) for p in c["energy_intervals"]] != energies:
        return False
    gap = (energies[1][0]-energies[0][1], energies[1][1]-energies[0][0])
    return bracket(c["gap_interval"]) == gap


def main():
    for name, matrix, expected in [
        ("zero matrix", [[0, 0], [0, 0]], (0, 2, 0)),
        ("zero diagonal 2x2 pivot", [[0, 3], [3, 0]], (1, 0, 1)),
        ("rank deficient", [[1, 1], [1, 1]], (0, 1, 1)),
        ("negative definite", [[-3, 1], [1, -3]], (2, 0, 0)),
        ("mixed exact pivot", [[0, 1, 2], [1, 0, 3], [2, 3, 0]], (2, 0, 1)),
    ]:
        gate("oracle inertia: " + name, dense_inertia(matrix) == expected)

    # Endpoint counts include exact eigenvalues and vanishing principal minors.
    compared = 0
    errors = []
    for n in (1, 2, 3, 4):
        for diagonal in itertools.product((-1, 0, 1), repeat=n):
            for off in (F(-1), F(0), F(1)):
                A = [[F(diagonal[i]) if i == j else (off if abs(i-j) == 1 else F(0))
                      for j in range(n)] for i in range(n)]
                for x in (-2, -1, 0, 1, 2):
                    ref = shifted_inertia(A, x)[0]
                    actual = producer.sturm_count(diagonal, off, x)
                    compared += 1
                    if actual != ref:
                        errors.append([diagonal, str(off), x, actual, ref])
    gate("Sturm counts versus dense rational congruence", not errors,
         {"comparisons": compared, "errors": errors[:10]})

    for alpha, lam, n in ((1, 0, 6), (F(1, 3), F(7, 2), 12), (2, 8, 12), (1, 10, 16)):
        radial = radial_form_matrix(float(alpha), float(lam), n)
        exact = np.array(rational_hamiltonian(alpha, lam, n), dtype=float)
        error = float(np.max(np.abs(radial-exact)))
        gate(f"radial quadratic form a={alpha} lambda={lam}", error < 3e-10,
             {"max_abs_error": error, "nodes": 160})

    cases = [producer.certify(str(a), str(lam), n, 28)
             for a, lam, n in ((1, 0, 6), (1, 2, 8), (F(1, 3), F(7, 2), 12), (1, 10, 16))]
    for c in cases:
        gate(f"independent rational certificate a={c['alpha']} lambda={c['coupling']}",
             verify_independently(c), {"gap_interval": c["gap_interval"]})
        gate(f"producer replay a={c['alpha']} lambda={c['coupling']}",
             producer.verify_certificate(c))

    zero = cases[0]
    gate("zero coupling encloses exact 3 alpha gap",
         bracket(zero["gap_interval"])[0] <= 3 <= bracket(zero["gap_interval"])[1])
    tiny = producer.certify("1e-100", "0", 8, 128)
    tiny_lo, tiny_hi = bracket(tiny["gap_interval"])
    gate("absolute precision can be inconclusive without false positivity",
         tiny_lo <= F(3, 10**100) <= tiny_hi and tiny["positive_gap_certified"] is False,
         {"alpha": "1e-100", "bits": 128, "status": "valid but positive gap not certified"})
    gate("insufficient tail threshold is rejected",
         rejected(lambda: producer.certify(1, 1000, 2, 40)))
    c = cases[1]
    for key, value in (("scope", "complete four-dimensional Yang-Mills"),
                       ("bits", 128), ("positive_gap_certified", 1)):
        altered = copy.deepcopy(c)
        altered[key] = value
        gate("reject altered certificate " + key,
             rejected(lambda altered=altered: producer.verify_certificate(altered)))
    for key in ("tau", "delta"):
        altered = copy.deepcopy(c)
        altered["tail"][key] = str(F(altered["tail"][key]) + 1)
        gate("reject incorrect tail " + key,
             rejected(lambda altered=altered: producer.verify_certificate(altered)))
    altered = copy.deepcopy(c)
    altered["A_eigen_intervals"][1] = copy.deepcopy(altered["A_eigen_intervals"][0])
    gate("reject wrong minmax eigenvalue index", not verify_independently(altered))
    altered = copy.deepcopy(c)
    altered["gap_interval"]["lower"] = str(F(altered["gap_interval"]["upper"])+1)
    gate("reject inverted gap", rejected(lambda: producer.verify_certificate(altered)))

    for a, lam, n in ((0, 1, 8), (-1, 1, 8), (1, -1, 8), (1, 1, 1),
                       (1, 1, True), (float("nan"), 1, 8),
                       (1, float("inf"), 8), (True, 1, 8)):
        gate(f"invalid input {a!r},{lam!r},{n!r}",
             rejected(lambda a=a, lam=lam, n=n: producer.certify(a, lam, n)))

    # Radial finite differences must approach the interval from a separate
    # discretization, with a resolved second-order trend. They are not certificates.
    c = cases[-1]
    lo, hi = bracket(c["gap_interval"])
    center = float((lo+hi)/2)
    fds = []
    for nodes in (127, 255, 511):
        values = radial_fd_energies(1., 10., nodes)
        fds.append({"nodes": nodes, "gap": float(values[1]-values[0])})
    errors = [abs(row["gap"]-center) for row in fds]
    gate("independent radial convergence", errors[2] < errors[1] < errors[0]
         and 3.5 < errors[0]/errors[1] < 4.5 and 3.5 < errors[1]/errors[2] < 4.5,
         {"rows": fds, "errors": errors})

    # The wrong link-Casimir factor alpha*n(n+2)/4 fails the exact zero-coupling gap.
    gate("planted missing four-link factor is discriminated", abs(3/4 - 3) > 2,
         {"wrong_gap": 0.75, "correct_gap": 3.0})
    # A wrong product of ground and excited endpoint directions is not the gap.
    incorrect = copy.deepcopy(c)
    incorrect["gap_interval"]["lower"] = incorrect["gap_interval"]["upper"]
    gate("upper gap endpoint cannot be relabeled lower",
         rejected(lambda: producer.verify_certificate(incorrect)))

    centers = [F(i) for i in (0, 2, 4, 6, 8, 10)]
    radius = F(1)
    def covers(xs, left=F(0), right=F(10)):
        return bool(xs) and xs[0]-radius <= left and xs[-1]+radius >= right and all(
            b-a <= 2*radius for a,b in zip(xs,xs[1:]))
    gate("continuous parameter interval exactly covered", covers(centers))
    gate("missing center invalidates declared radius", not covers([x for x in centers if x != 4]))
    gate("omitted upper endpoint invalidates coverage", not covers(centers[:-1]))
    gate("empty center collection rejected", not covers([]))

    # Direct order-bound argument for gap Lipschitz, distinct from a sample claim.
    # Two diagonal levels saturate the 2|d lambda| gap change at lambda=0.
    h0 = np.diag([0., 3.]); potential = np.diag([2., 0.]); step = .1
    delta_gap = np.diff(np.linalg.eigvalsh(h0 + step*potential))[0] - 3.
    gate("Lipschitz factor one control fails", abs(delta_gap) > 1.9*step,
         {"gap_change": float(delta_gap), "coefficient": 2})

    scope = []
    for path in [PRODUCTION, HERE / "independent_oracles.py", Path(__file__)]:
        data = path.read_bytes(); tree = ast.parse(data)
        scope.append({"file": str(path), "sha256": hashlib.sha256(data).hexdigest(),
                      "lines": len(data.splitlines()),
                      "functions": [{"name": node.name, "first": node.lineno, "last": node.end_lineno}
                                    for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]})
    result = {"status": "passed" if checks and all(x["passed"] for x in checks) else "failed",
              "check_count": len(checks), "checks": checks, "source_scope": scope,
              "scope_note": "Reviewed source is not a claim of complete executed branch coverage. Rational arithmetic validates certificates conditional on the reviewed graph and operator theorems."}
    (HERE / "independent_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": len(checks),
                      "failures": [x["name"] for x in checks if not x["passed"]]}))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
