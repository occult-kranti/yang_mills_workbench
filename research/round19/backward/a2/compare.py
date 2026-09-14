#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
CHECK_PATH = HERE / "check.py"


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_check():
    spec = importlib.util.spec_from_file_location("ym19_backward_a2_check", CHECK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load independent check")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def frac(value: Any, name: str) -> Fraction:
    if isinstance(value, bool):
        raise ValueError(f"{name} is Boolean")
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        text = value.strip()
        if "symbolic" in text or "positive" in text:
            raise ValueError(f"{name} is symbolic, not numeric ratio")
        return Fraction(text)
    raise ValueError(f"{name} must be integer or rational string")


def load_evidence(path: Path) -> tuple[Path, dict[str, Any]]:
    if path.is_dir():
        for name in ["results.json", "a2-results.json"]:
            c = path / name
            if c.exists():
                path = c
                break
        else:
            raise ValueError(f"no recognized results file in {path}")
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError("producer evidence must be object")
    return path, data


def producer_hashes(path: Path) -> dict[str, str]:
    if path.is_file():
        return {str(path): sha256_path(path)}
    if path.is_dir():
        return {str(p): sha256_path(p) for p in sorted(path.rglob("*")) if p.is_file()}
    raise ValueError(f"producer path missing: {path}")


def verify_manifest(ev_path: Path, producer: Path, producer_hash: str | None) -> tuple[bool, dict[str, Any]]:
    manifest_path = ev_path.parent / "source-manifest.json"
    if not manifest_path.exists():
        return False, {"reason": "missing source-manifest.json next to evidence"}
    manifest = json.loads(manifest_path.read_text())
    problems = []
    src = manifest.get("source_files")
    if not isinstance(src, dict):
        problems.append({"field": "source_files", "reason": "missing"})
    else:
        if producer_hash is not None and src.get("check.py") != producer_hash:
            problems.append({"field": "source_files.check.py", "declared": src.get("check.py"), "actual": producer_hash})
        report = producer.parent / "report.md"
        if report.exists() and src.get("report.md") != sha256_path(report):
            problems.append({"field": "source_files.report.md", "declared": src.get("report.md"), "actual": sha256_path(report)})
    outs = manifest.get("outputs")
    if isinstance(outs, dict):
        for name, declared in outs.items():
            p = ev_path.parent / name
            if not p.exists():
                problems.append({"field": f"outputs.{name}", "reason": "missing"})
            elif sha256_path(p) != declared:
                problems.append({"field": f"outputs.{name}", "declared": declared, "actual": sha256_path(p)})
    else:
        problems.append({"field": "outputs", "reason": "missing"})
    src_inputs = manifest.get("source_inputs", {})
    if isinstance(src_inputs, dict):
        repo = Path.cwd()
        for rel, declared in src_inputs.items():
            p = repo / rel
            if not p.exists():
                problems.append({"field": f"source_inputs.{rel}", "reason": "file missing"})
            elif sha256_path(p) != declared:
                problems.append({"field": f"source_inputs.{rel}", "declared": declared, "actual": sha256_path(p)})
    return not problems, {"manifest": str(manifest_path), "sha256": sha256_path(manifest_path), "problems": problems[:8]}


def find_mapping(ev: dict[str, Any], *keys: str) -> dict[str, Any]:
    for key in keys:
        value = ev.get(key)
        if isinstance(value, dict):
            return value
    return {}


def get_nested(ev: dict[str, Any], field: str) -> Any:
    for container in [ev, ev.get("theorem", {}), ev.get("scale_register", {}), ev.get("spectral_argument", {})]:
        if isinstance(container, dict) and field in container:
            return container[field]
    return None




def S(m: int) -> Fraction:
    return sum(Fraction(1, 2**k) for k in range(m))


def selected_weight_inside(m: int) -> Fraction:
    zsum = S(m)
    ysum = sum(Fraction(1, 2**y) for y in range(m) if y % 2 == 0)
    xsum = sum(Fraction(1, 2**x) for x in range(m) if x % 4 in (0, 1, 2))
    return Fraction(1, 24) * zsum * ysum * xsum


def total_weight_inside(m: int) -> Fraction:
    return Fraction(1, 8) * S(m) ** 3


def omitted_weight_inside(m: int) -> Fraction:
    return total_weight_inside(m) - selected_weight_inside(m)


def expected_tail_row(m: int) -> dict[str, str]:
    omitted_total = Fraction(107, 135)
    omitted = omitted_weight_inside(m)
    return {
        "coordinate_cutoff_m": str(m),
        "total_weight_inside": str(total_weight_inside(m)),
        "selected_weight_inside": str(selected_weight_inside(m)),
        "omitted_weight_inside": str(omitted),
        "omitted_tail_to_infinity": str(omitted_total - omitted),
        "tail_nonnegative": "True",
    }


def check_summable_ledger(ev: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    led = ev.get("summable_ledger_closed_form")
    if not isinstance(led, dict):
        return False, {"reason": "missing summable_ledger_closed_form"}
    expected = {
        "total_weight": "1",
        "selected_weight": "28/135",
        "omitted_weight": "107/135",
        "beta_exact_over_alpha_for_abs_tau": "|tau|*107/135",
        "beta_crude_over_alpha_for_abs_tau": "|tau|",
        "omitted_le_total": True,
    }
    problems = {k: {"expected": v, "got": led.get(k)} for k, v in expected.items() if led.get(k) != v}
    return not problems, {"expected": expected, "problems": problems}


def check_tail_fixtures(ev: dict[str, Any], ev_path: Path) -> tuple[bool, dict[str, Any]]:
    rows = ev.get("truncation_tail_fixtures")
    if not isinstance(rows, list):
        return False, {"reason": "missing truncation_tail_fixtures"}
    expected_ms = [1, 2, 3, 4, 5, 8, 12, 16, 32]
    problems = []
    if [r.get("coordinate_cutoff_m") for r in rows] != expected_ms:
        problems.append({"field": "coordinate_cutoff_m sequence", "got": [r.get("coordinate_cutoff_m") for r in rows]})
    for row, m in zip(rows, expected_ms):
        exp = expected_tail_row(m)
        for k, v in exp.items():
            got = str(row.get(k))
            if got != v:
                problems.append({"m": m, "field": k, "expected": v, "got": got})
    csv_path = ev_path.parent / "tail-fixtures.csv"
    if csv_path.exists():
        import csv
        with csv_path.open(newline="") as f:
            csv_rows = list(csv.DictReader(f))
        if len(csv_rows) != len(expected_ms):
            problems.append({"field": "csv row count", "expected": len(expected_ms), "got": len(csv_rows)})
        for crow, m in zip(csv_rows, expected_ms):
            exp = expected_tail_row(m)
            for k, v in exp.items():
                if crow.get(k) != v:
                    problems.append({"m": m, "field": "csv." + k, "expected": v, "got": crow.get(k)})
    else:
        problems.append({"field": "tail-fixtures.csv", "reason": "missing"})
    return not problems, {"rows": len(rows), "problems": problems[:8]}


def check_representative_coefficients(ev: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    rows = ev.get("representative_coefficients")
    if not isinstance(rows, list):
        return False, {"reason": "missing representative_coefficients"}
    by = {(tuple(r.get("face", [])), r.get("status")): r for r in rows if isinstance(r, dict)}
    expected = [
        (("xy", 0, 0, 0), "selected-reference-block", "1/2", None),
        (("xy", 1, 0, 0), "selected-reference-block", "1/8", None),
        (("xy", 2, 0, 0), "selected-reference-block", "1/2", None),
        (("xy", 3, 0, 0), "summable-perturbation", "1/12288", [0, 3, 0, 0]),
        (("xy", 0, 1, 0), "summable-perturbation", "1/3072", [1, 0, 1, 0]),
        (("xz", 0, 0, 0), "summable-perturbation", "1/1536", [2, 0, 0, 0]),
        (("yz", 0, 0, 0), "summable-perturbation", "1/1536", [2, 0, 0, 0]),
    ]
    problems=[]
    for face,status,coeff,witness in expected:
        row=by.get((face,status))
        if row is None:
            problems.append({"face": face, "status": status, "reason": "missing"}); continue
        if row.get("coefficient_over_alpha") != coeff:
            problems.append({"face": face, "field":"coefficient_over_alpha", "expected": coeff, "got": row.get("coefficient_over_alpha")})
        if status == "summable-perturbation":
            if row.get("absolute_budget_over_alpha") != coeff:
                problems.append({"face": face, "field":"absolute_budget_over_alpha", "expected": coeff, "got": row.get("absolute_budget_over_alpha")})
            if row.get("zero_mean_witness_link") != witness:
                problems.append({"face": face, "field":"zero_mean_witness_link", "expected": witness, "got": row.get("zero_mean_witness_link")})
    return not problems, {"rows": len(rows), "problems": problems[:8]}


def check_structured_premises(ev: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    problems=[]
    if ev.get("route") != "constructive_product_representation":
        problems.append({"field":"route", "got": ev.get("route")})
    ftc=ev.get("finite_tensor_core")
    if not isinstance(ftc, dict):
        problems.append({"field":"finite_tensor_core", "reason":"missing"})
    else:
        if "operator/form domains" not in ftc.get("definition", ""):
            problems.append({"field":"finite_tensor_core.definition", "reason":"does not bind local form/operator domains"})
        if ftc.get("not_used") != "arbitrary bounded-operator orbit of the product vector":
            problems.append({"field":"finite_tensor_core.not_used", "got": ftc.get("not_used")})
    theorem = ev.get("operator_theorem", {})
    domain_text = theorem.get("domain_essential_spectrum_record", "") if isinstance(theorem, dict) else ""
    domain_text_lower = domain_text.lower()
    if "need not equal d(h_ref)" in domain_text_lower or "need not equal" in domain_text_lower:
        problems.append({"field":"operator_theorem.domain_essential_spectrum_record", "reason":"bounded V should preserve operator domain D(H)=D(H_ref), but stale text says need not equal"})
    operator_domain_ok = (
        "d(h)=d(h_ref)" in domain_text_lower
        or ("operator domain" in domain_text_lower and "same" in domain_text_lower)
        or "self-adjoint on exactly d(h_ref)" in domain_text_lower
        or "self adjoint on exactly d(h_ref)" in domain_text_lower
    )
    form_domain_ok = "form domain" in domain_text_lower and "same" in domain_text_lower
    if not (operator_domain_ok and form_domain_ok):
        problems.append({"field":"operator_theorem.domain_essential_spectrum_record", "reason":"must explicitly state bounded-perturbation operator-domain equality and unchanged form domain"})
    gauge=ev.get("gauge_and_physical_noncavity")
    if not isinstance(gauge, dict):
        problems.append({"field":"gauge_and_physical_noncavity", "reason":"missing"})
    else:
        for k in ["local_gauge_invariance", "reference_ground_invariance", "perturbed_ground_invariance", "nonzero_gauss_excitation_witness", "physical_gap_wording"]:
            if not gauge.get(k):
                problems.append({"field":"gauge_and_physical_noncavity."+k, "reason":"missing"})
    blocks=ev.get("local_blocks")
    try:
        comp=blocks["complete_strip_local_input"]
        free=blocks["free_link_factor"]
        part=blocks["reference_partition"]
        if comp.get("gap_lower_delta_over_alpha") != "1/8" or comp.get("unique_ground") is not True or comp.get("full_link_before_gauss") is not True:
            problems.append({"field":"local_blocks.complete_strip_local_input", "got": comp})
        if free.get("casimir_gap_over_alpha") != "3/4" or free.get("dominates_delta") is not True:
            problems.append({"field":"local_blocks.free_link_factor", "got": free})
        if part.get("selected_strip_supports_disjoint") is not True:
            problems.append({"field":"local_blocks.reference_partition.selected_strip_supports_disjoint", "got": part.get("selected_strip_supports_disjoint")})
    except Exception as exc:
        problems.append({"field":"local_blocks", "reason":str(exc)})
    forbidden = ev.get("not_claimed")
    if not isinstance(forbidden, list) or not any("finite clipped" in x for x in forbidden) or not any("continuum" in x for x in forbidden):
        problems.append({"field":"not_claimed", "got": forbidden})
    return not problems, {"problems": problems[:8]}

def check_theorem(ev: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    detail: dict[str, Any] = {}
    try:
        alpha = frac(get_nested(ev, "alpha_over_E_star"), "alpha_over_E_star")
        delta = frac(get_nested(ev, "delta_over_E_star"), "delta_over_E_star")
        beta_crude = frac(get_nested(ev, "beta_crude_over_E_star"), "beta_crude_over_E_star")
        beta_exact = frac(get_nested(ev, "beta_exact_over_E_star"), "beta_exact_over_E_star")
        tau = frac(get_nested(ev, "tau"), "tau")
        gap_crude = frac(get_nested(ev, "gap_lower_crude_over_E_star"), "gap_lower_crude_over_E_star")
        gap_exact = frac(get_nested(ev, "gap_lower_exact_over_E_star"), "gap_lower_exact_over_E_star")
        accepted = ev.get("accepted_statement", {}) if isinstance(ev.get("accepted_statement"), dict) else {}
        common_raw = get_nested(ev, "common_crude_gap_lower_over_E_star")
        if common_raw is None:
            common_raw = accepted.get("common_crude_gap_lower_over_E_star")
        common_crude = frac(common_raw, "common_crude_gap_lower_over_E_star")
    except Exception as exc:
        return False, {"reason": str(exc)}
    detail.update({
        "alpha_over_E_star": str(alpha), "delta_over_E_star": str(delta), "tau": str(tau),
        "beta_crude_over_E_star": str(beta_crude), "beta_exact_over_E_star": str(beta_exact),
        "gap_lower_crude_over_E_star": str(gap_crude), "gap_lower_exact_over_E_star": str(gap_exact),
        "common_crude_gap_lower_over_E_star": str(common_crude),
    })
    ok = (
        alpha == 2 and delta == alpha / 8 and tau == Fraction(1, 64)
        and beta_crude == alpha * abs(tau)
        and beta_exact == alpha * abs(tau) * Fraction(107, 135)
        and gap_crude == delta - beta_crude
        and gap_exact == delta - beta_exact
        and common_crude == Fraction(7, 64)
        and accepted.get("gap_lower_crude_over_alpha") == "7/64"
        and accepted.get("gap_lower_exact_over_alpha") == "973/8640"
        and accepted.get("common_crude_gap_lower_over_E_star") == "7/64"
    )
    return ok, detail

def mutation_controls(ev: dict[str, Any]) -> list[dict[str, Any]]:
    controls = []
    bad = json.loads(json.dumps(ev))
    for container_key in ["operator_theorem", "scale_register"]:
        if isinstance(bad.get(container_key), dict):
            bad[container_key]["beta_crude_over_E_star"] = bad[container_key].get("delta_over_E_star", "1/4")
            bad[container_key]["gap_lower_crude_over_E_star"] = "0"
    ok, _ = check_theorem(bad)
    controls.append({"name": "beta>=delta mutation rejected", "passed": not ok})
    bad2 = json.loads(json.dumps(ev))
    for container_key in ["operator_theorem", "scale_register"]:
        if isinstance(bad2.get(container_key), dict):
            bad2[container_key]["gap_lower_exact_over_E_star"] = "99"
    ok2, _ = check_theorem(bad2)
    controls.append({"name": "altered exact gap lower bound rejected", "passed": not ok2})
    bad3 = json.loads(json.dumps(ev))
    if isinstance(bad3.get("truncation_tail_fixtures"), list) and bad3["truncation_tail_fixtures"]:
        bad3["truncation_tail_fixtures"].pop()
    ok3, _ = check_tail_fixtures(bad3, Path("/nonexistent/results.json"))
    controls.append({"name": "missing tail fixture rejected", "passed": not ok3})
    bad4 = json.loads(json.dumps(ev))
    if isinstance(bad4.get("representative_coefficients"), list):
        for r in bad4["representative_coefficients"]:
            if isinstance(r, dict) and r.get("status") == "summable-perturbation":
                r["zero_mean_witness_link"] = None
                break
    ok4, _ = check_representative_coefficients(bad4)
    controls.append({"name": "missing zero-mean witness rejected", "passed": not ok4})
    return controls

def add(checks: list[dict[str, Any]], name: str, passed: bool, kind: str, **extra: Any) -> None:
    checks.append({"name": name, "passed": bool(passed), "kind": kind, **extra})


def compare(producer: Path, evidence: Path) -> dict[str, Any]:
    mod = load_check()
    own = mod.build_result()
    ev_path, ev = load_evidence(evidence)
    hashes = producer_hashes(producer)
    checks: list[dict[str, Any]] = []
    add(checks, "producer evidence is JSON object", True, "provenance", evidence=str(ev_path))
    add(checks, "producer source hash syntax is sha256", isinstance(ev.get("source_sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", ev.get("source_sha256", "")) is not None, "provenance")
    producer_hash = next(iter(hashes.values())) if len(hashes) == 1 else None
    add(checks, "producer source hash matches supplied source bytes", producer_hash is not None and ev.get("source_sha256") == producer_hash, "provenance", actual=producer_hash, declared=ev.get("source_sha256"))
    manifest_ok, manifest_detail = verify_manifest(ev_path, producer, producer_hash)
    add(checks, "producer source manifest matches source and outputs", manifest_ok, "provenance", **manifest_detail)
    theorem_ok, theorem_detail = check_theorem(ev)
    add(checks, "product-representation theorem scale/gap fields recompute exactly", theorem_ok, "mathematics", **theorem_detail)
    ledger_ok, ledger_detail = check_summable_ledger(ev)
    add(checks, "full dyadic summable ledger recomputes to selected 28/135 and omitted 107/135", ledger_ok, "mathematics", **ledger_detail)
    tails_ok, tails_detail = check_tail_fixtures(ev, ev_path)
    add(checks, "truncation tail fixtures and CSV match exact dyadic formulas", tails_ok, "mathematics", **tails_detail)
    coeff_ok, coeff_detail = check_representative_coefficients(ev)
    add(checks, "representative coefficients and zero-mean witnesses match exact assignment", coeff_ok, "mathematics", **coeff_detail)
    struct_ok, struct_detail = check_structured_premises(ev)
    add(checks, "structured domain/gauge/open-claim premises are present", struct_ok, "mathematics", **struct_detail)
    add(checks, "independent verifier itself passed", own.get("status") == "passed", "mathematics")
    for m in mutation_controls(ev):
        add(checks, m["name"], m["passed"], "mutation-control")
    failed_prov = [c for c in checks if c["kind"] == "provenance" and not c["passed"]]
    failed_math = [c for c in checks if c["kind"] != "provenance" and not c["passed"]]
    status = "accepted" if not failed_prov and not failed_math else ("producer-provenance-incomplete" if failed_prov and not failed_math else "producer-mathematics-incomplete")
    return {
        "schema": "ym19-backward-a2-comparison-v1",
        "status": status,
        "producer": str(producer),
        "evidence": str(ev_path),
        "scope": "provenance and mathematics are distinct; producer code is not imported",
        "checks": checks,
        "summary": {"provenance_failures": len(failed_prov), "mathematics_failures": len(failed_math), "source_hashes_do_not_admit_json_by_themselves": True},
        "producer_hashes": hashes,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--producer", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if out.exists():
        raise SystemExit(f"output exists: {out}")
    out.mkdir(parents=True)
    result = compare(Path(args.producer), Path(args.evidence))
    (out / "comparison.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "checks": len(result["checks"]), **result["summary"]}))


if __name__ == "__main__":
    main()
