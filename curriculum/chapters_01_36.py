C(1,'Arithmetic, proportional reasoning, and scientific notation','math',[], 'math',
'''Number sense:Signed numbers and absolute value;Order of operations;Fractions and equivalent ratios>Evaluate a mixed fraction expression by hand and explain each sign change.
|Proportions:Decimal and percentage conversion;Direct and inverse proportionality;Rates and scale factors>Scale a recipe-like measurement table and distinguish doubling a length from doubling an area.
|Powers and roots:Integer exponent laws;Square roots and fractional powers;Orders of magnitude>Compare the sizes of 10^-6 and 10^-9 without a calculator.
|Scientific notation:Normalized mantissas;Arithmetic with exponent notation;Significant digits versus exact counts>Compute a distance from a speed and duration while retaining guard digits.
|Quantitative estimation:Bounds and approximations;Fermi estimates;Checking plausible magnitude>Estimate the number of seconds in a human lifetime and state the assumed lifetime.''',
'Derive the exponent rules for multiplying and dividing powers by expanding small integer examples, then extend them consistently to zero and negative exponents.',
'Complete a twenty-question mixed set of signed arithmetic, fractions, percentages, rates, and powers; annotate the order-of-magnitude check for every physical quantity.',
'Score at least 18/20, correct the remaining errors, and explain why a percentage increase followed by the same percentage decrease does not restore the original value.',
'More displayed decimal digits do not mean a measurement or estimate contains more information.')

C(2,'Algebra, functions, and mathematical models','math',[1], 'math',
'''Symbols and equations:Variables and parameters;Equality-preserving operations;Linear equations and inequalities>Solve for an unknown on both sides and check by substitution.
|Polynomial models:Factoring and expansion;Quadratic roots and discriminants;Rational expressions and excluded inputs>Find every real root of a quadratic and identify a denominator that cannot vanish.
|Functions as mappings:Domain and range;Composition and inverse functions;Graphs and intercepts>Sketch a piecewise motion-like function and state its allowed input interval.
|Exponential and logarithmic models:Growth and decay factors;Logarithm laws;Linearizing exponential relationships>Find how many repeated halvings reduce a quantity to one eighth of its initial value.
|Model interpretation:Parameters with dimensions;Sensitivity to parameter changes;Interpolation versus extrapolation>Fit a straight line to two points and explain why it may fail outside their range.''',
'Starting from y = a exp(bx), isolate x using logarithms and derive the constant interval needed for the value to double when b is positive.',
'Build a handwritten model sheet for linear growth, inverse proportionality, quadratic variation, and exponential decay, including a graph, domain, parameter meanings, and one solved inverse problem each.',
'Rearrange five unfamiliar formulas without changing their domains and explain the physical meaning of a slope, an intercept, and a dimensionless logarithm argument.',
'An algebraically produced root is not automatically admissible; excluded inputs and extraneous roots must be checked in the original equation.')

C(3,'Geometry, trigonometry, and spatial reasoning','math',[2], 'math up1',
'''Euclidean geometry:Similar triangles;Pythagorean theorem;Areas and volumes>Recover an inaccessible height from a measured baseline and a triangle diagram.
|Angles and circles:Degrees and radians;Arc length and sector area;Angular versus linear displacement>Convert an angle to radians before computing the length of a circular arc.
|Trigonometric functions:Unit-circle sine and cosine;Tangent and inverse functions;Quadrants and periodicity>Find both angles in one revolution having a specified positive sine.
|Trigonometric relations:Addition formulas;Double-angle identities;Small-angle approximations>Compare sin(theta) with theta at several angles and report relative error.
|Coordinate geometry:Lines and distances;Circles and conic sections;Polar and Cartesian coordinates>Convert an ellipse sketch and a set of polar points into Cartesian descriptions.''',
'Derive the sine and cosine addition formulas using a rotated unit vector, then obtain the double-angle identities as a special case.',
'Analyze a triangle, a circular arc, and an ellipse from labeled diagrams; include units, branch choices for inverse trigonometric functions, and a numerical small-angle error table.',
'Resolve an angle into consistent sine and cosine components in all four quadrants and state an explicit angular range for a chosen small-angle accuracy.',
'Angles expressed in degrees cannot be inserted unchanged into formulas or approximations that assume radians.')

C(4,'Units, dimensions, vectors, and coordinate systems','math',[3], 'up1 nist math',
'''Physical quantities:SI base and derived units;Prefixes and conversion chains;Exact constants versus measured constants>Convert a speed through a dimensional conversion chain and identify which factors are exact.
|Dimensional reasoning:Dimension vectors;Homogeneous equations;Dimensionless combinations>Reject an equation that adds a length to a speed, then repair its dimensions with a time scale.
|Vector algebra:Components and basis vectors;Vector addition and magnitude;Unit vectors and projections>Resolve two displacements into components and reconstruct their resultant.
|Vector products:Dot product and angles;Cross product and orientation;Scalar and vector triple products>Calculate the area and oriented normal of a parallelogram from two edge vectors.
|Coordinate choices:Cartesian and polar bases;Cylindrical and spherical coordinates;Coordinate components versus physical vectors>Express one displacement in two rotated bases and confirm its length is unchanged.''',
'Derive the dot-product component formula from orthonormal basis vectors and show that an orthogonal coordinate rotation preserves vector length.',
'Create a units-and-vectors notebook covering six conversions, three dimensional checks, and force-like vector sums in two and three dimensions; verify one result in a rotated basis.',
'Distinguish units from dimensions and scalar quantities from vector components, then solve a three-vector addition problem without mixing coordinate bases.',
'Dimensional consistency is necessary but cannot determine a missing dimensionless coefficient or prove a proposed physical law.')

