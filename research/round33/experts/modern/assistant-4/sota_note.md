# BD1/BD2 relative to the literature this lens already reads (advisory note)

Round33 sub-round 4, modern (Penrose/Feynman) lens, research assistant/coder
"assistant-4". **This file is advisory. It counts zero research loops,
admits nothing, and is not a contract, a premise or a gate.** Every source
cited below is already recorded in
`research/round33/experts/modern/sources.json`; nothing new was fetched to
write this note, per instruction. No claim of scientific priority is made
anywhere in this file, matching the BD1/BD2 `claim_exclusions`
(`scientific_priority_verified: false` in both gates).

## 1. Centre symmetry and N-ality (BD1) against the confinement literature

BD1 turns the Round32 AW1 centre-flip/parity mechanism (SU(2): the element
`-I` acts as `-1` on the Wilson representation, and `E_Haar[W^3]=0`) into
two exact criteria and tests them, group by group, on the one-plaquette
finite graphs `H_FG(G)`: the link-flip lemma transfers to every listed
group **with a central element acting as `-1`** (SU(2), SU(4), U(1), Z2),
and the first-order parity theorem transfers to every group **with a
vanishing third Haar moment `E[W^3]`** (the same four, plus SU(5)); SU(3)
and SO(3) are recorded obstructions with exact nonzero coefficients
(`E[W^3]=1/108` and `1/27` respectively), and SU(5) is a recorded flip
obstruction via its exact nonzero fourth-order coefficient
`1/63403380965376 = 1/(2^30 3^10)`, since its centre (the fifth roots of
unity) contains no `-1`. This is exactly the group-theoretic mechanism that
the confinement literature calls **centre symmetry and N-ality**:

