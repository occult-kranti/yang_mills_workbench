"""Source-linked patent and historical-document research; reviewed 2026-09-08.

Loaded by content.py. Descriptions are concise original paraphrases. Study tasks
are proposals, not completed replications. The catalogue preserves source rows.
"""
def PS(id,title,publisher,url,type='Patent publication',use='',date='Historical document; reviewed 2026-09-08',note=''):
    existing=next((r['id'] for r in resources if r['url']==url),None)
    if existing:return existing
    R(id,title,publisher,url,type,use,date,'Free public reading',note)
    return id

PS('patent-catalogue','Tesla patent catalogue · 112 US and 199 foreign entries','Snežana Šarboh / Nikola Tesla Museum','https://tesla-museum.org/wp-content/uploads/2023/05/lista_patenata_eng.pdf','Primary catalogue','Numbered inventory across 27 historical jurisdictions; use row-level data and correction notes.','2019 catalogue; reviewed 2026-09-08','PDF summary and overview contain discrepancies; this room preserves the 311 numbered entries.')
PS('patent-families','Patent families: simple and extended','European Patent Office','https://www.epo.org/en/searching-for-patents/helpful-resources/first-time-here/patent-families','Reference','Learn how priority links group documents; family definitions change counts.')
PS('patent-search','Espacenet search and learning gateway','European Patent Office','https://www.epo.org/en/searching-for-patents/technical/espacenet','Search + tutorials','Search names, priorities, citations, classifications and families; record search date and scope.')
PS('patent-model','Applying for patents: models and specimens','USPTO','https://www.uspto.gov/patents/basics/apply','Reference','A working model is not ordinarily required; special cases may be treated differently.')
PS('patent-utility','MPEP §2107 · Utility examination','USPTO','https://www.uspto.gov/web/offices/pac/mpep/s2107.html','Reference','Examination includes specific, substantial, credible utility. A grant remains distinct from independent experimental validation.')
PS('patent-utility-model','Utility models','WIPO','https://www.wipo.int/en/web/patents/topics/utility_models','Reference','Distinguish utility-model registration from invention-patent examination; procedures vary by jurisdiction.')
PS('patent-newton-register','Patents of invention: historical research guide','The National Archives, UK','https://www.nationalarchives.gov.uk/help-with-your-research/research-guides/patents-of-invention/','Archive guide','Starting point for a bounded register and index search beyond Newton manuscript catalogues.',note='Institutional indexed guide verified; full-page retrieval returned an access error in this review.')
PS('patent-nasa-msfc','NASA Marshall Space Flight Center Barrel-Shaped Asymmetrical Capacitor','Campbell, Carruth, Edwards and colleagues / NASA','https://ntrs.nasa.gov/api/citations/20040171466/downloads/20040171466.pdf','Experimental report','Compare the tested air and hard-vacuum configurations with electrostatic-thrust claims.','NASA/TM–2004–213283 · June 2004','Read the original PDF. Findings apply to the reported apparatus and measurement conditions.')
PS('patent-nasa-ion','Asymmetrical Capacitors for Propulsion','Francis X. Canning, Cory Melcher & Edwin Winet / NASA','https://ntrs.nasa.gov/api/citations/20040171929/downloads/20040171929.pdf','Experimental report','Study pressure, polarity, grounding and ion-momentum explanations.','NASA/CR–2004–213312 · October 2004','Original report inspected; its observations do not require a new physical principle.')

patent_cases=[]
def PC(id,title,owner,date,group,themes,connectionType,relation,claim,inputs,assessment,test,chapters,extra='',type='Granted patent publication'):
    url=f'https://patents.google.com/patent/{id}/en'
    rid=PS('patent-'+id,title+' · '+id,owner,url,type,'Read the specification and claims alongside the annotated dossier.',date+' publication; reviewed 2026-09-08','Publication type and date identify this document; no current enforceability assessment is supplied.')
    patent_cases.append(dict(id=id,title=title,owner=owner,date=date,type=type,group=group,themes=themes.split('|'),connectionType=connectionType,relation=relation,claim=claim,inputs=inputs,assessment=assessment,test=test,chapters=chapters.split(),resources=[rid]+extra.split(),url=url))

PC('US381968A','Electromagnetic motor','Nikola Tesla','1888-05-01','Tesla','Magnetism|Motors','Original Tesla patent','A foundation for studying Tesla’s rotating-field engineering.',
   'Alternating-current circuits progressively shift the magnetic poles of a motor.',
   'A generator supplies electrical energy; the motor converts part of it to shaft work.',
   'Rotating magnetic fields provide an ordinary electromechanical explanation. Permanent magnets or rotating poles alone do not establish a self-powered motor.',
   'Model two sinusoidal perpendicular fields. Compare their resultant for 0°, 90° and 180° phase offsets, then add winding resistance to an energy budget.','P038 P039 P040 P045 P102','mitem up2')
