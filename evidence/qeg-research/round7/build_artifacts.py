#!/usr/bin/env python3
"""Create the cited report, scientific figures and recorded Site data."""
from pathlib import Path
import csv
import html
import json
import re
import shutil
import textwrap
import numpy as np
import scipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, LongTable, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE=Path(__file__).resolve().parent
SITE=HERE.parents[1]/'physics-observatory'/'dist'
OUT=HERE/'output'; OUT.mkdir(exist_ok=True)

def read(name): return json.loads((HERE/name).read_text())
def csvrows(name): return list(csv.DictReader((HERE/name).open()))
f=read('finite_results.json'); g=read('gravity_results.json')
root=read('root_validation.json'); critic=read('independent_results.json')
proof=read('proof_search_results.json'); lib=read('proof_library.json')
if any(r['status']!='passed' for r in (f,g,root,critic)) or len(g['cases'])!=8:
    raise RuntimeError('Complete validated scientific output required before authoring')

fc=csvrows('finite_correct.csv'); fw=csvrows('finite_wrong.csv'); gc=csvrows('gravity_constraints.csv')
gm=[r for r in gc if r['case']=='coupled_mixed']
def points(rows,x,y): return [[float(r[x]),float(r[y])] for r in rows]
plots={
 'finite':dict(title='A dynamical scalar exchanges energy with the driven field',xLabel='s = electron mass × time',yLabel='Dimensionless fields',csv='/finite_correct.csv',
     caption='Recorded finite model: b=10, N=1 inclusive, K=20, nK=128; g=0.1, nu=0.5, phi(0)=0.4, y(0)=0.1. The drive has support 0<s<4. These fields use electron-based units.',
     series=[dict(name='Electric field x',points=points(fc,'t','x')),dict(name='Scalar phi',points=points(fc,'t','phi'))]),
 'work':dict(title='Removing one exchange term breaks the energy balance',xLabel='s',yLabel='W(s) − W(0) − external work',csv='/finite_wrong.csv',
     caption='Correct and deliberately incomplete finite equations, with identical preparation and drive. The omitted Maxwell term produces the independently integrated defect f_phi y x². The difference is physical inconsistency of the modified model, not evidence of numerical instability.',
     series=[dict(name='Complete finite action',points=points(fc,'t','energy_mismatch')),dict(name='Omitted Maxwell exchange',points=points(fw,'t','energy_mismatch'))]),
 'gravity':dict(title='The Einstein constraint detects an unsupported scalar force',xLabel='tau = reference frequency × time',yLabel='Dimensionless Hamiltonian constraint',csv='/gravity_constraints.csv',
     caption='Classical Bianchi I mixed-field case, c=0.45, mhat=0.35, lambda=0.01. Correct evolution retains the constraint; removing only the scalar electromagnetic force creates the predicted Ward-driven drift. No QED quantum stress is present.',
     series=[dict(name='Complete classical stress',points=points(gm,'tau','C_full')),dict(name='Omitted scalar force',points=points(gm,'tau','C_wrong'))])}

plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white'})
for key,p in plots.items():
    fig,ax=plt.subplots(figsize=(8.2,4.1),layout='constrained')
    for i,s in enumerate(p['series']):
        a=np.asarray(s['points']); ax.plot(a[:,0],a[:,1],label=s['name'],color=('#146d75','#b04738')[i],lw=2)
    ax.set(xlabel=p['xLabel'],ylabel=p['yLabel'],title=p['title']);ax.grid(alpha=.18);ax.legend(loc='best',frameon=False)
    fig.savefig(OUT/f'{key}.png',dpi=180);fig.savefig(OUT/f'{key}.pdf');plt.close(fig)

sources=[];seen=set()
for name in ('renormalization_sources.json','skeptic_sources.json'):
    for s in read(name)['sources']:
        if s['url'] not in seen: sources.append(s);seen.add(s['url'])
documents={f'round7/{p.name}':p.read_text() for p in [HERE/n for n in
 ['variable_contract.md','advisor_plan.md','renormalization_map.md','skeptic_review.md','code_audit.md','search_contract.md']]}
