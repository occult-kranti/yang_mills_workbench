# What this computation can establish

The implemented object is a finite four-dimensional Euclidean Wilson measure on a periodic lattice. Every link belongs to SU(2); there are no matter, scalar, photon or gravitational variables. On a lattice with V sites there are 4V links and 6V positively oriented plaquettes.

## Conventions and exact finite-measure existence

Write U(q)=q0 I−i(q1 sigma1+q2 sigma2+q3 sigma3), with q0²+q1²+q2²+q3²=1. Then scalar(U)=Tr(U)/2=q0. The product of represented quaternions has vector part q0 r+r0 q+q×r. The exact action and probability measure are

    S(U)=beta sum_(x,mu<nu) [1−(1/2)ReTr U_mu(x) U_nu(x+mu)
                                          U_mu(x+nu)^dagger U_nu(x)^dagger],
    dP_beta(U)=Z_beta^(-1) exp[−S(U)] product_links dU_link.

All Haar measures here have total mass one. Since −1≤Tr(U_p)/2≤1, one has 0≤S≤12 beta V and exp(−12 beta V)≤Z_beta≤1. Compactness and continuity therefore give a well-defined finite measure for every finite beta≥0. This elementary finite-dimensional argument supplies neither a continuum quantum field theory nor a uniform spectral gap.

## Oriented staples and local updates

For the link U=U_mu(x), let A be the sum of six paths from x+mu back to x:

    A = sum_(nu!=mu) [
      U_nu(x+mu) U_mu(x+nu)^dagger U_nu(x)^dagger
      + U_nu(x+mu−nu)^dagger U_mu(x−nu)^dagger U_nu(x−nu)].

At fixed other links, S(U)=constant−beta scalar(UA). The implemented delta for replacing U by U' is consequently −beta scalar[(U'−U)A]. The length≥2 restriction makes A independent of the updated link even on a length-two periodic direction; length-one directions would require a different treatment. Random local differences are tested against an independent full-action complex-matrix oracle, including length-two and unequal odd/even lattices.

For a left proposal U'=RU, the inverse step uses R^dagger. Our Haar/isotropic-rotation mixture has equal densities for R and R^dagger. The Metropolis acceptance probabilities obey a_forward/a_reverse=exp(−delta S). Each update preserves the target measure. Fixed-order composition of such updates preserves the measure, even though whole-sweep detailed balance is not claimed. This argument does not certify that a finite warmup has reached equilibrium.

## Exact one-link Haar identity inside the interacting 4D lattice

This derivation requires no strong-coupling approximation. Hold A fixed while integrating the selected link. Let UA=s I−i v·sigma and vary U(theta)=exp(i theta sigma_a/2)U. Then

    d_a s=v_a/2,       d_a² s=−s/4,
    d_a S=−beta v_a/2, d_a² S=beta s/4.

On compact SU(2), Haar integration of a total derivative vanishes. Apply this to d_a[(d_a S) exp(−S)], obtaining

    <(d_a S)²−d_a² S>=0.

Sum a=1,2,3 and multiply by four:

    < beta² |v|²−3 beta s >=0.

The program reports this residual averaged over every link of each saved measurement. Shared links and successive Markov samples create correlations; the program uses sweep-level batching rather than treating individual link terms as IID. At beta zero the residual is identically zero and is labeled algebraically trivial. At beta>0 consistency is a necessary sampler check, not a sufficient equilibration or theory-validity certificate. Dropping the factor three or changing a staple dagger should be detectable by the deterministic derivative/action tests and by this stochastic diagnostic.

## Haar plaquette benchmark and controlled one-matrix integral

At beta=0 links are independent Haar matrices under the target measure. A plaquette is a product of four distinct independent links when all periodic lengths are at least two, so its product is Haar. With t=Tr(U_p)/2,

    p_0(t)=(2/pi)sqrt(1−t²), −1≤t≤1,
    E[t]=0, E[t²]=1/4, Var(t)=1/4.

Plaquettes within a configuration need not be independent. Their spatial average's variance is therefore not simply 1/(4 times the plaquette count) without a covariance argument.

An independent *single-matrix* comparison has density proportional to exp(beta t)dU. Its exact integral is

    Z_1(beta)=2 I1(beta)/beta,
    E_1[t]=d_beta log Z_1=I2(beta)/I1(beta),
    E_1[t²]=1−3 E_1[t]/beta.

The beta→0 limits are supplied analytically. Small-beta series avoid cancellation, and scaled modified Bessel functions avoid avoidable exponential overflow at ordinary large beta. Extreme cases where derived arithmetic is nonfinite fail explicitly. The rejection sampler proposes Haar t and accepts with probability exp[beta(t−1)], producing IID accepted samples. The one-matrix Bessel formula is not used as an exact 4D lattice plaquette prediction at nonzero beta.

## Relation to the Yang–Mills target

Forward: compact SU(2) link variables → finite positive Wilson measure → gauge-invariant expectation values → exact finite-lattice identities → implementation and finite sampling diagnostics.

Backward: a nonzero physical mass gap requires a reconstructed continuum theory and a uniform, physically normalized spectral bound. These require controlled ultraviolet and infinite-volume limits, renormalized observables, and the relevant positivity/regularity assumptions. None follows from the six small-lattice chains in this package. No plaquette curve, one-matrix mass scale or short noisy correlation fit is presented as a glueball mass.

The useful falsifiable next step is a sampler-comparison and volume study with independently implemented heatbath updates and preregistered error budgets, followed by proper gauge-invariant correlators on a sufficiently long time extent. That is a numerical research plan, not a proof route completing the Millennium problem.

## Sources and reading depth

- Kenneth G. Wilson, *Confinement of quarks* (1974), DOI: https://doi.org/10.1103/PhysRevD.10.2445. Official publisher abstract inspected September 2026: lattice gauge invariance and the distinction between strong-coupling behavior and Euclidean-invariant limits. Full paper not obtained in this subtask.
- Robert W. Johnson, *General heatbath algorithm for pure lattice gauge theory* (2010), https://arxiv.org/abs/1003.3219v2. Abstract inspected: independent algorithm-comparison context; it does not certify this implementation or supply its numerical values.
- Michael Creutz, *Monte Carlo study of quantized SU(2) gauge theory* (1980), official record https://www.osti.gov/biblio/5458175. Search metadata inspected; direct record fetch timed out. Historical lead only, not full-text verified here.

The explicit algebra and Haar integral above were derived for this implementation and checked independently; they are standard finite lattice identities, not claimed as new discoveries.