PC('US396121A','Thermomagnetic motor','Nikola Tesla','1889-01-15','Tesla','Magnetism|Heat|Motors','Original Tesla patent','Thermal changes in magnetic response, rather than an unexplained magnetic fuel.',
   'Heating and cooling magnetic material changes its attraction; a spring or weight helps produce reciprocation.',
   'The described arrangement uses heat and cooling, with mechanical restoring forces.',
   'The relevant questions are heat flow, material response and cycle efficiency. A moving magnet is not evidence of net work without an energy source.',
   'Draw a full heating–motion–cooling–return cycle. Identify every energy reservoir and the measurements needed to estimate efficiency.','P022 P053 P054 P039','up2')
PC('US454622A','System of electric lighting','Nikola Tesla','1891-06-23','Tesla','Electrostatics|Resonance|Radiation','Original Tesla patent','The historical specification uses ether language in a powered electrical system.',
   'A source charges a capacitor; oscillatory discharge and induction produce high-frequency lighting arrangements.',
   'Electrical generation, capacitor charging and circuit losses remain part of the system.',
   'Unusual lamp connections are a study of fields and circuit coupling. The specification does not establish supernatural energy. Catalogue row US-053 has title and filing-date transcription discrepancies.',
   'Map each source, storage element, coupling path and load in a diagram; explain why a single visible wire does not specify the complete return path.','P036 P040 P041 P042','teslaether up2')
PC('US512340A','Coil for electromagnets','Nikola Tesla','1894-01-09','Tesla','Magnetism|Resonance|Scalar claims','Original Tesla patent','Explicitly cited by the later Hively and Soniphi publications in this room.',
   'Adjacent insulated conductors connected in series alter interturn voltage and distributed capacitance.',
   'A driving circuit supplies energy; inductance, capacitance, resistance and frequency determine response.',
   'The large stored-energy comparison concerns the stated winding comparison, not measured whole-device output/input efficiency. A citation does not validate a later scalar-wave interpretation.',
   'Compare lumped and distributed circuit models. Plot resonance shift with capacitance and identify the frequency beyond which a lumped approximation breaks down.','P036 P040 P041 P044','up2 tongem')
PC('US514169A','Reciprocating engine','Nikola Tesla','1894-02-06','Tesla','Resonance|Sound|Mechanics','Original Tesla patent','A useful document for investigating later “earthquake machine” interpretations.',
   'A steam- or gas-driven piston works against an elastic restoring force, including an air spring.',
   'Pressurized working fluid supplies energy; damping, load and spring nonlinearity affect motion.',
   'Approximate constancy of period has a limited operating range. This patent does not demonstrate city-scale destruction by resonance.',
   'Use the oscillator tool, then simulate damping and a cubic spring correction. Compare frequency and amplitude as drive and load change.','P027 P028 P047','scipy up1')
PC('US613809A','Control of moving vessels or vehicles','Nikola Tesla','1898-11-08','Tesla','Radio control|Information','Original Tesla patent','Remote command offers a concrete comparison with claims of action at a distance.',
   'A transmitter and receiver operate mechanisms that steer or otherwise control a vessel or vehicle.',
   'The command signal and local propulsion/control power are distinct parts of the apparatus.',
   'A receiver can turn a weak command into a powered action without the command carrying all the mechanical energy. Telepathy is not needed by the disclosed mechanism.',
   'Draw separate information-flow and power-flow diagrams. Plan a software-only controller with message loss, delay and an explicit safe state.','P037 P042 P044 P103','up2')
PC('US645576A','System of transmission of electrical energy','Nikola Tesla','1900-03-20','Tesla','Wireless power|Earth|Resonance','Original Tesla patent','Later energy-conversion writers invoke Tesla; their attribution is separate from his original disclosure.',
   'A generating station, ground connection and elevated terminals are proposed to transmit energy through natural media to tuned receivers.',
   'The transmitter is powered. Coupling, leakage, conductor losses and receiver loading determine delivered energy.',
   'Wireless transfer is not energy creation. Patent publication alone does not validate global-range or commercial-efficiency extrapolations.',
   'Start with two coupled resonators. Sweep distance through a chosen coupling model and show where that model cannot represent an Earth-scale proposal.','P040 P041 P042 P044 P103','up2 meep')
PC('US685957A','Apparatus for utilization of radiant energy','Nikola Tesla','1901-11-05','Tesla','Electrostatics|Radiant energy','Original Tesla patent','Read before assessing claims that Tesla patented an inputless energy source.',
   'Incident radiation acts on an insulated conductor connected to a capacitor, with another terminal grounded or connected to another source; accumulated charge is discharged.',
   'Incoming radiation, and any apparatus producing it, belong in the energy budget.',
   'Radiation harvesting and charge accumulation do not establish energy creation. Historical terminology should be compared with modern photoelectric and circuit models carefully.',
   'Choose a hypothetical incident power and conversion fraction. Calculate charging time and stored energy, and label every assumption rather than claiming a replication.','P036 P037 P060','up2 up3')
