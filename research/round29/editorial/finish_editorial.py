#!/usr/bin/env python3
from pathlib import Path
import json,re,shutil
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'papers/draft-02'
r=json.loads((OUT/'registry/hnm-registry.json').read_text())
# Separate genuine equation labels from inherited section labels.
sections=r.get('section_aliases',[]);equations=[]
for e in r['equations']:
 source=(OUT/e['source']).read_text();pos=source.index('\\label{'+e['legacy_label']+'}');stack=[]
 for m in re.finditer(r'\\(begin|end)\{([^}]+)\}',source[:pos]):
  if m[1]=='begin':stack.append(m[2])
  elif m[2] in stack:stack=stack[:len(stack)-1-stack[::-1].index(m[2])]
 if any(x in ['equation','align','gather','multline','alignat','flalign'] for x in stack):
  e['label_kind']='equation';equations.append(e)
 else:
  e['id']=e['id'].replace('HNM-E-','HNM-S-');e['label_kind']='section';sections.append(e)
r['equations']=equations;r['section_aliases']=sections
for x in r['contributions']:
 source_rounds=sorted({int(n) for p in x['source_paths'] for n in re.findall(r'round(\d+)',p)})
 x['source_rounds']=source_rounds
 if x['round']=='3–26' and source_rounds:x['round']=min(source_rounds)
# All genuine numbered-equation labels are in scope, irrespective of spelling.
seen={e['legacy_label'] for e in r['equations']}
for p in sorted((OUT/'sections').glob('*.tex'))+sorted((OUT/'addenda').rglob('*.tex')):
 source=p.read_text()
 for match in re.finditer(r'\\label\{([^}]+)\}',source):
  label=match[1]
  if label in seen:continue
  stack=[]
  for env in re.finditer(r'\\(begin|end)\{([^}]+)\}',source[:match.start()]):
   if env[1]=='begin':stack.append(env[2])
   elif env[2] in stack:stack=stack[:len(stack)-1-stack[::-1].index(env[2])]
  if not any(z in ['equation','align','gather','multline','alignat','flalign'] for z in stack):continue
  r['equations'].append(dict(id='HNM-E-'+re.sub('[^A-Za-z0-9]+','-',label).upper().strip('-'),legacy_label=label,label_kind='equation',source=str(p.relative_to(OUT)),contribution_ids=[],scope='Stable source equation locator; all mathematical premises and external attributions remain in the cited derivation.'))
  seen.add(label)
for e in r['equations']:
 lab=e['legacy_label'];ids=set(e.get('contribution_ids',[]))
 if lab.startswith('r28:ag2:'):ids.add('HNM-C-AG2')
 if lab.startswith('r29:calculator:'):ids.add('HNM-C-AM2')
 if lab.startswith('r27:eq:'):
  stem=lab[7:]
  if e['source'].endswith('/ag1.tex'):ids.add('HNM-C-R27-AG1')
  if e['source'].endswith('/ai2.tex'):
   if stem in ['probes','collars','tail']:ids.add('HNM-C-R27-AI2-SUPPORT')
   if stem in ['center','disk','hypotheses','time2','margin','ratioerror','ratio']:ids.add('HNM-C-R27-AI2-DISKS')
  if e['source'].endswith('/body.tex'):
   if stem in ['clock','endpoints','surrogate','fiber','monotone','slope']:ids.add('HNM-C-R27-AI1-FIBERS')
   if stem in ['clock','carrier','alias']:ids.add('HNM-C-R27-AI1-CARRIER')
 e['contribution_ids']=sorted(ids)
 if not ids:e['join_note']='Cross-model synthesis or general bookkeeping; not assigned to a distinct claimed contribution.'
for x in r['contributions']:
 x['equation_labels']=sorted(set(x.get('equation_labels',[]))|{e['legacy_label'] for e in r['equations'] if x['id'] in e['contribution_ids']})
# Taxonomy is result type, never acceptance or proof-completion status.
recent_negative={5,17,20,25,27,34}
recent_computation={14,15,16,18,19,21,22,23,28,29,31,33}
for x in r['contributions']:
 x['source_status']=x.get('source_status',x['status'])
 if x['legacy_id'].startswith('recent'):
  n=int(x['legacy_id'][6:])
  x['classification']='scoped obstruction or negative control' if n in recent_negative else 'scoped computation or certificate' if n in recent_computation else 'scoped derivation'
  x['classification_source']='Editorial content-based classification; inherited mixed-type status was not used as a keyword classifier.'
 x['proof_status']=x['status'] if isinstance(x['round'],int) and x['round']>=27 else 'Scoped historical result; read the stated assumptions and unresolved obligations.'
