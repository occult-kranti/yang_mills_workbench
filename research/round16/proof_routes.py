#!/usr/bin/env python3
"""Two-front dependency search with freshly reconstructed finite evidence."""
from pathlib import Path
from types import MappingProxyType
import argparse,hashlib,importlib.util,json,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
CORE_HASH='07b5b397af86b6bf5a481b114844c6252046e8ca2b5604dac7d158091632be94'
SOURCE_BYTES=Path(__file__).read_bytes()
INVENTORY_HASH='71a9b8d4aa44f528d60585136df6de68dabda6cfa0cfa9b13546b5e0d8f130d3'
HYPOTHESES=frozenset({'two_cube_measure','target_parameters','physical_family'})
GATES=frozenset({'graph_gate','haar_gate','coefficient_gate','remainder_gate','difference_gate','scale_gate'})
OPEN=frozenset({'local_uniform_constants','volume_family_contract','uniform_dimensionless_gap','uniform_energy_scale','uniform_smallness','matched_generator','continuum_axioms','nontrivial_limit','controlled_spectral_limit','uniform_gap','ym_gap'})
STATEMENTS=MappingProxyType({
 'two_cube_measure':'Product normalized SU(2) link Haar on the actual adjacent-cube complex, with eleven distinct face terms.',
 'target_parameters':'All-eleven trace product, outer coefficients1/8, shared1/8 compared with0; same observable; width target1e-12 and total-degree cap24.',
 'physical_family':'Physical untruncated gauge-invariant finite graph Hamiltonians, Gauss at all vertices, no charges, H_N=alpha_N K_N with alpha_N>0 in a common unit.',
 'graph_gate':'Actual signed graph, disk decomposition and complete center-parity classification independently replayed.',
 'haar_gate':'Independent exact matrix-index shared-edge projector and class-polynomial Haar checks replayed.',
 'coefficient_gate':'Independent ordinary-character polynomial projection reconstructs total-degree numerator and partition coefficients.',
 'remainder_gate':'Complete action-dependent exponential and normalization errors independently reconstructed, including changed-action comparator.',
 'difference_gate':'The frozen primary normalized expectation difference has positive exact lower endpoint and width<=1e-12.',
 'scale_gate':'Exact scaling and free-box counterexample replayed; no interacting uniform dimensionless bound admitted.',
 'signed_complex':'The full11-face action differs from the outer10-face action; four links have incidence3.',
 'bounded_observable':'All normalized face traces and their all-eleven product have modulus at most1.',
 'disk_fusion':'Two five-face disk convolutions and a three-character Haar invariant give the graph-specific contraction.',
 'exact_coefficients':'Finite total-degree coefficients include each of the eleven insertions separately.',
 'positive_normalization':'Haar face means vanish and Jensen gives Z>=1 for either real finite action.',
 'tail_enclosure':'Whole-action remainder controls both signed numerators and partition functions.',
 'observable_intervals':'Exact rational quotient intervals enclose both finite expectations.',
 'shared_effect':'At the declared fixed parameters the shared interaction produces a strictly positive difference in the all-eleven observable.',
 'scale_identity':'Positive common-domain scalar multiplication gives Delta(H_N)=alpha_N Delta(K_N).',
 'scale_counterexample':'Free cubic boxes n>=2 have Delta(K_n)=3; alpha_n=1/n makes physical gaps3/n tend to0 despite zero dimensionless coupling.',
 'local_uniform_constants':'A reviewed applicable local-gap estimate or theorem, with explicit operator and overlap constants for the stated Hamiltonian family.',
 'volume_family_contract':'A reviewed common domain, locality and boundary contract for every volume.',
 'uniform_smallness':'A verified source-specific per-interaction smallness condition independent of plaquette count.',
 'uniform_dimensionless_gap':'A proved positive spectral lower bound d for every K_N in the stated family.',
 'uniform_energy_scale':'A declared and verified alpha_N>=alpha_min>0 in common physical units for the whole family.',
 'uniform_gap':'A common positive physical gap under both dimensionless and scale premises.',
 'matched_generator':'A physical vacuum and time generator matched to a valid reconstruction of the measures.',
 'continuum_axioms':'Required continuum reconstruction axioms and their applicability.',
 'nontrivial_limit':'A nontrivial four-dimensional pure Yang-Mills continuum construction.',
 'controlled_spectral_limit':'A proved transfer of physical spectral bounds through volume and spacing limits.',
 'ym_gap':'The four-dimensional pure Yang-Mills existence and positive mass-gap target.'})