PC('US685958A','Method of utilizing radiant energy','Nikola Tesla','1901-11-05','Tesla','Electrostatics|Radiant energy','Original Tesla patent','Companion method document to US685957A; a separate publication need not be a separate invention family.',
   'Radiation-driven charge accumulation and controlled discharge form a method of obtaining an electrical effect.',
   'Sunlight or an excited radiation source supplies energy; excited sources themselves require power.',
   'A brief discharge can have high peak power after slow accumulation. Peak power and total energy answer different questions.',
   'Use E = ½CV² with an assumed input power. Compare a one-second discharge with a one-hour charging interval and include losses.','P004 P022 P036 P060','up2 up3')
PC('US787412A','Transmission through the natural mediums','Nikola Tesla','1905-04-18','Tesla','Wireless power|Earth|Resonance','Original Tesla patent','Earth-wave language is a starting point for a mechanism audit, not an automatic link to ley lines.',
   'A grounded resonant circuit is proposed to excite stationary electrical waves in the Earth, with reception at selected locations.',
   'An energized transmitter and a propagation medium are required; losses and boundary conditions matter.',
   'The proposal must not be equated with Schumann resonances, spiritual frequencies or arbitrary Earth-grid diagrams without a matching physical model and measurements.',
   'Compare boundary conditions for a transmission line and a spherical cavity. List which observations would distinguish the two models.','P011 P042 P044 P103','tongem meep')
PC('US1119732A','Apparatus for transmitting electrical energy','Nikola Tesla','1914-12-01','Tesla','Wireless power|Resonance|Electrostatics','Original Tesla patent','A resonant-transmitter design with attention to surface curvature and leakage.',
   'The apparatus combines resonant electrical elements and elevated conducting surfaces arranged to reduce unwanted discharge.',
   'An alternator or capacitor-driven primary circuit supplies energy.',
   'High local voltage can coexist with limited total energy. Terminal shape concerns electric-field concentration and losses, not proof of an unlimited source.',
   'Use a normalized electrostatic model to compare curvature and field concentration. State the idealized boundaries and omit apparatus construction.','P035 P036 P041 P046','fenics up2')
PC('US1655114A','Apparatus for aerial transportation','Nikola Tesla','1928-01-03','Tesla','Flight|Motors','Original Tesla patent','A primary-source check for claims that Tesla’s aircraft patents describe antigravity craft.',
   'A powered aircraft arrangement combines an airscrew with mechanisms for changing its orientation and flight operation.',
   'A prime mover drives the airscrew; interaction with air provides aerodynamic thrust.',
   'The disclosed mechanism is not gravitational shielding. Its existence does not establish a later flying-saucer interpretation.',
   'Draw the forces during vertical and horizontal operation. Identify the power, stability and transition questions the patent does not settle experimentally.','P021 P023 P032','up1')

PC('GB300311A','Producing force or motion','Thomas Townsend Brown','1928-11-15','Related','Electrostatics|Gravity claims','Thematic comparison','Related through electric-field and gravity claims; not a Tesla or Newton patent.',
   'The specification asserts that charged, rigidly connected bodies can experience an unbalanced gravitational force.',
   'Electrical charging and the environment must be included in the system boundary.',
   'This is an extraordinary assertion in the text. Its publication is not an independent measurement of modified gravity; later capacitor experiments provide a bounded comparison.',
   'Extract one force prediction and preregister polarity, orientation, pressure and sham controls; account for forces on cables and surrounding conductors.','P014 P019 P023 P033 P096','patent-nasa-msfc patent-nasa-ion')
PC('US1974483A','Electrostatic motor','Thomas Townsend Brown','1934-09-25','Related','Electrostatics|Motors|Ion motion','Thematic comparison','Brown’s motor document describes more specific interactions than a generic antigravity label.',
   'Charged dielectric members interact with neighboring electrodes; another arrangement charges a surrounding fluid to produce reaction forces.',
   'The text explicitly maintains connection to an external electrical source during operation.',
   'Identify each proposed interaction before interpreting motion. Powered electrostatic forces, charged-fluid momentum and a gravity-change claim require different measurements.',
   'Annotate the specification’s solid-electrode and fluid variants separately. Draw complete force balances including the enclosure and electrical supply.','P021 P023 P033 P034','up2 patent-nasa-ion')
PC('US2949550A','Electrokinetic apparatus','Thomas Townsend Brown','1960-08-16','Related','Electrostatics|Ion motion|Gravity claims','Thematic comparison','Historical asymmetric-electrode propulsion, compared with independent NASA studies.',
   'An electric-field arrangement with asymmetric electrodes is described as producing force.',
   'The power supply, charged particles, gas and surrounding structures can exchange energy and momentum.',
   'NASA’s reported capacitor observations were consistent with charged-particle momentum transfer. Their apparatus and conditions limit what can be concluded about this patent.',
   'Make a comparison table of patent geometry versus NASA geometry, medium, grounding and measured force. Mark unmatched parameters explicitly.','P023 P032 P034 P096','patent-nasa-msfc patent-nasa-ion')
