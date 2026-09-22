"""Bind the completed human-readable model-agent audit; not an automated theorem prover.
Run only after the reviewer has approved the current manuscript text.
"""
from pathlib import Path
import json,hashlib,re,collections
B=Path(__file__).resolve().parents[1]
R=B.parent/'yang_mills_workbench'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((B/n).read_text())
E=read('audit/early-ledger.json');M=read('audit/middle-ledger.json');N=read('audit/recent-ledger.json');H=read('audit/history-ledger.json')
notes={
'early01':'Matched subtraction, field quotient, energy identity and continuous-drive finite ODE continuation checked. Fixed-regulator simulation and refinement endpoints NOT_REEXECUTED.',
'early02':'Complete divided-current tangent and admissible stationary pure-state quadratic form checked; transformed energy does not bound the raw secular tangent. Exact sign controls executed.',
'early03':'Primitive, continuous-window maximum versus discrete quadrature, explicit electromagnetic-coupling hypothesis and cofinal harmonic divergence checked. Bounded addition keeps fixed/bounded potential. Exact rational constant executed.',
'early04':'Bianchi constraint derivative -theta*C-kappa*Q and shear signs checked symbolically; regulated current/stress are bare quantities. No common covariant renormalized closure inferred.',
'early05':'Scalar exchange and work cancellation checked with the scalar equation retained. New scalar matter and separate classical gravity remain different models.',
'early06':'Nonzero finite nonnegative-energy spectral measure and strong-resolvent/dense-observable quantifiers checked. Counterexamples distinguish a finite gap or apparent plateau from a limiting physical gap.',
'early07':'All-insertion Haar converse and atomic falsifier checked; finite stochastic Wilson results NOT_REEXECUTED. Failed beta=2.2 autocorrelation remains a failure.',
'early08':'Character/Bessel dimension normalization, Casimir clock, negative-beta positivity counterexample and strong fixed-spin rotor limit checked. No interacting transfer identification.',
'early09':'Rank-one positive Markov counterexample and common-vacuum contraction/telescoping hypotheses checked. Product-L1 does not control operator norm.',
'early10':'One-square Jacobi/domain/tail/continuous-coupling proof checked. A new independent rational Sturm/full-tail certificate covers the entire historical interval. Optimized alpha-limit bound retains its support-width premise.',
'early11':'Three-trace quotient, Haar normalization, induced mixed kinetic derivatives, shell spectrum and minimum shell tail checked. Independent rational quaternion and spin-label controls executed.',
'early12':'Min-max signs, true Haar metric, nonnegative-potential tail and k=0,1 restriction checked. Full heat-comparison bound is finite-graph and deteriorating. Historical two-square numerical production NOT_REEXECUTED.',
'early13':'Free physical girth gap, tensor counterbenchmark, extensive certificate, ground/Gibbs distinction and physical-limit obligations checked. Conditional curvature criteria remain conditional.',
'early14':'Shell bandwidth, full-state factorial error, midpoint/commutator remainder and unnormalized numerical composition checked. Exact retained arithmetic is separate from full-space error and from unbounded-observable control.',
'early15':'Haar recurrence, nonzero variance and tested point-closure residual checked exactly. Version-specific external displayed-formula objections are not a universal objection to all closures; full external paper NOT_REVERIFIED.',
'early16':'Finite rule planner and admission-history claims checked as workflow records, not a proof kernel. Full historical software execution and unavailable R8 symbolic replay NOT_REVERIFIED.',
'early17':'Surviving context and variance/separability/regularity controls checked. Missing independent R1/R2 packages and imported prescribed-background outputs remain NOT_REVERIFIED as original full derivations.'}
groups={
'moments':'Moment positivity/uniqueness, static response, normalization and signed interval-tail logic checked. Positive-kappa residual domain is explicit. Historical high-order interval tables and optimization runs NOT_REEXECUTED; exact low-order falsifiers independently tested.',
'gluing':'Actual closed-surface dimension factors, separate insertion derivatives, shared-face fusion and center parity checked. Eleven-face baseline is not zero after deleting only its action coefficient. Historical degree24 numerical enclosures NOT_REEXECUTED.',
'conditional':'Complete adjoint channels and negative off-diagonal Gram entries, full action/observable Gram including singular cases, common-middle dependencies and surrounding normalization checked. New quaternion integration verifies low Taylor coefficients; high-order original tables NOT_REEXECUTED.',
'finite-gap':'Full-space E1 lower versus E0 upper directions, complete physical complement and signed-box domains checked. Fresh independent census verifies strict rank48 and99/107 threshold counts. Full historic867-entry cross-Gram production NOT_REEXECUTED; its frozen evidence is an explicit premise.',
'strips':'Full-link block factorization, invariant unique ground, clipped-boundary coefficient consistency, infinite closed form sum, zero reference mean, norm-convergent summable perturbation and correct exterior lift checked. Arbitrary-phase claim is local-state convergence only.',
'gns':'Full-algebra cyclicity is used before finite gauge averaging; invariant cyclic-space equality, restricted self-adjoint domain and ground-energy subtraction checked. Positive Wilson variance and upper imaginary-time decay have correct direction and model scope.',
'dynamics':'Interaction-picture strong integral and unitary chain resummation checked; no unbounded Casimir norm expansion. Norm convergence between volumes does not imply point-norm time continuity on all bounded local operators.',
'profile':'Exact geometric profile sums, nonzero perturbation norm versus strong convergence, variance scaling and fixed-spacing ground comparison checked. Certificate boundary is not a measured critical point.',
'windows':'Stationary cancellation, all-vector strong Duhamel, complete factor supports and moving-support incidence checked. The necessity statement applies only to the nonnegative certificate with beta,gamma>=0 and positive constants, not actual correlations.',
'clock':'Conditional positive divergence-form dynamics, actual shared-middle gradient, action range and physical clock nonidentifiability checked. Exact rate matrix and hidden-mobility curvature recomputed; finite slopes do not identify arbitrary mobility or full time curves.',
'tree':'Nonclosable old section and its physical energy defect checked. Genuine tree Haar map, all tree vector fields, reducing projection and representation-block domain argument retained. Old and new observable completions cannot share a fitted clock silently.',
'memory':'Full conditional leakage multiplier and strong second-order coefficient, bounded block Duhamel/Volterra/Schur signs and complement gap checked. All seven path-recoupling weights and nonzero cross channel independently recomputed. Absolute error is not late-time relative accuracy.',
'homogeneous':'Yarotsky hypothesis dictionary and unevaluated constants retained. Actual star variance, skew sign, domain-preserving finite-volume rotation and rooted word count checked. Common and direction-only constants remain distinct; no numerical homogeneous gap follows.',
'inverse':'Scalar/diagonal/source split, positive-residual majorant radius, actual initial interacting inverse and all crossing stars checked. Sandwiched Neumann plus sign and response graph convergence do not imply global operator-domain equality or local full-source cancellation.'}
recent={
's1':'Generated repeated-anchor cubic source algebra and nonzero sign checked independently; full identity extension, graph-domain inverse,3 origin versus12 translated crossings retained. Other regrouped terms could cancel.',
's2':'Strong odd-kernel integration-by-parts identity, graph domain and indexed original weight2 series checked. The residual remains and the form-limit identification is separate from a global norm limit.',
't1':'Full complementary-memory block and both leakage insertions checked; noncommuting heat order is not inferred from form order. Repeated returns are retained, with unshifted all-time decay in its own clock.',
't2':'Separate actual ground centers, projector derivative, ground-ground cancellation and nonzero initial complementary excited remainder checked. Same-author historical provenance and infinite-rank absolute scope retained.',
'u1':'Actual paths, free factors and resonant matrix element checked; a first derivative is not a complete endpoint theorem. Limited gate retained.',
'u2':'Complete connected remainder, stationary state replacement and small-z positive margin checked. It is an existence-of-one-observable endpoint obstruction on the frozen interval, with same-author provenance.',
'v1':'Full rank observable PVM/coherent correlation identity, multiplication-norm obstruction and actual operator domains checked. Finite outcomes do not construct finite Haar evolution or physical quotient norm approximation.',
'v2':'Bounded commutator physical-time error and distinct forward/reverse preparation, timing and sampling conventions checked. Resource numbers are mathematical assumptions, not feasible implemented experiments.',
'w1':'Actual source form moment, decreasing spectral weighting, inverse Jensen lower bound and retained short-filter residual checked. Nonzero filtered residual does not prove a resonant block or universal inverse obstruction.',
'w2':'Fixed-G telescoping, vacuum-column graph convergence and finite-volume strong pinching checked. Excited near-resonances prevent promotion to norm inverse or changed-diagonal iteration.',
'x1':'Two different truncation domains, full complement/ground bounds, polynomial shell bandwidth and actual rank21 matrix checked. Complete strict P21 sector distinguished from unassembled large-cutoff examples and numerical evaluation.',
'x2':'All ground residual channels, Gram normalization and moment sum, Temple/variational directions, late-time own-ground decomposition and scalar numerical allowance checked. Historical full sparse certificate production NOT_REEXECUTED in manuscript.',
'y1':'Complete reference-factor collar conventions and one omitted-word tail checked; forward and reverse regional Hamiltonians differ. Finite spatial region remains infinite-dimensional.',
'y2':'Pure-point strong averaging primitive, fixed-energy-block estimate and ordered scalar transfer checked. Scalar endpoint existence is separated from an evaluated full spectrum and global q=1 dynamics.',
'z1':'Actual retained true-ground-null vector and computable Ritz-ground-null vector distinguished; their denominators and limiting relative defects checked. Correctly centered operators themselves do not diverge.',
'z2':'Entire retained-to-omitted Gram, delayed vacuum loading, separate center defect, normalized preparation and true full denominator checked. Increasing early/decreasing late envelopes give continuous all-time coverage.',
'aa1':'Fresh independent16-cycle census, adjacency polynomial, projector ranks and source moments reproduce the reached spectrum. Cube-shell computation alone does not prove exterior closure; limited historic gate preserved.',
'aa2':'Fresh audit checks all20 touching exterior faces and distinct factor owners. Actual charged-sector spectral exclusion, both averaging columns, finite-q weighted adjacency and original small-z clock are retained. Same-author historic provenance explicit.',
'ab1':'Boundary-complete source pinching, signs and factor2 norm checked. Uniform finite-volume resonant upper bound does not evaluate vanishing or preserve weighted locality.',
'ab2':'Gaussian odd tail, jump derivative, total variation, full retained boundary and graph domain checked. Full-source norm contraction is fixed-source/initial-G and not an all-stage weighted iteration.',
'ac1':'Complete293 generated physical basis and metric,1088 directed entries and all new-column envelope checked. B+P21=0 is initial leakage only; old parent accuracy gate stays limited.',
'ac2':'Actual new-channel loading includes feedback, every new leakage channel has a bound, and early/late proof uses original normalized P21 preparation and true denominator. Exact retained semigroup theorem is separated from numerical evaluator.',
'ad1':'Actual norm2 elementary Wilson observables, full state/averaging transfer and null endpoint checked. The two directions use distinct observable/collar instances and no slow-rate identification is inferred.',
'ad2':'Actual multiplication norms2 and2sqrt2, variances/fourth moments and both spectral measures independently checked. Equality of vacuum vectors does not transfer rank-operator budgets. Full finite-q and limiting scope is0<z<=1e-6.',
'ae1':'All-time unbounded-onsite chain framework, collar distance/incidence, Gaussian tail and separate reverse graph error checked. Diameter decay does not establish the original cardinality-weight norm.',
'ae2':'Compact triangular kernel,12 translated crossings, family contraction2072/2997, original weight2 finiteness and old-cap certificate incompatibility checked. SmallerM region and lack of weighted contraction/induction explicit.',
'af1':'Executed physical point heat has correct minimum-ground identification, actual Gram coordinate disks and independent export agreement. Prior Round26 receipts retained; no new293 production replay claimed.',
'af2':'Continuous all-time piecewise evaluator has separate physical and numerical budgets, late projector identification, join/tail proof and true denominator. Real-rational executable interface, complex demos and broader operator theorem remain distinct.'}
reviews=[]
for x in E['contributions']:
 reviews.append({'id':x['id'],'title':x['title'],'manuscript':x['manuscript'],'equation_labels':x['equation_labels'],'verdict':'accepted_within_declared_scope','review':notes[x['id']],'limitations':x['limitations'],'source_paths':x['source_paths'],'priority':'NOT_REVERIFIED','full_historical_production_reexecution':False})
