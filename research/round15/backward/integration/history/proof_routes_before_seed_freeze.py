#!/usr/bin/env python3
"""Actual two-front conventional-proof planning with fresh evidence admission."""
from pathlib import Path
from types import MappingProxyType
import argparse,hashlib,importlib.util,json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
CORE_HASH='07b5b397af86b6bf5a481b114844c6252046e8ca2b5604dac7d158091632be94'
SOURCE_BYTES=Path(__file__).read_bytes()
# This inventory digest is frozen after the six scientific gates and before review.
INVENTORY_HASH='b2fb1cfd608d7d56fffb970de617cdc821ebf037d4495ef47ab0bbcea3fe5788'
HYPOTHESES=frozenset({'finite_measure','fixed_interval','cube_measure','physical_cube'})
GATES=frozenset({'derivative_gate','cover_gate','graph_gate','cube_tail_gate','cube_target_gate','free_gap_gate','minmax_gate','trial_haar_gate','trial_interval_gate'})
OPEN=frozenset({'local_uniform_constants','matched_generator','continuum_axioms','nontrivial_limit','volume_family_contract','uniform_energy_scale','uniform_smallness','controlled_spectral_limit','uniform_gap','ym_gap'})
STATEMENTS=MappingProxyType({
 'finite_measure':'Round14 SU(2)^2 normalized Haar deformation with k1=k2=1.',
 'fixed_interval':'The complete closed eta interval[1/8,1/4], unchanged through refinement.',
 'derivative_gate':'Reviewed centered derivative and |C prime|<=2; independent algebra replayed.',
 'cover_gate':'All exact point values, transported cells, endpoints and transitions replayed.',
 'bounded_support':'The three normalized traces lie in[-1,1].',
 'derivative_transport':'Point enclosure transports across each cell with error2*radius.',
 'complete_union':'The canonical21-cell union equals the original closed target.',
 'interval_positive':'Finite covariance is strictly positive throughout the original interval.',
 'cube_measure':'Product normalized SU(2) link Haar and actual closed cube Wilson action.',
 'graph_gate':'Actual signed cube words and independent character/index contract reviewed.',
 'cube_tail_gate':'Independent tensor-power oracle replays total Taylor and both normalization tails.',
 'cube_target_gate':'k1/4 degree24 expectation width<1e-12 and positive partition excess replayed.',
 'cube_haar':'Closed-sphere character gluing retains dimension power minus4.',
 'cube_polynomials':'Exact partition and distinct-six-face insertion Taylor polynomials.',
 'cube_enclosures':'Whole-action remainder and positive normalization enclose the finite observables.',
 'cube_nonfactorization':'At k1/4 the six independent-face partition approximation is rigorously excluded.',
 'physical_cube':'Physical untruncated cube link Haar Hilbert space; all Gauss constraints, no charges, alpha>0.',
 'free_gap_gate':'Reviewed active spin-network support argument; exact graphgirth and free gap replayed.',
 'minmax_gate':'Reviewed bounded-potential min-max lower bound on full E1 and Haar E0 upper bound.',
 'trial_haar_gate':'Independent B1 repeated Haar moments validate the trial Gram and Hamiltonian entries.',
 'trial_interval_gate':'Independent exact radical enclosure and central lambda=alpha/2 target replayed.',
 'free_physical_gap':'The cube free physical gap is exactly3alpha.',
 'excited_lower':'The full second eigenvalue is at least3alpha-sum|lambda_p|.',
 'trial_ground_upper':'The reviewed Haar trial space yields E0<=(3alpha-sqrt(9alpha^2+sum lambda_p^2))/2.',
 'finite_gap_bound':'The separate full E1 lower and trial E0 upper imply a finite physical gap inequality.',
 'improved_boundary':'At six common lambda=alpha/2 the improved physical gap bound is positive.',
 'local_uniform_constants':'An explicit valid local stability threshold independent of graph volume.',
 'volume_family_contract':'The full growing-volume family satisfies common source-theorem/locality, operator and boundary hypotheses.',
 'uniform_energy_scale':'A common physical energy normalization is fixed with alpha>=alpha_min>0 throughout the family.',
 'uniform_smallness':'The actual couplings satisfy the explicit volume-independent stability threshold.',
 'controlled_spectral_limit':'The spectral lower bound transfers in matched physical units through the controlled continuum limit.',
 'uniform_gap':'A common positive physical gap survives the required growing-volume family.',
 'matched_generator':'The intended continuum physical vacuum, generator and units are reconstructed.',
 'continuum_axioms':'The required four-dimensional continuum construction and reconstruction axioms.',
 'nontrivial_limit':'The constructed limit is nontrivial pure nonabelian Yang-Mills.',
 'ym_gap':'Nontrivial four-dimensional Yang-Mills existence and positive physical mass gap.'})
