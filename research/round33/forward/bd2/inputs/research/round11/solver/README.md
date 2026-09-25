# Two adjacent SU(2) plaquettes: exact algebra, certificates and driven evolution

This is an infinite-representation quantum calculation on one fixed open graph of two adjacent squares, six vertices and seven links. It does not establish a spatial-volume limit, a continuum quantum field theory, or the four-dimensional Yang–Mills mass gap. The representation degree D changes a computational cutoff, not graph size or physical lattice spacing.

## Run

Python dependencies: NumPy, SciPy and Matplotlib. No network or computer-algebra package is required. From this directory:

```bash
python two_plaquette.py --degree 3 --lambda1 1 --lambda2 2 --certificate
python run_study.py
python test_solver.py
python -O test_solver.py
python -O run_study.py
```

All output paths are resolved relative to these scripts, so the directory can be moved intact. The first command constructs and replays a single exact certificate. Without `--certificate`, it reports floating Ritz estimates with an explicit noncertificate status. Exact rational inputs such as `--alpha 1/2` are accepted. The study uses at most degree 5 (56 invariant polynomials), with exact finite-to-infinite certificates at degrees 2–4 (10–35 polynomials).

`two_plaquette.py` is the exact invariant-algebra and certificate API; `run_study.py` produces the bounded experiments and plots; `test_solver.py` contains deterministic fixtures, unreduced link checks and rejected mutations. The public certificate verifiers are `verify_certificate(c)` and `verify_continuous_rectangle(c)`.

## Graph, parameters and gauge constraints

Vertices are TL, TM, TR, BL, BM, BR. Oriented links are:

| Link | Orientation |
|---|---|
| h1 | TL → TM |
| h2 | TM → TR |
| h3 | BL → BM |
| h4 | BM → BR |
| vL | TL → BL |
| vM | TM → BM |
| vR | TR → BR |

Each link carries normalized SU(2) Haar measure. Gauge transformations are independent at all six vertices, and physical states obey every vertex Gauss constraint. With root TM, define

`A = vM h3⁻¹ vL⁻¹ h1`, `B = h2 vR h4⁻¹ vM⁻¹`.

Tree reduction leaves two Haar SU(2) matrices modulo simultaneous conjugation. Their invariant coordinates are `x=Tr(A)/2`, `y=Tr(B)/2`, `z=Tr(AB)/2`. The shared link cancels from the trace defining z. The physical Hilbert space is L² of

`−1≤x,y≤1`, `(z−xy)²≤(1−x²)(1−y²)`

with constant measure `2/π² dx dy dz`. It is not a cube with independent x, y and z. Equivalently x and y have independent semicircle densities `(2/π)sqrt(1−x²)`, and `z=xy−sqrt(1−x²)sqrt(1−y²)u`, with u uniform on [−1,1]. This conditional representation is used for exact rational moments. Important fixtures are E[x²]=E[y²]=E[z²]=1/4 and E[xyz]=1/16.

The Hamiltonian is

`H = α Kρ + λ1(1−x) + λ2(1−y)`,

`Kρ = Σouter C_e + ρ C_vM`,

with α>0, λ1,λ2≥0, ρ>0 and link Casimir normalization j(j+1). α, λ1 and λ2 have energy units; ρ is dimensionless. ρ=1 is the ordinary seven-link electric sum. Varying ρ defines a different gauge-invariant link-weighted Hamiltonian; varying λ1 and λ2 defines specified magnetic coefficients on the two plaquettes. They are coefficients in a canonical gauge action, not added mass or scalar fields: the corresponding phase-space action is the usual link symplectic term minus H, with vertex multipliers imposing Gauss constraints. The selected API retains strictly positive ρ. ρ=0 lies outside this chosen parameter contract; it is not claimed to be mathematically singular.

At the reduced group level, `Kρ=3C_A+3C_B+ρC_shared`. In coordinates its positive kinetic operator is

