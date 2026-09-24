#!/usr/bin/env python3
"""Round33 BA1 skeptic post-comparison checker (zero-selected patterned family).

Written after both BA1 producers froze and were committed (forward 721ffe5, reverse e87511b),
following the skeptic's pre-comparison package (09ae71e, committed first). Standard library only;
exact Fractions decide every admission Boolean; floats appear only in labelled previews. Every
check raises an explicit exception, so python -O cannot disable it. Model-agent skeptic with
correlated ancestry; not human peer review.

What it does:
  * pins both producer freeze records and the skeptic pre-comparison freeze record, re-hashes
    every closure file, checks both 27-file input inventories against the contract (reverse
    premise isolation) and every snapshot against its repository source;
  * replays both producers (normal and -O, fresh temporary directories outside the checkout)
    and the skeptic pre-comparison program, byte-comparing with the frozen outputs;
  * re-derives every producer headline, floor, crude-tier, per-comparison and refinement
    constant and every tau -> tau/100 ratio exactly, compares them with the pre-comparison
    predictions, and decides which constants the gate binds (the larger valid K per frozen pair);
  * runs source edits on temporary copies: an unmutated copy of each producer (must reproduce
    its frozen output), one validator weakening per contract control per producer (37 x 2; each
    must abort with 'damaging mutation accepted: <label of that control>'), and input edits;
  * rejects damaged producer packets with its own value validator;
  * scans both reports (negation-aware, template removed as one literal), counts the template
    span, and builds and scans the supported statement and limitations of the review.

Usage: python3 -B research/round33/skeptic/ba1_postreview_check.py --output /absolute/fresh/dir
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[3]
CONTRACT_REL = 'research/round33/contracts/ba1.json'
CONTRACT_SHA256 = '2c761366d2d81ee21fa631497f8df9b80dc760bec160c985023152cd768532b9'
PROD = {'forward': 'research/round33/forward/ba1', 'reverse': 'research/round33/reverse/ba1'}
FREEZE_SHA = {'forward': 'cffc6fdf4246fb6e98e5dcfc9bfab44d2e0f520164e801f643a52fa9460582d0',
              'reverse': '7749f2f932499b02a5674f25d939bfbb4aca011c34cf233b910e75b9cd99e7c4'}
PRE_FREEZE_REL = 'research/round33/skeptic/ba1-independent-freeze.json'
PRE_FREEZE_SHA = 'cb1e1f9b546da81f45c1a798e346ce25bb0b6a3792817b4cb23f280ab9621f21'
PRE_RESULTS_REL = 'research/round33/skeptic/ba1-independent/results.json'
PRE_CHECK_REL = 'research/round33/skeptic/ba1_check.py'
FORBIDDEN_IN_REVERSE = ('research/round33/skeptic/', 'research/round33/experts/', 'research/round33/forward/',
                        'research/round33/advisor/deliberation', 'research/round33/advisor/plan', 'research/round33/advisor/brief',
                        'research/round33/advisor/panel')
ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state',
]
NEGATION = re.compile(r"\b(not|never|no|nor|neither|without|excludes?|excluded|exclusion|forbidden|"
                      r"cannot|does not|is not|are not|nothing|none)\b", re.I)
R = F(1, 64)
G_R, GP_R = F(148, 7), F(352)


class ReviewFailure(RuntimeError):
    """A review check failed; the run aborts without output."""


class Rejected(Exception):
    """The review's value validator refused a packet."""


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise ReviewFailure(cid)
    if any(row['id'] == cid for row in CHECKS):
        raise ReviewFailure('duplicate check id ' + cid)
    row = {'id': cid, 'passed': True}
    row.update(detail)
    CHECKS.append(row)


def reject(ok, reason):
    if ok is not True:
        raise Rejected(reason)


def rejects(fn, reason):
    try:
        fn()
    except Rejected as exc:
        if reason not in str(exc):
            raise ReviewFailure('rejected for the wrong reason: %s (expected %s)' % (exc, reason))
        return True
    return False


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha(path):
    return sha_bytes(Path(path).read_bytes())


def q(x):
    return str(F(x))


def fq(s):
    return F(s)


def preview(x):
    return format(float(x), '.12e')


def fact(n):
    out = 1
    for i in range(2, n + 1):
        out *= i
    return out


def exp_up(x, n=12):
    x = F(x)
    if x < 0 or x >= n + 2:
        raise ReviewFailure('exp_up domain')
    return sum((x ** k / fact(k) for k in range(n + 1)), F(0)) + x ** (n + 1) / fact(n + 1) / (1 - x / (n + 2))


def g_up(t):
    return 16 * exp_up(8 * t, 12 if 8 * t >= F(1, 100) else 4) * (1 + 10 * t)


def gp_up(t):
    return 16 * exp_up(8 * t, 12 if 8 * t >= F(1, 100) else 4) * (18 + 80 * t)


# ------------------------------------------------------------------ independent formulas
def fwd_formula(tau, w, tier):
    """The forward producer's declared constants, re-derived independently from its report section 6:
    Gamma = J w G'(R) with G'(R) at most 352, T_w = w t_1/(1-Gamma), S = w t_1 + Gamma T_w (exact tier) or
    w J G(R) (crude), K_own = S/(1-Gamma); nested K_own/w; general by telescoping K_own + K_nest/(1-q)."""
    tau = abs(F(tau))
    j, t1, w = 28 * tau, F(49, 144) * tau, F(w)
    gam = j * w * GP_R
    selfmap = j * w * G_R
    if not (selfmap <= R and gam < 1):
        raise ReviewFailure('forward formula outside the weighted ball')
    if tier == 'exact_first_order':
        t = w * t1 / (1 - gam)
        s = w * t1 + gam * t
    else:
        t = selfmap
        s = w * j * G_R
    own = s / (1 - gam)
    qq = 1 / w
    nest = qq * own
    return {'Gamma': gam, 'selfmap': selfmap, 'T_w': t, 'source': s, 'K_own': own, 'K_F1_vs_F2': own,
            'K_nested': nest, 'K_general_telescoping': own + nest / (1 - qq), 'K_general_direct': own + nest,
            'K_union': 2 * nest, 'q': qq}


def fwd_pair(d):
    return max(d['K_F1_vs_F2'], d['K_nested'], d['K_general_telescoping'])


def skeptic_sharp_forward(tau, w):
    """The skeptic pre-comparison contract-form constant (G'(T_w) in the Lipschitz factor, G(T_w)-16 in the source)."""
    tau = abs(F(tau))
    j, t1, w = 28 * tau, F(49, 144) * tau, F(w)
    t = w * t1 / (1 - j * w * GP_R)
    return w * (t1 + j * (g_up(t) - 16)) / (1 - j * w * gp_up(t))


def rev_formula(tau, rho, tier='exact_first_order', count='contract', cauchy='schwarz', sup=None):
    tau, rho = abs(F(tau)), F(rho)
    tau_star = R / (28 * G_R)
    if not (0 < rho <= tau_star and 28 * rho * G_R <= R):
        raise ReviewFailure('disc outside the contraction domain')
    lip = 28 * rho * GP_R
    t = F(49, 144) * rho / (1 - lip)
    if tier == 'exact_first_order':
        m = 2 * t if sup is None else (2 * lip * t if sup == 'first_order_cancellation' else None)
    else:
        m = 2 * 28 * rho * G_R
    if m is None:
        raise ReviewFailure('sup rule')
    qq = tau / rho
    k = m / (1 - qq) if cauchy == 'coefficientwise' else m
    return k * qq if count == 'sharp' else k


