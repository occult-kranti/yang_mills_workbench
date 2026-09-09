## A fully quantum comparator that challenges mean-field validation

Gralla and Mizuno's revised April 2026 analysis uses bosonization in massive $1+1$-dimensional QED to compute a controlled first-order-in-mass correction in a strong external field. Its frequency correction is absent in the corresponding semiclassical calculation. This is a useful adversarial comparator: reproducing an anomaly or conserving mean-field energy cannot certify that a massive mean-field model contains all relevant quantum physics. It is not a numerical error bar for our $3+1$-dimensional Landau model. [@N01]

### Reduction, periodicity and a separate numerical scheme

Use the source's positive charge $q$, electric-field parameter $E_C$ and bosonization mass $M=q/\sqrt\pi$. Define

$$\tau=Mt,\qquad A=\frac{2\pi E_C}{q},\qquad
g=2e^{\gamma}\sqrt\pi\,\frac{m}{q},\qquad
z=2\sqrt\pi\langle\phi\rangle+A.$$

Here $g$ is the comparator's mass-expansion parameter, not the WGC gauge coupling or the metric. The first-order effective equation becomes

$$z''+z+g\sin(z-A)=0,\qquad z(0)=A,\quad z'(0)=0,$$
$$V(z)=\frac{z^2}{2}-g\cos(z-A),\qquad
\frac{z'^2}{2}+V(z)=V(A).$$

For the tested $|g|<1$, $V''\geq1-|g|>0$. The nonstationary trajectories between two regular turning points are periodic. This avoids silently applying a blanket claim that every bounded one-dimensional trajectory is periodic: equilibrium and separatrix cases need separate treatment in more general potentials.

The source predicts

$$\frac{\omega}{M}=1+g\cos A\,\frac{J_1(A)}A+O(g^2).$$

The project implemented two independent period measurements: a time-domain DOP853 solution with successive minimum events, and an energy integral between the turning points. A sine-type turning-point substitution removes the square-root endpoint singularity before 128/256-node Gauss–Legendre integration. The code does not infer frequency from a visually fitted plot.

### Executed results and their proper meaning

Fifteen cases use $A=0.5,2,5$ and $g=0,0.02,0.01,0.005,0.0025$. The maximum period difference between the two numerical methods is $1.21\times10^{-11}$. The observed small-$g$ remainder orders approach 1.985, 2.007 and 2.001 for the three amplitude sequences, consistent with the stated second-order remainder.

| Amplitude, at $g=0.0025$ | Numerical $\omega/M$ | First-order prediction |
|---|---:|---:|
| $A=0.5$ | 1.001063299799 | 1.001063052869 |
| $A=2$ | 0.999700230880 | 0.999699997245 |
| $A=5$ | 0.999953598003 | 0.999953539093 |

All four declared comparator gates passed. Solving the truncated nonlinear equation accurately also generates higher powers of $g$ numerically. Those powers are not derived higher-order predictions of full QED. The comparator establishes a reproducible first-order challenge and a numerical check of its effective equation, not a new all-orders quantum solution.

### Questioning the argument rather than merely citing it

The source's small-mass comparison needs care near zero momentum: a pointwise expansion in $m/k$ is not uniform at $k=0$. The independent verifier supplies a compact-momentum finite-time bound. With $u=r_x+ir_y$ and $u'=2ipu-2imr_z$, initial vacuum data and unit norm give

$$|u(t)|\leq\frac{|m|}{\sqrt{k^2+m^2}}+2|m|T,$$
$$\int_{-K}^{K}|r_z(t)-r_z(0)|dk
\leq4m^2T\,\operatorname{asinh}(K/|m|)+8Km^2T^2=o(|m|).$$

This repairs the compact region's order estimate at fixed $K,T$. It does not justify exchanging the limit with an infinite ultraviolet integral or extending it to secular times $T\sim1/m$. Those are additional estimates, not automatic consequences of the paper's headline result.

The revised source also warns that a conserved classical-looking effective total energy need not split into the separate quantum field and matter expectation values by naive replacement of operators with their means. In particular, a normal-ordered quadratic expectation can contain a variance term beyond the square of the expectation. We therefore use the comparator's period and total effective energy, without identifying each nonlinear-potential term as a separately measured quantum energy. [@N01]

