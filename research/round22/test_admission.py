#!/usr/bin/env python3
"""Exercise admission rejection paths against coherent mutations of a copied gate."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
import admission as a


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--loop', default='n1')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    original_root = a.ROOT
    original_gate = a.gate(args.loop)
    gate_name = f'research/round22/advisor/{args.loop}-gate.json'
    prefix = f'research/round22/forward/{args.loop}/'
    rows = []

    def write(path, value):
        path.write_text(json.dumps(value, indent=2)+'\n')

    def test(name, mutate):
        with tempfile.TemporaryDirectory(prefix='ym22-admission-') as folder:
            root = Path(folder)
            names = set(original_gate['files']) | {gate_name}
            contract = a.read(original_root/f'research/round22/contracts/{args.loop}.json')
            names.update(contract['dependencies'])
            for rel in names:
                target = root/rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(original_root/rel, target)
            a.ROOT = root
            try:
                a.gate(args.loop)
                g = deepcopy(original_gate)
                mutate(root, g)
                write(root/gate_name, g)
                rejected = False
                try:
                    a.gate(args.loop)
                except (ValueError, KeyError, TypeError):
                    rejected = True
                a.require(rejected, 'mutation admitted: '+name)
                rows.append({'control':name, 'rejected':True})
            finally:
                a.ROOT = original_root

    def rebind(root, g, rel):
        g['files'][rel] = a.digest(root/rel)

    def changed_result(field, value):
        def mutate(root, g):
            rel = prefix+'output/results.json'
            d = a.read(root/rel)
            d[field] = value
            write(root/rel, d)
            rebind(root, g, rel)
            manifest_name = prefix+'output/source-manifest.json'
            manifest = a.read(root/manifest_name)
            manifest['outputs']['results.json'] = g['files'][rel]
            write(root/manifest_name, manifest)
            rebind(root, g, manifest_name)
        return mutate

    test('missing_required_report', lambda root,g:(root/(prefix+'report.md')).unlink())
    test('dropped_required_report_inventory', lambda root,g:g['files'].pop(prefix+'report.md'))
    test('changed_source_bytes', lambda root,g:(root/(prefix+'check.py')).write_text('# changed\n'))
    test('coherent_false_result_status', changed_result('status', True))
    test('coherent_wrong_loop', changed_result('loop', 'n2' if args.loop != 'n2' else 'n1'))
    test('coherent_wrong_direction', changed_result('direction', 'reverse'))
    test('coherent_nonboolean_passed', changed_result('passed', 'true'))
    test('coherent_false_passed', changed_result('passed', False))
    for field, expected in original_gate['expected_results']['forward'].items():
        if field in ('loop', 'direction', 'status', 'passed'):
            continue
        test('coherent_changed_reviewed_'+field, changed_result(field, {'unsupported_change':True}))

    def missing_controls(root, g):
        rel = prefix+'output/controls.json'
        (root/rel).unlink()
        g['files'].pop(rel)
        manifest_name = prefix+'output/source-manifest.json'
        manifest = a.read(root/manifest_name)
        manifest['outputs'].pop('controls.json')
        write(root/manifest_name, manifest)
        rebind(root, g, manifest_name)
    test('coherently_removed_required_controls', missing_controls)

    def missing_instruction(root, g):
        contract = a.read(root/f'research/round22/contracts/{args.loop}.json')
        rel = next(n for n in contract['instruction_inputs'] if n != 'research/round22/methods/team-protocol.md')
        (root/rel).unlink()
        g['files'].pop(rel)
        for direction in ('forward','reverse'):
            mname = f'research/round22/{direction}/{args.loop}/output/source-manifest.json'
            m = a.read(root/mname)
            m['inputs'].pop(rel)
            write(root/mname, m)
            rebind(root, g, mname)
    test('coherently_removed_declared_instruction_snapshot', missing_instruction)

    def changed_controls(flag, nested=False):
        def mutate(root, g):
            rel = prefix+'output/controls.json'
            controls = a.read(root/rel)
            if nested:
                controls['controls'][0]['passed'] = flag
            else:
                controls['passed'] = flag
            write(root/rel, controls)
            rebind(root, g, rel)
            mname = prefix+'output/source-manifest.json'
            m = a.read(root/mname)
            m['outputs']['controls.json'] = g['files'][rel]
            write(root/mname, m)
            rebind(root, g, mname)
        return mutate
    test('coherent_failed_controls', changed_controls(False))
    test('coherent_truthy_nonboolean_controls', changed_controls('true'))
    test('coherent_failed_nested_control', changed_controls(False, nested=True))

    def parent_link(root, g):
        folder = root/prefix/'output'
        alternate = folder.parent/'moved-output'
        folder.rename(alternate)
        folder.symlink_to(alternate, target_is_directory=True)
    test('symlinked_parent_with_identical_bytes', parent_link)

    def duplicate_contract(root, g):
        rel = f'research/round22/contracts/{args.loop}.json'
        data = (root/rel).read_text()
        (root/rel).write_text('{"loop":"'+args.loop+'",'+data.lstrip()[1:])
        rebind(root, g, rel)
        for direction in ('forward','reverse'):
            mname = f'research/round22/{direction}/{args.loop}/output/source-manifest.json'
            m = a.read(root/mname)
            m['inputs'][rel] = g['files'][rel]
            write(root/mname, m)
            rebind(root, g, mname)
    test('duplicate_contract_key_with_rebound_hashes', duplicate_contract)
    output = a.unlinked(args.output.absolute())
    a.require(not output.exists(), 'output must be fresh')
    output.parent.mkdir(parents=True, exist_ok=True)
    write(output, {'status':'passed', 'loop':args.loop, 'controls':rows,
                   'optimized':not __debug__, 'gate_sha256':a.digest(original_root/gate_name),
                   'research_loops_added':0})
    print(json.dumps({'status':'passed', 'rejected_mutations':len(rows)}))


if __name__ == '__main__':
    main()