scenarios={'finite_continuation':{k:v for k,v in lib.items() if k!='scenarios'},**lib['scenarios']}
results={'finite_continuation':{k:v for k,v in proof.items() if k!='scenario_results'},**proof['scenario_results']}
routes={k:dict(library=v,result={q:r for q,r in results[k].items() if q not in ('search_trace','frontier')}) for k,v in scenarios.items()}
site_data=dict(round=7,date='9 September 2026',finite=f,gravity=g,root=root,critic=critic,
               plots=plots,sources=sources,documents=documents,routes=routes,
               variables=read('variable_dependencies.json')['variables'])
SITE.mkdir(exist_ok=True)
(SITE/'research-closures-data.js').write_text('window.OBSERVATORY_CLOSURES = '+json.dumps(site_data,ensure_ascii=False).replace('</','<'+chr(92)+'/')+';\n')
(SITE/'closure-proof-map.json').write_text(json.dumps(dict(libraries=scenarios,results=results),indent=2)+'\n')
for name in ['finite_correct.csv','finite_wrong.csv','finite_delayed.csv','finite_refinement.csv','finite_matrix.csv',
             'gravity_constraints.csv','gravity_case_summary.csv']:
    shutil.copy2(HERE/name,SITE/name)

fd=f['gates']; gd=g['cases'][0]['diagnostics']
spinerr=max(c['evidence'] for c in root['checks'] if c['name'].startswith('Spinor/Bloch agreement:'))
report=f'''# Einstein-QED: variables, cutoff matching and two verified reduced closures

Research snapshot: 9 September 2026. Round 7 of the Physics Observatory.

## What changed and what this establishes

This study makes a proposed additional variable concrete: a canonical scalar field with a specified gauge-kinetic interaction, its own equation and its own energy. Two distinct reduced models were derived and simulated. In the finite quantum-mode model, scalar exchange closes the exact energy balance. In the classical Einstein-Maxwell-scalar model, action-derived directional stress preserves the gravitational constraint. These are useful mathematical and computational results under declared assumptions. Their novelty in the literature has not been established.

The full Einstein-QED theory has not been completed. The two models do not yet share a quantum state, current, directional pressures or covariant subtraction. Adding a variable that keeps a separated coefficient positive does not by itself establish those missing quantities. The project therefore records a successful finite closure and a successful classical-gravity closure alongside an explicit unfinished interface.

The advisor and skeptic supplied independently derived equations. Both implementation drafts were then audited and corrected by the root after the delegated agents reached a usage limit. The source files, original drafts, raw histories and validation records are retained. This report provides derivations, assumptions, evidence and decisions rather than a claim to reproduce private internal reasoning.

## 1. Resolve the ambiguity in the Landau cutoff

N labels retained Landau levels. K bounds canonical longitudinal momentum. nK resolves an integral at fixed N,K. None is automatically a physical renormalization scale. A continuous interpolation of an analytic digamma expression does not create fractional Landau states or a new degree of freedom. The scalar mass ratio nu in the finite solver is also distinct from the interpolation symbol used in the variable inventory.

For one Dirac species, the high-energy one-loop QED equation is `mu_RG de/dmu_RG = e³/(12 pi²) + O(e⁵)`. Integrating the displayed term yields `1/e²(mu_RG)=1/e²(mu0)-log(mu_RG/mu0)/(6 pi²)`. Its formal pole is an extrapolation beyond perturbative control. It is not identified here with loss of positivity of the finite-mode divided coefficient. See the exact-RG and charge-renormalization sources in the reference ledger.

The finite coefficient is `Z=1+chi-e²C`. The previously proved continuous-integral maximum at a=0 gives a constructive possibility: set `chi_NK=z_ref-1+e²C_NK(0)`, constant in time for each run. Then `Z_NK(a)=z_ref+e²[C_NK(0)-C_NK(a)] >= z_ref > 0`. This is valid algebra and changes the fixed-chi premise. It does not prove that this is an allowed universal physical counterterm or that the combined current and stress converge.

Conversely, for bounded potential and a uniformly bounded replacement coefficient h, the shifted window contains the centered window K-A. Its positive coefficient diverges along cofinal N,K. Therefore `Z=h-e²C` cannot retain a uniform positive gap. A scalar confined to a common compact interval with a continuous f is bounded and cannot evade this result. A regulator-dependent divergent scalar, singular f or running charge changes the assumptions and creates new physical matching obligations.

The exact integral and arbitrary quadrature must remain distinct. An independent two-node Gauss counterexample produces a larger coefficient near a retained node than at the origin. The reference-at-zero inequality does not transfer to that discretization without a separate bound.

## 2. Introduce a variable with a specified action

The organizing covariant action is Einstein gravity plus a canonical scalar, potential and gauge kinetic term: `S = integral sqrt(-g) [Mpl²(R-2 Lambda)/2 - (grad Phi)²/2 - V(Phi) - f(Phi) F²/4]`. A genuine quantum extension also needs one causal state-dependent in-in functional and consistent effective-action terms. Simply writing that functional as a symbol is not computing it.

Scalar-dependent electromagnetic couplings are an established theory class, with precedents in Bekenstein, dilaton gravity and anisotropic inflation. We use them as explicit model hypotheses, not evidence that an undiscovered scalar is required by QED. The inflation reference writes the entire kinetic multiplier as a squared function; our f is already the entire multiplier. This convention matters for factors of two.

Prescribing chi(t) is a different operation. Inserting it into the old Maxwell equation gives a positive half chi-prime work defect; varying an explicitly time-dependent kinetic action instead adds a Maxwell term and gives the opposite sector-work sign. Neither gives a closed unsupported energy budget. A dynamical scalar supplies an equation and the compensating sector energy.

## 3. Finite quantum-mode scalar model: exact formulation

Use s=mt, a=e Az/m, x=e Ez/m², b=|eB|/m² and phi=e Phi/m. At fixed positive masses M_i, weights w_i and canonical nodes k_i, define p_i=k_i-a, h_i=(M_i,0,p_i), omega_i=sqrt(M_i²+p_i²). Bloch vectors retain their complete coherent evolution. S, C, D and U are the finite sums defined in Appendix A; they must not be replaced by an instantaneous particle-number ansatz.

Choose `f=1+g² phi²`, `V=nu² phi²/2`, `Z=f+chi_b-e²C`. The equations are `a′=-x`, `r_i′=2 h_i cross r_i`, `phi′=y`, `y′=-nu² phi+f_phi(x²-b²)/2`, and `Z x′=F-e²(S+D x²)-f_phi y x`. The magnetic field is fixed in this reduction, but its scalar-dependent energy cannot be discarded.

The finite action includes the normalized spinor Berry term, subtracted mode energy, Z a′²/2, scalar kinetic and potential terms, magnetic energy f b²/2 and source term -a F. Varying it fixes all exchange signs. The complete first-order action and normalizations are given in Appendix A.

The shifted energy is `Wtilde=Z x²/2+e²U+y²/2+(nu²+g²b²)phi²/2`. Precession gives `U′=xS`; coefficient differentiation gives `Z′=f_phi y+2e²Dx`. Field and mode work equals `xF-f_phi y x²/2`; scalar plus shifted magnetic work equals the omitted half. Thus `Wtilde′=xF` exactly.

At b=10,K=20, the old exact positive-quadrature certificate gives a global gap at least 3/4 for every finite inclusive N. Since f>=1, it remains a gap for the new model. Physical Bloch norms make U nonnegative. An epsilon-regularized square-root energy estimate bounds all state variables on every finite interval. If Omega²=nu²+g²b² vanishes, g=nu=0 and the scalar is affine; it is handled separately. Smoothness and the finite-dimensional continuation criterion yield a unique global forward solution for each finite model. No regulator-removal or current-limit theorem follows.

## 4. Finite simulations and falsification

The recorded main preparation is b=10, N=1 inclusive, K=20, nK=128, g=0.1, nu=0.5, phi0=0.4 and y0=0.1. A normalized smooth compact drive has amplitude 0.15 and support 0<s<4; the run ends at s=6. A delayed probe is a separate recorded source history. DOP853 uses rtol=2e-10 and atol=2e-12, with maximum step 0.05. There are 121 output samples; all quoted maxima are sampled diagnostics, not interval enclosures.

| Test | Recorded result | Interpretation |
|---|---|---|
| Correct main energy residual | {fd['correct']['max_energy_mismatch']:.3e} | Sampled work identity in this finite run |
| Minimum sampled kinetic coefficient | {fd['correct']['min_Z']:.9f} | Numerical domain check; exact lower bound is separate |
| Wrong-model unaccounted energy | {fd['wrong']['max_energy_mismatch']:.3e} | Removing only the Maxwell exchange is distinguishable |
| Wrong-model predicted-defect residual | {fd['wrong']['max_defect_integral_residual']:.3e} | Independently integrated defect explains the failure |
| 128-to-256-node field/potential discrepancy | {fd['node_refinement_max_abs_ax']:.3e} | Quadrature refinement at fixed N,K |
| Largest independent spinor/Bloch macro discrepancy | {spinerr:.3e} | Distinct state representation and RK45 integrator |
| Historical g=0 field discrepancy | {fd['g0_baseline']['max_abs_x']:.3e} | Actual archived solver was imported and compared |

The zero-drive oscillator, zero-frequency affine scalar, zero-scalar invariant subspace and canonical gauge translation also pass. The delayed-source response is consistent across three centered perturbation sizes and has a negligible pre-source derivative. Its differences are already very small; this run does not demonstrate a truncation-dominated second-order convergence interval. A nonzero response alone was not accepted as an accuracy check.

## 5. Classical gravity model: complete directional stress

Choose the axial metric `ds²=-dt²+A²(dx²+dy²)+Cmetric² dz²` with aligned orthonormal E and B. Set tau=mu t, varphi=Phi/Mpl, h=H/mu and electromagnetic fields Ecal=E/(mu Mpl), Bcal likewise. Here mu is a fixed frequency, not a renormalization scale. Use f=exp(2c varphi), potential U=mhat² varphi²/2 and theta=2h_perp+h_parallel.

The energy and directional pressures are `rho=v²/2+U+rho_EM`, `p_perp=v²/2-U+rho_EM`, `p_parallel=v²/2-U-rho_EM`, with `rho_EM=f(Ecal²+Bcal²)/2`. Evolving Ecal, Bcal, varphi, v and both spatial Einstein equations gives the complete eight-variable system in Appendix A. Initial isotropic expansion rates satisfy the Hamiltonian constraint; anisotropic stress can subsequently make the rates different.

Define `Cg=h_perp²+2h_perp h_parallel-rho-lambda`. Independent differentiation gives `Cg′=-theta Cg-Q_total`, where Q_total is the anisotropic matter-conservation residual. The scalar and electromagnetic exchange terms cancel exactly, so a satisfied constraint propagates on the regular interval. The code does not enforce this by resetting a state variable.

The source-free flux laws eliminate Ecal and Bcal in a second integration. Its gravitational RHS is shared with the production implementation, so this is a useful consistency comparison rather than wholly independent code. The skeptic separately derived the equations and implemented another system; the root independently checked the finite model with complex spinors.

## 6. Gravity experiments and negative controls

Eight recorded cases cover mixed, pure electric, pure magnetic, constant-coupling, Minkowski, de Sitter, scalar-only and short contracting data. DOP853 and Radau integrate full, flux-reduced and deliberately incomplete equations. Two analytic fixtures are actually executed: de Sitter and a massless isotropic scalar. Additional root holdouts cover negative coupling and equal initial E,B. Equal initial fields do not imply the electromagnetic invariant remains zero when f evolves.

For the mixed case the maximum correct constraint residual is {gd['max_constraint_abs_full']:.3e}, while deleting the scalar electromagnetic force produces {gd['wrong_model_max_constraint_abs']:.3e}. The independently integrated weighted Ward defect explains that drift with residual {gd['wrong_model_max_invariant_residual']:.3e}. Across all eight cases the largest full-method discrepancy is {max(c['diagnostics']['max_full_vs_Radau_state_abs'] for c in g['cases']):.3e}. Analytic de Sitter and massless-scalar discrepancies are {g['analytic_fixtures']['de_sitter_max_abs_error']:.3e} and {g['analytic_fixtures']['massless_scalar_max_abs_error']:.3e}.

These finite-time results do not prove absence of later collapse or singularity formation. They do not contain Dirac vacuum polarization, Schwinger current or quantum pressure. The elementary scalar-gravity benchmark must not be relabeled Einstein-QED because its constraints pass.

## 7. Bidirectional linking and the exact remaining gap

The executable finite Horn graph contains a 17-rule route from the finite action/domain to global finite-model continuation and an 11-rule route to classical-gravity constraint propagation. Two four-rule routes certify the reference-subtraction lemma and bounded-addition obstruction. A hash guard binds the proof notes and code. Independent forward uniform-cost search certifies route cost; the bidirectional heuristic is h=0.

Withdrawing the Maxwell-equation certificate prevents the finite continuation route. The full semiclassical target is also underivable in the reviewed finite library. This is a useful failure: the forward results do not meet the backward obligations for common quantum stress, state, matching and evolution. It is not a proof that no mathematical solution exists elsewhere. The search checks inference replay, not the mathematical truth of its prose certificates.

The next concrete calculation is a common causal quantum current and stress in a prescribed smooth axial geometry. Derive state evolution, current, energy and both pressures together; fix allowed counterterms and one physical normalization. Independently evaluate their force Ward residual. Only then attempt self-consistent geometry and regulator limits. Reconstructing a pressure from the Ward identity being tested would make that test circular.

## 8. Relationship to the wider frontier

The variable extension supplies a tested exchange pattern for later strong-field backreaction. It does not settle the Festina Lente/WGC inequalities, near-extremal decay, Schwinger creation at electron-scale curvature, Cauchy-horizon mass inflation or quantum-corrected photon-graviton conversion. Those previously mapped problems retain distinct state, geometry and approximation obligations.

A low-energy Euler-Heisenberg benchmark is planned in its controlled overlap regime. Its leading polynomial does not apply at B much greater than the QED critical field. The full constant-field one-loop action has a broader amplitude range, but that fact does not supply the needed nonlocal in-in stress in a rapidly changing curved background. The 2026 de Sitter study and the July 2026 Einstein-Euler-Heisenberg preprint are relevant recent context in the source ledger, not empirical or mathematical verification of this project's scalar hypothesis.

## 9. Validation, use and reproducibility

The independent skeptical script passes 42 checks; the root validation passes 47. Both also pass with optimized Python, where removable assertions cannot serve as acceptance gates. These counts combine different checks and are not confidence percentages. The audit preserves thirteen classes of implementation or interpretation issues, including a skipped comparator, unexecuted fixtures and clipped diagnostics.

Use the research home for the current and historical summaries. The variables page explains each kind of freedom. The finite and gravity pages expose equations, recorded plots and wrong-model controls. The proof page shows all reviewed substeps and the underivable branches. Documents open on request. Downloadable CSVs are exact plotted histories; the archive contains source, primary-reference metadata, complete equation notes and this report.

To reproduce, follow README.md and requirements.txt. Do not edit the historical rounds to make a comparison pass. Intentionally changed physical parameters require fresh results, and intentionally changed proof premises require a newly reviewed manifest. The sources below support their stated framework or result; none is presented as a blanket certificate of this project.
'''
(HERE/'research_report.md').write_text(report)
(HERE/'requirements.txt').write_text(f'numpy=={np.__version__}\nscipy=={scipy.__version__}\nsympy==1.14.0\nmatplotlib=={matplotlib.__version__}\nreportlab\npypdf\n')

