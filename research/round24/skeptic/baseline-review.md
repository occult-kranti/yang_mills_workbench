# Round24 independent baseline review

Reviewer: separate skeptic model agent. This is an independent agent check of
shared premises, not external peer review. It does not relabel historical U1/U2
same-author work as independently reviewed at the time of its admission.

## Verdict

No concrete invalid inference was found in the inherited U2 endpoint proof in
this targeted audit. U2 may be used as a scoped premise for V1. That statement
does not certify every inherited result or claim that an independent theorem
prover has verified the report. No current Round24 producer was read for this
baseline review.

## Actual objections examined

* **Eigenstate and local algebra.** U1's two length-six loops consist of free
  singleton factors. Their common-energy superposition is an exact reference
  electric eigenstate. The local swap acts on the eight-factor Haar space and
  is extended by identity; it is not a two-state truncation of the dynamics.
  The closed-loop vectors and local vacuum are invariant under boundary gauge
  actions, so the rank operators commute with those actions. This argument
  requires the inherited bounded physical operator algebra; it supplies no
  membership in the Wilson multiplication subalgebra.
* **First order versus finite-time sufficiency.** With the inherited negative-time
  Heisenberg convention, `Z=U_0(-t)U_q(t)` gives
  `F'=-(i/hbar)[V_I,F]` for `F=ZWZ*`. The U1 matrix element has the reported
  sign. U2 keeps the complementary channels through a full connected-word
  remainder. It does not infer nonconvergence from U1's derivative alone.
* **Whole-system loading.** Each complete reference factor owns at most ten
  links and meets at most forty faces. Reading a word from its innermost
  commutator gives at most `8+3k` occupied factors. Hence the product
  `prod 40(8+3k)`, rather than a fixed-support power, counts a valid overestimate
  of all ordered connected words, including repetitions. Reference free
  evolution retains complete factors even when it spreads among their links.
* **Convergence and topology.** For each fixed `q<1`, bounded `V_q` validates the
  strong interaction-picture series through the global Dyson bound. The
  connected majorant then controls the local tail in the stated small scaled
  time disk. These roles are distinct. No norm continuity of the unbounded
  reference generator, no `q=1` Hamiltonian and no exchange with an uncontrolled
  expansion are needed for the conclusion as written.
* **Stationary replacement.** N1 defines centered stationary correlations using
  the same negative-time convention. The raw-expectation and two mean-product
  replacements cost at most `6d_q`. The carrier phase has modulus one; a ground
  phase is not silently dropped. The identity observable gives zero connected
  covariance and catches the uncentered-unitary false model.
* **Strict lower bound.** The tail bound is quadratic near zero and its ratio
  to `z` is increasing on the stated interval. The exact rational cap check,
  combined with that analytic monotonicity, establishes a positive lower
  bound for every fixed `0<z<=10^-6`. A negative finite-q lower estimate is
  inconclusive, as inherited reports already state.

## Replay and source evidence

All four inherited U1/U2 direction checkers passed in fresh directories under
`baseline-replays/`. Their executable checks are finite algebra and arithmetic
checks supporting the proof, not a numerical realization of the infinite
Hamiltonian. The separate `check_baseline.py` reconstructs thirty connected
coefficients, the exact positive margin and profile polynomial inequality,
and executes frozen-support and omitted-ground-phase false-model controls.
`baseline-checks.json` binds the reviewed reports, gates, V1 contract and check.

## Forward review constraints

V1 must keep a fixed bounded local operator, actual stationary dynamics,
positive physical scales and a uniform correlator error. Finite rank is not a
finite-dimensional whole-system dynamics. A spectral measurement may be a
mathematically valid finite-outcome observable without a demonstrated physical
instrument. Wilson multiplication membership needs its own argument. An
operational approximation must quantify its error relative to the very small
U2 margin. Newton's inverse-inference and Tesla's loading practices motivate
these checks; historical or esoteric claims supply no modern theorem premise.

Later loop reviews require both producer freezes before comparison, contract
compliance, source hash binding, independent checker replay and actual
discriminating controls. Mathematical scope will be accepted or limited on the
evidence; completing an investigation does not automatically solve its target.