C(5,'Differential calculus: limits, rates, and approximation','math',[2,3], 'calculus math sympy',
'''Limits and continuity:One-sided limits;Continuous and discontinuous functions;Difference quotients>Estimate a derivative using shrinking positive and negative steps.
|Differentiation rules:Power and product rules;Quotient and chain rules;Derivatives of exponential and trigonometric functions>Differentiate a composed oscillatory exponential and check each chain-rule factor.
|Implicit and inverse differentiation:Implicit curves;Inverse-function derivatives;Related rates>Relate the changing radius and volume of a sphere at one instant.
|Local and global behavior:Critical points;First and second derivative tests;Constrained interval endpoints>Find every candidate maximum of a function on a closed interval.
|Approximation and error:Linearization;Taylor polynomials;Remainder and validity interval>Compare first- and second-order approximations to an exponential over a finite range.''',
'Derive d(x^n)/dx for positive integer n from the difference quotient and use it to obtain the tangent approximation near an arbitrary expansion point.',
'Differentiate eight functions by hand, verify them symbolically, and study finite-difference error as the step decreases; explain why extremely small steps can worsen numerical results.',
'Compute and interpret first and second derivatives, find a bounded-domain extremum, and attach a numerical error estimate to one local approximation.',
'A derivative is a local rate; a tangent-line approximation need not remain accurate far from its expansion point.')

C(6,'Integral calculus, infinite series, and accumulation','math',[5], 'calculus math sympy',
'''Definite integrals:Riemann sums;Signed area;Fundamental theorem of calculus>Approximate accumulated displacement from tabulated velocities and compare rectangle choices.
|Integration techniques:Substitution;Integration by parts;Partial fractions>Integrate a polynomial times an exponential and verify by differentiation.
|Geometrical and physical integrals:Areas between curves;Volumes and arc length;Weighted averages>Compute an average value over an interval and explain its weighting measure.
|Improper integrals and convergence:Infinite intervals;Integrable singularities;Comparison tests>Determine which powers give a finite integral near zero and at infinity.
|Sequences and series:Geometric series;Taylor series and convergence radius;Truncation bounds>Approximate a convergent geometric sum with an explicit remainder bound.''',
'Derive the finite geometric-series identity and its infinite limit, stating the magnitude condition on the ratio and the exact truncation remainder.',
'Solve one integral by substitution, one by parts, and two convergence problems; approximate a non-elementary definite integral numerically and compare two resolutions.',
'Distinguish an antiderivative from a definite integral and determine whether a proposed infinite sum or improper integral converges before assigning it a finite value.',
'A formal series expansion does not converge everywhere; its convergence domain and truncation error are part of the result.')

C(7,'Linear algebra: spaces, operators, and decompositions','math',[4,5], 'linear sympy',
'''Linear systems:Row reduction;Rank and null spaces;Existence and uniqueness>Solve an underdetermined system and parameterize every solution.
|Vector spaces:Linear independence;Basis and dimension;Linear transformations>Represent one transformation in two bases and compare its matrices.
|Inner-product geometry:Orthogonality;Projections and Gram-Schmidt;Least-squares fitting>Project noisy observations onto a line model and inspect residual orthogonality.
|Eigenvalue problems:Eigenvectors and eigenspaces;Diagonalization;Real symmetric and complex Hermitian matrices>Find the principal directions of a symmetric two-by-two matrix.
|Numerical decompositions:Singular-value decomposition;Condition numbers;Pseudoinverse and low-rank approximation>Perturb a nearly singular linear system and measure solution sensitivity.''',
'Derive the least-squares normal equations from minimizing squared residuals, then explain why a QR or SVD solver can be numerically preferable to forming them directly.',
'Analyze a two-dimensional linear map with determinant, rank, eigenvectors, and singular values; fit a noisy line using a stable solver and report parameter sensitivity.',
'Identify a linear system as unique, inconsistent, or underdetermined and choose an appropriate decomposition without explicitly inverting its matrix.',
'A square matrix need not be invertible or diagonalizable, and a numerically tiny residual does not guarantee an accurate solution to an ill-conditioned problem.')

C(8,'Multivariable calculus and coordinate transformations','math',[6,7], 'multivar sympy',
'''Functions of several variables:Level curves and surfaces;Partial derivatives;Differentiability and tangent planes>Draw level curves and compare partial slopes at a selected point.
|Directional changes:Gradient;Multivariable chain rule;Jacobian matrices>Differentiate a function along a parameterized path in two ways.
|Optimization:Hessian and stationary-point classification;Lagrange multipliers;Boundary extrema>Find constrained extrema on a circle and check exceptional points.
|Multiple integration:Iterated integrals;Integration-region geometry;Order-of-integration changes>Evaluate a triangular-region integral in both orders.
|Change of variables:Jacobian determinants;Polar and spherical measures;Volume distortion>Derive the polar area element and integrate over a disk.''',
'Derive the Jacobian area factor for polar coordinates by taking the determinant of the coordinate map, then use it to recover the area of a disk.',
'Optimize a two-variable function with a constraint and integrate a nonrectangular region; supply sketches, stationary-point classification, and checks using a different coordinate description.',
'Apply the chain rule to a composed coordinate map and choose integration limits and Jacobian factors that describe the intended region exactly once.',
'Replacing Cartesian coordinates with polar coordinates changes the integration measure as well as the function arguments.')

C(9,'Vector calculus and integral theorems','math',[8,4], 'multivar tongem sympy',
'''Vector fields:Field-line interpretation;Scalar potentials;Gradient and directional rate>Sketch a gradient field and identify directions of increasing potential.
|Differential operators:Divergence as local flux;Curl as local circulation;Laplacian and vector identities>Compute divergence and curl of contrasting radial and rotational fields.
|Line integrals:Parameterization and orientation;Work-like integrals;Conservative fields and domain topology>Integrate a field around two paths with common endpoints.
|Surface and volume integrals:Oriented surface elements;Flux through curved surfaces;Divergence theorem>Evaluate the flux of F = r through a sphere directly and from its divergence.
|Circulation and boundaries:Green theorem;Stokes theorem;Singularities and excluded regions>Compare a circulation integral with a surface curl integral and identify any forbidden singular point.''',
'Verify the divergence theorem for F = (x,y,z) on a sphere of radius R, obtaining total flux 4 pi R^3 by both a surface and a volume calculation.',
'Solve one conservative-path problem, one circulation problem, and one flux problem in each of two ways; explicitly state the domain, orientation, and regularity assumptions.',
'Select the appropriate integral theorem and explain why zero curl on a punctured domain does not by itself establish a globally single-valued potential.',
'Field lines are visualization aids rather than literal trajectories, and a zero local curl statement does not remove topological restrictions.')