- **`r33-greensite-hep-lat-0301023`** (J. Greensite, *The Confinement
  Problem in Lattice Gauge Theory*, Prog. Part. Nucl. Phys. 51 (2003)):
  already recorded in `sources.json` with the relevance note "Background
  for the BD1 centre-symmetry transfer: N-ality selection rules replace the
  SU(2) link flip for SU(3)", at `reading_depth: search summary only` (not
  read in full this round either). Its review-level content -- confinement
  mechanisms organized around `Z_N` centre symmetry, centre vortices, and
  N-ality as the selection rule for which Wilson loops can be screened --
  is the same organizing idea BD1's `flip_criterion_central_minus_one`
  control makes exact and finite-model-specific: a *sufficient* condition
  for the link-flip identity `U_E H(tau) U_E^* = H(-tau)` to exist is a
  central element realizing `-1` on the Wilson representation, and BD1's
  own SU(3)/SO(3)/SU(5) obstruction cells are exact, checked
  counterexamples where that mechanism is absent. BD1's own wording is
  explicit that this connection is the producer's own derivation, not
  something re-proved from Greensite's review
  (`sources.json`: "the transfer criteria in the memo are this lens's own
  derivation, not taken from the review"), and that remains true here:
  this note does not claim BD1 reproduces, extends or is anticipated by
  Greensite's survey, only that it sits inside the same, standard
  confinement-literature picture, one exact finite-graph coefficient at a
  time. **What genuinely differs in scope**: Greensite's N-ality is a
  statement about which *Wilson loops in the confining, infinite-volume
  theory* obey a perimeter law versus an area law (screening by dynamical
  matter in the adjoint representation, etc.); BD1's N-ality-adjacent
  finding is a statement about the sign/parity of a *finite-model,
  weak-tau Taylor coefficient* on `H_FG(G)` and, separately, on
  `H^G_N` box models each inside their own Kato radius -- explicitly
  excluded from any AQ, AM2, continuum, or "predicts/confirms" reading
  (`am2_not_reinstantiated`, `no_transfer_called_prediction` controls).
  These are the same underlying representation-theoretic fact (centre
  acting by `-1`, or not) applied at two very different scales, and BD1's
  own `claim_exclusions` keep that boundary explicit.

- **`r33-osterwalder-seiler-1978`** (K. Osterwalder, E. Seiler, *Gauge field
  theories on a lattice*, Ann. Phys. 110 (1978)): recorded with the
  relevance note "Classical Euclidean counterpart of the conditional
  Hamiltonian area-law application", `reading_depth: search summary only`.
  BD1 does not use it (no area-law claim is made anywhere in BD1). BD2 does
  name the area law explicitly, but only as an **obligation row, not a
  result**: BD2 contract item 6 lists "the area law (no zero-free region)"
  among the "Obligations and no-transfer rows", and the BD2 gate's
  `accepted` text repeats this among the things *not* claimed ("not an
  area law, not a certified sign of the 1x2 mean"). Osterwalder-Seiler's
  strong-coupling area-law theorem is the classical Euclidean statement
  that this obligation would eventually need to connect to (a genuinely
  different, Euclidean-path-integral proof technique from BD2's Hamiltonian
  Rayleigh-Schroedinger/Kato-radius machinery); this note records that
  connection as background only, exactly as `sources.json` already labels
  it, and changes nothing in BD2's own obligation row.

## 2. Strong-coupling expansions (BD1/BD2) against this lens's reading

Both BD1 and BD2 are, in the strict technical sense used in the lattice
literature, **strong-coupling (small-`tau`) Hamiltonian perturbation
theory** around the Kogut-Susskind electric-field vacuum: `H_FG(G) = 32 C_2
- (tau/3) W`, `tau` playing the role of the small strong-coupling expansion
parameter, with every coefficient in BD1's moment/obstruction tables and
BD2's two-plaquette-graph coefficients (`<W_1>`, `<z>`, `<C_shared>` through
total order 4) an exact term of such a series. This is the same genre of
calculation as the classical Kogut-Susskind strong-coupling expansion of
the Hamiltonian lattice gauge theory ground-state energy and Wilson-loop
expectation, organized group-by-group and graph-by-graph rather than as an
all-orders series in a single coupling. **No source in
`research/round33/experts/modern/sources.json` is the original Kogut-Susskind
paper or a modern strong-coupling-expansion review beyond Greensite's
confinement survey** (`r33-greensite-hep-lat-0301023`, itself only a search
summary); this is recorded as a reading gap in Section 3 below, not filled
here. The one *certified numerics* source on file,
**`r33-ciavarella-quantum-10-2216`** (Ciavarella, *Truncation uncertainties
for accurate quantum simulations of lattice gauge theories*, Quantum 10,
2216, category `c`), is about truncation error in a different
sense -- on-site Hilbert-space/electric-flux truncation for quantum
simulation, not the strong-coupling Taylor-series truncation BD1/BD2 both
certify exactly (zero truncation error, by construction, since every BD1
and BD2 coefficient reported here is an exact finite-order rational, not a
truncated numerical series) -- and neither BD1 nor BD2 relies on it; it is
listed in `sources.json` for a different context (Round33's broader
quantum-hardware background) and is not used by this note either.

## 3. Wegner duality for Z2 (BD1's Z2 cell): a reading request, not a claim

BD1's Z2 cell (`C_2=0` on the even/trivial link state, `C_2=1` on the odd
state, Wilson representation the sign character) transfers both the
link-flip lemma and the first-order parity theorem, with first-order
coefficient `1/48` (`E[W^2]=1`, `E[W^3]=0`, `E[W^4]=1` exactly, confirmed
independently in `group_moments_flint.py`'s SU/SO(3) computations only by
analogy of method, not by direct Z2 recomputation in this script -- Z2 is
outside this lens's own three tasked scripts and is not recomputed here).
The natural literature comparison for a `Z_2` lattice gauge theory's
strong/weak-coupling structure is **Wegner's duality** (F. J. Wegner, 1971,
`Z_2` lattice gauge theory on a `d`-dimensional lattice is dual to the
`(d-1)`-dimensional Ising model, exchanging strong and weak coupling) --
**no record for this exists in `research/round33/experts/modern/sources.json`
at any reading depth**. This is recorded here as a genuine reading request,
not fetched, per instruction:

1. **Wegner, J. Math. Phys. 12, 2259 (1971), "Duality in Generalized Ising
   Models and Phase Transitions without Local Order Parameters"** (or a
   modern secondary exposition, e.g. a lattice-gauge-theory textbook
   chapter on Kramers-Wannier/Wegner duality) -- needed to check whether
   BD1's Z2 flip lemma (the operator identity `U_E H(tau) U_E^* = H(-tau)`
   on `H_FG(Z2)` and the `H^{Z2}_N` box models) is the Hamiltonian,
   finite-graph shadow of Wegner's duality transformation, or a logically
   separate fact that merely happens to hold for the same group; and
   whether the admitted first-order coefficient `1/48` has a natural dual
   reading on the `(d-1)`-dimensional side. Nothing in BD1 currently makes
   or needs this connection -- it is listed only as a concrete next reading
   step for a deeper Z2-specific comparison, should one ever be wanted.
2. A modern review of `Z_N`/`Z_2` gauge-Higgs duality and its relation to
   centre symmetry for general `Z_N` (bridging Section 1's N-ality
   discussion, currently only sourced via Greensite's SU(N) review, and the
   `Z_2`-specific duality of item 1) -- also not on file at any depth.

None of these is fetched here; each is listed only as a concrete next
reading step, not acted on. This note carries no premise weight and
changes no BD1 or BD2 verdict. The four-dimensional Yang-Mills existence
and mass-gap problem remains open.
