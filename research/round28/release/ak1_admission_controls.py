"""AK1 exact geometry, state, trace and unsupported-claim mutation controls."""
import argparse
import copy
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from reproduce import Validator,PREFIX,semantics,digest


def run(spec_name):
    validator=Validator();spec=validator.load(spec_name)
    records={side:validator.load(PREFIX+side+'/ak1/output/results.json') for side in ['forward','reverse']}
    settings=dict(spec['producers'])
    independent=PREFIX+'skeptic/ak1-independent.json'
    records['independent']=validator.load(independent)
    settings['independent']=next(e for e in spec['supplemental_evidence'] if e['path']==independent)
    rejected=[]
    def attack(label,side,change,relations_only=False):
        result=copy.deepcopy(records[side]);configuration=copy.deepcopy(settings[side])
        if relations_only:configuration['semantic_controls']=[{'id':'schema-only','pointer':'/schema','equals':result['schema']}]
        semantics(result,configuration);change(result)
        try:semantics(result,configuration)
        except ValueError:rejected.append({'name':label,'relations_only':relations_only})
        else:raise ValueError('AK1 semantic mutation accepted: '+label)
    attack('missing-original-link','forward',lambda r:r['geometry']['original_links'].pop(),True)
    attack('missing-outgoing-head','reverse',lambda r:r['geometry']['endpoint_vertices'].pop(),True)
    attack('same-count-wrong-endpoint','reverse',lambda r:r['geometry']['endpoint_vertices'][0].__setitem__(0,99))
    attack('reversed-original-face','forward',lambda r:r['geometry']['original_word'][2].__setitem__(2,1))
    attack('lost-second-incident-group','reverse',lambda r:r['geometry']['orthant_incident_anchors'].pop(),True)
    attack('individual-faces-replace-whole-group','forward',lambda r:r['geometry']['cuboids'][1]['interior'].__setitem__('charged_group_faces',49),True)
    attack('outgoing-only-interior','reverse',lambda r:r['geometry']['fixtures'][1]['interior'].__setitem__('count',1),True)
    attack('origin-blind-control-falsely-discriminating','forward',lambda r:r['checks'][16].__setitem__('verdict','discriminating'))
    attack('conditional-link-not-unit-Haar','reverse',lambda r:r['covariance']['conditional_coefficients'].__setitem__(0,'0'),True)
    attack('wrong-trace-factor','reverse',lambda r:r['certificate'].__setitem__('trace_norm_ceiling','1/48'),True)
    attack('missing-trace-square-root','forward',lambda r:r['quantitative'].__setitem__('trace_distance_ceiling','7/8192'),True)
    attack('mixed-distance-imposed-pure-equality','reverse',lambda r:r['certificate']['mixed_density_control'].__setitem__('trace_norm_squared','32/25'),True)
    attack('nonpositive-mixed-density','reverse',lambda r:r['certificate']['mixed_density_control']['rho'][0].__setitem__(1,'1'),True)
    attack('unknown-mean-square-uncharged','reverse',lambda r:r['certificate'].__setitem__('variance_floor','5/24'),True)
    attack('Haar-variance-substituted','forward',lambda r:r['quantitative'].__setitem__('actual_variance_lower','1/4'),True)
    attack('normal-concentration-meets-actual-energy','reverse',lambda r:r['certificate']['concentrating_normal_state'].__setitem__('reference_energy_lower_bound','0'),True)
    attack('reference-scalar-forgotten','reverse',lambda r:r['certificate']['reference_scalar_and_scale'].__setitem__('ground','0'),True)
    attack('wrong-reference-energy-units','reverse',lambda r:r['certificate']['reference_scalar_and_scale'].__setitem__('delta','24'),True)
    attack('extra-cap-promoted-to-stability-radius','forward',lambda r:r['quantitative'].__setitem__('numerical_stability_interval_evaluated',True))
    attack('chosen-positive-coupling-fabricated','reverse',lambda r:r['certificate'].__setitem__('chosen_positive_admissible_tau','1/65536'))
    attack('reference-energy-promoted-to-physical-moment','forward',lambda r:r['scope'].__setitem__('physical_energy_moment_claimed',True))
    attack('unproved-operator-domain','reverse',lambda r:r['scope'].__setitem__('operator_domain_proved',True))
    attack('unproved-spectral-window','reverse',lambda r:r['scope'].__setitem__('spectral_window_proved',True))
    attack('continuum-upgrade','reverse',lambda r:r['scope'].__setitem__('continuum_claim',True))
    attack('effect-half-factor-applied-to-signed-mean','independent',lambda r:r['certificate_and_controls'].__setitem__('mean_absolute_ceiling',{'numerator':1,'denominator':48}),True)
    attack('refinement-attribution-erased','independent',lambda r:r['scope'].__setitem__('independent_stronger_floor','119/576'))
    return {'status':'passed','semantic_mutations_rejected':len(rejected),'controls':rejected,
            'specification_sha256':digest(validator.source(spec_name)),'new_research_loops':0,'producer_executions':0,
            'scope':'Hash-independent exact and scope projections; no new scientific execution or evidence.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--spec',default=PREFIX+'advisor/ak1-admission.json');args=parser.parse_args()
    print(json.dumps(run(args.spec),sort_keys=True))
