#!/usr/bin/env python3
"""Independent source-bound audit of the additive AH portability repair.

Fresh absolute --output FILE; deterministic under normal/optimized Python.
No producer arithmetic or release validation implementation is imported.
Administrative replay/mutation evidence is verified, not reexecuted here.
"""
import argparse
import ast
import difflib
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE='research/round28/'
REPAIR=BASE+'release/ah-portability/'
MANIFEST=REPAIR+'manifest.json'
EXPECTED='f2032dd55e5c2ffce75a76147e20aae8d769f27fdb3db3bcb2a9af7157f18671'
LEGACY=Path('/workspace/scratch/9daefcf0521b/yang_mills_workbench')
checks=[]
bindings={}

def require(ok,label):
    if not ok: raise ValueError(label)
    checks.append(label)

def path(name):
    p=Path(name)
    if p.is_absolute() or '..' in p.parts: raise ValueError('Unsafe evidence path: '+name)
    q=ROOT/p
    if not q.is_file() or any(x.is_symlink() for x in [q,*q.parents] if x.is_relative_to(ROOT)):
        raise ValueError('Missing or linked evidence: '+name)
    return q

def sha(name):return hashlib.sha256(path(name).read_bytes()).hexdigest()
def read(name):return json.loads(path(name).read_text())
def typed(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)
def bind(name,digest):
    require(sha(name)==digest,'Exact evidence '+name)
    if name in bindings: require(bindings[name]==digest,'Consistent evidence '+name)
    bindings[name]=digest

def fullset(folder):
    p=ROOT/folder
    items=list(p.rglob('*'))
    require(not any(x.is_symlink() for x in [p,*items]),'No linked evidence tree '+folder)
    return {str(x.relative_to(p)) for x in items if x.is_file()}

