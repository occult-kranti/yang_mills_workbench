# Bidirectional proof planning: what is actually certified

The implementation reuses the audited round6 finite ground-Horn planner and its independent forward uniform-cost certificate. Its heuristic is h=0, an admissible special case of A*. Costs count reviewed rule applications. They do not estimate scientific plausibility, computer time or experimental cost. Backward regression creates sufficient obligations; it never reverses implication.

Round7 admits 17 finite-model steps, 11 classical-gravity steps, 4 reference-coefficient steps and 4 bounded-addition obstruction steps. The scalar and gravity domains are distinct. The executable graph carries assumptions, references and scopes on every node and rule. Numerical evidence is kept outside the exact-rule premises. Successful routes remain conditional on their declared model assumptions even when the legacy engine status string is `proved`.

The finite route ends at finite-dimensional global continuation, using an exact positive gap and an energy estimate. The classical-gravity route ends at constraint propagation on an existing regular interval; it does not prove global existence. The coefficient route proves a positive continuous-integral coefficient after changing a regulator-dependent parameter; it does not prove physical renormalization. The obstruction route applies only to uniformly bounded additions and bounded potential along cofinal regulator sequences.

Two negative scenarios are mandatory. Withdrawing the reviewed Maxwell-equation certificate makes finite continuation underivable in that library. Separately, the proposed common Einstein-QED closure is underivable because no reviewed sufficient connection has been supplied. The latter is not marked as a hard-coded blocked goal: exhaustive finite search returns `not_derivable`. Its listed research obligations are proposals, not executable proof rules. Failure of this finite library is not a theorem that no other mathematical solution exists.

The planner validates metadata and inference replay, not the truth of a prose proof. The SHA-256 manifest binds the exact rule library, planner, guard and referenced notes before and after search. This prevents silent source replacement; it does not turn a human-readable derivation into a formal proof assistant certificate.

Run `python proof_obligations.py` to verify the frozen evidence. `--freeze` is a separate authoring operation for a newly reviewed snapshot and must not be used to conceal changed evidence. The delivered archive also contains an independent manifest of every packaged research file.