# ------------------------------------------------------------------ validator weakenings (one per control per producer)
# (control id, [(unique anchor in the producer check.py, replacement)], label of the damaging mutation that must then be accepted)
FWD = [
 ('coarse_metric_named', [("lambda: require(all(dist_set([p], [(1, 0, 0)], d_one) <= 0 + diam(S_STAR, d_inf) for p in S_STAR),",
                           "lambda: require(True or all(dist_set([p], [(1, 0, 0)], d_one) <= 0 + diam(S_STAR, d_inf) for p in S_STAR),")],
  'l1_distance_with_l_inf_diameter'),
 ('parameters_declare_metric_weights_window', [("            require(k in keys, 'parameters lack ' + k)", "            require(True, 'parameters lack ' + k)")],
  'weights_removed_from_parameters'),
 ('weighted_norm_contraction_rechecked', [("        require(value == P['J0'] * w * P['GR_up'], 'weighted self-map value must carry the weight w')",
                                           "        require(True, 'weighted self-map value must carry the weight w')")],
  'unweighted_am2_selfmap_cited_for_weighted_ball'),
 ('q_min_not_crossed', [("rejected(lambda: require(P['J0'] * (2 * w_max) * GR_true_lo <= R,", "rejected(lambda: require(True or P['J0'] * (2 * w_max) * GR_true_lo <= R,")],
  'rate_below_q_min_with_true_G_lower_bound'),
 ('ball_radius_not_used_as_tree_decay_ratio', [("        require(basis == 'chosen weight w with its own weighted contraction check',",
                                                "        require(True or basis == 'chosen weight w with its own weighted contraction check',")],
  'ball_radius_as_tree_ratio'),
 ('rate_constant_pair_prefrozen', [("        require(q == V['q_head'] and K_target == V['K_head_target'] and w == V['w_head'],",
                                    "        require(True or q == V['q_head'] and K_target == V['K_head_target'] and w == V['w_head'],")],
  'q_optimized_after_constants_reported_as_headline'),
 ('tier_mixing_rejected', [("    require(derived == tier, 'tier mixing rejected:", "    require(True or derived == tier, 'tier mixing rejected:")],
  'exact_source_with_crude_t_labelled_exact'),
 ('tau_scaling_exponent', [("        require(bracket[0] <= ratio <= bracket[1], 'ratio outside its preregistered bracket')",
                            "        require(True, 'ratio outside its preregistered bracket')")],
  'square_root_bound_labelled_linear'),
 ('global_lipschitz_not_decay', [("        require(chain[n] <= L ** n / (1 - L), 'global Lipschitz constant used as a per-step decay factor is false')",
                                  "        require(True, 'global Lipschitz constant used as a per-step decay factor is false')")],
  'lipschitz_as_decay_nonlocal_chain_n3'),
 ('weight_direction_toward_source', [("            require(chain_bounds(n, direction)[1] <= K1 * Q(1, 2) ** n, 'no decay certified by the ' + direction + ' weight')",
                                      "            require(True, 'no decay certified by the ' + direction + ' weight')")],
  'weight_growing_with_distance_from_R'),
 ('loss_per_interaction_not_per_creation', [("        require(actual_w <= bound, 'weighted estimate violated with the ' + charge + ' charge')",
                                             "        require(True, 'weighted estimate violated with the ' + charge + ' charge')")],
  'loss_charged_only_per_creation_k0'),
 ('diameter_subadditivity_through_interaction', [("            require(dM <= dX + max(diam(I1, d_inf), diam(I2, d_inf)), 'max-instead-of-sum shortcut')",
                                                  "            require(True, 'max-instead-of-sum shortcut')")],
  'max_instead_of_sum_disconnected_output'),
 ('missing_incoming_stars', [("        require(J == P['J_per_tau'], 'per-site sum must include incoming anchors (28|tau|)')",
                              "        require(True, 'per-site sum must include incoming anchors (28|tau|)')")],
  'outgoing_star_only_7tau'),
 ('boundary_source_new_terms_only', [("        require(all(X & B for X in new_terms), 'a source term does not meet the source set')",
                                      "        require(True, 'a source term does not meet the source set')")],
  'old_terms_charged_in_source'),
 ('f2_regrouping_charged_once', [("        require(len(pool) == len(set(pool)) and set(pool) == set(big_faces), 'a face charged twice or missing')",
                                  "        require(True, 'a face charged twice or missing')")],
  'regrouped_groups_charged_whole'),
 ('boundary_distance_exact', [("        require(exponent == want, 'off-by-one exponent for ' + comparison)", "        require(True, 'off-by-one exponent for ' + comparison)")],
  'F1_vs_F2_exponent_N_instead_of_N_minus_1'),
 ('face_count_all_sites', [("        require(pp == V['pins'], 'face pins differ')", "        require(True, 'face pins differ')")], 'site_0_only_counts'),
 ('full_original_wilson_cover', [("        require(len(set(links)) == 48 and len(endpoints) == 36, 'complete cover has 48 links and 36 endpoints')",
                                  "        require(True, 'complete cover has 48 links and 36 endpoints')")],
  'four_drawn_links_as_cover'),
 ('coefficient_decay_not_marginal_decay', [("        require(ra == rb, 'equal coefficients meeting R do not give equal marginals')",
                                            "        require(True, 'equal coefficients meeting R do not give equal marginals')")],
  'state_decay_inferred_from_coefficient_decay'),
 ('wrong_delta_alpha_hbar_clock', [("        require(val == Q(-1, 72), 'first-order face amplitude must be -tau/72 per unit tau')",
                                    "        require(True, 'first-order face amplitude must be -tau/72 per unit tau')")],
  'tau_over_576_mixed_units'),
 ('root_n_misuse', [("        require(total >= sum(parts), 'deterministic bounds add linearly')", "        require(True, 'deterministic bounds add linearly')")],
  'root_sum_of_squares_over_49_aligned_faces'),
 ('exact_arithmetic_admission', [("    if isinstance(value, bool) or isinstance(value, float):\n        raise AdmissionError('non-exact input rejected: ' + repr(value))\n",
                                  "    if isinstance(value, float):\n        return Q(value)\n    if isinstance(value, bool):\n        raise AdmissionError('non-exact input rejected: ' + repr(value))\n")],
  'float_input'),
 ('changed_model_relabelled', [("        require(m == MODEL, 'packet model differs from the contract')", "        require(True, 'packet model differs from the contract')")],
  'other_group'),
 ('insufficient_verdict_retained', [("        require(verdict_for(tier_value, Kf) == claimed, 'verdict does not follow from the constants')",
                                     "        require(True, 'verdict does not follow from the constants')")],
  'crude_tier_relabelled_accepted'),
 ('no_priority_or_continuum_claim', [("            require(cl.get(k) is val, 'claim flag ' + k + ' must be ' + str(val))",
                                      "            require(True, 'claim flag ' + k + ' must be ' + str(val))"),
                                     ("                require(cl.get(k, val) is val, 'claim flag disagrees with gate field ' + k)",
                                      "                require(True, 'claim flag disagrees with gate field ' + k)")],
  'continuum_claim_true'),
 ('gate_fields_topic_specific', [("        require(gf == V['gate_fields'], 'gate fields differ from the contract gate_fields_required')",
                                  "        require(True, 'gate fields differ from the contract gate_fields_required')")],
  'rate_in_N_field_dropped'),
 ('untruncated_coefficients_not_asserted', [("        require(scope.startswith('each on-site cutoff space Q_L'), 'coefficient statement must be made in each Q_L')",
                                             "        require(True, 'coefficient statement must be made in each Q_L')")],
  'cutoff_removed_for_coefficients'),
 ('decay_rate_in_N_not_a', [("        require(label == 'per coarse step in N at fixed spacing', 'rate must be per coarse step in N at fixed spacing')",
                             "        require(True, 'rate must be per coarse step in N at fixed spacing')")],
  'rate_converted_to_fm'),
 ('two_families_named', [("        require(sorted(fam) == ['F1', 'F2'] and fam == FAMILIES, 'exactly the two named families')",
                          "        require(True, 'exactly the two named families')")],
  'one_family_only'),
 ('subsequence_versus_whole_sequence', [("                require(abs(seq[i] - seq[j]) <= K * q ** i, 'whole-sequence claim needs a Cauchy bound')",
                                         "                require(True, 'whole-sequence claim needs a Cauchy bound')")],
  'alternating_sequence_with_convergent_subsequences'),
 ('uniform_in_N_not_in_a', [("            require(ok, 'unqualified uniformity statement in ' + label + ': ' + sentence[:160])",
                             "            require(True, 'unqualified uniformity statement in ' + label + ': ' + sentence[:160])")],
  'unqualified_uniformity_next_to_rate'),
 ('cardinality_weight_rate_labelled', [("            require(q_value ** 4 >= V['q_floor'], 'cardinality rate below (q_min)^(1/4)')",
                                        "            require(True, 'cardinality rate below (q_min)^(1/4)')")],
  'diameter_rate_relabelled_as_cardinality_rate'),
 ('analytic_route_disc_radius', [("        require(28 * rho * P['GR_up'] <= R, 'disc self-map 28 rho G(R) at most R fails')",
                                  "        require(True, 'disc self-map 28 rho G(R) at most R fails')")],
  'disc_radius_beyond_tau_star'),
 ('reverse_premise_isolation', [("        require(not [x for x in lst if banned.search(x)], 'reverse inventory contains an excluded file')",
                                 "        require(True, 'reverse inventory contains an excluded file')"),
                                ("        require(sorted(lst) == reverse_list, 'reverse inventory differs from AGENTS + contract + shared premises')",
                                 "        require(True, 'reverse inventory differs from AGENTS + contract + shared premises')")],
  'deliberation_added'),
 ('negation_aware_phrase_scan', [("    require(not bad, 'affirmative forbidden phrase in ' + label + ': ' + json.dumps(bad[:2]))",
                                  "    require(True, 'affirmative forbidden phrase in ' + label + ': ' + json.dumps(bad[:2]))")],
  'affirmative_thermodynamic_limit'),
 ('placeholder_span_rejected', [("        require(not (re.search(r'\\s', inner) or '|' in inner or 'e.g.' in inner),\n                'placeholder angle-bracket span in '",
                                 "        require(True,\n                'placeholder angle-bracket span in '")],
  'angle_span_with_whitespace'),
 ('coherent_evidence_tampering', [("            require(cid in ids and ids[cid]['passed'] is True and ids[cid].get('rejected_mutations'), 'required control missing or failed: ' + cid)",
                                   "            require(True, 'required control missing or failed: ' + cid)")],
  'control_boolean_flipped_hash_rebound'),
]
REV = [
 ('coherent_evidence_tampering', [("    require(hashlib.sha256(raw).hexdigest() == expected_sha, 'contract bytes do not match the bound hash')",
                                   "    require(True, 'contract bytes do not match the bound hash')")], 'byte_change_without_rehash'),
 ('exact_arithmetic_admission', [("def parse_q(value):\n    if isinstance(value, bool) or isinstance(value, float):\n        raise AdmissionError('non-exact numeric input rejected: ' + repr(value))\n",
                                  "def parse_q(value):\n    if isinstance(value, float):\n        return Q(value)\n    if isinstance(value, bool):\n        raise AdmissionError('non-exact numeric input rejected: ' + repr(value))\n")], 'float_tau'),
 ('no_priority_or_continuum_claim', [("        require(flags.get(k) is False, 'claim flag must be false: ' + k)", "        require(True, 'claim flag must be false: ' + k)")], 'continuum_true'),
 ('changed_model_relabelled', [("    require(abs(parse_q(pk['tau'])) <= parse_q(pre['tau']['value']), 'coupling above the preregistered cap')",
                                "    require(True, 'coupling above the preregistered cap')")], 'coupling_above_cap'),
 ('insufficient_verdict_retained', [("    require(recorded == producer_outcome(**inputs), 'recorded outcome differs from the rule-derived outcome')",
                                     "    require(True, 'recorded outcome differs from the rule-derived outcome')")], 'floor_only_relabelled_accepted'),
 ('tau_scaling_exponent', [("    require(lo <= ratio <= hi, 'tau -> tau/100 ratio ' + sci(ratio, 8) + ' outside the prefrozen bracket')",
                            "    require(True, 'tau -> tau/100 ratio ' + sci(ratio, 8) + ' outside the prefrozen bracket')")], 'first_order_cancellation_as_headline'),
 ('wrong_delta_alpha_hbar_clock', [("    require(value == -tau / 72, 'first-order face amplitude must be -tau/72 in both unit systems')",
                                    "    require(True, 'first-order face amplitude must be -tau/72 in both unit systems')")], 'mixed_units_tau_over_9'),
 ('missing_incoming_stars', [("    require(stars_per_site == 4, 'per-site sum must include incoming stars (4 stars, 28|tau|), not %d' % stars_per_site)",
                              "    require(True, 'per-site sum must include incoming stars (4 stars, 28|tau|), not %d' % stars_per_site)")], 'outgoing_star_only_J_7'),
 ('root_n_misuse', [("    require(value >= count * per, 'anchored sum is an l1 sum over faces; '", "    require(True, 'anchored sum is an l1 sum over faces; '")], 'sqrt49_first_order'),
 ('tier_mixing_rejected', [("        require(t_kind == 'self_consistent_T(rho)' and M_kind == 'two_balls', 'exact_first_order constant mixes tiers: '",
                            "        require(True, 'exact_first_order constant mixes tiers: '")], 'first_order_cancellation_with_crude_t_labelled_exact'),
 ('reverse_premise_isolation', [("        require(not f.startswith(FORBIDDEN_PREFIXES), 'forbidden premise in reverse inputs: ' + f)",
                                 "        require(True, 'forbidden premise in reverse inputs: ' + f)"),
                                ("    require(sorted(files) == sorted(expected) and len(files) == len(expected),",
                                 "    require(set(expected) <= set(files),")], 'forward_ba1_added'),
 ('face_count_all_sites', [("    require(derivation == 'translation covariance over the anchors u-S from the I1 table', 'face counts must be derived, not '",
                            "    require(True, 'face counts must be derived, not '")], 'literal_counts'),
 ('uniform_in_N_not_in_a', [("        require('in n at fixed spacing' in low or 'uniformly in the cutoff' in low, 'unqualified uniformity word next to a rate')",
                             "        require(True, 'unqualified uniformity word next to a rate')")], 'unqualified_uniform_rate'),
 ('placeholder_span_rejected', [("        require(not (re.search(r'\\s', inner) or '|' in inner or 'e.g.' in inner), 'placeholder span: <' + inner + '>')",
                                 "        require(True, 'placeholder span: <' + inner + '>')")], 'angle_span_with_space'),
 ('negation_aware_phrase_scan', [("    require(hits == [], 'affirmative forbidden phrasing: ' + json.dumps(hits[:2]))",
                                  "    require(True, 'affirmative forbidden phrasing: ' + json.dumps(hits[:2]))")], 'affirmative_thermodynamic_limit'),
 ('parameters_declare_metric_weights_window', [("        require(k in p and bool(p[k]), 'contract parameters must declare ' + k)",
                                                "        require(k == 'clock' or (k in p and bool(p[k])), 'contract parameters must declare ' + k)")], 'clock_removed'),
 ('global_lipschitz_not_decay', [("    require(abs(value_at_R) <= claimed_bound, 'claimed decay bound '", "    require(True, 'claimed decay bound '")],
  'nonlocal_fixture_lipschitz_power_claim'),
 ('weighted_norm_contraction_rechecked', [("    require(cited == 'evaluated at the declared rho', 'disc contraction cited from ' + cited + ' instead of re-evaluated')",
                                           "    require(True, 'disc contraction cited from ' + cited + ' instead of re-evaluated')")], 'real_cap_constants_cited_for_disc'),
 ('loss_per_interaction_not_per_creation', [("    require(out_diam <= budget, 'reach charged %s gives %d < output diameter %d' % (rule, budget, out_diam))",
                                             "    require(True, 'reach charged %s gives %d < output diameter %d' % (rule, budget, out_diam))")], 'per_creation_reach_first_order_face'),
 ('diameter_subadditivity_through_interaction', [("    require(diam(M, metric) <= bound, 'output diameter %d exceeds the %s-rule bound %d' % (diam(M, metric), rule, bound))",
                                                  "    require(True, 'output diameter %d exceeds the %s-rule bound %d' % (diam(M, metric), rule, bound))")], 'max_instead_of_sum'),
 ('coarse_metric_named', [("    require(METRICS[distance_metric][1] == diameter_convention, 'metric mixing: %s distances with diameter %d'",
                           "    require(True, 'metric mixing: %s distances with diameter %d'")], 'l1_distance_with_linf_diameter'),
 ('weight_direction_toward_source', [("    require(bound < unweighted, 'the weighted bound at R, '", "    require(True, 'the weighted bound at R, '"),
                                     ("    require(all(weights[i] >= weights[i + 1] for i in range(n)), 'difference weight grows with distance from R '",
                                      "    require(True, 'difference weight grows with distance from R '")], 'weight_growing_from_R'),
 ('cardinality_weight_rate_labelled', [("        require(rate >= q_card_lower, 'cardinality rate ' + sci(rate, 6) + ' is below q_min^(1/4)')",
                                        "        require(True, 'cardinality rate ' + sci(rate, 6) + ' is below q_min^(1/4)')")], 'cardinality_relabelled_diameter_rate'),
 ('boundary_distance_exact', [("    require(claimed == actual, 'claimed source distance %d differs from the enumerated %d' % (claimed, actual))",
                               "    require(True, 'claimed source distance %d differs from the enumerated %d' % (claimed, actual))")], 'nested_shell_distance_N'),
 ('boundary_source_new_terms_only', [("    require(set(inv) == set(A) ^ set(B), 'source inventory differs from the symmetric difference of the two boxes')",
                                      "    require(True, 'source inventory differs from the symmetric difference of the two boxes')")], 'source_missing_a_new_star'),
 ('f2_regrouping_charged_once', [("    require(len(charges) == len(set(charges)), 'an F2 face is charged twice')", "    require(True, 'an F2 face is charged twice')")], 'face_charged_twice'),
 ('rate_constant_pair_prefrozen', [("    require(parse_q(pair['q']) == q and parse_q(pair['K_target']) == K_target, 'rate/constant pair differs from the frozen pair')",
                                    "    require(True, 'rate/constant pair differs from the frozen pair')")], 'headline_q_optimized'),
 ('q_min_not_crossed', [("    require(q >= q_min, 'rate ' + sci(q, 6) + ' crosses the proved minimum q_min='", "    require(True, 'rate ' + sci(q, 6) + ' crosses the proved minimum q_min='")],
  'rate_half_q_min'),
 ('analytic_route_disc_radius', [("    require(obj == 'AM2 creation coefficients' or zero_free_region_proved is True,", "    require(True,")], 'reduced_density_analytic_on_disc'),
 ('untruncated_coefficients_not_asserted', [("        require('not' in window or 'no ' in window, 'untruncated creation coefficients asserted')",
                                             "        require(True, 'untruncated creation coefficients asserted')")], 'untruncated_asserted'),
 ('decay_rate_in_N_not_a', [("    require(unit == 'per coarse step at fixed spacing (a coarse step is (4a,2a,a))',", "    require(True,")], 'per_fermi'),
 ('coefficient_decay_not_marginal_decay', [("        require(coefficient_difference != 0 or state_trace_norm_sq == 0,", "        require(True,")], 'state_decay_inferred'),
 ('two_families_named', [("    require(list(families) == [F1_NAME, F2_NAME], 'exactly the two named construction families: '",
                          "    require(True, 'exactly the two named construction families: '")], 'single_family'),
 ('subsequence_versus_whole_sequence', [("        require(basis == 'Cauchy bound' and obj == 'AM2 creation coefficients on supports meeting R in each Q_L',",
                                         "        require(True,")], 'whole_sequence_states'),
 ('full_original_wilson_cover', [("    require(n_links == 48 and n_endpoints == 36, 'cover must be the complete factors (48 links, 36 endpoints), not drawn links')",
                                  "    require(True, 'cover must be the complete factors (48 links, 36 endpoints), not drawn links')")], 'four_drawn_links'),
 ('gate_fields_topic_specific', [("        require(fields[k] == v, 'gate field value differs from the contract: ' + k)",
                                  "        require(True, 'gate field value differs from the contract: ' + k)")], 'rate_in_N_false'),
 ('ball_radius_not_used_as_tree_decay_ratio', [("    require(prov in ('disc radius rho=64|tau| (q=|tau|/rho), disc contraction checked',", "    require(True or prov in ('disc radius rho=64|tau| (q=|tau|/rho), disc contraction checked',")],
  'ball_radius_as_ratio'),
]


