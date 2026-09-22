# AE1 reverse: all-time Gaussian collars and the remaining volume-weight obstruction

Independent reverse work, without current forward AE1 access. The actual homogeneous initial G=H0+sum_b D_b has unbounded complete onsite blocks, bounded four-site stars ||D_b||<=M=7|tau|<=35/1664, and source A supported on Y={0,e_x,e_y,e_z}, ||A||=r. The identity extension and all retained stars remain. Physical scales are unchanged; Gaussian duration s is a proof regulator.

The result is a volume-uniform finite-collar operator and bounded-commutator approximation of the actual AB2 Gaussian inverse and residual. It also identifies a limitation: the resulting radius decay supplies exponential diameter control, but does not certify the existing exponential support-cardinality norm. This is a failure of that upper certificate, not divergence of the actual operator or every decomposition.

## The all-time premise is valid on infinite-dimensional onsite blocks

Primary reading: Nachtergaele and Sims, [arXiv:1410.8174v1](https://arxiv.org/pdf/1410.8174), Section 2 strong integral calculus and Section 3, especially the support-preserving interaction picture and iterative commutator estimate (71)-(73). Those arguments allow separable infinite-dimensional onsite Hilbert spaces with self-adjoint onsite generators and bounded interactions. They avoid differentiating an arbitrary bounded observable through the unbounded onsite operator. The explicit constants and Gaussian integration below are this report's specialization, not numbers taken from that paper. No finite-qudit theorem is substituted.

At each finite volume, onsite conjugation preserves every complete factor support and every interaction norm. Iteration of the bounded-commutator recurrence gives a sum over chains of overlapping interaction stars with factor (2|t|)^n/n!. Each site lies in at most four stars. Hence a four-site source or any succeeding four-site star meets at most sixteen anchors. This safe count includes repeats; replacing it by a growing support count would unnecessarily recreate the old finite-radius majorant.

For a fixed boundary star Z and source A, if at least R interaction stars are needed to connect Y to Z, the all-time commutator bound is

    ||[alpha_t^region(A),D_Z]||
       <=2rM sum_(n>=R) (32M|t|)^n/n!
       <=2rM 2^-R exp(v|t|), v=64M.              (AE1.R1)

The last bound uses 1_(n>=R)<=2^(n-R). It is valid at every real t, not only within a Dyson radius. Strong-integral recurrences first hold in finite volume with finite bounded interaction sums; their constants depend only on incidence and norms, not the onsite dimension or volume. At M=0 the actual source and boundary contributions vanish; no division by M is used.

## Exact collar geometry and Duhamel comparison

Let C_R={0,...,R+1}^3, R>=1, in coarse coordinates. It contains Y and (R+2)^3 complete onsite factors. Retain every star wholly contained in C_R and leave the common exterior onsite evolution unchanged. Denote this regional generator by G_R when considered on a larger finite containing volume.

Every star crossing C_R is anchored inside the cube, with at least one coordinate R+1. There are at most

    b_R=(R+2)^3-(R+1)^3=3R²+9R+7               (AE1.R2)

such stars; an outer finite boundary can only remove some. A star-chain starting on Y can increase each maximal coordinate by at most one per step. A crossing anchor has a coordinate R+1, while Y's coordinate maximum is one, so at least R intervening stars are needed. The checker enumerates the exact boundary and shortest chains for small radii; this coordinate argument proves every radius.

Strong Duhamel comparison between the two bounded interaction-picture evolutions retains all crossing stars and gives

    ||alpha_t^G(A)-alpha_t^(G_R)(A)||
       <=2rM b_R |t| 2^-R exp(v|t|).             (AE1.R3)

All interactions strictly outside C_R commute with its evolved local observable. No total global onsite norm is used. The bound is uniform in every containing finite volume. It may be combined with the trivial 2r bound, but the untruncated expression is already integrable against a Gaussian.

## Integrating the whole Gaussian, including its tails

Define R_s and J_s exactly as AB2, with p_s normalized Gaussian and h_s(t)=sign(t) integral_|t|^infinity p_s(u)du. Let R_s,R and J_s,R use G_R instead of G. Their supports lie in the complete C_R, extended by exterior identity.

For a centered Gaussian T with variance s², completing the square gives

    E exp(v|T|)<=2 exp(v²s²/2),
    E[|T|exp(v|T|)]<=2s(1+vs)exp(v²s²/2).

For t>0, Mills' integral estimate h_s(t)<=s² p_s(t)/t follows by inserting u/t>=1 in its Gaussian tail. Therefore

    integral |h_s(t)||t|exp(v|t|)dt<=2s²exp(v²s²/2),
    integral |h_s(t)|exp(v|t|)dt<=2s(1+vs)exp(v²s²/2).

The second also follows directly by Fubini and integral_0^u exp(vt)dt<=u exp(vu). These analytic estimates integrate the entire time axis; no discarded Gaussian tail or beyond-radius series is hidden.

Put

    epsilon_R=4rM b_R s(1+vs) exp(v²s²/2) 2^-R,
    kappa_R=4rM b_R s² exp(v²s²/2) 2^-R.

Equations (AE1.R1)-(AE1.R3) imply

    ||R_s(A)-R_s,R(A)||<=epsilon_R,
    ||J_s(A)-J_s,R(A)||<=kappa_R.                 (AE1.R4)

Both go to zero at fixed s,M as R increases, uniformly in containing finite volumes. At the frozen cap, s=2 and R=40, exact rational upper enclosure gives epsilon_R/r<2e-7 and kappa_R/r<1e-7. The checker reports the larger complete-factor count (42)^3=74088: the operator-norm precision is mathematically useful but the collar is computationally expensive and its onsite Hilbert spaces remain infinite dimensional.

## Graph domains and every boundary commutator

Each regional Gaussian inverse preserves D(G_R) by AB2's weak-commutator argument. Its local finite-volume commutator with H0 is bounded, since the regional bounded interaction sum is finite; extending by identity therefore preserves the full D(H0)=D(G). The exact full-generator identity is

    [J_s,R(A),G]=-A+R_s,R(A)+F_s,R,
    F_s,R=sum_(Z crossing C_R)[J_s,R(A),D_Z].     (AE1.R5)

Integrating (AE1.R1) against |h_s| gives ||F_s,R||<=epsilon_R. Thus the locally generated inverse has a full actual residual at most ||R_s(A)||+2epsilon_R, and

    ||[J_s(A)-J_s,R(A),G]||<=2epsilon_R.          (AE1.R6)

Together with (AE1.R4), this controls the operator difference in the G graph norm by kappa_R+2epsilon_R. Mere operator-norm approximation alone would not imply (AE1.R6); it is the independent complete boundary calculation that supplies it. At s=2,R=40 the AB2 contraction below 2r/3 survives this explicit localization cost. No crossing term is silently deleted.

## Diameter decay is not the requested cardinality norm

For a fixed single source, form the telescoping decomposition of successive local approximants. Its Rth difference is supported in C_R and has an upper norm bounded by a polynomial in R times 2^-R, using (AE1.R4) at R and R-1. Its diameter in the coarse infinity metric is R+1. Hence an exponential diameter weight exp(gamma diam) with gamma<log(2) remains summable. Polynomial translation multiplicities would not defeat that radius decay, though no new translation-family constant is evaluated here.

The existing norm instead weights the declared full support by exp(mu|C_R|)=exp[mu(R+2)^3], mu>0. The same telescoping upper budget then contains polynomial(R) exp[mu(R+2)^3-R log(2)], which does not even tend to zero. Increasing a fixed radius-decay parameter does not change that cubic-versus-linear asymptotic. Therefore this collar certificate cannot close the existing exponential-support-cardinality norm. A different connected-cluster decomposition or stronger estimate is required; the failed upper budget proves neither actual divergence nor impossibility of such a decomposition.

These all-time norm and graph estimates concern the initial homogeneous G and one indexed source. They do not establish later-diagonal stability, a numerical homogeneous gap, a physical scale match or continuum Yang-Mills. Scientific priority is unverified.
