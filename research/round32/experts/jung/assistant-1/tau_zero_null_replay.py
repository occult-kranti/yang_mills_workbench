#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 1, assistant script 1 of 3: tau=0 null replay.

Pre-registration audit / test only (loop3-signoff.md section 4, item 1). Counts zero
research loops; not a producer, contract, gate or skeptical review, and nothing here
is read back into any of those. Human project author: Hruday N M (BUNZEEY); AI-assisted.

What this does, using the AV1/AV2 producers' *exported formulas* re-implemented with
exact ``fractions.Fraction`` (no import of forward/av1/check.py, reverse/av1/check.py
or any other producer/skeptic module):

1. Evaluate the AV1 state bound D(tau) for tier (i) and tier (ii) at tau=0 (must be
   exactly Fraction(0) for both) and at tau=10^-8 (the AV1 cap; reported only).
2. Evaluate the planned AV2 window radius E(tau) = 2(D+D^2) + 49|tau|s/pi, itemized
   into state + mean_square + kernel_dynamics + arithmetic terms (contract item 4),
   at tau=0: the state, mean_square and kernel_dynamics terms must vanish exactly and
   E(0) must equal the arithmetic term alone -- taken here as the width of a Taylor
   bracket of exp(-3)/4 that this script computes -- versus tau=10^-8.
3. Report the resolving-power ratio rho = E(10^-8) / (|tau|/144) and label the
   certificate `reference_unresolved` if rho > 1 (E swallows the first-order free-
   reference distance |tau|/144, so no interaction claim follows -- AV2 required
   item 7 / claim_exclusions).

PASS iff: D_i(0)==0 and D_ii(0)==0 exactly; E(0) equals the arithmetic term alone
(state/mean_square/kernel_dynamics terms all exactly 0 at tau=0); and rho is
reported (with its reference_unresolved label set correctly).

