# AI3 forward post-freeze clarification: width, containment and the Taylor floor

This is an additive interpretation note after the advisor opened exchange. The
original forward report, checker, output and freeze remain unchanged. It relies
on the skeptic's already executed exact post-review checks; no new calculation,
physical cell, collar or research loop is introduced.

In sections 4 and 5 of the frozen forward report, **“slightly tighter on this
grid” means a smaller interval width, not endpoint containment**. The skeptic's
`ai3-post-review.json` verifies smaller widths for the direct scalar all-corner
ratio intervals in all twenty hypotheses. It also records twenty cases in which
the direct interval is not wholly contained in the cancellation-centered
interval. Thus the wording must not be read as saying that one enclosure
dominates the other endpoint by endpoint.

The reason is that two effects compete. The all-order retained combination tail
can improve one endpoint relative to using two independent scalar arithmetic
radii. Conversely, independently boxing the cancellation numerator and its
denominator loses their shared physical e4 dependence and can widen the other
endpoint. Both constructions are valid enclosures; their intersection is valid.
The reverse producer additionally preserves e4 in a sixteen-corner enlarged
error box. The reverse and skeptic intersection tests still find overlapping
candidate intervals in every frozen cell. No full physical error cancellation
or sharpness for the actual joint physical error set follows.

Also distinguish two improvements that the frozen report discusses together.
**Replacing the separate cubic linearization errors by the exact degree-eight
centers removes the material Taylor floor on this finite grid.** Ordinary
degree-eight scalar arithmetic was already negligible relative to every
physical error and candidate separation tested here. The further all-order
`1-q` factor is a proved retained refinement, but it did not cause a successful
finite-grid ratio discriminator; there is no such success. That factor may be
useful in a subsequently contracted uniform family with u tending to zero,
where a fixed individual numerator Taylor bound would eventually exceed a
shrinking candidate separation. This is a prospective use, not an executed
AI4 result.

All ten physical ratio verdicts remain insufficient. The direct scalar
distinction for both probes at `u=10^-18,k=5`, the complete physical budgets,
and their stated scalar tolerance remain unchanged. Overlap remains a failure
of these sufficient interval certificates, not physical equality or a general
identification impossibility.

The pre-existing `post-freeze/interval-comparison/` directory contains a
post-exchange source-snapshot record and copies. It was encountered already
present during this resumed review and has been preserved without alteration;
this note does not claim authorship of that snapshot operation or any execution
from it. The present author's source identities and confirmation that the
original freeze bindings remain intact are recorded in
`tesla-clarification-sources.json`.
