# Hruday parity theorem, link-flip antisymmetry and the first-order Wilson mean — AW1 reverse (reconstruction route)

Human project author: **Hruday N M (BUNZEEY)**. This is AI-assisted reverse production under premise isolation (contract control `reverse_premise_isolation`). I read the frozen contract snapshot `inputs/research/round32/contracts/aw1.json` first (sha256 `c24bf7eb6a1c24034427c810a9c26c4c86d1f9c1d31b0fe36ea4cf2a796814ef`). After it I read only snapshots in `inputs/` and the inherited protocol and code-style files named in Section 10. I did not read `skeptic/triage.md`, `skeptic/loop2-response.md`, any `advisor/deliberation-*.md`, any file under `research/round32/experts/` other than the snapshotted `modern/loop3-signoff.md`, or anything under `research/round32/forward/aw1/`.

HNM labels are project aliases. The following are established mathematics:
- Peter–Weyl theory and the Clebsch–Gordan series for SU(2);
- Weyl integration;
- center (Z_2) gradings and center-flip symmetries of lattice gauge theories, which are a known kind of argument, so no priority is claimed for the flip lemma;
- Rayleigh–Schrödinger and Duhamel perturbation formulas, and Kato's analytic perturbation theory for bounded perturbations.

The commuting-creation expansion is the admitted AM2 construction. The AM2 lineage credits Bravyi–DiVincenzo–Loss 2008, and AM2 used Gauvin arXiv:2503.15539v3, Supplement A.6–A.8, as its template. Scientific priority is unverified.

## Verdict (reverse half)

The model is the zero-selected AQ subfamily: selected triple `(0,0,0)`, whole stars `phi_b=-(tau/3) sum_f W_f`, both signs of `|tau|<=10^-8`, centered whole-star boxes `Lambda_N` with `N>=2`, cover `R={0,e_z}` and the Haar reference. In that model the reverse route establishes the following.

1. **Parity theorem (item 1): complete.** It is proved from the per-link center grading. In the Peter–Weyl basis a link carrying spin j has center parity `(-1)^{2j}`, and a product whose factors put an odd number of j=1/2 factors on some link has zero Haar mean. In every finite box, every first-order term of `omega(W^2)`, of `omega(W alpha_theta(W))` and of `C(s)` vanishes, and the state, Duhamel and energy terms vanish separately.
   - Haar moments: `E[W^3]=0`, `E[W^2 W_f]=0` for every omitted f including f=W, `E[W^2]=1/4` and `E[W^4]=1/8`. Three exact routes agree: the Clebsch–Gordan count, Weyl integration by Wallis ratios, and the free-link unit-sphere moments.
   - The energy-24 multiplet vector `W Omega_0` has zero first-order splitting.
   - Consequences: `C(s)=e^{-3s}/4+O(tau^2)` in each finite box, with the tau^2 constant explicitly left unbounded, and `omega(W^2)=1/4+O(tau^2)` with a supplementary exact-tier constant `K_W2 ≈ 1677.33` that is uniform in N.
2. **Flip lemma (item 2): complete at kappa=0.** It holds in every finite box and every on-site cutoff, and passes to AQ limits as a statement about the whole set of subsequential limits.
   - The flip set E is reconstructed rather than assumed: exactly two one-coordinate parity rules meet every plaquette oddly, the contract's cyclic E and an anti-cyclic rule, and the two differ by a center gauge transformation.
   - The general identity is `U_E H_N(tau,kappa) U_E^* = H_N(-tau,-kappa)`.
   - Oddness gives **no** O(tau^3) remainder.
3. **First-order coefficient (item 3).** `omega_tau(W)=+tau/144+r(tau)` for either sign of tau. The sign is re-derived from I1.5.
   - Convention finding: with the AV1-admitted creation coefficient `c^(1)=L_0` (AM2 sign, `psi=e^{-C}Omega_0`), the correct identity is `omega=-2 Re<W Omega_0,c^(1)>+O(tau^2)`.
   - The contract's display `2<W Omega_0,c^(1)>` is therefore correct only for the ground-vector correction `psi^(1)=-c^(1)`. Read literally with the AM2 sign it gives `-tau/144`, and the sign fixture rejects that reading.
4. **Remainder K_2 (item 4).** `|r_N(tau)|<=K_2^+ tau^2`, uniformly in N and passed to every AQ subsequential limit, itemized in seven prereg names:
   - **exact tier:** `K_2^+ ≈ 3354.4994` (exact rational in Section 6);
   - **crude tier:** `K_2^+ ≈ 7.93756e6`;
   - **labelled conservative variant** (overlap factor 4): `≈ 1.34168e4`.
5. **Feasibility (item 5).**
   - At the cap, `K_2^+ tau ≈ 3.3545e-5 <= 1/288`, with a margin of about 103.5.
   - The sign margin is `1/(144 K_2^+ tau) ≈ 207 >= 2`.
   - The frozen rule gives `tau_AW2 = 10^-8`.
   - The crude tier fails `1/288` at the cap and is retained as a limited-tier value.
6. **Checker.** `check.py` runs 57 exact checks: 27 positive checks and all 30 contract controls as damaging mutations. Its output is byte-identical under `-B` and `-B -O`.

**Proposed outcome of this producer:** `accepted_within_scope` with sub-label `static_not_dynamic`. Admission still needs the forward route, the exchange and the skeptical review.

This producer does **not** claim:
- an enclosure or sign certificate of `omega(W)` (that is AW2);
- a dynamical or mass-gap correction;
- any tau^3 remainder;
- uniqueness of the AQ state, or a rate in N;
- a uniform Wilson theory or a continuum statement.

## 1. Model, units and conventions

In normalized units `delta=alpha/8` (I1.3 at the zero triple, I1.5, AM2.1):

\[
H_N(\tau)=\sum_{b\in\Lambda_N}h_b+\sum_{b+S\subseteq\Lambda_N}\phi_b,\qquad h_b=8\sum_{e\ \mathrm{owned\ by}\ b}C_e,\qquad \phi_b=-\frac{\tau}{3}\sum_{f\in O_b}W_f,\qquad W_f=\tfrac12\operatorname{Tr}U_f .
\tag{HNM-AW1-R01}
\]

The physical Hamiltonian contains `-(alpha tau/24) W_f` for every omitted face (I1.2, I1.5). In alpha units `G=H/alpha` the omitted interaction is `V=-(tau/24) sum_f W_f`, a face vector `W_f Omega_0` has energy 3 (24 normalized), and the clock is `s=alpha t_E/hbar`.

