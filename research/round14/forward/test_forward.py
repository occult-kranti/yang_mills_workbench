"""Executed diagnostics and adversarial controls for the loop-1 forward model.

Uses explicit gates, also under python -O. Passing comparisons are floating
diagnostics; the accompanying conventional derivations carry exact claims.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import scipy

from forward_model import (MOMENT_NAMES, conditional, direct_moments,
                           marginal_moments, radial_coefficients,
                           single_loop, special_family)

HERE = Path(__file__).resolve().parent


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    source_bytes = (HERE / "forward_model.py").read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    checks = []

    def gate(name, passed, **detail):
        passed = bool(passed)
        checks.append({"name": name, "status": "passed" if passed else "failed", **detail})
        if not passed:
            (out / "failed_checks.json").write_text(json.dumps(checks, indent=2) + "\n")
            raise RuntimeError(f"failed gate: {name}")

    def reject(name, call):
        try:
            call()
        except (ValueError, ArithmeticError):
            gate(name, True)
        else:
            gate(name, False)

    def distance(a, b):
        return max(abs(a[k] - b[k]) for k in MOMENT_NAMES)

    for bad in (True, np.bool_(False), float("nan"), float("inf"), -float("inf"),
                "1", 101, -101, 1+0j, None):
        for axis in range(3):
            params = [0, 0, 0]
            params[axis] = bad
            reject(f"invalid parameter axis {axis}: {type(bad).__name__} {str(bad)}",
                   lambda p=params: marginal_moments(*p))
    for bad in (True, np.bool_(True), 3, 513, 8.0, "8", float("nan")):
        reject(f"invalid marginal nodes {type(bad).__name__} {bad}",
               lambda b=bad: marginal_moments(0, 0, 0, b))
    for bad in (True, 3, 129, 8.0):
        reject(f"invalid direct nodes {type(bad).__name__} {bad}",
               lambda b=bad: direct_moments(0, 0, 0, b))
    for bad in (True, -1, 201, float("nan")):
        reject(f"invalid h {bad}", lambda b=bad: radial_coefficients(b))
    for bad in (True, -1.0001, 1.0001, float("nan")):
        reject(f"invalid conjugacy x {bad}", lambda b=bad: conditional(b, 1, 1))
    reject("unrepresentably large real parameter", lambda: marginal_moments(10**500,0,0))
    reject("special-family eta domain retained", lambda: special_family(101))
    gate("derived single-loop field 199 is admissible", math.isfinite(single_loop(199)["mean"]))

    sigma = (np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),
             np.array([[1,0],[0,-1]],complex))
    def matrix(q):
        return q[0]*np.eye(2)+1j*sum((q[i+1]*sigma[i] for i in range(3)),np.zeros((2,2),complex))
    quaternion_cases = [((1,0,0,0),(3/5,4/5,0,0)),
                        ((-1,0,0,0),(3/5,0,4/5,0)),
                        ((3/5,4/5,0,0),(5/13,12/13,0,0)),
                        ((3/5,4/5,0,0),(5/13,0,12/13,0)),
                        ((0,0,0,1),(0,0,0,-1))]
    for qa,qb in quaternion_cases:
        x,y=qa[0],qb[0]
        z=x*y-np.dot(qa[1:],qb[1:])
        u,v=matrix(qa),matrix(qb)
        residual=abs(np.trace(u@v)/2-z)
        inverse_z=float(np.real(np.trace(u@v.conj().T))/2)
        gate(f"independent complex-matrix trace and geometry {qa,qb}",
             residual<1e-14 and (z-x*y)**2 <= (1-x*x)*(1-y*y)+1e-14 and
             abs(z+inverse_z-2*x*y)<1e-14,trace_residual=float(residual))
    qa,qb=quaternion_cases[2]
    actual=float(np.real(np.trace(matrix(qa)@matrix(qb)))/2)
    gate("wrong relative-orientation deletion is discriminated", abs(actual-qa[0]*qb[0])>.7)
    gate("wrong normalized-trace factor is discriminated", abs(2*actual-actual)>.5)

    log_z, t, r = radial_coefficients(0)
    gate("removable h zero exact float limits", log_z == 0 and t == .25 and r == 1/24)
    for h in (1e-200, 1e-12, 1e-6, .499999999, .5, .500000001, 1, 100, 200):
        lz, t, r = radial_coefficients(h)
        gate(f"radial coefficients finite positive {h}",
             all(math.isfinite(q) for q in (lz, t, r)) and lz >= 0 and t > 0 and r > 0)
        if h >= .1:
            gate(f"independent Bessel recurrence {h}", abs(4*t+h*h*r-1) < 2e-14,
                 residual=abs(4*t+h*h*r-1))
    for x, k2, eta in ((1, 100, -100), (-1, 100, 100), (1, -100, 100), (-1, -100, -100)):
        c = conditional(x, k2, eta)
        gate(f"central zero field {x,k2,eta}",
             c["h"] == 0 and c["y"] == 0 and c["z"] == 0 and
             c["yy"] == .25 and c["zz"] == .25 and c["yz"] == x/4)
    for x in (-1.0, 1.0, np.nextafter(-1.0, 0.0), np.nextafter(1.0, 0.0)):
        c = conditional(float(x), 100, -100 if x > 0 else 100)
        gate(f"near central cancellation {x}",
             c["h"] >= 0 and max(abs(c[k]) for k in ("y", "z", "yy", "zz", "yz")) <= 1)
    for x in (-1, 1):
        for k2, eta in ((1, 2), (-3, 2), (100, -99)):
            c = conditional(x, k2, eta)
            one = single_loop(k2 + eta*x)
            gate(f"central holonomy z=x y {x,k2,eta}",
                 max(abs(c["y"]-one["mean"]), abs(c["z"]-x*one["mean"]),
                     abs(c["yy"]-one["second"]), abs(c["zz"]-one["second"]),
                     abs(c["yz"]-x*one["second"])) < 3e-14)

    cases = [(0,0,0), (1,2,0), (-1,2,0), (5,-3,0), (100,-100,0),
             (0,0,1), (0,0,-5), (0,2,1), (1,2,1), (1,1,.25), (-1,2,1), (1,-2,-1),
             (3,-4,2), (20,20,-20), (30,-20,10), (100,100,100), (100,100,-100)]
    comparison_rows = []
    for params in cases:
        a = marginal_moments(*params, 128)
        b = direct_moments(*params, 96)
        d = distance(a, b)
        ld = abs(a["log_z"]-b["log_z"])
        gate(f"independent angular comparison {params}", d < 5e-12 and ld < 5e-11,
             max_moment_difference=d, log_normalization_difference=ld)
        eigen = float(np.linalg.eigvalsh(a["covariance"])[0])
        gate(f"covariance matrix PSD diagnostic {params}", eigen > -3e-13,
             minimum_eigenvalue=eigen)
        swapped = marginal_moments(params[1], params[0], params[2], 128)
        swap_error = max(abs(a["x"]-swapped["y"]), abs(a["y"]-swapped["x"]),
                         abs(a["z"]-swapped["z"]), abs(a["xy"]-swapped["xy"]),
                         abs(a["xz"]-swapped["yz"]), abs(a["xx"]-swapped["yy"]))
        gate(f"loop exchange symmetry {params}", swap_error < 5e-12, residual=swap_error)
        center = marginal_moments(-params[0], params[1], -params[2], 128)
        center_error = max(abs(a["x"]+center["x"]), abs(a["y"]-center["y"]),
                           abs(a["z"]+center["z"]), abs(a["xy"]+center["xy"]),
                           abs(a["xz"]-center["xz"]), abs(a["yz"]+center["yz"]))
        gate(f"center transformation U to minus U {params}", center_error < 5e-12,
             residual=center_error)
        comparison_rows.append(dict(k1=params[0], k2=params[1], eta=params[2],
                                    covariance=a["cov_xy"], direct_covariance=b["cov_xy"],
                                    maximum_moment_difference=d, log_z_difference=ld))

    for k1, k2 in ((0,0), (1,2), (-1,2), (10,-5), (100,-100)):
        a = marginal_moments(k1, k2, 0, 128)
        u, v = single_loop(k1), single_loop(k2)
        gate(f"exact factorized baseline {k1,k2}",
             max(abs(a["x"]-u["mean"]), abs(a["y"]-v["mean"]),
                 abs(a["xy"]-u["mean"]*v["mean"]),
                 abs(a["z"]-u["mean"]*v["mean"]), abs(a["cov_xy"])) < 5e-13)
    for eta in (-100, -20, -5, -1, -1e-6, 0, 1e-6, 1, 5, 20, 100):
        a = marginal_moments(0,0,eta,128)
        b = special_family(eta)
        gate(f"exact special covariance family eta {eta}", distance(a,b) < 5e-13,
             max_moment_difference=distance(a,b))

    derivative_rows = []
    for k1, k2 in ((0,0), (1,2), (-1,2), (10,-5)):
        target = single_loop(k1)["variance"] * single_loop(k2)["variance"]
        errors = []
        for step in (.1, .05, .025, .0125):
            plus = marginal_moments(k1,k2,step,96)["cov_xy"]
            minus = marginal_moments(k1,k2,-step,96)["cov_xy"]
            derivative = (plus-minus)/(2*step)
            error = abs(derivative-target)
            errors.append(error)
            derivative_rows.append(dict(k1=k1,k2=k2,step=step,derivative=derivative,
                                        exact_identity_float=target,absolute_difference=error))
        ratios = [errors[j]/errors[j+1] for j in range(3)]
        gate(f"susceptibility centered difference second order {k1,k2}",
             all(3.8 < r < 4.2 for r in ratios), successive_error_ratios=ratios)
        gate(f"positive exact baseline susceptibility {k1,k2}", target > 0,
             variance_product=target)

    refinement_rows = []
    for params in ((1,2,1),(20,20,-20),(100,100,100),(100,100,-100)):
        reference = marginal_moments(*params,128)
        for method, sequence in (("marginal",(8,16,32,64)),("direct",(12,24,48,96))):
            errors = []
            for n in sequence:
                result = (marginal_moments if method == "marginal" else direct_moments)(*params,n)
                error = distance(result,reference)
                errors.append(error)
                refinement_rows.append(dict(k1=params[0],k2=params[1],eta=params[2],method=method,
                                            nodes=n,max_moment_difference=error,
                                            reference="1D nodes 128; floating diagnostic"))
            gate(f"actual quadrature refinement {method} {params}", errors[-1] < 5e-12,
                 initial_error=errors[0], final_error=errors[-1])
            if max(map(abs,params)) == 100:
                gate(f"coarse grid is rejected {method} {params}", errors[0] > 1e-4,
                     initial_error=errors[0], declared_target=5e-12)

    false_factor = marginal_moments(1,2,1,128)["cov_xy"]
    gate("wrong factorization is discriminated for changed mixed-loop action",
         abs(false_factor) > .02, actual_covariance=false_factor, wrong_covariance=0.0)
    special_false = special_family(5)["cov_xy"]
    gate("special family retains nonzero covariance despite Haar marginals",
         special_false > .17, actual_covariance=special_false, wrong_covariance=0.0)
    gate("source bytes unchanged during run", source_bytes == (HERE / "forward_model.py").read_bytes())

    def write_csv(name, rows):
        with (out/name).open("w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

    write_csv("comparison.csv",comparison_rows)
    write_csv("susceptibility_refinement.csv",derivative_rows)
    write_csv("quadrature_refinement.csv",refinement_rows)
    curve_rows=[]
    slope=single_loop(1)["variance"]*single_loop(2)["variance"]
    for eta in np.linspace(-3,3,61):
        curve_rows.append(dict(eta=float(eta),covariance_1_2=marginal_moments(1,2,float(eta),96)["cov_xy"],
                               covariance_0_0=special_family(float(eta))["cov_xy"],
                               tangent_1_2=float(eta)*slope,false_factorization=0.0))
    write_csv("covariance_curves.csv",curve_rows)
    report={"schema":"ym14-forward-loop1-v1", "status":"passed", "source_sha256":source_hash,
            "test_source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "check_count":len(checks), "checks":checks,
            "versions":{"python":sys.version.split()[0],"numpy":np.__version__,"scipy":scipy.__version__},
            "scope":"Declared compact two-loop Euclidean measure; floating diagnostics only",
            "not_claimed":["rigorous quadrature interval","Hamiltonian vacuum","mass gap",
                           "undeformed four-dimensional Yang–Mills construction"],
            "maximum_independent_moment_difference":max(r["maximum_moment_difference"] for r in comparison_rows),
            "wrong_factorization_covariance_1_2_1":false_factor}
    (out/"results.json").write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    print(json.dumps({k:report[k] for k in ("status","check_count","source_sha256","maximum_independent_moment_difference")}))


if __name__ == "__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path,default=HERE/"output")
    run(parser.parse_args().output)
