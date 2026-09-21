# Newton, Tesla and resonance: sources, equations and limits

Reading updated 21 September 2026. This is a selected coverage map relevant to the workbench, not a claim to have completed every field studied by Newton or Tesla. Primary text, modern reconstruction and project inference are separated below. Full copyrighted articles are linked, not bundled. The machine-readable reading ledger records what was actually inspected and access gaps.

## Tesla did not use Schumann's later equation

[Tesla's US787412A](https://patents.google.com/patent/US787412A/en), granted in 1905, proposes stationary waves in an Earth conductor, a diameter/quarter-wavelength condition, and a lowest rate near six per second. It also discusses tuned circuits and an excitation duration. These are patent proposals and reported observations, not an established modern cavity derivation. Writing his lowest diameter condition in modern notation gives f≈c/(8R), about 5.88 Hz for R=6371 km. That reconstruction is ours.

The [Tesla Museum identity-document catalogue](https://tesla-museum.org/en/legacy/archive/identity-documents/) dates his death to 7 January 1943. Schumann's paper is from 1952, [DOI 10.1515/zna-1952-0202](https://doi.org/10.1515/zna-1952-0202). Its bibliographic identity was checked, but the full original paper could not be retrieved in this review. Thus attributing that later equation to Tesla is chronologically unsupported.

The thin, lossless spherical-shell model has surface Laplacian eigenvalues l(l+1)/R². Combining them with wave speed c gives the modern reconstruction

    omega_l = (c/R) sqrt(l(l+1)),
    f_l = c/(2 pi R) sqrt(l(l+1)), l=1,2,... .

Its first frequency is about 10.59 Hz, not 7.8 Hz. [Simões, Pfaff and Freudenreich's NASA manuscript](https://ntrs.nasa.gov/api/citations/20120000051/downloads/20120000051.pdf), pages 2–4, states this ideal model and explains why realistic boundaries and losses lower the frequencies. It lists approximate mean modes 7.8,14.3,20.8,27.3,33.8 Hz; its particular satellite spectrogram has peaks near 7.8,14.0,20.4,26.7,33.0 Hz. Those are different summaries, not contradictory exact constants. The paper reports detection above the nominal cavity boundary. Neither sequence is an exact integer harmonic ladder.

| Model | Boundary and source | Frequency meaning |
|---|---|---|
| Tesla patent proposal | Earth conductor; driven electrical apparatus | Diameter/quarter-wave operating condition, not the later shell eigenproblem |
| Ideal Schumann model | Thin lossless Earth–ionosphere shell | Eigenfrequencies proportional to sqrt(l(l+1)) |
| Measured Earth response | Lossy, varying ionosphere; lightning; location and field component | Broad forced spectral peaks; source and measurement geometry matter |
| AA endpoint | Canonical SU(2) reference-energy block; specified quantum input | Dimensionless splittings 2 and 2 sqrt(3) in theta=z/84; no identification with terrestrial Hz |

## Add variables only when they resolve a specified ambiguity

An illustrative single-mode response is

    u''+2 gamma u'+omega_0² u=d(t),
    H(omega)=1/[omega_0²-omega²-2i gamma omega],
    dE/dt=d(t)u'-2 gamma(u')²,
    E=[(u')²+omega_0² u²]/2.

Here gamma is a loss rate in s^-1 and d is a driver with displacement/s² units in this normalization. For white forcing and a constant readout, the displacement-power maximum is at sqrt(omega_0²-2 gamma²), when that is real. A colored driver or a different field readout changes the peak. This elementary model illustrates a distinction; it is not a complete Earth-ionosphere solver or a new law.

A speed factor chi in f_l=chi c sqrt(l(l+1))/(2 pi R) is a declared phenomenological correction. One mode can fit chi; the other modes must remain held-out predictions. If both chi and R are unknown, every frequency sees only chi/R: more frequencies of the same ideal family do not identify them separately. Independent geometry or additional transfer data are necessary. In reverse reconstruction, keep the full Jacobian and its null space; in forward synthesis, predict another mode, phase or linewidth. Never insert a free constant solely to force agreement.

## The mystical material, with provenance

[Newton's Keynes MS.28](https://webapp1.dlib.indiana.edu/newton/mss/norm/ALCH00017), English translation on ff.2r–2v, preserves the Emerald Tablet's above/below correspondence and cycles of separation and recombination. This is Newton's transcription/translation of a Hermetic text attributed to Hermes, not a measured Newtonian scale-equivalence theorem. Its Latin commentary was located but not fully translated in this review. A modern use is to ask whether two descriptions have an actual intertwining map and a controlled remainder. The P1/P2 failures and AA closure proof show why a metaphor alone cannot supply that map.

[Newton's experimental notebook ALCH00109](https://newton.dlib.indiana.edu/text/ALCH00109/normalized), December 1678, records weights, residues and failed mixtures. The reusable lesson is to retain a quantitative ledger and negative outcomes. [The 1729 General Scholium translation](https://www.newtonproject.ox.ac.uk/view/texts/normalized/NATP00056) contains theology and a speculative subtle spirit, while acknowledging inadequate experiments for its laws. Do not turn that speculation into an established field or mass parameter. [Mythology notes TRAN00013](https://www.newtonproject.ox.ac.uk/view/texts/normalized/TRAN00013) include copied ancient authorities; copied material and Newton's own assertions require different attribution.

[Vivekananda's letter to E.T. Sturdy, 13 February 1896](https://www.ramakrishnavivekananda.info/vivekananda/volume_5/epistles_first_series/057_blessed_and_beloved.htm), reports Tesla's interest in prana, akasha and kalpas and an anticipated mathematical demonstration. The letter supplies no completed derivation. Vedanta is the appropriate cultural context; it should not be collapsed into Western occultism. A unifying idea can motivate a common-variable hypothesis, but its physical map, dimensions and falsifier must be supplied separately. No authenticated 3–6–9 cosmological equation is established by these sources.

## Relevant modern methods, checked scope

| Primary source | Inspected contribution | How to use it here | Remaining boundary |
|---|---|---|---|
| [Koloskov, Hayakawa, Nickolaenko, 18 Sep 2026](https://angeo.copernicus.org/articles/44/949/2026/) | Introduction and calibration/conclusion passages distinguish forced spectral peaks from eigenfrequencies and use paired electric/magnetic or mode information | Reserve multiple independent observables when reconstructing hidden variables | Station/model-dependent calibration; not universal frequency numerology |
| [Bozóki et al., 2025](https://doi.org/10.1029/2025JD043989) | Conclusions compare analytical and FDTD spectra for impulse and continuing-current sources | Include driver duration as a separate source variable and check predicted spectral shape | Model comparison is not proof that one fitted parameter uniquely identifies nature |
| [Ciavarella, Burbano, Bauer, 2503.11888v2](https://arxiv.org/html/2503.11888v2) | Local Krylov/large-Nc truncations and SU(3) numerical tests | Inform AC basis construction and resource questions | Their truncation assumptions do not certify this SU(2) remainder or a continuum gap |
| [Jakobs et al., 2503.03397v1](https://arxiv.org/html/2503.03397v1) | SU(2) partitioning, Gauss penalty and single-plaquette weak-coupling study | Compare representation choices on matched finite problems | Single-plaquette cost claims do not establish large-volume continuum convergence |
| [Nachtergaele–Sims, 1410.8174v1](https://arxiv.org/abs/1410.8174) | Bounded strong evolution framework, inherited Y2 reading | Justify vectorwise integration before estimating its primitive | AA's source-specific separation and reducing-space proof remain additional project arguments |
| [Jaffe–Witten official problem](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf) | Section 4 and constructive-method obligations | Keep the intended continuum theory, axioms, physical scales and positive gap in view | Fixed-spacing or finite-sector success does not establish that construction |

Searches were targeted, not an exhaustive priority review. Not every new preprint or historical manuscript was read. The [Clay problem page](https://www.claymath.org/millennium/yang-mills-the-maths-gap/) still describes the mass-gap proof as unknown at this review date. Project novelty means a new derivation or certificate in this workbench; scientific priority remains unverified.