Usage: python3 -B tau_zero_null_replay.py
"""
import sys
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as K  # noqa: E402


def run():
    C1 = K.av1_constants()
    C2 = K.av2_constants()
    tau_cap = C1['tau_cap']
    require = K.require

    # -------------------- 1. AV1 state bound at tau=0 and at the cap --------------------
    d_i_zero = K.D_tier_i(0, C1)
    d_ii_zero = K.D_tier_ii(0, C1)
    require(d_i_zero['D'] == 0, 'tier (i) D(0) is not exactly zero: ' + K.s(d_i_zero['D']))
    require(d_ii_zero['D'] == 0, 'tier (ii) D(0) is not exactly zero: ' + K.s(d_ii_zero['D']))
    require(d_i_zero['t'] == 0 and d_i_zero['eps'] == 0, 'tier (i) intermediate terms not exactly zero at tau=0')
    require(d_ii_zero['T'] == 0 and d_ii_zero['eps'] == 0, 'tier (ii) intermediate terms not exactly zero at tau=0')

    d_i_cap = K.D_tier_i(tau_cap, C1)
    d_ii_cap = K.D_tier_ii(tau_cap, C1)
    require(d_i_cap['D'] > 0 and d_ii_cap['D'] > 0, 'state bounds at the cap must be strictly positive')
    require(d_ii_cap['D'] < d_i_cap['D'], 'tier (ii) must sharpen tier (i) at the cap')

    # Cross-check against the admitted forward AV1 tier (ii) bound recorded in the gate
    # (research/round32/advisor/av1-gate.json / skeptic/av1.md), purely as a sanity
    # datum -- this script does not read that value back into any admission Boolean.
    admitted_D_ii_fwd = Q(585079838465912592144137406066050,
                          42981220507576537932303142777593983768257)
    reproduces_admitted_D_ii = (d_ii_cap['D'] == admitted_D_ii_fwd)

    # -------------------- 2. AV2 window radius at tau=0 vs the cap --------------------
    e_zero = K.av2_window_radius(0, C2['s'], d_ii_zero['D'])
    require(e_zero['state_term'] == 0, 'AV2 state term must vanish at tau=0')
    require(e_zero['mean_square_term'] == 0, 'AV2 mean-square term must vanish at tau=0')
    require(e_zero['kernel_dynamics_term'] == 0, 'AV2 kernel-dynamics term must vanish at tau=0')
    require(e_zero['arithmetic_term'] > 0, 'the exp(-3)/4 Taylor-bracket width must be a genuine positive datum')
    require(e_zero['E'] == e_zero['arithmetic_term'],
            'E(0) must equal the arithmetic term alone: E(0)=' + K.s(e_zero['E'])
            + ' arithmetic_term=' + K.s(e_zero['arithmetic_term']))

    e_cap = K.av2_window_radius(tau_cap, C2['s'], d_ii_cap['D'])
    require(e_cap['E'] > e_zero['E'], 'E must grow away from tau=0')

    # -------------------- 3. resolving-power ratio rho --------------------
    first_order_mean_reference = tau_cap / 144  # tau/144, the planned AW2 first-order coefficient
    rho = e_cap['E'] / first_order_mean_reference
    reference_unresolved = rho > 1
    require(reference_unresolved is True or reference_unresolved is False, 'rho comparison must be decidable')

    # A damaging mutation: mislabel the certificate as resolving the reference
    # (reference_unresolved=False) although rho>1. Must be rejected.
    def mutation_mislabel_resolved():
        require(not (rho > 1), 'reference_unresolved=False is inadmissible: rho=' + K.dec(rho) + ' > 1')
    mutation_rejected = K.expect_rejected(mutation_mislabel_resolved) if rho > 1 else None

    result = {
        'id': 'tau_zero_null_replay',
        'role': 'pre-registration audit / test; zero research loops',
        'formulas_source': 'research/round32/contracts/av1.json, contracts/av2.json (re-implemented; no producer modules imported)',
        'tau_cap': K.s(tau_cap),
        'av1_state_bound': {
            'tier_i': {
                'D_at_tau_0': K.s(d_i_zero['D']),
                'D_at_tau_0_is_exact_zero': d_i_zero['D'] == 0,
                'D_at_tau_cap': K.s(d_i_cap['D']),
                'D_at_tau_cap_preview': K.dec(d_i_cap['D']),
            },
            'tier_ii': {
                'D_at_tau_0': K.s(d_ii_zero['D']),
                'D_at_tau_0_is_exact_zero': d_ii_zero['D'] == 0,
                'D_at_tau_cap': K.s(d_ii_cap['D']),
                'D_at_tau_cap_preview': K.dec(d_ii_cap['D']),
                'reproduces_admitted_forward_D_ii': reproduces_admitted_D_ii,
                'admitted_forward_D_ii_source': 'research/round32/advisor/av1-gate.json (decision field) / skeptic/av1.md',
            },
        },
        'av2_window_radius': {
            'formula': 'E = 2(D+D^2) + 49|tau|s/pi, itemized state+mean_square+kernel_dynamics+arithmetic',
            'at_tau_0': {
                'state_term': K.s(e_zero['state_term']),
                'mean_square_term': K.s(e_zero['mean_square_term']),
                'kernel_dynamics_term': K.s(e_zero['kernel_dynamics_term']),
                'arithmetic_term': K.s(e_zero['arithmetic_term']),
                'arithmetic_term_preview': K.dec(e_zero['arithmetic_term']),
                'arithmetic_term_source': 'width of a Taylor bracket of exp(-3)/4 computed by this script (common.exp_minus3_over4_bracket)',
                'E': K.s(e_zero['E']),
                'E_equals_arithmetic_term_alone': e_zero['E'] == e_zero['arithmetic_term'],
            },
            'at_tau_cap': {
                'state_term': K.s(e_cap['state_term']),
                'mean_square_term': K.s(e_cap['mean_square_term']),
                'kernel_dynamics_term': K.s(e_cap['kernel_dynamics_term']),
                'arithmetic_term': K.s(e_cap['arithmetic_term']),
                'E': K.s(e_cap['E']),
                'E_preview': K.dec(e_cap['E']),
            },
        },
        'resolving_power': {
            'first_order_mean_reference_tau_over_144': K.s(first_order_mean_reference),
            'rho_formula': 'rho = E(tau_cap) / (|tau_cap|/144)',
            'rho': K.s(rho),
            'rho_preview': K.dec(rho),
            'reference_unresolved': reference_unresolved,
            'mutation_mislabel_resolved_rejected_because': mutation_rejected,
        },
        'checks': [
            {'id': 'tier_i_D_zero_at_tau_zero', 'passed': d_i_zero['D'] == 0},
            {'id': 'tier_ii_D_zero_at_tau_zero', 'passed': d_ii_zero['D'] == 0},
            {'id': 'av2_dynamics_terms_zero_at_tau_zero', 'passed': (e_zero['state_term'] == 0
                                                                      and e_zero['mean_square_term'] == 0
                                                                      and e_zero['kernel_dynamics_term'] == 0)},
            {'id': 'av2_E_equals_arithmetic_term_alone_at_tau_zero', 'passed': e_zero['E'] == e_zero['arithmetic_term']},
            {'id': 'rho_reported', 'passed': isinstance(rho, Q)},
            {'id': 'reference_unresolved_label_matches_rho', 'passed': reference_unresolved == (rho > 1)},
        ],
    }
    result['pass'] = all(c['passed'] for c in result['checks'])
    return result


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'tau_zero_null_replay', result)
    print('tau_zero_null_replay: %s' % ('PASS' if result['pass'] else 'FAIL'))
    print('  D_i(0)=%s  D_ii(0)=%s' % (result['av1_state_bound']['tier_i']['D_at_tau_0'],
                                        result['av1_state_bound']['tier_ii']['D_at_tau_0']))
    print('  E(0)=%s (arithmetic term alone)  E(tau_cap)~%s' %
          (result['av2_window_radius']['at_tau_0']['E'], result['av2_window_radius']['at_tau_cap']['E_preview']))
    print('  rho=%s (%s)  label=%s' % (result['resolving_power']['rho_preview'],
                                        'reference_unresolved' if result['resolving_power']['reference_unresolved'] else 'resolved',
                                        result['resolving_power']['reference_unresolved']))
    for c in result['checks']:
        print('   [%s] %s' % ('x' if c['passed'] else ' ', c['id']))
    if not result['pass']:
        sys.exit(1)


if __name__ == '__main__':
    main()
