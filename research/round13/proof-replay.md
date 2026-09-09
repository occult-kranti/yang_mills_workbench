# Round 13 proof replay

This adapter runs the actual two-front finite Horn search already reviewed in
rounds 11–12. Its search core is byte-identical to round 12, with SHA-256
`07b5b397af86b6bf5a481b114844c6252046e8ca2b5604dac7d158091632be94`.
The adapter locates and checks implication routes through separately reviewed
mathematical arguments. It is not a formal mathematics proof kernel and does
not solve the four-dimensional Yang–Mills problem.

## Portable layout and execution

Place these files at the top of `research/round13/`, alongside the final
`advisor/`, `moments/`, `locality/`, `response/`, and `skeptic/` folders.
Python 3.10 or newer is sufficient for the replay adapter. Moment witness and
locality replay use the standard library. The response producer has its own
NumPy/SciPy/Matplotlib requirements; this adapter binds its diagnostic report
to reviewed source without promoting floating comparisons into a proof.

After scientific acceptance has been issued for the exact delivered sources:

```bash
python -B research/round13/make_proof_manifest.py
python -B research/round13/proof_routes.py
python -B research/round13/test_proof_routes.py
python -B -O research/round13/test_proof_routes.py --output research/round13/proof_adapter_tests_optimized.json
```

The manifest command is an explicit packaging operation. It first requires
an independent acceptance ledger with matching scientific source hashes and
the precise reviewed rule IDs. A failed proof replay never automatically
rewrites its manifest or acceptance. The same files can be tested in another
assembled location with `--root /absolute/path/to/round13`.

## What is replayed

The adapter freezes a complete exact input set and rejects symlinks, escaped
paths, stale hashes, an altered historical search core, and a different
adapter version. It loads scientific code from those frozen bytes.
The passed replay retains a SHA-256 map of every input. Before constructing
each route, the adapter matches the complete current byte snapshot against
that map and revalidates the scientific acceptance and reviewed rule IDs.
Changing a rule, certificate, report or ledger after replay invalidates the
admission record.

* All 28 recorded moment certificates are checked with exact rational
  arithmetic. The case set is pinned: hierarchy orders 1–6 at positive tilts
  1, 5, and 20, plus ten zero, negative, near-zero, and extreme-tilt cases.
  Each nonzero-tilt witness checks its quadratic form, separating direction,
  rational endpoint, variance image, inner feasible points, and slack.
* The locality producer is rerun from frozen source in an isolated temporary
  directory. Every recorded check and every byte of its four CSV files must
  match. Finite graph checks support the implementation; the general chain
  count and boundary-tail statements still depend on the reviewed theorem.
* The response report must match its own explicit schema and source hash.
  Its floating ODE comparisons remain diagnostics. The scalar susceptibility
  and Riccati rules depend on the declared compact measure and the reviewed
  differentiation argument.
* The independent scientific acceptance ledger must cover the advisor,
  supplement, all scientific implementations, and all 21 advisor rule IDs.

The final `proof_results.json` contains all 24 route libraries, actual search
traces, first forward/backward meetings for positive routes, independent
forward least-cost certificates, and a separate ordered certificate replay.
No trace is replaced by a hand-drawn route.

## Premises are visible

Finite moments and finite diagnostic cases cannot establish infinitely many
constraints. The all-order uniqueness branch explicitly assumes every
normalized compact support and recurrence condition at a fixed finite real
tilt. The convergence branch additionally assumes nested compact relaxations.
Algorithm convergence additionally assumes successfully certified orders
tending to infinity and vanishing certified optimization slack. The present
implementation only supports orders through 6.

The fixed-spacing local dynamics branch retains a common locally integrable
absolute interaction envelope, bounded incidence, shared coefficients, fixed
finite observable support, and nested exhaustive regions. Its boundary-tail
gate is withdrawn in a mandatory negative route.

The product-ground-state stability branch assumes the qualitative smallness
condition of the cited stability theorem, the electric product vacuum,
finite-range static interactions, admissible boundary padding, and the Gauss
restriction. It provides no invented numerical coupling threshold. Removing
smallness blocks both the finite-volume uniform gap route and the canonical
physical gap route. The small-interaction-to-electric-energy regime at fixed
spacing does not supply a weak-coupling continuum limit.

## Search optimization and boundaries

Each route uses the complete backward dependency cone of its selected goal.
Every rule whose conclusion can feed that goal is retained, including all
alternative derivations and rules feeding already supplied seed atoms.
Unrelated branches are omitted to avoid exponentially many irrelevant
interleavings. The retained and omitted rule IDs are recorded per route.
Optimality concerns only the supplied finite frozen ground rule library, with
zero heuristic; it is not optimality over all possible mathematical proofs.

Mandatory negative routes block missing PSD witnesses, variance images,
boundary tails, path counts, all-order hypotheses, nested relaxations,
asymptotic optimizer slack, and stability smallness. Additional routes reject
locality-to-spectral-decay, lattice-to-continuum, and identification of
Euclidean and Hamiltonian states by shared notation. The full four-dimensional
mass-gap target remains underivable from these reviewed premises.

The mutation suite uses explicit runtime gates that remain active under
`python -O`. Its graph-only fixtures test adapter logic and cannot issue or
replace scientific acceptance. Normal and optimized runs are duplicate
execution modes of the same checks and must not be counted twice.

An independent review found that the original public `make_library` helper
accepted a previously passed replay with subsequently changed frozen inputs.
Changing rule M8 to require only the compact measure could therefore create
an unreviewed hierarchy-uniqueness route. The ordinary final execution did
not mutate its inputs, so its recorded routes were unaffected. The repaired
adapter checks the complete input fingerprint and acceptance again before
constructing each library. The previous adapter and gate report are retained
in `history/`, with the independent failed controls in the skeptic records.