The Wilson loop is the xz face at the fine origin, `W=(1/2)Tr U_(0,x)U_(e_x,z)U_(e_z,x)^{-1}U_(0,z)^{-1}` (AQ2 §4, AT4 F04). Its link owners are 0,0,0 and `e_z`, so its cover is `R={0,e_z}`. It is the omitted class `xz, r=0, s=0` anchored at 0, which makes it one of the 21 omitted faces in the star `phi_0`.

At the zero triple the Haar product is the onsite ground (AT4 F01). A nonzero triple is a changed model.

**First-order vector and sign convention.** Rayleigh–Schrödinger perturbation theory and AM2's `L_0` give

\[
\psi^{(1)}=-H_0^{-1}P\,V\Omega_0=+\frac{\tau}{72}\sum_fW_f\Omega_0,\qquad c^{(1)}:=L_0=H_M^{-1}P_MV\Omega_0=-\frac{\tau}{72}\sum_fW_f\Omega_0=-\psi^{(1)} .
\tag{HNM-AW1-R02}
\]

The coefficient is `tau/72` in both unit systems, `(tau/3)/24` normalized and `(tau/24)/3` in alpha units. AM2 writes `psi=e^{-C}Omega_0=prod(1-hat c_I)Omega_0`, so the ground vector's first-order correction is `-c^(1)`. Mixing the two unit systems gives `tau/1152` or `tau/18`, and the checker rejects both.

## 2. Reverse analysis: from the desired conclusions back to sufficient premises

The desired conclusions, which are the contract's targets and are not assumed, are:

\[
\text{(D1)}\ \ \omega_\tau(W)=\tfrac{\tau}{144}+r(\tau),\ |r|\le K_2\tau^2\ \text{uniformly in }N;\qquad
\text{(D2)}\ \ \partial_\tau C(s),\ \partial_\tau\omega(W^2)\big|_{0}=0;\qquad
\text{(D3)}\ \ \omega_{-\tau}(W)=-\omega_\tau(W).
\tag{HNM-AW1-R03}
\]

**Working back from (D2).** For a bounded operator A, the first-order coefficient of a ground expectation is `2 Re<(A-omega_0(A))Omega_0, psi^(1)>`. The coefficient of a heat or real-time correlation adds a Duhamel term and a ground-energy term. By (R02), every one of these terms is a pairing of the form `<X, W_f Omega_0>` with X built from `W^2 Omega_0`, `W alpha^0_theta(W) Omega_0` or `Omega_0`. A **sufficient** premise is therefore a symmetry that fixes X and changes the sign of `W_f Omega_0`. The Z_2 center grading (Section 3) supplies it.

**Working back from (D3).** One wants a unitary that:
- fixes `Omega_0`, every Casimir and every gauge action;
- changes the sign of every plaquette variable.

Products of per-link center flips `Gamma_l` (`U_l -> -U_l`) do the first job, and the sign they put on `W_f` is `(-1)^{|f cap E|}`. The requirement becomes a Z_2 1-cochain E with coboundary `delta E = 1` on every plaquette. A necessary condition is that the constant 2-cochain 1 be a cocycle. It is, because a cube has six faces and six is even. Section 4 constructs E and records the kernel of this inverse problem (Newton lens): the solution is unique up to center gauge transformations.

**Working back from (D1).** One needs an exact representation of `omega(W)` whose linear part is a single computable inner product and whose other parts are provably quadratic. The AV1 product split supplies it. It is a shared premise, admitted in AV1: `psi=psi_out+delta`, `(P_R x 1)psi=psi_out`.

Because `W Omega_R` is excited at **both** sites of R, the only linear overlap is with the creation supported exactly on R (Section 6). Everything else must be charged as second order, so it has to be itemized. One lemma was missing and is proved here: the outside excitation of `phi_out` is controlled by the anchored norm (R15).

## 3. Parity theorem (item 1)

**Grading.** For each link l let `Gamma_l` be the unitary `(Gamma_l psi)(U)=psi(...,-U_l,...)`. Haar measure is invariant under multiplication by the central element `-1`, so `Gamma_l` is unitary and fixes `Omega_0`.

On the Peter–Weyl block of spin j at link l, `Gamma_l` acts as `D^j(-1)=(-1)^{2j}`, while the Casimir `C_l` acts as `j(j+1)`. The two operators are therefore simultaneously diagonal and commute. Because `-1` is central, `Gamma_l` also commutes with every left and right translation, and hence with every endpoint gauge action.

A product of plaquette variables is odd under `Gamma_l` exactly when link l carries an odd number of j=1/2 factors. Hence

\[
\mathbb E_{\rm Haar}\Big[\prod_iW_{f_i}\Big]=0\quad\text{whenever }\ f_1\triangle f_2\triangle\cdots\ne\varnothing ,
\tag{HNM-AW1-R04}
\]

which is the Peter–Weyl statement that the trivial representation does not occur in a tensor product containing an odd number of spin-1/2 factors at some link. For a single plaquette, the holonomy of four independent Haar links is Haar. So `E[W^n]` equals `2^-n` times the multiplicity of spin 0 in `(1/2)^{⊗n}`. That multiplicity is a Catalan number for even n and 0 for odd n.

\[
\mathbb E[W^n]_{n=0..8}=1,0,\tfrac14,0,\tfrac18,0,\tfrac5{64},0,\tfrac7{128}.
\tag{HNM-AW1-R05}
\]

The checker computes these values three independent ways, all in exact rationals:
- **Clebsch–Gordan recursion:** `chi_{1/2}chi_j=chi_{j-1/2}+chi_{j+1/2}`.
- **Weyl integration:** `(2/pi) int_0^pi cos^n sin^2`, evaluated by Wallis ratios.
- **Free-link cross-check (AQ2 §5):** W contains the free z link `(e_x,z)`. Conditional on the other links, the face holonomy `A U_(e_x,z) B` is therefore Haar, `W=q_0` is uniform on S³, and `E[q_0^{2m}]=prod_{i<m}(2i+1)/(4+2i)`. This route gives `E[W]=0` and `E[W^2]=1/4` without the character count, as the contract requires. It is a named cross-check, not a replacement.