C(10,'Ordinary differential equations and dynamical systems','math',[6,7], 'ode scipy sympy',
'''First-order equations:Separation of variables;Integrating factors;Initial conditions>Compare the general and initial-value solutions of a decay equation.
|Second-order linear equations:Characteristic roots;Forced solutions;Initial displacement and derivative>Solve an equation with repeated roots and verify both initial conditions.
|Transforms and forcing:Laplace transforms;Impulse and step response;Convolution>Construct the response to a delayed step using a known impulse response.
|Coupled systems:First-order state representation;Matrix exponentials;Phase portraits and linear stability>Classify an equilibrium from a two-by-two system matrix.
|Numerical initial-value problems:Adaptive stepping;Absolute and relative tolerances;Events and stiff equations>Integrate a known solution with solve_ivp and compare global error as tolerances tighten.''',
'Derive the integrating-factor solution of y-prime + p(t)y = q(t), retaining the initial-value term and checking the result by substitution.',
'Solve a forced second-order equation analytically and with solve_ivp; report initial conditions, solver choice, error norms, and an event marking a specified crossing.',
'Convert a higher-order ODE into a first-order system and explain the distinction between a stable physical equilibrium and a stable numerical integration method.',
'An ODE solver returns an approximation controlled by tolerances; smooth plots and successful solver status alone do not establish accuracy.')

C(11,'Fourier analysis and partial differential equations','math',[9,10], 'ode tong mitnum fipy',
'''Orthogonal expansions:Fourier sine and cosine series;Orthogonality and coefficients;Even and odd extensions>Compute the first nonzero coefficients of a piecewise periodic function.
|Frequency-space analysis:Fourier transform conventions;Convolution theorem;Sampling and aliasing>Show two sampled sinusoids that become indistinguishable at an insufficient sampling rate.
|Canonical PDEs:Diffusion equation;Wave equation;Laplace equation>Classify initial and boundary data for each equation type.
|Separation of variables:Eigenfunctions from boundary conditions;Mode superposition;Decay and propagation of modes>Solve diffusion on a finite interval with fixed endpoint values.
|Numerical PDE reasoning:Spatial discretization;Time-step stability;Resolution and boundary convergence>Compare a finite-difference diffusion result with its analytic first-mode decay.''',
'Separate variables in the one-dimensional diffusion equation with homogeneous Dirichlet boundaries and derive the sine eigenfunctions and their exponential decay rates.',
'Reconstruct a piecewise function with increasing Fourier modes, then solve a one-dimensional diffusion problem at two mesh spacings; report Gibbs behavior separately from discretization error.',
'Choose compatible boundary conditions and a time step satisfying the explicit diffusion stability condition for the stated discretization, and demonstrate convergence to an analytic mode.',
'Adding more Fourier modes cannot eliminate the Gibbs overshoot in the uniform sense at a jump, and finer spatial grids can require smaller explicit time steps.')

C(12,'Complex numbers, analytic functions, and contour methods','math',[6,7,9], 'tong math sympy',
'''Complex algebra:Cartesian and polar forms;Euler formula;Roots and arguments>Locate all roots of a complex number and track the selected argument branch.
|Analytic functions:Complex differentiability;Cauchy-Riemann equations;Harmonic real and imaginary parts>Test whether a function of z and its conjugate is analytic on a stated domain.
|Contour integration:Parameterized contours;Cauchy integral theorem;Cauchy integral formula>Evaluate the same simple contour integral directly and by a theorem.
|Singularities and residues:Poles and Laurent expansions;Residue theorem;Real integrals by contour closure>Compute residues and justify the vanishing of the chosen large-arc contribution.
|Branches and applications:Complex logarithm;Branch cuts and multivalued powers;Frequency-response poles>Specify a logarithm branch and explain the jump on crossing its cut.''',
'Derive the Cauchy-Riemann conditions by comparing real- and imaginary-direction difference quotients, including the regularity assumptions needed for the converse.',
'Evaluate one real rational integral by residues, identify every enclosed pole, and provide an independent numerical check; diagram a branch cut for a separate logarithmic example.',
'Determine analyticity, classify a singularity, and justify a contour choice rather than applying the residue theorem without accounting for arcs and branch cuts.',
'A complex derivative is more restrictive than separate real partial derivatives, and the complex logarithm cannot be globally single-valued on the punctured plane.')

C(13,'Probability, random variables, and stochastic reasoning','math',[6], 'prob math',
'''Events and counting:Sample spaces;Combinations and permutations;Probability axioms>Count outcomes for a small experiment before assigning equal probabilities.
|Conditional reasoning:Conditional probability;Independence;Bayes theorem>Compute a posterior probability from a base rate and a noisy measurement model.
|Random variables:Discrete and continuous distributions;Density versus probability;Cumulative distribution functions>Normalize a density and calculate the probability of an interval.
|Moments and dependence:Expectation and variance;Covariance and correlation;Conditional expectation>Calculate the variance of a sum with and without independence.
|Limit behavior and random processes:Law of large numbers;Central limit theorem;Random walks and diffusion scaling>Simulate or tabulate a short symmetric random walk ensemble and compare its mean with its mean-square displacement.''',
'Derive the mean and variance of the sum of independent identically distributed variables and show why the standard deviation of their average decreases as one over the square root of sample count.',
'Solve a Bayes diagnostic example and analyze binomial and Gaussian measurement models; distinguish event probabilities, probability densities, and likelihoods in the written interpretation.',
'Normalize a distribution, propagate a covariance term correctly, and explain the assumptions required before applying a central-limit approximation.',
'Uncorrelated variables need not be independent, and a probability density at a point is not the probability of observing that exact value.')

C(14,'Statistics, measurement uncertainty, and inference','math',[8,13], 'prob math nist',
'''Measurement models:Measurand and calibration;Random and systematic effects;Resolution and repeatability>Write a measurement equation that includes a shared calibration offset.
|Summarizing observations:Sample mean and variance;Outliers and robust summaries;Autocorrelation and effective sample size>Compare a mean and median after one observation is contaminated.
|Uncertainty propagation:Linearized Jacobian propagation;Covariance matrices;Monte Carlo propagation>Propagate uncertainty in a ratio with a shared uncertain calibration factor.
|Parameter estimation:Likelihood functions;Weighted least squares;Confidence intervals and bootstrap>Fit a straight-line model with unequal measurement uncertainties and inspect residuals.
|Testing and model criticism:Null models and p-values;Multiple comparisons;Prediction and posterior checks>Explain a small p-value without assigning it as the probability that the null hypothesis is true.''',
'Derive the first-order output covariance J Sigma J-transpose from a linearized measurement model, retaining cross-covariances and identifying when linearization is inadequate.',
'Design an analysis of repeated pendulum-period measurements with a clock calibration uncertainty; estimate a parameter, propagate both uncertainty sources, and report residual diagnostics.',
'Produce a reproducible estimate with units, uncertainty definition, correlation assumptions, and interval interpretation; distinguish improved precision from removal of a shared bias.',
'Averaging repeated measurements does not necessarily reduce a systematic calibration uncertainty, and statistical significance does not measure practical importance.')

