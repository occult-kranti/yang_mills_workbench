C(37,'Electric current and DC networks','em',[36], 'up2 mitem phet',
'''Charge transport: current density; carrier density; drift speed; continuity equation > Infer the electron drift speed in a copper wire from a stated current and cross-section.|
Resistance and materials: resistivity; geometry dependence; temperature coefficient; microscopic versus lumped models > Compare equal-volume wires of different lengths and identify when constant resistance fails.|
Network laws: node potentials; Kirchhoff current law; loop equations; source internal resistance > Solve a two-loop network and verify charge conservation at every junction.|
Energy in circuits: electric power; Joule heating; source work; loading a source > Calculate where the power goes when a load is connected to a nonideal battery.|
Measurement and transients: voltmeter loading; ammeter insertion; RC charging; time constants > Predict the effect of a finite-input-resistance meter and fit a simulated capacitor charging trace.''',
'Derive I = n q A v_d for signed carrier drift, then obtain R = rho L/A from J = sigma E.',
'Analyze a 12 V source with 1 ohm internal resistance feeding 6 ohm and 3 ohm parallel loads; report terminal voltage, branch currents, and a complete power balance.',
'Solve an unfamiliar DC network, justify every current sign, and reconcile supplied power with dissipated power.',
'Current is not consumed by a resistor: charge flow is conserved while electrical energy is transferred.', 'circuit rc')

C(38,'Magnetic forces and the Biot-Savart law','em',[37], 'up2 mitem tongem',
'''Magnetic force: Lorentz force; cross products; sign of charge; force on a current segment > Draw forces for positive and negative charges moving through the same field.|
Particle trajectories: perpendicular motion; gyroradius; cyclotron frequency; helical motion > Separate parallel and perpendicular velocity and compute a nonrelativistic helix.|
Current elements: Biot-Savart integral; source-observer displacement; superposition; right-hand rule > Numerically sum the field of a discretized current loop on its axis.|
Canonical geometries: straight wire; circular loop; finite-wire corrections; symmetry axes > Derive the infinite-wire limit and quantify a finite-wire correction.|
Magnetic interactions: parallel currents; dipole moment; loop torque; force in a gradient > Compare a loop in a uniform field with one in a spatially varying field.''',
'Integrate the Biot-Savart law along an infinite straight wire to obtain B = mu0 I/(2 pi r).',
'Compute the trajectory of an electron launched obliquely into a uniform 1 mT field; explain the work done by the magnetic force and the limits of the nonrelativistic result.',
'Predict magnetic-field directions and particle trajectories, and choose between exact geometry integrals and justified approximations.',
'A magnetic force on a point charge is perpendicular to its instantaneous velocity and does no work; a complete device may also contain electric fields.', 'wire_field lorentz')

C(39,'Ampere law and magnetic matter','em',[38], 'up2 tongem feynman',
'''Integral and local laws: circulation; curl of B; enclosed current; magnetostatic assumptions > Test why an arbitrary loop does not automatically make Ampere law easy to solve.|
Symmetry-based fields: ideal solenoid; toroid; coaxial currents; exterior limits > Obtain toroid fields and compare with a long solenoid approximation.|
Magnetization: microscopic moments; magnetization density; bound volume currents; bound surface currents > Replace a uniformly magnetized cylinder with its equivalent bound currents.|
Material response: H field; susceptibility; dia- and paramagnetism; ferromagnetic domains > Distinguish B, H, and M in a simple linear material without assuming every material is linear.|
Hysteresis and energy: remanence; coercivity; saturation; magnetic boundary conditions > Interpret a measured hysteresis loop and estimate energy lost per unit volume per cycle.''',
'Use magnetostatic Ampere law to derive B = mu0 n I inside an ideal long vacuum solenoid, stating the neglected end field.',
'For a toroid with specified turns, radii, and linear permeability, calculate field variation and identify why the same calculation cannot describe a saturated core.',
'Use symmetry and material assumptions explicitly, and distinguish free current from magnetization current in boundary problems.',
'Permeability is not generally a fixed multiplier: nonlinear response, hysteresis, frequency, and geometry can matter.', 'wire_field')

C(40,'Induction, inductance, and field energy','em',[39,10], 'up2 mitem tongem',
'''Changing magnetic flux: oriented area; Faraday law; Lenz sign; induced electric circulation > Predict the voltage sign for a loop entering and leaving a magnetic region.|
Moving conductors: motional emf; magnetic force on carriers; moving circuit boundaries; energy source > Derive the emf of a sliding conducting rod and track mechanical input power.|
Inductance: flux linkage; self-inductance; mutual inductance; reciprocity > Estimate the inductance of a long solenoid from geometry.|
Inductive transients: RL step response; stored magnetic energy; continuity of current; dissipation > Solve an RL switch-on and switch-off model with physically specified current paths.|
Coupling and losses: transformer action; leakage flux; eddy currents; frequency dependence > Compare an ideal coupled-coil model with a measured frequency response.''',
'Derive the RL charging solution I(t) = (V/R)(1 - exp(-Rt/L)) and show that the magnetic energy is L I^2/2.',
'A 200-turn coil of area 0.01 m^2 sees a uniform normal field rise from 0 to 0.2 T in 0.05 s; calculate average emf and explain what extra information determines current.',
'Compute induced emf with a declared orientation and reconcile electrical output with mechanical or source energy.',
'Induction does not create energy from changing flux without an energy source; the reaction force or driving circuit is part of the balance.', 'induction transformer')

C(41,'AC circuits, resonance, and coupled oscillators','em',[40,11], 'up2 ode tesla1892',
'''Sinusoidal signals: amplitude; phase; angular frequency; RMS values > Convert a plotted sinusoid into a phasor and check peak-to-RMS factors.|
Complex impedance: resistor; inductor; capacitor; series and parallel combinations > Derive the voltage-current phase for each ideal component.|
Resonance and damping: series RLC; natural frequency; bandwidth; quality factor > Sweep frequency and compare the current maximum with the impedance minimum.|
AC power: real and reactive power; power factor; energy exchange; source loading > Calculate average power and instantaneous storage in a driven RLC circuit.|
Coupled resonators: normal-mode splitting; mutual inductance; detuning; nonideal losses > Plot two weakly coupled oscillator resonances and identify where a single-resonance model fails.''',
'Starting from the driven circuit differential equation, derive Z = R + i(omega L - 1/(omega C)) and the series resonance frequency.',
'For R = 20 ohm, L = 10 mH, C = 1 microfarad, and 5 V RMS, calculate resonance, current, phase, bandwidth, and component voltages.',
'Translate between differential equations, phasors, and resonance curves while distinguishing peak, RMS, and average quantities.',
'Large resonant voltage is not unlimited power: damping, source loading, component limits, and energy conservation constrain the response.', 'rlc oscillator')

