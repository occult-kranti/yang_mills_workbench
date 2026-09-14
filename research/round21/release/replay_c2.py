#!/usr/bin/env python3
"""Replay C2 against a separately reviewed inventory, retaining its legacy failure.

No historical source or gate is changed. Expected data is read only after its
digest is checked against a frozen trust anchor. No gate is generated here.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
R19 = 'research/round19/'
INVENTORY_SHA256 = 'a3dbec14652f4b5b3c024fe8e9e125c5845fe410e0869178321fe333ee6c764b'
EXCLUDED = R19+'backward/c2/history/pre-round20-validator-audit/__pycache__/compare.cpython-312.pyc'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def checked_path(root, relative):
    if type(relative) is not str or not relative or Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise ValueError('invalid admitted relative path')
    p = root/relative
    for part in (p, *p.parents):
        if part.is_symlink():
            raise ValueError('symlink in admitted path: '+relative)
    if not p.is_file():
        raise ValueError('missing scientific/reviewed file: '+relative)
    return p


def validate_inventory(root, inventory):
    # Inspect the lexical path before resolving it, including intermediate links.
    for p in (inventory, *inventory.parents):
        if p.is_symlink():
            raise ValueError('symlink inventory path')
    if digest(inventory) != INVENTORY_SHA256:
        raise ValueError('reviewed inventory digest mismatch; expected hashes are not trusted')
    data = json.loads(inventory.read_text())
    if data['schema'] != 'ym21-c2-reviewed-inventory-v1' or set(data['excluded']) != {EXCLUDED}:
        raise ValueError('unexpected inventory schema or exclusion')
    for name, expected in data['files'].items():
        if type(expected) is not str or re.fullmatch('[0-9a-f]{64}', expected) is None:
            raise ValueError('invalid digest')
        if digest(checked_path(root, name)) != expected:
            raise ValueError('reviewed scientific/release bytes changed: '+name)
    if not set(data['required_scientific_inputs']) <= data['files'].keys():
        raise ValueError('incomplete scientific inventory')
    return data


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def exact_semantics(target, role):
    result = json.loads((target/'results.json').read_text())
    rows = json.loads((target/'coefficients.json').read_text())['rows']
    if [r['degree'] for r in rows] != list(range(9)) or any(type(r['degree']) is not int for r in rows):
        raise ValueError('coefficient degree inventory/type')
    N = [F(r['numerator_taylor_coeff']) for r in rows]
    Z = [F(r['partition_taylor_coeff']) for r in rows]
    if N[:4] != [F(0), F(0), F(1,324), F(13,1296)] or Z[:4] != [F(1), F(0), F(13,8), F(1,4)]:
        raise ValueError('scientific coefficient mismatch despite any passed flag')
    if any(F(r['numerator_moment']) != N[n]*math.factorial(n) or
           F(r['partition_moment']) != Z[n]*math.factorial(n) for n,r in enumerate(rows)):
        raise ValueError('moment/Taylor normalization mismatch')
    # Reconstruct the exact rational exponential upper bound and primary margin;
    # this arithmetic does not import either producer or use their passed flags.
    K = F(1,8)
    t = 7*K
    E = sum(t**n/F(math.factorial(n)) for n in range(61))
    E += t**61/F(math.factorial(61))/(1-t/62)
    loss = sum(abs(N[n])*K**(n-2) for n in range(3,9))
    tail = E*7**9*K**7/F(math.factorial(9))
    C = N[2]-loss-tail
    if C <= 0 or C/E < F(1,2048):
        raise ValueError('independent exact continuous primary margin failed')
    cert = result['primary_theorem']['certificate']
    if F(cert['K']) != K or F(cert['C_N']) != C or F(cert['exp_upper_E']) != E:
        raise ValueError('certificate differs from independent reconstruction')
    counts = (8,20) if role == 'forward' else (8,13)
    if type(result['checks_count']) is not int or type(result['controls_count']) is not int:
        raise ValueError('noninteger semantic count')
    if (result['checks_count'],result['controls_count']) != counts:
        raise ValueError('semantic fixture inventory')
    if len(result['checks']) != counts[0] or len(result['controls']) != counts[1]:
        raise ValueError('incomplete semantic fixture lists')
    if result['status'] != 'passed' or any(v.get('passed') is not True for v in result['checks']+result['controls']):
        raise ValueError('semantic execution failed')
    if result['static_scope'] != 'kappa is a static integral parameter only; not E_star and not a physical energy/time scale; physical-scale matching remains open/unmatched':
        raise ValueError('unreviewed physical scope')
    return {'degree_count': 9, 'exact_primary_margin': str(C/E-F(1,2048)),
            'semantic_checks': counts[0], 'producer_controls': counts[1]}


def verify_outputs(root, target, role, inventory):
    expected = inventory['expected_outputs'][role]
    actual = {p.name for p in target.iterdir() if p.is_file()}
    if actual != set(expected):
        raise ValueError('fresh output inventory mismatch')
    for name,wanted in expected.items():
        p = checked_path(target,name)
        if digest(p) != wanted:
            raise ValueError('fresh output differs from reviewed expected hash: '+role+'/'+name)
        old = checked_path(root,R19+role+'/c2/output/'+name)
        if p.read_bytes() != old.read_bytes():
            raise ValueError('fresh output differs from historical scientific evidence')
    return exact_semantics(target,role)


def verify_comparison(root, target, producer, evidence, inventory):
    got = json.loads((target/'comparison.json').read_text())
    expected = json.loads(checked_path(root,inventory['comparison_expected']).read_text())
    if got['producer_source'] != str(producer.resolve()) or got['producer_evidence'] != str(evidence.resolve()):
        raise ValueError('comparator did not consume the fresh producer evidence')
    for name in inventory['comparison_volatile_fields']:
        del got[name]
        del expected[name]
    if canonical(got) != canonical(expected):
        raise ValueError('comparison changed beyond its two declared absolute paths')
    if got['status'] != 'accepted' or got['admission_failures'] != []:
        raise ValueError('comparator admission failed')
    if type(got['checks_count']) is not int or got['checks_count'] != 34 or len(got['checks']) != 34 or len(got['mutation_controls']) != 27:
        raise ValueError('comparison controls missing or mistyped')
    if any(c['passed'] is not True for c in got['checks']+got['mutation_controls']):
        raise ValueError('comparison control failed')
    if any(not c['detected_failures'] for c in got['mutation_controls']):
        raise ValueError('mutation accepted without an actual rejecting condition')
    verify_outputs(root,target/'independent-reconstruction','backward',inventory)
    return {'semantic_checks': 34, 'rejected_scientific_mutations': 27,
            'identical_to_historical_except_validated_absolute_paths': True}


def execute(cmd, root, log):
    p = subprocess.run(cmd,cwd=root,capture_output=True,text=True)
    log.write_text(p.stdout+p.stderr)
    if p.returncode:
        raise RuntimeError('scientific replay failed; see '+str(log))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True,help='fresh directory outside repository')
    ap.add_argument('--inventory',type=Path,default=HERE/'reviewed-inventory.json')
    ap.add_argument('--optimized',action='store_true')
    args = ap.parse_args()
    inventory = validate_inventory(ROOT,args.inventory)
    out = args.output.absolute()
    if out.exists() or out.resolve() == ROOT or ROOT in out.resolve().parents:
        raise ValueError('fresh output outside repository required')
    out.mkdir(parents=True)
    flags = ['-B']+(['-O'] if args.optimized else [])
    legacy_cmd = [sys.executable,*flags,str(ROOT/(R19+'reproduce.py')),
                  '--from-loop','c2','--through','c2','--output',str(out/'historical-attempt')]
    legacy = subprocess.run(legacy_cmd,cwd=ROOT,capture_output=True,text=True)
    (out/'historical-failure.log').write_text(legacy.stdout+legacy.stderr)
    if legacy.returncode == 0 or 'missing gate file: '+EXCLUDED[len(R19):] not in legacy.stderr:
        raise ValueError('historical failure differs from reviewed cache omission')
    legacy_record = {'command':legacy_cmd, 'returncode':legacy.returncode,
                     'missing_file':EXCLUDED, 'historical_gate_remains_failed':True}
    records = {}
    for role in ('forward','backward'):
        target = out/role
        execute([sys.executable,*flags,str(ROOT/(R19+role+'/c2/check.py')),
                 '--output',str(target)],ROOT,out/(role+'.log'))
        records[role] = verify_outputs(ROOT,target,role,inventory)
    producer = ROOT/(R19+'forward/c2/check.py')
    execute([sys.executable,*flags,str(ROOT/(R19+'backward/c2/compare.py')),
             '--producer',str(producer),'--evidence',str(out/'forward'),
             '--output',str(out/'comparison')],ROOT,out/'comparison.log')
    records['comparison'] = verify_comparison(ROOT,out/'comparison',producer,out/'forward',inventory)
    validate_inventory(ROOT,args.inventory)
    result = {'schema':'ym21-c2-replay-v1','status':'completed', 'optimized':args.optimized,
              'inventory_sha256':INVENTORY_SHA256,'bound_files':len(inventory['files']),
              'historical_failure':legacy_record,'replays':records,
              'research_loops_added':0,
              'scope':'Reproducibility repair for the existing static C2 theorem only; no new physics theorem or physical scale matching.'}
    (out/'replay.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'completed','bound_files':len(inventory['files']),
                      'research_loops_added':0,'historical_failure_preserved':True}))


if __name__ == '__main__':
    main()