**Vanishing pairings.** Distinct plaquettes share at most one link, so `f≠W` has at least three links outside W.
- For `W^2 W_f` with `f≠W`, the links of f outside W carry exactly one j=1/2 factor. For `f=W`, every link of W carries three.
- Hence `E[W^2 W_f]=0` for every omitted f, including f=W, and `E[W_f]=0`.

The checker enumerates all 1344 omitted faces of `Lambda_2` and all 82 faces meeting R.

**The three first-order terms.** Write `C_N(s)=<chi_N,e^{-s(G_N-E_N)}chi_N>`, with `chi_N=(W-m_N)psi_N` and `m_N=omega_N(W)`. Since `e^{-s(G-E)}psi=psi`, it follows that `C_N(s)=<W psi_N, e^{-s(G_N-E_N)} W psi_N> - m_N^2`, where `m_N^2=O(tau^2)`. At `tau=0`, `W Omega_0` is a `G_0` eigenvector with eigenvalue 3. Then

\[
\begin{aligned}
\text{state:}&\quad 2e^{-3s}\,\mathrm{Re}\langle\psi^{(1)},W^2\Omega_0\rangle=2e^{-3s}\tfrac{\tau}{72}\sum_f\mathbb E[W^2W_f]=0,\\
\text{Duhamel:}&\quad -s\,e^{-3s}\big(\langle W\Omega_0,V\,W\Omega_0\rangle-E^{(1)}\|W\Omega_0\|^2\big)=-s\,e^{-3s}\big(-\tfrac{\tau}{24}\textstyle\sum_f\mathbb E[W^2W_f]-0\big)=0,\\
\text{energy:}&\quad E^{(1)}=\langle\Omega_0,V\Omega_0\rangle=-\tfrac{\tau}{24}\textstyle\sum_f\mathbb E[W_f]=0 .
\end{aligned}
\tag{HNM-AW1-R06}
\]

The real-time correlation `omega(W alpha_theta(W))-m^2` has the same three terms, with `e^{3i theta}` and `i theta e^{3i theta}` in place of `e^{-3s}` and `-s e^{-3s}`.

The state term pairs `c^(1)` against the vector `W alpha^0_theta(W) Omega_0 = e^{3i theta} W^2 Omega_0`. It also pairs `c^(1)` against the adjoint-ordered vector `e^{-3i theta}[(1/4)Omega_0 + e^{8i theta}(W^2-1/4)Omega_0]`. Both vectors are even under every `Gamma_l`, while each summand of `c^(1)` is odd on the four links of its face, so both pairings vanish. The same state term shows that `omega(W^2)` has no first-order part.

By contrast, `2 Re<W Omega_0, psi^(1)> = (tau/36) sum_f E[W W_f] = tau/144`, because only f=W pairs with W. **Parity does not remove the first-order mean.**

**Degenerate multiplet.** The vector `V W Omega_0` is a sum of components `W_f W Omega_0` whose odd-link sets are `W △ f`. The checker enumerates all 1344 faces of `Lambda_2`:
- **Size 0**, for f=W only. The component is `W^2 Omega_0 = (1/4)Omega_0 + (W^2-1/4)Omega_0`, with the vacuum at energy 0 and spin one on W's links at energy 64 (normalized).
- **Size 6**, for the 10 omitted faces that share one link with W; the other two faces sharing a link with W are selected.
- **Size 8**, for the remaining 1333 faces, which share no link with W.

An energy-24 vector has exactly four odd (j=1/2) links and spin 0 everywhere else. So no omitted face maps `W Omega_0` back into the energy-24 multiplet, except through the identity component, which leaves it.

\[
P_{24}\,V\,W\Omega_0=0,\qquad\text{and on the gauge-invariant multiplet } \mathrm{span}\{W_g\Omega_0\}:\ \ \mathbb E[W_gW_fW_h]=0\ \ \forall g,f,h .
\tag{HNM-AW1-R07}
\]

The triple statement follows because E, defined in Section 4, pairs oddly with the Z_2 chain `g+f+h`, which therefore cannot vanish. The checker verifies all 95,284 multisets of three faces meeting R. The first-order splitting of the physical multiplet is therefore zero.

This is not claimed for the unconstrained, non-gauge-invariant energy-24 eigenspace. There, vectors with two of their four half-spin links on a face f can be mapped by `W_f` back into the eigenspace. The dynamics of `chi` stays in the gauge-invariant sector, because G commutes with the gauge actions.

**Conclusion of item 1.** Fix N and the cutoff. `H_N(tau)=H_0+tau V'` with V' bounded, and the ground is simple with a gap of at least 1/2 for `|tau|<=10^-8` (AM2). By analytic perturbation theory (Kato; cited, not machine-checked), `psi_N`, `C_N(s)`, `c_N(theta)` and `omega_N(W^2)` are therefore real-analytic in tau on the interval. Their first derivatives at 0 are the sums of the terms in (R06), which vanish. Hence

- `C_N(s) = e^{-3s}/4 + O(tau^2)` in every finite box. **The O(tau^2) constant of C(s) is explicitly left unbounded**, so no uniform-in-N or AQ-limit tau² statement for C(s) is made here.
- `omega(W^2) = 1/4 + O(tau^2)`, with a supplementary uniform exact-tier constant (R19). That constant passes to every AQ subsequential limit.

The flip lemma of Section 4 gives a second, independent route to the same first-order vanishing in each finite box: `C_N` and `omega_N(W^2)` are even in tau, so their odd Taylor coefficients vanish.

## 4. Link-flip antisymmetry lemma (item 2)

**Reconstructing E.** Search the rules "link `(p,d)` is in E iff `p_{sigma(d)}` is even", where `sigma: {x,y,z} -> {x,y,z}`.
- In an xy face the two x links differ only in `p_y`, and the two y links differ only in `p_x`.
- So the face meets such a set oddly iff exactly one of `[sigma(x)=y]` and `[sigma(y)=x]` holds. The same holds for xz and yz with the corresponding pairs.

Exactly two of the 27 rules satisfy all three orientations. The checker enumerates the rules on the residue cube. The two solutions are the derangements:

\[
E=\{(p,x):p_y\text{ even}\}\cup\{(p,y):p_z\text{ even}\}\cup\{(p,z):p_x\text{ even}\}\ \ (\text{cyclic}),\qquad E'=\{(p,x):p_z\}\cup\{(p,y):p_x\}\cup\{(p,z):p_y\}\ \ (\text{anti-cyclic}).
\tag{HNM-AW1-R08}
\]

