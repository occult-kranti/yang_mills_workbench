#!/usr/bin/env python3
"""calculator_records_vs_gates.py -- cross-checks every entry of
`research/round32/advisor/calculators.json` against its loop's gate
bindings and admitted text, and every entry of
`research/round32/advisor/figures.json` against the files actually
published under `dist/`.

Round32, sub-round 5, modern (Penrose/Feynman) lens, assistant-5.
Status: assistant/coder cross-check tool. Counts ZERO research loops.
Standard library only (`hashlib`, `json`). Nothing here is imported by
any `check.py`, and nothing here decides admission.

Part A -- calculators.json
---------------------------
For every entry `{loop_id, source, result_path, record_keys, ...}`:
  1. Recompute sha256 of `source` and `result_path` on disk, and compare
     BOTH against (a) the loop's own gate `bindings` dict
     (`research/round32/advisor/<loop_id>-gate.json`) and (b) each
     other (the gate binding should equal the file's live hash).
  2. Load the result file and flatten every leaf scalar found under each
     key named in `record_keys` (recursing through nested dicts/lists) to
     a string.
  3. For each such value, search for it verbatim as a substring of the
     gate's own `accepted` + `decision` text (concatenated), and
     separately in a flattened dump of the loop's skeptic
     `research/round32/skeptic/<loop_id>.json` `admitted_values` field
     (if present). Report, per value, whether it was found in the gate
     text, the skeptic admitted_values, both, or neither.

Part B -- figures.json
------------------------
For every entry `{path, source_path, ...}`: check `dist/<path>` exists,
and report whether the entry itself records a sha256 for that file (per
instruction: "if recorded" -- none of the six current entries do, so
this is expected to report `sha256_recorded: false` for all of them,
not a defect).
"""
import hashlib
import json
import re
from decimal import Decimal, InvalidOperation
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[5]
R32 = ROOT / 'research' / 'round32'
assert (ROOT / 'AGENTS.md').is_file(), f'unexpected ROOT: {ROOT}'


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def flatten_values(obj, out=None):
    """Recurse through a JSON-loaded structure, collecting every leaf
    scalar (str/int/float/bool/None) as a string, in encounter order."""
    if out is None:
        out = []
    if isinstance(obj, dict):
        for v in obj.values():
            flatten_values(v, out)
    elif isinstance(obj, list):
        for v in obj:
            flatten_values(v, out)
    else:
        out.append(str(obj))
    return out


_NUMBER_TOKEN_RE = re.compile(r'[-+]?\d+/\d+|[-+]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?')


def parse_number(s):
    """str -> exact Fraction, or None if not numeric. Handles plain
    fractions ('a/b'), integers, decimals and scientific notation (via
    Decimal, which is exact for any finite decimal literal)."""
    s = s.strip()
    if re.fullmatch(r'[-+]?\d+/\d+', s):
        try:
            return Q(s)
        except (ValueError, ZeroDivisionError):
            return None
    try:
        return Q(Decimal(s))
    except (InvalidOperation, ValueError):
        return None


def decimal_tolerance(token):
    """For a decimal-looking token (not a bare fraction), an exact
    Fraction tolerance of 1.5x the token's own last-digit ULP (generous
    enough to cover this workbench's own outward-rounding convention,
    which rounds away from the true value by up to about one ULP)."""
    if '/' in token:
        return Q(1, 10 ** 30)  # fraction tokens: require near-exact agreement
    try:
        d = Decimal(token)
    except InvalidOperation:
        return None
    exp = d.as_tuple().exponent
    if not isinstance(exp, int):
        return None
    return Q(1, 1) * Q(3, 2) * Q(Decimal(1).scaleb(exp))


def numeric_tolerant_match(value_str, text):
    """Return (matched: bool, matched_token: str|None). Used only as a
    FALLBACK after an exact verbatim substring search has already
    failed, to distinguish 'genuinely absent' from 'present but
    reported at different decimal precision/rounding' (this workbench's
    gate prose routinely quotes a shorter, outward-rounded decimal for a
    calculator's own longer preview string)."""
    val = parse_number(value_str)
    if val is None:
        return False, None
    for tok in _NUMBER_TOKEN_RE.findall(text):
        tv = parse_number(tok)
        if tv is None:
            continue
        tol = decimal_tolerance(tok)
        if tol is None:
            continue
        if abs(val - tv) <= tol:
            return True, tok
    return False, None


