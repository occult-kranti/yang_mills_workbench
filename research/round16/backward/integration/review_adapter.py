"""Narrow independent source admission and two-front proof adapter review."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,subprocess,sys,tempfile

CASES={'finite_shared_effect':'proved','shared_haar_reduction':'proved','physical_scale_counterexample':'proved',
 'missing_graph':'not_derivable','missing_projector':'not_derivable','missing_coefficients':'not_derivable','missing_total_tail':'not_derivable','missing_difference':'not_derivable','missing_scale_audit':'not_derivable','original_uniform_goal':'not_derivable','unmatched_generator':'not_derivable','four_dimensional_yang_mills':'not_derivable'}


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


def audit(round_dir,output):
    root=Path(round_dir).resolve();out=Path(output);out.mkdir(parents=True,exist_ok=False)
    reviewed={name:(root/name).read_bytes() for name in ('proof_routes.py','replay_evidence.py','proof_inputs.json','proof_search.py','proof_results.json')}
    m=load(root/'proof_routes.py','ym16_adapter_review');core=load(root/'proof_search.py','ym16_reviewed_core');frozen=m.snapshot();saved=json.loads(reviewed['proof_results.json']);checks=[]
    def check(name,ok=True):
        if not ok:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError,FileNotFoundError):check(name);return
        raise ValueError('accepted invalid input: '+name)
    check('saved report binds executing adapter',saved.get('adapter_sha256')==digest(reviewed['proof_routes.py']))
    check('complete frozen inventory binds saved results',saved['source_sha256']==json.loads(reviewed['proof_inputs.json'])=={n:digest(v) for n,v in frozen.items()})
    check('unchanged reviewed core hash',digest(reviewed['proof_search.py'])=='07b5b397af86b6bf5a481b114844c6252046e8ca2b5604dac7d158091632be94')
    check('exact twelve route inventory',set(saved['routes'])==set(CASES))
    for name,status in CASES.items():
        route=saved['routes'][name];lib,res=route['library'],route['result']
        check(name+' independent forward closure',closure(lib)==(status=='proved') and res['status']==status)
        check(name+' open premises absent from seeds',not set(lib['initial_facts'])&m.OPEN)
        core.load_library(lib)
        if status=='proved':
            cost=ordered(lib,res['certified_proof']);meeting_cost=ordered(lib,res['first_meeting_candidate']);events={(row.get('phase'),row.get('event')) for row in res['search_trace']}
            check(name+' real forward and backward search plus separate ordered replay',('bidirectional','forward_pop') in events and ('bidirectional','backward_pop') in events and cost==res['certified_cost'] and meeting_cost>=cost)
    check('finite route uses eight reviewed rules',saved['routes']['finite_shared_effect']['result']['certified_cost']==8)
    withdrawal={'missing_graph':'graph_gate','missing_projector':'haar_gate','missing_coefficients':'coefficient_gate','missing_total_tail':'remainder_gate','missing_difference':'difference_gate','missing_scale_audit':'scale_gate'}
    for name,gate in withdrawal.items():
        lib=saved['routes'][name]['library'];normal=saved['routes']['physical_scale_counterexample' if name=='missing_scale_audit' else 'finite_shared_effect']['library']
        check(name+' exactly the required gate withdrawn',set(normal['initial_facts'])-set(lib['initial_facts'])=={gate} and normal['rules']==lib['rules'] and not closure(lib))
    for name,target in [('finite_shared_effect','shared_effect'),('physical_scale_counterexample','scale_counterexample')]:
        lib,accepted=m.library(frozen,target)
        check(name+' cold independent admission reproduces saved library',serial(lib)==serial(saved['routes'][name]['library']) and accepted['independent']=={'loop1':{'checks':118,'status':'passed'},'loop2':{'checks':84,'status':'passed'}})
    lib,accepted=m.library(frozen,'ym_gap')
    check('successful scientific replay leaves outer target underivable',not closure(lib) and not set(lib['initial_facts'])&m.OPEN)
    rules={r['id']:r for r in lib['rules']}
    check('uniform physical bridge explicitly requires common energy scale',set(rules['U2']['premises'])=={'uniform_dimensionless_gap','uniform_energy_scale','scale_identity'})
    check('uniform source bridge retains family and smallness obligations',set(rules['U1']['premises'])=={'local_uniform_constants','volume_family_contract','uniform_smallness'} and 'theorem' in m.STATEMENTS['local_uniform_constants'])
    check('continuum target requires controlled spectral limit and matched generator',set(rules['Y1']['premises'])=={'uniform_gap','matched_generator','continuum_axioms','nontrivial_limit','controlled_spectral_limit'})
    reject('caller passed record cannot seed proof',lambda:m.library({'status':'passed','gates':list(m.GATES)},'shared_effect'))
    reject('empty frozen inventory rejected',lambda:m.library({},'shared_effect'))
    missing=dict(frozen);missing.pop('backward/loop2/polynomial_oracle.py');reject('required independent source cannot be omitted',lambda:m.library(missing,'shared_effect'))
    changed=dict(frozen);changed['forward/loop2/output/collection.json']+=b'\n';reject('changed frozen arithmetic rejected',lambda:m.library(changed,'shared_effect'))
    reject('unsupported premise withdrawal rejected',lambda:m.library(frozen,'shared_effect',('uniform_energy_scale',)))
    reject('duplicate premise withdrawal rejected',lambda:m.library(frozen,'shared_effect',('graph_gate','graph_gate')))
    for attr,modify,target in [
      ('HYPOTHESES',lambda v:frozenset(set(v)|{'uniform_energy_scale'}),'uniform_energy_scale'),
      ('HYPOTHESES',lambda v:frozenset(set(v)|{'matched_generator'}),'matched_generator'),
      ('GATES',lambda v:frozenset(set(v)|{'uniform_gap'}),'uniform_gap'),
      ('OPEN',lambda v:frozenset(set(v)-{'uniform_energy_scale'}),'uniform_energy_scale'),
      ('STATEMENTS',lambda v:{**v,'shared_effect':'Four-dimensional mass gap proved.'},'shared_effect'),
      ('RULES',lambda v:tuple(v)+(('injected',('two_cube_measure',),'ym_gap'),),'ym_gap')]:
        old=getattr(m,attr);setattr(m,attr,modify(old))
        try:reject('runtime '+attr+' injection into '+target,lambda target=target:m.library(frozen,target))
        finally:setattr(m,attr,old)
    goodlib=saved['routes']['finite_shared_effect']['library'];goodproof=saved['routes']['finite_shared_effect']['result']['certified_proof']
    bad=copy.deepcopy(goodproof);bad['steps'].pop(0);reject('forged passed proof missing premise step',lambda:ordered(goodlib,bad))
    bad=copy.deepcopy(goodproof);bad['steps'][0]['conclusion']='ym_gap';reject('changed proof conclusion rejected',lambda:ordered(goodlib,bad))
    bad=copy.deepcopy(goodproof);bad['cost']=True;reject('Boolean proof cost rejected',lambda:ordered(goodlib,bad))
    hidden=copy.deepcopy(goodlib);node=copy.deepcopy(hidden['nodes'][0]);node.update(id='hidden_open',kind='target',assumption_ids=[]);hidden['nodes'].append(node)
    next(n for n in hidden['nodes'] if n['id']=='shared_effect')['assumption_ids'].append('hidden_open')
    reject('hidden conclusion assumption cannot be laundered by rule metadata',lambda:core.load_library(hidden))
    with tempfile.TemporaryDirectory(prefix='ym16-adapter-review-',dir=out) as tmp:
        isolated=Path(tmp);copy_snapshot(isolated,frozen);(isolated/'proof_routes.py').write_bytes(reviewed['proof_routes.py']);(isolated/'proof_inputs.json').write_bytes(reviewed['proof_inputs.json'])
        own=load(isolated/'proof_routes.py','ym16_isolated_review');own.snapshot();path=isolated/'backward/loop2/polynomial_oracle.py';original=path.read_bytes()
        path.write_bytes(original+b'\n');reject('warm source cache cannot hide disk modification',own.snapshot);path.write_bytes(original)
        path.unlink();reject('missing frozen file rejected',own.snapshot);path.write_bytes(original)
        other=isolated/'alias.py';other.write_bytes(original);path.unlink();path.symlink_to(other);reject('symlink replacement rejected',own.snapshot);path.unlink();path.write_bytes(original)
        inventory=json.loads(reviewed['proof_inputs.json']);inventory.pop('backward/loop2/polynomial_oracle.py');(isolated/'proof_inputs.json').write_text(json.dumps(inventory));reject('shortened inventory cannot authorize missing premise',own.snapshot)
        (isolated/'proof_inputs.json').write_text('{}');reject('empty disk inventory rejected',own.snapshot);(isolated/'proof_inputs.json').write_bytes(reviewed['proof_inputs.json'])
        # Directly challenge the replay executable as well as the outer hash gate.
        cp=isolated/'forward/loop2/output/collection.json';c=json.loads(cp.read_bytes());c['refinement'][-1]['difference_interval']=['1','2'];cp.write_text(json.dumps(c))
        target=isolated/'forged-admission.json';proc=subprocess.run([sys.executable,str(isolated/'replay_evidence.py'),str(target)],cwd=isolated,capture_output=True,text=True,timeout=120)
        check('cold independent arithmetic rejects forged passed difference',proc.returncode!=0 and not target.exists())
    check('all frozen sources and saved results unchanged',m.snapshot()==frozen and all((root/name).read_bytes()==raw for name,raw in reviewed.items()))
    report={'schema':'ym16-independent-adapter-review-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'reviewed_source_sha256':{name:digest(raw) for name,raw in reviewed.items()},'reviewer_source_sha256':digest(Path(__file__).read_bytes()),
      'frozen_inputs':len(frozen),'routes':12,'proved_routes':3,'blocked_routes':9,
      'limits':['Reviewed finite Horn-rule obligations, not a formal proof-assistant kernel.','Actual two-front search and separately reconstructed ordered certificates are distinct checks.','Uniform local theorem, physical scale, generator and continuum premises are not supplied by finite arithmetic.']}
    (out/'review.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks),'routes':12}));return report


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--round-dir',required=True);parser.add_argument('--output',required=True);args=parser.parse_args();audit(args.round_dir,args.output)
