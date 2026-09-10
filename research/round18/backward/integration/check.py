"""Bounded independent Round18 source-admission and integration review."""
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
 ('dressed_bridge','bridge_gap',(),'proved'),
 ('inhomogeneous_uniform_family','inhomogeneous_physical_gap',(),'proved'),
 ('full_complement','complement_control',(),'proved'),
 ('finite_coefficient_box','finite_box_gap',(),'proved'),
 ('endpoint_improvement','finite_endpoint_gap',(),'proved'),
 ('central_gram','central_gram_closure',(),'proved'),
 ('two_link_integral','controlled_two_link',(),'proved'),
 ('weak_bare_matching','weak_bare_domain_obstruction',(),'proved'),
 ('outer_gram_connection','outer_gram_reduction',(),'proved'),
 ('no_dressed_haar','bridge_gap',('a1_gate',),'not_derivable'),
 ('no_bridge_geometry','bridge_gap',('bridge_geometry',),'not_derivable'),
 ('no_clusters','inhomogeneous_physical_gap',('cluster_support',),'not_derivable'),
 ('no_decay_schedule','inhomogeneous_physical_gap',('summable_schedule',),'not_derivable'),
 ('no_common_scale','inhomogeneous_physical_gap',('common_scale',),'not_derivable'),
 ('no_cluster_gate','inhomogeneous_physical_gap',('a2_gate',),'not_derivable'),
 ('no_complete_complement','finite_box_gap',('b1_gate',),'not_derivable'),
 ('no_box','finite_box_gap',('coefficient_box',),'not_derivable'),
 ('no_spectral_gate','finite_box_gap',('b2_gate',),'not_derivable'),
 ('no_endpoint','finite_endpoint_gap',('endpoint_magnitudes',),'not_derivable'),
 ('no_gram_validity','central_gram_closure',('admissible_gram',),'not_derivable'),
 ('undeclared_observable','central_gram_closure',('central_dot_observables',),'not_derivable'),
 ('no_gram_gate','central_gram_closure',('c1_gate',),'not_derivable'),
 ('missing_face_weights','controlled_two_link',('six_face_conditional',),'not_derivable'),
 ('no_integral_gate','controlled_two_link',('c2_gate',),'not_derivable'),
 ('no_rotor_contract','bridge_gap',('rotor_contract',),'not_derivable'),
 ('no_dense_geometry','finite_box_gap',('dense_two_cube',),'not_derivable'),
 ('no_conditional_coefficient','controlled_two_link',('conditional_coefficient',),'not_derivable'),
 ('no_bare_matching','weak_bare_domain_obstruction',('standard_bare_matching',),'not_derivable'),
 ('no_central_gate_for_outer','outer_gram_reduction',('c1_gate',),'not_derivable'),
 ('no_joint_gate_for_outer','outer_gram_reduction',('c2_gate',),'not_derivable'),
 ('no_common_coefficient_for_outer','outer_gram_reduction',('conditional_coefficient',),'not_derivable'),
 ('homogeneous_dense_uniform','dense_uniform_gap',(),'not_derivable'),
 ('full_bulk','full_bulk_contraction',(),'not_derivable'),
 ('continuum_yang_mills','ym_gap',(),'not_derivable')]


