# Feynman-method pre-contract triage, Round28

Date: 2026-09-22. Baseline: merged `a7f4b8d`; branch
`research/round28-five-goal-pairs`. This is preparatory reconstruction and source
triage, not an executed physics loop, a frozen AG2 result, or participation by
Richard Feynman. No current forward proposal or production was read. The
advisor must freeze AG2 before new calculations or experiments.

## Recommendation and inherited evidence

Freeze AG2 as an **exact inventory and weighted-error question for the complete
original O1 remainder**, followed by transport through the already admitted AG1
correction. Do not begin by asserting that the extra remainder is fourth order
or that the selected cubic source is the full input.

The Round27 handoff, additive manuscript, final panel and research network agree
on this missing implication. AI1 classified declared surrogate maps, AI2 found
one successful finite-hypothesis scalar discriminator with complete errors,
and AG1 controlled a selected cubic family. The network's proposed AG1-to-AG2
edge is an investigation dependency, not a proved transfer. AG1's reviewed
`<2/3` bound for `M<=1e-4` applies to its selected `G+A^(3)` problem. The
independent reverse bound `.923603` and skeptic bound `.604164` are compatible
sufficient estimates, not measurements of different dynamics.

## Recover the original operator before bounding E

Use the inherited **homogeneous complete-block model**, not the summable-profile
model used for AI. Each coarse site contains the complete 24-link factor; each
retained star is `Z_b=b+{0,e1,e2,e3} subset Lambda`. The 21 omitted anchored
faces remain in `phi_b`. Boundaries delete complete stars only. The dimensionless
Hamiltonian is multiplied by the fixed positive physical unit `delta=alpha/8`;
positive `E_star`, `alpha/E_star`, lattice spacing and volume remain separately
recorded. There is no new fitted clock or action deformation.

O1 uses the following **linear** local rank operators:

```
v_b = phi_b Omega_b
u_b = (H0,Z_b restricted to Q_b)^(-1) v_b
S1_b = |u_b><Omega_b| - |Omega_b><u_b|
A1_b = |v_b><Omega_b| + |Omega_b><v_b|
D_b = Q_b phi_b Q_b
X = sum_b S1_b, Phi = sum_b phi_b, A1 = sum_b A1_b
G = H0 + sum_b D_b.
```

Here `H0,Z_b u_b=v_b`, `||v_b||^2=7 tau^2/12`, and
`[X,H0]=-A1`. The last commutator holds on the graph domain, with a bounded
extension in every finite cuboid. The bounded finite-volume `X` preserves
`D(H0)`; its graph-norm exponential preserves this domain as well. Integrating
the bounded first commutator, instead of expanding unbounded `H0` in operator
norm, yields the inherited exact O1 identity:

```
Hbar = exp(X) (H0+Phi) exp(-X) = G + R_O1
R_O1 = sum_(n>=1) [ad_X^n(Phi)/n! - ad_X^n(A1)/(n+1)!].
```

Every term expands over ordered anchor tuples `(b,b1,...,bn)`. Repeated anchors
are retained. A potentially nonzero word attaches each new star to the preceding
union, with support size at most `4+3n`. The assigned union is retained even if
an operator has a smaller minimal support. Uniform interaction bounds need a
sum over all possible roots, not merely a count relative to the original anchor.

The S1 selected cubic source uses only the all-anchors-equal term at `n=2`:

```
C_b = (1/2) ad_(S1_b)^2(phi_b) - (1/6) ad_(S1_b)^2(A1_b)
a_b = <u_b,v_b>, beta_b = ||u_b||^2
w_b = Q_b C_b Omega_b = -a_b u_b - (beta_b/3) v_b
A3_b = |w_b><Omega_b| + |Omega_b><w_b|.
```

This notation deliberately distinguishes `A1` from `A3`. The nonzero actual
`w_b` proven in S1 is not its cubic upper budget. Its complete cubic term also
contains `c_b=<Omega_b,C_b Omega_b>=<u_b,phi_b u_b>` and
`D3_b=Q_b(C_b-c_b I)Q_b`. The scalar is a reference expectation, not an
interacting ground energy.

