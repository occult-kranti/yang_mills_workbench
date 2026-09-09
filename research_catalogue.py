"""Authored research annotations. Metadata snapshot checked 7 September 2026.
Executed by content.py, which supplies the shared data constructors.
"""
papers=[]
def P(i,title,authors,field,date,updated,status,summary,method,limits,pre,doi=''):
    papers.append(dict(id=i,title=title,authors=authors,field=field,date=date,updated=updated,status=status,url='https://arxiv.org/abs/'+i,doi=doi,summary=summary,method=method,limits=limits,prereqs=[f'P{x:03}' for x in pre]))

P('2503.14738','DESI DR2 Results II: Measurements of Baryon Acoustic Oscillations and Cosmological Constraints','DESI Collaboration (M. Abdul-Karim et al.)','Cosmology','2025-03-18','2025-10-09','Peer-reviewed · Physical Review D 112, 083515 (2025)',
 'Baryon acoustic oscillation measurements constrain cosmic expansion and, with additional datasets, test dark-energy models.',
 'Large galaxy and quasar survey; distance measurements and cosmological parameter inference.',
 'Preferences for evolving dark energy depend on the model and datasets combined. They are not an established discovery of a new dark-energy mechanism.',[14,81,107],'https://doi.org/10.1103/tr6y-kpc6')
P('2609.04991','Expanding the scope of dark siren cosmology: Inferring the population properties of gravitational wave-hosting galaxies','Rachel Gray, Daniel Williams & Alexander Papadopoulos','Gravitational-wave cosmology','2026-09-04','','Preprint · hierarchical inference',
 'Connects gravitational-wave populations with the properties of possible host galaxies to improve dark-siren cosmological inference.',
 'Hierarchical population and cosmological modeling using galaxy information and gravitational-wave observations.',
 'Host weighting, catalogue incompleteness, selection effects, and population assumptions can change the inference; this is not a direct distance-ladder measurement.',[80,81,107])
P('2609.05001','Fabrication-Aware Design of a Hybrid Metasurface-Bragg Mirror for Low-Noise Precision Optics','Mika Gaedtke et al.','Precision optics','2026-09-04','','Preprint · design and simulation',
 'Studies a hybrid optical reflector with fabrication tolerances included in the design of low-noise precision optics.',
 'Electromagnetic modeling and tolerance sampling connect design choices with predicted optical and noise properties.',
 'Predicted improvements require fabrication and measurement. A component simulation does not establish an operating detector’s sensitivity.',[46,51,96])
P('2608.03996','Reduced-order modeling for electromagnetic inverse problems: a layered medium benchmark','Konstantinos Alexopoulos & Josselin Garnier','Electromagnetic inverse problems','2026-08-04','','Preprint · computational methods',
 'Develops a reduced representation for recovering electromagnetic properties of layered media.',
 'A reduced-order inverse formulation tested against a five-layer numerical benchmark.',
 'Layered geometry and controlled synthetic data are narrower than general three-dimensional, noisy experimental reconstruction.',[35,46,107])
P('2606.23974','The science of compressional heating on the LM26 magnetized target fusion experiment','S. J. Howard et al.','Plasma and fusion','2026-06-22','2026-06-30','Preprint · experiment',
 'Reports compressional heating studies of magnetized deuterium plasma in a lithium-liner experiment.',
 'Analysis of eleven compression shots and their plasma diagnostics.',
 'Evidence of heating is distinct from fusion gain, net energy production, sustained operation, or commercial electricity generation.',[91,96,107])
P('2602.10041','Design of experiments characterising heat conduction in magnetised, weakly collisional plasma','T. A. Vincent et al.','Plasma transport','2026-02-10','','Preprint · experimental design',
 'Proposes a laboratory platform for testing heat conduction in magnetized, weakly collisional plasma.',
 'FLASH magnetohydrodynamic simulations and proposed laser-experiment conditions.',
 'A designed experiment and predicted transport suppression do not constitute a measured result. Kinetic assumptions require careful checking.',[59,91,107])
