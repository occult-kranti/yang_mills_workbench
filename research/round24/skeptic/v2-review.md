# V2 independent skeptic review

Verdict: **accepted as a conditional finite-sample, single-endpoint resource
certificate**. Both reports were frozen before comparison. No observations,
apparatus, efficient simulator, or optimal resource bound have been produced.
This is independent model-agent review, not external peer review.

## Domain and physical time

The actual local vectors defining W have energies zero and `9alpha/2`. The
local swap preserves the reference domain and has bounded commutator norm
`9alpha/2`. Complete-factor tensor decomposition and graph-norm closure justify
the extension to the full reference domain. Bounded V preserves that domain
and adds at most `2||V||=alpha eta/4`. This proves the specific observable's
norm-Lipschitz time estimate; it does not assume that arbitrary bounded
observables enjoy this property. Reverse also proves the same estimate for its
self-adjoint unitary completions because their zero projector commutes with H0.

The timing hypotheses differ legitimately. Forward assumes all settings of a
model share one fixed displaced time and bounds the actual W correlation,
giving pair cost `(9+eta/4)theta`. Reverse permits displacement of each
quadrature setting/shot, bounds the completion products separately, and uses
twice that coefficient. Neither coefficient may be copied into the other's
noise model. Both retain the physical time units `hbar/alpha`; no clock is fit
to an observed signal. The implementation error assumes that all remaining
errors, including imperfect coherent evolution inside a setting, are already
bounded. This remains a conditional premise.

## Estimator and confidence

Eight quadrature settings and one separate W-mean setting per model correctly
reconstruct the complex connected quantity. Squaring the sampled mean is not
claimed unbiased; its realized error is bounded using both means in `[-1,1]`.
The concentration derivations apply to independent bounded observations and
the union bound covers eighteen settings. Forward's identically distributed
assumption is sufficient; reverse's independent but non-identically distributed
version also works with its uniform per-trial bias bounds. Unconditional shot
independence remains required; unknown shared drift is not covered merely by
calling repetitions separate preparations.

Forward uses full trace norm `s`, hence expectation cost `s`; reverse uses half
trace norm `epsilon_p`, hence cost `2epsilon_p`. This factor is correctly carried
into their distinct resource formulas. Neither offers all-q/all-time or
adaptive-stopping confidence. The positive lower bound for the estimator's
magnitude is a probability statement conditional on the model and noise
assumptions, not a fabricated experimental value.

## Arithmetic, controls and replay

Both finite-q examples keep the stationary state error and use integer-root
enclosures. Both prove a finite-q lower margin above `10^-8`, at different q.
The positive rational Taylor partial sum proves `exp(9)>3600`; therefore
`N=18/r^2` suffices for 99% simultaneous confidence over the eighteen means.
The total is `3.24e22` preparations in both examples. Forward's bound is
`3.3125e-9` with relative time error `5e-23`; reverse's different tolerances
give `8.4225e-10` with relative time error `5e-31`. These are sufficient bounds
under their stated assumptions, with no minimality or practicality theorem.

Normal and optimized producer replays match all frozen scientific outputs.
Submission sources, contract dependencies and instruction bindings verify;
both contain at least three true Boolean controls. `v2-replay.json` records
the hashes. The forward checker now constructs the controlled-unitary ancilla
and traces out the system, computes the imaginary signal, detects reversed Y
sign, and computes sequential readout failure. Reverse checks the phase,
commutator algebra, finite-q state correction and exact error budget. Positive
finite Bernoulli error probability correctly rejects deterministic sampling
certainty. Scalar comparison controls are algebraic checks, not experiments.

## Remaining premise

Ground-state preparation, coherent full-system control, extremely small
systematic errors, calibration and the required independence are assumed.
V2 makes their required accuracy explicit; it does not supply the apparatus.
The Wilson witness, homogeneous gap and continuum construction remain open.
The next goal should follow the roadmap's residual/iteration issue; no claim
that a measurement resource certificate closes those mathematical gaps is
admissible.
