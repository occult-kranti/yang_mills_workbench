#!/usr/bin/env python3
"""Administrative relocation/mutation fixtures only; no new science or original edits."""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
BASE = 'research/round28/'
REPAIR = BASE + 'release/ah-portability/'
MANIFEST_SHA = 'f2032dd55e5c2ffce75a76147e20aae8d769f27fdb3db3bcb2a9af7157f18671'
RUNNER_SHA = '1feccf9a737b5ee04f7105907224746805b4fb1c56a2ceefe8213d1ce29a514c'
checks = []
mutations = []

def require(value, label):
    if not value:
        raise ValueError(label)
    checks.append(label)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rejected(label, action):
    try:
        action()
    except (ValueError, RuntimeError, FileNotFoundError):
        checks.append(label)
        mutations.append({'control': label, 'rejected': True})
    else:
        raise ValueError('Mutation passed: ' + label)

# Run the actual source binding function while forbidding reads through every
# recorded old repository and installed-origin pathname. No mathematics runs.
PROBE = r"""
import json, pathlib, runpy, sys
root, loop = pathlib.Path(sys.argv[1]), sys.argv[2]
base='research/round28/'
inv=json.loads((root/base/'reverse'/loop/'inputs/instruction-inventory.json').read_text())
forbidden={str(pathlib.Path(e['origin'])) for e in inv.values()}
legacy=pathlib.Path('/workspace/scratch/9daefcf0521b/yang_mills_workbench')
def guard(event,args):
    if event=='open' and isinstance(args[0],(str,bytes)):
        q=pathlib.Path(args[0].decode() if isinstance(args[0],bytes) else args[0])
        if str(q) in forbidden or q.is_relative_to(legacy):
            raise RuntimeError('recorded external origin read forbidden')
sys.addaudithook(guard)
script=root/base/'release/ah-portability'/loop/'check.py'
d=runpy.run_path(str(script),run_name='administrative_source_probe')
b=d['source_bindings' if loop=='ah1' else 'bind_inputs']()
expected=json.loads((root/base/'release/ah-portability'/loop/'expected/results.json').read_text())
if b!=expected['bindings']: raise RuntimeError('actual source bindings differ from approved provenance')
prefix='repo_instruction_original_' if loop=='ah1' else 'repo_instruction_'
actual={k:v for k,v in d['CHECKS'].items() if k.startswith(prefix)}
required={k:v for k,v in expected['checks'].items() if k.startswith(prefix)}
if actual!=required or len(actual)!=8: raise RuntimeError('repository checks dropped')
print(json.dumps({'passed':True,'repo_checks':len(actual),'bindings':len(b)},sort_keys=True))
"""

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True,type=Path)
    target=ap.parse_args().output
    if not target.is_absolute() or target.exists(): raise ValueError('fresh absolute output file required')
    require(sha(ROOT/REPAIR/'manifest.json')==MANIFEST_SHA,'frozen manifest before controls')
    require(sha(ROOT/BASE/'portable_reproduce.py')==RUNNER_SHA,'frozen runner before controls')
    sys.path.insert(0,str(ROOT/BASE))
    import portable_reproduce as runner
    originals={loop:json.loads((ROOT/BASE/'reverse'/loop/'output/results.json').read_text()) for loop in runner.LOOPS}
    expected={loop:json.loads((ROOT/REPAIR/loop/'expected/results.json').read_text()) for loop in runner.LOOPS}
    # The minimal independently staged closure contains every producer runtime
    # file plus original/portable outputs, inventories and source helpers.
    paths=set()
    for loop in runner.LOOPS:
        paths.update(expected[loop]['bindings'])
        paths.update(str(p.relative_to(ROOT)) for p in (ROOT/REPAIR/loop/'expected').rglob('*') if p.is_file())
        paths.add(BASE+f'reverse/{loop}/output/results.json')
    runs=[]
    python=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])
    with tempfile.TemporaryDirectory(prefix='ym-ah-portability-independent-') as temp:
        work=Path(temp); stage=work/'unrelated-checkout'; stage.mkdir()
        for name in sorted(paths):
            src=ROOT/name; dst=stage/name; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
        require(not stage.is_relative_to(ROOT) and not ROOT.is_relative_to(stage),'independent unrelated staged root')
        validator=runner.Validator(stage)
        for loop in runner.LOOPS:
            # Full code replay, one per interpreter mode, under an unrelated
            # checkout and nonrepository cwd. Check the entire output tree.
            script=REPAIR+loop+'/check.py'; out=work/(loop+'-output')
            run=subprocess.run(python+[str(stage/script),'--output',str(out)],cwd=work,capture_output=True,text=True)
            require(run.returncode==0,'fresh full relocated '+loop+' replay')
            expected_dir=stage/REPAIR/loop/'expected'
            actual_files={str(p.relative_to(out)) for p in out.rglob('*') if p.is_file()}
            expected_files={str(p.relative_to(expected_dir)) for p in expected_dir.rglob('*') if p.is_file()}
            require(actual_files==expected_files,'entire relocated output set '+loop)
            require(all((out/n).read_bytes()==(expected_dir/n).read_bytes() for n in actual_files),'all relocated output bytes '+loop)
            runs.append({'loop':loop,'check_count':expected[loop]['check_count'],'bindings':len(expected[loop]['bindings']),
                         'outputs':{n:sha(out/n) for n in sorted(actual_files)},'absolute_entrypoint':True,
                         'unrelated_repository':True,'nonrepository_cwd':True,'passed':True})
            def probe():
                r=subprocess.run(python+['-c',PROBE,str(stage),loop],cwd=work,capture_output=True,text=True)
                if r.returncode: raise RuntimeError('Source-only probe rejected')
                return json.loads(r.stdout)
            require(probe()['repo_checks']==8,'all originals checked without old-root or installed reads '+loop)
            inv=json.loads((stage/BASE/'reverse'/loop/'inputs/instruction-inventory.json').read_text())
            entry=inv['repo-filtered-sources-and-connected-limits.md']
            original='.codex/skills/qeg-research-advisor/references/filtered-sources-and-connected-limits.md'
            contract=json.loads((stage/BASE/'contracts'/f'{loop}.json').read_text())
            require(original not in contract['sources'],'original mutation is not masked by contract verification '+loop)
            snapshot=BASE+f'reverse/{loop}/'+entry['snapshot']
            for kind,name in [('current-original',original),('owned-snapshot',snapshot),
                              ('historical-script',BASE+f'reverse/{loop}/check.py'),('executed-script',script)]:
                path=stage/name; data=path.read_bytes()
                path.write_bytes(data+b'\n# administrative mutation\n')
                try: rejected(loop+' rejects changed '+kind,probe)
                finally: path.write_bytes(data)
                if kind in ('current-original','owned-snapshot'):
                    path.unlink()
                    try: rejected(loop+' rejects missing '+kind,probe)
                    finally: path.write_bytes(data)
            # Mapping semantics are exercised directly using the exact runner
            # resolver and a local source-validating inventory fixture.
            class InventoryFixture(runner.Validator):
                def load(self,name): return copy.deepcopy(self.fixture)
            fixture=InventoryFixture(stage)
            for kind in ['missing','foreign','traversal','unsupported','misclassified']:
                d=copy.deepcopy(inv); key='repo-filtered-sources-and-connected-limits.md'
                if kind=='missing': del d[key]
                elif kind=='foreign': d[key]['origin']='/tmp/foreign-instruction.md'
                elif kind=='traversal': d[key]['origin']=str(runner.LEGACY_ROOT/'.codex/skills/qeg-research-advisor/references/../escape.md')
                elif kind=='unsupported': d[key]['origin']=str(runner.LEGACY_ROOT/'unsupported.md')
                else: d['external-disguised']=d.pop(key)
                fixture.fixture=d
                rejected(loop+' rejects '+kind+' origin mapping',lambda:runner.repository_origins(fixture,loop))
            path=stage/original; data=path.read_bytes(); path.unlink(); path.symlink_to(ROOT/original)
            try: rejected(loop+' rejects linked current-root original',lambda:runner.repository_origins(validator,loop))
            finally: path.unlink();path.write_bytes(data)
            # Full typed result comparison rejects even a Boolean/integer swap.
            for kind in ['removed-check','changed-count','changed-binding','missing-executed-binding','typed-flag']:
                d=copy.deepcopy(expected[loop])
                if kind=='removed-check': del d['checks'][next(iter(d['checks']))]
                elif kind=='changed-count': d['check_count']-=8
                elif kind=='changed-binding': d['bindings'][BASE+f'reverse/{loop}/check.py']='0'*64
                elif kind=='missing-executed-binding': del d['bindings'][script]
                else: d['all_checks_passed']=1
                rejected(loop+' rejects '+kind+' result',lambda:runner.payload_relation(originals[loop],d,script,sha(stage/script)))
            artifacts={n:sha(expected_dir/n) for n in expected_files if n!='results.json'}
            (out/'extra.txt').write_text('administrative fixture')
            try: rejected(loop+' rejects extra output',lambda:runner.replay_artifacts(out,expected_dir,artifacts))
            finally: (out/'extra.txt').unlink()
            data=(out/'results.json').read_bytes();(out/'results.json').unlink()
            try: rejected(loop+' rejects missing result output',lambda:runner.replay_artifacts(out,expected_dir,artifacts))
            finally: (out/'results.json').write_bytes(data)
            if artifacts:
                name=next(iter(artifacts));data=(out/name).read_bytes();(out/name).write_bytes(data+b' ')
                try: rejected(loop+' rejects changed sidecar',lambda:runner.replay_artifacts(out,expected_dir,artifacts))
                finally: (out/name).write_bytes(data)
        require(all(sha(stage/n)==sha(ROOT/n) for n in paths),'all staged source mutations restored exactly')
    result={'schema':'ym28-ah-portability-independent-controls-v1','passed':True,'check_count':len(checks),
            'checks':checks,'mutation_count':len(mutations),'mutations':mutations,'full_relocated_runs':runs,
            'interpreter_mode_recorded_separately':True,'old_root_and_installed_origin_reads_prohibited_in_source_probes':True,
            'original_repository_mutated':False,'new_research_loops':0,'scope':'Administrative source/path/output controls; full unchanged mathematical checkers replayed only once per loop per interpreter mode.',
            'bindings':{BASE+'portable_reproduce.py':RUNNER_SHA,REPAIR+'manifest.json':MANIFEST_SHA,
                        str(Path(__file__).resolve().relative_to(ROOT)):sha(Path(__file__).resolve())}}
    target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'check_count':len(checks),'mutations':len(mutations),'sha256':sha(target)}))

if __name__=='__main__': main()