C(42,'Maxwell equations and electromagnetic waves','em',[41,11], 'up2 tongem feynman',
'''Four field equations: electric sources; magnetic divergence; induction; displacement current > Explain the charging-capacitor inconsistency resolved by displacement current.|
Continuity and consistency: divergence identities; local charge conservation; integral versus differential forms > Derive charge continuity from Maxwell equations.|
Vacuum propagation: coupled curls; wave equation; transverse plane waves; wave speed > Show how the E and B amplitudes are related for a plane wave.|
Energy and momentum: Poynting vector; field energy density; radiation pressure; momentum flux > Calculate the pressure on absorbing and reflecting ideal surfaces.|
Interfaces and media: boundary conditions; impedance; reflection; dispersion > Derive normal-incidence reflection for a simple nonmagnetic dielectric interface.''',
'Take the curl of Faraday law in source-free vacuum and obtain the electric-field wave equation with c = 1/sqrt(mu0 epsilon0).',
'For a 1 W/m^2 vacuum plane wave, calculate RMS and peak electric and magnetic amplitudes, then explain their directions and units.',
'Connect Maxwell equations to propagation, interface behavior, and conserved energy using one consistent set of conventions.',
'The plane-wave relation E = cB is not a universal relation for static fields, near fields, or arbitrary media.')

C(43,'Retarded fields and electromagnetic radiation','em',[42], 'tongem feynman up3',
'''Finite propagation: retarded time; potentials; gauge freedom; causality > Estimate retardation across a source and decide whether the quasistatic approximation is adequate.|
Near and far zones: distance scalings; reactive fields; outgoing waves; wavelength criteria > Separate 1/r, 1/r^2, and 1/r^3 contributions in a model dipole field.|
Electric-dipole radiation: oscillating dipole; angular pattern; polarization; frequency scaling > Plot the dipole radiation pattern and locate its nodes.|
Radiated energy: angular integration; Poynting flux; nonrelativistic acceleration radiation; source back-reaction > Integrate a sin-squared angular intensity pattern over solid angle.|
Scattering and spectra: driven charges; Rayleigh regime; resonant scattering; radiation limitations > Explain the wavelength dependence of small-particle scattering and where it fails.''',
'Integrate the far-zone intensity of an oscillating electric dipole over solid angle and establish the dependence of mean radiated power on omega^4 and dipole-amplitude squared.',
'Compare otherwise identical dipoles operated at frequencies f and 2f in the dipole approximation; predict total radiated-power ratio and test the required size-to-wavelength condition.',
'Distinguish radiative from reactive fields and identify the assumptions behind a radiation or scattering approximation.',
'A strong near field does not imply equally strong power transmission to arbitrarily distant receivers.')

C(44,'Transmission lines, waveguides, and antennas','em',[43], 'tongem meep feynman',
'''Distributed circuits: per-length inductance and capacitance; telegrapher equations; characteristic impedance; propagation delay > Determine when a wire is too long to treat as a lumped connection.|
Reflection and matching: load impedance; reflection coefficient; standing waves; termination > Predict a voltage-step reflection at open, shorted, and matched line ends.|
Guided modes: conducting boundaries; TE and TM modes; cutoff frequency; group and phase velocities > Derive the lowest cutoff of an ideal rectangular vacuum waveguide.|
Antenna fundamentals: radiation resistance; gain; directivity; polarization; effective aperture > Account separately for efficiency, pattern shape, and polarization mismatch.|
Links and simulation: far-field distance; free-space link budget; bandwidth; numerical boundaries > Build a dimensioned link budget and test whether the far-field approximation holds.''',
'Apply perfect-conductor boundary conditions to a rectangular guide and obtain the TE10 cutoff frequency c/(2a).',
'For a 50 ohm line terminated in 100 ohm, calculate the voltage reflection coefficient and reflected-power fraction; contrast these with a matched line.',
'Select a lumped, transmission-line, guided-wave, or radiation model based on geometry, wavelength, and observable.',
'Phase velocity above c in a waveguide does not imply information or energy propagating faster than light.')

C(45,'Electromechanics and Tesla engineering foundations','em',[41,38], 'up2 teslamotor teslatransformer teslacontrol',
'''Force and torque: loop magnetic moment; torque; mechanical work; energy conversion > Derive the angle dependence of torque on a simple current loop.|
Rotating fields: phase-shifted windings; field-vector addition; synchronous speed; pole pairs > Animate the sum of two perpendicular sinusoidal coil fields in quadrature.|
Induction machines: rotor induction; slip; torque-speed behavior; copper and core losses > Explain why an induction motor requires nonzero slip to generate steady torque.|
Transformers and coupling: turns ratio; current ratio; leakage; saturation; nonideal regulation > Compare an ideal turns-ratio calculation with a loss-inclusive power budget.|
Control and primary sources: sensors; command encoding; switching; feedback versus teleoperation > Map the components of Tesla's remote-control patent to a modern block diagram without equating it to autonomous intelligence.''',
'Add two equal perpendicular magnetic fields oscillating a quarter-cycle apart and show that their resultant rotates with constant magnitude.',
'Read US381968A, identify the phase-shifted circuits, and annotate which functions are explained by induction, magnetic torque, and mechanical loading.',
'Explain a motor or transformer using field, circuit, and mechanical energy models, and trace a historical claim to an identified patent.',
'A patent documents a claimed invention and its specification; it is not an independent measurement of efficiency or proof of every proposed application.', 'transformer rlc')

C(46,'Computational electromagnetism','em',[42,15], 'meep fenics scipy tongem',
'''Model formulation: Poisson equation; wave equation; material properties; boundary and initial conditions > Turn a capacitor geometry into a well-posed electrostatic boundary-value problem.|
Discretization: finite differences; weak forms; finite elements; grid staggering > Implement a small 2D Poisson stencil and compare with a simple analytic solution.|
Time-domain fields: Yee-grid idea; FDTD updates; Courant stability; numerical dispersion > Derive a time-step bound for a one-dimensional vacuum discretization.|
Boundaries and sources: prescribed potentials; absorbing layers; source normalization; spurious reflections > Vary absorbing-layer thickness and quantify reflection artifacts.|
Verification and reuse: mesh refinement; conservation residuals; Meep; FEniCSx; versioned inputs > Run an existing Meep tutorial and reproduce its result before changing one physical parameter.''',
'Derive the centered finite-difference approximation to the one-dimensional Laplacian and its second-order truncation error.',
'Solve a parallel-plate electrostatic test at three grid spacings, compare against E = V/d away from edges, and distinguish discretization error from fringing physics.',
'Produce a reproducible EM calculation with boundary assumptions, convergence evidence, dimensional checks, and an analytic benchmark.',
'A smooth numerical field plot is not evidence that the grid, boundary treatment, or underlying physical model is accurate.', 'capacitor')

