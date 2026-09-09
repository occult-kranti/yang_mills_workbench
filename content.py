from pathlib import Path
import json
ROOT=Path(__file__).parent
resources=[]
def R(id,title,publisher,url,type,use,date='Living resource; checked 2026-09-07',access='Free public material',note=''):
    resources.append(dict(id=id,title=title,publisher=publisher,url=url,type=type,use=use,date=date,access=access,note=note))
R('math','OpenStax mathematics collection','OpenStax / Rice','https://openstax.org/k12/math','Book','Arithmetic, algebra, precalculus, calculus, and statistics with worked examples.','Editions vary','Open textbooks')
R('up1','University Physics · Volume 1','OpenStax / Rice','https://openstax.org/details/books/university-physics-volume-1','Book','Core mechanics, oscillations, waves, and fluids; solve problems alongside reading.','2016; online edition','Open textbook')
R('up2','University Physics · Volume 2','OpenStax / Rice','https://openstax.org/details/books/university-physics-volume-2','Book','Thermodynamics, electricity, magnetism, circuits, and electromagnetic waves.','2016; online edition','Open textbook')
R('up3','University Physics · Volume 3','OpenStax / Rice','https://openstax.org/details/books/university-physics-volume-3','Book','Optics, relativity, quantum, atomic, nuclear, and particle foundations.','2016; online edition','Open textbook')
R('feynman','The Feynman Lectures on Physics','Feynman, Leighton & Sands / Caltech','https://www.feynmanlectures.caltech.edu/','Book + recordings','Conceptual depth across mechanics, electromagnetism, matter, and quantum physics.','1963–1965; online edition','Free to read/listen online','Caltech restricts downloading/redistributing this edition; books are linked, not bundled.')
R('calculus','MIT 18.01SC · Single Variable Calculus','David Jerison / MIT','https://ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/','Course + video','Differentiation, integration, series, worked examples, and problem-solving videos.','2010','Free OpenCourseWare')
R('multivar','MIT 18.02SC · Multivariable Calculus','Denis Auroux / MIT','https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/','Course + video','Partial derivatives, multiple integrals, vector fields, flux, and integral theorems.','2010','Free OpenCourseWare')
R('linear','MIT 18.06SC · Linear Algebra','Gilbert Strang / MIT','https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/','Course + video','Vector spaces, least squares, eigenvalues, and matrix decompositions.','2011','Free OpenCourseWare')
R('ode','MIT 18.03SC · Differential Equations','MIT course team','https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/','Course + video','First/second-order equations, oscillations, transforms, systems, and stability.','2011','Free OpenCourseWare')
R('prob','Statistics 110','Joseph Blitzstein / Harvard','https://stat110.hsites.harvard.edu/','Course + video','Probability, conditioning, random variables, expectations, and problem solving.','Established course','Free course resources')
R('python','CS50P · Python','David Malan / Harvard','https://cs50.harvard.edu/python/','Course + video','Programming foundations, files, functions, tests, and reusable code.','OpenCourseWare','Free course resources')
R('missing','The Missing Semester','MIT','https://missing.csail.mit.edu/','Course + video','Shell, Git, debugging, tools, and reproducible development.','2026 edition available','Free course materials')
R('nist','CODATA 2022 fundamental constants','NIST','https://physics.nist.gov/cuu/Constants/Table/allascii.txt','Reference','Authoritative constants, units, and standard uncertainties used by the calculators.','2022 adjustment; data update 2024','Public constants table','The 2026 adjustment is not yet a replacement at this snapshot; measured and exact constants differ.')
R('mitmech','MIT 8.01SC · Classical Mechanics','MIT Physics','https://ocw.mit.edu/courses/8-01sc-classical-mechanics-fall-2016/','Course + video','A problem-based mechanics sequence from motion to rotation and gravitation.','2016','Free OpenCourseWare')
R('mitem','MIT 8.02 · Electricity and Magnetism','MIT Physics','https://ocw.mit.edu/courses/8-02-physics-ii-electricity-and-magnetism-spring-2007/','Course + video','Electric/magnetic fields, circuits, induction, and conceptual demonstrations.','2007','Free OpenCourseWare')
R('mitqm','MIT 8.04 · Quantum Physics I','MIT Physics','https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2013/','Course + video','Experimental origins, wavefunctions, operators, and Schrödinger problems.','2013','Free OpenCourseWare')
R('mitstat','MIT 8.044 · Statistical Physics I','MIT Physics','https://ocw.mit.edu/courses/8-044-statistical-physics-i-spring-2013/','Course','Probability, ensembles, thermal physics, and quantum statistics.','2013','Free OpenCourseWare')
R('mitgr','MIT 8.962 · General Relativity','Scott Hughes / MIT','https://ocw.mit.edu/courses/8-962-general-relativity-spring-2020/','Course + video','Graduate GR with geometry, field equations, applications, and experimental tests.','2020','Free OpenCourseWare')
R('mitparticle','MIT 8.701 · Nuclear and Particle Physics','MIT Physics','https://ocw.mit.edu/courses/8-701-introduction-to-nuclear-and-particle-physics-fall-2020/','Course','Nuclear and particle concepts tied to experimental methods and observables.','2020','Free OpenCourseWare')
R('mitnum','MIT 2.29 · Numerical Fluid Mechanics','MIT','https://ocw.mit.edu/courses/2-29-numerical-fluid-mechanics-spring-2015/','Course','Discretization, stability, numerical errors, solvers, and fluid applications.','2015','Free OpenCourseWare','Some supplied examples use MATLAB; use the mathematical methods with Python alternatives.')
R('tong','Physics lecture notes collection','David Tong','https://davidtong.org/teaching/','Book / notes','Open routes into dynamics, mathematical methods, quantum, matter, relativity, and field theory.','Living teaching collection','Free author notes','Use individual course prerequisites; these are not all beginner texts.')
R('tongem','Electromagnetism','David Tong','https://davidtong.org/teaching/electromagnetism/','Book / notes','Vector calculus, static fields, induction, radiation, relativity, and matter.','Living teaching notes')
R('tonggr','General Relativity','David Tong','https://davidtong.org/teaching/general-relativity/','Book / notes','Geodesics, manifolds, curvature, Einstein equations, weak gravity, and black holes.')
R('tongcosmo','Cosmology','David Tong','https://davidtong.org/teaching/cosmology/','Book / notes','Expansion, thermal history, and structure formation after the GR/thermal foundations.')
R('tongfluid','Fluid Mechanics','David Tong','https://davidtong.org/teaching/fluid-mechanics/','Book / notes','Euler/Navier–Stokes, waves, instability, and turbulence.')
R('tongqft','Quantum Field Theory','David Tong','https://davidtong.org/teaching/quantum-field-theory/','Book + video','Graduate canonical quantization, field types, interactions, and related lecture recordings.')
R('tongstatfield','Statistical Field Theory','David Tong','https://davidtong.org/teaching/statistical-field-theory/','Book / notes','Phase transitions, coarse graining, renormalization, and universality.')
R('preskill','Physics 219 · Quantum Information','John Preskill / Caltech','https://www.preskill.caltech.edu/ph219/index.html','Book / notes','Density operators, channels, entanglement, algorithms, and quantum error correction.')
R('ibmlearn','IBM Quantum Learning','IBM','https://quantum.cloud.ibm.com/learning/en','Course + video','Structured quantum-information, circuits, and computation courses.','Living courses','Free learning material','Hardware/service access is separate.')
R('plasmatext','Plasma Physics lectures','Richard Fitzpatrick / UT Austin','https://farside.ph.utexas.edu/teaching/plasma/lectures1/index.html','Book / notes','Plasma parameters, particle motion, fluid/kinetic models, waves, and MHD.')
R('phet','PhET Interactive Simulations','University of Colorado Boulder','https://phet.colorado.edu/','Simulation','Use existing simulations for forces, fields, waves, circuits, quantum concepts, and measurement.','Living collection','Free educational simulations','External simulations remain their own applications; check individual licensing for redistribution.')
R('scipy','SciPy solve_ivp','SciPy community','https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html','Open-source tool','Reuse tested ODE integrators with tolerances, events, dense output, and solver diagnostics.')
R('sympy','SymPy','SymPy community','https://www.sympy.org/en/index.html','Open-source tool','Symbolic derivatives, integrals, matrices, and equation checking; retain assumptions and domains.')
R('qutip','QuTiP','QuTiP community','https://qutip.org/','Open-source tool','Quantum states, driven systems, master equations, and open-system simulations.')
R('qiskit','Qiskit guides','IBM / Qiskit','https://quantum.cloud.ibm.com/docs/en/guides','Open-source tool','Circuit construction, compilation, simulation, and optional hardware workflows.')
R('kwant','Kwant','Kwant project','https://kwant-project.org/','Open-source tool','Tight-binding transport, bands, scattering matrices, and boundary effects.')
R('qe','Quantum ESPRESSO','Quantum ESPRESSO Foundation','https://www.quantum-espresso.org/','Open-source tool','Electronic structure with plane waves and pseudopotentials; study convergence before interpreting bands.')
R('openmc','OpenMC','OpenMC community','https://docs.openmc.org/en/stable/','Open-source tool','Monte Carlo neutron/photon transport, tallies, and statistical uncertainty.','Living documentation','Open-source software','Requires suitable nuclear cross-section data; use educational shielding/transport cases.')
R('lammps','LAMMPS','LAMMPS community','https://www.lammps.org/','Open-source tool','Classical molecular dynamics, interatomic potentials, ensembles, and materials/soft-matter statistics.')
R('scikithep','Scikit-HEP','Scikit-HEP community','https://scikit-hep.org/','Open-source tool','Columnar particle data, histograms, fitting, and interoperable HEP analysis.')
R('cern','CERN Open Data','CERN and experiment collaborations','https://opendata.cern.ch/','Open data','Public particle-physics datasets and reproducible analysis examples.','Living portal','Open datasets; item-specific terms')
R('et','Einstein Toolkit tutorial','Einstein Toolkit community','https://einsteintoolkit.org/documentation/new-user-tutorial.html','Open-source tool','Numerical-relativity infrastructure, parameter files, tutorial runs, and convergence studies.','Living documentation','Open-source software','Full numerical-relativity projects can require substantial compute.')
R('gwosc','Gravitational Wave Open Science Center tutorials','GWOSC / gravitational-wave collaborations','https://gwosc.org/tutorials/','Open data + notebooks','Detector noise, spectra, strain data, signal extraction, and scientific-figure notebooks.')
R('rebound','REBOUND','Hanno Rein and contributors','https://rebound.hanno-rein.de/','Open-source tool','Established N-body integrators for orbit and few-body studies with conservation diagnostics.')
R('astropy','Learn Astropy','Astropy community','https://learn.astropy.org/','Open-source tool','Astronomical units, coordinates, tables, FITS data, and cosmology workflows.')
R('meep','Meep','Meep community','https://meep.readthedocs.io/','Open-source tool','FDTD electromagnetics and photonics with Python interfaces; test resolution and absorbing boundaries.')
R('fenics','FEniCS documentation','FEniCS project','https://fenicsproject.org/documentation/','Open-source tool','Finite-element methods and FEniCSx/DOLFINx for PDE applications.','Living documentation','Open-source software','Use current FEniCSx examples; legacy FEniCS APIs differ.')
R('fipy','FiPy','NIST','https://www.ctcms.nist.gov/fipy/','Open-source tool','Finite-volume diffusion, advection, and phase-field PDEs in Python.')
R('plasmapy','PlasmaPy','PlasmaPy community','https://www.plasmapy.org/','Open-source tool','Reuse particle data, units, and plasma calculation workflows.')
R('arxivapi','arXiv API manual','arXiv','https://info.arxiv.org/help/api/user-manual.html','Reference','Metadata query, category selection, submission/update dates, journal references, and version identifiers.','Living documentation','Free public API','Discovery metadata is not independent peer-review verification or exhaustive coverage.')
R('newton','The Newton Project','University of Oxford / Newton Project','https://www.newtonproject.ox.ac.uk/','Historical archive','Scientific, mathematical, religious, alchemical, administrative, and correspondence editions.','Ongoing edition of historical works','Free transcriptions','A comprehensive editorial mission does not mean every surviving document is already online.')
R('principia','Annotated first-edition Principia','Isaac Newton / Cambridge University Library','https://cudl.lib.cam.ac.uk/view/PR-ADV-B-00039-00001/9','Primary work','Definitions, laws, geometric dynamics, and Newton’s marginal revisions.','1687; later annotations','Public catalogue/facsimile','Direct retrieval returned 403 during research; indexed university record was verified.')
R('opticks','Opticks · Book I Part I','Isaac Newton / Newton Project','https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00033','Primary work','Begin with the optical experiments and follow linked continuations through the work.','1704','Free scholarly transcription','This linked section is not the entire book.')
R('waste','Newton’s Waste Book','Cambridge University Library','https://cudl.lib.cam.ac.uk/view/MS-ADD-04004/2','Primary work','Early mathematics, fluxions, series, and mechanics as developing notebook work.','Principally 1660s','Public catalogue/facsimile','Direct access restricted in research; pair with Newton Project editorial navigation.')
R('chymistry','The Chymistry of Isaac Newton','Indiana University','https://webapp1.dlib.indiana.edu/newton/','Historical archive','Study historical laboratory notes, terminology, copying practices, and alchemical interpretation.','Ongoing scholarly edition','Free reading; reuse restrictions','Historical alchemy is not modern physics; do not reproduce hazardous recipes.')
R('newtonnli','Newton manuscripts','National Library of Israel','https://www.nli.org.il/en/discover/humanities/newton-manuscripts','Historical archive','Religious, chronological, and related manuscripts with institutional context.','Historical collection','Public collection gateway','Direct retrieval failed during checking; availability of each item must be checked.')
R('einstein','Einstein Papers Project','Caltech','https://www.einstein.caltech.edu/','Historical archive','Current edition information, published volumes, and custodial archive gateways.','Ongoing edition','Free descriptions/catalogue links','Published edition and digitized corpus remain incomplete.')
R('einportal','Einstein Portal / current publisher landing page','Princeton University Press / publishing partners','https://einsteinpapers.press.princeton.edu/einstein-database/','Historical archive','Check current digital-edition access arrangements and stated coverage.','Landing page checked 7 Sep 2026','Access arrangements; announced September 30 launch','Advertised initial 16 volumes through 1930; not a verified currently free complete archive.')
R('eincatalog','Einstein Archives Online · temporary catalogue','Albert Einstein Archives / Hebrew University','https://ein-web.adlibhosting.com/aea/search/advanced','Historical archive','Search correspondence and archival identifiers beyond edited volumes.','Current temporary catalogue','Public search; subset digitized','Records are not all downloadable documents; custodian describes about 2,000 digitized items.')
R('ein1905','Einstein’s 1905 papers guide','Library of Congress','https://guides.loc.gov/einstein-annus-mirabilis/1905-papers','Primary-work guide','Read light quanta, Brownian motion, special relativity, and mass–energy as distinct investigations.','1905 papers; modern guide','Free guide; linked full-text access varies')
R('einlight','On a heuristic viewpoint concerning light','Albert Einstein / Annalen der Physik','https://doi.org/10.1002/andp.19053220607','Primary paper','Original light-quantum argument and photoelectric predictions.','1905','Publisher Free Access record verified')
R('einbrown','Brownian-motion paper','Albert Einstein / Annalen der Physik','https://doi.org/10.1002/andp.19053220806','Primary paper','Diffusion and molecular explanations of suspended-particle motion.','1905','Publisher Free Access record verified')
R('einsr','On the electrodynamics of moving bodies','Albert Einstein / Annalen der Physik','https://doi.org/10.1002/andp.19053221004','Primary paper','Operational simultaneity and special-relativistic transformations.','1905','Publisher Free Access record verified')
R('einmass','Does the inertia of a body depend upon its energy content?','Albert Einstein / Annalen der Physik','https://doi.org/10.1002/andp.19053231314','Primary paper','The short mass–energy argument, read alongside relativistic momentum.','1905','Bibliographic DOI; full text not verified','Direct publisher retrieval returned 403.')
R('eingr','The foundation of the general theory of relativity','Albert Einstein / Annalen der Physik','https://onlinelibrary.wiley.com/doi/10.1002/andp.19163540702','Primary paper','Technical 1916 exposition after geometry, tensors, and field equations.','1916','Publisher record; full-text access not established')
R('eincosmo','Cosmological considerations in general relativity','Albert Einstein / NASA ADS scan','https://articles.adsabs.harvard.edu/pdf/1917SPAW.......142E','Primary paper','Original static cosmological model and cosmological-term context.','1917','Open original German scan')
R('einradiation','On the quantum theory of radiation','Albert Einstein / INSPIRE','https://inspirehep.net/literature/858448','Primary-paper record','Absorption, spontaneous/stimulated emission, and equilibrium coefficients.','1917','Free metadata; full text not verified')
R('einbose','Einstein’s ideal-gas manuscript archive','Leiden University','https://www.lorentz.leidenuniv.nl/history/Einstein_archive/','Primary work','Read the Bose-gas manuscript with Bose’s antecedent contribution and modern statistics.','Manuscript 1924; publication 1925','Free manuscript photographs/context')
R('epr','Can Quantum-Mechanical Description of Physical Reality Be Considered Complete?','Einstein, Podolsky & Rosen / Physical Review','https://journals.aps.org/pr/abstract/10.1103/PhysRev.47.777','Primary paper','Study the original assumptions before Bell/CHSH and modern entanglement experiments.','1935','Publisher Free to Read')
R('ein17','Collected Papers · Volume 17','Einstein Papers Project / Caltech','https://www.einstein.caltech.edu/what-we-do/published-volumes/volume-17','Historical archive','Teleparallel unification, collaborators, criticism, and quantum-foundations correspondence.','Documents June 1929–November 1930','Free authoritative description; volume access varies')
R('einbook','Relativity: The Special and General Theory','Albert Einstein / Project Gutenberg','https://www.gutenberg.org/ebooks/5001','Primary book','Einstein’s accessible exposition before the technical original papers.','English translation 1920','Public-domain-in-USA text; check local terms')
R('tesla','Nikola Tesla Museum archive','Nikola Tesla Museum','https://tesla-museum.org/en/legacy/archive/','Historical archive','Primary archival gateway for notes, drawings, correspondence, calculations, and legal records.','Documents 1856–1943','Free descriptions; not full digitized corpus','163,911 call numbers are archival units, not inventions or guaranteed readable files.')
R('teslalectures','Tesla lecture index','Nikola Tesla Museum','https://tesla-museum.org/en/nikola-tesla-2/lectures/','Primary-work guide','Navigate dated lectures on machinery, high-frequency experiments, and teleautomatics.','Historical lecture catalogue','Free bibliography; full texts vary','Some lecture manuscripts are lost or incomplete.')
R('teslawritings','Tesla writings index','Nikola Tesla Museum','https://tesla-museum.org/en/nikola-tesla-2/writings/','Primary-work guide','Navigate publications and autobiographical/historical writings, then verify specific claims.','Historical bibliography','Free index; item access varies')
R('teslapatents','Tesla patent inventory','Nikola Tesla Museum','https://tesla-museum.org/en/nikola-tesla-2/patents/','Historical archive','Distinguish inventions, national equivalents, applications, and granted claims.','1885–1928 patent career','Free catalogue','Avoid ambiguous aggregate patent totals; use individually identified records.')
R('teslamotor','US381968A · Electro-magnetic motor','Nikola Tesla / original patent','https://patents.google.com/patent/US381968A/en','Patent','Study independently phased circuits and shifting magnetic poles.','Granted 1 May 1888','Free original specification and scan')
R('teslatransformer','US593138A · Electrical transformer','Nikola Tesla / original patent','https://patents.google.com/patent/US593138A/en','Patent','Study winding arrangements, high potentials, and resonant/distributed behavior.','Granted 2 November 1897','Free original specification','Patent claims do not establish safe construction or universal performance.')
R('teslacontrol','US613809A · Control of moving vessels','Nikola Tesla / original patent','https://patents.google.com/patent/US613809A/en','Patent','Read receiver, command, switching, and actuator structure as teleoperation.','Granted 8 November 1898','Free original specification')
R('teslapower','US645576A · Transmission of electrical energy','Nikola Tesla / original patent','https://patents.google.com/patent/US645576A/en','Patent','Analyze proposed transmission through natural media using coupling and energy budgets.','Granted 20 March 1900','Free original specification','A proposed worldwide system is not a demonstrated global electricity network.')
R('teslaturbine','US1061206A · Turbine','Nikola Tesla / original patent','https://patents.google.com/patent/US1061206A/en','Patent','Study disk/fluid interaction, angular-momentum transfer, and operating conditions.','Granted 6 May 1913','Free original specification')
R('tesla1892','Experiments with Alternate Currents of High Potential and High Frequency','Nikola Tesla / Project Gutenberg','https://www.gutenberg.org/ebooks/13476','Primary lecture','Read a preserved lecture alongside modern circuit/radiation theory.','1892','Public-domain-in-USA text; check local terms','One preserved lecture, not complete works; simulation-first study.')
R('wardenclyffe','Wardenclyffe tower history','Tesla Science Center','https://teslasciencecenter.org/history/tower/','Historical reference','Site-custodian context for Tesla’s wireless ambitions and the unfinished system.')

