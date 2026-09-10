"""Bounded independent Round17 source-admission and integration review."""
from pathlib import Path
from types import MappingProxyType
import argparse,copy,hashlib,importlib.util,json,subprocess,sys,tempfile

def digest(raw):return hashlib.sha256(raw).hexdigest()


def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module);return module


def serial(value):return json.dumps(value,sort_keys=True,allow_nan=False,separators=(',',':'))


def closure(library):
    known=set(library['initial_facts'])
    while True:
        following=known|{rule['conclusion'] for rule in library['rules'] if set(rule['premises'])<=known}
        if following==known:return set(library['goals'])<=known
        known=following


def ordered(library,proof):
    if type(proof) is not dict or proof.get('passed') is not True or type(proof.get('steps')) is not list:raise ValueError('checked ordered proof required')
    rules={r['id']:r for r in library['rules']};known=set(library['initial_facts']);cost=0
    for step in proof['steps']:
        if type(step) is not dict or set(step)!={'rule_id','premises','conclusion','cost'}:raise ValueError('proof step schema')
        rule=rules.get(step['rule_id'])
        if rule is None or serial(step)!=serial({'rule_id':rule['id'],'premises':rule['premises'],'conclusion':rule['conclusion'],'cost':rule['cost']}):raise ValueError('step differs from reviewed rule')
        if not set(rule['premises'])<=known:raise ValueError('step executed without premises')
        known.add(rule['conclusion']);cost+=rule['cost']
    if not set(library['goals'])<=known or proof.get('final_facts')!=sorted(known) or type(proof.get('cost')) is not int or proof['cost']!=cost:raise ValueError('incomplete proof or wrong cost')
    return cost


def copy_snapshot(root,frozen):
    for name,raw in frozen.items():
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)


CASES=[
 ('local_obstruction','relative_counterexample',(),'proved'),
 ('sparse_uniform_family','sparse_physical_gap',(),'proved'),
 ('finite_trial_bound','finite_gap_bound',(),'proved'),
 ('finite_endpoint_repair','finite_endpoint_repair',(),'proved'),
 ('central_projector','rank_three_projector',(),'proved'),
 ('conditional_channel_experiment','channel_contrast',(),'proved'),
 ('missing_local','relative_counterexample',('a1_gate',),'not_derivable'),
 ('missing_sparse','sparse_physical_gap',('a2_gate',),'not_derivable'),
 ('missing_scale','sparse_physical_gap',('common_scale',),'not_derivable'),
 ('overlapping_support','sparse_physical_gap',('sparse_support',),'not_derivable'),
 ('missing_trial','finite_gap_bound',('b1_gate',),'not_derivable'),
 ('missing_adjoint','finite_endpoint_repair',('b2_gate',),'not_derivable'),
 ('missing_endpoint','finite_endpoint_repair',('endpoint_trial',),'not_derivable'),
 ('missing_graph','rank_three_projector',('c1_gate',),'not_derivable'),
 ('missing_kernel','channel_contrast',('c2_gate',),'not_derivable'),
 ('original_dense_uniform_goal','dense_uniform_gap',(),'not_derivable'),
 ('full_bulk_integral','full_bulk_contraction',(),'not_derivable'),
 ('four_dimensional_yang_mills','ym_gap',(),'not_derivable')]


