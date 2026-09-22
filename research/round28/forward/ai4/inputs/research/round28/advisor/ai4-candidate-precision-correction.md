# Planning correction: where arithmetic error enters

This additive note corrects the broad square-root statement in the advisor's
unselected uniform-schedule candidate. The Feynman-method researcher and the
skeptic independently pointed out the distinction after reviewing AI3.

A fixed absolute rounding tolerance on a *final scalar error radius* can
create a nonvanishing floor. That is not how the current AI3 square-root
brackets are used. They round sqrt(b(q^2)/96) before multiplying by tau and
the other declared factors. The resulting added scalar error has a factor
tau=O(u^3) on the fixed hypotheses and therefore decays as u tends to zero.
It must be charged, but it is not a constant physical-error floor.

If a uniform AI4 target is selected, trace arithmetic errors through their
actual multipliers. Analytic relative envelopes are one valid option, not a
necessary replacement merely because an inner square root uses fixed absolute
rounding. The separate individual retained Taylor remainder is independent of
u at fixed duration; the cancellation-combination remainder has the proved
1-q factor. These are different arithmetic questions.

No proposed schedule or new numerical claim is proved or selected by this
planning correction. The earlier candidate is preserved to show the review.
