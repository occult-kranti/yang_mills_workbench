# Candidate only: integrate the central link and one surrounding link

This is an unexecuted candidate, to be selected or revised only after C1. Its boundary values, nonzero coupling and error target are not yet accepted fixtures.

On the four-cube graph, unfreeze the central vertical link U and the surrounding vertical link V from(1,0,0) to(1,0,1). Fix every other link to identity. The affected-face union should contain six faces: four touching U, three touching V, with one shared face counted once. The other fourteen face terms are constant under the two-variable integral and cancel from this normalized conditional expectation, but remain part of any surrounding marginal.

With correct actual signed face words, normalized traces should reduce to x=Tr U/2, y=Tr V/2 and w=Tr(UV†)/2, with central actionκ(3x+2y+w). Both U and V remain independently integrated SU(2) Haar variables; they need not commute. The original central four-adjoint product becomes O=(4x²−1)³(4w²−1)/81. Its exactκ=0 mean is tentatively zero because integration over V annihilates the shared adjoint. Freezing V to identity instead gives the different one-link Haar mean1/27. Both values must be checked from the graph and integrals.

Two genuinely different moment representations are available. Conditional angular integration uses w=xy+sqrt((1−x²)(1−y²))z, z uniform on[−1,1], with independent semicircle x,y. Expanding z-even powers gives exact rational moments without numerically dividing by a vanishing sine. Alternatively decompose powers of each fundamental trace into SU(2) characters. If m(a,n) is the multiplicity of character indexn inχ_1^a, the proposed joint moment is

    E[x^a y^b w^c]=2^(−a−b−c) Σ_n m(a,n)m(b,n)m(c,n)/(n+1).

The dimension factor is essential. A candidate discriminator isE[xyw]=1/16, whereas three independently sampled trace coordinates would give zero. These are planning derivations, not executed evidence.

An eventual small but nonzero commonκ, for example1/64, bounds the total variable action byM=6|κ|=3/32. A predetermined Taylor sequence can bound the full numerator and partition with the exponential remainder. The chosen precision must distinguish the nonzero weighted value and retain insufficient coarse levels. A missing one of the two extra V-only weights is a different action; it must not pass as the complete surrounding-link integration. The new joint-Gram coordinate statement must not be confused with factorization of x,y,w or with using the old scalar-axis central code at genericb(V).

The remaining thirty-one link variables remain fixed. Even a successful candidate would be a conditional two-link integral, not a complete twenty-face bulk calculation or a physical spectral-gap result.

## Advisor planning correction to the proposed small-coupling diagnostic

The full six-face action includes the two V-only weights. A tentative independent character calculation gives the numerator's quadratic coefficient5/648, while dropping both V-only weights gives1/648. In detail, with A(x)=(4x²−1)³, E[A(x)]=1, E[A(x)(4x²−1)]=3, and both E[O w²] and E[O y²] equal1/324. The S²/2 terms w² and4y² therefore sum to5/648. This corrects an earlier planning estimate that retained only the w² term. It is an unexecuted diagnostic to check independently, not an accepted result or the final normalized finite-κ value.

## Additional pre-execution diagnostic candidates

The same character identities tentatively give partition coefficient [κ³]Z=3/8 and numerator coefficient [κ³]N=1/54. They come from the correlated xyw term. Thus the complete six-weight integral need not be even inκ. Deleting both V-only weights produces the different action3x+w, whose factorized x,w integrals are even. Deleting only one V-only weight gives3x+y+w and tentative quadratic numerator coefficient1/324, between1/648 and5/648. These are advisor hypotheses to check independently before any acceptance; they suggest using signedκ and both one- and two-weight omission controls.

## A precise common variable connecting C1 to this boundary case

For a fixed surrounding quaternion V with y=V0, the three unshared central directions are e0 and the shared direction is V. The central action vector is b(V)=κ(3e0+V). Its complete joint Gram is determined by y: |b|²=κ²(10+6y), b·e0=κ(3+y), b·V=κ(3y+1), e0·V=y. Thus C1's complete geometry, rather than an action-only assumption, can justify a one-dimensional outer coordinate for this identity-boundary case. The induced y density is (2/π)sqrt(1−y²), and the other31 links remain fixed.

The full denominator is ∫ρ(y)e^(2κy) Z_U(G(y))dy and numerator is ∫ρ(y)e^(2κy) N_U(G(y))dy. Averaging the normalized central expectation N_U/Z_U requires its additional Z_U weight; averaging it with bare surrounding Haar is a different measure. At y=±1 the Gram becomes rank deficient without making the integral singular. This proposed connection should be checked in C2 together with the actual signed graph; it does not state a scalar closure for arbitrary surrounding boundaries.
