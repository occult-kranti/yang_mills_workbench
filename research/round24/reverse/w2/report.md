# W2 reverse — repeated residuals converge on the vacuum column, with full-source limits kept separate

Independent reverse reconstruction before reading forward W2. Keep exactly initial homogeneous G, actual identity-extended source A and S2's L_Theta and R_Theta. W1 supplies a nonzero cubic source and a positive one-step residual; it does not assert every repeated residual stays above that one-step bound. Newton's reconstruction and Tesla's complete-return-path check require separate conclusions for a vector column, the full operator and the interaction decomposition.

## Exact all-step identity at fixed G

Write R=R_Theta and L=L_Theta, and set A_0=A, A_n=R^n(A), K_0=0 and

    K_n=sum_{k=0}^{n-1} L(A_k).

R is an average of unitary conjugations, so it is a unital completely positive contraction on bounded operators, preserves self-adjointness, and ||A_n||<=r=||A||. Each L(A_k) is bounded skew-adjoint, preserves D(G), and satisfies the S2 integrated commutator identity. Summing it gives for every finite n

    [K_n,G]=-A+A_n on D(G),
    ||K_n||<=n Theta r/2,
    ||G K_n xi||<=||K_n|| ||G xi||+2r||xi||.            (W2.R1)

Thus K_n and exp(+-K_n) preserve the actual graph domain. The bound is finite-n; it is not a uniform global inverse bound as n grows. This is an accumulated linear homological inverse, not a sequence of full nonlinear BCH conjugations. Such conjugations would also change scalar, diagonal and interaction terms.

On a Bohr frequency omega, with t(omega)=sinc(Theta omega), the two maps have coefficients

    A_n: t(omega)^n,
    K_n: [1-t(omega)^n]/omega for omega!=0,
    K_n: 0 at omega=0.                               (W2.R2)

Every zero-frequency block is retained at every step. These scalar expressions do not by themselves prove a bounded Schur-multiplier inverse on the entire operator algebra. The time-domain construction proves the finite-n statement (W2.R1) without requiring that unjustified inference.

## Quantified actual vacuum-column decay and graph convergence

The actual initial vacuum obeys G Omega=0, A Omega=w_full, ||w_full||=r and w_full is orthogonal to Omega. Its positive spectral support has gap g=1-4M>=381/416, M=7|tau|. Therefore

    A_n Omega=sinc(Theta G)^n w_full,
    K_n Omega=G_Q^(-1)[I-sinc(Theta G)^n]w_full.         (W2.R3)

There is a simple uniform scalar contraction. Let a=Theta g in (0,1/16] and rho=1-a^2/8<1. For a<=x<=2, sinc x is nonnegative and its alternating Taylor upper bound gives

    sinc x<=1-x^2/6+x^4/120<=1-(2/15)x^2<=rho.

For x>=2, |sinc x|<=1/x<=1/2<=rho. Hence |sinc(Theta lambda)|<=rho for all lambda>=g. Spectral calculus on this **column** proves

    ||A_n Omega||<=rho^n r,
    ||K_n Omega-G_Q^(-1)w_full||<=rho^n r/g,
    ||G(K_n Omega-G_Q^(-1)w_full)||<=rho^n r.           (W2.R4)

The limiting vector is in D(G). These are norm and G-graph convergence of the actual vacuum-response vector, uniform in complete-star containing cuboids and valid in the admitted infinite representation. The lower constant g comes from the initial form comparison and the fixed physical energy delta*g, delta=alpha/8. It is not an excited Bohr-frequency gap. Neither (W2.R3) nor (W2.R4) replaces the exterior identity in A by a vacuum projection.

W1's actual h[w]/r^2<=24 and one-step lower bound >=311r/1664 remain compatible: a small filter initially retains much of the source, while enough repeated averages reduce this vacuum column. Its cubic nonzero source remains relevant; at fixed tau and fixed n the factor rho^n is just a numerical factor, not automatic improvement of the power of tau.

For an exact numerical sufficiency example at |tau|=5/1664 and Theta=1/16, put u=1-rho=(381/6656)^2/8. Bernoulli gives rho^n<=(1+nu)^(-1). Taking n=ceil(9/u) therefore guarantees vacuum-column reduction by at least ten, with no logarithmic rounding or numerical spectral simulation. A stronger decay rate follows from rho^n<=exp(-nu), but is not needed for the exact demonstration. To certify an additional factor |tau| for nonzero |tau|<1 using this conservative inequality, take n>=ceil((1/|tau|-1)/u). This improves this column's upper order to quartic while n grows; it is not an all-sector or weighted-iteration theorem.