P('2606.01470','Emergent Transfer of a Physics Foundation Model from Simulation to Laboratory Turbulence','Payel Mukhopadhyay et al.','Turbulence and scientific machine learning','2026-05-31','','Preprint · computational and laboratory comparison',
 'Investigates whether a pretrained physics model can transfer from a small collection of Rayleigh–Taylor simulations to laboratory mixing behavior.',
 'Fine-tuning and comparison of a learned surrogate with a selected experimental flow.',
 'A successful transfer case does not establish general turbulence prediction; training overlap, boundary conditions, and out-of-distribution tests matter.',[31,32,94,106])
P('2401.17871','Experimental study of three-dimensional turbulence under a free surface','Timothée Jamin, Michael Berhanu & Eric Falcon','Fluid dynamics','2024-01-31','','Peer-reviewed · Physical Review Fluids 10, 034608 (21 March 2025)',
 'Studies how a free surface changes turbulent velocity fluctuations and anisotropy beneath it.',
 'A laboratory jet-array flow with spatially resolved velocity statistics.',
 'The observed suppression and enhancement of different velocity components depend on the geometry and accessible flow regime.',[32,94,107],'https://doi.org/10.1103/PhysRevFluids.10.034608')
P('2608.12485','Dual Gauge Theory for Two Dimensional Superfluid Turbulence','Tobias Helbig, Sayak Bhattacharjee & Srinivas Raghu','Superfluids and field theory','2026-08-12','','Preprint · theory',
 'Uses a gauge-theory description to study energy transfer in two-dimensional superfluid vortex dynamics.',
 'An effective point-vortex framework and its emergent field-theoretic representation.',
 'The model’s dimensionality and vortex approximations limit direct application to generic three-dimensional turbulence.',[58,85,89])
P('2609.02696','A viscoelastic theory for ultrasound-induced intracellular streaming','Niels Gieseler, Falko Ziebert & Ulrich S. Schwarz','Biophysics and acoustics','2026-09-02','','Preprint · theory',
 'Predicts how viscoelastic response can affect acoustically driven streaming in a simplified intracellular setting.',
 'A semi-analytic viscoelastic droplet model using an Oldroyd-B constitutive description.',
 'Model predictions, including possible flow reversal, need comparison with biological measurements; a cell has additional structures and active processes.',[32,47,95])
P('2609.00564','Mudskippers use tail thrusting to help crutching to move on mud of various wetness','Divya Ramesh, Gargi Sadalgekar, Jiangqi Tan & Chen Li','Biomechanics','2026-09-01','','Preprint · experimental study; journal review reported',
 'Examines how mudskippers combine appendage and tail forces across substrates with different wetness.',
 'Laboratory locomotion observations coupled to characterization of clay-like substrate mechanics.',
 'Animal numbers, substrate preparation, and laboratory conditions bound the conclusions; a reported review status is not publication.',[21,32,95,107])
P('2603.23043','Assessing the Robustness of Climate Foundation Models under No-Analog Distribution Shifts','Maria Conchita Agana Navarro, Geng Li, Theo Wolf & Maria Perez-Ortiz','Climate and scientific machine learning','2026-03-24','2026-04-22','Preprint · benchmark',
 'Compares learned climate prediction models under distribution shifts beyond their historical training conditions.',
 'Controlled training and evaluation of neural model families on no-analog conditions.',
 'Benchmark performance is conditional on data and protocols; it is not a new observational estimate of climate sensitivity.',[94,106,107])
P('2608.15352','Conforming and nonconforming Trefftz approximations for two-dimensional scalar electromagnetic problems','Igor Tsukerman','Computational electromagnetism','2026-08-15','','Preprint · numerical methods',
 'Studies approximation spaces informed by local differential equations for selected electromagnetic problems.',
 'Trefftz-based discretizations evaluated on two-dimensional scalar examples.',
 'Reported accuracy should be compared at matched error and cost; selected scalar examples do not establish general three-dimensional vector performance.',[11,35,46,106])
