#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 sub-round 2, assistant-2 script 2 of 4: template-span
and gate-field audit (calling task item 2).

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not import
`forward/*/check.py`, `reverse/*/check.py`, or any other producer/skeptic module.

BB1 and BB2 have no advisor gate yet (`research/round33/advisor/bb1-gate.json`
and `bb2-gate.json` do not exist at the time this package was written), so
"exported gate fields" here means each producer's own `output/results.json`
`gate_fields`-family blocks, not a gate's -- there is no gate to read.

Two sub-checks:

  1. `mandatory_template_span_check` (rule R7) -- for each of the four packets
     (forward/bb1, reverse/bb1, forward/bb2, reverse/bb2), the contract's
     `preregistration.mandatory_sentence_template` appears, after whitespace
     normalization, as EXACTLY ONE unbroken span inside that packet's own
     `report.md` (0 occurrences and 2-or-more occurrences are both defects, not
     only 0). Cross-checked, where present, against the producer's own
     self-reported `mandatory_sentence_verbatim_once` / occurrence-count check
     in `output/results.json`, without trusting it.

  2. `gate_fields_comparison` -- compares every exported gate field against the
     contract's `preregistration.gate_fields_required`. BB1 has no discharge
     complexity: both producers' single `gate_fields` block is compared directly
     against the contract and must match exactly (key set and every value).
     BB2 has the discharge structure the calling task names explicitly:
       - reverse's TOP-LEVEL `gate_fields` is the BEFORE-discharge block (every
         BB1-dependent field false, `dynamics_level` at the BA2 algebraic
         level) -- compared against the contract for key-set completeness only
         (it is *expected* to differ in value from `gate_fields_required`,
         which holds only `accepted_within_scope` after the discharge); its
         `gate_fields_after_discharge` block is the one that must equal the
         contract's `gate_fields_required` exactly.
       - forward's TOP-LEVEL `gate_fields` (== its `gate_fields_proposed`) is
         the proposed, already-discharged-shape values and must equal the
         contract's `gate_fields_required` exactly; its
         `gate_fields_if_undischarged` block is the before-discharge shape,
         compared for key-set completeness only, exactly as reverse's top-level
         block is.
     A cross-producer check also compares forward's `gate_fields_if_undischarged`
     against reverse's top-level (before-discharge) `gate_fields`: both express
     "the state before the BB1 gate discharges anything" and are expected to
     agree field for field; any difference is tabulated (not scored as a defect
     by itself, since the calling task asks to "tabulate the differences", not
     to adjudicate which producer is right -- that is the skeptic's job at the
     discharge).

Usage: python3 -B template_and_fields.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common2 as K  # noqa: E402


def normalize(text):
    return K.normalize(text)


# ---------------------------------------------------------------------------
# 1. Rule R7: mandatory_sentence_template as exactly one unbroken span in
#    report.md, for each of the four packets.
# ---------------------------------------------------------------------------
def mandatory_template_span_check():
    per_packet = {}
    for loop in K.LOOPS:
        L = loop.upper()
        contract = K.load_contract(loop)
        template = contract['preregistration']['mandatory_sentence_template']
        norm_template = normalize(template)
        for side, path in (('forward', K.FORWARD_REPORT_PATHS[loop]), ('reverse', K.REVERSE_REPORT_PATHS[loop])):
            report_text = normalize(K.load_text(path))
            occurrences = report_text.count(norm_template)
            self_reported = None
            results_path = K.FORWARD_RESULTS_PATHS[loop] if side == 'forward' else K.REVERSE_RESULTS_PATHS[loop]
            data = K.load_json(results_path)
            # Look specifically for the producer's own self-reported occurrence-count check, without trusting it.
            for json_path, obj in K.dicts_with_key(data, 'id'):
                if isinstance(obj, dict) and obj.get('id') == 'mandatory_sentence_verbatim_once':
                    self_reported = {'occurrences_in_report': obj.get('occurrences_in_report'), 'passed': obj.get('passed')}
            key_name = '%s_%s' % (L, side)
            per_packet[key_name] = {
                'template_len': len(template), 'occurrences_in_report': occurrences,
                'self_reported_by_producer': self_reported, 'passed': occurrences == 1,
            }
    passed = all(v['passed'] for v in per_packet.values())
    findings = []
    for key_name, v in per_packet.items():
        tag = 'PASS' if v['passed'] else 'DEFECT'
        findings.append('%s: mandatory_sentence_template (%d chars) occurs %d time(s) as one unbroken normalized '
                        'span in report.md (self-reported by the producer: %r) -- %s'
                        % (key_name, v['template_len'], v['occurrences_in_report'], v['self_reported_by_producer'], tag))
    return {'id': 'mandatory_template_span_check', 'per_packet': per_packet, 'passed': passed, 'findings': findings}