```
Kρ f = 3(3+ρ)/4 (x f_x + y f_y) + 9/2 z f_z
       −(3+ρ)/4 [(1−x²)f_xx + (1−y²)f_yy]
       −3/2 (1−z²)f_zz
       −ρ/2 (z−xy)f_xy
       −3/2 (y−xz)f_xz −3/2 (x−yz)f_yz.
```

For ρ=1 this gives Kx=3x, Ky=3y, Kz=9z/2 and K(xy)=13xy/2−z/2. In particular the outer-loop excitation and the shared-link cross derivatives prevent replacing the answer by two independent rotor spectra. The test suite perturbs all seven original links before gauge fixing and compares the full action derivatives to this reduced operator. It also compares quaternion and complex-matrix loop products and tests independent vertex gauge transformations.

## Exact finite-to-infinite certificate

Monomials x^a y^b z^c of total degree at most D span P_D. The kinetic differential operator is triangular in degree, with diagonal value

`ε(a,b,c) = 3j(j+1)+3k(k+1)+ρl(l+1)`,

`j=(a+c)/2`, `k=(b+c)/2`, `l=(a+b)/2`.

Exact symmetry under the Haar Gram matrix makes each orthogonal polynomial layer invariant. Polynomials are dense on the compact quotient, so these layers give the complete kinetic spectrum. Its free physical gap is `min(3(3+ρ)/4,9/2)` times α. The free gap is doubly degenerate at ρ=1.

The first omitted layer has d=D+1. For ρ=1 its exact minimum is

`τ/α = 5d²/8 + 2d + 3(d mod 2)/8`.

For other positive ρ the code minimizes the exact ε over a+b+c=d. This also bounds every later layer: lowering any nonzero exponent decreases spin labels coordinatewise and hence decreases the energy. Because both magnetic potentials are nonnegative, the full discarded Hamiltonian is at least τ.

Let G be the exact Haar Gram matrix, A the Hamiltonian form matrix on P_D, and M the form matrix of W=λ1x+λ2y. The exact form matrix of P H Q H P is

`C = P W² P − M G⁻¹ M`.

Choose a rational U above the certified second eigenvalue of A and below τ. Completing the square gives the infinite-space form comparison

`H ≥ B ⊕ U`, with `B=A−C/(τ−U)` interpreted with Gram matrix G.

Exact Fraction congruence inertia encloses the first two generalized eigenvalues of A and B. A nonzero diagonal pivot is used when available; a 2×2 pivot handles nonzero offdiagonal matrices with zero diagonal. Exact zero eigenvalues are counted without a machine epsilon. Floating eigenvalues only propose initial rational intervals; exact refinement enforces the declared absolute width, including at very large energy scales.

Rayleigh–Ritz supplies the upper energy bounds and the lower comparison supplies lower bounds. The gap interval is `[lower E1−upper E0, upper E1−lower E0]`. Subtracting two Ritz upper bounds is never treated as a gap lower bound. `verify_certificate` reconstructs every matrix and checks the graph scope, parameters, degree/dimension, exact inertia endpoints, requested precision, tail/threshold inequalities, source hash and semantic positivity status. This is an exact arithmetic verifier conditional on the documented mathematical reduction and form inequalities; it is not a formal proof kernel.

## Bounded results

For matched α=1, λ1=2, λ2=3, ρ=1:

| Degree | Dimension | Certified gap interval |
|---:|---:|---:|
| 2 | 10 | [3.2984242431, 3.4159621091] |
| 3 | 20 | [3.3615855656, 3.3637733444] |
| 4 | 35 | [3.3623860610, 3.3624083907] |

Displayed intervals are rounded outward; exact JSON rationals are authoritative. The separate D=5 numerical Ritz gap is 3.36239180265. A converged numerical difference alone is not the certificate.

Since the centered multiplication coordinates have norm at most one,

`|Δ(λ1,λ2)−Δ(μ1,μ2)| ≤ 2(|λ1−μ1|+|λ2−μ2|)`.

Nine exact point certificates at {0,1,2}², with closed radius-1/2 cells in each coordinate, cover the complete square [0,2]². Replaying each point, coverage cell and margin proves

`Δ ≥ 963936567779819/1000000000000000 > 0`