C(47,'Mechanical waves and acoustics','thermal',[10,11,32], 'up1 feynman scipy',
'''Traveling disturbances: displacement fields; frequency; wavelength; phase; wave speed > Read a wave snapshot and a time trace without confusing particle speed with wave speed.|
Wave dynamics: tension and inertia; wave equation; energy density; acoustic pressure > Derive the wave speed on a stretched string from a short force balance.|
Boundaries and modes: reflection; fixed/free ends; standing waves; harmonic spectra > Predict the mode frequencies of a string and open or closed air columns.|
Superposition and packets: beats; interference; dispersion; group velocity > Combine nearby frequencies and measure carrier and envelope motion numerically.|
Sound and measurement: intensity; decibels; impedance; Doppler shifts; Fourier spectra > Analyze a recorded or synthetic tone and explain why adding equal sources need not add decibels directly.''',
'Obtain the string wave equation from Newton law and derive v = sqrt(T/mu) for uniform tension and linear density.',
'Compare the fundamental and first three allowed overtones of a 0.5 m open-open tube and a 0.5 m open-closed tube using a stated sound speed.',
'Connect wave equations, boundary conditions, and measured spectra while keeping phase, group, and particle velocities distinct.',
'A wave transports energy and information without requiring its material particles to travel alongside the disturbance.', 'oscillator')

C(48,'Ray optics and optical instruments','thermal',[47], 'up3 phet opticks',
'''Geometrical limit: rays; refractive index; optical path; Fermat principle > Identify when an aperture is too small for a ray-only description.|
Reflection and refraction: Snell law; critical angle; total internal reflection; dispersion > Calculate the acceptance of a simple internal-reflection geometry.|
Images: spherical mirrors; thin lenses; sign conventions; real and virtual images > Solve one converging and one diverging lens problem with diagrams.|
Optical systems: magnification; lens combinations; matrix optics; aperture stops > Predict the image formed by two separated thin lenses.|
Instruments and limits: microscope; telescope; aberrations; resolution preview > Compare magnification with resolving power for two idealized instruments.''',
'Using paraxial refraction or ray geometry, derive 1/f = 1/d_o + 1/d_i with an explicitly stated sign convention.',
'Place an object 30 cm from a converging lens of focal length 10 cm, calculate image position and magnification, then examine the focal-plane singular case.',
'Construct and calculate images consistently and state when paraxial, thin-lens, or geometric-optics assumptions break down.',
'Higher magnification alone does not recover spatial detail that the aperture and wavelength cannot resolve.', 'lens')

C(49,'Interference, diffraction, and coherence','thermal',[48,11], 'up3 feynman meep',
'''Coherent superposition: amplitudes; phase difference; optical path; visibility > Calculate two-beam intensity for unequal amplitudes and arbitrary phase.|
Interferometers: double slit; Michelson geometry; fringe counting; path stability > Infer a small mirror displacement from a counted fringe shift.|
Diffraction integrals: Huygens-Fresnel idea; Fraunhofer limit; aperture transform; single slit > Obtain and plot the normalized sinc-squared intensity with its finite central limit.|
Multiple apertures: gratings; order conditions; angular dispersion; finite resolution > Determine allowed grating orders before calculating their positions.|
Coherence and imaging: temporal coherence; spatial coherence; point-spread function; Fourier filtering > Compare coherent and incoherent addition in a simple two-source example.''',
'Integrate a uniform slit aperture in the Fraunhofer approximation and derive the first-minimum condition a sin(theta) = lambda.',
'For 550 nm light through a 50 micrometer slit onto a screen 2 m away, compare the exact trigonometric first-minimum position with its small-angle approximation.',
'Predict fringe or diffraction structure from amplitudes and geometry, and justify coherence and far-field assumptions.',
'Intensity is proportional to squared total amplitude; adding separate intensities erases interference terms unless coherence is absent.', 'diffraction')

C(50,'Polarization and optical material response','thermal',[49,42], 'up3 tongem feynman',
'''Polarization states: transverse components; relative phase; linear; circular; elliptical > Construct field traces for three polarization states and identify handedness using a declared convention.|
Polarizers and retarders: Malus law; Jones vectors; Jones matrices; wave plates > Calculate the output of a linear polarizer followed by a quarter-wave plate.|
Statistical polarization: partially polarized light; coherency matrix; Stokes parameters; detector averages > Explain why a single Jones vector cannot represent every mixed polarization state.|
Interfaces: Fresnel coefficients; s and p components; Brewster angle; reflection phase > Calculate Brewster angle for a nonabsorbing air-glass interface.|
Anisotropic media: birefringence; optic axes; dichroism; polarization measurements > Design a sequence of analyzer settings that determines an unknown ideal polarization state.''',
'Project a linearly polarized field onto an analyzer axis and derive I = I0 cos^2(theta), stating the ideal-polarizer assumptions.',
'Track initially horizontal light through polarizers at 30 and 90 degrees and explain the result using projections rather than a particle-filter metaphor.',
'Use amplitude or statistical descriptions appropriately and predict polarization transformations through simple optical elements.',
'Circular polarization is not unpolarized light: it has a definite phase relation between transverse field components.')

C(51,'Lasers, photonics, and light-matter interaction','thermal',[50], 'up3 einradiation meep feynman',
'''Emission mechanisms: absorption; spontaneous emission; stimulated emission; Einstein coefficients > Draw rate arrows and distinguish a population from a transition rate.|
Gain and pumping: inversion; gain coefficient; two/three/four-level schemes; saturation > Explain why a simple equilibrium two-level medium cannot provide sustained population inversion.|
Optical cavities: longitudinal modes; round-trip gain; loss; threshold > Derive a threshold condition for specified mirror reflectivities and cavity length.|
Laser dynamics: coupled rate equations; relaxation behavior; linewidth; coherence > Integrate a simplified population-photon model and label its approximations.|
Photonics applications: resonators; waveguides; photonic bands; sensing; simulation > Adapt an existing Meep cavity example and test frequency convergence with resolution.''',
'Balance a cavity round trip to obtain the small-signal threshold relation exp(2gL) R1 R2 exp(-2 alpha L) = 1.',
'For a 0.1 m cavity with mirror reflectivities 0.99 and 0.95 and a stated internal loss, compute the threshold gain and explain how output coupling changes it.',
'Explain laser action as a driven gain-and-loss process and distinguish cavity modes, inversion, coherence, and useful output.',
'Stimulated emission does not supply energy without pumping; equilibrium thermal populations do not generally produce laser gain.')

