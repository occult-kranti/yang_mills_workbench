C(75,'Special relativity: clocks, events, and spacetime','gravity',[3,4,7], 'up3 einsr einbook tong',
'''Events and operational measurements: reference frames; ideal clocks and rulers; Einstein synchronization; inertial observers > Draw the emission, reflection, and reception events for a radar distance measurement.
| Lorentz transformations: invariant light speed; Lorentz factor; coordinate transformations; inverse transformation > Transform two events between frames moving at 0.6c and check their invariant interval.
| Time, length, and simultaneity: proper time; time dilation; length contraction; relativity of simultaneity > Explain why measuring both endpoints simultaneously matters when measuring a moving rod.
| Causal geometry: light cones; timelike and spacelike separation; spacetime diagrams; proper-time integrals > Classify five event pairs and identify which can have their time ordering reversed.
| Relativistic motion: velocity addition; rapidity; relativistic Doppler shift; accelerated worldlines > Compare Earth and traveler elapsed times for an outward-and-return journey with explicitly stated turnaround assumptions.''',
'Derive the one-dimensional Lorentz transformation from linearity, reciprocity, and light-cone invariance; recover Galilean behavior when speed is small compared with c.',
'A spacecraft travels 4 light-years in the Earth frame at 0.8c, turns around, and returns at the same speed. Compute Earth time, traveler proper time, and the simultaneity change at idealized turnaround.',
'Transform events consistently, identify an invariant and a frame-dependent quantity, and resolve a clock comparison using complete worldlines.',
'Time dilation alone is not a complete twin-paradox explanation: reunion compares different worldlines, and a turnaround changes the traveler’s inertial frame.')

C(76,'Relativistic dynamics and electromagnetic covariance','gravity',[75,9,16], 'up3 tongem einmass feynman',
'''Four-vectors and invariants: four-position; four-velocity; Minkowski inner product; metric-sign convention > Verify four-velocity normalization for a particle moving at 0.8c using one declared sign convention.
| Energy and momentum: four-momentum; rest energy; kinetic energy; mass-shell relation > Compare Newtonian and relativistic kinetic energy over speeds from 0.01c to 0.99c.
| Reactions and collisions: center-of-momentum frame; invariant mass; threshold energy; conservation laws > Calculate the invariant mass of two photons with arbitrary crossing angle.
| Relativistic electrodynamics: four-current; field tensor; electric and magnetic field transformations; Lorentz-force equation > Transform a simple transverse electric field and test the field invariants.
| Conservation and radiation: stress-energy tensor; energy flux; momentum flux; radiation pressure > Relate the power of an absorbed light beam to force and identify the source of its momentum.''',
'Derive E² = p²c² + m²c⁴ from four-momentum normalization, then derive the nonrelativistic kinetic-energy limit.',
'Two photons of energies 2 MeV and 3 MeV collide head-on. Compute the system invariant mass and explain why parallel photons with the same energies give a different result.',
'Solve a relativistic conservation problem in two frames and explain how electric and magnetic fields belong to one covariant field.',
'Rest mass is invariant; a particle’s energy and momentum depend on the observer. Avoid treating an increase of kinetic energy as a change of invariant mass.')

C(77,'The geometry of general relativity','gravity',[17,75,16], 'tonggr mitgr sympy',
'''Local coordinates and manifolds: charts; tangent vectors; covectors; coordinate versus physical components > Transform a vector from Cartesian to polar coordinates and distinguish its components from its magnitude.
| Metrics and proper distance: Lorentzian signature; line element; inverse metric; volume element > Compute distances on a sphere and proper time along a simple timelike curve.
| Connections and transport: covariant derivative; Christoffel symbols; parallel transport; local inertial coordinates > Compute the polar-coordinate connection in a flat plane and explain why nonzero symbols need not mean curvature.
| Curvature and tides: Riemann tensor; Ricci tensor; scalar curvature; geodesic deviation > Calculate the curvature scalar of a two-sphere and compare with a flat plane in curved coordinates.
| Geodesics and symmetries: variational geodesic equation; affine parameter; Killing vectors; conserved quantities > Derive a conserved quantity from a time-independent metric and check it along a numerical trajectory.''',
'Derive the geodesic equation by varying the metric action and distinguish coordinate acceleration from invariant tidal effects.',
'For ds² = dr² + r²dθ², calculate the nonzero Christoffel symbols and verify that the Riemann tensor vanishes away from the coordinate singularity.',
'Compute a connection and a curvature invariant in a simple metric, and explain which apparent effects disappear after a coordinate change.',
'Curved coordinates are not evidence of curved spacetime. Christoffel symbols can be nonzero in flat space, while tidal curvature cannot be removed throughout a region.')

