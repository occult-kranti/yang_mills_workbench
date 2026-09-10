#!/usr/bin/env python3
"""Bidirectional finite dependency search; fresh evidence, no missing premises seeded."""
from pathlib import Path
from types import MappingProxyType
import argparse,hashlib,importlib.util,json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
CORE_HASH='07b5b397af86b6bf5a481b114844c6252046e8ca2b5604dac7d158091632be94'
INVENTORY_HASH='971eeec347f8136f6e5ab3fa89df57e08612cadb93406d6311e0be7bfa4a3bf6'
SOURCE_BYTES=Path(__file__).read_bytes()
HYPOTHESES=frozenset({'rotor_contract','sparse_support','common_scale','dense_two_cube','four_cube_contract','conditional_boundary','endpoint_trial'})
GATES=frozenset({'a1_gate','a2_gate','b1_gate','b2_gate','c1_gate','c2_gate'})
OPEN=frozenset({'applicable_rotor_stability','dense_coupling_smallness','dense_overlap_control','dense_uniform_gap','full_bulk_contraction','matched_generator','continuum_axioms','nontrivial_limit','controlled_spectral_limit','ym_gap'})
STATEMENTS=MappingProxyType({
 'rotor_contract':'Open finite cubic SU(2) link rotors, normalized Haar, Casimir j(j+1), all-vertex Gauss law, no external charges; alpha>0 and real plaquette couplings in energy units.',
 'sparse_support':'Nonzero plaquette terms have pairwise disjoint LINK supports, with max|lambda_p|/alpha<=rho<3/4; shared vertices are allowed.',
 'common_scale':'For this family, all alpha_N>=alpha_min>0 in one physical energy unit.',
 'dense_two_cube':'Actual two-cube graph, eleven face terms and twelve-character trial at the declared couplings; physical free gap3alpha.',
 'endpoint_trial':'All eleven lambda_p/alpha=12/43, and the declared adjoint trial amplitude eta=3/3817; same fixed dense finite Hamiltonian.',
 'four_cube_contract':'The actual four-cube2x2x1 complex and its central link are defined independently of the outer boundary.',
 'conditional_boundary':'The specified surrounding link variables are fixed boundary data; only the central link is integrated.',
 'a1_gate':'Independent exact local operator/graph/trial checks and the written form-domain argument have been replayed.',
 'a2_gate':'Independent sparse-support mask, spectral constants, gauge-invariant ground argument and rejecting controls have been replayed.',
 'b1_gate':'Independent physical trial Gram, electric/magnetic elements and full E1 bound have been replayed.',
 'b2_gate':'Independent added-representation trial and exact finite endpoint-repair inequality have been replayed.',
 'c1_gate':'Independent actual graph, central invariant-space dimension and Haar projector have been replayed.',
 'c2_gate':'Independent equal-action tetrahedral/commuting conditional expectations, complete numerator and partition remainders, and zero-action-vector controls have been replayed.',
 'local_split':'The magnetic multiplier splits into a vacuum-diagonal term and a nonzero vacuum-offdiagonal term of norm1/2.',
 'diagonal_bound':'The diagonal term has the uniform form coefficient16 max|lambda_p|/(3alpha); this does not bound the entire perturbation.',
 'relative_counterexample':'The physical trial gives |<V>|/<H0>=|lambda_p|/(3alpha|t|), unbounded as t approaches0 for nonzero lambda_p.',
 'block_factorization':'The full link Hilbert space and Hamiltonian factor into four-link interacting blocks and free links.',
 'block_gap':'Each block has a unique ground with excitation lower bound alpha(3/4-rho).',
 'invariant_ground':'The unique product ground is invariant under the global SU(2) vertex gauge group and lies in the physical sector.',
 'sparse_dimensionless_gap':'Restricting to the physical sector retains the ground and cannot lower its excitation threshold, so Delta/alpha>=3/4-rho.',
 'sparse_physical_gap':'The sparse-support family has Delta>=alpha_min(3/4-rho)>0 uniformly in its finite volumes.',
 'trial_gram':'The vacuum and eleven fundamental characters give the declared exact twelve-state Gram and Hamiltonian matrices.',
 'excited_lower':'The full physical first excited energy is bounded below by3alpha-sum|lambda_p|.',
 'trial_upper':'Rayleigh-Ritz gives a ground-energy upper bound from the exact physical trial matrix.',
 'finite_gap_bound':'Combining the full E1 lower bound and trial E0 upper bound yields the improved finite sufficient gap inequality.',
 'adjoint_trial':'One shared-face adjoint component with an independently checked variational amplitude gives a strictly better trial energy at the tested endpoint.',
 'finite_endpoint_repair':'At the frozen endpoint, the separate full E1 bound and the enlarged trial give a strictly positive physical gap lower bound.',
 'four_cube_graph':'The full four-cube complex contains the central four-valent link absent from the outer-boundary-only complex.',
 'rank_three_projector':'Four central adjoint representations have a rank-three invariant Haar projector with nontrivial pairing coefficients.',
 'conditional_kernel':'At zero central coupling the complete Haar projector contracts the declared boundary data; nonzero coupling requires weighted moments.',
 'channel_contrast':'At the declared nonzero coupling the two realized boundaries have the same conditional action vector and partition function but different joint expectations; the complete rational enclosures retain observable geometry.',
 'dense_overlap_control':'An explicit quantitative local estimate for overlapping rotor interactions, including the vacuum-offdiagonal term.',
 'applicable_rotor_stability':'A proved stability implication applicable to the declared infinite-dimensional rotors, four-link interactions, domains, overlap geometry and local estimate, with all constants explicit.',
 'dense_coupling_smallness':'The declared dense family satisfies the explicit numerical smallness hypotheses of that applicable stability implication uniformly over its finite volumes.',
 'dense_uniform_gap':'A positive volume-uniform physical gap for the dense overlapping Hamiltonian family.',
 'full_bulk_contraction':'The surrounding link integrations and all face weights have been controlled for the full four-cube bulk observable.',
 'matched_generator':'A physical vacuum and time generator matched to the required reconstructed measure.',
 'continuum_axioms':'The required continuum reconstruction axioms have been proved for the constructed theory.',
 'nontrivial_limit':'A nontrivial four-dimensional pure Yang-Mills continuum limit has been constructed.',
 'controlled_spectral_limit':'The spectral lower bound survives the required volume and spacing limits.',
 'ym_gap':'Four-dimensional quantum Yang-Mills existence and positive mass gap.'})