# ------------------------------------------------------------------ producer value validators
def check_by_id(res, cid):
    for c in res['checks']:
        if c['id'] == cid:
            return c
    raise Rejected('check missing: ' + cid)


def validate_forward(res, tau, template, targets):
    reject(res.get('contract_sha256') == CONTRACT_SHA256 and res.get('direction') == 'forward', 'forward identity')
    h = res['headline']
    w_max = R / (28 * tau * G_R)
    for pair, w, tgt in (('headline_pair', F(64), targets['headline']), ('floor_pair', w_max, targets['floor'])):
        want = fwd_formula(tau, w, 'exact_first_order')
        blk = h[pair]
        for sgn in ('+', '-'):
            ps = blk['per_sign'][sgn]
            reject(fq(ps['tau']) == (tau if sgn == '+' else -tau), 'forward sign replay')
            for key in ('K_F1_vs_F2', 'K_nested', 'K_general_telescoping', 'K_general_direct', 'K_union', 'K_own', 'T_w'):
                reject(fq(ps[key]) == want[key], 'forward %s %s not reproduced by the declared formula' % (pair, key))
            reject(fq(ps['Gamma_w']) == want['Gamma'] and fq(ps['source']) == want['source'], 'forward Gamma or source')
            reject(fq(ps['K_pair']) == fwd_pair(want), 'forward %s K_pair not the largest comparison' % pair)
        reject(fq(blk['K_pair']) == fwd_pair(want) and fq(blk['K_target']) == tgt, 'forward %s pair value or target' % pair)
        reject(blk['target_met'] is (fq(blk['K_pair']) <= tgt), 'forward %s target flag' % pair)
        reject(blk['tier'] == 'exact_first_order' and blk['route'] == 'weighted_norm', 'forward %s tier or route' % pair)
    crude = fwd_formula(tau, F(64), 'crude_majorant')
    reject(fq(h['crude_tier_at_q_1_64']['K_pair']) == fwd_pair(crude), 'forward crude headline not reproduced')
    reject(h['crude_tier_at_q_1_64']['meets_headline_target'] is False and fwd_pair(crude) > targets['headline'],
           'forward crude tier must fail and be retained')
    crude_f = fwd_formula(tau, w_max, 'crude_majorant')
    reject(fq(h['floor_pair']['crude_majorant_tier']['K_pair']) == fwd_pair(crude_f)
           and h['floor_pair']['crude_majorant_tier']['target_met'] is True, 'forward crude floor not reproduced')
    comps = h['comparisons']
    hw = fwd_formula(tau, F(64), 'exact_first_order')
    fw = fwd_formula(tau, w_max, 'exact_first_order')
    rows = {'F1 on Lambda_N versus F1 on Lambda_{N+1}': ('K_nested', 'N', 'N+1'),
            'F2 on Lambda_N versus F2 on Lambda_{N+1}': ('K_nested', 'N', 'N+1'),
            'F1 versus F2 on the same Lambda_N': ('K_F1_vs_F2', 'N-1', 'N')}
    for name, (key, dz, d0) in rows.items():
        c = comps[name]
        reject(fq(c['K_headline']) == hw[key] and fq(c['K_floor']) == fw[key], 'forward comparison ' + name)
        reject(c['distance_e_z'] == dz and c['distance_0'] == d0, 'forward distance ' + name)
    reject(fq(comps['any two centered boxes Lambda_M, Lambda_M\' (M, M\' at least N) of F1 or F2']['K_headline'])
           == hw['K_general_telescoping'], 'forward general comparison')
    reject(fq(comps['two finite complete-factor volumes of one prescription both containing Lambda_N (labelled)']['K_headline'])
           == hw['K_union'], 'forward union comparison')
    ratios = check_by_id(res, 'tau_scaling_exponent')['ratios']
    r_head = fwd_pair(hw) / fwd_pair(fwd_formula(tau / 100, F(64), 'exact_first_order'))
    r_floor = fwd_pair(fw) / fwd_pair(fwd_formula(tau / 100, R / (28 * (tau / 100) * G_R), 'exact_first_order'))
    reject(fq(ratios['headline_K_pair']['exact']) == r_head and F(95) <= r_head <= F(105), 'forward headline ratio')
    reject(fq(ratios['floor_K_pair']['exact']) == r_floor and F(99, 100) <= r_floor <= F(101, 100), 'forward floor ratio')
    reject(fq(ratios['q_min']['exact']) == 100 and fq(ratios['floor_K_nested_contract_form']['exact']) == 100,
           'forward q_min and nested floor ratio')
    reject(res['mandatory_sentence'] == template, 'forward mandatory sentence')
    return True


