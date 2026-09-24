#!/usr/bin/env python3
"""k2_bracket.py -- bracket the AW1 gate-bound K_2^+ against assistant-1's S2
preview tiers and the three admitted exact-tier values.

Round32, sub-round 2, modern (Penrose/Feynman) lens, assistant-2.
Status: assistant/coder preview tool. Counts ZERO research loops. Never
admission arithmetic; nothing here is imported by any `check.py`. All
comparisons are exact `fractions.Fraction`.

Reads (live, not retyped, to avoid transcription error):
  research/round32/advisor/aw1-gate.json                 (the admitted K_2^+, cited literally)
  research/round32/forward/aw1/output/results.json        (forward's exact-tier K2 and its
                                                             unpinned_t_bounds variant)
  research/round32/reverse/aw1/output/results.json        (reverse's exact-tier K2)
  research/round32/experts/modern/assistant-1/flip_parity_k2.py  (S2's k2_tier_check(), imported
                                                             directly, not retyped)

Background (aw1-gate.json 'accepted', item 4): the admitted
  K_2^+ = 81108864767825329926713064490531229475390625
          / 24176936535511801466930759024724079017984
        ~ 3354.80322946
is "the skeptic itemization, identical to the forward's labelled
unpinned_t_bounds variant, dominating the forward 3354.63832966 and reverse
3354.49942587 exact-tier values, all three valid". This script verifies that
sentence's arithmetic exactly, and separately brackets the admitted value
against assistant-1's three cruder S2 preview tiers (crude AM2 majorant
~1.65e7, skeptic's 84-face bound ~1.88e4, the enumerated 49-face triangle
~1.10e4), which come from a different (coarser, geometry-based) route in
loop2-response.md and are not expected to be tight to the gate value.

Pass iff: the gate-bound K_2^+ is >= each of the three exported exact-tier
values (its own value trivially, plus forward's and reverse's), AND the
gate-bound K_2^+ is strictly less than assistant-1's S2 crude tier.
"""
import importlib.util
import json
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
GATE_PATH = ROOT / 'research/round32/advisor/aw1-gate.json'
FWD_RESULTS = ROOT / 'research/round32/forward/aw1/output/results.json'
REV_RESULTS = ROOT / 'research/round32/reverse/aw1/output/results.json'
S2_PATH = ROOT / 'research/round32/experts/modern/assistant-1/flip_parity_k2.py'

# Literal transcription of aw1-gate.json's admitted K_2^+ (item 4 of 'accepted'),
# kept here as an independent second source alongside the live JSON read below.
K2_PLUS_GATE_LITERAL = Q(
    81108864767825329926713064490531229475390625,
    24176936535511801466930759024724079017984,
)


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_exported_values():
    fwd = json.loads(FWD_RESULTS.read_text())
    rev = json.loads(REV_RESULTS.read_text())
    gate_text = GATE_PATH.read_text()

    fwd_headline_exact = Q(fwd['headline']['K2_exact_plus'])
    fwd_unpinned_variant = Q(fwd['k2']['variants']['unpinned_t_bounds']['K2'])
    fwd_crude = Q(fwd['headline']['K2_crude'])
    rev_exact_tier = Q(rev['ledgers']['exact_plus']['K2_exact_rational'])
    rev_crude_tier = Q(rev['ledgers']['crude_plus']['K2_exact_rational'])

    gate_literal_str = str(K2_PLUS_GATE_LITERAL.numerator) + '/' + str(K2_PLUS_GATE_LITERAL.denominator)
    gate_value_appears_in_gate_text = gate_literal_str in gate_text.replace('\n', '')

    gate_equals_forward_unpinned_variant = (K2_PLUS_GATE_LITERAL == fwd_unpinned_variant)

    return {
        'gate_bound_K2_plus': K2_PLUS_GATE_LITERAL,
        'gate_bound_K2_plus_preview': float(K2_PLUS_GATE_LITERAL),
        'gate_literal_string_found_verbatim_in_gate_json': gate_value_appears_in_gate_text,
        'gate_equals_forward_unpinned_t_bounds_variant_exactly': gate_equals_forward_unpinned_variant,
        'forward_headline_exact_tier': fwd_headline_exact,
        'forward_headline_exact_tier_preview': float(fwd_headline_exact),
        'reverse_exact_tier': rev_exact_tier,
        'reverse_exact_tier_preview': float(rev_exact_tier),
        'forward_crude_tier': fwd_crude,
        'reverse_crude_tier': rev_crude_tier,
    }


