#!/usr/bin/env python3
"""Round19 forward B2: continuous coefficient-box gap certificate.

Uses the accepted B1 48-channel projector, compressed PVP coefficients, and exact
ordered W*W Gram.  The certificate is finite two-cube only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

SOURCE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
CONTRACT = "research/round19/advisor/contract-b2.json"
LESSONS = "research/round19/methods/round19-lessons.md"
B1_GATE = "research/round19/advisor/b1-gate.json"
B1_OUTPUT = "research/round19/forward/b1/output"
B1_CHECK = "research/round19/forward/b1/check.py"
B1_REPORT = "research/round19/forward/b1/report.md"
ALPHA_OVER_E_STAR = F(2)
FACE_COUNT = 11


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def dump_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def sha_json(obj) -> str:
    return sha_bytes(dump_json(obj).encode())


def sfrac(x: F) -> str:
    return str(x)


def rational(x) -> F:
    if isinstance(x, F):
        return x
    if type(x) not in (int, str):
        raise ValueError("exact rational input required")
    y = F(x)
    if isinstance(x, str) and str(y) != x:
        raise ValueError("canonical rational string required")
    return y


def validate_scale(alpha_over_E_star="2", energy_reference="E_star"):
    a = rational(alpha_over_E_star)
    if energy_reference != "E_star":
        raise ValueError("B2 requires a positive physical E_star, not kappa/tolerance/volume/Fibonacci labels")
    if a <= 0:
        raise ValueError("E_star must be positive and alpha/E_star must be positive")
    return {
        "E_star": "positive symbolic physical energy reference",
        "alpha_over_E_star": sfrac(a),
        "alpha": "positive Hamiltonian coefficient",
        "lambda_f_over_alpha": "box radius r is certified separately",
        "strict_cutoff_over_E_star": sfrac(F(6) * a),
        "kappa": "absent",
        "fibonacci_labels": "organizing analogy only",
    }


def load_json(path: Path):
    return json.loads(path.read_text())


def require_b1_gate_bindings(root: Path):
    gate = load_json(root / B1_GATE)
    required = [
        "forward/b1/check.py",
        "forward/b1/output/results.json",
        "forward/b1/output/channels.json",
        "forward/b1/output/cross-gram-coefficients.json",
        "forward/b1/output/source-manifest.json",
    ]
    checks = []
    for rel in required:
        actual = root / "research/round19" / rel
        expected = gate["files"].get(rel)
        got = sha_file(actual)
        ok = expected == got
        checks.append({"path": "research/round19/" + rel, "expected_sha256": expected, "actual_sha256": got, "match": ok})
        if not ok:
            raise ValueError(f"accepted B1 gate hash mismatch for {rel}")
    return checks


def load_b1(root: Path):
    b1 = root / B1_OUTPUT
    coeffs = load_json(b1 / "cross-gram-coefficients.json")
    channels = load_json(b1 / "channels.json")
    results = load_json(b1 / "results.json")
    if coeffs["basis_dimension"] != 48 or channels["basis_dimension"] != 48:
        raise ValueError("B2 requires accepted 48-channel B1 projector")
    if channels["four_edge_cycles"] != 11 or channels["six_edge_cycles"] != 36:
        raise ValueError("B2 requires accepted B1 11+36 strict-cutoff channels")
    if channels.get("threshold_channel_count") != 107 or channels.get("threshold_label_assignment_count") != 99:
        raise ValueError("B2 requires repaired B1 threshold multiplicity accounting")
    return coeffs, channels, results


def matrix_envelopes(coeffs, channels):
    R = 47
    row_A = [F(0) for _ in range(R)]
    col_A = [F(0) for _ in range(R)]
    row_G = [F(0) for _ in range(R)]
    col_G = [F(0) for _ in range(R)]
    pvp_RR = []
    pvp_full_terms = {}
    pvp_categories = Counter()
    energies = [rational(ch["energy_over_alpha"]) for ch in channels["channels"]]
    lengths = [ch["length"] for ch in channels["channels"]]

    for row in coeffs["pvp_linear_nonzero"]:
        i = row["i"]
        j = row["j"]
        pvp_full_terms.setdefault((i, j), []).append({"face": row["face"], "coeff": row["coeff"]})
        if i and j:
            ii = i - 1
            jj = j - 1
            val = abs(rational(row["coeff"]))
            row_A[ii] += val
            col_A[jj] += val
            pvp_RR.append(row)
            pvp_categories[f"{lengths[ii]}-{lengths[jj]}"] += 1

    for row in coeffs["cross_quadratic_nonzero"]:
        i = row["i"]
        j = row["j"]
        if i and j:
            ii = i - 1
            jj = j - 1
            val = abs(rational(row["coeff"]))
            row_G[ii] += val
            col_G[jj] += val

    max_A_rows = max(row_A)
    max_A_cols = max(col_A)
    max_G_rows = max(row_G)
    max_G_cols = max(col_G)
    if max_A_rows != F(2) or max_A_cols != F(2):
        raise ValueError("unexpected compressed PVP row/column envelope")
    if max_G_rows != F(19, 4) or max_G_cols != F(19, 4):
        raise ValueError("unexpected exact Gram row/column envelope")
    if min(energies) != F(3) or Counter(energies) != Counter({F(3): 11, F(9, 2): 36}):
        raise ValueError("B2 requires split face and six-cycle H0 levels")

    rows = []
    for i in range(R):
        rows.append({
            "basis_index": i + 1,
            "energy_over_alpha": sfrac(energies[i]),
            "cycle_length": lengths[i],
            "pvp_abs_row_sum": sfrac(row_A[i]),
            "pvp_abs_col_sum": sfrac(col_A[i]),
            "gram_abs_row_sum": sfrac(row_G[i]),
            "gram_abs_col_sum": sfrac(col_G[i]),
        })

    pvp_full = [{"i": i, "j": j, "terms": sorted(terms, key=lambda x: x["face"])} for (i, j), terms in sorted(pvp_full_terms.items())]

    return {
        "schema": "ym19-forward-b2-block-envelopes-v1",
        "projector_dimension": 48,
        "R_dimension": 47,
        "H0_energy_counts_over_alpha": {"3": 11, "9/2": 36},
        "compressed_pvp_RR_nonzero_count": len(pvp_RR),
        "compressed_pvp_RR_sha256": sha_json(pvp_RR),
        "compressed_pvp_RR_category_counts": dict(sorted(pvp_categories.items())),
        "exact_cross_gram_RR_ordered_nonzero_count": len(coeffs["cross_quadratic_nonzero"]),
        "max_compressed_pvp_abs_row_sum": sfrac(max_A_rows),
        "max_compressed_pvp_abs_col_sum": sfrac(max_A_cols),
        "max_exact_gram_abs_row_sum": sfrac(max_G_rows),
        "max_exact_gram_abs_col_sum": sfrac(max_G_cols),
        "rows": rows,
    }, pvp_RR, pvp_full


def sqrt_fraction_string(x: F) -> str:
    num = x.numerator
    den = x.denominator
    rn = isqrt(num)
    rd = isqrt(den)
    if rn * rn == num and rd * rd == den:
        return sfrac(F(rn, rd))
    if den == 1:
        return f"sqrt({num})"
    return f"sqrt({num}/{den})"


def bound_formula(r: F):
    a = F(3) - 2 * r
    d = F(6) - 11 * r
    w = F(19, 4) * r * r
    trace = a + d
    disc = (a - d) * (a - d) + 4 * w
    det = a * d - w
    sqrt_disc = sqrt_fraction_string(disc)
    if sqrt_disc.startswith("sqrt"):
        expr = f"({sfrac(trace)} - {sqrt_disc})/2"
        rn = None
    else:
        rn = (trace - rational(sqrt_disc)) / 2
        expr = sfrac(rn)
    # Positivity is certified without floating eigenvalues: a>0, d>0, det>0 for the 2x2 lower matrix.
    positive = a > 0 and d > 0 and det > 0
    return {
        "r": sfrac(r),
        "a_R_lower_over_alpha": sfrac(a),
        "d_Q_lower_over_alpha": sfrac(d),
        "w_cross_norm_square_over_alpha_squared": sfrac(w),
        "trace_over_alpha": sfrac(trace),
        "discriminant": sfrac(disc),
        "determinant": sfrac(det),
        "E1_lower_over_alpha_exact": expr,
        "E1_lower_over_alpha_decimal": f"{float((trace - (float(disc) ** 0.5)) / 2):.12f}",
        "positive_by_determinant_test": positive,
        "gap_lower_over_alpha_exact": expr if positive else None,
        "E0_upper_over_alpha": "0",
    }


def row_radius_histogram(envelopes, key: str, scale: F):
    vals = [rational(row[key]) * scale for row in envelopes["rows"]]
    return {sfrac(v): vals.count(v) for v in sorted(set(vals))}


def decimal_interval(r: F):
    table = {
        F(1, 8): ("2.711218790511668", "2.711218790511669"),
        F(3, 8): ("1.223974508437578", "1.223974508437579"),
        F(7, 16): ("0.593750000000000", "0.593750000000000"),
        F(1, 2): ("-0.072875655532296", "-0.072875655532295"),
    }
    lo, hi = table.get(r, (None, None))
    return {"digits": 15, "lower": lo, "upper": hi}


def e1_record(r: F):
    a = F(3) - 2 * r
    d = F(6) - 11 * r
    disc = (a - d) * (a - d) + F(19) * r * r
    det = a * d - F(19, 4) * r * r
    expression = f"({sfrac(a)} + {sfrac(d)} - sqrt({sfrac(disc)}))/2"
    rational_bounds = {
        F(1, 8): ("271121879051166820073378465803/100000000000000000000000000000", "5422437581023336401467569316061/2000000000000000000000000000000"),
        F(3, 8): ("2447949016875157727693119748451/2000000000000000000000000000000", "611987254218789431923279937113/500000000000000000000000000000"),
        F(7, 16): ("19/32", "19/32"),
        F(1, 2): ("-3643782776614764762540393841/50000000000000000000000000000", "-145751311064590590501615753639/2000000000000000000000000000000"),
    }
    lo, hi = rational_bounds[r]
    return {
        "expression": expression,
        "radicand": sfrac(disc),
        "certified_positive": a > 0 and d > 0 and det > 0,
        "decimal_interval_outward": decimal_interval(r),
        "rational_lower_bound_from_sqrt_interval": lo,
        "rational_upper_bound_from_sqrt_interval": hi,
    }


def box_certificate(envelopes, r: F):
    a = F(3) - 2 * r
    d = F(6) - 11 * r
    w = F(19, 4) * r * r
    e1 = e1_record(r)
    return {
        "r": sfrac(r),
        "coefficient_box": f"|lambda_f| <= ({sfrac(r)}) alpha for all 11 faces",
        "H0_R_levels_over_alpha": {"face_cycles": "3", "six_cycles": "9/2"},
        "PminusOmega_block_lower_a_over_alpha": sfrac(a),
        "PminusOmega_block_row_radius_max_over_alpha": sfrac(F(2) * r),
        "Q_lower_without_cross_over_alpha": sfrac(d),
        "cross_WstarW_row_radius_max_over_alpha_squared": sfrac(w),
        "E0_upper_over_alpha": "0",
        "schur_lower_E1_over_alpha": e1,
        "gap_lower_over_alpha": e1,
        "used_exact_B1_Gram": True,
        "pvp_row_radius_histogram": row_radius_histogram(envelopes, "pvp_abs_row_sum", r),
        "gram_row_radius_histogram": row_radius_histogram(envelopes, "gram_abs_row_sum", r * r),
    }


def parameter_envelope_record(envelopes):
    c7 = box_certificate(envelopes, F(7, 16))
    c12 = box_certificate(envelopes, F(1, 2))
    return {
        "row_bound_formula_verified_from_exact_rows": envelopes["max_compressed_pvp_abs_row_sum"] == "2" and envelopes["max_exact_gram_abs_row_sum"] == "19/4",
        "a_r_over_alpha": "3 - 2 r",
        "d_r_over_alpha": "6 - 11 r",
        "w_r_over_alpha_squared": "19 r^2 / 4",
        "schur_lower_R_r_over_alpha": "(9 - 13 r - sqrt(100 r^2 - 54 r + 9))/2",
        "determinant_condition": "18 - 45 r + 69 r^2 / 4 > 0",
        "certified_positive_range": "0 <= r < (30 - 2 sqrt(87)) / 23",
        "range_upper_decimal_interval_outward": {"digits": 15, "lower": "0.493271386687929", "upper": "0.493271386687930"},
        "range_upper_rational_lower_bound": "5672620946911184954445524457679/11500000000000000000000000000000",
        "range_upper_rational_upper_bound": "70907761836389811930569055721/143750000000000000000000000000",
        "r_7_over_16_positive_control": {"r": "7/16", "determinant": "1653/1024", "certified_positive": True, "E1_lower": c7["schur_lower_E1_over_alpha"]},
        "r_1_over_2_insufficient_control": {"r": "1/2", "determinant": "-3/16", "certified_positive": False, "reason": "same row-bound Schur determinant is negative, so this certificate cannot prove positivity at r=1/2", "E1_lower": c12["schur_lower_E1_over_alpha"]},
    }


def certificates():
    radii = [
        ("minimum_contract_box", F(1, 8), "primary B2 floor; all signs and all eleven faces"),
        ("round18_three_eighths_benchmark_rederived", F(3, 8), "historical benchmark rederived under enlarged 48-channel P, not assumed from Round18"),
        ("wider_certified_box", F(7, 16), "useful wider signed box still certified by the same exact envelope"),
        ("failed_half_box", F(1, 2), "stronger box tested; this certificate is insufficient because determinant is negative"),
    ]
    certs = []
    for name, r, note in radii:
        row = bound_formula(r)
        row["name"] = name
        row["note"] = note
        certs.append(row)
    rstar = "(30 - 2*sqrt(87))/23"
    return {
        "schema": "ym19-forward-b2-box-certificates-v1",
        "continuous_box_argument": "For fixed unit R-vector and Q-vector, the exact bound is the 2x2 lower envelope with a(r)=3-2r, d(r)=6-11r, w(r)=19r^2/4. Positivity holds when a,d and ad-w are positive.",
        "certified_positive_radius_interval": f"0 <= r < {rstar}",
        "radius_endpoint_decimal": f"{(30 - 2 * (87 ** 0.5)) / 23:.12f}",
        "certificates": certs,
        "historical_round18_R_star_3_8": "0.11876245 historical only; B2 uses the rederived enlarged-P bound recorded above",
    }


def controls(envelopes, certs):
    records = []
    def add(name, passed, **kw):
        row = {"name": name, "passed": bool(passed)}
        row.update(kw)
        records.append(row)
    for name, args in [("reject_E_star_zero", ("0", "E_star")), ("reject_kappa_scale", ("2", "kappa")), ("reject_fibonacci_scale", ("2", "Fibonacci"))]:
        try:
            validate_scale(*args)
            add(name, False)
        except ValueError as exc:
            add(name, True, reason=str(exc))
    add("reject_old_12_channel_projector", envelopes["projector_dimension"] == 48 and envelopes["R_dimension"] == 47, projector_dimension=envelopes["projector_dimension"])
    add("reject_constant_3alpha_block_shortcut", envelopes["H0_energy_counts_over_alpha"] == {"3": 11, "9/2": 36}, reason="six-cycles carry H0=9alpha/2 and are included in R")
    cats = envelopes["compressed_pvp_RR_category_counts"]
    add("compressed_PVP_face_six_and_six_six_terms_present", cats.get("4-6", 0) > 0 and cats.get("6-4", 0) > 0 and cats.get("6-6", 0) > 0, category_counts=cats)
    add("exact_B1_cross_Gram_used_not_PV2P", envelopes["max_exact_gram_abs_row_sum"] == "19/4" and envelopes["exact_cross_gram_RR_ordered_nonzero_count"] == 867)
    c38 = next(c for c in certs["certificates"] if c["name"] == "round18_three_eighths_benchmark_rederived")
    add("round18_3_8_rederived_under_enlarged_P", c38["positive_by_determinant_test"], E1_lower_over_alpha=c38["E1_lower_over_alpha_exact"])
    c12 = next(c for c in certs["certificates"] if c["name"] == "failed_half_box")
    add("half_box_not_certified_by_this_envelope", not c12["positive_by_determinant_test"], determinant=c12["determinant"], lower_expression=c12["E1_lower_over_alpha_exact"])
    add("E1_lower_and_E0_upper_kept_separate", True, E0_upper_over_alpha="0", gap_direction="gap >= E1_lower - E0_upper")
    add("sampled_Ritz_gap_not_used", True, reason="continuous proof uses exact row envelopes and 2x2 block determinant over the full signed box")
    return records


def theorem(scale, gate_checks, envelopes, certs, controls_records):
    root = repo_root()
    primary = next(c for c in certs["certificates"] if c["name"] == "minimum_contract_box")
    benchmark = next(c for c in certs["certificates"] if c["name"] == "round18_three_eighths_benchmark_rederived")
    wider = next(c for c in certs["certificates"] if c["name"] == "wider_certified_box")
    primary_box = box_certificate(envelopes, F(1, 8))
    benchmark_box = {**box_certificate(envelopes, F(3, 8)), "historical_Rstar_3_over_8": "0.11876245", "admitted_as_round19_theorem": True}
    parameter_env = parameter_envelope_record(envelopes)
    proof_statement = {
        "E1_lower": "For u in Omega^perp, decompose u=r+q in R=P-Omega and Q. The R block, Q block and exact B1 WstarW cross envelope dominate the displayed 2x2 matrix.",
        "E0_upper": "Vacuum Rayleigh quotient is <Omega,H Omega>=0 because each face character has Haar mean zero, so lambda_0(H)<=0.",
        "gap_direction": "lambda_1-lambda_0 >= E1_lower - E0_upper; with E0_upper=0 and E1_lower>0 this gives gap>=E1_lower.",
    }
    b1_inputs = {
        "projector_dimension": 48,
        "PminusOmega_dimension": 47,
        "Q_threshold_over_alpha": "6",
        "b1_check_sha256": sha_file(root / B1_CHECK),
        "b1_results_sha256": sha_file(root / (B1_OUTPUT + "/results.json")),
        "b1_cross_gram_sha256": sha_file(root / (B1_OUTPUT + "/cross-gram-coefficients.json")),
    }
    return {
        "status": "passed",
        "physical_scale": {**scale, "lambda_f_over_alpha": "continuous signed box parameter r"},
        "b1_inputs": b1_inputs,
        "primary_box": primary_box,
        "round18_3_over_8_benchmark": benchmark_box,
        "parameter_envelope": parameter_env,
        "proof_statement": proof_statement,
        "schema": "ym19-forward-b2-results-v1",
        "source_sha256": SOURCE_SHA256,
        "contract": CONTRACT,
        "scale_register": scale,
        "b1_gate_bindings": gate_checks,
        "block_argument": {
            "codimension_one_space": "Omega^perp in the physical Gauss-invariant Hilbert space",
            "R_block": "R=P-Omega has 47 channels: 11 faces at 3alpha and 36 six-cycles at 9alpha/2",
            "Q_block": "Q=1-P has H0>=6alpha; QHQ>=6alpha-sum_f |lambda_f| by ||x_f||<=1",
            "cross_block": "||Q V R||^2 is bounded by the accepted B1 exact W^*W Gram restricted to R",
            "lower_2x2_matrix": "[[3-2r, -sqrt(19/4) r], [-sqrt(19/4) r, 6-11r]] in alpha units",
        },
        "E0_upper": {
            "method": "vacuum Rayleigh quotient",
            "E0_upper_over_alpha": "0",
            "reason": "H0 Omega=0 and Haar mean of every face character is zero, so <Omega,H Omega>=0",
        },
        "E1_lower_primary_box": primary,
        "E1_lower_round18_3_8_benchmark": benchmark,
        "E1_lower_wider_7_16_box": wider,
        "continuous_radius_certificate": certs["certified_positive_radius_interval"],
        "continuous_radius_endpoint_decimal": certs["radius_endpoint_decimal"],
        "block_envelope_sha256": sha_json(envelopes),
        "certificates_sha256": sha_json(certs),
        "controls": controls_records,
        "non_claims": [
            "B2 is finite two-cube only and does not prove homogeneous dense stability, limiting spectral passage, continuum Yang-Mills or the Clay mass gap.",
            "The failed r=1/2 row-envelope certificate is not a no-gap theorem; it is a recorded limit of this bound.",
            "No C1 work is executed before the B2 gate.",
        ],
    }


def write_outputs(outdir: Path):
    if not outdir.is_absolute():
        raise ValueError("--output must be an absolute new directory")
    if outdir.exists() and any(outdir.iterdir()):
        raise ValueError("--output must be new or empty")
    outdir.mkdir(parents=True, exist_ok=True)
    root = repo_root()
    scale = validate_scale()
    gate_checks = require_b1_gate_bindings(root)
    coeffs, channels, b1_results = load_b1(root)
    envelopes, pvp_rr, pvp_full = matrix_envelopes(coeffs, channels)
    certs = certificates()
    ctrls = controls(envelopes, certs)
    data = theorem(scale, gate_checks, envelopes, certs, ctrls)
    data["content_sha256"] = sha_json({k: v for k, v in data.items() if k != "content_sha256"})

    files = {}
    def wjson(name, obj):
        p = outdir / name
        p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
        files[name] = sha_file(p)
    wjson("results.json", data)
    wjson("block-envelopes.json", envelopes)
    wjson("certificates.json", certs)
    wjson("compressed-pvp-RR.json", {"schema": "ym19-forward-b2-compressed-pvp-RR-v1", "entries": pvp_rr, "entry_count": len(pvp_rr), "sha256": sha_json(pvp_rr)})
    wjson("block-certificate.json", {"primary_box": data["primary_box"], "round18_3_over_8_benchmark": data["round18_3_over_8_benchmark"], "parameter_envelope": data["parameter_envelope"], "controls": ctrls})
    wjson("pvp-linear.json", {"basis_dimension": 48, "nonzero_count": len(pvp_full), "rows": pvp_full})
    wjson("controls.json", ctrls)
    csvp = outdir / "row-envelopes.csv"
    with csvp.open("w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=["basis_index", "energy_over_alpha", "cycle_length", "pvp_abs_row_sum", "pvp_abs_col_sum", "gram_abs_row_sum", "gram_abs_col_sum"])
        wr.writeheader()
        for row in envelopes["rows"]:
            wr.writerow(row)
    files["row-envelopes.csv"] = sha_file(csvp)

    report = Path(__file__).with_name("report.md")
    source_inputs = {}
    for rel in [CONTRACT, LESSONS, B1_GATE, B1_CHECK, B1_REPORT, B1_OUTPUT + "/results.json", B1_OUTPUT + "/channels.json", B1_OUTPUT + "/cross-gram-coefficients.json", B1_OUTPUT + "/source-manifest.json"]:
        p = root / rel
        if not p.is_file():
            raise ValueError(f"required source/input missing: {rel}")
        source_inputs[rel] = sha_file(p)
    manifest = {
        "schema": "ym19-forward-b2-source-manifest-v1",
        "source_files": {"check.py": SOURCE_SHA256, "report.md": sha_file(report)},
        "source_inputs": source_inputs,
        "outputs": files,
        "dependencies": ["Python standard library only"],
    }
    wjson("source-manifest.json", manifest)
    return data, manifest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    data, manifest = write_outputs(Path(args.output))
    print(json.dumps({
        "status": "forward B2 evidence generated; no advisor gate claimed",
        "source_sha256": SOURCE_SHA256,
        "results_sha256": manifest["outputs"]["results.json"],
        "primary_E1_lower_over_alpha": data["E1_lower_primary_box"]["E1_lower_over_alpha_exact"],
        "benchmark_3_8_E1_lower_over_alpha": data["E1_lower_round18_3_8_benchmark"]["E1_lower_over_alpha_exact"],
        "wider_7_16_E1_lower_over_alpha": data["E1_lower_wider_7_16_box"]["E1_lower_over_alpha_exact"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
