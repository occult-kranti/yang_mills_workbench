# Forward B2: continuous signed box from the accepted 48-channel projector

This executes the frozen `ym19-b2-contract-v1` forward loop. It uses the accepted B1 disk hashes for the actual two-cube graph, the 48-dimensional strict-cutoff projector, the full compressed PVP ledger and the exact ordered cross Gram. It does not start C1 and does not claim homogeneous dense stability, a limiting spectral passage, continuum Yang-Mills or the Clay mass gap.

## Operator split

Write `R=P-Omega`, so `dim R=47`. On `Omega^perp`, a normalized vector has components `u in R` and `q in Q=1-P`. In units of `alpha`, the accepted B1 projector gives 11 four-edge channels at energy 3 and 36 six-edge channels at energy `9/2`; the complement has `H0 >= 6`.

For the signed box `|lambda_f| <= r alpha`, the B1 compressed PVP ledger gives the exact row envelope

\[
RHR \ge (3-2r)\,I_R.
\]

This uses the full 47-by-47 compressed PVP row sums, including face-six and six-six couplings; it is not the old Round18 constant face block. On the complement,

\[
QHQ \ge (6-11r)\,I_Q,
\]

because each `x_f=chi_f/2` has operator norm at most one. The accepted B1 exact Gram gives

\[
\|QVRu\|^2 \le {19\over4} r^2 \|u\|^2.
\]

Thus the codimension-one min-max lower bound on `Omega^perp` is the lower eigenvalue of

\[
\begin{pmatrix}
3-2r & -\sqrt{19/4}\,r\\
-\sqrt{19/4}\,r & 6-11r
\end{pmatrix}.
\]

Equivalently,

\[
E_1(H)/\alpha \ge R(r)
={9-13r-\sqrt{100r^2-54r+9}\over2}.
\]

The determinant condition is

\[
(3-2r)(6-11r)-{19\over4}r^2
=18-45r+{69\over4}r^2>0,
\]

so this certificate is positive for

\[
0\le r < {30-2\sqrt{87}\over23}\approx 0.493271386688.
\]

## Certified boxes

The required continuous box is certified:

\[
|\lambda_f|\le {\alpha\over 8}\quad\Longrightarrow\quad
E_1(H)/\alpha \ge {59-2\sqrt{61}\over16}\approx2.711218790512.
\]

The Round18 `3/8` benchmark is rederived under the enlarged B1 projector rather than imported from Round18:

\[
|\lambda_f|\le {3\alpha\over8}\quad\Longrightarrow\quad
E_1(H)/\alpha \ge {33-6\sqrt5\over16}\approx1.223974508438.
\]

A wider useful rational box is also certified:

\[
|\lambda_f|\le {7\alpha\over16}\quad\Longrightarrow\quad
E_1(H)/\alpha \ge {19\over32}.
\]

The same row-envelope method does not certify `r=1/2`; there the determinant is `-3/16` and the lower expression is negative. This is recorded as a failed stronger bound, not as a no-gap theorem.

## Ground upper bound and gap direction

The ground upper bound is separate. The vacuum Rayleigh quotient gives

\[
E_0(H)\le \langle\Omega,H\Omega\rangle=0,
\]

since `H0 Omega=0` and every face character has Haar mean zero. Therefore the finite two-cube gap bound is

\[
\lambda_1(H)-\lambda_0(H)\ge E_1^{\rm lower}-E_0^{\rm upper}=E_1^{\rm lower}
\]

on each certified signed coefficient box.

## Evidence

Run from this directory:

```bash
python -B check.py --output /absolute/new/output_dir
```

Generated files:

- `results.json`: theorem statement, scale register, B1 gate bindings, E0/E1 bounds and non-claims;
- `block-envelopes.json`: exact PVP and Gram row/column envelopes from the accepted B1 ledgers;
- `block-certificate.json`: comparator-facing primary, benchmark and parameter-envelope certificates;
- `certificates.json`: exact formulas for `r=1/8`, `r=3/8`, `r=7/16`, the positive interval and failed `r=1/2` attempt;
- `compressed-pvp-RR.json`: full compressed PVP nonzero ledger on `R=P-Omega`;
- `pvp-linear.json`: compact full 48-by-48 PVP nonzero ledger;
- `row-envelopes.csv`: per-row exact envelope data;
- `controls.json`: wrong-model and sign-direction controls;
- `source-manifest.json`: source, report, B1 gate and B1 input hashes.