C(52,'Temperature, heat, and thermal measurements','thermal',[37,47], 'up2 mitstat nist',
'''Thermal state: equilibrium; zeroth law; thermometers; temperature scales > Convert temperature intervals and absolute temperatures without mixing their offsets.|
Energy transfer: heat versus work; heat capacity; specific heat; latent heat > Construct an energy budget for warming and melting a sample.|
Expansion and response: linear expansion; volumetric expansion; constraints; thermal stress > Estimate expansion of a rod and describe why mechanical constraint changes the problem.|
Heat-transfer mechanisms: conduction; convection; radiation; emissivity; surroundings > Separate emitted radiative power from net exchange with a warm environment.|
Measurement design: calorimetry; sensor lag; calibration; systematic errors > Fit a cooling curve and identify which assumptions permit a single time constant.''',
'Derive the equilibrium temperature of two insulated bodies with constant heat capacities from conservation of energy.',
'Mix 0.2 kg of water at 80 degrees C with 0.3 kg at 20 degrees C in a calorimeter of known heat capacity; quantify the error from neglecting the container.',
'Construct thermal energy budgets with phase changes, units, and explicitly modeled surroundings.',
'Heat is energy transferred because of a temperature difference, not a substance stored inside a body.', 'thermal')

C(53,'The first law and thermodynamic processes','thermal',[52], 'up2 mitstat feynman',
'''State variables: pressure; volume; equation of state; internal energy > Distinguish an equilibrium state from the process used to reach it.|
First-law bookkeeping: work conventions; heat transfer; cyclic operation; energy balance > Translate the same piston process between two common work-sign conventions.|
Quasistatic work: pressure-volume diagrams; reversible paths; area integrals; irreversible limits > Compare work along two paths connecting identical endpoints.|
Ideal-gas processes: isothermal; isochoric; isobaric; adiabatic; heat capacities > Calculate heat and work for each process using stated gas properties.|
Real-system models: enthalpy; open versus closed systems; flow energy; nonideal equations > Identify the additional terms required for a steady-flow heater compared with a sealed vessel.''',
'For a calorically ideal gas in a reversible adiabatic process, combine the first law with pV = nRT to derive p V^gamma = constant.',
'Expand one mole of monatomic ideal gas from V to 2V once isothermally and once reversibly adiabatically; compare final temperatures, work, heat, and internal-energy change.',
'Calculate process-dependent heat and work while preserving state-function consistency and the chosen sign convention.',
'Internal energy is a state function; heat and work generally depend on the path.', 'ideal_gas')

C(54,'Entropy, the second law, and useful energy','thermal',[53], 'up2 mitstat tong',
'''Direction of processes: irreversibility; reservoirs; heat engines; Kelvin-Planck and Clausius statements > Diagnose why a proposed cyclic engine violates or respects the second law.|
Reversible benchmarks: Carnot cycle; absolute temperature; efficiency; refrigerator performance > Compute maximum engine efficiency and distinguish it from refrigerator coefficient of performance.|
Entropy as a state function: reversible heat integral; entropy changes; entropy generation; mixing > Calculate the entropy change of two bodies reaching thermal equilibrium.|
Free energies: Helmholtz energy; Gibbs energy; constrained equilibrium; chemical-potential preview > Choose the potential appropriate to fixed T,V or fixed T,p.|
Availability and limits: finite reservoirs; exergy idea; dissipation; local decreases versus total change > Explain how a refrigerator lowers one subsystem's entropy while the combined entropy increases.''',
'Use a reversible Carnot cycle to derive eta_max = 1 - T_c/T_h and relate reversible heat exchanges to entropy balance.',
'Compare an engine working between 600 K and 300 K with a proposed 70 percent-efficient device; compute the entropy balance for a stated heat input.',
'Apply entropy balance to a complete system and distinguish reversibility, equilibrium, energy conservation, and useful work.',
'The second law does not forbid local entropy decreases; it constrains total entropy production for the complete isolated system.')

C(55,'Kinetic theory and molecular transport','thermal',[54,32], 'up2 mitstat lammps',
'''Microscopic gas model: molecular velocities; collision assumptions; momentum flux; ideal-gas pressure > Derive pressure from particles colliding elastically with a wall.|
Velocity distributions: Maxwell-Boltzmann distribution; most probable speed; mean speed; RMS speed > Compare the three characteristic speeds for nitrogen at a stated temperature.|
Energy and equipartition: quadratic degrees of freedom; molecular rotation; heat capacities; classical limits > Predict classical heat capacities and identify temperatures where the prediction can fail.|
Collisions and paths: collision cross-section; mean free path; collision time; Knudsen number > Decide whether a rarefied gas requires a kinetic description.|
Transport estimates: diffusion; viscosity; thermal conductivity; random-walk scaling > Estimate a diffusion coefficient from thermal speed and mean free path and assess its uncertainty.''',
'Derive p = n_number m mean(v^2)/3 from isotropic momentum transfer and combine it with equipartition to recover the ideal-gas law.',
'Compute the RMS speed and an estimated mean free path for a gas using supplied molecular mass, diameter, pressure, and temperature; state where the hard-sphere approximation enters.',
'Connect microscopic distributions and collisions to macroscopic pressure and transport without confusing density conventions.',
'At a fixed temperature molecules do not all have the same speed; temperature constrains a distribution.', 'ideal_gas')