priority=['recent25','AM2','AQ2','AK2','AO2','early10','AH2','recent35','AI4','AJ1','AG2','AG3','R27-AI1-FIBERS','AK1','R27-AI2-DISKS']
reasons={
'AQ2':'The numerical finite-volume certificate reaches the complete physical sector of a locally normal fixed-lattice GNS representation, with a nonzero original Wilson witness. This is a model-specific application of an established transfer strategy, without uniqueness of all thermodynamic states.',
'AO2':'The actual inherited Wilson vector gains an operator-domain statement and exact first-energy identity, closing a documented AK2 loss-of-moment limitation while retaining both original smallness conditions.',
'AM2':'A complete alternative creation proof supplies an explicit finite-volume coupling cap for the actual untruncated model, including excitation exclusion and removal of representation cutoffs. It does not identify an infinite-volume state.',
'recent25':'A full-model counterexample marks the critical growing-time boundary; useful for rejecting an unjustified interchange of limits.',
'AK2':'A real physical fluctuation has controlled spectral weight and imaginary-time correlation, conditionally within the declared fixed-spacing state. The general mechanism has prior overlap.',
'early10':'Full representation-space spectral enclosure distinguishes a certified infinite tail from a finite matrix diagonalization.',
'AH2':'A complete 561-state finite-graph enrichment improves the all-time omitted-channel heat certificate on a fixed preparation class.',
'recent35':'Actual Wilson multiplier endpoints expose nontrivial readout structure under a proved but very small scaled-time window.',
'AI4':'Candidate-pair separation survives all declared physical errors over a continuous profile range, with divergent clock cost and vanishing error allowance.',
'AJ1':'Local normality and reducing physical dynamics make the subsequent Wilson statements meaningful in the actual representation.',
'AG2':'Restoring the full original remainder closes a previously omitted source inventory before claiming correction quality.',
'AG3':'One complete-source update quantifies support-weight loss and shows why a sufficient bound is weaker than an iteration theorem.',
'R27-AI1-FIBERS':'Exact readout fibers prevent false parameter identification from universal endpoint data.',
'AK1':'The conditional quantitative variance floor prevents a vacuous observable claim while exposing the unevaluated stability radius.',
'R27-AI2-DISKS':'A sharply scoped successful scalar discrimination test retains the physical cost that an attractive central prediction could hide.'}
priority=[key for key in priority if any(x['legacy_id']==key for x in r['contributions'])]
for x in r['contributions']:
 x['priority']=priority.index(x['legacy_id'])+1 if x['legacy_id'] in priority else None
 if x['priority']:x['priority_rationale']=reasons[x['legacy_id']]
extra_quantities=[
('CANDIDATE-SCALE-PATH',r'(a_n,g_n^2)=(a_0/n,1/n)','prospectively frozen weak-bare-coupling test path','length and dimensionless coupling','AL1 algebraic candidate only; not a derived physical renormalization trajectory.'),
('HOMOGENEOUS-LOCAL-NORM',r'\epsilon=7|\tau|','complete one-anchor normalized omitted norm','dimensionless','I1/AL context; distinct from the canonical profile deficit also denoted epsilon.'),
('SOURCE-CONSTANTS',r'c_1(S),c_2(S)','inherited range-dependent stability constants','dimensionless','Yarotsky source parameters keep their external attribution and remain unevaluated by AM2.'),
('ONE-FACTOR-WITNESS',r'v_b=(W_p-m_p)\Omega_b','actual one-coarse-factor physical witness','Hilbert vector','AM1: no implication of four excited coarse factors and no measured excitation energy.'),
('FINITE-CREATOR',r'C=\sum_{I\ne\varnothing}\widehat{c_I}','finite-volume nilpotent creation operator','dimensionless','AM2 cutoff proof construction; no bounded infinite-volume similarity operator is asserted.'),
('SPECTRAL-SHIFT',r'|z|<1/2','centered normalized excitation shift','normalized energy','AM2 exclusion window; distinct from the canonical scaled-time z.'),
('INTERPOLATION-PARAMETER',r'|s|\le1','finite-model proof interpolation parameter','dimensionless','AM2 interpolation, distinct from AL2 magnetic suppression despite its reused symbol.'),
('MATCHING-RATIO',r'r=\lambda/\alpha=4/g^4','full uniform magnetic/electric matching ratio','dimensionless','AL1 convention; no new field and no proof of a continuum trajectory.'),
('COMMON-SCALE',r'k>0','common positive energy multiplier','dimensionless','AL2: preserves eligibility ratios but changes physical gaps at fixed units.'),
('MAGNETIC-DEFORMATION',r's\ge0','independent magnetic multiplier','dimensionless','AL2: changing it with electric scale fixed changes the action; it is not a units conversion.'),
('FOUR-SITE-MAJORANT',r'G(t)=16e^{8t}(1+10t)','four-site creation majorant','dimensionless','AM2 proof bound, not a physical generator or invented law.'),
('CREATION-RADIUS',r'R=1/64','creation coefficient-ball radius','dimensionless','AM2 proof parameter; no optimality claim.'),
('GROUPED-SITE-BUDGET',r'J\le28|\tau|','complete indexed interaction budget','dimensionless normalized norm','Includes all four incident whole-star anchors; not a global extensive operator norm.'),
('FINITE-VOLUME-CAP',r'|\tau|\le10^{-8}','explicit finite-volume coupling cap','dimensionless','AM2 full untruncated finite-volume theorem only; no numerical infinite-state interval follows automatically.')]
if any(x['legacy_id']=='AN1' for x in r['contributions']):
 extra_quantities += [
 ('COMMON-BULK-REGION',r'D_n=[-n+2,n-2]^3','twice-eroded comparison bulk','coarse lattice coordinates','AN1 exact boundary dictionary; physical lattice spacing is unchanged.'),
 ('BOUNDARY-COMPARISON-STATES',r'\rho_{A_n},\rho_{B_n}','matched finite-box normal ground states','normalized states','AN1 compares actual whole-star models with the same coarse-translation-invariant selected coefficients.'),
 ('HTW-SMALLNESS',r'7|\tau|\le c_{\rm HTW}(1,1)','independent locality smallness condition','dimensionless','HTW source condition remains unevaluated and is not supplied by AM2.'),
 ('HTW-DECAY',r'\min\{2,e^{2C_1-C_2(n-2)}\}','conditional local comparison enclosure','dimensionless norm bound','AN1: source decay constants remain symbolic; this is not a simulated expectation or an assertion about near-boundary equality.')]
