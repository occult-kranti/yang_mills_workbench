# Independent B2 review: a shared-face adjoint trial

This calculation keeps the full physical Hamiltonian on the actual dense two-cube graph fixed. It adds a trial vector, not an interaction, auxiliary field, or adjustable physical constant. The model is SU(2), eleven normalized fundamental plaquette traces (x_p=\operatorname{Tr}U_p/2\), and

\[
H=\alpha\sum_{e=1}^{20}C_e-\frac{12\alpha}{43}\sum_{p=1}^{11}x_p,\qquad\alpha>0.
\]

The previous independent graph constructor/validator is retained locally in `geometry.py`. The new integral and matrix algorithms are independent of the forward producer. The shared face is located by its four geometric vertices at x=1, after checking every signed edge of every square. Face names are not sufficient evidence.

## New Haar obligations

Let (s) denote that shared face and (z=\chi_2(U_s)=4x_s^2-1\), where the character has dimension three and spin one. Normalized SU(2) Haar moments are (m_2=1/4,m_4=1/8\), with all odd moments zero. Thus

\[
\langle z\rangle=0,\quad\langle z^2\rangle=16m_4-8m_2+1=1,
\quad\langle z\chi_s\rangle=0.
\]

For every pair of distinct actual faces, either face has a link absent from the other. Holding the other links fixed and integrating that exclusive link makes its face holonomy Haar distributed. Consequently the two-face moment factors, including

\[
\langle x_p^2x_s^2\rangle=m_2^2=1/16\quad(p\ne s).
\]

This is a conditional Haar argument, not an inference from distinct-face parity or a claim that all faces of the two-cube graph are independent. The code checks the exclusive edge in the actual incidence graph for each use. For the remaining polynomial monomials of degree at most five, an odd incidence on any actual link makes the integral zero under that link's center transformation (U_e\mapsto-U_e\). Any unsupported surviving multi-face monomial causes an error instead of an invented zero.

These integrals give an orthonormal thirteen-vector basis (\{\Omega,\chi_p,z\}\). They give all 1,859 magnetic insertions, including repeats:

\[
\langle\Omega,x_f\chi_p\rangle=\tfrac12\delta_{fp},\qquad
\langle z,x_f\chi_p\rangle=\tfrac12\delta_{fs}\delta_{ps},
\qquad\langle z,x_fz\rangle=\langle\Omega,x_fz\rangle=0.
\]

In particular, the potential coupling of the new state to the shared fundamental state is (-\lambda_s/2\). The potentially nontrivial case (p=f\ne s\) vanishes because (8(1/16)-2(1/4)=0\), not because every exponent is odd. The adjoint character is an electric eigenfunction with four spin-one edges: (H_0z=4\alpha(1)(2)z=8\alpha z\). Applying the fundamental energy (3\alpha\) to this state would be wrong.

## Exact full-gap lower bound

The independent full physical min-max bound remains (E_1(H)\ge3\alpha-11(12\alpha/43)=-3\alpha/43\). It is not an excited Ritz eigenvalue. The physical free gap (3\alpha\) follows from the graph's girth four and the Gauss-law active-support argument already accepted in B1.

At \(\alpha=1\), write (e=-3/43\) and

\[
v_0=\Omega+\frac1{22}\sum_p\chi_p,\quad G=\|v_0\|^2=\frac{45}{44},
\quad\langle z,Hv_0\rangle=-\frac3{473}.
\]

The old twelve-dimensional matrix obeys (H_{12}v_0=ev_0\). In the actual full operator, the Rayleigh numerator of (v_\eta=v_0+\eta z\) is therefore

\[
N(\eta)=eG-\frac6{473}\eta+8\eta^2,\qquad
R(\eta)=\frac{N(\eta)}{G+\eta^2}.
\]

The norm is positive for every real amplitude. Rayleigh–Ritz bounds the full ground energy above by (R\), so the separate full (E_1\) lower bound yields

\[
\Delta(H)\ge e-R(\eta)=
\frac{(6/473)\eta-(347/43)\eta^2}{45/44+\eta^2}
=\frac{(347/43)\eta(6/3817-\eta)}{45/44+\eta^2}.
\]

The factorization proves positivity throughout the open interval (0<\eta<6/3817\). It is an algebraic interval proof, independent of the amplitude plot. At either endpoint this particular bound is zero; outside the interval it is negative. Those amplitudes remain valid quantum states and do not demonstrate gap closure. Scaling restores the exact physical bound by multiplication with \(\alpha>0\).

The convenient rational choice \(\eta=3/3817\) maximizes the quadratic numerator. It does not maximize the quotient: at this positive amplitude the numerator derivative is zero and the denominator derivative is positive, hence the quotient derivative is strictly negative. No optimum claim is used.

## Verification and limitations

The runnable verifier expands every basis polynomial, recomputes the Gram and magnetic matrices from link incidence and Haar moments, and calculates the exact Rayleigh polynomial by matrix multiplication. It checks sign endpoints, negative amplitudes, physical scaling, malformed graph metadata, and deliberately wrong normalization/energy/mixed-coupling controls. Exact fractions are authoritative; the plot samples do not prove the interval statement.

This establishes a strictly positive sufficient bound at one finite dense graph and the previous variational endpoint. It does not provide a volume-uniform dense-interaction theorem, a continuum construction, or a Millennium-problem solution. No new unplanned C-loop calculation is included.

The accepted rational value is

\[
\Delta(H)\ge\alpha\frac{1388}{284767457}
\approx4.8741524562618824\times10^{-6}\alpha.
\]

The independent verifier passes **25 named checks**. Its separate producer comparison passes **20 named checks**, including every saved Haar entry, all nine parameter-bound matrix certificates, and the seven-row producer amplitude ledger. Ordinary and optimized Python produce byte-identical semantic outputs; the two execution modes are not counted twice. The independent polynomial oracle and the producer's character-fusion oracle agree exactly. No material discrepancy was found in this B2 comparison. The tested wrong-energy, omitted-coupling and malformed-certificate cases are deliberately broken controls, not reported discoveries of bugs.

The focused source review covered the new independent `shared_face`, `haar`, `moment`, polynomial multiplication, `entries`, `bilinear`, `compute`, CLI checks and complete comparison reconstruction; and the producer's source guard, rational/index validation, geometric shared-face selection, character-polynomial matrix construction, exact Rayleigh quotient and certificate replay. The producer checks its pinned graph/Haar/current-source bytes before serving a cached matrix moment. The copied earlier Haar engine is an accepted dependency, not a newly audited full file in this phase. The review establishes this specified finite calculation and does not claim a universal audit of the whole repository.

Run `python check.py --output ../b2-reproduced` from this source directory. Run `python compare.py --producer <forward-b2-source> --evidence <forward-b2-output> --output ../b2-comparison-reproduced` for the separate cross-implementation check. Each destination must be a new directory outside the frozen source directory.