C(78,'Einstein equations, the Newtonian limit, and precision tests','gravity',[77,76], 'tonggr mitgr eingr nist',
'''Matter as a gravitational source: stress-energy; energy density; pressure and stresses; local conservation > Write the rest-frame stress-energy tensor of a perfect fluid and interpret every diagonal term.
| Field equations and action: Einstein tensor; cosmological constant; Einstein-Hilbert action; Bianchi identity > Explain why the contracted Bianchi identity is compatible with covariant stress-energy conservation.
| Recovering familiar gravity: weak-field metric; slow-motion limit; Poisson equation; equivalence principle > Extract Newtonian acceleration from a weak static metric and identify neglected terms.
| Solar-system tests: gravitational redshift; light bending; perihelion precession; Shapiro delay > Estimate the solar contribution to light deflection and state the weak-field approximation.
| Comparing models with data: clock comparisons; post-Newtonian parameters; nuisance parameters; residuals and systematics > Design a residual plot that distinguishes an incorrect model parameter from an unmodeled timing offset.''',
'Recover Poisson’s equation and Newtonian motion from the weak-field, slow-motion limit of general relativity; track the convention for gravitational potential.',
'Estimate the fractional clock-rate difference between stationary clocks separated vertically by 100 m near Earth using gh/c²; distinguish the approximation from an exact spacetime model.',
'Explain how a theoretical metric produces an observable, give an uncertainty budget for one precision test, and identify where the approximation fails.',
'The equivalence principle is local. Uniform acceleration can imitate a local gravitational effect, but it cannot eliminate tidal curvature over an extended laboratory.')

C(79,'Black holes, horizons, and relativistic compact objects','gravity',[78], 'tonggr mitgr et',
'''Schwarzschild geometry: areal radius; exterior solution; horizon; coordinate singularity > Compare the behavior of metric components and a curvature invariant at the Schwarzschild radius.
| Orbits and observation: effective potentials; circular-orbit stability; photon sphere; redshift and lensing > Plot timelike effective potentials and locate the innermost stable circular orbit in Schwarzschild spacetime.
| Horizon-regular descriptions: ingoing coordinates; null geodesics; causal diagrams; infalling proper time > Follow an inward light ray in horizon-regular coordinates and explain the difference from distant coordinate time.
| Rotating black holes: Kerr parameters; ergoregion; frame dragging; spin-dependent orbits > Distinguish the event horizon, ergosurface, photon region, and observed shadow.
| Thermodynamics and evidence: area law; Hawking temperature; accretion observables; model-dependent inference > Estimate the Hawking temperature of a solar-mass black hole and compare it with the cosmic microwave background.''',
'Derive the Schwarzschild circular-orbit conditions from the radial effective potential and distinguish null and timelike orbits.',
'For a nonrotating ten-solar-mass black hole, compute horizon, photon-sphere, and innermost-stable-orbit radii; state what changes when spin is introduced.',
'Interpret a black-hole diagram without confusing a coordinate singularity, causal horizon, physical singularity, and telescope observable.',
'A black-hole shadow is not a direct photograph of the event horizon; photon propagation, emitting matter, viewing geometry, and instrument response shape the image.')

