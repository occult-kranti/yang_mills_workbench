# A2 bounded-perturbation domain correction

Corrected the forward A2 report and generated theorem source strings to use the standard bounded self-adjoint perturbation statement: `H = H_ref + V` is self-adjoint on exactly `D(H_ref)`, and the closed quadratic-form domain is unchanged. The previous wording said the operator domains need not be equal, which was wrong for this bounded perturbation.

Follow-up: added the explicit comparator-readable equality `D(H)=D(H_ref)` while keeping the corrected bounded self-adjoint perturbation statement.
