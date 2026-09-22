# Findings since the approved Round27 merge

This is a living advisor summary for the user's request to list the new findings.
It describes workbench contributions; scientific priority has not been established.
All ten requested investigations are now admitted within their reviewed
scopes, completing five adaptive goal pairs. AJ1/AJ2 identify the actual
homogeneous physical representation and its nonzero Wilson fluctuation;
AK1/AK2 quantify that fluctuation, its physical form energy and its
imaginary-time correlation. Scientific production stopped after AK2.
Further goals in the roadmap are planning only.

## AG2: complete original homogeneous remainder

The earlier selected-cubic analysis is now connected to the entire original
remainder: quadratic terms, the remaining same-anchor cubic terms, ordered
cross-anchor cubic terms and the complete higher-order tail. Its transport
retains scalar energy, vacuum mixing and centered diagonal contributions.
The complete output interaction budget is below 0.007 for M<=1/1000 and below
0.00007 for M<=1/10000. The extracted reference has a positive gap. The full
Hamiltonian still contains mixing, so this is not its numerical gap theorem.

Evidence: [AG2 gate](ag2-gate.json), [forward report](../forward/ag2/report.md),
[reverse report](../reverse/ag2/report.md), [skeptical review](../skeptic/ag2.md).

## AG3: one complete-mixing correction, with a crucial comparator

A new correction treats the actual complete mixing family and keeps the
retained-diagonal commutator in its recurrence. Its sufficient factors are
3060/3623 on the main interval and 5949/96812 on the narrow interval, between
support weights 2 and 3/2. Scalar and diagonal updates and domains remain explicit.

Changing the weight alone gives an uncorrected embedding ceiling of 81/256.
The main correction does not improve that ceiling; the narrow correction does.
Neither comparison proves a ratio to the actual uncorrected lower-weight norm,
all-stage convergence, or a gap for the complete original Hamiltonian.

Evidence: [AG3 gate](ag3-gate.json), [forward report](../forward/ag3/report.md),
[reverse report](../reverse/ag3/report.md), [skeptical review](../skeptic/ag3.md).

## AI3: exact retained cancellation and a complete-error obstruction

Exact signed moment differences through orders three, five and seven retain a
factor 1-q^2; the all-order combination remainder retains 1-q. The physical
transfer includes state and connected-mean costs, full spatial tails, both
averaging columns and a denominator bound. All ten tested full physical ratio
intervals overlap. Separate state and spatial costs explain the failed sufficient
separation certificate. This is not equality of actual physical outputs.
The earlier direct-scalar distinction remains valid for both Wilson probes at
u=10^-18, k=5, with positive complete scalar margins about 3.2145*10^-26 and
4.4050*10^-26. Forming a ratio can discard information present in those scalars.

The new exact moment identities include

    Delta m3 = 2 q^13 (1-q^2),
    Delta m5 = q^21 (1-q^2) (12+8q+12q^2),
    Delta m7 = q^29 (1-q^2) (54+72q+164q^2+72q^3+54q^4).

The symmetry underlying the all-order cancellation belongs to the retained
endpoint matrix, not automatically to the full canonical Hamiltonian.

Evidence: [AI3 gate](ai3-gate.json), [forward report](../forward/ai3/report.md),
[reverse report](../reverse/ai3/report.md), [skeptical review](../skeptic/ai3.md).

## AI4: a uniform family of conditional physical discriminators

A revised duration and growing-collar schedule gives a full physical ratio
separation at least 39u/40 for every real 0<u<=10^-24. Coordinate induction and
all-band recurrences establish the unbounded family; finite fixtures only check
the implementation. An additional forward per-scalar allowance zu/12000 preserves
a gap above 0.78u. Other valid allowances remain separately attributed.
The forward all-depth complete-collar envelope is
N_k<=24(k+1)^3+14(k+1)^2; the other directions prove valid larger envelopes.

