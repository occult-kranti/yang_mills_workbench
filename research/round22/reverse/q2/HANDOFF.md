# Q2 reverse frozen handoff

Only reverse/q2 was written. Current forward/q2 and skeptical Q2 solutions were not read. No R1 work or further-loop selection occurred. Do not edit inventoried sources or outputs after freeze.

Submission SHA256: fdc55f47ae110f32e9558988f895b21980dca7c97d0fb51f9c0558b5e00c682f
Report SHA256: 5b722e3888b8c0a44a0c2c0ddfb02848defe42b188ad7cb4da1e269369901cec
Checker SHA256: a42f188317767f6e3d0350b34ee41b7dba803e36c5e07ef3fef100c5498047ba
Results SHA256: 185368c847e4b6db06b75d89b8a51eecca319ca75b2473c45229e9bc55c4f03f
Controls SHA256: 21477bbb7ac29e6e24aafbafbf1a5dca5513dc1a26063e861f5790d56c506266
Manifest SHA256: 599ad654ce8bb19e9ab2cd27203b3ba1bda1020e8a431d0fb9c570297da365c8
Optimized summary SHA256: 1d093c06d6b877191b08d2a124bbb71c51ae06947f670c8b582a3f4420456a85

Complement: physical Gauss admissibility forbids a degree-one vertex in a nontrivial edge-spin support. Actual graph girth4 gives H_E>=3alpha off the constant ground; Q is orthogonal to it. W0 in Q witnesses sharp C0 bottom3alpha. For lambda>=0 positivity preserves C_lambda>=3alpha on QD(H_E), with complementary H1 form domain.

Exact memory: T'=-(A/hbar)T+hbar^-2 K*T, with K=B*exp(-sC/hbar)B. Its mild double integral must retain the full T in the return factor. Exact compressed resolvent is (A+z-Sigma(z))^-1, Sigma=B*(C+z)^-1B; Schur domain D(A), lower bound z. All block/domain and strong-integral premises are proved.

Leading fixed-channel spectral table, in energy/alpha units, columns (00,01,11):
3: (19/4,1/4,1/8)
9/2: (0,0,1/8)
6: (0,0,3/8)
15/2: (0,0,9/4)
8: (0,0,9/8)
17/2: (0,0,3/8)
9: (0,0,3/8)

The kernel matrix is (alpha lambda)^2 times the weighted exponentials exp(-epsilon alpha s/hbar); self-energy uses denominators epsilon alpha+z. f1=2x uses the original six-link P2 completion. Nineteen face intersections have shared path lengths0,1,2,3 with counts9,6,2,2. Nonzero lengths have exact shared spin0/1 weights1/16,3/16, yielding a finite exact spectral orbit. Center parity makes distinct face-products spectrally orthogonal; only (9,15),(15,9) contribute cross-channel triples, each1/8. This rejects scalar reference replacement.

Full-H3 errors, valid for all lambda>=0 including0..1/100:
||K-Klead|| <=250 alpha^3 lambda^3(s/hbar)exp(-3alpha s/hbar),
||Sigma-Sigmalead|| <=250 alpha^3 lambda^3/(3alpha+z)^2.
Uniform absolute bounds are250alpha^2lambda^3/(3e) and250alpha lambda^3/9. At lambda<=1/100 they are alpha^2/(12000e) and alpha/36000. No relative late-delay bound, full-resolvent small-z uniformity or norm time Taylor series is claimed.

Ordinary and optimized runs passed byte-identically. Controls cover actual graph/path orientations, girth, center parity, ambient spherical Casimir polynomial eigenfunctions, exact Haar recoupling, fixed-channel orthonormality/Q1 multiplier matrix, nonconstant spectral delay, wrong Schur sign, complementary scalar shifts, omitted memory returns at degree4 and lambda0. The exact sparse polynomial/Haar helper is imported only from own frozen Q1 checker and explicitly hash-bound. No failed control candidate occurred in Q2.

Primary reading: targeted Burbano-Bauer product-Haar, Gauss, Peter-Weyl and invariant-tensor passages. The actual gap and spectral weights are independently proved. Haar f0 is not an interacting ground; no autonomous finite closure, calibration, homogeneous or continuum transfer follows. Await joint review and root selection.
