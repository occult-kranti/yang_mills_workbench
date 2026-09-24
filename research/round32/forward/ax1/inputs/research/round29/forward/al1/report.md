# AL1 forward: HNM full-interaction matching audit

Human project author: **Hruday N M (BUNZEEY)**. HNM labels identify this project's derivation; priority is unverified. The candidate was supplied by the advisor. This forward derivation and executable were completed without reading current reverse or skeptic results.

**Result: the frozen candidate has an exact bulk coefficient dictionary but the specified weak-bare-coupling path is outside the actual I1 sufficient regime.** This is failure of a sufficient certificate, not absence of a mass gap. The bridge restriction and whole-star boundary must be retained.

## Complete dictionary

Use the untruncated Haar link Hilbert spaces with the original Casimir and all endpoint gauge actions. With the primary convention of Bauer et al., arXiv:2307.11829, p.6, Eqs.55–56, and `W_p=Tr U_p/2`, the raw SU(2) magnetic term is `lambda sum_p(1-W_p)`, where

\[
\alpha={g^2\over2a},\qquad\lambda={2\over g^2a},\qquad r={\lambda\over\alpha}={4\over g^4}.
\tag{HNM-AL1.1}
\]

The identity link and Wilson map preserves Hilbert space, every link Casimir, all endpoint actions, and all bounded local physical observables. On a finite fixed link/face inventory, bounded magnetic multiplication leaves the Casimir-sum operator domain unchanged; equal coefficients give equal operators on that domain. The additive magnetic scalar is `lambda N_p`; it is not the interacting ground energy.

The I1 cell owns all three outgoing links from each of its eight `(r,s,k)` tail vertices, `r=0..3,s=0..1`: 24 links, partitioned into ten selected-strip and fourteen free reference links. Each cell anchors 8 xy, 8 xz and 8 yz faces. Selected xy classes are `(r,s)=(0,0),(1,0),(2,0)`, giving two endpoints and one bridge. The remaining five xy, eight xz and eight yz classes are the 21 omitted faces. Unique Euclidean division of coordinates proves completeness at every translated cell; the finite checker audits these phase classes.

For a face with base p in directions i,j, its exact owner support is `{pi(p),pi(p+e_i),pi(p+e_j)}`. Its fourth vertex is not another link tail. The union of all omitted owner supports is `S={0,e_x,e_y,e_z}`. The uniform bulk coefficient assignment matches I1 only when

\[
\lambda_L=\lambda_R=\mu=\nu=\lambda,\qquad
\tau={24\lambda\over\alpha}={96\over g^4},\qquad
\epsilon=7|\tau|={672\over g^4}.
\tag{HNM-AL1.2}
\]

The exact I1 inequalities therefore read

\[
r\le\tfrac12\quad\hbox{(ends)},\qquad r\le\tfrac18\quad\hbox{(bridge)},
\qquad {672\over g^4}<c_1(S),\qquad {672c_2(S)\over g^4}<\tfrac12.
\tag{HNM-AL1.3}
\]

Here `c1,c2` remain the positive, unevaluated source constants. Equivalently the selected bridge requires `g^4>=32`, and the omitted interaction requires `g^4>672/c1` and `g^4>1344c2`. No convenient numerical value is assigned to either source constant. The inherited R18-B2 bound `g^4>=32/3` concerned a different finite-graph coefficient box. The stronger bridge condition here and the omitted-coefficient dictionary are the incremental audit; the general weak-coupling obstruction is inherited in kind.

## Path and fixed clock

For the prospectively frozen sequence `a_n=a0/n, g_n^2=1/n`,

\[
\alpha_n={1\over2a_0},\quad\lambda_n={2n^2\over a_0},\quad
r_n=4n^2,\quad\tau_n=96n^2,\quad\epsilon_n=672n^2.
\tag{HNM-AL1.4}
\]

Thus `alpha/E_star` is fixed and positive, but even the endpoint condition fails for every positive integer n; the bridge condition fails more strongly. For any fixed positive finite c1,c2 both omitted inequalities eventually fail. This is an explicit algebraic test path, not a claim that this is the physically correct renormalization trajectory. More generally every path with `g->0` eventually violates the bridge condition.

Let `H_tilde` denote the finite I1 normalized Hamiltonian, including the selected-strip ground subtraction, and let `E_tilde` be its actual ground energy. On a matched finite face inventory,

`H_KS = (alpha/8) H_tilde + sum_b E_strip,b + lambda N_p`.

Consequently its centered operator is exactly `(alpha/8)(H_tilde-E_tilde)`; the frequency generator is this operator divided by the same fixed hbar. The raw scalar and selected reference scalar cancel under actual centering. Replacing the frequency by normalized `G/hbar` changes the clock unless `alpha/8=1` in already fixed units. Positive `E_star` is a physical reference, never a regulator chosen as zero.

## Boundary and model limits

The preceding equality uses the same retained inventory. I1 retains an omitted anchor group only if its entire star lies in the coarse volume. For `B={0,e_z}`, no whole star is retained, although ten omitted faces anchored at zero have their actual supports in B. Thus I1's boundary prescription is not automatically the ordinary all-contained-plaquette boundary. The checker derives this exact mismatch. Deep bulk coefficient agreement supplies no boundary-state identification, which remains AN's obligation.

An interior local site belongs to four star anchors `x,x-e_x,x-e_y,x-e_z`. Dropping incoming stars loses three interaction groups. A summable profile is not the uniform omitted interaction: over N complete anchors the same-sign norm budget is `7N|tau|`, not bounded independently of N. Neither substitution repairs (HNM-AL1.3).

## Evidence and interpretation

`check.py` independently constructs face phases/supports and computes all scale identities using exact rational arithmetic. Its controls reject omitting the bridge, `tau=r`, lost incoming stars, a wrong electric coefficient, normalized-clock replacement, zero reference energy and summable-profile substitution. Finite arithmetic checks audit the all-n argument; they are not physical simulations or observations.

Newton's analysis/synthesis method here is the explicit observable/domain dictionary followed by the all-n consequence. Tesla's whole-device method is the retention of omitted plaquettes, incoming stars and the physical clock. Neither historical analogy supplies a modern theorem premise.

Primary reading: Bauer et al. PDF introduction pp.1–2 and Hamiltonian definitions p.6 were freshly checked on 2026-09-22; their truncation numerics are not used. I1 and R19-A1 are inherited full reports. The local stability constants, matched continuum construction and continuum mass gap remain unresolved.

Reproduce: `python -B research/round29/forward/al1/check.py --output /absolute/new/output`.
