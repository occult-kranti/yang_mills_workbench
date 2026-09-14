# D1 reverse reconstruction: the embedding needed for a resolvent claim

A desired norm-resolvent conclusion on the A2 Hilbert representation first
requires a common self-adjoint reference on one domain. Define the lift using
all exterior positive reference factors, not the tensor identity alone:

\[
H_L=K_L\otimes I+I\otimes H_{\mathrm{ref,out}},\qquad
K_L=\sum_{i\in I_L}h_i+V_L.
\]

Each omitted face anchored at coordinates `0..L` has four links. Classify each
link by the unique complete reference factor containing it: a three-square xy
strip has six x-links and four y-links; all other links are single free factors.
Closing the face support under those factors uses at most forty links per face.
This proves finite factor count. Each link space is `L^2(SU(2))`, so the finite
factor Hilbert space is still infinite dimensional. Every factor eventually
appears because every free link and strip support touches an omitted face.

This prescription preserves every coefficient of A2, including faces with an
anchor at the cutoff whose links cross its coordinate boundary. It is not the
literal original clipped-box Hamiltonian.

For an independent tail calculation, partition omitted faces directly into
three disjoint classes: all xz/yz faces, odd-y xy faces, and even-y xy faces at
x=3 modulo 4. Write

\[
S_L=2(1-2^{-L-1}),\quad
Y_L={4\over3}(1-4^{-\lfloor L/2\rfloor-1}),\quad
X_L={2\over15}(1-16^{-\lfloor(L+1)/4\rfloor}).
\]

Here `Y_L` sums even y and `X_L` sums separator x. The retained omitted-face
weight and exact tail are

\[
W_L={2S_L^3+S_L(S_L-Y_L)S_L+X_LY_LS_L\over24},\qquad
t_L={107\over135}-W_L.
\]

The three infinite weights are respectively `2/3`, `1/9`, `2/135`.
Thus `t_L` decreases to zero and is strictly positive at finite L. The checker
compares the product formula against coordinate enumeration for L=0 through 8,
constructs all closures, and reconstructs the first L reaching each requested
energy tolerance.

Since `|x_f|<=1`, the exact omitted coefficient sum yields
`||H-H_L||=||V-V_L||<=epsilon_L=alpha*|tau|*t_L`. Signed cancellation is
unavailable in this operator-norm estimate. Both operators are self-adjoint on
`D(H_ref)` by bounded perturbation. For a common nonreal physical energy z,

\[
R_H(z)-R_{H_L}(z)=-R_H(z)(V-V_L)R_{H_L}(z),\qquad
\|R_H(z)-R_{H_L}(z)\|\le{\epsilon_L\over|\Im z|^2}.
\]

The executable scale example fixes `alpha/E_star=2`, `tau=1/64`, and
`Im(z)/E_star=1/2`. Hence `epsilon_L/E_star=t_L/32` and the dimensionless
resolvent discrepancy `E_star*||R_H-R_HL||` is bounded by `t_L/8`.
Neither static kappa nor a spiral index defines this energy scale.

An exterior-vacuum embedding is useful for states but does not justify deleting
`H_ref,out` as an operator on the full representation. On a free exterior link,
Casimir eigenvalues `alpha*j(j+1)` are unbounded. Deleting that generator leaves
an unbounded difference, defeating the bounded-tail argument. This obstruction
is retained, along with controls for crossing-support deletion, signed
cancellation, zero energy reference, and false finite-dimensionality.

This result concerns the specified summable product representation. It proves
neither the original clipped-box limit nor a homogeneous or continuum theory.