# A PDF with readable equations, complete contract and a linked source ledger.
font='/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DejaVu',font+'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuBold',font+'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuMono',font+'DejaVuSansMono.ttf'))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyQ',fontName='DejaVu',fontSize=9.2,leading=14,spaceAfter=7))
styles.add(ParagraphStyle(name='TitleQ',fontName='DejaVuBold',fontSize=23,leading=29,spaceAfter=19,textColor=colors.HexColor('#15535c')))
styles.add(ParagraphStyle(name='HeadQ',fontName='DejaVuBold',fontSize=14,leading=19,spaceBefore=12,spaceAfter=9,keepWithNext=True))
styles.add(ParagraphStyle(name='SubQ',fontName='DejaVuBold',fontSize=11,leading=16,spaceBefore=9,spaceAfter=6,keepWithNext=True))
styles.add(ParagraphStyle(name='CellQ',fontName='DejaVu',fontSize=8,leading=11))
styles.add(ParagraphStyle(name='CodeQ',fontName='DejaVuMono',fontSize=8,leading=11,spaceAfter=8,backColor=colors.HexColor('#eff4f4'),borderPadding=6))

def fmt(s):
    s=s.replace('–','-').replace('—','-').replace('‑','-')
    s=html.escape(s)
    s=re.sub(r'\[([^]]+)\]\((https://[^)]+)\)',lambda m:f'<a color="#155d6e" href="{m[2]}">{m[1]}</a>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="DejaVuMono">\1</font>',s)
    s=re.sub(r'\*\*([^*]+)\*\*',r'<font name="DejaVuBold">\1</font>',s)
    return s

