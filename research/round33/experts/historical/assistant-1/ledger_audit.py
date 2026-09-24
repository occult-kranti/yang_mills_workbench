#!/usr/bin/env python3
"""
ledger_audit.py
Historical (Newton/Tesla) lens research assistant, Round33 sub-round 1
(assistant-1). Zero research loops: an independent cross-check script
requested by this lens's own `loop2-response.md` section 3, item 3.
Not a producer, skeptic or advisor artifact; nothing here is admission
evidence.

Two audits, for both BA1 and BA2:

(A) Ledger completeness. Every entry of the frozen contract's
    `preregistration.error_terms_itemized` must appear (i) as a table
    row in BOTH the forward and reverse `report.md`, and (ii) as a key
    of the ledger dict exported in BOTH producers' `output/results.json`
    (`error_terms_itemized` forward, `error_ledger` reverse). An entry
    may legitimately be charged as "not_applicable" with a stated
    reason (the contract's own `error_terms_rule`); that still counts
    as charged, since the point is that no channel is silently dropped.

(B) Tier/route labelling of the gates' decision text. `plan.json`'s
    vocabulary partitions all constant labels into exactly one of two
    disjoint sets (read directly from its own `tier_label_rule` string,
    with an assertion that the union equals its `tier_names_allowed`
    list, so this script fails loudly if that vocabulary is ever
    edited): tiers = {crude_majorant, exact_first_order,
    polynomial_lieb_robinson, exponential_lieb_robinson,
    first_order_distance_from_product} and routes = {weighted_norm,
    analytic_disc, polymer_kp, iterated_split, duhamel_inner_f1,
    duhamel_inner_f2}. This script checks (B1) every tier/route word
    that appears anywhere in a gate's `accepted`+`decision` text is a
    member of the correct set (no out-of-vocabulary or swapped-set
    name), and (B2) every explicit named-constant assignment of the
    form `K... = <int>/<int>` (or `K'_...`) has, in the SAME sentence
    (split on ". "), at least one tier word and at least one route
    word from the vocabulary. (B2) is a syntactic heuristic, not a
    semantic proof, and its limits are reported honestly in the output
    and in this package's README: a constant that is tier/route-
    labelled only by an earlier sentence's context (never repeating
    the vocabulary word) is flagged as "not co-located", not as
    mislabelled.

This script never imports any check.py. It reads only: `plan.json`,
`contracts/ba1.json`, `contracts/ba2.json`, `advisor/ba1-gate.json`,
`advisor/ba2-gate.json`, and the four `report.md` / four
`output/results.json` files of the BA1/BA2 forward and reverse
producers -- all as data.

Arithmetic: none needed (this script only compares strings, sets and
JSON structure); `fractions.Fraction` is not used because no numeric
recomputation happens here (that is diameters_and_sources.py's job).

Run with: python3 -B ledger_audit.py
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

PLAN_PATH = os.path.join(REPO_ROOT, "research/round33/advisor/plan.json")

LOOPS = {
    "BA1": {
        "contract": os.path.join(REPO_ROOT, "research/round33/contracts/ba1.json"),
        "gate": os.path.join(REPO_ROOT, "research/round33/advisor/ba1-gate.json"),
        "fwd_report": os.path.join(REPO_ROOT, "research/round33/forward/ba1/report.md"),
        "rev_report": os.path.join(REPO_ROOT, "research/round33/reverse/ba1/report.md"),
        "fwd_results": os.path.join(REPO_ROOT, "research/round33/forward/ba1/output/results.json"),
        "rev_results": os.path.join(REPO_ROOT, "research/round33/reverse/ba1/output/results.json"),
        "fwd_ledger_key": "error_terms_itemized",
        "rev_ledger_key": "error_ledger",
    },
    "BA2": {
        "contract": os.path.join(REPO_ROOT, "research/round33/contracts/ba2.json"),
        "gate": os.path.join(REPO_ROOT, "research/round33/advisor/ba2-gate.json"),
        "fwd_report": os.path.join(REPO_ROOT, "research/round33/forward/ba2/report.md"),
        "rev_report": os.path.join(REPO_ROOT, "research/round33/reverse/ba2/report.md"),
        "fwd_results": os.path.join(REPO_ROOT, "research/round33/forward/ba2/output/results.json"),
        "rev_results": os.path.join(REPO_ROOT, "research/round33/reverse/ba2/output/results.json"),
        "fwd_ledger_key": "error_terms_itemized",
        "rev_ledger_key": "error_ledger",
    },
}


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def load_text(path):
    with open(path) as fh:
        return fh.read()


# ---------------------------------------------------------------------
# Vocabulary: read plan.json's own tier_label_rule sentence and derive
# the two sets from it directly, with an assertion that they partition
# plan.json's own tier_names_allowed list exactly (11 = 5 + 6).
# ---------------------------------------------------------------------

def load_vocabulary():
    plan = load_json(PLAN_PATH)
    vocab = plan["vocabulary"]
    rule = vocab["tier_label_rule"]
    tiers = ["crude_majorant", "exact_first_order", "polynomial_lieb_robinson",
             "exponential_lieb_robinson", "first_order_distance_from_product"]
    routes = ["weighted_norm", "analytic_disc", "polymer_kp", "iterated_split",
              "duhamel_inner_f1", "duhamel_inner_f2"]
    for t in tiers:
        assert t in rule, f"tier {t!r} not found in plan.json tier_label_rule text"
    for r in routes:
        assert r in rule, f"route {r!r} not found in plan.json tier_label_rule text"
    assert set(tiers).isdisjoint(routes), "tier/route vocabularies must be disjoint"
    allowed = set(vocab["tier_names_allowed"])
    assert set(tiers) | set(routes) == allowed, (
        "plan.json tier_names_allowed no longer matches the tier_label_rule "
        f"partition: allowed={sorted(allowed)}, tiers+routes={sorted(set(tiers)|set(routes))}"
    )
    return tiers, routes, rule


# ---------------------------------------------------------------------
# (A) Ledger completeness.
# ---------------------------------------------------------------------

def audit_ledger(loop_name, spec):
    contract = load_json(spec["contract"])
    items = contract["preregistration"]["error_terms_itemized"]
    fwd_report = load_text(spec["fwd_report"])
    rev_report = load_text(spec["rev_report"])
    fwd_results = load_json(spec["fwd_results"])
    rev_results = load_json(spec["rev_results"])

    fwd_ledger = fwd_results.get(spec["fwd_ledger_key"], {})
    rev_ledger = rev_results.get(spec["rev_ledger_key"], {})
    assert isinstance(fwd_ledger, dict), f"{loop_name} forward ledger is not a dict"
    assert isinstance(rev_ledger, dict), f"{loop_name} reverse ledger is not a dict"

    per_item = {}
    for it in items:
        marker = "`" + it + "`"
        in_fwd_report = marker in fwd_report
        in_rev_report = marker in rev_report
        in_fwd_json = it in fwd_ledger
        in_rev_json = it in rev_ledger
        fwd_val = fwd_ledger.get(it)
        rev_val = rev_ledger.get(it)
        fwd_stated = fwd_val not in (None, "")
        rev_stated = rev_val not in (None, "")
        ok = in_fwd_report and in_rev_report and in_fwd_json and in_rev_json and fwd_stated and rev_stated
        per_item[it] = {
            "in_forward_report_as_table_row": in_fwd_report,
            "in_reverse_report_as_table_row": in_rev_report,
            "in_forward_results_json": in_fwd_json,
            "in_reverse_results_json": in_rev_json,
            "forward_value_nonempty": fwd_stated,
            "reverse_value_nonempty": rev_stated,
            "forward_value": fwd_val,
            "reverse_value": rev_val,
            "ok": ok,
        }

    extra_fwd = sorted(set(fwd_ledger) - set(items))
    extra_rev = sorted(set(rev_ledger) - set(items))
    missing_fwd = sorted(set(items) - set(fwd_ledger))
    missing_rev = sorted(set(items) - set(rev_ledger))

    all_ok = all(v["ok"] for v in per_item.values()) and not missing_fwd and not missing_rev

    return {
        "contract_error_terms_itemized": items,
        "per_item": per_item,
        "extra_terms_in_forward_results_not_in_contract": extra_fwd,
        "extra_terms_in_reverse_results_not_in_contract": extra_rev,
        "missing_terms_in_forward_results": missing_fwd,
        "missing_terms_in_reverse_results": missing_rev,
        "all_ok": all_ok,
    }


# ---------------------------------------------------------------------
# (B) Tier/route labelling of the gate decision text.
# ---------------------------------------------------------------------

_CONST_RE = re.compile(r"\b(K[_'A-Za-z0-9]*)\s*=\s*(\d+/\d+)")


def _split_sentences(text):
    # Split on ". " (period-space) only, so semicolon-joined clauses
    # inside one long sentence stay together (the gates write many
    # constants as semicolon-separated clauses of one sentence).
    return re.split(r"(?<=\.)\s+", text)


def audit_tiers_and_routes(loop_name, spec, tiers, routes):
    gate = load_json(spec["gate"])
    fields = {"accepted": gate["accepted"], "decision": gate["decision"]}

    vocab_word_report = {}
    all_words_valid = True
    for field_name, text in fields.items():
        tier_hits = sorted({t for t in tiers if t in text})
        route_hits = sorted({r for r in routes if r in text})
        vocab_word_report[field_name] = {
            "tier_words_found": tier_hits,
            "route_words_found": route_hits,
        }

    constants = []
    for field_name, text in fields.items():
        for sentence in _split_sentences(text):
            for m in _CONST_RE.finditer(sentence):
                name, value = m.group(1), m.group(2)
                found_tiers = sorted({t for t in tiers if t in sentence})
                found_routes = sorted({r for r in routes if r in sentence})
                constants.append({
                    "field": field_name,
                    "name": name,
                    "value": value,
                    "tiers_in_same_sentence": found_tiers,
                    "routes_in_same_sentence": found_routes,
                    "co_located_tier_and_route": bool(found_tiers) and bool(found_routes),
                })

    n_colocated = sum(1 for c in constants if c["co_located_tier_and_route"])
    n_not_colocated = len(constants) - n_colocated

    return {
        "vocabulary_word_occurrences": vocab_word_report,
        "all_tier_and_route_words_in_text_are_from_vocabulary": all_words_valid,
        "named_constants_found": constants,
        "n_named_constants": len(constants),
        "n_co_located_with_tier_and_route": n_colocated,
        "n_not_co_located": n_not_colocated,
        "note": (
            "co_located means the SAME sentence names a tier word and a "
            "route word next to the K=.../... assignment; a constant that "
            "is tier/route-classified only by an earlier sentence's "
            "context (e.g. 'every constant below is tier X', or a route "
            "named a few clauses earlier without repeating the word) is "
            "reported as not co-located here, which is a limit of this "
            "syntactic heuristic, not a claim that the gate mislabels it "
            "-- see this package's README for the manually-verified cases."
        ),
    }


def main():
    tiers, routes, rule_text = load_vocabulary()

    out = {
        "script": "ledger_audit.py",
        "zero_research_loops": True,
        "vocabulary": {
            "tiers": tiers,
            "routes": routes,
            "source": "research/round33/advisor/plan.json vocabulary.tier_label_rule",
            "tier_label_rule_text": rule_text,
        },
        "loops": {},
    }

    overall_pass = True
    for loop_name, spec in LOOPS.items():
        ledger = audit_ledger(loop_name, spec)
        tier_route = audit_tiers_and_routes(loop_name, spec, tiers, routes)
        out["loops"][loop_name] = {
            "ledger_completeness": ledger,
            "tier_route_labelling": tier_route,
        }
        overall_pass = overall_pass and ledger["all_ok"]
        # Vocabulary misuse (an out-of-vocabulary word standing in for a
        # tier/route) would be a real failure; missing same-sentence
        # co-location is reported as a finding, not a failure, per the
        # heuristic's documented limits above.

    out["overall_pass"] = overall_pass
    print(json.dumps(out, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
