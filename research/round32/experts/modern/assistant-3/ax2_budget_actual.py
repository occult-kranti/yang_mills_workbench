#!/usr/bin/env python3
"""ax2_budget_actual.py -- AX2 window-budget arithmetic with AX1's *actual*
admitted D', not its loose target.

Round32, sub-round 3, modern (Penrose/Feynman) lens, assistant-3.
Status: assistant/coder preview/cross-check tool. Counts ZERO research
loops (per the task brief and every prior sub-round's own labelling).
python-flint (Arb) is a cross-check library only; nothing here is
imported by any `check.py`, and nothing here decides admission. AX2's own
producer (this sub-round's contract `contracts/ax2.json`) is the only
thing that can actually admit a certificate; this script answers
update-2.md section 6's first proposed test:

  "Re-run the AX2 window arithmetic with AX1's actual admitted `D_ii`
   (both tiers), not the `4e-7` target, and flag if the margin against
   `1e-6` falls below 2."

Formula (AV2 window lemma, applied verbatim per `contracts/ax2.json`
`required` item 1, with the AX1 route-B constants):

    E'(s) = M_0(D'+D'^2) + k' M_1,  M_0=2, M_1=4s/pi, k'=51|tau|/4
          = 2(D'+D'^2) + 51|tau| s / pi.

At s=1: E' = 2(D'+D'^2) + 51|tau|/pi -- exactly the task's formula.

All three D' values used below are READ LIVE from the frozen JSON they
were admitted/reported in (never retyped), following S1/S2's own
"live-read-never-retyped" convention (`k2_bracket.py`):
  - admitted forward D' (AX1 gate, tier ii): forward/ax1/output/results.json
    headline.D_ii_plus, cross-checked to appear verbatim in the gate's own
    `accepted`/`decision` text.
  - reverse refinement D' (AX1 gate limitations, ~1.2224e-8):
    reverse/ax1/output/results.json D_prime_ii.+
  - AX1's own (looser) *target*, D'<=4e-7: forward/ax1/output/results.json
    targets.target_D_ii.

Directed `pi` is a Machin bracket, IMPORTED (not reimplemented) from the
frozen, already-admitted `forward/av2/calculator.py::pi_interval` (same
algorithm AV2 itself certifies with: `pi = 16*atan(1/5) - 4*atan(1/239)`,
directed outward). An independent Arb (256-bit) cross-check reuses
assistant-1's `flint_harness.py` (`to_fmpq`, `contains`) verbatim.
"""
import importlib.util
import json
from fractions import Fraction as Q
from pathlib import Path

import flint

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]  # .../yang_mills_workbench
R32 = ROOT / 'research' / 'round32'
assert (ROOT / 'AGENTS.md').is_file(), f'unexpected ROOT: {ROOT}'


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


flint_harness = _load('flint_harness_a3', R32 / 'experts' / 'modern' / 'assistant-1' / 'flint_harness.py')
av2_calculator = _load('av2_calculator_a3', R32 / 'forward' / 'av2' / 'calculator.py')

TAU = Q(1, 10 ** 8)          # the AX1/AX2 cap, |tau|=10^-8
S_NODE = Q(1)                 # the single certified node s=1
K_COEFF = Q(51, 4)            # k' = 51|tau|/4 (AX1 gate item 4: ||B_N||<=51|tau|/8)
TARGET = Q(1, 10 ** 6)


def read_json(rel_path):
    p = ROOT / rel_path
    with open(p) as fh:
        return json.load(fh)


