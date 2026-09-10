# Same-family covariance transport

Fix k1=k2=1 in dmu_eta=Z(eta)^-1 exp(x+y+eta*z)dHaar(U)dHaar(V), where x=Tr U/2, y=Tr V/2, z=Tr(UV)/2. Each coordinate is in [-1,1]. Compactness permits differentiation under the integral for every finite real eta. For an eta-independent bounded observable f,

d E[f]/deta = E[f*z]-E[f]E[z].

Differentiate C=E[xy]-E[x]E[y]. Expanding the three centered factors gives exactly C'=E[(x-E[x])(y-E[y])(z-E[z])]. Since |z-E[z]|<=2 and Cauchy–Schwarz gives E[|delta x delta y|]<=sqrt(Var x Var y)<=1, |C'|<=2. This is a bound for this same normalized action family; it is not an assumption about independent x and y at nonzero eta.

For an exact point enclosure C(c) in [L,U] and a closed cell [l,r] with midpoint c, radius rho=(r-l)/2, the mean-value estimate gives C(eta) in [L-2rho,U+2rho] throughout the complete cell. A positive lower endpoint certifies strict positivity on that cell. A nonpositive endpoint is only an insufficient bound and does not imply C is nonpositive anywhere.

The requested complete target is [1/8,1/4]. Eight equal cells form the deliberately coarse A1 experiment. Exact point enclosures retain every Taylor and normalization error. Every rational endpoint, center, radius, parameter, source and margin is replayed. Adjacent cells meet exactly; the cover cannot omit the target boundaries or replace the interval by just its midpoints.

This derivative theorem is a mathematical argument. Hashing this file binds the stated theorem but does not mechanically check its proof. Independent advisor/backward review must establish the derivative and interval-transfer argument before proof-planner admission.