C(15,'Numerical Python and reproducible scientific computing','math',[7,10,14], 'python missing scipy sympy mitnum',
'''Programming foundations:Variables and control flow;Functions and exceptions;Lists and structured records>Write a function that rejects an invalid physical input and returns a labeled result.
|Scientific arrays:NumPy shapes and broadcasting;Vectorized calculations;Units and data types>Compute a trajectory array while documenting the shape and units of every column.
|Numerical algorithms:Root finding with brackets;Quadrature and ODE integration;Floating-point cancellation>Compare a stable and unstable evaluation of a difference between nearly equal numbers.
|Scientific data workflows:Delimited files and metadata;Plot labels and uncertainty bars;Deterministic random seeds>Read a small dataset and produce a graph whose caption states units and processing steps.
|Reproducibility and verification:Virtual environments and dependencies;Git and executable notebooks;Analytic checks and convergence tests>Re-run an analysis from a fresh environment using its documented commands.''',
'Derive the centered finite-difference approximation and its leading truncation order from Taylor expansions, then explain its competition with floating-point roundoff.',
'Create a small repository that fits measured data, integrates an ODE, and exports a labeled figure; include a requirements file, seed, units, assumptions, and one analytic regression check.',
'Another reader can reproduce the stated figure and numerical result from documented commands, while your convergence table resolves a concrete accuracy target.',
'A library function removes implementation work but does not choose the correct model, units, tolerances, or interpretation for the experiment.')

C(16,'Variational calculus and constrained functionals','math',[8,10], 'tong sympy',
'''Functionals:Functions versus functionals;Admissible curves;Endpoint conditions>Evaluate one functional on several trial curves with the same endpoints.
|First variations:Perturbing a path;Integration by parts;Stationary versus minimizing paths>Compute the first-order change of an integral under a compactly supported perturbation.
|Euler-Lagrange equations:One dependent function;Several dependent functions;Explicit versus implicit coordinate dependence>Derive the differential equation for a simple quadratic functional.
|Constraints and symmetries:Integral constraints;Lagrange multipliers;Cyclic variables and first integrals>Find a first integral when the integrand is independent of the path parameter.
|Extensions and numerical approximations:Natural boundary conditions;Second variations;Rayleigh-Ritz trial functions>Approximate an extremal with a finite trial basis and compare with the exact solution.''',
'Derive the Euler-Lagrange equation from a first variation with fixed endpoints, explicitly displaying the boundary term removed by those endpoint conditions.',
'Find the extremal of the integral of y-prime squared with fixed endpoints, establish that it is the straight line, and compare a two-parameter Ritz approximation with the exact answer.',
'Specify admissible variations and endpoint conditions before deriving an extremal equation, and distinguish stationarity from a demonstrated minimum.',
'The principle of stationary action or any stationary functional does not assert that every physical path is a global minimum.')

C(17,'Tensors, differential geometry, and curvature','math',[7,9,12,16], 'tonggr mitgr sympy',
'''Manifolds and coordinates:Charts and transition maps;Tangent vectors;Coordinate basis transformations>Describe two overlapping coordinate charts on a simple curved surface.
|Tensor language:Covectors and dual bases;Tensor products and contractions;Transformation laws>Transform a vector and covector and verify that their contraction is invariant.
|Metric geometry:Metric tensors;Lengths and volume elements;Raising and lowering indices>Compute distance elements in polar coordinates and distinguish basis components from lengths.
|Differentiation on manifolds:Connections;Covariant derivatives;Parallel transport and geodesics>Calculate the nonzero connection coefficients of the plane in polar coordinates.
|Curvature and forms:Riemann and Ricci tensors;Differential forms and exterior derivative;Coordinate artifacts versus intrinsic curvature>Compare zero curvature in polar coordinates with nonzero curvature on a sphere.''',
'Vary the metric length-related energy functional to derive the geodesic equation and identify the Levi-Civita connection coefficients in coordinates.',
'Calculate metric, connection, and curvature for a two-dimensional example; verify a tensor contraction in two charts and compare numerical geodesics with a known symmetry.',
'Explain why nonzero connection coefficients can occur in flat space and demonstrate a coordinate-independent curvature or transport result.',
'Curved-looking coordinate grids do not establish intrinsic curvature, and tensor components alone have no coordinate-independent meaning.')

C(18,'Groups, symmetries, and topological ideas','math',[7,12,17], 'tong tonggr',
'''Group structure:Closure and identity;Inverses and composition;Subgroups and homomorphisms>Build a multiplication table for the symmetries of an equilateral triangle.
|Representations:Matrices representing transformations;Invariant subspaces;Reducible and irreducible representations>Represent a planar rotation on coordinate vectors and check composition.
|Continuous symmetries:Lie groups and generators;Commutators and Lie algebras;Exponentiating an infinitesimal transformation>Recover a finite planar rotation from its generator.
|Topological structure:Open sets and continuity;Connectedness and compactness;Homotopy and winding numbers>Distinguish paths that can contract in a disk from paths circling a missing point.
|Physics-facing applications:SO(3) and SU(2) overview;Order-parameter spaces;Local descriptions and global obstructions>Explain what additional structure is needed before identifying a topological label with a physical observable.''',
'Derive the infinitesimal generator of planar rotations by differentiating its matrix at zero angle and verify the exponential reconstruction of the finite rotation.',
'Create a worked symmetry dossier containing a finite group table, a continuous matrix representation, and winding-number examples; state which results are algebraic and which are topological.',
'Check a proposed representation against the group operation and explain a global obstruction that cannot be detected from local derivatives alone.',
'Two symmetry groups with related local generators need not have identical global structure or identical allowed representations.')