The physical clock starts at 2*10^65 hbar/alpha. Its design depends on the
proposed parameter pair, and tolerated scalar errors shrink with u. Same-u
pair discrimination is not a cross-parameter inverse, an unknown-u instrument,
a demonstrated apparatus or an empirically calibrated clock.

Evidence: [AI4 gate](ai4-gate.json), [forward report](../forward/ai4/report.md),
[reverse report](../reverse/ai4/report.md), [skeptical review](../skeptic/ai4.md).

## AH1: complete physical enrichment on the larger graph

The open 3-by-2-by-1 cell graph has 24 vertices, 46 original links and 29 faces,
including seven internal faces. The strict electric cutoff has rank 30. Its
individually resolved generated enrichment has rank 561, with 465 metric
weights one and 96 metric weights three. The complete electric and magnetic
actions are exact: 2,124 magnetic nonzeros and 312,597 structural zeros.

The complete outside map vanishes on the initial sector but has a nonzero
spin-3/2 component on a new input. Its simultaneous norm envelope, both nested
projector comparisons and true output denominator give all-time relative heat
error below 0.0022 for the declared normalized complex vacuum-near preparations.
The reverse bound below 0.00215 is separately attributed. These are exact
semigroup error bounds on one graph, not computed heat-vector errors or a
volume-uniform result.

Evidence: [AH1 gate](ah1-gate.json), [forward report](../forward/ah1/report.md),
[reverse report](../reverse/ah1/report.md), [skeptical review](../skeptic/ah1.md).

## AH2: delayed loading improves the sufficient heat bound

Admitted after independent review. Both frozen directions retain all 531
new channels, their feedback, stationary face loading, full outside returns,
the actual independent centers and the true denominator. At the predeclared
join sigma=3 they prove the common all-time true-relative ceiling

    18126701281201/212761890290715000 = approximately 0.000085197124619.

The independently frozen skeptic obtains

    4501862190047/53190472572678750 = approximately 0.000084636627056.

The complete old-face-to-new Gram is 7I+J/4, so the exact source norm is
sqrt(57)*lambda/2. The actual centered new-to-new block has damping at least
9/2. These facts control the complete coupled trajectory without assuming a
bright-only invariant subsystem.

Both are below the prospective 0.0001 target on the unchanged coupling interval
and full radius-0.01 preparation class. The difference is a valid tighter
rational coupling-norm cap, not disagreement about physical data. The 27
predeclared fixtures evaluate certificates and preparation membership, not
numerical heat states. The stationary loading term dominates this sufficient
early estimate.

An additional forward argument proves that the retained ground leaks into a
specific omitted character, so its energy strictly exceeds the full ground
energy at positive coupling. It follows that the retained output norm can
exceed the true output norm and cannot simply replace the true denominator.
The independent review verifies this argument and distinguishes it from the
other submissions' abstract diagnostic counterexamples.

Evidence: [AH2 gate](ah2-gate.json), [AH2 contract](../contracts/ah2.json),
[forward report](../forward/ah2/report.md),
[reverse report](../reverse/ah2/report.md),
[independent skeptical derivation](../skeptic/ah2-independent-derivation.md).

## AJ1: the actual homogeneous physical representation

For the existing I1 nonsummable homogeneous omitted-coupling model, a complete
regional vacuum-reset argument gives

    Tr(rho_Lambda,R h_R) <= 2M n_Lambda(R) <= 8M|R| = 56|tau||R|.

All incoming and outgoing complete interaction stars are counted. Compact
regional energy cutoffs turn this uniform estimate and the inherited local
state limit into actual local trace-norm density convergence. Normality of the
represented local factors is also proved, with the spectator-factor transfer
made explicit in the skeptical review.

The result justifies the original endpoint Haar averages in the homogeneous
GNS representation, and proves that the cyclic space of all bounded local
gauge-invariant observables equals the joint gauge-fixed vector space.
Covariance of the actual closed generator makes this physical space reducing.
Its centered self-adjoint physical energy restriction inherits the threshold
alpha/16 on the same positive but unevaluated I1 coupling interval.