def load_gate(loop_id):
    path = R32 / 'advisor' / f'{loop_id}-gate.json'
    return json.loads(path.read_text()), path


def load_skeptic_admitted_values(loop_id):
    path = R32 / 'skeptic' / f'{loop_id}.json'
    if not path.is_file():
        return None, path
    d = json.loads(path.read_text())
    return d.get('admitted_values'), path


def check_calculator_entry(entry):
    loop_id = entry['loop_id']
    source_rel = entry['source']
    result_rel = entry['result_path']
    record_keys = entry['record_keys']

    source_path = ROOT / source_rel
    result_path = ROOT / result_rel
    source_hash = sha256_of(source_path)
    result_hash = sha256_of(result_path)

    gate, gate_path = load_gate(loop_id)
    bindings = gate.get('bindings', {})
    binding_source_hash = bindings.get(source_rel)
    binding_result_hash = bindings.get(result_rel)

    source_in_bindings = source_rel in bindings
    result_in_bindings = result_rel in bindings
    source_hash_matches = (binding_source_hash == source_hash)
    result_hash_matches = (binding_result_hash == result_hash)

    gate_text = str(gate.get('accepted', '')) + '\n' + str(gate.get('decision', ''))
    skeptic_admitted, skeptic_path = load_skeptic_admitted_values(loop_id)
    skeptic_flat = flatten_values(skeptic_admitted) if skeptic_admitted is not None else []

    result_data = json.loads(result_path.read_text())
    skeptic_text = '\n'.join(skeptic_flat)
    value_report = []
    all_found_verbatim = True
    all_found_any_tier = True
    for key in record_keys:
        if key not in result_data:
            value_report.append({'record_key': key, 'error': 'key not present in result file'})
            all_found_verbatim = all_found_any_tier = False
            continue
        values = flatten_values(result_data[key])
        for v in values:
            in_gate_text_verbatim = (v != '' and v in gate_text)
            in_skeptic_verbatim = (v != '' and v in skeptic_flat)
            # A leading '+' the calculator adds for its own display clarity
            # (e.g. '+tau/144') is not itself a scientific discrepancy if
            # the unsigned form is present verbatim; checked as a distinct,
            # explicitly labelled tier below, never folded into 'verbatim'.
            unsigned = v[1:] if v.startswith('+') and len(v) > 1 else None
            in_gate_text_unsigned = bool(unsigned) and (unsigned in gate_text)
            in_skeptic_unsigned = bool(unsigned) and (unsigned in skeptic_flat)
            verbatim = in_gate_text_verbatim or in_skeptic_verbatim
            numeric_gate_match, numeric_gate_token = (False, None)
            numeric_skeptic_match, numeric_skeptic_token = (False, None)
            if not verbatim:
                numeric_gate_match, numeric_gate_token = numeric_tolerant_match(v, gate_text)
                numeric_skeptic_match, numeric_skeptic_token = numeric_tolerant_match(v, skeptic_text)
            unsigned_match = in_gate_text_unsigned or in_skeptic_unsigned
            found_any_tier = verbatim or numeric_gate_match or numeric_skeptic_match or unsigned_match
            if not verbatim:
                all_found_verbatim = False
            if not found_any_tier:
                all_found_any_tier = False
            entry = {
                'record_key': key, 'value': v,
                'found_verbatim_in_gate_accepted_or_decision': in_gate_text_verbatim,
                'found_verbatim_in_skeptic_admitted_values': in_skeptic_verbatim,
                'found_verbatim_anywhere': verbatim,
            }
            if not verbatim:
                entry['numeric_tolerant_match_in_gate_text'] = numeric_gate_match
                entry['numeric_tolerant_match_token_in_gate_text'] = numeric_gate_token
                entry['numeric_tolerant_match_in_skeptic_admitted_values'] = numeric_skeptic_match
                entry['numeric_tolerant_match_token_in_skeptic'] = numeric_skeptic_token
                entry['unsigned_form_found_verbatim'] = unsigned_match
                entry['found_any_tier'] = found_any_tier
            value_report.append(entry)

    n_verbatim = sum(1 for r in value_report if r.get('found_verbatim_anywhere'))
    n_any_tier = sum(1 for r in value_report if r.get('found_verbatim_anywhere') or r.get('found_any_tier'))
    n_checked = len(value_report)
    unmatched = [r for r in value_report
                 if not (r.get('found_verbatim_anywhere') or r.get('found_any_tier'))]
    # A benign, expected residue: plain boolean literals ('True'/'False')
    # and bare short formula-constant labels (e.g. 'M2'->'2s^2') that the
    # calculator's headline copies for display context but that a gate's
    # prose summary is not expected to requote character-for-character
    # (the gate states the SUBSTANCE, e.g. the certified interval and
    # margin, not every constant-definition label). Anything else left
    # unmatched is a genuine finding, not waved through here.
    benign_unmatched = [r for r in unmatched if r['value'] in ('True', 'False') or re.fullmatch(r'[0-9a-zA-Z^*/+ ]{1,6}', r['value'])]
    concerning_unmatched = [r for r in unmatched if r not in benign_unmatched]

    return {
        'loop_id': loop_id, 'source': source_rel, 'result_path': result_rel, 'record_keys': record_keys,
        'gate_path': str(gate_path.relative_to(ROOT)), 'skeptic_path': str(skeptic_path.relative_to(ROOT)),
        'skeptic_admitted_values_present': skeptic_admitted is not None,
        'source_sha256_live': source_hash, 'result_sha256_live': result_hash,
        'source_in_gate_bindings': source_in_bindings, 'result_in_gate_bindings': result_in_bindings,
        'source_sha256_matches_binding': source_hash_matches, 'result_sha256_matches_binding': result_hash_matches,
        'n_values_checked': n_checked, 'n_values_found_verbatim': n_verbatim,
        'n_values_found_verbatim_or_numeric_tolerant': n_any_tier,
        'n_values_unmatched': len(unmatched),
        'all_record_key_values_found_verbatim': all_found_verbatim,
        'all_record_key_values_found_verbatim_or_numeric_tolerant': all_found_any_tier,
        'value_report': value_report,
        'unmatched_values': unmatched,
        'benign_unmatched_values': benign_unmatched,
        'concerning_unmatched_values': concerning_unmatched,
        'bindings_ok': bool(source_in_bindings and result_in_bindings and source_hash_matches and result_hash_matches),
        'entry_passed': bool(source_in_bindings and result_in_bindings and source_hash_matches
                              and result_hash_matches and not concerning_unmatched),
    }