DOMAIN_ROWS=[('math','Mathematical language','Arithmetic to geometry, probability, and computation','#516ad9'),('mechanics','Classical mechanics','Motion, conservation, dynamics, and continua','#af7130'),('em','Electricity & magnetism','Fields, circuits, Maxwell theory, and electromagnetic design','#b36630'),('thermal','Waves, light & thermal physics','Optics, heat, ensembles, and collective behavior','#997532'),('quantum','Quantum physics & information','Amplitudes, atoms, entanglement, and quantum computation','#7351c5'),('gravity','Relativity, gravity & cosmology','Spacetime, curved geometry, gravitational waves, and expansion','#396f99'),('frontier','Matter, particles & interdisciplinary physics','Materials, fields, nuclei, plasma, astronomy, and living systems','#378274'),('history','Newton, Einstein & Tesla','Primary works, contributions, and intellectual context','#a16673'),('research','Research practice','Reading, reproducing, testing, and developing a research question','#526f7e')]
domains=[dict(id=i,name=n,description=d,color=c) for i,n,d,c in DOMAIN_ROWS]
chapters=[]
def C(n,title,domain,pre,refs,seq,derive,exercise,gate,misconception,tools='',hours=None):
    level='Foundation' if n<=24 else 'Intermediate' if n<=66 else 'Advanced' if n<=96 else 'Source study' if n<=104 else 'Research'
    base=[18,30] if level=='Foundation' else [25,45] if level=='Intermediate' else [35,60] if level=='Advanced' else [25,45]
    lessons=[]
    for row in seq.split('|'):
        head,rest=row.strip().split(':',1)
        topics,practice=rest.split('>',1)
        lessons.append(dict(title=head.strip(),topics=[x.strip() for x in topics.split(';')],practice=practice.strip()))
    assert len(lessons)==5,(n,len(lessons))
    chapters.append(dict(id=f'P{n:03}',title=title,domain=domain,level=level,hours=hours or base,prereqs=[f'P{x:03}' for x in pre],summary=gate,lessons=lessons,derive=derive,exercise=exercise,gate=gate,misconception=misconception,resources=refs.split(),tools=tools.split()))

