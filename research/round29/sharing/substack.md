# Vanishing local coefficients, a nonvanishing long-time correlation difference

*A research notebook by Hruday N M (BUNZEEY)*

The most surprising result in my Yang–Mills workbench is a warning about limits: making an interaction small locally does not guarantee that its effect disappears when you also wait longer.

In one precisely defined, regulated SU(2) model, we obtained a strictly positive lower bound for the difference between an interacting correlation and its reference correlation—even as a parameter approaches the endpoint where the local perturbation coefficients vanish.

This is a scoped mathematical result, not a solution of the four-dimensional Yang–Mills mass-gap problem. I am sharing the derivation, executable checks, and remaining gaps so other people can inspect and challenge them.

## The effect

Let \(0<q<1\), write \(\varepsilon=1-q\), and consider the workbench's canonical summable full-link model. Fix the lattice spacing and positive physical energy and time units. Its local interaction scale behaves as

\[
\tau_q\sim \frac{8\eta}{7}\varepsilon^3,
\]

with fixed \(0<\eta<1\). Observe the system at the growing physical time

\[
T_q=C\frac{\hbar}{\alpha}\varepsilon^{-3},\qquad z=C\eta.
\]

The small local coefficient and long observation time balance. That observation suggests a persistent effect, but it does not prove one: omitted channels, higher orders, and the interacting state can spoil a two-state calculation.

For the particular bounded, gauge-invariant local rank observable specified in the draft, let C_q be its stationary connected real-time autocorrelation in the q-model and C_0 its reference autocorrelation. The full-system estimate is

\[
\liminf_{q\to1^-}|C_q(T_q)-C_0(T_q)|
\geq \frac{z}{84}-\frac{44}{9}
\frac{(80z/7)^2}{(1-80z/7)^5}
>\frac{z}{168}>0,
\quad 0<z\leq10^{-6}.
\]

This endpoint nonconvergence witness is indexed as **HNM-C-RECENT25**, with the original identifier **Round23 U2** retained. HNM labels identify workbench results; they do not establish priority over the scientific literature.

## Where the bound comes from

The reference observable has variance one and excitation energy \(E=9\alpha/2\), so its reference correlation is \(C_0(t)=e^{-iEt/\hbar}\).

First, compute the actual resonant matrix element. The first-order contribution to the demodulated correlation is \(i s_q q^4/96\), where

\[
s_q=\frac{\alpha\tau_q t}{\hbar}.
\]

Second, include the full connected expansion. Starting from the observable's eight complete reference factors, the number of potentially interacting factors after \(k\) steps is at most \(8+3k\). Each factor meets at most forty omitted faces. Counting ordered connected words and retaining repeated faces bounds the order-\(n\) term by

\[
(10s_q)^n\frac{(8/3)_n}{n!}.
\]

Here \((8/3)_n\) is the rising factorial. Summing the terms from order two onward gives the explicit upper bound

\[
R(x)\leq \frac{44}{9}\frac{x^2}{(1-x)^5},\qquad x=10s_q<1.
\]

Third, retain the state-replacement error. The proof bounds it and shows that it tends to zero as \(q\to1^-\). It is not discarded because it looks small in a simulation.

Finally, at \(t=T_q\), we have \(s_q\to8z/7\). The leading response tends to \(z/84\), while the complete higher-order bound is quadratic in \(z\). An exact rational endpoint check, together with monotonicity on the whole declared interval, proves that the remainder stays below \(z/168\).

This establishes an actual lower bound on a full correlation difference. It is stronger than merely failing to prove convergence.

## What changed—and what did not

Earlier bounds gave convergence on windows growing more slowly than \(\varepsilon^{-3}\). This witness shows that the endpoint exponent cannot be included in a general convergence statement for every bounded local observable in this particular model.

It does not say that every observable fails to converge. The original witness is a rank observable, not an ordinary Wilson multiplication measurement. The total perturbation norm is exactly \(\|V_q\|=\alpha\eta/8\), constant in q: coefficientwise vanishing is not norm-small convergence. The lower bound is deliberately tiny, and the long time window is not a demonstrated laboratory protocol. The endpoint \(q=1\) itself is outside the summable family.