The contract's E is the cyclic solution; its text is parsed and compared only after this derivation. The two solutions differ by the coboundary of `g(p)=p_xp_y+p_yp_z+p_zp_x mod 2`, which the checker verifies on a box. That coboundary is a center gauge transformation and acts trivially on gauge-invariant observables. E itself is not a cocycle, since its coboundary is 1 on every plaquette. So `U_E` is **not** a gauge transformation, and it genuinely flips gauge-invariant observables.

**Odd intersection, by full enumeration.** The count in each orientation is `1+2[one coordinate even]`, which lies in `{1,3}`. The checker enumerates:
- all 24 residue cases (three orientations times `p in {0,1}^3`);
- every plaquette of the fine box `[-9,9]^3`: 20,577 plaquettes, 10,830 meeting E once, 9,747 meeting it three times, and 0 meeting it evenly;
- **all 49 omitted faces of factor 0 and all 49 of factor e_z.** These two factors exhaust the two z-parity classes: coarse x and y translations are even fine shifts (4 and 2), while a coarse z translation is a unit fine shift;
- the selected faces;
- every omitted and selected face of `Lambda_2`.

The histogram agrees with the numbers in the snapshotted skeptic sign-off (§3). Five damaging mutations are rejected:
- deleting one link from E, which leaves 4 plaquettes even;
- a vertex-star coboundary;
- the x-part of E alone;
- E on a periodic box with an odd side, which leaves 16 even seam plaquettes;
- the claim that a spin-one term `W_f^2` flips.

**Operator identity.** `U_E := prod_{l in E cap Lambda_N} Gamma_l` has the following properties:
- it commutes with every Casimir, every endpoint gauge action (and so every Gauss projector), and every on-site spectral cutoff `1_[0,L](h_x)`;
- it fixes `Omega_0` and `P_R`;
- it maps `W_f` to `-W_f` for every plaquette.

In particular it flips the selected faces, whose terms `-lambda_i W_i` appear in the onsite operator at a nonzero triple (AT4 F01). Therefore

\[
U_E\,H_N(\tau,\kappa)\,U_E^*=H_N(-\tau,-\kappa)\qquad\text{for every centered whole-star box and every on-site cutoff compression } Q_LH_NQ_L .
\tag{HNM-AW1-R09}
\]

The checker verifies (R09) term by term on `Lambda_2`:
- all onsite Casimirs, 1344 omitted and 375 selected face terms;
- at `kappa=0` and at `kappa=(1/7,-1/9,1/3)`;
- and it shows that the image differs from `H(-tau,kappa)` whenever `kappa≠0`.

An exact rational SU(2) configuration of W's four links and its four endpoint gauge elements confirms the operator facts directly: `W=167/210` goes to `-167/210` under the flip (three of W's links lie in E), is invariant under the gauge transformation, and the flip commutes with the gauge action.

**Finite volume at kappa=0.** AM2 gives a unique ground in the full Hilbert space and in every cutoff space. Since `U_E psi_N(tau)` is a ground of `H_N(-tau)`,

\[
U_E\psi_{N}(\tau)\propto\psi_N(-\tau),\qquad \omega_{N,-\tau}=\omega_{N,\tau}\circ\alpha_E,\qquad
\omega_{N,-\tau}(W)=-\omega_{N,\tau}(W),\quad \omega_{N,-\tau}(W^2)=\omega_{N,\tau}(W^2),\quad C_{N,-\tau}=C_{N,\tau},\ c_{N,-\tau}=c_{N,\tau} .
\tag{HNM-AW1-R10}
\]

For the correlations, `alpha_E` intertwines `e^{i theta G_N(tau)}` with `e^{i theta G_N(-tau)}`. Then `W->-W` appears twice, and the mean `m -> -m` enters only through `m^2`.

**AQ passage.** Along any subsequence `N_k` on which `omega_{N_k,tau}` converges locally in trace norm, the states `omega_{N_k,-tau}` converge to `omega_tau ∘ alpha_E`. Here `alpha_E` is conjugation by the local `U_{E cap F}` on each finite region F, and these conjugations define a consistent automorphism of the quasi-local algebra. Hence

\[
\mathcal S(-\tau)=\mathcal S(\tau)\circ\alpha_E\qquad(\text{sets of subsequential AQ limits}).
\tag{HNM-AW1-R11}
\]

The identity `omega_{-tau}(W)=-omega_tau(W)` holds state by state only for states paired along a common subsequence. AQ1's diagonal extraction depends on tau, so the chosen `-tau` state must be defined that way.

`alpha_E` intertwines the finite dynamics, and hence their Nachtergaele–Sims norm limits, and it transports the GNS data. So paired states have equal `C(s)`, `c(theta)` and `omega(W^2)`. The checker's toy sequence obeys the finite-volume identity exactly and has two subsequential limits. Its limit sets are negatives of each other, but independently chosen subsequences give a nonzero sum `1/500`. The pointwise claim without a common subsequence is rejected.

**Oddness gives no O(tau^3).** In each finite box, real-analyticity plus oddness removes the tau² Taylor coefficient of `omega_N(W)`, but with an N-dependent tau³ constant. An odd function obeying `|r|<=K tau^2` need not be `O(tau^3)`: `r=K tau|tau|` is odd and saturates the bound. The AQ limit function of tau is not even known to be continuous. **No third-order remainder is claimed.** `K_2` below is an absolute second-order bound. The snapshotted modern-lens remark that the "direct" remainder is `O(tau^3)` is not used.

**Nonzero kappa.** The identity sends kappa to -kappa. The contract control rejects tau-antisymmetry "from U_E" at a nonzero triple, and the checker implements that rejection. There is also a positive demonstration on a finite graph (`two_plaquette_omitted_plus_selected`, `model_is_finite_graph:true`, `transfers_to_aq:false`):
- **Plaquettes.** One omitted plaquette f carries tau and one selected plaquette g carries `kappa=1/7`; each is truncated at `j<=1/2`.
- **Hamiltonian image.** `U_E H(tau,kappa) U_E = H(-tau,-kappa)` exactly, and this differs from `H(-tau,kappa)`.
- **Signed selected-face mean.** `<W_g> = (7/884)sqrt(442/49)` at `(tau,kappa)` and its exact negative at `(-tau,-kappa)`. At `(-tau,kappa)` it is unchanged, so it is not tau-odd. Its first-order coefficient in kappa is `1/6`.