if any(x['legacy_id']=='AN2' for x in r['contributions']):
 extra_quantities += [
 ('INDEPENDENT-CUTOFFS',r'O_{n,L}=[-n,L-n]^3,\ C_M=[-M,M]^3','independent orthant and centered cutoff boxes','coarse lattice coordinates','AN2 requires every L >= 2n and M >= n before the ordered state limits; a diagonal sequence alone does not suffice.'),
 ('BULK-LOCAL-STATE',r'\omega_{\mathbb Z}(A)=\operatorname{Tr}(\rho_F A)','compatible locally normal centered-box state','normalized state','AN2 identifies this specified state under both inherited I1 and independent HTW smallness; equality of generators does not follow.'),
 ('BULK-STATE-ENCLOSURE',r'\varepsilon_n(F)=\min\{2,e^{C_1|F|-C_2(n-r-1)}\}','ordered local-state identification enclosure','dimensionless trace norm','AN2 on a fixed finite complete-factor region F inside [-r,r]^3; C1 and C2 remain unevaluated source constants.'),
 ('INHERITED-STATE-CAP',r'|\tau|<\tau_*','inherited orthant-state sufficient smallness','dimensionless','I1 source-dependent threshold remains distinct from the explicit AM2 finite-volume cap and the additional HTW restriction.')]
if any(x['legacy_id']=='AO1' for x in r['contributions']):
 extra_quantities += [
 ('WILSON-SECOND-MOMENT',r'\mu_{2,\Lambda}=\int E^2\,d\nu_\Lambda(E)','actual finite physical Wilson second moment','energy squared','AO1 proves the uniform bound alpha squared times (36+28|tau|) for the original origin cover under the inherited state conditions.'),
 ('REGIONAL-KINETIC-ENERGY',r'T_R=\alpha\sum_{e\text{ owned by }R}C_e','actual regional electric energy','energy','AO1 reconstructs it from the selected reference, retaining the exact ground scalar before an upper-bound relaxation.'),
 ('WILSON-DERIVATIVE-TERM',r'Z_\Lambda=\sum_{e\in p,a}(X_{ea}W)X_{ea}\Omega_\Lambda','Wilson electric derivative cross term','Hilbert vector','AO1 requires the original half-Pauli normalization; the interacting selected reference is not replaced by a constant Haar vector.')]
if any(x['legacy_id']=='AO2' for x in r['contributions']):
 extra_quantities += [
 ('LIMITING-MOMENT-BUDGET',r'B_2=\alpha^2(36+28|\tau|)','inherited-state physical second-moment budget','energy squared','AO2 bounds the limiting second moment; it does not identify it with a limit of finite second moments.'),
 ('UNIFORM-FIRST-ENERGY-TAIL',r'\int_{E>L}E\,d\nu_\Lambda(E)\le B_2/L','uniform first-energy tail enclosure','energy','AO2 uses L > 0 as a physical spectral cutoff and retains the inherited orthant-state restrictions.'),
 ('LIMITING-FIRST-ENERGY',r'\langle\chi,H_{\rm phys}\chi\rangle=\alpha\omega(1-W^2)','actual inherited-state Wilson first-energy identity','energy','AO2 establishes equality for the same I1/AJ1/AK2 state; another thermodynamic construction needs its own state dictionary.')]