PC('US3187206A','Electrokinetic apparatus','Thomas Townsend Brown','1965-06-01','Related','Electrostatics|Vacuum|Gravity claims','Thematic comparison','The description includes environmental-field and vacuum assertions worth separating from air-thrust demonstrations.',
   'Asymmetric electrical structures are described with asserted reaction effects, including discussion of operation in vacuum.',
   'Electrical supply, remaining gas, field coupling and apparatus supports remain candidate inputs or momentum paths.',
   'NASA reported no performance in its hard-vacuum barrel-capacitor configuration. That bounded result is not a direct replication of every configuration or a universal theorem.',
   'Specify a detection limit, pressure-dependent prediction, thermal drift model and null experiment before interpreting a small force signal.','P014 P023 P034 P096','patent-nasa-msfc patent-nasa-ion')
PC('US4151431A','Permanent magnet motor','Howard R. Johnson','1979-04-24','Related','Magnetism|Energy claims|Motors','Thematic comparison','A later permanent-magnet claim, not Tesla authorship or a documented Newton connection.',
   'Magnet arrangements are asserted to provide continuous motive work through magnetic interactions associated with electron spins.',
   'A full accounting must include magnet state, mechanical resets, assembly work, load and any external drive.',
   'This review did not establish independent confirmation of continuous net energy production. A favorable part of a trajectory does not settle work over a complete repeatable cycle.',
   'Model a conservative magnetic potential. Integrate force around a closed path and explain how hysteresis, demagnetization and measurement error change the accounting.','P022 P038 P039 P085','up2 sympy')
PC('US9871431B2','Spintronic generator','Kirk Miller / Spintronics Inc.','2018-01-16','Related','Magnetism|Energy claims|Spin|Vacuum','Thematic comparison','The text invokes Searl-related background; Kirk Miller is the named inventor, not Tesla or Searl.',
   'The document proposes magnetic/resonant arrangements with claims involving natural spin, zero-point energy and cooling.',
   'Mechanical, electrical and thermal ports all require measurement across a complete operating cycle.',
   'Spintronics is an established field, but its existence does not validate this generator. Independent confirmation of the exceptional energy claims was not established in this review.',
   'Create a control-volume energy balance and an uncertainty budget that includes temperature drift, startup energy and changes in stored magnetic energy.','P014 P053 P065 P085','up2')
PC('US10144532B2','Craft using an inertial mass reduction device','Salvatore Cezar Pais / U.S. Navy assignee','2018-12-04','Related','Gravity claims|Vacuum|Resonance','Thematic comparison','A later government-assigned patent; no Tesla or Newton inventorship is implied.',
   'A charged resonant-cavity arrangement with vibration and electromagnetic excitation is proposed to modify the surrounding vacuum and reduce inertial effects.',
   'Excitation, mechanical drive, field generation and interactions with the environment must be counted.',
   'Government assignment and a grant do not certify a working craft. Independent confirmation of the claimed inertial-mass reduction was not established here.',
   'Define inertial mass operationally. Identify an observable that distinguishes it from ordinary thrust, electromagnetic forces, vibration and sensor artifacts.','P076 P077 P078 P096','mitgr')
PC('US10322827B2','High frequency gravitational wave generator','Salvatore Cezar Pais / U.S. Navy assignee','2019-06-18','Related','Gravity claims|Resonance|Sound','Thematic comparison','A proposed generator; distinct from astronomical gravitational-wave observations.',
   'Charged and vibrated cavity structures with electromagnetic excitation are proposed to generate gravitational-field fluctuations.',
   'Mechanical and electromagnetic excitation are explicit parts of the proposal.',
   'Gravitational-wave detections elsewhere do not verify this device. This review did not establish independent confirmation of its claimed performance.',
   'After the GR prerequisites, distinguish source strength, near-field effects and far-field strain. Design an inference question with an explicit background model.','P077 P078 P080','mitgr gwosc')
PC('US10135366B2','Electromagnetic field generator','Salvatore Cezar Pais / U.S. Navy assignee','2018-11-20','Related','Magnetism|Resonance|Radiation','Thematic comparison','Part of a later field-generator research trail; attribution remains with the named inventor.',
   'The specification describes driven charged structures, field generation and claimed high-energy effects; some variants discuss radioactive materials.',
   'The text includes a power plant, thermoelectric generation and motor-driven components.',
   'Explicitly trace those inputs before evaluating exceptional effects. This is a document-analysis case; no independent performance confirmation is established here.',
   'Produce a block diagram and dimensional audit of one selected claim using published quantities. Record missing measurements without designing or constructing the apparatus.','P004 P040 P042 P090 P096','up2')