A related observation is recorded in Section 11 as a finding, and nothing in the claims depends on it.

## 5. First-order coefficient (item 3)

From (R02), with only f=W surviving (R04) and `E[W^2]=1/4`,

\[
\omega_\tau(W)=2\,\mathrm{Re}\langle W\Omega_0,\psi^{(1)}\rangle+O(\tau^2)=-2\,\mathrm{Re}\langle W\Omega_0,c^{(1)}\rangle+O(\tau^2)=2\cdot\frac{\tau}{72}\cdot\frac14+O(\tau^2)=\frac{\tau}{144}+O(\tau^2).
\tag{HNM-AW1-R12}
\]

**Sign.** The sign comes from the frozen convention. I1.5 puts `-(alpha tau/24) W_f` in H, so `tau>0` lowers the energy of `W_f>0` configurations and `psi^(1)` is `+(tau/72) sum W_f Omega_0`. The first-order terms at the two signs are `+1/14400000000` and `-1/14400000000`.

The sign fixture, `one_plaquette_character_truncation`, is a finite graph (`transfers_to_aq:false`) that does not use the creation formalism.
- **Model.** It is one gauge-invariant plaquette in the character basis `chi_j(U_f)`, with `G_0=diag(4j(j+1))` and `W chi_j=(chi_{j-1/2}+chi_{j+1/2})/2`. Its coupling is the I1.5 term `-(tau/24)W`.
- **Exact values.** At `j<=1/2` the checker computes `<W>` exactly in `Q(sqrt(9+tau^2/576))` for `+tau` and `-tau` separately. The results are exact negatives, and `<W>` has the sign of tau (about `6.9444e-11` at the cap).
- **Series.** At `j<=3/2` the exact series is `<W> = tau/144 + 0 tau^2 - (5/11943936)tau^3 + ...` and `<W^2> = 1/4 + 0 tau + (7/331776)tau^2 + ...`.

Reading the contract's display literally with the AM2 `c^(1)` would give `-tau/144`. That mutation is rejected, and so is the opposite-sign coupling.

**Wrong-face and orientation controls.**
- `E[W W_f]=0` for all 81 other faces meeting R, and the only nonzero pairing is W with itself.
- For each of the 21 omitted classes (xy with `s=1` or `r=3`, xz, yz), the class face `g` anchored at 0 has first-order mean coefficient exactly `1/144`, because only g pairs with itself. The coefficient is therefore orientation-invariant.
- Reversing the loop gives the same W, since `chi_{1/2}(U^{-1})=chi_{1/2}(U)`.

**Keeping f=W separate.** The 21 omitted classes anchored at 0 are W and 20 others:
- **9 others with owner set R.** They lie in `c^(1)_R` with W, but their pairing with W is zero by parity.
- **6 that strictly contain R.** Owner sets `{0,e_x,e_z}` (2 faces) and `{0,e_y,e_z}` (4 faces). They reach `omega(W)` only through the straddling term.
- **5 at the single site 0.** They reach it only through the two-creation and density terms.

The checker rejects excluding W from the omitted set (coefficient 0), merging it with the other R faces (`10/144`) and counting it twice (`2/144`).

## 6. Second-order remainder K_2 (item 4)

**Exact decomposition.** This is the shared AV1 split, admitted in AV1. Write `w := W Omega_R`. Then `||w||=1/2`, `<Omega_R,w>=0`, and w lies in `Q_0 ⊗ Q_{e_z} H_R`, because integrating over the link `(0,x)` (owned by 0) or `(e_z,x)` (owned by `e_z`) kills a single j=1/2 factor. Let `n=||phi_out||`, `d=||delta||`, `e=d/n`. Then

\[
\omega_N(W)=\frac{X+Y}{1+e^2},\qquad X=\frac{2\,\mathrm{Re}\langle w\otimes\varphi_{\rm out},\delta\rangle}{n^2},\qquad Y=\frac{\langle\delta,(W\otimes1)\delta\rangle}{n^2},\qquad |X|\le e,\ |Y|\le\|W\|e^2 .
\tag{HNM-AW1-R13}
\]

Insert `delta = -sum_{I cap R ≠ ∅} hat c_I psi_out + sum_{I∋0, J∋e_z, I cap J=∅} hat c_I hat c_J psi_out` (AV1 R07/F08) and sort the supports:

\[
X=\underbrace{-2\,\mathrm{Re}\langle w,c_R\rangle}_{I=R}\;\underbrace{-\;\frac{2}{n^2}\sum_{I\supsetneq R}\mathrm{Re}\langle w\otimes\varphi_{\rm out},\hat c_I\psi_{\rm out}\rangle}_{\text{straddling pairing}}\;+\;\underbrace{0}_{|I\cap R|=1}\;+\;\underbrace{\frac{2}{n^2}\sum_{\rm pairs}\mathrm{Re}\langle w\otimes\varphi_{\rm out},\hat c_I\hat c_J\psi_{\rm out}\rangle}_{\text{two-creation}} .
\tag{HNM-AW1-R14}
\]

The pieces behave as follows:
- **One site of R.** A creation meeting only one site of R leaves the vacuum at the other site, so it is orthogonal to w. Only the creation supported **exactly** on R overlaps `w`, with multiplier `2||w||=1`.
- **Supports strictly containing R.** For `I ⊋ R`, `<w ⊗ phi_out, hat c_I psi_out> = <(Q_{I∖R} ⊗ 1)phi_out, v ⊗ chi>`. Here `v=(<w| ⊗ 1)c_I` has norm at most `||w|| ||c_I||`, and `chi=(<Omega_{I∖R}| ⊗ 1)phi_out` has norm at most n.
- **Missing lemma.** For any outside site x, split `C_out = C_x + C_rest` with `C_x^2=0`. Then `phi_out = phi' - C_x phi'` with `phi' = (P_x ⊗ 1)phi_out`, so

\[
\|(Q_x\otimes1)\varphi_{\rm out}\|=\|C_x\varphi'\|\le t_x\|\varphi'\|\le t\,\|\varphi_{\rm out}\|,\qquad t_x=\sum_{I\ni x,\ I\cap R=\varnothing}\|c_I\|\le t=\|c\|_a .
\tag{HNM-AW1-R15}
\]