def audit(round_dir,output):
    root=Path(round_dir).resolve();out=Path(output).resolve()
    if out.is_relative_to(Path(__file__).resolve().parent):raise ValueError('review output outside source required')
    out.mkdir(parents=True,exist_ok=False)
    names=('proof_routes.py','replay_evidence.py','proof_inputs.json','proof_search.py','proof_results.json','reproduce.py','advisor/freeze_gate.py','next-roadmap.md','advisor/integration-review-contract.md')
    reviewed={n:(root/n).read_bytes() for n in names};m=load(root/'proof_routes.py','ym18_adapter_review');core=load(root/'proof_search.py','ym18_existing_core');frozen=m.snapshot();saved=json.loads(reviewed['proof_results.json']);checks=[]
    def check(name,ok=True):
        if type(ok) is not bool or not ok:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError,FileNotFoundError):check(name);return
        raise ValueError('accepted invalid evidence: '+name)
    check('executing adapter and complete262-file snapshot are bound to saved proof report',saved['adapter_sha256']==digest(reviewed['proof_routes.py']) and saved['source_sha256']==json.loads(reviewed['proof_inputs.json'])=={n:digest(v) for n,v in frozen.items()} and len(frozen)==262)
    check('search core is byte-identical to the previously independently audited core',digest(reviewed['proof_search.py'])=='07b5b397af86b6bf5a481b114844c6252046e8ca2b5604dac7d158091632be94')
    check('all34 intended route cases and their order are retained',list(saved['routes'])==[x[0] for x in CASES])
    libraries,accepted=m.build_libraries(frozen,[(goal,removed) for _,goal,removed,_ in CASES])
    expected_counts={loop:{'status':'passed','checks_count':json.loads(frozen['backward/'+loop+'/output/results.json'])['checks_count'],
      'comparison_checks_count':json.loads(frozen['backward/'+loop+'/comparison/results.json'])['checks_count']} for loop in ('a1','a2','b1','b2','c1','c2')}
    check('fresh subprocess independently executes all six scientific and comparison gates',accepted==saved['arithmetic'] and accepted['independent']==expected_counts and accepted['gates']==[p+'_gate' for p in expected_counts])
    for (name,goal,removed,status),lib in zip(CASES,libraries):
        route=saved['routes'][name];res=route['result'];core.load_library(lib)
        okay=serial(lib)==serial(route['library']) and route['target']==goal and res['status']==status and closure(lib)==(status=='proved') and not set(lib['initial_facts'])&m.OPEN
        if status=='proved':
            cost=ordered(lib,res['certified_proof']);mcost=ordered(lib,res['first_meeting_candidate']);events={(e.get('phase'),e.get('event')) for e in res['search_trace']}
            meetings=[e for e in res['search_trace'] if e.get('phase')=='bidirectional' and e.get('event')=='first_meeting']
            okay &= ('bidirectional','forward_pop') in events and ('bidirectional','backward_pop') in events and len(meetings)==1
            okay &= set(meetings[0]['backward_goals'])<=set(meetings[0]['forward_facts']) and meetings[0]['checker_passed'] is True and meetings[0]['cost']==mcost
            okay &= cost==res['certified_cost'] and mcost>=cost and res['independent_ordered_replay']=={'passed':True,'steps':cost,'cost':cost}
        check(name+': fresh library, independent closure and checked two-front/ordered replay',okay)
    bases={goal:name for name,goal,removed,status in CASES if status=='proved'}
    for name,goal,removed,status in CASES:
        if not removed:continue
        original=saved['routes'][bases[goal]]['library'];lib=saved['routes'][name]['library']
        check(name+': exactly the necessary premise is withdrawn',set(original['initial_facts'])-set(lib['initial_facts'])==set(removed) and original['rules']==lib['rules'] and not closure(lib))
    rules={x[0]:x for x in m.RULES}
    check('cluster tensorization uses full-link spectral control and invariant ground, not only a physical-subspace gap',set(rules['A3'][1])=={'bridge_gap','cluster_support','a2_gate'} and 'full-link gap' in m.STATEMENTS['bridge_gap'] and 'gauge-invariant full-link ground' in m.STATEMENTS['bridge_gap'] and 'full-link clusters' in m.STATEMENTS['cluster_reference'])
    check('inhomogeneous bound retains support, summable interactions and common physical scale',set(rules['A5'][1])=={'rotor_contract','summable_schedule','a2_gate'} and set(rules['A7'][1])=={'inhomogeneous_dimensionless_gap','common_scale'} and 'alpha_min>0' in m.STATEMENTS['common_scale'] and 'spatially decaying' in m.STATEMENTS['inhomogeneous_dimensionless_gap'])
    check('full complement and endpoint trial retain explicit positive-scale rotor contract',all('rotor_contract' in rules[key][1] for key in ('B1','B2','B5','B6')) and 'alpha>0' in m.STATEMENTS['rotor_contract'] and '9alpha/2' in m.STATEMENTS['complete_complement'] and 'H0-reducing' in m.STATEMENTS['complete_complement'])
    check('finite signed box pairs full E1 lower with a separate endpoint Rayleigh E0 upper',set(rules['B7'][1])=={'full_excited_bound','endpoint_upper'} and '|lambda_p|=3alpha/8' in m.STATEMENTS['endpoint_magnitudes'] and 'E0/alpha<=' in m.STATEMENTS['endpoint_upper'])
    check('direct two-link result is independent of C1 implementation',set(rules['C4'][1])=={'joint_link_moments','conditional_coefficient','c2_gate'} and 'c1_gate' not in saved['routes']['two_link_integral']['library']['initial_facts'])
    check('repaired C1-to-C2 bridge retains actual geometry, common coefficient and induced weighted measure',set(rules['C5'][1])=={'central_gram_closure','joint_link_moments','six_face_conditional','conditional_coefficient','c2_gate'} and 'conditional partition' in m.STATEMENTS['outer_gram_reduction'] and 'semicircle' in m.STATEMENTS['outer_gram_reduction'])
    check('bare matching conclusion is domain obstruction rather than no-gap claim',set(rules['B8'][1])=={'standard_bare_matching','coefficient_box','b2_gate'} and 'g^4>=32/3' in m.STATEMENTS['weak_bare_domain_obstruction'] and 'not a no-gap theorem' in m.STATEMENTS['weak_bare_domain_obstruction'])
    check('dense and continuum bridges retain all unresolved theorem and limit premises',set(rules['U1'][1])=={'rotor_contract','dense_overlap_control','applicable_rotor_stability','dense_coupling_smallness','common_scale'} and set(rules['Y1'][1])=={'dense_uniform_gap','matched_generator','continuum_axioms','nontrivial_limit','controlled_spectral_limit'} and {'applicable_rotor_stability','dense_coupling_smallness'}<=m.OPEN)
    reject('caller supplied passed record cannot seed a library',lambda:m.build_libraries({'status':'passed','gates':list(m.GATES)},[('ym_gap',())]))
    reject('empty frozen inventory rejected',lambda:m.build_libraries({},[('controlled_two_link',())]))
    missing=dict(frozen);missing.pop('backward/c2/angular.py');reject('missing independent arithmetic source rejected',lambda:m.build_libraries(missing,[('controlled_two_link',())]))
    changed=dict(frozen);changed['forward/c2/output/completecollection.json']+=b'\n';reject('changed scientific bytes rejected despite retained pass metadata',lambda:m.build_libraries(changed,[('controlled_two_link',())]))
    injections=[('HYPOTHESES',lambda v:frozenset(set(v)|{'applicable_rotor_stability','dense_coupling_smallness'}),'dense_uniform_gap'),
      ('HYPOTHESES',lambda v:frozenset(set(v)|{'finite_box_gap'}),'finite_box_gap'),
      ('GATES',lambda v:frozenset(set(v)|{'ym_gap'}),'ym_gap'),
      ('OPEN',lambda v:frozenset(set(v)-{'nontrivial_limit'}),'ym_gap'),
      ('STATEMENTS',lambda v:MappingProxyType({**v,'common_scale':'Every alpha is separately positive, with no common floor.'}),'inhomogeneous_physical_gap'),
      ('STATEMENTS',lambda v:MappingProxyType({**v,'conditional_coefficient':'Six independent unrelated coefficients.'}),'outer_gram_reduction'),
      ('RULES',lambda v:tuple(v)+(('injected',('joint_link_moments',),'ym_gap'),),'ym_gap')]
    for attr,modify,target in injections:
        old=getattr(m,attr);setattr(m,attr,modify(old))
        try:reject('runtime '+attr+' injection targeting '+target,lambda target=target:m.build_libraries(frozen,[(target,())]))
        finally:setattr(m,attr,old)
    route=saved['routes']['outer_gram_connection'];lib=route['library'];proof=route['result']['certified_proof']
    bad=copy.deepcopy(proof);bad['steps'].pop(0);reject('passed certificate with omitted prerequisite step rejected',lambda:ordered(lib,bad))
    bad=copy.deepcopy(proof);bad['steps'][-1]['conclusion']='ym_gap';reject('altered theorem conclusion after search rejected',lambda:ordered(lib,bad))
    bad=copy.deepcopy(proof);bad['cost']=True;reject('Boolean proof cost rejected',lambda:ordered(lib,bad))
    hidden=copy.deepcopy(lib);node=copy.deepcopy(hidden['nodes'][0]);node.update(id='hidden_open',statement='Unproved surrounding measure',kind='target',assumption_ids=[]);hidden['nodes'].append(node)
    next(n for n in hidden['nodes'] if n['id']=='outer_gram_reduction')['assumption_ids'].append('hidden_open');reject('hidden outer-measure assumption cannot bypass rule antecedents',lambda:core.load_library(hidden))
    with tempfile.TemporaryDirectory(prefix='ym18-adapter-review-',dir=out) as td:
        isolated=Path(td);copy_snapshot(isolated,frozen);(isolated/'proof_routes.py').write_bytes(reviewed['proof_routes.py']);(isolated/'proof_inputs.json').write_bytes(reviewed['proof_inputs.json'])
        local=load(isolated/'proof_routes.py','ym18_isolated_admission');local.snapshot();path=isolated/'backward/c2/angular.py';original=path.read_bytes()
        path.write_bytes(original+b'\n');reject('warm admission detects changed source file',local.snapshot);path.write_bytes(original)
        path.unlink();reject('missing source file detected on disk',local.snapshot);path.write_bytes(original)
        alias=isolated/'alias.py';alias.write_bytes(original);path.unlink();path.symlink_to(alias);reject('symlink source replacement rejected by proof admission',local.snapshot);path.unlink();path.write_bytes(original)
        inv=isolated/'proof_inputs.json';inv.write_text('{}');reject('empty on-disk inventory rejected',local.snapshot);inv.write_bytes(reviewed['proof_inputs.json'])
        short=json.loads(reviewed['proof_inputs.json']);short.pop('backward/c2/angular.py');inv.write_text(json.dumps(short));reject('shortened inventory cannot remove a proof obligation',local.snapshot);inv.write_bytes(reviewed['proof_inputs.json'])
        adapter=isolated/'proof_routes.py';adapter.write_bytes(reviewed['proof_routes.py']+b'\n');reject('loaded adapter detects changed own source',local.snapshot);adapter.write_bytes(reviewed['proof_routes.py'])
        # Gate/reproducer boundary must also reject a symlink role directory, not just symlink leaf files.
        gate_module=load(isolated/'advisor/freeze_gate.py','ym18_gate_boundary');gate_module.verify(isolated/'advisor/a1-gate.json')
        role=isolated/'backward/a1';outside=isolated/'outside-a1';role.rename(outside);role.symlink_to(outside,target_is_directory=True)
        reject('repaired gate verifier rejects symlink role-root directory',lambda:gate_module.verify(isolated/'advisor/a1-gate.json'))
        role.unlink();outside.rename(role)
        parent=isolated/'backward';outside_parent=isolated/'outside-backward';parent.rename(outside_parent);parent.symlink_to(outside_parent,target_is_directory=True)
        reject('repaired gate verifier rejects a symlink intermediate role directory',lambda:gate_module.verify(isolated/'advisor/a1-gate.json'))
        parent.unlink();outside_parent.rename(parent)
        supplied=isolated/'alias-gate.json';supplied.symlink_to(isolated/'advisor/a1-gate.json')
        reject('repaired gate verifier rejects a supplied symlink gate file',lambda:gate_module.verify(supplied));supplied.unlink()
        extra=isolated/'forward/c2/undeclared.py';extra.write_text('unexpected=True\n');reject('gate inventory rejects an undeclared source file',lambda:gate_module.verify(isolated/'advisor/c2-gate.json'));extra.unlink()
        # Bypass only the outer inventory here: prove that arithmetic itself rejects a forged result.
        target=isolated/'forward/c2/output/completecollection.json';wrong=json.loads(target.read_bytes());wrong['refinements'][-1]['expectation_interval']['lower']='1';target.write_text(json.dumps(wrong))
        destination=isolated/'forged-comparison';command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(isolated/'backward/c2/compare.py'),'--producer',str(isolated/'forward/c2'),'--evidence',str(isolated/'forward/c2/output'),'--output',str(destination)]
        p=subprocess.run(command,cwd=isolated,capture_output=True,text=True,timeout=90)
        check('independent comparator itself rejects forged arithmetic after deliberate outer-hash bypass',p.returncode!=0 and 'full signed tail division at degree8' in p.stderr and not (destination/'results.json').exists())
    with tempfile.TemporaryDirectory(prefix='ym18-relocation-review-',dir=out) as td:
        temp=Path(td);target=temp/'fresh'
        p=subprocess.run([sys.executable,str(root/'reproduce.py'),'--optimized','--independent-only','--output',str(target)],cwd=temp,capture_output=True,text=True,timeout=300)
        if p.returncode:raise ValueError('optimized relocated reproduction failed: '+p.stderr[-1800:])
        rr=json.loads((target/'reproduction.json').read_bytes())
        check('unrelated-directory optimized independent mode executes all twelve fresh programs',rr['status']=='passed' and rr['optimized'] is True and rr['independent_only'] is True and rr['loops']==6 and len(rr['runs'])==12 and {x['role'] for x in rr['runs']}=={'backward','comparison'})
        for run in rr['runs']:
            name=('backward/'+run['loop']+'/comparison/results.json') if run['role']=='comparison' else ('backward/'+run['loop']+'/output/results.json')
            if run['results_sha256']!=digest(frozen[name]):raise ValueError('relocated result differs from bound input')
        check('every relocated science and comparison result matches frozen semantic bytes')
        (out/'optimized-reproduction.json').write_text(json.dumps(rr,indent=2)+'\n')
        p=subprocess.run([sys.executable,str(root/'reproduce.py'),'--output',str(target)],cwd=temp,capture_output=True,text=True,timeout=30);check('reproducer rejects an existing destination',p.returncode!=0)
        unsafe=root/'unsafe-review-output';p=subprocess.run([sys.executable,str(root/'reproduce.py'),'--output',str(unsafe)],cwd=temp,capture_output=True,text=True,timeout=30)
        check('reproducer rejects a destination inside the accepted tree',p.returncode!=0 and not unsafe.exists())
    check('review left all accepted sources and saved results unchanged',m.snapshot()==frozen and all((root/n).read_bytes()==raw for n,raw in reviewed.items()))
    report={'schema':'ym18-independent-integration-review-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'reviewed_source_sha256':{n:digest(raw) for n,raw in reviewed.items()},'reviewer_source_sha256':digest(Path(__file__).read_bytes()),
      'frozen_inputs':len(frozen),'routes':34,'proved_routes':9,'withdrawal_controls':22,'open_targets':3,
      'scope':'Bounded new-adapter, source admission, portable reproduction and roadmap review. The unchanged core is hash-checked without repeating its earlier exhaustive library tests.',
      'limits':['Rule replay is not a formal proof-assistant kernel.','The homogeneous dense, bulk and continuum goals remain open.','Ordinary and optimized reviews repeat the same named gates and count once.','Browser/UI/public hosting have separate verification records.']}
    (out/'results.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks),'routes':34}));return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--round-dir',required=True);p.add_argument('--output',required=True);ns=p.parse_args();audit(ns.round_dir,ns.output)