for source in sorted((ROOT/'curriculum').glob('chapters_*.py')):
    exec(compile(source.read_text(encoding='utf-8'),str(source),'exec'))

# Required preparation is narrower than every potentially useful application.
# Introduce advanced mathematics when a physical branch actually needs it.
prerequisite_overrides={
 14:[7,13],17:[7,9,16],18:[7,12],19:[4],22:[6,21],26:[6,23,24],
 29:[16,21,24],36:[14,22,34],47:[11,27],48:[3,4],52:[4,22],
 55:[13,21,53],56:[13,54,55],60:[49,55],61:[7,13,60],
 64:[7,62],65:[7,61],68:[57,61,65],69:[13,61,65],72:[61,69,70],
 74:[29,30,62,68],85:[39,57,65,68,83],88:[65,76],90:[14,65,67,76],
 91:[9,10,11,38,40,55],92:[54,55,79,90],95:[13,14,32,56,59],
 96:[14,37,49],97:[21,24,26]
}
for n,pre in prerequisite_overrides.items():
    next(c for c in chapters if c['id']==f'P{n:03}')['prereqs']=[f'P{x:03}' for x in pre]
priority=[1,2,3,4,19,5,6,20,7,10,21,22,23,24,13,14,15,8,9,26,27,48,52,53,54,55,25,11,28,16,29,30,31,32]+list(range(33,47))+[47,49,50,51]+list(range(56,109))+[12,17,18]
lookup={c['id']:c for c in chapters};ordered=[];seen=set()
def visit(cid):
    if cid in seen:return
    for p in lookup[cid]['prereqs']:visit(p)
    seen.add(cid);ordered.append(lookup[cid])
