#!/usr/bin/env python3
"""Create additive Draft02. Historical source files are read-only inputs."""
from pathlib import Path
import json, re, shutil, hashlib, subprocess
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'papers/draft-02'; OLD=ROOT/'papers/draft-01'
OUT.mkdir(exist_ok=True)
for name in ['sections','sources','figures','calculators','audit']:
    if (OLD/name).exists(): shutil.copytree(OLD/name,OUT/name,dirs_exist_ok=True)
for name in ['calculators.html','main.bbl']:
    if (OLD/name).exists(): shutil.copy2(OLD/name,OUT/name)
(OUT/'registry').mkdir(exist_ok=True)

def tex(s):
    s=str(s).replace('–','--').replace('—','---').replace('→',r'$\to$').replace('≤',r'$\le$').replace('≥',r'$\ge$')
    return ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}'}.get(c,c) for c in s)

def classify(r):
    status=r['status']
    if status=='model-specific derivation, obstruction, or certified computation':status=''
    text=(r['title']+' '+status).lower()
    if any(s in text for s in ['obstruction','counterexample','no-go','insufficient']): return 'scoped obstruction or negative control'
    if any(s in text for s in ['numerical','computation','arithmetic','certificate','enumeration','algorithm']): return 'scoped computation or certificate'
    if any(s in text for s in ['conjecture','proposed']): return 'conjecture or proposed route'
    if any(s in text for s in ['established','known','specialization','application']): return 'application of established mathematics'
    return 'scoped derivation'
rows=[]
for r in json.loads((OLD/'audit/contribution-catalog.json').read_text())['contributions']:
    c=dict(r); c['legacy_id']=r['id']; c['legacy_title']=r['title']; c['id']='HNM-C-'+r['id'].upper(); c['display_name']='Hruday '+r['title'][0].lower()+r['title'][1:]; c['classification']=classify(r); c['round']='3–26'; c['priority']=None
    c['priority_status']='unverified; registry attribution is not scientific priority'; rows.append(c)
# Derived metadata transcribes admitted addendum ledgers; no new proof status is assigned.
r27=[
('R27-AI1-FIBERS','Exact readout fibers','scoped derivation','Remove redundant parameter fits and identify required independent calibration.','The exact surrogate fibers are not equivalences of the finite-q physical model.','papers/round27-addendum/round27-addendum.tex'),
('R27-AI1-CARRIER','Carrier and slow-rate identification','scoped derivation','Design phase-aware nonaliased readouts.','Calibrated time, action and phase are additional data; eta–q ambiguity remains.','papers/round27-addendum/round27-addendum.tex'),
('R27-AI2-SUPPORT','Complete physical multiplier support','scoped computation or certificate','Retain all observable-dependent outside channels.','Source-specific canonical family; the reached component is not the full shell.','papers/round27-addendum/ai2.tex'),
('R27-AI2-DISKS','Complete scalar prediction-disk separation','scoped computation or certificate','Reject one of two frozen candidate models using complete error disks.','One successful frozen grid cell; enormous time and tiny error allowance; no apparatus or continuous inverse.','papers/round27-addendum/ai2.tex'),
('R27-AG1','One selected-source homogeneous correction','application of established mathematics','Track nonlinear remainder and spent support weight in one actual correction.','Restricted source sector and one update; no complete-Hamiltonian contraction or iteration.','papers/round27-addendum/ag1.tex')]
for rid,title,status,use,limit,source in r27:
    rows.append(dict(id='HNM-C-'+rid,legacy_id=rid,legacy_title=title,title=title,display_name='Hruday '+title[0].lower()+title[1:],classification=status,status=status,round=27,equation_labels=[],source_paths=[source],application=use,limitation=limit,next='See the linked admitted derivation and current roadmap.',priority=None,priority_status='unverified; registry attribution is not scientific priority'))