story=[]
def para(s,style='BodyQ'): return Paragraph(fmt(s),styles[style])
def markdown(md):
    lines=md.splitlines(); i=0; code=False
    while i<len(lines):
        line=lines[i].strip();i+=1
        if not line: continue
        if line.startswith('```'):
            code=not code;continue
        if code:
            for chunk in textwrap.wrap(line,92,replace_whitespace=False) or [' ']:story.append(para(chunk,'CodeQ'))
        elif line.startswith('|'):
            rows=[line]
            while i<len(lines) and lines[i].strip().startswith('|'):
                rows.append(lines[i].strip());i+=1
            parsed=[[c.strip() for c in r.strip('|').split('|')] for r in rows if not re.fullmatch(r'[| :\-]+',r)]
            n=max(map(len,parsed));width=479/n
            tt=LongTable([[para(c,'CellQ') for c in r] for r in parsed],colWidths=[width]*n,repeatRows=1,hAlign='LEFT')
            tt.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e0eded')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('LINEBELOW',(0,0),(-1,-1),.25,colors.HexColor('#cadada'))]))
            story.extend([tt,Spacer(1,10)])
        elif line.startswith('# '):story.append(para(line[2:],'TitleQ'))
        elif line.startswith('## '):story.append(para(line[3:],'HeadQ'))
        elif line.startswith('### '):story.append(para(line[4:],'SubQ'))
        elif line.startswith('- '):story.append(para('• '+line[2:]))
        else:story.append(para(line))

