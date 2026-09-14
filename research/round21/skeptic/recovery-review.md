# Recovery review before M2

This is a recovery audit, not an additional research loop. The recovered tree
contains nine admitted Round21 loops, I1 through M1, and a frozen M2 contract.
M2 is not counted or accepted by this document. I inspected the nine gate
claims, advisor decisions and existing skeptical reviews, and re-read the
operator arguments underlying I, J, K/L and M1. The root integrator is conducting
the fresh complete source replay; this document does not substitute stored
success fields for that release check.

## The handoff contains obsolete open-item wording

| Handoff item | Evidence recovered | Correct remaining boundary |
| --- | --- | --- |
| Direct infinite product construction, domain and gap for the summable exception | Round19 A2 constructs the incomplete tensor product, closed form, common self-adjoint domain, unique ground and gap. | This is a specific summable representation; it is not the homogeneous ground representation or the continuum theory. |
| Convergence of finite clipped restrictions to any limiting state, resolvent or dynamics | Round20 D proves finite-factor exterior-reference lifted resolvent and ground convergence; E proves literal-box local-state convergence, including arbitrary upper phases; G constructs literal-box local dynamics and its full-algebra GNS generator. | State local convergence, lifted resolvent convergence and local dynamic convergence are distinct statements. No global norm convergence of arbitrary-phase boundary vectors was proved. Homogeneous boundary equivalence remains separate. |
| Physical observable sector | Round21 J identifies the dyadic physical cyclic GNS space with the invariant subspace, supplies its restricted generator and an actual positive Wilson fluctuation. | Do not transfer its numerical gap to another coefficient profile without checking that profile. |
| Homogeneous dense nondecaying stability | I1 now supplies a complete local theorem dictionary and qualitative fixed-spacing stability for sufficiently small homogeneous omitted coupling. | Numerical smallness constants, a constructive overlapping-star iteration, and equality of alternative homogeneous thermodynamic boundary limits remain unresolved. It is inaccurate to say no homogeneous stability result exists at all. |
| Limiting profile dynamics | M1 proves strong perturbation, strong-resolvent and compact-time strong unitary convergence on the canonical fixed-budget profile. | This tends to the selected-strip reference, with every fixed omitted coupling tending to zero. Norm-resolvent and propagator-norm conclusions remain undetermined. |

The explicit Yarotsky threshold, a matched four-dimensional continuum
construction, the Clay mass gap, and an independently tested physical role for
double-Fibonacci geometry remain open. The physical clock and conditional
mobility matching also remain unresolved despite exact inverse maps.

## Substantive audit of the nine loops

**I1/I2.** Complete tail ownership gives 24 links and 21 omitted faces per
anchor block. All omitted faces cross a block boundary; their maximum support
lies in a four-site star. The source local norm is exactly `7|tau|`, whereas
the global absolute sum diverges at nonzero homogeneous coupling. The theorem
uses the former. Its source empty-boundary prescription uses the full star;
padding transfers finite-volume estimates, but does not prove equality of all
thermodynamic boundary limits. I2 correctly retains both the diagonal
`Q phi Q` term and the exact transformed remainder. The local operator `S`
has range in the unbounded operator domain, so its exponential preserves that
domain. The rational estimate `707 tau^2/60` is a one-star statement in
normalized energy units. It does not control an infinite sequence of overlapping
rotations.

**J1/J2.** The variance transfer uses the actual perturbed-vacuum projector
distance, rather than only a reference fluctuation. Gauge averaging of a
bounded local operator is a weak operator integral; applying it to the
invariant vacuum gives a strong vector integral. This avoids an unsupported
operator-norm continuity premise. Full-algebra cyclicity then proves the reverse
inclusion in `H_cyc=H_inv`. Spectral reduction gives the self-adjoint restriction
on `D(H) intersect H_inv`. The gap remains a lower spectral threshold, not an
identified excitation energy. The positive exponentially bounded Wilson
correlation is in imaginary time; no real-time magnitude decay follows.