C(56,'Statistical ensembles and partition functions','thermal',[55,7], 'mitstat prob tong',
'''Counting states: multiplicity; microstates and macrostates; entropy; probability weights > Count a small two-level system exactly and compare likely macrostates.|
Microcanonical ensemble: fixed energy; accessible states; entropy derivatives; reservoir argument > Show how a small subsystem acquires Boltzmann weights when coupled to a large reservoir.|
Canonical ensemble: partition function; free energy; mean energy; energy fluctuations > Calculate all thermodynamic quantities of a two-state spin in a field.|
Grand canonical ensemble: particle exchange; chemical potential; number fluctuations; grand potential > Derive the probability ratio between states differing by one particle.|
Ensemble equivalence and computation: thermodynamic limit; finite-size effects; sampling; autocorrelation > Compare exact enumeration with Monte Carlo estimates for a small spin model.''',
'Differentiate ln Z with respect to beta to obtain mean energy and the energy variance, then relate the variance to heat capacity.',
'For N independent spins with energies plus or minus mu B, derive partition function, magnetization, and heat capacity and test the high-temperature limit.',
'Choose an ensemble from physical constraints and obtain observables and fluctuations from the appropriate partition function.',
'Different ensembles need not agree for every finite system or every observable; equivalence requires suitable limiting conditions.')

C(57,'Quantum statistics and collective quantum gases','thermal',[56], 'mitstat einbose up3',
'''Quantum state occupancy: indistinguishability; occupation numbers; bosonic and fermionic rules; classical dilution > Compare counting arrangements of distinguishable particles, bosons, and fermions.|
Distribution functions: Bose-Einstein; Fermi-Dirac; Maxwell-Boltzmann limit; chemical potential > Plot occupation versus energy and identify the dilute classical regime.|
Density of states: box quantization; momentum-space counting; dimensional dependence; continuum limit > Derive the three-dimensional free-particle density of states with spin degeneracy explicit.|
Fermion gases: Fermi energy; degeneracy pressure; low-temperature excitations; electron heat capacity > Estimate the Fermi temperature from an electron number density.|
Bosons and radiation: Planck spectrum; photon chemical potential; Einstein solid; Bose condensation > Explain which assumptions permit Bose-Einstein condensation in the ideal homogeneous gas.''',
'Sum the allowed occupation numbers of one mode in the grand canonical ensemble to obtain Bose-Einstein and Fermi-Dirac mean occupancies.',
'Compare thermal energy with Fermi energy for a supplied electron density, and determine whether Maxwell-Boltzmann statistics is an adequate approximation.',
'Select the correct statistics and density of states, explain degeneracy, and identify ideal-gas assumptions behind condensation claims.',
'Bose condensation and superconductivity are not interchangeable names; interactions, charge, and the relevant ordered state must be specified.', 'thermal ideal_gas')

C(58,'Phase transitions and critical phenomena','thermal',[57,15], 'tongstatfield mitstat lammps',
'''Phases and order: order parameters; broken symmetry; coexistence; first- and continuous transitions > Identify appropriate order parameters for a magnet and a liquid-gas system.|
Landau description: free-energy expansion; stability; minima; response and metastability > Minimize a quartic free energy and track its minima across a transition.|
Ising models: lattice Hamiltonian; partition sum; mean field; domain walls > Compare exact enumeration of a small lattice with a mean-field prediction.|
Critical behavior: correlation length; susceptibility; critical exponents; scaling > Fit a power law over several windows and show how finite-size effects bias an exponent.|
Renormalization and simulation: coarse graining; universality; finite-size scaling; autocorrelation > Reproduce a Binder-cumulant crossing using several lattice sizes and independent runs.''',
'Minimize f(m) = a(T-T_c)m^2/2 + b m^4/4 for b positive and derive the mean-field order-parameter exponent.',
'Simulate a small 2D Ising model with Metropolis updates; report thermalization, autocorrelation, uncertainty, and the difference between finite-size rounding and a true thermodynamic singularity.',
'Explain a transition through symmetry, fluctuations, and scale dependence, supported by finite-size and sampling diagnostics.',
'A sharp-looking curve from one small simulation is not sufficient evidence of a thermodynamic phase transition.')

C(59,'Transport, fluctuations, and nonequilibrium physics','thermal',[58,11,15], 'tongfluid fipy scipy mitstat',
'''Conservation equations: local balance; currents; constitutive relations; boundary fluxes > Derive a diffusion equation from particle conservation and Fick law.|
Stochastic dynamics: random walks; Langevin force; fluctuation-dissipation; Fokker-Planck equation > Simulate Brownian trajectories and compare mean-square displacement with an analytic limit.|
Linear response: perturbation and response; correlation functions; Green-Kubo idea; response times > Estimate a response coefficient from a simulated equilibrium correlation function.|
Driven systems: steady states; detailed-balance violation; entropy production; currents > Compare equilibrium and driven hopping models with identical state spaces.|
Research diagnostics: rare events; coarse-graining; time correlations; numerical and model uncertainty > Repeat a transport estimate over time steps and observation windows and explain the remaining uncertainty.''',
'Derive mean-square displacement equal to 2Dt in one dimension from the diffusion equation with a localized initial condition.',
'Generate Brownian trajectories at three time steps, estimate D from an ensemble, and compare the result with fitting one long trajectory; report uncertainty and correlation assumptions.',
'Formulate a transport problem from conservation and constitutive laws, then distinguish equilibrium fluctuations from driven currents.',
'A nonequilibrium steady state can have time-independent averages while sustaining currents and positive entropy production.')

C(60,'Experimental origins of quantum physics','quantum',[49,57], 'mitqm up3 ein1905 einlight einbrown',
'''Thermal radiation: blackbody observations; classical ultraviolet failure; Planck hypothesis; domain of models > Compare classical and Planck spectral shapes at low and high frequencies.|
Light quanta: photoelectric threshold; stopping potential; intensity and frequency; Einstein argument > Extract a work function and Planck constant from a synthetic stopping-potential dataset.|
Matter and atoms: Brownian motion; atomic evidence; spectral lines; Rutherford scattering > Explain which observations support molecular reality and which probe atomic structure.|
Wave-particle experiments: Compton shift; de Broglie wavelength; electron diffraction; detection events > Calculate a matter wavelength and compare it with a lattice spacing.|
Historical reasoning: Bohr model; correspondence principle; successes and failures; primary-paper context > Build a table separating each early model's successful prediction from its unresolved contradiction.''',
'Use energy conservation in the single-photon photoelectric model to derive e V_stop = h f - phi above threshold.',
'For wavelengths 300, 400, and 600 nm incident on a material with a 2.5 eV work function, determine emission thresholds and maximum kinetic energies without treating subthreshold zero as an emitted electron.',
'Explain why distinct experiments required changes to classical models and distinguish their measured observables from later interpretations.',
'Increasing intensity below a one-photon photoelectric threshold does not raise an individual photon energy; multiphoton physics is a different regime.', 'photon de_broglie thermal')

