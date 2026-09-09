"""Authored learning sequence and proposed projects; not completed experiments."""
patents['modules']=[]
def PM(id,title,prereqs,lessons,gate,refs,cases,tools=''):
    patents['modules'].append(dict(id=id,title=title,prereqs=prereqs.split(),lessons=[dict(title=t,topics=topics.split('|'),practice=p) for t,topics,p in lessons],gate=gate,resources=refs.split(),cases=cases.split(),tools=tools.split()))

PM('PA01','01 · Learn to read a patent and an archive record','P001 P004 P019',[
 ('Identity before interpretation','Inventor versus applicant and assignee|Priority, filing and publication dates|Applications, grants, reissues, utility models and royal instruments','Compare one Tesla grant, DE19915730A1, DE29604486U1 and a Newton Mint record in a four-row identity table.'),
 ('Trace the documentary chain','Catalogue entry versus full specification|Source edition versus original work date|Citations, equivalents and family definitions','Follow US-097 to its reissue publication. Explain why counting every foreign equivalent as a new invention inflates a census.'),
 ('Build a claim ledger','Exact claim location|Paraphrase versus interpretation|Verified, unresolved and inaccessible fields','Create a one-page dossier with source URL, document type, claim, access date and one unresolved question.')
], 'Correctly classify all four document types and distinguish publication count from invention count. No physics claim may rest only on a title or an inventor’s reputation.',
 'patent-catalogue patent-families patent-search patent-model patent-utility patent-utility-model','US512340A DE19915730A1 DE29604486U1 N11 N12')
PM('PA02','02 · Charge, voltage, capacitance and radiant energy','P001 P002 P004 P022 P033 P034 P035 P036',[
 ('Electric quantities and units','Charge in coulombs|Potential difference and work per charge|Capacitance and boundary conditions','Use the capacitor calculator to predict how changing area, separation and dielectric constant changes stored energy at fixed voltage.'),
 ('Storage and accumulation','E = ½CV²|Power integrated over time|Radiation input and conversion assumptions','For a declared hypothetical incident power, compute an ideal charging-time lower bound; add leakage and show why actual time rises.'),
 ('Read the two radiant-energy documents','Apparatus versus method claim|Radiation source versus electrical output|Historical language versus modern photoelectric models','Annotate US685957A and US685958A together. Explain the difference between high peak power and net energy produced.')
], 'Produce a dimensionally correct energy budget with radiation, charging, leakage and discharge. State which parts are a modern model rather than a replication of the patent.',
 'up2 up3 mitem','US685957A US685958A US454622A','capacitor rc photon')
PM('PA03','03 · Magnetic forces, motors and complete cycles','P021 P022 P038 P039 P040 P053 P054',[
 ('Fields and mechanical work','Magnetic force and torque|Induction and electrical loading|Conservative forces and closed paths','Draw both field and energy-flow diagrams for a driven rotating-field motor; identify how a load changes current.'),
 ('Thermomagnetic conversion','Temperature-dependent magnetization|Heat reservoirs and cooling|Return steps and cycle efficiency','Analyze Tesla’s thermomagnetic motor as a heat-driven cycle. Include the energy needed to restore its initial state.'),
 ('Permanent-magnet claims','Magnetization as a state variable|Hysteresis and dissipation|Work over the entire cycle','Create a force-versus-position model with a clearly defined cycle; compare one favorable segment with the integral over the closed path.')
], 'Explain why a torque measurement at one angle does not establish sustained net output. Account for electrical, thermal, mechanical and magnetic state changes.',
 'up2 mitem sympy','US381968A US396121A US4151431A US9871431B2','wire_field lorentz induction')
PM('PA04','04 · Resonance without confusing voltage and energy','P010 P027 P028 P036 P040 P041',[
 ('Driven damped motion','Natural and driven frequencies|Damping, quality factor and bandwidth|Transient versus steady response','Use the oscillator and RLC tools to predict the effect of doubling damping; compare amplitude and energy.'),
 ('Coupled and distributed systems','Mutual inductance|Distributed capacitance|Model bandwidth and parasitic elements','Write a two-resonator model using SciPy. Check energy conservation in the undriven lossless limit before adding a source and resistance.'),
 ('Tesla’s coils and mechanical oscillator','Bifilar winding interpretation|Pressurized-fluid drive|Field concentration and leakage','For US512340A, US514169A and US1119732A, list the driver, storage, loss and load. Identify a statement that the patent does not experimentally establish.')
], 'Show that increased resonant amplitude is compatible with energy conservation. Your numerical result must converge when solver tolerances are tightened.',
 'up1 up2 scipy','US512340A US514169A US1119732A','oscillator rlc transformer')