C(19,'Observation, experimental design, and physical evidence','mechanics',[4,14,15], 'up1 mitmech phet',
'''From question to measurement:Operational definitions;Testable hypotheses;Observable versus inferred quantity>Turn a claim about falling objects into a specific measurable comparison.
|Experimental controls:Independent and dependent variables;Controlled conditions;Confounding and randomization>Design a comparison that separates release-height effects from timing bias.
|Instrumentation:Calibration curves;Sampling and sensor bandwidth;Zero offsets and saturation>Inspect a sensor specification and predict a measurement it cannot resolve.
|Evidence analysis:Uncertainty budgets;Residuals and alternative models;Replication and reproducibility>Compare a constant-speed model with an accelerating model using residual patterns.
|Engineering artifacts:Laboratory notebooks;Data provenance;Methods and limitations sections>Write a method another learner can follow with stated instruments and settings.''',
'Derive the measurement equation for a speed inferred from two position readings and a time interval, then propagate its input uncertainties with the stated correlations.',
'Plan and analyze a safe tabletop or simulated motion experiment, including a calibration record, original data, competing fits, uncertainty budget, and falsifiable prediction.',
'A reader can separate your observations from model-based conclusions and reproduce the analysis while understanding the main confounder and accuracy limit.',
'Agreement with one prediction supports a model within the tested conditions; it does not uniquely prove the model or establish unlimited validity.')

C(20,'Kinematics in one, two, and three dimensions','mechanics',[4,5,6,19], 'up1 mitmech phet',
'''Describing motion:Position and displacement;Average and instantaneous velocity;Acceleration and graph slopes>Recover velocity signs from a position-time graph without confusing position with motion direction.
|One-dimensional trajectories:Constant acceleration;Piecewise acceleration;Integration with initial conditions>Construct a braking trajectory with a finite stopping time and continuous position.
|Planar motion:Projectile components;Range and flight time;Assumptions of uniform gravity and negligible drag>Derive the trajectory for unequal launch and landing heights.
|Curvilinear motion:Tangential acceleration;Normal acceleration;Polar-coordinate derivatives>Separate changing speed from changing direction on a curved path.
|Relative motion:Reference-frame translations;Relative velocities;Measurement in moving frames>Compare the velocity of one object reported by two uniformly moving observers.''',
'Starting from constant Cartesian accelerations and initial conditions, derive projectile x(t), y(t), and the parabolic y(x) relation for a nonvertical launch.',
'Analyze a piecewise one-dimensional journey and a projectile landing below its launch point; verify position continuity, velocity components, and the correct positive flight-time root.',
'Reconstruct motion from either a graph or acceleration function, and identify exactly which assumptions permit use of the familiar constant-acceleration formulas.',
'Zero instantaneous velocity does not imply zero acceleration, and constant speed does not imply constant velocity on a curved path.')

C(21,'Newton laws, forces, and interaction models','mechanics',[10,20], 'up1 mitmech principia',
'''Inertial dynamics:Newton first law;Inertial frames;Mass and net force>Explain which force balance is required for constant-velocity motion.
|Force inventory:Weight and normal forces;Tension and elastic forces;Free-body diagrams>Draw separate free-body diagrams for two connected objects.
|Contact models:Static friction inequality;Kinetic friction approximation;Constraints and impending slip>Determine whether an object actually slips before using a kinetic-friction equation.
|Coupled motion:Massless ropes and pulleys;Shared acceleration constraints;Action-reaction pairs>Solve a two-body pulley system without canceling forces acting on different bodies.
|Differential force models:Linear drag;Terminal speed;Validity of idealized force laws>Compare a falling object's initial acceleration and late-time terminal behavior.''',
'Derive the velocity of a body released from rest under constant gravity and linear drag, including its terminal speed and characteristic relaxation time.',
'Solve an incline-with-friction problem and a connected-mass problem, then numerically integrate a drag case; document every body boundary and constraint.',
'Build a correct free-body diagram, decide which friction regime applies, and obtain a force-based equation of motion consistent with the direction conventions.',
'Newton third-law forces act on different bodies and therefore do not cancel within the free-body equation for either body alone.')

C(22,'Work, energy, and conservative interactions','mechanics',[9,21], 'up1 mitmech',
'''Work as an integral:Constant-force work;Variable-force work;Path dependence>Compute work from both a force-distance graph and its integral.
|Kinetic energy:Work-energy theorem;Translational kinetic energy;System boundaries>Use the net work to find a speed without first solving the trajectory.
|Potential energy:Conservative forces;Potential differences;Force from a gradient>Recover a one-dimensional force from a plotted potential.
|Energy landscapes:Turning points;Stable and unstable equilibria;Small-displacement expansion>Locate accessible regions for a specified total energy.
|Energy accounting:Mechanical versus total energy;Dissipation and internal energy;Power and efficiency>Build an energy budget for a sliding object with friction.''',
'Derive the work-energy theorem by taking the dot product of Newton second law with velocity, then integrate over the trajectory.',
'Analyze motion in a quartic potential, locate equilibria and turning points, and add a dissipative segment with an explicit energy transfer to the surroundings.',
'Choose an energy method when appropriate and state whether mechanical energy, total energy of a larger system, or neither chosen quantity is conserved.',
'Potential energy belongs to a specified interaction or configuration, and its arbitrary additive reference does not alter measurable force or energy differences.')

C(23,'Momentum, impulse, collisions, and center of mass','mechanics',[21,22], 'up1 mitmech',
'''Linear momentum:Momentum of a particle;Impulse as a force-time integral;External-force accounting>Find the impulse from a triangular force pulse and compare with momentum change.
|Many-particle systems:Center of mass;Internal-force cancellation;Center-of-mass motion>Find the center of mass of an unequal-mass system and its velocity.
|Collision models:Elastic collisions;Perfectly inelastic collisions;Coefficient of restitution>Solve a one-dimensional collision and check whether kinetic energy is conserved.
|Two-dimensional scattering:Vector momentum conservation;Laboratory and center-of-mass frames;Scattering-angle geometry>Transform a collision result between center-of-mass and laboratory descriptions.
|Open systems:Momentum flux;Variable-mass bookkeeping;Ideal rocket equation>Draw the system boundary for a short interval of rocket mass ejection.''',
'Derive the ideal rocket equation from momentum balance for the rocket plus freshly expelled mass, declaring the exhaust-speed convention and neglecting external forces.',
'Solve elastic and sticking collisions in one dimension and a two-dimensional scattering example; report momentum residuals and the kinetic-energy change in the declared frame.',
'Select the correct system before invoking momentum conservation and distinguish momentum transfer, kinetic-energy loss, and total-energy conservation.',
'Momentum conservation does not imply kinetic-energy conservation, and applying F = m a to a variable-mass subsystem without flux terms can be incorrect.')

