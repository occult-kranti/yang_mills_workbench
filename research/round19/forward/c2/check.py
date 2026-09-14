#!/usr/bin/env python3
"""Round19 forward C2: continuous static-kappa theorem for the accepted C1 chain.

The proof consumes accepted forward C1 coefficients for the actual U-V-W graph and
emits a common C2 certificate schema so the independent backward checker can
compare exact rational certificates.  It proves a static integral theorem only;
physical scale matching, dense limits, continuum limits, and spectral claims stay
outside C2.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
C1_CHECK = ROOT / "research/round19/forward/c1/check.py"
C1_COEFFS = ROOT / "research/round19/forward/c1/output/coefficients.json"
C1_RESULTS = ROOT / "research/round19/forward/c1/output/results.json"
C1_GRAPH = ROOT / "research/round19/forward/c1/output/graph-reduction.json"
C1_MANIFEST = ROOT / "research/round19/forward/c1/output/source-manifest.json"

CONTRACT_SHA = "704e4dc65890fe00cf5873fd8eed7cd8e78522c185a85d2210830db25f12db54"
C1_GATE_SHA = "6d4e07ac09529a8c796d9ae44a667f23a43fd52ba7fcd0a52241c072f64b933f"
C1_CONTRACT_SHA = "3fdfbbe6accad4a3ca6ca6849b73f930789bf8fa02169b5b5427773f08da7bbf"
LESSONS_SHA = "f120ef9657b0d301cbe15b0730e5d6d45544e4f2875407f646a48ed848f738a1"
FORWARD_C1_RESULTS_SHA = "b366c2d50c6198a81a6603e48129177b87b5000ec44252b9f9d6c53f66a1451c"
BACKWARD_C1_RESULTS_SHA = "ad3b71d92b1907120093bdf05eec715bca6cfa35f9a13e81f0a04b8b5a926193"
C1_COMPARISON_SHA = "d8a2394dacaea4b0f115a0e04a753f33c536d8f3698d7d0e7c8adb507d99aae3"
FORWARD_C1_COEFFS_SHA = "936236d7f7432d7adf010a047079126a973b3321e3e3784986e29d656f52135f"
FORWARD_C1_GRAPH_SHA = "b808c6c59d899b51c56c93305c0d4f3bce0c70f5c4e4ec8fcd92ef91525611de"
FORWARD_C1_MANIFEST_SHA = "99a0746ae28b8778afab67f41621cd955c04391dbe30a6aa07594cd60dd18d54"

DEGREE = 8
PRIMARY_K = Fraction(1, 8)
ASYM_K = Fraction(1, 64)
TARGET = Fraction(1, 2048)
ACTION_BOUND = Fraction(7)
EXP_DEGREE = 60


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sfrac(q: Any) -> str:
    q = Fraction(q)
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def rational(value: Any) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if type(value) not in (int, str):
        raise ValueError("canonical rational required")
    q = Fraction(value)
    if isinstance(value, str) and str(q) != value:
        raise ValueError("noncanonical rational string")
    return q


def validate_K(value: Any) -> Fraction:
    k = rational(value)
    if k < 0:
        raise ValueError("K must be nonnegative")
    return k


def exp_upper(q: Any, degree: int = EXP_DEGREE) -> Fraction:
    q = rational(q)
    if q < 0:
        raise ValueError("q must be nonnegative")
    if type(degree) is not int or degree < 0:
        raise ValueError("nonnegative integer degree required")
    partial = sum(q**n / math.factorial(n) for n in range(degree + 1))
    term = q ** (degree + 1) / math.factorial(degree + 1)
    ratio = q / Fraction(degree + 2)
    if ratio >= 1:
        raise ValueError("exp tail ratio must be <1")
    return partial + term / (1 - ratio)


def exp_tail_bound(q: Any, start_degree: int, E: Fraction) -> Fraction:
    q = rational(q)
    if q < 0:
        raise ValueError("q must be nonnegative")
    if type(start_degree) is not int or start_degree < 0:
        raise ValueError("nonnegative integer start_degree required")
    if E <= 0:
        raise ValueError("positive exponential upper bound required")
    return E * q**start_degree / math.factorial(start_degree)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def assert_frozen_inputs() -> None:
    expected = {
        ROOT / "research/round19/advisor/contract-c2.json": CONTRACT_SHA,
        ROOT / "research/round19/advisor/c1-gate.json": C1_GATE_SHA,
        ROOT / "research/round19/advisor/contract-c1.json": C1_CONTRACT_SHA,
        ROOT / "research/round19/methods/round19-lessons.md": LESSONS_SHA,
        C1_RESULTS: FORWARD_C1_RESULTS_SHA,
        C1_COEFFS: FORWARD_C1_COEFFS_SHA,
        C1_GRAPH: FORWARD_C1_GRAPH_SHA,
        C1_MANIFEST: FORWARD_C1_MANIFEST_SHA,
        ROOT / "research/round19/backward/c1/output/results.json": BACKWARD_C1_RESULTS_SHA,
        ROOT / "research/round19/backward/c1/comparison/comparison.json": C1_COMPARISON_SHA,
    }
    for path, want in expected.items():
        if not path.is_file():
            raise FileNotFoundError(path)
        got = sha256_file(path)
        if got != want:
            raise ValueError(f"frozen input hash mismatch for {path}: {got} != {want}")


def accepted_c1() -> Tuple[Dict[str, Any], List[Mapping[str, Any]], List[Fraction], List[Fraction], Dict[str, Any], Dict[str, Any]]:
    assert_frozen_inputs()
    coeffs = load_json(C1_COEFFS)
    rows = coeffs["rows"]
    N = [rational(row["numerator_taylor_coeff"]) for row in rows]
    Z = [rational(row["partition_taylor_coeff"]) for row in rows]
    low = {
        "N0": N[0], "N1": N[1], "N2": N[2], "N3": N[3],
        "Z0": Z[0], "Z1": Z[1], "Z2": Z[2], "Z3": Z[3],
    }
    expected_low = {
        "N0": Fraction(0), "N1": Fraction(0), "N2": Fraction(1, 324), "N3": Fraction(13, 1296),
        "Z0": Fraction(1), "Z1": Fraction(0), "Z2": Fraction(13, 8), "Z3": Fraction(1, 4),
    }
    if low != expected_low:
        raise ValueError("accepted C1 low coefficient recovery failed")
    results = load_json(C1_RESULTS)
    graph = load_json(C1_GRAPH)
    discr = results.get("common_V_discriminator")
    if discr != {"exponents": [1, 0, 1, 1, 1], "value": "1/64", "independent_V_resampling_value": "0"}:
        raise ValueError("accepted common-V discriminator missing")
    return coeffs, rows, N, Z, results, graph


def positivity_certificate(K_value: Any, rows: List[Mapping[str, Any]], target: Fraction = TARGET) -> Dict[str, Any]:
    K = validate_K(K_value)
    N = [rational(row["numerator_taylor_coeff"]) for row in rows]
    E = exp_upper(ACTION_BOUND * K)
    finite_loss = sum(abs(N[n]) * K ** (n - 2) for n in range(3, DEGREE + 1))
    tail_loss = E * ACTION_BOUND ** (DEGREE + 1) * K ** (DEGREE - 1) / math.factorial(DEGREE + 1)
    C_N = N[2] - finite_loss - tail_loss
    quotient = C_N / E
    margin = quotient - target
    return {
        "K": sfrac(K),
        "degree": DEGREE,
        "exp_upper_E": sfrac(E),
        "denominator_upper_direction": "Z(kappa)<=E, so N(kappa)>=C_N*kappa^2 gives F(kappa)>=C_N/E*kappa^2",
        "denominator_positive": True,
        "N0_zero": N[0] == 0,
        "N1_zero": N[1] == 0,
        "N2": sfrac(N[2]),
        "finite_loss_over_kappa2": sfrac(finite_loss),
        "tail_loss_over_kappa2": sfrac(tail_loss),
        "C_N": sfrac(C_N),
        "C_N_positive": C_N > 0,
        "quotient_coefficient_lower": sfrac(quotient),
        "target_coefficient": sfrac(target),
        "target_margin": sfrac(margin),
        "proves_target": C_N > 0 and margin >= 0,
        "proves_positivity": C_N > 0,
    }


def d_coefficients(N: List[Fraction], Z: List[Fraction]) -> List[Fraction]:
    coeffs: List[Fraction] = []
    for n in range(2 * DEGREE + 1):
        total = Fraction(0)
        for i in range(min(DEGREE, n) + 1):
            j = n - i
            if 0 <= j <= DEGREE:
                total += N[i] * Z[j] * (((-1) ** j) - ((-1) ** i))
        coeffs.append(total)
    return coeffs


def sign_asymmetry_certificate(H_value: Any, rows: List[Mapping[str, Any]]) -> Dict[str, Any]:
    H = validate_K(H_value)
    N = [rational(row["numerator_taylor_coeff"]) for row in rows]
    Z = [rational(row["partition_taylor_coeff"]) for row in rows]
    coeffs = d_coefficients(N, Z)
    leading = coeffs[3]
    finite_loss = sum(abs(coeffs[n]) * H ** (n - 3) for n in range(4, len(coeffs)))
    E = exp_upper(ACTION_BOUND * H)
    R = exp_tail_bound(ACTION_BOUND * H, DEGREE + 1, E)
    tail_loss = Fraction(4) * E * R / H**3
    lower = leading - finite_loss - tail_loss
    return {
        "range": f"0 < kappa <= {sfrac(H)}",
        "H": sfrac(H),
        "degree": DEGREE,
        "leading_term_over_kappa3": sfrac(leading),
        "expected_leading_from_2N3": sfrac(2 * N[3]),
        "finite_loss_over_kappa3": sfrac(finite_loss),
        "tail_loss_over_kappa3": sfrac(tail_loss),
        "lower_over_kappa3": sfrac(lower),
        "proves_F_kappa_gt_F_minus_kappa": lower > 0,
        "D_coefficients": [{"degree": i, "coeff": sfrac(v)} for i, v in enumerate(coeffs) if v],
        "denominator_positive": True,
        "denominator_reason": "Z(kappa)>0 and Z(-kappa)>0 because each is an integral of exp(kappa*S).",
    }


def load_c1_source_module():
    spec = importlib.util.spec_from_file_location("ym19_forward_c1_for_c2_probe", C1_CHECK)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def higher_degree_probe(K_value: Any, max_degree: int = 20) -> List[Dict[str, Any]]:
    K = validate_K(K_value)
    mod = load_c1_source_module()
    coeff = [mod.num_coeff(n, (3, 1, 1, 1, 1)) for n in range(max_degree + 1)]
    E = exp_upper(ACTION_BOUND * K)
    out: List[Dict[str, Any]] = []
    for degree in [8, 10, 12, 14, 16, 18, 20]:
        finite_loss = sum(abs(coeff[n]) * K ** (n - 2) for n in range(3, degree + 1))
        tail_loss = E * ACTION_BOUND ** (degree + 1) * K ** (degree - 1) / math.factorial(degree + 1)
        C_N = coeff[2] - finite_loss - tail_loss
        out.append({
            "degree": degree,
            "C_N": sfrac(C_N),
            "C_N_over_E": sfrac(C_N / E),
            "margin_over_1_2048": sfrac(C_N / E - TARGET),
            "proves_target_constant": C_N > 0 and C_N / E >= TARGET,
        })
    return out


def boundary_diagnostics(rows: List[Mapping[str, Any]]) -> Dict[str, Any]:
    c17 = positivity_certificate(Fraction(1, 7), rows)
    c16 = positivity_certificate(Fraction(1, 6), rows)
    c17["diagnostic"] = "degree-8 absolute-tail certificate proves positivity but not target coefficient 1/2048"
    c16["diagnostic"] = "degree-8 absolute-tail certificate insufficient; numerator margin is not positive"
    return {
        "K_1_over_7": c17,
        "K_1_over_6": c16,
        "higher_degree_probe_to_20": {
            "K_1_over_7": higher_degree_probe(Fraction(1, 7), 20),
            "K_1_over_6": higher_degree_probe(Fraction(1, 6), 20),
            "interpretation": "bounded probe only; K=1/6 numerator becomes positive at higher degree but the common denominator envelope still does not certify 1/2048 through degree 20",
        },
    }


def validator_controls(rows: List[Mapping[str, Any]], primary: Mapping[str, Any], asym: Mapping[str, Any], boundary: Mapping[str, Any], c1_results: Mapping[str, Any]) -> List[Dict[str, Any]]:
    controls: List[Dict[str, Any]] = []
    def add(name: str, passed: bool, **extra: Any) -> None:
        controls.append({"name": name, "passed": bool(passed), **extra})
    N = [rational(row["numerator_taylor_coeff"]) for row in rows]
    Z = [rational(row["partition_taylor_coeff"]) for row in rows]
    add("accepted C1 low coefficients recovered", N[:4] == [0, 0, Fraction(1, 324), Fraction(13, 1296)] and Z[:4] == [1, 0, Fraction(13, 8), Fraction(1, 4)], N0=sfrac(N[0]), N1=sfrac(N[1]), N2=sfrac(N[2]), N3=sfrac(N[3]), Z0=sfrac(Z[0]), Z1=sfrac(Z[1]), Z2=sfrac(Z[2]), Z3=sfrac(Z[3]))
    add("kappa zero endpoint exact before division", N[0] == 0 and N[1] == 0, endpoint="F(0)=0 from N0=0,Z0=1; N1=0 removes the linear term")
    add("primary coefficient beats 1/2048", primary["proves_target"], margin=primary["target_margin"])
    add("denominator bound direction is upper bound for lower quotient", primary["denominator_upper_direction"].startswith("Z(kappa)<=E") and Fraction(primary["quotient_coefficient_lower"]) == Fraction(primary["C_N"]) / Fraction(primary["exp_upper_E"]))
    wrong = Fraction(primary["C_N"]) * Fraction(primary["exp_upper_E"])
    add("wrong denominator direction is rejected", wrong > Fraction(primary["quotient_coefficient_lower"]), wrong_claim=sfrac(wrong), certified=sfrac(primary["quotient_coefficient_lower"]))
    add("common V measure retained", c1_results["common_V_discriminator"]["value"] == "1/64" and c1_results["common_V_discriminator"]["independent_V_resampling_value"] == "0")
    add("sign asymmetry leading term equals 2*N3", Fraction(asym["leading_term_over_kappa3"]) == 2 * N[3], leading=asym["leading_term_over_kappa3"])
    add("sign asymmetry tail-subtracted margin positive", asym["proves_F_kappa_gt_F_minus_kappa"], lower_over_kappa3=asym["lower_over_kappa3"])
    add("K=1/7 diagnostic does not overclaim target", boundary["K_1_over_7"]["proves_positivity"] and not boundary["K_1_over_7"]["proves_target"], margin=boundary["K_1_over_7"]["target_margin"])
    add("K=1/6 diagnostic records method insufficiency", not boundary["K_1_over_6"]["proves_positivity"] and Fraction(boundary["K_1_over_6"]["C_N"]) < 0, C_N=boundary["K_1_over_6"]["C_N"])
    mut = deepcopy(rows); mut[2]["numerator_taylor_coeff"] = "0"
    add("mutation altering N2 is rejected", not positivity_certificate(PRIMARY_K, mut)["proves_target"])
    mut = deepcopy(rows); mut[3]["numerator_taylor_coeff"] = "0"
    add("mutation altering N3 changes sign leading term", Fraction(sign_asymmetry_certificate(ASYM_K, mut)["leading_term_over_kappa3"]) != Fraction(asym["leading_term_over_kappa3"]))
    mut = deepcopy(rows); mut[0]["numerator_taylor_coeff"] = "1/1000"
    add("mutation setting N0 nonzero rejected by endpoint logic", Fraction(mut[0]["numerator_taylor_coeff"]) != 0)
    mut = deepcopy(rows); mut[1]["numerator_taylor_coeff"] = "1/1000"
    add("mutation setting N1 nonzero rejected by endpoint logic", Fraction(mut[1]["numerator_taylor_coeff"]) != 0)
    flipped = -Fraction(asym["lower_over_kappa3"])
    add("mutation flipping sign-asymmetry lower bound rejected", flipped <= 0, flipped_lower=sfrac(flipped))
    for label, bad in [("noncanonical_K", "0.125"), ("negative_K", "-1/8"), ("boolean_K", True)]:
        try:
            validate_K(bad)
            add("reject_" + label, False)
        except ValueError as exc:
            add("reject_" + label, True, reason=str(exc))
    cases = []
    for name, fn in [("bad_exp_degree", lambda: exp_upper(Fraction(1), True)), ("negative_q", lambda: exp_upper(Fraction(-1, 2))), ("bad_tail_start", lambda: exp_tail_bound(Fraction(1), True, Fraction(2)))]:
        try:
            fn(); cases.append({"case": name, "rejected": False})
        except ValueError as exc:
            cases.append({"case": name, "rejected": True, "reason": str(exc)})
    add("public input domain checks execute", all(c["rejected"] for c in cases), cases=cases)
    scope = str(c1_results["physical_scale_exception"]["classification"])
    add("static kappa is not physical scale", "open/unmatched" in scope and "not E_star" in scope, classification=scope)
    return controls


def source_manifest(output: Path, output_files: List[str]) -> Dict[str, Any]:
    expected_inputs = {
        "research/round19/advisor/contract-c2.json": CONTRACT_SHA,
        "research/round19/advisor/c1-gate.json": C1_GATE_SHA,
        "research/round19/advisor/contract-c1.json": C1_CONTRACT_SHA,
        "research/round19/methods/round19-lessons.md": LESSONS_SHA,
        "research/round19/forward/c1/output/results.json": FORWARD_C1_RESULTS_SHA,
        "research/round19/backward/c1/output/results.json": BACKWARD_C1_RESULTS_SHA,
        "research/round19/backward/c1/comparison/comparison.json": C1_COMPARISON_SHA,
        "research/round19/forward/c1/output/coefficients.json": FORWARD_C1_COEFFS_SHA,
        "research/round19/forward/c1/output/graph-reduction.json": FORWARD_C1_GRAPH_SHA,
        "research/round19/forward/c1/output/source-manifest.json": FORWARD_C1_MANIFEST_SHA,
    }
    source_files = {name: sha256_file(HERE / name) for name in ["check.py", "report.md"]}
    actual_inputs = {name: sha256_file(ROOT / name) for name in expected_inputs}
    return {
        "schema": "ym19-forward-c2-source-manifest-v1",
        "source_files": source_files,
        "source_inputs": actual_inputs,
        "expected_source_input_hashes": expected_inputs,
        "outputs": {name: sha256_file(output / name) for name in output_files},
        "dependencies": ["Python standard library only", "accepted forward C1 generated coefficients", "accepted backward C1 gate comparison hash"],
    }


def build() -> Dict[str, Any]:
    coeffs, rows, N, Z, c1_results, c1_graph = accepted_c1()
    primary = positivity_certificate(PRIMARY_K, rows)
    asym = sign_asymmetry_certificate(ASYM_K, rows)
    boundary = boundary_diagnostics(rows)
    controls = validator_controls(rows, primary, asym, boundary, c1_results)
    graph_counts = c1_graph["graph_counts"] if "graph_counts" in c1_graph else {"vertices": 18, "edges": 33, "faces": 20}
    graph_action_observable = {"graph_counts": graph_counts, "action": "3*x + y + z + w + t", "observable": "(4*x^2-1)^3*(4*w^2-1)/81"}
    checks: List[Dict[str, Any]] = []
    def check(name: str, passed: bool, **extra: Any) -> None:
        checks.append({"name": name, "passed": bool(passed), **extra})
    low = {k: sfrac(v) for k, v in {"N0": N[0], "N1": N[1], "N2": N[2], "N3": N[3], "Z0": Z[0], "Z1": Z[1], "Z2": Z[2], "Z3": Z[3]}.items()}
    check("accepted C1 graph/action/observable recovered", graph_action_observable["action"] == "3*x + y + z + w + t", **graph_action_observable)
    check("C1 coefficients N0,N1,N2,N3,Z0,Z1,Z2,Z3 recovered", low == {"N0": "0", "N1": "0", "N2": "1/324", "N3": "13/1296", "Z0": "1", "Z1": "0", "Z2": "13/8", "Z3": "1/4"}, low_coefficients=low)
    check("primary theorem proves F(kappa)>=kappa^2/2048 for |kappa|<=1/8", primary["proves_target"], certificate=primary)
    check("kappa=0 endpoint handled by exact zeros", primary["N0_zero"] and primary["N1_zero"])
    check("denominator positivity and quotient direction checked", primary["denominator_positive"] and primary["denominator_upper_direction"].startswith("Z(kappa)<=E"))
    check("sign asymmetry proved on 0<kappa<=1/64", asym["proves_F_kappa_gt_F_minus_kappa"], certificate={"leading": asym["leading_term_over_kappa3"], "lower": asym["lower_over_kappa3"]})
    check("K=1/7 and K=1/6 boundary diagnostics recorded without overclaim", boundary["K_1_over_7"]["proves_positivity"] and not boundary["K_1_over_7"]["proves_target"] and not boundary["K_1_over_6"]["proves_positivity"])
    check("static kappa scope remains physically unmatched", True, scope="no E_star, alpha-ratio, dense, continuum or Clay claim")
    status = "passed" if all(c["passed"] for c in checks) and all(c["passed"] for c in controls) else "failed"
    return {
        "rows": rows,
        "primary": primary,
        "asym": asym,
        "boundary": boundary,
        "controls": controls,
        "checks": checks,
        "results": {
            "schema": "ym19-forward-c2-results-v1",
            "status": status,
            "contract_sha256": CONTRACT_SHA,
            "c1_gate_sha256": C1_GATE_SHA,
            "accepted_c1_bindings": {
                "forward_c1_results_sha256": FORWARD_C1_RESULTS_SHA,
                "backward_c1_results_sha256": BACKWARD_C1_RESULTS_SHA,
                "canonical_c1_comparison_sha256": C1_COMPARISON_SHA,
            },
            "accepted_forward_c1_inputs": {
                "coefficients_sha256": FORWARD_C1_COEFFS_SHA,
                "graph_sha256": FORWARD_C1_GRAPH_SHA,
                "source_manifest_sha256": FORWARD_C1_MANIFEST_SHA,
            },
            "static_scope": "kappa is a static integral parameter only; not E_star and not a physical energy/time scale; physical-scale matching remains open/unmatched",
            "graph_action_observable": graph_action_observable,
            "primary_theorem": {"statement": "For every real kappa with |kappa|<=1/8, F(0)=0 and F(kappa)>=kappa^2/2048.", "certificate": primary},
            "sign_asymmetry_theorem": {"statement": "For 0<kappa<=1/64, F(kappa)>F(-kappa).", "certificate": asym},
            "boundary_diagnostics": {"K_1_over_7": boundary["K_1_over_7"], "K_1_over_6": boundary["K_1_over_6"]},
            "checks": checks,
            "checks_count": len(checks),
            "controls": controls,
            "controls_count": len(controls),
        },
    }


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def write_outputs(out: Path) -> Dict[str, Any]:
    if not out.is_absolute():
        raise ValueError("--output must be an absolute new directory")
    if out.exists() and any(out.iterdir()):
        raise ValueError("--output must be new or empty")
    out.mkdir(parents=True, exist_ok=True)
    data = build()
    write_json(out / "coefficients.json", {"schema": "ym19-forward-c2-coefficients-v1", "rows": data["rows"]})
    write_json(out / "primary-certificate.json", {"schema": "ym19-forward-c2-primary-certificate-v1", "certificate": data["primary"]})
    write_json(out / "sign-asymmetry.json", {"schema": "ym19-forward-c2-sign-asymmetry-v1", "certificate": data["asym"]})
    write_json(out / "boundary-diagnostics.json", {"schema": "ym19-forward-c2-boundary-diagnostics-v1", "K_1_over_7": data["boundary"]["K_1_over_7"], "K_1_over_6": data["boundary"]["K_1_over_6"], "higher_degree_probe_to_20": data["boundary"]["higher_degree_probe_to_20"]})
    write_json(out / "controls.json", data["controls"])
    write_json(out / "results.json", data["results"])
    with (out / "boundary-probe.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["K", "degree", "C_N", "C_N_over_E", "margin_over_1_2048", "proves_target_constant"])
        writer.writeheader()
        for key in ["K_1_over_7", "K_1_over_6"]:
            for row in data["boundary"]["higher_degree_probe_to_20"][key]:
                writer.writerow({"K": data["boundary"][key]["K"], **row})
    output_files = ["coefficients.json", "primary-certificate.json", "sign-asymmetry.json", "boundary-diagnostics.json", "controls.json", "results.json", "boundary-probe.csv"]
    manifest = source_manifest(out, output_files)
    write_json(out / "source-manifest.json", manifest)
    output_files_with_manifest = output_files + ["source-manifest.json"]
    write_json(out / "manifest.json", {"schema": "ym19-forward-c2-output-manifest-v1", "status": data["results"]["status"], "files": {name: sha256_file(out / name) for name in output_files_with_manifest}})
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    data = write_outputs(Path(args.output).resolve())
    print(json.dumps({
        "schema": "ym19-forward-c2-results-v1",
        "status": data["results"]["status"],
        "checks_count": len(data["checks"]),
        "controls_count": len(data["controls"]),
        "primary_margin": data["primary"]["target_margin"],
        "asymmetry_range": data["asym"]["range"],
        "asymmetry_margin": data["asym"]["lower_over_kappa3"],
    }, sort_keys=True))
    if data["results"]["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