**The exact-tier ledger.** The ingredients are as follows.
- **Enumerated face counts.** A face vector has norm `|tau|/144`. The counts come from the snapshotted I1 table by translation covariance: 49, 15, 82, 16, 10, and 72 = 6 + 33 + 33. They are derived first and then compared with the contract's and the selection note's candidates.
- **Remainder.** `T=t_1/(1-352J)`, where `t_1=49|tau|/144` and `J=28|tau|`, and `rho=352 J T >= ||c-c^(1)||_a` (AM2; the self-consistent inequality admitted in AV1).
- **Sums.** `s_str=6|tau|/144+rho` over the 6 supports strictly containing R. `s_0=s_z=33|tau|/144+rho` over the single-site supports. `eps=82|tau|/144+2 rho+s_0 s_z`, which is at least e.

With these,

\[
|r_N(\tau)|\le B(\tau):=\underbrace{2\|w\|\,\rho}_{\rm am2\_remainder}+\underbrace{2\|w\|\,T\,s_{\rm str}}_{\rm straddling}+\underbrace{2\|w\|\,s_0s_z}_{\rm two\_creation}+\underbrace{\|W\|\,\varepsilon^2}_{\rm density}+\underbrace{(2\|w\|\varepsilon+\|W\|\varepsilon^2)\,\varepsilon^2}_{\rm normalization,\ third\ order},
\tag{HNM-AW1-R16}
\]

uniformly in N (anchored sums at the two sites of R, and the global t), and for every on-site cutoff `L>=24`.

Two remarks on the ledger:
- **Normalization.** The term is `-(X+Y)e^2/(1+e^2)`, which is third order.
- **Two-creation term.** The charge `2||w|| s_0 s_z` is conservative. Every first-order support has at least two sites, so a pair overlaps w only through an outside excitation (a further factor of t) or through second-order single-site remainders.

The bound passes to the untruncated ground (AV1 R20–R21, admitted) and to every AQ subsequential limit, by local trace-norm convergence with `W ∈ B(H_R)`.

**Values.** At the cap every entry is an exact rational; the table gives the ledger entries divided by tau².

| prereg term | exact tier: formula | exact tier / tau² | crude tier: formula | crude / tau² |
|---|---|---:|---|---:|
| `am2_remainder` | `2‖w‖·352JT` | 3354.108358 | `352 J t_c`, `t_c=J G(R)=592|tau|` | 5,834,752 |
| `straddling` | `2‖w‖·T(6|tau|/144+ρ)` | 0.014191053 | `t_c²` | 350,464 |
| `two_creation` | `2‖w‖·(33|tau|/144+ρ)²` | 0.052532735 | `t_c²` | 350,464 |
| `density` | `‖W‖ε²`, `ε=82|tau|/144+2ρ+s_0s_z` | 0.324343380 | `(2t_c+t_c²)²` | 1,401,864.30 |
| `normalization_order` | third order: `(ε+ε²)ε²` | 1.85e-9 | same form | 16.598 |
| `overlap_multiplier` | `2‖WΩ_R‖=1`; factor 4 only as a labelled conservative variant | (multiplier) | 1 | (multiplier) |
| `arithmetic` | exact rationals; 10^-40 ceiling recorded | 0 | exact | 0 |
| **K_2^+** | | **3354.499425** | | **7,937,560.897** |

The exact-tier inputs at the cap are:
- `J=7/25000000` and `352J=77/781250`;
- `t_1=49/14400000000` and `T=49/14398580736`;
- `rho=3773/11248891200000000`, about `3.354e-13`;
- `s_str=4690811/11248891200000000`;
- `s_0=s_z=12891241/5624445600000000`;
- `eps=180161487949673694520081/31634388307359360000000000000000`, about `5.695e-9`.

\[
K_2^{+}\big|_{\rm exact}=\tfrac{335942915356298769555715666601290415707014310237805041914404419632200046154878741653786750596559055288284056326721}{100146958668647993093845753187387660708265550837569567080841216\cdot10^{48}}\le\tfrac{33544994258669290845093439980837832702606211}{10^{40}}\approx3354.4994,
\tag{HNM-AW1-R17}
\]

\[
K_2^{+}\big|_{\rm crude}=\tfrac{1848107412764512772541657452411636431629453921}{232830643653869628906250000000000000000}\approx7.9375609\times10^{6}.
\tag{HNM-AW1-R18}
\]

Tier discipline:
- Every entry names its tier and provenance, and the checker rejects tier mixing.
- The crude tier uses only `t_c` and never the face counts.

**Variants:**
- *Conservative overlap factor 4:* `K_2 ≈ 13,416.82` (labelled). It sits inside the skeptic sign-off's "1.1–1.9e4" range, which appears to charge that factor.
- *Directed remainder `rho'=J(G^+(T)-16)`:* about `288 J T`, giving `K_2 ≈ 2744.66`.

`B(tau)/tau^2` is nondecreasing in `|tau|`, since every entry is `tau^2` times a nondecreasing function. The cap value therefore bounds every smaller `|tau|`. The checker's values at `tau/10`, `tau/100` and `tau/1000` are 3354.2018, 3354.1720 and 3354.1691. The exact ratio `B(tau)/B(tau/10)=100.00887` confirms quadratic scaling, against 10 for the first-order term and 10.0009 for AV1's linear D. The `-tau` evaluation is a replay of the same `|tau|` formula.

**Supplementary constant for `omega(W^2)` (item 1; not a target).** With `y=(W^2-1/4)Omega_R`, `||y||=1/4`, y excited at both sites of R, and `||W^2-1/4||=3/4`:

\[
|\omega_N(W^2)-\tfrac14|\le 2\|y\|\,(\rho+T s_{\rm str}+s_0s_z)+\tfrac34\varepsilon^2,\qquad K_{W^2}\approx1677.3308 .
\tag{HNM-AW1-R19}
\]

**Algebra audit.** The exact finite fixture `four_site_creation_algebra` (`model_is_finite_graph:true`, `transfers_to_aq:false`) has sites 0 and `e_z` of dimension 3, two outside sites of dimension 2, ten creations of every support type, and a Hermitian W with `||W Omega_R||=1/2`. The checker verifies the following exactly:
- (R13), and that the product order of the creations is irrelevant;
- the split (R14): the five one-site-of-R creations contribute exactly 0;
- the straddling part `-391/2930` and the pair part `-612/36625` lie inside their bounds, and `X ≠ X_R`, so the straddling term must be charged;
- `|Y| <= ||W|| e^2` and `e <= eps`;
- (R15) at both outside sites.