PC('US7235945B2','Energy conversion systems','Paulo N. Correa & Alexandra N. Correa','2007-06-26','Related','Orgone|Energy claims|Scalar claims|Wireless power','Explicit historical attribution','The description explicitly invokes Tesla and Wilhelm Reich; this is the later authors’ attribution.',
   'The disclosure proposes conversion of what it calls massfree energy, with Tesla-wave, Reich-related and faster-than-light interpretations.',
   'Receivers, excited circuits and conversion components require a complete power and signal-timing audit.',
   'Neither a Tesla reference nor an analogy with known radiation establishes the proposed energy type. Independent confirmation of these exceptional claims was not established here.',
   'Separate a measurable circuit-output claim from an ontological claim about a new energy. Specify calibration, source isolation and timing controls for each.','P014 P022 P042 P075 P105','up2')
PC('DE19915730A1','Orgone accumulator and gravitational-field energy density','Dieter R. Schulze','2000-11-09','Related','Orgone|Gravity claims|Electrostatics','Thematic comparison','Explicit orgone terminology in a later document, not a Tesla or Newton invention.',
   'The published application proposes electrically influenced accumulator arrangements with asserted orgone and gravitational-energy effects.',
   'Electrical supply, magnetic materials, environmental heat and any claimed output must be defined separately.',
   'This is an application publication, not a verified grant. The document does not independently establish orgone as a physical energy or confirm the claimed effects.',
   'Translate one assertion into an observable with units. If no operational definition can be extracted, record that gap before proposing an experiment.','P004 P019 P033 P105','patent-utility-model',type='Published patent application')
PC('DE29604486U1','Orgone accumulator with minerals','Susanne Henze (listed applicant); claim sheet also names Jürgen Fischer','1996-06-20','Related','Orgone|Minerals|Health claims','Thematic comparison','A Reich-related utility-model record; inventor identity must not be inferred from a single applicant field.',
   'Layered materials and minerals are proposed as an orgone accumulator, with effects asserted in the document.',
   'Environmental heat, ordinary material properties and subjective endpoints need separate treatment.',
   'A utility-model publication is not clinical evidence or a demonstration of supernatural energy. No independent efficacy finding is established by this review.',
   'Compare an active and visually identical sham object on a predefined physical endpoint. Explain why a temperature difference alone would not establish a health benefit.','P014 P019 P052 P096','patent-utility-model',type='German utility-model publication')
PC('US2482773A','Detection of emanations from materials','Thomas G. Hieronymus','1949-09-27','Related','Radionics|Emanations|Subjective detection','Thematic comparison','A document for studying unusual detection claims and operator-dependent measurement.',
   'A prism and electrical arrangement are proposed to detect material emanations; the described endpoint includes perceived adhesion or friction while an operator strokes a plate.',
   'Apparatus settings, sample identity, operator knowledge and contact conditions can influence the reported endpoint.',
   'A subjective signal requires blinding and repeatability checks. Independent confirmation of the proposed emanation mechanism was not established here.',
   'Design a randomized, coded-sample analysis with a prespecified scoring rule. Compare sensitivity, false positives and chance performance using synthetic data.','P013 P014 P019 P107','prob')
PC('US9306527B1','Generating and utilizing scalar-longitudinal waves','Lee M. Hively / Gradient Dynamics LLC','2016-04-05','Related','Scalar claims|Magnetism|Wireless power','Explicit patent citation','Cites Tesla’s US512340A. This citation documents a connection, not Tesla’s endorsement.',
   'Bifilar antenna arrangements and modified electromagnetic descriptions are proposed to generate scalar-longitudinal waves; the text includes inventor-reported experimental data.',
   'Driving circuits, ordinary fields, receiver coupling and instrumentation must be accounted for.',
   'Ordinary scalar potential and longitudinal plasma modes are legitimate concepts. They do not by themselves verify this proposed propagating mode; independent replication was not established here.',
   'Extract a falsifiable prediction that differs from Maxwell-based coupling. Plan shielding, near/far-field, common-mode and instrument-crosstalk controls.','P009 P042 P043 P044 P091','tongem plasmatext')
PC('US10924868B2','Earbuds with scalar coil','Deric Solis, Matthew Sanderson, James McClanahan III & Wayne J. Powell / Soniphi LLC','2021-02-16','Related','Scalar claims|Sound|Perception','Explicit patent citation','Cites US512340A; later acoustic claims remain separate from Tesla’s winding disclosure.',
   'The document combines speaker circuitry, coils and a laser arrangement with claimed changes in perceived sound.',
   'Electrical drive, acoustic output level and device geometry are ordinary variables that can affect listening results.',
   'Patent publication does not establish a supernatural field or therapeutic effect. Independent support for the proposed exceptional mechanism was not established here.',
   'Specify level-matched blind listening and frequency-response measurements. Separate an audible difference from a claim explaining its physical cause.','P014 P037 P041 P047','scipy')