C(24,'Rotation, torque, and angular momentum','mechanics',[4,6,23], 'up1 mitmech',
'''Angular kinematics:Angular position and velocity;Angular acceleration;Linear and angular relations>Connect rim speed and tangential acceleration to a rotating disk's angular motion.
|Rotational inertia:Discrete mass sums;Continuous inertia integrals;Parallel-axis theorem>Calculate the moment of inertia of a uniform rod about two parallel axes.
|Torque and dynamics:Lever arms and vector torque;Fixed-axis rotational equations;Rotational work and power>Find the torque produced by an oblique force at a specified application point.
|Angular momentum:Orbital angular momentum;External torque relation;Conservation about a chosen origin>Explain the angular-momentum change caused by shifting the reference origin.
|Rolling and coupled motion:No-slip kinematic constraint;Translation plus rotation energy;Role of static friction>Compare the acceleration of a rolling hoop and solid cylinder down an incline.''',
'Derive the parallel-axis theorem by expanding squared distances from the shifted axis and using the center-of-mass condition to cancel the cross term.',
'Determine the acceleration, friction direction, and energy budget for a rolling object on an incline; verify that the required static friction is available.',
'Compute torque and inertia about a declared axis and solve a coupled translation-rotation problem without assuming that angular momentum is always parallel to angular velocity.',
'Static friction need not dissipate mechanical energy in ideal rolling without slipping, although it can be essential for the required torque.')

C(25,'Rigid bodies and noninertial reference frames','mechanics',[7,10,24], 'tong up1',
'''Rigid-body geometry:Orientation and rotation matrices;Angular-velocity vector;Inertia tensor>Find principal axes of a simple rigid-body mass distribution.
|Three-dimensional rotation:Euler equations;Torque-free motion;Stability about principal axes>Compare rotation near the largest and intermediate principal inertia axes.
|Gyroscopic behavior:Torque-induced precession;Nutation;Approximation regimes>Estimate a slow-precession rate and list conditions under which the approximation fails.
|Accelerating frames:Translational inertial forces;Rotating-basis derivatives;Centrifugal and Coriolis terms>Derive the direction of the Coriolis acceleration for a stated motion and rotation axis.
|Frame-dependent applications:Foucault-pendulum geometry;Rotating-fluid surfaces;Effective gravity>Predict the shape of a steadily rotating liquid surface from its effective potential.''',
'Derive the rotating-frame acceleration relation by differentiating a vector twice with the rotating-basis derivative rule, identifying Coriolis, centrifugal, and angular-acceleration terms.',
'Integrate torque-free rigid-body equations near two principal axes and analyze one rotating-frame trajectory; compare conserved quantities in the inertial description.',
'Distinguish real interactions from terms introduced by frame choice and explain the intermediate-axis instability with the inertia tensor and equations of motion.',
'An apparent force in a rotating frame is not an extra physical interaction, and three-dimensional rotational dynamics cannot generally use a single scalar inertia.')

C(26,'Gravitation, orbital mechanics, and celestial systems','mechanics',[9,23,24], 'up1 mitmech principia rebound astropy',
'''Newtonian gravity:Inverse-square force;Superposition;Gravitational potential and field>Compare the contributions of two separated masses at a point.
|Spherical and extended bodies:Shell theorem;Interior and exterior fields;Potential reference at infinity>Compute the gravitational field inside a uniform sphere and check the surface limit.
|Two-body reduction:Center-of-mass coordinates;Reduced mass;Angular momentum and effective potential>Reduce two mutually gravitating bodies to a relative-coordinate problem.
|Kepler orbits:Conic sections;Energy and eccentricity;Period and escape conditions>Determine whether an orbit is bound from a specified position and velocity.
|Beyond an isolated pair:Tidal acceleration;Restricted three-body ideas;N-body integration and conservation diagnostics>Run a small REBOUND system and compare energy error for two integration settings.''',
'Derive Kepler third law for circular relative motion including both masses, then connect the general bound-orbit energy to the semimajor axis.',
'Calculate orbital angular momentum, specific energy, eccentricity, periapsis, and apoapsis; confirm the orbit classification with a numerical trajectory and conservation report.',
'Use a consistent gravitational parameter and distinguish two-body idealization, tidal effects, numerical drift, and genuinely non-Newtonian phenomena.',
'An orbiting object is continually accelerating in free fall; apparent weightlessness does not mean gravity has vanished.')

C(27,'Oscillations, damping, resonance, and response','mechanics',[10,22], 'up1 ode scipy',
'''Linear oscillators:Stable-equilibrium expansion;Natural frequency;Initial-value solutions>Approximate motion near a potential minimum and identify the effective stiffness.
|Energy and phase:Kinetic-potential exchange;Amplitude and phase representation;Phase-space ellipse>Relate an initial position and velocity to amplitude and phase.
|Damping regimes:Underdamping;Critical damping;Overdamping>Classify three parameter sets and compare their return to equilibrium.
|Driven response:Steady-state amplitude;Phase lag;Transient versus particular solution>Plot amplitude and phase as the drive frequency crosses the natural frequency.
|Resonance measurements:Quality factor;Bandwidth and energy loss;Linear-model breakdown>Estimate damping from a ringdown and compare with a frequency-sweep estimate.''',
'Derive the steady-state response of a damped oscillator using complex amplitudes and identify the frequency-dependent amplitude and phase.',
'Generate a ringdown and frequency sweep for the same oscillator, estimate damping by both methods, and report where finite observation time affects the fit.',
'Distinguish natural, damped, and response-peak frequencies and explain the energy source and loss mechanism in a driven resonant system.',
'Resonance does not create energy, and the frequency of maximum displacement response need not equal the undamped natural frequency.')