if any(x['legacy_id']=='AQ1' for x in r['contributions']):
 extra_quantities += [
 ('NUMERICAL-CAP-STATE',r'\omega_{\rm num}','locally normal numerical-cap subsequential state','normalized state','AQ1 constructs a full coarse-lattice state without the old symbolic thresholds; uniqueness and identification with the earlier orthant/bulk states are not established.'),
 ('LOCAL-RESET-ENERGY',r'C_F=56|\tau||F|','actual reference reset-energy budget','normalized reference energy','AQ1 includes all incoming whole-star terms; this is not a Haar or pure-electric replacement.'),
 ('COMPACT-RESOLVENT-CUTOFF',r'Q_{F,L}=\mathbf1_{[0,L]}(h_F)','finite-rank local reference-energy cutoff','projection','AQ1 combines the actual compact resolvent with a trace-tail bound; L is normalized reference energy, distinct from AO2 physical energy.'),
 ('DYNAMICS-DECAY-KERNEL',r'F(r)=(1+r)^{-4}','admissible lattice decay kernel','dimensionless','The Nachtergaele--Sims source framework retains its authorship; this choice only supplies the model dictionary.'),
 ('DYNAMICS-INTERACTION-NORM',r'\|\Phi\|_F\le2268|\tau|','complete whole-star interaction norm bound','dimensionless normalized norm','AQ1 norm volume convergence is not norm continuity in time on the full local bounded-operator algebra.'),
 ('NUMERICAL-CAP-GENERATOR',r'H_{\rm num}\ge0','strongly continuous numerical-cap GNS energy generator','energy','AQ1 proves nonnegativity and a reducing physical cyclic restriction; a positive physical gap requires the separate AQ2 gate.')]
if any(x['legacy_id']=='AQ2' for x in r['contributions']):
 extra_quantities += [
 ('ORIGINAL-ENDPOINT-GROUP',r'G=\prod_{v\in V}\mathrm{SU}(2)','complete original-endpoint gauge group','compact group','AQ2 retains every fine-lattice tail and head; the compact product and Haar construction are established mathematics.'),
 ('FULL-PHYSICAL-PROJECTION',r'P_G=\int_GV_g\,dg','complete physical fixed-sector projection','orthogonal projection','AQ2 uses strong vector integration and the actual locally normal GNS state, without a physical tensor-factor decomposition.'),
 ('LOCAL-GAUGE-AVERAGE',r'\mathcal E_F(A)=\int\beta_g(A)\,dg','bounded local endpoint-gauge average','observable','AQ2 operator averaging is ultraweak, not an assumed norm-Bochner integral on all bounded operators.'),
 ('NUMERICAL-PHYSICAL-GAP',r'm_{\rm gap}=\alpha/16','numerical-cap physical spectral-gap lower bound','energy','AQ2 proves it in the chosen AQ1 representation, with simple vacuum there; this is not uniqueness of all thermodynamic states or a particle-mass evaluation.'),
 ('SEVEN-STAR-RESET',r'\omega_{\rm num}(h_R)\le98|\tau|','full-lattice seven-star reference reset bound','normalized reference energy','AQ2 applies to the same original two-factor Wilson cover; the orthant two-star count cannot be substituted.'),
 ('NUMERICAL-STATE-TRACE-BOUND',r'\|\rho_R-P_R\|_1\le1/500','same-state reference trace-distance enclosure','dimensionless trace norm','AQ2 compares the interacting marginal to its actual selected-reference product at |tau| <= 10^-8; it does not call the interacting state Haar.'),
 ('NUMERICAL-WILSON-VARIANCE',r'\operatorname{Var}_{\omega_{\rm num}}(W)\ge61999/250000>1/5','common numerical-cap Wilson variance floor','dimensionless','AQ2 makes the physical excitation nonzero in the same state, without importing the older AO2 operator domain or moment identity.'),
 ('REVERSE-WILSON-VARIANCE',r'\operatorname{Var}_{\omega_{\rm num}}(W)\ge3099951/12500000','separately admitted reverse variance refinement','dimensionless','AQ2 reverse proof and gate support this stronger floor; common synthesis retains the forward floor and explicit attribution.')]
for rid,symbol,name,units,limit in extra_quantities:
 if rid.startswith(('FOUR','CREATION','GROUPED','FINITE')) and not any(x['legacy_id']=='AM2' for x in r['contributions']):continue
 entry=dict(id='HNM-Q-'+rid,symbol=symbol,display_name='Hruday registry: '+name,units=units,limitation=limit)
 if not any(x['id']==entry['id'] for x in r['quantities']):r['quantities'].append(entry)
