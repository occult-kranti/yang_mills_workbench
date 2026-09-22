# Bounded current-claims inspection

Read on 2026-09-22 by the contemporary Feynman-method agent. This supplements
the Round28 source triage and does not alter frozen AG2 evidence. It is a
targeted passage review, not external peer review, independent replication,
formal verification, a new physics loop or selection of another goal.

## Faizal and Shabir, arXiv:2606.19362v1

The [primary record](https://arxiv.org/abs/2606.19362) claims a four-dimensional
construction and lists journal publication plus four appended papers. The
combined PDF has 593 pages; only selected passages were inspected.

Three questions need resolution before importing its estimates. In Theorem
11.1, the displayed lower operator comparison (11.3) is followed by an upper
Rayleigh comparison (11.5); the latter requires additional upper control.
Equation (11.8) also needs a quantitative defect sum smaller than the initial
gap, including the time-spacing factors in (11.7). In appended Theorem A.9,
one-parameter tuning of the Gaussian projection needs an explicit image/rank
condition and a controlled neighborhood for the inverse-function argument.

These are questions about the inspected passages, not a conclusion that every
supporting section lacks the needed result or that the entire claim has been
refuted. Prior sections, appendices and cited constructions were not audited
completely. The publication record is not independent replication.

## Nair, arXiv:2608.10133v2

The [outline](https://arxiv.org/html/2608.10133v2), revised 2026-08-22, concerns
2+1 dimensions. Its gauge-orbit measure leads to a proposed kinetic-operator
inequality `T^2-mT>=0`. Equations (28)-(40) and the surrounding discussion were
inspected. The passage after (40) explicitly assumes regularization and
subtraction can retain positivity of the potential.

Before applying this route, require a common closed-domain statement,
regulator control, and identification of the full Hamiltonian's vacuum and
energy subtraction. A positive comparison with a kinetic operator does not by
itself identify the excitation gap above the changed ground energy. This is a
methodological obligation, not an audit of the complete referenced framework.
The two-dimensional spatial parametrization is not a four-dimensional model
matching proof.

## Implication for this workbench

Keep three records separate: what a paper states, which implication has been
checked, and whether its hypotheses match the workbench. The present AG2 result
already distinguishes a reference-only bound from the complete corrected
Hamiltonian. A future theorem transfer must additionally identify the physical
scale, surviving vacuum sector, topology of the limit and complete error
budget. No inspected claim supplies those missing identifications automatically.

No numerical or algebraic experiment was executed during this source pass.
The proposed Douglas et al. formalization source was left unread in this bounded
pass, and is not counted as a reviewed record here. Exact reading depths and
access outcomes are retained in `current-claims-sources.json`.