This closes a representation obligation left open at the cumulative AH2
inventory cutoff. It does not evaluate the coupling constants, establish a
nonzero Wilson excitation, identify every boundary-state limit, or construct
continuum Yang-Mills. A gap exclusion alone would also hold in a vacuum-only
physical space; the nonzero-observable question was still open at the AJ1 checkpoint. AJ2 below closes it.

Evidence: [AJ1 gate](aj1-gate.json), [forward report](../forward/aj1/report.md),
[reverse report](../reverse/aj1/report.md),
[skeptical review](../skeptic/aj1.md),
[postreview analytic clarification](../skeptic/aj1-post-review.md).

## AJ2: a nonzero actual homogeneous Wilson fluctuation

The specified elementary xz Wilson observable uses four original links inside
two complete factors, comprising 48 links and 36 endpoint gauge actions.
Conditional Haar integration in one actual link proves that every real level
set of this multiplier has Haar measure zero, including its endpoint levels.

AJ1's actual normal local density therefore has strictly positive Wilson
variance: a zero variance would require its nonzero range to lie in a zero
eigenspace of the multiplier. No faithfulness or equality to the Haar
reference state is assumed. This proves that the physical GNS space contains
a nonzero centered Wilson vector, closing AJ1's nonvacuity omission.

For its actual variance v>0, the connected imaginary-time correlation obeys

    0<C(t)<=v exp[-alpha t/(16 hbar)]  for every finite t>=0.

The result holds over the same inherited symbolic coupling interval. The
variance is unevaluated, and bounded semigroup calculus supplies this result
without an energy-moment or generator-domain assertion. Atomlessness of the
Wilson multiplier does not determine whether its energy spectral measure
has atoms. No lower decay estimate, threshold eigenvalue, real-time decay,
measured mass or continuum construction is established.

Evidence: [AJ2 gate](aj2-gate.json), [forward report](../forward/aj2/report.md),
[reverse report](../reverse/aj2/report.md),
[skeptical review](../skeptic/aj2.md).

## AK1: a quantitative actual homogeneous Wilson fluctuation

For the same origin xz Wilson observable, both independently frozen producers
prove

    Var_omega(W) >= 119/576 > 1/5,

conditional on both |tau|<the inherited unevaluated tau_* and |tau|<=2^-16.
The complete region has exactly two incident orthant interaction stars.
AJ1's actual reference-energy bound therefore gives Tr(rho_R h_R)<=28|tau|.
The full product-reference gap bounds the vacuum-overlap deficit; a proved
mixed-density inequality gives full trace norm ||rho_R-P||_1<1/24.
Transporting both Wilson moments then charges the unknown mean squared.

The independently frozen skeptic proves the stronger floor131/576, using
the half-distance cost for the positive effect W^2 while retaining the full
distance cost for signed W. The comparison review validates this refinement
and preserves its attribution. These are lower bounds, not computed actual
variances. At zero omitted coupling the exact reference variance is1/4.

Normal concentrating states and a tilted reference state demonstrate why
normality alone or uncharged centering cannot establish the result. Blind
origin incidence tests remain recorded beside discriminating interior tests.
The extra numerical cap does not evaluate the original stability constants.
No variance theorem for all translated observables, physical excited-vector
energy moment, numerical mass or continuum construction is supplied by AK1.

Evidence: [AK1 gate](ak1-gate.json), [forward report](../forward/ak1/report.md),
[reverse report](../reverse/ak1/report.md),
[independent skeptical derivation](../skeptic/ak1-independent-derivation.md),
[skeptical review](../skeptic/ak1.md),
[Newton comparison](../experts/newton/ak1-comparison.md).

## AK2: actual physical form energy and a finite spectral window

The same original origin Wilson excitation now has finite physical form
energy. A domain-valid finite-volume ground-state calculation gives

    mu_1,Lambda = alpha omega_Lambda(1-W^2) <= alpha.

