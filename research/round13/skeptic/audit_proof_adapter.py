"""Independent round13 adapter audit; no scientific sources are edited.

Uses an independently implemented exhaustive Dijkstra/Horn solver and mutated
copies of frozen inputs. The scientific acceptance ledger remains unchanged.
"""
from pathlib import Path
import argparse,copy,hashlib,heapq,importlib.util,json,sys,tempfile
p=argparse.ArgumentParser();p.add_argument('adapter');p.add_argument('root');p.add_argument('--label',default='proof_adapter_normal');args=p.parse_args()
source=Path(args.adapter).resolve();root=Path(args.root).resolve();before=hashlib.sha256(source.read_bytes()).hexdigest()
spec=importlib.util.spec_from_file_location('proof_routes',source);m=importlib.util.module_from_spec(spec);sys.modules['proof_routes']=m;spec.loader.exec_module(m)
checks=[];failures=[]
def check(name,ok,detail=''):
    row={'name':name,'status':'passed' if ok else 'failed','detail':detail};checks.append(row)
    if not ok:failures.append(row)
def reject(name,f):
    try:f()
    except (ValueError,TypeError,KeyError,RuntimeError):check(name,True);return
    check(name,False,'Unexpected acceptance')
def json_changed(frozen,key,edit):
    altered=dict(frozen);item=json.loads(altered[key]);edit(item);altered[key]=json.dumps(item).encode();return altered

def independent_cost(library):
    start=frozenset(library['initial_facts']);goal=library['goals'][0]
    queue=[(0,0,start)];best={start:0};counter=0
    while queue:
        cost,_,state=heapq.heappop(queue)
        if best[state]!=cost:continue
        if goal in state:return cost
        for r in library['rules']:
            if r['conclusion'] not in state and set(r['premises'])<=state:
                nxt=state|{r['conclusion']};value=cost+r['cost']
                if value<best.get(nxt,float('inf')):
                    best[nxt]=value;counter+=1;heapq.heappush(queue,(value,counter,nxt))
    return None

