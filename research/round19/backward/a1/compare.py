#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import re
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
CHECK_PATH = HERE / "check.py"
ROLE_BOUNDS = {"L": Fraction(1, 2), "M": Fraction(1, 8), "R": Fraction(1, 2)}
ROLE_CANON = {
    "L": "L", "left": "L", "left-end": "L",
    "M": "M", "bridge": "M", "middle": "M",
    "R": "R", "right": "R", "right-end": "R",
}
EXPECTED_ROLES = {"L", "M", "R", "LM", "MR", "LMR"}


def load_check():
    spec = importlib.util.spec_from_file_location("ym19_backward_a1_check", CHECK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load backward check module")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def producer_hashes(path: Path) -> dict[str, str]:
    if path.is_file():
        return {str(path): sha256_path(path)}
    if path.is_dir():
        return {str(p): sha256_path(p) for p in sorted(path.rglob("*")) if p.is_file()}
    raise ValueError(f"producer path missing: {path}")


def load_evidence(path: Path) -> tuple[Path, dict[str, Any]]:
    if path.is_dir():
        for name in ["clipped_restrictions_results.json", "results.json"]:
            c = path / name
            if c.exists():
                path = c
                break
        else:
            raise ValueError(f"no known evidence json in {path}")
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise ValueError("evidence must be a JSON object")
    return path, data


def frac(value: Any, field: str) -> Fraction:
    if isinstance(value, bool):
        raise ValueError(f"{field} is Boolean")
    if isinstance(value, int):
        return Fraction(value, 1)
    if isinstance(value, str):
        return Fraction(value.strip())
    raise ValueError(f"{field} must be integer or rational string")


def canon_roles(raw: Any) -> str:
    if isinstance(raw, str):
        text = raw.replace("+", "").replace(" ", "")
        if text in EXPECTED_ROLES:
            return text
        parts = [p for p in re.split(r"[^A-Za-z-]+", raw) if p]
    elif isinstance(raw, list):
        parts = [str(p) for p in raw]
    else:
        raise ValueError("roles must be string or list")
    out = "".join(ROLE_CANON[p] for p in parts)
    if out not in EXPECTED_ROLES:
        raise ValueError(f"noncontiguous or unknown roles {raw!r}")
    return out


def sign_for(item: dict[str, Any], role: str) -> int:
    signs = item.get("signs", {})
    if not isinstance(signs, dict):
        raise ValueError("signs must be object")
    candidates = [role]
    candidates += [k for k, v in ROLE_CANON.items() if v == role]
    found = None
    for key in candidates:
        if key in signs:
            found = signs[key]
            break
    if found is None:
        raise ValueError(f"missing sign for {role}")
    if isinstance(found, bool) or found not in (-1, 0, 1):
        raise ValueError(f"invalid sign for {role}: {found!r}")
    return int(found)


def ratio_for(item: dict[str, Any], role: str) -> Fraction:
    # Canonical forward evidence records signed rational coefficients; older exploratory
    # evidence recorded only signs.  Reconstruct from signed ratios when present.
    ratios = item.get("signed_ratios_over_alpha")
    if isinstance(ratios, dict):
        candidates = [role]
        candidates += [k for k, v in ROLE_CANON.items() if v == role]
        for key in candidates:
            if key in ratios:
                return frac(ratios[key], f"signed ratio {role}")
        raise ValueError(f"missing signed ratio for {role}")
    return ROLE_BOUNDS[role] * sign_for(item, role)


def recompute_signed_case(item: dict[str, Any]) -> dict[str, Any]:
    roles = canon_roles(item.get("roles"))
    abs_coeff = {r: abs(ratio_for(item, r)) for r in roles}
    if roles == "LMR":
        lower = Fraction(3, 4) - max(abs_coeff["L"], abs_coeff["R"]) - abs_coeff["M"]
        budget = sum(abs_coeff.values())
    else:
        budget = sum(abs_coeff.values())
        lower = Fraction(3, 4) - budget
    declared_budget = frac(item.get("absolute_norm_budget_over_alpha", item.get("magnetic_norm_budget_over_alpha")), "absolute_norm_budget_over_alpha")
    declared_lower = frac(item.get("gap_lower_over_alpha", item.get("certified_lower_over_alpha")), "gap_lower_over_alpha")
    declared_pass = item.get("passes_alpha_over_8", item.get("passes_alpha_over_8_local_target"))
    return {
        "roles": roles,
        "budget": budget,
        "lower": lower,
        "budget_matches": declared_budget == budget,
        "lower_matches": declared_lower == lower,
        "pass_matches": declared_pass is (lower >= Fraction(1, 8)),
        "passes": lower >= Fraction(1, 8),
    }


def independent_case_index(own: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    return {(case["n"], case["x_phase"]): case for case in own["cases"]}


def count_map(case: dict[str, Any]) -> dict[str, int]:
    mapping = {
        "('left',)": "L", "('bridge',)": "M", "('right',)": "R",
        "('left', 'bridge')": "LM", "('bridge', 'right')": "MR", "('left', 'bridge', 'right')": "LMR",
    }
    out: dict[str, int] = {k: 0 for k in EXPECTED_ROLES}
    for key, value in case.get("component_role_counts", {}).items():
        out[mapping[key]] = int(value)
    return out


def selected_face_count_from_counts(counts: dict[str, int]) -> int:
    return sum(len(role) * int(count) for role, count in counts.items())


def producer_fixture_key(item: dict[str, Any]) -> tuple[int, int]:
    n = item.get("n")
    phase = item.get("x_phase", item.get("x_phase_offset", item.get("phase")))
    if isinstance(n, bool) or not isinstance(n, int):
        raise ValueError("fixture n must be int")
    if isinstance(phase, bool) or not isinstance(phase, int):
        raise ValueError("fixture phase must be int")
    return n, phase


def producer_counts(item: dict[str, Any]) -> dict[str, int]:
    raw = item.get("component_role_counts", item.get("component_counts", item.get("cluster_type_counts", item.get("finite_box_component_counts"))))
    if not isinstance(raw, dict):
        raise ValueError("fixture lacks component counts")
    out = {k: 0 for k in EXPECTED_ROLES}
    aliases = {
        "left": "L", "left-end": "L", "bridge": "M", "middle": "M", "right": "R", "right-end": "R",
        "L": "L", "M": "M", "R": "R", "LM": "LM", "MR": "MR", "LMR": "LMR",
        "left-end+bridge": "LM", "bridge+right-end": "MR", "left-end+bridge+right-end": "LMR",
    }
    for key, value in raw.items():
        ck = aliases.get(str(key))
        if ck is None:
            ck = canon_roles(str(key))
        out[ck] = int(value)
    return out


def fixture_witness_count(item: dict[str, Any]) -> int | None:
    if "omitted_face_count" in item:
        return int(item["omitted_face_count"])
    if "remaining_face_count" in item:
        return int(item["remaining_face_count"])
    if isinstance(item.get("remaining_case_counts"), dict):
        return sum(int(v) for v in item["remaining_case_counts"].values())
    if isinstance(item.get("sample_unused_witnesses"), list) and item.get("all_remaining_have_witness") is True:
        return None
    return None


def example_edge_check(item: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    examples = item.get("component_examples", {})
    if isinstance(examples, dict):
        for label, ex in examples.items():
            if not isinstance(ex, dict):
                errors.append(f"component example {label} is not object")
                continue
            roles = canon_roles(ex.get("roles"))
            expected_links = {"L": 4, "M": 4, "R": 4, "LM": 7, "MR": 7, "LMR": 10}[roles]
            if int(ex.get("link_count", -1)) != expected_links:
                errors.append(f"{label} link_count {ex.get('link_count')} != {expected_links}")
    witnesses = item.get("remaining_witness_examples", {})
    if isinstance(witnesses, dict):
        for label, w in witnesses.items():
            if not isinstance(w, dict) or "face" not in w or "free_witness" not in w:
                errors.append(f"witness example {label} missing face/free_witness")
    elif witnesses not in ({}, None):
        errors.append("remaining_witness_examples is not object")
    return errors


def declared_phase_fixtures(ev: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ["phase_fixtures_n2_to_n12_all_x_phases", "phase_box_fixtures", "all_phase_box_fixtures", "finite_phase_fixtures", "box_phase_fixtures"]:
        if isinstance(ev.get(key), list):
            return ev[key]
    # canonical_box_fixtures intentionally lacks x phase in old proposal, so it is not accepted as full v1.1 coverage.
    return []


def extract_scale(ev: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    containers = []
    for key in ["scale_register", "physical_contract", "energy_reference"]:
        if isinstance(ev.get(key), dict):
            containers.append(ev[key])
    merged: dict[str, Any] = {}
    for c in containers:
        merged.update(c)
    try:
        ae = frac(merged.get("alpha_over_E_star"), "alpha_over_E_star")
        amin = frac(merged.get("alpha_min_over_E_star", merged.get("alpha_min/E_star", merged.get("alpha_floor_over_E_star"))), "alpha_min_over_E_star")
    except Exception as exc:
        return False, {"reason": str(exc), "fields_seen": sorted(merged.keys())}
    E_raw = merged.get("E_star")
    symbolic_positive = isinstance(E_raw, str) and "positive" in E_raw.lower() and "symbolic" in E_raw.lower()
    numeric_positive = False
    if not symbolic_positive:
        try:
            numeric_positive = frac(E_raw, "E_star") > 0
        except Exception:
            numeric_positive = False
    bad_kappa = any("kappa" in k.lower() and "absent" not in str(merged[k]).lower() and "not present" not in str(merged[k]).lower() for k in merged)
    ok = (symbolic_positive or numeric_positive) and ae > 0 and amin > 0 and not bad_kappa
    return ok, {"E_star": str(E_raw), "alpha_over_E_star": str(ae), "alpha_min_over_E_star": str(amin), "fields_seen": sorted(merged.keys())}




def verify_source_manifest(ev_path: Path, producer: Path, producer_hash: str | None) -> tuple[bool, dict[str, Any]]:
    manifest_path = ev_path.parent / "source-manifest.json"
    if not manifest_path.exists():
        return False, {"reason": "missing source-manifest.json next to evidence"}
    try:
        manifest = json.loads(manifest_path.read_text())
    except Exception as exc:
        return False, {"reason": f"manifest is not valid JSON: {exc}"}
    problems: list[dict[str, Any]] = []
    src = manifest.get("source_files")
    if not isinstance(src, dict):
        problems.append({"field": "source_files", "reason": "missing or not object"})
    else:
        check_declared = src.get("check.py")
        if producer_hash is not None and check_declared != producer_hash:
            problems.append({"field": "source_files.check.py", "declared": check_declared, "actual": producer_hash})
        report_path = producer.parent / "report.md"
        if report_path.exists():
            report_hash = sha256_path(report_path)
            if src.get("report.md") != report_hash:
                problems.append({"field": "source_files.report.md", "declared": src.get("report.md"), "actual": report_hash})
    outs = manifest.get("outputs")
    if not isinstance(outs, dict):
        problems.append({"field": "outputs", "reason": "missing or not object"})
    else:
        for name, declared in outs.items():
            out_file = ev_path.parent / name
            if not out_file.exists():
                problems.append({"field": f"outputs.{name}", "reason": "file missing"})
                continue
            actual = sha256_path(out_file)
            if declared != actual:
                problems.append({"field": f"outputs.{name}", "declared": declared, "actual": actual})
    return not problems, {"manifest": str(manifest_path), "sha256": sha256_path(manifest_path), "problems": problems[:8]}

def add(checks: list[dict[str, Any]], name: str, passed: bool, kind: str, **extra: Any) -> None:
    checks.append({"name": name, "kind": kind, "passed": bool(passed), **extra})


def mutate_signed_bad(ev: dict[str, Any]) -> bool:
    bad = copy.deepcopy(ev)
    cases = bad.get("signed_cases", bad.get("local_signed_cases"))
    if not isinstance(cases, list) or not cases:
        return False
    if "gap_lower_over_alpha" in cases[0]:
        cases[0]["gap_lower_over_alpha"] = "99"
    else:
        cases[0]["certified_lower_over_alpha"] = "99"
    try:
        vals = [recompute_signed_case(item) for item in cases]
        return not all(v["lower_matches"] and v["budget_matches"] and v["pass_matches"] and v["passes"] for v in vals)
    except Exception:
        return True


def mutate_missing_phase(ev: dict[str, Any]) -> bool:
    bad = copy.deepcopy(ev)
    fixtures = declared_phase_fixtures(bad)
    if not fixtures:
        return True
    fixtures.pop()
    try:
        keys = [producer_fixture_key(item) for item in fixtures]
        return len(keys) != 44 or len(set(keys)) != 44
    except Exception:
        return True


def compare(producer: Path, evidence: Path) -> dict[str, Any]:
    mod = load_check()
    own = mod.build_result()
    ev_path, ev = load_evidence(evidence)
    hashes = producer_hashes(producer)
    checks: list[dict[str, Any]] = []

    add(checks, "producer evidence is JSON object", isinstance(ev, dict), "provenance", evidence=str(ev_path))
    add(checks, "producer source hash syntax is sha256", isinstance(ev.get("source_sha256"), str) and re.fullmatch(r"[0-9a-f]{64}", ev.get("source_sha256", "")) is not None, "provenance")
    producer_hash = None
    if len(hashes) == 1 and isinstance(ev.get("source_sha256"), str):
        producer_hash = next(iter(hashes.values()))
        add(checks, "producer source hash matches supplied source bytes", producer_hash == ev["source_sha256"], "provenance", actual=producer_hash, declared=ev["source_sha256"])
    else:
        add(checks, "producer source hash matches supplied source bytes", False, "provenance", producer_file_count=len(hashes))
    manifest_ok, manifest_detail = verify_source_manifest(ev_path, producer, producer_hash)
    add(checks, "producer source manifest matches source files and output files", manifest_ok, "provenance", **manifest_detail)

    scale_ok, scale_detail = extract_scale(ev)
    add(checks, "exact positive E_star and alpha_over_E_star are declared separately", scale_ok, "mathematics", **scale_detail)

    signed = ev.get("signed_cases", ev.get("local_signed_cases"))
    signed_vals: list[dict[str, Any]] = []
    signed_error = None
    try:
        if not isinstance(signed, list):
            raise ValueError("local_signed_cases must be list")
        signed_vals = [recompute_signed_case(item) for item in signed]
    except Exception as exc:
        signed_error = str(exc)
    roles_seen = {v["roles"] for v in signed_vals}
    declared_signed_count = ev.get("signed_case_count", ev.get("local_signed_case_count"))
    add(checks, "signed cases cover exactly recomputable contiguous component roles", signed_error is None and EXPECTED_ROLES <= roles_seen and declared_signed_count == len(signed_vals), "mathematics", roles_seen=sorted(roles_seen), error=signed_error, declared_count=declared_signed_count, actual_count=len(signed_vals))
    add(checks, "every signed local bound matches independent Fraction arithmetic", signed_error is None and all(v["budget_matches"] and v["lower_matches"] and v["pass_matches"] and v["passes"] for v in signed_vals), "mathematics")

    bad_noncontig = ev.get("rejected_non_restrictions")
    explicit_bad = isinstance(bad_noncontig, list) and all(item.get("rejected") is True for item in bad_noncontig) and {item.get("roles") for item in bad_noncontig} >= {"LR", "LMRextra"}
    add(checks, "non-contiguous clipped types are not admitted", explicit_bad or roles_seen <= EXPECTED_ROLES, "mathematics", explicit_control_present=explicit_bad)

    own_cases = independent_case_index(own)
    fixtures = declared_phase_fixtures(ev)
    fixture_errors = []
    keys: list[tuple[int, int]] = []
    if fixtures:
        for item in fixtures:
            try:
                key = producer_fixture_key(item)
                keys.append(key)
                expected = own_cases[key]
                got_counts = producer_counts(item)
                exp_counts = count_map(expected)
                if got_counts != exp_counts:
                    fixture_errors.append({"key": key, "field": "counts", "expected": exp_counts, "got": got_counts})
                if "edge_count" in item and int(item["edge_count"]) != expected["edge_count"]:
                    fixture_errors.append({"key": key, "field": "edge_count", "expected": expected["edge_count"], "got": item.get("edge_count")})
                if "face_count" in item and int(item["face_count"]) != expected["face_count"]:
                    fixture_errors.append({"key": key, "field": "face_count", "expected": expected["face_count"], "got": item.get("face_count")})
                witness_count = fixture_witness_count(item)
                omitted_expected = expected["face_count"] - selected_face_count_from_counts(exp_counts)
                if witness_count is not None and witness_count != omitted_expected:
                    fixture_errors.append({"key": key, "field": "witness/omitted count", "expected": omitted_expected, "got": witness_count})
                if witness_count is None and not item.get("sample_unused_witnesses") and not item.get("remaining_case_counts"):
                    fixture_errors.append({"key": key, "field": "witness evidence", "expected": "count or witnesses", "got": "missing"})
                for edge_error in example_edge_check(item):
                    fixture_errors.append({"key": key, "field": "edge/witness example", "error": edge_error})
            except Exception as exc:
                fixture_errors.append({"fixture": item, "error": str(exc)[:160]})
    expected_keys = {(n, p) for n in range(2, 13) for p in range(4)}
    add(checks, "finite phase fixtures cover exactly n=2..12 times four x phases", set(keys) == expected_keys and len(keys) == 44 and len(set(keys)) == 44, "mathematics", count=len(keys), duplicates=len(keys)-len(set(keys)), missing=sorted(expected_keys-set(keys))[:8])
    add(checks, "phase fixture counts, edge counts and witness counts match independent enumeration", bool(fixtures) and not fixture_errors, "mathematics", errors=fixture_errors[:6])

    rest = ev.get("restriction_stability_witness", {})
    stable_direct = isinstance(rest, dict) and rest.get("same_coefficient_for_every_box_containing_face") is True
    stable_control = False
    for ctrl in ev.get("controls", []) if isinstance(ev.get("controls"), list) else []:
        if ctrl.get("control") == "reject_complete_strip_only_coefficient_reclassification":
            stable_control = ctrl.get("passed") is True and ctrl.get("literal_B6_ratio") == ctrl.get("literal_B8_ratio") and ctrl.get("complete_strip_only_B6_ratio") != ctrl.get("complete_strip_only_B8_ratio")
    add(checks, "stable restriction witness for face (xy,4,0,0) is recorded", stable_direct or stable_control, "mathematics", direct=stable_direct, control=stable_control)
    add(checks, "independent verifier result itself passed", own.get("status") == "passed", "mathematics")

    add(checks, "altered signed lower bound is rejected by recomputation", mutate_signed_bad(ev), "mutation-control")
    add(checks, "missing phase fixture is rejected by exact coverage gate", mutate_missing_phase(ev), "mutation-control")

    failed_math = [c for c in checks if c["kind"] != "provenance" and not c["passed"]]
    failed_prov = [c for c in checks if c["kind"] == "provenance" and not c["passed"]]
    status = "accepted" if not failed_math and not failed_prov else ("producer-mathematics-incomplete" if failed_math else "producer-provenance-incomplete")
    return {
        "schema": "ym19-backward-a1-comparison-v2",
        "status": status,
        "producer": str(producer),
        "evidence": str(ev_path),
        "scope": "provenance checks and mathematical comparison are distinct; producer source/evidence are read as bytes and producer code is not imported",
        "checks": checks,
        "summary": {
            "provenance_failures": len(failed_prov),
            "mathematics_failures": len(failed_math),
            "source_hashes_do_not_admit_json_by_themselves": True,
        },
        "accept_reject_conditions": {
            "accept": "exact positive scale fields, 44 unique phase fixtures with matching counts/edges/witnesses, independently recomputed Fraction local bounds, stable restriction witness, mutation controls and source provenance all pass",
            "reject": "any forged pass Boolean, altered rational bound, missing phase, duplicate fixture, zero E_star or unbound source blocks acceptance",
        },
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
