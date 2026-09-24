#!/usr/bin/env python3
"""
round_consistency_sweep.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 5.

Zero research loops: cross-check/test script for the historical
(Newton/Tesla) lens's Round32 assistant package (assistant-5), not a
producer, skeptic or advisor artifact; nothing here is admission
evidence. Reads only JSON/Markdown data files -- no check.py of any
producer, skeptic replay or reverse checker is imported or executed.

Task (panel-update-4.md item 7, historical share, test 2). For all ten
Round32 loops (AV1, AV2, AW1, AW2, AX1, AX2, AY1, AY2, AZ1, AZ2) read
research/round32/advisor/<loop>-gate.json,
research/round32/contracts/<loop>.json, every producer's
research/round32/{forward,reverse}/<loop>/output/results.json and
research/round32/skeptic/<loop>.json, and check:

  (a) every gate's `verdict` and `accepted` text equal the corresponding
      research/round32/advisor/admission-spec.json and
      research/round32/advisor/findings.json entries;
  (b) every claim flag listed in the admission spec's per-direction
      `claims` dict equals the value the matching producer's
      output/results.json actually exports;
  (c) every producer results.json has continuum_claim: false,
      scientific_priority_verified: false and
      resolved_interaction_shift: false;
  (d) every contract's preregistration.controls_required.ids equals its
      top-level controls list;
  (e) every gate's `bindings` sha256 hashes match the working tree;
  (f) every sub-label used in a gate (`sub_label` and any
      `secondary_sub_labels`) is in that loop's contract
      preregistration.sub_labels_allowed;
  (g) gate sequence numbers run 1..10 in loop order and
      subround == (sequence+1)//2.

Two of these checks are known, by the round's own record, to have a
single documented, non-blocking exception each (not a defect this
script introduces or repairs -- historical rounds are immutable):

  - AW2/forward's results.json legitimately has
    resolved_interaction_shift: true (AW2 is exactly the loop that
    supplies a sign-certified enclosure of the interaction shift/Wilson
    mean; the admission spec's own AW2/forward `claims` entry says
    resolved_interaction_shift: true, so this is not a mismatch of
    check (b), only of the blanket wording of check (c) taken alone).
  - AV2's contract.controls lists 24 ids while
    preregistration.controls_required.ids lists only 23, omitting
    `c1_window_preview_only`; this is the AV2 gate's own recorded
    "non-blocking clerical defect" (both AV2 producers implemented the
    missing id anyway; the frozen contract is deliberately not amended;
    `freeze_contract.py` was updated afterwards to reject the
    mismatch). See research/round32/advisor/av2-gate.json,
    research/round32/advisor/admission-spec.json and
    research/round32/experts/jung/assistant-1/README.md.

This script's checks (c) and (d) therefore assert that any mismatch
found is *exactly* this single documented exception (the same style
research/round32/skeptic/av2_check.py itself uses:
`need(set(contract['controls']) - set(mirror) == {'c1_window_preview_only'}, ...)`)
and fail on anything beyond it -- so a genuinely new inconsistency
elsewhere in the round would still be caught.

Arithmetic/hashing: hashlib.sha256 and exact string/value equality only;
no floats anywhere in this script.

Run with: python3 -B round_consistency_sweep.py
"""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
ADVISOR = os.path.join(REPO_ROOT, "research/round32/advisor")
CONTRACTS = os.path.join(REPO_ROOT, "research/round32/contracts")
SKEPTIC = os.path.join(REPO_ROOT, "research/round32/skeptic")

LOOPS = ["av1", "av2", "aw1", "aw2", "ax1", "ax2", "ay1", "ay2", "az1", "az2"]