C(80,'Gravitational waves: prediction, detectors, and open data','gravity',[78,11,14,15], 'tonggr gwosc et scipy',
'''Linearized gravitational waves: metric perturbations; gauge choice; transverse-traceless modes; strain > Sketch the relative displacement pattern for plus and cross polarizations.
| Sources and waveforms: quadrupole radiation; binary inspiral; chirp mass; inspiral-merger-ringdown > Estimate a chirp mass from an idealized frequency and frequency derivative with all SI units shown.
| Interferometer measurement: differential arm length; transfer functions; shot noise; seismic and thermal noise > Convert a stated strain to a differential arm displacement and explain why detector calibration is needed.
| Signal detection: sampling; power spectral density; whitening; matched filtering and false alarms > Use a GWOSC tutorial to compare a signal-containing interval with neighboring noise and document preprocessing.
| Scientific inference: waveform models; Bayesian posteriors; calibration uncertainty; selection bias > Make a signal-versus-noise analysis log and separate detection significance from source-parameter precision.''',
'Derive the leading inspiral frequency scaling with chirp mass using Newtonian orbital energy and quadrupole energy loss; state its regime of validity.',
'Reproduce a public GWOSC time-series or spectrum figure with recorded event identifier, detector, sample rate, filters, and excluded data-quality intervals.',
'Explain what was measured, how noise was characterized, which waveform assumptions entered, and why a filtered visual oscillation is insufficient evidence by itself.',
'Matched-filter signal-to-noise ratio is not automatically a false-alarm probability; the background, trial factors, detector coincidence, and noise behavior matter.')

C(81,'Cosmology: expansion, thermal history, and structure','gravity',[78,14], 'tongcosmo mitgr astropy eincosmo',
'''Homogeneous expanding models: cosmological principle; FLRW metric; scale factor; comoving coordinates > Convert between proper and comoving separations for two stated scale factors.
| Cosmic dynamics: Friedmann equations; density parameters; curvature; matter, radiation, and dark energy > Solve flat matter-dominated expansion and compare its age relation with a model containing a cosmological constant.
| Distances and redshift: luminosity distance; angular-diameter distance; standard candles; standard rulers > Plot both distance definitions versus redshift using an explicitly specified Astropy cosmology.
| Thermal history: radiation cooling; nucleosynthesis; recombination; cosmic microwave background > Place major events in chronological order and distinguish recombination from reionization.
| Structure and inference: perturbation growth; matter power spectrum; BAO; dark-matter and dark-energy constraints > Read a cosmological contour plot and list dataset, model, prior, and nuisance assumptions.''',
'Derive the density scaling with scale factor for a perfect fluid with constant equation-of-state parameter using the cosmological continuity equation.',
'Compare luminosity distance at redshifts 0.1, 1, and 3 for two flat cosmologies with different matter fractions; explain why a low-redshift approximation eventually fails.',
'Trace a cosmological claim from observable to likelihood and assumptions, and distinguish a fit preference from an established new component or discovery.',
'Cosmological redshift is not adequately described as every distant galaxy moving through static space with an ordinary special-relativistic recession velocity.')

C(82,'Quantum gravity and the limits of established knowledge','gravity',[79,81,74], 'tonggr tongqft preskill arxivapi',
'''Why a new description is sought: Planck scales; singularities; quantum matter in classical gravity; semiclassical regimes > Calculate the Planck length and explain why dimensional analysis does not establish an experiment’s reach.
| Effective field theory of gravity: expansion in energy; operators; renormalization; low-energy predictions > Identify which terms can be constrained at low energy without claiming a complete ultraviolet theory.
| Quantum fields in curved spacetime: observer-dependent particles; Hawking radiation; Unruh effect; backreaction > Separate a semiclassical calculation from a full quantization of spacetime.
| Competing research programs: string theory; loop approaches; asymptotic safety; causal and discrete approaches > Build a comparison matrix of assumptions, controlled results, open problems, and potential observables.
| Evidence and frontier reading: information paradox; holography; cosmological signatures; proposed tabletop tests > Audit one paper’s abstract against its assumptions and classify its main result as theorem, model calculation, simulation, proposal, or measurement.''',
'Construct Planck units from G, c, and ħ and derive the energy scaling that motivates a low-energy effective expansion, explicitly distinguishing power counting from a completed theory.',
'Write a one-page assessment of a quantum-gravity paper containing its central question, definitions, regime, result, unresolved step, and an observation that could challenge it.',
'Discuss multiple programs without presenting conjectures as established facts, and state what the selected paper actually demonstrates.',
'An elegant mathematical framework or a suggestive analogue experiment does not by itself verify a fundamental quantum theory of gravity.')