for n in priority:visit(f'P{n:03}')
chapters[:]=ordered

# Sophistication follows the subject rather than merely the chapter number.
for c in chapters:
    n=int(c['id'][1:])
    if n in (8,9,10,11,12,14,15,16): c['level']='Intermediate'; c['hours']=[25,45]
    if n in (17,18): c['level']='Advanced'; c['hours']=[35,60]
tool_links={20:'kinematics projectile',21:'kinematics',22:'oscillator gravity',26:'gravity orbit',27:'oscillator',33:'coulomb',34:'coulomb',36:'capacitor',37:'circuit rc',38:'wire_field lorentz',40:'induction',41:'rc rlc',45:'transformer',48:'lens',49:'diffraction',53:'ideal_gas',55:'ideal_gas',60:'photon de_broglie',63:'quantum_well',75:'relativity',76:'relativity',79:'schwarzschild',90:'decay'}
for n,ts in tool_links.items():
    c=next(c for c in chapters if c['id']==f'P{n:03}')
    c['tools']=list(dict.fromkeys(c['tools']+ts.split()))
for file in ('research_catalogue.py','learning_program.py','specialisms.py','patent_archive.py'):
    exec(compile((ROOT/file).read_text(encoding='utf-8'),str(ROOT/file),'exec'))