r['statements']=[]
statement_types={'AL1':('P','scoped proposition'),'AL2':('P','scoped proposition'),'AM2':('T','scoped theorem'),'AN1':('P','source-theorem application'),'AN2':('T','source-theorem application'),'AO1':('P','scoped proposition'),'AO2':('P','scoped proposition'),'AQ1':('T','source-theorem application'),'AQ2':('T','source-theorem application')}
for x in r['contributions']:
 x['statement_ids']=[]
 if x['round']!=29 or x['legacy_id'] not in statement_types:continue
 if x['status'] not in ['accepted_within_scope','accepted']:continue
 rid=x['legacy_id'];prefix,kind=statement_types[rid];sid='HNM-'+prefix+'-'+rid
 r['statements'].append(dict(id=sid,type=kind,contribution_id=x['id'],legacy_id=rid,title=x['display_name'],summary=x['application'],scope=x['limitation'],status=x['status'],source_paths=x['source_paths'],gate=x['source_paths'][0],manuscript_label='stmt:'+rid,priority_status='Project statement alias; scientific priority remains unverified.'))
 x['statement_ids']=[sid]
for x in r['contributions']:
 x['current_extensions']=[]
 for later in {'AK2':['AO2'],'AM1':['AM2'],'AM2':['AQ1','AQ2'],'AN1':['AN2'],'AO1':['AO2'],'AQ1':['AQ2']}.get(x['legacy_id'],[]):
  matches=[y for y in r['contributions'] if y['legacy_id']==later and y['status'] in ['accepted_within_scope','accepted']]
  for y in matches:x['current_extensions'].append({k:y[v] for k,v in [('id','id'),('title','display_name'),('summary','application'),('source_paths','source_paths')]})