for x in M['entries']:
 reviews.append({'id':x['ID'],'title':x['audit']['historical_title'],'manuscript':'sections/middle.tex','equation_description':x['equation'],'section_label':x['derivation_location']['section_label'],'historical_status':x['status'],'verdict':'accepted_within_declared_scope','review':groups[x['group']],'limitations':x['limitation'],'source_paths':x['source_paths'],'priority':'NOT_REVERIFIED','full_historical_production_reexecution':False})
# Review every recent contribution, and retain a separate historical-loop index.
entries=N['entries'];recent_loop_reviews=[]
for x in entries:
 k=x['historical_entry_id'].lower()
 if k not in recent:raise ValueError(('unmapped recent record',k))
 recent_loop_reviews.append({'history_id':x['history_id'],'loop':k,'historical_verdict':x['historical_verdict'],'review_mode':x['review_mode'],'contribution_ids':x['contribution_ids'],'verdict':'accepted_as_scoped_historical_record','review':recent[k],'full_historical_production_reexecution':False})
for x in N['contributions']:
 ks=x['historical_loops']
 reviews.append({'id':x['id'],'title':x['title'],'manuscript':'sections/recent.tex','historical_loops':ks,'equation_labels':x['equation_labels'],'mathematical_statement':x['mathematical_statement'],'verdict':'accepted_within_declared_scope','review':' '.join(recent[k] for k in ks),'limitations':x['limitations'],'source_paths':x['source_paths'],'priority':'NOT_REVERIFIED','full_historical_production_reexecution':False,'round26_prior_review':any(k[:2] in ('ab','ac','ad','ae','af') for k in ks)})