Every one of the four original oriented links contributes
(1-W^2)/4 to the gradient square. All selected and omitted magnetic terms
are retained and commute as multiplication operators; both ground scalars
are accounted for before centering. This is the actual finite ground state,
not a Haar replacement or AK1's different local reference-energy estimate.

The inherited bounded-local tested resolvent limit, justified moving
centering and nonnegative spectral cutoffs establish

    chi in D(sqrt(H_phys)),   mu_1 = integral E dnu(E) <= alpha.

The finite moment identity has not been proved to survive as equality in the limit. The
independent counterexamples show how moment can escape to arbitrarily
large energies while bounded spectral tests and total masses converge.
No physical operator-domain or second-moment theorem is asserted.

With the common admitted variance consequence v>=1/5 and inherited
support above alpha/16, this gives the frozen closed-window bound

    nu([alpha/16,10alpha]) >= 1/10,

and, for every finite t>=0, the two-sided imaginary-time inequalities

    (1/5)exp[-5alpha t/hbar] <= C(t)
                           <= v exp[-alpha t/(16hbar)].

The upper bound is inherited from AJ2; the lower bound uses the newly
proved physical moment and convexity of the exponential. The spectral
mass is unnormalized Wilson variance. A nonzero interval weight is not an
identified eigenatom, exact lowest mass, or real-time decay statement.

All three independently frozen derivations support the same targets. The
skeptic additionally constructs a bounded physical operator on the complete
free local region whose excited vector has infinite form energy, showing
why W's proved smooth multiplier regularity matters. That diagnostic is
separately attributed and extended by identity outside its region; it is
not a global vacuum projector. The producers' abstract counterexamples
remain valid. Blind inverse-sign squared-gradient controls and a forward
pre-execution syntax failure are preserved. The postreview also records
the reverse diagnostic's unused stale gap label without changing its
correct energy/heat calculations or frozen bytes.

Both coupling conditions remain essential: |tau|<the unevaluated tau_*
and |tau|<=2^-16. The additional cap supplies no evaluated nonzero
stability interval. The result concerns this fixed-spacing, selected-strip
homogeneous omitted-interaction orthant state and this original Wilson;
it supplies no other-boundary identification or continuum construction.

Evidence: [AK2 gate](ak2-gate.json), [forward report](../forward/ak2/report.md),
[reverse report](../reverse/ak2/report.md),
[independent skeptical derivation](../skeptic/ak2-independent-derivation.md),
[postreview](../skeptic/ak2-post-review.md),
[final review](../skeptic/ak2.md),
[Newton comparison](../experts/newton/ak2-comparison.md).

## Research and strategy findings

The archive audit corrected an omission: Round21 I1 already establishes an
existential homogeneous-omitted-coupling stability result and a specified
full-algebra orthant GNS construction. Recovering that same qualitative result
with another theorem would duplicate admitted scope. New quantitative,
all-stage, physical-representation or boundary statements need their own
proof obligations. See the [I1 planning correction](../experts/feynman/i1-stability-planning-clarification.md).

The readout audit separates two missing quantifiers: a clock fixed using only
coarse prior information, and discrimination between candidates whose unknown
parameters vary independently. Solving the first does not automatically solve
the second. See [unknown-clock planning](../experts/tesla/unknown-clock-planning.md).

The two source ledgers currently contain 33 attributed primary/historical/forum/
bibliographic reading records at 41 recorded URLs, plus five screening or reopen
records; the URL union including screening is 46. These are records of limited
reading, not complete books, comprehensive proof audits or independent studies.
Historical and occult material supplies methodological questions; it supplies
no unsupported physical premise. The [source survey](../experts/source-survey.md)
and [additive review](../experts/source-supplement.md) preserve the evidence levels.

## What these findings do not establish

No numerical volume-uniform interval for the full homogeneous Hamiltonian,
complete homogeneous iteration, required model/scale matching, nontrivial
four-dimensional continuum Yang-Mills construction, or continuum mass-gap proof
has been established by this cycle. A defensible scalar percentage of solving
Yang-Mills cannot be inferred from investigation counts, matrices, bounds or
the size of the research graph.
