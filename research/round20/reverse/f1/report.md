# F1 reverse reconstruction: an invariant measure does not determine a clock

Retain exactly the C1 conditional state space `SU(2)^3`, with shared U,V,W and
`S=3x+y+z+w+t`. This is a conditional link model, with no newly asserted Gauss
sector. Let `rho_k=exp(kS)/Z_k` relative to normalized product Haar. Its density
is smooth, strictly positive and bounded above and below on this connected
compact manifold, for every finite real k.

On `L^2(rho_k dHaar)`, define the closed form

\[
q_k[f]=\int |\nabla f|^2\rho_k\,dHaar,\qquad D(q_k)=H^1(SU(2)^3).
\]

Weighted and unweighted Sobolev norms are equivalent, so this domain is closed
and smooth functions are a form core. The nonnegative self-adjoint operator
associated to the form is

\[
A_k=-\rho_k^{-1}\operatorname{div}(\rho_k\nabla)
    =-\Delta-k\nabla S\cdot\nabla.
\]

Integration by parts supplies symmetry and the form identity. Vanishing form
energy implies a constant function by connectedness; constants are therefore
the unique zero mode. A Haar Poincare comparison also proves a positive gap:
if `m<=rho<=M`, `gap(A_k)>=(3/4)m/M>0`, with the Casimir normalization fixed
by the contract. This construction is standard diffusion theory; see the
primary context in [Ledoux, section 1.1](https://www.numdam.org/item/AFST_2000_6_9_2_305_0.pdf).
Only that targeted section was consulted, and no literature-priority claim is
made for the present conditional model.

For every externally supplied positive energy coefficient c,

\[
H_{k,c}=cA_k,\qquad T_t=\exp(-tcA_k/\hbar)
\]

has exactly the same invariant density and static moments. Its excitation
energies multiply by c. In weighted representation the ground function is 1;
in Haar representation it is `sqrt(rho_k)`, independent of c. Thus even
restricting to local reversible differential generators leaves the physical
energy/time coefficient underidentified.

The exact dynamic discriminator is k=0, for which `x=Tr(U)/2` has Haar mean
zero, variance 1/4 and Casimir eigenvalue 3/4. Its stationary autocorrelation is

\[
C_c(t)={1\over4}\exp[-3ct/(4\hbar)].
\]

The two choices `c/E_star=1` and `2` share all static observables while their
initial normalized decay rates are `3/4` and `3/2` in `E_star/hbar` units.
An independently measured time correlation or matched coefficient is required
to select c. The known A2 coefficient alpha and the dimensionless k are not
such a calibration simply because they occur elsewhere in this investigation.

Two exact wrong-model controls are tied to the actual action. At U=V=W=I,
`grad S=0` and `Delta S=-27/4`. Reversing the drift sign leaves a nonzero
stationarity residual `27k*rho/2` there, for either nonzero sign of k. If the
correct weighted generator is instead claimed symmetric in unweighted Haar,
`<1,A_k S>_Haar=-45k/16` while `<A_k1,S>_Haar=0`. The number 45/16 is
reconstructed from the five orthogonal action terms and their one- or two-link
Casimir eigenvalues. These failures survive exact arithmetic.

At c=0 the whole operator vanishes, so its kernel is not simple and no positive
gap remains. Nonpositive c and E_star, c inferred from k or alpha without data,
and Fibonacci-based time matching are outside the admitted model. This family
is added reversible dynamics; it has not reconstructed the original Yang-Mills
Hamiltonian or a reflection-positive temporal transfer operator.