RULES=(
 ('a01',('finite_measure',),'bounded_support'),
 ('a02',('bounded_support','derivative_gate'),'derivative_transport'),
 ('a03',('fixed_interval','cover_gate'),'complete_union'),
 ('a04',('complete_union','derivative_transport','cover_gate'),'interval_positive'),
 ('b01',('cube_measure','graph_gate'),'cube_haar'),
 ('b02',('cube_haar','cube_tail_gate'),'cube_polynomials'),
 ('b03',('cube_polynomials','cube_tail_gate'),'cube_enclosures'),
 ('b04',('cube_enclosures','cube_target_gate'),'cube_nonfactorization'),
 ('c01',('physical_cube','free_gap_gate'),'free_physical_gap'),
 ('c02',('free_physical_gap','minmax_gate'),'excited_lower'),
 ('c03',('physical_cube','graph_gate','trial_haar_gate'),'trial_ground_upper'),
 ('c04',('excited_lower','trial_ground_upper'),'finite_gap_bound'),
 ('c05',('finite_gap_bound','trial_interval_gate'),'improved_boundary'),
 ('u01',('local_uniform_constants','volume_family_contract','uniform_energy_scale','uniform_smallness'),'uniform_gap'),
 ('y01',('uniform_gap','matched_generator','continuum_axioms','nontrivial_limit','controlled_spectral_limit'),'ym_gap'))
RULE_BYTES=json.dumps(RULES,separators=(',',':'))
class ContractError(ValueError):pass
def sha(raw):return hashlib.sha256(raw).hexdigest()
def regular(root,name):
    p=Path(root)
    if Path(name).is_absolute() or '..' in Path(name).parts:raise ContractError('Invalid source path')
    for part in Path(name).parts:
        p/=part
        if p.is_symlink():raise ContractError('Symlink input')
    if not p.is_file():raise ContractError('Missing input '+name)
    return p.read_bytes()
def snapshot(root=HERE):
    inv=regular(root,'proof_inputs.json')
    if sha(inv)!=INVENTORY_HASH:raise ContractError('Changed reviewed inventory')
    expected=json.loads(inv)
    if type(expected) is not dict or not expected or any(type(h) is not str or len(h)!=64 for h in expected.values()):raise ContractError('Invalid inventory')
    f={n:regular(root,n) for n in expected}
    if {n:sha(raw) for n,raw in f.items()}!=expected:raise ContractError('Frozen source changed')
    if f.get('proof_search.py') is None or sha(f['proof_search.py'])!=CORE_HASH:raise ContractError('Core changed')
    if regular(root,'proof_routes.py')!=SOURCE_BYTES:raise ContractError('Executing adapter differs from disk')
    return f

def fresh_admission(frozen):
    if type(frozen) is not dict or any(type(v) is not bytes for v in frozen.values()):raise ContractError('Frozen bytes required')
    inv=regular(HERE,'proof_inputs.json')
    if sha(inv)!=INVENTORY_HASH or {n:sha(v) for n,v in frozen.items()}!=json.loads(inv):raise ContractError('Incomplete or changed frozen evidence')
    if json.dumps(RULES,separators=(',',':'))!=RULE_BYTES:raise ContractError('In-memory rule semantics changed')
    # Every import occurs in a fresh interpreter over exactly the reviewed byte snapshot.
    # Temporary replays live outside the research tree and cannot enter its package.
    with tempfile.TemporaryDirectory(prefix='ym15-admission-',dir=HERE.parents[2]) as name:
        root=Path(name)
        for path,raw in frozen.items():
            p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        result=root/'admission.json'
        proc=subprocess.run([sys.executable,str(root/'replay_evidence.py'),str(result)],cwd=root,capture_output=True,text=True,timeout=120)
        if proc.returncode:raise ContractError('Independent replay failed: '+proc.stderr[-1200:])
        accepted=json.loads(result.read_bytes())
        if accepted.get('status')!='passed' or set(accepted.get('gates',[]))!=GATES:raise ContractError('Required arithmetic gate absent')
    return accepted