if len(reviews)!=114 or len(entries)!=28 or len(N['contributions'])!=35:raise ValueError(('coverage',len(reviews),len(entries)))
# Every displayed labelled equation is indexed, including those not specially starred.
equations=[]
for name in ('early','middle','recent','synthesis'):
 p=B/f'sections/{name}.tex';s=p.read_text()
 for mat in re.finditer(r'\\begin\{(equation\*?|align\*?|gather\*?)\}([\s\S]*?)\\end\{\1\}',s):
  block=mat.group(0)
  for lab in re.findall(r'\\label\{([^}]+)\}',block):
   equations.append({'label':lab,'manuscript':str(p.relative_to(B)),'line':s[:mat.start()].count('\n')+1,'display_sha256':hashlib.sha256(block.encode()).hexdigest(),'verdict':'written_derivation_and_scope_reviewed','starred':r'\workstar' in block,'fresh_execution':'Selected identities independently exercised in the158-check suite; full historic production NOT_REVERIFIED unless separately stated.','priority':'NOT_REVERIFIED'})
for e in equations:
 e['contribution_ids']=[c['id'] for c in reviews if e['label'] in c.get('equation_labels',[]) or e['label'] in c.get('equation_description','')]
 if not e['contribution_ids']:
  if not e['label'].endswith(('memory-synthesis','error-accounting')):raise ValueError(('unmapped equation',e['label']))
  e['classification']='Established conditional block/triangle identities used for synthesis; not a new claimed theorem.'