markdown(report)
story.append(para('Recorded simulations','TitleQ'))
for key,p in plots.items():
    story.append(Image(str(OUT/f'{key}.png'),width=479,height=239.5))
    story.append(para(p['caption']))
    if key!='gravity':story.append(PageBreak())
story.append(PageBreak());story.append(para('Appendix A - full action and equation contract','TitleQ'))
markdown((HERE/'variable_contract.md').read_text().split('\n',1)[1])
story.append(para('Appendix B - advisor decisions and next experiments','TitleQ'))
markdown((HERE/'advisor_plan.md').read_text().split('\n',1)[1])
story.append(para('Appendix C - primary references and reading scope','TitleQ'))
for j,s in enumerate(sources,1):
    story.append(para(f'{j}. {s["title"]}','SubQ'))
    story.append(para(f'[{s["url"]}]({s["url"]})'))
    for key in ['authors','year','date','version','inspection','inspected_sections','relevance','scope_limit','supports','use','reading_scope','read_scope','readdepth','limitation','limitations','limits','access','status']:
        if s.get(key):story.append(para(key.replace('_',' ').capitalize()+': '+str(s[key])))

def decorate(canvas,doc):
    canvas.saveState();canvas.setFont('DejaVu',8);canvas.setFillColor(colors.HexColor('#566772'))
    canvas.drawString(58,25,'Physics Observatory • Round 7 • 9 September 2026')
    canvas.drawRightString(537,25,str(doc.page));canvas.restoreState()
pdf=OUT/'einstein-qed-variable-study.pdf'
SimpleDocTemplate(str(pdf),pagesize=(595,842),leftMargin=58,rightMargin=58,topMargin=48,bottomMargin=45,title='Einstein-QED: variable and closure study',author='Physics Observatory research project').build(story,onFirstPage=decorate,onLaterPages=decorate)
shutil.copy2(pdf,SITE/pdf.name)
print(json.dumps({'report':str(pdf),'primary_sources':len(sources),'figures':len(plots),'proof_routes':len(routes)}))
