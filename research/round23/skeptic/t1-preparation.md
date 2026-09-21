# T1 independent preparation

Prepared solely from frozen contract `2e3cc33531ce062d5cd50344eaaccbad1e623c1505618da9faa55a5f367f6407` and inherited Q2. Current T1 producers have not been read. The shared Htilde candidate is a definition from root/reverse planning, not an independently discovered choice.

## Full block operator and positivity

Use dimensionless heat time sigma=alpha t/hbar and dimensionless Hamiltonians h=H/alpha. The actual blocks obey `a>=19lambda`, `c0>=3`, `||b||<=5lambda/2`. The unbounded diagonal domain is the actual Q2/P2 electric direct-sum domain; every new block is a bounded perturbation there. Htilde is self-adjoint on that domain. Its removal of a positive complementary magnetic compression does not automatically preserve nonnegativity; a new block estimate is necessary.

One valid independent bound is `htilde>=m I`, with `m=18lambda`, throughout `0<=lambda<=1/100`. After subtracting mI, the scalar lower block comparison has diagonal lambda and3-18lambda, offdiagonal norm at most5lambda/2. Its determinant is

`lambda(3-18lambda)-(25/4)lambda^2 = lambda(3-(97/4)lambda)>=0`.

Both diagonal entries are nonnegative. Thus the scalar quadratic form is positive and controls the actual block form. Since `h=htilde+lambda QVmag Q`, h obeys the same lower bound. At lambda0 both are exactly the electric operator. This strictly positive unshifted energy for lambda>0 is not a spectral gap above the interacting ground.

## Full-return dynamics and projected comparison

The approximate compression Ttilde exists on all H3 by its heat semigroup. Eliminating its complementary component yields the exact leading kernel `k2(v)=b*exp(-v c0)b` with the full Ttilde return factor. Bounded kernel and locally bounded semigroups give unique strongly continuous Volterra solutions on each compact interval. A one-insertion replacement of Ttilde by exp(-u a), or use of two channels as an autonomous state space, would change this solution.

Write `q_h(s)=Q exp(-s h)J`. Complement elimination and `c,c0>=3` give the basic leakage bound

`||q_h(s)||,||q_htilde(s)|| <= (5lambda/6)(1-exp(-3s))`.

Projected Duhamel has a complementary perturbation on both sides. It therefore gains two leakage factors:

`T(sigma)-Ttilde(sigma)=-lambda integral_0^sigma J*exp(-(sigma-u)h)Q Vmag Q exp(-u htilde)J du`.

Consequently the independent finite-time certificate is

`||T-Ttilde|| <= (250/9)lambda^3 F(sigma)`,
`F(sigma)=sigma(1+exp(-3sigma))-(2/3)(1-exp(-3sigma))`.

F is the integral of the two nonnegative leakage profiles; it behaves as(3/2)sigma^3 at zero and at most sigma for all sigma>=0. Hence a simpler valid bound is `(250/9)lambda^3 sigma`; a cubic short-time bound is `(125/3)lambda^3 sigma^3`. These are absolute errors, with the full selected Hilbert space and actual fixed clock.

The stronger lower bound m above can supply an additional uniform-time envelope if fully proved. Leakage is at most `b0(exp(-m s)-exp(-3s))/(3-m)`, b0=5lambda/2. Then

`||T-Ttilde|| <= [250lambda^3/(3-m)^2] sigma exp(-m sigma)`

and for lambda>0 its supremum is at most `250lambda^3/[e m(3-m)^2]`, of order lambda^2. This is a possible direct consequence of the frozen operator hypotheses, not a presumed producer result or next-loop selection. A uniform absolute bound does not supply relative late-time accuracy after dividing by a decaying amplitude. Common scalar shifts multiply both heat evolutions and their absolute error by the same heat factor; they must also shift C0 consistently.

## Discriminating controls and limits

In an algebra block fixture h-h_tilde supported only in Q, the selected first two powers coincide. The first nonzero selected difference is at cubic power, `P(h^3-h_tilde^3)P=b*(c-c0)b`. Its coefficient in exp(-sigma h) is negative1/6. This directly checks the projected lambda^3 sigma^3 mechanism and Duhamel sign. Repeated memory returns contribute at fourth and higher orders; a single return has a missing b*b b*b term. Equal diagonal moment weights in two channels do not imply scalar kernels, as Q2's unequal first moments already prove.

The actual source Vmag is bounded, but neither its compression nor dropping its Q block creates a finite autonomous system. The approximate heat evolution is a mathematically defined different block operator. Its ground and full spectral gaps are not thereby calibrated to the physical continuum. No real-time-unitary conclusion, relative infinite-time error, time-dependent-lambda drive or homogeneous transfer is supplied by these heat estimates.
