#!/usr/bin/env python3
"""Bidirectional finite dependency search; fresh evidence, no missing premises seeded."""
from pathlib import Path
from types import MappingProxyType
import argparse,hashlib,importlib.util,json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
CORE_HASH='07b5b397af86b6bf5a481b114844c6252046e8ca2b5604dac7d158091632be94'
INVENTORY_HASH='12d00d4300632606095b321cb27b82d3a583eb5603e939ffb5b33285fc59827b'
SOURCE_BYTES=Path(__file__).read_bytes()
HYPOTHESES=frozenset(['admissible_gram', 'bridge_geometry', 'central_dot_observables', 'cluster_support', 'coefficient_box', 'common_scale', 'conditional_coefficient', 'dense_two_cube', 'endpoint_magnitudes', 'rotor_contract', 'six_face_conditional', 'standard_bare_matching', 'summable_schedule'])
GATES=frozenset({'a2_gate', 'c2_gate', 'a1_gate', 'c1_gate', 'b2_gate', 'b1_gate'})
OPEN=frozenset({'full_bulk_contraction', 'dense_uniform_gap', 'ym_gap', 'matched_generator', 'continuum_axioms', 'dense_overlap_control', 'nontrivial_limit', 'dense_coupling_smallness', 'controlled_spectral_limit', 'applicable_rotor_stability'})
STATEMENTS=MappingProxyType({'rotor_contract': 'Open finite cubic SU(2) Haar link rotors, untruncated Casimir j(j+1), all-vertex Gauss law, no charges, alpha>0 and real magnetic couplings in energy units.', 'bridge_geometry': 'The actual three-square strip has disjoint end-block links and untouched middle links, with |lambda_end|<=alpha/2 and |mu|<=alpha/8.', 'cluster_support': 'Complete xy strips at (4i,2j,z) fit the open n-vertex box; all electric links are retained; internally overlapping cluster supports are mutually link-disjoint.', 'summable_schedule': 'Every remaining face has coefficient alpha*tau*2^(-x-y-z)/24, with 0<|tau|<=1/64; every actual cluster coupling is nonzero and satisfies the bridge limits.', 'common_scale': 'All family members satisfy alpha_N>=alpha_min>0 in the same physical energy unit.', 'dense_two_cube': 'Actual 12-vertex,20-link,11-face two-cube graph; P spans the physical vacuum and all eleven fundamental face characters.', 'coefficient_box': 'Every one of the eleven real couplings satisfies |lambda_p|<=3alpha/8 on this same finite graph.', 'endpoint_magnitudes': 'Every |lambda_p|=3alpha/8, with the signed physical star trial on the same finite graph.', 'central_dot_observables': 'The declared central observable and weight depend only on the dot products of a Haar S3 coordinate with b,a1,a2,a3,a4.', 'admissible_gram': 'The complete real joint Gram is positive semidefinite, rank at most four, with unit a_i and exact b=sum kappa_i a_i constraints.', 'six_face_conditional': 'The actual four-cube graph integrates central U and surrounding V, fixes the other31 links to identity, and retains all six affected face weights.', 'conditional_coefficient': 'The two-link static action is kappa(3x+2y+w) at the frozen kappa=1/64 and the declared observable; this coefficient is not a physical time generator.', 'a1_gate': 'Fresh independent dressed-reference Haar, graph and spectral-transfer checks, with reviewed domains.', 'a2_gate': 'Fresh independent all-volume support proof checks, finite coefficient ledgers, common-scale and zero-case controls.', 'b1_gate': 'Fresh independent complete low-energy support classification and full cross-complement moment calculations.', 'b2_gate': 'Fresh independent full-operator codimension-one inequality, continuous coefficient box and radical enclosures.', 'c1_gate': 'Fresh independent complete Gram validation and central moment/invariance checks.', 'c2_gate': 'Fresh independent two-link moment integration, all affected weights and complete normalization error checks.', 'dressed_haar': 'The bridge has zero mean and second moment1/4 in the actual dressed reference ground.', 'bridge_gap': 'Separate full-link min-max E1 and reference Rayleigh E0 bounds imply a unique gauge-invariant full-link ground and full-link gap at leastalpha/8, hence the same physical strip lower bound.', 'cluster_reference': 'Repeated disjoint full-link clusters and free links give a unique product reference ground with gap at leastalpha/8.', 'remainder_zero_mean': 'Every remaining face has an untouched free link and zero expectation in the dressed cluster reference.', 'summable_norm': 'The norm of the complete remaining interaction is at mostalpha/64 by the positive orthant weight sum.', 'inhomogeneous_dimensionless_gap': 'The specified full-support, spatially decaying family has physical gap/alpha at least7/64.', 'inhomogeneous_physical_gap': 'The specified inhomogeneous finite-volume family has common physical gap at least7alpha_min/64.', 'complete_complement': 'The H0-reducing physical P omits no state below9alpha/2, and an actual six-edge loop attains this complement threshold.', 'cross_gram': 'The full W=QVP obeys W*W=PV^2P-(PVP)^2 with the declared exact eleven-face coefficient matrix.', 'complement_control': 'The complete Q electric threshold and exact full cross Gram are established on the declared finite graph.', 'full_excited_bound': 'A codimension-one min-max form on Omega-perp gives the full physical E1 lower bound alpha(27-3sqrt70)/16 throughout the coefficient box.', 'finite_box_gap': 'The separate vacuum E0 upper bound yields physical gap at leastalpha(27-3sqrt70)/16>0 on the declared finite graph and entire signed box.', 'endpoint_upper': 'A signed physical star trial gives E0/alpha<=(24-15sqrt3)/16 at the endpoint magnitudes.', 'finite_endpoint_gap': 'Combining full E1 and actual endpoint Rayleigh E0 yields gap at leastalpha(3+15sqrt3-3sqrt70)/16.', 'gram_isometry': 'Equal valid joint Grams determine a span isometry that extends to O(4), including singular configurations.', 'central_gram_closure': 'The complete Gram identifies the declared central Haar integrals; it does not specify an independently transformed surrounding measure.', 'joint_link_moments': 'Independent Haar U,V induce correlated x,y,w moments with the full character dimension factor, not three independent traces.', 'controlled_two_link': 'The complete six-weight two-link normalized expectation has a certified numerator and partition error at the frozen coefficient.', 'dense_overlap_control': 'A quantitative uniform local estimate for the nondecaying overlapping rotor interactions, including their offdiagonal terms.', 'applicable_rotor_stability': 'A proved rotor-applicable stability implication with all numerical constants, domains and overlap hypotheses explicit.', 'dense_coupling_smallness': "The homogeneous dense family satisfies that theorem's numerical smallness hypotheses uniformly.", 'dense_uniform_gap': 'A positive physical gap uniform over the homogeneous nondecaying-coupling volumes.', 'full_bulk_contraction': 'All surrounding links and all twenty face weights have been integrated with complete normalization control.', 'matched_generator': 'A physical vacuum and time generator matched to the required reconstructed measure.', 'continuum_axioms': 'The continuum construction satisfies the required reconstruction axioms.', 'nontrivial_limit': 'A nontrivial four-dimensional pure Yang-Mills limit has been constructed.', 'controlled_spectral_limit': 'The spectral lower bound survives the required volume and spacing limits.', 'ym_gap': 'Four-dimensional quantum Yang-Mills existence and a positive mass gap.', 'standard_bare_matching': 'The positive homogeneous SU(2) convention has alpha=g^2/(2a), lambda=2/(g^2a), g,a>0, after removing the declared additive constant.', 'weak_bare_domain_obstruction': 'The selected r<=3/8 box under the matched convention requires g^4>=32/3 and therefore does not cover the g->0 path. This is an applicability obstruction, not a no-gap theorem.', 'outer_gram_reduction': 'For the identity-boundary two-link model, G(y) with b=kappa(3e0+V) is admissible, including rank-one endpoints. The exact outer semicircle integral retains exp(2kappa*y) and the conditional partition, and equals the declared two-link integral.'})
RULES=(('A1', ('rotor_contract', 'bridge_geometry', 'a1_gate'), 'dressed_haar'), ('A2', ('dressed_haar', 'rotor_contract', 'bridge_geometry', 'a1_gate'), 'bridge_gap'), ('A3', ('bridge_gap', 'cluster_support', 'a2_gate'), 'cluster_reference'), ('A4', ('cluster_reference', 'cluster_support', 'a2_gate'), 'remainder_zero_mean'), ('A5', ('rotor_contract', 'summable_schedule', 'a2_gate'), 'summable_norm'), ('A6', ('cluster_reference', 'remainder_zero_mean', 'summable_norm', 'a2_gate'), 'inhomogeneous_dimensionless_gap'), ('A7', ('inhomogeneous_dimensionless_gap', 'common_scale'), 'inhomogeneous_physical_gap'), ('B1', ('rotor_contract', 'dense_two_cube', 'b1_gate'), 'complete_complement'), ('B2', ('rotor_contract', 'dense_two_cube', 'b1_gate'), 'cross_gram'), ('B3', ('complete_complement', 'cross_gram'), 'complement_control'), ('B4', ('complement_control', 'coefficient_box', 'b2_gate'), 'full_excited_bound'), ('B5', ('full_excited_bound', 'rotor_contract', 'b2_gate'), 'finite_box_gap'), ('B6', ('rotor_contract', 'dense_two_cube', 'endpoint_magnitudes', 'b2_gate'), 'endpoint_upper'), ('B7', ('full_excited_bound', 'endpoint_upper'), 'finite_endpoint_gap'), ('C1', ('admissible_gram', 'c1_gate'), 'gram_isometry'), ('C2', ('gram_isometry', 'central_dot_observables', 'c1_gate'), 'central_gram_closure'), ('C3', ('six_face_conditional', 'c2_gate'), 'joint_link_moments'), ('C4', ('joint_link_moments', 'conditional_coefficient', 'c2_gate'), 'controlled_two_link'), ('U1', ('rotor_contract', 'dense_overlap_control', 'applicable_rotor_stability', 'dense_coupling_smallness', 'common_scale'), 'dense_uniform_gap'), ('Y1', ('dense_uniform_gap', 'matched_generator', 'continuum_axioms', 'nontrivial_limit', 'controlled_spectral_limit'), 'ym_gap'), ('B8', ('standard_bare_matching', 'coefficient_box', 'b2_gate'), 'weak_bare_domain_obstruction'), ('C5', ('central_gram_closure', 'joint_link_moments', 'six_face_conditional', 'conditional_coefficient', 'c2_gate'), 'outer_gram_reduction'))
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
    with tempfile.TemporaryDirectory(prefix='ym18-admission-') as temp:
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
        lib={'nodes':[{'id':n,'statement':STATEMENTS[n],'scope':'round18-declared-contract','kind':'declared_hypothesis' if n in HYPOTHESES else 'target' if n in OPEN else 'theorem','assumption_ids':sorted(deps[n]-{n}),'verification':'Reviewed conventional argument and freshly replayed independent arithmetic.','source':'Round18 frozen role evidence','version':'18.1'} for n in sorted(atoms)],'rules':[{'id':i,'premises':list(p),'conclusion':c,'cost':1,'scope':'round18-declared-contract','proof_ref':'Reviewed rule '+i,'review_status':'reviewed'} for i,p,c in selected],'initial_facts':sorted(((HYPOTHESES|GATES)-set(removed))&atoms),'goals':[goal],'conditional_assumptions':[],'blocked_goals':[]}
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
    frozen=snapshot();spec=importlib.util.spec_from_file_location('ym18_core',HERE/'proof_search.py');core=importlib.util.module_from_spec(spec);sys.modules[spec.name]=core
    exec(compile(frozen['proof_search.py'],str(HERE/'proof_search.py'),'exec'),core.__dict__)
    cases=[('dressed_bridge', 'bridge_gap', (), 'proved'), ('inhomogeneous_uniform_family', 'inhomogeneous_physical_gap', (), 'proved'), ('full_complement', 'complement_control', (), 'proved'), ('finite_coefficient_box', 'finite_box_gap', (), 'proved'), ('endpoint_improvement', 'finite_endpoint_gap', (), 'proved'), ('central_gram', 'central_gram_closure', (), 'proved'), ('two_link_integral', 'controlled_two_link', (), 'proved'), ('weak_bare_matching', 'weak_bare_domain_obstruction', (), 'proved'), ('outer_gram_connection', 'outer_gram_reduction', (), 'proved'), ('no_dressed_haar', 'bridge_gap', ('a1_gate',), 'not_derivable'), ('no_bridge_geometry', 'bridge_gap', ('bridge_geometry',), 'not_derivable'), ('no_clusters', 'inhomogeneous_physical_gap', ('cluster_support',), 'not_derivable'), ('no_decay_schedule', 'inhomogeneous_physical_gap', ('summable_schedule',), 'not_derivable'), ('no_common_scale', 'inhomogeneous_physical_gap', ('common_scale',), 'not_derivable'), ('no_cluster_gate', 'inhomogeneous_physical_gap', ('a2_gate',), 'not_derivable'), ('no_complete_complement', 'finite_box_gap', ('b1_gate',), 'not_derivable'), ('no_box', 'finite_box_gap', ('coefficient_box',), 'not_derivable'), ('no_spectral_gate', 'finite_box_gap', ('b2_gate',), 'not_derivable'), ('no_endpoint', 'finite_endpoint_gap', ('endpoint_magnitudes',), 'not_derivable'), ('no_gram_validity', 'central_gram_closure', ('admissible_gram',), 'not_derivable'), ('undeclared_observable', 'central_gram_closure', ('central_dot_observables',), 'not_derivable'), ('no_gram_gate', 'central_gram_closure', ('c1_gate',), 'not_derivable'), ('missing_face_weights', 'controlled_two_link', ('six_face_conditional',), 'not_derivable'), ('no_integral_gate', 'controlled_two_link', ('c2_gate',), 'not_derivable'), ('no_rotor_contract', 'bridge_gap', ('rotor_contract',), 'not_derivable'), ('no_dense_geometry', 'finite_box_gap', ('dense_two_cube',), 'not_derivable'), ('no_conditional_coefficient', 'controlled_two_link', ('conditional_coefficient',), 'not_derivable'), ('no_bare_matching', 'weak_bare_domain_obstruction', ('standard_bare_matching',), 'not_derivable'), ('no_central_gate_for_outer', 'outer_gram_reduction', ('c1_gate',), 'not_derivable'), ('no_joint_gate_for_outer', 'outer_gram_reduction', ('c2_gate',), 'not_derivable'), ('no_common_coefficient_for_outer', 'outer_gram_reduction', ('conditional_coefficient',), 'not_derivable'), ('homogeneous_dense_uniform', 'dense_uniform_gap', (), 'not_derivable'), ('full_bulk', 'full_bulk_contraction', (), 'not_derivable'), ('continuum_yang_mills', 'ym_gap', (), 'not_derivable')]
    libs,accepted=build_libraries(frozen,[(g,r) for _,g,r,_ in cases]);routes={}
    for (name,goal,removed,expected),lib in zip(cases,libs):
        result=core.plan(lib,max_states=10000,max_backward_states=10000)
        if result['status']!=expected:raise ContractError('Unexpected route '+name)
        if expected=='proved':
            check=ordered_replay(lib,[s['rule_id'] for s in result['certified_proof']['steps']])
            if not result.get('first_meeting_candidate',{}).get('passed') or check['cost']!=result['certified_cost']:raise ContractError('Unchecked meeting')
            result['independent_ordered_replay']=check
        routes[name]={'target':goal,'library':lib,'result':result}
    report={'status':'passed','arithmetic':accepted,'source_sha256':{n:sha(v) for n,v in frozen.items()},'adapter_sha256':sha(SOURCE_BYTES),'routes':routes,'scope':'Nine conventional result/connection routes from six loops and withdrawn/open-premise controls; this is not a formal proof kernel or a continuum construction.'}
    Path(output).write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');print(json.dumps({'status':'passed','routes':len(routes),'proved':9}));return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);execute(p.parse_args().output)