RULES=(
 ('A1',('rotor_contract','a1_gate'),'local_split'),
 ('A2',('local_split','a1_gate'),'diagonal_bound'),
 ('A3',('local_split','a1_gate'),'relative_counterexample'),
 ('S1',('rotor_contract','sparse_support','a2_gate'),'block_factorization'),
 ('S2',('block_factorization','a2_gate'),'block_gap'),
 ('S3',('block_gap','a2_gate'),'invariant_ground'),
 ('S4',('block_gap','invariant_ground'),'sparse_dimensionless_gap'),
 ('S5',('sparse_dimensionless_gap','common_scale'),'sparse_physical_gap'),
 ('B1',('rotor_contract','dense_two_cube','b1_gate'),'trial_gram'),
 ('B2',('rotor_contract','dense_two_cube','b1_gate'),'excited_lower'),
 ('B3',('trial_gram',),'trial_upper'),
 ('B4',('excited_lower','trial_upper'),'finite_gap_bound'),
 ('B5',('trial_gram','endpoint_trial','b2_gate'),'adjoint_trial'),
 ('B6',('adjoint_trial','excited_lower'),'finite_endpoint_repair'),
 ('C1',('four_cube_contract','c1_gate'),'four_cube_graph'),
 ('C2',('four_cube_graph','c1_gate'),'rank_three_projector'),
 ('C3',('rank_three_projector','conditional_boundary','c1_gate'),'conditional_kernel'),
 ('C4',('conditional_kernel','c2_gate'),'channel_contrast'),
 ('U1',('rotor_contract','dense_overlap_control','applicable_rotor_stability','dense_coupling_smallness','common_scale'),'dense_uniform_gap'),
 ('Y1',('dense_uniform_gap','matched_generator','continuum_axioms','nontrivial_limit','controlled_spectral_limit'),'ym_gap'),
)
def semantics():
    return json.dumps({'hypotheses':sorted(HYPOTHESES),'gates':sorted(GATES),'open':sorted(OPEN),'statements':dict(STATEMENTS),'rules':RULES},sort_keys=True,separators=(',',':'))