# All textual star markers have a review location even when not an equation.
markers=[]
for name in ('early','middle','recent'):
 s=(B/f'sections/{name}.tex').read_text()
 for mat in re.finditer(r'\\workstar',s):
  prev=re.findall(r'\\(?:subsection|subsubsection|paragraph)\{([^\n]+)',s[:mat.start()])
  markers.append({'manuscript':f'sections/{name}.tex','line':s[:mat.start()].count('\n')+1,'context':prev[-1][:180] if prev else 'scope/legend','verdict':'scope_and_derivation_reviewed; not priority-certified'})
# Source inventory is provenance validation, not a claim that290 files were all freshly replayed.
for p,h in H['source_sha256'].items():
 if sha(R/p)!=h:raise ValueError(('source hash mismatch',p))
c=collections.Counter(x['kind'] for x in H['entries'])
if c!={'study':35,'physics_loop':86}:raise ValueError(c)
if len(re.findall(r'^R\d+\\par ',(B/'sections/history-appendix.tex').read_text(),re.M))!=121:raise ValueError('history table coverage')
suites=[]
for name,src,normal,count in [('general','skeptic_checks.py','skeptic-output-final-normal',90),('early','skeptic_early_checks.py','skeptic-output-early',12),('middle','skeptic_middle_checks.py','skeptic-output-middle-final',33),('recent','skeptic_recent_checks.py','skeptic-output-recent',23)]:
 a=B/'audit'/normal/'results.json';b=B/'audit'/f'skeptic-output-release-{name}-optimized'/'results.json';d=json.loads(a.read_text())
 if d['count']!=count or a.read_bytes()!=b.read_bytes():raise ValueError(('run mismatch',name))
 if d.get('script_sha256',d.get('own_script_sha256'))!=sha(B/'audit'/src):raise ValueError(('script mismatch',name))
 suites.append({'name':name,'checks':count,'script':f'audit/{src}','script_sha256':sha(B/'audit'/src),'normal_output':str(a.relative_to(B)),'optimized_output':str(b.relative_to(B)),'output_sha256':sha(a),'byte_equal':True})