def validate_reverse(res, tau, template, targets):
    reject(res.get('contract_sha256') == CONTRACT_SHA256 and res.get('direction') == 'reverse', 'reverse identity')
    h = res['headline']
    tau_star = R / (28 * G_R)
    hp, fp = h['headline_pair'], h['floor_pair']
    reject(fq(hp['K']['exact']) == rev_formula(tau, 64 * tau) and fq(hp['q']) == F(1, 64), 'reverse headline K not reproduced')
    reject(fq(fp['K']['exact']) == rev_formula(tau, tau_star) and fq(fp['q']) == tau / tau_star, 'reverse floor K not reproduced')
    reject(hp['tier'] == fp['tier'] == 'exact_first_order' and hp['route'] == fp['route'] == 'analytic_disc',
           'reverse tier or route')
    reject(hp['target_met'] is (fq(hp['K']['exact']) <= targets['headline'])
           and fp['target_met'] is (fq(fp['K']['exact']) <= targets['floor']), 'reverse target flags')
    reject(hp['signs'] == {'+': True, '-': True} and fp['signs'] == {'+': True, '-': True}, 'reverse both signs')
    ch, cf = h['crude_tier_headline_q'], h['crude_tier_floor_q']
    reject(fq(ch['K']['exact']) == rev_formula(tau, 64 * tau, tier='crude_majorant') and ch['target_met'] is False,
           'reverse crude headline must fail and be retained')
    reject(fq(cf['K']['exact']) == rev_formula(tau, tau_star, tier='crude_majorant') == 2 * R and cf['target_met'] is True,
           'reverse crude floor')
    ref = check_by_id(res, 'labelled_refinements')
    reject(fq(ref['sharp_exponent']['headline_K_times_q']['exact']) == rev_formula(tau, 64 * tau, count='sharp')
           and fq(ref['sharp_exponent']['floor_K_times_q_min']['exact']) == rev_formula(tau, tau_star, count='sharp'),
           'reverse sharp refinement')
    reject(fq(ref['first_order_cancellation']['headline']['exact'])
           == rev_formula(tau, 64 * tau, sup='first_order_cancellation'), 'reverse cancellation refinement')
    reject(fq(ref['cauchy_coefficient_form']['headline']['exact']) == rev_formula(tau, 64 * tau, cauchy='coefficientwise'),
           'reverse coefficientwise form')
    kh = rev_formula(tau, 64 * tau)
    tele = kh * (2 - F(1, 64)) / (1 - F(1, 64))
    reject(fq(ref['telescoped_general']['headline']['exact']) == tele and tele > targets['headline']
           and ref['telescoped_general']['meets_headline_target'] is False, 'reverse telescoping must be recorded as missing')
    rat = check_by_id(res, 'tau_scaling_per_constant')['ratios']
    r_head = kh / rev_formula(tau / 100, 64 * tau / 100)
    reject(fq(rat['K_exact_first_order_at_q_1_64']['exact']) == r_head and F(95) <= r_head <= F(105), 'reverse headline ratio')
    reject(fq(rat['K_floor_pair']['exact']) == 1 and fq(rat['q_min']['exact']) == 100, 'reverse floor and q_min ratios')
    reject(res['mandatory_sentence_template'] == template, 'reverse mandatory sentence')
    return True