C(61,'States, operators, and the Born rule','quantum',[60,7], 'mitqm linear preskill',
'''State vectors: complex amplitudes; normalization; global phase; basis changes > Normalize a two-component state and identify physically irrelevant global phase.|
Observables: Hermitian matrices; eigenstates; spectral decomposition; compatible measurements > Diagonalize a two-level observable and interpret its eigenvalues.|
Probabilities: Born rule; projectors; expectation values; variance > Predict outcome frequencies in two different measurement bases.|
Operator algebra: commutators; uncertainty relations; unitary transformations; generators > Calculate Pauli-matrix commutators and test an uncertainty relation for a chosen state.|
Composite systems: tensor products; product states; entanglement preview; measurement records > Construct a two-qubit basis and distinguish coherent superposition from classical random preparation.''',
'Expand a normalized state in an observable eigenbasis to derive its expectation as the probability-weighted sum of eigenvalues.',
'For the state (sqrt(3)/2, i/2), calculate sigma_z and sigma_x outcome probabilities, expectations, and variances, showing every basis transformation.',
'Translate a state and observable into probabilities with correct normalization, units, and basis conventions.',
'A state-vector component is a probability amplitude, generally complex; its squared magnitude supplies a probability.')

C(62,'Schrodinger dynamics and probability conservation','quantum',[61,10,11], 'mitqm scipy sympy',
'''Wavefunctions: position representation; square integrability; boundary conditions; probability density > Normalize a continuous wavefunction and check physical dimensions.|
Time evolution: Hamiltonian; time-dependent Schrodinger equation; unitary propagator; stationary states > Evolve a superposition of two energy eigenstates and identify changing interference terms.|
Probability flow: continuity equation; probability current; flux; boundary conservation > Compute the current of a plane wave and a real bound-state eigenfunction.|
Free wave packets: dispersion relation; Fourier representation; spreading; classical correspondence > Propagate a Gaussian packet and compare center motion with its spreading.|
Numerical dynamics: finite differences; spectral methods; stable stepping; norm and energy checks > Compare an analytic solution with a numerical propagator at several resolutions.''',
'Combine the Schrodinger equation with its complex conjugate to derive the probability continuity equation and current for a real scalar potential.',
'Propagate a Gaussian free-particle packet, verify norm conservation, measure its center and width, and distinguish boundary artifacts from physical spreading.',
'Solve or simulate a simple quantum evolution while verifying normalization, probability flux, and relevant conservation laws.',
'A stationary energy eigenstate may have a time-dependent overall phase while its probability density remains unchanged.', 'quantum_well')

C(63,'Wells, scattering, and quantum tunneling','quantum',[62], 'mitqm up3 scipy',
'''Hard-wall confinement: allowed eigenfunctions; discrete energies; normalization; node counting > Derive the first three infinite-well states and compare energy spacings.|
Finite confinement: matching conditions; evanescent tails; parity; number of bound states > Solve a finite-well eigenvalue condition graphically or numerically.|
Potential steps: incident and reflected amplitudes; transmission; current ratios; threshold cases > Show why transmission probability needs a velocity factor when asymptotic potentials differ.|
Barrier tunneling: exact rectangular barrier; exponential limits; resonance; flux conservation > Sweep barrier width and identify the regime of approximately exponential transmission.|
Wave-packet scattering: packet versus plane-wave descriptions; dwell behavior; energy bandwidth; interpretation limits > Compare stationary transmission with the transmitted norm of a narrow-band packet.''',
'Apply zero-wavefunction boundary conditions to a one-dimensional infinite well to obtain E_n = n^2 h^2/(8mL^2).',
'Compute electron energy levels in a 1 nm well, then replace the hard walls by finite barriers and explain qualitatively and numerically how the low-energy states change.',
'Match wavefunctions and appropriate derivatives, compute flux-based reflection/transmission, and identify the assumptions behind tunneling approximations.',
'A nonzero wavefunction inside a barrier does not by itself give the transmission probability; probability current and boundary conditions matter.', 'quantum_well de_broglie')

C(64,'The quantum harmonic oscillator','quantum',[63,7], 'mitqm qutip feynman',
'''Quadratic Hamiltonian: equilibrium expansion; oscillator scales; dimensionless variables; normalizability > Identify the oscillator length and energy scales for a specified mass and frequency.|
Ladder operators: commutators; ground state; raising and lowering; number operator > Construct the first few states algebraically and check their normalization.|
Wavefunctions and uncertainty: Hermite structure; nodes; position/momentum variances; zero-point energy > Plot densities and compare classical turning points with quantum tails.|
Coherent dynamics: coherent states; displacement; classical motion of means; phase-space picture > Use QuTiP to follow a coherent state and compare its mean trajectory with a classical oscillator.|
Perturbations and applications: weak anharmonicity; coupled modes; phonon preview; numerical truncation > Increase a truncated basis until an anharmonic energy correction converges.''',
'Factor the oscillator Hamiltonian with ladder operators to derive E_n = hbar omega(n + 1/2) and the ground-state uncertainty product.',
'Compare ground, first-excited, and coherent states through energy, position variance, and time evolution; test numerical basis truncation rather than trusting a single cutoff.',
'Use algebraic and coordinate descriptions consistently and distinguish zero-point fluctuations from a classical particle trajectory.',
'Zero-point energy is not automatically extractable cyclic work from an equilibrium ground state.', 'oscillator')

C(65,'Angular momentum and intrinsic spin','quantum',[64,7], 'mitqm tong qutip',
'''Rotations and generators: angular-momentum commutators; eigenvalues; ladder operations; measurement axes > Derive allowed magnetic quantum numbers for a chosen angular momentum.|
Orbital angular momentum: spherical coordinates; spherical harmonics; L squared; parity > Plot angular densities for low-order spherical harmonics.|
Spin one-half: Pauli matrices; Stern-Gerlach sequences; spinors; Bloch-sphere coordinates > Predict a three-analyzer spin sequence using matrix products.|
Addition of angular momentum: product basis; coupled basis; singlet/triplet states; Clebsch-Gordan structure > Construct two-spin singlet and triplet states and verify total-spin eigenvalues.|
Magnetic dynamics: Zeeman Hamiltonian; Larmor precession; resonance; spin-orbit preview > Evolve a spin initially transverse to a magnetic field and calculate measured expectations.''',
'Use angular-momentum commutators and ladder-operator norms to derive m = -j,...,j and J squared = hbar squared j(j+1).',
'Prepare a spin-up z state, rotate the measurement axis through an angle theta, and compute both outcome probabilities and their experimental frequency interpretation.',
'Calculate spin and orbital measurement outcomes, combine two angular momenta, and state the chosen basis and magnetic conventions.',
'Electron spin is intrinsic angular momentum and is not a literal classical sphere rotating about its axis.', 'lorentz')

