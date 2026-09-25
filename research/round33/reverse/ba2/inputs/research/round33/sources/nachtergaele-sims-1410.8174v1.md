# Nachtergaele–Sims, "On the dynamics of lattice systems with unbounded on-site terms in the Hamiltonian", arXiv:1410.8174v1 — source excerpt

Committed by the Round33 advisor as a repository premise so that producers quote the Lieb–Robinson inequality from a committed source, not from a report that cites it (Round33 skeptic loop-2 review, blocking item BA2-7; plan rule P4(d)). This file is a transcription and an automated text extraction of the named passages; it is not an admission of anything and carries no project claim.

- URL: https://arxiv.org/pdf/1410.8174v1 (retrieved 2026-09-24 through the session proxy)
- PDF sha256: `501af040512f2bdb62344ecbd093664e79ad1861338eabbce2c9791fca4e2fba` (203467 bytes, 14 pages), identical to the binding recorded in `research/round29/experts/aq-primary-bindings.json` (id `ns-2014`).
- Passages: Section 3, pages 7–8 (definitions (40)–(50), Theorem 3.1 with (51)–(53)); Section 4, page 11 (Theorem 4.1 with (77)–(79)).
- Method: `pdftotext -layout` extraction (Part B, verbatim machine text, with the known loss of norm bars and superscripts), and a transcription of the displayed formulas checked by the advisor against the rendered page images at 110 dpi (Part A). Where Part A and Part B differ, the rendered page is authoritative; Part A follows it.

## Part A. Transcription of the statements (checked against the rendered pages)

Setting (Section 3). Γ is a countable set with a metric d. If Γ is infinite, F : [0, ∞) → (0, ∞) is non-increasing and

- (40) ‖F‖ = sup_{x∈Γ} Σ_{y∈Γ} F(d(x, y)) < ∞ (uniform integrability);
- (41) C = sup_{x,y∈Γ} Σ_{z∈Γ} F(d(x, z)) F(d(z, y)) / F(d(x, y)) < ∞ (convolution condition).

To each x ∈ Γ a separable complex Hilbert space H_x is associated; for finite Λ ⊂ Γ, H_Λ = ⊗_{x∈Λ} H_x and A_Λ = B(H_Λ). For each x there is a self-adjoint operator H_x with dense domain D_x ⊂ H_x; the bounded interaction Φ maps finite X ⊂ Γ to Φ(X)* = Φ(X) ∈ A_X, and

- (44) H_Λ = Σ_{x∈Λ} H_x + Σ_{X⊂Λ} Φ(X),

essentially self-adjoint on the dense domain (45) D_Λ = span{⊗_{x∈Λ} ψ_x | ψ_x ∈ D_x}; (46) τ_t^Λ(A) = e^{itH_Λ} A e^{−itH_Λ} for A ∈ A_Λ.

- (48) ‖Φ‖ = sup_{x,y∈Γ} (1/F(d(x, y))) Σ_{X⊂Γ: x,y∈X} ‖Φ(X)‖ < ∞ defines the space B_F(Γ).
- (49) S_Λ(X) = {Z ⊂ Λ : Z ∩ X ≠ ∅ and Z ∩ (Λ \ X) ≠ ∅}, the surface of X in Λ, and S(X) = S_Γ(X).
- (50) ∂_Φ X = {x ∈ X : ∃Z ∈ S(X) with x ∈ Z and Φ(Z) ≠ 0}, the Φ-boundary of X.

**Theorem 3.1.** Let Γ and F be as indicated above. Fix a collection of local Hamiltonians {H_x}_{x∈Γ} and an interaction Φ ∈ B_F(Γ). Let X, Y ⊂ Γ be finite disjoint sets. For any finite Λ ⊂ Γ with X ∪ Y ⊂ Λ and any A ∈ A_X and B ∈ A_Y, the bound

- (51) ‖[τ_t^Λ(A), B]‖ ≤ (2‖A‖‖B‖ / C) (e^{2‖Φ‖C|t|} − 1) D(X, Y)

holds for all t ∈ ℝ, where the quantity D(X, Y) is given by

- (52) D(X, Y) = min{ Σ_{x∈X} Σ_{y∈∂_Φ Y} F(d(x, y)), Σ_{x∈∂_Φ X} Σ_{y∈Y} F(d(x, y)) }.

Note (after (52)): if X ∩ Y ≠ ∅, one always has ‖[τ_t^Λ(A), B]‖ ≤ 2‖A‖‖B‖. If Φ ∈ B(Γ, F_a) with F_a(r) = e^{−ar}F(r) for some a > 0, then (53) D(X, Y) ≤ min{Σ_{x∈X}Σ_{y∈∂_Φ Y} F(d(x, y)), Σ_{x∈∂_Φ X}Σ_{y∈Y} F(d(x, y))} e^{−a d(X,Y)} ≤ min{|∂_Φ X|, |∂_Φ Y|} ‖F‖ e^{−a d(X,Y)}.

