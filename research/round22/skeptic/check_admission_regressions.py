#!/usr/bin/env python3
"""Independent replay of the two admission holes found during N2 preparation."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import shutil
import tempfile

ROOT = Path(__file__).absolute().parents[3]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise RuntimeError('output must be fresh')
    module_path = ROOT/'research/round22/admission.py'
    spec = importlib.util.spec_from_file_location('independent_ym22_admission', module_path)
    a = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(a)
    original = a.gate('n1')
    gate_name = 'research/round22/advisor/n1-gate.json'
    names = set(original['files']) | {gate_name}
    names.update(a.read(ROOT/'research/round22/contracts/n1.json')['dependencies'])
    rows = []
    for mode in ('drop_required_instruction', 'false_controls_status'):
        with tempfile.TemporaryDirectory(prefix='ym22-skeptic-regression-') as folder:
            work = Path(folder)
            for name in names:
                target = work/name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT/name, target)
            a.ROOT = work
            g = a.read(work/gate_name)
            if mode == 'drop_required_instruction':
                name = 'research/round22/methods/AGENTS-at-selection.md'
                (work/name).unlink()
                g['files'].pop(name)
                for direction in ('forward', 'reverse'):
                    mname = f'research/round22/{direction}/n1/output/source-manifest.json'
                    m = a.read(work/mname)
                    m['inputs'].pop(name)
                    (work/mname).write_text(json.dumps(m))
                    g['files'][mname] = a.digest(work/mname)
            else:
                name = 'research/round22/forward/n1/output/controls.json'
                c = a.read(work/name)
                c['passed'] = False
                (work/name).write_text(json.dumps(c))
                g['files'][name] = a.digest(work/name)
                mname = 'research/round22/forward/n1/output/source-manifest.json'
                m = a.read(work/mname)
                m['outputs']['controls.json'] = g['files'][name]
                (work/mname).write_text(json.dumps(m))
                g['files'][mname] = a.digest(work/mname)
            (work/gate_name).write_text(json.dumps(g))
            try:
                a.gate('n1')
            except ValueError as error:
                rows.append({'mutation': mode, 'rejected': True, 'reason': str(error)})
            else:
                raise RuntimeError('coherent mutation admitted: '+mode)
            finally:
                a.ROOT = ROOT
    result = {
        'schema': 'ym22-skeptic-admission-regressions-v1',
        'status': 'passed',
        'optimized': not __debug__,
        'research_loops_added': 0,
        'source_hashes': {
            str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (module_path, ROOT/'research/round22/test_admission.py', Path(__file__).absolute())
        },
        'n1_gate_sha256': hashlib.sha256((ROOT/gate_name).read_bytes()).hexdigest(),
        'mutations': rows,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': 'passed', 'rejected_mutations': len(rows), 'optimized': not __debug__}))


if __name__ == '__main__':
    main()
