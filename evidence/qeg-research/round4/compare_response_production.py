"""Compare frozen production arrays with independently generated spinor data.

Imports no solver. Reads the independent verification JSON and production
results, requires identical preparation/regulator/sampling, and verifies code
provenance before evaluating differences. A changed producer file is rejected.
"""
from pathlib import Path
import argparse
import hashlib
import json

import numpy as np

ROOT=Path(__file__).resolve().parent
PARAMETERS={'b':'b','nmax':'ncut','Kmax':'Kmax','nK':'nK','amplitude':'target_E',
            'pump_duration':'Tpump','final_time':'tfinal','samples':'sample_count','a0':'a0'}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--production',type=Path,default=ROOT/'response_results.json')
    parser.add_argument('--production-source',type=Path,default=ROOT/'code/response.py')
    args=parser.parse_args()
    production=json.loads(args.production.read_text())
    independent=json.loads((ROOT/'response_verification.json').read_text())
    current_source_hash=digest(args.production_source)
    independent_hash=digest(ROOT/'verify_response.py')
    checks={
      'independent_gates_passed':independent['all_checks_passed'],
      'independent_source_matches':independent_hash==independent['provenance']['source_sha256'],
      'production_top_source_matches':current_source_hash==production['source_hash'],
    }
    cases={}
    for name in ['baseline','heldout']:
        ref=independent[name]
        matches=[]
        for label,record in production['records'].items():
            params=record['parameters']
            if record['mode']!='source_amplitude':
                continue
            if all(np.isclose(params[there],ref['config'][here],rtol=0,atol=1e-13)
                   for here,there in PARAMETERS.items()):
                matches.append((label,record))
        checks[name+'_matching_case']=bool(matches)
        if len(matches)!=1:
            cases[name]={'status':'missing_or_ambiguous_record','matching_labels':[p[0] for p in matches]}
            checks[name+'_matching_case']=False
            continue
        label,record=matches[0]
        macro=record['base']['macro']
        checks[name+'_record_source_matches']=record['source_hash']==current_source_hash
        checks[name+'_sampling_matches']=len(macro['s'])==len(ref['t']) and np.allclose(macro['s'],ref['t'],rtol=0,atol=2e-13)
        if not checks[name+'_sampling_matches']:
            cases[name]={'status':'sample_grid_mismatch'}
            continue
        differences={}
        for key,other in [('u','dx_damplitude'),('v','da_damplitude'),
                          ('deltaJmatter_direct','dcurrent_damplitude'),
                          ('deltaJmatter','dcurrent_damplitude'),('x','x')]:
            differences[key]=float(np.max(abs(np.asarray(macro[key])-ref[other])))
        checks[name+'_field_tangent']=differences['u']<2e-8
        checks[name+'_potential_tangent']=differences['v']<2e-8
        checks[name+'_direct_matched_current_tangent']=differences['deltaJmatter_direct']<2e-8
        checks[name+'_Maxwell_matched_current_tangent']=differences['deltaJmatter']<2e-8
        checks[name+'_background_field']=differences['x']<2e-8
        cases[name]={'production_record':label,'configuration':record['parameters'],
                     'maximum_full_history_absolute_differences':differences,
                     'acceptance_threshold':2e-8,
                     'production_record_source_hash':record['source_hash'],
                     'independent_direct_current':'Differentiated matched current using u-prime in derivative counterterms',
                     'shared_assumptions':'Same finite weights, vacuum preparation, one-loop matching and homogeneous mean-field model'}
    result={
      'scope':'Independent complex-spinor versus production real-Bloch comparison at two identical finite regulators and preparations. No continuum, noise, all-time stability or gravitational validity certificate.',
      'cases':cases,'checks':checks,'all_checks_passed':all(checks.values()),
      'provenance':{
        'production_results_sha256':digest(args.production),
        'production_source_sha256':current_source_hash,
        'independent_results_sha256':digest(ROOT/'response_verification.json'),
        'independent_source_sha256':independent_hash,
        'comparison_source_sha256':digest(Path(__file__)),
        'production_code_imported':False,
      }
    }
    (ROOT/'response_production_comparison.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2))
    if not result['all_checks_passed']:
        raise AssertionError('Frozen comparison did not satisfy all recorded gates')


if __name__=='__main__':
    main()