PM('PA05','05 · Wireless transfer, radio control and scalar claims','P009 P011 P042 P043 P044',[
 ('Signal and power paths','Command information versus actuator energy|Near-field coupling versus radiation|Ground and return paths','Draw separate information and energy diagrams for the radio-controlled vessel. Explain how a weak received signal can control a powered motor.'),
 ('Propagation models','Maxwell equations and boundary conditions|Resonators, waveguides and Earth-scale extrapolation|Scalar potential versus longitudinal modes','Compare a quasistatic coupled circuit with a propagating-wave model. State where each approximation fails.'),
 ('Compare original and later wording','Citation versus endorsement|Inventor-reported data versus independent replication|A new observable versus a renamed ordinary effect','Extract a prediction from Hively’s document and an ordinary-coupling alternative. Specify shielding, cable and receiver controls that could distinguish them.')
], 'Identify a measurable difference between competing mechanisms. Do not infer an exotic wave merely from a Tesla citation or the term scalar.',
 'tongem up2 meep plasmatext','US613809A US645576A US787412A US9306527B1 US10924868B2','transformer rlc')
PM('PA06','06 · Electrostatic thrust and momentum accounting','P014 P021 P023 P032 P034 P096',[
 ('Define the full mechanical system','Charged particles and gas momentum|Electrode and support forces|Cables, grounding and nearby surfaces','Sketch a control volume containing the apparatus, supply and air; identify momentum crossing its boundary.'),
 ('Read independent experimental reports','Air versus reduced-pressure conditions|Detection limits and null results|Matching geometry and operating regime','Compare the two NASA reports with one Brown patent. Make a matrix of matched, different and unspecified conditions.'),
 ('Design a decisive analysis','Calibration and drift|Pressure dependence and polarity controls|Ordinary-force model versus gravity modification','Create synthetic force data containing an ion-drift signal and sensor drift; compare a model that includes drift with one that ignores it.')
], 'Explain precisely what the NASA tests support and what they do not test. Report uncertainties and apparatus differences alongside any conclusion.',
 'patent-nasa-msfc patent-nasa-ion up2 scipy','GB300311A US1974483A US2949550A US3187206A')
PM('PA07','07 · Newton’s experiments, alchemy and sacred history','P003 P004 P019 P098 P104',[
 ('Separate the roles of a manuscript','Author, copyist, translator and annotator|Date, edition and shelfmark|Natural philosophy, experiment and theology','Compare the telescope account, electrical letter and Emerald Tablet manuscript. Assign a documentary role to each statement you use.'),
 ('Read historical concepts in context','Ether and active principles|Chymistry and Hermetic language|Description of belief versus endorsement','Choose one Opticks Query and one alchemical passage. Record their vocabulary and argument before offering a modern interpretation.'),
 ('Geometry, chronology and royal patents','Temple dimensions and cubit assumptions|Conditional prophetic calculations|Mint offices and royal privileges','Draw a temple plan from declared textual assumptions, then classify N10–N12 without treating a date calculation or letters patent as an invention disclosure.')
], 'Produce a source-backed comparison that neither erases Newton’s nonmodern interests nor treats them as experimental confirmation of supernatural physics.',
 'newton chymistry patent-tablet-text patent-gentile-translation newton2060','N01 N02 N03 N04 N05 N06 N07 N08 N09 N10 N11 N12')
PM('PA08','08 · Test emanations, orgone and perception claims','P013 P014 P019 P052 P096 P107',[
 ('Operational definitions','Observable with units|Mechanism versus claimed benefit|Physical measurement versus subjective report','Translate a claim from each selected document into a measurable endpoint; mark any term lacking an operational definition.'),
 ('Controls for subtle effects','Randomized coded samples|Active and sham comparisons|Temperature, contact and acoustic-level confounds','Design a blinded Hieronymus-style detection analysis using synthetic outcomes. Explain why operator knowledge can change results without a new physical force.'),
 ('Analyze before explaining','Base rates and chance accuracy|Multiple comparisons and stopping rules|Effect size, uncertainty and replication','Write a fixed analysis plan for a listening comparison or material-temperature study. Separate detecting a difference from proving its proposed cause.')
], 'Deliver a preregistered analysis plan with a null model, sample-size rationale, scoring rule and a result that would count against the claim.',
 'prob scipy patent-utility-model','US2482773A DE19915730A1 DE29604486U1 US10924868B2 US7235945B2')