with tempfile.TemporaryDirectory(prefix='proof-adapter-audit-',dir=Path(__file__).resolve().parent) as tmp:
    tmp=Path(tmp);m.HERE=tmp
    frozen={name:m.read_regular(root,name) for name in m.EXPECTED}
    frozen['proof_routes.py']=source.read_bytes()
    for name,raw in frozen.items():
        f=tmp/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(raw)
    mspec=importlib.util.spec_from_file_location('maker',source.with_name('make_proof_manifest.py'));maker=importlib.util.module_from_spec(mspec);mspec.loader.exec_module(maker)
    maker.create(tmp)
    manifest,original=m.checked_inputs(tmp);check('manifest_exact_set',set(manifest['sha256'])==m.EXPECTED)
    replay=m.replay_evidence(original,tmp);check('full_frozen_replay',replay['status']=='passed')
    search=m.load_frozen('independent_adapter_search','proof_search.py',original,tmp)
    statuses={}
    for name,goal,hyps,gates,expected in m.route_specs():
        lib,opt=m.make_library(original,replay,goal,hyps,gates)
        cost=independent_cost(lib);actual=search.plan(lib,max_states=10000,max_backward_states=10000)
        statuses[name]=actual['status']
        check('independent_horn_'+name,(cost is not None)==(expected=='proved') and actual['status']==expected and (cost is None or cost==actual['certified_cost']))
        if cost is not None:
            steps=actual['certified_proof']['steps'];state=set(lib['initial_facts']);total=0
            known={r['id']:r for r in lib['rules']}
            for step in steps:
                r=known[step['rule_id']]
                if not set(r['premises'])<=state:raise RuntimeError('Invalid explicit ordered certificate')
                state.add(r['conclusion']);total+=r['cost']
            check('independent_ordered_replay_'+name,goal in state and total==cost)
    for key in ['stability_without_smallness','canonical_gap_without_smallness','finite_constraints_not_all_orders','finite_optimizer_slack_not_asymptotic','four_dimensional_mass_gap']:
        check('critical_negative_'+key,statuses[key]=='not_derivable')
    loc={'link_tensor','onsite_selfadjoint','bounded_plaquettes','bounded_incidence','gauge_invariance'}
    for withdrawn in ['onsite_selfadjoint','bounded_plaquettes','bounded_incidence']:
        lib,_=m.make_library(original,replay,'bounded_local_volume_limit',loc-{withdrawn},{'path_count','boundary_shell_sum'})
        check('withdraw_locality_'+withdrawn,independent_cost(lib) is None)
    for invalid in ['yang_mills_4d_gap','hierarchy_unique','uniform_physical_hamiltonian_gap','uniform_physical_decay']:
        reject('invalid_seed_'+invalid,lambda invalid=invalid:m.make_library(original,replay,'yang_mills_4d_gap',[invalid],[]))
    reject('hypothesis_cannot_be_gate',lambda:m.make_library(original,replay,'hierarchy_unique',['compact_measure'],['all_order_constraints']))

    # The independently found stale-input bug must be closed after a real replay.
    mutated=json_changed(original,'advisor/inference_rules.json',lambda d:next(r for r in d['rules'] if r['id']=='M8').update(premises=['compact_measure']))
    reject('post_replay_rule_mutation',lambda:m.make_library(mutated,replay,'hierarchy_unique',['compact_measure'],[]))
    reject('recomputed_fingerprint_unreviewed_rule',lambda:m.make_library(mutated,{**replay,'frozen_input_sha256':m.frozen_fingerprint(mutated)},'hierarchy_unique',['compact_measure'],[]))
    mutated=json_changed(original,'moments/output/certificates.json',lambda d:d['certificates'][0].update(variance_interval=['0','0']))
    reject('post_replay_certificate_mutation',lambda:m.make_library(mutated,replay,'moment_outer_interval',['compact_measure'],['rational_exclusion_gate']))
    mutated=json_changed(original,'response/output/results.json',lambda d:d.update(check_count=0,checks=[]))
    reject('post_replay_report_mutation',lambda:m.make_library(mutated,replay,'susceptibility_identity',['compact_measure','exponential_family_differentiation'],[]))
    mutated=json_changed(original,'skeptic/acceptance.json',lambda d:d.update(status='pending'))
    reject('post_replay_acceptance_mutation',lambda:m.make_library(mutated,replay,'moment_outer_interval',['compact_measure'],['rational_exclusion_gate']))
    reject('recomputed_fingerprint_pending_ledger',lambda:m.make_library(mutated,{**replay,'frozen_input_sha256':m.frozen_fingerprint(mutated)},'moment_outer_interval',['compact_measure'],['rational_exclusion_gate']))
    reject('missing_replay_provenance',lambda:m.make_library(original,{'status':'passed','gates':sorted(m.GATES),'reviewed_rule_ids':replay['reviewed_rule_ids']},'moment_outer_interval',['compact_measure'],['rational_exclusion_gate']))

    a=tmp/'advisor/advisor.md';raw=a.read_bytes();a.write_bytes(raw+b'changed')
    reject('disk_source_changed',lambda:m.checked_inputs(tmp))
    reject('manifest_builder_stale_review',lambda:maker.create(tmp));a.write_bytes(raw)
    # File and intermediate-directory symlinks are both rejected.
    a.unlink();a.symlink_to(root/'advisor/advisor.md');reject('file_symlink',lambda:m.checked_inputs(tmp));a.unlink();a.write_bytes(raw)
    saved=tmp/'advisor_saved';(tmp/'advisor').rename(saved);(tmp/'advisor').symlink_to(saved,target_is_directory=True)
    reject('directory_symlink',lambda:m.checked_inputs(tmp));(tmp/'advisor').unlink();saved.rename(tmp/'advisor')
    mf=tmp/'proof_manifest.json';mfraw=mf.read_bytes();mf.unlink();mf.symlink_to(root/'proof_manifest.json')
    reject('manifest_symlink',lambda:m.checked_inputs(tmp));reject('builder_manifest_symlink',lambda:maker.create(tmp));mf.unlink();mf.write_bytes(mfraw)
    for path in ['../escape','/etc/passwd','']:
        reject('relative_path_contract_'+repr(path),lambda path=path:m.read_regular(tmp,path))
    changed=json.loads(mfraw);changed['sha256']['proof_search.py']='0'*64;mf.write_text(json.dumps(changed));reject('digest_mismatch',lambda:m.checked_inputs(tmp));mf.write_bytes(mfraw)
    core=tmp/'proof_search.py';core.write_bytes(core.read_bytes()+b'\n#changed\n');changed=json.loads(mfraw);changed['sha256']['proof_search.py']=m.digest(core.read_bytes());mf.write_text(json.dumps(changed))
    reject('rehash_historical_core',lambda:m.checked_inputs(tmp))

check('adapter_unchanged',hashlib.sha256(source.read_bytes()).hexdigest()==before)
hashes={name:hashlib.sha256(source.with_name(name).read_bytes()).hexdigest() for name in ['proof_routes.py','make_proof_manifest.py','test_proof_routes.py','proof_search.py']}
out={'status':'passed' if not failures else 'failed','count':len(checks),'checks':checks,'failures':failures,'reviewed_source_hashes':hashes,'scope':'Independent adapter admission, exhaustive Dijkstra/Horn route comparison and ordered replay. This does not replace scientific acceptance or create missing mathematical premises.'}
Path(__file__).with_name(args.label+'_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'count':len(checks),'failures':failures},indent=2))
if failures:raise SystemExit(1)
