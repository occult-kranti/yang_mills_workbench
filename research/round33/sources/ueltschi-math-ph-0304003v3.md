# Ueltschi, "Cluster expansions and correlation functions", arXiv:math-ph/0304003v3 (Moscow Math. J. 4 (2004) 511–522) — source excerpt

Committed by the Round33 advisor AFTER the BB1 producers froze, as a repair source for the BB1 review: the BB1 forward producer (route polymer_kp) cites the Kotecký–Preiss criterion "in the decay-function form written as in D. Ueltschi, *Cluster expansions and correlation functions*" (its Theorem 6.1) without a committed excerpt and without re-inspecting the primary source (skeptic BB1 post-comparison review, point 3 and new contract defect D2: plan rule P4(d) was not carried into the BB1 contract). This file lets a reader compare that cited statement with the source. It is NOT a premise of any frozen BB1 packet (no BB1 producer read it), it is not an admission of anything and it carries no project claim. The original Kotecký–Preiss paper (R. Kotecký, D. Preiss, Comm. Math. Phys. 103 (1986) 491–498) is not committed; Ueltschi states (Section 1) that his criterion (3) "is the same as in [KP] in the case where polymers are subsets of a lattice".

- URL: https://arxiv.org/pdf/math-ph/0304003 (served as v3, 18 Feb 2005; retrieved 2026-09-25 through the session proxy; the v1 and v2 URLs returned an arXiv "file unavailable" page)
- PDF sha256: `2cc3e036af5b2a46afe95acf0b5863fe5c7d31554debb10a2a5cade4122bdbfc` (191795 bytes, 11 pages)
- Passages: Section 2, page 2 (definitions (1)–(2), Theorem 1 with (3)–(4), inequality (5)); Section 3, pages 4–5 (the weights b, c; Theorem 3 with (16)–(19)); Section 4.2, pages 8–9 (lattice polymer models with hard-core non-intersection).
- Method: as for the Nachtergaele–Sims excerpt: `pdftotext -layout` extraction (Part B, verbatim machine text with the known loss of integral signs, superscripts and subscripts) and a transcription of the displayed formulas checked by the advisor against the rendered page images at 110 dpi (Part A). Where Part A and Part B differ, the rendered page is authoritative; Part A follows it.

## Part A. Transcription of the statements (checked against the rendered pages)

Setting (Section 2). (𝔸, 𝒜, µ) is a measure space; µ is a complex measure with |µ|(𝔸) < ∞, |µ| its total variation. ζ is a complex measurable symmetric function on 𝔸 × 𝔸.

- (1) Z = Σ_{n≥0} (1/n!) ∫dµ(A_1)…∫dµ(A_n) Π_{1≤i<j≤n} (1 + ζ(A_i, A_j)); the term n = 0 is 1.
- 𝒢_n is the set of (unoriented) graphs with n vertices and 𝒞_n ⊂ 𝒢_n the connected ones.
- (2) φ(A_1,…,A_n) = 1 if n = 1, and (1/n!) Σ_{G∈𝒞_n} Π_{(i,j)∈G} ζ(A_i, A_j) if n ≥ 2 (product over the edges of G). A sequence (A_1,…,A_n) is a cluster if the graph with an edge between i and j whenever ζ(A_i, A_j) ≠ 0 is connected.

**Theorem 1 (Cluster expansion).** Assume that |1 + ζ(A, A′)| ≤ 1 for all A, A′ ∈ 𝔸, and that there exists a nonnegative function a on 𝔸 such that for all A ∈ 𝔸,

- (3) ∫d|µ|(A′) |ζ(A, A′)| e^{a(A′)} ≤ a(A),

and ∫d|µ|(A) e^{a(A)} < ∞. Then Z = exp{ Σ_{n≥1} ∫dµ(A_1)…∫dµ(A_n) φ(A_1,…,A_n) }. Combined sum and integrals converge absolutely. Furthermore, for all A_1 ∈ 𝔸,

- (4) 1 + Σ_{n≥2} n ∫d|µ|(A_2)…∫d|µ|(A_n) |φ(A_1,…,A_n)| ≤ e^{a(A_1)}.

In the proof (page 2): multiplying both sides of (4) by |ζ(A, A_1)| and integrating over A_1, using (3),

- (5) Σ_{n≥1} ∫d|µ|(A_1)…∫d|µ|(A_n) (Σ_{i=1}^n |ζ(A, A_i)|) |φ(A_1,…,A_n)| ≤ a(A) for all A ∈ 𝔸.