## 7. Sign-certificate feasibility and the frozen AW2 rule (item 5)

The target `1/288` and the rule text are read from the hash-checked contract.

\[
K_2^+\tau\big|_{\tau=10^{-8}}\approx3.3545\times10^{-5}\le\tfrac1{288}\ (\text{margin}\approx103.51),\qquad \frac{1}{144K_2^+\tau}\approx207.02\ge2,\qquad \tau_{\rm AW2}=10^{-8}.
\tag{HNM-AW1-R20}
\]

For comparison:
- **Conservative variant:** `K_2 tau ≈ 1.3417e-4` is also feasible, with margin about 25.9.
- **Crude tier:** `K_2 tau ≈ 7.94e-2` fails `1/288` by a factor of about 22.9. It is retained as a limited-tier value. Its rule value `10^-10` is recorded as information only, because the frozen rule takes the exact-tier constant.

**No enclosure or sign of `omega(W)` is admitted in AW1.** AW2 instantiates the enclosure at `tau_AW2`, and the `-tau` enclosure will be the image of the `+tau` one under (R10). The static nature is explicit: the first-order C(s) coefficient is zero while the `omega(W)` coefficient is `1/144`. This is an equal-time ground mean, not a dynamical or mass-gap correction.

## 8. Consistency controls (item 6)

- **Sign flip.** `tau -> -tau` flips the signed first-order term, the exact one-plaquette values (signs +1 and -1) and, by (R10), the exact finite-volume value. The sign-blind readings are rejected.
- **AV1 compatibility.** The AV1-admitted `D_ii = 585079838465912592144137406066050/42981220507576537932303142777593983768257 ≈ 1.3612e-8`, read from the AV1 gate snapshot, satisfies `D_ii >= |tau|/144 + K_2^+ tau^2 ≈ 6.978e-11`.
- **Haar parity.** It is computed exactly from character tables, the Weyl formula and sphere moments. There is no sympy or float anywhere in the admission path; the one-plaquette fixtures use exact `Q(sqrt D)` arithmetic.

## 9. Checker and controls (item 7)

`check.py --output <absolute fresh dir>` uses the standard library only.

**Before any evaluation it:**
- records its own sha256;
- verifies the contract snapshot's sha256;
- derives the first-order coefficient.

**It then reads** the following from the contract, and validates each semantically:
- the target `1/288`;
- the reference values `0` and `1/4`;
- the flip set;
- the AW2 rule;
- the first-order candidate;
- the prereg error-term list;
- the 30 controls.

**Outputs.** It writes `results.json` with sorted keys and 57 checks, and `source-manifest.json`.

**Claim flags:**
- `continuum_claim:false`
- `uniform_wilson_claim:false`
- `resolved_interaction_shift:false`
- `scientific_priority_verified:false`
- `first_order_parity_claim:true` (item 1 complete)
- `flip_lemma_claim:true` (kappa=0, finite volume and set-level AQ)
- `third_order_remainder_claim:false`

Every one of the 30 controls is a damaging mutation that must raise an explicit exception. The checker never uses `assert`.

| control | damaging mutations rejected |
|---|---|
| missing_incoming_stars | outgoing-star count 21; two-anchor sum 42; anchors {0,e_z} only |
| full_original_wilson_cover | cover {0}; cover with an extra factor |
| wrong_delta_alpha_hbar_clock | mixed-unit amplitudes (tau/1152, tau/18); exponent 24 on the alpha clock; exponent 3 on the delta clock |
| vector_versus_scalar_centering | scalar subtraction as vector centering (−51/10000 vs +1/10000); negative vector residue |
| first_order_mean_charged | zero first-order mean; uncentered = centered at tau² (m² = tau²/20736); variance without m² |
| tau_scaling_exponent | AV1 linear D as the tau² remainder (ratio 10.0009); first-order term as remainder; cubic claim |
| changed_model_relabelled | nonzero triple; coupling above cap; finite-graph id as model; finite-box provenance |
| coherent_evidence_tampering | 8 rehashed contract tampers (target 1/144, flip set, candidate tau/72, AW2 threshold, cap, reference 1/3, error term, control removed) + byte change |
| insufficient_verdict_retained | crude-only → accepted; parity failure → limited; coefficient failure → limited; finite-volume flip → accepted |
| exact_arithmetic_admission | float tau; bool; NaN; float admission; zero denominator |
| root_n_misuse | sqrt(82) for the l1 R-sum (≈9.06 vs ≥43.49); root-sum-square ledger |
| no_priority_or_continuum_claim | continuum, priority, uniform-Wilson, resolved-shift flags true |
| haar_parity_exact | E[W³]=1/8; E[W⁴]=E[W²]²; E[W²]=1/2; float moment |
| first_order_shift_of_C_vanishes | state term with W for W²; Duhamel counting f=W; static mean as C shift; missing itemization |
| degenerate_multiplet_first_order | identity component, one-shared-link (energy 36) and spin-one (64) components as multiplet members |
| wilson_mean_first_order_coefficient | 1/36, 1/288, −1/144 (AM2 sign literal), 1/1152, 1/18, 10/144 |
| wrong_face_control | an in-R yz face contributing; a straddling face contributing; W self-pairing dropped |
| sign_flip_tau | sign-blind −tau term; sign-blind fixture; fixture read at +tau for −tau |
| second_order_remainder_itemized | straddling dropped; zero AM2 remainder; unpinned density; normalization dropped |
| static_not_dynamic_effect | dynamical, mass-gap and C(s)-shift labels |
| wilson_overlap_single_component | unlabelled factor 4; multiplier 1/2; factor 2 as conservative |
| sign_convention_fixture | contract formula with AM2 c^(1) (−tau/144); opposite-sign coupling |
| aw2_coupling_rule_prefrozen | 10^-9 (not largest); crude-constant choice; off-grid 2·10^-8; threshold 1/144 |
| flip_set_odd_intersection | E minus one link (4 even); vertex-star coboundary; x-part only; odd periodic side; W_f² flips |
| flip_breaks_at_nonzero_kappa | tau-antisymmetry via U_E at kappa_L or kappa_M ≠ 0; image claimed H(−tau,kappa) |
| flip_no_third_order_claim | O(tau³) from oddness; O(tau³) from the flip lemma (counterexample K tau|tau|) |
| tier_mixing_rejected | exact counts with crude remainder; crude ledger with exact density; t_1 without self-consistency |
| reverse_premise_isolation | triage, loop-2 response, deliberation, forward AW1 file added; premise removed |
| wilson_face_separated | W excluded (20 classes); W merged with the 10 R faces; W counted twice |
| flip_nonzero_kappa_positive_demonstration | image claimed H(−tau,kappa); selected mean claimed tau-odd at fixed kappa (the positive demonstration is recorded alongside) |