def audit(round_dir,output):
    root=Path(round_dir).resolve();out=Path(output).resolve()
    if out.is_relative_to(Path(__file__).resolve().parent):raise ValueError('review output outside frozen source required')
    out.mkdir(parents=True,exist_ok=False)
    names=('proof_routes.py','replay_evidence.py','proof_inputs.json','proof_search.py','proof_results.json','reproduce.py','advisor/freeze_gate.py','next-roadmap.md')
    reviewed={n:(root/n).read_bytes() for n in names};m=load(root/'proof_routes.py','ym17_adapter_review');core=load(root/'proof_search.py','ym17_existing_core');frozen=m.snapshot();saved=json.loads(reviewed['proof_results.json']);checks=[]
    def check(name,ok=True):
        if not ok:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError,FileNotFoundError):check(name);return
        raise ValueError('accepted invalid evidence: '+name)
    check('saved report binds executing adapter and complete 158-file snapshot',saved['adapter_sha256']==digest(reviewed['proof_routes.py']) and saved['source_sha256']==json.loads(reviewed['proof_inputs.json'])=={n:digest(v) for n,v in frozen.items()} and len(frozen)==158)
    check('unchanged previously audited search core',digest(reviewed['proof_search.py'])=='07b5b397af86b6bf5a481b114844c6252046e8ca2b5604dac7d158091632be94')
    check('all eighteen declared route cases retained',list(saved['routes'])==[c[0] for c in CASES])
    libs,accepted=m.build_libraries(frozen,[(goal,removed) for _,goal,removed,_ in CASES])
    expected_counts={loop:{'status':'passed','checks_count':json.loads(frozen['backward/'+loop+'/output/results.json'])['checks_count'],
      'comparison_checks_count':json.loads(frozen['backward/'+loop+'/comparison/results.json'])['checks_count']} for loop in ('a1','a2','b1','b2','c1','c2')}
    check('fresh subprocess independently executes all six science and comparison gates',accepted==saved['arithmetic'] and accepted['independent']==expected_counts and accepted['gates']==[p+'_gate' for p in expected_counts])
    for (name,goal,removed,status),lib in zip(CASES,libs):
        route=saved['routes'][name];res=route['result'];core.load_library(lib)
        okay=serial(lib)==serial(route['library']) and route['target']==goal and res['status']==status and closure(lib)==(status=='proved') and not set(lib['initial_facts'])&m.OPEN
        if status=='proved':
            cost=ordered(lib,res['certified_proof']);meetingcost=ordered(lib,res['first_meeting_candidate']);events={(e.get('phase'),e.get('event')) for e in res['search_trace']};meetings=[e for e in res['search_trace'] if e.get('phase')=='bidirectional' and e.get('event')=='first_meeting']
            okay &= ('bidirectional','forward_pop') in events and ('bidirectional','backward_pop') in events and len(meetings)==1
            okay &= set(meetings[0]['backward_goals'])<=set(meetings[0]['forward_facts']) and meetings[0]['checker_passed'] is True and meetings[0]['cost']==meetingcost
            okay &= cost==res['certified_cost'] and meetingcost>=cost and res['independent_ordered_replay']=={'passed':True,'steps':cost,'cost':cost}
        check(name+' fresh library, independent closure and actual checked route',okay)
    bases={goal:name for name,goal,removed,status in CASES if status=='proved'}
    for name,goal,removed,status in CASES:
        if not removed:continue
        normal=saved['routes'][bases[goal]]['library'];lib=saved['routes'][name]['library']
        check(name+' exactly the necessary premise withdrawn',set(normal['initial_facts'])-set(lib['initial_facts'])==set(removed) and normal['rules']==lib['rules'] and not closure(lib))
    rules={r[0]:r for r in m.RULES}
    check('sparse physical conclusion retains disjoint supports and common energy units',set(rules['S1'][1])=={'rotor_contract','sparse_support','a2_gate'} and set(rules['S5'][1])=={'sparse_dimensionless_gap','common_scale'})
    check('finite positive endpoint requires explicit frozen coupling and amplitude',set(rules['B5'][1])=={'trial_gram','endpoint_trial','b2_gate'} and '12/43' in m.STATEMENTS['endpoint_trial'] and '3/3817' in m.STATEMENTS['endpoint_trial'])
    check('weighted conditional contrast is not inferred from Haar projection alone',set(rules['C4'][1])=={'conditional_kernel','c2_gate'} and 'zero central coupling' in m.STATEMENTS['conditional_kernel'] and 'nonzero coupling requires weighted moments' in m.STATEMENTS['conditional_kernel'])
    check('repaired dense bridge retains applicable stability and actual smallness obligations',set(rules['U1'][1])=={'rotor_contract','dense_overlap_control','applicable_rotor_stability','dense_coupling_smallness','common_scale'} and {'applicable_rotor_stability','dense_coupling_smallness'}<=m.OPEN and not {'applicable_rotor_stability','dense_coupling_smallness'}&m.HYPOTHESES)
    check('continuum target still requires separate construction and spectral obligations',set(rules['Y1'][1])=={'dense_uniform_gap','matched_generator','continuum_axioms','nontrivial_limit','controlled_spectral_limit'})
    reject('external passed object cannot admit a source library',lambda:m.build_libraries({'status':'passed','gates':list(m.GATES)},[('ym_gap',())]))
    reject('empty frozen byte inventory rejected',lambda:m.build_libraries({},[('channel_contrast',())]))
    missing=dict(frozen);missing.pop('backward/c2/angular.py');reject('missing independent coefficient oracle rejected',lambda:m.build_libraries(missing,[('channel_contrast',())]))
    changed=dict(frozen);changed['forward/c2/output/collection.json']+=b'\n';reject('changed scientific bytes rejected despite passed metadata',lambda:m.build_libraries(changed,[('channel_contrast',())]))
    injections=[
      ('HYPOTHESES',lambda v:frozenset(set(v)|{'applicable_rotor_stability','dense_coupling_smallness'}),'dense_uniform_gap'),
      ('HYPOTHESES',lambda v:frozenset(set(v)|{'finite_endpoint_repair'}),'finite_endpoint_repair'),
      ('GATES',lambda v:frozenset(set(v)|{'ym_gap'}),'ym_gap'),
      ('OPEN',lambda v:frozenset(set(v)-{'dense_coupling_smallness'}),'dense_uniform_gap'),
      ('STATEMENTS',lambda v:MappingProxyType({**v,'common_scale':'Each alpha is separately positive, without a common lower bound.'}),'sparse_physical_gap'),
      ('STATEMENTS',lambda v:MappingProxyType({**v,'endpoint_trial':'The amplitude eta is zero.'}),'finite_endpoint_repair'),
      ('RULES',lambda v:tuple(v)+(('injected',('conditional_kernel',),'ym_gap'),),'ym_gap')]
    for attr,modify,target in injections:
        old=getattr(m,attr);setattr(m,attr,modify(old))
        try:reject('runtime '+attr+' injection targeting '+target,lambda target=target:m.build_libraries(frozen,[(target,())]))
        finally:setattr(m,attr,old)
    good=saved['routes']['finite_endpoint_repair'];lib=good['library'];proof=good['result']['certified_proof']
    bad=copy.deepcopy(proof);bad['steps'].pop(0);reject('passed proof record without its first premise step rejected',lambda:ordered(lib,bad))
    bad=copy.deepcopy(proof);bad['steps'][-1]['conclusion']='ym_gap';reject('proof conclusion cannot be changed after search',lambda:ordered(lib,bad))
    bad=copy.deepcopy(proof);bad['cost']=True;reject('Boolean proof cost rejected',lambda:ordered(lib,bad))
    hidden=copy.deepcopy(lib);node=copy.deepcopy(hidden['nodes'][0]);node.update(id='hidden_open',statement='Unproved bridge',kind='target',assumption_ids=[]);hidden['nodes'].append(node)
    next(n for n in hidden['nodes'] if n['id']=='finite_endpoint_repair')['assumption_ids'].append('hidden_open')
    reject('hidden endpoint assumption cannot be omitted from the checked route',lambda:core.load_library(hidden))
    with tempfile.TemporaryDirectory(prefix='ym17-adapter-review-',dir=out) as tmp:
        isolated=Path(tmp);copy_snapshot(isolated,frozen);(isolated/'proof_routes.py').write_bytes(reviewed['proof_routes.py']);(isolated/'proof_inputs.json').write_bytes(reviewed['proof_inputs.json'])
        own=load(isolated/'proof_routes.py','ym17_isolated_admission');own.snapshot();path=isolated/'backward/c2/angular.py';original=path.read_bytes()
        path.write_bytes(original+b'\n');reject('warm snapshot detects changed source file',own.snapshot);path.write_bytes(original)
        path.unlink();reject('missing source file detected on disk',own.snapshot);path.write_bytes(original)
        alias=isolated/'alias.py';alias.write_bytes(original);path.unlink();path.symlink_to(alias);reject('symlink source replacement rejected',own.snapshot);path.unlink();path.write_bytes(original)
        inv=isolated/'proof_inputs.json';inv.write_text('{}');reject('empty on-disk inventory rejected',own.snapshot);inv.write_bytes(reviewed['proof_inputs.json'])
        shortened=json.loads(reviewed['proof_inputs.json']);shortened.pop('backward/c2/angular.py');inv.write_text(json.dumps(shortened));reject('shortened source inventory cannot authorize an omitted obligation',own.snapshot);inv.write_bytes(reviewed['proof_inputs.json'])
        ownpath=isolated/'proof_routes.py';ownpath.write_bytes(reviewed['proof_routes.py']+b'\n');reject('loaded adapter detects its own changed bytes',own.snapshot);ownpath.write_bytes(reviewed['proof_routes.py'])
        target=isolated/'forward/c2/output/collection.json';altered=json.loads(target.read_bytes());altered['refinements'][-1]['contrast']['interval']=['1','2'];target.write_text(json.dumps(altered))
        admission=isolated/'forged-admission.json';proc=subprocess.run([sys.executable,str(isolated/'replay_evidence.py'),str(admission)],cwd=isolated,capture_output=True,text=True,timeout=240)
        check('cold independent arithmetic itself rejects a forged passed contrast',proc.returncode!=0 and not admission.exists())
    # Exercise the portable reproducer's mode, path protections and semantic admission.
    with tempfile.TemporaryDirectory(prefix='ym17-reproduce-review-',dir=out) as tmp:
        temp=Path(tmp);target=temp/'fresh'
        proc=subprocess.run([sys.executable,str(root/'reproduce.py'),'--optimized','--independent-only','--output',str(target)],cwd=temp,capture_output=True,text=True,timeout=300)
        if proc.returncode:raise ValueError('portable independent reproduction failed: '+proc.stderr[-1800:])
        rr=json.loads((target/'reproduction.json').read_bytes())
        check('portable optimized independent mode executes twelve fresh programs',rr['status']=='passed' and rr['optimized'] is True and rr['independent_only'] is True and rr['loops']==6 and len(rr['runs'])==12 and {x['role'] for x in rr['runs']}=={'backward','comparison'})
        proc=subprocess.run([sys.executable,str(root/'reproduce.py'),'--output',str(target)],cwd=temp,capture_output=True,text=True,timeout=30)
        check('portable reproducer rejects reuse of an existing output directory',proc.returncode!=0)
        proc=subprocess.run([sys.executable,str(root/'reproduce.py'),'--output',str(root/'unsafe-review-output')],cwd=temp,capture_output=True,text=True,timeout=30)
        check('portable reproducer rejects writing inside accepted sources',proc.returncode!=0 and not (root/'unsafe-review-output').exists())
    check('review leaves all source evidence and saved results unchanged',m.snapshot()==frozen and all((root/n).read_bytes()==raw for n,raw in reviewed.items()))
    report={'schema':'ym17-independent-integration-review-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'reviewed_source_sha256':{n:digest(raw) for n,raw in reviewed.items()},'reviewer_source_sha256':digest(Path(__file__).read_bytes()),
      'frozen_inputs':len(frozen),'routes':18,'proved_routes':6,'withdrawal_controls':9,'open_targets':3,
      'scope':'Bounded new-adapter review, fresh independent scientific admission, complete premise withdrawal and two-front/ordered replay; unchanged search core is hash-checked rather than exhaustively re-audited.',
      'limits':['A finite Horn-rule certificate is not a formal proof-assistant kernel.','The dense stability, bulk and continuum obligations remain unproved.','Ordinary and optimized review runs repeat the same named gates; count once.']}
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks),'routes':18}));return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--round-dir',required=True);p.add_argument('--output',required=True);a=p.parse_args();audit(a.round_dir,a.output)
