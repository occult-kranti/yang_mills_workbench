# Round19 initial advisor review

Applied skills: `qeg-research-advisor` and local validation skill `paired-physics-research` with `scale-and-exceptions.md`.

Starting commit: `b9d32afb9e74c91477fd8914411eba347430e606`. I audited the Round18 handoff against the current repository before freezing any new scientific loop. The Round18 A1, A2 and post-A gate manifests all replay against the current files with no missing files and no SHA-256 mismatches. This review applies the project advisor contract and treats the recorded source/data as authoritative over roadmap prose.

## Continuity decision

The next cycle keeps the user-requested structure: root integration with delegated advisor-skeptic review, forward derivation, independent reverse/skeptic reconstruction, three goals, two sequentially gated loops per goal, and two advisor decisions counted separately from research loops. The first advisor decision is this review. The second occurs only after Goal A has two accepted or terminal loops. A1 is the only frozen scientific contract now; A2 and all B/C second loops stay gated by evidence.

The recovered historical Goal A pair is essential:

| Source cycle | Accepted A1 result | Accepted A2 result | Consequence for Round19 |
|---|---|---|---|
| Round17 | Exact local projector/diagonal estimate, plus a counterexample showing the pure relative-form shortcut fails for the vacuum-offdiagonal magnetic term. | Pairwise link-disjoint nonzero plaquette supports have a physical gap at least `alpha_min(3/4-rho)` for `rho<3/4`; dense overlapping support remains open. | Do not use sparse factorization for an overlapping bridge. Any local overlap must prove its own zero-mean/offdiagonal structure. |
| Round18 | A dressed three-face bridge passes: two dressed end blocks plus an overlapping bridge give the primary local lower estimate `alpha/8` under the stated coefficient bounds. | A spatially decaying, full-support finite-volume family passes with bound `7 alpha_min/64`, but its complete-strip-only boundary rule is not a literal restriction family. | The next A1 must repair coefficient consistency at finite boundaries before any compactness or dense-stability bridge is attempted. |

This changes the next plan in one concrete way: Round19 Goal A starts with boundary consistency, not another larger finite-volume estimate. The finite local mechanisms from Round18 are reusable only after every clipped component produced by a single infinite coefficient assignment is classified and bounded. Boundary faces whose coefficients change when a larger box is chosen are now a rejecting control.

## Physical and mathematical scope

The active Hamiltonian branch remains pure finite-graph SU(2) Yang-Mills rotors:

`H_N = alpha * sum_e C_e - sum_f lambda_f x_f`, with `C_e=j(j+1)` and `x_f=Tr(U_f)/2`.

`alpha`, `lambda`, `mu` and the newly frozen `E_star` are physical energy quantities. A1 must record `alpha/E_star` separately from `lambda/alpha`, `mu/alpha`, finite volume and any lattice-spacing label. A common physical conclusion requires `E_star > 0`, a positive lower bound on `alpha/E_star`, and fixed local coefficients on overlapping finite restrictions. Static Euclidean `kappa`, conditional Haar measures, variational trial amplitudes, and dependency-graph labels are separate variables. No new physical-time generator, continuum limit, thermodynamic state, or Clay mass-gap implication is supplied by this contract.

The user’s forward/reverse reconstruction analogy is useful as a work discipline: the forward derivation declares the infinite local assignment and derives finite restrictions; the backward verifier starts from the desired common-scale conclusion and reconstructs the premises needed for it. Their paired expansion nodes must agree at the same physical `alpha` scale. The “double Fibonacci geometry” remains a testable organizing hypothesis only; A1 must pass by exact graph, Haar and min-max arguments, not by the analogy.

## Initial substantive A-boundary progress

I wrote an advisor-side preliminary classification record at `boundary-classification.json`. It is not a scientific gate, but it fixes the first cheap discriminator. If the infinite local pattern marks xy faces on even-y rows with x-phases `left, bridge, right`, finite restrictions contain maximal one-, two- and three-face components depending on the box boundary phase. The required local obligations are:

- single selected face: free full-link gap comparison gives at least `3alpha/4 - alpha/2 = alpha/4` for an end face, and a larger bound for a bridge-only face;
- two contiguous selected faces `left+bridge` or `bridge+right`: free full-link comparison with zero Haar means gives the candidate `3alpha/4 - (alpha/2 + alpha/8) = alpha/8`;
- full three-face strip: reuse or reprove the Round18 dressed bridge mechanism, including the actual untouched-link Haar premise, to get `alpha/8`.

The classification also says what can falsify this route: a reachable clipped component without a bound, a missing free-link zero-mean premise, or an n-dependent coefficient assignment like the Round18 complete-strip selector.

## Decision-relevant ambiguities and omissions found during skill validation

- The new reusable skill requires a fixed positive `E_star`; the first draft only used `alpha_min`. The frozen contract now adds `E_star > 0` and rejects `E_star = 0`, tolerance normalization, static `kappa` normalization and Fibonacci index normalization.
- The current steering clarifies that the user did not demand exactly three active agents. The review now treats the structure as root integration plus delegated advisor-skeptic work with independent forward and reverse scientific evidence where assigned.
- No observable or competing model currently makes the double-Fibonacci geometry physically operative. It remains an organizing hypothesis until a held-out prediction is specified.

## Provisional B and C plan

Goal B remains the complete larger low-energy projector on the actual two-cube graph. The first loop should classify every physical channel below the frozen electric threshold, including nonplanar six-edge cycles and all multiplicities, before computing the exact complement cross block. No B2 coupling box is frozen before B1 evidence and the post-A advisor decision.

Goal C remains the genuinely integrated link-cluster problem. The first loop should unfreeze a specified surrounding link or minimal cluster only after proving the discriminator for the chosen normalized observable and retaining the induced joint measure, partition factor and singular endpoints. No omitted-weight or dagger control is accepted unless it is proved to distinguish the observable being tested.

## Frozen next action

`contract-a1.json` is the frozen Round19 A1 contract. It specifies the physical contract, forward and backward deliverables, acceptance tests, falsifying controls and stop condition. A1 should stop once it proves or rejects the boundary-consistent local `alpha/8` component bridge; compactness, limiting states, spectral passage and dense homogeneous stability belong to later gates.
