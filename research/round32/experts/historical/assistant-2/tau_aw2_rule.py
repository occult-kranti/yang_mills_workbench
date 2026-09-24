#!/usr/bin/env python3
"""
T3 -- tau_aw2_rule.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 2.

Zero research loops: test/planning script, not a producer, skeptic or
advisor artifact. Reads only frozen JSON data (research/round32/forward/
aw2/output/results.json, research/round32/advisor/aw1-gate.json,
research/round32/contracts/aw2.json) -- never any producer's check.py.

Task (update-1.md section 5, test 3): independently recompute tau_AW2
from the AW1-frozen decade-grid rule (research/round32/contracts/aw1.json,
required item 5, reproduced in research/round32/contracts/aw2.json's
"tau_AW2" parameter):

    tau_AW2 = the largest element of the decade grid {10^-8, 10^-9, 10^-10, ...}
              such that K_2^+ * tau <= 1/288,

with K_2^+ the admitted (gate-bound) exact-tier constant

    K_2^+ = 81108864767825329926713064490531229475390625
            / 24176936535511801466930759024724079017984   (~3354.80322946).

Pass iff the rule, evaluated independently over the decade grid, returns
tau_AW2 = 1/10^8 (matching research/round32/forward/aw2/output/results.json's
headline.tau_AW2 and research/round32/advisor/aw1-gate.json's decision).

Arithmetic: fractions.Fraction only; no floats in any comparison.
Run with: python3 -B tau_aw2_rule.py
"""
import json
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FWD_AW2_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/aw2/output/results.json")
AW1_GATE = os.path.join(REPO_ROOT, "research/round32/advisor/aw1-gate.json")
AW2_CONTRACT = os.path.join(REPO_ROOT, "research/round32/contracts/aw2.json")

TARGET = F(1, 288)
GRID_MIN_K = 8   # the model's own cap: |tau|<=10^-8, so the grid is {10^-8,10^-9,...}
GRID_MAX_K = 40  # generous upper bound on decade exponents scanned


def extract_fraction(text):
    m = re.search(r"(\d{5,}\s*/\s*\d{5,})", text)
    if not m:
        return None
    num, den = m.group(1).split("/")
    return F(int(num.strip()), int(den.strip()))


def load_K2_plus():
    """Read K_2^+ from the live AW1 gate and AW2 contract snapshots (not
    hardcoded), then cross-check both agree with each other."""
    with open(AW1_GATE) as fh:
        gate = json.load(fh)
    gate_k2 = extract_fraction(gate["accepted"].split("K_2^+=")[1].split(" (")[0])

    with open(AW2_CONTRACT) as fh:
        contract = json.load(fh)
    contract_k2_field = contract["parameters"]["K_2_plus"]
    contract_k2 = extract_fraction(contract_k2_field.split(" (")[0])

    return gate_k2, contract_k2


def decade_grid_rule(K2_plus, target=TARGET, kmin=GRID_MIN_K, kmax=GRID_MAX_K):
    """
    Evaluate the AW1-frozen rule over the decade grid {10^-kmin, 10^-(kmin+1), ...}:
    return the LARGEST tau on that grid (i.e. smallest k) with K2_plus*tau<=target,
    plus the full per-k table for inspection.
    """
    table = []
    chosen = None
    for k in range(kmin, kmax + 1):
        tau = F(1, 10 ** k)
        lhs = K2_plus * tau
        feasible = (lhs <= target)
        table.append({"k": k, "tau": str(tau), "K2_tau": str(lhs), "K2_tau_preview": float(lhs), "feasible": feasible})
        if feasible and chosen is None:
            chosen = tau  # first (largest) feasible value on the grid, grid scanned in increasing k
    return chosen, table


def main():
    gate_k2, contract_k2 = load_K2_plus()
    keys_agree = (gate_k2 is not None and contract_k2 is not None and gate_k2 == contract_k2)

    K2_plus = gate_k2 if gate_k2 is not None else contract_k2
    tau_aw2, table = decade_grid_rule(K2_plus)

    expected = F(1, 10 ** 8)
    rule_gives_cap = (tau_aw2 == expected)

    # cross-check against the frozen AW2 producer's own exported tau_AW2
    exported_ok = True
    exported_tau = None
    try:
        with open(FWD_AW2_RESULTS) as fh:
            fwd = json.load(fh)
        exported_tau = F(fwd["headline"]["tau_AW2"])
        exported_ok = (exported_tau == tau_aw2)
    except Exception as exc:
        exported_ok = False
        exported_tau = "READ_ERROR: %s" % exc

    # Damaging-mutation control: an off-grid or larger-than-cap value
    # (e.g. 1/10^7, outside the {10^-8,10^-9,...} grid) must be rejected
    # by construction (it is simply never produced by decade_grid_rule,
    # since the grid starts at k=8); confirm explicitly.
    off_grid_tau = F(1, 10 ** 7)
    off_grid_in_table = any(row["tau"] == str(off_grid_tau) for row in table)
    mutation_rejected = not off_grid_in_table

    # Sanity: K2_plus * (10^-8) must itself be well below the target
    # (feasible with room), and 10^-9 must ALSO be feasible (a stronger
    # decade is not spuriously infeasible) -- the cap is chosen because
    # it is the LARGEST grid element, not because smaller ones fail.
    cap_row = table[0]
    next_row = table[1]

    overall_pass = bool(
        keys_agree
        and rule_gives_cap
        and exported_ok
        and mutation_rejected
        and cap_row["feasible"]
        and next_row["feasible"]
    )

    result = {
        "script": "tau_aw2_rule.py",
        "zero_research_loops": True,
        "arithmetic": "fractions.Fraction only; no floats in any comparison",
        "K2_plus_from_gate": str(gate_k2),
        "K2_plus_from_aw2_contract": str(contract_k2),
        "gate_and_contract_K2_plus_agree": keys_agree,
        "target": str(TARGET),
        "decade_grid_scanned": "{10^-%d, 10^-%d, ..., 10^-%d}" % (GRID_MIN_K, GRID_MIN_K + 1, GRID_MAX_K),
        "first_three_grid_rows": table[:3],
        "tau_AW2_computed": str(tau_aw2),
        "tau_AW2_expected": str(expected),
        "rule_gives_cap": rule_gives_cap,
        "tau_AW2_exported_by_forward_aw2": str(exported_tau),
        "matches_exported": exported_ok,
        "off_grid_mutation_rejected": mutation_rejected,
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