C(83,'Solid-state foundations: crystals, phonons, and bands','frontier',[7,11,68], 'tong up3 qe',
'''Crystal geometry: Bravais lattices; basis; reciprocal lattice; diffraction condition > Construct reciprocal vectors for a square lattice and label its first Brillouin zone.
| Lattice vibrations: normal modes; acoustic and optical phonons; dispersion; density of states > Derive and plot the dispersion relation of a one-dimensional monoatomic chain.
| Electrons in periodic potentials: Bloch theorem; nearly-free electrons; tight binding; band gaps > Compare a free-electron parabola with a nearest-neighbor tight-binding band.
| Occupation and response: Fermi surface; effective mass; group velocity; electrical and thermal response > Fill a simple band at zero temperature and locate occupied states and Fermi points.
| Connecting models to materials: symmetries; idealizations; defects; spectroscopy and transport > Explain which material properties a one-band model can address and which require additional orbitals or interactions.''',
'Derive a one-dimensional nearest-neighbor tight-binding dispersion and obtain group velocity and effective mass near a band extremum.',
'For a chain with stated lattice spacing and hopping energy, plot its band and density-of-states singularities; check normalization and energy units.',
'Move between real and reciprocal space, explain the origin of a band gap, and distinguish a microscopic model from a material-specific calculation.',
'A band diagram alone does not determine conductivity: occupations, scattering, disorder, contacts, and temperature also matter.')

C(84,'Semiconductors, junctions, and optoelectronic devices','frontier',[83,65,14], 'up3 tong qe',
'''Carriers and statistics: intrinsic and doped semiconductors; electron and hole densities; chemical potential; charge neutrality > Solve a simple nondegenerate carrier-density problem and state when Boltzmann statistics fail.
| Carrier motion: drift; diffusion; mobility; recombination and lifetime > Compare drift and diffusion currents for a specified electric field and density gradient.
| Junction electrostatics: p–n junction; depletion approximation; built-in potential; Poisson equation > Sketch charge, electric field, and potential profiles across an abrupt junction.
| Device operation: diode current; transistor field control; photodiodes; photovoltaic energy conversion > Separate photon absorption, charge collection, and recombination losses in a solar-cell diagram.
| Measurement and nonidealities: contact resistance; traps; leakage; temperature dependence > Fit the exponential region of a diode curve and identify where series resistance invalidates that model.''',
'Derive the depletion-width scaling of an abrupt junction from charge neutrality and Poisson’s equation, stating the one-dimensional depletion assumptions.',
'Compare calculated diode currents over two temperatures using stated model parameters, then show why extrapolating a fitted ideality factor to every bias is unjustified.',
'Connect semiconductor statistics to a measured current-voltage curve and identify at least three assumptions separating an ideal device from a real one.',
'A hole is an effective description of missing electronic occupation in a nearly filled band, not a separate elementary particle residing in the crystal.')

C(85,'Magnetism, superconductivity, and collective order','frontier',[83,65,68,76], 'tong tongstatfield up3 qutip',
'''Microscopic magnetic response: spin and orbital moments; susceptibility; diamagnetism; paramagnetism > Compare the temperature trends expected for independent moments and itinerant electrons.
| Magnetic order: exchange; Ising and Heisenberg models; ferromagnetism; antiferromagnetism > Enumerate energies of a short spin chain and compare ferro- and antiferromagnetic coupling.
| Collective excitations and domains: spin waves; anisotropy; domain walls; hysteresis > Explain why a bulk hysteresis curve needs more than an equilibrium single-domain model.
| Superconducting phenomenology: zero resistance; Meissner effect; London penetration; type-I and type-II behavior > Distinguish field expulsion from the flux behavior of an ideal perfect conductor.
| Microscopic and mesoscopic descriptions: Cooper pairing; BCS gap; Ginzburg–Landau theory; vortices and Josephson effects > Identify which superconducting observations follow from phenomenology and which require a pairing model.''',
'Derive Curie susceptibility for dilute independent spin-one-half moments in the weak-field limit, then explain why interacting magnets violate its assumptions.',
'Use a simple Ginzburg–Landau free energy to find the equilibrium order-parameter magnitude on both sides of a transition and discuss the domain of mean-field theory.',
'Separate magnetic order, superconducting phase coherence, and ideal conductivity, and connect each to a distinct measurement.',
'Zero measured resistance alone is insufficient to characterize a superconducting state; magnetic response, transition behavior, and measurement sensitivity also matter.')