## What happens to the complete source

For every finite containing cuboid, G has compact resolvent. The finite-link electric Casimir has discrete spectrum with finite multiplicity tending to infinity; selected strip multiplication terms, ground shifts and the finite retained D sum are bounded perturbations. Thus G has a complete eigenbasis. Define the bounded diagonal-block map

    D_G(A)=sum_E P_E A P_E,

where the sum converges strongly and ||D_G(A)||<=||A||. For an eigenvector xi of energy E,

    R^n(A)xi=sinc(Theta(G-E))^n Axi -> P_E Axi

in vector norm by bounded spectral convergence. The eigenvector span is dense and R^n are uniform norm contractions. Consequently

    R^n(A) -> D_G(A) strongly in every fixed finite cuboid.     (W2.R5)

This is a legitimate full-source strong-operator limit, not a proof that its value is zero. The actual diagonal blocks P_E A P_E have not been computed here, including excited/exterior blocks. Nor is the convergence asserted in operator norm, uniformly across volumes, or in the connected interaction norm. Small nonzero excited energy differences can make scalar convergence arbitrarily slow. The infinite homogeneous G need not have a complete pure-point eigenbasis, so the finite-volume proof cannot be carried into it without a spectral/limit argument. The column result (W2.R4) does survive there and is the admitted infinite statement.

For Hilbert-Schmidt sources one can additionally use the spectral theorem for the self-adjoint commutator generator on the Hilbert-Schmidt space: R^n converges in that norm to its zero-frequency projection. This does **not** apply to A=A_Y tensor I_ext, which is not Hilbert-Schmidt whenever the exterior has an infinite-dimensional factor. A finite number of spatial factors does not make its Hilbert space finite dimensional. We do not use this optional Hilbert-Schmidt observation to prove (W2.R5) or to discard exterior sectors.

An explicit topology control on l^2(N) shows why even strong convergence to zero need not imply norm convergence: with G e_k=k^(-1)e_k and A mapping alternating neighboring basis vectors to each other, each fixed transition has a nonzero Bohr difference and its sinc power vanishes, while the differences approach zero and the residual operator norm stays one for every n. This bounded diagnostic G does not have the actual model's compact-resolvent properties and is only a wrong-inference control. No such norm obstruction is claimed for the actual SU(2) source without its spectral data.

## Connected support and later diagonals remain separate obligations

R^n is an n-fold average of the actual orbit alpha_(s1+...+sn)(A), each |sj|<=Theta. The existing positive connected Dyson majorant can be invoked directly only when its radius condition holds throughout the total-time support. The reverse S2 certificate requires 208M n Theta<1; at the frozen parameter cap 208MTheta=35/128, this covers n<=3 and fails at n=4. The forward certificate has another constant but the same finite-duration limitation. Its failure does not prove divergence or nonlocality of the actual maps. It does prevent using that particular positive bound to justify the many-step weighted closure needed by the numerical column reduction.

Iterating a one-step weighted inequality on the original source-star class is also invalid without bounding the new larger support distributions. Every step's source has generated connected unions, ordered multiplicity and incoming crossings. A scalar contraction of the vacuum column cannot replace that all-source support estimate. No sum of all translated K_n is asserted bounded on the infinite Hilbert space.

For a later-diagonal algorithm, one must separately update G_j, its domain/form constants and ground projector, the actual source A_j, the scalar shift, centered diagonal and complete support decomposition. One then needs a remainder inequality and all-step contraction summable in the chosen weighted interaction norm. Equations (W2.R1)–(W2.R5) solve the fixed-G linear iteration in named topologies; they do not construct those nonlinear updates or a homogeneous numerical gap. Zero coupling is the exact zero-source exception. Filter duration and iteration count are proof variables, with no new fitted physical clock or action coefficient.

## Checks and conclusion

The exact checker verifies the telescoping multiplier including omega=0, retained diagonal versus decaying vacuum transitions in a rational coefficient fixture, the actual cap contraction and the conservative reduction count, and the old connected-radius breakdown. These fixtures verify algebra and topology distinctions, not an actual spectral truncation. Normal/-O checks are explicit. Accepted result: actual vacuum-response graph convergence and finite-volume full-source strong convergence to the retained diagonal map. Full-source norm/weighted decay, infinite-volume all-sector limit, actual excited diagonal blocks and later-diagonal closure remain open; no continuum or priority claim is made.