The proof (steps 1–4) uses an interaction-picture dynamics (57) generated from H_0 = Σ_{x∈Λ} H_x + Σ_{Z⊂X} Φ(Z) (54), which is how the unbounded on-site terms are handled.

**Theorem 4.1** (Section 4, "On the existence of the thermodynamic limit"; the paper states it is from its reference [12]). Let Γ and F be as described in Section 3. Fix a collection of on-site Hamiltonians {H_x}_{x∈Γ} and an interaction Φ ∈ B_F(Γ). For each t ∈ ℝ and A ∈ A_Γ^loc, the norm limit

- (77) τ_t(A) = lim_{Λ→Γ} τ_t^Λ(A)

exists and the convergence is uniform for t in compact sets. The limit may be taken along any increasing sequence of finite sets Λ which tend to Γ, and the result is independent of the particular sequence. This limiting dynamics τ_t(·) can be uniquely extended to a one-parameter group of *-automorphisms on A_Γ.

In its proof: (78) U_Λ(t, s) = e^{itH_Λ^loc} e^{−i(t−s)H_Λ} e^{−isH_Λ^loc}, with (79) H_Λ^loc = Σ_{x∈Λ} H_x.

(The words "thermodynamic limit" above are the paper's section title, quoted; they are not project wording.)

## Part B. Verbatim `pdftotext -layout` extraction of the same passages
```text

                           3. A proof of the Lieb-Robinson bound
  The models we consider are defined over a countable set Γ equipped with a metric d. In the
event that the cardinality of Γ is infinite, we will assume that there is a non-increasing function
F : [0, ∞) → (0, ∞) for which:
  i) F is uniformly integrable, i.e.
                                              X
(40)                               kF k = sup    F (d(x, y)) < ∞,
                                          x∈Γ y∈Γ

and
  ii) F satisfies the convolution condition
                                          X F (d(x, z))F (d(z, y))
(41)                           C = sup                             <∞
                                    x,y∈Γ        F (d(x, y))
                                        z∈Γ
  A quantum system over Γ is now defined as follows. To each site x ∈ Γ, we associate a separable,
complex Hilbert space Hx . By B(Hx ) we will denote the algebra of all bounded linear operators
over Hx . For any finite set Λ ⊂ Γ, the Hilbert space of states and algebra of local observables over
Λ will be denoted by
                                       O
(42)                             HΛ =      Hx and AΛ = B(HΛ )
                                       x∈Λ
For any two finite sets Λ0 ⊂ Λ ⊂ Γ, AΛ0 can be naturally identified with the subset of AΛ consisting
of Ã = A ⊗ 1lΛ\Λ0 ∈ AΛ , for all A ∈ AΛ0 . The algebra of local observables is given by the inductive
limit
                                                   [
(43)                                        Aloc
                                             Γ   =    AΛ ,
                                                    Λ⊂Γ

where the union taken over all finite subsets of Γ. The completion of AlocΓ with respect to the
operator norm, which we denote by AΓ , is a C ∗ -algebra, and it will be called the algebra of all
quasi-local observables.
   The models we will be considering are defined by families of Hamiltonians comprised of two
types of terms: strictly local terms and bounded interactions. For each x ∈ Γ, there is a self-
adjoint operator Hx with dense domain Dx ⊂ Hx . The bounded interactions are described by a
map Φ from the set of finite subsets of Γ to Aloc
                                               Γ with the property that: for each X ⊂ Γ finite,
Φ(X)∗ = Φ(X) ∈ AX . Then, for each finite Λ ⊂ Γ, the Hamiltonian for the system in Λ is given
by
                                         X         X
(44)                               HΛ =      Hx +      Φ(X),
                                             x∈Λ       X⊂Λ
which is well-defined and essentially self-adjoint on the dense domain (see, e.g., [3, Theorem
VIII.33])
                                      O
(45)                     DΛ = span{       ψx | ψx ∈ Dx , for all x ∈ Λ}.
                                        x∈Λ

Using the spectral theorem, one can define the Heisenberg dynamics, τtΛ , generated by this self-
adjoint operator, which is the one parameter group of automorphisms of AΛ defined by
(46)                         τtΛ (A) = eitHΛ Ae−itHΛ      for any   A ∈ AΛ .
  By Stone’s theorem, see e.g. Section VIII.4 of [3] or Theorem 7.3.7 of [6], the unitaries t 7→ UtΛ =
e−itHΛ are strongly continuous, leave the domain of H   Λ invariant, and satisfy
                      d Λ
(47)                    U ψ = −iHΛ UtΛ ψ = −iUtΛ HΛ ψ for all ψ ∈ DΛ .
                     dt t
8                                   B. NACHTERGAELE AND R. SIMS

We conclude that for any A ∈ AΛ , the time evolution of A, defines a strongly continuous function
t 7→ A(t) = τtΛ (A), in the sense of Section 2.
   Lieb-Robinson bounds provide an estimate of the rate at which the support of an observable
grows as it evolves under the dynamics (46). We will prove a Lieb-Robinson bound for a class of
sufficiently short- range interactions defined as follows. Let Γ and F be taken as above. The space
of interactions BF (Γ) consists of those Φ for which
                                                 1      X
(48)                          kΦk = sup                     kΦ(X)k < ∞
                                      x,y∈Γ F (d(x, y))
                                                      X⊂Γ:
                                                     x,y∈X

For any finite X ⊂ Λ ⊂ Γ, we define
(49)                   SΛ (X) = {Z ⊂ Λ : Z ∩ X 6= ∅ and Z ∩ (Λ \ X) 6= ∅},
the surface of X in Λ and set S(X) = SΓ (X). The Φ-boundary of a set X is then given by
(50)                 ∂Φ X = {x ∈ X : ∃Z ∈ S(X) with x ∈ Z and Φ(Z) 6= 0}.
For generic Φ, ∂Φ X = X, but if Φ is of finite range, ∂Φ X is a strict subset of X when X is
sufficiently large. We can now state the bound.
Theorem 3.1. Let Γ and F be as indicated above. Fix a collection of local Hamiltonians {Hx }x∈Γ
and an interaction Φ ∈ BF (Γ). Let X, Y ⊂ Γ be finite disjoint sets. For any finite Λ ⊂ Γ with
X ∪ Y ⊂ Λ and any A ∈ AX and B ∈ AY , the bound
                            Λ           2kAkkBk 2kΦkC|t|
(51)                        τt (A), B ≤              (e       − 1)D(X, Y )
                                              C
holds for all t ∈ R, where the quantity D(X, Y ) is given by
                                                                              
                                    X X                     X X               
(52)               D(X, Y ) = min              F (d(x, y)),         F (d(x, y))
                                                                              
                                      x∈X y∈∂Φ Y             x∈∂Φ X y∈Y

   Note that if X ∩ Y 6= ∅, one always has τtΛ (A), B ≤ 2kAkkBk. If Φ is exponentially decaying
                                                      

in the sense that there exists a > 0 such that Φ ∈ B(Γ, Fa ), with Fa (r) = e−ar F (r), F (r) as above,
then
                                                                            
                                 X X                    X X                 
             D(X, Y ) ≤ min                 F (d(x, y)),          F (d(x, y)) e−ad(X,Y )
                                                                            
                                  x∈X y∈∂Φ Y             x∈∂Φ X y∈Y
                                                     −ad(X,Y )
(53)                   ≤ min{|∂Φ X|, |∂Φ Y |}kF ke               ,
and the upper bound (51) can be replaced by one of the exponential form found in [8].
...


                      4. On the existence of the thermodynamic limit
  It is well-known, see e.g [1], Lieb-Robinson bounds are useful in proving the existence of the
thermodynamic limit of the dynamics for quantum spin systems. The same is true in this setting.
The following result is from [12].
Theorem 4.1. Let Γ and F be as described in Section 3. Fix a collection of on-site Hamiltonians
{Hx }x∈Γ and an interaction Φ ∈ BF (Γ). For each t ∈ R and A ∈ Aloc
                                                                 Γ , the norm limit

(77)                                        τt (A) = lim τtΛ (A)
                                                       Λ→Γ

exists and the convergence is uniform for t in compact sets. The limit may be taken along any
increasing sequence of finite sets Λ which tend to Γ, and the result is independent of the particular
sequence. This limiting dynamics τt (·) can be uniquely extended to a one-parameter group of ∗-
automorphisms on AΓ .
Proof. Let {Λn }n≥0 be any non-decreasing, exhaustive sequence of finite subsets of Γ. Let A ∈ AlocΓ
and denote by X ⊂ Γ the finite support of A. For any T > 0, we will show that the sequence
{τtΛn (A)}n≥0 is Cauchy in norm, uniformly for t ∈ [−T, T ].
   It will again be convenient to define an interaction-picture dynamics. In this case, for any finite
Λ ⊂ Γ, define a two-parameter family of unitaries on HΛ by setting
                                                    loc                         loc
(78)                             UΛ (t, s) = eitHΛ e−i(t−s)HΛ e−isHΛ
where HΛ is as in (44) and
                                                           X
(79)                                           HΛloc =           Hx
                                                           x∈Λ

is just the strictly local part of HΛ . The finite volume interaction-picture dynamics in Λ is then
defined by
```
