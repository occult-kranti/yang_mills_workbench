# Forward O1 frozen handoff

Model: homogeneous I1/I2 full-link 24-link blocks, full retained four-site
stars in finite cuboids, normalized by delta=alpha/8. No canonical q profile.

Proved: simultaneous exp(sum S_b) preserves D(H0), gives the exact retained
remainder series, and every ordered connected word has support at most 4+3n.
The weighted interaction recurrence is N_(n+1)<=64s(8+3n)N_n, N0<=64b.
Hence R_w<=25460736*tau^2/25 for |tau|<=5/1536, independent of volume.
The first-order diagonal relative coefficient is 28|tau|. At |tau|=1/4096,
R_w<=777/12800 and the relative coefficient is 7/1024.

Verdict limited for numerical homogeneous stability. A small retained local
remainder is proved, but no full iterative contraction/gap threshold follows.
The actual finite-volume remainder has a negative quadratic vacuum mean
near tau=0 for nonempty anchor sets, so it is not generally purely relative.
Generated supports need a closed future iteration and uniform inverse/domain
bounds. No O2 chosen or executed.

Independent of all current O1 reverse/skeptic solutions before freeze.
Both fresh ordinary and optimized runs passed 11 controls and produced
byte-identical results, controls and manifests. All code is standard-library,
with no other producer import. Full hashes are in submission.json.
