#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 2, assistant-2 script 1 of 3: replay the
AW1-gate -> AW2-contract -> AW2-check.py coupling-rule derivation chain.

Pre-registration test only (`update-1.md` section 5, item 1; the calling task).
Counts zero research loops; not a producer, contract, gate or skeptical review, and
nothing here is read back into any of those. Human project author: Hruday N M
(BUNZEEY); AI-assisted.

What this replays, independently (no import of `forward/aw2/check.py` or any other
producer/skeptic module -- every parse and every arithmetic step below is written
fresh from the frozen `advisor/aw1-gate.json` and `contracts/aw1.json` texts):

  1. Read K_2^+ from the AW1 gate's `decision` text (cross-checked against its
     `accepted` text), and the AW1 cap from the same `accepted` text.
  2. Read the frozen decade-grid rule from `contracts/aw1.json.parameters.
     aw2_coupling_rule` ("... never chosen after K_2 is seen"): grid start, bound
     (1/288).
  3. Apply the rule: walk the decade grid {10^-8, 10^-9, ...} and stop at the first
     tau with K_2^+ * tau <= bound.
  4. Compare the result with (a) `contracts/aw2.json.parameters.tau_AW2`'s stated
     value and (b) `forward/aw2/output/results.json`'s recorded `tau_AW2`. All three
     must agree exactly, as `Fraction`s.
  5. Grep `forward/aw2/check.py`'s source text for the literal string
     `1/100000000` (AW2's tau at the cap, i.e. 10^-8) used as an input, with an
     explanation of every raw substring hit (a false-positive collision inside the
     unrelated literal `1/1000000000` = 10^-9 does occur once, and is explained,
     not silently dropped); likewise for `Q(1, 10 ** 8)` occurrences, each
     classified by its surrounding statement.
  6. A self-contained rejection test: a hard-coded-literal derivation of tau_AW2 is
     rejected by a locally-defined provenance check, the same discipline the
     producer's own `validate_coupling` implements (mirrored here, not imported).

Usage: python3 -B coupling_rule_chain.py
"""
import re
import sys
from fractions import Fraction as Q
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common2 as K  # noqa: E402


# ---------------------------------------------------------------------------
# 1. AW1 gate: K_2^+, the cap, and the gate's own claimed rule outcome (parsed
#    for cross-reference only; not trusted in place of the independent replay).
# ---------------------------------------------------------------------------
def parse_aw1_gate():
    gate = K.load_json(K.AW1_GATE)
    K.require(gate.get('loop') == 'AW1' and gate.get('verdict') == 'accepted_within_scope', 'AW1 gate identity')
    acc, dcs = gate['accepted'], gate['decision']

    m = K.match(r'Bind K_2\^\+ = (\d+)/(\d+) \(about ([0-9.]+); the largest of the three valid exact-tier upper '
                r'bounds, outward ceiling (\d+)/10\^(\d+)\) as the admitted constant for AW2', dcs,
                'gate decision K_2^+')
    K2_decision = Q(int(m.group(1)), int(m.group(2)))

    m2 = K.match(r'the bound value is K_2\^\+=(\d+)/(\d+) \(~([0-9.]+), outward (\d+)/10\^(\d+);', acc,
                 'gate accepted K_2^+')
    K2_accepted = Q(int(m2.group(1)), int(m2.group(2)))
    K.require(K2_decision == K2_accepted, "gate's decision and accepted K_2^+ texts disagree")

    m3 = K.match(r'at both signs of tau with \|tau\|<=10\^-(\d+):', acc, 'gate cap')
    cap = Q(1, 10 ** int(m3.group(1)))

    m4 = K.match(r'\(5\) K_2\^\+ tau<=1/(\d+) at tau=10\^-(\d+), so the frozen decade-grid rule gives '
                 r'tau_AW2=10\^-(\d+) \(the cap\) with sign margin 1/\((\d+) K_2\^\+ tau\)~([0-9.]+)', acc,
                 'gate item 5')
    gate_bound = Q(1, int(m4.group(1)))
    gate_tau_from_item5 = Q(1, 10 ** int(m4.group(3)))

    m5 = K.match(r'The frozen AW2 coupling rule gives tau_AW2 = 10\^-(\d+) with sign margin about (\d+)\.', dcs,
                 'gate decision rule sentence')
    gate_tau_from_decision = Q(1, 10 ** int(m5.group(1)))

    return {'K2': K2_decision, 'cap': cap, 'gate_bound': gate_bound,
            'gate_tau_item5': gate_tau_from_item5, 'gate_tau_decision': gate_tau_from_decision,
            'raw_decision': dcs, 'raw_accepted': acc}


# ---------------------------------------------------------------------------
# 2-3. AW1 contract's frozen rule text, and applying it (own decade-grid search,
#    not the producer's `aw2_rule`).
# ---------------------------------------------------------------------------
def parse_aw1_rule():
    c = K.aw1_contract()
    rule_text = c['parameters']['aw2_coupling_rule']
    m = K.match(r'^tau_AW2 = the largest element of the decade grid \{10\^-(\d+), 10\^-(\d+), \.\.\.\} with '
                r'K_2\^\+ \* tau <= (\d+)/(\d+) \(half the first-order coefficient\), K_2\^\+ the admitted '
                r'exact-tier remainder constant; frozen here, never chosen after K_2 is seen$', rule_text,
                'AW1 frozen decade-grid rule')
    start = int(m.group(1))
    K.require(int(m.group(2)) == start + 1, 'decade grid step is not one decade')
    bound = Q(int(m.group(3)), int(m.group(4)))
    tau_cap = K.rat(c['parameters']['tau_cap'])
    K.require(Q(1, 10 ** start) == tau_cap, 'rule grid does not start at the AW1 cap')
    return {'text': rule_text, 'start': start, 'bound': bound, 'tau_cap': tau_cap}


def decade_search(K2, bound, start, max_steps=60):
    """Independent re-implementation of the decade-grid rule: the largest
    tau=10^-k, k>=start, with K2*tau<=bound."""
    k = start
    trail = []
    while True:
        tau = Q(1, 10 ** k)
        lhs = K2 * tau
        ok = lhs <= bound
        trail.append({'k': k, 'tau': tau, 'K2_times_tau': lhs, 'satisfied': ok})
        if ok:
            return tau, trail
        k += 1
        K.require(k <= start + max_steps, 'decade grid exhausted without satisfying the bound')


# ---------------------------------------------------------------------------
# 4. AW2 contract text and AW2 forward results.json: must agree with the replay.
# ---------------------------------------------------------------------------
def parse_aw2_contract_tau():
    c = K.aw2_contract()
    text = c['parameters']['tau_AW2']
    m = K.match(r'^(\d+)/(\d+) \(from the AW1 rule: largest decade-grid coupling with K_2\^\+ tau <= (\d+)/(\d+), '
                r'evaluated inside check\.py from the AW1 gate snapshot\)$', text, 'AW2 contract tau_AW2 text')
    tau = Q(int(m.group(1)), int(m.group(2)))
    bound = Q(int(m.group(3)), int(m.group(4)))
    rule_ref = c['preregistration']['tau']['rule_if_chosen_later']
    K.require(rule_ref == ('AW1 decade-grid rule, frozen in contracts/aw1.json and evaluated in check.py '
                            'from advisor/aw1-gate.json'),
              "AW2 contract's rule_if_chosen_later is not the frozen formula reference (must not be null or a "
              "bare number)")
    K.require(K.rat(c['preregistration']['tau']['value']) == tau, 'AW2 preregistration.tau.value disagrees')
    return {'tau': tau, 'bound': bound, 'raw_text': text, 'rule_reference': rule_ref}


def parse_aw2_results_tau():
    r = K.load_json(K.FORWARD_AW2_RESULTS)
    headline_tau = K.rat(r['headline']['tau_AW2'])
    tau_plus = K.rat(r['tau_values']['+'])
    tau_minus = K.rat(r['tau_values']['-'])
    K.require(tau_plus == headline_tau and tau_minus == -headline_tau, 'results.json tau_values disagree with headline')
    K2_results = K.rat(r['headline']['K_2_plus'])
    return {'tau': headline_tau, 'K2': K2_results, 'raw_headline': r['headline']}


# ---------------------------------------------------------------------------
# 5. Grep AW2's check.py for a hard-coded '1/100000000' (or 10**8) used as input.
# ---------------------------------------------------------------------------
def scan_check_py_for_literal_tau():
    text = K.load_text(K.FORWARD_AW2_CHECK)
    lines = text.split('\n')

    def line_of(pos):
        return text.count('\n', 0, pos) + 1

    def line_text(n):
        return lines[n - 1].strip()

    # (a) the exact literal string, digit-bounded so '1/1000000000' (10^-9) cannot
    #     satisfy it merely because it contains '100000000' as a sub-run of zeros.
    standalone = [line_of(m.start()) for m in re.finditer(r'(?<!\d)1/100000000(?!\d)', text)]

    # (b) every raw occurrence of the substring '1/100000000', for transparency,
    #     classified as 'standalone' or 'inside-a-longer-literal' by inspecting the
    #     character immediately after the match.
    raw_hits = []
    for m in re.finditer(re.escape('1/100000000'), text):
        end = m.end()
        collided = end < len(text) and text[end].isdigit()
        raw_hits.append({'line': line_of(m.start()), 'text': line_text(line_of(m.start())),
                          'classification': 'inside_longer_literal_collision' if collided else 'standalone'})

    # (c) Q(1, 10 ** 8) / Q(1,10**8) style constructions, digit-bounded on the 8.
    pow8_hits = []
    for m in re.finditer(r'Q\(\s*1\s*,\s*10\s*\*\*\s*8\s*\)', text):
        n = line_of(m.start())
        txt = line_text(n)
        if 'rejected(' in txt or "'literal" in txt:
            cls = 'inside_a_rejected_damaging_mutation_test'
        elif 'abs(' in txt or '< Q(1, 10 ** 8)' in txt or 'tolerance' in txt.lower():
            cls = 'decimal_tolerance_bound_not_tau'
        else:
            cls = 'UNCLASSIFIED_NEEDS_REVIEW'
        pow8_hits.append({'line': n, 'text': txt, 'classification': cls})

    # (d) the only assignment of the `tau_aw2` variable must come from calling the
    #     rule function, never a literal.
    assignments = []
    for i, ln in enumerate(lines, start=1):
        if re.search(r'^\s*tau_aw2\s*(?:,\s*[A-Za-z_]\w*\s*)?=(?!=)', ln):
            assignments.append({'line': i, 'text': ln.strip()})

    return {'standalone_literal_lines': standalone,
            'raw_substring_hits': raw_hits,
            'pow8_hits': pow8_hits,
            'tau_aw2_assignments': assignments}


# ---------------------------------------------------------------------------
# 6. Self-contained rejection test: a locally-defined provenance check (mirroring,
#    not importing, the producer's own `validate_coupling`) rejects a hard-coded
#    literal even when it is numerically the right answer, and rejects a coupling
#    that fails the rule bound; it accepts only the rule-derived value tied to the
#    gate-bound K_2^+.
# ---------------------------------------------------------------------------
def provenance_checked_tau(value, provenance, K2, bound):
    K.require(provenance == 'aw1_rule_evaluated_from_gate',
              'literal or non-rule coupling rejected: provenance=' + repr(provenance))
    K.require(K2 * value <= bound, 'coupling fails the rule bound K_2^+ * tau <= bound')
    return value


def run():
    items = []

    gate = parse_aw1_gate()
    items.append({'item': 'aw1_gate_K2_and_cap_parsed',
                  'passed': True,
                  'detail': {'K_2_plus': K.s(gate['K2']), 'cap': K.s(gate['cap']),
                             'gate_tau_item5': K.s(gate['gate_tau_item5']),
                             'gate_tau_decision_sentence': K.s(gate['gate_tau_decision'])}})

    rule = parse_aw1_rule()
    items.append({'item': 'aw1_contract_rule_parsed_as_formula_not_number',
                  'passed': rule['start'] == 8 and rule['bound'] == Q(1, 288) and rule['tau_cap'] == gate['cap'],
                  'detail': {'grid_start_10^-k': rule['start'], 'bound': K.s(rule['bound']),
                             'rule_text': rule['text']}})

    computed_tau, trail = decade_search(gate['K2'], rule['bound'], rule['start'])
    items.append({'item': 'decade_rule_independently_applied',
                  'passed': computed_tau == gate['cap'] == gate['gate_tau_item5'] == gate['gate_tau_decision'],
                  'detail': {'computed_tau_AW2': K.s(computed_tau),
                             'trail': [{'k': t['k'], 'tau': K.s(t['tau']), 'K2_times_tau': K.s(t['K2_times_tau']),
                                        'satisfied': t['satisfied']} for t in trail]}})

    aw2c = parse_aw2_contract_tau()
    items.append({'item': 'aw2_contract_tau_matches_replay',
                  'passed': aw2c['tau'] == computed_tau and aw2c['bound'] == rule['bound'],
                  'detail': {'contract_tau_AW2': K.s(aw2c['tau']), 'contract_text': aw2c['raw_text'],
                             'rule_reference_is_a_formula_not_null_or_number': aw2c['rule_reference']}})

    aw2r = parse_aw2_results_tau()
    items.append({'item': 'aw2_results_json_tau_matches_replay',
                  'passed': aw2r['tau'] == computed_tau and aw2r['K2'] == gate['K2'],
                  'detail': {'results_tau_AW2': K.s(aw2r['tau']), 'results_K_2_plus': K.s(aw2r['K2'])}})

    scan = scan_check_py_for_literal_tau()
    zero_standalone = len(scan['standalone_literal_lines']) == 0
    single_assignment = (len(scan['tau_aw2_assignments']) == 1
                         and 'aw2_rule(' in scan['tau_aw2_assignments'][0]['text'])
    pow8_all_classified = all(h['classification'] != 'UNCLASSIFIED_NEEDS_REVIEW' for h in scan['pow8_hits'])
    items.append({'item': 'aw2_check_py_contains_no_literal_1_over_100000000_used_as_input',
                  'passed': zero_standalone and single_assignment and pow8_all_classified,
                  'detail': {
                      'standalone_literal_1_over_100000000_occurrences': len(scan['standalone_literal_lines']),
                      'raw_substring_hits_explained': scan['raw_substring_hits'],
                      'q_1_10_pow_8_hits_explained': scan['pow8_hits'],
                      'tau_aw2_assignment_sites': scan['tau_aw2_assignments'],
                      'explanation': (
                          "grep for the literal string '1/100000000' (digit-bounded) finds zero standalone "
                          "occurrences in forward/aw2/check.py. A raw, non-bounded substring search does find one "
                          "hit, but it lies inside the unrelated literal '1/1000000000' (=10^-9, 9 zeros, used in "
                          "an unrelated mutation-fixture tuple), which contains '100000000' (8 zeros) only as a "
                          "coincidental digit-run collision; the digit-bounded regex correctly excludes it. Two "
                          "occurrences of 'Q(1, 10 ** 8)' exist: one is a decimal-string tolerance bound in a "
                          "cross-check (never assigned to tau_aw2), and the other is the literal value fed, with "
                          "provenance='literal', into a call wrapped in rejected(...) -- i.e. check.py's own "
                          "validate_coupling is required to raise AdmissionError for exactly this hard-coded "
                          "literal, which it does; a second, similar rejected(...) call even feeds the contract's "
                          "own displayed tau text with provenance='contract_parameter_text' and requires that "
                          "rejected too. The sole assignment of the tau_aw2 variable in the file is "
                          "'tau_aw2, steps = aw2_rule(K, R)' (K read from the hash-verified AW1 gate, R from the "
                          "hash-verified AW1 contract rule), never a literal.")}})

    # Self-contained rejection test (update-1.md sec.5 item 1: "rejecting any
    # mutation that hard-codes tau_AW2 instead of deriving it").
    accepted_val = provenance_checked_tau(computed_tau, 'aw1_rule_evaluated_from_gate', gate['K2'], rule['bound'])
    rej1 = K.expect_rejected(provenance_checked_tau, Q(1, 10 ** 8), 'literal_hardcode', gate['K2'], rule['bound'])
    rej2 = K.expect_rejected(provenance_checked_tau, Q(1, 10 ** 8), 'contract_parameter_text', gate['K2'],
                              rule['bound'])
    # A coupling that is correctly-provenanced but violates the rule bound must
    # also be rejected (guards the second half of the provenance check): tau=10^-5
    # gives K_2^+ * tau ~ 0.0335 > bound (1/288 ~ 0.00347).
    rej3 = K.expect_rejected(provenance_checked_tau, Q(1, 10 ** 5), 'aw1_rule_evaluated_from_gate', gate['K2'],
                              rule['bound'])
    items.append({'item': 'self_contained_hardcode_rejection_test',
                  'passed': accepted_val == computed_tau,
                  'detail': {'accepted_rule_derived_value': K.s(accepted_val),
                             'rejected_literal_hardcode': rej1,
                             'rejected_contract_text_as_coupling': rej2,
                             'rejected_off_rule_coupling': rej3}})

    # Bonus robustness note (not a hard pass/fail condition; the gate's crude-tier
    # K_2 is quoted only as an approximate decimal '~7.9375e6' in `accepted`, so this
    # is a preview, matching the skeptic's own remark that the crude rule "would give
    # 10^-10, information only"): confirms the decade search is sensitive to K, i.e.
    # AW2's tau is not a constant independent of K_2^+.
    m = re.search(r'The crude tier \(t_c=(\d+)\|tau\|, K_2~([0-9.]+)e(\d+), margin ([0-9.]+)\) fails at the cap',
                  gate['raw_accepted'])
    crude_note = None
    if m:
        # A decimal preview parsed to a Fraction only for this illustrative, non-admission note.
        crude_K2_preview = Q(m.group(2).replace('.', '')) * Q(10, 1) ** (int(m.group(3)) - len(m.group(2).split('.')[1]))
        crude_tau, crude_trail = decade_search(crude_K2_preview, rule['bound'], rule['start'])
        crude_note = {'crude_K2_preview_decimal': m.group(2) + 'e' + m.group(3),
                      'crude_tau_from_same_rule': K.s(crude_tau),
                      'differs_from_exact_tier_tau': crude_tau != computed_tau,
                      'note': 'preview only; illustrates the rule genuinely depends on K_2^+ (a larger K gives a '
                              'smaller tau), consistent with the skeptic\'s remark that the crude rule would give '
                              '10^-10'}

    result = {
        'id': 'coupling_rule_chain',
        'role': 'pre-registration test; zero research loops; replays AW1-gate -> AW2-contract -> AW2-check.py',
        'inputs': ['research/round32/advisor/aw1-gate.json', 'research/round32/contracts/aw1.json',
                   'research/round32/contracts/aw2.json', 'research/round32/forward/aw2/check.py',
                   'research/round32/forward/aw2/output/results.json'],
        'items': items,
        'crude_tier_robustness_preview': crude_note,
    }
    result['pass'] = all(it['passed'] for it in items)
    return result


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'coupling_rule_chain', result)
    print('coupling_rule_chain: %s' % ('PASS' if result['pass'] else 'FAIL'))
    for it in result['items']:
        print('   [%s] %s' % ('x' if it['passed'] else ' ', it['item']))
    if not result['pass']:
        sys.exit(1)


if __name__ == '__main__':
    main()