RULES=(
 ('G1',('two_cube_measure','graph_gate'),'signed_complex'),
 ('G2',('two_cube_measure',),'bounded_observable'),
 ('G3',('signed_complex','haar_gate'),'disk_fusion'),
 ('E1',('disk_fusion','coefficient_gate'),'exact_coefficients'),
 ('E2',('signed_complex','haar_gate'),'positive_normalization'),
 ('E3',('bounded_observable','target_parameters','remainder_gate'),'tail_enclosure'),
 ('E4',('exact_coefficients','positive_normalization','tail_enclosure'),'observable_intervals'),
 ('E5',('observable_intervals','difference_gate'),'shared_effect'),
 ('S1',('physical_family','scale_gate'),'scale_identity'),
 ('S2',('scale_identity','scale_gate'),'scale_counterexample'),
 ('U1',('local_uniform_constants','volume_family_contract','uniform_smallness'),'uniform_dimensionless_gap'),
 ('U2',('uniform_dimensionless_gap','uniform_energy_scale','scale_identity'),'uniform_gap'),
 ('Y1',('uniform_gap','matched_generator','continuum_axioms','nontrivial_limit','controlled_spectral_limit'),'ym_gap'),
)
def semantic_snapshot():
    return json.dumps({'hypotheses':sorted(HYPOTHESES),'gates':sorted(GATES),'open':sorted(OPEN),'statements':dict(STATEMENTS),'rules':RULES},sort_keys=True,separators=(',',':'))
DECLARED_SEMANTICS=semantic_snapshot()
def check_semantics():
    if semantic_snapshot()!=DECLARED_SEMANTICS:raise ContractError('In-memory proof declarations changed')
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
    check_semantics()
    # Every import occurs in a fresh interpreter over exactly the reviewed byte snapshot.
    # Temporary replays live outside the research tree and cannot enter its package.
    with tempfile.TemporaryDirectory(prefix='ym16-admission-') as name:
        root=Path(name)
        for path,raw in frozen.items():
            p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        result=root/'admission.json'
        proc=subprocess.run([sys.executable,str(root/'replay_evidence.py'),str(result)],cwd=root,capture_output=True,text=True,timeout=180)
        if proc.returncode:raise ContractError('Independent replay failed: '+proc.stderr[-1200:])
        accepted=json.loads(result.read_bytes())
        if accepted.get('status')!='passed' or set(accepted.get('gates',[]))!=GATES:raise ContractError('Required arithmetic gate absent')
    check_semantics()
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
    lib={'nodes':[{'id':n,'statement':STATEMENTS[n],'scope':'round16-declared-contract','kind':'declared_hypothesis' if n in HYPOTHESES else 'target' if n in OPEN else 'theorem','assumption_ids':sorted(deps[n]-{n}),'verification':'Reviewed conventional proof and independently replayed arithmetic; no formal-kernel claim.','source':'Frozen round16 derivations and independent evidence','version':'16.1'} for n in sorted(atoms)],
      'rules':[{'id':i,'premises':list(p),'conclusion':c,'cost':1,'scope':'round16-declared-contract','proof_ref':'Reviewed rule '+i,'review_status':'reviewed'} for i,p,c in selected],
      'initial_facts':sorted(((HYPOTHESES|GATES)-set(removed))&atoms),'goals':[goal],'conditional_assumptions':[],'blocked_goals':[]}
    check_semantics()
    return lib,accepted

def ordered_replay(lib,steps):
    known=set(lib['initial_facts']);rules={r['id']:r for r in lib['rules']}
    for step in steps:
        if step not in rules or not set(rules[step]['premises'])<=known:raise ContractError('Invalid ordered certificate')
        known.add(rules[step]['conclusion'])
    if not set(lib['goals'])<=known:raise ContractError('Incomplete certificate')
    return {'passed':True,'steps':len(steps),'cost':len(steps)}
def execute(output):
    frozen=snapshot();spec=importlib.util.spec_from_file_location('ym16_frozen_core',HERE/'proof_search.py');core=importlib.util.module_from_spec(spec);sys.modules[spec.name]=core
    exec(compile(frozen['proof_search.py'],str(HERE/'proof_search.py'),'exec'),core.__dict__)
    cases=[('finite_shared_effect','shared_effect',(),'proved'),('shared_haar_reduction','disk_fusion',(),'proved'),('physical_scale_counterexample','scale_counterexample',(),'proved')]
    for name,goal,gate in [('missing_graph','shared_effect','graph_gate'),('missing_projector','shared_effect','haar_gate'),('missing_coefficients','shared_effect','coefficient_gate'),('missing_total_tail','shared_effect','remainder_gate'),('missing_difference','shared_effect','difference_gate'),('missing_scale_audit','scale_counterexample','scale_gate')]:cases.append((name,goal,(gate,),'not_derivable'))
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
