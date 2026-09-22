# Prospective Loop 2: one finite window and inverse-energy response

Human author and project direction: **Hruday N M (BUNZEEY)**. Prepared as source/method advice in response to the advisor's question, conditional on acceptance of AT1. This document is not a frozen contract, producer output or admitted finding. It does not select Loop 3.

## Proposed bounded question

In the actual AQ state, certify (i) a positive lower bound on Wilson spectral mass in `[alpha/16, 8 alpha]`, and (ii) an interval for the inverse-energy spectral functional. Preserve the actual unknown moments rather than replacing them by their reference values. Accompany the result with explicit measures sharing the same zeroth, first and second moments but having different spectra and inverse-energy responses.

Let `x=E/alpha`, let `eta` be the pushforward of the actual centered Wilson spectral measure, and put `a=1/16`. Prospective AT1 premises are

`supp eta subset [a,infinity)`, `s=int d eta`, `u=int x d eta`, `v=int x^2 d eta <= B=36+98|tau|`.

The actual local quantities obey `w=omega_num(W)`, `q=omega_num(W^2)`, `s=q-w^2`, `u=1-q`. AQ2 supplies `|w|<=1/500`, `|q-1/4|<=1/500` and the inherited variance lower bound. These are deterministic analytic uncertainty bounds. They are not data with a sampling covariance, and `s` and `u` are correlated. A calculator must either accept actual compatible moments or optimize its stated certificate over this joint `(q,w)` domain. Endpoint substitution in two independent intervals can give a valid conservative result, but must not be described as sharp over the actual feasible set.

Define `R=int E^(-1) dnu(E)=alpha^(-1) int x^(-1) d eta(x)`. This has inverse-energy units. The positive gap makes this finite and it equals the squared-vector resolvent form `<chi,H_phys^(-1)chi>` on the vacuum-orthogonal sector. If called a response, specify this mathematical definition. Calling `2R` a static susceptibility of an infinite-volume deformed ground state would require a further ground-state differentiability argument that this contract does not supply.

## Certificate semantics

The classical method is pointwise domination followed by positive integration. For a quadratic `p(x)=c0+c1*x+c2*x^2`:

- If `p<=k` on the entire support and `c2<=0`, then `int k d eta >= c0*s+c1*u+c2*B`.
- If `p>=k` on the entire support and `c2>=0`, then `int k d eta <= c0*s+c1*u+c2*B`.

The signs matter because only an upper second-moment bound is known. Using `v=B` as an equality is invalid. When `c2=0`, no second-moment premise is used and the record should say so. Additional valid inequalities on v could strengthen a certificate, but must be named and proved. For rational targets, multiplying by a denominator is permitted only after proving that denominator is strictly positive throughout `[a,infinity)`.

Prove the one-sided inequalities over the full continuous half-line by exact factorization or exact positive-semidefinite/SOS data. Dense grid samples and floating-point SDP status alone cannot certify between-sample behavior or the high-energy tail. Weak duality is enough for a valid bound; no claim of optimality, strong duality or uniqueness of an extremal measure is needed.

## Candidate certificates to verify under the future contract

For `L=8`, a simple baseline is the affine minorant

`p_L(x)=(L-x)/(L-a) <= 1_[a,L](x)` for `x>=a`.

It suggests `eta([a,L]) >= (L*s-u)/(L-a)`, clipped below by zero if needed. It treats a possible atom at L correctly: the minorant is zero there while the indicator is one. It uses the gap and first moment, not B. Retaining the unknown `(q,w)` relation gives numerator `(L+1)*q - L*w^2 - 1`; the prospective exact code should evaluate a guaranteed rational floor from the declared bounds. Do not claim that the true measure has a hard upper energy cutoff.

For the inverse-energy lower bound, a tangent candidate at a declared `c>0` is

`ell_c(x)=2/c-x/c^2`, with `1/x-ell_c(x)=(x-c)^2/(c^2*x)`.

For an upper bound, choose a declared `b>=a` and test

`p_b(x)=[x^2-(2*b+a)*x+b^2+2*a*b]/(a*b^2)`.

The proposed exact residual factorization is

`p_b(x)-1/x=(x-a)*(x-b)^2/(a*b^2*x)`.

This upper certificate has positive quadratic coefficient, so replacing v by B is in the safe direction. A practical prospective choice is `c=3`, `b=49`, with parameters explicitly classified as dimensionless certificate choices, not new physical couplings. These choices should be frozen, not tuned after observing the answer. Retain simpler baselines `R>=alpha^(-1)*s^2/u` and `R<=alpha^(-1)*s/a` as established Cauchy/Jensen/support comparisons, with their actual denominator conditions. The new deliverable would be an evaluated model-specific interval with exact checks, not invention of these general inequalities.

## Equal-moment countercontrols to verify

Candidate dimensionless measures are

`eta_A=(1/8)delta_2+(1/8)delta_4`,

`eta_B=(1/32)delta_1+(3/16)delta_3+(1/32)delta_5`,

and `eta_C=(1/4)*Uniform[3-sqrt(3),3+sqrt(3)]`.

They are proposed to have the common triple `(s,u,v)=(1/4,3/4,5/2)`, respecting `s=q-w^2`, `u=1-q` at `q=1/4,w=0` and lying above the declared gap. Their inverse moments and spectral types differ: A/B have different atom sets, while C is atomless. These fixtures should be checked exactly. None is claimed to be the AQ measure or to be physically realized by its Hamiltonian; they test whether the contracted information logically identifies a pole. They show insufficiency even when the second moment is known exactly, a stronger information assumption than AT1's ceiling.

If desired, the spectrum of an abstract nonnegative multiplication operator on `L^2(eta)` with source vector 1 realizes each fixture, and a separate vacuum summand implements centering. That construction still does not provide a lattice-gauge counterexample. Do not infer different AQ phases or multiple thermodynamic states from these moment controls.

## Primary literature and overlap

Bertsimas and Popescu, *SIAM Journal on Optimization* 15 (2005), 780–804, Section 2 (Theorems 2.1–2.2) and Section 3 (Proposition 3.1), formulate moment-constrained probability bounds through polynomial dual certificates; upper-moment inequalities require coefficient-sign restrictions. Their author-hosted paper was read at those passages. This supplies method ancestry, not a grant of model-specific constants.

[Author-hosted paper](https://web.mit.edu/dbertsim/www/papers/MomentProblems/Optimal-inequalities-in-probability-theory-A-convex-optimization-approach-SIAM15.pdf)

Abbott, Fields, Jay, Oare and Saccardi, arXiv:2605.20509v1 (19 May 2026), explicitly frame positive spectral reconstruction through one-sided kernel bounds. Sections III.1 and IV.1–IV.3 cover dual certificates and positive-denominator rational/piecewise kernels; VII.4 distinguishes extremal feasible spectra from the true spectrum. This recent preprint directly overlaps the proposed method. We do not import its statistical assumptions or claim to invent a spectral bootstrap.

[Version-pinned primary preprint](https://arxiv.org/html/2605.20509v1)

The proposed Hruday/HNM label should identify this AQ application, physical dictionary, exact numerical envelope and audited countercontrols. Priority of the general moment method is not new, and priority of the application has not been established by this selected-source check. Loop 3 should be selected only after this result and its skeptical objections are known.