C(66,'Hydrogen, spectra, and atomic structure','quantum',[65], 'mitqm up3 nist',
'''Central potentials: separation of variables; radial equation; reduced mass; effective centrifugal term > Derive the radial equation from the three-dimensional Schrodinger equation.|
Hydrogen states: principal/orbital/magnetic numbers; energy degeneracy; radial nodes; orbital densities > Distinguish radial probability from local probability density for a 1s state.|
Transitions and spectra: energy differences; dipole matrix elements; selection rules; emitted frequency > Calculate a hydrogen transition wavelength and test whether it is electric-dipole allowed.|
Corrections: fine structure; spin-orbit interaction; hyperfine structure; Lamb-shift context > Rank correction scales and distinguish a correction model from a new quantum number.|
Beyond one electron: screening; effective charge; Pauli principle preview; periodic structure > Compare hydrogenic and screened orbital estimates while identifying the missing electron correlations.''',
'Obtain the hydrogenic bound-state energy dependence on reduced mass and 1/n squared, with the Coulomb coupling and SI constants explicit.',
'Calculate the n = 3 to n = 2 hydrogen wavelength using reduced mass, compare it with the infinite-nuclear-mass approximation, and identify which orbital transitions are allowed.',
'Relate quantum numbers and wavefunctions to atomic spectra while separating leading predictions from relativistic and radiative corrections.',
'An atomic orbital is a quantum state or its spatial representation, not a sharply defined planetary orbit.', 'photon')

C(67,'Approximation methods in quantum mechanics','quantum',[66,15], 'tong mitqm scipy sympy',
'''Stationary perturbation: small parameters; first-order energies; wavefunction corrections; breakdown near degeneracy > Calculate a weak quartic oscillator correction and estimate its validity range.|
Degenerate perturbation: subspace restriction; matrix diagonalization; level splitting; symmetry > Resolve a twofold degeneracy before applying perturbation theory.|
Variational methods: trial states; normalization; energy functional; upper-bound property > Optimize a one-parameter trial state and compare with an exact ground energy.|
Semiclassical methods: WKB action; turning points; connection rules; tunneling exponent > Compare a WKB barrier estimate with an exact rectangular-barrier solution away from turning-point singularities.|
Time-dependent methods: transition amplitudes; resonance; Fermi golden rule; adiabatic conditions > Compare weak-drive perturbation with exact two-level Rabi dynamics.''',
'Expand the eigenvalue equation to first order in a weak perturbation and derive the nondegenerate energy shift as its unperturbed-state expectation.',
'Apply both a variational estimate and first-order perturbation theory to an anharmonic oscillator, compare their domains, and verify selected points by matrix diagonalization.',
'Choose an approximation using an identified expansion parameter and validate it against an exact limit or controlled numerical calculation.',
'A variational energy bound does not guarantee equally accurate wavefunctions or every other observable.')

C(68,'Identical particles and many-body quantum language','quantum',[67,57], 'tong preskill qutip',
'''Exchange symmetry: symmetric/antisymmetric states; indistinguishability; Pauli exclusion; exchange versus force > Antisymmetrize two orbitals and show when the resulting state vanishes.|
Many-particle bases: Slater determinants; occupation notation; basis growth; conserved particle number > Count the dimension of a fixed-particle-number fermionic Hilbert space.|
Second quantization: creation/annihilation; commutators and anticommutators; number operators; field operators > Construct small bosonic and fermionic operator matrices and verify their algebra in the valid subspace.|
Interactions: one-body and two-body terms; Hubbard model; mean-field ideas; correlation > Build a two-site Hubbard Hamiltonian and compare noninteracting with interacting spectra.|
Computational approaches: exact diagonalization; truncation; tensor-network motivation; symmetry reduction > Benchmark a tiny many-body problem before increasing system size.''',
'Construct a normalized two-fermion Slater determinant and demonstrate the exclusion of two particles from the same one-particle state.',
'Diagonalize the two-site spinful Hubbard model at half filling across several U/t values and relate energy changes to double occupancy and spin correlations.',
'Translate between particle wavefunctions and occupation-space operators and identify both physical approximations and computational truncations.',
'Exchange effects follow from state symmetry and are not an additional classical repulsive force between identical fermions.')

C(69,'Entanglement, EPR, and Bell tests','quantum',[68,61], 'epr preskill ibmlearn qiskit',
'''Composite states: separability; Schmidt decomposition; reduced states; entanglement entropy > Compute the reduced state of a Bell pair and compare it with the pure joint state.|
EPR reasoning: original assumptions; prediction with certainty; completeness; locality questions > Annotate the EPR argument without attributing later Bell inequalities to the 1935 paper.|
Bell and CHSH: local hidden-variable models; correlation functions; classical bound; quantum predictions > Derive the CHSH bound and calculate the singlet prediction for chosen analyzer angles.|
Experimental inference: measurement settings; detection; locality; freedom-of-choice assumptions; statistical uncertainty > Simulate finite samples and report an uncertainty interval for the CHSH statistic.|
No-signaling and interpretation: marginal probabilities; classical communication; loopholes; interpretations versus observations > Verify that local measurement choices do not alter the remote unconditioned outcome distribution.''',
'For predetermined plus-or-minus-one local outcomes, derive the CHSH absolute bound of 2 and compare it with the quantum value 2 sqrt(2).',
'Simulate a Bell-pair experiment with adjustable depolarizing noise and finite shots; identify the noise level at which the chosen CHSH witness ceases to violate its bound.',
'Explain exactly which assumptions a Bell inequality tests and distinguish entanglement, correlation, postselection, and usable communication.',
'Entanglement correlations do not provide controllable faster-than-light signaling; conditioned correlations require comparison of classical records.')