PM('PA09','09 · Advanced branch: spin, vacuum and gravitational claims','P053 P065 P074 P076 P077 P078 P080 P085',[
 ('Use the right level of theory','Intrinsic spin versus classical rotation|Material magnetism and spin transport|Vacuum states versus a usable power supply','Create a vocabulary map connecting each term to an established model and an observable. Do not treat shared vocabulary as a shared mechanism.'),
 ('Distinguish inertia, gravity and thrust','Operational inertial-mass measurement|Near-field gravitational effects|Radiative gravitational-wave strain','For the Pais craft and wave-generator cases, specify separate observables for ordinary force, inertia change and far-field strain.'),
 ('Audit the strongest version of a claim','Dimensional consistency|Stated energy and momentum inputs|Independent evidence and missing parameters','Write the proposed mechanism in equations only where the document defines the quantities. List what remains underspecified and what would discriminate competing models.')
], 'State a falsifiable, quantitatively defined question while respecting the theory’s validity range. This graduate branch is optional until its linked prerequisites are secure.',
 'mitgr tongqft gwosc up2','US9871431B2 US10144532B2 US10322827B2 US10135366B2')
PM('PA10','10 · Publish a reproducible research dossier and extend the census','P015 P104 P105 P106 P107 P108',[
 ('Reproducible source research','Search strings and inclusion criteria|Saved identifiers and access dates|Family merging and name disambiguation','Extend one narrow theme in Espacenet. Record every included and excluded result with a reason instead of claiming all related inventions.'),
 ('Reproducible computation','Versioned parameters and software|Analytic limits and convergence|Data provenance and uncertainty','Package one project as a notebook with a README, environment specification, machine-readable inputs and a limitations section.'),
 ('Independent challenge review','Strongest ordinary alternative|Unmatched replication conditions|What evidence would change the conclusion','Have a reviewer argue against your favored interpretation. Revise the dossier with a response table and preserve unresolved disagreements.')
], 'Deliver a traceable research artifact another learner can reproduce. Every conclusion distinguishes historical attribution, patent assertion, model prediction and independent observation.',
 'patent-search patent-families missing scipy','US512340A US9306527B1 N11')

patents['projects']=[]
def PP(id,title,question,software,steps,gate,deliver,refs,chapters,cases):
    patents['projects'].append(dict(id=id,title=title,question=question,software=software,steps=steps,gate=gate,deliver=deliver,resources=refs.split(),chapters=chapters.split(),cases=cases.split()))
PP('PAP01','Audit and extend the Tesla catalogue','Can another researcher reconstruct your count and distinguish documents from invention families?',
   'Python standard library: csv, json, collections; museum catalogue and Espacenet.',[
   'Start with this room’s source-linked 311 rows. Check US serials 1–112, foreign serials 1–199 and jurisdiction/number duplicates.',
   'Manually inspect ten distributed rows, the reissue, both missing grant dates and the title/date correction against source pages.',
   'Choose one patent and investigate foreign equivalents using verified priority information; record family-definition uncertainty.',
   'Add one narrowly defined search extension with date, query, inclusion rule and rejected candidates. Keep unverified identifiers out of the confirmed table.'
   ],'The same rules reproduce the same counts; all corrections retain the source transcription and supporting document.',
   'CSV/JSON inventory, correction ledger, search log and a one-page coverage statement.','patent-catalogue patent-search patent-families','P015 P104','US512340A')
