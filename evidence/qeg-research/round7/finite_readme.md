# Round-7 finite scalar bridge

This run evaluates the finite variational model with inclusive Landau levels,
an independent Gauss grid, and `f(phi)=1+g^2 phi^2`.  It uses
`p=k-a`, `h=(M,0,p)`, `S=sum(w*(rz+p/omega))`,
`C=sum(w*M^2/(4*omega^5))`, and `D=sum(w*5*M^2*p/(8*omega^7))`.
The scalar equations are `phi'=y` and
`y'=-nu^2 phi + f_phi*(x^2-b^2)/2`; the potential equation includes
`-f_phi*y*x` in `Z*x'`.  The shifted energy is
`Wtilde=Z*x^2/2+e2*sum(w*(h.r+omega))+y^2/2+
(nu^2+g^2*b^2)*phi^2/2`, and its expected work is `x*F`.

The wrong-control CSV removes only `-f_phi*y*x` from the potential equation.
Its expected defect is `f_phi*y*x^2`, integrated in an independent state and
compared with the observed energy mismatch.  Bloch norms are raw values; no
clipping or projection is applied.  The zero-drive gate checks the harmonic
solution with `Omega^2=nu^2+g^2*b^2`, and the g=0 gate compares the actual
archived round-6 solver with a required successful import and comparison.

Acceptance thresholds and failures are recorded in `finite_results.json`.
Current status: **passed**.  The scalar data are nondegenerate
(`phi0=0.4`, `y0=0.1`); the model is not a derived continuum-QED or
gravitational closure.