The exact proposed bookkeeping definition is `E=R_O1-A3`. It has four classes:

| Class | Exact content | Degree in tau | Declared support |
|---|---|---|---|
| E2 | `[X,Phi] - [X,A1]/2`, including overlapping ordered pairs | 2 | union of two stars, at most 7 factors |
| E3,same | `sum_b(c_b I+D3_b)` | 3 | original 4-factor stars |
| E3,other | all `n=2` words except the all-equal tuple | 3 | ordered union, at most 10 factors |
| E4plus | every `n>=3` word with both complete factorial coefficients | at least 4 | at most `4+3n` factors |

This is a partition of the inherited exact series, not a claim that individual
terms never cancel after regrouping. In particular, E2 cannot be deleted because
a selected third-order mixing term is nonzero. O1 already warned that the
remainder is not automatically vacuum-annihilating or purely relative. A generic
matrix fixture alone would not establish the value of the actual SU(2)
second-order mixing source.

## Proposed AG2 question and discriminating checks

Can this exact E inventory be given a uniform `rho=9/4` interaction bound for
the admitted `M=7|tau|<=1e-3`, with a separately reported narrower `M<=1e-4`
case, retaining all supports, scalar density and complete tails? Can the bound
then be transported through the *same selected* AG1 generator S without
discarding E or spending the rho-to-2 margin twice?

The inherited identity to be reconstructed independently is

```
exp(S) Hbar exp(-S) = G + R_AG1 + N_AG1 + exp(ad_S) E.
```

For each self-adjoint indexed term K_X, retain
`c_X I_X`, `P_X K_X Q_X+adjoint`, and `Q_X(K_X-c_X I_X)Q_X` with costs at most
`1,1,2` times its norm. A whole-E bound may be insufficient for choosing the
next reference; report class-resolved mixing and diagonal budgets where proved.
An extensive scalar must have an interaction-density estimate rather than a
false volume-independent global operator norm.

Suggested frozen controls: missing n=1 class; wrong `1/6` coefficient; deletion
of repeated ordered anchors; incoming-root omission; removal of a scalar;
boundary deletion; both coupling signs; zero coupling before any division;
exact reconstruction in rational finite matrices; and a complete analytic tail
beyond the enumerated depths. Finite matrices check algebra, not full-Hilbert
SU(2) or infinite-volume completeness. Require actual input norms or proved
lower bounds for any contraction statement. The cubic upper estimate cannot
serve as a denominator. A bound that fails to prove contraction should remain
an insufficient certificate, not be advertised as divergence or gap failure.

AG3 should be selected only after this inventory is reviewed: either control
the changed reference diagonal and next source, sharpen a demonstrably dominant
class, or state the precise obstruction to the proposed iteration. The old
bare-reference iteration from O2 already leaves a term linear in the residual;
repeating that step without tracking the updated diagonal would not resolve it.

## Three primary technical leads, read 2026-09-22

Full provenance, dates and exact reading depth are in `sources.json`. These
are selected leads, not an exhaustive claim about the literature or scientific
priority. No unconventional source supplies an additional Hamiltonian term.

1. **Del Vecchio, Froehlich and Pizzo (2021):** inspected the actual separable
   onsite-space assumptions, graph/form-domain passages, weighted potentials
   and Theorem 3.3. This is the closest complete-iteration comparator. Its
   changed local reference and induction need explicit matching before any
   theorem or numerical threshold is imported into this workbench.
2. **Bravyi, DiVincenzo and Loss (2011):** inspected the local/global distinction
   and section 4.4 expansion. This motivates checking the full transformed
   operator and truncation tail together. Their finite-dimensional/spin setting
   does not settle the present unbounded-domain or continuum obligations.
3. **Ying, Li and Po (2025):** inspected the stabilizer excitation denominators
   and binary Pauli implementation discussion. It suggests an efficient exact
   independent fixture for ordered commutator algebra. A qubit fixture cannot
   replace the actual SU(2) source or prove a uniform Hilbert-space truncation.

No new physics checker, numerical run or AG2 evidence is produced in this
triage. The advisor's frozen contract determines production.