contribution_sources={p:sha(R/p) for x in reviews for p in x.get('source_paths',[])}
# Final manuscript files known to this review. The PDF has a separate compiled-text receipt.
paths=['main.tex','sections/introduction.tex','sections/early.tex','sections/middle.tex','sections/recent.tex','sections/synthesis.tex','sections/verification.tex','sections/roadmap.tex','sections/history-appendix.tex','sections/reproduction.tex','sections/figures.tex','sources/related-work.tex','sources/references.bib','audit/early-ledger.json','audit/middle-ledger.json','audit/recent-ledger.json','audit/history-ledger.json','audit/prior-round26-release-receipt.json','audit/calculator-review.json','audit/web-calculator-tests.json']
if (B/'sections/contribution-appendix.tex').exists():paths.append('sections/contribution-appendix.tex')
if (B/'audit/contribution-catalog.json').exists():paths.append('audit/contribution-catalog.json')
# Check the scientific issue resolutions as text conditions; these are guards, not substitutes for reading.
m=(B/'sections/middle.tex').read_text();n=(B/'sections/recent.tex').read_text()
if r'\gamma\ge0' not in m:raise ValueError('N2 nonnegative time exponent missing')
if not ('0<z' in n and '10^{-6}' in n):raise ValueError('endpoint scope missing')
data={'schema':'ym-manuscript-skeptic-v1','verdict':'accepted_within_declared_scope_for_author_review','blocking_issues':[],'source_commit':H['source_commit'],'source_tree':'169b2db4e8017f5c4e783ba5f42e4f96522ad2b1','counts':{'historical_entries':121,'historical_studies':35,'historical_explicit_loops':86,'historical_recorded_rounds':24,'reviewed_contribution_entries':114,'early_groups':17,'middle_entry_reviews':62,'recent_contribution_groups':35,'recent_loop_reviews':28,'displayed_labelled_equations':len(equations),'textual_star_occurrences':len(markers),'fresh_exact_stress_checks':158,'new_research_loops':0},'review_authorship':'Independent skeptic model-agent review; not external peer review or formal proof. Writers and skeptic share inherited sources.','audit_depth':'Every manuscript contribution and displayed labelled equation reviewed for written derivation and model/domain scope. Targeted new exact computations supplement this reading; original numerical production is not comprehensively replayed. Underlying proof assistants, all source-code paths and full external papers are NOT_REVERIFIED.','unverified':['Scientific priority for every contribution','Missing independently identifiable Round1/2 packages','Unavailable Round8 symbolic replay','Comprehensive historical simulations, high-degree numeric tables and software mutation suites','All-stage homogeneous nonlinear iteration or a numerical homogeneous gap','Continuum Yang-Mills construction/mass gap, experimental feasibility and cross-model clock calibration'],'checks':suites,'contributions':reviews,'recent_historical_loop_reviews':recent_loop_reviews,'equations':equations,'star_index':markers,'historical_entry_index':[{'id':x['record_id'],'historical_verdict':x['historical_verdict'],'manuscript_admission':'accepted_as_scoped_historical_record','production_replay':'NOT_REEXECUTED_BY_MANUSCRIPT_SKEPTIC'} for x in H['entries']],'historical_sources_sha256':H['source_sha256'],'contribution_sources_sha256':contribution_sources,'manuscript_sha256':{p:sha(B/p) for p in paths},'prior_round26_receipt':'audit/prior-round26-release-receipt.json (same pinned tree; separate prior evidence, not fresh158-check suite)','compiled_text_review':'Final 92-page extracted PDF text checked for repaired mathematical scopes, contribution/history coverage and reference resolution. The exact PDF and extracted-text hashes are bound separately in audit/skeptic-compiled-review.json; visual layout QA belongs to the integrator. This is a final representation check, not a repeat of the 158 mathematical stress checks.','notes':['The17+62+35 catalog groups31 early history records into17 contributions and splits28 recent loops into35 contribution groups. It does not invent121 separate discoveries.','Historical limited verdicts are preserved; accepting their accurate manuscript presentation does not upgrade the parent goals.','All290 history-ledger bindings were checked by SHA256; this is provenance verification, not290 fresh mathematical proofs.','Superseded intermediate test outputs are excluded from the158 total and the final bundle.']}
(B/'audit/skeptic-review.json').write_text(json.dumps(data,indent=2)+'\n')
p=B/'audit/skeptic-review.md';s=p.read_text().replace('# Independent manuscript audit — provisional pending final ledger binding','# Independent manuscript audit — accepted within declared scope').replace('The mathematical draft is suitable for author review within its stated models, subject to the final source/ledger binding below.','The mathematical draft is suitable for author review within its stated models. The final source/ledger binding is in `skeptic-review.json`; no mathematical blocking issue remains in that reviewed version.')
s=re.sub(r'\nFinal index:[^\n]*\n?', '\n',s)
s+='\nFinal index: **114 contribution entries** (17 early groups, 62 middle entries, 35 recent groups from 28 loops), **'+str(len(equations))+' displayed labelled equations**, and **'+str(len(markers))+' textual star markers** are indexed. Every priority claim remains NOT_REVERIFIED. The 158-check total is independent of these index counts.\n'
p.write_text(s)
print(json.dumps({'verdict':data['verdict'],'contributions':len(reviews),'equations':len(equations),'markers':len(markers),'checks':158}))
