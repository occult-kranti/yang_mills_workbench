#!/usr/bin/env python3
"""Falsify C2 release admission in isolated copies, ordinary and optimized safe."""
import argparse
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def load_validator():
    spec = importlib.util.spec_from_file_location('c2_release_validator',HERE/'replay_c2.py')
    if spec is None or spec.loader is None:
        raise RuntimeError('validator unavailable')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--replay-minimal-checkout',action='store_true',
                    help='also execute C2 with only the admitted 298 files present')
    args = ap.parse_args()
    if args.output.exists():
        raise ValueError('fresh control report required')
    v = load_validator()
    original = HERE/'reviewed-inventory.json'
    inventory = v.validate_inventory(ROOT,original)
    results = []
    minimal_replay = None
    def reject(name,call):
        try:
            call()
        except (ValueError,FileNotFoundError) as err:
            results.append({'name':name,'rejected':True,'reason':str(err)})
        else:
            raise RuntimeError('mutation wrongly admitted: '+name)
    with tempfile.TemporaryDirectory(prefix='ym21-c2-controls-') as tmp:
        base = Path(tmp)
        isolated = base/'repo'
        for name in inventory['files']:
            p = isolated/name
            p.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/name,p)
        v.validate_inventory(isolated,original)
        if args.replay_minimal_checkout:
            release = isolated/'research/round21/release'
            release.mkdir(parents=True)
            shutil.copyfile(HERE/'replay_c2.py',release/'replay_c2.py')
            shutil.copyfile(original,release/'reviewed-inventory.json')
            cmd = [sys.executable,'-B',str(release/'replay_c2.py'),
                   '--output',str(base/'minimal-replay')]
            process = subprocess.run(cmd,cwd=isolated,capture_output=True,text=True)
            if process.returncode:
                raise RuntimeError('minimal inventory checkout failed: '+process.stdout+process.stderr)
            minimal_replay = json.loads((base/'minimal-replay/replay.json').read_text())
        actual_sources = ['forward/c1/check.py','backward/c1/check.py',
                          'forward/c2/check.py','backward/c2/check.py',
                          'backward/c2/compare.py','forward/c1/output/coefficients.json']
        for name in actual_sources:
            p = isolated/(v.R19+name)
            old = p.read_bytes()
            p.unlink()
            reject('missing_required_scientific_input:'+name,
                   lambda:v.validate_inventory(isolated,original))
            p.write_bytes(old)
        p = isolated/(v.R19+'backward/c1/check.py')
        p.write_bytes(p.read_bytes()+b'\n# altered scientific input\n')
        reject('changed_imported_scientific_module',lambda:v.validate_inventory(isolated,original))
        shutil.copyfile(ROOT/(v.R19+'backward/c1/check.py'),p)
        for name,mutate in [
            ('empty_file_inventory', lambda d:d.update(files={})),
            ('deleted_scientific_inventory_entry',lambda d:d['files'].pop(v.R19+'backward/c1/check.py')),
            ('tampered_expected_source_hash',lambda d:d['files'].update({v.R19+'backward/c1/check.py':'0'*64})),
            ('tampered_expected_output_hash',lambda d:d['expected_outputs']['forward'].update({'results.json':'0'*64})),
            ('blanket_cache_exclusion',lambda d:d['excluded'].update({'**/*.pyc':{'reason':'skip'}})),
        ]:
            d = deepcopy(inventory)
            mutate(d)
            candidate = base/(name+'.json')
            candidate.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
            reject(name,lambda:v.validate_inventory(isolated,candidate))
        alias = base/'same-bytes-inventory.json'
        alias.symlink_to(original)
        reject('symlink_inventory',lambda:v.validate_inventory(isolated,alias))
        linked_root = base/'linked-root'
        linked_root.symlink_to(isolated,target_is_directory=True)
        reject('symlink_role_root',lambda:v.validate_inventory(linked_root,original))
        p = isolated/(v.R19+'backward/c1/check.py')
        p.unlink()
        p.symlink_to(ROOT/(v.R19+'backward/c1/check.py'))
        reject('byte_identical_symlink_scientific_source',lambda:v.validate_inventory(isolated,original))
        p.unlink()
        shutil.copyfile(ROOT/(v.R19+'backward/c1/check.py'),p)
        # Hold all recorded success flags fixed while changing actual arithmetic.
        output = base/'forged-output'
        shutil.copytree(ROOT/(v.R19+'forward/c2/output'),output)
        coeff = output/'coefficients.json'
        d = json.loads(coeff.read_text())
        d['rows'][2]['numerator_taylor_coeff'] = '1/325'
        coeff.write_text(json.dumps(d))
        reject('forged_pass_with_wrong_N2_hash_gate',
               lambda:v.verify_outputs(isolated,output,'forward',inventory))
        reject('forged_pass_with_wrong_N2_independent_arithmetic',
               lambda:v.exact_semantics(output,'forward'))
        shutil.copyfile(ROOT/(v.R19+'forward/c2/output/coefficients.json'),coeff)
        result = output/'results.json'
        d = json.loads(result.read_text())
        d['checks_count'] = True
        result.write_text(json.dumps(d))
        reject('boolean_semantic_count',lambda:v.exact_semantics(output,'forward'))
        v.validate_inventory(isolated,original)
    report = {'schema':'ym21-c2-admission-controls-v1','status':'completed',
              'inventory_sha256':v.INVENTORY_SHA256,'controls':results,
              'rejected_count':len(results),'historical_mutations':0,
              'minimal_inventory_checkout_replay':minimal_replay,
              'research_loops_added':0}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'completed','rejected_controls':len(results)}))


if __name__ == '__main__':
    main()
