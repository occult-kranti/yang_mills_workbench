# A2: adaptive refinement of the unchanged covariance target

The accepted A1 run showed that all eight degree24 midpoint enclosures were positive while every transported cell bound was insufficient. The advisor therefore retained the exact action, target interval [1/8,1/4], Lipschitz bound2 and Taylor degree24, and changed only the numerical partition. No fitting parameter or additional physical field was introduced.

At each transition, bisect every cell whose exact transported lower endpoint is nonpositive. Retain all other cells unchanged. A child center is recomputed from its exact rational endpoints. Its new covariance certificate includes the full original Taylor/normalization errors; its transport radius is half its width. The fixed endpoints and unchanged cells ensure that each step covers exactly the same complete closed interval.

Executed stages have8,16,21 cells. The first stage has8 insufficient cells; the second has5; the third has none. Thus two actual refinement transitions suffice. The final exact minimum lower bound is approximately0.00033465252509729616. The rational value, rather than this rounded display, is used in all acceptance gates. Positivity includes both target endpoints.

There are45 cell evaluations across the saved levels; unchanged cells may be replayed from the deterministic point evaluator's arithmetic cache. This count is an evidence count, not a timing benchmark or a claim about distinct new physical experiments.

Cap0 and cap1 correctly stop with an insufficient result; a maximum cell count8 also stops insufficient. These retained cases establish that exhausting a computation budget cannot promote an unresolved cover into a proof. Malformed cells, overlaps, midpoint or parameter substitutions, incorrect bisection history, metadata additions and Boolean limits are rejected.

The producer has23 explicit gates. Its normal and optimized Python runs must produce identical evidence. Independent backward reconstruction uses a different character moment oracle and is recorded outside this producer package; no producer rerun counts as that independent check.

This establishes a property of a fixed finite Euclidean SU(2)^2 action. It does not certify a Hamiltonian spectrum, distance decay, uniformity in volume, deformation removal in a continuum theory, or the four-dimensional Yang–Mills mass gap.
