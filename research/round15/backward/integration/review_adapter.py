"""Independent finite-rule replay, cold-admission and metadata mutation audit."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
SOURCE_BYTES=Path(__file__).read_bytes()
CASES={'A_complete_interval':'proved','B_cube_nonfactorization':'proved','C_improved_boundary':'proved',
 'A_missing_cover':'not_derivable','A_missing_derivative':'not_derivable','B_missing_graph':'not_derivable',
 'B_missing_tail':'not_derivable','C_missing_graph':'not_derivable','C_missing_minmax':'not_derivable',
 'C_missing_trial_moments':'not_derivable','C_missing_interval':'not_derivable',
 'original_uniform_goal':'not_derivable','unmatched_generator':'not_derivable','four_dimensional_yang_mills':'not_derivable'}


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module);return module


def serial(value):return json.dumps(value,sort_keys=True,allow_nan=False,separators=(',',':'))


def saturate(library):
    known=set(library['initial_facts']);changed=True
    while changed:
        changed=False
        for rule in library['rules']:
            if set(rule['premises'])<=known and rule['conclusion'] not in known:
                known.add(rule['conclusion']);changed=True
    return set(library['goals'])<=known


def replay(library,proof):
    if type(proof) is not dict or proof.get('passed') is not True or type(proof.get('steps')) is not list:raise ValueError('checked proof steps required')
    known=set(library['initial_facts']);rules={r['id']:r for r in library['rules']};cost=0
    for step in proof['steps']:
        if type(step) is not dict or set(step)!={'rule_id','premises','conclusion','cost'}:raise ValueError('strict proof step schema')
        rule=rules.get(step['rule_id'])
        if rule is None or serial(step)!=serial({'rule_id':rule['id'],'premises':rule['premises'],'conclusion':rule['conclusion'],'cost':rule['cost']}):raise ValueError('step differs from reviewed rule')
        if not set(rule['premises'])<=known:raise ValueError('ordered step missing premise')
        known.add(rule['conclusion']);cost+=rule['cost']
    if not set(library['goals'])<=known or proof.get('final_facts')!=sorted(known) or type(proof.get('cost')) is not int or proof['cost']!=cost:raise ValueError('incomplete ordered proof or cost metadata')
    return cost


def clone(root,frozen):
    for name,data in frozen.items():
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)


def audit(round_dir,output_dir):
    root=Path(round_dir);adapter_bytes=(root/'proof_routes.py').read_bytes();inventory_bytes=(root/'proof_inputs.json').read_bytes();replay_bytes=(root/'replay_evidence.py').read_bytes()
    module=load(root/'proof_routes.py','ym15_independent_adapter_review');frozen=module.snapshot()
    result_bytes=(root/'proof_results.json').read_bytes();saved=json.loads(result_bytes);checks=[]
    def gate(name,test=True):
        if not test:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    gate('saved proof report binds actual adapter bytes',saved.get('adapter_sha256')==hashlib.sha256(adapter_bytes).hexdigest())
    gate('complete input inventory and report hashes match',saved['source_sha256']==json.loads(inventory_bytes)=={n:hashlib.sha256(v).hexdigest() for n,v in frozen.items()})
    gate('exact14 route set retained',set(saved['routes'])==set(CASES))
    for name,expected in CASES.items():
        route=saved['routes'][name];library=route['library'];result=route['result']
        gate(name+' independent saturation agrees',saturate(library)==(expected=='proved') and result['status']==expected)
        gate(name+' no open premise admitted',not(set(library['initial_facts'])&module.OPEN))
        if expected=='proved':
            cost=replay(library,result['certified_proof']);meeting=replay(library,result['first_meeting_candidate'])
            events={(row.get('phase'),row.get('event')) for row in result['search_trace']}
            gate(name+' actual two fronts and independent ordered replay',('bidirectional','forward_pop') in events and ('bidirectional','backward_pop') in events and cost==result['certified_cost'] and meeting>=cost)
    # Reconstruct each positive library with fresh independent scientific admission.
    for name,target in [('A_complete_interval','interval_positive'),('B_cube_nonfactorization','cube_nonfactorization'),('C_improved_boundary','improved_boundary')]:
        library,accepted=module.library(frozen,target)
        gate(name+' cold library matches saved exact rules',serial(library)==serial(saved['routes'][name]['library']) and accepted['status']=='passed')
    library,accepted=module.library(frozen,'ym_gap')
    gate('cold scientific success cannot admit outer Yang-Mills premises',not library['initial_facts'] and not saturate(library))
    uniform=saved['routes']['original_uniform_goal']['library']['rules'][0]
    gate('uniform route requires actual common physical scale and smallness',set(uniform['premises'])=={'local_uniform_constants','volume_family_contract','uniform_energy_scale','uniform_smallness'})
    outer=next(r for r in library['rules'] if r['id']=='y01')
    gate('continuum route includes controlled spectral limit',set(outer['premises'])=={'uniform_gap','matched_generator','continuum_axioms','nontrivial_limit','controlled_spectral_limit'})
    def rejected(name,call):
        try:call()
        except(ValueError,TypeError,KeyError):gate(name);return
        raise ValueError('mutation accepted '+name)
    rejected('caller passed record cannot serve as frozen evidence',lambda:module.library({'status':'passed','gates':list(module.GATES)},'interval_positive'))
    rejected('empty source mapping rejected',lambda:module.library({},'interval_positive'))
    missing=dict(frozen);missing.pop('backward/A1/derivative-proof.md')
    rejected('one required frozen input omitted',lambda:module.library(missing,'interval_positive'))
    changed=dict(frozen);changed['forward/C2/output/central_certificate.json']+=b'\n'
    rejected('changed frozen scientific evidence rejected',lambda:module.library(changed,'improved_boundary'))
    rejected('unexpected removal rejected',lambda:module.library(frozen,'interval_positive',('ym_gap',)))
    rejected('duplicate removed premise rejected',lambda:module.library(frozen,'interval_positive',('cover_gate','cover_gate')))
    for attribute,mutation in [
      ('HYPOTHESES',lambda value:frozenset(set(value)|{'matched_generator'})),
      ('GATES',lambda value:frozenset(set(value)|{'matched_generator'})),
      ('OPEN',lambda value:frozenset(set(value)-{'matched_generator'})),
      ('STATEMENTS',lambda value:{**value,'interval_positive':'The four-dimensional Millennium problem is solved.'}),
      ('RULES',lambda value:tuple(value)+(('injected',('finite_measure',),'ym_gap'),)),
    ]:
        previous=getattr(module,attribute);setattr(module,attribute,mutation(previous))
        try:rejected('in-memory '+attribute+' declaration mutation',lambda:module.library(frozen,'matched_generator'))
        finally:setattr(module,attribute,previous)
    # Disk mutation tests run in a complete isolated copy; the project remains untouched.
    with tempfile.TemporaryDirectory(prefix='ym15-adapter-review-',dir=root.parents[2]) as temp:
        isolated=Path(temp)/'research/round15';isolated.mkdir(parents=True);clone(isolated,frozen)
        (isolated/'proof_routes.py').write_bytes(adapter_bytes);(isolated/'proof_inputs.json').write_bytes(inventory_bytes)
        own=load(isolated/'proof_routes.py','ym15_isolated_adapter_review');own.snapshot()
        source=isolated/'backward/A1/derivative-proof.md';original=source.read_bytes();source.write_bytes(original+b'\n')
        rejected('fresh snapshot rejects changed source after warm load',own.snapshot);source.write_bytes(original)
        source.unlink();rejected('fresh snapshot rejects missing required input',own.snapshot);source.write_bytes(original)
        copy_path=isolated/'alias.md';copy_path.write_bytes(original);source.unlink();source.symlink_to(copy_path)
        rejected('fresh snapshot rejects symlink substitution',own.snapshot);source.unlink();source.write_bytes(original)
        manifest=json.loads(inventory_bytes);manifest.pop('backward/A1/derivative-proof.md');(isolated/'proof_inputs.json').write_text(json.dumps(manifest))
        rejected('shortened inventory cannot authorize missing proof',own.snapshot);(isolated/'proof_inputs.json').write_bytes(inventory_bytes)
        # Independently test the scientific subprocess itself, beyond hash rejection.
        cp=isolated/'forward/C2/output/central_certificate.json';c=json.loads(cp.read_bytes());c['certified_gap_lower']='99';cp.write_text(json.dumps(c))
        output=isolated/'bad-replay.json';proc=subprocess.run([sys.executable,str(isolated/'replay_evidence.py'),str(output)],cwd=isolated,capture_output=True,text=True,timeout=120)
        gate('cold independent arithmetic rejects forged central lower bound',proc.returncode!=0 and not output.exists())
    # Ordered proof replay must reject even a forged passed=true certificate.
    goodlib=saved['routes']['A_complete_interval']['library'];proof=copy.deepcopy(saved['routes']['A_complete_interval']['result']['certified_proof'])
    proof['steps']=proof['steps'][1:];rejected('fake passed proof missing required ordered step',lambda:replay(goodlib,proof))
    proof=copy.deepcopy(saved['routes']['A_complete_interval']['result']['certified_proof']);proof['steps'][0]['conclusion']='ym_gap';rejected('step text cannot change reviewed conclusion',lambda:replay(goodlib,proof))
    gate('all scientific and adapter inputs unchanged at completion',module.snapshot()==frozen and (root/'proof_routes.py').read_bytes()==adapter_bytes and (root/'replay_evidence.py').read_bytes()==replay_bytes and (root/'proof_results.json').read_bytes()==result_bytes)
    output={'schema':'ym15-independent-proof-adapter-review-v1','status':'passed','checks_count':len(checks),'checks':checks,
       'reviewer_source_sha256':hashlib.sha256(SOURCE_BYTES).hexdigest(),'adapter_sha256':hashlib.sha256(adapter_bytes).hexdigest(),
       'replay_sha256':hashlib.sha256(replay_bytes).hexdigest(),'inventory_sha256':hashlib.sha256(inventory_bytes).hexdigest(),
       'proof_results_sha256':hashlib.sha256(result_bytes).hexdigest(),'frozen_inputs':len(frozen),'routes':len(CASES),
       'limits':['Finite reviewed Horn rules encode conventional proof obligations, not a formal proof-assistant kernel.',
                 'Two-front meetings and independently replayed ordered certificates are separate checks.',
                 'Original uniform and continuum premises remain absent; successful finite arithmetic does not supply them.']}
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True);(out/'independent_adapter_review.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks':len(checks),'routes':len(CASES)}));return output


if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: review_adapter.py ROUND15 OUTPUT_DIR')
    audit(*sys.argv[1:])
