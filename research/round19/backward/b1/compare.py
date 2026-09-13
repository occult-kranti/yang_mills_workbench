#!/usr/bin/env python3
"""Round19 B1 independent comparison against an actual producer schema.

API kept compatible with root replay:
  python3 compare.py --producer SOURCE --evidence FORWARD_OUTPUT --output NEW_DIR

`--producer` may be a source file or source directory.  `--evidence` is the
producer output directory.  The comparator reruns this backward checker once into
NEW_DIR/independent unless that directory already contains a fresh reconstruction.
It compares canonical coordinate masks, threshold multiplicities, physical scale,
source-manifest hashes and the full commutative cross-Gram polynomial.  Mutation
controls use the same admission predicate on altered in-memory normalized inputs;
control-name presence is not accepted as falsification.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

HERE = Path(__file__).resolve().parent
CHECK = HERE / "check.py"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def frac_norm(x: Any) -> str:
    q = Fraction(str(x))
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"




def scale_has_positive_E_star(scale: Mapping[str, Any]) -> bool:
    val = scale.get("E_star")
    if val is True:
        return True
    if isinstance(val, (int, float)):
        return val > 0
    text = str(val).strip().lower() if val is not None else ""
    if not text or text in {"0", "0.0", "zero", "none", "null", "false"}:
        return False
    forbidden = ["e_star=0", "kappa", "tolerance", "fibonacci", "volume"]
    if any(word in text for word in forbidden):
        return False
    return "positive" in text or "reference" in text or "energy" in text

def abs_path(path: str | Path) -> Path:
    return Path(path).resolve()


def canonical_edge_maps(graph: Mapping[str, Any]) -> Tuple[Dict[int, int], Dict[int, int], List[Tuple[Tuple[int, int, int], Tuple[int, int, int]]]]:
    """Return old edge id -> canonical id and orientation sign.

    Canonical id order is lexicographic by unordered endpoint pair, independent of
    producer edge numbering.  Orientation sign is +1 when the producer tail/head
    agrees with the canonical directed endpoint pair and -1 otherwise.
    """
    edges = graph.get("edges", [])
    triples = []
    for e in edges:
        old = int(e["id"])
        tail = tuple(int(x) for x in e["tail"])
        head = tuple(int(x) for x in e["head"])
        lo, hi = (tail, head) if tail <= head else (head, tail)
        orient = 1 if (tail, head) == (lo, hi) else -1
        triples.append((old, lo, hi, orient))
    ordered = sorted(triples, key=lambda t: (t[1], t[2]))
    id_map = {old: i for i, (old, _lo, _hi, _orient) in enumerate(ordered)}
    sign_map = {old: orient for old, _lo, _hi, orient in triples}
    edge_pairs = [(lo, hi) for _old, lo, hi, _orient in ordered]
    return id_map, sign_map, edge_pairs


def mask_from_ids(ids: Iterable[int]) -> str:
    m = 0
    for eid in ids:
        m |= 1 << int(eid)
    return f"{m:05x}"


def canonical_support_mask(support: Iterable[int], id_map: Mapping[int, int]) -> str:
    return mask_from_ids(id_map[int(e)] for e in support)




def canonical_closed_word(word: Sequence[Tuple[int, int]]) -> Tuple[Tuple[int, int], ...]:
    if not word:
        return tuple()
    variants = []
    n = len(word)
    seq = list(word)
    rev = [(edge, -sign) for edge, sign in reversed(seq)]
    for candidate in (seq, rev):
        for k in range(n):
            variants.append(tuple(candidate[k:] + candidate[:k]))
    return min(variants)

def face_word_items(face: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]:
    if "signed_word" in face:
        return face["signed_word"]
    return face["word"]


def canonical_face_records(graph: Mapping[str, Any]) -> List[Dict[str, Any]]:
    id_map, sign_map, edge_pairs = canonical_edge_maps(graph)
    out = []
    for face in graph.get("faces", []):
        signed = []
        support = []
        path_vertices = []
        closed_ordered_path = True
        for item in face_word_items(face):
            old = int(item["edge"])
            cid = id_map[old]
            sign = int(item["sign"]) * sign_map[old]
            signed.append((cid, sign))
            support.append(cid)
            lo, hi = edge_pairs[cid]
            tail, head = (lo, hi) if sign == 1 else (hi, lo)
            if not path_vertices:
                path_vertices.append(tail)
            elif path_vertices[-1] != tail:
                closed_ordered_path = False
            path_vertices.append(head)
        if len(path_vertices) < 2 or path_vertices[0] != path_vertices[-1]:
            closed_ordered_path = False
        out.append({
            "producer_face_id": int(face.get("id", len(out))),
            "mask": mask_from_ids(support),
            "signed_edges_sorted": tuple(sorted(signed)),
            "canonical_ordered_word": canonical_closed_word(signed),
            "closed_ordered_path": closed_ordered_path,
        })
    return sorted(out, key=lambda r: (r["mask"], r["canonical_ordered_word"]))


def canonical_graph_signature(graph: Mapping[str, Any]) -> Dict[str, Any]:
    _id_map, _sign_map, pairs = canonical_edge_maps(graph)
    vertices = sorted(tuple(int(x) for x in v) for v in graph.get("vertices", []))
    faces = canonical_face_records(graph)
    return {
        "vertices": vertices,
        "edges": pairs,
        "face_count": len(faces),
        "face_masks": sorted(f["mask"] for f in faces),
        "signed_face_edge_sets": sorted(f["signed_edges_sorted"] for f in faces),
        "canonical_face_words": sorted(f["canonical_ordered_word"] for f in faces),
        "all_faces_closed_ordered_paths": all(f["closed_ordered_path"] and len(f["canonical_ordered_word"]) == 4 for f in faces),
    }


def independent_channel_masks(channels: Mapping[str, Any], graph: Mapping[str, Any]) -> Dict[int, str]:
    id_map, _sign_map, _pairs = canonical_edge_maps(graph)
    rows = channels.get("retained_channels") or []
    out: Dict[int, str] = {}
    for idx, row in enumerate(rows):
        if str(row.get("mask")) == "00000" or row.get("kind") == "vacuum":
            out[idx] = "00000"
        else:
            # Backward masks are in its native edge order; canonicalize from the set bits.
            native = int(str(row["mask"]), 16)
            support = [i for i in range(64) if native & (1 << i)]
            out[idx] = canonical_support_mask(support, id_map)
    return out


def producer_channel_masks(channels: Mapping[str, Any], graph: Mapping[str, Any]) -> Dict[int, str]:
    id_map, _sign_map, _pairs = canonical_edge_maps(graph)
    out: Dict[int, str] = {0: "00000"}
    for row in channels.get("channels", []):
        out[int(row["basis_index"])] = canonical_support_mask(row["support"], id_map)
    # Also support backward-like schema for self-tests.
    if not channels.get("channels") and channels.get("retained_channels"):
        return independent_channel_masks(channels, graph)
    return dict(sorted(out.items()))


def canonical_face_id_map(graph: Mapping[str, Any]) -> Dict[int, str]:
    id_map, _sign_map, _pairs = canonical_edge_maps(graph)
    out = {}
    for face in graph.get("faces", []):
        support = [int(item["edge"]) for item in face_word_items(face)]
        out[int(face.get("id", len(out)))] = canonical_support_mask(support, id_map)
    return out


def expected_cross_entries(ind_cross: Mapping[str, Any], ind_masks_by_idx: Mapping[int, str], ind_graph: Mapping[str, Any]) -> Dict[Tuple[str, str], Dict[Tuple[str, str], Fraction]]:
    face_by_id = canonical_face_id_map(ind_graph)
    out: Dict[Tuple[str, str], Dict[Tuple[str, str], Fraction]] = {}
    for entry in ind_cross["entries"]:
        i, j = int(entry["row"]), int(entry["col"])
        cp = tuple(sorted((ind_masks_by_idx[i], ind_masks_by_idx[j])))
        poly = out.setdefault(cp, {})
        for term in entry["terms"]:
            f, g = (int(term["lambda_pair"][0]), int(term["lambda_pair"][1]))
            fp = tuple(sorted((face_by_id[f], face_by_id[g])))
            coeff = Fraction(str(term["coefficient"]))
            poly[fp] = poly.get(fp, Fraction(0)) + coeff
    return {k: {kk: vv for kk, vv in sorted(v.items()) if vv} for k, v in sorted(out.items())}


def clean_poly(poly: Dict[Tuple[str, str], Fraction]) -> Dict[Tuple[str, str], Fraction]:
    return {k: v for k, v in sorted(poly.items()) if v}


def transpose_failures_from_ordered(ordered: Mapping[Tuple[str, str], Mapping[Tuple[str, str], Fraction]]) -> List[Dict[str, Any]]:
    failures: List[Dict[str, Any]] = []
    for (a, b), poly in ordered.items():
        if a == b:
            continue
        rev = (b, a)
        if rev not in ordered:
            failures.append({"matrix_pair": [a, b], "reason": "missing_transpose"})
        elif dict(ordered[rev]) != dict(poly):
            failures.append({"matrix_pair": [a, b], "reason": "transpose_polynomial_mismatch"})
    return failures


def producer_cross_entry_maps(prod_cross: Mapping[str, Any], prod_masks_by_idx: Mapping[int, str], prod_graph: Mapping[str, Any]) -> Dict[str, Any]:
    face_by_id = canonical_face_id_map(prod_graph)
    rows = prod_cross.get("cross_quadratic_nonzero") or prod_cross.get("entries") or prod_cross.get("upper_triangle_entries")
    if not isinstance(rows, list):
        raise ValueError("producer cross Gram does not expose row entries")
    ordered: Dict[Tuple[str, str], Dict[Tuple[str, str], Fraction]] = {}
    upper_only_schema = False
    for row in rows:
        i = int(row.get("i", row.get("row")))
        j = int(row.get("j", row.get("col")))
        if i not in prod_masks_by_idx or j not in prod_masks_by_idx:
            raise ValueError(f"cross row references absent basis index {(i, j)}")
        cp_ordered = (prod_masks_by_idx[i], prod_masks_by_idx[j])
        if "face_f" in row:
            coeff = Fraction(str(row.get("coeff", row.get("coefficient"))))
            f, g = int(row["face_f"]), int(row["face_g"])
            fp = tuple(sorted((face_by_id[f], face_by_id[g])))
            poly = ordered.setdefault(cp_ordered, {})
            poly[fp] = poly.get(fp, Fraction(0)) + coeff
        else:
            # Backward-style upper-triangle entries used only for self-tests.
            upper_only_schema = True
            terms = row.get("terms")
            if not isinstance(terms, list):
                raise ValueError("entry row without face_f/face_g must provide terms")
            poly = ordered.setdefault(cp_ordered, {})
            for term in terms:
                f, g = int(term["lambda_pair"][0]), int(term["lambda_pair"][1])
                fp = tuple(sorted((face_by_id[f], face_by_id[g])))
                poly[fp] = poly.get(fp, Fraction(0)) + Fraction(str(term["coefficient"]))
    ordered_clean = {k: clean_poly(v) for k, v in sorted(ordered.items())}
    transpose_failures = [] if upper_only_schema else transpose_failures_from_ordered(ordered_clean)
    upper: Dict[Tuple[str, str], Dict[Tuple[str, str], Fraction]] = {}
    upper_conflicts: List[Dict[str, Any]] = []
    for key, poly in ordered_clean.items():
        upkey = tuple(sorted(key))
        if upkey in upper and upper[upkey] != poly:
            upper_conflicts.append({"matrix_pair": list(upkey), "reason": "upper_duplicate_polynomial_mismatch"})
        else:
            upper[upkey] = dict(poly)
    return {"upper": {k: v for k, v in sorted(upper.items())}, "ordered": ordered_clean, "transpose_failures": transpose_failures + upper_conflicts}


def load_output_dir(evidence: Path) -> Dict[str, Any]:
    return {
        "results": load_json(evidence / "results.json"),
        "channels": load_json(evidence / "channels.json"),
        "graph": load_json(evidence / "graph.json"),
        "cross": load_json(evidence / "cross-gram-coefficients.json") if (evidence / "cross-gram-coefficients.json").exists() else load_json(evidence / "cross-gram-status.json"),
        "controls": load_json(evidence / "controls.json"),
        "source_manifest": load_json(evidence / "source-manifest.json") if (evidence / "source-manifest.json").exists() else None,
    }


def run_independent(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-B"]
    if sys.flags.optimize:
        cmd.append("-" + "O" * sys.flags.optimize)
    cmd += [str(CHECK), "--output", str(output_dir)]
    subprocess.run(cmd, check=True)


def normalize_bundle(kind: str, data: Mapping[str, Any]) -> Dict[str, Any]:
    graph = data["graph"]
    channels = data["channels"]
    cross = data["cross"]
    cross_maps = {"ordered": {}, "transpose_failures": []}
    if kind == "producer":
        masks = producer_channel_masks(channels, graph)
        cross_maps = producer_cross_entry_maps(cross, masks, graph)
        cross_entries = cross_maps["upper"]
        scale = data["results"].get("scale_register") or data["results"].get("physical_scale") or {}
        threshold_assignment_count = channels.get("threshold_label_assignment_count")
        threshold_physical_count = channels.get("threshold_physical_channel_count_with_intertwiner_multiplicity") or channels.get("threshold_channel_count")
        threshold_dist = channels.get("threshold_intertwiner_multiplicity_distribution")
        basis_dim = channels.get("basis_dimension") or len(masks)
        source_manifest = data.get("source_manifest")
    else:
        masks = independent_channel_masks(channels, graph)
        cross_entries = expected_cross_entries(cross, masks, graph)
        scale = data["results"].get("physical_scale", {})
        audit = channels.get("threshold_label_audit", {})
        threshold_assignment_count = audit.get("assignment_count")
        threshold_physical_count = audit.get("physical_channel_count_with_intertwiners")
        threshold_dist = audit.get("multiplicity_distribution_by_assignment")
        basis_dim = channels.get("retained_dimension") or len(masks)
        source_manifest = None
    threshold_witness = channels.get("threshold_witness") or data["results"].get("channel_summary", {}).get("threshold_witness")
    return {
        "kind": kind,
        "graph_signature": canonical_graph_signature(graph),
        "masks_by_idx": masks,
        "mask_set": set(masks.values()),
        "basis_dim": int(basis_dim),
        "cross_entries": cross_entries,
        "ordered_cross_entries": cross_maps["ordered"] if kind == "producer" else {},
        "cross_transpose_failures": cross_maps["transpose_failures"] if kind == "producer" else [],
        "cross_coeff_ordered_count": cross.get("cross_quadratic_nonzero_count") or cross.get("ordered_quadratic_coefficients_in_upper_entries"),
        "cross_quartic_candidates": cross.get("quartic_upper_triangle_unordered_face_candidates"),
        "cross_branch_hist": cross.get("rank4_link_branch_histogram_upper_unordered_faces"),
        "scale": scale,
        "threshold_witness": threshold_witness,
        "threshold_assignment_count": threshold_assignment_count,
        "threshold_physical_count": threshold_physical_count,
        "threshold_dist": threshold_dist,
        "source_manifest": source_manifest,
    }


def admission_failures(prod: Mapping[str, Any], exp: Mapping[str, Any], producer_source: Path | None = None, evidence_dir: Path | None = None) -> List[str]:
    failures = []
    if prod["graph_signature"] != exp["graph_signature"]:
        failures.append("graph_signed_incidence")
    if prod["basis_dim"] != 48 or exp["basis_dim"] != 48:
        failures.append("basis_dimension")
    if prod["mask_set"] != exp["mask_set"]:
        failures.append("basis_mask_set")
    tw = prod.get("threshold_witness") or {}
    if str(tw.get("energy_over_alpha")) != "6":
        failures.append("threshold_witness")
    if prod.get("threshold_assignment_count") != 99 or prod.get("threshold_physical_count") != 107 or prod.get("threshold_dist") != {"1": 91, "2": 8}:
        failures.append("threshold_multiplicity")
    scale = prod.get("scale", {})
    if (not scale_has_positive_E_star(scale)) or str(scale.get("alpha_over_E_star")) != "2" or str(scale.get("strict_cutoff_over_E_star")) != "12":
        failures.append("physical_scale")
    transpose_failures = transpose_failures_from_ordered(prod.get("ordered_cross_entries", {})) if prod.get("ordered_cross_entries") else prod.get("cross_transpose_failures", [])
    if transpose_failures:
        failures.append("cross_gram_transpose_symmetry")
    if prod["cross_entries"] != exp["cross_entries"]:
        failures.append("cross_gram_polynomial")
    if prod.get("cross_coeff_ordered_count") != 867:
        failures.append("cross_gram_ordered_coefficient_count")
    if producer_source is not None and evidence_dir is not None:
        sm = prod.get("source_manifest")
        if not sm:
            failures.append("source_manifest_missing")
        else:
            source_files = sm.get("source_files", {})
            required_source_names = ["check.py", "report.md"]
            source_dir = producer_source if producer_source.is_dir() else producer_source.parent
            for name in required_source_names:
                source_path = source_dir / name
                if name not in source_files:
                    failures.append(f"source_manifest_missing_source_entry:{name}")
                elif not source_path.exists():
                    failures.append(f"source_manifest_missing_source_file:{name}")
                elif source_files[name] != sha256_file(source_path):
                    failures.append(f"source_manifest_source_hash:{name}")
            outputs = sm.get("outputs", {})
            required_outputs = ["basis.csv", "channels.json", "controls.json", "cross-gram-coefficients.json", "fixture-matrices.json", "graph.json", "results.json"]
            for name in required_outputs:
                p = evidence_dir / name
                if name not in outputs:
                    failures.append(f"source_manifest_missing_output_entry:{name}")
                elif not p.exists():
                    failures.append(f"source_manifest_missing_output_file:{name}")
                elif outputs[name] != sha256_file(p):
                    failures.append(f"source_manifest_output_hash:{name}")
    return failures


def mutate_and_expect_reject(prod: Dict[str, Any], exp: Dict[str, Any], producer_source: Path, evidence_dir: Path) -> List[Dict[str, Any]]:
    controls = []
    def run(name: str, mutator) -> None:
        mutated = deepcopy(prod)
        mutator(mutated)
        failures = admission_failures(mutated, exp, producer_source, evidence_dir)
        controls.append({"name": name, "passed": bool(failures), "detected_failures": failures})
    run("omit_below_cutoff_channel", lambda m: m["mask_set"].remove(next(x for x in m["mask_set"] if x != "00000")))
    run("include_threshold_in_basis", lambda m: m["mask_set"].add("0cc0f"))
    run("drop_signed_face_incidence", lambda m: m.__setitem__("graph_signature", {**m["graph_signature"], "signed_face_edge_sets": []}))
    def change_coeff(m):
        key = next(iter(m["cross_entries"]))
        poly = dict(m["cross_entries"][key])
        pk = next(iter(poly))
        poly[pk] = poly[pk] + Fraction(1, 16)
        m["cross_entries"] = dict(m["cross_entries"])
        m["cross_entries"][key] = poly
    run("alter_one_cross_gram_coefficient", change_coeff)

    def antisymmetric(m):
        ordered = {k: dict(v) for k, v in m["ordered_cross_entries"].items()}
        target = next(k for k in ordered if k[0] != k[1] and (k[1], k[0]) in ordered)
        rev = (target[1], target[0])
        face_key = next(iter(ordered[target]))
        ordered[target][face_key] = ordered[target][face_key] + Fraction(1, 16)
        ordered[rev][face_key] = ordered[rev].get(face_key, Fraction(0)) - Fraction(1, 16)
        m["ordered_cross_entries"] = ordered
    run("antisymmetric_matrix_triangle_perturbation", antisymmetric)
    def missing_sub(m):
        m["cross_entries"] = dict(m["cross_entries"])
        vac = tuple(sorted(("00000", "00000")))
        m["cross_entries"][vac] = {("00505", "00505"): Fraction(1, 4)}
    run("missing_PVP_subtraction_spurious_vacuum", missing_sub)
    run("zero_alpha_ratio", lambda m: m["scale"].__setitem__("alpha_over_E_star", "0"))
    run("zero_E_star_field_with_ratios_unchanged", lambda m: m["scale"].__setitem__("E_star", "0"))
    run("kappa_substituted_for_E_star_with_ratios_unchanged", lambda m: m["scale"].__setitem__("E_star", "kappa"))
    run("fibonacci_substituted_for_E_star_with_ratios_unchanged", lambda m: m["scale"].__setitem__("E_star", "Fibonacci index"))
    run("wrong_cutoff_scale", lambda m: m["scale"].__setitem__("strict_cutoff_over_E_star", "9"))
    def bound_as_exact(m):
        m["cross_entries"] = {tuple(sorted(("00000", "00000"))): {("bound", "bound"): Fraction(867)}}
        m["cross_coeff_ordered_count"] = 1
    run("bound_as_exact_gram", bound_as_exact)
    run("threshold_assignment_count_misreported_as_physical", lambda m: m.__setitem__("threshold_physical_count", 99))

    def remove_check_hash(m):
        m["source_manifest"] = deepcopy(m["source_manifest"])
        m["source_manifest"].setdefault("source_files", {}).pop("check.py", None)
    run("manifest_missing_check_hash", remove_check_hash)
    def remove_output_entry(m):
        m["source_manifest"] = deepcopy(m["source_manifest"])
        m["source_manifest"].setdefault("outputs", {}).pop("results.json", None)
    run("manifest_missing_required_output_entry", remove_output_entry)
    def corrupt_output_hash(m):
        m["source_manifest"] = deepcopy(m["source_manifest"])
        m["source_manifest"].setdefault("outputs", {})["results.json"] = "0" * 64
    run("manifest_wrong_required_output_hash", corrupt_output_hash)
    return controls


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--producer", required=True, help="producer source file/directory for source binding")
    ap.add_argument("--evidence", required=True, help="producer output directory")
    ap.add_argument("--output", required=True, help="comparison output directory")
    args = ap.parse_args()
    producer_source = abs_path(args.producer)
    evidence_dir = abs_path(args.evidence)
    output_dir = abs_path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    independent_dir = output_dir / "independent-reconstruction"
    run_independent(independent_dir)

    prod_data = load_output_dir(evidence_dir)
    ind_data = {
        "results": load_json(independent_dir / "results.json"),
        "channels": load_json(independent_dir / "channels.json"),
        "graph": load_json(independent_dir / "graph.json"),
        "cross": load_json(independent_dir / "cross-gram-status.json"),
        "controls": load_json(independent_dir / "controls.json"),
        "source_manifest": None,
    }
    exp = normalize_bundle("independent", ind_data)
    prod = normalize_bundle("producer", prod_data)

    checks: List[Dict[str, Any]] = []
    def add(name: str, passed: bool, **extra: Any) -> None:
        row = {"name": name, "passed": bool(passed)}
        row.update(extra)
        checks.append(row)

    add("actual signed graph incidence matches by coordinate-normalized edges/faces", prod["graph_signature"] == exp["graph_signature"])
    add("strict-cutoff basis mask set matches independent 48-channel P", prod["basis_dim"] == 48 and prod["mask_set"] == exp["mask_set"], producer_count=len(prod["mask_set"]), expected_count=len(exp["mask_set"]))
    add("threshold witness and multiplicity audit match 99 assignments / 107 physical channels", prod.get("threshold_assignment_count") == 99 and prod.get("threshold_physical_count") == 107 and prod.get("threshold_dist") == {"1": 91, "2": 8}, producer_assignment_count=prod.get("threshold_assignment_count"), producer_physical_count=prod.get("threshold_physical_count"), producer_dist=prod.get("threshold_dist"))
    add("scale checkpoint has positive E_star, alpha/E_star=2 and strict_cutoff/E_star=12", scale_has_positive_E_star(prod["scale"]) and str(prod["scale"].get("alpha_over_E_star")) == "2" and str(prod["scale"].get("strict_cutoff_over_E_star")) == "12", producer_scale=prod["scale"])
    add("full ordered matrix entries have matching transposes before upper-triangle comparison", not prod.get("cross_transpose_failures"), transpose_failures=prod.get("cross_transpose_failures"))
    add("full cross-Gram commutative polynomial matches independent exact epsilon contraction", prod["cross_entries"] == exp["cross_entries"], producer_entries=len(prod["cross_entries"]), expected_entries=len(exp["cross_entries"]))
    add("forward ordered quadratic coefficient count is 867", prod.get("cross_coeff_ordered_count") == 867, producer_value=prod.get("cross_coeff_ordered_count"))

    sm = prod.get("source_manifest")
    if sm:
        manifest_fail = [f for f in admission_failures(prod, exp, producer_source, evidence_dir) if f.startswith("source_manifest")]
        add("source manifest binds actual producer source and output bytes", not manifest_fail, failures=manifest_fail, source_manifest_sha256=sha256_file(evidence_dir / "source-manifest.json") if (evidence_dir / "source-manifest.json").exists() else None)
    else:
        add("source manifest binds actual producer source and output bytes", False, reason="source-manifest.json absent")

    mutation_controls = mutate_and_expect_reject(prod, exp, producer_source, evidence_dir)
    for c in mutation_controls:
        checks.append({"name": "mutation rejects " + c["name"], "passed": c["passed"], "detected_failures": c["detected_failures"]})

    failures = admission_failures(prod, exp, producer_source, evidence_dir)
    status = "accepted" if all(row["passed"] for row in checks) and not failures else "rejected"
    comparison = {
        "schema": "ym19-backward-b1-comparison-v2",
        "status": status,
        "producer_source": str(producer_source),
        "producer_evidence": str(evidence_dir),
        "producer_results_sha256": sha256_file(evidence_dir / "results.json"),
        "producer_cross_gram_sha256": sha256_file(evidence_dir / "cross-gram-coefficients.json"),
        "producer_source_manifest_sha256": sha256_file(evidence_dir / "source-manifest.json") if (evidence_dir / "source-manifest.json").exists() else None,
        "independent_results_sha256": sha256_file(independent_dir / "results.json"),
        "independent_cross_gram_sha256": sha256_file(independent_dir / "cross-gram-status.json"),
        "checks_count": len(checks),
        "checks": checks,
        "admission_failures": failures,
        "mutation_controls": mutation_controls,
        "normalized_counts": {
            "basis_masks": len(exp["mask_set"]),
            "cross_matrix_pairs": len(exp["cross_entries"]),
            "producer_cross_matrix_pairs": len(prod["cross_entries"]),
            "ordered_quadratic_coefficients": prod.get("cross_coeff_ordered_count"),
        },
    }
    out_path = output_dir / "comparison.json"
    out_path.write_text(json.dumps(comparison, indent=2, sort_keys=True, default=str) + "\n")
    print(json.dumps({"status": status, "checks_count": len(checks), "output": str(out_path)}, sort_keys=True))
    if status != "accepted":
        sys.exit(1)


if __name__ == "__main__":
    main()