r['new_axioms_count']=0
r['axioms']=[]
r['statement_policy']='The number of newly asserted axioms is zero. Semantic statement aliases identify admitted scoped theorems, propositions and source-theorem applications even when the source does not use formal LaTeX theorem environments. They add no premises or proof steps. External axioms and theorem names retain their attribution.'
r['priority_policy']='Qualitative advisor/editorial ordering by usefulness to the declared research route. These are neither numerical discovery scores nor percentages of a continuum proof; literature priority is separate.'
(OUT/'registry/hnm-registry.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
def tx(s):
 s=str(s).replace('–','--').replace('—','---').replace('→','to').replace('≤','<=').replace('≥','>=').replace('≠','!=').replace('∞','infinity').replace('×','x').replace('∈','in')
 s=re.sub(r'\\(?:le|ge)\b','',s)
 for old,new in [('\\addlinespace',''),('\\',''),('$','')]:s=s.replace(old,new)
 return ''.join({'^':r'\textasciicircum{}','~':r'\textasciitilde{}','&':r'\&','%':r'\%','#':r'\#','_':r'\_','{':r'\{','}':r'\}'}.get(c,c) for c in s)
front=r'''\section{Human authorship, integrated coverage and naming policy}
\label{sec:editorial-front}
\textbf{Human author: Hruday N M (BUNZEEY).} This is an integrated manuscript prepared with AI assistance in research, derivation checking, code, source comparison, and editing. Model-agent reviews are disclosed in the historical chapters. No external human peer review or formal proof-assistant verification is claimed; there is no asserted arXiv submission or acceptance.

The complete Draft01 research body and appendices through Round26 and the complete Round27 and Round28 research addenda are carried forward here, including failures, conditions and retrospective roadmaps. The original source packages remain unchanged. A dated roadmap is a record of the question selected then, not a claim that subsequently completed work remains unexecuted. The Round29 chapter contains the new reviewed investigations and the current closing roadmap. Equation numbers and cross-references are unified; original identifiers remain recoverable in the registry.

\subsection{What Hruday and HNM do and do not name}
Hruday names and the HNM namespace identify this project's records. They do not rename Yang--Mills theory, Haar measure, Wilson observables, Jensen's inequality, the GNS construction, Schur complements, Duhamel's formula or any established external theorem. Mathematical notation and physical units stay intact. In particular, adding HNM to a result does not convert a conditional estimate into a theorem about another model, and does not establish historical priority. The number of newly asserted axioms is zero. HNM-T and HNM-P statement aliases identify admitted scoped theorem statements and propositions by mathematical content, including source-theorem applications. These aliases add no premises or proof steps. External axioms retain their names and attribution.

Every contribution has a stable HNM-C identifier with its legacy ID. Labelled equations have stable HNM-E keys derived from their original source labels; the printed HNM equation numbers are document locators. HNM-Q quantity entries give traceable names while retaining their conventional symbols. Shared symbols with different meanings remain local to the stated model. The exact machine-readable registry is \repo{registry/hnm-registry.json}; the appendix prints the contribution aliases and equation concordance.

The double-star marker continues to mean derived, specialized, checked or implemented within this research record. It is not evidence that a method or equation is new to the literature. The priority table ranks usefulness to this route qualitatively, rather than assigning discovery scores or a percentage of the Millennium problem.

\subsection{The requested primary-source comparison changes the novelty boundary}
The September 2026 version of Gauvin's preprint \cite{gauvin2026} gives a regulated $\mathrm{SU}(3)$ analysis in Sections II.3--II.4, with supplemental proofs: physical gap estimates, local Wilson survival, a finite energy moment, and physical GNS correlation bounds. This overlaps the general strategy of our AJ/AK branch. The Wilson variance--moment--window--Jensen mechanism therefore must not be presented as a Hruday invention. Our stated $\mathrm{SU}(2)$ model, constants, domains, boundary convention and source-bound computations remain individually inspectable; their distinct scientific novelty is unverified. The preprint's constants cannot be transferred by relabeling its group or energy scales. Its abstract also leaves the interacting continuum construction open. This is a scoped comparison, not an endorsement or complete proof audit of the external work.

The official problem description \cite{jaffe_witten} remains the governing target: a nontrivial four-dimensional quantum theory of the requisite axiomatic strength with a positive physical mass gap for each compact simple gauge group. Finite graphs, a fixed-spacing homogeneous limit, a selected boundary state and a conditional spectral estimate do not jointly supply that construction. The pending model map, scale trajectory, uniform estimates, nontrivial observables and limiting reconstruction are explicit proof obligations.

\subsection{How to read the enlarged manuscript}
The historical first part establishes the model vocabulary and source-bound calculations. Round27 studies identifiability and one nonlinear correction. Round28 restores complete sources, improves finite-graph heat control and establishes conditional physical Wilson estimates. Round29 tests the next missing implications against the reviewed external sources. Use the ranked appendix to locate a useful result, then read its full assumptions and surviving objection. A negative or insufficient gate is a completed investigation with a limited conclusion, not a solved target.
'''
if any(x['legacy_id']=='AQ1' for x in r['contributions']):
 front=front.replace('The official problem description',r'''The numerical-cap AQ branch has a further explicit prior-method boundary: Gauvin's Supplement A.10 already presents the thermodynamic compactness, dynamics, GNS and Fourier-test strategy. The actual unbounded-onsite dynamics placement uses Nachtergaele--Sims~\citep{nachtergaele2014dynamics}, with the source panel also checking the modern Nachtergaele--Sims--Young framework~\citep{nachtergaele2019quasilocality}. The contribution is a separately checked $\mathrm{SU}(2)$ selected-strip model dictionary and numerical-cap application. Neither renaming nor a bounded-spin theorem supplies the unbounded-rotor hypotheses. Volume-norm convergence of a fixed local evolution remains distinct from norm continuity in time on every bounded local operator.

The official problem description''')
(OUT/'sections/editorial-front.tex').write_text(front)
main_path=OUT/'main.tex';main=main_path.read_text()
main=re.sub(r'\\title\{.*?\}\n\\author',lambda m:r'\title{Hruday gauge-theory workbench:\\spectral bounds, local corrections, Wilson readouts,\\and controlled evolution}'+'\n'+r'\author',main,flags=re.S)
main=re.sub(r'pdftitle=\{[^}]*\}',lambda m:'pdftitle={Hruday gauge-theory workbench}',main)
admitted={x['legacy_id'] for x in r['contributions']}
abstract=r'''This integrated research compendium carries the complete Draft01 body through Round26, the Round27 and Round28 addenda, and the reviewed Round29 continuation. It follows regulated benchmarks, finite and full-representation $\mathrm{SU}(2)$ calculations, canonical readouts and a distinct homogeneous fixed-lattice model. Results include controlled spectral and heat approximations, a critical growing-time endpoint counterexample, complete source budgets and conditional nonzero physical Wilson fluctuations. '''
if 'AM2' in admitted:
 abstract+=r'''A four-site creation certificate gives a unique ground and physical gap at least $\alpha/16$ for every nonempty finite complete-factor volume at both signs of $|\tau|\le10^{-8}$, with representation cutoffs removed. '''
if 'AQ1' in admitted:
 abstract+=r'''A separate construction at that numerical cap supplies a locally normal full-lattice subsequential state and strongly continuous GNS evolution. '''
 if 'AQ2' in admitted:
  abstract+=r'''In that same representation the complete original-endpoint physical sector has gap at least $\alpha/16$, a simple vacuum and original Wilson variance greater than $1/5$. The full-GNS strengthening uses the separately reviewed full-Hilbert finite-volume premise. '''
 else:abstract+=r'''Its physical energy generator is nonnegative. '''
 abstract+=r'''This does not identify the earlier conditional orthant state or establish uniqueness of all thermodynamic states. '''
if 'AO2' in admitted:
 abstract+=r'''For the earlier orthant state under its original restrictions, a uniform second-moment estimate establishes the actual Wilson operator domain and exact first-energy identity; equality of second moments remains unproved. '''
abstract+=r'''Contemporary primary-source comparison materially limits distinct mathematical novelty. Hruday/HNM labels identify project records; established mechanisms retain their attribution. These fixed-model results do not construct four-dimensional continuum Yang--Mills theory or prove its continuum physical mass gap.'''
main=re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}',lambda m:r'\begin{abstract}'+'\n'+abstract+'\n'+r'\end{abstract}',main,flags=re.S)
main_path.write_text(main)
bib=OUT/'sources/references.bib'
if 'nachtergaele2019quasilocality' not in bib.read_text():
 bib.write_text(bib.read_text()+'''\n@article{nachtergaele2019quasilocality,
 author={Bruno Nachtergaele and Robert Sims and Amanda Young},
 title={Quasi-Locality Bounds for Quantum Lattice Systems. Part I. Lieb--Robinson Bounds, Quasi-Local Maps, and Spectral Flow Automorphisms},
 journal={Journal of Mathematical Physics},
 volume={60},
 pages={061101},
 year={2019},
 doi={10.1063/1.5095769},
 eprint={1810.02428},
 archivePrefix={arXiv},
 note={Source version arXiv:1810.02428v2},
 url={https://arxiv.org/abs/1810.02428v2}
}\n''')
if 'gauvin2026' not in bib.read_text():
 bib.write_text(bib.read_text()+'''\n@misc{gauvin2026,
 author={Shoshauna Gauvin},
 title={Pinched Multi Affine Geometry and Confinement: Describing the Yang--Mills Mass Gap},
 year={2026},
 eprint={2503.15539},
 archivePrefix={arXiv},
 primaryClass={physics.gen-ph},
 note={Version 3, revised 14 September 2026. Sections II.3--II.4 and accompanying supplemental material; preprint, not adopted as an independently verified premise},
 url={https://arxiv.org/abs/2503.15539v3}
}\n''')
for stem in ['aj1','aj2','ak1','ak2']:
 p=OUT/f'addenda/round28/loops/{stem}.tex';s=p.read_text(); pos=s.index('\n',s.index('\\section{'))+1
 note=r'\begin{quote}\small Draft02 attribution update. See Section~\ref{sec:editorial-front} for the primary-source comparison and its novelty limitation. HNM labels identify project records.\end{quote}'
 s=re.sub(r'\\begin\{quote\}\\small Draft02 attribution update\..*?\\end\{quote\}\n?', '', s)
 pos=s.index('\n',s.index('\\section{'))+1
 s=s[:pos]+note+'\n'+s[pos:]
 p.write_text(s)