# The two documented, non-blocking exceptions this sweep must not flag
# as new/unexpected (see module docstring).
KNOWN_CLAIM_TRUE_EXCEPTIONS = {("aw2", "forward", "resolved_interaction_shift")}
KNOWN_CONTROLS_MISMATCH = {"av2": {"extra_in_controls": {"c1_window_preview_only"}, "missing_in_ids": set()}}


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def repo_path(*parts):
    return os.path.join(REPO_ROOT, *parts)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def main():
    admission_spec = load_json(os.path.join(ADVISOR, "admission-spec.json"))["loops"]
    findings = {l["id"]: l for l in load_json(os.path.join(ADVISOR, "findings.json"))["loops"]}

    table = []
    all_mismatches = []  # collects every unexpected mismatch found anywhere
    binding_totals = {"checked": 0, "mismatched": 0, "missing": 0}

    for i, loop in enumerate(LOOPS, start=1):
        row = {"loop": loop.upper(), "sequence_expected": i}

        gate = load_json(os.path.join(ADVISOR, f"{loop}-gate.json"))
        contract = load_json(os.path.join(CONTRACTS, f"{loop}.json"))
        skeptic = load_json(os.path.join(SKEPTIC, f"{loop}.json"))
        spec = admission_spec[loop]
        find = findings[loop]

        # ---- (g) sequence / subround ----
        seq = gate.get("sequence")
        subround = gate.get("subround")
        expected_subround = (seq + 1) // 2 if isinstance(seq, int) else None
        row["g_sequence_ok"] = (seq == i)
        row["g_subround_ok"] = (subround == expected_subround)

        # ---- (a) verdict / accepted vs admission-spec and findings ----
        row["a_verdict_ok"] = (gate.get("verdict") == spec.get("verdict"))
        row["a_accepted_vs_spec_ok"] = (gate.get("accepted") == spec.get("accepted"))
        row["a_accepted_vs_findings_ok"] = (gate.get("accepted") == find.get("accepted"))
        if not row["a_verdict_ok"]:
            all_mismatches.append({"loop": loop, "check": "a_verdict", "gate": gate.get("verdict"), "spec": spec.get("verdict")})
        if not row["a_accepted_vs_spec_ok"]:
            all_mismatches.append({"loop": loop, "check": "a_accepted_vs_spec"})
        if not row["a_accepted_vs_findings_ok"]:
            all_mismatches.append({"loop": loop, "check": "a_accepted_vs_findings"})

        # bonus, informational: skeptic verdict vs gate verdict
        row["bonus_skeptic_verdict_matches_gate"] = (skeptic.get("verdict") == gate.get("verdict"))

        # ---- producers / directions for this loop ----
        directions = spec.get("producers", [])
        row["producers"] = directions

        # ---- (b) claim flags vs producer results.json ----
        claims_ok = True
        for direction in directions:
            claims = spec.get(direction, {}).get("claims", {})
            results_path = repo_path("research", "round32", direction, loop, "output", "results.json")
            if not os.path.exists(results_path):
                claims_ok = False
                all_mismatches.append({"loop": loop, "check": "b_claims", "direction": direction, "error": "results.json missing"})
                continue
            results = load_json(results_path)
            for key, expected_val in claims.items():
                actual_val = results.get(key, "<MISSING KEY>")
                if actual_val != expected_val:
                    claims_ok = False
                    all_mismatches.append({
                        "loop": loop, "check": "b_claims", "direction": direction,
                        "key": key, "expected": expected_val, "actual": actual_val,
                    })
        row["b_claims_match_producer_results_ok"] = claims_ok

        # ---- (c) continuum_claim / scientific_priority_verified / resolved_interaction_shift all false ----
        c_flags_ok = True
        c_flag_findings = []
        for direction in directions:
            results_path = repo_path("research", "round32", direction, loop, "output", "results.json")
            results = load_json(results_path)
            for flag in ("continuum_claim", "scientific_priority_verified", "resolved_interaction_shift"):
                val = results.get(flag, "<MISSING KEY>")
                if val is not False:
                    is_known = (loop, direction, flag) in KNOWN_CLAIM_TRUE_EXCEPTIONS
                    c_flag_findings.append({
                        "loop": loop, "direction": direction, "flag": flag, "value": val,
                        "documented_exception": is_known,
                    })
                    if not is_known:
                        c_flags_ok = False
                        all_mismatches.append({
                            "loop": loop, "check": "c_claim_flags_false", "direction": direction,
                            "flag": flag, "value": val,
                        })
        row["c_continuum_priority_shift_all_false_or_documented_ok"] = c_flags_ok
        row["c_non_false_flags_found"] = c_flag_findings

        # ---- (d) contract controls == preregistration.controls_required.ids ----
        controls = set(contract.get("controls", []))
        mirror_ids = set(contract.get("preregistration", {}).get("controls_required", {}).get("ids", []))
        extra_in_controls = controls - mirror_ids
        missing_in_ids = mirror_ids - controls
        exact_match = (not extra_in_controls) and (not missing_in_ids)
        if exact_match:
            d_ok = True
        else:
            known = KNOWN_CONTROLS_MISMATCH.get(loop)
            d_ok = bool(known) and extra_in_controls == known["extra_in_controls"] and missing_in_ids == known["missing_in_ids"]
            if not d_ok:
                all_mismatches.append({
                    "loop": loop, "check": "d_controls_mirror", "extra_in_controls": sorted(extra_in_controls),
                    "missing_in_ids": sorted(missing_in_ids),
                })
        row["d_controls_equals_prereg_ids_ok"] = d_ok
        row["d_controls_exact_match"] = exact_match
        row["d_extra_in_controls"] = sorted(extra_in_controls)
        row["d_missing_in_prereg_ids"] = sorted(missing_in_ids)

        # ---- (e) gate bindings hashes match the working tree ----
        bindings = gate.get("bindings", {})
        e_ok = True
        e_checked = 0
        e_mismatched = []
        e_missing = []
        for path, expected_hash in bindings.items():
            full_path = repo_path(path)
            e_checked += 1
            binding_totals["checked"] += 1
            if not os.path.exists(full_path):
                e_ok = False
                e_missing.append(path)
                binding_totals["missing"] += 1
                all_mismatches.append({"loop": loop, "check": "e_bindings", "path": path, "error": "file missing"})
                continue
            actual_hash = sha256_of(full_path)
            if actual_hash != expected_hash:
                e_ok = False
                e_mismatched.append(path)
                binding_totals["mismatched"] += 1
                all_mismatches.append({"loop": loop, "check": "e_bindings", "path": path, "error": "hash mismatch"})
        row["e_bindings_ok"] = e_ok
        row["e_bindings_checked"] = e_checked
        row["e_bindings_mismatched"] = e_mismatched
        row["e_bindings_missing"] = e_missing

        # ---- (f) sub-labels used in gates are in contract's sub_labels_allowed ----
        allowed = set(contract.get("preregistration", {}).get("sub_labels_allowed", []))
        top_level_allowed = contract.get("sub_labels_allowed")
        sub_label = gate.get("sub_label")
        secondary = gate.get("secondary_sub_labels", []) or []
        sub_ok = (sub_label is None) or (sub_label in allowed)
        secondary_ok = all(s in allowed for s in secondary)
        f_ok = sub_ok and secondary_ok
        if not f_ok:
            all_mismatches.append({
                "loop": loop, "check": "f_sub_labels", "sub_label": sub_label,
                "secondary": secondary, "allowed": sorted(allowed),
            })
        row["f_sub_label"] = sub_label
        row["f_secondary_sub_labels"] = secondary
        row["f_sub_labels_allowed_in_contract_ok"] = f_ok
        row["f_contract_top_level_sub_labels_allowed_is_null"] = (top_level_allowed is None)

        row_ok = all([
            row["g_sequence_ok"], row["g_subround_ok"],
            row["a_verdict_ok"], row["a_accepted_vs_spec_ok"], row["a_accepted_vs_findings_ok"],
            row["b_claims_match_producer_results_ok"],
            row["c_continuum_priority_shift_all_false_or_documented_ok"],
            row["d_controls_equals_prereg_ids_ok"],
            row["e_bindings_ok"],
            row["f_sub_labels_allowed_in_contract_ok"],
        ])
        row["row_pass"] = row_ok
        table.append(row)

    overall_pass = all(r["row_pass"] for r in table) and len(all_mismatches) == 0

    # A short, human-readable table for the README / stdout.
    header = f"{'loop':6}{'seq':5}{'subrnd':7}{'a':4}{'b':4}{'c':4}{'d':4}{'e':4}{'f':4}{'row':5}"
    lines = [header, "-" * len(header)]
    for r in table:
        lines.append(
            f"{r['loop']:6}{r['sequence_expected']:<5}"
            f"{'ok' if r['g_subround_ok'] else 'X':7}"
            f"{'ok' if (r['a_verdict_ok'] and r['a_accepted_vs_spec_ok'] and r['a_accepted_vs_findings_ok']) else 'X':4}"
            f"{'ok' if r['b_claims_match_producer_results_ok'] else 'X':4}"
            f"{'ok' if r['c_continuum_priority_shift_all_false_or_documented_ok'] else 'X':4}"
            f"{'ok' if r['d_controls_equals_prereg_ids_ok'] else 'X':4}"
            f"{'ok' if r['e_bindings_ok'] else 'X':4}"
            f"{'ok' if r['f_sub_labels_allowed_in_contract_ok'] else 'X':4}"
            f"{'ok' if r['row_pass'] else 'X':5}"
        )
    text_table = "\n".join(lines)

    result = {
        "script": "round_consistency_sweep.py",
        "zero_research_loops": True,
        "role": "cross-check only; not a producer, skeptic or advisor artifact; never admission evidence",
        "loops_checked": [l.upper() for l in LOOPS],
        "known_documented_exceptions": {
            "c_claim_flags": sorted(f"{l}/{d}/{f}" for (l, d, f) in KNOWN_CLAIM_TRUE_EXCEPTIONS),
            "d_controls_mirror": {k: {kk: sorted(vv) for kk, vv in v.items()} for k, v in KNOWN_CONTROLS_MISMATCH.items()},
        },
        "binding_totals": binding_totals,
        "table": table,
        "text_table": text_table,
        "unexpected_mismatches": all_mismatches,
        "n_unexpected_mismatches": len(all_mismatches),
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2, default=str))
    print("\n" + text_table, file=sys.stderr)
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
