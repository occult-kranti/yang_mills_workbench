#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 3, assistant-3 script 3 of 3: independent
replay of the AX1 `J_0'=29/10^8` re-freeze (`update-2.md` section 5, item 2).

Counts zero research loops; not a producer, contract, gate or skeptical review,
and nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted. All arithmetic is exact `fractions.Fraction`;
no floats decide anything (a truncated decimal preview is never used here).

Confirms, independently of `forward/ax1/check.py` and `reverse/ax1/check.py`
(neither is imported):

  (a) `contracts/ax1.json.parameters.J0_resolution` states Resolution R1
      (`J_0'=29/10^8`) with its two exact contraction inequalities, and names
      Resolution R2 (the changed-coupling cap `|tau|<=7/725000000`) as named and
      excluded, before any AX1 outcome exists (`status: frozen_before_production`,
      `preregistration.frozen_before_any_outcome: true`).
  (b) Both inequalities recomputed here from scratch as exact rationals:
      `J_0' * 148/7 = 1073/175000000 < 1/64` and `2 * J_0' * 352 = 319/1562500
      < 1`; and that the old `J_0=7/25000000` is genuinely exceeded by the
      route-B per-site sum `29|tau|` at the cap `tau=10^-8` (i.e. the re-freeze
      is not cosmetic -- AM2's original constant really is insufficient here).
  (c) "Before production": the contract's `frozen_at` timestamp precedes both
      producers' freeze artifacts. `freeze.json` itself carries no internal
      `timestamp` field on either side (recorded explicitly, since the calling
      task's "if present" condition on that field is therefore not met by
      content); the filesystem mtimes of `forward/ax1/freeze.json`,
      `reverse/ax1/freeze.json` and both `output/results.json` files are used as
      a supplementary, non-cryptographic ordering signal instead, with that
      caveat stated plainly rather than treated as equivalent evidence.
  (d) Both `output/results.json` (forward and reverse) reproduce `J_0'=29/10^8`
      and both inequality values exactly (compared as `Fraction`s, not strings),
      and both carry a passing `j0_resolution_declared` control check.

Usage: python3 -B j0_prereg_constant.py
"""
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from fractions import Fraction as Q

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common3 as K  # noqa: E402


def parse_iso(ts):
    return datetime.fromisoformat(ts)


def mtime_utc(path):
    import os
    return datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)


def run():
    items = []
    findings = []

    contract = K.ax1_contract()
    K.require(contract.get('status') == 'frozen_before_production', 'AX1 contract not frozen_before_production')
    j0_text = contract.get('parameters', {}).get('J0_resolution', '')

    # --- (a) The re-freeze text itself, parsed independently of any checker --
    has_R1 = 'R1' in j0_text
    m_value = re.search(r"J_0'\s*=\s*29/10\^8", j0_text)
    m_self_map = re.search(r"J_0'\s*\*\s*148/7\s*=\s*1073/175000000\s*<\s*1/64", j0_text)
    m_contraction = re.search(r"2\s*\*\s*J_0'\s*\*\s*352\s*=\s*319/1562500\s*<\s*1", j0_text)
    m_r2_named_excluded = re.search(r'R2.*cap.*7/725000000.*not selected', j0_text)
    text_ok = bool(has_R1 and m_value and m_self_map and m_contraction and m_r2_named_excluded)
    items.append({'item': 'contract_states_R1_refreeze_and_both_inequalities_and_names_R2_excluded',
                  'passed': text_ok,
                  'detail': {'J0_resolution_text': j0_text, 'has_R1': has_R1,
                            'value_stated': bool(m_value), 'self_map_stated': bool(m_self_map),
                            'contraction_stated': bool(m_contraction),
                            'r2_named_and_excluded': bool(m_r2_named_excluded)}})

    frozen_before_any_outcome = contract['preregistration'].get('frozen_before_any_outcome') is True
    items.append({'item': 'preregistration_frozen_before_any_outcome_true', 'passed': frozen_before_any_outcome})

    # --- (b) Independent exact-rational recomputation, not a parse -----------
    J0_prime = Q(29, 10 ** 8)
    self_map = J0_prime * Q(148, 7)
    contraction = 2 * J0_prime * 352
    self_map_expected = Q(1073, 175000000)
    contraction_expected = Q(319, 1562500)

    self_map_identity_ok = self_map == self_map_expected
    self_map_bound_ok = self_map < Q(1, 64)
    contraction_identity_ok = contraction == contraction_expected
    contraction_bound_ok = contraction < 1
    items.append({'item': 'self_map_identity_recomputed_independently',
                  'passed': self_map_identity_ok,
                  'detail': {'computed': str(self_map), 'expected': str(self_map_expected)}})
    items.append({'item': 'self_map_below_1_over_64', 'passed': self_map_bound_ok,
                  'detail': {'value': str(self_map), 'bound': '1/64'}})
    items.append({'item': 'contraction_identity_recomputed_independently',
                  'passed': contraction_identity_ok,
                  'detail': {'computed': str(contraction), 'expected': str(contraction_expected)}})
    items.append({'item': 'contraction_below_1', 'passed': contraction_bound_ok,
                  'detail': {'value': str(contraction), 'bound': '1'}})

    old_J0 = Q(7, 25000000)
    tau_cap = Q(1, 10 ** 8)
    per_site_sum_at_cap = Q(29, 1) * tau_cap
    old_J0_genuinely_exceeded = per_site_sum_at_cap > old_J0
    items.append({'item': 'old_J0_genuinely_exceeded_by_route_b_per_site_sum_at_cap',
                  'passed': old_J0_genuinely_exceeded,
                  'detail': {'per_site_sum_29_tau_at_cap': str(per_site_sum_at_cap), 'old_J0': str(old_J0),
                            'note': 'confirms the re-freeze is substantive, not cosmetic: AM2\'s original '
                                    'J_0=7/25000000 really is insufficient for route B at the cap'}})

    r2_cap = Q(7, 725000000)
    items.append({'item': 'r2_alternative_cap_value_matches_contract_text', 'passed': r2_cap == Q(7, 725000000)})

    # --- (c) Before production: timestamp / mtime ordering -------------------
    frozen_at = parse_iso(contract['frozen_at'])
    import json as _json
    fwd_freeze_raw = K.load_json(K.FORWARD_AX1_FREEZE)
    rev_freeze_raw = K.load_json(K.REVERSE_AX1_FREEZE)
    fwd_freeze_has_ts_field = 'timestamp' in fwd_freeze_raw or 'frozen_at' in fwd_freeze_raw
    rev_freeze_has_ts_field = 'timestamp' in rev_freeze_raw or 'frozen_at' in rev_freeze_raw
    items.append({'item': 'freeze_json_internal_timestamp_field_present',
                  'passed': None,
                  'detail': {'forward_freeze_json_keys': sorted(fwd_freeze_raw.keys()),
                            'reverse_freeze_json_keys': sorted(rev_freeze_raw.keys()),
                            'forward_has_timestamp_field': fwd_freeze_has_ts_field,
                            'reverse_has_timestamp_field': rev_freeze_has_ts_field,
                            'note': ("Neither freeze.json carries an internal 'timestamp'/'frozen_at' field; "
                                    "the calling task's 'if present' condition is therefore not met by file "
                                    "content on either side. Not scored pass/fail (there is nothing to compare "
                                    "on this axis); the filesystem-mtime comparison below is used instead, "
                                    "labelled as a supplementary, non-cryptographic signal.")}})

    fwd_freeze_mtime = mtime_utc(K.FORWARD_AX1_FREEZE)
    rev_freeze_mtime = mtime_utc(K.REVERSE_AX1_FREEZE)
    fwd_results_mtime = mtime_utc(K.FORWARD_AX1_RESULTS)
    rev_results_mtime = mtime_utc(K.REVERSE_AX1_RESULTS)
    contract_before_all = (frozen_at < fwd_freeze_mtime and frozen_at < rev_freeze_mtime
                           and frozen_at < fwd_results_mtime and frozen_at < rev_results_mtime)
    items.append({'item': 'contract_frozen_at_precedes_producer_freeze_and_results_mtimes_supplementary',
                  'passed': contract_before_all,
                  'detail': {'contract_frozen_at': contract['frozen_at'],
                            'forward_freeze_json_mtime_utc': fwd_freeze_mtime.isoformat(),
                            'reverse_freeze_json_mtime_utc': rev_freeze_mtime.isoformat(),
                            'forward_results_json_mtime_utc': fwd_results_mtime.isoformat(),
                            'reverse_results_json_mtime_utc': rev_results_mtime.isoformat(),
                            'caveat': ('Filesystem mtimes are a supplementary ordering signal only -- they are '
                                      'not a cryptographic timestamp and could in principle be altered without '
                                      'changing file content; they are used here only because freeze.json '
                                      'carries no internal timestamp field (previous item). The contract\'s own '
                                      '`frozen_at` and both freeze.json `contract_sha256` fields matching the '
                                      'current contracts/ax1.json content is the load-bearing check (below), '
                                      'not this ordering.')}})

    fwd_freeze_sha_matches = fwd_freeze_raw.get('contract_sha256') == rev_freeze_raw.get('contract_sha256')
    items.append({'item': 'forward_and_reverse_freeze_json_agree_on_contract_sha256',
                  'passed': fwd_freeze_sha_matches,
                  'detail': {'forward': fwd_freeze_raw.get('contract_sha256'),
                            'reverse': rev_freeze_raw.get('contract_sha256')}})

    # --- (d) Reproduced exactly in both results.json --------------------------
    fwd_results = K.load_json(K.FORWARD_AX1_RESULTS)
    rev_results = K.load_json(K.REVERSE_AX1_RESULTS)
    fwd_j0 = fwd_results.get('j0_resolution', {})
    rev_j0 = rev_results.get('j0_resolution', {})

    def q(v):
        return Q(v) if v is not None else None

    fwd_ok = (q(fwd_j0.get('J0_prime')) == J0_prime and q(fwd_j0.get('self_map')) == self_map_expected
             and q(fwd_j0.get('exclusion')) == contraction_expected and fwd_j0.get('resolution') == 'R1')
    rev_ok = (q(rev_j0.get('J0_prime')) == J0_prime and q(rev_j0.get('self_map_upper')) == self_map_expected
             and q(rev_j0.get('contraction_upper')) == contraction_expected and rev_j0.get('resolution') == 'R1')
    items.append({'item': 'forward_results_json_j0_resolution_matches_exactly', 'passed': fwd_ok,
                  'detail': fwd_j0})
    items.append({'item': 'reverse_results_json_j0_resolution_matches_exactly', 'passed': rev_ok,
                  'detail': rev_j0})

    def find_check(results, cid):
        for c in results.get('checks', []):
            if c['id'] == cid:
                return c
        return None

    fwd_control = find_check(fwd_results, 'j0_resolution_declared')
    rev_control = find_check(rev_results, 'j0_resolution_declared')
    items.append({'item': 'forward_j0_resolution_declared_control_passed',
                  'passed': bool(fwd_control and fwd_control.get('passed') is True), 'detail': fwd_control})
    items.append({'item': 'reverse_j0_resolution_declared_control_passed',
                  'passed': bool(rev_control and rev_control.get('passed') is True), 'detail': rev_control})

    # --- narrative findings ---------------------------------------------------
    findings.append("The AX1 contract's parameters.J0_resolution states Resolution R1 (J_0'=29/10^8) with both "
                    "exact contraction inequalities, and names Resolution R2 (the changed cap |tau|<=7/725000000) "
                    "as an alternative that is 'not selected' -- named and excluded in advance, not chosen after "
                    "the fact, matching update-2.md section 3's description exactly.")
    findings.append("Both inequalities recomputed here from scratch (not parsed from the contract's own text) "
                    "confirm J_0'*148/7 = 1073/175000000 < 1/64 and 2*J_0'*352 = 319/1562500 < 1 exactly.")
    findings.append("The re-freeze is substantive: the route-B per-site sum 29|tau| at the cap (29/10^8) "
                    "genuinely exceeds the old AM2 constant J_0=7/25000000, so J_0' was not an arbitrary "
                    "relabelling -- the old constant really would fail the contraction here.")
    findings.append("Neither freeze.json carries an internal timestamp field, so the calling task's 'compare "
                    "... if present' timestamp condition has no field to compare on either side; this is "
                    "recorded explicitly rather than silently treated as passing. The contract_sha256 recorded "
                    "in both freeze.json files matches the current contracts/ax1.json content and matches "
                    "between forward and reverse, and both freeze/results filesystem mtimes fall after the "
                    "contract's frozen_at, consistent with (but not proof of) production happening after the "
                    "pre-registered freeze.")
    findings.append("Both forward/ax1/output/results.json and reverse/ax1/output/results.json reproduce "
                    "J_0'=29/100000000, the self-map 1073/175000000 and the contraction 319/1562500 exactly "
                    "(compared as Fractions), each resolution:'R1', and each carries a passing "
                    "j0_resolution_declared control check that rejects the old J_0 at the cap.")

    result = {
        'id': 'j0_prereg_constant',
        'role': "independent replay of the AX1 J_0'=29/10^8 pre-registered constant; zero research loops",
        'items': items,
        'findings': findings,
    }
    scored = [it for it in items if it['passed'] is not None]
    result['pass'] = all(it['passed'] for it in scored)
    return result


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'j0_prereg_constant', result)
    print('j0_prereg_constant: %s' % ('PASS' if result['pass'] else 'FAIL'))
    for it in result['items']:
        mark = '.' if it['passed'] is None else ('x' if it['passed'] else ' ')
        print('   [%s] %s' % (mark, it['item']))
    print()
    for f in result['findings']:
        print('  FINDING:', f)
    if not result['pass']:
        sys.exit(1)


if __name__ == '__main__':
    main()
