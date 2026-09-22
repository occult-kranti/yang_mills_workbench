# AG3 additive passive-embedding comparison

This interpretation was added after the reverse report, checker and output
froze, in response to the advisor's explicit comparison request. Those
scientific bytes and all input snapshots remain unchanged. This review adds
zero research loops.

All actual indexed B supports have at least four blocks. Consequently the
identity operation already satisfies

```
||B||_(3/2) <= (3/4)^4 ||B||_2 = (81/256)r.
```

The active AG3 main-interval coefficient `3060/3623` is **larger** than
`81/256`. Its cross-weight upper certificate therefore does not show a stronger
bound than merely measuring the uncorrected source at the lower weight. It
still supplies the exact full conjugation, domain, retained-diagonal and
scalar identities, together with its stated bound. It must not be advertised
as certified improvement over doing no correction on the main interval.

The narrow-interval coefficient `5949/96812` is **smaller** than `81/256`.
Thus its active upper certificate is stronger than the passive upper
certificate. These are comparisons of sufficient bounds against the same
actual input r. They do not evaluate the actual lower-weight norm of either
source, prove a pointwise comparison of those two actual norms, or establish
same-weight contraction and an all-stage iteration.

In particular, the generated supports have no fixed maximum size. A family
concentrated on size m can have passive norm ratio `(3/4)^m`, arbitrarily
smaller than the universal ceiling `81/256`. No lower comparison for the
actual uncorrected B has been proved. The narrow result beats the universal
passive **upper ceiling**, not necessarily the actual passive norm.

Exact rational comparisons and bindings to the frozen evidence are in
`post-freeze-passive-comparison.json`. This note supplements the numerical
interpretation; it changes none of the admitted mathematical identities.