def phrase_hits(text, forbidden, template=None):
    body = re.sub(r'\s+', ' ', str(text)).strip()
    if template:
        body = body.replace(re.sub(r'\s+', ' ', template).strip(), ' ')
    hits = []
    for clause in [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', body) if c.strip()]:
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                if not NEGATION.search(clause):
                    hits.append({'phrase': phrase, 'clause': clause[:160]})
    return hits


# ------------------------------------------------------------------ mutation harness
def mutated_run(direction, edits=(), extra_input=None, contract_append=None):
    src = ROOT / PROD[direction]
    with tempfile.TemporaryDirectory(prefix='hnm-r33-ba1-review-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / PROD[direction]
        dst.mkdir(parents=True)
        shutil.copyfile(src / 'check.py', dst / 'check.py')
        shutil.copyfile(src / 'report.md', dst / 'report.md')
        shutil.copytree(src / 'inputs', dst / 'inputs')
        text = (dst / 'check.py').read_text(encoding='utf-8')
        for old, new in edits:
            if text.count(old) != 1:
                raise ReviewFailure('mutation anchor not unique in %s: %r' % (direction, old[:60]))
            text = text.replace(old, new)
        (dst / 'check.py').write_text(text, encoding='utf-8')
        if extra_input is not None:
            p = dst / 'inputs' / extra_input
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('skeptic mutation fixture\n')
        if contract_append is not None:
            p = dst / 'inputs' / CONTRACT_REL
            p.write_bytes(p.read_bytes() + contract_append)
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(dst / 'check.py'), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(repo))
        outputs = {p.name: p.read_bytes() for p in sorted(out.glob('*.json'))} if out.is_dir() else {}
        last = done.stderr.strip().splitlines()[-1] if done.stderr.strip() else ''
        if any(p.name == '__pycache__' or p.suffix == '.pyc' for p in repo.rglob('*')):
            raise ReviewFailure('interpreter cache written into a mutated copy')
        return done.returncode, outputs, last.replace(tmp, '<tmp>')


def replay(rel_script, optimized):
    with tempfile.TemporaryDirectory(prefix='hnm-r33-ba1-replay-') as tmp:
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if optimized else [])
        done = subprocess.run([sys.executable] + flags + [str(ROOT / rel_script), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(ROOT))
        if done.returncode != 0:
            raise ReviewFailure('replay failed: ' + rel_script + ' ' + done.stderr[-400:])
        return {p.name: sha(p) for p in sorted(out.glob('*.json'))}


# ------------------------------------------------------------------ execute
def execute():
    contract_bytes = (ROOT / CONTRACT_REL).read_bytes()
    need(sha_bytes(contract_bytes) == CONTRACT_SHA256, 'contract_sha256_pinned', sha256=CONTRACT_SHA256)
    con = json.loads(contract_bytes)
    pre = con['preregistration']
    tau = F(pre['tau']['value'])
    template = pre['mandatory_sentence_template']
    forbidden = ROUND_FORBIDDEN + list(pre['forbidden_phrasings'])
    rc = con['parameters']['rate_constant_pair']
    targets = {'headline': F(rc['headline']['K_target']), 'floor': F(rc['rate_floor']['K_target'])}
    q_head, q_floor = F(rc['headline']['q']), F(rc['rate_floor']['q'])
    tau_star = R / (28 * G_R)
    need(targets == {'headline': F(1, 2000000), 'floor': F(1, 12)} and q_head == F(1, 64) and q_floor == F(148, 390625)
         and tau == F(1, 10 ** 8) and q_floor == tau / tau_star, 'contract_pairs_read')

    # 1. closures, inventories, isolation, snapshots
    inventory = sorted(['AGENTS.md', CONTRACT_REL] + list(con['shared_premises']))
    closures = {}
    res = {}
    for d, rel in sorted(PROD.items()):
        base = ROOT / rel
        fz_bytes = (base / 'freeze.json').read_bytes()
        if sha_bytes(fz_bytes) != FREEZE_SHA[d]:
            raise ReviewFailure('freeze record changed: ' + d)
        fz = json.loads(fz_bytes)
        files = sorted(p.relative_to(ROOT).as_posix() for p in base.rglob('*')
                       if p.is_file() and p.name != 'freeze.json')
        if any('__pycache__' in f or f.endswith('.pyc') for f in files):
            raise ReviewFailure('interpreter cache inside closure ' + d)
        if files != sorted(fz['sources']) or any(sha(ROOT / f) != h for f, h in fz['sources'].items()):
            raise ReviewFailure('closure differs from freeze.json: ' + d)
        inputs = sorted(p.relative_to(base / 'inputs').as_posix() for p in (base / 'inputs').rglob('*') if p.is_file())
        if inputs != inventory:
            raise ReviewFailure('input inventory differs from AGENTS.md + contract + shared_premises: ' + d)
        if any((base / 'inputs' / f).read_bytes() != (ROOT / f).read_bytes() for f in inputs):
            raise ReviewFailure('snapshot differs from its repository source: ' + d)
        forbidden_present = [f for f in inputs if f.startswith(FORBIDDEN_IN_REVERSE)]
        if forbidden_present:
            raise ReviewFailure('isolation: ' + d + ' ' + json.dumps(forbidden_present))
        if fz['contract_sha256'] != CONTRACT_SHA256 or fz['loop'] != 'BA1' or fz['direction'] != d \
                or fz['normal_optimized_identical'] is not True:
            raise ReviewFailure('freeze identity ' + d)
        res[d] = json.loads((base / 'output/results.json').read_text())
        closures[d] = {'closure_files': len(fz['sources']), 'inputs': len(inputs), 'freeze_json_sha256': FREEZE_SHA[d],
                       'results_sha256': sha(base / 'output/results.json'),
                       'source_manifest_sha256': sha(base / 'output/source-manifest.json'),
                       'check_py_sha256': sha(base / 'check.py'), 'report_sha256': sha(base / 'report.md'),
                       'checks': len(res[d]['checks'])}
    need(len(inventory) == 27 and con['forward_additional_premises'] == [] and con['reverse_premise_isolation'] is True,
         'closures_inventories_and_reverse_isolation', closures=closures, inventory=27,
         note='both inputs/ equal AGENTS.md + contract + the 25 shared premises byte for byte; no Round33 skeptic, '
              'expert, deliberation, plan, panel or forward file in either inventory')
    need(res['forward']['check_py_sha256_recorded_before_evaluation'] == closures['forward']['check_py_sha256']
         and res['reverse']['check_py_sha256_recorded_before_evaluation'] == closures['reverse']['check_py_sha256'],
         'check_py_sha256_recorded_before_evaluation_matches_frozen')

    # 2. replays: both producers and the skeptic pre-comparison program, normal and -O
    replays = {}
    for d, rel in sorted(PROD.items()):
        frozen = {p.name: sha(p) for p in sorted((ROOT / rel / 'output').glob('*.json'))}
        runs = {mode: replay(rel + '/check.py', mode == 'optimized') for mode in ('normal', 'optimized')}
        if runs['normal'] != frozen or runs['optimized'] != frozen:
            raise ReviewFailure('producer replay differs from frozen output: ' + d)
        replays[d] = {'frozen_outputs': frozen, 'normal_and_optimized_byte_identical_to_frozen': True}
    pre_fz_bytes = (ROOT / PRE_FREEZE_REL).read_bytes()
    pre_fz = json.loads(pre_fz_bytes)
    if sha_bytes(pre_fz_bytes) != PRE_FREEZE_SHA or pre_fz['contract_sha256'] != CONTRACT_SHA256 \
            or any(sha(ROOT / f) != h for f, h in pre_fz['files'].items()):
        raise ReviewFailure('skeptic pre-comparison package changed after its freeze')
    pre_runs = {mode: replay(PRE_CHECK_REL, mode == 'optimized') for mode in ('normal', 'optimized')}
    if pre_runs['normal'] != {'results.json': sha(ROOT / PRE_RESULTS_REL)} or pre_runs['optimized'] != pre_runs['normal']:
        raise ReviewFailure('skeptic pre-comparison replay differs')
    replays['skeptic_pre_comparison'] = {'results_sha256': sha(ROOT / PRE_RESULTS_REL), 'freeze_record_sha256': PRE_FREEZE_SHA,
                                         'files_unchanged': sorted(pre_fz['files']),
                                         'normal_and_optimized_byte_identical_to_frozen': True}
    need(True, 'replays_byte_identical', replays=replays)

    # 3. values: every producer constant re-derived; predictions; binding
    need(validate_forward(res['forward'], tau, template, targets), 'forward_values_reproduced_exactly',
         note='every per-sign, per-comparison, crude and floor constant and the tau ratios re-derived from the '
              'declared formula (Gamma=J w G\'(R), S=w t_1+Gamma T_w, telescoping 1/(1-q))')
    need(validate_reverse(res['reverse'], tau, template, targets), 'reverse_values_reproduced_exactly',
         note='2T(rho) at rho=64|tau| and tau_star, crude 2x28 rho G(R), sharp and cancellation refinements, '
              'coefficientwise form, telescoping, tau ratios')
    pre_res = json.loads((ROOT / PRE_RESULTS_REL).read_text())
    pc = {k: F(v['value']) for k, v in pre_res['constants'].items()}
    hw, fw = fwd_formula(tau, F(64), 'exact_first_order'), fwd_formula(tau, R / (28 * tau * G_R), 'exact_first_order')
    fwd_head, fwd_floor = fwd_pair(hw), fwd_pair(fw)
    rev_head, rev_floor = rev_formula(tau, 64 * tau), rev_formula(tau, tau_star)
    need(fq(res['reverse']['headline']['headline_pair']['K']['exact']) == pc['rev_head'] == rev_head
         and fq(res['reverse']['headline']['floor_pair']['K']['exact']) == pc['rev_floor'] == rev_floor
         and fq(res['reverse']['headline']['crude_tier_headline_q']['K']['exact']) == pc['rev_head_crude']
         and fq(res['reverse']['headline']['crude_tier_floor_q']['K']['exact']) == pc['rev_floor_crude']
         and rev_formula(tau, 64 * tau, count='sharp') == pc['rev_head_sharp']
         and rev_formula(tau, 64 * tau, cauchy='coefficientwise') == pc['rev_head_coefwise'],
         'reverse_equals_pre_comparison_prediction',
         identical=['headline 49/111790368', 'floor 49/2018304', 'crude 296/390625 and 1/32', 'sharp 49/7154583552',
                    'coefficientwise 14/31441041'])
    k12_variant = F(19140625, 86785322066496)
    need(hw['K_F1_vs_F2'] == k12_variant and hw['K_F1_vs_F2'] >= pc['fwd_head'] and fw['K_F1_vs_F2'] >= pc['fwd_floor']
         and hw['K_general_telescoping'] == hw['K_F1_vs_F2'] / (1 - q_head) and fwd_head == F(2734375, 12204185915601)
         and fwd_floor == F(708203125, 43148545682688) and skeptic_sharp_forward(tau, 64) == pc['fwd_head'],
         'forward_reconciled_with_pre_comparison',
         forward_F1_vs_F2=q(hw['K_F1_vs_F2']), skeptic_contract_form=q(pc['fwd_head']),
         forward_general=q(fwd_head), forward_floor=q(fwd_floor), skeptic_floor=q(pc['fwd_floor']),
         reason='the forward uses G\'(R) (at most 352) in Gamma and in the remainder, the skeptic G\'(T_w); the forward '
                'binds the telescoped general comparison (factor 1/(1-q)=64/63); its F1-vs-F2 constant is the exact '
                'variant listed in the skeptic derivation section 10; all are valid upper bounds')
    bind_head, bind_floor = max(fwd_head, rev_head), max(fwd_floor, rev_floor)
    need(bind_head == rev_head and bind_floor == rev_floor and bind_head <= targets['headline']
         and bind_floor <= targets['floor'] and fwd_head <= bind_head and fwd_floor <= bind_floor,
         'binding_larger_valid_K_per_pair', headline=q(bind_head), floor=q(bind_floor),
         headline_margin=preview(targets['headline'] / bind_head), floor_margin=preview(targets['floor'] / bind_floor),
         forward_headline_labelled=q(fwd_head), forward_floor_labelled=q(fwd_floor),
         note='both routes certify K at most the bound value: the forward proves a smaller K for every comparison')
    r_bind_head = bind_head / rev_formula(tau / 100, 64 * tau / 100)
    r_bind_floor = bind_floor / rev_formula(tau / 100, tau_star)
    crude_fwd, crude_rev = fwd_pair(fwd_formula(tau, F(64), 'crude_majorant')), rev_formula(tau, 64 * tau, tier='crude_majorant')
    need(r_bind_head == F(4340004, 43129) and F(95) <= r_bind_head <= F(105) and r_bind_floor == 1
         and crude_fwd == F(9472, 24454143) and crude_rev == F(296, 390625) and min(crude_fwd, crude_rev) > targets['headline'],
         'bound_constants_scaling_and_crude_tier', ratio_headline=q(r_bind_head), ratio_floor='1', q_min_ratio='100',
         crude_forward=q(crude_fwd), crude_reverse=q(crude_rev))
    tele = rev_head * (2 - q_head) / (1 - q_head)
    union_rev = 2 * rev_head
    need(tele > targets['headline'] and union_rev > targets['headline'] and hw['K_union'] <= targets['headline']
         and hw['K_general_direct'] <= targets['headline'], 'general_comparison_routes',
         reverse_telescoped=q(tele), reverse_two_step_union=q(union_rev), reverse_direct=q(rev_head),
         forward_union_2K_nested=q(hw['K_union']),
         note='the reverse must compare two volumes directly (as it does); telescoping or a two-step union at exponent '
              'N-1 would miss 1/2000000; the face sets are totally ordered, so any pair is one nested comparison')
    cancel = rev_formula(tau, 64 * tau, sup='first_order_cancellation')
    cancel_ratio = cancel / rev_formula(tau / 100, 64 * tau / 100, sup='first_order_cancellation')
    need(cancel == F(3773, 1364628515625) and cancel_ratio > 10000 and not (F(95) <= cancel_ratio <= F(105))
         and pc['rev_head_remainder'] <= cancel, 'first_order_cancellation_is_quadratic',
         reverse_value=q(cancel), ratio=preview(cancel_ratio), skeptic_pre_value=q(pc['rev_head_remainder']),
         note='self-correction: the pre-comparison listed this refinement without noting that it is quadratic in tau '
              'and so outside the prefrozen linear headline bracket; it is a labelled refinement only')
    k_ref = (F(49, 144) * tau + F(49, 3) * tau * GP_R * hw['T_w']) / (1 - hw['Gamma'])
    fwd_ref = check_by_id(res['forward'], 'labelled_refinements_and_alternatives')['refined_source_loss_F1_vs_F2']['K']
    need(fq(fwd_ref) == k_ref == F(57270955, 16662781836767232) and k_ref < hw['K_F1_vs_F2'], 'forward_loss_one_refinement_reproduced', value=q(k_ref),
         note='source loss 1 because the extra F2 faces lie inside the outer layer; face-level J_new=49|tau|/3 in the '
              'source remainder; labelled, not bound')
    no_decay = F(7, 25000000) * G_R / (1 - F(7, 25000000) * GP_R)
    with_two = F(7, 25000000) * G_R / (1 - 2 * F(7, 25000000) * GP_R)
    need(no_decay == F(37, 6249384) and with_two == F(37, 6248768), 'lipschitz_wording_reconciled',
         map_lipschitz='J_0G\'(R) < 77/781250', exclusion_constant='2J_0G\'(R) < 77/390625',
         note='the contract semantics of global_lipschitz_not_decay (skeptic loop-1/2 wording) call 2J_0G\'(R) the '
              'sup-norm Lipschitz constant; 37/6249384 uses J_0G\'(R); both producers found this independently')

    # 4. damaged packets rejected by this review's validator
    def damaged(direction, fn):
        pk = json.loads(json.dumps(res[direction]))
        fn(pk)
        return lambda: (validate_forward if direction == 'forward' else validate_reverse)(pk, tau, template, targets)

    def f_half(pk):
        pk['headline']['headline_pair']['K_pair'] = q(fq(pk['headline']['headline_pair']['K_pair']) / 2)

    def f_skeptic_value(pk):
        pk['headline']['headline_pair']['per_sign']['+']['K_F1_vs_F2'] = q(pc['fwd_head'])

    def f_crude(pk):
        pk['headline']['crude_tier_at_q_1_64']['meets_headline_target'] = True

    def f_sign(pk):
        pk['headline']['floor_pair']['per_sign']['-']['K_nested'] = q(fq(pk['headline']['floor_pair']['per_sign']['-']['K_nested']) * 2)

    def f_dist(pk):
        pk['headline']['comparisons']['F1 versus F2 on the same Lambda_N']['distance_e_z'] = 'N'

    def r_sharp(pk):
        pk['headline']['headline_pair']['K']['exact'] = q(rev_formula(tau, 64 * tau, count='sharp'))

    def r_floor_ratio(pk):
        for c in pk['checks']:
            if c['id'] == 'tau_scaling_per_constant':
                c['ratios']['K_floor_pair']['exact'] = '100'

    def r_tele(pk):
        for c in pk['checks']:
            if c['id'] == 'labelled_refinements':
                c['telescoped_general']['meets_headline_target'] = True

    def r_crude(pk):
        pk['headline']['crude_tier_headline_q']['target_met'] = True

    def r_template(pk):
        pk['mandatory_sentence_template'] = template.replace('not decay of the reduced density, ', '')
    dmg = [('forward', 'headline_K_halved', f_half, 'pair value'), ('forward', 'skeptic_value_substituted', f_skeptic_value, 'not reproduced'),
           ('forward', 'crude_marked_met', f_crude, 'crude tier must fail'), ('forward', 'minus_sign_differs', f_sign, 'not reproduced'),
           ('forward', 'f1_vs_f2_distance_N', f_dist, 'forward distance'), ('reverse', 'sharp_as_contract_form', r_sharp, 'headline K'),
           ('reverse', 'floor_ratio_100', r_floor_ratio, 'floor and q_min ratios'),
           ('reverse', 'telescoping_marked_met', r_tele, 'telescoping'), ('reverse', 'crude_marked_met', r_crude, 'crude headline'),
           ('reverse', 'template_trimmed', r_template, 'mandatory sentence')]
    rows = []
    for d, label, fn, reason in dmg:
        if not rejects(damaged(d, fn), reason):
            raise ReviewFailure('damaged packet accepted: ' + label)
        rows.append({'producer': d, 'mutation': label, 'rejected_for': reason})
    need(True, 'damaged_packets_rejected_by_review_validator', rows=rows)

    # 5. source-edit runs on temporary copies
    runs = []
    for d in ('forward', 'reverse'):
        code, outs, last = mutated_run(d)
        frozen = {p.name: p.read_bytes() for p in sorted((ROOT / PROD[d] / 'output').glob('*.json'))}
        if code != 0 or outs != frozen:
            raise ReviewFailure('unmutated copy does not reproduce the frozen output: ' + d)
        runs.append({'producer': d, 'edit': 'unmutated copy', 'outcome': 'reproduces frozen output byte for byte'})
    label_sets = {}
    for d in ('forward', 'reverse'):
        labels = {}
        for c in res[d]['checks']:
            rm = c.get('rejected_mutations')
            if rm:
                labels[c['id']] = sorted(rm) if isinstance(rm, list) else sorted(rm)
        label_sets[d] = labels
    controls = list(con['controls'])
    for d, table in (('forward', FWD), ('reverse', REV)):
        if sorted(t[0] for t in table) != sorted(controls):
            raise ReviewFailure('weakening table does not cover the 37 controls: ' + d)
        for cid, edits, label in table:
            if label not in label_sets[d].get(cid, []):
                raise ReviewFailure('expected label is not a mutation of the control: %s %s %s' % (d, cid, label))
            code, outs, last = mutated_run(d, edits=edits)
            m = re.search(r'damaging mutation accepted: (\S+)$', last)
            if code == 0 or outs or m is None or m.group(1) != label:
                raise ReviewFailure('weakening not caught at the intended control: %s %s (%s)' % (d, cid, last[-160:]))
            runs.append({'producer': d, 'control': cid, 'edit': 'validator weakened (%d anchor%s)' % (len(edits), 's' if len(edits) > 1 else ''),
                         'aborted_with': 'damaging mutation accepted: ' + label})
    input_edits = [
        ('forward', 'contract byte edit without rehash', dict(contract_append=b' '), 'contract'),
        ('reverse', 'contract byte edit without rehash', dict(contract_append=b' '), 'contract'),
        ('forward', 'undeclared skeptic file in inputs', dict(extra_input='research/round33/skeptic/triage.md'), ''),
        ('reverse', 'undeclared skeptic file in inputs', dict(extra_input='research/round33/skeptic/triage.md'), ''),
        ('reverse', 'forward BA1 report in inputs', dict(extra_input='research/round33/forward/ba1/report.md'), ''),
    ]
    for d, label, kw, token in input_edits:
        code, outs, last = mutated_run(d, **kw)
        if code == 0 or outs:
            raise ReviewFailure('input edit not caught: %s %s' % (d, label))
        runs.append({'producer': d, 'edit': label, 'outcome': 'aborted without output'})
    n_weak = sum(1 for r_ in runs if 'control' in r_)
    need(n_weak == 74, 'source_edit_runs', weakenings=n_weak, unmutated=2, input_edits=len(input_edits), runs=runs)

    # 6. reports: phrase scan, template span, checker counts
    scan = {}
    for d in ('forward', 'reverse'):
        text = (ROOT / PROD[d] / 'report.md').read_text(encoding='utf-8')
        hits = phrase_hits(text, forbidden, template)
        count = text.count(template)
        if hits or count != 1:
            raise ReviewFailure('report scan or template span: ' + d)
        scan[d] = {'affirmative_hits': 0, 'template_spans': 1}
    fwd_ctrl = [c for c in res['forward']['checks'] if c['id'] in controls]
    rev_ctrl = [c for c in res['reverse']['checks'] if c['id'] in controls]
    need(len(fwd_ctrl) == 37 == len(rev_ctrl) and all(c.get('rejected_mutations') for c in fwd_ctrl + rev_ctrl)
         and res['forward']['rejected_mutation_total'] == 96 and res['reverse']['damaging_mutations_total'] == 132
         and len(res['forward']['checks']) == 51 and len(res['reverse']['checks']) == 61,
         'reports_scanned_and_checker_counts', scan=scan, forward={'checks': 51, 'controls': 37, 'rejected_mutations': 96},
         reverse={'checks': 61, 'controls': 37, 'rejected_mutations': 132})
    gate_fields = dict(pre['gate_fields_required'])
    need(res['forward']['gate_fields'] == gate_fields == res['reverse']['gate_fields'], 'gate_fields_equal_contract',
         fields=sorted(gate_fields))

    # 7. the review statement, limitations and exported values
    statement = supported_statement(template, bind_head, bind_floor, fwd_head, fwd_floor)
    lims = limitations()
    hits = phrase_hits(statement, forbidden, template) + [h for x in lims for h in phrase_hits(x, forbidden, template)]
    norm = lambda s: re.sub(r'\s+', ' ', s).strip()
    need(hits == [] and norm(template) in norm(statement) and statement.count(template) == 1
         and not any(norm(template) in norm(x) for x in lims), 'review_statement_scanned_template_one_span')
    return {
        'loop': 'BA1', 'stage': 'post_comparison', 'reviewer': 'skeptic (model agent, correlated ancestry)',
        'human_author': 'Hruday N M (BUNZEEY)', 'contract_sha256': CONTRACT_SHA256,
        'verdict': 'accepted_within_scope', 'sub_label': 'boundary_decay_rate_only',
        'secondary_sub_labels': ['static_not_dynamic'], 'blocking_issues': [],
        'supported_statement': statement, 'limitations': lims, 'gate_fields': gate_fields,
        'recommended_bound': {
            'headline': {'q': '1/64', 'K': q(bind_head), 'K_preview': preview(bind_head), 'tier': 'exact_first_order',
                         'route': 'analytic_disc', 'disc_radius': '64|tau|', 'exponent': 'N-1', 'target': '1/2000000',
                         'margin_preview': preview(targets['headline'] / bind_head), 'tau_ratio': q(r_bind_head),
                         'also_certified_by': {'route': 'weighted_norm', 'K': q(fwd_head), 'K_preview': preview(fwd_head),
                                               'comparison': 'any two centered boxes, telescoped'}},
            'floor': {'q': '148/390625', 'K': q(bind_floor), 'K_preview': preview(bind_floor), 'tier': 'exact_first_order',
                      'route': 'analytic_disc', 'disc_radius': 'tau_star=1/37888', 'exponent': 'N-1', 'target': '1/12',
                      'margin_preview': preview(targets['floor'] / bind_floor), 'tau_ratio': '1',
                      'also_certified_by': {'route': 'weighted_norm', 'K': q(fwd_floor), 'K_preview': preview(fwd_floor)}},
            'crude_majorant_reported': {'headline_forward': q(crude_fwd), 'headline_reverse': q(crude_rev),
                                        'meets_headline_target': False,
                                        'floor_forward': q(fwd_pair(fwd_formula(tau, R / (28 * tau * G_R), 'crude_majorant'))),
                                        'floor_reverse': q(rev_formula(tau, tau_star, tier='crude_majorant')),
                                        'meets_floor_target': True},
            'q_min': q(q_floor), 'q_min_ratio': '100'},
        'admitted_values': {
            'forward': {'K_F1_vs_F2': q(hw['K_F1_vs_F2']), 'K_nested': q(hw['K_nested']),
                        'K_general_telescoping': q(hw['K_general_telescoping']), 'K_general_direct': q(hw['K_general_direct']),
                        'K_union_one_prescription': q(hw['K_union']), 'T_w_headline': q(hw['T_w']), 'Gamma_headline': q(hw['Gamma']),
                        'floor_K_F1_vs_F2': q(fw['K_F1_vs_F2']), 'floor_K_nested': q(fw['K_nested']),
                        'floor_K_general_telescoping': q(fw['K_general_telescoping']), 'T_w_floor': q(fw['T_w']),
                        'Gamma_floor': q(fw['Gamma']), 'headline_tau_ratio': q(fwd_head / fwd_pair(fwd_formula(tau / 100, F(64), 'exact_first_order')))},
            'reverse': {'headline': q(rev_head), 'floor': q(rev_floor), 'T_rho_headline': q(F(49, 144) * 64 * tau / (1 - 28 * 64 * tau * GP_R)),
                        'T_rho_floor': q(F(49, 144) * tau_star / (1 - 28 * tau_star * GP_R)),
                        'coefficientwise_headline': q(rev_formula(tau, 64 * tau, cauchy='coefficientwise')),
                        'telescoped_headline_misses': q(tele)},
            'labelled_refinements': {'reverse_sharp_exponent_headline': q(rev_formula(tau, 64 * tau, count='sharp')),
                                     'reverse_sharp_exponent_floor': q(rev_formula(tau, tau_star, count='sharp')),
                                     'reverse_first_order_cancellation_headline': q(cancel),
                                     'forward_loss_one_F1_vs_F2': q(k_ref),
                                     'skeptic_contract_form_forward_headline': q(pc['fwd_head'])},
            'no_decay_sup_norm_difference': q(no_decay), 'tau_star': q(tau_star)},
        'closures': closures, 'replays': replays,
        'continuum_claim': False, 'scientific_priority_verified': False, 'weak_coupling_claim': False,
        'state_decay_claimed': False, 'uniqueness_of_ground_state_claimed': False,
        'checks': CHECKS,
        'previews': {'bound_headline': preview(bind_head), 'bound_floor': preview(bind_floor),
                     'forward_headline': preview(fwd_head), 'forward_floor': preview(fwd_floor),
                     'headline_margin': preview(targets['headline'] / bind_head),
                     'forward_headline_margin': preview(targets['headline'] / fwd_head),
                     'reverse_telescoped': preview(tele), 'cancellation_ratio': preview(cancel_ratio)},
    }


def supported_statement(template, kh, kf, fh, ff):
    return ('In the AM2/AQ1 zero-selected patterned family (model AQ_patterned_zero_selected: SU(2) Kogut-Susskind form '
            'on Z^3 at fixed spacing, coarse 24-link factors, selected triple exactly (0,0,0) with Haar product reference, '
            '21 omitted faces per anchor entering as -(tau/3)W_f in normalized units delta=alpha/8; both signs '
            '|tau|<=10^-8; AM2 creation expansion with J<=28|tau|, R=1/64, G(t)=16e^{8t}(1+10t); cover R={0,e_z}; '
            'coarse l-infinity metric with star diameter d_X=1), with the named construction families F1 = AQ1 centered '
            'whole-star boxes Lambda_N=[-N,N]^3 and F2 = I1 section 6 all-contained-face boxes with padding on the same '
            'Lambda_N, N at least 2: ' + template + ' Constants (exact, both signs, every comparison of the contract: '
            'F1 on Lambda_N versus Lambda_(N+1), F2 on Lambda_N versus Lambda_(N+1), F1 versus F2 on the same Lambda_N, '
            'any two centered boxes of size at least N and any two complete-factor volumes of one prescription containing '
            'Lambda_N): headline pair q=1/64 with K=' + q(kh) + ' (about 4.3832e-7; exact_first_order tier, analytic_disc '
            'route on the disc of radius 64|tau|; margin about 1.1407 against the frozen 1/2000000), also certified by the '
            'weighted_norm route with the smaller K=' + q(fh) + ' (about 2.2405e-7, labelled); floor pair '
            'q=148/390625=37888|tau| with K=' + q(kf) + ' (about 2.4278e-5; exact_first_order tier, analytic_disc route on '
            'the disc of radius tau_star=1/37888), also certified by the weighted_norm route with K=' + q(ff) + ' (about '
            '1.6413e-5, labelled). The crude_majorant tier at q=1/64 (296/390625 analytic_disc, 9472/24454143 '
            'weighted_norm) misses 1/2000000 and is retained. The tau to tau/100 ratios are 4340004/43129 for the headline '
            'K, exactly 1 for the floor K and exactly 100 for q_min. The rate is in N, per coarse l-infinity step at fixed '
            'spacing; every interaction term present in one box and not the other lies at coarse l-infinity distance at '
            'least N-1 from R, and the bound uses the contract form ceil(d/diam) of the order-versus-distance count. For '
            'each family the whole sequence of coefficients on supports meeting R is Cauchy in each on-site cutoff space; '
            'this is a coefficient statement only, with no state, reduced density, common limit or untruncated coefficient '
            'asserted.')


def limitations():
    return [
        'Only the zero-selected patterned family (selected triple (0,0,0), Haar reference), the cover R={0,e_z}, fixed '
        'spacing and |tau|<=10^-8, with F1 and F2 on centered cubes Lambda_N, N at least 2, and complete-factor volumes of '
        'one prescription containing Lambda_N; nothing transfers to nonzero selected triples, the uniform route-B model, '
        'literal vertex boxes, weak coupling or the continuum; every constant is uniform in N at fixed spacing and in the '
        'cutoff, never in a.',
        'Coefficients only: the statements concern AM2 creation coefficients in each on-site cutoff space Q_L with '
        'constants independent of L; they are not decay of the reduced density or of any state (BB1/BB2), not a statement '
        'about untruncated creation coefficients, and the analyticity in the coupling is not extended to the reduced '
        'density (no zero-free region of the complexified normalization is proved).',
        'The coefficient Cauchy property gives whole-sequence convergence of coefficients per cutoff space only; '
        'whole_sequence_claimed and common_limit_claimed concern states and stay false; no uniqueness of any ground state '
        'is asserted.',
        'Thin headline margin: the bound headline K=49/111790368 is about 1.1407 below 1/2000000 (the freeze-time margin '
        'rule was checked against the forward preview only); the labelled refinements (reverse sharp exponent '
        '49/7154583552, reverse first-order cancellation 3773/1364628515625 which is quadratic in tau, forward loss-one '
        'F1-versus-F2 value 57270955/16662781836767232) are recorded and not bound.',
        'Exponent convention: the bound uses the contract form ceil(d/diam) (exponent N-1 at e_z for every comparison); the '
        'sharp count 1+ceil(d/diam) gives exponent N, but a floor constant written that way is linear in tau (ratio exactly '
        '100) and falls outside the prefrozen floor bracket, so every sharp form is labelled.',
        'General comparisons: the reverse compares any two volumes directly (constant K); telescoping at exponent N-1 would '
        'give 889/1006113312 and a two-step union 49/55895184, both above 1/2000000; the forward telescoped constant '
        '2734375/12204185915601 and its union constant are valid labelled values; the face sets are totally ordered '
        '(F1_N inside F2_N inside F1_(N+1)), so one nested comparison suffices for any pair of centered boxes.',
        'Contract wording read as follows: the source set of a nested comparison is the shell, and the literal set of sites '
        'met by the new terms adds the outer layer of Lambda_N (98, 218, 386 sites at N=2,3,4) at distance N-1 from e_z, '
        'which gives the same bound once the source loss is charged; the fixed-point map has Lipschitz constant '
        'J_0G\'(R) below 77/781250, while 2J_0G\'(R) is the AM2 exclusion constant; gate_fields_topic_specific is read as '
        'the 12 frozen gate fields; the floor difference weight is e^beta=w=390625/148.',
        'Inherited without re-proof: the AM2 multilinear majorant, fixed point, uniqueness in the ball and cutoff facts; '
        'the AV1 exact first-order coefficient and self-consistent remainder; the AY1 item-by-item F2 premises; the I1 '
        'dictionary; Banach, Weierstrass and the maximum principle are standard and not machine-checked.',
        'Independence is limited to routes, enumerations and code: the contract and selection note name both mechanisms, '
        'the skeptic triage proposed both routes and the frozen parameters, all agents are correlated model agents, and '
        'isolation is verified for repository inputs only.',
        'Upper bounds only; the -tau values replay the same |tau| formula; scientific priority is unverified.',
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('--output must be an absolute path')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('--output must be fresh (absent or empty)')
    if ROOT == out.resolve() or ROOT in out.resolve().parents:
        raise SystemExit('--output must lie outside the checkout')
    result = execute()
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checks': len(result['checks']), 'verdict': result['verdict'],
                      'bound_headline': result['previews']['bound_headline'], 'bound_floor': result['previews']['bound_floor']}))


if __name__ == '__main__':
    main()