scope=(ROOT/'papers/round28-addendum/scope-table.tex').read_text()
r28names={'AG2':'Complete original-remainder transport','AG3':'One complete-source homogeneous correction','AI3':'Odd-moment and reflection-tail certificate','AI4':'Uniform conditional physical ratio separation','AH1':'561-state physical graph enrichment','AH2':'Delayed-loading heat certificate','AJ1':'Locally normal physical representation','AJ2':'Nonzero original Wilson fluctuation','AK1':'Conditional Wilson variance floor','AK2':'Wilson form-energy, spectral-window and heat-envelope certificate'}
for line in scope.splitlines():
    if not re.match(r'^(AG|AI|AH|AJ|AK)\d &',line):continue
    rid,summary,use,limit=line.split(' & ',3); limit=re.sub(r'\\\\.*','',limit).strip()
    title=r28names[rid]
    rows.append(dict(id='HNM-C-'+rid,legacy_id=rid,legacy_title=title,title=title,display_name='Hruday '+title[0].lower()+title[1:],classification='application of established mathematics' if rid in ['AJ1','AJ2','AK1','AK2'] else 'scoped computation or certificate',status='accepted within the frozen model and assumptions',round=28,equation_labels=[],source_paths=['papers/round28-addendum/loops/'+rid.lower()+'.tex','research/round28/advisor/'+rid.lower()+'-gate.json'],application=use,limitation=limit,next='See the inherited closeout and the Round29 review.',summary=summary,priority=None,priority_status='unverified; arXiv:2503.15539v3 comparison limits distinctness for the homogeneous Wilson branch'))
# Priority is editorial value for this route, not theorem-completion units or scientific priority.
priority_ids=['AK2','AK1','AJ1','AJ2','AH2','AI4','AG2','AG3','R27-AI1-FIBERS','R27-AI2-DISKS']
for r in rows:
    if r['legacy_id'] in priority_ids:r['priority']=priority_ids.index(r['legacy_id'])+1

# Preserve every source-body paragraph, with new labels/paths only; historical roadmap prose is explicitly dated.
for r in [27,28]:
    src=ROOT/f'papers/round{r}-addendum'; target=OUT/f'addenda/round{r}'
    target.mkdir(parents=True,exist_ok=True)
    for p in src.rglob('*.tex'):
        if p.name in ['main.tex','round27-addendum.tex']:continue
        dst=target/p.relative_to(src);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dst)
    if (src/'figures').exists():shutil.copytree(src/'figures',target/'figures',dirs_exist_ok=True)
    original=(src/('round27-addendum.tex' if r==27 else 'main.tex')).read_text()
    body=original[original.index(r'\section{Inherited'):original.index(r'\end{document}')]
    if r==27:body=body.replace(r'\appendix',r'\subsection*{Round27 contribution and reproduction appendix (historical checkpoint)}')
    else:body=body.replace(r'\appendix',r'\subsection*{Round28 contribution and reproduction appendix (historical checkpoint)}')
    (target/'body.tex').write_text(body)
    for p in target.rglob('*.tex'):
        content=p.read_text()
        content=re.sub(r'\\(label|eqref|ref|autoref)\{([^}]+)\}',lambda m:'\\'+m[1]+'{r'+str(r)+':'+m[2]+'}',content)
        content=re.sub(r'\\input\{([^}]+)\}',lambda m:r'\input{addenda/round'+str(r)+'/'+m[1]+'}',content)
        if r==28:content=re.sub(r'(\\includegraphics(?:\[[^]]*\])?\{)(figures/)',lambda m:m[1]+'addenda/round28/'+m[2],content)
        for rid in r28names if r==28 else ['AI1','AI2','AG1']:
            content=content.replace(r'\section{'+rid+':',r'\section{HNM '+rid+':')
        # Earlier closeouts are retained verbatim as dated snapshots, not the current stopping state.
        if p.name in ['closeout.tex','contributions.tex']:
            content='\\begin{quote}\\small Historical Round'+str(r)+' checkpoint. References below to planned, unexecuted or next work describe the state at that checkpoint; the integrated Round29 chapter supersedes that plan.\\end{quote}\n'+content
        content=content.replace('p{46mm}','p{44mm}') if r==27 else content.replace('p{48mm}','p{47mm}')
        p.write_text(content)
