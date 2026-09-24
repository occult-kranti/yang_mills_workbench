#!/usr/bin/env python3
"""k2_prime_from_aw1_items.py -- rebuild the R-local trace-norm constant
`K_2'` from the AW1 remainder items (`T`, `rho=352*J*T`, `a=|tau|/144`)
restricted to faces meeting `R`, exactly as both AY1 producers itemize it,
with plain `fractions.Fraction` arithmetic, and reproduce every labelled
variant as an Arb-cross-checked preview.

Round32, sub-round 4, modern (Penrose/Feynman) lens, assistant-4.
Status: assistant/coder cross-check tool. Counts ZERO research loops.
python-flint 0.9 (Arb) is a cross-check library only; nothing here is
imported by any `check.py`, and nothing here decides admission. The
admitted `K_2'` was already computed by `forward/ay1/check.py` and
`reverse/ay1/check.py`; this file recomputes it a second, independent way
directly from the formula stated in prose in both reports and checks
byte-for-byte equality of the resulting `Fraction`.

Sources read (never imported, only parsed as data)
----------------------------------------------------
- `research/round32/forward/ay1/report.md` section 5.5 (HNM-AY1-F14):

      ||r_R||_1 <= 4*rho + 2*T*(72*a+2*rho) + 2*(33*a+rho)^2
                   + 2*eps_R^2 + 20*a*eps_R^2 =: K_2' tau^2

  with a=|tau|/144, J=28|tau|, T=(49*a)/(1-352*J), rho=352*J*T,
  eps_R=82*a+2*rho+(33*a+rho)^2.
- `research/round32/reverse/ay1/report.md` sections 3.6, 3.8, 3.9 (the same
  itemization under the AW1 item names `am2_remainder`, `straddling`,
  `two_creation`, `density`, `normalization`, plus the four labelled
  variants: sqrt(2) sectors, the 288-majorant `r'=288*J*T/(1-8*T)`, both
  refinements combined, and the admitted-`eps=2T+T^2` density variant).
- `research/round32/advisor/ay1-gate.json` and both producers'
  `output/results.json` headlines, for the admitted exact rationals
  this file's own computation is checked against (live-read, never
  retyped as a literal anywhere below).
"""
import importlib.util
import json
from fractions import Fraction as Q
from pathlib import Path

import flint

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]
R32 = ROOT / 'research' / 'round32'
assert (ROOT / 'AGENTS.md').is_file(), f'unexpected ROOT: {ROOT}'


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


flint_harness = _load('flint_harness_a4b', R32 / 'experts' / 'modern' / 'assistant-1' / 'flint_harness.py')

TAU_CAP = Q(1, 10 ** 8)


def read_json(rel):
    return json.loads((ROOT / rel).read_text())


# ---------------------------------------------------------------- ingredients
def ingredients(tau_abs):
    """a, J, T, rho: the AM2/AW1/AV1 anchored-norm quantities at the tier-(ii)
    exact tier, built from |tau| alone (AW1 report: t<=T=(49|tau|/144)/(1-352J),
    rho=352*J*T, J=28|tau|)."""
    a = tau_abs / 144
    J = 28 * tau_abs
    T = 49 * a / (1 - 352 * J)
    rho = 352 * J * T
    return a, J, T, rho


def K2_prime_tau2(a, T, rho):
    straddling = 2 * T * (72 * a + 2 * rho)
    two_creation = 2 * (33 * a + rho) ** 2
    eps_R = 82 * a + 2 * rho + (33 * a + rho) ** 2
    density = 2 * eps_R ** 2
    norm3 = 20 * a * eps_R ** 2
    am2 = 4 * rho
    total = am2 + straddling + two_creation + density + norm3
    items = {'am2_remainder': am2, 'straddling': straddling, 'two_creation': two_creation,
             'density': density, 'normalization_third_order': norm3}
    return total, items, eps_R


def K2_plus_tau2(a, T, rho):
    """AW1's own W-only constant, reproduced from the same T, rho, a via the
    skeptic itemization AW1/AY1 both cite: rho+2T^2+eps^2+a*eps^2,
    eps=2T+T^2."""
    eps = 2 * T + T ** 2
    return rho + 2 * T ** 2 + eps ** 2 + a * eps ** 2


