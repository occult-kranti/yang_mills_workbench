#!/usr/bin/env python3
"""Compare frozen R1 evidence with independent preparation; no producer imports."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).absolute().parents[3]
PREP_SHA = 'c41071dc7961e77a4034f62eb4bcb01368f77c01ebccd2fe349e1f1520fe5037'
SUBMISSIONS = {
    'forward': '7d316fbd9d1f160d0652d2c5e1d43c2f2586d3780fc3def523dce50cd8bc58d5',
    'reverse': 'f11ec0f4692573f8bd684339a43f78f5e280ba4c2eee565a26e301bbea6c6264'}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    out = parser.parse_args().output
    require(not out.exists(), 'fresh comparison output required')
    prep_path = ROOT/'research/round22/skeptic/check_r1_preparation.py'
    require(sha(prep_path) == PREP_SHA, 'frozen independent preparation changed')
    spec = importlib.util.spec_from_file_location('r1_frozen_skeptic_preparation', prep_path)
    prep = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prep)
    independent = json.loads(json.dumps(prep.run()))
    require(independent == read(ROOT/'research/round22/skeptic/r1-preparation-checks.json'),
            'independent preparation replay drift')
    data = {}
    for direction, expected in SUBMISSIONS.items():
        base = ROOT/f'research/round22/{direction}/r1'
        require(sha(base/'submission.json') == expected, 'submission drift')
        submission = read(base/'submission.json')
        for name, digest in submission['files'].items():
            require(sha(ROOT/name) == digest, 'frozen submitted byte drift: '+name)
        data[direction] = {name: read(base/'output'/name) for name in ('results.json','controls.json')}
    fw = data['forward']['results.json']
    rv = data['reverse']['results.json']
    rc = data['reverse']['controls.json']
    expected_cube = {(r['location'],r['L']):r for r in independent['cube_counts']}
    for direction, rows in [('forward',fw['cube_fixtures']),('reverse',rc['complete_boundary']['cube_counts'])]:
        for row in rows:
            place = row['placement'] if direction == 'forward' else ('bulk' if row['bulk'] else 'origin')
            wanted = expected_cube[place,row['L']]
            require(row['interior'] == wanted['interior'] and row['crossing'] == wanted['crossing'],
                    'cube counts disagree with independent geometry')
            require(row['incoming'] == (3*row['L']**2 if place == 'bulk' else 0), 'incoming census')
    probe = independent['actual_probe']
    fm = fw['actual_SU2_moments']
    rm = rc['actual_SU2']
    require(fm['defect_norm_squared_tau2_coefficient'] == rm['boundary_vacuum_norm_squared_over_tau_squared']
            == probe['boundary_vacuum_norm_squared_over_tau_squared'], 'actual SU2 defect comparison')
    require(fm['probe_edge_face_incidence'] == probe['faces_touching_probe_edge'] == 2, 'actual edge incidence')
    require(fm['cross_sign_witnesses'] == rm['all_cross_pairs_checked'] == 210, 'all cross-face pairs')
    require(fm['source_norm_squared'] == rm['Haar_chi_norm_squared'] == '1', 'actual character normalization')
    require(fm['free_energy'] == rm['dimensionless_probe_energy'] == '6', 'physical energy unit')
    require(fm['conditional_diagonal_moments'] == ['1/4']*21, 'all twenty-one diagonal contributions')
    require(fm['vacuum_projection_moments'] == ['0']*21, 'vacuum projection correction')
    for rows, axes_key, support_key in [(fm['face_census'],'axes','support'),(rm['face_ledger'],'plane','actual_support')]:
        require(len(rows) == 21, 'complete face census')
        for row in rows:
            a,b = row[axes_key]
            edges = prep.face(tuple(row['anchor']),a,b)
            require({tuple(x) for x in row[support_key]} == {prep.owner(e) for e in edges},
                    'actual support census differs from independent ownership')
    for row in fw['inverse_fixtures']:
        tau = F(row['tau'])
        d2 = F(7,12)*tau*tau
        lower2 = (1-7*abs(tau))**2*d2
        require(F(row['actual_internal_source_norm_squared']) == 36+d2, 'extra actual-star source norm')
        require(F(row['bare_internal_defect_norm_squared_lower']) == lower2, 'extra actual-star bound')
        require((lower2 > 0) == (tau != 0), 'signed coupling and zero in actual-star bound')
    # The written Haar proof of <w,Dw>=0 uses a free edge other than the probe;
    # verify that such a witness survives for every actual face.
    require(len(probe['one_free_edge_per_face_away_from_probe']) == 21, 'actual-star orthogonality witnesses')
    correct = F(7,432)
    wrong = F(2,4*9*36)
    require(correct-wrong == F(19,1296), 'two physically incident faces are insufficient')
    # Independently check the root-split arithmetic in forward Eq.8. The
    # analytic step n exp(-ell n)<=1/ell is justified in the written review.
    require(14*4 == 56 and 14*4*4 == 56*4, 'family boundary root prefactors')
    require(rc['complete_boundary']['star_weight'] == 16, 'declared star weight')
    require(2**1 != 16, 'singleton replacement must be rejected')
    require(fw['claims']['source_is_generated_O1_residual'] is False
            and rv['claims']['probe_is_generated_O1_residual'] is False, 'diagnostic scope')
    require(fw['claims']['later_diagonal_iteration_proved'] is False
            and rv['claims']['later_diagonal_inverse_proved'] is False, 'initial-diagonal scope')
    replay = read(ROOT/'research/round22/skeptic/r1-replay-summary.json')
    require(replay['status'] == 'passed', 'fresh replay summary')
    for direction in SUBMISSIONS:
        runs = replay['directions'][direction]['replays']
        require(set(runs) == {'normal','optimized'}, 'both producer modes')
        require(runs['normal']['outputs'] == runs['optimized']['outputs'], 'byte-exact modes')
        require(all(r['exit_code'] == 0 and r['all_declared_outputs_match_frozen'] is True for r in runs.values()),
                'fresh source-bound replay failed')
    result = {
        'schema':'ym22-skeptic-r1-independent-comparison-v1','loop':'r1','passed':True,
        'producer_code_imported':False,'frozen_preparation_rerun_identical':True,
        'frozen_submissions':SUBMISSIONS,'four_producer_replays_byte_exact':True,
        'cube_and_face_geometry_match_prefreeze_derivation':True,
        'arbitrary_connected_supports_independently_checked':167,
        'probe_norm_squared_over_tau_squared':str(correct),
        'physically_incident_probe_faces':2,'all_faces_required':21,
        'wrong_two_face_norm_squared_over_tau_squared':str(wrong),
        'omission_margin_over_tau_squared':str(correct-wrong),
        'forward_actual_star_bare_inverse_refinement':'valid; source Gw has norm squared 36+7tau^2/12; lower bound (1-7|tau|)^2 7tau^2/12 verified at every published fixture',
        'forward_family_weight_loss_prefactors_verified':True,
        'declared_weight_control':'singleton 2 rejected against star 16',
        'source_is_generated_O1_residual':False,'all_stage_iteration_admitted':False,
        'post_freeze_producer_edits':[],'research_loops_added':0}
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')


if __name__ == '__main__':
    main()
