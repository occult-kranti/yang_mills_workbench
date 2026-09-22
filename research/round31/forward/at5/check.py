#!/usr/bin/env python3
"""Source-bound AT5 fixed design and reusable-domain controls."""
from pathlib import Path
from fractions import Fraction as Q
import argparse
import hashlib
import json
from calculator import certify,exact,require

BASE=Path(__file__).resolve().parent
CONTRACT_SHA='b936651d4520436e559e1e6bd071376c609bed868214751bf55a833a0ab6fba1'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def compute():
    path=BASE/'inputs/research/round31/contracts/at5.json'
    require(sha(path)==CONTRACT_SHA,'wrong contract bytes')
    c=json.loads(path.read_text())
    require(c['id']=='AT5' and c['parameters']['tau']=='1/100000000000000','wrong frozen design')
    result=certify(fixed_design=True)
    checks=[]
    def check(identity,condition,**details):
        require(condition,'failed '+identity);checks.append({'id':identity,'passed':True,**details})
    radius=Q(result['certified_absolute_error']); width=Q(result['interval_width']);datum=Q(result['certified_datum'])
    lo=Q(result['actual_C_interval']['lower']);hi=Q(result['actual_C_interval']['upper'])
    check('nonzero_frozen_coupling',result['nonzero_interacting_coupling'] is True and result['parameters']['tau']=='1/100000000000000')
    check('complete_rational_datum_radius',sum((Q(x) for x in result['costs'].values()),Q(0))==radius and lo==datum-radius and hi==datum+radius)
    check('frozen_target_met',result['target_met'] is True and radius<=Q(1,10**6) and width<=Q(2,10**6),certified_radius=result['certified_absolute_error'])
    check('radius_versus_width',Q(1,10**6)<width<=Q(2,10**6) and width==2*radius,description='width exceeds 1e-6 but valid point-error radius is below 1e-6')
    check('free_reference_not_excluded',lo<=Q(result['free_C_interval']['lower']) and Q(result['free_C_interval']['upper'])<=hi and result['resolved_interaction_shift'] is False)
    small_L=certify(L='10000')
    cap=certify(tau='1/100000000')
    check('small_cutoff_still_insufficient',small_L['target_met'] is False and Q(small_L['costs']['Poisson_tail'])>Q(1,10**6))
    check('original_cap_still_insufficient',cap['target_met'] is False and Q(cap['costs']['state'])>Q(1,10**6))
    negative=certify(tau='-1/100000000000000')
    check('both_signs_same_certificate',negative['certified_datum']==result['certified_datum'] and negative['certified_absolute_error']==result['certified_absolute_error'])
    zero=certify(tau='0')
    check('zero_coupling_free_limit',zero['exact_zero_reference_branch'] is True and zero['actual_C_interval']==zero['free_C_interval'] and all(Q(zero['costs'][key])==0 for key in ('state','centering','real_time_comparison','Poisson_tail')))
    check('uncentered_mean_square_retained',Q(result['costs']['centering'])==Q(result['state_distance_upper'])**2>0 and radius>radius-Q(result['costs']['centering']))
    scaled=certify(alpha='5',hbar='7',E_star='3',lattice_spacing='2')
    check('physical_clock_not_eightfold',scaled['physical_Euclidean_time']=='7/5' and Q(5)*Q(scaled['physical_Euclidean_time'])/Q(7)==1 and Q(5,8)*Q(scaled['physical_Euclidean_time'])/Q(7)==Q(1,8) and scaled['certified_datum']==result['certified_datum'])
    rejected=[]
    cases=[
      ('nonzero_selected',{'selected':('0','1/100','0')}),
      ('selected_wrong_length',{'selected':('0','0')}),
      ('selected_float',{'selected':('0',0.0,'0')}),
      ('selected_malformed',{'selected':('0','NaN','0')}),
      ('positive_cap_exceeded',{'tau':'1/10000000'}),
      ('negative_cap_exceeded',{'tau':'-1/10000000'}),
      ('tau_float',{'tau':1e-14}),('tau_bool',{'tau':True}),
      ('tau_nan',{'tau':'NaN'}),('tau_infinity',{'tau':'Infinity'}),
      ('tau_empty',{'tau':''}),('tau_zero_denominator',{'tau':'1/0'}),
      ('tau_bad_separator',{'tau':'1//2'}),('tau_object',{'tau':None}),
      ('s_zero',{'s':'0'}),('s_negative',{'s':'-1'}),
      ('L_zero',{'L':'0'}),('L_negative',{'L':'-1'}),
      ('alpha_zero',{'alpha':'0'}),('hbar_negative',{'hbar':'-1'}),
      ('E_star_zero',{'E_star':'0'}),('lattice_spacing_zero',{'lattice_spacing':'0'}),
      ('target_zero',{'target':'0'}),('target_float',{'target':1e-6}),
      ('fixed_design_changed_tau',{'fixed_design':True,'tau':'0'}),
      ('fixed_design_changed_s',{'fixed_design':True,'s':'2'}),
      ('fixed_design_changed_L',{'fixed_design':True,'L':'10000'}),
      ('fixed_design_changed_target',{'fixed_design':True,'target':'1/100'}),
      ('fixed_design_not_boolean',{'fixed_design':'true'}),
    ]
    for name,kwargs in cases:
        try:certify(**kwargs)
        except ValueError:rejected.append(name)
        else:raise RuntimeError('invalid calculator case accepted: '+name)
    check('malformed_and_domain_inputs_rejected',len(rejected)==len(cases),rejected_cases=rejected)
    check('exact_input_forms',exact(Q(1,10),'q')==exact('0.1','decimal')==exact('1/10','ratio') and exact(1,'int')==Q(1))
    # The exact rational midpoint is the exported datum; arithmetic interval
    # radius is paid separately even though it is tiny at this design.
    check('arithmetic_error_explicit',Q(result['costs']['arithmetic'])>0 and Q(result['costs']['arithmetic'])<Q(1,10**25))
    return {'loop':'AT5','direction':'forward','human_author':'Hruday N M (BUNZEEY)',
            'contribution_alias':'HNM-AT5-F certified single-node AQ comparison',
            **result,'checks':checks,
            'controls_summary':{'small_L_radius':small_L['certified_absolute_error'],'cap_radius':cap['certified_absolute_error'],'zero_radius':zero['certified_absolute_error'],'negative_coupling_radius':negative['certified_absolute_error']},
            'stop_scope':'one certified node only; no grid or inverse response evaluated'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
    out=Path(args.output);require(out.is_absolute() and not out.exists(),'fresh absolute output required')
    result=compute();out.mkdir(parents=True)
    (out/'results.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    sources={p.relative_to(BASE).as_posix():sha(p) for p in sorted(BASE.rglob('*')) if p.is_file() and (p.relative_to(BASE).parts[0]=='inputs' or p.name in ('check.py','calculator.py','report.md'))}
    manifest={'loop':'AT5','direction':'forward','sources':sources,'outputs':{'results.json':sha(out/'results.json')},'contract_sha256':CONTRACT_SHA}
    (out/'source-manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'loop':'AT5','direction':'forward','checks_passed':len(result['checks']),'target_met':result['target_met'],'resolved_interaction_shift':False},sort_keys=True))
if __name__=='__main__':main()