**K1/K2/L1/L2.** Positive mobility changes the generator while preserving the
specified stationary density. The mobility derivative and the full transformed
potential are required. Exact rate inversion holds only in the declared family
and with the stated known static coefficient. K2's continuous-interval rank
proof uses the actual full marginal and a two-copy covariance identity. Its
conditioning bound concerns `(c,c*zeta)`, with an additional singular division
when recovering `zeta` near zero `c`. L1 adds a detecting third observable only
for its declared cubic family. L2 correctly limits its general obstruction to
finitely many initial slopes. A positive hidden fifth-degree direction changes
the same observable's second derivative, so it does not preserve a full time
curve. No physical data or lattice-to-conditional generator identification was
supplied by these loops.

**M1.** The commutator must use every link in the complete reference factors
covering the operator. The origin-xz example has 22 such links and 28 incident
omitted faces, rather than four displayed links and five faces. The reference
finite-excitation orbit is dense through bounded finite-factor rank-one
operators; arbitrary bounded operators need not preserve `D(H_ref)`. Uniform
boundedness extends the local estimate to strong convergence on fixed vectors.
The resolvent identity is applied to a fixed reference-resolvent vector, and
compactness of a fixed reference time orbit supplies uniformity on finite time
windows. Constant nonzero perturbation norm alone determines neither
norm-resolvent convergence nor its failure.

I also performed an independent exact Catalan-moment reconstruction, without
importing either producer. It gives the L1 matrix rows
`(3/16,0,0)`, `(25/128,1/32,0)`, `(59/256,9/64,9/512)`, determinant
`27/262144`, all three zero p5 slope changes, and curvature coefficient
`1/1024`. Separate rational calculations recover I2's rounded coefficient
`7/12+14(4/5)=707/60` and J1's floor
`1/4-2/150-4/150^2=5321/22500`. These arithmetic checks accompany the
written arguments; they do not numerically prove the infinite-dimensional
statements.

## Novelty and checked primary sources

The recovered evidence supports project-specific derivations, theorem
applications, and explicit obstructions. It does not establish scientific
priority for any of them. The classical tools must not be renamed as newly
invented equations or axioms.

- I independently checked Yarotsky's definitions and Theorems 1–2: the local
  interaction norm, finite range and empty-boundary conventions are explicit,
  while the checked threshold constants are existential. The project adds an
  explicit geometry dictionary and local estimates for its model.
  [Yarotsky, 2004](https://arxiv.org/pdf/math-ph/0411042).
- I checked the DLMF finite Gegenbauer expansion. It gives
  `p3=C_3^(2)/32` and `p5=C_5^(2)/192`; these polynomial families are established.
  Their concrete null-rate and curvature roles here are the application under
  review. [DLMF 18.5.10](https://dlmf.nist.gov/18.5.E10).
- I checked Teschl's strong-resolvent functional calculus in section 6.6,
  Theorem 6.31. The general operator-convergence method is established; this
  model's complete-factor estimate and time-window qualifications are its
  additional calculation. [Teschl](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf).
- I inspected the physical-observable discussion, Theorem 4.1 and conclusions
  in Grundling–Rudolph. Infinite-lattice dynamics, gauge constraints and
  gauge-invariant ground states already form an established research program.
  Their QCD model and algebra are different, so that work neither supplies
  this model's constants nor establishes its equivalence to QCD.
  [Grundling–Rudolph, 2015](https://arxiv.org/pdf/1512.06319).

This is a targeted primary-source comparison, not an exhaustive literature
priority search. The C2 wrapper restores reproduction under a new reviewed
inventory while preserving the historical missing-cache defect; it adds no
physical theorem and no research loop. No material implication error was found
in the nine claims within the scopes above. M2 requires its own fresh
independent review before ten-loop completion and future-goal selection.