C(86,'Topology, quantum Hall physics, and spin-liquid questions','frontier',[83,85,18,65], 'tong kwant tongstatfield',
'''Geometry of quantum states: adiabatic evolution; Berry connection; Berry phase; gauge dependence > Compute a spin-one-half Berry phase for a closed path on the Bloch sphere.
| Topological band models: winding number; chiral symmetry; SSH chain; bulk-boundary correspondence > Compare bulk spectra and end states for the two dimerization patterns of an open chain.
| Hall systems: Landau levels; integer quantum Hall effect; Chern number; edge transport > Relate an ideal quantized Hall plateau to occupied bands while listing finite-temperature and disorder qualifications.
| Interacting topological matter: fractionalization; emergent gauge fields; frustrated magnets; spin-liquid candidates > Compare absence of magnetic order with positive evidence required for a spin-liquid interpretation.
| Numerical and experimental tests: finite-size effects; boundary conditions; transport signatures; alternative explanations > Use a Kwant example to test how a claimed edge feature responds to disorder and symmetry-breaking perturbations.''',
'Derive the SSH Bloch Hamiltonian and its winding criterion, specifying the unit-cell convention and symmetry on which the classification depends.',
'Diagonalize an open SSH chain for several lengths, compare end-state localization and splitting, and contrast with periodic-boundary results.',
'Explain the difference between a robust topological invariant, a finite-system edge feature, and a material candidate whose interpretation remains unsettled.',
'Unusual transport or missing magnetic order does not automatically prove topological order or a quantum spin liquid; competing mechanisms must be tested.')

C(87,'Computational many-body physics and materials workflows','frontier',[83,67,68,15,14], 'qe lammps kwant scipy',
'''Choosing a model: classical versus quantum degrees of freedom; Hamiltonians; effective potentials; observable targets > Select an appropriate method for a molecular liquid, a semiconductor band gap, and an interacting spin chain.
| Small-system quantum calculations: occupation bases; exact diagonalization; sparse eigensolvers; symmetry sectors > Diagonalize a short interacting chain and verify eigenpairs with residual norms.
| Electronic-structure methods: density-functional theory; exchange-correlation approximations; pseudopotentials; plane-wave cutoffs > Use a Quantum ESPRESSO example to produce a cutoff and k-point convergence table.
| Sampling many-body systems: molecular dynamics; Monte Carlo; equilibration; autocorrelation and finite size > Estimate an effective sample size before attaching error bars to an average energy.
| Beyond introductory methods: tensor networks; quantum Monte Carlo and sign problems; excited-state corrections; reproducibility > Compare the errors each method controls and the approximations it leaves uncontrolled.''',
'Derive the Metropolis acceptance rule from detailed balance and explain why detailed balance alone does not guarantee rapid equilibration.',
'Reproduce one small public materials example while changing one convergence parameter at a time; preserve input files, software version, units, and numerical uncertainty.',
'Choose a solver according to the physical question and report statistical, discretization, finite-size, and model errors separately.',
'More computation cannot remove an incorrect Hamiltonian or exchange-correlation approximation; numerical convergence and physical accuracy are different claims.')

C(88,'Particles, interactions, and the Standard Model','frontier',[76,65,18], 'mitparticle tong cern scikithep',
'''Particle inventory and quantum numbers: leptons; quarks; gauge bosons; electric charge and flavor > Classify familiar particles by spin, charges, and interaction channels without treating hadrons as elementary.
| Symmetries and interactions: gauge groups; conserved quantities; weak chirality; strong color > Distinguish a global conservation law from a gauge redundancy in a simple example.
| Kinematics and probabilities: invariant mass; decay phase space; cross section; luminosity > Calculate an expected event count from luminosity, cross section, acceptance, and efficiency.
| Symmetry breaking and masses: Higgs field; electroweak breaking; fermion couplings; composite mass > Explain why most proton mass is not simply the sum of its quark Higgs masses.
| Experimental inference and limits: reconstructed objects; backgrounds; significance; open questions > Build an invariant-mass histogram from a CERN educational dataset and document selection effects.''',
'Derive two-body decay momentum in the parent rest frame from four-momentum conservation and identify the kinematic threshold.',
'For a hypothetical process with specified luminosity, cross section, efficiency, and background, estimate yield and explain why significance needs a statistical model.',
'Connect a particle-model prediction to a measured distribution and distinguish Standard Model successes from neutrino, dark-matter, and gravity questions beyond its minimal form.',
'Feynman diagrams are terms in a calculational expansion, not literal photographs of tiny particles following observable trajectories through each internal line.')