PC('US600457A','Electrical battery','Nathan B. Stubblefield','1898-03-08','Related','Earth|Electrostatics|Energy claims','Thematic comparison','A useful primary-text comparison for Earth-energy interpretations; not a Tesla patent.',
   'Copper and iron conductors form a voltaic couple with water or moist earth participating as electrolyte.',
   'The specification explicitly invokes galvanic action; chemical change and polarization belong in the accounting.',
   'An earth-connected battery does not demonstrate energy from ley lines or an inexhaustible planetary source.',
   'Build a paper energy budget from a galvanic-cell model. Identify what chemical and electrical measurements would distinguish it from an inputless-source claim.','P022 P037 P053','up2')

newton_records=[]
def NR(id,title,type,role,workDate,editionDate,shelfmark,catalogueId,claim,boundary,task,chapters,path='normalized',extra=''):
    url=f'https://www.newtonproject.ox.ac.uk/view/texts/{path}/{catalogueId}' if path=='normalized' else f'https://www.newtonproject.ox.ac.uk/catalogue/record/{catalogueId}'
    rid=PS('patent-'+id,title+' · '+catalogueId,'Newton Project / named archival custodian',url,type,task,workDate+'; edition '+editionDate+'; reviewed 2026-09-08')
    newton_records.append(dict(id=id,title=title,type=type,role=role,workDate=workDate,editionDate=editionDate,shelfmark=shelfmark,catalogueId=catalogueId,claim=claim,boundary=boundary,task=task,chapters=chapters.split(),resources=[rid]+extra.split(),url=url))