def inverse_transform(original,portable,loop,mapping):
    # Independent reversal of the three fully reviewed source edits; whole-text
    # equality then covers every mathematical definition and output statement.
    header='ROOT = Path(__file__).resolve().parents[5]\nHERE = ROOT / '+repr(BASE+'reverse/'+loop)
    header+='\nREPOSITORY_ORIGINS = '+json.dumps(mapping,indent=4,sort_keys=True)+'\n'
    changes=[(header,'HERE = Path(__file__).resolve().parent\nROOT = HERE.parents[3]\n')]
    if loop=='ah1':
        changes += [('        if e["origin"] in REPOSITORY_ORIGINS:\n            original = ROOT / REPOSITORY_ORIGINS[e["origin"]]',
                     '        if original.is_relative_to(ROOT):'),
                    ('    bindings[str(Path(__file__).resolve().relative_to(ROOT))] = sha(Path(__file__).resolve())\n','')]
    else:
        changes[0]=(header,'HERE=Path(__file__).resolve().parent\nROOT=HERE.parents[3]\n')
        changes += [('        if e["origin"] in REPOSITORY_ORIGINS:\n            origin=ROOT/REPOSITORY_ORIGINS[e["origin"]]',
                     '        if origin.is_relative_to(ROOT):'),
                    ('    bindings[str(Path(__file__).resolve().relative_to(ROOT))]=sha(Path(__file__).resolve())\n','')]
    recovered=portable
    for changed,initial in changes:
        require(recovered.count(changed)==1,'Unique reviewed source edit '+loop)
        recovered=recovered.replace(changed,initial,1)
    require(recovered==original,'Entire scientific source unchanged outside declared repair '+loop)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path)
    target=ap.parse_args().output
    if not target.is_absolute() or target.exists():raise ValueError('Fresh absolute output file required')
    bind(MANIFEST,EXPECTED)
    manifest=read(MANIFEST)
    require(manifest['schema']=='ym28-ah-portability-manifest-v1','Exact repair schema')
    require(type(manifest['new_research_loops']) is int and manifest['new_research_loops']==0,'Administrative zero-loop scope')
    require(set(manifest['substitutions'])=={'ah1','ah2'},'Only two AH reverse substitutions')
    require(len(manifest['bindings'])==3012,'Complete 3012-member approved proposal closure')
    for name,h in manifest['bindings'].items():bind(name,h)
    require(manifest['bindings'][BASE+'portable_reproduce.py']=='1feccf9a737b5ee04f7105907224746805b4fb1c56a2ceefe8213d1ce29a514c','Exact executed additive runner')
    require(manifest['bindings'][BASE+'reproduce.py']=='6ebf9b5116aba99cae5432796b890745872d7785d1bdedd8afee17d2a517b5fd','Original reproducibility machinery unchanged')
    require(manifest['bindings'][BASE+'release/admitted.json']=='5280e49631cdabf646edc1ff3e494a59ddb513ebbb96a0a102f3e551a7ade078','Original admission registry unchanged')
    requirements=BASE+'skeptic/ah-portability-requirements.json'
    bind(requirements,'b56cd1b82e3dbfb728f4086f5e637a05c2e2547a7ebc9318348eab8f2fc617e2')
    for name,h in read(requirements)['bindings'].items():bind(name,h)
    require(BASE+'advisor/ah-portability-decision.md' in bindings,'Root decision explicitly bound')
    failure_folder=BASE+'advisor/ah-portability-failure/'
    for name in sorted(fullset(failure_folder)):require(failure_folder+name in bindings,'Preserved root failure evidence bound '+name)
    original_failure=read(BASE+'reverse/ah1/output/results.json')
    relocated_failure=read(failure_folder+'ah1-relocated-results.json')
    require(original_failure['check_count']==320 and relocated_failure['check_count']==312,'Original location defect observed as 320 to 312')
    omitted_checks=set(original_failure['checks'])-set(relocated_failure['checks'])
    require(omitted_checks=={'repo_instruction_original_%02d'%i for i in range(15,23)},'Exactly eight original instruction checks lost')
    require(len(set(original_failure['bindings'])-set(relocated_failure['bindings']))==6,'Exactly six old binding keys lost')
    for key in original_failure:
        if key not in {'checks','check_count','bindings'}:
            require(typed(original_failure[key])==typed(relocated_failure[key]),'Failed release preserved mathematical payload '+key)
    totals={}
    outputs={}
    for loop in ['ah1','ah2']:
        original_prefix=BASE+'reverse/'+loop+'/'
        portable_prefix=REPAIR+loop+'/'
        item=manifest['substitutions'][loop]
        require(item['original_script']==original_prefix+'check.py' and item['portable_script']==portable_prefix+'check.py'
                and item['original_output']==original_prefix+'output/results.json' and item['portable_output']==portable_prefix+'expected/results.json',
                'Exact declared execution interfaces '+loop)
        inventory=read(original_prefix+'inputs/instruction-inventory.json')
        require(len(inventory)==26,'All owned instruction snapshots '+loop)
        ordered=sorted(inventory.items()) if loop=='ah1' else list(inventory.items())
        entries=[];mapping={}
        for index,(name,e) in enumerate(ordered):
            snap=original_prefix+e['snapshot'];bind(snap,e['sha256'])
            origin=Path(e['origin'])
            if not name.startswith('repo-'):
                require(not origin.is_relative_to(LEGACY),'Installed origin is metadata only '+loop+'/'+name)
                continue
            require(origin.is_absolute() and origin.is_relative_to(LEGACY),'Recorded original has historical repository provenance '+loop+'/'+name)
            relative=str(origin.relative_to(LEGACY))
            require(relative.startswith('.codex/skills/qeg-research-advisor/references/') and relative.endswith('.md') and '..' not in Path(relative).parts,'Safe current-root instruction mapping '+loop+'/'+name)
            bind(relative,e['sha256'])
            require(e['origin'] not in mapping,'Unique mapping '+loop+'/'+name)
            mapping[e['origin']]=relative
            entries.append({'instruction':name,'index':index,**e,'repository_path':relative,
                            'original_check':('repo_instruction_original_' if loop=='ah1' else 'repo_instruction_')+f'{index:02}'})
        require(len(mapping)==8 and typed(entries)==typed(item['repository_origins']),'Complete exact eight-entry mapping '+loop)
        original_text=path(item['original_script']).read_text();portable_text=path(item['portable_script']).read_text()
        parsed=ast.parse(portable_text)
        declarations=[n for n in parsed.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='REPOSITORY_ORIGINS' for t in n.targets)]
        require(len(declarations)==1 and ast.literal_eval(declarations[0].value)==mapping,'Executed literal map matches frozen sources '+loop)
        inverse_transform(original_text,portable_text,loop,mapping)
        expected_diff=''.join(difflib.unified_diff(original_text.splitlines(True),portable_text.splitlines(True),fromfile=item['original_script'],tofile=item['portable_script']))
        require(path(portable_prefix+'checker.diff').read_text()==expected_diff,'Complete truthful source diff '+loop)
        original=read(item['original_output']);portable=read(item['portable_output'])
        augmented=dict(original);augmented['bindings']={**original['bindings'],item['portable_script']:sha(item['portable_script'])}
        require(item['portable_script'] not in original['bindings'],'Executed script is separately identified '+loop)
        require(typed(portable)==typed(augmented),'Only actual executed-script binding differs '+loop)
        count=320 if loop=='ah1' else 717
        require(portable['check_count']==original['check_count']==item['original_check_count']==count,'All original check counts retained '+loop)
        require(len(original['bindings'])==(123 if loop=='ah1' else 108) and len(portable['bindings'])==(124 if loop=='ah1' else 109),'Exactly one additive provenance binding '+loop)
        require(all(portable['checks'].get(e['original_check']) is True for e in entries),'All original instruction checks retained '+loop)
        for name,h in portable['bindings'].items():bind(name,h)
        expected_files={'basis.json','graph.json','magnetic.json','results.json'} if loop=='ah1' else {'results.json'}
        require(fullset(original_prefix+'output')==fullset(portable_prefix+'expected')==expected_files,'Exact full output inventories '+loop)
        for name in sorted(expected_files-{'results.json'}):
            require(path(original_prefix+'output/'+name).read_bytes()==path(portable_prefix+'expected/'+name).read_bytes(),'Sidecar exact original bytes '+loop+'/'+name)
        frozen=read(original_prefix+'freeze.json')['files']
        require(set(frozen)==fullset(original_prefix)-{'freeze.json'},'Full unchanged original producer freeze '+loop)
        for name,h in frozen.items():bind(original_prefix+name,h)
        totals[loop]={'checks':count,'original_bindings':len(original['bindings']),'portable_bindings':len(portable['bindings']),'repository_original_checks':8}
        outputs[loop]={n:sha(portable_prefix+'expected/'+n) for n in sorted(expected_files)}
    evidence=read(REPAIR+'relocated-replay-evidence.json')
    require(evidence['status']=='passed' and evidence['producer_executions']==4 and evidence['additional_research_loops']==0,'Preserved proposal full relocation evidence')
    require({(r['loop'],r['mode']) for r in evidence['runs']}=={(l,m) for l in ['ah1','ah2'] for m in ['normal','optimized']},'All four proposal replay modes')
    for run in evidence['runs']:require(run['exit_code']==0 and run['outputs']==outputs[run['loop']],'Exact full proposal replay '+run['loop']+'/'+run['mode'])
    controlpath=BASE+'skeptic/ah-portability-controls.json'
    bind(controlpath,'63e57b79b83df217ee39b95a893fddbdc1584437d0344d0ef14b4f5b39e5b236')
    controls=read(controlpath)
    require(controls['passed'] is True and controls['check_count']==53 and controls['mutation_count']==39,'Independent targeted administrative controls')
    require(len(controls['mutations'])==39 and all(x['rejected'] is True for x in controls['mutations']),'All required negative controls reject')
    require(controls['old_root_and_installed_origin_reads_prohibited_in_source_probes'] is True and controls['original_repository_mutated'] is False,'No original mutation or old-origin runtime dependency')
    require(controls['new_research_loops']==0,'Control fixtures are not science investigations')
    for run in controls['full_relocated_runs']:
        require(run['passed'] is True and run['unrelated_repository'] is True and run['nonrepository_cwd'] is True and run['outputs']==outputs[run['loop']],'Independent full relocation '+run['loop'])
    for name,h in controls['bindings'].items():bind(name,h)
    receiptpath=BASE+'skeptic/ah-portability-controls-replay.json'
    bind(receiptpath,sha(receiptpath));receipt=read(receiptpath)
    require(receipt['passed'] is True and receipt['normal_optimized_byte_identical'] is True and receipt['failed_executions']==[],'Independent controls normal/optimized equality')
    require(len(receipt['runs'])==2 and {r['mode'] for r in receipt['runs']}=={'normal','optimized'},'Both independent control interpreter modes')
    require(all(r['exit_code']==0 and r['sha256']==sha(controlpath) for r in receipt['runs']),'Exact independent control output identity')
    preparation=BASE+'skeptic/ah-portability-audit-preparation.json'
    bind(preparation,sha(preparation));history=read(preparation)
    for name,h in history['bindings'].items():bind(name,h)
    require(history['both_executions_passed'] is True and history['normal_optimized_byte_identical'] is False
            and history['all_non_checklist_fields_equal'] is True and history['check_sets_equal'] is True,
            'Initial audit ordering-only mismatch preserved transparently')
    own=str(Path(__file__).resolve().relative_to(ROOT));bind(own,sha(own))
    result={'schema':'ym28-ah-portability-independent-audit-v1','accepted':True,'blocking_issues':[],
            'new_research_loops':0,'manifest':MANIFEST,'manifest_sha256':EXPECTED,
            'check_count':len(checks),'checks':checks,'bindings':dict(sorted(bindings.items())),
            'producer_counts':totals,'exact_expected_outputs':outputs,'independent_mutation_controls':39,
            'normal_optimized_administrative_evidence_equal':True,'old_origin_runtime_reads':False,
            'scientific_payload_or_original_source_changes':False,'provenance_delta':'Exactly one actual executed portable-checker binding per affected result; no removal or normalization.',
            'scope':'Source-bound administrative portability acceptance for only AH1/reverse and AH2/reverse; final new-commit all-twenty-per-mode release verification remains required.',
            'producer_or_release_arithmetic_imported':False,'producer_replays_repeated_by_this_audit':False}
    target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'accepted':True,'check_count':len(checks),'bindings':len(bindings),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()}))

if __name__=='__main__':main()