Most importantly, the homogeneous model and continuum Yang–Mills theory are different mathematical targets. Transferring this result to either requires an actual model and physical-scale comparison.

The new audit makes that concern concrete. For the standard uniform SU(2) coefficient convention \(\alpha=g^2/(2a)\), \(\lambda=2/(g^2a)\), the complete I1 sufficient certificate requires \(\lambda/\alpha\leq1/8\), hence \(g^4\geq32\). A weak-bare-coupling path falls outside this certificate. Changing units cannot repair a dimensionless inequality. This is a limitation of our current proof route, not proof that a mass gap is absent.

## A second result from the new cycle

The new HNM four-site stability certificate (Round29 AM2) supplies a numerical finite-volume interval for the complete selected-strip SU(2) model: throughout the signed interval |τ|≤10⁻⁸, its physical gap is at least α/16, uniformly over the declared nonempty complete-factor volumes. The proof retains every omitted interaction, the actual ground-energy shift, and the removal of representation cutoffs. It derives a four-site creation bound rather than importing an SU(3) constant.

The final two investigations, AQ1 and AQ2, then construct a locally normal full-lattice state at this same numerical cap and pass the bound to its actual physical GNS generator:

\[
H_{\mathrm{phys}}\geq\frac{\alpha}{16}(I-P_\Omega),
\qquad
\operatorname{Var}_{\omega}(W)\geq\frac{61999}{250000}>\frac15.
\]

Here W is the original xz Wilson loop in that same state. Its complete local cover has 48 links, 36 original endpoints and seven incident interaction stars. The proof first obtains a reference-energy budget of 98|τ|, converts it to a trace-distance bound of at most 1/500, and transfers the reference Wilson moments 0 and 1/4 as inequalities. This gives the displayed variance floor. The gap passage separately uses centered spectral tests that include zero energy; leaving zero out would fail to establish a simple vacuum.

This is a conservative fixed-spacing result for a particular constructed representation. The creation-expansion methods are established, and the general compactness/GNS/gauge-averaging/Fourier route already appears in Gauvin's Supplement A.10, with dynamics supplied by Nachtergaele–Sims and Nachtergaele–Sims–Young. Our contribution is the audited model-specific application and constants. We have not proved uniqueness of every thermodynamic state, independence of boundary choices, or a weak-coupling continuum limit.

A separate new result, AO2, proves the exact first-moment identity αω(1−W²) and operator-domain membership for the older conditional orthant state. That is a different construction with additional hypotheses; its energy identity has not been transferred to the numerical-cap state above.

## Why publish the notebook?

I want the useful part to be inspectable: which assumptions were used, which terms survive, which proposed extensions failed, and exactly what each calculation establishes. Potential uses include testing long-time perturbative approximations and designing error budgets for regulated gauge-theory simulators; practical usefulness still needs its own validation.

The revised draft also compares the work with [Shoshauna Gauvin's arXiv:2503.15539v3](https://arxiv.org/abs/2503.15539v3). That paper discusses regulated gap certificates and conditional continuum transfer, with important methodological overlap. Its results keep their original authorship. The general spectral and perturbative tools used here are established methods; the priority of project-specific refinements is unverified.

The [Clay problem statement](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf) remains the standard for what a solution would require. Our work does not yet meet it.

Human author and project direction: **Hruday N M (BUNZEEY)**. Research, coding, and drafting used AI assistance. U2's original derivation and critical review were by the same model author; later independent model-agent reviews share model ancestry and are not external human peer review.

- [Read the complete revised draft](https://occult-kranti.github.io/yang_mills_workbench/ym-draft-02.pdf)
- [Explore the research website and priority table](https://occult-kranti.github.io/yang_mills_workbench/)
- [Inspect the code, contracts, and evidence](https://github.com/occult-kranti/yang_mills_workbench)

I would especially welcome criticism of the complete-factor counting, limiting argument, and model-matching assumptions—and pointers to prior results that sharpen the novelty assessment.