NR('N01','Reflecting telescope account','Published instrument account','Newton’s instrument; the printed account also contains editorial narration','25 March 1672','Philosophical Transactions 81, pp. 4004–4007','Printed Royal Society account','NATP00007','The account describes a reflecting telescope associated with Newton.','An invention described in a scientific publication is not automatically a patented invention. Do not attribute every third-person editorial sentence to Newton.','Sketch the optical path and compare mirror and lens aberrations; record the document type in a citation.','P048 P098')
NR('N02','Rubbed glass and paper fragments','Correspondence / experimental report','Newton writing to Henry Oldenburg','21 December 1675','Scholarly transcription of the letter','Cambridge University Library, MS Add. 9597/2/18/46–47','NATP00264','Newton discusses electrostatic behavior, rubbing materials and difficulty reproducing an effect.','“Electric virtue” is historical vocabulary. The letter documents experimental inquiry, not evidence of a supernatural agency.','Translate the procedure into variables and controls without modernizing the original claim; explain why replication conditions matter.','P019 P033 P098')
NR('N03','Hypothesis explaining the properties of light','Hypothesis communicated to the Royal Society','Newton as author of a conjectural physical account','1675','Thomas Birch, History of the Royal Society, vol. 3 (1757)','Printed historical transmission, pp. 247–305','NATP00002','Ether-like constituents are considered in connection with light, electrical and magnetic effects, gravity and animal motion.','A conjectured medium is not an observed substance. The work date, later printed edition and modern transcription are different dates.','Make a two-column list of observations and proposed causes; identify one alternative explanation available to a later physicist.','P042 P049 P098')
NR('N04','Opticks, Book III: the Queries','Published questions and natural philosophy','Newton as author','Queries developed across editions','Second English edition, 1718','Opticks Book III','NATP00051','Queries discuss possible media and active principles in heat, gravity, sensation and matter.','Questions and proposed causes have different force from the book’s optical experiments. “Occult” and “active” must be read in their historical arguments, not assigned one modern meaning.','Compare a selected Query with an experimental proposition; mark interrogative wording and distinguish a measurable regularity from a proposed cause.','P019 P049 P098')
NR('N05','General Scholium','Natural philosophy and theology','Newton as author; later English translation','First Latin version 1713; revised 1726','English edition 1729, vol. 2, pp. 387–393','Principia General Scholium','NATP00056','The text discusses gravity, divine order and a possible subtle spirit, while acknowledging insufficient experiments to establish the latter’s laws.','Newton’s gravitational law, its unknown cause and his natural theology are distinct claims. The closing speculation is not a verified unifying field theory.','Classify each selected paragraph as mathematical result, empirical generalization, conjecture or theology and justify the classification.','P026 P097 P105')
NR('N06','Emerald Tablet translation and commentary','Alchemical transcription / translation / commentary','Newton as translator, copyist and commentator, not author of the older attributed work','Early 1680s–1690s; some annotations may be later','Modern scholarly catalogue and transcription','Keynes MS 28, King’s College, Cambridge','ALCH00017','The manuscript records engagement with the Hermetic Emerald Tablet tradition.','Copying a proposition does not establish endorsement, experimental success or Newtonian authorship of the source. Symbolic correspondence is not a demonstrated field equation.','Compare the English, Latin and commentary sections; annotate which voice is speaking and what evidence each interpretation would require.','P098 P104',path='catalogue',extra='chymistry')
PS('patent-tablet-text','Emerald Tablet manuscript · normalized transcription','Indiana University / Chymistry of Isaac Newton','https://webapp1.dlib.indiana.edu/newton/mss/norm/ALCH00017','Primary transcription','Compare translation, copied text and commentary, with manuscript folios.')
newton_records[-1]['resources'].append('patent-tablet-text')
NR('N07','Fitzwilliam Notebook','Notebook / accounts / scientific and religious notes','Newton as notebook keeper','1662–1669','Modern scholarly catalogue','Fitzwilliam Museum notebook','ALCH00069','Entries include mathematics, physics, religion and expenses; purchases of chemicals, furnaces and an alchemical collection document chymical study.','Purchasing equipment or using possible cipher-like notation does not demonstrate secret working technology. Notebook contents have mixed purposes.','Construct a dated evidence table separating purchases, copied knowledge, calculations and reported observations.','P098 P104',path='catalogue',extra='chymistry')
NR('N08','Philosophical origins of gentile theology','Draft historical and theological work','Newton as author; portions in Humphrey Newton’s hand with Isaac’s amendments','Mainly 1684–1690; later material also present','Modern catalogue; linked English translation','Yahuda MS 16, National Library of Israel','THEM00059','The main drafts explore ancient wisdom, astronomical interpretation of gods, sacred philosophy and origins of idolatry and magic. The catalogue also notes mid-1711 Mint material on f. 20v.','Describing a tradition does not equal endorsing it. The work also criticizes astrological superstition; it is not a patented cosmological machine.','Trace one ancient-source attribution through the translation. Separate Newton’s historical reconstruction from evidence about the ancient practice.','P098 P104',path='catalogue')
PS('patent-gentile-translation','Philosophical origins of gentile theology · translation','Newton Project','https://www.newtonproject.ox.ac.uk/view/translation/TRAN00010','Scholarly translation','Read the argument and attribution layers alongside the manuscript catalogue.')
newton_records[-1]['resources'].append('patent-gentile-translation')
NR('N09','Description of Solomon’s Temple','Textual and geometrical reconstruction','Newton as author; posthumous publication','Published posthumously in 1728','Chronology of Ancient Kingdoms Amended, chapter V','Printed chapter','THEM00190','The chapter reconstructs temple dimensions and layout from textual sources and metrological assumptions.','A geometric reconstruction is not an archaeological survey or evidence of an energy-focusing device. An adopted cubit changes inferred dimensions.','Draw a dimensioned plan for two declared cubit assumptions. Keep textual constraints separate from speculative physical interpretations.','P003 P004 P098')
NR('N10','Prophecy calculations and 2060','Theological fragments','Newton as interpreter of prophetic chronology','After 1700','Modern scholarly transcription','Yahuda MS 7.3g, especially ff. 13v–14r','THEM00437','A conditional calculation combines a 1,260-year interval with a starting point of AD 800, with qualifications about rash date-setting.','This is theological chronology, not a physics-based forecast of the world’s destruction. A conditional calculation is not an unconditional prediction.','Rewrite the calculation as explicit assumptions and implications; list what the manuscript qualifies and what a popular summary might omit.','P001 P098 P105')
NR('N11','Patent reappointing Henry Harris as engraver','Royal appointment instrument','Newton is catalogued as an author, not as an inventor','26 September 1702','Modern scholarly catalogue','The National Archives, MINT 19/1/161–2','MINT00054','The record concerns an engraver’s appointment.','The word patent here identifies a royal instrument. It does not establish an invention patent by Isaac Newton.','Record the appointee, office, author attribution and document type; compare with the metadata fields of a modern invention patent.','P104',path='catalogue')
NR('N12','Reply about the engravers’ patent','Administrative reply about royal privileges','Unknown author and Newton; date in Newton’s hand','12 October 1704','Modern scholarly catalogue','The National Archives, MINT 19/1/172–3','MINT00070','The query concerns engravers’ privileges, royal imagery and distinctions involving Mint stamps and private work.','A discussion of privileges over coin or medal production is not Newton inventorship of an electromagnetic device.','Identify the privilege under discussion and its beneficiary; explain why a keyword-only patent search would misclassify this record.','P104',path='catalogue')

