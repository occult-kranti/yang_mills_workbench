#!/usr/bin/env python3
"""Independent frozen-preparation comparisons for R2; no producer-code imports."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from math import comb
from pathlib import Path

ROOT=Path(__file__).absolute().parents[3]
SUBMISSIONS={'forward':'e94ce5dc3a6a0dcdb6d0bae6c47962e99cac9d5fc519cec7badd83847a885d83',
             'reverse':'4018a911ec3f0563b668a07f33110a8f3d4858011b669db4c3d8718d9f3ca96f'}
PREP_SHA='482c7e3bc31339f5d835e8828fc0676f5355fc89ea06b202f489702713106ba1'


def require(ok,reason):
    if not ok:
        raise RuntimeError(reason)


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def origin_tail(a,k):
    g=1-k
    moments=[1/g,k/g**2,k*(1+k)/g**3,k*(1+4*k+k*k)/g**4]
    return k**a*sum((comb(3,j)*a**(3-j)*moments[j] for j in range(4)),F(0))


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output
    require(not out.exists(),'fresh output required')
    path=ROOT/'research/round22/skeptic/check_r2_preparation.py'
    require(sha(path)==PREP_SHA,'independent preparation source changed')
    spec=importlib.util.spec_from_file_location('skeptic_r2_frozen_prep',path)
    prep=importlib.util.module_from_spec(spec);spec.loader.exec_module(prep)
    own=json.loads(json.dumps(prep.run()))
    require(own==read(ROOT/'research/round22/skeptic/r2-preparation-checks.json'),'frozen preparation replay drift')
    data={}
    for direction,expected in SUBMISSIONS.items():
        base=ROOT/f'research/round22/{direction}/r2'
        require(sha(base/'submission.json')==expected,'frozen submission changed')
        submission=read(base/'submission.json')
        for name,digest in submission['files'].items():
            require(sha(ROOT/name)==digest,'submitted byte drift')
        data[direction]={name:read(base/'output'/name) for name in ('results.json','controls.json')}
    fw=data['forward']['results.json'];rv=data['reverse']['results.json'];rc=data['reverse']['controls.json']
    fs={'origin':{(0,0,0)},'two_sites':{(0,0,0),(1,0,0)},'bulk':{(2,2,2)}}
    rs={'origin':{(0,0,0)},'bulk':{(4,4,4)},'connected_three':{(0,0,0),(1,0,0),(0,1,0)}}
    for row in fw['collar_checks']:
        x=prep.collar(fs[row['source']],row['n'])
        require(row['collar_sites']==len(x) and row['meeting_anchors']==len(prep.touching(x)),'forward collar and full anchor census')
    for row in rc['collars_and_boundaries']['collars']:
        x=prep.collar(rs[row['source']],row['n'])
        require(row['collar_size']==len(x) and row['meeting_stars']==len(prep.touching(x)),'reverse collar and full anchor census')
    for row in fw['tail_checks']:
        k=F(row['kappa']);n=row['N'];e=k**(n+1)/(1-k);t=prep.tail(k,n);j=origin_tail(n+1,k)
        require(F(row['Hilbert_energy_tail_over_r'])==e,'forward geometric tail')
        require(F(row['general_H0_tail_over_r_sizeY'])==t,'forward general graph tail')
        require(F(row['origin_H0_tail_over_r'])==j<=t,'forward sharper origin tail')
        require(F(row['finite_volume_Hilbert_energy_over_r'])==2*e,'forward finite norm/energy factor')
        require(F(row['finite_volume_origin_H0_over_r'])==2*j,'forward finite H0 factor')
        require(F(row['finite_volume_origin_G_over_r'])==j,'forward finite G factor')
        require(F(row['origin_G_partial_residual_over_r'])==(n+1)**3*k**(n+1),'forward local G residual')
    for row in rc['explicit_tails']['evaluations']:
        k=F(row['a']);n=row['N'];t=prep.tail(k,n)
        require(F(row['E_N'])==k**(n+1)/(1-k) and F(row['T_N'])==t,'reverse common tails')
        require(F(row['finite_H_graph_error_over_r_sizeY'])==2*t,'reverse finite H0 factor')
        require(F(row['finite_G_graph_error_over_r_sizeY'])==t,'reverse finite G factor')
    k=F(35,416)
    require(prep.tail(k,0)==k*(1+23*k+23*k*k+k**3)/(1-k)**4,'independent graph generating numerator')
    require(set(prep.touching(prep.star(prep.ZERO)))==prep.star(prep.ZERO),'exact four acting anchors for wrong-sign bound')
    for row in fw['actual_SU2_controls']['coupling_fixtures']:
        tau=F(row['tau']);k=28*abs(tau);bare=F(7,432)*tau*tau
        require(F(row['bare_residual_squared'])==bare,'forward actual boundary defect')
        require(F(row['wrong_first_correction_residual_squared_lower'])==(2-k)**2*bare,'forward actual wrong-sign lower bound')
        require(row['exterior_source_error_squared']=='1','forward exterior sector')
    for row in rc['actual_SU2_source_sectors']['tau_rows']:
        tau=F(row['tau']);bare=F(7,432)*tau*tau
        require(F(row['bare_residual_squared'])==F(row['H_u1_squared'])==bare,'reverse actual first image')
        require(F(row['wrong_first_sign_H_error_squared'])==4*bare,'reverse H-image sign discrepancy')
        require(row['source_sector_error_squared']=='1','reverse exterior sector')
    for direction,rows in [('forward',fw['volume_weight_checks']),('reverse',[rc['volume_weight']])]:
        for row in rows:
            k=F(row['kappa'] if direction=='forward' else row['a'])
            terms=row['upper_terms_over_r'] if direction=='forward' else row['weighted_upper_terms']
            ratios=row['successive_ratios'] if direction=='forward' else row['successive_term_ratios']
            require([F(x) for x in terms]==[2**((n+1)**3)*k**n for n in range(len(terms))],'declared cubic weight terms')
            require([F(x) for x in ratios]==[k*2**(3*n*n+9*n+7) for n in range(len(ratios))],'declared cubic weight ratio')
    require(rv['claims']['local_rank_two_creator_norm_series_converges'] is True,'reverse local creator refinement')
    require(rv['claims']['local_creator_identified_with_global_vacuum_generator'] is False,'creator versus vacuum generator')
    require(fw['claims']['local_operator_norm_locality_proved'] is False,'forward narrower attribution')
    replay=read(ROOT/'research/round22/skeptic/r2-replay-summary.json')
    require(replay['status']=='passed','fresh producer replays')
    for row in replay['directions'].values():
        modes=row['replays']
        require(modes['normal']['outputs']==modes['optimized']['outputs'],'exact producer modes')
        require(all(x['all_declared_outputs_match_frozen'] is True and x['exit_code']==0 for x in modes.values()),'source-bound replay')
    result={'schema':'ym22-skeptic-r2-independent-comparison-v1','loop':'r2','passed':True,
        'frozen_submissions':SUBMISSIONS,'producer_code_imported':False,'frozen_preparation_rerun_identical':True,
        'four_producer_replays_byte_exact':True,'all_published_collar_and_tail_fixtures_match':True,
        'forward_sharper_origin_tail_valid':True,'common_finite_volume_H0_factor':2,'common_finite_volume_G_factor':1,
        'forward_wrong_sign_control':'lower bound on actual full G residual',
        'reverse_wrong_sign_control':'exact H-image discrepancy, a different quantity',
        'actual_exterior_source_error_squared':'1','reverse_local_creator_norm_series_valid':True,
        'local_creator_equals_global_vacuum_generator':False,
        'volume_weight_failure_scope':'specified geometric upper certificate on full collars; no lower bound on actual norms',
        'global_operator_domain_equality_admitted':False,'post_freeze_producer_edits':[],'research_loops_added':0}
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':
    main()
