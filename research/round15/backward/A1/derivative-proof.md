# Independent backward derivative and transport proof

Keep the finite normalized probability measure dmu_eta=Z_eta^-1 exp(x+y+eta z) dU dV with normalized product Haar, x=Tr(U)/2, y=Tr(V)/2 and z=Tr(UV)/2. The variables lie in[-1,1]. On every compact real eta interval the exponential and all its derivatives are uniformly bounded. Dominated differentiation therefore gives D E[O]=E[Oz]-E[O]E[z] for any fixed bounded O.

For C=E[xy]-E[x]E[y], the product rule yields

C'=E[xyz]-E[xy]E[z]-E[xz]E[y]-E[yz]E[x]+2 E[x]E[y]E[z].

Expansion of E[(x-E[x])(y-E[y])(z-E[z])] gives the same expression. Thus

|C'| <= 2 E| (x-E[x])(y-E[y]) |
       <= 2 sqrt(Var(x) Var(y)) <= 2.

The first inequality uses |z-E[z]|<=2. The second is Cauchy–Schwarz. The last uses Var(X)<=1 for X in[-1,1], not merely an empirical sampled variance. These bounds hold for every finite real eta and for the same action being differentiated.

If an exact point certificate gives C(c) in[a,b] and c lies in[l,r], then every eta in that entire cell satisfies C(eta) in[a-2R,b+2R], where R=max(c-l,r-c). This is the fundamental theorem of calculus applied to the derivative bound. A finite union of such cells proves a target-wide positive sign only if the cells cover the whole closed target and every transported lower endpoint is strictly positive. Numerical center values alone prove neither condition.

The moment polynomial check in the independent verifier expands both the differentiated covariance and the third centered moment as exact polynomials in raw moments. The analytic boundedness and dominated-differentiation argument above is a separate conventional proof obligation, not a consequence of the polynomial equality test.