throughout that square at α=ρ=1. This exceeds what the elementary free-gap/constant-trial estimate establishes near the square's upper corner. The exact scaling identity `H(α,λ1,λ2,ρ)=α H(1,λ1/α,λ2/α,ρ)` gives the corresponding bound times α when 0≤λ1,λ2≤2α and ρ=1. It is not uniform as α tends to zero.

`parameter_sweep.csv` changes one of α, λ1, λ2 and ρ at a time while explicitly recording all fixed coefficients. These are sparse numerical comparisons, not a global monotonicity theorem or a renormalization trajectory. Unequal plaquette coefficients can change the ordering of excitations, and no monotonic gap claim is imposed.

## Both couplings driven in continuous time

The finite-Galerkin protocol is α=ρ=1,

`λ1(t)=1−cos(πt/2)`, `λ2(t)=1.5[1−cos(πt/2)]`, 0≤t≤2,

starting from the constant normalized Haar wavefunction. Its exact finite-dimensional identity is

`d⟨H⟩/dt = λ1′(t)⟨1−x⟩ + λ2′(t)⟨1−y⟩`.

DOP853 integrates the state and work as separate variables. An independent unitary midpoint propagator integrates the same work rate by Simpson quadrature. Neither defines work as the endpoint energy difference. Each method must pass its own work and norm gates, and deliberately omitted work is rejected in both.

At D=4 the final energy is 4.137719528396 and integrated work is 4.137719528400; the maximum recorded work defect is below 4.8e−11. The D=3 to D=4 final state difference is about 0.00409. This is a measured cutoff difference, not an error bound for infinite-dimensional evolution. Tightening the DOP853 tolerance at fixed D=3 gives a 1.10e−9 state difference. Midpoint state discrepancies converge with orders 1.9997 and 1.9999. Stationary tail certificates do not certify this driven evolution.

The study's explicit acceptance thresholds are norm defect≤1e−8 for both methods, DOP work defect≤1e−7, midpoint work defect≤2e−4, DOP tolerance discrepancy<1e−7, finest midpoint state discrepancy<2e−4, and midpoint state orders in (1.7,2.3). Cutoff differences are reported without a fabricated pass threshold. These thresholds belong to this bounded implementation and were not externally preregistered. All mathematical acceptance gates use exceptions and also run under optimized Python.

## Files and audit boundaries

- `output/stationary_certificates.json`: exact rational point and matched-cutoff certificates.
- `output/continuous_rectangle_certificate.json`: full exact points, coverage cells and common margin.
- `output/stationary_convergence.csv`, `parameter_sweep.csv`: labeled exact displays and numerical comparisons.
- `output/dynamic_history.csv`, `dynamic_dop_comparison_history.csv`, `dynamic_midpoint_history.csv`, `dynamic_summary.json`: raw sampled work/norm histories for every reported method and independent-method summaries.
- `output/exact_fixtures.json`: portable exact measure, low-degree kinetic and moment anchors.
- `output/stationary_convergence.png/.svg`, `coupled_drive.png/.svg`: reproducible plots.
- `output/edge_tests.json`, `edge_tests_optimized.json`: executed fixtures and mutations, with source hashes.
- `output/validation.json`: study gates and complete expected source-hash set; failed reruns are marked failed.

Independent review found and retained two initial API defects: integer inputs could contaminate the exact coupling square through ordinary division, and a very large floating energy proposal could expand a certificate beyond its advertised absolute precision. The first was repaired by rational normalization and direct polynomial construction; the second by exact inertia refinement before returning. Both held-out examples are now in the normal and optimized test suite. The independent audit is maintained separately by the project skeptic.

The mathematical source review, explicit derivation and broader finite-graph theorem are supplied by the accompanying round-11 advisor materials. Historical provenance is the canonical Hamiltonian formulation of [Kogut and Susskind (1975)](https://doi.org/10.1103/PhysRevD.11.395); the one-plaquette comparison is discussed in [Bauer et al.](https://arxiv.org/abs/2307.11829). These sources motivate the setting; the seven-link normalization is checked here directly against the unreduced link graph.
