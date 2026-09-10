# A1: available local constants and the failed pure-relative shortcut

## Physical operator and projector conventions

Work on a finite open cubic link graph with vertex extent n>=2. A link has L2(SU(2),normalized Haar) and electric Casimir C_e=j(j+1). Impose Gauss law at every vertex, with no external charges. H0=alpha*sum_e C_e, alpha>0; the magnetic perturbation is W=-sum_p lambda_p*x_p, x_p=Tr(U_p)/2 around a simple square with four distinct links. Alpha and lambda have energy units; lambda/alpha is a Hamiltonian ratio, not the Euclidean action coefficient in earlier static integrals.

Let P_e project one link onto its constant Haar function, q_e=1-P_e. For square p let P_p=product_(e in p)P_e and Q_p=1-P_p. These are operators on the full tensor-product Hilbert space (tensored with the identity outside the square). They commute with all endpoint gauge actions: Haar averaging projects onto the left/right invariant constant. Thus their identities and inequalities restrict to the physical Gauss-invariant subspace; the physical Hilbert space itself is not being factorized.

## Exact local split and norms

Multiplication by x_p is bounded self-adjoint with norm<=1. Its one-holonomy Haar moments are E[x_p]=0, E[x_p^2]=1/4 and E[x_p^3]=0. The ordered product of the four independent links is Haar. Therefore P_p x_p P_p=0 and

x_p=Q_p x_p Q_p+P_p x_p Q_p+Q_p x_p P_p.

The operator Q_p x_p P_p maps the local constant vector to x_p, whose norm is1/2, so ||Q_p x_p P_p||=1/2. The combined offdiagonal operator has matrix[[0,1/2],[1/2,0]] on the span of the normalized constant and chi_p=2x_p, and is zero on its orthogonal complement within the local block. Its norm is also1/2, not1. The diagonal compression satisfies ||Q_p x_p Q_p||<=1. These exact rank-two facts do not assert that the full multiplication operator acts only in a two-state space.

## A volume-independent diagonal form bound

Since the P_e commute, their joint0/1 eigenspaces give Q_p<=sum_(e in p)q_e. Peter–Weyl spectral values give q_e<=(4/3)C_e: a nontrivial link representation has j>=1/2 and C_e>=3/4. Every link belongs to at most4 elementary plaquettes in three spatial dimensions, so

sum_p Q_p<=4sum_e q_e<=(16/3)sum_e C_e.

For W_diag=-sum_p lambda_p Q_p x_p Q_p and lambda_max=max_p|lambda_p|, the quadratic-form bound is

|<psi,W_diag psi>|<=(16/3)lambda_max<psi,sum_e C_e psi>
=(16/3)(lambda_max/alpha)<psi,H0 psi>.

The constant is independent of volume. Boundary links can have smaller incidence. A square touches at most12 distinct OTHER plaquettes sharing a link, or1+4*(4-1)=13 plaquettes including itself. Meeting only at a vertex does not mean sharing tensor factors. Actual small open-box incidences and both kinds of meeting are computed as geometry checks; the output records both neighbor-count conventions separately.

These estimates are valid on the H0 form domain and hence on its physical restriction. They control only the vacuum-diagonal part. Applying them to the full W would erase a nonzero offdiagonal term.

## Exact physical trial falsifies the shortcut

Set only one simple plaquette's magnetic coefficient to lambda and keep the full graph. The normalized state

psi_t=(Omega+t*chi_p)/sqrt(1+t^2), real t,

is gauge invariant, belongs to the electric operator domain, and uses Haar-orthonormal Omega and chi_p. The fundamental loop excites four links, each with Casimir3/4, so H0 chi_p=3alpha chi_p. This physical loop energy3alpha is different from the unprojected four-link block's free gap3alpha/4.

Using the exact Haar moments gives

<H0> =3alpha*t^2/(1+t^2),
<-lambda*x_p> =-lambda*t/(1+t^2),
|<W>|/<H0> =|lambda|/(3alpha*|t|) for t!=0.

For every nonzero lambda the ratio diverges as t tends to0. Therefore no finite constant c can satisfy the pure bound |<W>|<=c<H0> on all these physical states. A fixed proposed c>0 is already refuted by t=lambda/(6alpha*c), which gives ratio2c. Signed t and lambda are allowed. At t=0 both expectations vanish, so the ratio is undefined, not a passing zero residual. Even there, ||W Omega||^2=lambda^2/4 remains nonzero for nonzero lambda. At lambda=0 the perturbation vanishes and this obstruction is absent.

This rejects one shortcut, not relative estimates with additive constants, correct vacuum dressing, or a valid local stability theorem. The original dense interacting uniform-gap goal remains open at its missing local contraction/source-theorem estimate.

## What this first loop permits next

The exact overlap distinction motivates an advisor review of pairwise link-disjoint nonzero plaquettes on the original graph. Such a support mask would be a restricted family of the same Hamiltonian with other coefficients0. The potential A2 block factorization and its Gauss-invariant ground-state proof have not been executed here and require their own gate. No first-order rotation or guessed constant is promoted into a dense uniform-gap proof.

The standard-library program checks exact fractions, projector truth tables, actual graph words/incidence and invalid physical inputs. Ordinary and optimized Python repeat the same checks and count once. This author's checks are distinct from the backward researcher's independent derivation and implementation.

The geometry API accepts the declared canonical open-box encoding with vertex extent2..12. It intentionally rejects alternate encodings as contract mismatches; this is not a mathematical claim that an isomorphic graph is invalid. The implementation cap12 is a finite test-program limit, whereas the proved incidence constants hold for all finite open cubic boxes with n>=2. The65 named producer gates comprise45 positive checks and20 rejecting controls, not exhaustive branch coverage or independent acceptance.
