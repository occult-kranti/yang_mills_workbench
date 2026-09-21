"""Read-only admission of reviewed Round23 evidence; never create expectations here."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[2]
LOOPS = tuple(a+b for a in 'stuvw' for b in '12')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def strict_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: '+key)
        result[key] = value
    return result


def read(path):
    return json.loads(path.read_text(), object_pairs_hook=strict_pairs)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def unlinked(path):
    for part in (path, *path.parents):
        require(not part.is_symlink(), 'symlink path component: '+str(part))
    return path


def relative(name):
    require(type(name) is str and bool(name), 'invalid file name')
    p = Path(name)
    require(not p.is_absolute() and '..' not in p.parts and '\\' not in name
            and str(p) == name, 'noncanonical file name: '+name)
    require('__pycache__' not in p.parts and p.suffix not in ('.pyc', '.pyo'),
            'nonportable interpreter cache')
    return p


def source(name):
    p = unlinked(ROOT / relative(name))
    require(p.is_file(), 'missing scientific source: '+name)
    return p


def check_hashes(files):
    require(type(files) is dict and bool(files), 'empty source inventory')
    for name, expected in files.items():
        require(type(expected) is str and re.fullmatch('[0-9a-f]{64}', expected),
                'invalid digest: '+name)
        require(digest(source(name)) == expected, 'changed scientific source: '+name)


def payload(result, loop, direction, expected):
    require(type(result) is dict, 'result must be an object')
    require(result.get('loop') == loop and result.get('direction') == direction,
            'wrong result identity')
    require(type(result.get('status')) is str, 'status must be text')
    if 'passed' in result:
        require(type(result['passed']) is bool and result['passed'], 'passed must be true Boolean')
    require(type(expected) is dict and bool(expected), 'no reviewed semantic expectations')
    # Expectations follow the disclosed review mode, including explicit solo review.
    # Match exact JSON types as well as values: true must never stand for one.
    for key, value in expected.items():
        require(key in result and type(result[key]) is type(value)
                and json.dumps(result[key], sort_keys=True) == json.dumps(value, sort_keys=True),
                'reviewed semantic field differs: '+direction+'/'+key)


def gate(loop):
    require(loop in LOOPS, 'unknown Round23 loop')
    prefix = 'research/round23/'
    g = read(source(prefix+'advisor/'+loop+'-gate.json'))
    require(g.get('schema') == 'ym23-gate-v1' and g.get('loop') == loop, 'wrong gate identity')
    require(g.get('status') in ('accepted', 'limited', 'rejected'), 'loop has no reviewed verdict')
    for key in ('claim', 'scope', 'target_verdict', 'next_missing_premise'):
        require(type(g.get(key)) is str and bool(g[key]), 'missing '+key)
    require(type(g.get('equations')) is list, 'equations must be a list')
    files = g.get('files')
    check_hashes(files)
    contract = read(source(prefix+'contracts/'+loop+'.json'))
    require(contract.get('loop') == loop and contract.get('status') == 'frozen', 'contract not frozen')
    instructions = contract.get('instruction_inputs')
    require(type(instructions) is list and bool(instructions)
            and all(type(name) is str for name in instructions), 'instruction snapshot set missing')
    require(len(set(instructions)) == len(instructions), 'duplicate instruction snapshots')
    required = {prefix+'contracts/'+loop+'.json', prefix+'advisor/'+loop+'-decision.md',
                prefix+'skeptic/'+loop+'.md', prefix+'methods/team-protocol.md'}
    required.update(instructions)
    required.update(contract['dependencies'])
    for direction in ('forward', 'reverse'):
        base = prefix+direction+'/'+loop+'/'
        required.update(base+x for x in ('report.md', 'check.py', 'output/results.json',
                                         'output/controls.json', 'output/source-manifest.json'))
        manifest = read(source(base+'output/source-manifest.json'))
        inputs, outputs = manifest.get('inputs'), manifest.get('outputs')
        require(type(inputs) is dict and type(outputs) is dict, 'missing producer closure')
        require({base+'report.md', base+'check.py', prefix+'contracts/'+loop+'.json',
                 prefix+'methods/team-protocol.md'} <= inputs.keys(), 'incomplete required inputs')
        require(set(instructions) <= inputs.keys(), 'missing contract-declared instruction input')
        require({'results.json', 'controls.json'} <= outputs.keys(), 'incomplete required outputs')
        for name, expected in inputs.items():
            require(name in files and files[name] == expected, 'unbound producer source: '+name)
        for name, expected in outputs.items():
            relative(name)
            full = base+'output/'+name
            require(full in files and files[full] == expected, 'unbound producer output: '+full)
        result = read(source(base+'output/results.json'))
        payload(result, loop, direction, g['expected_results'][direction])
        controls = read(source(base+'output/controls.json'))
        require(type(controls) is dict and controls.get('loop') == loop
                and controls.get('direction') == direction, 'wrong controls identity')
        require(controls.get('passed') is True, 'controls must explicitly pass')
        def control_flags(value):
            if type(value) is dict:
                for key, child in value.items():
                    if key == 'passed':
                        require(child is True, 'control passed flag must be true Boolean')
                    else:
                        control_flags(child)
            elif type(value) is list:
                for child in value:
                    control_flags(child)
        control_flags(controls)
        if loop in ('u1', 'u2'):
            require(result.get('execution_mode') == 'single-agent-correlated-formulations'
                    and result.get('independent_agent_review') is False
                    and controls.get('independent_agent_review') is False,
                    'U evidence must disclose correlated single-agent execution')
            required_controls = {
                'u1': {'forward': ('all_links_free','unique_face_parity','haar_normalization',
                        'wrong_normalized_trace_rejected','missing_face_changes_coefficient',
                        'identity_zero_variance','compression_autonomy_not_assumed'),
                       'reverse': ('moment_contraction','rank_operator_cubic_identity',
                        'wrong_normalized_trace_rejected','vacuum_mean_not_vacuum_annihilation',
                        'missing_face_changes_coefficient','compression_autonomy_not_assumed',
                        'fixed_clock_checked','identity_zero_variance')},
                'u2': {'forward': ('connected_word_identity','support_growth_required',
                        'profile_uniform_bound','exact_positive_margin','state_square_root_enclosures',
                        'finite_q_positive','outside_series_disk_rejected','large_window_certificate_only',
                        'no_two_state_autonomy','first_order_bound_to_u1'),
                       'reverse': ('all_order_domination_argument','exact_positive_margin',
                        'complete_factor_incidence','single_link_budget_rejected',
                        'support_growth_required','first_order_bound_to_u1','state_error_retained',
                        'no_two_state_autonomy','magnitude_lower_bound_not_upper_failure',
                        'large_window_certificate_only')}}
            require(all(controls.get(k) is True for k in required_controls[loop][direction]),
                    'missing or unsuccessful U discriminating control')
            require(result.get('endpoint_proved') is (loop == 'u2')
                    and result.get('continuum_proved') is False, 'U claim scope drift')
        if loop == 't2':
            amendment = prefix+'methods/t2-solo-override.md'
            require(amendment in inputs and amendment in files, 'missing T2 solo amendment')
            require(result.get('execution_mode') == 'single-agent-correlated-formulations'
                    and result.get('independent_agent_review') is False,
                    'T2 must disclose single-agent execution')
            require(controls.get('independent_agent_review') is False,
                    'T2 controls must disclose single-agent execution')
            required_controls = {
                'forward': ('different_grounds_enclosed', 'different_ground_weights_enclosed',
                    'lambda_zero_exact', 'time_zero_identity', 'infinity_projection_checked',
                    'partial_shift_rejected', 'common_shift_preserved', 'clock_mismatch_rejected'),
                'reverse': ('whole_interval_margin_proved', 'ground_ground_cancellation_checked',
                    'common_ground_assumption_rejected', 'missing_centering_rejected',
                    'missing_initial_projection_rejected', 'missing_leakage_budget_rejected',
                    'relative_ratio_inference_rejected', 'spectral_derivative_identities_checked')}
            require(all(controls.get(k) is True for k in required_controls[direction]),
                    'missing or unsuccessful T2 discriminating control')
    require(required <= files.keys(), 'incomplete required gate inventory')
    check_hashes(contract['dependencies'])
    require(type(g.get('independence')) is dict, 'missing independence disclosure')
    if loop in ('t2', 'u1', 'u2'):
        require(g['independence'].get('independent_agents') is False
                and g['independence'].get('mode') == 'single-agent-correlated-formulations',
                'solo gate cannot claim independent agents')
    return g
