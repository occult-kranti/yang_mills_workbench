# AI2 independent reconstruction before producer exchange

The skeptic uses the actual cube at O=(3,1,0). It rebuilds its twelve links, six faces and all sixteen simple six-cycles from coordinates. A six-edge even subgraph with six occupied vertices cannot split into disjoint cycles on this cube because its girth is four. The two source pairs are (XZ,YZ) and (XZ,XZ symmetric-difference the x=4 yz face). Their connecting face exponents are four and five. Both vacuum sources are normalized sums of two orthogonal characters. Their multiplication norm is 2 sqrt(2); it is not the norm-one rank source used in earlier work.

The combined support has ten free-link factors. Complete-factor incidence gives the following retained-face counts from depths zero to five:

    N_k = 2, 25, 143, 359, 695, 1171.

At depth five there are 993 reference factors and 1857 complete links. All six cube faces occur by depth one. The old eight-link support misses part of the new source; copying N_3=332 would therefore be wrong.

For a support starting on ten factors, the complete-factor connected count changes the Pochhammer parameter from 8/3 to 10/3. Each factor contains at most ten links, each link is incident to at most four faces, and each new face adds at most three factors. Combining the factor-two commutator, coefficient 1/24 and time simplex gives an order-n bound J (10/3)_n x^n/n! with x=10 alpha tau |t|/hbar. At the original clock, x<=15z. The conservative entire omitted tail is

    D_k(x) = [(10/3)_(k+1)/(k+1)!] x^(k+1)/(1-x)^(k+5).

The larger denominator exponent rounds k+13/3 upward. It never truncates the omitted tail at the first shell.

The inherited AA2 component-wide exterior-exclusion and averaged-orbit argument applies to either new source in the same sixteen-state space. With v=s_q/96 and M=N_k/24, the exact degree-eight retained scalar polynomial has remainder at most (6v)^9/9!. The complete physical disk is bounded by

    48 dhat_q + 8 D_k(15z)
      + 64 tau_q M (1+3zM) + (6v)^9/9!.

The factor 64 is the conservative bound (1+2sqrt(2))*16 < 64. The first term retains the full stationary connected state correction, the second keeps actual multiplier norms, and the third retains both source/vacuum evolution replacements. This applies the inherited theorem; it does not independently re-prove the entire infinite-system history.

The retained first moments are exactly q^4 and q^5. A finite-time ratio can use |Im f_r(v)-v q^r|<=36v^3, from the scalar spectral sine remainder. If delta_r includes this and the full physical/readout errors, then a positive denominator vq^4-delta_4 gives

    |y5/y4-q| <= (delta_5+q delta_4)/(vq^4-delta_4).

A denominator containing zero permits no ratio conclusion. This value certificate is not differentiated into a derivative theorem.

All eighteen predeclared scalar comparisons were evaluated in exact rational arithmetic, with upward square-root enclosure. The compensated hypotheses have equal alpha eta(1-q)^3 and therefore the same physical time. Only u=10^-18, k=5 certifies disjoint imaginary intervals (hence disjoint complex disks) for either probe. Conservative gap margins are approximately 3.2145242143e-26 for B4 and 4.4050004047e-26 for B5. They permit equal extra absolute readout-error radii strictly below half of those margins for each hypothesis. The physical time is 2e48 hbar/alpha.

The simple cubic ratio enclosure is insufficient to resolve the two q values at every predeclared cell. At u=10^-12 the state error is dominant; at u=10^-24 the finite collar spatial tail is dominant. Overlap says this sufficient certificate fails, not that the two exact physical models are equal. The successful cell is a conditional mathematical two-hypothesis discrimination, not a general continuous parameter inverse or realizable experiment.

Executed evidence is in `ai2-independent.json` from `ai2_independent.py`. No current producer AI2 report/checker was read before these calculations were completed.