def load_s2_preview_tiers():
    """Import assistant-1's S2 module directly (not retyped) and pull its
    k2_tier_check() report, then reconstruct the same exact Fraction values
    the module itself constructs internally (its own output only carries
    float previews), checking float(reconstructed) matches the module's own
    float preview bit-for-bit as a live consistency guard against silent
    transcription drift."""
    s2 = _load_module(S2_PATH, 'assistant1_s2_flip_parity_k2')
    report = s2.k2_tier_check()

    # Same literal construction as flip_parity_k2.k2_tier_check()'s internal
    # `tiers` dict (crude Q(165,10)*10**6, skeptic Q(188,10)*10**3, enumerated
    # Q(110,10)*10**3); reconstructed here (not imported, since the function
    # does not expose the Fraction objects) and cross-checked below.
    reconstructed = {
        'crude_AM2_majorant_only': Q(165, 10) * 10 ** 6,
        'skeptic_84_face_bound': Q(188, 10) * 10 ** 3,
        'enumerated_49_face_triangle': Q(110, 10) * 10 ** 3,
    }
    consistency = {
        name: float(val) == report[name]['K2_preview']
        for name, val in reconstructed.items()
    }
    return {
        's2_module_path': str(S2_PATH),
        's2_own_report_passed': report['passed'],
        'reconstructed_exact_tiers': {name: str(val) for name, val in reconstructed.items()},
        'reconstruction_matches_s2_float_preview': consistency,
        'reconstruction_trustworthy': all(consistency.values()),
        'tiers': reconstructed,
    }


def bracket():
    exported = load_exported_values()
    s2 = load_s2_preview_tiers()

    gate = exported['gate_bound_K2_plus']
    exported_exact_tier_values = {
        'gate_own_value(skeptic_itemization)': gate,
        'forward_headline_exact_tier': exported['forward_headline_exact_tier'],
        'reverse_exact_tier': exported['reverse_exact_tier'],
    }
    ge_each_exported = {
        name: (gate >= val) for name, val in exported_exact_tier_values.items()
    }

    crude_tier = s2['tiers']['crude_AM2_majorant_only']
    below_crude = gate < crude_tier

    skeptic_84_tier = s2['tiers']['skeptic_84_face_bound']
    enumerated_49_tier = s2['tiers']['enumerated_49_face_triangle']

    passed = bool(
        exported['gate_literal_string_found_verbatim_in_gate_json']
        and exported['gate_equals_forward_unpinned_t_bounds_variant_exactly']
        and s2['reconstruction_trustworthy']
        and all(ge_each_exported.values())
        and below_crude
    )

    return {
        'tool': 'k2_bracket',
        'gate_bound_K2_plus': str(gate),
        'gate_bound_K2_plus_preview': exported['gate_bound_K2_plus_preview'],
        'sources': {
            'gate_json': str(GATE_PATH),
            'forward_output': str(FWD_RESULTS),
            'reverse_output': str(REV_RESULTS),
        },
        'provenance_checks': {
            'gate_literal_string_found_verbatim_in_gate_json': exported['gate_literal_string_found_verbatim_in_gate_json'],
            'gate_equals_forward_unpinned_t_bounds_variant_exactly': exported['gate_equals_forward_unpinned_t_bounds_variant_exactly'],
        },
        'exported_exact_tier_values': {name: str(v) for name, v in exported_exact_tier_values.items()},
        'exported_exact_tier_previews': {
            name: float(v) for name, v in exported_exact_tier_values.items()
        },
        'gate_ge_each_exported_exact_tier_value': ge_each_exported,
        'assistant1_s2_preview_tiers': {
            'crude_AM2_majorant_only': str(crude_tier),
            'skeptic_84_face_bound': str(skeptic_84_tier),
            'enumerated_49_face_triangle': str(enumerated_49_tier),
        },
        'assistant1_s2_preview_tiers_reconstruction_check': s2['reconstruction_matches_s2_float_preview'],
        'gate_lt_crude_tier': below_crude,
        'gate_vs_skeptic_84_tier_(informational_only,_not_gated)': {
            'gate_lt_skeptic_84_tier': gate < skeptic_84_tier,
            'ratio_skeptic_84_over_gate': float(skeptic_84_tier / gate),
        },
        'gate_vs_enumerated_49_tier_(informational_only,_not_gated)': {
            'gate_lt_enumerated_49_tier': gate < enumerated_49_tier,
            'ratio_enumerated_49_over_gate': float(enumerated_49_tier / gate),
        },
        'ordering_summary_(exported_exact_tiers_tightest,_then_S2_previews_coarser)': [
            {'name': 'reverse_exact_tier', 'value_preview': exported['reverse_exact_tier_preview']},
            {'name': 'forward_headline_exact_tier', 'value_preview': exported['forward_headline_exact_tier_preview']},
            {'name': 'gate_bound_K2_plus (admitted)', 'value_preview': exported['gate_bound_K2_plus_preview']},
            {'name': 'S2_enumerated_49_face_triangle', 'value_preview': float(enumerated_49_tier)},
            {'name': 'S2_skeptic_84_face_bound', 'value_preview': float(skeptic_84_tier)},
            {'name': 'S2_crude_AM2_majorant', 'value_preview': float(crude_tier)},
        ],
        'passed': passed,
    }


def main():
    result = bracket()
    print(json.dumps(result, indent=2, default=str))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
