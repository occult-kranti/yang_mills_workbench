# Compact identities and missing moments

This is a finite one-plaquette Euclidean measure benchmark. Its integration parameter κ is not the real-time two-plaquette drive, and its moments are not Hamiltonian ground-state expectations. It supplies a controlled failure test for a proposed closure of an identity hierarchy.

## Exact identity before approximation

On a finite product of compact groups, Haar invariance gives ∫ Lf dU=0 for a differentiable insertion. With a smooth real action S and normalized density e^(−S), Leibniz's rule gives

    ⟨Lf⟩ = ⟨f LS⟩.

This is an ordinary finite-dimensional integration-by-parts theorem. Passing to a continuum measure, fixing a gauge, interpreting gauge-variant insertions, or replacing a hierarchy by finitely many scalar variables requires further premises.

For one SU(2) square, x=Tr(U)/2 lies in [−1,1]. The class Haar density is (2/π)√(1−x²). Define

    dμκ(x) = Zκ^−1 exp(κx) (2/π)√(1−x²) dx.

κ is any finite real number. Integrating the derivative of (1−x²)^(3/2) exp(κx) f(x) gives, for C¹ insertions,

    ⟨(1−x²)f′⟩ = ⟨[3x−κ(1−x²)]f⟩.

The boundary term vanishes at both endpoints. For f=x^n and m_n=⟨x^n⟩,

    n m_(n−1) − (n+3)m_(n+1) + κ(m_n−m_(n+2)) = 0.

The n=0 expression has no m_(−1) term. m_0=1 is a separate normalization premise. Positivity and support constraints on the entire moment sequence remain necessary for a probability measure; finitely many recurrence equations do not replace them.

## A new scalar variable helps only with its next equation

Let v=m_2−m_1². Then the first equation is exactly

    3m_1 = κ(1−m_1²−v).

v is an existing fluctuation observable, not an adjustable mass. Defining it repairs the false equality m_2=m_1², but calculating it requires the next moment equation and ultimately a controlled hierarchy or an independently constructed measure.

At finite κ the variance is strictly positive. Indeed dμκ/dμ0 ≥ exp(−2|κ|). Using Varμ(x)=inf_c Eμ[(x−c)²] and Varμ0(x)=1/4 proves

    v ≥ exp(−2|κ|)/4 > 0.

If m_2 is replaced by m_1² while preserving the true m_1, the first identity has residual κv. For κ≠0 it cannot vanish. At κ=0 the first identity is blind to v; the next equation forces m_2=1/4. This edge case is why checking a single identity can wrongly accept a closure.

The exact Haar moments are m_(2r)=Catalan(r)/4^r and odd moments vanish. The executable check verifies this recurrence with rational arithmetic. Tilted moment curves use floating quadrature and report estimated quadrature error; they are not interval proofs. The variance lower bound above is analytic.

This counterbenchmark rejects only the explicitly defined point-concentration closure. It does not claim that every scalar reduction sets v=0, or refute a particular author's different ansatz.

## Primary-source formula review

Chatterjee, Frasca, Ghoshal and Groote, *Exact Lattice Identities and Continuum-Limit Dyson–Schwinger Equations for Yang-Mills Theory*, arXiv:2608.05415v1, 5 August 2026: https://arxiv.org/html/2608.05415v1 . Sections II–III supply the compact-group starting point; the introduction and Sections IV–V explicitly distinguish a formal continuum comparison, omitted ghosts and a scalar ansatz. Those qualifications prevent treating the abstract as a completed continuum construction. The following checks concern formulas as displayed in v1 HTML.

Take one open square, N=2, β=1, three identity links and U=diag(e^(iθ),e^(−iθ)). Use the stated generator T³=diag(1/2,−1/2). Left multiplication by exp(iεT³) shifts θ by ε/2.

1. **Equation 8 counting.** Its first directed-plaquette sum gives S=−2cosθ. Its later unordered real-trace form gives S=−cosθ. The difference depends on θ, so an additive constant cannot reconcile the displayed equality. These statements use exactly the directed and unordered sums shown, with no silent redefinition of β.
2. **Equation 14 derivative.** For the later action, LS=(1/2)sinθ. With the square's staple Σ=I, the displayed prefactor gives (1/8)sinθ. At θ=π/2 the exact values are 1/2 and 1/8. Differentiation of the underlying action is the acceptance criterion.
3. **Equation 18 source phase.** At U=I and a=b=3, the source derivative is i Tr(T³T³)=i/2 by Equation 5. The printed right-hand coefficient after the product decomposition is 1/2. Dividing the whole identity by i would require changing its left side too.
4. **Equation 29 rank.** The stated color-Lorentz normalization has matrix form ηᵀgη=I_(N²−1). A D-by-(N²−1) matrix η has rank at most D, as does ηᵀgη. At D=4 and SU(3), the right side has rank8, so this normalization is impossible. The rank obstruction holds for real or complex entries and any metric. Selecting fewer color directions changes the asserted full-color contraction; it cannot preserve the displayed identity for every color. SU(2) has three color directions, so this rank argument alone does not rule it out; signature or other constraints are separate questions.

These are local coefficient/phase discrepancies in the cited display, subject to correction in later versions. They do not invalidate Haar invariance. The workbench uses its independently declared action and derivative convention, not the inconsistent coefficients.

The derivative discrepancy is not specific to an open boundary. In a periodic two-dimensional box of side at least3, vary one link and keep all other links at identity. Its two incident plaquettes give Σ=2I, LS=sinθ for the later action, and sinθ/4 for the printed derivative. Constant contributions from other plaquettes disappear under differentiation. The same quarter ratio remains.

## Bidirectional connection

Forward: compact Haar measure → exact identity → moment recurrence → nonzero variance → explicit closure residual.

Backward: a claimed exact scalar closure → reproduction of the first two identities and positive moments → a required fluctuation variable and its evolution/constraint → remaining higher moments.

The meeting point is the same measure and moment sequence, not a shared symbol. The full four-dimensional target remains missing continuum construction, suitable reconstruction axioms, nontriviality and a positive gap for the entire physical sector.