C(89,'Quantum field theory: fields, scattering, and effective descriptions','frontier',[74,76,18,16], 'tongqft tong mitparticle',
'''Classical fields and symmetry: action density; Euler–Lagrange equations; Noether currents; relativistic covariance > Derive the field equation and conserved energy for a real scalar field.
| Quantized free fields: mode expansion; creation and annihilation; commutators; vacuum fluctuations > Relate each Fourier mode of a scalar field to a harmonic oscillator.
| Relativistic matter and gauge fields: Dirac fields; spin and statistics; gauge redundancy; physical polarizations > Count physical photon polarizations and explain why gauge components are not additional measured particles.
| Interactions and scattering: interaction picture; time ordering; propagators; amplitudes and cross sections > Translate a low-order scalar interaction diagram into factors while declaring normalization conventions.
| Renormalization and effective theory: regulators; counterterms; running couplings; power counting > Separate a regulator-dependent intermediate expression from a matched observable and identify an expansion’s breakdown scale.''',
'Derive the Klein–Gordon equation from the scalar-field action, quantize its normal modes, and explain where positive-energy creation operators enter.',
'Work through a tree-level two-to-two scalar scattering example: specify the Lagrangian, symmetry factor, amplitude, phase space, and validity of perturbation theory.',
'Trace a simple observable from a Lagrangian through approximations to a measurable probability, keeping convention and regularization choices explicit.',
'Renormalization is not permission to arbitrarily discard infinities; parameters and operators must be defined and constrained consistently by a scheme and physical input.')

C(90,'Nuclear physics, neutrinos, and radiation measurements','frontier',[88,67,14], 'mitparticle up3 openmc nist',
'''Nuclear structure: binding energy; mass defect; liquid-drop trends; shell structure > Compute a binding energy per nucleon from stated atomic masses while handling electron-mass conventions correctly.
| Decays and reactions: exponential decay; activity; Q values; conservation and selection rules > Solve a parent-daughter decay chain and distinguish activity from absorbed dose.
| Nuclear models and transport: scattering; cross sections; mean free path; stochastic particle transport > Simulate attenuation with a stated energy-dependent cross section and compare with a uniform-slab analytic limit.
| Neutrino physics: flavor versus mass states; mixing; oscillation phases; matter effects > Plot a two-flavor vacuum survival probability against baseline at a specified energy.
| Experiments and unresolved parameters: detector response; counting backgrounds; mass ordering; absolute mass and Majorana questions > Explain what an oscillation experiment constrains and what it cannot establish about absolute masses.''',
'Derive two-flavor vacuum neutrino oscillations from the coherent evolution of mass eigenstates and state the approximations behind the result.',
'Analyze a synthetic radioactive-counting dataset with background subtraction and Poisson uncertainty; estimate half-life without handling radioactive material.',
'Distinguish nuclear energetics, event rates, dose quantities, and neutrino inference, and attach the correct units and uncertainty to each.',
'A neutrino oscillation measurement establishes mass-squared differences and mixing information; it does not by itself determine every absolute neutrino mass.')

C(91,'Plasma physics and fusion: from particle orbits to diagnostics','frontier',[76,9,10,11,14], 'plasmatext plasmapy tongfluid',
'''Recognizing a plasma: Debye screening; plasma frequency; quasineutrality; collision scales > Calculate Debye length and particles per Debye sphere for a stated density and temperature.
| Charged-particle orbits: gyration; guiding-center motion; electric drift; magnetic-moment approximation > Integrate a particle orbit in uniform crossed fields and compare drift with the analytic result.
| Fluid and kinetic descriptions: distribution functions; moments; two-fluid equations; ideal MHD > Identify the ordering assumptions needed to replace a kinetic model with an MHD model.
| Waves, instability, and transport: Alfvén waves; dispersion; Landau damping; reconnection and heat transport > Classify whether an ideal-MHD approximation can represent a specified collisionless damping mechanism.
| Fusion and evidence: confinement; Lawson reasoning; heating and losses; diagnostic inference and gain definitions > Audit a fusion paper’s input/output energy boundary and separate temperature rise, fusion yield, plasma gain, and facility gain.''',
'Derive Debye screening in the linearized electrostatic limit and the electron plasma frequency from a small collective displacement.',
'Build a parameter table for three idealized plasmas containing gyrofrequency, gyroradius, plasma frequency, Debye length, and beta; label temperature in kelvin versus energy units.',
'Choose an appropriate plasma model, check its scale ordering, and distinguish a measured heating milestone from a demonstrated net-energy claim.',
'A hotter or denser plasma, increased neutron emission, and net electrical energy production are different achievements with different measurement boundaries.')

