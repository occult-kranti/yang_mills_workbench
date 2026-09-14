# M1 forward: strong convergence on the canonical H2 profile

The proposed strong limits hold in the fixed A2 full-link incomplete tensor product. They coexist with the nonzero perturbation norm `alpha eta/8`. No operator-norm resolvent or propagator conclusion is obtained. This report was derived independently before reading reverse M1.

## Fixed model and inherited premises

Keep the selected complete-strip Hamiltonian `H_ref`, reference ground `Omega`, spacing, `E_star>0`, `alpha/E_star>0`, `hbar>0`, and `0<eta<1` fixed. All limits below are `q` increasing to 1 through `0<q<1`. The dimensionless action-profile parameter and matched budget coefficient are

\[
w_f(q)=q^{x+y+z}/24,\quad
B(q)=\frac{2+5q+5q^2+6q^3+3q^4}
 {24(1-q)^3(1+q)^2(1+q^2)},\quad
\tau_q=\frac{\eta}{8B(q)},\quad
V_q=-\alpha\tau_q\sum_{f\in O}w_f(q)x_f.
\]

Here q is a spatial coefficient deformation and tau is fixed by its budget, not a clock or a lattice-spacing regulator. H1 supplies the exact omitted-face ledger and `(1-q)^3 B(q)->7/64`. H2 supplies

\[
\sigma_q^2:=\|V_q\Omega\|^2
=\frac{\alpha^2\tau_q^2B(q^2)}{96},\quad
\|V_q\|=M:=\alpha\eta/8,\quad
-\sigma_q^2/\bar g\le e_q\le0,
\qquad \bar g=\alpha(1-\eta)/8>0.
\tag{1}
\]

Consequently `tau_q=O((1-q)^3)` and `sigma_q=O(alpha(1-q)^(3/2))`; exactly,

\[
\frac{\sigma_q^2}{\alpha^2(1-q)^3}\longrightarrow
\frac{\eta^2}{5376}.
\tag{2}
\]

These are admitted infinite-model premises, not new conclusions inferred from finite fixtures. A2 fixes the self-adjoint `H_ref`, its dense finite tensor core and the tensor factorization. G2 justifies density of the orbit of Omega under the full bounded local-factor algebra. J2's physical-sector method remains scoped to the invariant subspace and its energy shift; no conditional K/L diffusion is identified with this Hamiltonian.

## Complete support makes the commutator finite

A complete strip at anchor `(4i,2j,z)` owns six x-links at `x=4i,4i+1,4i+2`, `y=2j,2j+1`, and four y-links at `x=4i,...,4i+3`, `y=2j`, all at height z. Thus it has ten links. Every z-link, every y-link on an odd row, and every x-link with tail x congruent to 3 modulo 4 is a free one-link factor. This partitions all positive-orthant links. Selected faces are xy faces on even y rows with x residue 0, 1 or 2 modulo 4; all others are omitted.

Let F be a finite set of complete reference factors and let E(F) contain **all** their links. A bounded A on those factors commutes with x_f whenever f has no link in E(F). This implication uses complete factors: an arbitrary operator on a dressed strip may act on links absent from the displayed Wilson loop.

For a link with axis a and tail p, each transverse axis b permits only the two elementary faces with anchors p and `p-e_b`, when the latter remains in the nonnegative orthant. Hence every link belongs to at most four faces; boundary links have fewer. Define the finite set and budget

\[
\mathcal I_F=\{f\in O:\operatorname{links}(f)\cap E(F)\ne\varnothing\},
\qquad D_F(q)=\sum_{f\in\mathcal I_F}w_f(q).
\]

Each face is counted once. Since `w_f(q)<=1/24`,

\[
|\mathcal I_F|\le4|E(F)|,\qquad
D_F(q)\le |E(F)|/6.
\tag{3}
\]

The checker independently reconstructs this partition and compares incidence lists with direct face enumeration. The boundary xz face at `(0,0,0)` has four displayed links but its complete factor cover has 22 links: two ten-link strips and two free z-links. The omitted xz face at `(2,1,0)` meets that full cover while missing every displayed link. An edge-only count is therefore rejected. Fixtures illustrate the complete-cover issue; the all-link incidence argument proves (3).

For fixed q the infinite perturbation series converges in operator norm. Its commutator with A is precisely the finite sum over `I_F`, so

\[
\begin{aligned}
\|V_qA\Omega\|
&\le\|A\|\|V_q\Omega\|+\|[V_q,A]\|\\
&\le\|A\|[\sigma_q+2\alpha\tau_qD_F(q)]\\
&\le\|A\|[\sigma_q+\alpha\tau_q|E(F)|/3]
\longrightarrow0.
\end{aligned}
\tag{4}
\]

The factor 2 follows from `||[x_f,A]||<=2||x_f||||A||<=2||A||`; tau is positive on this canonical ray. This argument does not require strict positivity of the strip wavefunction or a multiplier-density assumption.

## Dense vectors imply strong perturbation convergence