PHYSICS=dict(date='2026-09-07',chapters=chapters,domains=domains,paths=paths,resources=resources,papers=papers,feeds=feeds,pioneers=pioneers,projects=projects,advisor=advisor,specialisms=specialisms,patents=patents)

def validate():
    assert len(chapters)==108 and len({c['id'] for c in chapters})==108
    ids={c['id'] for c in chapters}; refs={r['id'] for r in resources}
    position={c['id']:i for i,c in enumerate(chapters)}
    assert len(refs)==len(resources)
    for c in chapters:
        assert c['domain'] in {d['id'] for d in domains},c['id']
        assert len(c['lessons'])==5 and all(len(l['topics'])>=3 for l in c['lessons']),c['id']
        assert set(c['prereqs']) <= ids and all(p<c['id'] for p in c['prereqs']),c['id']
        assert all(position[p]<position[c['id']] for p in c['prereqs']),c['id']
        assert set(c['resources'])<=refs,c['id']
        assert all(c[x] for x in ('derive','exercise','gate','misconception')),c['id']
    for p in paths:
        pids=set(p['chapters']);assert pids<=ids
        assert all(set(c['prereqs'])<=pids for c in chapters if c['id'] in pids),p['id']
    for p in papers: assert set(p['prereqs'])<=ids,p['id']
    for p in projects: assert set(p['chapters'])<=ids and set(p['resources'])<=refs,p['id']
    for p in pioneers:
        assert set(p['chapters'])<=ids
        for c in p['contributions']: assert set(c['resources'])<=refs
    subjects={s['id'] for s in specialisms}; moduleids=set(); categories={f['category'] for f in feeds}
    assert len(subjects)==7 and len(categories)==len(feeds)
    for s in specialisms:
        assert set(s['prereqs'])<=ids and set(s['related'])<=subjects,s['id']
        assert set(s['frontier']['categories'])<=categories,s['id']
        assert len(s['modules'])==6 and len(s['projects'])==2,s['id']
        for r in s['reading']: assert r['resource'] in refs,s['id']
        for m in s['modules']:
            assert m['id'] not in moduleids,m['id']
            moduleids.add(m['id'])
            assert len(m['lessons'])==3 and all(len(l['topics'])==3 and l['practice'] for l in m['lessons']),m['id']
            assert m['gate'] and m['idea'] and set(m['resources'])<=refs,m['id']
        for p in s['projects']+s['claims']: assert set(p['resources'])<=refs,s['id']
    inventory=patents['inventory']; cases=patents['cases']; records=patents['newton']['records']
    assert len(inventory)==311 and len({r['id'] for r in inventory})==311
    assert len({(r['country'],r['number']) for r in inventory})==311
    assert len({r['country'] for r in inventory})==27
    for section,count in [('US',112),('Foreign',199)]:
        assert [r['serial'] for r in inventory if r['section']==section]==list(range(1,count+1))
    assert len(cases)==28 and len(records)==12
    caseids={c['id'] for c in cases+records}; assert len(caseids)==40
    for c in cases+records:
        assert set(c['chapters'])<=ids and set(c['resources'])<=refs,c['id']
        assert c['url'].startswith('https://'),c['id']
    assert len(patents['modules'])==10 and len(patents['projects'])==6
    for m in patents['modules']:
        assert len(m['lessons'])==3 and all(len(l['topics'])==3 and l['practice'] for l in m['lessons']),m['id']
        assert set(m['prereqs'])<=ids and set(m['resources'])<=refs and set(m['cases'])<=caseids,m['id']
    for p in patents['projects']:
        assert len(p['steps'])==4 and set(p['resources'])<=refs and set(p['chapters'])<=ids and set(p['cases'])<=caseids,p['id']
    for g in patents['glossary']:assert set(g['resources'])<=refs,g['term']
    return dict(chapters=len(chapters),subchapters=sum(len(c['lessons']) for c in chapters),topics=sum(len(l['topics']) for c in chapters for l in c['lessons']),resources=len(resources),paths=len(paths),projects=len(projects),papers=len(papers),feeds=len(feeds),subject_pages=len(specialisms),subject_modules=len(moduleids),subject_lessons=sum(len(m['lessons']) for s in specialisms for m in s['modules']),subject_projects=sum(len(s['projects']) for s in specialisms),patent_catalogue=len(inventory),patent_dossiers=len(cases),newton_documents=len(records),patent_modules=len(patents['modules']),patent_lessons=sum(len(m['lessons']) for m in patents['modules']),patent_projects=len(patents['projects']))

if __name__=='__main__':
    counts=validate()
    (ROOT/'dist').mkdir(exist_ok=True)
    text=json.dumps(PHYSICS,ensure_ascii=False,separators=(',',':'))
    (ROOT/'dist/content.js').write_text('window.PHYSICS = '+text+';\n',encoding='utf-8')
    (ROOT/'dist/content.json').write_text(json.dumps(PHYSICS,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(counts,indent=2))
