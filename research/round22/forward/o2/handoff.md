# Forward O2 frozen handoff

Homogeneous I1/I2/O1 model; no q-profile transfer. Arbitrary-support local
splitting keeps scalar cI, mixing A and vacuum-annihilating Z, with norms
|c|,||A||,||S||<=||R_Y|| and ||Z||<=2||R_Y||. Bare inverse gap is exactly
at least one. Simultaneous finite-volume rotation preserves D(H0).

An equal-weight universal commutator estimate is false on growing supports.
With loss delta_w, the derived bound is 4/delta_w. All nested terms give
rho=12r/delta_w and r_next<=(d+3r/2)rho/(1-rho), with d_next<=d+2r and
kappa_next<=kappa+2r. The retained D term is essential.

Limited verdict: this scalar majorant must eventually lose rho<1 for any
positive d0,r0 under every positive summable loss schedule, because its
linear factor is at least 12d0/delta_n -> infinity. This does not prove
actual algorithm or homogeneous-gap failure. The controlled rational
recurrence at tau=2^-22 reaches first rho failure at step 42 after its
minimum residual at step 15. The exact-log recurrence also eventually fails,
but its first failure index is not claimed to be 42.

Nine checks pass in ordinary and optimized fresh executions; all three
outputs match byte-for-byte. Only ordinary output and optimized-summary.json
are retained. No current reverse O2 solution read. No next loop selected.