## 10. Premise isolation and files read (item 8)

**Inventory.** `inputs/` equals AGENTS.md, the contract and the 29 `shared_premises` exactly, 31 files in all. The checker and `freeze.py` enforce this, and nothing was added.

**Snapshots read in full:**
- the contract and AGENTS.md;
- `selection-aw1.md`;
- both loop-3 sign-offs;
- AV1's contract, gate, forward report, reverse report and skeptic review;
- AV2's contract, gate (without its bindings list) and reverse report;
- AM2's forward report, reverse report, skeptic review and gate;
- AQ1, AQ2, AT4 and I1;
- the paired-physics, Newton, Tesla and historical-panel SKILL files, the complete-residual reference, the historical `lenses-and-evidence.md` and the Newton `references/research.md`.

**Snapshots read in part:**
- AV2 forward report and `skeptic/av2.md`: a keyword search for parity, first-order and flip, plus the skeptic's "advice for AW1" section;
- Tesla `references/research.md`: its Round32 rule only.

**Inherited files outside `inputs/`, for protocol and style only:**
- `research/round32/tools/README.md` and `research/round32/tools/freeze.py`;
- `research/round32/reverse/av1/check.py`, portions, for code style;
- `research/round32/reverse/av2/check.py`: its line count only.

None of these carries premise weight.

**What is shared rather than derived.** The AV1 product split and the AM2 constants are shared, admitted premises. So is the contract's own text, which states the flip set, the target coefficient and the candidate counts; I parsed those and compared them only after my derivation. The panel sign-offs I read also state the flip idea. Independence is therefore claimed only for:
- the derivations and reconstructions: the grading argument, the reconstruction of E (with the two-solution kernel), the lemma (R15), the itemization and the convention finding;
- the code and the fixtures.

All producers and reviewers are correlated model agents. This is not human review.

## 11. Findings for review

1. **Sign convention in contract item 3.** `omega=2<W Omega_0,c^(1)>` holds for `psi^(1)`, not for the AM2 `c^(1)=L_0`, which is its negative. The value `+tau/144` stands.
2. **The kappa obstruction is not intrinsic (finding, not claimed).** The selected-face indicator is a Z_2 coboundary. Every elementary cube contains 0 or 2 selected faces, and an explicit period-8 cochain `E''` has `delta E''` equal to the selected indicator; this is enumerated exactly (check `finding_selected_even_flip_cochain_not_claimed`). The set `E_1 = E xor E''` then meets omitted faces oddly and selected faces evenly, so `U_{E_1}` would map `H(tau,kappa)` to `H(-tau,kappa)`. That would extend tau-antisymmetry of omitted-face means to every selected triple, **provided** the selected-strip onsite operator contains only Casimirs and selected `W` terms. That is the AT4 F01 form; the A1 strip theorem is not among my inputs. No claim flag or Boolean uses this finding. It does not change the contract control, which concerns U_E.
3. **K_2 size.** The exact-tier constant is dominated, about 99.99%, by AM2's generic remainder `352 J T`. The directed `G` form lowers it to about 2745. The parity grading kills the tau² coefficient of the actual `omega_N(W)` in finite volume but does not shrink this absolute bound.
4. **Two-creation refinement.** First-order supports have at least two sites, so the pair term is actually third order. The charged `s_0 s_z` is conservative.

## 12. Limitations and exclusions

**Claim exclusions, exactly as the contract lists them:**
- an admitted enclosure of omega(W) (AW2)
- a dynamical or mass-gap correction (static_not_dynamic)
- any third-order remainder from oddness alone
- uniform Wilson magnetic theory
- AQ uniqueness or a rate in N
- continuum construction
- scientific priority

**Preregistered exclusions, also respected:**
- a free reference inside the enclosure means no interaction claim;
- uniqueness of the AQ state;
- whole-sequence convergence or a rate in N;
- continuum or weak coupling;
- transfer from a finite graph;
- relabelling a static shift as dynamical;
- scientific priority.

**Honest gaps.** The following are incomplete or rest on inheritance.
- **C(s) at order tau².** Its constant is explicitly unbounded. The first-order vanishing of C(s) is a finite-volume Taylor statement, and in AQ limits only the set-level evenness (R11) is proved.
- **Inherited without re-proof:**
  - AM2's fixed point, majorant and gaps;
  - AV1's product split, self-consistent remainder, cutoff-vector convergence and AQ passage;
  - AQ1's construction and Nachtergaele–Sims dynamics;
  - the I1 dictionary.
- **Cited, not machine-checked:** Kato's analytic perturbation theory, the Duhamel formula and the Peter–Weyl theorem. The checker verifies their finite consequences.
- **Fixtures.** They are finite graphs or algebra audits (`transfers_to_aq:false`) and prove nothing about infinite volume.
- **Upper bounds only.** K_2 is an upper bound, with no lower bound and no sign of `r(tau)`. The `-tau` ledger is a replay.
- **Model scope.** Nothing transfers to nonzero selected triples, to uniform Wilson theory or to the continuum.

**Method lenses.** These are modern methodological uses of the frozen Round32 skills; no historical figure endorses anything here.
- **Newton:** every inverse problem is solved with its kernel stated. The flip set is unique up to center gauge transformations, and the first-order coefficient was computed before any error budget was charged, following the Round32 rule.
- **Tesla:**
  - the source is the seven incident stars, with 82 faces meeting R;
  - the load is the cover R;
  - there is no clock, because the effect is static;
  - the transfer element is the partial vacuum contraction, with every channel charged;
  - the `±tau` mirror is a control, not a magnitude.
- **Historical panel:** set-level AQ statements are never called uniqueness.

## Reproduce

```bash
python3 -B research/round32/reverse/aw1/check.py --output /absolute/fresh/dir
python3 -B -O research/round32/reverse/aw1/check.py --output /absolute/fresh/dir2   # byte-identical
python3 -B research/round32/tools/freeze.py verify research/round32/reverse/aw1
```
