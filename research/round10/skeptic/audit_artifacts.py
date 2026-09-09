"""Verify delivered stationary and continuum-parameter artifacts independently."""
from fractions import Fraction as F
from pathlib import Path
import ast
import csv
import hashlib
import json
import math
import sys

from audit_independent import verify_independently, bracket

HERE = Path(__file__).resolve().parent
SOLVER = HERE.parent / "solver" if (HERE.parent / "solver").is_dir() else HERE.parent / "ym10-solver"
OUT = SOLVER / "output"
checks = []


def gate(name, passed, details=None):
    checks.append({"name": name, "passed": bool(passed), "details": details})


def main():
    certs = json.loads((OUT / "stationary_certificates.json").read_text())
    gate("nonempty stationary certificate collection", len(certs) == 16)
    for i, c in enumerate(certs):
        gate(f"delivered rational certificate {i}", verify_independently(c),
             {"alpha": c["alpha"], "coupling": c["coupling"], "N": c["N"],
              "gap_interval": c["gap_interval"]})
    cover = json.loads((OUT / "continuous_range_certificate.json").read_text())
    centers = [F(x) for x in cover["centers"]]
    radius = F(cover["nearest_center_radius"])
    lipschitz = F(cover["gap_lipschitz_constant"])
    gate("exact declared centers, radius and Lipschitz contract",
         centers == [F(x) for x in (0, 2, 4, 6, 8, 10)] and radius == 1 and lipschitz == 2)
    cells = [[F(x) for x in pair] for pair in cover["cells"]]
    exact_cells = [[max(F(0), x-radius), min(F(10), x+radius)] for x in centers]
    gate("every coverage cell has proved radius", cells == exact_cells)
    gate("exact closed interval coverage", cells[0][0] == 0 and cells[-1][-1] == 10
         and all(a[1] >= b[0] for a, b in zip(cells, cells[1:])))
    lowers = []
    for center in centers:
        index = cover["certificate_index_by_center"][str(center)]
        c = certs[index]
        gate(f"coverage certificate identity center={center}",
             F(c["alpha"]) == 1 and F(c["coupling"]) == center)
        lowers.append(bracket(c["gap_interval"])[0])
    computed = min(lowers)-radius*lipschitz
    gate("uniform lower computed exactly", computed == F(cover["uniform_gap_lower"]))
    conservative = F(cover["conservative_uniform_gap_lower"])
    gate("simple bound is positive and conservative", 0 < conservative <= computed,
         {"proved_lower": str(computed), "advertised_lower": str(conservative)})
    gate("no unsupported field-theory scope in coverage",
         cover["scope"] == "alpha=1; single plaquette; coupling in closed [0,10]")

    with (OUT / "stationary_intervals.csv").open() as f:
        rows = list(csv.DictReader(f))
    gate("CSV count matches every exact certificate", len(rows) == len(certs))
    discrepancy = []
    for c, row in zip(certs, rows):
        lo, hi = bracket(c["gap_interval"])
        if (F(row["coupling"]) != F(c["coupling"]) or int(row["N"]) != c["N"]
            or float(lo) != float(row["gap_lower"]) or float(hi) != float(row["gap_upper"])):
            discrepancy.append([c["coupling"], c["N"]])
    gate("CSV is faithful floating display of exact endpoints", not discrepancy, discrepancy)

    with (OUT / "dynamic_history.csv").open() as f:
        history = list(csv.DictReader(f))
    gate("dynamic history contains all401 declared times", len(history) == 401)
    finite = all(math.isfinite(float(v)) for row in history for v in row.values())
    gate("dynamic raw history is finite", finite)
    derivative_protocol = []
    identity = []
    e0 = float(history[0]["energy"])
    for row in history:
        t = float(row["time"])
        derivative_protocol.append(abs(float(row["coupling"])-5*(1-math.cos(math.pi*t/2))))
        identity.append(abs(float(row["work_defect"])-(float(row["energy"])-e0-float(row["integrated_work"]))))
    gate("dynamic history follows declared coefficient", max(derivative_protocol) < 5e-15)
    gate("reported work defect uses raw independent work", max(identity) < 2e-15)
    summary = json.loads((OUT / "dynamic_summary.json").read_text())
    gate("dynamic summary matches history energy and work",
         float(summary["energy_change"]) == float(history[-1]["energy"])-e0 and
         float(summary["integrated_work"]) == float(history[-1]["integrated_work"]))
    gate("changing coefficient carries resolved external work", float(summary["energy_change"]) > 1)

    sources = []
    validation = json.loads((OUT / "validation.json").read_text())
    gate("producer validation includes evaluated gates", validation["status"] == "passed"
         and len(validation["gates"]) == validation["gate_count"] > 0
         and all(row["passed"] is True for row in validation["gates"]))
    gate("producer source freeze preserved", validation["source_hashes_before"] == validation["source_hashes_after"])
    for name, claimed in validation["source_hashes_after"].items():
        path = SOLVER / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        gate("executed producer hash " + name, claimed == actual)
    for path in (SOLVER / "certified_plaquette.py", SOLVER / "run_study.py"):
        data = path.read_bytes(); tree = ast.parse(data)
        sources.append({"file": str(path), "sha256": hashlib.sha256(data).hexdigest(),
                        "lines": len(data.splitlines()),
                        "functions": [{"name": node.name, "first": node.lineno, "last": node.end_lineno}
                                      for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]})
    result = {"status": "passed" if checks and all(x["passed"] for x in checks) else "failed",
              "check_count": len(checks), "checks": checks, "source_scope": sources,
              "artifact_hashes": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in sorted(OUT.glob("*.json"))}}
    (HERE / "artifact_audit.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "checks": len(checks),
                      "failures": [x["name"] for x in checks if not x["passed"]]}))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