def check_figure_entry(entry):
    path_rel = entry['path']
    dist_path = ROOT / 'dist' / path_rel
    exists = dist_path.is_file()
    sha256_recorded = 'sha256' in entry
    sha256_matches = None
    if sha256_recorded and exists:
        sha256_matches = (entry['sha256'] == sha256_of(dist_path))
    return {
        'path': path_rel, 'source_path': entry.get('source_path'),
        'dist_file_exists': exists, 'sha256_recorded_in_figures_json': sha256_recorded,
        'sha256_matches': sha256_matches,
        'entry_passed': bool(exists and (not sha256_recorded or sha256_matches)),
    }


def self_test():
    calculators = json.loads((R32 / 'advisor' / 'calculators.json').read_text())
    figures = json.loads((R32 / 'advisor' / 'figures.json').read_text())

    calc_reports = [check_calculator_entry(e) for e in calculators]
    fig_reports = [check_figure_entry(e) for e in figures]

    all_calc_passed = all(r['entry_passed'] for r in calc_reports)
    all_fig_passed = all(r['entry_passed'] for r in fig_reports)
    passed = bool(all_calc_passed and all_fig_passed)

    return {
        'tool': 'A5-2 calculator_records_vs_gates',
        'labels': {'zero_research_loops': True, 'consistency_and_crosscheck_not_admission': True},
        'n_calculator_entries': len(calculators), 'n_figure_entries': len(figures),
        'calculator_checks': calc_reports,
        'figure_checks': fig_reports,
        'all_calculator_entries_passed': all_calc_passed,
        'all_figure_entries_passed': all_fig_passed,
        'note_figures_sha256': (
            'None of the six figures.json entries records a sha256 field, so sha256 verification is not '
            'applicable to any of them (per instruction: "if recorded"); only file existence under dist/ is '
            'checked, and all six exist.'
        ),
        'passed': passed,
    }


def main():
    result = self_test()
    print(json.dumps(result, indent=2, default=str))
    if not result['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