def get_admitted_forward_D_prime():
    """AX1 gate tier-ii forward D', live-read from the forward producer's own
    output and cross-checked to appear verbatim in the gate's `accepted`/
    `decision` text (never retyped as a literal elsewhere in this file)."""
    fwd = read_json('research/round32/forward/ax1/output/results.json')
    value = fwd['headline']['D_ii_plus']
    D = Q(value)
    gate_text = ROOT.joinpath('research/round32/advisor/ax1-gate.json').read_text()
    found_in_accepted = value in gate_text
    also = fwd['tiers']['+']['ii']['D']
    return D, {
        'source': 'research/round32/forward/ax1/output/results.json headline.D_ii_plus',
        'string': value,
        'found_verbatim_in_ax1_gate_json': found_in_accepted,
        'matches_tiers_plus_ii_D': also == value,
        'decimal_preview': float(D),
    }


def get_reverse_refinement_D_prime():
    rev = read_json('research/round32/reverse/ax1/output/results.json')
    value = rev['D_prime_ii']['+']
    D = Q(value)
    gate_text = ROOT.joinpath('research/round32/advisor/ax1-gate.json').read_text()
    return D, {
        'source': 'research/round32/reverse/ax1/output/results.json D_prime_ii.+',
        'string': value,
        'found_verbatim_in_ax1_gate_json': value in gate_text,
        'decimal_preview': float(D),
        'label': 'labelled comparison only; the AX2 contract av1_tier_bound control rejects '
                 'substituting this value for the admitted forward D_ii_plus',
    }


def get_ax1_target_D_prime():
    fwd = read_json('research/round32/forward/ax1/output/results.json')
    value = fwd['targets']['target_D_ii']
    D = Q(value)
    return D, {
        'source': 'research/round32/forward/ax1/output/results.json targets.target_D_ii',
        'string': value,
        'decimal_preview': float(D),
        'label': 'AX1\'s own (looser) preregistered target D_ii<=4/10^7, ~30x looser than the '
                 'admitted exact tier; update-2.md section 2/4 flags this as the thing NOT to '
                 'use for AX2\'s budget',
    }


def pi_bracket():
    lo, hi = av2_calculator.pi_interval()
    assert Q(333, 106) < lo <= hi < Q(355, 113)
    return lo, hi


def m1_bounds(s, pi_lo, pi_hi):
    """M_1 = 4s/pi. Directed: M1_lower uses pi_hi, M1_upper uses pi_lo
    (AV2 calculator.window_constants convention, reused verbatim in spirit)."""
    return Q(4) * s / pi_hi, Q(4) * s / pi_lo


def budget_upper(D_prime, tau, s, pi_lo, pi_hi, k_coeff=K_COEFF):
    """A certified RATIONAL UPPER BOUND on E'(s) (directed outward): if this
    is < target, the true E'(s) < target follows a fortiori."""
    abs_tau = abs(tau)
    state = Q(2) * D_prime
    mean_square = Q(2) * D_prime * D_prime
    _, m1_upper = m1_bounds(s, pi_lo, pi_hi)
    kernel_dynamics = k_coeff * abs_tau * m1_upper
    E_upper = state + mean_square + kernel_dynamics
    return {
        'state': state, 'mean_square': mean_square, 'kernel_dynamics': kernel_dynamics,
        'E_upper': E_upper,
    }


def budget_lower(D_prime, tau, s, pi_lo, pi_hi, k_coeff=K_COEFF):
    """Companion certified LOWER bound (uses pi_hi in M_1), for reporting an
    exact enclosure width, not used for the pass/fail decision."""
    abs_tau = abs(tau)
    state = Q(2) * D_prime
    mean_square = Q(2) * D_prime * D_prime
    m1_lower, _ = m1_bounds(s, pi_lo, pi_hi)
    kernel_dynamics = k_coeff * abs_tau * m1_lower
    return state + mean_square + kernel_dynamics