C(28,'Normal modes, coupled systems, and continuum waves','mechanics',[7,11,27], 'up1 tong scipy',
'''Coupled oscillators:Mass and stiffness matrices;Symmetric and antisymmetric motion;Energy exchange>Derive the two normal frequencies of equal coupled masses.
|Generalized eigenproblems:Mass-weighted coordinates;Mode orthogonality;Modal amplitudes>Decompose an arbitrary initial displacement into normalized modes.
|Chains and dispersion:Periodic mass-spring chains;Allowed wave numbers;Phase and group velocities>Plot a discrete-chain dispersion relation and identify its long-wavelength limit.
|Continuum limit:Wave equation from a chain;String tension and linear density;Boundary and initial conditions>Recover the wave speed of a stretched string from a force balance.
|Driven and nonideal continua:Standing modes;Damping and mode widths;Finite-resolution spectral identification>Infer a string's parameters from several synthetic resonance frequencies.''',
'Derive the one-dimensional wave equation from transverse force balance on a short string segment, stating the small-slope and constant-tension assumptions.',
'Solve a three-mass normal-mode problem, compare it with a longer chain, and reconstruct a localized initial disturbance from its mode amplitudes.',
'Relate a discrete spectrum to boundary conditions and explain how the continuum approximation emerges without confusing phase and group velocities.',
'Normal modes are collective patterns of the whole coupled system, not individual particles vibrating independently of their neighbors.')

C(29,'Lagrangian mechanics, constraints, and symmetry','mechanics',[16,21,24,28], 'tong sympy',
'''Generalized coordinates:Configuration space;Holonomic constraints;Independent degrees of freedom>Choose coordinates for a pendulum pair and count its independent degrees of freedom.
|Action formulation:Lagrangian T minus V;Euler-Lagrange equations;Endpoint conditions>Derive a pendulum equation without resolving the tension force.
|Constraints and generalized forces:Multiplier constraints;Nonconservative generalized forces;Time-dependent constraints>Recover a constraint force using a Lagrange multiplier.
|Symmetries and conservation:Cyclic coordinates;Noether reasoning;Energy function and time dependence>Identify the conserved quantity associated with one continuous coordinate symmetry.
|Applications and approximations:Small-oscillation expansion;Double-pendulum equations;Coordinate transformations>Linearize coupled pendulum equations and compare their modes with the matrix method.''',
'Derive the Euler-Lagrange equation for a pendulum from its kinetic and gravitational potential energies, then obtain the small-angle limit and its domain of approximation.',
'Construct a Lagrangian for a two-coordinate mechanical system, derive its equations symbolically, identify a symmetry where present, and validate a numerical trajectory against a conservation law.',
'Choose independent coordinates, include explicit time dependence correctly, and explain when a conserved canonical momentum differs from a familiar Cartesian mechanical momentum.',
'The Lagrangian is not generally the total energy, and conservation of an energy function requires appropriate assumptions about explicit time dependence.')

C(30,'Hamiltonian mechanics and phase-space structure','mechanics',[7,29], 'tong sympy scipy',
'''Legendre transformation:Canonical momenta;Regular velocity-momentum maps;Hamiltonian construction>Transform a quadratic kinetic-energy Lagrangian into a Hamiltonian.
|Hamilton equations:First-order canonical dynamics;Phase-space trajectories;Energy-level geometry>Recover an oscillator trajectory from Hamilton equations.
|Poisson brackets:Bracket definition;Time evolution of observables;Conserved quantities>Compute elementary brackets and check a proposed conserved observable.
|Canonical transformations:Symplectic structure;Generating-function ideas;Action-angle variables>Verify that a simple variable transformation preserves the canonical bracket.
|Geometric integration:Liouville volume preservation;Symplectic stepping;Long-time energy behavior>Compare explicit Euler and a symplectic scheme over many oscillator periods.''',
'Derive Hamilton equations by differentiating the Legendre transform of a regular Lagrangian, explaining why the velocity-dependent terms cancel.',
'Integrate a nonlinear one-dimensional Hamiltonian system with two methods and compare phase-space area and long-time energy behavior rather than inspecting trajectory plots alone.',
'Construct canonical momenta and a Hamiltonian, evaluate a Poisson bracket, and distinguish an energy function from the broader role of the Hamiltonian as a generator of evolution.',
'Canonical momentum need not equal mass times velocity, and a symplectic method does not necessarily conserve the exact numerical value of energy at every step.')

C(31,'Nonlinear dynamics, bifurcations, and chaos','mechanics',[10,15,27,30], 'tong scipy',
'''Nonlinear phase portraits:Fixed points;Linearization;Basins of attraction>Locate equilibria and compare linear predictions with nonlinear trajectories.
|Bifurcations:Saddle-node and pitchfork examples;Hopf bifurcation concepts;Parameter continuation>Track stable and unstable fixed points as a control parameter changes.
|Maps and sections:Discrete iteration;Poincare sections;Periodic and quasiperiodic motion>Construct a stroboscopic section for a driven oscillator.
|Chaos diagnostics:Sensitive dependence;Lyapunov-exponent estimation;Bounded deterministic aperiodicity>Estimate finite-time divergence while staying below saturation of trajectory separation.
|Reliable nonlinear computation:Transient removal;Time-step convergence;Noise versus deterministic sensitivity>Repeat a chaos diagnostic with smaller time steps and a longer discarded transient.''',
'Linearize a one-dimensional nonlinear flow near a fixed point and derive its local perturbation growth law, stating why it does not determine the full global dynamics.',
'Create a bifurcation diagram for a logistic-map parameter sweep and a Poincare section for a driven oscillator; disclose transients, sample count, and numerical resolution.',
'Support a chaos claim with more than an irregular time series and explain how numerical error, external noise, and deterministic sensitivity can be distinguished operationally.',
'Chaotic dynamics can be deterministic; unpredictability does not imply that the equations themselves are random or that every nonlinear system is chaotic.')

C(32,'Fluids, transport, and continuum mechanics','mechanics',[9,11,21,22], 'up1 tongfluid mitnum fipy',
'''Continuum description:Density and pressure fields;Material versus spatial viewpoints;Continuum approximation>Estimate when a molecular scale is small enough relative to a flow length scale.
|Conservation laws:Mass continuity;Momentum balance;Material derivative>Derive steady incompressible flow continuity through a narrowing channel.
|Ideal flow:Euler equation;Bernoulli relation;Vorticity and circulation>Apply Bernoulli along a streamline and list the conditions it assumes.
|Viscous flow:Newtonian stress;Navier-Stokes equation;Poiseuille and Couette solutions>Recover the velocity profile and flow rate in a simple pressure-driven geometry.
|Dimensionless regimes:Reynolds number;Boundary-layer scales;Instability and turbulence limitations>Compare two geometrically scaled flows and identify which dimensionless groups must match.''',
'Derive plane Poiseuille flow from steady incompressible Navier-Stokes with no-slip walls, then integrate the velocity profile to obtain flow per unit width.',
'Solve a viscous channel problem analytically and numerically, check mass conservation and grid convergence, and compare the pressure-work input with viscous dissipation.',
'State continuum, incompressibility, constitutive, and boundary assumptions separately and decide whether an inviscid relation is appropriate for a proposed flow.',
'Bernoulli is not a universal statement that faster fluid always has lower pressure; its streamline and energy assumptions must hold.')