for x in r['contributions']:
 rid=x['legacy_id'];path=OUT/f'addenda/round29/{rid.lower()}.tex' if x['round']==29 else OUT/'addenda/round28/loops/ak2.tex' if rid=='AK2' else None
 if path is None or not path.exists():continue
 text=path.read_text()
 text=re.sub(r'% BEGIN CURRENT REGISTRY NOTE\n.*?% END CURRENT REGISTRY NOTE\n','',text,flags=re.S)
 notes=[]
 if x['statement_ids']:
  sid=x['statement_ids'][0]
  notes.append(r'\paragraph{Statement alias '+tx(sid)+r'.}\label{stmt:'+rid+r'} This identifier denotes the scoped mathematical claim admitted by this chapter\textquotesingle s gate. It adds no assumption and establishes no literature-priority claim.')
 for ext in x['current_extensions']:
  lid=ext['id'].removeprefix('HNM-C-')
  notes.append(r'\begin{quote}\small\textbf{Current extension: '+tx(ext['id'])+r'.} The historical limitation below remains the scope of this original result. The later, separately gated statement in Section~\ref{stmt:'+lid+'} records the extension: '+tx(ext['summary'])+r' Its own model and state assumptions remain required.\end{quote}')
 if notes:
  pos=text.index('\n',text.index(r'\section{'))+1
  text=text[:pos]+'% BEGIN CURRENT REGISTRY NOTE\n'+'\n'.join(notes)+'\n% END CURRENT REGISTRY NOTE\n'+text[pos:]
 path.write_text(text)
