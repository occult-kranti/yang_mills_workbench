#!/usr/bin/env python3
"""
T5 -- ax2_budget_preview.py
Newton/Tesla historical-lens assistant script, Round32 sub-round 3.

Zero research loops: test/planning script, not a producer, skeptic or
advisor artifact. AX2 (research/round32/contracts/ax2.json) is frozen
"before production" -- it has NOT been produced, reviewed or gated yet.
Everything below is therefore explicitly labelled a PLANNING PREVIEW,
never an admitted AX2 result, and no verdict word ("accepted_within_
scope"/"limited"/"insufficient") is used for it.

Task (update-2.md section 5, test 5): with Fractions and a directed pi
enclosure, assemble

    E' = M0*(D'+D'^2) + k'*M1,  M0=2,  M1=4s/pi,  k'=51|tau|/4

(research/round32/contracts/ax2.json required.1: "E'=M_0(D'+D'^2)+k' M_1
... k'=51|tau|/4 ... D' read from the AX1 gate snapshot") with D' the
admitted forward AX1 tier-(ii) rational, at tau=10^-8, s=1 (expect
~1.9e-7 <1e-6), and the crossover s* where E'=10^-6.

Reuse: imports research/round32/experts/historical/assistant-1/
window_kernel_budget.py (an assistant script, not a producer) for its
Machin-formula directed pi enclosure (pi_bounds/arctan_bounds) -- the
exact E'=M0(D+D^2)+k*M1 template that script (S3, for AV2) already
built, since the AX2 contract states explicitly that "the AV2 window
lemma applies verbatim" with only D' and k' replaced by AX1's route-B
values. Also imports this lens's own uniform_state_tiers.py (T4, this
sub-round, same author) to recompute D' independently rather than only
trusting the contract's copy of it.

Arithmetic: fractions.Fraction with a directed (outward-rounded)
Machin-formula rational enclosure of pi for every pass/fail comparison.
No floats appear in any comparison; decimal previews are for
readability only.
Run with: python3 -B ax2_budget_preview.py
"""
import importlib.util
import json
import os
import re
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
ASSISTANT1_DIR = os.path.join(REPO_ROOT, "research/round32/experts/historical/assistant-1")
AX2_CONTRACT = os.path.join(REPO_ROOT, "research/round32/contracts/ax2.json")
AX1_GATE = os.path.join(REPO_ROOT, "research/round32/advisor/ax1-gate.json")
FWD_RESULTS = os.path.join(REPO_ROOT, "research/round32/forward/ax1/output/results.json")


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_wkb = _load_module("window_kernel_budget", os.path.join(ASSISTANT1_DIR, "window_kernel_budget.py"))
_tiers = _load_module("uniform_state_tiers", os.path.join(HERE, "uniform_state_tiers.py"))

PI_LO, PI_HI = _wkb.PI_LO, _wkb.PI_HI
assert PI_HI - PI_LO < F(1, 10 ** 30)

TAU = F(1, 10 ** 8)
S_CLOCK = F(1)
M0 = F(2)
K_SLOPE = F(51) * TAU / 4     # ax2.json parameters.k_prime = 51|tau|/4
TARGET = F(1, 10 ** 6)


def extract_leading_fraction(text):
    m = re.match(r"\s*(\d+)\s*/\s*(\d+)", text)
    assert m, "no leading fraction found in %r" % (text,)
    return F(int(m.group(1)), int(m.group(2)))


def get_admitted_D_prime():
    """D' read from THREE independent frozen sources, cross-checked to
    agree bit-for-bit, plus this session's own T4 re-derivation:
      - contracts/ax2.json parameters.D_prime (the frozen premise AX2
        production must use, per required.1 and av1_tier_bound);
      - advisor/ax1-gate.json decision text ("Bind the forward D'_ii=...");
      - forward/ax1/output/results.json tiers['+']['ii']['D'] (the
        producer's own export);
      - uniform_state_tiers.py's forward_D(1e-8) (this sub-round's
        independent from-scratch recomputation, T4)."""
    contract = load_json(AX2_CONTRACT)
    D_from_contract = extract_leading_fraction(contract["parameters"]["D_prime"])

    gate = load_json(AX1_GATE)
    decision_text = gate["decision"]
    marker = "D'_ii = "
    i = decision_text.index(marker) + len(marker)
    j = decision_text.index(" ", i)
    D_from_gate = F(decision_text[i:j].rstrip(";,"))

    fwd = load_json(FWD_RESULTS)
    D_from_forward_export = F(fwd["tiers"]["+"]["ii"]["D"])

    D_own, _ = _tiers.forward_D(TAU)

    all_agree = (D_from_contract == D_from_gate == D_from_forward_export == D_own)
    return D_from_contract, all_agree, {
        "contract": D_from_contract, "gate": D_from_gate,
        "forward_export": D_from_forward_export, "own_T4": D_own,
    }


