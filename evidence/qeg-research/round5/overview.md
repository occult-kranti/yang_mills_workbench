# Bidirectional proof dossier: a finite Maxwell–Dirac theorem and its gravity frontier

Research round 5 • 9 September 2026 • Equation audit, conventional proof, adversarial checks and executable dependency search.

## What this round establishes

We selected one sharply defined claim from the larger electromagnetic–quantum–gravitational project and proved it under explicit assumptions: the finite homogeneous Maxwell–Dirac initial-value problem used in the accepted response experiment has a unique solution for every finite future time. It has a quantitative electric-field bound; smooth changes in admissible initial data and drive have a finite-time differentiable response with retarded source support. For the selected regulator the proof establishes a global denominator bound, not just a sampled one:

\[
Z(a)>\frac34\quad(a\in\mathbb R),\qquad
|x(s)|\le\frac43|\lambda|\quad(s\ge0)
\]

for the exact vacuum start and a normalized nonnegative pulse of amplitude \(\lambda\). This is a conventional mathematical theorem obtained from the explicitly stated finite equations and standard ODE results. It is not a novel universal theorem of QED, a formal proof-assistant certificate, a continuum limit, or a solution of quantum gravity. The theorem's useful contribution is to remove a precise regularity gap in this project's finite model.

The wider theory remains open. The four original fronts share mechanisms, but their assumptions differ: de Sitter black-hole discharge bounds, curved-space particle creation, inner-horizon instability, and photon–graviton mixing cannot be chained as if each implies the next. The map below records those connections with separate edge types. A conjecture is never silently promoted to an axiom.

## How to read and reproduce this dossier

Start with the theory map to see what is assumed, established, derived here or unresolved. Read the theorem statement before its proof. Follow the forward estimates and the backward continuation requirements until they meet. Then inspect the explicit counterexamples: they determine which stronger statements this proof cannot support. Finally, use the gravity interface lemma to see what is needed next.

The companion package includes editable Markdown, the full machine-readable map, every proof-planning rule, symbolic checks, independent falsification tests, exact rational certificates, source reading-depth ledgers and the historical model contract. Run the instructions in README.md from the extracted package root. Reported test counts refer to executed checks, not votes by agents or a probability that a physical theory is true.

## Selection before search

| Candidate | Current proof-ready inputs | Missing decisive lemma | Decision |
|---|---|---|---|
| Global finite-model existence and causal response | Explicit smooth finite equations, positive modal state space, matched work identity | Global Z margin and compact continuation estimate | Select; both gaps are closed in this round |
| Uniform-in-time tangent stability | Exact first-variation equations | Positive perturbation norm or spectral/dynamical stability argument | Do not infer from signed tangent work |
| Regulator-independent continuum response | Finite trajectories and one fixed-window quadrature study | State, subtraction, uniform bounds, current and derivative convergence | Retain as a separate research target |
| Self-consistent Bianchi-I Einstein–QED | Classical constraints and a chosen symmetry | Renormalized directional stress, total force Ward identity, local closure | Derive constraint propagation now; quantum closure remains open |
| Unified WGC/FL, singularity and conversion theory | Several established model results and conjectural bounds | Shared hypotheses and genuine bridge theorems | No proof route currently supplied |

## What “bidirectional A*” means here

Mathematical proof is an AND/OR dependency problem. Applying a theorem often needs several premises simultaneously. A theory-name graph with ordinary reversible arrows would lose those conjunctions and permit invalid arguments. We therefore use finite ground Horn rules: a rule records every premise, one conclusion, its scope and a reference to an independently reviewed derivation.

Forward search accumulates conclusions only when every premise is present. Backward search replaces an unproved goal with a sufficient set of premises of an applicable theorem. For example, global continuation can be reduced to local uniqueness, a regular vector field and finite-time compact bounds. This is goal regression; it does not assert that global existence logically implies those particular sufficient conditions.

The two searches meet when all remaining backward obligations are already among the forward facts. The reconstructed route is replayed independently. We use the admissible zero heuristic, so costs are uniform-cost search costs. A first meeting is only a candidate. A separate forward uniform-cost goal pop certifies least cost within the frozen, finite supplied rule library. Neither minimal cost nor successful JSON replay validates the mathematics behind a rule: the attached derivations and critic review serve that separate purpose. Official Lean documentation makes the stronger distinction between proof generation and kernel verification. [Lean tactics](https://lean-lang.org/theorem_proving_in_lean4/Tactics/), [Lean FAQ](https://lean-lang.org/faq/).

Costs currently count reviewed rule applications. They do not measure scientific truth, novelty, proof length in an unbounded mathematical language, or compute needed for quantum gravity. A failed search says that this finite library lacks a derivation, not that the target is false. Research conjectures can be explored only as retained explicit conditions.

## Corrections and methodological lessons

The energy estimate must cover zero initial energy, which is the actual vacuum preparation. We use \(\sqrt{W+\epsilon}\) and take a limit, avoiding division by zero. The global Z condition must hold for every potential reached by any allowed solution; a good trajectory minimum cannot supply it. A first variation of energy is signed and cannot become a positive tangent norm by naming it an energy. Fixed-time differentiability does not imply bounded response for all time. Finally, a covariant gravity source needs directional pressures and external-work accounting, not just an energy history.

During code review, the first planner draft ran forward certification to completion before its backward phase. Its positive fixture therefore met immediately at the original goal. That draft checked a proof route but did not demonstrate useful two-front search. The correction requires actual frontier expansion in both directions, an intermediate meeting, and a separate certification phase. The executable record states whether those gates pass; the algorithm's label is not acceptance evidence.

The theorem advisor and critic worked independently on the algebra and counterexamples. A separate search advisor specified the logical contract, and the coding agent implemented it. Completed prior agents remain inactive; they are not an unmonitored continuing swarm. Agent review is supporting process evidence, not a substitute for mathematical proof.

## Model coordinates and domain

Use \(\hbar=c=1\), physical fermion mass \(m>0\), charge magnitude \(e>0\), and

\[
s=mt,\qquad a=eA_z/m,\qquad x=eE_z/m^2,
\qquad b=|eB|/m^2.
\]

All theorem primes refer to dimensionless time s; its use of t as an abstract ODE variable is interchangeable with s, not with dimensionful proper time without the factor m. The selected values are b=10, longitudinal momentum window [-20,20] and Landau indices 0 through 4 inclusive. The theorem covers every positive exact Gauss–Legendre node count in that window. The historical response experiment used 1,024 longitudinal nodes per retained level. This is a temporal initial-value problem: it has no radial horizon condition, origin condition or spatial infinity boundary. Introducing one merely to resemble the original black-hole request would change the problem.
