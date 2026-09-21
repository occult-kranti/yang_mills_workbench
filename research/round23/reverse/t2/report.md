# T2 reverse obligation audit — same author

This is a second formulation by the same agent, after the forward derivation. It is not an independent reconstruction. The user explicitly prohibited subagents. The unchanged frozen T2 contract and `methods/t2-solo-override.md` govern this work.

## Start from the desired all-time centered comparison

A finite-time perturbation bound proportional to time cannot establish the target. An unshifted decaying bound is also insufficient: the two centering exponentials differ. To obtain a uniform derivative along the actual complementary-block interpolation, require the following four sufficient premises:

1. A common self-adjoint domain, compact resolvent and a simple ground separated uniformly by g>0.
2. A complementary ground leakage bound ell and centered complementary leakage bound ell.
3. The exact spectral derivative epsilon'=lambda <psi,D psi>, which cancels the ground-ground part of centered Duhamel.
4. Decay exp(-g u) after removing the actual ground projection, retaining QF(0)J=-QGJ.

Reconstruction from the T1 graph supplies them. Positive diagonal magnetic blocks and offdiagonal norm b=5lambda/2 give L_s>=H_E/alpha-b. Min-max and the electric vacuum trial vector imply a ground energy <=40lambda and second eigenvalue >=3-b. Hence g>=3-(85/2)lambda>=103/40. Compactness on the gauge-invariant reducing subspace establishes existence; strict separation gives simplicity. Bounded perturbation preserves D(H_E).

The complementary diagonal lies >=3, and subtracting epsilon_s leaves d>=3-40lambda>=13/5. Inverting that actual block in the ground equation gives ell=b/d. The spectral derivative then yields nonnegative energy change <=40lambda ell^2 and projection derivative norm <=40lambda ell/g. For the evolution, the centered contraction and complementary variation of constants give ||QE_s(u)J||<=ell. Subtracting its ground limit gives ||QF_s(u)J||<=2ell, while the spectral theorem independently gives exp(-g u).

In the four Duhamel terms, the ground-ground term cancels; the two mixed terms cost 40lambda ell/g each; the excited/excited magnetic term costs 80lambda ell/g; the scalar shift term costs at most40lambda ell^2/g. The sum is below60lambda^2 at the coupling cap and decreases with smaller lambda after factoring lambda^2. The forward report contains the domain argument and complete integral derivation. This audit recomputes constants rather than treating the final claimed bound as a premise.

## What would break the argument?

- An assumed common ground leaves a nonzero ground-ground derivative and secular time growth.
- Dropping the complementary leakage replaces a quadratic projected certificate by a linear general perturbation budget.
- Removing the ground projection from F without retaining its initial Q component breaks the leakage bound at zero time.
- A partial energy shift changes a block, rather than merely centering the same full generator.
- A scalar ratio is not controlled when an operator has small spectral values. The bound is absolute in operator norm.
- An unproved gap or a variable physical clock defeats the uniform constants.
- A two-state matrix fixture can discriminate algebraic errors, but cannot certify the actual full graph's premises.

The exact checker tests the polynomial constant margin on the complete interval using nonnegative Bernstein coefficients, verifies a rational nontrivial spectral family and exhibits the wrong-centering secular term. The forward interval fixture is an additional correlated check. Neither checker is a formal proof kernel.

**Conclusion:** the frozen mathematical T2 target has a self-reviewed proof with explicit bound60lambda^2 and the spectral estimates reported forward. Independent-agent and human review were not performed. The full ten-loop cycle remains at four completed investigations. U1 is a handoff only.