C(70,'Open quantum systems and decoherence','quantum',[69,10], 'qutip preskill scipy',
'''Mixed-state description: density operators; positivity; trace; partial trace; ensembles > Compare a coherent superposition and a mixture with identical diagonal populations.|
Quantum channels: Kraus operators; trace preservation; amplitude damping; dephasing > Verify the completeness condition of a simple channel and evolve a state.|
Master equations: unitary and dissipative terms; Lindblad form; Markov assumption; bath approximations > Derive population and coherence equations for a damped two-level system.|
Noise characterization: T1; T2; pure dephasing; spectra; non-Markovian warnings > Fit simulated relaxation and Ramsey traces without imposing T2 = T1.|
Simulation and validation: QuTiP solvers; collapse operators; positivity checks; basis and time convergence > Reproduce an official open-system tutorial and test norm/trace, limiting cases, and solver tolerances.''',
'Solve a two-level amplitude-damping master equation to obtain exponential excited-state decay and the associated coherence decay.',
'Simulate driven Rabi oscillations with independent relaxation and dephasing rates; recover undamped motion when both rates vanish and estimate which rate suppresses the observed contrast.',
'Build a physically valid reduced-system model, state its bath assumptions, and verify trace, positivity, and known limits.',
'A density matrix can describe classical preparation uncertainty or entanglement with an environment; its mixedness does not uniquely identify the cause.')

C(71,'Atomic, molecular, and optical quantum research','quantum',[70,51], 'qutip mitqm feynman meep',
'''Atom-light coupling: dipole Hamiltonian; selection rules; rotating frame; rotating-wave approximation > Derive a resonant two-level effective Hamiltonian and state when counter-rotating terms matter.|
Coherent control: Rabi pulses; Ramsey interferometry; detuning; pulse errors > Compare a pi pulse and two pi-over-two pulses with a controlled delay.|
Cooling and trapping: Doppler cooling; recoil; optical dipole forces; magnetic and optical traps > Compare thermal, recoil, and trap energy scales using supplied parameters.|
Programmable atoms: optical lattices; tweezers; Hubbard parameters; Rydberg interactions > Identify which optical control parameters change local energies, hopping, or interactions in a simulator.|
Sensing and validation: atom interferometer phase; shot noise; technical noise; systematic shifts > Construct a simulated interferometer sensitivity budget and connect each term to an experimental observable.''',
'Solve resonant two-level dynamics to obtain the sin-squared Rabi excitation probability and derive pulse areas for inversion and equal superposition.',
'Reproduce a Ramsey fringe with QuTiP, add detuning and dephasing separately, and report how fringe spacing, phase, and contrast distinguish the effects.',
'Read an AMO paper by separating apparatus specifications, demonstrated quantum observables, numerical proposals, and unresolved systematics.',
'A precise quantum sensor is not automatically limited only by quantum shot noise; calibration and technical noise can dominate.')

C(72,'Quantum information and computation','quantum',[71,69], 'preskill ibmlearn qiskit',
'''Circuit model: one- and two-qubit gates; measurement; classical control; universal gate sets > Convert a short matrix calculation into an equivalent circuit.|
Information protocols: teleportation; superdense coding; communication costs; no-cloning > Track both quantum and classical resources through a teleportation protocol.|
Algorithm principles: interference; phase kickback; Fourier transform; amplitude amplification > Implement a small phase-estimation example and explain the information in each register.|
Noise and resource costs: sampling error; circuit depth; connectivity; compilation; error mitigation > Compare logical circuit gates with the compiled physical gate count.|
Reproducible experiments: statevector versus shot simulation; seeds; classical baselines; optional hardware > Reproduce a Qiskit tutorial locally and include a classical baseline and complete execution settings.''',
'Prove the no-cloning result by applying inner-product preservation of a hypothetical unitary copier to two nonorthogonal states.',
'Implement three-qubit teleportation, verify several distinct input states, include classical feed-forward, and explain why the protocol does not transmit information before the classical bits arrive.',
'Explain an algorithm through state evolution and measurement, and report resource and noise assumptions alongside any performance claim.',
'Quantum algorithms do not reveal every component of a superposition in one measurement; useful speedups require structured interference and suitable output tasks.')

C(73,'Quantum error correction and fault tolerance','quantum',[72], 'preskill qiskit qutip',
'''Noise and redundancy: bit flips; phase flips; coherent errors; encoding; error detection > Show why classical repetition alone does not protect an arbitrary qubit from all Pauli errors.|
Stabilizer codes: Pauli groups; commuting checks; syndrome; logical operators; code distance > Enumerate syndromes of a small code and identify undetectable logical operations.|
Repeated correction: syndrome extraction circuits; measurement faults; decoding; leakage and loss > Simulate multiple rounds with data and measurement errors rather than a perfect decoder oracle.|
Fault tolerance: propagated faults; thresholds; physical/logical error rates; resource overhead > Distinguish a one-round improvement from an asymptotic threshold claim.|
Research architectures: surface and toric codes; LDPC connectivity; neutral-atom rearrangement; decoder latency > Compare an experimental memory result with a simulated high-rate-code proposal using matched claim categories.''',
'Derive the independent-bit-flip logical failure probability 3p^2 - 2p^3 for a three-bit repetition code with ideal majority decoding.',
'Simulate repetition-code memory curves with and without measurement noise, report confidence intervals, and explain why this does not demonstrate full quantum fault tolerance.',
'Evaluate a QEC claim using its noise model, code distance, cycle count, decoder assumptions, logical task, and complete resource overhead.',
'An extrapolated tiny logical error rate under a selected noise model is not the same evidence as observing that error rate on hardware.')

C(74,'From quantum mechanics to quantum field theory','quantum',[73,68,29,30], 'tongqft tong preskill',
'''Why fields: variable particle number; locality; classical fields; continuum normal modes > Explain why a fixed-particle Schrodinger description is insufficient for particle creation processes.|
Classical field dynamics: Lagrangian density; Euler-Lagrange equations; Noether currents; stress-energy idea > Derive the classical scalar-field equation from an action.|
Quantization bridge: oscillator modes; canonical commutators; creation/annihilation; vacuum correlations > Quantize a finite set of scalar modes before considering the continuum limit.|
Interactions and predictions: perturbative expansion; propagators; scattering amplitudes; observable cross sections > Identify the external states, approximation order, and observable in a simple scattering calculation.|
Effective theories and limits: regularization versus renormalization; energy scales; gauge symmetry preview; relativistic prerequisites > Write a prerequisite plan for graduate QFT and label which conclusions require special relativity beyond this bridge.''',
'Apply the Euler-Lagrange field equation to a real scalar Lagrangian with quadratic kinetic and mass terms, then connect each Fourier mode to a harmonic oscillator.',
'Discretize a free scalar field on a short periodic chain, diagonalize its normal modes, and compare the small-momentum dispersion with the continuum prediction.',
'Translate between particles, field modes, actions, and observables, while recognizing that this bridge precedes a complete relativistic QFT course.',
'Virtual particles in a perturbative diagram are internal mathematical contributions, not directly detected little objects borrowing energy from a violated conservation law.')