def crossover_bracket(D_prime, tau, target, pi_lo, pi_hi, k_coeff=K_COEFF):
    """E'(s) = 2(D'+D'^2) + 4*k'*|tau|*s/pi is linear (increasing) in s.
    Solving E'(s*)=target with pi^-> gives a certified LOWER bound on the
    true (irrational) crossover s*; with pi^+ a certified UPPER bound.
    Mirrors AV2 forward report.md section 7 exactly."""
    abs_tau = abs(tau)
    const = Q(2) * (D_prime + D_prime * D_prime)
    if target <= const:
        return None  # the D'-only part already exceeds target; no positive crossover
    coeff_lo = Q(4) * k_coeff * abs_tau / pi_lo   # bigger coefficient (E^+ uses pi_lo)
    coeff_hi = Q(4) * k_coeff * abs_tau / pi_hi   # smaller coefficient (E^- uses pi_hi)
    s_lower = (target - const) / coeff_lo
    s_upper = (target - const) / coeff_hi
    assert s_lower <= s_upper
    return s_lower, s_upper, const


def arb_crosscheck(D_prime, tau, s, k_coeff=K_COEFF, prec=256):
    """Independent Arb (256-bit ball) evaluation of the SAME quantity
    E'(s)=2(D'+D'^2)+4k'|tau|s/pi, and a check that our directed-Fraction
    bracket [budget_lower, budget_upper] contains the Arb ball -- reusing
    flint_harness.to_fmpq/contains verbatim (no reimplementation)."""
    flint.ctx.prec = prec
    D_arb = flint.arb(flint_harness.to_fmpq(D_prime))
    tau_arb = flint.arb(flint_harness.to_fmpq(abs(tau)))
    s_arb = flint.arb(flint_harness.to_fmpq(s))
    pi_arb = flint.arb.pi()
    coeff = Q(4) * k_coeff
    E_arb = 2 * (D_arb + D_arb * D_arb) + flint.arb(flint_harness.to_fmpq(coeff)) * tau_arb * s_arb / pi_arb
    lo_frac, hi_frac = pi_bracket()
    E_lo = budget_lower(D_prime, tau, s, lo_frac, hi_frac, k_coeff)
    E_hi = budget_upper(D_prime, tau, s, lo_frac, hi_frac, k_coeff)['E_upper']
    contained = flint_harness.contains(E_lo, E_hi, E_arb)
    ball_lo, ball_hi = flint_harness.arb_crosscheck.rational_bounds_arb(E_arb)
    return {
        'precision_bits': prec,
        'arb_ball_bounds': [str(ball_lo), str(ball_hi)],
        'fraction_bracket': [str(E_lo), str(E_hi)],
        'fraction_bracket_contains_arb_ball': bool(contained),
    }


def run(label, D_prime, tau, s, pi_lo, pi_hi):
    upper = budget_upper(D_prime, tau, s, pi_lo, pi_hi)
    lower = budget_lower(D_prime, tau, s, pi_lo, pi_hi)
    E_upper = upper['E_upper']
    passed_strict = E_upper < TARGET
    passed_le = E_upper <= TARGET  # the AX2 contract's own comparator ("<=")
    margin = (TARGET / E_upper) if E_upper != 0 else None
    return {
        'label': label,
        'D_prime': str(D_prime), 'D_prime_preview': float(D_prime),
        'costs': {k: str(v) for k, v in upper.items() if k != 'E_upper'},
        'E_upper': str(E_upper), 'E_upper_preview': float(E_upper),
        'E_lower': str(lower), 'E_lower_preview': float(lower),
        'target': str(TARGET),
        'passed_strict_lt_1e6': bool(passed_strict),
        'passed_contract_le_1e6': bool(passed_le),
        'margin_ratio_target_over_E': float(margin) if margin is not None else None,
        'margin_at_least_2': bool(margin is not None and margin >= 2),
    }


