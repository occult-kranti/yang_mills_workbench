# B2 decision snapshot

Status: accepted for Goal B loop 2 only.

The accepted B1 strict-cutoff projector and exact cross Gram support a finite two-cube continuous coefficient-box gap certificate. The proof works on the finite graph Hilbert space with the standard electric operator/form domain; the magnetic terms are bounded multiplication operators. On `Omega^perp`, write `R=P\ominus Omega` and `Q=1-P`. The accepted B1 evidence gives `dim P=48`, `dim R=47`, eleven face channels at `3 alpha`, thirty-six six-cycle channels at `9 alpha/2`, and `QH0Q >= 6 alpha`.

For `|lambda_f| <= r alpha`, both producers agree on the exact row-envelope certificate

\[
a(r)=3-2r,\qquad d(r)=6-11r,\qquad w(r)=\frac{19}{4}r^2.
\]

The Schur/min-max lower bound on `Omega^perp` is

\[
R(r)=\frac{9-13r-\sqrt{100r^2-54r+9}}2,
\]

positive while

\[
18-45r+\frac{69}{4}r^2>0,
\]

namely for `0 <= r < (30-2 sqrt(87))/23`. This range is a certificate range for the finite row-bound method. It is not a uniform positive floor as `r` approaches the endpoint and is not a dense, limiting, continuum or physical-scale closure result.

Concrete accepted boxes:

- required primary box `r=1/8`: `E1/alpha >= (59-2 sqrt(61))/16`, outward interval `[2.711218790511668, 2.711218790511669]`;
- Round18 benchmark box `r=3/8`, rederived with enlarged 48-state `P`: `E1/alpha >= (33-6 sqrt(5))/16`, outward interval `[1.223974508437578, 1.223974508437579]`;
- wider control `r=7/16`: exact `E1/alpha >= 19/32`;
- `r=1/2`: same certificate is insufficient, determinant `-3/16`; this is not a no-gap theorem.

The ground upper bound is kept separate: the vacuum Rayleigh quotient gives `E0 <= 0` because `H0 Omega=0` and face-character Haar means vanish. Thus the finite-graph gap lower bound is admitted as `lambda_1-lambda_0 >= E1_lower - E0_upper`, with `E0_upper=0` here.

The ordinary and optimized producer outputs replay byte-for-byte. The final independent comparison accepts 26 checks and reconstructs B1 bindings, block levels, the full 47-row envelope table, all 208 compressed `PVP_RR` entries, exact certificates, scale checks, source bindings and mutation controls.
