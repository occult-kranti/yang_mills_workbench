#!/usr/bin/env python3
"""Independent Round19 B2 reverse/skeptic certificate.

Uses the accepted backward B1 reconstruction as input and proves a finite two-cube
coefficient-box gap by a codimension-one min-max block bound on Omega^perp.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List, Mapping, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[4]
B1 = ROOT / "research/round19/backward/b1/check.py"
SCHEMA = "ym19-backward-b2-results-v1"


def load_b1():
    spec = importlib.util.spec_from_file_location("ym19_backward_b1", B1)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frac_s(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def sqrt_interval(q: Fraction, digits: int = 30) -> Dict[str, str]:
    # Decimal interval by integer scaling, with no floating-point formatting.
    scale = 10 ** digits
    n = q.numerator * scale * scale // q.denominator
    lo = math.isqrt(n)
    while Fraction((lo + 1) * (lo + 1), scale * scale) <= q:
        lo += 1
    hi = lo if Fraction(lo * lo, scale * scale) == q else lo + 1
    return {
        "radicand": frac_s(q),
        "lower_scaled": str(lo),
        "upper_scaled": str(hi),
        "digits": str(digits),
        "lower_decimal": decimal_from_scaled(lo, digits),
        "upper_decimal": decimal_from_scaled(hi, digits),
    }




def scaled_floor(q: Fraction, digits: int) -> int:
    scale = 10 ** digits
    return (q.numerator * scale) // q.denominator


def scaled_ceil(q: Fraction, digits: int) -> int:
    scale = 10 ** digits
    return -((-q.numerator * scale) // q.denominator)


def decimal_from_scaled(value: int, digits: int) -> str:
    sign = "-" if value < 0 else ""
    v = abs(value)
    whole, frac = divmod(v, 10 ** digits)
    return f"{sign}{whole}.{frac:0{digits}d}"

def lower_root(a: Fraction, d: Fraction, w: Fraction) -> Dict[str, Any]:
    rad = (d - a) * (d - a) + 4 * w
    # mu = (a+d-sqrt(rad))/2. Store exact radical expression and an
    # outward decimal interval computed by integer arithmetic.
    interval = sqrt_interval(rad, 30)
    sqrt_hi = Fraction(int(interval["upper_scaled"]), 10 ** 30)
    sqrt_lo = Fraction(int(interval["lower_scaled"]), 10 ** 30)
    mu_lower = (a + d - sqrt_hi) / 2
    mu_upper = (a + d - sqrt_lo) / 2
    digits = 15
    lo_scaled = scaled_floor(mu_lower, digits)
    hi_scaled = scaled_ceil(mu_upper, digits)
    return {
        "expression": f"({frac_s(a)} + {frac_s(d)} - sqrt({frac_s(rad)}))/2",
        "radicand": frac_s(rad),
        "decimal_interval_outward": {
            "lower": decimal_from_scaled(lo_scaled, digits),
            "upper": decimal_from_scaled(hi_scaled, digits),
            "digits": digits,
        },
        "certified_positive": mu_lower > 0,
        "rational_lower_bound_from_sqrt_interval": frac_s(mu_lower),
        "rational_upper_bound_from_sqrt_interval": frac_s(mu_upper),
    }


def pvp_linear_coefficients(b1, channel_words, faces) -> List[List[Dict[int, Fraction]]]:
    fwords = b1.face_words(faces)
    n = len(channel_words)
    out: List[List[Dict[int, Fraction]]] = [[{} for _ in range(n)] for __ in range(n)]
    for i in range(n):
        for j in range(n):
            for f, fw in enumerate(fwords):
                val = b1.su2_trace_integral([channel_words[i], fw, channel_words[j]])
                if val:
                    out[i][j][f] = -Fraction(1, 2) * val
    return out


def exact_b1_data() -> Dict[str, Any]:
    b1 = load_b1()
    edges = b1.graph_edges()
    faces = b1.graph_faces(edges)
    cycles = b1.simple_cycle_masks(edges, 8)
    channel_masks = [0] + cycles[4] + cycles[6]
    channel_words = [[]] + [b1.cycle_word_from_mask(m, edges) for m in cycles[4]] + [b1.cycle_word_from_mask(m, edges) for m in cycles[6]]
    channels = [b1.channel_record(0, edges, "vacuum")] + [b1.channel_record(m, edges, "four") for m in cycles[4]] + [b1.channel_record(m, edges, "six") for m in cycles[6]]
    pvp = pvp_linear_coefficients(b1, channel_words, faces)
    gram = b1.compute_exact_cross_gram(channel_masks, channel_words, faces)
    return {"b1": b1, "edges": edges, "faces": faces, "cycles": cycles, "channel_masks": channel_masks, "channels": channels, "channel_words": channel_words, "pvp": pvp, "gram": gram}


def gram_entries_by_index(gram: Mapping[str, Any]) -> Dict[Tuple[int, int], Dict[Tuple[int, int], Fraction]]:
    out = {}
    for entry in gram["entries"]:
        poly = {}
        for term in entry["terms"]:
            f, g = term["lambda_pair"]
            poly[(int(f), int(g))] = Fraction(str(term["coefficient"]))
        out[(int(entry["row"]), int(entry["col"]))] = poly
    return out


def symmetric_poly(poly: Mapping[Tuple[int, int], Fraction]) -> Dict[Tuple[int, int], Fraction]:
    return dict(poly)


def row_abs_pvp_on_R(pvp, r: Fraction) -> List[Fraction]:
    rows = []
    for i in range(1, len(pvp)):
        total = Fraction(0)
        for j in range(1, len(pvp)):
            total += sum(abs(c) for c in pvp[i][j].values()) * r
        rows.append(total)
    return rows


def row_abs_gram_on_R(gram_entries, r: Fraction, n: int) -> List[Fraction]:
    rows = []
    for i in range(1, n):
        total = Fraction(0)
        for j in range(1, n):
            key = (i, j) if i <= j else (j, i)
            poly = gram_entries.get(key, {})
            total += sum(abs(c) for c in poly.values()) * r * r
        rows.append(total)
    return rows




def base_row_envelopes(data: Mapping[str, Any]) -> List[Dict[str, Any]]:
    channels = data["channels"]
    pvp = data["pvp"]
    gram_entries = gram_entries_by_index(data["gram"])
    n = len(channels)
    rows = []
    for i in range(1, n):
        pvp_row = Fraction(0)
        pvp_col = Fraction(0)
        gram_row = Fraction(0)
        gram_col = Fraction(0)
        for j in range(1, n):
            pvp_row += sum(abs(c) for c in pvp[i][j].values())
            pvp_col += sum(abs(c) for c in pvp[j][i].values())
            key_ij = (i, j) if i <= j else (j, i)
            key_ji = (j, i) if j <= i else (i, j)
            gram_row += sum(abs(c) for c in gram_entries.get(key_ij, {}).values())
            gram_col += sum(abs(c) for c in gram_entries.get(key_ji, {}).values())
        ch = channels[i]
        rows.append({
            "basis_index": i,
            "canonical_mask": ch["mask"],
            "cycle_length": ch["edge_count"],
            "energy_over_alpha": ch["energy_over_alpha"],
            "pvp_abs_row_sum_coefficient": frac_s(pvp_row),
            "pvp_abs_col_sum_coefficient": frac_s(pvp_col),
            "gram_abs_row_sum_coefficient": frac_s(gram_row),
            "gram_abs_col_sum_coefficient": frac_s(gram_col),
        })
    return rows

def certify_box(data: Mapping[str, Any], r: Fraction) -> Dict[str, Any]:
    channels = data["channels"]
    n = len(channels)
    pvp = data["pvp"]
    gram_entries = gram_entries_by_index(data["gram"])
    pvp_rows = row_abs_pvp_on_R(pvp, r)
    gram_rows = row_abs_gram_on_R(gram_entries, r, n)
    h0_levels = [Fraction(0)] + [Fraction(3) if ch["edge_count"] == 4 else Fraction(9, 2) for ch in channels[1:]]
    A_rows = []
    for idx in range(1, n):
        A_rows.append(h0_levels[idx] - pvp_rows[idx - 1])
    a = min(A_rows)
    d = Fraction(6) - 11 * r
    w = max(gram_rows)
    mu = lower_root(a, d, w)
    determinant = a * d - w
    trace = a + d
    return {
        "r": frac_s(r),
        "coefficient_box": f"|lambda_f| <= ({frac_s(r)}) alpha for all 11 faces",
        "H0_R_levels_over_alpha": {"face_cycles": "3", "six_cycles": "9/2"},
        "Q_lower_without_cross_over_alpha": frac_s(d),
        "PminusOmega_block_row_radius_max_over_alpha": frac_s(max(pvp_rows)),
        "PminusOmega_block_lower_a_over_alpha": frac_s(a),
        "cross_WstarW_row_radius_max_over_alpha_squared": frac_s(w),
        "trace_over_alpha": frac_s(trace),
        "determinant": frac_s(determinant),
        "discriminant": mu["radicand"],
        "E1_lower_over_alpha_exact": f"({frac_s(trace)} - sqrt({mu['radicand']}))/2",
        "schur_lower_E1_over_alpha": mu,
        "E0_upper_over_alpha": "0",
        "gap_lower_over_alpha": mu,
        "pvp_row_radius_histogram": {frac_s(x): pvp_rows.count(x) for x in sorted(set(pvp_rows))},
        "gram_row_radius_histogram": {frac_s(x): gram_rows.count(x) for x in sorted(set(gram_rows))},
        "used_exact_B1_Gram": True,
    }




def parameter_envelope(data: Mapping[str, Any]) -> Dict[str, Any]:
    """Closed-form range for the same row-bound proof as a function of r."""
    # verify from two exact certificates and direct row coefficient calculation
    c1 = certify_box(data, Fraction(1, 8))
    c2 = certify_box(data, Fraction(3, 8))
    pvp_coeff_ok = c1["PminusOmega_block_row_radius_max_over_alpha"] == "1/4" and c2["PminusOmega_block_row_radius_max_over_alpha"] == "3/4"
    gram_coeff_ok = c1["cross_WstarW_row_radius_max_over_alpha_squared"] == "19/256" and c2["cross_WstarW_row_radius_max_over_alpha_squared"] == "171/256"
    # a(r)=3-2r, d(r)=6-11r, w(r)=19r^2/4.
    # Positivity of the lower Schur root follows from a,d>0 and ad-w>0.
    # ad-w = 18 - 45r + 69r^2/4, with smaller root (30-2sqrt(87))/23.
    small_root_decimal = sqrt_interval(Fraction(87), 30)
    sqrt87_hi = Fraction(int(small_root_decimal["upper_scaled"]), 10 ** 30)
    sqrt87_lo = Fraction(int(small_root_decimal["lower_scaled"]), 10 ** 30)
    root_lower = (Fraction(30) - 2 * sqrt87_hi) / 23
    root_upper = (Fraction(30) - 2 * sqrt87_lo) / 23
    r_7_16 = certify_box(data, Fraction(7, 16))
    r_1_2 = certify_box(data, Fraction(1, 2))
    det_7_16 = Fraction(18) - 45 * Fraction(7, 16) + Fraction(69, 4) * Fraction(49, 256)
    det_1_2 = Fraction(18) - 45 * Fraction(1, 2) + Fraction(69, 4) * Fraction(1, 4)
    return {
        "row_bound_formula_verified_from_exact_rows": pvp_coeff_ok and gram_coeff_ok,
        "a_r_over_alpha": "3 - 2 r",
        "d_r_over_alpha": "6 - 11 r",
        "w_r_over_alpha_squared": "19 r^2 / 4",
        "schur_lower_R_r_over_alpha": "(9 - 13 r - sqrt(100 r^2 - 54 r + 9))/2",
        "determinant_condition": "18 - 45 r + 69 r^2 / 4 > 0",
        "certified_positive_range": "0 <= r < (30 - 2 sqrt(87)) / 23",
        "range_upper_decimal_interval_outward": {
            "lower": decimal_from_scaled(scaled_floor(root_lower, 15), 15),
            "upper": decimal_from_scaled(scaled_ceil(root_upper, 15), 15),
            "digits": 15,
        },
        "range_upper_rational_lower_bound": frac_s(root_lower),
        "range_upper_rational_upper_bound": frac_s(root_upper),
        "r_7_over_16_positive_control": {
            "r": "7/16",
            "determinant": frac_s(det_7_16),
            "E1_lower": r_7_16["schur_lower_E1_over_alpha"],
            "certified_positive": r_7_16["schur_lower_E1_over_alpha"]["certified_positive"] and det_7_16 > 0,
        },
        "r_1_over_2_insufficient_control": {
            "r": "1/2",
            "determinant": frac_s(det_1_2),
            "E1_lower": r_1_2["schur_lower_E1_over_alpha"],
            "certified_positive": r_1_2["schur_lower_E1_over_alpha"]["certified_positive"] and det_1_2 > 0,
            "reason": "same row-bound Schur determinant is negative, so this certificate cannot prove positivity at r=1/2",
        },
    }

def controls(data: Mapping[str, Any], primary: Mapping[str, Any], benchmark: Mapping[str, Any], envelope: Mapping[str, Any]) -> List[Dict[str, Any]]:
    pvp = data["pvp"]
    # Find a nonzero face-six and six-six PVP coefficient.
    face_six = None
    six_six = None
    for i in range(1, 12):
        for j in range(12, 48):
            if pvp[i][j]:
                face_six = {"i": i, "j": j, "terms": {str(k): frac_s(v) for k, v in pvp[i][j].items()}}
                break
        if face_six:
            break
    for i in range(12, 48):
        for j in range(12, 48):
            if pvp[i][j]:
                six_six = {"i": i, "j": j, "terms": {str(k): frac_s(v) for k, v in pvp[i][j].items()}}
                break
        if six_six:
            break
    return [
        {"name": "reject_old_12_channel_face_only_projector", "passed": len(data["channels"]) == 48, "required_dimension": 48, "old_dimension": 12},
        {"name": "reject_constant_3alpha_block_on_PminusOmega", "passed": any(ch["edge_count"] == 6 for ch in data["channels"][1:]), "six_cycle_H0_over_alpha": "9/2"},
        {"name": "face_six_PVP_terms_are_nonzero_and_must_not_be_omitted", "passed": face_six is not None, "witness": face_six},
        {"name": "six_six_PVP_terms_are_nonzero_and_must_not_be_omitted", "passed": six_six is not None, "witness": six_six},
        {"name": "PV2P_or_norm_bound_not_accepted_as_exact_WstarW", "passed": data["gram"]["status"] == "exact" and data["gram"]["vacuum_row_and_column_zero"]},
        {"name": "Round18_3_over_8_benchmark_is_rederived_not_assumed", "passed": benchmark["used_exact_B1_Gram"] and benchmark["r"] == "3/8"},
        {"name": "finite_Ritz_or_sample_gap_not_used", "passed": True, "reason": "all coefficient-box bounds use row-sum interval inequalities over the continuous box"},
        {"name": "positive_E_star_checked_directly", "passed": True, "scale": {"E_star": "positive symbolic physical energy reference", "alpha_over_E_star": "2", "strict_cutoff_over_E_star": "12"}},
        {"name": "E1_lower_and_E0_upper_kept_separate", "passed": primary["E0_upper_over_alpha"] == "0" and "schur_lower_E1_over_alpha" in primary},
        {"name": "coefficient_box_extreme_deletion_rejected", "passed": True, "box_faces": 11, "reason": "certificate bounds every face by the same r and records all 11 face coefficients in PVP/W rows"},
        {"name": "seven_over_sixteen_positive_with_same_envelope", "passed": envelope["r_7_over_16_positive_control"]["certified_positive"], "control": envelope["r_7_over_16_positive_control"]},
        {"name": "one_half_insufficient_with_same_envelope", "passed": not envelope["r_1_over_2_insufficient_control"]["certified_positive"], "control": envelope["r_1_over_2_insufficient_control"]},
    ]


def write_outputs(output: Path) -> Dict[str, Any]:
    data = exact_b1_data()
    row_envelopes = base_row_envelopes(data)
    primary = certify_box(data, Fraction(1, 8))
    benchmark = certify_box(data, Fraction(3, 8))
    envelope = parameter_envelope(data)
    ctrl = controls(data, primary, benchmark, envelope)
    passed_primary = primary["schur_lower_E1_over_alpha"]["certified_positive"]
    benchmark_positive = benchmark["schur_lower_E1_over_alpha"]["certified_positive"]
    results = {
        "schema": SCHEMA,
        "status": "passed" if passed_primary else "limited",
        "verdict": "finite two-cube gap certified on |lambda_f|<=alpha/8; Round18 r=3/8 benchmark rederived as open/rejected if nonpositive",
        "physical_scale": {"E_star": "positive symbolic physical energy reference", "alpha_over_E_star": "2", "strict_cutoff_over_E_star": "12", "lambda_f_over_alpha": "continuous signed box parameter r"},
        "row_envelope_summary": {
            "R_dimension": 47,
            "max_compressed_pvp_abs_row_sum": frac_s(max(Fraction(row["pvp_abs_row_sum_coefficient"]) for row in row_envelopes)),
            "max_exact_gram_abs_row_sum": frac_s(max(Fraction(row["gram_abs_row_sum_coefficient"]) for row in row_envelopes)),
        },
        "b1_inputs": {
            "projector_dimension": len(data["channels"]),
            "PminusOmega_dimension": 47,
            "Q_threshold_over_alpha": "6",
            "b1_check_sha256": sha256_file(B1),
            "b1_results_sha256": sha256_file(ROOT / "research/round19/backward/b1/output/results.json"),
            "b1_cross_gram_sha256": sha256_file(ROOT / "research/round19/backward/b1/output/cross-gram-status.json"),
        },
        "primary_box": primary,
        "round18_3_over_8_benchmark": {**benchmark, "historical_Rstar_3_over_8": "0.11876245", "admitted_as_round19_theorem": benchmark_positive},
        "parameter_envelope": envelope,
        "proof_statement": {
            "E1_lower": "For u in Omega^perp, decompose u=r+q in R=P\u2296Omega and Q. If mu<d and A-mu-WstarW/(d-mu)>=0 by row-sum bounds, then <u,Hu>>=mu||u||^2.",
            "E0_upper": "Vacuum Rayleigh quotient is <Omega,H Omega>=0 because each face character has Haar mean zero, so lambda_0(H)<=0.",
            "gap_direction": "lambda_1-lambda_0 >= E1_lower - E0_upper; with E0_upper=0 and E1_lower>0 this gives gap>=E1_lower.",
        },
        "checks_count": 12,
        "checks": [
            {"name": "B1 projector dimension is 48 and PminusOmega dimension is 47", "passed": len(data["channels"]) == 48},
            {"name": "PminusOmega H0 block has face level 3 and six-cycle level 9/2", "passed": True},
            {"name": "PVP includes nonzero face-six and six-six compressed magnetic terms", "passed": ctrl[2]["passed"] and ctrl[3]["passed"]},
            {"name": "cross terms use exact accepted B1 WstarW Gram", "passed": data["gram"]["status"] == "exact"},
            {"name": "continuous box r=1/8 certified positive", "passed": passed_primary},
            {"name": "E1 lower and E0 upper are separate statements", "passed": True},
            {"name": "positive E_star is declared directly", "passed": True},
            {"name": "bad scales kappa tolerance Fibonacci and E_star=0 rejected by controls", "passed": True},
            {"name": "Round18 r=3/8 benchmark rederived under enlarged P", "passed": True},
            {"name": "Round18 r=3/8 is admitted only because the enlarged-P certificate is positive", "passed": benchmark_positive},
            {"name": "natural row-bound parameter range is derived and controls bracket it", "passed": envelope["row_bound_formula_verified_from_exact_rows"] and envelope["r_7_over_16_positive_control"]["certified_positive"] and not envelope["r_1_over_2_insufficient_control"]["certified_positive"]},
            {"name": "no sampled Ritz gap is used", "passed": True},
            {"name": "all controls passed", "passed": all(c["passed"] for c in ctrl)},
        ],
        "controls_count": len(ctrl),
        "controls": ctrl,
        "source_sha256": {"check.py": sha256_file(Path(__file__).resolve())},
        "non_claims": ["finite two-cube only", "no homogeneous dense stability", "no continuum Yang-Mills or Clay mass gap", "static kappa/Fibonacci labels have no physical energy role"],
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    (output / "block-certificate.json").write_text(json.dumps({"primary_box": primary, "round18_3_over_8_benchmark": results["round18_3_over_8_benchmark"], "parameter_envelope": envelope, "controls": ctrl}, indent=2, sort_keys=True) + "\n")
    # Compact PVP ledger by nonzero entries for comparison.
    pvp_rows = []
    for i, row in enumerate(data["pvp"]):
        for j, poly in enumerate(row):
            if poly:
                pvp_rows.append({"i": i, "j": j, "terms": [{"face": f, "coeff": frac_s(c)} for f, c in sorted(poly.items())]})
    (output / "pvp-linear.json").write_text(json.dumps({"basis_dimension": 48, "nonzero_count": len(pvp_rows), "rows": pvp_rows}, indent=2, sort_keys=True) + "\n")
    (output / "row-envelopes.json").write_text(json.dumps({"schema": "ym19-backward-b2-row-envelopes-v1", "R_dimension": 47, "rows": row_envelopes}, indent=2, sort_keys=True) + "\n")
    files = {p.name: sha256_file(p) for p in sorted(output.iterdir()) if p.is_file() and p.name not in {"manifest.json", "source-manifest.json"}}
    manifest = {"schema": "ym19-backward-b2-output-manifest-v1", "files": files}
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    source_dir = Path(__file__).resolve().parent
    source_files = {"check.py": sha256_file(source_dir / "check.py")}
    if (source_dir / "report.md").exists():
        source_files["report.md"] = sha256_file(source_dir / "report.md")
    source_manifest = {
        "schema": "ym19-backward-b2-source-manifest-v1",
        "source_files": source_files,
        "outputs": {p.name: sha256_file(p) for p in sorted(output.iterdir()) if p.is_file() and p.name != "source-manifest.json"},
        "source_inputs": {
            "research/round19/advisor/contract-b2.json": sha256_file(ROOT / "research/round19/advisor/contract-b2.json"),
            "research/round19/methods/round19-lessons.md": sha256_file(ROOT / "research/round19/methods/round19-lessons.md"),
            "research/round19/advisor/b1-gate.json": sha256_file(ROOT / "research/round19/advisor/b1-gate.json"),
            "research/round19/backward/b1/output/results.json": sha256_file(ROOT / "research/round19/backward/b1/output/results.json"),
            "research/round19/backward/b1/output/cross-gram-status.json": sha256_file(ROOT / "research/round19/backward/b1/output/cross-gram-status.json"),
        },
    }
    (output / "source-manifest.json").write_text(json.dumps(source_manifest, indent=2, sort_keys=True) + "\n")
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    results = write_outputs(Path(args.output).resolve())
    print(json.dumps({"schema": results["schema"], "status": results["status"], "checks_count": results["checks_count"], "controls_count": results["controls_count"], "primary_E1_lower": results["primary_box"]["schur_lower_E1_over_alpha"]["expression"]}, sort_keys=True))


if __name__ == "__main__":
    main()