def library(frozen,goal,removed=()):
    if goal not in STATEMENTS:raise ContractError('Unknown target')
    if not isinstance(removed,(tuple,list,set,frozenset)) or len(removed)!=len(set(removed)) or not set(removed)<=HYPOTHESES|GATES:raise ContractError('Unsupported seed mutation')
    # No caller-supplied passed record can seed facts: recompute evidence at admission.
    accepted=fresh_admission(frozen)
    atoms={goal};selected=[]
    changed=True
    while changed:
        changed=False
        for rule in RULES:
            if rule[2] in atoms and rule not in selected:selected.append(rule);atoms.update(rule[1]);changed=True
    selected.sort();deps={n:({n} if n in HYPOTHESES|GATES|OPEN else set()) for n in atoms}
    for _ in atoms:
        for _,p,c in selected:deps[c]=set().union(*(deps[x] for x in p))
    lib={'nodes':[{'id':n,'statement':STATEMENTS[n],'scope':'round15-declared-contract','kind':'declared_hypothesis' if n in HYPOTHESES else 'target' if n in OPEN else 'theorem','assumption_ids':sorted(deps[n]-{n}),'verification':'Reviewed conventional proof and independently replayed arithmetic; no formal-kernel claim.','source':'Frozen round15 derivations and independent evidence','version':'15.1'} for n in sorted(atoms)],
      'rules':[{'id':i,'premises':list(p),'conclusion':c,'cost':1,'scope':'round15-declared-contract','proof_ref':'Reviewed rule '+i,'review_status':'reviewed'} for i,p,c in selected],
      'initial_facts':sorted(((HYPOTHESES|GATES)-set(removed))&atoms),'goals':[goal],'conditional_assumptions':[],'blocked_goals':[]}
    return lib,accepted

def ordered_replay(lib,steps):
    known=set(lib['initial_facts']);rules={r['id']:r for r in lib['rules']}
    for step in steps:
        if step not in rules or not set(rules[step]['premises'])<=known:raise ContractError('Invalid ordered certificate')
        known.add(rules[step]['conclusion'])
    if not set(lib['goals'])<=known:raise ContractError('Incomplete certificate')
    return {'passed':True,'steps':len(steps),'cost':len(steps)}
def execute(output):
    frozen=snapshot();spec=importlib.util.spec_from_file_location('ym15_frozen_core',HERE/'proof_search.py');core=importlib.util.module_from_spec(spec);sys.modules[spec.name]=core
    exec(compile(frozen['proof_search.py'],str(HERE/'proof_search.py'),'exec'),core.__dict__)
    cases=[('A_complete_interval','interval_positive',(),'proved'),('B_cube_nonfactorization','cube_nonfactorization',(),'proved'),('C_improved_boundary','improved_boundary',(),'proved')]
    for name,goal,gate in [('A_missing_cover','interval_positive','cover_gate'),('A_missing_derivative','interval_positive','derivative_gate'),('B_missing_graph','cube_nonfactorization','graph_gate'),('B_missing_tail','cube_nonfactorization','cube_tail_gate'),('C_missing_graph','improved_boundary','graph_gate'),('C_missing_minmax','improved_boundary','minmax_gate'),('C_missing_trial_moments','improved_boundary','trial_haar_gate'),('C_missing_interval','improved_boundary','trial_interval_gate')]:cases.append((name,goal,(gate,),'not_derivable'))
    cases += [('original_uniform_goal','uniform_gap',(),'not_derivable'),('unmatched_generator','matched_generator',(),'not_derivable'),('four_dimensional_yang_mills','ym_gap',(),'not_derivable')]
    routes={};accepted=None
    for name,goal,removed,expected in cases:
        lib,accepted=library(frozen,goal,removed);result=core.plan(lib,max_states=10000,max_backward_states=10000)
        if result['status']!=expected:raise ContractError('Unexpected route '+name)
        if expected=='proved':
            check=ordered_replay(lib,[r['rule_id'] for r in result['certified_proof']['steps']])
            if not result.get('first_meeting_candidate',{}).get('passed') or result['certified_cost']!=check['cost']:raise ContractError('Unverified meeting')
            result['independent_ordered_replay']=check
        routes[name]={'library':lib,'result':result}
    out={'status':'passed','arithmetic':accepted,'source_sha256':{n:sha(v) for n,v in frozen.items()},'adapter_sha256':sha(SOURCE_BYTES),'routes':routes,'scope':'Actual two-front search and separately replayed conventional rules, not formal-kernel theorem discovery.'}
    Path(output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print(json.dumps({'status':'passed','routes':len(routes),'proved':3}));return out
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(HERE/'proof_results.json'));execute(parser.parse_args().output)
