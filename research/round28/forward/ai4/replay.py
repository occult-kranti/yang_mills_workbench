#!/usr/bin/env python3
"""Fresh exact AI4 forward replays with semantic checks, including Python -O."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    receipt=HERE/'verification.json'
    if receipt.exists():
        raise ValueError('preserve existing verification')
    bound=('check.py','report.md','output/results.json','inputs/source-inventory.json','inputs/snapshot-event.json')
    before={p:sha(HERE/p) for p in bound}
    expected=(HERE/'output/results.json').read_bytes()
    records=[]
    with tempfile.TemporaryDirectory(prefix='ai4-fresh-',dir=HERE) as temporary:
        for mode,flags in [('normal',['-B']),('optimized',['-O','-B'])]:
            output=Path(temporary)/mode
            command=[sys.executable,*flags,str(HERE/'check.py'),'--output',str(output)]
            result=subprocess.run(command,capture_output=True,text=True)
            if result.returncode:
                raise ValueError(mode+' failed: '+result.stderr)
            generated=(output/'results.json').read_bytes()
            if generated!=expected:
                raise ValueError(mode+' output changed')
            data=json.loads(generated)
            if data['check_count']!=7625 or data['check_count']!=len(data['checks']):
                raise ValueError('active semantic check count')
            fixture_keys=[(r['j'],r['position']) for r in data['fixtures']]
            expected_keys=[(j,p) for j in [0,1,8,64,512] for p in ['upper','midpoint']]
            if fixture_keys!=expected_keys or data['new_collar_enumerations']!=0:
                raise ValueError('frozen fixture and collar scope')
            proof=data['uniform_proof']
            if F(proof['uniform_gap_coefficient'])<=F(97,100):
                raise ValueError('uniform theorem coefficient')
            if F(proof['gap_coefficient_with_extra_scalar_error'])<=F(78,100):
                raise ValueError('additional scalar allowance')
            required={'geometry_induction','continuous_q_bounds','all_j_spatial_recurrence',
                'all_j_growing_M_and_M_squared_recurrence','all_order_numerator_tail','fixed_inner_rounding_propagated'}
            if set(proof['proof_anchors'])!=required or any(v is not True for v in proof['proof_anchors'].values()):
                raise ValueError('required uniform proof declarations')
            if data['current_reverse_AI4_read'] is not False:
                raise ValueError('independent freeze scope')
            records.append({'mode':mode,'flags':flags,'exit_code':0,'byte_equal_to_frozen':True,
                'result_sha256':sha(output/'results.json'),'checks':data['check_count'],'fixtures':len(fixture_keys)})
    after={p:sha(HERE/p) for p in bound}
    if before!=after:
        raise ValueError('source changed during replay')
    receipt.write_text(json.dumps({'status':'passed','normal_optimized_byte_equality':True,
        'producer_before':before,'producer_after':after,'replay_sha256':sha(Path(__file__)),
        'runs':records,'temporary_outputs_removed_after_byte_comparison':True},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','runs':records},indent=2))


if __name__=='__main__':
    main()