C(92,'Stars, stellar evolution, and compact remnants','frontier',[78,81,90], 'tongcosmo up3 astropy',
'''Stellar observables: luminosity; temperature; spectra; Hertzsprung–Russell diagrams > Place a supplied sample on an HR diagram and distinguish absolute luminosity from apparent flux.
| Stellar structure: hydrostatic equilibrium; mass continuity; energy generation; radiative and convective transport > Integrate a simple hydrostatic toy model with stated equation of state and boundary conditions.
| Evolution and populations: main-sequence lifetimes; mass dependence; composition; stellar populations > Explain how age and metallicity can produce degenerate interpretations of integrated light.
| Stellar death: white dwarfs; electron degeneracy; neutron stars; supernova mechanisms > Compare the pressure support of a main-sequence star, white dwarf, and neutron star.
| Compact-object observations: pulsars; accretion; dense-matter constraints; multimessenger inference > List the model assumptions connecting a neutron-star observation to a radius or equation-of-state constraint.''',
'Derive hydrostatic equilibrium from force balance in a spherical shell and combine it with mass continuity to define a solvable stellar-structure problem.',
'Estimate an order-of-magnitude main-sequence lifetime from available nuclear energy and luminosity, then list why luminosity evolution and usable fuel fraction limit the estimate.',
'Connect a stellar observable to a physical model, explain its degeneracies, and identify which transport and equation-of-state assumptions control the inference.',
'A star’s observed color or brightness alone does not uniquely determine its mass, distance, age, or composition; extinction and other degeneracies must be addressed.')

C(93,'Galaxies and observational astrophysics','frontier',[81,92,15,14], 'astropy gwosc tongcosmo',
'''Coordinates, time, and images: celestial frames; time standards; FITS metadata; world-coordinate systems > Read a FITS header and explain the coordinate, time, and unit conventions before measuring anything.
| Imaging and photometry: point-spread function; aperture photometry; sky background; detector calibration > Measure a source with several aperture radii and quantify background and aperture-correction sensitivity.
| Spectra and velocities: wavelength calibration; redshift; line profiles; extinction > Fit a synthetic spectral line and distinguish calibration uncertainty from fit uncertainty.
| Galactic dynamics and populations: rotation curves; mass-to-light ratio; dark-matter inference; stellar populations > Compare a rotation curve with the prediction of a stated visible-matter distribution.
| Surveys and selection: flux limits; completeness; weak lensing; population and cosmological inference > Construct a toy flux-limited catalogue and demonstrate how it biases the observed luminosity distribution.''',
'Derive the inverse-square flux relation and the distance-modulus formula, identifying extinction, bandpass, and redshift qualifications.',
'Create a reproducible small astronomy notebook that records data provenance, calibrations, coordinate conventions, selections, measurements, and an uncertainty table.',
'Explain how raw detector values become an astrophysical inference and expose selection effects and calibration assumptions in the final report.',
'A catalogue is not an unbiased inventory of the universe; flux limits, masks, classification errors, and survey selection shape every population inference.')