def E_bounds(D, s=S_CLOCK, k=K_SLOPE):
    """(E_lower, E_upper): directed rational bounds on
    E'=M0*(D+D^2)+k*(4s/pi). M1=4s/pi is DECREASING in pi, so the
    smaller pi (PI_LO) gives the larger M1 and hence the larger E'."""
    state_term = M0 * (D + D ** 2)
    M1_upper = 4 * s / PI_LO
    M1_lower = 4 * s / PI_HI
    return state_term + k * M1_lower, state_term + k * M1_upper


def crossover_bounds(D, k=K_SLOPE):
    """s* solves M0*(D+D^2) + k*(4 s*/pi) = TARGET, i.e.
    s* = (TARGET - M0*(D+D^2)) * pi / (4k). pi appears un-inverted here,
    so PI_LO/PI_HI map directly to s_lower/s_upper."""
    state_term = M0 * (D + D ** 2)
    coefficient = (TARGET - state_term) / (4 * k)
    assert coefficient > 0, "tier-ii state term already exceeds target; no crossover"
    return coefficient * PI_LO, coefficient * PI_HI


def main():
    D_prime, D_sources_agree, D_sources = get_admitted_D_prime()

    E_lower, E_upper = E_bounds(D_prime)
    below_target = bool(E_upper < TARGET)
    margin_lower_bound = TARGET / E_upper  # a valid lower bound on TARGET/E' since E_upper>=E'

    s_lower, s_upper = crossover_bounds(D_prime)
    crossover_width = s_upper - s_lower
    crossover_tight = bool(crossover_width < F(1, 10 ** 20))

    # contract's own stated preview, cross-checked (not an admission):
    contract = load_json(AX2_CONTRACT)
    contract_preview_text = contract["parameters"]["preview_radius"]
    contract_target_text = contract["parameters"]["target"]
    contract_target = F(contract_target_text)
    target_matches_contract = (contract_target == TARGET)

    overall_pass = bool(
        D_sources_agree
        and below_target
        and target_matches_contract
        and crossover_tight
        and s_lower > 0
    )

    def s(x):
        return str(x) if isinstance(x, F) else x

    result = {
        "script": "ax2_budget_preview.py",
        "zero_research_loops": True,
        "labelled": "PLANNING PREVIEW ONLY -- AX2 is frozen_before_production; not yet produced or gated; no accepted/limited/insufficient verdict is asserted here",
        "arithmetic": "fractions.Fraction with a directed Machin pi enclosure (reused from assistant-1's window_kernel_budget.py) for every comparison",
        "pi_enclosure": {
            "pi_lower": s(PI_LO), "pi_upper": s(PI_HI),
            "width_decimal": float(PI_HI - PI_LO),
        },
        "D_prime": {
            "value": s(D_prime),
            "decimal_preview": float(D_prime),
            "sources_agree_bit_for_bit": D_sources_agree,
            "sources": {k: s(v) for k, v in D_sources.items()},
        },
        "inputs": {
            "tau": s(TAU), "s": s(S_CLOCK), "M0": s(M0),
            "k_prime_51_tau_over_4": s(K_SLOPE), "target": s(TARGET),
        },
        "E_prime": {
            "formula": "E'=M0*(D'+D'^2)+k'*(4s/pi), k'=51|tau|/4",
            "E_lower": s(E_lower), "E_upper": s(E_upper),
            "E_upper_decimal_preview": float(E_upper),
            "below_1e-6": below_target,
            "margin_lower_bound_target_over_E": s(margin_lower_bound),
            "margin_decimal_preview": float(margin_lower_bound),
        },
        "crossover_s_star": {
            "definition": "s* solves E'(s*)=10^-6 at tau=10^-8",
            "s_lower": s(s_lower), "s_upper": s(s_upper),
            "decimal_preview": [float(s_lower), float(s_upper)],
            "enclosure_width_below_1e-20": crossover_tight,
        },
        "contract_cross_check": {
            "target_matches_contract_1e-6": target_matches_contract,
            "contract_preview_radius_text": contract_preview_text,
            "contract_D_prime_text_prefix": contract["parameters"]["D_prime"].split(" (")[0],
        },
        "claim_flags": {
            "continuum_claim": False,
            "weak_coupling_claim": False,
            "uniform_wilson_claim": True,
            "resolved_interaction_shift": False,
            "scientific_priority_verified": False,
            "ax2_gate_status": "not_yet_produced_or_gated; this script's output is a labelled preview, not an admission",
        },
        "overall_pass": overall_pass,
    }
    print(json.dumps(result, indent=2, default=str))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