lines=['# Hruday / HNM contribution registry','','Human author: **Hruday N M (BUNZEEY)**. HNM names identify project records, not scientific priority. Standard mathematical and physical symbols remain unchanged.','','| Stable ID | Legacy ID | Project display name | Classification |','|---|---|---|---|']
for x in r['contributions']:lines.append('| '+x['id']+' | '+x['legacy_id']+' | '+x['display_name']+' | '+x['classification']+' |')
(OUT/'registry/README.md').write_text('\n'.join(lines)+'\n')
for n in ['ym-round27-contraction-bounds.png','ym-round27-discrimination.png']:shutil.copy2(ROOT/'dist'/n,OUT/'figures'/n)
for p in (OUT/'addenda/round27').rglob('*.tex'):p.write_text(p.read_text().replace('../../dist/ym-round27-','figures/ym-round27-'))
lines=[r'\section{Priority-ranked admitted results and their limits}',r'\label{app:priority}',r'This qualitative ordering selects findings most useful to the declared research route; the complete contribution catalog follows. It does not rank scientific priority, assign discovery scores or estimate how much of continuum Yang--Mills has been solved. All entries are scoped to their stated model. New Round29 findings are recorded separately with their gate verdicts; a recently executed loop does not outrank a prior result merely by recency. Limitations describe each named result at its own gate; separately gated current extensions may close a listed obligation only under their own model and state assumptions.',r'\begingroup\small\setlength{\tabcolsep}{4pt}',r'\begin{longtable}{@{}p{8mm}p{44mm}p{53mm}p{43mm}@{}}',r'\toprule Rank & HNM record & Why useful / application & Surviving limitation\\\midrule\endhead']
for x in sorted([x for x in r['contributions'] if x['priority']],key=lambda x:x['priority']):
 limit=tx(x['limitation'])
 if x['current_extensions']:limit+=r'\par Current separately gated extensions: '+', '.join(tx(e['id']) for e in x['current_extensions'])+'.'
 lines.append(str(x['priority'])+' & '+r'\textbf{'+tx(x['id'])+'} '+tx(x['title'])+' & '+tx(x['priority_rationale'])+' & '+limit+r'\\\addlinespace')
lines += [r'\bottomrule\end{longtable}\endgroup']
(OUT/'sections/priority-appendix.tex').write_text('\n'.join(lines)+'\n')
lines=[r'\section{Complete HNM naming and equation concordance}',r'\label{app:hnm-names}',r'The HNM-C IDs below map every contribution in the original 114-row catalog and the two integrated addenda. The equation keys are stable source aliases; printed equation numbers are locators in this edition. No alias changes a model, variable, proof premise, external eponym or literature-priority status.',r'\subsection{Contribution aliases}',r'\begingroup\footnotesize\setlength{\tabcolsep}{4pt}',r'\begin{longtable}{@{}p{30mm}p{26mm}p{65mm}p{27mm}@{}}',r'\toprule HNM ID & Legacy ID & Hruday project name & Classification\\\midrule\endhead']
for x in r['contributions']:lines.append(tx(x['id'])+' & '+tx(x['legacy_id'])+' & '+tx(x['display_name'])+' & '+tx(x['classification'])+r'\\\addlinespace')
lines += [r'\bottomrule\end{longtable}\endgroup',r'\subsection{Scoped statement aliases}',r'These semantic names index admitted claims, not newly invented axioms. Each linked chapter supplies the complete hypotheses, proof record, source attribution and final limitations. The theorem/proposition naming does not imply external peer review.',r'\begingroup\small\setlength{\tabcolsep}{4pt}',r'\begin{longtable}{@{}p{32mm}p{36mm}p{80mm}@{}}',r'\toprule Statement alias & Type / chapter & Named scoped statement\\\midrule\endhead']
for s in r['statements']:lines.append(tx(s['id'])+' & '+tx(s['type'])+r'; Section~\ref{'+s['manuscript_label']+'} & '+tx(s['title'])+r'\\\addlinespace')
lines += [r'\bottomrule\end{longtable}\endgroup',r'\subsection{Named quantity aliases}',r'\begingroup\small\setlength{\tabcolsep}{4pt}',r'\begin{longtable}{@{}p{37mm}p{40mm}p{72mm}@{}}',r'\toprule HNM quantity & Retained notation / units & Meaning and limit\\\midrule\endhead']
for q in r['quantities']:lines.append(tx(q['id'])+' & $'+q['symbol']+'$; '+tx(q['units'])+' & '+tx(q['display_name'])+'. '+tx(q['limitation'])+r'\\\addlinespace')
lines += [r'\bottomrule\end{longtable}\endgroup',r'\subsection{Labelled equation aliases}',r'\begingroup\footnotesize\setlength{\tabcolsep}{4pt}',r'\begin{longtable}{@{}p{99mm}p{47mm}@{}}',r'\toprule Stable equation alias & Equation in this edition\\\midrule\endhead']
for e in r['equations']:lines.append(r'\path{'+e['id']+'} & '+r'\eqref{'+e['legacy_label']+'}'+r'\\')
lines += [r'\bottomrule\end{longtable}\endgroup']
(OUT/'sections/naming-appendix.tex').write_text('\n'.join(lines)+'\n')
p=OUT/'sections/round29.tex'
if not p.exists():p.write_text(r'''\section{Round29 editorial integration checkpoint}
The reviewed Round29 research findings are being integrated. No unreviewed investigation is admitted by this editorial checkpoint; the release builder requires the final ten-loop findings and gates before publication.
''')
print(json.dumps({'contributions':len(r['contributions']),'equations':len(r['equations']),'priorities':len(priority)}))
