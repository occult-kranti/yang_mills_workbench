# AO2 forward: HNM limiting Wilson energy identity

Human project author: **Hruday N M (BUNZEEY)**. Independent forward execution, before reading current reverse or skeptic results. The spectral-measure method is standard; this is a source-qualified application to the actual AK2 state. Scientific priority is unverified.

**The former first-moment-loss limitation is closed for the contracted state:**

\[
\chi\in D(H_{\rm phys}),\qquad
\|H_{\rm phys}\chi\|^2\le B_2:=\alpha^2(36+28|\tau|)<37\alpha^2,
\qquad
\langle\chi,H_{\rm phys}\chi\rangle
=\alpha\,\omega(1-W^2).\tag{HNM-AO2.1}
\]

This is exactly the inherited I1/AJ1/AK2 homogeneous whole-star orthant state, original 48-link/36-endpoint Wilson cover, actual physical ground subtraction and fixed energy clock. Both `|tau|<tau_*` and `|tau|<=2^-16` remain. It is not an identity for a newly constructed AQ state without its own dictionary.

## 1. The actual limiting measures

Use the positive finite measures nu_Lambda of `chi_Lambda=(W-m_Lambda)Omega_Lambda` for the centered physical K_Lambda, and the actual spectral measure nu of `chi=(pi(W)-m)Omega` for the reducing self-adjoint H_phys. AK2 already proved C_0 spectral-test convergence from its tested resolvent limit, with moving finite means handled explicitly. Their masses converge to the actual Wilson variance. These are not measures on an assumed common concrete finite/infinite Hilbert space.

AO1 gives `int E² dnu_Lambda <= B2` uniformly. The finite exact identity is `mu1_Lambda=alpha omega_Lambda(1-W²)`. Since 1-W² is bounded local, these first moments converge numerically to `s=alpha omega(1-W²)`. The remaining task is to show that this number equals the limiting spectral first moment; bounded-local convergence alone had not done that in AK2.

## 2. Second moment transfer and uniform energy tails

For a physical energy cutoff L>0, choose the continuous function theta(u) equal to one for u<=1, 2-u for 1<u<2, and zero for u>=2. On E>=0 set `F_L(E)=E theta(E/L)` and `Q_L(E)=E² theta(E/L)`, extending both by zero on negative E. These are nonnegative continuous compact tests; as L increases, they increase to E and E² on the positive half-line.

The admitted C_0 convergence gives `int Q_L dnu=lim_Lambda int Q_L dnu_Lambda<=B2`. Monotone convergence therefore proves

\[
\int E^2d\nu(E)\le B_2.\tag{HNM-AO2.2}
\]

For every finite measure and for nu itself,

\[
\int_{E>L}E\,d\nu_\Lambda(E)\le B_2/L,\qquad
\int_{E>L}E\,d\nu(E)\le B_2/L.\tag{HNM-AO2.3}
\]

This follows from `E<=E²/L` above L and is uniform integrability of the first moment. The bound has energy units because B2 has energy-squared units. The analogous probability tail is at most B2/L². Neither statement is uniform integrability of the **second** moment.

## 3. Equality and operator domain

Because F_L agrees with E below L and satisfies 0<=F_L<=E,

`0<=mu1_Lambda-int F_L dnu_Lambda<=B2/L`.

At fixed L take the volume limit. The left first term converges to s, and the compact test converges to `int F_L dnu`, so

`0<=s-int F_L dnu<=B2/L`.

Then take L to infinity. Monotone convergence proves `int E dnu=s`, establishing the equality in (HNM-AO2.1). No formal differentiation at t=0 or unjustified interchange of an unbounded spectral test is used.

For a self-adjoint operator, membership of chi in D(H_phys) is equivalent to finiteness of its spectral second moment. Equation(HNM-AO2.2) therefore supplies the **actual** operator-domain statement and `||H_phys chi||²<=B2`. Its physical restriction and original ground centering are inherited intact. We have not proved convergence of finite second moments to that number, nor a common-Hilbert-space strong convergence of the vectors K_Lambda chi_Lambda.

## 4. Countercontrols and scope

The old AK2 measures `(1-1/(2n))delta_(1/4)+(1/(2n))delta_n` have bounded first moments but second moments growing at least n/2. They violate the new hypothesis and cannot support a counterexample to this argument.

Conversely, `eta_n=(1-1/n²)delta_1+(1/n²)delta_n` converges on bounded tests to delta_1, has uniformly bounded second moments `2-1/n²`, and first moments tending to one. Its second moments tend to two, whereas the limiting second moment is one. The escaping second-moment tail equals one. This proves that our new upper bound does not license equality of second moments.

The exact checker computes both families, their rational resolvent tests, tail inequalities, and energy-unit and finite-centering controls. It retains the original symbolic source restriction. Removing finite mean or ground subtraction changes the spectral measure, while an alpha/delta mismatch changes the physical first and second moments by different powers. These abstract controls are not additional data about the actual SU(2) state.

The result closes the specified AK2 energy-identity and operator-domain obligations. It does not supply a continuum construction, identify another infinite-volume state, or determine the actual first positive eigenenergy.

Reproduce: `python -B research/round29/forward/ao2/check.py --output /absolute/new/output`.

Pre-admission repair: the first frozen checker gave identical labels to two distinct cutoff fixture positions when n=2, since 1=n/2. Root admission correctly rejected the duplicate executed-check IDs. The original complete report, checker, inputs, outputs and freeze are preserved under `attempts/duplicate-check-ids-001/original/`. The repaired checker adds the cutoff position to each label, preserves all 67 executed checks and their mathematics, and is freshly rerun in normal and optimized modes. This is an evidence-label repair, not a ninth investigation or a changed theorem.
