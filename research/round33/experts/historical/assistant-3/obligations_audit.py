#!/usr/bin/env python3
"""
obligations_audit.py
Historical (Newton/Tesla) lens research assistant, Round33 sub-round 3
(assistant-3). Zero research loops: a structural audit of the reviewed
obligations table in research/round33/skeptic/bc1.json
(`reviewed_obligations_table`), checking that:

  1. every "closed_within_scope" row names a gate that actually exists
     on disk (a `<TOKEN> gate` reference resolving to a real
     `<token>-gate.json` file somewhere under `research/round*/advisor/`)
     and that its `closing_gate_and_scope` text states a scope (the
     word "scope" appears in it);
  2. rows O1a and O1b are both present (the BC1 gate's own reviewed
     split of the AY2 row O1, replacing the forward producer's single
     O1 row -- BC1 gate `limitations` item "O1 in the narrow form
     only");
  3. every "open" row carries a non-trivial `missing_premise` and a
     non-trivial `candidate_route` (never blank, never the literal
     word "none").

This script never imports or executes any check.py (in particular not
research/round33/skeptic/bc1_check.py or bc1_postreview_check.py, which
produced this table), and never reads anything under
research/round33/forward/bd*/ or research/round33/reverse/bd1/ (in
production at the time this package was written). Only
research/round33/skeptic/bc1.json is read as data (its
`reviewed_obligations_table`, `o1_decision` and `obligations_reconciliation`
fields); gate *existence* is checked by a plain filesystem glob, never
by reading gate content beyond what the earlier assistant-3 scripts
already read for other purposes.

Arithmetic: none (this script is a structural/textual audit of JSON
records; every check is a string search, a set membership test or a
count, all exact).

Run with: python3 -B obligations_audit.py
Also checked identical under: python3 -B -O obligations_audit.py
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

BC1_SKEPTIC = os.path.join(REPO_ROOT, "research/round33/skeptic/bc1.json")

FORBIDDEN_SUBSTRINGS = ("forward/bd", "reverse/bd1")
assert not any(f in BC1_SKEPTIC for f in FORBIDDEN_SUBSTRINGS)


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


GATE_TOKEN_RE = re.compile(r"\b([A-Z]{2}\d)\s+gate\b")


def gate_exists(token):
    """A `<TOKEN> gate` reference (e.g. "BB2 gate") resolves to
    research/round*/advisor/<token-lower>-gate.json somewhere in the
    repository. Returns (exists, matched_paths)."""
    pattern = os.path.join(REPO_ROOT, "research", "round*", "advisor", "%s-gate.json" % token.lower())
    matches = sorted(glob.glob(pattern))
    return (len(matches) > 0), matches


def gate_tokens_in(text):
    return sorted(set(GATE_TOKEN_RE.findall(text)))


def audit_closed_row(row):
    """Returns (ok, detail) for one closed row: every gate token named
    in `closing_gate_and_scope` must resolve to a real gate file, at
    least one gate token must be present, and the text must state a
    scope."""
    text = row.get("closing_gate_and_scope", "")
    tokens = gate_tokens_in(text)
    resolved = {}
    for tok in tokens:
        exists, paths = gate_exists(tok)
        resolved[tok] = {"exists": exists, "paths": paths}
    has_scope = "scope" in text.lower()
    has_tokens = len(tokens) > 0
    all_resolved = all(v["exists"] for v in resolved.values())
    ok = has_tokens and all_resolved and has_scope
    return ok, {
        "id": row.get("id"),
        "status": row.get("status"),
        "gate_tokens_found": tokens,
        "gate_tokens_resolved": resolved,
        "has_scope_word": has_scope,
        "has_at_least_one_gate_token": has_tokens,
        "all_named_gates_exist": all_resolved,
    }


def is_blank_or_none(text):
    if text is None:
        return True
    stripped = text.strip().rstrip(".")
    return stripped == "" or stripped.lower() == "none"


def audit_open_row(row):
    """Returns (ok, detail) for one open row: `missing_premise` and
    `candidate_route` must both be present and non-trivial (not blank,
    not literally "none"); `closing_gate_and_scope` for an open row is
    expected to read "none (open)" (recorded, not required to differ)."""
    mp = row.get("missing_premise", "")
    cr = row.get("candidate_route", "")
    mp_ok = not is_blank_or_none(mp)
    cr_ok = not is_blank_or_none(cr)
    closing = row.get("closing_gate_and_scope", "")
    closing_is_none_open = closing.strip().lower().startswith("none")
    ok = mp_ok and cr_ok
    return ok, {
        "id": row.get("id"),
        "status": row.get("status"),
        "missing_premise_present": mp_ok,
        "candidate_route_present": cr_ok,
        "closing_gate_and_scope_is_none_open": closing_is_none_open,
        "missing_premise_len": len(mp),
        "candidate_route_len": len(cr),
    }


def main():
    data = load_json(BC1_SKEPTIC)
    table = data["reviewed_obligations_table"]

    ids = [row.get("id") for row in table]
    statuses = {row.get("id"): row.get("status") for row in table}
    closed_rows = [row for row in table if row.get("status") == "closed_within_scope"]
    open_rows = [row for row in table if row.get("status") == "open"]
    other_status_rows = [row for row in table if row.get("status") not in ("closed_within_scope", "open")]

    closed_audit = [audit_closed_row(row) for row in closed_rows]
    open_audit = [audit_open_row(row) for row in open_rows]

    all_closed_ok = all(ok for ok, _ in closed_audit)
    all_open_ok = all(ok for ok, _ in open_audit)

    o1a_present = "O1a" in ids
    o1b_present = "O1b" in ids
    o1_split_present = o1a_present and o1b_present
    o1a_status_closed = statuses.get("O1a") == "closed_within_scope"
    o1b_status_open = statuses.get("O1b") == "open"
    old_style_o1_absent = "O1" not in ids  # the un-split producer row must not reappear

    # Cross-check against the gate's own record of the split and the
    # table's own stated row count (data only; no re-derivation).
    o1_decision = data.get("o1_decision", {})
    reconciliation = data.get("obligations_reconciliation", {})
    cross_checks = {
        "table_has_21_rows": len(table) == 21,
        "reconciliation_reviewed_rows_21": reconciliation.get("reviewed_rows") == 21,
        "o1_decision_mentions_O1a": "O1a" in o1_decision.get("reviewed", "") if isinstance(o1_decision.get("reviewed"), str) else False,
        "o1_decision_mentions_O1b": "O1b" in o1_decision.get("reviewed", "") if isinstance(o1_decision.get("reviewed"), str) else False,
        "n_closed_rows_is_6": len(closed_rows) == 6,
        "n_open_rows_is_15": len(open_rows) == 15,
        "closed_row_ids": sorted(r.get("id") for r in closed_rows),
        "open_row_ids": sorted(r.get("id") for r in open_rows),
    }
    cross_checks["closed_row_ids_expected"] = cross_checks["closed_row_ids"] == sorted(
        ["O1a", "O2", "O3", "O4", "O5", "O6"]
    )
    expected_open = sorted(["O1b"] + ["N%d" % i for i in range(1, 15)])
    cross_checks["open_row_ids_expected"] = cross_checks["open_row_ids"] == expected_open

    checks = {
        "no_rows_with_unexpected_status": len(other_status_rows) == 0,
        "all_closed_rows_name_an_existing_gate_and_a_scope": all_closed_ok,
        "all_open_rows_have_missing_premise_and_candidate_route": all_open_ok,
        "o1a_present": o1a_present,
        "o1b_present": o1b_present,
        "o1_split_present": o1_split_present,
        "o1a_is_closed_within_scope": o1a_status_closed,
        "o1b_is_open": o1b_status_open,
        "unsplit_O1_row_absent": old_style_o1_absent,
    }
    checks.update({k: v for k, v in cross_checks.items() if isinstance(v, bool)})

    overall = all(checks.values())

    report = {
        "script": "obligations_audit.py",
        "task": "parse the reviewed obligations table from research/round33/skeptic/bc1.json "
                "and check that every closed row names a gate that exists and a scope, that "
                "O1a/O1b are both present, and that every open row has a missing premise and a "
                "candidate route",
        "source": "research/round33/skeptic/bc1.json reviewed_obligations_table",
        "row_count": len(table),
        "row_ids_in_order": ids,
        "closed_row_audit": [detail for _, detail in closed_audit],
        "open_row_audit": [detail for _, detail in open_audit],
        "other_status_rows": other_status_rows,
        "cross_checks": cross_checks,
        "checks": checks,
        "overall_pass": overall,
    }
    print(json.dumps(report, indent=2, sort_keys=True, default=str))
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