patents=dict(
    date='2026-09-08',
    scope='A source-led research room: the full 311-row Tesla museum catalogue, 28 selected patent studies, and 12 Newton archive records. Study unusual claims through original wording, physics, and testable predictions.',
    inventory=json.loads((ROOT/'data/tesla-patent-index.json').read_text(encoding='utf-8')),
    cases=patent_cases,
    newton=dict(scope='No invention patent naming Isaac Newton (1642–1727) as inventor was verified in this research pass. His archive includes royal letters patent concerning appointments and privileges; these are different document types. A complete negative finding would require a historical register and index search.',records=newton_records),
    connections=[
      dict(from_='US512340A · Tesla',to='US9306527B1 · Hively',relation='Later publication cites Tesla’s coil patent; citation is not endorsement or experimental validation.',url='https://patents.google.com/patent/US9306527B1/en'),
      dict(from_='US512340A · Tesla',to='US10924868B2 · Soniphi inventors',relation='Later earbud publication cites the coil patent; the acoustic mechanism requires its own evidence.',url='https://patents.google.com/patent/US10924868B2/en'),
      dict(from_='Tesla and Reich as named in the text',to='US7235945B2 · Correa & Correa',relation='Explicit historical attribution by the later authors, not shared inventorship.',url='https://patents.google.com/patent/US7235945B2/en'),
      dict(from_='Brown asymmetric-capacitor claims',to='NASA 2004 experimental reports',relation='Independent experimental comparison of specified capacitor arrangements; not replication of every claimed variant.',url='https://ntrs.nasa.gov/api/citations/20040171929/downloads/20040171929.pdf'),
      dict(from_='Newton archive keyword “patent”',to='MINT00054 and MINT00070',relation='Royal appointment/privilege documents; no invention-patent identity established.',url='https://www.newtonproject.ox.ac.uk/catalogue/record/MINT00070')
    ],
    coverage=[
      'Catalogue scope: all numbered rows in Snežana Šarboh’s 2019 list hosted by the Nikola Tesla Museum: 112 US and 199 foreign entries, across 27 historical granting jurisdictions. Historical jurisdictions are not present-day country counts.',
      'These are 311 catalogue entries, not 311 distinct inventions. Priority relationships, equivalents and reissues affect family counts. No worldwide completeness claim is made for all patents “around” magnetism, electrostatics or unconventional concepts.',
      'The US and foreign row sequences were checked against the source PDF. Only 12 selected Tesla specifications receive detailed analysis here; other entries are catalogue metadata, with US publication links and foreign source-page links.',
      'Source discrepancy: the PDF summary says two New South Wales entries, while numbered rows 168–171 list four. This room uses the numbered rows; the summary’s counts sum to 309 rather than 311.',
      'Source discrepancy: the museum English overview prints 119 US basic patents in an arithmetic statement whose Serbian original says 109. This room does not adopt that inconsistent overview as a definitive invention-family total.',
      'US row 97 is reissue USRE11865E. Its source cells contain the original patent’s 14 August 1900 grant date and number 655,838; the reissue application was filed 21 September 1900, serial 30,722. US row 53 prints Lightning and filing 26.04.1891; the specification says Lighting and filing 25 April 1891. Original table text is retained with a correction note.',
      'Argentina entry INT-001 and Transvaal entry INT-195 have no grant date listed in the catalogue. An empty source field is shown as not listed, not guessed. Dates in that table retain day.month.year format.',
      'The museum reports unsuccessful and unsubmitted Tesla applications outside this granted-entry list. They have not been enumerated here. Later patents are a deliberately selected thematic set, not an exhaustive global census.',
      'Google Patents provides readable publication text and metadata. Foreign catalogue identifiers preserve their historical form; no modern identifier is invented where the mapping is unverified.',
      'Patent review snapshot: 8 September 2026. Existing research-paper annotations retain their own dates. No legal-status, validity or current enforceability opinion is supplied.'
    ],
    protocol=[
      'Identify the document: inventor, applicant/assignee, jurisdiction, publication identifier and kind, filing/priority/publication dates. Distinguish a published application, grant, reissue, utility model and royal letters patent.',
      'Read the actual specification and claims. Separate what the inventor asserts from a later interpretation, archive description, press story or cited reference.',
      'Draw a system boundary. List electrical, chemical, mechanical, radiative and thermal inputs; stored energy changes; material flows; outputs; and return/reset steps.',
      'Translate the unusual claim into a prediction with units and a detection threshold. Distinguish a working observable from a proposed explanation for it.',
      'Search for independent tests with the same geometry, medium and operating regime. Record disagreements, nulls, measurement limits and unmatched conditions.',
      'Plan calibration, blinding where relevant, randomization, environmental controls, uncertainty and an analysis rule before interpreting data. Include ordinary coupling and instrument artifacts.',
      'Write a bounded conclusion: what the source documents, what the experiment supports, and what remains untested. Preserve editions, URLs, dates and negative search scope.'
    ],
    gaps=[
      'Extend the Tesla census through museum archival application files and verified foreign gazettes. Record rejected, withdrawn and unsubmitted documents separately; reconcile invention-family definitions.',
      'Search historical British invention-patent indexes/registers with an explicit date range and name-disambiguation protocol before making a universal claim about Newton’s patent activity.',
      'For every exceptional modern claim, seek independent data, apparatus details, controls, corrections and unsuccessful replications. “Not established in this review” is not a claim that no such work could exist anywhere.',
      'Expand related patents by one declared theme and classification at a time. Save queries, inclusion rules and family decisions rather than treating name mentions as inventor relationships.'
    ]
)
for edge in patents['connections']:edge['from']=edge.pop('from_')
exec(compile((ROOT/'patent_learning.py').read_text(encoding='utf-8'),str(ROOT/'patent_learning.py'),'exec'))