DECLARED_SEMANTICS=semantics()
class ContractError(ValueError):pass
def check_semantics():
    if semantics()!=DECLARED_SEMANTICS:raise ContractError('In-memory proof declarations changed')
def sha(raw):return hashlib.sha256(raw).hexdigest()
def regular(root,name):
    if not isinstance(name,str) or Path(name).is_absolute() or '..' in Path(name).parts:raise ContractError('Invalid source path')
    p=Path(root)
    for part in Path(name).parts:
        p/=part
        if p.is_symlink():raise ContractError('Symlink evidence')
    if not p.is_file():raise ContractError('Missing source '+name)
    return p.read_bytes()
def snapshot(root=HERE):
    raw=regular(root,'proof_inputs.json')
    if sha(raw)!=INVENTORY_HASH:raise ContractError('Changed reviewed inventory')
    expected=json.loads(raw)
    if type(expected) is not dict or not expected:raise ContractError('Invalid inventory')
    frozen={name:regular(root,name) for name in expected}
    if {n:sha(b) for n,b in frozen.items()}!=expected:raise ContractError('Changed frozen source')
    if sha(frozen.get('proof_search.py',b''))!=CORE_HASH:raise ContractError('Changed search core')
    if regular(root,'proof_routes.py')!=SOURCE_BYTES:raise ContractError('Adapter changed after import')
    check_semantics();return frozen
def fresh_admission(frozen):
    raw=regular(HERE,'proof_inputs.json')
    if type(frozen) is not dict or any(type(v) is not bytes for v in frozen.values()) or sha(raw)!=INVENTORY_HASH or {n:sha(b) for n,b in frozen.items()}!=json.loads(raw):raise ContractError('Incomplete or changed frozen bytes')
    check_semantics()
    with tempfile.TemporaryDirectory(prefix='ym17-admission-') as temp:
        root=Path(temp)
        for name,data in frozen.items():
            p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        output=root/'admission.json'
        proc=subprocess.run([sys.executable,str(root/'replay_evidence.py'),str(output)],cwd=root,capture_output=True,text=True,timeout=300)
        if proc.returncode:raise ContractError('Independent fresh replay failed: '+proc.stderr[-1800:])
        result=json.loads(output.read_bytes())
        if result.get('status')!='passed' or set(result.get('gates',[]))!=GATES:raise ContractError('Incomplete arithmetic admission')
    check_semantics();return result
def build_libraries(frozen,cases):
    # Batch admission performs the same six independent computations once for this
    # complete set of routes. No external passed object can seed a proof library.
    accepted=fresh_admission(frozen);libraries=[]
    for goal,removed in cases:
        if goal not in STATEMENTS or type(removed) is not tuple or len(set(removed))!=len(removed) or not set(removed)<=HYPOTHESES|GATES:raise ContractError('Invalid target/withdrawal')
        atoms={goal};selected=[];changed=True
        while changed:
            changed=False
            for rule in RULES:
                if rule[2] in atoms and rule not in selected:
                    selected.append(rule);atoms.update(rule[1]);changed=True
        selected.sort();deps={n:({n} if n in HYPOTHESES|GATES|OPEN else set()) for n in atoms}
        for _ in atoms:
            for _,p,c in selected:deps[c]=set().union(*(deps[x] for x in p))
        lib={'nodes':[{'id':n,'statement':STATEMENTS[n],'scope':'round17-declared-contract','kind':'declared_hypothesis' if n in HYPOTHESES else 'target' if n in OPEN else 'theorem','assumption_ids':sorted(deps[n]-{n}),'verification':'Reviewed conventional argument and freshly replayed independent arithmetic.','source':'Round17 frozen role evidence','version':'17.1'} for n in sorted(atoms)],'rules':[{'id':i,'premises':list(p),'conclusion':c,'cost':1,'scope':'round17-declared-contract','proof_ref':'Reviewed rule '+i,'review_status':'reviewed'} for i,p,c in selected],'initial_facts':sorted(((HYPOTHESES|GATES)-set(removed))&atoms),'goals':[goal],'conditional_assumptions':[],'blocked_goals':[]}
        libraries.append(lib)
    check_semantics();return libraries,accepted
