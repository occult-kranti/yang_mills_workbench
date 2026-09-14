# C1 initial draft defects preserved after repair

The first backward C1 draft was not locked.  It was overwritten during repair before a byte snapshot was preserved.  The defects identified by root review were:

- Several `check.py` controls were baseline assertions labeled as rejections rather than actual mutated-admission tests.
- The freeze-W regression field `same_after...` compared the old interval to itself and was tautological.
- The original remainder comment used the invalid implication `M<1 => exp(M)<2`; the repaired checker uses the geometric bound valid for the actual `M=7/64<1/2`.
- The quotient interval routine did not explicitly reject negative remainder radii or `Z-R<=0`.
- The action polynomial was initially hard-coded as `[3,1,1,1,1]`; the repaired checker constructs it from the graph-derived signed-face coefficient dictionary.
- The source-manifest writer skipped missing report/output files instead of requiring them.
- The signed-word mutation coverage did not yet include an actual noncommuting V-W face-word alteration.

Repairs now present in `backward/c1/check.py` and `backward/c1/compare.py`:

- Check-side diagnostics are labeled as baselines; actual rejection controls are in `compare.py` mutation tests.
- Freeze-W verifies exact coefficient convolution through degree 8 for numerator and partition, then cancels the common `exp(kappa)` factor analytically.
- Taylor remainder uses `M^(N+1)/((N+1)!*(1-M))` with an enforced `0<=M<1/2` guard.
- Quotient interval construction rejects invalid remainder/denominator bounds.
- Primary action polynomial is built from `graph()['derived_S_terms']`.
- Source-manifest generation raises on any missing required source or output file.
- Comparator mutates the `t=Tr(V W^dagger)/2` face from `V W^dagger` to a wrong signed word and requires rejection.


Second pre-lock repair note:

- The signed-κ fixture initially compared full result dictionaries, so the κ label alone could make the positive and negative fixtures differ.  The repaired control checks disjoint exact enclosures and records a nonzero odd coefficient witness.
- The independent-V resampling control initially assigned `0`; the repaired control computes `E[xw] * E[zt]`.
- The noncommuting face-word control initially checked only the word list.  The repaired checker also stores an exact quaternion sign-flip fixture for `Tr(UV†)/2` versus `Tr(UV)/2` and `Tr(VW†)/2` versus `Tr(VW)/2`.
- Public API rejection controls are executed for bool, negative and wrong-dimension moment/degree/κ inputs.