PP('PAP02','Resonance and energy-accounting notebook','How can a circuit develop large voltage while remaining consistent with its input energy?',
   'SciPy solve_ivp, NumPy and optional Matplotlib; existing capacitor, oscillator and RLC tools.',[
   'Begin with an analytic LC oscillator and verify the stored-energy formula in the undriven lossless limit.',
   'Add resistance and a sinusoidal driver; integrate instantaneous source power, resistor loss and change in stored energy.',
   'Extend to two coupled resonators and sweep coupling, load and frequency. Separate transient buildup from steady behavior.',
   'Relate the model to US512340A while listing omitted distributed geometry, high-frequency parasitics and nonlinear effects.'
   ],'Energy residual and observable curves converge with tighter solver tolerances; no efficiency claim uses peak voltage alone.',
   'Notebook, energy-balance plot, convergence table and a model-to-patent correspondence sheet.','scipy up2','P010 P015 P036 P040 P041','US512340A US1119732A US685958A')
PP('PAP03','Electrostatic geometry and ordinary coupling','Which field patterns follow from electrode geometry before introducing a new force?',
   'PhET for intuition; SymPy for analytic checks; optional FEniCSx for electrostatics or Meep for a separate wave model.',[
   'Solve a simple potential problem with declared boundary conditions and compare with an analytic parallel-plate limit.',
   'Change electrode curvature or asymmetry in a normalized numerical domain; check mesh convergence and boundary placement.',
   'Map electric-field energy and forces on every modeled conductor. Label any omitted gas, leakage or external support interaction.',
   'Compare the assumptions with the Tesla terminal and Brown capacitor documents. Do not infer gravity modification from an electrostatic simulation.'
   ],'Show a converged result and a full force/energy boundary; state clearly whether the model includes gas momentum.',
   'Geometry files, field maps, convergence record and a limitations table. This is a computer project, not a high-voltage construction guide.','phet sympy fenics meep','P009 P015 P035 P046','US1119732A US2949550A')
PP('PAP04','Reanalyze the logic of a NASA propulsion test','How strong a conclusion is justified when apparatus conditions differ?',
   'Original NASA reports; Python/SciPy for explicitly labeled synthetic data or clearly sourced digitized values.',[
   'Extract apparatus, medium, grounding, measurement method and stated limitations from both original reports.',
   'Build a comparison matrix with one Brown specification and identify conditions that were not matched.',
   'Use reported numerical values only where their location and units are clear; otherwise construct labeled synthetic data to explore drift and pressure dependence.',
   'Write two conclusions: one confined to the measured configuration and one proposed follow-up question. Explain why a null is bounded by sensitivity.'
   ],'Every numerical datum is traceable or labeled synthetic. A result from one setup is never advertised as testing all devices.',
   'Evidence matrix, analysis notebook and a bounded replication proposal.','patent-nasa-msfc patent-nasa-ion scipy','P014 P023 P096 P107','GB300311A US2949550A US3187206A')
PP('PAP05','Newton documentary atlas','How do authorship, edition and genre change the meaning of a striking quotation?',
   'Newton Project and Indiana Chymistry editions; a spreadsheet or Python CSV; SymPy for optional geometry.',[
   'Select one experimental, one alchemical, one theological and one administrative record from this room.',
   'Record work date, edition date, manuscript shelfmark, author/copyist role and a short claim paraphrase with an exact locator.',
   'Compare two interpretations against surrounding text. Track assumptions in a temple reconstruction or conditional chronology separately from evidence.',
   'Write a correction note for a hypothetical misattribution, preserving Newton’s documented interests without turning them into verified supernatural effects.'
   ],'A reader can recover each passage and identify whose voice it is. A royal patent is never relabeled an invention patent.',
   'Four-record mini-edition, interpretation comparison and source-linked timeline.','newton chymistry patent-tablet-text patent-gentile-translation','P003 P098 P104','N02 N06 N08 N09 N10 N11')
PP('PAP06','Blind-test design for unusual detection and sound claims','What would separate an observable effect from expectation, drift and selective reporting?',
   'Python standard library random plus SciPy statistics; optional existing wave/acoustics tools. Use synthetic data for the first analysis.',[
   'Choose a single endpoint: coded-sample identification, measured temperature difference or level-matched listening preference.',
   'Define active/sham conditions, randomization, concealment, exclusions, stopping rule and a sample-size rationale before generating data.',
   'Simulate chance, small-effect and confounded datasets. Evaluate false positives, uncertainty and how unblinding changes interpretation.',
   'Write a replication plan that distinguishes detecting a difference from establishing orgone, scalar waves or a therapeutic mechanism.'
   ],'The fixed analysis handles both null and non-null simulations and reports effect size with uncertainty; it does not infer mechanism from significance alone.',
   'Preregistered protocol, simulation notebook and a reviewer’s confound checklist.','prob scipy','P013 P014 P019 P107','US2482773A DE29604486U1 US10924868B2')