# Human authorship overrides old pending-author copy in the current manuscript, without touching archives.
road=OUT/'sections/roadmap.tex'; s=road.read_text(); s=s[:s.index(r'\section*{Authorship')]; s='\\begin{quote}\\small Historical Round26 roadmap; subsequent integrated chapters record its execution.\\end{quote}\n'+s; road.write_text(s)
p=OUT/'sections/introduction.tex';s=p.read_text().replace('research compendium and first manuscript','integrated research compendium').replace('throughout this first draft','throughout this manuscript'); s=s.replace('The source checkpoint is repository commit','The historical Round26 source checkpoint is repository commit');p.write_text(s)
# Alias every catalog entry in the integrated copy. Keep legacy IDs alongside stable aliases.
p=OUT/'sections/contribution-appendix.tex';s=p.read_text()
for r in rows[:114]:s=s.replace(r'\textbf{'+r['legacy_id']+'}',r'\textbf{'+r['id']+'} (legacy '+r['legacy_id']+')')
p.write_text(s)
# Equation aliases are stable keys based on original source labels. Printed HNM numbers are document locators.
eqs=[]; statements=[]
for p in sorted((OUT/'sections').glob('*.tex'))+sorted((OUT/'addenda').rglob('*.tex')):
    if p.name in ['contribution-appendix.tex','history-appendix.tex']:continue
    s=p.read_text()
    for lab in re.findall(r'\\label\{([^}]+)\}',s):
        if lab.startswith(('eq:','early:','recent:','r27:eq:','r28:eq:')):
            eid='HNM-E-'+re.sub('[^A-Za-z0-9]+','-',lab).upper().strip('-')
            related=[r['id'] for r in rows if lab in r['equation_labels'] or (lab.startswith('r28:eq:') and lab[7:].split('-')[0].upper()==r['legacy_id'])]
            eqs.append(dict(id=eid,legacy_label=lab,source=str(p.relative_to(OUT)),contribution_ids=related,scope='Document alias; see equation assumptions and attribution in source. No renaming of standard mathematics.'))
    for i,m in enumerate(re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary|definition)\}(?:\[([^]]*)\])?',s),1):
        statements.append(dict(id='HNM-S-'+p.stem.upper()+'-'+str(i).zfill(3),kind=m[1],original_title=m[2],source=str(p.relative_to(OUT)),scope='Scoped manuscript statement; theorem title does not establish original scientific priority.'))