Weights (Section 3, page 5). b ≥ 0 is a function on 𝔸 and c ≥ 0 a symmetric function on 𝔸 × 𝔸 (both may vanish identically). µ_b(A) = µ(A) e^{b(A)}; ζ_c(A, A′) = ζ(A, A′) e^{c(A,A′)}; c(A_1,…,A_n) = min_{G∈𝒞_n} Σ_{(i,j)∈G} c(A_i, A_j) if n ≥ 3; φ_c(A_1,…,A_n) = φ(A_1,…,A_n) e^{c(A_1,…,A_n)}.

**Theorem 3 (Decay of correlations).** Assume that |1 + ζ_c(A, A′)| ≤ 1 for all A, A′ ∈ 𝔸, and that there exists a nonnegative function a on 𝔸 such that

- (16) ∫d|µ_b|(A′) |ζ_c(A, A′)| e^{a(A′)} ≤ a(A) for all A ∈ 𝔸.

Then for all m ≥ 1 and all A_1,…,A_m ∈ 𝔸,

Σ_{n≥m} (n!/(n−m)!) ∫d|µ_b|(A_{m+1})…∫d|µ_b|(A_n) |φ_c(A_1,…,A_n)| ≤ exp{ (1/(mγ)) [(1+γ)^m − 1] Σ_{i=1}^m a(A_i) } Π_{1≤i<j≤m} (1 + |ζ_c(A_i, A_j)|),

where (17) γ = sup_n sup_{A_0,…,A_n} | Π_{i=1}^n (1 + ζ(A_0, A_i)) − 1 | (clearly 0 ≤ γ ≤ 2). The case m = 1 is

- (18) 1 + Σ_{n≥2} n ∫d|µ_b|(A_2)…∫d|µ_b|(A_n) |φ_c(A_1,…,A_n)| ≤ e^{a(A_1)},

and multiplying (18) by |ζ_c(A, A_1)| and integrating over A_1, from (16),

- (19) Σ_{n≥1} ∫d|µ_b|(A_1)…∫d|µ_b|(A_n) (Σ_{i=1}^n |ζ_c(A, A_i)|) |φ_c(A_1,…,A_n)| ≤ a(A) for all A ∈ 𝔸.

The paper states that (18) and (19) "can be proved exactly the same way as (4) and (5)".

Section 4.2 (pages 8–9), lattice polymer models: a polymer is a connected subset of ℤ^d; µ is the counting measure times a weight w(A); polymers interact through non-intersection, ζ(A, A′) = −1 if A ∩ A′ ≠ ∅ and 0 otherwise (the hard-core case, where |1 + ζ| ≤ 1 holds).

Reading note (advisor, not a result): with hard-core ζ ∈ {0, −1}, c ≡ 0 and b = d (a distance weight on polymers), (16) is the Kotecký–Preiss hypothesis Σ_{γ′≁γ} |w(γ′)| e^{a(γ′)+d(γ′)} ≤ a(γ), and (19) bounds the weighted cluster sum over clusters incompatible with γ by a(γ); whether the BB1 forward's Theorem 6.1 (including its test-set clause and the factor e^{d(X)} with d(X) = Σ_{γ′∈X} d(γ′)) matches (16)/(19) is for the skeptic's repair record, not decided here.

## Part B. Verbatim `pdftotext -layout` extraction of the same passages

### Page 2: definitions (1)-(2), Theorem 1 with (3)-(4), and (5)

```text

function on A × A. The partition function Z is defined by
                  X 1 Z                  Z           Y                           
             Z=             dµ(A1 ) . . . dµ(An )                 1 + ζ(Ai , Aj ) .       (1)
                      n!
                   n ⩾0                             1 ⩽ i<j ⩽ n
The term n = 0 of the sum is understood to be 1.
   We denote by Gn the set of all (unoriented) graphs with n vertices, and Cn ⊂ Gn the set
of connected graphs of n vertices. We introduce the following combinatorial function on
finite sequences (A1 , . . . , An ) of A:
                                        (
                                          1                             if n = 1
                 ϕ(A1 , . . . , An ) = 1 P        Q                                    (2)
                                          n! G∈Cn   (i,j)∈G ζ(Ai , Aj ) if n ⩾ 2.

The product is over edges of G. A sequence (A1 , . . . , An ) is a cluster if the graph with n
vertices and an edge between i and j whenever ζ(Ai , Aj ) 6= 0, is connected.
   The cluster expansion allows to express the logarithm of the partition function as a sum
(or an integral) over clusters.
Theorem 1 (Cluster expansion).
Assume that |1 + ζ(A, A′ )| ⩽ 1 for all A, A′ ∈ A, and that there exists a nonnegative
function a on A such that for all A ∈ A,
                           Z
                                                       ′
                             d|µ|(A′ ) |ζ(A, A′ )| ea(A ) ⩽ a(A),                  (3)

and d|µ|(A) ea(A) < ∞. Then we have
    R
                         nX Z                   Z                           o
                 Z = exp           dµ(A1 ) . . . dµ(An ) ϕ(A1 , . . . , An ) .
                            n⩾1
Combined sum and integrals converge absolutely. Furthermore, we have for all A1 ∈ A
               X Z                  Z
           1+      n d|µ|(A2 ) . . . d|µ|(An ) |ϕ(A1 , . . . , An )| ⩽ ea(A1 ) .   (4)
                  n ⩾2

   The rest of the section is devoted to the proof of this theorem; the reader interested in
results only should jump to Section 3 that discusses correlation functions.
```

