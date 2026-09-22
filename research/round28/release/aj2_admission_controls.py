"""AJ2 geometry and forbidden inference mutations, independent of file hashes."""
import argparse
import copy
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reproduce import PREFIX, Validator, digest, semantics, require


def run(spec_name):
    validator = Validator()
    spec = validator.load(spec_name)
    require(spec.get('loop') == 'aj2', 'AJ2 admission specification required')
    original = {side: validator.load(PREFIX + f'{side}/aj2/output/results.json') for side in ['forward', 'reverse']}
    rejected = []
    def attack(label, side, change, relations_only=False):
        result = copy.deepcopy(original[side]); configuration = copy.deepcopy(spec['producers'][side])
        if relations_only:
            configuration['semantic_controls'] = [{'id': 'schema-only', 'pointer': '/schema', 'equals': result['schema']}]
        semantics(result, configuration); change(result)
        try:
            semantics(result, configuration)
        except ValueError:
            rejected.append({'name': label, 'relations_only': relations_only})
        else:
            raise ValueError('AJ2 semantic attack admitted: ' + label)
    attack('missing-complete-link', 'forward', lambda r: r['geometry']['owned_links'].pop(), True)
    attack('wrong-original-link-head', 'forward', lambda r: r['geometry']['owned_links'][0]['head'].__setitem__(0, 2), True)
    attack('reversed-face-orientation', 'reverse', lambda r: r['geometry']['face'][2].__setitem__('sign', 1), True)
    attack('missing-boundary-endpoint', 'reverse', lambda r: r['geometry']['endpoints'].pop(), True)
    attack('same-count-wrong-owner', 'reverse', lambda r: r['geometry']['face'][2]['owner'].__setitem__(2, 0))
    attack('Boolean-geometry-coordinate', 'forward', lambda r: r['geometry']['owned_links'][0]['tail'].__setitem__(0, False))
    attack('conditional-link-not-unit-Haar-coordinate', 'forward', lambda r: r['quaternion_and_haar_diagnostics']['conditional_coefficients'][0].__setitem__('numerator', 0), True)
    attack('missing-head-control-erased', 'reverse', lambda r: r['geometry']['quaternion_fixture'].__setitem__('missing_head_wilson', r['geometry']['quaternion_fixture']['wilson']), True)
    attack('nonconstant-step-falsely-forces-variance', 'forward', lambda r: r['controls']['nonconstant_step_multiplier'].__setitem__('variance', {'numerator': 1, 'denominator': 4}), True)
    attack('normal-band-no-concentration', 'reverse', lambda r: r['state_and_reference_controls']['epsilon_diagnostic_ceilings'][3].__setitem__('variance_ceiling', '1/4'), True)
    attack('Haar-value-substituted-for-actual-variance', 'reverse', lambda r: r['state_and_reference_controls'].__setitem__('actual_interacting_variance_value', '1/4'))
    attack('normality-promoted-to-faithfulness', 'forward', lambda r: r['scope'].__setitem__('normality_implies_faithfulness', True))
    attack('normal-band-identified-with-actual-ground', 'forward', lambda r: r['controls']['normal_concentration_bands'][0].__setitem__('actual_ground_state', True))
    attack('uncentered-vacuum-plateau-omitted', 'reverse', lambda r: r['spectral_and_domain_controls'].__setitem__('uncentered_correlation', r['spectral_and_domain_controls']['centered_correlation']), True)
    attack('upper-bound-turned-into-lower-bound', 'forward', lambda r: r['controls']['spectral_point_measure_controls'][0].__setitem__('heat_at_s_log2', {'numerator': 1, 'denominator': 2}), True)
    attack('spectral-energy-relabelled', 'forward', lambda r: r['controls']['spectral_point_measure_controls'][0].__setitem__('energy_in_units_Delta', 3), True)
    attack('threshold-atom-invented', 'reverse', lambda r: r['spectral_and_domain_controls'].__setitem__('threshold_atom_mass_in_countermodel', '1/4'), True)
    attack('real-time-decay-invented', 'reverse', lambda r: r['spectral_and_domain_controls'].__setitem__('real_time_amplitude_at_phase_pi_over_2', ['0', '0']), True)
    attack('form-moment-divergence-erased', 'reverse', lambda r: r['spectral_and_domain_controls']['domain_countermodel_partials'][3].__setitem__('first_energy_moment_in_g', '1'), True)
    attack('actual-energy-moment-invented', 'reverse', lambda r: r['spectral_and_domain_controls'].__setitem__('actual_first_moment_proved', True))
    attack('uniform-positive-variance-invented', 'forward', lambda r: r['scope'].__setitem__('uniform_positive_variance_margin', True))
    attack('numerical-stability-regime-invented', 'reverse', lambda r: r['scope'].__setitem__('evaluated_stability_interval', True))
    attack('lower-decay-claim-invented', 'forward', lambda r: r['scope'].__setitem__('lower_decay_bound_claimed', True))
    attack('continuum-gap-invented', 'reverse', lambda r: r['scope'].__setitem__('continuum_mass_gap_solution', True))
    return {'status': 'passed', 'semantic_mutations_rejected': len(rejected), 'controls': rejected,
            'specification_sha256': digest(validator.source(spec_name)), 'new_research_loops': 0,
            'scope': 'Hash-independent geometry/arithmetic and unsupported inference controls, not new scientific executions.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--spec', default=PREFIX+'advisor/aj2-admission.json'); args=parser.parse_args()
    print(json.dumps(run(args.spec), sort_keys=True))