On any finite set F, the bounded rank-one operator `|xi_F><Omega_F|` sends its product ground to any chosen finite-factor vector xi_F. Their finite linear combinations are dense in the A2 incomplete tensor product. This is Hilbert-space density, not a claim that arbitrary bounded A preserves the unbounded Hamiltonian domain.

Equation (4) therefore gives convergence on a dense set. For any fixed psi and a dense approximant phi,

\[
\|V_q\psi\|\le M\|\psi-\phi\|+\|V_q\phi\|.
\]

First take q to 1, then phi to psi. Thus

\[
\boxed{V_q\longrightarrow0\ \text{strongly},\qquad
\|V_q\|=\alpha\eta/8>0.}
\tag{5}
\]

The vector is fixed before the limit. H2's almost norm-maximizing localized vectors depend on q and cannot be substituted into (5).

## Resolvents and fixed compact time intervals

Every V_q is bounded self-adjoint. Therefore `H_q=H_ref+V_q` is self-adjoint on exactly `D(H_ref)` and has the same quadratic-form domain. For nonreal z, put `R_q(z)=(H_q-z)^(-1)`. The resolvent identity gives

\[
R_q(z)-R_0(z)=-R_q(z)V_qR_0(z),\qquad
\|(R_q-R_0)\psi\|\le
\frac{\|V_qR_0(z)\psi\|}{|\operatorname{Im}z|}\longrightarrow0.
\tag{6}
\]

This proves strong-resolvent convergence without a spectral compactness assumption. The numerator involves a fixed vector. It is not bounded by a quantity tending to zero uniformly on the unit sphere.

Write `U_q(t)=exp(-itH_q/hbar)`. Bounded-perturbation Duhamel, initially on the common domain and then by density, gives for every fixed psi and finite T

\[
\sup_{|t|\le T}\|(U_q(t)-U_0(t))\psi\|
\le\frac{T}{\hbar}
\sup_{|s|\le T}\|V_qU_0(s)\psi\|.
\tag{7}
\]

The reference orbit `{U_0(s)psi: |s|<=T}` is compact in Hilbert norm by strong continuity. A uniformly bounded strongly vanishing family converges uniformly on each compact set: choose a finite epsilon-net and bound the remaining error by M times its mesh. Thus the right side of (7) tends to zero. This proves compact-time uniform **strong**, not operator-norm, unitary convergence.

The optional ground-energy subtraction gives `U_tilde_q(t)=exp(it e_q/hbar)U_q(t)`. From (1), `|e_q|<=sigma_q^2/gbar->0`, and

\[
\sup_{|t|\le T}\|(\widetilde U_q(t)-U_0(t))\psi\|
\le\sup_{|t|\le T}\|(U_q(t)-U_0(t))\psi\|
+\frac{T\sigma_q^2}{\hbar\bar g}\|\psi\|
\longrightarrow0.
\tag{8}
\]

The domains are unchanged by this scalar shift. It matters for the ground-vector phase and cancels in observable conjugation. Connected correlator transfer and growing time windows are left for an evidence-selected M2.

## Discriminating controls and scope

The checker uses `P_n=|e_n><e_n|` on ell2 to distinguish quantifiers: `P_n` annihilates every fixed finitely supported vector eventually, while `||P_n e_n||=||P_n||=1`. With `H_ref=0` and `V_n=P_n`, the squared norm of the resolvent difference at z=i is exactly 1/2; the unitary norm difference at t=pi and hbar one is 2. Strong convergence does not imply either norm conclusion.

Conversely, for fixed diagonal `H_ref e_n=n e_n` and the same V_n, the squared resolvent-norm difference at i is exactly `1/[(n^2+1)((n+1)^2+1)]`, which tends to zero although `||V_n||=1`. Nonzero perturbation norm therefore cannot prove norm-resolvent failure in the actual profile. M1 leaves both norm-resolvent and propagator-norm status unresolved. The controls are exact abstract counterexamples, not replacements for the lattice proof.

For each fixed omitted face, `alpha tau_q w_f(q)->0`; the selected strips stay fixed. The endpoint is the selected-strip reference, not a nonzero homogeneous omitted coupling and not necessarily a free Haar state. Spacing is fixed; no continuum, physical mass measurement or K/L diffusion matching follows. The q=1 coefficient series itself is outside the summable family. Zero physical energy reference, zero hbar, eta outside `(0,1)`, and q outside `(0,1)` are rejected.

This contribution is the complete-support commutator extension of H2's reference-vector residual to the full fixed Hilbert space, followed by applications of the resolvent identity and Duhamel. These are established operator tools; scientific priority is unverified. The infinite theorem is proved in (3)–(8), not inferred from the finite numerical fixtures.

The H1/H2/G2/A2 and J2 reports were read in depth for the stated premises. Their relevant admitted report hashes are checked against their gates; no earlier full study is re-audited. `check.py` uses its own standard-library geometry/profile implementation and imports no other research implementation. The source manifest binds code, this report, frozen contract, selection evidence, method snapshot, inherited reports/gates and every generated output.

```bash
python3 -B research/round21/forward/m1/check.py --output /absolute/new/m1-forward-output
```

Normal and optimized execution are repeat validation of this one M1 loop. M2 has not been selected or executed.
