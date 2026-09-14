# Independent Round20 audit of the inherited C2 validator

The inherited C2 mathematical argument survives this audit, but the admission
checker failed to reconstruct three of its claimed premises. Running its
`admission_failures` against the unchanged accepted coefficient rows returned
an empty failure list both for the baseline and for each of these mutations:

1. Set the claimed sign-asymmetry endpoint `H=1000`, preserving the old margin.
2. Replace the exponential upper bound by `E=1`, recomputing `C_N/E` and the
   declared target margin consistently while retaining the old numerator loss.

The first breaks the unverified range dependence of the finite and tail losses.
The second breaks `E >= exp(7K)` at `K=1/8`. Merely hashing such scalar fields
does not verify the corresponding mathematical inequality.

Repair: independently recompute finite losses from every coefficient, validate
the exponential envelope using an exact rational Taylor-plus-geometric bound,
recompute the product-tail lower requirement at the claimed endpoint, verify
the lower-margin identity, and reject missing endpoint/positivity premises.
Boundary diagnostics must also pass their arithmetic identities, including
the negative numerator margin where the method is insufficient.

The preserved pre-repair source is in
`research/round19/backward/c2/history/pre-round20-validator-audit/`.
This is an evidence-admission repair, not a new physics research loop.
