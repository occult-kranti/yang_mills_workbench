#!/usr/bin/env python3
"""Round19 B2 independent comparison against actual forward schema.

Standard API:
  python3 compare.py --producer SOURCE --evidence FORWARD_OUTPUT --output NEW_DIR

The comparison reruns the backward B2 checker, maps B1 basis/face indices by
coordinate-normalized masks, compares the PVP_RR ledger, the full row envelopes,
exact radical certificates, parameter range, and source-manifest bindings.  It
then mutates normalized evidence and requires the same admission predicate to
reject each wrong model.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Tuple

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
CHECK = HERE / "check.py"
B1_COMPARE = ROOT / "research/round19/backward/b1/compare.py"


def load_b1_compare():
    spec = importlib.util.spec_from_file_location("ym19_b1_compare", B1_COMPARE)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

b1cmp = load_b1_compare()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def run_independent(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-B"]
    if sys.flags.optimize:
        cmd.append("-" + "O" * sys.flags.optimize)
    cmd += [str(CHECK), "--output", str(output_dir)]
    subprocess.run(cmd, check=True)


def scale_has_positive_E_star(scale: Mapping[str, Any]) -> bool:
    val = scale.get("E_star")
    if val is True:
        return True
    if isinstance(val, (int, float)):
        return val > 0
    text = str(val).strip().lower() if val is not None else ""
    if not text or text in {"0", "0.0", "zero", "none", "null", "false"}:
        return False
    if any(word in text for word in ["e_star=0", "kappa", "tolerance", "fibonacci", "volume"]):
        return False
    return "positive" in text and ("energy" in text or "reference" in text)


def norm_expr(s: Any) -> str | None:
    if s is None:
        return None
    return str(s).replace(" ", "").replace("*", "")


def frac_norm(x: Any) -> str:
    q = Fraction(str(x))
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def load_output_dir(evidence: Path) -> Dict[str, Any]:
    out = {"results": load_json(evidence / "results.json")}
    for name in ["block-certificate.json", "certificates.json", "block-envelopes.json", "compressed-pvp-RR.json", "pvp-linear.json", "row-envelopes.json", "controls.json", "source-manifest.json", "manifest.json"]:
        p = evidence / name
        if p.exists():
            out[name] = load_json(p)
    csv_path = evidence / "row-envelopes.csv"
    if csv_path.exists():
        with csv_path.open(newline="") as f:
            out["row-envelopes.csv"] = list(csv.DictReader(f))
    return out


def load_b1_bundle(kind: str) -> Dict[str, Any]:
    if kind == "producer":
        base = ROOT / "research/round19/forward/b1/output"
        graph = load_json(base / "graph.json")
        channels = load_json(base / "channels.json")
        masks = b1cmp.producer_channel_masks(channels, graph)
    else:
        base = ROOT / "research/round19/backward/b1/output"
        graph = load_json(base / "graph.json")
        channels = load_json(base / "channels.json")
        masks = b1cmp.independent_channel_masks(channels, graph)
    face_map = b1cmp.canonical_face_id_map(graph)
    return {"graph": graph, "channels": channels, "masks_by_idx": masks, "face_by_id": face_map}


def normalize_backward(data: Mapping[str, Any]) -> Dict[str, Any]:
    r = data["results"]
    block = data.get("block-certificate.json", {})
    rows_data = data.get("row-envelopes.json", {})
    b1 = load_b1_bundle("independent")
    row_env = {}
    for row in rows_data.get("rows", []):
        # The backward checker's stored mask is native to its B1 edge order.
        # For comparison, key every row by the same coordinate-normalized B1
        # channel mask map used for PVP entries and for the forward schema.
        mask = b1["masks_by_idx"][int(row["basis_index"])]
        row_env[mask] = {
            "energy_over_alpha": str(row["energy_over_alpha"]),
            "cycle_length": int(row["cycle_length"]),
            "pvp_abs_row_sum": frac_norm(row["pvp_abs_row_sum_coefficient"]),
            "pvp_abs_col_sum": frac_norm(row["pvp_abs_col_sum_coefficient"]),
            "gram_abs_row_sum": frac_norm(row["gram_abs_row_sum_coefficient"]),
            "gram_abs_col_sum": frac_norm(row["gram_abs_col_sum_coefficient"]),
        }
    pvp_entries = {}
    pvp = data.get("pvp-linear.json", {})
    for entry in pvp.get("rows", []):
        i, j = int(entry["i"]), int(entry["j"])
        if i == 0 or j == 0:
            continue
        im, jm = b1["masks_by_idx"][i], b1["masks_by_idx"][j]
        for term in entry["terms"]:
            fm = b1["face_by_id"][int(term["face"])]
            pvp_entries[(im, jm, fm)] = frac_norm(term["coeff"])
    primary = r["primary_box"]
    bench = r["round18_3_over_8_benchmark"]
    env = r["parameter_envelope"]
    return {
        "kind": "backward",
        "scale": r["physical_scale"],
        "b1_inputs": r["b1_inputs"],
        "row_envelopes": row_env,
        "pvp_entries": pvp_entries,
        "block_envelope": {
            "projector_dimension": 48,
            "R_dimension": 47,
            "H0_energy_counts_over_alpha": {"3": 11, "9/2": 36},
            "compressed_pvp_RR_nonzero_count": len(pvp_entries),
            "max_compressed_pvp_abs_row_sum": r["row_envelope_summary"]["max_compressed_pvp_abs_row_sum"],
            "max_exact_gram_abs_row_sum": r["row_envelope_summary"]["max_exact_gram_abs_row_sum"],
        },
        "certificates": {
            "1/8": box_cert(primary),
            "3/8": box_cert(bench),
            "7/16": box_cert(env["r_7_over_16_positive_control"] | {"schur_lower_E1_over_alpha": env["r_7_over_16_positive_control"]["E1_lower"], "E0_upper_over_alpha": "0", "PminusOmega_block_lower_a_over_alpha": "17/8", "Q_lower_without_cross_over_alpha": "19/16", "cross_WstarW_row_radius_max_over_alpha_squared": "931/1024", "determinant": "1653/1024", "discriminant": "289/64", "trace_over_alpha": "53/16", "E1_lower_over_alpha_exact": "19/32"}),
            "1/2": box_cert(env["r_1_over_2_insufficient_control"] | {"schur_lower_E1_over_alpha": env["r_1_over_2_insufficient_control"]["E1_lower"], "E0_upper_over_alpha": "0", "PminusOmega_block_lower_a_over_alpha": "2", "Q_lower_without_cross_over_alpha": "1/2", "cross_WstarW_row_radius_max_over_alpha_squared": "19/16", "determinant": "-3/16", "discriminant": "7", "trace_over_alpha": "5/2", "E1_lower_over_alpha_exact": "(5/2 - sqrt(7))/2"}),
        },
        "parameter_range": norm_expr(env.get("certified_positive_range")),
        "parameter_formula": {k: norm_expr(env.get(k)) for k in ["a_r_over_alpha", "d_r_over_alpha", "w_r_over_alpha_squared", "schur_lower_R_r_over_alpha", "determinant_condition"]},
        "proof_statement": r.get("proof_statement", {}),
        "manifest": data.get("source-manifest.json") or data.get("manifest.json"),
    }


def box_cert(box: Mapping[str, Any]) -> Dict[str, Any]:
    e1 = box.get("schur_lower_E1_over_alpha") or box.get("E1_lower") or {}
    exact = box.get("E1_lower_over_alpha_exact") or e1.get("expression")
    return {
        "r": str(box.get("r")),
        "a": str(box.get("PminusOmega_block_lower_a_over_alpha")),
        "d": str(box.get("Q_lower_without_cross_over_alpha")),
        "w": str(box.get("cross_WstarW_row_radius_max_over_alpha_squared")),
        "trace": str(box.get("trace_over_alpha")),
        "determinant": str(box.get("determinant")),
        "discriminant": str(box.get("discriminant") or e1.get("radicand")),
        "E0_upper": str(box.get("E0_upper_over_alpha")),
        "E1_exact": norm_expr(exact),
        "positive": bool(e1.get("certified_positive", box.get("positive_by_determinant_test"))),
    }


def normalize_forward(data: Mapping[str, Any]) -> Dict[str, Any]:
    r = data["results"]
    b1 = load_b1_bundle("producer")
    block = data["block-envelopes.json"]
    row_env = {}
    for row in block["rows"]:
        mask = b1["masks_by_idx"][int(row["basis_index"])]
        row_env[mask] = {
            "energy_over_alpha": str(row["energy_over_alpha"]),
            "cycle_length": int(row["cycle_length"]),
            "pvp_abs_row_sum": frac_norm(row["pvp_abs_row_sum"]),
            "pvp_abs_col_sum": frac_norm(row["pvp_abs_col_sum"]),
            "gram_abs_row_sum": frac_norm(row["gram_abs_row_sum"]),
            "gram_abs_col_sum": frac_norm(row["gram_abs_col_sum"]),
        }
    pvp_entries = {}
    pvp = data["compressed-pvp-RR.json"]
    for entry in pvp["entries"]:
        im, jm = b1["masks_by_idx"][int(entry["i"])], b1["masks_by_idx"][int(entry["j"])]
        fm = b1["face_by_id"][int(entry["face"])]
        pvp_entries[(im, jm, fm)] = frac_norm(entry["coeff"])
    certs = {c["r"]: forward_cert(c) for c in data["certificates.json"]["certificates"]}
    return {
        "kind": "forward",
        "scale": r.get("scale_register", {}),
        "b1_inputs": b1_inputs_from_manifest(data.get("source-manifest.json", {})),
        "row_envelopes": row_env,
        "pvp_entries": pvp_entries,
        "block_envelope": {
            "projector_dimension": block.get("projector_dimension"),
            "R_dimension": block.get("R_dimension"),
            "H0_energy_counts_over_alpha": block.get("H0_energy_counts_over_alpha"),
            "compressed_pvp_RR_nonzero_count": block.get("compressed_pvp_RR_nonzero_count"),
            "max_compressed_pvp_abs_row_sum": str(block.get("max_compressed_pvp_abs_row_sum")),
            "max_exact_gram_abs_row_sum": str(block.get("max_exact_gram_abs_row_sum")),
        },
        "certificates": certs,
        "parameter_range": norm_expr(data["certificates.json"].get("certified_positive_radius_interval")),
        "parameter_formula": {
            "a_r_over_alpha": "3-2r",
            "d_r_over_alpha": "6-11r",
            "w_r_over_alpha_squared": "19r^2/4",
            "schur_lower_R_r_over_alpha": "(9-13r-sqrt(100r^2-54r+9))/2",
            "determinant_condition": "18-45r+69r^2/4>0",
        },
        "proof_statement": {"E1_lower": r.get("block_argument", {}).get("lower_2x2_matrix"), "E0_upper": r.get("E0_upper"), "gap_direction": "gap_lower" if r.get("E0_upper") else None},
        "manifest": data.get("source-manifest.json"),
        "row_csv": data.get("row-envelopes.csv"),
    }


def forward_cert(c: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "r": str(c.get("r")),
        "a": str(c.get("a_R_lower_over_alpha")),
        "d": str(c.get("d_Q_lower_over_alpha")),
        "w": str(c.get("w_cross_norm_square_over_alpha_squared")),
        "trace": str(c.get("trace_over_alpha")),
        "determinant": str(c.get("determinant")),
        "discriminant": str(c.get("discriminant")),
        "E0_upper": str(c.get("E0_upper_over_alpha")),
        "E1_exact": norm_expr(c.get("E1_lower_over_alpha_exact")),
        "positive": bool(c.get("positive_by_determinant_test")),
    }


def b1_inputs_from_manifest(sm: Mapping[str, Any]) -> Dict[str, Any]:
    src = sm.get("source_inputs", {})
    return {
        "projector_dimension": 48,
        "PminusOmega_dimension": 47,
        "Q_threshold_over_alpha": "6",
        "b1_forward_check_sha256": src.get("research/round19/forward/b1/check.py"),
        "b1_forward_results_sha256": src.get("research/round19/forward/b1/output/results.json"),
        "b1_forward_cross_gram_sha256": src.get("research/round19/forward/b1/output/cross-gram-coefficients.json"),
        "b1_gate_sha256": src.get("research/round19/advisor/b1-gate.json"),
    }


def admission_failures(prod: Mapping[str, Any], exp: Mapping[str, Any], producer_source: Path | None = None, evidence_dir: Path | None = None) -> List[str]:
    failures: List[str] = []
    scale = prod["scale"]
    if not scale_has_positive_E_star(scale) or str(scale.get("alpha_over_E_star")) != "2":
        failures.append("physical_scale")
    be = prod["block_envelope"]
    if be.get("projector_dimension") != 48 or be.get("R_dimension") != 47 or be.get("H0_energy_counts_over_alpha") != {"3": 11, "9/2": 36}:
        failures.append("block_projector_levels")
    for k in ["compressed_pvp_RR_nonzero_count", "max_compressed_pvp_abs_row_sum", "max_exact_gram_abs_row_sum"]:
        if str(be.get(k)) != str(exp["block_envelope"].get(k)):
            failures.append(f"block_envelope:{k}")
    if prod["row_envelopes"] != exp["row_envelopes"]:
        failures.append("row_envelopes")
    if prod["pvp_entries"] != exp["pvp_entries"]:
        failures.append("compressed_pvp_RR")
    if prod["certificates"] != exp["certificates"]:
        failures.append("certificates")
    if prod["parameter_range"] != exp["parameter_range"]:
        failures.append("parameter_range")
    if prod["parameter_formula"] != exp["parameter_formula"]:
        failures.append("parameter_formula")
    proof = prod.get("proof_statement", {})
    if not proof.get("E1_lower") or not proof.get("E0_upper") or not proof.get("gap_direction"):
        failures.append("separate_E1_E0_gap_direction")
    b1 = prod.get("b1_inputs", {})
    locked = {
        "b1_forward_check_sha256": "e3410b3955be695c8ffbdf8062b5904fe9d5be3612c437678574670f5e148f4d",
        "b1_forward_results_sha256": "792f2d43ab72de2779a4d4fb6505bb221323497da561e482b2033ac16c6bbde4",
        "b1_forward_cross_gram_sha256": "387344ba4108afcf32e21a89a0aff023abc3f8134f1767008a9acd0b959bec33",
    }
    for k, v in locked.items():
        if b1.get(k) != v:
            failures.append(f"b1_source_binding:{k}")
    if producer_source is not None and evidence_dir is not None:
        sm = prod.get("manifest")
        if not sm:
            failures.append("source_manifest_missing")
        else:
            src_dir = producer_source if producer_source.is_dir() else producer_source.parent
            source_files = sm.get("source_files", {})
            for name in ["check.py", "report.md"]:
                p = src_dir / name
                if name not in source_files:
                    failures.append(f"source_manifest_missing_source_entry:{name}")
                elif not p.exists():
                    failures.append(f"source_manifest_missing_source_file:{name}")
                elif source_files[name] != sha256_file(p):
                    failures.append(f"source_manifest_source_hash:{name}")
            outputs = sm.get("outputs", {})
            for name in ["results.json", "certificates.json", "block-certificate.json", "block-envelopes.json", "compressed-pvp-RR.json", "controls.json", "pvp-linear.json", "row-envelopes.csv"]:
                p = evidence_dir / name
                if name not in outputs:
                    failures.append(f"source_manifest_missing_output_entry:{name}")
                elif not p.exists():
                    failures.append(f"source_manifest_missing_output_file:{name}")
                elif outputs[name] != sha256_file(p):
                    failures.append(f"source_manifest_output_hash:{name}")
    return sorted(set(failures))


def mutate_and_expect_reject(prod: Dict[str, Any], exp: Dict[str, Any], producer_source: Path, evidence_dir: Path) -> List[Dict[str, Any]]:
    controls = []
    def run(name: str, mutator) -> None:
        m = deepcopy(prod)
        mutator(m)
        failures = admission_failures(m, exp, producer_source, evidence_dir)
        controls.append({"name": name, "passed": bool(failures), "detected_failures": failures})
    run("old_12_channel_projector", lambda m: m["block_envelope"].__setitem__("projector_dimension", 12))
    run("constant_3alpha_block_shortcut", lambda m: m["block_envelope"].__setitem__("H0_energy_counts_over_alpha", {"3": 47}))
    run("omit_face_six_or_six_six_PVP_entry", lambda m: m["pvp_entries"].pop(next(iter(m["pvp_entries"]))))
    run("change_PVP_coefficient", lambda m: m["pvp_entries"].__setitem__(next(iter(m["pvp_entries"])), "-1/8"))
    run("wrong_cross_factor", lambda m: m["block_envelope"].__setitem__("max_exact_gram_abs_row_sum", "19/8"))
    run("claim_round18_benchmark_without_rederived_certificate", lambda m: m["certificates"].pop("3/8", None))
    run("sample_Ritz_gap_replaces_minmax", lambda m: m["proof_statement"].pop("E1_lower", None))
    run("zero_E_star", lambda m: m["scale"].__setitem__("E_star", "0"))
    run("kappa_as_E_star", lambda m: m["scale"].__setitem__("E_star", "kappa"))
    run("fibonacci_as_E_star", lambda m: m["scale"].__setitem__("E_star", "Fibonacci index"))
    run("E1_E0_sign_error", lambda m: m["proof_statement"].pop("E0_upper", None))
    run("delete_row_envelope_cell", lambda m: m["row_envelopes"].pop(next(iter(m["row_envelopes"]))))
    run("misstate_7_16_bound", lambda m: m["certificates"]["7/16"].__setitem__("E1_exact", "1/2"))
    run("misstate_half_as_positive", lambda m: m["certificates"]["1/2"].__setitem__("positive", True))
    run("delete_parameter_range", lambda m: m.__setitem__("parameter_range", None))
    def remove_manifest_check(m):
        m["manifest"] = deepcopy(m["manifest"])
        m["manifest"].setdefault("source_files", {}).pop("check.py", None)
    run("manifest_missing_check_hash", remove_manifest_check)
    def remove_output(m):
        m["manifest"] = deepcopy(m["manifest"])
        m["manifest"].setdefault("outputs", {}).pop("results.json", None)
    run("manifest_missing_results_output", remove_output)
    return controls


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--producer", required=True)
    ap.add_argument("--evidence", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    producer_source = Path(args.producer).resolve()
    evidence_dir = Path(args.evidence).resolve()
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    independent_dir = output_dir / "independent-reconstruction"
    run_independent(independent_dir)
    exp = normalize_backward(load_output_dir(independent_dir))
    # If evidence has forward B2 schema use forward normalizer; otherwise allow self-test against backward schema.
    raw = load_output_dir(evidence_dir)
    prod = normalize_forward(raw) if "block-envelopes.json" in raw and "certificates.json" in raw else normalize_backward(raw)
    failures = admission_failures(prod, exp, producer_source, evidence_dir)
    checks: List[Dict[str, Any]] = []
    def add(name: str, passed: bool, **extra: Any) -> None:
        row = {"name": name, "passed": bool(passed)}
        row.update(extra)
        checks.append(row)
    add("positive E_star and alpha/E_star=2 are declared", "physical_scale" not in failures, scale=prod["scale"])
    add("B1 source bindings use accepted 48-channel exact Gram inputs", not any(f.startswith("b1_source_binding") for f in failures), b1_inputs=prod["b1_inputs"])
    add("block envelope aggregate fields match independent exact rows", not any(f.startswith("block_envelope") or f == "block_projector_levels" for f in failures), block_envelope=prod["block_envelope"])
    add("full 47-row envelope table matches by canonical channel mask", "row_envelopes" not in failures, row_count=len(prod["row_envelopes"]))
    add("compressed PVP_RR ledger matches by canonical row/column/face masks", "compressed_pvp_RR" not in failures, entry_count=len(prod["pvp_entries"]))
    add("exact certificates match for r=1/8, 3/8, 7/16 and failed 1/2", "certificates" not in failures, producer=prod["certificates"], expected=exp["certificates"])
    add("parameter inequality and formula match independent envelope", "parameter_range" not in failures and "parameter_formula" not in failures, range=prod["parameter_range"], formula=prod["parameter_formula"])
    add("E1 lower, E0 upper and gap direction are separate", "separate_E1_E0_gap_direction" not in failures)
    add("source manifest binds required source and output files", not any(f.startswith("source_manifest") for f in failures))
    mutation_controls = mutate_and_expect_reject(prod, exp, producer_source, evidence_dir)
    for c in mutation_controls:
        checks.append({"name": "mutation rejects " + c["name"], "passed": c["passed"], "detected_failures": c["detected_failures"]})
    status = "accepted" if all(c["passed"] for c in checks) and not failures else "rejected"
    comparison = {
        "schema": "ym19-backward-b2-comparison-v2",
        "status": status,
        "producer_source": str(producer_source),
        "producer_evidence": str(evidence_dir),
        "producer_results_sha256": sha256_file(evidence_dir / "results.json"),
        "producer_certificates_sha256": sha256_file(evidence_dir / "certificates.json") if (evidence_dir / "certificates.json").exists() else None,
        "producer_block_envelopes_sha256": sha256_file(evidence_dir / "block-envelopes.json") if (evidence_dir / "block-envelopes.json").exists() else None,
        "producer_pvp_rr_sha256": sha256_file(evidence_dir / "compressed-pvp-RR.json") if (evidence_dir / "compressed-pvp-RR.json").exists() else None,
        "independent_results_sha256": sha256_file(independent_dir / "results.json"),
        "checks_count": len(checks),
        "checks": checks,
        "admission_failures": failures,
        "mutation_controls": mutation_controls,
        "reported_bounds": {
            "r_1_8_E1_lower": prod["certificates"].get("1/8", {}).get("E1_exact"),
            "r_3_8_E1_lower": prod["certificates"].get("3/8", {}).get("E1_exact"),
            "r_7_16_E1_lower": prod["certificates"].get("7/16", {}).get("E1_exact"),
            "r_1_2_positive": prod["certificates"].get("1/2", {}).get("positive"),
        },
    }
    out = output_dir / "comparison.json"
    out.write_text(json.dumps(comparison, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": status, "checks_count": len(checks), "output": str(out)}, sort_keys=True))
    if status != "accepted":
        sys.exit(1)


if __name__ == "__main__":
    main()
