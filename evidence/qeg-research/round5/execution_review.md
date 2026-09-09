# Executed proof route and validation record

These are results from the supplied code, not an illustrative invented search. The selected-regulator scenario starts from the parameter, state, drive and imported mathematical assumptions. It does not assume the positive margin that it seeks to derive. All outputs preserve the finite-model scope.

## Accepted search route

| Step | Reviewed rule | New conclusion |
|---|---|---|
| 1 | PM01 | `finite_parameter_certificate` |
| 2 | PM02 | `positive_margin` |
| 3 | R01 | `Zpositive` |
| 4 | R02 | `norm` |
| 5 | R03 | `regular_rhs` |
| 6 | R04 | `localwellposed` |
| 7 | R05 | `energyidentity` |
| 8 | R06 | `Upositive` |
| 9 | R07 | `energybound` |
| 10 | R08 | `compacttrajectory` |
| 11 | R09 | `globalwellposed` |
| 12 | R10 | `smoothflow` |
| 13 | R11 | `causal_tangent` |
| 14 | R12 | `selected_theorem` |

The genuine intermediate meeting has forward cost **8** and backward suffix cost **6**. At that meeting, the backward goals are a subset of the forward facts. The checked combined route costs **14**. Independent forward uniform-cost certification popped **24** states; the bidirectional phase popped **548** backward states. These are counts of algorithm states, not physical degrees of freedom.

At the meeting, the forward side has already established the parameter certificate, positive margin, regular vector field, local solution, invariant norms, work identity and positive/coercive energy. The backward side has reduced the target to those facts plus the retained model, drive and ODE assumptions. It then replays the field bound, finite-time compactness, continuation, smooth dependence and conditional causal support. Every required premise is retained.

The generic margin-assumed theorem has certified cost 12; the isolated margin calculation has cost 2. The full selected-regulator route joins those calculations in one actual scenario. Costs apply only to the supplied reviewed rule library. The search did not invent or symbolically prove the ODE theorems referenced by its rules.

## Executed checks

| Check family | Executed result | Meaning |
|---|---|---|
| Root symbolic algebra | 16/16 passed | Exact identities, including deliberately omitted quotient and wrong constraint coefficient |
| Independent mathematical critic | 24/24 passed | Algebra, rational bounds and explicit failed generalizations |
| Planner regression suite | 24/24 passed | Conjunction, scope, assumption retention, immutable certificates, costs and limits |
| Independent search review | 19/19 gates passed | Includes 64 independently enumerated small-library cost comparisons |
| Rounded coefficient certificate | Exact rational comparison passed | Display-only global lower bound 0.7653173589206453 exceeds 3/4 |
| Continuum or gravitational closure | Not established | Not converted into a passing gate or an assumed proof edge |

Some independent algebraic checks intentionally overlap. Adding their counts does not measure confidence or create a larger theorem. Source hashes in the raw logs tie each execution to its actual code and fixture. The rational-coefficient check certifies a nearby exact finite model defined by rounded inputs, not the numerical time trajectory.

## Defects found and corrected during this run

| Defect | Why it mattered | Accepted correction |
|---|---|---|
| Forward solve completed before backward search | The supposed two-front result immediately met at the original target | Alternate actual frontiers; retain an intermediate meet and separate optimality certificate |
| Parameter-margin fixture was isolated | The full theorem still used an unexplained margin seed | Add an integrated selected-constants-to-theorem scenario |
| Hidden assumption metadata and unverified seeds | A route could appear exact while depending on an undisclosed conjecture | Require retained seed dependencies, safe theorem verification and inherited assumptions |
| Mutable library after hash creation | Costs or rules could change while the old hash remained attached | Immutable mappings plus hash recomputation at planning and replay |
| Causal-support statement lacked its comparison condition | Varying initial data may produce pre-probe response | State identical preparation/source histories and zero initial tangent explicitly |

Initial findings are preserved separately. One early inline metadata probe did not retain its own source hash; its provenance is identified as a contemporaneous observation, not retroactively presented as a reproducible failing test. The later regression tests and final independent review are reproducible.

## Evidence limits and next proof frontier

The analytical proof is a reviewed conventional argument, supported by exact checks. It has not been translated into a proof-assistant kernel. The strongest accepted mathematical claim is the finite-model theorem under its displayed assumptions, together with the separate conditional Bianchi identity. No numerical horizon resolution, cosmological solution, quantum-noise calculation, continuum limit or proof of WGC/FL is hidden in the reported success status.

The next frontier consists of concrete obligations: a common renormalized quantum current and directional stress, their force Ward identity, regulator-uniform estimates where a continuum claim is intended, and consistent total constrained gravitational data. The supplied solver prompt keeps these obligations explicit.