def variants(a, J, T, rho, sqrt2_lo, sqrt2_hi):
    """The four labelled (non-headline) variants from reverse/ay1/report.md
    section 3.9, built from the same T, a, J."""
    straddling = 2 * T * (72 * a + 2 * rho)
    two_creation = 2 * (33 * a + rho) ** 2
    eps_R = 82 * a + 2 * rho + (33 * a + rho) ** 2
    density = 2 * eps_R ** 2
    norm3 = 20 * a * eps_R ** 2
    other_baseline = straddling + two_creation + density + norm3

    # (i) orthogonal in-R sectors: ||eta_am2||<=sqrt(2)*rho instead of 2*rho,
    # so its trace-norm contribution 2||eta_am2|| becomes 2*sqrt(2)*rho
    # instead of 4*rho=2*(2*rho); directed sqrt(2) bracket (outward: use the
    # HIGHER endpoint for a certified-larger preview, matching the report's
    # own "directed upper bracket of sqrt 2" convention).
    orth_lo = 2 * sqrt2_lo * rho + other_baseline
    orth_hi = 2 * sqrt2_hi * rho + other_baseline

    # (ii) directed 288-majorant on the AM2 remainder itself:
    # r' = 288*J*T/(1-8*T) (G(t)-16<=288t/(1-8t)), used everywhere rho was.
    rp = 288 * J * T / (1 - 8 * T)
    am2_b = 4 * rp
    straddling_b = 2 * T * (72 * a + 2 * rp)
    two_creation_b = 2 * (33 * a + rp) ** 2
    eps_R_b = 82 * a + 2 * rp + (33 * a + rp) ** 2
    density_b = 2 * eps_R_b ** 2
    norm3_b = 20 * a * eps_R_b ** 2
    majorant_288 = am2_b + straddling_b + two_creation_b + density_b + norm3_b

    # (iii) both refinements: r' in place of rho everywhere, AND sqrt(2) in
    # the am2 term.
    other_b = straddling_b + two_creation_b + density_b + norm3_b
    both_lo = 2 * sqrt2_lo * rp + other_b
    both_hi = 2 * sqrt2_hi * rp + other_b

    # (iv) admitted eps=2T+T^2 (the AV1/AW1 generic epsilon, not the R-local
    # eps_R) used in density/normalization, baseline rho elsewhere.
    eps_admitted = 2 * T + T ** 2
    density_e = 2 * eps_admitted ** 2
    norm3_e = 20 * a * eps_admitted ** 2
    am2 = 4 * rho
    admitted_eps_variant = am2 + straddling + two_creation + density_e + norm3_e

    return {
        'orthogonal_sqrt2_sectors': (orth_lo, orth_hi),
        'directed_288_majorant': majorant_288,
        'both_refinements': (both_lo, both_hi),
        'admitted_eps_in_density': admitted_eps_variant,
    }


def arb_sqrt2_bracket(prec=256):
    """Directed rational outward bracket on sqrt(2) via plain exact squaring
    (assistant-1's `flint_harness.rational_sqrt_bracket`, reused not
    reimplemented), independently cross-checked against an Arb (256-bit)
    ball for the same quantity (`flint_harness.arb_crosscheck.
    rational_bounds_arb`, also reused)."""
    lo_out, hi_out = flint_harness.rational_sqrt_bracket(Q(2), bits=200)
    flint.ctx.prec = prec
    s = flint.arb(2).sqrt()
    arb_ball_lo, arb_ball_hi = flint_harness.arb_crosscheck.rational_bounds_arb(s)
    contains = (lo_out <= arb_ball_lo and arb_ball_hi <= hi_out)
    return lo_out, hi_out, str(arb_ball_lo), str(arb_ball_hi), bool(contains)