def ordered_replay(lib,steps):
    known=set(lib['initial_facts']);rules={r['id']:r for r in lib['rules']}
    for step in steps:
        if step not in rules or not set(rules[step]['premises'])<=known:raise ContractError('Invalid ordered proof')
        known.add(rules[step]['conclusion'])
    if not set(lib['goals'])<=known:raise ContractError('Incomplete proof')
    return {'passed':True,'steps':len(steps),'cost':len(steps)}
def execute(output):
    frozen=snapshot();spec=importlib.util.spec_from_file_location('ym17_core',HERE/'proof_search.py');core=importlib.util.module_from_spec(spec);sys.modules[spec.name]=core
    exec(compile(frozen['proof_search.py'],str(HERE/'proof_search.py'),'exec'),core.__dict__)
    cases=[('local_obstruction','relative_counterexample',(),'proved'),('sparse_uniform_family','sparse_physical_gap',(),'proved'),('finite_trial_bound','finite_gap_bound',(),'proved'),('finite_endpoint_repair','finite_endpoint_repair',(),'proved'),('central_projector','rank_three_projector',(),'proved'),('conditional_channel_experiment','channel_contrast',(),'proved')]
    for name,goal,gate in [('missing_local','relative_counterexample','a1_gate'),('missing_sparse','sparse_physical_gap','a2_gate'),('missing_scale','sparse_physical_gap','common_scale'),('overlapping_support','sparse_physical_gap','sparse_support'),('missing_trial','finite_gap_bound','b1_gate'),('missing_adjoint','finite_endpoint_repair','b2_gate'),('missing_endpoint','finite_endpoint_repair','endpoint_trial'),('missing_graph','rank_three_projector','c1_gate'),('missing_kernel','channel_contrast','c2_gate')]:cases.append((name,goal,(gate,),'not_derivable'))
    cases += [('original_dense_uniform_goal','dense_uniform_gap',(),'not_derivable'),('full_bulk_integral','full_bulk_contraction',(),'not_derivable'),('four_dimensional_yang_mills','ym_gap',(),'not_derivable')]
    libs,accepted=build_libraries(frozen,[(g,r) for _,g,r,_ in cases]);routes={}
    for (name,goal,removed,expected),lib in zip(cases,libs):
        result=core.plan(lib,max_states=10000,max_backward_states=10000)
        if result['status']!=expected:raise ContractError('Unexpected route '+name)
        if expected=='proved':
            check=ordered_replay(lib,[s['rule_id'] for s in result['certified_proof']['steps']])
            if not result.get('first_meeting_candidate',{}).get('passed') or check['cost']!=result['certified_cost']:raise ContractError('Unchecked meeting')
            result['independent_ordered_replay']=check
        routes[name]={'target':goal,'library':lib,'result':result}
    report={'status':'passed','arithmetic':accepted,'source_sha256':{n:sha(v) for n,v in frozen.items()},'adapter_sha256':sha(SOURCE_BYTES),'routes':routes,'scope':'Six finite conventional result routes and withdrawn/open-premise controls; this is not a formal proof kernel or a continuum construction.'}
    Path(output).write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');print(json.dumps({'status':'passed','routes':len(routes),'proved':6}));return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);execute(p.parse_args().output)
