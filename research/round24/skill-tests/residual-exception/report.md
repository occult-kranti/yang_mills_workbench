# Residual exception: a three-dimensional skill test

**Result.** Nonzero leakage does **not** imply unbounded all-time relative heat error for the specified retained inputs and denominator. Here the exact relative error is uniformly below (1/20). The full-input, zero-extended operator error at time zero is nevertheless exactly (1).

This is a single-author derivation and correlated arithmetic check of the updated paired-physics method. It is not a physics research loop, an independent pair of derivations, a claim about the T graph, or a novelty claim.

## Exact centering and complete residual

Set (a=1/10), (s=\sqrt{101}/10=\sqrt{1+a^2}>1), and let (P_2=|e_2\rangle\langle e_2|). The actual eigenvalues of the supplied full matrix are
\[
\epsilon=2-s,\qquad E_1=2+s,\qquad E_2=5.
\]
Thus the true ground is simple, its actual gap is (2s), and all domain/second-moment requirements hold on \(\mathbb C^3\). On \(\operatorname{ran}P\), (A=[1]), so its Ritz ground is (\mu=1\) and (A-\mu I_P=0\). The true and Ritz shifts differ by
\[
\delta=\mu-\epsilon=s-1=\frac{1/100}{1+s}>0.
\]
For the normalized Ritz vector (e_0), the **complete** residual and leakage operator are
\[
r=(H-\mu I)e_0=-\tfrac1{10}e_1,\qquad
HP-PA=-\tfrac1{10}|e_1\rangle\langle e_0|,\qquad \rho=1/10.
\]
Here (PA) means the natural inclusion of the retained operator. The (e_2) residual component is exactly zero; all three components have been accounted for. The projected Ritz residual (Pr=0) is not the full residual.

The actual ground projection is
\[
\Pi=\frac1{2s}\begin{pmatrix}s+1&a&0\\a&s-1&0\\0&0&0\end{pmatrix}.
\]
Define (c^2=(1+1/s)/2), (d^2=(1-1/s)/2), with (c,d>0). Its unit ground vector is (ce_0+de_1), and
\[
\|P-\Pi\|=\|(I-\Pi)e_0\|=d\approx0.0498137.
\]
This projector distance is distinct from the distance between chosen unit ground vectors.

## A valid energy and projector certificate

The **full** excited spectrum is at least (b=3>\mu), because (E_1=2+s>3) and (E_2=5). The complete-residual bounds therefore give
\[
0\le\mu-\epsilon\le\frac{\rho^2}{b-\mu}=\frac1{200},\qquad
\|P-\Pi\|\le\frac{\rho}{b-\mu}=\frac1{20}.
\]
In particular (199/200\le\epsilon\le1\). Their premises are established in the supplied full space, not inferred from a gap inside the one-dimensional Ritz matrix.

Using the exact separation (b=E_1=2+s\) sharpens the energy certificate to equality,
\(\rho^2/(b-\mu)=s-1\), and gives the valid projector bound
\(d\le\rho/(1+s)=\sqrt{101}-10\).
These identities can also be checked directly from \(s^2=101/100\).

An invalid claimed lower threshold (b=31/10\) would instead predict
\(\delta\le1/210\) and \(d\le1/21\). Both are false: the actual first excited level is below (31/10\). Merely checking (b>\mu\) is insufficient.

## Exact all-time relative error on retained inputs

Let \(\Pi_1=I-\Pi-P_2\). The correctly, separately centered full and zero-extended Ritz heat operators are
\[
T(t)=e^{-t(H-\epsilon I)}=\Pi+e^{-2st}\Pi_1+e^{-(3+s)t}P_2,
\qquad S(t)=e^{-t(A-\mu I_P)}P=P.
\]
For every retained unit input (v=e^{i\phi}e_0\), the specified denominator equals
\(\|e^{-t(A-\min A)}v\|=1\). Since (P_2v=0\),
\[
\boxed{\frac{\|T(t)v-S(t)v\|}{\|e^{-t(A-\min A)}v\|}
=(1-e^{-2st})d\le d<\frac1{20}\quad(t\ge0).}
\]
The supremum is (d\), approached as (t\to\infty\); the error starts at zero. Thus this particular leakage produces a bounded change in the surviving ground projection. The denominator has a uniform positive lower bound because **every retained input here lies in the Ritz ground space**. No conclusion is being transferred to retained excited inputs with a decaying denominator.

Wrongly replacing the true shift by the Ritz shift in the full heat operator gives
\(\widetilde T(t)=e^{-t(H-\mu I)}\). Its ground coefficient is (e^{\delta t}\), and
\[
\|\widetilde T(t)e_0-e_0\|\ge c(e^{\delta t}-1)\ge c\delta t\longrightarrow\infty.
\]
This growth is a centering error, not the behavior of the requested comparison. The arithmetic check proves its lower bound exceeds (4.9\) at (t=1000\), while the correctly centered error stays below (0.05\).

For **all** unit inputs in the full space, zero extension instead gives
\[
T(0)-S(0)=I-P,\qquad\boxed{\|T(0)-S(0)\|=1.}
\]
The unit vectors (e_1,e_2\) witness this distinction. Their retained heat denominator is zero, so the stated relative quotient cannot be extended to all full-space inputs without changing its domain. Absolute full-input and relative retained-input questions are different even in this small example.

## Arithmetic evidence and scope

`check.py` verifies the full spectral resolution in the exact field \(\mathbb Q(s)\), including (H\Pi=\epsilon\Pi\), all orthogonal projectors, the complete residual, and \((P-\Pi)^2=d^2(I-P_2)\). Integer-square-root rational enclosures certify the numerical energy/projector comparisons. The all-time statement follows from the displayed spectral formula, not a finite time sample.

Controls reject the projected-only residual, an invalid excited-spectrum threshold, a nonpositive separation denominator, and Ritz-centering of the full heat operator. A zero-coupling control restores coincident ground projections and zero retained-input error. The exact full-input identity-error control remains one.

Executed commands, from this directory:

```sh
python -B check.py --output output
python -B -O check.py --output output-optimized
```

Both runs passed and their `results.json` and `controls.json` bytes agree. Reproduction requires fresh output directories. Arithmetic enclosures are controlled; there is no physical truncation or sampling error in this finite supplied model. The time-growth control uses the analytic inequality (e^x\ge1+x\), not an approximate exponential.

Read in full: the updated installed `paired-physics-research/SKILL.md`, `references/complete-residual-and-error-scope.md`, and `references/centered-heat-and-solo-closeout.md`. Their paths and hashes, plus the report/check source hashes, are recorded in the outputs. No current Z producer, X2 solution, or opposite researcher's work was read. The learned method correctly retains this exception when the centering, input class, and denominator are specified. No missing premise remains for the stated finite-dimensional claims.
