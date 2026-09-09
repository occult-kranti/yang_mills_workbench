#!/usr/bin/env python3
"""Assemble the bounded reviewer handoff after independent audit execution.

Reads the declared round-12 directory and writes only beside this script.
It does not execute production studies, change sources, or publish anything.
"""
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction as F
from math import factorial
import argparse, hashlib, json

HERE=Path(__file__).resolve().parent
REQUIRED=['advisor/advisor.md','solver/drive_bound.py','solver/exact_stepper.py',
          'solver/run_study.py','solver/test_solver.py','volume/volume_checks.py',
          'volume/volume-bridge.md','closure/closure_audit.py','closure/closure-audit.md','proof_routes.py']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((HERE/name).read_text())
def require(ok,message):
    if not ok:raise RuntimeError(message)
def write(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2,allow_nan=False)+'\n')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('round12',type=Path);args=parser.parse_args();root=args.round12.resolve()
    now=datetime.now(timezone.utc).isoformat();hashes={name:sha(root/name) for name in REQUIRED}
    inherited=[('banded_results.json',35,'independent_banded.py',None),
               ('closure_results.json',76,'independent_closure.py',None),
               ('final_drive_normal_results.json',210,'audit_drive_bound.py','solver/drive_bound.py'),
               ('final_drive_optimized_results.json',210,'audit_drive_bound.py','solver/drive_bound.py'),
               ('final_numerical_normal_results.json',23,'audit_numerics.py','solver/run_study.py'),
               ('final_numerical_optimized_results.json',23,'audit_numerics.py','solver/run_study.py')]
    for name,count,audit,source in inherited:
        d=read(name);require(d['status']=='passed' and d['gate_count']==count,'Inherited result mismatch: '+name)
        rows=d.get('records',d.get('gates'));require(len(rows)==count and all(x['passed'] is True for x in rows),'Incomplete inherited gates: '+name)
        require(d.get('audit_sha256',d['source_sha256'])==sha(HERE/audit),'Inherited independent audit bytes changed: '+name)
        if source:require(d['source_sha256']==hashes[source],'Inherited production source changed: '+source)
    for label in ['normal','optimized']:
        for kind,count,source in [('exact',28,'solver/exact_stepper.py'),('proof',34,'proof_routes.py')]:
            name='verifier_'+kind+'_'+label+'_results.json';d=read(name)
            require(d['status']=='passed' and d['gate_count']==count and len(d['records'])==count,'Final audit incomplete: '+name)
            require(d['optimized_python']==(label=='optimized'),'Interpreter mode mismatch: '+name)
            require(all(x['passed'] is True for x in d['records']) and not d.get('defects'),'Final audit defect: '+name)
            require(d['source_sha256']==hashes[source],'Final source changed: '+source)
            require(d['audit_sha256']==sha(HERE/('audit_exact_stepper.py' if kind=='exact' else 'audit_proof_routes.py')),'Final audit script changed: '+name)
            bindings=d['source_hashes'] if kind=='exact' else d['reviewed_source_hashes']
            for rel,digest in bindings.items():
                p=root/'solver'/rel if kind=='exact' else root/rel
                require(sha(p)==digest,'Final replay binding changed: '+str(p))
    require(read('volume_final_hash.json')['source_sha256']==hashes['volume/volume_checks.py'],'Volume handoff source changed')
    handoff=read('handoff_provenance.json')
    for item in handoff['records']:require(sha(HERE/item['file'])==item['sha256'],'Preserved historical artifact changed: '+item['file'])
    manifest=json.loads((root/'proof_manifest.json').read_text())['sha256']
    require(all(sha(root/rel)==digest for rel,digest in manifest.items()),'Current proof manifest is stale')
    for rel in ['solver/output/edge_tests.json','solver/output/edge_tests_optimized.json']:
        output=json.loads((root/rel).read_text())
        require(output['status']=='passed','Production edge report is not passed: '+rel)
        require(all(sha(root/'solver'/name)==digest for name,digest in output['source_hashes'].items()),'Production edge report is stale: '+rel)
    c=json.loads((root/'solver/output/exact_step_certificate.json').read_text());eps=F(114,5)**101/factorial(101);total=F(27,80000)+2*eps+eps*eps
    require(F(c['total_state_error_upper'])==total and total<F(337501,10**9),'Independent total bound mismatch')
    require(c['protocol']=={'kind':'piecewise_constant','segments':[{'duration':'1','lambda1':'1/20','lambda2':'1/10'},{'duration':'1','lambda1':'1/10','lambda2':'1/20'}]},'Exact physical fixture changed')
    descriptions={
      'advisor/advisor.md':'Reviewed the degree-shell Duhamel derivation, same-phase physical norm, exact polynomial remainder/composition, and separation of missing volume/continuum premises; prior skeptical mathematical review is retained.',
      'solver/drive_bound.py':'Current source matches the inherited 210-gate independent normal and optimized action/certificate audits.',
      'solver/exact_stepper.py':'Post-fix independent normal and optimized 28-gate replay; backwards rational Horner and independently constructed Gram/form matrices reproduce the unrenormalized state.',
      'solver/run_study.py':'Current source matches inherited independent 23-gate normal and optimized diagnostic/input-comparison audits.',
      'solver/test_solver.py':'Read the current explicit-exception acceptance guards, physical input/phase/time comparisons, and exact-state metadata mutations. Production tests are not added to independent gate totals.',
      'volume/volume_checks.py':'Current source matches the prior final volume hash. Read explicit require guards and source/output status handling; retained prior optimization-disabled assertion failure and corrected source snapshot.',
      'volume/volume-bridge.md':'Reviewed finite graph/ground-state/tensor arguments and stated conditional continuum requirements. External literature review remains attributed to the prior researchers.',
      'closure/closure_audit.py':'Reviewed direct Gaussian-rational trace fixtures, finite tilted-Haar diagnostic scope, and explicit runtime guards; current normal and optimized production source records match.',
      'closure/closure-audit.md':'Reviewed variance comparison, zero-coupling edge case, point-concentration-only rejection and source-formula scope against the inherited independent 76-gate record.',
      'proof_routes.py':'Post-fix normal and optimized 34-gate frozen-byte/source/semantic mutation audits. Source review confirms all eight named cases fix kind, duration, both magnetic scales, final time, alpha, rho, initial degree, degree set and unique labels.'}
    source_review={'status':'passed','reviewed_utc':now,'count':len(REQUIRED),'reviewed_source_hashes':hashes,
      'records':[{'source':name,'sha256':hashes[name],
                  'source_modified_utc':datetime.fromtimestamp((root/name).stat().st_mtime,timezone.utc).isoformat(),
                  'review_method':descriptions[name]} for name in REQUIRED],
      'scope':'Current source inspection and byte binding; independent executed counts remain in the six separate reports.',
      'all_current_proof_manifest_bindings_match':True,'handoff_files_preserved_unchanged':True}
    write('source_review.json',source_review)
    reports=[
      {'name':'Independent banded theorem stress cases','status':'passed','count':35,'scope':'Prior reviewer: exact finite banded models and broken hypotheses; the general theorem additionally requires its analytic proof.','artifact':'banded_results.json'},
      {'name':'Independent compact identities and closure','status':'passed','count':76,'scope':'Prior reviewer: exact matrix jets and rigorous tilted-Haar moment intervals for the specified finite closure.','artifact':'closure_results.json'},
      {'name':'Independent action and certificate inputs','status':'passed','count':210,'scope':'Prior reviewer: independent action enclosures, factorial arithmetic, metadata and dependency mutations; repeated in normal and optimized Python.','artifact':'final_drive_normal_results.json'},
      {'name':'Independent numerical diagnostics','status':'passed','count':23,'scope':'Prior reviewer: finite floating diagnostic comparison, refinement, phase/time/grid checks; no certified floating cosine error.','artifact':'final_numerical_normal_results.json'},
      {'name':'Independent exact computed state','status':'passed','count':28,'scope':'Final verifier: post-fix exact backwards Horner, physical Gram algebra, total error and invalid-input/mutation checks in normal and optimized Python.','artifact':'verifier_exact_normal_results.json'},
      {'name':'Independent frozen proof-wrapper admission','status':'passed','count':34,'scope':'Final verifier: current frozen source replay, fixture semantics, provenance, negative routes and target-seeding rejection in normal and optimized Python.','artifact':'verifier_proof_normal_results.json'}]
    acceptance={'status':'passed','completed_utc':now,'contract':'ym12-bounded-independent-review-v1',
      'scope':'Seven-link finite graph; exact fixed nonnegative two-segment state plus separately bounded representation, finite-volume and defined-closure claims. No four-dimensional Yang-Mills or floating cosine total-error claim.',
      'reviewed_source_hashes':hashes,'reports':reports,'independent_gate_count':sum(x['count'] for x in reports),
      'counting_policy':'Each distinct gate is counted once; normal/optimized repetitions and earlier pre-fix runs are not added.',
      'provenance':{'inherited':'banded, closure, drive and numerical audits executed by the previous independent reviewer; artifacts copied unchanged from ym12-skeptic.',
                    'new':'Post-fix exact-stepper and proof-wrapper audits executed by the final verifier; current source inspection and all final byte bindings checked.',
                    'record':'handoff_provenance.json','current_source_review':'source_review.json'},
      'mode_replays':{'drive':['final_drive_normal_results.json','final_drive_optimized_results.json'],
                      'numerical':['final_numerical_normal_results.json','final_numerical_optimized_results.json'],
                      'exact':['verifier_exact_normal_results.json','verifier_exact_optimized_results.json'],
                      'proof':['verifier_proof_normal_results.json','verifier_proof_optimized_results.json']},
      'preserved_prior_findings':['initial_drive_audit_results.json','initial_exact_step_audit_results.json','initial_proof_mutations.json','initial_time_grid_failure.json','volume_initial_hashes.json'],
      'exact_result':{'degree':3,'alpha':'1','rho':'1','initial_state':'constant normalized product-Haar state','segments':c['protocol']['segments'],
                      'polynomial_order_per_segment':100,'representation_error_upper':'27/80000','step_remainder_formula':'e=(114/5)^101/101!',
                      'total_error_formula':'27/80000+2e+e^2','strict_decimal_upper':'0.000337501','total_state_error_upper':str(total),
                      'computed_vector_was_renormalized':False},
      'limitations':['Conventional mathematical review and exact arithmetic execution; no proof-assistant formalization.',
                     'Floating cosine trajectories remain numerical diagnostics without certified total error.',
                     'Disconnected tensor examples do not prove a gap on growing connected lattices.',
                     'The defined finite point-concentration closure is rejected; general scalar ansatze are not all ruled out.',
                     'Construction, reconstruction, nontriviality and a four-dimensional physical mass gap remain unresolved.']}
    write('acceptance.json',acceptance)
    (HERE/'REVIEW.md').write_text('''# Round 12 independent review

The bounded review passes for the current source hashes in `acceptance.json`. The exact fixed two-segment computation has an independently replayed total Hilbert-state error below **0.000337501**. This is a finite seven-link graph result.

The physical fixture has alpha=rho=1, degree D=3 and the normalized constant Haar initial state. It applies (lambda1,lambda2)=(1/20,1/10) for one time unit, then (1/10,1/20) for one time unit. Each segment uses the exact order-100 Taylor polynomial. The stored complex coefficients are rational pairs and remain unrenormalized. With e=(114/5)^101/101!, the full error bound is exactly

    27/80000 + 2e + e^2 < 0.000337501.

The representation part is 27/80000, from action A=3/10. The product-of-approximate-steps contribution is 2e+e^2. Both the state and its Haar norm were reconstructed using independent spherical moments, a divergence-form kinetic matrix, an independently inverted Gram matrix, and backward Horner polynomial evaluation. The production solver uses forward term accumulation. Substituting the form matrix for its Gram-correct coordinate operator was independently falsified.

## Executed evidence and attribution

| Audit | Distinct gates | Execution provenance |
|---|---:|---|
| Banded finite models and broken hypotheses | 35 | Previous independent reviewer; retained optimized record |
| Compact identities and defined scalar closure | 76 | Previous independent reviewer; retained optimized record |
| Exact action and certificate input paths | 210 | Previous independent reviewer; normal and optimized records |
| Numerical diagnostic/input comparisons | 23 | Previous independent reviewer; normal and optimized records |
| Exact stored polynomial state | 28 | Final verifier; post-fix normal and optimized runs |
| Frozen proof-wrapper admission | 34 | Final verifier; current normal and optimized runs |

There are **406 distinct recorded gates**. Repeating an audit under optimized Python does not increase this number. The previous reviewer performed the first four audits; the final verifier reviewed their scripts/records and checked their source bindings rather than claiming those executions as new work. `handoff_provenance.json` preserves original hashes and modification timestamps. `source_review.json` records the ten current reviewed files, their hashes, timestamps and review methods.

The final proof-wrapper runs reconstruct arithmetic from checked immutable bytes. Their mutations reject stale/self source, missing inputs, same-byte symlinks, altered dependency roles, wrong stored vectors, normalization metadata changes, changed error claims and a valid certificate attached to the wrong named protocol. Source inspection also checks all eight declared analytic fixtures: protocol kind/duration/both magnetic scales, evaluation time, alpha, rho, initial degree, unique case labels and the degree-3/4 pair set. A frozen-byte replay remains successful after isolated on-disk source corruption, which tests the actual execution path. No production source was mutated by this reviewer.

The positive routes have costs 6 (cosine representation), 12 (fixed exact computed state), 3 (finite-volume comparison), 2 (decaying bound does not imply gap closure), and 3 (defined point-closure rejection). Missing bandwidth, support, absolute action and exact-vector replay block their dependent conclusions. Floating-cosine total error and the four-dimensional target remain not derivable; seeding the unproved final target is rejected.

## Preserved findings and corrections

The initial dependency-manifest symlink acceptance is retained in `initial_drive_audit_results.json`; the corrected source passes 210 independent gates in both Python modes. Initial proof-manifest symlink acceptance is retained in `initial_proof_mutations.json`; the current wrapper rejects that mutation.

The initial volume implementation used assertions that disappeared under optimized Python. `volume_initial_hashes.json` preserves an incorrect-count mutation reported as passed under optimization, together with the historical source and mutant scripts. The final source uses explicit exception guards and matches `volume_final_hash.json`; its production result binds to that corrected source. No additional full volume sweep is claimed by the final verifier.

`initial_exact_step_audit_results.json` preserves the earlier 27-gate exact replay and public API defect: passing a floating state to `norm_squared` returned a float. The certificate constructor itself was unaffected. The corrected helper converts Gram entries and state components with the rational-input parser, validates complex-pair shape, and now returns the exact expected 1/100 for the regression input. Both post-fix independent runs pass 28 gates without defects.

`initial_time_grid_failure.json` retains the caught mismatched-grid diagnostic rather than hiding an unsuccessful comparison. The final numerical audit checks matching times, phases, protocol and shapes and rejects nonfinite transient entries. The previous proof normal report is also retained unchanged; fresh verifier labels bind the new exact-stepper source and certificate.

During source inspection, the final verifier notified the integrator that one production optimized edge-test report still referenced the old exact-stepper source. The integrator regenerated it, and final assembly checked both production edge reports against the current source bytes. Those production checks are not added to independent gate counts. This review's acceptance covers the named independent artifacts and reviewed sources, not deployment or archive contents.

## Mathematical scope

The advisor's bandwidth-one, one-sided Duhamel argument compares full and exact Galerkin evolution in the physical Haar norm with matched phases and initial state. The exact polynomial calculation adds a separately bounded finite-step error. It supplies neither an operator norm for the unbounded full kinetic energy nor a retrospective temporal certificate for floating cosine histories.

The finite-volume comparison retains its explicit link/plaquette dependence. The disconnected tensor counterbenchmark shows that decay of this lower bound does not imply decay of the true gap. It is not a theorem for growing connected lattices. The actual quantum ground-state density is distinct from the tilted Euclidean Gibbs measure; the conditional local curvature, limiting-semigroup, vacuum and observable-density premises remain unproved where stated.

The closure audit rejects the explicitly defined point-concentration replacement on a finite tilted-Haar measure using positive variance and the next identity at zero coupling. The inherited source-formula review has a stated version and convention boundary. The final verifier reviewed its local artifacts and did not conduct a new external literature audit. This does not rule out every scalar ansatz.

These are conventional mathematical reviews with exact arithmetic checks, not proof-assistant formalizations. Continuum construction, reconstruction, nontriviality and a positive four-dimensional Yang-Mills physical mass gap remain unresolved.
''')
    (HERE/'README.md').write_text('''# Independent reviewer artifacts

`acceptance.json` is the bounded verdict and lists the ten current reviewed source hashes plus six independent reports. `REVIEW.md` explains the result, provenance, corrections and limits. `source_review.json` records source timestamps and review methods. `handoff_provenance.json` identifies files copied unchanged from the earlier reviewer.

The exact finite-graph result uses two duration-one nonnegative segments, (1/20,1/10) then (1/10,1/20), alpha=rho=1, D=3, the constant initial state and exact order-100 polynomials. Its unrenormalized stored vector has total error 27/80000+2e+e^2 < 0.000337501, where e=(114/5)^101/101!.

The previous reviewer supplied `banded_results.json` (35), `closure_results.json` (76), `final_drive_*_results.json` (210) and `final_numerical_*_results.json` (23). The final verifier supplied `verifier_exact_*_results.json` (28) and `verifier_proof_*_results.json` (34). Counts are per distinct gate, not per interpreter run. The older `final_proof_normal_results.json` is preserved handoff evidence and is superseded by fresh verifier proof records for final source binding.

From an extracted round-12 directory with this folder named `skeptic`, reproduce the final independent checks with:

```bash
python -B skeptic/audit_exact_stepper.py solver/exact_stepper.py --label verifier_exact_normal
python -B -O skeptic/audit_exact_stepper.py solver/exact_stepper.py --label verifier_exact_optimized
python -B skeptic/audit_proof_routes.py . --label verifier_proof_normal
python -B -O skeptic/audit_proof_routes.py . --label verifier_proof_optimized
python -B skeptic/finalize_review.py .
```

The exact-state and proof-wrapper auditors use Python standard-library arithmetic and copied independent algebra helpers. The wrapper creates isolated probe directories beside its audit script, copies the declared manifest inputs, and restores its mutation fixtures. It never mutates the supplied round-12 sources. Earlier numerical audits additionally require NumPy/SciPy; volume plotting requires Matplotlib. `-B` avoids writing bytecode into reviewed source directories.

Historical findings remain in the `initial_*` JSON files and volume historical sources/mutants. The integrator also retains earlier failure probe folders in the portable package. Do not replace historical files with passing outputs: use fresh labels when changing an audit or source. Source hashes show identity, not mathematical truth.

Acceptance covers the declared finite claims and exact computation. It does not certify floating cosine total error, all scalar reductions, a growing connected-lattice gap, a four-dimensional continuum result, UI behavior or published package contents.
''')
    require({name:sha(root/name) for name in REQUIRED}==hashes,'Reviewed source changed during final assembly')
    print(json.dumps({'status':'passed','independent_gate_count':acceptance['independent_gate_count'],'reports':len(reports),'reviewed_sources':len(hashes),'output':str(HERE)}))
if __name__=='__main__':main()