quantities=[
('ENERGY-REFERENCE',r'E_\star','fixed positive physical energy reference','energy','Reference, not a fitted constant.'),
('KINETIC-SCALE',r'\alpha','declared kinetic energy scale','energy','Model-local scale; no continuum identification supplied.'),
('ACTION',r'\hbar','fixed action reference','action','Established physical constant, not a project invention.'),
('HOMOGENEOUS-UNIT',r'\delta=\alpha/8','homogeneous conversion unit','energy','Inherited normalization, not a new fundamental constant.'),
('HOMOGENEOUS-COUPLING',r'\tau','homogeneous omitted-interaction coupling','dimensionless','Admissible symbolic interval also required.'),
('STABILITY-RADIUS',r'\tau_*','unevaluated homogeneous stability radius','dimensionless','Positive theorem parameter; not yet a certified numerical interval.'),
('CANONICAL-PROFILE',r'q','canonical summable profile parameter','dimensionless','Not identified with lattice spacing.'),
('CANONICAL-STRENGTH',r'\eta','canonical coupling strength','dimensionless','Not automatically a homogeneous coupling.'),
('PROFILE-DEFECT',r'\epsilon=1-q','canonical profile deficit','dimensionless','Separate from a continuum regulator.'),
('SLOW-COMPOSITE',r'\rho=\eta(1-q)^3','canonical slow composite','dimensionless','Readout information is model and protocol dependent.'),
('CARRIER-RATE',r'\beta=\alpha/\hbar','carrier scale','inverse time','Requires calibrated physical time and action.'),
('SLOW-RATE',r'\lambda=\beta\rho/84','surrogate slow rate','inverse time','This lambda is distinct from couplings reused in other chapters.'),
('WILSON-WITNESS',r'\chi=(\pi(W)-\omega(W)I)\Omega','centered physical Wilson vector','Hilbert vector','Specified origin plaquette and conditional orthant state.'),
('WILSON-VARIANCE',r'v=\|\chi\|^2','Wilson fluctuation mass','dimensionless','Variance, not number of particles.'),
('WILSON-MEASURE',r'\nu','Wilson spectral measure','dimensionless mass','Positive actual state-dependent measure, not an evaluated spectrum.'),
('FIRST-MOMENT',r'\mu_1=\int E\,d\nu(E)','Wilson first energy moment','energy','Upper bound passes to limit; equality needs additional control.'),
('HEAT-READOUT',r'C(t)','physical imaginary-time Wilson correlation','dimensionless','Not a real-time signal or measured mass.'),
('HEAT-CLOCK',r'\sigma=\alpha t/\hbar','finite-graph heat coordinate','dimensionless','Each finite and full heat uses its correct ground center.'),
('SUPPORT-WEIGHT',r'a','rooted support-cardinality proof weight','dimensionless','Symbol a elsewhere denotes spacing; meaning is local to model.')]
registry=dict(schema_version=1,human_author='Hruday N M (BUNZEEY)',naming_policy='HNM and Hruday are project attribution/document aliases. Historical IDs, external eponyms, physical symbols, source evidence and known theorem attribution are preserved. Renaming provides no evidence of scientific novelty or priority.',contribution_count=len(rows),contributions=rows,equations=eqs,statements=statements,quantities=[dict(id='HNM-Q-'+rid,symbol=symbol,display_name='Hruday registry: '+name,units=units,limitation=limit) for rid,symbol,name,units,limit in quantities])
(OUT/'registry/hnm-registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
# All newly generated source paths are in Draft02, making it self contained apart from original R27 plot links.
main=(OLD/'main.tex').read_text()
main=main.replace(r'\fancyhead[L]{\small Certified finite-model gauge calculations}',r'\fancyhead[L]{\small Hruday N M (BUNZEEY): gauge workbench}')
main=main.replace(r'\fancyhead[R]{\small First draft}',r'\fancyhead[R]{\small Integrated Draft02}')
main=main.replace(r'\DeclareMathOperator{\Cov}{Cov}',r'\DeclareMathOperator{\Cov}{Cov}'+'\n'+r'\DeclareMathOperator{\ad}{ad}'+'\n'+r'\DeclareMathOperator{\Impart}{Im}'+'\n'+r'\renewcommand{\theequation}{HNM-\arabic{equation}}')
main=main.replace('pdfsubject={First research compendium draft through Round26}','pdfsubject={Integrated source-bound research compendium through Round29},pdfauthor={Hruday N M (BUNZEEY)}')
main=main.replace(r'\author{First manuscript draft for author review}',r'\author{Hruday N M (BUNZEEY)}').replace('Research checkpoint: Round26','Integrated research checkpoint: Round29')
start=main.index(r'\begin{abstract}');end=main.index(r'\clearpage',start)
main=main[:start]+r'''\begin{abstract}
This integrated research compendium assembles the complete surviving Draft01 body through Round26, the Round27 and Round28 addenda, and the new Round29 review. It follows regulated mean-field benchmarks, finite and full-representation $\mathrm{SU}(2)$ calculations, canonical readouts, and a distinct homogeneous fixed-lattice model. Project results include controlled spectral and heat approximations, explicit identification obstructions, complete source budgets, and conditional nonzero physical Wilson fluctuations. The latter admit quantitative variance, first-energy-moment, finite spectral-window and imaginary-time bounds under inherited stability assumptions. A new four-site creation certificate gives a unique ground and physical gap at least $\alpha/16$ for every nonempty finite complete-factor volume at both signs of $|\tau|\le10^{-8}$, with representation cutoffs removed. This numerical finite-volume result does not select an infinite-volume state. Contemporary primary-source comparison materially limits any claim of distinct mathematical novelty. Hruday/HNM labels are traceable project aliases; established mechanisms retain their attribution. Model-specific derivations and reproducible code do not construct the required four-dimensional continuum Yang--Mills theory or prove its continuum physical mass gap.
\end{abstract}
\begin{center}\small\textbf{Human author: Hruday N M (BUNZEEY).} AI systems assisted research, mathematical checking, implementation and editing. No external human peer review, journal acceptance or arXiv submission is claimed. Scientific priority remains unverified.\end{center}
'''+main[end:]
main=main.replace(r'\input{sections/introduction}',r'\input{sections/editorial-front}'+'\n'+r'\input{sections/introduction}')
main=main.replace(r'\input{sections/roadmap}',r'\input{sections/roadmap}'+'\n'+r'\clearpage\part{Round27: readout identification and nonlinear correction}'+'\n'+r'\input{addenda/round27/body}'+'\n'+r'\clearpage\part{Round28: complete remainders and physical observables}'+'\n'+r'\input{addenda/round28/body}'+'\n'+r'\clearpage\part{Round29: source comparison and next admitted investigations}'+'\n'+r'\input{sections/round29}')
main=main.replace(r'\input{sections/contribution-appendix}',r'\input{sections/priority-appendix}'+'\n'+r'\input{sections/naming-appendix}'+'\n'+r'\input{sections/contribution-appendix}')
main=main.replace(r'\begin{document}',r'\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}'+'\n'+r'\begin{document}')
(OUT/'main.tex').write_text(main)
# Human-readable registry, kept alongside exact machine-readable keys.
lines=['# Hruday / HNM contribution registry','','Human author: **Hruday N M (BUNZEEY)**. Names identify workbench records, not scientific priority. Standard mathematical and physical symbols remain unchanged.','','| Stable ID | Legacy ID | Project display name | Classification |','|---|---|---|---|']
for r in rows:lines.append('| '+r['id']+' | '+r['legacy_id']+' | '+r['display_name']+' | '+r['classification']+' |')
(OUT/'registry/README.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'contributions':len(rows),'equation_aliases':len(eqs),'statement_aliases':len(statements),'quantities':len(quantities)}))
