#!/usr/bin/env python3
"""Mutate disposable copies; require fail-closed admission after coherent rebinding.

Threat model: recorded evidence, result controls, inventories and their digests
may be changed together. The reviewed release specification and validator are
held fixed. This is not a cryptographic defense against rewriting trusted code.
"""
from __future__ import annotations
import argparse
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from research.round29.release.admission import validate_loop, digest, require


def load(path): return json.loads(path.read_text())
def write(path, data): path.write_text(json.dumps(data, indent=2) + '\n')


def coherent_rebind(root, loop):
    """Update manifest, freeze, independent review and gate hashes in dependency order."""
    base = root / 'research/round29'
    for side in ('forward', 'reverse'):
        producer = base / side / loop
        for manifest_path in [producer / 'output/source-manifest.json', producer / 'output/manifest.json']:
            if not manifest_path.is_file(): continue
            manifest = load(manifest_path)
            if 'outputs' in manifest: manifest['outputs']['results.json'] = digest(producer / 'output/results.json')
            if 'results_sha256' in manifest: manifest['results_sha256'] = digest(producer / 'output/results.json')
            write(manifest_path, manifest)
        frozen = load(producer / 'freeze.json')
        if isinstance(frozen['files'], dict):
            frozen['files'] = {rel: digest(producer / rel) for rel in frozen['files']}
        else:
            for row in frozen['files']: row['sha256'] = digest(producer / row['path'])
        write(producer / 'freeze.json', frozen)
    review_path = base / f'skeptic/{loop}.json'; review = load(review_path)
    review['bindings'] = {rel: digest(root / rel) for rel in review['bindings']}
    write(review_path, review)
    gate_path = base / f'advisor/{loop}-gate.json'; gate = load(gate_path)
    gate['bindings'] = {rel: digest(root / rel) for rel in gate['bindings']}
    write(gate_path, gate)


def run(root=ROOT, complete=False, use_reproduce=True):
    root = Path(root).resolve(); base = root / 'research/round29'
    findings = load(base / 'advisor/findings.json'); loops = [item['id'].lower() for item in findings['loops']]
    require(bool(loops), 'No admitted loops to test')
    for row in findings['loops']: validate_loop(root, row['id'], row=row)
    if use_reproduce:
        spec = importlib.util.spec_from_file_location('ym29_mutation_reproduce', base / 'reproduce.py'); reproduce = importlib.util.module_from_spec(spec); spec.loader.exec_module(reproduce)
        def validate(target): return reproduce.verify(target, complete=complete)
    else:
        def validate(target):
            f = load(target/'research/round29/advisor/findings.json')
            for row in f['loops']: validate_loop(target, row['id'], row=row)
    validate(root)
    cases = []
    # Each semantic contract must be exercised; controls are selected by name, never by a count.
    contract = load(base / 'release/admission-contract.json')
    for loop in loops:
        required_reverse = contract['loops'][loop]['directions']['reverse'].get('controls', [])
        if required_reverse:
            cases.extend([(loop, 'omitted_required_control', required_reverse[0]), (loop, 'coherently_rebound_false_control', required_reverse[0])])
        required_forward = contract['loops'][loop]['directions']['forward'].get('checks', [])
        if required_forward: cases.append((loop, 'omitted_required_check', required_forward[0]))
    if 'am2' in loops:
        cases += [('am2','nonstrict_resolvent_cap',None),('am2','false_infinite_volume_claim',None)]
    first = loops[0]
    cases += [(first, 'missing_source', None), (first, 'removed_counterpart', None), (first, 'changed_limits', None), (first, 'reviewer_omits_counterpart', None)]
    receipts = []
    with tempfile.TemporaryDirectory(prefix='ym29-admission-') as temporary:
        for index, (loop, case, key) in enumerate(cases):
            fixture = Path(temporary) / str(index); target = fixture / 'research/round29'
            shutil.copytree(base, target, ignore=shutil.ignore_patterns('__pycache__', 'replays', 'presentation'))
            if case in ('omitted_required_control', 'coherently_rebound_false_control'):
                output = target / f'reverse/{loop}/output/results.json'; data = load(output)
                if case == 'omitted_required_control': del data['controls'][key]
                else: data['controls'][key] = False
                write(output, data); coherent_rebind(fixture, loop)
            elif case in ('nonstrict_resolvent_cap','false_infinite_volume_claim'):
                output = target / f'forward/{loop}/output/results.json'; data=load(output)
                if case == 'nonstrict_resolvent_cap': data['exclusion_cap']='1'
                else: data['infinite_volume_proven']=True
                write(output,data);coherent_rebind(fixture,loop)
            elif case == 'omitted_required_check':
                output = target / f'forward/{loop}/output/results.json'; data = load(output); data['checks'].remove(key)
                write(output, data); coherent_rebind(fixture, loop)
            elif case == 'missing_source':
                source = next(p for p in (target / f'forward/{loop}/inputs').rglob('*') if p.is_file()); source.unlink()
            elif case == 'removed_counterpart':
                gate_path = target / f'advisor/{loop}-gate.json'; gate = load(gate_path)
                del gate['bindings'][f'research/round29/reverse/{loop}/report.md']; write(gate_path, gate)
            elif case == 'changed_limits':
                gate_path = target / f'advisor/{loop}-gate.json'; gate = load(gate_path); gate['limitations'] = ['No remaining assumptions or limitations.']; write(gate_path, gate)
                fpath = target/'advisor/findings.json'; f = load(fpath)
                for row in f['loops']:
                    if row['id'].lower() == loop: row['limitations'] = gate['limitations']
                write(fpath, f)
            elif case == 'reviewer_omits_counterpart':
                rpath = target / f'skeptic/{loop}.json'; review = load(rpath)
                del review['bindings'][f'research/round29/reverse/{loop}/freeze.json']; write(rpath, review)
                gpath = target / f'advisor/{loop}-gate.json'; gate = load(gpath); gate['bindings'][str(rpath.relative_to(fixture))] = digest(rpath); write(gpath, gate)
            try:
                validate(fixture)
            except (ValueError, FileNotFoundError, KeyError) as error:
                receipts.append({'loop': loop, 'case': case, 'control': key, 'verdict': 'rejected', 'reason': str(error)})
            else:
                raise RuntimeError('Admission accepted mutant ' + loop + '/' + case)
    return {'status': 'passed', 'validator': 'reproduce.verify' if use_reproduce else 'release.admission.validate_loop', 'admitted_loops': len(loops), 'mutations_rejected': len(receipts), 'threat_model': __doc__.split('Threat model:')[1].strip(), 'cases': receipts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path); parser.add_argument('--complete', action='store_true'); parser.add_argument('--admission-only', action='store_true')
    args = parser.parse_args(); result = run(complete=args.complete, use_reproduce=not args.admission_only)
    if args.output:
        require(args.output.is_absolute() and not args.output.resolve().is_relative_to(ROOT.resolve()), 'Use an external absolute receipt path')
        require(not args.output.exists(), 'Receipt must be fresh'); args.output.parent.mkdir(parents=True, exist_ok=True); write(args.output, result)
    print(json.dumps(result))

if __name__ == '__main__': main()