patents['glossary']=[
 dict(term='Patent publication and evidence',meaning='A public technical/legal document containing a disclosure and claims. USPTO guidance includes credible-utility examination; working models are not ordinarily required.',boundary='A grant is neither independent replication nor a guarantee of commercial performance. Check document type and avoid blanket claims about all offices or eras.',resources=['patent-model','patent-utility','patent-utility-model']),
 dict(term='Patent family and historical jurisdiction',meaning='Related publications may share priority or similar technical content. Simple and extended family definitions differ; old granting territories do not map one-to-one to modern countries.',boundary='Count publications, catalogue rows and inventions separately. A family link or citation does not make every named person a co-inventor.',resources=['patent-families','patent-catalogue']),
 dict(term='Radiant energy',meaning='Energy arriving through radiation; Tesla’s selected disclosures describe charge accumulation and discharge in that context.',boundary='Incoming radiation is an input. Historical terms do not by themselves establish vacuum-energy extraction or energy creation.',resources=[next(c['resources'][0] for c in patent_cases if c['id']=='US685957A'),'up3']),
 dict(term='Ether, spirit and active principles',meaning='Terms whose meanings depend on author, date, genre and argument. Newton’s hypotheses, Queries and theology must be read in their own context.',boundary='Historical vocabulary is not interchangeable with modern quantum fields, nor does its presence alone prove a supernatural assertion.',resources=['patent-N03','patent-N04','patent-N05','teslaether']),
 dict(term='Occult and Hermetic material',meaning='Historical discussions of hidden causes and Hermetic/alchemical traditions include both interpretation and criticism. Newton’s copying, translation and commentary have distinct roles.',boundary='The presence of a text in an archive does not establish its propositions experimentally or show that the copyist endorsed each one.',resources=['patent-N06','patent-tablet-text','patent-N08','chymistry']),
 dict(term='Resonance and geometry',meaning='System geometry and boundary conditions affect modes, capacitance, inductance, field concentration and coupling.',boundary='A resonant peak or geometric pattern does not establish unlimited energy, a special consciousness effect or a universal sacred frequency.',resources=['up1','up2','patent-US512340A']),
 dict(term='Scalar and longitudinal',meaning='Scalar potential and longitudinal modes in appropriate physical media are legitimate mathematical and physical concepts.',boundary='A proposed new propagating scalar-longitudinal wave requires its own equations, observables and independent evidence. Hively’s reported data are inventor-reported, not independent replication.',resources=['tongem','plasmatext','patent-US9306527B1']),
 dict(term='Orgone and massfree energy',meaning='Terms used in Reich-related and later unconventional energy claims, including several documents linked in this room.',boundary='A term in a patent is not an established energy species. Specify a measurable quantity and distinguish it from heat, charge, ordinary radiation and experimental artifacts.',resources=['patent-US7235945B2','patent-DE19915730A1','patent-DE29604486U1']),
 dict(term='Electrostatic thrust and antigravity',meaning='Electrical apparatus can exchange momentum with charged particles, gas and external structures. NASA’s cited tests investigated specified asymmetrical capacitor arrangements.',boundary='Thrust alone is not evidence of gravitational shielding. The reports’ air and vacuum findings must retain their configuration and sensitivity limits.',resources=['patent-nasa-msfc','patent-nasa-ion']),
 dict(term='Spin, zero-point energy and gravitational waves',meaning='These belong to established but distinct areas of quantum matter, field theory and gravitation.',boundary='The existence of those fields does not validate a specific generator or craft. The proposed mechanism and claimed performance require independent tests.',resources=['up3','tongqft','mitgr','gwosc']),
 dict(term='Radionics, emanations and subjective endpoints',meaning='Some unusual detection claims use an operator’s sensation or judgment as their reported signal.',boundary='Blinding, predefined scoring, calibration and chance baselines are needed. Detecting a repeatable difference would still leave its physical mechanism to be established.',resources=['patent-US2482773A','prob'])
]