# ---------------------------------------------------------------------------
# 2. Gate-field comparison, respecting BB2's before/after-discharge blocks.
# ---------------------------------------------------------------------------
def diff_dicts(a, b):
    """Returns (only_in_a, only_in_b, value_mismatches) for two flat dicts."""
    only_in_a = sorted(set(a) - set(b))
    only_in_b = sorted(set(b) - set(a))
    mismatches = {k: {'a': a[k], 'b': b[k]} for k in a if k in b and a[k] != b[k]}
    return only_in_a, only_in_b, mismatches


def gate_fields_comparison():
    per_loop = {}
    findings = []

    # --- BB1: no discharge complexity. ---
    loop = 'bb1'
    L = 'BB1'
    contract = K.load_contract(loop)
    gfr = contract['preregistration']['gate_fields_required']
    fwd = K.load_json(K.FORWARD_RESULTS_PATHS[loop])
    rev = K.load_json(K.REVERSE_RESULTS_PATHS[loop])
    fwd_gf = fwd.get('gate_fields', {})
    rev_gf = rev.get('gate_fields', {})
    rows = {}
    for side, gf in (('forward', fwd_gf), ('reverse', rev_gf)):
        only_c, only_g, mism = diff_dicts(gfr, gf)
        rows[side] = {'only_in_contract': only_c, 'only_in_producer': only_g, 'value_mismatches': mism,
                      'passed': not only_c and not only_g and not mism}
    fwd_rev_only_a, fwd_rev_only_b, fwd_rev_mism = diff_dicts(fwd_gf, rev_gf)
    rows['forward_vs_reverse'] = {'only_in_forward': fwd_rev_only_a, 'only_in_reverse': fwd_rev_only_b,
                                  'value_mismatches': fwd_rev_mism, 'passed': not fwd_rev_only_a and not fwd_rev_only_b and not fwd_rev_mism}
    per_loop[L] = {'rows': rows, 'passed': all(r['passed'] for r in rows.values())}
    for side in ('forward', 'reverse'):
        r = rows[side]
        tag = 'PASS' if r['passed'] else 'DEFECT'
        findings.append('BB1 %s: gate_fields (no discharge for BB1) vs contract.gate_fields_required -- %s (%d keys); '
                        'missing=%r extra=%r mismatches=%r' % (side, tag, len(gfr), r['only_in_contract'], r['only_in_producer'], r['value_mismatches']))
    tag = 'PASS' if rows['forward_vs_reverse']['passed'] else 'DEFECT'
    findings.append('BB1 forward.gate_fields vs reverse.gate_fields -- %s; only_in_forward=%r only_in_reverse=%r '
                    'mismatches=%r' % (tag, rows['forward_vs_reverse']['only_in_forward'], rows['forward_vs_reverse']['only_in_reverse'], rows['forward_vs_reverse']['value_mismatches']))

    # --- BB2: before/after-discharge blocks. ---
    loop = 'bb2'
    L = 'BB2'
    contract = K.load_contract(loop)
    gfr = contract['preregistration']['gate_fields_required']
    fwd = K.load_json(K.FORWARD_RESULTS_PATHS[loop])
    rev = K.load_json(K.REVERSE_RESULTS_PATHS[loop])

    fwd_proposed = fwd.get('gate_fields_proposed') or fwd.get('gate_fields', {})
    fwd_top = fwd.get('gate_fields', {})
    fwd_undischarged = fwd.get('gate_fields_if_undischarged', {})
    rev_top_before = rev.get('gate_fields', {})
    rev_after = rev.get('gate_fields_after_discharge', {})

    rows2 = {}

    # forward top-level == forward gate_fields_proposed (should be identical by construction).
    a, b, m = diff_dicts(fwd_top, fwd_proposed)
    rows2['forward_top_equals_proposed'] = {'only_in_top': a, 'only_in_proposed': b, 'mismatches': m, 'passed': not a and not b and not m}

    # forward's "proposed" (== top-level) must equal the contract's gate_fields_required exactly (after-discharge shape).
    only_c, only_g, mism = diff_dicts(gfr, fwd_proposed)
    rows2['forward_proposed_vs_contract'] = {'only_in_contract': only_c, 'only_in_producer': only_g, 'value_mismatches': mism,
                                             'passed': not only_c and not only_g and not mism}

    # reverse's gate_fields_after_discharge must equal the contract's gate_fields_required exactly.
    only_c, only_g, mism = diff_dicts(gfr, rev_after)
    rows2['reverse_after_discharge_vs_contract'] = {'only_in_contract': only_c, 'only_in_producer': only_g, 'value_mismatches': mism,
                                                    'passed': not only_c and not only_g and not mism}

    # forward's proposed vs reverse's after-discharge: both are the "should hold once BB1 is admitted" state.
    a, b, m = diff_dicts(fwd_proposed, rev_after)
    rows2['forward_proposed_vs_reverse_after_discharge'] = {'only_in_forward': a, 'only_in_reverse': b, 'mismatches': m, 'passed': not a and not b and not m}

    # before/if-undischarged blocks: key-set completeness against the contract (values are EXPECTED to differ --
    # this is the whole point of the block -- so only key-set completeness is scored as pass/fail; value
    # differences from the contract are informational, not defects).
    for name, block in (('forward_if_undischarged_keys', fwd_undischarged), ('reverse_before_discharge_keys', rev_top_before)):
        only_c, only_g, _ = diff_dicts(gfr, block)
        rows2[name] = {'only_in_contract': only_c, 'only_in_producer': only_g, 'passed': not only_c and not only_g}

    # The cross-producer check the calling task cares about: forward's "if undischarged" state should agree with
    # reverse's top-level "before discharge" state field for field, since both express the same semantic state
    # from the two different producers' own export conventions.
    a, b, m = diff_dicts(fwd_undischarged, rev_top_before)
    rows2['forward_if_undischarged_vs_reverse_before_discharge'] = {
        'only_in_forward': a, 'only_in_reverse': b, 'value_mismatches': m, 'passed': not a and not b and not m,
    }

    per_loop[L] = {'rows': rows2, 'passed': all(r['passed'] for r in rows2.values())}

    findings.append('BB2 forward.gate_fields == forward.gate_fields_proposed: %s' % rows2['forward_top_equals_proposed']['passed'])
    r = rows2['forward_proposed_vs_contract']
    findings.append('BB2 forward.gate_fields_proposed (after-discharge shape) vs contract.gate_fields_required -- %s; '
                    'missing=%r extra=%r mismatches=%r' % ('PASS' if r['passed'] else 'DEFECT', r['only_in_contract'], r['only_in_producer'], r['value_mismatches']))
    r = rows2['reverse_after_discharge_vs_contract']
    findings.append('BB2 reverse.gate_fields_after_discharge vs contract.gate_fields_required -- %s; missing=%r '
                    'extra=%r mismatches=%r' % ('PASS' if r['passed'] else 'DEFECT', r['only_in_contract'], r['only_in_producer'], r['value_mismatches']))
    r = rows2['forward_proposed_vs_reverse_after_discharge']
    findings.append('BB2 forward.gate_fields_proposed vs reverse.gate_fields_after_discharge (both the '
                    '"once-discharged" state) -- %s; only_in_forward=%r only_in_reverse=%r mismatches=%r'
                    % ('PASS' if r['passed'] else 'DEFECT', r['only_in_forward'], r['only_in_reverse'], r['mismatches']))
    for name in ('forward_if_undischarged_keys', 'reverse_before_discharge_keys'):
        r = rows2[name]
        findings.append('BB2 %s: key set vs contract.gate_fields_required -- %s (value differences from the '
                        'contract are expected here and not scored; the whole point of this block is that they '
                        'differ before the BB1 discharge); missing=%r extra=%r'
                        % (name, 'PASS' if r['passed'] else 'DEFECT (missing/extra key)', r['only_in_contract'], r['only_in_producer']))
    r = rows2['forward_if_undischarged_vs_reverse_before_discharge']
    tag = 'PASS (agree field for field)' if r['passed'] else 'DIFFERENCE (tabulated, not a decision -- see calling task item 2)'
    findings.append('BB2 forward.gate_fields_if_undischarged vs reverse.gate_fields (top-level, before discharge) '
                    '-- both express "state before the BB1 gate discharges anything" -- %s; only_in_forward=%r '
                    'only_in_reverse=%r value_mismatches=%r' % (tag, r['only_in_forward'], r['only_in_reverse'], r['value_mismatches']))
    if r['value_mismatches']:
        for k, vv in r['value_mismatches'].items():
            findings.append('  DIFFERENCE: %s -- forward.gate_fields_if_undischarged.%s=%r vs reverse.gate_fields.%s=%r'
                            % (k, k, vv['a'], k, vv['b']))

    passed = per_loop['BB1']['passed'] and (
        rows2['forward_top_equals_proposed']['passed'] and rows2['forward_proposed_vs_contract']['passed']
        and rows2['reverse_after_discharge_vs_contract']['passed']
        and rows2['forward_proposed_vs_reverse_after_discharge']['passed']
        and rows2['forward_if_undischarged_keys']['passed'] and rows2['reverse_before_discharge_keys']['passed']
        # forward_if_undischarged_vs_reverse_before_discharge is a tabulated difference, not gated on here (see
        # calling task item 2: "tabulate the differences", not "reject the difference").
    )
    return {'id': 'gate_fields_comparison', 'per_loop': per_loop, 'passed': passed, 'findings': findings}


def run():
    checks = [mandatory_template_span_check(), gate_fields_comparison()]
    return {
        'id': 'template_and_fields',
        'role': 'Jung/Pauli lens, Round33 sub-round 2, assistant-2: template-span (R7) and gate-field-comparison '
                'audit (including BB2\'s before/after-discharge blocks), calling task item 2; zero research loops; '
                'audits only, never admission evidence',
        'checks': {c['id']: c for c in checks},
        'passed': all(c['passed'] for c in checks),
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'template_and_fields', result)
    print('template_and_fields: %s' % ('PASS (no defects)' if result['passed'] else 'FAIL (see findings)'))
    for check_id, c in result['checks'].items():
        print('  %s: %s' % (check_id, 'PASS' if c['passed'] else 'FAIL'))
        for f in c['findings']:
            print('    -', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