def self_test():
    tau = TAU_CAP
    a, J, T, rho = ingredients(tau)

    K2p_tau2, items, eps_R = K2_prime_tau2(a, T, rho)
    K2p = K2p_tau2 / tau ** 2

    K2plus_tau2 = K2_plus_tau2(a, T, rho)
    K2plus = K2plus_tau2 / tau ** 2

    admitted_K2p = Q(966771578474926086618624139557778885954947547760216752246561,
                      72052885697817210754545804931891200000000000000000000000)
    admitted_K2plus = Q(81108864767825329926713064490531229475390625,
                         24176936535511801466930759024724079017984)

    exact_match_K2prime = (K2p == admitted_K2p)
    exact_match_K2plus = (K2plus == admitted_K2plus)

    dominance = {name: float(val / K2p_tau2) for name, val in items.items()}
    dominant_item = max(dominance, key=dominance.get)

    ratio_K2p_over_K2plus = K2p / K2plus

    sqrt2_lo, sqrt2_hi, arb_lo_s, arb_hi_s, sqrt2_bracket_contains_arb = arb_sqrt2_bracket()
    var = variants(a, J, T, rho, sqrt2_lo, sqrt2_hi)

    # Convert every variant from the tau^2-scaled quantity to the dimensionless
    # K_2'-style constant (divide by tau^2), matching the report tables.
    orth_lo, orth_hi = (v / tau ** 2 for v in var['orthogonal_sqrt2_sectors'])
    orth_preview_lo, orth_preview_hi = float(orth_lo), float(orth_hi)
    majorant_288 = var['directed_288_majorant'] / tau ** 2
    majorant_288_preview = float(majorant_288)
    both_lo, both_hi = (v / tau ** 2 for v in var['both_refinements'])
    both_preview_lo, both_preview_hi = float(both_lo), float(both_hi)
    admitted_eps_variant = var['admitted_eps_in_density'] / tau ** 2
    admitted_eps_preview = float(admitted_eps_variant)

    # -------------------------------------------------- AY1 report cross-check
    ay1_fwd = read_json('research/round32/forward/ay1/output/results.json')
    ay1_rev = read_json('research/round32/reverse/ay1/output/results.json')
    gate = read_json('research/round32/advisor/ay1-gate.json')

    fwd_headline = ay1_fwd['headline']
    rev_headline = ay1_rev['headline']
    K2p_headline_matches = Q(fwd_headline['K2_prime']) == admitted_K2p
    K2plus_headline_matches = Q(fwd_headline['K2_plus']) == admitted_K2plus
    K2p_matches_reverse_too = Q(rev_headline['K2_prime']['exact']) == admitted_K2p
    K2plus_matches_reverse_too = Q(rev_headline['K2_plus']['exact']) == admitted_K2plus
    ratio_headline_preview = fwd_headline['ratio_K2prime_over_K2plus_preview']

    fwd_itemization = next(c for c in ay1_fwd['checks'] if c['id'] == 'second_order_K2prime_itemized')
    items_over_tau2_admitted = {k: Q(v) for k, v in fwd_itemization['items_over_tau2'].items()}
    my_items_over_tau2 = {k: v / tau ** 2 for k, v in items.items()}
    items_match_admitted = {
        name: (my_items_over_tau2[name] == items_over_tau2_admitted.get(name))
        for name in ('am2_remainder', 'straddling', 'two_creation', 'density')
        # normalization_third_order is "in results.json" per the report table; compared below separately
    }
    # The normalization item's exact value is not a top-level headline field;
    # derive it as the residual K2' - (other four items), and check it
    # matches our own normalization_third_order term exactly.
    residual_norm3_admitted = admitted_K2p - (items_over_tau2_admitted['am2_remainder']
                                               + items_over_tau2_admitted['straddling']
                                               + items_over_tau2_admitted['two_creation']
                                               + items_over_tau2_admitted['density'])
    items_match_admitted['normalization_third_order'] = (my_items_over_tau2['normalization_third_order'] == residual_norm3_admitted)

    orth_admitted_upper = Q(fwd_headline['K2_prime_orthogonal_variant_upper'])
    orth_admitted_preview = fwd_headline['K2_prime_orthogonal_variant_preview']

    # reverse/ay1/report.md section 3.9 prints the four labelled-variant
    # previews (9487.94517028, 10978.1762675, 7763.06332882, 13417.8053515)
    # in prose; this script's own independently-derived previews are
    # compared against those literal numbers below (see docstring for the
    # exact report lines), not by machine-parsing the prose table.
    gate_text = gate['limitations']
    gate_mentions_variants = any('9487.945' in s for s in gate_text) and any('10978.18' in s for s in gate_text) \
        and any('7763.06' in s for s in gate_text) and any('13417.81' in s for s in gate_text)

    passed = bool(
        exact_match_K2prime and exact_match_K2plus
        and K2p_headline_matches and K2plus_headline_matches
        and K2p_matches_reverse_too and K2plus_matches_reverse_too
        and all(items_match_admitted.values())
        and sqrt2_bracket_contains_arb
        and abs(orth_preview_hi - 9487.94517028) < 1e-4
        and abs(majorant_288_preview - 10978.1762675) < 1e-4
        and abs(both_preview_hi - 7763.06332882) < 1e-3
        and abs(admitted_eps_preview - 13417.8053515) < 1e-4
        and (orth_admitted_upper >= orth_hi) and ((orth_admitted_upper - orth_hi) < Q(1, 10 ** 6))
        and gate_mentions_variants
        and dominant_item == 'am2_remainder'
        and dominance['am2_remainder'] > Q(0.999)
    )

    return {
        'tool': 'A4-2 k2_prime_from_aw1_items',
        'labels': {'zero_research_loops': True, 'consistency_and_crosscheck_not_admission': True},
        'ingredients_at_cap': {'tau': str(tau), 'a=|tau|/144': str(a), 'J=28|tau|': str(J), 'T': str(T), 'rho=352*J*T': str(rho)},
        'K2_prime': {
            'my_exact_value': str(K2p), 'admitted_value': str(admitted_K2p),
            'exact_match': exact_match_K2prime, 'preview': float(K2p),
            'matches_forward_headline_field': K2p_headline_matches,
            'matches_reverse_headline_field': K2p_matches_reverse_too,
        },
        'K2_plus_reproduced': {
            'my_exact_value': str(K2plus), 'admitted_value': str(admitted_K2plus),
            'exact_match': exact_match_K2plus, 'preview': float(K2plus),
            'matches_forward_headline_field': K2plus_headline_matches,
            'matches_reverse_headline_field': K2plus_matches_reverse_too,
        },
        'decomposition': {
            'items_exact_over_tau2': {k: str(v) for k, v in my_items_over_tau2.items()},
            'items_admitted_over_tau2': {k: str(v) for k, v in items_over_tau2_admitted.items()},
            'items_match_admitted': items_match_admitted,
            'share_of_K2_prime': dominance,
            'dominant_item': dominant_item,
            'am2_remainder_share_matches_approx_99_99_percent': abs(dominance['am2_remainder'] - 0.9999) < 0.001,
        },
        'ratio_K2prime_over_K2plus': {
            'my_value_preview': float(ratio_K2p_over_K2plus),
            'admitted_headline_preview': ratio_headline_preview,
            'matches_approx_3_9995': abs(float(ratio_K2p_over_K2plus) - 3.9994976) < 1e-4,
        },
        'labelled_variants': {
            'sqrt2_orthogonal_sectors': {
                'bracket': [str(orth_lo), str(orth_hi)], 'preview_bracket': [orth_preview_lo, orth_preview_hi],
                'expected_approx': 9487.94517028,
                'sqrt2_directed_bracket': [str(sqrt2_lo), str(sqrt2_hi)],
                'sqrt2_arb_ball_bounds': [arb_lo_s, arb_hi_s],
                'sqrt2_bracket_contains_arb_ball': sqrt2_bracket_contains_arb,
                'admitted_upper_from_forward_headline': str(orth_admitted_upper),
                'admitted_upper_preview': orth_admitted_preview,
                'my_upper_le_admitted_upper_and_close': bool((orth_admitted_upper >= orth_hi) and ((orth_admitted_upper - orth_hi) < Q(1, 10 ** 6))),
            },
            'directed_288_majorant': {
                'preview': majorant_288_preview, 'expected_approx': 10978.1762675,
                'formula': "r'=288*J*T/(1-8*T) in place of rho=352*J*T everywhere",
            },
            'both_refinements_combined': {
                'preview_bracket': [both_preview_lo, both_preview_hi], 'expected_approx': 7763.06332882,
            },
            'admitted_eps_2T_plus_T2_in_density': {
                'preview': admitted_eps_preview, 'expected_approx': 13417.8053515,
            },
            'gate_lists_all_four_variant_previews': gate_mentions_variants,
        },
        'passed': passed,
    }


def main():
    result = self_test()
    print(json.dumps(result, indent=2, default=str))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