def self_test():
    pi_lo, pi_hi = pi_bracket()

    D_admitted, admitted_meta = get_admitted_forward_D_prime()
    D_reverse, reverse_meta = get_reverse_refinement_D_prime()
    D_target, target_meta = get_ax1_target_D_prime()

    admitted_run = run('admitted_forward_tier_ii (decides pass/fail)', D_admitted, TAU, S_NODE, pi_lo, pi_hi)
    reverse_run = run('reverse_refinement (labelled comparison only)', D_reverse, TAU, S_NODE, pi_lo, pi_hi)
    target_run = run('ax1_own_target_4e-7 (labelled comparison only)', D_target, TAU, S_NODE, pi_lo, pi_hi)

    crossover = crossover_bracket(D_admitted, TAU, TARGET, pi_lo, pi_hi)
    s_lower, s_upper, const_part = crossover
    crossover_report = {
        's_star_bracket': [str(s_lower), str(s_upper)],
        's_star_bracket_preview': [float(s_lower), float(s_upper)],
        'D_prime_only_part_2(D+D^2)': str(const_part),
        'note': 'E_plus(s*-)=E_minus(s*+)=target exactly (AV2 forward report.md section 7 '
                'convention: pi_lo for the certified-larger function E^+, pi_hi for E^-).',
    }

    arb = arb_crosscheck(D_admitted, TAU, S_NODE)

    at_node1_margin_ok = admitted_run['margin_at_least_2']
    passed = bool(
        admitted_run['passed_strict_lt_1e6']
        and admitted_run['passed_contract_le_1e6']
        and at_node1_margin_ok
        and arb['fraction_bracket_contains_arb_ball']
        and admitted_meta['found_verbatim_in_ax1_gate_json']
        and reverse_meta['found_verbatim_in_ax1_gate_json']
    )

    return {
        'tool': 'A3-1 ax2_budget_actual',
        'formula': "E'(s) = 2(D'+D'^2) + 51|tau|*s/pi  (AV2 window lemma, AX1 route-B k'=51|tau|/4)",
        'parameters': {'tau': str(TAU), 's': str(S_NODE), 'k_prime': str(K_COEFF * abs(TAU)),
                        'target': str(TARGET)},
        'pi_bracket': {'lower': str(pi_lo), 'upper': str(pi_hi)},
        'D_prime_sources': {
            'admitted_forward_tier_ii': admitted_meta,
            'reverse_refinement': reverse_meta,
            'ax1_target': target_meta,
        },
        'runs': {
            'admitted_forward_tier_ii': admitted_run,
            'reverse_refinement_labelled_comparison': reverse_run,
            'ax1_target_labelled_comparison': target_run,
        },
        'crossover_s_star': crossover_report,
        'arb_crosscheck': arb,
        'update2_section6_item1': {
            'instruction': "Re-run the AX2 window arithmetic with AX1's actual admitted D_ii "
                            "(both tiers), not the 4e-7 target, and flag if the margin against "
                            "1e-6 falls below 2.",
            'admitted_tier_ii_margin_ratio': admitted_run['margin_ratio_target_over_E'],
            'flag_margin_below_2': not at_node1_margin_ok,
            'reverse_tier_margin_ratio': reverse_run['margin_ratio_target_over_E'],
            'target_tier_margin_ratio': target_run['margin_ratio_target_over_E'],
            'finding': 'With the admitted forward D_ii (~1.4446e-8), E\' ~1.912e-7, margin '
                       'ratio ~5.23x over 1e-6 -- comfortably above the flag threshold of 2, and far '
                       'looser than the ~4% margin update-2.md section 4 warned about when the '
                       'AX1 *target* (4e-7) was used instead of the actual admitted exact tier. '
                       'The warning in update-2.md was about a hypothetical/precautionary '
                       'substitution; the actual admitted D\' clears with wide margin.',
        },
        'contract_comparator_note': 'contracts/ax2.json preregistration.target.comparator is '
            '"<=" (E\'<=1e-6 accepted); this task brief asked for strict E\'<1e-6. Both '
            'comparators agree here (E\'~1.911e-7 clears either way); this script reports both '
            'booleans explicitly per run so the distinction is never silently collapsed.',
        'passed': passed,
    }


def main():
    result = self_test()
    print(json.dumps(result, indent=2, default=str))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