P('2608.02773','Quantum error correction at ultra-low overhead','Zhide Lu, Weikang Li & Dong-Ling Deng','Quantum error correction','2026-08-03','2026-08-17','Preprint · theory and simulation',
 'Proposes Cornucopia quantum low-density parity-check codes with favorable simulated overhead and error-correction behavior.',
 'Code construction, decoding analysis, and simulations under specified noise assumptions.',
 'Extrapolated logical error rates depend on noise and implementation assumptions. The paper is not a demonstration of a working large fault-tolerant processor.',[18,72,73])
P('2606.04079','Quantum error correction with the toric code','Atom Computing and collaborators','Quantum computing hardware','2026-06-02','','Preprint · experiment',
 'Demonstrates repeated syndrome extraction and replacement of lost neutral atoms in a toric-code setting.',
 'Neutral-atom experiments with repeated cycles; distinct protocols evaluate extended operation and code-distance behavior.',
 'Do not combine unlike protocols: the long reload sequence and the shorter distance comparison establish different facts. This is not general fault-tolerant computation.',[71,73,96])
P('2608.28418','Optomechanical inertial reference for atom interferometry','A. Rajagopalan et al.','Atomic sensing','2026-08-28','','Preprint · experiment',
 'Uses an optomechanical reference to address vibration noise in atom-interferometric sensing.',
 'A shared mechanical reference with optical and atomic measurements.',
 'Sensor characterization and vibration rejection do not by themselves test the quantization of gravity or a quantum-gravity theory.',[27,49,71,96])
P('2608.18071','Ultrafast and high resolution spatial light modulation for cold atoms','Alexander Dennisovich Deters, Yanfei Li, Alexander Douglas, Markus Greiner & Aaron W. Young','Atomic control and photonics','2026-08-18','','Preprint · optical demonstration and modeling',
 'Develops rapid spatial optical control relevant to cold-atom experiments and discusses modeled many-body applications.',
 'Optical performance measurements paired with numerical examples of atom-control applications.',
 'Measured pattern performance and simulated Hubbard-model control are different evidence levels; heating and realized atom-control fidelity require separate validation.',[49,51,71,87])
P('2609.04319','Exact quantum spin liquids with topological order on maple-leaf and trellis lattices','Li Ern Chern, Roderich Moessner & Claudio Castelnovo','Quantum materials','2026-09-03','','Preprint · theory and simulation',
 'Constructs lattice-spin models supporting topologically ordered quantum spin-liquid phases.',
 'Designed anisotropic models, Majorana representations, flux analysis, and numerical sampling.',
 'A phase of a specified mathematical model is not an experimental identification of that phase in a newly discovered material.',[65,86,87])
P('2609.04291','Reproducible capillary fluctuation analysis of solid-liquid interfaces for stiffness and anisotropy calculations','Kai Liu, Douglas E. Spearot & Damien Tourret','Computational materials','2026-09-03','','Preprint · computational methodology',
 'Examines how analysis choices affect interfacial stiffness and anisotropy inferred from capillary fluctuations.',
 'Molecular-dynamics interface analysis with sampling, geometry, and fitting sensitivity checks.',
 'Pure-aluminum examples and chosen potentials limit material generality; sampling duration and interface definitions can dominate uncertainty.',[56,87,106,107])
P('2608.30871','On the relaxation problem in statistical mechanics','Giuseppe Del Vecchio Del Vecchio','Statistical mechanics foundations','2026-08-31','2026-09-01','Preprint · foundational proposal',
 'Discusses relaxation using an observer-record and information perspective.',
 'Conceptual and formal analysis of the relation between microscopic descriptions and recorded macroscopic behavior.',
 'Treat this as a proposal to compare critically with ensemble and dynamical accounts, not an established replacement for thermodynamics.',[13,30,56,59])
P('2609.04856','The elasticity of semiflexible polymers with reversible spontaneous curvature in two dimensions','Donghyeon Kim & Panayotis Benetatos','Soft matter','2026-09-04','','Peer-reviewed · Journal of Chemical Physics 165, 064111 (11 August 2026)',
 'Analyzes the elasticity of a polymer model whose spontaneous curvature can switch reversibly.',
 'An analytic two-state wormlike-chain model in a two-dimensional weak-bending regime.',
 'Dimensionality, weak bending, and the ensemble choice constrain interpretation. Journal publication predates this arXiv submission.',[56,59,95],'https://doi.org/10.1063/5.0349713')
