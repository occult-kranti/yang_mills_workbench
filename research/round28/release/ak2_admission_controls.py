"""AK2 exact coefficient, spectral-limit and unsupported-scope mutations."""
import argparse
import copy
from fractions import Fraction
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from reproduce import Validator,PREFIX,semantics,digest


def run(spec_name):
    validator=Validator();spec=validator.load(spec_name)
    records={side:validator.load(PREFIX+side+'/ak2/output/results.json') for side in ['forward','reverse']}
    settings=dict(spec['producers'])
    for label,path in [('independent',PREFIX+'skeptic/ak2-independent.json'),('clarification',PREFIX+'experts/newton/ak2-comparison-sources.json')]:
        records[label]=validator.load(path);settings[label]=next(e for e in spec['supplemental_evidence'] if e['path']==path)
    rejected=[]
    def attack(label,side,change,relations_only=False):
        result=copy.deepcopy(records[side]);configuration=copy.deepcopy(settings[side])
        if relations_only:configuration['semantic_controls']=[{'id':'schema-only','pointer':'/schema','equals':result['schema']}]
        semantics(result,configuration);change(result)
        try:semantics(result,configuration)
        except ValueError:rejected.append({'name':label,'relations_only':relations_only})
        else:raise ValueError('AK2 semantic mutation accepted: '+label)
    attack('missing-original-kinetic-link','forward',lambda r:r['geometry']['links'].pop(),True)
    attack('missing-boundary-endpoint','reverse',lambda r:r['geometry']['endpoint_actions'].pop(),True)
    attack('same-count-wrong-original-head','reverse',lambda r:r['geometry']['endpoint_actions'][0]['vertex'].__setitem__(0,99))
    attack('missing-21-face-whole-group','forward',lambda r:r['geometry']['cuboids'][1].__setitem__('retained_omitted_faces',147),True)
    attack('kinetic-gradient-factor-four','forward',lambda r:r['differential'].__setitem__('Gamma_W',str(4*Fraction(r['differential']['Gamma_W']))),True)
    attack('wrong-fundamental-Casimir','forward',lambda r:r['differential']['per_link'][0].__setitem__('Casimir_W',r['differential']['W']),True)
    attack('inverse-first-sign-hidden-by-square','reverse',lambda r:r['derivatives']['first_second_derivatives'][6].__setitem__('first',str(-Fraction(r['derivatives']['first_second_derivatives'][6]['first']))),True)
    attack('blind-square-channel-promoted','reverse',lambda r:r['derivatives']['inverse_sign_controls'][0].__setitem__('squared_comparison','discriminating'))
    attack('missing-double-commutator-half','forward',lambda r:r['physical_controls']['abstract_commutator'].__setitem__('moment','3/2'),True)
    attack('unsubtracted-ground-used-as-form-moment','forward',lambda r:r['physical_controls']['abstract_commutator'].__setitem__('moment','5/2'),True)
    attack('delta-energy-factor-omitted','reverse',lambda r:r['spectral_controls']['physical_scalar_fixture'].__setitem__('physical_excitation','2'),True)
    attack('hbar-frequency-factor-omitted','forward',lambda r:r['physical_controls']['units_fixture'].__setitem__('frequency','6'),True)
    attack('vacuum-plateau-in-centered-heat','reverse',lambda r:r['spectral_controls']['centering'].__setitem__('centered_heat_at_log2','65/256'),True)
    attack('stale-gap-used-as-implemented-energy','reverse',lambda r:r['spectral_controls']['centering'].__setitem__('first_moment','1/16'),True)
    attack('stale-label-recast-as-intentional-bound','clarification',lambda r:r['reverse_centering_metadata_clarification'].__setitem__('retrospective_intentional_lower_bound_claimed',True))
    attack('bounded-locality-fabricates-finite-energy','forward',lambda r:r['spectral']['bounded_operator_domain_counterexample'][2].__setitem__('form_moment_prefix_over_alpha','1/3'),True)
    attack('moment-loss-erased','reverse',lambda r:r['spectral_controls']['first_moment_loss_at_infinity'][0].__setitem__('first_moment','1/16'),True)
    attack('bounded-test-first-moment-equality-promoted','forward',lambda r:r['analytic_claims'].__setitem__('first_moment_equality_claimed',True))
    attack('common-space-strong-resolvent-invented','forward',lambda r:r['analytic_claims'].__setitem__('common_concrete_strong_resolvent_limit_claimed',True))
    attack('limiting-operator-domain-invented','reverse',lambda r:r['spectral_controls'].__setitem__('limiting_operator_domain_asserted',True))
    attack('second-moment-invented','forward',lambda r:r['analytic_claims'].__setitem__('second_moment_claimed',True))
    attack('closed-window-endpoint-dropped','independent',lambda r:r['controls']['closed_window_endpoint_control'].__setitem__('inclusive_mass',r['controls']['closed_window_endpoint_control']['incorrect_exclusive_mass']),True)
    attack('window-mass-without-tail-cost','forward',lambda r:r['spectral'].__setitem__('window_mass_lower','1/5'),True)
    attack('gap-only-countermodel-falsely-meets-moment','reverse',lambda r:r['spectral_controls']['gap_variance_without_moment'].__setitem__('first_moment_over_alpha','1'),True)
    attack('upper-rate-substituted-for-lower-rate','reverse',lambda r:r['spectral_controls'].__setitem__('lower_heat_rate_times_hbar_over_alpha','1/16'),True)
    attack('free-corner-promoted-to-interacting-observation','forward',lambda r:r['physical_controls']['free_corner'].__setitem__('scope','actual interacting state at all admitted coefficients'))
    attack('auxiliary-character-operator-identified-with-W','independent',lambda r:r['controls']['bounded_local_domain_control'].__setitem__('auxiliary_operator_is_original_W',True))
    attack('window-identified-as-actual-eigenatom','independent',lambda r:r['scope'].__setitem__('actual_spectral_eigenatom_or_lowest_overlap_claim',True))
    attack('symbolic-coupling-premise-dropped','reverse',lambda r:r['spectral_controls']['coupling_control'].__setitem__('cap_without_symbolic_condition_rejected',False))
    attack('additional-cap-premise-dropped','independent',lambda r:r['scope'].__setitem__('strict_unevaluated_tau_star_and_additional_cap',False))
    attack('positive-numerical-coupling-fabricated','forward',lambda r:r['spectral'].__setitem__('chosen_positive_admissible_tau','1/65536'))
    attack('imaginary-time-promoted-to-real-time-decay','independent',lambda r:r['scope'].__setitem__('real_time_decay_claim',True))
    attack('continuum-promotion','reverse',lambda r:r['scope'].__setitem__('continuum_claim',True))
    attack('eleventh-investigation-claimed','reverse',lambda r:r['scope'].__setitem__('eleventh_investigation_executed',True))
    return {'status':'passed','semantic_mutations_rejected':len(rejected),'controls':rejected,
            'specification_sha256':digest(validator.source(spec_name)),'new_research_loops':0,'producer_executions':0,
            'scope':'Hash-independent exact and scope projections; no new scientific execution or observed spectral data.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--spec',default=PREFIX+'advisor/ak2-admission.json');args=parser.parse_args()
    print(json.dumps(run(args.spec),sort_keys=True))