C(94,'Fluids, geophysics, and climate as continuum systems','frontier',[9,10,11,14,15], 'tongfluid mitnum fipy fenics',
'''Continuum conservation: material derivative; mass continuity; stress tensor; Navier–Stokes equations > Derive the control-volume mass balance and distinguish Eulerian from Lagrangian descriptions.
| Flow regimes and instability: Reynolds number; viscosity; boundary layers; Rayleigh–Taylor and shear instability > Nondimensionalize a simple flow and identify which terms can be neglected in a stated regime.
| Rotating and stratified fluids: buoyancy frequency; Coriolis force; geostrophic balance; Rossby and internal waves > Estimate Rossby number for a weather system and for a sink-scale flow using realistic length scales.
| Earth and climate physics: elastic seismic waves; radiative balance; greenhouse absorption; feedback and heat transport > Compare a zero-dimensional radiation-balance model with the physical processes it omits.
| Computational and observational tests: discretization; turbulence closure; parameter estimation; climate-model and emulator validation > Run a diffusion or advection benchmark, check convergence, and explain why numerical accuracy does not establish climate predictive skill.''',
'Derive a one-box planetary energy balance from absorbed solar and emitted thermal power; linearize around equilibrium and state the assumptions behind the relaxation timescale.',
'Compare two explicit diffusion timesteps, one stable and one unstable, then conduct a spatial-refinement study and report both conservation error and solution error.',
'Use nondimensional scales to select a continuum model and distinguish weather prediction, climate statistics, observational constraints, and computational approximation.',
'Chaotic weather does not make all climate statistics unpredictable, and a skillful climate emulator within its training distribution is not automatically reliable under unfamiliar forcing.')

C(95,'Soft matter, statistical biophysics, and living systems','frontier',[13,14,68,94], 'tong tongstatfield lammps fipy',
'''Mesoscopic forces and fluctuations: thermal energy; Brownian motion; diffusion; low-Reynolds-number motion > Compare sedimentation and diffusion times for particles with two different sizes.
| Polymers and complex fluids: random walks; entropic elasticity; viscoelastic response; relaxation times > Simulate polymer random walks and test how mean-square end-to-end distance scales with segment count.
| Interfaces and self-assembly: surface tension; wetting; amphiphiles; phase separation > Compare interfacial and bulk contributions to the free energy of a simple droplet.
| Biological organization: membranes; molecular motors; reaction-diffusion; active matter > Distinguish equilibrium self-assembly from a motor-driven process that continually consumes energy.
| Linking models to experiments: microscopy; tracking; rheology; parameter identifiability > Fit a mean-square-displacement curve while testing localization noise, motion blur, drift, and limited observation time.''',
'Derive the Einstein relation connecting diffusion coefficient and mobility under equilibrium assumptions, then explain why active systems can violate the same inference.',
'Generate noisy two-dimensional Brownian trajectories, estimate diffusivity with uncertainty, and repeat after adding drift to show how an incorrect model biases the result.',
'Choose an appropriate mesoscopic model, state whether equilibrium assumptions apply, and separate biological interpretation from what the measured trajectory directly supports.',
'Random-looking biological motion need not be thermal Brownian motion; active forcing, confinement, tracking artifacts, and viscoelasticity can produce similar plots.')

C(96,'Metrology, detectors, and the design of decisive measurements','frontier',[14,65,80,93], 'nist gwosc cern astropy',
'''Defining the measurand: operational definitions; SI traceability; calibration chains; reference standards > Rewrite an imprecise measurement claim as a measurand with units, conditions, and a stated calibration reference.
| Signals and detector response: transfer functions; bandwidth; gain; efficiency and dead time > Model a detector with finite response time and calculate how it biases a rapidly varying input.
| Noise and uncertainty: counting noise; correlated drift; covariance propagation; repeated-measurement statistics > Compare averaging behavior for white noise and slowly drifting noise rather than assuming every sample is independent.
| Experimental design: controls; modulation and lock-in detection; blinding; nuisance parameters > Design a control measurement that would distinguish the proposed signal from one specific instrumental explanation.
| Reporting evidence: likelihoods; upper limits; reproducibility; systematic checks and data provenance > Produce a measurement note that includes a calibration plot, residual plot, uncertainty budget, and conditions for rejecting the interpretation.''',
'Derive linear uncertainty propagation using the Jacobian and full covariance matrix; recover the independent-error formula only as a special case.',
'Analyze a synthetic sensor calibration with correlated offset uncertainty, propagate it into a derived quantity, and show why increasing sample count cannot remove the calibration bias.',
'Specify what was measured, how the instrument responds, what could mimic the result, and which uncertainty terms improve with more data.',
'Precision, accuracy, resolution, sensitivity, and confidence are different quantities; many repeated digits do not establish an accurate or significant physical result.')