P('2609.04402','Search for the rare Higgs boson decay H → Zγ in proton-proton collisions at √s = 13 and 13.6 TeV','CMS Collaboration','Particle physics','2026-09-03','','Preprint · submitted to Physics Letters B',
 'Searches for a rare Higgs-boson decay using collision data and invariant-mass reconstruction.',
 'Signal and background fits with detector and modeling uncertainties.',
 'The reported 1.9-standard-deviation signal significance does not establish observation or discovery. Submission is distinct from peer-reviewed publication.',[76,88,96,107])
P('2609.04302','Eye-opening bounds on cusps','Ryan A. Lanzetta, Ian Moult & Yifan Wang','Quantum field theory','2026-09-03','','Preprint · mathematical theory',
 'Derives constraints involving cusps in a conformal-defect field-theory setting.',
 'Reflection positivity and field-theoretic inequalities.',
 'The bounds depend on their theoretical hypotheses and are not direct collider measurements.',[18,89])
P('2609.04376','Spin-dependent azimuthal asymmetry of coherent J/ψ photoproduction in hadronic PbPb collisions at √sNN = 5.36 TeV','CMS Collaboration','Nuclear and high-energy physics','2026-09-03','','Preprint · submitted to Physical Review Letters',
 'Studies azimuthal decay patterns in coherent charmonium photoproduction in heavy-ion collisions.',
 'Muon-pair reconstruction and harmonic analysis with systematic uncertainties.',
 'A significant harmonic supports a specified polarization interpretation; it does not uniquely settle every production model or nuclear-structure question.',[65,88,90,96])
P('2503.18667','Sterile-neutrino search based on 259 days of KATRIN data','KATRIN Collaboration (Himal Acharya et al.)','Neutrino physics','2025-03-24','','Peer-reviewed · Nature 648, 70–75 (3 December 2025)',
 'Uses precision beta-decay spectroscopy to test sterile-neutrino admixture over an accessible mass and mixing range.',
 'Analysis of approximately 36 million electrons collected over 259 measurement days.',
 'Exclusion regions apply to the tested model and parameter range; they do not exclude all sterile-neutrino hypotheses.',[90,96,107],'https://doi.org/10.1038/s41586-025-09739-9')

FEED_ROWS=[('quant-ph','Quantum physics'),('cond-mat.str-el','Strongly correlated electrons'),('cond-mat.mtrl-sci','Materials science'),('cond-mat.stat-mech','Statistical mechanics'),('cond-mat.mes-hall','Mesoscopic systems'),('cond-mat.soft','Soft condensed matter'),('hep-ex','High-energy experiments'),('hep-th','High-energy theory'),('hep-ph','Particle phenomenology'),('nucl-ex','Nuclear experiments'),('nucl-th','Nuclear theory'),('gr-qc','General relativity and quantum cosmology'),('astro-ph.CO','Cosmology'),('astro-ph.HE','High-energy astrophysics'),('astro-ph.IM','Astronomical instrumentation'),('astro-ph.EP','Earth and planetary astrophysics'),('astro-ph.GA','Galaxies'),('astro-ph.SR','Solar and stellar astrophysics'),('physics.atom-ph','Atomic physics'),('physics.optics','Optics'),('physics.plasm-ph','Plasma physics'),('physics.flu-dyn','Fluid dynamics'),('nlin.CD','Chaos and nonlinear dynamics'),('physics.bio-ph','Biological physics'),('physics.ao-ph','Atmospheric and oceanic physics'),('physics.geo-ph','Geophysics'),('physics.comp-ph','Computational physics'),('physics.ins-det','Instrumentation and detectors')]
feeds=[dict(id=c,label=n,category=c,url='https://arxiv.org/list/'+c+'/recent',description='Eight newest submissions returned by the selected category query; manually refreshed and cached for 15 minutes. Browse the linked category for broader coverage.') for c,n in FEED_ROWS]
