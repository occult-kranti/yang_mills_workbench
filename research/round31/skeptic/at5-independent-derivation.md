# AT5 independent calculation before producer comparison

The AT4 reviewed method applies at the newly declared zero-selected tau=+10^-14 AQ state. It does not identify that state with AT4's tau=+10^-8 state. At s=1,L=10^9, write p=49*tau/3, D=2sqrt(p), and k=49*tau/4. The conservative reverse route gives a complete radius bounded by

D + 4p + (k/pi) log(1+L²) + 4/(pi L).

Independent coarse rational bounds suffice: pi>3 and log(1+10^18)<42. The logarithm inequality follows without calling a transcendental function: exp(1)>sum_{j=0}^5 1/j!>27/10, and exact integer arithmetic verifies (27/10)^42>1+10^18. Thus the sufficient bound D+4p+14k+4/(3L) is below 10^-6. Integer square-root enclosure supplies an outward D. A degree-44 alternating enclosure for exp(-1), cubed and divided by four, brackets the exact free C_0(1).

The actual AQ interval is [C_0^- - error,C_0^+ + error]; its midpoint is rational and its full point-error radius includes half the free arithmetic interval width. The independent output verifies this radius is below 10^-6 while the full interval width exceeds 10^-6; this distinguishes radius from width. The exact free value remains inside, so no interaction-induced shift is resolved. Both signs obey the same estimate through |tau|; exact tau=0 has the separate exact free identity.

This direct infinite-state analytic enclosure bypasses a numerical finite-box/cutoff solver only for the declared parameter subcase. The generator, complete-factor geometry, seven-star incidence, true centering and nonnegative spectrum remain the admitted AT4/AQ premises. No state uniqueness, cap-level precision, uniform Wilson theory or inverse response follows.

The independent checker passes 19 exact controls in normal and optimized Python. It imports no current producer implementation or output. Its coarse log/tail enclosure differs from the previously used precision arithmetic and independently suffices for the claimed accuracy. API semantics and producer-specific tight constants will be audited only after both reports freeze.
