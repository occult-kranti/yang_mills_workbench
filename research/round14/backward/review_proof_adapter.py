#!/usr/bin/env python3
"""Independent isolated round14 adapter review, using actual scientific bytes.

A synthetic review gate enables testing before root creates its final handoff.
It is labelled as such and is never offered as scientific reviewer authority.
"""
from pathlib import Path
import contextlib
import hashlib
import io
import itertools
import json
import sys
import tempfile
import types


def digest(raw):return hashlib.sha256(raw).hexdigest()


def saturate(nodes,rules):
    known=set(nodes)
    while True:
        extra={c for _,p,c in rules if set(p)<=known}-known
        if not extra:return known
        known.update(extra)


def main(project_round,producer_dir,output_dir):
    project_round=Path(project_round).resolve();producer_dir=Path(producer_dir).resolve()
    own=Path(__file__).resolve().parent;output_dir=Path(output_dir).resolve()
    output_dir.mkdir(parents=True,exist_ok=True)
    adapter=(project_round/'proof_routes.py').read_bytes()
    bundle=json.loads((producer_dir/'loop2_output/certificates.json').read_text())
    central=next(e['certificate'] for e in bundle['certificates']
       if e['certificate']['parameters']=={'k1':'1','k2':'1','eta':'1/4'} and e['certificate']['degree']==24)
    inputs={
      'proof_routes.py':adapter,
      'proof_search.py':(project_round/'proof_search.py').read_bytes(),
      'central-certificate.json':(json.dumps(central,indent=2)+'\n').encode(),
      'forward/loop2_certificate.py':(producer_dir/'loop2_certificate.py').read_bytes(),
      'backward/verify_certificate.py':(own/'verify_certificate.py').read_bytes(),
      'backward/oracle.py':(own/'oracle.py').read_bytes(),
      'advisor/loop1_gate.json':(project_round/'advisor/loop1_gate.json').read_bytes(),
    }
    rule_ids=['r'+str(i).zfill(2) for i in range(1,12)]
    review_gate={'status':'accepted within declared finite-model scope','reviewed_rule_ids':rule_ids,
      'source_sha256':{n:digest(inputs[n]) for n in [
          'forward/loop2_certificate.py','backward/verify_certificate.py','backward/oracle.py',
          'central-certificate.json','proof_routes.py']},
      'test_fixture_only':'Synthetic isolated review gate; not the final advisor acceptance record.'}
    inputs['advisor/loop2_gate.json']=(json.dumps(review_gate,indent=2)+'\n').encode()
    checks=[]
    def gate(name,condition,details=None):
        if not condition:raise ValueError(name)
        checks.append({'name':name,'passed':True,'details':details})
    def rejected(name,fn):
        try:fn()
        except (ValueError,TypeError):gate(name,True);return
        raise ValueError('unexpected acceptance: '+name)
    with tempfile.TemporaryDirectory(prefix='adapter-review-',dir=own) as directory:
        tmp=Path(directory)
        for n,raw in inputs.items():
            path=tmp/n;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
        (tmp/'proof_manifest.json').write_text(json.dumps({'sha256':{n:digest(b) for n,b in inputs.items()}})+'\n')
        module=types.ModuleType('independent_reviewed_adapter');module.__file__=str(tmp/'proof_routes.py')
        sys.modules[module.__name__]=module
        exec(compile(adapter,module.__file__,'exec'),module.__dict__)
        snapshot=module.snapshot(tmp);accepted=module.replay(snapshot)
        gate('actual independent central replay succeeds',accepted['status']=='passed')
        gate('all eleven reviewed rules have exact IDs',[r[0] for r in module.RULES]==rule_ids)
        with contextlib.redirect_stdout(io.StringIO()):
            result=module.execute(output_dir/'independent_proof_routes.json')
        gate('actual two-front routes complete',result['status']=='passed' and len(result['routes'])==11)
        for name,route in result['routes'].items():
            lib=route['library'];proof=route['result']
            known=saturate(lib['initial_facts'],[(r['id'],r['premises'],r['conclusion']) for r in lib['rules']])
            expect=all(goal in known for goal in lib['goals'])
            gate('independent reachability '+name,(proof['status']=='proved')==expect)
            if expect:
                gate('separate ordered replay '+name,proof['independent_ordered_replay']['passed'] is True)
                gate('two-front meeting recorded '+name,proof['first_meeting_candidate']['passed'] is True)
        # Enumerate every subset of the seven seed facts; compare independent
        # forward saturation to the necessary all-seeds condition for this DAG.
        atoms=sorted(module.HYPOTHESES|module.GATES);tested=0
        for size in range(len(atoms)+1):
            for seed in itertools.combinations(atoms,size):
                result_set=saturate(seed,module.RULES)
                if ('central_positive' in result_set)!=(set(seed)==set(atoms)):
                    raise ValueError('unexpected hidden premise or bypass in rule DAG')
                if 'yang_mills_gap' in result_set:
                    raise ValueError('finite seed family reached continuum target')
                tested+=1
        gate('all128 seed subsets respect finite and continuum obligations',tested==128)
        fake={n:b'' for n in module.INPUTS}
        forged={'status':'passed','frozen_sha256':module.fingerprint(fake),'gates':sorted(module.GATES)}
        rejected('original forged-empty-snapshot bypass blocked',lambda:module.library(fake,forged))
        forged=dict(accepted);forged['interval']=['0','1']
        rejected('forged accepted interval blocked',lambda:module.library(snapshot,forged))
        original_rules=module.RULES
        module.RULES=original_rules+(('injected',('measure',),'yang_mills_gap'),)
        rejected('original in-memory rule injection blocked',lambda:module.library(snapshot,accepted,goal='yang_mills_gap'))
        module.RULES=original_rules
        rejected('unproved physical premise cannot be a hypothesis seed',
                 lambda:module.library(snapshot,accepted,hypotheses={'measure','matched_generator'}))
        rejected('target cannot be a gate seed',
                 lambda:module.library(snapshot,accepted,gates=set(module.GATES)|{'central_positive'}))
        rejected('duplicate hypothesis seed blocked',
                 lambda:module.library(snapshot,accepted,hypotheses=['measure','measure']))
        missing=dict(snapshot);missing.pop('central-certificate.json')
        rejected('incomplete frozen evidence blocked',lambda:module.replay(missing))
        changed=dict(snapshot);bad_gate=json.loads(changed['advisor/loop2_gate.json']);bad_gate['reviewed_rule_ids'].remove('r09')
        changed['advisor/loop2_gate.json']=json.dumps(bad_gate).encode()
        rejected('missing reviewed rule blocked',lambda:module.replay(changed))
        changed=dict(snapshot);bad_gate=json.loads(changed['advisor/loop2_gate.json']);bad_gate['source_sha256']['proof_routes.py']='0'*64
        changed['advisor/loop2_gate.json']=json.dumps(bad_gate).encode()
        rejected('reviewed adapter hash mismatch blocked',lambda:module.replay(changed))
        changed=dict(snapshot);bad=json.loads(changed['central-certificate.json']);bad['enclosures']['covariance']=['1','2']
        changed['central-certificate.json']=json.dumps(bad).encode()
        bad_gate=json.loads(changed['advisor/loop2_gate.json']);bad_gate['source_sha256']['central-certificate.json']=digest(changed['central-certificate.json'])
        changed['advisor/loop2_gate.json']=json.dumps(bad_gate).encode()
        rejected('rehashed false interval still fails exact replay',lambda:module.replay(changed))
        lib=module.library(snapshot,accepted)
        rejected('proof cannot omit its first dependency',lambda:module.ordered_replay(lib,['r10']))
        rejected('unknown proof rule blocked',lambda:module.ordered_replay(lib,['not_a_rule']))
        outer=module.library(snapshot,accepted,goal='yang_mills_gap')
        gate('outer goal and implication have physical-continuum scope',
             all(n['scope']=='R14-physical-continuum' for n in outer['nodes']) and
             all(r['scope']=='R14-physical-continuum' for r in outer['rules']))
        gate('central full route has ten separately replayed rules',
             result['routes']['certified_positive_covariance']['result']['independent_ordered_replay']['steps']==10)
        rejected('path traversal input rejected',lambda:module.read(tmp,'../oracle.py'))
        manifest=tmp/'proof_manifest.json';saved=manifest.read_bytes();manifest.unlink();manifest.symlink_to(tmp/'advisor/loop2_gate.json')
        rejected('symlink manifest rejected',lambda:module.snapshot(tmp));manifest.unlink();manifest.write_bytes(saved)
    gate('reviewed adapter unchanged during review',(project_round/'proof_routes.py').read_bytes()==adapter)
    report={'schema':'ym14-independent-proof-adapter-review-v1','status':'passed','phase':'loop2',
      'check_count':len(checks),'checks':checks,'source_sha256':digest(Path(__file__).read_bytes()),
      'reviewed_rule_ids':rule_ids,'reviewed_source_hashes':{
          'proof_routes.py':digest(adapter),'proof_search.py':digest(inputs['proof_search.py']),
          'backward/verify_certificate.py':digest(inputs['backward/verify_certificate.py']),
          'backward/oracle.py':digest(inputs['backward/oracle.py']),
          'forward/loop2_certificate.py':digest(inputs['forward/loop2_certificate.py'])},
      'test_gate_policy':'Synthetic isolated test gate, clearly labelled; root must issue its actual second-loop gate after this handoff.',
      'acceptance':'Eleven conventional rules reviewed; two-front finite routes and independent ordered/reachability replay pass; observed admission bypasses blocked.',
      'limits':['Rule implications are conventional mathematical arguments, not a formal proof kernel.',
                'Only finite covariance claims are derived; physical-generator and continuum targets remain blocked.']}
    (output_dir/'independent_proof_adapter_review.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'passed','check_count':len(checks),'adapter_sha256':digest(adapter),'reviewed_rule_ids':rule_ids}))


if __name__=='__main__':
    if len(sys.argv)!=4:raise SystemExit('usage: review_proof_adapter.py PROJECT_ROUND PRODUCER_DIR OUTPUT')
    main(*sys.argv[1:])