C(33,'Electric charge, Coulomb interaction, and superposition','em',[4,6,21], 'up2 mitem phet',
'''Charge as a property:Positive and negative charge;Charge conservation;Quantization and macroscopic approximations>Track net charge when two isolated objects exchange electrons.
|Coulomb interaction:Magnitude and vector direction;Point-charge approximation;Vacuum permittivity and units>Compute the force on one charge from a second with the displacement vector stated explicitly.
|Superposition:Vector sums of interactions;Symmetry and cancellation;Many-charge configurations>Find a net force from three charges without adding force magnitudes as scalars.
|Continuous charge:Linear surface and volume densities;Charge elements and integration;Finite-size corrections>Integrate the force from a uniformly charged finite line on an axial test charge.
|Material and modeling distinctions:Conductors and insulators;Induction and polarization overview;Electrostatic idealization>Explain attraction of a neutral object without assigning it an unexplained net charge.''',
'Derive the total axial force from a finite uniformly charged line by integrating Coulomb contributions and check the distant-point-charge limit.',
'Solve a three-point-charge force problem and a finite-line problem, sketch directions, verify units, and show how each result changes under a uniform rescaling of all distances.',
'Construct a vector Coulomb sum or charge-density integral and identify when the point-charge and electrostatic approximations are justified.',
'A neutral object can contain separated or polarizable charge; neutrality alone does not imply the absence of electric interactions.')

C(34,'Electric fields, flux, and Gauss law','em',[9,33], 'up2 mitem tongem phet',
'''Field definition:Force per test charge;Source-field separation;Field-line conventions>Infer a field from the force on test charges of opposite signs.
|Fields of distributions:Finite lines;Rings and disks;Symmetry-axis integrals>Derive the axial field of a charged ring and inspect its far-distance limit.
|Electric flux:Oriented area vectors;Flux integrals;Open versus closed surfaces>Calculate flux through a tilted flat surface in a uniform field.
|Gauss law:Integral and differential forms;Enclosed charge;Gaussian-surface choice>Use spherical symmetry to find the field inside and outside a uniform charge sphere.
|Symmetry and limitations:Planar and cylindrical symmetry;Piecewise field matching;When Gauss law does not simplify the field>Explain why knowing enclosed charge alone is insufficient to determine an asymmetric local field.''',
'Use Gauss law to derive the electric field inside and outside a uniformly charged solid sphere and verify continuity at the sphere surface.',
'Compare a ring field calculated by integration with a sphere field calculated by Gauss law; plot their axial dependence and label assumptions and limiting cases.',
'Choose a Gaussian surface only when symmetry justifies taking the field outside the flux integral and distinguish total flux from the field at one point.',
'Zero enclosed charge means zero net flux through a closed surface, not necessarily zero electric field everywhere on that surface.')

C(35,'Electric potential and boundary-value problems','em',[8,11,34], 'up2 tongem fenics sympy',
'''Potential differences:Work per charge;Path independence in electrostatics;Reference conventions>Calculate a potential difference and explain why the arbitrary zero cancels.
|Field-potential relation:Negative gradient;Equipotential surfaces;Potential of point and continuous charges>Recover field direction and magnitude from a one-dimensional potential profile.
|Electrostatic energy:Assembly of charge configurations;Self-energy caveats;Field-energy density>Compare pairwise assembly energy with a simple field-energy calculation.
|Boundary-value equations:Poisson and Laplace equations;Dirichlet and Neumann data;Uniqueness and compatibility>Specify a well-posed rectangular-domain potential problem without overprescribing its boundary.
|Solution methods:Method of images;Separation of variables;Finite-element or finite-difference convergence>Solve a point charge near a grounded plane and check the conductor boundary value.''',
'Derive Poisson equation from Gauss law and E = minus gradient of potential, then use the image-charge construction to satisfy a grounded-plane boundary condition.',
'Solve a rectangular Laplace problem numerically and an image-charge problem analytically; verify boundary values, residuals, and refinement behavior before interpreting field plots.',
'Distinguish boundary data from sources, explain the relevant uniqueness result, and calculate an electric field from a potential with a consistent sign and reference.',
'Electric potential is a scalar energy-per-charge quantity, not electric potential energy itself, and an image charge is a mathematical construction outside the physical solution region.')

C(36,'Dielectrics, polarization, and capacitive systems','em',[14,22,35], 'up2 mitem tongem',
'''Capacitance:Charge-voltage relation;Geometry dependence;Series and parallel combinations>Find an equivalent capacitance and track charge and voltage on every component.
|Energy and forces:Stored capacitor energy;Fixed-charge versus fixed-voltage conditions;Work exchanged with a source>Compare dielectric insertion into an isolated capacitor and one connected to a voltage source.
|Polarization:Dipole moment density;Bound volume and surface charges;Microscopic response overview>Compute bound surface charge for a uniformly polarized slab.
|Macroscopic fields:Electric displacement;Linear isotropic constitutive law;Interface boundary conditions>Solve a two-layer dielectric capacitor while matching free-charge and potential constraints.
|Real-material limitations:Frequency-dependent response;Dielectric loss and breakdown;Measurement and uncertainty>Estimate a capacitor parameter from uncertain geometry and permittivity without assuming ideal behavior at all frequencies.''',
'Derive the capacitance of a parallel-plate capacitor containing two dielectric layers in series using displacement-field continuity and the sum of the voltage drops.',
'Analyze a layered capacitor, compute stored energy under both fixed-charge and fixed-voltage conditions, and propagate geometric and permittivity uncertainties with stated correlations.',
'Separate free and bound charge, apply interface conditions correctly, and include source work when predicting forces or energy changes in a connected capacitor.',
'Inserting a dielectric does not have the same energy accounting at fixed charge and fixed voltage; a connected voltage source can exchange energy with the system.')