### Pages 4-5: Theorem 3 with (16)-(19)

```text
                                                                    k
                               Z(A1 , . . . , Am )         X        Y                      
                                                   =                        Ẑ (Ai )i∈Vj
                                      Z
                                                        {V1 ,...,Vk } j=1

                        CLUSTER EXPANSIONS & CORRELATION FUNCTIONS                                                  5


where the sum is over partitions of {1, . . . , m}, i.e. V1 ∪· · ·∪Vk = {1, . . . , m}, and Vi ∩Vj =
∅ if i 6= j.
   The next result deals with estimates of correlations. To exhibit a suitable decay, an
efficient strategy is to establish the criterion (3) in a stronger form. We consider a non-
negative function b on A, and a nonnegative symmetric function c on A × A (both can be
identically zero, but the larger they are the better). We introduce the notation
                         µb (A) = µ(A) eb(A)
                                                             ′
                         ζc (A, A′ ) = ζ(A, A′ ) ec(A,A )
                                                    X
                         c(A1 , . . . , An ) = min        c(Ai , Aj ) if n ⩾ 3
                                                G∈Cn
                                                       (i,j)∈G

                         ϕc (A1 , . . . , An ) = ϕ(A1 , . . . , An ) ec(A1 ,...,An ) .
The utility of functions b and c will be illustrated in Section 4. The following theorem
contains estimates on correlations; compare with the definition (15) of Ẑ(A1 , . . . , Am ).
Theorem 3 (Decay of correlations).
Assume that |1 + ζc (A, A′ )| ⩽ 1 for all A, A′ ∈ A, and that there exists a nonnegative
function a on A such that
                           Z
                                                            ′
                              d|µb |(A′ ) |ζc (A, A′ )| ea(A ) ⩽ a(A)               (16)

for all A ∈ A. Then the following estimate holds true for all m ⩾ 1, and all A1 , . . . , Am ∈
A,
                    Z                    Z
      X       n!
                      d|µb |(Am+1 ) . . . d|µb |(An ) |ϕc (A1 , . . . , An )|
           (n − m)!
     n ⩾m
                           n               m       o
                                           X                                  Y
                             1
                               (1 + γ)m − 1
                                                                                                            
                      ⩽ exp mγ                a(Ai )                                     1 + |ζc (Ai , Aj )| .
                                                            i=1           1 ⩽ i<j ⩽ m

Here, we set
                                                    n
                                                    Y                      
                              γ = sup sup                   1 + ζ(A0 , Ai ) − 1                                  (17)
                                      n A0 ,...,An
                                                   i=1
(clearly, 0 ⩽ γ ⩽ 2).
```

### Page 8-9: Section 4.2, polymer models (hard-core non-intersection)

```text
                                                            
                                                                                                                               (29)
The right side converges to e3 as |x1 − x2 | → ∞. This shows that
                                         |ρt2 (x1 , x2 )| ⩽ const e−c(x1 −x2 )                                                 (30)
for all functions c satisfying (28).
4.2. Polymer models. A polymer is a connected subset of Zd . Let A be the set of
polymers in a finite set Λ ⊂ Zd . The measure µ is taken to be the counting measure
multiplied
     √
            by a weight w(A) satisfying |w(A)| ⩽ e−η|A| with η = 2 log(2dφ) + φ−1 . Here
φ = 5+12   is the Golden Ratio. Polymers interact through a condition of non-intersection,
that is, ζ(A, A′ ) is −1 if A ∩ A′ 6= ∅, and is 0 otherwise.
   To check the criterion (3), we choose a(A) = φ−1 |A|. It is enough to consider the case
where A = {0}. If A is a connected set, there exists a closed walk with nearest-neighbor

                        CLUSTER EXPANSIONS & CORRELATION FUNCTIONS                                       9


jumps whose support is A, and whose length is at most 2|A|. This can be seen by induction:
```
